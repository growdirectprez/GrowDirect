# Transaction Stream Processor (TSP)

> **Status:** Complete — written from code
> **Namespace:** canary
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/tsp/`, `Canary/canary/models/sales/`

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

---

## 1. Overview

The Transaction Stream Processor (TSP) is Canary's core data ingestion pipeline. It receives webhook events from Square, validates their authenticity, publishes them to a Valkey stream, and fans them out to four independent consumer groups that each perform a distinct function: cryptographic evidence sealing, CRDM record parsing, Merkle tree batching for Bitcoin inscription, and Chirp rule evaluation.

The pipeline was originally called the "Triple Subscriber Pipeline" (three consumers at launch), extended to four consumers with the addition of Sub 4 (detection). The name TSP is canonical throughout the codebase and documentation.

**Core guarantees:**

- Every webhook is SHA-256 hashed from raw bytes _before_ any JSON parsing. The hash is the immutable identity of the payload as received.
- Sub 1 (seal) stores the raw payload verbatim in a write-once evidence table. No updates, no deletes — enforced at the database layer with triggers.
- Sub 2 (parse) routes the parsed payload into structured CRDM tables that feed the Chirp detection engine.
- Sub 3 (merkle) accumulates event hashes into deterministic Merkle trees and prepares them for Bitcoin inscription, providing permanent public proof of notarization.
- Sub 4 (detect) reads from a separate detection stream published by Sub 2, evaluates each CRDM record against the Chirp rule engine, and writes alerts.
- Each consumer group is independent: a failure in Sub 3 does not affect Sub 1 or Sub 2.

**Patent:** The hash-before-parse ordering, chain hash construction, and Merkle inscription design are covered under Patent Application #63/991,596. The Merkle tree construction algorithm is confidential.

---

## 2. Architecture

### Component Diagram

```
Square Webhooks
      |
      v
[ POST /webhooks/<source> ]   (Flask — webhooks_tsp.py)
      |
      | 1. HMAC-SHA256 validate
      | 2. SHA-256 hash raw bytes
      | 3. JSON parse + enrich
      | 4. Stateless Chirp (Tier 1)
      | 5. Idempotency check (Valkey DB 3)
      | 6. XADD → canary:events (Valkey DB 4)
      | 7. INSERT ingestion_log
      |
      v
 canary:events (Valkey Stream DB 4)
      |
      +----------+-----------+
      |          |           |
      v          v           v
  sub1-seal  sub2-parse  sub3-merkle
  (Sub 1)    (Sub 2)     (Sub 3)
      |          |           |
      |          | XADD      |
      |          v           |
      |    canary:detection  |
      |    (Valkey DB 4)     |
      |          |           |
      v          v           v
evidence_  CRDM tables  inscription_pool
records    (canary_sales) + event_inscriptions
(canary_                    (canary_sales)
 sales)            |
            detection-engine
                (Sub 4)
                   |
                   v
            canary_app.alerts
```

### Request / Data Flow

**Phase 1 — Webhook Gateway (synchronous, sub-5ms)**

1. Square POSTs to `POST /webhooks/square`.
2. Raw bytes are read from the request body before any parsing.
3. HMAC-SHA256 signature is verified against `X-Square-Hmacsha256-Signature` using `SQUARE_WEBHOOK_SIGNATURE_KEY` and `SQUARE_NOTIFICATION_URL`. Invalid signatures return `401`.
4. SHA-256 of raw bytes is computed. This is the `event_hash` — the content-addressable identity of the payload.
5. JSON is parsed to extract `merchant_id`, `source_event_id`, and `event_type`. If JSON parse fails, the event is still accepted with `parse_failed=true`.
6. For order events (`order.created`, `order.updated`), the Square Orders API is called synchronously to fetch full line-item data (the enricher in `enrichers/square.py`). This converts notification-only webhooks into complete payloads.
7. Tier 1 stateless Chirp rules are evaluated against the parsed payload in-process with no database access.
8. Idempotency is checked via a Valkey dedup key (`dedup:<source>:<source_event_id>` in DB 3, TTL 24h). Duplicates return `200 OK` without re-publishing.
9. A ULID `event_id` is assigned.
10. The event is published to `canary:events` via `XADD` with 9 fields (the TSP-01 Queue Message Schema).
11. An `ingestion_log` row is written to PostgreSQL.
12. `200 OK` is returned to Square with the `event_id`.

**Phase 2 — Sub 1: Hash & Seal (async, target <T+15ms)**

1. `XREADGROUP sub1-seal` reads from `canary:events` one message at a time (`BATCH_SIZE=1` is mandated for chain integrity).
2. `event_hash` is re-verified: `SHA-256(raw_payload)` must match the queue field. Hash mismatch triggers a dead-letter write and ACK (poison message cleared).
3. A PostgreSQL advisory lock is acquired per `merchant_id` (`pg_advisory_xact_lock(hashtext(merchant_id))`) to serialize chain hash computation within a merchant.
4. The previous `chain_hash` for this merchant is read from `evidence_records` (latest row by `id DESC`).
5. `chain_hash = SHA-256(previous_chain_hash || event_hash)`. For the genesis record, `previous_chain_hash` is `NULL` and the computation uses only `event_hash`.
6. An `EvidenceRecord` row is inserted: write-once, no updates, no deletes.
7. `XACK` is sent. On DB failure, the message is not ACK'd and will be redelivered.

**Phase 3 — Sub 2: Parse & Route (async)**

1. `XREADGROUP sub2-parse` reads from `canary:events`.
2. `raw_payload` is JSON-parsed. If `parse_failed=true`, the message is ACK'd without CRDM writes.
3. The `event_type` is resolved through the `webhook_dispatch` registry to a route that specifies a parser function, target model class, and optional `detection_type`.
4. The parser function creates one or more CRDM model instances and writes them to `canary_sales`.
5. `ingestion_log.status` is updated to `'parsed'`.
6. If the route has a `detection_type`, a message is published to `canary:detection` via `publish_detection_event()`.
7. `XACK` is sent.

**Phase 4 — Sub 3: Merkle Batch (async, batched)**

1. `XREADGROUP sub3-merkle` reads from `canary:events`.
2. `event_hash` and `event_id` are extracted and added to a Valkey sorted set accumulator (`canary:batch:current`, scored by timestamp).
3. The message is NOT ACK'd during accumulation — messages remain in the Pending Entry List (PEL).
4. When the batch reaches `BATCH_COUNT_THRESHOLD` (default 100 events) or `BATCH_TIME_THRESHOLD_SECONDS` (default 600s), the batch is flushed:
   - All hashes are read from the accumulator, sorted hex-ascending, padded to the next power of 2, and a Merkle tree is built.
   - An `InscriptionPool` row and one `EventInscription` row per event are written in a single PostgreSQL transaction.
   - All pending message IDs are bulk-ACK'd.
   - The accumulator sorted set is deleted.
   - Mock inscription data is written (Sprint 6; real OrdinalsBot integration requires spend gate approval).

**Phase 5 — Sub 4: Detection (async, separate stream)**

1. `XREADGROUP detection-engine` reads from `canary:detection`.
2. `detection_type` routes to the appropriate `ChirpRuleEngine` evaluate method: `evaluate_readonly` (transaction), `evaluate_cash_drawer`, `evaluate_gift_card_activity`, `evaluate_loyalty_event`, `evaluate_dispute`, `evaluate_invoice`.
3. The rule engine queries `canary_sales` for the CRDM record.
4. Resulting alerts are written to `canary_app.alerts` via `write_alerts_to_session()`.
5. `XACK` is sent.

### Key Design Decisions

**Hash-before-parse ordering.** The SHA-256 hash is computed from the raw request bytes before any JSON decoding. This ensures the hash reflects exactly what Square sent, not a re-serialized interpretation. This ordering is patent-critical (FIG. 2 T+0ms).

**Advisory lock for chain integrity.** Sub 1 acquires a per-merchant advisory lock before reading the previous `chain_hash`. This prevents two concurrent Sub 1 workers from computing the same chain position, which would break the evidence chain. `BATCH_SIZE=1` is enforced in code as an additional guard.

**Independent consumer groups.** Each consumer group maintains its own delivery cursor and ACK state. A crash in Sub 3 does not affect Sub 1 or Sub 2 delivery.

**Separate detection stream.** Sub 4 reads from `canary:detection`, not `canary:events`. Sub 2 publishes to `canary:detection` only after a successful CRDM write. This guarantees that Chirp evaluation runs on persisted, queryable records — not raw webhook bytes.

**Valkey stream DB isolation.** The TSP uses Valkey DB 4 for streams, separate from the application cache (DB 0 for Canary). The stream client is configured with `socket_timeout=30` to exceed the 5-second `XREADGROUP block_ms` without spurious timeouts.

**Dedup at two layers.** A Valkey key in DB 3 (`dedup:<source>:<source_event_id>`, TTL 24h) provides fast duplicate rejection. The `uq_ingestion_source_event` unique constraint on `ingestion_log` is the backstop for cache misses.

**Stateless Chirp (Tier 1) in the gateway.** Some Chirp rules fire directly from the webhook payload without any database access. These are evaluated synchronously in the gateway handler before the event is queued. They are additive — a failure in stateless Chirp evaluation does not prevent the webhook from being accepted.

**Order enrichment.** Square order webhooks are notification-only: they contain `{order_id, state, version}` but no line items or tenders. The `enrichers/square.py` module fetches the full order from the Square Orders API synchronously before publishing. This ensures Sub 2 receives complete data.

---

## 3. Data Model

All models use SQLAlchemy 2.0 `Mapped[]` syntax. All tables are in the `canary` database. The TSP pipeline writes to the `canary_sales` schema (`SalesBase`).

### 3.1 Ingestion Layer

#### IngestionLog (`ingestion_log`)

Per-event ingestion status log. Every accepted webhook writes a row here. Status tracks receipt → parsed → complete / failed.

```python
class IngestionLog(SalesBase):
    __tablename__ = "ingestion_log"

    id: Mapped[str]                     # UUID primary key
    merchant_id: Mapped[str]            # Tenant identifier
    source: Mapped[str]                 # WEBHOOK|POLLING|BATCH
    event_id: Mapped[str]               # ULID from TSP-01 gateway
    source_event_id: Mapped[Optional[str]]  # Square's event_id
    event_type: Mapped[str]             # payment.created, etc.
    received_at: Mapped[datetime]       # Gateway receipt timestamp
    processed_at: Mapped[Optional[datetime]]
    status: Mapped[str]                 # received|processing|complete|failed|parsed
    error_message: Mapped[Optional[str]]
    event_hash: Mapped[Optional[bytes]] # SHA-256 of raw payload (BYTEA)
    ip_address: Mapped[Optional[str]]   # Source IP for audit
    user_agent: Mapped[Optional[str]]   # Source User-Agent header
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

