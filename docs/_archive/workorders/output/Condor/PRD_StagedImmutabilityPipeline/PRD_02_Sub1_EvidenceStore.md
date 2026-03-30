---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Sub 1 — Raw Evidence Store Writer
**Version:** 1.0
**Owner:** Jeremy
**Depends on:** Message queue, PostgreSQL database (with trigger support), SHA-256 hash library
**Gates:** Bilateral Verification, Replay Procedure, Sub 3 (Ordinal Minter)
**Sprint target:** Sprint 6

---

## Purpose

Sub 1 is the first queue subscriber. It reads verbatim webhook payloads, writes them unchanged to the evidence store, and cryptographically seals each record with a SHA-256 hash. Sub 1 enforces write-once, chain-links hashes to the preceding record (per merchant), and guarantees forensic immutability. No parsing, no transformation, no logic—just storage and sealing.

**North Star Alignment:** One immutable record of every event, forever. Tamper-proof by design.

---

## Acceptance Criteria

1. **Verbatim Payload Storage:** Raw webhook payload stored exactly as received. No modification, transformation, or interpretation.

2. **Database-Computed Hash:** SHA-256 hash computed by database trigger on INSERT, not by application. Trigger computes hash(event_id || payload || received_at || merchant_id) and stores in hash column.

3. **Cryptographic Chain Link:** Each record includes chain_hash field that links to the hash of the preceding record for the same merchant. Chain ordered by received_at. First record per merchant has chain_hash = null.

4. **Write-Once Enforcement:** Primary key = (merchant_id, event_id). Once inserted, no UPDATE permitted. Application layer rejects any update attempt. Database constraint enforces at schema level.

5. **Idempotency Key:** If application re-attempts insert with same (merchant_id, event_id), second attempt returns gracefully (e.g., PostgreSQL UPSERT with ON CONFLICT DO NOTHING) without error or duplicate hash.

6. **Key Structure:** Records keyed by merchant_id:event_id for fast lookup and chain traversal.

7. **Chain Integrity Verification:** Procedure (separate component) can re-link chain for any merchant + time range and verify no gaps.

8. **Schema Agnostic:** Evidence store does not validate webhook schema. Corrupted, malformed, or unexpected JSON stored as-is.

9. **Durability:** Writes confirmed only after WAL flush (PostgreSQL fsync). No data loss on power failure during write.

---

## Test Cases

### Happy Path
- Webhook payload received from queue
- Event_id, merchant_id, payload extracted
- Database INSERT trigger fires
- Hash computed by trigger: hash(event_id || payload || received_at || merchant_id)
- Chain_hash set to previous record's hash for same merchant
- Record inserted successfully
- Downstream Sub 2 and Sub 3 independently read same queue message

### Edge Cases
- **First Event for Merchant:** No prior record exists. chain_hash = null. Hash computed normally.
- **Duplicate Attempt:** Same (merchant_id, event_id) queued twice within 1 second. First INSERT succeeds. Second INSERT triggers ON CONFLICT DO NOTHING. No duplicate record, no error.
- **Malformed JSON Payload:** Invalid JSON, yet valid signature at Sub 1. Stored verbatim in BYTEA column. No parse attempted.
- **Large Payload:** 10MB payload. Stored verbatim. Hash computed on full blob.
- **Non-ASCII Encoding:** Binary or unusual encoding in payload. Stored as BYTEA. Hash includes exact bytes.
- **Out-of-Order Arrival:** Events received out-of-order per merchant (event_B received before event_A). Each stored with chain_hash pointing to the preceding record by received_at timestamp. Chain verified on integrity check.

### Toy Store Spike Scenario (REQUIRED)
- 500 webhooks received from queue in 60-second burst
- All 500 INSERT statements execute successfully
- All 500 hashes computed by trigger (not application)
- All 500 chain_hash values link correctly to preceding record
- Hash chain verified: unbroken from first to 500th record
- Zero records lost
- Database remains responsive (query latency < 100ms) during and after spike

### Failure Modes
- **Database Connection Lost:** Sub 1 loses connection mid-write. Message remains in queue. Sub 1 reconnects and retries. ON CONFLICT DO NOTHING prevents duplicate.
- **Trigger Failure:** Hash trigger raises exception. INSERT rolled back. Message remains in queue for retry.
- **Disk Full:** Database cannot write. INSERT fails. Message remains in queue. Manual intervention required to free space and resume.
- **Network Partition:** Sub 1 node isolated. Queue broker confirms message still in queue. Sub 1 reconnects, retries, idempotent ON CONFLICT resolves.

---

## Integration Points

**Reads from:**
- Message queue (same queue as Sub 2 and Sub 3, independently)
- Queue message format: { event_id, merchant_id, received_at, raw_payload }

**Writes to:**
- PostgreSQL evidence store table (merchant_id, event_id, raw_payload, hash, chain_hash, created_at)
- Structured logging (insert success/failure, hash computed, chain validated)

