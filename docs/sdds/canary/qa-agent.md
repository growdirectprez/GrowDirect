# QA Agent

> **Status:** Ops-upgraded — code-reviewed for production readiness
> **Type:** MCP Server (Canary)
> **Namespace:** canary
> **Last updated:** 2026-04-13
> **Code location:** `Canary/canary/services/qa_agent/`
> **Linear:** GRO-326

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]

---

## Purpose

The QA Agent is a Claude-powered interactive test assistant running as a sidecar container for the Canary Ops Console. It provides a conversational interface to interrogate live Canary system state via 62 in-process MCP tools, fire Square Sandbox test scenarios, and diagnose detection pipeline behavior. The agent is scoped to the Square Sandbox environment and holds no persistent state -- all conversation history lives in the browser.

---

## Dependencies

| Dependency | Type | Required |
|---|---|---|
| `growdirect_postgres` (canary DB) | Database | Yes -- QA-only tools query DetectionRule, live_fire_poll |
| Anthropic API (`claude-sonnet-4-20250514`) | External API | Yes -- all chat requests |
| Anthropic Python SDK (`anthropic`) | Python package | Yes -- lazy-imported at request time |
| `uvicorn` | Python package | Yes -- ASGI server for sidecar |
| `requests` | Python package | Yes -- Flask proxy to sidecar |
| Canary Flask app (port 5001) | Upstream service | Yes -- proxies chat requests |
| Canary MCP registries (8 services) | In-process | Yes -- Atlas, Alerts, Analytics, Chirp, Fox, Identity, Owl, TSP |
| `canary.services.scenario_fire` | In-process | Yes -- fire_scenario, SCENARIO_REGISTRY |
| `canary.services.health_check.chirp_lab` | In-process | Yes -- live_fire_poll |
| Docker network `growdirect` | Infrastructure | Yes -- Flask-to-sidecar routing |
| Flask-Limiter (`canary.extensions.limiter`) | In-process (Flask side) | Yes -- 10/min rate limit |

---

## Data Flow & PII Map

### What enters

- **User messages** via `POST /ops/qa/chat` -- JSON array of `{role, content}` messages. Content may include a merchant UUID prefix injected by the browser (`[Page: ... | Merchant: <uuid>]`).
- **Session ID** (optional) -- string identifier for per-session rate limiting. Currently not propagated from Flask; all requests share the `"default"` bucket.

### What's stored

Nothing persistent. The QA Agent stores no data of its own. Rate-limit counters (`_session_counts`, `_daily_count`) are module-level Python dicts in the sidecar process. They reset on every container restart.

### What exits

- **To Anthropic API:** Full conversation history (system prompt + messages + tool results). Tool results may include merchant names, employee names, location names, transaction amounts, alert details, and detection rule configurations read from the Canary database. These are sent to the Anthropic API as context for Claude's response.
- **To browser:** Final text response, list of tool calls invoked (name + input params), model identifier, and rate-limit usage counters.
- **To Canary database (write path):** `fire_scenario` creates real payments in the Square Sandbox via the Square API. These payments flow through the TSP pipeline and may create transactions, alerts, and cases in the `canary` database.

### PII classification

| Field | Classification | Notes |
|---|---|---|
| Merchant UUID | internal | Extracted from browser context, passed to MCP tools |
| Merchant name | internal | Returned by Identity tools, forwarded to Anthropic API |
| Employee names | internal | Returned by Identity tools |
| Location names | public | Returned by Identity tools |
| Transaction amounts | internal | Returned by TSP/Alert tools |
| Alert details (rule IDs, severities) | internal | Returned by Alert/Chirp tools |
| Detection rule thresholds | internal | Returned by Chirp/QA tools |
| Conversation history | internal | Sent in full to Anthropic API on every turn |
| ANTHROPIC_API_KEY | restricted | Read from environment, never logged or returned |

**Note:** All data is Square Sandbox data in development. In production, if the sandbox-only guard were bypassed, real merchant data would flow through the Anthropic API. The `ops_guard` before_request check on the Flask blueprint enforces `SQUARE_ENVIRONMENT == "sandbox"`.

