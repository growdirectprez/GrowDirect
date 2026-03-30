---
type: spec
domain: tsp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Bilateral Verification Procedure
**PRD ID:** TSP-08
**Version:** 1.2
**Owner:** Jeremy
**Patent Figure Reference:** FIG. 2 — Bilateral Verification bar, FIG. 3 — External Verification (SHA-256 Compare · Merkle Proof · Block Explorer)
**Depends on:** TSP-03 (evidence store), TSP-05 (inscription and Merkle proof)
**Gates:** Forensic audit capability
**Sprint target:** Sprint 6

---

## Purpose

The Bilateral Verification Procedure is an on-demand forensic process that proves — without requiring trust in GrowDirect — that a specific event occurred, was not modified, and is anchored to the Bitcoin time chain. Given an event identifier, the procedure retrieves the raw evidence, recomputes the content hash, verifies the chain hash links to adjacent records, and (if inscribed) verifies the Merkle proof path against the inscription. The result is a structured evidentiary report suitable for audit, legal, or regulatory proceedings. This procedure is read-only — it never modifies the evidence store.

**Authentication:** This endpoint is restricted to authenticated users with the `audit` role (GrowDirect admin, merchant owner, or external auditor with granted access). Unlike TSP-07's 402 endpoint (where hash disclosure is harmless), bilateral verification exposes full evidence details, chain structure, and Merkle proof paths. Access is controlled via the same JWT/session auth used by the Canary app.

---

## Architecture Position

**What it reads (canary_sales — read-only):**
- TSP-03 `evidence_records` — `event_id`, `merchant_id`, `source_event_id`, `event_hash` (BYTEA), `chain_hash` (BYTEA), `previous_chain_hash` (BYTEA), `raw_payload` (TEXT), `parse_failed`, `sealed_at`
- TSP-05 `event_inscriptions` — `event_hash` (BYTEA), `batch_id`, `leaf_index`, `merkle_proof_path` (JSONB)
- TSP-05 `inscription_pool` — `batch_id`, `merkle_root` (BYTEA), `tree_depth`, `tree_algorithm_version`, `inscription_id`, `bitcoin_block`, `bitcoin_txid`, `block_explorer_url`, `status`

**What it writes (canary_app — append-only):**
- `verification_audit_log` — full report for every invocation, immutable

**Cross-database note:** Same pattern as TSP-07. Evidence in `canary_sales` (read-only role), audit log in `canary_app` (write). Two connection strings. Audit log writes are best-effort — if `canary_app` INSERT fails, the verification report is still returned to the caller.

**FIG. 2 mapping:** Bilateral Verification bar — spans the full timeline, can be invoked at any point.

**FIG. 3 mapping:** External Verification path — SHA-256 Compare · Merkle Proof · Block Explorer.

---

## API Contract

### Verify Event

**URL:** `POST /verify`
**Auth:** `Authorization: Bearer <jwt>` — requires `audit` role.

**Input validation:** If `event_hash` is provided, it must be exactly 64 hex characters. If not, return 400. The API converts hex to BYTEA for the PostgreSQL query: `decode('{event_hash}', 'hex')`.

**Request (by merchant + source event):**
```json
{
  "merchant_id": "offset-coffee-001",
  "source_event_id": "py_abc123def456"
}
```

**Request (by event hash):**
```json
{
  "event_hash": "a3f9c8d7..."
}
```

**Response — 400 Bad Request (malformed input):**
```json
{
  "status": "bad_request",
  "message": "event_hash must be exactly 64 hex characters (SHA-256)."
}
```

**Response — 401 Unauthorized:**
```json
{
  "status": "unauthorized",
  "message": "Authentication required. Provide a valid JWT with audit role."
}
```

**Response — 200 OK (all checks pass):**

