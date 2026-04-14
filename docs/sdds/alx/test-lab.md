# Test Lab

## Purpose

The Test Lab is a developer-facing subsystem inside Canary's Ops Console that generates test data and verifies that the full Canary pipeline — Square webhook ingestion, TSP parsing, Chirp rule evaluation, alert creation, Fox case escalation — responds correctly to known transaction patterns. It has two execution modes: Scenario Fire (real Square sandbox API calls that trigger webhooks back through the production code path) and Scenario Runner (synthetic data inserted directly into PostgreSQL for dashboard verification). A Sandbox Seeder prepopulates the Square sandbox with team members and catalog items. Scenario Verify confirms expected outcomes via parameterized SQL after a fire.

**Service type:** App Service (Platform/Canary)
**Code location:** `Canary/canary/services/scenario_fire.py`, `Canary/canary/services/scenario_runner.py`, `Canary/canary/services/scenario_verify.py`, `Canary/canary/services/square_sandbox_seeder.py`, `Canary/canary/blueprints/ops_console.py`

---

## Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| Square Sandbox API (`connect.squareupsandbox.com/v2`) | External API | All Scenario Fire operations: orders, payments, refunds, cancellations; Sandbox Seeder: team members, catalog items |
| `growdirect_postgres` (canary database) | Infrastructure | Scenario Runner writes via psycopg2; Scenario Verify reads via SQLAlchemy; Scenario Fire reads employee-location assignments |
| `growdirect_valkey` (DB 0) | Infrastructure | Flask session backend for admin authentication (indirect) |
| `canary.services.health_check.chirp_lab` | Internal service | `live_fire_order()`, `live_fire_transaction()`, `cancel_payment()`, `_get_square_client()` — Square SDK wrappers used by Scenario Fire |
| `canary.db.session_factory` | Internal service | SQLAlchemy sessions for ORM queries and Scenario Verify |
| `canary.models.app.employee_links.EmployeeLocationAssignment` | Model | Resolves default `team_member_id` / `location_id` before fire steps |
| `canary.services.chirp.rule_definitions.RULE_MAP` | Internal service | Threshold definitions for the inline threshold controls |
| `tests.fixtures.use_cases` | Test fixtures | Cross-domain seed functions for `"seed"` action steps (timecards, cash drawers, disputes) |
| `psycopg2` | Library | Direct database connection for Scenario Runner |
| `requests` | Library | HTTP client for Sandbox Seeder Square API calls |
| Square Python SDK | Library | Orders, Payments, Refunds API (via `chirp_lab`) |
| Flask session + `g.merchant_id` | Framework | Admin authentication and merchant context |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Ops Console UI | Scenario name, optional overrides (team_member_id, location_id) | JSON POST body |
| Square Sandbox API responses | Payment IDs, order IDs, refund IDs, team member IDs, catalog item IDs | JSON API responses |
| Environment variables | `SQUARE_ACCESS_TOKEN`, database credentials | Process env / `.env` file |

### What's Stored

**Scenario Fire path:** No direct database writes. Data enters CRDM only through the normal webhook pipeline (Square fires webhooks after sandbox API calls, TSP parses them, Chirp evaluates rules, alerts are created). The fire service itself stores nothing except an in-process `_last_fire_poll_ids` dict (keyed by scenario name, not persisted).

**Scenario Runner path:** Direct psycopg2 inserts into:

| Table | Fields written | ID pattern |
|-------|---------------|------------|
| `sales.transactions` | id, merchant_id, external_id, location_id, employee_id, transaction_type, transaction_date, amount_cents, source_type, currency, created_at, updated_at | `sc-txn-{type}-{hex8}` |
| `sales.cash_drawer_shifts` | id, square_shift_id, state, opened_at, starting_cash_cents, cash_variance_cents | `sc-shift-{hex8}` |
| `app.alerts` | id, rule_id, alert_type, severity, source_table, source_id, details (JSON), created_by | `sc-alert-{rule}-{hex8}` |
| `app.fox_cases` | id, case_number, merchant_id, status, assigned_to, created_at, updated_at | `sc-case-{hex8}` |
| `app.fox_case_timeline` | id, case_id, event_type, details | `sc-tl-{hex8}` |
| `app.fox_evidence` | id, case_id, file_name, file_hash, chain_hash, previous_chain_hash | `sc-evid-{hex8}` |

