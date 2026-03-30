---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Replay Procedure
**Version:** 1.0
**Owner:** Jeremy
**Depends on:** Sub 1 evidence store (raw payloads), Sub 2 parser (current version), application database schema, progress tracking
**Gates:** Disaster recovery, schema migration, correction of past detections
**Sprint target:** Sprint 7

---

## Purpose

Replay Procedure is an operational capability that rebuilds Sub 2's structured store from Sub 1's immutable evidence. Given a merchant_id and time range, the procedure scans the evidence store (raw payloads with immutable proof), feeds each payload through the current Sub 2 parser, and inserts records into the application database. Replay is idempotent, read-only against the evidence store, and essential for disaster recovery (corrupted application store) or schema migrations (new field added to parser).

**North Star Alignment:** One immutable source of truth. Rebuild any application state from the ground truth in Sub 1.

---

## Acceptance Criteria

1. **Scan Evidence Store:** Given merchant_id + time_range (start_timestamp, end_timestamp), scan evidence_store ordered by received_at. Retrieve all records WHERE merchant_id = X AND received_at BETWEEN Y AND Z.

2. **Feed Through Parser:** For each raw_payload, invoke current Sub 2 parser with merchant_id, event_type (extracted from payload), and raw_payload. Parser returns structured fields (or parse error).

3. **Insert into Application Store:** For each successfully parsed record, insert into application database (same table as live Sub 2 would insert). Use ON CONFLICT DO NOTHING to ensure idempotency: duplicate event_id does not error or update.

4. **Failed Parse Handling:** If parser throws exception on a record, log the error (merchant_id, event_id, error_msg), add to dead-letter queue, **continue processing next record** (do not halt).

5. **Idempotent Operation:** Replay the same time_range twice. Second replay produces identical output: same record count, same field values, no duplicate records.

6. **Read-Only Against Evidence Store:** Replay never modifies Sub 1 evidence_store. Writes only to application database.

7. **Progress Tracking:** Log progress every 100 records: [timestamp] Replayed 100/10000 records (1%). Allow operator to monitor long-running replays.

8. **Completion Report:** On success, output summary: merchant_id, time_range, record_count, parse_failure_count, duration, final_verification_count.

9. **Parser Version Lock:** At replay start, record which Sub 2 parser version is active. Use that version for entire replay. If parser upgraded mid-replay, subsequent replay uses new parser (operator must decide: re-run with old parser or accept version divergence).

---

## Test Cases

### Happy Path
- Replay toy_store events from 2026-02-01 to 2026-02-07
- Evidence store scan returns 1,000 records ordered by received_at
- All 1,000 payloads parse successfully
- All 1,000 inserted into application_store
- Progress logged: 100, 200, 300, ..., 1000 records
- Completion report: 1,000 records inserted, 0 failures, duration 45 seconds

### Edge Cases
- **Empty Time Range:** No events in range. Scan returns 0 records. Replay completes immediately with 0 records inserted.
- **Partial Parse Failure:** 10,000 records in range. 9,990 parse successfully. 10 fail (unknown event type). 9,990 inserted. 10 logged to dead-letter. Replay continues, completes with 9,990 records, failure_count=10.
- **Duplicate Insertion:** Replay 1,000 records. Half already exist in application_store from previous replay. ON CONFLICT DO NOTHING prevents duplicate insert. Final count: 500 new + 500 existing = 500 net insertion.
- **Schema Evolution:** Parser v1 (original replay) had fields [a, b, c]. Parser v2 (new code) has fields [a, b, c, d]. Replay with v2: all records inserted with d populated. Subsequent replay with v2 produces identical output (idempotent).
- **Out-of-Order Records in Evidence Store:** Records retrieved in received_at order, not insert order. Replay maintains received_at order. Output matches original Sub 2 behavior.

### Toy Store Spike Scenario (REQUIRED)
- Evidence store contains 10,000 toy_store records from spike period (5,000 in 6 hours + backlog)
- Replay scans all 10,000, ordered by received_at
- Parser processes all 10,000 successfully (no unknown event types)
- All 10,000 inserted into application_store
- Progress tracking: logged at 100, 200, ..., 10,000
- Completion: 10,000 records, 0 failures, duration < 2 minutes
- Post-replay verification: SELECT COUNT(*) FROM app_store WHERE merchant_id='toy_store' = 10,000
- Results match original insertion (if original Sub 2 run completed)

### Failure Modes
- **Database Connection Lost During Replay:** Replay halts at record N. Operator reconnects. Replay restarted at beginning of same time_range. ON CONFLICT ensures no duplicates. (Recommendation: implement checkpoint/resume logic in Sprint 7.)
- **Parser Upgrade Mid-Replay:** Parser upgraded. Replay detects version change. Operator must decide: restart with new parser version or continue with old. (Document decision explicitly.)
- **Evidence Store Query Timeout:** Large time_range retrieves 100K+ records. Query takes > 5 minutes. Return error + offer smaller time_range for subdivision.

---

## Integration Points

**Reads from:**
- Evidence store (Sub 1): merchant_id, event_id, raw_payload, received_at
- Schema registry: merchant's webhook schema definition
- Sub 2 parser (current version): parse(merchant_id, event_type, raw_payload) → structured_fields or exception

