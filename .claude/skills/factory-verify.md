---
name: factory-verify
roles-primary: [Jeremy]
roles-assist: [Jim]
stage: verify
description: |
  Full test suite execution and regression detection. Runs all tests, checks migration validity, confirms no regressions from assembly.
---

# factory-verify — Verification

## Run the full test suite

```bash
python3 -m pytest tests/ -v
```

Show the output. Do not summarize — paste the actual results. Evidence before assertions.

## Check for regressions

Count tests before and after. Any test that was passing before and is now failing = regression. Fix it before moving on.

## Verify new code has tests

For every new file or function added during assembly:
- Is there a corresponding test?
- Does the test cover the happy path AND at least one error path?

If new code has no test, write it now.

## Check migrations

If any models changed:
```bash
docker exec <appname>_flask alembic upgrade head
```

Must succeed with no errors. If migration is missing, generate it:
```bash
docker exec <appname>_flask alembic revision --autogenerate -m "description"
```
Review the generated migration before committing — autogenerate misses some things.

## Check git diff

```bash
git diff HEAD~<n> --stat
```

Does the set of changed files match what the blueprint planned? Unexpected files changed = investigate.

## Report format

```
Tests: [N] passed, [N] failed, [N] skipped
New tests: [N]
Regressions: none / [list any]
Migrations: [applied / not needed]
Diff: [matches plan / deviations noted]
```

Do not proceed to QA with any failures.
