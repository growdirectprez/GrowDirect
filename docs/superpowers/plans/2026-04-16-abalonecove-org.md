# abalonecove.org Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Launch abalonecove.org as a static editorial site hosting a ~7,500-word long-form feature article about PV Peninsula history and the 0 Clipper development, with an evidence room, interactive map, and timeline.

**Architecture:** Static HTML site on GitHub Pages (same pattern as ownpalosverdes.com — no generator, no build step, push-to-deploy). Content drawn from existing Brain wiki articles and Cove documentary record sections. Map ported from Cove's Leaflet module as client-side-only JavaScript.

**Tech Stack:** Static HTML, inline CSS (Tailwind-inspired custom properties), Georgia serif typography, Leaflet.js (map), GitHub Pages, Cloudflare DNS (abalonecove.org).

**Spec:** `docs/superpowers/specs/2026-04-16-abalonecove-org-design.md`

---

## File Structure

```
~/abalonecove/                          # New repo (like ~/ownpalosverdes/)
├── index.html                          # The feature article (homepage IS the article)
├── evidence/index.html                 # Evidence room — document index
├── map/index.html                      # Interactive map page
├── map/data/                           # GeoJSON layers (copied from Cove)
│   ├── tract-14649-boundary.geojson
│   ├── declaration-one.geojson
│   ├── declaration-one-a.geojson
│   ├── landslide-complex.geojson
│   ├── landslide-moratorium.geojson
│   ├── coastal-zone.geojson
│   ├── clipper-0-contested.geojson
│   └── lot106-tract-32977-wong.geojson
├── timeline/index.html                 # Visual chronological timeline
├── about/index.html                    # Foundation, methodology, contact
├── images/                             # Hero images, document scans, logos
│   ├── abalone-shell-logo.png          # From existing letterhead
│   └── hero/                           # Section hero images
├── CNAME                               # abalonecove.org
├── robots.txt
├── sitemap.xml
└── docs/                               # Evidence room source documents (PDFs, images)
    ├── declarations/
    ├── tract-maps/
    ├── geological/
    ├── coastal-plan/
    ├── litigation/
    └── shore-club/
```

---

## Chunk 1: Repository Setup and Site Shell

### Task 1: Create repo and deploy empty site

**Files:**
- Create: `~/abalonecove/CNAME`
- Create: `~/abalonecove/robots.txt`
- Create: `~/abalonecove/index.html`

- [ ] **Step 1: Create the repo directory and initialize git**

```bash
mkdir ~/abalonecove
cd ~/abalonecove
git init
```

- [ ] **Step 2: Create CNAME for GitHub Pages**

```
abalonecove.org
```

- [ ] **Step 3: Create robots.txt**

```
User-agent: *
Allow: /
Sitemap: https://abalonecove.org/sitemap.xml
```

- [ ] **Step 4: Create minimal index.html placeholder**

A bare HTML page with the site title, Georgia serif font, and a "Coming soon"
message. Include the CSS custom properties that will be used site-wide.

Design tokens (from letterhead/abalone shell aesthetic):
- `--shell-teal: #2a7a7a` (primary — abalone interior)
- `--shell-sage: #6b8f7a` (secondary — kelp/coastal green)
- `--shell-cream: #f5f0e8` (background — paper/parchment)
- `--shell-dark: #1a1a2e` (text — deep navy/near-black)
- `--shell-warm: #c4a87a` (accent — shell exterior)
- `--shell-mist: #e8ede9` (alternate background — fog)
- Font stack: `Georgia, "Times New Roman", serif`
- Body: 18px/1.7 line-height for long-form reading

- [ ] **Step 5: Initial commit**

```bash
git add -A && git commit -m "chore: initialize abalonecove.org repo with GitHub Pages"
```

- [ ] **Step 6: Create GitHub repo and push**

```bash
gh repo create growdirectprez/abalonecove --public --source=. --push
```

Note: `--public` required for GitHub Pages on free plans. If org has
GitHub Pro/Team, `--private` is fine.

- [ ] **Step 7: Enable GitHub Pages on main branch**

