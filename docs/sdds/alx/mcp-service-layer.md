# MCP Service Layer

> **Status:** Complete — written from code
> **Namespace:** alx
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/mcp/`, `Canary/canary/blueprints/*_mcp.py`, `Canary/canary/services/*/tools.py`

---

## 1. Overview

The MCP Service Layer is the agent-facing API surface for the Canary platform. It exposes Canary's
internal domain services as structured tool calls over HTTP, following the Model Context Protocol
(MCP) convention. IDE agents (Cursor, Claude Code, Claude Desktop) and internal automation consume
these endpoints over a stdio bridge; the Canary Flask app and standalone containers expose them
over HTTP.

The layer was consolidated under GRO-174 (shared base kit) and expanded through GRO-183, GRO-185,
and GRO-186. Before GRO-174, each MCP server duplicated its own tool class, registry dict, and
blueprint boilerplate. The refactor extracted three shared primitives (`MCPTool`, `MCPRegistry`,
`create_mcp_blueprint`) and a stdio adapter (`streamable_server.py`) that drives all 12 servers
without modification.

**12 active MCP servers:**

| Server | URL Prefix | Domain |
|--------|-----------|--------|
| canary-owl | `/owl` | Retail intelligence, search, heartbeat, LLM |
| canary-chirp | `/chirp` | Detection rule catalog and evaluation |
| canary-alert | `/alert` | Alert lifecycle and impact scoring |
| canary-fox | `/fox` | Case management and evidence chain |
| canary-analytics | `/analytics` | Dashboard, heatmap scoring, velocity |
| canary-identity | `/identity` | Merchants, employees, locations |
| canary-tsp | `/tsp` | Webhook pipeline, stream health, Merkle |
| canary-raas | `/raas` | Namespace resolution and source management |
| canary-bff | `/bff` | Frontend aggregation (home, chirp feed, flags) |
| canary-condor | `/condor` | External intelligence (benchmarks, SDK, regulatory) |
| canary-atlas | `/atlas` | Diagram management and drift detection |
| canary-alx | `/alx` | Platform memory bus (extracted to memory-bus MCP, GRO-172) |

The `alx` server is registered in the streamable server prefix map but its Flask blueprint was
extracted to the standalone memory-bus MCP service (GRO-172) and is not present in
`Canary/canary/blueprints/`. It is omitted from `standalone.py`'s `SERVER_BLUEPRINTS`.

---

## 2. Architecture

### Component Diagram

```
IDE Agent (Cursor / Claude Code / Claude Desktop)
    |
    | MCP stdio (stdin/stdout)
    v
streamable_server.py          -- stdio adapter, one process per server
    |
    | HTTP POST /owl/tools/<name>
    | Authorization: Bearer <token>  OR  X-API-Key: <key>
    v
Canary Flask App (port 5001)  -- or standalone container (port 8001)
    |
    |-- owl_api.py              -- /owl/* (uses create_mcp_blueprint + extra routes)
    |-- chirp_mcp.py            -- /chirp/*
    |-- alert_mcp.py            -- /alert/*
    |-- fox_mcp.py              -- /fox/*
    |-- analytics_mcp.py        -- /analytics/*
    |-- identity_mcp.py         -- /identity/*
    |-- tsp_mcp.py              -- /tsp/*
    |-- raas_mcp.py             -- /raas/*
    |-- bff_mcp.py              -- /bff/*
    |-- condor_mcp.py           -- /condor/*
    |-- atlas_mcp.py            -- /atlas/*
         |
         v
    create_mcp_blueprint(prefix, registry, health_fn)
         |
         |-- MCPRegistry._tools: Dict[str, MCPTool]
         |-- MCPTool.invoke(params, context) -> response envelope
              |
              +-- domain service (canary/services/*/...)
              +-- PostgreSQL (canary db, schemas: app, sales, metrics)
              +-- Valkey (DB 0, canary:events stream)
              +-- Ollama (qwen3-embedding:8b, growdirect_ollama:11434)
