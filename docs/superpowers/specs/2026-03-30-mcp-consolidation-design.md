# MCP Consolidation — Platform SDK, ALX Extraction, Full Sweep

> **Date:** 2026-03-30
> **Status:** Approved
> **Scope:** Platform MCP package (`growdirect-mcp`), ALX extraction from Canary, Cove polish, Memory Bus full sweep, SDD updates, ADR
> **Goal:** Establish the official `mcp` Python SDK as the platform standard, extract ALX to platform level, and address all known MCP-related architectural findings from the SDD audit

---

## Context

The SDD build-out (2026-03-30) audited all 17 services and surfaced critical architectural findings in the MCP layer:

1. **Canary built a custom MCP framework** (`MCPTool`/`MCPRegistry`/`create_mcp_blueprint`) without knowing the official `mcp` Python SDK existed. This is legitimate tech debt.
2. **Cove uses the SDK correctly** — `mcp.server.Server`, `mcp.types.Tool`, stdio transport, async-native. This is the right pattern.
3. **ALX is tangled into Canary** — the COO/platform agent infrastructure lives in `Canary/canary/mcp/` and `Canary/canary/services/qa_agent/`. ALX belongs at platform level.
4. **Memory Bus has 7 unaddressed Section 11 findings** — dual-codebase confusion, auth, misplaced tests, dead tables, missing indexes, soft FKs, no migration strategy, SDK alignment.
5. **QA Agent is misclassified** — it's a Canary app-level test runner, not ALX. Its SDD sits in `docs/sdds/alx/` incorrectly.
6. **Dual-codebase confusion** — `services/memory-bus/` (platform memory, FastMCP HTTP) and `Cove/cove/mcp/` (legal knowledge, SDK stdio) are different services with different purposes, but both get called "MCP" and the split is undocumented. Builders don't know which to use.

### Architectural Decision

- The official `mcp` Python SDK is the platform standard for all MCP servers going forward. This decision requires an ADR at `docs/decisions/2026-03-30-mcp-sdk-platform-standard.md`.
- Cove's implementation is the reference pattern.
- ALX is a platform service (`services/alx/`), not a Canary service.
- The MCP SDK package lives at `services/growdirect-mcp/` (platform infrastructure), separate from `services/alx/` (the COO agent). ALX consumes the package but doesn't own it — the package is platform infrastructure that all apps use.
- Canary's custom MCP framework is tech debt. Canary keeps its 12 domain servers on the custom framework until a separate retrofit spec. No Canary code changes in this spec except removing ALX-specific entries.
- If Canary needs an app-level agent, that's a Canary app agent, not ALX.
- Memory Bus (`services/memory-bus/`) is **platform organizational memory** — ALX sessions, decisions, context blocks. Cove MCP (`cove/mcp/`) is **app-level legal knowledge** — CC&Rs, bylaws, litigation documents. They are different services with different purposes, different databases, and different transports. This spec clarifies the boundary and documents it in both SDDs.

---

## Scope

### In Scope

1. Platform MCP SDK package at `services/growdirect-mcp/`
2. ALX extraction from Canary to `services/alx/`
3. Cove MCP polish (registry pattern, remove hardcoded dispatch)
4. Memory Bus full sweep (all Section 11 findings including dual-codebase clarification)
5. SDD updates for all affected documents
6. QA Agent SDD reclassification (`alx/` → `canary/`)
7. ADR documenting the `mcp` SDK as platform standard

### Out of Scope

- Canary MCP retrofit to SDK (separate spec)
- QA Agent code changes (parked, Canary app-level)
- ALX builder dispatch / Linear coordination (future spec)
- ALX Cowork session management (future spec)

---

## 1. Platform MCP Package

**Location:** `services/growdirect-mcp/`

A shared platform package wrapping the official `mcp` Python SDK with GrowDirect conventions. Every app's MCP servers import from here. This is platform infrastructure — not owned by ALX, Canary, or Cove. All apps consume it.

### Package Name and Distribution