```bash
gh api repos/growdirectprez/abalonecove/pages -X POST \
  -f source.branch=main -f source.path=/
```

- [ ] **Step 8: Configure Cloudflare DNS**

Point abalonecove.org to GitHub Pages (CNAME → growdirectprez.github.io).
Verify the CNAME is working. This is a manual step — confirm with user.

---

### Task 2: Build the article page template

**Files:**
- Modify: `~/abalonecove/index.html`

- [ ] **Step 1: Build full HTML template for long-form article**

The homepage IS the article. Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Meta: title, description, OG tags, JSON-LD Article schema -->
  <!-- GA4 tag (same property as OwnPV or new) -->
  <!-- CSS: inline <style> block with all design tokens -->
</head>
<body>
  <header>
    <!-- Abalone shell logo + "Abalone Cove" wordmark -->
    <!-- Minimal nav: Evidence | Map | Timeline | About -->
  </header>

  <article>
    <h1>Here's Something You Didn't Know About LA</h1>
    <p class="byline">By an HOA Board Member on the Palos Verdes Peninsula</p>
    <p class="dateline">Published [date] · [reading time] min read</p>

    <!-- 13 sections as <section> elements with id anchors -->
    <!-- Sticky progress bar or section indicator (optional) -->
    <!-- Evidence room links inline as <a> tags -->
  </article>

  <footer>
    <!-- Foundation name, mission statement, contact -->
    <!-- "If you have documents or stories, get in touch" -->
  </footer>
