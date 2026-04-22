---
date: 2026-04-13
type: wiki
status: active
tags: [angel, data-platform, crmls, apn, listings, parcels, ingestion]
sources: [docs/sdds/angel/data-platform.md, Cove/cove/models/listing.py, Cove/scripts/import_crmls.py, Angel/knowledge/south-bay-dataset.md]
last-compiled: 2026-04-13
needs-review: 2026-04-27
---

# Angel Data Platform

## Summary

Angel's data platform is a property intelligence layer built on top of Cove's parcel model. It ingests MLS listing data from CRMLS, bridges it to Cove's APN-keyed `parcels` table, and will enrich both with ATTOM property data. The result: a unified dataset covering residential parcels on the Palos Verdes peninsula with county records, MLS history, and market estimates tied to a single key — the APN.

Angel does not maintain its own database. It extends Cove's `cove` PostgreSQL database with additional tables for listings, leads, market snapshots, and community intelligence.

## V1 Scope (What We're Building Now)

**In the database:** MLS listings from CRMLS Top Producer exports, parcels in the unified `parcels` table (WPBCA lots + surrounding area), market snapshots (monthly/quarterly/annual aggregations), RSS-crawled community events, and manually seeded local entities.

**Not in the database yet:** Lead records, ATTOM enrichment, ownership chains, deed history.

**The weekly rhythm:** CRMLS exports arrive as static CSV snapshots. Each week's data is fact — it doesn't change. We absorb it into the growing historical record. Over time, this becomes the most complete transaction history for the PV peninsula that any single agent has access to.

## Data Sources

### Tier 1 — Live and Integrated

| Source | Key | Table | Status |
|--------|-----|-------|--------|
| LA County GIS (ArcGIS REST) | APN | `parcels` | ✅ Live |
| CRMLS Top Producer exports | MLS# + APN | `listings` | ✅ Loaded (GRO-457) |
| RSS feeds (8 South Bay sources) | URL hash | `community_events` | ✅ Crawling daily |
| Manual seed data | Name + neighborhood | `local_entities` | ✅ Seeded |

### Tier 2 — Ready to Activate

| Source | Key | What It Adds | Status |
|--------|-----|-------------|--------|
| ATTOM API | APN (via FIPS+APN) | AVM, deed history, ownership, mortgage, schools, hazards | Script exists, needs API key (GRO-459) |
| Firecrawl MCP | URL | Deep web scraping — Yelp, school sites, city calendars | ✅ Used 2026-04-13: 19 neighborhood content pools crawled into Brain wiki |

### Tier 3 — Planned

| Source | What It Adds | Status |
|--------|-------------|--------|
| CRMLS RESO Web API | Live listing search, legal descriptions, agent data | Needs license agreement through broker |
| GreatSchools API | School ratings, feeder patterns (currently manual) | Free tier available |
| US Census ACS | Demographics, income by tract (GRO-478) | Backlog |
| CA DRE Licensee File | Agent license verification | Free download |

### Tier 4 — Manual / Reference

LA County Assessor Portal (per-APN detail), LA County Recorder (deeds, $1-2/page), Redfin Data Center (migration patterns, free CSV), Google Keyword Planner (SEO volume).

## APN as Universal Key

Every data source resolves to APN. The APN links Angel to Cove's data model and to county records, MLS listings, and grant deeds.

```
LA County GIS ──┐
ATTOM API ──────┤
CRMLS Listings ─┤──→ APN ──→ Unified Parcel Record
Title Company ──┤
Cove Parcels ───┘
```

### APN Format Normalization

| Source | Format | Example |
|--------|--------|---------|
| Cove / LA County | Dashed | 7573-006-008 |
| CRMLS | Stripped | 7573006008 |
| ATTOM | Stripped | 7573006008 |

**Rule:** Store with dashes (Cove canonical format). Strip dashes for API lookups.

### APN Bridge

The `parcels` and `listings` tables overlap on APN but neither fully covers the other. Many CRMLS listings reference APNs that don't have a `parcels` row yet. Many parcels (undeveloped, HOA common areas) have no MLS activity.

**Known gaps:**
- CRMLS-only APNs need backfill into `parcels` (from CRMLS data or county GIS re-pull)
- The original full-peninsula LA County GIS pull (`research_parcels`, ~5,500 parcels) was lost during schema consolidation — that data needs to be re-pulled to close coverage gaps
- ATTOM enrichment would add historical transactions for parcels without MLS activity

