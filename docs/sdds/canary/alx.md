# ALX

## Overview

The ALX domain owns institutional memory for the Canary LP platform. It is a pgvector-powered knowledge store that persists decisions, architectural patterns, findings, and operational context across agent sessions. ALX is what makes the agent more than a stateless assistant — it remembers what was decided, why, and what remains unresolved.

**Core architecture:** PostgreSQL-only with pgvector embeddings. Two-tier search: semantic first (pgvector cosine similarity on 768-dim nomic-embed-text vectors), full-text fallback (PostgreSQL `to_tsvector/plainto_tsquery`), then ILIKE as a last resort. Embedding is inline on write — `memory_store()` generates and persists the vector immediately via Ollama `/api/embed`. No batch lag. Separate database (`growdirect_memory`) from the three main schemas, served by memory bus MCP server on port 8003 (GRO-172).

**Memory types:** `decision`, `finding`, `context`, `architecture`, `work_product`, `team_profile`, `context_block`, `foundation`, `session_summary`, `procedure`. Context blocks (SDD-058) are pre-assembled domain-coherent chunks stored as `memory_type = 'context_block'` with structured metadata for targeted retrieval.

**Five narratives classification:** Every memory maps to one of five narratives — founder (team lineage, consulting history), retail_process (LP methodology), retail_systems (POS/EHR/IoT), platform (Canary retail offer, heartbeat, RaaS), tech_stack (agentic development, SDD factory).

**Blueprints:**

| Blueprint | Prefix | Purpose |
|-----------|--------|---------|
| `alx_api` | `/alx` | MCP tool server (7 tools), health check |

**MCP tools (canary-alx server, 7 tools):** `memory_store`, `memory_recall`, `memory_search`, `session_start`, `session_close`, `context_assemble`, `domain_context`. Three categories: memory (store/recall/search), session (start/close), context (assemble/domain_context).

**Code entry points:**
- `canary/services/alx/memory.py` — core service: store, recall, semantic search, session lifecycle, context block retrieval, domain context assembly
- `canary/services/alx/tools.py` — MCP tool definitions, MCPRegistry, handlers
- `canary/blueprints/alx_api.py` — Flask blueprint via `create_mcp_blueprint` factory
- `devops/scripts/embed_memories_batch.py` — batch re-embedding script
- `devops/scripts/seed_context_blocks.py` — seed 33 domain context blocks from SDDs + OpenAPI spec

**Inbound contracts:**
- Any agent calls MCP tools via `POST /alx/tools/<name>` (X-API-Key or JWT auth).
- Owl reads institutional knowledge via `memory_semantic_search()` through `build_institutional_context()` (SDD-061).

**Outbound contracts:**
- Owl prompt injection — institutional knowledge flows one-way into Owl's prompt assembly as Window 0 (~2000 token budget).
- Ollama `/api/embed` — nomic-embed-text for embedding generation on every `memory_store()` call.

## API Contracts

### MCP Endpoints (`/alx`)

Standard MCP protocol endpoints stamped by `create_mcp_blueprint`: `/alx/manifest`, `/alx/tools`, `/alx/tools/<name>`, `/alx/health`. Rate limiting is exempted for all ALX endpoints (internal agent-to-agent use).

| Path | Method | Auth | Description |
|------|--------|------|-------------|
| `/alx/manifest` | GET | Public | MCP server manifest (name: `canary-alx`, version: `0.1.0`) |
| `/alx/tools` | GET | Public | List all 7 tools in MCP format |
| `/alx/tools/<name>` | POST | JWT / X-API-Key | Invoke tool. Body: `{"params": {...}, "context": {...}}` |
| `/alx/health` | GET | Public | Health check: database connectivity + tool count |

### MCP Tool Contracts

| Tool | Category | Required Params | Optional Params | Returns |
|------|----------|----------------|-----------------|---------|
| `memory_store` | memory | `content` | `memory_type`, `session_id`, `gro_issue`, `metadata` | `{memory_id, session_id, memory_type, stored, embedded}` |
| `memory_recall` | memory | `query` | `limit` (default 10), `memory_type` | `{query, matches[], count, source}` |
| `memory_search` | memory | (none) | `session_id`, `memory_type`, `since`, `limit` (default 20) | `{matches[], count, filters}` |
| `session_start` | session | (none) | `gro_issues[]` | `{session_id, status, gro_issues, context, started_at}` |
| `session_close` | session | `session_id`, `summary` | `decisions[]`, `unresolved[]` | `{session_id, status, summary_stored, decisions_count, unresolved_count, closed_at}` |
| `context_assemble` | context | (none) | `topic`, `gro_issue`, `limit` (default 15) | `{context, memory_count, topic, gro_issue, sources[]}` |
| `domain_context` | context | `domain` | `topic`, `token_budget` (default 4000) | `{context, domain, topic, blocks_used[], token_estimate}` |

### Response Envelope

