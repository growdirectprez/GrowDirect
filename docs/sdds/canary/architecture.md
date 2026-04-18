# Canary Architecture

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Type:** Platform Service (Canary index SDD)
**Last reviewed:** 2026-04-13
**Source SDDs:** SDD-045, SDD-047, SDD-048, SDD-049, SDD-050, SDD-051, SDD-052, SDD-053, SDD-054, SDD-057, SDD-059, SDD-060, SDD-062

---

## Purpose

Canary LP is a 7-layer distributed system for AI-powered loss prevention, built on 11 bounded service domains exposed through 12 MCP servers (84 tools total). The platform processes Square webhook events in real time, evaluates transactions against 26 detection rules, and surfaces actionable insights to merchants through an AI-powered assistant.

This is the **Canary index SDD** -- it documents the platform topology, startup order, service dependencies, cross-boundary data flows, and links to all domain-specific SDDs. Individual domain behavior is documented in its own SDD.

---

## Dependencies

### Shared Infrastructure (external -- started separately)

These services run from `~/GrowDirect/devops/docker-compose.yml` on the `growdirect` network:

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| PostgreSQL 17 | `growdirect_postgres` | 5432 | All databases (canary, canary_test, growdirect_memory) |
| Valkey 8 | `growdirect_valkey` | 6379 | Sessions, cache, rate limiting, TSP streams |
| pgAdmin | `growdirect_pgadmin` | 5050 | DB administration UI |
| Ollama | `growdirect_ollama` | 11434 | LLM inference (qwen3:14b) + embeddings (qwen3-embedding:8b) |
| Memory Bus | `growdirect_memory_bus` | 8003 | Platform session memory MCP (FastMCP, pgvector) |

### Canary Application Stack

These services run from `Canary/devops/docker-compose.localhost.yml` (dev) or `docker-compose.qa.yml` (QA):

| Service | Container | Port | Image | Purpose |
|---------|-----------|------|-------|---------|
| Flask | `canary_flask` | 5001 | `canary-flask` | Monolith: 29 blueprints, 12 MCP servers, all business logic |
| nginx | `canary_localhost_nginx` | 80, 443 | `nginx:1.25-alpine` | TLS termination (mkcert), reverse proxy |
| TSP Sub1 (Seal) | `canary_localhost_tsp_sub1` | -- | `canary-flask` | Valkey stream consumer: hash-seal incoming events |
| TSP Sub2 (Parse) | `canary_localhost_tsp_sub2` | -- | `canary-flask` | Valkey stream consumer: parse + route + feed detection stream |
| TSP Sub3 (Merkle) | `canary_localhost_tsp_sub3` | -- | `canary-flask` | Valkey stream consumer: Merkle tree construction |
| TSP Sub4 (Detect) | `canary_localhost_tsp_sub4` | -- | `canary-flask` | Valkey stream consumer: Chirp rule evaluation |
| Owl MCP | `canary_localhost_owl_mcp` | 8001 | `canary-owl-mcp` | Standalone AI/chat MCP server (proof of concept extraction) |
| QA Agent | `canary_localhost_qa_agent` | 8002 | `canary-qa-agent` | Claude Agent SDK sidecar for ops QA (uvicorn) |
| nginx-wait | `canary_localhost_infra_check` | -- | `busybox` | Sentinel: waits for shared infra before Flask starts |

### Enterprise Stack (QA / future production)

`Canary/devops/docker-compose.canary.yml` defines the full enterprise stack (self-contained, does not use growdirect shared infra):

| Service | Port | Profile | Purpose |
|---------|------|---------|---------|
| PostgreSQL 17 | 5432 | core | Dedicated Canary instance |
| Valkey 8 | 6379 | core | Dedicated cache/broker |
| PgBouncer | 6432 | core | Connection pooling (transaction mode, max 200 clients) |
| Flask | 5001 | core | Business logic (4 workers in enterprise mode) |
| Apache Superset 6 | 8088 | core | Analytics dashboards |
| Apache Airflow 3 | 8793 | core | ETL orchestration, Chirp sweeps |
| Keycloak 26 | 8080 | qa | OIDC identity provider |
| Hasura v2 CE | 8081 | qa | GraphQL/REST auto-generated API |
| Directus 11 | 8055 | qa | Internal admin panel |
| nginx | 80 | qa | Reverse proxy |

### External APIs

| API | Auth Method | Purpose |
|-----|------------|---------|
| Square Connect API | OAuth 2.0 (AES-256-GCM encrypted tokens) | Merchant data, transactions, webhooks |
| Square Webhooks | HMAC-SHA256 signature validation | Real-time event push |

---

## Startup Order and Dependency Graph

### Dev Stack (localhost)

