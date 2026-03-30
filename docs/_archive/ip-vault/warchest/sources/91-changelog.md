---
type: pitch
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Change Log

> *Version history for the GrowDirect Private Briefing.*

---

## Version 2.5 — February 27, 2026

**Full navigation overhaul + embed fix + elJeffe conversion**

- Replaced horizontal nav with dropdown SECTIONS menu — full section list with numbered entries
- Current section name displayed in top bar next to menu button
- Dropdown includes utility pages under "Reference & Governance" divider
- Embedded pages (Economy, Product) now wrapped with auth, nav, prev/next, and footer via iframe
- Resolved ISS-013 (embed pages bypass auth) and ISS-014 (embed pages missing nav)
- Converted elJeffe from embedded HTML orbital diagram to narrative markdown page
- elJeffe re-added to pack and investor feeds (was set aside in v2.2)
- Pack now builds 22 pages (18 content + 4 utility)

---

## Version 2.4 — February 27, 2026

**Market & Financial Model — P0 gaps closed**

- Added The Market (WP-4.3) — TAM/SAM/SOM, competitive landscape, defensible moat, platform play
- Added The Financials (WP-4.4) — revenue model, unit economics, 3-year projections, operating costs
- Archived 4 slide decks to `archive/slides/`
- Resolved ISS-001 (Financial Model) and ISS-004 (Market Analysis)
- Pack now builds 21 pages (17 content + 4 utility)

---

## Version 2.3 — February 27, 2026

**Full navigation overhaul + reference pages**

- Added session-based authentication — navigate between pages without re-entering access code
- Fixed top navigation bar across all pages including index
- Added previous/next navigation at the bottom of every section
- Added Disclaimer, Change Log, Issues, and References as utility pages
- Utility pages accessible from footer and index TOC
- Back-to-index navigation via GROWDIRECT logo on every page

---

## Version 2.2 — February 27, 2026

**elJeffe page set aside**

- Removed elJeffe orbital diagram from pack (duplicated The Economy content)
- Section preserved in catalog for future use, removed from all output feeds
- Pack now builds 15 content pages

---

## Version 2.1 — February 27, 2026

**Full content library population**

- Added 8 new source files: Investment Thesis, Architecture, Data Model, How We Build, Team, Compliance, Protection, The Article
- All 16 sections now have content (up from 8)
- Agent name sanitization pass — removed all internal team references from external-facing content
- Fixed internal team references in product prototype to role-based labels
- Working Papers index created (WORKING_PAPERS.md) — 7 domains, 37 chapters, 200+ files mapped

---

## Version 2.0 — February 27, 2026

**War Chest v2.0 manifest redesign**

- Manifest upgraded with feeds routing (pack, investor, public)
- Outputs block added (pack, investor, public targets)
- Published version history added to manifest
- Build script patched for feeds-based filtering
- Muted text color improved from #5a5a5a to #8a8a8a for readability

---

## Version 0.6 — February 27, 2026

**Pre-population build**

- 8 existing content sections built (Pitch, Economy, Play, Product, Fox, Goose, Owl, elJeffe)
- Password gate operational
- Pack archived to archive/v0.6/

---

## Version 0.5 — February 27, 2026

- Navigation refinements
- Table styling improvements
- Section ordering stabilized

---

## Version 0.4 — February 27, 2026

- Design system implementation (Bebas Neue, DM Sans, Space Mono)
- Bitcoin-orange gradient treatment for headings
- Grain texture overlay
- Card component styling

---

## Version 0.3 — February 27, 2026

- Multi-page site structure implemented
- Table of contents index page
- Per-section HTML generation from markdown sources

---

## Version 0.2 — February 27, 2026

- Initial password-gated prototype
- Basic markdown-to-HTML conversion
- First archived build

---

*GrowDirect Confidential*
