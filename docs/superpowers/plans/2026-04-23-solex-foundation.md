# Solex Foundation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up `Solex/` as a working Flask commerce app peer to Canary/Cove: a browseable Solex-mirrored storefront where a guest can add products to cart, check out through the Square Web Payments SDK against the Square sandbox, receive a confirmation email, and have the resulting order state reconciled via Square webhooks.

**Architecture:** Flask 3 + Jinja + Tailwind + Alpine, SQLAlchemy 2.0 `Mapped[]` against Postgres 17, sessions + cart in Valkey DB 2, Gunicorn with `--reload` in dev. Full-fidelity commerce architecture per the design spec, with tax/shipping/fulfillment as stub strategies behind real interfaces. Square integration uses the `squareup` Python SDK pointed at sandbox via `SQUARE_ENVIRONMENT=sandbox`.

**Tech Stack:** Python 3.12, Flask 3, SQLAlchemy 2.0, Postgres 17, Valkey 8, Tailwind 3.x, Alpine 3.x, pytest, Alembic, Flask-Login, Flask-WTF, Flask-Limiter, squareup (Square Python SDK), tenacity, pydantic, RQ (foundation includes worker container but no jobs scheduled yet), MailHog (dev SMTP).

---

## Scope

**This is Plan 1 of 4.** It lands the foundation only.

**In scope:**
- Repo scaffold + Docker compose + shared-infra wiring
- Config, app factory, extensions, blueprints
- Data model for catalog, cart, orders, customers, admin, webhooks
- Catalog YAML loader + ~5 seed products for smoke tests (full 25-SKU curation is a later pass)
- Storefront browse: `/`, `/shop`, `/shop/<category>`, `/products/<slug>`
- Cart: add/remove/update, cart drawer + cart page, Valkey-backed for guests
- Guest checkout: address form, Square Web Payments SDK card element, order placement via Square sandbox
- Order confirmation page + email (MailHog)
- Square webhook endpoint with signature verification + orphan-payment recovery
- Basic admin login (magic-link + password) — blueprint exists, routes stubbed except login/logout
- Smoke tests + developer runbook

**Out of scope (later plans):**
- Admin UI surfaces beyond login (Plan 2)
- Customer accounts / self-service (Plan 2)
- Autoship subscriptions (Plan 2)
- Customer-facing refund flow (Plan 2; admin-initiated refund + webhook orphan recovery ARE in scope)
- Returns flow (Plan 2)
- Cart abandonment emails (Plan 2)
- Search (Plan 2)
- Scenario runner + 9 scenarios (Plan 3)
- Tailwind theme matching solexglobal.com (Plan 4)
- Full 25-SKU catalog curation + imagery (Plan 4)

