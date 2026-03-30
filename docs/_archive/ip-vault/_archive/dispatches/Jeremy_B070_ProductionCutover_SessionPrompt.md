---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — B-070: Production Cutover (Sandbox → Live)

**Date:** March 1, 2026
**Blocker:** B-064 (Heartbeat Rule) — next gate: production credentials
**Priority:** 🔴 CRITICAL — this is the heartbeat
**Branch:** `sprint-6-tsp` (current HEAD: `996562f`)
**Depends on:** B-065-B (webhook automation ✅), B-067 (explorer QA ✅), B-032 (Square merchant ✅)

---

## Context

The sandbox gate is cleared. 26 webhooks processed, all 200 OK. Jim's QA on the capability explorer is PASSED — 16/16 families, both bugs fixed. The `sprint-6-tsp` branch is pushed to origin.

**Now we go live.** Switch from Square sandbox to GrowDirect Lab production merchant credentials. Point the webhook subscription at production. Jeffe triggers a real transaction. Real data flows through the pipeline and populates the explorer.

---

## Standing Directives (non-negotiable)

1. **B-063 SDK Contamination:** Step 0 → `pip show squareup` → confirm v44+. If not, upgrade before touching any code.
2. **B-064 Heartbeat Rule:** Every line traces to a TSP PRD. If it can't, it doesn't belong.
3. Read Condor's coding standards before writing new code: `_ALX/WorkOrders/output/Condor/Square_TSP_CodingStandards_v1.0.md`

---

## Deliverables

### Deliverable 1: Credential Swap (Sandbox → Production)

**Scope:**
1. In `.env` (and `.env.alpha3x` if applicable), swap Square sandbox credentials for GrowDirect Lab **production** credentials:
   - `SQUARE_ACCESS_TOKEN` → production token from Square Developer Dashboard
   - `SQUARE_ENVIRONMENT` → `production` (was `sandbox`)
   - `SQUARE_APPLICATION_ID` → production app ID
   - Verify `SQUARE_MERCHANT_ID` is `MLE55GCYANCYT` (should already be correct — same merchant, different environment)
2. **DO NOT** delete sandbox credentials. Comment them out with `# SANDBOX:` prefix so we can switch back if needed.
3. Verify `.env` is in `.gitignore` — production tokens must NEVER hit the repo.

### Deliverable 2: Webhook Subscription Update

**Scope:**
1. Use `square_webhook_manager.py` to update the existing `canary-hooks` subscription:
   - Verify the subscription works in production mode (sandbox subscriptions may not carry over — check if a new subscription is needed)
   - If new subscription needed: create via `square_webhook_manager.py create` with the same event types
   - Capture new signature key if subscription is recreated → wire to `.env`
2. Confirm the webhook URL is reachable:
   - ngrok tunnel: verify it's running and the URL is current
   - OR if Mac Mini has a stable IP/port: use direct URL (preferred for reliability)
3. Test with Square's test webhook feature first (`square_webhook_manager.py test`) before Jeffe triggers a real transaction.

### Deliverable 3: Explorer Live Verification

**Scope:**
1. After credential swap + webhook wiring, hit the explorer at `/explorer`
2. Confirm the 16 API families are now querying **production** data (not sandbox)
3. Families that returned "empty" in sandbox (8 of 16) should return real data if the merchant account has activity
4. Document which families return data and which are still empty (some may need Jeffe to trigger specific activity types first — e.g., cash drawer, timecards, gift cards)

### Deliverable 4: Real Transaction End-to-End

**Scope:**
1. Coordinate with Jeffe: he triggers a real transaction on the GrowDirect Lab Square terminal (or Square Online)
2. Verify:
   - Webhook fires and hits the endpoint
   - Response is 200 OK
   - Payload is received and processed by TSP-01 (webhook receipt)
   - Data appears in PostgreSQL (Sub 1 seal)
   - Explorer shows the transaction data in the relevant family (Payments, Orders, etc.)
3. **This is the production heartbeat.** One real Square event → Canary catches → processes → visible in explorer.

---

## Output Files

- Updated `.env` / `.env.alpha3x` (production credentials wired, sandbox commented)
- Session notes: `_ALX/WorkOrders/output/Jeremy/Jeremy_B070_ProductionCutover_Notes.md`
  - Include: which families return data, which are empty, any issues encountered, webhook subscription details
- If new webhook subscription created: capture subscription ID + signature key

---

## Success Criteria

1. Explorer at `/explorer` returns production data (not sandbox)
2. At least one family shows real merchant data
3. A Jeffe-triggered transaction is visible end-to-end (webhook → process → explorer)
4. No sandbox credentials are in any committed file
5. Rollback path documented (can switch back to sandbox by uncommenting)

---

## What NOT To Do

- Do NOT modify the explorer code (B-067 is CLOSED, Jim QA passed — no code changes)
- Do NOT change the TSP pipeline code (that's separate Sprint 6 work)
- Do NOT push production credentials to git
- Do NOT create a new branch — this is environment config, not code

---

*Dispatch by ALX | March 1, 2026*
*B-064 Heartbeat Rule: production gate*
