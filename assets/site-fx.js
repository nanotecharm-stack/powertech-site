/* ══════════════════════════════════════════════════════════════
   PowerTech — section choreography ("everything is measured")
   Shared by all three language pages. No dependencies.

   1. Side rail — a fixed measurement-scale navigation on the right
      (desktop only), built from the header nav so labels localise.
   2. Draw-on-scroll — signal SVGs (parameter sparklines, the report
      voltage curve, the 7-day timeline) draw themselves when they
      enter the viewport; dashed guides fade, event dots pop.
   3. Count-ups — section indices tick from 00, the big "7" counts up.
   4. About photo — quiet scroll parallax inside its frame.

   Everything is progressive enhancement: without JS / IO / with
   prefers-reduced-motion nothing is hidden and nothing moves.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var reduced = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  /* ── 1. Side rail ─────────────────────────────────────────── */
  (function rail() {
    var navLinks = document.querySelectorAll('.nav-links a');
    var navEl = document.querySelector('.nav-links');
    if (!navLinks.length || document.querySelector('.side-rail')) return;
    var rail = document.createElement('nav');
    rail.className = 'side-rail';
    rail.setAttribute('aria-label', (navEl && navEl.getAttribute('aria-label')) || 'Sections');
    var targets = [];
    Array.prototype.forEach.call(navLinks, function (a, i) {
      var id = (a.getAttribute('href') || '').replace('#', '');
      var sec = id && document.getElementById(id);
      if (!sec) return;
      var item = document.createElement('a');
      item.href = '#' + id;
      var n = i + 1;
      item.innerHTML = '<span class="sr-label">' + a.textContent + '</span><b class="sr-num">' +
        (n < 10 ? '0' + n : n) + '</b><i class="sr-tick" aria-hidden="true"></i>';
      rail.appendChild(item);
      targets.push({ el: sec, link: item });
    });
    if (!targets.length) return;
    document.body.appendChild(rail);

    if (hasIO) {
      var spy = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) targets.forEach(function (t) {
            t.link.classList.toggle('active', t.el === e.target);
          });
        });
      }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
      targets.forEach(function (t) { spy.observe(t.el); });

      /* hide the rail while the hero owns the screen — it must never sit
         on the oscilloscope traces; it settles in as section 01 arrives */
      var heroEl = document.querySelector('.hero');
      if (heroEl) {
        rail.classList.add('over-hero');
        new IntersectionObserver(function (es) {
          rail.classList.toggle('over-hero', es[0].isIntersecting);
        }, { rootMargin: '-32% 0px -32% 0px', threshold: 0 }).observe(heroEl);
      }

      /* invert the rail while it crosses the dark sections (hero, proc) */
      var darkState = [];
      var darkEls = document.querySelectorAll('.hero, .proc');
      var darkIO = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var i = Array.prototype.indexOf.call(darkEls, e.target);
          darkState[i] = e.isIntersecting;
        });
        var any = false;
        for (var i = 0; i < darkState.length; i++) if (darkState[i]) any = true;
        rail.classList.toggle('over-dark', any);
      }, { rootMargin: '-50% 0px -49% 0px', threshold: 0 });
      Array.prototype.forEach.call(darkEls, function (el) { darkIO.observe(el); });
    }
  }());

  /* Everything below is motion — bail out politely where it must
     stay still. Content is never hidden in that case. */
  if (reduced || !hasIO) return;

  /* Safety net: if IO exists but never delivers (broken/throttled env),
     finish every prepped animation so nothing stays hidden. IO always
     fires an initial callback per observed target, so a healthy observer
     marks itself alive within a tick of page load. */
  var pending = [];
  var ioAlive = false;
  setTimeout(function () {
    if (ioAlive) return;
    pending.forEach(function (fn) { fn(); });
    pending = [];
  }, 4000);

  /* ── 2. Draw-on-scroll helpers ────────────────────────────── */
  function prepDraw(el) {
    var L;
    try { L = el.getTotalLength(); } catch (e) { return false; }
    if (!L) return false;
    el.style.strokeDasharray = L + ' ' + (L + 2);
    el.style.strokeDashoffset = L;
    return true;
  }
  function runDraw(el, dur, delay) {
    el.style.transition = 'stroke-dashoffset ' + dur + 'ms cubic-bezier(.4,0,.2,1) ' + (delay || 0) + 'ms';
    el.style.strokeDashoffset = '0';
  }
  function finishDraw(el) {
    el.style.transition = 'none';
    el.style.strokeDashoffset = '0';
  }
  function prepFade(el) { el.classList.add('fx-hide'); }
  function runFade(el, delay) {
    el.style.transitionDelay = (delay || 0) + 'ms';
    el.classList.add('fx-in');
  }
  function prepPop(el) { el.classList.add('fx-dot'); }
  function runPop(el, delay) {
    el.style.transitionDelay = (delay || 0) + 'ms';
    el.classList.add('fx-in');
  }
  function finishFx(el) {
    el.style.transitionDelay = '0ms';
    el.classList.add('fx-in');
  }
  function onSeen(el, cb, threshold) {
    var io = new IntersectionObserver(function (es) {
      ioAlive = true;
      es.forEach(function (e) {
        if (e.isIntersecting) { io.unobserve(e.target); cb(); }
      });
    }, { threshold: threshold || 0.3 });
    io.observe(el);
  }

  /* a. Parameter sparklines — each module draws its signal when seen */
  Array.prototype.forEach.call(document.querySelectorAll('.pm-signal svg'), function (svg, mi) {
    var draws = [], fades = [], pops = [];
    Array.prototype.forEach.call(svg.querySelectorAll('path, line'), function (el) {
      if (el.getAttribute('stroke-dasharray')) { prepFade(el); fades.push(el); }
      else if (prepDraw(el)) draws.push(el);
    });
    Array.prototype.forEach.call(svg.querySelectorAll('circle'), function (el) {
      prepPop(el); pops.push(el);
    });
    var base = (mi % 3) * 130;   /* soft stagger for modules arriving together */
    var go = function () {
      fades.forEach(function (el) { runFade(el, base); });
      draws.forEach(function (el, i) { runDraw(el, 900, base + i * 160); });
      pops.forEach(function (el, i) { runPop(el, base + 480 + i * 120); });
    };
    pending.push(function () {
      draws.forEach(finishDraw); fades.forEach(finishFx); pops.forEach(finishFx);
    });
    onSeen(svg, go, 0.4);
  });

  /* b. Report chart — the 7-day curve draws, the sag event pops mid-way,
        then the event-log rows arrive */
  (function reportChart() {
    var chart = document.querySelector('.rep-chart svg');
    if (!chart) return;
    var curve = chart.querySelector('path[stroke="#1B1B1B"]');
    var evDot = chart.querySelector('circle[fill="#F25749"]');
    var evText = null, volts = null;
    Array.prototype.forEach.call(chart.querySelectorAll('text'), function (t) {
      if (t.getAttribute('fill') === '#F25749') evText = t;
      else if ((t.getAttribute('x') | 0) > 480 && (t.getAttribute('y') | 0) < 110) volts = t;
    });
    var evLine = chart.querySelector('line[stroke="#F25749"]');
    var doc = document.querySelector('.rep-doc');

    var haveCurve = curve && prepDraw(curve);
    if (doc) doc.classList.add('fx-armed');
    if (evDot) prepPop(evDot);
    if (evText) prepFade(evText);
    if (volts) prepFade(volts);
    if (evLine) prepFade(evLine);
    var go = function () {
      if (haveCurve) runDraw(curve, 2100, 150);
      /* the sag sits ~47% along the curve → the pen reaches it ≈ 1.1s in */
      if (evDot) runPop(evDot, 1150);
      if (evLine) runFade(evLine, 1250);
      if (evText) runFade(evText, 1350);
      if (volts) runFade(volts, 1900);
      if (doc) doc.classList.add('live');
    };
    pending.push(function () {
      if (haveCurve) finishDraw(curve);
      [evDot, evText, volts, evLine].forEach(function (el) { if (el) finishFx(el); });
      if (doc) doc.classList.add('live');
    });
    onSeen(chart, go, 0.35);
  }());

  /* c. 7-day timeline in the dark section — baseline draws, day ticks
        land one by one, the coral day-7 marker pops last */
  (function timeline() {
    var svg = document.querySelector('.proc-timeline svg');
    if (!svg) return;
    var lines = svg.querySelectorAll('line');
    if (!lines.length) return;
    var baseline = lines[0], coral = null, ticks = [];
    Array.prototype.forEach.call(lines, function (l, i) {
      if (i === 0) return;
      if ((l.getAttribute('stroke') || '').indexOf('F25749') > -1) coral = l;
      else ticks.push(l);
    });
    var dot = svg.querySelector('circle');
    var haveBase = prepDraw(baseline);
    ticks.forEach(prepFade);
    if (coral) prepFade(coral);
    if (dot) prepPop(dot);
    var go = function () {
      if (haveBase) runDraw(baseline, 900, 0);
      ticks.forEach(function (l, i) { runFade(l, 250 + i * 110); });
      if (coral) runFade(coral, 250 + ticks.length * 110 + 80);
      if (dot) runPop(dot, 250 + ticks.length * 110 + 200);
    };
    pending.push(function () {
      if (haveBase) finishDraw(baseline);
      ticks.forEach(finishFx);
      if (coral) finishFx(coral);
      if (dot) finishFx(dot);
    });
    onSeen(svg, go, 0.5);
  }());

  /* ── 3. Count-ups ─────────────────────────────────────────── */
  function countUp(el, from, to, dur, fmt) {
    var t0 = null;
    function step(now) {
      if (t0 === null) t0 = now;
      var p = Math.min(1, (now - t0) / dur);
      var eased = 1 - Math.pow(1 - p, 2.2);
      el.textContent = fmt(Math.round(from + (to - from) * eased));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  /* section indices: 01…06 tick in from 00 */
  Array.prototype.forEach.call(
    document.querySelectorAll('.s02-idx, .obj-idx, .proc-idx, .params-idx, .report-idx, .appr-idx'),
    function (el) {
      var n = parseInt(el.textContent, 10);
      if (!n) return;
      onSeen(el, function () {
        countUp(el, 0, n, 520, function (v) { return v < 10 ? '0' + v : '' + v; });
      }, 0.6);
    });
  /* the big "7" counts its days */
  (function seven() {
    var el = document.querySelector('.proc-7');
    if (!el || el.textContent.trim() !== '7') return;
    onSeen(el, function () {
      countUp(el, 1, 7, 850, function (v) { return '' + v; });
    }, 0.6);
  }());

  /* ── 4. About photo parallax ──────────────────────────────── */
  (function aboutParallax() {
    if (innerWidth < 1000) return;
    var frame = document.querySelector('.about-photo');
    var img = frame && frame.querySelector('img');
    if (!img) return;
    img.classList.add('fx-parallax');
    var ticking = false;
    function apply() {
      ticking = false;
      var r = frame.getBoundingClientRect();
      var vh = innerHeight || 1;
      if (r.bottom < -60 || r.top > vh + 60) return;
      var p = ((r.top + r.height / 2) - vh / 2) / vh;   /* -0.5 … 0.5 */
      var y = Math.max(-1, Math.min(1, p * 2)) * -4;    /* ±4% */
      img.style.transform = 'translateY(' + y.toFixed(2) + '%) scale(1.09)';
    }
    addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }, { passive: true });
    apply();
  }());
}());
