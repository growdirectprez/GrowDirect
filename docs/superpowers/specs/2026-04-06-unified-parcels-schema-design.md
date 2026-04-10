# Unified Parcels Schema Design

**Date:** 2026-04-06
**Author:** ALX + Jeffe
**Status:** Approved
**Scope:** Cove database — `parcels`, `listings`, `research_parcels` tables
**ADR:** Approach B — widen `parcels` with real columns + JSONB enrichment

---

## Problem

Parcel data is fragmented across three tables:

1. **`parcels`** (5,514 rows) — LA County GIS, Cove-centric, APN as PK
2. **`research_parcels`** (legacy) — ATTOM enrichment target, overlapping columns with `parcels`
3. **`listings`** (2,301 rows) — CRMLS data with duplicate property fields (address, beds, baths, sqft, lat/lon, year_built)

This fragmentation means:
- ATTOM enrichment writes to a side table instead of the canonical parcel record
- Listing queries duplicate property data instead of joining to a single source
- 1,458 CRMLS APNs have no parcel row at all
- No path to scale to 180K South Bay parcels without creating more subsets

## Solution

One `parcels` table. Every data source enriches it. No subsets.

---

## 1. Parcels Table — Unified Schema

### 1.1 Core Identity (existing)

| Column | Type | Notes |
|--------|------|-------|
| `apn` | String(20) | **PK** — dashed format XXXX-XXX-XXX |
| `address` | String(255) | Street address |
| `street` | String(100) | Street name only |
| `lot_number` | Integer | Nullable |
| `city` | String(100) | Default "Rancho Palos Verdes" removed — no default for South Bay |
| `state` | String(2) | Default "CA" |
| `zip_code` | String(10) | No default — varies across South Bay |

### 1.2 Property Characteristics (new columns from listings)

| Column | Type | Source |
|--------|------|--------|
| `property_type` | String(50) | CRMLS (SFR, Condo/TH, Multi) |
| `bedrooms` | Integer | CRMLS |
| `bathrooms` | Float | CRMLS |
| `sqft` | Integer | CRMLS / ATTOM |
| `architectural_style` | String(255) | CRMLS |

### 1.3 Property Data (existing, widened)

| Column | Type | Source |
|--------|------|--------|
| `lot_size_sqft` | Integer | County GIS / CRMLS |
| `year_built` | Integer | County / ATTOM |
| `owner_name` | String(255) | County / ATTOM |
| `use_description` | String(255) | County / ATTOM |
| `zoning` | String(50) | County |

### 1.4 Location (existing + from listings)

| Column | Type | Source |
|--------|------|--------|
| `geometry` | JSON | County GIS polygon |
| `center_lat` | Float | County GIS / ATTOM |
| `center_lon` | Float | County GIS / ATTOM |
| `mls_area` | String(100) | CRMLS (PVE, RPV, RHE, RH) — **indexed** |
| `subdivision` | String(255) | CRMLS |

### 1.5 Valuation (existing + from ATTOM)

| Column | Type | Source |
|--------|------|--------|
| `assessed_land_value` | Integer | County / ATTOM |
| `assessed_improvement_value` | Integer | County / ATTOM |
| `market_value` | Integer | **New** — ATTOM AVM |
| `last_sale_price` | Integer | County / ATTOM |
| `last_sale_date` | DateTime | Renamed from `transfer_date` |

### 1.6 Enrichment (new)

| Column | Type | Notes |
|--------|------|-------|
| `enrichment` | JSONB | Full ATTOM response blob — deed chains, mortgage history, school assignments, hazard data, building details. Anything too nested for a column. Use `sqlalchemy.dialects.postgresql.JSONB` for indexing and containment operator support. |
| `enrichment_source` | String(100) | Comma-separated sources: `county_gis`, `attom`, `crmls` |
| `enriched_at` | DateTime | Timestamp of last enrichment run |

### 1.7 Legal References (existing)

| Column | Type |
|--------|------|
| `tract_number` | String(20) — indexed |
| `map_book` | String(10) |
| `legal_description` | Text |

### 1.8 Cove-Specific (existing — nullable for non-Cove parcels)

| Column | Type | Notes |
|--------|------|-------|
| `organization_id` | String(36) FK | NULL for non-Cove parcels |
| `is_association_member` | Boolean | Default False — indexed |
| `is_combined` | Boolean | Default False |
| `combined_with_apn` | String(20) FK | Self-referential |
| `lot_h_status` | String(30) | Default "unknown" — indexed |
| `lot_h_on_title` | Boolean | Nullable |

### 1.9 Metadata (existing)

| Column | Type |
|--------|------|
| `notes` | Text |
| `created_at` | DateTime |
| `updated_at` | DateTime |

### 1.10 New Indexes

- `mls_area` — filter by market area
- `city` — South Bay expansion queries
- `zip_code` — geographic filtering
- `property_type` — market stats by type

### 1.11 New Relationships

Existing relationships (member, organization, profile, tag_assignments, comments, contacts) are unchanged.