**Sandbox Seeder path:** Writes to Square sandbox only (external). Creates team members and catalog items via Square API. No local database writes.

### What Exits

| Destination | Data | Purpose |
|-------------|------|---------|
| Square Sandbox API | Orders, payments, refunds, cancellations | Scenario Fire creates real sandbox transactions |
| Ops Console UI | Fire results (poll_ids, step statuses), verify results (SQL output, pass/fail), seeder results | Displayed to the admin operator |
| Canary webhook pipeline | Webhook events triggered by Square after fire | Square sends `payment.completed`, `refund.created`, etc. webhooks that enter TSP |

### PII Classification

| Field | Classification | Notes |
|-------|---------------|-------|
| `SQUARE_ACCESS_TOKEN` | **restricted** | OAuth token for sandbox API access. Read from env, never logged. |
| Team member emails (seeder) | **internal** | Hardcoded test emails (`sofia@growdirect.io`, etc.). Not real person data. Sent to Square sandbox only. |
| Team member names (seeder) | **internal** | Hardcoded test names. Sent to Square sandbox only. |
| `merchant_id` | **internal** | Hardcoded demo ID `demo-sq-farmers-market-0001`. Not real merchant data. |
| Database credentials (`PG_USER`, `PG_PASS`) | **restricted** | Used by psycopg2 connections. Read from env. |
| Transaction amounts, dates, types | **public** | Synthetic test data with no real-world correlation. |
| Square payment IDs (poll_ids) | **internal** | Sandbox-only IDs returned by Square. Cached in-process and passed to verify. |

**Key finding:** The Test Lab operates exclusively against synthetic/demo data. No real merchant PII enters or exits this service. All team members are hardcoded fictional names. All merchant IDs are demo-prefixed. The only sensitive values are the Square sandbox OAuth token and database credentials, both read from environment variables.

---

## API Contract

All routes are registered on `ops_console_bp` with URL prefix `/ops/`. All routes require sandbox environment (`SQUARE_ENVIRONMENT == "sandbox"`) and an authenticated admin session (enforced by `ops_guard` `before_request`).

### Scenario Fire

**`POST /ops/api/scenario/fire`** — Fire a named scenario against Square sandbox API.
- Body: `{"scenario": "refund_detection"}`
- Returns: `{ok, scenario, scenario_name, steps[], poll_ids[], step_count, elapsed_seconds, detail}`
- Error: `{ok: false, error, available[]}`

**`POST /ops/api/scenario/batch`** — Fire multiple scenarios sequentially.
- Body: `{"scenarios": ["happy_path_payment", "refund_detection"]}` (omit to fire all)
- Returns: `{ok, results: {scenario_name: {...}, _summary: {total, succeeded, failed}}}`

**`GET /ops/api/scenario/poll/<payment_id>`** — Poll pipeline status for a Square payment.
- Returns: `{ok, payment_id, ingested, transaction_id, alerts[], pipeline_complete}`

**`POST /ops/api/scenario/verify-owl`** — Run SQL verification after fire.
- Body: `{scenario, poll_ids[]}`
- Falls back to server-side `_last_fire_poll_ids` cache if poll_ids absent
- Returns: `{ok, scenario, all_passed, results[{query, expect_min, actual_count, passed, sql, rows[], query_time_ms, error}]}`

### Threshold Controls

**`GET /ops/api/scenario/thresholds`** — Current threshold values for all rules referenced by scenarios.
- Returns: `{ok, thresholds: {rule_id: {rule_name, defaults, overrides, effective, primary_key, primary_value}}}`

