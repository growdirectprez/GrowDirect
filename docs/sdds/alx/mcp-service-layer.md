# MCP Service Layer (Platform SDK)

> **Status:** Production review — upgraded from design spec
> **Type:** MCP Server (Platform)
> **Namespace:** alx
> **Last updated:** 2026-04-13
> **Code location:** `services/growdirect-mcp/`

**Wiki:** [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]] · [[Brain/wiki/document-management|Document Management]]
**Related:** [[docs/sdds/platform/memory-bus|Memory Bus]] · [[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]]

---

## Purpose

The MCP Service Layer is the platform SDK wrapper that provides shared infrastructure for all GrowDirect MCP servers. It wraps the official `mcp` Python SDK with GrowDirect conventions: a tool registry, standard response envelopes, optional auth, and a discovery bridge. Any new MCP server imports from this package (`growdirect-mcp`) rather than from the raw `mcp` SDK directly.

The package is a library, not a running service. It has no process, no port, no container. It runs inside the process of whatever server imports it.

---

## Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| `mcp>=1.0` | Python package | Official MCP Python SDK — Server, Tool, TextContent types |
| `httpx>=0.27` | Python package | Async HTTP client for bridge discovery |
| `PyJWT>=2.8` | Python package | JWT token validation (auth module) |

No external services required. The SDK runs inside the host server's process and inherits that server's database connections, Valkey sessions, and network context.

**Consumers (servers that import this package):**

| Server | Transport | Auth | Where |
|--------|-----------|------|-------|
| Memory Bus | HTTP (streamable-http, port 8003) | API key per-tool (manual) | `services/memory-bus/` |
| Cove Knowledge | stdio | None (trusted transport) | `Cove/cove/mcp/` |

**Not yet consuming (custom framework):**

| Server | Notes |
|--------|-------|
| Canary (12 domain servers) | Custom `MCPTool`/`MCPRegistry`/`create_mcp_blueprint` — retrofit deferred |

---

## Data Flow & PII Map

The MCP Service Layer itself stores no data. It is a pass-through wrapper. However, every tool dispatched through this layer can access whatever data its parent server exposes. This makes the SDK a **PII amplifier** — its security posture determines the security posture of all data behind every consuming server.

### What enters

- MCP `call_tool` requests from IDE agents (Claude Code, Cursor, Claude Desktop)
- Tool arguments as JSON dictionaries
- Optional API key (as `X-API-Key` header for HTTP, as tool parameter for Memory Bus)

### What's stored

Nothing. The `GrowDirectRegistry` is an in-memory `dict[str, GrowDirectTool]` for the lifetime of the server process. No persistence layer.

### What exits

- MCP `TextContent` responses containing JSON-serialized response envelopes
- Response envelopes include: tool name, ok/error status, result payload, ISO timestamp

### PII exposure by consuming server

| Server | PII Fields Accessible via SDK Dispatch | Classification |
|--------|---------------------------------------|----------------|
| Memory Bus | Session summaries, decisions, context content (may contain any project data including names, addresses) | internal |
| Cove Knowledge | Legal document chunks, CC&R text, litigation records, APN references, HOA member names in meeting transcripts | internal/sensitive |
| Bridge (future) | Aggregates tools from all servers — full PII surface of every connected server | sensitive |

**Key risk:** The SDK provides no field-level PII filtering. Whatever the handler returns goes straight into the response envelope and out to the MCP client. PII redaction is entirely the handler's responsibility.

---

## API Contract

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
| `register` | `(tool: GrowDirectTool) -> None` | Add a tool. Raises `ValueError` on duplicate name. |
| `get` | `(name: str) -> GrowDirectTool | None` | Look up a tool by name. |
| `list_tools` | `() -> list[Tool]` | Return SDK `Tool` objects for MCP `list_tools` response. |
| `dispatch` | `(name, arguments, context) -> list[TextContent]` | Invoke a tool and return MCP-formatted result. |
| `get_manifest` | `() -> dict` | Return full server manifest (name, version, description, tools). |
| `build_server` | `() -> Server` | Build configured `mcp.server.Server` with handlers wired. |
| `tool_names` | `() -> list[str]` | Return list of registered tool names. |

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
| `input_schema` | `dict` | JSON Schema for input (documentation only — not enforced) |
| `category` | `str` | Optional grouping label (`"search"`, `"retrieval"`, `"ingest"`, etc.) |

