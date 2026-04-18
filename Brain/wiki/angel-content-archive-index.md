---
date: 2026-04-13
type: wiki
status: active
tags: [angel, archive, content-inventory, data-sources, collateral]
sources: [Angel/ directory scan]
last-compiled: 2026-04-13
---

# Angel Content Archive — Index & Catalog Plan

## Summary

The `Angel/` directory contains ~1.26 GB across 412 files — a mix of CRMLS data exports, Compass marketing collateral, HTML prototypes, brainstorm artifacts, listing photos, and raw data files. Much of this has never been cataloged or imported. This article indexes everything and defines the work needed to make it usable.

## File Inventory by Type

| Type | Files | Size | What It Is |
|------|-------|------|------------|
| .pdf | 30 | 617 MB | Listing presentations, buyer guides, trifolds, prototypes, marketing collateral |
| .zip | 1 | 608 MB | New Compass content drop (April 13 — needs extraction and catalog) |
| .jpg | 218 | 20 MB | CRMLS listing photos, Lightning/CMA exports |
| .html | 30 | 3.6 MB | Brainstorm prototypes, early Angel concepts, OwnPV site |
| .png | 29 | 7.4 MB | Logos (AREA, Compass), UI assets |
| .csv | 14 | 0.8 MB | Hot Sheets, 1004MC appraisal data, market reports, agent roster |
| .docx | 12 | 1.1 MB | Agent bios, email signatures, client date sheets, open house signs |
| .md | 44 | 0.3 MB | Knowledge base articles, scaffold notes |
| .py | 13 | 0.1 MB | Legacy Angel code (pre-Cove-module era) |
| .txt | 3 | 0.5 MB | Lightning and CMA listing exports (tab-delimited) |
| Other | misc | ~0.5 MB | .pptx, .pages, .svg, .jsx, .json, .pre |

## Unprocessed Data (Import Candidates)

### Hot Sheet CSVs (5 files)
Daily CRMLS listing event data — new listings, price changes, status changes, back-on-market.
- `Agent Hot Sheet.csv` through `Agent Hot Sheet-5.csv`
- These should be imported into `listing_events` table
- Source for the Tuesday "What's New" content

### Don's 1004MC CSVs (6 files)
Appraisal comparable data in FNMA 1004MC form format. Likely from an appraiser Angelique works with.
- `Don's 1004MC.csv` through `Don's 1004MC-6.csv`
- Contains comp selections, adjustments, value conclusions
- Could feed into CMA/valuation intelligence

### Lightning v2 Export
Tab-delimited CRMLS export with fields NOT in Top Producer:
- Zip codes (missing from TP)
- School assignments (elementary, middle, high)
- Showing instructions
- Full public remarks with agent commentary
- Should be imported — fills gaps in our listings data

### Neighborhood Market Report CSV
Pre-built CRMLS market statistics — likely aggregate data by area.
- Compare against our computed `market_snapshots` for validation

### Agent 1 Line CSV
Agent roster/contact data from CRMLS.
- Feeds into the future `agents` table

### Full.csv
Unknown scope — could be a comprehensive listing export. Needs inspection.

### Pocket Real Estate - Residential.pre
Another CRMLS export format. Needs format analysis.

### New Zip (608 MB — April 13, 2026) — DUPLICATE, SAFE TO DELETE
`4. Angelique Lyle-20260413T214528Z-3-001.zip`
**Verified 2026-04-13:** Extracted and compared file-by-file. Identical to `Compass Content - Angelique Lyle/` — 55 files, same sizes. This is a Google Drive export of the same Compass content already in the repo. Safe to delete to reclaim 608 MB.

## Marketing Collateral — Compass Content (Fully Cataloged)

`Angel/Compass Content - Angelique Lyle/` — 55 files, 613 MB, 15 directories.

### Collateral Inventory by Category

**Print Material (17 files, ~370 MB):**
| File | Year | Type | Size |
|------|------|------|------|
| Angelique Buyers Guide 2023 | 2023 | Buyer's Guide | 18 MB |
| Buyers Workbook Bifold | 2023 | Buyer's Workbook | 7 MB |
| Angelique Cover Letter August 2023 | 2023 | Cover Letter | 2 MB |
| AREA Camera Ready Home Checklist | 2023 | Checklist | 76 KB |
| Social Media Friendly Home | 2023 | Social Media Guide | 170 KB |
| Angelique 2024 Buyers Guide with Origin Point | 2024 | Buyer's Guide | 31 MB |
| 2024 Listing Presentation | 2024 | Listing Pres | 24 MB |
| Compass Concierge Flyer | 2024 | Flyer | 3 MB |
| Private Exclusive Flyer Campaign | 2024 | Flyer | 4 MB |
| AREA Escrow Roadmap | undated | Process Guide | 5 MB |
| Angelique - Insta QR | undated | QR Code | 1 MB |
| Angelique-Lyle---2026-Buyers-Guide | 2026 | Buyer's Guide | 18 MB |