```json
{
  "status": "verified",
  "event_id": "evt_01HXYZ789ABC",
  "merchant_id": "offset-coffee-001",
  "source_event_id": "py_abc123def456",
  "parse_failed": false,
  "verification_steps": [
    {
      "step": 1,
      "name": "evidence_retrieval",
      "status": "pass",
      "detail": "Evidence record found. chain_position: 4721."
    },
    {
      "step": 2,
      "name": "hash_recomputation",
      "status": "pass",
      "detail": "SHA-256 of stored raw_payload (TEXT) matches stored event_hash (BYTEA).",
      "computed_hash": "a3f9c8d7...",
      "stored_hash": "a3f9c8d7..."
    },
    {
      "step": 3,
      "name": "source_comparison",
      "status": "skipped",
      "detail": "Source comparison deferred to Phase 2. Webhook body is not retrievable from Square API."
    },
    {
      "step": 4,
      "name": "chain_integrity",
      "status": "pass",
      "detail": "chain_hash correctly links to previous record for this merchant.",
      "chain_hash": "b4e2f1a9...",
      "previous_chain_hash": "c5d3e2b8...",
      "expected_chain_hash": "b4e2f1a9...",
      "algorithm": "SHA-256(previous_chain_hash || event_hash)"
    },
    {
      "step": 5,
      "name": "bitcoin_inscription",
      "status": "pass",
      "detail": "Merkle root recomputed from proof path matches inscription_pool.merkle_root.",
      "inscription_id": "i39f7a...",
      "bitcoin_block": 884201,
      "block_explorer_url": "https://ordinals.com/inscription/i39f7a...",
      "merkle_root_verified": true,
      "tree_algorithm_version": 1
    }
  ],
  "overall_result": "VERIFIED — event integrity confirmed across all layers",
  "verified_at": "2026-02-26T15:45:00Z"
}
```

**Response — 200 OK (tamper detected):**

```json
{
  "status": "tamper_detected",
  "verification_steps": [
    {
      "step": 2,
      "name": "hash_recomputation",
      "status": "FAIL",
      "detail": "SHA-256 of stored raw_payload does NOT match stored event_hash. Possible data modification.",
      "computed_hash": "XXXXXXXX...",
      "stored_hash": "a3f9c8d7..."
    }
  ],
  "overall_result": "TAMPER DETECTED — evidence integrity compromised",
  "verified_at": "2026-02-26T15:45:00Z"
}
```

**Response — 404 Not Found:**

```json
{
  "status": "not_found",
  "message": "No evidence record found for the given identifier."
}
```

---

## Verification Steps (Numbered Procedure)

| Step | Name | Operation | Pass Condition | Fail Condition |
|------|------|-----------|---------------|----------------|
| 1 | Evidence retrieval | `SELECT * FROM evidence_records WHERE merchant_id = $1 AND source_event_id = $2` (or `WHERE event_hash = decode($1, 'hex')` if lookup by hash). | Row found | Row not found → 404 |
| 2 | Hash recomputation | Read `raw_payload` (TEXT column). Encode as UTF-8 bytes. Compute `SHA-256(bytes)`. Compare against stored `event_hash` (BYTEA). | Match | Mismatch → TAMPER DETECTED |
| 3 | Source comparison | **Phase 1: SKIPPED.** Returns `skipped` with explanation. See Phase 2 note below. | N/A Phase 1 | N/A Phase 1 |
| 4 | Chain integrity | Query previous record: `SELECT chain_hash FROM evidence_records WHERE merchant_id = $1 AND id < $2 ORDER BY id DESC LIMIT 1`. **Genesis:** verify `chain_hash = SHA-256(event_hash)` and `previous_chain_hash IS NULL`. **Non-genesis:** verify `previous_chain_hash` matches previous record's `chain_hash`, then verify `chain_hash = SHA-256(previous_chain_hash \|\| event_hash)` where `\|\|` is byte concatenation. | Chain links correctly | Chain gap, missing predecessor, or hash mismatch |
| 5 | Bitcoin inscription | Look up `event_inscriptions` for this `event_hash`. Retrieve `merkle_proof_path` (JSONB array of `{position, hash}` siblings). Starting from `leaf_hash = double-SHA-256(event_hash)` (per TSP-05 second-preimage defense), walk the proof path upward, hashing with each sibling at the indicated position (left/right). Compare recomputed root against `inscription_pool.merkle_root`. Pass if match. | Root matches | Proof invalid or inscription not found |

**Step 2 note:** The `raw_payload` column is TEXT (not JSONB) specifically to preserve byte-identity for hash re-verification. JSONB normalizes JSON (reorders keys, strips whitespace) which would break SHA-256. This design decision in TSP-03 v1.1 is what makes bilateral verification possible.

**Step 3 — Phase 1 (Sprint 6): Always `skipped`.** The original concept of comparing against "the source network's send log" is not feasible as designed. The `event_hash` is SHA-256 of the webhook body, but Square's API endpoints (e.g., `GET /v2/payments/{id}`) return a different JSON structure than the webhook payload. You cannot hash the API response and match it against the webhook body hash. **Phase 2 design options:** (a) Field-level comparison — fetch event from Square API, compare key business fields (amount, currency, created_at) against parsed_payload JSONB, report matches/mismatches; (b) Webhook replay — if Square offers webhook replay/audit logs in the future; (c) Merchant-initiated — merchant provides their own copy of the event data for comparison. Phase 2 will choose after Square API capabilities are assessed.

