# Knowledge Module

**Status:** Active
**Type:** MCP Server
**Last updated:** 2026-04-13
**Server:** `cove.mcp.server` (stdio transport)
**Model:** `cove/models/knowledge.py`
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]] | [[Brain/wiki/cove-legal-framework|Cove Legal Framework]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]

---

## Purpose

Standalone MCP server exposing Cove's pgvector knowledge base for semantic search over WPBCA legal documents. Stores verbatim text chunks from the archive (CC&Rs, bylaws, litigation filings, title reports, city records, historical corporate documents) with full provenance metadata. Designed for precise retrieval of exact legal language, not summarization.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | `knowledge_chunks` table with pgvector | Yes |
| Ollama (`growdirect_ollama:11434`) | Embedding generation (qwen3-embedding:8b, 1024d) | Yes (for search and ingest) |
| MCP SDK (`mcp` Python package) | Server framework, stdio transport | Yes |
| `Cove/docs/archive/` (filesystem) | Source documents for seed script | For seeding only |

---

## Data Flow & PII Map

### What enters
- Seed script: reads `.md` files from `docs/archive/`, chunks text, generates embeddings, inserts to DB
- MCP ingest tools: accept document content + metadata, chunk and embed
- MCP search tools: accept query strings, generate query embedding

### What's stored

| Table | Field | Classification | Encryption |
|-------|-------|---------------|------------|
| `knowledge_chunks` | `content` | internal | Plaintext (legal document text) |
| `knowledge_chunks` | `heading` | internal | Plaintext |
| `knowledge_chunks` | `source_file` | internal | Plaintext (file path) |
| `knowledge_chunks` | `extra` (JSONB) | internal | Plaintext (APN refs, citations) |
| `knowledge_chunks` | `embedding` | internal | Vector(1024) |

### What exits
- Search results: chunk content, heading, source_file, category, provenance metadata
- Statistics: chunk counts, category breakdowns
- Resources: bylaws config JSON, category list, community context

**PII note:** Knowledge chunks contain legal document text. Some chunks may reference property owners by name in historical documents (litigation, title reports). These are public record references, not collected PII, but should be treated as internal.

---

## MCP Tool Registry

| Tool | Auth Required | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|
| `knowledge_search` | No (stdio trusted) | None | None | Semantic search with category/date filters |
| `knowledge_get_chunk` | No | None | None | Retrieve chunk by ID with optional neighbors |
| `knowledge_list_sources` | No | None | None | List source documents grouped by category |
| `knowledge_stats` | No | None | None | Knowledge base statistics |
| `knowledge_find_by_apn` | No | None | None | Find chunks referencing an APN |
| `knowledge_find_by_citation` | No | None | None | Find chunks referencing a legal citation |
| `knowledge_ingest_document` | Write key (SSE) | None | None | Ingest and chunk a new document |
| `knowledge_add_chunk` | Write key (SSE) | None | None | Add a single chunk directly |
| `knowledge_delete_source` | Write key (SSE) | None | None | Delete all chunks from a source |
| `knowledge_reindex` | Write key (SSE) | None | None | Re-generate embeddings |

### MCP Resources

| URI | Description |
|-----|-------------|
| `cove://bylaws/config` | Current bylaws config JSON |
| `cove://categories` | Knowledge categories with descriptions |
| `cove://legislative/updates` | Recent California HOA legislation |
| `cove://community/context` | WPBCA summary: parcels, members, board |

---

## Cross-App Data Access

The Knowledge MCP server accesses only the `knowledge_chunks` table and bylaws config in the `cove` database. It has **read/write access to knowledge_chunks** and **read-only access to bylaws config**. It does not access member data, governance data, or any other application tables.

No cross-app data access exists. The server is scoped to Cove's knowledge base only.

---

## Tool Dispatch Security

- **Stdio transport**: Trusted -- runs as a subprocess of the calling agent. No network authentication.
- **SSE transport** (future): `MCP_API_KEY` for read tools, `MCP_WRITE_KEY` for write tools (ingest, delete, reindex). Keys from environment variables.
- **Privilege escalation**: Write tools can modify/delete knowledge chunks but cannot access other tables. SQL injection prevented by parameterized queries.
- **Compromise scenario**: If the MCP server is compromised, an attacker could modify legal document chunks (data integrity risk) but cannot access member PII or governance data.

