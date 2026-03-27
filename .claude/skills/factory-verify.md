# factory-verify

## Verification

1. Run full test suite: `pytest -v` — all must pass
2. Check for regressions: did any existing tests break?
3. Verify integration: do the new routes work with existing services?
4. Check database: run `alembic upgrade head` if migrations were added
5. Check Docker: does `docker compose up` still work?
6. Manual smoke test: hit the new URLs, verify responses

Report: "[N] tests pass, [N] new, [N] existing, no regressions"
