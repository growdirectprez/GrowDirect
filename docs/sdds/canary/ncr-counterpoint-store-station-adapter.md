---
id: sdd-cp-store-station
title: NCR Counterpoint — Store & Station Adapter (Module N)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/ncr-counterpoint-tsp-adapter.md
  - docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring.md
  - Canary/docs/sdds/v2/identity.md
source-endpoints:
  - GET /Store/{StoreID} (per-store sync)
  - GET /Store/{StoreID}/Station/{StationID} (per-station sync)
  - GET /Device/Config (device config, Phase 2+)
  - GET /Workgroup (Phase 2+)
source-tables: PS_STR, PS_STR_CFG_PS, PS_STA, PS_STA_CFG_PS
target-tables:
  - app.locations (existing — external_identities bridge)
  - app.cp_store_config (new)
  - app.cp_station_config (new)
  - app.external_identities (existing — entity_type='location', 'device')
  - app.poll_watermarks (existing — entity_type='store', 'station')
resolves-open-question: R-OQ-02 (anonymous customer sentinel per store)
---

# NCR Counterpoint — Store & Station Adapter (Module N)

## 1. Purpose and scope

This SDD specifies how Canary syncs Counterpoint store and station
configuration into Canary's location registry and a new store-config
attribute table.

Store and station data serve three purposes in Canary:

1. **Location identity:** Counterpoint `STR_ID` maps to Canary's
   `app.locations` via `external_identities`. Transaction records reference
   `store_id` (Canary UUID); the bridge resolves Counterpoint's
   string STR_ID at ingest time.

2. **Anonymous customer resolution:** `PS_STR_CFG_PS.WALK_IN_CUST_NO`
   is the per-store sentinel for anonymous (cash/walk-in) transactions.
   This resolves open question R-OQ-02 from the customer adapter SDD.
   Different stores can have different walk-in sentinels.

3. **Module Q substrates:** `PS_STR_CFG_PS` carries the store-level LP
   configuration that multiple Chirp rules depend on — `MAX_DISC_AMT`,
   `MAX_DISC_PCT` (for C-1001), `USE_VOID_COMP_REAS` (for C-1101),
   `ALLOW_DRW_REACTIV` (for C-1303), and the store-level `MIN_PFT_PCT`
   override (for C-1501 when set).

**Not covered here:** device-level configuration (`GET /Device/Config`),
workgroup management (`GET /Workgroup`), tokenization config
(`GET /StoreTokenizeInfo`) — all Phase 2+.

## 2. Architecture overview

```
Counterpoint REST API
  GET /Store/{STR_ID}                    -- per-store detail + PS_STR_CFG_PS
  GET /Store/{STR_ID}/Station/{STA_ID}  -- per-station detail + PS_STA_CFG_PS
           │
           ▼
  CounterpointStorePoller
  (POSAdapter subclass — poll_intervals: store=86400s, station=86400s)
           │
           ├── Emits CanonicalEvent(event_type="store.upserted")
           ├── Emits CanonicalEvent(event_type="station.upserted")
           │
           ▼
  canary:events stream → Sub2
           │
           ├── app.locations         (external_identities bridge, additive)
           ├── app.cp_store_config   (LP config substrates, per-store)
           ├── app.cp_station_config (station-level tender defaults)
           └── app.external_identities (STR_ID → location UUID)
```

**Discovery model:** There is no `GET /Stores` list endpoint (only
`GET /Store/{StoreID}` single-record fetch). Store IDs must be discovered
at onboarding time — provided by the operator or enumerated from Document
records (Documents carry `STR_ID`). The adapter accumulates known STR_IDs
into a `app.cp_known_store_ids` table; new STR_IDs seen in Documents
trigger on-demand store fetches (same cache-miss pattern as items).

## 3. Polling strategy

| Property | Value |
|---|---|
| Endpoint | `GET /Store/{STR_ID}` per known store |
| Watermark | None — re-sync all known stores daily |
| Poll interval | 86400s (daily) |
| Discovery | STR_IDs seeded at onboarding via operator input; new ones discovered from Document `STR_ID` fields via cache-miss fetch |
| Station discovery | After a store sync, fetch station list via Document `STA_ID` values seen in that store. No `GET /Stations` bulk endpoint. |
| `poll_watermarks` key | `(merchant_id, 'counterpoint', company_alias, 'store')` |
| Cache flush | Send `ServerCache: no-cache` on store syncs — Store data is server-cached 24h |
| Error handling | Exponential backoff. Per-store failures don't block other stores. |

