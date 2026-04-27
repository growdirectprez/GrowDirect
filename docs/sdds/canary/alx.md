# ALX — Knowledge Store

**Type:** App Service (Canary) / Platform Service (Memory Bus)
**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/ALX|ALX]]
**Last reviewed:** 2026-04-13

## Purpose

ALX owns institutional memory for the GrowDirect platform. It is a pgvector-powered knowledge store that persists decisions, architectural patterns, findings, and operational context across agent sessions. ALX is what makes the agent more than a stateless assistant — it remembers what was decided, why, and what remains unresolved.

As of GRO-172, the core memory operations live in a standalone Memory Bus MCP server (`services/memory-bus/`) running on port 8003. The Canary-side ALX module (`Canary/canary/services/alx/`) is now a stub pointing to the platform service. Owl's institutional knowledge adapter (`Canary/canary/services/owl/institutional.py`) reads from the Memory Bus via HTTP.

## Dependencies

| Dependency | Type | Required | Notes |
|------------|------|:--------:|-------|
| PostgreSQL 17 (`growdirect_memory` database) | Database | Yes | pgvector extension, HNSW index |
| Ollama (`growdirect_ollama:11434`) | Embedding service | No | Best-effort; memories store without vectors if unavailable |
| Valkey | None | -- | ALX does not use Valkey |
| growdirect-mcp SDK | Python package | Yes | Auth module (`validate_api_key`, `AuthError`) |
| Canary Flask app | Consumer | No | Owl reads via HTTP; ALX does not depend on Canary running |

**Startup order:** PostgreSQL must be healthy before Memory Bus starts. Ollama should be available but is not blocking.

## Data Flow & PII Map

### What enters

| Source | Format | Transport |
|--------|--------|-----------|
| Agent sessions (Claude Code, Cursor) | MCP tool calls via FastMCP | stdio bridge -> HTTP POST to port 8003 |
| Owl institutional knowledge adapter | HTTP POST | `httpx` call to `growdirect_memory_bus:8003` |
| Seed scripts (`seed_clean.py`) | Direct SQL INSERT | SQLAlchemy engine against `growdirect_memory` |

### What is stored

**Database:** `growdirect_memory` (separate from `canary` which holds `app`, `sales`, `metrics` schemas)

**Table: `alx_memories`**

| Column | Type | PII Classification | Notes |
|--------|------|--------------------|-------|
| id | UUID PK | public | Auto-generated `uuid4` |
| session_id | TEXT (FK) | internal | References `alx_sessions.session_id` |
| memory_type | TEXT | public | Constrained: decision, finding, context, architecture, session_summary, procedure, context_block, work_product, team_profile, foundation |
| content | TEXT | **sensitive** | May contain team member names, architectural decisions with internal details, session summaries with project-specific context |
| metadata | JSONB | internal | Tags, source agent, GRO issue references, block_type, domain, sdd_refs |
| embedding | vector(1024) | internal | qwen3-embedding:8b via Ollama, Matryoshka truncation from native 4096d |
| layer | TEXT | public | Constrained: corp, canary, cove, shared |
| created_at | TIMESTAMPTZ | public | Auto-set |
| updated_at | TIMESTAMPTZ | public | Auto-set |

**Table: `alx_sessions`**

| Column | Type | PII Classification | Notes |
|--------|------|--------------------|-------|
| id | UUID PK | public | Auto-generated |
| session_id | TEXT UNIQUE | internal | Format: `alx-{uuid4_hex[:12]}` |
| started_at | TIMESTAMPTZ | public | |
| closed_at | TIMESTAMPTZ | public | Set on close |
| status | TEXT | public | Constrained: active, closed, abandoned |
| gro_issues | JSONB | internal | Array of GRO issue numbers |
| summary | TEXT | **sensitive** | Session summary text — may contain internal project details |
| decisions | JSONB | **sensitive** | Array of decision strings |
| unresolved | JSONB | internal | Array of unresolved items |
| created_at | TIMESTAMPTZ | public | |
| updated_at | TIMESTAMPTZ | public | |

