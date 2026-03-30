---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Dev Loop First Cycle (Mac Mini / venv)
*Issued by ALX · February 24, 2026 · Priority: 🔴 CRITICAL PATH*
*Supersedes: WORKORDER_Jeremy_ClosedLoop.md, WORKORDER_Jeremy_Day3_Sprint5Ph2.md*

**Jeffe directive:** Everything runs in dev first. Mac Mini. venv. Terminal. No iMac Docker, no Playwright against live services — not yet. The dev loop needs to actually *loop* before we commit this package and pull it down for real hardware testing.

**What "done" looks like:** Jeffe types one command in terminal, walks away, comes back to a LOOP_REPORT that shows multiple iterations with real test counts going up and real failures going down. That has never happened yet.

---

## WHAT'S ACTUALLY TRUE RIGHT NOW

| Thing | Status |
|---|---|
| dev_loop.py exists | ✅ Yes — 7 phases, multi-tier model routing, cost tracking |
| dev_loop.py has run | ✅ Once — iteration 1, Feb 23 |
| dev_loop.py looped | ❌ **No.** Ran --once, declared false green, stopped |
| B-018 false positive | ❌ Active — declares 🐦 with 0 tests |
| pytest works in venv | ✅ 485 passed / 38 failed / 183 errors (Mac Mini, Feb 23) |
| Playwright installed | ❌ Not in venv yet |
| App serving locally | ❓ Unknown — Flask may not boot in dev mode without Docker |
| Loop actually iterates | ❌ **Never happened** |

---

## THE PLAN — 5 STEPS TO A REAL DEV LOOP

Everything below happens on the Mac Mini, in the venv, under Claude's control. No Docker. No iMac. Terminal only.

### STEP 1: Fix B-018 — The False Positive

The loop lies. Fix it.

In `devops/scripts/dev_loop.py`, function `phase_report()`:

```python
# CURRENT (broken):
tests_green = test.get("failed", 0) == 0 and test.get("errors", 0) == 0

# FIXED:
tests_green = (
    test.get("total", 0) > 0
    and test.get("failed", 0) == 0
    and test.get("errors", 0) == 0
)
```

Same for `all_green` — it should require `tests_total > 0`. If browser is skipped, that's OK (browser tests are Phase 2 on real hardware). But test count must be positive.

Also in `all_green`:
```python
# CURRENT:
all_green = tests_green and (browser_green or browser.get("skipped"))

# FIXED:
all_green = tests_green and (browser_green or browser.get("skipped"))
# tests_green already requires total > 0, so this is now honest
```

Reset state:
```bash
python3 devops/scripts/dev_loop.py --reset
```

**Commit:** `fix: dev_loop requires total>0 for green — no more false canary (B-018)`

---

### STEP 2: Get pytest Baseline Solid in venv

Before the loop can iterate meaningfully, we need to know exactly what passes and what fails *in the dev venv on the Mac Mini*.

```bash
cd /Users/geofflyle/GrowDirect/Canary
source venv/bin/activate

# Clean baseline — skip browser tests, skip anything needing Docker
pytest tests/ -m "not browser" --tb=short -q --no-header 2>&1 | tail -30
```

Record: total, passed, failed, errors. This is the starting line.

**The 183 errors from Feb 23 were mostly:**
- `test_rls_isolation.py` — needs real Postgres (expected to fail in SQLite dev mode)
- App factory cascades — Flask app not fully bootstrapping

**Jeremy's job:** Categorize the failures:
- **Fixable in dev (no Docker needed):** import errors, wiring issues, missing fixtures, bad test assumptions → fix these
- **Requires Postgres (skip for now):** RLS tests, trigger tests, anything that needs real DB → mark with `@pytest.mark.postgres` or `@pytest.mark.skip(reason="requires postgres")`
- **Requires running app (skip for now):** e2e tests that call localhost → mark with `@pytest.mark.e2e`

**Goal:** Get a clean pytest run where everything that *can* pass in dev *does* pass, and everything that can't is explicitly skipped with a reason. No mystery failures.

**The number that matters:** How many tests pass in dev mode? That's what the dev loop iterates against.

---

### STEP 3: Make the Dev Loop Actually Loop

The loop ran `--once`. It needs to run `--max-iter 5` (or 10) and actually:
1. SCAN — find gaps
2. TRIAGE — route to Qwen
3. BUILD — Qwen writes code
4. TEST — pytest runs
5. REPORT — log results
6. **SLEEP → GO BACK TO STEP 1**

