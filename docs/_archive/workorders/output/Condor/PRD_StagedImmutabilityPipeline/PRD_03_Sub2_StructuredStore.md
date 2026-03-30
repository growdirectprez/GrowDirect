---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Sub 2 — Structured Store Writer
**Version:** 1.0
**Owner:** Jeremy
**Depends on:** Message queue, Application database (PostgreSQL), Sub 1 (evidence store output), Detection engine
**Gates:** Live detection, Replay Procedure, user-facing queries
**Sprint target:** Sprint 6

---

## Purpose

Sub 2 is the second queue subscriber. It reads the same raw webhook payloads that Sub 1 reads, but instead of storing verbatim, it parses them into structured fields and loads them into the application database. Sub 2 is independent from Sub 1—either can fail without affecting the other. Detection engine triggers on Sub 2 output. Sub 2 enables fast, indexed queries and real-time analysis, while Sub 1 preserves immutable proof.

**North Star Alignment:** Fast detection, searchable store, human-readable insights—all without compromising forensic integrity.

---

## Acceptance Criteria

1. **Independent Queue Consumption:** Sub 2 subscribes to same queue as Sub 1 and Sub 3. Each message consumed independently. No coordination between subscribers. One Sub 2 failure does not affect Sub 1 or Sub 3.

2. **Schema-Aware Parsing:** Payload parsed according to merchant's webhook schema (e.g., Stripe event format, Square format, custom). Parser is schema-specific, not generic.

3. **Structured Field Routing:** Parsed fields routed to appropriate table based on event type. Example: charge.succeeded → transactions table, customer.created → customers table.

4. **Merchant Partition Loading:** Records stored in merchant-specific partition or namespace. Fast queries: SELECT * FROM app_store WHERE merchant_id = X AND created_at > Y.

5. **Detection Engine Trigger:** Sub 2 INSERT triggers detection rules. Detection output available within SLA (separate PRD, Canary Detection Engine).

6. **Idempotent Replay:** Given merchant_id + time_range + current parser version, sub can replay events from Sub 1's evidence store. Output must be byte-for-byte identical to original Sub 2 output (given same parser version).

7. **Failed Parse Does Not Block:** If parse fails on a single event, that event is logged to dead-letter queue, but other events continue processing. Sub 1 still has evidence.

8. **Audit Trail:** Every Sub 2 insert logged with source event_id, parser version, timestamp.

---

## Test Cases

### Happy Path
- Stripe charge.succeeded webhook queued
- Sub 2 consumes message independently
- Payload parsed: extracts charge_id, amount, currency, customer_id, timestamp
- Fields routed to transactions table
- Record inserted: transaction_id = event_id, amount, merchant_id, created_at
- Detection engine evaluates transaction against rules
- Query: SELECT * FROM app_store WHERE merchant_id='X' returns transaction immediately

### Edge Cases
- **Unknown Event Type:** Webhook event type not in parser schema (e.g., future Stripe event). Parse fails gracefully. Event logged to dead-letter queue. Sub 1 has evidence. Sub 2 continues with next message.
- **Partial Fields:** Webhook missing optional field (e.g., customer_id null). Parsed with null field. Inserted successfully.
- **Schema Evolution:** Parser updated to handle new field. Old events (from queue, from replay) parsed with old parser during overlap. New events parsed with new parser. No collision.
- **Large Nested Object:** Webhook contains deeply nested JSON (e.g., customer metadata). Parsed and normalized to relational structure or JSONB column.
- **Concurrent Inserts:** Multiple Sub 2 instances insert same event_id (clock skew). Second insert de-duplicated by unique constraint or application logic.

### Toy Store Spike Scenario (REQUIRED)
- 500 webhooks (toy store charge.succeeded) received in 60 seconds
- Sub 2 parses all 500 independently from Sub 1
- All 500 transactions inserted into structured store
- All 500 trigger detection engine
- Detection latency: average 5 seconds per batch (500 records / 100 evaluations per second)
- Query latency: SELECT * FROM app_store WHERE merchant_id='toy_store' returns 500 records in < 500ms
- Zero events dropped
- Zero parse errors (all valid Stripe schemas)

### Failure Modes
- **Parser Version Mismatch:** Sub 2 has Parser v2, but event was created for Parser v1. Backward compatibility check. Parse succeeds if v2 understands v1 format.
- **Database Connection Lost:** Sub 2 loses database connection. Message remains in queue. Sub 2 reconnects, retries, idempotent.
- **Detection Engine Unavailable:** Sub 2 successfully inserts, but detection trigger raises exception. Sub 2 INSERT succeeds anyway. Detection run separately (async).
- **Parser Throws Exception:** Malformed Stripe event (not valid against schema). Parse fails, event sent to dead-letter. Sub 1 evidence preserved. Sub 2 continues.

---

## Integration Points

