---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Bilateral Verification Procedure
**Version:** 1.0
**Owner:** Jeremy
**Depends on:** Sub 1 evidence store, SHA-256 hash library, audit logging
**Gates:** User-facing forensics, legal discovery, merchant dispute resolution
**Sprint target:** Sprint 6

---

## Purpose

Bilateral Verification is an on-demand forensic procedure that proves integrity of any notarized event. Given an event identifier, the procedure retrieves the original raw payload from Sub 1's evidence store, independently recomputes its hash, compares against the stored hash, and produces a cryptographic proof that the event has not been tampered with. This procedure is read-only, non-destructive, and audited.

**North Star Alignment:** Prove integrity without explanation. A merchant can verify any event was received and stored exactly as sent.

---

## Acceptance Criteria

1. **Retrieve by Key:** Given (merchant_id, event_id), retrieve record from evidence store. If not found, return 404.

2. **Recompute Hash Independently:** Using same SHA-256 formula as Sub 1 trigger, independently compute hash from: event_id || raw_payload || received_at || merchant_id.

3. **Hash Comparison:** Compare recomputed hash to stored hash. Report match or mismatch.

4. **Chain Verification:** Walk chain backward from target record: verify chain_hash points to preceding record's hash. Verify preceding record's chain_hash points to its predecessor. Report: chain_unbroken [true/false], gap_locations [list].

5. **Evidentiary Report:** Output structured report:
   ```json
   {
     "event_id": "...",
     "merchant_id": "...",
     "status": "verified" | "tampered" | "not_found",
     "hash_stored": "...",
     "hash_recomputed": "...",
     "hash_match": true | false,
     "chain_unbroken": true | false,
     "chain_gaps": [],
     "received_at": "...",
     "verified_at": "...",
     "proof_of_integrity": {...}
   }
   ```

6. **Read-Only Operation:** Bilateral Verification never modifies evidence store. Zero side effects except logging.

7. **Audit Log:** Every invocation logged: who requested, when, which event, result (match/mismatch/not_found). Audit log itself immutable.

8. **Batch Verification:** Support verification of multiple events in single call. Report per-event results.

---

## Test Cases

### Happy Path
- Merchant requests bilateral verification of event_id='evt_abc123'
- Record retrieved: raw_payload, stored_hash, chain_hash all present
- Hash recomputed: hash(event_id || payload || received_at || merchant_id)
- Hashes match: stored_hash == recomputed_hash
- Chain walked: linked to preceding record, preceding linked to its predecessor
- Report: status='verified', hash_match=true, chain_unbroken=true
- Audit log: entry recorded with timestamp and user

### Edge Cases
- **Event Not Found:** event_id does not exist in evidence store. Return 404 + report status='not_found'.
- **Tampered Payload:** (Simulated during test) Stored hash mismatches recomputed. Report status='tampered', hash_match=false. (Indicates evidence store corruption or deliberate tampering.)
- **Chain Gap:** Record retrieved, but chain_hash points to a record that does not exist. Report chain_unbroken=false, gap_locations=[predecessor_id].
- **First Event per Merchant:** chain_hash = null (expected). Verification succeeds: chain_unbroken=true for single record.
- **Batch Verification:** Request verifies 10 events in single call. Returns 10 reports, per-event status.
- **Large Payload:** Event with 10MB raw_payload. Recomputation takes ~1 second. Report generated with hash match confirmed.

### Failure Modes
- **Hash Library Failure:** SHA-256 computation throws exception. Verification fails. Error logged. Report status='error'.
- **Database Read Error:** evidence_store query fails (connection lost). Error logged. Report status='error', event accessible after database recovery.
- **Audit Log Full:** (Unlikely) Audit log table disk full. Verification still completes, but audit entry fails. Separate alert triggered for ops.

---

## Integration Points

**Reads from:**
- Evidence store (Sub 1): merchant_id, event_id, raw_payload, hash, chain_hash, received_at
- Audit log table (for historical verification queries)

**Writes to:**
- Audit log (immutable record of verification request)
- Structured logging (proof report, metrics)

**Evidence Store Query:**
```sql
SELECT merchant_id, event_id, raw_payload, hash, chain_hash, received_at
FROM evidence_store
WHERE merchant_id = $1 AND event_id = $2;
```

**Chain Walk Query (for chain verification):**
```sql
WITH RECURSIVE chain_walk AS (
  SELECT merchant_id, event_id, hash, chain_hash, received_at, 1 as depth
  FROM evidence_store
  WHERE merchant_id = $1 AND event_id = $2

  UNION ALL

  SELECT e.merchant_id, e.event_id, e.hash, e.chain_hash, e.received_at, cw.depth + 1
  FROM evidence_store e
  JOIN chain_walk cw ON e.merchant_id = cw.merchant_id AND e.hash = cw.chain_hash
  WHERE cw.depth < 10000  -- prevent infinite recursion
)
SELECT * FROM chain_walk
ORDER BY received_at DESC;
```

