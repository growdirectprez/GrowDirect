# Ops

## Overview

The Ops domain owns internal tooling for health check orchestration, synthetic data generation, pipeline monitoring, and configuration management. None of this is merchant-facing. All testing tools are sandbox-gated (`SQUARE_ENVIRONMENT == "sandbox"`). The domain has no persistent ORM models of its own — session state lives in Valkey with TTLs, and all DB writes go to tables owned by other domains (canary_sales transactions, canary_app alerts/owl_sessions).

**Health Check Pipeline** is the primary feature: an 8-stage state machine that runs a full merchant assessment. Stages progress forward-only: `created` -> `oauth` -> `ingest` -> `load` -> `analyze` -> `present` -> `act` -> `completed`. Any stage failure transitions to `aborted`. State is persisted to Valkey (`hc:session:{uuid}`, 1-hour TTL) and polled by the ops UI. The orchestrator runs in a daemon thread — `start_session()` returns immediately, the UI polls `get_session_state()`.

**Architecture split:** `runner.py` handles threading, Valkey persistence, and the public API. `session.py` contains the state machine (SessionStage enum, HealthCheckSession dataclass, HealthCheckOrchestrator). This separation keeps infrastructure concerns out of business logic.

**Three data generators** at different scales, each with prefixed IDs for deterministic cleanup:

- `MerchantSimulator` (`sim-` prefix) — Full-quarter (14 weeks) pipeline pump. Builds Square-format webhook payloads, runs them through real production parsers (`parse_payment`, `parse_order_line_items`, `parse_order_tenders`). Models employee pools, shift patterns, day-of-week volume curves, and 6 progressive anomaly patterns. Background execution via Valkey state tracking (`sim:session:{uuid}`, 2-hour TTL).
- `DataFactory` (`hc-` prefix) — Single-day transaction generator. Direct ORM inserts (no parser pipeline). Three profiles: cafe (40-60 txns), retail (15-30), restaurant (20-40). Four embedded suspicious patterns (rapid refund, after-hours, high-value refund, round-dollar). Used by Health Check demo mode.
- `ChirpLab` (`lab-` prefix) — Single-transaction firing range. Two modes: local fire (ORM insert + Chirp evaluation) and live fire (real Square Payments API in sandbox, polls for webhook roundtrip). Includes scoreboard for all 26 Chirp rules.

**Heartbeat scoring** is a pure function: severity-weighted deductions from a 100-point baseline (critical=25, high=15, medium=8, low=3, info=0). Band classification: healthy (90-100), normal (70-89), warning (40-69), alert (0-39). HeartbeatResult is a frozen dataclass — immutable, no DB, no side effects.

**Report generation** uses three professional assessment lenses (Loss Prevention, Operations, Analytics). LLM path via Ollama qwen3:14b (120s timeout, JSON mode, think=false). Deterministic fallback when LLM is offline. Post-validation patches hallucinated scores (+/-15 tolerance regex) and finding trends against delta engine output. Legacy field migration (jim->lp, tom->ops, phd->analytics).

**DevOps Pipeline Monitor** provides real-time TSP pipeline visibility across 4 stages (ingestion, sealed, parsed, batched). Reads table counts from all three databases via SQL-injection-safe allowlist (`_ALLOWED_TABLES` frozenset). Monitors Valkey streams (lengths, consumer groups, pending messages). Event tracing follows a single event across stages using event_id as correlation key.

**Config Service** provides centralized configuration with a 3-level resolution chain: AppConfig DB value > ENV var > CONFIG_REGISTRY default. 35 registered env vars across 6 categories (database, auth, general, square, cms, monitoring). Secrets are masked in the health dashboard and blocked from update via the editor.

**Feature Flags** support per-merchant overrides with 3-tier resolution: merchant override > global DB flag > ENV var fallback. Three ENV-backed flags: billing_enabled (false), audit_logging_enabled (true), api_keys_enabled (false). Graceful degradation — DB failure falls through to ENV-only flags.

**Health blueprint** provides `/health` (liveness, always 200, no deps) and `/readiness` (stub, planned dependency checks for DB/Valkey/Keycloak).

**MCP server:** `canary-ops` with 8 tools at `/ops-mcp/*`. Blueprints: `ops_console` (/ops), `devops_monitor` (/devops), `ops_mcp` (/ops-mcp).

**Domain boundaries:** Inbound from UI/BFF (ops console page routes). Outbound to Chirp (chirp_lab fires rule evaluations), Owl (generate_health_report for narrative), and Webhook Pipeline (simulator generates synthetic transactions through parsers).

## API Contracts

### Ops Console (`ops_console.py` -> `/ops/*`)

