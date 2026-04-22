---
name: factory-newapp
roles-primary: [Tom]
roles-assist: [Jeremy]
description: |
  Scaffold a new GrowDirect platform app from proven patterns. Use when starting
  a new project, prototyping a new service, or spinning up a new app. Triggers on
  "new app", "new project", "scaffold", "prototype", "spin up", "start a new",
  "platform template".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - TodoWrite
---

# Factory New App — GrowDirect Platform Scaffolding

Spin up a new app from battle-tested platform patterns. No empty scaffolding — only create what you'll use in the first sprint.

**Announce:** "I'm using factory-newapp to scaffold [app name]."

---

## Philosophy

> Don't scaffold aspirationally. Build what you need, when you need it.
> Every file must earn its place in the first commit.

Platform lessons:
- Empty modules become cleanup debt
- Data belongs with the module that serves it (not a generic `data/` dir)
- Privacy, security, and compliance are cheaper to build in than bolt on
- CLAUDE.md drifts from reality fast — update it with every refactor
- Skills ARE the dev process — ship them with the code

---

## Step 1: Define the Domain

Before touching code, answer these questions with Jeffe:

```markdown
## App Definition
- **Name:** [app name]
- **One-liner:** [what it does in 10 words]
- **First deployment:** [org/community name]
- **Domain:** [domain.tld]
- **Primary entity:** [the thing everything resolves to — like APN in Cove, merchant in Canary]
- **Users:** [who logs in? how many?]
- **Compliance:** [what laws/regulations apply?]
- **Stack:** Python 3.12 / Flask 3.1 / SQLAlchemy 2.0 / PostgreSQL 17 / Tailwind CSS / Alpine.js
```

The primary entity answer is critical. Everything chains from it:
```
PrimaryEntity → User → Action
PrimaryEntity → Data → Report
PrimaryEntity → Event → Audit
```

Your app needs this anchor. Without it, the data model will drift.

---

## Step 2: Create the Repo

```bash
mkdir -p ~/GrowDirect/{AppName}
cd ~/GrowDirect/{AppName}
git init

# Core structure — ONLY what you need day one
mkdir -p {app}/models {app}/auth {app}/member {app}/public {app}/templates
mkdir -p devops docs/security migrations/versions tests/{unit,integration,smoke}
```

---

## Step 3: Copy the Platform Skeleton

These files are proven and reusable. Copy and adapt:

### App Factory (`{app}/__init__.py`)
```python
import os
from flask import Flask
from {app}.config import config_by_name
from {app}.extensions import db, login_manager, mail, csrf

def create_app(config_name: str | None = None) -> Flask:
    config_name = config_name or os.getenv("FLASK_ENV", "prod")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

    # Register blueprints — ONLY the ones you've built
    from {app}.public.routes import public_bp
    from {app}.auth.routes import auth_bp
    from {app}.member.routes import member_bp

    app.register_blueprint(public_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(member_bp, url_prefix="/member")

    # User loader
    from {app}.models.member import Member

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Member, user_id)

    return app
```

### Extensions (`{app}/extensions.py`)
```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
mail = Mail()
csrf = CSRFProtect()
```

### Config (`{app}/config.py`)
```python
import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "redis"
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    WTF_CSRF_ENABLED = True

class DevConfig(BaseConfig):
    DEBUG = True

class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProdConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

config_by_name = {
    "dev": DevConfig, "development": DevConfig,
    "test": TestConfig, "testing": TestConfig,
    "prod": ProdConfig, "production": ProdConfig,
}
```

### Base Model Pattern
```python
import uuid
from datetime import datetime, timezone
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from {app}.extensions import db

class ExampleModel(db.Model):
    __tablename__ = "example_models"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
```

**Rules:**
- UUID primary keys as native `Mapped[uuid.UUID]`
- `Mapped[]` type hints — no legacy `Column()`
- Every entity has `org_id` for multi-tenant scoping
- `created_at` and `updated_at` on every table
- All models imported in `{app}/models/__init__.py`

### Docker Compose (`devops/docker-compose.yml`)

Apps connect to shared GrowDirect infrastructure — they do NOT run their own
Postgres or Valkey.

```yaml
name: {app}

services:
  flask:
    image: {app}-flask
    build:
      context: ..
      dockerfile: Dockerfile
    container_name: {app}_flask
    ports:
      - "{port}:5000"
    volumes:
      - ../{app}:/app/{app}
      - ../templates:/app/templates
      - ../static:/app/static
      - ../wsgi.py:/app/wsgi.py
      - ../migrations:/app/migrations
    environment:
      FLASK_ENV: development
      DATABASE_URL: postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/{app}
      VALKEY_URL: redis://growdirect_valkey:6379/{valkey_db}
      SECRET_KEY: dev-secret
    networks:
      - growdirect

networks:
  growdirect:
    external: true
```