**Audit Log Schema:**
```sql
CREATE TABLE bilateral_verification_audit (
  audit_id SERIAL PRIMARY KEY,
  requested_by VARCHAR(255),  -- user ID or API key
  requested_at TIMESTAMP NOT NULL,
  merchant_id VARCHAR(255),
  event_ids TEXT[],  -- array of requested event IDs
  result VARCHAR(50),  -- "verified", "tampered", "not_found", "error"
  report_summary JSONB,
  ip_address INET,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Latency per event** | < 500ms | Retrieve, recompute, compare |
| **Latency (P99)** | < 2 seconds | Chain walk on large history |
| **Chain walk depth** | 10,000+ records | Support merchants with high event volume |
| **Batch verification** | 100 events/call | Scale to 1,000 if needed |
| **Audit log retention** | Permanent | Never purged |
| **Read availability** | 99.99% | Read-only, minimal lock contention |

---

## Kubernetes Readiness

1. **Is this component stateless?**
   - **Yes.** Reads from database. No local state. Audit log writes are externalized. Pod restart does not affect functionality.

2. **Does it scale horizontally?**
   - **Yes.** Multiple instances can verify independently. All read same evidence_store. No coordination needed. All instances produce identical proof for same input.

3. **Does it support rolling deployment?**
   - **Yes.** Read-only operation. v1 and v2 can coexist. Both use same evidence_store table. No schema change required.

4. **What is the scaling trigger?**
   - **API request rate.** K8s watches HTTP request rate to verification endpoint. If > 100 requests/second, spawn additional instance.

5. **Toy store scaling profile?**
   - **Baseline:** 1 instance handles on-demand verification requests (not high volume).
   - **High contention scenario:** If merchants run batch verification (100 events × 50 merchants), scale to 3–4 instances for query latency headroom.

---

## Proof of Integrity Output

Example bilateral verification report (JSON):

```json
{
  "event_id": "evt_stripe_charge_20260226_123456",
  "merchant_id": "toy_store_42",
  "status": "verified",
  "verification_timestamp": "2026-02-26T15:30:22.456Z",
  "evidence": {
    "received_at": "2026-02-26T14:23:45.123Z",
    "stored_hash": "a3c7f9e2d4b8c1a6e9f2d5c8a3b7e0f1",
    "recomputed_hash": "a3c7f9e2d4b8c1a6e9f2d5c8a3b7e0f1",
    "hash_algorithm": "SHA-256",
    "payload_size_bytes": 2048,
    "chain_position": 42,
    "chain_unbroken": true,
    "chain_length": 10000,
    "chain_gap_locations": []
  },
  "cryptographic_proof": {
    "hash_match": true,
    "chain_linked_to_predecessor": true,
    "predecessor_event_id": "evt_stripe_charge_20260226_123455",
    "predecessor_hash": "b4d8f0e3a5c9d2b7f0e3a6d9b4c8f1a2"
  },
  "integrity_verdict": "UNALTERED",
  "audit_record_id": "audit_20260226_987654321",
  "further_verification_contact": "security@growdirect.com"
}
```

---

## Bilateral Verification Use Cases

1. **Merchant Dispute:** Merchant claims event was not received or was modified. Bilateral verification proves exact receipt + storage.

2. **Regulatory Audit:** Regulator requests proof of event integrity. Verification report is legal evidence.

3. **Incident Investigation:** Security team investigating potential breach. Verification proves no tampering between receipt and storage.

4. **Compliance Audit:** Annual audit. Batch verify sample of events from preceding year.

---

## IP Protection Notes

**Safe to document externally:**
- Hash algorithm (SHA-256, public standard)
- Verification procedure (read-only, non-destructive)
- Proof of integrity narrative (blockchain-like immutability)
- Chain linking concept (cryptographic chain, industry standard)

**Crown Jewels (do not expose):**
- Exact hash formula (event_id || payload || received_at || merchant_id order)
- Chain walk implementation (recursive SQL query)
- Audit log schema and retention policy
- Proof report JSON structure (internal contract)

---

## Success Criteria

- [ ] Unaltered event: hash match confirmed, chain unbroken
- [ ] Simulated tamper: hash mismatch detected and reported
- [ ] Chain gap: detected and reported with gap location
- [ ] Batch verification: 10 events verified in < 5 seconds
- [ ] Audit log: every verification request logged with user, timestamp, result
- [ ] Proof report: JSON structured, reproducible, legally credible

---

## Open Questions

1. **API access control:** Who can invoke bilateral verification? Only merchant's own events, or any user?
2. **Audit log access:** Can merchants view their own verification history via API?
3. **Hash tampering detection:** If evidence_store is compromised, can we detect it? (Merkle tree on Sub 1 output?)
4. **Report signature:** Should proof report be cryptographically signed by GrowDirect? (Adds legal credibility)
