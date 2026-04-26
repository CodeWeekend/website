/* ============================================================
   CodeWeekend — Language switcher
   Uses Google Translate to render the page in Dari (fa) or Pashto (ps)
   When fa or ps is active, the page switches to RTL.
   ============================================================ */

(function () {
  'use strict';

  const RTL_LANGS = ['fa', 'ps', 'ar', 'ur', 'fa-AF'];
  const STORAGE_KEY = 'codeweekend-lang';

  // ---------- Apply RTL class as early as possible ----------
  // Read stored language and immediately set dir to avoid layout flash
  function applyDir(lang) {
    const isRTL = RTL_LANGS.includes(lang);
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    document.documentElement.lang = lang === 'fa' ? 'fa-AF' : (lang || 'en');
  }

  const savedLang = (() => {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  })();
  if (savedLang) applyDir(savedLang);

  // ---------- Cookie helpers ----------
  function setCookie(name, value, days) {
    const expires = new Date(Date.now() + (days || 365) * 86400000).toUTCString();
    const host = window.location.hostname;
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
    if (host && host !== 'localhost') {
      // Set on apex domain too, so subdomains share translation state
      const apex = host.split('.').slice(-2).join('.');
      document.cookie = `${name}=${value}; expires=${expires}; path=/; domain=.${apex}`;
    }
  }

  function clearCookie(name) {
    const past = 'Thu, 01 Jan 1970 00:00:00 UTC';
    const host = window.location.hostname;
    document.cookie = `${name}=; expires=${past}; path=/`;
    if (host && host !== 'localhost') {
      const apex = host.split('.').slice(-2).join('.');
      document.cookie = `${name}=; expires=${past}; path=/; domain=.${apex}`;
    }
  }

  // ---------- Initialize Google Translate widget (offscreen) ----------
  // Hugo's Hugo Pipes will inline this via the partial, but the function name
  // must exist on window.googleTranslateElementInit so the GT script can call it.
  window.googleTranslateElementInit = function () {
    /* global google */
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'en,fa,ps',
      autoDisplay: false,
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
  };

  // ---------- Switch language ----------
  function switchTo(lang) {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* ignore */ }

    if (lang === 'en') {
      // Clear Google Translate cookie and reload
      clearCookie('googtrans');
      applyDir('en');
      // Force reload without the gt cookie
      window.location.reload();
      return;
    }

    // Dari (fa) or Pashto (ps) — set the GT cookie and reload
    setCookie('googtrans', `/en/${lang}`, 365);
    applyDir(lang);
    window.location.reload();
  }

  // ---------- Set up button bindings ----------
  function bindLangButtons() {
    document.querySelectorAll('[data-lang]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const lang = btn.dataset.lang;
        if (lang) switchTo(lang);
      });
    });

    // Mark active button
    const current = (savedLang || 'en');
    document.querySelectorAll('[data-lang]').forEach((btn) => {
      if (btn.dataset.lang === current) btn.classList.add('active');
      else btn.classList.remove('active');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindLangButtons);
  } else {
    bindLangButtons();
  }

  // ---------- Auto-trigger Google Translate on page load if cookie is set ----------
  // Google Translate reads the googtrans cookie automatically on load and translates the page.
  // We just ensure the widget script is loaded.
  function loadGoogleTranslate() {
    if (window.google && window.google.translate) return;
    const script = document.createElement('script');
    script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    script.async = true;
    document.body.appendChild(script);
  }

  // Only load GT if user has chosen a non-English language
  if (savedLang && savedLang !== 'en') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', loadGoogleTranslate);
    } else {
      loadGoogleTranslate();
    }
  }
})();
