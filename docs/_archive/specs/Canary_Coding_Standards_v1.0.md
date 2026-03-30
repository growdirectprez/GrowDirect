---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary Coding Standards v1.0

**Date:** February 22, 2026
**Author:** Eva (Program Manager), informed by auto_scan.py findings
**Status:** ACTIVE — all new code must comply
**Enforced by:** Jim (QA gate), auto_scan.py (automated), Jeremy (code review)

---

## Why This Exists

The Feb 22 codebase scan (`auto_scan.py`) revealed structural debt that makes regression triage slow and error-prone:

- **71 of 152 routes** have zero test coverage (47%)
- **611 of 658 tests** lack AC references — when they fail, nobody knows which feature broke
- **29 of 60 models** have no schema validation tests
- **5 Chirp rules** have no test coverage at all
- **Legacy/wired blueprint duplicates** create shadow routes where changes don't propagate

These standards exist to stop the gap from growing. Every new line of code should make traceability *better*, not worse.

---

## 1. Every Route Gets a Test

**Rule:** No route is merged without at least one test that hits it.

**Minimum test for any route:**
```python
def test_my_route_not_500(self, client):
    """E1-F5-AC1: Alert detail endpoint returns valid response."""
    resp = client.get("/alerts/1")
    assert resp.status_code != 500
```

**What counts:** A smoke test (non-500) is the minimum. Functional tests with assertions on response body are preferred. Either way, the scanner must stop flagging it as an orphan.

**Enforcement:** `auto_scan.py` ORPHAN_REPORT §1 tracks this. The count must go DOWN with every sprint, never up.

---

## 2. Every Test Gets an AC Reference

**Rule:** Every test function or test class must reference its Acceptance Criterion in the docstring.

**Format:** `E{epic}-F{feature}-AC{number}` or at minimum `E{epic}-F{feature}`

```python
class TestWebhookEndpoint:
    """E1-F1: Webhook HMAC validation."""

    def test_webhook_rejects_bad_hmac(self, client):
        """E1-F1-AC2: Rejects requests without valid HMAC signature."""
        ...
```

**Why:** When a test fails in CI, the AC reference tells you *instantly* which feature is broken. Without it, you're reading code to figure out what broke — that's triage time that compounds.

**Cross-cutting tests** that don't map to a single feature use these tags:
- `BRAND` — brand compliance (colors, fonts, logos)
- `UI` — browser rendering
- `INFRA` — infrastructure/scaffold health
- `SMOKE` — basic health checks
- `REGRESSION` — regression-specific tests

**Enforcement:** `auto_scan.py` ORPHAN_REPORT §4 tracks this. The `inject_ac_refs.py` script (Qwen-generated) can batch-tag existing tests.

---

## 3. One Blueprint, One Source of Truth

**Rule:** No route may exist in more than one blueprint file.

**The problem:** The scanner found routes duplicated across legacy (`alerts.py`) and wired (`alerts_wired.py`) files. Changes to one don't propagate to the other. This is how regressions hide.

**The standard:**
- `*_wired.py` files are the **canonical source** (these use the new service layer and db_session)
- Legacy `*.py` blueprint files (alerts.py, fox.py, chirp.py, employees.py, locations.py, merchants.py) are **deprecated**
- No new routes in legacy files. Period.
- When touching a legacy route, migrate it to the wired version and delete the legacy copy
- `wsgi.py` legacy routes stay until the wired blueprints are fully registered and tested

**Enforcement:** `detect_duplicates.py` (Qwen prompt S06) generates the DUPLICATES.md report. The count of duplicate routes must reach zero before alpha gate.

---

## 4. Models Get Schema Tests

**Rule:** Every SQLAlchemy model class must have a test that validates:
1. Import succeeds
2. `__tablename__` matches expected value
3. At least 2-3 key columns exist

```python
def test_alert_history_schema(self):
    """E1-F5-AC3: AlertHistory model has correct schema."""
    from canary.models.app.detection import AlertHistory
    assert AlertHistory.__tablename__ == "alert_history"
    cols = [c.key for c in AlertHistory.__table__.columns]
    assert "alert_id" in cols
    assert "old_status" in cols
```

**Why:** Schema drift is silent. A column rename or dropped table doesn't throw an error until runtime. These tests catch it at build time.

**Enforcement:** `auto_scan.py` ORPHAN_REPORT §3 tracks untested models.

---

## 5. Chirp Rules Are Testable Contracts

**Rule:** Every Chirp detection rule (C-xxx) must have:
1. A test that triggers it (positive case)
2. A test that confirms it doesn't fire below threshold (negative case)
3. A docstring referencing its rule ID

```python
class TestCashVarianceC102:
    """E1-F6-AC2: Cash drawer variance detection (C-102)."""

    def test_high_variance_triggers(self, chirp):
        """C-102: Variance > $5 should trigger alert."""
        ...

    def test_normal_variance_no_alert(self, chirp):
        """C-102: Variance < $5 should NOT trigger."""
        ...
```