**`POST /ops/api/scenario/threshold`** — Update a rule threshold for the authenticated merchant.
- Body: `{"rule_id": "C-001", "key": "seconds", "value": 600}`

### Sandbox Seeder

**`POST /ops/api/sandbox/seed`** — Run sandbox seeder (team members + catalog). Idempotent.
- Returns: `{ok, results: {phase: {created, skipped, errors}}}`

**`GET /ops/api/sandbox/team-members`** — List Square sandbox team members.
- Returns: `{ok, team_members: [{name, id}]}`

**`GET /ops/api/sandbox/locations`** — List Square sandbox locations.
- Returns: `{ok, locations: [{id, name, status}]}`

### Python API

| Function | Module | Purpose |
|----------|--------|---------|
| `fire_scenario(name)` | `scenario_fire` | Execute named scenario, returns fire result dict |
| `batch_fire(keys)` | `scenario_fire` | Sequential batch execution |
| `run_scenario(name)` | `scenario_runner` | Execute synthetic data scenario |
| `run_randomizer(count)` | `scenario_runner` | Generate random transactions (capped at 50) |
| `purge_scenario_data()` | `scenario_runner` | Delete all `sc-*` prefixed rows; blocked in production |
| `get_scenario_counts()` | `scenario_runner` | Count live scenario rows per table |
| `reseed_baseline()` | `scenario_runner` | Invoke `level_b_demo.py` via subprocess |
| `SquareSandboxSeeder.seed_all()` | `square_sandbox_seeder` | Idempotent team member + catalog seeding |
| `run_verification_queries(queries, merchant_id, poll_ids)` | `scenario_verify` | Parameterized SQL verification |

---

## Operations

### Startup Sequence

1. Test Lab has no independent startup. It runs within the Canary Flask process.
2. Ops Console blueprint (`ops_console_bp`) is registered during Flask app factory.
3. `ops_guard` `before_request` hook blocks all `/ops/` access unless `SQUARE_ENVIRONMENT == "sandbox"`.
4. No health check endpoint specific to Test Lab. It relies on the Canary app-level health check.

### How to Run Scenarios

**Prerequisite:** Shared Docker infra running (`growdirect_postgres`, `growdirect_valkey`). Canary app running on port 5001 with `SQUARE_ENVIRONMENT=sandbox`.

```bash
# Start shared infra + Canary
cd ~/GrowDirect/devops && docker compose up -d
cd ~/GrowDirect/Canary/devops && docker compose up -d

# Seed the Square sandbox (idempotent)
curl -X POST http://localhost:5001/ops/api/sandbox/seed \
  -H "Cookie: session=<admin_session>" \
  -H "Content-Type: application/json"

# Fire a single scenario
curl -X POST http://localhost:5001/ops/api/scenario/fire \
  -H "Cookie: session=<admin_session>" \
  -H "Content-Type: application/json" \
  -d '{"scenario": "refund_detection"}'

# Fire all scenarios
curl -X POST http://localhost:5001/ops/api/scenario/batch \
  -H "Cookie: session=<admin_session>" \
  -H "Content-Type: application/json"

# Verify results
curl -X POST http://localhost:5001/ops/api/scenario/verify-owl \
  -H "Cookie: session=<admin_session>" \
  -H "Content-Type: application/json" \
  -d '{"scenario": "refund_detection", "poll_ids": ["<payment_id>"]}'
```

**CLI (sandbox seeder only):**
```bash
python3 -m canary.services.square_sandbox_seeder --all
python3 -m canary.services.square_sandbox_seeder --dry-run --team
```

### How to Reset Sandbox State

