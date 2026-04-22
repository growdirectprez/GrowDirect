# Cove Architecture — INDEX SDD

**Status:** Active
**Type:** Platform Service (Cove)
**Last updated:** 2026-04-13
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]] | [[Brain/wiki/cove-platform|Cove Platform]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

---

## Purpose

Cove is the HOA governance platform for the West Portuguese Bend Community Association (WPBCA). This SDD describes the app factory, extensions, config, blueprint registration, and request lifecycle that form the platform foundation. It serves as the **index SDD** for all Cove services.

---

## Cove SDD Index

| SDD | Type | What it covers |
|-----|------|---------------|
| [[docs/sdds/cove/architecture|architecture]] | Platform Service | **This file.** App factory, extensions, config, blueprint registration |
| [[docs/sdds/cove/member-auth|member-auth]] | App Service | Magic link + password auth, session management, onboarding |
| [[docs/sdds/cove/governance-engine|governance-engine]] | App Service | Proposal lifecycle, voting, ballot tallying, bylaws config |
| [[docs/sdds/cove/secret-ballot-elections|secret-ballot-elections]] | App Service | Election orchestration, ballot secrecy, RLS |
| [[docs/sdds/cove/parcel-map-engine|parcel-map-engine]] | App Service | Parcel identity, GeoJSON layers, Leaflet rendering |
| [[docs/sdds/cove/vault|vault]] | App Service | Document storage, versioning, access tiers |
| [[docs/sdds/cove/treasury|treasury]] | App Service | Assessments, budgets, payment records |
| [[docs/sdds/cove/meetings|meetings]] | App Service | Meeting scheduling, ARC applications |
| [[docs/sdds/cove/board|board]] | App Service | Board-only operations, bulletins, roster |
| [[docs/sdds/cove/notifications|notifications]] | App Service | Notification delivery, email routing |
| [[docs/sdds/cove/knowledge|knowledge]] | MCP Server | pgvector legal document search |
| [[docs/sdds/cove/archive-system|archive-system]] | App Service | Document viewer, path traversal prevention |
| [[docs/sdds/cove/agent|agent]] | App Service | AI Q&A assistant, transparency log |
| [[docs/sdds/cove/sitemap-redesign|sitemap-redesign]] | App Service | Role-gated navigation |

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL 17 (`growdirect_postgres:5432/cove`) | Primary data store | Yes |
| Valkey 8 (`growdirect_valkey:6379/1`) | Sessions, rate limiter backend | Yes |
| Ollama (`growdirect_ollama:11434`) | Embeddings (qwen3-embedding:8b) | No (graceful degradation) |
| MailHog (dev) / Cloudflare Email Routing (prod) | Email delivery | No (notifications degrade) |
| Anthropic API | Agent Q&A | No (agent returns unconfigured message) |

---

## Data Flow & PII Map

### What enters
- Member registration: name, personal_email, lot_email, phone (from board invite)
- Document uploads: files to disk, metadata to DB
- Governance actions: proposals, ballots, votes
- Meeting data: scheduling, ARC applications with parcel references

### What's stored

| Table | PII Fields | Classification | Encryption |
|-------|-----------|---------------|------------|
| `members` | `name`, `personal_email`, `phone` | sensitive | **Plaintext (P0)** |
| `members` | `lot_email` | internal | Plaintext |
| `members` | `password_hash` | restricted | Werkzeug hash |
| `members` | `magic_link_nonce` | restricted | Signed token |
| `ballot_envelopes` | `member_id` + `ballot_id` link | restricted | RLS-gated (DB-side only) |
| `parcel_contacts` | `name`, `email`, `phone` | sensitive | **Plaintext (P0)** |
| `notifications` | `member_id`, email content | internal | Plaintext |
| `audit_log` | `actor_id`, IP (if logged) | internal | Plaintext |

### What exits
- Rendered HTML to authenticated browsers
- Email notifications via SMTP (lot_email forwarding to personal_email)
- iCalendar exports (meeting data)
- Agent API responses (JSON, no PII)
- MCP tool responses (knowledge chunks, no member PII)

---

## App Factory (`cove/__init__.py`)

`create_app()` executes these steps in order:

1. **Resolve config** -- reads `config_name` or `FLASK_ENV` (default `"prod"`)
2. **Create Flask instance** -- template/static folders set to project root
3. **Load config** -- `app.config.from_object(config_by_name[config_name])`
4. **Initialize Valkey session** -- Redis connection from `VALKEY_URL`, falls back to cookie sessions
5. **Initialize extensions** -- `db`, `login_manager`, `mail`, `csrf`, `sess`, `talisman`, `limiter`
6. **Initialize Talisman** -- CSP headers, X-Frame-Options DENY, HSTS
7. **Initialize rate limiter** -- Flask-Limiter backed by Valkey
8. **Create upload directory** -- `os.makedirs(UPLOAD_FOLDER, exist_ok=True)`
9. **Register ARC gate** -- `before_request` on map, archive, parcels blueprints for ARC role check
10. **Register 17 blueprints** -- imported inside function to avoid circular imports
11. **Register user loader** -- `login_manager.user_loader` calls `db.session.get(Member, user_id)`
12. **Register privacy consent hook** -- redirects onboarded members without consent
13. **Register context processor** -- injects `notification_count` into all templates
14. **Register CLI commands** -- Angel crawl, market, CRMLS commands
15. **Register SEO routes** -- Angel web routes at app root
16. **Register `/health` route** -- returns `{"status": "ok"}, 200`
17. **Register 429 handler** -- rate limit error page
18. **Register `/vault/*` redirect** -- 301 to `/documents/*` (GRO-395)

---

## Extensions (`cove/extensions.py`)

| Instance | Class | Purpose |
|----------|-------|---------|
| `db` | `SQLAlchemy()` | ORM, pool pre-ping, 300s recycle |
| `login_manager` | `LoginManager()` | `login_view = "auth.login"` |
| `mail` | `Mail()` | MailHog dev, Cloudflare prod |
| `csrf` | `CSRFProtect()` | Global CSRF; disabled in `TestConfig` |
| `sess` | `Session()` | Valkey DB 1; skipped when `SESSION_TYPE = "null"` |
| `talisman` | `Talisman()` | CSP, HSTS, X-Frame-Options |
| `limiter` | `Limiter()` | Rate limiting, Valkey storage |

---

## Blueprint Registration

17 blueprints registered in `create_app()`:

| # | Blueprint | URL Prefix | Module Path |
|---|-----------|------------|-------------|
| 1 | `public_bp` | `/` | `cove.public.routes` |
| 2 | `auth_bp` | `/auth` | `cove.auth.routes` |
| 3 | `member_bp` | `/member` | `cove.member.routes` |
| 4 | `governance_bp` | `/vote` | `cove.governance.routes` |
| 5 | `proceeding_bp` | `/proceedings` | `cove.governance.proceeding_routes` |
| 6 | `vault_bp` | `/documents` | `cove.vault.routes` |
| 7 | `board_bp` | `/board` | `cove.board.routes` |
| 8 | `treasury_bp` | `/treasury` | `cove.treasury.routes` |
| 9 | `parcels_bp` | `/parcels` | `cove.parcels.routes` |
| 10 | `meetings_bp` | `/meetings` | `cove.meetings.routes` |
| 11 | `election_bp` | `/vote/election` | `cove.governance.election_routes` |
| 12 | `agent_bp` | `/agent` | `cove.agent.routes` |
| 13 | `archive_bp` | `/archive` | `cove.archive.routes` |
| 14 | `map_bp` | `/map` | `cove.map.routes` |
| 15 | `research_bp` | `/research` | `cove.research.routes` |
| 16 | `community_bp` | `/community` | `cove.community` |
| 17 | `angel_web_bp` | `/angel/web` | `cove.angel.web_routes` |

Angel chat blueprint (`angel_chat_bp`) also registered at `/angel`.

---

## Config Classes (`cove/config.py`)

All inherit from `BaseConfig`. Selected via `config_by_name` dict.

### BaseConfig

| Setting | Value |
|---------|-------|
| `SECRET_KEY` | `os.environ["SECRET_KEY"]` (required) |
| `SQLALCHEMY_DATABASE_URI` | `os.environ["DATABASE_URL"]` (required) |
| `SESSION_TYPE` | `"redis"` (Valkey-compatible) |
| `VALKEY_URL` | env or `redis://localhost:6379/1` |
| `MAX_CONTENT_LENGTH` | 50 MB |
| `MAGIC_LINK_EXPIRY` | 900 seconds (15 min) |
| `SESSION_DURATION_DAYS` | 7 |
| `DOMAIN` | `abalonecove.org` |
| `UPLOAD_FOLDER` | `../uploads` relative to `cove/` |

### ProdConfig

`SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE = "Lax"`, `REMEMBER_COOKIE_SECURE`, `REMEMBER_COOKIE_HTTPONLY`.

### TestConfig

`TESTING = True`, `WTF_CSRF_ENABLED = False`, `SESSION_TYPE = "null"`, separate test DB.

---

## Models

28 model classes across 16 files, all imported in `cove/models/__init__.py` for Alembic detection.

Conventions: UUID primary keys as `String(36)`, `Mapped[]` annotations, `back_populates`, `created_at`/`updated_at` timestamps.

---

## Multi-Tenant Isolation

All queries are scoped by `organization_id` (FK to `organizations.id`). Routes verify `entity.organization_id == current_user.organization_id` before returning data. No cross-org data access is possible through the app layer.

---

## Startup Order and Dependency Graph

```
1. growdirect_postgres  (shared infra)
2. growdirect_valkey    (shared infra)
3. growdirect_ollama    (shared infra, optional)
4. cove_flask           (depends on 1, 2)
5. cove_localhost_mailhog (dev only, independent)
```

### Blast Radius

| If this fails | Impact |
|--------------|--------|
| PostgreSQL | Complete outage — all routes return 500 |
| Valkey | Session creation fails, rate limiting disabled, fallback to cookie sessions |
| Ollama | Embedding generation returns None, semantic search unavailable |
| Mail | Notification emails silently fail, in-app notifications still work |
| Anthropic API | Agent Q&A returns "not configured", all other routes unaffected |

---

## Operations

### Startup Sequence

```bash
cd ~/GrowDirect/devops && docker compose up -d      # shared infra
cd ~/GrowDirect/Cove/devops && docker compose up -d  # cove_flask + mailhog
```

### Health Check

`GET /health` returns `{"status": "ok"}, 200`. Docker healthcheck: every 10s, 20s start period, 5 retries.

### Failure Modes

- **DB connection lost**: Pool pre-ping detects, reconnects on next request. Extended outage = 500s.
- **Valkey down**: Falls back to cookie sessions if `redis` import fails at startup. If Valkey dies at runtime, session operations fail.
- **Gunicorn worker crash**: Auto-restarts (1 worker, 4 threads, 120s timeout).

### Configuration (env vars)

| Variable | Required | Default |
|----------|----------|---------|
| `SECRET_KEY` | Yes | (none) |
| `DATABASE_URL` | Yes | (none) |
| `FLASK_ENV` | No | `prod` |
| `VALKEY_URL` | No | `redis://localhost:6379/1` |
| `OLLAMA_URL` | No | `http://localhost:11434` |
| `ANTHROPIC_API_KEY` | No | (none) |
| `MAIL_SERVER` | No | `localhost` |
| `MAIL_PORT` | No | `1025` |

---

## Deployment

### Docker Service Definition

```yaml
# Cove/devops/docker-compose.yml
name: cove
services:
  flask:
    build: ..
    image: cove-flask
    container_name: cove_flask
    ports: ["5002:5000"]
    command: gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 4 --timeout 120 --reload wsgi:app
    networks: [growdirect]
    volumes:
      - ../cove:/app/cove
      - ../templates:/app/templates
      - ../static:/app/static
      - ../wsgi.py:/app/wsgi.py
      - ../migrations:/app/migrations
```

### AWS Target

- **Compute**: ECS/Fargate (single task, 0.5 vCPU, 1GB memory)
- **Database**: RDS PostgreSQL 17 with pgvector extension
- **Cache**: ElastiCache Valkey
- **Secrets**: AWS Secrets Manager for `SECRET_KEY`, `DATABASE_URL`, `ANTHROPIC_API_KEY`
- **Storage**: EFS for upload volume
- **Domain**: abalonecove.org via Cloudflare (DNS + email routing)

### CI/CD Requirements

- Run `pytest` against `cove_test` database
- Build Docker image, push to ECR
- Deploy via ECS service update
- Run Alembic migrations before traffic cutover

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P0** | Member PII (name, personal_email, phone) stored plaintext in `members` table | Field-level AES-256-GCM encryption using Canary's `crypto.py` pattern |
| 2 | **P0** | Parcel contact PII (name, email, phone) stored plaintext in `parcel_contacts` | Same field-level encryption |
| 3 | **P0** | `SECRET_KEY` and `DATABASE_URL` in `.env` files, not secrets manager | AWS Secrets Manager + `boto3` retrieval at startup |
| 4 | **P1** | RLS for `ballot_envelopes` is DB-side only -- app code does not enforce separation | Application-level enforcement + integration tests |
| 5 | **P1** | No data retention policy -- old sessions, audit logs, notifications accumulate indefinitely | Automated purge: sessions >30d, audit logs >24mo |
| 6 | **P1** | No rate limiting on agent `/api/ask` endpoint (Anthropic API cost exposure) | Add Flask-Limiter decorator (e.g., 10/min per user) |
| 7 | **P1** | Notification email addresses (lot_email) visible in SMTP logs | Ensure SMTP transport uses TLS in production |
| 8 | **P2** | `String(36)` UUID primary keys across all models -- not native UUID type | Migrate to `Mapped[uuid.UUID]` on new tables, backfill on major version |
| 9 | **P2** | Session keys unencrypted in Valkey | Enable Valkey AUTH + TLS in production |
| 10 | **P2** | No key rotation procedure documented | Document rotation for SECRET_KEY, DB credentials, API keys |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (members.personal_email, members.phone, parcel_contacts.*)
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check endpoint responds (`/health` -- done)
- [ ] Audit logging for sensitive operations (partial -- governance and vault audited, board contacts not audited)
- [ ] Data retention policy implemented
- [ ] Rate limiting on public endpoints (limiter initialized, needs per-route decoration)
- [ ] Error responses don't leak internals (Talisman CSP active, need custom 500 page)
- [ ] Ballot envelope RLS enforced at application layer
- [ ] SMTP TLS enforced in production
- [ ] Valkey AUTH + TLS in production