- **Package name:** `growdirect-mcp`
- **Import path:** `from growdirect_mcp import GrowDirectRegistry, GrowDirectTool`
- **Distribution:** Installed via `pip install -e /path/to/services/growdirect-mcp` in dev. In Docker, the package directory is copied into the build context and installed during image build. No private PyPI — the monorepo is the distribution mechanism.
- **Docker integration:** Each app's `Dockerfile` adds `COPY services/growdirect-mcp /tmp/growdirect-mcp && pip install /tmp/growdirect-mcp` before installing app dependencies. This requires adjusting Docker build contexts to include the platform services directory (e.g., `context: ../../` with appropriate `.dockerignore`).

### Components

#### `registry.py` — GrowDirectRegistry

Wraps the SDK's `Server` class. Provides:

- Tool registration with JSON Schema input validation
- Context injection (merchant_id, org_id, user_id) — passed to handlers as a `context` dict
- Health check convention — every server exposes health status
- Manifest generation — tool catalog for discovery

Replaces Canary's custom `MCPRegistry`. Uses the same handler signature (`def handler(params: dict, context: dict) -> dict`) so existing tool handlers can migrate with minimal changes.

#### `tool.py` — GrowDirectTool

Thin wrapper around SDK `Tool`. Adds:

- Standard response envelope: `{"ok": true/false, "result"/"error": <data>, "timestamp": "ISO-8601"}`
- Exception handling — handler exceptions caught, logged, wrapped as `ok: false`
- Category tagging — tools grouped by category for discovery

#### `bridge.py` — Stdio-HTTP Bridge

Platform-level IDE integration. Replaces Canary's `streamable_server.py`.

- Uses the SDK's native stdio transport (not custom FastMCP wrapper)
- Discovers tools from SDK-based servers only (Cove, Memory Bus, future apps). Canary's custom framework servers are not discoverable until Canary retrofit.
- Auth: API key (production), Bearer token (dev)
- Supports all apps that use the platform MCP package

#### `auth.py` — Auth Middleware

Composable auth for MCP transports:

- API key validation (`X-API-Key` header or `MCP_API_KEY` env var)
- JWT validation (for inter-service calls)
- No-auth mode for trusted Docker network (explicit opt-in, not default)

### Design Principles

- **No Flask dependency.** The SDK is async-native. Transports run standalone or as sidecars.
- **No database opinions.** Tools bring their own DB access (psycopg2, SQLAlchemy, or none).
- **No embedding opinions.** Tools call Ollama directly if needed.
- **Transport-agnostic.** Same registry serves stdio (IDE), HTTP (inter-service), or both.

### Directory Structure

```
services/growdirect-mcp/
├── growdirect_mcp/
│   ├── __init__.py           — exports GrowDirectRegistry, GrowDirectTool
│   ├── registry.py           — GrowDirectRegistry (SDK Server wrapper)
│   ├── tool.py               — GrowDirectTool (SDK Tool wrapper)
│   ├── bridge.py             — stdio↔HTTP for IDE integration
│   └── auth.py               — API key + JWT middleware
├── pyproject.toml            — package metadata, mcp SDK dependency
└── tests/
    ├── test_registry.py
    ├── test_tool.py
    ├── test_bridge.py
    └── test_auth.py
```

---

## 2. ALX Extraction

ALX moves from Canary to platform level. ALX is the COO — platform coordination, memory, agent infrastructure.

### What Moves

| Source (Canary) | Destination (Platform) | Notes |
|-----------------|----------------------|-------|
| `canary/mcp/streamable_server.py` | `services/growdirect-mcp/growdirect_mcp/bridge.py` | Rewritten to use SDK native stdio, discovers tools from SDK-based servers |

### What Stays in Canary

| File | Reason |
|------|--------|
| `canary/mcp/registry.py` | Custom framework, tech debt — retrofit later |
| `canary/mcp/tool.py` | Custom framework, tech debt — retrofit later |
| `canary/mcp/blueprint.py` | Custom framework, tech debt — retrofit later |
| `canary/mcp/standalone.py` | Obsoleted by SDK native transports, dead code until retrofit |
| `canary/services/qa_agent/` | App-level test runner, not ALX |
| All `*_mcp.py` blueprints | Domain tools, app-level |

