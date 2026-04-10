# Architecture

## Platform Overview

Canary LP is a 7-layer distributed system for AI-powered loss prevention, built on 11 bounded service domains exposed through 12 MCP servers (84 tools total). The platform processes Square webhook events in real time, evaluates transactions against 26 detection rules, and surfaces actionable insights to merchants through an AI-powered assistant.

**7-Layer Stack:**

| Layer | Name | Components |
|-------|------|------------|
| 0 | Infrastructure | Docker Compose (local), ECS Fargate (cloud target) |
| 1 | Data | PostgreSQL 17 (4 databases), Valkey 8 (streams + cache), PgBouncer |
| 2 | Domain Services | 12 MCP servers, one per bounded context |
| 3 | Agent Mesh | Owl, ALX, Chirp, Fox, Inscription, Condor (6 agents) |
| 4 | Orchestration | Mastra (TypeScript) agent workflows |
| 5 | Gateway | Kong (self-hosted) / AWS API Gateway |
| 6 | Frontend | Next.js App Router + RSC + PWA (target), Flask/Jinja2 (current) |
| 7 | Protocol | elJeffe / RaaS: Bitcoin L1 inscription + Avalanche L2 naming |

**11 Service Domains:**

| # | Domain | Purpose | MCP Tools |
|---|--------|---------|-----------|
| 1 | Identity | Merchants, users, roles, Square OAuth, tenant context | 6 |
| 2 | Webhook Pipeline (TSP) | Webhook intake, HMAC validation, stream processing, parsing | 6 |
| 3 | Chirp | Stateless detection rules, threshold config, sensitivity presets | 10 |
| 4 | Alert | Alert lifecycle, history, impact scoring, notifications | 6 |
| 5 | Owl | AI chat, personalities, MCP tools, merchant memory, reports | 8 |
| 6 | Fox | Case management, evidence locker, hash-chained timeline | 8 |
| 7 | Analytics | Dashboard metrics, heatmaps, velocity baselines, scorecards | 7 |
| 8 | ALX | Institutional memory (pgvector semantic search, 954+ memories) | 7 |
| 9 | RaaS | Namespace resolution, merchant onboarding, source registration | 7 |
| 10 | Ops | Health check runner, simulator, ops console, Chirp Lab | 8 |
| 11 | UI/BFF | Desktop + mobile rendering, feature flags, config | 4 |
| 12 | Condor | Industry benchmarks, SDK currency, tooling landscape, regulatory | 7 |

**MCP as Universal Integration Protocol:** Every domain exposes `GET /manifest`, `GET /tools`, `POST /tools/<name>`, and `GET /health`. The shared base kit (`canary/mcp/`) stamps these endpoints via `create_mcp_blueprint()`. Handler signature: `(params: Dict, context: Dict) -> Dict`. Auth: JWT on tool invocation; manifest/tools/health are public.

**Decomposition Strategy:**

| Phase | Status | Scope |
|-------|--------|-------|
| 0 | Done | Shared MCP base kit (`canary/mcp/`) |
| 1 | Done | Owl + ALX migrated to shared base; dashboard helpers to service layer |
| 2 | Done (Mar 2026) | 5 MCP servers: analytics, fox, chirp, alert, identity (37 tools) |
| 3 | Done (Mar 2026) | 5 MCP servers: tsp, ops, bff, raas, condor (32 tools) |
| 4 | Next | Container extraction: standalone agents, API gateway, Mastra, Next.js |

**Bounded Context Rules:** Every file maps to exactly one domain. No orphans, no shared ownership. Domains communicate via sync function calls (today) and MCP tool invocation over HTTP (target). Inter-domain data flows follow strict contracts documented in the domain map.

**Knowledge Flow:** Institutional knowledge flows one-way from ALX memory store (954+ pgvector-embedded memories) through the Owl institutional adapter into merchant-facing responses. SDDs, process architecture, detection patterns, and 30 years of retail LP ontology are embedded and searchable. Owl reads from ALX but never writes to it.