Query the DB for current overlap stats — don't trust static counts in this wiki.

## CRMLS Data Inventory

### The 6 Exports

Top Producer CSV exports in `Angel/Top Producer - Residential*/`, 214 columns each:

| Export | Cities | Statuses | Dates |
|--------|--------|----------|-------|
| Residential | PVE, RPV, RH, RHE | Active, Coming Soon | Current |
| Residential-2 | RPV, RH, RHE, PV Peninsula | Closed | Jan 2024 – Dec 2025 |
| Residential-3 | RPV, RHE, San Pedro | Closed | Jan 2025 – Dec 2025 |
| Residential-4 | All PV + San Pedro | Closed, Canceled, Expired | 2023–2024 |
| Residential-5 | All PV + San Pedro | Canceled, Hold, Withdrawn | 2024 |
| Residential-6 | All PV + San Pedro | Active, Pending, Closed | 2024–2025 |

### Key Fields (Available)

| Field | Column Name | Coverage | Use |
|-------|-------------|----------|-----|
| APN | `Parcel Number` | Most records | Universal key |
| Address | `Street Number` + `Street Name` | All | Display, geocoding |
| City | `City` | All | Geography |
| Status | `Standard Status` | All | Active/Closed/Expired/etc. |
| List Price | `List Price` | All | Pricing analysis |
| Close Price | `Close Price` | Closed only | Transaction value |
| List Date | `Listing Contract Date` | All | Time on market |
| Close Date | `Close Date` | Closed only | Transaction timing |
| Beds/Baths | `Bedrooms Total` / `Bathrooms Total Integer` | Most | Property profile |
| Sqft | `Living Area` | Most | Price-per-sqft |
| Year Built | `Year Built` | Most | Property age |
| Sub Type | `Property Sub Type` | Most | SFR, Condo, etc. |
| Office | `List Office Name` / `Buyer Office Name` | Most | Agent/office analysis |
| Remarks | `Public Remarks` | Most | Content, descriptions |
| HOA Fee | `Association Fee` | Where applicable | Cost analysis |
| Style | `Architectural Style` | Some | Neighborhood character |

### Sparse/Missing Fields

| Field | Issue | Workaround |
|-------|-------|------------|
| Agent names | `List Agent Full Name` MISSING in most exports | Use office names; ATTOM or RESO API for agent data |
| Zip codes | `Postal Code` MISSING in some exports | Derive from city + address geocoding |
| School assignments | Elementary/Middle/High School fields empty | GreatSchools API + PVPUSD boundary lookup |
| Property Type | `Property Type` MISSING | `Property Sub Type` has "Single Family Residence" etc. |
| DOM | `Days On Market` MISSING | Calculate from list date to close date |
| Lot Size | `Lot Size Sq Ft` MISSING in some | ATTOM enrichment or county assessor |

## Database Schema

### Implemented Tables

**`listings`** — One row per MLS listing event. A property can have multiple listings over time.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| mls_number | String(20), unique, indexed | Primary lookup key |
| apn | String(20), indexed | Dashed format, nullable |
| status | String | Active, Closed, Expired, Canceled, Pending, Withdrawn, Hold |
| list_price / close_price | Integer | |
| list_date / close_date | Date | |
| dom / cdom | Integer | Days on market / cumulative |
| address, city, zip_code | String | |
| property_type, bedrooms, bathrooms, sqft, lot_sqft, year_built | Mixed | |
| latitude, longitude | Float | |
| mls_area, subdivision, architectural_style | String | |
| listing_agent_name/email, listing_office | String | Sparse |
| buyer_agent_name/email, buyer_office | String | Sparse |
| hoa_fee, tax_amount, buyer_compensation | Mixed | |
| remarks, virtual_tour_url | Text | |
| raw_data | JSON | Full Top Producer row preserved |
| source | String | `crmls_tp`, `crmls_api`, `manual` |
| batch_id | String | ISO timestamp + source |

**`listing_events`** — Status changes over time (from Agent Hot Sheet data).

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| mls_number | FK → listings | |
| event_type | String | New, Price Chg, Back on Market, Status Chg, Expired |
| event_date | Datetime | |
| old_value / new_value | String | e.g., old/new price |

