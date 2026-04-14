# growdirect.io Portfolio Site — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Bitcoin notarization single-pager at growdirect.io with a multi-page consulting portfolio site showcasing three product pillars.

**Architecture:** Static HTML/CSS/JS site deployed on GitHub Pages via `growdirectprez/growdirectprez.github.io` repo. No framework, no build step. CSS custom properties enable per-pillar brand theming. Formspree handles the contact form. GA4 tracks engagement events.

**Tech Stack:** HTML5, CSS3 (custom properties, flexbox, grid), vanilla JS, Google Fonts (Inter, Space Grotesk), GA4, Formspree

**Spec:** `docs/superpowers/specs/2026-04-14-growdirect-io-portfolio-site-design.md`

---

## File Structure

```
growdirectprez.github.io/
├── index.html              — Homepage (hero, service cards, capabilities, about, contact, footer)
├── pos-platform.html       — POS Platform pillar page (Canary gold accent)
├── re-toolkit.html         — RE Toolkit pillar page (Angel teal accent)
├── membership.html         — Membership Framework pillar page (Cove blue accent)
├── contact.html            — Contact form + direct email
├── 404.html                — Branded 404 page
├── assets/
│   ├── css/
│   │   └── style.css       — All styles: reset, typography, layout, nav, cards, pillar theming, responsive
│   ├── js/
│   │   └── main.js         — GA4 gtag config, custom events, Formspree AJAX submit, mobile nav toggle, sticky nav border
│   └── img/                — (empty for now — OG images added post-launch)
├── favicon.svg             — GrowDirect wordmark favicon (replace existing canary bird)
├── CNAME                   — growdirect.io (KEEP EXISTING — do not modify)
├── robots.txt              — Allow all, no disallow rules
├── sitemap.xml             — 4 indexable pages (excludes contact.html)
├── .gitignore              — (keep existing)
└── README.md               — (replace with brief project description)
```

**Files to keep from existing repo:** `CNAME`, `.gitignore`
**Files to delete:** existing `index.html`, `assets/brand/`, `assets/social/`, `favicon.svg`, `README.md`

---

## Chunk 1: Repository Setup + CSS + JS Foundation

### Task 1: Clone repo and clean existing files

**Files:**
- Keep: `CNAME`, `.gitignore`
- Delete: `index.html`, `assets/`, `favicon.svg`, `README.md`
- Create: `assets/css/`, `assets/js/`, `assets/img/`

- [ ] **Step 1: Clone the GitHub Pages repo into a working location**

```bash
cd /tmp
git clone git@github.com:growdirectprez/growdirectprez.github.io.git
cd growdirectprez.github.io
```

- [ ] **Step 2: Delete old site files, keep CNAME and .gitignore**

```bash
rm -f index.html favicon.svg README.md
rm -rf assets/
```

- [ ] **Step 3: Create new directory structure**

```bash
mkdir -p assets/css assets/js assets/img
```

- [ ] **Step 4: Commit clean slate**

```bash
git add -A
git commit -m "chore: remove old Bitcoin notarization site, prepare for portfolio rebuild"
```

---

### Task 2: Create favicon.svg

**Files:**
- Create: `favicon.svg`

The favicon is a simple "GD" monogram in Space Grotesk style. SVG text element, near-black on transparent.

- [ ] **Step 1: Create favicon.svg**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="4" fill="#1A1A1A"/>
  <text x="16" y="22" text-anchor="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="16" fill="#F8F7F4">GD</text>
</svg>
```

- [ ] **Step 2: Commit**

```bash
git add favicon.svg
git commit -m "feat: add GrowDirect favicon"
```

---

### Task 3: Create style.css — full site stylesheet

**Files:**
- Create: `assets/css/style.css`

This is the single stylesheet for the entire site. It contains: CSS reset, custom properties (base + per-pillar overrides), typography, layout primitives, nav, hero, service cards, capabilities strip, about section, contact section, footer, pillar page template styles, contact form styles, 404 styles, and responsive breakpoints.

- [ ] **Step 1: Create assets/css/style.css with complete styles**

```css
/* ============================================
   GrowDirect Portfolio Site — style.css
   No build step. No framework. One file.
   ============================================ */

/* --- Reset --- */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* --- Custom Properties --- */
:root {
  /* Base palette */
  --bg: #F8F7F4;
  --text: #1A1A1A;
  --text-secondary: #555555;
  --accent: #3D3D3D;
  --border: #E5E3DF;
  --card-bg: #FFFFFF;

  /* Pillar accents — overridden per page via body class */
  --pillar-accent: var(--accent);

  /* Canary gold */
  --canary-gold: #FBBF24;
  /* Angel teal */
  --angel-teal: #2DD4BF;
  /* Cove blue */
  --cove-blue: #1E3A5F;

  /* Typography */
  --font-body: 'Inter', system-ui, -apple-system, sans-serif;
  --font-heading: 'Space Grotesk', var(--font-body);

  /* Spacing */
  --section-pad: 5rem 1.5rem;
  --container-max: 1080px;

  /* Nav */
  --nav-height: 64px;
}

