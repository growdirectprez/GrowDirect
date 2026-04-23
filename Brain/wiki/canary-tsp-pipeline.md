---
date: 2026-04-23
type: wiki
tags: [canary, tsp, webhook, ingestion, pipeline, valkey, merkle, evidence]
sources:
  - Canary/docs/sdds/v2/webhook-pipeline.md
  - Canary/canary/blueprints/webhooks_tsp.py
  - Canary/canary/services/tsp/
  - Canary/canary/services/parsers/
last-compiled: 2026-04-23
needs-review: 2026-05-07
method-role: Writer
method-stage: close
---

# Canary TSP Pipeline

## Summary

TSP (Triple Subscriber Pipeline) is Canary's ingestion front door. Every Square webhook enters through a single Flask endpoint, gets HMAC-validated and hashed, and is published to a Valkey stream. Four independent consumer services then read from that stream — one seals evidence, one parses into the canonical data model, one batches hashes into Merkle trees for Bitcoin anchoring, and one runs detection. The stream is the source of truth; the database is downstream.

## What it does

TSP receives Square webhooks, proves they arrived intact, and hands them to four independent workers without coupling any of them. A webhook cannot be lost, duplicated, or silently modified between Square and Canary: signature verification happens before parsing, the SHA-256 hash is computed over raw bytes before JSON ever touches the payload, and idempotency is enforced by a Valkey `SET NX` check. Once the stream write succeeds, TSP returns 200 to Square. Everything downstream is decoupled from the HTTP path.

## How it works

### The entry point

`POST /webhooks/<source>` is served by the `webhooks_tsp_bp` blueprint. It runs a fixed 10-step sequence on every request:

1. Read raw bytes from the request
2. Validate the source is registered (`square` is the only current source)
3. Check payload size against `MAX_PAYLOAD_BYTES` (1MB)
4. Verify HMAC-SHA256 signature with timing-safe comparison (`hmac.compare_digest`)
5. Compute `event_hash = SHA-256(raw_bytes)` — before any JSON parsing
6. Parse JSON to extract routing fields (merchant_id, event_type)
7. Idempotency check against Valkey DB 3 with a 24h TTL
8. Generate a ULID as the Canary-internal event_id
9. Publish a 9-field message to the `canary:events` Valkey stream
10. Best-effort insert into `ingestion_log` and return 200

Step 5 is load-bearing. The hash is the content-addressable anchor for the entire evidence chain, so it must be computed on the exact bytes Square sent, not on a re-serialization.

### The four consumers

Each consumer is a separate Docker service launched by `python -m canary.services.tsp.run_consumer --consumer sub1|sub2|sub3|sub4`. Each uses `XREADGROUP` with its own consumer group, so they read the same stream without coordinating and scale independently.

**Sub1 — seal.** Recomputes the event hash from the raw payload, compares it to the hash the HTTP handler wrote. A mismatch is a tamper signal, routed to the dead letter stream. If it matches, Sub1 computes a per-merchant chain hash (`SHA-256(prev_chain_hash || event_hash)` — genesis rows hash only the event hash), takes a `pg_advisory_xact_lock` on the merchant to serialize chain writes, and inserts a write-once row into `evidence_records`. Immutability is enforced by PostgreSQL trigger, not application code.

**Sub2 — parse.** Routes events by `event_type` to one of six Square parser modules, each a pure function (JSON dict in, flat dict out, no side effects). The parsers cover payments + refunds, orders + line items + tenders, loyalty accounts and events, payouts, disputes, and auxiliaries (cash drawer shifts and events, timecards, inventory, gift cards). Parsed rows become SQLAlchemy model instances and are written to the `sales` schema. `ingestion_log.status` updates to `parsed`. If the event is detection-eligible, Sub2 publishes a 5-field message to a second stream, `canary:detection`.

**Sub3 — merkle.** Accumulates event hashes in a Valkey sorted set. Flushes when either 100 events have arrived or 600 seconds have elapsed, whichever comes first. Builds a deterministic Merkle tree: leaves sorted by hex, double-hashed, padded to a power of two. The tree root goes to `inscription_pool`; per-event proof paths go to `event_inscriptions`. Bitcoin inscription is mocked in dev (`MOCK_INSCRIPTION=true`). Critically, Sub3 does not acknowledge stream messages until the batch commits — if the flush fails, every event in the batch redelivers.

**Sub4 — detect.** Reads from `canary:detection`, not `canary:events`. Routes by `detection_type` (transaction, cash_drawer, gift_card, loyalty) into the Chirp rule engine. Sub4 uses two SQLAlchemy sessions: it reads from `canary_sales` and writes alerts to `canary_app`. See [[canary-chirp-rules|Canary Chirp Rules]] for what happens once Sub4 hands the transaction off.

### The two streams

| Stream | Fields | Consumers |
|---|---|---|
| `canary:events` | 9: event_id, merchant_id, source, source_event_id, event_type, event_hash, raw_payload, received_at, parse_failed | Sub1, Sub2, Sub3 |
| `canary:detection` | 5: transaction_id, merchant_id, event_type, event_id, detection_type | Sub4 |

The two-stream split means detection never blocks evidence sealing or Merkle batching. Sub2 is the only bridge between them.

### Failure handling

