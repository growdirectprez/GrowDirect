---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Square API — Full LP Data Coverage Analysis

**Version:** 1.0
**Date:** February 20, 2026
**Prepared by:** Jeremy (Developer Quant)
**Triggered by:** Eva/Jess Enterprise LP Data Specification v1.1 analysis
**Classification:** Internal — Engineering Reference
**Purpose:** Map every Square API data source against the enterprise ancestor spec to identify what we're leaving on the table

---

## Executive Summary

**We are currently ingesting 2 of 14+ available Square API data sources.**

Canary subscribes to `payment.created`, `payment.updated`, `refund.created`, and `refund.updated` webhooks. That's it. Square exposes at least **14 distinct API families** with LP-relevant data, including a full **Cash Drawer Shifts API** that literally tracks no-sales, paid-ins, paid-outs, and cash tender events — the exact operator actions the enterprise ancestor spec identifies as critical for LP.

This document maps every available Square data source against the Enterprise LP Data Specification v1.1, identifies what we're missing, and provides extraction recommendations with priority.

---

## 1. What We Currently Ingest

### Webhook Subscriptions (Active)

| Event | Handler | Data Extracted |
|-------|---------|----------------|
| `payment.created` | `square_client.py:444` | 26 fields via `parse_payment_to_transaction` v2 |
| `payment.updated` | `square_client.py:444` | Same as above |
| `refund.created` | `square_client.py:453` | refund_id, payment_id, refund_data blob |
| `refund.updated` | `square_client.py:453` | Same as above |

**That's 4 event types out of 40+ available webhook event types.**

### Payment Object Fields Extracted (v2 — 26 fields)

Already extracting: amount, currency, status, created_at, location_id, employee_id/team_member_id, card_brand, card_last4, card_fingerprint, card_bin, card_type, card_prepaid_type, entry_method, cvv_status, avs_status, device_id, risk_level, customer_id, order_id, square_product, tip_cents, is_offline, refund_ids, refunded_money, line_items (JSONB from order), receipt_number.

**Assessment: The payment extraction is solid after PhD's v2 upgrade. The problem is not depth — it's breadth. We're only looking at one data source when Square gives us fourteen.**

---

## 2. Square API Data Sources We Are NOT Ingesting

### 2.1 CASH DRAWER SHIFTS API — 🔴 CRITICAL GAP

**Enterprise ancestor equivalent:** Operator Actions (Section 2, highest-priority data source for LP)
**Square endpoint:** `GET /v2/cash-drawers/shifts` and `GET /v2/cash-drawers/shifts/{shift_id}/events`
**Permission required:** `CASH_DRAWER_READ`

**This API literally gives us every cash drawer event for every shift:**

| CashDrawerEventType | LP Significance | Priority |
|---------------------|----------------|----------|
| `NO_SALE` | **#1 LP signal.** No-sale opens the cash drawer without a transaction. High-frequency no-sales = internal theft indicator. Amount is always zero. | 🔴 P0 |
| `PAID_IN` | Money added to drawer for non-transaction reasons. Could indicate loan sharking, unreported sales, or cash manipulation. | 🔴 P0 |
| `PAID_OUT` | Money removed from drawer (e.g., paying delivery driver). Excessive paid-outs = potential embezzlement channel. | 🔴 P0 |
| `CASH_TENDER_PAYMENT` | Cash payment events — ties to drawer balance reconciliation. | P1 |
| `CASH_TENDER_CANCELLED_PAYMENT` | Split tender cancellation after cash tendered — potential sweet-hearting. | 🔴 P0 |
| `CASH_TENDER_REFUND` | Cash refund given from drawer — phantom refund detection. | 🔴 P0 |
| `OTHER_TENDER` | Non-cash payment on drawer (check, gift card) — gift card fraud vector. | P1 |

**The CashDrawerShift object also provides:**
- `opened_at`, `closed_at`, `ended_at` — shift timing (after-hours detection)
- `opening_team_member_id`, `closing_team_member_id`, `ending_team_member_id` — who opened/closed
- `opened_cash_money` — starting drawer amount
- `expected_cash_money` vs. `closed_cash_money` — **CASH VARIANCE** (the single most important LP metric for cash-handling fraud)
- `cash_payment_money`, `cash_refund_money`, `cash_paid_in_money`, `cash_paid_out_money` — per-shift totals
- `device` — the terminal/device used