**Source SDDs:** SDD-057 (Service Domain Map), SDD-059 (Modern Architecture Blueprint).

---

## Infrastructure

Canary runs on a single PostgreSQL 17 instance with four databases, Valkey 8 for caching and streams, and Docker Compose for local development. Cloudflare Tunnel provides external access with zero inbound ports.

**Database Architecture:**

| Database | Schema | Tables | Access Pattern | Write Pattern |
|----------|--------|--------|---------------|---------------|
| `canary_app` | app | ~40 | Read/write | CRUD with soft delete + audit trail |
| `canary_sales` | sales | ~19 | Write-once, read-many | IMMUTABLE (PostgreSQL trigger-enforced) |
| `canary_metrics` | metrics | ~20 | Write-periodically, read-often | Aggregation (fully re-derivable) |
| `growdirect_memory` | memory | ~2 | Read/write | pgvector embeddings (768-dim, HNSW cosine), via MCP server (GRO-172) |

**Session Factory:** `get_db_session(db_name)` routes to the correct database by string key (`app`, `sales`, `metrics`, `memory`). Sessions are request-scoped in the Flask context, committed on success, rolled back on exception. `init_engines(app)` initializes the engine pool from Flask config. All databases share one PostgreSQL instance.

**Valkey Cache Layer (8 databases):**

| Namespace | Key Pattern | TTL | Purpose |
|-----------|------------|-----|---------|
| Thresholds | `chirp:thresholds:{merchant_id}:{rule_id}` | 300s | Chirp threshold cache |
| Velocity | `chirp:velocity:{merchant_id}:{rule_id}:{window}` | varies | Tier 2 windowed counters |
| Rate limits | `ratelimit:{scope}:{identifier}` | 60s | API rate limiting |
| Sessions | `session:{session_id}` | 3600s | Flask session data |
| Health check | `hc:session:{session_id}` | 7200s | HC session state |
| Notifications | `notif:cap:{merchant_id}:{window}` | varies | Notification rate caps |

Cache invalidation: threshold cache invalidated on config write/delete; session cache on logout/timeout; all caches `FLUSHDB` on container restart (acceptable: all re-derivable).

**Python Version:** 3.12 — aligned across Dockerfile, CI, and CLAUDE.md. All type hints use `Mapped[]` syntax (SQLAlchemy 2.0).

**Docker Compose Dev Stack:** Single compose file `devops/docker-compose.localhost.yml`. Flask (Python 3.12 + Gunicorn, 1 worker, 4 threads, port 5001), PostgreSQL 17, Valkey 8, pgAdmin. Source is volume-mounted (`DEV_RELOAD=true`): file saves are live, Gunicorn auto-reloads Python. Rebuild only for new pip packages, Dockerfile, or compose changes. Entry: `./devops/scripts/dev.sh up`.

**Alembic Migration Framework (3 chains):**

| Chain | Config | Tables |
|-------|--------|--------|
| `canary_app` | `canary/migrations/alembic.ini` | 17+ migrations applied |
| `canary_sales` | `canary/migrations/sales/alembic.ini` | Immutable event stream tables |
| `canary_metrics` | `canary/migrations/metrics/alembic.ini` | Star schema tables |

Migration naming: `NNN_groXXX_feature_name.py`. Revision IDs chain sequentially. PostgreSQL transactional DDL means failed migrations roll back entirely. `alembic_version` column widened to `varchar(128)`.

**Cloudflare Tunnel:** Outbound-only encrypted tunnels to Cloudflare edge. No inbound ports on DSR-250 router. Dev: `dev.growdirect.app` (Mac Mini, local config). QA: `qa.growdirect.app` (iMac, token-based Docker service). Cloudflare handles TLS termination, DDoS protection, and WAF.

**Deploy Pipeline (dev -> QA -> prod):**

| Script | Purpose |
|--------|---------|
| `canary_deploy.sh --full` | Pull, build, migrate, test, deploy (local Mac Mini) |
| `remote_deploy.sh` | SSH push to QA iMac, same sequence |

