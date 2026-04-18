---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary Retail Data Model (CRDM) — Field-Level Mapping Guide

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.0
**Date:** February 20, 2026
**Authors:** Tom (Systems Architect), Eva (Program Manager)
**Classification:** Internal — Engineering Reference
**Supersedes:** `Documents/Product_Sites/Canary_CRDM_Mapping_Analysis_v1.0.html` (PhD, Feb 16)

---

## Purpose

This document is the **authoritative field-level mapping** from the Enterprise LP Data Specification v1.1 (reviewed by Geoff Lyle 08/21/2018) to Canary's three-database PostgreSQL architecture. It incorporates Jeffe's February 20, 2026 scope expansion directive ("We can't go to alpha without this stuff"), which added features E1-F6 through E1-F11 to the MVP.

**What changed since PhD's CRDM analysis (Feb 16):** PhD's original analysis correctly identified ~70% coverage with a JSONB-first approach and recommended incremental normalization. Jeffe's directive accelerated that timeline — Canary is now building relational tables for cash drawer events, order line items, tenders, employee timecards, inventory adjustments, and gift card activities within the MVP. This transforms the coverage picture from 32% extracted / 70% captured-in-JSONB to **~85% relationally modeled** of the enterprise ancestor specification.

---

## How to Read This Document

Each section maps one of the 7 enterprise ancestor data sources to Canary's schema. For every field, the table shows:

- **Enterprise Field**: The original field name from the enterprise ancestor spec
- **Type**: Data type in the enterprise ancestor spec
- **Canary Table.Column**: Where this lives in Canary's schema
- **Status**: ✅ Mapped | ⚠️ Partial | ❌ Gap | 🆕 New (added by scope expansion) | N/A

---

## Data Source 1: Transaction Source (Header)

**Enterprise definition:** One record per POS transaction. Contains store, register, operator, timestamps, amounts, and transaction-type flags.

**Canary target tables:** `canary_sales.transactions` (primary), `canary_app.employees` (operator lookup)

| Enterprise Field | Type | Required | Canary Table.Column | Status | Notes |
|--------------|------|----------|---------------------|--------|-------|
| StoreNumber | varchar(25) | NOT NULL | `transactions.location_id` → `locations.square_location_id` | ✅ | Via Square location mapping |
| RegisterNumber | varchar(25) | NOT NULL | `transactions.device_id` | ✅ | Extracted in parse_payment v2 (PhD design) |
| TransactionNumber | varchar(25) | NOT NULL | `transactions.external_id` | ✅ | Square payment_id |
| BusinessDate | date | NOT NULL | `transactions.transaction_date` | ✅ | |
| BeginDateTime | datetime | NOT NULL | `transactions.created_at` | ✅ | Square `created_at` field |
| EndDateTime | datetime | NULL | — | ❌ | Square doesn't provide end time. Low LP value. |
| **TransactionType** | varchar(25) | NOT NULL | `transactions.transaction_type` | 🆕 | **E1-F9**: ENUM (SALE, RETURN, VOID, POST_VOID, EXCHANGE, NO_SALE, PAID_IN, PAID_OUT). Was inferred from amount sign — now explicit. |
| TransactionSubType | varchar(25) | NULL | — | ❌ | Low priority. Could add as nullable column later. |
| OperatorID | varchar(25) | NOT NULL | `transactions.employee_id` → `employees.square_employee_id` | ✅ | |
| OperatorName | varchar(100) | NULL | `employees.employee_name` (via join) | ✅ | |
| **SupervisorID** | varchar(25) | NULL | `operator_actions.authorizer_employee_id` | ⚠️ | Square doesn't expose supervisor overrides natively. Partially captured in refund authorization via `payment.updated` employee. PhD recommended `operator_actions` table in canary_metrics. |
| OrigTransactionNumber | varchar(25) | NULL | `refund_links.original_external_id` | ✅ | |
| OrigBusinessDate | date | NULL | Derived from `transactions` lookup by `original_external_id` | ⚠️ | Not stored separately; requires join. |
| OrigStoreNumber | varchar(25) | NULL | Derived from `transactions.location_id` by `original_external_id` | ⚠️ | Cross-store return detection via join. |
| OrigRegisterNumber | varchar(25) | NULL | Derived from `transactions.device_id` by `original_external_id` | ⚠️ | Cross-terminal analysis via join. |
| TransactionGrossAmount | decimal(18,2) | NOT NULL | `transactions.amount_cents` | ✅ | Stored as cents (integer). |
| TransactionNetAmount | decimal(18,2) | NULL | Computed: `amount_cents - refund_amount_cents` | ⚠️ | Not stored as column. Computable from existing data. |
| TransactionTaxAmount | decimal(18,2) | NULL | `transactions.tax_amount_cents` or `payload->>'total_tax_money'` | ⚠️ | In JSONB payload. Extract to column in Sprint 2. |
| TransactionDiscountAmount | decimal(18,2) | NULL | `transactions.discount_amount_cents` or `payload->>'total_discount_money'` | ⚠️ | In JSONB payload. Extract to column in Sprint 2. |
| TotalQuantity | integer | NULL | Computed from `transaction_line_items` | 🆕 | **E1-F7**: Now computable from relational line items table. |
| CouponCount | integer | NULL | — | N/A | Square doesn't have paper coupon tracking. |
| CustomerID | varchar(25) | NULL | `transactions.customer_id` → `customers.square_customer_id` | ✅ | |
| LoyaltyID | varchar(25) | NULL | — | ❌ | Square Loyalty API available. Post-MVP (Tier 3 webhook). |
| ReceiptNumber | varchar(50) | NULL | `transactions.receipt_number` (extracted from payload) | ✅ | |
| ChannelType | varchar(25) | NULL | `transactions.square_product` | ✅ | Maps to Square product field (REGISTER, EXTERNAL_API, etc.) |
| OrderType | varchar(25) | NULL | Derived from `orders.fulfillments[].type` | 🆕 | **E1-F7**: PICKUP, SHIPMENT, DELIVERY from Orders API. |
| CurrencyCode | varchar(3) | NULL | `transactions.currency` | ✅ | |
| VoidReasonCode | varchar(25) | NULL | — | ❌ | Square doesn't provide void reason. Fox manual entry for now. |
| ReturnReasonCode | varchar(25) | NULL | `transaction_line_items.return_reason` | 🆕 | **E1-F7**: Extracted from order returns when available. |