### `auth.validate_api_key`

```python
from growdirect_mcp.auth import validate_api_key, AuthError

is_valid = validate_api_key(provided_key)
# Checks against MCP_API_KEY env var
# Returns True if MCP_AUTH_DISABLED=1 (explicit opt-out)
# Raises AuthError on failure
```

### `auth.validate_jwt`

```python
from growdirect_mcp.auth import validate_jwt, AuthError

claims = validate_jwt(token)
# Decodes HS256 JWT using MCP_JWT_SECRET env var
# Returns claims dict on success
# Raises AuthError on failure
```

### `bridge.discover_servers` / `bridge.build_bridge_registry`

```python
from growdirect_mcp.bridge import discover_servers, build_bridge_registry

servers = discover_servers()       # Reads MCP_BRIDGE_SERVERS env var (JSON array)
bridge = build_bridge_registry(servers)  # Builds registry with proxied tools
```

### Response Envelope

Every tool invocation returns a standard envelope:

```json
{
  "tool": "tool_name",
  "ok": true,
  "result": { ... },
  "timestamp": "2026-04-13T12:00:00+00:00"
}
```

Error variant:

```json
{
  "tool": "tool_name",
  "ok": false,
  "error": "Human-readable error message",
  "timestamp": "2026-04-13T12:00:00+00:00"
}
```

---

## MCP Tool Registry

The MCP Service Layer is a library, not a tool-serving server. It does not expose tools directly. Instead, it provides the registry pattern that consuming servers use to register and dispatch their own tools.

### Tool Registration Pattern

1. Server creates a `GrowDirectRegistry` with server metadata
2. Server creates `GrowDirectTool` instances wrapping handler functions
3. Server calls `registry.register(tool)` for each tool
4. Server calls `registry.build_server()` to get a configured `mcp.server.Server`
5. Server runs the built server on its chosen transport (stdio or HTTP)

Alternatively (Memory Bus pattern): server uses `FastMCP` directly from the `mcp` SDK and imports only `validate_api_key` from `growdirect_mcp.auth` for auth validation. This bypasses the registry entirely.

### How New Tools Are Registered

A new tool requires:
1. A handler function with signature `(params: dict, context: dict) -> dict`
2. A JSON Schema defining accepted input
3. A `GrowDirectTool` wrapper with name, description, handler, schema
4. A `registry.register(tool)` call before the server starts

There is no dynamic registration after startup. All tools are registered at import time.

### Tools Dispatched Through Consuming Servers

| Server | Tool | Auth | PII Access | Description |
|--------|------|:----:|:----------:|-------------|
| Memory Bus | `session_start` | API key | No | Start ALX session |
| Memory Bus | `session_close` | API key | Low | Close session with summary |
| Memory Bus | `memory_store` | API key | Yes — content may contain any data | Store memory with embedding |
| Memory Bus | `memory_recall` | API key | Yes — returns stored content | Semantic search over memories |
| Memory Bus | `memory_search` | API key | Yes — returns stored content | Structured search by filters |
| Memory Bus | `context_assemble` | API key | Yes — assembles cross-domain context | Context window assembly |
| Memory Bus | `domain_context` | API key | Yes — full domain context | Domain context with token budget |
| Cove Knowledge | `knowledge_search` | None | Yes — legal docs, names in transcripts | Semantic search |
| Cove Knowledge | `knowledge_get_chunk` | None | Yes — full chunk content | Chunk retrieval |
| Cove Knowledge | `knowledge_list_sources` | None | No | Source listing |
| Cove Knowledge | `knowledge_stats` | None | No | Statistics |
| Cove Knowledge | `knowledge_find_by_apn` | None | Yes — APN is quasi-PII | APN search |
| Cove Knowledge | `knowledge_find_by_citation` | None | No | Citation search |
| Cove Knowledge | `knowledge_ingest_document` | None | Yes — raw doc content | Document ingestion |
| Cove Knowledge | `knowledge_add_chunk` | None | Yes — chunk content | Single chunk add |
| Cove Knowledge | `knowledge_delete_source` | None | No | Source deletion |
| Cove Knowledge | `knowledge_reindex` | None | No | Embedding regeneration |

