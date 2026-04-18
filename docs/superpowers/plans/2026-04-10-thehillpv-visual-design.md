# TheHillPV.com Visual Design — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reskin all Angel/TheHillPV.com templates from the current cove-teal HOA palette to a warm luxury editorial aesthetic matching Angelique Lyle's brand.

**Architecture:** Add `taupe-*` accent palette and `font-editorial` (Playfair Display) to Tailwind config. Recolor all Angel templates from `cove-*`/`shore-*` to `taupe-*`/`ink-*`. Add hero image sections with dark overlays. Generate placeholder hero images via Canva AI.

**Tech Stack:** Tailwind 3.x (PostCSS build), Jinja2 templates, Google Fonts (Playfair Display), Canva MCP (image generation)

**Spec:** `docs/superpowers/specs/2026-04-10-thehillpv-visual-design.md`

---

## Chunk 1: Foundation (Config + Base Template)

### Task 1: Add taupe palette and font-editorial to Tailwind config

**Files:**
- Modify: `Cove/tailwind.config.js`

- [ ] **Step 1: Add taupe color palette**

In `theme.extend.colors`, add after the `rust` block:

```js
/* Taupe — warm accent for Angel/TheHillPV pages */
taupe: {
  50:  '#F5F1ED',
  100: '#E8E0D6',
  200: '#D4C9BB',
  300: '#C4B5A3',
  400: '#BEB09E',
  500: '#A89A86',
  600: '#8A7D6B',
  700: '#6B5B4E',
  800: '#4E4238',
  900: '#332C24',
},
```

- [ ] **Step 2: Add font-editorial family**

In `theme.extend.fontFamily`, add:

```js
editorial: ['Playfair Display', 'Georgia', 'serif'],
```

- [ ] **Step 3: Build CSS to verify no errors**

Run: `cd /Users/gclyle/GrowDirect/Cove && npm run build`
Expected: Clean build, no errors

- [ ] **Step 4: Commit**

```bash
git add tailwind.config.js
git commit -m "config: add taupe accent palette and font-editorial for Angel pages"
```

---

### Task 2: Update base.html — fonts, nav, footer recolor

**Files:**
- Modify: `Cove/templates/angel/base.html`

- [ ] **Step 1: Add Playfair Display to Google Fonts link**

Change the existing Google Fonts `<link>` to include Playfair Display with italic variants:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Source+Sans+3:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap">
```

- [ ] **Step 2: Recolor navigation**

Replace all `cove-*` classes in the nav with warm equivalents:

| Current class | New class |
|--------------|-----------|
| `text-cove-700` (logo) | `text-ink-800` |
| `hover:text-cove-600` (nav links) | `hover:text-taupe-600` |
| `bg-cove-600` (CTA button) | `bg-ink-800` |
| `hover:bg-cove-700` (CTA hover) | `hover:bg-ink-700` |
| `text-cove-600` (mobile CTA) | `text-taupe-700` |
| `hover:bg-cove-50` (mobile CTA hover) | `hover:bg-taupe-50` |

- [ ] **Step 3: Recolor footer**

Replace footer color classes:

| Current class | New class |
|--------------|-----------|
| `bg-ink-800` (footer bg) | `bg-ink-900` (slightly darker) |
| `border-ink-700` (footer divider) | `border-ink-800` |
| No change needed for `cream-*` text colors — they already work |

- [ ] **Step 4: Verify in browser**

Open: `http://localhost:5002/angel/web/`
Check: Nav links are warm (not teal), CTA button is black, footer is dark. Playfair Display loads (check DevTools > Network > Fonts).

- [ ] **Step 5: Commit**

```bash
git add templates/angel/base.html
git commit -m "style(angel): recolor nav/footer from cove-teal to warm neutrals, add Playfair Display"
```

---

## Chunk 2: Neighborhood Hub Page Reskin

### Task 3: Recolor neighborhood.html — swap all cove/shore references

**Files:**
- Modify: `Cove/templates/angel/neighborhood.html`

- [ ] **Step 1: Add hero image section at the top**

Replace the current page header section (`bg-cream-100/50 border-b border-cream-200`) with a hero image section:

```html
{# --- Hero Image --- #}
<section class="relative h-[400px] sm:h-[500px] overflow-hidden">
  {% if neighborhood.hero_image %}
  <img src="{{ neighborhood.hero_image }}" alt="{{ neighborhood.name }}" class="absolute inset-0 w-full h-full object-cover">
  {% else %}
  <div class="absolute inset-0 bg-gradient-to-br from-ink-800 to-ink-600"></div>
  {% endif %}
  <div class="absolute inset-0 bg-black/35"></div>
  <div class="relative h-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col justify-end pb-12">
    <nav class="text-sm text-white/70 mb-3">
      <a href="{{ url_for('angel_web.neighborhoods') }}" class="hover:text-white transition-colors">Neighborhoods</a>
      <span class="mx-2">/</span>
      <span class="text-white">{{ neighborhood.name }}</span>
    </nav>
    <h1 class="text-3xl sm:text-4xl lg:text-5xl font-editorial font-bold text-white">{{ neighborhood.name }}</h1>
    <p class="mt-2 text-lg text-taupe-200 font-medium">{{ neighborhood.tagline }}</p>
  </div>
</section>
```

- [ ] **Step 2: Recolor all cove-* and shore-* references**

Global replacements in neighborhood.html:

| Pattern | Replacement | Context |
|---------|-------------|---------|
| `text-cove-600` | `text-taupe-600` | Links, accents |
| `text-cove-700` | `text-taupe-700` | Link hover, strong accent |
| `text-cove-800` | `text-taupe-800` | Dark accent text |
| `hover:text-cove-600` | `hover:text-taupe-600` | Link hover states |
| `hover:text-cove-700` | `hover:text-taupe-700` | Link hover states |
| `bg-cove-600` | `bg-ink-800` | CTA buttons |
| `hover:bg-cove-700` | `hover:bg-ink-700` | CTA button hover |
| `bg-cove-50` | `bg-taupe-50` | Light fills, featured event bg |
| `border-cove-100` | `border-taupe-100` | Featured event border |
| `bg-cove-500` | `bg-taupe-500` | Bullet dots |
| `bg-cove-400` | `bg-taupe-400` | Accent dots |
| `bg-shore-50` | `bg-taupe-50` | School badges (Niche) |
| `text-shore-700` | `text-taupe-700` | School badge text |
| `text-shore-600` | `text-taupe-600` | School badge text |
| `bg-shore-500/10` | `bg-taupe-100` | School badges |

- [ ] **Step 3: Swap font-heading to font-editorial on H1 and H2**

Replace `font-heading` with `font-editorial` on all `<h1>` and `<h2>` elements. Leave `<h3>` elements as `font-heading` (Source Sans 3).

- [ ] **Step 4: Style the closing blockquote with taupe accent**

Update the closing voice section:

```html
{% if voice.closing %}
<section class="border-t border-cream-200 pt-8">
  <blockquote class="bg-cream-100 rounded-xl p-6 border-l-4 border-taupe-400">
    <p class="text-sm text-ink-600 italic leading-relaxed font-editorial">{{ voice.closing }}</p>
    <cite class="block mt-3 text-xs text-ink-400 not-italic">
      — Angelique Lyle, Compass · 310.751.8335 · CA DRE# 01475592
    </cite>
  </blockquote>
</section>
{% endif %}
```

- [ ] **Step 5: Add hover effects to restaurant cards**

Wrap each restaurant card in a container with hover transition:

```html
<div class="border-b border-cream-100 pb-3 last:border-0 last:pb-0 hover:-translate-y-0.5 transition-transform duration-150">
```

- [ ] **Step 6: Verify in browser**

Open: `http://localhost:5002/angel/web/neighborhoods/lunada-bay`
Check: Hero gradient (no image yet), taupe accents throughout, no teal remaining, Playfair Display on H1/H2, warm closing blockquote.

- [ ] **Step 7: Commit**

```bash
git add templates/angel/neighborhood.html
git commit -m "style(angel): reskin neighborhood hub — hero section, taupe palette, editorial font"
```

---

### Task 4: Add hero_image field to NEIGHBORHOODS data

**Files:**
- Modify: `Cove/cove/angel/web_routes.py`

- [ ] **Step 1: Add hero_image key to each neighborhood dict**

Add `"hero_image": None` to each entry in `NEIGHBORHOODS`. This field will hold a URL to the hero image (populated in Task 8 when we generate images).

```python
{
    "slug": "lunada-bay",
    "name": "Lunada Bay",
    "tagline": "Cliffside living with world-class surf breaks",
    "city": "Palos Verdes Estates",
    "hero_image": None,  # populated by image generation task
    "description": "...",
},
```