**Definition of done for Plan 1:**
1. `cd ~/GrowDirect/Solex/devops && docker compose up -d` brings up `solex_web` and `solex_worker` on the `growdirect` network.
2. `curl http://localhost:5003/health` returns `{"ok": true}`.
3. `docker compose exec web python3 -m solex.cli catalog import` loads the 5 seed products.
4. Browsing `http://localhost:5003/shop` lists products, `/products/<slug>` renders a product detail page, cart drawer add-to-cart works.
5. A full guest checkout against Square sandbox produces: a persisted `Order`, a Square sandbox payment, decremented inventory, a confirmation email in MailHog, and a reconciled `SquareWebhookEvent` for the payment.
6. `pytest tests/unit tests/integration tests/smoke` is green.
7. Canary can OAuth the same Square sandbox merchant and begin observing the `Order`s this app produces. (Canary work is out of scope here — we just don't break that path.)

---

## Prerequisites

Before starting:

- [ ] Linear parent issue exists and is referenced in commits (e.g., `GRO-XXX`). If not, create one titled "Solex commerce app — Foundation (Plan 1)" with a link to `docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md` in the description. Not optional — the platform rule is "no issue, no work."
- [ ] Shared infra is running: `cd ~/GrowDirect/devops && docker compose up -d` → verify `docker ps | grep growdirect_postgres` shows the container.
- [ ] A Square sandbox application exists in the developer dashboard (the one Canary already uses is fine — per memory, the sandbox is shared across apps, data is not to be deleted).
- [ ] You have these secrets available locally:
  - `SQUARE_SANDBOX_APPLICATION_ID`
  - `SQUARE_SANDBOX_ACCESS_TOKEN`
  - `SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY`
  - `SQUARE_SANDBOX_LOCATION_ID`
- [ ] Port 5003, MailHog ports 1027 / 8027, and Valkey DB 2 are unclaimed (Canary=5001/DB 0, Cove=5002/DB 1).
- [ ] Engineer is in a fresh git worktree for this plan, branched off `main`. If not, create one: `git worktree add ../solex-foundation -b plan/solex-foundation`.

Useful skills to reference during execution:
- @superpowers:test-driven-development — this plan is TDD throughout
- @superpowers:systematic-debugging — when a task fails, use this before proposing a fix
- @superpowers:verification-before-completion — before marking any task complete, run the verification command and confirm output

---

## File Structure

Every file this plan creates, grouped by subsystem. **Rule:** one clear responsibility per file. If a file grows past ~300 lines in this plan, stop and split it.

### Repo scaffold

```
Solex/
├── CLAUDE.md                         app-specific agent context
├── README.md                         dev-setup quickstart
├── wsgi.py                           Gunicorn entry point; single entry
├── pyproject.toml                    project metadata
├── requirements.txt                  runtime deps
├── requirements-dev.txt              test + lint deps
├── package.json                      Tailwind + Alpine build
├── postcss.config.js                 PostCSS pipeline
├── tailwind.config.js                Tailwind theme config
├── .env.example                      documented env-var template
├── .gitignore                        Python + Node ignores
├── pytest.ini                        pytest config
├── alembic.ini                       Alembic config
├── devops/
│   ├── Dockerfile                    multi-stage: build tailwind, then Python runtime
│   ├── docker-compose.yml            web + worker services
│   └── scripts/
│       └── dev.sh                    up/down/logs/shell helper
├── alembic/
│   ├── env.py                        Alembic env
│   ├── script.py.mako                migration template
│   └── versions/
│       └── 0001_initial.py           initial schema (all tables in scope)
├── catalog/
│   ├── products.yaml                 5 seed products for smoke; full catalog later
│   └── images/                       placeholder imagery
├── solex/
│   ├── __init__.py                   app factory (create_app)
│   ├── config.py                     BaseConfig / DevConfig / TestConfig / ProdConfig
│   ├── extensions.py                 db, login_manager (admin + customer), csrf, limiter, mail
│   ├── cli.py                        click entry: catalog import, etc.
│   ├── logging.py                    structured logging setup
│   ├── feature_flags.py              env-var-backed flags
│   ├── models/
│   │   ├── __init__.py               re-exports
│   │   ├── base.py                   BaseModel w/ UUID PK + timestamps
│   │   ├── catalog.py                Category, Product, ProductTag
│   │   ├── inventory.py              Inventory, InventoryAdjustment
│   │   ├── cart.py                   Cart, CartLine
│   │   ├── order.py                  Order, OrderItem, OrderNote
│   │   ├── refund.py                 Refund (customer-facing flow deferred; model here)
│   │   ├── customer.py               Customer, Address
│   │   ├── admin.py                  AdminUser
│   │   ├── auth.py                   MagicLinkToken
│   │   ├── ops.py                    SquareWebhookEvent, EmailLog
│   ├── services/
│   │   ├── __init__.py
│   │   ├── square_client.py          wraps squareup SDK
│   │   ├── cart.py                   cart load/add/remove/update/totals
│   │   ├── checkout.py               place_order orchestration
│   │   ├── inventory.py              decrement/increment/adjust + adjustment log
│   │   ├── refunds.py                issue_refund / issue_refund_by_payment_id (orphan recovery)
│   │   ├── tax.py                    TaxService protocol + FlatRateTaxStub
│   │   ├── shipping.py               ShippingService protocol + FlatRateShippingStub
│   │   ├── addresses.py              AddressValidator protocol + NoopValidator
│   │   ├── fulfillment.py            FulfillmentService protocol + ManualFulfillmentStub
│   │   ├── catalog.py                list_products, get_product
│   │   ├── catalog_import.py         YAML loader
│   │   ├── email.py                  EmailService (SMTP)
│   │   ├── auth.py                   magic-link + password helpers
│   │   └── webhooks.py               Square webhook handler
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── storefront.py             /, /shop, /shop/<category>, /products/<slug>
│   │   ├── cart.py                   /cart, /cart/add, /cart/remove, /cart/update
│   │   ├── checkout.py               /checkout, /checkout/submit, /order/<token>
│   │   ├── admin_auth.py             /admin/login, /admin/logout
│   │   ├── account_auth.py           /account/login, /account/logout (routes only, no surfaces yet)
│   │   ├── api.py                    /api/webhooks/square, /health
│   ├── templates/
│   │   ├── base.html                 shell: nav, footer, cart drawer
│   │   ├── storefront/
│   │   │   ├── home.html
│   │   │   ├── shop.html
│   │   │   ├── product_detail.html
│   │   ├── cart/
│   │   │   ├── cart.html
│   │   │   └── _drawer.html
│   │   ├── checkout/
│   │   │   ├── checkout.html
│   │   │   └── order_confirmation.html
│   │   ├── auth/
│   │   │   ├── admin_login.html
│   │   │   ├── magic_link_sent.html
│   │   ├── emails/
│   │   │   ├── order_confirmation.html
│   │   │   ├── order_confirmation.txt
│   │   │   └── magic_link.html
│   │   └── errors/
│   │       ├── 404.html
│   │       ├── 500.html
│   └── static/
│       ├── css/
│       │   ├── input.css             Tailwind entry
│       │   └── output.css            generated (gitignored in dev)
│       ├── js/
│       │   ├── alpine_init.js
│       │   ├── cart_drawer.js
│       │   └── checkout.js           wires Square Web Payments SDK
│       └── catalog/images/           images copied in by import
└── tests/
    ├── conftest.py                   app, db, client fixtures
    ├── unit/
    │   ├── test_models_base.py
    │   ├── test_models_catalog.py
    │   ├── test_services_cart.py
    │   ├── test_services_inventory.py
    │   ├── test_services_tax_stub.py
    │   ├── test_services_shipping_stub.py
    │   ├── test_services_catalog_import.py
    │   ├── test_services_checkout.py (Square mocked)
    │   ├── test_services_refunds.py (Square mocked)
    │   ├── test_services_webhooks.py
    │   ├── test_services_auth.py
    │   └── test_routes_storefront.py
    ├── integration/
    │   ├── test_checkout_sandbox.py  (real Square sandbox — marked sandbox_live)
    │   ├── test_webhook_endpoint.py
    │   └── test_catalog_import.py
    └── smoke/
        └── test_compose_boot.py
```

Nothing in this plan creates files outside `Solex/` except the plan file itself and a one-line Linear cross-reference in commit messages.

---

## Chunk 1: Repo scaffold + Docker

Goal at end of chunk: `docker compose build` produces `solex-web` and `solex-worker` images; the web container boots (even though no routes exist yet) and answers `/health`; tests scaffold runs with 0 collected.

### Task 1.1 — Create repo skeleton

**Files:**
- Create: `Solex/.gitignore`
- Create: `Solex/pyproject.toml`
- Create: `Solex/README.md`
- Create: `Solex/.env.example`

- [ ] **Step 1: Create Solex directory + .gitignore**

```bash
mkdir -p ~/GrowDirect/Solex
cd ~/GrowDirect/Solex
cat > .gitignore <<'EOF'
__pycache__/
*.py[cod]
.venv/
.env
.env.local
*.egg-info/
node_modules/
solex/static/css/output.css
solex/static/catalog/images/*
!solex/static/catalog/images/.gitkeep
.pytest_cache/
.coverage
htmlcov/
dist/
build/
EOF
```

- [ ] **Step 2: Create pyproject.toml**

```toml
[project]
name = "solex"
version = "0.1.0"
description = "Solex commerce mockup — Canary-observable Square sandbox merchant"
requires-python = ">=3.12"

[tool.ruff]
line-length = 100
target-version = "py312"
```

- [ ] **Step 3: Create .env.example**

```bash
# Flask
SOLEX_ENV=development
SECRET_KEY=change-me-dev-only

# Database
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/solex
TEST_DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/solex_test

# Valkey (shared; DB 2 = Solex)
VALKEY_URL=redis://growdirect_valkey:6379/2

# Square sandbox
SQUARE_ENVIRONMENT=sandbox
SQUARE_SANDBOX_APPLICATION_ID=
SQUARE_SANDBOX_ACCESS_TOKEN=
SQUARE_SANDBOX_LOCATION_ID=
SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY=

# SMTP (MailHog in dev)
SMTP_HOST=mailhog
SMTP_PORT=1025
SMTP_FROM=orders@solex.local

# Feature flags
SOLEX_FLAG_SYNC_CATALOG_TO_SQUARE=false
SOLEX_FLAG_SUB_SELFSERVE=false
```

- [ ] **Step 4: Create README.md (minimal)**

```markdown
# Solex

Canary-observable Square sandbox merchant. See
`../docs/superpowers/specs/2026-04-23-solex-commerce-mockup-design.md`.

## Dev quickstart

```bash
cp .env.example .env
# fill in Square sandbox credentials
cd devops && docker compose up -d
docker compose exec web python3 -m solex.cli catalog import
open http://localhost:5003
```
```

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect
git add Solex/
git commit -m "solex: scaffold skeleton — pyproject, gitignore, env template, readme

Refs GRO-XXX. Plan 1 task 1.1."
```

### Task 1.2 — Requirements files

**Files:**
- Create: `Solex/requirements.txt`
- Create: `Solex/requirements-dev.txt`

- [ ] **Step 1: Write requirements.txt**

```
Flask==3.0.3
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-Limiter==3.8.0
Flask-Mail==0.10.0
Flask-Session==0.8.0
SQLAlchemy==2.0.36
alembic==1.14.0
psycopg[binary]==3.2.3
redis==5.2.0
rq==1.16.2
rq-scheduler==0.14.0
squareup==38.1.0.20241017
tenacity==9.0.0
pydantic==2.9.2
PyYAML==6.0.2
gunicorn==23.0.0
click==8.1.7
python-dotenv==1.0.1
Jinja2==3.1.4
itsdangerous==2.2.0
```

- [ ] **Step 2: Write requirements-dev.txt**

```
-r requirements.txt
pytest==8.3.3
pytest-cov==6.0.0
pytest-mock==3.14.0
responses==0.25.3
freezegun==1.5.1
ruff==0.7.4
```

- [ ] **Step 3: Commit**

```bash
git add Solex/requirements.txt Solex/requirements-dev.txt
git commit -m "solex: pin runtime + dev dependencies

Refs GRO-XXX. Plan 1 task 1.2."
```

> **Flag dependency changes:** Before any future task adds a package, surface it in chat, get approval, commit the requirements change separately, and rebuild the image. Per standing feedback.

### Task 1.3 — Dockerfile

**Files:**
- Create: `Solex/devops/Dockerfile`

- [ ] **Step 1: Write Dockerfile (multi-stage)**

```dockerfile
# syntax=docker/dockerfile:1.7

# --- stage 1: tailwind build ---
FROM node:20-alpine AS assets
WORKDIR /assets
COPY package.json tailwind.config.js postcss.config.js ./
RUN npm install
COPY solex/static/css ./solex/static/css
COPY solex/templates ./solex/templates
RUN npx tailwindcss -i ./solex/static/css/input.css -o ./solex/static/css/output.css --minify

# --- stage 2: runtime ---
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .
COPY --from=assets /assets/solex/static/css/output.css ./solex/static/css/output.css

EXPOSE 5003
CMD ["gunicorn", "-b", "0.0.0.0:5003", "--reload", "--workers", "2", "wsgi:app"]
```

- [ ] **Step 2: Commit**

```bash
git add Solex/devops/Dockerfile
git commit -m "solex: Dockerfile — tailwind build + gunicorn runtime

Refs GRO-XXX. Plan 1 task 1.3."
```

### Task 1.4 — docker-compose.yml

**Files:**
- Create: `Solex/devops/docker-compose.yml`
- Create: `Solex/devops/scripts/dev.sh`

- [ ] **Step 1: Write docker-compose.yml**

```yaml
name: solex

services:
  web:
    image: solex-web
    container_name: solex_web
    build:
      context: ..
      dockerfile: devops/Dockerfile
    ports:
      - "5003:5003"
    env_file: ../.env
    environment:
      - SOLEX_ENV=development
    volumes:
      - ../solex:/app/solex
      - ../wsgi.py:/app/wsgi.py
      - ../alembic:/app/alembic
      - ../alembic.ini:/app/alembic.ini
      - ../catalog:/app/catalog
      - ../tests:/app/tests
      - ../pytest.ini:/app/pytest.ini
    depends_on:
      - mailhog
    networks:
      - growdirect

  worker:
    image: solex-worker
    container_name: solex_worker
    build:
      context: ..
      dockerfile: devops/Dockerfile
    command: ["rq", "worker", "--url", "redis://growdirect_valkey:6379/2", "solex-default"]
    env_file: ../.env
    volumes:
      - ../solex:/app/solex
    networks:
      - growdirect

  mailhog:
    image: mailhog/mailhog:latest
    container_name: solex_mailhog
    ports:
      - "1027:1025"
      - "8027:8025"
    networks:
      - growdirect

networks:
  growdirect:
    external: true
```

- [ ] **Step 2: Write dev.sh helper**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-up}" in
  up)    docker compose -f devops/docker-compose.yml up -d ;;
  down)  docker compose -f devops/docker-compose.yml down ;;
  logs)  docker compose -f devops/docker-compose.yml logs -f "${2:-web}" ;;
  shell) docker compose -f devops/docker-compose.yml exec web bash ;;
  test)  docker compose -f devops/docker-compose.yml exec web pytest "${@:2}" ;;
  *) echo "usage: dev.sh up|down|logs [svc]|shell|test" && exit 1 ;;
esac
```

```bash
chmod +x Solex/devops/scripts/dev.sh
```

- [ ] **Step 3: Commit**

```bash
git add Solex/devops/
git commit -m "solex: docker-compose — web + worker + mailhog on growdirect net

Refs GRO-XXX. Plan 1 task 1.4."
```

### Task 1.5 — Tailwind + Alpine build config

**Files:**
- Create: `Solex/package.json`
- Create: `Solex/tailwind.config.js`
- Create: `Solex/postcss.config.js`
- Create: `Solex/solex/static/css/input.css`

- [ ] **Step 1: Write package.json**

```json
{
  "name": "solex-assets",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "build:css": "tailwindcss -i ./solex/static/css/input.css -o ./solex/static/css/output.css --minify",
    "watch:css": "tailwindcss -i ./solex/static/css/input.css -o ./solex/static/css/output.css --watch"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.14",
    "postcss": "^8.4.47",
    "autoprefixer": "^10.4.20",
    "@tailwindcss/forms": "^0.5.9",
    "@tailwindcss/typography": "^0.5.15"
  },
  "dependencies": {
    "alpinejs": "^3.14.3"
  }
}
```

- [ ] **Step 2: Write tailwind.config.js**

```js
module.exports = {
  content: [
    './solex/templates/**/*.html',
    './solex/static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        solex: { /* placeholder palette — Plan 4 replaces this */ },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

- [ ] **Step 3: Write postcss.config.js**

```js
module.exports = {
  plugins: { tailwindcss: {}, autoprefixer: {} },
};
```

- [ ] **Step 4: Write solex/static/css/input.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 5: Commit**

```bash
git add Solex/package.json Solex/tailwind.config.js Solex/postcss.config.js Solex/solex/static/css/input.css
git commit -m "solex: tailwind + alpine build config

Refs GRO-XXX. Plan 1 task 1.5."
```

### Task 1.6 — Minimal wsgi.py + create_app stub + /health

This is the first thing that must actually run inside the container. We'll expand the app factory in Chunk 2; here we prove the build works.

**Files:**
- Create: `Solex/wsgi.py`
- Create: `Solex/solex/__init__.py`
- Create: `Solex/solex/routes/__init__.py`
- Create: `Solex/solex/routes/api.py`
- Create: `Solex/tests/__init__.py`
- Create: `Solex/tests/smoke/__init__.py`
- Create: `Solex/tests/smoke/test_health.py`
- Create: `Solex/pytest.ini`

- [ ] **Step 1: Write pytest.ini**

```ini
[pytest]
testpaths = tests
markers =
    sandbox_live: requires real Square sandbox credentials (skipped in CI default)
addopts = -ra --strict-markers
```

- [ ] **Step 2: Write the smoke test (fails first)**

```python
# tests/smoke/test_health.py
def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"ok": True}
```

- [ ] **Step 3: Run the test and confirm it fails**

```bash
cd ~/GrowDirect/Solex
docker compose -f devops/docker-compose.yml build web
docker compose -f devops/docker-compose.yml run --rm web pytest tests/smoke/test_health.py -v
```

Expected: fail — `client` fixture undefined.

- [ ] **Step 4: Write the minimal app factory + health route**

```python
# solex/routes/api.py
from flask import Blueprint, jsonify

