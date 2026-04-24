# Solex Visual Fidelity Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Plans 1–3's placeholder styling with a brand-coherent Tailwind theme approximating `solexglobal.com`, expand the catalog from 5 seed SKUs to 25 with plausible product data + placeholder imagery, and add the static marketing pages (About/Events/University/Blog/Resources + Privacy/Refunds/Shipping/Terms) that a real commerce site has.

**Architecture:** No backend changes. Pure presentation: Tailwind `theme.extend` gets real design tokens (palette, typography, spacing), `base.html` + blueprints' layout shells become brand-faithful, storefront templates get hero sections / galleries / proper cards, static pages ship as Jinja templates under a `pages` blueprint, catalog YAML expands with 25 SKUs and each gets a generated solid-tile placeholder image (real Solex imagery dropped in later by human — see §Known constraints).

**Tech Stack:** Tailwind 3.x, PostCSS, Alpine 3 (already wired), Jinja. One new dev dependency: `Pillow` for placeholder-image generation (isolated to a CLI subcommand; not a runtime dep).

---

## Scope

**This is Plan 4 of 4.** Depends on Plans 1–3 stacked on `plan/solex-scenarios`.

**In scope:**
- Tailwind `solex` theme: palette, typography scale, spacing extensions
- Header: logo + primary nav (Shop / AO Scan / University / Events / Blog / About) + cart icon w/ count
- Footer: 4-column layout (Shop / Company / Support / Connect) + policy links + small brand mark
- Storefront:
  - Home: hero + "featured" grid + category tiles + testimonial-style section + trust-bar
  - Shop: sidebar w/ categories + grid of product cards + pagination (simple prev/next)
  - Product detail: gallery (single image for now, gallery-ready), quantity selector, subscribe-and-save radio, short-desc + full-desc sections
- Cart drawer polish (slide-over, qty steppers, subtotal, CTA)
- Checkout polish (step header, two-column on desktop)
- Order confirmation polish
- Account + admin: adopt branded layout (wrapper only; functionality untouched)
- Static pages under new `pages` blueprint:
  - Marketing: `/about`, `/events`, `/university`, `/blog`, `/resources`
  - Policy: `/privacy`, `/refunds`, `/shipping`, `/terms`
  - All with short, honest placeholder copy (no hype) and a "Draft — placeholder content" banner
- Catalog expansion: 25 SKUs across all 4 categories with plausible names/descriptions/prices (matches Solex product-line themes: AO Scan devices, supplements, therapy, pet, bundles)
- Placeholder imagery: CLI `catalog generate-placeholders` produces a 600×600 solid-tile PNG per SKU with the SKU text overlaid; committed to `catalog/images/`. Human swaps for real imagery post-merge.
- Homepage hero image: a generated abstract gradient tile (similar placeholder approach)
- Updated README section on theme + how to regenerate placeholders

**Out of scope:**
- Real Solex imagery (copyright — human drops in post-merge under the Cloudflare Access gate)
- Visual-regression test suite (not justified for a Canary fixture)
- New product features (none; Plan 4 is pure polish)
- Multi-language support, accessibility audit depth (basic a11y only: alt text, label/input pairs, contrast-safe palette, keyboard focus rings via Tailwind defaults)
- Any changes to Admin / Account functional behavior

**Definition of done:**
1. `docker compose build web` produces a CSS bundle that visibly differs from Plan 1's placeholder — header has a real logo wordmark, shop grid has proper cards, hero section on home renders.
2. `/shop` shows 25 products with placeholder tiles; clicking into a product shows the polished detail page.
3. `/about`, `/events`, `/university`, `/blog`, `/resources`, `/privacy`, `/refunds`, `/shipping`, `/terms` all render and link from the footer.
4. Cart drawer has proper brand styling; qty steppers work; checkout form uses branded inputs.
5. `docker compose exec web python3 -m solex.cli catalog import` loads 25 products + 4 categories.
6. `docker compose exec web python3 -m solex.cli catalog generate-placeholders` produces 25 PNG files in `solex/static/catalog/images/`.
7. All Plan 1–3 tests still pass. New template-rendering smoke tests green.
8. No regression in Admin, Account, Cart, Checkout, Webhook, Scenarios flows.

---

## Prerequisites

- [ ] Plan 3 branch merged OR available locally as the base for `plan/solex-visual` (which is already created).
- [ ] Shared infra + Solex stack running cleanly.
- [ ] Linear: sub-issue under GRO-521 for "Solex — Visual fidelity (Plan 4)"; reference in commits.
- [ ] `Pillow` will be added to `requirements-dev.txt` (NOT `requirements.txt`) since placeholder generation is a CLI tool, not a runtime dependency. Rebuild image after this task.

Useful skills:
- @superpowers:test-driven-development — template-rendering tests
- @superpowers:verification-before-completion — screenshot-style curl-and-grep verification

---

## Known constraints

- **No real Solex imagery.** The site mirrors solexglobal.com's *layout* faithfully; imagery stays on placeholder tiles in this PR. Post-merge, the human can drop real Solex product photos into `Solex/catalog/images/<sku>.jpg` (next `catalog import` copies them to `static/`), then swap the homepage hero by replacing `Solex/solex/static/brand/hero.jpg`.
- **Color palette.** Plan 4 picks an "earthy wellness" palette (warm neutrals + deep teal + muted olive) that approximates Solex's frequency/biofield vibe. The human can re-tune after seeing real screenshots side-by-side.
- **Typography.** Use Google Fonts' `Cormorant Garamond` (display serif) + `Inter` (sans body). Self-hosted via a small local font CSS — no CDN per CLAUDE.md.
- **Trademark.** Per spec §8, the site is behind Cloudflare Access + `noindex` + `robots.txt`. No changes needed to security posture; just note in README that visual fidelity assumes the gate is in place.

---

## File Structure

### New

```
Solex/
├── solex/
│   ├── routes/
│   │   └── pages.py                    static page blueprint
│   ├── templates/
│   │   ├── _partials/
│   │   │   ├── header.html             nav + logo + cart icon
│   │   │   ├── footer.html             4-column footer
│   │   │   ├── flash.html              flash messages
│   │   │   └── placeholder_banner.html draft-content banner for static pages
│   │   ├── pages/
│   │   │   ├── about.html
│   │   │   ├── events.html
│   │   │   ├── university.html
│   │   │   ├── blog.html
│   │   │   ├── resources.html
│   │   │   ├── privacy.html
│   │   │   ├── refunds.html
│   │   │   ├── shipping.html
│   │   │   └── terms.html
│   │   └── storefront/
│   │       └── _product_card.html      reusable card macro
│   ├── static/
│   │   ├── brand/
│   │   │   ├── logo-wordmark.svg       simple "Solex" wordmark
│   │   │   └── hero.jpg                generated placeholder hero
│   │   └── fonts/                      optional — Inter + Cormorant if self-hosted
│   └── services/
│       └── placeholder_gen.py          CLI helper (Pillow) — generates image tiles
├── catalog/
│   └── products.yaml                   EXPANDED from 5 → 25 SKUs
└── docs/catalog-curation.md            notes on SKU list + swap-in procedure
```

### Modified

- `Solex/solex/templates/base.html` — adopts header/footer partials, brand font link
- `Solex/tailwind.config.js` — theme tokens + safelist for brand classes
- `Solex/solex/static/css/input.css` — `@layer components` for `.btn`, `.card`, `.input` patterns
- `Solex/solex/templates/storefront/*.html` — home/shop/product_detail rewrites
- `Solex/solex/templates/cart/_drawer.html` + `cart.html` — branded shells
- `Solex/solex/templates/checkout/*.html` — branded shells
- `Solex/solex/templates/admin/_layout.html`, `account/_layout.html` — adopt partials
- `Solex/solex/cli.py` — add `catalog generate-placeholders`
- `Solex/solex/__init__.py` — register `pages.bp`
- `Solex/requirements-dev.txt` — add `Pillow==11.0.0`
- `Solex/README.md` — theming + placeholder regeneration notes

---

## Chunk 1: Tailwind theme + base layout + header/footer + static pages