Indexes: `(merchant_id, source)`, `(merchant_id, status)`, `(merchant_id, received_at)`, `event_hash`.
Unique constraint: `(source, source_event_id)` — the database-layer dedup backstop.

#### DeadLetterQueue (`dead_letter_queue`)

Unprocessable events held for retry or manual intervention. Written by Sub 1 when payload validation fails (hash mismatch, missing required fields). Also written when a consumer fails after exhausting in-process retries.

```python
class DeadLetterQueue(SalesBase):
    __tablename__ = "dead_letter_queue"

    id: Mapped[str]                     # UUID primary key
    merchant_id: Mapped[str]
    source: Mapped[str]                 # WEBHOOK|POLLING|BATCH
    event_id: Mapped[str]               # ULID
    event_type: Mapped[str]
    payload: Mapped[str]                # Full event payload (Text) for replay
    error_message: Mapped[str]          # Failure reason
    failed_at: Mapped[datetime]
    retry_count: Mapped[int]            # Number of retry attempts
    next_retry_at: Mapped[Optional[datetime]]  # Exponential backoff schedule
    resolved_at: Mapped[Optional[datetime]]    # NULL = unresolved
```

Retry schedule (SDD-040): attempt 0 → 5s delay, attempt 1 → 30s delay, attempt 2 → 5 min delay. Max 3 retries. After exhaustion, `resolved_at` is set and `error_message` is appended with "max retries exceeded".

#### ETLBatch (`etl_batches`)

Batch ingestion progress tracking for multi-event sync jobs (payment sync, customer sync, etc.). Links multiple `IngestionLog` records to a single batch execution.

```python
class ETLBatch(SalesBase):
    __tablename__ = "etl_batches"

    id: Mapped[str]
    batch_type: Mapped[str]             # PAYMENT_SYNC|CUSTOMER_SYNC|INVENTORY_SYNC|etc.
    started_at: Mapped[datetime]
    completed_at: Mapped[Optional[datetime]]
    records_processed: Mapped[int]
    records_failed: Mapped[int]
    status: Mapped[str]                 # started|processing|completed|failed
```

### 3.2 Evidence Layer

#### EvidenceRecord (`evidence_records`)

Write-once immutable evidence store. Sub 1 inserts exactly one row per webhook event. The table has database-level INSERT-only triggers — no UPDATE or DELETE is possible. Chain hash links each record to its predecessor within a merchant's evidence sequence.

The primary key is a `BIGSERIAL` (auto-incrementing integer), not a UUID. The sequential integer defines chain ordering within a merchant's evidence sequence.

```python
class EvidenceRecord(SalesBase):
    __tablename__ = "evidence_records"

    id: Mapped[int]                     # BIGSERIAL — chain ordinal within merchant
    event_id: Mapped[str]               # ULID from TSP-01 (unique across all merchants)
    merchant_id: Mapped[str]            # Merchant partition key
    source: Mapped[str]                 # e.g., 'square'
    source_event_id: Mapped[str]        # Source network's event ID
    event_type: Mapped[str]             # e.g., 'payment.created'
    event_hash: Mapped[bytes]           # SHA-256 of raw_payload (BYTEA, 32 bytes)
    chain_hash: Mapped[bytes]           # SHA-256(prev_chain_hash || event_hash)
    previous_chain_hash: Mapped[Optional[bytes]]  # NULL for genesis record
    raw_payload: Mapped[str]            # Verbatim payload as UTF-8 (TEXT)
    parsed_payload: Mapped[Optional[dict]]  # JSONB; NULL when parse_failed=True
    parse_failed: Mapped[bool]          # True if TSP-01 could not parse JSON
    received_at: Mapped[datetime]       # Timestamp from gateway
    sealed_at: Mapped[datetime]         # server_default=now() — Sub 1 seal time
```

Unique constraint: `(merchant_id, source_event_id)` — prevents duplicate seals.
Indexes: `(merchant_id, received_at)`, `event_hash`, `(merchant_id, id)`, `(source, source_event_id)`.

### 3.3 Inscription Layer

#### InscriptionPool (`inscription_pool`)

One row per Merkle tree batch. Created by Sub 3 when a batch is flushed. Updated with Bitcoin inscription data after submission and confirmation (mock in Sprint 6).

