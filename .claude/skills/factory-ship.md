# factory-ship

## Deployment Preparation

1. Run full test suite one final time: `pytest -v`
2. Check migrations: `alembic upgrade head` succeeds cleanly
3. Check Docker build: `docker compose build` succeeds
4. Run smoke test against Docker stack
5. Review all commits — are messages clear and linked to GRO issue?
6. Update changelog if one exists
7. Tag the release if appropriate

Ship is done when the code is ready for production deployment.
