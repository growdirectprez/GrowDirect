(function () {
  'use strict';

  // Sticky nav shadow
  var nav = document.querySelector('.doc-nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 10);
    });
  }

  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var links = document.querySelector('.nav-links');
      if (links) {
        links.classList.toggle('open');
      }
    });
  }

  // GA4 custom events
  function trackEvent(name, params) {
    if (typeof gtag === 'function') {
      gtag('event', name, params || {});
    }
  }

  document.querySelectorAll('a[href^="mailto:"]').forEach(function (el) {
    el.addEventListener('click', function () {
      trackEvent('email_click');
    });
  });

  document.querySelectorAll('[data-track="cta"]').forEach(function (el) {
    el.addEventListener('click', function () {
      trackEvent('cta_click', { label: el.dataset.label || '' });
    });
  });

  document.querySelectorAll('[data-track="pillar"]').forEach(function (el) {
    el.addEventListener('click', function () {
      trackEvent('pillar_click', { pillar: el.dataset.pillar || 'unknown' });
    });
  });

  // Smooth scroll focus management for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      var id = el.getAttribute('href').slice(1);
      if (!id) return;
      var target = document.getElementById(id);
      if (target) {
        // Allow CSS scroll-behavior to handle scrolling; manage focus for a11y
        setTimeout(function () {
          if (!target.hasAttribute('tabindex')) {
            target.setAttribute('tabindex', '-1');
          }
          target.focus({ preventScroll: true });
        }, 100);
      }
    });
  });
})();