---

## API Contract

### HTTP: Flask Routes (public-facing, behind ops_guard)

Both routes are registered on `ops_console_bp` under the `/ops` prefix. The `ops_guard` before_request handler enforces: (1) `SQUARE_ENVIRONMENT == "sandbox"`, (2) authenticated session via `load_session_user()`, (3) admin role via `has_any_role("admin")`.

**GET `/ops/qa`** -- Renders the QA Agent chat UI. Returns HTML.

**POST `/ops/qa/chat`** -- Rate limit: 10 req/min per IP (Flask-Limiter).

Request:
```json
{
  "messages": [
    {"role": "user", "content": "[Page: /alerts | Merchant: <uuid>] What alerts fired today?"}
  ]
}
```

Response (always HTTP 200 unless server error):
```json
{
  "text": "Three high-priority alerts fired today...",
  "tool_calls": [
    {"tool": "list_alerts", "input": {"merchant_id": "<uuid>", "severity": "high"}}
  ],
  "model": "claude-sonnet-4-20250514",
  "usage": {
    "session_remaining": 47,
    "daily_remaining": 193
  }
}
```

### HTTP: Sidecar Routes (internal only, Docker network)

Container `canary_localhost_qa_agent`, port 8002. Not exposed through nginx.

**GET `/health`** -- Docker healthcheck. Returns `{service, status, daily_usage, daily_limit}`.

**POST `/chat`** -- Internal endpoint called by Flask `agent.py` only. Same request/response shape as `/ops/qa/chat`.

---

## MCP Tool Registry

62 tools total: 58 from 8 MCP service registries + 4 QA-only tools. All execute in-process inside the sidecar (no HTTP round-trips).

### Atlas (6 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `atlas_figure` | None | None | Sidecar | Load atlas figure by ID |
| `atlas_search` | None | None | Sidecar | Search atlas figures by keyword |
| `atlas_validate` | None | None | Sidecar | Validate figure syntax and completeness |
| `atlas_index` | None | None | Sidecar | Return atlas index in summary/full/embedding format |
| `atlas_render` | None | None | Sidecar | Render figure to SVG/PNG |
| `atlas_drift` | None | None | Sidecar | Drift detection vs live codebase |

### Alerts (6 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `lifecycle_summary` | None | None | Sidecar | Compute alert lifecycle counts (active, stale, resolved, etc.) |
| `calculate_impact` | None | None | Sidecar | Estimate dollar impact of an alert |
| `rank_alerts` | None | None | Sidecar | Rank alerts by severity + dollar impact |
| `get_impact_summary` | None | None | Sidecar | Total dollar impact across alerts |
| `list_alerts` | None | merchant_id | Sidecar | List alerts for a merchant with filters |
| `get_alert` | None | merchant_id, alert_id | Sidecar | Get single alert with status history |

### Analytics (7 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `get_dashboard` | None | merchant_id | Sidecar | Period dashboard with health score and KPI bands |
| `get_trends` | None | merchant_id | Sidecar | Trend data for a single metric across periods |
| `get_top_risks` | None | merchant_id, employee/location names | Sidecar | Top risk employees and locations |
| `get_drilldown` | None | merchant_id, entity names | Sidecar | Detailed metrics for employee or location |
| `score_metrics` | None | None | Sidecar | Score KPI actuals against baselines (pure function) |
| `detect_velocity` | None | None | Sidecar | Statistical anomaly detection (pure function) |
| `get_period_metrics` | None | merchant_id | Sidecar | Raw KPI actuals for a fiscal period |

