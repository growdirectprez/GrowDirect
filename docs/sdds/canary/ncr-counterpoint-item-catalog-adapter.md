---
id: sdd-cp-item-catalog
title: NCR Counterpoint — Item Catalog Adapter (Module S)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/ncr-counterpoint-tsp-adapter.md
  - docs/sdds/canary/ncr-counterpoint-customer-adapter.md
  - Canary/docs/sdds/v2/data-model.md
source-endpoints:
  - GET /Items (RS_UTC_DT watermarked bulk sync)
  - GET /Item/{ItemNo} (per-record fetch)
  - GET /ItemCategories (category + margin targets, cached)
  - GET /ItemCategory/{CategCod} (single category)
source-tables: IM_ITEM, IM_CATEG_COD, IM_SUBCAT_COD, IM_ITEM_NOTE
target-tables:
  - app.cp_item_catalog (new)
  - app.cp_item_categories (new)
  - app.external_identities (existing — new rows, entity_type='product')
  - app.poll_watermarks (existing — new entity_type 'item', 'item_categories')
---

# NCR Counterpoint — Item Catalog Adapter (Module S)

## 1. Purpose and scope

This SDD specifies how Canary's TSP adapter syncs the NCR Counterpoint item
master (`IM_ITEM`) and item category taxonomy (`IM_CATEG_COD`) into Canary's
internal catalog tables.

The item catalog serves two purposes in Canary:

1. **Transaction enrichment:** When a Document line item references an ITEM_NO,
   Canary resolves it to a Canary product UUID via `external_identities` and
   joins the catalog for enriched display (description, category, price).

2. **Module Q detection substrate:** `LST_COST`, `PRC_1`, `IS_DISCNTBL`,
   `PROMPT_FOR_PRC`, `ITEM_IS_MISC`, and the category-level `MIN_PFT_PCT` /
   `TRGT_PFT_PCT` fields are the margin and discount anomaly substrates for
   the Chirp rule families Q-C and Q-P.

**Not covered here:** inventory levels by location (`GET /Item/Inventory`,
`GET /InventoryLocations` — deferred to Module D), serial number tracking
(`GET /ItemSerial` — Phase 2+), vendor-item relationships (`GET /VendorItem`
— Phase 2+).

## 2. Architecture overview

```
Counterpoint REST API
  GET /Items?StartDate={watermark}      -- RS_UTC_DT-filtered item page
  GET /Item/{ITEM_NO}                   -- per-item refresh
  GET /ItemCategories                   -- category taxonomy (24h cached)
           │
           ▼
  CounterpointItemPoller
  (POSAdapter subclass — poll_intervals: item=86400s, item_categories=86400s)
           │
           ├── Emits CanonicalEvent(event_type="item.upserted")
           ├── Emits CanonicalEvent(event_type="item_categories.refreshed")
           │
           ▼
  canary:events stream (Valkey)
           │
           ▼
  Sub2 — ItemUpsertParser / ItemCategoryParser
           │
           ├── Route to:
           │     app.cp_item_catalog       (item master)
           │     app.cp_item_categories    (category + margin targets)
           │     app.external_identities   (ITEM_NO → Canary product UUID)
           │
           └── Emit item_catalog.refreshed event after initial load
```

**Poll cadence rationale:** The Counterpoint server caches item METADATA for
24 hours; it does not cache inventory levels. Canary's item catalog poll runs
daily (86400s) for catalog integrity, with a faster on-demand trigger available
when a Document line item references an ITEM_NO not found in `cp_item_catalog`
(cache-miss trigger pattern — see §8).

## 3. Polling strategy

| Property | Value |
|---|---|
| Endpoint | `GET /Items` |
| Watermark field | `RS_UTC_DT` |
| Watermark params | `StartDate={last_event_ts}` |
| Default poll interval | 86400s (daily) |
| Cold start behavior | No `StartDate` — full catalog pull. May be large for multi-thousand-SKU retailers. Page in batches of 500. |
| `poll_watermarks` key | `(merchant_id, 'counterpoint', company_alias, 'item')` |
| Categories poll interval | 86400s (daily); separate watermark entity_type = `'item_categories'` |
| Error handling | Exponential backoff. 401/403 → halt + `credential_error` status on source. |
| Cache flush | Send `ServerCache: no-cache` on first item poll of each day, because item metadata is server-cached 24h and out-of-band UI edits would not auto-invalidate. |