**Step 4 note:** The chain hash algorithm is defined in TSP-03 v1.1: `chain_hash = SHA-256(previous_chain_hash || event_hash)` for non-genesis records, `chain_hash = SHA-256(event_hash)` for genesis records. `||` is byte concatenation (not string concatenation with delimiters). The existing `hash_chain.py` in the codebase uses a different algorithm (pipe-delimited string concatenation for `fox_evidence`) — TSP pipeline chain hashes are a separate, BYTEA-based system. Do not confuse the two.

**Step 5 note:** If the event has not yet been inscribed (batch pending in `inscription_pool`), step 5 returns `pending` — not a failure. The `tree_algorithm_version` from `inscription_pool` determines which Merkle tree algorithm to use for root recomputation (currently version 1: duplicate-last-leaf padding, double-hash leaves).

**parse_failed events:** When the target event has `parse_failed = true`, the response includes `"parse_failed": true`. Steps 1-2 still work (raw_payload is stored as TEXT, hash is valid). Step 3 is skipped (Phase 1). Steps 4-5 work normally — malformed payloads are still chained and inscribed. The verifier should note that the event data may not be interpretable as JSON, but its cryptographic integrity is fully verified.

---

## Data Model

### Evidence Data (read-only from this service)

**Database:** `canary_sales` (read — owned by TSP-03 and TSP-05)
**Tables:** `evidence_records`, `event_inscriptions`, `inscription_pool`

This service connects to `canary_sales` with a read-only PostgreSQL role. No writes to sales data.

### Verification Audit Log

**Database:** `canary_app` (write — this service owns it)
**Table:** `verification_audit_log`

```sql
CREATE TABLE verification_audit_log (
    id              BIGSERIAL PRIMARY KEY,
    event_hash      BYTEA NOT NULL,
    merchant_id     TEXT,
    requestor_id    TEXT NOT NULL,
    requestor_role  TEXT NOT NULL,
    steps_executed  INTEGER NOT NULL,
    steps_passed    INTEGER NOT NULL,
    steps_skipped   INTEGER NOT NULL DEFAULT 0,
    steps_failed    INTEGER NOT NULL,
    overall_result  TEXT NOT NULL,
    full_report     JSONB NOT NULL,
    verified_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_verification_audit_event ON verification_audit_log (event_hash, verified_at);
CREATE INDEX idx_verification_audit_result ON verification_audit_log (overall_result, verified_at);
CREATE INDEX idx_verification_audit_requestor ON verification_audit_log (requestor_id, verified_at);
```

Every invocation is logged immutably (best-effort — audit log failure does not block report delivery). If a merchant asks "was my data ever verified?" the answer is in this log. `requestor_id` and `requestor_role` are extracted from the JWT.

---

## Acceptance Criteria

1. Endpoint requires authentication (JWT with `audit` role). Unauthenticated requests return 401.
2. Malformed `event_hash` (not 64 hex chars) returns 400.
3. Given a valid `merchant_id` + `source_event_id` (or valid `event_hash`), the procedure executes all 5 steps and returns a structured report.
4. Step 2 (hash recomputation) reads `raw_payload` from the TEXT column, computes SHA-256 of the UTF-8 bytes, and compares against stored `event_hash` (BYTEA). Detects any modification — even a single byte change.
5. Step 3 (source comparison) returns `skipped` in Phase 1 with explanation. Does not affect overall result.
6. Step 4 (chain integrity) uses the exact TSP-03 v1.1 algorithm: `SHA-256(previous_chain_hash || event_hash)` for non-genesis, `SHA-256(event_hash)` for genesis. Finds predecessor by `WHERE merchant_id = $1 AND id < $2 ORDER BY id DESC LIMIT 1`. Detects any gap or modification.
7. Step 5 (Bitcoin verification) recomputes Merkle root from proof path using `tree_algorithm_version` from `inscription_pool`. Comparison is purely computational — no server-side block explorer HTTP calls. Block explorer URL is informational only (included in response for human verification).
8. The procedure is strictly read-only on `canary_sales` — it never modifies evidence_records, event_inscriptions, or inscription_pool.
9. Every invocation is logged in `verification_audit_log` (best-effort — log failure does not block report delivery).
10. If step 5 (Bitcoin inscription) is pending, the step returns `pending` — not a failure.
11. The verification report is structured JSON suitable for legal proceedings (clear step names, pass/fail/skipped/pending, specific hash values, algorithm identifiers).
12. For `parse_failed` events, the response includes `"parse_failed": true`. All verification steps still execute normally.
13. `requestor_id` and `requestor_role` in audit log are extracted from JWT claims.