### Store ID seed at onboarding

During merchant activation, the operator enters store IDs (e.g., `["MAIN", "EAST", "WEST"]`). These seed `app.cp_known_store_ids`. At runtime, any Document with an unknown `STR_ID` triggers an on-demand `GET /Store/{STR_ID}` fetch and registration.

```sql
CREATE TABLE app.cp_known_store_ids (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES app.merchants(id),
    str_id      TEXT NOT NULL,
    discovered_from TEXT,   -- 'onboarding' | 'document_cache_miss' | 'manual'
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (merchant_id, str_id)
);
```

## 4. PII handling

`PS_STR` contains store address and contact information. Unlike customer
records, store address IS stored — it is operational data, not personal
data. The store is a business location, not an individual.

**Strip:** Contact names and email addresses that identify specific
individuals (`CONTCT_1`, `CONTCT_2`, `EMAIL_ADRS_1`, `EMAIL_ADRS_2`,
`FAX_1`, `FAX_2`). These are site-contact details, not business-critical.

**Retain:** `ADRS_1`, `ADRS_2`, `CITY`, `STATE`, `ZIP_COD`, `CNTRY`,
`PHONE_1` — needed for business-hours timezone inference and multi-store
geo context.

Store address data maps to the existing `app.locations` address columns
(which already store Square location addresses). No privacy concern.

## 5. Field mapping — app.locations (bridge only)

`app.locations` is not extended with Counterpoint-specific fields. It
serves only as the identity anchor: one row per Counterpoint store, with
the standard location fields populated from PS_STR.

The existing `square_location_id` column has the same multi-POS problem
as `app.customers.square_customer_id` — it is NOT NULL and Square-specific.
The same Phase 0b Alembic migration makes it nullable.

| app.locations column | Source | Notes |
|---|---|---|
| `id` | Generated | UUID on first upsert |
| `merchant_id` | Context | From poll context |
| `location_name` | `PS_STR.DESCR` | Store display name |
| `timezone` | Derived | From `PS_STR.STATE` + IANA timezone DB lookup (see §8) |
| `address_line1` | `PS_STR.ADRS_1` | |
| `address_line2` | `PS_STR.ADRS_2` | |
| `city` | `PS_STR.CITY` | |
| `state` | `PS_STR.STATE` | |
| `postal_code` | `PS_STR.ZIP_COD` | |
| `country` | `PS_STR.CNTRY` | |
| `business_hours` | NULL initially | Counterpoint does not carry business hours. Operator enters hours in Canary onboarding UI. |
| `square_location_id` | NULL | After nullable migration |

## 6. New table — app.cp_store_config

Counterpoint-specific store configuration, with emphasis on Module Q substrates.

### DDL

