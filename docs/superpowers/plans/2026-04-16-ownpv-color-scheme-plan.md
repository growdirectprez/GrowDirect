# OwnPalosVerdes.com Color Scheme Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the navy/gold color scheme with an ink/teal/copper palette across all ownpalosverdes.com pages and the market report generator.

**Architecture:** CSS variable swap + hardcoded rgba replacement across 5 static HTML files and 1 Python template generator. No layout changes. No font changes. One new image asset (blended shell logo).

**Tech Stack:** HTML/CSS (static site), Python (report generator), image processing (shell logo)

**Spec:** `docs/superpowers/specs/2026-04-16-ownpv-color-scheme-redesign.md`

---

## Chunk 1: Homepage Color Swap

### Task 1: Replace `:root` CSS variables in index.html

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/index.html:74-88`

- [ ] **Step 1: Replace the `:root` block**

Replace lines 74-88 in index.html with:

```css
:root {
  --ink: #1A1A1A;
  --stone: #3D3D3D;
  --drift: #5A5A5A;
  --foam: #F7F5F2;
  --sand: #EDE8E0;
  --sand-mid: #E0D9CE;
  --teal: #2E6E68;
  --teal-hover: #245855;
  --copper: #C97D54;
  --error: #B44A3E;
  --white: #FFFFFF;
  --serif: 'Playfair Display', Georgia, serif;
  --sans: 'Outfit', system-ui, sans-serif;
}
```

- [ ] **Step 2: Add teal bold rule**

Add after the `:root` block, before the `html` rule:

```css
[style*="var(--teal)"], .teal-text { font-weight: 500; }
```

Note: This is a safety net. Each teal usage should also have `font-weight: 500` explicitly.

- [ ] **Step 3: Open index.html in browser and verify variables loaded**

Run: Open `/Users/gclyle/ownpalosverdes/index.html` in browser.
Expected: Page loads but many elements may look wrong because old variable names (`--ocean`, `--sand-dark`, `--sunset`) are now undefined. This is expected — we fix them in the next tasks.

- [ ] **Step 4: Commit**

```bash
cd /Users/gclyle/ownpalosverdes
git add index.html
git commit -m "refactor: replace :root CSS variables with new ink/teal/copper palette"
```

---

### Task 2: Migrate `var(--ocean)` references in index.html

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/index.html`

Every `var(--ocean)` becomes `var(--ink)`. There are ~35 instances across nav, hero, sections, buttons, and dark backgrounds.

- [ ] **Step 1: Find-and-replace `var(--ocean-mid)` → `var(--stone)`**

There are 2 instances:
- Line 618: `.form-submit:hover { background: var(--ocean-mid); }` → `var(--stone);`
- Line 700: `.mobile-nav a:hover { color: var(--ocean-mid); }` → `var(--stone);`

- [ ] **Step 2: Find-and-replace `var(--ocean)` → `var(--ink)`**

Apply to all ~33 remaining instances. This is a straight text replacement — every `var(--ocean)` becomes `var(--ink)`.

Key areas:
- Nav: `.nav-logo`, `.nav-links a:hover`, `.nav-cta`, `.nav-menu` (lines 104-120)
- Hero: `.hero-left` background (line 129)
- Sections: `.section-heading` (line 208), `#neighborhoods` (line 242), `#history` (line 344)
- About: `.about-photo-caption`, `.sig-name`, `.sig-cta` (lines 220-239)
- Market: `.market-report-month`, `.market-view-all` (lines 300-326)
- Schools: `.school-name` (line 338)
- Welcome: `.welcome-pkg-card` (line 407)
- Resources: `.resource-title`, `.resource-btn` (lines 531-543)
- Testimonials: `.test-quote` (line 557)
- Contact: `#contact` background, `.form-input:focus`, `.form-submit`, `.form-success` (lines 573-621)
- Footer: `footer a` (lines 631-634)
- Modal: `.modal-close:hover`, `.modal-title` (lines 651-652)
- Mobile nav: `.mobile-nav a`, close button (lines 698-703)
- Inline styles in HTML body: `style="...color:var(--ocean)..."` (line 1003)
- Radio accent-color (line 1098): `accent-color:var(--ocean)` → `accent-color:var(--teal)`