All tool invocations return: `{"tool": "<name>", "ok": true, "result": {...}, "timestamp": "ISO8601"}`. On failure: `ok: false`, `error: "..."`, HTTP 500.

### Health Response

`{"service": "canary-alx", "healthy": <bool>, "database": "connected"|"unavailable", "tools": 7}`. Health is true if Tier 1 (database) is reachable. HTTP 503 if database is down.

### MCP Stdio Bridge (SDD-065)

IDE agents (Claude Code, Cursor) connect via `streamable_server.py` which translates MCP stdio calls into authenticated HTTP requests. The bridge runs in a dedicated `.venv-mcp/` virtualenv (Python 3.11 + `mcp`, `requests`, `python-dotenv`). Auth uses `X-API-Key` header loaded from `.env` — survives the stub-to-Keycloak transition. IDE config in `.mcp.json`: `{"command": ".venv-mcp/bin/python3", "args": ["canary/mcp/streamable_server.py", "--server", "alx", "--api-key-env", "CANARY_MCP_API_KEY"]}`.

## Data Model

All ALX tables live in the `growdirect_memory` database (separate from `canary` which holds the `app`, `sales`, and `metrics` schemas). Tables use raw SQL via `sqlalchemy.text()` — no ORM models, no `Mapped[]` declarations. Dedicated engine with `pool_size=5`, `max_overflow=2`, `pool_pre_ping=True`, `pool_recycle=300`. Note: as of GRO-172, the memory bus is served by a standalone MCP server on port 8003.

### alx_memories

Primary knowledge store. Each row is one memory with optional pgvector embedding.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | `uuid4` generated on insert |
| session_id | VARCHAR | FK to `alx_sessions.session_id` |
| memory_type | VARCHAR | decision, finding, context, architecture, work_product, team_profile, context_block, foundation, session_summary, procedure |
| content | TEXT | Full text content |
| metadata | JSONB | Tags, source agent, GRO issue, block_type, domain, sdd_refs |
| embedding | vector(768) | nomic-embed-text via Ollama `/api/embed` |
| created_at | TIMESTAMP | Auto-set, used for ordering |

**Vector index:** HNSW with cosine distance operator (`<=>`). The `<=>` operator returns cosine distance (0 = identical, 2 = opposite); similarity is computed as `1 - distance`.

**Embedding pipeline:** Inline on write via `_get_embedding()` which calls Ollama `/api/embed` with 4000-char truncation. Returns 768-dim float vector serialized as a bracket-delimited string for SQL insertion. Batch re-embedding via `devops/scripts/embed_memories_batch.py`.

**Semantic search SQL pattern:**
```sql
SELECT id, content, memory_type, metadata, created_at,
       1 - (embedding <=> CAST(:qvec AS vector)) AS similarity
FROM alx_memories
WHERE embedding IS NOT NULL
  AND (embedding <=> CAST(:qvec AS vector)) < :threshold
  [AND memory_type = :mtype]
ORDER BY embedding <=> CAST(:qvec AS vector)
LIMIT :lim
```

Note: `CAST(:qvec AS vector)` is used instead of `::vector` because SQLAlchemy interprets `::` as a parameter binding delimiter.

**Default threshold:** 0.62 cosine distance (nomic-embed-text produces distances ~0.45-0.60 for relevant SDD content).

### alx_sessions

Session lifecycle tracking. One row per agent session.

| Column | Type | Notes |
|--------|------|-------|
| id | SERIAL PK | Auto-increment |
| session_id | VARCHAR UNIQUE | Format: `alx-YYYYMMDD-HHMMSS-{6 hex chars}` |
| status | VARCHAR | `active` or `closed` |
| gro_issues | JSONB | Array of GRO issue numbers |
| summary | TEXT | Written on close |
| decisions | JSONB | Array of decision strings |
| unresolved | JSONB | Array of unresolved items |
| closed_at | TIMESTAMP | Set on close |
| created_at | TIMESTAMP | Auto-set |

### Context Block Metadata (SDD-058)

Context blocks are stored as regular `alx_memories` rows with `memory_type = 'context_block'` and structured JSONB metadata: `block_type` (domain_overview | workflow | data_model | api_contract), `domain` (primary), `domains[]` (all involved, for workflows), `sdd_refs[]`, `api_paths[]`, `code_entry_points[]`, `mcp_server`, `mcp_tools[]`, `tables[]`, `database`, `token_estimate`. 33 blocks total: 11 domain overview (~1200 tokens each), 7 workflow (~2000 tokens), 4 data model (~1500 tokens), 11 API contract (~1200 tokens).

## Workflows

### Session Lifecycle

The session lifecycle provides continuity across agent conversations. Each session records what was done, what was decided, and what remains open.

**Start:** `session_start(gro_issues=[])` creates a new session record (status=active) and assembles startup context. Context assembly pulls: last 3 session summaries (truncated to 200 chars each), last 5 decisions, and up to 5 memories per specified GRO issue. Returns structured markdown under `## ALX Session Context`.