bp = Blueprint("api", __name__)

@bp.get("/health")
def health():
    return jsonify(ok=True)
```

```python
# solex/routes/__init__.py
from solex.routes import api
__all__ = ["api"]
```

```python
# solex/__init__.py
from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    from solex.routes import api
    app.register_blueprint(api.bp)
    return app
```

```python
# wsgi.py
from solex import create_app
app = create_app()
```

- [ ] **Step 5: Write the conftest that provides `client`**

```python
# tests/conftest.py
import pytest
from solex import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app

@pytest.fixture()
def client(app):
    return app.test_client()
```

- [ ] **Step 6: Run the test again and confirm it passes**

```bash
docker compose -f devops/docker-compose.yml run --rm web pytest tests/smoke/test_health.py -v
```

Expected: PASS.

- [ ] **Step 7: Bring the stack up and curl health**

```bash
docker compose -f devops/docker-compose.yml up -d web
sleep 2
curl -s http://localhost:5003/health
```

Expected output: `{"ok":true}`

- [ ] **Step 8: Commit**

```bash
git add Solex/
git commit -m "solex: app factory + /health — container boots, smoke green

Refs GRO-XXX. Plan 1 task 1.6."
```

**Checkpoint — chunk 1 done.** The container boots, health responds, tests scaffold works. Nothing domain-specific yet.

---

## Chunk 2: Config, extensions, base models

Goal: real `BaseConfig`/`DevConfig`/`TestConfig`/`ProdConfig`, SQLAlchemy wired against Postgres, Alembic initialized, `BaseModel` with UUID PK + timestamps, Flask-Session pointed at Valkey DB 2. Test DB created and used by tests.

### Task 2.1 — Config classes

**Files:**
- Create: `Solex/solex/config.py`
- Modify: `Solex/solex/__init__.py`
- Create: `Solex/tests/unit/test_config.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_config.py
from solex.config import resolve_config, DevConfig, TestConfig, ProdConfig

def test_dev_env_returns_dev_config(monkeypatch):
    monkeypatch.setenv("SOLEX_ENV", "development")
    assert resolve_config() is DevConfig

def test_test_env_returns_test_config(monkeypatch):
    monkeypatch.setenv("SOLEX_ENV", "testing")
    assert resolve_config() is TestConfig

def test_invalid_env_raises(monkeypatch):
    monkeypatch.setenv("SOLEX_ENV", "bogus")
    import pytest
    with pytest.raises(ValueError):
        resolve_config()
```

- [ ] **Step 2: Confirm failure**

`pytest tests/unit/test_config.py -v` → ImportError.

- [ ] **Step 3: Write config.py**

```python
# solex/config.py
import os

class BaseConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    VALKEY_URL = os.environ["VALKEY_URL"]
    SESSION_TYPE = "redis"
    SESSION_KEY_PREFIX = "solex:session:"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 3600
    WTF_CSRF_TIME_LIMIT = None
    SQUARE_ENVIRONMENT = os.environ.get("SQUARE_ENVIRONMENT", "sandbox")
    SQUARE_APPLICATION_ID = os.environ.get("SQUARE_SANDBOX_APPLICATION_ID", "")
    SQUARE_ACCESS_TOKEN = os.environ.get("SQUARE_SANDBOX_ACCESS_TOKEN", "")
    SQUARE_LOCATION_ID = os.environ.get("SQUARE_SANDBOX_LOCATION_ID", "")
    SQUARE_WEBHOOK_SIGNATURE_KEY = os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", "")
    SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "1025"))
    SMTP_FROM = os.environ.get("SMTP_FROM", "orders@solex.local")
    TAX_RATE_PCT = float(os.environ.get("TAX_RATE_PCT", "0.0"))
    SHIPPING_FLAT_CENTS = int(os.environ.get("SHIPPING_FLAT_CENTS", "695"))
    SHIPPING_FREE_THRESHOLD_CENTS = int(os.environ.get("SHIPPING_FREE_THRESHOLD_CENTS", "9900"))

class DevConfig(BaseConfig):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        BaseConfig.SQLALCHEMY_DATABASE_URI + "_test",
    )
    WTF_CSRF_ENABLED = False

class ProdConfig(BaseConfig):
    DEBUG = False

def resolve_config():
    env = os.environ.get("SOLEX_ENV", "development").lower()
    match env:
        case "development": return DevConfig
        case "testing":     return TestConfig
        case "production":  return ProdConfig
        case _: raise ValueError(f"Invalid SOLEX_ENV: {env}")
```

- [ ] **Step 4: Wire into create_app**

```python
# solex/__init__.py
from flask import Flask
from solex.config import resolve_config

def create_app(config_cls=None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_cls or resolve_config())
    from solex.routes import api
    app.register_blueprint(api.bp)
    return app
```

- [ ] **Step 5: Update conftest to pass TestConfig**

```python
# tests/conftest.py
import pytest
from solex import create_app
from solex.config import TestConfig

@pytest.fixture()
def app():
    return create_app(TestConfig)

@pytest.fixture()
def client(app):
    return app.test_client()
```

- [ ] **Step 6: Run tests green**

```bash
docker compose -f devops/docker-compose.yml run --rm \
  -e SOLEX_ENV=testing -e SECRET_KEY=test \
  -e DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/solex \
  -e TEST_DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/solex_test \
  -e VALKEY_URL=redis://growdirect_valkey:6379/2 \
  web pytest tests/unit/test_config.py tests/smoke/test_health.py -v
```

Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add Solex/
git commit -m "solex: config classes — Base/Dev/Test/Prod + env resolution

Refs GRO-XXX. Plan 1 task 2.1."
```

### Task 2.2 — Create Postgres databases

**Files:** (no app files; Postgres-side only)

- [ ] **Step 1: Create solex + solex_test databases**

```bash
docker exec -i growdirect_postgres psql -U growdirect -d postgres <<'SQL'
CREATE DATABASE solex OWNER growdirect;
CREATE DATABASE solex_test OWNER growdirect;
SQL
```

- [ ] **Step 2: Verify**

```bash
docker exec -i growdirect_postgres psql -U growdirect -d postgres -c "\l" | grep solex
```

Expected: both `solex` and `solex_test` listed.

### Task 2.3 — Extensions (db, login, csrf, limiter, session, mail)

**Files:**
- Create: `Solex/solex/extensions.py`
- Modify: `Solex/solex/__init__.py`

- [ ] **Step 1: Write extensions.py**

```python
# solex/extensions.py
import redis
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self):
        self.engine = None
        self.session = None

    def init_app(self, app):
        self.engine = create_engine(
            app.config["SQLALCHEMY_DATABASE_URI"],
            **app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {}),
        )
        self.session = scoped_session(sessionmaker(bind=self.engine, future=True))

        @app.teardown_appcontext
        def remove_session(exc=None):
            self.session.remove()

db = Database()
admin_login = LoginManager()
admin_login.login_view = "admin_auth.login"
customer_login = LoginManager()
customer_login.login_view = "account_auth.login"
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
server_session = Session()
mail = Mail()

def init_extensions(app):
    db.init_app(app)
    admin_login.init_app(app)
    customer_login.init_app(app)
    csrf.init_app(app)

    app.config["SESSION_REDIS"] = redis.Redis.from_url(app.config["VALKEY_URL"])
    server_session.init_app(app)

    storage_uri = app.config["VALKEY_URL"]
    limiter.storage_uri = storage_uri
    limiter.init_app(app)

    app.config.setdefault("MAIL_SERVER", app.config["SMTP_HOST"])
    app.config.setdefault("MAIL_PORT", app.config["SMTP_PORT"])
    app.config.setdefault("MAIL_DEFAULT_SENDER", app.config["SMTP_FROM"])
    mail.init_app(app)
```

> Two `LoginManager` instances because admin and customer audiences must not share user_loader state. Each blueprint binds to its own.

- [ ] **Step 2: Wire into create_app**

```python
# solex/__init__.py
from flask import Flask
from solex.config import resolve_config
from solex.extensions import init_extensions

def create_app(config_cls=None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_cls or resolve_config())
    init_extensions(app)
    from solex.routes import api
    app.register_blueprint(api.bp)
    return app
```

- [ ] **Step 3: Verify boot**

```bash
docker compose -f devops/docker-compose.yml restart web
sleep 2
curl -s http://localhost:5003/health
```

Expected: `{"ok":true}`.

- [ ] **Step 4: Commit**

```bash
git add Solex/
git commit -m "solex: extensions — db, logins, csrf, limiter, session, mail

Refs GRO-XXX. Plan 1 task 2.3."
```

### Task 2.4 — BaseModel (UUID PK + timestamps)

**Files:**
- Create: `Solex/solex/models/__init__.py`
- Create: `Solex/solex/models/base.py`
- Create: `Solex/tests/unit/test_models_base.py`

- [ ] **Step 1: Write failing test**