**What this means for Chirp:** We can build a `cash_drawer_variance` alert that fires when `closed_cash_money - expected_cash_money` exceeds a threshold. We can count `NO_SALE` events per employee per shift. We can flag `PAID_OUT` events above a dollar threshold. This is the foundation of traditional LP and we're currently blind to it.

**Recommended implementation:**
1. Poll `ListCashDrawerShifts` daily per location (read-only API, no webhooks available)
2. For each shift, poll `ListCashDrawerShiftEvents` to get individual events
3. Store in new `cash_drawer_shifts` and `cash_drawer_events` tables in `canary_sales`
4. Add Chirp detection rules: high no-sale frequency, cash variance threshold, after-hours drawer opens

---

### 2.2 ORDERS API — 🟡 HIGH VALUE

**Enterprise ancestor equivalent:** Item Source (line items, discounts, taxes, voids)
**Square endpoint:** `GET /v2/orders/{order_id}`, webhooks `order.created`, `order.updated`, `order.fulfillment_updated`
**Permission required:** `ORDERS_READ`

**What the Order object gives us that Payments don't:**

| Order Field | LP Significance | Current Status |
|-------------|----------------|----------------|
| `line_items[]` (full detail) | Item-level fraud: selective scanning, sweet-hearting, price overrides | ⚠️ Partial — in JSONB |
| `line_items[].applied_discounts[]` | Sweet-hearting: employee applying unauthorized discounts to friends/family | ❌ Not parsed |
| `line_items[].applied_taxes[]` | Tax manipulation: under-collecting tax | ❌ Not parsed |
| `line_items[].modifiers[]` | Modifier fraud: not charging for add-ons | ❌ Not parsed |
| `discounts[]` (order-level) | Whole-order discounts — unauthorized comp meals, etc. | ❌ Not tracked |
| `returns[]` | **Itemized return detail** — which specific items were returned | ❌ Not tracked |
| `refunds[]` | Refund detail at order level | ⚠️ Via refund webhook only |
| `fulfillments[]` | Fulfillment fraud: marking orders fulfilled when not shipped | ❌ Not tracked |
| `state` (OPEN/COMPLETED/CANCELED/DRAFT) | Order lifecycle — canceled orders = potential void signal | ❌ Not tracked |
| `tenders[]` | **Split-tender detail** — multiple payment methods on one order | ❌ Not tracked |
| `service_charges[]` | Service charge manipulation | ❌ Not tracked |

**Why this matters:** The enterprise ancestor spec models the Item Source and Tender Source as separate entities precisely because line-item and tender-level detail is where LP discovers fraud patterns. A $50 order with 10 items tells a different story than a $50 order with 1 item. We need both.

**Recommended implementation:**
1. Subscribe to `order.created` and `order.updated` webhooks
2. On every order event, parse full line_items, discounts, taxes, returns, tenders
3. Store in `transaction_line_items` and `transaction_tenders` relational tables (not JSONB)
4. Backfill historical orders via `SearchOrders` API for existing merchants

---

### 2.3 LABOR / TIMECARDS API — 🟡 HIGH VALUE

**Enterprise ancestor equivalent:** Employee Source (login/logout, shift times, breaks)
**Square endpoint:** Timecard API (`/v2/labor/timecards`), webhooks `labor.timecard.created`, `labor.timecard.updated`, `labor.timecard.deleted`
**Permission required:** `TIMECARDS_READ`

**What we get:**

| Data | LP Significance |
|------|----------------|
| Timecard `start_at` / `end_at` | Employee on-clock vs. off-clock. Transactions processed while employee is off-clock = instant alert |
| `breaks[]` with start/end times | Transactions during break = suspicious activity |
| `team_member_id` | Links to payment team_member_id — cross-reference who was working vs. who processed payments |
| `location_id` | Employee at wrong location processing transactions |
| `hourly_rate` | Cost-of-labor analysis for Owl |
| `declared_cash_tip_money` | Tip manipulation / unreported income |
| `status` (OPEN/CLOSED) | Is this employee currently clocked in? |