/* Pillar page overrides */
body.pillar-pos { --pillar-accent: var(--canary-gold); }
body.pillar-re { --pillar-accent: var(--angel-teal); }
body.pillar-membership { --pillar-accent: var(--cove-blue); }

/* --- Base --- */
html {
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--pillar-accent, var(--accent));
  text-decoration: none;
  transition: opacity 0.15s;
}

a:hover {
  opacity: 0.8;
}

img {
  max-width: 100%;
  display: block;
}

/* --- Typography --- */
h1, h2, h3, h4 {
  font-family: var(--font-heading);
  font-weight: 600;
  line-height: 1.2;
  color: var(--text);
}

h1 { font-size: 2.5rem; font-weight: 700; }
h2 { font-size: 1.75rem; }
h3 { font-size: 1.25rem; }
h4 { font-size: 1.1rem; }

p + p { margin-top: 1rem; }

/* --- Layout --- */
.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 1.5rem;
}

section {
  padding: var(--section-pad);
}

/* --- Nav --- */
.site-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg);
  height: var(--nav-height);
  display: flex;
  align-items: center;
  transition: box-shadow 0.2s;
}

.site-nav.scrolled {
  box-shadow: 0 1px 0 var(--border);
}

.site-nav .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.site-nav__wordmark {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text);
  text-decoration: none;
}

.site-nav__wordmark:hover {
  opacity: 1;
}

.site-nav__links {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.site-nav__links a {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
}

.site-nav__links a:hover {
  color: var(--text);
  opacity: 1;
}

.site-nav__links a.active {
  color: var(--text);
}

/* Hamburger */
.nav-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.nav-toggle span {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--text);
  margin: 5px 0;
  transition: transform 0.2s, opacity 0.2s;
}

/* --- Hero --- */
.hero {
  padding: 6rem 1.5rem 4rem;
  text-align: center;
}

.hero__wordmark {
  font-family: var(--font-heading);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.hero h1 {
  max-width: 700px;
  margin: 0 auto;
}

/* --- Service Cards --- */
.service-cards {
  padding: var(--section-pad);
}

.service-cards__grid {
  display: grid;
  gap: 2rem;
  max-width: var(--container-max);
  margin: 0 auto;
}

.service-cards__grid--two {
  grid-template-columns: 1fr 1fr;
}

.service-cards__grid--one {
  max-width: 540px;
}

a.service-card {
  display: block;
  text-decoration: none;
  color: inherit;
}

.service-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 2rem;
  border-top: 3px solid var(--card-accent, var(--accent));
  transition: box-shadow 0.15s;
}

.service-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.service-card[data-accent="canary"] { --card-accent: var(--canary-gold); }
.service-card[data-accent="angel"] { --card-accent: var(--angel-teal); }
.service-card[data-accent="cove"] { --card-accent: var(--cove-blue); }

.service-card h3 {
  margin-bottom: 0.75rem;
}

.service-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.service-card__audience {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-style: italic;
  margin-bottom: 1rem;
}

.service-card__link {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--card-accent, var(--accent));
}

/* --- Capabilities Strip --- */
.capabilities {
  padding: 3rem 1.5rem;
  text-align: center;
}

.capabilities__tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.75rem;
  max-width: var(--container-max);
  margin: 0 auto;
}

.capabilities__tag {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 0.4rem 1rem;
}

/* --- About --- */
.about {
  padding: var(--section-pad);
  max-width: var(--container-max);
  margin: 0 auto;
}

.about h2 {
  margin-bottom: 1.5rem;
}

.about p {
  color: var(--text-secondary);
  max-width: 680px;
}

/* --- Contact CTA (homepage) --- */
.contact-cta {
  padding: var(--section-pad);
  text-align: center;
}

.contact-cta__email {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text);
  display: block;
  margin-bottom: 1rem;
}

.contact-cta__link {
  font-size: 0.95rem;
  font-weight: 500;
}