```python
# tests/unit/test_models_base.py
import uuid
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

class ThingForTest(BaseModel):
    __tablename__ = "things_for_test"
    name: Mapped[str] = mapped_column(String(32))

def test_base_has_uuid_pk_and_timestamps():
    assert hasattr(ThingForTest, "id")
    assert hasattr(ThingForTest, "created_at")
    assert hasattr(ThingForTest, "updated_at")
    t = ThingForTest(name="x")
    assert t.id is None or isinstance(t.id, uuid.UUID)
```

- [ ] **Step 2: Confirm failure**

`pytest tests/unit/test_models_base.py -v` → ImportError.

- [ ] **Step 3: Write base.py**

```python
# solex/models/base.py
import uuid
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.extensions import Base

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
        onupdate=func.now(), nullable=False,
    )
```

- [ ] **Step 4: Write models/__init__.py (empty for now, will aggregate later)**

```python
# solex/models/__init__.py
from solex.models.base import BaseModel
__all__ = ["BaseModel"]
```

- [ ] **Step 5: Run test green**

```bash
docker compose -f devops/docker-compose.yml run --rm web pytest tests/unit/test_models_base.py -v
```

- [ ] **Step 6: Commit**

```bash
git add Solex/
git commit -m "solex: BaseModel — UUID PK + timestamps

Refs GRO-XXX. Plan 1 task 2.4."
```

### Task 2.5 — Alembic init + empty migration 0001

**Files:**
- Create: `Solex/alembic.ini`
- Create: `Solex/alembic/env.py`
- Create: `Solex/alembic/script.py.mako`
- Create: `Solex/alembic/versions/0001_initial.py` (empty — populated in Chunk 3)

- [ ] **Step 1: Initialize Alembic (inside container)**

```bash
docker compose -f devops/docker-compose.yml run --rm web alembic init alembic
```

- [ ] **Step 2: Edit `alembic/env.py` to use our metadata**

```python
# alembic/env.py (only the changed bits)
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from solex.config import resolve_config
from solex.extensions import Base

# Import all models so MetaData is populated (none yet; added in Chunk 3):
# import solex.models  # noqa

config = context.config
cfg = resolve_config()
config.set_main_option("sqlalchemy.url", cfg.SQLALCHEMY_DATABASE_URI)
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 3: Confirm a no-op migration can run**

```bash
docker compose -f devops/docker-compose.yml run --rm web alembic upgrade head
```

Expected: "INFO  [alembic.runtime.migration] Context impl PostgresqlImpl." and nothing else. `alembic_version` table exists.

- [ ] **Step 4: Commit**

```bash
git add Solex/alembic* Solex/alembic/
git commit -m "solex: alembic init — wired to Base metadata, no migrations yet

Refs GRO-XXX. Plan 1 task 2.5."
```

**Checkpoint — chunk 2 done.** Config + DB + Alembic + BaseModel are real. Next: the data model.

---

## Chunk 3: Data model

Goal: every table in Plan 1 scope exists via SQLAlchemy models, with the initial Alembic migration creating them. Each model has a minimal unit test asserting it can be instantiated and persisted.

Tables in this chunk: `Category`, `Product`, `ProductTag`, `Inventory`, `InventoryAdjustment`, `Cart`, `CartLine`, `Order`, `OrderItem`, `OrderNote`, `Refund`, `Customer`, `Address`, `AdminUser`, `MagicLinkToken`, `SquareWebhookEvent`, `EmailLog`.

> Follow the same TDD rhythm for each: write model + test, run failing, implement, run green, commit. I'll show the pattern in Task 3.1 and elide repetition for the rest — each later task lists only the model code + the test.

### Task 3.1 — Catalog models (Category, Product, ProductTag)

**Files:**
- Create: `Solex/solex/models/catalog.py`
- Create: `Solex/tests/unit/test_models_catalog.py`
- Modify: `Solex/solex/models/__init__.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_models_catalog.py
from solex.models.catalog import Category, Product, ProductTag

def test_category_fields():
    c = Category(name="Supplements", slug="supplements", sort=1)
    assert c.name == "Supplements"

def test_product_fields():
    p = Product(
        sku="AO-YOUTH-30",
        slug="ao-youth-30",
        name="AO Youth 30ct",
        description="...",
        price_cents=4995,
        image_path="catalog/images/ao-youth-30.jpg",
        active=True,
        weight_grams=120,
    )
    assert p.sku == "AO-YOUTH-30"
    assert p.price_cents == 4995

def test_product_tag_links_to_product():
    t = ProductTag(tag="wellness")
    assert t.tag == "wellness"
```

- [ ] **Step 2: Confirm failure** — `pytest tests/unit/test_models_catalog.py -v` → ImportError.

- [ ] **Step 3: Write the models**

```python
# solex/models/catalog.py
import uuid
from typing import Optional
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    sort: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    products: Mapped[list["Product"]] = relationship(back_populates="category")

class Product(BaseModel):
    __tablename__ = "products"
    sku: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(240), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    compare_at_cents: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    image_path: Mapped[str] = mapped_column(String(400), default="", nullable=False)
    gallery_paths: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weight_grams: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    dimensions_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    square_catalog_object_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    category: Mapped[Optional[Category]] = relationship(back_populates="products")
    tags: Mapped[list["ProductTag"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_products_active", "active"),
    )

class ProductTag(BaseModel):
    __tablename__ = "product_tags"
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    tag: Mapped[str] = mapped_column(String(80), nullable=False)
    product: Mapped[Product] = relationship(back_populates="tags")
```

- [ ] **Step 4: Re-export from models/__init__.py**

```python
# solex/models/__init__.py
from solex.models.base import BaseModel
from solex.models.catalog import Category, Product, ProductTag

__all__ = ["BaseModel", "Category", "Product", "ProductTag"]
```

- [ ] **Step 5: Run test green**

```bash
docker compose -f devops/docker-compose.yml run --rm web pytest tests/unit/test_models_catalog.py -v
```

- [ ] **Step 6: Commit**

```bash
git add Solex/solex/models/catalog.py Solex/solex/models/__init__.py Solex/tests/unit/test_models_catalog.py
git commit -m "solex(models): Category, Product, ProductTag

Refs GRO-XXX. Plan 1 task 3.1."
```

### Task 3.2 — Inventory models

**Files:**
- Create: `Solex/solex/models/inventory.py`
- Create: `Solex/tests/unit/test_models_inventory.py`
- Modify: `Solex/solex/models/__init__.py`

Same TDD rhythm.

```python
# solex/models/inventory.py
import uuid
from typing import Optional
from sqlalchemy import Integer, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

class Inventory(BaseModel):
    __tablename__ = "inventories"
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"),
        unique=True, nullable=False,
    )
    on_hand: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reorder_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

class InventoryAdjustment(BaseModel):
    __tablename__ = "inventory_adjustments"
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False,
    )
    delta: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(40), nullable=False)  # sale|refund|restock|shrink|correction|initial
    order_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True,
    )
    refund_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("refunds.id", ondelete="SET NULL"), nullable=True,
    )
    scenario_tag: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    note: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    __table_args__ = (
        Index("ix_inv_adj_product", "product_id"),
        Index("ix_inv_adj_reason", "reason"),
    )
```

Test:

```python
# tests/unit/test_models_inventory.py
from solex.models.inventory import Inventory, InventoryAdjustment

def test_inventory_has_product_link():
    inv = Inventory(on_hand=10)
    assert inv.on_hand == 10

def test_adjustment_requires_reason_and_delta():
    adj = InventoryAdjustment(delta=-1, reason="sale")
    assert adj.delta == -1
    assert adj.reason == "sale"
```

Commit message: `solex(models): Inventory + InventoryAdjustment. Refs GRO-XXX.`

### Task 3.3 — Customer + Address + AdminUser + MagicLinkToken

- [ ] Follow the same rhythm. Files:
  - `solex/models/customer.py` — `Customer`, `Address`
  - `solex/models/admin.py` — `AdminUser`
  - `solex/models/auth.py` — `MagicLinkToken`
  - Matching tests under `tests/unit/`

```python
# solex/models/customer.py
import uuid
from typing import Optional
from sqlalchemy import String, ForeignKey, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    square_customer_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    default_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True,
        use_existing_column=False,
    )
    addresses: Mapped[list["Address"]] = relationship(
        "Address", primaryjoin="Address.customer_id == Customer.id",
        back_populates="customer", cascade="all, delete-orphan",
    )

class Address(BaseModel):
    __tablename__ = "addresses"
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False,
    )
    label: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    line1: Mapped[str] = mapped_column(String(200), nullable=False)
    line2: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    city: Mapped[str] = mapped_column(String(120), nullable=False)
    region: Mapped[str] = mapped_column(String(80), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(2), default="US", nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    customer: Mapped["Customer"] = relationship(
        "Customer", primaryjoin="Address.customer_id == Customer.id",
        back_populates="addresses",
    )
```

```python
# solex/models/admin.py
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

class AdminUser(BaseModel):
    __tablename__ = "admin_users"
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
```

```python
# solex/models/auth.py
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

class MagicLinkToken(BaseModel):
    __tablename__ = "magic_link_tokens"
    audience: Mapped[str] = mapped_column(String(16), nullable=False)  # "admin" | "customer"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (Index("ix_mlt_audience_user", "audience", "user_id"),)
```

Test files are one `instantiate + assert a field` test per model. Commit after each file following the established pattern. Commit messages: `solex(models): Customer + Address`, `solex(models): AdminUser`, `solex(models): MagicLinkToken`.

### Task 3.4 — Cart + CartLine

- [ ] Follow the rhythm. File `solex/models/cart.py`:

```python
# solex/models/cart.py
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

class Cart(BaseModel):
    __tablename__ = "carts"
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True,
    )
    session_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    applied_promo_code: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recovered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    abandonment_emailed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    lines: Mapped[list["CartLine"]] = relationship(back_populates="cart", cascade="all, delete-orphan")
    __table_args__ = (
        Index("ix_carts_session", "session_key"),
        Index("ix_carts_customer", "customer_id"),
    )

