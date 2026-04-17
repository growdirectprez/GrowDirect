# Abalone Cove Timeline Enrichment — Design Spec

**Date:** 2026-04-17
**Project:** abalonecove.org (static site, GitHub Pages)
**File:** `~/abalonecove/timeline/index.html`

---

## Purpose

Transform the timeline page from a flat chronological list into the Abalone Cove Foundation's definitive public record of land use regulation, geological events, and civic decisions at Abalone Cove and the Palos Verdes south coast.

This is not an HOA document. It is the factual basis for a 501(c)(3) foundation — credible enough for a donor, clear enough for a neighbor, thorough enough for a commissioner. Every entry that references a document closes the loop: link to the evidence room if we hold it, link to a civic source if it's public, or state the fact with no link if neither exists. No stubs. No broken links. No promises.

## Constraints

- Pure static HTML with embedded CSS. No JavaScript. No build tools.
- All internal links use relative paths (`../evidence/`, `../docs/`). Site must work from `file://` — opened from a zip without a web server.
- Same design system as the rest of abalonecove.org (shell-teal, shell-cream, Georgia serif, 680px max-width, sticky header with hamburger nav).
- No new CSS patterns beyond `<details>` styling and era dividers.

## Page Structure

### Header
Same sticky header/nav as all other pages. Timeline link gets `aria-current="page"`.

### Intro
- **Title:** "Timeline"
- **Subtitle:** Reframed — not "113 years of land use history" but something that establishes the regulatory record and the foundation's purpose.
- **Intro paragraph:** 2-3 sentences. This is a chronological record of the land itself — the restrictions placed on it, the geological forces acting on it, and the civic decisions that shaped it. The foundation exists because the public record proves this land was never meant to be developed the way it's now being proposed.

### Era Groupings

The timeline is divided into four eras with styled `<h2>` dividers. The vertical timeline line pauses at each divider and resumes. Dividers use `--shell-warm` border, small caps, centered text.

1. **Rancho Era** (1882–1925)
2. **Declarations & Development** (1929–1954)
3. **Geology & Regulation** (1956–1986)
4. **Modern Era** (2009–2026)

### Timeline Entries

Each entry retains the existing layout (year label, dot on vertical line, title, description). Enriched entries add a `<details>` element below the description.

```html
<div class="timeline-entry">
  <div class="timeline-year">1949</div>
  <div class="timeline-body">
    <div class="timeline-title">Declaration No. One</div>
    <div class="timeline-desc">Tract 14649 established — WPBCA created, 81 lots, single-family only</div>
    <details class="timeline-detail">
      <summary>Record</summary>
      <p>What the document does, what flows from it, recorder references.</p>
      <ul>
        <li><a href="../docs/originals/declarations/1949-WPBCA-Declaration.pdf">Original (PDF)</a></li>
        <li><a href="../docs/declarations/1949-WPBCA-Declaration-No-One-Verbatim.md">Verbatim transcription</a></li>
      </ul>
    </details>
  </div>
</div>
```

**`<summary>` labels:**
- "Record" for document-based entries (declarations, deeds, tract maps)
- "Context" for regulatory and event entries (Coastal Act, landslides, rezoning)

**External link indicator:** Any `<a>` targeting an external URL gets a CSS `::after` arrow via `a[href^="http"]::after`. No JavaScript.

### Footer
Same footer as all other pages.

## Entry Tiering

### Tier 1 — Full Breakdown

Full chain-of-title treatment: what the document does, what flows from it, recorder book/page or case number, links to evidence room PDFs and transcriptions.

| Entry | Year | Evidence Room Links |
|-------|------|-------------------|
| Bixby Partition | 1882 | Tract map md (`docs/tract-maps/1880-rancho-los-palos-verdes-patent-plat-book-2-pp-543-546.md`) |
| Declaration No. One | 1949 | PDF (`docs/originals/declarations/1949-WPBCA-Declaration.pdf`), verbatim (`docs/declarations/1949-WPBCA-Declaration-No-One-Verbatim.md`) |
| Declaration of Easements | 1949 | PDF (`docs/originals/declarations/1949-Declaration-of-Easements.pdf`), verbatim (`docs/declarations/1949-Declaration-of-Easements-Verbatim.md`) |
| Lot H Declaration | 1950 | PDF (bundled in `docs/originals/declarations/1949-1950-Amendments.pdf`), verbatim (`docs/declarations/1950-Lot-H-Declaration-Verbatim.md`) |
| Declaration One-A | 1950 | Verbatim (`docs/declarations/1950-Declaration-One-A-Verbatim.md`) |
| Wong Subdivision | 1980 | Tract map PDF (`docs/originals/tract-maps/1980-06-17-Tract-32977-Lot-H-Subdivision-MB950-PG14-15.pdf`), md (`docs/tract-maps/1980-06-17-Tract-32977-Lot-H-Subdivision-MB950-PG14-15.md`) |
| Reversion | 1986 | Tract map PDF (`docs/originals/tract-maps/1986-02-26-Tract-43725-Reversion-To-Acreage-MB1063-PG91-92.pdf`), md (`docs/tract-maps/1986-02-26-Tract-43725-Reversion-To-Acreage-MB1063-PG91-92.md`) |
| Restated Declaration | 2009 | PDF (`docs/originals/declarations/2009-Restated-Declaration.pdf`), text (`docs/declarations/2009-Restated-Declaration-Text.md`) |
| Rezoning | 2024 | City council comment (`docs/litigation/2024-06-04-Comment-to-City-Council-Re-0-Clipper-Rezoning-Verbatim.md`) |

### Tier 2 — Context with Citations

