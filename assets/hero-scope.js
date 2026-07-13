/* ══════════════════════════════════════════════════════════════
   PowerTech — Hero "live measurement" scene
   A hand-rolled canvas oscilloscope: three phase traces with a
   slowly-evolving harmonic mix, occasional grid events (voltage
   sags / THD bursts) flagged with coral markers, a measurement
   cursor that follows the pointer, and HUD readouts that tick in
   sync with the signal. Pauses off-screen and in hidden tabs;
   renders a single static frame under prefers-reduced-motion.
   No dependencies. Shared by all three language pages.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var hero = document.querySelector('.hero');
  var canvas = document.querySelector('.hero-canvas');
  if (!hero || !canvas || !canvas.getContext) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePtr = window.matchMedia && matchMedia('(pointer: fine)').matches;

  hero.classList.add('scope-on'); /* hides the static CSS fallback waveform */

  var TAU = Math.PI * 2;
  var CORAL = '242,87,73';
  var UNIT = canvas.getAttribute('data-unit') || 'V';  /* per-language volt symbol */
  var W = 0, H = 0, narrow = false;

  function resize() {
    var r = hero.getBoundingClientRect();
    W = Math.max(1, Math.round(r.width));
    H = Math.max(1, Math.round(r.height));
    narrow = W < 700;
    var dpr = Math.min(window.devicePixelRatio || 1, narrow ? 1.5 : 2);
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  /* ── signal model ─────────────────────────────────────────── */
  function baseY()  { return H * (narrow ? 0.84 : 0.60); }
  function ampl()   { return narrow ? Math.min(30, H * 0.05) : Math.min(64, H * 0.085); }
  var WL = 210;          /* px per cycle */
  var SPEED = 1.35;      /* rad/s drift */

  /* one active grid event at a time: a sag or a THD burst */
  var ev = null;         /* {x, t0, dur, depth, type, label} */
  var nextEvAt = 4.0;    /* first event a few seconds in */

  function scheduleEvent(t) {
    var sag = Math.random() < 0.6;
    var depth = sag ? (0.07 + Math.random() * 0.09) : (0.030 + Math.random() * 0.035);
    ev = {
      x: W * (narrow ? (0.25 + Math.random() * 0.5) : (0.60 + Math.random() * 0.30)),
      t0: t,
      dur: 2.6 + Math.random() * 1.4,
      depth: depth,
      type: sag ? 'sag' : 'thd',
      label: sag ? ('U↓ −' + (depth * 100).toFixed(1) + '%')
                 : ('THD ' + (2.3 + depth * 100).toFixed(1) + '%')
    };
    nextEvAt = t + ev.dur + 4.5 + Math.random() * 4.5;
    flashChip(sag ? 'u' : 'thd');
  }

  /* temporal envelope of the event: eases in, holds, eases out (0..1) */
  function evPhase(t) {
    if (!ev) return 0;
    var p = (t - ev.t0) / ev.dur;
    if (p <= 0 || p >= 1) return 0;
    return p < 0.25 ? p / 0.25 : (p > 0.7 ? (1 - p) / 0.3 : 1);
  }

  function wave(x, t, ph, kEnv) {
    var a = x * (TAU / WL) - t * SPEED + ph;
    var h3 = 0.10 + 0.05 * Math.sin(t * 0.23 + ph);
    var h5 = 0.045;
    var e = evPhase(t);
    if (ev && e > 0) {
      /* spatial reach of the disturbance around its marker */
      var dx = (x - ev.x) / 150;
      var g = Math.exp(-dx * dx) * e;
      if (ev.type === 'thd') { h3 += g * 0.35; h5 += g * 0.22; }
      else { kEnv *= 1 - g * ev.depth * 4.2; }
    }
    var v = Math.sin(a) + h3 * Math.sin(3 * a + t * 0.7) + h5 * Math.sin(5 * a - t * 0.4);
    return v * ampl() * kEnv * (1 + 0.05 * Math.sin(t * 0.6 + ph * 2));
  }

  /* stroke alpha ramps up left→right on wide screens so the traces
     never fight the text column; near-uniform on phones */
  function traceGradient(r, g, b, peak) {
    var gr = ctx.createLinearGradient(0, 0, W, 0);
    if (narrow) {
      gr.addColorStop(0, 'rgba(' + r + ',' + g + ',' + b + ',' + peak * 0.55 + ')');
      gr.addColorStop(0.5, 'rgba(' + r + ',' + g + ',' + b + ',' + peak * 0.85 + ')');
      gr.addColorStop(1, 'rgba(' + r + ',' + g + ',' + b + ',' + peak * 0.55 + ')');
    } else {
      /* stay invisible under the whole text column (~52% width), then ramp */
      gr.addColorStop(0.40, 'rgba(' + r + ',' + g + ',' + b + ',0)');
      gr.addColorStop(0.54, 'rgba(' + r + ',' + g + ',' + b + ',' + peak * 0.12 + ')');
      gr.addColorStop(0.72, 'rgba(' + r + ',' + g + ',' + b + ',' + peak * 0.6 + ')');
      gr.addColorStop(0.88, 'rgba(' + r + ',' + g + ',' + b + ',' + peak + ')');
      gr.addColorStop(1, 'rgba(' + r + ',' + g + ',' + b + ',' + peak * 0.92 + ')');
    }
    return gr;
  }

  function tracePath(t, ph, kEnv) {
    var y0 = baseY(), step = narrow ? 7 : 5;
    ctx.beginPath();
    for (var x = 0; x <= W + step; x += step) {
      var y = y0 + wave(x, t, ph, kEnv);
      x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
  }

  /* ── measurement cursor (desktop, fine pointers only) ─────── */
  var mouse = { x: -1, y: -1, in: false };
  var cur = { x: -1, a: 0 };  /* smoothed position + visibility */
  if (finePtr && !reduced) {
    hero.addEventListener('mousemove', function (e) {
      var r = hero.getBoundingClientRect();
      mouse.x = e.clientX - r.left;
      mouse.y = e.clientY - r.top;
      mouse.in = true;
    });
    hero.addEventListener('mouseleave', function () { mouse.in = false; });
  }

  function drawCursor(t) {
    var want = (mouse.in && mouse.x > W * 0.55) ? 1 : 0;
    cur.a += (want - cur.a) * 0.12;
    if (cur.a < 0.02) return;
    if (cur.x < 0) cur.x = mouse.x;
    cur.x += (mouse.x - cur.x) * 0.16;

    var y0 = baseY(), A = ampl();
    var yv = y0 + wave(cur.x, t, 0, 1);
    ctx.save();
    ctx.globalAlpha = cur.a;

    ctx.strokeStyle = 'rgba(255,255,255,.22)';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 5]);
    ctx.beginPath();
    ctx.moveTo(cur.x + 0.5, y0 - A * 1.9);
    ctx.lineTo(cur.x + 0.5, y0 + A * 1.9);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = 'rgba(' + CORAL + ',.95)';
    ctx.beginPath();
    ctx.arc(cur.x, yv, 3, 0, TAU);
    ctx.fill();
    ctx.strokeStyle = 'rgba(' + CORAL + ',.35)';
    ctx.beginPath();
    ctx.arc(cur.x, yv, 7, 0, TAU);
    ctx.stroke();

    var val = (230 + (wave(cur.x, t, 0, 1) / A) * 7.5).toFixed(1) + ' ' + UNIT;
    ctx.font = '10.5px "IBM Plex Mono", ui-monospace, Menlo, monospace';
    var tw = ctx.measureText(val).width;
    var bx = Math.min(cur.x + 12, W - tw - 22), by = yv - 26;
    chipRect(bx, by, tw + 14, 19);
    ctx.fillStyle = 'rgba(255,255,255,.9)';
    ctx.fillText(val, bx + 7, by + 13);
    ctx.restore();
  }

  function chipRect(x, y, w, h) {
    ctx.fillStyle = 'rgba(10,11,13,.78)';
    ctx.strokeStyle = 'rgba(255,255,255,.14)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, 3); else ctx.rect(x, y, w, h);
    ctx.fill();
    ctx.stroke();
  }

  /* ── event marker ─────────────────────────────────────────── */
  function drawEvent(t) {
    var e = evPhase(t);
    if (!ev || e <= 0) return;
    var y0 = baseY(), A = ampl();
    ctx.save();
    ctx.globalAlpha = Math.min(1, e * 1.4);

    ctx.strokeStyle = 'rgba(' + CORAL + ',.55)';
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(ev.x + 0.5, y0 - A * 2.1);
    ctx.lineTo(ev.x + 0.5, y0 + A * 2.1);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.fillStyle = 'rgba(' + CORAL + ',.9)';
    ctx.fillRect(ev.x - 2, y0 - A * 2.1 - 2, 4, 4);

    ctx.font = '10.5px "IBM Plex Mono", ui-monospace, Menlo, monospace';
    var tw = ctx.measureText(ev.label).width;
    var bx = Math.min(Math.max(8, ev.x - (tw + 14) / 2), W - tw - 22);
    var by = y0 - A * 2.1 - 30;
    chipRect(bx, by, tw + 14, 19);
    ctx.fillStyle = 'rgba(' + CORAL + ',.95)';
    ctx.fillText(ev.label, bx + 7, by + 13);
    ctx.restore();
  }

  /* ── axis ─────────────────────────────────────────────────── */
  function drawAxis() {
    var y0 = baseY();
    ctx.strokeStyle = 'rgba(255,255,255,.07)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, y0 + 0.5);
    ctx.lineTo(W, y0 + 0.5);
    ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.13)';
    ctx.beginPath();
    for (var x = 42; x < W; x += 84) {
      ctx.moveTo(x + 0.5, y0 - 3);
      ctx.lineTo(x + 0.5, y0 + 3);
    }
    ctx.stroke();
  }

  /* ── HUD readouts ─────────────────────────────────────────── */
  var chips = {};
  ['u', 'f', 'thd'].forEach(function (k) {
    var el = document.querySelector('[data-hud="' + k + '"]');
    if (el) chips[k] = { el: el, chip: el.closest('.hud-chip'), show: 0, target: 0 };
  });
  var HUD = {
    u:   { base: 230.0, jit: 1.6,  dp: 1, tick: 1.9 },
    f:   { base: 50.00, jit: 0.03, dp: 2, tick: 2.3 },
    thd: { base: 2.4,   jit: 0.5,  dp: 1, tick: 2.7 }
  };
  var hudNext = { u: 0, f: 0, thd: 0 };

  function hudInit() {
    for (var k in chips) {
      chips[k].show = chips[k].target = HUD[k].base;
      chips[k].el.textContent = HUD[k].base.toFixed(HUD[k].dp);
    }
  }
  function hudStep(t) {
    for (var k in chips) {
      var c = chips[k], cfg = HUD[k];
      if (t >= hudNext[k]) {
        c.target = cfg.base + (Math.random() * 2 - 1) * cfg.jit;
        hudNext[k] = t + cfg.tick * (0.7 + Math.random() * 0.6);
      }
      /* the sag pulls U down while it lasts */
      var goal = c.target;
      if (k === 'u' && ev && ev.type === 'sag') goal -= evPhase(t) * ev.depth * 230;
      if (k === 'thd' && ev && ev.type === 'thd') goal += evPhase(t) * ev.depth * 100;
      c.show += (goal - c.show) * 0.06;
      c.el.textContent = c.show.toFixed(cfg.dp);
    }
  }
  function flashChip(k) {
    var c = chips[k];
    if (!c || !c.chip) return;
    c.chip.classList.add('is-alert');
    setTimeout(function () { c.chip.classList.remove('is-alert'); }, 2400);
  }

  /* ── frame ────────────────────────────────────────────────── */
  var t0 = null, drawnIn = false;
  function frame(t) {
    ctx.clearRect(0, 0, W, H);

    /* entrance: traces sweep in from the left over ~1.6s */
    var p = Math.min(1, t / 1.6);
    if (p < 1) {
      var pe = 1 - Math.pow(1 - p, 3);
      ctx.save();
      ctx.beginPath();
      ctx.rect(0, 0, W * pe, H);
      ctx.clip();
    } else drawnIn = true;

    drawAxis();

    /* phases L2 / L3 — quiet grey companions */
    ctx.lineWidth = 1;
    ctx.strokeStyle = traceGradient(210, 220, 232, 0.30);
    tracePath(t, TAU / 3, 0.92); ctx.stroke();
    ctx.strokeStyle = traceGradient(210, 220, 232, 0.20);
    tracePath(t, TAU * 2 / 3, 0.85); ctx.stroke();

    /* phase L1 — the coral signature trace, with a soft glow */
    ctx.save();
    ctx.lineWidth = narrow ? 1.4 : 1.7;
    ctx.shadowColor = 'rgba(' + CORAL + ',.55)';
    ctx.shadowBlur = narrow ? 6 : 12;
    ctx.strokeStyle = traceGradient(242, 87, 73, narrow ? 0.9 : 0.95);
    tracePath(t, 0, 1); ctx.stroke();
    ctx.restore();

    drawEvent(t);
    if (!narrow) drawCursor(t);
    if (!drawnIn) ctx.restore();
  }

  /* ── loop control: pause when hidden / off-screen ─────────── */
  var inView = true, rafId = 0, running = false, tPrev = 0, tSim = 0;

  function loop(now) {
    if (!running) return;
    if (t0 === null) { t0 = now; tPrev = now; }
    var dt = Math.min(0.05, (now - tPrev) / 1000);
    tPrev = now;
    tSim += dt;
    if (tSim >= nextEvAt && (!ev || evPhase(tSim) === 0 && tSim > ev.t0 + ev.dur)) scheduleEvent(tSim);
    frame(tSim);
    hudStep(tSim);
    rafId = requestAnimationFrame(loop);
  }
  function setRunning(on) {
    if (on === running) return;
    running = on;
    if (on) { tPrev = performance.now(); rafId = requestAnimationFrame(loop); }
    else cancelAnimationFrame(rafId);
  }
  function evalRun() { setRunning(!reduced && inView && !document.hidden); }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en) {
      inView = en[0].isIntersecting;
      evalRun();
    }, { threshold: 0 }).observe(hero);
  }
  document.addEventListener('visibilitychange', evalRun);

  /* ── parallax + content fade on scroll (motion-ok only) ───── */
  var content = hero.querySelector('.hero-content');
  var fx = hero.querySelector('.hero-fx');
  if (!reduced && content) {
    var pxTick = false;
    var parallax = function () {
      pxTick = false;
      var sy = window.scrollY || 0;
      if (sy > H + 60) return;
      var k = Math.min(1, sy / Math.max(1, H));
      canvas.style.transform = 'translateY(' + (sy * 0.22).toFixed(1) + 'px)';
      content.style.transform = 'translateY(' + (sy * 0.10).toFixed(1) + 'px)';
      content.style.opacity = String(1 - k * 0.75);
      if (fx) fx.style.opacity = String(1 - k * 1.2);
    };
    window.addEventListener('scroll', function () {
      if (!pxTick) { pxTick = true; requestAnimationFrame(parallax); }
    }, { passive: true });
    parallax();
  }

  /* ── magnetic CTA buttons (fine pointers, motion-ok) ──────── */
  if (finePtr && !reduced) {
    Array.prototype.forEach.call(hero.querySelectorAll('.hero-actions .btn'), function (btn) {
      btn.classList.add('btn-mag');
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2);
        var dy = e.clientY - (r.top + r.height / 2);
        btn.style.transform = 'translate(' + (dx * 0.14).toFixed(1) + 'px,' + (dy * 0.22).toFixed(1) + 'px)';
      });
      btn.addEventListener('mouseleave', function () { btn.style.transform = ''; });
    });
  }

  /* ── boot ─────────────────────────────────────────────────── */
  resize();
  hudInit();
  if ('ResizeObserver' in window) {
    var ro = new ResizeObserver(function () {
      resize();
      if (reduced) frame(8);   /* re-render the static frame */
    });
    ro.observe(hero);
  } else {
    window.addEventListener('resize', function () { resize(); if (reduced) frame(8); });
  }

  if (reduced) {
    /* one calm, fully-drawn frame; no loop, no events, no cursor */
    drawnIn = true;
    frame(8);
  } else {
    /* paint one frame synchronously so the scene is never blank while the
       first rAF is pending (background tabs, throttled webviews) */
    frame(0.12);
    evalRun();
  }
}());