class CartLine(BaseModel):
    __tablename__ = "cart_lines"
    cart_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("carts.id", ondelete="CASCADE"), nullable=False,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False,
    )
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    price_snapshot_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    cart: Mapped["Cart"] = relationship(back_populates="lines")
```

Test + commit as above. Commit message: `solex(models): Cart + CartLine`.

### Task 3.5 — Order + OrderItem + OrderNote

- [ ] File `solex/models/order.py`:

```python
# solex/models/order.py
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from solex.models.base import BaseModel

ORDER_STATUSES = ("pending", "paid", "shipped", "delivered",
                  "refunded", "partially_refunded", "cancelled", "failed")

class Order(BaseModel):
    __tablename__ = "orders"
    public_token: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    customer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True,
    )
    customer_email: Mapped[str] = mapped_column(String(254), nullable=False)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    shipping_address_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    billing_address_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    subtotal_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    tax_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    shipping_cents: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)
    square_order_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    square_payment_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    autoship: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    autoship_subscription_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True,
    )
    scenario_tag: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    placed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fulfilled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    tracking_number: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    notes: Mapped[list["OrderNote"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    __table_args__ = (
        Index("ix_orders_status", "status"),
        Index("ix_orders_placed_at", "placed_at"),
        Index("ix_orders_scenario_tag", "scenario_tag"),
    )

class OrderItem(BaseModel):
    __tablename__ = "order_items"
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,
    )
    product_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"), nullable=True,
    )
    sku_snapshot: Mapped[str] = mapped_column(String(64), nullable=False)
    name_snapshot: Mapped[str] = mapped_column(String(240), nullable=False)
    image_path_snapshot: Mapped[str] = mapped_column(String(400), default="", nullable=False)
    price_snapshot_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    line_total_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped["Order"] = relationship(back_populates="items")

class OrderNote(BaseModel):
    __tablename__ = "order_notes"
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,
    )
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    internal: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    order: Mapped["Order"] = relationship(back_populates="notes")
```

Test + commit: `solex(models): Order + OrderItem + OrderNote`.

### Task 3.6 — Refund + SquareWebhookEvent + EmailLog

- [ ] File `solex/models/refund.py`:

```python
# solex/models/refund.py
import uuid
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

class Refund(BaseModel):
    __tablename__ = "refunds"
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False,
    )
    square_refund_id: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(120), nullable=False)
    admin_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True,
    )
    scenario_tag: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
```

- [ ] File `solex/models/ops.py`:

```python
# solex/models/ops.py
from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from solex.models.base import BaseModel

class SquareWebhookEvent(BaseModel):
    __tablename__ = "square_webhook_events"
    square_event_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

