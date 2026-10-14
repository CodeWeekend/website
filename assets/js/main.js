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

  // ---------- Tabs (home: Bootcamp showcase, graduate voices) ----------
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-tabs]').forEach((root) => {
    const tabs = Array.from(root.querySelectorAll('[role="tab"]'));
    const panels = Array.from(root.querySelectorAll('[data-panel]'));
    if (!tabs.length) return;
    let current = Math.max(0, tabs.findIndex((t) => t.classList.contains('is-active')));

    const select = (i, focus) => {
      current = (i + tabs.length) % tabs.length;
      tabs.forEach((t, n) => {
        const on = n === current;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
      });
      panels.forEach((p) => p.classList.toggle('is-active', Number(p.dataset.panel) === current));
      if (focus) tabs[current].focus();
      const strip = tabs[current].parentElement;
      if (strip.scrollWidth > strip.clientWidth) {
        strip.scrollTo({ left: tabs[current].offsetLeft - 20, behavior: reduceMotion ? 'auto' : 'smooth' });
      }
    };

    const stopAutoplay = () => root.classList.remove('is-autoplay', 'is-playing');

    tabs.forEach((tab, i) => {
      tab.addEventListener('click', () => { stopAutoplay(); select(i); });
      tab.addEventListener('keydown', (e) => {
        const keys = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
        if (e.key in keys) { e.preventDefault(); stopAutoplay(); select(current + keys[e.key], true); }
        else if (e.key === 'Home') { e.preventDefault(); stopAutoplay(); select(0, true); }
        else if (e.key === 'End') { e.preventDefault(); stopAutoplay(); select(tabs.length - 1, true); }
      });
    });

    if (!root.hasAttribute('data-autoplay') || reduceMotion || !('IntersectionObserver' in window)) return;
    root.classList.add('is-autoplay');
    let visible = false;
    let hovering = false;
    let focused = false;
    const sync = () => root.classList.toggle('is-playing', root.classList.contains('is-autoplay') && visible && !hovering && !focused);
    root.addEventListener('mouseenter', () => { hovering = true; sync(); });
    root.addEventListener('mouseleave', () => { hovering = false; sync(); });
    root.addEventListener('focusin', () => { focused = true; sync(); });
    root.addEventListener('focusout', (e) => {
      focused = root.contains(e.relatedTarget);
      sync();
    });
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      sync();
    }, { threshold: 0.35 }).observe(root);
    root.addEventListener('animationend', (e) => {
      if (e.target.closest('.is-active') && e.target.parentElement.classList.contains('hm-show__progress') && root.classList.contains('is-autoplay')) {
        select(current + 1);
      }
    });
  });

  // ---------- Home hero: code editor types each graduate's capstone ----------
  document.querySelectorAll('[data-ide]').forEach((root) => {
    const code = root.querySelector('[data-ide-code]');
    const state = root.querySelector('[data-ide-state]');
    const picks = Array.from(root.querySelectorAll('[data-ide-pick]'));
    const apps = Array.from(root.querySelectorAll('.hm-ide__app img'));
    const credit = root.querySelector('.hm-ide__credit');
    const nameEl = root.querySelector('[data-ide-name]');
    const projectEl = root.querySelector('[data-ide-project]');
    const avatarEl = root.querySelector('[data-ide-avatar]');
    if (!code || picks.length < 2) return;

    const builds = picks.map((p) => ({ ...p.dataset }));
    const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const tokensFor = (b) => [
      ['c', '// Class of 2026 · Web & AI Bootcamp'], ['', '\n'],
      ['k', 'const'], ['', ' developer = '], ['s', `"${b.name}"`], ['', ';\n\n'],
      ['f', 'build'], ['', '('], ['s', `"${b.project}"`], ['', ', {\n  '],
      ['p', 'by'], ['', ': developer,\n  '],
      ['p', 'for'], ['', ': '], ['s', `"${b.for}"`], ['', ',\n});'],
    ];
    const lengthOf = (t) => t.reduce((n, [, s]) => n + s.length, 0);
    const render = (t, n) => {
      let out = '';
      for (const [cls, s] of t) {
        if (n <= 0) break;
        const part = s.slice(0, n);
        n -= part.length;
        out += cls ? `<span class="${cls}">${esc(part)}</span>` : esc(part);
      }
      code.innerHTML = out + '<span class="hm-ide__caret"></span>';
    };
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));

    let current = 0;
    let run = 0;
    let visible = true;

    const select = (i) => {
      current = i;
      picks.forEach((p, k) => {
        p.classList.toggle('is-active', k === i);
        p.setAttribute('aria-pressed', k === i ? 'true' : 'false');
      });
    };
    const reveal = (i) => {
      const b = builds[i];
      apps.forEach((a, k) => a.classList.toggle('is-active', k === i));
      nameEl.textContent = b.name;
      projectEl.textContent = b.project;
      avatarEl.innerHTML = b.avatar ? `<img src="${esc(b.avatar).replace(/"/g, '&quot;')}" alt="" width="48" height="48">` : esc(b.initials || '');
      credit.classList.remove('is-swap');
      void credit.offsetWidth;
      credit.classList.add('is-swap');
    };

    const play = async (i, id) => {
      const from = tokensFor(builds[current]);
      const to = tokensFor(builds[i]);
      select(i);
      if (reduceMotion) { render(to, lengthOf(to)); reveal(i); return true; }
      root.classList.add('is-typing');
      state.textContent = 'Typing…';
      apps.forEach((a) => a.classList.remove('is-active'));
      for (let n = lengthOf(from); n > 0; n -= 7) {
        if (id !== run) return false;
        render(from, n);
        await wait(10);
      }
      const total = lengthOf(to);
      for (let n = 0; n <= total; n += 1) {
        if (id !== run) return false;
        render(to, n);
        await wait(18 + Math.random() * 34);
      }
      root.classList.remove('is-typing');
      state.textContent = '✓ Built';
      reveal(i);
      return true;
    };

    const loop = async (id) => {
      if (reduceMotion) return;
      while (id === run) {
        await wait(5200);
        while (!visible && id === run) await wait(300);
        if (id !== run) return;
        await play((current + 1) % builds.length, id);
      }
    };

    picks.forEach((p, k) => p.addEventListener('click', () => {
      const id = ++run;
      play(k, id).then((done) => { if (done) loop(id); });
    }));

    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => { visible = entries[0].isIntersecting; }, { threshold: 0.2 }).observe(root);
    }
    loop(++run);
  });

  // ---------- Impact story: sticky year rail follows the chapters ----------
  document.querySelectorAll('[data-story]').forEach((root) => {
    const chapters = Array.from(root.querySelectorAll('.im-chapter'));
    const links = Array.from(root.querySelectorAll('.im-story__nav a'));
    const list = root.querySelector('.im-story__nav ol');
    const yearEl = root.querySelector('[data-story-year]');
    const tagEl = root.querySelector('[data-story-tag]');
    const numEl = root.querySelector('[data-story-num]');
    if (!chapters.length || !list) return;
    root.classList.add('is-live');

    let active = -1;
    const swap = (el, text) => {
      if (!el || el.textContent === text) return;
      el.textContent = text;
      el.classList.remove('is-swap');
      void el.offsetWidth;
      el.classList.add('is-swap');
    };

    const update = () => {
      const line = window.innerHeight * 0.4;
      let next = 0;
      chapters.forEach((c, i) => { if (c.getBoundingClientRect().top <= line) next = i; });

      const first = chapters[0].getBoundingClientRect().top;
      const last = chapters[chapters.length - 1].getBoundingClientRect().top;
      const progress = last === first ? 1 : Math.min(Math.max((line - first) / (last - first), 0), 1);
      list.style.setProperty('--progress', progress.toFixed(3));

      if (next === active) return;
      active = next;
      chapters.forEach((c, i) => c.classList.toggle('is-active', i === active));
      links.forEach((a, i) => {
        a.classList.toggle('is-active', i === active);
        a.classList.toggle('is-past', i < active);
        if (i === active) a.setAttribute('aria-current', 'step');
        else a.removeAttribute('aria-current');
      });
      root.classList.toggle('is-last', active === chapters.length - 1);
      swap(yearEl, chapters[active].dataset.year);
      swap(tagEl, chapters[active].dataset.tag);
      if (numEl) numEl.textContent = String(active + 1).padStart(2, '0');
    };

    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { ticking = false; update(); });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  });

})();
