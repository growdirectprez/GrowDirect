# Shared Infrastructure

> **Status:** Complete — written from code
> **Namespace:** platform
> **Last updated:** 2026-03-30
> **Code location:** `devops/docker-compose.yml`, `devops/init-db/`

---

## 1. Overview

The GrowDirect shared infrastructure is a single Docker Compose stack that provides all stateful services used by every GrowDirect application. No app runs its own database or cache. Instead, each app container joins the `growdirect` Docker network and connects to the shared services by hostname.

The stack has five services:

- **PostgreSQL 17 + pgvector** — all app databases in one instance, one schema-separated database per app
- **Valkey 8** — Redis-compatible key-value store used for session management, caching, and background task queues; password-protected
- **pgAdmin 4** — web-based database browser for development (dev-only tool, not deployed to production)
- **Ollama** — local LLM inference server used for embedding generation across all apps
- **Memory Bus** — GrowDirect's platform-level knowledge store; an MCP server built on FastMCP that exposes semantic memory tools to AI agents

The stack is started once from `~/GrowDirect/devops`. Individual apps then start their own Flask containers separately. All containers communicate over the shared `growdirect` Docker network using container-name DNS resolution.

---

## 2. Architecture

### Component Diagram

```
Host machine (localhost)
│
├── devops/docker-compose.yml  ← shared infra stack
│   │
│   ├── growdirect_postgres   (pgvector/pgvector:pg17)
│   │     Listens on 127.0.0.1:5432 (host) / 5432 (network)
│   │     Volumes: growdirect_pgdata (named Docker volume)
│   │     Init scripts: devops/init-db/ (runs on first boot only)
│   │
│   ├── growdirect_valkey     (valkey/valkey:8-alpine)
│   │     Listens on 127.0.0.1:6379 (host) / 6379 (network)
│   │     Auth: requirepass valkey_dev
│   │     Volumes: growdirect_valkey_data
│   │
│   ├── growdirect_pgadmin    (dpage/pgadmin4:latest)
│   │     Listens on 127.0.0.1:5050 (host) / 80 (container)
│   │     Depends on: postgres (healthy)
│   │     Volumes: growdirect_pgadmin_data
│   │
│   ├── growdirect_ollama     (ollama/ollama)
│   │     Listens on 127.0.0.1:11434 (host) / 11434 (network)
│   │     Volumes: growdirect_ollama_data
│   │
│   └── growdirect_memory_bus (growdirect-memory-bus, built from services/memory-bus/)
│         Listens on 127.0.0.1:8003 (host) / 8003 (network)
│         Depends on: postgres (healthy)
│
├── Canary/devops/docker-compose.yml  ← app stack (joins growdirect network)
│   └── canary_flask          (canary-flask)
│         Port 5001 → container 5000
│         Env: DATABASE_URL → growdirect_postgres/canary
│         Env: VALKEY_URL   → growdirect_valkey/0
│
└── Cove/devops/docker-compose.yml    ← app stack (joins growdirect network)
    ├── cove_flask            (cove-flask)
    │     Port 5002 → container 5000
    │     Env: DATABASE_URL → growdirect_postgres/cove
    │     Env: VALKEY_URL   → growdirect_valkey/1
    ├── cove_knowledge_mcp    (cove-knowledge-mcp, stdio MCP)
    └── cove_localhost_mailhog

All containers above share:
    Docker network: growdirect (bridge, external to app stacks)
```

### Request / Data Flow

**App → Database:**
1. App Flask container resolves `growdirect_postgres` via Docker DNS on the `growdirect` network.
2. SQLAlchemy connection pool connects to `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/<appname>`.
3. Pool is configured with `pool_pre_ping=True` and `pool_recycle=300` seconds (Cove; Canary uses default SQLAlchemy pool settings).

**App → Valkey (sessions):**
1. Flask-Session resolves `growdirect_valkey` via Docker DNS.
2. Each app connects to its own Valkey logical database: Canary uses DB 0, Cove uses DB 1.
3. Valkey requires password authentication (`valkey_dev`).
4. Connection string format: `redis://:valkey_dev@growdirect_valkey:6379/<db_number>`.

**App → Ollama (embeddings):**
1. Embedding service code calls `http://growdirect_ollama:11434`.
2. Model: `qwen3-embedding:8b` (1024-dimension vectors, Matryoshka truncated from 4096d).
3. If Ollama is unreachable, embedding services return `None` and callers handle gracefully.

