---
type: session
domain: business
status: active
created: 2026-03-02
updated: 2026-03-19
---
# Session Output — 2026-03-02 Board Triage

## What was done

### Linear board triage
- Reviewed all Canary LP backlog issues in order
- **GRO-11** (Production heartbeat) — **Canceled**. Nowhere near production, premature.
- **GRO-29** (20 routes without tests) — **Canceled**. All tests wiped (see below). Will rewrite against stable codebase post-UAT.

### GRO-32: SQLite remnants — Config layer cleanup (Done)
Edited 5 critical config files to remove all SQLite references:

| File | Change |
|------|--------|
| `.env` | `DATABASE_URL` → `postgresql://canary:canary@localhost:5432/canary_dev` with multi-env comments |
| `.env.template` | Same — placeholder with dev/QA/hosted examples |
| `canary/config.py` | Removed SQLite fallback default, updated docstrings, `TestingConfig` now uses PostgreSQL |
| `canary/services/db_session.py` | Rewrote to PostgreSQL-only — removed SQLite toggle, `CANARY_DB_BACKEND` env var, all SQLite paths |
| `devops/docker-compose.qa.yml` | Added `postgres:16-alpine` service, app + test containers depend on it with health checks |

**Note:** Issue also mentions app code docstrings (auth/services, fox/services, fox/models, database.py) and test files still referencing SQLite. App docstrings not yet cleaned. Tests wiped entirely (see below).

### Test suite wipe
- Deleted all 53 test files (147 total with pycache) from `tests/`
- Left clean skeleton: `tests/__init__.py`, `tests/conftest.py`, `tests/unit/__init__.py`
- Rationale: All tests were broken, written against SQLite patterns. Plan is stabilize → UAT → write fresh unit tests against clean PostgreSQL codebase.

## Where we stopped
- **GRO-18** (Multi-tenant partition architecture) — needs Tom + PhD input. Comment left on issue. Stays in Backlog.
- Next items to triage: GRO-20, GRO-24, GRO-37, then the rest of backlog

## Remaining backlog (in order)
1. GRO-18 — Multi-tenant partition architecture (High) — waiting on Tom + PhD
2. GRO-20 — Square SDK → CRDM alignment audit (High)
3. GRO-24 — 7 domains on Cloudflare — DNS config (High)
4. GRO-37 — Two template directories — consolidate (Medium)
5. GRO-27 — Square Labor API polling adapter redesign (Medium)
6. GRO-26 — Square Bitcoin onboarding test (Medium)
7. GRO-25 — Founder origin story — evidence recovery (Medium)
8. GRO-23 — Trademark search — elJeffe (Medium)
9. GRO-22 — Grafana AGPL license review (Medium, due 3/31)
10. GRO-31 — Password vault selection (Medium)
11. GRO-30 — Airflow 3.0 migration (Low)
