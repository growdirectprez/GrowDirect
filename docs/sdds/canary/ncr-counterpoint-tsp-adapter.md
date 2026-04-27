---
classification: internal
owner: GrowDirect LLC
type: sdd
audience: Canary engineering + ALX
date: 2026-04-26
status: draft-1
depends-on:
  - docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
  - docs/sdds/canary/ncr-counterpoint-square-coupling-audit.md
  - docs/sdds/canary/tsp.md
  - docs/sdds/canary/data-model.md
source-corpus: Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/
companion-wiki:
  - Brain/wiki/ncr-counterpoint-document-model.md
  - Brain/wiki/ncr-counterpoint-endpoint-spine-map.md
  - Brain/wiki/canary-tsp-pipeline.md
---

# SDD — NCR Counterpoint TSP Adapter: Counterpoint → CRDM Sales Schema

## Governing thesis

Square enters Canary through a webhook — an event push from a third party. Counterpoint enters through a polling loop — Canary pulls. The TSP pipeline's job is the same in both cases: validate, hash, parse, and write to the `sales` schema. What changes is the ingress path. This SDD specifies the Counterpoint ingress path and the mapping from every Counterpoint `Document` field to a `sales` schema row. Everything downstream of the `canary:events` stream — Sub1 (seal), Sub3 (Merkle), Sub4 (detect) — is source-agnostic and requires no changes.

The one-line contract: a Counterpoint polling worker polls `GET /Document` on a watermark schedule, builds a `CanonicalEvent` for each document, publishes it to `canary:events`, and Sub2 routes it to the same `sales` schema tables Square uses — extended where Counterpoint's Document model is richer.

## Architecture overview

```
┌────────────────────────────────────────┐
│  Customer site (Counterpoint on-prem)  │
│  REST API server, Windows host         │
│  HTTPS :52000 (or customer-configured) │
└──────────────────┬─────────────────────┘
                   │  poll GET /Document
                   │  HTTP Basic + APIKey header
                   ▼
┌────────────────────────────────────────┐
│  canary/services/pos/counterpoint/     │
│  ┌──────────────────────────────────┐  │
│  │  CounterpointPoller              │  │
│  │  per-tenant, per-company-alias   │  │
│  │  watermark keyed on RS_UTC_DT    │  │
│  └───────────────┬──────────────────┘  │
│                  │ CounterpointEvent   │
│  ┌───────────────▼──────────────────┐  │
│  │  DocumentRouter                  │  │
│  │  DOC_TYP → CanonicalEvent        │  │
│  └───────────────┬──────────────────┘  │
│                  │ CanonicalEvent      │
│  ┌───────────────▼──────────────────┐  │
│  │  stream_publisher.XADD           │  │
│  │  canary:events  (9-field msg)    │  │
│  └───────────────┬──────────────────┘  │
└──────────────────┼─────────────────────┘
                   │
          ┌────────┴──────────────────────┐
          │  TSP consumers (unchanged)    │
          │  Sub1 seal  Sub2 parse        │
          │  Sub3 merkle  Sub4 detect     │
          └───────────────────────────────┘
                   │
          ┌────────▼──────────────────────┐
          │  sales schema (PostgreSQL)    │
          │  transactions, line_items,    │
          │  tenders, taxes, audit_log,   │
          │  evidence_records             │
          └───────────────────────────────┘
```

**Key architectural decisions:**

- The poller runs as a standalone Canary service (`canary/services/pos/counterpoint/poller.py`), one Celery worker per active Counterpoint tenant, scheduled via Valkey-backed task queue.
- Square's `POST /webhooks/square` ingress and Counterpoint's poller are **sibling ingress paths** — both publish to `canary:events` with `source=counterpoint`. No Square code is modified.
- Sub2's parser dispatch is generalized from `event_type → handler` to `(source, event_type) → handler`. This is the only Sub2 change required.
- The `canary:events` 9-field message contract is unchanged. `source` carries `"counterpoint"`.

