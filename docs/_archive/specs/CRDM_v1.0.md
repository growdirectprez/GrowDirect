---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# CRDM — Canary Retail Data Model

**It's transactional. Everything else is window dressing.**

**Version:** 1.0
**Date:** February 20, 2026
**Authors:** Eva (Program Manager), Tom (Systems Architect), Jeremy (Developer Quant)
**Directive:** Jeffe — "If the soil is barren our little farm won't grow anything."
**Classification:** Internal — **MANDATORY PROJECT CONTEXT**
**Status:** **LOAD EVERY SESSION. NO EXCEPTIONS.**

---

> *"Our soil is our data model, built at enterprise scale, time-tested, hundreds of billions of rows processed, billions saved. But if it's not right now, it's harder and harder to fix."*
> — Jeffe, February 20, 2026

---

## Why This Document Exists

This is the single authoritative reference for every data decision in Canary. It synthesizes five sources into one logical truth:

| Source | What It Provides | Where It Lives |
|--------|-----------------|----------------|
| **Enterprise LP Data Specification v1.1** (2018) | The enterprise LP data model Jeffe reviewed and signed off on. The ancestor. | `Archive/SysRepublic/Enterprise_LP_Data_Specification_v1.1.pdf` |
| **GrowDirect Unified Data Model v1.0** | Tom/Jeremy's GSLM + CRDM + Walmart patterns adapted for modern SMB | `Markdown/Specs/GrowDirect_Unified_Data_Model_v1.0.md` |
| **Canary CRDM v1.0** (Field-Level Mapping) | Every enterprise ancestor field mapped to Canary columns with gap analysis | `Markdown/Specs/Canary_CRDM_v1.0.md` |
| **Square API LP Coverage Analysis** | Jeremy's 14-API-family gap analysis — what Square gives us vs. what we ingest | `Markdown/Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md` |
| **Schema Quick Reference** | Three-database architecture, design patterns, indexing, data flow | `Markdown/Specs/SCHEMA_QUICK_REFERENCE.md` |

**Rule:** If a question about the data model can't be answered from this guide, the guide is incomplete. Fix it.

---

## Part 1: The Foundation — Three Guiding Principles

### Principle 1: Enterprise Bones, SMB Skin

The Canary data model is not invented. It descends from a proven enterprise LP data architecture that processed hundreds of billions of rows across 7-Eleven (6,800+ stores), IKEA, Stein Mart, Walmart (the only combined US + International view), Kroger, Tesco, and Home Depot. We are packaging that architecture for Square merchants at $49/month.

**Provenance — TDS → Walmart SMART → CRDM:** The original ancestor of the CRDM was called **TDS (Till Data Store)** — built from the ground up for Tesco. TDS was a bidirectional data store for register configuration, items, price files, and all enterprise-to-store metadata. In the 2010s, Jeffe morphed the TDS blueprint into the **Walmart SMART System format** — a canonical abstraction layer for Walmart International's aggressive acquisition of small chains (bodegas) across Central and South America. That model was deployed to thousands of stores, with data round-tripping through SysRepublic's SQL Server infrastructure validated at HP Labs (Microsoft, Walmart, HP, SysRepublic). **The CRDM is the third generation of the same canonical schema pattern, now targeting Square SMB merchants.** The orchestration layer that fed TDS was **RTI (Real Time Integrator)** — SysRepublic's original product, a lightweight Windows service agent for real-time data movement deployed across Tesco worldwide, Ross Stores, and Delta Airlines. RTI is the direct ancestor of Canary's webhook listeners and polling workers. *(Jeffe disclosures, February 20, 2026)*

What this means in practice:

- Every table traces its lineage to either the **Enterprise LP Data Specification** (7 data sources, 13 transaction types) or the **GSLM/CRDM/Walmart** patterns Tom and Jeremy codified
- We do not invent new entity patterns without verifying they have enterprise precedent
- When in doubt, check the enterprise ancestor spec first. If it was modeled there, there's a reason

### Principle 2: Canonical Schema — POS-Agnostic by Design

Per Jeffe's mandate (Feb 17): *"Every POS integration must map to a canonical transaction schema via a vendor-specific parser. Bake it into the ethos."*

```
Square Webhook ──→ Square Parser ──→ CRDM Canonical Tables ──→ Chirp Detection
Clover Webhook ──→ Clover Parser ──→ CRDM Canonical Tables ──→ Chirp Detection
Toast  Webhook ──→ Toast  Parser ──→ CRDM Canonical Tables ──→ Chirp Detection
```

