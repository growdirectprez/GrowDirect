---
classification: confidential
owner: GrowDirect LLC
---

# Shared Infrastructure — Local Dev Stack

> [!warning] Scope: local development only
> Per **GRO-700 v2** and `Brain/wiki/cards/platform-stack-commitment.md`, the production substrate is **GCP** (Cloud Run + Cloud SQL + Memorystore + Pub/Sub + Vertex AI + Identity Platform). The Docker Compose stack documented below is the **local dev environment only** — it does not describe production. Do not extend this doc with production claims; production runtime topology lives in `Brain/wiki/cards/gcp-foundation-runbook.md` and (forthcoming) `docs/sdds/platform/gcp-target-architecture.md`.

> **Status:** Local dev contract
> **Type:** Platform Service (dev environment)
> **Namespace:** platform
> **Last updated:** 2026-05-01 (scope retitled per GRO-700 v2)
> **Code location:** `devops/docker-compose.yml`, `devops/init-db/`
> **Production substrate:** GCP — see `Brain/wiki/cards/gcp-foundation-runbook.md`
> **Author role:** [[docs/team/DevOps|DevOps]] · **Operator role:** [[docs/team/Engineer|Engineer]]

**Wiki:** [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]] · [[Brain/projects/Canary|Canary MOC]] · [[Brain/projects/Cove|Cove MOC]] · [[Brain/projects/Angel|Angel MOC]]
**Method:** [[Brain/projects/Method|Method MOC]]

---

## Purpose

The shared infrastructure is a single Docker Compose stack that provides all stateful services for every GrowDirect application in development. No app runs its own database or cache. Each app container joins the `growdirect` Docker network and connects to shared services by container-name DNS. The stack is started once from `~/GrowDirect/devops`; individual apps start their own Flask containers separately.

---

## Dependencies

| Dependency | Required | Purpose |
|-----------|:--------:|---------|
| Docker Engine 24+ | Yes | Container runtime for all services |
| Docker Compose v2 | Yes | Stack orchestration |
| Host ports 5432, 6379, 5050, 11434, 8003 | Yes | Service access from host and between stacks |
| `devops/init-db/` SQL scripts | Yes | Database provisioning on first boot |

No external network dependencies. The entire stack runs offline on localhost.

---

## Data Flow & PII Map

### What Enters

All PII enters through app containers (Canary Flask, Cove Flask, Angel Agent), not through shared infrastructure directly. Shared infra is the persistence and compute layer.

| Source | Data type | Entry path |
|--------|-----------|------------|
| Canary Flask | Square merchant transactions, OAuth tokens, merchant profiles | SQLAlchemy writes to `canary` database |
| Cove Flask | HOA member profiles, ballot data, parcel records | SQLAlchemy writes to `cove` database |
| Angel Agent | Real estate leads with contact info | SQLAlchemy writes to `cove` database (Angel is a Cove module) |
| Memory Bus | AI agent session logs, decisions, embeddings | FastMCP writes to `growdirect_memory` database |

### What Is Stored — PII by Database

| Database | PII Fields | Classification | Encryption at Rest |
|----------|-----------|---------------|-------------------|
| `canary` | Merchant names, business emails, Square OAuth tokens (AES-256-GCM in `app.merchants`), transaction amounts, customer names on transactions | sensitive | **None** (PostgreSQL default — unencrypted data volume). OAuth tokens encrypted at application level. |
| `cove` | Member names, lot emails, personal emails, phone numbers, home addresses (via parcel), ballot content (RLS-gated), password hashes | sensitive / restricted (ballots) | **None**. No field-level encryption. Ballot secrecy enforced by PostgreSQL RLS only. |
| `growdirect_memory` | Session decisions, architecture notes. May contain quoted PII from agent interactions. | internal | **None**. Content field is plaintext. |
| Valkey (DB 0) | Canary session tokens, rate limiter state | internal | **None**. No persistence encryption. `requirepass` only. |
| Valkey (DB 1) | Cove session tokens (Flask-Session serialized user IDs) | internal | **None**. No persistence encryption. |

### What Exits

