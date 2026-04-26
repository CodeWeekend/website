/* ============================================================
   CodeWeekend — Main JS
   Sticky nav, animated stat counters, fade-in observers
   ============================================================ */

(function () {
  'use strict';

  // ---------- Sticky nav with backdrop blur on scroll ----------
  const navWrap = document.getElementById('navWrap');
  if (navWrap) {
    const onScroll = () => {
      if (window.scrollY > 8) navWrap.classList.add('scrolled');
      else navWrap.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ---------- Animated stat counters ----------
  const statNums = document.querySelectorAll('.stat__num[data-target]');
  if (statNums.length && 'IntersectionObserver' in window) {
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

  // ---------- Newsletter form (placeholder; redirects to external service) ----------
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const url = newsletterForm.dataset.formUrl;
      if (url) {
        window.open(url, '_blank', 'noopener,noreferrer');
      } else {
        alert('Newsletter signup is not yet configured.');
      }
    });
  }
})();