---

## Cross-App Data Access

The MCP Service Layer enables cross-app data access through two mechanisms:

1. **Bridge discovery** (`bridge.py`): Aggregates tool manifests from multiple servers. A bridge registry can expose tools from Memory Bus, Cove Knowledge, and any future server through a single MCP endpoint. Not yet deployed in production.

2. **Memory Bus layer scoping**: Memory Bus stores memories tagged with layer (`corp`, `canary`, `cove`, `shared`). Any MCP client with the API key can query any layer — there is no per-layer access control.

**Tenant isolation:** None. The platform is single-tenant (GrowDirect). All apps share the same Memory Bus. The API key is the same for all callers. There is no concept of app-scoped or user-scoped access tokens.

---

## Tool Dispatch Security

### Authentication model

- **Auth is opt-in, not built into dispatch.** The `registry.dispatch()` method calls the handler directly. It does not invoke `validate_api_key` or `validate_jwt`. Auth must be implemented by each consuming server independently.
- **`build_server()` passes empty context.** The built server's `handle_call_tool` calls `dispatch(name, arguments, {})` — the context dict that could carry auth identity is always empty.
- **Memory Bus implements auth per-tool.** Each tool function accepts `api_key` as a parameter and calls `validate_api_key()` manually. This works but is error-prone — a new tool added without the auth check silently runs unauthenticated.
- **Cove Knowledge has no auth.** Relies on stdio transport being trusted. Correct for local IDE use; problematic if the server is ever exposed over HTTP.

### Privilege escalation risks

- **Bridge proxy:** If the bridge aggregates tools from servers with different auth levels, a single API key grants access to all tools. There is no per-tool or per-server auth scoping.
- **No RBAC:** All authenticated callers have identical privileges. There is no read-only vs. read-write distinction.
- **Handler exceptions expose internals:** `str(e)` in the error envelope can leak database connection strings, file paths, or internal state.

### What happens if the MCP server is compromised

If an attacker gains access to the MCP transport:
- **Memory Bus (HTTP):** Full read/write access to all memories across all layers. Can store malicious content, recall any stored data. Mitigated by `127.0.0.1` port binding and Docker network isolation.
- **Cove Knowledge (stdio):** Full read/write access to the knowledge base. Can ingest malicious documents, delete sources. Mitigated by stdio being process-local.
- **Bridge (future):** Full access to all aggregated servers' tools.

---

## Operations

### Startup Sequence

N/A — the SDK is a library, not a service. It initializes when imported by a consuming server. No startup sequence, no readiness probe.

### Health Checks

N/A — no process to monitor. Health of consuming servers is documented in their respective SDDs.

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Handler raises exception | Single tool call fails | Exception caught, wrapped in error envelope, client receives valid JSON |
| Handler returns `{"error": ...}` | Single tool call fails gracefully | Wrapped in error envelope with `ok: false` |
| Unknown tool dispatched | Single tool call rejected | Error envelope returned, no crash |
| `build_server()` called with 0 tools | Server starts but `list_tools` returns empty | Clients see no available tools |
| Auth env vars missing on HTTP server | All authenticated calls fail | `AuthError` raised, but only if auth is manually invoked |
| Bridge target server unreachable | Bridge startup loses that server's tools | Warning logged, bridge continues with remaining servers |

### Configuration

| Env Var | Required | Default | Notes |
|---------|----------|---------|-------|
| `MCP_API_KEY` | No | `""` | API key for HTTP server auth. Dev default: `growdirect-memory-dev-key` |
| `MCP_AUTH_DISABLED` | No | `""` | Set to `"1"` to disable auth. **Note:** code checks for `"1"`, not `"true"` despite earlier docs. |
| `MCP_JWT_SECRET` | No | `""` | JWT secret for token-based auth (not used by any server currently) |
| `MCP_BRIDGE_SERVERS` | No | `""` | JSON array of `{name, base_url, transport, api_key}` objects for bridge discovery |

