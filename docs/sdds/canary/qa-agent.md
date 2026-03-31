# QA Agent

> **Status:** Complete — written from code
> **Namespace:** canary
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/qa_agent/`
> **Linear:** GRO-326

---

## 1. Overview

The QA Agent is a Claude-powered interactive test assistant embedded in the Canary Ops Console. It gives the operator a conversational interface to interrogate live Canary system state, fire sandbox scenarios, and diagnose detection pipeline behavior — all without leaving the browser.

The agent is scoped to the Square Sandbox environment. It has no write access to production data. Its primary purpose is to accelerate QA and debug cycles during development and pre-release validation.

**Core capabilities:**

- Query live Canary system state (alerts, cases, transactions, rules, streams) via 30+ MCP tools.
- Fire named test scenarios against the Square Sandbox and poll the full detection pipeline for results.
- Surface rule thresholds, TSP ingestion health, and Owl search behavior in plain language.
- Maintain merchant context automatically from browser page state — operators do not need to re-supply IDs.
- Emit deep links back into the Canary app for any referenced entity (alert, case, search query, setting).

The agent does not maintain persistent state between browser sessions. All conversation history lives in the browser and is forwarded with each request. There is no database schema for this service.

---

## 2. Architecture

### Component Diagram

```
Browser (ops/qa page)
    │  POST /ops/qa/chat  (JSON, full message history)
    │  10 req/min rate limit (Flask-Limiter)
    ▼
Flask Blueprint (ops_console_bp)
    │  calls chat(messages)
    ▼
canary/services/qa_agent/agent.py  ← Flask-side proxy
    │  POST http://qa-agent:8002/chat  (120 s timeout)
    ▼
qa-agent container (uvicorn ASGI, port 8002)
    │  canary/services/qa_agent/server.py
    │  in-memory rate limiting (50/session, 200/day)
    │  builds Anthropic client
    │  passes SYSTEM_PROMPT + tool_definitions + messages
    ▼
Anthropic API (claude-sonnet-4-20250514, max_tokens=4096)
    │  tool_use response block
    ▼
canary/services/qa_agent/tools.py  ← tool dispatch (in-process)
    ├── MCP registry tools (Atlas, Alerts, Analytics, Chirp,
    │   Fox, Identity, Owl, TSP) — lazy-loaded, cached
    └── QA-only tools (fire_scenario, poll_scenario,
        list_scenarios, get_thresholds)
    │  result (JSON, truncated at 8000 chars)
    ▼
Anthropic API (tool_result → next message turn)
    │  up to 10 tool dispatch iterations
    ▼
Final text response → Flask → Browser
```

The sidecar runs its own ASGI process (uvicorn) independent of the Gunicorn Flask workers. Flask has no Anthropic SDK dependency — it only speaks HTTP to the sidecar. This boundary makes the underlying dispatch engine swappable without touching Flask code.

### Request / Data Flow

1. **Browser** accumulates the full conversation as a `messages` array (OpenAI-compatible format: `[{role, content}]`). On each user turn it POSTs the full array to `POST /ops/qa/chat`.

2. **Flask blueprint** (`ops_console_bp`) validates that at least one message exists, then calls `agent.chat(messages)`. Flask-Limiter enforces 10 requests per minute per IP at this layer.

3. **`agent.py` proxy** forwards the messages array to the sidecar at `http://qa-agent:8002/chat` (configurable via `QA_AGENT_URL`). The HTTP call has a 120-second timeout. Connection errors and timeouts are caught and returned as structured error responses with the same `{text, tool_calls, model}` shape as a successful response — the browser never sees a non-200.

4. **Sidecar `server.py`** checks in-memory rate limits (per-session and daily), retrieves `ANTHROPIC_API_KEY` from environment, then enters the tool dispatch loop.