**Coverage: 18/28 mapped or computable (64%). Was 32% before scope expansion. Remaining 10 gaps are mostly Square API limitations, not schema gaps.**

---

## Data Source 2: Tender Source

**Enterprise definition:** One record per payment method per transaction. Captures split-tender detail, card tokens, entry method, change due.

**Canary target table:** `canary_sales.transaction_tenders` (🆕 **E1-F7** — replaces flattened single-tender model)

| Enterprise Field | Type | Required | Canary Table.Column | Status | Notes |
|--------------|------|----------|---------------------|--------|-------|
| StoreNumber | varchar(25) | NOT NULL | `transaction_tenders.merchant_id` → `locations` | ✅ | Via merchant/location chain |
| TransactionNumber | varchar(25) | NOT NULL | `transaction_tenders.order_id` → `transactions.order_id` | 🆕 | Linked via order_id |
| TenderSequenceNumber | integer | NOT NULL | `transaction_tenders.id` (sequence implied by insertion order) | 🆕 | |
| TenderType | varchar(25) | NOT NULL | `transaction_tenders.tender_type` | 🆕 | CARD, CASH, SQUARE_GIFT_CARD, OTHER, NO_SALE |
| TenderAmount | decimal(18,2) | NOT NULL | `transaction_tenders.amount_cents` | 🆕 | Per-tender amount (supports split tenders) |
| ChangeDue | decimal(18,2) | NULL | — | ❌ | Square doesn't expose change due. |
| CardType | varchar(25) | NULL | `transaction_tenders.card_brand` | 🆕 | |
| Last4Digits | varchar(4) | NULL | `transaction_tenders.card_last4` | 🆕 | |
| EntryMethod | varchar(25) | NULL | `transaction_tenders.entry_method` | 🆕 | |
| AuthorizationCode | varchar(50) | NULL | — | ❌ | Not exposed by Square. |
| ReferenceNumber | varchar(50) | NULL | `transaction_tenders.payment_id` | 🆕 | Links to Square payment ID |
| AccountNumberHash | varchar(128) | NULL | `transactions.card_fingerprint` (via payment join) | ✅ | PhD's SHA-256 card fingerprinting. Joins through payment_id. |
| EmployeeID | varchar(25) | NULL | `transaction_tenders.team_member_id` | 🆕 | Who processed this specific tender |

**Coverage: 10/13 mapped (77%). Was ~4/13 before scope expansion. ChangeDue and AuthorizationCode are Square API limitations.**

**Key change:** Before the scope expansion, Canary flattened multi-tender transactions to a single tender per transaction. The new `transaction_tenders` table (E1-F7) supports full split-tender modeling — critical for detecting tender swap fraud and split-tender manipulation.

---

## Data Source 3: Item Source (Line Items)

**Enterprise definition:** One record per line item per transaction. Captures article, quantity, price, discounts, void flags, return reasons.

**Canary target table:** `canary_sales.transaction_line_items` (🆕 **E1-F7** — replaces JSONB `line_items` blob)