- [ ] **Step 2: Commit**

```bash
git add cove/angel/web_routes.py
git commit -m "data(angel): add hero_image field to neighborhood data (None placeholder)"
```

---

## Chunk 3: Schools + Home + Neighborhoods Index Reskin

### Task 5: Recolor schools.html

**Files:**
- Modify: `Cove/templates/angel/schools.html`

- [ ] **Step 1: Swap all cove-*/shore-* to taupe-*/ink-***

Same pattern as Task 3 Step 2. Key replacements:

| Pattern | Replacement |
|---------|-------------|
| `text-cove-700` | `text-taupe-700` |
| `text-cove-600` | `text-taupe-600` |
| `bg-cove-700` | `bg-taupe-700` |
| `bg-cove-50` | `bg-taupe-50` |
| `bg-cove-600` (CTA) | `bg-ink-800` |
| `hover:bg-cove-700` (CTA) | `hover:bg-ink-700` |
| `bg-shore-500/10` | `bg-taupe-100` |
| `text-shore-600` | `text-taupe-600` |
| `bg-shore-50` | `bg-taupe-50` |
| `text-shore-700` | `text-taupe-700` |

- [ ] **Step 2: Swap font-heading to font-editorial on H1 and H2**

- [ ] **Step 3: Verify**

Open: `http://localhost:5002/angel/web/schools`
Check: No teal/blue, taupe accents, editorial font on headings.

- [ ] **Step 4: Commit**

```bash
git add templates/angel/schools.html
git commit -m "style(angel): reskin schools page — taupe palette, editorial font"
```

---

### Task 6: Reskin home.html

**Files:**
- Modify: `Cove/templates/angel/home.html`

- [ ] **Step 1: Replace hero section with dark image-ready hero**

Replace the current `bg-cove-700` hero with:

```html
<section class="relative overflow-hidden">
  <div class="absolute inset-0 bg-gradient-to-br from-ink-900/95 to-ink-700/85"></div>
  <div class="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32 lg:py-40">
    <div class="max-w-2xl">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-editorial font-bold text-white leading-tight">
        Life Above<br>the Pacific
      </h1>
      <p class="mt-6 text-lg sm:text-xl text-cream-200 leading-relaxed max-w-lg">
        The Palos Verdes Peninsula is more than a place to live. It's ocean
        views at sunrise, trails through wildflower preserves, and neighborhoods
        where people know each other by name.
      </p>
      <div class="mt-8 flex flex-col sm:flex-row gap-4">
        <a href="{{ url_for('angel_web.neighborhoods') }}" class="inline-flex items-center justify-center px-6 py-3 bg-white text-ink-800 font-semibold rounded-lg hover:bg-cream-100 transition-colors">
          Explore Neighborhoods
        </a>
        <a href="{{ url_for('angel_web.ask') }}" class="inline-flex items-center justify-center px-6 py-3 border-2 border-white/30 text-white font-semibold rounded-lg hover:bg-white/10 transition-colors">
          Ask Angelique
        </a>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Swap font-heading to font-editorial on H1/H2**

All `<h1>` and `<h2>` tags get `font-editorial` instead of `font-heading`.

- [ ] **Step 3: Recolor all cove-* references**

| Pattern | Replacement |
|---------|-------------|
| `text-cove-600` | `text-taupe-600` |
| `text-cove-700` | `text-taupe-700` |
| `hover:text-cove-600` | `hover:text-taupe-600` |
| `hover:text-cove-700` | `hover:text-taupe-700` |
| `hover:border-cove-200` | `hover:border-taupe-200` |
| `bg-cove-600` (CTA) | `bg-ink-800` |
| `hover:bg-cove-700` (CTA) | `hover:bg-ink-700` |
| `text-cove-100` | `text-cream-200` |
| `bg-cove-700` (ask section) | `bg-ink-800` |

- [ ] **Step 4: Verify**

Open: `http://localhost:5002/angel/web/`
Check: Dark warm hero (not teal), taupe accents on cards, black CTAs, editorial font, warm "Ask Angelique" section.

- [ ] **Step 5: Commit**

```bash
git add templates/angel/home.html
git commit -m "style(angel): reskin home page — warm hero, taupe accents, editorial font"
```

---

### Task 7: Reskin neighborhoods.html (index page)

**Files:**
- Modify: `Cove/templates/angel/neighborhoods.html`

- [ ] **Step 1: Swap font-heading to font-editorial on H1/H2**