**Agent → Memory Bus (knowledge retrieval):**
1. ALX or a builder agent calls Memory Bus MCP tools via streamable-HTTP transport at `http://growdirect_memory_bus:8003`.
2. Memory Bus connects to `growdirect_memory` database on `growdirect_postgres`.
3. Semantic search uses pgvector cosine distance (`<=>` operator) against the `embedding vector(1024)` column.
4. Falls back to PostgreSQL full-text search, then ILIKE if no vector match exists.

**Init sequence (first boot):**
1. `postgres` container starts; Docker runs all scripts in `devops/init-db/` in filename order.
2. `01-create-databases.sql` creates all app databases, enables extensions, creates schemas, and sets up roles.
3. `02-create-memory-db.sql` creates `growdirect_memory` and `growdirect_memory_test` schemas and tables.
4. Init scripts are idempotent (`IF NOT EXISTS` guards throughout). They only run on a fresh data volume.

### Key Design Decisions

**One PostgreSQL instance, many databases.** All apps share a single Postgres container. Isolation is enforced at the database level (each app has its own database) and, within Canary, at the schema level (`app`, `sales`, `metrics`). This reduces operational overhead compared to per-app database containers.

**External Docker network.** The `growdirect` network is declared as the `default` network in the shared compose file and as `external: true` in each app's compose file. This means the network survives `docker compose down` on any individual app stack, and apps can join or leave without restarting shared services.

**Valkey logical database isolation.** Multiple apps share one Valkey instance. Isolation is enforced using Valkey's numbered logical databases (DB 0 = Canary, DB 1 = Cove). This avoids key namespace collisions without running separate Valkey containers.

**Named Docker volumes.** All persistent volumes use explicit `name:` declarations (`growdirect_pgdata`, `growdirect_valkey_data`, `growdirect_pgadmin_data`, `growdirect_ollama_data`). This prevents Docker Compose from generating prefixed names that vary by working directory.

**Memory Bus as a platform service.** The Memory Bus MCP server runs in the shared devops stack (not per-app). All AI agents (ALX, builders) connect to it for platform-wide knowledge. Its own database (`growdirect_memory`) is provisioned by the init scripts alongside app databases.

**Host-only port binding.** All ports are bound to `127.0.0.1` on the host, not `0.0.0.0`. This prevents accidental external exposure of dev credentials. Inter-container communication uses Docker network DNS and does not traverse the host.

---

## 3. Data Model

The shared Postgres instance contains six databases provisioned by the init scripts. Note: this section documents database-level structure (databases, schemas, extensions, roles), not SQLAlchemy models — those are documented in per-app SDDs.

### Database Inventory

| Database | Owner | Purpose | Schemas |
|----------|-------|---------|---------|
| `growdirect` | growdirect | Default database created by Postgres image (unused by apps) | public |
| `canary` | growdirect | Canary production data | app, sales, metrics, public |
| `canary_test` | growdirect | Canary test runner — recreated per CI run | app, sales, metrics, public |
| `growdirect_memory` | growdirect | Platform memory bus — ALX sessions and embeddings | public |
| `growdirect_memory_test` | growdirect | Memory bus test runner — identical schema | public |
| `cove` | growdirect | Cove production data | public |
| `cove_test` | growdirect | Cove test runner — recreated per CI run | public |

### Extensions Enabled Per Database

All app databases have the same three extensions. They are enabled by the init scripts at database creation time.

| Extension | Purpose | Enabled in |
|-----------|---------|-----------|
| `vector` (pgvector) | Vector similarity search with `<=>` cosine distance operator | All databases |
| `pgcrypto` | `gen_random_uuid()`, cryptographic hashing | All databases |
| `uuid-ossp` | `uuid_generate_v4()` for UUID generation | All databases |

### Canary Schema Layout

Canary is the only app using multiple schemas within its database. This separation enforces write-path isolation between the application layer and the data ingestion layer.

| Schema | Purpose | Write-access roles |
|--------|---------|-------------------|
| `app` | Application domain models (merchants, alerts, cases, users) | `growdirect`, `canary_app` |
| `sales` | Square transaction and payment data ingested by TSP | `growdirect`, `canary_tsp` |
| `metrics` | Derived analytics and aggregation tables | `growdirect`, `canary_app` |
| `public` | Shared utilities and extensions | `growdirect`, `canary_app` |