/* --- Footer --- */
.site-footer {
  padding: 2rem 1.5rem;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.site-footer a {
  color: var(--text-secondary);
}

.site-footer p + p {
  margin-top: 0.25rem;
}

/* ================================
   Pillar Page Styles
   ================================ */
.pillar-hero {
  padding: 5rem 1.5rem 3rem;
  border-bottom: 3px solid var(--pillar-accent);
}

.pillar-hero h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.pillar-hero__product {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--pillar-accent);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.pillar-section {
  padding: var(--section-pad);
  max-width: var(--container-max);
  margin: 0 auto;
}

.pillar-section h2 {
  margin-bottom: 1.5rem;
}

.pillar-section p {
  color: var(--text-secondary);
  max-width: 720px;
}

/* Capability list on pillar pages */
.capability-list {
  list-style: none;
  display: grid;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.capability-list li {
  padding-left: 1rem;
  border-left: 3px solid var(--pillar-accent);
}

.capability-list li strong {
  display: block;
  margin-bottom: 0.25rem;
}

.capability-list li span {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* Stack tags */
.stack-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.stack-tag {
  font-size: 0.8rem;
  font-weight: 500;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.3rem 0.75rem;
}

/* Pillar CTA */
.pillar-cta {
  padding: var(--section-pad);
  text-align: center;
  border-top: 1px solid var(--border);
}

.pillar-cta a {
  font-size: 1rem;
  font-weight: 500;
  color: var(--pillar-accent);
}

/* ================================
   Contact Page
   ================================ */
.contact-page {
  padding: 5rem 1.5rem;
  max-width: 560px;
  margin: 0 auto;
}

.contact-page h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.contact-page > p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.contact-form label {
  font-size: 0.9rem;
  font-weight: 500;
  display: block;
  margin-bottom: 0.25rem;
}

.contact-form input,
.contact-form textarea {
  width: 100%;
  padding: 0.75rem;
  font-family: var(--font-body);
  font-size: 0.95rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--card-bg);
  color: var(--text);
}

.contact-form input:focus,
.contact-form textarea:focus {
  outline: 2px solid var(--accent);
  outline-offset: 1px;
}

.contact-form textarea {
  min-height: 120px;
  resize: vertical;
}

.contact-form button {
  align-self: flex-start;
  padding: 0.75rem 2rem;
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--bg);
  background: var(--text);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.15s;
}

.contact-form button:hover {
  opacity: 0.85;
}

.contact-form__success {
  display: none;
  padding: 1rem;
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #065F46;
}

.contact-form__success.visible {
  display: block;
}

.contact-direct {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* ================================
   404 Page
   ================================ */
.page-404 {
  padding: 8rem 1.5rem;
  text-align: center;
}

.page-404 h1 {
  font-size: 4rem;
  color: var(--border);
  margin-bottom: 1rem;
}

.page-404 p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

/* ================================
   Responsive
   ================================ */

/* Mobile: < 768px */
@media (max-width: 767px) {
  :root {
    --section-pad: 3rem 1.25rem;
  }

  h1 { font-size: 1.75rem; }
  h2 { font-size: 1.35rem; }

  .hero { padding: 4rem 1.25rem 3rem; }

  /* Mobile nav */
  .nav-toggle { display: block; }

  .site-nav__links {
    display: none;
    position: absolute;
    top: var(--nav-height);
    left: 0;
    right: 0;
    background: var(--bg);
    flex-direction: column;
    padding: 1rem 1.5rem 1.5rem;
    gap: 1rem;
    border-bottom: 1px solid var(--border);
  }

  .site-nav__links.open {
    display: flex;
  }

  /* Stacked cards */
  .service-cards__grid--two {
    grid-template-columns: 1fr;
  }

  /* Capabilities wrap */
  .capabilities__tags {
    gap: 0.5rem;
  }

  .capability-list {
    grid-template-columns: 1fr;
  }
}

/* Tablet: 768-1024px */
@media (min-width: 768px) and (max-width: 1024px) {
  .capability-list {
    grid-template-columns: 1fr 1fr;
  }
}

/* Desktop: > 1024px */
@media (min-width: 1025px) {
  .capability-list {
    grid-template-columns: 1fr 1fr;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add assets/css/style.css
git commit -m "feat: add complete site stylesheet with pillar theming and responsive breakpoints"
```

---

### Task 4: Create main.js — GA4 + events + form + nav

**Files:**
- Create: `assets/js/main.js`

- [ ] **Step 1: Create assets/js/main.js**

```javascript
/* ============================================
   GrowDirect Portfolio Site — main.js
   GA4 events, Formspree AJAX, mobile nav, sticky nav
   ============================================ */

(function () {
  'use strict';

  // --- Sticky nav border on scroll ---
  var nav = document.querySelector('.site-nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 10) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
    });
  }

  // --- Mobile nav toggle ---
  var toggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.site-nav__links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      var expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
    });
  }

  // --- GA4 custom events ---
  function trackEvent(eventName, params) {
    if (typeof gtag === 'function') {
      gtag('event', eventName, params || {});
    }
  }

  // pillar_click — service card links on homepage
  document.querySelectorAll('[data-track="pillar"]').forEach(function (el) {
    el.addEventListener('click', function () {
      trackEvent('pillar_click', { pillar: el.dataset.pillar || 'unknown' });
    });
  });

  // email_click — any mailto link
  document.querySelectorAll('a[href^="mailto:"]').forEach(function (el) {
    el.addEventListener('click', function () {
      trackEvent('email_click');
    });
  });

  // cta_click — any CTA link
  document.querySelectorAll('[data-track="cta"]').forEach(function (el) {
    el.addEventListener('click', function () {
      trackEvent('cta_click', { label: el.dataset.label || '' });
    });
  });

  // --- Formspree AJAX form submission ---
  var form = document.getElementById('contact-form');
  var successMsg = document.querySelector('.contact-form__success');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      }).then(function (response) {
        if (response.ok) {
          form.reset();
          if (successMsg) successMsg.classList.add('visible');
          trackEvent('contact_form_submit');
        } else {
          window.location.href = 'mailto:jeff@growdirect.io?subject=Contact%20from%20growdirect.io';
        }
      }).catch(function () {
        window.location.href = 'mailto:jeff@growdirect.io?subject=Contact%20from%20growdirect.io';
      });
    });
  }
})();
```

- [ ] **Step 2: Commit**

```bash
git add assets/js/main.js
git commit -m "feat: add GA4 event tracking, Formspree AJAX, mobile nav, and sticky nav"
```

---

## Chunk 2: Homepage

### Task 5: Create index.html

**Files:**
- Create: `index.html`

This is the most complex page — hero, two lead service cards, third pillar card, capabilities strip, about, contact CTA, and footer. The nav and footer pattern established here is reused by all other pages.

- [ ] **Step 1: Create index.html with all sections**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GrowDirect — Full-Stack Platform Development</title>
  <meta name="description" content="Full-stack platform development for retail, real estate, and membership organizations. From prototype to production.">
  <link rel="canonical" href="https://growdirect.io/">

  <!-- OG -->
  <meta property="og:title" content="GrowDirect — Full-Stack Platform Development">
  <meta property="og:description" content="Full-stack platform development for retail, real estate, and membership organizations. From prototype to production.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://growdirect.io/">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="GrowDirect — Full-Stack Platform Development">
  <meta name="twitter:description" content="Full-stack platform development for retail, real estate, and membership organizations. From prototype to production.">

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">

  <!-- Styles -->
  <link rel="stylesheet" href="/assets/css/style.css">

  <!-- GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
</head>
<body>

  <!-- Nav -->
  <nav class="site-nav" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="site-nav__wordmark">GrowDirect</a>
      <button class="nav-toggle" aria-expanded="false" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="site-nav__links">
        <li><a href="/pos-platform.html">POS Platform</a></li>
        <li><a href="/re-toolkit.html">RE Toolkit</a></li>
        <li><a href="/membership.html">Membership</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </div>
  </nav>

  <main>

    <!-- Hero -->
    <section class="hero">
      <div class="hero__wordmark">GrowDirect</div>
      <h1>From prototype to production. Platforms that ship.</h1>
    </section>

    <!-- Two Lead Service Lines -->
    <section class="service-cards">
      <div class="service-cards__grid service-cards__grid--two container">

        <a href="/pos-platform.html" class="service-card" data-accent="canary" data-track="pillar" data-pillar="pos-platform">
          <h3>Retail &amp; POS Intelligence</h3>
          <p>Event pipelines, real-time detection, merchant analytics, Bitcoin notarization.</p>
          <p class="service-card__audience">For Square merchants and the Square partnership ecosystem.</p>
          <span class="service-card__link">Explore platform →</span>
        </a>

        <a href="/re-toolkit.html" class="service-card" data-accent="angel" data-track="pillar" data-pillar="re-toolkit">
          <h3>Real Estate Agent Toolkit</h3>
          <p>Content engines, MLS market data, SEO, neighborhood intelligence, agent chat, lead capture.</p>
          <p class="service-card__audience">For Compass, Redfin, and LP agents who are overpaying for basic websites.</p>
          <span class="service-card__link">Explore toolkit →</span>
        </a>

      </div>
    </section>

    <!-- Third Pillar -->
    <section class="service-cards">
      <div class="service-cards__grid service-cards__grid--one container">

        <a href="/membership.html" class="service-card" data-accent="cove" data-track="pillar" data-pillar="membership">
          <h3>Membership Framework</h3>
          <p>GIS/mapping, governance workflows, member management, document vault, county services integration.</p>
          <p class="service-card__audience">For HOAs, membership organizations, and BPO automation.</p>
          <span class="service-card__link">Explore framework →</span>
        </a>

      </div>
    </section>

    <!-- Capabilities Strip -->
    <section class="capabilities">
      <div class="capabilities__tags">
        <span class="capabilities__tag">Data Modeling</span>
        <span class="capabilities__tag">API Gateway</span>
        <span class="capabilities__tag">MCP Architecture</span>
        <span class="capabilities__tag">Agentic Systems</span>
        <span class="capabilities__tag">Machine Learning</span>
        <span class="capabilities__tag">Dashboards</span>
        <span class="capabilities__tag">SEO</span>
        <span class="capabilities__tag">Data Governance</span>
        <span class="capabilities__tag">Event Pipelines</span>
        <span class="capabilities__tag">GIS / Mapping</span>
        <span class="capabilities__tag">Content Engines</span>
        <span class="capabilities__tag">Lead Generation</span>
        <span class="capabilities__tag">Factory Process</span>
      </div>
    </section>

    <!-- About -->
    <section class="about">
      <h2>About</h2>
      <p>Thirty years in retail technology — from IBM 4690 POS systems and LaneHawk self-checkout to modern cloud platforms. Along the way, one observation kept surfacing: every POS system has mutable transaction logs. Records that can be silently edited after the fact.</p>
      <p>GrowDirect builds platforms that solve real problems — from prototype to production, solo or with a team. AI-assisted development that ships real products, not slide decks.</p>
    </section>

    <!-- Contact CTA -->
    <section class="contact-cta">
      <a href="mailto:jeff@growdirect.io" class="contact-cta__email">jeff@growdirect.io</a>
      <a href="/contact.html" class="contact-cta__link" data-track="cta" data-label="homepage-contact">Have something to build? →</a>
    </section>

  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <p>© 2026 GrowDirect. <a href="mailto:jeff@growdirect.io">jeff@growdirect.io</a></p>
      <p>This site uses Google Analytics to measure traffic. No advertising. No remarketing.</p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Preview and verify**

Open the file in a browser or use preview tools. Check:
- Nav renders with wordmark left, links right
- Hero headline renders centered in Space Grotesk
- Two service cards side by side with colored top borders (gold, teal)
- Third card centered below
- Capabilities tags wrap horizontally
- About section readable
- Footer at bottom
- Resize to mobile (< 768px): cards stack, hamburger appears

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add homepage with service cards, capabilities, about, and contact CTA"
```