```
1. growdirect_postgres  (healthcheck: pg_isready)
2. growdirect_valkey    (healthcheck: valkey-cli ping)
   ├── growdirect_pgadmin    (depends: postgres healthy)
   ├── growdirect_ollama     (independent)
   └── growdirect_memory_bus (depends: postgres healthy)
3. canary_localhost_infra_check  (nginx-wait: nc -z postgres 5432 && nc -z valkey 6379)
4. canary_flask  (depends: nginx-wait, healthcheck: HTTP GET /health)
   Boot phases inside Flask (wsgi.py):
     Phase 1: SQLAlchemy session factory init (consolidated schema)
     Phase 2: Security extensions (CSRF, Talisman, Rate Limiter, Flask-Session)
     Phase 3: Blueprint registration (29 blueprints, resilient -- each try/except)
     Phase 4: TSP consumer group init, detection rule seeding, audit chain verification
     Phase 5: Boot summary log
5. canary_localhost_nginx  (depends: flask healthy)
6. canary_localhost_tsp_sub{1,2,3,4}  (depends: flask healthy)
7. canary_localhost_owl_mcp  (depends: flask healthy)
8. canary_localhost_qa_agent (depends: flask healthy)
```

### Enterprise Stack

```
1. canary_postgres      (healthcheck: pg_isready)
2. canary_valkey         (healthcheck: valkey-cli ping)
3. canary_pgbouncer      (depends: postgres healthy)
4. canary_flask          (depends: postgres healthy + valkey healthy)
5. canary_airflow_scheduler (depends: postgres healthy)
   canary_airflow_web      (depends: postgres healthy)
   canary_superset          (depends: postgres healthy + valkey healthy)
6. [qa profile] keycloak → hasura → directus → nginx
```

### Failure Cascade

| If this goes down... | ...these break |
|---------------------|---------------|
| PostgreSQL | Everything (Flask degrades to health-only mode, TSP consumers stall, Owl MCP returns errors) |
| Valkey | Sessions lost, rate limiting fails open, TSP stream processing halts, Chirp threshold cache stale |
| Ollama | Owl AI chat returns errors, ALX embeddings fail, analytics AI features unavailable |
| Flask | All HTTP endpoints down; TSP consumers continue processing independently but cannot write alerts without Flask health |
| nginx | External HTTPS access lost; direct Flask :5001 still reachable |
| Any TSP consumer | That processing stage stalls; upstream/downstream consumers continue; dead letter stream catches failures |

---

## Data Flow & PII Map

### Database Architecture

| Database | Schema | Tables | Write Pattern |
|----------|--------|--------|---------------|
| `canary` | `app` | ~40 | CRUD with soft delete + audit trail |
| `canary` | `sales` | ~19 | IMMUTABLE (PostgreSQL trigger-enforced, no UPDATE/DELETE) |
| `canary` | `metrics` | ~20 | Aggregation (fully re-derivable from sales) |
| `growdirect_memory` | `memory` | ~2 | pgvector embeddings (1024-dim HNSW cosine) |

Session factory: single engine, three schemas. `DatabaseSessionFactory` in `canary/db/session_factory.py` uses `scoped_session` with RLS context bridge -- sets `current_merchant_id` via `set_current_merchant(:mid)` at transaction start.

### PII Classification (Platform-Level Cross-Boundary Flows)

| Data Category | Fields | Classification | Storage | Encryption | Crosses Boundary To |
|--------------|--------|----------------|---------|------------|-------------------|
| OAuth tokens | `access_token`, `refresh_token` | **restricted** | `app.merchant_sources` | AES-256-GCM (`crypto.py`) | Square API (HTTP), Owl MCP |
| Merchant identity | `business_name`, `merchant_id` | internal | `app.merchants` | plaintext | All services, UI, analytics |
| Square merchant ID | `square_merchant_id` | internal | `app.merchant_sources` | plaintext | TSP pipeline, webhooks |
| Transaction data | `customer_id`, `tender_id`, amounts | internal | `sales.*` (immutable) | plaintext | Chirp (detection), Owl (analysis), Fox (cases) |
| Employee data | `employee_id`, `first_name`, `last_name` | **sensitive** | `app.employees` | plaintext | Chirp alerts, Fox cases, analytics |
| Location data | `address`, `name` | internal | `app.locations` | plaintext | UI, analytics |
| Alert content | `description`, linked txn/employee IDs | internal | `app.alerts` | plaintext | Notifications (email stub), Fox cases |
| Case evidence | screenshots, notes, txn references | internal | `app.fox_cases` + evidence locker | plaintext | Owl analysis |
| Session data | `session_id`, `merchant_id` | internal | Valkey DB 0 | plaintext in Valkey | Flask request context |
| AI chat history | merchant questions, Owl responses | internal | Valkey (ephemeral) + ALX memory | plaintext | Ollama inference |
| Webhook payloads | raw Square event JSON (may contain customer PII) | **sensitive** | `sales.raw_webhooks` | plaintext | TSP Sub1-4 |
| Detection results | rule match details, severity scores | internal | `app.alerts`, `metrics.*` | plaintext | UI, notifications |
| Notification log | channel, status, recipient metadata | internal | `app.notification_log` | plaintext | Email (stub), SMS (stub) |