Test gates enforce: unit tests block merge, integration tests block QA push, smoke tests run after every rebuild. Docker garbage collection after every rebuild.

**Ollama (native, not containerized):** qwen3:14b (9.3GB Q4_K_M) for chat/analysis, nomic-embed-text for embeddings. Runs on host at port 11434.

**Crypto Module (`canary/utils/crypto.py`, GRO-248):**
- AES-256-GCM encryption at rest for OAuth tokens and secrets.
- Key: `CANARY_ENCRYPTION_KEY` env var (base64-encoded 32 bytes).
- Prefix scheme: `"GCM:"` (current), `"UNENCRYPTED:"` (testing stubs), no prefix (legacy Fernet).
- Hard fail in production: missing key or missing `cryptography` package raises `RuntimeError`. Plaintext fallback only when `CANARY_ENV=testing`.
- Transparent Fernet-to-GCM migration on next token store.

**Notification Dispatcher (`canary/services/notification_dispatcher.py`, GRO-254):**
- Routes alert notifications to channels: in-app (live), email (stub), SMS (stub).
- Called from `rule_engine._write_alerts()` after alert flush.
- Per-rule toggle: `MerchantRuleConfig.notify_enabled` — if `False`, notification suppressed before any filter.
- Filters (applied in order): severity threshold (`notif_severity_threshold`), quiet hours (`notif_quiet_start`/`notif_quiet_end`, wraps midnight), daily limit (`notif_daily_limit`, default 50).
- Email/SMS stubs log `STATUS_SUPPRESSED` with reason until providers (SendGrid/SES, Twilio) are wired.
- Every dispatch attempt (sent or suppressed) logged to `NotificationLog` with channel, status, severity, and failure reason.

**Source SDDs:** SDD-045 (DB Session Factory), SDD-047 (Valkey Cache), SDD-049 (Docker Compose), SDD-050 (Alembic Migrations), SDD-051 (Cloudflare Tunnel), SDD-052 (Deploy Pipeline).

---

## Patterns

Canary enforces consistent patterns across all models, blueprints, and tests through shared base classes, mixins, and a three-layer test strategy.

**Base Classes (SQLAlchemy 2.0 `Mapped[]` syntax throughout):**

| Base | Database | Purpose |
|------|----------|---------|
| `AppBase` | canary_app | Operational models (merchants, alerts, cases) |
| `SalesBase` | canary_sales | Transaction log (immutable event stream) |
| `MetricsBase` | canary_metrics | Analytics star schema (re-derivable) |

No legacy `declarative_base`. All models use SQLAlchemy 2.0 `Mapped[]` column syntax.

**GSLM Mixins (Get/Save/List/Merge):**

| Mixin | Columns | Used By | Purpose |
|-------|---------|---------|---------|
| `TenantMixin` | `merchant_id` (String(36), indexed) | 18 models | Multi-tenant isolation key |
| `AuditMixin` | `created_at`, `updated_at`, `created_by`, `modified_by` | 29 models | Standard audit timestamps and attribution |
| `SoftDeleteMixin` | `db_status` (draft/active/archived), `db_effective_from`, `db_effective_to` | 9 models | Soft delete with effective dating (GSLM pattern) |
| `ImmutableMixin` | (trigger-enforced) | All canary_sales tables | PostgreSQL `BEFORE UPDATE OR DELETE` trigger blocks mutations |

**Data Mutation Patterns:**

| Pattern | Scope | Enforcement |
|---------|-------|-------------|
| WRITE-ONCE IMMUTABLE | canary_sales (all 19 tables) | PostgreSQL BEFORE trigger raises IMMUTABILITY VIOLATION |
| APPEND-ONLY | Alert, AlertHistory, AuditLog, NotificationLog | Application convention (future: trigger) |
| SOFT DELETE (GSLM) | 9 app models (Merchant, Location, Employee, etc.) | SoftDeleteMixin columns |
| OPERATIONAL | All other app models | Standard CRUD with audit trail |

