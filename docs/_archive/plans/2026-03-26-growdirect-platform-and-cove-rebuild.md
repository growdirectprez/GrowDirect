# GrowDirect Platform & Cove Rebuild Implementation Plan

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create GrowDirect platform standards and shared factory skills, then rebuild Cove's frontend on the real framework while keeping all backend services.

**Architecture:** GrowDirect-level CLAUDE.md + shared factory skills define how every app is built. Cove keeps its models/services/data, throws away all templates/routes/CSS, rebuilds on Tailwind+PostCSS with component classes. Docker compose follows the same pattern as Canary — identical startup, health checks, service structure.

**Tech Stack:** Python 3.12, Flask 3+, SQLAlchemy 2.0, PostgreSQL 17 + pgvector, Valkey 8, Tailwind 3.x + PostCSS, Alpine.js 3.x, Leaflet.js (all via npm), Gunicorn, Docker Compose, pytest

**Spec:** `docs/superpowers/specs/2026-03-26-growdirect-platform-and-cove-rebuild-design.md`

---

## Chunk 1: GrowDirect Platform Layer

### Task 1: Create GrowDirect CLAUDE.md

**Files:**
- Create: `~/GrowDirect/CLAUDE.md`

- [ ] **Step 1: Write the platform CLAUDE.md**

This is the master standards document. Every app's CLAUDE.md references it. Contents:

```markdown
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
    # Ports: 5432 internal, host port varies per app

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

  # App-specific services below this line
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
```

- [ ] **Step 2: Commit**

```bash
cd ~/GrowDirect
git add CLAUDE.md
git commit -m "feat: create GrowDirect platform standards (GRO-365)"
```

---

### Task 2: Create shared factory skills

**Files:**
- Create: `~/GrowDirect/.claude/skills/factory-startup.md`
- Create: `~/GrowDirect/.claude/skills/factory-close.md`
- Create: `~/GrowDirect/.claude/skills/factory-blueprint.md`
- Create: `~/GrowDirect/.claude/skills/factory-tdd.md`
- Create: `~/GrowDirect/.claude/skills/factory-assembly.md`
- Create: `~/GrowDirect/.claude/skills/factory-verify.md`
- Create: `~/GrowDirect/.claude/skills/factory-qa.md`
- Create: `~/GrowDirect/.claude/skills/factory-ship.md`

These skills are extracted from the existing `canary-*` skills. Each shared skill contains the universal process; app-specific skills become thin wrappers.

- [ ] **Step 1: Read existing Canary factory skills**

Read every `canary-*` skill file in `~/GrowDirect/Canary/.claude/skills/` to understand the current factory process. Note what is universal vs Canary-specific.

- [ ] **Step 2: Read existing Cove factory skills**

Read every `cove-*` skill file in `~/GrowDirect/Cove/.claude/skills/` to compare. Note duplicated patterns.

- [ ] **Step 3: Write factory-startup skill**

```markdown
# factory-startup

## Platform Context Load

1. Read `~/GrowDirect/CLAUDE.md` (platform standards)
2. Read the current app's `CLAUDE.md` (app-specific domain context)
3. Load last session context if available
4. Confirm: "Loaded GrowDirect platform standards + [app name] context."
```

- [ ] **Step 4: Write factory-close skill**

```markdown
# factory-close

## Session Close

1. Summarize what was completed this session (files changed, tests written, features delivered)
2. List any pending items or blockers
3. Note any issues found outside current scope (create Linear issues if needed)
4. Update app agent's knowledge graph with session learnings
5. Output: "Session summary: [completed] | Pending: [items] | New issues: [items]"
```

- [ ] **Step 5: Write factory-blueprint skill**

```markdown
# factory-blueprint

## Feature Specification

Before writing any code, answer these questions:

1. **Linear issue:** What GRO issue is this? (No issue = no work)
2. **What:** One sentence describing the deliverable
3. **Files:** List every file that will be created or modified
4. **Models:** Any new tables or columns? (Follow platform model standards)
5. **Routes:** What URLs? What HTTP methods? What responses?
6. **Tests:** What test files? What scenarios?
7. **Dependencies:** What existing services/models does this touch?

Output the blueprint as a checklist. Get user confirmation before proceeding to TDD.
```

- [ ] **Step 6: Write factory-tdd skill**

```markdown
# factory-tdd

## Test-First Development

1. Write the test file FIRST — one test per behavior
2. Each test follows: Arrange (setup) → Act (call) → Assert (verify)
3. Run the test — it MUST fail (if it passes, the test is wrong or the feature already exists)
4. Use pytest fixtures from conftest.py (app, client, authenticated_client, db_session)
5. Test naming: `test_<what>_<condition>_<expected>` (e.g., `test_login_valid_email_redirects_to_dashboard`)
6. Cover: happy path, validation errors, auth required, not found, edge cases

Do NOT proceed to assembly until all tests are written and failing for the right reasons.
```

- [ ] **Step 7: Write factory-assembly skill**

```markdown
# factory-assembly

## Implementation

1. Pick one failing test
2. Write the MINIMAL code to make it pass — no extra features, no premature abstraction
3. Run the test — it must pass
4. Pick the next failing test, repeat
5. After all tests pass, run the full test suite: `pytest -v`
6. If any test breaks, fix before proceeding

Assembly is done when all tests from the TDD phase are green.
```

- [ ] **Step 8: Write factory-verify skill**

```markdown
# factory-verify

## Verification

1. Run full test suite: `pytest -v` — all must pass
2. Check for regressions: did any existing tests break?
3. Verify integration: do the new routes work with existing services?
4. Check database: run `alembic upgrade head` if migrations were added
5. Check Docker: does `docker compose up` still work?
6. Manual smoke test: hit the new URLs, verify responses

Report: "[N] tests pass, [N] new, [N] existing, no regressions"
```

- [ ] **Step 9: Write factory-qa skill**

```markdown
# factory-qa

## Quality Assurance

1. **Security:** No SQL injection, no XSS, CSRF tokens on all forms, @login_required on protected routes
2. **Code quality:** No dead code, no commented-out code, no TODO without a Linear issue
3. **Standards compliance:** Models use Mapped[], UUIDs, timestamps. Config from env. No hardcoded secrets.
4. **CSS compliance:** Templates use component classes from <appname>.css, no raw utility soup
5. **Test coverage:** Every route has at least one happy-path and one error-path test
6. **Davis-Stirling (Cove only):** Secret ballot separation, quorum rules, notice requirements

Fix any issues found before proceeding to ship.
```

- [ ] **Step 10: Write factory-ship skill**

