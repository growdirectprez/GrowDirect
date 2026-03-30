---
type: workorder
domain: infra
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Deploy Pipeline Gate Check
*Issued by ALX · February 26, 2026 · Priority: 🔴 CRITICAL — Jim dry-runs Friday*

**Context:** All five pieces of the deploy pipeline have been built but not in sequence — stack, seed data, smoke test, deploy script, remote deploy script all exist but no gate has been formally verified between them. We can't trust the state of the system going into Jim's Friday dry-run without walking the chain in order.

**Two machines — know which is which:**
- **Mac Mini `192.168.10.102`** — dev box, where the code lives, where Jeremy's Code session runs, where the stack is currently running
- **iMac UAT `192.168.10.117`** — the UAT target box, where `imac_deploy.sh` will deploy TO

**Gates 1–3** run locally on the Mac Mini. No SSH to self. Just run the commands directly in terminal.
**Gate 4–5** test `imac_deploy.sh` SSHing from Mac Mini → iMac UAT.

**Goal:** One session. Walk the pipeline from left to right. Verify each gate. Stop at any failure and fix it before moving on. Do not skip ahead.

**Output:** A single gate check log file at `devops/deploy_reports/GATE_CHECK_2026-02-26.md` that ALX can read and Jim can trust before he picks up his phone Friday.

---

## THE FIVE GATES — IN ORDER

Do not proceed to the next gate until the current one is confirmed GREEN.

---

### GATE 1 — Stack is Healthy

**What to run (directly in terminal on Mac Mini — no SSH to self):**
```bash
cd ~/GrowDirect/Canary

# Services
docker compose --env-file devops/.env.alpha3x -f devops/docker-compose.alpha3x.yml ps

# Migrations at HEAD
docker exec canary_flask alembic -c canary/migrations/alembic.ini current
docker exec canary_flask alembic -c canary/migrations/sales/alembic.ini current
docker exec canary_flask alembic -c canary/migrations/metrics/alembic.ini current

# Trigger count
docker exec canary_postgres psql -U canary -d canary_app -c \
  "SELECT COUNT(*) FROM information_schema.triggers WHERE trigger_schema='public';"

# Test baseline
docker exec canary_flask pytest tests/ -q -m "not docker" --ignore=tests/browser --ignore=tests/e2e
```

**Gate GREEN when:**
- All 4 core services healthy (postgres, flask, valkey, pgbouncer)
- All 3 databases return `(head)`
- Trigger count ≥ 22
- Tests: 0 failures, 0 errors

**If RED:** Run `canary_deploy.sh --full` to rebuild from scratch, then re-check. Do not proceed to Gate 2 with a red stack.

---

### GATE 2 — Seed Data is Loaded and Correct

**What to run:**
```bash
# Re-run the seed script (it's idempotent — safe to run again)
docker exec canary_flask python devops/seeds/level_b_demo.py

# Verify the two active Chirps exist
docker exec canary_postgres psql -U canary -d canary_app -c \
  "SELECT alert_type, severity, created_at FROM alerts WHERE merchant_id='demo-offset-coffee-torrance-0001' ORDER BY created_at;"

# Verify the cash variance is -$18
docker exec canary_postgres psql -U canary -d canary_sales -c \
  "SELECT cash_variance_cents, state FROM cash_drawer_shifts WHERE merchant_id='demo-offset-coffee-torrance-0001';"

# Verify Fox evidence chain hash was computed by trigger
docker exec canary_postgres psql -U canary -d canary_app -c \
  "SELECT id, chain_hash, previous_chain_hash FROM fox_evidence WHERE merchant_id='demo-offset-coffee-torrance-0001';"
```

**Gate GREEN when:**
- 2 active alerts in canary_app (C-102 cash variance, C-001 refund frequency)
- cash_variance_cents = -1800 and state = CLOSED on the morning shift
- fox_evidence.chain_hash is NOT null and NOT 'TRIGGER_WILL_SET'

**If RED:** Fix the seed script or re-run it. The Chirp data is what Jim will see on screen Friday.

---

### GATE 3 — App Serves the Demo on Phone

**What to run:**

From any device on the same WiFi, open:
```
http://192.168.10.102:5002/companion/demo
```
*(This is the Mac Mini dev stack — correct for Gate 3. The iMac UAT stack is Gate 4+.)*

Walk through:
1. Today's View loads — hero banner shows cash shortage Chirp
2. Chirp peek indicator is visible (2 active Chirps)
3. Tap hero Chirp → Process 4 wizard opens (no page reload)
4. Tap through all 6 steps
5. Wizard completes → Chirp resolves → returns to Today's View

**Gate GREEN when:**
- Today's View renders on a real device in under 10 seconds
- Hero Chirp and peek indicator both visible
- Process 4 wizard completes end to end
- Chirp marked resolved on completion

**If RED:** This is a Flask/template issue. Check `docker logs canary_flask --tail 50` for errors. Fix and re-verify Gate 1 before re-testing Gate 3.

---

### GATE 4 — imac_deploy.sh Runs Clean