### Item count estimates for garden center verticals

A 31-store garden center typically carries 8,000–20,000 active SKUs. Initial
load at 500 rows/page = 16–40 API pages. At ~200ms/page, initial sync completes
in under 10 seconds. Watermark-filtered daily delta is typically < 100 items.

## 4. Field mapping — app.cp_item_catalog

No PII in item records. Strip only the DESCR_UPR and NAM_UPR normalized
variants (redundant uppercase copies) and the `IM_ITEM_NOTE` array (may
contain operational text; strip to avoid capturing vendor pricing notes).
`EC_ITEM_DESCR.HTML_DESCR` is also stripped — not needed for LP analytics.

### DDL

```sql
CREATE TABLE app.cp_item_catalog (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID NOT NULL REFERENCES app.merchants(id),

    -- Identity
    item_no             TEXT NOT NULL,               -- IM_ITEM.ITEM_NO (POS item code)
    descr               TEXT,                         -- IM_ITEM.DESCR (display description)
    long_descr          TEXT,                         -- IM_ITEM.LONG_DESCR
    short_descr         TEXT,                         -- IM_ITEM.SHORT_DESCR
    addl_descr_1        TEXT,                         -- supplemental descriptions
    addl_descr_2        TEXT,
    addl_descr_3        TEXT,

    -- Classification
    item_typ            TEXT,                         -- I=inventory, N=non-inventory, S=service, M=assembly
    categ_cod           TEXT,                         -- top-level category (FK → cp_item_categories)
    subcat_cod          TEXT,                         -- subcategory
    categ_subcat        TEXT,                         -- denormalized CATEG/SUBCAT composite
    acct_cod            TEXT,                         -- GL account code
    attr_cod_1          TEXT,                         -- attribute 1 (e.g. color)
    attr_cod_2          TEXT,                         -- attribute 2 (e.g. material)
    trk_meth            TEXT,                         -- N=none, S=serial, L=lot
    stat                TEXT,                         -- A=active, I=inactive

    -- Unit of measure
    stk_unit            TEXT,                         -- stocking UOM (EACH, LB, FLAT, TRAY, CU YD)
    qty_decs            INTEGER,                      -- qty decimal places (>0 = fractional item)
    prc_decs            INTEGER,                      -- price decimal places
    is_weighed          BOOLEAN,                      -- weighed item (bulk goods, soil)
    pref_unit_nam       TEXT,                         -- preferred unit name
    pref_unit_numer     INTEGER,                      -- preferred unit numerator
    pref_unit_denom     INTEGER,                      -- preferred unit denominator

    -- Pricing (Module Q substrate)
    prc_1               NUMERIC(12, 4),               -- price level 1 (base retail)
    reg_prc             NUMERIC(12, 4),               -- regular price
    lst_cost            NUMERIC(12, 4),               -- last cost (margin floor substrate)
    dflt_cost_of_sls_pct NUMERIC(5, 2),              -- default cost-of-sales % (margin floor)
    item_vend_no        TEXT,                         -- primary vendor code

    -- Discount / price control flags (Module Q substrate)
    is_discntbl         BOOLEAN,                      -- discountable flag
    prompt_for_prc      BOOLEAN,                      -- operator-prompted price (open price risk)
    prompt_for_cost     BOOLEAN,                      -- operator-prompted cost
    prompt_for_descr    BOOLEAN,                      -- operator-prompted description
    item_is_misc        BOOLEAN,                      -- miscellaneous/no-barcode item (elevated risk)
    mix_match_cod       TEXT,                         -- mix-and-match promotion code

    -- Tax
    is_txbl             BOOLEAN,
    is_food_stmp_item   BOOLEAN,

    -- eCommerce
    is_ecomm_item       BOOLEAN,
    barcod              TEXT,                         -- primary barcode

    -- Kit / BOM
    is_bom_par          BOOLEAN,                      -- bill-of-materials parent
    is_kit_par          BOOLEAN,                      -- kit parent

    -- Source metadata
    lst_maint_dt        TIMESTAMPTZ,
    lst_maint_usr_id    TEXT,
    lst_recv_dat        TIMESTAMPTZ,                  -- last received from vendor
    stat_dat            TIMESTAMPTZ,                  -- status change date
    rs_utc_dt           TIMESTAMPTZ NOT NULL,
    rs_stat             INTEGER,                      -- 0=active, 1=changed

    -- Canary metadata
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (merchant_id, item_no)
);

CREATE INDEX idx_cp_item_catalog_merchant_categ
    ON app.cp_item_catalog (merchant_id, categ_cod);

CREATE INDEX idx_cp_item_catalog_merchant_stat
    ON app.cp_item_catalog (merchant_id, stat);

CREATE INDEX idx_cp_item_catalog_merchant_discntbl
    ON app.cp_item_catalog (merchant_id, is_discntbl)
    WHERE is_discntbl = FALSE;

CREATE INDEX idx_cp_item_catalog_merchant_openpr
    ON app.cp_item_catalog (merchant_id, prompt_for_prc)
    WHERE prompt_for_prc = TRUE;
```

