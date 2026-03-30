---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-20 — Square SDK → CRDM Alignment Audit

**Issue:** GRO-20 (B-036)
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** Internal — Technical Audit
**Gate:** Gates Tom's DDL work on GRO-18. Tom validates, Jeremy implements.
**Done When:** Audit report showing gaps/mismatches between Square SDK and CRDM.

---

## 1. Methodology

This audit maps every CRDM v1.0 data source (7 canonical sources, ~35 tables) against the Square API objects and webhook events that feed them. For each field, we assess: does the Square API provide it, what's the exact field path, and is there a gap?

**Square APIs in scope:** Payments, Orders, Refunds, Catalog, Inventory, Labor (Timecards), Team, Customers, Cash Drawers, Gift Cards, Gift Card Activities, Locations, Disputes.

**Note:** The Square Developer site (developer.squareup.com) was inaccessible during this audit. Field mappings are based on web search results, Square SDK documentation fragments, and CRDM v1.0's existing mappings. Tom should validate against live API responses before finalizing DDL.

---

## 2. Source 1: Transaction Header → Payments API + Orders API

**CRDM Table:** `canary_sales.transactions`
**Square APIs:** Payments API (`/v2/payments`), Orders API (`/v2/orders`)
**Webhook Events:** `payment.created`, `payment.updated`, `order.created`, `order.updated`

| CRDM Column | Square API Field Path | API | Status | Notes |
|-------------|----------------------|-----|--------|-------|
| `external_id` | `payment.id` | Payments | ✅ Aligned | Primary key from Square |
| `location_id` | `payment.location_id` | Payments | ✅ Aligned | |
| `device_id` | `payment.device_details.device_id` | Payments | ✅ Aligned | Only present for in-person payments |
| `transaction_date` | `payment.created_at` | Payments | ✅ Aligned | RFC 3339 → DATE extraction needed |
| `transaction_type` | Inferred from event + status | Multiple | ⚠️ Derived | See CRDM Transaction Type Enum. SALE = `payment.created` + COMPLETED; RETURN = `refund.created`; VOID = COMPLETED→CANCELED (immediate); POST_VOID = COMPLETED→CANCELED (delayed). Requires state machine logic in ingestion. |
| `employee_id` | `payment.team_member_id` | Payments | ✅ Aligned | Maps to `employees.square_employee_id` |
| `amount_cents` | `payment.amount_money.amount` | Payments | ✅ Aligned | Already in cents (smallest denomination) |
| `currency` | `payment.amount_money.currency` | Payments | ✅ Aligned | |
| `tax_amount_cents` | `order.total_tax_money.amount` | Orders | ⚠️ Sprint 2 | Not on Payment object — must join to Order |
| `discount_amount_cents` | `order.total_discount_money.amount` | Orders | ⚠️ Sprint 2 | Not on Payment object — must join to Order |
| `customer_id` | `payment.customer_id` or `order.customer_id` | Both | ✅ Aligned | |
| `square_product` | `payment.source_type` | Payments | ✅ Aligned | CARD, CASH, etc. |
| `card_fingerprint` | `payment.card_details.card.fingerprint` | Payments | ✅ Aligned | Tokenized — not PCI sensitive |
| `payload` | Full webhook body | Webhook | ✅ Aligned | JSONB storage after scrub (GRO-19) |
| `scrub_version` | N/A (Canary-generated) | — | ✅ New | Added per GRO-19 memo |
| `record_hash` | N/A (Canary-generated) | — | ✅ New | SHA-256 hash chain (Pattern 4) |

**Coverage: 14/16 columns mapped. 2 deferred to Sprint 2 (tax, discount — require Order join).**

**Gap: `transaction_type` derivation.** This is the most complex mapping in the CRDM. Jeremy's ingestion pipeline needs a state machine that tracks payment status transitions to distinguish VOID from POST_VOID. The CRDM documents the detection method but the implementation requires tracking `payment.updated` events with status changes over time. Tom should review the state machine design before Jeremy implements.

---

## 3. Source 2: Tender → Payments API (Card Details)

**CRDM Table:** `canary_sales.transaction_tenders`
**Square API:** Payments API — `payment.card_details`, plus tender array on Order
**Webhook Events:** `payment.created`, `payment.updated`

