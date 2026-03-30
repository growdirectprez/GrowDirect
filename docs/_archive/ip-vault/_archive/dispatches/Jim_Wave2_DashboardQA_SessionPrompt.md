---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jim Wave 2 Session — B-067 Dashboard QA + TSP Smoke Test Validation
**Work Order:** B-067 QA + TSP pipeline validation
**Date:** February 28, 2026 (queued — fires after Jeremy Wave 2 delivers)
**Dispatched by:** ALX
**Priority:** 🟡 HIGH — Jeffe sees this dashboard. It needs to be clean.
**Session type:** QA + Validation

---

## Context

The B-067 Square Capability Dashboard is a strategic instrument — Jeffe opens it to see everything Square exposes against real sandbox data. Three agents built it:
- **Condor:** Capability map (16 API families)
- **Jeremy:** Backend explorer module + Flask blueprint (16 explore functions)
- **Qwen:** Frontend HTML shell (cards, grid, pipeline strip)

Jeremy wired it together in Wave 2. Now it needs your eyes before Jeffe touches it.

---

## Task 1: Dashboard QA (B-067)

### Access
```
http://localhost:5001/explorer
```
(Or whatever port Flask is running on — check `.env`)

### Test Matrix

| Test | Pass Criteria |
|---|---|
| Page loads without errors | No JS console errors, all 16 cards render |
| Phase badges correct | Payments/Refunds/Webhooks = LIVE (green), Orders through Gift Cards = PHASE 2 (amber), rest = PHASE 3 (gray) |
| Fetch Live Data — Payments | Returns real sandbox data, record count > 0, JSON displays |
| Fetch Live Data — Refunds | Returns real sandbox data (may be 0 if no refunds in sandbox) |
| Fetch Live Data — Webhooks | Returns subscription list (should show `canary-hooks`) |
| Scope Not Granted handling | Phase 2/3 APIs return clean "scope not granted" message, not a crash |
| Error handling | Disconnect network → fetch → shows "Network error" gracefully |
| Mobile responsive | Load on phone (ngrok or LAN) — cards stack to 1 column |
| Pipeline strip | TSP flow diagram renders, coverage table shows LIVE/PHASE 2/PHASE 3 correctly |
| Merchant + Locations auto-fetch | On page load, merchant and locations cards fetch automatically |
| SDK call display | Each card shows the actual SDK method used (e.g., `client.payments.list(limit=10)`) |
| JSON output readable | Pre-formatted, syntax-highlighted, scrollable within card |

### Output
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jim/B067_DashboardQA_v1.0.md
```

For each test: PASS / FAIL / NOTE. If FAIL, include screenshot path or exact error.

---

## Task 2: TSP Pipeline Smoke Test Validation

### Context
Jeremy committed 33 files to `sprint-6-tsp` including `tests/smoke_test_heartbeat.py` with 7 smoke tests. These passed during Jeremy's build session. Validate they still pass on the current branch.

### Run
```bash
cd /Users/geofflyle/GrowDirect/Canary
git checkout sprint-6-tsp
python -m pytest tests/smoke_test_heartbeat.py -v
```

### Output
Append to the same QA doc:
- All 7 tests: PASS / FAIL
- If any fail: exact error output
- Verdict: TSP pipeline smoke tests CLEAN or REGRESSION FOUND

---

## Task 3: Existing Test Baseline Check

Run the full test suite to confirm the new code hasn't broken anything:
```bash
python -m pytest --tb=short -q
```

Expected baseline from Sprint 5: 541 pass / 0 fail / 0 errors / 216 skipped.
Sprint 6 should show the same or better (7 new smoke tests = up to 548 pass).

Report any delta from baseline.

---

## Standing Directives

- This is QA only. No code changes.
- If you find a bug, document it in the QA doc and flag severity (P1-P4). Do NOT fix it.
- P1 bugs route to Jeremy immediately. P2-P4 go to TRIAGE.md.
- The dashboard is for Jeffe — visual polish matters. Flag any card that looks wrong even if the data is correct.

---

## Session Close

Update HANDOFF.md Jim section:
- B-067 QA: PASS or FAIL (with bug count)
- TSP smoke tests: PASS or REGRESSION
- Full suite baseline: match or delta
- Go/No-Go for Jeffe to see the dashboard

Log timelog per TRIAGE Step 0.

---

*ALX | February 28, 2026 | Wave 2 — Jim Dashboard QA + Smoke Test*
*Nothing ships to Jeffe without Jim's sign-off.*
