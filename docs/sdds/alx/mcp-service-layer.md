# MCP Service Layer (Platform SDK)

> **Status:** Complete — written from code
> **Namespace:** alx
> **Last updated:** 2026-03-30
> **Code location:** `services/growdirect-mcp/`

---

## 1. Overview

The MCP Service Layer is the platform SDK wrapper that provides shared infrastructure for all GrowDirect MCP servers. It wraps the official `mcp` Python SDK with GrowDirect conventions: a tool registry, standard response envelopes, optional auth, and a discovery bridge.

The package lives at `services/growdirect-mcp/` and is installable as `growdirect-mcp`. Any new MCP server — whether for a GrowDirect app or a platform service — imports from this package rather than from the raw `mcp` SDK directly. See ADR `docs/decisions/2026-03-30-mcp-sdk-platform-standard.md`.

**Reference implementation:** Cove Knowledge MCP Server (`Cove/cove/mcp/server.py`) was refactored to use this package first and serves as the canonical pattern for all future servers.

**Relationship to Canary's custom framework:** Canary built its own `MCPTool`/`MCPRegistry`/`create_mcp_blueprint` stack (documented in `Canary/canary/mcp/`) before the official SDK existed. That framework continues to serve Canary's 12 domain servers. Retrofitting Canary is a separate spec — see Section 11.

---

## 2. Architecture

### Component Diagram

```
IDE Agent (Cursor / Claude Code / Claude Desktop)
    |
    | MCP stdio or streamable-HTTP
    v
App MCP Server (e.g., Cove/cove/mcp/server.py)
    |
    | imports
    v
services/growdirect-mcp/
    |
    +-- registry.py       GrowDirectRegistry — tool catalog + dispatch
    +-- tool.py           GrowDirectTool — handler wrapper + response envelope
    +-- auth.py           API key validation (optional)
    +-- bridge.py         Multi-server discovery bridge (future)
    |
    v
mcp Python SDK (mcp>=1.0)
    |
    +-- mcp.server.Server        — low-level server (used by Cove, new app servers)
    +-- mcp.server.fastmcp       — high-level API (used by Memory Bus)
    +-- mcp.server.stdio         — stdio transport (Cove)
    +-- mcp.server.streamable_http — HTTP transport (Memory Bus)
```

### Request / Data Flow

1. **Registration.** At server startup, the app creates a `GrowDirectRegistry` instance and calls `registry.register(GrowDirectTool(...))` once per tool. The registry holds a `dict[str, GrowDirectTool]`.

2. **List tools.** The MCP client calls `list_tools`. The server's `@server.list_tools()` handler delegates to `registry.list_tools()`, which returns `[tool.to_mcp() for tool in self._tools.values()]` — converting each `GrowDirectTool` to an `mcp.types.Tool`.

3. **Invocation.** The client calls a tool. The server's `@server.call_tool()` handler delegates to `registry.dispatch(name, arguments, context)`. The registry finds the tool, calls `tool.invoke(arguments, context)`, and returns `list[TextContent]`.

4. **Auth (optional).** If `auth.py` is wired, the `validate_api_key` function checks the `MCP_API_KEY` environment variable before dispatch. Auth is opt-in — stdio servers (trusted transport) typically skip it; HTTP servers enable it.

5. **Response envelope.** `GrowDirectTool.invoke` wraps the handler result in a standard envelope: `{"tool": name, "ok": true/false, "result": {...}, "timestamp": "..."}`. Handlers signal failure by returning `{"error": "msg"}`.

### Key Design Decisions

**Registry-per-server.** Each server creates its own `GrowDirectRegistry`. No global registry. Tool name collisions across servers are impossible by design.

**Handler signature.** `handler(params: dict, context: dict) -> dict`. The `params` are the tool's input arguments; `context` carries server-injected values (auth identity, request metadata). Async handlers are supported — `tool.invoke` detects coroutines and awaits them.

**SDK-native tool definitions.** `GrowDirectTool.to_mcp()` converts to `mcp.types.Tool` for the protocol layer. The registry never reimplements MCP wire format — it delegates to the SDK.