---

## API Contract

Server: `cove-knowledge` via stdio.

```bash
# Run directly
python -m cove.mcp.server

# Via Docker
docker exec -i cove_knowledge_mcp python -m cove.mcp.server
```

---

## Embedding Service (`cove/services/embedding.py`)

| Config | Value |
|--------|-------|
| Model | `qwen3-embedding:8b` (1024 dimensions) |
| API | `POST /api/embed` to Ollama |
| Truncation | 6000 chars max input |
| Timeout | 15s (service), 30s (seed script) |
| Failure | Returns `None` gracefully |

Similarity: cosine distance via `<=>` operator.

---

## Seed Script (`seed_knowledge.py`)

- **Strategy**: Truncate-and-reload on each run
- **Chunking**: Split on `##`/`###`/`####` headings, then paragraphs, then sentences. Target ~1500 chars, minimum 50 chars.
- **Provenance**: Extracts APN references, instrument numbers, legal citations into `extra` JSONB
- **Scale**: ~148 source files, ~4567 chunks, spanning 1929-2026
- **Performance**: Uses raw psycopg2 for bulk insert; commits per file

---

## Operations

### Startup

```bash
# Start as MCP server (stdio)
python -m cove.mcp.server

# Seed knowledge base
docker exec cove_flask python3 seed_knowledge.py [--dry-run] [--no-embed] [--verbose]
```

### Health Checks
No built-in health check (stdio transport). Health inferred from successful tool calls.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| PostgreSQL down | All tools return error JSON | Server stays alive, reconnects on next call |
| Ollama down | Search returns no results (null embeddings); ingest stores chunks without embeddings | Reindex after Ollama recovery |
| Seed script interrupted | Partially seeded knowledge base (committed per file) | Re-run seed script (truncates and rebuilds) |

### Configuration

| Variable | Required | Default |
|----------|----------|---------|
| `DATABASE_URL` | Yes | (none) |
| `OLLAMA_URL` | No | `http://localhost:11434` |
| `MCP_API_KEY` | No (stdio) | (empty) |
| `MCP_WRITE_KEY` | No (stdio) | (empty) |

---

## Deployment

### Docker Service Definition

Knowledge MCP server can run as:
1. **Subprocess**: Started by the calling agent directly (current dev pattern)
2. **Dedicated container**: `cove_knowledge_mcp` with stdio piped from agent container

### AWS Target

- **Compute**: Sidecar container in ECS task (shares network with Flask)
- **Database**: Same RDS instance as Cove app
- **Secrets**: `DATABASE_URL`, `OLLAMA_URL` via Secrets Manager

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P0** | Write tools (ingest, delete, reindex) have no authentication on stdio transport -- any MCP client can modify the knowledge base | Implement tool-level auth check even for stdio; require `MCP_WRITE_KEY` |
| 2 | **P1** | Seed script truncates entire table on each run -- no incremental update mechanism | Add incremental mode: hash source files, only re-seed changed files |
| 3 | **P1** | Dual embedding functions (service + seed script) with different timeouts could produce inconsistent embeddings if model changes | Consolidate to single embedding function with configurable timeout |
| 4 | **P1** | No input validation on `knowledge_ingest_document` content length -- unbounded text could cause OOM | Add content length limit (e.g., 1MB per document) |
| 5 | **P2** | Handler dispatch uses lambda wrappers with `asyncio.to_thread` for sync functions -- consider native async handlers | Refactor to native async for better performance |
| 6 | **P2** | No observability -- tool call metrics, latency, error rates not tracked | Add structured logging per tool call |
| 7 | **P2** | Resource URIs use custom `cove://` scheme -- standard MCP practice but not discoverable by generic clients | Document resource URIs in server metadata |

---

## Production Readiness Checklist

- [x] No member PII in knowledge chunks (legal document text only)
- [ ] Write tool authentication enforced
- [ ] Secrets in AWS Secrets Manager
- [ ] Health check mechanism for MCP server
- [ ] Input validation on ingest tools (content length limits)
- [ ] Incremental seed capability (avoid full truncate)
- [x] Error responses don't leak internals (JSON error format)
- [ ] Tool call observability (metrics, logging)
- [ ] Embedding function consolidated (single source of truth)
