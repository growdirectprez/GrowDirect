# Memory Bus

> **Status:** Complete — written from code
> **Namespace:** platform
> **Last updated:** 2026-03-30
> **Code location (primary service):** `services/memory-bus/`
> **Code location (DDL):** `devops/init-db/02-create-memory-db.sql`
> **Code location (Cove consumer):** `Cove/cove/mcp/`

---

## 1. Overview

The Memory Bus is a platform-level MCP (Model Context Protocol) server that provides persistent, semantically-searchable organizational knowledge for all GrowDirect apps and agents. It serves as ALX's long-term memory across sessions — storing decisions, architectural findings, session summaries, context blocks, and team profiles in a shared PostgreSQL database with pgvector embeddings.

The service runs as a standalone FastMCP server on port 8003, accessible over HTTP. Any MCP-compatible client (ALX, builders, future agents) can call its tools to store and retrieve memories without sharing prompt context between sessions.

**Primary consumers:**
- ALX (COO agent) — session lifecycle, decision capture, context assembly at session start
- Canary builder — domain context retrieval for Canary-specific memories
- Cove builder — domain context retrieval for Cove-specific memories

**What it is not:** The Memory Bus is not the same service as the Cove Knowledge MCP Server (`Cove/cove/mcp/`). See Section 11 for the full architectural distinction.

---

## 2. Architecture

### Component Diagram

```
┌────────────────────────────────────────────────────────┐
│                  GrowDirect Network                    │
│                                                        │
│  ALX / Builders                                        │
│  (MCP clients)                                         │
│       │  HTTP (streamable-http transport)              │
│       ▼  port 8003                                     │
│  ┌─────────────────────────────────┐                   │
│  │   Memory Bus MCP Server         │                   │
│  │   services/memory-bus/          │                   │
│  │                                 │                   │
│  │   FastMCP (mcp[cli] >=1.9.0)   │                   │
│  │   server.py — tool definitions  │                   │
│  │   store.py  — core engine       │                   │
│  │   embeddings.py — Ollama client │                   │
│  │   config.py — env config        │                   │
│  └──────────┬──────────────────────┘                   │
│             │                                          │
│     ┌───────┴──────────────────────┐                   │
│     │                              │                   │
│     ▼                              ▼                   │
│  growdirect_postgres:5432     growdirect_ollama:11434   │
│  database: growdirect_memory  model: qwen3-embedding:8b │
│  tables: alx_sessions,        1024-dim vectors          │
│          alx_memories,        Matryoshka truncation      │
│          seed_embeddings       from native 4096d        │
└────────────────────────────────────────────────────────┘
```

### Request / Data Flow

**memory_store (write path):**

```
Client calls memory_store(content, memory_type, layer, ...)
  → server.py validates and delegates to store.memory_store()
  → embeddings.get_embedding(content)
      → POST http://growdirect_ollama:11434/api/embed
      → text truncated to 6000 chars before embedding
      → response.json()["embedding"][:1024] (Matryoshka truncation)
      → returns list[float] or None on failure
  → INSERT INTO alx_memories (id, session_id, memory_type, content, metadata,
                               embedding, layer, created_at, updated_at)
  → returns {memory_id, memory_type, layer, has_embedding, created_at}
```

**memory_recall (read path — three-tier fallback):**

```
Client calls memory_recall(query, limit, memory_type, layer)
  → embeddings.get_embedding(query) → embedding vector or None

  Tier 1 (vector search — if embedding available):
    → SELECT ... 1 - (embedding <=> :embedding::vector) AS similarity
      FROM alx_memories WHERE embedding IS NOT NULL [AND filters]
      ORDER BY embedding <=> :embedding::vector LIMIT :limit
    → if rows returned → format and return (source: "vector")

  Tier 2 (full-text search — if vector search returns 0 rows or no embedding):
    → SELECT ... ts_rank(to_tsvector('english', content),
                         plainto_tsquery('english', :query)) AS similarity
      FROM alx_memories
      WHERE to_tsvector('english', content) @@ plainto_tsquery('english', :query)
      [AND filters] ORDER BY similarity DESC LIMIT :limit
    → if rows returned → format and return (source: "fulltext")

  Tier 3 (ILIKE fallback — if both upper tiers return 0 rows):
    → SELECT ... 0.0 AS similarity FROM alx_memories
      WHERE content ILIKE '%query%' [AND filters]
      ORDER BY created_at DESC LIMIT :limit
    → return (source: "ilike")
```

**session_start (startup context assembly):**

```
Client calls session_start(gro_issues)
  → INSERT INTO alx_sessions (id, session_id, status='active', gro_issues, ...)
  → _assemble_startup_context(gro_issues):
      → SELECT last 5 decisions (ORDER BY created_at DESC)
      → For each GRO issue: SELECT memories WHERE content ILIKE '%<gro>%' LIMIT 3
      → Build markdown summary string
  → return {session_id, status, started_at, gro_issues, startup_context}
```

