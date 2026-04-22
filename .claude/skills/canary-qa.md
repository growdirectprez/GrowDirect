---
name: canary-qa
roles-primary:[Compliance]
roles-assist:[QA]
stage: qa
description: |
  Diff-aware QA testing for Canary. Use when asked to "qa", "test this", "verify
  the branch", "check what changed", or before shipping. Four modes: diff-aware
  (automatic on feature branches), full (systematic all-route sweep), quick
  (30-second smoke), regression (compare against baseline). Produces structured
  report with health score, row counts, and pipeline proof.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Write
---

# Canary QA — Diff-Aware Quality Assurance

> "We treat data integrity with the utmost seriousness. This is people's lives
> and jobs we are analyzing. If we accuse someone, we have to be sure and have
> the facts."

## Overview

Test the app like a merchant depends on it — because they do. Don't just run
pytest and call it done. Prove the data flows, prove the routes respond, prove
the pipeline delivers.

**Announce at start:** "I'm using canary-qa to test this work."

---

## Setup

```bash
# Confirm the stack is running
curl -sf http://localhost:5001/health | python3 -m json.tool || echo "APP NOT RUNNING"
docker compose -f docker-compose.dev.yml ps

# Create report directory
REPORT_DIR="docs/qa-reports"
mkdir -p "$REPORT_DIR"
```

If the app isn't running, stop. QA without a running app is fiction.

---

## Mode Selection

### Diff-Aware (default on feature branches)

When you're on a feature branch and the user says "qa" or "test this":

**1. Analyze the branch diff:**
```bash
git diff main...HEAD --name-only
git log main..HEAD --oneline
git diff main...HEAD --stat
```

**2. Classify changed files -> affected surfaces:**

| Changed File Pattern | Affected Surface | How to Test |
|---|---|---|
| `canary/services/<svc>/routes.py` | HTTP routes | `curl` each route, verify JSON contract |
| `canary/services/<svc>/service.py` | Business logic | `pytest tests/unit/test_<svc>*` |
| `canary/services/<svc>/models.py` | Data persistence | Integration test + row count check |
| `canary/templates/**/*.html` | UI rendering | `curl` the page, check 200 + no Jinja errors |
| `canary/models/*.py` | Schema / ORM | Check migrations, verify table structure |
| `canary/static/**` | Frontend assets | `curl` the asset path, check 200 |
| `tests/**` | Test infrastructure | Run the changed tests directly |
| `alembic/**` | Migrations | Verify migration applied, schema matches model |
| `canary/db/**` | DB session/connection | Health check + basic query test |

**3. Test each affected surface** with targeted tests, route checks, data integrity checks, and log scans.

**4. Cross-reference with commit messages** to understand intent.

**5. Check pipeline node boundaries** — verify data flows across node boundaries.

**6. Check adjacent routes for regressions.**

**7. Report scoped to the branch.**

### Full (systematic sweep)

Test every registered route. Use when preparing for deploy or after major refactor.

```bash
python3 -c "
from canary.app import create_app
app = create_app()
for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    if rule.endpoint != 'static':
        print(f'{rule.methods} {rule.rule} -> {rule.endpoint}')
"
```

### Quick (30-second smoke)

```bash
curl -sf http://localhost:5001/health | python3 -m json.tool
python3 -m pytest tests/unit/ -q --tb=no
python3 -m pytest tests/smoke/ -q --tb=no --timeout=30
```

### Regression (compare against baseline)

Run full mode, load `baseline.json` from a previous run, diff for fixed/new issues.

---

## The Lazy Pipe Detector

For every route that returns JSON, verify the response is real — not hardcoded,
not stubbed, not TODO'd.

**A route that returns hardcoded JSON is not done.**
**A service that doesn't persist is not done.**

---

## Health Score Rubric

Compute each category score (0-100), weighted average:

| Category | Weight |
|----------|--------|
| App Health | 20% |
| Test Suite | 25% |
| Route Coverage | 20% |
| Data Integrity | 20% |
| Pipeline Completeness | 15% |

| Score | Rating | Ship? |
|-------|--------|-------|
| 90-100 | Excellent | Yes |
| 75-89 | Good | Yes, with notes |
| 50-74 | Needs Work | Fix first |
| < 50 | Critical | Do not ship |

---

## Report Format

Save report to: `docs/qa-reports/qa-report-{branch}-{YYYY-MM-DD}.md`

Include: changes tested, route verification table, data integrity table,
test results, issues found, lazy pipe check, health score breakdown,
and recommendation (SHIP IT / FIX FIRST / BLOCK).

---

## Integration with Other Skills

- **Before canary-ship:** Run canary-qa in diff-aware mode. Ship should not proceed if health score < 75.
- **After canary-assembly:** Run canary-qa to verify the assembled work.
- **With canary-verify:** canary-qa is the broader sweep; canary-verify is the per-claim evidence gate.
- **With canary-deploy:** Run canary-qa quick mode after deploy to verify QA environment health.

---

*Canary QA v1.0 — Diff-Aware Quality Assurance*