**Note:** The radio accent-color is the ONE exception — it maps to `--teal`, not `--ink`, because it's an interactive form element.

- [ ] **Step 3: Verify in browser**

Open index.html. All text that was navy should now be near-black. Dark sections (neighborhoods, history, contact, welcome-pkg-card, concierge-card) should have `--ink` backgrounds.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "refactor: migrate all --ocean references to --ink"
```

---

### Task 3: Migrate `var(--sand-dark)` and `var(--sunset)` in index.html

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/index.html`

`--sand-dark` was the gold accent — Sotheby's signal. Each usage maps to a new variable based on its role. `--sunset` maps to `--copper` (decorative) or `--error` (functional).

- [ ] **Step 1: Map and replace each `var(--sand-dark)` by context**

**On dark backgrounds (editorial/decorative context) → `var(--copper)`:**
- Hero eyebrow text + line (lines 140, 143): `color: var(--sand-dark)` → `color: var(--copper)`
- Hero title italic (line 149): `color: var(--sand-dark)` → `color: var(--copper)`
- Hero stat numbers (line 180): `color: var(--sand-dark)` → `color: var(--copper)`
- Seam label + line (lines 191, 194): `color: var(--sand-dark)` → `color: var(--copper)`
- About photo caption text (line 220): `color: var(--sand-dark)` → `color: var(--copper)`
- Neighborhoods section-tag (lines 247-248): `color: var(--sand-dark)` → `color: var(--copper)`, `background: var(--sand-dark)` → `background: var(--copper)`
- Hood card tag (line 270): `color: var(--sand-dark)` → `color: var(--copper)`
- Hood card arrow (line 277): `color: var(--sand-dark)` → `color: var(--copper)`
- History section-tag (lines 363-364): same swap
- History link (line 369): `color: var(--sand-dark)` → `color: var(--copper)`
- Chapter arrow (line 403): `color: var(--sand-dark)` → `color: var(--copper)`
- Pkg label (line 420): `color: var(--sand-dark)` → `color: var(--copper)`
- Concierge booklet label (line 463): `color: var(--sand-dark)` → `color: var(--copper)`
- Concierge section-tag (lines 468-469): same swap
- Concierge feature numbers (line 478): `color: var(--sand-dark)` → `color: var(--copper)`
- Concierge card label (line 501): `color: var(--sand-dark)` → `color: var(--copper)`
- Concierge card check (line 511): `color: var(--sand-dark)` → `color: var(--copper)`
- Contact section-tag (lines 580-581): same swap
- Contact detail icon border (line 589): `color: var(--sand-dark)` → `color: var(--copper)`
- Contact detail label (line 592): `color: var(--sand-dark)` → `color: var(--copper)`
- Footer col title (line 631): `color: var(--sand-dark)` → `color: var(--copper)`
- SVG path stroke (line 870): `stroke="var(--sand-dark)"` → `stroke="var(--copper)"`

**Interactive buttons on dark backgrounds → `var(--sand)` (light visible color):**
- `.btn-primary` background (line 157): `background: var(--sand-dark)` → `background: var(--sand)`
- `.btn-ghost` text (line 166): `color: var(--sand-dark)` → `color: var(--sand)`
- `.btn-ghost:hover` border (line 170): `border-color: var(--sand-dark)` → `border-color: var(--sand)`
- `.pkg-btn` background (line 433): `background: var(--sand-dark)` → `background: var(--sand)`
- `.pkg-input:focus` border (line 430): `border-color: var(--sand-dark)` → `border-color: var(--sand-mid)`
- `.concierge-cta` border (line 486): `border: 1px solid var(--sand-dark)` → `border: 1px solid var(--sand)`
- `.concierge-cta:hover` bg (line 489): `background: var(--sand-dark)` → `background: var(--sand)`
- `.concierge-booklet:hover` border (line 459): `border-color: var(--sand-dark)` → `border-color: var(--sand)`
- `.form-submit` bg (line 613): `background: var(--ocean)` already handled; `color: var(--sand-dark)` → `color: var(--sand)`
- Contact form submit hover accent (line 451 area): check for `--sand-dark` in contact CTA bar