**`local_sources`** — RSS feed registry.
**`community_events`** — Crawled + seeded events with neighborhood taxonomy.
**`local_entities`** — Restaurants, schools, businesses, parks with lat/lng.

### Built (2026-04-13)

**`market_snapshots`** — Periodic aggregations per area (monthly, quarterly, annual) across MLS areas, cities, and peninsula-wide. Stats: active_count, closed_count, median prices, median DOM, ppsf, inventory months, list-to-close ratio, YoY comparisons. CLI: `flask market snapshot/trend/summary`. Service: `cove/angel/market.py`. Model: `cove/models/market_snapshot.py`.

### Designed But Not Built

**`leads`** — APN-based lead records. Born when an APN changes status or meets a scoring threshold. Pipeline: identified → engaged → captured → contacted → showing → offer → escrow → closed → archived. Includes score, score_factors (JSON), trigger_event, compass_contact_id.

## Ingestion Pipeline

### CRMLS Top Producer Import (Live)

```
CRMLS Export (.tp CSV, 214 columns)
    → scripts/import_crmls.py
        ├── Read CSV, normalize column names
        ├── Normalize APN: strip dashes → re-dash to Cove format
        ├── Deduplicate by MLS# (upsert)
        ├── Parse dates, prices, coordinates
        ├── Store full raw row in raw_data JSON column
        ├── Write to listings table
        └── Log batch_id, row count, errors
```

Batch tracking: each import run gets `batch_id` (ISO timestamp + source). Duplicate MLS numbers are updated in place (upsert).

### RSS Crawl Pipeline (Live)

```
8 Tier 1 RSS sources (Easy Reader, Patch×5, Daily Breeze, LAist)
    → flask crawl run (CLI, daily)
        ├── feedparser reads each feed
        ├── SHA-256 hash dedup (guid or link)
        ├── Keyword classification → neighborhood + category
        └── Write to community_events table
```

Neighborhood keywords: lunada_bay, malaga_cove, valmonte, miraleste, rancho_palos_verdes, rolling_hills, rolling_hills_estates.
Category keywords: nature, dining, schools, arts, events, community.

### ATTOM Enrichment (Ready, Not Active)

Script exists at `Cove/scripts/enrich_attom.py`. Adds: AVM, deed history (last sale date + amount), assessment (market values), school assignments. Needs API key activation (GRO-459). Free trial: 1,000 calls/day for 30 days.

### Future: CRMLS RESO Web API

When API access is established (license agreement through broker): incremental sync via `ModificationTimestamp > last_sync`, full weekly sync, live listing search. Replaces manual CSV export workflow.

## Data Quality Rules

1. **APN normalization** — all APNs stored as `XXXX-XXX-XXX`
2. **MLS# uniqueness** — one row per MLS number (upsert, not duplicate)
3. **Price validation** — close_price > 0 for Closed status
4. **Date validation** — close_date required for Closed status
5. **Coordinate validation** — lat/lon within PV bounding box (33.7°–33.82° N, 118.28°–118.44° W)
6. **Status normalization** — canonical set: Active, Pending, Closed, Expired, Canceled, Withdrawn, Hold
7. **Batch tracking** — every import logged with batch_id, counts, errors

## What the Data Enables

**For the wiki (now):** Market intelligence articles, neighborhood price trends, area comparisons, seasonal patterns, inventory analysis. Each weekly import makes the historical record deeper.

**For TheHillPV.com (next):** Auto-generated market reports (60+/year × 5 areas), neighborhood pages with live pricing, street-level transaction histories, data-backed content that no competitor can replicate.

**For Angel Agent (next):** Parcel lookup, listing search, market stats, CMA summaries — all backed by real data, not IDX feed.

**For lead generation (future):** Propensity-to-sell scoring (ownership duration, equity, permit activity, neighborhood trends), listing event signals (price reductions, expirations, back-on-market), sphere-of-influence mining from transaction history.

## Related

- [[Brain/wiki/angel-architecture|Angel Architecture]] — System design, 5 layers, infrastructure
- [[Brain/wiki/angel-content-engine|Angel Content Engine]] — How data becomes content
- [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] — Content geography and voice
- [[Brain/projects/Angel|Angel MOC]] — Project hub with Linear issues