```markdown
# factory-ship

## Deployment Preparation

1. Run full test suite one final time: `pytest -v`
2. Check migrations: `alembic upgrade head` succeeds cleanly
3. Check Docker build: `docker compose build` succeeds
4. Run smoke test against Docker stack
5. Review all commits — are messages clear and linked to GRO issue?
6. Update changelog if one exists
7. Tag the release if appropriate

Ship is done when the code is ready for production deployment.
```

- [ ] **Step 11: Commit**

```bash
cd ~/GrowDirect
git add .claude/skills/
git commit -m "feat: create shared factory skills (GRO-365)"
```

---

### Task 3: Create platform standards docs

**Files:**
- Create: `~/GrowDirect/docs/standards/tech-stack.md`
- Create: `~/GrowDirect/docs/standards/coding-standards.md`
- Create: `~/GrowDirect/docs/standards/css-framework.md`
- Create: `~/GrowDirect/docs/standards/factory-process.md`
- Create: `~/GrowDirect/docs/standards/docker-standard.md`

- [ ] **Step 1: Write tech-stack.md**

Sections: Language & Runtime (Python 3.12), Web Framework (Flask 3+), ORM (SQLAlchemy 2.0), Database (PostgreSQL 17 + pgvector), Cache (Valkey 8), Frontend (Tailwind 3.x, Alpine.js 3.x, Leaflet.js), Server (Gunicorn), Containers (Docker Compose), Testing (pytest). Each with exact version pin and rationale.

- [ ] **Step 2: Write coding-standards.md**

Sections: Model Pattern (Mapped[] example with UUID PK, timestamps, audit mixin), Service Pattern (stateless functions, db session from caller, return domain objects), Route Pattern (thin handlers that call services, form validation, flash messages), Test Pattern (conftest fixtures, three layers with examples), Import Order (stdlib, third-party, local), Error Handling (service raises, route catches and flashes).

- [ ] **Step 3: Write css-framework.md**

Sections: Build Pipeline (PostCSS + Tailwind + autoprefixer), File Structure (main.css entry, appname.css components, dist/ output), Component Class Convention (when to create one: pattern repeats > 2x), How to Add Components (write @apply class, rebuild, use in template), Template Rules (use component classes, never raw utility chains for defined patterns).

- [ ] **Step 4: Write factory-process.md**

Sections: Overview (six stages in order, no skipping), Blueprint (what it produces: checklist of files/routes/tests), TDD (what it produces: failing test files), Assembly (what it produces: passing code), Verify (what it produces: full green test suite), QA (what it produces: security/quality sign-off), Ship (what it produces: deployable artifact). Each with a concrete example.

- [ ] **Step 5: Write docker-standard.md**

Sections: Compose Template (exact YAML structure every app follows), Dockerfile Template (two-stage build, non-root user), Health Check Patterns (HTTP endpoint, CLI ping, pg_isready), Port Allocation Table, Container Naming (`<appname>_localhost_<service>`), Startup Order (postgres → valkey → flask), Volume Mounts (dev: source mount with --reload, prod: COPY at build).

- [ ] **Step 5b: Create post-mortems directory**

```bash
mkdir -p ~/GrowDirect/docs/post-mortems
echo "# Post-Mortems\n\nAgent writes post-mortems after ship cycles. Jeffe reviews and promotes learnings to platform standards." > ~/GrowDirect/docs/post-mortems/README.md
```

- [ ] **Step 6: Commit**

```bash
cd ~/GrowDirect
git add docs/standards/
git commit -m "feat: create platform standards documentation (GRO-365)"
```

---

### Task 4: Update Cove CLAUDE.md to reference parent

**Files:**
- Modify: `~/GrowDirect/Cove/CLAUDE.md`

- [ ] **Step 1: Read current Cove CLAUDE.md**

Read `~/GrowDirect/Cove/CLAUDE.md` in full.

- [ ] **Step 2: Add parent reference at top**

Add to the very top of Cove's CLAUDE.md:

```markdown
> **Platform parent:** Read `~/GrowDirect/CLAUDE.md` first. This file adds Cove-specific domain context on top of GrowDirect platform standards.
```

- [ ] **Step 3: Remove any content that duplicates platform standards**

Anything already covered in the parent CLAUDE.md (tech stack, model standards, test standards, hard rules) gets removed from Cove's CLAUDE.md. Keep only Cove-specific domain knowledge (Davis-Stirling, APN-as-identity, secret ballot separation, etc.)

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Cove
git add CLAUDE.md
git commit -m "refactor: reference GrowDirect platform parent in Cove CLAUDE.md (GRO-365)"
```

---

### Task 5: Make Cove factory skills thin wrappers

**Files:**
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-startup.md`
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-close.md`
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-blueprint.md`
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-tdd.md`
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-assembly.md`
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-verify.md`
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-qa.md`
- Modify: `~/GrowDirect/Cove/.claude/skills/cove-ship.md`

- [ ] **Step 1: Read all current cove-* skills**

Read each skill to understand what's Cove-specific vs what's generic factory process.

- [ ] **Step 2: Rewrite each cove-* skill as thin wrapper**

Each skill becomes:
```markdown
# cove-<stage>

> Delegates to: `~/GrowDirect/.claude/skills/factory-<stage>.md`

## Cove-specific context for this stage:
[Only the Cove-domain additions — Davis-Stirling checks, APN validation, etc.]
```

- [ ] **Step 3: Commit**

```bash
cd ~/GrowDirect/Cove
git add .claude/skills/
git commit -m "refactor: make cove skills thin wrappers over factory skills (GRO-365)"
```

---

## Chunk 2: Cove CSS Framework & Build Pipeline

### Task 6: Set up Tailwind + PostCSS build pipeline

**Files:**
- Create: `~/GrowDirect/Cove/package.json`
- Create: `~/GrowDirect/Cove/postcss.config.js`
- Create: `~/GrowDirect/Cove/tailwind.config.js`
- Create: `~/GrowDirect/Cove/static/css/main.css`
- Create: `~/GrowDirect/Cove/static/css/cove.css`

- [ ] **Step 1: Write package.json**

```json
{
  "name": "cove",
  "private": true,
  "scripts": {
    "dev": "postcss static/css/main.css -o static/css/dist/main.css --watch",
    "build": "NODE_ENV=production postcss static/css/main.css -o static/css/dist/main.css"
  },
  "devDependencies": {
    "tailwindcss": "^3.4",
    "postcss": "^8.4",
    "postcss-cli": "^11.0",
    "postcss-import": "^16.0",
    "autoprefixer": "^10.4"
  },
  "dependencies": {
    "alpinejs": "^3.14",
    "leaflet": "^1.9"
  }
}
```

