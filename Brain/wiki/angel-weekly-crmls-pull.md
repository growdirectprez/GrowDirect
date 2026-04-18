---
date: 2026-04-13
type: wiki
status: active
tags: [angel, crmls, data-pipeline, weekly-ops, process]
sources: [listings table analysis, CRMLS Top Producer export interface]
last-compiled: 2026-04-13
---

# Angel Weekly CRMLS Pull — Process Definition

## Purpose

Define exactly what gets pulled from CRMLS each week, how to expand scope, and how to run the import. This is the data heartbeat that feeds market snapshots, content, and eventually the Angel Agent.

## Current State (as of April 13, 2026)

| Metric | Value |
|--------|-------|
| Records in DB | 2,301 |
| Unique MLS numbers | 2,301 |
| Closed transactions | 1,468 |
| Date range | Jul 2023 – Apr 2026 (34 months) |
| Last import batch | `crmls_tp_20260406_211141` (April 6, 2026) |
| Most recent list date | April 6, 2026 |
| Most recent close date | April 3, 2026 |
| Geographic coverage | RPV, PVE, RHE, RH, San Pedro, PV Peninsula (unincorp) |
| MLS areas covered | 18 |

## Weekly Pull Definition

### What to Pull

**Export 1 — Current Activity (weekly, small)**
- **Filter:** Status = Active, Coming Soon, Pending, Active Under Contract
- **Area:** All PV Peninsula cities (RPV, PVE, RH, RHE) + San Pedro South Shores
- **Expected volume:** 50-150 records (well under 500 limit)
- **Purpose:** Track what's on the market right now, new listings, price changes

**Export 2 — Recent Closings (weekly, small)**
- **Filter:** Status = Closed, Close Date = last 30 days
- **Area:** Same as Export 1
- **Expected volume:** 30-70 records
- **Purpose:** Capture transactions as they close, feed market snapshots

**Export 3 — Status Changes (weekly, small)**
- **Filter:** Status = Expired, Canceled, Withdrawn, Hold, modified in last 7 days
- **Area:** Same as Export 1
- **Expected volume:** 10-30 records
- **Purpose:** Track listings that fell through — expired = lead signal

**Total weekly volume:** ~100-250 records. One export may cover all three if Top Producer allows OR/compound filters. Otherwise 2-3 separate exports.

### How to Pull (Top Producer Interface)

1. Log into CRMLS Top Producer
2. Go to Search → Residential
3. Set filters:
   - **City:** Rancho Palos Verdes, Palos Verdes Estates, Rolling Hills, Rolling Hills Estates, San Pedro
   - **Status:** (per export definition above)
   - **Date range:** (per export — e.g., "Close Date: Last 30 days" for closings)
4. Run search
5. Export → CSV (Top Producer format, .tp file)
6. Save to `Angel/Top Producer - Residential-weekly/` (new directory for weekly pulls)
7. Run import: `docker exec cove_flask flask --app cove:create_app crmls import Angel/Top\ Producer\ -\ Residential-weekly/*.tp`
8. Recompute snapshots: `docker exec cove_flask flask --app cove:create_app market snapshot`

### File Naming Convention

`YYYY-MM-DD-weekly-{type}.tp` — e.g., `2026-04-13-weekly-active.tp`, `2026-04-13-weekly-closings.tp`

## Scope Expansion

### Phase 1: Current (PV Peninsula)
Cities: RPV, PVE, RH, RHE, San Pedro
MLS Areas: 18 (160-179 range)

### Phase 2: Beach Cities (next expansion)
Cities to add: Manhattan Beach, Hermosa Beach, Redondo Beach
Zip codes: 90266, 90254, 90277, 90278
Approach: One-time historical bulk export (500 per batch, ~4-6 batches for 3 years), then fold into weekly pull

### Phase 3: Torrance + Inland
Cities to add: Torrance, Lomita, Harbor City
Zip codes: 90501-90505, 90717, 90710
Approach: Same — bulk historical, then weekly

### How to Expand
1. Add new city/zip to the Top Producer search filters
2. Do a one-time bulk export of historical data (all statuses, all dates)
   - Export in 500-record batches (Top Producer limit)
   - Save each batch: `2026-04-XX-bulk-{city}-{batch}.tp`
3. Import all batches: `flask crmls import Angel/Top\ Producer\ -\ Residential-bulk/*.tp`
4. Recompute snapshots: `flask market snapshot`
5. Going forward, include new cities in the weekly pull filters

## Historical Backfill

The current dataset starts July 2023. To go deeper:

**Option A: Top Producer historical export**
- Filter by year ranges (e.g., Closed 2020-2022)
- 500 per batch, probably 3-4 batches per year
- Gets us 5+ years of PV Peninsula history

**Option B: ATTOM API (GRO-459)**
- 10-year sales history per APN
- More complete but needs API key activation
- Fills gaps Top Producer doesn't cover

**Recommended:** Do Option A first (free, uses existing workflow). Option B later for enrichment.

## Import Script Requirements

The import script (`flask crmls import`) needs to:
1. Read one or more .tp CSV files
2. Normalize column names (Top Producer uses mixed case with spaces)
3. Normalize APN format: strip to digits → re-format as `XXXX-XXX-XXX`
4. Parse dates (Top Producer format: `MM/DD/YYYY HH:MM:SS AM`)
5. Parse prices (remove commas, convert to int)
6. Upsert by MLS# (update if exists, insert if new)
7. Store full raw row in `raw_data` JSON column
8. Track batch_id (ISO timestamp + source)
9. Report: inserted N, updated N, errors N

## After Each Weekly Import

1. Run `flask market snapshot` — recomputes monthly snapshots for affected months
2. Run `flask market snapshot --period quarterly` — update quarterly rollups
3. Check `flask market summary` — verify peninsula-wide numbers look right
4. Update any wiki articles where market data shifted significantly (automated freshness detection is future)

## Related

- [[Brain/wiki/angel-data-platform|Angel Data Platform]] — Schema, APN bridge, full data source inventory
- [[Brain/wiki/angel-content-engine|Angel Content Engine]] — Weekly operating rhythm
- [[Brain/wiki/angel-market-intelligence|Angel Market Intelligence]] — What the data tells us
- [[Brain/projects/Angel|Angel MOC]] — Project hub
