# Inventory — Source Material for Canonical Data Model

**Working file. Chunk 1 output. Not for promotion.** Branch: `gd-canonical-data-model`.

Catalogues every entity-mention across every source. Anchors the entity-by-entity reconciliation walk that follows. Built per the founder's directive: *"go table by table by entity in the GSLM and produce the canonical."*

## Sources

| # | Source | Path | Era | Layer | Entities |
|---|---|---|---|---|---|
| **S0** | **GSLM MDM Site** ⭐ (HTML domain documentation, 9-domain canonical) | `~/CRDM-recovery/gslm-mdm-site/` (converted from `Brain/raw/inbox/DollarDollar/GSLM/GSLM WEB Content/`) | 2009-12 to 2010-01, Walmart Int'l GSLM team | **Master data — full canonical reference** | **~102** (across 9 domains) |
| S1 | GSLM SQL DDL (partial impl) | `~/CRDM-recovery/sql/Logical-Model-2009-12-14.sql` | 2009-12 | Master data — implementation subset | 43 |
| S2 | **CRDM POS 1.8 Data Dictionary** | `~/CRDM-recovery/data-dictionaries/CRDM-1.8-Data-Dictionary.md` | ~2013, Secure Store 3.2 | POS operational | 25 |
| S3 | CRDM POS 1.7.2 Data Dictionary | `~/CRDM-recovery/data-dictionaries/CRDM-1.7.2-Data-Dictionary.md` | ~2012 | POS operational | 27 |
| S4 | **Canary Go data-model.md** (active) | `docs/sdds/go-handoff/data-model.md` | 2026, GA-track | Canary platform + commercial | ~116 (65 detailed + 51 listed) |
| S5 | Canary Python data-model.md (frozen) | `docs/sdds/canary/data-model.md` | 2025, v0-python-prototype | Earlier Canary draft | ~95 |
| S6 | Recovery DDL fragments | `~/CRDM-recovery/sql/*.sql` (excl. Logical-Model) | 2010-2015 | Misc operational + reference | ~20 |
| S7 | GSLM Entity Descriptions (Word) | `~/CRDM-recovery/gslm-mdm-site/GSLM-Entity-Descriptions.md` | 2009-12 | Merchandise hierarchy reference | ~25 (subset of S0) |
| S8 | GSLM per-domain narrative overviews (.doc) | `~/CRDM-recovery/gslm-mdm-site/GSLM*Overview.txt` (11 files) | 2009-2010 | Domain rationale / context | n/a (prose) |
| **S9** | **TOM Interface Design Documents** ⭐ (Tesco Operating Model integration program) | `Brain/raw/inbox/Interface Design Documents/` | 2007, Project BEN | **Operational reality — field-level data exchange between named systems** | **82 interface specs** (154 .doc + 69 .vsd + 129 .xls) |

**Authority order for canonical reconciliation (REVISED again — S9 added):**
1. **GSLM MDM Site (S0)** ⭐ — full canonical structure; the abstract anchor
2. **TOM Interface Design Documents (S9)** ⭐ — operational reality / field-level data exchange between real systems; the concrete reinforcement
3. **GSLM Entity Descriptions (S7)** — entity-by-entity attribute reference (subset of S0)
4. **GSLM SQL DDL (S1)** — physical implementation reference (for type choices, constraint patterns)
5. **GSLM narrative overviews (S8)** — domain rationale, context for design decisions
6. **Canary Go data-model (S4)** — active platform spec, supersedes Python proto
7. **CRDM 1.8 (S2)** — POS operational layer; preferred over 1.7.2 where they overlap
8. **CRDM 1.7.2 (S3)** — only consulted for entities dropped in 1.8 (Customer, Repair) or to surface evolution deltas
9. **Python proto (S5)** — semantic reference only; no DDL pulls
10. **Recovery DDL fragments (S6)** — pulled selectively for specific reference tables and platform precursors

**S0 vs S9 relationship:** GSLM (S0) is the abstract canonical model — what entities SHOULD exist and how they SHOULD relate. TOM Interface Design Documents (S9) are the concrete operational specs — what FIELDS actually moved between real production systems (RMS, GFO, Storeline, ORMS, RWMS, TIMS, etc.) at Tesco circa 2007. S0 tells us what the entity is; S9 tells us what its real-world payload looks like, in COBOL flat-file precision (PIC clauses, byte positions). Use them together: S0 for entity definition, S9 for field-level grounding and missing operational entities (Orders, Distribution movements, Finance flows).

## S0 — GSLM MDM Site entities (~102 across 9 domains, ANCHOR)

Founder's own canonical retail data model, fully documented as a 9-domain web property (Jan 2010 build). Each domain has its own HTML page (now markdown), narrative .doc overview, and ERD PNG diagram. **This is the actual canonical — the SQL was a partial implementation subset.**