5. **Tool dispatch loop** (max 10 iterations):
   - Calls `client.messages.create()` with the full message history, system prompt, and tool definitions.
   - If the response contains a `tool_use` block, `execute_tool(name, input)` is called in-process for each tool.
   - Tool results are appended as a `user` role message with `tool_result` content blocks.
   - If no `tool_use` block is present, the loop exits and the final text content is collected.
   - If 10 iterations are exhausted without a pure-text response, a max-depth error is returned.

6. **Tool execution** (`tools.py`) routes to the appropriate MCP registry tool or QA-only handler. MCP tool results are unwrapped from the `{tool, ok, result, timestamp}` envelope. Results longer than 8000 characters are truncated before being sent back to the Anthropic API to control token consumption.

7. **Response** is returned as `{text, tool_calls, model, usage}` where `usage` carries `session_remaining` and `daily_remaining` counts. The browser renders the text and may use `tool_calls` to display which tools were invoked.

### Key Design Decisions

**Sidecar over in-process SDK.** The Claude Agent SDK at time of implementation (GRO-326) requires a TTY / Claude Code binary and does not support headless Docker containers. Rather than block the feature, the sidecar wraps the Anthropic Python SDK directly in a minimal ASGI process. The architecture isolates all SDK concerns in one container; when the SDK gains headless support the swap is a one-file change in `server.py`.

**Minimal ASGI, no framework.** The sidecar uses a hand-written ASGI `app` function under uvicorn with only two routes (`POST /chat`, `GET /health`). No Flask, no FastAPI. This minimizes the dependency surface of the sidecar image and keeps its startup time fast.

**In-process tool execution.** MCP tools execute inside the sidecar process by importing the same Python registries used by the Canary Flask app. This means no HTTP round-trips for tool calls — they are synchronous function calls. The tradeoff is that the sidecar image must include the full Canary codebase (same Dockerfile base), which it does via `Dockerfile.qa-agent`.

**Stateless message history.** The browser owns the conversation. Every request carries the full history. This means the sidecar holds no per-session conversation state — it is fully stateless between requests. The only in-process state is the rate-limit counters, which reset on container restart.

**Schema normalization at tool load time.** `get_tool_definitions()` normalizes MCP `inputSchema` (camelCase) to Claude API `input_schema` (snake_case) and unwraps double-nested schemas that some `to_mcp()` implementations produce. This runs once at startup (lazy, cached) so per-request overhead is zero.

**Dual tool surface.** The tool catalog is split into two groups: MCP registry tools (loaded dynamically from eight service registries) and QA-only tools (`fire_scenario`, `poll_scenario`, `list_scenarios`, `get_thresholds`) that have no MCP equivalent. The QA-only tools live directly in `tools.py` with their own handlers. Both groups are merged into the single `tool_definitions` list passed to the Anthropic API.

---

## 3. Data Model

N/A. The QA Agent is a stateless tool proxy. It persists no data of its own. All data it surfaces belongs to other Canary services (Chirp rules, Fox cases, TSP stream health, etc.) and is read from their respective stores via MCP tools at query time.

Rate-limit counters (`_session_counts`, `_daily_count`) are module-level Python dicts in the sidecar process. They reset on every container restart and are never written to any database or cache.

---

## 4. Interfaces

### HTTP: Flask Routes (public-facing)

Both routes are registered on `ops_console_bp` under the `/ops` prefix via the main app factory.

**GET `/ops/qa`**

Renders the QA Agent chat UI (`templates/ops/qa.html`). No authentication beyond the existing `ops_console_bp` access control. Returns HTML.

**POST `/ops/qa/chat`**

Rate limit: 10 requests/minute (Flask-Limiter, per-IP).

Request body (JSON):

```json
{
  "messages": [
    {"role": "user", "content": "[Page: /alerts | Merchant: <uuid>] What alerts fired today?"}
  ]
}
```

The `messages` array follows the Anthropic Messages API format. The browser accumulates the full conversation and re-sends it on every turn. Page context and merchant UUID are injected as a prefix on the first content string of each user message by the frontend.

Response body (JSON, always HTTP 200 unless server error):

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