### Chirp (10 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `get_rules` | None | None | Sidecar | List detection rules with optional filters |
| `get_rule` | None | None | Sidecar | Look up single rule by ID |
| `evaluate_stateless` | None | None | Sidecar | Evaluate Tier 1 rules against parsed payload (pure) |
| `apply_sensitivity` | None | None | Sidecar | Compute adjusted thresholds for sensitivity level |
| `get_templates` | None | None | Sidecar | List configuration templates |
| `apply_template` | None | None | Sidecar | Apply config template, return adjusted thresholds |
| `validate_thresholds` | None | None | Sidecar | Validate proposed thresholds against rule def |
| `get_config_summary` | None | None | Sidecar | Summarize merchant rule config vs defaults |
| `estimate_sensitivity` | None | None | Sidecar | Classify current thresholds by sensitivity level |
| `get_merchant_thresholds` | None | merchant_id | Sidecar | Get merchant-specific thresholds (Valkey/DB/defaults) |

### Fox (8 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `create_case` | None | merchant_id | Sidecar | Create a new investigation case |
| `get_case` | None | merchant_id, case details | Sidecar | Get case with full details |
| `list_cases` | None | merchant_id | Sidecar | List cases with filters |
| `update_case_status` | None | merchant_id | Sidecar | Change case status |
| `add_subject` | None | merchant_id, employee names | Sidecar | Add subject to a case |
| `get_timeline` | None | merchant_id | Sidecar | Get case event timeline |
| `verify_chain` | None | None | Sidecar | Verify evidence chain hash integrity |
| `link_alert` | None | merchant_id | Sidecar | Link an alert to a case |

### Identity (6 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `get_merchant` | None | merchant name | Sidecar | Get merchant details |
| `get_settings` | None | merchant_id | Sidecar | Get merchant settings |
| `list_employees` | None | employee names | Sidecar | List employees for a merchant |
| `get_employee` | None | employee name | Sidecar | Get single employee details |
| `list_locations` | None | location names | Sidecar | List locations for a merchant |
| `get_location` | None | location name | Sidecar | Get single location details |

### Owl (8 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `the_one_thing` | None | merchant_id | Sidecar | Get the single most important insight |
| `ask` | None | merchant_id | Sidecar | Natural language question about merchant data |
| `heartbeat` | None | None | Sidecar | Owl service health check |
| `check_heartbeat` | None | None | Sidecar | Detailed Ollama/model health check |
| `score_payment` | None | transaction data | Sidecar | Score a payment for risk |
| `search` | None | merchant_id, transaction data | Sidecar | Search transactions/alerts/cases |
| `dashboard` | None | merchant_id | Sidecar | Owl dashboard summary |
| `knowledge_search` | None | None | Sidecar | Search knowledge base |

### TSP (7 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `get_stream_health` | None | None | Sidecar | Valkey stream health metrics |
| `get_dead_letters` | None | transaction data | Sidecar | List dead-letter events |
| `replay_event` | None | transaction data | Sidecar | Replay a dead-letter event |
| `get_ingestion_stats` | None | None | Sidecar | Pipeline ingestion statistics |
| `get_receipt` | None | transaction data | Sidecar | Get parsed receipt for a payment |
| `verify_merkle` | None | None | Sidecar | Verify Merkle proof for a transaction |
| `process_dead_letters` | None | transaction data | Sidecar | Batch process dead-letter events |

### QA-Only Tools (4 tools)

| Tool | Auth | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `fire_scenario` | None | Creates sandbox payments | Sidecar | Fire named test scenario in Square Sandbox |
| `poll_scenario` | None | transaction/alert data | Sidecar | Poll pipeline status for a fired scenario |
| `list_scenarios` | None | None | Sidecar | List available test scenarios |
| `get_thresholds` | None | None | Sidecar | Read detection rule thresholds from DB |

**Auth column:** "None" means the tool has no per-tool authentication. All tools rely on the blueprint-level `ops_guard` (session auth + admin role + sandbox-only) and sidecar network isolation. The tools themselves perform no authorization checks.

**Rate Limit column:** "Sidecar" means the tool is rate-limited only by the sidecar's global limits (50/session, 200/day) and the Flask-side 10/min per IP. There are no per-tool rate limits.

---

## Cross-App Data Access

The QA Agent sidecar imports the full Canary Python codebase. All 8 MCP service registries execute in-process, giving the agent read access to the entire `canary` database across all three schemas (`app`, `sales`, `metrics`).