The CRDM tables documented here ARE the canonical schema. Chirp detection rules operate on these tables and work identically regardless of source POS. The parser layer is vendor-specific; the data model is universal.

### Principle 3: Immutable Where It Matters

Three categories of data integrity, non-negotiable:

| Category | Pattern | Tables | Why |
|----------|---------|--------|-----|
| **Financial ledger** | APPEND-ONLY (no UPDATE, no DELETE) | `transactions`, `refund_links`, `cash_drawer_events`, `gift_card_activities` | Financial data is a ledger. You don't erase entries. |
| **Evidentiary** | INSERT-ONLY (enforced by DB trigger) | `case_evidence`, `evidence_access_log`, `case_timeline` | Law enforcement chain of custody. If we accuse someone, we have to be sure and have the facts. |
| **Audit trail** | APPEND-ONLY + SHA-256 hash chain | `audit_log` | Tamper detection. Each entry's hash includes the previous entry's hash. Break one, break the chain downstream. |
| **Operational** | Soft delete (`db_status`, `db_effective_from/to`) | Everything else | Normal CRUD with history preservation. |

---

## Part 2: The Three-Database Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CANARY PLATFORM                           │
├──────────────────┬──────────────────┬──────────────────────┤
│   canary_app     │   canary_sales   │   canary_metrics     │
│   (Operational)  │   (Transaction   │   (Analytics & ML)   │
│                  │    Log)          │                      │
├──────────────────┼──────────────────┼──────────────────────┤
│ ACID, RLS        │ Append-only      │ Star schema          │
│ Normalized       │ JSONB payloads   │ Pre-aggregated       │
│ Soft deletes     │ Monthly partn.   │ Monthly partn.       │
├──────────────────┼──────────────────┼──────────────────────┤
│ Users, Merchants │ Transactions     │ Daily/Hourly metrics │
│ Locations, Prods │ Line Items  🆕   │ Employee metrics     │
│ Employees, Custs │ Tenders     🆕   │ Product metrics      │
│ Alerts, Cases    │ Cash Drawer  🆕  │ ML features/scores   │
│ Evidence, Audit  │ Inventory    🆕  │ Operator actions     │
│ Timecards    🆕  │ Gift Cards   🆕  │ Scorecards           │
│ Disputes     🆕  │ Ingestion log    │ Risk score history   │
│                  │ ETL batches      │ Baselines            │
│                  │ Dead letter Q    │                      │
└──────────────────┴──────────────────┴──────────────────────┘
```

**Current implementation:** SQLite (single DB, MVP). PostgreSQL three-database architecture is the target after Square Marketplace certification. The schema design is Postgres-ready — the table structures, constraints, and patterns are identical. Only the deployment topology changes.

---

## Part 3: The Seven Canonical Data Sources

These are the seven data domains that feed any retail LP platform. They were defined in the enterprise ancestor spec (2018) that Jeffe reviewed and signed off on. Canary implements them via Square APIs. Every new POS integration must map to these same seven sources.

### Source 1: Transaction Header

**What it is:** One record per POS transaction. The backbone.

**Canary table:** `canary_sales.transactions`

**Key fields and their lineage:**

| CRDM Field | Enterprise Origin | Square Source | Canary Column | Status |
|------------|---------------|---------------|---------------|--------|
| Store | StoreNumber | `location_id` | `transactions.location_id` | ✅ |
| Register | RegisterNumber | `device_id` from payment | `transactions.device_id` | ✅ |
| Transaction ID | TransactionNumber | `payment_id` | `transactions.external_id` | ✅ |
| Business Date | BusinessDate | `created_at` | `transactions.transaction_date` | ✅ |
| **Transaction Type** | TransactionType | Inferred + explicit | `transactions.transaction_type` | 🆕 E1-F9 |
| Operator | OperatorID | `team_member_id` | `transactions.employee_id` | ✅ |
| Original Txn | OrigTransactionNumber | via refund link | `refund_links.original_external_id` | ✅ |
| Gross Amount | TransactionGrossAmount | `amount_money` | `transactions.amount_cents` | ✅ |
| Tax | TransactionTaxAmount | `total_tax_money` | `transactions.tax_amount_cents` | ⚠️ Extract Sprint 2 |
| Discount | TransactionDiscountAmount | `total_discount_money` | `transactions.discount_amount_cents` | ⚠️ Extract Sprint 2 |
| Customer | CustomerID | `customer_id` | `transactions.customer_id` | ✅ |
| Channel | ChannelType | `square_product` | `transactions.square_product` | ✅ |
| Currency | CurrencyCode | `currency` | `transactions.currency` | ✅ |

**Transaction Type Enum** (🆕 E1-F9 — the single most important schema addition):

| Type | Enterprise Code | Square Detection Method | Chirp Relevance |
|------|-------------|------------------------|-----------------|
| SALE | Sale | `payment.created` status=COMPLETED | Baseline |
| RETURN | Return | `refund.created` | Core Chirp target |
| VOID | Void | `payment.updated` status=CANCELED (immediate) | `HIGH_VOID_RATE` |
| POST_VOID | PostVoid | `payment.updated` COMPLETED→CANCELED (delayed) | `POST_VOID_ALERT` — always fires |
| NO_SALE | NoSale | Cash Drawer Events API | `HIGH_NO_SALE_FREQUENCY` |
| PAID_IN | PaidIn | Cash Drawer Events API | `EXCESSIVE_PAID_OUT` |
| PAID_OUT | PaidOut | Cash Drawer Events API | `EXCESSIVE_PAID_OUT` |
| EXCHANGE | Exchange | Order with `line_items` + `returns` | Derived |

**Coverage: 18/28 enterprise ancestor fields (64%).** Remaining gaps are mostly Square API limitations (no EndDateTime, no SupervisorID natively, no VoidReasonCode).

---

### Source 2: Tender (Payment Method Detail)

**What it is:** One record per payment method per transaction. Supports split-tender.

**Canary table:** `canary_sales.transaction_tenders` (🆕 E1-F7)

| CRDM Field | Canary Column | Status |
|------------|---------------|--------|
| Tender Type | `tender_type` (CARD, CASH, SQUARE_GIFT_CARD, OTHER, NO_SALE) | 🆕 |
| Tender Amount | `amount_cents` | 🆕 |
| Card Brand | `card_brand` | 🆕 |
| Last 4 | `card_last4` | 🆕 |
| Entry Method | `entry_method` | 🆕 |
| Card Fingerprint | Via `transactions.card_fingerprint` join on `payment_id` | ✅ |
| Employee | `team_member_id` | 🆕 |

**Why this matters:** Before this table, Canary flattened multi-tender transactions to a single tender. You cannot detect tender swap fraud or split-tender manipulation without per-tender records.

**Coverage: 10/13 (77%).** ChangeDue and AuthorizationCode are Square API limitations.

---

### Source 3: Line Items

**What it is:** One record per item per transaction. Where sweet-hearting and selective scanning live.

**Canary table:** `canary_sales.transaction_line_items` (🆕 E1-F7)

| CRDM Field | Canary Column | Status |
|------------|---------------|--------|
| Item ID | `catalog_object_id` | 🆕 |
| Item Name | `item_name` | 🆕 |
| Quantity | `quantity` (supports fractional, e.g., 2.5 lbs) | 🆕 |
| Unit Price | `base_price_cents` | 🆕 |
| Extended Price | `gross_sales_cents` | 🆕 |
| Discount | `total_discount_cents` — **the sweet-hearting signal** | 🆕 |
| Tax | `total_tax_cents` | 🆕 |
| Item Type | `item_type` (ITEM, CUSTOM_AMOUNT, GIFT_CARD) | 🆕 |
| Void Flag | `is_voided` | 🆕 |
| Return Reason | `return_reason` | 🆕 |

**Why this matters:** This is the single biggest schema improvement in the scope expansion. You cannot detect sweet-hearting, selective scanning, or discount abuse without line-item-level relational access. Before E1-F7, all of this was buried in JSONB.

**Coverage: 14/21 (67%).** Gaps are merchandise hierarchy (Dept/Class/Subclass) which Square doesn't natively provide, and VendorID (Bull module scope).

---

### Source 4: Employee

**What it is:** Reference data for all operators + real-time shift data.

**Canary tables:** `canary_app.employees` (existing) + `canary_app.employee_timecards` (🆕 E1-F8)

| CRDM Field | Canary Column | Status |
|------------|---------------|--------|
| Employee ID | `employees.square_employee_id` | ✅ |
| Name | `employees.employee_name` | ✅ |
| Status | `employees.db_status` | ✅ |
| Primary Location | `employees.primary_location_id` | ✅ |
| Risk Score | `employees.risk_score` | ✅ |
| **Shift Start** | `employee_timecards.start_at` | 🆕 E1-F8 |
| **Shift End** | `employee_timecards.end_at` | 🆕 E1-F8 |
| **Breaks** | `employee_timecards.breaks` (JSONB) | 🆕 E1-F8 |
| **Location Worked** | `employee_timecards.location_id` | 🆕 E1-F8 |

**What Canary adds that the enterprise ancestor never had:** Real-time timecard cross-reference. The legacy platform received employee data as batch reference files. Canary's real-time ingestion enables three detection rules impossible on legacy platforms:

- `OFF_CLOCK_TRANSACTION` — payment by employee not on active timecard
- `BREAK_TRANSACTION` — payment during declared break
- `WRONG_LOCATION_ACTIVITY` — clocked in at A, payment at B

**Coverage: 9/10 original fields + 4 new (90%+).**

---

### Source 5: Product/Article

**What it is:** Reference data for all sellable items.

**Canary table:** `canary_app.products` (existing)

| CRDM Field | Canary Column | Status |
|------------|---------------|--------|
| Item ID | `products.square_item_id` | ✅ |
| Description | `products.product_name` | ✅ |
| UPC | `products.UPC` | ✅ |
| SKU | `products.SKU` | ✅ |
| Cost (COGS) | `products.COGS` | ✅ |
| Retail Price | `products.unit_price` | ✅ |
| Department/Class/Subclass | — | ❌ Square doesn't provide hierarchy |

**Coverage: 7/11 (64%).** Merchandise hierarchy gap is structural to Square. Tom's GSLM-inspired hierarchy pattern can extend to products post-MVP.

---

### Source 6: Store/Location

**What it is:** Reference data for physical locations with organizational hierarchy.

**Canary table:** `canary_app.locations` (existing)

| CRDM Field | Canary Column | Status |
|------------|---------------|--------|
| Store ID | `locations.square_location_id` | ✅ |
| Store Name | `locations.location_name` | ✅ |
| Region/District/Market | `locations.hierarchy_id` → location_hierarchy (GSLM pattern) | ✅ |
| Timezone | `locations.timezone` | ✅ |
| Coordinates | `locations.coordinates` | ✅ |
| Business Hours | `locations.business_hours` (JSONB) | ✅ |
| Address fields | In Square data, extract to columns Sprint 2 | ⚠️ |
| Square Footage | — | ❌ Critical for Owl shrinkage-per-sqft. Add post-MVP. |

**Coverage: 12/17 (71%).**

---

### Source 7: Customer

**What it is:** Customer identification and lifetime value.

**Canary table:** `canary_app.customers` (existing)

| CRDM Field | Canary Column | Status |
|------------|---------------|--------|
| Customer ID | `customers.square_customer_id` | ✅ |
| Lifetime Value | `customers.lifetime_value` | ✅ |
| Transaction Count | `customers.transaction_count` | ✅ |
| Loyalty | — | ❌ Post-MVP (Square Loyalty API) |
| PII (address/phone/email) | — | ❌ **By design** — privacy-first |

**Coverage: 3/7 (43%).** Gaps are loyalty (post-MVP) and PII (not tracked by design).

---

## Part 4: Canary-Native Data Sources (Beyond the Enterprise Ancestor)

These didn't exist in the enterprise ancestor spec because legacy platforms relied on batch SFTP feeds that couldn't expose real-time operational data. Canary's Square API integration enables capabilities the ancestor platform never had.

### Cash Drawer Events (🆕 E1-F6)

**Tables:** `canary_sales.cash_drawer_shifts` + `canary_sales.cash_drawer_events`

**LP significance:** Cash drawer is the #1 traditional LP signal. No-sales, paid-outs, and cash variance are the foundation of brick-and-mortar loss prevention.

**Key computed field:** `cash_variance_cents = closed_cash_cents - expected_cash_cents` — The single most important LP metric for cash-handling fraud.

**Chirp rules enabled:**

| Rule ID | Rule | Default Threshold |
|---------|------|-------------------|
| C-101 | `HIGH_NO_SALE_FREQUENCY` | >5/shift |
| C-102 | `CASH_VARIANCE_THRESHOLD` | >±$20 |
| C-103 | `EXCESSIVE_PAID_OUT` | >$100/shift |
| C-104 | `AFTER_HOURS_DRAWER_OPEN` | Any |

---

### Inventory Adjustments (🆕 E1-F10)

**Table:** `canary_sales.inventory_adjustments`

**LP significance:** Bridges the gap from suspicious transactions to actual shrinkage measurement.

| Rule ID | Rule | Default Threshold |
|---------|------|-------------------|
| C-501 | `SHRINKAGE_SPIKE` | >2% in category |
| C-502 | `MANUAL_ADJUSTMENT_VELOCITY` | >3/day per employee |

---

### Gift Card Activities (🆕 E1-F11)

**Table:** `canary_sales.gift_card_activities`

**LP significance:** Gift card fraud is top-3 LP loss category industry-wide.

| Rule ID | Rule | Default Threshold |
|---------|------|-------------------|
| C-601 | `GIFT_CARD_LOAD_VELOCITY` | >5/day per employee |
| C-602 | `RETURN_TO_GIFT_CARD` | Pattern detection |

---

## Part 5: Complete Chirp Detection Registry

All 22 detection rules organized by data source. Every rule traces to a CRDM field and a table in this guide.

### Payment-Based (C-001 to C-008) — Existing

| ID | Rule | Signal | Source Table |
|----|------|--------|-------------|
| C-001 | `HIGH_REFUND_FREQUENCY` | >5 refunds/day per employee | `transactions` + `refund_links` |
| C-002 | `HIGH_REFUND_AMOUNT` | Single refund >$500 | `transactions` |
| C-003 | `RAPID_REFUND_VELOCITY` | >3 refunds in 1 hour | `transactions` |
| C-004 | `AFTER_HOURS_REFUND` | Refund outside business hours | `transactions` + `locations.business_hours` |
| C-005 | `CROSS_STORE_RETURN` | Return at different location than sale | `transactions` + `refund_links` |
| C-006 | `CARD_FINGERPRINT_NOMAD` | Same card >3 locations in 24h | `transactions.card_fingerprint` |
| C-007 | `PREPAID_CARD_VELOCITY` | >5 prepaid cards/day per employee | `transactions.card_prepaid_type` |
| C-008 | `CVV_AVS_MISMATCH` | Verification failure pattern | `transactions.cvv_status` + `avs_status` |

### Cash Drawer (C-101 to C-104) — 🆕 E1-F6

| ID | Rule | Signal | Source Table |
|----|------|--------|-------------|
| C-101 | `HIGH_NO_SALE_FREQUENCY` | >5 no-sales/shift | `cash_drawer_events` |
| C-102 | `CASH_VARIANCE_THRESHOLD` | >±$20 variance | `cash_drawer_shifts.cash_variance_cents` |
| C-103 | `EXCESSIVE_PAID_OUT` | >$100/shift | `cash_drawer_events` |
| C-104 | `AFTER_HOURS_DRAWER_OPEN` | Outside business hours | `cash_drawer_shifts` + `locations.business_hours` |

### Order/Line-Item (C-201 to C-203) — 🆕 E1-F7

| ID | Rule | Signal | Source Table |
|----|------|--------|-------------|
| C-201 | `EXCESSIVE_DISCOUNT_RATE` | >50% avg discount | `transaction_line_items.total_discount_cents` |
| C-202 | `LINE_ITEM_VOID_RATE` | >10% void rate | `transaction_line_items.is_voided` |
| C-203 | `SWEET_HEART_PATTERN` | >3 high-discount occurrences same customer+employee | `transaction_line_items` + `transactions.customer_id` |

### Timecard Cross-Reference (C-301 to C-303) — 🆕 E1-F8

| ID | Rule | Signal | Source Table |
|----|------|--------|-------------|
| C-301 | `OFF_CLOCK_TRANSACTION` | Payment by off-clock employee | `transactions.employee_id` vs `employee_timecards` |
| C-302 | `BREAK_TRANSACTION` | Payment during break | `transactions` vs `employee_timecards.breaks` |
| C-303 | `WRONG_LOCATION_ACTIVITY` | Clocked in A, payment at B | `employee_timecards.location_id` vs `transactions.location_id` |

### Void/Post-Void (C-401 to C-402) — 🆕 E1-F9

| ID | Rule | Signal | Source Table |
|----|------|--------|-------------|
| C-401 | `HIGH_VOID_RATE` | >5 voids/day per employee | `transactions.transaction_type = VOID` |
| C-402 | `POST_VOID_ALERT` | Any post-void (always suspicious) | `transactions.transaction_type = POST_VOID` |

### Inventory (C-501 to C-502) — 🆕 E1-F10

| ID | Rule | Signal | Source Table |
|----|------|--------|-------------|
| C-501 | `SHRINKAGE_SPIKE` | >2% variance in category | `inventory_adjustments` |
| C-502 | `MANUAL_ADJUSTMENT_VELOCITY` | >3 manual adjustments/day | `inventory_adjustments.team_member_id` |

### Gift Card (C-601 to C-602) — 🆕 E1-F11

| ID | Rule | Signal | Source Table |
|----|------|--------|-------------|
| C-601 | `GIFT_CARD_LOAD_VELOCITY` | >5 loads/day per employee | `gift_card_activities` |
| C-602 | `RETURN_TO_GIFT_CARD` | Refund → gift card load pattern | `gift_card_activities` + `transactions` |

---

## Part 6: Complete Table Inventory

### canary_sales — Transaction Log (Append-Only)

| Table | CRDM Source | Status | LP Role |
|-------|------------|--------|---------|
| `transactions` | Transaction Header (#1) | Existing | Core — every query starts here |
| `refund_links` | Transaction Header (#1) | Existing | Refund ↔ original linking |
| `transaction_line_items` | Item Source (#3) | 🆕 E1-F7 | Sweet-hearting, selective scanning, discount abuse |
| `transaction_tenders` | Tender Source (#2) | 🆕 E1-F7 | Tender swap, split-tender manipulation |
| `cash_drawer_shifts` | Canary-native | 🆕 E1-F6 | Cash variance, shift reconciliation |
| `cash_drawer_events` | PaidIn/PaidOut entity | 🆕 E1-F6 | No-sales, paid-outs, per-event tracking |
| `inventory_adjustments` | Product Source (partial) | 🆕 E1-F10 | Actual shrinkage measurement |
| `gift_card_activities` | GiftCard entity | 🆕 E1-F11 | Gift card fraud lifecycle |
| `ingestion_log` | — | Existing | Webhook idempotency |
| `etl_batches` | — | Existing | ETL job tracking |
| `dead_letter_queue` | — | Existing | Failed payload replay |

### canary_app — Operational

| Table | CRDM Source | Status | LP Role |
|-------|------------|--------|---------|
| `merchants` | — | Existing | Multi-tenant root |
| `users` | — | Existing | RBAC (owner/admin/manager/analyst/viewer) |
| `locations` | Store/Location Source (#6) | Existing | Geographic hierarchy, business hours |
| `products` | Product/Article Source (#5) | Existing | Item reference, COGS, pricing |
| `employees` | Employee Source (#4) | Existing | Operator tracking, risk scoring |
| `customers` | Customer Source (#7) | Existing | Lifetime value, transaction count |
| `employee_timecards` | Employee Source (#4, extended) | 🆕 E1-F8 | Ghost employee, off-clock detection |
| `alerts` | — | Existing | Chirp detection results (immutable) |
| `alert_history` | — | Existing | Alert status workflow |
| `detection_rules` | — | Existing | Configurable Chirp thresholds |
| Fox tables (7) | — | Existing | Cases, subjects, evidence, timeline, actions |
| `audit_log` | — | Existing | Hash-chained tamper detection |
| `webhook_events` | — | Existing | Idempotent webhook processing |
| `card_profiles` | — | Existing | Card risk profiling |
| `blocked_entities` | — | Existing | Blocked cards/employees/devices |
| `schema_fingerprints` | — | Existing | Schema drift detection |
| `disputes` | — | 🆕 Sprint 3 | Chargeback signal |

### canary_metrics — Analytics & ML

| Table | Status | Role |
|-------|--------|------|
| `daily_metrics` | Existing | Location-level daily rollups |
| `hourly_metrics` | Existing | Location-level hourly rollups |
| `employee_daily_metrics` | Existing | Per-employee daily (refunds, voids, no-sales, off-clock) |
| `product_daily_metrics` | Existing | Per-product daily (sold, returned, return rate) |
| `operator_actions` | 🆕 PhD design | Supervisor override tracking |
| `transaction_features` | Existing | Per-transaction ML feature vectors |
| `feature_definitions` | Existing | Feature registry |
| `ml_models` | Existing | Model registry |
| `entity_risk_scores` | Existing | Running risk assessments |
| `risk_score_history` | Existing | Immutable risk score audit |
| `metric_baselines` | Existing | Statistical baselines for anomaly detection |
| `weekly_scorecard` | Existing | KPI rollups |
| `monthly_scorecard` | Existing | KPI rollups |

**Total: ~35 tables** (27 existing + 8 new from scope expansion)

---

## Part 7: Design Patterns (Non-Negotiable)

### Pattern 1: Multi-Tenant RLS
```
SET app.current_merchant_id = <merchant_id>;
-- Every tenant-scoped table has:
CREATE POLICY tenant_isolation ON <table>
    USING (merchant_id = current_setting('app.current_merchant_id'));