**Required:** `name:` at top level (prevents project name collisions). `image:` on
every service with `build:` (prevents image tag collisions). See platform CLAUDE.md.

Register the port and Valkey DB in `~/GrowDirect/CLAUDE.md` port allocation table.

---

## Step 4: Security & Compliance (Day One)

Don't skip this. Create and adapt:

### docs/security/data-retention-policy.md
Define what data you store, how long, and when it's destroyed.

### docs/security/encryption-strategy.md
Data classification (public/internal/confidential/restricted) + encryption roadmap.

### docs/security/breach-notification-procedure.md
Discovery → containment → assessment → notification → remediation.

### Privacy Policy + Terms
Every app gets `/privacy` and `/terms` from day one.

---

## Step 5: CLAUDE.md

Write the agent instructions BEFORE building features. This is the contract
between you and the agent that works on this app.

Template sections:
1. **Identity** — app name, founder, stack, entry point
2. **Hard Rules** — primary key entity, DB choice, compliance requirements, protected files
3. **Architecture** — app factory, extensions, blueprint table, module structure
4. **Data Model** — table map, key model details, relationships
5. **Frontend Patterns** — template inheritance, CSS approach, JS framework
6. **Authentication** — login flow, session management
7. **Infrastructure** — config classes, Docker stack, migrations, seed data
8. **Workflow** — reference the factory process skills
9. **Coding Standards** — Python version, ORM patterns, route/template conventions
10. **Domain Context** — who uses this, why it matters, what's at stake

**Keep it current.** Every refactor updates CLAUDE.md.

---

## Step 6: Skills

Create app-specific factory process overrides at `~/GrowDirect/.claude/skills/`:

```
{app}-preflight.md   — App-specific preflight additions (delegates to factory-preflight)
{app}-blueprint.md   — App-specific plan additions (delegates to factory-blueprint)
{app}-tdd.md         — App-specific test additions (delegates to factory-tdd)
{app}-assembly.md    — App-specific assembly additions (delegates to factory-assembly)
{app}-verify.md      — App-specific verify additions (delegates to factory-verify)
{app}-qa.md          — App-specific QA additions (delegates to factory-qa)
{app}-ship.md        — App-specific ship additions (delegates to factory-ship)
{app}-close.md       — App-specific close additions (delegates to factory-close)
```

Each delegates to the corresponding `factory-*.md` skill and adds domain-specific
guardrails (compliance checks, data integrity flags, etc.).

---

## Step 7: First Feature

NOW you build the first domain-specific feature. Not before.

The pattern:
1. Create the model (in `{app}/models/`)
2. Create the blueprint (`{app}/{module}/routes.py`)
3. Register the blueprint in `__init__.py`
4. Create the service layer (`{app}/{module}/services.py`)
5. Create templates (`{app}/{module}/templates/{module}/`)
6. Write tests (TDD — test first, then implement)
7. Create migration (`alembic revision --autogenerate`)
8. Smoke test in Docker

**One blueprint per domain.** Don't create empty modules for "later."

---

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Create empty modules for planned features | Build when needed, not before |
| Put data files at repo root | Data belongs with the module that serves it |
| Use a generic `data/` or `static/` dir | `{module}/data/` or `{module}/static/` |
| Skip privacy/security on "v1" | Ship privacy policy, consent flow, and security docs from day one |
| Let CLAUDE.md drift from reality | Update it with every refactor — it's the agent's eyes |
| Scaffold aspirationally | Every file in the first commit must be used in the first sprint |
| Run your own Postgres/Valkey | Connect to shared GrowDirect infra |
| Use `String(36)` for UUIDs | Use native `Mapped[uuid.UUID]` |
| Skip `image:` on Docker services | Always tag: `image: {app}-{service}` |
| Skip `name:` on Docker compose | Always declare: `name: {app}` |

---

## Checklist: Ready to Ship v0.1

- [ ] App factory with 3+ blueprints (public, auth, member + domain)
- [ ] Connected to shared GrowDirect PostgreSQL + Valkey
- [ ] Port registered in platform CLAUDE.md
- [ ] Valkey DB number registered in platform CLAUDE.md
- [ ] Docker compose has `name:` and `image:` tags
- [ ] At least one domain model with migration
- [ ] Login works (magic link or password)
- [ ] Privacy policy at `/privacy`
- [ ] Terms at `/terms`
- [ ] CSRF on all forms
- [ ] ProdConfig enforces SECRET_KEY
- [ ] Session cookie flags set
- [ ] `docs/security/` has retention + encryption + breach docs
- [ ] CLAUDE.md is written and accurate
- [ ] App-specific factory skills created at `~/GrowDirect/.claude/skills/`
- [ ] Tests exist and pass
- [ ] No empty modules, no orphaned files