- [ ] **Step 2: Write postcss.config.js**

```js
module.exports = {
  plugins: {
    'postcss-import': {},
    tailwindcss: {},
    autoprefixer: {},
  }
}
```

- [ ] **Step 3: Write tailwind.config.js**

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './cove/**/templates/**/*.html',
    './templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        cove: {
          50:  '#f0f7ff',
          100: '#e0effe',
          200: '#b9dffe',
          300: '#7cc5fd',
          400: '#36a9fa',
          500: '#0c8eeb',
          600: '#0070c9',
          700: '#0059a3',
          800: '#054b86',
          900: '#0a3f6f',
        },
      },
    },
  },
  plugins: [],
}
```

- [ ] **Step 4: Write main.css entry point**

```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import './cove.css';
@import 'tailwindcss/utilities';
```

- [ ] **Step 5: Write cove.css with component classes**

Create `static/css/cove.css` with all component classes from the spec:

```css
/* Layout */
.cove-page { @apply min-h-screen bg-gray-50; }
.cove-sidebar { @apply w-64 bg-white border-r border-gray-200 min-h-screen; }
.cove-content { @apply flex-1 p-6; }

/* Cards */
.cove-card { @apply bg-white rounded-lg shadow-sm border border-gray-200; }
.cove-card-header { @apply px-6 py-4 border-b border-gray-200; }
.cove-card-body { @apply px-6 py-4; }

/* Forms */
.cove-form { @apply space-y-4; }
.cove-input { @apply w-full rounded-md border-gray-300 shadow-sm focus:border-cove-500 focus:ring-cove-500; }
.cove-select { @apply w-full rounded-md border-gray-300 shadow-sm focus:border-cove-500 focus:ring-cove-500; }
.cove-checkbox { @apply rounded border-gray-300 text-cove-600 focus:ring-cove-500; }
.cove-error { @apply text-sm text-red-600 mt-1; }
.cove-error-inline { @apply text-sm text-red-600 mt-1; }
.cove-label { @apply block text-sm font-medium text-gray-700 mb-1; }

/* Tables */
.cove-table { @apply min-w-full divide-y divide-gray-200; }
.cove-th { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50; }
.cove-td { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900; }

/* Navigation */
.cove-nav { @apply flex flex-col space-y-1 px-3 py-4; }
.cove-nav-item { @apply px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-100 hover:text-gray-900; }
.cove-nav-active { @apply px-3 py-2 text-sm font-medium text-cove-700 bg-cove-50 rounded-md; }

/* Buttons */
.cove-btn { @apply inline-flex items-center px-4 py-2 text-sm font-medium rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2; }
.cove-btn-primary { @apply bg-cove-600 text-white hover:bg-cove-700 focus:ring-cove-500; }
.cove-btn-secondary { @apply bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 focus:ring-cove-500; }
.cove-btn-danger { @apply bg-red-600 text-white hover:bg-red-700 focus:ring-red-500; }

/* Modals */
.cove-modal { @apply fixed inset-0 z-50 flex items-center justify-center; }
.cove-modal-overlay { @apply fixed inset-0 bg-black bg-opacity-50; }
.cove-modal-content { @apply relative bg-white rounded-lg shadow-xl max-w-lg w-full mx-4 p-6; }

/* Badges / Status */
.cove-badge { @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium; }
.cove-status-active { @apply bg-green-100 text-green-800; }
.cove-status-pending { @apply bg-yellow-100 text-yellow-800; }
.cove-status-closed { @apply bg-gray-100 text-gray-800; }
.cove-status-draft { @apply bg-blue-100 text-blue-800; }

/* Maps */
.cove-map-container { @apply w-full h-96 rounded-lg border border-gray-200 overflow-hidden; }
.cove-map-overlay { @apply absolute top-2 right-2 z-[1000] bg-white rounded-lg shadow-md p-2; }
.cove-parcel-popup { @apply text-sm; }

/* Voting */
.cove-ballot { @apply bg-white rounded-lg shadow-sm border-2 border-cove-200 p-6; }
.cove-proposal-card { @apply bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow; }
.cove-vote-btn { @apply w-full py-3 text-center font-medium rounded-md border-2 transition-colors; }

/* Documents */
.cove-doc-card { @apply bg-white rounded-lg shadow-sm border border-gray-200 p-4; }
.cove-doc-preview { @apply bg-gray-50 rounded-lg border border-gray-200 p-4 max-h-96 overflow-y-auto; }
```

- [ ] **Step 6: Install npm dependencies and build**

```bash
cd ~/GrowDirect/Cove
npm install
mkdir -p static/css/dist
npm run build
```

- [ ] **Step 7: Verify build output exists**

```bash
ls -la ~/GrowDirect/Cove/static/css/dist/main.css
```

Expected: file exists with reasonable size (Tailwind base + component classes).

- [ ] **Step 8: Add node_modules and dist to .gitignore**

Ensure `~/GrowDirect/Cove/.gitignore` includes:
```
node_modules/
static/css/dist/
```

- [ ] **Step 9: Commit**

```bash
cd ~/GrowDirect/Cove
git add package.json postcss.config.js tailwind.config.js static/css/main.css static/css/cove.css .gitignore
git commit -m "feat: add Tailwind + PostCSS build pipeline with cove.css component classes (GRO-365)"
```

---

## Chunk 3: Cove Infrastructure — Config, Extensions, Docker

### Task 6b: Adapt Cove config.py and extensions.py to platform standard

**Files:**
- Modify: `~/GrowDirect/Cove/cove/config.py`
- Modify: `~/GrowDirect/Cove/cove/extensions.py`

- [ ] **Step 1: Read current config.py and extensions.py**

```bash
cat ~/GrowDirect/Cove/cove/config.py
cat ~/GrowDirect/Cove/cove/extensions.py
```

- [ ] **Step 2: Adapt config.py to platform pattern**

Restructure to match the platform config standard from `~/GrowDirect/CLAUDE.md`:
- BaseConfig with `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `SQLALCHEMY_ENGINE_OPTIONS` (pool_pre_ping, pool_recycle), `SESSION_TYPE = "redis"`, `WTF_CSRF_ENABLED = True`, `MAX_CONTENT_LENGTH`
- DevConfig, TestConfig, StagingConfig, ProdConfig subclasses
- All secrets from environment variables, no hardcoded values
- Add `VALKEY_URL` config: `os.environ.get("VALKEY_URL", "redis://localhost:6380/0")`

- [ ] **Step 3: Adapt extensions.py to add Valkey session config**