```python
class InscriptionPool(SalesBase):
    __tablename__ = "inscription_pool"

    id: Mapped[int]                     # BIGSERIAL
    batch_id: Mapped[str]               # ULID — unique batch identifier
    merkle_root: Mapped[bytes]          # SHA-256 Merkle root (32 bytes, BYTEA)
    batch_event_count: Mapped[int]      # Original event count before padding
    padded_leaf_count: Mapped[int]      # Leaf count after padding to power of 2
    tree_depth: Mapped[int]             # Balanced tree depth
    tree_algorithm_version: Mapped[int] # 1 = current algorithm
    inscription_id: Mapped[Optional[str]]     # OrdinalsBot inscription ID
    bitcoin_txid: Mapped[Optional[str]]       # Bitcoin transaction ID
    bitcoin_block: Mapped[Optional[int]]      # Block number of confirmation
    block_explorer_url: Mapped[Optional[str]] # Public verification URL
    fee_sats: Mapped[Optional[int]]           # Inscription fee in satoshis
    payment_txid: Mapped[Optional[str]]       # Payment transaction ID
    status: Mapped[str]                 # pending|tree_built|submitted|confirmed|verified
    batch_started_at: Mapped[datetime]
    batch_completed_at: Mapped[Optional[datetime]]
    inscription_submitted_at: Mapped[Optional[datetime]]
    inscription_confirmed_at: Mapped[Optional[datetime]]
    created_at: Mapped[datetime]
```

Indexes: `status`, `bitcoin_block`.

#### EventInscription (`event_inscriptions`)

Maps each individual event to its Merkle batch. Contains the Merkle proof path for independent verification of inclusion without needing the full tree.

```python
class EventInscription(SalesBase):
    __tablename__ = "event_inscriptions"

    id: Mapped[int]                     # BIGSERIAL
    event_hash: Mapped[bytes]           # SHA-256 of event (BYTEA, unique)
    event_id: Mapped[str]               # ULID from TSP-01
    merchant_id: Mapped[str]
    batch_id: Mapped[str]               # References inscription_pool.batch_id
    leaf_index: Mapped[int]             # Position in sorted leaf array
    merkle_proof_path: Mapped[dict]     # JSONB: {siblings, root, leaf_hash, tree_depth}
    created_at: Mapped[datetime]
```

Indexes: `batch_id`, `(merchant_id, created_at)`, `event_id`.

### 3.4 CRDM Sales Tables

These tables are the structured domain records written by Sub 2. They are the input to Chirp rule evaluation.

#### Transaction (`transactions`)

Core transactional record. Every Square payment, refund, void, no-sale, paid-in/out, and exchange logs a transaction row. Append-only.