**Evidence Store Schema:**
```sql
CREATE TABLE evidence_store (
  merchant_id VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  raw_payload BYTEA NOT NULL,
  hash VARCHAR(64) NOT NULL,  -- SHA-256, hex-encoded
  chain_hash VARCHAR(64),     -- hash of preceding record, null for first
  received_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (merchant_id, event_id),
  CONSTRAINT write_once UNIQUE (merchant_id, event_id)
);

CREATE TRIGGER evidence_store_hash_trigger
BEFORE INSERT ON evidence_store
FOR EACH ROW
EXECUTE FUNCTION compute_hash_and_chain();
```

**Trigger Logic (pseudocode):**
```
FUNCTION compute_hash_and_chain():
  NEW.hash = SHA256(NEW.event_id || NEW.raw_payload || NEW.received_at || NEW.merchant_id)
  PRECEDING = SELECT hash FROM evidence_store
              WHERE merchant_id = NEW.merchant_id
              ORDER BY received_at DESC LIMIT 1
  NEW.chain_hash = PRECEDING.hash OR NULL
  RETURN NEW
```

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Throughput** | 1,000 inserts/minute | Sustain 50x spike (5,000 events / 6 hours = ~14/minute sustained, 500/minute burst) |
| **Latency per INSERT** | < 50ms | Includes trigger execution and WAL flush |
| **Latency (P99)** | < 200ms | Even under spike load |
| **Durability** | WAL fsync before ACK | No data loss on power failure |
| **Storage** | TBD | Depends on merchant webhook volume and retention policy |
| **Query Performance** | < 100ms | Point queries by (merchant_id, event_id); range queries by merchant + time |
| **Chain Gap Detection** | Automatic on read | Can identify missing sequence numbers per merchant |

---

## Kubernetes Readiness

1. **Is this component stateless?**
   - **Yes.** Sub 1 reads from queue, writes to database. Database connection is externalized. Pod restart does not affect state. Next pod picks up where previous left off (idempotent ON CONFLICT).

2. **Does it scale horizontally?**
   - **Yes, with caveats.** Multiple Sub 1 instances can insert in parallel. Idempotency enforced by (merchant_id, event_id) unique constraint. No coordination needed. However, **chain_hash ordering depends on received_at timestamp, not insertion order.** If events arrive out-of-order (network jitter), chain reflects receive order, not insert order. This is acceptable (chain is forensic, not sequential).

3. **Does it support rolling deployment (v1 and v2 simultaneously safe)?**
   - **Yes.** Both versions use same table schema. Both fire same trigger. v1 and v2 instances coexist. On drain, v1 continues processing queued messages until drained, then exits. No schema change required.

4. **What is the scaling trigger?**
   - **Queue depth + database write latency.** K8s watches queue depth (upstream) and database INSERT latency (via metrics export). If queue depth > 5,000 OR database INSERT P99 > 200ms for > 1 minute, spawn additional Sub 1 pod.

5. **Toy store scaling profile (50x spike)?**
   - **Baseline:** 1 instance handles 100 events/day = ~1 INSERT per 14 minutes.
   - **50x spike (500 events / 60 seconds):** 1 instance sustains 500 INSERTs / 60 seconds = ~8.3/second. PostgreSQL with SSD easily handles 100+ INSERTs/second. **Scale to 2 instances for resilience, not capacity.** One instance is throughput-sufficient; two instances protect against node failure.

---

## Chain Integrity Procedure (Separate PRD, referenced here)

Sub 1 outputs can be verified by:
1. Select all records for (merchant_id) ordered by received_at
2. Walk chain forward: for each record, verify chain_hash == hash of preceding record
3. No gaps in chain. First record has chain_hash = null.
4. Output: chain unbroken [true/false], gap locations [list], total records [N]

This procedure is implemented in Bilateral Verification (PRD_04).

---

## IP Protection Notes

**Safe to document externally:**
- Triple subscriber architecture (concept)
- Write-once enforcement (security property, industry standard)
- Cryptographic hash sealing (public algorithm: SHA-256)
- Chain-linking structure (forensic pattern, publicly documented)

**Crown Jewels (do not expose):**
- Trigger implementation details (database-level, not application-level, enforcement)
- Exact hash function formula (event_id || payload || timestamp || merchant_id order)
- Chain re-linking algorithm for gap recovery
- Specific PostgreSQL configuration (fsync policy, WAL settings)

---

## Success Criteria

- [ ] 500 records inserted in spike scenario, all hashes correct
- [ ] Chain integrity unbroken: first to 500th record linked correctly
- [ ] Duplicate (merchant_id, event_id) idempotent: no error, no duplicate
- [ ] Write-once enforced: any UPDATE attempt rejected at application + database level
- [ ] Trigger fires on every INSERT: hash computed by database, not application
- [ ] Bilateral Verification procedure passes: chain walkable, no gaps
- [ ] Kubernetes scaling: 2 instances during spike, no performance degradation

---

## Open Questions

1. **Out-of-order chain:** If events B, A, C arrive in that order (different network paths), is chain_hash ordered by received_at or arrival order?
2. **Chain reconstruction:** If Sub 1 downtime causes queue backlog, and messages arrive out-of-order, does chain need re-linking?
3. **Storage policy:** Is evidence store retained forever, or archived after X days? If archived, how are old hashes linked?
4. **Encryption at rest:** Should raw_payload be encrypted in the database? Trade-off: security vs. query performance.