Consumers acknowledge only on success. Failed messages stay in the Pending Entries List and redeliver. A consecutive error count over 10 shuts the consumer down. Backoff between retries is `min(2^(errors-1), 30)` seconds. Poison messages — malformed fields, tamper-detected events, repeated failures — go to the `canary:dead_letter` stream and the `dead_letter_queue` table with full error context. The DLQ retry processor (`canary/services/tsp/dlq_processor.py`) re-enters failed events at the stage that failed; exhausted retries stay in the table with an exposed MCP tool for manual replay.

### Schema drift

Every accepted webhook gets a fingerprint: SHA-256 of the sorted set of field paths in the payload. Known fingerprints increment an occurrence counter. New fingerprints trigger a diff against the latest variant for that event type and create a `schema_drift_alerts` row. These surface in the DevOps dashboard, which is how the team finds out Square added or moved a field before the parser breaks.

## Key decisions

**Hash before parse.** Computing the event hash on raw bytes before JSON parsing means the evidence chain anchors to exactly what Square sent, not a re-encoded version. This matters for forensic admissibility and for catching any byte-level tampering.

**Stream is the source of truth.** The HTTP handler returns 200 only after `XADD` succeeds; the `ingestion_log` insert is best-effort. This inverts the usual pattern (commit to DB, then queue) but eliminates the write-ahead-log/outbox complexity at the cost of a narrow race where the DB row might lag the stream entry by a few milliseconds. The downstream consumers rebuild `ingestion_log` anyway.

**One stream, four consumer groups.** Using consumer groups instead of four separate streams means every consumer sees every event without the publisher having to fan out. Each consumer advances its own cursor independently.

**Write-once, trigger-enforced.** The 19 `canary_sales` tables are SOX-relevant. Rather than trusting application code to not modify rows, PostgreSQL BEFORE UPDATE / BEFORE DELETE triggers reject the mutation outright. Direct writes are blocked; data enters only via the TSP consumer pipeline or the initial sync batch path.

**Hash chain is per-merchant, not global.** Each merchant has its own chain starting from a genesis row. This keeps chains tractable when a merchant churns and avoids a global contention point on the chain head.

**Two hash chain algorithms.** The `evidence_records` chain (raw BYTEA concatenation) and the `fox_evidence` chain (sorted JSON + pipe-delimited hex) coexist. They serve different purposes and intentionally do not share code. See [[canary-fox-case-management|Canary Fox Case Management]] for the Fox-side chain.

## Code pointers

- [canary/blueprints/webhooks_tsp.py](../../Canary/canary/blueprints/webhooks_tsp.py) — HTTP entry point, 10-step sequence, HMAC validation
- [canary/blueprints/receipt_tsp.py](../../Canary/canary/blueprints/receipt_tsp.py) — Sealed evidence + inscription proof lookup by hash or event_id
- [canary/services/tsp/run_consumer.py](../../Canary/canary/services/tsp/run_consumer.py) — Consumer entry point, launched per Docker service
- [canary/services/tsp/stream_publisher.py](../../Canary/canary/services/tsp/stream_publisher.py) — XADD wrapper, 9-field message contract
- [canary/services/tsp/consumers/sub1_seal.py](../../Canary/canary/services/tsp/consumers/sub1_seal.py) — Chain hashing, evidence write
- [canary/services/tsp/consumers/sub2_parse.py](../../Canary/canary/services/tsp/consumers/sub2_parse.py) — Parser dispatch, CDM write, detection stream publish
- [canary/services/tsp/consumers/sub3_merkle.py](../../Canary/canary/services/tsp/consumers/sub3_merkle.py) — Accumulator, Merkle tree, inscription pool
- [canary/services/tsp/consumers/sub4_detect.py](../../Canary/canary/services/tsp/consumers/sub4_detect.py) — Chirp dispatch, dual-session alert write
- [canary/services/tsp/validators/square.py](../../Canary/canary/services/tsp/validators/square.py) — HMAC and payload validation
- [canary/services/tsp/merkle.py](../../Canary/canary/services/tsp/merkle.py) — Deterministic Merkle tree construction
- [canary/services/tsp/dlq_processor.py](../../Canary/canary/services/tsp/dlq_processor.py) — Dead letter retry, exponential backoff
- [canary/services/tsp/heartbeat.py](../../Canary/canary/services/tsp/heartbeat.py) — Consumer liveness reporting
- [canary/services/webhook_dispatch.py](../../Canary/canary/services/webhook_dispatch.py) — `resolve_route(event_type)` — the parser + CDM + detection_type routing table
- [canary/services/evidence_chain.py](../../Canary/canary/services/evidence_chain.py) — BYTEA chain hash for `evidence_records`
- [canary/services/parsers/](../../Canary/canary/services/parsers/) — Six pure-function parser modules (payment, order, loyalty, payout, dispute, auxiliary)

## Related

- [[canary-architecture|Canary Architecture]] — System overview, where TSP fits in the service mesh
- [[canary-chirp-rules|Canary Chirp Rules]] — What Sub4 does after it picks up a detection message
- [[canary-fox-case-management|Canary Fox Case Management]] — The Fox evidence chain (related but distinct from the TSP evidence chain)
- [[canary-data-model|Canary Data Model]] — Schemas written by the pipeline
- [[canary-detection|Canary Detection Engine]] — Detection architecture overview
- [[Brain/projects/Canary|Canary MOC]]

## Sources

- `Canary/docs/sdds/v2/webhook-pipeline.md` — Source SDD (design authority)
- `Canary/canary/blueprints/webhooks_tsp.py` — Implementation (code authority)
- `Canary/canary/services/tsp/` — Consumer implementations
- `Canary/canary/services/parsers/` — Square parser suite
