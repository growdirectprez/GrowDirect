---
classification: confidential
owner: GrowDirect LLC
---

# Memory Bus

> **Status:** Production-grade ops contract
> **Service type:** MCP Server (Platform)
> **Namespace:** platform
> **Last updated:** 2026-04-13
> **Code location (MCP server):** `services/memory-bus/`
> **Code location (platform SDK):** `services/growdirect-mcp/`
> **Code location (DDL):** `devops/init-db/02-create-memory-db.sql`
> **Migrations:** `services/memory-bus/migrations/` (Alembic, 4 revisions)
> **Docker service:** `growdirect_memory_bus` (port 8003)
> **Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/DevOps|DevOps]]

**Wiki:** [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]] · [[Brain/wiki/document-management|Document Management]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Related:** [[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]] · [[docs/sdds/alx/mcp-service-layer|MCP Service Layer]]

---

## Purpose

The Memory Bus is a platform-level MCP server that provides persistent,
semantically-searchable organizational knowledge for all GrowDirect apps and
agents. It stores decisions, architectural findings, session summaries, context
blocks, and team profiles in a shared PostgreSQL database with pgvector
embeddings. Any MCP-compatible client on the Docker network can call its tools
to store and retrieve memories without sharing prompt context between sessions.

**What it is not:** The Memory Bus is not the Cove Knowledge MCP Server
(`Cove/cove/mcp/`). See the boundary table below.

| | Platform Memory Bus (this service) | Cove Knowledge MCP |
|-|-----------------------------------|-------------------|
| Location | `services/memory-bus/` | `Cove/cove/mcp/` |
| Transport | FastMCP streamable-HTTP (port 8003) | MCP stdio |
| Database | `growdirect_memory` | `cove` (`knowledge_chunks` table) |
| Purpose | ALX long-term memory across sessions | Legal/governance RAG for CC&Rs, bylaws |
| Consumers | ALX agent, all builders | Cove AI agent, external MCP clients |

---

## Dependencies

| Dependency | Address | Required | Notes |
|------------|---------|:--------:|-------|
| PostgreSQL 17 | `growdirect_postgres:5432` | Yes | Database `growdirect_memory`, extensions: `vector`, `pgcrypto`, `uuid-ossp` |
| Ollama | `growdirect_ollama:11434` | No | Embedding generation via `/api/embed`. Service degrades gracefully without it. |
| Docker network | `growdirect` | Yes | All inter-service communication flows over this network |
| `growdirect-mcp` SDK | `services/growdirect-mcp/` | Yes | `auth.py` provides `validate_api_key()` for tool dispatch |

**Startup order:** PostgreSQL must be healthy before Memory Bus starts. Ollama
is not required at startup -- if unavailable, memories are stored without
embeddings and retrieved via full-text or ILIKE search.

**Blast radius (if Memory Bus goes down):**
- ALX cannot persist or recall session context -- agent sessions lose long-term
  memory
- Builders lose domain context retrieval -- `domain_context` and
  `context_assemble` tools unavailable
- No impact on Canary, Cove, or Angel application functionality -- they do not
  depend on the Memory Bus at runtime
- No data loss -- all memories persist in PostgreSQL

---

## Data Flow & PII Map

### What enters

| Source | Format | Contains PII? |
|--------|--------|:-------------:|
| ALX agent sessions | MCP tool calls (JSON over HTTP) | No -- architectural decisions, findings |
| Builder agents | MCP tool calls (JSON over HTTP) | No -- domain context queries |
| `seed_clean.py` | Direct SQL inserts | No -- SDDs, team profiles, decisions docs |

### What is stored

| Table | Field | Classification | Encryption | Notes |
|-------|-------|---------------|:----------:|-------|
| `alx_sessions.session_id` | internal | None | Human-readable ID (`alx-<12 hex>`) |
| `alx_sessions.gro_issues` | internal | None | GRO issue identifiers (JSONB array) |
| `alx_sessions.summary` | internal | None | Session summary text |
| `alx_sessions.decisions` | internal | None | Decision strings (JSONB array) |
| `alx_sessions.unresolved` | internal | None | Unresolved items (JSONB array) |
| `alx_memories.content` | internal | None | Memory text -- architectural notes, SDDs, team profiles |
| `alx_memories.metadata` | internal | None | Arbitrary JSONB -- domain, block_type, source_file |
| `alx_memories.embedding` | internal | None | 1024-dim float vector, nullable |
| `alx_memories.layer` | public | None | Scope tag: `corp`, `canary`, `cove`, `shared` |

**PII posture:** No PII is expected or designed to flow through the Memory Bus.
Content consists of architectural decisions, technical findings, session
summaries, and domain context blocks. However, the service accepts arbitrary
text via `memory_store` with no content filtering -- if a caller stores PII
(e.g., team member email in a team profile), it would be stored plaintext
with no field-level encryption. The `layer` column provides logical scoping
but not access control.

**Cove-layer sensitivity:** Memories tagged `layer='cove'` may reference
WPBCA governance data (APN numbers, governance decisions). This is
operationally sensitive but not PII. No access restriction exists beyond the
`layer` filter parameter on recall tools.

### What exits

| Destination | Format | Contains PII? | Notes |
|-------------|--------|:-------------:|-------|
| ALX agent | JSON over HTTP | No | Recalled memories, session context |
| Builder agents | JSON over HTTP | No | Domain context blocks |
| Ollama | HTTP POST to `/api/embed` | No | Raw text sent for embedding (truncated to 6000 chars) |

---

## API Contract

Transport: `streamable-http` | Host: `0.0.0.0` | Port: `8003`
Service name: `GrowDirect Memory Bus`

### MCP Tool Registry

| Tool | Auth Required | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `session_start` | Yes (API key) | None | None | Create ALX session, assemble startup context from recent decisions |
| `session_close` | Yes (API key) | None | None | Close session with summary, decisions, unresolved items |
| `memory_store` | Yes (API key) | None (but accepts arbitrary text) | None | Store memory with embedding, layer tag, type classification |
| `memory_recall` | Yes (API key) | None | None | Semantic search: vector -> full-text -> ILIKE fallback |
| `memory_search` | Yes (API key) | None | None | Structured search by session, type, date, layer |
| `context_assemble` | Yes (API key) | None | None | Multi-source context window for topic or GRO issue |
| `domain_context` | Yes (API key) | None | None | Budget-aware domain context block assembly (11 Canary domains) |

All 7 tools are read-write with no role differentiation. Every tool accepts an
optional `api_key` parameter for authentication. Auth is enforced per-tool via
`validate_api_key()` from the platform SDK.

### Tool: `session_start`

Start a new ALX session. Creates a session record and assembles startup context
from recent decisions and GRO-issue-related memories.

**Parameters:**

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `gro_issues` | `list[str]` | No | `None` | GRO issue identifiers to associate |
| `api_key` | `str` | No | `None` | API key for auth |

**Returns:** `{session_id, status, started_at, gro_issues, startup_context}`

**Behavior:** `startup_context` contains last 5 decisions + up to 3 memories
per GRO issue (ILIKE match). Gives ALX immediate prior context without a
separate `memory_recall` call.

### Tool: `session_close`

Close an active session with a summary and optional decision capture.
Automatically stores summary as a `session_summary` memory.

**Parameters:**

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `session_id` | `str` | Yes | -- | Must match an `active` session |
| `summary` | `str` | Yes | -- | Prose summary of the session |
| `decisions` | `list[str]` | No | `None` | Decisions made during session |
| `unresolved` | `list[str]` | No | `None` | Unresolved items to carry forward |
| `api_key` | `str` | No | `None` | API key for auth |

**Returns:** `{session_id, status, closed_at, summary}`

On error: `{"error": "No active session found: <session_id>"}`

### Tool: `memory_store`

Store a memory with optional embedding, layer tag, and type classification.

**Parameters:**

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `content` | `str` | Yes | -- | Memory text (truncated to 6000 chars for embedding) |
| `memory_type` | `str` | No | `"context"` | Must be one of 10 valid types |
| `session_id` | `str` | No | `None` | Defaults to `"unattached"` |
| `metadata` | `dict` | No | `None` | Arbitrary JSONB metadata |
| `layer` | `str` | No | `"shared"` | `corp`, `canary`, `cove`, or `shared` |
| `api_key` | `str` | No | `None` | API key for auth |

**Returns:** `{memory_id, memory_type, layer, has_embedding, created_at}`

**Valid `memory_type` values:** `decision`, `finding`, `context`,
`architecture`, `session_summary`, `procedure`, `context_block`,
`work_product`, `team_profile`, `foundation`

**Valid `layer` values:** `corp`, `canary`, `cove`, `shared`

### Tool: `memory_recall`

Semantic search with three-tier fallback: vector -> full-text -> ILIKE.

**Parameters:**

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `query` | `str` | Yes | -- | Natural language search query |
| `limit` | `int` | No | `10` | Maximum results |
| `memory_type` | `str` | No | `None` | Filter to specific type |
| `layer` | `str` | No | `None` | Filter by layer. `None` = all layers |
| `api_key` | `str` | No | `None` | API key for auth |

**Returns:** `{query, matches[], count, source}`
where `source` is `"vector"`, `"fulltext"`, or `"ilike"`.

### Tool: `memory_search`

Structured search by session, type, date range, or layer. No semantic
component -- pure relational filtering, ordered by `created_at DESC`.

**Parameters:**

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `session_id` | `str` | No | `None` | Filter to specific session |
| `memory_type` | `str` | No | `None` | Filter to specific type |
| `since` | `str` | No | `None` | ISO datetime -- filters `created_at >= since` |
| `layer` | `str` | No | `None` | Filter by layer |
| `limit` | `int` | No | `20` | Maximum results |
| `api_key` | `str` | No | `None` | API key for auth |

**Returns:** `{memories[], count, filters}`

### Tool: `context_assemble`

Assemble a context window combining semantic recall, recent decisions, and the
last session summary.

**Parameters:**

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `topic` | `str` | No | `None` | Natural language topic for semantic recall |
| `gro_issue` | `str` | No | `None` | GRO issue identifier for targeted recall |
| `limit` | `int` | No | `15` | Maximum memories per semantic query |
| `api_key` | `str` | No | `None` | API key for auth |

**Returns:** `{context, memory_count, topic, gro_issue, sources[]}`

### Tool: `domain_context`

Budget-aware domain context block assembly for Canary service domains.

**Parameters:**

| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `domain` | `str` | Yes | -- | One of 11 valid domains |
| `topic` | `str` | No | `None` | Selects most relevant workflow block |
| `token_budget` | `int` | No | `4000` | Approx token budget (converted to `budget * 4` chars) |
| `api_key` | `str` | No | `None` | API key for auth |

**Valid domains:** `identity`, `tsp`, `chirp`, `alert`, `owl`, `fox`,
`analytics`, `alx`, `raas`, `ops`, `ui_bff`

**Returns:** `{context, domain, topic, blocks_used[], token_estimate}`

---

## Cross-App Data Access

The Memory Bus stores data from all GrowDirect applications in one database.
The `layer` column provides logical isolation:

| Layer | What it holds | Who writes | Who reads |
|-------|--------------|------------|-----------|
| `corp` | Platform SDDs, team profiles, ADRs | `seed_clean.py`, ALX | All agents |
| `canary` | Canary SDDs, Canary-specific findings | `seed_clean.py`, Canary builder | Canary builder, ALX |
| `cove` | Cove SDDs, governance foundations, WPBCA config | `seed_clean.py`, Cove builder | Cove builder, ALX |
| `shared` | Cross-app context, unclassified | ALX, any builder | All agents |

**Isolation model:** Layer filtering is optional and enforced at the application
level only. Any authenticated caller can pass `layer=None` to search across all
layers. There is no database-level row security, no tenant isolation, and no
per-layer access control. A compromised Canary builder could read all Cove
governance memories and vice versa.

**Multi-tenant scope:** Not applicable today (single-tenant platform). If
GrowDirect onboards multiple organizations, the Memory Bus would need a
tenant column and RLS policies.

---

## Tool Dispatch Security

**Authentication model:** API key via `MCP_API_KEY` environment variable.
When set, callers must pass `api_key=<key>` as a tool parameter. The
`validate_api_key()` function in `services/growdirect-mcp/growdirect_mcp/auth.py`
handles validation. When `MCP_AUTH_DISABLED=1` is set, all callers are permitted.

**Current deployment:** `MCP_API_KEY` is set in docker-compose to
`${MCP_API_KEY:-growdirect-memory-dev-key}` -- a default dev key is baked
into the compose file. In production, this must be replaced with a
Secrets Manager value.

**JWT support:** `auth.py` includes a `validate_jwt()` function using HS256,
but no tool in `server.py` calls it. JWT auth is scaffolded but not wired.

**Authorization:** None. All 7 tools are available to any authenticated caller
with no role, scope, or permission differentiation. A valid API key grants
full read-write access to all memories across all layers.

**Privilege escalation:** Not possible within the MCP server itself. The
service has no concept of roles. However, `seed_clean.py --drop-first` deletes
all memories and sessions -- this script runs via `docker exec` with no
additional auth beyond container access.

**Compromise scenario:** If the MCP server is compromised, an attacker gains:
- Read access to all organizational knowledge (decisions, architecture, SDDs)
- Write access to inject false memories (could poison agent context)
- Delete access via `seed_clean.py --drop-first` (requires container exec)
- No access to app databases (Canary, Cove) -- separate databases, separate
  credentials
- No PII exposure (no PII stored by design)

---

## Data Model

Database: `growdirect_memory` (PostgreSQL 17)
Extensions: `vector`, `pgcrypto`, `uuid-ossp`
Test database: `growdirect_memory_test`
Migrations: Alembic (4 revisions -- baseline, drop seed_embeddings, HNSW index,
session FK)

### Table: `alx_sessions`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | Internal row ID |
| `session_id` | `TEXT` | NOT NULL, UNIQUE | Format `alx-<12 hex chars>` |
| `started_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | |
| `closed_at` | `TIMESTAMPTZ` | nullable | Populated on `session_close` |
| `status` | `TEXT` | NOT NULL, DEFAULT `'active'`, CHECK IN (`active`, `closed`, `abandoned`) | |
| `gro_issues` | `JSONB` | DEFAULT `'[]'` | Array of GRO identifiers |
| `summary` | `TEXT` | nullable | Written on close |
| `decisions` | `JSONB` | DEFAULT `'[]'` | Decision strings |
| `unresolved` | `JSONB` | DEFAULT `'[]'` | Carried forward |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | Auto-updated by trigger |

Indexes: `idx_sessions_status`, `idx_sessions_started`

### Table: `alx_memories`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK, DEFAULT `gen_random_uuid()` | |
| `session_id` | `TEXT` | NOT NULL, FK -> `alx_sessions.session_id` | Added in migration 004 |
| `memory_type` | `TEXT` | NOT NULL, CHECK IN (10 valid types) | |
| `content` | `TEXT` | NOT NULL | Up to 6000 chars used for embedding |
| `metadata` | `JSONB` | DEFAULT `'{}'` | domain, block_type, source_file, etc. |
| `embedding` | `vector(1024)` | nullable | NULL when Ollama unavailable at write time |
| `layer` | `TEXT` | NOT NULL, DEFAULT `'shared'`, CHECK IN (`corp`, `canary`, `cove`, `shared`) | |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | Auto-updated by trigger |

Indexes: `idx_memories_session`, `idx_memories_type`, `idx_memories_created`,
`idx_memories_layer`, `idx_alx_memories_embedding_hnsw` (HNSW, vector_cosine_ops)

### Table: `seed_embeddings`

**Status: Dropped.** Migration 002 removes this table. It existed in the
baseline schema but was never queried by `store.py`. This resolves the open
item from the original SDD.

---

## Operations

### Startup sequence

1. `Config()` reads `DATABASE_URL` from env (raises `KeyError` if missing)
2. `MemoryStore(config)` creates SQLAlchemy engine (`pool_size=5`,
   `max_overflow=10`, `pool_pre_ping=True`)
3. `FastMCP("GrowDirect Memory Bus", host="0.0.0.0", port=config.port)`
   registers 7 tools
4. `mcp.run(transport="streamable-http")` starts the HTTP server

No Ollama connectivity check at startup. Ollama failures are handled per-request
in `get_embedding()`.

### Health check

Docker compose health check:
```
curl -so /dev/null -w '%{http_code}' http://localhost:8003/mcp | grep -q '406'
```

This checks that FastMCP is responding (406 = Method Not Allowed on GET, which
confirms the HTTP endpoint is up). The `MemoryStore.healthy()` method exists
(`SELECT 1`) but is not exposed as an MCP tool or HTTP endpoint.

### Failure modes

| Failure | Impact | Recovery | Fails safe? |
|---------|--------|----------|:-----------:|
| PostgreSQL down | All tools return errors | Restart Postgres, Memory Bus reconnects via `pool_pre_ping` | Yes -- errors returned, no data corruption |
| Ollama down | Memories stored without embeddings | Restart Ollama. Memories without embeddings still retrievable via full-text/ILIKE | Yes -- graceful degradation |
| Ollama slow (>120s) | Embedding request times out | `httpx.TimeoutException` caught, memory stored without vector | Yes |
| Memory Bus container crash | Agents lose memory access | Docker `restart: unless-stopped` auto-restarts | Yes -- no in-memory state lost |
| Invalid API key | Tool returns `{"error": "..."}` | Caller must provide correct key | Yes |
| Full disk on Postgres | INSERT failures | Expand volume, clean old data | No -- no data retention policy to auto-purge |

### Monitoring

**Currently implemented:**
- Docker healthcheck (10s interval, 5 retries)
- Python `logging` module warnings for embedding failures

**Not implemented:**
- No metrics endpoint (Prometheus, StatsD)
- No alerting on embedding failure rate
- No query latency tracking
- No memory count dashboards

### Configuration

| Env Var | Required | Default | Notes |
|---------|----------|---------|-------|
| `DATABASE_URL` | Yes | -- | PostgreSQL connection string |
| `OLLAMA_URL` | No | `http://growdirect_ollama:11434` | Ollama API endpoint |
| `EMBEDDING_MODEL` | No | `qwen3-embedding:8b` | Model for `/api/embed` |
| `PORT` | No | `8003` | FastMCP HTTP port |
| `MCP_API_KEY` | No | `""` | API key for tool auth. Empty = auth depends on `MCP_AUTH_DISABLED` |
| `MCP_AUTH_DISABLED` | No | `""` | Set to `"1"` to bypass API key auth |

**Hardcoded constants:**
- `embedding_dimensions = 1024` (Matryoshka target)
- `max_text_length = 6000` (chars truncated before embedding)
- `pool_size = 5`, `max_overflow = 10` (SQLAlchemy connection pool)
- Embedding timeout: `120.0` seconds

---

## Deployment

### Docker service definition

```yaml
memory-bus:
  image: growdirect-memory-bus
  container_name: growdirect_memory_bus
  build:
    context: ../services/memory-bus
    dockerfile: Dockerfile
  environment:
    DATABASE_URL: postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory
    OLLAMA_URL: http://growdirect_ollama:11434
    EMBEDDING_MODEL: qwen3-embedding:8b
    PORT: "8003"
    MCP_API_KEY: ${MCP_API_KEY:-growdirect-memory-dev-key}
  ports:
    - "127.0.0.1:8003:8003"
  depends_on:
    postgres:
      condition: service_healthy
  healthcheck:
    test: ["CMD-SHELL", "curl -so /dev/null -w '%{http_code}' http://localhost:8003/mcp | grep -q '406' || exit 1"]
    interval: 10s
    start_period: 15s
    retries: 5
  restart: unless-stopped
```

Network: `growdirect` (shared across all platform services)

### Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml .
COPY memory_bus/ memory_bus/
RUN pip install --no-cache-dir .
EXPOSE 8003
CMD ["python3", "-m", "memory_bus.server"]
```

Entry point: `python3 -m memory_bus.server` calls
`mcp.run(transport="streamable-http")`.

### AWS target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Memory Bus container | ECS Fargate | Single task, 0.5 vCPU, 1GB memory |
| Database | RDS PostgreSQL 17 | Shared `growdirect_postgres` instance, `growdirect_memory` database |
| Secrets | Secrets Manager | `DATABASE_URL`, `MCP_API_KEY`, `MCP_JWT_SECRET` |
| Ollama | ECS Fargate (GPU) or external | Shared embedding service |
| Networking | VPC private subnet | Memory Bus not internet-facing |

### CI/CD requirements

- Build Docker image on push to `services/memory-bus/`
- Run Alembic migrations before container deployment: `alembic upgrade head`
- Run unit tests (no infra needed): `pytest tests/test_config.py tests/test_embeddings.py`
- Run smoke test against staging: `pytest tests/test_smoke.py`

---

## Runtime dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp[cli]` | `>=1.9.0` | FastMCP server, streamable-HTTP transport |
| `sqlalchemy` | `>=2.0` | Database engine and connection pool |
| `pgvector` | `>=0.3.0` | pgvector SQLAlchemy type handling |
| `psycopg2-binary` | `>=2.9` | PostgreSQL driver |
| `httpx` | `>=0.27` | HTTP client for Ollama API calls |
| `pytest` | `>=8.0` | Test runner (dev) |
| `pytest-asyncio` | `>=0.24` | Async test support (dev) |

---

## Testing

Tests: `services/memory-bus/tests/`

### Unit tests (no infra)

- `test_config.py` -- Config class: env var loading, defaults, missing DATABASE_URL
- `test_embeddings.py` -- Embedding generation: mocked httpx, 1024-dim slicing,
  None on failure, text truncation
- `test_store.py` -- MemoryStore context block retrieval and assembly

### Smoke tests (requires running infra)

- `test_smoke.py` -- Full roundtrip: `session_start` -> `memory_store` ->
  `memory_recall`. Requires `growdirect_memory_test` database and Ollama with
  `qwen3-embedding:8b`.

### Running

```bash
# Unit tests
cd services/memory-bus && python3 -m pytest tests/test_config.py tests/test_embeddings.py -v

# Smoke test
DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory_test \
OLLAMA_URL=http://localhost:11434 \
python3 -m pytest tests/test_smoke.py -v
```

### Seed script

`services/memory-bus/scripts/seed_clean.py` populates `alx_memories` from
platform documents. Idempotent with `--drop-first`, additive without it.

```bash
# Inside Docker
docker exec growdirect_memory_bus python3 scripts/seed_clean.py --drop-first
```

| Source | Memory type | Layer |
|--------|------------|-------|
| `docs/sdds/platform/*.md` | `context_block` | `corp` |
| `docs/sdds/canary/*.md` | `context_block` | `canary` |
| `docs/sdds/cove/*.md` | `context_block` | `cove` |
| `docs/sdds/alx/*.md` | `context_block` | `shared` |
| `docs/team/*.md` | `team_profile` | `corp` |
| `docs/decisions/*.md` | `decision` | `corp` |
| `docs/research/lp-dashboard-pattern-catalog.md` | `foundation` | `canary` |
| `Cove/cove/governance/wpbca-bylaws-config.json` | `foundation` | `cove` |

---

## Error Handling

| Scenario | Behavior | Response |
|----------|----------|----------|
| Invalid `memory_type` | Returns error dict, no exception | `{"error": "Invalid memory_type: ..."}` |
| Invalid `layer` | Returns error dict, no exception | `{"error": "Invalid layer: ..."}` |
| Invalid `domain` | Returns error dict, no exception | `{"error": "Unknown domain: ..."}` |
| Session not found on close | Returns error dict | `{"error": "No active session found: ..."}` |
| Session not found on store | Returns error dict (migration 004 FK) | `{"error": "Session '...' does not exist"}` |
| Ollama unreachable | `get_embedding()` returns None, logs warning | Memory stored without embedding, `has_embedding: false` |
| Ollama timeout (>120s) | `httpx.TimeoutException` caught | Same as unreachable |
| Database down | Exception propagates to MCP client | MCP-level error |
| Auth failure | Returns error dict | `{"error": "API key required ..."}` or `{"error": "Invalid API key"}` |
| Unhandled exception in tool | Propagates as MCP-level error | No custom error middleware |

---

## Code Review Findings

### P0 -- Blocks Production

**P0-1: Default API key in docker-compose is a hardcoded credential.**
The compose file sets `MCP_API_KEY: ${MCP_API_KEY:-growdirect-memory-dev-key}`.
If the env var is not overridden in production, the service runs with a
well-known key. Any client knowing this string has full read-write access.
**Fix:** Remove the default value. Require `MCP_API_KEY` to be set explicitly
in production via AWS Secrets Manager. Fail startup if missing in non-dev
environments.
**Linear:** TBD

**P0-2: API key passed as a tool parameter, not HTTP header.**
Every tool accepts `api_key` as an MCP tool parameter. This means the API key
appears in MCP request logs, tool call traces, and potentially in agent
conversation history. The `auth.py` module supports header-based auth
(`X-API-Key`), but `server.py` does not read HTTP headers -- it extracts the
key from the tool's own arguments.
**Fix:** Move auth to HTTP middleware (FastMCP supports request hooks). Remove
`api_key` parameter from all tool signatures. Validate via `X-API-Key` header
or MCP protocol auth.
**Linear:** TBD

**P0-3: No content sanitization on `memory_store`.**
The `content` parameter accepts arbitrary text up to 6000 chars. If a caller
stores PII (email, phone, name) or sensitive data, it is persisted in
plaintext with no encryption, no redaction, and no audit trail. While the
design intent excludes PII, there is no enforcement.
**Fix:** Add a content classification check before storage. At minimum, log
warnings if content matches PII patterns (email regex, phone patterns). For
production with external customers, implement content filtering or require
callers to declare PII status.
**Linear:** TBD

### P1 -- Before GA

**P1-1: No audit trail for memory writes or deletes.**
There is no audit log for who stored, modified, or deleted memories. The
`seed_clean.py --drop-first` operation deletes all memories with no record of
what was removed or who initiated it. Session close records are the only
breadcrumb.
**Fix:** Add an `audit_log` table with columns: `action` (store/delete/seed),
`actor` (API key hash or caller ID), `target_id`, `timestamp`. Log every
`memory_store` and every seed script invocation.
**Linear:** TBD

**P1-2: No data retention policy.**
Memories accumulate indefinitely. There is no TTL, no archival process, and no
mechanism to purge old memories. As the platform grows, the `alx_memories`
table will grow unbounded, degrading query performance.
**Fix:** Implement retention policy: auto-archive memories older than 12 months
(move to archive table or add `archived_at` column). Exclude archived memories
from default queries. Add `seed_clean.py --purge-before <date>` flag.
**Linear:** TBD

**P1-3: No rate limiting on MCP tools.**
All 7 tools can be called unlimited times with no throttling. A misconfigured
agent loop could flood the database with duplicate memories or overload Ollama
with embedding requests.
**Fix:** Add rate limiting at the FastMCP level (request/minute per API key).
Alternatively, implement deduplication in `memory_store` -- check for content
hash before inserting.
**Linear:** TBD

**P1-4: `healthy()` method not exposed.**
`MemoryStore.healthy()` exists and checks database connectivity with
`SELECT 1`, but it is not registered as an MCP tool and not exposed as an
HTTP endpoint. The Docker healthcheck works around this by checking for a
406 response from the MCP endpoint.
**Fix:** Register `healthy` as an MCP tool or expose `/health` as a plain
HTTP endpoint that calls `store.healthy()` and checks Ollama connectivity.
**Linear:** TBD

**P1-5: SQL injection surface in ILIKE queries.**
The `_assemble_startup_context` method interpolates GRO issue identifiers
directly into ILIKE patterns: `f"%{gro}%"`. While these values come from
the caller's `gro_issues` parameter (not user-facing input), they are passed
as parameterized queries via SQLAlchemy `text()` bindings, which mitigates
SQL injection. However, the ILIKE pattern itself is not escaped for special
characters (`%`, `_`). A GRO issue containing `%` would match more broadly
than intended.
**Fix:** Escape ILIKE special characters in query parameters.
**Linear:** TBD

### P2 -- Post-Launch

**P2-1: No key rotation mechanism.**
The `MCP_API_KEY` is a single static key. Rotating it requires restarting the
container with a new env var. No grace period, no dual-key support.
**Fix:** Support comma-separated keys in `MCP_API_KEY` (any valid key
accepted). Document rotation procedure.
**Linear:** TBD

**P2-2: JWT auth scaffolded but not wired.**
`auth.py` includes `validate_jwt()` with HS256 support, but no tool calls it.
The `MCP_JWT_SECRET` env var is documented in auth.py but not in any compose
file or deployment docs.
**Fix:** Either wire JWT auth into FastMCP middleware as an alternative to API
key, or remove the dead code to avoid confusion.
**Linear:** TBD

**P2-3: No monitoring or metrics.**
No Prometheus endpoint, no StatsD counters, no query latency tracking. The
only observability is Docker healthchecks and Python logging.
**Fix:** Add a `/metrics` endpoint with counters for: tool calls by name,
embedding failures, recall tier usage (vector/fulltext/ilike), memory count
by layer.
**Linear:** TBD

**P2-4: Connection pool not configurable.**
`pool_size=5` and `max_overflow=10` are hardcoded in `store.py`. These cannot
be tuned via environment variables.
**Fix:** Add `DB_POOL_SIZE` and `DB_MAX_OVERFLOW` env vars to `Config`.
**Linear:** TBD

**P2-5: Embedding timeout at 120s is aggressive for cold-start Ollama.**
The `httpx.post()` timeout is 120 seconds. Ollama cold-starts (loading model
into VRAM) can exceed this. The original SDD documented 30s -- code now uses
120s, which is better but may still be tight for GPU memory pressure.
**Fix:** Make timeout configurable via `EMBEDDING_TIMEOUT` env var. Add
retry logic (1 retry with exponential backoff).
**Linear:** TBD

**P2-6: `seed_clean.py` bypasses MCP auth and session FK enforcement.**
The seed script writes directly to the database via SQLAlchemy, bypassing all
MCP-layer auth. It also creates its own `seed-clean` session to satisfy the
FK constraint. This is by design for bulk operations, but it means the auth
layer can be completely circumvented by anyone with `docker exec` access.
**Fix:** Document this as an operational risk. In production, restrict
`docker exec` access via IAM policies on ECS tasks.
**Linear:** TBD

---

## Production Readiness Checklist

- [ ] PII encrypted at rest -- N/A by design (no PII stored), but no enforcement mechanism prevents PII from being stored plaintext (P0-3)
- [ ] Secrets in AWS Secrets Manager (not .env) -- Not implemented. `DATABASE_URL` and `MCP_API_KEY` in docker-compose env (P0-1)
- [ ] Health check endpoint responds -- Partial. Docker healthcheck works via 406 response, but no dedicated health endpoint (P1-4)
- [ ] Audit logging for sensitive operations -- Not implemented. No audit trail for memory writes or deletes (P1-1)
- [ ] Data retention policy implemented -- Not implemented. Memories accumulate indefinitely (P1-2)
- [ ] Rate limiting on public endpoints -- Not implemented. No rate limiting on any tool (P1-3)
- [ ] Error responses don't leak internals -- Partial. Error messages include valid type/layer lists (acceptable for dev, review for prod)
- [ ] API key not hardcoded in compose -- Fails. Default dev key in compose (P0-1)
- [ ] Auth enforced at transport level, not tool parameter level -- Fails. API key passed as tool argument (P0-2)
- [ ] Cross-app data isolation enforced -- Partial. Layer column exists but is advisory, not enforced (see Cross-App Data Access)
- [ ] Monitoring and alerting -- Not implemented (P2-3)
- [ ] Key rotation documented -- Not implemented (P2-1)

---

## Migration History

| Revision | Date | Description |
|----------|------|-------------|
| `001_baseline` | 2026-03-30 | Capture existing DDL: `alx_sessions`, `alx_memories`, `seed_embeddings` |
| `002_drop_seed_embeddings` | 2026-03-30 | Drop unused `seed_embeddings` table |
| `003_hnsw_index` | 2026-03-30 | Add HNSW index on `alx_memories.embedding` |
| `004_session_fk` | 2026-03-30 | Backfill orphan sessions, add FK constraint `alx_memories.session_id -> alx_sessions.session_id` |

---

## Reconciliation Notes (GRO-379)

All issues from the MCP consolidation audit have been addressed:

- **Dual-codebase architecture** -- Boundary documented in Purpose section
- **Misplaced test files** -- Rewritten to test `memory_bus.store` directly
- **No authentication** -- `MCP_API_KEY` env var supported (see P0-1, P0-2 for remaining gaps)
- **No HNSW index** -- Added in migration 003
- **`session_id` soft FK** -- Hardened in migration 004 (FK constraint added, orphan sessions backfilled)
- **`seed_embeddings` unused** -- Dropped in migration 002
- **Cove MCP stdio transport** -- Documented in Purpose boundary table (no code change needed)