## Source registration

Before the first poll, the tenant bootstrap step registers Counterpoint as a source:

```sql
-- source_systems (already exists; insert if absent)
INSERT INTO app.source_systems (code, display_name, category)
VALUES ('counterpoint', 'NCR Counterpoint', 'pos')
ON CONFLICT (code) DO NOTHING;

-- external_identities entity_type CHECK extension
-- Add 'cp_document', 'cp_customer', 'cp_item', 'cp_store', 'cp_station'
-- to the existing entity_type CHECK constraint (Alembic migration).
```

The `merchant_sources` record ties a Canary `merchant_id` to a Counterpoint `(base_url, company_alias)` pair. Multi-company deployments (one API server, multiple Counterpoint companies) each get a distinct `merchant_sources` row.

## Authentication

Every Counterpoint API call carries two credentials:

| Header | Value | Source |
|---|---|---|
| `Authorization` | `Basic base64("<company>.<username>:<password>")` | `pos_tenant_credentials` table, encrypted at rest |
| `APIKey` | `<installed key>` | `pos_tenant_credentials` table, encrypted at rest |

The `CounterpointAuthClient` reads credentials from `pos_tenant_credentials` (not from env). Credential rotation triggers a `credential_rotated` event; the poller reloads credentials on the next poll cycle without restart.

Three endpoints do NOT require APIKey (`POST /NSPTransaction`, `POST /Store/{id}/Tokenize`, `GET /Store/{id}/TokenizeInfo`) — the auth client omits the header for those paths.

## Poll loop design

### Watermark strategy