| CRDM Column | Square API Field Path | Status | Notes |
|-------------|----------------------|--------|-------|
| `tender_type` | `order.tenders[].type` | ✅ Aligned | CARD, CASH, SQUARE_GIFT_CARD, OTHER, NO_SALE |
| `amount_cents` | `order.tenders[].amount_money.amount` | ✅ Aligned | Per-tender amount |
| `card_brand` | `payment.card_details.card.card_brand` | ✅ Aligned | VISA, MASTERCARD, etc. |
| `card_last4` | `payment.card_details.card.last_4` | ⚠️ Legal gate | Pending Syd's ruling (GRO-19). Default: STRIP |
| `entry_method` | `payment.card_details.entry_method` | ✅ Aligned | KEYED, SWIPED, EMV, CONTACTLESS, ON_FILE |
| `team_member_id` | `payment.team_member_id` | ✅ Aligned | Inherited from payment |
| `payment_id` (FK) | `payment.id` | ✅ Aligned | Join key to transactions |

**Coverage: 7/7 columns mapped. card_last4 gated on GRO-19 legal ruling.**

**Key finding:** Split-tender detection requires the `order.tenders[]` array, not just the Payment object. The Payment object represents a single tender; multi-tender transactions are represented as multiple Payments linked to one Order. Jeremy's ingestion must process at the Order level for tender analysis, not just at the Payment level.

---

## 4. Source 3: Line Items → Orders API

**CRDM Table:** `canary_sales.transaction_line_items`
**Square API:** Orders API — `order.line_items[]`
**Webhook Events:** `order.created`, `order.updated`

| CRDM Column | Square API Field Path | Status | Notes |
|-------------|----------------------|--------|-------|
| `catalog_object_id` | `order.line_items[].catalog_object_id` | ✅ Aligned | Links to Catalog API |
| `item_name` | `order.line_items[].name` | ✅ Aligned | |
| `quantity` | `order.line_items[].quantity` | ✅ Aligned | String type — supports fractional (e.g., "2.5") |
| `base_price_cents` | `order.line_items[].base_price_money.amount` | ✅ Aligned | |
| `gross_sales_cents` | `order.line_items[].gross_sales_money.amount` | ✅ Aligned | |
| `total_discount_cents` | `order.line_items[].total_discount_money.amount` | ✅ Aligned | **The sweet-hearting signal** |
| `total_tax_cents` | `order.line_items[].total_tax_money.amount` | ✅ Aligned | |
| `item_type` | `order.line_items[].item_type` | ✅ Aligned | ITEM, CUSTOM_AMOUNT, GIFT_CARD |
| `is_voided` | Inferred from `order.returns[]` | ⚠️ Derived | No native "voided" flag — must derive from returns/cancellation |
| `return_reason` | `order.returns[].return_line_items[].return_reason` | ⚠️ Partial | Only present if merchant enters reason |

**Coverage: 8/10 direct, 2 derived. No blocking gaps.**

**Gap: `is_voided` derivation.** Square doesn't have a native void flag on line items. A voided line item appears as a return within the same order. Jeremy needs to detect: if an `order.returns[]` entry references a `line_item_uid` from the same order and was created within the same session window, flag as void rather than return. The time window threshold should be configurable (default: 5 minutes).

---

## 5. Source 4: Employee → Team API + Labor API (Timecards)

**CRDM Tables:** `canary_app.employees`, `canary_app.employee_timecards`
**Square APIs:** Team API (`/v2/team-members`), Labor API (`/v2/labor/timecards`)
**Webhook Events:** `team_member.created`, `team_member.updated` (Team); **NONE for Labor — poll only**