### What exits

| Destination | Data | Transport |
|-------------|------|-----------|
| Agent sessions | Recall results, context blocks, session context | MCP tool response (JSON) |
| Owl prompt assembly | Institutional knowledge (Window 0, ~2000 token budget) | HTTP response via `build_institutional_context()` |
| No external APIs | ALX never sends data outside the Docker network | -- |

### PII Summary

ALX stores **no end-user PII** (no customer emails, phones, payment data). Its sensitive data consists of:
- Internal team member names in `team_profile` memories
- Architectural decisions and session summaries containing internal business context
- GRO issue references that map to Linear tickets

**Risk level:** Low-Medium. The data is organizational knowledge, not customer data. However, `content` and `summary` fields could contain references to internal strategies, team evaluations, or confidential business decisions.

## API Contract

### MCP Server (FastMCP on port 8003)

The Memory Bus runs as a standalone FastMCP server, not a Flask blueprint. Transport: streamable-HTTP.

**Auth:** Every tool accepts an `api_key` parameter. The `validate_api_key()` function from `growdirect_mcp.auth` checks against `MCP_API_KEY` env var. Auth can be disabled with `MCP_AUTH_DISABLED=1` for trusted networks.

| Tool | Category | Required Params | Optional Params | Returns |
|------|----------|----------------|-----------------|---------|
| `session_start` | session | -- | `gro_issues[]`, `api_key` | `{session_id, status, started_at, gro_issues, startup_context}` |
| `session_close` | session | `session_id`, `summary` | `decisions[]`, `unresolved[]`, `api_key` | `{session_id, status, closed_at, summary}` |
| `memory_store` | memory | `content` | `memory_type`, `session_id`, `metadata`, `layer`, `api_key` | `{memory_id, memory_type, layer, has_embedding, created_at}` |
| `memory_recall` | memory | `query` | `limit` (10), `memory_type`, `layer`, `api_key` | `{query, matches[], count, source}` |
| `memory_search` | memory | -- | `session_id`, `memory_type`, `since`, `layer`, `limit` (20), `api_key` | `{memories[], count, filters}` |
| `context_assemble` | context | -- | `topic`, `gro_issue`, `limit` (15), `api_key` | `{context, memory_count, topic, gro_issue, sources[]}` |
| `domain_context` | context | `domain` | `topic`, `token_budget` (4000), `api_key` | `{context, domain, topic, blocks_used[], token_estimate}` |

### Recall search tiers

1. **Tier 1 (pgvector):** Embeds query via Ollama, cosine similarity search with HNSW index. No explicit threshold — returns top-N results.
2. **Tier 2 (full-text):** PostgreSQL `to_tsvector/plainto_tsquery` with `ts_rank` ordering.
3. **Tier 3 (ILIKE):** `content ILIKE '%query%'` ordered by `created_at DESC`.

### MCP Stdio Bridge (SDD-065)

IDE agents connect via `Canary/canary/mcp/streamable_server.py` which translates MCP stdio calls into authenticated HTTP requests. The bridge runs in a dedicated `.venv-mcp/` virtualenv. Note: the streamable server `SERVER_PREFIXES` map does **not** include an `alx` entry — ALX is accessed directly via the Memory Bus on port 8003, not through the Canary Flask proxy.

### Institutional Knowledge Adapter (Owl, SDD-061)

`Canary/canary/services/owl/institutional.py` calls the Memory Bus directly:

- `build_institutional_context(personality, user_message, token_budget=2000)` — formats memories for Owl Window 0
- `knowledge_search(query, personality, limit)` — structured results for MCP tool exposure
- Adapter uses `httpx.post()` to `http://growdirect_memory_bus:8003/mcp/v1/tools/memory_recall`
- **Best-effort:** Returns empty string if Memory Bus is unreachable

### Response Envelope