---

## Chunk 3: Pillar Pages

### Task 6: Create pos-platform.html

**Files:**
- Create: `pos-platform.html`

- [ ] **Step 1: Create pos-platform.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Retail &amp; POS Intelligence — GrowDirect</title>
  <meta name="description" content="Real-time loss prevention and analytics platform built on Square's API. Event pipelines, detection rules, merchant dashboards.">
  <link rel="canonical" href="https://growdirect.io/pos-platform.html">

  <meta property="og:title" content="Retail & POS Intelligence — GrowDirect">
  <meta property="og:description" content="Real-time loss prevention and analytics platform built on Square's API. Event pipelines, detection rules, merchant dashboards.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://growdirect.io/pos-platform.html">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Retail & POS Intelligence — GrowDirect">
  <meta name="twitter:description" content="Real-time loss prevention and analytics platform built on Square's API. Event pipelines, detection rules, merchant dashboards.">

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
</head>
<body class="pillar-pos">

  <nav class="site-nav" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="site-nav__wordmark">GrowDirect</a>
      <button class="nav-toggle" aria-expanded="false" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="site-nav__links">
        <li><a href="/pos-platform.html" class="active" aria-current="page">POS Platform</a></li>
        <li><a href="/re-toolkit.html">RE Toolkit</a></li>
        <li><a href="/membership.html">Membership</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </div>
  </nav>

  <main>

    <section class="pillar-hero">
      <div class="container">
        <p class="pillar-hero__product">Canary Platform</p>
        <h1>Retail &amp; POS Intelligence</h1>
      </div>
    </section>

    <section class="pillar-section">
      <h2>What Was Built</h2>
      <p>A real-time loss prevention and analytics platform built on Square's API. Captures every webhook event, seals it cryptographically, runs 29 detection rules, and surfaces alerts to merchants in plain language.</p>
    </section>

    <section class="pillar-section">
      <h2>Capabilities</h2>
      <ul class="capability-list">
        <li>
          <strong>Square Webhook Pipeline</strong>
          <span>OAuth, HMAC validation, real-time event capture</span>
        </li>
        <li>
          <strong>Transaction Stream Processing</strong>
          <span>4-stage pipeline (hash, parse, merkle, detect)</span>
        </li>
        <li>
          <strong>Chirp Detection Engine</strong>
          <span>29 rules across 3 severity tiers, plain-language alerts</span>
        </li>
        <li>
          <strong>Fox Case Management</strong>
          <span>Investigation workflows with evidence chains</span>
        </li>
        <li>
          <strong>Owl AI Analytics</strong>
          <span>Ollama-powered analysis, MCP tool interface</span>
        </li>
        <li>
          <strong>RaaS Namespace</strong>
          <span>Bitcoin Ordinal inscription, namespace resolution</span>
        </li>
        <li>
          <strong>Merchant Dashboard</strong>
          <span>Risk scoring, KPI visualization, alert management</span>
        </li>
        <li>
          <strong>Multi-POS Architecture</strong>
          <span>Adapter pattern for source-agnostic ingestion</span>
        </li>
      </ul>
    </section>

    <section class="pillar-section">
      <h2>Stack</h2>
      <div class="stack-tags">
        <span class="stack-tag">Python / Flask</span>
        <span class="stack-tag">PostgreSQL 17</span>
        <span class="stack-tag">pgvector</span>
        <span class="stack-tag">Valkey 8</span>
        <span class="stack-tag">SQLAlchemy 2.0</span>
        <span class="stack-tag">Alembic</span>
        <span class="stack-tag">Tailwind CSS</span>
        <span class="stack-tag">Alpine.js</span>
        <span class="stack-tag">Ollama</span>
        <span class="stack-tag">Docker Compose</span>
      </div>
    </section>

    <section class="pillar-cta">
      <a href="/contact.html" data-track="cta" data-label="pos-platform">Let's talk about your merchants →</a>
    </section>

  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© 2026 GrowDirect. <a href="mailto:jeff@growdirect.io">jeff@growdirect.io</a></p>
      <p>This site uses Google Analytics to measure traffic. No advertising. No remarketing.</p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Preview and verify**