**Default secure.** `MCP_AUTH_DISABLED=true` must be set explicitly to skip auth on HTTP servers. Stdio servers are trusted by transport (no auth needed on stdio).

---

## 3. Data Model

**N/A — the platform SDK has no database tables.**

The `GrowDirectRegistry` is an in-memory `dict[str, GrowDirectTool]` held for the lifetime of the server process. There is no persistence layer.

Tool handlers access the data model of their parent domain (e.g., Cove's `knowledge_chunks` table, Memory Bus's `alx_memories`). Those models are documented in their respective SDDs.

---

## 4. Public API

### `GrowDirectRegistry`

```python
from growdirect_mcp import GrowDirectRegistry

registry = GrowDirectRegistry(
    server_name="my-server",
    version="1.0.0",
    description="Description of what this server exposes",
)
```

| Method | Signature | Description |
|--------|-----------|-------------|
| `register` | `(tool: GrowDirectTool) -> None` | Add a tool to the registry. Raises `ValueError` if name already registered. |
| `get` | `(name: str) -> GrowDirectTool \| None` | Look up a tool by name. |
| `list_tools` | `() -> list[Tool]` | Return SDK `Tool` objects for the MCP `list_tools` response. |
| `dispatch` | `(name, arguments, context) -> list[TextContent]` | Invoke a tool and return MCP-formatted result. |
| `get_manifest` | `() -> dict` | Return full server manifest (name, version, description, tools). |
| `build_server` | `() -> Server` | Build and return a configured `mcp.server.Server` with handlers wired. |

### `GrowDirectTool`

```python
from growdirect_mcp import GrowDirectTool

tool = GrowDirectTool(
    name="my_tool",
    description="What this tool does",
    handler=my_handler_function,   # (params: dict, context: dict) -> dict
    input_schema={...},            # JSON Schema object
    category="search",             # Optional category label
)
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Tool name — must be unique within a registry |
| `description` | `str` | Human-readable description for the MCP client |
| `handler` | `Callable` | Sync or async function `(params, context) -> dict` |
| `input_schema` | `dict` | JSON Schema for input validation |
| `category` | `str` | Optional grouping label (`"search"`, `"retrieval"`, `"ingest"`, etc.) |

### `auth.validate_api_key`

```python
from growdirect_mcp.auth import validate_api_key

is_valid = validate_api_key(provided_key)
# Checks against MCP_API_KEY env var
# Returns True if MCP_AUTH_DISABLED=true (explicit opt-out)
```

### `bridge.discover_servers`

```python
from growdirect_mcp.bridge import discover_servers