**Footer links hover:**
- Line 634: `.footer-links a:hover { color: var(--sand-dark); }` → `color: var(--sand);`

- [ ] **Step 2: Replace `var(--sunset)` usages**

There are 3 instances:
- Line 431: `.pkg-input[aria-invalid="true"] { border-color: var(--sunset); }` → `border-color: var(--error);`
- Line 443: `.pkg-error { font-size: 0.72rem; color: var(--sunset); }` → `color: var(--error);`
- Line 605: `.form-input[aria-invalid="true"] { border-color: var(--sunset); }` → `border-color: var(--error);`
- Line 620: `.form-error { font-size: 0.72rem; color: var(--sunset); }` → `color: var(--error);`

- [ ] **Step 3: Verify — search for any remaining old variable names**

Run in terminal:
```bash
grep -n 'var(--ocean)\|var(--sand-dark)\|var(--sunset)\|var(--ocean-mid)' /Users/gclyle/ownpalosverdes/index.html
```
Expected: Zero results.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "refactor: migrate --sand-dark and --sunset to copper/sand/error"
```

---

### Task 4: Migrate hardcoded rgba() values in index.html

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/index.html`

- [ ] **Step 1: Replace ocean-based rgba (28,58,74 → 26,26,26)**

Find-and-replace across the file. Instances (~8):
- Line 98: `rgba(249,247,244,0.92)` → `rgba(247,245,242,0.92)` (foam-based, update to new foam)
- Line 103: `rgba(28,58,74,0.08)` → `rgba(26,26,26,0.08)`
- Line 176: `rgba(28,58,74,0.6)` → `rgba(26,26,26,0.65)` (hero overlay — bump opacity slightly)
- Line 179: `rgba(28,58,74,0.75)` → `rgba(26,26,26,0.75)`
- Line 268: `rgba(28,58,74,0.85)` → `rgba(26,26,26,0.85)`
- Line 305: `rgba(28,58,74,0.08)` → `rgba(26,26,26,0.08)`
- Line 336: `rgba(28,58,74,0.1)` → `rgba(26,26,26,0.1)`
- Line 524: `rgba(28,58,74,0.08)` → `rgba(26,26,26,0.08)`
- Line 644: `rgba(28,58,74,0.8)` → `rgba(26,26,26,0.8)`

- [ ] **Step 2: Replace sand-dark-based rgba (200,185,154 → 224,217,206)**

Instances (~10):
- Line 100: `rgba(200,185,154,0.25)` → `rgba(224,217,206,0.25)`
- Line 165: `rgba(200,185,154,0.4)` → `rgba(224,217,206,0.4)`
- Line 178: `rgba(200,185,154,0.2)` → `rgba(224,217,206,0.2)`
- Line 253: `rgba(200,185,154,0.15)` → `rgba(224,217,206,0.15)`
- Line 275: `rgba(200,185,154,0.3)` → `rgba(224,217,206,0.3)`
- Line 370: `rgba(200,185,154,0.4)` → `rgba(224,217,206,0.4)`
- Line 413: `rgba(200,185,154,0.15)` → `rgba(224,217,206,0.15)`
- Line 418: `rgba(200,185,154,0.08)` → `rgba(224,217,206,0.08)`
- Line 425: `rgba(200,185,154,0.25)` → `rgba(224,217,206,0.25)`
- Line 456: `rgba(200,185,154,0.2)` → `rgba(224,217,206,0.2)`
- Line 475: `rgba(200,185,154,0.15)` → `rgba(224,217,206,0.15)`
- Line 587: `rgba(200,185,154,0.25)` → `rgba(224,217,206,0.25)`

- [ ] **Step 3: Replace old-drift-based rgba (138,155,168 → 90,90,90)**

Instances (3):
- Line 429: `rgba(138,155,168,0.6)` → `rgba(90,90,90,0.6)`
- Line 440: `rgba(138,155,168,0.5)` → `rgba(90,90,90,0.5)`
- Line 492: `rgba(138,155,168,0.3)` → `rgba(90,90,90,0.3)`

- [ ] **Step 4: Verify no old rgba values remain**