**Gate 4 is the first time we touch the iMac UAT box (`10.117`).** Before running, confirm:
- iMac UAT is powered on and reachable: `ping 192.168.10.117`
- SSH key is installed: `ssh gclyle@192.168.10.117 echo ok`
- If SSH key not installed: `ssh-copy-id gclyle@192.168.10.117`
- iMac UAT has Docker installed and the repo cloned at `~/GrowDirect/Canary`
- `.env.alpha3x` exists on the iMac UAT

**What to run (from Mac Mini terminal):**
```bash
cd ~/GrowDirect/Canary
./devops/imac_deploy.sh --status
```

This SSHes into `10.117` and reports its stack health without rebuilding anything.

Then do one rebuild to prove the full pipeline:
```bash
./devops/imac_deploy.sh --fast --no-test
```

**Gate GREEN when:**
- `--status` reaches `10.117` and reports service state
- `--fast --no-test` completes, stack on `10.117` comes up
- Demo URL on iMac UAT responds: `http://192.168.10.117:5002/companion/demo`

**If RED:** Most likely causes — iMac UAT not reachable, SSH key not installed, repo not cloned on `10.117`, or `.env.alpha3x` missing on `10.117`. Fix the prerequisite, not the script.

---

### GATE 5 — Full Pipeline Verified End to End

**What to run:**

Simulate what happens the day of the demo — push a change, deploy to UAT, verify it's live.

```bash
# 1. Make a trivial change on Mac Mini, commit it
git commit -am "gate-check: pipeline verification run $(date +%Y%m%d)"
git push origin alpha-clean

# 2. Run the remote deploy to iMac UAT
./devops/imac_deploy.sh

# 3. After deploy completes, re-run seed on iMac UAT
ssh gclyle@192.168.10.117 "cd ~/GrowDirect/Canary && docker exec canary_flask python devops/seeds/level_b_demo.py"

# 4. Verify demo URL on iMac UAT is live
curl -s http://192.168.10.117:5002/companion/demo | head -5
```

**Gate GREEN when:**
- `imac_deploy.sh` (full, with tests) completes on `10.117` without error
- Seed re-runs cleanly on `10.117` after deploy
- Demo URL `http://192.168.10.117:5002/companion/demo` responds

**If RED:** Most likely — seed data wiped by `--full` volume teardown. This is expected behavior. Document the two-step deploy+seed procedure and consider adding `--seed` flag to `imac_deploy.sh` to automate it.

---

## GATE CHECK LOG

When each gate passes, write its result to `devops/deploy_reports/GATE_CHECK_2026-02-26.md`:

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

Fill in actual notes for each gate — what you observed, any issues fixed, the final state.

---

## CRITICAL: SEED DATA SURVIVES REDEPLOY

Gate 5 will likely reveal that `canary_deploy.sh --full` wipes the Docker volumes including the database, which destroys the seed data. This is the expected behavior of `--full` mode. But it means every full deploy needs a seed re-run.

Document this clearly in the gate check log. The procedure for Jim's Friday dry-run and Monday demo is:

```
1. ./devops/imac_deploy.sh --fast --no-test    ← quick rebuild if needed
2. docker exec canary_flask python devops/seeds/level_b_demo.py   ← re-seed
3. Verify demo URL responds
```

If this is cumbersome, add a `--seed` flag to `imac_deploy.sh` that auto-runs the seed script after a successful deploy. Optional — document the manual procedure first, automate it if time allows.

---

## ACCEPTANCE CRITERIA

| # | Criterion |
|---|---|
| AC-1 | All 5 gates verified GREEN in sequence |
| AC-2 | Gate check log written to `devops/deploy_reports/GATE_CHECK_2026-02-26.md` |
| AC-3 | Seed-after-deploy procedure documented (manual or automated) |
| AC-4 | Jim's section in HANDOFF.md updated with: demo URL, seed procedure, any known gaps |

---

## FILE LOCATIONS

| File | Path |
|---|---|
| This work order | `_ALX/WorkOrders/WORKORDER_Jeremy_DeployPipelineGateCheck.md` |
| Gate check log (to create) | `Canary/devops/deploy_reports/GATE_CHECK_2026-02-26.md` |
| Deploy script | `Canary/devops/canary_deploy.sh` |
| Remote deploy script | `Canary/devops/imac_deploy.sh` |
| Seed script | `Canary/devops/seeds/level_b_demo.py` |

---

## ESTIMATED EFFORT

**2–3 hours.** Most of this is running commands and reading output, not writing code. The only likely code fix is the seed-after-deploy procedure if Gate 5 reveals the volumes are wiped.

---

## HANDOFF TO JIM

When all 5 gates are GREEN, update Jim's section in HANDOFF.md:

```
Demo URL: http://192.168.10.102:5002/companion/demo
Seed procedure: docker exec canary_flask python devops/seeds/level_b_demo.py
Gate check log: Canary/devops/deploy_reports/GATE_CHECK_2026-02-26.md
Status of all 5 gates: [GREEN/RED + notes]
Known gaps before dry-run: [anything that didn't pass]
```

Jim needs to know exactly what to expect Friday before he picks up his phone.

---

*Issued by ALX.*
*Acceptance: Gate check log exists, all 5 gates GREEN, Jim's HANDOFF updated.*