Check: gold accent on pillar hero border, capability list with gold left borders, stack tags, CTA link, active nav state on "POS Platform", mobile responsive.

- [ ] **Step 3: Commit**

```bash
git add pos-platform.html
git commit -m "feat: add POS Platform pillar page (Canary gold accent)"
```

---

### Task 7: Create re-toolkit.html

**Files:**
- Create: `re-toolkit.html`

- [ ] **Step 1: Create re-toolkit.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Real Estate Agent Toolkit — GrowDirect</title>
  <meta name="description" content="Neighborhood intelligence platform for real estate agents. MLS data, community content, conversational AI, and lead capture.">
  <link rel="canonical" href="https://growdirect.io/re-toolkit.html">

  <meta property="og:title" content="Real Estate Agent Toolkit — GrowDirect">
  <meta property="og:description" content="Neighborhood intelligence platform for real estate agents. MLS data, community content, conversational AI, and lead capture.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://growdirect.io/re-toolkit.html">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Real Estate Agent Toolkit — GrowDirect">
  <meta name="twitter:description" content="Neighborhood intelligence platform for real estate agents. MLS data, community content, conversational AI, and lead capture.">

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
</head>
<body class="pillar-re">

  <nav class="site-nav" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="site-nav__wordmark">GrowDirect</a>
      <button class="nav-toggle" aria-expanded="false" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="site-nav__links">
        <li><a href="/pos-platform.html">POS Platform</a></li>
        <li><a href="/re-toolkit.html" class="active" aria-current="page">RE Toolkit</a></li>
        <li><a href="/membership.html">Membership</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </div>
  </nav>

  <main>

    <section class="pillar-hero">
      <div class="container">
        <p class="pillar-hero__product">Angel Platform</p>
        <h1>Real Estate Agent Toolkit</h1>
      </div>
    </section>

    <section class="pillar-section">
      <h2>What Was Built</h2>
      <p>A neighborhood intelligence platform for real estate agents. Combines MLS listing data, county parcel records, community content, and conversational AI into a toolkit that replaces basic hosted websites with a data-driven content engine.</p>
    </section>

    <section class="pillar-section">
      <h2>Capabilities</h2>
      <ul class="capability-list">
        <li>
          <strong>Neighborhood Hub System</strong>
          <span>DB-backed pages with voice overlays, Schema.org markup, SEO optimization</span>
        </li>
        <li>
          <strong>MLS Data Platform</strong>
          <span>CRMLS integration, 214-column listing ingest, APN-based parcel bridge</span>
        </li>
        <li>
          <strong>Market Snapshots</strong>
          <span>Automated monthly/quarterly aggregations by area</span>
        </li>
        <li>
          <strong>Community Intelligence</strong>
          <span>RSS crawl pipeline, entity/event database, keyword classification</span>
        </li>
        <li>
          <strong>Agent Chat Widget</strong>
          <span>Claude-powered sidecar with 12 MCP tools, trained on neighborhood knowledge</span>
        </li>
        <li>
          <strong>Lead Capture Pipeline</strong>
          <span>Webhook integration, CRM sync, contact management</span>
        </li>
        <li>
          <strong>SEO Foundation</strong>
          <span>Sitemap, robots.txt, OG meta, canonical URLs, school guide pages</span>
        </li>
      </ul>
    </section>

    <section class="pillar-section">
      <h2>Stack</h2>
      <div class="stack-tags">
        <span class="stack-tag">Python / Flask</span>
        <span class="stack-tag">PostgreSQL 17</span>
        <span class="stack-tag">Tailwind CSS</span>
        <span class="stack-tag">Alpine.js</span>
        <span class="stack-tag">Leaflet.js</span>
        <span class="stack-tag">Claude API</span>
        <span class="stack-tag">Docker Compose</span>
      </div>
    </section>

    <section class="pillar-cta">
      <a href="/contact.html" data-track="cta" data-label="re-toolkit">Want something like this for your agents? →</a>
    </section>

  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© 2026 GrowDirect. <a href="mailto:jeff@growdirect.io">jeff@growdirect.io</a></p>
      <p>This site uses Google Analytics to measure traffic. No advertising. No remarketing.</p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Preview and verify**