### Monitoring

No metrics emitted by the SDK itself. Consuming servers should instrument:
- Tool dispatch latency (per tool name)
- Error rate (envelope `ok: false` count)
- Auth failure count

---

## Deployment

### Package Installation

The SDK is installed as an editable package or pinned dependency in consuming server containers:

```bash
# In Dockerfile or requirements.txt
pip install -e /app/services/growdirect-mcp/
# or
pip install growdirect-mcp>=0.1.0
```

### Docker

No standalone container. The SDK ships inside consuming server images:
- Memory Bus: `devops/docker-compose.yml` → `memory-bus` service
- Cove Knowledge: runs inside `cove_flask` container as a subprocess

### AWS Target

- Package included in ECS task definitions for consuming services
- `MCP_API_KEY` → AWS Secrets Manager (not env var)
- `MCP_JWT_SECRET` → AWS Secrets Manager (if JWT auth is enabled)

### Build

```toml
[project]
name = "growdirect-mcp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["mcp>=1.0", "httpx>=0.27", "PyJWT>=2.8"]
```

---

## Testing

Tests live in `services/growdirect-mcp/tests/`. All pure unit tests — no external infrastructure required.

| File | Coverage |
|------|---------|
| `test_registry.py` | Registration, duplicate detection, dispatch to known/unknown tools, list_tools output, manifest, contains, len |
| `test_tool.py` | Sync handler, async handler, error dict passthrough, exception wrapping, envelope format, to_mcp conversion |
| `test_auth.py` | API key match/mismatch/missing, `MCP_AUTH_DISABLED` bypass, JWT valid/invalid/no-secret |
| `test_bridge.py` | Server config creation, env var parsing, empty env handling, bridge registry with HTTP discovery |

```bash
cd services/growdirect-mcp
python3 -m pytest tests/ -v
```

### Test Gaps

- No integration test for `build_server()` end-to-end (server build → list_tools → call_tool)
- No test for auth integration with dispatch (because auth is not integrated with dispatch)
- No test for timing-safe key comparison
- No test for `MCP_AUTH_DISABLED=true` (code only checks `"1"`)
- Bridge proxy handlers are tested for registration but not for actual HTTP proxying

---

## Code Review Findings

### P0 — Blocks Production

**P0-1: Auth not integrated into `build_server()` dispatch path**

`build_server()` creates a server where `handle_call_tool` calls `dispatch(name, arguments, {})` with empty context. Auth validation from `auth.py` is never invoked. Any server using `build_server()` runs completely unauthenticated regardless of `MCP_API_KEY` configuration. The Memory Bus works around this by not using `build_server()` (it uses `FastMCP` and validates auth per-tool manually), but this means the primary API of the SDK — the one documented as the canonical pattern — has no auth.

**Recommended fix:** Add an optional `auth_required: bool` parameter to `GrowDirectRegistry`. When enabled, `build_server()` should extract the API key from the MCP request context and call `validate_api_key()` before dispatching. Alternatively, add auth middleware to the `dispatch()` method itself.

**Linear:** Needs GRO issue.

---

**P0-2: API key comparison is not timing-safe**

`auth.py` line 27: `if provided_key != expected_key` uses Python's default string comparison, which short-circuits on first differing character. This enables timing attacks against the API key on HTTP-exposed servers.

**Recommended fix:** Replace with `hmac.compare_digest(provided_key, expected_key)`.

**Linear:** Needs GRO issue.

---

**P0-3: `MCP_API_KEY` hardcoded default in docker-compose**

`devops/docker-compose.yml` line 107: `MCP_API_KEY: ${MCP_API_KEY:-growdirect-memory-dev-key}`. The fallback default `growdirect-memory-dev-key` means the Memory Bus starts with a known, committed-to-git API key if the env var is unset. In production, if the Secrets Manager integration fails or the env var is misconfigured, the server falls back to a public key.

