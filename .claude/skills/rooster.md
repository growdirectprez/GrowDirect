---
name: rooster
description: |
  E2E Testing skill for GrowDirect apps. Use whenever anyone says: "run e2e",
  "test end-to-end", "run tests", "health check", "smoke test", "is the site up",
  "validate the build", "test [feature]", "run rooster". Three modes: Quick Crow
  (health check), Feature Patrol (API-level E2E), Full Strut (Playwright browser).
  Adapt test targets and epic references to the app being tested.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
---

# The Rooster — E2E Testing Skill

The Rooster is the platform's test engineer. It has four layers: context processor
integrity (unit), a quick crow (health check), a feature patrol (API-level E2E),
and a full strut (Playwright browser tests). Every test maps back to an Epic,
Feature, and Acceptance Criterion for traceability.

## Three Modes

### Mode 1: Quick Crow (Health Check)

Trigger: "check the app", "is it up", "health check", "smoke test", "quick check"

This is the 30-second "is it alive" check. Run in order, stop on first failure:

1. **Health Endpoint**: `curl -s http://localhost:<PORT>/health`
2. **Login Page**: check auth route returns 200
3. **Dashboard**: check main route returns 200 or 302
4. **Static Assets**: CSS and JS return 200
5. **Key Routes**: hit critical endpoints — all should return 200 or 302
6. **Error Log Scan**: check for tracebacks in Flask output

Report as:
```
ROOSTER QUICK CROW — [timestamp]
Target: http://localhost:<PORT> | Version: X.X.X
──────────────────────────────────────
[status] Health endpoint     [status] Login page
[status] Dashboard           [status] Static assets
[status] Key routes (N/N)    [status] No errors in log
──────────────────────────────────────
RESULT: [ALL CLEAR / FAILURES] (N/N)
```

### Mode 2: Feature Patrol (Epic-Specific E2E)

Trigger: "run e2e", "test [feature]", "full test"

Generate and run pytest-based E2E tests for a specific Epic or feature. Tests
live in `tests/e2e/` and map directly to PRD acceptance criteria.

**Stack:**
- pytest + requests for API-level E2E (fast, no browser overhead)
- Playwright (sync API) for browser/UI tests when needed
- Test against sandbox credentials from `.env`
- Never run destructive operations against production data

**Conventions:**
- Filename: `test_e2e_[epic_or_feature].py`
- Markers: `@pytest.mark.e2e`, `@pytest.mark.smoke`, plus epic-specific markers
- Each test docstring includes the AC reference: `"""E1-F2-AC3: Description."""`

### Mode 3: Full Strut (Playwright Browser Tests)

Trigger: "browser test", "full strut", "visual test", "playwright"

Real Chromium browser tests (headless by default). Catches JS errors, CSS failures,
broken forms, missing elements.

```bash
# All browser tests (headless)
pytest tests/browser/ -m browser -v

# Watch the browser (debugging)
pytest tests/browser/ -m browser --headed -v
```

**Screenshots:** Failed tests auto-capture to `test-results/screenshots/FAIL_*.png`

## Running Tests

```bash
# Quick Crow (health check only)
python3 -m pytest tests/e2e/test_e2e_health.py -v

# Full patrol — all E2E tests
python3 -m pytest tests/e2e/ -v --tb=short

# Specific epic
python3 -m pytest tests/e2e/ -m <epic> -v

# With coverage
python3 -m pytest tests/e2e/ -v --cov=<appname> --cov-report=term-missing
```

## Report Format

```
ROOSTER PATROL REPORT — [timestamp]
Target: http://localhost:<PORT> | Version: X.X.X
═══════════════════════════════════════════════════
Epic E0 — Platform Foundation       N/N   [status]
Epic E1 — Core Detection            N/N   [status]
Cross-Cutting — Audit Integrity     N/N   [status]
═══════════════════════════════════════════════════
TOTAL: N/N passed | N pending | N skipped
RESULT: [status] — [summary]
═══════════════════════════════════════════════════
```

## Safety Rules

- Never execute real transactions — always use sandbox credentials
- Test data should be clearly marked (IDs prefixed with `test-*`)
- Never modify `.env` or production database
- If a test requires destructive setup, use a separate test database

## After Running

1. Analyze failures — categorize as code bug vs. unimplemented feature vs. test issue
2. Propose fixes for code bugs with specific file + line references
3. Mark unimplemented features as "pending" (not "failed") in the report
4. If all tests pass, output the full report and suggest committing