---

## Test Cases

### Authentication

1. **No auth header:** `POST /verify` without JWT. Verify: 401.
2. **Wrong role:** JWT with `viewer` role (not `audit`). Verify: 401.
3. **Valid auth:** JWT with `audit` role. Verify: proceeds to verification.

### Input Validation

4. **Malformed event_hash:** 32-char hex string. Verify: 400.
5. **Non-hex event_hash:** 64 chars with 'g'. Verify: 400.

### Happy Path

6. **Full verification pass:** Verify an event that is sealed + inscribed. Steps 1-2 pass, step 3 skipped (Phase 1), steps 4-5 pass. Report shows VERIFIED. Block explorer URL included for human follow-up.

7. **Partial verification (pending inscription):** Verify an event sealed but not yet inscribed. Steps 1-2 pass, step 3 skipped, step 4 passes, step 5 returns `pending`. Overall: VERIFIED (pending Bitcoin confirmation).

8. **Lookup by event_hash:** Provide hex event_hash instead of merchant_id + source_event_id. Verify: same full report. Hex correctly converted to BYTEA for query.

### Failure Detection

9. **Tamper detection (hash mismatch):** Manually modify a raw_payload byte in evidence_records (bypass trigger for test only). Run verification. Verify: Step 2 FAILS with computed_hash != stored_hash. Overall: TAMPER DETECTED.

10. **Chain gap:** Delete one evidence record (bypass trigger for test). Verify next record. Step 4 FAILS: previous_chain_hash doesn't match predecessor's chain_hash.

11. **Chain hash recomputation failure:** Modify chain_hash byte in evidence_records (bypass trigger). Verify: Step 4 FAILS: recomputed chain_hash doesn't match stored chain_hash.

12. **Invalid Merkle proof:** Modify one sibling hash in merkle_proof_path. Verify. Step 5 FAILS: recomputed root doesn't match inscription_pool.merkle_root.

### Edge Cases

13. **Genesis record:** First record for a merchant. Step 4: previous_chain_hash IS NULL. Verify: chain_hash = SHA-256(event_hash). Passes correctly.

14. **parse_failed event:** Verify an event where `parse_failed = true`. Verify: all steps execute normally, response includes `"parse_failed": true`, raw_payload TEXT hash matches event_hash.

15. **Step 3 always skipped (Phase 1):** Verify any event. Confirm step 3 status is `skipped` with Phase 2 deferral message. Overall result is not affected.

16. **Audit log write failure:** Simulate canary_app connection failure. Verify: verification report still returned to caller (best-effort logging).

---

## Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PORT` | integer | 3003 | API listen port |
| `CANARY_SALES_DATABASE_URL` | string | — | canary_sales read-only connection (evidence + inscriptions) |
| `CANARY_APP_DATABASE_URL` | string | — | canary_app read-write connection (verification_audit_log) |
| `JWT_SECRET` | secret | — | JWT verification key (shared with Canary app auth) |
| `BLOCK_EXPLORER_BASE_URL` | string | `https://ordinals.com` | Base URL for block explorer links in response (informational only — no server-side HTTP calls) |

---

## Deployment Readiness (Docker Compose)

1. **Stateless?** Yes. Read-only against evidence store. Audit log is append-only.
2. **Horizontal scaling?** Scaling is via Gunicorn `--workers N` flag in the Flask container (`devops/docker-compose.alpha3x.yml`, line ~279). Multiple instances serve verification requests concurrently. No orchestrator — manual `docker compose up --scale service=N`.
3. **Rolling deployment?** Not supported in Docker Compose. Blue-green deployment via `docker compose up -d` with new image tag. Verification algorithm is deterministic — same input always produces same result. Downtime window: ~5 seconds during container replacement.
4. **Scaling trigger?** Manual. Monitor via Prometheus metrics + Grafana dashboards. Alert threshold: request rate — primarily scales with audit/legal demand, not transaction volume.
5. **Toy store scaling profile:** Verification is rare in normal operation. Single instance handles any demand.

**Cross-PRD Sync (Gap 7):** Synced: all deployment sections reference Docker Compose + Gunicorn (no K8s).

---

## Non-Functional Requirements

| Metric | Target |
|--------|--------|
| **Verification latency (p95)** | < 2 seconds (all steps). Step 5 Merkle recomputation is purely in-memory — no external HTTP calls. |
| **Throughput** | 50 verifications/second (read-only — DB bound) |
| **Durability** | Audit log is append-only. Never deleted. |
| **Accuracy** | 100% — a FAIL must mean real tamper or gap. No false positives. |

---