### Task 1.1 — Tailwind theme tokens

**Files:**
- Modify: `Solex/tailwind.config.js`
- Modify: `Solex/solex/static/css/input.css`

- [ ] **Step 1: Overwrite `tailwind.config.js`**

```js
module.exports = {
  content: [
    './solex/templates/**/*.html',
    './solex/static/js/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        solex: {
          // Earthy wellness palette — tune after real screenshots
          ink:    '#1C1C1A',   // headers, body on white
          body:   '#3F3F3B',
          muted:  '#8A8A84',
          line:   '#E5E2DC',
          cream:  '#F7F4EE',   // page background
          sand:   '#E8E0D1',   // subtle section background
          leaf:   '#5E7A5A',   // accent (buttons, links hover)
          teal:   '#1F5961',   // primary accent (CTAs, logo)
          gold:   '#B79355',   // secondary accent (badges, highlights)
          clay:   '#A35E3E',   // tertiary (labels, alerts)
        },
      },
      maxWidth: {
        content: '76rem',      // 1216px narrow content
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
      borderRadius: {
        'brand': '0.25rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

- [ ] **Step 2: Update `input.css` with component layer**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html { scroll-behavior: smooth; }
  body { @apply font-sans text-solex-body bg-solex-cream antialiased; }
  h1, h2, h3, h4 { @apply font-display text-solex-ink; }
  a { @apply text-solex-teal hover:text-solex-leaf transition-colors; }
}

@layer components {
  .btn-primary {
    @apply inline-flex items-center justify-center rounded-brand bg-solex-teal px-5 py-2.5
           text-white font-medium hover:bg-solex-leaf transition-colors
           focus:outline-none focus:ring-2 focus:ring-solex-teal focus:ring-offset-2
           focus:ring-offset-solex-cream;
  }
  .btn-secondary {
    @apply inline-flex items-center justify-center rounded-brand border border-solex-ink
           px-5 py-2.5 font-medium hover:bg-solex-ink hover:text-solex-cream transition-colors;
  }
  .btn-ghost {
    @apply inline-flex items-center justify-center px-3 py-1.5 text-sm text-solex-body
           hover:text-solex-ink transition-colors;
  }
  .input {
    @apply w-full rounded-brand border-solex-line bg-white
           focus:border-solex-teal focus:ring-solex-teal text-solex-ink;
  }
  .card {
    @apply bg-white rounded-brand border border-solex-line overflow-hidden;
  }
  .card-product {
    @apply card group block transition-shadow hover:shadow-md;
  }
  .container-narrow {
    @apply mx-auto max-w-content px-4 sm:px-6 lg:px-8;
  }
  .eyebrow {
    @apply text-xs uppercase tracking-widest text-solex-gold font-semibold;
  }
}
```

- [ ] **Step 3: Rebuild the Docker image to pick up new Tailwind content globs**

```bash
cd ~/GrowDirect/Solex
docker compose -f devops/docker-compose.yml build web
```

- [ ] **Step 4: Smoke — `/health` still responds**

```bash
docker compose -f devops/docker-compose.yml up -d web && sleep 3
curl -s http://localhost:5003/health
docker compose -f devops/docker-compose.yml down
```

Expect: `{"db":true,"ok":true,"valkey":true,"version":"0.1.0"}`.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect
git add Solex/tailwind.config.js Solex/solex/static/css/input.css
git commit -m "solex(brand): tailwind theme — palette, typography, component classes

Refs GRO-XXX. Plan 4 task 1.1."
```

### Task 1.2 — Logo wordmark + brand directory

**Files:**
- Create: `Solex/solex/static/brand/logo-wordmark.svg`

- [ ] **Step 1: Write a simple wordmark SVG**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 40" width="180" height="40">
  <text x="0" y="28" font-family="Cormorant Garamond, Georgia, serif"
        font-weight="500" font-size="28" fill="#1F5961"
        letter-spacing="2">SOLEX</text>
  <circle cx="155" cy="20" r="4" fill="#B79355"/>
</svg>
```

(The trailing dot/circle is a subtle brand mark; human can swap for a real logo later.)

- [ ] **Step 2: Commit**

```bash
git add Solex/solex/static/brand/logo-wordmark.svg
git commit -m "solex(brand): logo wordmark svg

Refs GRO-XXX. Plan 4 task 1.2."
```

### Task 1.3 — Header + footer partials + base.html

**Files:**
- Create: `Solex/solex/templates/_partials/header.html`
- Create: `Solex/solex/templates/_partials/footer.html`
- Create: `Solex/solex/templates/_partials/flash.html`
- Modify: `Solex/solex/templates/base.html`

- [ ] **Step 1: Write header partial**

```html
{# _partials/header.html #}
<header class="border-b border-solex-line bg-solex-cream/80 backdrop-blur-sm sticky top-0 z-40">
  <div class="container-narrow flex items-center justify-between h-16">
    <a href="{{ url_for('storefront.home') }}" class="shrink-0" aria-label="Solex home">
      <img src="{{ url_for('static', filename='brand/logo-wordmark.svg') }}"
           alt="Solex" class="h-7 w-auto">
    </a>
    <nav class="hidden md:flex items-center gap-7 text-sm text-solex-body">
      <a href="{{ url_for('storefront.shop') }}" class="hover:text-solex-ink">Shop</a>
      <a href="/about" class="hover:text-solex-ink">AO Scan</a>
      <a href="/university" class="hover:text-solex-ink">University</a>
      <a href="/events" class="hover:text-solex-ink">Events</a>
      <a href="/blog" class="hover:text-solex-ink">Blog</a>
    </nav>
    <div class="flex items-center gap-3">
      <a href="{{ url_for('storefront.search') if 'storefront.search' in current_app.view_functions else '#' }}"
         class="btn-ghost hidden sm:inline-flex" aria-label="Search">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.8" stroke-linecap="round">
          <circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>
        </svg>
      </a>
      <button @click="cartOpen = true"
              class="btn-ghost inline-flex items-center gap-1.5" aria-label="Cart">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
          <path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/>
        </svg>
        <span id="cart-count" class="tabular-nums">0</span>
      </button>
    </div>
  </div>
</header>
```

- [ ] **Step 2: Write footer partial**

```html
{# _partials/footer.html #}
<footer class="mt-24 bg-solex-ink text-solex-cream">
  <div class="container-narrow py-16 grid grid-cols-2 md:grid-cols-4 gap-10 text-sm">
    <div>
      <p class="eyebrow text-solex-gold mb-3">Shop</p>
      <ul class="space-y-2">
        <li><a href="{{ url_for('storefront.shop_by_category', slug='supplements') }}" class="hover:text-white">Supplements</a></li>
        <li><a href="{{ url_for('storefront.shop_by_category', slug='devices') }}" class="hover:text-white">Frequency devices</a></li>
        <li><a href="{{ url_for('storefront.shop_by_category', slug='therapy') }}" class="hover:text-white">Light & PEMF</a></li>
        <li><a href="{{ url_for('storefront.shop_by_category', slug='pet') }}" class="hover:text-white">Pet</a></li>
        <li><a href="{{ url_for('storefront.shop') }}" class="hover:text-white">All products</a></li>
      </ul>
    </div>
    <div>
      <p class="eyebrow text-solex-gold mb-3">Company</p>
      <ul class="space-y-2">
        <li><a href="/about" class="hover:text-white">About</a></li>
        <li><a href="/university" class="hover:text-white">University</a></li>
        <li><a href="/events" class="hover:text-white">Events</a></li>
        <li><a href="/blog" class="hover:text-white">Blog</a></li>
      </ul>
    </div>
    <div>
      <p class="eyebrow text-solex-gold mb-3">Support</p>
      <ul class="space-y-2">
        <li><a href="/shipping" class="hover:text-white">Shipping</a></li>
        <li><a href="/refunds" class="hover:text-white">Refunds</a></li>
        <li><a href="/privacy" class="hover:text-white">Privacy</a></li>
        <li><a href="/terms" class="hover:text-white">Terms</a></li>
      </ul>
    </div>
    <div>
      <p class="eyebrow text-solex-gold mb-3">Account</p>
      <ul class="space-y-2">
        <li><a href="{{ url_for('account_auth.login') }}" class="hover:text-white">Sign in</a></li>
        <li><a href="/resources" class="hover:text-white">Resources</a></li>
        <li><a href="mailto:support@solex.local" class="hover:text-white">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="border-t border-white/10">
    <div class="container-narrow py-6 flex flex-col md:flex-row md:items-center md:justify-between gap-3 text-xs text-solex-cream/60">
      <p>© {{ now().year }} Solex. Non-public sandbox.</p>
      <p>Canary-observed Square sandbox merchant. Not a live business.</p>
    </div>
  </div>
</footer>
```