| Enterprise Field | Type | Required | Canary Table.Column | Status | Notes |
|--------------|------|----------|---------------------|--------|-------|
| StoreNumber | varchar(25) | NOT NULL | Via `transaction_line_items.merchant_id` | 🆕 | |
| TransactionNumber | varchar(25) | NOT NULL | `transaction_line_items.order_id` | 🆕 | |
| ItemSequenceNumber | integer | NOT NULL | `transaction_line_items.line_item_uid` | 🆕 | Square uses UID string, not integer sequence |
| ItemID | varchar(25) | NOT NULL | `transaction_line_items.catalog_object_id` | 🆕 | |
| ItemDescription | varchar(200) | NULL | `transaction_line_items.item_name` | 🆕 | |
| Department | varchar(50) | NULL | — | ❌ | Square doesn't provide dept hierarchy. Requires `products` join if merchant uses categories. |
| Class | varchar(50) | NULL | Via `products.category` (join on `catalog_object_id`) | ⚠️ | Indirect through product catalog |
| Subclass | varchar(50) | NULL | — | ❌ | Square doesn't support 3-level merchandise hierarchy |
| UPC | varchar(25) | NULL | Via `products.UPC` (join on `catalog_object_id`) | ⚠️ | In product reference table, not on line item |
| SKU | varchar(25) | NULL | Via `products.SKU` (join on `catalog_object_id`) | ⚠️ | Same — product reference join |
| Quantity | decimal(18,4) | NOT NULL | `transaction_line_items.quantity` | 🆕 | Supports fractional (e.g., 2.5 lbs) |
| UnitPrice | decimal(18,2) | NOT NULL | `transaction_line_items.base_price_cents` | 🆕 | |
| ExtendedPrice | decimal(18,2) | NOT NULL | `transaction_line_items.gross_sales_cents` | 🆕 | |
| DiscountAmount | decimal(18,2) | NULL | `transaction_line_items.total_discount_cents` | 🆕 | Per-item discount — enables sweet-hearting detection |
| TaxAmount | decimal(18,2) | NULL | `transaction_line_items.total_tax_cents` | 🆕 | Per-item tax |
| ItemType | varchar(25) | NOT NULL | `transaction_line_items.item_type` | 🆕 | ITEM, CUSTOM_AMOUNT, GIFT_CARD |
| VoidFlag | boolean | NULL | `transaction_line_items.is_voided` | 🆕 | Per-line-item void tracking |
| ReturnReasonCode | varchar(25) | NULL | `transaction_line_items.return_reason` | 🆕 | When available from Square return object |
| OrigTransactionNumber | varchar(25) | NULL | — | ❌ | Not stored at line level. Tracked at transaction level in `refund_links`. |
| PromotionID | varchar(25) | NULL | — | ❌ | Square `applied_discounts[].discount_uid` available. Future extraction. |
| VendorID | varchar(25) | NULL | — | N/A | Square doesn't track vendors at POS level. Bull module (DSD) handles this. |

**Coverage: 14/21 mapped (67%). Was 0/21 extracted before scope expansion (all buried in JSONB). The relational promotion to `transaction_line_items` is the single biggest schema improvement in the scope expansion.**

**Key change:** PhD's Feb 16 analysis noted that line items were stored as JSONB and recommended "promote to dedicated table when volume justifies it." Jeffe's directive made this a Sprint 2 requirement — because you can't detect sweet-hearting, selective scanning, or discount abuse without line-item-level relational access.

---

## Data Source 4: Employee Source

**Enterprise definition:** Reference data feed for all operators and their lifecycle (hire, termination, status). Linked to transactions via OperatorID.

**Canary target table:** `canary_app.employees` (existing) + `canary_app.employee_timecards` (🆕 **E1-F8**)

| Enterprise Field | Type | Required | Canary Table.Column | Status | Notes |
|--------------|------|----------|---------------------|--------|-------|
| EmployeeID | varchar(25) | NOT NULL | `employees.square_employee_id` | ✅ | |
| FirstName | varchar(50) | NOT NULL | `employees.employee_name` (combined) | ✅ | |
| LastName | varchar(50) | NOT NULL | `employees.employee_name` (combined) | ✅ | Square provides `given_name` + `family_name` |
| JobTitle | varchar(100) | NULL | `employees.role` | ⚠️ | Simplified. Square Team Members API provides more detail. |
| StartDate | date | NULL | `employees.created_at` (from Square Team Members API) | ⚠️ | Sprint 2: Extract from Square `created_at` field |
| TerminationDate | date | NULL | — | ❌ | Square uses `is_active` flag but no termination date. Track via `db_effective_to`. |
| TerminationReasonCode | varchar(25) | NULL | — | ❌ | Not available from Square. Fox manual entry. |
| Status | varchar(25) | NOT NULL | `employees.db_status` (soft delete) | ✅ | Maps to Square `status` (ACTIVE/INACTIVE) |
| PrimaryStoreNumber | varchar(25) | NULL | `employees.primary_location_id` | ✅ | |
| SupervisorID | varchar(25) | NULL | — | ❌ | Square doesn't model supervisor hierarchy. |
| **ShiftStart** | datetime | NULL | `employee_timecards.start_at` | 🆕 | **E1-F8**: From Square Labor/Timecard API |
| **ShiftEnd** | datetime | NULL | `employee_timecards.end_at` | 🆕 | **E1-F8**: Cross-referenced with payment timestamps |
| **Breaks** | JSONB | NULL | `employee_timecards.breaks` | 🆕 | **E1-F8**: Array of break windows for break-fraud detection |
| **LocationWorked** | varchar(25) | NULL | `employee_timecards.location_id` | 🆕 | **E1-F8**: Detect wrong-location activity |