On sidecar connection failure or timeout, `text` carries a human-readable error description and `tool_calls` is an empty array. HTTP status remains 200 so the browser can display the error inline.

Error response (HTTP 400 — empty messages array):

```json
{"text": "No message provided.", "tool_calls": [], "model": null}
```

### HTTP: Sidecar Routes (internal only, not exposed through nginx)

The sidecar container (`canary_localhost_qa_agent`) binds port 8002. On localhost it is accessible for debugging; in production it should only be reachable on the Docker internal `growdirect` network.

**GET `/health`**

Returns service status and daily usage counters. Used by Docker healthcheck.

```json
{
  "service": "canary-qa-agent",
  "status": "healthy",
  "daily_usage": 14,
  "daily_limit": 200
}
```

**POST `/chat`**

Internal endpoint. Flask `agent.py` is the only caller.

Request body (JSON):

```json
{
  "messages": [...],
  "session_id": "optional-string"
}
```

`session_id` is used to track per-session message counts against `MAX_MESSAGES_PER_SESSION`. If omitted, `"default"` is used — all sessionless callers share one bucket.

Response body: same shape as the Flask `/ops/qa/chat` response (see above), including `usage`.

### Tool Catalog

The sidecar exposes the following named tools to the Anthropic API. All MCP registry tools use the prefix `mcp__canary__` in the system prompt but are referenced without prefix in the API call.

**MCP Registry Tools (dynamically loaded from 8 service registries):**

| Registry | Sample tools |
|---|---|
| Atlas | `atlas_figure`, `atlas_search`, `atlas_validate`, `atlas_index` |
| Alerts | `list_alerts`, `get_alert`, `lifecycle_summary`, `rank_alerts` |
| Analytics | `get_dashboard`, `get_trends`, `get_top_risks`, `score_metrics` |
| Chirp | `get_rules`, `get_rule`, `get_config_summary`, `validate_thresholds` |
| Fox | `list_cases`, `get_case`, `get_timeline`, `verify_chain` |
| Identity | `get_merchant`, `list_employees`, `list_locations` |
| Owl | `search`, `ask`, `knowledge_search`, `score_payment` |
| TSP | `get_stream_health`, `get_ingestion_stats`, `get_dead_letters` |

**QA-Only Tools (defined directly in `tools.py`):**

| Tool | Description |
|---|---|
| `fire_scenario` | Fire a named test scenario in Square Sandbox. Creates a real payment and triggers the detection pipeline. Required param: `scenario` (string). |
| `poll_scenario` | Poll pipeline status for a fired scenario payment. Returns ingestion, transaction, and alert status. Required param: `payment_id` (string). |
| `list_scenarios` | List all available test scenarios with descriptions and the rule IDs each scenario tests. No parameters. |
| `get_thresholds` | Read current detection rule thresholds (defaults, overrides, effective values) for all rules exercised by scenarios. No parameters. |

---

## 5. Service Layer

### `agent.py` — Flask-side proxy

**`chat(messages: list[dict]) -> dict`**

The only public function. Forwards the message list to the sidecar via `requests.post`. Handles three failure modes:

- `ConnectionError` — sidecar is down. Returns `{"text": "QA agent sidecar is not running...", "tool_calls": [], "model": None}`.
- `Timeout` (120 s) — returns `{"text": "QA agent timed out...", "tool_calls": [], "model": DEFAULT_MODEL}`.
- Any other exception — logs at ERROR with traceback, returns `{"text": "QA agent error: <msg>", "tool_calls": [], "model": DEFAULT_MODEL}`.

The function never raises. Flask callers do not need try/except around it.

**`SYSTEM_PROMPT`**

Module-level constant (~600 characters). Establishes agent persona, tool-first directive, tool category listing, merchant context extraction rules, response length guidelines, and entity deep-link format. Shared with `server.py` via import.

### `server.py` — Sidecar ASGI application

**`handle_chat(data: dict) -> dict`** (async)