| Schema | Access | What the agent can read |
|---|---|---|
| `app` | Read + Write (via `fire_scenario`) | Merchants, employees, locations, alerts, cases, detection rules, rule configs |
| `sales` | Read | Transactions, receipts, Merkle proofs, dead letters |
| `metrics` | Read | KPI snapshots, risk scores, heatmap data, period metrics |

**Write access:** The only write path is `fire_scenario`, which calls the Square API to create sandbox payments. These payments are then ingested by the TSP pipeline and create rows in `sales.transactions`, `app.alerts`, and potentially `app.fox_cases`. The agent itself does not perform direct database writes -- the writes happen through the normal TSP pipeline triggered by Square webhook callbacks.

Additionally, `create_case`, `update_case_status`, `add_subject`, `link_alert`, and `replay_event` are write-capable Fox and TSP tools available to the agent. These can create/modify cases and replay dead-letter events.

**Tenant isolation:** None. The QA Agent has access to all merchants in the database. The system prompt instructs Claude to use the merchant UUID from browser context, but there is no enforcement at the tool layer. Any tool can be called with any merchant_id.

**Cross-app boundary:** The agent accesses only Canary data. It has no access to Cove, Angel, or platform databases. The `CANARY_MEMORY_DB_URL` is passed to the container but is not used by any tool handler.

---

## Tool Dispatch Security

### How are tool calls authenticated?

Tool calls are not individually authenticated. The dispatch path is:

1. Browser sends messages to Flask (`POST /ops/qa/chat`).
2. Flask `ops_guard` before_request checks: sandbox-only + session auth + admin role.
3. Flask proxies to sidecar over Docker internal network.
4. Sidecar passes messages to Anthropic API, receives tool_use responses.
5. Sidecar calls `execute_tool(name, input)` in-process -- no auth check.
6. Tool executes using the sidecar's database connection (same creds as the Flask app).

The trust boundary is at step 2 (Flask ops_guard). Once a request reaches the sidecar, all 62 tools are callable without further authentication.

### Can a tool escalate privileges?

Yes, within the Canary domain. The agent can:
- **Create cases** via `create_case` -- writes to Fox case tables.
- **Modify case status** via `update_case_status` -- changes case lifecycle state.
- **Add subjects** via `add_subject` -- associates employees with cases.
- **Link alerts** via `link_alert` -- associates alerts with cases.
- **Replay dead letters** via `replay_event` -- re-injects events into the TSP pipeline.
- **Fire scenarios** via `fire_scenario` -- creates real Square Sandbox payments.

These are all within the Canary domain and gated by the sandbox-only guard. Claude decides which tools to call based on the conversation; the operator does not directly select tools.

### What happens if the sidecar is compromised?

A compromised sidecar has:
- Full read access to the `canary` database (all schemas).
- Write access to Square Sandbox (via `fire_scenario`).
- Write access to Fox cases (via case management tools).
- Write access to TSP dead letters (via `replay_event`).
- Access to `ANTHROPIC_API_KEY` (could make arbitrary Anthropic API calls).
- No access to production Square environment (sandbox-only config).
- No access to Cove, Angel, or platform databases.

The sidecar does not have network access to the internet (Docker network isolation), but it does have access to the Anthropic API endpoint (required for operation).

---

## Operations

### Startup sequence

1. Shared infrastructure must be running (`growdirect_postgres`, `growdirect_valkey`).
2. Flask container starts and becomes healthy (healthcheck on port 5001).
3. QA Agent sidecar starts (`python -m canary.services.qa_agent.server`), binds port 8002.
4. On first chat request, MCP registries are lazy-loaded and cached.

### Health checks

| Endpoint | Interval | What it checks |
|---|---|---|
| `GET /health` (sidecar, port 8002) | 10s (compose), 30s (Dockerfile) | Returns JSON with service name, status, daily usage |
| Flask healthcheck (port 5001) | 10s | urllib request to `/health` |

### Failure modes