### Data Flow Diagram

```
Square Webhooks (HMAC-SHA256 validated)
  │
  ▼
Flask /webhooks/square (TSP publisher)
  │
  ├──▶ Valkey stream canary:events
  │     │
  │     ├──▶ Sub1 (Seal): hash + write to sales.raw_webhooks
  │     ├──▶ Sub2 (Parse): parse JSON → sales.transactions + emit canary:detection
  │     ├──▶ Sub3 (Merkle): build Merkle tree for integrity chain
  │     └──▶ Sub4 (Detect): Chirp rule evaluation → app.alerts → notifications
  │
  ├──▶ Owl MCP (:8001) → Ollama (qwen3:14b) → AI chat responses
  │     └──▶ ALX Memory (pgvector) → institutional knowledge retrieval
  │
  └──▶ Flask UI (Jinja2) → Browser
        ├── Dashboard (analytics from metrics.*)
        ├── Chirps (alert feed from app.alerts)
        ├── Fox (cases from app.fox_cases)
        └── Owl (AI chat, SSE streaming)
```

---

## API Contract

### MCP Server Registry (12 servers, 84 tools)

All MCP servers use `create_mcp_blueprint()` which stamps four endpoints per domain:

- `GET /{prefix}/manifest` -- server manifest (JWT required, 100/hr)
- `GET /{prefix}/tools` -- list available tools (JWT required, 100/hr)
- `POST /{prefix}/tools/<name>` -- invoke a tool (JWT required, 1000/hr)
- `GET /{prefix}/health` -- service health (public, no auth)

Response envelope: `{"tool": name, "ok": true/false, "result"|"error": ..., "timestamp": ISO}`

| # | Domain | Prefix | Tools | SDD | Description |
|---|--------|--------|-------|-----|-------------|
| 1 | Identity | `/identity` | 6 | [[docs/sdds/canary/identity|Identity]] | Merchants, users, roles, Square OAuth, tenant context |
| 2 | TSP | `/tsp` | 6 | [[docs/sdds/canary/tsp|TSP]] | Webhook intake, stream processing, parsing |
| 3 | Chirp | `/chirp` | 10 | [[docs/sdds/canary/chirp|Chirp]] | Detection rules, threshold config, sensitivity presets |
| 4 | Alert | `/alert` | 6 | [[docs/sdds/canary/alert|Alert]] | Alert lifecycle, history, impact scoring, notifications |
| 5 | Owl | `/owl` | 8 | [[docs/sdds/canary/owl|Owl]] | AI chat, personalities, MCP tools, merchant memory |
| 6 | Fox | `/fox` | 8 | [[docs/sdds/canary/fox|Fox]] | Case management, evidence locker, hash-chained timeline |
| 7 | Analytics | `/analytics` | 7 | [[docs/sdds/canary/analytics|Analytics]] | Dashboard metrics, heatmaps, velocity baselines |
| 8 | ALX | `/alx` | 7 | [[docs/sdds/canary/alx|ALX]] | Institutional memory (pgvector, 954+ memories) |
| 9 | RaaS | `/raas` | 7 | [[docs/sdds/canary/raas|RaaS]] | Namespace resolution, merchant onboarding |
| 10 | Ops | `/ops` | 8 | [[docs/sdds/canary/ops|Ops]] | Health check runner, simulator, Chirp Lab |
| 11 | BFF | `/bff` | 4 | [[docs/sdds/canary/ui-bff|UI/BFF]] | Desktop + mobile rendering, feature flags |
| 12 | Condor | `/condor` | 7 | -- | Industry benchmarks, regulatory intelligence |

Additional MCP servers (non-domain, standalone):
- **Atlas** (`/atlas`) -- diagram service (GRO-323)
- **Owl MCP** (`:8001`) -- standalone extraction of Owl, same tools as monolith `/owl/*`
- **QA Agent** (`:8002`) -- Claude Agent SDK sidecar, proxied via `/ops/qa/chat`

### Blueprint Registry (29 blueprints in wsgi.py)