Main dispatch coroutine. Flow:

1. Extract `messages` and `session_id` from `data`.
2. Check session count (`_session_counts[session_id]`) against `MAX_MESSAGES_PER_SESSION` (50).
3. Check global daily count (`_daily_count`) against `MAX_MESSAGES_PER_DAY` (200).
4. Retrieve `ANTHROPIC_API_KEY` from environment; return error if missing.
5. Import `Anthropic` client (runtime import to allow the module to load without the SDK installed).
6. Load tool definitions via `get_tool_definitions()`.
7. Enter tool dispatch loop (max 10 iterations):
   - Call `client.messages.create()` synchronously (blocking I/O inside the async function — acceptable because uvicorn runs the coroutine in a single-worker event loop and the Anthropic call is the only meaningful I/O).
   - If any content block has `type == "tool_use"`: call `execute_tool(block.name, block.input)` for each, append assistant turn and tool_result user turn to `messages`, continue loop.
   - If no `tool_use` blocks: collect all `text` blocks, break.
8. Increment rate-limit counters.
9. Return `{text, tool_calls, model, usage}`.

**`app(scope, receive, send)`** (async ASGI callable)

Minimal router. Handles `GET /health` (returns JSON status) and `POST /chat` (reads body, calls `handle_chat`, returns JSON). Returns 404 for all other paths. No middleware, no auth — relies on network isolation.

**Rate limit constants:**

| Constant | Value |
|---|---|
| `MAX_MESSAGES_PER_SESSION` | 50 |
| `MAX_MESSAGES_PER_DAY` | 200 |

Counters are in-memory dicts (`_session_counts`, `_daily_count`) at module scope. They reset on sidecar restart.

### `tools.py` — Tool registry and dispatch

**`_load_registries()`** (private)

Lazy-loads all eight MCP service registries via `importlib.import_module`. Populates two module-level caches: `_registries` (dict of `tool_name → mcp_tool_object`) and `_tool_defs` (list of raw MCP tool definitions). Called once; subsequent calls are no-ops. Import failures per registry are logged as warnings and do not abort startup — the tool set degrades gracefully if a service registry fails to load.

**`get_tool_definitions() -> list[dict]`**

Returns the full merged tool catalog in Anthropic Messages API format. Performs two normalizations on registry tools:

1. `inputSchema` (camelCase, MCP convention) → `input_schema` (snake_case, Anthropic convention).
2. Double-nested schema unwrapping: some `to_mcp()` implementations nest the full schema dict under the `properties` key. This function detects that pattern and unwraps it.

Appends the four QA-only tool definitions (already in correct format) after the registry tools.

**`execute_tool(name: str, tool_input: dict) -> Any`**

Two-stage dispatch:

1. Check `_registries` (MCP tools). If found, call `t.invoke(tool_input, {})`, unwrap the `{tool, ok, result, timestamp}` envelope, return `result`.
2. Check `_QA_HANDLERS` dict. If found, call the handler function.
3. If neither matches, return `{"error": "Unknown tool: <name>"}`.

All invocation paths catch exceptions and return `{"error": "Tool <name> failed: <msg>"}` rather than propagating.

**`build_canary_mcp_server()`**

Alternative integration path for future Claude Agent SDK support. Uses `claude_agent_sdk.tool` and `create_sdk_mcp_server` to wrap every MCP registry tool and QA-only tool as an SDK custom tool. Each SDK tool delegates to `execute_tool()` and truncates results at 8000 characters. The returned server object is intended to be passed to `ClaudeAgentOptions.mcp_servers`. Currently not used in the live dispatch path (which uses `handle_chat` directly) but is tested and ready for the SDK migration.

**QA-only tool handlers:**