```

### Request / Data Flow

1. **Discovery.** The stdio adapter calls `GET /<prefix>/manifest` on startup. The Flask app
   returns the registry's manifest: server name, version, description, and the full tool list
   with input schemas. The adapter registers FastMCP tool stubs for each discovered tool.

2. **Invocation.** The IDE agent calls a registered tool. FastMCP serializes the call to
   `stdin`. The adapter's handler posts to `POST /<prefix>/tools/<tool_name>` with body
   `{"params": {...}}`.

3. **Auth.** The `jwt_required` decorator intercepts every tool invocation route (not health
   or manifest). It checks for `X-API-Key` first, then `Authorization: Bearer`. If the API
   key matches `CANARY_MCP_API_KEY`, context is set as `user_id=alx-agent, roles=[admin]`.
   In dev mode, `Bearer <token>` is validated against `CANARY_DEV_JWT_SECRET`.

4. **Context injection.** After auth, `g.merchant_id` and `g.user_id` are available on Flask's
   `g`. The blueprint's `tool_invoke` view extracts `params` and `context` from the request
   body, then injects `merchant_id` and `user_id` from `g` if the caller did not supply them.

5. **Kwargs unpacking.** FastMCP serializes `**kwargs` handlers as a single `kwargs` string
   parameter containing JSON. The blueprint detects `{"kwargs": "<json string>"}` and unpacks
   it to a proper `params` dict before invoking the tool. This guard exists in both the
   blueprint (`blueprint.py` lines 99-108) and the adapter (`streamable_server.py` lines
   133-142).

6. **Tool execution.** `MCPTool.invoke(params, context)` calls the handler. Handlers signal
   logical failure by returning a dict containing an `"error"` key — the envelope then sets
   `ok=False` and the blueprint returns HTTP 500.

7. **Response envelope.** Every tool call returns:
   ```json
   {
     "tool": "<name>",
     "ok": true,
     "result": { ... },
     "timestamp": "2026-03-30T12:00:00+00:00"
   }
   ```
   On failure: `"ok": false` and `"error": "<message>"` replaces `"result"`.

### Key Design Decisions

**One registry per server, not one global registry.** Each server creates its own `MCPRegistry`
instance. This allows servers to be extracted into standalone containers with no risk of tool
name collisions across domains.

**Blueprint factory instead of copy-paste.** Before GRO-174, `owl_api.py` and `alx_api.py`
each had ~136 lines of duplicate route definitions. `create_mcp_blueprint` stamps the four
standard routes (`manifest`, `tools`, `tools/<name>`, `health`) in 15 lines per server.

**Strangler fig migration.** REST blueprints (`*_wired.py`) remain untouched. MCP blueprints
live alongside them at a different URL prefix. Agents use MCP; browser users use REST. No
forced migration.

**Stateless handlers preferred.** Handlers that require no database are marked in their module
docstrings (e.g., Chirp has "9 pure, 1 DB-read"; Alert has "4 pure, 2 DB-read"). Pure handlers
allow server extraction without database dependency.

**Rate limiting at higher thresholds.** MCP endpoints are agent-to-agent. The factory applies
`100/hour` on manifest and tools list, `1000/hour` on tool invocations. These are higher than
browser-facing routes. The limiter is imported lazily and skipped gracefully in unit tests.

**Health routes are auth-exempt.** `GET /<prefix>/health` has no `@jwt_required` decorator.
This allows Docker health checks and load balancer probes to function without credentials.

---

## 3. Data Model

**N/A — the MCP layer has no database tables of its own.**

The registry (`MCPRegistry`) is an in-memory `dict[str, MCPTool]` instantiated at module import
time and held for the lifetime of the Flask worker process. There is no persistence layer for
tool registrations.

Tool handlers access the data model of their parent domain:

- Handlers in `canary/services/alerts/tools.py` query `app.alerts`, `app.alert_history`
- Handlers in `canary/services/fox/tools.py` query `app.fox_cases`, `app.fox_case_timeline`, `app.fox_case_alerts`
- Handlers in `canary/services/analytics/tools.py` query the `metrics` schema
- Handlers in `canary/services/tsp/tools.py` query `ingestion_log`, `evidence_records`, `event_inscriptions`, `inscription_pool`
- Handlers in `canary/services/identity/tools.py` query `app.merchants`, `app.employees`, `app.locations`

Those models are documented in their respective domain SDDs (fox, alert, tsp, identity, analytics).

---

## 4. Interfaces

All endpoints require `Content-Type: application/json` on POST. Auth header is required on all
routes except health.

### Standard routes (stamped by `create_mcp_blueprint` for every server)

#### `GET /<prefix>/manifest`
Returns the MCP server manifest.

**Auth:** Required (`jwt_required`)
**Rate limit:** 100/hour
**Response:**
```json
{
  "name": "canary-owl",
  "version": "0.1.0",
  "description": "Canary LP Owl — retail intelligence engine",
  "tools": [
    {
      "name": "the_one_thing",
      "description": "...",
      "inputSchema": { "type": "object", "properties": { ... } }
    }
  ]
}
```

#### `GET /<prefix>/tools`
Returns the tool list only (subset of manifest).

**Auth:** Required
**Rate limit:** 100/hour
**Response:** `{ "tools": [ ... ] }`

#### `POST /<prefix>/tools/<tool_name>`
Invoke a tool.

**Auth:** Required
**Rate limit:** 1000/hour
**Request body:**
```json
{
  "params": { "merchant_id": "...", ... },
  "context": { "merchant_id": "...", "user_id": "..." }
}
```
**Success response (HTTP 200):**
```json
{ "tool": "list_alerts", "ok": true, "result": { ... }, "timestamp": "..." }
```
**Failure response (HTTP 500):**
```json
{ "tool": "list_alerts", "ok": false, "error": "merchant_id is required", "timestamp": "..." }
```
**Tool not found (HTTP 404):**
```json
{ "ok": false, "error": "Unknown tool: foo", "available": ["list_alerts", "get_alert", ...] }
```

#### `GET /<prefix>/health`
Service health check.

**Auth:** None
**Response (HTTP 200 or 503):**
```json
{ "service": "canary-tsp", "healthy": true, "valkey_connected": true, "tools": 7 }
```

### Server-specific tools and dependencies

#### canary-owl (`/owl`) — 10 tools, depends on: `app` DB, Ollama

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `the_one_thing` | insights | Ollama (optional), `metrics` DB | Top priority insight from alerts + dashboard |
| `ask` | query | Ollama (required), `growdirect_memory` DB | Freeform plain-English question |
| `heartbeat` | health | None (pure) | Store health score from alert counts |
| `check_heartbeat` | health | `app` DB, Ollama (optional) | Full health check with memory context + report |
| `score_payment` | scoring | None (pure) | Stateless Chirp rules on a payment dict |
| `search` | search | `app` DB, Ollama | NL query → parameterized PostgreSQL → results |
| `dashboard` | dashboard | `metrics` DB | KPI bands, health score, top risks |
| `knowledge_search` | knowledge | `growdirect_memory` DB (pgvector) | Semantic search over institutional memory |

Note: `owl_api.py` extends the factory blueprint with two additional routes: `GET /owl/one-thing`
(convenience shortcut) and `POST /owl/chat` (personality-routed conversational interface, GRO-133).
These are not stamped by the factory.

#### canary-chirp (`/chirp`) — 10 tools, depends on: `app` DB (1 tool only)

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `get_rules` | rules | None (pure) | List Chirp rule catalog, filter by category or tier |
| `get_rule` | rules | None (pure) | Single rule lookup by ID (e.g. C-001) |
| `evaluate_stateless` | evaluation | None (pure) | Run Tier 1 rules on a parsed payload |
| `apply_sensitivity` | configuration | None (pure) | Compute thresholds at a sensitivity level |
| `get_templates` | configuration | None (pure) | List config templates |
| `apply_template` | configuration | None (pure) | Apply template, return full rule config |
| `validate_thresholds` | configuration | None (pure) | Validate proposed thresholds against rule |
| `get_config_summary` | configuration | None (pure) | Summarize merchant config vs catalog defaults |
| `estimate_sensitivity` | configuration | None (pure) | Classify thresholds as strict/default/relaxed/minimal |
| `get_merchant_thresholds` | configuration | `app` DB, Valkey | Get merchant thresholds (cache → DB → defaults) |

#### canary-alert (`/alert`) — 6 tools, depends on: `app` DB (2 tools)

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `lifecycle_summary` | lifecycle | None (pure) | Count active/stale/archived/resolved/dismissed/case_opened |
| `calculate_impact` | impact | None (pure) | Dollar impact estimate from rule, amount, severity |
| `rank_alerts` | impact | None (pure) | Rank alerts by severity + impact composite score |
| `get_impact_summary` | impact | None (pure) | Aggregate dollar impact across alert list |
| `list_alerts` | alerts | `app` DB | Paginated alert list with severity/rule filters |
| `get_alert` | alerts | `app` DB | Single alert with full status history |

#### canary-fox (`/fox`) — 8 tools, depends on: `app` DB

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `create_case` | cases | `app` DB | Open investigation case with timeline entry |
| `get_case` | cases | `app` DB | Case details by UUID |
| `list_cases` | cases | `app` DB | Paginated case list with status/date filters |
| `update_case_status` | cases | `app` DB | State machine transition with timeline write |
| `add_subject` | cases | `app` DB | Link employee/vendor/party to case |
| `get_timeline` | cases | `app` DB | Append-only audit trail (hash-chained) |
| `verify_chain` | evidence | `app` DB | Validate evidence hash chain integrity |
| `link_alert` | cases | `app` DB | Idempotent alert-to-case junction |

#### canary-analytics (`/analytics`) — 7 tools, depends on: `metrics` DB (5 tools)

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `get_dashboard` | dashboard | `metrics` DB | Period summary: health score, KPI bands, anomaly count |
| `get_trends` | dashboard | `metrics` DB | Sparkline data for a single metric across periods |
| `get_top_risks` | dashboard | `metrics` DB | Top 5 employees and locations by risk score |
| `get_drilldown` | dashboard | `metrics` DB | Per-entity metric detail with band scoring |
| `score_metrics` | scoring | None (pure) | Score actuals vs baselines through heatmap engine |
| `detect_velocity` | scoring | None (pure) | Z-score anomaly detection on time series |
| `get_period_metrics` | metrics | `metrics` DB | Raw KPI actuals for a fiscal period |

#### canary-identity (`/identity`) — 6 tools, depends on: `app` DB

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `get_merchant` | merchant | `app` DB | Merchant profile (name, email, phone) |
| `get_settings` | merchant | `app` DB | Merchant settings (timezone, currency, notification prefs) |
| `list_employees` | employee | `app` DB | All employees, optional location/active filters |
| `get_employee` | employee | `app` DB | Single employee with risk score |
| `list_locations` | location | `app` DB | All locations for a merchant |
| `get_location` | location | `app` DB | Single location |

#### canary-tsp (`/tsp`) — 7 tools, depends on: Valkey + `app`/`sales` DB

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `get_stream_health` | health | Valkey | Stream length, consumer groups, pending entries, DL count |
| `get_dead_letters` | health | Valkey | List dead-letter stream entries |
| `replay_event` | management | Valkey | Re-publish dead letter to main stream |
| `get_ingestion_stats` | analytics | `app` DB | Throughput, error rates, latency from `ingestion_log` |
| `get_receipt` | evidence | `app` DB | Evidence receipt with chain hash and inscription proof |
| `verify_merkle` | evidence | `app` DB (or pure) | Merkle proof verification — inline or DB lookup |
| `process_dead_letters` | management | Valkey | Batch DLQ processing with exponential backoff |

The TSP health check in `tsp_mcp.py` pings Valkey directly — it is the only server whose
`health_fn` can return `healthy: false` based on infrastructure state.

#### canary-raas (`/raas`) — 7 tools, depends on: `app` DB

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `resolve_namespace` | namespace | `app` DB | merchant_id → `raas:{merchant_id}` |
| `ensure_namespace` | namespace | `app` DB | Resolve or create namespace |
| `register_source` | sources | `app` DB | Register POS system connection (idempotent) |
| `get_sources` | sources | `app` DB | List active source connections |
| `disconnect_source` | sources | `app` DB | Soft-delete source connection |
| `build_key` | keys | None (pure) | Build namespaced Valkey key |
| `link_jeffe` | identity | `app` DB | Bridge namespace to .jeffe identity |

#### canary-bff (`/bff`) — 4 tools, depends on: `app` DB + Ollama

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `get_home_data` | aggregation | `app` DB, Ollama | Full home screen: alerts, stats, cases, dashboard, The One Thing |
| `get_chirp_feed` | aggregation | `app` DB | Alert feed with severity cap (critical/high always shown) |
| `refresh` | aggregation | `app` DB, Ollama | Lightweight pull-to-refresh: severity counts + The One Thing |
| `get_feature_flags` | config | `app` DB | Feature flag state (merchant override → global DB → ENV) |

#### canary-condor (`/condor`) — 7 tools, depends on: none (all pure/static)

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `get_benchmarks` | merchant_intelligence | None (static) | NRF shrinkage benchmarks by segment/region |
| `compare_to_industry` | merchant_intelligence | None (pure) | Merchant shrinkage rate vs industry benchmark |
| `get_sdk_currency` | platform_intelligence | None (static) | Current SDK versions (Square, MCP, Ollama, frameworks) |
| `get_tooling_landscape` | platform_intelligence | None (static) | Agent framework comparison matrix |
| `get_mcp_patterns` | platform_intelligence | None (static) | MCP design patterns as applied in Canary |
| `get_regulatory` | merchant_intelligence | None (static) | LP-relevant regulatory landscape (ORC, PCI, privacy) |
| `evaluate_framework` | platform_intelligence | None (static) | Assessment of a specific agent framework |

#### canary-atlas (`/atlas`) — 6 tools, depends on: filesystem (Canary atlas directory)

| Tool | Category | Dependencies | Description |
|------|----------|-------------|-------------|
| `atlas_figure` | atlas | Filesystem | Load full figure by ID (frontmatter, Mermaid, notes) |
| `atlas_search` | atlas | Filesystem | Keyword search across figures |
| `atlas_validate` | atlas | Filesystem | Validate figure(s) for syntax and completeness |
| `atlas_index` | atlas | Filesystem | Index in summary, full, or embedding format |
| `atlas_render` | atlas | Filesystem, `mmdc` | Render figure to SVG or PNG via mmdc |
| `atlas_drift` | atlas | Filesystem, `app` codebase | Detect stale or undiagrammed service references |

---

## 5. Service Layer

### MCPTool (`canary/mcp/tool.py`)

The `MCPTool` class is the unit of work in the MCP layer. It carries:

- `name: str` — unique within its server's registry
- `description: str` — surfaced in the manifest for IDE agent discovery
- `input_schema: Dict` — JSON Schema properties passed to `inputSchema.properties` in the manifest
- `handler: Callable[(params: Dict, context: Dict) -> Dict]`
- `category: str` — grouping label (not surfaced externally)

`to_mcp()` serializes to the MCP tool definition format. `invoke()` calls the handler inside
a try/except and wraps the result in the standard envelope. Handlers that return a dict
containing an `"error"` key are detected as logical failures (`ok=False`).

### MCPRegistry (`canary/mcp/registry.py`)

Server-scoped in-memory tool store. Each server module creates one instance at the top of
`canary/services/<domain>/tools.py` and registers tools at import time.

Methods:
- `register(tool: MCPTool)` — adds to `_tools` dict
- `get(name: str) -> Optional[MCPTool]` — lookup by name
- `list_tools() -> List[Dict]` — returns MCP format list
- `get_manifest() -> Dict` — returns full manifest dict
- `tool_names() -> List[str]` — for error messages (unknown tool response)
- `__len__` / `__contains__` — used by health checks and blueprint

### Blueprint factory (`canary/mcp/blueprint.py`)

`create_mcp_blueprint(prefix, registry, health_fn=None, bp_name=None)` is the only factory.
It creates a Flask `Blueprint` and registers the four standard routes. Route implementations
live inside the factory closure. This pattern avoids route re-registration if the module is
imported multiple times.

The factory attempts to import `canary.extensions.limiter` for rate limiting. If the import
fails (e.g., unit tests run outside the Docker stack), the `_limit` decorator is a no-op.
This graceful degradation keeps all unit tests runnable without Flask extensions.

### Standalone app factory (`canary/mcp/standalone.py`)

`create_app(server_name)` builds a minimal Flask app that serves exactly one MCP server.
Used by `Dockerfile.mcp` for standalone container extraction:

```bash
gunicorn "canary.mcp.standalone:create_app('owl')" --bind 0.0.0.0:8001
```

The factory initializes only the infrastructure the target server actually needs, based on
`SERVER_DEPS`:

| Server | DBs | Valkey | Ollama |
|--------|-----|--------|--------|
| owl | app | No | Yes |
| chirp | app | No | No |
| alert | (none) | No | No |
| fox | app | No | No |
| analytics | metrics | No | No |
| identity | app | No | No |
| tsp | app, sales | Yes | No |
| raas | app | No | No |
| bff | app | No | Yes |
| condor | (none) | No | No |

Note: `alert` and `condor` are listed with empty `dbs` — they are stateless or static. The
factory sets `db_ok = True` without attempting a database connection.

A `before_request` hook on the standalone app resolves `SQUARE_MERCHANT_ID` to an internal
UUID via `_resolve_merchant_uuid` and places it on `g.merchant_id`. This mirrors what the
full monolith's session middleware does.

### Stdio adapter (`canary/mcp/streamable_server.py`)

Bridges IDE agents to Canary HTTP endpoints. Started as a subprocess by the IDE's MCP config:

```bash
python3 canary/mcp/streamable_server.py --server owl --api-key-env CANARY_MCP_API_KEY
```

On startup, `build_server()`:
1. Fetches the manifest from `GET /<prefix>/manifest`
2. Creates a `FastMCP` server instance
3. Generates a closure handler for each tool in the manifest
4. Registers each handler with `mcp_server.tool()`
5. Runs `mcp_server.run(transport="stdio")`

Auth priority:
1. `--api-key-env VAR` — reads the API key from the named env var, sends `X-API-Key` header
2. `--auth-token TOKEN` — sends `Authorization: Bearer TOKEN`
3. Neither specified — sends `Authorization: Bearer dev-local-token` (local dev fallback)

The manifest fetch itself is unauthenticated in the current implementation. This is a known
gap — see section 11.

### Tool registration pattern

Each domain service registers tools by placing a `tools.py` module in its service directory:

```
canary/services/<domain>/tools.py
```

The module:
1. Creates a `MCPRegistry` instance
2. Exports convenience aliases (`get_tool`, `list_tools`, `get_manifest`)
3. Defines handler functions
4. Calls `registry.register(MCPTool(...))` for each tool

The corresponding blueprint in `canary/blueprints/<domain>_mcp.py` simply imports the registry
and calls `create_mcp_blueprint`:

```python
from canary.mcp.blueprint import create_mcp_blueprint
from canary.services.<domain>.tools import registry

