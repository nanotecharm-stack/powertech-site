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

  /* count a small "01…06" index (or any integer) up from zero */
  function countUp(el, to, dur, pad) {
    var o = { v: 0 };
    ScrollTrigger.create({
      trigger: el, start: 'top 88%', once: true,
      onEnter: function () {
        gsap.to(o, {
          v: to, duration: dur, ease: 'power2.out',
          onUpdate: function () {
            var v = Math.round(o.v);
            el.textContent = pad && v < 10 ? '0' + v : '' + v;
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
      if (isHY) { rise(h, h, { y: 30 }); return; }
      var words = splitWords(h);
      if (!words.length) return;
      gsap.set(words, { yPercent: 112 });
      ScrollTrigger.create({
        trigger: h, start: 'top 86%', once: true,
        onEnter: function () {
          gsap.to(words, {
            yPercent: 0, duration: 0.85, ease: 'power4.out', stagger: 0.065,
            onComplete: function () { gsap.set(words, { clearProps: 'transform' }); }
          });
        }
      });
    });

  /* ── 2. Calibration rules — every section head gets "measured in":
        a tick ruler draws across the eyebrow row, a coral node lands ── */
  gsap.utils.toArray(
    '.s02-eyebrow-row, .obj-eyebrow-row, .proc-eyebrow-row, .params-eyebrow-row,' +
    '.report-eyebrow-row, .appr-eyebrow-row, .contact-eyebrow-row'
  ).forEach(function (row) {
    var rule = document.createElement('span');
    rule.className = 'aw-rule' + (row.closest('.proc, .appr') ? ' aw-rule-dark' : '');
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

  /* ── 3. Section index marks tick up from 00 ──────────────────── */
  gsap.utils.toArray('.s02-idx, .obj-idx, .proc-idx, .params-idx, .report-idx, .appr-idx')
    .forEach(function (el) {
      var n = parseInt(el.textContent, 10);
      if (n) countUp(el, n, 0.55, true);
    });

  /* ── 4. Intros / editorial paragraphs — quiet rise ───────────── */
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

  /* ── 6. Objects — the rows arrive with the same quiet staggered
        rise as the rest of the page; the illustrations keep their
        own load fade and stay untouched ───────────────────────── */
  batchRise('.obj-row', { y: 24, stagger: 0.1 });

  /* ── 7. Dark section — the signature: the week measures itself.
        Scrub-linked: the baseline draws, day ticks land one per
        scroll-step, the "7" counts the days, the coral marker pops ── */
  (function proc() {
    var sec = document.querySelector('.proc');
    if (!sec) return;
    var svg = sec.querySelector('.proc-timeline svg');
    var seven = sec.querySelector('.proc-7');
    var label = sec.querySelector('.proc-7-label');

    var tl = gsap.timeline({
      scrollTrigger: { trigger: sec, start: 'top 78%', end: 'top 22%', scrub: 0.5 }
    });

    if (label) {
      gsap.set(label, { autoAlpha: 0 });
      tl.to(label, { autoAlpha: 1, duration: 0.3 }, 0);
    }
    if (svg) {
      var lines = svg.querySelectorAll('line');
      var baseline = lines[0];
      var ticks = [], coral = null;
      Array.prototype.forEach.call(lines, function (l, i) {
        if (i === 0) return;
        if ((l.getAttribute('stroke') || '').indexOf('F25749') > -1) coral = l;
        else ticks.push(l);
      });
      var dot = svg.querySelector('circle');
      if (prepDraw(baseline)) tl.to(baseline, { strokeDashoffset: 0, duration: 1, ease: 'none' }, 0);
      ticks.forEach(function (t, i) {
        gsap.set(t, { autoAlpha: 0 });
        tl.to(t, { autoAlpha: 1, duration: 0.08 }, 0.12 + i * 0.14);
      });
      if (coral) {
        gsap.set(coral, { autoAlpha: 0 });
        tl.to(coral, { autoAlpha: 1, duration: 0.08 }, 1.02);
      }
      if (dot) {
        gsap.set(dot, { scale: 0, transformOrigin: '50% 50%' });
        tl.to(dot, { scale: 1, duration: 0.18, ease: 'back.out(3)' }, 1.06);
      }
    }
    if (seven && seven.textContent.trim() === '7') {
      var o = { d: 1 };
      tl.to(o, {
        d: 7, duration: 1.1, ease: 'none',
        onUpdate: function () { seven.textContent = '' + Math.round(o.d); }
      }, 0);
    }
    batchRise('.proc-point', { y: 26, stagger: 0.1 });
    rise('.proc-note', '.proc-note', { y: 16 });
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

  /* ── 10. Approach — the coral accent draws, principles line up,
        their ticks extend ─────────────────────────────────────── */
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

    mm.add('(min-width: 861px)', function () {
      var img = document.querySelector('.about-photo img');
      if (!img) return;
      gsap.fromTo(img,
        { yPercent: -4, scale: 1.1 },
        {
          yPercent: 4, scale: 1.1, ease: 'none',
          scrollTrigger: { trigger: '.about-photo', start: 'top bottom', end: 'bottom top', scrub: 0.6 }
        });
    });
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