```sql
CREATE TABLE app.cp_store_config (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id             UUID NOT NULL REFERENCES app.merchants(id),
    str_id                  TEXT NOT NULL,
    location_id             UUID REFERENCES app.locations(id),

    -- Anonymous customer sentinel (resolves R-OQ-02)
    walk_in_cust_no         TEXT,   -- WALK_IN_CUST_NO; default "CASH"

    -- Module Q substrates: discount caps
    max_disc_amt            NUMERIC(12, 2),  -- MAX_DISC_AMT; C-1001 threshold
    max_disc_pct            NUMERIC(5, 2),   -- MAX_DISC_PCT; C-1001 threshold
    min_pft_pct             NUMERIC(5, 2),   -- MIN_PFT_PCT (store override)
    min_pft_pct_meth        TEXT,            -- '!' = use category; 'S' = store override

    -- Module Q substrates: workflow control flags
    use_void_comp_reas      BOOLEAN,   -- USE_VOID_COMP_REAS; C-1101 context
    use_ret_reas            BOOLEAN,   -- USE_RET_REAS; return reason required
    use_prc_chng_reas       BOOLEAN,   -- USE_PRC_CHNG_REAS; price-change reason required
    allow_drw_reactiv       BOOLEAN,   -- ALLOW_DRW_REACTIV; C-1303 context
    auto_drw_activ          BOOLEAN,   -- AUTO_DRW_ACTIV; drawer lifecycle
    auto_drw_cnt            BOOLEAN,   -- AUTO_DRW_CNT
    auto_drw_recon          BOOLEAN,   -- AUTO_DRW_RECON; reconciliation automated
    login_per_tkt           BOOLEAN,   -- LOGIN_PER_TKT; per-ticket re-auth requirement
    retain_cr_card_no_hist  BOOLEAN,   -- RETAIN_CR_CARD_NO_HIST; card retention flag

    -- Operational context
    industry_typ            TEXT,      -- R=retail, G=grocery, H=hospitality
    edc_processor           TEXT,      -- payment processor code
    stk_loc_id              TEXT,      -- default stock location
    prc_loc_id              TEXT,      -- default price location
    tkt_no_meth             TEXT,      -- ticket numbering method (S=sequential)
    ar_tax_cod              TEXT,      -- default AR tax code

    -- Drawer assignment
    assgn_drws_by           TEXT,      -- S=station, U=user
    drw_dflt_meth           TEXT,      -- U=user, S=station

    -- Source metadata
    str_no                  INTEGER,   -- PS_STR.STR_NO (numeric ID)
    use_ps                  BOOLEAN,   -- Point-of-Sale enabled
    lst_maint_dt            TIMESTAMPTZ,
    lst_maint_usr_id        TEXT,
    rs_utc_dt               TIMESTAMPTZ NOT NULL,
    rs_stat                 INTEGER,

    -- Canary metadata
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (merchant_id, str_id)
);

CREATE INDEX idx_cp_store_config_merchant_location
    ON app.cp_store_config (merchant_id, location_id);
```

## 7. New table — app.cp_station_config

Station (register) configuration. One row per (merchant, store, station).

```sql
CREATE TABLE app.cp_station_config (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL REFERENCES app.merchants(id),
    str_id      TEXT NOT NULL,
    sta_id      TEXT NOT NULL,
    descr       TEXT,
    sta_no      INTEGER,

    -- Tender defaults (context for tender-mix rules)
    dflt_tnd_pay_cod    TEXT,   -- default tender pay code (CASH, VISA, etc.)
    dflt_chng_pay_cod   TEXT,   -- change tender
    dflt_rfnd_pay_cod   TEXT,   -- default refund tender

    -- Station behavior
    use_consol_lins     BOOLEAN, -- consolidated line items
    offline_nxt_tkt_no  TEXT,    -- offline ticket prefix (identifies offline transactions)

    -- Source metadata
    lst_maint_dt        TIMESTAMPTZ,
    rs_utc_dt           TIMESTAMPTZ,
    rs_stat             INTEGER,

    -- Canary metadata
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (merchant_id, str_id, sta_id)
);
```

## 8. Timezone resolution

Counterpoint does not store timezone in `PS_STR`. Canary needs store
timezone for:
- After-hours transaction detection (C-004, C-1302, C-2105)
- Day boundary determination in batch rule windows
- Business-hours enforcement (Q-M-05)

**Strategy:** Derive timezone from `STATE` field using a US state → IANA
timezone lookup table. For multi-timezone states (e.g., Indiana, Texas,
Kentucky), default to the major metropolitan timezone and flag for
operator confirmation during onboarding.

