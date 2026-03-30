---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Day 3 Finish + Sprint 5 Phase 2
*Issued by ALX · February 24, 2026 · Priority: 🔴 CRITICAL PATH*

**Context:** Day 1+2 of Tom's punch list: DONE. P0-1, P0-2, P0-3 migrations delivered. Valkey verified. You're ahead of schedule. This work order covers what's left — Day 3, CRDM gap closures, and iMac Phase 2 execution.

**Goal:** Close all remaining Tom punch list items + get migrations running on real Postgres (iMac QA box).

---

## PRIORITY 1 — Day 3 Remaining (Tom Punch List)

### Task 1: Verify `cash_variance_cents` computation
**What:** Column exists on `cash_drawer_shifts` per Tom's CRDM. Verify the application code actually *computes* it on shift close.
**Where to look:**
- `canary/services/` — any shift close or cash drawer logic
- `canary/blueprints/` — cash drawer endpoints
- `canary/models/sales/cash_drawer_shifts.py` — the model

**Expected outcome:**
- If computation exists: document where, confirm it writes to the column. Done.
- If computation is MISSING: write it. Formula: `cash_variance_cents = actual_close_amount - expected_close_amount`. This is a business logic gap, not a schema gap. File: wherever shift close logic lives.

**Note from Tom:** `cash_drawer_shifts` is explicitly NOT immutable — it needs UPDATE for shift close events. This is correct and intentional.

---

## PRIORITY 2 — CRDM Gap Closures (Sprint 5 Phase 2)

### Task 2: B-020 — Add `employee_id` + `location_id` to `refund_links`
**Why:** Blocks C-005 CROSS_STORE_RETURN detection rule. Without these columns, Chirp can't detect refunds processed at a different location than the original sale, or by a different employee.
**What:**
- Add `employee_id VARCHAR` (nullable, FK to employees) to `refund_links` model
- Add `location_id VARCHAR` (nullable, FK to locations) to `refund_links` model
- Alembic migration: `005_add_employee_location_to_refund_links.py` in `canary/migrations/sales/versions/`
- Chain from latest sales migration

### Task 3: B-021 — Add `order_id` to `transactions`
**Why:** Needed for Order→LineItem→Tender join path. Without it, we can't trace a transaction back to its order context.
**What:**
- Add `order_id VARCHAR` (nullable) to `transactions` model
- Alembic migration: `006_add_order_id_to_transactions.py` in `canary/migrations/sales/versions/`
- Chain from latest sales migration (or from 005 if Task 2 runs first)

---

## PRIORITY 3 — Run Migrations on Real Postgres (iMac QA Box)

This is the moment of truth. Eva's Phase 2 brief is at:
`Canary_IP/Markdown/Sessions/Jeremy_Phase2_iMac_Brief_2026-02-23.md`

### Task 4: S5-07 — Run Alembic Migrations on iMac
**Prereqs:** Phase 1 Boot is ✅ DONE (12 Docker services healthy).
**What:** Run all Alembic migrations against real PostgreSQL on the 3-database architecture.

```bash
# Get into Flask container
docker exec -it canary_flask bash
cd /app

# canary_app migrations (includes your P0-2, P0-3 triggers)
alembic -c canary/migrations/alembic.ini upgrade head

# canary_sales migrations (includes your P0-1 triggers + CRDM-G2, G3)
alembic -c canary/migrations/sales/alembic.ini upgrade head

# canary_metrics migrations
alembic -c canary/migrations/metrics/alembic.ini upgrade head
```

**Known risk:** Tables may not exist yet. If you get `relation does not exist`, use autogenerate:
```bash
alembic -c canary/migrations/alembic.ini revision --autogenerate -m "initial_canary_app_tables"
alembic -c canary/migrations/alembic.ini upgrade head
```

See Eva's brief for full fallback plan.

### Task 5: S5-08 — Validate INSERT-Only Triggers on Real Postgres
Run the trigger validation tests from Eva's brief. The exact SQL is there. Confirm:
- UPDATE on `fox_evidence` → `CHAIN OF CUSTODY VIOLATION`
- DELETE on `fox_evidence` → same
- UPDATE on `transactions` → `IMMUTABILITY VIOLATION`
- DELETE on `transactions` → same

### Task 6: S5-09 — Validate Hash Chain on Real Postgres
Run the hash chain verification test from Eva's brief:
- Build a 3-record chain
- `verify_hash_chain()` → all valid
- Tamper with record 2 → `verify_hash_chain()` catches it

**Note:** Your Migration 004 moved hash computation from Python to DB triggers. The test in Eva's brief uses the old Python `compute_entry_hash` approach. Instead, test by INSERTing records and verifying the trigger populated `entry_hash` and `previous_chain_hash` correctly, then call `verify_hash_chain()`.

### Task 7: S5-10 — RLS Policy Validation
Apply RLS policies and test tenant isolation per Eva's brief. Known gotcha: table owner bypasses RLS by default — may need `FORCE ROW LEVEL SECURITY`.

---

## PRIORITY 4 — Legacy Cleanup Note

Jeremy flagged in his Feb 24 session: `canary/audit/logger.py` has legacy SQLite-based hash computation (sets `hash` and `prior_hash`). This is the OLD code path — SQLite dialect, `?` params. Does not interact with PostgreSQL triggers.

**Action:** Do NOT fix this now. Log it for Sprint 6 deprecation when Flask fully migrates to PostgreSQL. Just confirm it doesn't interfere with the new trigger-based hashing.

---

## SESSION OUTPUT FORMAT

When done, write to `_ALX/JEREMY_SESSION_OUTPUT_2026-02-2X.md`:

```
# JEREMY SESSION OUTPUT — Feb [date], 2026

## Day 3 Completion
- cash_variance_cents: [found/missing/written]
- Location in code: [file path]

## CRDM Gap Closures
- B-020 (employee_id + location_id on refund_links): [done/blocked]
- B-021 (order_id on transactions): [done/blocked]

## iMac Phase 2 Results
- S5-07 Alembic migrations: [pass/fail — details]
- S5-08 INSERT-only triggers: [pass/fail — details]
- S5-09 Hash chain verification: [pass/fail — details]
- S5-10 RLS policies: [pass/fail — details]
- Table count: canary_app=[n], canary_sales=[n], canary_metrics=[n]
- Trigger count: [n]

## Files Created/Modified
1. [list]

## Blockers Encountered
- [any new items for TRIAGE.md]

## Routing for ALX
- Eva: [status update]
- Jim: [anything unblocked for QA]
- Tom: [any architecture questions]
```

---

## Rules of Engagement

1. **Commit after each completed task.** Don't batch.
2. **If Alembic chokes on multi-database metadata: document it, use create_all as QA workaround, write proper migrations after.** Don't burn hours fighting tooling.
3. **If a trigger test fails: STOP. Document exact error. Don't improvise the fix** — route to Tom if it's architectural.
4. **Orphan counts go DOWN, never UP.**
5. **Log everything.** Terminal output from iMac is Phase 2 evidence.

---

*"Day 1+2 done ahead of schedule. Finish strong."* — ALX

*Issued by ALX. Jeremy owns execution. Report back on completion or if blocked.*
*Canary LP | Confidential*