The partial indexes on `is_discntbl=FALSE` and `prompt_for_prc=TRUE` optimize
the Module Q query path: both rule families need only the minority-case items.

## 5. Field mapping — app.cp_item_categories

Category-level margin targets are the primary output of `GET /ItemCategories`.
This is the Module Q margin floor substrate — every Chirp rule that asks
"was this item sold below minimum margin?" joins through here.

### DDL

```sql
CREATE TABLE app.cp_item_categories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID NOT NULL REFERENCES app.merchants(id),

    categ_cod       TEXT NOT NULL,
    descr           TEXT,

    -- Module Q margin targets (critical substrate)
    min_pft_pct     NUMERIC(5, 2),    -- minimum profit % (floor); Q-M.1 substrate
    trgt_pft_pct    NUMERIC(5, 2),    -- target profit % (benchmark); Q-M.1 context

    -- Source metadata
    lst_maint_dt    TIMESTAMPTZ,
    lst_maint_usr_id TEXT,
    rs_utc_dt       TIMESTAMPTZ,
    rs_stat         INTEGER,

    -- Canary metadata
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (merchant_id, categ_cod)
);

CREATE TABLE app.cp_item_subcategories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID NOT NULL REFERENCES app.merchants(id),
    categ_cod       TEXT NOT NULL
        REFERENCES app.cp_item_categories (categ_cod)
        DEFERRABLE INITIALLY DEFERRED,  -- avoid insert ordering issues
    subcat_cod      TEXT NOT NULL,
    descr           TEXT,
    lst_maint_dt    TIMESTAMPTZ,
    rs_stat         INTEGER,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (merchant_id, categ_cod, subcat_cod)
);
```

`GET /ItemCategories` returns the full hierarchy in one call — categories with
nested `IM_SUBCAT_COD[]` arrays. The parser flattens to two tables.

**Caching note:** `ItemCategories` is server-cached 24 hours. Send
`ServerCache: no-cache` on the first category poll of each day.

## 6. external_identities bridge

Every item that enters Canary gets a row in `app.external_identities`:

| external_identities column | Value |
|---|---|
| `entity_type` | `'product'` |
| `entity_id` | Canary product UUID (from `cp_item_catalog.id`) |
| `source_code` | `'counterpoint'` |
| `external_id` | `IM_ITEM.ITEM_NO` (the alphanumeric SKU, e.g. `"ADM-SCD"`) |
| `is_primary` | `True` |

**Forward resolution** (ITEM_NO from Document line → Canary catalog entry):

```python
def resolve_item(db, merchant_id: UUID, item_no: str) -> Optional[UUID]:
    row = db.query(ExternalIdentity).filter_by(
        merchant_id=str(merchant_id),
        source_code="counterpoint",
        entity_type="product",
        external_id=item_no,
    ).first()
    return UUID(row.entity_id) if row else None
```

