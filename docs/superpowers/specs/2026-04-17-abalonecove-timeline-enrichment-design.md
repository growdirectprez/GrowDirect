# Abalone Cove Timeline Enrichment — Design Spec

**Date:** 2026-04-17
**Project:** abalonecove.org (static site, GitHub Pages)
**File:** `~/abalonecove/timeline/index.html`

> **Parent specs:** The [Abalone Cove Foundation consolidated design spec (2026-04-18)](2026-04-18-abalone-cove-foundation-design.md) is the top-level parent (entity, mission, strategy). The [abalonecove.org design spec (2026-04-16)](2026-04-16-abalonecove-org-design.md) is the Surface 1 parent (site architecture, narrative spine). This timeline spec is a sub-component of Surface 1.
>
> **2026-04-19 synthesis update:** inventory expands to include new anchor dates derived from the five Cove synthesis articles ([planning framework](../../../Brain/wiki/cove-rpv-planning-framework-2026.md), [case-law ledger](../../../Brain/wiki/cove-case-law-lessons.md), [species constraints](../../../Brain/wiki/cove-endangered-species-constraints.md), [2018 Safety Element](../../../Brain/wiki/cove-rpv-safety-element-2018.md), [lessons learned](../../../Brain/wiki/cove-lessons-learned.md)). See "2026-04-19 Entry Additions" below.

---

## Purpose

Transform the timeline page from a flat chronological list into the Abalone Cove Foundation's definitive public record of land use regulation, geological events, and civic decisions at Abalone Cove and the Palos Verdes south coast.

This is not an HOA document. It is the factual basis for a 501(c)(3) foundation — credible enough for a donor, clear enough for a neighbor, thorough enough for a commissioner. Every entry that references a document closes the loop: link to the evidence room if we hold it, link to a civic source if it's public, or state the fact with no link if neither exists. No stubs. No broken links. No promises.

## Constraints

- Pure static HTML with embedded CSS. No JavaScript. No build tools.
- All internal links use relative paths (`../evidence/`, `../docs/`). Site must work from `file://` for PDF links and page navigation. The document viewer (`docs/viewer.html`) requires a web server (`fetch` + `marked.js`) and will not function offline — this is a known limitation. For offline use, PDF links open natively; transcription links show raw markdown.
- Same design system as the rest of abalonecove.org (shell-teal, shell-cream, Georgia serif, 680px max-width, sticky header with hamburger nav).
- No new CSS patterns beyond `<details>` styling and era dividers.

### Navigation and file:// compatibility

The existing site uses absolute root-relative paths in navigation (`/evidence/`, `/timeline/`, etc.) across all pages. These do not work under `file://` protocol. This is a site-wide limitation, not specific to the timeline.

For this spec: **the timeline page uses relative paths for all document links** (`../docs/...`, `../evidence/...`) so evidence room links work from `file://`. Navigation links remain absolute (matching the rest of the site) — fixing nav paths site-wide is out of scope.

## Page Structure

### Header
Same sticky header/nav as all other pages. Timeline link gets `aria-current="page"`. Use the border-bottom style for `aria-current` (matching the evidence room pattern): `border-bottom: 1px solid var(--shell-teal)`.

### Intro
- **Title:** "Timeline"
- **Subtitle:** "The regulatory record of Abalone Cove, 1882–2026"
- **Intro paragraph:** "A chronological record of the land itself — the restrictions placed on it, the geological forces acting on it, and the civic decisions that shaped it. Every document cited here is linked to its source."

### Era Groupings

The timeline is divided into four eras with styled `<h2>` dividers. The vertical timeline line runs continuously behind the dividers. Each divider has `background: var(--shell-cream)` with enough horizontal padding to visually mask the line segment behind it.

1. **Rancho Era** (1882–1925)
2. **Declarations & Development** (1929–1954)
3. **Geology, Regulation & Resistance** (1946–2008) — *2026-04-19 expansion: extended from 1956–1986 to cover the 1946 federal geological report pre-dating the slide, and the 1994 / 2001 / 2008 SCOTUS / *Monks* litigation arc*
4. **Modern Era** (2018–2026) — *2026-04-19 adjustment: start moved from 2009 to 2018 to align with the 2018 General Plan + Safety Element adoption that defines the current regulatory framework*