```python
class Transaction(SalesBase):
    __tablename__ = "transactions"

    id: Mapped[str]                     # UUID primary key (Canonical UUID — GRO-237)
    merchant_id: Mapped[str]            # Internal UUID from app.merchants.id
    external_id: Mapped[str]            # Square payment_id or refund_id
    order_id: Mapped[Optional[str]]     # Square order_id
    receipt_number: Mapped[Optional[str]]
    source_type: Mapped[str]            # WEBHOOK|POLLING|BATCH
    location_id: Mapped[str]            # Square location_id
    employee_id: Mapped[Optional[str]]  # Square team_member_id
    customer_id: Mapped[Optional[str]]
    device_id: Mapped[Optional[str]]
    transaction_type: Mapped[str]       # SALE|RETURN|VOID|POST_VOID|NO_SALE|PAID_IN|PAID_OUT|EXCHANGE
    cancel_context: Mapped[Optional[str]]  # IMMEDIATE_VOID|MANAGER_VOID|EXPIRED_HOLD|TIMEOUT_VOID|UNKNOWN
    transaction_date: Mapped[datetime]
    amount_cents: Mapped[int]
    tax_amount_cents: Mapped[int]
    discount_amount_cents: Mapped[int]
    tip_amount_cents: Mapped[int]
    currency: Mapped[str]               # ISO 4217, default USD
    card_fingerprint: Mapped[Optional[str]]
    card_brand: Mapped[Optional[str]]   # VISA|MASTERCARD|AMEX|DISCOVER|etc.
    card_last4: Mapped[Optional[str]]
    card_prepaid_type: Mapped[Optional[str]]  # PREPAID|DEBIT|CREDIT|UNKNOWN
    cvv_status: Mapped[Optional[str]]
    avs_status: Mapped[Optional[str]]
    entry_method: Mapped[Optional[str]] # CHIP|CONTACTLESS|KEYED|SWIPED|MANUAL
    square_product: Mapped[Optional[str]]  # POS|INVOICES|ONLINE_STORE|VIRTUAL_TERMINAL
    risk_level: Mapped[Optional[str]]   # low|medium|high (Square fraud score)
    approved_amount_cents: Mapped[Optional[int]]
    processing_fee_cents: Mapped[Optional[int]]
    app_fee_cents: Mapped[Optional[int]]
    delay_action: Mapped[Optional[str]] # CANCEL|COMPLETE
    delay_duration: Mapped[Optional[str]]  # ISO 8601 duration (e.g. 'PT36H')
    delayed_until: Mapped[Optional[str]]
    card_type: Mapped[Optional[str]]    # DEBIT|CREDIT|NON_GIFT_CARD|UNKNOWN
    card_bin: Mapped[Optional[str]]     # First 6 digits (issuer BIN)
    card_exp_month: Mapped[Optional[int]]
    card_exp_year: Mapped[Optional[int]]
    verification_method: Mapped[Optional[str]]  # PIN|SIGNATURE|ON_DEVICE|NONE
    application_id: Mapped[Optional[str]]
    device_installation_id: Mapped[Optional[str]]
    statement_description: Mapped[Optional[str]]
    is_offline_payment: Mapped[Optional[bool]]
    payload: Mapped[Optional[str]]      # Full JSON webhook payload (forensic)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

Unique constraint: `(merchant_id, external_id)`.

#### RefundLink (`refund_links`)

Cross-reference between a refund transaction and its original payment. Enables Chirp to track refund-to-payment chains.

```python
class RefundLink(SalesBase):
    __tablename__ = "refund_links"

    id: Mapped[str]
    merchant_id: Mapped[str]
    refund_external_id: Mapped[str]     # Square refund_id
    original_external_id: Mapped[str]  # Square payment_id
    refund_amount_cents: Mapped[int]
    reason: Mapped[Optional[str]]
    employee_id: Mapped[Optional[str]]
    location_id: Mapped[Optional[str]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### TransactionLineItem (`transaction_line_items`)

Product-level breakdown for each transaction. Enables per-SKU LP analysis: return rates, discount patterns, category shrinkage. FK to `transactions.id`.

```python
class TransactionLineItem(SalesBase):
    __tablename__ = "transaction_line_items"

    id: Mapped[str]
    merchant_id: Mapped[str]
    transaction_id: Mapped[str]         # FK → transactions.id
    catalog_object_id: Mapped[Optional[str]]
    item_name: Mapped[Optional[str]]
    variation_name: Mapped[Optional[str]]
    category_name: Mapped[Optional[str]]
    quantity: Mapped[Decimal]           # Numeric(10, 4) — supports weight/measure
    base_price_cents: Mapped[int]
    gross_sales_cents: Mapped[int]
    total_discount_cents: Mapped[int]
    total_tax_cents: Mapped[int]
    item_type: Mapped[str]              # ITEM|CUSTOM_AMOUNT|GIFT_CARD
    is_voided: Mapped[bool]
    return_reason: Mapped[Optional[str]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### TransactionTender (`transaction_tenders`)

Payment method detail per transaction. A single transaction may have multiple tenders (split payment). FK to `transactions.id`.

```python
class TransactionTender(SalesBase):
    __tablename__ = "transaction_tenders"

    id: Mapped[str]
    merchant_id: Mapped[str]
    transaction_id: Mapped[str]         # FK → transactions.id
    payment_id: Mapped[Optional[str]]   # Square payment_id
    tender_type: Mapped[str]            # CARD|CASH|SQUARE_GIFT_CARD|OTHER|NO_SALE
    amount_cents: Mapped[int]
    card_brand: Mapped[Optional[str]]
    card_last4: Mapped[Optional[str]]
    entry_method: Mapped[Optional[str]]
    team_member_id: Mapped[Optional[str]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### LineItemDiscount (`line_item_discounts`)

Discount applied to an order or line item. Captures the full `OrderLineItemDiscount` object from Square. FK to `transactions.id`. Feeds Chirp C-201 (excessive discount) and C-203 (sweethearting).

```python
class LineItemDiscount(SalesBase):
    __tablename__ = "line_item_discounts"

    id: Mapped[str]
    merchant_id: Mapped[str]
    transaction_id: Mapped[str]         # FK → transactions.id
    discount_uid: Mapped[Optional[str]]
    catalog_discount_id: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    discount_type: Mapped[Optional[str]]  # FIXED_PERCENTAGE|FIXED_AMOUNT|VARIABLE_PERCENTAGE|VARIABLE_AMOUNT
    percentage: Mapped[Optional[str]]
    amount_cents: Mapped[Optional[int]]
    applied_cents: Mapped[Optional[int]]
    scope: Mapped[Optional[str]]        # ORDER|LINE_ITEM
    reward_ids: Mapped[Optional[str]]   # JSON array of loyalty reward IDs
    pricing_rule_id: Mapped[Optional[str]]
    created_at: Mapped[datetime]
```

#### OrderServiceCharge (`order_service_charges`)

Service charge (e.g., auto-gratuity) applied to an order. FK to `transactions.id`. Enables detection of unexpected charges and gratuity manipulation.

```python
class OrderServiceCharge(SalesBase):
    __tablename__ = "order_service_charges"

    id: Mapped[str]
    merchant_id: Mapped[str]
    transaction_id: Mapped[str]         # FK → transactions.id
    charge_uid: Mapped[Optional[str]]
    catalog_charge_id: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    percentage: Mapped[Optional[str]]
    amount_cents: Mapped[Optional[int]]
    applied_cents: Mapped[Optional[int]]
    total_tax_cents: Mapped[Optional[int]]
    calculation_phase: Mapped[Optional[str]]
    taxable: Mapped[Optional[bool]]
    charge_type: Mapped[Optional[str]]  # AUTO_GRATUITY|CUSTOM
    treatment_type: Mapped[Optional[str]]
    scope: Mapped[Optional[str]]        # ORDER|LINE_ITEM
    created_at: Mapped[datetime]
```

#### OrderReturn (`order_returns`)

Return associated with an order. Captures the full `OrderReturn` object including return line items, amount, tax, discount, and tip components. FK to `transactions.id`.

```python
class OrderReturn(SalesBase):
    __tablename__ = "order_returns"

    id: Mapped[str]
    merchant_id: Mapped[str]
    transaction_id: Mapped[str]         # FK → transactions.id
    return_uid: Mapped[Optional[str]]
    source_order_id: Mapped[Optional[str]]   # Original order being returned
    return_line_items: Mapped[Optional[str]] # JSON array of returned line items
    return_amount_cents: Mapped[Optional[int]]
    return_tax_cents: Mapped[Optional[int]]
    return_discount_cents: Mapped[Optional[int]]
    return_tip_cents: Mapped[Optional[int]]
    created_at: Mapped[datetime]
```

#### CashDrawerShift (`cash_drawer_shifts`)

Cash drawer shift opening and closing. Updated when the shift is closed. `cash_variance_cents` is the primary LP metric — the difference between expected and actual cash counted at close. Triggers the `HIGH_CASH_VARIANCE` Chirp rule.

```python
class CashDrawerShift(SalesBase):
    __tablename__ = "cash_drawer_shifts"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_shift_id: Mapped[str]
    location_id: Mapped[str]
    device_id: Mapped[Optional[str]]
    employee_id: Mapped[Optional[str]]
    opened_at: Mapped[datetime]
    closed_at: Mapped[Optional[datetime]]
    starting_cash_cents: Mapped[int]
    expected_cash_cents: Mapped[Optional[int]]
    closed_cash_cents: Mapped[Optional[int]]
    cash_variance_cents: Mapped[Optional[int]]  # Primary LP signal
    state: Mapped[str]                  # OPEN|CLOSED
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]        # Updated on close
```

#### CashDrawerEvent (`cash_drawer_events`)

Individual cash drawer events (no-sale, paid-in, paid-out) within a shift. Append-only. References `cash_drawer_shifts.id` via `shift_id`.

```python
class CashDrawerEvent(SalesBase):
    __tablename__ = "cash_drawer_events"

    id: Mapped[str]
    merchant_id: Mapped[str]
    shift_id: Mapped[str]               # FK to cash_drawer_shifts.id
    event_type: Mapped[str]             # NO_SALE|PAID_IN|PAID_OUT|CASH_TENDER_PAYMENT|CASH_TENDER_CANCELLED_PAYMENT|OTHER
    amount_cents: Mapped[int]
    employee_id: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    event_at: Mapped[datetime]
    created_at: Mapped[datetime]
```

#### GiftCardActivity (`gift_card_activities`)

Gift card activations, loads, redemptions, and refunds. Append-only. Feeds `GIFT_CARD_LOAD_VELOCITY` Chirp rule.

```python
class GiftCardActivity(SalesBase):
    __tablename__ = "gift_card_activities"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_activity_id: Mapped[str]
    gift_card_id: Mapped[str]
    activity_type: Mapped[str]          # ACTIVATE|LOAD|REDEEM|DEACTIVATE|ADJUST|REFUND|CLEAR_BALANCE
    amount_cents: Mapped[int]           # Positive for load, negative for redeem
    balance_after_cents: Mapped[Optional[int]]
    location_id: Mapped[Optional[str]]
    employee_id: Mapped[Optional[str]]
    linked_transaction_id: Mapped[Optional[str]]
    order_id: Mapped[Optional[str]]
    payment_id: Mapped[Optional[str]]
    reference_id: Mapped[Optional[str]]
    redeem_status: Mapped[Optional[str]]  # PENDING|COMPLETED
    buyer_payment_instrument_ids: Mapped[Optional[str]]  # JSON array
    occurred_at: Mapped[datetime]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### LoyaltyAccount (`loyalty_accounts`)

Loyalty program accounts. Operational (updated when balance changes). Feeds Chirp rules C-801 through C-804.

```python
class LoyaltyAccount(SalesBase):
    __tablename__ = "loyalty_accounts"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_loyalty_id: Mapped[str]
    phone_hash: Mapped[Optional[str]]   # SHA-256 of phone number (PII protection)
    points_balance: Mapped[int]
    lifetime_points: Mapped[int]
    enrollment_source: Mapped[Optional[str]]  # TERMINAL|ONLINE|IMPORT
    enrollment_location_id: Mapped[Optional[str]]
    enrolled_by_employee_id: Mapped[Optional[str]]
    enrolled_at: Mapped[datetime]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### LoyaltyEvent (`loyalty_events`)

Loyalty point events (accumulate, redeem, adjust, expire). Append-only. References `loyalty_accounts.id`.

```python
class LoyaltyEvent(SalesBase):
    __tablename__ = "loyalty_events"

    id: Mapped[str]
    merchant_id: Mapped[str]
    loyalty_account_id: Mapped[str]
    square_event_id: Mapped[str]
    event_type: Mapped[str]             # ACCUMULATE|REDEEM|CREATE|ADJUST|EXPIRE|DELETE_REWARD
    points: Mapped[int]                 # Positive for earn, negative for redeem
    location_id: Mapped[Optional[str]]
    employee_id: Mapped[Optional[str]]
    linked_transaction_id: Mapped[Optional[str]]
    order_id: Mapped[Optional[str]]
    source_name: Mapped[Optional[str]]
    reward_id: Mapped[Optional[str]]
    occurred_at: Mapped[datetime]
    created_at: Mapped[datetime]
```

#### Dispute (`disputes`)

Payment disputes (chargebacks). Append-only. Maps from Square Disputes API webhook events.

```python
class Dispute(SalesBase):
    __tablename__ = "disputes"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_dispute_id: Mapped[str]
    payment_id: Mapped[Optional[str]]
    order_id: Mapped[Optional[str]]
    location_id: Mapped[Optional[str]]
    reason: Mapped[Optional[str]]       # AMOUNT_DIFFERS|CANCELLED|DUPLICATE|NO_KNOWLEDGE|etc.
    state: Mapped[str]                  # INQUIRY_EVIDENCE_REQUIRED|INQUIRY_PROCESSING|INQUIRY_CLOSED|
                                        # EVIDENCE_REQUIRED|PROCESSING|WON|LOST|ACCEPTED
    amount_cents: Mapped[int]
    currency: Mapped[str]
    due_at: Mapped[Optional[datetime]]
    reported_at: Mapped[Optional[datetime]]
    created_at: Mapped[datetime]
```

#### Invoice (`invoices`)

Square invoices. Append-only. Maps from Square Invoices API webhook events.

```python
class Invoice(SalesBase):
    __tablename__ = "invoices"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_invoice_id: Mapped[str]
    order_id: Mapped[str]
    location_id: Mapped[Optional[str]]
    creator_team_member_id: Mapped[Optional[str]]
    subscription_id: Mapped[Optional[str]]
    invoice_number: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    invoice_status: Mapped[Optional[str]]  # DRAFT|UNPAID|SCHEDULED|PARTIALLY_PAID|PAID|
                                           # PARTIALLY_REFUNDED|REFUNDED|CANCELED|FAILED|PAYMENT_PENDING
    version: Mapped[Optional[int]]
    timezone: Mapped[Optional[str]]
    delivery_method: Mapped[Optional[str]]  # EMAIL|SMS|SHARE_MANUALLY
    scheduled_at: Mapped[Optional[datetime]]
    public_url: Mapped[Optional[str]]
    next_payment_amount_cents: Mapped[Optional[int]]
    currency: Mapped[str]
    sale_or_service_date: Mapped[Optional[str]]  # YYYY-MM-DD
    store_payment_method_enabled: Mapped[Optional[bool]]
    primary_recipient: Mapped[Optional[dict]]     # JSONB
    payment_requests: Mapped[Optional[list]]      # JSONB
    accepted_payment_methods: Mapped[Optional[dict]]  # JSONB
    custom_fields: Mapped[Optional[list]]         # JSONB
    attachments: Mapped[Optional[list]]           # JSONB
    raw_square_object: Mapped[Optional[dict]]     # JSONB — complete API response
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### Payout (`payouts`)

Merchant payouts from Square to bank account. Append-only. Maps from Square Payouts API webhook events.

```python
class Payout(SalesBase):
    __tablename__ = "payouts"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_payout_id: Mapped[str]
    location_id: Mapped[Optional[str]]
    status: Mapped[str]                 # SENT|PAID|FAILED
    amount_cents: Mapped[int]
    currency: Mapped[str]
    destination_type: Mapped[Optional[str]]  # BANK_ACCOUNT|CARD
    arrival_date: Mapped[Optional[datetime]]
    failure_reason: Mapped[Optional[str]]
    created_at: Mapped[datetime]
```

#### InventoryAdjustment (`inventory_adjustments`)

Inventory count adjustments. Append-only. Feeds the `INVENTORY_SHRINKAGE_SPIKE` Chirp rule.

```python
class InventoryAdjustment(SalesBase):
    __tablename__ = "inventory_adjustments"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_adjustment_id: Mapped[str]
    catalog_object_id: Mapped[str]      # Square catalog SKU
    location_id: Mapped[str]
    adjustment_type: Mapped[str]        # SHRINKAGE|RECEIPT|SALE|MANUAL|TRANSFER_IN|TRANSFER_OUT
    quantity_change: Mapped[Decimal]    # Numeric(10, 4); positive or negative
    team_member_id: Mapped[Optional[str]]
    reason: Mapped[Optional[str]]
    occurred_at: Mapped[datetime]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### EmployeeTimecard (`employee_timecards`)

Employee shift clock-in / clock-out records. Operational (updated during shift). Used for `OFF_CLOCK_TRANSACTION` Chirp detection.

```python
class EmployeeTimecard(SalesBase):
    __tablename__ = "employee_timecards"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_timecard_id: Mapped[str]
    employee_id: Mapped[str]
    location_id: Mapped[str]
    start_at: Mapped[datetime]          # Clock-in timestamp
    end_at: Mapped[Optional[datetime]]  # Clock-out timestamp
    breaks: Mapped[Optional[str]]       # JSON array of {start, end} pairs
    status: Mapped[str]                 # OPEN|CLOSED
    hourly_rate_cents: Mapped[Optional[int]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]        # Updated on clock-out
```

#### Device (`devices`)

POS terminal and device metadata. Operational (updated on status change). Used for device fingerprinting, offline payment detection, and correlating transactions to physical terminals.

```python
class Device(SalesBase):
    __tablename__ = "devices"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_device_id: Mapped[str]
    location_id: Mapped[Optional[str]]
    serial_number: Mapped[Optional[str]]
    device_name: Mapped[Optional[str]]
    os_version: Mapped[Optional[str]]
    app_version: Mapped[Optional[str]]
    payment_region: Mapped[Optional[str]]
    network_connection_type: Mapped[Optional[str]]  # WIFI|ETHERNET
    wifi_network_name: Mapped[Optional[str]]
    wifi_network_strength: Mapped[Optional[str]]    # POOR|FAIR|GOOD|EXCELLENT
    ip_address: Mapped[Optional[str]]
    battery_percentage: Mapped[Optional[str]]
    charging_state: Mapped[Optional[str]]           # CHARGING|NOT_CHARGING
    raw_square_object: Mapped[Optional[dict]]       # JSONB — complete API response
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### TerminalCheckout (`terminal_checkouts`)

Square Terminal checkout sessions (in-person POS flow). Append-only. LP signals: canceled checkout followed by cash tender, correlation with disputed payments.

```python
class TerminalCheckout(SalesBase):
    __tablename__ = "terminal_checkouts"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_checkout_id: Mapped[str]     # tmco_... ID
    order_id: Mapped[Optional[str]]
    location_id: Mapped[Optional[str]]
    device_id: Mapped[Optional[str]]
    reference_id: Mapped[Optional[str]]
    note: Mapped[Optional[str]]
    amount_cents: Mapped[int]
    currency: Mapped[str]
    status: Mapped[Optional[str]]       # PENDING|IN_PROGRESS|CANCEL_REQUESTED|CANCELED|COMPLETED
    cancel_reason: Mapped[Optional[str]]
    payment_ids: Mapped[Optional[str]]  # JSON array of linked payment IDs
    deadline_duration: Mapped[Optional[str]]  # ISO 8601 (e.g. PT5M)
    app_id: Mapped[Optional[str]]
    square_created_at: Mapped[Optional[datetime]]
    square_updated_at: Mapped[Optional[datetime]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

#### TerminalRefund (`terminal_refunds`)

Square Terminal refund sessions (in-person refund flow). Append-only. LP signals: terminal refund without POS receipt, multiple refunds on same payment.

```python
class TerminalRefund(SalesBase):
    __tablename__ = "terminal_refunds"

    id: Mapped[str]
    merchant_id: Mapped[str]
    square_refund_id: Mapped[str]       # tmrf_... ID
    refund_id: Mapped[Optional[str]]    # Linked Square refund ID
    payment_id: Mapped[Optional[str]]
    order_id: Mapped[Optional[str]]
    location_id: Mapped[Optional[str]]
    device_id: Mapped[Optional[str]]
    amount_cents: Mapped[int]
    currency: Mapped[str]
    reason: Mapped[Optional[str]]
    status: Mapped[Optional[str]]       # PENDING|IN_PROGRESS|CANCEL_REQUESTED|CANCELED|COMPLETED
    cancel_reason: Mapped[Optional[str]]
    deadline_duration: Mapped[Optional[str]]
    square_created_at: Mapped[Optional[datetime]]
    square_updated_at: Mapped[Optional[datetime]]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

---

## 4. Interfaces

### 4.1 Webhook Endpoints (`webhooks_tsp_bp` — registered at `/webhooks`)

**`POST /webhooks/<source>`**

Universal webhook entry point. `source` must be in `REGISTERED_SOURCES` (currently only `"square"`). Validates HMAC, hashes, parses, enriches, and publishes.

Request: raw webhook body (Square JSON format).
Headers: `X-Square-Hmacsha256-Signature` (required for Square source).
Response `200`: `{"status": "accepted", "event_id": "<ulid>", "received_at": "<iso8601>"}`.
Response `200` (duplicate): `{"status": "accepted", "event_id": "duplicate:<source_event_id>", "duplicate": true}`.
Response `401`: HMAC validation failed.
Response `404`: Unknown source.
Response `413`: Payload exceeds `MAX_PAYLOAD_BYTES` (default 1 MB).
Response `503`: Valkey unavailable — caller should retry with backoff.

**`GET /webhooks/health`**

Health check. Returns `200` if Valkey stream is reachable, `503` otherwise.
Response: `{"status": "healthy"|"degraded", "queue_connected": bool, "version": "1.0.0"}`.

**`GET /webhooks/ready`**

Readiness probe. Checks Valkey connectivity, `SQUARE_WEBHOOK_SIGNATURE_KEY`, and `SQUARE_NOTIFICATION_URL`.
Response `200`: `{"status": "ready"}`.
Response `503`: `{"status": "not_ready", "errors": ["queue: ...", "signature_key: ..."]}`.

**`GET /webhooks/live`**

Liveness probe — always returns `200`.
Response: `{"status": "alive"}`.

### 4.2 Receipt Endpoints (`receipt_tsp_bp` — registered at `/receipt`)

Read-only query interface for evidence receipts. Returns sealed evidence plus inscription proof for any event.

**`GET /receipt/by-hash/<event_hash_hex>`**

Lookup by 64-character hex SHA-256 hash. Returns `404` if not found.

**`GET /receipt/by-event/<event_id>`**

Lookup by ULID event_id.

**Receipt response fields:**

```json
{
    "status": "verified|verified_pending_inscription|verified_inscription_pending",
    "verified": true,
    "event_hash": "<64-char hex>",
    "event_id": "<ulid>",
    "merchant_id": "<uuid>",
    "source": "square",
    "event_type": "payment.created",
    "chain_hash": "<64-char hex>",
    "chain_position": <int>,
    "previous_chain_hash": "<64-char hex>|null",
    "parse_failed": false,
    "received_at": "<iso8601>",
    "sealed_at": "<iso8601>",
    "inscription": {
        "batch_id": "<ulid>",
        "inscription_id": "<ordinal_id>",
        "bitcoin_txid": "<txid>",
        "bitcoin_block": <int>,
        "block_explorer_url": "<url>",
        "status": "confirmed",
        "batch_event_count": <int>,
        "leaf_index": <int>,
        "merkle_proof": {...},
        "merkle_root": "<64-char hex>"
    }
}
```

`inscription` is `null` if the event has not yet been included in a Merkle batch.

**`GET /receipt/health`**

Health check. Returns `{"status": "healthy", "service": "receipt-tsp"}`.

### 4.3 MCP Tools (`tsp_mcp_bp` — registered at `/tsp`)

The TSP MCP server (`canary-tsp`, v0.1.0) exposes 7 tools via the Canary MCP blueprint framework. All tools are accessible through the standard MCP request/response format.

**`get_stream_health`** (category: health)
Returns stream length, consumer groups, pending message counts, and dead letter count for `canary:events` and `canary:detection`. No parameters.

**`get_dead_letters`** (category: health)
Lists failed events from the `canary:dead_letter` stream. Parameter: `limit` (int, default 20, max 100). Returns stream_id, event_id, merchant_id, event_type, reason, and original stream/group information.

**`replay_event`** (category: management)
Replays a dead-letter entry back to `canary:events`. Strips dead-letter metadata, re-publishes, and deletes the original. Parameter: `stream_id` (string, required). Write operation.

**`get_ingestion_stats`** (category: analytics)
Returns ingestion throughput, status breakdown, event type counts, processing latency (avg/max/min), and error rate from `ingestion_log`. Parameters: `merchant_id` (string, optional), `hours` (int, default 24, max 168).

**`get_receipt`** (category: evidence)
Retrieves a sealed evidence receipt with chain hash and inscription proof. Equivalent to the HTTP receipt endpoint. Parameters: `event_hash` (string) or `event_id` (string); one is required.

**`verify_merkle`** (category: evidence)
Verifies a Merkle proof for an event. Can look up the proof from the database or verify an inline proof. Parameter: `event_hash` (string, required), `proof` (object, optional), `expected_root` (string, optional).

**`process_dead_letters`** (category: management)
Processes eligible DLQ entries with exponential backoff (SDD-040 schedule). Parameter: `batch_size` (int, default 10, max 50).

### 4.4 Consumer Groups

The four consumer groups read from two Valkey streams and are each run as a separate Docker Compose service using the same Flask image with a different `--consumer` argument.

| Group | Stream | Consumer module | Key |
|---|---|---|---|
| `sub1-seal` | `canary:events` | `sub1_seal.run_consumer` | `--consumer sub1` |
| `sub2-parse` | `canary:events` | `sub2_parse.run_consumer` | `--consumer sub2` |
| `sub3-merkle` | `canary:events` | `sub3_merkle.run_consumer` | `--consumer sub3` |
| `detection-engine` | `canary:detection` | `sub4_detect.run_consumer` | `--consumer sub4` |

Each consumer creates a minimal Flask app (database config only, no blueprints) via `create_consumer_app()` in `run_consumer.py`. Consumers are started with:

```
python -m canary.services.tsp.run_consumer --consumer <sub1|sub2|sub3|sub4>
```

---

## 5. Service Layer

### `stream_publisher.py`

Singleton Valkey client (DB 4) with 30-second socket timeout and 5-second connection timeout. Exports:

- `get_stream_client()` — lazy-initialized Valkey client for stream DB.
- `init_consumer_groups()` — creates all four consumer groups on `canary:events` and `canary:detection` at startup. Safe to call multiple times (catches `BUSYGROUP`).
- `publish_event(...)` — `XADD` to `canary:events` with the 9-field TSP-01 Queue Message Schema.
- `publish_detection_event(...)` — `XADD` to `canary:detection` with `{transaction_id, merchant_id, event_type, event_id, detection_type}`.

### `validators/square.py`

Square-specific HMAC-SHA256 signature validation.

- `validate_signature(raw_body, signature_header)` — computes `Base64(HMAC-SHA256(notification_url + raw_body, signature_key))` and performs timing-safe comparison via `hmac.compare_digest`.
- `get_signature_key()` — loads `SQUARE_WEBHOOK_SIGNATURE_KEY` from environment; raises `RuntimeError` if not configured.
- `get_notification_url()` — loads `SQUARE_NOTIFICATION_URL` from environment.
- `extract_merchant_id(payload)` — reads `payload["merchant_id"]`.
- `extract_source_event_id(payload)` — reads `payload["event_id"]`.
- `extract_event_type(payload)` — reads `payload["type"]`.

### `enrichers/square.py`

Order webhook enrichment. Square order events (`order.created`, `order.updated`) are notification-only — they contain only `{order_id, state, version}`. The enricher calls the Square Orders API synchronously to fetch the full order with line items and embeds it in the payload.

- `enrich(payload, event_type)` — entry point. Returns `(enriched_payload, was_enriched)`.
- Falls back gracefully if `SQUARE_ACCESS_TOKEN` is not set or the API call fails.

### `merkle.py`

Deterministic Merkle tree construction. Algorithm version 1.

- **Leaf ordering:** sorted by `event_hash` hex ascending (deterministic).
- **Padding:** duplicate-last-leaf to next power of 2.
- **Leaf hashing:** `SHA-256(event_hash)` — double-hashing prevents second-preimage attacks.
- **Internal nodes:** `SHA-256(left_child || right_child)`.
- `build_tree(event_hashes)` — returns `MerkleResult` with root, proof paths, depth, leaf counts.
- `verify_proof(event_hash, proof, expected_root)` — recomputes root from proof path and compares. Returns `bool`.

### `heartbeat.py`

Valkey-based liveness signal. Each consumer writes a Unix timestamp to `canary:heartbeat:<consumer_name>` on every loop iteration with TTL of 120 seconds.

- `write_heartbeat(consumer_name)` — best-effort; swallows errors so a Valkey hiccup does not crash the consumer.
- `check_heartbeat(consumer_name, threshold=60)` — returns `True` if heartbeat exists and is younger than `threshold` seconds.

### `dlq_processor.py`

DLQ retry processor. Processes eligible `DeadLetterQueue` rows in batches and replays them to `canary:events`.

Backoff schedule: `{0: 5s, 1: 30s, 2: 300s}`. After 3 retries, `resolved_at` is set and the entry is considered exhausted.

- `process_dead_letters(batch_size=10)` — queries eligible rows (unresolved, past `next_retry_at`, under max retries), replays each to `canary:events`, increments retry count, and schedules or exhausts. Returns `{processed, replayed, exhausted, errors}`.

### `tools.py`

MCP tool definitions. Registers all 7 TSP MCP tools in the `canary-tsp` registry. Tools are registered via `registry.register(MCPTool(...))`.

---

## 6. Configuration

All configuration is via environment variables. No hardcoded values.

| Variable | Default | Description |
|---|---|---|
| `VALKEY_URL` | `redis://localhost:6379/0` | Base Valkey connection URL. The stream client derives its URL by replacing the DB segment. |
| `VALKEY_STREAM_DB` | `4` | Valkey DB number for `canary:events` and `canary:detection`. Isolated from cache DBs (0-3) to prevent volatile-lru eviction. |
| `VALKEY_STREAM` | `canary:events` | Primary event stream name. |
| `VALKEY_DEAD_LETTER_STREAM` | `canary:dead_letter` | Dead letter stream name. |
| `DETECTION_STREAM` | `canary:detection` | Detection routing stream for Sub 4. |
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | (required) | Per-subscription HMAC key from Square Developer Dashboard. Required for production. |
| `SQUARE_NOTIFICATION_URL` | (required) | The URL Square posts to. Required for HMAC computation. Must match Square's registered endpoint. |
| `SQUARE_ACCESS_TOKEN` | (optional) | Square API access token for order enrichment. If absent, enrichment is skipped. |
| `SQUARE_ENVIRONMENT` | `sandbox` | `sandbox` or `production`. Controls which Square API endpoint is called by the enricher. |
| `MAX_PAYLOAD_BYTES` | `1048576` | Maximum webhook payload size (1 MB). Requests exceeding this return `413`. |
| `DATABASE_URL` | (required) | PostgreSQL connection string for the `canary` database. |
| `CANARY_DB_URL` | falls back to `DATABASE_URL` | Consumer-specific DB URL override. |
| `SUB1_BLOCK_MS` | `5000` | XREADGROUP blocking timeout for Sub 1 (ms). |
| `SUB2_BLOCK_MS` | `5000` | XREADGROUP blocking timeout for Sub 2 (ms). |
| `SUB3_BLOCK_MS` | `2000` | XREADGROUP blocking timeout for Sub 3 (ms). |
| `SUB4_BLOCK_MS` | `5000` | XREADGROUP blocking timeout for Sub 4 (ms). |
| `BATCH_COUNT_THRESHOLD` | `100` | Sub 3: number of events that triggers a Merkle batch flush. |
| `BATCH_TIME_THRESHOLD_SECONDS` | `600` | Sub 3: time elapsed (seconds) that triggers a batch flush regardless of count. |
| `MOCK_INSCRIPTION` | `true` | Sub 3: `true` = use mock OrdinalsBot responses (Sprint 6). Set to `false` when live API keys are available. |

**Socket timeout rule:** The Valkey stream client is configured with `socket_timeout=30` seconds. This must exceed `XREADGROUP block_ms` (max 5000ms) by a safe margin to prevent "Timeout reading from socket" errors during blocking reads.

---

## 7. Security & Compliance

### HMAC-SHA256 Webhook Validation

Every webhook from Square must pass HMAC-SHA256 signature validation before processing. The signature is computed as:

```
expected = Base64(HMAC-SHA256(notification_url + raw_body, signature_key))
```

The comparison uses `hmac.compare_digest` (timing-safe) to prevent timing oracle attacks. Invalid signatures return `401` and the event is not published to the stream. The signature key (`SQUARE_WEBHOOK_SIGNATURE_KEY`) is per-subscription, not per-merchant.

### Hash-Before-Parse Invariant

The SHA-256 hash of raw bytes is computed before JSON parsing. This is a patent-critical ordering invariant (FIG. 2, T+0ms). The hash reflects exactly what Square transmitted, not a re-serialized interpretation.

### Chain Hash Integrity

Each `EvidenceRecord` stores a `chain_hash = SHA-256(previous_chain_hash || event_hash)`. This links records in a tamper-evident sequence per merchant. An advisory lock (`pg_advisory_xact_lock`) ensures no two Sub 1 workers compute the same chain position for the same merchant concurrently.

### Write-Once Evidence Store

`evidence_records` is enforced as INSERT-only at the database layer via triggers. The SQLAlchemy model has no `update()` or `delete()` methods. Tampering with historical records would break the chain hash sequence and be immediately detectable.

### Merkle Proof Integrity

Each event's inclusion in a Bitcoin inscription batch can be verified independently using only its `event_hash`, the `merkle_proof_path` from `event_inscriptions`, and the `merkle_root` from `inscription_pool`. The `verify_proof()` function in `merkle.py` performs this verification without network access.

### Data Isolation

- Webhook dedup keys are stored in Valkey DB 3 (separate from stream DB 4).
- Stream data is in Valkey DB 4, isolated from application cache (DB 0) to prevent eviction.
- Consumer processes create minimal Flask apps with no blueprints, no auth extensions, and no template routes — database config only.

### PII Handling

- `LoyaltyAccount.phone_hash` stores SHA-256 of phone number, never the raw number.
- `EvidenceRecord.raw_payload` stores complete webhook payloads including any customer data. Access is restricted to evidence audit workflows.
- Card data stored in `Transaction` is limited to `card_last4`, `card_brand`, and `card_fingerprint`. No PANs are stored.

---

## 8. Error Handling

### Gateway Error Responses

| Condition | Status | Action |
|---|---|---|
| Unknown source | `404` | Reject — not registered |
| Payload too large | `413` | Reject — over `MAX_PAYLOAD_BYTES` |
| HMAC validation failed | `401` | Reject — do not publish |
| Signature key not configured | `503` | Return 503 with `retry_after_seconds: 30` |
| Valkey XADD fails | `503` | Return 503 — Square will retry |
| JSON parse fails | `200` | Accept with `parse_failed=true` — raw bytes are hashed and published |
| DB write of `ingestion_log` fails | Log error, continue | Stream is source of truth — do not lose the event |

### Sub 1 Error Handling

- **Missing required fields:** Move to dead letter stream, ACK (clear poison message).
- **Hash mismatch (tamper detected):** Move to dead letter stream, ACK.
- **Duplicate event** (`uq_evidence_merchant_event` constraint): ACK — already sealed.
- **DB failure (other):** Do NOT ACK. Message stays in PEL and will be redelivered.
- **Consecutive errors:** Exponential backoff (`min(2^(n-1), 30)` seconds). After 10 consecutive errors, the consumer stops and requires a restart.

### Sub 2 Error Handling

- **`parse_failed=true` messages:** ACK without CRDM writes — cannot parse.
- **Unknown event type:** ACK (log-only event) — no structured parse needed.
- **`IntegrityError`** on CRDM insert: Typically a duplicate. Log and ACK.
- **DB failure (other):** Do NOT ACK. Redelivered.

### Sub 3 Error Handling

- **Malformed message** (missing `event_hash` or `event_id`): ACK and skip.
- **Merkle tree build failure:** Log error, do NOT ACK batch messages — they stay in PEL for redelivery.
- **PostgreSQL commit failure:** Roll back, do NOT ACK. Redelivered.
- **Orphaned accumulator on startup:** Deleted on startup (`client.delete(BATCH_KEY)`). Messages are redelivered from PEL.
- **Shutdown with unACK'd messages:** Logged as warning. Messages remain in PEL and will be redelivered when the consumer restarts.

### Sub 4 Error Handling

- **Missing `transaction_id` or `merchant_id`:** ACK (malformed — don't redeliver).
- **Record not found in CRDM:** ACK — record may have been deleted or not yet committed.
- **Rule engine exception:** Do NOT ACK. Redelivered.
- **Pending recovery on startup:** Sub 4 reads from PEL first (using `id="0"`) before switching to new messages (`id=">"`).

### Dead Letter Stream

Poison messages (hash mismatch, malformed fields) go to `canary:dead_letter` via `_move_to_dead_letter()`. The DLQ processor (`dlq_processor.py`) retries them with exponential backoff (5s, 30s, 5min) against the `dead_letter_queue` database table. After 3 retries, the entry is marked resolved with "max retries exceeded".

The `replay_event` MCP tool enables manual replay of individual dead-letter entries.

### Stream Lag Monitoring

The `get_stream_health` MCP tool reports `pending` message counts per consumer group. High pending counts indicate a consumer is lagging or has stopped. Consumer heartbeats in `canary:heartbeat:<name>` (TTL 120s) provide a secondary signal — a missing or stale heartbeat indicates the process is dead.

---

## 9. Testing

Tests follow the three-layer standard.

**Unit layer** (`tests/unit/`)

- `tests/unit/test_tsp_merkle.py` — Merkle tree construction, proof generation, and `verify_proof()`. Tests deterministic ordering, power-of-2 padding, duplicate-last-leaf behavior, single-event tree, and proof verification for all leaves.
- `tests/unit/test_tsp_validator.py` — HMAC-SHA256 signature validation, timing-safe comparison, merchant/event_type/source_event_id extraction.
- `tests/unit/test_dlq_processor.py` — DLQ backoff schedule calculations, `calculate_next_retry()` at each retry count, exhaustion behavior.

**Integration layer** (`tests/integration/`)

- `tests/integration/test_tsp_pipeline.py` — End-to-end: POST webhook → verify ingestion_log row → verify evidence_records row → verify CRDM row in canary_sales → verify detection message on canary:detection.
- `tests/integration/test_sub1_seal.py` — Chain hash computation, advisory lock behavior, duplicate rejection, dead letter writes.
- `tests/integration/test_sub3_merkle.py` — Batch accumulation, threshold triggers, Merkle tree commit, XACK behavior, mock inscription update.

**Smoke layer** (`tests/smoke/`)

- `tests/smoke/test_tsp_health.py` — `GET /webhooks/health` returns 200 with `queue_connected: true` when Valkey is running.
- `tests/smoke/test_receipt_health.py` — `GET /receipt/health` returns 200.

**Test database:** `canary_test`. Separate from dev. Created/destroyed per test run.

---

## 10. Dependencies

### Upstream

| Dependency | Role |
|---|---|
| Square Webhooks | Event source. Sends webhook POSTs to `/webhooks/square`. |
| Square Orders API | Called synchronously by the enricher for `order.*` events. |
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | Per-subscription HMAC key. Provisioned in Square Developer Dashboard. |
| `SQUARE_NOTIFICATION_URL` | The registered webhook URL. Must match exactly for HMAC computation. |

### Downstream

| Consumer | What it reads | What it writes |
|---|---|---|
| Sub 1 (seal) | `canary:events` | `evidence_records` |
| Sub 2 (parse) | `canary:events` | CRDM tables (`transactions`, `transaction_line_items`, `cash_drawer_shifts`, etc.), `ingestion_log.status` update, `canary:detection` |
| Sub 3 (merkle) | `canary:events` | `inscription_pool`, `event_inscriptions` |
| Sub 4 (detect) | `canary:detection` | `canary_app.alerts` (via Chirp rule engine) |
| Receipt endpoints | `evidence_records`, `event_inscriptions`, `inscription_pool` | read-only |
| MCP tools | `canary:events`, `canary:detection`, `canary:dead_letter`, `ingestion_log`, `evidence_records`, `event_inscriptions` | `canary:events` (replay only), `dead_letter_queue` (process) |

### Shared Infrastructure

| Service | Usage |
|---|---|
| `growdirect_postgres:5432` | `canary` database — all TSP tables live here |
| `growdirect_valkey:6379` | DB 0: Canary app cache; DB 3: webhook dedup; DB 4: TSP streams (`canary:events`, `canary:detection`, `canary:dead_letter`, `canary:batch:current`, `canary:heartbeat:*`) |
| Flask app (`canary-flask`) | Hosts webhook and receipt blueprints; gateway for all inbound events |
| Canary MCP (`canary-tsp` on port 8001) | MCP server hosting the 7 TSP management tools |
| Chirp rule engine | Sub 4 depends on `ChirpRuleEngine` from `canary.services.chirp.rule_engine` |

---

## 11. Known Issues & Reconciliation

### Sprint 6 Scope Constraints

**Mock inscription only.** Sub 3 writes mock Bitcoin inscription data (deterministic fake `inscription_id`, `bitcoin_txid`, `bitcoin_block`). Real OrdinalsBot API integration is Sprint 7+ and requires spend gate approval from Jeffe per Principle 9. No live API keys are held. `MOCK_INSCRIPTION=true` is the default.

**No L402 payment gate on receipts.** The receipt endpoint (`receipt_tsp.py`) returns proof data without requiring a Lightning payment. TSP-07 will wrap the receipt endpoint with an L402 Lightning payment gate. This requires Strike API integration and a separate spend gate approval.

### Architecture Considerations

**Sub 3 XACK timing.** Messages accumulating in Sub 3 are NOT ACK'd during the accumulation window (up to 10 minutes). This means all accumulating messages appear in the Pending Entry List. If Sub 3 crashes mid-batch, messages are redelivered from PEL on restart. The orphaned accumulator check on startup (`client.delete(BATCH_KEY)`) ensures no stale batch state persists.

**Merchant ID resolution.** The webhook gateway attempts to resolve Square's `merchant_id` string to an internal UUID via `app.merchants.source_merchant_id`. If this lookup fails (new merchant, lookup error), the Square `merchant_id` string is used as-is. This means some evidence records may have Square IDs rather than internal UUIDs as `merchant_id`. Sub 2 uses the same value from the stream message.

**Sub 2 employee fallback.** When a transaction has no `team_member_id`, Sub 2 attempts to assign the primary employee for the location via `EmployeeLocationAssignment`. This lookup is best-effort; if it fails, `employee_id` is NULL on the transaction.

**Stateless Chirp alert location resolution.** The gateway resolves `location_id` from Square location IDs to internal location UUIDs via `app.locations.square_location_id`. If a location is not found, `location_id` is set to NULL on the alert. This does not prevent the alert from being created.

**Order enrichment latency.** The Square Orders API call in the enricher runs synchronously in the webhook handler. API latency adds to the gateway's P99 response time. If the API call fails or times out, the webhook is accepted and published with the original (unenriched) payload.

**DLQ table vs. stream.** Two DLQ mechanisms exist: the `canary:dead_letter` Valkey stream (written by Sub 1 for poison messages) and the `dead_letter_queue` PostgreSQL table (used by `dlq_processor.py` for structured retry tracking). These are not synchronized — the stream DLQ is for immediate quarantine, the DB table is for scheduled retry with state. The `replay_event` MCP tool operates on the Valkey stream DLQ only.