**Recommended fix:** Remove the default. Require `MCP_API_KEY` to be set explicitly. Server should refuse to start if the key is missing in production.

**Linear:** Needs GRO issue.

---

### P1 — Before GA

**P1-1: No input schema validation on dispatch**

`dispatch()` passes raw `arguments` to the handler without validating against the tool's `input_schema`. The schema is used only for documentation (sent to clients via `list_tools`). A malformed or malicious input payload reaches the handler unchecked. Handlers must defensively validate all input individually.

**Recommended fix:** Add optional JSON Schema validation in `dispatch()` before calling `tool.invoke()`. Use `jsonschema.validate()` or equivalent. Make it opt-in per registry to avoid breaking existing servers.

**Linear:** Needs GRO issue.

---

**P1-2: Exception messages leak to MCP clients**

`GrowDirectTool.invoke()` catches all exceptions and wraps `str(e)` in the error envelope. Database connection errors (`sqlalchemy.exc.OperationalError`), file path errors, and internal assertion messages are sent verbatim to the MCP client.

**Recommended fix:** Sanitize error messages before including in the envelope. Log the full exception server-side; return a generic error message to the client (e.g., "Internal error — check server logs"). Add a `debug_mode` flag that allows full messages in dev.

**Linear:** Needs GRO issue.

---

**P1-3: JWT validation lacks audience and issuer checks**

`auth.validate_jwt()` calls `pyjwt.decode(token, secret, algorithms=["HS256"])` without specifying `audience` or `issuer`. A JWT minted for one service could be replayed against another. No expiration enforcement is configured (PyJWT checks `exp` by default, but no `leeway` is set).

**Recommended fix:** Add `audience` and `issuer` parameters to `validate_jwt()`. Require `iss=growdirect` and `aud=<server_name>` claims. Set a reasonable `leeway` (e.g., 30 seconds).

**Linear:** Needs GRO issue.

---

**P1-4: `MCP_AUTH_DISABLED` value inconsistency**

Code in `auth.py` checks `MCP_AUTH_DISABLED == "1"`. The original SDD documented the value as `"true"`. Memory Bus docker-compose does not set this variable at all (relying on the API key instead). If someone reads the old docs and sets `MCP_AUTH_DISABLED=true`, auth remains enabled — a silent misconfiguration that could cause production incidents.

**Recommended fix:** Accept both `"1"` and `"true"` (case-insensitive). Document the canonical value as `"1"` everywhere.

**Linear:** Needs GRO issue.

---

**P1-5: No audit logging for tool dispatch**

Neither the SDK nor any consuming server logs which tools were called, by whom, or with what arguments. For servers handling PII (Memory Bus stores/recalls arbitrary content, Cove Knowledge searches legal docs), there is no audit trail.

**Recommended fix:** Add structured logging in `dispatch()`: log tool name, timestamp, truncated arguments (with PII redaction), and outcome (ok/error). Consuming servers add caller identity from auth context.

**Linear:** Needs GRO issue.

---

**P1-6: No rate limiting on tool dispatch**

The SDK provides no rate limiting. Memory Bus is exposed on port 8003 (bound to `127.0.0.1`) with no request throttling. A compromised IDE extension or runaway agent could exhaust database connections or embedding API quotas.

**Recommended fix:** Add optional rate limiting to `GrowDirectRegistry` (token bucket per tool or per caller). Alternatively, document that rate limiting is the consuming server's responsibility and add it at the transport layer.

**Linear:** Needs GRO issue.

---

### P2 — Post-Launch

**P2-1: Bridge proxy handlers are stubs**

`bridge.py` `build_bridge_registry()` registers tools with lambda handlers that return `{"proxy": True, "server": url, "tool": name}` — metadata about where to call, but no actual HTTP proxying. The bridge cannot forward tool calls to remote servers.

**Recommended fix:** Implement actual HTTP proxying in bridge tool handlers using `httpx.AsyncClient`. Add timeout, retry, and error handling.

**Linear:** Needs GRO issue.

---