**seed_clean.py (offline seeding):**

```
Run manually or via docker exec
  → Reads source files via SOURCES config (globs + single files)
  → For each file: read_content() truncates to 6000 chars
  → build_metadata() captures source_file, seeded_by, seeded_at, plus metadata_extra
  → embeddings.get_embedding(content)
  → INSERT INTO alx_memories (session_id='seed-clean', ...)
```

### Key Design Decisions

1. **FastMCP over streamable-http transport** — All tools are exposed as HTTP-callable MCP endpoints rather than stdio. This allows long-running agent sessions and parallel callers without spawning processes.

2. **Three-tier recall fallback** — Vector search is the primary mechanism but degrades gracefully. If Ollama is unreachable at write time (no embedding stored), full-text and ILIKE search still work. This means memories stored without embeddings are still retrievable.

3. **Layer isolation** — A `layer` column (`corp`, `canary`, `cove`, `shared`) allows agents to scope queries to their domain without separate databases. Callers can pass `layer=None` to search across all layers.

4. **Session-scoped memories** — Every memory belongs to a session ID (or `'seed-clean'` / `'unattached'` for programmatic writes). Sessions carry GRO issue associations, making it possible to assemble context for a specific issue at session start.

5. **Embedding degradation without failure** — If Ollama is unreachable, `get_embedding()` returns `None` and logs a warning. The memory is stored without a vector. No exception is raised, no write is aborted.

6. **Matryoshka truncation** — Ollama's `qwen3-embedding:8b` produces 4096-dimensional vectors natively. The service slices the first 1024 dimensions (`embedding[:1024]`), matching the `vector(1024)` column and the platform standard.

---

## 3. Data Model

Database: `growdirect_memory` (PostgreSQL 17, `growdirect_postgres:5432`)
Extensions: `vector`, `pgcrypto`, `uuid-ossp`
Test database: `growdirect_memory_test` (identical schema)

### Table: `alx_sessions`

