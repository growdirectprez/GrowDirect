---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Closed-Loop Dev Loop on Real Hardware
*Issued by ALX · February 24, 2026 · Priority: 🔴 CRITICAL PATH*
*Supersedes: WORKORDER_Jeremy_Day3_Sprint5Ph2.md*

**Jeffe directive:** Jim does not touch QA test scenarios until the dev loop is executing closed-loop testing on real hardware with the front end up. No exceptions.

**The goal is simple:** `dev_loop.py` runs on the iMac, pytest passes against real Postgres, Playwright merchant journey executes against the live front end, and the Rooster can actually see screenshots of a working app. Until that's true, nothing goes to Jim.

---

## THE CRITICAL PATH (in order — don't skip ahead)

### STEP 1: Fix dev_loop.py False Positive (B-018)
**What's broken:** `phase_report()` declares ALL GREEN when `tests_total == 0`. It checks `failed == 0 and errors == 0` but doesn't check `total > 0`. Iteration 1 already logged a false 🐦 CANARY SINGS with zero tests.

**The fix** (in `devops/scripts/dev_loop.py`, `phase_report()` function):

Change this logic:
```python
tests_green = test.get("failed", 0) == 0 and test.get("errors", 0) == 0
```

To:
```python
tests_green = (
    test.get("total", 0) > 0
    and test.get("failed", 0) == 0
    and test.get("errors", 0) == 0
)
```

Same for browser:
```python
browser_green = (
    browser.get("total", 0) > 0
    and browser.get("failed", 0) == 0
    and not browser.get("skipped")
)
```

Also reset the loop state so it doesn't carry the false positive forward:
```bash
python3 devops/scripts/dev_loop.py --reset
```

**Commit:** `fix: dev_loop false positive — require total>0 for green (B-018)`

---

### STEP 2: Get the App Booting on iMac Docker (S5-07)
**Prereq:** Phase 1 Boot ✅ DONE — 12 Docker services healthy.

Run Alembic migrations against real Postgres on the 3-database architecture. Eva's full brief is at `Canary_IP/Markdown/Sessions/Jeremy_Phase2_iMac_Brief_2026-02-23.md`.

```bash
docker exec -it canary_flask bash
cd /app

# canary_app migrations
alembic -c canary/migrations/alembic.ini upgrade head

# canary_sales migrations
alembic -c canary/migrations/sales/alembic.ini upgrade head

# canary_metrics migrations
alembic -c canary/migrations/metrics/alembic.ini upgrade head
```

**Known risk:** Tables may not exist. If `relation does not exist`:
```bash
alembic -c canary/migrations/alembic.ini revision --autogenerate -m "initial_canary_app_tables"
alembic -c canary/migrations/alembic.ini upgrade head
```

Or fallback: `Base.metadata.create_all(engine)` per Eva's brief.

**Gate:** All three databases have tables. `SELECT count(*) FROM pg_tables WHERE schemaname='public';` returns non-zero for each.

---

### STEP 3: Validate Triggers on Real Postgres (S5-08 + S5-09)
Run the INSERT-only trigger tests and hash chain verification from Eva's brief against real Postgres. This proves your P0-1/P0-2/P0-3 migrations actually work on hardware, not just in code review.

```bash
# Should FAIL with CHAIN OF CUSTODY VIOLATION
docker exec canary_postgres psql -U canary -d canary_app -c \
  "UPDATE fox_evidence SET evidence_type = 'tampered' WHERE id = 'test-001';"

# Should FAIL with IMMUTABILITY VIOLATION
docker exec canary_postgres psql -U canary -d canary_sales -c \
  "UPDATE transactions SET amount_cents = 9999 WHERE id = 'txn-test-001';"
```

Hash chain: INSERT 3 records → `verify_hash_chain()` → valid. Tamper record 2 → catches it.

**Gate:** Triggers fire correctly. Chain verification works. Log the terminal output.

---

### STEP 4: Get Flask Serving the Front End
**What:** The Flask app needs to be serving pages at `http://localhost:5001` (or whatever `CANARY_BASE_URL` is set to) inside the Docker stack.

Verify:
```bash
# From inside the Docker network or the host
curl -s http://localhost:5001/health | python3 -m json.tool

# Check dashboard renders HTML, not a traceback
curl -s http://localhost:5001/dashboard | head -20
```

**If health endpoint returns JSON and dashboard returns HTML:** front end is up.
**If not:** Debug. Common issues:
- Flask not starting (check `docker logs canary_flask`)
- Blueprint registration errors (B-008 — auth double-registration)
- Template not found (Jinja2 paths)
- Static files not mounted