### Canary Database Roles

Two dedicated database roles enforce write-path isolation (SOX compliance intent). Both are created idempotently by the init script.

| Role | Login password (dev) | Read | Write |
|------|---------------------|------|-------|
| `canary_app` | `canary_app_dev_2026` | Full DML on `app`, `metrics`, `public`; SELECT-only on `sales` | INSERT/UPDATE/DELETE on `app`, `metrics` |
| `canary_tsp` | `canary_tsp_dev_2026` | SELECT-only on `app` | Full DML on `sales` |

Both roles have access to `canary_test` with the same privilege structure.

### Memory Bus Schema

The `growdirect_memory` database has three tables, all created directly by `02-create-memory-db.sql` (not via Alembic). The `growdirect_memory_test` database has an identical schema.

#### `alx_sessions`

Tracks the lifecycle of ALX working sessions. Each session is created when ALX starts work on one or more GRO issues and closed when work ends.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key, `gen_random_uuid()` |
| `session_id` | TEXT UNIQUE NOT NULL | Human-readable session identifier |
| `started_at` | TIMESTAMPTZ | Defaults to `NOW()` |
| `closed_at` | TIMESTAMPTZ | NULL while session is active |
| `status` | TEXT | CHECK: `active`, `closed`, `abandoned` |
| `gro_issues` | JSONB | Array of GRO issue identifiers associated with session |
| `summary` | TEXT | Human-readable session summary written on close |
| `decisions` | JSONB | Array of key decisions made during session |
| `unresolved` | JSONB | Array of open items or questions not resolved |
| `created_at` | TIMESTAMPTZ | Row creation timestamp |
| `updated_at` | TIMESTAMPTZ | Auto-updated by trigger |

Indexes: `status`, `started_at DESC`.

#### `alx_memories`

Stores individual memory items with embeddings for semantic retrieval. Memories are tagged with a `layer` to scope retrieval to a specific app or platform context.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key, `gen_random_uuid()` |
| `session_id` | TEXT NOT NULL | References `alx_sessions.session_id` (soft FK, not enforced) |
| `memory_type` | TEXT NOT NULL | CHECK: `decision`, `finding`, `context`, `architecture`, `session_summary`, `procedure`, `context_block`, `work_product`, `team_profile`, `foundation` |
| `content` | TEXT NOT NULL | Full memory text, max 6000 characters (enforced in Memory Bus config) |
| `metadata` | JSONB | Arbitrary metadata (source file, GRO issue, etc.) |
| `embedding` | vector(1024) | pgvector column; NULL if Ollama was unreachable at store time |
| `layer` | TEXT NOT NULL | CHECK: `corp`, `canary`, `cove`, `shared`; default `shared` |
| `created_at` | TIMESTAMPTZ | Row creation timestamp |
| `updated_at` | TIMESTAMPTZ | Auto-updated by trigger |

Indexes: `session_id`, `memory_type`, `created_at DESC`, `layer`.

#### `seed_embeddings`

Curated knowledge base of platform documentation sections, pre-embedded for RAG retrieval. Sourced from CLAUDE.md files, SDDs, and other platform documents by the seed script (`services/memory-bus/scripts/seed_clean.py`).

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key, `gen_random_uuid()` |
| `source_file` | TEXT NOT NULL | Source document path |
| `section_path` | TEXT NOT NULL | Hierarchical path within document (e.g., `Auth Pattern > Magic Link`) |
| `content` | TEXT NOT NULL | Text content of the section |
| `embedding` | vector(1024) NOT NULL | Required — seed entries without embeddings are not inserted |
| `metadata` | JSONB | Additional context (document type, namespace, etc.) |
| `created_at` | TIMESTAMPTZ | Defaults to `NOW()` |
| `updated_at` | TIMESTAMPTZ | Auto-updated by trigger |

Indexes: HNSW index on `embedding` using `vector_cosine_ops` (enables fast approximate nearest-neighbor search), `source_file`.

### Database Triggers

All three memory bus tables have `BEFORE UPDATE` triggers that call `update_updated_at_column()`, which sets `NEW.updated_at = NOW()`. The same trigger function and trigger definitions are duplicated in the `growdirect_memory_test` database.

---

## 4. Interfaces

### Port Allocation Map

All host ports are bound to `127.0.0.1` only, not `0.0.0.0`.