| Destination | Data type | Path |
|------------|-----------|------|
| App Flask containers | Query results containing PII | SQLAlchemy reads over `growdirect` Docker network (plaintext TCP) |
| Ollama | Text content for embedding (may contain PII) | HTTP to port 11434 (plaintext) |
| Memory Bus clients | Session memories (may contain PII references) | HTTP MCP over port 8003 (plaintext) |
| pgAdmin | Full database access (dev only) | HTTP on port 5050 (plaintext) |

---

## Multi-Tenant Isolation Model

All apps share one PostgreSQL instance and one Valkey instance. Isolation is enforced at multiple levels — none of which prevent cross-app access if credentials are compromised.

### PostgreSQL Isolation

| Layer | Mechanism | Strength |
|-------|-----------|----------|
| Database-level | Each app has its own database (`canary`, `cove`, `growdirect_memory`) | Strong — connection string targets one database. Cross-database queries require explicit `dblink` or reconnection. |
| Schema-level (Canary only) | `app`, `sales`, `metrics` schemas within `canary` database | Moderate — enforced by role-based `ALTER DEFAULT PRIVILEGES`. The `growdirect` superuser bypasses all schema restrictions. |
| Role-level (Canary only) | `canary_app` (read-write app/metrics, read-only sales) and `canary_tsp` (read-write sales, read-only app) | Moderate — SOX-style write-path isolation. But apps currently connect as `growdirect` superuser, not as restricted roles. |

**Gap:** All apps connect as the `growdirect` superuser (`growdirect:growdirect_dev`). The restricted `canary_app` / `canary_tsp` roles exist but are not used in the Docker Compose connection strings. Any app can read/write any database.

### Valkey Isolation

| Layer | Mechanism | Strength |
|-------|-----------|----------|
| Logical database | Canary uses DB 0, Cove uses DB 1. TSP streams use DB 4. | Weak — prevents accidental key collisions but does not prevent cross-app access. Same password for all. |
| Password auth | `--requirepass valkey_dev` | Weak — single password shared by all apps. Any app with the password can access any logical database. |
| Key namespacing | Canary TSP uses `canary:events` prefix. Flask-Session uses `session:` prefix. | Convention only — not enforced. |

**Gap:** No ACL rules. No per-app Valkey users. Cross-app session hijacking is theoretically possible.

---

## Startup Order and Dependency Graph

```
                    ┌─────────────┐
                    │  PostgreSQL  │  ← starts first (no dependencies)
                    └──────┬──────┘
                           │ healthy
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼────┐ ┌─────▼──────┐
        │  pgAdmin   │ │ Memory │ │   Valkey    │  ← starts independently
        │ (dev only) │ │  Bus   │ │ (no deps)   │
        └────────────┘ └────────┘ └──────┬──────┘
                                         │
                    ┌─────────────┐       │
                    │   Ollama    │       │  ← starts independently
                    │ (no deps)   │       │
                    └──────┬──────┘       │
                           │              │
    ════════════════════════╪══════════════╪═══════════  shared infra healthy
                           │              │
              ┌────────────┴──────────────┴──┐
              │     App stacks start here    │
              │  (Canary Flask, Cove Flask)  │
              │  nginx-wait checks pg+valkey │
              └──────────────────────────────┘
```

**Start command:**
```bash
cd ~/GrowDirect/devops && docker compose up -d     # shared infra
cd ~/GrowDirect/Canary && ./devops/scripts/dev.sh up  # Canary app
cd ~/GrowDirect/Cove/devops && docker compose up -d   # Cove app
```

**Dependency enforcement:**
- `pgadmin` and `memory-bus` declare `depends_on: postgres: condition: service_healthy`
- Canary uses a `nginx-wait` sentinel container that polls `growdirect_postgres:5432` and `growdirect_valkey:6379` before Flask starts
- Cove Flask does not declare explicit depends_on for shared infra (relies on restart loop)

---

## Blast Radius

What breaks when each component goes down.

