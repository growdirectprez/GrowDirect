# SDD: Architecture

**Status:** Active
**Last updated:** 2026-03-29

---

## 1. App Factory (`cove/__init__.py`)

`wsgi.py` calls `create_app()` which executes these steps in order:

1. **Resolve config** -- reads `config_name` argument or falls back to `FLASK_ENV` env var (default `"prod"`). Looks up the config class from `config_by_name` dict.
2. **Create Flask instance** -- `template_folder` and `static_folder` are set to the project root's `templates/` and `static/` directories (resolved via `pathlib`), not the package-relative defaults.
3. **Load config** -- `app.config.from_object(config_by_name[config_name])`.
4. **Initialize Valkey session** -- if `SESSION_TYPE` is `"redis"`, creates a Redis connection from `VALKEY_URL` and assigns it to `SESSION_REDIS`. Falls back to `"null"` (cookie sessions) if the `redis` package is missing.
5. **Initialize extensions** -- `db`, `login_manager`, `mail`, `csrf` are always initialized. `sess` (Flask-Session) is initialized only when session type is not `"null"`.
6. **Create upload directory** -- `os.makedirs(UPLOAD_FOLDER, exist_ok=True)`.
7. **Register 13 blueprints** -- imported inside the function to avoid circular imports.
8. **Register user loader** -- `login_manager.user_loader` calls `db.session.get(Member, user_id)`.
9. **Register `before_request` hook** -- privacy consent check (see section 7).
10. **Register context processor** -- injects `notification_count` into all templates (see section 7).
11. **Register `/health` route** -- returns `{"status": "ok"}, 200`.
12. **Return app**.

---

## 2. Extensions (`cove/extensions.py`)

Seven extension instances are created at module level and initialized in the app factory via `init_app()`:

| Instance | Class | Configuration |
|----------|-------|---------------|
| `db` | `SQLAlchemy()` | Database URI from `SQLALCHEMY_DATABASE_URI`. Pool pre-ping enabled, 300s recycle. |
| `login_manager` | `LoginManager()` | `login_view = "auth.login"`, `login_message = "Please log in to access this page."` |
| `mail` | `Mail()` | MailHog in dev (SMTP port 1025), Cloudflare Email Routing in prod. Configured via `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_DEFAULT_SENDER`. |
| `csrf` | `CSRFProtect()` | Enabled globally. Disabled only in `TestConfig` (`WTF_CSRF_ENABLED = False`). |
| `sess` | `Session()` | Flask-Session backed by Valkey (DB 1). Skipped when `SESSION_TYPE = "null"` (test config). |
| `talisman` | `Talisman()` | Flask-Talisman for CSP, X-Frame-Options, HSTS security headers. |
| `limiter` | `Limiter()` | Flask-Limiter for rate limiting, backed by Valkey storage. |

Import pattern: `from cove.extensions import db, login_manager, mail, csrf, sess`.

---

## 3. Config Classes (`cove/config.py`)

All classes inherit from `BaseConfig`. Selected by `FLASK_ENV` env var via the `config_by_name` dict, which accepts aliases (`"dev"/"development"`, `"test"/"testing"`, `"staging"`, `"prod"/"production"`).

### BaseConfig

| Setting | Value |
|---------|-------|
| `SECRET_KEY` | `os.environ["SECRET_KEY"]` (required) |
| `SQLALCHEMY_DATABASE_URI` | `os.environ["DATABASE_URL"]` (required) |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | `False` |
| `SQLALCHEMY_ENGINE_OPTIONS` | `pool_pre_ping=True`, `pool_recycle=300` |
| `SESSION_TYPE` | `"redis"` (Valkey-compatible) |
| `VALKEY_URL` | `os.environ.get("VALKEY_URL", "redis://localhost:6379/1")` |
| `WTF_CSRF_ENABLED` | `True` |
| `MAX_CONTENT_LENGTH` | 50 MB |
| `MAIL_SERVER` | `localhost` (overridden in env) |
| `MAIL_PORT` | `1025` (MailHog default) |
| `MAIL_DEFAULT_SENDER` | `cove@abalonecove.org` |
| `MAGIC_LINK_EXPIRY` | 900 seconds (15 min) |
| `SESSION_DURATION_DAYS` | 7 |
| `DOMAIN` | `abalonecove.org` |
| `UPLOAD_FOLDER` | `../uploads` relative to `cove/` package |
| `ALLOWED_UPLOAD_EXTENSIONS` | `pdf, doc, docx, xls, xlsx, png, jpg, jpeg, gif` |
| `MAX_AVATAR_SIZE` | 2 MB |
| `MAX_MEETING_ATTACHMENT_SIZE` | 10 MB |
| `MAX_DOCUMENT_SIZE` | 25 MB |

### DevConfig