class EmailLog(BaseModel):
    __tablename__ = "email_logs"
    template: Mapped[str] = mapped_column(String(80), nullable=False)
    to: Mapped[str] = mapped_column(String(254), nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    provider_message_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
```

Tests + commit as pattern.

### Task 3.7 — Aggregate models/__init__.py + generate 0001 migration

**Files:**
- Modify: `Solex/solex/models/__init__.py`
- Replace: `Solex/alembic/versions/0001_initial.py` with an autogenerated migration.

- [ ] **Step 1: Update `models/__init__.py` to import all models**

```python
# solex/models/__init__.py
from solex.models.base import BaseModel
from solex.models.catalog import Category, Product, ProductTag
from solex.models.inventory import Inventory, InventoryAdjustment
from solex.models.customer import Customer, Address
from solex.models.admin import AdminUser
from solex.models.auth import MagicLinkToken
from solex.models.cart import Cart, CartLine
from solex.models.order import Order, OrderItem, OrderNote, ORDER_STATUSES
from solex.models.refund import Refund
from solex.models.ops import SquareWebhookEvent, EmailLog

__all__ = [
    "BaseModel",
    "Category", "Product", "ProductTag",
    "Inventory", "InventoryAdjustment",
    "Customer", "Address",
    "AdminUser", "MagicLinkToken",
    "Cart", "CartLine",
    "Order", "OrderItem", "OrderNote", "ORDER_STATUSES",
    "Refund",
    "SquareWebhookEvent", "EmailLog",
]
```

- [ ] **Step 2: Import models into alembic env**

Edit `alembic/env.py` — uncomment: `import solex.models  # noqa`.

- [ ] **Step 3: Generate the migration**

```bash
docker compose -f devops/docker-compose.yml run --rm web \
  alembic revision --autogenerate -m "initial schema"
```

- [ ] **Step 4: Review the generated file**

Rename the generated file to `0001_initial.py` (delete the placeholder empty file if present). Verify every model you added is present as `op.create_table`. If anything's missing, the likely cause is a forgotten `import` in `solex/models/__init__.py`.

- [ ] **Step 5: Run upgrade**

```bash
docker compose -f devops/docker-compose.yml run --rm web alembic upgrade head
```

- [ ] **Step 6: Verify tables exist in both DBs**

```bash
docker exec -i growdirect_postgres psql -U growdirect -d solex -c "\dt"
# then again for solex_test:
SOLEX_ENV=testing docker compose -f devops/docker-compose.yml run --rm -e SOLEX_ENV=testing web alembic upgrade head
docker exec -i growdirect_postgres psql -U growdirect -d solex_test -c "\dt"
```

Expected: all 15+ tables listed in both.

- [ ] **Step 7: Commit**

```bash
git add Solex/
git commit -m "solex(models): initial migration — all foundation tables

Refs GRO-XXX. Plan 1 task 3.7."
```

**Checkpoint — chunk 3 done.** Data model is live in both databases.

---

## Chunk 4: Services (strategy stubs + inventory + cart + catalog + catalog import)

Goal: the backing services for storefront flows exist and are unit-tested. Square integration still a stub; checkout/webhooks come in Chunks 6 and 7.

### Task 4.1 — Tax, shipping, address, fulfillment strategy stubs

**Files:**
- Create: `Solex/solex/services/__init__.py`
- Create: `Solex/solex/services/tax.py`
- Create: `Solex/solex/services/shipping.py`
- Create: `Solex/solex/services/addresses.py`
- Create: `Solex/solex/services/fulfillment.py`
- Create: `Solex/tests/unit/test_services_tax_stub.py`
- Create: `Solex/tests/unit/test_services_shipping_stub.py`

- [ ] Write each via TDD. Code:

```python
# solex/services/tax.py
from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class TaxCalculation:
    tax_cents: int

class TaxService(Protocol):
    def compute(self, subtotal_cents: int, shipping_cents: int, region: str) -> TaxCalculation: ...

class FlatRateTaxStub:
    def __init__(self, rate_pct: float):
        self.rate_pct = rate_pct
    def compute(self, subtotal_cents: int, shipping_cents: int, region: str) -> TaxCalculation:
        total = subtotal_cents + shipping_cents
        return TaxCalculation(tax_cents=round(total * (self.rate_pct / 100.0)))
```

```python
# solex/services/shipping.py
from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class ShippingQuote:
    shipping_cents: int
    label: str

class ShippingService(Protocol):
    def quote(self, subtotal_cents: int, region: str) -> ShippingQuote: ...

class FlatRateShippingStub:
    def __init__(self, flat_cents: int, free_threshold_cents: int):
        self.flat_cents = flat_cents
        self.free_threshold_cents = free_threshold_cents
    def quote(self, subtotal_cents: int, region: str) -> ShippingQuote:
        if subtotal_cents >= self.free_threshold_cents:
            return ShippingQuote(shipping_cents=0, label="Free ground")
        return ShippingQuote(shipping_cents=self.flat_cents, label="Flat ground")
```

```python
# solex/services/addresses.py
from typing import Protocol

class AddressValidator(Protocol):
    def validate(self, address: dict) -> tuple[bool, list[str]]: ...

class NoopValidator:
    REQUIRED = ("first_name", "last_name", "line1", "city", "region", "postal_code", "country")
    def validate(self, address: dict) -> tuple[bool, list[str]]:
        missing = [k for k in self.REQUIRED if not address.get(k)]
        return (not missing, missing)
```

```python
# solex/services/fulfillment.py
from typing import Protocol

class FulfillmentService(Protocol):
    def mark_shipped(self, order_id, tracking_number: str | None = None) -> None: ...

class ManualFulfillmentStub:
    def mark_shipped(self, order_id, tracking_number=None):
        # real impl will also enqueue shipment emails etc.
        return None
```

Tests (tax + shipping enough; others get exercised in later chunks):

```python
# tests/unit/test_services_tax_stub.py
from solex.services.tax import FlatRateTaxStub

def test_zero_tax_when_rate_zero():
    stub = FlatRateTaxStub(rate_pct=0.0)
    assert stub.compute(10000, 695, "CA").tax_cents == 0

def test_computes_on_subtotal_plus_shipping():
    stub = FlatRateTaxStub(rate_pct=8.0)
    assert stub.compute(10000, 695, "CA").tax_cents == round(10695 * 0.08)
```

```python
# tests/unit/test_services_shipping_stub.py
from solex.services.shipping import FlatRateShippingStub

def test_flat_rate_under_threshold():
    s = FlatRateShippingStub(flat_cents=695, free_threshold_cents=9900)
    assert s.quote(5000, "CA").shipping_cents == 695

def test_free_over_threshold():
    s = FlatRateShippingStub(flat_cents=695, free_threshold_cents=9900)
    assert s.quote(15000, "CA").shipping_cents == 0
```

Commit: `solex(services): tax/shipping/address/fulfillment stubs`.

### Task 4.2 — Inventory service

**Files:**
- Create: `Solex/solex/services/inventory.py`
- Create: `Solex/tests/unit/test_services_inventory.py`

- [ ] TDD. Code:

```python
# solex/services/inventory.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import Inventory, InventoryAdjustment, Order, Refund

class InventoryError(Exception):
    pass

class InventoryService:
    def __init__(self, session: Session):
        self.session = session

    def on_hand(self, product_id) -> int:
        inv = self.session.execute(
            select(Inventory).where(Inventory.product_id == product_id).with_for_update()
        ).scalar_one_or_none()
        return inv.on_hand if inv else 0

    def adjust(self, product_id, delta: int, reason: str, **ctx) -> InventoryAdjustment:
        inv = self.session.execute(
            select(Inventory).where(Inventory.product_id == product_id).with_for_update()
        ).scalar_one_or_none()
        if inv is None:
            inv = Inventory(product_id=product_id, on_hand=0)
            self.session.add(inv)
            self.session.flush()
        inv.on_hand += delta
        adj = InventoryAdjustment(product_id=product_id, delta=delta, reason=reason, **ctx)
        self.session.add(adj)
        self.session.flush()
        return adj

    def decrement_for_order(self, order: Order):
        for item in order.items:
            self.adjust(item.product_id, -item.qty, reason="sale", order_id=order.id)

    def increment_for_refund(self, refund: Refund):
        order = self.session.get(Order, refund.order_id)
        for item in order.items:
            self.adjust(item.product_id, item.qty, reason="refund",
                        order_id=order.id, refund_id=refund.id)
```

Tests exercise `adjust` (happy + first-time-insert), `decrement_for_order` against a seeded order. Follow TDD. Commit: `solex(services): InventoryService`.

### Task 4.3 — Catalog service

**Files:**
- Create: `Solex/solex/services/catalog.py`
- Create: `Solex/tests/unit/test_services_catalog.py`

```python
# solex/services/catalog.py
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from solex.models import Product, Category

class CatalogService:
    def __init__(self, session: Session):
        self.session = session

    def list_products(self, category_slug: str | None = None, active_only: bool = True):
        q = select(Product).options(selectinload(Product.category))
        if active_only:
            q = q.where(Product.active == True)
        if category_slug:
            q = q.join(Category).where(Category.slug == category_slug)
        return self.session.execute(q.order_by(Product.name)).scalars().all()

    def get_product(self, slug: str) -> Product | None:
        return self.session.execute(
            select(Product).where(Product.slug == slug)
        ).scalar_one_or_none()

    def list_categories(self):
        return self.session.execute(
            select(Category).order_by(Category.sort, Category.name)
        ).scalars().all()
```

Tests + commit.

### Task 4.4 — Catalog YAML import

**Files:**
- Create: `Solex/solex/services/catalog_import.py`
- Create: `Solex/solex/cli.py`
- Create: `Solex/catalog/products.yaml` (5 seed entries)
- Create: `Solex/catalog/images/.gitkeep`
- Create: `Solex/tests/unit/test_services_catalog_import.py`
- Create: `Solex/tests/integration/test_catalog_import.py`

- [ ] **Step 1: Write the YAML seed (5 products)**

```yaml
# catalog/products.yaml
categories:
  - slug: supplements
    name: Supplements
    sort: 1
  - slug: devices
    name: Frequency Devices
    sort: 2
  - slug: therapy
    name: Light & PEMF Therapy
    sort: 3
  - slug: pet
    name: Pet
    sort: 4

products:
  - sku: AO-YOUTH-30
    slug: ao-youth-30
    name: AO Youth — 30 count
    short_description: Daily cellular support supplement.
    description: >
      Placeholder description. Real Solex copy pulled in Plan 4.
    price_cents: 4995
    image_path: catalog/images/ao-youth-30.jpg
    category_slug: supplements
    active: true
    weight_grams: 120
    starting_inventory: 100

  - sku: AO-SCAN-V1
    slug: ao-scan-v1
    name: AO Scan — Baseline
    short_description: Frequency diagnostic tool.
    description: Placeholder description.
    price_cents: 149900
    image_path: catalog/images/ao-scan.jpg
    category_slug: devices
    active: true
    weight_grams: 500
    starting_inventory: 20

  - sku: PEMF-MAT-INF
    slug: ao-infinity-mat
    name: AO Infinity Mat
    short_description: Full-body PEMF therapy mat.
    description: Placeholder description.
    price_cents: 259900
    image_path: catalog/images/infinity-mat.jpg
    category_slug: therapy
    active: true
    weight_grams: 8000
    starting_inventory: 10

  - sku: RED-LIGHT-BELT
    slug: red-light-belt
    name: Red Light Belt
    short_description: Targeted red light therapy belt.
    description: Placeholder description.
    price_cents: 34900
    image_path: catalog/images/red-light-belt.jpg
    category_slug: therapy
    active: true
    weight_grams: 900
    starting_inventory: 40

  - sku: PET-GUT-60
    slug: pet-gut-60
    name: Pet Gut — 60 count
    short_description: Pet gut support.
    description: Placeholder description.
    price_cents: 3495
    image_path: catalog/images/pet-gut.jpg
    category_slug: pet
    active: true
    weight_grams: 90
    starting_inventory: 60
```

- [ ] **Step 2: Write the import service**

```python
# solex/services/catalog_import.py
from pathlib import Path
from typing import Iterable
import shutil
import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session
from solex.models import Category, Product, Inventory

class CatalogImporter:
    def __init__(self, session: Session, catalog_root: Path, static_root: Path):
        self.session = session
        self.catalog_root = Path(catalog_root)
        self.static_root = Path(static_root)

    def import_from_yaml(self, yaml_path: Path) -> dict:
        data = yaml.safe_load(Path(yaml_path).read_text())
        counts = {"categories": {"inserted": 0, "updated": 0},
                  "products":   {"inserted": 0, "updated": 0}}

        slug_to_cat = {}
        for c in data.get("categories", []):
            cat = self.session.execute(
                select(Category).where(Category.slug == c["slug"])
            ).scalar_one_or_none()
            if cat is None:
                cat = Category(slug=c["slug"], name=c["name"], sort=c.get("sort", 0))
                self.session.add(cat)
                counts["categories"]["inserted"] += 1
            else:
                cat.name = c["name"]; cat.sort = c.get("sort", 0)
                counts["categories"]["updated"] += 1
            slug_to_cat[c["slug"]] = cat
        self.session.flush()

        for p in data.get("products", []):
            prod = self.session.execute(
                select(Product).where(Product.sku == p["sku"])
            ).scalar_one_or_none()
            category = slug_to_cat.get(p.get("category_slug"))
            fields = dict(
                sku=p["sku"], slug=p["slug"], name=p["name"],
                description=p.get("description", ""),
                short_description=p.get("short_description", ""),
                price_cents=p["price_cents"],
                image_path=p.get("image_path", ""),
                category_id=(category.id if category else None),
                active=p.get("active", True),
                weight_grams=p.get("weight_grams", 0),
            )
            if prod is None:
                prod = Product(**fields)
                self.session.add(prod)
                counts["products"]["inserted"] += 1
            else:
                for k, v in fields.items():
                    setattr(prod, k, v)
                counts["products"]["updated"] += 1
            self.session.flush()

            inv = self.session.execute(
                select(Inventory).where(Inventory.product_id == prod.id)
            ).scalar_one_or_none()
            if inv is None:
                self.session.add(Inventory(product_id=prod.id, on_hand=p.get("starting_inventory", 0)))

            self._copy_image(p.get("image_path"))

        self.session.commit()
        return counts

    def _copy_image(self, rel_path: str | None):
        if not rel_path:
            return
        src = self.catalog_root / rel_path.replace("catalog/", "")
        dst = self.static_root / "catalog" / rel_path.replace("catalog/", "")
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dst)
```

- [ ] **Step 3: Write CLI entry**

```python
# solex/cli.py
from pathlib import Path
import click
from solex import create_app
from solex.extensions import db
from solex.services.catalog_import import CatalogImporter

@click.group()
def cli(): ...

@cli.group()
def catalog(): ...

@catalog.command("import")
@click.option("--path", default="catalog/products.yaml", show_default=True)
def import_catalog(path):
    app = create_app()
    with app.app_context():
        importer = CatalogImporter(
            session=db.session,
            catalog_root=Path("catalog"),
            static_root=Path("solex/static"),
        )
        counts = importer.import_from_yaml(Path(path))
        click.echo(f"imported: {counts}")

if __name__ == "__main__":
    cli()
```

Wire this to `python3 -m solex.cli`: add `__main__.py`:

```python
# solex/__main__.py
from solex.cli import cli
cli()
```

- [ ] **Step 4: Integration test**

```python
# tests/integration/test_catalog_import.py
import pytest
from pathlib import Path
from solex.services.catalog_import import CatalogImporter
from solex.models import Product, Category

@pytest.fixture()
def tmp_static(tmp_path):
    (tmp_path / "catalog").mkdir()
    return tmp_path

def test_imports_seed_yaml(app, db_session, tmp_static):
    importer = CatalogImporter(
        session=db_session,
        catalog_root=Path("catalog"),
        static_root=tmp_static,
    )
    counts = importer.import_from_yaml(Path("catalog/products.yaml"))
    assert counts["products"]["inserted"] == 5
    assert db_session.query(Product).count() == 5
    assert db_session.query(Category).count() == 4

def test_reimport_is_idempotent(app, db_session, tmp_static):
    importer = CatalogImporter(db_session, Path("catalog"), tmp_static)
    importer.import_from_yaml(Path("catalog/products.yaml"))
    importer.import_from_yaml(Path("catalog/products.yaml"))
    assert db_session.query(Product).count() == 5
```

Add the fixture to conftest:

```python
# tests/conftest.py (add)
import pytest
from solex.extensions import db as _db

@pytest.fixture()
def db_session(app):
    with app.app_context():
        yield _db.session
        _db.session.rollback()
        # Tear-down: truncate all data tables (keep schema)
        for table in reversed(_db.session.get_bind().dialect.get_table_names(_db.session.get_bind())):
            _db.session.execute(text(f'TRUNCATE "{table}" CASCADE'))
        _db.session.commit()
```

- [ ] **Step 5: Run the import against dev DB**

```bash
cd ~/GrowDirect/Solex
./devops/scripts/dev.sh up
docker compose -f devops/docker-compose.yml exec web python3 -m solex.cli catalog import
```

Expected: `imported: {'categories': {'inserted': 4, 'updated': 0}, 'products': {'inserted': 5, 'updated': 0}}`.

- [ ] **Step 6: Commit**

```bash
git add Solex/
git commit -m "solex: catalog import — YAML loader + CLI + 5 seed products

Refs GRO-XXX. Plan 1 task 4.4."
```

### Task 4.5 — Cart service (Valkey-backed for guests, DB-backed for customers)

- [ ] Create `solex/services/cart.py` and `tests/unit/test_services_cart.py`.

```python
# solex/services/cart.py
import json
from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID
from redis import Redis

@dataclass
class CartSnapshot:
    currency: str
    lines: list[dict]
    subtotal_cents: int

class CartBackend(Protocol):
    def load(self, key: str) -> CartSnapshot: ...
    def save(self, key: str, snapshot: CartSnapshot) -> None: ...

class ValkeyCartBackend:
    def __init__(self, redis: Redis, prefix: str = "solex:cart:"):
        self.redis = redis; self.prefix = prefix
    def _k(self, key): return f"{self.prefix}{key}"
    def load(self, key):
        raw = self.redis.get(self._k(key))
        if not raw:
            return CartSnapshot(currency="USD", lines=[], subtotal_cents=0)
        data = json.loads(raw)
        return CartSnapshot(**data)
    def save(self, key, snap):
        self.redis.setex(self._k(key), 7 * 24 * 3600, json.dumps(snap.__dict__))

class CartService:
    def __init__(self, backend: CartBackend, catalog_get_product):
        self.backend = backend
        self.get_product = catalog_get_product

    def add(self, key, product_id: UUID, qty: int) -> CartSnapshot:
        snap = self.backend.load(key)
        product = self.get_product(product_id)
        if product is None:
            raise ValueError("unknown product")
        for line in snap.lines:
            if line["product_id"] == str(product_id):
                line["qty"] += qty
                break
        else:
            snap.lines.append(dict(
                product_id=str(product_id), sku=product.sku, name=product.name,
                image_path=product.image_path, qty=qty,
                price_cents=product.price_cents,
            ))
        self._retotal(snap)
        self.backend.save(key, snap)
        return snap

    def update_qty(self, key, product_id, qty):
        snap = self.backend.load(key)
        snap.lines = [l for l in snap.lines
                      if not (l["product_id"] == str(product_id) and qty == 0)]
        for line in snap.lines:
            if line["product_id"] == str(product_id):
                line["qty"] = qty
        self._retotal(snap)
        self.backend.save(key, snap)
        return snap

    def remove(self, key, product_id):
        return self.update_qty(key, product_id, 0)

    def _retotal(self, snap):
        snap.subtotal_cents = sum(l["qty"] * l["price_cents"] for l in snap.lines)
```

Unit tests use an in-memory `dict`-backed `CartBackend` for speed; no Valkey needed. Commit.

**Checkpoint — chunk 4 done.** Services for catalog + cart + inventory + tax/shipping stubs exist and are unit-tested. Catalog seed loads.

---

## Chunk 5: Storefront routes + templates

Goal: a visitor can open the site, browse `/shop`, view a product, add to cart, see the cart drawer update.

### Task 5.1 — Base template + nav

- [ ] **Create `solex/templates/base.html`** — Jinja shell with Tailwind output CSS link, Alpine import, nav, cart icon (Alpine-driven open/close), footer.

Skeleton:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex,nofollow">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{% block title %}Solex{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/output.css') }}">
</head>
<body class="bg-white text-stone-900" x-data="{cartOpen:false}">
  <header class="border-b border-stone-200">
    <nav class="mx-auto max-w-6xl flex items-center justify-between p-4">
      <a href="{{ url_for('storefront.home') }}" class="font-semibold">Solex</a>
      <ul class="flex gap-6 text-sm">
        <li><a href="{{ url_for('storefront.shop') }}">Shop</a></li>
        <li><a href="#">AO Scan</a></li>
        <li><a href="#">University</a></li>
      </ul>
      <button @click="cartOpen = true" class="text-sm">Cart (<span id="cart-count">0</span>)</button>
    </nav>
  </header>
  <main class="mx-auto max-w-6xl p-4">{% block main %}{% endblock %}</main>
  {% include "cart/_drawer.html" %}
  <script src="{{ url_for('static', filename='js/alpine_init.js') }}" defer></script>
  <script src="{{ url_for('static', filename='js/cart_drawer.js') }}" defer></script>
</body>
</html>
```

Commit.

### Task 5.2 — Storefront blueprint + routes

- [ ] Create `solex/routes/storefront.py`:

```python
from flask import Blueprint, render_template, abort
from solex.extensions import db
from solex.services.catalog import CatalogService

bp = Blueprint("storefront", __name__)

def _catalog():
    return CatalogService(db.session)

@bp.get("/")
def home():
    products = _catalog().list_products()[:4]
    return render_template("storefront/home.html", products=products)

@bp.get("/shop")
def shop():
    return render_template("storefront/shop.html",
                           products=_catalog().list_products(),
                           categories=_catalog().list_categories())

@bp.get("/shop/<slug>")
def shop_by_category(slug):
    products = _catalog().list_products(category_slug=slug)
    return render_template("storefront/shop.html",
                           products=products,
                           categories=_catalog().list_categories(),
                           active_slug=slug)

@bp.get("/products/<slug>")
def product_detail(slug):
    product = _catalog().get_product(slug)
    if product is None or not product.active:
        abort(404)
    return render_template("storefront/product_detail.html", product=product)
```

- [ ] **Register in `create_app`:**

```python
from solex.routes import api, storefront
app.register_blueprint(api.bp)
app.register_blueprint(storefront.bp)
```

- [ ] **Create templates** under `solex/templates/storefront/`: `home.html`, `shop.html`, `product_detail.html`. Minimal but functional — product cards with image, name, price, add-to-cart form. Not visually polished (that's Plan 4).

- [ ] **Write a route unit test:**

```python
# tests/unit/test_routes_storefront.py
def test_shop_lists_products(client, db_session, seed_catalog):
    resp = client.get("/shop")
    assert resp.status_code == 200
    assert b"AO Youth" in resp.data

def test_product_detail_by_slug(client, db_session, seed_catalog):
    resp = client.get("/products/ao-youth-30")
    assert resp.status_code == 200
    assert b"AO Youth" in resp.data

def test_product_detail_404_for_missing(client, db_session, seed_catalog):
    assert client.get("/products/nope").status_code == 404
```

Add the `seed_catalog` fixture to conftest (imports the YAML into the test DB once per session).

Commit.

### Task 5.3 — Cart blueprint + drawer

- [ ] Create `solex/routes/cart.py` with `POST /cart/add`, `POST /cart/update`, `POST /cart/remove`, `GET /cart`. Add-to-cart uses `CartService` + session key.
- [ ] Create `solex/templates/cart/_drawer.html` (Alpine-driven slide-over) and `solex/templates/cart/cart.html`.
- [ ] `solex/static/js/cart_drawer.js` — fetches `/cart.json` (add a JSON subroute), updates drawer contents on add events (dispatch a CustomEvent).

Commit.

**Checkpoint — chunk 5 done.** Site is browseable end-to-end, cart works, nothing paid yet.

---

## Chunk 6: Checkout + Square integration

Goal: guest can complete checkout against Square sandbox. Order persisted, payment captured, inventory decremented, confirmation email sent.

### Task 6.1 — Square client wrapper

**Files:**
- Create: `Solex/solex/services/square_client.py`
- Create: `Solex/tests/unit/test_services_square_client.py` (Square API mocked)

- [ ] Implement `SquareClient` with `create_order`, `create_payment`, `create_refund`, `verify_webhook_signature`. Wrap Square Python SDK; tenacity retry on 5xx.

Full code (abbreviated — caller pattern):

```python
# solex/services/square_client.py
from dataclasses import dataclass
from square.client import Client
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@dataclass
class SquareConfig:
    access_token: str
    environment: str
    location_id: str
    webhook_signature_key: str

class SquareError(Exception): ...
class SquareTransient(SquareError): ...
class SquareDeclined(SquareError): ...

class SquareClient:
    def __init__(self, cfg: SquareConfig):
        self.cfg = cfg
        self._client = Client(access_token=cfg.access_token, environment=cfg.environment)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4),
           retry=retry_if_exception_type(SquareTransient))
    def create_order(self, line_items, taxes_cents=0, shipping_cents=0, reference_id=None):
        body = {
            "idempotency_key": reference_id or _gen_idem_key(),
            "order": {
                "location_id": self.cfg.location_id,
                "line_items": line_items,
                "taxes": [{"name": "Tax", "type": "ADDITIVE",
                           "applied_money": {"amount": taxes_cents, "currency": "USD"}}] if taxes_cents else [],
                "service_charges": [{"name": "Shipping", "calculation_phase": "TOTAL_PHASE",
                                     "amount_money": {"amount": shipping_cents, "currency": "USD"}}] if shipping_cents else [],
                "reference_id": reference_id,
            },
        }
        result = self._client.orders.create_order(body=body)
        self._raise(result)
        return result.body["order"]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4),
           retry=retry_if_exception_type(SquareTransient))
    def create_payment(self, source_id, amount_cents, order_id, reference_id=None):
        result = self._client.payments.create_payment(body={
            "source_id": source_id,
            "idempotency_key": reference_id or _gen_idem_key(),
            "amount_money": {"amount": amount_cents, "currency": "USD"},
            "location_id": self.cfg.location_id,
            "order_id": order_id,
        })
        self._raise(result)
        return result.body["payment"]

    def verify_webhook_signature(self, url: str, body: bytes, header_sig: str) -> bool:
        import hmac, hashlib, base64
        expected = base64.b64encode(
            hmac.new(self.cfg.webhook_signature_key.encode(),
                     (url + body.decode()).encode(), hashlib.sha256).digest()
        ).decode()
        return hmac.compare_digest(expected, header_sig or "")

    def _raise(self, result):
        if result.is_success(): return
        code = result.status_code
        if 500 <= code < 600:
            raise SquareTransient(result.errors)
        if code == 402 or any(e.get("category") == "PAYMENT_METHOD_ERROR" for e in (result.errors or [])):
            raise SquareDeclined(result.errors)
        raise SquareError(result.errors)