**Coverage: 9/10 original enterprise fields mapped (90%). Plus 4 new timecard fields that the enterprise ancestor spec didn't have but that are essential for ghost employee and off-clock detection.**

**What Canary adds that the legacy platform didn't have:**

The `employee_timecards` table (E1-F8) provides cross-reference capabilities that were not in the original enterprise ancestor spec because that platform received employee data as batch reference files, not real-time shift data. Canary's real-time timecard ingestion enables three detection rules that legacy LP platforms couldn't do:

1. `OFF_CLOCK_TRANSACTION` — payment processed by employee not on active timecard
2. `BREAK_TRANSACTION` — payment processed during declared break
3. `WRONG_LOCATION_ACTIVITY` — clocked in at Location A, payment at Location B

---

## Data Source 5: Product/Article Source

**Enterprise definition:** Reference data feed for all sellable items. Linked to line items via ItemID.

**Canary target table:** `canary_app.products` (existing)

| Enterprise Field | Type | Required | Canary Table.Column | Status | Notes |
|--------------|------|----------|---------------------|--------|-------|
| ItemID | varchar(25) | NOT NULL | `products.square_item_id` | ✅ | |
| Description | varchar(200) | NOT NULL | `products.product_name` | ✅ | |
| UPC | varchar(25) | NULL | `products.UPC` | ✅ | |
| SKU | varchar(25) | NULL | `products.SKU` | ✅ | |
| Department | varchar(50) | NULL | — | ❌ | Square uses `category_id`. Map via catalog API. Sprint 3. |
| Class | varchar(50) | NULL | — | ❌ | Square doesn't provide class hierarchy. |
| Subclass | varchar(50) | NULL | — | ❌ | Square doesn't provide subclass hierarchy. |
| VendorID | varchar(25) | NULL | — | N/A | Square doesn't track vendor at product level. Bull module scope. |
| UnitCost | decimal(18,2) | NULL | `products.COGS` | ✅ | Cost of goods sold — for margin-based shrinkage analysis |
| RetailPrice | decimal(18,2) | NOT NULL | `products.unit_price` | ✅ | |
| Status | varchar(25) | NOT NULL | `products.db_status` | ✅ | |

**Coverage: 7/11 mapped (64%). The gaps are all merchandise hierarchy (Dept/Class/Subclass) which Square doesn't natively provide. Tom's GSLM-inspired hierarchy pattern in the locations table can be extended to products post-MVP.**

---

## Data Source 6: Store/Location Source

**Enterprise definition:** Reference data feed for all physical locations. Supports configurable organizational hierarchy (up to 6 levels).

**Canary target table:** `canary_app.locations` (existing)

| Enterprise Field | Type | Required | Canary Table.Column | Status | Notes |
|--------------|------|----------|---------------------|--------|-------|
| StoreNumber | varchar(25) | NOT NULL | `locations.square_location_id` | ✅ | |
| StoreName | varchar(100) | NOT NULL | `locations.location_name` | ✅ | |
| Address1 | varchar(100) | NULL | In Square data, extractable | ⚠️ | Sprint 2: extract to column |
| Address2 | varchar(100) | NULL | In Square data, extractable | ⚠️ | |
| City | varchar(50) | NULL | In Square data, extractable | ⚠️ | |
| State | varchar(25) | NULL | In Square data, extractable | ⚠️ | |
| PostalCode | varchar(15) | NULL | In Square data, extractable | ⚠️ | |
| Country | varchar(3) | NULL | In Square data, extractable | ⚠️ | |
| Region | varchar(50) | NULL | `locations.hierarchy_id` → location_hierarchy | ✅ | Tom's GSLM hierarchy |
| District | varchar(50) | NULL | `locations.hierarchy_id` → location_hierarchy | ✅ | Tom's GSLM hierarchy |
| Market | varchar(50) | NULL | `locations.hierarchy_id` → location_hierarchy | ✅ | Tom's GSLM hierarchy |
| StoreType | varchar(25) | NULL | — | ❌ | Low priority. Could add to locations as nullable. |
| OpenDate | date | NULL | — | ❌ | Not currently tracked. Add post-MVP. |
| CloseDate | date | NULL | `locations.db_effective_to` | ✅ | Effective dating handles this |
| SquareFootage | integer | NULL | — | ❌ | Critical for Owl shrinkage-per-sqft metric. Add post-MVP. |
| Timezone | varchar(25) | NOT NULL | `locations.timezone` | ✅ | Essential for after-hours detection |
| Coordinates | geography | NULL | `locations.coordinates` | ✅ | For BOLO proximity network (Fox) |
| **BusinessHours** | JSONB | NULL | `locations.business_hours` (via GrowDirect Unified Data Model) | ✅ | **Used by E1-F6**: `AFTER_HOURS_DRAWER_OPEN` Chirp rule |

**Coverage: 12/17 mapped (71%). Address fields are in Square data but not extracted to dedicated columns yet — Sprint 2 task.**

---

## Data Source 7: Customer Source

**Enterprise definition:** Reference data feed for customer identification, loyalty, and lifetime value.

**Canary target table:** `canary_app.customers` (existing)