- `DEBUG = True`
- `SESSION_COOKIE_SECURE = False`

### TestConfig

- `TESTING = True`
- `SQLALCHEMY_DATABASE_URI` overridden to `TEST_DATABASE_URL` env var or `postgresql://growdirect:growdirect_dev@localhost:5432/cove_test`
- `WTF_CSRF_ENABLED = False`
- `SESSION_TYPE = "null"` (no Valkey needed in tests)
- `SQLALCHEMY_ENGINE_OPTIONS = {}` (pool options disabled)

### StagingConfig

- `SESSION_COOKIE_SECURE = True`

### ProdConfig

- `SESSION_COOKIE_SECURE = True`
- `SESSION_COOKIE_HTTPONLY = True`
- `SESSION_COOKIE_SAMESITE = "Lax"`
- `REMEMBER_COOKIE_SECURE = True`
- `REMEMBER_COOKIE_HTTPONLY = True`

---

## 4. Blueprint Registration

14 blueprints registered in `create_app()`, in this order:

| # | Blueprint | URL Prefix | Module Path |
|---|-----------|------------|-------------|
| 1 | `public_bp` | `/` | `cove.public.routes` |
| 2 | `auth_bp` | `/auth` | `cove.auth.routes` |
| 3 | `member_bp` | `/member` | `cove.member.routes` |
| 4 | `governance_bp` | `/vote` | `cove.governance.routes` |
| 5 | `proceeding_bp` | `/proceedings` | `cove.governance.proceeding_routes` |
| 6 | `vault_bp` | `/vault` | `cove.vault.routes` |
| 7 | `board_bp` | `/board` | `cove.board.routes` |
| 8 | `treasury_bp` | `/treasury` | `cove.treasury.routes` |
| 9 | `parcels_bp` | `/parcels` | `cove.parcels.routes` |
| 10 | `meetings_bp` | `/meetings` | `cove.meetings.routes` |
| 11 | `election_bp` | `/vote/election` | `cove.governance.election_routes` |
| 12 | `agent_bp` | `/agent` | `cove.agent.routes` |
| 13 | `archive_bp` | `/archive` | `cove.archive.routes` |
| 14 | `map_bp` | `/map` | `cove.map.routes` |

All blueprint imports are inside `create_app()` to avoid circular imports with extensions.

---

## 5. Models

16 model files imported in `cove/models/__init__.py` for Alembic autogenerate detection. 28 model classes total.

| File | Models |
|------|--------|
| `organization.py` | `Organization` |
| `parcel.py` | `Parcel` |
| `member.py` | `Member`, `Role`, `MemberRole`, `DirectoryPreference` |
| `governance.py` | `Proposal`, `Ballot`, `BallotEnvelope` |
| `election.py` | `Election`, `Candidate`, `ElectionChoice` |
| `treasury.py` | `Assessment`, `LedgerEntry`, `Budget`, `ParcelPayment` |
| `vault.py` | `Document`, `DocumentVersion` |
| `meetings.py` | `Meeting`, `ARCApplication`, `ARCReview` |
| `audit.py` | `AuditLog` |
| `proceeding.py` | `Proceeding`, `ProceedingEntry` |
| `research_parcel.py` | `ResearchParcel` |
| `parcel_profile.py` | `ParcelProfile` |
| `parcel_tag.py` | `ParcelTag`, `ParcelTagAssignment` |
| `notification.py` | `Notification` |
| `knowledge.py` | `KnowledgeChunk` |

Import pattern in `cove/models/__init__.py`: every model is explicitly imported with `# noqa: F401` so Alembic's `autogenerate` detects all tables.

Model conventions: UUID primary keys (stored as `String(36)`), `Mapped[]` type annotations, `back_populates` (not `backref`), `created_at` and `updated_at` timestamps.

---

## 6. Request Lifecycle

```
Client -> Gunicorn (5000 inside container, 5002 on host)
       -> Flask WSGI app
       -> before_request hooks
       -> @login_required check (Flask-Login)
       -> Blueprint route handler
       -> Service layer (business logic)
       -> SQLAlchemy ORM -> PostgreSQL (growdirect_postgres:5432/cove)
       -> Jinja2 template render (extends templates/base.html)
       -> HTML response
```

### before_request Hooks

**Privacy consent check** (`_check_privacy_consent`):
- Skips unauthenticated users.
- Skips exempt endpoints: `auth.*`, `public.*`, `static`, `agent.*`, and `member.accept_privacy`.
- For authenticated, onboarded members whose `privacy_consent_at` is `None`, redirects to `/member/accept-privacy`.

### Context Processors

**`inject_notification_count`**:
- For authenticated users, calls `cove.notifications.services.unread_count(current_user.id)` and injects `notification_count` into all template contexts.
- Returns `0` for unauthenticated users or on any exception.