```
Every table has `merchant_id`. No exceptions. No cross-tenant queries without explicit admin override.

### Pattern 2: Standard Entity Fields
All dimension tables carry:
```
db_status          -- draft/active/archived (soft delete)
db_effective_from  -- when does this become active?
db_effective_to    -- when does this expire? (GSLM effective dating)
created_by, created_at, modified_by, modified_at
```

### Pattern 3: JSONB + Extracted Columns
```
transactions.payload    -- Full Square webhook (future flexibility)
transactions.amount_cents  -- Extracted for current queries (fast)
```
Square API evolves → payload captures new fields automatically. No schema migration needed for new fields. Current queries use extracted columns for performance. Full data preserved for forensic analysis.

### Pattern 4: Hash Chain (Audit Trail)
```
record_hash = SHA-256(current_entry + previous_entry_hash)
```
If someone modifies entry #100, entry #101's hash (which includes #100's hash) breaks. The entire chain downstream breaks. Tampering is immediately detectable.

### Pattern 5: Monthly Partitioning
```
transactions PARTITION BY RANGE (transaction_date)
-- transactions_2026_01, transactions_2026_02, etc.
```
Dashboard queries scan only relevant partitions. Old partitions can be archived to cold storage. Parallel query execution.

### Pattern 6: Merchant-First Indexing
```
CREATE INDEX idx_<table>_merchant_<column>
    ON <table>(merchant_id, <column>);