All tool invocations return JSON (serialized via `json.dumps(result, default=str)`). On auth failure, returns `{"error": "..."}`. No HTTP status code differentiation — errors are in-band.

### Health Check

No dedicated health endpoint on the FastMCP server. The Docker healthcheck uses: `curl -so /dev/null -w '%{http_code}' http://localhost:8003/mcp | grep -q '406'` (expects a 406 from the MCP protocol endpoint to confirm the server is responding).

The `MemoryStore.healthy()` method checks database connectivity via `SELECT 1`.

## Operations

### Startup Sequence

1. PostgreSQL container healthy (healthcheck passes)
2. Memory Bus container starts: `python3 -m memory_bus.server`
3. `Config.__init__()` reads `DATABASE_URL`, `OLLAMA_URL`, `EMBEDDING_MODEL`, `PORT`, `MCP_API_KEY` from environment
4. `MemoryStore.__init__()` creates SQLAlchemy engine with `pool_size=5`, `max_overflow=10`, `pool_pre_ping=True`
5. FastMCP server binds to `0.0.0.0:8003` with streamable-HTTP transport
6. Docker healthcheck confirms MCP endpoint responds (406 = alive)

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| PostgreSQL down | **All operations fail** | `MemoryStore.healthy()` returns false. Tool calls return errors. Agent sessions proceed without memory. |
| Ollama down | Embeddings unavailable | `get_embedding()` returns `None`, memories store without vectors. Recall falls back to full-text/ILIKE. Partial degradation — search quality degrades but system remains functional. |
| Memory Bus container down | No memory operations | Agents proceed without institutional context. Owl's `build_institutional_context()` returns empty string. |
| HNSW index corrupted | Vector search fails | Full-text and ILIKE fallback tiers still function. `REINDEX` required. |
| Embedding model changed | Existing vectors incompatible | Batch re-embed all memories. Old vectors produce poor similarity scores against new queries. |

### Monitoring

| Metric | Alert Threshold | Source |
|--------|----------------|--------|
| Container health | Unhealthy 2+ checks | Docker healthcheck |
| `alx_memories` row count | Baseline tracking (currently 900+) | `SELECT count(*) FROM alx_memories` |
| Embedding coverage | < 80% of memories have non-NULL embedding | `SELECT count(*) FILTER (WHERE embedding IS NOT NULL) * 100.0 / count(*) FROM alx_memories` |
| Session orphans | Active sessions older than 24h | `SELECT * FROM alx_sessions WHERE status = 'active' AND started_at < now() - interval '24 hours'` |

### Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `DATABASE_URL` | (required) | PostgreSQL connection string to `growdirect_memory` |
| `OLLAMA_URL` | `http://growdirect_ollama:11434` | Ollama embedding endpoint |
| `EMBEDDING_MODEL` | `qwen3-embedding:8b` | Model for 1024-dim vectors (Matryoshka from 4096d native) |
| `PORT` | `8003` | FastMCP server port |
| `MCP_API_KEY` | (empty) | API key for tool auth; empty = auth fails unless `MCP_AUTH_DISABLED=1` |
| `MCP_AUTH_DISABLED` | (unset) | Set to `1` to bypass API key validation |

### Seeding

`services/memory-bus/scripts/seed_clean.py` populates baseline knowledge from:
- `docs/sdds/**/*.md` as `context_block` memories
- `docs/team/*.md` as `team_profile` memories
- `docs/decisions/*.md` as `decision` memories
- `docs/research/lp-dashboard-pattern-catalog.md` as `foundation` memory
- `Cove/cove/governance/wpbca-bylaws-config.json` as `foundation` memory

Run: `docker exec growdirect_memory_bus python3 scripts/seed_clean.py --drop-first`

## Deployment

### Docker Service Definition