### Changes in Canary

- Remove ALX entries from `SERVER_PREFIXES` and `SERVER_BLUEPRINTS` maps (partially done per GRO-172)
- `streamable_server.py` stays as dead code until retrofit (no deletion — Canary might still reference it)

### ALX Platform Responsibilities

ALX at platform level owns:

1. **Platform coordination** — dispatch, monitoring, status rollups (future specs)
2. **Memory bus integration** — ALX is the primary consumer of `services/memory-bus/`

ALX consumes but does NOT own:

- **Platform MCP package** (`services/growdirect-mcp/`) — platform infrastructure, all apps use it

ALX does NOT own (future specs):

- Builder dispatch / Linear coordination
- Cowork session management
- App-level agents (those belong to their apps)

---

## 3. Cove MCP Polish

Cove already uses the SDK correctly. The changes here make it the reference implementation by addressing the scaling issues.

### Refactor Tool Registration

**Current (hardcoded):**
```python
TOOLS = [Tool(name="knowledge_search", ...), Tool(name="knowledge_get_chunk", ...), ...]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "knowledge_search":
        result = await search.knowledge_search(**arguments)
    elif name == "knowledge_get_chunk":
        result = await retrieval.knowledge_get_chunk(**arguments)
    # ... 8 more elif chains
```

**Target (platform registry):**
```python
from growdirect_mcp import GrowDirectRegistry, GrowDirectTool

registry = GrowDirectRegistry(
    server_name="cove-knowledge",
    version="1.0.0",
    description="Cove legal/governance knowledge base",
)

registry.register(GrowDirectTool(
    name="knowledge_search",
    description="Semantic similarity search across knowledge base",
    handler=search.knowledge_search,
    input_schema={...},
    category="search",
))
# ... register remaining tools
```

### What Stays Unchanged

- `db.py` — psycopg2 connection pool. Correct for standalone knowledge service.
- `embeddings.py` — Ollama HTTP interface. Domain-specific, well-built.
- `chunking.py` — Markdown-aware document splitting. Domain-specific.
- `tools/search.py`, `tools/retrieval.py`, `tools/ingest.py` — Handler functions stay as-is. Only the registration and dispatch mechanism changes.
- `tools/resources.py` — MCP Resources. SDK handles these natively.
- Stdio transport — correct for Cove's use case.
- Async model — native to the SDK.

### Net Effect

Cove's `server.py` gets simpler. Registry replaces hardcoded list. Dispatch is automatic. Cove becomes the pattern every future MCP server follows.

---

## 4. Memory Bus Full Sweep

`services/memory-bus/` is already platform-level. Address all Section 11 findings.

### 4.0 Dual-Codebase Clarification

**Finding (CRITICAL):** `services/memory-bus/` (platform organizational memory) and `Cove/cove/mcp/` (app-level legal knowledge) are both "MCP services" but serve completely different purposes. The split is undocumented and confusing.

**Fix:** Document the boundary explicitly in both SDDs:
- **Memory Bus** = platform memory. Stores ALX sessions, architectural decisions, context blocks. Database: `growdirect_memory`. Transport: FastMCP HTTP (port 8003). Consumers: ALX, all builders.
- **Cove Knowledge MCP** = app-level knowledge. Stores CC&Rs, bylaws, litigation docs, property records. Database: `cove` (knowledge_chunks table). Transport: MCP SDK stdio. Consumers: Cove agents, Claude Desktop/Cowork.

They share embedding infrastructure (both use `qwen3-embedding:8b`, 1024-dim) but are architecturally separate. This is correct — platform memory and app-level knowledge are different domains. The confusion was naming, not architecture.

### 4.1 Authentication

**Finding:** Any container on the `growdirect` Docker network can read/write all memories with no authentication.

**Fix:** Add `MCP_API_KEY` env var check on all tool calls. Match the pattern Cove uses. Reject unauthenticated calls with a clear error. Update `docker-compose.yml` to set the key.

### 4.2 Misplaced Tests

**Finding:** `test_context_blocks.py` and `test_rag_retrieval.py` import from `canary.services.alx.memory` — old Canary-side code that doesn't exist in the memory-bus service.