**The killer insight:** By cross-referencing timecard data with payment data, we can detect:
- **Ghost employees**: Payments processed by employees not clocked in
- **After-hours transactions**: Payments outside any open timecard
- **Break fraud**: Transactions during declared breaks
- **Wrong-location activity**: Employee clocked in at Location A but processing payments at Location B

**Recommended implementation:**
1. Subscribe to `labor.timecard.created`, `labor.timecard.updated`, `labor.timecard.deleted` webhooks
2. Store in `employee_timecards` table in `canary_app`
3. Build Chirp cross-reference engine: payment.team_member_id vs. open timecard window
4. Poll `SearchTimecards` for historical backfill

---

### 2.4 INVENTORY API — 🟡 MEDIUM-HIGH VALUE

**Enterprise ancestor equivalent:** Product/Article Source (inventory counts, adjustments)
**Square webhook:** `inventory.count.updated`
**Permission required:** `INVENTORY_READ`

**What we get:**

| Data | LP Significance |
|------|----------------|
| Inventory count changes | Shrinkage detection — expected vs. actual inventory |
| `adjustment.reason` | Why inventory changed (SOLD, RECEIVED, RECOUNT, DAMAGE, THEFT, etc.) |
| `adjustment.team_member_id` | Who made the adjustment |
| `physical_count` vs. system count | **The shrinkage number** — the core LP metric |

**This is the most direct path to actual shrinkage measurement.** Without inventory data, Canary can only detect suspicious transaction patterns. With inventory data, we can calculate actual loss.

**Recommended implementation:**
1. Subscribe to `inventory.count.updated` webhook
2. Store in `inventory_adjustments` table in `canary_sales`
3. Build Owl shrinkage dashboard: expected inventory (sold + received - returned) vs. physical count
4. Alert on manual inventory adjustments by employee (potential cover-up of theft)

---

### 2.5 DISPUTES API — 🟡 MEDIUM VALUE

**Enterprise ancestor equivalent:** Not in the enterprise ancestor spec (they were pre-chargeback era for most clients)
**Square webhooks:** `dispute.created`, `dispute.state.updated`
**Permission required:** `DISPUTES_READ`

| Data | LP Significance |
|------|----------------|
| Chargeback disputes | External signal of fraud — customer claims unauthorized charge |
| `reason` (DUPLICATE, FRAUD, etc.) | Nature of the dispute |
| `disputed_payment` | Links to specific payment |
| `amount_money` | Financial exposure |

**Recommended implementation:** Subscribe to dispute webhooks, link to existing payment/transaction records, add to employee risk scoring.

---

### 2.6 GIFT CARDS API — 🟡 MEDIUM VALUE

**Enterprise ancestor equivalent:** Tender Source (gift card as tender type)
**Square webhooks:** `gift_card.created`, `gift_card.activity.created`, `gift_card.updated`
**Permission required:** `GIFTCARDS_READ`

| Data | LP Significance |
|------|----------------|
| Gift card creation/load activities | Manufactured spending, gift card fraud, return-to-gift-card schemes |
| `activity_type` (ACTIVATE, LOAD, REDEEM, REFUND, TRANSFER_BALANCE_TO/FROM, etc.) | Full lifecycle tracking |
| Balance transfers | Moving balances between cards = laundering indicator |
| `location_id`, `team_member_id` | Who created/loaded the card |

**Gift card fraud is one of the top 3 LP loss categories.** This is not a "nice to have."

**Recommended implementation:** Subscribe to all gift card webhooks, store in `gift_card_activities` table, build velocity alerts (multiple activations per employee, unusual load amounts).

---

### 2.7 CUSTOMER API — 🟢 MEDIUM VALUE

**Enterprise ancestor equivalent:** Customer Source
**Square webhooks:** `customer.created`, `customer.updated`, `customer.deleted`
**Permission required:** `CUSTOMERS_READ`

We already pull `customer_id` from payments. But the Customer API gives us:

| Data | LP Significance |
|------|----------------|
| Customer creation/merge events | Return-fraud-by-account: creating multiple customer profiles to circumvent return limits |
| `customer.deleted` events | Deleting customer profiles to hide return history |
| Loyalty data (via Loyalty API) | Loyalty point manipulation |