Check: teal accent on pillar hero border, teal left borders on capabilities, active nav on "RE Toolkit".

- [ ] **Step 3: Commit**

```bash
git add re-toolkit.html
git commit -m "feat: add RE Toolkit pillar page (Angel teal accent)"
```

---

### Task 8: Create membership.html

**Files:**
- Create: `membership.html`

- [ ] **Step 1: Create membership.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Membership Framework — GrowDirect</title>
  <meta name="description" content="Governance and operations platform for HOAs and membership organizations. GIS parcels, elections, treasury, document vault.">
  <link rel="canonical" href="https://growdirect.io/membership.html">

  <meta property="og:title" content="Membership Framework — GrowDirect">
  <meta property="og:description" content="Governance and operations platform for HOAs and membership organizations. GIS parcels, elections, treasury, document vault.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://growdirect.io/membership.html">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Membership Framework — GrowDirect">
  <meta name="twitter:description" content="Governance and operations platform for HOAs and membership organizations. GIS parcels, elections, treasury, document vault.">

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
</head>
<body class="pillar-membership">

  <nav class="site-nav" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="site-nav__wordmark">GrowDirect</a>
      <button class="nav-toggle" aria-expanded="false" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="site-nav__links">
        <li><a href="/pos-platform.html">POS Platform</a></li>
        <li><a href="/re-toolkit.html">RE Toolkit</a></li>
        <li><a href="/membership.html" class="active" aria-current="page">Membership</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </div>
  </nav>

  <main>

    <section class="pillar-hero">
      <div class="container">
        <p class="pillar-hero__product">Cove Platform</p>
        <h1>Membership Framework</h1>
      </div>
    </section>

    <section class="pillar-section">
      <h2>What Was Built</h2>
      <p>A governance and operations platform for a real HOA (81 lots, Davis-Stirling compliant). GIS-integrated parcel management, secret ballot elections with row-level security, treasury, document vault, and AI-powered legal document search.</p>
    </section>

    <section class="pillar-section">
      <h2>Capabilities</h2>
      <ul class="capability-list">
        <li>
          <strong>GIS Parcel Engine</strong>
          <span>5,514 APN-keyed parcels, Leaflet mapping, GeoJSON rendering, county data enrichment</span>
        </li>
        <li>
          <strong>Governance Engine</strong>
          <span>Proposal lifecycle, quorum calculation, Davis-Stirling compliance</span>
        </li>
        <li>
          <strong>Secret Ballot Elections</strong>
          <span>Two-envelope scheme, PostgreSQL RLS, cryptographic ballot separation</span>
        </li>
        <li>
          <strong>Treasury Management</strong>
          <span>Assessment tracking, payment processing, delinquency workflows</span>
        </li>
        <li>
          <strong>Document Vault</strong>
          <span>Upload, access tiers, embedding generation for semantic search</span>
        </li>
        <li>
          <strong>Knowledge Search</strong>
          <span>pgvector legal document search via MCP server</span>
        </li>
        <li>
          <strong>Meeting Management</strong>
          <span>Scheduling, ARC reviews, ICS generation</span>
        </li>
        <li>
          <strong>Member Auth</strong>
          <span>Magic link login, role-based access (member, board, admin)</span>
        </li>
      </ul>
    </section>

    <section class="pillar-section">
      <h2>Stack</h2>
      <div class="stack-tags">
        <span class="stack-tag">Python / Flask</span>
        <span class="stack-tag">PostgreSQL 17</span>
        <span class="stack-tag">pgvector</span>
        <span class="stack-tag">Valkey 8</span>
        <span class="stack-tag">Leaflet.js</span>
        <span class="stack-tag">Tailwind CSS</span>
        <span class="stack-tag">Alpine.js</span>
        <span class="stack-tag">Ollama</span>
        <span class="stack-tag">Docker Compose</span>
      </div>
    </section>

    <section class="pillar-cta">
      <a href="/contact.html" data-track="cta" data-label="membership">Have a membership organization that needs this? →</a>
    </section>

  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© 2026 GrowDirect. <a href="mailto:jeff@growdirect.io">jeff@growdirect.io</a></p>
      <p>This site uses Google Analytics to measure traffic. No advertising. No remarketing.</p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Preview and verify**