**Fix:** Remove both files. Write replacement tests that exercise the actual `memory_bus` service: `memory_store`, `memory_recall`, `context_assemble`, and `session_start`/`session_close` workflows.

### 4.3 seed_embeddings Table

**Finding:** `seed_embeddings` table exists in DDL but is not queried by any code. `seed_clean.py` inserts into `alx_memories`, not `seed_embeddings`. `store.py` does not reference it.

**Fix:** Drop the table. Remove from `02-create-memory-db.sql`. If a high-fidelity RAG source is needed in the future, design it with a clear purpose and add it through Alembic.

### 4.4 HNSW Index

**Finding:** Vector search on `alx_memories.embedding` uses sequential scan. Will degrade at tens of thousands of memories.

**Fix:** Add HNSW index with cosine distance operator:
```sql
CREATE INDEX idx_alx_memories_embedding_hnsw
ON alx_memories USING hnsw (embedding vector_cosine_ops);
```

### 4.5 session_id Foreign Key

**Finding:** `alx_memories.session_id` is a text column with no referential integrity constraint. Allows arbitrary session IDs (`'seed-clean'`, `'unattached'`) without corresponding session records.

**Fix:** Create session records for existing orphan session IDs, then add the FK constraint.

Data migration:
1. Query `SELECT DISTINCT session_id FROM alx_memories WHERE session_id NOT IN (SELECT session_id FROM alx_sessions)` to find all orphans
2. For each orphan, insert a session record with `status='closed'`, `started_at=MIN(created_at)` from that session's memories, `closed_at=MAX(created_at)`
3. Add FK: `ALTER TABLE alx_memories ADD CONSTRAINT fk_memories_session FOREIGN KEY (session_id) REFERENCES alx_sessions(session_id)`

Post-migration: `seed_clean.py` must create a proper session before writing memories. `memory_store()` must validate that the session exists before accepting writes.

### 4.6 Alembic Migration Management

**Finding:** `growdirect_memory` schema is managed by raw SQL in `02-create-memory-db.sql`, not through Alembic. Schema changes require manual SQL or volume wipe.

**Fix:** Bring `growdirect_memory` under Alembic. Sequencing:

1. Create initial Alembic migration capturing the **pre-fix** DDL (current state of `02-create-memory-db.sql`). This is the baseline.
2. Fixes 4.3 (drop seed_embeddings), 4.4 (HNSW index), and 4.5 (session_id FK) are each their own Alembic migration, applied in order after the baseline.
3. Existing dev environments: run `alembic stamp <baseline-rev>` to mark the current schema, then `alembic upgrade head` to apply fixes 4.3–4.5.
4. Fresh installs: `02-create-memory-db.sql` creates the database and extensions only (no tables). Alembic `upgrade head` creates all tables in their final state.
5. Update `02-create-memory-db.sql` to remove table DDL — it becomes database/extension bootstrap only.

### 4.7 SDK Alignment

**Finding:** Memory bus uses FastMCP. Need to verify it's using current patterns and not deprecated APIs.

**Fix:** FastMCP is the high-level API within the `mcp` package (ships as part of `mcp[cli]`). It is not a separate library — it is the SDK. Cove uses the lower-level `mcp.server.Server` class directly. Both are valid API surfaces within the same package.