**Cache-miss pattern:** If `resolve_item()` returns `None` for an ITEM_NO
encountered in a Document line, the TSP adapter queues an on-demand
`GET /Item/{item_no}` fetch. The resulting item is inserted into
`cp_item_catalog` and `external_identities` immediately (outside the normal
daily sync). The Document line item is then re-processed with the resolved
catalog entry. This handles new/unknown items that arrive in transactions
before the daily catalog sync runs.

## 7. Transaction line item linkage

The existing `sales.transaction_line_items` table uses `catalog_object_id`
as the vendor item ID. For Counterpoint transactions (from
`ncr-counterpoint-tsp-adapter.md`), the `parse_cp_transaction()` function
writes `PS_DOC_LIN.ITEM_NO` to `transaction_line_items.catalog_object_id`.

The enrichment join at query time:

```sql
SELECT
    li.*,
    ci.descr,
    ci.categ_cod,
    ci.categ_subcat,
    ci.prc_1         AS catalog_price,
    ci.lst_cost,
    ci.is_discntbl,
    ci.prompt_for_prc,
    ci.item_is_misc,
    cat.min_pft_pct,
    cat.trgt_pft_pct
FROM sales.transaction_line_items li
LEFT JOIN app.external_identities ei
    ON ei.merchant_id = li.merchant_id
   AND ei.source_code = 'counterpoint'
   AND ei.entity_type = 'product'
   AND ei.external_id  = li.catalog_object_id
LEFT JOIN app.cp_item_catalog ci
    ON ci.id = ei.entity_id::uuid
LEFT JOIN app.cp_item_categories cat
    ON cat.merchant_id = ci.merchant_id
   AND cat.categ_cod   = ci.categ_cod
WHERE li.transaction_id = :txn_id;
```

## 8. Module Q integration

### Margin floor detection (Q-M.1 family)

The core loss-prevention use case. Two thresholds apply:

**Item-level cost floor:** If `PS_DOC_LIN_PRICE < IM_ITEM.LST_COST`, the
item was sold at a loss — sweethearting or cost-entry manipulation.

```
alert trigger:
  transaction_line_items.base_price_cents / 100.0
  < cp_item_catalog.lst_cost
  AND cp_item_catalog.lst_cost IS NOT NULL
  AND cp_item_catalog.lst_cost > 0
```

**Category margin floor:** If `(sale_price - cost) / sale_price < MIN_PFT_PCT / 100`,
the margin is below the operator-defined floor for the category.

```
alert trigger:
  (base_price_cents/100.0 - lst_cost) / NULLIF(base_price_cents/100.0, 0)
  < cp_item_categories.min_pft_pct / 100.0
```

### Non-discountable item discount (Q-M.2)

If `cp_item_catalog.is_discntbl = FALSE` and `transaction_line_items.total_discount_cents > 0`,
flag as unauthorized discount on a non-discountable item.

### Open-price item anomaly (Q-P.1)

Items with `prompt_for_prc = TRUE` or `item_is_misc = TRUE` carry elevated
risk because the cashier manually enters the price. Detection logic:

- Compare the entered price against the median price for the same ITEM_NO over
  the trailing 30 days. Deviation > configurable threshold → flag.
- `item_is_misc = TRUE` items with no `catalog_object_id` match (they have
  no ITEM_NO in the ticket) are flagged as miscellaneous category transactions
  for secondary review.

### Fractional quantity anomaly (Q-Q.1 — garden center)

Garden center items with `qty_decs > 0` or `is_weighed = TRUE` (bulk soil,
peat moss, mulch) are susceptible to quantity manipulation at the scale level.
Rule: if `PS_DOC_LIN.QTY_SOLD` for a weighed item is an unusually round
number (e.g., exactly 1.0 LB for a product normally sold at 2–10 LB), flag
for secondary review.

### Item status change (Q-STAT.1)