```yaml
# In devops/docker-compose.yml
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

### AWS Target

| Component | AWS Service | Notes |
|-----------|-------------|-------|
| Memory Bus container | ECS/Fargate | Single task, no scaling needed |
| `growdirect_memory` database | RDS PostgreSQL 17 with pgvector | Shared RDS instance, separate database |
| Ollama | ECS/Fargate or SageMaker endpoint | For embedding generation |
| `MCP_API_KEY` | Secrets Manager | Not `.env` |
| `DATABASE_URL` | Secrets Manager | Connection string with IAM auth |

### CI/CD Requirements

- Alembic migrations run before container deploy: `cd services/memory-bus && alembic upgrade head`
- Seed script runs after migrations on fresh environments
- No Tailwind/npm build step — pure Python service

### Migrations

Managed by Alembic in `services/memory-bus/migrations/`:

| Revision | Description |
|----------|-------------|
| `001_baseline` | Initial schema: `alx_sessions`, `alx_memories`, `seed_embeddings` |
| `002_drop_seed_embeddings` | Drops legacy `seed_embeddings` table |
| `003_hnsw_index` | HNSW index on `alx_memories.embedding` for vector search |
| `004_session_fk` | Backfills orphan sessions, adds FK from `alx_memories.session_id` to `alx_sessions.session_id` |

## Hawk Case Context Integration

ALX's recall surface includes Hawk card bodies via the `hawk_cards.vector` column (pgvector 1024-dim). When an agent session queries `memory_recall("loss prevention cases at Store B")`, the recall tiers search across both `alx_memories` (institutional knowledge) and `hawk_cards` (investigation summaries). Card frontmatter fields (`incident_class`, `de_pv_flag`, `subject_types`) enable filtered recall.

**Not yet wired.** The Hawk card table lives in the `canary` database (`app` schema), not the `growdirect_memory` database. Cross-database recall requires either: (a) a federated query via `dblink` / foreign data wrapper, or (b) a sync job that copies card embeddings into `alx_memories` with `memory_type=hawk_card`. Option (b) is preferred — it keeps the Memory Bus self-contained and avoids cross-database coupling. See `docs/sdds/canary/hawk.md` §Card Factory and `docs/sdds/canary/owl.md` §Phase 4 Stub.

## Multi-POS Awareness

ALX's knowledge store is POS-agnostic — memories, decisions, and context blocks carry no provider attribution. However, when ALX serves as the VSM (Virtual Store Manager) diagnostic agent, the interaction model varies by POS substrate:

| Dimension | Square tenant | Counterpoint tenant |
|---|---|---|
| Data freshness | Real-time (webhook push, sub-second) | Near-real-time (poll cadence, 60s steady-state) |
| Audit trail depth | Limited (no per-document audit log) | Rich (PS_DOC_AUDIT_LOG with ACTIV codes) |
| Drawer session model | CashDrawerShift events | DRW_SESSION_ID correlation via audit log |
| Cutover status | Live (v1 production) | Scaffold/Seed phase (Hawk Phase 1) |

The VSM diagnostic frame (described in `Brain/wiki/canary-vsm-diagnostic-mode-requirement.md`) must be cutover-aware: ALX suppresses diagnostic queries that depend on Counterpoint-specific substrates (audit log depth, margin targets, multi-authority tax) when the tenant's POS source is Square-only. Provider attribution on `CanonicalEvent.provider` is the runtime signal; ALX reads it from the CRDM, not from configuration.

## Code Review Findings

### P0 — Blocks Production

**P0-1: SQL injection via ILIKE in startup context assembly**

`MemoryStore._assemble_startup_context()` interpolates GRO issue strings directly into an ILIKE pattern without escaping SQL wildcards or special characters:

```python
params = {"pattern": f"%{gro}%"}
```

While parameterized queries prevent classic SQL injection, the `gro` value is user-controlled (passed via `session_start(gro_issues=[...])`) and could contain ILIKE metacharacters (`%`, `_`) that alter query behavior. More critically, the `gro_issues` parameter comes from MCP tool input with no validation — a malicious agent could pass arbitrary strings.

**Recommended fix:** Validate `gro_issues` entries against a pattern (e.g., `^GRO-\d+$`). Escape ILIKE metacharacters in the pattern string.

**P0-2: SQL injection via ILIKE in memory_recall Tier 3**

`MemoryStore.memory_recall()` Tier 3 fallback uses the raw query string in an ILIKE pattern:

```python
{"pattern": f"%{query}%"}
```

The `query` parameter comes directly from MCP tool input. While parameterized, ILIKE metacharacters are not escaped. A query containing `%` or `_` will match unintended content.

**Recommended fix:** Escape ILIKE metacharacters before interpolation. Consider whether Tier 3 ILIKE fallback should exist in production at all — it bypasses the semantic and full-text search quality gates.

**P0-3: Auth bypass via MCP_AUTH_DISABLED environment variable**

`validate_api_key()` in `growdirect_mcp/auth.py` checks `MCP_AUTH_DISABLED=1` to skip all authentication. The Docker Compose file does not set this variable, but it is trivially exploitable if someone sets it in the environment. There is no alternative auth mechanism — no JWT validation on the MCP server, no mTLS, no network policy.

**Recommended fix:** Remove `MCP_AUTH_DISABLED` for production. Implement network-level isolation (Docker network policies or AWS security groups) so only authorized containers can reach port 8003. Add JWT validation as an alternative to API key auth.

**P0-4: Default API key in Docker Compose**

```yaml
MCP_API_KEY: ${MCP_API_KEY:-growdirect-memory-dev-key}
```

The fallback `growdirect-memory-dev-key` is committed to the repo. In production, if the env var is not set, the service runs with a known, committed API key.

**Recommended fix:** Remove the default. Production deployments must fail to start if `MCP_API_KEY` is not set. Move to AWS Secrets Manager.

### P1 — Before GA

**P1-1: No audit logging for memory operations**

`memory_store()`, `session_start()`, and `session_close()` have no audit trail. There is no record of who stored what, who queried what, or which agent session performed which operations. The `api_key` parameter is validated but not logged (not even the key identity, just pass/fail).

**Recommended fix:** Add structured audit logging (caller identity, operation, timestamp, memory_id) to a separate audit table or structured log stream.

**P1-2: No data retention policy**

Memories accumulate indefinitely. There is no TTL, no archival, no purge mechanism. The `seed_clean.py --drop-first` flag is a nuclear option that deletes everything.

**Recommended fix:** Implement tiered retention: session summaries auto-archive after 90 days, context blocks refreshed on re-seed, decisions preserved indefinitely. Add `archived_at` column and periodic cleanup job.

**P1-3: No rate limiting on MCP tool calls**

The FastMCP server has no rate limiting. Any client with a valid API key can flood the server with store/recall operations.

**Recommended fix:** Add rate limiting per API key at the FastMCP middleware level, or implement connection-level limits in the Docker/AWS network configuration.

**P1-4: Error responses may leak internal details**

Auth errors return descriptive messages like `"MCP_API_KEY not configured"` and `"Invalid API key"`. Store errors return raw exception strings. This reveals internal configuration details.

**Recommended fix:** Return generic error codes in production. Log detailed errors server-side only.

**P1-5: No TLS on Memory Bus port**

The Memory Bus listens on plain HTTP (port 8003). Within the Docker network this is acceptable for development, but in AWS the traffic between containers should be encrypted.

**Recommended fix:** Enable TLS on the FastMCP server in production, or use AWS App Mesh / service mesh for mTLS between services.

**P1-6: Embedding model version not tracked per memory**

Memories store embeddings generated by whatever model is configured at write time. If the model changes (e.g., from `nomic-embed-text` to `qwen3-embedding:8b`, which already happened), old embeddings become incompatible with new query embeddings. There is no column tracking which model generated each embedding.

**Recommended fix:** Add `embedding_model` column to `alx_memories`. Use it to filter or flag stale embeddings when the model changes.

**P1-7: `memory_store()` accepts `session_id="unattached"` as default**

In `server.py`, when `session_id` is not provided, it defaults to `"unattached"`:

```python
session_id=session_id or "unattached"
```

If no `"unattached"` session exists in `alx_sessions`, the FK constraint (migration 004) will cause the insert to fail. The error handling returns the error in-band but the UX is confusing.

**Recommended fix:** Auto-create an `"unattached"` session on first use, or require `session_id` to be non-optional.

### P2 — Post-Launch

**P2-1: No key rotation procedure documented**

API key rotation requires updating the `MCP_API_KEY` env var in Docker Compose and restarting the container. No documented procedure, no graceful transition with two keys active simultaneously.

**Recommended fix:** Document rotation procedure. Support multiple valid API keys during transition window.

**P2-2: HNSW index parameters not tuned**

The HNSW index uses default `ef_construction` and `m` parameters. For the current dataset (~900 memories), defaults are fine. At scale (10K+ memories), tuning these parameters affects recall quality and search latency.

**Recommended fix:** Benchmark and tune HNSW parameters when memory count exceeds 5K.

**P2-3: Embedding truncation at 6000 chars**

`Config.max_text_length = 6000` truncates content before embedding. Long SDDs or session summaries lose tail content. The truncation is silent — no metadata records how much was truncated.

**Recommended fix:** Record `original_length` and `truncated_length` in metadata. Consider chunking long documents into multiple memories.

**P2-4: `_pick_best_workflow()` uses naive keyword overlap**

Workflow selection in `domain_context()` scores by counting how many topic words appear in the content. This is a word-presence check, not semantic similarity. For single-word topics or ambiguous terms, it may pick the wrong workflow block.

**Recommended fix:** Use embedding similarity for workflow selection when topic is provided, falling back to keyword overlap only when embedding is unavailable.

**P2-5: Institutional knowledge adapter URL is hardcoded**

`institutional.py` hardcodes `http://growdirect_memory_bus:8003/mcp/v1/tools/memory_recall`. This assumes a Docker network hostname that will not resolve in all deployment topologies (e.g., AWS ECS with service discovery).

