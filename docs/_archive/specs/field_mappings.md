---
type: spec
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# Field Mappings: Square Webhook to CRDM

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

Square webhook events are parsed by the TSP pipeline and mapped to CRDM tables.
This document covers all 6 event types tested by the data pump suite.

Parser source files:
- `canary/services/parsers/square_payment_parser.py`
- `canary/services/parsers/square_order_parser.py`
- `canary/services/parsers/square_auxiliary_parsers.py`
- `canary/services/tsp/consumers/sub2_parse.py` (order Transaction creation)

---

## 1. payment.created / payment.updated -> transactions

Parser: `parse_payment(payload)`

| Square Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `merchant_id` (root) | string | `merchant_id` | varchar | Direct |
| `data.object.id` | string | `external_id` | varchar | Direct |
| `data.object.order_id` | string | `order_id` | varchar | Direct |
| `data.object.receipt_number` | string | `receipt_number` | varchar | Direct |
| `data.object.location_id` | string | `location_id` | varchar | Direct |
| `data.object.team_member_id` | string | `employee_id` | varchar | Direct |
| `data.object.customer_id` | string | `customer_id` | varchar | Direct |
| `data.object.device_details.device_id` | string | `device_id` | varchar | Nested extract |
| `data.object.amount_money.amount` | int (cents) | `amount_cents` | int | Direct |
| `data.object.amount_money.currency` | string | `currency` | varchar | Direct |
| `data.object.tax_money.amount` | int (cents) | `tax_amount_cents` | int | Fallback: `total_tax_money.amount`. Default 0 |
| `data.object.tip_money.amount` | int (cents) | `tip_amount_cents` | int | Default 0 |
| _(not available at payment level)_ | | `discount_amount_cents` | int | Hardcoded 0 |
| `data.object.card_details.card.fingerprint` | string | `card_fingerprint` | varchar | Nested extract |
| `data.object.card_details.card.card_brand` | string | `card_brand` | varchar | Nested extract |
| `data.object.card_details.card.last_4` | string | `card_last4` | varchar | Nested extract |
| `data.object.card_details.card.prepaid_type` | string | `card_prepaid_type` | varchar | Nested extract |
| `data.object.card_details.cvv_status` | string | `cvv_status` | varchar | Direct |
| `data.object.card_details.avs_status` | string | `avs_status` | varchar | Direct |
| `data.object.card_details.entry_method` | string | `entry_method` | varchar | Direct |
| `data.object.source_type` | string | `square_product` | varchar | Default "WEBHOOK" |
| `data.object.risk_evaluation.risk_level` | string | `risk_level` | varchar | Nested extract |
| `data.object.created_at` | ISO datetime | `transaction_date` | datetime | `fromisoformat()` |
| `data.object.status` + `capabilities` + `refund_money` | composite | `transaction_type` | varchar | Logic: NO_SALE if capabilities contains "NO_SALE", SALE if COMPLETED with no refund, RETURN if COMPLETED with refund, POST_VOID if CANCELED with updated_at > created_at, else VOID |
| _(entire payload)_ | dict | `payload` | text | `json.dumps(payload)` |

---

## 2. refund.created -> transactions + refund_links

Parser: `parse_refund(payload)`

### transactions (transaction_type forced to "RETURN" by sub2_parse)

| Square Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `merchant_id` (root) | string | `merchant_id` | varchar | Direct |
| `data.object.id` | string | `external_id` | varchar | Direct |
| `data.object.location_id` | string | `location_id` | varchar | Direct |
| `data.object.team_member_id` | string | `employee_id` | varchar | Direct |
| `data.object.amount_money.amount` | int (cents) | `amount_cents` | int | Default 0 |
| `data.object.amount_money.currency` | string | `currency` | varchar | Default "USD" |
| `data.object.created_at` | ISO datetime | `transaction_date` | datetime | `fromisoformat()` |
| _(hardcoded)_ | | `source_type` | varchar | "WEBHOOK" |
| _(entire payload)_ | dict | `payload` | text | `json.dumps(payload)` |

### refund_links

| Square Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `merchant_id` (root) | string | `merchant_id` | varchar | Direct |
| `data.object.id` | string | `refund_external_id` | varchar | Direct |
| `data.object.payment_id` | string | `original_external_id` | varchar | Direct (links refund to original payment) |
| `data.object.amount_money.amount` | int (cents) | `refund_amount_cents` | int | Direct |
| `data.object.reason` | string | `reason` | varchar | Direct |
| `data.object.team_member_id` | string | `employee_id` | varchar | Direct |
| `data.object.location_id` | string | `location_id` | varchar | Direct |

---

## 3. order.created / order.updated -> transactions

Created inline by sub2_parse (not the order parser).