When `IM_ITEM.STAT` transitions `A → I` (active to inactive), Canary logs
the event in `cp_item_catalog.updated_at` + emits a `item.deactivated`
event. If transactions continue to reference the ITEM_NO after deactivation
date, flag as anomalous (potential use of discontinued item codes).

### Rule substrate summary table

| Rule | Primary field | Table | Join path |
|---|---|---|---|
| Q-M.1 cost floor | `lst_cost` | `cp_item_catalog` | `external_identities` → `cp_item_catalog` |
| Q-M.1 margin floor | `min_pft_pct` | `cp_item_categories` | `cp_item_catalog.categ_cod` → `cp_item_categories` |
| Q-M.2 non-discountable | `is_discntbl` | `cp_item_catalog` | same |
| Q-P.1 open price | `prompt_for_prc`, `item_is_misc` | `cp_item_catalog` | same |
| Q-Q.1 fractional qty | `qty_decs`, `is_weighed` | `cp_item_catalog` | same |
| Q-STAT.1 deactivated item | `stat` transition | `cp_item_catalog` | direct |

## 9. Garden center vertical — item type notes

The H&G vertical has item patterns that affect Module Q substrates:

| Pattern | IM_ITEM fields | Detection implication |
|---|---|---|
| Live goods (annuals, perennials) | `STAT` transitions frequently (seasonal); `STK_UNIT=EACH/FLAT/TRAY` | Q-STAT.1: deactivation in fall, reactivation in spring; normal — suppress false positives via seasonal calendar |
| Bulk amendments (soil, mulch) | `IS_WEIGHED=Y`, `QTY_DECS>0`, `STK_UNIT=CU YD/LB` | Q-Q.1: weighed goods; baseline weight distribution needed for anomaly detection |
| Tropicals / houseplants | High `PRC_1` variance (individual specimen pricing); `PROMPT_FOR_PRC=Y` for premium specimens | Q-P.1: open-price rule applies; threshold must be calibrated to category variance |
| Cash vendor plants | `ITEM_VEND_NO` absent or generic; `CATEG_COD` = nursery/plant category | Q-VEND.1: cash-purchase receipts in Module Q allow-list (see `ncr-counterpoint-tsp-adapter.md §12`) |
| Gift items / hardgoods | `IS_DISCNTBL=Y`; end-of-season 50% clearance is legitimate | Q-M.2: clearance discount rules need seasonal suppression window to avoid alert flood |

These vertical-specific thresholds are configured in `app.merchant_rule_configs`,
not hardcoded in the detection rules themselves. The rules are generic;
per-merchant calibration happens at config time.

## 10. Event types in the canary:events stream

| CanonicalEvent.event_type | Trigger |
|---|---|
| `item.upserted` | New or updated item from `GET /Items` watermark poll |
| `item.cache_miss` | ITEM_NO in Document line not found in catalog; triggers on-demand fetch |
| `item.deactivated` | STAT transition A→I detected during sync |
| `item_categories.refreshed` | After successful `GET /ItemCategories` poll |
| `item_catalog.initial_load_complete` | After full initial catalog sync completes |

Sub2 dispatch additions:

```python
EVENT_TYPE_PARSERS: dict[tuple[str, str], Callable] = {
    ...  # existing entries
    ("counterpoint", "item.upserted"):              parse_cp_item,
    ("counterpoint", "item.cache_miss"):             parse_cp_item,    # same parser
    ("counterpoint", "item_categories.refreshed"):  parse_cp_item_categories,
}
```

## 11. Parser function shapes

### parse_cp_item