**Recommended implementation:** Subscribe to customer webhooks, track customer profile velocity (multiple creations from same employee), detect profile deletions that could indicate cover-up.

---

### 2.8 LOYALTY API — 🟢 MEDIUM VALUE

**Enterprise ancestor equivalent:** Customer Source (LoyaltyID, LoyaltyTier fields)
**Square webhooks:** `loyalty.account.created`, `loyalty.account.updated`, `loyalty.event.created`, `loyalty.promotion.created`
**Permission required:** `LOYALTY_READ`

| Data | LP Significance |
|------|----------------|
| Loyalty point accruals/redemptions | Point manipulation fraud — employees awarding points to personal accounts |
| `loyalty.event.created` | Every point-earning/burning event with employee and customer linkage |
| Promotion activity | Promo abuse detection |

---

### 2.9 DEVICES API — 🟢 LOW-MEDIUM VALUE

**Enterprise ancestor equivalent:** RegisterNumber / terminal identification
**Square endpoint:** `GET /v2/devices`
**Permission required:** `DEVICE_CREDENTIAL_MANAGEMENT`

| Data | LP Significance |
|------|----------------|
| Device inventory per location | Know every terminal — detect unauthorized devices |
| Device status (online/offline) | Offline devices may be used for off-book transactions |
| `device_id` ↔ location mapping | Terminal at wrong location = red flag |

---

### 2.10 TEAM MEMBERS API — 🟢 LOW-MEDIUM VALUE (Already Partially Covered)

**Enterprise ancestor equivalent:** Employee Source (reference data)
**Square endpoint:** `GET /v2/team-members`
**Permission required:** `EMPLOYEES_READ`

We pull basic employee data. Missing fields:

| Data | LP Significance |
|------|----------------|
| `is_owner` flag | Distinguish owner activity from employee activity |
| `status` (ACTIVE/INACTIVE) | Inactive employees processing transactions = instant alert |
| `assigned_locations` | Cross-location authorization |
| `created_at` | Employment start date |
| Wage data (`ListTeamMemberWages`) | Not LP-relevant directly, useful for Owl |

---

### 2.11 CATALOG API — 🟢 LOW VALUE FOR LP

**Enterprise ancestor equivalent:** Product/Article Source
**Square webhook:** `catalog.version.updated`
**Permission required:** `ITEMS_READ`

Product catalog data — item names, prices, categories. We already pull this for the products table. The webhook would let us track price changes (detecting unauthorized price modifications).

---

### 2.12 INVOICES API — 🟢 LOW VALUE FOR LP

**Square webhooks:** `invoice.created`, `invoice.updated`, etc.
Not directly LP-relevant for most SMB merchants but useful for B2B scenarios.

---

### 2.13 BOOKINGS API — ⚪ NOT LP-RELEVANT

Service-based bookings. Not applicable to retail LP.

---

### 2.14 SUBSCRIPTIONS API — ⚪ NOT LP-RELEVANT

Recurring billing subscriptions. Not applicable to retail LP.

---

## 3. The Enterprise Ancestor Transaction Type Coverage Matrix

Here's the definitive answer to "can Square give us the enterprise ancestor transaction types?"

| Enterprise Ancestor Transaction Type | Square Data Source | Available? | Currently Ingested? | Extraction Method |
|--------------------------|-------------------|------------|--------------------|--------------------|
| **Sale** | Payments API | ✅ Yes | ✅ Yes | `payment.created` webhook |
| **Return/Refund** | Refunds API | ✅ Yes | ✅ Yes | `refund.created` webhook |
| **Void (pre-capture)** | Payments API | ✅ Yes | ⚠️ Partial | `payment.updated` with status=CANCELED — we receive but don't flag as void |
| **Post Void (post-capture cancel)** | Payments API | ✅ Yes | ❌ No | `payment.updated` with status change COMPLETED→CANCELED after delay |
| **No Sale** | Cash Drawer API | ✅ Yes | ❌ No | `CashDrawerEventType.NO_SALE` |
| **Paid In** | Cash Drawer API | ✅ Yes | ❌ No | `CashDrawerEventType.PAID_IN` |
| **Paid Out** | Cash Drawer API | ✅ Yes | ❌ No | `CashDrawerEventType.PAID_OUT` |
| **Exchange** | Orders API | ✅ Yes | ❌ No | Order with both `line_items` and `returns` in same order |
| **Training Transaction** | Payments API | ⚠️ Partial | ❌ No | Sandbox test payments may have marker; POS-side training mode doesn't hit API |
| **Suspended/Resumed** | Orders API | ⚠️ Partial | ❌ No | Order with state=OPEN (not yet completed) — conceptually similar |
| **Layaway** | Orders API | ⚠️ Partial | ❌ No | Installment payments via recurring order |
| **Pickup (BOPIS)** | Orders API | ✅ Yes | ❌ No | `fulfillments[].type=PICKUP` |
| **Operator Override** | N/A | ❌ No | ❌ No | Square doesn't expose register-level overrides via API |

