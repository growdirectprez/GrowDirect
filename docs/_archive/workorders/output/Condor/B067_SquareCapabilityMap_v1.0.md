---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# B-067-A: Square API Capability Map
**Work Order:** B-067-A
**Author:** Condor
**Date:** February 28, 2026
**SDK Version:** Square Python SDK v44.0.1.20260122 (`squareup` package)
**SDK Import:** `from square import Square` / `client = Square(token=..., environment=...)`
**Status:** DELIVERED — gates Jeremy B-067-B wiring pass + Qwen B-067-C dashboard

---

## How to Read This Map

Each block below documents one of 16 Square API families. Fields are:

- **SDK Namespace:** How to access this family from the `Square` client
- **Sandbox Permission:** OAuth scope required (sandbox grants all by default)
- **Canary Phase:** When this family enters the Canary pipeline
- **TSP Component:** Which TSP PRD specification covers this family
- **LP Signal:** What fraud/loss prevention insight this family provides
- **Key Read Methods:** 3-5 actual SDK method names verified against cloned repo
- **Sample Call:** One-line real v44 syntax
- **Dashboard Section Title:** What Jeffe sees as the card header
- **Fetch Button Label:** Button text on the dashboard
- **Phase Badge:** Visual indicator for the dashboard
- **explore_ function name:** Function name for Jeremy's B-067-B module

---

## API Family Blocks

### 1. Payments

```
SDK Namespace:            client.payments
Sandbox Permission:       PAYMENTS_READ
Canary Phase:             Phase 1 LIVE
TSP Component:            TSP-01, TSP-03, TSP-04, TSP-05, TSP-06
LP Signal:                Core transaction record — amount, tender type, card fingerprint, risk evaluation, void/post-void detection
Key Read Methods:         list(), get(payment_id), create(), update(payment_id), cancel_by_idempotency_key()
Sample Call (Python):     for payment in client.payments.list(location_id="L88917AVBK2S5"): print(payment.id)
Dashboard Section Title:  Payments
Fetch Button Label:       Fetch Live Data
Phase Badge:              LIVE
explore_ function name:   explore_payments
```

---

### 2. Refunds

```
SDK Namespace:            client.refunds
Sandbox Permission:       PAYMENTS_READ
Canary Phase:             Phase 1 LIVE
TSP Component:            TSP-01, TSP-03, TSP-04, TSP-05, TSP-06
LP Signal:                Refund amount, reason, employee attribution — primary Chirp trigger (C-004: refund >$10)
Key Read Methods:         list(), get(refund_id), refund_payment()
Sample Call (Python):     for refund in client.refunds.list(location_id="L88917AVBK2S5"): print(refund.id)
Dashboard Section Title:  Refunds
Fetch Button Label:       Fetch Live Data
Phase Badge:              LIVE
explore_ function name:   explore_refunds
```

---

### 3. Orders

```
SDK Namespace:            client.orders
Sandbox Permission:       ORDERS_READ
Canary Phase:             Phase 2
TSP Component:            TSP-04 (deferred parser)
LP Signal:                Line item detail, tender breakdown, discount abuse, void patterns per item
Key Read Methods:         search(), get(order_id), batch_get(), calculate(), clone()
Sample Call (Python):     response = client.orders.search(location_ids=["L88917AVBK2S5"], query={"filter": {"date_time_filter": {"created_at": {"start_at": "2026-02-01T00:00:00Z"}}}})
Dashboard Section Title:  Orders
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_orders
```

---

### 4. Catalog

```
SDK Namespace:            client.catalog
Sandbox Permission:       ITEMS_READ
Canary Phase:             Phase 2
TSP Component:            N/A (reference data — supports Sub 2 parsing)
LP Signal:                Item names, prices, categories, modifiers — enables line-item-level anomaly detection
Key Read Methods:         list(), search(), search_items(), batch_get(), info()
Sample Call (Python):     for item in client.catalog.list(types=["ITEM"]): print(item.id, item.item_data.name)
Dashboard Section Title:  Catalog
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_catalog
```

---

### 5. Inventory

```
SDK Namespace:            client.inventory
Sandbox Permission:       INVENTORY_READ
Canary Phase:             Phase 2
TSP Component:            TSP-04 (deferred parser — inventory.count.updated)
LP Signal:                Shrinkage detection — physical count vs expected, adjustment anomalies, write-off patterns
Key Read Methods:         batch_get_counts(), batch_get_changes(), get_count(catalog_object_id), get_adjustment(adjustment_id), get_changes()
Sample Call (Python):     counts = client.inventory.batch_get_counts(catalog_object_ids=["ITEM_123"])
Dashboard Section Title:  Inventory
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_inventory
```