```python
# On Parcel model (new)
listings: Mapped[list["Listing"]] = relationship(
    "Listing", back_populates="parcel", order_by="Listing.list_date.desc()"
)

# On Listing model (new)
parcel: Mapped["Parcel | None"] = relationship("Parcel", back_populates="listings")
```

---

## 2. Listings Table — Cleaned

`listings` becomes a pure MLS transaction record. Property data comes from `parcels` via JOIN.

### 2.1 Columns Removed

These move to `parcels` (data migrated before columns drop):

- `address`, `city`, `zip_code`
- `property_type`, `bedrooms`, `bathrooms`, `sqft`, `year_built`, `architectural_style`
- `lot_sqft` — maps to `parcels.lot_size_sqft` (different column name)
- `latitude`, `longitude` — map to `parcels.center_lat`, `parcels.center_lon`
- `mls_area`, `subdivision`

### 2.1.1 Listing Model Properties Affected

- `Listing.price_per_sqft` — currently reads `self.sqft`. Must be updated to `self.parcel.sqft` or moved to `Parcel` model.
- `Listing.__repr__` — currently reads `self.address`. Must be updated to use `self.mls_number` and `self.status` (or `self.parcel.address` with null guard).

### 2.1.2 Template / View Impact

Templates and views that render `listing.address`, `listing.city`, `listing.bedrooms`, etc. must be updated to use `listing.parcel.address`, `listing.parcel.city`, etc. Grep for direct attribute access on listing objects in `templates/angel/` and any route that renders listing data.

### 2.2 Columns Retained

| Column | Type | Notes |
|--------|------|-------|
| `id` | String(36) | UUID PK |
| `mls_number` | String(20) | Unique, indexed |
| `apn` | String(20) | **FK to parcels.apn** — was nullable unlinked, now proper FK |
| `status` | String(50) | Active, Closed, Expired, Canceled, Pending, Withdrawn, Hold |
| `list_price` | Integer | |
| `close_price` | Integer | |
| `list_date` | Date | |
| `close_date` | Date | |
| `dom` | Integer | Days on market |
| `cdom` | Integer | Cumulative days on market |
| `listing_agent_name` | String(255) | |
| `listing_agent_email` | String(255) | |
| `listing_office` | String(255) | |
| `buyer_agent_name` | String(255) | |
| `buyer_agent_email` | String(255) | |
| `buyer_office` | String(255) | |
| `hoa_fee` | Integer | |
| `tax_amount` | Integer | |
| `buyer_compensation` | String(100) | |
| `remarks` | Text | Public remarks |
| `virtual_tour_url` | String(500) | |
| `raw_data` | JSON | Full Top Producer row preserved |
| `source` | String(20) | crmls_tp, crmls_api, manual |
| `batch_id` | String(50) | |
| `created_at` | DateTime | |
| `updated_at` | DateTime | |

### 2.3 Query Pattern

```sql
-- "3-bed homes in RPV under $2M, active"
SELECT l.mls_number, l.list_price, l.status, l.dom,
       p.address, p.bedrooms, p.bathrooms, p.sqft, p.mls_area
FROM listings l
JOIN parcels p ON l.apn = p.apn
WHERE p.bedrooms >= 3
  AND p.mls_area = 'RPV'
  AND l.list_price < 2000000
  AND l.status = 'Active';
```

---

## 3. `research_parcels` Elimination

### 3.1 Current State

The `research_parcels` table may still exist in the database, but the model file
(`cove/models/research_parcel.py`) has already been removed from the codebase.
`scripts/enrich_attom.py` still imports `ResearchParcel` (line 29), making it
currently non-functional. The migration must check whether `research_parcels`
exists in the database before attempting data migration or `DROP TABLE`.

### 3.2 Migration Steps

1. Check if `research_parcels` table exists in the database
2. If it exists: copy any data not already in `parcels` into `parcels` rows, transfer Lot H status and ATTOM enrichment data
3. Drop `research_parcels` table (if it exists)

### 3.3 Files Deleted

- `cove/models/research_parcel.py` — model (may already be gone — confirm and delete if present)
- `scripts/seed_research_parcels.py` — seeder
- `scripts/archive_research_parcels.py` — migration helper (job done)

### 3.4 Files Rewritten

- `scripts/enrich_attom.py` — target `Parcel` model, write to `enrichment` JSONB + real columns, update `enrichment_source` and `enriched_at`

---

## 4. Parcel Ingestion — Closing the Gap

### 4.1 CRMLS APNs Without Parcel Rows (1,458 APNs)

The Alembic migration:
1. Queries `SELECT DISTINCT apn FROM listings WHERE apn IS NOT NULL AND apn NOT IN (SELECT apn FROM parcels)`
2. For each, creates a `parcels` row using the most recent listing's property data (address, city, zip, beds, baths, sqft, lat/lon, property_type, mls_area, subdivision)
3. Sets `enrichment_source = 'crmls'`

### 4.2 Future Import Behavior