```bash
# Purge all sc-* prefixed scenario data from PostgreSQL
# (done via Ops Console UI "Purge" button or programmatically)
# purge_scenario_data() deletes from all target tables in FK-safe order

# Reseed baseline demo data
# reseed_baseline() calls devops/seeds/level_b_demo.py via subprocess

# Square sandbox data: cannot be deleted via API.
# Square sandbox is shared and non-deletable. Seed operations are idempotent.
```

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Square sandbox API unreachable | Scenario Fire fails | `_get_square_client()` raises `RuntimeError`; fire returns `{ok: false}` |
| Square sandbox rate limited | Fire steps fail individually | Per-step error recorded; batch continues to next scenario |
| PostgreSQL unreachable | Runner and Verify fail | psycopg2 `OperationalError` or SQLAlchemy connection error returned |
| Webhook not received (Square delay) | Poll shows `ingested: false` | UI keeps polling; operator can re-fire. Normal Square webhook latency is 5-30 seconds |
| Admin session expired | All ops routes blocked | `ops_guard` redirects to login page |
| `SQUARE_ENVIRONMENT != "sandbox"` | All ops routes return 403 | Process-level guard in `ops_guard` |

### Monitoring

| Signal | What it means | Alert threshold |
|--------|--------------|-----------------|
| `scenario_fire` logger errors | Square API failures or unexpected exceptions | Any error in production should not occur (Test Lab is sandbox-only) |
| `purge_scenario_data` failure | Trigger manipulation failed or production guard tripped | Immediate — indicates environment misconfiguration |
| Scenario verify `all_passed: false` | Pipeline regression — expected rules did not fire | Informational during dev; critical during pre-release QA |
| `_last_fire_poll_ids` growing unbounded | In-process dict not cleaned | Monitor process memory; no auto-cleanup exists |

### Configuration

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `SQUARE_ENVIRONMENT` | Yes | — | Must be `"sandbox"`. Guards all Test Lab access. |
| `SQUARE_ACCESS_TOKEN` | Yes | — | Bearer token for Square sandbox API. |
| `SEED_PG_HOST` | No | Falls back to `PG_HOST`, then `"postgres"` | PostgreSQL host for psycopg2 connections. |
| `PG_PORT` | No | `5432` | PostgreSQL port. |
| `PG_USER` | No | `"canary"` | Database user. |
| `PG_PASS` / `PG_PASSWORD` | No | `"canary_dev_2026"` | Database password. |
| `CANARY_ENV` | No | `"development"` | `purge_scenario_data()` blocks trigger manipulation when `"production"`. |

---

## Deployment

### Docker Service

Test Lab runs inside the Canary Flask container. No separate Docker service.

```yaml
# In Canary/devops/docker-compose.yml
services:
  canary-app:
    image: canary-app
    ports:
      - "5001:5001"
    environment:
      - SQUARE_ENVIRONMENT=sandbox   # Required for Test Lab
      - SQUARE_ACCESS_TOKEN=${SQUARE_ACCESS_TOKEN}
    # ... other Canary config
```

### AWS Target

| Component | Target | Notes |
|-----------|--------|-------|
| Canary Flask (includes Test Lab) | ECS/Fargate | Test Lab routes available only in staging/sandbox task definitions |
| `SQUARE_ACCESS_TOKEN` | AWS Secrets Manager | Currently in `.env` (P0 finding) |
| `PG_PASS` | AWS Secrets Manager | Currently in `.env` (P0 finding) |
| Sandbox guard | Environment variable | `SQUARE_ENVIRONMENT` must be `sandbox` in the ECS task definition for staging; omitted or set to `production` for prod |

### CI/CD Requirements

- Test Lab routes must NOT be reachable in production ECS tasks. Enforced by `SQUARE_ENVIRONMENT` env var (not `sandbox` in prod).
- Sandbox seeder CLI can run as a one-shot ECS task for staging environment setup.
- No database migrations required (Test Lab uses existing CRDM tables).

---

## Code Review Findings

### P0 — Blocks Production