Tracks ALX work sessions. Each session is opened at the start of a work cycle and closed with a summary and decision capture.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK, `DEFAULT gen_random_uuid()` | Internal row ID |
| `session_id` | `TEXT` | NOT NULL, UNIQUE | Human-readable ID — format `alx-<12 hex chars>` (e.g., `alx-a3f2c9d1e8b4`) |
| `started_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | Session open time |
| `closed_at` | `TIMESTAMPTZ` | nullable | Populated on `session_close` |
| `status` | `TEXT` | NOT NULL, DEFAULT `'active'`, CHECK IN `('active', 'closed', 'abandoned')` | Lifecycle state |
| `gro_issues` | `JSONB` | nullable | Array of GRO issue identifiers (e.g., `["GRO-378", "GRO-379"]`) |
| `summary` | `TEXT` | nullable | Session summary written on close |
| `decisions` | `JSONB` | nullable | Array of decision strings captured at close |
| `unresolved` | `JSONB` | nullable | Array of unresolved items carried forward |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW(), auto-updated by trigger | |

**Indexes:**
- `idx_alx_sessions_status` on `(status)`
- `idx_alx_sessions_started` on `(started_at DESC)`

**Trigger:** `trg_alx_sessions_updated_at` — BEFORE UPDATE sets `updated_at = NOW()`

### Table: `alx_memories`

The core knowledge store. Each row is a single memory item with optional vector embedding and layer classification.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK, `DEFAULT gen_random_uuid()` | |
| `session_id` | `TEXT` | NOT NULL | References `alx_sessions.session_id` by value (no FK constraint) |
| `memory_type` | `TEXT` | NOT NULL, CHECK IN enumerated set | See valid types below |
| `content` | `TEXT` | NOT NULL | The memory content — up to 6000 chars before embedding truncation |
| `metadata` | `JSONB` | nullable | Arbitrary metadata — domain, block_type, source_file, etc. |
| `embedding` | `vector(1024)` | nullable | 1024-dim cosine vector. NULL when Ollama unavailable at write time |
| `layer` | `TEXT` | NOT NULL, DEFAULT `'shared'`, CHECK IN `('corp', 'canary', 'cove', 'shared')` | Scope isolation |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW(), auto-updated by trigger | |

**Valid `memory_type` values:**

| Type | Purpose |
|------|---------|
| `decision` | Architectural or product decisions |
| `finding` | Research or debugging findings |
| `context` | General contextual information |
| `architecture` | System design notes |
| `session_summary` | Written at session close — full session recap |
| `procedure` | How-to or operational procedures |
| `context_block` | Structured domain context (domain overview, API contract, workflow, data model). Queried by `domain_context` tool. |
| `work_product` | Deliverables produced during a session |
| `team_profile` | Team member role profiles |
| `foundation` | Curated foundational knowledge (LP patterns, governance config) |

**Valid `layer` values:**

| Layer | Scope |
|-------|-------|
| `corp` | Platform-wide, non-app-specific (team profiles, ADRs, platform SDDs) |
| `canary` | Canary app memories (Canary SDDs, Canary-specific findings) |
| `cove` | Cove app memories (Cove SDDs, governance foundations) |
| `shared` | Cross-app or unclassified |

**Indexes:**
- `idx_alx_memories_session` on `(session_id)`
- `idx_alx_memories_type` on `(memory_type)`
- `idx_alx_memories_created` on `(created_at DESC)`
- `idx_alx_memories_layer` on `(layer)`

Note: No HNSW or IVFFlat index on the `embedding` column in this table. Vector search uses a sequential scan. For the current scale (thousands of memories) this is acceptable. The `seed_embeddings` table (below) does use HNSW.

**Trigger:** `trg_alx_memories_updated_at` — BEFORE UPDATE sets `updated_at = NOW()`

### Table: `seed_embeddings`

Curated knowledge base for RAG-style retrieval. Seeded from source documents (SDDs, team profiles, ADRs, research docs). This table is populated by `seed_clean.py` and by legacy seed scripts. It is searched separately from `alx_memories` in older code paths; the current service primarily uses `alx_memories` with `memory_type='context_block'` and `memory_type='foundation'` for this purpose.

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `UUID` | PK, `DEFAULT gen_random_uuid()` | |
| `source_file` | `TEXT` | NOT NULL | Relative path to source document |
| `section_path` | `TEXT` | NOT NULL | Logical path within document (heading hierarchy) |
| `content` | `TEXT` | NOT NULL | Chunk content |
| `embedding` | `vector(1024)` | NOT NULL | Required — not nullable unlike `alx_memories.embedding` |
| `metadata` | `JSONB` | nullable | Tier, domain, block_type, seeding metadata |
| `created_at` | `TIMESTAMPTZ` | DEFAULT NOW() | |
| `updated_at` | `TIMESTAMPTZ` | DEFAULT NOW(), auto-updated by trigger | |

**Indexes:**
- `idx_seed_embeddings_vector` — HNSW on `(embedding vector_cosine_ops)` — the only HNSW index in the memory database
- `idx_seed_embeddings_source` on `(source_file)`

**Trigger:** `trg_seed_embeddings_updated_at`

**Note:** `seed_embeddings` is not directly queried by the current `store.py` implementation. It is populated by `seed_clean.py` (which inserts into `alx_memories`, not `seed_embeddings`) and by legacy migration scripts. Its role going forward needs clarification — see Section 11.

---

## 4. Interfaces

The Memory Bus exposes all functionality as MCP tools via FastMCP streamable-HTTP transport.

**Transport:** `streamable-http`
**Host:** `0.0.0.0` (all interfaces within Docker network)
**Port:** `8003`
**Service name:** `GrowDirect Memory Bus`
**Description:** `Platform-level organizational knowledge store`

### Tool: `session_start`

Start a new ALX session. Creates a session record and assembles startup context from recent decisions and GRO-issue-related memories.

**Parameters:**
| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `gro_issues` | `list[str]` | No | `None` | GRO issue identifiers to associate (e.g., `["GRO-378"]`) |

**Returns:** JSON string containing:
```json
{
  "session_id": "alx-a3f2c9d1e8b4",
  "status": "active",
  "started_at": "2026-03-30T12:00:00+00:00",
  "gro_issues": ["GRO-378"],
  "startup_context": "## Recent Decisions\n- ...\n\n## Context for GRO-378\n- ..."
}
```

**Behavior:** The `startup_context` field contains the last 5 decisions and up to 3 memories per GRO issue retrieved by ILIKE match. This gives ALX immediate prior context without requiring a separate `memory_recall` call.

---

### Tool: `session_close`

Close an active session with a summary and optional decision capture. Automatically stores the summary as a `session_summary` memory.

**Parameters:**
| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `session_id` | `str` | Yes | — | Must match an `active` session |
| `summary` | `str` | Yes | — | Prose summary of the session |
| `decisions` | `list[str]` | No | `None` | Decisions made — stored in `alx_sessions.decisions` |
| `unresolved` | `list[str]` | No | `None` | Unresolved items to carry forward |

**Returns:** JSON string:
```json
{
  "session_id": "alx-a3f2c9d1e8b4",
  "status": "closed",
  "closed_at": "2026-03-30T14:30:00+00:00"
}
```
On error (session not found or not active): `{"error": "No active session found: <session_id>"}`

**Behavior:** Updates `alx_sessions` status to `'closed'` and stores `summary` as a `session_summary` memory in `alx_memories` via `memory_store`. The session summary is embedded and searchable via `memory_recall`.

---

### Tool: `memory_store`

Store a memory with optional embedding, layer tag, and type classification.

**Parameters:**
| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `content` | `str` | Yes | — | Memory text — truncated to 6000 chars for embedding |
| `memory_type` | `str` | No | `"context"` | Must be one of the 10 valid types |
| `session_id` | `str` | No | `None` | Associates memory with a session; defaults to `"unattached"` |
| `metadata` | `dict` | No | `None` | Arbitrary metadata stored as JSONB |
| `layer` | `str` | No | `"shared"` | Must be one of: `corp`, `canary`, `cove`, `shared` |

**Returns:** JSON string:
```json
{
  "memory_id": "550e8400-e29b-41d4-a716-446655440000",
  "memory_type": "decision",
  "layer": "cove",
  "has_embedding": true,
  "created_at": "2026-03-30T12:05:00+00:00"
}
```
On validation failure: `{"error": "Invalid memory_type: ..."}`

**Behavior:** Attempts embedding generation via Ollama. If Ollama is unreachable, stores the memory without an embedding (`has_embedding: false`). The memory remains retrievable via full-text and ILIKE search.

---

### Tool: `memory_recall`

Semantic search over memories. Uses a three-tier fallback: vector search first, then PostgreSQL full-text search, then ILIKE substring match.

**Parameters:**
| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `query` | `str` | Yes | — | Natural language search query |
| `limit` | `int` | No | `10` | Maximum results to return |
| `memory_type` | `str` | No | `None` | Filter to specific memory type |
| `layer` | `str` | No | `None` | Filter to specific layer (`corp`, `canary`, `cove`, `shared`). `None` searches all layers. |

**Returns:** JSON string:
```json
{
  "query": "secret ballot separation",
  "matches": [
    {
      "memory_id": "550e8400-...",
      "session_id": "alx-a3f2c9d1e8b4",
      "memory_type": "decision",
      "content": "Secret ballot separation is required by Davis-Stirling Civil Code 5100",
      "metadata": {},
      "layer": "cove",
      "created_at": "2026-03-30T12:05:00+00:00",
      "similarity": 0.87
    }
  ],
  "count": 1,
  "source": "vector"
}
```

**`source` field values:**
- `"vector"` — cosine similarity search succeeded (embedding was generated and Ollama was reachable at query time)
- `"fulltext"` — PostgreSQL `to_tsvector`/`plainto_tsquery` match
- `"ilike"` — substring match fallback (similarity score is `0.0` for all results)

**Behavior:** The `layer` filter applies as an `AND` clause at each tier. If `memory_type` is set, it also filters at each tier. The fallback proceeds to the next tier only when the current tier returns zero rows.

---

### Tool: `memory_search`

Structured search by session, type, date range, or layer. No semantic component — pure relational filtering, ordered by `created_at DESC`.

**Parameters:**
| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `session_id` | `str` | No | `None` | Filter to specific session |
| `memory_type` | `str` | No | `None` | Filter to specific type |
| `since` | `str` | No | `None` | ISO datetime string — filters `created_at >= since` |
| `layer` | `str` | No | `None` | Filter to specific layer |
| `limit` | `int` | No | `20` | Maximum results |

**Returns:** JSON string:
```json
{
  "memories": [
    {
      "memory_id": "...",
      "session_id": "alx-a3f2c9d1e8b4",
      "memory_type": "decision",
      "content": "...",
      "metadata": {},
      "layer": "corp",
      "created_at": "..."
    }
  ],
  "count": 5,
  "filters": {
    "session_id": null,
    "memory_type": "decision",
    "since": null,
    "layer": null
  }
}
```

---

### Tool: `context_assemble`

Assemble a context window combining semantic recall, recent decisions, and the last session summary. Useful for giving an agent a structured view of everything relevant to a topic or GRO issue.

**Parameters:**
| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `topic` | `str` | No | `None` | Natural language topic for semantic recall |
| `gro_issue` | `str` | No | `None` | GRO issue identifier for targeted recall |
| `limit` | `int` | No | `15` | Maximum memories per semantic query |

**Returns:** JSON string:
```json
{
  "context": "## ALX Memory Context\n\n### Last Session (...)\n...\n\n### Recent Decisions\n- ...\n\n### Related Context\n- [finding] ...",
  "memory_count": 12,
  "topic": "ballot separation",
  "gro_issue": "GRO-378",
  "sources": ["550e8400-...", "661f9511-..."]
}
```

**Behavior:** Performs separate `memory_recall` calls for `gro_issue` and `topic` (if different), appends the 5 most recent decisions and the last session summary, deduplicates by `memory_id`, then formats into a structured markdown context block.

---

### Tool: `domain_context`

Retrieve structured domain context blocks for a specific service domain, respecting a token budget. Pulls `context_block` memories tagged with the target domain and assembles them in order: overview → API contract → workflow (if topic provided) → data model.

**Parameters:**
| Name | Type | Required | Default | Notes |
|------|------|----------|---------|-------|
| `domain` | `str` | Yes | — | Must be one of 11 valid domains (see below) |
| `topic` | `str` | No | `None` | Selects the most relevant workflow block via keyword matching |
| `token_budget` | `int` | No | `4000` | Approximate token budget — converted to `budget * 4` chars. Workflow and data model blocks are truncated or omitted to fit. |

**Valid `domain` values:** `identity`, `tsp`, `chirp`, `alert`, `owl`, `fox`, `analytics`, `alx`, `raas`, `ops`, `ui_bff`

**Returns:** JSON string:
```json
{
  "context": "## Chirp Domain Context\n\n### Overview\n...\n\n### API Contract\n...",
  "domain": "chirp",
  "topic": null,
  "blocks_used": ["domain_overview", "api_contract"],
  "token_estimate": 620
}
```

If no context blocks exist for the domain:
```json
{
  "context": "## Chirp Domain Context\n\n_No context blocks found for this domain. Run seed_context_blocks.py to populate._",
  "domain": "chirp",
  "topic": null,
  "blocks_used": [],
  "token_estimate": 30
}
```

**Behavior:** Queries `alx_memories` where `memory_type = 'context_block'` and `metadata->>'domain' = :domain` (or `metadata->'domains' @> :domain`). Block types are fetched in priority order. Workflow blocks are selected by `_pick_best_workflow()` which scores each workflow by keyword overlap with the `topic` string.

---

## 5. Service Layer

The `MemoryStore` class in `store.py` is the sole data access layer. It creates a SQLAlchemy engine with a connection pool (`pool_size=5`, `max_overflow=10`, `pool_pre_ping=True`) and exposes one method per MCP tool.

All SQL is written as raw `text()` queries — no SQLAlchemy ORM models are used. This keeps the service lightweight and decoupled from Alembic migrations.

### `get_embedding(text, config)` — `embeddings.py`

Generates a 1024-dimensional embedding vector via Ollama's `/api/embed` endpoint.

- Input text is truncated to `config.max_text_length` (6000 chars) before the API call
- Uses `httpx.post()` with a 30-second timeout
- The Ollama response includes a native 4096-dim vector. The function slices `embedding[:1024]` (Matryoshka truncation) before returning
- Returns `None` on any exception — the caller is always responsible for handling `None`
- Does not retry

### `memory_store()` — write path

1. Validates `memory_type` against `VALID_MEMORY_TYPES` (frozenset of 10 values)
2. Validates `layer` against `VALID_LAYERS` (frozenset: `corp`, `canary`, `cove`, `shared`)
3. Generates a UUID memory ID
4. Calls `get_embedding(content, config)` — gets vector or None
5. Inserts into `alx_memories` — uses a different INSERT statement depending on whether embedding is available (the vector column cannot be set to NULL via the parameterized path, so the column is simply omitted when embedding is None)

### `memory_recall()` — three-tier read path

The tier evaluation is sequential: each tier is only attempted if the previous tier returned zero rows (or was not applicable).

**Tier 1 — pgvector cosine similarity:**
- SQL: `WHERE embedding IS NOT NULL [AND filters] ORDER BY embedding <=> :embedding::vector LIMIT :limit`
- Similarity score: `1 - (embedding <=> :embedding::vector)` (0 = orthogonal, 1 = identical)
- Skipped entirely if `get_embedding(query)` returns None

**Tier 2 — PostgreSQL full-text search:**
- Uses `to_tsvector('english', content)` and `plainto_tsquery('english', :query)`
- Similarity score: `ts_rank(...)` — not a probability, just a relevance rank
- Language: `english` (stemming, stop words applied)

**Tier 3 — ILIKE substring:**
- SQL: `WHERE content ILIKE '%query%' ORDER BY created_at DESC`
- Similarity score: hardcoded `0.0` — no semantic weight
- Always runs and always returns (may be empty list)

### `context_assemble()` — multi-source assembly

Performs two `memory_recall` calls (one per gro_issue, one per topic), then appends structured `memory_search` calls for `decision` (limit 5) and `session_summary` (limit 1). Deduplicates results by `memory_id`. Builds a markdown-structured string with sections: Last Session, Recent Decisions, Related Context.

### `domain_context()` — budget-aware assembly

Validates `domain` against `VALID_DOMAINS` (11 Canary service domains). Converts `token_budget` to character budget (`* 4`). Fetches context blocks in four passes via `_recall_context_blocks()`:

1. `domain_overview` — always included first (no budget check)
2. `api_contract` — always included (no budget check)
3. `workflow` — only if `topic` provided; `_pick_best_workflow()` selects the block with the most topic-word overlap; truncated if over budget
4. `data_model` — only if remaining budget > 400 chars; truncated if needed

`_recall_context_blocks(domain, block_type)` queries memories where:
```sql
memory_type = 'context_block'
AND (
    metadata->>'domain' = :domain
    OR metadata->'domains' @> CAST(:domain_jsonb AS jsonb)
)
[AND metadata->>'block_type' = :block_type]
ORDER BY created_at DESC
```

### `_assemble_startup_context()` — session init

Runs two queries at session start (no embedding generation):
1. Last 5 decisions ordered by `created_at DESC`
2. For each GRO issue: 3 most recent memories matching `content ILIKE '%<gro>%'`

Returns a markdown string. Used as `startup_context` in `session_start` response.

---

## 6. Configuration

All configuration is environment-based via `memory_bus/config.py`. The `Config` class raises `KeyError` at startup if `DATABASE_URL` is not set.

| Env Var | Required | Default | Notes |
|---------|----------|---------|-------|
| `DATABASE_URL` | Yes | — | Must be set. Format: `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory` |
| `OLLAMA_URL` | No | `http://growdirect_ollama:11434` | Shared Ollama service |
| `EMBEDDING_MODEL` | No | `qwen3-embedding:8b` | Model name passed to Ollama `/api/embed` |
| `PORT` | No | `8003` | HTTP port for FastMCP server |