| Failure | Impact | Recovery |
|---|---|---|
| Sidecar container down | Chat returns "QA agent sidecar is not running" | Auto-restart (unless-stopped policy) |
| Anthropic API key missing | Chat returns "ANTHROPIC_API_KEY not configured" | Add key to `.env`, restart container |
| Anthropic API error | Chat returns "Claude API error: ..." with partial tool_calls | Retry request |
| MCP registry load failure | Affected tools absent from catalog; other tools work | Restart sidecar |
| Database unavailable | QA-only tools (poll_scenario, get_thresholds) fail; pure-function tools still work | Restore database |
| Anthropic API timeout (>120s) | Chat returns "QA agent timed out" | Simplify question |
| Tool dispatch loop exhaustion (10 iterations) | Chat returns "Agent reached maximum tool depth" | Simplify question |
| Daily rate limit (200) reached | Chat returns "Daily limit reached" | Wait for container restart or next day |

### Monitoring

| Metric | Normal range | Alert threshold |
|---|---|---|
| Daily message count | 0-50 | >150 (approaching 200 limit) |
| Sidecar response time | 2-30s | >60s |
| Tool dispatch iterations per request | 1-3 | >7 (approaching 10 max) |
| MCP registry tool count at startup | 58 | <50 (registry load failures) |

### Configuration

| Variable | Default | Description |
|---|---|---|
| `QA_AGENT_URL` | `http://qa-agent:8002` | Sidecar URL (read by `agent.py`) |
| `ANTHROPIC_API_KEY` | (required) | Anthropic API key (read at request time) |
| `QA_AGENT_PORT` | `8002` | Sidecar bind port |
| `DEFAULT_MODEL` | `claude-sonnet-4-20250514` | Model for Anthropic API calls (module constant, not env-overridable) |
| `CANARY_DB_URL` | (required) | PostgreSQL connection for QA-only tool handlers |
| `CANARY_MEMORY_DB_URL` | (passed but unused) | Memory bus DB connection |
| `MAX_MESSAGES_PER_SESSION` | `50` | In-memory per-session limit (code constant) |
| `MAX_MESSAGES_PER_DAY` | `200` | In-memory daily limit (code constant) |

---

## Deployment

### Docker service definition

```yaml
# From Canary/devops/docker-compose.localhost.yml
qa-agent:
  image: canary-qa-agent
  build:
    context: ..
    dockerfile: Dockerfile.qa-agent
  container_name: canary_localhost_qa_agent
  ports:
    - "8002:8002"      # localhost debug access
  env_file:
    - ../.env
  environment:
    QA_AGENT_PORT: "8002"
    CANARY_ENV: standalone
    CANARY_AUTH_MODE: stub
    CANARY_DB_BACKEND: postgresql
    CANARY_DB_URL: postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/canary
    CANARY_MEMORY_DB_URL: postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory
  depends_on:
    flask:
      condition: service_healthy
  healthcheck:
    test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8002/health')"]
    interval: 10s
    timeout: 5s
    retries: 5
    start_period: 15s
  restart: unless-stopped
  networks:
    - growdirect
```

The sidecar uses `Dockerfile.qa-agent` -- a two-stage build (builder + production) based on `python:3.12-slim`. It copies the full Canary codebase because MCP registries import models and services. Runs as non-root user `canary`.

### AWS target

| Component | AWS Service | Notes |
|---|---|---|
| Sidecar container | ECS/Fargate | Single task, no autoscaling needed (low traffic internal tool) |
| Anthropic API key | Secrets Manager | Currently in `.env` -- must migrate |
| Database connection | RDS (shared `canary` instance) | Same credentials as Flask app |
| Networking | VPC private subnet | Sidecar should not be reachable from internet |

### CI/CD requirements

- Sidecar image rebuild on any change to `Canary/canary/` (shares full codebase).
- Unit tests: `python3 -m pytest Canary/tests/unit/test_qa_agent_tools.py -v`.
- No integration tests against Anthropic API (mocked in tests).
- Healthcheck validation after deploy.

---

## Code Review Findings

### F1: No per-tool authorization -- any tool callable with any merchant_id

**Severity:** P1 (before GA)

