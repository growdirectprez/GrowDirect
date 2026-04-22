# Angel Data Platform

> **Type:** App Service
> **Status:** Active — CRMLS import pipeline live, market snapshots computed, ATTOM pending
> **Namespace:** angel
> **Date:** 2026-04-06 (ops upgrade 2026-04-13)
> **Author:** ALX (COO) / Jeffe (CEO)
> **Dependencies:** Cove parcel model, shared PostgreSQL, Valkey

**Wiki:** [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] · [[Brain/wiki/angel-data-platform|Angel Data Platform]] · [[Brain/wiki/angel-market-intelligence|Angel Market Intelligence]] · [[Brain/projects/Angel|Angel MOC]]
**Parent:** [[docs/sdds/angel/angel-overview|Angel Overview]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

---

## Purpose

Angel's data platform is a property intelligence layer built on top of Cove's
existing parcel model. It ingests MLS listing data from CRMLS, bridges it to
Cove's 5,514 APN-keyed research parcels, and enriches both with ATTOM property
data. The result is a unified dataset covering every residential parcel on the
Palos Verdes Peninsula.

---

## Dependencies

| Dependency | Type | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | Data store — listings, events, snapshots | Yes |
| Cove `parcels` table | APN-based parcel geometry and county data | Yes (for APN bridge) |
| Cove `research_parcels` table | Extended parcel data from county GIS | Yes (for ATTOM enrichment) |
| CRMLS member access (Jeffe) | Manual CSV exports | Yes (current method) |
| ATTOM API | Property enrichment | No (planned — script ready) |
| CRMLS RESO Web API | Automated listing sync | No (future — requires license) |

---

## Data Flow & PII Map

### What Enters

| Source | Data | PII Content |
|--------|------|------------|
| CRMLS Top Producer CSV (.tp) | 214 columns per listing — prices, dates, agents, property details | Agent names, agent emails |
| CRMLS Agent Hot Sheet CSV | Status change events (New, Price Chg, Back on Market) | None |
| CRMLS Lightning v2 (.txt) | Enriched listing data — zip codes, school assignments, longer remarks | Agent names |
| ATTOM API (planned) | Deed history, AVM, mortgage, schools, hazards | Owner names (from deed records) |

### What's Stored

| Table | Fields with PII | Classification | Current Encryption |
|-------|----------------|---------------|-------------------|
| `listings` | `listing_agent_name` | internal | **Plaintext** |
| `listings` | `listing_agent_email` | **sensitive** | **Plaintext (P0)** |
| `listings` | `buyer_agent_name` | internal | **Plaintext** |
| `listings` | `buyer_agent_email` | **sensitive** | **Plaintext (P0)** |
| `listings` | `listing_office`, `buyer_office` | internal | Plaintext |
| `listings` | `remarks` | public | N/A |
| `listings` | `raw_data` (JSON) | **sensitive** — contains full CSV row with agent PII | **Plaintext (P0)** |
| `listing_events` | None | N/A | N/A |
| `market_snapshots` | None — aggregate stats only | public | N/A |

### What Exits

| Destination | Data | PII Exposed |
|-------------|------|------------|
| Angel web pages (TheHillPV.com) | Aggregate market stats, neighborhood data | None — stats only |
| Angel Agent sidecar | Listing data for chat queries | Agent names visible to chat users (public MLS data) |
| Market snapshot CLI | Computed stats | None |

---

## API Contract

### CLI Commands (Flask CLI)

| Command | Purpose |
|---------|---------|
| `flask crmls import <path>` | Import .tp CSV files into listings table |
| `flask crmls hotsheet <path>` | Import Agent Hot Sheet events |
| `flask crmls lightning <path>` | Import Lightning v2 enrichment data |
| `flask crmls watch` | Scan inbox, import .tp/.zip files, archive originals |
| `flask crmls status` | Show current data inventory counts |
| `flask market snapshot [-p monthly/quarterly/annual]` | Compute market snapshots |
| `flask market trend -a <area>` | Show trend for an area over N months |
| `flask market summary` | Print peninsula-wide market summary |

### Internal Python API

| Function | Module | Purpose |
|----------|--------|---------|
| `import_files(paths)` | `cove.angel.import_crmls` | Import one or more .tp files |
| `watch_inbox()` | `cove.angel.import_crmls` | Scan/import/archive workflow |
| `compute_all_snapshots(period_type)` | `cove.angel.market` | Compute snapshots for all areas |
| `get_trend(area, months)` | `cove.angel.market` | Retrieve N months of snapshots |
| `get_snapshot(area, period_start)` | `cove.angel.market` | Retrieve single snapshot |

---

## Data Sources

### Tier 1 — Live and Integrated

| Source | Key | Status | Cost | Refresh |
|--------|-----|--------|------|---------|
| LA County GIS (ArcGIS REST) | APN | LIVE — 5,514 parcels in Cove | Free | On-demand |
| CRMLS (Top Producer export) | MLS# + APN | Loaded — 2,368 listings across 6 batches | Member access (Jeffe) | Manual export, target: weekly |

### Tier 2 — Configured, Ready to Activate

| Source | Key | Status | Cost |
|--------|-----|--------|------|
| ATTOM API | APN (via FIPS+APN) | Script exists, needs API key activation | Free trial, then subscription |

### Tier 3 — Planned

| Source | Key | Status |
|--------|-----|--------|
| CRMLS RESO Web API | MLS# / APN | Needs license agreement |
| Regrid Parcel API | APN | REST API available |
| GreatSchools API | Address | Free tier |

---

## Data Model

Angel tables live in the `cove` database. Angel does NOT duplicate Cove's parcel
table — it references APNs and stores only listing/pipeline data.

### Tables

| Table | Purpose | Row Count |
|-------|---------|-----------|
| `listings` | One row per MLS listing (upsert by MLS#) | ~2,368 |
| `listing_events` | Status/price change events over time | ~400 |
| `market_snapshots` | Periodic aggregations by area/period | ~1,500 |
| `leads` | Lead pipeline (planned — model not yet created) | 0 |
| `local_entities` | Restaurants, businesses, schools per neighborhood | ~100 |
| `community_events` | RSS-sourced local events | ~50 |
| `local_sources` | RSS feed registry for community crawl | ~10 |

### APN as Universal Key

All data sources resolve to APN. Format: dashed `XXXX-XXX-XXX` (Cove canonical).
Normalization: `_normalize_apn()` strips non-digits, re-formats to dashed.

```
LA County GIS ──┐
ATTOM API ──────┤
CRMLS Listings ─┤──→ APN ──→ Unified Parcel Record
Cove Parcels ───┘
```

### APN Overlap (Current)

| Dataset | Count |
|---------|-------|
| Cove `research_parcels` | 5,514 APNs |
| CRMLS `listings` (unique APNs) | 1,837 |
| Overlap (in both) | 379 |
| Cove-only | 5,135 |
| CRMLS-only | 1,458 |

---

## Ingestion Pipeline

### CRMLS Top Producer Import

```
CRMLS Export (.tp CSV, 214 columns)
    │
    ▼
cove/angel/import_crmls.py
    ├── Read CSV, normalize column names
    ├── Normalize APN (strip dashes → re-dash to Cove format)
    ├── Deduplicate by MLS# (upsert)
    ├── Detect events (status change, price change, new close)
    ├── Store full raw row in raw_data JSON column
    ├── Write to listings + listing_events tables
    └── Log batch_id, row count, error count
```

### CRMLS Watch (Automated Inbox)

```
/data/crmls/inbox/ (mounted Docker volume)
    ├── .zip files extracted → .tp files
    ├── All .tp files imported
    ├── Market snapshots recomputed (monthly + quarterly)
    └── Originals archived to /data/crmls/archive/YYYY-MM/
```

### Market Snapshot Computation

```
listings table
    │
    ▼
cove/angel/market.py
    ├── 25 areas (18 MLS areas + 6 cities + 1 peninsula)
    ├── Monthly, quarterly, annual periods
    ├── SQL aggregation: median prices, DOM, PPSF, inventory months
    ├── YoY comparison against prior snapshots
    └── Upsert to market_snapshots table
```

---

## Data Quality Rules

1. **APN normalization** — all APNs stored in dashed format (XXXX-XXX-XXX)
2. **MLS# uniqueness** — one row per MLS number in listings (upsert)
3. **Price validation** — close_price > 0 for Closed status
4. **Date validation** — close_date required for Closed status
5. **Coordinate validation** — lat/lon within PV peninsula bounding box
6. **Status normalization** — canonical set: Active, Pending, Closed, Expired, Canceled, Withdrawn, Hold
7. **Batch tracking** — every import run logged with batch_id, counts, errors

---

## Operations

### Startup Sequence

No separate startup — data platform code runs inside Cove Flask.
CLI commands invoked via `flask crmls` / `flask market` / `flask crawl`.

### Health Checks

- `flask crmls status` — shows listing counts, batch info, date ranges
- `flask market summary` — verifies snapshot computation pipeline

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| CSV parse error (single row) | Row skipped, `db.session.rollback()`, continues | Check error log, fix CSV if systemic |
| Invalid APN format | APN set to None, listing still imported | Manual APN cleanup pass |
| DB connection during import | Import halts | Restart DB, re-run import |
| Market snapshot SQL error | Snapshot skipped for that area/period | Check raw listing data quality |

### Monitoring

| Metric | Alert Threshold |
|--------|----------------|
| Import error rate | > 5% of rows in a batch |
| Listings with no APN | > 20% of new imports |
| Snapshot computation time | > 5 minutes (currently ~30s) |
| Days since last import | > 14 days |

### Configuration

| Env Var | Purpose | Default |
|---------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection | From Cove .env |
| `ATTOM_API_KEY` | ATTOM enrichment | Not yet configured |
| Inbox path | CRMLS file drop location | `/data/crmls/inbox` |
| Archive path | Processed file archive | `/data/crmls/archive` |

---

## Deployment

### Docker

Data platform code is part of the `cove-flask` container. CRMLS inbox/archive
directories are Docker volume mounts:

```yaml
volumes:
  - ../Angel/Top Producer - Residential-weekly:/data/crmls/inbox
  - ../Angel/Top Producer - Residential-archive:/data/crmls/archive
```

### AWS Target

| Component | AWS Service |
|-----------|------------|
| Import pipeline | ECS Fargate (runs as CLI commands via `flask crmls`) |
| Market computation | ECS Fargate (scheduled task or Lambda trigger) |
| Data storage | RDS PostgreSQL 17 |
| File staging | S3 bucket for CRMLS exports (replaces Docker volume mount) |

### CI/CD

Not yet configured. Import pipeline runs manually via CLI.

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | Agent emails stored plaintext in `listings.listing_agent_email` and `listings.buyer_agent_email` | Field-level AES-256-GCM encryption using Canary's `crypto.py` pattern | — |
| 2 | `raw_data` JSON column preserves full 214-column CSV row including agent names, emails, office affiliations | Scrub PII fields from `raw_data` before storage, or encrypt the blob | — |
| 3 | No authentication or authorization on import CLI — anyone with shell access can import data | Not blocking for dev (CLI requires container access), but add audit logging for all imports | — |

### P1 — Before GA

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | Per-row `db.session.commit()` in import loop — O(N) commits for N rows, no batch atomicity | Batch commits (every 100 rows) with rollback on batch failure | — |
| 2 | No data retention policy — listings accumulate indefinitely | Define retention: listings retained (public data), raw_data purged after 24 months | — |
| 3 | No audit trail for import operations beyond `batch_id` — no record of who ran what, when | Structured audit log per import: operator, file, counts, errors, timestamp | — |
| 4 | APN normalization handles 10-digit and 7-digit APNs but silently passes through other lengths | Add validation warning for non-standard APN lengths | — |
| 5 | `market.py` builds raw SQL with f-string interpolation for `area_filter` — parameterized but area_type is from internal code only, not user input. Still fragile. | Refactor to use SQLAlchemy ORM queries or explicit allow-list for area_type | — |
| 6 | `ListingEvent.id` created as `str(uuid.uuid4())` — not using `Mapped[uuid.UUID]` | Align with platform standard UUID columns | — |

### P2 — Post-Launch

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | `Listing.id` uses `String(36)` for UUID — Cove historical pattern, not platform standard | Migrate to native UUID column type | — |
| 2 | No index on `listings.close_date` — market snapshot queries filter on this heavily | Add index: `ix_listings_close_date` | — |
| 3 | No CRMLS RESO API integration — manual CSV export is current workflow | Build automated sync when license agreement is complete | — |
| 4 | Snapshot computation is synchronous — blocks CLI during computation | Move to background task (Valkey queue or scheduled ECS task) | — |
| 5 | Community crawl (`crawl.py`) uses `feedparser` without timeout — could hang on unresponsive feeds | Add configurable timeout per feed | — |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (agent emails in listings)
- [ ] `raw_data` JSON column scrubbed of PII before storage
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check: `flask crmls status` in monitoring
- [ ] Audit logging for all import operations
- [ ] Data retention policy implemented (raw_data TTL)
- [ ] Rate limiting: N/A (CLI-only, no public endpoints)
- [ ] Error responses: N/A (CLI output, not HTTP)
- [ ] Batch import atomicity (commit every N rows, rollback on failure)
- [ ] APN normalization validation tightened
- [ ] Close date index added for snapshot query performance

---

*Angel Data Platform SDD — GrowDirect Inc.*