```python
STATE_TIMEZONE_DEFAULTS = {
    "AL": "America/Chicago",    "AK": "America/Anchorage",
    "AZ": "America/Phoenix",    "AR": "America/Chicago",
    "CA": "America/Los_Angeles", "CO": "America/Denver",
    "CT": "America/New_York",   "DE": "America/New_York",
    "FL": "America/New_York",   "GA": "America/New_York",
    "HI": "Pacific/Honolulu",   "ID": "America/Denver",
    "IL": "America/Chicago",    "IN": "America/Indiana/Indianapolis",
    "IA": "America/Chicago",    "KS": "America/Chicago",
    "KY": "America/New_York",   "LA": "America/Chicago",
    "ME": "America/New_York",   "MD": "America/New_York",
    "MA": "America/New_York",   "MI": "America/Detroit",
    "MN": "America/Chicago",    "MS": "America/Chicago",
    "MO": "America/Chicago",    "MT": "America/Denver",
    "NE": "America/Chicago",    "NV": "America/Los_Angeles",
    "NH": "America/New_York",   "NJ": "America/New_York",
    "NM": "America/Denver",     "NY": "America/New_York",
    "NC": "America/New_York",   "ND": "America/Chicago",
    "OH": "America/New_York",   "OK": "America/Chicago",
    "OR": "America/Los_Angeles", "PA": "America/New_York",
    "RI": "America/New_York",   "SC": "America/New_York",
    "SD": "America/Chicago",    "TN": "America/Chicago",
    "TX": "America/Chicago",    "UT": "America/Denver",
    "VT": "America/New_York",   "VA": "America/New_York",
    "WA": "America/Los_Angeles", "WV": "America/New_York",
    "WI": "America/Chicago",    "WY": "America/Denver",
}
```

International locations (`CNTRY != "USA"`) require operator-entered timezone.
Flag these during onboarding.

## 9. external_identities bridge

Each Counterpoint store gets an `external_identities` row:

| Column | Value |
|---|---|
| `entity_type` | `'location'` |
| `entity_id` | Canary location UUID (`app.locations.id`) |
| `source_code` | `'counterpoint'` |
| `external_id` | `PS_STR.STR_ID` (string, e.g. `"MAIN"`) |
| `is_primary` | `True` |

**Forward resolution** (STR_ID from Document → Canary location UUID):

```python
def resolve_store(db, merchant_id: UUID, str_id: str) -> Optional[UUID]:
    row = db.query(ExternalIdentity).filter_by(
        merchant_id=str(merchant_id),
        source_code="counterpoint",
        entity_type="location",
        external_id=str_id,
    ).first()
    return UUID(row.entity_id) if row else None
```

Cache-miss: if `str_id` is unknown, queue on-demand `GET /Store/{str_id}`,
register, return UUID. Same pattern as item cache-miss in §3 of the item
catalog SDD.

Stations do NOT get `external_identities` rows — stations are sub-entities
of stores and are referenced via `(str_id, sta_id)` composite key directly
in `cp_station_config`. Station IDs are not globally unique across stores.

## 10. Anonymous customer sentinel resolution

This resolves **R-OQ-02** from the customer adapter SDD.

`PS_STR_CFG_PS.WALK_IN_CUST_NO` is the per-store anonymous customer
sentinel. In the TSP adapter's `parse_cp_transaction()`, the customer
resolution logic is:

```python
def resolve_transaction_customer(
    db,
    merchant_id: UUID,
    str_id: str,
    cust_no: Optional[str],
) -> Optional[UUID]:
    """Resolve CUST_NO to Canary UUID. Returns None for anonymous transactions."""
    if not cust_no:
        return None

    # Get the per-store walk-in sentinel
    store_cfg = db.query(CpStoreConfig).filter_by(
        merchant_id=str(merchant_id), str_id=str_id
    ).first()
    walk_in_sentinel = store_cfg.walk_in_cust_no if store_cfg else "CASH"

    if cust_no == walk_in_sentinel:
        return None  # anonymous transaction

    # Look up in external_identities
    return resolve_customer(db, merchant_id, cust_no)
```

The sentinel lookup requires `cp_store_config` to be populated BEFORE
Document sync begins. Store sync must run as part of tenant activation,
before the first Document poll. The activation ordering is:

```
1. Credential validation (GET /Company)
2. Store sync (GET /Store/{id} for each known store)  ← populates WALK_IN_CUST_NO
3. CustomerControl sync
4. ItemCategories sync
5. Customer initial load
6. Item catalog initial load
7. Document initial load (watermark = epoch - 90 days or configurable lookback)
```

## 11. Module Q wiring — store-config substrates

### C-1001 DISCOUNT_CAP_EXCEEDED

The rule's `MAX_DISC_AMT` / `MAX_DISC_PCT` thresholds are no longer
hardcoded in `merchant_rule_configs`. They are read from `cp_store_config`
at evaluation time:

