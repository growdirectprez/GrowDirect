/*
 * ═══════════════════════════════════════════════════════════════
 *  ANGELIQUE LYLE — LP BEHAVIOR LAYER
 *  Injected via Luxury Presence → Global Scripts → Body JavaScript
 *  Paste into: LP Global Scripts > Body JavaScript (wrapped in script tags)
 *
 *  Handles: nav scroll shadow, scroll reveals, modals,
 *           smooth nav, seam animation, form webhook bridge
 * ═══════════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ── FONT INJECTION ──────────────────────────────────────────
  // LP may not have DM Serif Display / DM Sans — inject them
  if (!document.querySelector('link[href*="DM+Serif+Display"]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap';
    document.head.appendChild(link);
  }

  // ── NAV SCROLL SHADOW ───────────────────────────────────────
  function initNavScroll() {
    const nav = document.querySelector('header, nav, .site-header, [class*="navbar"]');
    if (!nav) return;

    function onScroll() {
      nav.classList.toggle('al-scrolled', window.scrollY > 40);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // initial state
  }

  // ── SCROLL REVEAL ───────────────────────────────────────────
  function initScrollReveal() {
    const reveals = document.querySelectorAll('.al-reveal');
    if (!reveals.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('al-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );

    reveals.forEach((el) => observer.observe(el));
  }

  // ── MODAL SYSTEM ────────────────────────────────────────────
  window.alOpenModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  };

  window.alCloseModal = function(id) {
    const modal = document.getElementById(id);
    if (modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }
  };

  // Close on overlay click
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('al-modal-overlay') && e.target.classList.contains('active')) {
      e.target.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  // Close on Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.al-modal-overlay.active').forEach(function(m) {
        m.classList.remove('active');
      });
      document.body.style.overflow = '';
    }
  });

  // ── SMOOTH SCROLL NAV ──────────────────────────────────────
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(a) {
      a.addEventListener('click', function(e) {
        const href = a.getAttribute('href');
        if (href === '#') return;
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

  // ── HISTORY SEAM ANIMATION ─────────────────────────────────
  // Duplicate seam content for infinite scroll illusion
  function initSeamScroll() {
    const seam = document.getElementById('al-seam');
    if (!seam) return;

    // Clone children for seamless loop
    const children = Array.from(seam.children);
    children.forEach(function(child) {
      seam.appendChild(child.cloneNode(true));
    });
  }

  // ── FORM WEBHOOK BRIDGE ────────────────────────────────────
  // Intercept LP form submissions and mirror data to Angel
  // This runs AFTER LP's own form handler, so LP CRM still gets the lead
  function initWebhookBridge() {
    // Configuration — update with real Angel endpoint when deployed
    const ANGEL_ENDPOINT = ''; // e.g., 'https://angel.growdirect.io/api/webhooks/lp'
    const WEBHOOK_ENABLED = false; // flip to true when Angel is live

    if (!WEBHOOK_ENABLED || !ANGEL_ENDPOINT) return;

    document.addEventListener('submit', function(e) {
      const form = e.target;
      if (!form || form.tagName !== 'FORM') return;

      // Collect form data
      const formData = new FormData(form);
      const payload = {};
      formData.forEach(function(value, key) {
        payload[key] = value;
      });

      // Add metadata
      payload._source = 'lp_form';
      payload._page = window.location.pathname;
      payload._timestamp = new Date().toISOString();
      payload._referrer = document.referrer || '';

      // Fire-and-forget to Angel (don't block LP's handler)
      try {
        fetch(ANGEL_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          keepalive: true
        }).catch(function() {
          // Silent fail — LP CRM is the safety net
        });
      } catch (err) {
        // Silent fail
      }
    }, true); // capture phase so we run before LP's handler
  }

  // ── ACTIVE NAV HIGHLIGHTING ────────────────────────────────
  function initActiveNav() {
    const sections = document.querySelectorAll('section[id]');
    if (!sections.length) return;

    const navLinks = document.querySelectorAll('nav a[href^="#"], header a[href^="#"]');
    if (!navLinks.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            navLinks.forEach((link) => {
              const isMatch = link.getAttribute('href') === '#' + id;
              link.style.color = isMatch ? 'var(--al-black)' : '';
            });
          }
        });
      },
      { threshold: 0.3, rootMargin: '-68px 0px 0px 0px' }
    );

    sections.forEach((section) => observer.observe(section));
  }

  // ── LAZY IMAGE LOADING ─────────────────────────────────────
  // Add loading="lazy" to images that LP might not have set
  function initLazyImages() {
    document.querySelectorAll('img:not([loading])').forEach(function(img) {
      // Don't lazy load above-the-fold hero images
      const rect = img.getBoundingClientRect();
      if (rect.top > window.innerHeight) {
        img.loading = 'lazy';
      }
    });
  }

  // ── INITIALIZE ──────────────────────────────────────────────
  function init() {
    initNavScroll();
    initScrollReveal();
    initSmoothScroll();
    initSeamScroll();
    initWebhookBridge();
    initActiveNav();
    initLazyImages();
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