<domain>_mcp_bp = create_mcp_blueprint("<prefix>", registry, health_fn=..., bp_name="...")
```

This three-file pattern (tools.py + *_mcp.py + blueprint registration in app factory) is
identical across all 11 active servers (owl_api.py is the only exception with extra routes).

---

## 6. Configuration

### Environment variables

| Variable | Used by | Purpose |
|----------|---------|---------|
| `CANARY_MCP_API_KEY` | `jwt_auth.py`, `streamable_server.py` | API key for agent-to-agent calls (X-API-Key header) |
| `CANARY_DEV_JWT_SECRET` | `jwt_auth.py` | Dev/test Bearer token value |
| `CANARY_ENV` | `jwt_auth.py` | `production` rejects all Bearer tokens; other values use dev mode |
| `CANARY_DEFAULT_ORG` | `jwt_auth.py` | Default `g.organization_id` for API-key auth |
| `CANARY_DEFAULT_MERCHANTS` | `jwt_auth.py` | Comma-separated Square merchant IDs for dev Bearer auth |
| `SQUARE_MERCHANT_ID` | `standalone.py`, `jwt_auth.py` | Merchant ID for standalone server context |
| `VALKEY_STREAM` | `tsp/tools.py` | Main stream name (default: `canary:events`) |
| `VALKEY_DEAD_LETTER_STREAM` | `tsp/tools.py` | Dead letter stream (default: `canary:dead_letter`) |
| `DETECTION_STREAM` | `tsp/tools.py` | Detection stream (default: `canary:detection`) |
| `FLASK_DEBUG` | `standalone.py` | Enable debug logging in standalone mode |

### IDE MCP configuration (`.mcp.json` / Claude Desktop `config.json`)

```json
{
  "mcpServers": {
    "canary-owl": {
      "command": "python3",
      "args": [
        "Canary/canary/mcp/streamable_server.py",
        "--server", "owl",
        "--base-url", "http://localhost:5001",
        "--api-key-env", "CANARY_MCP_API_KEY"
      ]
    }
  }
}
```

One entry per server. The `--server` argument selects from the `SERVER_PREFIXES` map in
`streamable_server.py`. Base URL defaults to `http://localhost:5001` (the Canary Flask dev
server).

