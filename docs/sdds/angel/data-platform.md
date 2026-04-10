# Angel Data Platform

> **Status:** Proposed — design spec, not yet built
> **Namespace:** angel
> **Date:** 2026-04-06
> **Author:** ALX (COO) / Jeffe (CEO)
> **Dependencies:** Cove parcel model, ATTOM MCP, shared PostgreSQL

---

## 1. Overview

Angel's data platform is a property intelligence layer built on top of Cove's
existing parcel model. It ingests MLS listing data from CRMLS, bridges it to
Cove's 5,514 APN-keyed research parcels, and enriches both with ATTOM property
data. The result is a unified dataset covering every residential parcel on the
Palos Verdes peninsula — with county records, MLS history, assessed values,
ownership chains, and market estimates tied to a single key: the APN.

Angel does not maintain its own parcel database. Cove is the source of truth
for parcel geometry, ownership, and county assessor data. Angel extends this
with MLS listing data, pipeline/CRM state, and content generation metadata.

**Scale:**
- 5,514 parcels (Cove research_parcels, LA County GIS)
- 2,368 MLS listings (CRMLS Top Producer exports, July 2023 – April 2026)
- 1,489 closed transactions with prices
- 379 APN overlaps between Cove parcels and CRMLS listings (current)
- Target: 100% APN coverage across both datasets

---

## 2. Data Sources

### Tier 1 — Live and Integrated

| Source | Key | Status | Cost | Refresh |
|--------|-----|--------|------|---------|
| LA County GIS (ArcGIS REST) | APN | LIVE — 5,514 parcels in Cove | Free | On-demand (`pull_county_parcels.py`) |
| CRMLS (Top Producer export) | MLS# + APN | Loaded — 2,368 listings across 6 batches | Member access (Jeffe) | Manual export, target: weekly |

### Tier 2 — Configured, Ready to Activate

| Source | Key | Status | Cost | What It Adds |
|--------|-----|--------|------|-------------|
| ATTOM API | APN (via FIPS+APN) | Script exists (`enrich_attom.py`), needs API key activation | Free trial (1K/day), then subscription | AVM, deed history, ownership chain, mortgage, schools, hazards |
| Apify Zillow Scraper | Address | MCP available | Free tier (limited) | Zestimate, listing status, photos |

### Tier 3 — Planned Integration

| Source | Key | Status | Cost | What It Adds |
|--------|-----|--------|------|-------------|
| First American TitleFlex | APN | Needs account | Subscription | Chain of title — gold standard for deed chain confirmation |
| CRMLS RESO Web API | MLS# / APN | Needs license agreement | Member access | Live listing search, legal descriptions, agent data |
| Regrid Parcel API | APN | REST API | Free starter (25/day) | Zoning, land use, additional parcel attributes |
| ParcelQuest | APN | REST API | Subscription | Deep assessor data, 13M California parcels |

### Tier 4 — Manual / Reference

| Source | What It Gives | Access |
|--------|-------------|--------|
| LA County Assessor Portal | Per-APN detail, ownership history | Free — manual lookup |
| LA County Recorder | Recorded instruments (deeds, declarations) | $1–2/page |
| LA County DPW Tract Maps | Tract boundaries, recording dates | Free |
| CA Coastal Commission | CDP applications, LCP amendments | Free |
| CA DRE | Agent/broker license verification | Free |
| GreatSchools API | School ratings, feeder patterns | Free tier |

---

## 3. APN as Universal Key

Every data source resolves to APN. The APN is the join key across all tables.

```
LA County GIS ──┐
ATTOM API ──────┤
CRMLS Listings ─┤──→ APN ──→ Unified Parcel Record
Title Company ──┤
Cove Parcels ───┘
```

### APN Format Normalization

Different sources format APNs differently:

| Source | Format | Example |
|--------|--------|---------|
| Cove / LA County | Dashed | 7573-006-008 |
| CRMLS | Stripped | 7573006008 |
| ATTOM | Stripped | 7573006008 |

**Rule:** Store with dashes (Cove canonical format). Strip dashes for API lookups.
Normalization function: `normalize_apn(raw) → "XXXX-XXX-XXX"`.

---

## 4. Data Model

Angel tables live in the `cove` database on shared PostgreSQL (Angel is a Cove
module). Angel does NOT duplicate Cove's parcel table — it references APNs and
stores only listing/pipeline data. All Angel tables and migrations are in the
Cove repository.

### 4.1 `listings` Table

The core MLS data table. One row per MLS listing event (a property can have
multiple listings over time).