**Hardcoded constants (not configurable via env):**
- `embedding_dimensions = 1024` — Matryoshka target dimensions
- `max_text_length = 6000` — chars truncated before embedding

**Dev connection strings:**
```
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory
OLLAMA_URL=http://growdirect_ollama:11434
EMBEDDING_MODEL=qwen3-embedding:8b
PORT=8003
```

**Test database:** `growdirect_memory_test` at the same host. Test conftest sets `DATABASE_URL` to the test DB before any imports.

---

## 7. Security and Compliance

**Authentication:** None at the MCP transport level. The Memory Bus relies on network isolation — it is only reachable within the `growdirect` Docker network. No API key or token is required to call any tool. Any container on the `growdirect` network can read and write all memories.

**Data classification:** Memories contain:
- Architectural decisions and findings (non-sensitive)
- Session summaries describing work done (non-sensitive)
- Context blocks derived from platform SDDs and team profiles (non-sensitive)
- Foundation memories including governance config for WPBCA (HOA governance data — no PII)
- Cove layer memories may reference property data (APN numbers, governance decisions) — not PII but should be treated as operationally sensitive

**PII posture:** No PII is expected in the memory bus. The `alx_memories.layer` system ensures Cove-specific data (including any WPBCA-related governance notes) is tagged `layer='cove'` and can be filtered by non-Cove consumers.