Decision: Memory Bus stays on FastMCP (it's already working and FastMCP IS the SDK). Cove stays on `mcp.server.Server`. The platform package (`growdirect-mcp`) wraps whichever API surface is appropriate — both are the official SDK. No migration needed here; the consistency requirement is satisfied by both using the `mcp` package.

---

## 5. SDD Updates

SDDs describe what exists. They update after the code changes.

### New

| Document | Purpose |
|----------|---------|
| `docs/decisions/2026-03-30-mcp-sdk-platform-standard.md` | ADR: official `mcp` Python SDK is the platform standard for all MCP servers |

### Rewrite

| SDD | Reason |
|-----|--------|
| `docs/sdds/alx/mcp-service-layer.md` | No longer documents Canary's custom framework. Now documents the platform MCP SDK package at `services/growdirect-mcp/`, the stdio bridge, and the SDK-first standard. Section 11: Canary retrofit deferred (separate spec), `ops` ghost prefix remains as Canary tech debt |

### Update

| SDD | Sections Affected |
|-----|-------------------|
| `docs/sdds/platform/memory-bus.md` | S2 (dual-codebase boundary clarified), S3 (seed_embeddings dropped, HNSW index added, session_id FK), S7 (auth added), S9 (new tests replace misplaced ones), S11 (all findings resolved with cross-reference to Cove knowledge MCP boundary) |
| `docs/sdds/cove/archive-system.md` | Minor — update if Cove MCP registration changes affect knowledge chunk ingestion paths |
| `docs/sdds/platform/shared-infrastructure.md` | S4 — add port allocation for any new platform services if applicable |

### Reclassify

| SDD | From | To | Reason |
|-----|------|----|--------|
| `docs/sdds/alx/qa-agent.md` | `docs/sdds/alx/` | `docs/sdds/canary/qa-agent.md` | App-level test runner, not ALX |

### Don't Touch

- Canary SDDs (tsp, fox, chirp, owl, identity, metrics) — no code changes
- Platform SDDs (factory-pipeline) — unaffected
- Cove SDDs (governance, elections, parcels, member-auth) — unaffected
- `docs/sdds/alx/test-lab.md` — unaffected by this spec

---

## 6. Canary Impact

No Canary code changes in this spec beyond removing ALX entries from server maps.

| Impact | Detail | Severity |
|--------|--------|----------|
| Stdio bridge extracted | `streamable_server.py` functionality moves to platform. IDE integration for Canary tools breaks until Canary retrofit. | Temporary — Canary retrofit is next spec |
| `standalone.py` obsoleted | SDK native transports replace the custom Flask standalone factory. Stays as dead code. | None — not actively used |
| ALX entries removed | `SERVER_PREFIXES` and `SERVER_BLUEPRINTS` lose ALX entries. | Low — partially done (GRO-172) |
| QA Agent untouched | Stays in Canary. SDD moves to `canary/` namespace. | None |
| 12 domain servers untouched | Continue running on custom framework. Tech debt, not broken. | None — retrofit is separate spec |

---

## Success Criteria

**Positive assertions (what exists):**
1. `services/growdirect-mcp/` exists as an installable package wrapping the `mcp` SDK
2. Platform stdio bridge discovers tools from SDK-based servers (Cove, Memory Bus)
3. Cove `server.py` uses `GrowDirectRegistry` instead of hardcoded tool list
4. Memory bus has API key auth, HNSW index, proper FK, Alembic migrations, clean tests
5. Dual-codebase boundary documented in both Memory Bus and Cove SDDs
6. All affected SDDs updated to reflect current architecture
7. QA Agent SDD moved to `docs/sdds/canary/`
8. ADR written at `docs/decisions/2026-03-30-mcp-sdk-platform-standard.md`
9. All changes committed with clean git history

**Negative assertions (what doesn't exist):**
10. `seed_embeddings` table absent from DDL and Alembic head state
11. No imports of `canary.services.alx.memory` in `services/memory-bus/tests/`
12. No `alx` entry in Canary's `SERVER_PREFIXES` or `SERVER_BLUEPRINTS`
13. No Canary domain code changed (12 MCP servers still work on custom framework)

---

## Execution Order

| Phase | Work | Depends On |
|-------|------|------------|
| 1 | Platform MCP package (`services/growdirect-mcp/`) + packaging strategy | Nothing |
| 2 | Memory Bus full sweep (all findings including Alembic) | Phase 1 (SDK alignment check) |
| 3 | Cove MCP polish (import platform package) | Phase 1 (package installable) |
| 4 | ALX extraction (bridge moves to platform, Canary server maps cleaned) | Phase 1 |
| 5 | SDD updates + QA Agent reclassification + ADR | Phases 2–4 |

Phases 2, 3, 4 can run in parallel after Phase 1 completes. Phase 1 must include the packaging/distribution solution (Docker build context changes) since Phases 2 and 3 depend on importing the platform package.
