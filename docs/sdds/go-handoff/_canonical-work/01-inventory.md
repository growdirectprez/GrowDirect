# Inventory — Source Material for Canonical Data Model

**Working file. Chunk 1 output. Not for promotion.** Branch: `gd-canonical-data-model`.

Catalogues every entity-mention across every source. Anchors the entity-by-entity reconciliation walk that follows. Built per the founder's directive: *"go table by table by entity in the GSLM and produce the canonical."*

## Sources

| # | Source | Path | Era | Layer | Entities |
|---|---|---|---|---|---|
| S1 | **GSLM3** (Global Store Logical Model) | `~/CRDM-recovery/sql/Logical-Model-2009-12-14.sql` | 2009-12, Walmart Int'l | Master data / reference | **43** |
| S2 | **CRDM POS 1.8 Data Dictionary** | `~/CRDM-recovery/data-dictionaries/CRDM-1.8-Data-Dictionary.md` | ~2013, Secure Store 3.2 | POS operational | **25** |
| S3 | **CRDM POS 1.7.2 Data Dictionary** | `~/CRDM-recovery/data-dictionaries/CRDM-1.7.2-Data-Dictionary.md` | ~2012 | POS operational | **27** |
| S4 | **Canary Go data-model.md** (active) | `docs/sdds/go-handoff/data-model.md` | 2026, GA-track | Canary platform + commercial | **~116** (65 detailed + 51 listed) |
| S5 | **Canary Python data-model.md** (frozen) | `docs/sdds/canary/data-model.md` | 2025, v0-python-prototype | Earlier Canary draft | ~95 (similar shape, less detail) |
| S6 | Recovery DDL fragments | `~/CRDM-recovery/sql/*.sql` (excl. Logical-Model) | 2010-2015 | Misc operational + reference | ~20 |