| Component Down | Direct Impact | Indirect Impact | Recovery |
|---------------|--------------|-----------------|----------|
| **PostgreSQL** | All app database queries fail. SQLAlchemy raises `OperationalError`. Every page load that touches the DB returns 500. | Alembic migrations cannot run. pgAdmin shows disconnected. Memory Bus cannot store/retrieve memories. | Container auto-restarts (`unless-stopped`). Data survives in `growdirect_pgdata` named volume. Apps reconnect via pool `pre_ping`. |
| **Valkey** | Cove: all authenticated sessions fail (Flask-Session backed by Valkey). Users effectively logged out. Canary: rate limiter falls back to in-memory (resets per worker, not shared). | TSP stream consumers (sub1-sub4) cannot read/write Valkey Streams. Transaction processing pipeline halts. | Container auto-restarts. Data survives in `growdirect_valkey_data`. Sessions lost if Valkey data was not persisted (RDB snapshots only, default interval). |
| **Ollama** | Embedding generation returns `None`. Semantic search degrades to full-text or ILIKE fallback. | New memories stored without embeddings. Knowledge MCP search quality degrades. Owl AI analysis unavailable. | Container auto-restarts. Model weights survive in `growdirect_ollama_data`. No data loss — embeddings can be regenerated. |
| **Memory Bus** | AI agent sessions cannot store or recall memories. `session_start`, `memory_recall`, `domain_context` MCP tools fail. | No impact on app containers — they do not depend on Memory Bus at runtime. Builder agents lose context recall. | Container auto-restarts. All memory data is in PostgreSQL (survives). |
| **pgAdmin** | No database administration UI. | No impact on any app or service. Dev convenience tool only. | Container auto-restarts. Config survives in `growdirect_pgadmin_data`. |
| **Docker network** (`growdirect`) | All inter-container communication fails. Every service becomes an island. | Complete platform outage. No database, no cache, no inference. | `docker network create growdirect` + restart all stacks. Named network survives `docker compose down` on individual stacks but not `docker network rm`. |

---

## API Contract

Shared infrastructure exposes no HTTP routes of its own (except Memory Bus, documented separately in [[docs/sdds/platform/memory-bus|Memory Bus]]). Services are accessed via protocol-specific connections:

| Service | Protocol | Connection Pattern |
|---------|----------|-------------------|
| PostgreSQL | PostgreSQL wire protocol (TCP 5432) | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/<db>` |
| Valkey | RESP protocol (TCP 6379) | `redis://:valkey_dev@growdirect_valkey:6379/<db_number>` |
| Ollama | HTTP REST (TCP 11434) | `http://growdirect_ollama:11434/api/embeddings` (and `/api/generate`, `/api/tags`) |
| pgAdmin | HTTP (TCP 5050) | Browser: `http://localhost:5050` (dev only) |

---

## Operations

### Health Checks

| Service | Command | Interval | Start Period | Retries |
|---------|---------|----------|-------------|---------|
| PostgreSQL | `pg_isready -U growdirect` | 5s | 10s | 10 |
| Valkey | `valkey-cli -a valkey_dev ping` | 5s | n/a | 5 |
| pgAdmin | `wget -q --spider http://localhost:80/misc/ping` | 15s | 30s | 3 |
| Ollama | `curl -sf http://localhost:11434/api/tags` | 10s | 30s | 5 |
| Memory Bus | `curl -so /dev/null -w '%{http_code}' http://localhost:8003/mcp \| grep -q '406'` | 10s | 15s | 5 |

### Restart Policy

All services: `restart: unless-stopped`. Auto-restart on crash, daemon restart, and host reboot. Does NOT restart if explicitly stopped.

### Monitoring (Current State)

**Not implemented.** No metrics collection, no alerting, no dashboards. Health checks exist for container orchestration only. Production monitoring is documented in [[docs/sdds/platform/aws-target-architecture|AWS Target Architecture]].

### Configuration — Environment Variables

#### PostgreSQL

| Variable | Value (dev) | Purpose |
|----------|-------------|---------|
| `POSTGRES_USER` | `growdirect` | Superuser for all databases |
| `POSTGRES_PASSWORD` | `growdirect_dev` | Superuser password (dev only) |
| `POSTGRES_DB` | `growdirect` | Default database (unused by apps) |

#### Valkey

| Setting | Value (dev) | Purpose |
|---------|-------------|---------|
| `--requirepass` | `valkey_dev` | Password for all connections |

#### pgAdmin