---

### 6. Customers

```
SDK Namespace:            client.customers
Sandbox Permission:       CUSTOMERS_READ
Canary Phase:             Phase 2
TSP Component:            N/A (reference data — supports card fingerprint correlation)
LP Signal:                Customer-card linkage, repeat refund patterns per customer, loyalty abuse correlation
Key Read Methods:         list(), search(), get(customer_id), bulk_retrieve_customers()
Sample Call (Python):     for customer in client.customers.list(): print(customer.id, customer.given_name)
Dashboard Section Title:  Customers
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_customers
```

---

### 7. Cash Drawers

```
SDK Namespace:            client.cash_drawers.shifts
Sandbox Permission:       CASH_DRAWER_READ
Canary Phase:             Phase 2
TSP Component:            TSP-04 (cash_drawer.shift.*, cash_drawer.event.created)
LP Signal:                Cash variance detection (expected vs actual), cash-in/cash-out anomalies, drawer left open
Key Read Methods:         list(location_id), retrieve(shift_id, location_id)
Sample Call (Python):     for shift in client.cash_drawers.shifts.list(location_id="L88917AVBK2S5"): print(shift.id, shift.state)
Dashboard Section Title:  Cash Drawers
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_cash_drawers
```

**NOTE:** B-047 — Cash Drawer API is **poll-only**. No webhook events. Requires polling adapter (TSP-02 addendum) to feed into TSP pipeline.

---

### 8. Labor (Timecards)

```
SDK Namespace:            client.labor
Sandbox Permission:       TIMECARDS_READ
Canary Phase:             Phase 2
TSP Component:            TSP-04 (deferred parser)
LP Signal:                Ghost employee detection, clock-in without sales, overtime anomalies, break compliance
Key Read Methods:         search_timecards(), retrieve_timecard(timecard_id), create_timecard(), search_scheduled_shifts()
Sub-namespaces:           client.labor.shifts, client.labor.break_types, client.labor.team_member_wages, client.labor.workweek_configs
Sample Call (Python):     response = client.labor.search_timecards(filter={"location_ids": ["L88917AVBK2S5"]})
Dashboard Section Title:  Labor & Timecards
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_labor
```

**NOTE:** B-047 — Labor API is **poll-only**. No webhook events for timecard state changes. Requires polling adapter (same as Cash Drawers).

---

### 9. Team Members

```
SDK Namespace:            client.team_members
Sandbox Permission:       EMPLOYEES_READ
Canary Phase:             Phase 2
TSP Component:            N/A (reference data — supports employee attribution in detections)
LP Signal:                Employee identity resolution, role-based access patterns, terminated employee activity
Key Read Methods:         search(), get(team_member_id), bulk_retrieve_team_members()
Sample Call (Python):     response = client.team_members.search(query={"filter": {"location_ids": ["L88917AVBK2S5"]}})
Dashboard Section Title:  Team Members
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_team_members
```

---

### 10. Loyalty

```
SDK Namespace:            client.loyalty
Sandbox Permission:       LOYALTY_READ
Canary Phase:             Phase 3
TSP Component:            N/A
LP Signal:                Loyalty point fraud — self-awarding, point inflation, redemption without purchase
Key Read Methods:         search_events()
Sub-namespaces:           client.loyalty.accounts (list, create, get, search), client.loyalty.programs (list, get), client.loyalty.rewards (create, search, get, delete)
Sample Call (Python):     response = client.loyalty.search_events(query={"filter": {"location_filter": {"location_ids": ["L88917AVBK2S5"]}}})
Dashboard Section Title:  Loyalty
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 3
explore_ function name:   explore_loyalty
```

---

### 11. Gift Cards

```
SDK Namespace:            client.gift_cards
Sandbox Permission:       GIFTCARDS_READ
Canary Phase:             Phase 2
TSP Component:            TSP-04 (deferred parser — gift_card_activity.created)
LP Signal:                Gift card load/redeem anomalies, balance manipulation, cross-location abuse
Key Read Methods:         list(), get(id), create(), transfer()
Sub-namespaces:           client.gift_cards.activities (list, create)
Sample Call (Python):     for card in client.gift_cards.list(): print(card.id, card.balance_money)
Dashboard Section Title:  Gift Cards
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 2
explore_ function name:   explore_gift_cards
```

---

### 12. Invoices

