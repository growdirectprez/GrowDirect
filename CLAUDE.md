# GrowDirect Platform Standards

GrowDirect builds enterprise SaaS tools using a factory process for consistent delivery.
Every app reads this file first. App-specific CLAUDE.md adds domain context on top.

**Apps:** Canary (loss prevention for Square merchants) · Cove (HOA governance)

---

## Tech Stack

- Python 3.12 (always `python3`, never `python`)
- Flask 3+ with Jinja2 templates — server-rendered, not an SPA
- SQLAlchemy 2.0 with `Mapped[]` syntax — no legacy `Column()` patterns
- PostgreSQL 17 with pgvector extension — no SQLite, ever
- Valkey 8 — session store, cache, background task queue
- Gunicorn (production), `--reload` flag in dev
- Alembic for database migrations
- pytest for testing (unit, integration, smoke layers)

### CSS / Frontend

- Tailwind 3.x with PostCSS build pipeline — `postcss-import`, `tailwindcss`, `autoprefixer` — no CDN
- Each app: `static/css/<appname>.css` with component classes using `@apply`; output → `static/css/dist/main.css`
- If a utility pattern appears more than twice, it becomes a component class
- Alpine.js 3.x via npm for interactivity; Leaflet.js via npm for maps (only where needed)
- All JS/CSS via npm — no CDN dependencies
- Forms: WTForms, server-side validation, inline error display below each field

### Embeddings

- Ollama — shared service at `http://growdirect_ollama:11434`
- Model: `qwen3-embedding:8b` (1024 dimensions, via litellm routing)
- Vector column: `Vector(1024)` on models that need semantic search
- Similarity search: cosine distance (`<=>` operator)

---

## Shared Infrastructure

All apps share one Docker Compose stack. Start it first, then start the app.

```
~/GrowDirect/devops/docker-compose.yml runs:
  growdirect_postgres   :5432  — all app databases in one instance
  growdirect_valkey     :6379  — sessions and cache
  growdirect_pgadmin    :5050  — database admin (http://localhost:5050)
  growdirect_ollama     :11434 — embedding and LLM inference
```

Network: `growdirect` (external — all app containers join this)

**Start shared infra:**
```bash
cd ~/GrowDirect/devops && docker compose up -d
```

**Start an app:**
```bash
cd ~/GrowDirect/<App>/devops && docker compose up -d
```

App compose files declare `networks: growdirect: external: true` — they connect
to the shared network; they do NOT start their own postgres or valkey.

---

## Database Layout

One PostgreSQL 17 instance (`growdirect_postgres`). All databases have the
`vector`, `pgcrypto`, and `uuid-ossp` extensions enabled.

| Database | Owner | Purpose |
|----------|-------|---------|
| `canary` | growdirect | Canary production (schemas: app, sales, metrics) |
| `canary_test` | growdirect | Canary test runs |
| `canary_memory` | growdirect | ALX agent knowledge graph |
| `cove` | growdirect | Cove production |
| `cove_test` | growdirect | Cove test runs |

**Dev credentials:** `growdirect / growdirect_dev`

Databases are created by `devops/init-db/01-create-databases.sql` on first boot.
To add a new app, add `CREATE DATABASE <appname>` to that file and connect the
app's flask container to the `growdirect` network.

**Valkey DB allocation:**
- DB 0 → Canary
- DB 1 → Cove

---

## App Structure

Each app is a separate directory with its own:

```
<App>/
├── CLAUDE.md                        # App context — references this parent
├── .claude/
│   ├── skills/                      # App-specific skills (delegate to platform skills)
│   └── settings.json                # App-specific permissions
├── devops/
│   └── docker-compose.yml           # App services only (flask + app-specific like nginx, mailhog)
├── .env                             # App secrets (gitignored)
├── wsgi.py                          # WSGI entry point
├── <appname>/                       # Python source
├── templates/                       # Jinja2 templates
├── static/                          # CSS, JS, images
└── migrations/                      # Alembic versions
```

---

## Port Allocation

| Service | Port |
|---------|------|
| Shared Postgres | 5432 |
| Shared Valkey | 6379 |
| Shared pgAdmin | 5050 |
| Shared Ollama | 11434 |
| Canary Flask | 5001 |
| Canary nginx | 443 / 80 |
| Canary Owl MCP | 8001 |
| Canary QA Agent | 8002 |
| Cove Flask | 5002 |
| Cove MailHog SMTP | 1026 |
| Cove MailHog Web | 8026 |

---

## Volume Mounting Rules

**Dev:** mount ALL code directories consistently. If one is mounted, all must be:
- `<app>/` — Python source
- `templates/` — Jinja2 templates
- `static/` — CSS, JS, images
- `wsgi.py` — entry point
- `migrations/` — Alembic versions

**Never mount:** `.env`, `requirements.txt`, `node_modules/`

**QA / prod:** nothing is mounted — everything is baked into the image.

---

## Docker Rebuild Rules

| Change type | Action required |
|-------------|----------------|
| Python files, templates, static assets | None — volume-mounted, Gunicorn `--reload` picks up changes |
| `requirements.txt` (new package) | `docker compose build flask` then `up -d flask` |
| `Dockerfile` or compose changes | `docker compose up -d --force-recreate flask` |