## IP Protection Notes

The bilateral verification concept — comparing a stored record against both its internal chain position and an external Bitcoin inscription — is part of the patent claim. In external documentation, describe WHAT can be verified (event integrity, chain position, Bitcoin anchoring) and the GUARANTEE (no trust in GrowDirect required for verification). Do NOT describe the specific step sequence, the hash recomputation order, or the chain walk algorithm.

---

## Merkle Proof Recomputation Algorithm (Step 5)

For Jeremy's implementation reference. This must match TSP-05 v1.1 tree construction exactly.

```
Input:
  event_hash       — BYTEA from evidence_records
  merkle_proof_path — JSONB array from event_inscriptions:
                      [{"position": "left"|"right", "hash": "<hex>"}]
  merkle_root      — BYTEA from inscription_pool
  tree_algorithm_version — INTEGER from inscription_pool (currently 1)

Algorithm (version 1):
  1. leaf_hash = SHA-256(SHA-256(event_hash))    // double-hash for second-preimage defense
  2. current = leaf_hash
  3. For each sibling in merkle_proof_path (bottom to top):
       if sibling.position == "left":
         current = SHA-256(decode(sibling.hash, 'hex') || current)
       else:
         current = SHA-256(current || decode(sibling.hash, 'hex'))
  4. Compare current against merkle_root
  5. If match → pass. If mismatch → FAIL.
```

Note: `||` is byte concatenation. The proof path walks from leaf to root. The position indicates where the sibling sits relative to the current node.

---

## Phase 1 Scope

**In scope (Sprint 6):**
- Steps 1, 2, 4, 5 — full internal verification
- Step 3 — returns `skipped` (deferred)
- JWT authentication with `audit` role
- Input validation (hex format, 400 errors)
- Structured JSON verification report
- Verification audit log (best-effort)
- parse_failed event handling
- Merkle proof recomputation (version 1 algorithm)

**Deferred (Phase 2+):**
- Step 3 source comparison — requires Square API assessment (field-level comparison, not hash comparison)
- Batch verification endpoint (multiple events in one request)
- PDF export of verification report for legal/court submission
- External auditor provisioning (invite flow for granting `audit` role)
- Rate limiting (low priority — forensic endpoint, not high-traffic)

---

## Integration Checklist

- [ ] Depends on TSP-03 — evidence_records queryable (canary_sales, read-only role)
- [ ] Depends on TSP-05 — event_inscriptions and inscription_pool queryable (canary_sales, read-only role)
- [ ] canary_sales read-only PostgreSQL role created for this service
- [ ] canary_app verification_audit_log migration applied
- [ ] JWT verification shared with Canary app auth (same JWT_SECRET)
- [ ] Chain hash algorithm matches TSP-03 v1.1 exactly: SHA-256(prev || event_hash) byte concatenation
- [ ] Merkle recomputation algorithm matches TSP-05 v1.1 exactly: double-hash leaves, version 1
- [ ] Step 3 returns `skipped` with clear Phase 2 deferral message
- [ ] Block explorer URL is informational only — no server-side HTTP calls to ordinals.com
- [ ] Audit log immutability verified (append-only, no UPDATE/DELETE)
- [ ] Report format reviewed by Syd for legal/evidentiary suitability
- [ ] parse_failed events verified — all steps pass, response includes parse_failed flag

---

## Revision Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-26 | Condor | Initial draft |
| 1.1 | 2026-02-28 | ALX | Added JWT authentication (audit role). Step 3 source comparison deferred to Phase 2 (webhook body not retrievable from Square API — hash comparison fundamentally impossible as designed). Fixed Step 4 chain walk to use `WHERE merchant_id AND id < $2 ORDER BY id DESC` instead of `id - 1`. Documented exact chain hash algorithm from TSP-03 v1.1 (byte concatenation, not pipe-delimited). Added Merkle proof recomputation algorithm (double-hash leaves, version 1). Made Step 5 purely computational — no server-side block explorer HTTP calls. Split database connections (canary_sales read-only, canary_app write). Made audit log best-effort. Added parse_failed event handling. Added input validation (400 for malformed hex). Added requestor_id/requestor_role to audit log. Documented hash_chain.py vs TSP chain hash difference. Added Phase 1 scope. Updated test cases (16 cases). |
| 1.2 | 2026-02-27 | ALX (B-059) | Deployment Readiness rewritten for Docker Compose + Gunicorn (removed K8s references). Cross-PRD sync note added (Gap 7: Docker Compose). |

---

*TSP-08 | Bilateral Verification Procedure | CONFIDENTIAL*
*Condor | February 27, 2026*