| Blueprint | Prefix | Auth | CSRF Exempt | Description |
|-----------|--------|------|:-----------:|-------------|
| `health_bp` | `/health` | None | Yes | Health checks |
| `auth_bp` | `/auth` | Session | No | Keycloak auth |
| `webhooks_tsp_bp` | `/webhooks` | HMAC | Yes | Square webhook receiver |
| `fox_bp` | `/api/fox` | JWT | Yes | Fox case CRUD |
| `alerts_bp` | `/api/alerts` | JWT | Yes | Alert CRUD |
| `chirp_bp` | `/api/chirp` | JWT | Yes | Chirp config CRUD |
| `square_oauth_bp` | `/oauth` | Session | Yes | Square OAuth flow |
| `merchants_bp` | `/api/merchants` | JWT | Yes | Merchant CRUD |
| `locations_bp` | `/api/locations` | JWT | Yes | Location CRUD |
| `employees_bp` | `/api/employees` | JWT | Yes | Employee CRUD |
| `analytics_bp` | `/api/analytics` | JWT | Yes | Analytics queries |
| `receipt_tsp_bp` | `/api/receipt` | JWT | Yes | Receipt proof |
| `square_explorer_bp` | -- | JWT | Yes | Square Capability Explorer |
| `views_bp` | -- | Session | No | Desktop UI (Jinja2) |
| `devops_monitor_bp` | `/devops` | JWT | Yes | DevOps pipeline monitor |
| `ops_console_bp` | `/ops` | JWT | Yes | Operations console |
| `charts_bp` | `/api/charts` | JWT | Yes | Dashboard chart APIs |
| 12 MCP blueprints | `/{domain}` | JWT | Yes | See MCP registry above |

---

## Operations

### Startup Sequence

See "Startup Order and Dependency Graph" above. Key details:

1. **Shared infra must be running first.** `cd ~/GrowDirect/devops && docker compose up -d`
2. **Flask boot is resilient.** Each blueprint loads independently via try/except. A missing import degrades one domain, not the whole app. Flask can run in "health-only mode" if the database is unreachable.
3. **TSP consumer groups** are initialized during Flask boot (Phase 4). If Valkey is unreachable, consumers will not receive events until groups are manually created.
4. **Detection rules** are seeded on first boot (Phase 4b, idempotent).
5. **Audit hash chain** is verified on startup (Phase 4c). A tampered chain logs `CRITICAL` but does not block startup (`raise_on_tamper=False`).

### Health Checks

| Service | Endpoint | Method | Interval | Timeout |
|---------|----------|--------|----------|---------|
| Flask | `http://localhost:5001/health` | HTTP GET | 10s | 5s |
| nginx | `http://localhost/nginx-health` | wget | 10s | 3s |
| TSP Sub{1-4} | `devops/scripts/tsp_healthcheck.py` | CMD | 15s | 5s |
| Owl MCP | `http://localhost:8001/health` | HTTP GET | 10s | 5s |
| QA Agent | `http://localhost:8002/health` | HTTP GET | 10s | 5s |
| PostgreSQL | `pg_isready` | CMD-SHELL | 5s (shared) / 10s (enterprise) | 5s |
| Valkey | `valkey-cli ping` | CMD | 5s (shared) / 10s (enterprise) | 5s |

### Failure Modes

| Failure | Detection | Behavior | Recovery |
|---------|-----------|----------|----------|
| PostgreSQL down | Flask health returns 503 | Flask enters health-only mode; CRUD endpoints return 500 | Auto-reconnect via `pool_pre_ping=True` |
| Valkey down | Rate limiting fails open | Sessions lost (users re-auth); TSP streams stall; threshold cache stale but usable (300s TTL) | Consumers retry on reconnect |
| Ollama down | Owl health returns unhealthy | AI chat returns error; embeddings fail; detection rules continue (no AI dependency) | Restart Ollama container |
| TSP consumer crash | Docker healthcheck fails | Container restarts (unless-stopped); unprocessed messages remain in stream | Consumer resumes from last ACK |
| Blueprint import failure | Logged at startup | Single domain degraded; all other domains continue | Fix import, restart Flask |
| Audit chain tampered | `CRITICAL` log on startup | Continues running (fail-open) | Investigate chain, rebuild if needed |

### Configuration (Environment Variables)

| Variable | Required | Default | Purpose |
|----------|:--------:|---------|---------|
| `SECRET_KEY` | Prod: Yes | `dev-fallback-not-for-production` | Flask session signing |
| `CANARY_ENV` | No | `development` | Environment: development/testing/production |
| `CANARY_DB_URL` | Yes | -- | PostgreSQL connection string |
| `VALKEY_URL` | Yes | -- | Valkey connection string (DB 0 for Canary) |
| `CANARY_ENCRYPTION_KEY` | Prod: Yes | -- | AES-256-GCM key (base64-encoded 32 bytes) |
| `CANARY_HOST` | No | -- | Hostname for Talisman force_https decision |
| `SQUARE_APPLICATION_ID` | Yes | -- | Square OAuth app ID |
| `SQUARE_APPLICATION_SECRET` | Yes | -- | Square OAuth secret |
| `SQUARE_WEBHOOK_SIGNATURE_KEY` | Yes | -- | HMAC-SHA256 webhook validation key |
| `OWL_URL` | No | `http://growdirect_ollama:11434` | Ollama inference endpoint |
| `OWL_MODEL` | No | `qwen3:14b` | Ollama model for AI chat |
| `CANARY_MEMORY_DB_URL` | No | -- | Memory bus PostgreSQL connection |
| `VALKEY_STREAM` | No | `canary:events` | TSP primary stream |
| `VALKEY_STREAM_DB` | No | `4` | Valkey DB for TSP streams |
| `QA_AGENT_URL` | No | `http://qa-agent:8002` | QA Agent sidecar endpoint |
| `CANARY_DEV_JWT_SECRET` | Dev only | -- | JWT signing secret for dev/test |

