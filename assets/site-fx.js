/* ══════════════════════════════════════════════════════════════
   PowerTech — side rail (fixed measurement-scale navigation).
   Shared by all three language pages. No dependencies.

   Since v8 this file owns ONLY the side rail: all scroll motion
   (draw-on-scroll signals, count-ups, parallax, reveals) moved to
   /assets/site-award.js, the GSAP choreography layer. The rail
   stays dependency-free so navigation works even if GSAP is ever
   missing. Content is never hidden here.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var hasIO = 'IntersectionObserver' in window;

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
         on the oscilloscope traces. Driven straight from the scroll
         handler (not an IntersectionObserver): during a fast jump to the
         top an observer fires a beat late and the rail flashed over the
         animation before fading. */
      var heroEl = document.querySelector('.hero');
      if (heroEl) {
        rail.classList.add('over-hero');
        var railTick = false;
        var updHero = function () {
          railTick = false;
          var vh = innerHeight || 1;
          /* hidden while the hero still covers the upper third band —
             the same window the old -32% rootMargin observer used */
          rail.classList.toggle('over-hero', heroEl.getBoundingClientRect().bottom > vh * 0.32);
        };
        addEventListener('scroll', function () {
          if (!railTick) { railTick = true; requestAnimationFrame(updHero); }
        }, { passive: true });
        addEventListener('resize', updHero);
        updHero();
      }

      /* …and again once the reader scrolls past "About" into the
         contact block / footer — the rail's job is done there */
      var endEls = document.querySelectorAll('.contact, .site-footer');
      if (endEls.length) {
        var endState = [];
        var endIO = new IntersectionObserver(function (es) {
          es.forEach(function (e) {
            var i = Array.prototype.indexOf.call(endEls, e.target);
            endState[i] = e.isIntersecting;
          });
          var any = false;
          for (var i = 0; i < endState.length; i++) if (endState[i]) any = true;
          rail.classList.toggle('over-end', any);
        }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 });
        Array.prototype.forEach.call(endEls, function (el) { endIO.observe(el); });
      }

      /* No dark-section color observer: tick/number colors invert per
         pixel via mix-blend-mode: difference in CSS, which also handles
         the rail straddling a section boundary. */
    }
  }());

  /* ── §02 industry slider — the typographic index drives the photo
        stage. Plain class toggling: CSS owns every transition, so it
        works identically with reduced motion (instant) and without
        GSAP. The first industry is pre-activated in the markup. ── */
  (function objectsSlider() {
    var items = Array.prototype.slice.call(document.querySelectorAll('.hs-item'));
    var imgs = Array.prototype.slice.call(document.querySelectorAll('.hs-img'));
    var caps = Array.prototype.slice.call(document.querySelectorAll('.hs-cap'));
    if (!items.length || items.length !== imgs.length) return;
    function setActive(n) {
      items.forEach(function (b, j) {
        b.classList.toggle('active', j === n);
        b.setAttribute('aria-selected', j === n ? 'true' : 'false');
      });
      imgs.forEach(function (im, j) { im.classList.toggle('active', j === n); });
      caps.forEach(function (c, j) { c.classList.toggle('active', j === n); });
    }
    items.forEach(function (btn, i) {
      btn.addEventListener('mouseenter', function () { setActive(i); });
      btn.addEventListener('focus', function () { setActive(i); });
      btn.addEventListener('click', function () { setActive(i); });
    });
  }());
}());
