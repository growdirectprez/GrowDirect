---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Session Prompt: Jeremy — Heartbeat Integration Testing
*Dispatched by: ALX | February 28, 2026 | Priority: 🔴 CRITICAL*
*Classification: INTERNAL — MAXIMUM CONFIDENTIAL*

---

## YOUR MISSION THIS SESSION

The Heartbeat code is BUILT (21 files, 7/7 smoke tests pass from Feb 27 s6). Your job now is to prove it runs end-to-end against real services. Integration testing. One pulse through the pipe.

**The goal:** `docker compose up` → migrations → workers → send a Square webhook → get a receipt back with sealed evidence + mock inscription proof.

---

## STANDING DIRECTIVES — READ BEFORE WRITING ANY CODE

**B-063 (SDK Contamination — non-negotiable):**
Before writing ANY Square integration code:
1. `pip show squareup` or `cat requirements.txt` — confirm SDK version matches latest stable (v43+)
2. If not current → update first, code second
3. You are building from TSP PRDs, NOT from existing code. Existing Square integration code is REFERENCE ONLY.

**B-064 (Heartbeat Rule — non-negotiable):**
Every line of code must trace to a TSP PRD. If it can't — it doesn't belong.

---

## INTEGRATION TEST SEQUENCE

Run these in order. Stop and document if any step fails.

```
Step 1: docker compose up -d
  → PostgreSQL + Valkey + Flask must all come up clean
  → Confirm PostgreSQL canary_sales database exists
  → Confirm Valkey is reachable on configured port

Step 2: Alembic migrations 004, 005, 006
  → Run against canary_sales
  → Confirm new tables: fox_evidence (chain_hash columns), inscriptions, evidence_batches
  → Confirm immutability triggers are active

Step 3: Start Flask app
  → python3 wsgi_alpha3x.py (or equivalent entry point)
  → Confirm webhook endpoint responds: GET /webhooks/square → 405 (method not allowed = good, means route exists)

Step 4: Start Sub 1 worker
  → python3 run_sub1.py (or however the consumer is launched)
  → Confirm it connects to Valkey stream and waits

Step 5: Start Sub 3 worker
  → python3 run_sub3.py
  → Confirm it connects and waits for seal events

Step 6: Send test webhook
  → curl -X POST http://localhost:5000/webhooks/square \
       -H "Content-Type: application/json" \
       -d '{"type":"refund.created","data":{"object":{"refund":{"amount_money":{"amount":1450,"currency":"USD"},"id":"test_refund_001","payment_id":"test_payment_001","created_at":"2026-02-28T14:31:00Z"}}}}'
  → Include HMAC signature header if webhook verification is active (use test signing key)
  → Expected: 200 OK, event published to Valkey stream

Step 7: Verify seal
  → Query fox_evidence table: SELECT * FROM fox_evidence ORDER BY created_at DESC LIMIT 1;
  → Confirm: event_hash populated, previous_chain_hash links correctly, payload stored

Step 8: Verify mock inscription
  → Query inscriptions table: SELECT * FROM inscriptions ORDER BY created_at DESC LIMIT 1;
  → Confirm: merkle_root populated, mock inscription_id generated

Step 9: Query receipt
  → curl http://localhost:5000/receipt/by-hash/<event_hash_from_step_7>
  → Expected: JSON with event details, seal proof, inscription proof
```

---

## KEY FILES TO READ FIRST

1. **TSP Consolidated Review:** `_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md` — bridge document, architecture overview, riskiest seams
2. **Sprint 6 Work Order:** `_ALX/WorkOrders/WORKORDER_B052_Sprint6_ParallelTracks.md` — full track definitions
3. **Smoke test file:** `tests/smoke_test_heartbeat.py` — your own tests from last session

---

## IF SOMETHING BREAKS

1. Document the failure precisely (step #, error message, stack trace)
2. Fix it if the fix is surgical (< 20 lines, traces to a PRD)
3. If the fix is architectural → STOP. Document. Route to ALX.
4. Do NOT add scope. Do NOT fix unrelated issues. Integration testing only.

---

## DELIVERABLES

1. Integration test results — pass/fail for each of the 9 steps above
2. Any fixes applied (with PRD traceability noted)
3. Screenshot or log output of the full pipeline: webhook received → evidence sealed → inscription created → receipt served
4. Updated TRIAGE.md entry for B-064 with integration test status

---

## SESSION CLOSE

File timelog to `Documents/timelogs/2026/02-February/daily/2026-02-28.md`.
Update HANDOFF.md Jeremy section with results.