---

## Deployment

### Docker Service Topology (Dev)

Compose file: `Canary/devops/docker-compose.localhost.yml`
Stack name: `canary`
Network: `growdirect` (external)
Dev overlay: `docker-compose.dev.yml` (mounts source for hot reload)

8 services total (+ 1 sentinel). All application containers share the `canary-flask` image except Owl MCP (`canary-owl-mcp`) and QA Agent (`canary-qa-agent`).

**Boot command:** `./devops/scripts/dev.sh up` (wraps docker compose with dev overlay)

### Docker Service Topology (QA)

Compose file: `Canary/devops/docker-compose.qa.yml`
Stack name: `canary-qa`
Network: `growdirect` (external)

6 services: app + 4 TSP consumers + test runner (profile). No nginx (direct access). No Owl MCP or QA Agent in QA yet. Test runner available via `--profile test`.

### AWS Target Architecture

| Component | Current | AWS Target |
|-----------|---------|-----------|
| Flask | Docker on Mac Mini | ECS Fargate (1 vCPU, 512MB) |
| TSP consumers | Docker on Mac Mini | ECS Fargate (4 tasks) |
| PostgreSQL | growdirect_postgres | RDS PostgreSQL 17 (db.t4g.micro) |
| Valkey | growdirect_valkey | ElastiCache Valkey (cache.t4g.micro) |
| Ollama | growdirect_ollama (Docker) | Mac Studio (local) or Bedrock fallback |
| Secrets | `.env` files | AWS Secrets Manager |
| TLS | Cloudflare Tunnel / mkcert | ALB + ACM |
| DNS | Cloudflare | Route 53 + Cloudflare CDN |

Infrastructure phases: Phase 1 (local lab, ~$10/mo), Phase 2 (hybrid: RDS + local inference, ~$100-150/mo), Phase 3 (full AWS: ECS Fargate + Bedrock, ~$205/mo).

### CI/CD

| Script | Purpose |
|--------|---------|
| `canary_deploy.sh --full` | Pull, build, migrate, test, deploy (local Mac Mini) |
| `remote_deploy.sh` | SSH push to QA iMac, same sequence |

Test gates: unit tests block merge, integration tests block QA push, smoke tests run after every rebuild.

---

## Multi-Tenant Isolation

### Current State

| Layer | Mechanism | Enforcement |
|-------|-----------|-------------|
| Application | `TenantMixin.merchant_id` (String(36), indexed) | 18 models require merchant_id; Flask `g.merchant_id` set from session |
| Database (RLS) | `set_current_merchant(:mid)` called at transaction start | `session_factory.py` event listener on engine `begin` |
| Valkey cache | Key prefix includes `{merchant_id}` | e.g. `chirp:thresholds:{merchant_id}:{rule_id}` |
| Session | `session["merchant_id"]` set after OAuth | Valkey DB 0, 1-hour TTL |
| MCP tools | `context["merchant_id"]` injected from JWT | `create_mcp_blueprint` injects from `g.merchant_id` |

### Gaps

- RLS policies exist in the database but application code does not enforce them consistently -- some queries bypass `g.merchant_id` filter.
- TSP consumers process events for all merchants in a single consumer group -- no per-tenant stream isolation.
- Valkey streams (`canary:events`) are shared across all tenants -- a high-volume merchant could starve others.
- No tenant-aware rate limiting -- all merchants share the same IP-based rate limits.

---

## Blast Radius

This section documents what breaks when each layer of the Canary platform fails.

| Component | Services Affected | Data at Risk | User Impact | Recovery Time |
|-----------|-------------------|-------------|-------------|---------------|
| PostgreSQL | Everything | All stored data | Complete outage | Minutes (restart) to hours (corruption) |
| Valkey | Sessions, TSP, cache, rate limiting | In-flight stream messages | Auth broken, detection delayed | Seconds (restart), messages re-derivable |
| Flask monolith | All HTTP, all MCP, UI | None (stateless) | Complete UI + API outage | Seconds (container restart) |
| Single TSP consumer | One processing stage | Messages queue in stream | Detection delayed for that stage | Seconds (auto-restart) |
| Ollama | Owl AI, ALX embeddings | None | AI features unavailable, detection rules continue | Minutes (model reload) |
| nginx | External HTTPS access | None | External users cannot connect | Seconds (restart), :5001 still works |
| Memory Bus | ALX memory recall, session memory | None (separate DB) | AI responses lack institutional context | Seconds (restart) |

---

## 7-Layer Stack