**Credential management:** Database credentials (`growdirect / growdirect_dev`) are passed via environment variable. These are dev-only credentials — production would require separate credentials and the `DATABASE_URL` to be managed via secret management (not yet implemented).

**Write access:** All MCP tools are read-write with no role differentiation. The `seed_clean.py` script can drop all memories with `--drop-first`. There is no audit trail for memory deletion.

**Isolation from app databases:** The `growdirect_memory` database is separate from `canary`, `cove`, and other app databases. Cross-database access is not possible at the application layer.

---

## 8. Error Handling

**Invalid parameters:** `memory_store` and `domain_context` return `{"error": "..."}` dicts (serialized to JSON) rather than raising exceptions. The MCP client receives a valid JSON response, not an MCP-level error.

**Embedding failures:** `get_embedding()` catches all exceptions from the Ollama HTTP call and returns `None`. The warning is logged but the write operation proceeds. The result dict includes `"has_embedding": false`.

**Session not found:** `session_close` returns `{"error": "No active session found: <session_id>"}` when the session_id does not match any active session. It does not raise.

**Database connectivity:** `MemoryStore.healthy()` checks connectivity with `SELECT 1`. There is no circuit breaker or retry logic in the service itself.

**Ollama timeout:** `httpx.post()` is called with `timeout=30.0` seconds. If Ollama takes longer than 30 seconds, the request raises `httpx.TimeoutException`, which is caught by the outer `except Exception` in `get_embedding()`. The service continues without an embedding.