Corrections to immutable data use compensating INSERTs, not updates. `generate_uuid()` returns `str(uuid.uuid4())` as default for all PK columns.

**Blueprint Route Registry:** All MCP servers use the shared base kit `create_mcp_blueprint()` factory, which stamps four endpoints: `GET /manifest`, `GET /tools`, `POST /tools/<name>` (JWT-required), `GET /health`. Response envelope: `{"tool": name, "ok": true/false, "result"|"error": ..., "timestamp": ISO}`.

**Flask Extensions (`canary/extensions.py`):**

| Extension | Instance | Purpose |
|-----------|----------|---------|
| Flask-WTF CSRFProtect | `csrf` | CSRF token generation/validation on POST/PUT/DELETE |
| Flask-Limiter | `limiter` | Rate limiting per-IP and per-merchant |
| Flask-Talisman | `talisman` | Security headers (HSTS, CSP, X-Frame-Options) |

API endpoints (JWT-authenticated) are CSRF-exempt (token-based auth is CSRF-safe). Webhook endpoints are CSRF-exempt (HMAC-verified). Talisman runs with `force_https=False` because Cloudflare handles TLS.

**Test Strategy (3 layers):**

| Layer | Location | Runner | Count | Gate |
|-------|----------|--------|-------|------|
| Unit | `tests/unit/` | `pytest tests/unit/` | 1,425+ | CI blocks merge |
| Integration | `tests/integration/` | `pytest tests/integration/ -m postgres` | ~50 | Must pass before QA push |
| Smoke | `tests/smoke/` | `pytest tests/smoke/` | ~10 | Must pass after every rebuild |

**Unit tests** (Layer 1): test business logic in isolation. Mock all I/O (DB, HTTP, Valkey). ~30 seconds runtime. If a test needs PostgreSQL, it goes to Layer 2.

**Integration tests** (Layer 2): verify ORM mappings, migrations, triggers (immutability), cross-table queries against real PostgreSQL. Transaction rollback per test, no pollution. ~2 minutes runtime.

**Smoke tests** (Layer 3): verify deployed stack is functional. Hit `/health`, key endpoints, check response codes. ~10 seconds runtime.

**Test conventions:** No `@pytest.mark.skip` on empty files (dead tests get deleted). Tests organized by layer, not sprint. Every feature gets a unit test. Commit after each green phase.

**Source SDDs:** SDD-048 (Flask Extensions/CSRF), SDD-053 (Test Strategy), SDD-054 (Base Mixins & Model Patterns).

---

## Target State

The target-state architecture extracts domains from the Flask monolith into standalone agent containers, adds an API gateway, replaces Jinja2 with Next.js, and introduces Mastra for multi-step agent orchestration. The same MCP tool contracts stay — transport changes from in-process calls to HTTP.

**API Gateway (Phase 2: Kong self-hosted, Phase 3: AWS API Gateway):**

The gateway externalizes cross-cutting concerns into a single auditable choke point:
- TLS termination (Cloudflare Phase 1, ALB Phase 2+)
- JWT validation before forwarding to domain services
- HMAC-SHA256 verification for Square webhooks
- Rate limiting per merchant tier (Open 100/min, Strict 10/min, Standard 60/min, Burst 300/min, Internal 1000/min)
- Product tier multipliers: Health Check 1x, Sentinel 2x, Full RaaS 5x
- Path-based routing: `/owl/*` -> canary-owl:8001, `/api/chirp/*` -> canary-chirp:8003, etc.
- CORS enforcement (no wildcards in production)
- SSE proxy for streaming AI responses, WebSocket upgrade (Phase 2+)
- Request/response logging with correlation IDs

Auth evolution: Flask middleware (now) -> Keycloak OIDC (self-hosted) -> AWS Cognito (cloud). All produce identical JWT payloads: `{sub, merchant_id, organization_id, roles, iss, exp}`. Service-to-service auth uses short-lived JWTs (5-min expiry, daily rotation).