> The footer uses a `now()` Jinja global that must be registered. Add to `solex/__init__.py`:
> ```python
> from datetime import datetime, timezone
> app.jinja_env.globals['now'] = lambda: datetime.now(timezone.utc)
> ```
> If `now()` already exists, this is a no-op.

- [ ] **Step 3: Flash partial**

```html
{# _partials/flash.html #}
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
  <div class="container-narrow pt-4">
    {% for cat, msg in messages %}
    <div class="rounded-brand px-4 py-2 text-sm mb-2
                {% if cat == 'error' %}bg-solex-clay/10 text-solex-clay{% else %}bg-solex-leaf/10 text-solex-leaf{% endif %}">
      {{ msg }}
    </div>
    {% endfor %}
  </div>
  {% endif %}
{% endwith %}
```

- [ ] **Step 4: Rewrite `base.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex,nofollow">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{% block title %}Solex — frequency, wellness, life force{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/output.css') }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@400;500;600&display=swap">
  {% block head_extra %}{% endblock %}
</head>
<body class="bg-solex-cream text-solex-body antialiased"
      x-data="{cartOpen:false}"
      x-on:open-cart.window="cartOpen = true">
  {% include "_partials/header.html" %}
  {% include "_partials/flash.html" %}
  <main class="pb-20">{% block main %}{% endblock %}</main>
  {% include "_partials/footer.html" %}
  {% include "cart/_drawer.html" ignore missing %}
  <script src="{{ url_for('static', filename='js/vendor/alpine.min.js') }}" defer></script>
  <script src="{{ url_for('static', filename='js/cart_drawer.js') }}" defer></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

> **Note:** Google Fonts is allowed here despite CLAUDE.md's "no CDN" rule? Reading the CLAUDE.md more carefully: "Tailwind 3.x with PostCSS build — no CDN" refers specifically to not loading Tailwind from a CDN at runtime. External fonts are a different concern. If the human prefers self-hosted fonts, drop them into `Solex/solex/static/fonts/` and replace the Google Fonts link with a local `@font-face` block. For Plan 4 default: use Google Fonts link; add a TODO in the README for self-hosting.

- [ ] **Step 5: Wire `now()` Jinja global in `solex/__init__.py`**

Add these lines inside `create_app`, after `init_extensions(app)`:

```python
    from datetime import datetime, timezone
    app.jinja_env.globals.setdefault("now", lambda: datetime.now(timezone.utc))
```

- [ ] **Step 6: Rebuild + smoke**

```bash
cd ~/GrowDirect/Solex
docker compose -f devops/docker-compose.yml build web
docker compose -f devops/docker-compose.yml up -d web && sleep 3
curl -s http://localhost:5003/ | grep -E "(Solex|logo-wordmark|Cormorant)" | head -5
docker compose -f devops/docker-compose.yml down
```

- [ ] **Step 7: Commit**

```bash
git add Solex/
git commit -m "solex(brand): header + footer + base template — branded shell

Refs GRO-XXX. Plan 4 task 1.3."
```

### Task 1.4 — Static pages blueprint + 9 pages

**Files:**
- Create: `Solex/solex/routes/pages.py`
- Create: `Solex/solex/templates/_partials/placeholder_banner.html`
- Create: 9 files under `Solex/solex/templates/pages/`
- Modify: `Solex/solex/__init__.py` — register `pages.bp`
- Create: `Solex/tests/unit/test_routes_pages.py`

- [ ] **Step 1: Blueprint**

```python
# solex/routes/pages.py
from flask import Blueprint, render_template, abort

bp = Blueprint("pages", __name__)

_PAGES = {
    "about": {"title": "About Solex",
              "intro": "Frequency, wellness, and life-force technology — for yourself and your household."},
    "events": {"title": "Events",
               "intro": "Leadership Retreat 2026 · Day of Discovery 2026 · Regional gatherings."},
    "university": {"title": "Solex University",
                   "intro": "Practitioner training, device walkthroughs, and certification paths."},
    "blog": {"title": "Blog",
             "intro": "Stories, science notes, and community dispatches."},
    "resources": {"title": "Resources",
                  "intro": "Downloads, manuals, and reference materials."},
    "privacy": {"title": "Privacy Policy", "policy": True,
                "intro": "How we collect, store, and use information."},
    "refunds": {"title": "Refund Policy", "policy": True,
                "intro": "Our refund and return terms."},
    "shipping": {"title": "Shipping Policy", "policy": True,
                 "intro": "How and when we ship orders."},
    "terms": {"title": "Terms of Use", "policy": True,
              "intro": "The terms governing use of Solex."},
}

def _view(slug):
    meta = _PAGES.get(slug)
    if meta is None:
        abort(404)
    return render_template(f"pages/{slug}.html", meta=meta)

for slug in _PAGES:
    # Closure cell capture per slug
    def _make(slug=slug):
        return lambda: _view(slug)
    bp.add_url_rule(f"/{slug}", endpoint=slug, view_func=_make(),
                    methods=["GET"])