**No server-level error middleware:** The FastMCP server does not define custom error handlers. Unhandled exceptions in tool implementations will propagate as MCP-level errors to the client.

---

## 9. Testing

Tests live in `services/memory-bus/tests/`. The test suite has three layers.

### Layer 1 — Unit tests (no database, no Ollama)

**`test_config.py`** — `TestConfig`:
- `DATABASE_URL` from env
- `DATABASE_URL` missing raises `KeyError`
- Default values for `OLLAMA_URL`, `EMBEDDING_MODEL`, `PORT`

**`test_embeddings.py`** — `TestGetEmbedding`:
- Returns `list[float]` of length 1024 on success (mocked httpx)
- Returns `None` on connection error (mocked exception)
- Truncates text over `max_text_length` before sending to Ollama
- Slices to 1024 dimensions from native 4096-dim response

**`test_context_blocks.py`** — Mixed unit/integration:
This file references `canary.services.alx.memory` (Canary app code), not `memory_bus.store`. It tests an older Canary-side implementation of `recall_context_blocks()` and `assemble_domain_context()`. These tests are mislabeled as memory-bus tests — they belong to the Canary test suite. See Section 11.

**`test_rag_retrieval.py`** — Integration/live:
This file also references `canary.services.alx.memory` and expects a live `canary_memory` database (a legacy database name predating `growdirect_memory`). These tests do not test `memory_bus.store` and cannot pass against the current service. See Section 11.

