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
}());