Add Flask-Session with Valkey backend:
```python
from flask_session import Session
sess = Session()
```

In the app factory, initialize: `sess.init_app(app)` after setting `SESSION_REDIS` from `VALKEY_URL`.

- [ ] **Step 4: Add flask-session to requirements.txt**

```
flask-session>=0.5
redis>=5.0  # Valkey is Redis-compatible
```

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Cove
git add cove/config.py cove/extensions.py requirements.txt
git commit -m "refactor: adapt config and extensions to GrowDirect platform standard (GRO-365)"
```

---

### Task 7: Rebuild Cove Docker compose to match Canary pattern

**Files:**
- Create: `~/GrowDirect/Cove/Dockerfile` (at project root, matching Canary pattern — move from devops/ if it exists there)
- Modify: `~/GrowDirect/Cove/devops/docker-compose.yml`

- [ ] **Step 1: Read current Cove Dockerfile and move to project root**

```bash
# Check where it currently lives
ls ~/GrowDirect/Cove/Dockerfile ~/GrowDirect/Cove/devops/Dockerfile 2>/dev/null
# If it's in devops/, move to project root (matching Canary pattern)
mv ~/GrowDirect/Cove/devops/Dockerfile ~/GrowDirect/Cove/Dockerfile 2>/dev/null || true
```

Dockerfile lives at project root. Compose references it with `context: ../` and `dockerfile: Dockerfile`.

- [ ] **Step 2: Write Cove Dockerfile matching Canary pattern**

Two-stage build, Python 3.12-slim, non-root user, health check:

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim
WORKDIR /app

RUN groupadd -r cove && useradd -r -g cove cove

COPY --from=builder /install /usr/local
COPY . .

RUN chown -R cove:cove /app
USER cove

EXPOSE 5000

ENV FLASK_APP=wsgi:app
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python3 -c "from urllib.request import urlopen; urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "120", "wsgi:app"]
```

- [ ] **Step 3: Write Cove docker-compose.yml matching Canary pattern**

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg17
    container_name: cove_localhost_pg
    ports:
      - "5433:5432"
    environment:
      POSTGRES_USER: cove
      POSTGRES_PASSWORD: cove_dev_2026
      POSTGRES_DB: cove
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cove -d cove"]
      interval: 5s
      start_period: 10s
      retries: 10
    restart: unless-stopped

  valkey:
    image: valkey/valkey:8-alpine
    container_name: cove_localhost_valkey
    ports:
      - "6380:6379"
    volumes:
      - valkey_data:/data
    healthcheck:
      test: ["CMD", "valkey-cli", "ping"]
      interval: 5s
      retries: 5
    restart: unless-stopped

  flask:
    build:
      context: ../
      dockerfile: Dockerfile
    container_name: cove_localhost_flask
    command: gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 4 --timeout 120 --reload wsgi:app
    ports:
      - "5002:5000"
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: "1"
      SECRET_KEY: localhost-dev-key-not-for-production-use
      COVE_ENV: development
      DATABASE_URL: postgresql://cove:cove_dev_2026@postgres:5432/cove
      VALKEY_URL: redis://valkey:6379/0
    env_file:
      - ../.env
    depends_on:
      postgres:
        condition: service_healthy
      valkey:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "python3 -c \"from urllib.request import urlopen; urlopen('http://localhost:5000/health')\""]
      interval: 10s
      start_period: 20s
      retries: 5
    volumes:
      - ../cove:/app/cove
      - ../templates:/app/templates:ro
      - ../static:/app/static:ro
    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: cove_localhost_pgadmin
    ports:
      - "5051:5050"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@growdirect.app
      PGADMIN_DEFAULT_PASSWORD: cove_dev_2026
      PGADMIN_LISTEN_PORT: 5050
      PGADMIN_CONFIG_SERVER_MODE: "False"
      PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: "False"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
      - ./pgadmin/servers.json:/pgadmin4/servers.json:ro
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "wget -q --spider http://localhost:5050/misc/ping || exit 1"]
      interval: 15s
      start_period: 30s
      retries: 3
    restart: unless-stopped

  mailhog:
    image: mailhog/mailhog:latest
    container_name: cove_localhost_mailhog
    ports:
      - "1026:1025"
      - "8026:8025"
    healthcheck:
      test: ["CMD-SHELL", "wget -q --spider http://localhost:8025 || exit 1"]
      interval: 10s
      retries: 3
    restart: unless-stopped

volumes:
  pg_data:
    name: cove_localhost_pg_data
  valkey_data:
    name: cove_localhost_valkey_data
  pgadmin_data:
    name: cove_localhost_pgadmin_data
```

- [ ] **Step 3b: Create pgAdmin servers.json**

```bash
mkdir -p ~/GrowDirect/Cove/devops/pgadmin
```

Create `~/GrowDirect/Cove/devops/pgadmin/servers.json`:
```json
{
  "Servers": {
    "1": {
      "Name": "Cove (localhost)",
      "Group": "GrowDirect",
      "Host": "postgres",
      "Port": 5432,
      "MaintenanceDB": "cove",
      "Username": "cove",
      "SSLMode": "prefer"
    }
  }
}
```

Access at `http://localhost:5051` — schemas and tables visible immediately.

- [ ] **Step 4: Add /health endpoint to Cove**

In `~/GrowDirect/Cove/cove/__init__.py` (the app factory), ensure there's a health check route:

```python
@app.route('/health')
def health():
    return {'status': 'ok'}, 200
```

- [ ] **Step 5: Test Docker compose starts cleanly**

```bash
cd ~/GrowDirect/Cove/devops
docker compose down -v
docker compose up -d --build
docker compose ps
```

Expected: all services healthy.

- [ ] **Step 6: Verify health check endpoint**

```bash
curl -s http://localhost:5002/health
```

Expected: `{"status": "ok"}`

- [ ] **Step 7: Commit**

```bash
cd ~/GrowDirect/Cove
git add Dockerfile devops/docker-compose.yml cove/__init__.py
git commit -m "feat: rebuild Docker compose to match Canary twin pattern (GRO-365)"
```

---

## Chunk 4: Cove Frontend Rebuild — Catalogue and Delete

### Task 8: Catalogue current URLs

**Files:**
- Create: `~/GrowDirect/Cove/docs/url-inventory.md`

- [ ] **Step 1: Generate URL inventory from routes**

Create `docs/url-inventory.md` with every current route:

| Method | URL | Function | Blueprint |
|--------|-----|----------|-----------|
| GET | `/` | landing | public |
| GET | `/privacy` | privacy | public |
| GET | `/terms` | terms | public |
| GET,POST | `/auth/login` | login | auth |
| GET | `/auth/verify/<token>` | verify | auth |
| GET | `/auth/logout` | logout | auth |
| GET | `/member/dashboard` | dashboard | member |
| GET | `/member/directory` | directory | member |
| GET,POST | `/member/profile` | profile | member |
| GET | `/member/uploads/avatars/<filename>` | serve_avatar | member |
| GET,POST | `/member/accept-privacy` | accept_privacy | member |
| GET,POST | `/member/onboarding` | onboarding | member |
| GET | `/member/notifications` | notifications | member |
| POST | `/member/notifications/<id>/read` | mark_notification_read | member |
| POST | `/member/notifications/read-all` | mark_all_notifications_read | member |
| GET | `/vote/` | proposals | governance |
| GET,POST | `/vote/create` | create_proposal | governance |
| GET | `/vote/<id>` | proposal_detail | governance |
| POST | `/vote/<id>/transition` | transition | governance |
| GET | `/vote/<id>/ballot` | ballot_form | governance |
| POST | `/vote/<id>/ballot` | cast_vote | governance |
| GET | `/vote/<id>/results` | results | governance |
| POST | `/vote/<id>/certify` | certify | governance |
| GET | `/vote/election/` | elections | election |
| GET,POST | `/vote/election/create` | create | election |
| GET | `/vote/election/<id>` | detail | election |
| GET,POST | `/vote/election/<id>/candidates/add` | nominate | election |
| POST | `/vote/election/<id>/candidates/<cid>/withdraw` | withdraw | election |
| POST | `/vote/election/<id>/acclamation` | acclamation | election |
| GET | `/vote/election/<id>/ballot` | ballot | election |
| POST | `/vote/election/<id>/ballot` | cast_ballot | election |
| GET | `/vote/election/<id>/results` | results | election |
| POST | `/vote/election/<id>/certify` | certify | election |
| GET | `/proceedings/` | index | proceeding |
| GET,POST | `/proceedings/create` | create | proceeding |
| GET | `/proceedings/<id>` | detail | proceeding |
| POST | `/proceedings/<id>/status` | update_status | proceeding |
| GET,POST | `/proceedings/<id>/add-entry` | add_entry | proceeding |
| GET | `/proceedings/<id>/evidence` | evidence | proceeding |
| GET | `/vault/` | index | vault |
| GET,POST | `/vault/upload` | upload | vault |
| GET | `/vault/<id>` | document | vault |
| GET | `/vault/<id>/download` | download_latest | vault |
| GET | `/vault/<id>/download/<vid>` | download_version | vault |
| POST | `/vault/<id>/version` | upload_version | vault |
| GET | `/board/` | dashboard | board |
| GET | `/board/members` | members | board |
| GET | `/board/diagrams` | diagrams | board |
| GET | `/board/parcels` | parcels | board |
| POST | `/board/tags/create` | create_tag | board |
| POST | `/board/tags/<id>/assign` | assign_tag_bulk | board |
| POST | `/board/tags/<id>/remove` | remove_tag_bulk | board |
| GET,POST | `/board/bulletin` | send_bulletin | board |
| GET | `/board/boundaries` | boundaries | board |
| POST | `/board/boundaries/parse` | parse_boundary | board |
| GET | `/treasury/` | index | treasury |
| GET | `/treasury/assessments` | assessments | treasury |
| GET | `/treasury/budget` | budget | treasury |
| GET,POST | `/treasury/assessments/create` | create_assessment | treasury |
| GET,POST | `/treasury/assessments/<id>/pay` | record_payment | treasury |
| GET | `/parcels/map` | map | parcels |
| GET | `/parcels/api/geojson` | parcel_geojson | parcels |
| GET | `/parcels/api/layers/<filename>` | map_layer_file | parcels |
| GET | `/parcels/api/lot-h` | lot_h_geojson | parcels |
| GET | `/parcels/api/research/<apn>` | research_parcel_detail | parcels |
| GET | `/parcels/api/research/stats` | research_stats | parcels |
| GET | `/parcels/api/research/chart-data` | research_chart_data | parcels |
| GET | `/parcels/<id>` | parcel_detail | parcels |
| GET | `/meetings/` | index | meetings |
| GET,POST | `/meetings/create` | create | meetings |
| GET,POST | `/meetings/<id>/edit` | edit | meetings |
| GET | `/meetings/<id>` | detail | meetings |
| GET | `/meetings/<id>/calendar.ics` | download_ics | meetings |
| GET | `/meetings/<id>/attachment` | download_attachment | meetings |
| POST | `/meetings/<id>/cancel` | cancel | meetings |
| GET,POST | `/meetings/arc/apply` | arc_apply | meetings |
| GET | `/meetings/arc/<id>` | arc_status | meetings |
| GET | `/agent/transparency` | transparency_log | agent |
| POST | `/agent/api/ask` | ask_agent | agent |
| GET | `/agent/api/agenda` | meeting_agenda | agent |
| GET | `/agent/api/quorum` | quorum_status | agent |
| GET | `/archive/` | index | archive |
| GET | `/archive/timeline` | timeline | archive |
| GET | `/archive/chain` | chain | archive |
| GET | `/archive/bylaws` | bylaws | archive |
| GET | `/archive/catalog` | catalog | archive |
| GET | `/archive/doc/<category>/<slug>` | document | archive |
| GET | `/archive/data/<filename>` | data_file | archive |
| GET | `/archive/originals/<path>` | originals | archive |
| POST | `/archive/request/<path>` | request_original | archive |

- [ ] **Step 2: Commit inventory**

```bash
cd ~/GrowDirect/Cove
git add docs/url-inventory.md
git commit -m "docs: catalogue all Cove URLs before frontend rebuild (GRO-365)"
```

---

### Task 9: Delete all frontend files

**Files:**
- Delete: all `routes.py` files in every blueprint
- Delete: all `forms.py` files in every blueprint
- Delete: all template files in every blueprint's `templates/` directory
- Delete: `~/GrowDirect/Cove/templates/base.html`
- Delete: `~/GrowDirect/Cove/static/css/` (old CSS, not the new cove.css)

- [ ] **Step 1: Delete all template files**

```bash
cd ~/GrowDirect/Cove
find cove -name "templates" -type d -exec rm -rf {} + 2>/dev/null
rm -rf templates/
```

- [ ] **Step 2: Delete all routes.py files**

```bash
cd ~/GrowDirect/Cove
find cove -name "routes.py" -o -name "election_routes.py" -o -name "proceeding_routes.py" | xargs rm -f
```