**P2-2: `discover_servers` is synchronous despite bridge needing async**

`bridge.discover_servers()` and `build_bridge_registry()` are synchronous functions using synchronous `httpx.get()`. This blocks the event loop if called from an async server context.

**Recommended fix:** Make `discover_servers()` async. Use `httpx.AsyncClient` for manifest fetching.

**Linear:** Needs GRO issue.

---

**P2-3: No tool versioning**

Tools have no version field. Schema changes to a tool's input are breaking changes with no way for clients to detect or negotiate API versions.

**Recommended fix:** Add optional `version` field to `GrowDirectTool`. Include in manifest output. Consider supporting multiple versions of the same tool.

**Linear:** Needs GRO issue.

---

**P2-4: Cove Knowledge MCP does not use the SDK**

Despite being documented as the "reference implementation" for the SDK, Cove Knowledge MCP server (`Cove/cove/mcp/server.py`) uses the raw `mcp.server.Server` directly. It does not import `GrowDirectRegistry` or `GrowDirectTool`. Tool definitions are raw `mcp.types.Tool` objects. The handler dispatch is a manual `_HANDLERS` dict. There is no response envelope wrapping.

This means the SDK has exactly zero deployed consumers using its registry/tool pattern. The Memory Bus imports only `validate_api_key` from `auth.py`.

**Recommended fix:** Either refactor Cove Knowledge to actually use the SDK (making it a true reference implementation) or update the documentation to accurately describe the current adoption state.

**Linear:** Needs GRO issue.

---

## Production Readiness Checklist

- [ ] **PII encrypted at rest** — N/A for SDK (no storage). Consuming servers: Memory Bus stores plaintext content in `growdirect_memory` DB. Cove Knowledge stores plaintext document chunks.
- [ ] **Secrets in AWS Secrets Manager** — `MCP_API_KEY` currently in docker-compose env with hardcoded fallback. `MCP_JWT_SECRET` not deployed. Needs migration to Secrets Manager.
- [ ] **Health check endpoint responds** — N/A (library, not service). Consuming servers have their own health checks.
- [ ] **Audit logging for sensitive operations** — Not implemented. No tool dispatch logging. See P1-5.
- [ ] **Data retention policy implemented** — N/A for SDK. Memory Bus has no retention policy (memories accumulate indefinitely). See Memory Bus SDD.
- [ ] **Rate limiting on public endpoints** — Not implemented. Memory Bus port 8003 has no rate limiting. See P1-6.
- [ ] **Error responses don't leak internals** — Not implemented. Exception messages pass through to clients. See P1-2.
- [ ] **Auth integrated into dispatch** — Not implemented. Auth is per-tool manual in Memory Bus, absent in Cove Knowledge. See P0-1.
- [ ] **Timing-safe key comparison** — Not implemented. See P0-2.
- [ ] **Input validation on tool dispatch** — Not implemented. See P1-1.

---

## Known Issues & Retrofit Notes

### Canary Custom Framework — Retrofit Deferred

Canary's 12 domain MCP servers use a custom framework (`MCPTool`, `MCPRegistry`, `create_mcp_blueprint`) built before the official SDK existed. This framework is functional and continues to serve Canary. Retrofitting it to use `growdirect-mcp` is a separate spec (not tracked yet).

### `ops` Ghost Prefix in Canary

`Canary/canary/mcp/streamable_server.py` contains `"ops": "/ops-mcp"` in `SERVER_PREFIXES`. No `ops_mcp.py` blueprint exists. The entry is kept to avoid breaking config references. Cleanup deferred until Canary retrofit.

### `alx` Entry Removed from Canary

The `"alx": "/alx"` entry was removed from Canary's `streamable_server.py` (GRO-379). ALX memory tools now live in the standalone Memory Bus service (GRO-172).

### SDK Adoption Gap

The SDK's primary API (`GrowDirectRegistry` + `GrowDirectTool` + `build_server()`) has no production consumers. Memory Bus uses `FastMCP` + manual auth. Cove Knowledge uses raw `mcp.server.Server`. The SDK is tested but not battle-tested. See P2-4.