### Timeline Entries

Each entry retains the existing layout (year label, dot on vertical line, title, description). Enriched entries add a `<details>` element below the description.

**`<summary>` labels:**
- "Record" for document-based entries (declarations, deeds, tract maps)
- "Context" for regulatory and event entries (Coastal Act, landslides, rezoning)

### Link Format

Two link types per entry:

1. **PDF originals** — link directly to the file. Use `-ocr.pdf` versions when available (consistent with evidence room). Format: `../docs/originals/declarations/1949-WPBCA-Declaration-ocr.pdf`
2. **Transcriptions** — link through the document viewer. Format: `../docs/viewer.html?doc=/docs/declarations/1949-WPBCA-Declaration-No-One-Verbatim.md&original=/docs/originals/declarations/1949-WPBCA-Declaration-ocr.pdf`

This matches how the evidence room links documents. Viewer links require a web server; PDF links work offline.

**External link indicator:** Scoped to timeline content only. Any `<a>` with an external href inside `.timeline-detail` gets a CSS `::after` arrow. Selector: `.timeline-detail a[href^="http"]::after`.

### Footer
Same footer as all other pages.

## Entry Inventory

### Tier 1 — Full Breakdown

Full chain-of-title treatment: what the document does, what flows from it, recorder book/page, links to evidence room.

| Entry | Year | PDF | Transcription |
|-------|------|-----|---------------|
| Bixby Partition | 1882 | — | `docs/tract-maps/1880-rancho-los-palos-verdes-patent-plat-book-2-pp-543-546.md` |
| Declaration No. One | 1949 | `docs/originals/declarations/1949-WPBCA-Declaration-ocr.pdf` | `docs/declarations/1949-WPBCA-Declaration-No-One-Verbatim.md` |
| Declaration of Easements | 1949 | `docs/originals/declarations/1949-Declaration-of-Easements-ocr.pdf` | `docs/declarations/1949-Declaration-of-Easements-Verbatim.md` |
| Lot H Declaration | 1950 | `docs/originals/declarations/1949-1950-Amendments-ocr.pdf` | `docs/declarations/1950-Lot-H-Declaration-Verbatim.md` |
| Wong Subdivision | 1980 | `docs/originals/tract-maps/1980-06-17-Tract-32977-Lot-H-Subdivision-MB950-PG14-15.pdf` | `docs/tract-maps/1980-06-17-Tract-32977-Lot-H-Subdivision-MB950-PG14-15.md` |
| Reversion to Acreage | 1986 | `docs/originals/tract-maps/1986-02-26-Tract-43725-Reversion-To-Acreage-MB1063-PG91-92.pdf` | `docs/tract-maps/1986-02-26-Tract-43725-Reversion-To-Acreage-MB1063-PG91-92.md` |
| Restated Declaration | 2009 | `docs/originals/declarations/2009-Restated-Declaration.pdf` | `docs/declarations/2009-Restated-Declaration-Text.md` |
| Rezoning | 2024 | — | `docs/litigation/2024-06-04-Comment-to-City-Council-Re-0-Clipper-Rezoning-Verbatim.md` |

### Tier 2 — Context with Citations

2-3 sentences of context in the expand. Links to evidence room or civic sources.