**P0-TL-01: `scenario_fire.py` has no independent sandbox guard**
`fire_scenario()` delegates sandbox enforcement entirely to `chirp_lab._get_square_client()`, which checks `SQUARE_ENVIRONMENT`. If `fire_scenario()` is ever called outside the Ops Console route context (e.g., imported and called from another module, a management command, or a test), the only guard is inside `_get_square_client()`. The function itself has no `SQUARE_ENVIRONMENT` check.
- **Risk:** If `_get_square_client()` is refactored or if `fire_scenario()` is called with a pre-constructed client, the sandbox guard is lost.
- **Fix:** Add `if os.getenv("SQUARE_ENVIRONMENT") != "sandbox": raise RuntimeError("sandbox only")` at the top of `fire_scenario()`.
- **Linear:** TBD

**P0-TL-02: Database credentials have hardcoded fallback defaults**
`scenario_runner.py` lines 31-34 set `PG_USER` default to `"canary"` and `PG_PASS` default to `"canary_dev_2026"` at module load time. These are dev credentials embedded in source code. If the env vars are unset in a deployed environment, the runner silently falls back to these defaults.
- **Risk:** Credentials in source code. If the module is loaded in production (even though routes are blocked), the defaults are in memory.
- **Fix:** Remove default values. Require env vars explicitly and raise on missing values. Move credentials to AWS Secrets Manager.
- **Linear:** TBD

**P0-TL-03: Secrets in `.env` files, not Secrets Manager**
`SQUARE_ACCESS_TOKEN` and database passwords are stored in `.env` files, not AWS Secrets Manager. This is consistent with the platform-wide P0 finding but specifically critical here because the Square sandbox token grants API access to create payments and refunds.
- **Fix:** Retrieve from AWS Secrets Manager via `boto3` at startup.
- **Linear:** TBD (platform-wide issue)

### P1 — Before GA

**P1-TL-01: `_insert()` uses f-string table name interpolation (SQL injection surface)**
`scenario_runner._insert()` (line 94) uses `f"INSERT INTO {table} ..."`. The `table` parameter is always a hardcoded string from internal callers (e.g., `"sales.transactions"`), never user input. However, this pattern is flagged by security scanners and creates risk if the function is ever called with user-controlled input.
- **Fix:** Validate `table` against an allowlist of known table names, or use `sql.Identifier()` from psycopg2.
- **Linear:** TBD

**P1-TL-02: No audit logging for destructive operations**
`purge_scenario_data()` deletes rows and disables/re-enables database triggers. `fire_scenario()` creates real Square sandbox payments. Neither operation is recorded in an audit log. The only trace is application logs (Python `logger`), which are ephemeral.
- **Fix:** Write audit log entries for: purge operations (who, when, row counts), scenario fires (who, which scenario, poll_ids), and threshold changes.
- **Linear:** TBD

**P1-TL-03: No rate limiting on Test Lab API endpoints**
The Ops Console fire, batch, seed, and purge endpoints have no rate limiting. The QA Agent chat endpoint has `@limiter.limit("10/minute")`, but the scenario endpoints do not. A malicious or buggy client could spam Square sandbox API calls.
- **Fix:** Add `@limiter.limit()` decorators to fire, batch, and seed endpoints.
- **Linear:** TBD

**P1-TL-04: `_last_fire_poll_ids` is an unbounded in-process dict**
The server-side poll_ids cache (`_last_fire_poll_ids` in `ops_console.py` line 204) grows without bound. Every scenario fire appends to it. In a long-running process, this leaks memory. It also does not survive process restarts (Gunicorn worker recycling).
- **Fix:** Use Valkey with TTL (e.g., 1 hour) instead of an in-process dict. Or add a max-size LRU cache.
- **Linear:** TBD

**P1-TL-05: `reseed_baseline()` uses `python` instead of `python3`**
Line 1065 of `scenario_runner.py` calls `subprocess.run(["python", ...])`. Platform standard is `python3`. On some environments, `python` may not be in PATH or may resolve to Python 2.
- **Fix:** Change to `["python3", ...]`.
- **Linear:** TBD

