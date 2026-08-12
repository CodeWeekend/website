/* ============================================================
   CodeWeekend Demo Day — Graduate profile modal
   ============================================================ */

(function () {
  'use strict';

  const viewer = document.getElementById('gradViewer');
  if (!viewer) return;

  let profiles = window.DEMO_DAY_PROFILES;
  if (typeof profiles === 'string') {
    try {
      profiles = JSON.parse(profiles);
    } catch (err) {
      return;
    }
  }
  if (!Array.isArray(profiles)) return;

  const placeholder = '/images/students-photo/placeholder.svg';
  const yagankarLogo = '/images/yagankar-logo.png';
  const imgEl = document.getElementById('gradViewerImg');
  const nameEl = document.getElementById('gradViewerName');
  const roleEl = document.getElementById('gradViewerRole');
  const locationEl = document.getElementById('gradViewerLocation');
  const quoteEl = document.getElementById('gradViewerQuote');
  const projectBlock = document.getElementById('gradViewerProjectBlock');
  const projectTitleEl = document.getElementById('gradViewerProjectTitle');
  const projectDescEl = document.getElementById('gradViewerProjectDesc');
  const demoSlot = document.getElementById('gradViewerDemo');
  const bioBlock = document.getElementById('gradViewerBioBlock');
  const bioEl = document.getElementById('gradViewerBio');
  const linksEl = document.getElementById('gradViewerLinks');

  let lastFocus = null;
  let activeTip = null;
  let focusTrapHandler = null;

  const unlockDate = String(window.DEMO_DAY_UNLOCK_DATE || '2026-08-27').trim();
  const eventDateLabel = String(window.DEMO_DAY_EVENT_DATE_LABEL || 'Thursday, 27 August 2026').trim();
  const demosLiveFromBuild = window.DEMO_DAY_DEMOS_LIVE === true;
  const demoLockedMessage = `The live demo will be available on Demo Day, ${eventDateLabel}.`;
  const lockIcon =
    '<svg class="grad-viewer__demo-lock" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17 9h-1V7a4 4 0 1 0-8 0v2H7a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zm-6-2a2 2 0 1 1 4 0v2h-4V7zm6 12H7v-8h10v8z"/></svg>';

  const stripMarkdown = (value) =>
    String(value || '')
      .replace(/\*\*/g, '')
      .replace(/\*/g, '')
      .trim();

  const setHidden = (el, hidden) => {
    if (!el) return;
    el.hidden = hidden;
  };

  const hasUrl = (value) => {
    const href = String(value || '').trim();
    return Boolean(href) && href !== '#';
  };

  const areDemosUnlocked = () => {
    if (demosLiveFromBuild) return true;
    try {
      const parts = new Intl.DateTimeFormat('en-CA', {
        timeZone: 'Asia/Kabul',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      }).formatToParts(new Date());
      const year = parts.find((part) => part.type === 'year')?.value;
      const month = parts.find((part) => part.type === 'month')?.value;
      const day = parts.find((part) => part.type === 'day')?.value;
      const today = `${year}-${month}-${day}`;
      return today >= unlockDate;
    } catch (err) {
      return new Date() >= new Date(`${unlockDate}T00:00:00+04:30`);
    }
  };

  const icons = {
    linkedin:
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.94 8.5H3.75V20h3.19V8.5zM5.34 4C4.22 4 3.3 4.93 3.3 6.05c0 1.1.92 2.03 2.05 2.03h.01C6.5 8.08 7.4 7.15 7.4 6.05 7.39 4.93 6.47 4 5.34 4zM20.25 13.37c0-3.54-1.89-5.19-4.41-5.19-2.03 0-2.94 1.12-3.45 1.9V8.5H9.25c.04.9 0 11.5 0 11.5h3.14v-6.42c0-.34.02-.68.13-.92.28-.68.9-1.38 1.96-1.38 1.38 0 1.93 1.05 1.93 2.58V20h3.14v-6.63z"/></svg>',
    portfolio:
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14 3h7v7h-2V6.41l-9.29 9.3-1.42-1.42 9.3-9.29H14V3zM5 5h6v2H7v10h10v-4h2v6H5V5z"/></svg>',
    yankar: `<img class="grad-viewer__yagankar" src="${yagankarLogo}" alt="" width="18" height="18" draggable="false" />`,
  };

  const clearActiveTip = () => {
    if (!activeTip) return;
    activeTip.classList.remove('is-tip-open');
    activeTip = null;
  };

  const bindUnavailableTip = (el) => {
    const show = () => {
      if (activeTip && activeTip !== el) clearActiveTip();
      el.classList.add('is-tip-open');
      activeTip = el;
    };
    const hide = () => {
      if (activeTip === el) clearActiveTip();
    };

    el.addEventListener('mouseenter', show);
    el.addEventListener('mouseleave', hide);
    el.addEventListener('focus', show);
    el.addEventListener('blur', hide);
    el.addEventListener('click', (event) => {
      event.preventDefault();
      if (el.classList.contains('is-tip-open')) {
        hide();
      } else {
        show();
      }
    });
  };

  const fillLinks = (student) => {
    const links = [
      {
        key: 'linkedin_url',
        label: 'LinkedIn',
        unavailable: 'LinkedIn profile is not available for this student.',
        icon: icons.linkedin,
      },
      {
        key: 'portfolio_url',
        label: 'Portfolio',
        unavailable: 'Portfolio is not available for this student.',
        icon: icons.portfolio,
      },
      {
        key: 'yankar_url',
        label: 'Yagankar profile',
        unavailable: 'Yagankar profile is not available for this student.',
        icon: icons.yankar,
      },
    ];

    linksEl.innerHTML = '';
    clearActiveTip();

    links.forEach((item) => {
      const href = String(student[item.key] || '').trim();
      const available = hasUrl(href);
      let el;

      if (available) {
        el = document.createElement('a');
        el.href = href;
        el.target = '_blank';
        el.rel = 'noopener noreferrer';
        el.setAttribute('aria-label', item.label);
        el.innerHTML = item.icon;
      } else {
        el = document.createElement('button');
        el.type = 'button';
        el.className = 'is-unavailable';
        el.setAttribute('aria-label', item.unavailable);
        el.setAttribute('title', item.unavailable);
        el.setAttribute('aria-disabled', 'true');
        el.innerHTML = `${item.icon}<span class="grad-viewer__tip" role="tooltip">${item.unavailable}</span>`;
        bindUnavailableTip(el);
      }

      linksEl.appendChild(el);
    });
  };

  const protectImage = (img) => {
    if (!img || img.dataset.protected === 'true') return;
    img.draggable = false;
    img.setAttribute('draggable', 'false');
    img.addEventListener('contextmenu', (event) => event.preventDefault());
    img.addEventListener('dragstart', (event) => event.preventDefault());
    img.dataset.protected = 'true';
  };

  const getFocusable = () => {
    if (!viewer) return [];
    return Array.from(
      viewer.querySelectorAll(
        'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
      )
    ).filter((el) => !el.hasAttribute('disabled') && el.offsetParent !== null && !el.closest('[hidden]'));
  };

  const releaseFocusTrap = () => {
    if (focusTrapHandler) {
      document.removeEventListener('keydown', focusTrapHandler, true);
      focusTrapHandler = null;
    }
    document.querySelectorAll('[data-grad-inert]').forEach((el) => {
      el.removeAttribute('inert');
      el.removeAttribute('data-grad-inert');
    });
  };

  const engageFocusTrap = () => {
    releaseFocusTrap();

    const markInertTree = (root) => {
      Array.from(root.children).forEach((child) => {
        if (child === viewer) return;
        if (child.contains(viewer)) {
          markInertTree(child);
          return;
        }
        child.setAttribute('inert', '');
        child.setAttribute('data-grad-inert', 'true');
      });
    };

    markInertTree(document.body);

    focusTrapHandler = (event) => {
      if (viewer.hidden || event.key !== 'Tab') return;
      const focusable = getFocusable();
      if (!focusable.length) {
        event.preventDefault();
        const closeBtn = viewer.querySelector('.grad-viewer__close');
        if (closeBtn) closeBtn.focus();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };

    document.addEventListener('keydown', focusTrapHandler, true);
  };

  const protectGraduateImages = () => {
    document
      .querySelectorAll('.event-grad-card__media img, .grad-viewer__photo img')
      .forEach(protectImage);
  };

  const fillDemo = (student) => {
    if (!demoSlot) return;
    demoSlot.replaceChildren();

    const href = String(student.demo_url || '').trim();
    const hasDemo = hasUrl(href) || student.demo_ready === true;

    if (!hasDemo) {
      setHidden(demoSlot, true);
      return;
    }

    if (areDemosUnlocked() && hasUrl(href)) {
      const link = document.createElement('a');
      link.className = 'grad-viewer__demo';
      link.href = href;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = 'View live demo';
      demoSlot.appendChild(link);
      setHidden(demoSlot, false);
      return;
    }

    const locked = document.createElement('button');
    locked.type = 'button';
    locked.className = 'grad-viewer__demo grad-viewer__demo--locked';
    locked.setAttribute('aria-disabled', 'true');
    locked.setAttribute('aria-label', demoLockedMessage);
    locked.setAttribute('title', demoLockedMessage);
    locked.innerHTML = `${lockIcon}<span>Live demo</span><span class="grad-viewer__tip" role="tooltip">${demoLockedMessage}</span>`;
    bindUnavailableTip(locked);
    demoSlot.appendChild(locked);
    setHidden(demoSlot, false);
  };

  const fillViewer = (student) => {
    const image = student.image && String(student.image).trim()
      ? student.image
      : placeholder;

    imgEl.src = image;
    imgEl.alt = student.name ? `Portrait of ${student.name}` : 'Graduate portrait';
    protectImage(imgEl);

    nameEl.textContent = student.name || '';
    roleEl.textContent = student.role || '';
    setHidden(roleEl, !student.role);

    locationEl.textContent = student.location || '';
    setHidden(locationEl, !student.location);

    fillLinks(student);

    if (student.quote) {
      const quote = stripMarkdown(student.quote).replace(/^["“]|["”]$/g, '');
      quoteEl.textContent = `“${quote}”`;
      setHidden(quoteEl, false);
    } else {
      quoteEl.textContent = '';
      setHidden(quoteEl, true);
    }

    if (student.bio) {
      const paragraphs = stripMarkdown(student.bio)
        .split(/\n\s*\n/)
        .map((part) => part.replace(/\n+/g, ' ').trim())
        .filter(Boolean);

      bioEl.replaceChildren();
      if (paragraphs.length) {
        paragraphs.forEach((text) => {
          const p = document.createElement('p');
          p.textContent = text;
          bioEl.appendChild(p);
        });
      } else {
        const p = document.createElement('p');
        p.textContent = stripMarkdown(student.bio);
        bioEl.appendChild(p);
      }
      setHidden(bioBlock, false);
    } else {
      bioEl.replaceChildren();
      setHidden(bioBlock, true);
    }

    if (student.project_title || student.project_description) {
      projectTitleEl.textContent = student.project_title || '';
      projectDescEl.textContent = stripMarkdown(student.project_description);
      setHidden(projectBlock, false);
      fillDemo(student);
    } else {
      setHidden(projectBlock, true);
      setHidden(demoSlot, true);
    }
  };

  const openViewer = (index) => {
    const student = profiles[index];
    if (!student || student.profile_complete === false) return;

    lastFocus = document.activeElement;
    fillViewer(student);

    const scrollEl = viewer.querySelector('.grad-viewer__scroll');
    if (scrollEl) scrollEl.scrollTop = 0;

    viewer.hidden = false;
    viewer.setAttribute('aria-hidden', 'false');
    document.body.classList.add('grad-viewer-open');
    engageFocusTrap();

    requestAnimationFrame(() => {
      viewer.classList.add('is-open');
    });

    const closeBtn = viewer.querySelector('.grad-viewer__close');
    if (closeBtn) closeBtn.focus();
  };

  const closeViewer = () => {
    if (viewer.hidden) return;

    clearActiveTip();
    releaseFocusTrap();
    viewer.classList.remove('is-open');
    document.body.classList.remove('grad-viewer-open');

    window.setTimeout(() => {
      viewer.hidden = true;
      viewer.setAttribute('aria-hidden', 'true');
      if (lastFocus && typeof lastFocus.focus === 'function') {
        lastFocus.focus();
      }
    }, 220);
  };

  document.addEventListener('click', (event) => {
    const openBtn = event.target.closest('[data-grad-open]');
    if (openBtn) {
      event.preventDefault();
      const index = Number(openBtn.getAttribute('data-grad-open'));
      if (!Number.isNaN(index)) openViewer(index);
      return;
    }

    if (event.target.closest('[data-grad-close]')) {
      event.preventDefault();
      closeViewer();
      return;
    }

    if (activeTip && !event.target.closest('.grad-viewer__links .is-unavailable, .grad-viewer__demo--locked')) {
      clearActiveTip();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !viewer.hidden) {
      event.preventDefault();
      closeViewer();
    }
  });

  protectGraduateImages();
})();