```python
def evaluate_c1001(transaction, db):
    store_cfg = db.query(CpStoreConfig).filter_by(
        merchant_id=transaction.merchant_id,
        str_id=transaction.store_id_raw,  # STR_ID string
    ).first()
    max_disc_pct = store_cfg.max_disc_pct if store_cfg else 50.0
    max_disc_amt = store_cfg.max_disc_amt if store_cfg else 200.0
    # ... evaluate per-line discount against thresholds
```

The per-store thresholds override any `merchant_rule_configs.default_threshold`
for this rule. If a merchant has stores with different discount limits
(common in multi-store chains: flagship vs satellite), each store fires
at its own configured limit.

### C-1101 VOID_WITHOUT_ORIGINAL

`USE_VOID_COMP_REAS = True` means the store requires a void-compensation
reason code. When this flag is set, the rule can distinguish between
structured voids (reason recorded → lower risk) and unstructured voids
(no reason → higher risk). The severity modifier:

- `USE_VOID_COMP_REAS = True` + void has reason code → `severity = low`
- `USE_VOID_COMP_REAS = True` + void missing reason code → `severity = high`
- `USE_VOID_COMP_REAS = False` → no reason required; void-without-reason
  is expected — `severity = medium` regardless

### C-1303 DRAWER_REACTIVATION_PATTERN

`ALLOW_DRW_REACTIV = True` means reactivations are permitted. The rule
fires only if `ALLOW_DRW_REACTIV = True` AND reactivation count exceeds
threshold. If `ALLOW_DRW_REACTIV = False`, any reactivation is a
configuration violation, not just a pattern — fire at `severity = critical`.

### After-hours rules (C-004, C-1302)

`app.locations.business_hours` (operator-entered during onboarding) is
the hours reference. The store's `timezone` (derived from STATE per §8)
normalizes transaction timestamps for comparison:

```python
from zoneinfo import ZoneInfo
from datetime import datetime

def is_after_hours(occurred_at_utc: datetime, location: Location) -> bool:
    tz = ZoneInfo(location.timezone)
    local_dt = occurred_at_utc.astimezone(tz)
    hours = json.loads(location.business_hours or "[]")
    day_name = local_dt.strftime("%A").upper()  # MONDAY, TUESDAY...
    store_hours = next((h for h in hours if h["day_of_week"] == day_name), None)
    if not store_hours:
        return True  # no hours defined = always after-hours (conservative)
    open_time  = datetime.strptime(store_hours["open_at"],  "%H:%M").time()
    close_time = datetime.strptime(store_hours["close_at"], "%H:%M").time()
    return not (open_time <= local_dt.time() <= close_time)
```

## 12. Event types in the canary:events stream

| CanonicalEvent.event_type | Trigger |
|---|---|
| `store.upserted` | Store sync (daily or cache-miss) |
| `store.cache_miss` | STR_ID in Document not found in cp_known_store_ids |
| `station.upserted` | Station sync (daily) |

Sub2 dispatch additions:

```python
EVENT_TYPE_PARSERS: dict[tuple[str, str], Callable] = {
    ...
    ("counterpoint", "store.upserted"):   parse_cp_store,
    ("counterpoint", "station.upserted"): parse_cp_station,
}
```

## 13. New tables summary — Alembic migration checklist

| Object | Schema | Action | Notes |
|---|---|---|---|
| `cp_known_store_ids` | app | CREATE | Store ID registry + discovery tracking |
| `cp_store_config` | app | CREATE | PS_STR_CFG_PS substrates for Q rules |
| `cp_station_config` | app | CREATE | PS_STA_CFG_PS; tender defaults |
| `locations.square_location_id` | app | ALTER nullable | Shared with customers migration |
| `locations.timezone` | app | ALTER nullable | Counterpoint stores use state-derived TZ |

## 14. Activation ordering constraint (documented)

This SDD formalizes the activation ordering dependency. The `CounterpointMerchantActivationService` must run sync steps in this order:

```
Phase A — Reference data (no Document dependency):
  1. Store sync → cp_store_config (WALK_IN_CUST_NO, discount caps)
  2. CustomerControl → cp_tier_definitions
  3. ItemCategories → cp_item_categories

Phase B — Entity sync (requires Phase A):
  4. Customer initial load → cp_customer_profiles + external_identities
  5. Item catalog initial load → cp_item_catalog + external_identities

Phase C — Transaction sync (requires Phase A + B for resolution):
  6. Document initial load → sales.transactions + all sub-tables
```