</body>
</html>
```

CSS priorities:
- Max article width: 680px centered (optimal reading width)
- Section spacing: 3rem between sections
- Blockquotes styled for primary source callouts (left border, cream bg)
- Image captions: smaller italic Georgia
- Links: teal underline, no color change on hover (understated)
- Mobile responsive: 16px body on mobile, 18px desktop
- Print stylesheet: clean article layout for printing

- [ ] **Step 2: Add placeholder content for all 13 sections**

Each section gets an `<h2>` with the section title and a placeholder paragraph
noting "[Content to be written in spine baseline session]". This validates
the layout and section flow.

- [ ] **Step 3: Verify in browser**

Open `index.html` locally. Check: typography, spacing, section flow,
mobile responsiveness (resize browser window), navigation links.

- [ ] **Step 4: Commit**

```bash
git add index.html && git commit -m "feat: article page template with 13-section layout"
```

---

### Task 3: Build evidence room page

**Files:**
- Create: `~/abalonecove/evidence/index.html`

- [ ] **Step 1: Create evidence room page**

Same header/footer as index.html. Body is a document index organized by
narrative section:

- Olmsted Plans (NPS Archive, File No. 8023)
- Founding Documents (1949-1952 declarations)
- Shore Club Records (incorporation, lease, 1972 ballot)
- Landslide Documentation (geological surveys, moratorium ordinances)
- Coastal Regulation (Coastal Specific Plan, General Plan)
- 0 Clipper Parcel (tract maps, chain of title, assessor data)
- Rezoning Record (ordinances, opposition letter, HCD correspondence)
- Litigation (petition, demurrer, opposition)

Each entry: title, date, source, one-line description, link to document
(PDF in `docs/` directory or external source URL).

Start with entries we know exist from the report sections. Documents
themselves get added as they're assembled.

- [ ] **Step 2: Commit**

```bash
git add evidence/ && git commit -m "feat: evidence room page with document index"
```

---

### Task 4: Build map page

**Files:**
- Create: `~/abalonecove/map/index.html`
- Create: `~/abalonecove/map/data/*.geojson` (copied from Cove)

- [ ] **Step 1: Copy existing GeoJSON layers from Cove**

```bash
mkdir -p ~/abalonecove/map/data
```

Copy layers from `~/GrowDirect/Cove/cove/map/data/layers/`:

```bash
SRC=~/GrowDirect/Cove/cove/map/data/layers
DST=~/abalonecove/map/data
cp $SRC/tract-14649-boundary.geojson $DST/
cp $SRC/declaration-one.geojson $DST/
cp $SRC/declaration-one-a.geojson $DST/
cp $SRC/landslide-complex.geojson $DST/
cp $SRC/landslide-moratorium.geojson $DST/
cp $SRC/coastal-zone.geojson $DST/
cp $SRC/clipper-0-contested.geojson $DST/
cp $SRC/lot106-tract-32977-wong.geojson $DST/
```

**Deferred map features (not in launch scope):**
- Clickable parcels with deed chain/HOA membership/zoning (needs data model)
- Shore Club / Shoreline Park footprint (no GeoJSON layer exists yet)
- APBL boundary as separate layer (currently covered by `landslide-complex`)
- Declaration 101 parcels (`dec101-p1` through `dec101-p7` exist but need context)

- [ ] **Step 2: Build map page with Leaflet**

Same header/footer. Body is a full-width Leaflet map:

```html
<!-- Leaflet CSS/JS from CDN (acceptable for static site) -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9/dist/leaflet.js"></script>

<div id="map" style="height: 80vh; width: 100%;"></div>

<script>
  // Initialize map centered on Abalone Cove
  // ~33.7395, -118.3765, zoom 15
  // Layer toggle control for each GeoJSON layer
  // Popup on parcel click showing basic info
  // Legend explaining layer colors
</script>
```

Layer styling:
- Tract 14649 boundary: teal outline
- Declaration zones: dashed borders, semi-transparent fill
- Landslide complex: red hatching or semi-transparent red
- Moratorium area: orange outline
- 0 Clipper parcel: highlighted yellow/gold

- [ ] **Step 3: Verify map loads and layers toggle**

Open in browser. Check: all layers load, toggle works, popups appear,
zoom/pan works on mobile.

- [ ] **Step 4: Commit**

```bash
git add map/ && git commit -m "feat: interactive map with existing GeoJSON layers"
```

---

### Task 5: Build timeline and about pages

**Files:**
- Create: `~/abalonecove/timeline/index.html`
- Create: `~/abalonecove/about/index.html`

- [ ] **Step 1: Create timeline page**

Vertical scrolling timeline from 1913 to 2026. Key events:

```
1913  Vanderlip purchases peninsula from Bixby syndicate
1925  PV Corporation reorganized (Delaware)
1929  Shore Club incorporated
1937  Frank Vanderlip Sr. dies
1949  Declaration No. One recorded (April 29)
1949  Declaration of Easements recorded (May 5)
1950  Lot H Declaration recorded (January 25)
1952  Grant Deeds — PV Corp sells individual lots
1953  PV Corp stock sold to Great Lakes Carbon (~$9M)
1954  PV Corp dissolved (Delaware)
1956  Portuguese Bend Landslide reactivates
1972  Shore Club vote: park over 138-170 condos
1973  RPV incorporates (March 7)
1974  Abalone Cove Landslide begins
1976  California Coastal Act
1978  Coastal Specific Plan adopted (Resolution 78-61)
1980  Tract 32977 — Wong subdivides 0 Clipper parcel
1986  Tract 43725 — reversion to acreage
2005  Wong Family Trust sells to Hartman Trust
2009  WPBCA Restated Declaration
2021  Clipper Development LLC acquires parcel ($2.2M)
2024  City rezones RS-4 → RM-22 (April-June)
2024  FPPC complaint filed (August)
2024  Petition for Writ of Mandate filed (September)
2024  Governor's emergency declaration (September)
2025  HCD confirms Site 16 removable (January)
2025  City Council keeps Site 16 (June)
2026  Ground movement: 2.14 in/week (March)
```

Pure CSS timeline (no JS library needed). Each entry: year, title, one-line
description. Optional link to evidence room.

- [ ] **Step 2: Create about page**

- Foundation name and mission (placeholder until 501(c)(3) formed)
- "About this project" — the AI methodology, brief version
- Contact: email address (foundation@abalonecove.org or similar)
- "If you have documents, photos, or stories about Abalone Cove,
  we'd love to hear from you"
- Disclaimer: "This site presents public records and personal research.
  It is not legal advice."

- [ ] **Step 3: Create sitemap.xml**

List all 5 pages with lastmod dates.

- [ ] **Step 4: Commit**

```bash
git add timeline/ about/ sitemap.xml && git commit -m "feat: timeline and about pages"
```

---

### Task 6: SEO and structured data

**Files:**
- Modify: `~/abalonecove/index.html`

- [ ] **Step 1: Add JSON-LD structured data to article page**

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Here's Something You Didn't Know About LA",
  "description": "A board member traces 113 years of land use history...",
  "author": {
    "@type": "Person",
    "name": "An HOA Board Member"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Abalone Cove Foundation"
  },
  "datePublished": "2026-XX-XX",
  "about": [
    "Palos Verdes Peninsula",
    "Abalone Cove",
    "California land use",
    "Portuguese Bend Landslide"
  ]
}
```

- [ ] **Step 2: Add OG meta tags for social sharing**

Title, description, image (abalone shell logo or hero image), URL.
Twitter card meta tags.

- [ ] **Step 3: Add canonical URL and meta description**

Target keywords: "Abalone Cove history", "0 Clipper Road Rancho Palos Verdes",
"Portuguese Bend landslide development", "Palos Verdes Peninsula history",
"Vanderlip Palos Verdes".

- [ ] **Step 4: Commit and push**

```bash
git add -A && git commit -m "seo: structured data, OG tags, meta descriptions"
git push
```

---

## Chunk 2: Narrative Spine Baseline

This chunk is a **Cowork session**, not a code task. It produces the actual
article content.

### Task 7: Spine baseline session

**Files:**
- Read: All `Cove/docs/archive/report/section-*.md` (10 files)
- Read: All `Brain/wiki/cove-*.md` (9 files)
- Output: Draft article text for all 13 sections

- [ ] **Step 1: Read all existing content**

Read every report section and Brain wiki article. Build a mapping:

| Spine Section | Source Material | Gap? |
|---|---|---|
| 1. Hook | New — personal narrative | YES |
| 2. Olmsted Thread | section-01, wiki/cove-community-history | Partial |
| 3. Vanderlip | wiki/cove-community-history, wiki/cove-pv-declaration-scheme | Partial |
| 4. Lawyer Brothers | section-04 (partial), wiki/cove-community-history | YES — 1929-1948 gap |
| 5. Parceling the Hill | section-02, section-03, wiki/cove-legal-framework | Rewrite needed |
| 6. The Slide | section-05, wiki/cove-property-geology | Rewrite needed |
| 7. Condos vs Beach | section-04 | Rewrite needed |
| 8. Coastal Wall | section-06 | Rewrite needed |
| 9. Wong Subdivision | section-07 | Rewrite needed |
| 10. The Rezoning | section-08 | Rewrite needed |
| 11. The Tools | New — AI methodology narrative | YES |
| 12. The Absurdity | New + section-05 (current conditions) | Partial |
| 13. Why? | New — conclusion | YES |

- [ ] **Step 2: Draft each section**

Rewrite existing content in LA Times Sunday Home section voice. Tight
paragraphs, let facts breathe, no legal verbatim. Each section ~300-500
words. Total target ~7,500 words.

Key voice notes:
- "Here's something you didn't know about LA" energy
- Don't get long-winded — author acknowledges tendency
- Previous homeowner was on the board in '50s AND Shore Club director
  (provenance for the garage documents)
- Davis-Stirling + electronic voting question started the AI journey
- Hartman/Wong subdivision never raised during planning commission
- Let reader draw conclusions; don't editorialize
- "This has been tried before and this is going to fail too"

- [ ] **Step 3: Fill the 1929-1948 gap**

Research the Lawyer Brothers, Filiorum Corporation, Neptune Fountain,
La Venta Inn, the Depression-era legal vehicles. Check Brain wiki and
any primary sources in the archive. This may require additional research
beyond existing materials.

- [ ] **Step 4: Write the personal sections (1, 11, 13)**

These have no existing source material. Written from the user's story:
- Hook: California taxpayer, grew up in LA, frustrations
- The Tools: Davis-Stirling question → AI journey → document discovery
- Why?: The pattern. The question. No call to action.

- [ ] **Step 5: Assemble full draft**

Combine all 13 sections into a single document. Check word count
(target ~7,500). Check narrative flow — does each section lead naturally
to the next?

- [ ] **Step 6: Insert draft into index.html**

Replace placeholder content with actual article text. Each section
in its `<section>` element with proper id anchors.

- [ ] **Step 7: Commit and push**

```bash
git add index.html && git commit -m "content: first draft — full 13-section narrative"
git push
```

---

## Chunk 3: Evidence Room Population and Polish

### Task 8: Populate evidence room with primary sources

**Files:**
- Create: `~/abalonecove/docs/declarations/*.pdf`
- Create: `~/abalonecove/docs/tract-maps/*.pdf`
- Create: `~/abalonecove/docs/geological/*.pdf`
- Create: `~/abalonecove/docs/coastal-plan/*.pdf`
- Create: `~/abalonecove/docs/litigation/*.pdf`
- Create: `~/abalonecove/docs/shore-club/*.pdf`
- Modify: `~/abalonecove/evidence/index.html`

- [ ] **Step 1: Inventory available primary source documents**

Check `Cove/docs/archive/report/` for rasterized source PDFs.
Check `Cove/docs/archive/originals/` if it exists.
List what we have vs. what the evidence room index references.

- [ ] **Step 2: Copy available documents into repo**

Organize into `docs/` subdirectories by topic. Keep filenames descriptive:
`1949-04-29-declaration-no-one.pdf`, `1978-12-19-coastal-specific-plan.pdf`, etc.

- [ ] **Step 3: Update evidence room links**

Point each evidence room entry to the actual document in `docs/` or to
external source URLs (LA County Recorder, NPS, court records).

- [ ] **Step 4: Commit and push**

```bash
git add docs/ evidence/ && git commit -m "content: evidence room populated with primary sources"
git push
```

---

### Task 9: Article polish and inline evidence links

**Files:**
- Modify: `~/abalonecove/index.html`

- [ ] **Step 1: Add inline evidence links throughout article**

Every factual claim in the article should link to the evidence room or
directly to a document. Example: "Declaration No. One" links to
`/evidence/#declaration-one` or directly to the PDF.

- [ ] **Step 2: Add section hero images (if available)**

The Olmsted plans, the Shore Club pamphlet (Ray Wallace illustration),
assessor parcel maps, the 1972 ballot — these are visual anchors.
Only add images we actually have. Don't use stock photography.

- [ ] **Step 3: Add reading progress indicator**

Subtle progress bar at top of page showing how far through the article
the reader is. Pure CSS + minimal JS (IntersectionObserver on sections).

- [ ] **Step 4: Final typography and spacing pass**

Check on mobile, tablet, desktop. Verify: blockquote styling, image
captions, link styling, section transitions, print layout.

- [ ] **Step 5: Commit and push**

```bash
git add -A && git commit -m "polish: evidence links, images, progress bar, typography"
git push
```

---

### Task 10: Launch checklist

- [ ] **Step 1: Verify GitHub Pages is serving abalonecove.org**
- [ ] **Step 2: Verify HTTPS working via Cloudflare**
- [ ] **Step 3: Test all internal links (article → evidence, evidence → docs)**
- [ ] **Step 4: Test map loads and layers work**
- [ ] **Step 5: Test mobile layout on actual phone**
- [ ] **Step 6: Submit sitemap to Google Search Console**
- [ ] **Step 7: Verify OG tags render correctly (use ogp.me debugger)**
- [ ] **Step 8: Final read-through of article for typos/flow**

---

## Execution Notes

- **Chunk 1 (Tasks 1-6)** can be done in a single Claude Code session.
  This is all site infrastructure — no content writing.
- **Chunk 2 (Task 7)** is a Cowork session with the user. The personal
  narrative sections require the user's input and approval. The rewrite
  of existing report content into editorial voice requires iterative
  review. This is the longest phase.
- **Chunk 3 (Tasks 8-10)** is a finishing session. Evidence assembly,
  inline linking, polish, and launch.
- **501(c)(3) formation** is a parallel track, not blocking the site launch.
  The about page can say "Foundation forming" until paperwork is complete.