| CRDM Column | Square API Field Path | API | Status | Notes |
|-------------|----------------------|-----|--------|-------|
| `square_employee_id` | `team_member.id` | Team | ✅ Aligned | |
| `employee_name` | `team_member.given_name` + `family_name` | Team | ✅ Aligned | Concatenate |
| `db_status` | `team_member.status` | Team | ✅ Aligned | ACTIVE, INACTIVE |
| `primary_location_id` | `team_member.assigned_locations.location_ids[0]` | Team | ⚠️ Heuristic | Square allows multi-location assignment; CRDM takes first as primary |
| `risk_score` | N/A (Canary-generated) | — | ✅ New | ML-computed |
| `start_at` | `timecard.clock_in_at` | Labor | ✅ Aligned | **API renamed: Shift → Timecard as of v2025-05-21** |
| `end_at` | `timecard.clock_out_at` | Labor | ✅ Aligned | |
| `breaks` | `timecard.breaks[]` | Labor | ✅ Aligned | Array: `{start_at, end_at, break_type_id, name, expected_duration, is_paid}` |
| `location_id` | `timecard.location_id` | Labor | ✅ Aligned | Where the shift was worked |
| `wage_rate` | `timecard.wage.hourly_rate` | Labor | ✅ Aligned | Optional — only if employer tracks |

**Coverage: 10/10 mapped. Zero gaps.**

**Critical finding — API rename:** Square renamed the Shift object to Timecard in API version 2025-05-21. The CRDM table name `employee_timecards` already matches the new naming. But Jeremy must ensure the SDK version targets `2025-05-21` or later, and uses `/v2/labor/timecards` endpoints (not the deprecated `/v2/labor/shifts`).

**Critical finding — no webhooks:** The Labor API has no webhook support. GRO-27 (Square Labor API polling adapter) is the mitigation. Polling interval recommendation: every 5 minutes during business hours, every 30 minutes off-hours. This directly affects Chirp rules C-301 (OFF_CLOCK_TRANSACTION), C-302 (BREAK_TRANSACTION), C-303 (WRONG_LOCATION_ACTIVITY) — these can only fire with a delay equal to the polling interval.

---

## 6. Source 5: Product/Article → Catalog API

**CRDM Table:** `canary_app.products`
**Square API:** Catalog API (`/v2/catalog`)
**Webhook Events:** `catalog.version.updated`

| CRDM Column | Square API Field Path | Status | Notes |
|-------------|----------------------|--------|-------|
| `square_item_id` | `catalog_object.id` | ✅ Aligned | |
| `product_name` | `catalog_object.item_data.name` | ✅ Aligned | |
| `UPC` | `catalog_object.item_data.variations[].item_variation_data.upc` | ✅ Aligned | Per-variation |
| `SKU` | `catalog_object.item_data.variations[].item_variation_data.sku` | ✅ Aligned | Per-variation |
| `COGS` | N/A | ❌ Gap | Square Catalog has no cost/COGS field. Must be manually entered or imported. |
| `unit_price` | `catalog_object.item_data.variations[].item_variation_data.price_money.amount` | ✅ Aligned | Per-variation |
| `department` | N/A | ❌ Gap | Square has no native merchandise hierarchy (Dept/Class/Subclass) |
| `class` | N/A | ❌ Gap | Same — structural limitation |
| `subclass` | N/A | ❌ Gap | Same |

**Coverage: 6/9 mapped. 3 structural gaps (COGS, merchandise hierarchy).**

**Gap analysis:** These are known limitations documented in CRDM v1.0. COGS must come from merchant manual entry or import (Bull module scope). Merchandise hierarchy requires Tom's GSLM-inspired pattern — deferred post-MVP. Neither gap blocks Chirp detection rules.

---

## 7. Source 6: Store/Location → Locations API

**CRDM Table:** `canary_app.locations`
**Square API:** Locations API (`/v2/locations`)
**Webhook Events:** None (poll-only, low frequency)

| CRDM Column | Square API Field Path | Status | Notes |
|-------------|----------------------|--------|-------|
| `square_location_id` | `location.id` | ✅ Aligned | |
| `location_name` | `location.name` | ✅ Aligned | |
| `address` | `location.address` | ✅ Aligned | Structured: address_line_1, city, state, postal, country |
| `timezone` | `location.timezone` | ✅ Aligned | IANA timezone string |
| `business_hours` | `location.business_hours.periods[]` | ✅ Aligned | Array of {day, start, end} |
| `status` | `location.status` | ✅ Aligned | ACTIVE, INACTIVE |
| `merchant_id` | `location.merchant_id` | ✅ Aligned | Square's merchant ID |
| `country` | `location.country` | ✅ Aligned | ISO 3166 |
| `currency` | `location.currency` | ✅ Aligned | |
| `capabilities` | `location.capabilities[]` | ✅ Aligned | CREDIT_CARD_PROCESSING, etc. |
| `mcc` | `location.mcc` | ✅ Aligned | Merchant Category Code |
| `phone_number` | `location.phone_number` | ✅ Aligned | |

