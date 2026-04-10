# LP Global Scripts Injection — Angelique Lyle

## How to Install

### 1. Head JavaScript (CSS Override)

Go to **LP Dashboard → Website Settings → Global Scripts → Head JavaScript**

Paste the entire contents of `lp-head-inject.html` (already wrapped in `<style>` tags).

### 2. Body JavaScript (Behavior Layer)

Go to **LP Dashboard → Website Settings → Global Scripts → Body JavaScript**

Paste the entire contents of `lp-body-inject.html` (already wrapped in `<script>` tags).

### 3. Target Site

Use the **second LP website instance** ("Angelique Lyle" — Preview Ready, no domain assigned) as the staging site. Do NOT inject into the live site until tested.

Preview URL: `https://p-6640af74-339a-4bac-8ba6-db2a4dad701d.presencepreview.site/`

## File Inventory

| File | Purpose | LP Field |
|------|---------|----------|
| `lp-head-inject.html` | Ready-to-paste CSS design override (v2, LP-class-aware) | Head JavaScript |
| `lp-body-inject.html` | Ready-to-paste JS behavior layer | Body JavaScript |

## v2 Changes (2026-04-06)

v2 rewrites the CSS to target LP's **actual DOM classes** discovered via live DOM audit, instead of relying on `al-` prefixed custom classes that needed manual HTML editing.

### LP DOM Classes Targeted

| LP Class | Purpose |
|----------|---------|
| `.header`, `.header__container`, `.header__right` | Navigation bar |
| `.logo__name`, `.logo__number` | Logo text + DRE badge |
| `.navigation__link` | Nav menu links |
| `.hamburger`, `.hamburger__dots` | Mobile menu toggle |
| `.sidemenu-wrapper`, `.sidemenu-wrapper__item` | Mobile side menu |
| `.solid-section` | Section wrapper |
| `.is-background-color-dark/light` | Section color toggles |
| `.is-font-color-dark/light` | Text color toggles |
| `.section-intro-subtitle`, `.section-intro-title` | Section eyebrow + heading |
| `.opening`, `.opening__content`, `.opening__slider` | Hero section |
| `.opening__item-text` | Hero headline |
| `.featured-agent`, `.featured-agent-img/content/title` | About section |
| `.featured-neighborhoods`, `.featured-neighborhoods-list-item` | Neighborhoods grid |
| `.featured-testimonials`, `.featured-testimonials-list-item` | Testimonials |
| `.btn`, `.btn-blue`, `.btn--outline` | Buttons |
| `.inp`, `.contact-popup-input` | Form inputs |
| `.contact-popup`, `.contact-popup-submit` | Contact popup |
| `.footer`, `.footer__top`, `.footer__contact` | Footer |
| `.lp-socials__link`, `.socials__item` | Social icons |
| `.slick-*` | Carousel (hero, testimonials) |
| `.wow`, `.fadeInUp` | Scroll animations |

### al- Prefix Classes (Retained)

Custom `al-` classes are retained for elements that don't map to LP's native components (custom HTML blocks, history seam, modals):

- `al-tag`, `al-eyebrow`, `al-section-heading`, `al-body-text` — typography
- `al-section-dark/light/muted` — custom section backgrounds
- `al-history-seam`, `al-seam-scroll` — scrolling ticker
- `al-hood-card` — custom neighborhood cards (for custom HTML)
- `al-test-card` — custom testimonial cards
- `al-modal-overlay`, `al-modal` — modal system
- `al-reveal`, `al-visible` — scroll reveals
- `al-scrolled` — nav scroll state

## Webhook Bridge

The JS includes a form webhook bridge that mirrors LP form submissions to the Angel backend. It's **disabled by default**. To activate:

1. Deploy Angel's `/api/webhooks/lp` endpoint
2. In `lp-body-inject.html`, set:
   - `ANGEL_ENDPOINT = 'https://angel.growdirect.io/api/webhooks/lp'`
   - `WEBHOOK_ENABLED = true`

The bridge runs fire-and-forget — LP's native CRM always receives the lead regardless.