- [ ] **Step 3: Delete all forms.py files**

```bash
cd ~/GrowDirect/Cove
find cove -name "forms.py" -o -name "election_forms.py" -o -name "proceeding_forms.py" | xargs rm -f
```

- [ ] **Step 4: Delete old CSS (preserve new cove.css and build pipeline)**

```bash
cd ~/GrowDirect/Cove
# Remove old CSS but keep new pipeline files
find static/css -type f ! -name "main.css" ! -name "cove.css" -delete 2>/dev/null
rm -rf static/css/dist/  # Will be regenerated by build
```

- [ ] **Step 5: Delete old package.json if separate from new one**

The new `package.json` was already created in Task 6. Remove any `run_dev.py` (the SQLite shortcut):

```bash
rm -f ~/GrowDirect/Cove/run_dev.py
```

- [ ] **Step 5b: Extract parcel service layer from routes before deletion**

The parcels blueprint has no `services.py` — all logic lives in routes.py. Before deleting routes, extract the data-serving logic into a new service file:

```bash
cd ~/GrowDirect/Cove
# Read the current parcels routes to identify what logic needs extracting
cat cove/parcels/routes.py
```

Create `~/GrowDirect/Cove/cove/parcels/services.py` with functions extracted from routes: `get_parcel_geojson(org_id)`, `get_lot_h_geojson()`, `get_map_layers()`, `get_research_detail(apn)`, `get_research_stats(org_id)`, `get_research_chart_data(org_id)`, `get_parcel(parcel_id)`. Move all data logic from routes into these functions.

- [ ] **Step 6: Verify services are untouched**

```bash
cd ~/GrowDirect/Cove
# These should all still exist:
ls cove/auth/services.py
ls cove/member/services.py
ls cove/governance/services.py
ls cove/governance/election_services.py
ls cove/governance/proceeding_services.py
ls cove/vault/services.py
ls cove/board/tag_services.py
ls cove/board/boundary_services.py
ls cove/treasury/services.py
ls cove/meetings/services.py
ls cove/agent/services.py
ls cove/archive/services.py
ls cove/notifications/services.py
ls cove/member/profile_services.py
ls cove/parcels/services.py  # newly extracted
```

- [ ] **Step 7: Verify models are untouched**

```bash
cd ~/GrowDirect/Cove
ls cove/models/
```

Expected: all model files still present.

- [ ] **Step 8: Commit the deletion**

```bash
cd ~/GrowDirect/Cove
git add -A
git commit -m "refactor: remove all Cove templates, routes, forms, old CSS for rebuild (GRO-365)"
```

---

## Chunk 5: Cove Frontend Rebuild — Base Templates and Auth

### Task 10: Create base.html and layout templates

**Files:**
- Create: `~/GrowDirect/Cove/templates/base.html`
- Create: `~/GrowDirect/Cove/templates/components/nav.html`
- Create: `~/GrowDirect/Cove/templates/components/flash.html`
- Create: `~/GrowDirect/Cove/templates/components/footer.html`

- [ ] **Step 1: Write base.html**

```html
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Cove{% endblock %}</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/dist/main.css') }}">
  {% block head %}{% endblock %}
</head>
<body class="h-full" x-data>
  {% block body %}
  <div class="cove-page flex">
    {% if current_user.is_authenticated %}
    {% include "components/nav.html" %}
    {% endif %}
    <main class="cove-content">
      {% include "components/flash.html" %}
      {% block content %}{% endblock %}
    </main>
  </div>
  {% endblock %}
  <script src="{{ url_for('static', filename='js/alpine.min.js') }}" defer></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

- [ ] **Step 2: Write nav.html component**

Sidebar nav using `cove-nav` classes. Links to all major sections: Dashboard, Directory, Governance, Vault, Meetings, Parcels, Treasury, Archive. Board section visible only to board members.

- [ ] **Step 3: Write flash.html component**

Flash message rendering using `cove-badge` / status classes.

- [ ] **Step 4: Write footer.html component**

Simple footer with copyright.

- [ ] **Step 5: Copy Alpine.js and Leaflet from node_modules to static/js**

```bash
cd ~/GrowDirect/Cove
mkdir -p static/js
cp node_modules/alpinejs/dist/cdn.min.js static/js/alpine.min.js
cp node_modules/leaflet/dist/leaflet.js static/js/leaflet.js
cp node_modules/leaflet/dist/leaflet.css static/css/leaflet.css
```

- [ ] **Step 6: Rebuild CSS (templates changed)**

```bash
cd ~/GrowDirect/Cove
npm run build
```

- [ ] **Step 7: Commit**

```bash
cd ~/GrowDirect/Cove
git add templates/ static/js/ static/css/leaflet.css
git commit -m "feat: create base.html and layout components with Alpine.js + Leaflet (GRO-365)"
```

---

### Task 10b: Create base form class

**Files:**
- Create: `~/GrowDirect/Cove/cove/forms.py`

- [ ] **Step 1: Write base form class**

```python
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

class CoveForm(FlaskForm):
    """Base form for all Cove forms. CSRF built in via FlaskForm.
    All app forms inherit from this, not FlaskForm directly."""
    pass

class CoveFileForm(CoveForm):
    """Base form for forms with file uploads."""
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
```

- [ ] **Step 2: Commit**

```bash
cd ~/GrowDirect/Cove
git add cove/forms.py
git commit -m "feat: create CoveForm base class (GRO-365)"
```

---

### Task 11: Rebuild auth blueprint (routes + forms + templates)

**Files:**
- Create: `~/GrowDirect/Cove/cove/auth/routes.py`
- Create: `~/GrowDirect/Cove/cove/auth/forms.py`
- Create: `~/GrowDirect/Cove/cove/auth/templates/login.html`
- Create: `~/GrowDirect/Cove/cove/auth/templates/verify.html`
- Create: `~/GrowDirect/Cove/tests/test_auth.py`

TDD flow: tests first, then implementation.

- [ ] **Step 1: Write auth route tests (BEFORE implementation)**

```python
# tests/test_auth.py
def test_login_get_returns_form(client):
    resp = client.get('/auth/login')
    assert resp.status_code == 200

def test_login_post_valid_email_sends_magic_link(client, db_session):
    resp = client.post('/auth/login', data={'email': 'test@example.com'})
    assert resp.status_code in (200, 302)

def test_verify_invalid_token_returns_error(client):
    resp = client.get('/auth/verify/invalid-token')
    assert resp.status_code in (400, 302)