### Rate limits (applied by Flask-Limiter)

| Route | Limit |
|-------|-------|
| `GET /<prefix>/manifest` | 100/hour |
| `GET /<prefix>/tools` | 100/hour |
| `POST /<prefix>/tools/<name>` | 1000/hour |
| `GET /<prefix>/health` | Unlimited (auth-exempt) |

---

## 7. Security and Compliance

### Authentication

The `jwt_required` decorator in `canary/middleware/jwt_auth.py` is applied to `manifest`,
`tools`, and `tools/<name>` routes. The health route has no auth requirement.

**API key path (production-ready):**
- `X-API-Key` header value must match `CANARY_MCP_API_KEY` env var exactly
- Sets `g.user_id = 'alx-agent'`, `g.roles = ['admin']`
- Resolves `SQUARE_MERCHANT_ID` → internal UUID via `_resolve_merchant_uuid()`
- This path is active in all environments

**Bearer token path (dev/test only):**
- Checked only when no API key is present
- Token must match `CANARY_DEV_JWT_SECRET` exactly (string comparison, no JWT library)
- If `CANARY_ENV == 'production'`, all Bearer token requests are rejected with 401
- Sets `g.user_id = 'dev-user'`, `g.roles = ['admin']`
- Resolves `CANARY_DEFAULT_MERCHANTS` → internal UUIDs