```python
def parse_cp_item(
    event: CanonicalEvent,
    db: Session,
) -> CpItemParseResult:
    """
    Input:  CanonicalEvent.payload = IM_ITEM dict
    Output: CpItemParseResult:
              - catalog_id: UUID (created or resolved)
              - item_no: str
              - catalog: CpItemCatalog (upsert target)
              - ext_identity: ExternalIdentity (upsert target)
              - stat_changed: bool (True if STAT transitioned to 'I')
    Strip:  DESCR_UPR, LONG_DESCR_UPR, IM_ITEM_NOTE (array), EC_ITEM_DESCR
    """

STRIP_FIELDS = frozenset({
    "DESCR_UPR", "LONG_DESCR_UPR", "SHORT_DESCR",  # keep SHORT_DESCR? assess
    "IM_ITEM_NOTE",
    "EC_ITEM_DESCR",
    # Ecommerce display fields not needed for LP analytics:
    "ECOMM_LST_PUB_STAT", "ECOMM_NXT_PUB_UPDT", "ECOMM_NXT_PUB_FULL",
    "ECOMM_LST_PUB_TYP", "ECOMM_LST_IMP_TYP",
    "ECOMM_TXBL_1", "ECOMM_TXBL_2", "ECOMM_TXBL_3",
    "BARCOD_3_OF_9",   # computed 3-of-9 barcode representation, redundant
    "GRID_ENT_1", "GRID_ENT_2", "GRID_ENT_3",   # UI grid settings
    "LST_LCK_DT",      # last lock datetime (UI artifact)
    "WARR_UNIT_1", "WARR_UNIT_2",  # warranty unit codes (not LP-relevant)
    "SER_NO_REQ_FOR_SAL",           # serial-number-on-sale flag (Phase 2+)
})
```

### parse_cp_item_categories

```python
def parse_cp_item_categories(
    event: CanonicalEvent,
    db: Session,
) -> CpItemCategoryParseResult:
    """
    Input:  CanonicalEvent.payload = {"ItemCategories": [...]} dict
    Output: List of (CpItemCategory, [CpItemSubcategory]) upsert targets
    Note:   Flattens the IM_SUBCAT_COD[] nested array into cp_item_subcategories.
    """
```

## 12. Upsert and status-change pattern

Item catalog rows are upserted on `(merchant_id, item_no)`. After upsert,
compare the new `stat` value against the stored value:

```python
previous_stat = db.query(CpItemCatalog.stat).filter_by(
    merchant_id=merchant_id, item_no=item_no
).scalar()

db.execute(
    pg_insert(CpItemCatalog).values(**item_data)
    .on_conflict_do_update(
        constraint="uq_cp_item_catalog_merchant_item",
        set_={k: stmt.excluded[k] for k in UPSERT_COLUMNS},
    )
)

if previous_stat == "A" and item_data.get("stat") == "I":
    emit_event(CanonicalEvent(
        event_type="item.deactivated",
        external_id=item_no,
        ...
    ))
```

## 13. poll_watermarks entries

```sql
INSERT INTO app.poll_watermarks
    (merchant_id, source_code, company_alias, entity_type, last_polled_at)
VALUES
    ({merchant_id}, 'counterpoint', {company_alias}, 'item',            now()),
    ({merchant_id}, 'counterpoint', {company_alias}, 'item_categories', now())
ON CONFLICT DO NOTHING;
```

## 14. New tables summary — Alembic migration checklist

| Table | Schema | Action | Purpose |
|---|---|---|---|
| `cp_item_catalog` | app | CREATE | Counterpoint item master |
| `cp_item_categories` | app | CREATE | Category taxonomy + margin targets |
| `cp_item_subcategories` | app | CREATE | Subcategory taxonomy |

## 15. Acceptance criteria

**AC-S-01 — Initial load:** A fresh tenant activation with the 3-item Counterpoint
test dataset (ITEM_NO: `18HOLES`, `ADM-SCD`, `WEDGE`) results in 3
`cp_item_catalog` rows, 3 `external_identities` rows, 1 `cp_item_categories`
row (GOLF), and 6 `cp_item_subcategories` rows. No `IM_ITEM_NOTE` or
`EC_ITEM_DESCR` content stored.

**AC-S-02 — Incremental sync:** Updating `ADM-SCD`'s `PRC_1` from 399.99 to
379.99 in Counterpoint (simulated) results in `cp_item_catalog.prc_1`
updating after the next poll. `LST_MAINT_DT` and `rs_utc_dt` advance.