| Entry | Year | Link Source |
|-------|------|------------|
| Vanderlip Purchase | 1913 | No document held — fact only |
| Olmsted Master Plan | 1923 | External: `https://www.loc.gov/collections/olmsted-associates-records/` (LOC) |
| PV Corporation | 1925 | No document held — fact only |
| Declaration 100 | 1929 | `docs/declarations/1929-declaration-100-basic-protective-restrictions-book-9436.html` |
| Declaration 101 | 1929 | `docs/declarations/1929-declaration-101-local-protective-restrictions-book-9482.html` |
| Shore Club | 1929 | `docs/shore-club/Abalone-Shore-Club-Corporate-Archives-Verbatim.md` |
| Filiorum Grant | 1930 | `docs/declarations/1930-pvcorp-to-filiorum-grant-deed-book-10226.md`, deed images: `images/filiorum-deed-grant.jpeg`, `images/filiorum-deed-restrictions.jpeg` |
| Modification | 1949 | `docs/originals/declarations/1949-1950-Amendments-ocr.pdf`, `docs/declarations/1949-Modification-of-Protective-Restrictions-Verbatim.md` |
| Declaration One-A | 1950 | `docs/declarations/1950-Declaration-One-A-Verbatim.md` |
| Grant Deeds (template) | 1952 | `docs/originals/declarations/1952-PVCorp-Grant-Deed-Lot1-ocr.pdf`, `docs/declarations/1952-PVCorp-Grant-Deed-Lot1-Verbatim.md` |
| Great Lakes Carbon | 1953 | No document held — fact only |
| Condos vs. Park | 1972 | `docs/shore-club/1971-1972-Shore-Club-Board-Docs-Verbatim.md`, `docs/shore-club/1972-Karshner-Proposal-Verbatim.md`, `docs/shore-club/1972-Abalone-Cove-Fact-Sheet-Verbatim.md`, `docs/shore-club/WPBCA-Letter-Condos-vs-Park-Verbatim.md` |
| RPV Incorporates | 1973 | No document held — fact only |
| Coastal Act | 1976 | External: California Coastal Commission URL |
| Coastal Specific Plan | 1978 | External: RPV municipal code URL if available, otherwise fact only |
| The Landslide | 1956 | `docs/geological/1935-county-surveyor-CSB1082-2-pv-drive-south.md` |
| Abalone Cove Slide | 1974 | No specific document — fact only |
| Clipper Development | 2021 | `docs/originals/property/2026-03-25-CTC-Title-Report-0-Clipper-APN-7573-006-024.pdf` |
| FPPC Complaint | 2024 | `docs/originals/litigation/2024-08-07-FPPC-Complaint-Cruikshank.pdf`, `docs/litigation/2024-08-07-FPPC-Complaint-Cruikshank-Verbatim.md` |
| Petition Filed | 2024 | `docs/originals/litigation/2024-11-27-City-Demurrer.pdf`, `docs/litigation/2024-11-27-City-Demurrer-Verbatim.md`, `docs/originals/litigation/2024-12-18-Opposition-to-Demurrer.pdf`, `docs/litigation/2024-12-18-Opposition-to-Demurrer-Verbatim.md` |
| HCD Confirms | 2025 | No document held — fact only |
| City Keeps Site 16 | 2025 | No document held — fact only |

### Tier 3 — One-Liners (no expand)

| Entry | Year |
|-------|------|
| Vanderlip Sr. Dies | 1937 |
| PV Corp Dissolved | 1954 |
| Emergency Declaration | 2024 |
| Ground Movement | 2026 |

## 2026-04-19 Entry Additions (from synthesis pass)

The 2026-04-19 cross-cutting synthesis surfaced anchor dates that belong in the inventory. These are additive — they do not replace or modify the Tier 1 / Tier 2 / Tier 3 tables above.

### New entries