| Variable | Value (dev) | Purpose |
|----------|-------------|---------|
| `PGADMIN_DEFAULT_EMAIL` | `admin@growdirect.com` | Login email |
| `PGADMIN_DEFAULT_PASSWORD` | `admin` | Login password |
| `PGADMIN_CONFIG_SERVER_MODE` | `False` | Single-user desktop mode |

#### Memory Bus

| Variable | Value (dev) | Purpose |
|----------|-------------|---------|
| `DATABASE_URL` | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory` | Memory database |
| `OLLAMA_URL` | `http://growdirect_ollama:11434` | Embedding endpoint |
| `EMBEDDING_MODEL` | `qwen3-embedding:8b` | 1024-dim embedding model |
| `PORT` | `8003` | MCP server listen port |
| `MCP_API_KEY` | `growdirect-memory-dev-key` (default) | API key for MCP auth |

### App-Side Connection Strings

| App | PostgreSQL | Valkey | Ollama |
|-----|-----------|--------|--------|
| Canary | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/canary` | `redis://:valkey_dev@growdirect_valkey:6379/0` (sessions + rate limiter) | `http://growdirect_ollama:11434` |
| Cove | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove` | `redis://:valkey_dev@growdirect_valkey:6379/1` (sessions) | `http://growdirect_ollama:11434` |
| Canary TSP streams | Same PostgreSQL | `redis://:valkey_dev@growdirect_valkey:6379/4` (Valkey Streams) | n/a |
| Canary Owl MCP | Same PostgreSQL + `growdirect_memory` | n/a | `http://growdirect_ollama:11434` (inference + embeddings) |

**Canary config divergence:** Canary's `Config` base class defaults to `canary:canary@localhost:5432/canary` — a user and host that do not exist in shared infra. This is overridden by the Docker Compose `environment:` block. The fallback is unsafe if the env var is missing.

---

## Deployment — Docker Service Definitions

### Services (5 containers)

| Service | Image | Container Name | Host Port | Volume |
|---------|-------|---------------|-----------|--------|
| PostgreSQL | `pgvector/pgvector:pg17` | `growdirect_postgres` | `127.0.0.1:5432` | `growdirect_pgdata` |
| Valkey | `valkey/valkey:8-alpine` | `growdirect_valkey` | `127.0.0.1:6379` | `growdirect_valkey_data` |
| pgAdmin | `dpage/pgadmin4:latest` | `growdirect_pgadmin` | `127.0.0.1:5050` | `growdirect_pgadmin_data` |
| Ollama | `ollama/ollama` | `growdirect_ollama` | `127.0.0.1:11434` | `growdirect_ollama_data` |
| Memory Bus | `growdirect-memory-bus` (built) | `growdirect_memory_bus` | `127.0.0.1:8003` | none |

### Network

```yaml
networks:
  default:
    name: growdirect  # bridge network, shared across all stacks
```

App stacks join via `external: true`:
```yaml
networks:
  growdirect:
    external: true
```

All host ports bound to `127.0.0.1` only — no external exposure.

### Volumes (Named)

All volumes use explicit `name:` to prevent Docker Compose directory-prefix collisions.

| Volume | Mount Point | Purpose |
|--------|------------|---------|
| `growdirect_pgdata` | `/var/lib/postgresql/data` | All database data files |
| `growdirect_valkey_data` | `/data` | Valkey RDB snapshots |
| `growdirect_pgadmin_data` | `/var/lib/pgadmin` | pgAdmin saved connections |
| `growdirect_ollama_data` | `/root/.ollama` | Downloaded model weights |

### Database Provisioning (First Boot)

Init scripts run once when `growdirect_pgdata` volume is first created:

1. `01-create-databases.sql` — Creates 6 databases (`canary`, `canary_test`, `cove`, `cove_test`, `growdirect_memory`, `growdirect_memory_test`), enables `vector`, `pgcrypto`, `uuid-ossp` extensions in each, creates Canary schemas (`app`, `sales`, `metrics`) and restricted roles (`canary_app`, `canary_tsp`).
2. `02-create-memory-db.sql` — Enables extensions in memory databases, grants privileges. Table creation is handled by Alembic (`services/memory-bus/migrations/`).

All statements are idempotent (`IF NOT EXISTS` throughout). Safe to re-run manually.

### Port Allocation Map (Full Platform)