| Square Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `merchant_id` (root) | string | `merchant_id` | varchar | Direct |
| `data.object.id` | string | `external_id` | varchar | Direct |
| `data.object.id` | string | `order_id` | varchar | Same as external_id |
| `data.object.location_id` | string | `location_id` | varchar | Direct |
| _(hardcoded)_ | | `transaction_type` | varchar | "SALE" |
| `data.object.created_at` | ISO datetime | `transaction_date` | datetime | Direct (string) |
| `data.object.total_money.amount` | int (cents) | `amount_cents` | int | Default 0 |
| `data.object.total_tax_money.amount` | int (cents) | `tax_amount_cents` | int | Default 0 |
| `data.object.total_discount_money.amount` | int (cents) | `discount_amount_cents` | int | Default 0 |
| _(hardcoded)_ | | `source_type` | varchar | "WEBHOOK" |

---

## 4. order.created / order.updated -> transaction_line_items

Parser: `parse_order_line_items(payload)`

Source path: `payload.order.line_items[]`

| Square Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `merchant_id` (root) | string | `merchant_id` | varchar | Direct |
| _(set by sub2_parse)_ | | `transaction_id` | uuid | FK to parent Transaction |
| `catalog_object_id` | string | `catalog_object_id` | varchar | Direct |
| `name` | string | `item_name` | varchar | Default "Unknown Item" |
| `variation_name` | string | `variation_name` | varchar | Direct |
| _(resolved via catalog)_ | string | `category_name` | varchar | Catalog lookup, null if missing |
| `quantity` | string | `quantity` | decimal | `Decimal(quantity_str)` |
| `base_price_money.amount` | int (cents) | `base_price_cents` | int | Default 0 |
| `gross_sales_money.amount` | int (cents) | `gross_sales_cents` | int | Default 0 |
| `total_discount_money.amount` | int (cents) | `total_discount_cents` | int | Default 0 |
| `total_tax_money.amount` | int (cents) | `total_tax_cents` | int | Default 0 |
| `item_type` | string | `item_type` | varchar | Default "ITEM" |
| `returns[].return_line_items` | array | `is_voided` | boolean | True if matching return exists |
| `returns[].reason` | string | `return_reason` | varchar | Matched by uid |

---

## 5. order.created / order.updated -> transaction_tenders

Parser: `parse_order_tenders(payload)`

Source path: `payload.order.tenders[]`

| Square Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `merchant_id` (root) | string | `merchant_id` | varchar | Direct |
| _(set by sub2_parse)_ | | `transaction_id` | uuid | FK to parent Transaction |
| `type` | string | `tender_type` | varchar | Direct (CARD, CASH, etc.) |
| `amount_money.amount` | int (cents) | `amount_cents` | int | Default 0 |
| `card_details.card.card_brand` | string | `card_brand` | varchar | Nested extract, null for CASH |
| `card_details.card.last_4` | string | `card_last4` | varchar | Nested extract, null for CASH |
| `card_details.entry_method` | string | `entry_method` | varchar | Nested extract, null for CASH |
| `payment_id` | string | `payment_id` | varchar | Links tender to payment Transaction |
| `employee_id` or `team_member_id` | string | `team_member_id` | varchar | Fallback chain |

---

## 6. inventory.count.updated -> inventory_adjustments

Parser: `parse_inventory_adjustment(payload)`

| Square Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `merchant_id` (root) | string | `merchant_id` | varchar | Direct |
| `data.object.id` | string | `square_adjustment_id` | varchar | Direct |
| `data.object.catalog_object_id` | string | `catalog_object_id` | varchar | Direct |
| `data.object.location_id` | string | `location_id` | varchar | Direct |
| `data.object.physical_count.quantity` | string | `quantity_change` | decimal | `Decimal()`. For ADJUSTMENT type, reads from `adjustment.quantity` |
| `data.object.type` | string | `adjustment_type` | varchar | PHYSICAL_COUNT or ADJUSTMENT |
| `data.object.team_member_id` | string | `team_member_id` | varchar | Direct |
| `data.object.occurred_at` | ISO datetime | `occurred_at` | datetime | `fromisoformat()` |

---

## Evidence Records (all event types)

Sub 1 (seal) writes to `evidence_records` for every event type.

| Stream Field | Type | CRDM Field | Type | Transform |
|---|---|---|---|---|
| `event_id` | string | `event_id` | varchar | Direct |
| `merchant_id` | string | `merchant_id` | varchar | Direct |
| `source` | string | `source` | varchar | Direct ("square") |
| `source_event_id` | string | `source_event_id` | varchar | Direct |
| `event_type` | string | `event_type` | varchar | Direct |
| `raw_payload` | string | `raw_payload` | text | Direct |
| `raw_payload` | string | `parsed_payload` | jsonb | `json.loads()` if parse_failed=false |
| SHA-256(raw_payload) | bytes | `event_hash` | bytea | Recomputed and verified against stream field |
| SHA-256(previous_chain_hash \|\| event_hash) | bytes | `chain_hash` | bytea | Computed per merchant chain |
| _(previous record)_ | bytes | `previous_chain_hash` | bytea | Read from last record for this merchant |
| `received_at` | ISO datetime | `received_at` | datetime | `fromisoformat()` |
| `parse_failed` | string | `parse_failed` | boolean | "true"/"false" string comparison |
