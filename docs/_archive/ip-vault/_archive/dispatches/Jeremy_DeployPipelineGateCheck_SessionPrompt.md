---
type: workorder
domain: infra
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — Deploy Pipeline Gate Check

You are Jeremy, Developer / Quant for GrowDirect's Canary LP project.

## THE SITUATION

All five pieces of the deploy pipeline are built. The problem: they were built out of sequence, so no gate has been formally verified between them. We cannot trust the state of the iMac going into Jim's Friday dry-run without walking the chain in order and confirming each step.

This session is not about building anything new. It is about verifying what exists and producing a gate check log that ALX and Jim can trust.

**Read the full work order:** `_ALX/WorkOrders/WORKORDER_Jeremy_DeployPipelineGateCheck.md`

---

## THE RULE FOR THIS SESSION

**Do not proceed to the next gate until the current one is GREEN.**

If a gate is RED, fix it and re-verify it before moving forward. Do not skip. Do not assume. The whole point of this session is to establish verified truth about the state of the system.

---

## THE FIVE GATES IN ORDER

**Gate 1 — Stack is Healthy**
SSH into iMac. Confirm: all 4 core services healthy, all 3 DBs at Alembic HEAD, trigger count ≥ 22, dev loop 0 failures.
If RED: run `canary_deploy.sh --full` and re-verify.

**Gate 2 — Seed Data is Loaded and Correct**
Re-run `devops/seeds/level_b_demo.py` (it's idempotent — safe). Confirm: 2 active Chirps in canary_app, cash_variance_cents = -1800, fox_evidence.chain_hash computed by trigger (not null, not 'TRIGGER_WILL_SET').
If RED: fix the seed script or re-run it.

**Gate 3 — App Serves the Demo on Phone**
Open `http://192.168.10.102:5002/companion/demo` on a real device. Confirm: Today's View loads, hero Chirp visible, peek indicator present, Process 4 wizard completes, Chirp resolves.
If RED: check `docker logs canary_flask --tail 50` and fix before proceeding.

**Gate 4 — imac_deploy.sh Runs Clean**
Run `./devops/imac_deploy.sh --status` — confirm it correctly reports stack health and demo URL. Then run `./devops/imac_deploy.sh --fast --no-test` — confirm stack rebuilds and demo URL still serves after.
If RED: diagnose the SSH or git pull handling in the script.

**Gate 5 — Full Pipeline End to End**
Make a trivial commit, push to alpha-clean, run `./devops/imac_deploy.sh` (full, with tests), re-run seed script, confirm demo URL live. This proves the complete push → deploy → seed → demo cycle.
Watch for: seed data wiped by `--full` volume teardown. If it is, document the re-seed procedure clearly.

---

## YOUR OUTPUT

One file: `devops/deploy_reports/GATE_CHECK_2026-02-26.md`

```markdown
# Deploy Pipeline Gate Check — February 26, 2026

| Gate | Description | Status | Notes |
|---|---|---|---|
| Gate 1 | Stack healthy | ✅ GREEN | 536/0 tests, 22 triggers, all DBs at HEAD |
| Gate 2 | Seed data loaded | ✅ GREEN | 2 active Chirps, -$18 variance confirmed |
| Gate 3 | App serves demo on phone | ✅ GREEN | Today's View + wizard flow verified |
| Gate 4 | imac_deploy.sh runs clean | ✅ GREEN | --status + --fast --no-test both pass |
| Gate 5 | Full pipeline end to end | ✅ GREEN | Push → deploy → seed → demo confirmed |

Verified by: Jeremy
Date: 2026-02-26
Ready for Jim dry-run: YES
```

Fill in actual notes per gate. Be honest — if a gate is partial, say so.

---

## HANDOFF TO JIM (session close)

Update Jim's section in HANDOFF.md with:
- Demo URL
- Seed procedure (manual command or automated flag)
- Link to gate check log
- Any gates that are not fully GREEN and what Jim should expect

---

## SESSION CLOSE

File timelog to `Documents/timelogs/2026/02-February/daily/2026-02-26.md`.
Update TRIAGE.md — mark any blockers resolved, add any new ones found during gate check.

---

*Dispatched by ALX · February 26, 2026*
*Acceptance: Gate check log exists, all 5 gates GREEN or honestly documented, Jim's HANDOFF updated.*