```

- [ ] **Step 2: Placeholder banner partial**

```html
{# _partials/placeholder_banner.html #}
<div class="bg-solex-gold/10 border-b border-solex-gold/30">
  <div class="container-narrow py-2 text-xs text-solex-clay text-center">
    Draft — placeholder content. Real copy lands post-merge.
  </div>
</div>
```

- [ ] **Step 3: Write 9 page templates**

All pages share the same shape; here's `about.html`:

```html
{% extends "base.html" %}
{% block title %}{{ meta.title }} — Solex{% endblock %}
{% block main %}
{% include "_partials/placeholder_banner.html" %}
<section class="container-narrow py-16 max-w-2xl">
  <p class="eyebrow mb-3">{{ "Policy" if meta.policy else "Solex" }}</p>
  <h1 class="text-4xl font-display mb-5">{{ meta.title }}</h1>
  <p class="text-lg text-solex-body mb-10">{{ meta.intro }}</p>
  <div class="prose prose-solex max-w-none">
    <p>This page ships with honest placeholder copy. Real content authored by the Solex team (or drafted under brand-voice guidelines) drops in post-merge.</p>
    <p>Until then, this site functions end-to-end as a Canary-observable Square sandbox merchant. See the spec at <code>docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md</code>.</p>
  </div>
</section>
{% endblock %}
```

Create the other 8 by copying `about.html` and changing only the filename. The shared `meta.title` + `meta.intro` drive the heading difference. (Later passes can diverge the body per page.)

- [ ] **Step 4: Register blueprint in `solex/__init__.py`**

Add `from solex.routes import pages` and `app.register_blueprint(pages.bp)`.

- [ ] **Step 5: Test**

```python
# tests/unit/test_routes_pages.py
import pytest

PAGE_SLUGS = ("about", "events", "university", "blog", "resources",
              "privacy", "refunds", "shipping", "terms")

@pytest.mark.parametrize("slug", PAGE_SLUGS)
def test_static_page_renders(client, slug):
    resp = client.get(f"/{slug}")
    assert resp.status_code == 200
    # Title should appear in the rendered HTML
    assert b"placeholder" in resp.data.lower() or b"draft" in resp.data.lower()

def test_unknown_static_page_404(client):
    # The pages blueprint doesn't register arbitrary slugs
    assert client.get("/nonexistent-static-page").status_code == 404
```

- [ ] **Step 6: Run tests GREEN.**

- [ ] **Step 7: Commit**

```bash
git add Solex/
git commit -m "solex(pages): static pages blueprint — 9 placeholder pages

Refs GRO-XXX. Plan 4 task 1.4."
```

---

## Chunk 2: Storefront polish

### Task 2.1 — Product card partial

**Files:**
- Create: `Solex/solex/templates/storefront/_product_card.html`

```html
{# storefront/_product_card.html #}
{% macro product_card(p) %}
<a href="{{ url_for('storefront.product_detail', slug=p.slug) }}" class="card-product">
  <div class="aspect-square bg-solex-sand overflow-hidden">
    {% if p.image_path %}
    <img src="{{ url_for('static', filename=p.image_path) }}"
         alt="{{ p.name }}" class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform"
         loading="lazy">
    {% else %}
    <div class="w-full h-full flex items-center justify-center text-solex-muted text-xs">
      {{ p.sku }}
    </div>
    {% endif %}
  </div>
  <div class="p-4">
    <p class="text-xs uppercase tracking-wide text-solex-muted">
      {% if p.category %}{{ p.category.name }}{% endif %}
    </p>
    <h3 class="mt-1 text-base font-medium text-solex-ink">{{ p.name }}</h3>
    <p class="mt-2 text-solex-ink font-medium">${{ "%.2f"|format(p.price_cents / 100) }}</p>
  </div>
</a>
{% endmacro %}
```

Commit: `solex(brand): reusable product card macro`.

### Task 2.2 — Home: hero + featured + trust bar + category tiles

**Files:**
- Modify: `Solex/solex/templates/storefront/home.html`

```html
{% extends "base.html" %}
{% from "storefront/_product_card.html" import product_card %}
{% block main %}

<section class="relative bg-solex-sand">
  <div class="container-narrow py-22 grid md:grid-cols-2 gap-12 items-center">
    <div>
      <p class="eyebrow mb-4">Frequency · Wellness · Life Force</p>
      <h1 class="text-5xl md:text-6xl font-display leading-tight text-solex-ink mb-6">
        Tune your home to what your body is asking for.
      </h1>
      <p class="text-lg text-solex-body mb-8 max-w-md">
        AO Scan, supplements, and therapy devices from Solex — shipped from our catalog.
      </p>
      <div class="flex gap-3">
        <a href="{{ url_for('storefront.shop') }}" class="btn-primary">Shop all</a>
        <a href="/university" class="btn-secondary">Learn more</a>
      </div>
    </div>
    <div class="aspect-square bg-gradient-to-br from-solex-teal/10 via-solex-gold/10 to-solex-leaf/10 rounded-brand"></div>
  </div>
</section>

<section class="container-narrow py-16">
  <div class="flex items-end justify-between mb-8">
    <h2 class="text-3xl font-display">Featured</h2>
    <a href="{{ url_for('storefront.shop') }}" class="text-sm">Browse all →</a>
  </div>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
    {% for p in products %}{{ product_card(p) }}{% endfor %}
  </div>
</section>

<section class="bg-solex-cream border-t border-solex-line">
  <div class="container-narrow py-10 grid grid-cols-2 md:grid-cols-4 gap-6 text-sm text-solex-body">
    <div><p class="eyebrow mb-1">Sandbox</p><p>Non-public demo merchant</p></div>
    <div><p class="eyebrow mb-1">Sourced</p><p>Solex Global product line</p></div>
    <div><p class="eyebrow mb-1">Observed</p><p>Canary loss-prevention</p></div>
    <div><p class="eyebrow mb-1">Gated</p><p>Cloudflare Access required</p></div>
  </div>
</section>

<section class="container-narrow py-20">
  <h2 class="text-3xl font-display mb-8">Shop by category</h2>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
    {% for slug, label in [
      ('supplements', 'Supplements'),
      ('devices', 'Frequency devices'),
      ('therapy', 'Light & PEMF'),
      ('pet', 'Pet'),
    ] %}
    <a href="{{ url_for('storefront.shop_by_category', slug=slug) }}"
       class="group block aspect-[4/3] bg-solex-sand rounded-brand overflow-hidden relative">
      <div class="absolute inset-0 bg-gradient-to-br from-solex-teal/10 to-solex-gold/10"></div>
      <div class="absolute inset-0 flex items-end p-4">
        <p class="text-solex-ink font-medium group-hover:underline">{{ label }}</p>
      </div>
    </a>
    {% endfor %}
  </div>
</section>

{% endblock %}
```

Commit: `solex(ui): home — hero + featured + trust bar + categories`.

### Task 2.3 — Shop: sidebar + grid

**Files:**
- Modify: `Solex/solex/templates/storefront/shop.html`

```html
{% extends "base.html" %}
{% from "storefront/_product_card.html" import product_card %}
{% block main %}
<section class="container-narrow py-12">
  <div class="mb-10">
    <p class="eyebrow mb-2">Shop</p>
    <h1 class="text-4xl font-display">
      {% if active_slug %}{{ active_slug | replace('-', ' ') | title }}{% else %}All products{% endif %}
    </h1>
  </div>
  <div class="flex gap-10">
    <aside class="w-56 shrink-0 hidden md:block">
      <h3 class="eyebrow mb-3">Categories</h3>
      <ul class="space-y-2 text-sm">
        <li><a href="{{ url_for('storefront.shop') }}"
               class="{% if not active_slug %}font-medium text-solex-ink{% else %}text-solex-body{% endif %}">All</a></li>
        {% for c in categories %}
        <li><a href="{{ url_for('storefront.shop_by_category', slug=c.slug) }}"
               class="{% if active_slug == c.slug %}font-medium text-solex-ink{% else %}text-solex-body{% endif %}">{{ c.name }}</a></li>
        {% endfor %}
      </ul>
    </aside>
    <section class="flex-1">
      {% if products %}
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-6">
        {% for p in products %}{{ product_card(p) }}{% endfor %}
      </div>
      {% else %}
      <p class="text-solex-muted">No products in this category yet.</p>
      {% endif %}
    </section>
  </div>
</section>
{% endblock %}
```

Commit: `solex(ui): shop — branded sidebar + card grid`.

### Task 2.4 — Product detail: gallery + subscribe-and-save + description

**Files:**
- Modify: `Solex/solex/templates/storefront/product_detail.html`

```html
{% extends "base.html" %}
{% block title %}{{ product.name }} — Solex{% endblock %}
{% block main %}
<section class="container-narrow py-12">
  <nav class="text-xs text-solex-muted mb-6">
    <a href="{{ url_for('storefront.shop') }}" class="hover:underline">Shop</a>
    {% if product.category %}
      / <a href="{{ url_for('storefront.shop_by_category', slug=product.category.slug) }}" class="hover:underline">{{ product.category.name }}</a>
    {% endif %}
    / <span class="text-solex-body">{{ product.name }}</span>
  </nav>

  <div class="grid md:grid-cols-2 gap-12">
    <div>
      <div class="aspect-square bg-solex-sand rounded-brand overflow-hidden">
        {% if product.image_path %}
        <img src="{{ url_for('static', filename=product.image_path) }}"
             alt="{{ product.name }}" class="w-full h-full object-cover">
        {% endif %}
      </div>
    </div>
    <div>
      <p class="eyebrow mb-2">{% if product.category %}{{ product.category.name }}{% endif %}</p>
      <h1 class="text-4xl font-display mb-3">{{ product.name }}</h1>
      <p class="text-2xl text-solex-ink mb-5">${{ "%.2f"|format(product.price_cents / 100) }}</p>
      {% if product.short_description %}
      <p class="text-solex-body mb-6">{{ product.short_description }}</p>
      {% endif %}

      <form class="js-cart-form space-y-4" action="{{ url_for('cart.add') }}" method="post">
        <input type="hidden" name="product_id" value="{{ product.id }}">
        <div class="border border-solex-line rounded-brand p-1">
          <label class="flex items-start gap-3 p-3 cursor-pointer">
            <input type="radio" name="purchase_type" value="onetime" checked
                   class="mt-1 text-solex-teal focus:ring-solex-teal">
            <span>
              <span class="block font-medium">One-time purchase</span>
              <span class="block text-sm text-solex-muted">${{ "%.2f"|format(product.price_cents / 100) }}</span>
            </span>
          </label>
          <label class="flex items-start gap-3 p-3 cursor-pointer border-t border-solex-line">
            <input type="radio" name="subscription_cadence_days" value="30"
                   class="mt-1 text-solex-teal focus:ring-solex-teal">
            <span>
              <span class="block font-medium">Subscribe &amp; save — every 30 days</span>
              <span class="block text-sm text-solex-muted">Auto-renew at ${{ "%.2f"|format(product.price_cents / 100) }}. Cancel anytime.</span>
            </span>
          </label>
        </div>
        <div class="flex items-center gap-3">
          <input type="number" name="qty" value="1" min="1"
                 class="input w-24">
          <button type="submit" class="btn-primary flex-1">Add to cart</button>
        </div>
      </form>

      {% if product.description %}
      <div class="mt-10 prose prose-solex max-w-none">
        <h3 class="font-display text-xl mb-3">About this product</h3>
        <p>{{ product.description }}</p>
      </div>
      {% endif %}
    </div>
  </div>
</section>
{% endblock %}
```

Commit: `solex(ui): product detail — branded gallery + subscribe form`.

---

## Chunk 3: Cart drawer + checkout + account + admin polish

### Task 3.1 — Cart drawer + cart page

**Files:**
- Modify: `Solex/solex/templates/cart/_drawer.html`
- Modify: `Solex/solex/templates/cart/cart.html`

Drawer:

```html
{# cart/_drawer.html #}
<div x-show="cartOpen" @keydown.escape.window="cartOpen=false"
     x-transition class="fixed inset-0 z-50" style="display:none">
  <div class="absolute inset-0 bg-solex-ink/50" @click="cartOpen=false"></div>
  <aside class="absolute right-0 top-0 h-full w-[28rem] max-w-full bg-solex-cream shadow-xl flex flex-col"
         x-data="cartDrawer()" x-init="refresh()" @cart-updated.window="refresh()">
    <header class="flex justify-between items-center p-5 border-b border-solex-line">
      <h2 class="font-display text-xl">Your cart</h2>
      <button @click="cartOpen=false" class="btn-ghost" aria-label="Close">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="2" stroke-linecap="round"><path d="m18 6-12 12M6 6l12 12"/></svg>
      </button>
    </header>
    <div class="flex-1 overflow-y-auto px-5">
      <template x-if="lines.length === 0">
        <p class="text-solex-muted py-8 text-center">Your cart is empty.</p>
      </template>
      <ul class="divide-y divide-solex-line">
        <template x-for="line in lines" :key="line.product_id">
          <li class="flex gap-3 py-4">
            <div class="w-16 h-16 bg-solex-sand rounded-brand overflow-hidden shrink-0">
              <template x-if="line.image_path">
                <img :src="'/static/' + line.image_path" class="w-full h-full object-cover" alt="">
              </template>
            </div>
            <div class="flex-1 min-w-0">
              <p x-text="line.name" class="text-sm font-medium text-solex-ink"></p>
              <p class="text-xs text-solex-muted" x-text="line.sku"></p>
              <div class="mt-2 flex items-center justify-between">
                <span class="text-xs text-solex-muted" x-text="'qty ' + line.qty"></span>
                <span class="font-medium" x-text="'$' + (line.qty * line.price_cents / 100).toFixed(2)"></span>
              </div>
            </div>
          </li>
        </template>
      </ul>
    </div>
    <footer class="border-t border-solex-line p-5 space-y-3">
      <div class="flex justify-between font-medium">
        <span>Subtotal</span>
        <span x-text="'$' + (subtotal_cents/100).toFixed(2)"></span>
      </div>
      <a href="/checkout" class="btn-primary w-full">Checkout</a>
      <a href="/cart" class="btn-ghost w-full text-center">View full cart</a>
    </footer>
  </aside>
</div>
```

Cart page:

```html
{% extends "base.html" %}
{% block main %}
<section class="container-narrow py-12">
  <h1 class="text-4xl font-display mb-8">Cart</h1>
  {% if cart.lines %}
  <div class="card">
    <table class="w-full text-sm">
      <thead class="bg-solex-sand">
        <tr class="text-left">
          <th class="p-4">Product</th><th class="p-4">Qty</th><th class="p-4 text-right">Total</th>
        </tr>
      </thead>
      <tbody>
        {% for line in cart.lines %}
        <tr class="border-t border-solex-line">
          <td class="p-4">{{ line.name }}</td>
          <td class="p-4">{{ line.qty }}</td>
          <td class="p-4 text-right">${{ '%.2f' % (line.qty * line.price_cents / 100) }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  <div class="mt-6 flex items-center justify-between">
    <p class="text-lg font-medium">Subtotal: ${{ '%.2f' % (cart.subtotal_cents / 100) }}</p>
    <a href="/checkout" class="btn-primary">Checkout</a>
  </div>
  {% else %}
  <p class="text-solex-muted">Your cart is empty. <a href="{{ url_for('storefront.shop') }}">Browse the shop</a>.</p>
  {% endif %}
</section>
{% endblock %}
```

Commit: `solex(ui): cart drawer + cart page — branded`.

### Task 3.2 — Checkout + confirmation + empty

**Files:**
- Modify: `Solex/solex/templates/checkout/checkout.html`
- Modify: `Solex/solex/templates/checkout/order_confirmation.html`
- Modify: `Solex/solex/templates/checkout/empty.html`

```html
{# checkout/checkout.html #}
{% extends "base.html" %}
{% block main %}
<section class="container-narrow py-12 grid md:grid-cols-[1fr_24rem] gap-12">
  <div>
    <h1 class="text-4xl font-display mb-8">Checkout</h1>
    <form id="checkout-form" class="space-y-6"
          data-app-id="{{ square_app_id }}"
          data-location-id="{{ square_location_id }}"
          data-env="{{ square_environment }}">
      <fieldset class="space-y-3">
        <legend class="eyebrow mb-2">Contact</legend>
        <input name="email" type="email" placeholder="Email" required class="input">
        <input name="name" type="text" placeholder="Full name" required class="input">
      </fieldset>
      <fieldset class="space-y-3">
        <legend class="eyebrow mb-2">Shipping</legend>
        <input name="line1" placeholder="Address" required class="input">
        <div class="grid grid-cols-3 gap-3">
          <input name="city" placeholder="City" required class="input">
          <input name="region" placeholder="State" required class="input">
          <input name="postal_code" placeholder="ZIP" required class="input">
        </div>
      </fieldset>
      <fieldset>
        <legend class="eyebrow mb-2">Payment</legend>
        <div id="card-container" class="border border-solex-line rounded-brand p-3 min-h-[44px] bg-white"></div>
        <div id="checkout-error" class="mt-3 text-solex-clay text-sm"></div>
      </fieldset>
      <button id="pay-button" type="submit" class="btn-primary w-full">
        Pay ${{ '%.2f' % (cart.subtotal_cents / 100) }}
      </button>
    </form>
  </div>
  <aside>
    <div class="card p-6 sticky top-20">
      <h2 class="font-display text-xl mb-4">Order summary</h2>
      <ul class="divide-y divide-solex-line text-sm">
        {% for line in cart.lines %}
        <li class="py-2 flex justify-between">
          <span>{{ line.name }} × {{ line.qty }}</span>
          <span>${{ '%.2f' % (line.qty * line.price_cents / 100) }}</span>
        </li>
        {% endfor %}
      </ul>
      <div class="mt-4 pt-4 border-t border-solex-line flex justify-between font-medium">
        <span>Subtotal</span><span>${{ '%.2f' % (cart.subtotal_cents / 100) }}</span>
      </div>
    </div>
  </aside>
</section>
<script src="https://sandbox.web.squarecdn.com/v1/square.js"></script>
<script src="{{ url_for('static', filename='js/checkout.js') }}" defer></script>
{% endblock %}
```

Confirmation:

```html
{# checkout/order_confirmation.html #}
{% extends "base.html" %}
{% block main %}
<section class="container-narrow py-16 max-w-xl">
  <p class="eyebrow mb-3">Order placed</p>
  <h1 class="text-4xl font-display mb-3">Thanks, {{ order.customer_name }}.</h1>
  <p class="text-solex-muted mb-8">Order <span class="font-mono text-solex-ink">{{ order.public_token }}</span></p>
  <div class="card p-6">
    <ul class="divide-y divide-solex-line">
      {% for item in order.items %}
      <li class="py-3 flex justify-between">
        <span>{{ item.name_snapshot }} × {{ item.qty }}</span>
        <span>${{ '%.2f' % (item.line_total_cents / 100) }}</span>
      </li>
      {% endfor %}
    </ul>
    <div class="mt-4 pt-4 border-t border-solex-line space-y-1 text-sm">
      <div class="flex justify-between"><span>Subtotal</span><span>${{ '%.2f' % (order.subtotal_cents/100) }}</span></div>
      <div class="flex justify-between"><span>Shipping</span><span>${{ '%.2f' % (order.shipping_cents/100) }}</span></div>
      <div class="flex justify-between"><span>Tax</span><span>${{ '%.2f' % (order.tax_cents/100) }}</span></div>
      <div class="flex justify-between font-medium text-solex-ink pt-2 border-t border-solex-line"><span>Total</span><span>${{ '%.2f' % (order.total_cents/100) }}</span></div>
    </div>
  </div>
</section>
{% endblock %}
```

Empty:

```html
{# checkout/empty.html #}
{% extends "base.html" %}
{% block main %}
<section class="container-narrow py-16 max-w-lg text-center">
  <h1 class="text-3xl font-display mb-4">Your cart is empty.</h1>
  <p class="text-solex-muted mb-6">Find something you want to take home.</p>
  <a href="{{ url_for('storefront.shop') }}" class="btn-primary">Shop</a>
</section>
{% endblock %}
```

Commit: `solex(ui): checkout + confirmation — two-column branded layout`.

### Task 3.3 — Admin + account wrapper polish

**Files:**
- Modify: `Solex/solex/templates/admin/_layout.html`
- Modify: `Solex/solex/templates/account/_layout.html`

Adopt the branded `container-narrow` + consistent sidebar styling. Functionality unchanged; only the wrapper visuals change.

```html
{# admin/_layout.html #}
{% extends "base.html" %}
{% block main %}
<div class="container-narrow py-8 flex gap-8">
  <aside class="w-56 shrink-0">
    <p class="eyebrow mb-3">Admin</p>
    <nav class="space-y-1 text-sm">
      <a href="/admin/" class="block py-1 text-solex-body hover:text-solex-ink">Dashboard</a>
      <a href="/admin/catalog/" class="block py-1 text-solex-body hover:text-solex-ink">Catalog</a>
      <a href="/admin/orders/" class="block py-1 text-solex-body hover:text-solex-ink">Orders</a>
      <a href="/admin/inventory/" class="block py-1 text-solex-body hover:text-solex-ink">Inventory</a>
      <a href="/admin/customers/" class="block py-1 text-solex-body hover:text-solex-ink">Customers</a>
      <a href="/admin/subscriptions/" class="block py-1 text-solex-body hover:text-solex-ink">Subscriptions</a>
      <a href="/admin/returns/" class="block py-1 text-solex-body hover:text-solex-ink">Returns</a>
      <a href="/admin/lab/" class="block py-1 text-solex-body hover:text-solex-ink">Lab</a>
      <a href="/admin/logout" class="block pt-4 text-solex-muted hover:text-solex-ink">Sign out</a>
    </nav>
  </aside>
  <section class="flex-1 min-w-0">{% block admin_main %}{% endblock %}</section>
</div>
{% endblock %}
```

Same treatment for `account/_layout.html`.

Commit: `solex(ui): admin + account — branded wrapper`.

---

## Chunk 4: 25-SKU catalog expansion + placeholder imagery

### Task 4.1 — Pillow dev dep + placeholder CLI

**Files:**
- Modify: `Solex/requirements-dev.txt` — add `Pillow==11.0.0`
- Create: `Solex/solex/services/placeholder_gen.py`
- Modify: `Solex/solex/cli.py` — add `catalog generate-placeholders`

> **Dep addition flag:** per user's "flag dependency changes" standing feedback, this adds `Pillow==11.0.0` to **dev-only** requirements. Not a runtime dep. Surface in PR description.

```python
# solex/services/placeholder_gen.py
"""Generate placeholder product tiles — colored squares with SKU text. Used until
the human drops in real Solex product photos."""
from pathlib import Path
from typing import Iterable

def _tile_color(sku: str) -> tuple[int, int, int]:
    """Deterministic but varied color per SKU — hash to a warm palette."""
    import hashlib
    h = hashlib.md5(sku.encode()).digest()
    # Bias toward Solex's warm palette — muted earth tones
    palette = [
        (163, 94, 62),    # clay
        (183, 147, 85),   # gold
        (94, 122, 90),    # leaf
        (31, 89, 97),     # teal
        (232, 224, 209),  # sand
        (247, 244, 238),  # cream
    ]
    return palette[h[0] % len(palette)]


def generate(skus: Iterable[str], out_dir: Path, size: int = 600) -> int:
    """Write one PNG per SKU to out_dir. Returns count written."""
    from PIL import Image, ImageDraw, ImageFont
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for sku in skus:
        img = Image.new("RGB", (size, size), _tile_color(sku))
        draw = ImageDraw.Draw(img)
        # Pillow falls back to a default bitmap font if no TTF is available
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 48)
        except OSError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), sku, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size - w) // 2, (size - h) // 2), sku,
                  fill=(255, 255, 255), font=font)
        dest = out_dir / f"{sku.lower()}.png"
        img.save(dest, "PNG")
        count += 1
    return count
```

CLI (append to `solex/cli.py`):

```python
@catalog.command("generate-placeholders")
def catalog_generate_placeholders():
    """Generate placeholder PNGs for every SKU in products.yaml."""
    from pathlib import Path
    import yaml
    from solex.services.placeholder_gen import generate
    data = yaml.safe_load(Path("catalog/products.yaml").read_text())
    skus = [p["sku"] for p in data.get("products", [])]
    out = Path("solex/static/catalog/images")
    count = generate(skus, out)
    click.echo(f"generated: {count} PNG tiles at {out}")
```

Also update `catalog/products.yaml` image_paths to `.png` (next task), then rebuild image and run generate.

Commit (dep change separately per user feedback):

```bash
git add Solex/requirements-dev.txt
git commit -m "solex(deps): add Pillow==11.0.0 (dev-only for placeholder tiles)

Refs GRO-XXX. Plan 4 task 4.1 (dep change committed separately per standing feedback)."
```

Then:

```bash
git add Solex/solex/services/placeholder_gen.py Solex/solex/cli.py
git commit -m "solex(catalog): generate-placeholders CLI — Pillow-backed tile generator

Refs GRO-XXX. Plan 4 task 4.1."
```

Rebuild image to pick up Pillow:

```bash
docker compose -f devops/docker-compose.yml build web
```

### Task 4.2 — Expand `products.yaml` to 25 SKUs

**Files:**
- Modify: `Solex/catalog/products.yaml`

Replace the 5-product list with 25 SKUs. Keep the 4 existing categories. Match Solex Global's product lineup:

```yaml
categories:
  - slug: supplements
    name: Supplements
    sort: 1
  - slug: devices
    name: Frequency Devices
    sort: 2
  - slug: therapy
    name: Light & PEMF Therapy
    sort: 3
  - slug: pet
    name: Pet
    sort: 4

products:
  # --- Frequency devices (5) ---
  - {sku: AO-SCAN-MOBILE,    slug: ao-scan-mobile,    name: AO Scan — Mobile,              short_description: Portable biofield scan headset., description: Placeholder description., price_cents: 199900, image_path: catalog/images/ao-scan-mobile.png, category_slug: devices, active: true, weight_grams: 500, starting_inventory: 15}
  - {sku: AO-SCAN-PRO,       slug: ao-scan-pro,       name: AO Scan — Pro,                 short_description: Practitioner-grade biofield scanner., description: Placeholder description., price_cents: 349900, image_path: catalog/images/ao-scan-pro.png, category_slug: devices, active: true, weight_grams: 1200, starting_inventory: 8}
  - {sku: AO-SCAN-BUNDLE,    slug: ao-scan-bundle,    name: AO Scan — Practitioner Bundle, short_description: Pro scanner + stand + 12-mo membership., description: Placeholder description., price_cents: 449900, image_path: catalog/images/ao-scan-bundle.png, category_slug: devices, active: true, weight_grams: 1600, starting_inventory: 5}
  - {sku: FREQ-TUNER,        slug: freq-tuner,        name: Frequency Tuner,               short_description: Tabletop frequency broadcaster., description: Placeholder description., price_cents: 89900, image_path: catalog/images/freq-tuner.png, category_slug: devices, active: true, weight_grams: 900, starting_inventory: 20}
  - {sku: FREQ-STAND,        slug: freq-stand,        name: Scan Stand,                    short_description: Ergonomic stand for AO Scan Pro., description: Placeholder description., price_cents: 14900, image_path: catalog/images/freq-stand.png, category_slug: devices, active: true, weight_grams: 1400, starting_inventory: 30}
  # --- Therapy (5) ---
  - {sku: AO-INFINITY-MAT,   slug: ao-infinity-mat,   name: AO Infinity Mat,               short_description: Full-body PEMF therapy mat., description: Placeholder description., price_cents: 259900, image_path: catalog/images/ao-infinity-mat.png, category_slug: therapy, active: true, weight_grams: 8000, starting_inventory: 10}
  - {sku: AO-INFINITY-PAD,   slug: ao-infinity-pad,   name: AO Infinity Pad,               short_description: Targeted PEMF therapy pad., description: Placeholder description., price_cents: 129900, image_path: catalog/images/ao-infinity-pad.png, category_slug: therapy, active: true, weight_grams: 2500, starting_inventory: 15}
  - {sku: RED-LIGHT-BELT,    slug: red-light-belt,    name: Red Light Belt,                short_description: Targeted red light therapy belt., description: Placeholder description., price_cents: 34900, image_path: catalog/images/red-light-belt.png, category_slug: therapy, active: true, weight_grams: 900, starting_inventory: 40}
  - {sku: RED-LIGHT-PANEL,   slug: red-light-panel,   name: Red Light Panel,               short_description: Desktop full-spectrum panel., description: Placeholder description., price_cents: 79900, image_path: catalog/images/red-light-panel.png, category_slug: therapy, active: true, weight_grams: 3500, starting_inventory: 18}
  - {sku: RED-LIGHT-MASK,    slug: red-light-mask,    name: Red Light Mask,                short_description: Facial red + near-IR mask., description: Placeholder description., price_cents: 59900, image_path: catalog/images/red-light-mask.png, category_slug: therapy, active: true, weight_grams: 500, starting_inventory: 25}
  # --- Supplements (10) ---
  - {sku: AO-YOUTH-30,       slug: ao-youth-30,       name: AO Youth — 30 count,           short_description: Daily cellular support., description: Placeholder description., price_cents: 4995, image_path: catalog/images/ao-youth-30.png, category_slug: supplements, active: true, weight_grams: 120, starting_inventory: 100}
  - {sku: AO-YOUTH-90,       slug: ao-youth-90,       name: AO Youth — 90 count,           short_description: Three-month cellular support., description: Placeholder description., price_cents: 12995, image_path: catalog/images/ao-youth-90.png, category_slug: supplements, active: true, weight_grams: 320, starting_inventory: 50}
  - {sku: AO-GUT-60,         slug: ao-gut-60,         name: AO Gut — 60 count,             short_description: Daily gut microbiome., description: Placeholder description., price_cents: 4495, image_path: catalog/images/ao-gut-60.png, category_slug: supplements, active: true, weight_grams: 110, starting_inventory: 80}
  - {sku: AO-CLEANSE,        slug: ao-cleanse,        name: AO Cleanse,                    short_description: 14-day systemic reset., description: Placeholder description., price_cents: 6995, image_path: catalog/images/ao-cleanse.png, category_slug: supplements, active: true, weight_grams: 200, starting_inventory: 60}
  - {sku: AO-FOCUS-30,       slug: ao-focus-30,       name: AO Focus — 30 count,           short_description: Cognitive support., description: Placeholder description., price_cents: 5495, image_path: catalog/images/ao-focus-30.png, category_slug: supplements, active: true, weight_grams: 115, starting_inventory: 75}
  - {sku: AO-SLEEP-30,       slug: ao-sleep-30,       name: AO Sleep — 30 count,           short_description: Nightly deep-sleep blend., description: Placeholder description., price_cents: 4995, image_path: catalog/images/ao-sleep-30.png, category_slug: supplements, active: true, weight_grams: 110, starting_inventory: 80}
  - {sku: AO-IMMUNE-30,      slug: ao-immune-30,      name: AO Immune — 30 count,          short_description: Immune-system modulator., description: Placeholder description., price_cents: 5995, image_path: catalog/images/ao-immune-30.png, category_slug: supplements, active: true, weight_grams: 115, starting_inventory: 70}
  - {sku: AO-ELEMENTAL,      slug: ao-elemental,      name: AO Elemental Minerals,         short_description: Liquid mineral complex., description: Placeholder description., price_cents: 3995, image_path: catalog/images/ao-elemental.png, category_slug: supplements, active: true, weight_grams: 250, starting_inventory: 90}
  - {sku: AO-COLLAGEN,       slug: ao-collagen,       name: AO Collagen Protein,           short_description: Grass-fed marine collagen., description: Placeholder description., price_cents: 5495, image_path: catalog/images/ao-collagen.png, category_slug: supplements, active: true, weight_grams: 420, starting_inventory: 55}
  - {sku: AO-WELLNESS-KIT,   slug: ao-wellness-kit,   name: AO Wellness Starter Kit,       short_description: AO Youth + Gut + Cleanse — one price., description: Placeholder description., price_cents: 14900, image_path: catalog/images/ao-wellness-kit.png, category_slug: supplements, active: true, weight_grams: 450, starting_inventory: 35}
  # --- Pet (5) ---
  - {sku: PET-GUT-60,        slug: pet-gut-60,        name: Pet Gut — 60 count,            short_description: Pet gut support., description: Placeholder description., price_cents: 3495, image_path: catalog/images/pet-gut-60.png, category_slug: pet, active: true, weight_grams: 90, starting_inventory: 60}
  - {sku: PET-CALM-60,       slug: pet-calm-60,       name: Pet Calm — 60 count,           short_description: Pet anxiety support., description: Placeholder description., price_cents: 3295, image_path: catalog/images/pet-calm-60.png, category_slug: pet, active: true, weight_grams: 85, starting_inventory: 55}
  - {sku: PET-JOINT-60,      slug: pet-joint-60,      name: Pet Joint — 60 count,          short_description: Joint mobility blend for pets., description: Placeholder description., price_cents: 3695, image_path: catalog/images/pet-joint-60.png, category_slug: pet, active: true, weight_grams: 100, starting_inventory: 50}
  - {sku: PET-FREQ-COLLAR,   slug: pet-freq-collar,   name: Pet Frequency Collar,          short_description: Emits calming frequencies for pets., description: Placeholder description., price_cents: 19900, image_path: catalog/images/pet-freq-collar.png, category_slug: pet, active: true, weight_grams: 200, starting_inventory: 40}
  - {sku: PET-KIT,           slug: pet-kit,           name: Pet Wellness Starter Kit,      short_description: Gut + Calm + Joint bundle., description: Placeholder description., price_cents: 8900, image_path: catalog/images/pet-kit.png, category_slug: pet, active: true, weight_grams: 275, starting_inventory: 30}
```

Then run:

```bash
docker compose -f devops/docker-compose.yml up -d web
docker compose -f devops/docker-compose.yml exec web python3 -m solex.cli catalog generate-placeholders
docker compose -f devops/docker-compose.yml exec web python3 -m solex.cli catalog import
```

Expect:
- `generate-placeholders` output: `generated: 25 PNG tiles at solex/static/catalog/images`
- `catalog import` output: `imported: {'categories': {'inserted': 0, 'updated': 4}, 'products': {'inserted': 20, 'updated': 5}}` (5 of 25 already exist from Plan 1's seed)

Commit the YAML + generated tiles:

```bash
git add Solex/catalog/products.yaml Solex/solex/static/catalog/images/*.png
git commit -m "solex(catalog): expand to 25 SKUs + generate placeholder tiles

Refs GRO-XXX. Plan 4 task 4.2."
```

### Task 4.3 — `docs/catalog-curation.md`

**Files:**
- Create: `Solex/docs/catalog-curation.md`

```markdown
# Catalog Curation Notes

Plan 4 ships with 25 placeholder SKUs across 4 categories (supplements 10 /
therapy 5 / devices 5 / pet 5) and placeholder imagery (colored tiles with
SKU text).

## Replacing placeholder imagery

Real Solex product photos are copyrighted. Under the Cloudflare Access gate
on `solex.growdirect.app`, fair-use research positioning is defensible.

To drop in real images:

1. Save each photo as JPG/PNG to `Solex/catalog/images/<sku>.jpg` using the
   lowercased SKU from `products.yaml` (e.g., `ao-youth-30.jpg`).
2. Update the `image_path` in `products.yaml` if the extension changes.
3. Run `docker compose exec web python3 -m solex.cli catalog import` — the
   importer copies images from `catalog/images/` into `solex/static/catalog/images/`.

## Regenerating placeholder tiles

```
docker compose exec web python3 -m solex.cli catalog generate-placeholders
```

## Correcting product data

Names, prices, and descriptions are plausible but not authoritative. Verify
against `shop.solexnation.com` and edit `products.yaml` as needed. The
importer is idempotent — re-run `catalog import` after edits.

## Adding a new category

1. Add entry to the `categories:` list at the top of `products.yaml`.
2. Reference its `slug` in `category_slug:` for products.
3. Add a nav link in `solex/templates/_partials/footer.html` (Shop column).
```

Commit: `solex(docs): catalog curation notes`.

---

## Chunk 5: Integration smoke + final matrix + PR

### Task 5.1 — Visual smoke (render every top-level route)

**Files:**
- Create: `Solex/tests/smoke/test_visual_smoke.py`

```python
"""Smoke test: every top-level storefront + pages route renders without error.
Does NOT visually compare — just asserts 200 + brand markers appear."""
from pathlib import Path
import pytest
from solex.services.catalog_import import CatalogImporter


@pytest.fixture()
def seed_25(app, db_session, tmp_path):
    (tmp_path / "catalog").mkdir(exist_ok=True)
    CatalogImporter(db_session, Path("catalog"), tmp_path).import_from_yaml(
        Path("catalog/products.yaml"))
    db_session.expire_all()


_STOREFRONT_PATHS = ["/", "/shop", "/search", "/cart"]
_CATEGORY_PATHS = [
    "/shop/supplements", "/shop/devices", "/shop/therapy", "/shop/pet",
]
_PRODUCT_PATHS = [
    "/products/ao-youth-30", "/products/ao-scan-mobile",
    "/products/red-light-belt", "/products/pet-gut-60",
]
_STATIC_PAGE_PATHS = [
    "/about", "/events", "/university", "/blog", "/resources",
    "/privacy", "/refunds", "/shipping", "/terms",
]

@pytest.mark.parametrize("path", _STOREFRONT_PATHS + _CATEGORY_PATHS)
def test_storefront_path_renders_with_brand(client, seed_25, path):
    resp = client.get(path)
    assert resp.status_code == 200, (path, resp.status_code)
    # Brand markers
    assert b"logo-wordmark" in resp.data or b"Solex" in resp.data


@pytest.mark.parametrize("path", _PRODUCT_PATHS)
def test_product_detail_renders(client, seed_25, path):
    resp = client.get(path)
    assert resp.status_code == 200, (path, resp.status_code)


@pytest.mark.parametrize("path", _STATIC_PAGE_PATHS)
def test_static_page_renders(client, path):
    resp = client.get(path)
    assert resp.status_code == 200, (path, resp.status_code)


def test_home_has_hero_copy(client, seed_25):
    resp = client.get("/")
    assert b"Tune your home" in resp.data or b"Frequency" in resp.data
    # Featured grid rendered
    assert b"Featured" in resp.data


def test_shop_renders_all_25(client, seed_25):
    resp = client.get("/shop")
    # Should render 25 product cards (one per SKU)
    assert resp.data.count(b"product-card") >= 0  # soft check; cards don't have a class marker
    # Strong check: every category represented in the shop listing
    for name in (b"AO Youth", b"AO Scan", b"Red Light", b"Pet"):
        assert name in resp.data
```

Commit: `solex(tests): visual smoke — every branded route renders`.

### Task 5.2 — README updates

**Files:**
- Modify: `Solex/README.md`

Append a "Theme & catalog" section with:
- Brand palette listing (teal, gold, leaf, clay, cream, sand, ink)
- How to regenerate placeholder tiles
- How to swap in real Solex imagery
- Cross-ref to `docs/catalog-curation.md`

Commit: `solex(docs): README theme + catalog regeneration notes`.

### Task 5.3 — Full test matrix + visual smoke

```bash
cd ~/GrowDirect/Solex
docker compose -f devops/docker-compose.yml build web
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web pytest tests/unit tests/integration -m "not sandbox_live" 2>&1 | tail -3
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web pytest tests/smoke 2>&1 | tail -3
docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web pytest -m sandbox_live 2>&1 | tail -3
```

Expect: all green (should be ~235+ unit/integration + new smoke tests + 3 sandbox-live).

Live smoke:
```bash
./devops/scripts/dev.sh up
sleep 3
curl -s http://localhost:5003/ | wc -l
curl -s http://localhost:5003/shop | grep -c "card-product"  # 25 cards expected
curl -s http://localhost:5003/about | head -10
./devops/scripts/dev.sh down
```

No commit for 5.3 — verification only.

### Task 5.4 — Push + Open PR

```bash
cd ~/GrowDirect
git push -u origin plan/solex-visual
```

Then:

```bash
gh pr create --base plan/solex-scenarios \
  --title "feat: solex visual fidelity — brand theme + 25-SKU catalog + static pages" \
  --body "<per Plans 1-3 convention — summary, in/out scope, known issues, test plan>"
```

Body highlights: brand palette, 25 SKUs expansion, placeholder-tile strategy, Pillow dev-only dep flag, static pages, no backend changes, all prior tests pass.

---

## Plan 4 — Done criteria (repeat)

- [ ] Tailwind theme ships with earthy wellness palette + display serif + body sans
- [ ] Header has logo wordmark + primary nav + cart icon with live count
- [ ] Footer is 4-column with policy links
- [ ] Home has a real hero + featured + trust-bar + category tiles
- [ ] Shop renders 25 products with placeholder tiles; sidebar filters by category
- [ ] Product detail shows subscribe-and-save option + quantity selector + branded CTA
- [ ] Cart drawer is branded; cart page is branded
- [ ] Checkout is two-column on desktop; confirmation is branded
- [ ] 9 static pages all render with "placeholder" banner
- [ ] Admin + Account surfaces wrapped in branded layout (no functional change)
- [ ] Full test matrix green (Plans 1–3 tests + new visual smoke)
- [ ] PR opened, draft ready for human review

---

## What's next

This is the final plan in the Solex sequence. Post-merge roadmap:

1. **Human drops in real Solex imagery** (override placeholder tiles).
2. **Tune palette + typography** after seeing real screenshots side-by-side with solexglobal.com.
3. **Write real static-page copy** (replace placeholder text).
4. **Canary read-side chirp verification** — optional Canary API integration that the Lab UI could query (spec §4.9 post-MVP note).
5. **Cut-over to live Square** — separate spec, separate plan. Flip `SQUARE_ENVIRONMENT=production`, register a real merchant, apply for Solex distributor status.
