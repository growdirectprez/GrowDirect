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

New field on all memory records: `layer` (enum: `corp`, `canary`, `cove`, `shared`) for scoped retrieval. Defaults to `shared`.

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
```

## Database Migration

- `canary_memory` renamed to `growdirect_memory` in `devops/init-db/01-create-databases.sql`
- `02-create-memory-db.sql` moves from `Canary/devops/init-db/` to `GrowDirect/devops/init-db/`, references `growdirect_memory`
- One-time migration script: `ALTER DATABASE canary_memory RENAME TO growdirect_memory`
- New test DB `growdirect_memory_test` added to init script

## Canary Cleanup

**Deleted:**
- `canary/services/alx/memory.py`
- `canary/services/alx/tools.py`
- `canary/blueprints/alx_api.py`
- `Canary/devops/init-db/02-create-memory-db.sql`

**Moved to `services/memory-bus/scripts/`:**
- `seed_context_blocks.py`, `seed_memory_foundation.py`, `seed_work_products.py`, `seed_team_profiles.py`, `seed_sdds_v2.py`, `embed_memories_batch.py`, `load_memories.py`, `ingest_tier2_batch.py`, `field_registry_seed.py`

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