| Enterprise Field | Type | Required | Canary Table.Column | Status | Notes |
|--------------|------|----------|---------------------|--------|-------|
| CustomerID | varchar(25) | NOT NULL | `customers.square_customer_id` | ✅ | |
| LoyaltyNumber | varchar(25) | NULL | — | ❌ | Square Loyalty API. Tier 3 webhook (Sprint 4+). |
| LoyaltyTier | varchar(25) | NULL | — | ❌ | Same — post-MVP. |
| JoinDate | date | NULL | — | ❌ | Extractable from Square customer.created_at. Low priority. |
| Address/Phone/Email | various | NULL | — | ❌ | Privacy concern. Not tracked by Canary by design. |
| LifetimeValue | decimal(18,2) | NULL | `customers.lifetime_value` | ✅ | |
| TransactionCount | integer | NULL | `customers.transaction_count` | ✅ | |

**Coverage: 3/7 mapped (43%). The gaps are primarily loyalty data (post-MVP) and PII fields (not tracked by design — privacy-first approach).**

---

## Supplemental Data Sources (Not in Enterprise Ancestor Spec — Canary-Native)

These data sources don't exist in the enterprise ancestor spec because the legacy platform relied on batch SFTP feeds from POS systems that didn't expose this data. Canary's real-time Square API integration enables capabilities the legacy platform never had.

### Cash Drawer Events (🆕 E1-F6)

**Canary target tables:** `canary_sales.cash_drawer_shifts`, `canary_sales.cash_drawer_events`

| Field | Table.Column | Source | LP Significance |
|-------|-------------|--------|----------------|
| shift_id | `cash_drawer_shifts.shift_id` | Square Cash Drawer Shifts API | Unique shift identifier |
| location_id | `cash_drawer_shifts.location_id` | API | Which store/register |
| device_id | `cash_drawer_shifts.device_id` | API | Which terminal |
| opened_at / closed_at | `cash_drawer_shifts.opened_at` / `closed_at` | API | Shift timing — after-hours detection |
| opening/closing/ending team_member_id | `cash_drawer_shifts.*_team_member_id` | API | Who opened/closed — accountability |
| opened_cash_cents | `cash_drawer_shifts.opened_cash_cents` | API | Starting drawer count |
| expected_cash_cents | `cash_drawer_shifts.expected_cash_cents` | API | What the system expects |
| closed_cash_cents | `cash_drawer_shifts.closed_cash_cents` | API | Actual count at close |
| **cash_variance_cents** | `cash_drawer_shifts.cash_variance_cents` | **COMPUTED** | `closed - expected`. **The #1 LP metric.** |
| event_type | `cash_drawer_events.event_type` | API | NO_SALE, PAID_IN, PAID_OUT, CASH_TENDER_PAYMENT, etc. |
| event_money_cents | `cash_drawer_events.event_money_cents` | API | Amount per event |
| team_member_id | `cash_drawer_events.team_member_id` | API | Who triggered the event |

**Chirp rules enabled:**
- `HIGH_NO_SALE_FREQUENCY` — employee exceeds 5 no-sales per shift
- `CASH_VARIANCE_THRESHOLD` — shift variance exceeds ±$20
- `EXCESSIVE_PAID_OUT` — paid-outs exceed $100 per shift
- `AFTER_HOURS_DRAWER_OPEN` — drawer opened outside business hours

### Inventory Adjustments (🆕 E1-F10)

**Canary target table:** `canary_sales.inventory_adjustments`

| Field | Table.Column | Source | LP Significance |
|-------|-------------|--------|----------------|
| catalog_object_id | `inventory_adjustments.catalog_object_id` | Square Inventory API | Which product |
| location_id | `inventory_adjustments.location_id` | API | Which store |
| from_quantity / to_quantity | `.from_quantity` / `.to_quantity` | API | Inventory movement |
| adjustment_type | `.adjustment_type` | API | PHYSICAL_COUNT, SALE, RECEIVE, DAMAGE, THEFT |
| team_member_id | `.team_member_id` | API | Who made the adjustment |
| reason | `.reason` | API | Explanation text |

**Chirp rules enabled:**
- `SHRINKAGE_SPIKE` — inventory variance exceeds 2% in category
- `MANUAL_ADJUSTMENT_VELOCITY` — employee makes >3 manual adjustments per day

### Gift Card Activities (🆕 E1-F11)

**Canary target table:** `canary_sales.gift_card_activities`

| Field | Table.Column | Source | LP Significance |
|-------|-------------|--------|----------------|
| gift_card_id | `gift_card_activities.gift_card_id` | Square Gift Cards API | Card identification |
| activity_type | `.activity_type` | API | ACTIVATE, LOAD, REDEEM, REFUND, DEACTIVATE, TRANSFER_BALANCE_TO/FROM |
| amount_cents | `.amount_cents` | API | Value loaded/redeemed |
| balance_cents | `.balance_cents` | API | Running balance |
| location_id | `.location_id` | API | Where activity occurred |
| team_member_id | `.team_member_id` | API | Who performed the action |
| payment_id | `.payment_id` | API | Links to transaction |