| Layer | Name | Components |
|-------|------|------------|
| 0 | Infrastructure | Docker Compose (local), ECS Fargate (cloud target) |
| 1 | Data | PostgreSQL 17 (1 instance, 3 schemas + memory DB), Valkey 8 (streams + cache), PgBouncer |
| 2 | Domain Services | 12 MCP servers, one per bounded context |
| 3 | Agent Mesh | Owl, ALX, Chirp, Fox, Inscription, Condor (6 agents) |
| 4 | Orchestration | Mastra (TypeScript) agent workflows (target) |
| 5 | Gateway | Kong (self-hosted) / AWS API Gateway (target) |
| 6 | Frontend | Flask/Jinja2 (current), Next.js App Router + RSC + PWA (target) |
| 7 | Protocol | elJeffe / RaaS: Bitcoin L1 inscription + Avalanche L2 naming |

## 11 Service Domains

| # | Domain | Purpose | MCP Tools | SDD |
|---|--------|---------|-----------|-----|
| 1 | Identity | Merchants, users, roles, Square OAuth, tenant context | 6 | [[docs/sdds/canary/identity|Identity]], [[docs/sdds/canary/identity-square|Identity Square]] |
| 2 | Webhook Pipeline (TSP) | Webhook intake, HMAC validation, stream processing, parsing | 6 | [[docs/sdds/canary/tsp|TSP]], [[docs/sdds/canary/webhook-pipeline|Webhook Pipeline]] |
| 3 | Chirp | Stateless detection rules, threshold config, sensitivity presets | 10 | [[docs/sdds/canary/chirp|Chirp]] |
| 4 | Alert | Alert lifecycle, history, impact scoring, notifications | 6 | [[docs/sdds/canary/alert|Alert]] |
| 5 | Owl | AI chat, personalities, MCP tools, merchant memory, reports | 8 | [[docs/sdds/canary/owl|Owl]] |
| 6 | Fox | Case management, evidence locker, hash-chained timeline | 8 | [[docs/sdds/canary/fox|Fox]] |
| 7 | Analytics | Dashboard metrics, heatmaps, velocity baselines, scorecards | 7 | [[docs/sdds/canary/analytics|Analytics]], [[docs/sdds/canary/metrics-analytics|Metrics Analytics]] |
| 8 | ALX | Institutional memory (pgvector semantic search, 954+ memories) | 7 | [[docs/sdds/canary/alx|ALX]] |
| 9 | RaaS | Namespace resolution, merchant onboarding, source registration | 7 | [[docs/sdds/canary/raas|RaaS]] |
| 10 | Ops | Health check runner, simulator, ops console, Chirp Lab | 8 | [[docs/sdds/canary/ops|Ops]] |
| 11 | UI/BFF | Desktop + mobile rendering, feature flags, config | 4 | [[docs/sdds/canary/ui-bff|UI/BFF]] |

Additional SDDs:
- [[docs/sdds/canary/data-model|Data Model]] -- Cross-schema data model reference (PII map anchor)
- [[docs/sdds/canary/external-identities|External Identities]] -- Entity resolution, PII abstraction
- [[docs/sdds/canary/goose|Goose]] -- Treasury/payment layer, Bitcoin/L402
- [[docs/sdds/canary/multi-pos-architecture-proof|Multi-POS Architecture Proof]] -- Multi-source adapter pattern
- [[docs/sdds/canary/qa-agent|QA Agent]] -- QA orchestration, 30+ MCP tools

---

## Patterns

### Base Classes (SQLAlchemy 2.0 `Mapped[]` syntax)

| Base | Schema | Purpose |
|------|--------|---------|
| `AppBase` | `app` | Operational models (merchants, alerts, cases) |
| `SalesBase` | `sales` | Transaction log (immutable event stream) |
| `MetricsBase` | `metrics` | Analytics star schema (re-derivable) |

### GSLM Mixins

| Mixin | Columns | Used By | Purpose |
|-------|---------|---------|---------|
| `TenantMixin` | `merchant_id` (String(36), indexed) | 18 models | Multi-tenant isolation key |
| `AuditMixin` | `created_at`, `updated_at`, `created_by`, `modified_by` | 29 models | Audit timestamps and attribution |
| `SoftDeleteMixin` | `db_status`, `db_effective_from`, `db_effective_to` | 9 models | Soft delete with effective dating |
| `ImmutableMixin` | (trigger-enforced) | All sales tables | PostgreSQL `BEFORE UPDATE OR DELETE` trigger |

### Data Mutation Patterns

| Pattern | Scope | Enforcement |
|---------|-------|-------------|
| WRITE-ONCE IMMUTABLE | `sales.*` (all 19 tables) | PostgreSQL BEFORE trigger |
| APPEND-ONLY | Alert, AlertHistory, AuditLog, NotificationLog | Application convention |
| SOFT DELETE (GSLM) | 9 app models | SoftDeleteMixin columns |
| OPERATIONAL | All other app models | Standard CRUD with audit trail |

### Security Extensions

