# GRO-172 — Platform Memory Bus Design

**Date:** 2026-03-30
**Status:** Approved
**Issue:** [GRO-172](https://linear.app/growdirect/issue/GRO-172)

## Problem

ALX ops memory (2,000+ organizational memories) lives inside the Canary codebase at `canary/services/alx/memory.py` and connects to `canary_memory`. This creates two problems:

1. Canary can't ship clean — ops memory either ships to production or must be manually excluded
2. Ops memory is locked to Canary — Cove, Cowork, and future apps can't query organizational knowledge without reaching into Canary's internals

## Decision

Extract ops memory into a standalone MCP server using the official MCP Python SDK (`FastMCP`). This becomes the reference implementation for "how we build MCP servers going forward" — Canary's existing Flask-based MCP framework stays as-is and gets retrofitted later.

## Architecture

Standalone Python service at `~/GrowDirect/services/memory-bus/`. Two transports:

- **stdio** — Claude Code local use
- **Streamable HTTP** (port 8003) — container/remote access (Cowork, future apps)

SSE is deprecated in the MCP spec; we skip it entirely and go straight to Streamable HTTP.

The service extracts business logic from `canary/services/alx/memory.py`. Core functions become `@mcp.tool()` decorated functions. The underlying PostgreSQL + pgvector search, Ollama embedding generation, and dual-table lookup (alx_memories + seed_embeddings) carry over unchanged.

### Three Knowledge Layers (unchanged)

| Layer | Database | Ships to Prod? | Audience | This Issue? |
|-------|----------|----------------|----------|-------------|
| ALX Ops Memory | `growdirect_memory` | NO | Cowork, builders, ALX | YES |
| Owl Product Knowledge | `canary` DB (`knowledge_chunks`) | YES | Merchants, QA agent | NO |
| Cove Domain Knowledge | `cove` DB (future) | YES | Members, archive search | NO |

## Service Structure

```
~/GrowDirect/services/memory-bus/
├── pyproject.toml              # Dependencies: mcp, sqlalchemy, pgvector, httpx
├── Dockerfile
├── memory_bus/
│   ├── __init__.py
│   ├── server.py               # FastMCP server, tool declarations
│   ├── store.py                # DB operations (from memory.py)
│   ├── embeddings.py           # Ollama embedding generation
│   └── config.py               # Environment-based config
└── scripts/
    ├── seed_context_blocks.py
    ├── seed_memory_foundation.py
    ├── seed_team_profiles.py
    ├── seed_sdds_v2.py
    ├── seed_work_products.py
    ├── embed_memories_batch.py
    ├── load_memories.py
    ├── ingest_tier2_batch.py
    └── field_registry_seed.py
```

## MCP Tools (7)

| Tool | Purpose |
|------|---------|
| `memory_store` | Persist memory with embedding, layer tag, type |
| `memory_recall` | Semantic search (pgvector → full-text → ILIKE fallback) |
| `memory_search` | Structured filter by session/type/date |
| `context_assemble` | Build context window for topic/GRO issue |
| `session_start` | Create session, assemble startup context |
| `session_close` | Close session, store summary/decisions |
| `domain_context` | Full domain context assembly with token budget |

New field on `alx_memories`: `layer` (enum: `corp`, `canary`, `cove`, `shared`) for scoped retrieval. Defaults to `shared`.

### Internal functions (not MCP tools)

These functions from `memory.py` become internal to `store.py` — not exposed as MCP tools:

| Function | Disposition |
|----------|-------------|
| `memory_semantic_search` | Internal to `store.py`. Used by `memory_recall` internally. If Canary's `institutional.py` needs it, it calls `memory_recall` via MCP. |
| `recall_context_blocks` | Internal to `store.py`. Used by `context_assemble` and `domain_context` internally. |
| `memory_healthy` | Exposed as the service health check endpoint, not as an MCP tool. |

### Canary `institutional.py` latency consideration

`institutional.py` currently imports `memory_semantic_search` directly for Owl/JPT prompts — a hot path on every merchant-facing chat. Moving to MCP adds a network round-trip. Mitigation options (decided during assembly):

1. **Acceptable latency** — memory bus is on the same Docker network, round-trip is <5ms
2. **Cache at Canary** — cache institutional context in Valkey with TTL, only hit memory bus on cache miss
3. **Keep direct DB query** — `institutional.py` queries `growdirect_memory` directly via SQLAlchemy without going through MCP (no code dependency on memory bus, just a DB connection)

Option 1 is the starting point. If latency is measurable in testing, fall back to option 2.

## Container Config

Added to `~/GrowDirect/devops/docker-compose.yml`:

```yaml
memory-bus:
  image: growdirect-memory-bus
  build:
    context: ../services/memory-bus
    dockerfile: Dockerfile
  container_name: growdirect_memory_bus
  ports:
    - "8003:8003"
  environment:
    - DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory
    - OLLAMA_URL=http://growdirect_ollama:11434
    - EMBEDDING_MODEL=qwen3-embedding:8b
  networks:
    - growdirect
  depends_on:
    postgres:
      condition: service_healthy
    ollama:
      condition: service_healthy
  healthcheck:
    test: ["CMD", "python", "-c", "import httpx; httpx.get('http://localhost:8003/health').raise_for_status()"]
    interval: 30s
    timeout: 10s
    retries: 3
```

## Database Migration

### Rename

- One-time migration script: `ALTER DATABASE canary_memory RENAME TO growdirect_memory`
- `devops/init-db/01-create-databases.sql` updated: `CREATE DATABASE canary_memory` → `CREATE DATABASE growdirect_memory`. Memory table DDL removed from this file — it only creates the database and enables extensions.
- `02-create-memory-db.sql` becomes the single canonical DDL source for all `growdirect_memory` tables. Moves from `Canary/devops/init-db/` to `GrowDirect/devops/init-db/`.
- New test DB `growdirect_memory_test` added to init script.

### Schema fixes during extraction

**`memory_type` CHECK constraint:** The current constraint only allows `decision`, `finding`, `context`, `architecture`, `session_summary`, `procedure` — but the codebase actively stores `context_block`, `work_product`, `team_profile`, and `foundation`. Update the CHECK constraint to include all actively-used types.

**`layer` column:** Add to `alx_memories` table:
```sql
ALTER TABLE alx_memories ADD COLUMN layer TEXT NOT NULL DEFAULT 'shared'
    CHECK (layer IN ('corp', 'canary', 'cove', 'shared'));
CREATE INDEX idx_alx_memories_layer ON alx_memories(layer);
```
Backfill: all existing records get `layer = 'shared'` (the default). Layer-specific tagging happens going forward as memories are stored with explicit layer values.

`seed_embeddings` does not get a `layer` column — seed data is curated platform knowledge and is always `shared`.

**`updated_at` column:** Add `updated_at TIMESTAMPTZ DEFAULT NOW()` to both `alx_memories` and `seed_embeddings` to comply with platform standards. Add trigger to auto-update on row modification.

### Environment variables

Current Canary env vars that change:
- `CANARY_MEMORY_DB_URL` — removed from Canary `.env` and `docker-compose.yml`. Memory bus uses `DATABASE_URL` instead.
- `OWL_URL` — renamed to `OLLAMA_URL` in memory bus config. Canary keeps `OWL_URL` for its own Ollama usage (Owl product knowledge).

## Canary Cleanup

**Deleted:**
- `canary/services/alx/memory.py`
- `canary/services/alx/tools.py`
- `canary/blueprints/alx_api.py`
- `Canary/devops/init-db/02-create-memory-db.sql`

**Moved to `services/memory-bus/scripts/`:**
- `seed_context_blocks.py`, `seed_memory_foundation.py`, `seed_work_products.py`, `seed_team_profiles.py`, `seed_sdds_v2.py`, `embed_memories_batch.py`, `load_memories.py`, `ingest_tier2_batch.py`, `field_registry_seed.py`

**Dropped (stale or superseded):**
- `enrich_cognee_batch.py` — Cognee integration was removed (GRO-198)
- `embed_seeds.py` — superseded by `embed_memories_batch.py`
- `refine_tier1_memories.py` — one-time refinement, already applied
- `sync_vault_to_pgvector.py` — Obsidian sync, superseded by memory bus MCP

**Updated imports:**
- `canary/services/owl/institutional.py` — calls memory bus via MCP client instead of direct import
- Test files (`test_rag_retrieval.py`, `test_context_blocks.py`, `test_owl_api_sessions.py`) — updated or moved

**Not touched:**
- Owl's `knowledge_chunks` table in the `canary` DB
- Owl semantic search over CRDM data
- `canary/mcp/` base kit (retrofitted separately, future GRO)

## Error Handling

- Ollama unavailable: memories store with `embedding=NULL`, recall falls back to full-text → ILIKE (same as current)
- Postgres unavailable: tools return error dict, preflight catches this before sessions start
- No retry logic in MCP layer — SDK handles transport-level retries

## Testing

- Unit tests for `store.py` and `embeddings.py` against `growdirect_memory_test`
- Integration tests for MCP tool round-trips using SDK's test client
- Smoke test: `memory_store` → `memory_recall` returns stored content

## Acceptance Criteria

- [ ] `growdirect_memory` DB exists, data migrated from `canary_memory`
- [ ] Memory bus MCP server runs as container on growdirect network, port 8003
- [ ] `memory_recall("secret ballot separation")` returns results via MCP
- [ ] `memory_store(text, layer="cove", type="architecture")` stores with layer tag
- [ ] Canary builds and runs without ops memory code — Owl search unaffected
- [ ] Cove builders can query platform memory without touching Canary codebase
- [ ] stdio transport works for Claude Code local connection
- [ ] Streamable HTTP transport works for remote/container access