Phases A and B can overlap for different entity types, but Phase C cannot
begin until Phase A is fully committed — specifically, WALK_IN_CUST_NO
must be set for all stores before the first Document is parsed.

## 15. Acceptance criteria

**AC-N-01 — Store sync:** After merchant activation with store list
`["MAIN"]`, `app.locations` has a row with `location_name = "Main Store"`,
`app.cp_store_config` has `max_disc_pct = 50`, `max_disc_amt = 200`,
`walk_in_cust_no = "CASH"`, and `app.external_identities` has
`entity_type='location', external_id='MAIN'`.

**AC-N-02 — WALK_IN_CUST_NO resolution:** `resolve_transaction_customer()`
with `cust_no = "CASH"` for the MAIN store returns `None`.
`resolve_transaction_customer()` with `cust_no = "1000"` returns the
correct Canary customer UUID. `cust_no = None` returns `None` without
hitting the DB.

**AC-N-03 — C-1001 store threshold:** A transaction line with a discount
amount equal to `max_disc_amt + $0.01` for the MAIN store triggers
C-1001 at severity `medium`. For a different store with `max_disc_amt = $500`,
the same dollar discount does NOT trigger.

**AC-N-04 — Cache-miss:** A Document referencing STR_ID `"EAST"` (not
in `cp_known_store_ids`) queues an on-demand `GET /Store/EAST` fetch.
After fetch, `cp_known_store_ids` and `cp_store_config` contain the EAST
store. The Document is re-processed with the resolved store_id.

**AC-N-05 — Timezone derivation:** A store with `STATE = "CA"` gets
`timezone = "America/Los_Angeles"` in `app.locations`. An after-hours
rule evaluating a transaction at 22:00 UTC (14:00 Pacific) correctly
identifies it as within business hours if the store is open until 20:00
Pacific.

**AC-N-06 — Station sync:** After store sync completes for MAIN, stations
are discovered from Document `STA_ID` values. `cp_station_config` has
one row per station with `dflt_tnd_pay_cod` populated.

**AC-N-07 — Activation ordering:** Running a Document sync before Phase A
completes raises `ActivationOrderError`. The error message names the
missing precondition (e.g., "store config not seeded for merchant {id}").

## 16. Open questions

| ID | Question | Impact |
|---|---|---|
| N-OQ-01 | Is there a `GET /Stores` (plural) bulk list endpoint not present in the API guide? If yes, replace the "discover from Documents" model with a proper initial fetch. | Store discovery mechanism |
| N-OQ-02 | Counterpoint's server cache includes Stores (24h). But `RS_UTC_DT` is present on `PS_STR`. Is it present in the Store response consistently? If yes, we can use it for watermark-filtered daily sync rather than full re-sync. | Polling efficiency at scale |
| N-OQ-03 | For a 31-store garden center, do all stores share the same `WALK_IN_CUST_NO` (likely `"CASH"`) or does each store configure it independently? Confirms whether per-store sentinel lookup is necessary or if a merchant-wide default suffices. | Sentinel lookup performance |
| N-OQ-04 | Business hours input: Counterpoint does not expose hours. Does Rapid POS' onboarding process collect store hours? Or does Canary need to ask for them during onboarding? If Rapid POS has them, a one-time import is better than manual entry. | After-hours rule accuracy |
| N-OQ-05 | `PS_STR_CFG_PS.EDC_PROCESSOR` encodes the payment processor. In sandbox it is `"N"` (simulate). What are the real-world values (e.g., `"FD"` for First Data)? Needed if tender-mix rules need to distinguish processor-specific tender patterns. | Tender-mix rule calibration |

---

## Related

- `docs/sdds/canary/ncr-counterpoint-tsp-adapter.md` — Document adapter; uses STR_ID resolution from this SDD
- `docs/sdds/canary/ncr-counterpoint-customer-adapter.md` — resolves R-OQ-02 (WALK_IN_CUST_NO)
- `docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring.md` — Q rules reading from cp_store_config
- `Brain/wiki/ncr-counterpoint-api-reference.md` — Counterpoint endpoint reference (§ Module N)
- `Canary/canary/models/app/locations.py` — Location model; bridge target