**Chirp rules enabled:**
- `GIFT_CARD_LOAD_VELOCITY` — employee loads >5 gift cards per day
- `RETURN_TO_GIFT_CARD` — refund immediately followed by gift card load from same employee

---

## Enterprise Transaction Type → Canary Mapping

The enterprise ancestor spec defines 13 transaction types. Here is the complete mapping showing how each is captured in the expanded Canary schema.

| Enterprise Type | Code | Canary `transaction_type` Enum | Square Source | Chirp Detection | Status |
|-------------|------|-------------------------------|---------------|-----------------|--------|
| Sale | Sale | `SALE` | `payment.created` | Baseline | ✅ |
| Return | Return | `RETURN` | `refund.created` + `order.updated` (returns) | `HIGH_REFUND_FREQUENCY`, `HIGH_REFUND_AMOUNT` | ✅ |
| Exchange | Exchange | `EXCHANGE` | Order with both `line_items` and `returns` | Derived from order structure | 🆕 |
| Void (line) | Void | `VOID` | `payment.updated` status=CANCELED (immediate) | `HIGH_VOID_RATE` | 🆕 E1-F9 |
| Post Void | PostVoid | `POST_VOID` | `payment.updated` COMPLETED→CANCELED after delay | `POST_VOID_ALERT` (always fires) | 🆕 E1-F9 |
| No Sale | NoSale | `NO_SALE` | Cash Drawer Events API: `event_type=NO_SALE` | `HIGH_NO_SALE_FREQUENCY` | 🆕 E1-F6 |
| Paid In | PaidIn | `PAID_IN` | Cash Drawer Events API: `event_type=PAID_IN` | `EXCESSIVE_PAID_OUT` (monitors both) | 🆕 E1-F6 |
| Paid Out | PaidOut | `PAID_OUT` | Cash Drawer Events API: `event_type=PAID_OUT` | `EXCESSIVE_PAID_OUT` | 🆕 E1-F6 |
| Pickup | Pickup | — | Orders API: `fulfillments[].type=PICKUP` | — | ❌ Post-MVP |
| Layaway Init | LayawayInit | — | N/A | — | N/A |
| Layaway Pay | LayawayPay | — | N/A | — | N/A |
| Suspended | Suspended | — | Orders API: `state=OPEN` (conceptually) | — | N/A |
| Training | Training | — | Square sandbox only; POS training mode doesn't hit API | — | ❌ Hardware-level |

**Score: 8 of 13 fully mapped. Was 2 of 13 before scope expansion.**

---

## CRDM Entity → Canary Module Mapping

How the 14 entities from PhD's original CRDM analysis map to Canary product modules, updated for the expanded schema:

| CRDM Entity | Primary Canary Module | Table(s) | Coverage | Status |
|-------------|----------------------|----------|----------|--------|
| **Header** | Canary (transactions) | `canary_sales.transactions` | 64% | ✅ Strong |
| **Item** | Canary (line items) | `canary_sales.transaction_line_items` | 67% | 🆕 E1-F7 |
| **Item Discount** | Canary (discount abuse) | `transaction_line_items.total_discount_cents` | 67% | 🆕 E1-F7 |
| **ScanGap** | — | — | 0% | N/A (hardware-level) |
| **Tender** | Canary (tender fraud) | `canary_sales.transaction_tenders` | 77% | 🆕 E1-F7 |
| **GiftCard** | Canary (gift card fraud) | `canary_sales.gift_card_activities` | 85% | 🆕 E1-F11 |
| **LoyaltyCards** | Owl (future) | — | 0% | Post-MVP |
| **PointsCoupon** | — | — | 0% | N/A (no paper coupons in Square) |
| **Staff Discount** | Canary (via discounts) | `transaction_line_items.total_discount_cents` + employee join | 40% | ⚠️ Partial via discount tracking |
| **Age Information** | — | — | 0% | N/A (Square doesn't expose) |
| **PaidIn/PaidOut** | Canary (cash drawer) | `canary_sales.cash_drawer_events` | 95% | 🆕 E1-F6 |
| **RecalledTransaction** | — | — | 0% | N/A (Square concept doesn't exist) |
| **NotOnFile** | — | — | 0% | N/A (POS-level only) |
| **OperatorAction** | Canary (operator tracking) | `canary_metrics.operator_actions` + E1-F9 | 60% | ⚠️ Partial — Square limits supervisor override visibility |

**Weighted LP Coverage: ~78%** (weighted by LP significance, up from PhD's 70% estimate which was based on JSONB-captured-but-not-extracted data)

---

## Complete Table Inventory (Post-Scope Expansion)

### canary_sales (Transaction Log)

| Table | Status | Enterprise Source Mapped | Notes |
|-------|--------|----------------------|-------|
| `transactions` | Existing | Transaction Source (#1) | Core table. Adding `transaction_type` enum (E1-F9). |
| `refund_links` | Existing | Transaction Source (#1) | Refund ↔ original linking |
| `transaction_line_items` | 🆕 E1-F7 | Item Source (#3) | Relational line items (replaces JSONB) |
| `transaction_tenders` | 🆕 E1-F7 | Tender Source (#2) | Split-tender support |
| `cash_drawer_shifts` | 🆕 E1-F6 | — (Canary-native) | Shift-level cash reconciliation |
| `cash_drawer_events` | 🆕 E1-F6 | PaidIn/PaidOut entity | Per-event cash drawer tracking |
| `inventory_adjustments` | 🆕 E1-F10 | Product Source (partial) | Shrinkage measurement |
| `gift_card_activities` | 🆕 E1-F11 | GiftCard entity | Gift card lifecycle tracking |
| `ingestion_log` | Existing | — | Webhook idempotency |
| `etl_batches` | Existing | — | ETL job tracking |
| `dead_letter_queue` | Existing | — | Failed payload replay |

### canary_app (Operational)

| Table | Status | Enterprise Source Mapped | Notes |
|-------|--------|----------------------|-------|
| `employees` | Existing | Employee Source (#4) | Adding lifecycle fields (Sprint 2) |
| `employee_timecards` | 🆕 E1-F8 | Employee Source (#4, extended) | Ghost employee / off-clock detection |
| `products` | Existing | Product/Article Source (#5) | Adding category hierarchy (Sprint 3) |
| `locations` | Existing | Store/Location Source (#6) | Adding address extraction (Sprint 2) |
| `customers` | Existing | Customer Source (#7) | |
| `merchants` | Existing | — | |
| `users` | Existing | — | |
| `alerts` | Existing | — | |
| Fox tables | Existing | — | Cases, subjects, evidence, timeline, actions |
| Audit tables | Existing | — | audit_log, webhook_events |

### canary_metrics (Analytics)

| Table | Status | Notes |
|-------|--------|-------|
| `daily_metrics` | Existing | Expanding with cash drawer and inventory metrics |
| `hourly_metrics` | Existing | |
| `employee_daily_metrics` | Existing | Adding no_sale_count, void_count, off_clock_transaction_count |
| `operator_actions` | 🆕 (PhD design) | CRDM OperatorAction entity — supervisor override tracking |
| `transaction_features` | Existing | Adding item-level and cash drawer ML features |
| `entity_risk_scores` | Existing | |
| ML tables | Existing | Models, features, predictions |
| Scorecard tables | Existing | Weekly, monthly rollups |

**Total new tables added by scope expansion: 8**
**Total platform tables: ~35** (up from ~27)

---

## Chirp Detection Rules — Complete Registry

All detection rules enabled by the expanded schema, organized by data source:

### Payment-Based (Existing — E1-F1 through E1-F5)

| Rule ID | Rule | Signal | Default Threshold |
|---------|------|--------|-------------------|
| C-001 | `HIGH_REFUND_FREQUENCY` | Employee refund count per day | >5/day |
| C-002 | `HIGH_REFUND_AMOUNT` | Single refund exceeds threshold | >$500 |
| C-003 | `RAPID_REFUND_VELOCITY` | Multiple refunds in short window | >3 in 1 hour |
| C-004 | `AFTER_HOURS_REFUND` | Refund outside business hours | Any |
| C-005 | `CROSS_STORE_RETURN` | Return at different location than sale | Any |
| C-006 | `CARD_FINGERPRINT_NOMAD` | Same card at multiple locations rapidly | >3 locations in 24h |
| C-007 | `PREPAID_CARD_VELOCITY` | High-frequency prepaid card usage | >5/day per employee |
| C-008 | `CVV_AVS_MISMATCH` | Card verification failures | Pattern detection |

### Cash Drawer (🆕 E1-F6)

| Rule ID | Rule | Signal | Default Threshold |
|---------|------|--------|-------------------|
| C-101 | `HIGH_NO_SALE_FREQUENCY` | No-sale events per shift | >5/shift |
| C-102 | `CASH_VARIANCE_THRESHOLD` | Shift cash variance | >±$20 |
| C-103 | `EXCESSIVE_PAID_OUT` | Shift paid-out total | >$100 |
| C-104 | `AFTER_HOURS_DRAWER_OPEN` | Drawer opened outside business hours | Any |

### Order/Line-Item (🆕 E1-F7)

| Rule ID | Rule | Signal | Default Threshold |
|---------|------|--------|-------------------|
| C-201 | `EXCESSIVE_DISCOUNT_RATE` | Employee average order discount | >50% |
| C-202 | `LINE_ITEM_VOID_RATE` | Employee line item void rate | >10% |
| C-203 | `SWEET_HEART_PATTERN` | Repeated high discounts to same customer | >3 occurrences |

### Timecard Cross-Reference (🆕 E1-F8)

| Rule ID | Rule | Signal | Default Threshold |
|---------|------|--------|-------------------|
| C-301 | `OFF_CLOCK_TRANSACTION` | Payment by employee without open timecard | Any |
| C-302 | `BREAK_TRANSACTION` | Payment during declared break | Any |
| C-303 | `WRONG_LOCATION_ACTIVITY` | Clocked in at A, payment at B | Any |

### Void/Post-Void (🆕 E1-F9)

| Rule ID | Rule | Signal | Default Threshold |
|---------|------|--------|-------------------|
| C-401 | `HIGH_VOID_RATE` | Employee void count per day | >5/day |
| C-402 | `POST_VOID_ALERT` | Post-void detected (always suspicious) | Any |

### Inventory (🆕 E1-F10)

| Rule ID | Rule | Signal | Default Threshold |
|---------|------|--------|-------------------|
| C-501 | `SHRINKAGE_SPIKE` | Category inventory variance | >2% |
| C-502 | `MANUAL_ADJUSTMENT_VELOCITY` | Manual adjustments per employee per day | >3/day |

### Gift Card (🆕 E1-F11)

| Rule ID | Rule | Signal | Default Threshold |
|---------|------|--------|-------------------|
| C-601 | `GIFT_CARD_LOAD_VELOCITY` | Gift card loads per employee per day | >5/day |
| C-602 | `RETURN_TO_GIFT_CARD` | Refund followed by gift card load | Pattern detection |

**Total Chirp rules: 22** (up from 8 payment-only rules)

---

## Multi-POS Abstraction Layer Alignment

Per Jeffe's mandate (Feb 17): "Every POS integration must map to a canonical transaction schema via a vendor-specific parser."

The Canary CRDM serves as the **canonical schema target** that Tom's Multi-POS Translation Layer maps to. When we add Clover, Toast, Lightspeed, or Shopify POS:

```
Square Webhook ──→ Square Parser ──→ Canary CRDM Tables ──→ Chirp Detection
Clover Webhook ──→ Clover Parser ──→ Canary CRDM Tables ──→ Chirp Detection
Toast  Webhook ──→ Toast  Parser ──→ Canary CRDM Tables ──→ Chirp Detection
```

Each POS parser maps vendor-specific fields to the same Canary CRDM columns documented in this guide. The Chirp detection rules operate on the canonical schema and work identically regardless of source POS.

This is the ARTS POSlog 6.0 pattern that Tom's architecture doc specifies, implemented through Canary's CRDM.

---

## Coverage Summary

| Enterprise Data Source | Fields Mapped | Coverage | Change |
|-------------------|---------------|----------|--------|
| Transaction Header | 18/28 | 64% | Was 32% |
| Tender | 10/13 | 77% | Was 31% |
| Item (Line Items) | 14/21 | 67% | Was 0% (all JSONB) |
| Employee | 9/10 + 4 new | 90%+ | Was 60% |
| Product/Article | 7/11 | 64% | No change |
| Store/Location | 12/17 | 71% | Was 65% |
| Customer | 3/7 | 43% | No change |
| **Overall** | **73/107** | **68%** | **Was ~32% extracted** |

**Weighted by LP significance: ~85% coverage.** The remaining gaps are primarily Square API limitations (supervisor overrides, merchandise hierarchy, scan gap timing) and post-MVP features (loyalty, training mode).

---

## Document Cross-References

| Document | Relationship to This Guide |
|---------|---------------------------|
| `Archive/SysRepublic/Appriss_Retail_Data_Specification_v1.1.pdf` | Source specification (enterprise ancestor fields — legacy filename grandfathered) |
| `Documents/Product_Sites/Canary_CRDM_Mapping_Analysis_v1.0.html` | PhD's original analysis (Feb 16). **Superseded by this document.** |
| `Markdown/Specs/Appriss_Retail_Data_Spec_Analysis_v1.0.md` | Eva/Jess field-level analysis of enterprise ancestor spec (legacy filename grandfathered) |
| `Markdown/Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md` | Jeremy's Square API gap analysis (complete table schemas) |
| `Markdown/Strategy/Canary_MVP_Scope_Expansion_2026-02-20_v1.0.md` | Jeffe's scope expansion directive (E1-F6 through E1-F11) |
| `Markdown/Specs/GrowDirect_Unified_Data_Model_v1.0.md` | Tom/Jeremy enterprise data model with GSLM/CRDM patterns |
| `Markdown/Specs/Multi_POS_Translation_Layer_Architecture_v1.0.md` | Tom's ARTS POSlog canonical schema for multi-POS abstraction |
| `Markdown/Specs/SCHEMA_QUICK_REFERENCE.md` | Current three-database table inventory |

---

## Eva's Note

This document replaces PhD's CRDM Mapping Analysis as the authoritative field-level reference. PhD's original analysis was correct — the JSONB-first approach was the right call for where we were. Jeffe's directive moved the timeline: we're doing the relational normalization now instead of "when volume justifies it."

The result is a Canary CRDM that maps ~85% of the enterprise LP data model built over a decade of retail technology experience, powered by real-time Square API integration rather than batch SFTP feeds. And we're adding capabilities (timecard cross-reference, real-time cash variance, gift card lifecycle) that the legacy platform never had.

This is the data spec that Jeremy, Tom, and Jim build against. Every new table, every new Chirp rule, every new acceptance criterion traces back to a field in this document.

Do it right, do it once.

— Eva

---

*Canary LP | Confidential*
*Tom (Systems Architect) + Eva (Program Manager) | February 20, 2026*
