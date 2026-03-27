# Factory Process

Six stages, always in order. No skipping. Each stage has a defined output — if the output isn't present, the stage isn't done.

## Overview

```
Blueprint → TDD → Assembly → Verify → QA → Ship
```

Every stage gate: the agent does not move to the next stage until the current stage's output is complete and confirmed.

---

## Stage 1: Blueprint

**Skill:** `factory-blueprint`

**What it produces:**
- List of files to be created or modified
- List of routes with method, URL, and purpose
- List of models with fields
- List of tests to be written (by name)
- Scope boundary — what is explicitly NOT in scope

**Example:** "Blueprint for GRO-412: add Farm detail page. Produces: `farms/routes.py` (GET `/farms/<id>`), `templates/farms/detail.html`, `tests/integration/test_farm_routes.py::test_farm_detail`."

---

## Stage 2: TDD

**Skill:** `factory-tdd`

**What it produces:**
- Failing test files for every item listed in the Blueprint
- Tests run and fail for the right reason (not import errors — actual assertion failures or 404s)

**Example:** "Write `test_farm_detail` — POSTs to `/farms/<uuid>`, asserts 200 and farm name in response. Currently returns 404 because route doesn't exist yet."

---

## Stage 3: Assembly

**Skill:** `factory-assembly`

**What it produces:**
- Implementation code that makes the failing tests pass
- No test modifications — if a test needs changing, stop and raise it

**Example:** "Add `GET /farms/<id>` route, `farm_service.get_farm()`, and `detail.html` template. Tests that were failing in TDD now pass."

---

## Stage 4: Verify

**Skill:** `factory-verify`

**What it produces:**
- Full test suite green (unit + integration + smoke)
- No regressions — existing tests still pass
- Output: `pytest` run log showing 0 failures

**Example:** "Run `pytest -v`. 47 passed, 0 failed. Farm detail route, service, and template all covered."

---

## Stage 5: QA

**Skill:** `factory-qa`

**What it produces:**
- Security checklist sign-off: auth on every non-public route, no secrets in code, CSRF enabled
- Quality checklist sign-off: no raw SQL, no `Column()` patterns, imports ordered, no orphan files
- Any issues found are new Linear issues — not patched inline unless trivial

**Example:** "QA pass: `@login_required` confirmed on farm detail route. No hardcoded credentials. `Mapped[]` syntax used throughout. LGTM."

---

## Stage 6: Ship

**Skill:** `factory-ship`

**What it produces:**
- Deployable artifact: clean git commit with GRO number in message
- Post-mortem written to `docs/post-mortems/<GRO-NNN>-<slug>.md`
- Migration script if schema changed (`alembic revision --autogenerate`)

**Example:** "Commit `feat: add farm detail page (GRO-412)`. Post-mortem written. Alembic migration generated and tested."
