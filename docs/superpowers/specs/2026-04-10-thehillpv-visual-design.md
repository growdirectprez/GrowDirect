# TheHillPV.com — Visual Design Spec

**Date:** 2026-04-10
**Project:** Angel (TheHillPV.com)
**Scope:** Visual identity, color system, typography, image strategy, component
styling for the public-facing content site.

---

## Design Principles

TheHillPV.com is an editorial lifestyle site for Palos Verdes Peninsula real
estate. It reads like a well-produced local magazine — not a property search
portal, not a corporate broker page. Every visual choice should feel like
Angelique: warm, confident, specific, never generic.

**Three anchors:**

1. **Warm luxury** — not cold minimalism, not flashy gold. Think linen, wood,
   afternoon light. The taupe accent from Accardo RE (#BEB09E) is the key.
2. **Editorial rhythm** — generous whitespace, strong type hierarchy, photography
   used as atmosphere (not decoration). Sections breathe.
3. **Brand continuity** — aligns with angeliquelyle.com (Playfair Display, black/
   white, dark overlays) while being warmer and more content-forward.

---

## Color System

The existing Tailwind config already has warm neutrals (`cream-*`, `ink-*`) that
work well for TheHillPV.com. We **keep those** and add a `taupe` accent group
to replace the `cove-*` teal and `shore-*` blue that Angel templates currently use.

### Token Strategy

| Existing Token | Angel Usage | Change? |
|---------------|-------------|---------|
| `cream-50` through `cream-300` | Backgrounds, section alternation | **Keep as-is** — already warm |
| `ink-50` through `ink-900` | Text hierarchy, headings | **Keep as-is** — already warm neutral |
| `cove-*` (teal) | Currently used for accent/links/buttons | **Replace with `taupe-*`** in Angel templates |
| `shore-*` (blue) | School badges, secondary accent | **Replace with `taupe-*`** in Angel templates |
| `rust-*` | Error/danger states | **Keep** — Angel inherits for form validation |

### New: Taupe Accent Palette

Add alongside existing `cove`, `shore`, etc. Angel templates use `taupe-*`
instead of `cove-*` for accents, links, and interactive elements.

| Token | Hex | Usage |
|-------|-----|-------|
| `taupe-50` | `#F5F1ED` | Light fills, badge backgrounds |
| `taupe-100` | `#E8E0D6` | Hover fills, input focus rings |
| `taupe-200` | `#D4C9BB` | Active states, borders |
| `taupe-300` | `#C4B5A3` | — |
| `taupe-400` | `#BEB09E` | **Primary accent** (from Accardo RE brand) |
| `taupe-500` | `#A89A86` | Link text, button backgrounds |
| `taupe-600` | `#8A7D6B` | Link hover, darker accent |
| `taupe-700` | `#6B5B4E` | Strong accent, active links |
| `taupe-800` | `#4E4238` | Dark accent text |
| `taupe-900` | `#332C24` | — |

### Overlay & CTA Treatment

Overlays are **not** custom color tokens. Use Tailwind's built-in opacity syntax:

- Hero image overlay: `bg-black/35`
- Heavy overlay (white text on photo): `bg-black/55`
- Primary CTA button: `bg-ink-800 hover:bg-ink-700 text-white`
- Secondary CTA: `bg-white border border-ink-300 text-ink-800 hover:bg-cream-100`

### Tailwind Config Addition

```js
// Add to theme.extend.colors in tailwind.config.js
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

---

## Typography

### Font Stack

| Role | Font | Weight | Source |
|------|------|--------|--------|
| **Editorial headings** | Playfair Display | 400, 700 (+ italics) | Google Fonts (matches angeliquelyle.com) |
| **UI headings** | Source Sans 3 | 600 | Already loaded — `font-heading` (keep for Cove) |
| **Body** | Source Sans 3 | 300, 400, 500, 600 | Already loaded in base.html |
| **Accent/Labels** | Source Sans 3 | 500, uppercase, letter-spaced | For badges, section labels |

Playfair Display brings editorial warmth for Angel pages. Source Sans 3
(already loaded) handles body text and UI elements. The existing `font-heading`
stays as Source Sans 3 for Cove governance pages — Angel templates use a new
`font-editorial` family key.

### Type Scale

| Element | Size | Weight | Line Height | Font |
|---------|------|--------|-------------|------|
| H1 (page title) | 2.5rem (40px) | 700 | 1.2 | Playfair Display (`font-editorial`) |
| H2 (section heading) | 1.5rem (24px) | 700 | 1.3 | Playfair Display (`font-editorial`) |
| H3 (card/subsection) | 1.125rem (18px) | 600 | 1.4 | Source Sans 3 (`font-heading`) |
| Body | 1rem (16px) | 400 | 1.7 | Source Sans 3 (`font-sans`) |
| Small/caption | 0.875rem (14px) | 400 | 1.5 | Source Sans 3 |
| Label/badge | 0.75rem (12px) | 500 | 1 | Source Sans 3, uppercase |

### Implementation

1. Add Playfair Display (roman + italic, 400 + 700) to Google Fonts link in
   Angel's `base.html`:
   ```
   family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700
   ```
2. Add `font-editorial` family to Tailwind config (does NOT replace `font-heading`):
   ```js
   fontFamily: {
     editorial: ['Playfair Display', 'Georgia', 'serif'],
     // existing font-heading, font-sans, etc. unchanged
   }
   ```
3. Angel templates use `font-editorial` on H1/H2, `font-heading` on H3.

---

## Photography & Image Strategy

### Image Types

| Type | Where Used | Spec | Source Strategy |
|------|-----------|------|----------------|
| **Neighborhood hero** | Top of each neighborhood page | 1200x500px, 16:6 ratio | Angelique's photos, Canva generation, or licensed stock |
| **Section accent** | Alongside voice intro text | 600x400px, 3:2 ratio | Neighborhood-specific atmospheric shots |
| **Card thumbnail** | Restaurant/business cards | 300x200px, 3:2 ratio | Entity-specific or category placeholder |
| **OG/social preview** | Meta tags, link previews | 1200x630px | Generated per page via Canva |
| **Agent headshot** | Sidebar, footer, about | 200x200px, 1:1 circle | Angelique's professional photo |

### Image Treatment

- **Hero images:** Full-width with `--hill-overlay` (35% black). White text
  overlay for page title and tagline. Image should be atmospheric — coastline,
  neighborhood character, not a specific property listing.
- **Section accents:** No overlay. Rounded corners (12px). Subtle shadow. Used
  sparingly — one per major section at most.
- **Card thumbnails:** Rounded corners (8px). Uniform aspect ratio. If no image
  available for an entity, use a category-specific placeholder (fork/knife for
  dining, book for schools, tree for nature).

### Placeholder Strategy (Phase 1)

Until Angelique provides real photography, use Canva AI to generate:

1. Seven neighborhood hero images (coastal PV aesthetic — bluffs, ocean, plazas,
   tree-lined streets)
2. Category placeholder icons for entity cards
3. OG preview card for social sharing

These get replaced with real photos as they become available. The templates
should use an `image_url` field on entities/neighborhoods so swapping is a
data change, not a code change.

---

## Layout Patterns

### Neighborhood Hub Page

```
┌─────────────────────────────────────────────────────┐
│  HERO IMAGE (full-width, 500px tall)                │
│  ┌───────────────────────────────────────┐          │
│  │  Breadcrumb > Neighborhood Name       │ overlay  │
│  │  H1: Lunada Bay                       │          │
│  │  Tagline in taupe accent              │          │
│  └───────────────────────────────────────┘          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────┐  ┌──────────────┐        │
│  │  MAIN COLUMN (2/3)   │  │  SIDEBAR     │        │
│  │                      │  │              │        │
│  │  Voice Intro         │  │  Ask Card    │        │
│  │  (with accent image) │  │              │        │
│  │                      │  │  Businesses  │        │
│  │  Real Estate Stats   │  │              │        │
│  │  (stat cards)        │  │  Other       │        │
│  │                      │  │  Neighborhoods│       │
│  │  Schools Section     │  │              │        │
│  │                      │  └──────────────┘        │
│  │  Dining Section      │                          │
│  │                      │                          │
│  │  Events Section      │                          │
│  │                      │                          │
│  │  Community Pulse     │                          │
│  │                      ���                          │
│  │  Further Reading     │                          │
│  │                      │                          │
│  │  Closing Quote       │                          │
│  └──────────────────────┘                          │
│                                                     │
├─────────────────────────────────────────────────────┤
│  FOOTER                                             │
└─────────────────────────────────────���───────────────┘
```

### Key Layout Rules

- **Max content width:** 72rem (1152px) — consistent with current `max-w-6xl`
- **Section spacing:** 3rem (48px) between major sections
- **Card padding:** 1.5rem (24px) internal padding
- **Card radius:** 12px (rounded-xl)
- **Card shadow:** Warm shadow, not blue/gray. `shadow-warm (already defined in Tailwind config)`
- **Alternating backgrounds:** White → cream → white for visual rhythm

---

## Component Styling

### Navigation

Keep the current sticky nav structure. Update colors:

- Background: `white/90` with backdrop blur (current, keep)
- Logo text: `--hill-ink` (black, not blue)
- Nav links: `--hill-ink-light` → hover `--hill-taupe`
- CTA button: `--hill-cta` (black) with white text

### Cards (Restaurants, Events, Schools)

```
┌──────────────────────────────┐
│  [Image or category icon]    │  ← 3:2 ratio, rounded-t
├──────────────────────────────┤
│  Badge: "New" / "Featured"   │  ← taupe-light bg
│  H3: Entity Name             │  ← Source Sans 600
│  Description (2 lines max)   │  ← ink-light, 14px
│  Hours · Tags                │  ← ink-muted, 12px
└─���────────────────────────────┘
```

- Border: 1px `--hill-sand`
- Background: white
- Hover: subtle translate-y (-2px) + shadow increase
- No blue — all warm tones

### Stat Cards (Real Estate Section)

Large number in `--hill-ink`, label in `--hill-ink-muted`. Background:
`--hill-cream`. Border: `--hill-sand`. Compact, side-by-side grid.

### Buttons

| Type | Style |
|------|-------|
| Primary CTA | Black bg, white text, rounded-lg, hover → #333 |
| Secondary | White bg, black border, black text, hover → cream bg |
| Link | `--hill-link` text, underline on hover, no bg |

### Blockquotes (Closing Voice Section)

Left border: 3px `--hill-taupe`. Italic text in `--hill-ink-light`. Cite in
`--hill-ink-muted`, not italic. Background: `--hill-cream` with 1.5rem padding.

---

## Responsive Breakpoints

Follow current Tailwind breakpoints (sm/md/lg). Key adaptations:

- **Hero image:** 400px tall on mobile (vs 500px desktop)
- **Content grid:** Single column on mobile, 2/3 + 1/3 on lg+
- **Sidebar:** Moves below main content on mobile
- **Stat cards:** 2-column on mobile (vs 4 on desktop)
- **Nav:** Hamburger on mobile (current Alpine.js toggle, keep)

---

## Implementation Order

1. **Tailwind config** — add `hill` palette and Playfair Display font
2. **base.html** — swap nav/footer colors from cove-* to hill-*
3. **neighborhood.html** — add hero image section, recolor all components
4. **schools.html** — recolor components, add editorial header
5. **home.html** — hero with overlay, neighborhood preview cards
6. **neighborhoods.html** — grid cards with images
7. **Image generation** — Canva AI for 7 neighborhood heroes + placeholders
8. **OG images** — Generate per-page social preview cards

---

## Image Sources & Rights

| Source | Status | Rights |
|--------|--------|--------|
| Angelique's own photography | Awaiting | She owns these |
| Canva AI generation | Available now | Canva license, commercial use OK |
| angeliquelyle.com images | Available | Her content, she controls rights |
| accardorealestate.com images | Available | Team content, check with team |
| Stock photography | Future option | Licensed per-image |

**Rule:** No scraping third-party sites for images. All imagery must be owned,
licensed, or AI-generated with commercial rights.

---

## Files Changed

| File | Changes |
|------|---------|
| `tailwind.config.js` | Add `hill` color palette, Playfair Display font |
| `static/css/main.css` | Add hill-specific component classes if needed |
| `templates/angel/base.html` | Playfair Display font link, nav/footer recolor |
| `templates/angel/neighborhood.html` | Hero image, recolored sections, image slots |
| `templates/angel/schools.html` | Recolored components |
| `templates/angel/home.html` | Hero section, visual neighborhood grid |
| `templates/angel/neighborhoods.html` | Card images, hover states |
| `static/images/angel/` | New directory for hero images and placeholders |

---

## Out of Scope

- Logo design (use text logo "TheHillPV" for now)
- Print PDF generation
- Newsletter email template styling
- Animation/motion design beyond hover transitions
- Dark mode