def test_logout_redirects_to_landing(authenticated_client):
    resp = authenticated_client.get('/auth/logout')
    assert resp.status_code == 302
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
cd ~/GrowDirect/Cove
pytest tests/test_auth.py -v
```

Expected: FAIL (no routes exist yet).

- [ ] **Step 3: Write auth form**

```python
from cove.forms import CoveForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(CoveForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
```

- [ ] **Step 4: Write auth routes**

Three routes: `login` (GET/POST), `verify/<token>` (GET), `logout` (GET). Call existing `auth/services.py` for magic link generation and verification.

- [ ] **Step 5: Write login.html template**

Uses `cove-card`, `cove-form`, `cove-input`, `cove-btn-primary` classes. Magic link as primary, password as fallback. Inline error display below each field using `cove-error-inline`.

- [ ] **Step 6: Run tests — verify they pass**

```bash
cd ~/GrowDirect/Cove
pytest tests/test_auth.py -v
```

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
cd ~/GrowDirect/Cove
git add cove/auth/ tests/test_auth.py
git commit -m "feat: rebuild auth blueprint with platform form standard (GRO-365)"
```

---

### Task 12: Rebuild public blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/public/routes.py`
- Create: `~/GrowDirect/Cove/cove/public/templates/landing.html`
- Create: `~/GrowDirect/Cove/cove/public/templates/privacy.html`
- Create: `~/GrowDirect/Cove/cove/public/templates/terms.html`

- [ ] **Step 1: Write public routes**

Three simple GET routes: `/`, `/privacy`, `/terms`. No auth required.

- [ ] **Step 2: Write landing.html**

Landing page with login CTA. Uses `cove-btn-primary`.

- [ ] **Step 3: Write privacy.html and terms.html**

Static content pages extending base.html.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect/Cove
git add cove/public/
git commit -m "feat: rebuild public blueprint (GRO-365)"
```

---

## Chunk 6: Cove Frontend Rebuild — Member, Governance, Elections

### Task 13: Rebuild member blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/member/routes.py`
- Create: `~/GrowDirect/Cove/cove/member/forms.py`
- Create: `~/GrowDirect/Cove/cove/member/templates/dashboard.html`
- Create: `~/GrowDirect/Cove/cove/member/templates/directory.html`
- Create: `~/GrowDirect/Cove/cove/member/templates/profile.html`
- Create: `~/GrowDirect/Cove/cove/member/templates/onboarding.html`
- Create: `~/GrowDirect/Cove/cove/member/templates/accept_privacy.html`
- Create: `~/GrowDirect/Cove/cove/member/templates/notifications.html`
- Create: `~/GrowDirect/Cove/tests/test_member.py`

Routes per URL inventory (8 routes including accept-privacy). Forms for profile and onboarding (inherit from CoveForm). All templates use `cove-*` component classes. Call existing `member/services.py` and `member/profile_services.py`.

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

### Task 14: Rebuild governance blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/governance/routes.py`
- Create: `~/GrowDirect/Cove/cove/governance/forms.py`
- Create: `~/GrowDirect/Cove/cove/governance/templates/proposals.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/create_proposal.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/proposal_detail.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/ballot.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/results.html`

Routes per URL inventory (8 routes). Call existing `governance/services.py`. Ballot template must enforce secret ballot separation — no member identification on ballot UI.

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

### Task 15: Rebuild election blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/governance/election_routes.py`
- Create: `~/GrowDirect/Cove/cove/governance/election_forms.py`
- Create: `~/GrowDirect/Cove/cove/governance/templates/elections.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/election_detail.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/election_ballot.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/election_results.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/nominate.html`

Routes per URL inventory (10 routes). Call existing `governance/election_services.py`. Acclamation flow (AB 502), reconvened quorum (AB 2460).

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

### Task 16: Rebuild proceeding blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/governance/proceeding_routes.py`
- Create: `~/GrowDirect/Cove/cove/governance/proceeding_forms.py`
- Create: `~/GrowDirect/Cove/cove/governance/templates/proceedings.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/proceeding_detail.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/add_entry.html`
- Create: `~/GrowDirect/Cove/cove/governance/templates/evidence.html`

Routes per URL inventory (6 routes). Call existing `governance/proceeding_services.py`.

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

## Chunk 7: Cove Frontend Rebuild — Vault, Board, Treasury

### Task 17: Rebuild vault blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/vault/routes.py`
- Create: `~/GrowDirect/Cove/cove/vault/forms.py`
- Create: `~/GrowDirect/Cove/cove/vault/templates/index.html`
- Create: `~/GrowDirect/Cove/cove/vault/templates/upload.html`
- Create: `~/GrowDirect/Cove/cove/vault/templates/document.html`

Routes per URL inventory (6 routes). File upload form for documents. Call existing `vault/services.py`.

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

### Task 18: Rebuild board blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/board/routes.py`
- Create: `~/GrowDirect/Cove/cove/board/forms.py`
- Create: `~/GrowDirect/Cove/cove/board/templates/dashboard.html`
- Create: `~/GrowDirect/Cove/cove/board/templates/members.html`
- Create: `~/GrowDirect/Cove/cove/board/templates/parcels.html`
- Create: `~/GrowDirect/Cove/cove/board/templates/diagrams.html`
- Create: `~/GrowDirect/Cove/cove/board/templates/bulletin.html`
- Create: `~/GrowDirect/Cove/cove/board/templates/boundaries.html`

Routes per URL inventory (10 routes). Board-only access. Call existing `board/tag_services.py` and `board/boundary_services.py`. Boundaries page uses Leaflet.js for map rendering.

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

### Task 19: Rebuild treasury blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/treasury/routes.py`
- Create: `~/GrowDirect/Cove/cove/treasury/forms.py`
- Create: `~/GrowDirect/Cove/cove/treasury/templates/index.html`
- Create: `~/GrowDirect/Cove/cove/treasury/templates/assessments.html`
- Create: `~/GrowDirect/Cove/cove/treasury/templates/budget.html`
- Create: `~/GrowDirect/Cove/cove/treasury/templates/create_assessment.html`
- Create: `~/GrowDirect/Cove/cove/treasury/templates/record_payment.html`

Routes per URL inventory (5 routes). Call existing `treasury/services.py`.

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

## Chunk 8: Cove Frontend Rebuild — Parcels, Meetings, Agent, Archive

### Task 20: Rebuild parcels blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/parcels/routes.py`
- Create: `~/GrowDirect/Cove/cove/parcels/templates/map.html`
- Create: `~/GrowDirect/Cove/cove/parcels/templates/parcel_detail.html`

Routes per URL inventory (8 routes, including API endpoints for GeoJSON). Map page loads Leaflet.js and GeoJSON data from API routes. Uses `cove-map-container` class.

- [ ] Steps: Write routes → Write templates (map with Leaflet init) → Test → Commit

---

### Task 21: Rebuild meetings blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/meetings/routes.py`
- Create: `~/GrowDirect/Cove/cove/meetings/forms.py`
- Create: `~/GrowDirect/Cove/cove/meetings/templates/index.html`
- Create: `~/GrowDirect/Cove/cove/meetings/templates/create.html`
- Create: `~/GrowDirect/Cove/cove/meetings/templates/detail.html`
- Create: `~/GrowDirect/Cove/cove/meetings/templates/edit.html`
- Create: `~/GrowDirect/Cove/cove/meetings/templates/arc_apply.html`
- Create: `~/GrowDirect/Cove/cove/meetings/templates/arc_status.html`

Routes per URL inventory (9 routes). Call existing `meetings/services.py`. ICS download, attachment handling, ARC applications.

- [ ] Steps: Write route tests (TDD) → Run tests (verify fail) → Write forms → Write routes → Write templates → Run tests (verify pass) → Commit

---

### Task 22: Rebuild agent blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/agent/routes.py`
- Create: `~/GrowDirect/Cove/cove/agent/templates/transparency.html`

Routes per URL inventory (4 routes, 3 are API). Call existing `agent/services.py`. Transparency log page + JSON API endpoints.

- [ ] Steps: Write routes → Write template → Test → Commit

---

### Task 23: Rebuild archive blueprint

**Files:**
- Create: `~/GrowDirect/Cove/cove/archive/routes.py`
- Create: `~/GrowDirect/Cove/cove/archive/templates/index.html`
- Create: `~/GrowDirect/Cove/cove/archive/templates/timeline.html`
- Create: `~/GrowDirect/Cove/cove/archive/templates/chain.html`
- Create: `~/GrowDirect/Cove/cove/archive/templates/bylaws.html`
- Create: `~/GrowDirect/Cove/cove/archive/templates/catalog.html`
- Create: `~/GrowDirect/Cove/cove/archive/templates/document.html`

Routes per URL inventory (9 routes). Call existing `archive/services.py`. Static file serving for originals and data files.

- [ ] Steps: Write routes → Write templates → Test → Commit

---

## Chunk 9: pgvector Integration & Final Verification

### Task 24: Add pgvector to Cove models

**Files:**
- Modify: `~/GrowDirect/Cove/cove/models/document.py` (add vector column)
- Modify: `~/GrowDirect/Cove/cove/models/governance.py` (add vector column to Proposal model)
- Modify: `~/GrowDirect/Cove/cove/models/meetings.py` (add vector column to Meeting model — note: plural filename)
- Create: `~/GrowDirect/Cove/cove/services/embedding.py`

- [ ] **Step 1: Write embedding service**

```python
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _model

def embed_text(text: str) -> list[float]:
    model = get_model()
    return model.encode(text).tolist()
```

- [ ] **Step 2: Add Vector columns to models**

Add `embedding: Mapped[Optional[Vector]] = mapped_column(Vector(384), nullable=True)` to Document, Proposal, and Meeting models.

- [ ] **Step 3: Create Alembic migration**

```bash
cd ~/GrowDirect/Cove
alembic revision --autogenerate -m "add pgvector embeddings to document, proposal, meeting"
alembic upgrade head
```

- [ ] **Step 4: Add embedding to vault service on document create/update**

Modify `vault/services.py` `upload_document` and `create_version` to call `embed_text` on document title + description.

- [ ] **Step 5: Add embedding to governance service on proposal create**

Modify `governance/services.py` `create_proposal` to call `embed_text` on title + description.

- [ ] **Step 6: Add semantic search to vault**

Add a `search_documents_semantic(org_id, query)` function to `vault/services.py` using cosine distance.

- [ ] **Step 6b: Add semantic search to governance**

Add a `search_proposals_semantic(org_id, query)` function to `governance/services.py` using cosine distance. This powers "find related proposals/precedents."

- [ ] **Step 6c: Add semantic search to meetings**

Add a `search_meetings_semantic(org_id, query)` function to `meetings/services.py` using cosine distance. This powers "find related discussions."

- [ ] **Step 7: Add sentence-transformers to requirements.txt**

```
sentence-transformers>=2.2
pgvector>=0.2
```

- [ ] **Step 8: Test embedding and search**

Write tests for embedding service and semantic search.

- [ ] **Step 9: Commit**

```bash
cd ~/GrowDirect/Cove
git add -A
git commit -m "feat: add pgvector semantic search to documents, proposals, meetings (GRO-365)"
```

---

### Task 25: Full verification pass

- [ ] **Step 1: Run full test suite**

```bash
cd ~/GrowDirect/Cove
pytest -v
```

All tests must pass.

- [ ] **Step 2: Verify every URL from inventory**

Start the Docker stack and hit every URL from `docs/url-inventory.md`. Each should return 200 (or appropriate redirect/auth challenge).

- [ ] **Step 3: Verify Docker health checks**

```bash
cd ~/GrowDirect/Cove/devops
docker compose ps
```

All services should show "healthy."

- [ ] **Step 4: Verify CSS build**

```bash
cd ~/GrowDirect/Cove
npm run build
ls -la static/css/dist/main.css
```

Build should succeed, output file should exist.

- [ ] **Step 5: Verify no CDN dependencies**

```bash
grep -r "cdn" ~/GrowDirect/Cove/templates/ ~/GrowDirect/Cove/cove/**/templates/ 2>/dev/null
```

Expected: no results (no CDN references in any template).

- [ ] **Step 6: Final commit**

```bash
cd ~/GrowDirect/Cove
git add -A
git commit -m "feat: complete Cove frontend rebuild on GrowDirect platform (GRO-365)"
```

---

## Summary

| Chunk | Tasks | What it produces |
|-------|-------|-----------------|
| 1 | 1-5 | GrowDirect platform layer (CLAUDE.md, factory skills, standards docs, Cove wrappers) |
| 2 | 6 | Tailwind + PostCSS build pipeline with cove.css |
| 3 | 7 | Docker compose twin (matches Canary pattern) |
| 4 | 8-9 | URL inventory + delete old frontend |
| 5 | 10-12 | Base templates, auth, public blueprints |
| 6 | 13-16 | Member, governance, elections, proceedings |
| 7 | 17-19 | Vault, board, treasury |
| 8 | 20-23 | Parcels (maps), meetings, agent, archive |
| 9 | 24-25 | pgvector integration + full verification |