**Score: 10 of 13 enterprise ancestor transaction types are available from Square. We ingest 2.**

---

## 4. Complete Webhook Subscription Recommendations

### Tier 1 — Subscribe Immediately (Sprint 2)

| Webhook Event | API | Why |
|--------------|-----|-----|
| `order.created` | Orders | Line-item detail, discounts, taxes, tenders |
| `order.updated` | Orders | Returns, exchanges, state changes, voids |
| `labor.timecard.created` | Labor | Employee clock-in — cross-ref with payments |
| `labor.timecard.updated` | Labor | Clock-out, breaks |
| `labor.timecard.deleted` | Labor | Deleted timecard = potential cover-up |

Plus **daily polling** of:
| API | Endpoint | Why |
|-----|----------|-----|
| Cash Drawer Shifts | `ListCashDrawerShifts` + `ListCashDrawerShiftEvents` | No-sales, paid in/out, cash variance |

### Tier 2 — Subscribe Sprint 3

| Webhook Event | API | Why |
|--------------|-----|-----|
| `inventory.count.updated` | Inventory | Shrinkage measurement |
| `dispute.created` | Disputes | Chargeback signals |
| `dispute.state.updated` | Disputes | Dispute resolution tracking |
| `gift_card.activity.created` | Gift Cards | Gift card fraud |
| `gift_card.created` | Gift Cards | New card velocity |

### Tier 3 — Subscribe Sprint 4+

| Webhook Event | API | Why |
|--------------|-----|-----|
| `customer.created` | Customers | Account fraud |
| `customer.updated` | Customers | Profile changes |
| `customer.deleted` | Customers | Profile deletion (cover-up signal) |
| `loyalty.event.created` | Loyalty | Point manipulation |
| `catalog.version.updated` | Catalog | Price change tracking |

---

## 5. New Database Tables Required

### canary_sales (append-only transaction data)