**Gate:** `curl /health` returns 200. `curl /dashboard` returns HTML with "Canary" in it.

---

### STEP 5: Get pytest Running Against Real Postgres
**What:** Run the full test suite against the Docker Postgres, not SQLite.

```bash
# Set the database URL to point at Docker Postgres
export DATABASE_URL="postgresql://canary:password@localhost:5432/canary_app"
export CANARY_ENV="testing"

# Run tests
pytest tests/ --tb=short -q -m "not browser" 2>&1 | tail -30
```

The 183 errors from the Mac Mini session were mostly `test_rls_isolation.py` needing real Postgres. With real Postgres, those should either pass or fail with real errors (not "SQLite doesn't support this").

**Gate:** Test count > 0. Know exactly how many pass, fail, error. The dev_loop needs `total > 0` to be meaningful.

---

### STEP 6: Get Playwright Merchant Journey Executing
**What:** Install Playwright, point it at the running app, run the 5-act merchant journey.

```bash
# Install Playwright in the venv
pip install pytest-playwright
playwright install chromium

# Run the journey (headless for CI, headed if you want to watch)
export CANARY_BASE_URL="http://localhost:5001"
pytest tests/browser/test_merchant_journey.py -m browser --tb=short -v
```

The journey has 5 acts (Connect, Watch, Alert, Investigate, Fox) + a Songbird audit. Many tests use `pytest.xfail` for features not yet wired — that's fine. What matters is:
- No 500 errors
- No Python tracebacks on any page
- Dashboard renders with dark theme
- Screenshots are captured to `test-results/journey-screenshots/`

**Gate:** Browser tests execute. Some may xfail. Zero hard failures. Screenshots exist.

---

### STEP 7: Run dev_loop.py Full Cycle
**What:** With B-018 fixed, app serving, Postgres live, Playwright installed — run the full loop.

```bash
cd /Users/geofflyle/GrowDirect/Canary
python3 devops/scripts/dev_loop.py --once --watch --reset
```

This runs all 7 phases: SCAN → TRIAGE → BUILD → MIGRATE → TEST → BROWSER → REPORT.

**What "done" looks like:**
- `LOOP_REPORT.md` shows an iteration with `T✅ > 0` and `B✅ > 0`
- Screenshots in `test-results/journey-screenshots/`
- No false positive 🐦

If tests fail or browser tests fail — that's expected at this stage. The point is the **loop itself is running closed-loop**. Jeremy iterates from there.

---

## SECONDARY (After the loop is running)

These items from the Day 3 punch list are still owed but are lower priority than getting the loop running:

| Task | Status |
|---|---|
| Verify `cash_variance_cents` computation | ⏳ Day 3 close-out |
| B-020: `employee_id` + `location_id` on `refund_links` | ⏳ CRDM-G2 |
| B-021: `order_id` on `transactions` | ⏳ CRDM-G3 |
| S5-10: RLS policy validation | ⏳ After triggers confirmed |

These can happen inside the dev_loop iteration cycle once the loop is live.

---

## SESSION OUTPUT FORMAT

When done, write to `_ALX/JEREMY_SESSION_OUTPUT_2026-02-2X.md`:

```
# JEREMY SESSION OUTPUT — Feb [date], 2026

## B-018 Fix
- dev_loop.py false positive: [fixed/not fixed]
- Loop state reset: [yes/no]

## iMac Docker Status
- Alembic migrations: [pass/fail — which DBs, table counts]
- Trigger validation: [pass/fail — INSERT-only + hash chain]
- Flask serving: [health endpoint status, dashboard renders]

## Test Suite on Real Postgres
- Total: [n] | Passed: [n] | Failed: [n] | Errors: [n]
- Comparison to Mac Mini baseline (485/755): [better/worse/same]

## Playwright Merchant Journey
- Installed: [yes/no]
- Acts passed: [n/5]
- Acts xfailed: [n]
- Acts hard-failed: [n]
- Screenshots captured: [yes/no, count]

## Dev Loop Full Cycle
- Ran: [yes/no]
- Iteration result: T✅=[n] T❌=[n] B✅=[n] B❌=[n]
- False positive fixed: [confirmed]

## Blockers Encountered
- [any new items for TRIAGE.md]
```

---

## THE RULE

**Jim gets the app when the Rooster can see screenshots of a working merchant journey, not before.**

The dev_loop is the gate. When it runs green — real tests, real browser, real Postgres — then we route to Jim for QA scenarios.

---

*Issued by ALX. Jeremy owns execution. Report back on completion or if blocked.*
*Canary LP | Confidential*