**Print Material/2025 (4 files, 243 MB — DUPLICATED in 2025/ root):**
| File | Type | Size |
|------|------|------|
| AREA Team Marketing Presentation 2025 | Team Pres | 33 MB |
| Compass Concierge Booklet 2025 | Concierge | 138 MB |
| 2025 Listing Presentation | Listing Pres | 36 MB |
| 2025 Buyers Guide | Buyer's Guide | 35 MB |

**2025/ root (4 files — same content as Print Material/2025/, sizes differ by <2 MB):**
Duplicates of Print Material/2025/ with minor size variations (different export timestamps). One copy should be deleted.

**2026/ (4 files, 42 MB):**
| File | Type | Size |
|------|------|------|
| AREA Team Page (April 2026) | Team Pres | 3 MB |
| 2026 Buyers Guide | Buyer's Guide | 18 MB |
| Horse Properties Flyer Campaign | Flyer | 13 MB |
| AREA Trifold / Brochure (April 2026) | Trifold | 8 MB |

**AREA Logo Downloads (17 files, 1.5 MB):** Full logo suite — horizontal, vertical, mark, agent brand, social circle variants in white/black/on-black. SVG + PNG.

**Agent Bio (2 files):** Agent bio (.docx) + social accounts (.docx)

**AREA Email Signature (1 file):** Angelique AREA email signature (.docx)

**Open House (8 files):** OH standard template, checklist, please sign in display, directional arrows, access signs, garage/storage signs.

**Important Dates & Contacts (3 files):** Buyer/seller/listing important dates templates (.docx)

**Empty Placeholder Directories:**
- `AREA QR CODES/` — empty, awaiting content
- `2026/2026 Listing Presentation/` — empty, 2026 listing pres not yet created

## HTML Prototypes (Brainstorm Era)

Early Angel concepts from before the Cove module architecture:

| File | What It Is |
|------|------------|
| `this-week-on-the-hill.html` / `this-week-v2.html` | "What's New This Week" newsletter prototype |
| `prototype-angeliquelyle.html` | LP homepage concept |
| `prototype-lp-homepage.html` | Another LP concept |
| `askangel-home.html` | Ask Angel chat page prototype |
| `pipeline_dashboard.html` | CRM pipeline dashboard |
| `neighborhood-school-guide.html` | School guide prototype |
| `ownpalosverdes_v2.html` | OwnPV site concept |
| `school_guide.html` | School guide v1 |
| `brand-system.html` | Brand identity concept |
| `compass_listing_playbook.html` | Listing strategy prototype |
| `compass_mcp_architecture.html` | Early MCP architecture concept |
| `crm_integration_pipeline.html` | CRM pipeline concept |
| `ai_intelligence_system.html` | AI system concept |
| `angelique_agentic_profile.html` | Agentic profile prototype |
| `lp-welcome-inject.html` | LP widget injection concept |
| `open-house-signin/` | Open house sign-in with QR code |
| `ownpalosverdes_deploy/` | Deployed OwnPV site (index + schools) |

## Historical Photography

`Angel/media/` — vintage PV peninsula photos:
- `humphrey-bluff-cove.jpg` — Bluff Cove historic photo
- `humphrey-chandler-preserve.jpg` — Chandler Preserve historic
- `humphrey-lost-horizon-lighthouse.jpg` — Point Vicente historic
- `humphrey-point-vicente.jpg` — Point Vicente historic
- `lighthouse-1937.jpg` — 1937 lighthouse photo
- `neptune-fountain-vintage.jpg` — Malaga Cove Neptune Fountain vintage

These are content assets for TheHillPV.com — historical context for neighborhood articles.

## Reference Images

`Angel/reference/` — Angelique's original 2-page printed neighborhood guide:
- `angelique-guide-page1-neighborhoods.jpeg`
- `angelique-guide-page2-lifestyle.jpeg`

This is the source document that the entire South Bay Wiki is replacing.

## Brokerage History & Content Eras

Angelique's 20-year career spans four brokerages. Content from all eras is scattered across NAS, Dropbox, and local drives:

| Era | Brokerage | Content Expected |
|-----|-----------|-----------------|
| Early career | Century 21 | Listing flyers, early marketing, transaction records |
| Mid-career | Willis Allen | Boutique PV/South Bay materials, client correspondence |
| Luxury tier | Sotheby's International Realty | High-end marketing, luxury property photography |
| Current (~2020+) | Compass / AREA | Everything in `Compass Content - Angelique Lyle/`, current collateral |

