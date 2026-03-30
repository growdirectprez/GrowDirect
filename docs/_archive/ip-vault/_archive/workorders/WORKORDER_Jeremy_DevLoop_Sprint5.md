---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy Dev Loop — Sprint 5 Autonomous Build & Test Cycle
*Issued by ALX · February 23, 2026 (evening) · Priority: 🔴 CRITICAL PATH*
*Updated: Feb 23, 2026 (evening) — discovered dev_loop.py already exists. USE IT.*

**Context:** Jeffe is doing the Ubuntu rebuild on Will's rig IRL. While that's happening, Jeremy needs to get into the dev loop on the existing codebase and start iterating the autonomous build-and-test cycle. This is the Sprint 5 integration work — proving that ~4,000 lines of generated code actually work.

**Goal:** By the time Jeffe finishes the hardware setup, Jeremy should have a clear picture of what's green, what's red, and what needs surgical fixes.

---

## 🚨 THE FAST PATH: dev_loop.py EXISTS

`devops/scripts/dev_loop.py` is a complete autonomous multi-model dev loop engine.
It handles SCAN → TRIAGE → BUILD (multi-tier Qwen/Claude) → MIGRATE → TEST → BROWSER → REPORT automatically.

**Run this first (one iteration, local only, $0):**
```bash
cd /Users/geofflyle/GrowDirect/Canary
source venv/bin/activate
python3 devops/scripts/dev_loop.py --once --watch --local-only --no-browser
```

**If that works, let it iterate:**
```bash
python3 devops/scripts/dev_loop.py --watch --local-only --no-browser --max-iter 10
```

**With Claude escalation (costs money, use sparingly):**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python3 devops/scripts/dev_loop.py --watch --tier-cap 3 --budget 5.00 --no-browser --max-iter 10
```

Reports go to: `devops/loop/LOOP_REPORT.md`
Cost tracking: `devops/loop/cost_ledger.json`

**The manual phases below are the FALLBACK if dev_loop.py fails to run.**

---

## PHASE 1: Environment Verify (Do This First)

```bash
cd /Users/geofflyle/GrowDirect/Canary

# 1. Confirm Ollama is running and Qwen model is loaded
curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; tags=json.load(sys.stdin); print([m['name'] for m in tags['models']])"
# Expected: should include 'qwen2.5-coder:7b-instruct-q4_K_M'

# If not running:
ollama serve &
ollama pull qwen2.5-coder:7b-instruct-q4_K_M

# 2. Confirm Docker is running (for QA box integration later)
docker --version
docker compose version

# 3. Confirm Python environment
source venv/bin/activate
python3 -c "import flask; import sqlalchemy; print('Core deps OK')"

# 4. Run current test suite to establish baseline
pytest tests/ --tb=short -q 2>&1 | tail -20
# Record: total passed, total failed, total errors
# Expected baseline: ~739 tests (some may fail without DB)
```

---

## PHASE 2: Run Remaining Sprint 5 Prompt Layers

The BUILD_LOG shows Sprint 5 prompts 600-637 exist but haven't been fully executed through auto_build.py on real hardware. Run them phase by phase:

```bash
# Phase 1: Boot configs (if not already generated)
python3 devops/scripts/auto_build.py --layer sprint5 --range 600-605

# Phase 2: Schema migrations (THE CRITICAL ONE)
python3 devops/scripts/auto_build.py --layer sprint5 --range 610-619

# Phase 3: Seed data
python3 devops/scripts/auto_build.py --layer sprint5 --range 620-624