### User Loader

Registered on `login_manager`: calls `db.session.get(Member, user_id)` to load the current user from session.

---

## 7. Infrastructure

Cove runs on the shared GrowDirect Docker Compose stack. It does NOT run its own PostgreSQL or Valkey. Start shared infrastructure first, then start Cove.

```bash
# 1. Start shared services
cd ~/GrowDirect/devops && docker compose up -d

# 2. Start Cove
cd ~/GrowDirect/Cove/devops && docker compose up -d
```

### Shared Services (from `~/GrowDirect/devops/docker-compose.yml`)

| Service | Container | Port |
|---------|-----------|------|
| PostgreSQL 17 | `growdirect_postgres` | 5432 |
| Valkey 8 | `growdirect_valkey` | 6379 |
| pgAdmin | `growdirect_pgadmin` | 5050 |
| Ollama | `growdirect_ollama` | 11434 |

### Cove Services (from `~/GrowDirect/Cove/devops/docker-compose.yml`)

| Service | Container | Ports (host:container) |
|---------|-----------|------------------------|
| Flask (Gunicorn) | `cove_flask` | 5002:5000 |
| MailHog | `cove_localhost_mailhog` | 1026:1025 (SMTP), 8026:8025 (Web UI) |

Both containers join the `growdirect` external Docker network.

### Connection Strings

```
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
VALKEY_URL=redis://growdirect_valkey:6379/1
OLLAMA_URL=http://growdirect_ollama:11434
```

### Gunicorn Configuration

`gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 4 --timeout 120 --reload wsgi:app`

### Volume Mounts (dev)

`cove/`, `templates/`, `static/`, `wsgi.py`, `migrations/` are mounted into the container. Gunicorn `--reload` picks up file changes without container restart.

### Health Check

Container health check hits `http://localhost:5000/health` every 10 seconds with a 20-second start period and 5 retries.

---

## 8. Frontend Build

PostCSS build pipeline via npm. No CDN dependencies.

### Pipeline (`postcss.config.js`)

Three plugins in order:
1. `postcss-import` -- resolves `@import` directives
2. `tailwindcss` -- processes Tailwind utility classes
3. `autoprefixer` -- adds vendor prefixes

### Tailwind Configuration (`tailwind.config.js`)

Content scanning paths:
- `./cove/**/templates/**/*.html`
- `./templates/**/*.html`

Custom color palette: `cove-50` through `cove-900` (blue tones, from `#f0f7ff` to `#0a3f6f`).

### CSS Build

- Source: `static/css/main.css`
- Output: `static/css/dist/main.css`
- Dev watch: `npm run dev` (PostCSS watch mode)
- Production build: `npm run build` (`NODE_ENV=production`)

### JavaScript

- Alpine.js 3.14+ via npm -- interactive UI components (modals, toggles, dropdowns)
- Leaflet.js 1.9+ via npm -- parcel map on `/parcels` routes only (not loaded globally)

### npm Packages (`package.json`)

**devDependencies:** `tailwindcss ^3.4`, `postcss ^8.4`, `postcss-cli ^11.0`, `postcss-import ^16.0`, `autoprefixer ^10.4`

**dependencies:** `alpinejs ^3.14`, `leaflet ^1.9`

---

## 9. Dependencies (`requirements.txt`)

### Core

| Package | Version | Purpose |
|---------|---------|---------|
| `flask` | 3.1.x | Web framework |
| `sqlalchemy` | 2.0.x | ORM |
| `flask-sqlalchemy` | 3.1.x | Flask-SQLAlchemy integration |
| `flask-login` | 0.6.x | Session-based authentication |
| `flask-mail` | 0.10.x | Email sending (magic links, notifications) |
| `flask-wtf` | 1.2.x | WTForms integration, CSRF protection |
| `flask-session` | >=0.5 | Server-side sessions (Valkey backend) |
| `psycopg2-binary` | 2.9.x | PostgreSQL driver |
| `alembic` | 1.14.x | Database migrations |
| `gunicorn` | 23.x | WSGI server |

### Utilities

| Package | Version | Purpose |
|---------|---------|---------|
| `python-dotenv` | 1.0.x | `.env` file loading |
| `itsdangerous` | 2.2.x | Magic link token signing |
| `werkzeug` | 3.1.x | Password hashing, HTTP utilities |
| `redis` | >=5.0 | Valkey client (Redis-compatible) |
| `mistune` | 3.1.x | Markdown rendering (archive module) |
| `pgvector` | >=0.3 | Vector similarity search |
| `httpx` | >=0.27 | HTTP client (agent module, Ollama calls) |
| `anthropic` | >=0.40 | Claude API (agent module) |

### Testing

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | 8.x | Test runner |
| `pytest-flask` | 1.3.x | Flask test fixtures |