**Production gap:** The current auth implementation does not use JWT library signature
verification. The "JWT" in the name is historical — the dev path does a literal string
comparison against an env var secret. A proper JWT validation path for production is not
yet implemented. The production guard (`CANARY_ENV == 'production'` → 401) prevents
Bearer auth from working in production, making API key auth the only viable production path.

### Merchant context isolation

`_resolve_merchant_uuid()` resolves Square's external `source_merchant_id` to the internal
UUID at every auth boundary. After resolution, all tool handlers see only internal UUIDs on
`g.merchant_id` and `context["merchant_id"]`. Square IDs do not cross the auth boundary into
business logic.

A worker-process-level cache (`_merchant_uuid_cache`) prevents repeated database lookups for
the same Square merchant ID within a Gunicorn worker's lifetime.

### Role authorization

`jwt_required` populates `g.roles`. The `role_required` and `roles_required` decorators in
`jwt_auth.py` can guard specific routes for role-based access. Current MCP routes use only
authentication (not additional role checks) — all authenticated callers receive full tool
access.

### Rate limiting

Flask-Limiter applies rate limits per the configuration in section 6. MCP tool invocations
are set higher (1000/hour) than typical browser-facing REST routes because agents call tools
repeatedly within a session.

---

## 8. Error Handling