| Service | Container name | Host port | Container port | Protocol |
|---------|---------------|-----------|----------------|----------|
| PostgreSQL | `growdirect_postgres` | 5432 | 5432 | TCP (PostgreSQL wire) |
| Valkey | `growdirect_valkey` | 6379 | 6379 | TCP (RESP) |
| pgAdmin | `growdirect_pgadmin` | 5050 | 80 | HTTP |
| Ollama | `growdirect_ollama` | 11434 | 11434 | HTTP (REST) |
| Memory Bus | `growdirect_memory_bus` | 8003 | 8003 | HTTP (MCP streamable-HTTP) |
| Canary Flask | `canary_flask` | 5001 | 5000 | HTTP (Gunicorn) |
| Canary Owl MCP | `canary_owl_mcp` | 8001 | — | HTTP (MCP) |
| Canary QA Agent | `canary_qa_agent` | 8002 | — | HTTP |
| Cove Flask | `cove_flask` | 5002 | 5000 | HTTP (Gunicorn) |
| Cove MailHog SMTP | `cove_localhost_mailhog` | 1026 | 1025 | SMTP |
| Cove MailHog Web | `cove_localhost_mailhog` | 8026 | 8025 | HTTP |

### Docker Network Topology

The `growdirect` network is a Docker bridge network. It is the `default` network in the shared devops compose file, so all shared-infra containers join it automatically. App stacks declare it as `external: true`.

```yaml
# devops/docker-compose.yml
networks:
  default:
    name: growdirect

# App compose files (e.g. Cove/devops/docker-compose.yml)
networks:
  growdirect:
    external: true
```

Within the network, containers resolve each other by container name via Docker's internal DNS. The canonical hostnames used by all apps:

| Resource | Hostname (within growdirect network) | Port |
|----------|-------------------------------------|------|
| PostgreSQL | `growdirect_postgres` | 5432 |
| Valkey | `growdirect_valkey` | 6379 |
| Ollama | `growdirect_ollama` | 11434 |
| Memory Bus | `growdirect_memory_bus` | 8003 |

### Volume Mount Conventions (Development)

In development, app Flask containers mount all code directories as Docker volumes so that Gunicorn's `--reload` flag picks up file changes without a container rebuild.

**Required mounts (all must be present if any are present):**

| Host path (relative to app root) | Container path |
|----------------------------------|---------------|
| `<appname>/` | `/app/<appname>/` |
| `templates/` | `/app/templates/` |
| `static/` | `/app/static/` |
| `wsgi.py` | `/app/wsgi.py` |
| `migrations/` | `/app/migrations/` |

**Never mounted:**

| Path | Reason |
|------|--------|
| `.env` | Contains secrets; baked into compose `environment:` or `env_file:` |
| `requirements.txt` | Baked into image at build time; mount would shadow installed packages |
| `node_modules/` | Large binary tree; baked into image |

**QA / production:** Nothing is mounted. All code is baked into the image via `COPY` in the Dockerfile.

### Docker Rebuild Rules

| Change type | Required action |
|-------------|----------------|
| Python files, Jinja2 templates, static assets | None — volume-mounted, Gunicorn `--reload` picks up changes automatically |
| `requirements.txt` (new package added) | `docker compose build flask && docker compose up -d flask` |
| `Dockerfile` modified | `docker compose up -d --force-recreate flask` |
| `docker-compose.yml` modified | `docker compose up -d --force-recreate <service>` |

`ModuleNotFoundError` in container logs always means the image needs a rebuild. Do not modify Python code to work around a missing package.

### Image Naming Convention

Every service with a `build:` block must have an explicit `image:` tag. Without this, Docker Compose derives image names from the compose file's parent directory. Because all apps store their compose files in `devops/`, services with the same name (e.g., `flask`) would collide — starting one app would silently clobber the other's image.

Pattern: `image: <appname>-<service>`

Examples:
- `canary-flask`
- `cove-flask`
- `cove-knowledge-mcp`
- `growdirect-memory-bus`

### Project Name Convention

Every app compose file must declare a top-level `name:` field. Without it, Docker Compose derives the project name from the directory (`devops` for all apps), causing cross-app container conflicts.

Examples:
- `name: cove` (Cove/devops/docker-compose.yml)
- `name: canary` (Canary devops compose)