```sql
-- Cash drawer events (Tier 1)
CREATE TABLE cash_drawer_shifts (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    shift_id VARCHAR(255) UNIQUE NOT NULL,
    location_id VARCHAR(255) NOT NULL,
    device_id VARCHAR(255),
    device_name VARCHAR(255),
    opened_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    ended_at TIMESTAMP,
    opening_team_member_id VARCHAR(255),
    closing_team_member_id VARCHAR(255),
    ending_team_member_id VARCHAR(255),
    opened_cash_cents INTEGER DEFAULT 0,
    expected_cash_cents INTEGER DEFAULT 0,
    closed_cash_cents INTEGER DEFAULT 0,
    cash_variance_cents INTEGER GENERATED ALWAYS AS (closed_cash_cents - expected_cash_cents) STORED,
    cash_payment_cents INTEGER DEFAULT 0,
    cash_refund_cents INTEGER DEFAULT 0,
    cash_paid_in_cents INTEGER DEFAULT 0,
    cash_paid_out_cents INTEGER DEFAULT 0,
    state VARCHAR(25),  -- OPEN, ENDED, CLOSED
    ingested_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cash_drawer_events (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    shift_id VARCHAR(255) NOT NULL REFERENCES cash_drawer_shifts(shift_id),
    event_id VARCHAR(255) UNIQUE NOT NULL,
    event_type VARCHAR(50) NOT NULL,  -- NO_SALE, PAID_IN, PAID_OUT, CASH_TENDER_PAYMENT, etc.
    event_money_cents INTEGER DEFAULT 0,
    team_member_id VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP DEFAULT NOW()
);

-- Line items (Tier 1 — replaces JSONB)
CREATE TABLE transaction_line_items (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    order_id VARCHAR(255) NOT NULL,
    line_item_uid VARCHAR(255) NOT NULL,
    catalog_object_id VARCHAR(255),
    item_name VARCHAR(255),
    variation_name VARCHAR(255),
    quantity DECIMAL(18,4) NOT NULL DEFAULT 1,
    base_price_cents INTEGER,
    gross_sales_cents INTEGER,
    total_discount_cents INTEGER DEFAULT 0,
    total_tax_cents INTEGER DEFAULT 0,
    total_money_cents INTEGER,
    item_type VARCHAR(50),  -- ITEM, CUSTOM_AMOUNT, GIFT_CARD
    is_voided BOOLEAN DEFAULT FALSE,
    return_reason VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(order_id, line_item_uid)
);

-- Split tenders (Tier 1)
CREATE TABLE transaction_tenders (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    order_id VARCHAR(255) NOT NULL,
    tender_id VARCHAR(255) UNIQUE NOT NULL,
    tender_type VARCHAR(50) NOT NULL,  -- CARD, CASH, SQUARE_GIFT_CARD, OTHER, NO_SALE
    amount_cents INTEGER NOT NULL,
    tip_cents INTEGER DEFAULT 0,
    processing_fee_cents INTEGER DEFAULT 0,
    card_brand VARCHAR(25),
    card_last4 VARCHAR(4),
    entry_method VARCHAR(25),
    payment_id VARCHAR(255),
    team_member_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP DEFAULT NOW()
);

-- Inventory adjustments (Tier 2)
CREATE TABLE inventory_adjustments (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    adjustment_id VARCHAR(255) UNIQUE NOT NULL,
    catalog_object_id VARCHAR(255) NOT NULL,
    location_id VARCHAR(255) NOT NULL,
    from_quantity DECIMAL(18,4),
    to_quantity DECIMAL(18,4),
    adjustment_type VARCHAR(50),  -- PHYSICAL_COUNT, ADJUSTMENT, SALE, RECEIVE, DAMAGE, THEFT
    team_member_id VARCHAR(255),
    reason VARCHAR(500),
    occurred_at TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP DEFAULT NOW()
);

-- Gift card activities (Tier 2)
CREATE TABLE gift_card_activities (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    activity_id VARCHAR(255) UNIQUE NOT NULL,
    gift_card_id VARCHAR(255) NOT NULL,
    activity_type VARCHAR(50) NOT NULL,  -- ACTIVATE, LOAD, REDEEM, REFUND, DEACTIVATE, TRANSFER_BALANCE_TO, TRANSFER_BALANCE_FROM, etc.
    amount_cents INTEGER,
    balance_cents INTEGER,
    location_id VARCHAR(255),
    team_member_id VARCHAR(255),
    payment_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP DEFAULT NOW()
);
```

### canary_app (operational data)

```sql
-- Employee timecards (Tier 1)
CREATE TABLE employee_timecards (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    timecard_id VARCHAR(255) UNIQUE NOT NULL,
    team_member_id VARCHAR(255) NOT NULL,
    location_id VARCHAR(255) NOT NULL,
    start_at TIMESTAMP NOT NULL,
    end_at TIMESTAMP,
    status VARCHAR(25) NOT NULL,  -- OPEN, CLOSED
    hourly_rate_cents INTEGER,
    declared_cash_tip_cents INTEGER DEFAULT 0,
    breaks JSONB DEFAULT '[]',  -- Array of {start_at, end_at, break_type_id, is_paid}
    ingested_at TIMESTAMP DEFAULT NOW()
);

-- Disputes (Tier 2)
CREATE TABLE disputes (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) NOT NULL,
    dispute_id VARCHAR(255) UNIQUE NOT NULL,
    payment_id VARCHAR(255) NOT NULL,
    reason VARCHAR(100),  -- DUPLICATE, FRAUD, NOT_AS_DESCRIBED, etc.
    state VARCHAR(50),  -- INQUIRY_EVIDENCE_REQUIRED, INQUIRY_CLOSED, WON, LOST, etc.
    amount_cents INTEGER NOT NULL,
    due_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT NOW()
);
```