| Entry | Year | Era | Tier | Source / citation |
|-------|------|-----|------|-------------------|
| Federal geological report on Portuguese Bend prehistoric slide plane | 1946 | Geology, Regulation & Resistance | 2 | Woodring 1946 USGS. Cited in *Albers* (1965) opinion as having been known to both the county and developers. Source: [`cove-case-law-lessons`](../../../Brain/wiki/cove-case-law-lessons.md) R10 |
| *Albers v. County of Los Angeles* — CA Supreme Court judgment | 1965 | Geology, Regulation & Resistance | 1 | 62 Cal. 2d 250. Judgments aggregating $5,360,000 affirmed on inverse-condemnation theory. Archive: [`1965-albers-v-county-la-supreme-court.md`](../../../Cove/docs/archive/originals/city-records/litigation/1965-albers-v-county-la-supreme-court.md); Synthesis: [`cove-case-law-lessons`](../../../Brain/wiki/cove-case-law-lessons.md) R9 |
| *Stuart v. City of Rancho Palos Verdes* — SCOTUS cert petition | 1994 | Geology, Regulation & Resistance | 2 | Filed May 31, 1994 (October Term 1993). Pro Per. Question 5 raised secret-meeting / collusion vector. Source: [`coac-rpv-scotus-petitions`](../../../Brain/wiki/coac-rpv-scotus-petitions.md) |
| *Echevarrieta v. City of Rancho Palos Verdes* — SCOTUS cert petition | 2001 | Geology, Regulation & Resistance | 2 | Filed June 19, 2001. Counseled (Robert Hampton Rogers, Sullivan, Workman & Dee LLP). View-ordinance takings argument. Source: [`coac-rpv-scotus-petitions`](../../../Brain/wiki/coac-rpv-scotus-petitions.md) |
| *Monks v. City of Rancho Palos Verdes* — CA Court of Appeal | 2008 | Geology, Regulation & Resistance | 2 | 167 Cal. App. 4th 263. Upheld RPV landslide-moratorium framework. Source: [`cove-case-law-lessons`](../../../Brain/wiki/cove-case-law-lessons.md) R11 |
| RPV 2018 General Plan + Safety Element adopted | 2018 | Modern Era | 2 | September 2018. Palos Verdes Fault Mw 7.3 / MMI XI at 0.691g PGA. Landslide Inventory Figure 3. Fire Hazard Severity Zone Figure 1. Coastal Cliff Retreat §5.9 validates Dec. One-A 40-ft bluff setback. Source: [`cove-rpv-safety-element-2018`](../../../Brain/wiki/cove-rpv-safety-element-2018.md) |
| *Colyear v. Rolling Hills Community Assn* — CA Court of Appeal | 2024 | Modern Era | 1 | Case B308382, March 1, 2024, certified for partial publication. Controls chain-of-title rule for PV Corp master declarations. Source: [`cove-colyear-2024`](../../../Brain/wiki/cove-colyear-2024.md) |
| Landslide moratorium made permanent | 2025 | Modern Era | 2 | Per [`cove-pvplc-partnership`](../../../Brain/wiki/cove-pvplc-partnership.md) timeline. Ordinance or resolution text — **open source thread**, confirm before publication |

### Tier upgrades (existing entries)

| Entry | Year | Change | Rationale |
|-------|------|--------|-----------|
| The Landslide | 1956 | Tier 2 → upgrade expand content | Cite 2018 Safety Element §5.3 language: "most studied and publicized landslide in the area, and perhaps in the Los Angeles Basin." Upper boundary under debate (Valley View Graben vs. Dibblee 1999). 1956 trigger = 175,000 cu yd grading fill in the Crenshaw extension easement per *Albers* (1965) record |
| Coastal Specific Plan | 1978 | Tier 2 → add internal synthesis link | Link to [`cove-coastal-specific-plan-s4`](../../../Brain/wiki/cove-coastal-specific-plan-s4.md) + [`cove-rpv-planning-framework-2026`](../../../Brain/wiki/cove-rpv-planning-framework-2026.md) for Subregion 4 operational framework |

### Citations pending verification (do not publish until resolved)

- **"Carlsbad, April 2026"** CC&R ruling referenced in abalonecove.org design spec §12 — open contradiction **OC-1** in [`cove-lessons-learned`](../../../Brain/wiki/cove-lessons-learned.md). If/when resolved, add as a timeline entry with proper citation.
- **RPV 2024 HE 6th-cycle adoption** (April 16, 2024) — staff report in archive but **HCD certification status is open contradiction OC-4**. Entry should be added at Tier 2 once certification status is confirmed.

---

## Entry Changes from Current Timeline

### Rename
- "Ocean Access Easement" (1949) → **removed as separate entry**. This is the Declaration of Easements (1949), which is now a Tier 1 entry. The ocean access easement detail is covered in the expand content for that entry.

### New Entries
| Entry | Year | Tier | Why |
|-------|------|------|-----|
| Declaration of Easements | 1949 | 1 | Replaces "Ocean Access Easement" — full document treatment |
| Modification of Protective Restrictions | 1949 | 2 | Amends Declaration No. One |
| Declaration One-A (Lots 1-5) | 1950 | 2 | Bluff setback protections |
| 2014 Redevelopment Conveyance | 2014 | 2 | Shoreline Park parcels conveyed to city — Dec 100/101 never referenced |