`ModuleNotFoundError` in container logs = image needs rebuild. Do NOT modify Python code to work around a missing package.

### Docker Image Naming — Required

Every service with a `build:` block **must** have an explicit `image:` tag prefixed
with the app name. Without this, Docker Compose derives image names from the
directory + service name (e.g., `devops-flask`). Since all apps keep their compose
files in `devops/`, services with the same name (like `flask`) collide — starting
one app silently clobbers the other's image.

**Pattern:** `image: <appname>-<service>`

```yaml
# Canary
flask:
  image: canary-flask        # ← REQUIRED — prevents collision with cove-flask
  build:
    context: ..
    dockerfile: Dockerfile

# Cove
flask:
  image: cove-flask           # ← REQUIRED — prevents collision with canary-flask
  build:
    context: ../
    dockerfile: Dockerfile
```

**Rule:** If you add a `build:` block to any compose service, you must also add
`image: <appname>-<descriptive-name>`. No exceptions. Services that reuse the
same Dockerfile (e.g., TSP consumers reusing the Flask image) should reference
the same image name so Docker builds once and reuses.

### Docker Compose Project Names — Required

Every app compose file **must** have a top-level `name:` field. Without it,
Docker Compose derives the project name from the directory containing the compose
file. Since all apps store compose files in `devops/`, they all get project name
`devops` — causing one app's `docker compose up` to see the other app's containers
as orphans and potentially recreate or remove them.

```yaml
# Top of every compose file — before services:
name: canary          # or cove, canary-qa, canary-enterprise, etc.

services:
  ...
```

**Rule:** Every compose file must declare `name: <appname>[-environment]` at the
top level. The name must be unique across all apps and environments.

---

## Model Standards

- UUID primary keys on every table (`Mapped[uuid.UUID]`, default `uuid.uuid4`)
- `created_at: Mapped[datetime]` and `updated_at: Mapped[datetime]` on every table
- Audit mixin for tables that need change tracking
- Tenant mixin for multi-org tables (`org_id` foreign key)
- Use `Mapped[]` type annotations — never `Column()`
- Relationships: `Mapped[list["Model"]]` syntax

---

## Auth Pattern

- Flask-Login for session management
- Login methods: magic link (primary), password (fallback)
- `@login_required` on every non-public route
- Role/permission model: Member belongs to Organization, has Roles, Roles have Permissions
- Session backend: Valkey (not filesystem, not database)

---

## Config Pattern

Every app uses env-based config classes. No hardcoded secrets — everything from environment or `.env`.

Four classes: `BaseConfig`, `DevConfig`, `TestConfig`, `ProdConfig`. Key fields:
- `SECRET_KEY = os.environ["SECRET_KEY"]`
- `SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]`
- `SESSION_TYPE = "redis"` (Valkey is Redis-compatible)
- `WTF_CSRF_ENABLED = True` (disabled only in `TestConfig`)
- `ProdConfig`: `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE = "Lax"`

Shared infra connection strings:
```
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/<appname>
VALKEY_URL=redis://growdirect_valkey:6379/<db_number>
OLLAMA_URL=http://growdirect_ollama:11434
```

---

## Test Standard

- pytest with `conftest.py` fixtures at project root
- Three layers: unit (models, services), integration (routes, database), smoke (health check, critical paths)
- Test database: separate from dev (`<appname>_test`), created/destroyed per test run
- Fixtures: app factory, test client, authenticated client, database session, sample data

---

## Protected Files

"Protected" means explain why before changing — not create workarounds to avoid touching.

- `.env` — secrets
- `wsgi.py` — entry point
- `<appname>/extensions.py` or `<appname>/db/session_factory.py` — database connection
- `Dockerfile` — build
- `docker-compose*.yml` — infrastructure
- Alembic `env.py` — migration config

---

## Hard Rules

1. No SQLite — PostgreSQL only
2. No lazy pipes — every service/route must be delivery complete (write test, verify data flow)
3. No file creation without cause — edit the original, never create `_v2/_new/_backup` variants
4. Canonical UUID — UUID is always the primary identifier for lookups, links, and cache keys
5. No CDN dependencies — all JS/CSS via npm and build pipeline
6. Linear is the task layer — no issue = no work, GRO number = exact scope
7. Scope control — bugs found outside scope = new Linear issue, not inline fix
8. Same problem, same solution — before implementing anything, check if the other app already solved it. Don't reinvent.

---

## Factory Process

Six stages, in order:

1. **Blueprint** — Specify what you're building (`factory-blueprint` skill)
2. **TDD** — Write failing tests first (`factory-tdd` skill)
3. **Assembly** — Implement to make tests pass (`factory-assembly` skill)
4. **Verify** — Run full test suite, check integration (`factory-verify` skill)
5. **QA** — Quality assurance pass (`factory-qa` skill)
6. **Ship** — Deployment preparation (`factory-ship` skill)

---

## Post-Mortem Process

- Agent writes post-mortem after each ship cycle
- Jeffe reviews and decides what gets promoted to platform standards
- Agent does NOT auto-update this file — human gate prevents bloat
