/* ══════════════════════════════════════════════════════════════
   PowerTech — award pass: GSAP scroll choreography.
   Shared by all three language pages. Requires gsap + ScrollTrigger
   (vendored in /assets/vendor/, loaded before this file).

   Concept — «измерительный проход»: the scroll IS the measurement.
   Signals draw themselves, the big "7" counts days with the reader's
   scroll, section heads get "calibrated" by a ruler line, object
   illustrations reveal like chart paper coming off a plotter.

   Progressive enhancement:
   · no JS / no gsap  → nothing is ever hidden (hiding happens only
     here, via gsap.set, right before a guaranteed reveal trigger);
   · prefers-reduced-motion → this whole file is a no-op;
   · no pinning, no scroll hijacking, ignoreMobileResize — the iOS
     collapsing toolbar behaviour stays untouched.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  if (!window.gsap || !window.ScrollTrigger) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  gsap.registerPlugin(ScrollTrigger);
  /* iOS address-bar show/hide fires resize — never re-layout triggers for it */
  ScrollTrigger.config({ ignoreMobileResize: true });

  var EASE = 'power3.out';
  var isHY = (document.documentElement.lang || '') === 'hy';
  var mm = gsap.matchMedia();

  /* ── helpers ──────────────────────────────────────────────── */

  function prepDraw(el) {
    var L;
    try { L = el.getTotalLength(); } catch (e) { return 0; }
    if (!L) return 0;
    el.style.strokeDasharray = L + ' ' + (L + 2);
    el.style.strokeDashoffset = L;
    return L;
  }

  /* one-shot rise: hide now, reveal (staggered) when the trigger enters */
  function rise(targets, trigger, vars) {
    var els = gsap.utils.toArray(targets);
    if (!els.length) return;
    vars = vars || {};
    gsap.set(els, { autoAlpha: 0, y: vars.y != null ? vars.y : 26 });
    ScrollTrigger.create({
      trigger: trigger || els[0],
      start: vars.start || 'top 84%',
      once: true,
      onEnter: function () {
        gsap.to(els, {
          autoAlpha: 1, y: 0,
          duration: vars.duration || 0.9,
          ease: EASE,
          stagger: vars.stagger != null ? vars.stagger : 0.08,
          onComplete: function () {
            /* give transforms back to CSS so hover states keep working */
            gsap.set(els, { clearProps: 'transform,opacity,visibility' });
          }
        });
      }
    });
  }

  /* batch rise for grids/lists — items reveal as each enters, staggered */
  function batchRise(selector, vars) {
    var els = gsap.utils.toArray(selector);
    if (!els.length) return;
    vars = vars || {};
    gsap.set(els, { autoAlpha: 0, y: vars.y != null ? vars.y : 30 });
    ScrollTrigger.batch(els, {
      start: 'top 86%',
      once: true,
      onEnter: function (batch) {
        gsap.to(batch, {
          autoAlpha: 1, y: 0,
          duration: 0.95, ease: EASE,
          stagger: vars.stagger != null ? vars.stagger : 0.1,
          onComplete: function () {
            gsap.set(batch, { clearProps: 'transform,opacity,visibility' });
          }
        });
      }
    });
  }

  /* ── 1. Headline reveals — words rise out of their own masks ── */
  /* Armenian compounds are long: HY falls back to a whole-block rise
     so no word ever refuses to wrap. */
  function splitWords(h) {
    var label = h.textContent.replace(/\s+/g, ' ').trim();
    var nodes = Array.prototype.slice.call(h.childNodes);
    var wrap = document.createElement('span');
    wrap.setAttribute('aria-hidden', 'true');
    var words = [];
    nodes.forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { wrap.appendChild(document.createTextNode(' ')); return; }
          var w = document.createElement('span'); w.className = 'aw-w';
          var i = document.createElement('span'); i.className = 'aw-wi';
          i.textContent = part;
          w.appendChild(i); wrap.appendChild(w); words.push(i);
        });
      } else {
        wrap.appendChild(n);
      }
    });
    h.textContent = '';
    h.setAttribute('aria-label', label);
    h.appendChild(wrap);
    return words;
  }

  gsap.utils.toArray('.s02-h2, .obj-h2, .params-h2, .report-h2, .appr-h2, .contact-h2')
    .forEach(function (h) {
      if (isHY) { rise(h, h, { y: 26, duration: 0.7 }); return; }
      var words = splitWords(h);
      if (!words.length) return;
      gsap.set(words, { yPercent: 112 });
      ScrollTrigger.create({
        trigger: h, start: 'top 88%', once: true,
        onEnter: function () {
          gsap.to(words, {
            /* quick: the text must never lag behind the reader */
            yPercent: 0, duration: 0.6, ease: 'power4.out', stagger: 0.045,
            onComplete: function () { gsap.set(words, { clearProps: 'transform' }); }
          });
        }
      });
    });

  /* ── 2. Calibration rules — light-section heads get "measured in":
        a tick ruler draws across the eyebrow row, a coral node lands.
        Dark sections (§03/§06) carry their own peaks and stay clean. ── */
  gsap.utils.toArray(
    '.s02-eyebrow-row, .obj-eyebrow-row, .params-eyebrow-row,' +
    '.report-eyebrow-row, .contact-eyebrow-row'
  ).forEach(function (row) {
    var rule = document.createElement('span');
    rule.className = 'aw-rule';
    rule.setAttribute('aria-hidden', 'true');
    var node = document.createElement('i');
    rule.appendChild(node);
    row.appendChild(rule);
    gsap.set(rule, { clipPath: 'inset(0 100% 0 0)' });
    gsap.set(node, { scale: 0, transformOrigin: '50% 50%' });
    ScrollTrigger.create({
      trigger: row, start: 'top 88%', once: true,
      onEnter: function () {
        gsap.to(rule, { clipPath: 'inset(0 0% 0 0)', duration: 1.05, ease: 'power2.inOut' });
        gsap.to(node, { scale: 1, duration: 0.5, delay: 0.85, ease: 'back.out(2.4)' });
      }
    });
  });

  /* ── 3. Intros / editorial paragraphs — quiet rise ───────────── */
  gsap.utils.toArray(
    '.s02-intro, .obj-intro, .params-intro, .report-intro, .proc-intro, .contact-intro'
  ).forEach(function (el) { rise(el, el, { y: 22 }); });
  rise('.appr-lead, .appr-p, .appr-note', '.appr-text', { y: 22, stagger: 0.12 });

  /* ── 5. Section 01 — the shared measurement line draws, the four
        scenarios thread onto it, their coral taps pop ─────────── */
  (function s02() {
    var map = document.querySelector('.s02-map');
    if (!map) return;
    var cards = map.querySelectorAll('.s02-trigger');
    gsap.set(map, { '--awline': 0 });
    Array.prototype.forEach.call(cards, function (c) { gsap.set(c, { '--awdot': 0 }); });
    batchRise(cards, { y: 34, stagger: 0.11 });
    ScrollTrigger.create({
      trigger: map, start: 'top 86%', once: true,
      onEnter: function () {
        gsap.to(map, { '--awline': 1, duration: 1.2, ease: 'power2.inOut' });
        gsap.to(cards, {
          '--awdot': 1, duration: 0.5, ease: 'back.out(2.4)',
          stagger: 0.22, delay: 0.25
        });
      }
    });
  }());

  /* ── 6. Objects — the industry index rises row by row, the photo
        stage fades in beside it (switching lives in site-fx.js) ── */
  batchRise('.hs-item', { y: 16, stagger: 0.07 });
  (function objectsStage() {
    var stage = document.querySelector('.hs-stage');
    if (!stage) return;
    gsap.set(stage, { autoAlpha: 0, y: 20 });
    ScrollTrigger.create({
      trigger: stage, start: 'top 86%', once: true,
      onEnter: function () {
        gsap.to(stage, {
          autoAlpha: 1, y: 0, duration: 0.9, ease: EASE,
          onComplete: function () { gsap.set(stage, { clearProps: 'transform,opacity,visibility' }); }
        });
      }
    });
  }());

  /* ── 6b. Objects, award layer — the stage becomes an instrument:
        every photo is "scanned in" by a coral sweep line (the
        oscilloscope beam), a mono counter flips in the corner, and
        until the visitor takes over the section quietly walks the
        industries by itself. Whole file is a no-op under reduced
        motion; the CSS clip transitions in style.css remain the
        fallback when this layer is absent. ── */
  (function objectsAward() {
    var stage = document.querySelector('.hs-stage');
    var api = window.__ptSlider;
    if (!stage || !api) return;
    var imgs = gsap.utils.toArray(stage.querySelectorAll('.hs-img'));
    if (!imgs.length) return;
    stage.classList.add('hs-anim');   /* CSS transitions off — GSAP owns the stage */

    var scan = document.createElement('div');
    scan.className = 'hs-scan';
    scan.setAttribute('aria-hidden', 'true');
    stage.appendChild(scan);
    var count = document.createElement('div');
    count.className = 'hs-count';
    count.setAttribute('aria-hidden', 'true');
    count.innerHTML = '<b>01</b><span>/ 0' + api.count + '</span>';
    stage.appendChild(count);
    gsap.set(scan, { autoAlpha: 0 });

    var FULL = 'polygon(0 0, 100% 0, 100% 100%, 0 100%)';
    var HID = 'polygon(0 0, 100% 0, 100% 0, 0 0)';
    var prev = -1;

    /* Independent tweens with overwrite:'auto' — no timelines and no
       deferred cleanup. The outgoing photo simply stays FULL beneath
       the incoming one (opaque cover-fit), so a rapid hover chain has
       nothing to race against. */
    function sweep(i) {
      var img = imgs[i];
      if (!img) return;
      imgs.forEach(function (im, j) {
        /* photo layers live at 0-2; scrim/captions/instruments sit above (3+) */
        gsap.set(im, { zIndex: j === i ? 2 : (j === prev ? 1 : 0) });
      });
      prev = i;
      gsap.fromTo(img,
        { clipPath: HID, scale: 1.06, transformOrigin: '50% 0%' },
        { clipPath: FULL, scale: 1, duration: 0.9, ease: 'power2.inOut', overwrite: 'auto' });
      gsap.killTweensOf(scan);
      gsap.fromTo(scan, { top: 0, autoAlpha: 1 },
        { top: '100%', duration: 0.9, ease: 'power2.inOut', overwrite: 'auto' });
      gsap.to(scan, { autoAlpha: 0, duration: 0.22, delay: 0.8, overwrite: false });
      var b = count.querySelector('b');
      if (b) {
        gsap.killTweensOf(b);
        gsap.to(b, {
          yPercent: -60, autoAlpha: 0, duration: 0.16, ease: 'power2.in', overwrite: 'auto',
          onComplete: function () {
            b.textContent = '0' + (i + 1);
            gsap.fromTo(b, { yPercent: 60, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 0.22, ease: 'power2.out' });
          }
        });
      }
    }
    document.addEventListener('pt:objslide', function (e) { sweep(e.detail.i); });

    /* entrance: the first photo is scanned in as the stage arrives */
    ScrollTrigger.create({
      trigger: stage, start: 'top 80%', once: true,
      onEnter: function () { sweep(api.index()); }
    });

    /* quiet self-demo: advance every ~5s while the section is on
       screen, stop forever at the visitor's first own interaction */
    var stopped = false, timer = null, inView = false;
    function ensureTimer() {
      if (inView && !stopped && !timer) {
        timer = setInterval(function () { api.go(api.index() + 1, 'auto'); }, 5200);
      }
      if ((!inView || stopped) && timer) {
        clearInterval(timer);
        timer = null;
      }
    }
    document.addEventListener('pt:objslide', function (e) {
      if (e.detail.src !== 'auto' && e.detail.src !== 'init') { stopped = true; ensureTimer(); }
    });
    ScrollTrigger.create({
      trigger: stage, start: 'top 78%', end: 'bottom 12%',
      onToggle: function (st) { inView = st.isActive; ensureTimer(); }
    });
  }());

  /* ── 7. Dark section — the signature scene: the week measures itself.
        Desktop: the section PINS and the visitor's scroll plays the
        week Д1→Д7 — the baseline draws, day ticks + labels land, the
        "7" counts, the two report events (Д3 dip, Д6 THD) flag
        themselves, the four points file in, the coral marker closes
        the week. Touch/small screens keep the old non-pinned scrub —
        no pinning ever happens there (iOS toolbar stays untouched). ── */
  (function proc() {
    var sec = document.querySelector('.proc');
    if (!sec) return;
    var svg = sec.querySelector('.proc-timeline svg');
    var seven = sec.querySelector('.proc-7');
    var label = sec.querySelector('.proc-7-label');
    var els = {
      base: svg && svg.querySelector('.pt-base'),
      ticks: svg ? gsap.utils.toArray(svg.querySelectorAll('.pt-tick')) : [],
      days: svg ? gsap.utils.toArray(svg.querySelectorAll('.pt-day')) : [],
      evs: svg ? gsap.utils.toArray(svg.querySelectorAll('.pt-ev')) : [],
      t7: svg && svg.querySelector('.pt-t7'),
      dot: svg && svg.querySelector('.pt-dot')
    };

    /* the week plays into tl; DAY(i) = position when day i (1..7) lands */
    function playWeek(tl) {
      var STEP = 0.22, T0 = 0.16;
      function DAY(i) { return T0 + (i - 1) * STEP; }
      if (label) {
        gsap.set(label, { autoAlpha: 0 });
        tl.to(label, { autoAlpha: 1, duration: 0.25 }, 0);
      }
      if (els.base && prepDraw(els.base)) {
        tl.to(els.base, { strokeDashoffset: 0, duration: DAY(7) - 0.04, ease: 'none' }, 0.04);
      }
      els.ticks.forEach(function (t, i) {           /* ticks = Д1..Д6 */
        gsap.set(t, { autoAlpha: 0 });
        tl.to(t, { autoAlpha: 1, duration: 0.07 }, DAY(i + 1));
      });
      els.days.forEach(function (d, i) {            /* labels Д1..Д7 */
        gsap.set(d, { autoAlpha: 0 });
        tl.to(d, { autoAlpha: 1, duration: 0.09 }, DAY(i + 1) + 0.03);
      });
      els.evs.forEach(function (g, i) {             /* events at Д3 / Д6 */
        gsap.set(g, { autoAlpha: 0, y: -3 });
        tl.to(g, { autoAlpha: 1, y: 0, duration: 0.12, ease: 'power2.out' }, DAY(i === 0 ? 3 : 6) + 0.08);
      });
      if (els.t7) {
        gsap.set(els.t7, { autoAlpha: 0 });
        tl.to(els.t7, { autoAlpha: 1, duration: 0.07 }, DAY(7));
      }
      if (els.dot) {
        gsap.set(els.dot, { scale: 0, transformOrigin: '50% 50%' });
        tl.to(els.dot, { scale: 1, duration: 0.16, ease: 'back.out(3)' }, DAY(7) + 0.04);
      }
      if (seven && seven.textContent.trim() === '7') {
        var o = { d: 1 };
        tl.to(o, {
          d: 7, duration: DAY(7) - DAY(1), ease: 'none',
          onUpdate: function () { seven.textContent = '' + Math.round(o.d); }
        }, DAY(1));
      }
      return DAY(7);
    }

    mm.add('(min-width: 981px) and (hover: hover) and (pointer: fine)', function () {
      /* desktop: pin the plate and let the scroll play the whole week */
      sec.classList.add('is-pinned');
      var tl = gsap.timeline({
        scrollTrigger: {
          trigger: sec, start: 'top top', end: '+=130%',
          pin: true, scrub: 0.55, anticipatePin: 1
        }
      });
      var d7 = playWeek(tl);
      var points = gsap.utils.toArray(sec.querySelectorAll('.proc-point'));
      points.forEach(function (p, i) {
        gsap.set(p, { autoAlpha: 0, y: 26 });
        tl.to(p, { autoAlpha: 1, y: 0, duration: 0.26, ease: 'power2.out' }, 0.28 + i * 0.36);
      });
      var note = sec.querySelector('.proc-note');
      if (note) {
        gsap.set(note, { autoAlpha: 0, y: 14 });
        tl.to(note, { autoAlpha: 1, y: 0, duration: 0.22 }, d7 + 0.1);
      }
      tl.to({}, { duration: 0.28 });   /* rest: the finished week holds before unpin */
      return function () {
        sec.classList.remove('is-pinned');
        gsap.set(sec.querySelectorAll('.proc-point, .proc-note'), { clearProps: 'all' });
      };
    });

    mm.add('(max-width: 980.98px), (hover: none), (pointer: coarse)', function () {
      /* touch / narrow: the week plays as the section crosses the viewport */
      var tl = gsap.timeline({
        scrollTrigger: { trigger: sec, start: 'top 78%', end: 'top 22%', scrub: 0.5 }
      });
      playWeek(tl);
      batchRise('.proc-point', { y: 26, stagger: 0.1 });
      rise('.proc-note', '.proc-note', { y: 16 });
    });
  }());

  /* ── 8. Parameters — each module arrives, then its signal trace
        draws itself: guides fade in, the pen runs, event dots pop ── */
  (function params() {
    batchRise('.param-module', { y: 30, stagger: 0.09 });
    gsap.utils.toArray('.pm-signal svg').forEach(function (svg, mi) {
      var draws = [], fades = [], pops = [];
      Array.prototype.forEach.call(svg.querySelectorAll('path, line'), function (el) {
        if (el.getAttribute('stroke-dasharray')) { gsap.set(el, { autoAlpha: 0 }); fades.push(el); }
        else if (prepDraw(el)) draws.push(el);
      });
      Array.prototype.forEach.call(svg.querySelectorAll('circle'), function (el) {
        gsap.set(el, { scale: 0, transformOrigin: '50% 50%' }); pops.push(el);
      });
      var base = (mi % 2) * 0.15;
      ScrollTrigger.create({
        trigger: svg, start: 'top 88%', once: true,
        onEnter: function () {
          if (fades.length) gsap.to(fades, { autoAlpha: 1, duration: 0.6, delay: base });
          draws.forEach(function (el, i) {
            gsap.to(el, { strokeDashoffset: 0, duration: 0.95, delay: base + 0.1 + i * 0.18, ease: 'power2.inOut' });
          });
          if (pops.length) gsap.to(pops, { scale: 1, duration: 0.45, delay: base + 0.6, stagger: 0.1, ease: 'back.out(2.6)' });
        }
      });
    });
  }());

  /* ── 9. Report — the document settles onto the desk; the 7-day
        curve is drawn by the reader's own scroll, the sag event and
        its log land as the pen passes them ─────────────────────── */
  (function report() {
    batchRise('.rep-item', { y: 22, stagger: 0.09 });
    rise('.report-instrument', '.report-instrument', { y: 16 });

    var fig = document.querySelector('.report-right');
    var doc = document.querySelector('.rep-doc');
    if (!fig || !doc) return;
    rise(doc, fig, { y: 44, duration: 1.05 });

    var chart = doc.querySelector('.rep-chart svg');
    if (chart) {
      var curve = chart.querySelector('path[stroke="#1B1B1B"]');
      var evDot = chart.querySelector('circle[fill="#F25749"]');
      var evLine = chart.querySelector('line[stroke="#F25749"]');
      var evText = null, volts = null;
      Array.prototype.forEach.call(chart.querySelectorAll('text'), function (t) {
        if (t.getAttribute('fill') === '#F25749') evText = t;
        else if ((t.getAttribute('x') | 0) > 480 && (t.getAttribute('y') | 0) < 110) volts = t;
      });
      var tl = gsap.timeline({
        scrollTrigger: { trigger: fig, start: 'top 74%', end: 'top 22%', scrub: 0.5 }
      });
      if (curve && prepDraw(curve)) tl.to(curve, { strokeDashoffset: 0, duration: 1, ease: 'none' }, 0);
      /* the sag sits ~47% along the curve — the pen reaches it there */
      if (evDot) { gsap.set(evDot, { scale: 0, transformOrigin: '50% 50%' }); tl.to(evDot, { scale: 1, duration: 0.1, ease: 'back.out(3)' }, 0.47); }
      if (evLine) { gsap.set(evLine, { autoAlpha: 0 }); tl.to(evLine, { autoAlpha: 1, duration: 0.1 }, 0.5); }
      if (evText) { gsap.set(evText, { autoAlpha: 0 }); tl.to(evText, { autoAlpha: 1, duration: 0.12 }, 0.53); }
      if (volts) { gsap.set(volts, { autoAlpha: 0 }); tl.to(volts, { autoAlpha: 1, duration: 0.12 }, 0.9); }
    }
    var evs = doc.querySelectorAll('.rep-events .rep-ev');
    if (evs.length) {
      gsap.set(evs, { autoAlpha: 0, x: -10 });
      ScrollTrigger.create({
        trigger: doc.querySelector('.rep-events'), start: 'top 90%', once: true,
        onEnter: function () {
          gsap.to(evs, { autoAlpha: 1, x: 0, duration: 0.6, ease: EASE, stagger: 0.12, delay: 0.35 });
        }
      });
    }
    /* desktop: the sheet drifts a touch slower than the page — paper on a desk */
    mm.add('(min-width: 981px)', function () {
      gsap.fromTo(doc, { y: 26 }, {
        y: -26, ease: 'none',
        scrollTrigger: { trigger: fig, start: 'top bottom', end: 'bottom top', scrub: 0.8 }
      });
    });
  }());

  /* ── 10. Approach — the coral accent draws, principles line up as a
        measurement chain: the row line draws itself across, then the
        coral ticks land one per principle ─────────────────────── */
  (function appr() {
    var accent = document.querySelector('.appr-accent');
    if (accent) {
      gsap.set(accent, { scaleX: 0, transformOrigin: '0 50%' });
      ScrollTrigger.create({
        trigger: accent, start: 'top 88%', once: true,
        onEnter: function () { gsap.to(accent, { scaleX: 1, duration: 0.9, ease: 'power2.inOut' }); }
      });
    }
    batchRise('.appr-principle', { y: 26, stagger: 0.12 });

    /* chain only where the principles share one row line (>700px) */
    mm.add('(min-width: 701px)', function () {
      var row = document.querySelector('.appr-principles');
      if (!row) return;
      var line = document.createElement('span');
      line.className = 'appr-chainline';
      line.setAttribute('aria-hidden', 'true');
      row.classList.add('fx-chain');
      row.appendChild(line);
      gsap.set(line, { clipPath: 'inset(0 100% 0 0)' });
      var ticks = gsap.utils.toArray(row.querySelectorAll('.appr-principle'));
      ticks.forEach(function (p) { gsap.set(p, { '--aptick': 0 }); });
      ScrollTrigger.create({
        trigger: row, start: 'top 84%', once: true,
        onEnter: function () {
          gsap.to(line, { clipPath: 'inset(0 0% 0 0)', duration: 1.15, ease: 'power2.inOut' });
          gsap.to(ticks, { '--aptick': 1, duration: 0.5, ease: 'power2.out', stagger: 0.22, delay: 0.3 });
        }
      });
      return function () {
        row.classList.remove('fx-chain');
        line.remove();
      };
    });
  }());

  /* ── 11. About — the engineering sheet settles, the wordmark rises
        out of its baseline, the photo breathes with the scroll ──── */
  (function about() {
    var panel = document.querySelector('.about-panel');
    if (!panel) return;
    rise(panel, panel, { y: 40, duration: 1.05 });

    var wm = panel.querySelector('.about-wordmark');
    if (wm) {
      var wmWrap = document.createElement('span');
      wmWrap.className = 'aw-w';
      wmWrap.setAttribute('aria-hidden', 'true');
      var inner = document.createElement('span');
      inner.className = 'aw-wi';
      while (wm.firstChild) inner.appendChild(wm.firstChild);
      wmWrap.appendChild(inner);
      wm.setAttribute('aria-label', inner.textContent);
      wm.appendChild(wmWrap);
      gsap.set(inner, { yPercent: 108 });
      ScrollTrigger.create({
        trigger: panel, start: 'top 72%', once: true,
        onEnter: function () {
          gsap.to(inner, { yPercent: 0, duration: 0.9, ease: 'power4.out', delay: 0.15 });
        }
      });
    }
    var baseline = panel.querySelector('.about-baseline');
    if (baseline) {
      gsap.set(baseline, { clipPath: 'inset(0 100% 0 0)' });
      ScrollTrigger.create({
        trigger: panel, start: 'top 72%', once: true,
        onEnter: function () {
          gsap.to(baseline, { clipPath: 'inset(0 0% 0 0)', duration: 1.1, delay: 0.35, ease: 'power2.inOut' });
        }
      });
    }
    rise(panel.querySelectorAll('.about-lead, .about-text'), panel, { y: 18, stagger: 0.12, start: 'top 70%' });
  }());

  /* ── 12. Contact — the request sheet assembles field by field ── */
  (function contact() {
    var form = document.querySelector('.contact-form');
    if (!form) return;
    rise(form, form, { y: 36, duration: 1 });
    var bits = form.querySelectorAll('.cf-field, .cf-submit');
    gsap.set(bits, { autoAlpha: 0, y: 14 });
    ScrollTrigger.create({
      trigger: form, start: 'top 78%', once: true,
      onEnter: function () {
        gsap.to(bits, {
          autoAlpha: 1, y: 0, duration: 0.6, ease: EASE, stagger: 0.07, delay: 0.3,
          onComplete: function () { gsap.set(bits, { clearProps: 'transform,opacity,visibility' }); }
        });
      }
    });
  }());

  /* ── 13. Footer — the closing pulse draws across, its coral node
        lands, the plate's columns settle ──────────────────────── */
  (function footer() {
    var foot = document.querySelector('.site-footer');
    if (!foot) return;
    var line = foot.querySelector('.f-pulse path');
    var dot = foot.querySelector('.f-pulse circle');
    var cols = foot.querySelectorAll('.f-brand, .f-contact, .f-nav');
    if (line && prepDraw(line)) {
      if (dot) gsap.set(dot, { scale: 0, transformOrigin: '50% 50%' });
      ScrollTrigger.create({
        trigger: foot, start: 'top 92%', once: true,
        onEnter: function () {
          gsap.to(line, { strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut' });
          if (dot) gsap.to(dot, { scale: 1, duration: 0.5, delay: 1.25, ease: 'back.out(3)' });
        }
      });
    }
    if (cols.length) rise(cols, foot, { y: 22, stagger: 0.13, start: 'top 88%' });
  }());

}());