The shared devops stack does not declare an explicit `name:` — it is uniquely identified by its location.

---

## 5. Service Layer

N/A — Shared infrastructure is not a Flask application and does not have a service layer in the GrowDirect sense. There are no routes, blueprints, or SQLAlchemy service classes. The Memory Bus MCP server exposes tools (not HTTP routes) and is documented separately in `docs/sdds/platform/memory-bus.md`.

The infrastructure exists as configuration (Docker Compose), SQL init scripts, and Docker volumes. "Services" in this context are Docker services, not Flask services.

---

## 6. Configuration

### Shared Infrastructure Environment Variables

These environment variables are set directly in `devops/docker-compose.yml` and control the shared services.

#### PostgreSQL (`growdirect_postgres`)

| Variable | Value | Purpose |
|----------|-------|---------|
| `POSTGRES_USER` | `growdirect` | Superuser account for all databases |
| `POSTGRES_PASSWORD` | `growdirect_dev` | Dev credential — never use in production |
| `POSTGRES_DB` | `growdirect` | Default database created by image entrypoint (not used by apps) |

#### Valkey (`growdirect_valkey`)

| Variable / Flag | Value | Purpose |
|----------------|-------|---------|
| `--requirepass` | `valkey_dev` | Password required for all connections |

#### pgAdmin (`growdirect_pgadmin`)

| Variable | Value | Purpose |
|----------|-------|---------|
| `PGADMIN_DEFAULT_EMAIL` | `admin@growdirect.com` | Login email |
| `PGADMIN_DEFAULT_PASSWORD` | `admin` | Login password (dev only) |
| `PGADMIN_LISTEN_PORT` | `80` | Internal HTTP port |
| `PGADMIN_CONFIG_SERVER_MODE` | `False` | Disables multi-user server mode (single dev use) |
| `PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED` | `True` | Requires master password for pgAdmin |

#### Memory Bus (`growdirect_memory_bus`)

| Variable | Value | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | `postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/growdirect_memory` | Memory database connection |
| `OLLAMA_URL` | `http://growdirect_ollama:11434` | Embedding inference endpoint |
| `EMBEDDING_MODEL` | `qwen3-embedding:8b` | Model name passed to Ollama |
| `PORT` | `8003` | MCP server listen port |

Internal Memory Bus config constants (from `services/memory-bus/memory_bus/config.py`):

| Constant | Value | Purpose |
|----------|-------|---------|
| `embedding_dimensions` | `1024` | Vector dimension — must match `Vector(1024)` in schema |
| `max_text_length` | `6000` | Character limit enforced before embedding; prevents oversized Ollama requests |

### App-Side Connection Strings

Apps set these in their compose `environment:` block (dev) or `.env` file (secrets). The `.env` file is gitignored and never committed.

#### Standard Pattern (Cove — follows platform standard exactly)

```
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
VALKEY_URL=redis://:valkey_dev@growdirect_valkey:6379/1
OLLAMA_URL=http://growdirect_ollama:11434
```

Cove's `BaseConfig` reads these as:
```python
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]   # required — raises KeyError if missing
VALKEY_URL = os.environ.get("VALKEY_URL", "redis://localhost:6379/1")
SESSION_TYPE = "redis"   # Flask-Session uses VALKEY_URL via SESSION_REDIS set in create_app
```

Cove `TestConfig` overrides the database URI using `TEST_DATABASE_URL` (falls back to `cove_test`):
```python
SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "postgresql://growdirect:growdirect_dev@localhost:5432/cove_test")
SESSION_TYPE = "null"   # Flask default cookie session; no Valkey needed in tests
```

#### Canary Config Pattern (diverges from platform standard in three areas)

```
DATABASE_URL=postgresql://canary:canary@localhost:5432/canary   # dev fallback default
RATE_LIMIT_STORAGE_URI=redis://valkey:6379/1                    # hardcoded in extensions.py
```

Canary's `Config` base class reads:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://canary:canary@localhost:5432/canary")
```

Note: The Canary base config fallback (`canary:canary@localhost`) references a user and host that do not match the shared infra credentials (`growdirect:growdirect_dev@growdirect_postgres`). When running inside Docker, `DATABASE_URL` must be explicitly set in the compose `environment:` block, which overrides the fallback.

Canary `TestingConfig` reads:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://growdirect:growdirect_dev@localhost:5432/canary_test")
```