**Active phase:** During the session, `memory_store()` persists decisions, findings, and context. Each write generates an inline embedding via Ollama and stores both text + vector. If Ollama is unreachable, the memory stores without embedding (best-effort).

**Close:** `session_close(session_id, summary, decisions[], unresolved[])` updates the session record to `closed`, then stores the summary as a `session_summary` memory. The next `session_start` will recall this summary as recent context.

Session ID format: `alx-YYYYMMDD-HHMMSS-{6 hex chars}` (e.g., `alx-20260314-153022-a7c3f1`).

### Memory Store (Write Path)

1. MCP client calls `POST /alx/tools/memory_store` with content and optional metadata.
2. Tool handler validates content is non-empty, extracts session_id from params or context.
3. `memory_store()` generates embedding via `_get_embedding()` (Ollama `/api/embed`, 4000-char truncation, 768-dim vector).
4. INSERT into `alx_memories` with id, session_id, memory_type, content, metadata, embedding.
5. Returns `{memory_id, stored: true, embedded: true/false}`.

Embedding failure is non-blocking — the memory stores with `embedding = NULL` and can be batch-embedded later.

### Memory Recall (Read Path)

1. MCP client calls `POST /alx/tools/memory_recall` with natural language query.
2. **Tier 1 (semantic):** `memory_semantic_search()` embeds the query via Ollama, runs pgvector cosine similarity search with threshold 0.62. Returns ranked results with similarity scores.
3. **Tier 2 (full-text):** If semantic search fails or returns empty, falls through to PostgreSQL `to_tsvector('english', content) @@ plainto_tsquery('english', :query)` with `ts_rank` ordering.
4. **Tier 3 (ILIKE):** If full-text returns zero results (common for short or unusual queries), falls back to `content ILIKE '%query%'` ordered by `created_at DESC`.
5. Returns `{query, matches[], count, source: "pgvector"|"postgresql"|"error"}`.

### Context Assembly

`context_assemble(topic, gro_issue)` builds a system prompt block from multiple memory sources:
1. If gro_issue specified: `memory_recall(gro_issue, limit=15)` for issue-specific memories.
2. If topic specified (and different from gro_issue): `memory_recall(topic, limit=15)`.
3. Always: `memory_search(type="decision", limit=5)` for recent decisions.
4. Always: `memory_search(type="session_summary", limit=1)` for last session.
5. Deduplicate by `memory_id`.
6. Format as structured markdown: `## ALX Memory Context` with sections for Last Session, Recent Decisions, Related Context.

### Domain Context Retrieval (SDD-058)

`domain_context(domain, topic, token_budget)` assembles a complete context window for one of 11 service domains. Budget: ~4000 tokens (~16,000 chars).

Assembly order with budget management:
1. **Domain Overview** (~1200 tokens) — always included. Retrieves via `recall_context_blocks(domain, "domain_overview")`.
2. **API Contract** (~1200 tokens) — always included.
3. **Workflow** (~2000 tokens) — included if topic specified. Best-match selected by keyword overlap scoring. Truncated if over budget.
4. **Data Model** — included if space permits (>400 chars remaining). Truncated to fit.

Valid domains: identity, tsp, chirp, alert, owl, fox, analytics, alx, raas, ops, ui_bff.

Context block retrieval queries `alx_memories WHERE memory_type = 'context_block'` with domain matching via direct metadata match (`metadata->>'domain' = :domain`) or JSONB array containment (`metadata->'domains' @> :domain_jsonb`) for workflow blocks that span multiple domains.

### Institutional Knowledge Flow (SDD-061)

ALX memory feeds Owl's prompt assembly via a one-way read path. Owl never writes to ALX.

1. Owl chat or health-check calls `build_institutional_context(personality, query, token_budget=2000)`.
2. Adapter looks up JPT lens affinity: jpt_detection gets LP patterns (chirp, alert, fox), jpt_operations gets process/ops (tsp, ops, analytics, raas), jpt_analytics gets all domains including foundation materials.
3. `memory_semantic_search(query, limit=8)` returns ranked results from pgvector.
4. Results filtered by personality-allowed `memory_type` values, formatted under 2000-token budget.
5. Injected into Owl system prompt as Window 0 (before merchant-specific Windows 1-3).

This is strictly best-effort. If ALX is unreachable, `build_institutional_context()` returns empty string and Owl continues without institutional context.

### Error Handling

All database operations wrap in try/except with `session.rollback()` on failure. `memory_recall()` returns `{source: "error", error: str(e)}` on query failure. `memory_store()` raises on DB failure (caller handles). `memory_search()` returns `{matches: [], count: 0, error: str(e)}`. Session start/close raise exceptions on DB failure. Health endpoint returns 503 when database is unreachable, 200 otherwise. Embedding failure is silent — memory stores without vector, search falls back to full-text.