def _gen_idem_key():
    import uuid; return str(uuid.uuid4())
```

Unit test mocks `Client.orders.create_order` via `pytest-mock`, asserts retry behavior on synthetic 500. Commit.

### Task 6.2 — CheckoutService

**Files:**
- Create: `Solex/solex/services/checkout.py`
- Create: `Solex/tests/unit/test_services_checkout.py` (Square mocked)

- [ ] Implement `place_order(cart_snapshot, customer_info, address, payment_token, *, autoship_source=None, scenario_tag=None, placed_at=None) -> Order` per the spec §6.1 flow. Use the stubs for tax/shipping. Wrap the whole DB transaction in `session.begin()`. On Square failure, no `Order` persists; re-raise. TDD with mocked `SquareClient`. Commit.

### Task 6.3 — Checkout routes + template

- [ ] Create `solex/routes/checkout.py`:
  - `GET /checkout` — renders form, passes Square Web Payments SDK app ID + location ID.
  - `POST /checkout/submit` — JSON endpoint receiving `{cart_key, customer, address, payment_token}`. Calls `CheckoutService.place_order()`. Returns `{order_token}` on success, error codes on failure.
  - `GET /order/<public_token>` — confirmation page.

- [ ] Create `solex/templates/checkout/checkout.html` with Web Payments SDK card element and `solex/static/js/checkout.js` that tokenizes and POSTs.

- [ ] Create `solex/templates/checkout/order_confirmation.html`.

- [ ] Integration test stubs with Square mocked go in Task 6.2; the real sandbox call is in Task 8.1.

Commit.

### Task 6.4 — Email service + order confirmation email

- [ ] Create `solex/services/email.py` (wraps `flask-mail`, logs to `EmailLog`, Jinja templates).
- [ ] Create `solex/templates/emails/order_confirmation.{html,txt}`.
- [ ] Hook into `CheckoutService.place_order` — enqueue-or-send after commit. For Plan 1, send synchronously (no RQ queue config yet for jobs; worker container is up but idle).
- [ ] Verify MailHog receives the email in dev: open `http://localhost:8027`, run through a checkout in `/checkout`, see the email.