The testing fallback does use the correct `growdirect` credentials.

Canary does not use `Flask-Session` — it uses a different session management approach and does not declare `SESSION_TYPE = "redis"` in its config class.

### SQLAlchemy Pool Settings

| App | `pool_pre_ping` | `pool_recycle` | Notes |
|-----|----------------|---------------|-------|
| Cove | `True` | 300s | Explicitly set in `SQLALCHEMY_ENGINE_OPTIONS` |
| Canary | Default | Default | Uses SQLAlchemy defaults; pool settings not overridden |

---

## 7. Security & Compliance

### Network Isolation

- All host-side ports are bound to `127.0.0.1`, preventing access from any network interface other than loopback. This applies to PostgreSQL (5432), Valkey (6379), pgAdmin (5050), Ollama (11434), and Memory Bus (8003).
- The `growdirect` Docker bridge network is internal. Containers communicate with each other without traversing the host network stack.
- App containers that do not join the `growdirect` network have no path to the shared services.

### Credential Management

- Dev credentials are hardcoded in Docker Compose environment blocks. These are development-only values, not used in production.
- App secrets (API keys, `SECRET_KEY`, Square tokens) are stored in each app's `.env` file, which is gitignored. The `.env` file is loaded via `env_file:` in the app's compose file.
- The shared devops compose file does not use `.env` files — all shared-service credentials are declared inline in the compose file as they are inherently non-secret dev values.
- `SECRET_KEY` is required at runtime by both apps. Cove raises `KeyError` on startup if missing (`os.environ["SECRET_KEY"]`). Canary uses a fallback (`dev-secret-change-in-production`) that is unsafe for production but does not crash on startup.

### PostgreSQL Authentication

- Single superuser account (`growdirect` / `growdirect_dev`) owns all databases.
- Canary additionally uses two restricted roles (`canary_app`, `canary_tsp`) for write-path isolation. These roles have schema-scoped privileges set via `ALTER DEFAULT PRIVILEGES`.
- All roles use password authentication (`md5` or `scram-sha-256` depending on Postgres `pg_hba.conf` defaults in the pgvector image).
- The `growdirect` default database is created by the image but not used by any app, reducing attack surface.

### Valkey Authentication

- Password authentication is required via `--requirepass valkey_dev`.
- Apps must include the password in the connection string: `redis://:valkey_dev@growdirect_valkey:6379/<db>`.
- Logical database separation (DB 0 = Canary, DB 1 = Cove) prevents accidental session key collisions between apps but does not prevent cross-app access if credentials are shared — both apps use the same Valkey password.

### Session Security

Cove `ProdConfig` enforces:
```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
REMEMBER_COOKIE_SECURE = True
REMEMBER_COOKIE_HTTPONLY = True
```

Canary `ProductionConfig` enforces:
```python
SESSION_COOKIE_SECURE = True
```

Both apps disable `CSRF` only in test config; it is enabled (`WTF_CSRF_ENABLED = True`) in all non-test environments.

### pgAdmin Security Notes

- pgAdmin is configured with `PGADMIN_CONFIG_SERVER_MODE = "False"` — it runs in desktop mode, suitable for single-developer use only.
- pgAdmin is never deployed to production environments.
- pgAdmin's login credentials (`admin` / `admin`) are intentionally minimal for local dev.

---

## 8. Error Handling

### Container Restart Policies

All five shared-infra services are configured with `restart: unless-stopped`. This means:

- Containers restart automatically after a crash, after Docker daemon restart, or after host reboot.
- Containers do NOT restart if explicitly stopped with `docker compose stop` or `docker compose down`.

### Health Checks

Each service defines a health check used by Docker and by dependent services via `condition: service_healthy`.

| Service | Health check command | Interval | Start period | Retries |
|---------|---------------------|----------|-------------|---------|
| `postgres` | `pg_isready -U growdirect` | 5s | 10s | 10 |
| `valkey` | `valkey-cli -a valkey_dev ping` | 5s | — | 5 |
| `pgadmin` | `wget -q --spider http://localhost:80/misc/ping` | 15s | 30s | 3 |
| `ollama` | `curl -sf http://localhost:11434/api/tags` | 10s | 30s | 5 |
| `memory-bus` | `curl -sf http://localhost:8003/health` | 10s | 15s | 5 |

