---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Session Prompt: Jeremy — Live Square Webhook Test (B-064 Final Gate)
*Dispatched by: ALX | February 28, 2026 | Priority: 🔴 CRITICAL*
*Classification: INTERNAL — MAXIMUM CONFIDENTIAL*

---

## CONTEXT

Last session (Feb 27 s7): Integration test PASSED — 9/9 steps. Mock webhook fired via curl, pipeline ran end-to-end. Evidence sealed. Mock inscription created. Receipt returned.

**Today:** We move from mock to real. Jeffe's Square sandbox merchant account fires a live webhook. Canary catches it, seals it, and returns a receipt. That's the heartbeat.

---

## STANDING DIRECTIVES

**B-063 (SDK Contamination — non-negotiable):**
- `pip show squareup` → confirm you're on latest (v44.0.1 from last session)
- `requirements.txt` must have `squareup` (no pin) — confirm this is still the case

**B-064 (Heartbeat Rule — non-negotiable):**
- Every line of code traces to a TSP PRD
- No scope additions — fix only what blocks the live webhook

---

## ENVIRONMENT

**Square credentials (.env):**
- `SQUARE_APPLICATION_ID=sandbox-sq0idb-SduFLmiaE43X0BeFC37Taw`
- `SQUARE_ACCESS_TOKEN=EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl`
- `SQUARE_ENVIRONMENT=sandbox`
- `SQUARE_WEBHOOK_SIGNATURE_KEY=` ← **THIS NEEDS TO BE SET** (see Step 2 below)

**Docker stack:** PostgreSQL + Valkey + Flask on the dev machine.
**Flask port:** Confirm from docker-compose (was 5001 in alpha3x stack; was 5000 in integration test).

---

## THE PLAN — RUN IN ORDER

### Step 0: Verify Stack Still Clean

```bash
# Confirm integration test state is intact
docker compose up -d  # or however you bring the stack up
docker ps             # PostgreSQL + Valkey + Flask all running
```

Quick sanity: `curl http://localhost:<port>/webhooks/square` → should return 405.

If anything is broken from last session → fix it before proceeding. Don't skip this step.

---

### Step 1: Expose Webhook Endpoint to Square

Square needs to reach your local endpoint. Two options — pick the one that's working:

**Option A: ngrok (recommended)**
```bash
ngrok http <flask_port>
# Copy the https forwarding URL: https://abc123.ngrok-free.app
```

**Option B: If ngrok is already configured and running**
- Get current URL: `curl http://localhost:4040/api/tunnels`

Note the public HTTPS URL. You'll need it in Step 2.

---

### Step 2: Register Webhook in Square Developer Dashboard

1. Go to: https://developer.squareup.com/apps
2. Select **GrowDirect Canary MVP**
3. Navigate to **Webhooks** (left sidebar)
4. Click **Add Subscription**
5. Set:
   - **URL:** `https://<your-ngrok-url>/webhooks/square`
   - **API version:** latest
   - **Events to subscribe:** `refund.created` (minimum for the heartbeat)
6. Click **Save**
7. **CRITICAL:** Copy the **Signature Key** Square generates and add it to `.env`:
   ```
   SQUARE_WEBHOOK_SIGNATURE_KEY=<paste here>
   ```
8. Restart Flask so it picks up the new env var.

**Verify:** Square shows the subscription as active.

---

### Step 3: Start the Workers

In separate terminal windows (or tmux panes):

**Terminal 1 — Sub 1:**
```bash
cd /path/to/Canary
python run_sub1.py
# Should say: "Starting Sub 1 — Hash & Seal Evidence Writer"
# Should say: "Connected to Valkey" or equivalent
```

**Terminal 2 — Sub 3:**
```bash
python run_sub3.py
# Should say: "Starting Sub 3 — Merkle Batcher & Ordinal Minter"
```

Confirm both workers are waiting. If either fails → fix before continuing.

---

### Step 4: Fire the Real Webhook — Two Options

**Option A: Square Test Event (easiest, no real transaction)**
In the Square Developer Dashboard, on your webhook subscription:
- Click **Test** (or "Send Test Event")
- Select event type: `refund.created`
- Square fires a real signed webhook with a synthetic payload
- Watch your Flask logs

**Option B: Real Sandbox Transaction (full flow)**
1. Use Square's Sandbox API to create a payment, then refund it
2. Or use the Square sandbox point-of-sale app to simulate a transaction

