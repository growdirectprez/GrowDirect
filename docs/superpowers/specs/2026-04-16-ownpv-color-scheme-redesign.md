# OwnPalosVerdes.com — Color Scheme Redesign

**Date:** 2026-04-16
**Status:** Approved
**Problem:** Current navy (#1C3A4A) + gold (#C8B99A) palette reads as Sotheby's International Realty — wrong signal for a Compass agent site.
**Solution:** Compass-adjacent ink/warm-white palette with abalone teal (interactive) and copper (editorial) accents. Coastal PV personality, no brokerage overlap.

---

## Design Decisions

- **Direction:** Compass-adjacent with Palos Verdes coastal personality (not generic Compass, not Sotheby's)
- **Fonts:** No change — Playfair Display (headings) + Outfit (body) stay
- **Accent strategy:** Two accents with distinct roles — teal for interactive elements, copper for editorial/decorative warmth
- **Logo:** New blended-edge abalone shell asset that fades into the foam background
- **Accessibility:** All ink/stone/drift text meets WCAG AA 4.5:1 on light backgrounds. Teal text relies on the bold-text exception (AA large/bold at 3.0:1) — always rendered at font-weight 500+. Copper is restricted to decorative/non-text uses (borders, dividers, rules) where contrast requirements do not apply.

---

## Color Palette

### New Variables

| Variable | Hex | Role | Contrast on foam (#F7F5F2) |
|----------|-----|------|-----------------------------|
| `--ink` | `#1A1A1A` | Headings, primary CTA backgrounds, body text | 15.4:1 |
| `--stone` | `#3D3D3D` | Nav links, secondary text | 9.7:1 |
| `--drift` | `#5A5A5A` | Captions, muted helper text (contrast floor) | 5.9:1 |
| `--foam` | `#F7F5F2` | Page background | — |
| `--sand` | `#EDE8E0` | Alternate section backgrounds | — |
| `--sand-mid` | `#E0D9CE` | Default borders, nav underline | — |
| `--teal` | `#2E6E68` | Interactive accent — links, secondary buttons, hover states | 5.8:1 |
| `--teal-hover` | `#245855` | Hover/active state for teal elements | 7.6:1 |
| `--copper` | `#C97D54` | Decorative only — section dividers, pull-quote borders, decorative rules | 2.9:1 (not used for text) |
| `--white` | `#FFFFFF` | Text on dark backgrounds | — |
| `--error` | `#B44A3E` | Form validation errors, error messages | 5.2:1 |

### Updated Variables (value changes to existing names)

These variables exist in the current CSS but their values shift from blue-tinted to neutral:

| Variable | Old Value | New Value | Why |
|----------|-----------|-----------|-----|
| `--ink` | `#1A2428` (blue-black) | `#1A1A1A` (neutral black) | Remove blue tint |
| `--stone` | `#4A5A62` (blue-gray) | `#3D3D3D` (neutral dark gray) | Remove blue tint |
| `--drift` | `#8A9BA8` (blue-gray) | `#5A5A5A` (neutral mid-gray) | Remove blue tint, improve contrast |
| `--foam` | `#F9F7F4` | `#F7F5F2` | Slightly warmer |
| `--sand` | `#F4EFE6` | `#EDE8E0` | Slightly deeper warm |
| `--sand-mid` | `#E8DDD0` | `#E0D9CE` | Aligned with new sand |

### Removed Variables

| Variable | Old Value | Why Removed |
|----------|-----------|-------------|
| `--ocean` | `#1C3A4A` | Navy — Sotheby's primary. All usages migrate to `--ink` |
| `--ocean-mid` | `#2C5568` | Navy mid — Sotheby's. All usages migrate to `--stone` |
| `--sand-dark` | `#C8B99A` | Gold — Sotheby's secondary. No replacement. |
| `--sunset` | `#D4784A` | Replaced by `--copper` (decorative) and `--error` (functional) |

---

## Migration Map

### Text and UI Elements (old → new)

| Old Usage | Old Variable/Value | New Variable |
|-----------|-------------------|-------------|
| Heading text | `--ocean` | `--ink` |
| Nav link default | `--stone` (blue-gray) | `--stone` (neutral) |
| Nav link hover | `--ocean` | `--ink` |
| CTA border/text | `--ocean` | `--ink` |
| CTA hover background | `--ocean` | `--ink` |
| Logo main text | `--ocean` | `--ink` |
| Logo italic text | `--stone` | `--stone` |
| Body text | `--ink` (blue-black) | `--ink` (neutral) |
| Muted/caption text | `--drift` (blue-gray) | `--drift` (neutral) |
| Accent links | `--sunset` | `--teal` (**bold**) |
| Form radio accent-color | `--ocean` | `--teal` |
| Form validation errors | `--sunset` | `--error` |
| Error text (.form-error, .pkg-error) | `--sunset` | `--error` |

### Backgrounds

| Old Usage | Old Variable/Value | New Variable | Notes |
|-----------|-------------------|-------------|-------|
| Page background | `--foam` (#F9F7F4) | `--foam` (#F7F5F2) | Subtle shift |
| Alt sections (schools, testimonials) | `--sand` (#F4EFE6) | `--sand` (#EDE8E0) | Subtle shift |
| Dark sections (neighborhoods, history, contact, concierge, package CTA, seam bar) | `--ocean` / `background: var(--ocean)` | `--ink` | All `background: var(--ocean)` become `background: var(--ink)` |

### Text on Dark Backgrounds

When sections use `background: var(--ink)` (#1A1A1A), text colors must change:

| Element on dark bg | Old Color | New Color | Contrast on #1A1A1A |
|--------------------|-----------|-----------|---------------------|
| Headings | `--sand` / `--white` | `--white` (#FFFFFF) | 15.4:1 |
| Body text | `--drift` (old: #8A9BA8) | `--sand` (#EDE8E0) | 11.8:1 |
| Muted/caption | `--drift` | `--sand-mid` (#E0D9CE) | 10.2:1 |
| Links on dark bg | n/a | `--sand` (not teal — insufficient contrast on dark) | 11.8:1 |

### Hardcoded `rgba()` Values

All hardcoded rgba values referencing old palette colors must be converted:

| Old rgba base | New rgba base | Instances |
|---------------|---------------|-----------|
| `rgba(28,58,74,...)` (ocean) | `rgba(26,26,26,...)` (ink) | ~8 instances |
| `rgba(200,185,154,...)` (sand-dark) | `rgba(224,217,206,...)` (sand-mid) | ~10 instances |
| `rgba(138,155,168,...)` (old drift) | `rgba(90,90,90,...)` (new drift) | ~3 instances |

The alpha values stay the same — only the RGB channels change.

### Hero Overlay

The hero uses a gradient overlay on a background image. Current: `rgba(28,58,74,0.6)`. New: `rgba(26,26,26,0.6)`. Since the underlying image varies, the overlay opacity may need adjustment (0.6 → 0.65 or 0.7) to maintain readable text. Verify visually during implementation.

---

## Teal Usage Rules

- Links (inline text links, nav active states)
- Secondary button borders and text (outline style)
- Hover/active states use `--teal-hover` (#245855)
- Form element accent-color (radio buttons, checkboxes)
- **Always bold when used as text** — `font-weight: 500` minimum
- Teal relies on WCAG AA bold-text exception (3.0:1 threshold). At 5.8:1 on foam, it exceeds this comfortably.
- **No teal text on dark backgrounds** — insufficient contrast. Use `--sand` for links on dark sections.
- **No filled teal buttons** — white on teal is only 3.6:1. Use outline style (teal border + teal text on foam bg) or ink-filled buttons with white text.

## Copper Usage Rules

- Section dividers — thin (1-2px) horizontal rules between major content blocks
- Pull-quote left borders (3-4px vertical accent)
- Decorative underlines or keylines
- **On light backgrounds (#F7F5F2 foam, #EDE8E0 sand): decorative only, never as text.** Copper at 2.9:1 on foam fails AA at every level. Eyebrow label *text* on light backgrounds uses `--stone`; a copper underline or rule can sit below for warmth.
- **On dark backgrounds (#1A1A1A ink): copper IS allowed as text.** Copper on ink = 5.4:1, passing AA. Use for eyebrow labels, feature numbers, section tags, italic accents, and decorative numerals on dark sections. This is the primary way copper adds editorial warmth to the site.
- **Never as a button color, link color, or any interactive element** (regardless of background).

## Error State Rules

- Form validation borders and error text use `--error` (#B44A3E), not copper or teal
- This replaces the old `--sunset` usage for `.form-error`, `.pkg-error`, `aria-invalid` borders

---

## Logo Treatment

### New Asset: Blended Abalone Shell

**Source:** `Cove/docs/brand/shell-256.png` (the teal abalone shell)

**Treatment:** Process the shell image to create a version where the edges fade via radial gradient from the shell's natural colors into `#F7F5F2` (foam). The result should float seamlessly on the warm white background with no hard rectangular boundary.

**Output sizes:**
- `shell-blended-256.png` — hero/footer mark
- `shell-blended-128.png` — inline decorative
- `shell-blended-64.png` — small mark
- `shell-blended-32.png` — favicon candidate

**Usage on site:**
- Footer: small shell mark alongside "Own Palos Verdes" text
- Potential: subtle watermark in hero section (very low opacity, 5-8%)

---

## Scope — Files to Modify

### Primary (static site)

1. **`/Users/gclyle/ownpalosverdes/index.html`**
   - Replace `:root` CSS custom properties block entirely
   - Add `--teal`, `--teal-hover`, `--copper`, `--error` variables
   - Remove `--ocean`, `--ocean-mid`, `--sand-dark`, `--sunset`
   - Convert all ~21 hardcoded `rgba()` values per the table above
   - Update dark-section text colors (drift → sand/sand-mid on ink backgrounds)
   - Add CSS rule: elements with `color: var(--teal)` get `font-weight: 500`
   - Update form radio `accent-color` from ocean to teal
   - Update form error styles from sunset to error
   - Verify hero overlay opacity with new colors

2. **`/Users/gclyle/ownpalosverdes/guides/{lifestyle,neighborhoods,schools}/index.html`**
   - Audit each file for inline `:root` blocks or hardcoded color values
   - If they embed their own styles, apply the same palette swap
   - If they inherit from index.html, verify inheritance works

3. **`/Users/gclyle/ownpalosverdes/market/*.html`**
   - Auto-generated by generate_reports.py — changes flow from #4

4. **`/Users/gclyle/ownpalosverdes/generate_reports.py`**
   - Full palette replacement required — the script embeds the complete `:root` block as a Python string template (around line 307-309)
   - Update all color references in the HTML template strings

### Logo Asset

5. **New files: `/Users/gclyle/ownpalosverdes/images/shell-blended-*.png`**
   - Process shell-256.png with radial fade to #F7F5F2
   - Generate size variants (256, 128, 64, 32)

### Secondary (Cove/Angel Tailwind — consistency pass)

6. **`/Users/gclyle/GrowDirect/Cove/tailwind.config.js`**
   - Update `shore` palette to align with new teal values
   - Add `copper` and `error` colors
   - Ensure Angel templates reference aligned colors

7. **`/Users/gclyle/GrowDirect/Cove/templates/angel/base.html`**
   - Update any hardcoded color classes to match new palette

---

## Out of Scope

- Layout changes (structure stays identical)
- Font changes (Playfair + Outfit stay)
- Content changes
- LP builder site (separate deployment, separate spec)
- Cove HOA app styling (separate from Angel/OwnPV public site)

---

## Verification

After implementation, every page should pass these checks:

1. No navy (#1C3A4A, #2C5568) or gold (#C8B99A) anywhere in computed styles
2. All ink/stone/drift text meets WCAG AA 4.5:1 on light backgrounds
3. Teal text is always bold (font-weight >= 500) and never appears on dark backgrounds
4. Copper appears only in decorative roles (dividers, rules, borders) — never as text, buttons, or links
5. Dark sections use --ink background with --white/--sand/--sand-mid text (not drift)
6. Error states use --error, not copper or sunset
7. Shell logo blends seamlessly into foam background (no hard edges visible)
8. Site reads "Compass-adjacent luxury coastal" — not Sotheby's, not generic
9. All rgba() values use neutral RGB channels, no blue-tinted remnants