```bash
grep -n 'rgba(28,58,74\|rgba(200,185,154\|rgba(138,155,168' /Users/gclyle/ownpalosverdes/index.html
```
Expected: Zero results.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "refactor: migrate hardcoded rgba values to new neutral palette"
```

---

### Task 5: Fix dark-section text contrast in index.html

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/index.html`

Sections with `background: var(--ink)` need their body text updated. The new `--drift` (#5A5A5A) is invisible on the dark background.

- [ ] **Step 1: Update text colors in dark sections**

These rules use `color: var(--drift)` on dark backgrounds and must change:

- Line 151: `.hero-sub { color: var(--drift); }` → `color: var(--sand);`
- Line 181: `.hero-stat-label { color: var(--drift); }` → `color: var(--sand-mid);`
- Line 196: `.seam-scroll span { color: var(--drift); }` → `color: var(--sand-mid);`
- Line 223: `.about-photo-caption .label { color: var(--drift); }` → `color: var(--sand-mid);`
- Line 272: `.hood-card-price { color: var(--drift); }` → `color: var(--sand-mid);`
- Line 366: `.history-content .body-text { color: var(--drift); }` → `color: var(--sand);`
- Line 422: `.pkg-body { color: var(--drift); }` → `color: var(--sand);`
- Line 442: `.pkg-success p { color: var(--drift); }` → `color: var(--sand);`
- Line 466: `.concierge-booklet-dl { color: var(--drift); }` → `color: var(--sand-mid);`
- Line 471: `.concierge-content .body-text { color: var(--drift); }` → `color: var(--sand);`
- Line 481: `.concierge-feature-text { color: var(--drift); }` → `color: var(--sand);`
- Line 509: `.concierge-card-item { color: var(--drift); }` → `color: var(--sand);`

- [ ] **Step 2: Visual verification**

Open index.html. Scroll through all dark sections (hero, neighborhoods, history, welcome package card, concierge, contact). All text should be clearly readable — warm whites and sands on near-black backgrounds.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "fix: update dark-section text colors for contrast on ink backgrounds"
```

---

## Chunk 2: Guide Pages + Report Generator

### Task 6: Update neighborhoods guide

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/guides/neighborhoods/index.html`

This file has its own `:root` block and ~28 old color references.

- [ ] **Step 1: Replace the `:root` block**

Find the `:root` block and replace with the same new palette from Task 1 Step 1.

- [ ] **Step 2: Find-and-replace old variable names**

Same mappings as Tasks 2-3:
- `var(--ocean)` → `var(--ink)` (except radio accent-color → `var(--teal)`)
- `var(--ocean-mid)` → `var(--stone)`
- `var(--sand-dark)` → context-dependent: `var(--copper)` for decorative, `var(--sand)` for buttons
- `var(--sunset)` → `var(--error)`

- [ ] **Step 3: Replace hardcoded rgba values**

Same mappings as Task 4.

- [ ] **Step 4: Fix dark-section text contrast**

Same pattern as Task 5 — any `color: var(--drift)` on dark backgrounds → `var(--sand)` or `var(--sand-mid)`.

- [ ] **Step 5: Verify — grep for old values**

```bash
grep -n 'var(--ocean)\|var(--sand-dark)\|var(--sunset)\|rgba(28,58,74\|rgba(200,185,154' /Users/gclyle/ownpalosverdes/guides/neighborhoods/index.html
```
Expected: Zero results.

- [ ] **Step 6: Commit**

```bash
git add guides/neighborhoods/index.html
git commit -m "refactor: update neighborhoods guide to new color palette"
```

---

### Task 7: Update schools guide

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/guides/schools/index.html`

~35 old color references. Same process as Task 6.

- [ ] **Step 1: Replace `:root` block**
- [ ] **Step 2: Find-and-replace old variable names**
- [ ] **Step 3: Replace hardcoded rgba values**
- [ ] **Step 4: Fix dark-section text contrast**
- [ ] **Step 5: Verify with grep**
- [ ] **Step 6: Commit**

```bash
git add guides/schools/index.html
git commit -m "refactor: update schools guide to new color palette"
```

---

### Task 8: Update lifestyle guide

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/guides/lifestyle/index.html`

~28 old color references. Same process as Task 6.

- [ ] **Step 1: Replace `:root` block**
- [ ] **Step 2: Find-and-replace old variable names**
- [ ] **Step 3: Replace hardcoded rgba values**
- [ ] **Step 4: Fix dark-section text contrast**
- [ ] **Step 5: Verify with grep**
- [ ] **Step 6: Commit**

```bash
git add guides/lifestyle/index.html
git commit -m "refactor: update lifestyle guide to new color palette"
```

---

### Task 9: Update generate_reports.py

**Files:**
- Modify: `/Users/gclyle/ownpalosverdes/generate_reports.py`

This script has TWO `:root` blocks (around lines 306 and 647) embedded in Python f-string templates, plus scattered old color references in the template HTML.

- [ ] **Step 1: Replace both `:root` blocks**

Find the two `:root` sections (lines ~306-309 and ~647-649) and replace each with the new palette. Note: Python f-strings use `{{` and `}}` for literal braces, so the CSS will look like:

```python
:root {{
  --ink: #1A1A1A; --stone: #3D3D3D; --drift: #5A5A5A;
  --foam: #F7F5F2; --sand: #EDE8E0; --sand-mid: #E0D9CE;
  --teal: #2E6E68; --teal-hover: #245855; --copper: #C97D54;
  --error: #B44A3E; --white: #FFFFFF;
  --serif: 'Playfair Display', Georgia, serif;
  --sans: 'Outfit', system-ui, sans-serif;
}}
```

- [ ] **Step 2: Replace all old variable names in templates**

Search the entire file for `--ocean`, `--sand-dark`, `--sunset`, `--ocean-mid` and apply the same mappings.

- [ ] **Step 3: Replace hardcoded rgba values**

Same channel swaps as Task 4.

- [ ] **Step 4: Fix dark-section text on ink backgrounds**

Same `--drift` → `--sand`/`--sand-mid` pattern for text on dark backgrounds.

- [ ] **Step 5: Verify with grep**

```bash
grep -n '\-\-ocean\|\-\-sand-dark\|\-\-sunset\|rgba(28,58,74\|rgba(200,185,154' /Users/gclyle/ownpalosverdes/generate_reports.py
```
Expected: Zero results.

- [ ] **Step 6: Regenerate one test report to verify**

```bash
cd /Users/gclyle/ownpalosverdes
python3 generate_reports.py --month 2025-02
```

Open the generated report in browser. Verify no navy or gold.

- [ ] **Step 7: Regenerate ALL market reports**

All 34 existing monthly reports still have old colors. Regenerate them all:

```bash
cd /Users/gclyle/ownpalosverdes
python3 generate_reports.py
```

If the script doesn't support a no-arg "regenerate all" mode, loop through each month:

```bash
for dir in market/20*/; do
  month=$(basename "$dir")
  python3 generate_reports.py --month "$month"
done
```

Also verify `market/index.html` (the market landing page) is regenerated with new colors.

- [ ] **Step 8: Commit**

```bash
git add generate_reports.py market/
git commit -m "refactor: update report generator templates and regenerate all reports"
```

---

## Chunk 3: Shell Logo + Final Verification

### Task 10: Create blended shell logo asset

**Files:**
- Source: `/Users/gclyle/GrowDirect/Cove/docs/brand/shell-256.png`
- Create: `/Users/gclyle/ownpalosverdes/images/shell-blended-256.png`
- Create: `/Users/gclyle/ownpalosverdes/images/shell-blended-128.png`
- Create: `/Users/gclyle/ownpalosverdes/images/shell-blended-64.png`
- Create: `/Users/gclyle/ownpalosverdes/images/shell-blended-32.png`

- [ ] **Step 1: Install Pillow if not available**

```bash
pip3 install Pillow
```

- [ ] **Step 2: Create blended shell script**

Write a Python script that:
1. Opens `shell-256.png`
2. Creates a radial gradient alpha mask that fades from fully opaque at center to transparent at edges
3. Composites the shell onto a `#F7F5F2` background using the mask
4. Saves at 256, 128, 64, 32px sizes

```python
from PIL import Image, ImageDraw
import math

def create_blended_shell(src_path, out_dir, foam_color=(247, 245, 242)):
    shell = Image.open(src_path).convert("RGBA")
    w, h = shell.size
    
    # Create radial gradient mask
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    cx, cy = w // 2, h // 2
    max_r = min(cx, cy)
    
    for y in range(h):
        for x in range(w):
            dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            # Fade starts at 60% of radius, fully transparent at 100%
            if dist < max_r * 0.6:
                alpha = 255
            elif dist < max_r:
                alpha = int(255 * (1 - (dist - max_r * 0.6) / (max_r * 0.4)))
            else:
                alpha = 0
            mask.putpixel((x, y), alpha)
    
    # Apply mask to shell alpha
    r, g, b, a = shell.split()
    a = Image.composite(a, Image.new("L", (w, h), 0), mask)
    shell = Image.merge("RGBA", (r, g, b, a))
    
    # Composite onto foam background
    bg = Image.new("RGBA", (w, h), foam_color + (255,))
    result = Image.alpha_composite(bg, shell)
    
    for size in [256, 128, 64, 32]:
        resized = result.resize((size, size), Image.LANCZOS)
        resized.save(f"{out_dir}/shell-blended-{size}.png")

create_blended_shell(
    "/Users/gclyle/GrowDirect/Cove/docs/brand/shell-256.png",
    "/Users/gclyle/ownpalosverdes/images"
)
```

- [ ] **Step 3: Run the script and verify output**

Check that all 4 sizes exist and the edges blend smoothly into #F7F5F2.

- [ ] **Step 4: Delete the generation script (one-shot artifact)**

- [ ] **Step 5: Commit**

```bash
cd /Users/gclyle/ownpalosverdes
git add images/shell-blended-*.png
git commit -m "feat: add blended abalone shell logo assets"
```

---

### Task 11: Full-site verification sweep

**Files:**
- All modified files

- [ ] **Step 1: Run color audit across all files**

```bash
for f in index.html guides/neighborhoods/index.html guides/schools/index.html guides/lifestyle/index.html market/index.html; do
  echo "=== $f ==="
  grep -c 'var(--ocean)\|var(--sand-dark)\|var(--sunset)\|var(--ocean-mid)\|rgba(28,58,74\|rgba(200,185,154\|rgba(138,155,168\|#1C3A4A\|#2C5568\|#C8B99A\|#D4784A\|#8A9BA8' "$f"
done
echo "=== sample market report ==="
grep -c 'var(--ocean)\|var(--sand-dark)\|var(--sunset)\|#1C3A4A\|#C8B99A' market/2025-02/index.html
echo "=== generate_reports.py ==="
grep -c '\-\-ocean\|\-\-sand-dark\|\-\-sunset\|rgba(28,58,74\|rgba(200,185,154\|#1C3A4A\|#C8B99A' generate_reports.py
```

Expected: All counts = 0.

- [ ] **Step 2: Visual check — open each page in browser**

Walk through:
1. `index.html` — check nav, hero, neighborhoods, market, schools, history, welcome, concierge, resources, testimonials, contact, footer
2. Each guide page
3. One market report

Verify:
- No navy or gold anywhere
- All text readable (no invisible drift on dark)
- Copper on light backgrounds: decorative only (dividers, rules, borders)
- Copper on dark backgrounds: used as text for eyebrows, labels, numbers (5.4:1 contrast — passes AA)
- Teal text is bold
- Dark sections use warm light text (sand/sand-mid for body, copper for accents), not drift

- [ ] **Step 3: Commit any fixes from visual review**

- [ ] **Step 4: Final commit with all changes**

```bash
git add index.html guides/ market/ generate_reports.py images/shell-blended-*.png
git commit -m "feat: complete color scheme redesign — ink/teal/copper palette

Replaces navy/gold (Sotheby's overlap) with Compass-adjacent palette.
See docs/superpowers/specs/2026-04-16-ownpv-color-scheme-redesign.md"
```

---

## Deferred (Secondary Scope)

The spec lists two secondary-scope items that are **not included** in this plan:

- **Cove `tailwind.config.js`** — update `shore` palette to align with teal, add `copper` and `error` colors
- **`Cove/templates/angel/base.html`** — update hardcoded color classes

These affect the Flask-served Angel/TheHillPV site (different deployment). They should be a follow-up session after the static site is confirmed working.