```
Every index leads with `merchant_id` because that's the RLS filter. No exceptions.

---

## Part 8: Coverage Scorecard

| Data Source | Fields Mapped | Coverage | Change Since Feb 16 |
|-------------|---------------|----------|---------------------|
| Transaction Header | 18/28 | 64% | Was 32% |
| Tender | 10/13 | 77% | Was 31% |
| Line Items | 14/21 | 67% | Was 0% (all JSONB) |
| Employee | 9/10 + 4 new | 90%+ | Was 60% |
| Product/Article | 7/11 | 64% | No change |
| Store/Location | 12/17 | 71% | Was 65% |
| Customer | 3/7 | 43% | No change |
| **Overall** | **73/107** | **68% raw** | **Was ~32%** |

**Weighted by LP significance: ~85% coverage.** The remaining gaps are primarily Square API limitations (supervisor overrides, merchandise hierarchy, scan gap timing) and post-MVP features (loyalty, training mode).

---

## Part 9: What Square Gives Us vs. What We Ingest

Jeremy's analysis (Feb 20) identified the breadth problem:

| Metric | Before Scope Expansion | After (Target) |
|--------|----------------------|----------------|
| Square API families actively used | 2 of 14+ | 8 of 14+ |
| Webhook event types subscribed | 4 | 20+ |
| Transaction types detected | 2 (sale, refund) | 8 (+ void, post-void, no-sale, paid in/out, exchange) |
| Chirp detection rules | 8 (payment-only) | 22 (multi-source cross-reference) |
| LP exposure coverage vs. enterprise ancestor | ~32% | ~85% |

**OAuth scopes required for full coverage:**

| Scope | Data Source | Sprint |
|-------|-----------|--------|
| `PAYMENTS_READ` | Payments API | ✅ Have |
| `ORDERS_READ` | Orders API (line items, tenders) | Sprint 2 |
| `CASH_DRAWER_READ` | Cash Drawer Shifts API | Sprint 2 |
| `TIMECARDS_READ` | Labor/Timecard API | Sprint 2 |
| `INVENTORY_READ` | Inventory API | Sprint 3 |
| `GIFTCARDS_READ` | Gift Cards API | Sprint 3 |
| `DISPUTES_READ` | Disputes API | Sprint 3 |
| `CUSTOMERS_READ` | Customer lifecycle events | ✅ Likely have |

---

## Part 10: Data Flow — Transaction to Case

```
1. Square Webhook → transactions (APPEND-ONLY)
2. → audit_log (hash-chained)
3. → ML scoring (transaction_features → risk_score)
4. → Chirp rule evaluation
5. IF alert triggered → alerts (IMMUTABLE)
6. → alert_history (status tracking)
7. → entity_risk_scores (updated)
8. → Dashboard surfaces alert
9. Manager reviews → "Open Case"
10. → cases (Fox) + case_timeline
11. → Upload evidence → case_evidence (INSERT-ONLY, SHA-256)
12. → evidence_access_log (who viewed, INSERT-ONLY)
13. → case_actions (investigate, terminate, refer to LE)
14. → Close or escalate
```

---

## Part 11: Rules for Everyone

### For Jeremy (writing code):
- Every new table MUST have `merchant_id` FK
- Every append-only table MUST have DB-level trigger preventing UPDATE/DELETE
- Every new field extraction from Square MUST trace to a CRDM field in this guide
- If you add a column, update this guide FIRST, then write the code
- The `payload` / `raw_data` JSONB column is your escape hatch — if Square sends it, we capture it

### For Tom (designing schema):
- Every entity pattern MUST trace to GSLM, CRDM, or Walmart precedent
- Effective dating on all reference/dimension tables
- Hierarchy support (parent_id pattern) where organizational grouping matters
- ARTS POSlog alignment check before any new canonical table

### For Eva (managing delivery):
- No sprint starts without a spec that references this guide
- Every acceptance criterion for a data feature must cite the CRDM field it satisfies
- Coverage scorecard (Part 8) updates with every sprint

### For Jim (testing):
- Every Chirp rule in Part 5 needs a corresponding test scenario
- Test immutability: attempt UPDATE/DELETE on append-only tables — must fail
- Test hash chain: verify audit_log integrity after every test run
- Test RLS: verify merchant isolation — no cross-tenant data leakage

### For Jess (documenting):
- This guide supersedes all previous CRDM/schema documents for field-level mapping
- The detailed docs (CRDM v1.0, Jeremy's API analysis, enterprise spec analysis) remain as supporting references
- When in conflict, THIS document wins

---

## Part 12: What We Don't Model (And Why)

| Gap | Reason | Resolution |
|-----|--------|------------|
| Supervisor overrides | Square doesn't expose register-level overrides via API | Fox manual entry for now |
| Merchandise hierarchy (Dept/Class/Subclass) | Square uses flat categories, not 3-level hierarchy | Tom's GSLM pattern can extend post-MVP |
| Scan gap timing | Hardware-level POS data, not accessible via API | Not applicable to Square integration |
| Loyalty points | Post-MVP, Square Loyalty API available | Sprint 4+ |
| Training transactions | POS training mode doesn't hit Square API | Not detectable via webhook |
| Paper coupons | Square doesn't have paper coupon tracking | N/A for modern POS |
| Vendor ID on products | Square doesn't track vendor at POS level | Bull module scope |
| PII (address/phone/email on customers) | **By design** — privacy-first approach | Not a gap, a principle |

---

## Document Hierarchy

This guide is the **logical synthesis**. The supporting documents provide depth:

```
THIS GUIDE (Master Data Model Guide)
  ├── Canary_CRDM_v1.0.md              — Field-by-field mapping detail
  ├── Square_API_LP_Coverage_Analysis    — Jeremy's 14-API analysis
  ├── Enterprise_Spec_Analysis           — Eva/Jess original spec parsing
  ├── GrowDirect_Unified_Data_Model      — Tom/Jeremy GSLM/CRDM patterns
  ├── SCHEMA_QUICK_REFERENCE.md          — Three-DB architecture & patterns
  └── Enterprise_LP_Data_Spec_v1.1.pdf   — The ancestor (Archive)
```

**When documents conflict, resolution order:**
1. This Master Guide (logical truth)
2. Canary CRDM v1.0 (field-level detail)
3. Live code (`canary/models.py` + `canary/fox/models.py`)
4. Supporting analysis docs

---

*"It all starts with the CRDM. Everything else is just window dressing."*
— Jeffe, February 20, 2026

---

*Canary LP | Confidential*
*Eva (PM) + Tom (Architect) + Jeremy (Dev Quant) | February 20, 2026*