**Why:** A Chirp rule without tests is a detection blindspot. If the rule logic changes and no test validates it, merchants lose coverage silently.

**Enforcement:** `auto_scan.py` ORPHAN_REPORT §2 tracks uncovered rule IDs.

---

## 6. The Wiring Chain Must Be Traceable

**Rule:** For any feature, you should be able to follow the chain:

```
PRD (AC) → Route → Service → Model → Chirp Rule → Test
```

If any link is missing, the feature is incomplete. The WIRING_MAP.md (generated by `generate_wiring_map.py`) makes this visible.

**New feature checklist:**
- [ ] PRD has acceptance criteria (Eva writes, Jim signs off)
- [ ] Route exists in a `*_wired.py` blueprint
- [ ] Route calls a service (not raw SQL or direct model access)
- [ ] Service uses models via `db_session` helper
- [ ] If detection-related: Chirp rule ID assigned and catalogued
- [ ] Test exists with AC reference in docstring
- [ ] Template exists (if user-facing) and is referenced by route

---

## 7. File Naming and Location

**Routes:**
- New blueprints: `canary/blueprints/{module}_wired.py`
- Legacy (deprecated): `canary/blueprints/{module}.py`

**Models:**
- App database: `canary/models/app/{domain}.py`
- Sales database: `canary/models/sales/{domain}.py` (APPEND-ONLY)
- Metrics database: `canary/models/metrics/{domain}.py`
- Fox: `canary/models/fox/{domain}.py`

**Services:**
- `canary/services/{domain}_service.py` or `canary/services/{domain}/`

**Tests:**
- Unit: `tests/test_{domain}.py`
- E2E: `tests/e2e/test_{epic_id}_{domain}.py` (e.g., `test_e1_chirp.py`)
- Browser: `tests/browser/test_browser_{domain}.py`
- Integration: `tests/integration/test_{concern}.py`

**Prompts (Qwen work orders):**
- `devops/prompts/{sprint_or_category}/{NN}_{short_name}.md`

---

## 8. Commit Message Convention

Format: `{type}({scope}): {description}`

Types:
- `feat` — new feature or endpoint
- `fix` — bug fix
- `test` — adding or fixing tests
- `docs` — documentation only
- `refactor` — code change that doesn't add feature or fix bug
- `chore` — build process, dependency, config
- `schema` — database schema changes (migrations)

Scope matches the module: `chirp`, `fox`, `alerts`, `auth`, `models`, `routes`, `e2e`, `browser`

Examples:
```
feat(chirp): add C-401 HIGH_VOID_RATE detection rule
test(fox): add schema validation for FoxCaseAction model
fix(alerts): wire acknowledge route to alerts_wired.py
schema(sales): add transaction_type enum to transactions table
refactor(routes): remove legacy alerts.py duplicate routes
```

---

## 9. Scanner Integration (Continuous)

**Run the scanner after every meaningful code change:**

```bash
# Quick check (5 seconds, no LLM)
python3 devops/scripts/auto_scan.py

# Or via the runner
./devops/scripts/scan_runner.sh --scan-only
```

**Track these metrics sprint-over-sprint:**

| Metric | Feb 22 Baseline | Target (Alpha Gate) |
|--------|----------------|---------------------|
| Routes without tests | 71 | 0 |
| Tests without AC refs | 611 | < 100 |
| Chirp rules without tests | 5 | 0 |
| Models without tests | 29 | 0 |
| Duplicate routes | TBD (S06) | 0 |

**The numbers go down. Never up. That's the rule.**

---

## 10. INSERT-Only Tables — No Exceptions

**Rule:** Sales database tables and Fox evidence tables are APPEND-ONLY.

- No `UPDATE` statements on `canary_sales` tables
- No `DELETE` statements on `canary_sales` tables
- `fox_evidence` and `fox_evidence_access_log` are INSERT-ONLY with hash chain verification
- PostgreSQL triggers enforce this at the database level (migration `001_insert_only_triggers.py`)
- Soft-delete pattern (db_status/db_effective_from/to) for operational tables in `canary_app`

**Why:** Evidentiary integrity. If we accuse someone, we have to be sure and have the facts. Hash-chained, immutable transaction logs are the foundation of Fox case management and any law enforcement referral.

---

## Running the Full Pipeline

```bash
# Phase 1: Scan (Python only, ~5 seconds)
./devops/scripts/scan_runner.sh --scan-only

# Phase 2: Generate gap-closure code via Qwen ($0, local)
./devops/scripts/scan_runner.sh --analyze

# Review outputs
cat devops/scan/ORPHAN_REPORT.md      # What's broken
cat devops/scan/TRACEABILITY_MATRIX.md # Full map
cat devops/scan/WIRING_MAP.md          # Feature → code chains
cat devops/scan/DUPLICATES.md          # Shadow routes
```

---

*"If it doesn't work on the dev sandbox, it doesn't work anywhere."* — Jeffe, Feb 20, 2026