**Coverage: 12/12 mapped. Fully aligned. No gaps.**

---

## 8. Source 7: Customer → Customers API

**CRDM Table:** `canary_app.customers`
**Square API:** Customers API (`/v2/customers`)
**Webhook Events:** `customer.created`, `customer.updated`

| CRDM Column | Square API Field Path | Status | Notes |
|-------------|----------------------|--------|-------|
| `square_customer_id` | `customer.id` | ✅ Aligned | |
| `customer_name` | `customer.given_name` + `family_name` | ✅ Aligned | |
| `email` | `customer.email_address` | ✅ Aligned | PII — retention per GRO-19 |
| `phone` | `customer.phone_number` | ✅ Aligned | PII — retention per GRO-19 |
| `lifetime_value` | N/A (Canary-computed) | ✅ New | Derived from transaction sum |
| `transaction_count` | N/A (Canary-computed) | ✅ New | Derived from transaction count |
| `created_at` | `customer.created_at` | ✅ Aligned | |

**Coverage: 5/7 mapped (2 are Canary-computed). No gaps.**

---

## 9. Additional CRDM Tables — Non-Canonical Sources

### Cash Drawers → Cash Drawers API

**CRDM Tables:** `canary_sales.cash_drawer_shifts`, `canary_sales.cash_drawer_events`
**Square API:** Cash Drawers API (`/v2/cash-drawers/shifts`)
**Webhook Events:** None (poll-only)

| CRDM Column | Square API Field Path | Status |
|-------------|----------------------|--------|
| Shift: `opened_at`, `closed_at` | `cash_drawer_shift.opened_at`, `closed_at` | ✅ |
| Shift: `opening_cash`, `closing_cash` | `cash_drawer_shift.opened_cash_money`, `closed_cash_money` | ✅ |
| Shift: `cash_paid_in`, `cash_paid_out` | `cash_drawer_shift.cash_paid_in_money`, `cash_paid_out_money` | ✅ |
| Shift: `expected_cash` | `cash_drawer_shift.expected_cash_money` | ✅ |
| Events: `event_type` | `cash_drawer_shift_event.event_type` | ✅ |
| Events: `event_money` | `cash_drawer_shift_event.event_money` | ✅ |
| Events: `team_member_id` | `cash_drawer_shift_event.team_member_id` | ✅ |
| Events: `description` | `cash_drawer_shift_event.description` | ✅ |

**Fully aligned. No gaps. But no webhooks — poll-only like Labor API.**

### Inventory Adjustments → Inventory API

**CRDM Table:** `canary_sales.inventory_adjustments`
**Square API:** Inventory API (`/v2/inventory`)
**Webhook Events:** `inventory.count.updated`

| CRDM Column | Square API Field Path | Status |
|-------------|----------------------|--------|
| `catalog_object_id` | `inventory_adjustment.catalog_object_id` | ✅ |
| `quantity` | `inventory_adjustment.quantity` | ✅ |
| `from_state`, `to_state` | `inventory_adjustment.from_state`, `to_state` | ✅ |
| `location_id` | `inventory_adjustment.location_id` | ✅ |
| `team_member_id` | `inventory_adjustment.team_member_id` | ✅ |
| `occurred_at` | `inventory_adjustment.occurred_at` | ✅ |

**Fully aligned. Webhook available for real-time updates.**

### Gift Card Activities → Gift Card Activities API

**CRDM Table:** `canary_sales.gift_card_activities`
**Square API:** Gift Card Activities API (`/v2/gift-cards/activities`)
**Webhook Events:** `gift_card.activity.created` (verify availability)

| CRDM Column | Square API Field Path | Status |
|-------------|----------------------|--------|
| `gift_card_id` | `gift_card_activity.gift_card_id` | ✅ |
| `activity_type` | `gift_card_activity.type` | ✅ |
| `amount` | `gift_card_activity.activate_activity_details.amount_money` (varies by type) | ⚠️ Nested |
| `balance` | `gift_card_activity.gift_card_balance_money` | ✅ |
| `location_id` | `gift_card_activity.location_id` | ✅ |
| `created_at` | `gift_card_activity.created_at` | ✅ |