```python
class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    mls_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    apn: Mapped[str | None] = mapped_column(String(20), index=True)  # dashed format

    # Listing state
    status: Mapped[str]  # Active, Closed, Expired, Canceled, Pending, Withdrawn, Hold
    list_price: Mapped[int | None]
    close_price: Mapped[int | None]
    list_date: Mapped[date | None]
    close_date: Mapped[date | None]
    dom: Mapped[int | None]  # days on market
    cdom: Mapped[int | None]  # cumulative days on market

    # Property
    address: Mapped[str]
    city: Mapped[str]
    zip_code: Mapped[str | None]
    property_type: Mapped[str | None]  # SFR, Condo/TH, etc.
    bedrooms: Mapped[int | None]
    bathrooms: Mapped[float | None]
    sqft: Mapped[int | None]
    lot_sqft: Mapped[int | None]
    year_built: Mapped[int | None]
    architectural_style: Mapped[str | None]

    # Location
    latitude: Mapped[float | None]
    longitude: Mapped[float | None]
    mls_area: Mapped[str | None]  # PVE, RPV, RHE, RH, etc.
    subdivision: Mapped[str | None]

    # Agents
    listing_agent_name: Mapped[str | None]
    listing_agent_email: Mapped[str | None]
    listing_office: Mapped[str | None]
    buyer_agent_name: Mapped[str | None]
    buyer_agent_email: Mapped[str | None]
    buyer_office: Mapped[str | None]

    # Financials
    hoa_fee: Mapped[int | None]
    tax_amount: Mapped[int | None]
    buyer_compensation: Mapped[str | None]

    # Content
    remarks: Mapped[str | None]  # public remarks
    virtual_tour_url: Mapped[str | None]

    # Raw data
    raw_data: Mapped[dict | None] = mapped_column(JSON)  # full Top Producer row

    # Metadata
    source: Mapped[str] = mapped_column(default="crmls_tp")  # crmls_tp, crmls_api, manual
    batch_id: Mapped[str | None]  # which import batch
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
```

### 4.2 `listing_events` Table

Tracks status changes over time (from Agent Hot Sheet data).

```python
class ListingEvent(Base):
    __tablename__ = "listing_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    mls_number: Mapped[str] = mapped_column(ForeignKey("listings.mls_number"), index=True)
    event_type: Mapped[str]  # New, Price Chg, Back on Market, Status Chg, Expired
    event_date: Mapped[datetime]
    old_value: Mapped[str | None]  # e.g., old price
    new_value: Mapped[str | None]  # e.g., new price
    source: Mapped[str] = mapped_column(default="hot_sheet")
    created_at: Mapped[datetime] = mapped_column(default=func.now())
```

### 4.3 `leads` Table

A lead is born when an APN changes status or meets a scoring threshold.

```python
class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    apn: Mapped[str] = mapped_column(String(20), index=True)
    owner_name: Mapped[str | None]
    owner_email: Mapped[str | None]
    owner_phone: Mapped[str | None]

    # Scoring
    score: Mapped[float | None]  # 0-100 likelihood to transact
    score_factors: Mapped[dict | None] = mapped_column(JSON)
    # e.g., {"equity_high": 20, "long_hold": 15, "nearby_sale": 10}

    # Pipeline
    stage: Mapped[str] = mapped_column(default="identified")
    # identified → engaged → captured → contacted → showing → offer → escrow → closed → archived

    # Source
    trigger_event: Mapped[str | None]  # "listing_expired", "price_reduction", "transfer", "equity_signal"
    trigger_mls: Mapped[str | None]  # MLS# that triggered the lead

    # CRM sync
    compass_contact_id: Mapped[str | None]
    compass_synced_at: Mapped[datetime | None]

    # Metadata
    notes: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
```

### 4.4 `market_snapshots` Table

Periodic aggregations for content generation and market reports.

```python
class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    period_start: Mapped[date]
    period_end: Mapped[date]
    area: Mapped[str]  # RPV, PVE, RHE, RH, peninsula-wide
    property_type: Mapped[str]  # SFR, Condo, All

    # Stats
    active_count: Mapped[int]
    closed_count: Mapped[int]
    median_list_price: Mapped[int | None]
    median_close_price: Mapped[int | None]
    median_dom: Mapped[int | None]
    median_ppsf: Mapped[int | None]  # price per square foot
    inventory_months: Mapped[float | None]
    list_to_close_ratio: Mapped[float | None]

    raw_data: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
```

---

## 5. Ingestion Pipeline

### 5.1 CRMLS Top Producer Import