### Layer 2 — Smoke tests (requires live infra)

**`test_smoke.py`** — `TestSmoke.test_store_recall_roundtrip`:
- Starts an MCP client session against the running server
- Calls `session_start`, `memory_store`, then `memory_recall`
- Asserts the recalled content contains query terms
- Requires: `growdirect_memory_test` database, Ollama running with `qwen3-embedding:8b`

### Running tests

```bash
# Unit tests only (no infra)
cd services/memory-bus
python3 -m pytest tests/test_config.py tests/test_embeddings.py -v

# Smoke test (requires running infra)
DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory_test \
OLLAMA_URL=http://localhost:11434 \
python3 -m pytest tests/test_smoke.py -v

# All tests (unit + smoke)
python3 -m pytest tests/ -v
```

### Seed script

`services/memory-bus/scripts/seed_clean.py` populates `alx_memories` from the platform document archive. It is idempotent with `--drop-first` (drops all memories first) or additive without it.

```bash
# Dry run — see what would be seeded
DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/growdirect_memory \
python3 services/memory-bus/scripts/seed_clean.py --dry-run

# Full seed with drop
docker exec growdirect_memory_bus python3 scripts/seed_clean.py --drop-first
```

Sources seeded by `seed_clean.py`:

| Source glob | Memory type | Layer |
|-------------|------------|-------|
| `docs/sdds/platform/*.md` | `context_block` | `corp` |
| `docs/sdds/canary/*.md` | `context_block` | `canary` |
| `docs/sdds/cove/*.md` | `context_block` | `cove` |
| `docs/sdds/alx/*.md` | `context_block` | `shared` |
| `docs/team/*.md` | `team_profile` | `corp` |
| `docs/decisions/*.md` | `decision` | `corp` |
| `docs/research/lp-dashboard-pattern-catalog.md` | `foundation` | `canary` |
| `Cove/cove/governance/wpbca-bylaws-config.json` | `foundation` | `cove` |

---

## 10. Dependencies