| Handler | Delegates to |
|---|---|
| `_handle_fire_scenario` | `canary.services.scenario_fire.fire_scenario` |
| `_handle_poll_scenario` | `canary.services.health_check.chirp_lab.live_fire_poll` (DB session) |
| `_handle_list_scenarios` | `canary.services.scenario_fire.SCENARIO_REGISTRY` |
| `_handle_get_thresholds` | `canary.models.detection_rules.DetectionRule` (DB query) |

---

## 6. Configuration

All configuration is injected via environment variables. The sidecar reads from `.env` via `env_file` in `docker-compose.localhost.yml`.

| Variable | Default | Description |
|---|---|---|
| `QA_AGENT_URL` | `http://qa-agent:8002` | URL of the sidecar. Read by `agent.py`. Override to point at a local uvicorn process for development outside Docker. |
| `ANTHROPIC_API_KEY` | (required, no default) | Anthropic API key. Read by `server.py` at request time. Missing key returns a descriptive error to the caller rather than raising. |
| `QA_AGENT_PORT` | `8002` | Port the sidecar uvicorn process binds. Read by `server.py` `__main__` block. |
| `DEFAULT_MODEL` | `claude-sonnet-4-20250514` | Model used for all Anthropic API calls. Defined as a module constant in `agent.py`; not currently overridable via environment (change the constant to make it configurable). |

The sidecar container also receives `CANARY_DB_URL` and `CANARY_MEMORY_DB_URL` because the QA-only tool handlers (`_handle_poll_scenario`, `_handle_get_thresholds`) call `get_session()` to query the Canary database directly.

---

## 7. Security & Compliance

**Session context isolation.** Merchant context (`merchant_id`) is extracted from the user message prefix injected by the browser. The agent is instructed in the system prompt to pass this UUID to all tools that accept `merchant_id`. Tools in the MCP registries enforce their own authorization checks — the QA Agent does not bypass them. Operators can only query data that the underlying MCP tools allow.

**Square Sandbox only.** The system prompt explicitly states "Environment: Square Sandbox — no real merchant data at risk." The sidecar connects to the same database as the Flask app; in the localhost compose configuration this is the `canary` database populated from Square Sandbox. No firewall rule enforces this constraint — it is a configuration-level guarantee.

**Network isolation.** The sidecar (`canary_localhost_qa_agent`) is on the `growdirect` Docker network and is not exposed through nginx. Port 8002 is bound on localhost for developer debugging but is not in the nginx upstream config. Internal requests from Flask arrive over the Docker network; external callers cannot reach the sidecar directly in production.

**Rate limiting.** Two layers:
- Flask-Limiter: 10 requests/minute per IP on `POST /ops/qa/chat`. Applied before the proxy call; protects Flask and the sidecar from burst traffic.
- Sidecar in-memory limits: 50 messages per session, 200 messages per day. Applied inside `handle_chat` before the Anthropic API call. Limits Anthropic API spend. Counters reset on container restart — they provide cost guardrails, not hard security controls.

**API key handling.** `ANTHROPIC_API_KEY` is read from environment inside `handle_chat` at runtime, not at import time. This means a missing or rotated key produces a clean error response rather than a startup failure. The key is never logged or returned in any response body.

**No CSRF protection.** `POST /ops/qa/chat` has `WTF_CSRF_ENABLED` set to True in production config (platform standard), but the endpoint uses JSON bodies not form submissions. Flask-WTF CSRF protection applies to form POSTs; JSON endpoints in this codebase rely on the `10/minute` rate limit and session-level auth rather than CSRF tokens. If this endpoint is expanded to accept form data, CSRF protection must be added explicitly.

---

## 8. Error Handling

The QA Agent has three error layers. Each layer catches failures and converts them to the standard `{text, tool_calls, model}` response shape rather than propagating exceptions to the browser.

**Layer 1 — Flask proxy (`agent.py`)**

| Condition | Response |
|---|---|
| Sidecar `ConnectionError` | `"QA agent sidecar is not running. Check Docker services."` |
| Sidecar `Timeout` (>120 s) | `"QA agent timed out. Try a simpler question."` |
| Any other exception | Logged at ERROR with traceback. `"QA agent error: <str(e)>"` |