For today, **Option A is preferred** — it proves the pipe without needing to set up a full sandbox payment. Option B is the next gate (real transaction from Jeffe's phone).

---

### Step 5: Verify the Pipeline

Watch the logs in real time. Expected sequence:

```
Flask:  Received POST /webhooks/square
Flask:  HMAC signature verified ✓
Flask:  Event published to canary:events stream — event_id: <ulid>

Sub 1:  Consumed event <ulid> from stream
Sub 1:  SHA-256 hash computed: <hash>
Sub 1:  Evidence sealed in evidence_records — id: <id>
Sub 1:  Chain hash linked to previous entry

Sub 3:  Batch ready — 1 event
Sub 3:  Merkle root computed: <root>
Sub 3:  Mock inscription created — inscription_id: <id>
```

If logs don't show this sequence → diagnose and fix. Document the failure precisely.

---

### Step 6: Confirm in the Database

```sql
-- Connect to canary_sales

-- Sealed evidence
SELECT event_id, event_hash, previous_chain_hash, created_at
FROM evidence_records
ORDER BY created_at DESC
LIMIT 1;

-- Mock inscription
SELECT inscription_id, merkle_root, status, created_at
FROM inscription_pool
ORDER BY created_at DESC
LIMIT 1;
```

Both rows should exist. Chain hash should link to prior entry.

---

### Step 7: Query the Receipt

```bash
# Use the event_hash from Step 6
curl http://localhost:<port>/receipt/by-hash/<event_hash>
```

Expected response:
```json
{
  "event_id": "...",
  "event_hash": "...",
  "sealed_at": "...",
  "inscription_id": "...",
  "merkle_root": "...",
  "proof_path": [...],
  "status": "mock_inscribed"
}
```

**This is the heartbeat.** Screenshot this response.

---

## IF THE HMAC SIGNATURE FAILS

The most likely failure point. If Flask rejects the webhook with 401:

1. Confirm `SQUARE_WEBHOOK_SIGNATURE_KEY` is set in `.env` and Flask restarted
2. Confirm the webhook URL in Square's dashboard exactly matches what Flask receives (include/exclude trailing slash consistently)
3. Check if the HMAC verification code in the webhook handler uses the raw request body (not parsed JSON) — **this is the patent-critical invariant (hash before parse)**
4. If HMAC verification is blocking the test, you can temporarily set a flag to log-but-not-reject (not skip) — log the mismatch, let the event through, then fix the HMAC. Document this as a bug if so.

---

## IF THE WORKERS DON'T CONSUME

If Sub 1 or Sub 3 isn't picking up the event:

1. Verify consumer groups exist: `XINFO GROUPS canary:events` → should show sub1-seal, sub2-parse, sub3-merkle
2. Check Valkey DB number — workers must connect to DB 4
3. Check stream name — Flask publishes to `canary:events`, workers consume from same

---

## SUCCESS CRITERIA

✅ Real Square webhook received (signed, verified)
✅ Event sealed in `evidence_records` with chain hash
✅ Mock inscription in `inscription_pool`
✅ Receipt endpoint returns full proof JSON
✅ Screenshot or log output captured

When all four are green: **B-064 HEARTBEAT CONFIRMED. The pipe is live.**

---

## NEXT GATE (after today)

The next gate is a **real transaction from Jeffe's phone** — Jeffe creates an order on the GrowDirect Lab merchant account, Square fires a real `payment.completed` and/or `refund.created`, Canary seals it. That's Phase 1 validation.

That can happen this session if the sandbox fires events on real API-created transactions. Or it can be a follow-up.

---

## DELIVERABLES

1. Confirmation message: "Live webhook received, sealed, inscribed (mock), receipt returned" — with screenshot/log
2. TRIAGE.md B-064 update: status → HEARTBEAT CONFIRMED (or document what's still needed)
3. HANDOFF.md Jeremy section: next gate clearly stated
4. Timelog: `Documents/timelogs/2026/02-February/daily/2026-02-28.md`

---

## ONE MORE THING

If this session produces a clean live receipt → ALX will write the Jeffe daily brief as:

> 🟢 SHIPPED: The heartbeat is live. Real Square webhook → Canary → sealed → receipt. The protocol works.

Let's get there.

---

*ALX | Chief of Staff | February 28, 2026*
*Reference: B-064 TRIAGE, Jeremy HANDOFF section, TSP_ConsolidatedReview_v1.0.md*