servers = await discover_servers()
# Reads MCP_BRIDGE_SERVERS env var (comma-separated URLs)
# Returns list of server metadata dicts
```

---

## 5. Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `registry.py` | Tool catalog, `dispatch`, `list_tools`, manifest generation |
| `tool.py` | Handler wrapping, response envelope, coroutine detection, exception handling |
| `auth.py` | API key validation against `MCP_API_KEY`; `MCP_AUTH_DISABLED` opt-out |
| `bridge.py` | Multi-server discovery — reads `MCP_BRIDGE_SERVERS`, aggregates manifests (future) |

---

## 6. Configuration

All configuration is environment-based.

| Env Var | Required | Default | Notes |
|---------|----------|---------|-------|
| `MCP_API_KEY` | No | `""` | API key for HTTP server auth. Empty = no auth (combined with `MCP_AUTH_DISABLED`). |
| `MCP_AUTH_DISABLED` | No | `false` | Set to `true` to explicitly disable auth on HTTP servers. |
| `MCP_JWT_SECRET` | No | `""` | JWT secret for token-based auth (alternative to API key). |
| `MCP_BRIDGE_SERVERS` | No | `""` | Comma-separated list of server base URLs for bridge discovery. |

---

## 7. Auth Model

The platform SDK uses a **default secure** posture:

- **Stdio transport:** No auth required. Stdio is a trusted transport — only the process that spawned the server can communicate with it.
- **HTTP transport:** Auth required by default. Set `MCP_API_KEY` in the server's environment. Clients must send `X-API-Key: <key>` on every tool call.
- **Explicit opt-out:** Set `MCP_AUTH_DISABLED=true` to skip API key validation. Use only in trusted network environments (e.g., internal Docker networks where network isolation is the auth boundary).

Cove Knowledge MCP uses stdio — no API key required. Memory Bus uses HTTP on the `growdirect` Docker network with `MCP_AUTH_DISABLED=true` (network isolation is the auth boundary). Future HTTP servers exposed outside the Docker network must use `MCP_API_KEY`.

---

## 8. Error Handling

Every tool invocation returns the standard response envelope. The envelope format for failures:

```json
{
  "tool": "tool_name",
  "ok": false,
  "error": "Human-readable error message",
  "timestamp": "2026-03-30T12:00:00+00:00"
}
```

**Handler-signaled failure:** Return `{"error": "msg"}` from the handler. The envelope sets `ok=False`.

**Unhandled exception:** `GrowDirectTool.invoke` catches all exceptions, logs them, and wraps them in the envelope. The MCP client always receives valid JSON.

**Unknown tool:** `registry.dispatch` returns an error envelope rather than raising. The client receives `{"tool": "name", "ok": false, "error": "Unknown tool: name"}`.

---

## 9. Testing

Tests live in `services/growdirect-mcp/tests/`.

| File | Coverage |
|------|---------|
| `test_registry.py` | Registration, duplicate detection, dispatch to known/unknown tools, list_tools output |
| `test_tool.py` | Sync handler, async handler, error dict passthrough, exception wrapping, envelope format |
| `test_auth.py` | API key match, key mismatch, `MCP_AUTH_DISABLED` bypass |
| `test_bridge.py` | Server discovery from `MCP_BRIDGE_SERVERS`, empty env var handling |

**Running tests:**

```bash
cd services/growdirect-mcp
python3 -m pytest tests/ -v
```

No external infrastructure required — all tests are pure unit tests using mocks.

---

## 10. Dependencies

### Runtime (`pyproject.toml`)

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp` | `>=1.0` | Official MCP Python SDK — Server, Tool, TextContent types |
| `httpx` | `>=0.27` | Async HTTP client for bridge discovery |
| `PyJWT` | `>=2.8` | JWT token validation (auth module) |

### Dev dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | `>=8.0` | Test runner |
| `pytest-asyncio` | `>=0.24` | Async test support |

### Build

```toml
[project]
name = "growdirect-mcp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["mcp>=1.0", "httpx>=0.27", "PyJWT>=2.8"]
```

Installed in app containers via `pip install -e services/growdirect-mcp/` or added to `requirements.txt` as `growdirect-mcp>=0.1.0`.

---

## 11. Known Issues & Retrofit Notes

### Canary Custom Framework — Retrofit Deferred

Canary's 12 domain MCP servers use a custom framework (`MCPTool`, `MCPRegistry`, `create_mcp_blueprint`) built before the official SDK existed. This framework is functional and continues to serve Canary. Retrofitting it to use `growdirect-mcp` is a separate spec (not tracked yet).

Until the retrofit, Canary's servers are reached via the custom HTTP blueprint stack (`Canary/canary/blueprints/*_mcp.py`) and the stdio adapter `Canary/canary/mcp/streamable_server.py`.

### `ops` Ghost Prefix in Canary

`Canary/canary/mcp/streamable_server.py` contains `"ops": "/ops-mcp"` in `SERVER_PREFIXES`. No `ops_mcp.py` blueprint exists in `Canary/canary/blueprints/`. The entry is marked with a `TODO` comment and kept to avoid breaking existing config references. Cleanup is deferred until the Canary retrofit spec.

### `alx` Entry Removed from Canary SERVER_PREFIXES

The `"alx": "/alx"` entry was removed from `Canary/canary/mcp/streamable_server.py` (GRO-379). The ALX memory tools were extracted to the standalone Memory Bus service (GRO-172) and are no longer served by the Canary Flask app.