**Aligned. Amount field path varies by activity type — Jeremy needs a type-aware extractor.**

### Disputes → Disputes API

**CRDM Table:** `canary_app.disputes` (Sprint 3)
**Square API:** Disputes API (`/v2/disputes`)
**Webhook Events:** `dispute.created`, `dispute.state.updated`

| CRDM Column | Square API Field Path | Status |
|-------------|----------------------|--------|
| `dispute_id` | `dispute.id` | ✅ |
| `payment_id` | `dispute.payment_id` | ✅ (verify) |
| `reason` | `dispute.reason` | ✅ |
| `amount` | `dispute.amount_money` | ✅ |
| `card_brand` | `dispute.card_brand` | ✅ |
| `state` | `dispute.state` | ✅ |
| `due_at` | `dispute.due_at` | ✅ |

**Aligned. Sprint 3 scope — no action needed now.**

---

## 10. Webhook Coverage Matrix

| CRDM Data Source | Webhook Available? | Event Types | Polling Fallback Needed? |
|------------------|--------------------|-------------|--------------------------|
| Transactions (Payments) | ✅ Yes | `payment.created`, `payment.updated` | No |
| Orders | ✅ Yes | `order.created`, `order.updated` | No |
| Refunds | ✅ Yes | `refund.created`, `refund.updated` | No |
| Customers | ✅ Yes | `customer.created`, `customer.updated` | No |
| Catalog/Products | ✅ Yes | `catalog.version.updated` | No |
| Inventory | ✅ Yes | `inventory.count.updated` | No |
| Disputes | ✅ Yes | `dispute.created`, `dispute.state.updated` | No |
| **Labor (Timecards)** | ❌ No | None | **YES — GRO-27** |
| **Cash Drawers** | ❌ No | None | **YES — include in GRO-27** |
| **Locations** | ❌ No | None | Low-frequency poll OK |
| Gift Card Activities | ⚠️ Verify | `gift_card.activity.created` (unconfirmed) | May need polling |

**2 APIs require polling adapters (Labor, Cash Drawers). GRO-27 should cover both, not just Labor.**

---

## 11. Gap Summary

| Gap | Severity | CRDM Source | Mitigation | Blocks |
|-----|----------|-------------|------------|--------|
| `transaction_type` derivation | HIGH | Source 1 | State machine in ingestion pipeline | Chirp rules C-401, C-402 |
| `card.last_4` retention | MEDIUM | Source 2 | GRO-19 legal ruling | Chirp rule C-004 |
| No Labor webhooks | MEDIUM | Source 4 | GRO-27 polling adapter | Chirp rules C-301, C-302, C-303 |
| No Cash Drawer webhooks | MEDIUM | Source 9 | Add to GRO-27 scope | Chirp rules C-201, C-202, C-203 |
| COGS not in Catalog API | LOW | Source 5 | Manual entry / import (Bull module) | Shrinkage $ calculation |
| Merchandise hierarchy | LOW | Source 5 | Tom's GSLM pattern, post-MVP | Category-level reporting |
| `is_voided` derivation | LOW | Source 3 | Session-window heuristic | Void detection accuracy |
| Shift → Timecard rename | INFO | Source 4 | Use SDK v2025-05-21+ | Breaking if wrong version |
| Gift card webhook availability | INFO | Source 9 | Verify; add polling if needed | Chirp rules C-601, C-602 |

---

## 12. Action Items

1. **Tom:** Review this audit against live Square API responses. Validate field paths I couldn't confirm due to site access restrictions. Prioritize the `transaction_type` state machine design.
2. **Jeremy:** Target Square SDK version `2025-05-21` or later to use Timecard endpoints. Implement type-aware extractors for gift card activity amounts.
3. **GRO-27 scope expansion:** Add Cash Drawer polling to GRO-27 (currently only scopes Labor). Both are poll-only, both feed Chirp rules.
4. **Jim:** Test plan should include webhook payload validation — confirm actual field paths match this audit for each event type.

---

*ALX | GRO-20 | March 2, 2026*