### Tool-level errors

Handlers signal errors in two ways:

1. **Return `{"error": "<message>"}` dict** — the `MCPTool.invoke()` wrapper detects the
   `"error"` key, sets `ok=False`, and returns HTTP 500. The tool name and timestamp are
   still included in the envelope.

2. **Raise an exception** — caught by the `try/except` in `MCPTool.invoke()`, logged at
   `ERROR` level, returned as `{"tool": ..., "ok": false, "error": str(e), "timestamp": ...}`.

### Blueprint-level errors

- **Unknown tool name:** HTTP 404 with `{"ok": false, "error": "Unknown tool: <name>", "available": [...]}`
- **Invalid JSON body:** `request.get_json(silent=True)` returns `None`; falls back to empty
  dict, so tools must validate required params themselves
- **Auth failure:** HTTP 401 via `abort(401)` from `jwt_required`
- **Rate limit exceeded:** HTTP 429 from Flask-Limiter

### Infrastructure errors

- **Valkey unavailable:** TSP tools that call `_get_valkey_client()` catch exceptions and
  return `{"ok": false, "error": "Valkey connection failed: ..."}`. The TSP health endpoint
  returns `healthy: false` and HTTP 503.
- **Database unavailable:** Individual handlers catch exceptions from `get_session()` and
  return structured error dicts. The standalone app factory logs a warning on DB init failure
  but does not crash — `db_ok` is set to `False` and the health endpoint reflects the state.
