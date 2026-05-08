---
last-compiled: 2026-05-08
needs-review: false
type: reference
status: active
tags: [counterpoint, ncr, catalog, data-model, audit, gap-report, schema, item-master, canary-go]
created: 2026-05-08
gro: GRO-880
source: docs/sdds/canary/ncr-counterpoint-openapi.yaml
---

# Counterpoint Catalog Data-Model Audit

A field-level comparison between **Counterpoint REST API v2.4** (the surface Canary's adapter can actually reach) and Canary's `catalog.*` schema, sequenced by which gap matters most for Bart's stores. Source of truth for Counterpoint side: `docs/sdds/canary/ncr-counterpoint-openapi.yaml` — the IM_ITEM, IM_INV, IM_CATEG, SN_SER, VendorItem schemas.

## Headline finding — the REST surface is narrower than the back-office

The audit's premise (filed in [GRO-880](https://linear.app/growdirect/issue/GRO-880)) assumed Counterpoint had:

- **3D grid** (Color × Size × Dimension matrix variants)
- **3-tier UOM** (Stocking / Alternate / Associated units)
- **5-level merchandise hierarchy** (Department → Class → Subclass → Category → Subcategory)
- **6 attributes + 20 profile codes** (rich metadata)
- **10-layer pricing** (Regular / Location / Special / Contract / Promotional / Rule / Mix-match / Break / Minimum / Tier)

All of those exist in Counterpoint's **back-office UI** (`frmitems`, `frmitemcategories`, etc., per `Brain/wiki/ncr-counterpoint-functional-decomposition.md` §3). **None of them are fully exposed in the REST API.** The REST surface flattens the back-office model:

| Capability | Back-office UI | REST API (CPAPI v2.4) | Implication |
|---|---|---|---|
| Grid (multi-dim matrix) | Yes — color/size/dim cells | **No** — each cell is a flat `ITEM_NO` row | Variants are sibling rows, not a hierarchy |
| Multi-UOM | Stocking + Alternate + Associated | **Single** — `STK_UNIT` + `PREF_UNIT` only | UOM conversions invisible at REST level |
| Multi-barcode | Yes — Barcode tab, N per item | **Single** — `BARCOD` field on IM_ITEM | Aliases not exposed |
| Hierarchy depth | Category + Subcategory + 6 attrs + 20 profiles | **2-level** + 2 ATTR codes + 3 ADDL_DESCR | UI hierarchy is mostly free-text profiles |
| Pricing layers | 10 distinct precedence levels | **3 fields** — `PRC_1`, `REG_PRC`, `LST_COST` | Tier/contract/promo derived from observation |

**This radically narrows the gap.** Canary's `catalog.items` schema is **closer** to Counterpoint REST than to Counterpoint back-office. The genuine gaps are mostly **additive columns + JSONB extensions** — not a fundamental restructure. The audit's earlier narrative ("schema needs to evolve to Counterpoint altitude") was true for back-office altitude; for REST altitude, the work is materially smaller.

The strategic question this surfaces: **does Canary integrate via REST only, or does it also have SQL Server direct access?** The Module T adapter reads `PS_DOC_HDR` directly from SQL Server (per `counterpoint-product-state-2026.md`). If the catalog adapter can do the same against `IM_ITEM_GRID` / `IM_ITEM_VEND_UNIT` / `IM_ITEM_BARCOD` tables, Canary can capture the back-office richness. **This is open question #1 for Bart's team.**

---

## IM_ITEM — the actual REST shape

From `docs/sdds/canary/ncr-counterpoint-openapi.yaml` lines 546-598. This is what `GET /Item/{ItemNo}` returns. **Reading this is the audit.**

### Identity

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `ITEM_NO` | string | `catalog.items.sku` | None |
| `DESCR` | string | `catalog.items.description` | None |
| `DESCR_UPR` | string | — | Derived; Canary computes via Postgres `lower()` index |
| `LONG_DESCR` | string | `catalog.items.attributes.long_description` (JSONB) | Promote to column |
| `SHORT_DESCR` | string | `catalog.items.short_description` | None |
| `ADDL_DESCR_1` | string | — | **Missing** — used for plant common name (garden centers) |
| `ADDL_DESCR_2` | string | — | **Missing** — used for botanical name |
| `ADDL_DESCR_3` | string | — | **Missing** — used for Spanish name / alt-language |
| `BARCOD` | string | `catalog.item_barcodes.barcode` (multi-row) | Canary richer — REST has only one |

**Gap:** add `addl_descr_1/2/3` columns OR carry as `attributes.descriptions` JSONB array. **Recommend JSONB** — these are language-style alternates; column-per-language doesn't compose.

### Classification

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `ITEM_TYP` | string | `catalog.items.item_type` | Counterpoint values are codes (`I`/`N`/...); Canary uses words (`standard`/`service`). Need adapter mapping table. |
| `CATEG_COD` | string | `catalog.items.category_id` (FK) | Need `vendor_category_code` mapping in `catalog.product_categories.attributes` |
| `SUBCAT_COD` | string | (none — flat in Canary) | **Gap** — Canary categories are flat single-level via FK; Counterpoint has 2-level. Add `subcategory_code` column on items, OR represent subcategory as a child category row with `parent_id` |
| `CATEG_SUBCAT` | string | — | Derived display; ignore |
| `ACCT_COD` | string | `catalog.items.attributes.gl_account_category` (JSONB) | Promote to column when finance module ships |
| `ATTR_COD_1` | string | — | **Missing** — generic attribute slot |
| `ATTR_COD_2` | string | — | **Missing** — generic attribute slot |
| `TRK_METH` | string | — | **Missing** — tracking method (serial / lot / none); see Tracking section |

**Gap:** the 2-level hierarchy is real. Three options:

1. **Add `subcategory_code` text column** (denormalized; matches REST shape)
2. **Make `catalog.product_categories` self-referential via existing `parent_id`** (already supports tree depth via ltree path; cleaner long-term, requires the adapter to insert parent + child rows)
3. **Store `vendor_subcategory_code` in `catalog.product_categories.attributes` JSONB** (lookup-on-write at adapter time)

**Recommend option 2** — `product_categories.parent_id` + ltree path already exists in the schema (`02_catalog_items.sql`). Adapter inserts category as parent and subcategory as child. Existing schema; zero migration.

For the 2 ATTR codes — these are user-defined dimensions. Treat as JSONB: `attributes.attr_cod_1` / `attributes.attr_cod_2`. No structural change needed.

### Status / sync metadata

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `STAT` | string | `catalog.items.status` | Counterpoint values are codes; Canary uses words. Adapter mapping table. |
| `STAT_DAT` | datetime | — | **Missing** — status-change date. Promote: `status_changed_at` column. |
| `LST_MAINT_DT` | datetime | `catalog.items.updated_at` | None (Counterpoint's last-maintained = Canary's updated_at) |
| `LST_MAINT_USR_ID` | string | — | **Missing** — who last touched it. Add `updated_by` (uuid → users) column when user table lands |
| `RS_UTC_DT` | datetime | — | **Missing** — record-sync timestamp; the adapter's high-water mark for incremental polls. Store as `attributes.rs_utc_dt` (sync-bookkeeping; not a domain field) |
| `RS_STAT` | int | — | **Missing** — record-sync status code; same as above |

### Pricing (REST surface — minimal)

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `PRC_1` | number | — | Price tier 1 — see Pricing section |
| `REG_PRC` | number | `catalog.items.default_price` | Canary's `default_price` ≈ Counterpoint's `REG_PRC` |
| `LST_COST` | number | `catalog.items.default_cost` | Canary's `default_cost` ≈ Counterpoint's `LST_COST` |
| `IS_TXBL` | string ("Y"/"N") | `catalog.items.tax_class` (text) | Counterpoint = boolean; Canary = tax-class lookup. Adapter sets tax_class to a default tenant taxable class when `IS_TXBL='Y'`, NULL otherwise. |
| `IS_DISCNTBL` | string ("Y"/"N") | — | **Missing** — discountable flag. Add `is_discountable boolean DEFAULT true`. |

The 10-layer pricing precedence does **not** appear in IM_ITEM. Only `PRC_1` and `REG_PRC` come over — see Pricing section below.

### Inventory metadata (on item)

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `QTY_DECS` | int | — | **Missing** — qty decimals (0 for whole-unit items, 2-4 for weighed). Promote: `qty_decimals smallint DEFAULT 0`. |
| `PRC_DECS` | int | — | **Missing** — price decimals. Promote: `price_decimals smallint DEFAULT 2`. |
| `STK_UNIT` | string | `catalog.items.unit_of_measure` | Direct match. |
| `PREF_UNIT` | string | — | **Missing** — preferred unit (display/order default different from stocking). Add `preferred_unit_of_measure` column. |
| `IS_WEIGHED` | string ("Y"/"N") | `catalog.items.weighable` | Direct match (boolean coerce). |
| `LST_RECV_DAT` | datetime | — | **Missing** — last received date. Useful operational metadata. Add `last_received_at` column OR carry in `attributes`. |

### Vendor

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `ITEM_VEND_NO` | string | (via `catalog.item_vendors.vendor_sku`) | Counterpoint exposes this on IM_ITEM (denormalized convenience); Canary keeps it on the link table. Adapter writes to `item_vendors.vendor_sku`. |

The full vendor link comes via the `VendorItem` schema (separate `GET /VendorItem/{VendorNo}/Item/{ItemNo}` endpoint):

| VendorItem field | Canary equivalent |
|---|---|
| `VEND_NO` | `catalog.vendors.vendor_code` |
| `ITEM_NO` | `catalog.items.sku` |
| `VEND_ITEM_NO` | `catalog.item_vendors.vendor_sku` |
| `VEND_DESCR` | — (add `vendor_description` to `catalog.item_vendors`) |
| `LST_COST` | `catalog.item_vendors.last_cost` (already has) |
| `ORD_UNIT` | — (add `order_unit_of_measure` to `catalog.item_vendors`) |

**Gap:** add `vendor_description` and `order_unit_of_measure` columns on `catalog.item_vendors`. Both are operationally meaningful — the order unit drives PO unit conversions, the vendor description is what shows up on the vendor's invoice.

### Ecommerce

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `IS_ECOMM_ITEM` | string ("Y"/"N") | — | **Missing** — flag for "publish to ecom" |
| `ECOMM_LST_PUB_STAT` | string | — | **Missing** — last publish status |
| `EC_ITEM_DESCR.HTML_DESCR` | string | — | **Missing** — rich-text HTML description for ecommerce |

**Gap:** the ecommerce fields live in a parallel ecommerce system (Counterpoint EC). Canary's `internal/ecom` package is mostly stubbed today. Recommend deferring these fields until the ecommerce surface lights up — no value carrying them in `catalog.items` if nothing reads them.

### Garden-center / specialty flags

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `MIX_MATCH_COD` | string | — | **Missing** — mix-and-match group code. See Discounts section. |
| `IS_ADM_TKT` | string | — | **Missing** — admission ticket flag |
| `IS_BOM_PAR` | string | (via `catalog.item_packs`) | Canary's `item_packs` table covers the parent-of-bill-of-materials concept |
| `IS_KIT_PAR` | string | (via `catalog.item_packs.pack_type='kit'`) | Canary's `item_packs.pack_type` enum supports 'kit' |

**Gap:** `MIX_MATCH_COD` is a real concept (group items together for "buy any 3 for $10" deals). Add column. `IS_ADM_TKT` is niche — defer.

### Compliance

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `IS_FOOD_STMP_ITEM` | string ("Y"/"N") | `catalog.items.food_stamp_eligible` | Direct match. |

(Counterpoint's REST does NOT expose age_restriction, hazardous, controlled-substance, allergen — those live in profile codes 4-20 in the back-office, not in REST. Bart's team integration may augment these via SQL Server reads. **Open question.**)

### Children / nested

| Counterpoint structure | Canary equivalent | Gap |
|---|---|---|
| `IM_ITEM_NOTE[]` (array of free-text notes) | — | **Missing** — add `catalog.item_notes` table OR carry in `attributes.notes` array. Notes drive POS prompts (showing "Check ID for tobacco" at scan); deferring this loses operational behavior. |
| `EC_ITEM_DESCR` (single embedded) | — | Defer with ecommerce fields. |

---

## IM_INV — per-location inventory snapshot

`GET /Item/{ItemNo}/Inventory/{LocId}` returns this.

| Counterpoint field | Type | Canary equivalent | Gap |
|---|---|---|---|
| `ITEM_NO` | string | (key) | None |
| `LOC_ID` | string | (key — `inventory.location_id`) | None |
| `QTY_ON_HND` | number | `inventory.positions.qty_on_hand` | Canary already has |
| `QTY_AVAIL` | number | `inventory.positions.qty_available` | Same |
| `QTY_ON_PO` | number | `inventory.positions.qty_on_po` | Same |
| `QTY_COMMIT` | number | `inventory.positions.qty_committed` | Same |
| `MIN_STK` | number | (replenishment params — separate domain, not in catalog) | **Gap noted in GRO-877** — replenishment params don't live in `catalog.*`. Whatever module owns them needs to ingest these. |
| `MAX_STK` | number | (same) | Same |
| `AVG_COST` | number | `inventory.positions.avg_cost` | Should already be there |
| `LST_COST` | number | (denormalized from item) | Already covered |

**Gap:** `MIN_STK` / `MAX_STK` per location is the replenishment parameter source. Whichever module owns `replenishment.params` needs to consume IM_INV to seed these. **This is open question #2** — does the seed flow happen via `internal/adapters/counterpoint` parser writing to a replenishment store, or does the replenishment module pull directly?

---

## IM_CATEG — categories

```
IM_CATEG:
  CATEG_COD: string
  DESCR: string
  Subcategories: [
    { CATEG_COD, SUBCAT_COD, DESCR }
  ]
```

| Field | Canary equivalent | Gap |
|---|---|---|
| `CATEG_COD` | `catalog.product_categories.code` | None |
| `DESCR` | `catalog.product_categories.name` | None |
| `Subcategories[].SUBCAT_COD` | `catalog.product_categories.code` (child row) | Adapter inserts as `parent_id` link |
| `Subcategories[].DESCR` | `catalog.product_categories.name` (child row) | Same |

**Gap:** zero. `catalog.product_categories` already supports parent-child via `parent_id` + ltree. The adapter pattern for ingesting IM_CATEG:

```
for each IM_CATEG row:
  upsert parent: parent_id=NULL, code=CATEG_COD, level=1
  for each Subcategory:
    upsert child: parent_id=<parent.id>, code=SUBCAT_COD, level=2
```

No schema change needed.

---

## SN_SER — serial number tracking

`GET /Item/{ItemNo}/Serial/{SerialNo}` and `GET /Item/{ItemNo}/Serials/Location/{LocId}` expose this.

```
SN_SER:
  ITEM_NO: string
  SER_NO: string
  LOC_ID: string
  STAT: string             (status: in-stock / sold / etc.)
  RECV_DAT: datetime
  SLD_DAT: datetime
  COST: number
```

| Canary state today |
|---|
| **No serial tracking schema exists.** |

**Gap:** add `catalog.item_serials` table:

```sql
CREATE TABLE catalog.item_serials (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id   UUID NOT NULL REFERENCES app.tenants(id),
    item_id     UUID NOT NULL REFERENCES catalog.items(id),
    serial_no   TEXT NOT NULL,
    location_id UUID,
    status      TEXT NOT NULL,
    received_at TIMESTAMPTZ,
    sold_at     TIMESTAMPTZ,
    cost        NUMERIC(12,4),
    UNIQUE (tenant_id, item_id, serial_no)
);
```

Plus a `tracking_method` column on `catalog.items` (`none` | `serial` | `lot`) so the read path knows whether to look at this table.

**Bart's-stores priority:** garden centers don't generally serial-track plants. Hardware stores DO serial-track high-value items (chainsaws, generators, power tools). **P1 — important for hardware-store customers, deferrable for pure garden centers.**

---

## Pricing — the real story

Counterpoint's REST surface exposes only `PRC_1` and `REG_PRC` on IM_ITEM. The 10-layer pricing precedence (per `Brain/wiki/ncr-counterpoint-functional-decomposition.md` §12) lives in:

- **Item record** — `REG_PRC`, `PRC_1` (REST exposes)
- **Item record / Prices tab** — location-specific prices (NOT in REST IM_ITEM)
- **Special Prices form** (`frmsipricesnt`) — date + qty triggered (NO REST endpoint)
- **Contract Prices form** — customer-specific (NO REST endpoint)
- **Planned Promotions form** — date-bounded campaigns (NO REST endpoint)
- **Mix-and-match codes + rules** — only the `MIX_MATCH_COD` flag is in REST
- **Price Breaks table** — quantity tiers (NO REST endpoint)
- **Customer category → price-list assignment** — derived from CustomerControl

**The implication for Canary:**

The catalog adapter can read `REG_PRC` and `PRC_1`, period. Everything else surfaces only as **outputs in PS_DOC_LIN_PRICE** when a transaction lands — i.e., the price the customer actually paid, with the rule code that fired.

Canary cannot replicate Counterpoint's pricing engine from REST. Canary CAN observe what Counterpoint priced things at, after the fact, by ingesting transactions. The prediction gap is real.

**Recommendation for `catalog.items` schema:**

- Keep `default_price` as Canary's `REG_PRC` equivalent (already there)
- Add `price_tier_1` numeric column (PRC_1 equivalent) — the second exposed price level
- Add a `pricing.observed_price_rules` table populated by the transaction adapter, NOT the catalog adapter, that captures `(item_id, customer_class, rule_code, observed_price, observed_at)` tuples. Over time this becomes Canary's empirical view of what Counterpoint's pricing engine did.

This is a **P0 architectural call.** The schema-evolution dispatch needs to decide whether Canary models a pricing engine OR observes Counterpoint's outputs. **Recommend: observe.** Canary's value-add is intelligence, not pricing-rule replacement.

---

## Tracking flags + tables

| Concept | Counterpoint REST | Canary today | Gap |
|---|---|---|---|
| Serial tracking | `SN_SER` schema, 2 endpoints | None | P1 — add `catalog.item_serials` (above) |
| Lot tracking | Not in REST | None | P2 — Counterpoint's lot tracking is in back-office only; defer |
| Tag tracking | Not in REST (Counterpoint Hardware add-on) | None | P3 — niche, defer |
| `TRK_METH` field | On IM_ITEM | None | P1 — add `tracking_method` text column on `catalog.items` |

---

## Item types — the actual enum

Counterpoint's `ITEM_TYP` codes (single character):
- `I` — Inventory
- `N` — Non-inventory (services, fees, comments — surfaceable at POS but no SOH)
- (other codes per the API doc; sample doesn't enumerate all)

Canary's `catalog.items.item_type` enum:
- `standard | service | giftcard | tare | pack | bundle`

**Gap:** the adapter mapping table:

| Counterpoint `ITEM_TYP` | Canary `item_type` |
|---|---|
| `I` | `standard` |
| `N` | `service` (default — narrow if richer Counterpoint codes can be distinguished) |
| `I` + `IS_KIT_PAR='Y'` | `bundle` |
| `I` + `IS_BOM_PAR='Y'` | `bundle` (same target; flag distinguishes assembly vs simple bundle) |
| `I` + `IS_WEIGHED='Y'` + `unit='LB'/'KG'/'OZ'` | `standard` (weighable is a separate flag, not item_type) |
| `I` + `IS_ADM_TKT='Y'` | `standard` (Canary doesn't have an admission-ticket type today; defer) |

**Gap:** Canary's `tare` enum value has no Counterpoint REST equivalent that I've found. May need to consult Bart's team — is tare modeled differently in Counterpoint, or just a back-office concept?

---

## Alternate items / substitutions

**Not in IM_ITEM. Not in any REST schema I found.**

Counterpoint's substitution model lives in back-office tables (likely `IM_ALT_ITEM` or similar — back-office only). REST does not expose alternate-item lookup.

**Bart's-stores priority:** P2. Substitutions are a nice-to-have for "we're out of A, suggest B" workflows. Not blocking for catalog parity.

**Gap:** none in the REST integration path. If we want the back-office substitution data, requires SQL Server direct read.

---

## Kit composition

Counterpoint exposes `IS_BOM_PAR` and `IS_KIT_PAR` flags on IM_ITEM but **the kit composition itself is not in REST.** The component list lives in back-office tables (`IM_BOM_LIN` or similar).

Canary's `catalog.item_packs` table covers the parent-of-pack relationship and component list:

```sql
CREATE TABLE catalog.item_packs (
  pack_item_id      uuid -- the parent kit
  component_item_id uuid -- the child
  quantity          numeric
  pack_type         text -- 'case' | 'bundle' | 'kit' | 'mix'
)
```

**Gap:** the schema is there. The data isn't reachable via REST. **P2** — populate via SQL Server direct read OR by post-creation manual entry in Canary's UI when kits are first sold (lazy population from PS_DOC_LIN ingestion).

---

## Sync metadata + multi-company

Counterpoint REST exposes `RS_UTC_DT` (record-sync UTC datetime) and `RS_STAT` (sync status) on IM_ITEM. These are **adapter-only** fields — Canary doesn't model them in the domain. Store in `attributes.counterpoint_sync` JSONB block:

```json
{
  "counterpoint_sync": {
    "rs_utc_dt": "2026-05-08T12:00:00Z",
    "rs_stat": 1,
    "company_alias": "main"
  }
}
```

**Multi-company:** Counterpoint REST routes requests by `<company>.<user>`. A single Canary tenant may have N Counterpoint companies (per `ncr-counterpoint-api-reference.md` §"Multi-company is real"). Add `company_alias` to the sync block AND track per-(tenant, company) credentials in `app.pos_tenant_credentials` (which already exists).

---

## Prioritized migration list

Sequenced by which Counterpoint-source field has operational impact for Bart's stores, with confidence drawn from the REST schema (high confidence — these are the fields the adapter will see).

### P0 — blocks any Counterpoint integration shipping

| # | Gap | Schema change | Why |
|---|---|---|---|
| 1 | Subcategory hierarchy | Adapter writes 2-row category insert (parent + child) using existing `product_categories.parent_id` | No schema change needed; adapter contract |
| 2 | `addl_descr_1/2/3` (3 alt-language description fields) | Add to `catalog.items.attributes.descriptions[]` JSONB | Plant common/botanical/Spanish names without these are unusable |
| 3 | `tracking_method` | Add `tracking_method TEXT NOT NULL DEFAULT 'none'` to `catalog.items` | Read path needs this to know whether to look at `item_serials` |
| 4 | `qty_decimals`, `price_decimals` | Add as smallint columns on `catalog.items` | POS quantity entry breaks without these for weighable items |
| 5 | Item-type code mapping (Counterpoint ITEM_TYP → Canary `item_type`) | Adapter mapping table; no schema change | Without this, every imported item lands as `standard` |
| 6 | Pricing observation strategy | Add `pricing.observed_price_rules` table; document that catalog adapter does NOT replicate Counterpoint's pricing engine | The 10-layer pricing engine cannot be replicated from REST; observation is the strategy |

### P1 — operationally meaningful for Bart's stores within first 90 days

| # | Gap | Schema change | Why |
|---|---|---|---|
| 7 | `catalog.item_serials` table + REST endpoints | New table per spec above | Hardware stores serial-track tools; required for warranty / theft recovery |
| 8 | `mix_match_code` | Add `mix_match_code TEXT` column on `catalog.items` | Garden-center mix-and-match deals are widespread |
| 9 | `is_discountable` | Add `is_discountable BOOLEAN NOT NULL DEFAULT true` | Receipt-paper, warranty cards, etc. should not be discountable; UI needs the flag |
| 10 | `preferred_unit_of_measure` | Add column | Display default sometimes differs from stocking unit (sell by ft, stock by case-of-100) |
| 11 | Vendor description + order UOM on `item_vendors` | Add `vendor_description` and `order_unit_of_measure` columns | PO conversions need order UOM; vendor invoices need their description for matching |
| 12 | Item notes (POS prompts) | New `catalog.item_notes` table OR `attributes.notes[]` array | "Check ID" / "Verify size" prompts at POS |
| 13 | Status-change date | Add `status_changed_at TIMESTAMPTZ` column | Audit + lifecycle reporting |
| 14 | `last_received_at` | Add column | Operational metadata; useful for dead-stock detection |
| 15 | `attr_cod_1`, `attr_cod_2` | Carry in `attributes.attr_cod_1/2` JSONB | User-defined dimensions; flexible; promote to columns only if a specific tenant uses them heavily |
| 16 | Multi-company sync metadata | `attributes.counterpoint_sync` JSONB block | Support N-companies-per-tenant |

### P2 — nice-to-have parity, defer until Phase 2

| # | Gap | Schema change | Why |
|---|---|---|---|
| 17 | Lot tracking | New `catalog.item_lots` table | Counterpoint REST doesn't expose lot data; SQL Server direct read needed |
| 18 | Tag tracking (Counterpoint Hardware add-on) | New table | Niche; defer |
| 19 | Alternate items / substitutions | New `catalog.item_alternates` table | Not in REST; SQL Server read needed |
| 20 | `is_admission_ticket` | Add flag | Niche use case |
| 21 | Ecommerce fields (`is_ecomm_item`, `ecomm_lst_pub_stat`, `EC_ITEM_DESCR`) | Add when ecom surface lights up | No reader today; deferred |
| 22 | Kit/BOM composition | Populate `catalog.item_packs` from SQL Server OR lazy from PS_DOC_LIN | Not in REST |
| 23 | Status lifecycle alignment (GRO-877 OQ #1) | Schema migration to add `draft`, `on_trial`, `phase_out` statuses | Counterpoint just has `active` / `inactive`; the richer Canary lifecycle is additive over what Counterpoint does, not a parity requirement |

---

## Open questions for Bart's team

These need a 30-min call. Ordered by leverage:

1. **REST-only or REST + SQL Server?** Does Bart's integration team rely on REST for catalog (in which case the gaps above are real) or also read SQL Server directly (in which case grid items, multi-UOM, multi-barcode, lot tracking, alternate items, kit composition, full attribute set, full profile codes, location-specific pricing, special prices, contract prices, promotional prices, price breaks all become reachable)? **This is the highest-leverage question** — answer determines whether Canary's catalog adapter is REST-bounded or back-office-altitude.

2. **Replenishment param ownership.** `IM_INV.MIN_STK` and `IM_INV.MAX_STK` are in REST. Does Canary's catalog adapter populate replenishment params, or does the replenishment module poll IM_INV directly?

3. **Item-type code enumeration.** REST sample shows `I = inventory, N = non-inventory, etc.` — what's the full enumeration? (`G` for gift card? `M` for modifier? `T` for tare?)

4. **Grid items in practice.** Counterpoint's back-office Grid tab generates separate `ITEM_NO` rows per cell. Do Bart's stores actually use grid items, or do operators stick to flat SKUs? (Affects whether Flow C's variant-matrix builder needs multi-dim support day-one.)

5. **Multi-barcode reality.** REST exposes only `BARCOD` (single). Do Bart's stores need multi-barcode-per-item (case barcode + each barcode + supplier-specific code)? If yes — does the integration read `IM_ITEM_BARCOD` directly from SQL?

6. **Tare modeling.** Canary has `item_type='tare'`. What does Counterpoint do for tare (deli scale, butcher scale)? Profile codes, weighable flag + special category, or something else?

7. **Status enumeration.** The REST sample has `STAT` but doesn't enumerate values. Active / inactive / discontinued / hold? This pins down the GRO-877 OQ #1 (status lifecycle alignment).

8. **Multi-company adoption rate.** Does the typical Bart's-stores tenant run one Counterpoint company per merchant, or multiple (chain with subsidiary entities)? Affects how aggressive the multi-company plumbing needs to be in the adapter.

---

## What this audit revises in earlier cards

- **GRO-877 / `canary-item-setup-screen-decomp.md` Flow C variant builder.** The audit confirms grid items are **flat ITEM_NO rows**, not a hierarchical structure. Flow C's variant matrix UI is a UI construct over flat rows — the data model doesn't need hierarchical changes. The screen decomp is correct as-is; the schema assumption (one parent style + N child SKUs) holds. Update: the parent style ID lives in `attributes.style_id` JSONB OR can be elided entirely (sibling rows share `attributes.attr_cod_1` = "Men's Oxford" and that's the grouping key).

- **GRO-877 OQ #1 (status lifecycle alignment).** Counterpoint's REST surface has `STAT` as a code, no Draft/Active/Trial/Phase-Out structure. The richer Canary lifecycle is additive — Counterpoint doesn't model it but doesn't preclude it. Recommend evolving Canary schema; treat Counterpoint sync as `STAT='A'` → Canary `active`, `STAT='I'` → Canary `inactive`, with Canary's Draft / On-Trial / Phase-Out as Canary-side states that don't round-trip.

- **GRO-877 OQ #2 (`catalog.import_jobs` table).** Confirmed not in Counterpoint REST. `import_jobs` is purely a Canary concept for the supplier-CSV flow. Schema migration when Flow B ships.

- **GRO-877 OQ #3 (replenishment params homelessness).** Confirmed: `MIN_STK` / `MAX_STK` come from `IM_INV`, not `IM_ITEM`. Belongs in the replenishment module, not catalog. Original recommendation in GRO-877 (defer replenishment to its own dispatch) holds.

- **`canary-item-master-and-catalog.md` "5-level merchandise hierarchy" framing.** The Brain card cited Department / Class / Subclass etc. as Counterpoint's depth. **This is true for the back-office UI** (via Profile Codes 1-5 + Attribute Codes 1-6). It is **NOT true for REST**, which exposes 2 levels (Category + Subcategory) plus 2 attribute codes. Canary's 2-level `product_categories` aligns to REST. Promoting profile codes to first-class hierarchy levels requires either a Counterpoint REST extension that doesn't exist, or SQL Server direct reads.

---

## See also

- [[counterpoint-product-state-2026]] — product architecture, October 2026 forcing function, multi-company reality
- [[ncr-counterpoint-api-reference]] — endpoint inventory, caching policy, cross-cutting findings
- [[ncr-counterpoint-document-model]] — transaction-side schema (PS_DOC_*); catalog audit's transaction-side counterpart
- [[ncr-counterpoint-functional-decomposition]] — the back-office UI depth (95 forms; what's NOT in REST)
- [[canary-item-master-and-catalog]] — the parent retail-substrate card; revised "5-level" framing per this audit
- [[canary-item-setup-screen-decomp]] — the screens this audit's findings inform
- `docs/sdds/canary/ncr-counterpoint-openapi.yaml` — the authoritative source for IM_ITEM, IM_INV, IM_CATEG, SN_SER, VendorItem schemas
- `CanaryGo/internal/adapters/counterpoint/parser.go` — current adapter (transaction-side; catalog-side is open)
- `CanaryGo/deploy/schema/02_catalog_items.sql` — Canary's catalog floor
- GRO-880 — this card's source dispatch
