(function () {
  'use strict';

  const RTL_LANGS = ['fa', 'ps', 'ar', 'ur', 'fa-AF'];
  const STORAGE_KEY = 'codeweekend-lang';

  function applyDir(lang) {
    const isRTL = RTL_LANGS.includes(lang);
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
    document.documentElement.lang = lang === 'fa' ? 'fa-AF' : (lang || 'en');
  }

  const savedLang = (() => {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  })();
  if (savedLang) applyDir(savedLang);

  function setCookie(name, value, days) {
    const expires = new Date(Date.now() + (days || 365) * 86400000).toUTCString();
    const host = window.location.hostname;
    document.cookie = name + '=' + value + '; expires=' + expires + '; path=/';
    if (host && host !== 'localhost') {
      const apex = host.split('.').slice(-2).join('.');
      document.cookie = name + '=' + value + '; expires=' + expires + '; path=/; domain=.' + apex;
    }
  }

  function clearCookie(name) {
    const past = 'Thu, 01 Jan 1970 00:00:00 UTC';
    const host = window.location.hostname;
    document.cookie = name + '=; expires=' + past + '; path=/';
    if (host && host !== 'localhost') {
      const apex = host.split('.').slice(-2).join('.');
      document.cookie = name + '=; expires=' + past + '; path=/; domain=.' + apex;
    }
  }

  window.googleTranslateElementInit = function () {
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'en,fa,ps',
      autoDisplay: false,
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
  };

  function switchTo(lang) {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* ignore */ }

    if (lang === 'en') {
      clearCookie('googtrans');
      applyDir('en');
      window.location.reload();
      return;
    }

    setCookie('googtrans', '/en/' + lang, 365);
    applyDir(lang);
    window.location.reload();
  }

  function bindLangButtons() {
    document.querySelectorAll('[data-lang]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const lang = btn.dataset.lang;
        if (lang) switchTo(lang);
      });
    });

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

  function loadGoogleTranslate() {
    if (window.google && window.google.translate) return;
    const script = document.createElement('script');
    script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    script.async = true;
    document.body.appendChild(script);
  }

  if (savedLang && savedLang !== 'en') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', loadGoogleTranslate);
    } else {
      loadGoogleTranslate();
    }
  }
})();