**Reads from:**
- Message queue (same queue as Sub 1 and Sub 3, independently)
- Queue message format: { event_id, merchant_id, received_at, raw_payload }
- Schema registry (merchant's webhook schema definition)

**Writes to:**
- Application database (partitioned by merchant_id)
- Partitioned table structure:
  - app_store_transactions (merchant_id, transaction_id, event_id, amount, currency, customer_id, created_at, ...)
  - app_store_customers (merchant_id, customer_id, event_id, name, email, created_at, ...)
  - app_store_events (merchant_id, event_id, event_type, parser_version, created_at, ...)
- Dead-letter queue (failed parses)
- Detection engine (rules evaluator)
- Structured logging (parse success/failure, routing decisions, latency metrics)

**Replay Integration (PRD_05):**
- Given merchant_id + time_range, Sub 2 replay procedure:
  1. Query evidence_store (Sub 1): SELECT * WHERE merchant_id = X AND received_at BETWEEN Y AND Z ORDER BY received_at
  2. Feed each raw_payload through current parser
  3. Insert into app_store (same logic as live Sub 2)
  4. Verify output matches original (sample verification)

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Throughput** | 1,000 parses + inserts/minute | Sustain 50x spike |
| **Latency (parse + insert)** | < 100ms | P99 < 500ms including detection trigger |
| **Parse success rate** | 99.9% | Valid webhook payloads always parse |
| **Query latency (merchant partition)** | < 100ms | SELECT by merchant_id + time range |
| **Parser version compatibility** | Backward 2 versions | v3 parser can handle v1, v2 payloads |
| **Storage efficiency** | Normalized relational + JSONB | No redundant copies of payload |
| **Availability** | 99.9% | Excludes scheduled maintenance |

---

## Kubernetes Readiness

1. **Is this component stateless?**
   - **Yes.** Sub 2 reads from queue, writes to database. Database connection externalized. Pod restart does not affect state. Idempotency enforced by event_id unique constraints.

2. **Does it scale horizontally?**
   - **Yes.** Multiple Sub 2 instances consume queue independently. Idempotency enforced by (merchant_id, event_id) unique constraint per table. No coordination needed. All instances produce identical output from same input.

3. **Does it support rolling deployment (v1 and v2 simultaneously safe)?**
   - **Yes, with caveats.** v1 and v2 can coexist. Both use same table schema (backward compatible). During overlap, v1 parses with old logic, v2 parses with new logic. Events may be processed by either version. Once v1 drains and exits, only v2 processes. Verify schema compatibility before rolling update.

4. **What is the scaling trigger?**
   - **Queue depth + detection latency.** K8s watches queue depth and average time for event to trigger detection. If queue depth > 5,000 OR detection latency > 15 seconds for > 1 minute, spawn additional Sub 2 pod.

5. **Toy store scaling profile (50x spike)?**
   - **Baseline:** 1 instance handles 100 events/day = ~1 parse + insert per 14 minutes.
   - **50x spike (500 events / 60 seconds):** 1 instance parses and inserts 500 events in 60 seconds = ~8.3/second. PostgreSQL easily sustains 100+ INSERTs/second on modern hardware. **Scale to 2 instances for resilience, not capacity.** One instance is sufficient; two instances protect against node failure.

---

## Parser Specification (Reference)

Sub 2 includes a modular parser registry:

```
Parser Registry:
  - stripe:charge.succeeded → StripeChargeParser
  - stripe:customer.created → StripeCustomerParser
  - square:payment.success → SquarePaymentParser
  - square:customer.created → SquareCustomerParser
  - custom:* → CustomWebhookParser (merchant-specific)
```

Each parser is versioned. Replay procedure must specify which parser version to use.

---

## Replay Procedure Walkthrough (See PRD_05)

Example: Rebuild customer records for merchant 'toy_store' from Jan 1 to Jan 31, 2026:

1. Scan evidence_store: SELECT * WHERE merchant_id='toy_store' AND received_at >= '2026-01-01' AND received_at < '2026-02-01' ORDER BY received_at
2. For each record, extract merchant's schema from schema registry
3. Fire current Sub 2 parser: parser.parse(raw_payload, merchant_id, event_type)
4. Insert into app_store_customers (or appropriate table)
5. Progress tracking: logged every 100 records
6. Final verification: count(original) == count(replayed)

---

## IP Protection Notes

**Safe to document externally:**
- Structured store concept (parsed, indexed, fast)
- Partition strategy (merchant isolation, performance)
- Parser architecture (modular, schema-aware)
- Idempotency mechanism (event deduplication)

**Crown Jewels (do not expose):**
- Specific merchant schema mappings (competitive advantage)
- Parser internal logic (proprietary interpretation rules)
- Detection rule trigger implementation (fraud detection specifics)
- Backward compatibility strategy (schema evolution details)

---

## Success Criteria

- [ ] 500 events parsed and inserted in spike scenario
- [ ] All 500 events trigger detection engine
- [ ] Query latency for merchant partition: < 100ms for 500 records
- [ ] Duplicate event_id idempotent: no error, no duplicate record
- [ ] Failed parse: logged to dead-letter, does not block other events
- [ ] Replay procedure: 10,000 events replayed and verified identical
- [ ] Kubernetes scaling: auto-scales to 2 instances during spike

---

## Open Questions

1. **Schema registration:** How are merchant webhook schemas registered? Per-merchant upload, or template library?
2. **Parser versioning:** If merchant's webhook API changes (e.g., new field), do we version the parser or the schema?
3. **Dead-letter handling:** How long do failed parse events remain in dead-letter? Can merchant review and re-parse?
4. **Detection SLA:** What is acceptable latency from Sub 2 insert to detection result available?
5. **Audit trail retention:** How long do Sub 2 insertion logs retained for compliance?