**Authority order for canonical reconciliation:**
1. **GSLM (S1)** — master/reference layer anchor (founder's own design)
2. **Canary Go data-model (S4)** — active platform spec, supersedes Python proto
3. **CRDM 1.8 (S2)** — POS operational layer; preferred over 1.7.2 where they overlap (later schema, same lineage)
4. **CRDM 1.7.2 (S3)** — only consulted for entities dropped in 1.8 (Customer, Repair) or to surface evolution deltas
5. **Python proto (S5)** — semantic reference only; no DDL pulls
6. **Recovery DDL fragments (S6)** — pulled selectively for specific reference tables (Vendors, Locations) and platform precursors (CaseCentre, Camera_Reference)

## S1 — GSLM3 entities (43, anchor)

Grouped by their natural domain in the GSLM schema:

### Catalog / Merchandise hierarchy (8)
`BusinessDivisions` · `Departments` · `Classes` · `SubClasses` · `Finelines` · `Sections` · `MerchandiseType` · `Merchandise` · `MerchandiseAttributesLanguages`

### Item / SKU / Style (10)
`SKUItems` · `SKUItemVendors` · `Styles` · `StyleVariants` · `StyleVariantValues` · `StyleVariantGroups` · `StyleVariantGroupAssignments` · `ArticleItems` · `ArticleTypes` · `Ingredients`

### Pack / multi-unit (3)
`PackItems` · `PackItemBreakout` · `PackBreakout`

### Sales outlet / store structure (8)
`SalesOutlets` · `SalesFloors` · `SalesFloorsInSalesOutlet` · `SalesOutletDepartments` · `SalesOutletAssets` · `SalesOutletAssetLocation` · `SalesOutletHolidays` · `SalesOutletSKUItemPromoCompDetails`

### In-store stock placement (2)
`SKUItemsInSalesOutlets` · `PackItemsInSalesOutlets`

### Vendor (1)
`Vendors`

### Tax (2)
`Taxes` · `ItemTaxesInSalesOutlets`

### Promotion (5)
`Promotions` · `PromotionComponents` · `PromotionComponentDetails` · `PromotionThresholds` · `ThresholdIntervals`

### Planogram (1)
`Planogram`

### User-defined attribute (2)
`UserDefinedAttributes` · `UserDefinedAttributeValues`

> **Critical observation:** GSLM3 is **purely master data and reference** — *what* is sold, *where*, by *whom*, under *what* promotion, taxed *how*. **It does not contain transactions, customers, employees, payments, inventory-on-hand, or any operational state.** That's CRDM's role. The canonical superset must walk GSLM for master data and CRDM POS for operational, then add Canary platform layers on top.

## S2/S3 — CRDM POS entities (25 in 1.8, 27 in 1.7.2)

All prefixed `CRDM_*`. Grouped by transaction role:

### Transaction core (3)
`CRDM_Header` · `CRDM_Item` · `CRDM_FastFact` (pre-aggregated transaction summary, ~110 columns)

### Transaction subtypes (5)
`CRDM_Tender` · `CRDM_TransactionDiscount` · `CRDM_ItemDiscount` · `CRDM_ItemFastFact` · `CRDM_RecalledTransaction`

### Money / payment subordinates (4)
`CRDM_AccountPayment` · `CRDM_GiftCard` · `CRDM_PointsCoupon` · `CRDM_PaidIn_PaidOut`

### Operational subordinates (4)
`CRDM_StaffDiscount` · `CRDM_OperatorAction` · `CRDM_AgeInformation` · `CRDM_NotOnFile`

### Inventory movement (5)
`CRDM_GoodsReceived` · `CRDM_StockAdjustment` · `CRDM_SupplierReturn` · `CRDM_Transfer` · `CRDM_WebItemReturn`

### Cash management (1)
`CRDM_CashOfficeSafe`

### Receipt + ETopUp + Loyalty (3)
`CRDM_Receipt` · `CRDM_ETopUp` · `CRDM_LoyaltyCard`

### Dropped between 1.7.2 → 1.8 (2 — only in 1.7.2)
`CRDM_Customer` · `CRDM_Repair`

> **Observation:** CRDM is operational POS event capture — every entity is rooted in a transaction (TransactionID/CheckPointID/StoreNo/POSNo/TicketNo/TradingDay/CashierNo skeleton). CRDM_Customer was likely dropped because customer master moved to a separate system; CRDM_Repair was a vertical-specific feature retired.

## S4 — Canary Go data-model.md entities (~116, by schema/domain)

### app schema (~60 tables)

| Domain | Tables |
|---|---|
| Identity (19) | organizations · merchants · merchant_settings · users · roles · user_roles · employees · locations · location_hierarchy · customers · products · square_oauth_tokens · source_systems · merchant_sources · external_identities · user_employee_links · employee_location_assignments · gift_cards · bank_accounts |
| Chirp / detection (2) | detection_rules · merchant_rule_config |
| Alert (4) | alerts · alert_history · notification_log · notification_schedule |
| Owl / observability (4) | owl_sessions · owl_findings · owl_merchant_memory · owl_action_log |
| Fox / case mgmt (7) | fox_cases · fox_case_alerts · fox_case_timeline · fox_case_actions · fox_evidence · fox_evidence_access_log · fox_subjects |
| Hawk / incident (8) | hawk_incident_types · hawk_sources · hawk_cases · hawk_subjects · hawk_actions · hawk_timeline · hawk_compliance_obligations · hawk_cards |
| Bull (Phase 3 stub) | (planned, no migration) |
| Webhook (3) | webhook_events · schema_fingerprints · schema_drift_alerts |
| UI/BFF (5) | feature_flags · merchant_feature_flags · app_config · card_profiles · blocked_entities |
| RaaS (2) | namespace_registrations · namespace_aliases |
| Vault (1) | vault_memories |
| Subscription/Transfer (2) | subscriptions · transfer_orders |
| Cross-cutting (2) | audit_log · interest_signups |

### sales schema (~30 tables)

| Domain | Tables |
|---|---|
| Transaction Core (4) | transactions · transaction_line_items · transaction_tenders · refund_links |
| Order Detail (6) | (listed, not all detailed in this version) |
| Cash Management (2) | cash_drawer_shifts · cash_drawer_events |
| Gift Card & Loyalty (3) | (listed) |
| Disputes & Payouts (3) | (listed) |
| Inventory & Labor (2) | (listed) |
| Terminal (2) | (listed) |
| Pipeline Infrastructure (3) | (listed) |
| Event Journal (5) | (listed) |

### metrics schema (~21 tables)

Fact (6) · Dimension (3) · ML Feature Store (3) · Risk Scoring (2) · Baselines & Scorecards (7)

### memory schema (2)

`memory.alx_memories` · `memory.alx_sessions`

### ledger schema (3)

`ledger.rib_batches` · `ledger.stock_ledger_entries` · `ledger.ilwac_positions`

> **Schema strategy** (per S4): schema-per-tenant for sales, single shared `app` schema for cross-tenant control plane. Multi-tenant isolation lives at the schema boundary.

## S6 — Recovery DDL fragments (selective)

| File | Tables | Why included |
|---|---|---|
| `wmt-ref-location-create.sql` | `Ref_LocationHierarchy` | Reference hierarchy for store grouping (banner/region/district) — pull during Store/Location domain |
| `CreateTablesAndProcedures.sql` | `Reference_*` (5 tables) | Reference data: AverageBrandItemRetailCost, HR, LOCATION, States, ZoneBrandMatch — pull selectively |
| `CaseCentre.sql` | `Case_Custom` | Case management precursor — already superseded by Canary Fox; consult for column ideas |
| `Video.sql` + `Video-CaseManagement.sql` | `Camera_Reference`, `Video_Queue`, `Video_Request`, `Case_Case_Case_Video` | Evidence/video chain precursor — consult during Q (LP) module Fox section |
| `RxAggTables.sql` + `RXScorecard*.sql` | `Rx*` (5 tables) | Pharmacy vertical aggregates — consult only if pharmacy vertical is in scope |
| `SAS-Scorecard*.sql` | `SASScorecardPOSAggregate` | POS aggregate — consult during metrics layer |
| `create-scorecard-base.sql` | `scorecards.Scorecard_StoreNo_CashierNo` | Cashier scorecard pattern — relevant for Q (LP) baselines |
| `3-Notifying-Table-Changes.sql` | `Notification_Checkpoint`, `Notification_SummaryCheckpoint` | Change-notification pattern — superseded by Canary webhook_events but consult |
| `CRDM-MaxID-Table-Changes.sql` | `MaximumTx` | TransactionID generator — pattern reference for sequencing |
| `Create-Dyno-Tab*.sql` | `Dyno_Tabs`, `Dyno_TabUserPreference` | UI dynamic-tab — superseded by Canary feature_flags pattern; consult if useful |

## Cross-source alias map (initial — to be expanded per chunk)

Anchors the canonical reconciliation. For each row, **canonical column convention** = lowercase snake_case, Postgres-typed, schema-qualified.

| Canonical entity | GSLM (S1) | CRDM 1.8 (S2) | Canary go-handoff (S4) | Module owner |
|---|---|---|---|---|
| `m.products` (item master) | `SKUItems` + `Styles` + `StyleVariants` | (referenced by ArticleID in `CRDM_Item`) | `app.products` | M (Merchandising) |
| `m.product_taxonomy` (department/class/etc.) | `BusinessDivisions` → `Departments` → `Classes` → `SubClasses` → `Finelines` → `Sections` | — | (not present — gap) | M |
| `m.vendors` | `Vendors` + `SKUItemVendors` | — | (not present — gap) | M |
| `m.taxes` | `Taxes` + `ItemTaxesInSalesOutlets` | (`TaxAmount` columns on Header/Item) | (not present — gap) | F or M |
| `m.promotions` | `Promotions` + `PromotionComponents` + `PromotionComponentDetails` + `PromotionThresholds` + `ThresholdIntervals` | (`PromotionID` referenced from `CRDM_ItemDiscount`/`CRDM_TransactionDiscount`) | (not present — gap) | P (Pricing) |
| `m.packs` | `PackItems` + `PackItemBreakout` + `PackBreakout` | — | (not present — gap) | M |
| `m.style_variants` | `StyleVariants` + `StyleVariantValues` + `StyleVariantGroups` + `StyleVariantGroupAssignments` | — | (subsumed in `app.products` attributes JSON?) | M |
| `m.ingredients` | `Ingredients` | — | (gap; matters for food/grocery/pharmacy verticals) | M |
| `m.user_defined_attrs` | `UserDefinedAttributes` + `UserDefinedAttributeValues` | — | (gap; partially served by `app.merchant_settings` JSON) | M |
| `a.locations` (sales outlets) | `SalesOutlets` | (referenced by `StoreNo`) | `app.locations` + `app.location_hierarchy` | A (Asset) |
| `a.location_hierarchy` | (implicit in SalesOutlets columns) | — | `app.location_hierarchy` + `Ref_LocationHierarchy` (S6) | A |
| `a.location_floors_sections` | `SalesFloors` + `SalesFloorsInSalesOutlet` + `Sections` | — | (gap) | A or S |
| `a.location_assets` | `SalesOutletAssets` + `SalesOutletAssetLocation` | — | (gap; partially `app.terminals`) | A or N |
| `a.location_holidays` | `SalesOutletHolidays` | — | (gap) | A |
| `s.planogram` | `Planogram` | — | (gap) | S (Space) |
| `s.shelf_placement` | `SKUItemsInSalesOutlets` + `PackItemsInSalesOutlets` | — | (gap) | S |
| `t.transactions` | — | `CRDM_Header` | `sales.transactions` | T (Transaction Pipeline) |
| `t.transaction_line_items` | — | `CRDM_Item` | `sales.transaction_line_items` | T |
| `t.transaction_tenders` | — | `CRDM_Tender` | `sales.transaction_tenders` | T |
| `t.transaction_discounts` | — | `CRDM_TransactionDiscount` + `CRDM_ItemDiscount` | (in line items?) | T |
| `t.transaction_summary` (FastFact) | — | `CRDM_FastFact` (~110 cols) + `CRDM_ItemFastFact` | `metrics.fact_*` (similar role) | T → metrics |
| `t.gift_card_events` | — | `CRDM_GiftCard` + `CRDM_PointsCoupon` | `app.gift_cards` (master) + (events gap) | T |
| `t.account_payments` | — | `CRDM_AccountPayment` | (gap) | F |
| `t.cash_drawer` | — | `CRDM_CashOfficeSafe` + `CRDM_PaidIn_PaidOut` | `sales.cash_drawer_shifts` + `sales.cash_drawer_events` | T or F |
| `t.recalled_transactions` | — | `CRDM_RecalledTransaction` | (gap) | T |
| `t.receipt` | — | `CRDM_Receipt` | (typically derived, not stored — confirm) | T |
| `c.customers` | — | `CRDM_Customer` (1.7.2 only) | `app.customers` | C (Customer) |
| `c.loyalty` | — | `CRDM_LoyaltyCard` + `CRDM_PointsCoupon` | (gap) | C |
| `c.age_verification` | — | `CRDM_AgeInformation` | (gap; matters for alcohol/tobacco/Rx) | C or Q |
| `e.staff_discount` | — | `CRDM_StaffDiscount` | (gap) | C/L (depending on framing) |
| `e.operator_actions` | — | `CRDM_OperatorAction` | (relates to `app.audit_log`?) | Q (LP) |
| `e.not_on_file` | — | `CRDM_NotOnFile` (items scanned without master) | (gap; LP signal) | Q |
| `d.goods_received` | — | `CRDM_GoodsReceived` | (gap) | D (Distribution) |
| `d.stock_adjustments` | — | `CRDM_StockAdjustment` | `ledger.stock_ledger_entries` (overlaps?) | D |
| `d.transfers` | — | `CRDM_Transfer` | `app.transfer_orders` | D |
| `d.supplier_returns` | — | `CRDM_SupplierReturn` | (gap) | D |
| `d.web_returns` | — | `CRDM_WebItemReturn` | (gap; matters for omnichannel) | O or D |
| `d.etopup` | — | `CRDM_ETopUp` (mobile top-up — vertical-specific) | (likely scope-out; phone vertical) | (skip) |

**(All Canary platform-mechanics entities — Chirp/Fox/Hawk/Owl/Bull/Webhook/RaaS/Vault/etc. — have no GSLM or CRDM analog and will be added in Chunk 8 as second-tier canonical: platform layer, not domain.)**

## Coverage gap summary (high-level findings for record)

**Modules well-covered between sources:**
- T (Transaction Pipeline) — CRDM operational + Canary sales schema
- A (Asset) — GSLM SalesOutlets + Canary app.locations
- M (Merchandising) — GSLM rich master data, Canary partial
- Q (Loss Prevention) — Canary platform layer (Chirp/Fox/Hawk) is the active build

**Modules with material gaps:**
- **P (Pricing)** — GSLM has full Promotion model (5 tables); Canary has none yet. **Gap.**
- **F (Finance)** — GSLM has Taxes; Canary has bank_accounts but no tax model, no GL, no AP/AR, no three-way match. **Big gap.**
- **D (Distribution)** — CRDM has 5 movement entities; Canary has only `transfer_orders` and `stock_ledger_entries`. **Material gap.**
- **S (Space)** — GSLM has Planogram (1 table) + SKU/Pack-in-outlet placement (2 tables); Canary has zero. **Gap.**
- **L (Labor)** — Neither GSLM nor CRDM nor Canary has this. **Greenfield gap — must design from scratch.**
- **O (Orders)** — Sales orders / purchase orders absent across all sources except Canary `transfer_orders`. **Greenfield gap.**
- **E (Execution / Workflow)** — No source has task/workflow tables. **Greenfield gap.**
- **N (Device)** — All sources have implicit POS/terminal references via columns; only Canary has explicit `app.terminals`/`sales.terminals`. **Partial.**
- **C (Customer)** — CRDM 1.7.2 had it, dropped in 1.8. Canary has app.customers. **OK at master, weak at loyalty/segmentation.**

## What Chunk 2 onward will produce

For each entity in the canonical (~100-120 total), one entry like:

```
### m.products  [Module M — Merchandising]

**Sources:**
- GSLM3.SKUItems (43 cols) — anchor
- GSLM3.Styles + StyleVariants — variant decomposition (folded as JSON or separate table; TBD per design)
- CRDM_Item.ArticleID — referenced by transactions
- Canary app.products (12 cols) — current Canary version

**Canonical DDL** (Postgres):
```sql
CREATE TABLE m.products (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES m.tenants(id),
  sku text NOT NULL,
  -- ...
);
```

**Reconciliation notes:**
- GSLM had `bigint` for product_id; canonical uses `uuid` per Canary convention
- GSLM has `style_variant_id` FK chain; canonical folds variants into `attributes jsonb` for simplicity (variant_group can be reconstructed via index)
- Canary current has no `vendor_id` link — added per GSLM
- ...
```

## Status

- **Chunk 1 complete.** This file = the foundation everything else builds on.
- **Resume point:** Chunk 2 — GSLM canonical walk, Item/Catalog domain. ~10 entities. Output: first ~10 canonical entries appended to `02-canonical-draft.md` in this folder.