`import_crmls.py` updated to:
1. Upsert into `parcels` first (create row if APN doesn't exist, update property fields if newer)
2. Then create/upsert the `listings` row (MLS-transaction data only)
3. APN normalization happens once at the parcels level

### 4.3 County GIS Backfill

After migration, run `fetch_gis_parcels.py` against the new APNs to pull geometry and assessed values. This is a data operation, not a schema change.

---

## 5. South Bay Expansion Path

The schema is now source-agnostic. Scaling to 180K parcels is a data ingestion problem:

| Source | Action | Parcels Added |
|--------|--------|---------------|
| LA County GIS bulk pull | Extend `fetch_gis_parcels.py` with South Bay zip/tract filters | ~170K |
| ATTOM bulk enrichment | Same script, bigger target. Subscription tier needed. | 0 (enriches existing) |
| CRMLS API (when activated) | Live listing feed auto-creates parcel rows for new APNs | Incremental |
| Regrid (planned) | Zoning + land use enrichment | 0 (enriches existing) |

No schema changes needed. Just more rows and enrichment passes.

---

## 6. APN Normalization

All sources normalize to dashed format before writing:

| Source | Raw Format | Normalized |
|--------|-----------|------------|
| LA County GIS | 7573-006-008 | 7573-006-008 (already correct) |
| CRMLS Top Producer | 7573006008 | 7573-006-008 |
| ATTOM API | 7573006008 | 7573-006-008 |
| User input | varies | 7573-006-008 |

Single normalization function: `normalize_apn(raw) -> str` — strips non-digits, inserts dashes at positions 4 and 7. Canonical location: `cove/parcels/services.py`. All scripts and models import from there — no duplicate implementations.

---

## 7. Migration Order

Two Alembic migrations for safer rollback. Migration A is additive (no data loss on rollback). Migration B is destructive (point of no return).

### Migration A — Additive (safe to roll back)

1. **Add new columns** to `parcels` (property_type, bedrooms, bathrooms, sqft, architectural_style, mls_area, subdivision, market_value, enrichment JSONB, enrichment_source, enriched_at)
2. **Rename** `transfer_date` to `last_sale_date` on `parcels`
3. **Remove defaults** for `city` and `zip_code` on `parcels`
4. **Add new indexes** (mls_area, city, zip_code, property_type)
5. **Migrate research_parcels** data into `parcels` (check if table exists first)
6. **Migrate listings property data** into `parcels` (most recent listing per APN wins; `listings.lot_sqft` → `parcels.lot_size_sqft`; `listings.latitude` → `parcels.center_lat`; `listings.longitude` → `parcels.center_lon`)
7. **Create parcel rows** for CRMLS APNs not in parcels — populate `address` and `street` (NOT NULL columns) from the most recent listing

### Migration B — Destructive (deploy atomically with model + script changes)

8. **Add FK** `listings.apn -> parcels.apn`
9. **Drop redundant columns** from `listings`
10. **Drop `research_parcels`** table (if it exists)

**Deployment constraint:** Migration B, the updated `Listing` model (without property columns), the updated `import_crmls.py`, and the updated `enrich_attom.py` must ship together in a single deploy. The model changes and migration are not independently deployable.

---

## 8. Affected Code

### Models
- `cove/models/parcel.py` — add new columns, relationships, remove city/zip defaults
- `cove/models/listing.py` — remove property columns, add FK + relationship
- `cove/models/research_parcel.py` — **delete**
- `cove/models/__init__.py` — remove ResearchParcel import

### Scripts
- `scripts/enrich_attom.py` — rewrite to target Parcel, write enrichment JSONB
- `scripts/import_crmls.py` — upsert parcels first, then listings
- `scripts/seed_research_parcels.py` — **delete**
- `scripts/archive_research_parcels.py` — **delete**

### Services / Routes
- Any code importing `ResearchParcel` — update to use `Parcel`
- `cove/map/services.py` — may need updates if it referenced research_parcels
- Angel agent tools (GRO-462) — query `parcels` directly, JOIN to `listings`

### Templates
- `templates/angel/` — any template rendering `listing.address`, `listing.city`, `listing.bedrooms`, etc. must switch to `listing.parcel.address`, `listing.parcel.city`, etc.
- Grep all templates for direct listing property attribute access before migration

### ListingEvent
- `listing_events` table and `ListingEvent` model are NOT modified (FK is on `mls_number`, not on dropped columns)
- Verify the `Listing.events` relationship still works after model changes

### Tests
- Update fixtures that create listings with property fields
- Add tests for parcel upsert from CRMLS import
- Add tests for enrichment JSONB structure
- Remove research_parcel test fixtures

---

## 9. What This Does NOT Cover

- PostGIS migration (geometry stays JSON — separate decision)
- Multi-tenant parcels (organization_id pattern stays as-is)
- String(36) UUID pattern on organization_id and listing.id (historical holdover per Cove CLAUDE.md — not addressed in this migration)
- Compass CRM sync (separate GRO issue)
- TheHillPV.com content generation (separate GRO issue)