### Known Content Locations
- `Angel/Compass Content - Angelique Lyle/` — current AREA/Compass collateral (cataloged)
- `/Volumes/archive/Unsorted/Downloads/` — mixed files from all eras (NAS, uncatalogued)
- Angelique's laptop — raw files, no organization
- Angelique's Dropbox — unknown scope, needs access
- Compass platform — listing presentations, CRM data, marketing materials

## Import Status (Completed 2026-04-13)

### Hot Sheet CSVs → listing_events (Done)
- **Script:** `cove/angel/import_hotsheet.py` + `flask crmls hotsheet`
- **Files:** 5 CSVs, 1,872 rows, 10 event types (Closed, Canceled, Expired, New, Pending, Price Chg, Active UC, Withdrawn, Hold, BoM, Coming Soon)
- **Result:** 31 new events imported, 1,730 already existed (detected during TP import upsert), 12 had no matching listing in DB
- **Columns mapped:** Major Change Timestamp → event_date, Chg Type → event_type, Listing ID → mls_number, L/C Price → new_value, City/Area → old_value

### Lightning v2 Export → listing enrichment (Done)
- **Script:** `cove/angel/import_lightning.py` + `flask crmls lightning`
- **File:** 1 tab-delimited export, 100 listings, 52 columns
- **Result:** 100 existing listings enriched with zip codes, school assignments, longer remarks
- **Fields enriched:** zip_code, elementary_school, middle_school, high_school, showing_instructions (stored in raw_data JSON), remarks (replaced if Lightning version longer), agent name/email (filled if missing)
- **Coverage:** 100 listings now have zip codes, 24 have school assignments

### NAS Archive — Angel-Related Content (Cataloged)
- **Location:** `/Volumes/archive/Unsorted/Downloads/`
- **Content:** 150+ files spanning Angelique's 20-year career across 4 brokerages
- **Transaction files (PV properties):**
  - 2320 Via Pinale (PVE) — offers, inspections, disclosures, repair requests, photos, signed contracts
  - 2321 Via Pinale (PVE) — structural reports, geotechnical reports, city reports, amend purchase price
  - 2391 Vista Valle Verde — disclosures, MLS photos
  - 2482 Via Victoria — repair requests
  - 2525 Via La Selva — offers, counters, disclosures, buyer documents
  - 2833 Via Victoria — repair requests
  - 2842 Via Victoria — mold reports, post-remediation, chimney repair
  - Morro Hills Road — listing contracts
- **Professional photos:** 12+ headshots (Angelique_Lyle-*.jpg series from professional shoot)
- **Marketing:** Testimonial images, P&L report (2016), appraisal appeal forms
- **Brokerage history:** Sotheby's 2015 exclusivity agreement, Century 21 era materials
- **Personal/financial:** Tax documents, refi docs, utility bills (Via Victoria) — DO NOT import these

## Remaining Archive Work (Next Session)

### Phase 1: Remaining Data Files
1. Inspect and import `Full.csv` (170KB — unknown scope, could be a comprehensive listing export)
2. Import `Neighborhood Market Report.csv` → validate against computed `market_snapshots`
3. Import `Agent 1 Line.csv` → future `agents` table (agent roster/contact data)
4. Analyze `Don's 1004MC*.csv` (6 files — FNMA appraisal comparable data)

### Phase 2: Cleanup Duplicates
5. Delete `4. Angelique Lyle-20260413T214528Z-3-001.zip` (608 MB — verified duplicate of Compass Content dir)
6. Delete either `2025/` root or `Print Material/2025/` (duplicated content, keep one)

### Phase 3: NAS Transaction Mining
8. Extract transaction data from NAS Via Pinale/Victoria/La Selva files → match APNs
9. Build transaction history timeline for Angelique's notable sales
10. Extract testimonials from marketing images on NAS

### Phase 4: Content Extraction
11. Extract text from key PDFs → wiki articles (voice training, process playbooks)
12. Extract testimonials from listing presentations → `angel-voice-training.md`

### Phase 5: Archive Organization
13. Move processed files to organized archive structure
14. Delete duplicates (Print Material/2025/ duplicates 2025/ root)
15. Create manifest linking each file to its wiki article or DB record

## Related

- [[Brain/wiki/angel-brand-and-team|Brand & Team]] — Collateral already cataloged
- [[Brain/wiki/angel-data-platform|Angel Data Platform]] — Where data imports go
- [[Brain/wiki/angel-content-engine|Angel Content Engine]] — How content gets produced
- [[Brain/projects/Angel|Angel MOC]] — Project hub