---

## 6. New Chirp Detection Rules Enabled

Each new data source enables specific detection rules that were previously impossible:

### From Cash Drawer API

| Rule | Signal | Threshold (configurable) |
|------|--------|--------------------------|
| `HIGH_NO_SALE_FREQUENCY` | Employee >5 no-sale events per shift | 5/shift |
| `CASH_VARIANCE_OVER` | Shift cash variance exceeds ±$20 | ±$20 |
| `EXCESSIVE_PAID_OUT` | Total paid-outs in shift >$100 | $100 |
| `AFTER_HOURS_DRAWER_OPEN` | Cash drawer opened outside business hours | Location hours |
| `SPLIT_TENDER_CANCEL` | Cash tendered then payment cancelled (cash kept) | Any occurrence |

### From Labor/Timecard API

| Rule | Signal | Threshold |
|------|--------|-----------|
| `OFF_CLOCK_TRANSACTION` | Payment processed by employee not on active timecard | Any occurrence |
| `BREAK_TRANSACTION` | Payment processed during declared break | Any occurrence |
| `WRONG_LOCATION_ACTIVITY` | Employee clocked in at Location A, payment at Location B | Any occurrence |
| `GHOST_EMPLOYEE` | Employee with no timecard in 30 days but processing payments | 30 days |

### From Orders API

| Rule | Signal | Threshold |
|------|--------|-----------|
| `EXCESSIVE_DISCOUNT_RATE` | Order-level discount >50% by same employee | 50% |
| `SWEET_HEART_PATTERN` | Repeated high discounts to same customer by same employee | 3+ occurrences |
| `MODIFIER_SKIP` | Items consistently rung without expected modifiers | Pattern detection |
| `LINE_ITEM_VOID_RATE` | Employee void rate on line items >10% | 10% |

### From Inventory API

| Rule | Signal | Threshold |
|------|--------|-----------|
| `SHRINKAGE_SPIKE` | Inventory variance exceeds 2% in category | 2% |
| `MANUAL_ADJUSTMENT_VELOCITY` | >3 manual inventory adjustments per day by one employee | 3/day |

### From Gift Card API

| Rule | Signal | Threshold |
|------|--------|-----------|
| `GIFT_CARD_LOAD_VELOCITY` | Employee loads >5 gift cards per day | 5/day |
| `BALANCE_TRANSFER_PATTERN` | Balance transfers between cards from same employee | 2+ per week |
| `RETURN_TO_GIFT_CARD` | Refund immediately followed by gift card load | Pattern detection |

---

## 7. OAuth Permission Expansion Required

Our current OAuth scope likely only includes payment and merchant permissions. To access these data sources, we need to request additional OAuth scopes during the Square Marketplace certification process (E2).

| Permission | Required For | Impact |
|-----------|-------------|--------|
| `CASH_DRAWER_READ` | Cash Drawer Shifts API | New |
| `ORDERS_READ` | Orders API (full detail) | Likely already granted |
| `TIMECARDS_READ` | Labor/Timecard API | New |
| `INVENTORY_READ` | Inventory API | New |
| `DISPUTES_READ` | Disputes API | New |
| `GIFTCARDS_READ` | Gift Cards API | New |
| `CUSTOMERS_READ` | Customer lifecycle events | Likely already granted |
| `LOYALTY_READ` | Loyalty program data | New |

**Eva note:** These permissions must be included in our Square Marketplace app listing. More permissions = more scrutiny during review, but every one of these is legitimate for an LP platform. The enterprise LP data specification itself serves as industry precedent that LP platforms need this data.

---

## 8. Implementation Roadmap

### Sprint 2 (Immediate — Foundation)