```
SDK Namespace:            client.invoices
Sandbox Permission:       INVOICES_READ
Canary Phase:             Phase 3
TSP Component:            N/A
LP Signal:                Invoice manipulation, unauthorized discounts, payment collection anomalies
Key Read Methods:         search(), get(invoice_id), create(), publish(invoice_id), cancel(invoice_id)
Sample Call (Python):     response = client.invoices.search(query={"filter": {"location_ids": ["L88917AVBK2S5"]}})
Dashboard Section Title:  Invoices
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 3
explore_ function name:   explore_invoices
```

---

### 13. Disputes

```
SDK Namespace:            client.disputes
Sandbox Permission:       DISPUTES_READ
Canary Phase:             Phase 3
TSP Component:            N/A
LP Signal:                Chargeback patterns, dispute frequency per employee/location, evidence submission tracking
Key Read Methods:         list(), get(dispute_id), accept(dispute_id), submit(dispute_id)
Sub-namespaces:           client.disputes.evidence
Sample Call (Python):     for dispute in client.disputes.list(location_id="L88917AVBK2S5"): print(dispute.id, dispute.state)
Dashboard Section Title:  Disputes
Fetch Button Label:       Fetch Live Data
Phase Badge:              PHASE 3
explore_ function name:   explore_disputes
```

---

### 14. Subscriptions

```
SDK Namespace:            client.subscriptions
Sandbox Permission:       SUBSCRIPTIONS_READ
Canary Phase:             Not planned
TSP Component:            N/A
LP Signal:                Minimal LP relevance — subscription billing is not a loss vector for most merchants
Key Read Methods:         search(), get(subscription_id), list_events(subscription_id), create()
Sample Call (Python):     response = client.subscriptions.search(query={"filter": {"location_ids": ["L88917AVBK2S5"]}})
Dashboard Section Title:  Subscriptions
Fetch Button Label:       Fetch Live Data
Phase Badge:              NOT PLANNED
explore_ function name:   explore_subscriptions
```

---

### 15. Merchants

```
SDK Namespace:            client.merchants
Sandbox Permission:       MERCHANT_PROFILE_READ
Canary Phase:             Phase 1 LIVE (infrastructure)
TSP Component:            N/A (infrastructure — merchant_id extraction from webhook payloads)
LP Signal:                Merchant identity, business type, country — context for all detections
Key Read Methods:         list(), get(merchant_id)
Sub-namespaces:           client.merchants.custom_attribute_definitions, client.merchants.custom_attributes
Sample Call (Python):     response = client.merchants.get(merchant_id="me")
Dashboard Section Title:  Merchant Profile
Fetch Button Label:       Fetch Live Data
Phase Badge:              LIVE
explore_ function name:   explore_merchants
```

---

### 16. Locations

```
SDK Namespace:            client.locations
Sandbox Permission:       MERCHANT_PROFILE_READ
Canary Phase:             Phase 1 LIVE (infrastructure)
TSP Component:            N/A (infrastructure — location_id context for all event routing)
LP Signal:                Multi-location patterns, location-specific anomalies, cross-location fraud rings
Key Read Methods:         list(), get(location_id), create(), update(location_id)
Sub-namespaces:           client.locations.custom_attribute_definitions, client.locations.custom_attributes, client.locations.transactions
Sample Call (Python):     response = client.locations.list()
Dashboard Section Title:  Locations
Fetch Button Label:       Fetch Live Data
Phase Badge:              LIVE
explore_ function name:   explore_locations
```

---

## TSP Coverage Table