All routes require sandbox environment AND admin role. Session-based auth (not JWT).

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/` | GET | Session+admin | Test lab page (single-page ops console) |
| `/test-lab` | GET | Session+admin | Legacy redirect to `/ops/` (301) |
| `/api/scenario/fire` | POST | Session+admin | Fire a named scenario via Square SDK. Input: `{scenario}`. Returns steps + poll_ids. |
| `/api/scenario/poll/<payment_id>` | GET | Session+admin | Poll webhook->pipeline status for a scenario payment. Checks ingestion_log, transactions, alerts. |
| `/api/scenario/verify-owl` | POST | Session+admin | Run Owl verification queries for completed scenario. Input: `{scenario, merchant_id?}`. Returns `{all_passed, results[]}`. |
| `/api/chirp-lab/live-fire/status` | GET | Session+admin | Check Square sandbox credentials configured. |
| `/api/chirp-lab/live-fire` | POST | Session+admin | Create real Square sandbox payment. Input: `{amount_cents, tip_amount_cents, nonce, note}`. Returns Square payment ID. |
| `/api/chirp-lab/live-fire/poll/<payment_id>` | GET | Session+admin | Poll pipeline for live-fired payment results. Returns `{webhook_received, transaction_stored, alerts, pipeline_complete}`. |

### DevOps Monitor (`devops_monitor.py` -> `/devops/*`)

Sandbox-gated via `before_request` hook. Returns 403 in production.

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/monitor` | GET | Sandbox guard | Legacy redirect to /ops/ (301) |
| `/monitor/api/pipeline-state` | GET | Sandbox guard | Full pipeline snapshot: table counts (3 DBs), Valkey stream state, last 10 events per stage |
| `/monitor/api/recent-events` | GET | Sandbox guard | Recent events by stage. Params: `stage` (ingestion/sealed/parsed/batched), `limit` (1-50, default 20) |
| `/monitor/api/event/<event_id>` | GET | Sandbox guard | Cross-stage event trace (ingestion_log, evidence_records, event_inscriptions) |

### Health Blueprint (`health.py`)

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/health` | GET | None | Container liveness. Always 200. Version from `CANARY_VERSION` env (default 0.5.0). Rate-limit exempt. |
| `/readiness` | GET | None | Dependency readiness (stub — returns hardcoded OK). |

### MCP Server (`canary-ops` at `/ops-mcp/*`)

8 tools covering health check orchestration, simulation, Chirp Lab, scenario runner, factory reset, and feature flags:

| Tool | Category | DB? | Input | Output |
|------|----------|-----|-------|--------|
| `start_health_check` | health_check | Yes | `merchant_id`, `mode?`, `profile?` | Session state dict with `session_id` |
| `poll_health_check` | health_check | No | `session_id` | Current session state from Valkey |
| `start_simulation` | simulation | Yes | `merchant_id?`, `profile?`, `weeks?`, `anomaly_density?` | Simulation session state with `session_id` |
| `poll_simulation` | simulation | No | `session_id` | Current simulation state from Valkey |
| `fire_chirp` | chirp_lab | Yes | `merchant_id`, transaction params | Alert summaries + rule fire counts |
| `run_scenario` | scenario | Yes | `scenario` name | Steps + poll IDs for pipeline tracking |
| `factory_reset` | ops | Yes | `merchant_id` | Cleanup counts by table |
| `get_feature_flags` | config | Yes | `merchant_id?` | All flags with resolution source |

### Internal Service APIs (no HTTP endpoints)

**Runner (health_check/runner.py):**

| Function | Signature | Purpose |
|----------|-----------|---------|
| `start_session` | `(merchant_id, profile="cafe", mode="demo") -> dict` | Creates session, stores initial Valkey state, launches daemon thread |
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

The Ops domain owns no persistent tables. All session state is in-memory (Valkey with TTLs). DB writes go to tables owned by other domains.

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
| `access_token` | Optional[str] | Square OAuth token (live mode) |
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
| canary_app | `app_config` | Config Service | N/A |
| canary_app | `feature_flags`, `merchant_feature_flags` | Feature Flags | N/A |

### Tables Read (Pipeline Monitor)

| Database | Tables |
|----------|--------|
| canary_sales | ingestion_log, evidence_records, transactions, transaction_line_items, transaction_tenders, inscription_pool, event_inscriptions, dead_letter_queue, refund_links |
| canary_app | webhook_events, merchants, locations, employees |
| canary_metrics | daily_metrics, hourly_metrics, employee_daily_metrics |

All monitor reads use `_safe_count()` with an `_ALLOWED_TABLES` frozenset to prevent SQL injection.

## Workflows

### Health Check Pipeline (8-Stage State Machine)

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
      |-- [INGEST] Live: InitialDataSync (30-day lookback).
      |           Demo: DataFactory.generate_merchant_day().
      |-- [LOAD] Confirm data in canary_sales CDM format.
      |-- [ANALYZE] ChirpRuleEngine.evaluate_readonly() on all txns.
      |            write_alerts_to_session() -> canary_app.
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

Volume curves by profile: cafe base=50, retail=22, restaurant=30. Day-of-week multipliers (Mon lowest 0.70-0.80, Sat highest 1.20-1.30). Business hours: cafe 6-18, retail 10-20, restaurant 11-22.

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

Report has 8 required fields: executive_summary, findings[], lp_assessment, ops_assessment, analytics_assessment, top_priority, positive_notes, outlook. Each finding has: category, severity, title, detail, trend, recommendation.

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
| Live mode lookback | Configurable via `MerchantSettings.lookback_days` (GRO-258). Default 30 days. NULL = all available history. Settings UI has 7d/30d/90d/All selector. Was hardcoded 30 days. | InitialDataSync |
| `CANARY_VERSION` | 0.5.0 | /health response |
