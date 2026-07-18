/* ══════════════════════════════════════════════════════════════
   PowerTech — dependency-free interactions (no GSAP required).
   Shared by all three language pages.

   Owns the §02 industry slider. (The side measurement rail that
   used to live here was removed per user request 2026-07-14.)
   Content is never hidden here.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── §02 industry slider — the typographic index drives the photo
        stage. Plain class toggling: CSS owns every transition, so it
        works identically with reduced motion (instant) and without
        GSAP. The first industry is pre-activated in the markup.
        site-award.js can take the stage over (scanline sweep) via the
        pt:objslide event + the window.__ptSlider API. ── */
  (function objectsSlider() {
    var items = Array.prototype.slice.call(document.querySelectorAll('.hs-item'));
    var imgs = Array.prototype.slice.call(document.querySelectorAll('.hs-img'));
    var caps = Array.prototype.slice.call(document.querySelectorAll('.hs-cap'));
    if (!items.length || items.length !== imgs.length) return;
    var current = 0;
    function setActive(n, src) {
      n = ((n % items.length) + items.length) % items.length;
      if (n === current && src !== 'init') return;
      var prev = current;
      current = n;
      items.forEach(function (b, j) {
        b.classList.toggle('active', j === n);
        b.setAttribute('aria-selected', j === n ? 'true' : 'false');
      });
      imgs.forEach(function (im, j) { im.classList.toggle('active', j === n); });
      caps.forEach(function (c, j) { c.classList.toggle('active', j === n); });
      try {
        document.dispatchEvent(new CustomEvent('pt:objslide', { detail: { i: n, prev: prev, src: src || 'user' } }));
      } catch (e) { /* CustomEvent unsupported — switching still works */ }
    }
    items.forEach(function (btn, i) {
      btn.addEventListener('mouseenter', function () { setActive(i); });
      btn.addEventListener('focus', function () { setActive(i); });
      btn.addEventListener('click', function () { setActive(i); });
    });
    /* arrow keys walk the index (focus triggers activation) */
    var list = document.querySelector('.hs-list');
    if (list) {
      list.addEventListener('keydown', function (e) {
        var d = (e.key === 'ArrowDown' || e.key === 'ArrowRight') ? 1 :
                (e.key === 'ArrowUp' || e.key === 'ArrowLeft') ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        items[((current + d) % items.length + items.length) % items.length].focus();
      });
    }
    /* touch: swipe on the stage flips industries */
    var stage = document.querySelector('.hs-stage');
    if (stage) {
      var x0 = null;
      stage.addEventListener('touchstart', function (e) {
        x0 = e.touches[0].clientX;
      }, { passive: true });
      stage.addEventListener('touchend', function (e) {
        if (x0 === null) return;
        var dx = e.changedTouches[0].clientX - x0;
        x0 = null;
        if (Math.abs(dx) > 44) setActive(current + (dx < 0 ? 1 : -1), 'swipe');
      }, { passive: true });
    }
    window.__ptSlider = { go: setActive, count: items.length, index: function () { return current; } };
  }());

  /* ── Section instrument heads — after the H2 removal the eyebrow
        rows became full-width instrument bars: big tabular index,
        mono label, calibration ruler with a coral node, a running
        trace. Injected here (dependency-free) so they exist without
        GSAP and under reduced motion; site-award.js animates the
        entrance when motion is allowed. CSS defaults are the final
        state. Labels are read from the page's own eyebrow texts, so
        every language localises itself. ── */
  (function instrumentHeads() {
    var WAVE = '<svg class="ih-wave" viewBox="0 0 188 26" fill="none" aria-hidden="true">' +
      '<path d="M4 13 l8 -7 l8 11 l8 -9 l8 7 l8 -6 l8 5 l8 -8 l8 9 l8 -6 l8 4 l8 -5 l8 6 l8 -4 l8 3 l8 -5 l8 4 l8 -2 l8 1 h20"/></svg>';
    var DEFS = [
      { sel: '.proc', idx: '.proc-idx', eye: '.proc-eyebrow',
        host: function (sec) { var b = sec.querySelector('.proc-body'); return b && { p: b, before: b.firstElementChild }; } },
      { sel: '.objects', idx: '.obj-idx', eye: '.obj-eyebrow',
        host: function (sec) { var w = sec.querySelector('.sx-grid'); return w && { p: w.parentNode, before: w }; } },
      { sel: '.params', idx: '.params-idx', eye: '.params-eyebrow',
        host: function (sec) { var b = sec.querySelector('.params-body'); return b && { p: b, before: b.firstElementChild }; } },
      { sel: '.report', idx: '.report-idx', eye: '.report-eyebrow',
        host: function (sec) { var g = sec.querySelector('.report-grid'); return g && { p: g.parentNode, before: g }; } }
    ];
    var made = 0;
    DEFS.forEach(function (d) {
      var sec = document.querySelector(d.sel);
      if (!sec) return;
      var idxEl = sec.querySelector(d.idx);
      var eyeEl = sec.querySelector(d.eye);
      var h = d.host(sec);
      if (!idxEl || !eyeEl || !h) return;
      var ih = document.createElement('div');
      ih.className = 'ih';
      ih.setAttribute('aria-hidden', 'true');
      ih.innerHTML = '<b class="ih-idx">' + idxEl.textContent.trim() + '</b>' +
        '<span class="ih-label">' + eyeEl.textContent.trim() + '</span>' +
        '<span class="ih-rule"><i class="ih-node"></i></span>' + WAVE;
      h.p.insertBefore(ih, h.before);
      made++;
    });
    if (made) document.documentElement.classList.add('has-ih');
  }());

  /* ── Chrome on iOS (CriOS) only: on first load WKWebView mis-computes the
        root scroll bounds / fixed-element frame, which shows as phantom scroll
        space below the footer and a clipped "to-top" button. A real resize
        (lock/unlock, rotate) clears it — so we force one relayout after load.
        Strictly CriOS-gated: Safari iOS and all desktop browsers are untouched,
        so the iOS address-bar auto-hide for the Safari majority is preserved. ── */
  (function iosChromeReflowFix() {
    var ua = navigator.userAgent || '';
    if (ua.indexOf('CriOS') === -1) return;          // Chrome on iOS only
    document.documentElement.classList.add('is-crios');
    function relayout() {
      var d = document.documentElement;
      var prev = d.style.minHeight;
      // Nudge the document height by 1px, then restore next frame. The set/reset
      // pair forces the same scroll-bounds recompute a manual resize triggers.
      d.style.minHeight = (window.innerHeight + 1) + 'px';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { d.style.minHeight = prev; });
      });
    }
    window.addEventListener('load', function () { setTimeout(relayout, 60); });
    window.addEventListener('orientationchange', function () { setTimeout(relayout, 220); });
    // Back/forward cache restore re-triggers the glitch
    window.addEventListener('pageshow', function (e) { if (e.persisted) relayout(); });
  }());
}());