**Recommended fix:** Make the Memory Bus URL configurable via environment variable.

**P2-6: Session ID format diverged between SDD and code**

The original SDD documented session ID format as `alx-YYYYMMDD-HHMMSS-{6 hex chars}`. The actual code uses `alx-{uuid4_hex[:12]}`, which produces a 12-character hex string without date components. The format is functional but differs from the documented contract.

**Recommended fix:** Update documentation to match code (already done in this SDD), or update code to match the more informative date-based format.

## Production Readiness Checklist

- [ ] PII encrypted at rest — `content` and `summary` fields contain organizational knowledge with internal details; currently plaintext. Low risk (no customer PII) but should be encrypted for compliance.
- [ ] Secrets in AWS Secrets Manager (not .env) — `MCP_API_KEY` and `DATABASE_URL` currently in Docker Compose env vars with committed defaults.
- [ ] Health check endpoint responds — Docker healthcheck works (406 from MCP protocol). No dedicated `/health` endpoint on the FastMCP server.
- [ ] Audit logging for sensitive operations — No audit trail for memory store/recall/session operations.
- [ ] Data retention policy implemented — No retention, no archival, no purge.
- [ ] Rate limiting on public endpoints — No rate limiting on MCP tool calls.
- [ ] Error responses don't leak internals — Auth errors reveal configuration state; store errors may leak exception details.
- [ ] ILIKE metacharacter escaping — Tier 3 recall and startup context assembly vulnerable to ILIKE pattern manipulation.
- [ ] Auth bypass removed — `MCP_AUTH_DISABLED` env var allows complete auth bypass.
- [ ] Default API key removed — `growdirect-memory-dev-key` committed to repo as fallback.
- [ ] Embedding model tracking — No per-memory record of which model generated the embedding.
- [ ] TLS in production — Plain HTTP on port 8003 within Docker network.