The primary data source. Jeffe (or an automated CRMLS RESO API integration
in Phase 2) exports Top Producer CSVs covering the PV peninsula.

```
CRMLS Export (Top Producer .tp CSV, 214 columns)
    │
    ▼
scripts/import_crmls.py
    ├── Read CSV, normalize column names to snake_case
    ├── Normalize APN: strip dashes from CRMLS format, re-dash to Cove format
    ├── Deduplicate by MLS# (upsert — update if exists)
    ├── Parse dates, prices, coordinates
    ├── Store full raw row in raw_data JSON column
    ├── Write to listings table
    └── Log batch_id, row count, error count

    │
    ▼
scripts/import_hot_sheet.py (separate)
    ├── Read Agent Hot Sheet CSV (19 columns)
    ├── Extract event_type (New, Price Chg, Back on Market)
    ├── Match to listing by MLS#
    └── Write to listing_events table
```

**Batch tracking:** Each import run gets a `batch_id` (ISO timestamp + source).
The `listings.batch_id` column tracks provenance. Duplicate MLS numbers are
updated in place (upsert), not inserted again.

### 5.2 ATTOM Enrichment

Reuses the existing `enrich_attom.py` pattern from Cove's shared infrastructure.
Angel tools read enriched parcel data directly from Cove's research_parcels table
(same database, native JOIN):

```
Cove research_parcels (APN list in cove database)
    │
    ▼
scripts/enrich_attom.py (in Cove/scripts/)
    ├── Property detail (type, year, tract)
    ├── Sale detail (last sale date, amount)
    ├── Assessment detail (market values)
    ├── School detail (district, ratings)
    └── Updates Cove research_parcels

Angel Agent tools join against research_parcels (native queries).
```

### 5.3 Future: CRMLS RESO Web API

When CRMLS API access is established (requires license agreement through
Jeffe's broker access), the import pipeline shifts from manual CSV export
to automated API pulls:

```
CRMLS RESO Web API (OData)
    │  GET /Property?$filter=City eq 'Rancho Palos Verdes'
    │  &$select=ListingId,ListPrice,ClosePrice,...
    ▼
scripts/sync_crmls_api.py (future)
    ├── Incremental sync (ModificationTimestamp > last_sync)
    ├── Full sync (weekly, all statuses)
    └── Write to listings + listing_events
```

---

## 6. APN Overlap Analysis

Current state of the APN bridge between datasets:

```
Cove research_parcels:  5,514 APNs (LA County GIS, polygon geometry)
CRMLS listings:         1,837 unique APNs (across 2,368 listings)
Overlap:                  379 APNs (in both datasets)
Cove-only:              5,135 APNs (no MLS activity in dataset)
CRMLS-only:             1,458 APNs (MLS listings without Cove parcel data)
```

**Gap closure plan:**
1. CRMLS-only APNs → pull county GIS data for these parcels (extend Cove dataset)
2. Cove-only APNs → many are undeveloped lots, HOA common areas, or properties
   that haven't transacted since July 2023. ATTOM enrichment will add historical
   transaction data.
3. Target: 100% of CRMLS APNs matched to Cove parcels within 30 days.

---

## 7. Data Quality Rules

1. **APN normalization** — all APNs stored in dashed format (XXXX-XXX-XXX)
2. **MLS# uniqueness** — one row per MLS number in listings table (upsert)
3. **Price validation** — close_price must be > 0 for Closed status
4. **Date validation** — close_date required for Closed status
5. **Coordinate validation** — lat/lon within PV peninsula bounding box
   (33.7°–33.82° N, 118.28°–118.44° W)
6. **Status normalization** — map all CRMLS status strings to canonical set:
   Active, Pending, Closed, Expired, Canceled, Withdrawn, Hold
7. **Batch tracking** — every import run logged with batch_id, counts, errors

---

## 8. Infrastructure

| Component | Detail |
|-----------|--------|
| Database | `cove` on shared PostgreSQL (`growdirect_postgres:5432`) (Angel tables coexist) |
| Test DB | `cove_test` on same instance |
| Credentials | `growdirect / growdirect_dev` |
| Valkey | DB 1 on `growdirect_valkey:6379` (shared with Cove) |
| Extensions | `vector`, `pgcrypto`, `uuid-ossp` |
| Migrations | Alembic in `Cove/migrations/` (Angel tables in same migration path) |
| Models | Python models in `Cove/cove/models/` (alongside Cove models) |
| Import Scripts | `Cove/scripts/import_crmls.py`, `import_hot_sheet.py`, etc. |

---

*Angel Data Platform SDD — GrowDirect Inc.*