HTTP status returned to browser is always 200 for proxy errors. Flask returns 400 if `messages` is empty before the proxy call is attempted, and 500 if the Flask route handler itself throws (logged at ERROR).

**Layer 2 — Sidecar rate limiter (`server.py`)**

| Condition | Response |
|---|---|
| Session limit (50) reached | `"Session limit reached (50 messages). Reload the page to start a new session."` |
| Daily limit (200) reached | `"Daily limit reached (200 messages). Try again tomorrow."` |
| `ANTHROPIC_API_KEY` missing | `"ANTHROPIC_API_KEY not configured."` |
| `anthropic` package import fails | `"Anthropic SDK not available: <ImportError>"` |
| Anthropic API call exception | `"Claude API error: <str(e)>"`. Logged at ERROR. |
| Tool dispatch loop hits 10 iterations | `"Agent reached maximum tool depth. Try a simpler question."` |
| Invalid JSON body | HTTP 400 with `{"text": "Invalid JSON.", "tool_calls": [], "model": null}` |

**Layer 3 — Tool dispatch (`tools.py`)**

| Condition | Response |
|---|---|
| MCP registry tool raises | `{"error": "Tool <name> failed: <str(e)>"}`. Logged at ERROR. |
| QA-only handler raises | `{"error": "Tool <name> failed: <str(e)>"}`. Logged at ERROR. |
| Tool name not found in either registry | `{"error": "Unknown tool: <name>"}` |
| Registry module fails to import at load time | Warning logged. That registry's tools are absent from the catalog. |

Tool errors are returned as JSON objects to the Anthropic API as `tool_result` content. Claude receives the error description and can decide to try an alternative tool or explain the failure to the user.

Result truncation: any tool result string exceeding 8000 characters is truncated with `"... (truncated)"` appended before being sent back to the Anthropic API. This prevents single large tool results from consuming the context window and inflating API cost.

---

## 9. Testing

Tests live in `Canary/tests/unit/test_qa_agent_tools.py`. Linear: GRO-326.

**Test classes:**

| Class | What it covers |
|---|---|
| `TestDynamicToolLoading` | Registry loads 10+ tools; Atlas and Alert tools present by name; every tool definition has `name`, `description`, and a schema key. |
| `TestMCPDispatch` | `execute_tool` dispatches to Atlas tools; unknown tool name returns `{error: "Unknown tool: ..."}`. |
| `TestQAOnlyTools` | `list_scenarios` returns a non-empty list with `name` key on each entry. |
| `TestAgentProxy` | `chat()` returns `{text, tool_calls, model}` even when sidecar is unreachable; connection error produces human-readable message; `SYSTEM_PROMPT` exists and mentions "tool"; proxy call reaches sidecar URL with `messages` payload. |
| `TestSidecarServer` | `handle_chat` is callable; empty messages returns "No message" text; missing API key returns "ANTHROPIC_API_KEY" text; rate limit constants are 50/200; `build_canary_mcp_server` returns a non-None object. |

**Test strategy:**

- Unit tests only — no integration tests that call the Anthropic API. Sidecar connectivity is mocked with `unittest.mock.patch`.
- `TestAgentProxy.test_chat_returns_dict_with_required_keys` and `test_chat_handles_sidecar_down` use an invalid port (`http://localhost:99999`) to force a real `ConnectionError` without mocking the network layer.
- `TestSidecarServer.test_handle_chat_empty_messages` and `test_handle_chat_no_api_key` call `asyncio.run(handle_chat(...))` directly — no HTTP client needed.
- MCP dispatch tests (`TestMCPDispatch.test_atlas_figure_dispatches_to_mcp`) call the live Atlas registry. They pass as long as the Atlas service and its database are available; they are not marked as integration tests. If Atlas tools are unavailable in CI, the `"error" not in result` assertion may need a marker.

**Running tests:**