| Task | Owner | Effort | Dependencies |
|------|-------|--------|-------------|
| Add Cash Drawer polling worker | Jeremy | 3 days | `CASH_DRAWER_READ` OAuth scope |
| Create `cash_drawer_shifts` + `cash_drawer_events` tables | Jeremy | 1 day | Schema migration |
| Subscribe to `order.created`/`order.updated` webhooks | Jeremy | 2 days | `ORDERS_READ` scope |
| Create `transaction_line_items` + `transaction_tenders` tables | Jeremy/Tom | 2 days | Schema migration |
| Subscribe to `labor.timecard.*` webhooks | Jeremy | 1 day | `TIMECARDS_READ` scope |
| Create `employee_timecards` table | Jeremy | 1 day | Schema migration |
| Add `transaction_type` enum to transactions table | Jeremy | 0.5 day | Schema migration |
| Detect void/post-void from `payment.updated` status changes | Jeremy | 1 day | Existing webhook handler |
| First 5 Chirp rules (no-sale, cash variance, off-clock, void rate, discount abuse) | Jeremy | 3 days | New data tables populated |

### Sprint 3 (Expand)

| Task | Owner | Effort |
|------|-------|--------|
| Subscribe to `inventory.count.updated` | Jeremy | 1 day |
| Create `inventory_adjustments` table | Jeremy/Tom | 1 day |
| Subscribe to `dispute.*` webhooks | Jeremy | 1 day |
| Subscribe to `gift_card.*` webhooks | Jeremy | 1 day |
| Create `gift_card_activities` + `disputes` tables | Jeremy | 1.5 days |
| Next 8 Chirp rules (shrinkage, gift card velocity, dispute flags, break fraud) | Jeremy | 3 days |
| Historical backfill via `SearchOrders`, `SearchTimecards` | Jeremy | 2 days |

### Sprint 4 (Complete)

| Task | Owner | Effort |
|------|-------|--------|
| Customer lifecycle webhooks | Jeremy | 1 day |
| Loyalty webhooks | Jeremy | 1 day |
| Catalog change tracking | Jeremy | 1 day |
| Remaining Chirp rules | Jeremy | 3 days |
| Owl dashboard integration (cash variance, shrinkage, labor vs. payment overlay) | Jeremy | 3 days |

---

## 9. Impact Summary

| Metric | Before | After |
|--------|--------|-------|
| Square webhook event types subscribed | 4 | 20+ |
| Square APIs actively polled | 0 | 2 (Cash Drawer, backfill) |
| Transaction types detected | 2 (sale, refund) | 10 (sale, refund, void, post-void, no-sale, paid in, paid out, exchange, pickup, discount abuse) |
| Chirp detection rules possible | ~8 (payment-only) | 25+ (multi-source cross-reference) |
| Data tables in canary_sales | 5 | 10 |
| Data tables in canary_app | ~10 | ~14 |
| LP exposure coverage vs. enterprise ancestor spec | ~32% | ~85% |

**Bottom line: We're building an LP platform on 14% of available data. This analysis shows how to get to 85%+ coverage using APIs Square already exposes and that our OAuth token can access with the right permissions.**

---

## 10. Square API Documentation References

- [Cash Drawer Shifts API](https://developer.squareup.com/docs/cashdrawershift-api/reporting)
- [Cash Drawer Event Types](https://github.com/square/square-nodejs-sdk/blob/master/doc/models/cash-drawer-event-type.md)
- [Payments API Webhooks](https://developer.squareup.com/docs/payments-api/webhooks)
- [Refunds API Webhooks](https://developer.squareup.com/docs/refunds-api/webhooks)
- [Orders API](https://developer.squareup.com/docs/orders-api/what-it-does)
- [Labor API / Timecards](https://developer.squareup.com/docs/labor-api/what-it-does)
- [Webhook Events Reference](https://developer.squareup.com/docs/webhooks/v2webhook-events-tech-ref)
- [Payment Object](https://developer.squareup.com/reference/square/objects/Payment)
- [CardPaymentDetails Object](https://developer.squareup.com/reference/square/objects/CardPaymentDetails)
- [Devices API](https://developer.squareup.com/reference/square/devices-api)
- [Gift Cards API](https://developer.squareup.com/docs/gift-cards/using-gift-cards-api)

---

*Prepared by Jeremy (Developer Quant). This analysis feeds directly into Sprint 2 planning and PRD E1 (Chirp) acceptance criteria updates. Eva to schedule Sprint 2 planning session with these recommendations.*