Dependency ordering:
- `pgadmin` waits for `postgres: healthy` before starting.
- `memory-bus` waits for `postgres: healthy` before starting.
- App containers (Canary, Cove) declare their own health checks against `/health` routes and should be started after shared infra is healthy.

### Behavior When Services Are Unavailable

| Service down | Effect on apps |
|-------------|---------------|
| `growdirect_postgres` | All app requests that touch the database fail. Flask returns 500 errors. SQLAlchemy connection pool exhausts retries and raises `OperationalError`. |
| `growdirect_valkey` | Session reads/writes fail. For Cove, `Flask-Session` is backed by Valkey — authenticated requests will fail to load sessions, effectively logging out all users. |
| `growdirect_ollama` | Embedding generation returns `None`. Cove's `generate_embedding()` returns `None` gracefully; callers must handle this. Memory Bus falls back to full-text or ILIKE search. Features that require embeddings degrade gracefully; app startup is unaffected. |
| `growdirect_memory_bus` | Memory Bus MCP tools become unavailable. AI agent sessions cannot store or recall memories. App containers are unaffected — they do not depend on Memory Bus at runtime. |

### Canary Rate Limiter Fallback

Canary's `limiter` in `extensions.py` is configured with `storage_uri=os.getenv("RATE_LIMIT_STORAGE_URI", "redis://valkey:6379/1")`. If Valkey is unreachable, `flask-limiter` uses an in-memory fallback by default, which resets on container restart and is not shared across workers. This is acceptable degradation in dev but would be a concern in a multi-worker production deployment.

### Init Script Idempotency

The `CREATE DATABASE` statements in `01-create-databases.sql` use `SELECT ... WHERE NOT EXISTS ... \gexec` pattern. All `CREATE EXTENSION IF NOT EXISTS`, `CREATE SCHEMA IF NOT EXISTS`, `CREATE TABLE IF NOT EXISTS`, and `CREATE INDEX IF NOT EXISTS` statements are idempotent. If the init scripts are re-run manually against an existing database, they do not fail and do not duplicate objects.

---

## 9. Testing

N/A for shared infrastructure as a unit — there are no pytest test suites that validate the Docker Compose stack itself.

Infrastructure health is verified indirectly:

- **App smoke tests** include a `/health` route check that fails if the app cannot connect to its database. Running `pytest tests/smoke/` for any app implicitly validates that the database and Valkey are reachable.
- **Memory Bus has its own test suite** at `services/memory-bus/tests/` covering config, embeddings, context block assembly, RAG retrieval, and a smoke test against `growdirect_memory_test`. These run against the `growdirect_memory_test` database.
- **Manual preflight** is performed by the `factory-preflight` skill before any factory build session. The skill checks that all required containers are healthy before any code changes begin.

To verify shared infra health manually:

```bash
# Check all container statuses
cd ~/GrowDirect/devops && docker compose ps

# Test PostgreSQL connectivity
docker exec growdirect_postgres pg_isready -U growdirect

# Test Valkey connectivity
docker exec growdirect_valkey valkey-cli -a valkey_dev ping

# Test Ollama API
curl -sf http://localhost:11434/api/tags | python3 -m json.tool

# Test Memory Bus health endpoint
curl -sf http://localhost:8003/health
```

---

## 10. Dependencies

### Shared Infrastructure Dependencies

| Service | Image | Version | Purpose |
|---------|-------|---------|---------|
| PostgreSQL + pgvector | `pgvector/pgvector` | `pg17` | Relational database with vector extension |
| Valkey | `valkey/valkey` | `8-alpine` | Redis-compatible key-value store |
| pgAdmin | `dpage/pgadmin4` | `latest` | Database admin UI |
| Ollama | `ollama/ollama` | `latest` | Local LLM inference |
| Memory Bus | `growdirect-memory-bus` | built from source | Platform memory MCP server |

### Memory Bus Python Dependencies

The Memory Bus service is a standalone Python application (`services/memory-bus/`). Key dependencies from `pyproject.toml`:

| Package | Purpose |
|---------|---------|
| `mcp[server]` (FastMCP) | MCP server framework; `streamable-http` transport |
| `psycopg2` or `psycopg` | PostgreSQL driver |
| `pgvector` | Python bindings for pgvector types |
| `httpx` or `requests` | HTTP client for Ollama API calls |

### App Dependencies on Shared Infrastructure