| Extension | Purpose | Config |
|-----------|---------|--------|
| CSRFProtect | CSRF tokens on POST/PUT/DELETE | API/webhook/MCP blueprints exempt (JWT/HMAC auth) |
| Flask-Limiter | Rate limiting | 2000/day, 500/hour default; MCP tools 1000/hour |
| Flask-Talisman | Security headers | HSTS, CSP, X-Frame-Options; force_https off for localhost |
| Flask-Session | Server-side sessions | Valkey DB 0, 1-hour TTL |

### Encryption

| Scope | Algorithm | Key Source | Migration |
|-------|-----------|-----------|-----------|
| OAuth tokens | AES-256-GCM | `CANARY_ENCRYPTION_KEY` (.env) | Transparent Fernet-to-GCM on next store |
| Session data | None | -- | Plaintext in Valkey |
| Employee PII | None | -- | Plaintext in PostgreSQL |
| Webhook payloads | None | -- | Plaintext in sales schema |

### Test Strategy

| Layer | Location | Gate | Runtime |
|-------|----------|------|---------|
| Unit | `tests/unit/` | CI blocks merge | ~30s |
| Integration | `tests/integration/` | Before QA push | ~2min |
| Smoke | `tests/smoke/` | After every rebuild | ~10s |

---

## Target State

The target-state architecture extracts domains from the Flask monolith into standalone agent containers, adds an API gateway, replaces Jinja2 with Next.js, and introduces Mastra for multi-step agent orchestration. The same MCP tool contracts stay -- transport changes from in-process calls to HTTP.

### API Gateway (Phase 2: Kong, Phase 3: AWS API Gateway)

Externalizes cross-cutting concerns: TLS termination, JWT validation, HMAC webhook verification, rate limiting per merchant tier (Open 100/min, Standard 60/min, Burst 300/min, Internal 1000/min), path-based routing, CORS enforcement, SSE proxy, and request/response logging with correlation IDs.

Auth evolution: Flask middleware (now) -> Keycloak OIDC (self-hosted) -> AWS Cognito. All produce identical JWT payloads: `{sub, merchant_id, organization_id, roles, iss, exp}`.

### Container Extraction (Phase 4)

Each agent becomes an independent container: MCP server + MCP client + event bus consumer + service logic + PgBouncer sidecar. AI agents (Owl, ALX, Condor) co-locate with Ollama on Mac Studio (192GB unified memory). Deterministic agents (Chirp, Fox, Alert) stay with the database. Agent discovery via Valkey hash (`canary:registry:<agent>`), 30-second heartbeat.

### Process Ontology Alignment

Canary's detection rules implement a 30-year retail operations process ontology:

| Source | Year | Canary Mapping |
|--------|------|----------------|
| Staples Level 2 (Hoover/PwC) | 1996 | 26 processes -> Chirp rule categories |
| Tesco Operating Model v1.24 | 2007 | ~100 processes -> KPI framework |
| Beck & Peacock "New Loss Prevention" | 2009 | Operational failure taxonomy -> detection philosophy |
| Speights, Downs & Raz | 2017 | Statistical methods -> velocity z-scores, baseline modeling |

The 6-layer scoring stack: per-transaction (Sales Audit), per-alert (Performance Monitoring), per-period heatmap (Performance Levers), time-series velocity (XPLOSS/Poisson), aggregate health (Heartbeat/CDSS), entity risk (SRA Scorecards).

**Source SDDs:** SDD-059 (Modern Architecture Blueprint), SDD-060 (Process Ontology Alignment), SDD-062 (API Gateway).

---

## Code Review Findings

### P0 -- Blocks Production

| # | Finding | Detail | Recommended Fix |
|---|---------|--------|-----------------|
| P0-1 | Employee PII stored plaintext | `first_name`, `last_name` in `app.employees` have no encryption. These fields flow to alerts, cases, and analytics. | Extend `crypto.py` AES-256-GCM to employee PII fields. Encrypt at write, decrypt at read. |
| P0-2 | Webhook payloads stored with raw customer data | `sales.raw_webhooks` preserves full Square JSON including customer IDs, tender details. Immutable table means redaction requires compensating INSERT. | Add a redaction step in TSP Sub1 (Seal) -- strip customer PII before persisting raw payload. Store hash of original for integrity. |
| P0-3 | Encryption key in `.env` file | `CANARY_ENCRYPTION_KEY` stored in plaintext `.env`, loaded via `os.getenv()`. Key compromise exposes all OAuth tokens. | Migrate to AWS Secrets Manager. Load at startup via `boto3`. Rotate key quarterly. |
| P0-4 | `SECRET_KEY` falls back to insecure default | `wsgi.py` lines 49-55: non-production environments get `dev-fallback-not-for-production`. If `CANARY_ENV` is misconfigured, production runs with a known key. | Remove fallback entirely. Fail hard if `SECRET_KEY` is not set, regardless of environment. |
| P0-5 | QA compose embeds encryption key in plaintext | `docker-compose.qa.yml` line 67: `CANARY_ENCRYPTION_KEY: BHDJWBeEEtNrcqqONlNbyVdLjec4vP0SymY-X5sPQic=` is a hardcoded secret in a committed file. | Remove from compose. Use `.env` file (gitignored) or Docker secrets. |