Commit: `solex: checkout end-to-end via Square sandbox (mocked in unit; sandbox-live integration covered in Chunk 8)`.

**Checkpoint — chunk 6 done.** Guest checkout end-to-end against sandbox. You can place an order from the browser.

---

## Chunk 7: Webhooks

Goal: Square sandbox webhooks arrive at `/api/webhooks/square`, are verified, dispatched, deduped, and — in the orphan-payment case — trigger an automatic refund per spec §4.10.

### Task 7.1 — Webhook handler service

- [ ] Create `solex/services/webhooks.py`:
  - `handle(square_event_id, event_type, body, signature, url)` — verify sig → dedupe via `SquareWebhookEvent.square_event_id` unique constraint → dispatch → mark `processed_at`.
  - `_handle_payment_updated(payload)` — look up `Order` by `square_payment_id`. If not found, call `RefundsService.issue_refund_by_payment_id(payment_id, reason="orphan-recovery")`.
  - `_handle_refund_updated(payload)` — update `Refund.square_refund_id` if still unset; mark as settled.
  - `_handle_order_updated(payload)` — no-op for now (Plan 2 uses this for admin visibility).

Unit tests mock `SquareClient`. Commit.

### Task 7.2 — RefundsService (minimal — orphan recovery only)

- [ ] Create `solex/services/refunds.py` with `issue_refund(order, amount_cents, reason)` and `issue_refund_by_payment_id(payment_id, reason)`. Payment-id variant calls Square directly (no local `Order`), creates a `Refund` row linked to a synthetic `Order` stub? **No** — per spec, we do not synthesize. Instead: create `Refund` with `order_id=None` allowed via nullable FK in a follow-up migration. Simpler: introduce a dedicated `OrphanRefund` table.
  - **Decision for Plan 1:** go with nullable `Refund.order_id`. Add Alembic migration `0002_refund_order_nullable.py`.
- [ ] Tests. Commit.

### Task 7.3 — Webhook route

- [ ] Add `POST /api/webhooks/square` to `solex/routes/api.py`:

```python
@bp.post("/api/webhooks/square")
@csrf.exempt
@limiter.limit("120 per minute")
def square_webhook():
    body = request.get_data()
    sig = request.headers.get("X-Square-HmacSha256-Signature", "")
    url = request.url
    try:
        webhooks_service().handle(
            square_event_id=request.json["event_id"],
            event_type=request.json["type"],
            body=body, signature=sig, url=url,
        )
    except BadSignature:
        abort(401)
    return "", 204
```

Integration test posts a captured sandbox webhook payload + signature. Commit.

**Checkpoint — chunk 7 done.** Webhook path is real. Sandbox-live test in Chunk 8.

---

## Chunk 8: Auth (minimum for admin login) + sandbox-live integration + smoke + runbook

### Task 8.1 — Sandbox-live integration test

**Files:**
- Create: `Solex/tests/integration/test_checkout_sandbox.py`

- [ ] Write a test marked `@pytest.mark.sandbox_live` that:
  1. Imports the seed catalog into `solex_test`.
  2. Builds a synthetic cart with 1 line item.
  3. Calls `CheckoutService.place_order` with Square's sandbox test card token `cnon:card-nonce-ok`.
  4. Asserts the resulting `Order.status == "paid"` and `square_payment_id` is set.
  5. Asserts inventory decremented.
  6. Tears down by issuing a refund against the payment to keep sandbox clean (per "Square sandbox is shared" memory — do NOT wipe, but do clean up what you created).

Run:

```bash
./devops/scripts/dev.sh test -m sandbox_live tests/integration/test_checkout_sandbox.py -v
```

Expect PASS against the real sandbox.

### Task 8.2 — Admin auth (login + logout only; surfaces deferred to Plan 2)

- [ ] Implement `solex/services/auth.py` (password check + magic-link request/consume), `solex/routes/admin_auth.py` (`/admin/login` GET+POST, `/admin/magic/<token>`, `/admin/logout`), and `account_auth.py` (same shape but customer-flavored, routes only — no account surface yet).
- [ ] Write a seed admin user (`dev@solex.local` / `password` — only in DevConfig, never Prod). Add a `python3 -m solex.cli admin create-seed-user` CLI.
- [ ] Tests + commit.

### Task 8.3 — /health expansion + smoke boot test

- [ ] Extend `/health` to check db connectivity and valkey ping; return `{"ok": true, "db": true, "valkey": true, "version": "0.1.0"}`.
- [ ] `tests/smoke/test_compose_boot.py`:

```python
import pytest, requests, time

@pytest.mark.smoke
def test_site_renders_and_health_is_green():
    # Assumes `./devops/scripts/dev.sh up` is running.
    for _ in range(20):
        try:
            r = requests.get("http://localhost:5003/health", timeout=1)
            if r.ok: break
        except Exception: pass
        time.sleep(1)
    else:
        pytest.fail("health never came up")
    r = requests.get("http://localhost:5003/health").json()
    assert r["ok"] and r["db"] and r["valkey"]
    assert "Solex" in requests.get("http://localhost:5003/shop").text
```

Run, commit.

### Task 8.4 — Runbook

- [ ] Append to `Solex/README.md`:
  - `dev.sh up | down | logs | shell | test`
  - Reseed: `docker compose exec web python3 -m solex.cli catalog import`
  - Seed admin: `docker compose exec web python3 -m solex.cli admin create-seed-user`
  - Alembic: `docker compose exec web alembic upgrade head` / `alembic revision --autogenerate -m "..."`
  - Square sandbox cards: `cnon:card-nonce-ok` (success), `cnon:card-nonce-declined` (declined).
  - MailHog: `http://localhost:8027`
  - Webhook tunneling for dev: note that Square sandbox webhook delivery requires a public URL; use `cloudflared tunnel run` against `localhost:5003` or skip webhook testing in dev (sandbox-live integration test covers it in CI).

Commit.

### Task 8.5 — Final plan-level smoke

- [ ] Run the full test matrix:

```bash
./devops/scripts/dev.sh test tests/unit -v
./devops/scripts/dev.sh test tests/integration -v -m "not sandbox_live"
./devops/scripts/dev.sh test tests/integration -v -m sandbox_live
./devops/scripts/dev.sh test tests/smoke -v
```

All four green = Plan 1 done.

- [ ] Summarize commits:

```bash
git log --oneline plan/solex-foundation ^main
```

- [ ] Open a PR titled `feat: solex foundation — browseable site + guest checkout + Square sandbox` with Plan 1's scope checklist in the body, linking the spec and Linear issue.

---

## Plan 1 — Done criteria (repeat)

All of these must be green before Plan 2 starts:

- [ ] `./devops/scripts/dev.sh up` boots the stack cleanly
- [ ] `/health` returns all green
- [ ] Catalog import loads 5 products + 4 categories
- [ ] `/shop`, `/products/<slug>`, `/cart` all render
- [ ] Guest checkout against Square sandbox places an `Order`, captures payment, decrements inventory, emails a confirmation (visible in MailHog)
- [ ] `/api/webhooks/square` verifies signatures and orphan-recovers missing orders
- [ ] Admin can log in at `/admin/login` (surfaces past login are Plan 2 scope)
- [ ] `pytest tests/unit tests/integration tests/smoke` green
- [ ] `tests/integration -m sandbox_live` green
- [ ] No uncommitted changes; commits reference GRO-XXX

---

## What's next (for context, not execution)

- **Plan 2 — Operations:** admin UI (catalog/orders/inventory/customers/subscriptions), customer account self-service, full refunds + returns flow, autoship subscriptions + scheduled charging, cart abandonment emails, search, SYNC_CATALOG_TO_SQUARE wiring.
- **Plan 3 — Scenario runner:** `/admin/lab` + 9 scenarios (normal day, after-hours, round-amount, high-value, autoship cohort, bulk reseller, refund wave, shrink event, cart abandonment) + ScenarioRun model + RQ execution.
- **Plan 4 — Visual fidelity:** Tailwind theme matching solexglobal.com, real imagery, full 25-SKU catalog, brand typography, hero sections, polished checkout.

Each of those gets its own spec ↔ plan cycle when its turn comes.