- **Ollama unavailable:** The Owl's `ask` tool calls `owl_healthy()` before attempting LLM
  calls and returns `{"answer": "I'm offline right now.", "ok": false}`. The `check_heartbeat`
  tool degrades gracefully to deterministic scoring if Ollama is down.

### Stdio adapter errors

If the manifest fetch fails on startup (Flask not running), `requests.get` raises and the
process exits. The IDE surfaces this as "server failed to start." No retry logic is in place
— the operator must ensure the Flask app is running before launching the stdio adapter.

---

## 9. Testing

### Unit test approach

`MCPTool` and `MCPRegistry` have no Flask dependencies and can be tested in isolation. The
blueprint factory's `_has_limiter = False` fallback allows blueprint instantiation in tests
that do not have the Flask extensions available.

Handler functions are imported directly and called with `(params, context)` dicts:

```python
from canary.services.chirp.tools import _handle_get_rules

result = _handle_get_rules({"category": "payment"}, {})
assert result["ok"] is True
assert result["result"]["count"] > 0
```

Pure handlers (those with no DB or Valkey dependency) can be tested without a running database.

### Integration test approach

Integration tests for MCP endpoints follow the same pattern as REST route tests:
- Use the test Flask app factory with `TestConfig` (CSRF disabled, test DB)
- Authenticate by setting the `X-API-Key` header to `CANARY_MCP_API_KEY`
- POST to `/<prefix>/tools/<name>` with a `params` dict
- Assert HTTP 200 and `ok: true` in the envelope

### Smoke test

`GET /<prefix>/health` on each server is the smoke check. No auth required. A healthy response
confirms the server is registered, the blueprint is mounted, and (for TSP) Valkey is reachable.

### Known test gaps

The stdio adapter (`streamable_server.py`) is not unit tested. Testing it requires either a
running Flask server or a mock HTTP layer. The manifest fetch and FastMCP registration path
are currently covered only by manual integration testing.

---

## 10. Dependencies

### Upstream

| Dependency | Used by | Notes |
|------------|---------|-------|
| Flask 3+ | All servers | Blueprint, request, g, jsonify |
| Flask-Limiter | `blueprint.py` | Rate limiting; imported lazily |
| `mcp[fastmcp]` (pip) | `streamable_server.py` | `FastMCP` stdio server |
| `requests` (pip) | `streamable_server.py` | HTTP calls to Flask app |
| `python-dotenv` (pip) | `streamable_server.py` | Loads `.env` for API key resolution |

### Downstream

