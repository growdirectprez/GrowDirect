# GrowDirect Platform Standards

Every GrowDirect app reads this file first. App-specific CLAUDE.md adds domain context on top.

## Tech Stack

- Python 3.12 (always `python3`, never `python`)
- Flask 3+ with Jinja2 templates
- SQLAlchemy 2.0 with `Mapped[]` syntax — no legacy `Column()` patterns
- PostgreSQL 17 with pgvector extension — no SQLite in production, ever
- Valkey 8 (session store, cache, background task queue)
- Gunicorn (production), Flask dev server (development)
- Alembic for database migrations
- pytest for testing (unit, integration, smoke layers)

## Model Standards

- UUID primary keys on every table (`Mapped[uuid.UUID]`, default `uuid.uuid4`)
- `created_at: Mapped[datetime]` and `updated_at: Mapped[datetime]` on every table
- Audit mixin for tables that need change tracking
- Tenant mixin for multi-org tables (`org_id` foreign key)
- Use `Mapped[]` type annotations, not `Column()`
- Relationships use `Mapped[list["Model"]]` syntax

## Auth Pattern

- Flask-Login for session management
- Login methods: magic link (primary), password (fallback)
- `@login_required` on every non-public route
- Role/permission model: Member belongs to Organization, has Roles, Roles have Permissions
- Session backend: Valkey (not filesystem, not database)

## Config Pattern

Every app uses env-based config classes:

```python
import os
from pathlib import Path

class BaseConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}
    SESSION_TYPE = "redis"  # Valkey is Redis-compatible
    SESSION_REDIS = None  # Set from VALKEY_URL in subclass
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit

class DevConfig(BaseConfig):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "postgresql://test:test@localhost:5432/test")
    WTF_CSRF_ENABLED = False

class StagingConfig(BaseConfig):
    SESSION_COOKIE_SECURE = True

class ProdConfig(BaseConfig):
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
```

No hardcoded secrets. Everything from environment variables or `.env` file.

## CSS Standard

- Tailwind 3.x with PostCSS build pipeline (not CDN)
- Every app has `static/css/<appname>.css` with component classes using `@apply`
- Templates use component classes, not raw Tailwind utility chains
- If a utility pattern appears more than twice, it becomes a component class
- Build: PostCSS with `postcss-import`, `tailwindcss`, `autoprefixer`
- Output: `static/css/dist/main.css` (templates reference this)
- All JS/CSS via npm — no CDN dependencies

## Frontend Standard

- Alpine.js 3.x via npm for client-side interactivity
- Leaflet.js via npm for maps (only on pages that need it)
- Server-rendered Jinja2 templates — not an SPA
- Forms: WTForms with server-side validation, inline error display below each field

## Docker Standard

Every app's compose follows this structure:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg17
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U <appname> -d <appname>"]
      interval: 5s
      start_period: 10s
      retries: 10

  valkey:
    image: valkey/valkey:8-alpine
    healthcheck:
      test: ["CMD", "valkey-cli", "ping"]
      interval: 5s
      retries: 5

  flask:
    build: ../
    command: gunicorn --bind 0.0.0.0:<port> --workers 1 --threads 4 --timeout 120 --reload wsgi:app
    depends_on:
      postgres: { condition: service_healthy }
      valkey: { condition: service_healthy }
    healthcheck:
      test: python -c "from urllib.request import urlopen; urlopen('http://localhost:<port>/health')"
      interval: 10s
      start_period: 20s
      retries: 5
```

Container naming: `<appname>_localhost_<service>`
Startup order: postgres healthy → valkey healthy → flask starts
Health checks: every service has one, always `service_healthy` conditions
Dockerfile: two-stage build, Python 3.12-slim, non-root user, EXPOSE port

## pgvector Standard

Every app gets vector search from day one:

- Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions, local, no API dependency)
- Vector column: `Vector(384)` on models that need semantic search
- Embedding on write (create/update), synchronous until scale demands async
- Similarity search: cosine distance (`<=>` operator)
- Agent memory: each app agent gets a pgvector knowledge graph for domain learning

## Valkey Standard

- Session store (Flask-Session with Redis/Valkey backend)
- Cache (frequently accessed queries, config)
- Background task queue (when needed — synchronous first, Valkey streams when scale demands)
- Every app's Docker compose includes a Valkey service

## Test Standard

- pytest with conftest.py fixtures at project root
- Three layers: unit (models, services), integration (routes, database), smoke (health check, critical paths)
- Test database: separate from dev database, created/destroyed per test run
- Fixtures: app factory, test client, authenticated client, database session, sample data

## Protected Files

These files require extra care — never casually edit:
- `.env` (secrets)
- `wsgi.py` (entry point)
- `<appname>/db/session_factory.py` or `<appname>/extensions.py` (database connection)
- `Dockerfile` (build)
- `docker-compose*.yml` (infrastructure)
- Alembic `env.py` (migration config)

## Hard Rules

1. No SQLite in production — PostgreSQL only
2. No lazy pipes — every service/route must be delivery complete (write test, verify data flow)
3. No file creation without cause — edit the original, don't create _v2/_new/_backup variants
4. Canonical UUID principle — UUID is always primary identifier
5. No CDN dependencies — all JS/CSS via npm and build pipeline
6. Linear is the task layer — no issue = no work, GRO number = exact scope
7. Scope control — bugs found outside scope = new Linear issue, not scope creep

## Factory Process

Six stages, in order:
1. **Blueprint** — Specify what you're building (factory-blueprint skill)
2. **TDD** — Write failing tests first (factory-tdd skill)
3. **Assembly** — Implement to make tests pass (factory-assembly skill)
4. **Verify** — Run full test suite, check integration (factory-verify skill)
5. **QA** — Quality assurance pass (factory-qa skill)
6. **Ship** — Deployment preparation (factory-ship skill)

## Post-Mortem Process

- Agent writes post-mortem after each ship cycle
- Jeffe reviews and decides what gets promoted to platform standards
- Agent does NOT auto-update this file — human gate prevents bloat

## Port Allocation

| App | Flask | Postgres (host) | Valkey | pgAdmin | Other |
|-----|-------|-----------------|--------|---------|-------|
| Canary | 5001 | 5432 | 6379 | 5050 | nginx 443/80, Owl 8001, QA 8002 |
| Cove | 5002 | 5433 | 6380 | 5051 | MailHog SMTP 1026, Web 8026 |