Check: deep blue accent, blue left borders, active nav on "Membership".

- [ ] **Step 3: Commit**

```bash
git add membership.html
git commit -m "feat: add Membership Framework pillar page (Cove blue accent)"
```

---

## Chunk 4: Contact, 404, SEO Files, and Deploy

### Task 9: Create contact.html

**Files:**
- Create: `contact.html`

**Note:** The Formspree endpoint URL (`https://formspree.io/f/YOUR_FORM_ID`) must be replaced with a real Formspree form ID before launch. Create one at formspree.io — free tier, no account needed for basic usage.

- [ ] **Step 1: Create contact.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contact — GrowDirect</title>
  <meta name="robots" content="noindex">

  <!-- OG (for link previews when shared directly) -->
  <meta property="og:title" content="Contact — GrowDirect">
  <meta property="og:description" content="Get in touch about your next platform project.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://growdirect.io/contact.html">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="Contact — GrowDirect">
  <meta name="twitter:description" content="Get in touch about your next platform project.">

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
</head>
<body>

  <nav class="site-nav" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="site-nav__wordmark">GrowDirect</a>
      <button class="nav-toggle" aria-expanded="false" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="site-nav__links">
        <li><a href="/pos-platform.html">POS Platform</a></li>
        <li><a href="/re-toolkit.html">RE Toolkit</a></li>
        <li><a href="/membership.html">Membership</a></li>
        <li><a href="/contact.html" class="active" aria-current="page">Contact</a></li>
      </ul>
    </div>
  </nav>

  <main>

    <div class="contact-page">
      <h1>Get in touch</h1>
      <p>Have something to build? Tell me about it.</p>

      <form id="contact-form" class="contact-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
        <div>
          <label for="name">Name</label>
          <input type="text" id="name" name="name" required>
        </div>
        <div>
          <label for="email">Email</label>
          <input type="email" id="email" name="email" required>
        </div>
        <div>
          <label for="message">What are you working on?</label>
          <textarea id="message" name="message" required></textarea>
        </div>
        <button type="submit">Send</button>
      </form>

      <div class="contact-form__success">
        Thanks for reaching out. I'll be in touch soon.
      </div>

      <div class="contact-direct">
        <p>Prefer email? <a href="mailto:jeff@growdirect.io">jeff@growdirect.io</a></p>
      </div>
    </div>

  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© 2026 GrowDirect. <a href="mailto:jeff@growdirect.io">jeff@growdirect.io</a></p>
      <p>This site uses Google Analytics to measure traffic. No advertising. No remarketing.</p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add contact.html