**AC-S-03 — Forward resolution:** `resolve_item(db, merchant_id, "ADM-SCD")`
returns the correct Canary UUID. `resolve_item(db, merchant_id, "UNKNOWN-SKU")`
returns `None` and triggers a cache-miss on-demand fetch.

**AC-S-04 — Deactivation event:** Updating `ADM-SCD.STAT` from `A` to `I`
in Counterpoint results in a `item.deactivated` event in the stream and
`cp_item_catalog.stat = 'I'` after the next poll.

**AC-S-05 — Module Q margin floor:** For a transaction line item on `ADM-SCD`
with `base_price_cents = 10000` (below `lst_cost = 159.996`), the Q-M.1 rule
triggers an alert with the correct item identifier and merchant context.

**AC-S-06 — Non-discountable detection:** For a transaction line item on any
item where `is_discntbl = FALSE` with `total_discount_cents > 0`, the Q-M.2
rule triggers. Verify the `cp_item_catalog` join resolves correctly.

**AC-S-07 — Category margin floor:** For a transaction line item in the `GOLF`
category (min_pft_pct = 50), a sale at 45% margin triggers Q-M.1. A sale at
55% margin does not.

**AC-S-08 — Cache-miss on-demand fetch:** A Document poll that contains an
ITEM_NO not yet in `cp_item_catalog` queues an on-demand `GET /Item/{ITEM_NO}`
fetch, which completes within the same poll cycle. The Document line item
re-processes with the resolved catalog entry.

## 16. Open questions

| ID | Question | Impact |
|---|---|---|
| S-OQ-01 | Price levels: Counterpoint supports up to 5 price levels (PRC_1 through PRC_5). Which price levels does the garden center deployment use? PRC_1 is confirmed. Are PRC_2–5 used for contractor/wholesale tiers? If yes, add PRC_2–5 columns to `cp_item_catalog`. | Module P (pricing tier) and Q-M.4 accuracy |
| S-OQ-02 | Live-goods STAT cycle: Do garden center Counterpoint deployments set `STAT=I` seasonally, or do they archive the item entirely (DELETE)? Determines whether Q-STAT.1 fires seasonally or only on true deactivation. | False positive rate for Q-STAT.1 |
| S-OQ-03 | Cash vendor receive DOC_TYP: When a garden center buys plants for cash from a local grower, what DOC_TYP and ITEM_NO pattern appears? Is it a new receipt (RECVR) against a generic vendor item, or an ad-hoc Document with a miscellaneous ITEM_NO? | Q-VEND.1 allow-list construction |
| S-OQ-04 | Bulk goods pricing unit: Is `IS_WEIGHED=Y` reliably set for all bulk amendment items (mulch, soil, fertilizer) in the garden center's Counterpoint config, or is it inconsistently applied? | Q-Q.1 fractional quantity detection reliability |
| S-OQ-05 | `MIN_PFT_PCT` calibration: Are the garden center's `IM_CATEG_COD.MIN_PFT_PCT` values actually set (non-zero), or are they left at 0 (default)? If all zeros, the category margin floor rule has no bite until the retailer configures them. | Q-M.1 effectiveness; may need operator-assisted config step |
| S-OQ-06 | Counterpoint item count for the target engagement: Approximate SKU count across all stores. Determines whether initial load requires chunking strategy beyond simple 500-row paging. | Initial load performance planning |

---

## Related

- `docs/sdds/canary/ncr-counterpoint-tsp-adapter.md` — Document/sales adapter; uses ITEM_NO → catalog resolution
- `docs/sdds/canary/ncr-counterpoint-customer-adapter.md` — Customer adapter; CATEG_COD parallel (customer vs item tier)
- `Brain/wiki/ncr-counterpoint-api-reference.md` — Counterpoint endpoint reference (§ Module S — Items)
- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — Module Q rule catalog; Q-M.1, Q-M.2, Q-P.1, Q-Q.1 rule definitions
- `Brain/wiki/garden-center-operating-reality.md` — H&G vertical specifics: seasonal STAT transitions, bulk goods, cash vendor receipts
- `Canary/docs/sdds/v2/data-model.md` — CRDM `sales.transaction_line_items` table definition
