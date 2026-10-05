/* ============================================================
   CodeWeekend — Main JS
   Sticky nav, mobile menu, animated stat counters
   ============================================================ */

(function () {
  'use strict';

  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- Sticky nav: paper bar gains a hairline once scrolled ----------
  const navWrap = document.getElementById('navWrap');
  if (navWrap) {
    const onScroll = () => {
      if (window.scrollY > 8) navWrap.classList.add('scrolled');
      else navWrap.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ---------- Mobile menu: close on Escape, outside click, or link choice ----------
  const mobileNav = document.querySelector('.mobile-nav');
  if (mobileNav) {
    const summary = mobileNav.querySelector('summary');
    const close = (restoreFocus) => {
      if (!mobileNav.open) return;
      mobileNav.open = false;
      if (restoreFocus && summary) summary.focus();
    };
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close(true);
    });
    document.addEventListener('click', (e) => {
      if (!mobileNav.contains(e.target)) close(false);
    });
    mobileNav.querySelectorAll('.mobile-nav__links a').forEach((a) => {
      a.addEventListener('click', () => close(false));
    });
    if (summary) {
      const syncLabel = () => {
        summary.setAttribute('aria-label', mobileNav.open ? 'Close navigation menu' : 'Open navigation menu');
      };
      mobileNav.addEventListener('toggle', syncLabel);
      syncLabel();
    }
  }

  // ---------- Animated stat counters ----------
  const statNums = document.querySelectorAll('.stat__num[data-target]');
  if (statNums.length && 'IntersectionObserver' in window && !reduceMotion) {
    const animate = (el) => {
      const target = el.dataset.target || '0';
      const isFloat = target.includes('.');
      const numericTarget = parseFloat(target);
      if (isNaN(numericTarget)) {
        return;
      }
      const duration = 1400;
      const start = performance.now();
      const suffixEl = el.querySelector('.stat__suffix');
      const suffix = suffixEl ? suffixEl.outerHTML : '';
      const step = (now) => {
        const t = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - t, 3);
        const v = isFloat
          ? (numericTarget * eased).toFixed(1)
          : Math.round(numericTarget * eased);
        el.innerHTML = v + suffix;
        if (t < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    const seen = new WeakSet();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !seen.has(entry.target)) {
          seen.add(entry.target);
          animate(entry.target);
        }
      });
    }, { threshold: 0.5 });
    statNums.forEach((s) => observer.observe(s));
  }

})();