**Writes to:**
- Application database: same tables as live Sub 2
- Dead-letter queue: failed parse records
- Structured logging: progress, completion report, failures
- Replay audit log (optional): history of replay operations

**Replay Query:**
```sql
SELECT merchant_id, event_id, raw_payload, received_at, event_type
FROM evidence_store
WHERE merchant_id = $1 AND received_at >= $2 AND received_at < $3
ORDER BY received_at;
```

**Replay Insert (same as Sub 2):**
```sql
INSERT INTO app_store_transactions (merchant_id, transaction_id, event_id, amount, currency, created_at)
VALUES ($1, $2, $3, $4, $5, NOW())
ON CONFLICT (merchant_id, event_id) DO NOTHING;
```

**Progress Logging:**
```
[2026-02-26 10:15:32] Replay started: merchant_id=toy_store, range=2026-02-01 to 2026-02-07, parser_version=sub2_v1.2.3
[2026-02-26 10:15:35] Replayed 100 / ~10000 records (1%)
[2026-02-26 10:15:42] Replayed 200 / ~10000 records (2%)
...
[2026-02-26 10:17:28] Replayed 10000 / 10000 records (100%)
[2026-02-26 10:17:30] Replay complete: 10000 inserted, 0 failed, duration 118 seconds
```

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Throughput** | 100 records/second | Scan evidence store + parse + insert |
| **Latency per record** | < 12ms | P95 < 50ms including parse |
| **Time range scan** | 100K records in < 20 minutes | Allows operator to subdivide large ranges |
| **Idempotency window** | Permanent | Replay any time_range multiple times, same output |
| **Parser version lock** | Record at replay start | Ensure entire replay uses same parser version |
| **Progress granularity** | Every 100 records | Operator can track long-running replays |
| **Error recovery** | Automatic resume on reconnect | (Sprint 7 enhancement) |

---

## Kubernetes Readiness

1. **Is this component stateless?**
   - **Yes, with caveats.** Replay reads from database, writes to database. No local state. However, replay is **long-running** (2–20 minutes for large ranges). Kubernetes pod eviction during replay would require checkpoint/resume logic. For Sprint 6, assume replay runs to completion without interruption.

2. **Does it scale horizontally?**
   - **Not applicable.** Replay is an operational procedure, not a continuously running service. Single replay job processes one time_range. Multiple simultaneous replays (different merchants) can run independently.

3. **Does it support rolling deployment?**
   - **N/A for replays.** Replay is triggered on-demand, not a background service. Parser upgrade affects future replays but not current replay in progress.

4. **What is the scaling trigger?**
   - **N/A.** Replay is manually triggered or scheduled. No automatic scaling metric.

5. **Toy store scaling profile?**
   - **Single-threaded replay of 10,000 records completes in < 2 minutes.** If parallelization needed (Sprint 8), split time_range across multiple pods and merge results.

---

## Replay Use Cases

| Use Case | Time Range | Notes |
|----------|-----------|-------|
| **Disaster Recovery** | Last 7 days | Application store corrupted. Rebuild from evidence. |
| **Schema Migration** | All records | New parser field added. Replay entire history with new schema. |
| **Bug Fix in Parser** | Last 30 days | Parser bug discovered. Correct parser deployed. Replay last month. |
| **Compliance Audit** | Year to date | Regulator requests verification of all events. |
| **Merchant Correction** | Custom range | Merchant requests correction of specific time range (e.g., "Feb 1-5"). |

---

## Replay Workflow (Operator Guide)

1. **Identify Problem:** Application store corrupted, or parser updated.
2. **Determine Time Range:** Based on last known good state or merchant request.
3. **Invoke Replay:** CLI or API: `POST /replay { merchant_id, start_timestamp, end_timestamp }`
4. **Monitor Progress:** Stream logs or polling. Progress logged every 100 records.
5. **Verify Results:** Query application store post-replay. Count records, spot-check data.
6. **Document:** Log reason for replay, time_range, operator, completion status.

---

## IP Protection Notes

**Safe to document externally:**
- Replay concept (rebuild from immutable source)
- Idempotency mechanism (event deduplication)
- Progress tracking (operator visibility)

**Crown Jewels (do not expose):**
- Parser version locking strategy
- Checkpoint/resume logic (not yet implemented)
- Dead-letter queue implementation (proprietary error handling)
- Schema evolution handling (competitive advantage)

---

## Success Criteria

- [ ] Replay 10,000 records in < 2 minutes
- [ ] All records inserted idempotently
- [ ] Replay twice: identical output both times
- [ ] Parse failure: logged, does not halt replay
- [ ] Progress tracked: logged every 100 records
- [ ] Completion report: summary with counts and duration
- [ ] Integration test: evidence_store scan + Sub 2 parser + app_store insert, end-to-end

---

## Open Questions

1. **Checkpoint/Resume:** If replay interrupted (pod eviction), should we checkpoint progress and resume from last record, or restart from beginning?
2. **Parallel Replay:** Can we split time_range across N pods and replay in parallel? Merge results after? (Enhancement for Sprint 7.)
3. **Replay Audit:** Should every replay operation be logged in a separate audit table for compliance?
4. **Merchant-Initiated Replay:** Can merchants trigger replays via UI, or operator-only?
5. **Parser Version Compatibility:** What if Sub 2 parser is downgraded? Can we replay with old parser version?