Canary uses `RS_UTC_DT` (the document's UTC timestamp) as the poll watermark. This field is:

- **Indexed** in Counterpoint's SQL Server backing store
- **Sortable** — ISO 8601, UTC
- **Stable** — does not change after a document is committed

Poll query: `GET /Document?orderby=RS_UTC_DT&ascending=true&limit=100&RS_UTC_DT_GTE=<last_watermark>`

Watermark is persisted per `(tenant_id, company_alias, entity_type)` in the `poll_watermarks` table:

```sql
CREATE TABLE app.poll_watermarks (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id   UUID NOT NULL REFERENCES app.merchants(id),
    source_code   TEXT NOT NULL,               -- 'counterpoint'
    company_alias TEXT NOT NULL,
    entity_type   TEXT NOT NULL,               -- 'document', 'customer', 'item', etc.
    last_polled_at TIMESTAMPTZ NOT NULL,
    last_event_ts  TIMESTAMPTZ,               -- RS_UTC_DT of last ingested record
    created_at    TIMESTAMPTZ DEFAULT now(),
    updated_at    TIMESTAMPTZ DEFAULT now(),
    UNIQUE (merchant_id, source_code, company_alias, entity_type)
);
```

### Poll intervals (default)

| Entity | Interval | Rationale |
|---|---|---|
| Document (sales, returns) | 5 min | Core event feed; LP detection latency target |
| Customer | 60 min | Less volatile; loyalty + tier data |
| Item / catalog | 4 h | Seasonal churn is slow; mid-season additions sync within 4 h |
| Store / Station | 24 h | Near-static; catch hardware changes |
| PayCode / TaxCode | 24 h | Rarely changes |

Intervals are per-tenant-configurable via `pos_poll_config` (extends `merchant_sources`). A `no-cache` header (`ServerCache: no-cache`) is sent only when fresh data is demanded (explicit refresh trigger), not on every poll.

### Rate limiting

Counterpoint's REST API server is on-prem Windows — there is no published rate limit, but the server runs on the customer's hardware alongside the POS terminals. Canary enforces:

- Max 5 concurrent requests per tenant
- 100ms minimum gap between paginated page fetches
- 429 / 5xx → exponential backoff (base 2s, max 120s, jitter ±20%)
- Consecutive failure count per tenant stored in Valkey; alert at count ≥ 5

## Document → CanonicalEvent routing

The `DocumentRouter` reads `DOC_TYP` (and `RET_LINS > 0` as a secondary discriminator) and emits one or more `CanonicalEvent` objects per Document. Every CanonicalEvent goes to `canary:events`.

| DOC_TYP | Condition | CanonicalEvent.event_type | Spine | Priority |
|---|---|---|---|---|
| `T` | `RET_LINS == 0` | `transaction.created` | T | P1 |
| `T` | `RET_LINS > 0` | `transaction.return` | T, Q | P1 |
| `T` | `IS_DOC_COMMITTED == "N"` and older than 24h | `transaction.voided` | T, Q | P1 |
| `XFER` | — | `inventory.transfer` | D | P3 |
| `RECVR` | — | `purchase.received` | J | P3 |
| `PO` | — | `purchase_order.created` | J | P3 |
| `PREQ` | — | `purchase_order.requested` | J | P3 |
| `RTV` | — | `purchase.return_to_vendor` | J | P3 |
| `GFC` | — | `gift_card.transaction` | F | P1 |
| `AR_DOC` | — | `ar.document` | C, F | P4 |
| unknown | — | `document.unrouted` | — | log + DLQ |

**Phase scoping:** P1 events (sales, returns, voids, gift cards) are ingested from day one. P3 events (transfers, POs, receivers) are ingested but parked in the CRDM without Chirp detection rules until Phase 3 spine modules are live. P4 events (AR) are captured but not processed until Phase 4.

Documents with `IS_DOC_COMMITTED == "N"` are ingested as `transaction.draft` and re-evaluated on subsequent polls. A draft that disappears from the feed without becoming committed within 24h is emitted as `transaction.voided`.

## Counterpoint Document → `sales` schema field mapping

### `sales.transactions`

This is the P1 core. Every `transaction.created` and `transaction.return` CanonicalEvent writes one row.

| `sales.transactions` column | Counterpoint source | Transform |
|---|---|---|
| `id` | — | Canary UUID (generated) |
| `merchant_id` | poller context | tenant binding |
| `source_code` | — | `'counterpoint'` |
| `external_id` | `PS_DOC_HDR.DOC_ID` | string passthrough |
| `external_guid` | `PS_DOC_HDR.DOC_GUID` | string passthrough |
| `location_id` | resolved via `external_identities` from `PS_DOC_HDR.STR_ID` | UUID lookup |
| `device_id` | resolved via `external_identities` from `PS_DOC_HDR.STA_ID` | UUID lookup |
| `employee_id` | resolved via `external_identities` from `PS_DOC_HDR.USR_ID` | UUID lookup (degraded — API user, not full employee) |
| `customer_id` | resolved via `external_identities` from `PS_DOC_HDR.CUST_NO` (null if `"CASH"`) | UUID lookup or null |
| `transaction_type` | `PS_DOC_HDR.DOC_TYP` + `RET_LINS` | `'sale'` / `'return'` / `'void'` |
| `occurred_at` | `PS_DOC_HDR.RS_UTC_DT` | ISO 8601 → TIMESTAMPTZ |
| `ticket_date` | `PS_DOC_HDR.TKT_DT` | local date |
| `ticket_number` | `PS_DOC_HDR.TKT_NO` | human-readable ref |
| `drawer_id` | `PS_DOC_HDR.DRW_ID` | string |
| `drawer_session_id` | `PS_DOC_HDR.DRW_SESSION_ID` | string |
| `sales_rep` | `PS_DOC_HDR.SLS_REP` | string (secondary employee ref) |
| `stock_location_id` | `PS_DOC_HDR.STK_LOC_ID` | string (Counterpoint location code) |
| `subtotal_amount` | `PS_DOC_HDR_TOT[type="SUB_TOT"].AMT` | integer cents |
| `discount_amount` | `PS_DOC_HDR_TOT[type="TOT_LIN_DISC"].AMT + PS_DOC_HDR_TOT[type="TOT_HDR_DISC"].AMT` | integer cents, sum |
| `tax_amount` | `PS_DOC_HDR_TOT[type="TAX_AMT"].AMT` | integer cents |
| `total_amount` | `PS_DOC_HDR_TOT[type="TOT"].AMT` | integer cents |
| `total_cost` | `PS_DOC_HDR_TOT[type="TOT_EXT_COST"].AMT` | integer cents — **gross margin computable** |
| `tender_total` | `PS_DOC_HDR_TOT[type="TOT_TND"].AMT` | integer cents |
| `change_amount` | `PS_DOC_HDR_TOT[type="TOT_CHNG"].AMT` | integer cents |
| `amount_due` | `PS_DOC_HDR_TOT[type="AMT_DUE"].AMT` | integer cents |
| `sale_line_count` | `PS_DOC_HDR.SAL_LINS` | integer |
| `return_line_count` | `PS_DOC_HDR.RET_LINS` | integer |
| `is_committed` | `PS_DOC_HDR.IS_DOC_COMMITTED` | bool |
| `is_offline` | `PS_DOC_HDR.IS_OFFLINE` | bool — flag offline-mode transactions for data-quality audit |
| `tax_code` | `PS_DOC_HDR.TAX_COD` | string |
| `raw_payload` | full `PS_DOC_HDR` JSON | JSONB — stored without `SIG_IMG` / `SIG_IMG_VECTOR` |

**New columns required** (Alembic migration, additive — no Square columns touched):

```python
# In sales.transactions
source_code: Mapped[str]                          # 'square' | 'counterpoint'
external_guid: Mapped[Optional[str]]              # DOC_GUID (Counterpoint cross-system key)
ticket_number: Mapped[Optional[str]]              # TKT_NO
drawer_session_id: Mapped[Optional[str]]          # DRW_SESSION_ID
sales_rep: Mapped[Optional[str]]                  # SLS_REP
stock_location_id: Mapped[Optional[str]]          # STK_LOC_ID
total_cost: Mapped[Optional[int]]                 # TOT_EXT_COST (cents) → enables gross margin
is_committed: Mapped[Optional[bool]]              # IS_DOC_COMMITTED
is_offline: Mapped[Optional[bool]]                # IS_OFFLINE
```

Square rows leave these null. Counterpoint rows populate them. No Square behavior changes.

### `sales.line_items`

One row per `PS_DOC_LIN` entry. Keyed on `(transaction_id, line_seq_no)`.

| `sales.line_items` column | Counterpoint source | Transform |
|---|---|---|
| `id` | — | Canary UUID |
| `transaction_id` | FK to `sales.transactions.id` | — |
| `source_code` | — | `'counterpoint'` |
| `external_id` | `PS_DOC_LIN.LIN_GUID` | string |
| `line_seq_no` | `PS_DOC_LIN.LIN_SEQ_NO` | integer |
| `line_type` | `PS_DOC_LIN.LIN_TYP` | `'S'` / `'R'` / other |
| `item_no` | `PS_DOC_LIN.ITEM_NO` | string |
| `item_id` | resolved via `external_identities` from `ITEM_NO` | UUID lookup or null |
| `description` | `PS_DOC_LIN.DESCR` | string |
| `category_code` | `PS_DOC_LIN.CATEG_COD` | string |
| `subcategory_code` | `PS_DOC_LIN.SUBCAT_COD` | string |
| `vendor_no` | `PS_DOC_LIN.ITEM_VEND_NO` | string (Module J cross-ref) |
| `qty_sold` | `PS_DOC_LIN.QTY_SOLD` | decimal |
| `qty_numerator` | `PS_DOC_LIN.QTY_NUMER` | integer (fractional unit numerator) |
| `qty_denominator` | `PS_DOC_LIN.QTY_DENOM` | integer (fractional unit denominator) |
| `qty_unit` | `PS_DOC_LIN.QTY_UNIT` | string (`'EA'`, `'LB'`, etc.) |
| `unit_price` | `PS_DOC_LIN.PRC` | integer cents |
| `regular_price` | `PS_DOC_LIN.REG_PRC` | integer cents |
| `extended_price` | `PS_DOC_LIN.EXT_PRC` | integer cents |
| `extended_cost` | `PS_DOC_LIN.EXT_COST` | integer cents |
| `has_price_override` | `PS_DOC_LIN.HAS_PRC_OVRD` | bool — **Module Q signal** |
| `is_discountable` | `PS_DOC_LIN.IS_DISCNTBL` | bool |
| `mix_match_code` | `PS_DOC_LIN.MIX_MATCH_COD` | string (H&G garden center mix-and-match pricing) |
| `tax_allocated` | `PS_DOC_LIN.TAX_AMT_ALLOC` | integer cents |
| `barcode` | `PS_DOC_LIN.BARCOD` | string |
| `is_kit_parent` | `PS_DOC_LIN.IS_KIT_PAR` | bool |

**Note on fractional quantities:** garden centers sell in fractional units (partial flats, cut quantities). `QTY_NUMER / QTY_DENOM` preserves the exact rational quantity. `QTY_SOLD` is the decimal approximation. Both are stored.

**Note on pricing rules:** `PS_DOC_LIN_PRICE[]` (pricing rule applied) is stored as a JSONB array in `line_items.pricing_rules_json` — not normalized. Module P reads from this to reconstruct observable pricing behavior without needing live pricing rule endpoints.

### `sales.tenders`

One row per `PS_DOC_PMT` entry.

| `sales.tenders` column | Counterpoint source | Transform |
|---|---|---|
| `id` | — | Canary UUID |
| `transaction_id` | FK | — |
| `source_code` | — | `'counterpoint'` |
| `seq_no` | `PS_DOC_PMT.PMT_SEQ_NO` | integer |
| `pay_code` | `PS_DOC_PMT.PAY_COD` | string (CASH, VISA, ZELLE, etc.) |
| `pay_code_type` | `PS_DOC_PMT.PAY_COD_TYP` | string |
| `line_type` | `PS_DOC_PMT.PMT_LIN_TYP` | `'T'` / `'R'` |
| `amount` | `PS_DOC_PMT.AMT` | integer cents |
| `currency_code` | `PS_DOC_PMT.CURNCY_COD` | ISO 4217 |
| `exchange_rate` | `PS_DOC_PMT.EXCH_RATE_NUMER / EXCH_RATE_DENOM` | decimal |
| `is_swiped` | `PS_DOC_PMT.SWIPED` | bool |
| `is_ecommerce` | `PS_DOC_PMT.SECURE_ECOMM_TRX` | bool |
| `auth_flag` | `PS_DOC_PMT.EDC_AUTH_FLG` | string |
| `signature_captured` | `PS_DOC_PMT.SIG_IMG IS NOT NULL` | bool — **raw image NEVER persisted** |

**PII enforcement:** `SIG_IMG` and `SIG_IMG_VECTOR` are stripped at parse time, before the raw_payload is written. The parser asserts `"SIG_IMG" not in stored_payload` before committing.

### `sales.transaction_taxes`

One row per `PS_DOC_TAX` entry (multi-authority). New table for Counterpoint; Square does not provide this granularity.

```sql
CREATE TABLE sales.transaction_taxes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id  UUID NOT NULL REFERENCES sales.transactions(id),
    source_code     TEXT NOT NULL DEFAULT 'counterpoint',
    authority_code  TEXT NOT NULL,       -- e.g. 'MEMPHIS', 'SHELBY', 'TN'
    tax_amount      INTEGER NOT NULL,    -- cents
    taxable_amount  INTEGER NOT NULL,    -- cents
    rule_code       TEXT,               -- e.g. 'TAX'
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON sales.transaction_taxes (transaction_id);
CREATE INDEX ON sales.transaction_taxes (authority_code, source_code);
```

### `sales.transaction_audit_log`

Flattened from `PS_DOC_AUDIT_LOG[]`. This is the primary substrate for Module Q (Loss Prevention) detection rules — every state change on a Document is logged with user, workstation, drawer, and timestamp.

```sql
CREATE TABLE sales.transaction_audit_log (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id  UUID NOT NULL REFERENCES sales.transactions(id),
    source_code     TEXT NOT NULL DEFAULT 'counterpoint',
    log_seq_no      INTEGER NOT NULL,
    doc_type        TEXT,                -- state of DOC_TYP at log time
    logged_at       TIMESTAMPTZ NOT NULL,-- CURR_DT → UTC
    store_id        TEXT,               -- CURR_STR_ID
    station_id      TEXT,               -- CURR_STA_ID
    drawer_id       TEXT,               -- CURR_DRW_ID
    user_id         TEXT,               -- CURR_USR_ID
    workstation_name TEXT,
    activity        TEXT,               -- ACTIV
    log_entry       TEXT,               -- human-readable LOG_ENTRY
    created_at      TIMESTAMPTZ DEFAULT now(),
    UNIQUE (transaction_id, log_seq_no)
);
CREATE INDEX ON sales.transaction_audit_log (transaction_id);
CREATE INDEX ON sales.transaction_audit_log (user_id, logged_at);
CREATE INDEX ON sales.transaction_audit_log (activity, logged_at);
```

### `sales.document_original_refs`

For returns and voids: `PS_DOC_HDR_ORIG_DOC[]` links back to the originating sale. Required for `transaction.return` event type and for refund-without-original-sale detection rules (Module Q).

```sql
CREATE TABLE sales.document_original_refs (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id    UUID NOT NULL REFERENCES sales.transactions(id),
    source_code       TEXT NOT NULL DEFAULT 'counterpoint',
    orig_doc_id       TEXT NOT NULL,    -- DOC_ID of the original sale
    orig_transaction_id UUID,           -- resolved FK after lookup; null if not yet ingested
    created_at        TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON sales.document_original_refs (transaction_id);
CREATE INDEX ON sales.document_original_refs (orig_doc_id);
```

The FK `orig_transaction_id` is resolved lazily — the original sale may not yet be in the CRDM if the return arrived before the back-fill. A reconciliation pass binds orphaned refs after full historical sync.

## `external_identities` registrations

Every Counterpoint entity that resolves to a Canary UUID goes through `app.external_identities`. The entity type taxonomy for Counterpoint:

| `entity_type` | Counterpoint source field | Canary target table |
|---|---|---|
| `cp_document` | `PS_DOC_HDR.DOC_ID` | `sales.transactions.id` |
| `cp_customer` | `AR_CUST.CUST_NO` | `app.customers.id` |
| `cp_item` | `IM_ITEM.ITEM_NO` | `app.products.id` |
| `cp_store` | `PS_STR.STR_ID` | `app.locations.id` |
| `cp_station` | `PS_STA.STA_ID` | `app.devices.id` |
| `cp_user` | `SY_USR.USR_ID` | `app.employees.id` (degraded; API user ≠ full employee) |
| `cp_workgroup` | `PS_WRKGRP.WRKGRP_ID` | `app.locations.id` (store-group hierarchy) |

All registrations use `source_code='counterpoint'` and the company_alias in the `source_merchant_id` field.

## Sub2 dispatch generalization

The current Sub2 dispatch is a flat dict:
```python
EVENT_TYPE_PARSERS: dict[str, Callable] = {
    "payment.created": parse_square_payment,
    ...
}
```

Generalized to compound key:
```python
EVENT_TYPE_PARSERS: dict[tuple[str, str], Callable] = {
    ("square", "payment.created"):    parse_square_payment,
    ("counterpoint", "transaction.created"): parse_cp_transaction,
    ("counterpoint", "transaction.return"):  parse_cp_return,
    ("counterpoint", "transaction.voided"):  parse_cp_void,
    ("counterpoint", "gift_card.transaction"): parse_cp_giftcard,
    ...
}
```

Route resolution: `EVENT_TYPE_PARSERS.get((msg["source"], msg["event_type"]))`. Square routes are unchanged. Falls through to DLQ on unknown `(source, event_type)` pairs.

## Parser shapes

### `parse_cp_transaction(event: CanonicalEvent) → list[SQLAlchemy model instances]`

Returns a transaction row + N line_item rows + M tender rows + K tax rows + J audit_log rows + up to 1 original_ref row. All written in a single DB transaction (atomic).

Steps:
1. Parse `PS_DOC_HDR` → `sales.transactions` row (see field mapping above)
2. Strip `SIG_IMG` / `SIG_IMG_VECTOR` from `raw_payload` before assigning
3. For each `PS_DOC_LIN`: parse → `sales.line_items` row
4. For each `PS_DOC_PMT`: parse → `sales.tenders` row (assert no SIG_IMG in row)
5. For each `PS_DOC_TAX`: parse → `sales.transaction_taxes` row
6. For each `PS_DOC_AUDIT_LOG`: parse → `sales.transaction_audit_log` row
7. If `PS_DOC_HDR_ORIG_DOC` is non-empty: parse → `sales.document_original_refs` row(s)
8. Register `external_identities` rows for DOC_ID, CUST_NO (if not "CASH"), USR_ID, STR_ID, STA_ID
9. If `IS_DOC_COMMITTED == "Y"` and `SAL_LINS > 0`: publish `canary:detection` message for Sub4

### `parse_cp_return(event: CanonicalEvent)`

Same as `parse_cp_transaction` with `transaction_type = 'return'`. Always writes `document_original_refs` from `PS_DOC_HDR_ORIG_DOC`. Module Q detection rule for return-without-original-reference reads this table.

### `parse_cp_void(event: CanonicalEvent)`

Writes a `transaction_type = 'void'` row. Does not write line_items or tenders (void has no financial lines). Writes audit_log rows only. Publishes to `canary:detection` with `detection_type = 'void_transaction'`.

### `parse_cp_giftcard(event: CanonicalEvent)`

`DOC_TYP = 'GFC'` documents flow to `sales.gift_card_transactions` (existing table). Field mapping:

| `sales.gift_card_transactions` | Counterpoint source |
|---|---|
| `gift_card_no` | `PS_DOC_GFC[0].GFC_NO` |
| `activity_type` | `PS_DOC_GFC[0].GFC_ACT_TYP` |
| `amount` | `PS_DOC_GFC[0].AMT` |
| `balance_after` | `PS_DOC_GFC[0].BAL_AFTER` |
| `transaction_id` | FK to the parent Document's `sales.transactions.id` |

## Evidence chain integration

Sub1 (seal) is source-agnostic — it reads `event_hash` and `raw_payload` from the stream message, not from the source. The Counterpoint raw payload written to `evidence_records` is the full `PS_DOC_HDR` JSON **with `SIG_IMG` / `SIG_IMG_VECTOR` stripped** at the poller (before it ever enters the stream). The hash is computed over the stripped bytes, ensuring the evidence chain is consistent with what Canary stores.

## Module Q integration (detection substrate)

After Sub2 writes the `sales` schema rows, it publishes to `canary:detection` with:

```python
{
  "transaction_id":  str(transaction.id),
  "merchant_id":     str(merchant.id),
  "event_type":      "transaction.created",
  "event_id":        event_id,
  "detection_type":  "transaction",       # same discriminator Sub4 already uses
  "source_code":     "counterpoint",      # new field; Sub4 routes rules by applicable_sources
}
```

Sub4 gates each Chirp rule against an `applicable_sources` set. Rules already validated against Counterpoint data are added to that set; Square-only rules (e.g. card_fingerprint velocity — `C-005`) exclude `"counterpoint"` until the garden-center rule catalog specifies an equivalent.

The `transaction_audit_log` table is the primary Counterpoint-specific detection substrate. Module Q rules that key on audit log entries (void patterns, price-override frequency, off-hours drawer sessions) join against this table, not against Square's equivalent event fields.

See `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` for the 23-rule H&G catalog.

## Acceptance criteria

Per the delivery spec (Cycles 7–9), this adapter is complete when:

- [ ] Poll loop runs for an active Counterpoint tenant; Documents appear in `canary:events` within 5 min of creation
- [ ] `sales.transactions` contains one row per polled committed Document (DOC_TYP=T), keyed on DOC_ID
- [ ] `sales.line_items` row count = sum of `SAL_LINS` across all polled Documents (validated against Counterpoint API response)
- [ ] `sales.tenders` row count = total `PS_DOC_PMT` entries across polled Documents
- [ ] `sales.transaction_taxes` row count = total `PS_DOC_TAX` entries
- [ ] `sales.transaction_audit_log` populated for every polled Document
- [ ] `SIG_IMG` / `SIG_IMG_VECTOR` absent from all stored rows and raw_payload blobs (asserted by integration test)
- [ ] Square tenants: zero behavior change, zero new rows in any of the above tables
- [ ] Return Documents: `document_original_refs` populated; `orig_transaction_id` resolved where original is present
- [ ] Watermark advances correctly; re-poll of same tenant does not duplicate rows (idempotency on DOC_ID)
- [ ] 429 / 5xx backoff fires in integration test under simulated rate pressure

## Open questions (resolve against sandbox / Bart call)

| # | Question | Impact |
|---|---|---|
| Q-01 | Exact DOC_TYP code string for voids — is it a separate type or `IS_DOC_COMMITTED=N` with no type change? | `DocumentRouter` void branch logic |
| Q-02 | LIN_TYP values beyond `S` and `R` — kit parent lines, service lines, gift card lines | `line_items.line_type` CHECK constraint |
| Q-03 | `IS_DOC_COMMITTED=N` documents — do they appear in `GET /Document` poll responses? | Whether draft-filtering is needed |
| Q-04 | DOC_TYP for dead-count / live-goods write-off (garden center shrink) | Garden center LP rule substrate |
| Q-05 | Pagination contract — does `RS_UTC_DT_GTE` filter work server-side, or must the poller filter client-side? | Poll efficiency and back-fill design |
| Q-06 | `USR_ID` field — is it the till operator or the manager who approved? | Employee LP rules accuracy |
| Q-07 | Multi-company: can two `company_alias` values share a single API server instance, or does each need its own base URL? | `pos_tenant_credentials` schema |

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — module-level integration SDD (this SDD is the adapter-level detail)
- `docs/sdds/canary/ncr-counterpoint-square-coupling-audit.md` — coupling audit (Phase 0a)
- `docs/sdds/canary/tsp.md` — TSP pipeline SDD
- `docs/sdds/canary/data-model.md` — full CRDM model SDD
- `Brain/wiki/ncr-counterpoint-document-model.md` — Document model deep-dive
- `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md` — per-endpoint CRDM mapping
- `Brain/wiki/canary-tsp-pipeline.md` — TSP pipeline wiki
- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — Module Q rule catalog (H&G)
- `docs/superpowers/plans/2026-04-25-canary-for-rapidpos-delivery-spec.md` — delivery roadmap

---

**Author:** ALX (laptop), 2026-04-26  
**Status:** draft-1 — open questions Q-01 through Q-07 resolve against NCR sandbox or Bart call  
**Review gate:** founder reviews before Cycle 8 model migration starts
