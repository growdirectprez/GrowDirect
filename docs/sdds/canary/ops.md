# Ops

**Service Type:** App Service (Canary)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/DevOps|DevOps]] · **Operator role:** [[docs/team/Engineer|Engineer]]

## Purpose

The Ops domain owns internal tooling for health check orchestration, synthetic data generation, pipeline monitoring, configuration management, and feature flags. It is the self-monitoring nervous system of Canary -- the service that validates every other service works end-to-end. None of its UI is merchant-facing. All testing tools are sandbox-gated (`SQUARE_ENVIRONMENT == "sandbox"`).

## Dependencies

| Dependency | Type | Required | What Fails Without It |
|------------|------|----------|----------------------|
| PostgreSQL (canary) | Database | Yes | Config service, feature flags, all data generators, pipeline monitor |
| Valkey (DB 0) | Cache | No (degrades) | Health check polling visibility lost; pipeline still runs |
| Valkey (DB 3) | Cache | No | Dedup cache size unavailable in pipeline monitor |
| Valkey (DB 4) | Stream | No | Stream state unavailable in pipeline monitor |
| Chirp Rule Engine | Service | Yes (for analyze) | Health check ANALYZE stage fails |
| Owl Report Generator | Service | No (degrades) | Health report falls back to deterministic template |
| Ollama (qwen3:14b) | External | No (degrades) | Report generation uses fallback path |
| Square SDK | External | No (sandbox only) | Live fire and scenario fire unavailable |
| Data Factory | Service | Yes (for demo HC) | Demo health check INGEST stage fails |
| InitialDataSync | Service | Yes (for live HC) | Live health check INGEST stage fails |

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Ops UI (admin) | Health check start request | JSON `{merchant_id, mode, profile}` |
| Ops UI (admin) | Live fire payment params | JSON `{amount_cents, tip_amount_cents, nonce, note}` |
| Ops UI (admin) | Scenario fire request | JSON `{scenario}` |
| Ops UI (admin) | Config update | JSON `{config_key, config_value}` |
| Ops UI (admin) | Feature flag toggle | JSON `{flag_key, is_enabled}` |
| Pipeline tables (read) | Table row counts from 3 schemas | SQL COUNT(*) queries |
| Valkey streams | Stream lengths, consumer groups | Valkey XLEN/XINFO commands |

### What's Stored

| Location | Data | Classification | Encryption | TTL |
|----------|------|---------------|------------|-----|
| Valkey `hc:session:{uuid}` | Session state JSON (merchant_id, stage, heartbeat, report, error) | internal | None | 3600s |
| Valkey `sim:session:{uuid}` | Simulator result JSON (merchant_id, config, heartbeat) | internal | None | 7200s |
| `app.app_config` | Runtime config key/value pairs | internal | None (secrets masked in UI) | Persistent |
| `app.feature_flags` | Global flag definitions | internal | None | Persistent |
| `app.merchant_feature_flags` | Per-merchant flag overrides | internal | None | Persistent |

### What Exits

| Destination | Data | Classification |
|------------|------|---------------|
| Ops UI (admin browser) | Session state, heartbeat scores, report JSON | internal |
| Ops UI (admin browser) | Config health status (env var names, non-secret values) | internal |
| Ops UI (admin browser) | Feature flag states per merchant | internal |
| Ops UI (admin browser) | Pipeline table counts, Valkey stream state | internal |
| Ops UI (admin browser) | IP addresses from ingestion_log | sensitive |
| canary_sales tables | Synthetic transactions (via DataFactory, Simulator, ChirpLab) | internal |
| canary_app tables | Alerts (via ChirpRuleEngine), Owl sessions/findings | internal |
| Square Sandbox API | Payment creation requests (live fire, scenario fire) | internal |

### PII Classification