Test this:
```bash
# Local only, no browser, 5 iterations, verbose
python3 devops/scripts/dev_loop.py \
    --local-only \
    --no-browser \
    --max-iter 5 \
    --watch \
    --sleep 10
```

**What to watch for:**
- Does it actually loop? (runs iteration 2, 3, 4, 5?)
- Does SCAN find real gaps each iteration?
- Does TRIAGE route tasks to Qwen?
- Does Qwen produce code that gets written?
- Does pytest run after each build phase?
- Does the test count change between iterations?
- Does LOOP_REPORT.md accumulate rows?

**If it doesn't loop:** Debug why. Common issues:
- Exits after iteration 1 because `all_green` is still broken
- Qwen not running (`ollama serve` not started)
- SCAN finds 0 gaps (all gaps already addressed) → skip_build → test → report → but should still iterate if tests aren't green
- Exception somewhere kills the loop

**If it loops but doesn't improve:** That's OK for now — it means the BUILD phase isn't targeting the right gaps, or Qwen's output isn't passing VERIFY. That's iteration 2 of the dev loop improvement. The first goal is: **it loops**.

---

### STEP 4: Tune the Loop to Actually Improve Test Counts

Once the loop runs multiple iterations, watch what happens:

- If test count stays flat: SCAN→TRIAGE isn't finding actionable gaps, or BUILD isn't producing code that helps
- If test count goes up: 🎉 the machine is working
- If test count goes DOWN: BUILD is breaking things — need better VERIFY gates

**Specific things to tune:**
1. **SCAN gap detection** — does `auto_scan.py` correctly identify the 20 orphan routes and other gaps?
2. **TRIAGE→prompt mapping** — `gap_to_prompts` dict maps gap types to prompt files. Are the right prompts getting triggered?
3. **Qwen output quality** — is Qwen 7B actually producing usable test stubs? If not, does it escalate to 14B?
4. **VERIFY commands** — do prompt files have working verify commands? If not, the loop can't tell if BUILD succeeded.

**The metric:** After 5 iterations, LOOP_REPORT should show test counts trending up (or at least stable, not down).

---

### STEP 5: Make It Runnable from Terminal

When Steps 1–4 are done, Jeffe should be able to do this:

```bash
cd /Users/geofflyle/GrowDirect/Canary
source venv/bin/activate
python3 devops/scripts/dev_loop.py --local-only --no-browser --max-iter 10 --watch
```

And walk away. Come back to a LOOP_REPORT with 10 rows showing real test counts.

That's the deliverable. One command. It loops. Tests run. Numbers move.

---

## WHAT'S EXPLICITLY NOT IN THIS WORK ORDER

| Item | Why not yet |
|---|---|
| iMac Docker deployment | Dev loop needs to work first. Commit the package, pull to iMac later. |
| Playwright browser tests | Phase 2 — after the dev loop proves tests work, we add browser. |
| Jim's QA test scenarios | Gated behind working dev loop + real hardware. |
| CRDM-G2, G3 migrations | Secondary — can happen inside loop iterations. |
| cash_variance_cents | Day 3 punch list — after loop works. |
| RLS policy validation | Needs real Postgres — iMac Phase 2. |

---

## SESSION OUTPUT FORMAT

```
# JEREMY SESSION OUTPUT — Feb [date], 2026

## B-018 Fix
- False positive fixed: [yes/no]
- Loop state reset: [yes/no]

## pytest Baseline (dev venv, Mac Mini)
- Total: [n] | Passed: [n] | Failed: [n] | Errors: [n] | Skipped: [n]
- Tests marked @postgres (skipped in dev): [n]
- Tests marked @e2e (skipped in dev): [n]
- Fixable failures fixed this session: [list]

## Dev Loop Iterations
- Iterations run: [n]
- Loop actually looped: [yes/no]
- Qwen available: [yes/no, which model]
- SCAN found gaps: [yes/no, count per iteration]
- BUILD produced code: [yes/no]
- Test count trend: [iteration 1: n, iteration 2: n, ...]
- LOOP_REPORT rows: [n]

## What Broke / What Needs Fixing
- [any loop issues, Qwen issues, scan issues]

## Blockers for TRIAGE.md
- [anything new]
```

---

## THE RULE

The dev loop must actually loop — in dev, in the venv, from terminal — before we commit and ship to real hardware. No skipping to iMac. No skipping to Jim. Get the machine running first.

---

*Issued by ALX. Jeremy owns execution. Report back on completion or if blocked.*
*Canary LP | Confidential*