# Phase 4: Integration tests
python3 devops/scripts/auto_build.py --layer sprint5 --range 630-637
```

**After each phase:** Check BUILD_LOG.md. Any FAIL needs surgical fix before proceeding to next phase.

**The surgical fix pattern (from Sprint 3.5):**
1. Read the FAIL output in BUILD_LOG
2. Open the generated file
3. Fix the specific issue (usually import paths, missing deps, or Qwen hallucinating a module)
4. Re-run the VERIFY command from the prompt file
5. When PASS, move to next prompt

---

## PHASE 3: Close the 20 Orphan Routes

Per ORPHAN_REPORT.md, these 20 routes have no tests:

**Priority 1 — companion_wired.py (5 routes):**
- `GET /today` → `today`
- `GET /wizard/<int:chirp_id>` → `wizard`
- `POST /wizard/<int:chirp_id>/step/<int:step_num>` → `complete_wizard_step`
- `GET /scorecard/<period>` → `scorecard_period`
- `POST /process/<int:process_id>/complete` → `complete_process`

**Priority 2 — fox_wired.py (3 routes):**
- `GET /cases/<int:case_id>/evidence/<int:evidence_id>` → `get_evidence_item`
- `POST /cases/<int:case_id>/actions` → `add_action`
- `GET /cases/<int:case_id>/evidence/verify` → `verify_evidence`

**Priority 3 — remaining:**
- `POST /<alert_id>/escalate` (alerts_wired.py)
- `GET /userinfo` (auth.py)
- `POST /sweep` (chirp_wired.py)
- `GET /readiness` (health.py)
- `GET /<location_id>/stats` (locations_wired.py)
- `GET /<int:id>` (merchants.py)
- `PUT /<int:id>` (merchants.py)
- `GET /billing` (settings.py)
- `GET /receipt/<payment_id>` (app.py)
- `POST /alerts/<int:alert_id>/resolve` (app.py)
- `GET /receipt/<payment_id>` (wsgi.py)
- `POST /alerts/<int:alert_id>/resolve` (wsgi.py)

**Method:** Write test stubs using the existing pattern from `tests/test_route_coverage.py`. Each test should:
1. Hit the route
2. Assert non-500 response
3. Include AC reference in docstring where applicable
4. Follow Coding Standards Rule 1 (AC refs in every test)

---

## PHASE 4: Auth Blueprint Wiring (B-008)

Known gap: `canary/auth/routes.py` exists but was never registered in `wsgi.py`.

```bash
# Check current state
grep -n "auth" wsgi.py
grep -n "register_blueprint" wsgi.py

# The fix (surgical edit — do not rewrite wsgi.py):
# Add the import and register_blueprint call following the Sprint 3.5 pattern
# Look at how fox_wired, chirp_wired, companion_wired are registered
# Mirror that pattern for auth
```

---

## PHASE 5: Docker Integration Test on QA Box

Once Phases 2-4 are clean locally:

```bash
# Build the Docker image
docker compose -f devops/docker-compose.alpha3x.yml build

# Start the stack
docker compose -f devops/docker-compose.alpha3x.yml up -d

# Verify all services boot
docker compose -f devops/docker-compose.alpha3x.yml ps

# Run health check
curl -s http://localhost:5000/health | python3 -m json.tool

# Run test suite inside container (or against container DB)
pytest tests/ -x --tb=short -q
```

---

## PHASE 6: Report Back

When you've completed a full cycle, produce this summary:

```
BUILD STATUS REPORT — Sprint 5 Dev Loop
========================================
Date: [date]
Qwen layers run: [which ranges]
Qwen PASS/FAIL: [counts]
Surgical fixes needed: [list]

TEST BASELINE:
  Before: 739 tests
  After: [count] tests
  Passed: [count]
  Failed: [count]
  New tests added: [count]

ORPHAN ROUTES:
  Before: 20
  After: [count]
  Routes covered this session: [list]

BLOCKERS ENCOUNTERED:
  [any new blockers for TRIAGE.md]

AUTH WIRING (B-008):
  Status: [done/in progress/blocked]

DOCKER BOOT:
  Status: [all services up / partial / blocked]
  Services running: [list]
  Services failing: [list with errors]
```

Write this to `devops/prompts/BUILD_LOG.md` (append) and also to `_ALX/HANDOFF.md` (Jeremy section update).

---

## Rules of Engagement

1. **Orphan counts go DOWN, never UP.** (Coding Standards Rule 10)
2. **AC refs required in every new test.** (Coding Standards Rule 1)
3. **If something breaks mid-cycle: STOP. Note the break. Fix it before continuing.** Don't push through confusion.
4. **Qwen first, Claude for surgical edits only.** Token budget matters. (R-003)
5. **Commit after each green phase.** Don't batch 4 phases into one commit.
6. **If a Qwen output needs more than 10 lines of manual fix, write a better prompt.** The prompt is the product, not the code.

---

*"Code generated ≠ code working. Sprint 5 on real hardware is the only thing that matters right now."* — Eva

*Issued by ALX. Jeremy owns execution. Report back on completion or if blocked.*