## Content Rule

**Only link what exists on disk. Only claim what the record proves.**

- Document exists as PDF in evidence room → direct relative link to PDF
- Document has transcription → viewer link with `?doc=` and `?original=` params
- Public civic record with known stable URL → external link
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
  padding: 0.5rem 1.5rem;
  border-top: 1px solid var(--shell-warm);
  border-bottom: 1px solid var(--shell-warm);
  font-weight: normal;
  background: var(--shell-cream);
  position: relative;
  z-index: 1;
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

/* External link indicator — scoped to timeline details only */
.timeline-detail a[href^="http"]::after {
  content: " \2197";
  font-size: 0.75em;
  opacity: 0.5;
}

/* Print: collapse details */
@media print {
  .timeline-detail { display: none; }
}
```

## Markup Example

```html
<!-- Era divider -->
<h2 class="timeline-era">Declarations & Development</h2>

<!-- Tier 1 entry -->
<div class="timeline-entry">
  <div class="timeline-year">1949</div>
  <div class="timeline-body">
    <div class="timeline-title">Declaration No. One</div>
    <div class="timeline-desc">Tract 14649 established &mdash; WPBCA created, 81 lots, single-family only</div>
    <details class="timeline-detail">
      <summary>Record</summary>
      <p>Book 29980, Page 159, LA County Recorder. Signed by Kelvin C. Vanderlip (President) and John H. Robertson (Asst. Secretary) for Palos Verdes Corporation.</p>
      <p>Creates the community's governing framework: single-family residential use, Architectural Review Committee, maintenance assessments, enforcement and reversion of title. Article VIII provides mechanism to annex Lot "H" land. Duration: until Jan 1, 1974, then auto-renews in 10-year periods.</p>
      <ul>
        <li><a href="../docs/originals/declarations/1949-WPBCA-Declaration-ocr.pdf">Original document (PDF)</a></li>
        <li><a href="../docs/viewer.html?doc=/docs/declarations/1949-WPBCA-Declaration-No-One-Verbatim.md&original=/docs/originals/declarations/1949-WPBCA-Declaration-ocr.pdf">Verbatim transcription</a></li>
      </ul>
    </details>
  </div>
</div>

<!-- Tier 2 entry -->
<div class="timeline-entry">
  <div class="timeline-year">1976</div>
  <div class="timeline-body">
    <div class="timeline-title">California Coastal Act</div>
    <div class="timeline-desc">Creates permanent Coastal Commission &mdash; development within the coastal zone requires a permit</div>
    <details class="timeline-detail">
      <summary>Context</summary>
      <p>Establishes state authority over development in the coastal zone. The Abalone Cove area falls within this zone. Any new construction requires a Coastal Development Permit in addition to city approvals.</p>
      <ul>
        <li><a href="https://www.coastal.ca.gov/coastact.pdf">California Coastal Act (full text)</a></li>
      </ul>
    </details>
  </div>
</div>

<!-- Tier 3 entry — no expand -->
<div class="timeline-entry">
  <div class="timeline-year">1937</div>
  <div class="timeline-body">
    <div class="timeline-title">Vanderlip Sr. Dies</div>
    <div class="timeline-desc">Frank Vanderlip Sr. passes; sons not yet of age</div>
  </div>
</div>
```

## File Changes

| File | Action |
|------|--------|
| `timeline/index.html` | Rewrite — enriched entries, era dividers, new CSS, updated intro |

No other files are created or modified. The evidence room and docs stay as-is. This is a single-file change.

## Verification

Before commit:
1. Open `timeline/index.html` from Finder (`file://` protocol) — PDF links open, page renders
2. Every relative link resolves to a file that exists on disk
3. No `href="#"` anywhere in the page
4. `<details>` elements expand/collapse without JavaScript
5. Mobile responsive — hamburger nav, narrower year column
6. External links marked with arrow indicator (only inside `.timeline-detail`)
7. Viewer links work when served from a web server (`python3 -m http.server`)
8. `aria-current` uses border-bottom style