### P2 — Post-Launch

**P2-TL-01: Duplicate production guard in `purge_scenario_data()`**
The `if os.getenv('CANARY_ENV') == 'production': raise RuntimeError(...)` check appears twice in sequence (lines 1008 and 1012). The second is dead code.
- **Fix:** Remove the duplicate check.
- **Linear:** TBD

**P2-TL-02: Duplicate scenario registries**
`scenario_runner.SCENARIOS` and `scenario_fire.SCENARIO_REGISTRY` are separate registries with overlapping scenario keys but different structures and execution engines. No single authoritative scenario list exists.
- **Fix:** Merge into a single registry with an `execution_mode` field, or rename runner scenarios to make the distinction explicit.
- **Linear:** TBD

**P2-TL-03: Test Lab services in flat services root**
`scenario_runner.py`, `scenario_fire.py`, `scenario_verify.py`, and `square_sandbox_seeder.py` live directly under `canary/services/` rather than in a dedicated `canary/services/test_lab/` subdirectory. Inconsistent with the Microservice Delivery Pattern.
- **Fix:** Consolidate into `canary/services/test_lab/` with re-exports.
- **Linear:** TBD

**P2-TL-04: No isolated test coverage for Test Lab services**
`scenario_fire.py` has no unit tests (requires live Square sandbox). `scenario_runner.py` has only schema-validation tests (no data insertion tests). `scenario_verify.py` has no tests. The existing `test_batch_fire.py` uses mocks but does not test step dispatch logic.
- **Fix:** Add mock-based unit tests for fire step dispatch. Add runner tests against `canary_test` database. Add verify tests with fixture data.
- **Linear:** TBD

**P2-TL-05: Scenario Verify `_build_verify_sql` uses string-based query dispatch**
`_build_verify_sql()` maps query labels like `"refunds today"` to SQL templates via string matching. Adding new verification query types requires modifying a growing if/elif chain. No validation that `query_label` matches a known type (returns `None` SQL on unknown labels).
- **Fix:** Refactor to a registry pattern (dict of label-to-builder functions).
- **Linear:** TBD

---

## Production Readiness Checklist

- [x] PII encrypted at rest — N/A: Test Lab handles only synthetic/demo data. No real merchant PII flows through this service. Square sandbox tokens are the only sensitive value (covered by secrets management).
- [ ] Secrets in AWS Secrets Manager (not .env) — `SQUARE_ACCESS_TOKEN` and `PG_PASS` are in `.env` files. (P0-TL-03)
- [ ] Health check endpoint responds — No Test Lab-specific health check. Relies on Canary app-level health check. Acceptable for an admin subsystem.
- [ ] Audit logging for sensitive operations — No audit log for purge, fire, or threshold changes. (P1-TL-02)
- [ ] Data retention policy implemented — Scenario data (`sc-*` prefix) has manual purge only. No automated retention. Acceptable for sandbox-only test data.
- [ ] Rate limiting on public endpoints — No rate limiting on fire/batch/seed endpoints. (P1-TL-03). Note: these are admin-only, not public.
- [x] Error responses don't leak internals — Error responses return generic messages. Stack traces go to server logs only. Exception details returned in some cases (`str(e)`) but behind admin auth.
- [x] Sandbox isolation enforced — `ops_guard` blocks all access when `SQUARE_ENVIRONMENT != "sandbox"`. `_get_square_client()` has independent sandbox check. `SquareSandboxSeeder.__init__` raises if not sandbox. `purge_scenario_data()` has production env guard. Three-layer defense.
- [x] Admin role required — `ops_guard` checks `has_any_role("admin")` before every request.
- [ ] Independent sandbox guard on `fire_scenario()` — Delegates to `_get_square_client()` only. (P0-TL-01)
- [ ] Hardcoded credentials removed from source — `PG_USER`/`PG_PASS` defaults in `scenario_runner.py`. (P0-TL-02)