| Service | Container | Host Port | Container Port | Stack |
|---------|-----------|-----------|---------------|-------|
| PostgreSQL | `growdirect_postgres` | 5432 | 5432 | shared |
| Valkey | `growdirect_valkey` | 6379 | 6379 | shared |
| pgAdmin | `growdirect_pgadmin` | 5050 | 80 | shared |
| Ollama | `growdirect_ollama` | 11434 | 11434 | shared |
| Memory Bus | `growdirect_memory_bus` | 8003 | 8003 | shared |
| Canary Flask | `canary_flask` | 5001 | 5001 | canary |
| Canary nginx | `canary_localhost_nginx` | 443, 80 | 443, 80 | canary |
| Canary Owl MCP | `canary_localhost_owl_mcp` | 8001 | 8001 | canary |
| Canary QA Agent | `canary_localhost_qa_agent` | 8002 | 8002 | canary |
| Cove Flask | `cove_flask` | 5002 | 5000 | cove |
| Cove MailHog SMTP | `cove_localhost_mailhog` | 1026 | 1025 | cove |
| Cove MailHog Web | `cove_localhost_mailhog` | 8026 | 8025 | cove |
| Angel Agent | `cove_angel_agent` | 8004 | 8004 | cove |

### Docker Conventions

**Image naming:** `<appname>-<service>` (e.g., `canary-flask`, `cove-flask`, `growdirect-memory-bus`). Required on every `build:` block to prevent directory-derived name collisions.

**Project naming:** Top-level `name:` required in every app compose file (`name: canary`, `name: cove`). Prevents cross-app container conflicts when all compose files live in `devops/`.

**Volume mounts (dev):** App source dirs mounted for Gunicorn `--reload`. Never mount `.env`, `requirements.txt`, or `node_modules/`.

**Rebuild triggers:** `requirements.txt` change or `Dockerfile` change requires `docker compose build`. Python/template/static changes are live via volume mount.

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P0-1 | **Shared superuser credentials across all apps** | All apps connect to PostgreSQL as `growdirect` (superuser). Canary can read/write `cove` database and vice versa. The restricted roles (`canary_app`, `canary_tsp`) exist but are unused in Docker Compose connection strings. | Create per-app database users with `CONNECT` privilege limited to their own database. Update all compose `environment:` blocks. Revoke superuser from app connections. |
| P0-2 | **No TLS between containers** | All inter-container communication (PostgreSQL, Valkey, Ollama, Memory Bus) is plaintext TCP over the Docker bridge network. PII in database queries, session tokens, and embedding text is transmitted unencrypted. | In production: require `sslmode=require` on PostgreSQL, enable Valkey TLS, use internal ALB or service mesh for HTTP services. In dev: accept as-is (localhost only). |
| P0-3 | **No PostgreSQL encryption at rest** | The `growdirect_pgdata` Docker volume stores all database files unencrypted. Contains member PII (names, emails, phones), merchant data, ballot content, and OAuth tokens. Only Canary OAuth tokens have application-level encryption. | Production: use AWS RDS with storage encryption (AES-256). Dev: acceptable risk for localhost-only access. |
| P0-4 | **Database credentials hardcoded in compose file** | `growdirect_dev`, `valkey_dev`, `admin`, and all role passwords are plaintext in `docker-compose.yml` and `01-create-databases.sql`, both committed to git. | Production: AWS Secrets Manager for all credentials, injected at runtime via ECS task definitions. Dev: acceptable (dev-only values, localhost-only binding). |
| P0-5 | **No backup strategy** | No automated database backups. No point-in-time recovery. `growdirect_pgdata` volume is the only copy of all data. A `docker volume rm` destroys everything. | Production: RDS automated backups + WAL archiving. Dev: add a cron-based `pg_dump` to a host directory outside Docker volumes. |

