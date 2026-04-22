---
name: factory-tdd
roles-primary: [Jeremy]
roles-assist: [Tom]
stage: tdd
description: |
  Test-first development workflow. RED-GREEN-REFACTOR cycle with test naming conventions and coverage requirements.
---

# factory-tdd — Test-First Development

## The rule

Write the test before writing the implementation. If the test passes before you write any code, the test is wrong or the feature already exists — stop and investigate.

## Cycle for each behavior

1. **Write one test** in the appropriate file under `tests/`
   - Unit tests: `tests/unit/test_<model_or_service>.py`
   - Integration tests: `tests/integration/test_<route_or_feature>.py`
   - Smoke tests: `tests/smoke/test_smoke.py`

2. **Run it — confirm it fails**
   ```bash
   python3 -m pytest tests/path/test_file.py::test_name -v
   ```
   Acceptable failures: `ImportError`, `AttributeError`, assertion failure. A passing test at this stage = broken test.

3. **Write minimal implementation** — only enough code to make this one test pass. No extras.

4. **Run it — confirm it passes**
   ```bash
   python3 -m pytest tests/path/test_file.py::test_name -v
   ```

5. **Run smoke tests** to catch regressions
   ```bash
   python3 -m pytest tests/ -k smoke -v
   ```

6. **Commit**
   ```bash
   git commit -m "test: <behavior description> (GRO-XXX)"
   ```

Repeat for each behavior in the blueprint.

## Test naming

`test_<what>_<condition>_<expected>`

Examples: `test_login_valid_email_redirects_to_dashboard`, `test_create_member_missing_email_returns_422`

## Coverage requirements

Every feature needs at minimum:
- Happy path (valid input, expected success)
- Validation error (bad input, expected failure)
- Auth required (unauthenticated request returns 302 to login)
- Not found (missing UUID returns 404)

## Fixtures

Use `conftest.py` fixtures — don't create test databases or test users inline.
Standard fixtures: `app`, `client`, `authenticated_client`, `db_session`, sample model objects.

## Split rule

"and" in a test name = two behaviors = two tests. Split it.

## Gate

Do NOT move to factory-assembly until all tests are written and failing for the correct reason.