### P1 -- Before GA

| # | Finding | Detail | Recommended Fix |
|---|---------|--------|-----------------|
| P1-1 | No data retention policy | No automated purge for any table. `sales.*` is immutable and append-only -- will grow indefinitely. | Implement retention: raw webhooks >12mo archived, sessions >30d purged, audit logs >24mo cold storage. |
| P1-2 | Session data unencrypted in Valkey | `session["merchant_id"]` and session state stored as plaintext Redis keys. No AUTH required on dev Valkey. | Enable Valkey AUTH + TLS in production. Consider session payload encryption. |
| P1-3 | No audit logging for MCP tool invocations | `create_mcp_blueprint` dispatches tool calls without logging who called what with what params. | Add audit log entry for every `POST /tools/<name>` with caller identity, tool name, params hash, result status. |
| P1-4 | Error responses may leak internals | `wsgi.py` error handlers render templates but Flask's default 500 handler can leak tracebacks in non-debug mode if templates are missing. | Ensure all error templates exist. Add catch-all JSON error handler for API routes. Strip stack traces in production. |
| P1-5 | RLS context fails open | `session_factory.py` `_set_rls_context`: if `g.merchant_id` is None, no RLS filter is applied -- queries see all tenants. | Add explicit `set_current_merchant('none')` when merchant_id is absent, or fail the query if tenant context is required. |
| P1-6 | No key rotation procedure | `crypto.py` supports Fernet-to-GCM migration but no GCM-to-GCM rotation. Key compromise requires manual re-encryption of all tokens. | Document rotation procedure. Build CLI command to re-encrypt all tokens with a new key. |
| P1-7 | Notification email/SMS stubs | `notification_dispatcher.py` logs `STATUS_SUPPRESSED` for email and SMS. No actual delivery channel is wired. | Wire SendGrid or SES for email before GA. SMS can remain stub with clear user documentation. |

### P2 -- Post-Launch

| # | Finding | Detail | Recommended Fix |
|---|---------|--------|-----------------|
| P2-1 | No structured monitoring | No Prometheus metrics, no Grafana dashboards, no alerting rules. Health checks exist but are not scraped. | Add Prometheus client to Flask. Export request latency, error rates, TSP throughput, queue depth. |
| P2-2 | Single Flask worker in dev | `--workers 1 --threads 4` is fine for dev but production needs multiple workers. Enterprise compose has `${FLASK_WORKERS:-4}`. | Ensure production deployment uses enterprise compose with 4+ workers. |
| P2-3 | No request correlation IDs | No `X-Request-ID` or trace ID propagated across Flask -> TSP consumers -> Owl MCP. Debugging cross-service issues requires log timestamp correlation. | Add middleware to generate/propagate correlation ID in all log entries. |
| P2-4 | Audit chain verification is fail-open | `wsgi.py` line 480: `raise_on_tamper=False`. A tampered audit chain only produces a CRITICAL log, does not block startup. | Consider fail-closed in production: if audit chain is tampered, refuse to serve write endpoints. |
| P2-5 | TSP consumers share one Valkey DB for all tenants | `canary:events` stream processes all merchants in one consumer group. High-volume merchants can delay processing for others. | Add per-tenant stream partitioning or priority-based routing in Phase 4 container extraction. |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (P0-1: employee names, P0-2: webhook payloads)
- [ ] Secrets in AWS Secrets Manager, not .env (P0-3, P0-5)
- [x] Health check endpoint responds (`/health` on Flask, Owl MCP, QA Agent, TSP consumers)
- [ ] Audit logging for sensitive operations (P1-3: MCP tool invocations not logged)
- [ ] Data retention policy implemented (P1-1: no automated purge)
- [x] Rate limiting on public endpoints (Flask-Limiter: 2000/day, 500/hour; MCP: 1000/hour)
- [ ] Error responses don't leak internals (P1-4: template fallback risk)
- [x] CSRF protection active (CSRFProtect on all session-auth routes)
- [x] TLS termination (Cloudflare Tunnel / nginx with mkcert)
- [x] OAuth tokens encrypted (AES-256-GCM via `crypto.py`)
- [x] Immutable sales data (PostgreSQL BEFORE trigger enforced)
- [x] Multi-tenant isolation at DB layer (RLS via `set_current_merchant`)
- [ ] Multi-tenant isolation fail-safe (P1-5: RLS fails open when merchant_id is None)
- [ ] Key rotation procedure documented (P1-6)
- [ ] Session encryption in Valkey (P1-2)
- [ ] Monitoring and alerting (P2-1)
- [ ] Request correlation IDs (P2-3)