```bash
cd ~/GrowDirect/Canary
python3 -m pytest tests/unit/test_qa_agent_tools.py -v
```

---

## 10. Dependencies

### Upstream

| Dependency | What it provides |
|---|---|
| Anthropic Python SDK (`anthropic`) | `client.messages.create()` — the core LLM API call in `server.py`. Lazy-imported at request time. |
| `requests` | HTTP client in `agent.py` for Flask → sidecar proxy call. |
| `uvicorn` | ASGI server that runs `server.py` in the sidecar container. |
| `ANTHROPIC_API_KEY` | Must be present in sidecar environment. Sourced from `.env` via `env_file`. |

### Downstream

| Consumer | How it uses the QA Agent |
|---|---|
| `canary/blueprints/ops_console.py` | `qa_agent_page()` renders the UI; `qa_agent_chat()` proxies POST requests to `agent.chat()`. |
| Browser (ops/qa.html) | Sends messages, renders `text` and `tool_calls` from responses. |

### Shared Infrastructure

| Infrastructure | Role |
|---|---|
| `growdirect_postgres` (canary DB) | QA-only tools `poll_scenario` and `get_thresholds` query this database directly via `get_session()`. |
| Canary MCP registries (Atlas, Alerts, Analytics, Chirp, Fox, Identity, Owl, TSP) | Loaded in-process by the sidecar. The sidecar image must include the full Canary Python package. |
| `canary.services.scenario_fire` | `fire_scenario` function and `SCENARIO_REGISTRY` used by QA-only tool handlers. |
| `canary.services.health_check.chirp_lab` | `live_fire_poll` used by `poll_scenario` handler. |
| Docker network `growdirect` | Both Flask and the sidecar must be on this network for `http://qa-agent:8002` routing to work. |
| Flask-Limiter (`canary.extensions.limiter`) | Provides the `10/minute` rate limit on the Flask-side route. |

---

## 11. Known Issues & Reconciliation

**Placement in Canary tree vs. ALX namespace.**

The QA Agent lives at `Canary/canary/services/qa_agent/` but its namespace in the SDD registry is `alx`. This is correct and intentional. The QA Agent is an ALX-scoped capability (platform-level test tooling) that happens to be implemented inside the Canary app tree because it runs as a Canary sidecar, requires the Canary MCP registries in-process, and is accessed through the Canary Ops Console. There is no separate ALX app container. When a standalone ALX container exists, the QA Agent could be extracted; until then, co-location in the Canary tree is the right call.

**Sidecar blocking I/O in async handler.**

`handle_chat` is an `async` coroutine but calls `client.messages.create()` synchronously (the Anthropic SDK does not expose an async client in the version used here). The sidecar runs a single uvicorn worker, so one in-flight request blocks the event loop. Concurrent requests will queue behind it. For a low-traffic internal tool this is acceptable; if concurrent use becomes common, migrate to `anthropic.AsyncAnthropic` or run multiple uvicorn workers.

**In-memory rate limits reset on restart.**

`_session_counts` and `_daily_count` are process-local. A container restart resets all counters. This means the daily limit is a soft guardrail, not a hard one. If cost control is a priority, move these counters to Valkey with a TTL-keyed structure.

**Session ID not propagated from Flask.**

`agent.py` does not extract a session identifier from the Flask session and forward it to the sidecar. All requests arrive at the sidecar with no `session_id`, so they all share the `"default"` bucket. The 50-message-per-session limit currently applies to all users collectively, not per user. To fix: extract `session['user_id']` or a browser-generated session token in `qa_agent_chat()` and include it in the JSON body forwarded to the sidecar.

**`build_canary_mcp_server` not in live path.**

`tools.py` implements `build_canary_mcp_server()` for the Claude Agent SDK integration path but the live sidecar uses `handle_chat` with direct `execute_tool` dispatch. The SDK builder is tested (unit test asserts non-None return) but not exercised end-to-end. It is forward infrastructure for when the Agent SDK supports headless containers.
