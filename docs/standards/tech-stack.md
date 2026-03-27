# Tech Stack

Platform-wide version pins. All apps follow these. Deviations require a new Linear issue and Jeffe sign-off.

## Language & Runtime

**Python 3.12**

Always invoke as `python3`, never `python`. 3.12 gives us better error messages, `@override`, and performance gains over 3.11. Type hints use `X | Y` union syntax (not `Optional[X]`).

## Web Framework

**Flask 3+**

Jinja2 templates, Blueprints for route grouping, app factory pattern (`create_app()`). Not an SPA — server-rendered HTML is the default. Flask-Login for session management, WTForms for form validation.

## ORM

**SQLAlchemy 2.0**

`Mapped[]` syntax only — no legacy `Column()`. All models use `DeclarativeBase`. Sessions are managed at the request layer; services receive a session from the caller.

```python
from sqlalchemy.orm import Mapped, mapped_column
id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
```

Alembic handles all schema migrations. Never run raw DDL manually.

## Database

**PostgreSQL 17 + pgvector**

Docker image: `pgvector/pgvector:pg17`. No SQLite, ever — not in dev, not in tests. Every app gets pgvector from day one: `Vector(384)` columns, cosine distance (`<=>`), embedding model `sentence-transformers/all-MiniLM-L6-v2`.

## Cache

**Valkey 8**

Docker image: `valkey/valkey:8-alpine`. Redis-compatible, used for: session store (Flask-Session), query/config cache, background task queue (Valkey streams when needed). Every app's compose includes a Valkey service.

## Frontend

**Tailwind 3.x** — utility-first CSS, PostCSS build pipeline (not CDN). Component classes via `@apply` when a pattern repeats more than twice.

**Alpine.js 3.x** — client-side interactivity via npm, not CDN. `x-data`, `x-show`, `x-on` for UI state; no full SPA framework.

**Leaflet.js** — maps via npm, loaded only on pages that need it. Not bundled globally.

All JS/CSS from npm. No CDN dependencies.

## Server

**Gunicorn**

Production command: `gunicorn --bind 0.0.0.0:<port> --workers 1 --threads 4 --timeout 120 --reload wsgi:app`

Flask dev server for local iteration only. `wsgi.py` is a protected file — never casually edit.

## Containers

**Docker Compose**

Every app ships a `docker/docker-compose.yml`. Structure: postgres → valkey → flask, with `service_healthy` dependency conditions on all upstream services. Two-stage Dockerfile, non-root user, EXPOSE port. See `docker-standard.md` for the exact template.

## Testing

**pytest**

Three layers: unit (models, services), integration (routes, database), smoke (health check, critical paths). `conftest.py` at project root defines all shared fixtures. Test database is separate from dev, created and torn down per run. No tests against SQLite.