MCP tools execute in-process with no per-call authorization. The `ops_guard` at the Flask blueprint level enforces admin role and sandbox-only, but once a request reaches the sidecar, any of the 62 tools can be called with any `merchant_id`. In a multi-tenant production scenario, this means an admin user could query data for merchants they should not have access to.

**Current mitigation:** Sandbox-only guard prevents production data exposure. The tool set is only accessible to admin-role users in the Ops Console.

**Recommended fix:** Add a merchant_id allowlist or tenant-scoping middleware in the sidecar's `execute_tool` path. For sandbox/dev this is low risk; for production multi-tenant, tool calls must validate the requesting user's merchant scope.

### F2: Session ID not propagated -- per-session rate limit is shared across all users

**Severity:** P1 (before GA)

`agent.py` does not extract a session or user identifier from the Flask session and forward it to the sidecar. All requests arrive with `session_id = "default"`, so the 50-message per-session limit applies to all users collectively. One heavy user consumes the session budget for everyone.

**Recommended fix:** Extract `session['user_id']` or a browser-generated session token in `qa_agent_chat()` and include it in the JSON body forwarded to the sidecar.

### F3: In-memory rate limits reset on container restart

**Severity:** P2 (post-launch)

`_session_counts` and `_daily_count` are process-local. Container restarts (intentional or crash-loop) reset all counters. The 200/day limit is a soft cost guardrail, not a hard one.

**Recommended fix:** Move rate-limit counters to Valkey with TTL-keyed structure (`qa:session:<id>` with 1-hour TTL, `qa:daily` with 24-hour TTL).

### F4: Sidecar port 8002 exposed to host in compose

**Severity:** P2 (post-launch)

The compose file maps port 8002 to localhost (`"8002:8002"`). This is intentional for dev debugging but must be removed in production compose. The sidecar should only be reachable on the Docker internal network.

**Recommended fix:** Remove port mapping in production compose. Use `expose: - "8002"` instead of `ports:`.

### F5: Blocking I/O in async handler

**Severity:** P2 (post-launch)

`handle_chat` is `async` but calls `client.messages.create()` synchronously. With a single uvicorn worker, concurrent requests queue behind the in-flight Anthropic API call (which can take 10-120 seconds). For a low-traffic internal tool this is acceptable.

**Recommended fix:** Migrate to `anthropic.AsyncAnthropic` or use `asyncio.to_thread()` to offload the blocking call. Alternatively, run multiple uvicorn workers if concurrency becomes an issue.

### F6: ANTHROPIC_API_KEY in .env file

**Severity:** P0 (blocks prod)

The Anthropic API key is stored in the `.env` file and loaded via `env_file` in Docker Compose. In production, secrets must be in AWS Secrets Manager.

**Recommended fix:** Use `boto3` to retrieve `ANTHROPIC_API_KEY` from Secrets Manager at startup. Add a fallback to environment variable for local development.

### F7: No audit logging for tool calls

**Severity:** P1 (before GA)

Tool invocations are logged at INFO level (`QA Agent -> MCP: tool_name(input)`) but there is no structured audit trail. In production, there should be a record of which user called which tools with which inputs and what data was returned.

**Recommended fix:** Add structured JSON audit logging for each tool dispatch: `{timestamp, user_id, session_id, tool_name, input_params, result_size, duration_ms}`. Write to a dedicated audit log or database table.

### F8: Write-capable tools accessible without explicit confirmation

**Severity:** P1 (before GA)

Fox tools (`create_case`, `update_case_status`, `add_subject`, `link_alert`) and TSP tools (`replay_event`) can modify database state. Claude decides when to call these based on conversation context. There is no human-in-the-loop confirmation before write operations execute.

**Recommended fix:** Add a `requires_confirmation` flag to write-capable tools. The sidecar should return a confirmation prompt to the browser before executing these tools, or restrict them to a read-only tool set for non-admin users.

### F9: No CSRF protection on JSON endpoint

**Severity:** P2 (post-launch)

`POST /ops/qa/chat` accepts JSON bodies. Flask-WTF CSRF protection applies to form POSTs, not JSON. The endpoint relies on session auth + rate limiting. A CSRF attack would require the attacker to forge a JSON POST with valid session cookies.