| Dependency | Used by | Notes |
|------------|---------|-------|
| PostgreSQL `canary` DB | Most tool handlers | Via `canary.db.session_factory.get_session()` |
| PostgreSQL `growdirect_memory` DB | Owl `ask`, `knowledge_search` | Platform memory bus (pgvector) |
| Valkey DB 0 | TSP tools, Chirp threshold cache | Via `canary.services.tsp.stream_publisher.get_stream_client()` |
| Ollama `qwen3-embedding:8b` | Owl `ask`, `knowledge_search`, BFF | `http://growdirect_ollama:11434` |

### Shared infrastructure

The MCP layer runs inside the Canary Flask container (or standalone containers). It shares the
`growdirect` Docker network and accesses `growdirect_postgres`, `growdirect_valkey`, and
`growdirect_ollama` via service hostnames. Standalone containers join the same network:

```yaml
# Canary devops/docker-compose.yml
networks:
  growdirect:
    external: true
```

Standalone MCP containers (e.g., Owl at port 8001) also declare the same external network
and connect directly to the shared Postgres, Valkey, and Ollama instances.

---

## 11. Known Issues and Reconciliation

### Manifest endpoint does not require authentication

`GET /<prefix>/manifest` has `@jwt_required` applied in `blueprint.py`, but the stdio adapter
calls it without credentials on startup (line 66-68 of `streamable_server.py`). This works
today because the adapter runs on localhost where `CANARY_DEV_JWT_SECRET` is set, but would
fail if the manifest endpoint enforced auth before the adapter has resolved its auth strategy.

Reconciliation path: the adapter should send the API key on the manifest fetch, or the
manifest/tools list endpoints should be explicitly public (auth-exempt), consistent with how
most MCP servers treat discovery endpoints.

### Bearer token auth is dev-only; no production JWT path exists

The `jwt_required` decorator notes `"JWT validation not implemented for production — rejecting"`
and returns 401 for all Bearer tokens when `CANARY_ENV == 'production'`. API key auth is the
only production-ready path. If multi-tenant production MCP access is required, a proper JWT
verification path (e.g., via PyJWT against a signing key) must be added.

### `alx` server prefix registered in streamable_server but not in standalone

`SERVER_PREFIXES` in `streamable_server.py` maps `"alx"` to `/alx`, but `SERVER_BLUEPRINTS`
in `standalone.py` does not include it (removed at GRO-172 with the comment "extracted to
platform memory-bus MCP service"). If someone launches the stdio adapter with `--server alx`
against `localhost:5001`, the manifest fetch will succeed only if the main app still mounts
an `/alx` blueprint. This dependency on the monolith for ALX should be resolved: either
remove `alx` from `SERVER_PREFIXES` or document the memory-bus MCP container as a required
dependency for ALX clients.

### `ops` server registered in streamable_server but has no blueprint

`SERVER_PREFIXES` maps `"ops"` to `/ops-mcp` but there is no `ops_mcp.py` in
`canary/blueprints/` and no `ops` entry in `SERVER_BLUEPRINTS` in `standalone.py`. Launching
with `--server ops` will succeed at manifest fetch only if the ops blueprint is registered in
the monolith. No `ops` tools file was found in `canary/services/`. This appears to be a
reserved slot that has not been implemented.

### Cove MCP layer uses a different architecture — platform vs app scope question

The Canary MCP layer (`canary/mcp/`) uses the `MCPTool` / `MCPRegistry` / `create_mcp_blueprint`
factory pattern with HTTP transport and a stdio adapter. The Cove MCP layer (`cove/cove/mcp/`)
is a separate implementation with its own server, tool structure, chunking, embedding, and DB
modules — it does not use the Canary base kit.

This creates a divergence question: should the `MCPTool` / `MCPRegistry` / `create_mcp_blueprint`
primitives be promoted to a platform-level package (e.g., `growdirect/mcp/`) shared by both apps,
or should each app maintain its own MCP implementation? The current state is app-scoped for
Canary (named `canary.mcp`) and fully independent for Cove.

A decision record should be written before any further MCP tooling is added to Cove. The
Canary pattern is the more mature implementation and a reasonable candidate for promotion, but
the two apps have different transport needs (Canary: HTTP + stdio bridge; Cove: may be stdio-
native). This is tracked as an open platform question rather than a defect.

### `ops-mcp` URL prefix does not follow the standard `/<name>` pattern

All other servers use a single-word prefix (`/owl`, `/chirp`, `/alert`, etc.). The ops server
is mapped to `/ops-mcp`. If the ops server is ever implemented, the prefix should be
rationalized to `/ops` for consistency, and `SERVER_PREFIXES` in `streamable_server.py`
updated accordingly.