- [ ] **Step 2: Recolor all cove-* references**

Same pattern: `cove-*` → `taupe-*` for accents, `ink-800` for CTAs.

- [ ] **Step 3: Verify**

Open: `http://localhost:5002/angel/web/neighborhoods/`
Check: Taupe accents on cards, no teal.

- [ ] **Step 4: Commit**

```bash
git add templates/angel/neighborhoods.html
git commit -m "style(angel): reskin neighborhoods index — taupe palette, editorial font"
```

---

## Chunk 4: Image Generation + CSS Build

### Task 8: Generate neighborhood hero images via Canva AI

**Files:**
- Create: `Cove/static/images/angel/` directory
- Modify: `Cove/cove/angel/web_routes.py` (update hero_image URLs)

- [ ] **Step 1: Create images directory**

```bash
mkdir -p /Users/gclyle/GrowDirect/Cove/static/images/angel
```

- [ ] **Step 2: Generate 7 hero images via Canva MCP**

Use `generate-design` for each neighborhood with these prompts:

| Neighborhood | Canva prompt |
|-------------|-------------|
| Lunada Bay | "Dramatic ocean bluffs and coastal sunset, Palos Verdes California, warm golden light, residential neighborhood above Pacific Ocean, cinematic landscape, no text" |
| Malaga Cove | "Mediterranean plaza with arched colonnades and fountain courtyard, red tile roofs, bougainvillea, California coastal town, warm afternoon light, no text" |
| Valmonte | "Tree-lined residential street with ranch-style homes, families walking, flat wide streets, California suburban neighborhood, golden hour, no text" |
| Miraleste | "Panoramic harbor and city skyline view from hillside, Los Angeles at dusk, residential neighborhood overlook, warm tones, no text" |
| Rancho Palos Verdes | "Coastal hiking trail along dramatic cliffs overlooking Pacific Ocean, wildflowers, Point Vicente lighthouse in distance, golden hour, no text" |
| Rolling Hills | "Gated equestrian estate with horse trails, oak trees, rolling green hills, California ranch landscape, warm natural light, no text" |
| Rolling Hills Estates | "Suburban park with playground and sports fields, families outdoors, hillside homes in background, South Bay California, sunny day, no text" |

Export each as JPG at 1200x500px. Save to `static/images/angel/{slug}-hero.jpg`.

- [ ] **Step 3: Update NEIGHBORHOODS data with hero_image paths**

```python
"hero_image": "/static/images/angel/lunada-bay-hero.jpg",
```

- [ ] **Step 4: Verify heroes render**

Open: `http://localhost:5002/angel/web/neighborhoods/lunada-bay`
Check: Hero image displays with dark overlay and white text.

- [ ] **Step 5: Commit**

```bash
git add static/images/angel/ cove/angel/web_routes.py
git commit -m "feat(angel): add Canva-generated hero images for all 7 neighborhoods"
```

---

### Task 9: Final CSS build + full verification

**Files:**
- Rebuild: `Cove/static/css/dist/main.css`

- [ ] **Step 1: Run Tailwind build**

```bash
cd /Users/gclyle/GrowDirect/Cove && npm run build
```

- [ ] **Step 2: Restart Flask container to pick up changes**

```bash
cd /Users/gclyle/GrowDirect/Cove/devops && docker compose restart flask
```

- [ ] **Step 3: Full page verification**

| Page | URL | Check |
|------|-----|-------|
| Home | `/angel/web/` | Dark warm hero, taupe cards, editorial font |
| Neighborhoods | `/angel/web/neighborhoods/` | Taupe card accents, no teal |
| Lunada Bay | `/angel/web/neighborhoods/lunada-bay` | Hero image, taupe throughout |
| Malaga Cove | `/angel/web/neighborhoods/malaga-cove` | Hero image, voice content styled |
| Schools | `/angel/web/schools` | Taupe ratings, editorial headings |
| Sitemap | `/sitemap.xml` | Still works |
| Robots | `/robots.txt` | Still works |

Check for zero instances of `cove-` classes in Angel templates:

```bash
grep -r "cove-" templates/angel/ | grep -v "{#" | grep -v "Malaga Cove"
```

Expected: No matches (all `cove-*` Tailwind classes replaced).

- [ ] **Step 4: Commit CSS build**

```bash
git add -f static/css/dist/main.css
git commit -m "build: regenerate Tailwind CSS with taupe palette + font-editorial"
```