**Recommended fix:** Add `X-Requested-With` header validation or a custom CSRF token in the JSON body for defense-in-depth.

### F10: Conversation history sent to Anthropic API contains Canary data

**Severity:** P1 (before GA)

Every turn sends the full conversation history (including previous tool results) to the Anthropic API. Tool results may contain merchant names, employee names, transaction amounts, and alert details. For sandbox data this is acceptable. For production data, this constitutes sending internal business data to a third-party API.

**Recommended fix:** Document in the data processing agreement with Anthropic. Consider truncating or redacting tool results in the message history before re-sending (currently only truncated at 8000 chars for token cost, not for PII). Alternatively, scope the QA Agent to sandbox-only permanently and build a separate, PII-aware assistant for production.

---

## Production Readiness Checklist

- [ ] **PII encrypted at rest** -- N/A for QA Agent itself (stateless), but data it reads from other services is not encrypted at the field level. Covered by service-level SDDs.
- [x] **Secrets in AWS Secrets Manager (not .env)** -- NOT MET. `ANTHROPIC_API_KEY` is in `.env`. See F6.
- [x] **Health check endpoint responds** -- MET. `GET /health` on port 8002.
- [ ] **Audit logging for sensitive operations** -- NOT MET. Tool calls logged at INFO but no structured audit trail. See F7.
- [ ] **Data retention policy implemented** -- N/A (stateless service, no persistent data).
- [x] **Rate limiting on public endpoints** -- MET. Flask-Limiter 10/min on `/ops/qa/chat` + sidecar 50/session + 200/day.
- [x] **Error responses don't leak internals** -- MET. All errors return `{text, tool_calls, model}` shape. Exception messages are included in `text` but these are Anthropic SDK errors, not stack traces.
- [ ] **Per-tool authorization** -- NOT MET. See F1.
- [ ] **Session-scoped rate limiting** -- NOT MET. See F2.
- [x] **Sandbox-only guard** -- MET. `ops_guard` checks `SQUARE_ENVIRONMENT == "sandbox"`.
- [x] **Network isolation** -- MET in Docker. Port 8002 exposed to localhost for debug; must be removed for production. See F4.
- [ ] **Write operation confirmation** -- NOT MET. See F8.

---

## Testing

Tests: `Canary/tests/unit/test_qa_agent_tools.py`

| Class | Coverage |
|---|---|
| `TestDynamicToolLoading` | Registry loads 10+ tools; Atlas and Alert tools present; all defs have name, description, schema |
| `TestMCPDispatch` | `execute_tool` dispatches to Atlas; unknown tool returns error |
| `TestQAOnlyTools` | `list_scenarios` returns non-empty list with name keys |
| `TestAgentProxy` | `chat()` returns correct shape on success and sidecar-down; SYSTEM_PROMPT exists |
| `TestSidecarServer` | `handle_chat` handles empty messages, missing API key, rate limits; `build_canary_mcp_server` returns non-None |

**Gaps:** No integration tests against Anthropic API. MCP dispatch tests call live Atlas registry (may fail in CI without database). No tests for write-capable tools (create_case, fire_scenario). No tests for rate-limit counter behavior across multiple requests.

```bash
cd ~/GrowDirect/Canary
python3 -m pytest tests/unit/test_qa_agent_tools.py -v
```

---

## Known Issues & Reconciliation

**Namespace placement.** The QA Agent lives at `Canary/canary/services/qa_agent/` and runs as a Canary sidecar. It is accessed through the Canary Ops Console and requires Canary MCP registries in-process. There is no separate ALX container.

**`build_canary_mcp_server` not in live path.** `tools.py` implements `build_canary_mcp_server()` for future Claude Agent SDK headless support. The live sidecar uses `handle_chat` with direct `execute_tool` dispatch. The SDK builder is tested but not exercised end-to-end.

**CANARY_MEMORY_DB_URL passed but unused.** The sidecar container receives this environment variable but no tool handler uses it. It can be removed from the compose configuration.