**Next.js App Router Frontend:**

Mobile-first PWA with React Server Components (RSC). App Router structure: `(auth)/` for OAuth, `(merchant)/` for the main shell with chirps (alert feed), owl (The One Thing + chat), vault (Fox cases), dashboard (analytics), and settings (thresholds). Server Actions invoke MCP tools directly. Client Components handle streaming AI chat via `useChat()` from Vercel AI SDK.

Real-time capabilities: SSE replaces pull-to-refresh for alert push, token-by-token streaming from Ollama through Owl agent to browser. PWA service worker caches alert feed for offline viewing, push notifications for critical/high alerts. Design tokens port from current CSS custom properties (`--color-*`, `--bg-*`, `--text-*`) to Tailwind CSS with custom theme.

**Mastra Orchestration:**

Mastra (TypeScript) connects to all 12 MCP servers via `MCPClient` and defines multi-step workflows:

| Workflow | Steps | Key Agents |
|----------|-------|------------|
| Health Check Pipeline | profile select -> OAuth/demo -> ingest -> chirp sweep -> heartbeat -> report -> merchant action -> persist memory | identity, tsp, chirp, owl, alx |
| Alert Lifecycle | alert created -> owl evaluate -> surface to merchant -> merchant action -> execute -> log outcome | chirp, owl, alert, alx |
| Case Investigation | case opened -> gather evidence -> owl analysis -> present findings -> escalate/close | fox, alert, analytics, owl |

Human-in-the-loop: Mastra pauses workflows at merchant decision points and resumes via Server Actions. Workflow state persists across page reloads.

**Process Ontology Alignment:**

Canary's detection rules and scoring methods implement a 30-year retail operations process ontology, not an ad hoc feature set:

| Source | Year | Canary Mapping |
|--------|------|----------------|
| Staples Level 2 (Tom Hoover / PwC) | 1996 | 26 processes, A/R/M/E accountability -> Chirp rule categories |
| Tesco Operating Model v1.24 | 2007 | ~100 processes, 13 value chain categories -> KPI framework |
| Beck & Peacock "New Loss Prevention" | 2009 | Operational failure taxonomy (Fig 7.1) -> detection philosophy |
| Speights, Downs & Raz | 2017 | Statistical methods -> velocity z-scores, baseline modeling |

Lineage: STPL (1996) -> Tesco (2007) -> Beck & Peacock (2009) -> Speights (2017) -> Canary Data Model / Secure EBR (2004-2020) -> elJeffe Protocol -> Canary LP (2025-present).

The 6-layer scoring stack maps directly: per-transaction scoring (Sales Audit), per-alert impact (Performance Monitoring), per-period heatmap (Performance Levers), time-series velocity (XPLOSS/Poisson), aggregate health (Heartbeat/CDSS), entity risk (SRA Scorecards). SRA (Shrink Risk Assessment) unifies refund amount + cash variance + discount total as the full operational failure surface, not just theft.

**Container Extraction (Phase 4):**

Each agent becomes an independent container: MCP server (my tools) + MCP client (consume others) + event bus consumer + service logic (pure Python) + PgBouncer sidecar. AI agents (Owl, ALX, Condor) co-locate with Ollama on the Mac Studio (192GB unified memory). Deterministic agents (Chirp, Fox, Alert) stay on the Mac Mini with the database. Agent discovery via Valkey hash (`canary:registry:<agent>`), 30-second heartbeat interval.

Infrastructure phases: Phase 1 (local lab, ~$10/mo electricity), Phase 2 (hybrid cloud: RDS + local inference, ~$100-150/mo), Phase 3 (full AWS: ECS Fargate + Bedrock fallback, ~$205/mo without GPU).

**Source SDDs:** SDD-059 (Modern Architecture Blueprint), SDD-060 (Process Ontology Alignment), SDD-062 (API Gateway).