| # | API Family | Webhook Events | Sub 1 (Seal) | Sub 2 (Parse) | Sub 3 (Inscribe) | Sub 6 (Detect) | Status |
|---|---|---|---|---|---|---|---|
| 1 | Payments | payment.created, payment.updated | hash + seal | parse_payment | ordinal | C-004, C-007 | LIVE |
| 2 | Refunds | refund.created, refund.updated | hash + seal | parse_refund | ordinal | C-004 (>$10 trigger) | LIVE |
| 3 | Orders | order.created, order.updated | hash + seal | parse_order (Phase 2) | ordinal | deferred | PLANNED |
| 4 | Catalog | N/A (reference data) | N/A | N/A | N/A | N/A | REFERENCE ONLY |
| 5 | Inventory | inventory.count.updated | hash + seal | parse_inventory (Phase 2) | ordinal | C-201+ (Phase 2) | PLANNED |
| 6 | Customers | N/A (reference data) | N/A | N/A | N/A | N/A | REFERENCE ONLY |
| 7 | Cash Drawers | NONE (poll-only, B-047) | hash + seal | parse_cash_drawer (Phase 2) | ordinal | C-101 to C-104 | PLANNED (needs polling adapter) |
| 8 | Labor | NONE (poll-only, B-047) | hash + seal | parse_timecard (Phase 2) | ordinal | C-301 (Phase 2) | PLANNED (needs polling adapter) |
| 9 | Team Members | N/A (reference data) | N/A | N/A | N/A | N/A | REFERENCE ONLY |
| 10 | Loyalty | loyalty.event.created (TBD) | hash + seal | parse_loyalty (Phase 3) | ordinal | deferred | NOT STARTED |
| 11 | Gift Cards | gift_card_activity.created | hash + seal | parse_gift_card (Phase 2) | ordinal | deferred | PLANNED |
| 12 | Invoices | invoice.* (TBD) | hash + seal | parse_invoice (Phase 3) | ordinal | deferred | NOT STARTED |
| 13 | Disputes | dispute.* | hash + seal | parse_dispute (Phase 3) | ordinal | deferred | NOT STARTED |
| 14 | Subscriptions | N/A | N/A | N/A | N/A | N/A | NOT PLANNED |
| 15 | Merchants | N/A (infrastructure) | N/A | N/A | N/A | N/A | INFRASTRUCTURE |
| 16 | Locations | N/A (infrastructure) | N/A | N/A | N/A | N/A | INFRASTRUCTURE |

---

## Phase Summary

| Phase | Families | Status |
|---|---|---|
| **Phase 1 LIVE** | Payments, Refunds, Merchants (infra), Locations (infra) | Operational — 26 webhooks processed, all 200 OK |
| **Phase 2** | Orders, Catalog, Inventory, Customers, Cash Drawers, Labor, Team Members, Gift Cards | Jeremy's LP analysis Tier 1 + Tier 2. Cash Drawers + Labor require polling adapter. |
| **Phase 3** | Loyalty, Invoices, Disputes | Lower LP priority. Webhook event availability TBD for some. |
| **Not Planned** | Subscriptions | No LP signal. Dashboard placeholder only. |

---

## SDK Architecture Notes

### Client Instantiation (v44)
```python
from square import Square

client = Square(
    token=os.environ["SQUARE_ACCESS_TOKEN"],
    environment="sandbox"  # or "production"
)
```

### Async Client
```python
from square import AsyncSquare

client = AsyncSquare(token=..., environment=...)
```

### Pagination
```python
# Stream items (preferred for real-time)
for payment in client.payments.list(location_id="..."):
    process(payment)

# Stream pages (preferred for batch operations)
for page in client.payments.list(location_id="...").iter_pages():
    process_batch(page)
```

### Error Handling
```python
from square.core.api_error import ApiError

try:
    response = client.payments.get(payment_id="...")
except ApiError as e:
    print(e.status_code, e.body)
```

### Webhook Signature Verification (SDK)
```python
from square.utils.webhooks_helper import verify_signature

is_valid = verify_signature(
    request_body=raw_body_string,
    signature_header=request.headers["x-square-hmacsha256-signature"],
    signature_key=os.environ["SQUARE_WEBHOOK_SIGNATURE_KEY"],
    notification_url=os.environ["SQUARE_NOTIFICATION_URL"],
)
```

### Built-in Retries
SDK retries automatically on 408, 429, 5xx with exponential backoff (default: max 2 retries). Configurable via `RequestOptions(max_retries=N)`.

### SDK Version
```
Package: squareup
Version: 44.0.1.20260122
Unpinned: per B-063 standing directive
```

---

## Warnings and Gaps

1. **B-047:** Cash Drawers + Labor are poll-only. No webhook events. TSP-02 needs polling adapter addendum.
2. **B-063:** SDK unpinned. Version could change on next `pip install`. Jeremy's session-open ritual must include version check.
3. **OAuth scopes:** Phase 2 families may require re-authorization to add scopes (INVENTORY_READ, TIMECARDS_READ, etc.).
4. **Legacy SDK:** `connect-python-sdk` in `square/` is deprecated. Do not import. The OAuth example in `connect-api-examples` uses the old `Client` class — do not copy.
5. **Sub 2 parsers:** Existing parsers in `canary/services/parsers/` are pre-TSP. TSP-04 parsers should be built fresh per PRD spec.

---

*Condor | B-067-A | February 28, 2026*
*Gates: Jeremy B-067-B wiring pass + Qwen B-067-C dashboard shell*