git commit -m "feat: add contact page with Formspree form and direct email"
```

---

### Task 10: Create 404.html

**Files:**
- Create: `404.html`

- [ ] **Step 1: Create 404.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page Not Found — GrowDirect</title>
  <meta name="robots" content="noindex">

  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>

  <nav class="site-nav" role="navigation" aria-label="Main navigation">
    <div class="container">
      <a href="/" class="site-nav__wordmark">GrowDirect</a>
      <button class="nav-toggle" aria-expanded="false" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
      <ul class="site-nav__links">
        <li><a href="/pos-platform.html">POS Platform</a></li>
        <li><a href="/re-toolkit.html">RE Toolkit</a></li>
        <li><a href="/membership.html">Membership</a></li>
        <li><a href="/contact.html">Contact</a></li>
      </ul>
    </div>
  </nav>

  <main>
    <div class="page-404">
      <h1>404</h1>
      <p>This page doesn't exist.</p>
      <a href="/">← Back to GrowDirect</a>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>© 2026 GrowDirect. <a href="mailto:jeff@growdirect.io">jeff@growdirect.io</a></p>
      <p>This site uses Google Analytics to measure traffic. No advertising. No remarketing.</p>
    </div>
  </footer>

  <script src="/assets/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add 404.html
git commit -m "feat: add branded 404 page"
```

---

### Task 11: Create robots.txt and sitemap.xml

**Files:**
- Create: `robots.txt`
- Create: `sitemap.xml`

- [ ] **Step 1: Create robots.txt**

```
User-agent: *
Allow: /

Sitemap: https://growdirect.io/sitemap.xml
```

- [ ] **Step 2: Create sitemap.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://growdirect.io/</loc>
    <lastmod>2026-04-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://growdirect.io/pos-platform.html</loc>
    <lastmod>2026-04-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://growdirect.io/re-toolkit.html</loc>
    <lastmod>2026-04-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://growdirect.io/membership.html</loc>
    <lastmod>2026-04-14</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

- [ ] **Step 3: Commit**

```bash
git add robots.txt sitemap.xml
git commit -m "feat: add robots.txt and sitemap.xml for SEO"
```

---

### Task 12: Update README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
# growdirect.io

Portfolio site for GrowDirect consulting. Static HTML/CSS/JS on GitHub Pages.

**Live:** https://growdirect.io
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README for portfolio site"
```

---

### Task 13: Pre-launch checklist and deploy

- [ ] **Step 1: Replace GA4 placeholder**

Search all HTML files for `G-XXXXXXXXXX` and replace with the real GA4 Measurement ID (create property at analytics.google.com first).

- [ ] **Step 2: Replace Formspree placeholder**

In `contact.html`, replace `YOUR_FORM_ID` with the real Formspree form ID (create form at formspree.io).

- [ ] **Step 3: Final preview — test all pages**

Open each page in a browser. Check:
- [ ] index.html: nav, hero, 3 cards, capabilities, about, contact CTA, footer
- [ ] pos-platform.html: gold accent, 8 capabilities, stack, CTA
- [ ] re-toolkit.html: teal accent, 7 capabilities, stack, CTA
- [ ] membership.html: blue accent, 8 capabilities, stack, CTA
- [ ] contact.html: form renders, noindex meta present, direct email link
- [ ] 404.html: branded message, nav, back link
- [ ] Mobile (< 768px): hamburger works, cards stack, no horizontal overflow
- [ ] All nav links work (no 404s between pages)
- [ ] All mailto links work
- [ ] Safari / iOS: test on iPhone or Safari desktop — fonts load, nav works, cards render

- [ ] **Step 4: Commit any placeholder replacements**

```bash
git add -A
git commit -m "chore: replace GA4 and Formspree placeholders with live IDs"
```

- [ ] **Step 5: Push to deploy**

```bash
git push origin main
```

Expected: GitHub Pages deploys automatically. Verify at https://growdirect.io within 2-3 minutes.

- [ ] **Step 6: Post-deploy verification**

- [ ] Site loads at https://growdirect.io
- [ ] HTTPS works (no mixed content warnings)
- [ ] All 5 pages accessible
- [ ] Contact form submits successfully (check Formspree dashboard)
- [ ] GA4 Realtime report shows page views
- [ ] Mobile renders correctly