### Runtime dependencies (`pyproject.toml`)

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp[cli]` | `>=1.9.0` | FastMCP server framework, streamable-HTTP transport |
| `sqlalchemy` | `>=2.0` | Database engine and session management |
| `pgvector` | `>=0.3.0` | pgvector SQLAlchemy integration (vector type handling) |
| `psycopg2-binary` | `>=2.9` | PostgreSQL driver |
| `httpx` | `>=0.27` | Async-capable HTTP client for Ollama calls |

### Dev dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | `>=8.0` | Test runner |
| `pytest-asyncio` | `>=0.24` | Async test support for smoke tests |

### Infrastructure dependencies

| Service | Address | Purpose |
|---------|---------|---------|
| `growdirect_postgres` | `growdirect_postgres:5432` | Database host — `growdirect_memory` database |
| `growdirect_ollama` | `growdirect_ollama:11434` | Embedding generation via `/api/embed` |

### Build

The service is built as a Docker image from `services/memory-bus/Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN apt-get install -y libpq-dev gcc  # psycopg2-binary requires libpq
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY memory_bus/ memory_bus/
EXPOSE 8003
CMD ["python3", "-m", "memory_bus.server"]
```

The entry point `python3 -m memory_bus.server` calls `mcp.run(transport="streamable-http", host="0.0.0.0", port=config.port)`.

The service is registered in the shared devops compose as `growdirect_memory_bus` with `image: growdirect-memory-bus`.

---

## 11. Known Issues and Reconciliation

### CRITICAL: Dual-Codebase Architecture

The term "Memory Bus" in the GrowDirect codebase refers to two distinct and separate services. This is a scope issue that requires active reconciliation.

---

**Service A — Platform Memory Bus** (this document)

- **Location:** `services/memory-bus/`
- **Deployed as:** `growdirect_memory_bus` Docker container, port 8003
- **Transport:** FastMCP streamable-HTTP
- **Database:** `growdirect_memory` (standalone database)
- **Purpose:** ALX's long-term organizational memory — sessions, decisions, context blocks, team profiles
- **Consumers:** ALX agent, all builders via MCP tool calls
- **Data model:** Three tables: `alx_sessions`, `alx_memories`, `seed_embeddings`

**Service B — Cove Knowledge MCP Server**

- **Location:** `Cove/cove/mcp/`
- **Entry point:** `python -m cove.mcp.server`
- **Transport:** MCP stdio
- **Database:** `cove` (Cove's application database, table `knowledge_chunks`)
- **Purpose:** Legal and community knowledge base for WPBCA governance — CC&Rs, bylaws, litigation records, city records, property documents
- **Consumers:** Cove AI agent, external MCP clients
- **Data model:** One table: `knowledge_chunks` with full provenance metadata

**Are they the same service?** No. They serve different purposes, store different data, use different databases, and run on different transports. They share the same embedding model and similar chunking/embedding patterns.

**Are they complementary?** Partially. Service A is the platform memory layer for AI agent continuity. Service B is a domain-specific RAG knowledge base for Cove governance queries. An agent working on Cove could legitimately use both.

**Are they redundant?** Only in their embedding and chunking infrastructure. Both call Ollama with `qwen3-embedding:8b`, both truncate to 1024 dimensions, both store chunks with provenance metadata. This duplication is intentional — Service B is self-contained within the Cove repo and can operate without Service A.

---

### Issue: `test_context_blocks.py` and `test_rag_retrieval.py` are in the wrong repository

Both files in `services/memory-bus/tests/` import from `canary.services.alx.memory`, not from `memory_bus.store`. They test an older Canary-side memory implementation that predates the standalone Memory Bus service. These tests cannot pass in the `services/memory-bus/` test environment.

**Resolution needed:** Move these test files to the Canary test suite or rewrite them to test `memory_bus.store` directly.

---

### Issue: `seed_embeddings` table purpose is unclear

The `seed_embeddings` table has an HNSW index and a NOT NULL embedding constraint — it was designed for direct RAG lookups. However, the current `seed_clean.py` script inserts into `alx_memories` (not `seed_embeddings`), and `store.py` does not query `seed_embeddings` at all.

Legacy integration tests (`test_rag_retrieval.py`) reference a `memory_semantic_search` function that queries both `alx_memories` and `seed_embeddings` via `UNION ALL`. This function exists in `canary.services.alx.memory`, not in `memory_bus.store`.

**Current state:** `seed_embeddings` is populated by legacy scripts (pre-GRO-379 seed scripts) and is not consumed by the current service. It should either be removed, or the service should be updated to search it as a higher-fidelity RAG source alongside `alx_memories`.

---

### Issue: No authentication on the MCP server

Any container on the `growdirect` Docker network can call any Memory Bus tool, including writing and deleting memories. There is no API key, no role differentiation, and no audit log for writes.

**Risk:** A misconfigured or compromised container could corrupt or wipe platform memory. The `seed_clean.py --drop-first` flag deletes all memories with no confirmation.

**Resolution needed:** Add optional API key authentication to the FastMCP server. Add a write audit log or at minimum protect destructive operations.

---

### Issue: No HNSW index on `alx_memories.embedding`

Vector search on `alx_memories` uses a sequential scan. At small scale (thousands of memories) this is acceptable. At tens of thousands of memories, recall latency will degrade.

**Resolution:** Add `CREATE INDEX USING hnsw (embedding vector_cosine_ops)` on `alx_memories` when the row count warrants it (generally above ~10,000 rows).

---

### Issue: `session_id` in `alx_memories` is a text foreign key with no constraint

Memories reference `alx_sessions.session_id` (the human-readable `alx-<hex>` identifier) by text value, not by a foreign key constraint. This allows memories to be stored with arbitrary session IDs (including `'seed-clean'` and `'unattached'`) without a corresponding session record.

This is an intentional design choice for flexibility but means referential integrity is not enforced at the database level.

---

### Issue: Cove MCP server runs on stdio, not HTTP

Service B (`Cove/cove/mcp/`) uses `mcp.server.stdio` transport. This means it must be invoked as a subprocess and communicates over stdin/stdout. It cannot be called by HTTP clients. Service A uses streamable-HTTP and can be called over the network.

If a Cove builder agent needs to access both services, it must use two different MCP connection methods. This should be documented in the Cove CLAUDE.md and any agent harness configuration.