| App | Package | Shared service used |
|-----|---------|-------------------|
| Canary | `SQLAlchemy` 2.0, `psycopg2` | PostgreSQL |
| Canary | `flask-limiter` | Valkey (rate limit counters) |
| Cove | `Flask-SQLAlchemy`, `psycopg2` | PostgreSQL |
| Cove | `Flask-Session` | Valkey (session storage) |
| Cove | `httpx` / `requests` (embedding service) | Ollama |

### Startup Order Dependency

```
growdirect_postgres (healthy)
    ↓
growdirect_pgadmin
growdirect_memory_bus
    ↓
canary_flask (app health check passes)
cove_flask (app health check passes)
```

`growdirect_valkey` and `growdirect_ollama` have no declared startup dependencies — they start in parallel with `growdirect_postgres`.

---

## 11. Known Issues & Reconciliation

### Canary Config Does Not Follow Platform Standard

The platform standard (`CLAUDE.md`) specifies config classes named `BaseConfig`, `DevConfig`, `TestConfig`, `ProdConfig`. Cove follows this exactly. Canary uses `Config`, `DevelopmentConfig`, `ProductionConfig`, `TestingConfig` — different class names and a different environment variable (`CANARY_ENV` instead of `FLASK_ENV`).

Additionally, Canary's `Config` base class uses `os.getenv()` with an insecure fallback for `DATABASE_URL` (`postgresql://canary:canary@localhost:5432/canary`). Cove uses `os.environ["DATABASE_URL"]` (raises `KeyError` if absent). The platform standard specifies `os.environ["DATABASE_URL"]` (no fallback). Canary's fallback silently connects to a non-existent user if the env var is not set.

**Status:** Inconsistency exists. Canary config predates the current platform standard. Aligning Canary to `BaseConfig`/`DevConfig`/`TestConfig`/`ProdConfig` naming and removing the insecure fallback is tracked as future cleanup.

### Canary Does Not Use Flask-Session

Cove uses `Flask-Session` backed by Valkey (DB 1). Canary uses Flask's default cookie-based sessions or a custom session mechanism — it does not import `Flask-Session` and does not declare `SESSION_TYPE = "redis"` in its config. Canary does use Valkey for rate limiting only.

**Status:** Intentional divergence or legacy gap. If Canary requires server-side sessions (e.g., for Magic Link or OAuth state), this should be aligned with the platform session standard (Valkey-backed Flask-Session).

### Canary Rate Limiter Uses Hardcoded Valkey DB

`Canary/canary/extensions.py` hardcodes `redis://valkey:6379/1` as the default `RATE_LIMIT_STORAGE_URI`. The hostname `valkey` (not `growdirect_valkey`) may not resolve correctly depending on Docker network configuration. Additionally, DB 1 is allocated to Cove sessions — using the same logical database for Canary rate limit counters creates a key namespace risk.

**Status:** The env var `RATE_LIMIT_STORAGE_URI` overrides this when set. However, the fallback is incorrect for the shared network hostname and the wrong Valkey DB. Canary rate limiting should use DB 0 (Canary's allocated DB) and hostname `growdirect_valkey`.

### Init Scripts Only Run on Fresh Volumes

`devops/init-db/` scripts execute only when PostgreSQL starts with an empty data volume. If the `growdirect_pgdata` volume already exists, adding a new database to `01-create-databases.sql` will have no effect until the volume is wiped or the SQL is run manually.

**Workaround documented in `devops/README.md`:**
```bash
docker exec -it growdirect_postgres psql -U growdirect -c "CREATE DATABASE <appname> OWNER growdirect;"
docker exec -it growdirect_postgres psql -U growdirect -d <appname> -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### pgAdmin Uses `latest` Tag

`growdirect_pgadmin` is pinned to `dpage/pgadmin4:latest`. All other images use explicit version tags (`pg17`, `8-alpine`). `latest` can change behavior unexpectedly after a Docker image pull.

**Status:** Low risk (pgAdmin is dev-only, not in the request path). Pin to a specific version when next updating the compose file.

### Memory Bus Schema Not Managed by Alembic

The `growdirect_memory` tables are created directly by `02-create-memory-db.sql`, not through Alembic migrations. Schema changes require either manual SQL execution or a volume wipe.

**Status:** Acceptable for now given the memory bus is a platform service without a SQLAlchemy model layer. If the schema evolves significantly, a lightweight migration strategy should be introduced.