### Domain entity counts (per `Entity Name` table headers)

| Domain | Entities | File | Narrative |
|---|---|---|---|
| **Item** | 22 | `Item.md` (3859 lines) | `GSLM Item Overview.txt` (33 KB) |
| **Supply** (Chain / Vendor / Inventory) | 19 | `Supply.md` (3512 lines) | `GSLM Supply Chain Overview.txt` (18 KB) |
| **Location** | 16 | `Location.md` (2083 lines) | `GSLM Location Overview.txt` (12 KB) |
| **Customer** | 14 | `Customer.md` (1956 lines) | `GSLM Customer Overview.txt` (12 KB) |
| **Finance** | 13 | `Finance.md` (2459 lines) | `GSLM Finance Overview.txt` (15 KB) |
| **Space** (Planning / Planogram) | 8 | `Space.md` (1420 lines) | `GSLM Space Planning Overview.txt` (9 KB) |
| **Price** (and Promotion) | 6 | `Price.md` (956 lines) | `GSLM Price and Promotion Overview.txt` (8 KB) |
| **People** | 4 | `People.md` (972 lines) | `GSLM People Overview.txt` (5 KB) |
| **Controls** (Parameters / interface scaffolding) | 0 (narrative only) | `Controls.md` (505 lines) | `GSLM Controls and Parameters Overview.txt` (3 KB) |
| **TOTAL** | **~102** | | |

### Why this changes everything

The Logical-Model SQL (S1, 43 tables) covered only the Item/Location/Vendor/Promotion subset that the Walmart project's first phase implemented. The MDM site (S0) is the **complete 9-domain canonical** — it includes:

- **Customer** (14 entities) — Canary currently has only `app.customers`
- **Finance** (13 entities) — Canary has `app.bank_accounts` and `ledger.*` only; no GL, AP/AR, three-way match, or tax model
- **People** (4 entities) — Canary has `app.employees` only; no labor/scheduling
- **Space** (8 entities) — GSLM SQL had only `Planogram` (1); MDM site has 8 including shelf placement
- **Supply** (19 entities — vendor + distribution + inventory) — Canary has 2 movement entities; MDM has the full chain

This means the **module gap analysis from earlier needs revision**:
- F (Finance), L (Labor), C (Customer) — **NOT greenfield** — they have full MDM-layer canonical to draw from
- D (Distribution), S (Space), P (Pricing) — gaps in Canary, **but rich source material** in GSLM MDM
- O (Orders), E (Execution) — still genuinely greenfield (no MDM source covers them)

### Per-domain entity name extraction status

The HTM-derived markdown retains MS Office HTML markup (inline styles), so the ~102 entity-name table cells require per-domain reading during the walk rather than a one-pass regex extract. Each chunk (2-7) will read its domain's full markdown and extract entities one at a time. This is fine — the canonical work is per-entity anyway.

## S1 — GSLM SQL DDL entities (43, partial implementation)

Subset of S0, with concrete SQL Server 2008 R2 DDL. Use for type/constraint reference when reconciling. Grouped by their natural place in S0's 9 domains:

| S0 Domain | S1 SQL tables (subset implemented) |
|---|---|
| Item (22 in S0) | `Merchandise`, `MerchandiseAttributesLanguages`, `MerchandiseType`, `BusinessDivisions`, `Departments`, `Classes`, `SubClasses`, `Finelines`, `Sections`, `SKUItems`, `Styles`, `StyleVariants`, `StyleVariantValues`, `StyleVariantGroups`, `StyleVariantGroupAssignments`, `ArticleItems`, `ArticleTypes`, `Ingredients`, `PackItems`, `PackItemBreakout`, `PackBreakout`, `UserDefinedAttributes`, `UserDefinedAttributeValues` (23 of S0's 22 — overlap likely from S0 not breaking out UDA from item core) |
| Location (16 in S0) | `SalesOutlets`, `SalesFloors`, `SalesFloorsInSalesOutlet`, `SalesOutletDepartments`, `SalesOutletAssets`, `SalesOutletAssetLocation`, `SalesOutletHolidays` (7 of 16) |
| Supply (19 in S0) | `Vendors`, `SKUItemVendors` (2 of 19 — minimal vendor master only) |
| Price (6 in S0) | `Promotions`, `PromotionComponents`, `PromotionComponentDetails`, `PromotionThresholds`, `ThresholdIntervals`, `Taxes`, `ItemTaxesInSalesOutlets`, `SalesOutletSKUItemPromoCompDetails`, `SKUItemsInSalesOutlets`, `PackItemsInSalesOutlets` (10 — Pricing + cross-store placement) |
| Space (8 in S0) | `Planogram` (1 of 8) |
| Customer (14 in S0) | (none implemented in SQL) |
| Finance (13 in S0) | (none — except `Taxes` listed under Price) |
| People (4 in S0) | (none implemented) |
| Controls (narrative) | (n/a) |

> **Critical observation (revised):** GSLM as documented in S0 covers all 9 domains of master data — including Customer, Finance, People — that the SQL implementation never reached. The canonical walk should anchor on S0 (full domain coverage), then use S1 where actual SQL types/constraints are needed, then add CRDM operational and Canary platform layers on top.

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

- **Chunk 1 complete (revised after S0 discovery).** This file = the foundation everything else builds on.

## Revised chunk plan (post-S9-discovery)

| # | Domain / Layer | S0 entities | + S9 prefix interfaces | + Operational (CRDM/Canary) | Module owner(s) |
|---|---|---|---|---|---|
| 2 | **Item** (S0) | 22 | C-Prefix (11): Product details, supplier ref, dept/sub-dept, store/warehouse attrs, PLU | + Canary `app.products`; CRDM `Item` line items | M (Merchandising) |
| 3 | **Location** (S0) + **Space** (S0) | 16 + 8 = 24 | S-Prefix (19): store details, store range, capacity info, planogram product map, range data | + Canary `app.locations`, `app.location_hierarchy`; recovery `Ref_LocationHierarchy` | A (Asset) + S (Space) |
| 4 | **Customer** (S0) + **People** (S0) | 14 + 4 = 18 | (P-Prefix empty; R-Prefix empty — gap remains for People exchange) | + Canary `app.customers`, `app.users`, `app.employees`, `app.user_*`, `app.employee_*`; CRDM 1.7.2 `Customer` | C (Customer) + L (Labor) |
| 5 | **Supply** (S0) — vendor + distribution + inventory | 19 | **D-Prefix (18)**: PO download, GRN, inventory adjustment, stocktake, RTV, direct PO receipt, stock transfer | + CRDM `GoodsReceived`, `Transfer`, `StockAdjustment`, `SupplierReturn`, `WebItemReturn`; Canary `transfer_orders`, `ledger.stock_ledger_entries` | M (vendors) + D (Distribution) |
| **5b** | **NEW — Orders** (closes greenfield) | (none in S0) | **J-Prefix (29)**: allocations, sales forecast, PBS/PBL/Direct order types, ASN, BOL picking, item-warehouse-supplier, transfer details, promotions interface | (no Canary equivalent — net new) | **O (Orders)** |
| 6 | **Price** (S0) + **Finance** (S0) | 6 + 13 = 19 | F-Prefix (5): PO RMS↔TIMS, supplier invoice, supplier info, PO ack, Tesco invoice ReIM | + Canary `app.bank_accounts`, `ledger.*` | P (Pricing) + F (Finance) |
| 7 | **CRDM POS Operational** (Transaction Pipeline) | n/a (S0 doesn't have transactions) | (no S9 prefix for POS — TOM was back-office) | CRDM 25 entities (Header, Item, Tender, Discount, FastFact, etc.) + Canary `sales.*` schema | T (Transaction Pipeline) |
| 8 | **Canary platform mechanics** | n/a (no MDM source) | n/a (TOM had its own "Operational Framework" — out of scope) | Chirp, Fox, Hawk, Owl, Bull, Webhook, RaaS, Vault, ILDWAC, blockchain anchor, evidence chain, identity, audit_log | Q (LP) + cross-cutting |
| 9 | Module ownership tagging across whole spine | | | | all 13 modules |
| 10 | Render `canonical-data-model.md` + provenance memo + closures | | | | |

**Estimated total canonical entities (REVISED):** ~165-180
- GSLM domains (S0): ~102
- TOM Order entities (S9 J-Prefix net-new): ~10-15 (PO, BOL, ASN, Allocation, Transfer Order, Direct Store Order, Procurement Order, Final Order, etc.)
- CRDM POS operational layer (S2): ~25
- Canary platform mechanics (S4 net-new): ~25-30

**Greenfield modules remaining (no source has them):**
- E (Execution / workflow) — task management, work assignment, status flows
- L (Labor schedules + time records) — People exists in S0 but only 4 entities (employee master); scheduling/time/labor allocation is greenfield

**Closed by S9:**
- ~~O (Orders)~~ — J-Prefix gives PBS, PBL, Direct Store Order, Allocation, Transfer; D-Prefix gives PO download/receipt
- ~~D (Distribution movements partial)~~ — D-Prefix gives full operational movement set

- **Resume point:** Chunk 2 — GSLM Item domain (22 entities). Read `~/CRDM-recovery/gslm-mdm-site/Item.md` entity-by-entity, reconcile with S1 SQL DDL types and Canary `app.products`, produce canonical entries appended to `02-canonical-draft.md` in this folder.