### P1 — Before GA

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P1-1 | **Single Valkey password for all apps** | Both apps use `valkey_dev` to access all logical databases. No ACL rules. Any app can read/modify another app's sessions. | Implement Valkey ACL: per-app usernames with `~canary:*` and `~cove:*` key patterns. Or use ElastiCache in production with IAM auth. |
| P1-2 | **Valkey persistence not configured** | Default Valkey RDB snapshot interval (every 60s if 1000+ keys changed). Sessions and rate limiter state may be lost on crash. TSP stream data in DB 4 has no persistence guarantee. | Add `appendonly yes` to Valkey command for AOF persistence. Production: ElastiCache with Multi-AZ and automatic failover. |
| P1-3 | **No data retention policy at infrastructure level** | Databases grow indefinitely. No automated cleanup of old sessions, stale embeddings, or expired memories. Memory Bus `alx_sessions` and `alx_memories` have no TTL. | Implement retention policies: sessions >30d, memories >12mo review, embeddings regenerated on model change. |
| P1-4 | **Canary config fallback references nonexistent credentials** | `Config.DATABASE_URL` defaults to `canary:canary@localhost:5432/canary` — a user that does not exist. If env var is missing, app crashes with misleading auth error. | Change fallback to match shared infra credentials, or remove fallback entirely and require the env var. |
| P1-5 | **Memory Bus health check is fragile** | Health check greps for HTTP 406 from `/mcp` endpoint. This is a side effect of sending a GET to a streamable-HTTP endpoint that expects POST. A real health endpoint (`/health`) would be more reliable. | Add a dedicated `/health` endpoint to Memory Bus that checks database connectivity. |
| P1-6 | **pgAdmin uses `latest` tag** | `dpage/pgadmin4:latest` is unpinned. Container behavior may change on rebuild. | Pin to specific version (e.g., `dpage/pgadmin4:8.4`). Dev-only service but still worth pinning. |

### P2 — Post-Launch

| # | Finding | Description | Recommended Fix |
|---|---------|-------------|-----------------|
| P2-1 | **No connection pooling at infrastructure level** | Each app manages its own SQLAlchemy pool. No PgBouncer or shared connection pooler. At scale, connection count could exhaust PostgreSQL `max_connections`. | Add PgBouncer as a sidecar or shared service in production. Configure `max_connections` based on total app worker count. |
| P2-2 | **Ollama model not pinned** | `ollama/ollama` image tag is `latest`. Model `qwen3-embedding:8b` must be pulled manually after first boot. No model provisioning in compose. | Add an init container that pulls `qwen3-embedding:8b` on first boot. Pin Ollama image version. |
| P2-3 | **No Valkey memory limits** | Valkey has no `maxmemory` configured. Could consume all available host memory if a session leak or stream backlog occurs. | Set `maxmemory 512mb` (dev) with `maxmemory-policy allkeys-lru`. |
| P2-4 | **SQLAlchemy pool settings inconsistent** | Cove configures `pool_pre_ping=True` and `pool_recycle=300`. Canary uses defaults. Canary may experience stale connection errors after PostgreSQL restarts. | Standardize pool settings across all apps: `pool_pre_ping=True`, `pool_recycle=300`, `pool_size=5`. |
| P2-5 | **Angel Agent port not bound to localhost** | `cove_angel_agent` exposes port `8004:8004` without `127.0.0.1` prefix. Accessible from any network interface. | Change to `127.0.0.1:8004:8004` to match all other services. |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest — PostgreSQL storage encryption (P0-3)
- [ ] PII encrypted in transit — TLS between all services (P0-2)
- [ ] Secrets in AWS Secrets Manager, not in compose files or .env (P0-4)
- [ ] Per-app database credentials, no shared superuser (P0-1)
- [ ] Automated database backups with point-in-time recovery (P0-5)
- [ ] Health check endpoints on all services (P1-5)
- [ ] Data retention policy implemented and automated (P1-3)
- [ ] Valkey ACL or per-app authentication (P1-1)
- [ ] Valkey persistence configured (AOF or RDB with known RPO) (P1-2)
- [ ] Connection pooling strategy for production scale (P2-1)
- [ ] All container images pinned to specific versions (P1-6, P2-2)
- [ ] Memory limits configured on all containers (P2-3)
- [ ] All ports bound to `127.0.0.1` in dev (P2-5)
- [ ] Monitoring and alerting configured (see [[docs/sdds/platform/aws-target-architecture|AWS Target Architecture]])
- [ ] Audit logging for database administrative operations
- [ ] Rate limiting on infrastructure management endpoints
- [ ] Error responses from infrastructure services do not leak credentials