2-3 sentences of context in the expand. Link to evidence room document if we hold it, or civic URL if public.

| Entry | Year | Link Source |
|-------|------|------------|
| Vanderlip Purchase | 1913 | No document held — fact only |
| Olmsted Master Plan | 1923 | External: Library of Congress job file URL |
| PV Corporation | 1925 | No articles on disk — fact only |
| Declaration 100 | 1929 | HTML (`docs/declarations/1929-declaration-100-basic-protective-restrictions-book-9436.html`) |
| Declaration 101 | 1929 | HTML (`docs/declarations/1929-declaration-101-local-protective-restrictions-book-9482.html`) |
| Shore Club | 1929 | Shore Club corporate archives (`docs/shore-club/Abalone-Shore-Club-Corporate-Archives-Verbatim.md`) |
| Filiorum Grant | 1930 | Transcription (`docs/declarations/1930-pvcorp-to-filiorum-grant-deed-book-10226.md`), deed images in `images/` |
| Condos vs. Park | 1972 | Shore Club board docs (`docs/shore-club/1971-1972-Shore-Club-Board-Docs-Verbatim.md`), Karshner proposal, fact sheet, WPBCA letter |
| RPV Incorporates | 1973 | No document held — fact only |
| Coastal Act | 1976 | External: California Coastal Commission URL |
| Coastal Specific Plan | 1978 | External: RPV municipal code / general plan URL if available, otherwise fact only |
| The Landslide | 1956 | CSB survey docs (`docs/geological/`) |
| Abalone Cove Slide | 1974 | Geological survey docs if applicable |
| Grant Deeds | 1952 | PDF + verbatim (`docs/originals/declarations/1952-PVCorp-Grant-Deed-Lot1.pdf`) |
| Great Lakes Carbon | 1953 | No document held — fact only |
| Modification | 1949 | PDF (bundled in Amendments), verbatim (`docs/declarations/1949-Modification-of-Protective-Restrictions-Verbatim.md`) |
| FPPC Complaint | 2024 | PDF (`docs/originals/litigation/2024-08-07-FPPC-Complaint-Cruikshank.pdf`), verbatim |
| Petition Filed | 2024 | Demurrer + opposition PDFs and verbatims |
| HCD Confirms | 2025 | No document held — fact only |
| City Keeps Site 16 | 2025 | No document held — fact only |
| Clipper Development | 2021 | Title report PDF (`docs/originals/property/2026-03-25-CTC-Title-Report-0-Clipper-APN-7573-006-024.pdf`) |

### Tier 3 — One-Liners (no expand)

| Entry | Year | Notes |
|-------|------|-------|
| Vanderlip Sr. Dies | 1937 | Biographical context only |
| PV Corp Dissolved | 1954 | Fact — Delaware dissolution |
| Emergency Declaration | 2024 | Governor's proclamation — no document held |
| Ground Movement | 2026 | Current conditions — fact only |

## New Entries to Add

The chain-of-title document and evidence inventory reveal entries missing from the current timeline:

| Entry | Year | Why |
|-------|------|-----|
| Declaration of Easements | 1949 | Tier 1 document — ocean access easements |
| Modification of Protective Restrictions | 1949 | Tier 2 — amends Declaration No. One |
| Declaration One-A (Lots 1-5) | 1950 | Tier 2 — bluff setback protections |
| 2014 Redevelopment Conveyance | 2014 | Key event — Shoreline Park parcels conveyed to city, Dec 100/101 never referenced |

## Content Rule

**Only link what exists on disk. Only claim what the record proves.**

- Document exists as PDF or transcription in evidence room → relative link
- Public civic record with known stable URL → external link with `::after` arrow
- Neither → state the fact, no link
- No `href="#"` stubs anywhere on the page
- Every link verified against the file inventory before commit

## CSS Additions

Minimal additions to the existing stylesheet:

```css
/* Era dividers */
.timeline-era {
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--shell-sage);
  text-align: center;
  margin: 3rem 0 2rem;
  padding: 0.5rem 0;
  border-top: 1px solid var(--shell-warm);
  border-bottom: 1px solid var(--shell-warm);
  font-weight: normal;
}

/* Details expand */
.timeline-detail {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  line-height: 1.6;
}

.timeline-detail summary {
  cursor: pointer;
  color: var(--shell-teal);
  font-size: 0.8rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.timeline-detail summary::-webkit-details-marker {
  color: var(--shell-warm);
}

.timeline-detail p {
  margin: 0.5rem 0;
  color: var(--shell-dark);
  opacity: 0.85;
}

.timeline-detail ul {
  list-style: none;
  margin: 0.5rem 0 0;
  padding: 0;
}

.timeline-detail li {
  margin: 0.25rem 0;
}

.timeline-detail a {
  color: var(--shell-teal);
  text-decoration: underline;
  text-decoration-color: var(--shell-warm);
  text-underline-offset: 2px;
}

/* External link indicator */
a[href^="http"]::after {
  content: " ↗";
  font-size: 0.75em;
  opacity: 0.5;
}

/* Print: collapse details */
@media print {
  .timeline-detail { display: none; }
}
```

## File Changes

| File | Action |
|------|--------|
| `timeline/index.html` | Rewrite — enriched entries, era dividers, new CSS, updated intro |

No other files are created or modified. The evidence room and docs stay as-is. This is a single-file change.

## Verification

Before commit:
1. Open `timeline/index.html` from Finder (file:// protocol) — all internal links work
2. Every relative link resolves to a file that exists on disk
3. No `href="#"` anywhere in the page
4. `<details>` elements expand/collapse without JavaScript
5. Mobile responsive — hamburger nav, narrower year column
6. External links marked with arrow indicator