| Field | Location | Classification | Notes |
|-------|----------|---------------|-------|
| `merchant_id` | All session state, config, flags | internal | Internal UUID, not PII itself |
| `access_token` | HealthCheckSession (in-memory) | restricted | Square OAuth token; never serialized to Valkey |
| `ip_address` | Pipeline monitor ingestion_log query | sensitive | Returned in API response, displayed in UI |
| `user_agent` | Pipeline monitor event trace query | sensitive | Returned in API response |
| Config secrets (passwords, keys) | ENV vars, app_config | restricted | Masked to `********` in UI; `is_secret=True` blocks updates |
| `SQUARE_APPLICATION_SECRET` | CONFIG_REGISTRY | restricted | ENV var; masked in health dashboard |
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | CONFIG_REGISTRY | restricted | ENV var; masked in health dashboard |

## API Contract

### Ops Console (`ops_console.py` -> `/ops/*`)

All routes require sandbox environment AND admin role. Session-based auth (not JWT).

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/` | GET | Session+admin | Test lab page (single-page ops console) |
| `/test-lab` | GET | Session+admin | Legacy redirect to `/ops/` (301) |
| `/atlas` | GET | Session+admin | Atlas diagram browser |
| `/atlas/figure` | GET | Session+admin | Single Atlas figure detail |
| `/qa` | GET | Session+admin | QA Agent interactive page |
| `/qa/chat` | POST | Session+admin | QA Agent chat endpoint (rate limited: 10/min) |
| `/api/scenario/fire` | POST | Session+admin | Fire a named scenario via Square SDK |
| `/api/scenario/batch` | POST | Session+admin | Fire multiple scenarios sequentially |
| `/api/scenario/poll/<payment_id>` | GET | Session+admin | Poll webhook->pipeline status for a scenario payment |
| `/api/scenario/verify-owl` | POST | Session+admin | Run Owl verification queries for completed scenario |
| `/api/scenario/thresholds` | GET | Session+admin | Return current thresholds for scenario-referenced rules |
| `/api/scenario/threshold` | POST | Session+admin | Update a single rule's threshold |
| `/api/sandbox/team-members` | GET | Session+admin | Return Square sandbox team members |
| `/api/sandbox/locations` | GET | Session+admin | Return Square sandbox locations |
| `/api/sandbox/seed` | POST | Session+admin | Run the sandbox seeder |
| `/api/chirp-lab/live-fire/status` | GET | Session+admin | Check Square sandbox credentials configured |
| `/api/chirp-lab/live-fire` | POST | Session+admin | Create real Square sandbox payment |
| `/api/chirp-lab/live-fire/poll/<payment_id>` | GET | Session+admin | Poll pipeline for live-fired payment results |

### DevOps Monitor (`devops_monitor.py` -> `/devops/*`)

Sandbox-gated via `before_request` hook. Also accepts `X-API-Key` header matching `CANARY_MCP_API_KEY` as auth fallback.

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/monitor` | GET | Sandbox guard | Legacy redirect to /ops/ (301) |
| `/monitor/api/pipeline-state` | GET | Sandbox guard + session/API key | Full pipeline snapshot: table counts (3 schemas), Valkey stream state, last 10 events per stage |
| `/monitor/api/recent-events` | GET | Sandbox guard + session/API key | Recent events by stage. Params: `stage` (ingestion/sealed/parsed/batched), `limit` (1-50, default 20) |
| `/monitor/api/event/<event_id>` | GET | Sandbox guard + session/API key | Cross-stage event trace (ingestion_log, evidence_records, event_inscriptions) |

### Health Blueprint (`health.py`)

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/health` | GET | None | Container liveness. Always 200. Version from `CANARY_VERSION` env (default 0.5.0). Rate-limit exempt. |
| `/readiness` | GET | None | Dependency readiness check: PostgreSQL (canary) + Valkey ping. Returns 503 if any dependency is down. |

### MCP Server (`canary-ops` at `/ops-mcp/*`)

**Status: Ghost entry.** The streamable_server.py registers `"ops": "/ops-mcp"` but notes it as a TODO with no corresponding blueprint. The 8 MCP tools documented in the original SDD are not currently wired. This is a code review finding (P2-OPS-08).

### Internal Service APIs (no HTTP endpoints)

**Runner (health_check/runner.py):**

| Function | Signature | Purpose |
|----------|-----------|---------|
| `start_session` | `(merchant_id, profile="cafe", mode="demo", lookback_days=None) -> dict` | Creates session, stores initial Valkey state, launches daemon thread |
| `get_session_state` | `(session_id) -> Optional[dict]` | Reads session JSON from Valkey for polling |
| `list_sessions` | `() -> list` | Up to 50 most recent sessions from Valkey sorted set |

**Config Service (config_service.py):**

| Function | Signature | Purpose |
|----------|-----------|---------|
| `get_config_value` | `(key, default=None) -> str` | 3-level resolution: DB > ENV > registry |
| `get_config_health` | `() -> dict` | Grouped env var status (set/default/missing) |
| `get_config_summary` | `() -> dict` | Counts: total/set/default/missing |
| `update_config` | `(key, value) -> bool` | Update non-secret config in DB. Refuses is_secret=True. |
| `get_editable_configs` | `() -> list[dict]` | Non-secret DB configs for editor UI |

**Feature Flags (feature_flags.py):**

| Function | Signature | Purpose |
|----------|-----------|---------|
| `is_flag_enabled` | `(flag_key, merchant_id=None) -> bool` | 3-tier: merchant override > global > ENV |
| `get_all_flags` | `(merchant_id=None) -> list[dict]` | All flags with resolved state + source |
| `set_global_flag` | `(flag_key, is_enabled) -> bool` | Toggle global default |
| `set_merchant_flag` | `(flag_key, merchant_id, is_enabled) -> bool` | Per-merchant override |
| `remove_merchant_override` | `(flag_key, merchant_id) -> bool` | Revert to global (idempotent) |

## Data Model

The Ops domain owns three persistent tables and uses Valkey for ephemeral session state. DB writes to other domains' tables happen through the data generators.

### Owned Tables

| Table | Schema | Purpose |
|-------|--------|---------|
| `app.app_config` | app | Runtime configuration key/value store (35 registered env vars) |
| `app.feature_flags` | app | Global feature flag catalog |
| `app.merchant_feature_flags` | app | Per-merchant feature flag overrides |

### Valkey State (Health Check)

| Key Pattern | Type | TTL | Content |
|-------------|------|-----|---------|
| `hc:session:{uuid}` | String | 3600s (1 hour) | JSON-serialized session state: session_id, merchant_id, mode, stage, started_at, completed_at, transaction_count, alert_count, heartbeat (score/band/breakdown), report dict, error, stage_log |
| `hc:sessions` | Sorted Set | N/A | Session IDs scored by start timestamp (capped at 50) |

### Valkey State (Simulator)

| Key Pattern | Type | TTL | Content |
|-------------|------|-----|---------|
| `sim:session:{uuid}` | String | 7200s (2 hours) | JSON-serialized SimulatorResult |
| `sim:sessions` | Sorted Set | N/A | Session IDs scored by timestamp (capped at 20) |

### In-Memory Dataclasses

**HealthCheckSession** (session.py):

| Field | Type | Purpose |
|-------|------|---------|
| `session_id` | str | UUID, generated at creation |
| `merchant_id` | str | Target merchant |
| `mode` | str | "demo" or "live" |
| `stage` | SessionStage | Current pipeline stage |
| `started_at` | datetime | UTC timestamp |
| `completed_at` | Optional[datetime] | Set on COMPLETED or ABORTED |
| `access_token` | Optional[str] | Square OAuth token (live mode only, never serialized to Valkey) |
| `events_published` | int | Count of events published to TSP stream (live mode) |
| `transaction_ids` | List[str] | Generated/synced transaction IDs |
| `alert_dicts` | List[Dict] | Alert output from Chirp evaluation |
| `heartbeat` | Optional[HeartbeatResult] | Scoring result |
| `report` | Optional[Dict] | Generated health report |
| `error` | Optional[str] | Error message if aborted |
| `stage_log` | List[Dict] | Append-only transition audit trail |

**HeartbeatResult** (frozen dataclass):

| Field | Type | Description |
|-------|------|-------------|
| `score` | int | 0-100 health score |
| `band` | str | healthy, normal, warning, alert |
| `total_alerts` | int | Count of alerts processed |
| `breakdown` | Dict[str, int] | Counts by severity level |

**SimulatorConfig:**

| Field | Type | Default | Constraints |
|-------|------|---------|-------------|
| `merchant_id` | str | auto `sim-merchant-{uuid}` | |
| `profile` | str | "cafe" | cafe, retail, restaurant |
| `weeks` | int | 14 | 1-52 |
| `employee_count` | int | 5 | 2-15 |
| `location_count` | int | 2 | 1-5 |
| `anomaly_density` | str | "medium" | low, medium, high |
| `seed` | Optional[int] | None | For reproducible runs |
| `run_chirp` | bool | True | Evaluate through Chirp |
| `append` | bool | False | Keep existing data |

### Tables Written (Owned by Other Domains)

| Database | Table | Written By | ID Prefix |
|----------|-------|------------|-----------|
| canary_sales | `transactions` | DataFactory, Simulator, ChirpLab | `hc-`, `sim-`, `lab-` |
| canary_sales | `transaction_line_items` | Simulator | `sim-` |
| canary_sales | `transaction_tenders` | Simulator | `sim-` |
| canary_sales | `employee_timecards` | Simulator | `sim-` |
| canary_app | `alerts`, `alert_history` | All (via ChirpRuleEngine) | N/A |
| canary_app | `owl_sessions`, `owl_findings` | Health Check ACT stage | N/A |
| canary_app | `owl_merchant_memory` | Health Check ACT stage | N/A |

### Tables Read (Pipeline Monitor)

| Database | Tables |
|----------|--------|
| canary_sales | ingestion_log, evidence_records, transactions, transaction_line_items, transaction_tenders, inscription_pool, event_inscriptions, dead_letter_queue, refund_links |
| canary_app | webhook_events, merchants, locations, employees |
| canary_metrics | daily_metrics, hourly_metrics, employee_daily_metrics |

All monitor reads use `_safe_count()` with an `_ALLOWED_TABLES` frozenset to prevent SQL injection.

## Workflows

### Health Check Pipeline (7-Stage State Machine + Terminal States)

```
start_session(merchant_id, profile, mode)
  |-- Creates HealthCheckSession (UUID)
  |-- Stores initial state in Valkey
  |-- Launches daemon thread -> _run_in_thread()
      |-- Opens own DB sessions (sales + app)
      |-- Creates HealthCheckOrchestrator(sales, app)
      |-- Calls orchestrator.run() with stage callback
      |
      |-- [CREATED] Initial state
      |-- [OAUTH] Live: verify Square token. Demo: skip.
      |-- [INGEST] Live: InitialDataSync (publish to TSP stream).
      |           Demo: DataFactory.generate_merchant_day().
      |-- [LOAD] Live: poll sales.transactions until count stabilizes
      |          (2min timeout, 2s poll, 3 stable ticks = done).
      |          Demo: transaction_ids already set from INGEST.
      |-- [ANALYZE] ChirpRuleEngine._evaluate_with_thresholds() on all txns.
      |            write_alerts_to_session() -> canary_app.
      |            Pre-loads thresholds once (avoids per-txn DB query).
      |-- [PRESENT] compute_heartbeat(alert_dicts) -> HeartbeatResult.
      |            Load merchant memory + previous findings for delta.
      |-- [ACT] assemble_context() -> generate_health_report().
      |         create_owl_session() + findings + update_merchant_memory.
      |-- [TEARDOWN] Demo: DataFactory.cleanup(). Live: data retained.
      |-- [COMPLETED] Final state to Valkey.
      |
      |-- Each stage callback -> serialize session -> write to Valkey
      |-- DB sessions closed in finally block
```

**Stage transitions** are forward-only via `_TRANSITIONS` dict. Any non-terminal stage can transition to ABORTED. `HealthCheckSession.advance()` raises ValueError on invalid transitions.

**Valkey resilience:** All Valkey operations are try/except. If Valkey is down, the pipeline still runs -- Valkey is for polling visibility, not execution control. `get_session_state()` returns None, `list_sessions()` returns empty list.

### Merchant Simulator Pipeline (5-Stage)

```
SimulatorConfig -> MerchantSimulator.simulate()
  |
  Stage 1: _build_employees() -> roster with role/shift/anomaly assignments
           _generate_timecards() -> EmployeeTimecard rows
  |
  Stage 2: For each week (0..13), each day (0..6):
           _daily_roster() -> active employees
           _generate_day() -> build Square webhook payloads
           -> parse_payment() + parse_order_*() -> CDM records
  |
  Stage 3: _inject_anomalies() per day:
           sweetheart (40-75% discounts), void_abuse (multi-void per shift),
           time_theft (outside hours), cash_skim ($150-350 refunds),
           rapid_refund (sale+refund in minutes), after_hours (1-5 AM),
           round_dollars (cluster of $X.00)
           Ramp formula: min(1.0, (week+1) / (weeks*0.6)) * density_mult * 0.4
  |
  Stage 4: _run_chirp() batched at 200 txns -> alerts to canary_app
  |
  Stage 5: compute_heartbeat(all_alert_dicts) -> SimulatorResult
```

### Report Generation Pipeline

```
alert_dicts -> compute_heartbeat() -> HeartbeatResult (pure, deterministic)
  |
  v
assemble_context() -> 3 windows: running summary + delta + heartbeat
  |
  v
generate_health_report(context, alerts, score, band, breakdown, findings_data)
  |
  +-- owl_healthy()? YES -> ask_owl(prompt, REPORT_SYSTEM_PROMPT, JSON, 120s)
  |     |-- Valid dict? -> _post_validate():
  |     |     1. Migrate legacy fields (jim->lp, tom->ops, phd->analytics)
  |     |     2. _fix_score_reference() regex in executive_summary
  |     |     3. Patch finding trends vs delta engine
  |     |     4. Ensure 8 required fields (fill defaults if missing)
  |     |     5. Set source="owl", heartbeat_score, heartbeat_band
  |     |-- Bad response -> _fallback_report()
  |
  +-- owl_healthy()? NO -> _fallback_report()
        Band-specific executive summary templates
        Group alerts by category -> findings per category
        Deterministic, correct, less nuanced. source="fallback"
```

### Config Resolution Chain

```
get_config_value("SOME_KEY")
  1. SELECT FROM app_config WHERE config_key = key  -> DB value wins
  2. os.environ.get(key)                            -> ENV var
  3. CONFIG_REGISTRY lookup                         -> registered default
  4. Caller-provided default (or None)
```

### Feature Flag Resolution

```
is_flag_enabled("billing_enabled", merchant_id="M123")
  1. merchant_feature_flags WHERE merchant_id + flag_key -> override wins
  2. feature_flags WHERE flag_key                        -> global default
  3. _ENV_FALLBACKS dict -> os.getenv() parsed as bool   -> ENV fallback
  4. False                                               -> final default
```

DB failures at any tier fall through to the next. `get_all_flags()` returns ENV-only flags (3 entries, source="env") when DB is unreachable.

## Operations

### Startup Sequence

1. Flask app factory registers three blueprints:
   - `ops_console_bp` at `/ops`
   - `devops_monitor_bp` at `/devops`
   - `health_bp` at `/health`
2. No background workers or cron jobs at startup.
3. Health check daemon threads are created on-demand when `start_session()` is called.
4. Config service reads CONFIG_REGISTRY (in-memory list of 35 env var definitions) -- no DB queries at startup.

### Health Checks

| Endpoint | Type | Dependencies Checked |
|----------|------|---------------------|
| `GET /health` | Liveness | None -- always returns 200 if Flask is up |
| `GET /readiness` | Readiness | PostgreSQL (`SELECT 1`), Valkey (`PING`) |

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Valkey down | Health check sessions cannot be polled | Pipeline still runs to completion; polling returns None; list_sessions returns empty |
| PostgreSQL down | Config service, feature flags degrade | `get_config_value` falls through to ENV/registry; `is_flag_enabled` falls through to ENV; `get_all_flags` returns 3 ENV-only entries |
| Ollama down | Health report generation degrades | `_fallback_report()` generates deterministic band-specific templates |
| Square API down | Live fire and scenario fire fail | RuntimeError raised; ops console shows error; no pipeline data generated |
| Health check thread crash | Session stuck in non-terminal stage | Error state written to Valkey with ABORTED; session TTLs out after 1 hour |
| DB session leak in HC thread | Connection pool exhaustion | Mitigated: finally block closes both sales and app sessions |

### Monitoring

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Health check session stuck >10 min | Valkey `hc:session:*` stage_log timestamps | Warning |
| `/health` non-200 | Container orchestrator | Critical -- container restart |
| `/readiness` 503 | Load balancer | Critical -- remove from rotation |
| Pipeline monitor table count = -1 | `_safe_count()` return value | Warning -- table missing or schema issue |
| Config vars with status="missing" | `get_config_summary()` | P1 if secret, P2 otherwise |

### Configuration

**35 registered env vars** across 6 categories:

| Category | Count | Secrets |
|----------|-------|---------|
| database | 4 | POSTGRES_PASSWORD, CANARY_DB_URL |
| auth | 5 | FLASK_SECRET_KEY, KEYCLOAK_ADMIN_PASSWORD |
| general | 7 | None |
| square | 10 | SQUARE_APPLICATION_SECRET, SQUARE_ACCESS_TOKEN, SQUARE_WEBHOOK_SIGNATURE_KEY |
| cms | 4 | DIRECTUS_SECRET, DIRECTUS_ADMIN_PASSWORD |
| monitoring | 5 | SUPERSET_SECRET_KEY, AIRFLOW_FERNET_KEY, AIRFLOW_WEBSERVER_SECRET, AIRFLOW_ADMIN_PASSWORD |

**Feature flags (3 ENV-backed):**

| Flag Key | ENV Var | Default | Purpose |
|----------|---------|---------|---------|
| `billing_enabled` | `BILLING_ENABLED` | false | Enable billing features |
| `audit_logging_enabled` | `AUDIT_LOGGING_ENABLED` | true | Enable audit logging |
| `api_keys_enabled` | `API_KEYS_ENABLED` | false | Enable API key management |

### Key Constants

| Constant | Value | Used By |
|----------|-------|---------|
| HC session TTL | 3600s (1 hour) | Valkey `hc:session:*` |
| HC session cap | 50 | Sorted set max |
| Sim session TTL | 7200s (2 hours) | Valkey `sim:session:*` |
| Sim session cap | 20 | Sorted set max |
| Chirp batch size | 200 | Simulator Chirp evaluation |
| Report timeout | 120s | LLM generation via ask_owl |
| Score tolerance | +/-15 | Post-validation score patching |
| Alert cap in prompt | 25 | Max alerts in report prompt |
| Narrative cap | 2000 chars | extract_narrative_summary() |
| Severity deductions | critical=25, high=15, medium=8, low=3, info=0 | compute_heartbeat() |
| Band thresholds | 90=healthy, 70=normal, 40=warning, 0=alert | HeartbeatResult |
| Live mode lookback | Configurable via `MerchantSettings.lookback_days` (GRO-258). Default 30 days. NULL = all available history. | InitialDataSync |
| Live mode TSP poll | 2s interval, 3 stable ticks, 120s timeout, 30s zero-patience | LOAD stage |
| QA chat rate limit | 10/minute | `/qa/chat` endpoint |
| `CANARY_VERSION` | 0.5.0 | /health response |

## Deployment

### Docker Service Definition

Ops runs inside the Canary Flask container -- no separate service. Blueprints are registered in the app factory.

```
canary-flask:
  ports: 5001
  healthcheck: GET /health (liveness)
  depends_on: growdirect_postgres, growdirect_valkey
```

### AWS Target

| Component | AWS Service | Notes |
|-----------|-------------|-------|
| Canary Flask (includes Ops) | ECS Fargate | Single task definition with /health liveness |
| PostgreSQL | RDS PostgreSQL 17 | Single instance, 3 schemas |
| Valkey | ElastiCache (Valkey mode) | Session state, stream processing |
| Secrets | AWS Secrets Manager | All 12 secret env vars from CONFIG_REGISTRY |

### CI/CD Requirements

- Health check endpoint must respond 200 before deployment completes.
- Readiness check must pass (DB + Valkey) for traffic routing.
- Sandbox guard (`SQUARE_ENVIRONMENT != "sandbox"`) must block all ops console and devops monitor routes in production.

## Code Review Findings

### P0 — Blocks Production

**P0-OPS-01: IP addresses and user agents exposed in pipeline monitor API responses.**
The devops monitor's `_query_ingestion_log()` and `_trace_event()` functions query `ip_address` and `user_agent` from `sales.ingestion_log` and return them directly in JSON API responses. In production, this would expose client IP addresses to any authenticated admin user. IP addresses are PII under GDPR/CCPA.
**Recommended fix:** Remove `ip_address` and `user_agent` from pipeline monitor query results, or hash/mask them. These fields exist for security forensics (webhook source verification), not for the ops dashboard.

**P0-OPS-02: Config value logged in plaintext on update.**
`config_service.py` line 230: `logger.info(f"Config '{config_key}' updated to '{config_value}'")`. If a non-secret config is later reclassified as sensitive, or if the value contains embedded credentials, this log line exposes the value. The `is_secret` guard only prevents DB writes, not log exposure of the value being written.
**Recommended fix:** Log the key and "updated" status only, never the value. For audit trail, record old/new value hashes.

**P0-OPS-03: No authorization on feature flag mutation endpoints.**
`set_global_flag()`, `set_merchant_flag()`, and `remove_merchant_override()` are pure service functions with no auth checks. Any code path that calls them can toggle flags for any merchant. While the ops console blueprint has admin guards, the MCP server (once wired) and any future internal callers have no authorization enforcement at the service layer.
**Recommended fix:** Add a `caller_role` or `actor_id` parameter to flag mutation functions. Enforce admin-only at the service layer, not just the blueprint layer.

### P1 — Before GA

**P1-OPS-04: No audit logging for config or feature flag changes.**
Config updates and feature flag toggles modify runtime behavior for all merchants (or specific merchants). No audit trail exists beyond application logs. There is no record of who changed what flag, when, or from what previous value.
**Recommended fix:** Write audit log entries to a dedicated `app.audit_log` table for all config and flag mutations. Include: actor, timestamp, key, old_value, new_value, merchant_id (for flag overrides).

**P1-OPS-05: Server-side poll_ids cache is an in-process module-level dict.**
`ops_console.py` line 204: `_last_fire_poll_ids: dict = {}` stores scenario fire poll_ids at module scope. With Gunicorn's multi-worker deployment, each worker has its own copy. A fire request handled by worker A will not have its poll_ids available if the verify request lands on worker B.
**Recommended fix:** Store poll_ids in Valkey (keyed by scenario name + short TTL) instead of a module-level dict.

**P1-OPS-06: Readiness endpoint does not check Ollama.**
The `/readiness` endpoint checks PostgreSQL and Valkey but not Ollama. Since the health check pipeline's ACT stage depends on Ollama for report generation (with fallback), the readiness probe should indicate when Ollama is unavailable so operators know report quality will be degraded.
**Recommended fix:** Add Ollama health check to `/readiness` as a non-blocking dependency (report degraded status but don't fail readiness).

**P1-OPS-07: No rate limiting on devops monitor API endpoints.**
The pipeline monitor's `/monitor/api/pipeline-state` runs COUNT(*) queries across 3 schemas (17 tables). A rapid poll loop could create significant DB load. The endpoint has no rate limiting.
**Recommended fix:** Apply Flask-Limiter to devops monitor API routes (e.g., 30/minute for pipeline-state).

### P2 — Post-Launch

**P2-OPS-08: MCP server `canary-ops` is a ghost entry.**
The streamable_server.py registers `"ops": "/ops-mcp"` with a TODO comment noting no corresponding blueprint exists. The 8 MCP tools documented in the original SDD are not wired to any implementation.
**Recommended fix:** Either implement the ops MCP blueprint or remove the ghost registry entry.

**P2-OPS-09: Health check session data has no retention policy.**
Valkey sessions TTL out (1 hour for HC, 2 hours for sim), but the Owl sessions, findings, and merchant memory written during the ACT stage persist indefinitely in PostgreSQL. Demo-mode health check runs create real rows in `owl_sessions`, `owl_findings`, and `owl_merchant_memory` that accumulate without cleanup.
**Recommended fix:** Add a retention sweep for demo-mode Owl artifacts (flag demo sessions with a source field, purge after 30 days).

**P2-OPS-10: Valkey state not encrypted in transit.**
Health check session state (including heartbeat scores, report JSON, and merchant_id) is stored in Valkey without TLS. In a production AWS deployment, ElastiCache should be configured with in-transit encryption.
**Recommended fix:** Enable TLS on ElastiCache Valkey; configure Valkey clients with `ssl=True`.

**P2-OPS-11: DevOps monitor creates a new DB session per helper call.**
Each internal helper (`_query_ingestion_log`, `_query_evidence_records`, etc.) calls `_get_session()` independently, creating and closing its own DB session. The `pipeline_state` endpoint calls `_get_table_counts()` (1 session) + `_get_recent_events_all()` (4 sessions) + potentially more. This is 5+ DB sessions per single API call.
**Recommended fix:** Pass a single session through the call chain or use a request-scoped session.

**P2-OPS-12: Config service sessions not consistently closed on error paths.**
`update_config()` calls `session.rollback()` in the except block but doesn't close the session. `get_config_value()` gets a session but never closes it. These are minor leaks that the connection pool handles, but they should be explicit.
**Recommended fix:** Use context managers or try/finally blocks for all session handling in config_service.py and feature_flags.py.

## Production Readiness Checklist

- [x] PII classified per field (see PII Classification table)
- [ ] PII encrypted at rest — IP addresses in ingestion_log stored plaintext (P0-OPS-01)
- [ ] Secrets in AWS Secrets Manager (not .env) — 12 secret env vars still in .env files
- [x] Health check endpoint responds (`/health` liveness, `/readiness` dependency check)
- [ ] Audit logging for sensitive operations — no audit trail for config/flag changes (P1-OPS-04)
- [ ] Data retention policy implemented — demo Owl artifacts accumulate indefinitely (P2-OPS-09)
- [ ] Rate limiting on internal API endpoints — devops monitor unthrottled (P1-OPS-07)
- [x] Error responses don't leak internals — generic error messages in ops console API
- [x] SQL injection prevention — `_ALLOWED_TABLES` frozenset on all pipeline monitor queries
- [x] Sandbox gating enforced — `before_request` hooks block production access on ops console and devops monitor
- [x] Auth required on all non-health endpoints — session+admin on ops console, session/API-key on devops monitor
- [x] Graceful degradation documented — Valkey, PostgreSQL, Ollama, Square API all have fallback paths
- [ ] Config values never logged in plaintext — current code logs values on update (P0-OPS-02)
- [ ] Feature flag mutations authorized at service layer — no auth in service functions (P0-OPS-03)
- [x] Access token excluded from serialization — `access_token` never written to Valkey
