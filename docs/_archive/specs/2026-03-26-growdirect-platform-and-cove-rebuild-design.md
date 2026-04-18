# GrowDirect Platform & Cove Rebuild Design

**GRO-365** | 2026-03-26

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

## Problem

When Cove was created, the agent copied Canary's structure and built a standalone app from scratch. No GrowDirect platform standards existed, so six weeks of sessions compounded drift. Auth, config, models, skills, CSS, Docker — all rebuilt from zero instead of following the patterns ALX learned building Canary.

GrowDirect is a software company that builds apps. The platform is the **process and standards**, not shared code. Each app is its own codebase and repo, but built the same way. Lessons learned on one project must carry forward to the next.

## Design

### Part 1: GrowDirect Platform Layer

#### What it is

A set of standards, factory skills, and a master CLAUDE.md that any new app agent loads on startup. Not a shared Python package. Not a monorepo framework. Just: "here's how we build things here."

#### Memory architecture

Three layers of knowledge, each with its own scope:

- **GrowDirect level** — Process memory. How we build things. Platform standards, factory process, post-mortems. Lives in `~/GrowDirect/CLAUDE.md` and `~/GrowDirect/docs/standards/`.
- **App agent level** — Product memory. Each app agent (ALX for Canary, Cove builder for Cove) maintains a pgvector knowledge graph of what it has learned about its codebase and domain. App-specific, not shared.
- **App user level** — pgvector powers user-facing features in each app (document search, semantic matching). Same infrastructure, different data.

#### Deliverables

**`~/GrowDirect/CLAUDE.md`** — Master standards document. Every app's CLAUDE.md starts by referencing this as parent. Contains:

- Tech stack (Flask 3+, SQLAlchemy 2.0 Mapped[], PostgreSQL 17 with pgvector, Alembic, Valkey, Gunicorn)
- Model standards (UUID primary keys, `created_at`/`updated_at`, audit mixins, tenant mixins)
- Auth pattern (Flask-Login, session management, role/permission base classes)
- Config pattern (env-based config classes with this structure):
  ```python
  class BaseConfig:
      SECRET_KEY = os.environ['SECRET_KEY']
      SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
      SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
      # Security defaults — every app gets these
  class DevConfig(BaseConfig): DEBUG = True
  class TestConfig(BaseConfig): TESTING = True; use test database
  class StagingConfig(BaseConfig): pass
  class ProdConfig(BaseConfig): pass
  ```
- CSS standard (Tailwind 3.x with PostCSS build, `<appname>.css` component classes, no CDN, no utility soup in templates)
- Frontend standard (Alpine.js 3.x via npm for interactivity — loaded from node_modules not CDN; Leaflet.js via npm for any map features)
- Docker standard (compose for dev, two-stage Dockerfile for prod, Gunicorn)
- Test standard (pytest, conftest with fixtures, unit/integration/smoke layers)
- Protected files list (.env, wsgi.py, session factory, Dockerfile, docker-compose)
- Factory process reference (blueprint -> tdd -> assembly -> verify -> qa -> ship)
- Valkey standard (session store + cache + background task queue via Valkey 8; every app's Docker compose includes a Valkey service; Flask config points session backend at Valkey)
- pgvector standard (every app gets vector search from day one):
  - Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions, runs locally, no API dependency)
  - Vector column: `Vector(384)` on any model that needs semantic search
  - Embedding happens on write (create/update) as a synchronous step — no background jobs until scale demands it
  - Similarity search via cosine distance (`<=>` operator)
- Form standard (WTForms with server-side validation; errors render inline below each field; base form class with CSRF built in; file uploads use a consistent upload service pattern)
- Hard rules (no SQLite in prod, no lazy pipes, no file creation without cause, canonical UUID principle, no CDN dependencies — all JS/CSS via npm and build pipeline)

**`~/GrowDirect/.claude/skills/`** — Shared factory skills:

- `factory-startup` — Reads `~/GrowDirect/CLAUDE.md` by absolute path first, then reads the app's own CLAUDE.md, then loads last session context. This is a literal file read, not an import mechanism.
- `factory-close` — Session close with summary
- `factory-blueprint` — Feature specification
- `factory-tdd` — Test-first development
- `factory-assembly` — Implementation against passing tests
- `factory-verify` — Verification and integration
- `factory-qa` — Quality assurance pass
- `factory-ship` — Deployment preparation

Existing `canary-*` and `cove-*` skills become thin wrappers that add app-specific domain context on top of the shared factory skills.

**`~/GrowDirect/docs/standards/`** — Human-readable references:

- `tech-stack.md` — Canonical stack with version pins
- `coding-standards.md` — Python/Flask/SQLAlchemy patterns
- `css-framework.md` — Tailwind + PostCSS build pipeline, component class patterns
- `factory-process.md` — The six-stage build process

**`~/GrowDirect/docs/post-mortems/`** — Post-mortem archive:

- Agent writes post-mortem after each ship cycle
- Jeffe reviews and decides what gets promoted to platform standards
- Agent does NOT auto-update standards — prevents closed-loop bloat

#### What it is NOT

- Not a shared Python package or library
- Not a monorepo — apps stay in separate directories (and can be separate repos)
- Not a template generator — the agent builds from knowledge of the standards, not from scaffolding scripts
- Not self-modifying — the post-mortem loop has a human gate

### Part 2: Cove Frontend Rebuild

#### Cutover strategy

Cove is pre-launch. No production users. This is a clean rebuild, not a migration. Steps:

1. Catalogue all current routes and URL patterns before deleting anything (save to `docs/url-inventory.md`)
2. Delete all templates, routes, forms, CSS
3. Rebuild on real framework
4. Verify every URL from the inventory works
5. Run full test suite

No feature flags, no parallel running, no rollback plan needed — there are no users to disrupt.

#### Keep (backend infrastructure)

Everything that represents domain logic and data:

- **All models** — ~33 SQLAlchemy tables (Organization, Parcel, Member, Proposal, Ballot, BallotEnvelope, Election, Assessment, Document, Meeting, etc.)
- **Voting engine** — Proposal creation, ballot management, secret ballot separation, quorum calculations, election services
- **Parcel engine** — APN-based identity, Leaflet.js/GeoJSON map services, parcel data management
- **Notification service** — Email notifications, Flask-Mail integration (notifications are handled within existing blueprints, not a separate blueprint)
- **Meeting engine** — Scheduling, ARC applications
- **Document vault** — Upload, versioning, search
- **Archive service** — Document archive, narrative, timeline
- **Treasury services** — Budget, assessments, ledger (assessments live inside the treasury blueprint)
- **Alembic migrations** — All 3 existing migrations, full migration history
- **All data** — Everything in the database stays
- **Davis-Stirling compliance logic** — Secret ballot separation (ballots table has no member_id), quorum rules (General 1/3, Assessment 1/2, Elections none), APN-as-identity, Civil Code sections 5100-5145
- **pgvector extension** — Already in Cove's Docker image (pg17 with pgvector). Currently unused. Wire it up properly this time.
- **`config.py`** — Adapt to platform config pattern (BaseConfig with security defaults, env-specific subclasses)
- **`extensions.py`** — db, login_manager, mail, csrf — adapt to platform pattern (add Valkey session config)
- **`wsgi.py`** — Entry point (protected file)

#### Throw away

Everything that is presentation/routing:

- All Jinja2 templates (60+ files across blueprints)
- All `routes.py` files in every blueprint (after cataloguing URLs — see cutover strategy)
- All `forms.py` files (rebuild with platform form standard)
- `base.html` and the CDN Tailwind setup
- Current CSS (static/css/)
- Current loose Alpine.js usage
- `package.json` (replace with proper build config)

#### Rebuild

- **`base.html`** — New base template with Tailwind build output, Alpine.js 3.x loaded from node_modules, Leaflet.js loaded from node_modules (only on pages that need maps)
- **`cove.css`** — Component classes built on Tailwind (cards, forms, tables, nav, modals, badges, status indicators, map containers)
- **`tailwind.config.js`** — Defines `cove-50` through `cove-900` color scale, content paths to templates
- **`postcss.config.js`** — PostCSS with `postcss-import`, `tailwindcss`, `autoprefixer` plugins
- **`package.json`** — Build scripts using PostCSS CLI: `dev` (watch), `build` (minified production output). Dependencies: tailwindcss, postcss, postcss-cli, postcss-import, autoprefixer, alpinejs, leaflet
- **Blueprint routes** — Same URL structure (verified against inventory), clean handlers that call existing services. 13 blueprints: public, auth, member, governance, election, proceeding, vault, board, treasury, parcels, meetings, agent, archive
- **Templates** — Fewer total, using component classes from `cove.css`. Each template uses defined component patterns, not ad-hoc Tailwind utilities
- **Forms** — Platform form standard: WTForms base class with CSRF, server-side validation, inline error rendering below each field, consistent file upload pattern for document vault
- **Auth flows** — Magic link + password login, rebuilt on platform auth standard
- **Map UI** — Leaflet.js from npm (not CDN), GeoJSON integration rebuilt on new templates, calling existing parcel service layer
- **pgvector integration** — Vector search for document vault (semantic document search), meeting minutes (find related discussions), governance (find related proposals/precedents). Uses `sentence-transformers/all-MiniLM-L6-v2`, `Vector(384)`, embeddings on write, cosine similarity search.

### Part 3: CSS Framework Standard

#### GrowDirect CSS standard (applies to all apps)

Every GrowDirect app has:

1. **`tailwind.config.js`** — App configuration
   - App-specific color scale (e.g., `cove-50` through `cove-900`)
   - Custom typography scale if needed
   - Content paths pointing to templates directory

2. **`postcss.config.js`** — Build pipeline
   ```js
   module.exports = {
     plugins: {
       'postcss-import': {},
       tailwindcss: {},
       autoprefixer: {},
     }
   }
   ```

3. **`static/css/main.css`** — Entry point
   ```css
   @import 'tailwindcss/base';
   @import 'tailwindcss/components';
   @import './<appname>.css';
   @import 'tailwindcss/utilities';
   ```

4. **`static/css/<appname>.css`** — Component classes using `@apply`
   - Every repeating visual pattern gets a component class
   - Templates reference component classes, not raw utility chains
   - If a utility pattern appears more than twice, it becomes a component class

5. **`package.json`** — Build scripts
   - `dev`: `postcss static/css/main.css -o static/css/dist/main.css --watch`
   - `build`: `postcss static/css/main.css -o static/css/dist/main.css --env production`
   - Templates reference `static/css/dist/main.css` (the built output)

6. **Build enforcement** — Agent skills block template creation that uses raw Tailwind utility chains for patterns that have component classes defined

#### Cove-specific CSS (`cove.css`)

Component classes for Cove's domain:

- **Layout**: `.cove-page`, `.cove-sidebar`, `.cove-content`
- **Cards**: `.cove-card`, `.cove-card-header`, `.cove-card-body`
- **Forms**: `.cove-form`, `.cove-input`, `.cove-select`, `.cove-checkbox`, `.cove-error`, `.cove-error-inline`
- **Tables**: `.cove-table`, `.cove-th`, `.cove-td`
- **Nav**: `.cove-nav`, `.cove-nav-item`, `.cove-nav-active`
- **Buttons**: `.cove-btn`, `.cove-btn-primary`, `.cove-btn-secondary`, `.cove-btn-danger`
- **Modals**: `.cove-modal`, `.cove-modal-overlay`
- **Badges/Status**: `.cove-badge`, `.cove-status-active`, `.cove-status-pending`, `.cove-status-closed`
- **Maps**: `.cove-map-container`, `.cove-map-overlay`, `.cove-parcel-popup`
- **Voting**: `.cove-ballot`, `.cove-proposal-card`, `.cove-vote-btn`
- **Documents**: `.cove-doc-card`, `.cove-doc-preview`

## Execution Order

1. **Platform layer first** — Create `~/GrowDirect/CLAUDE.md`, shared factory skills, standards docs
2. **CSS framework** — Define the Tailwind + PostCSS build standard, create `cove.css` with component classes
3. **Cove rebuild** — Catalogue URLs, throw away templates/routes, rebuild on real framework using `cove.css`
4. **Adapt Canary** — Update Canary's CLAUDE.md to reference parent, thin-wrap canary-* skills (separate GRO issue)

## Success Criteria

- Any new GrowDirect app agent loads platform standards on startup without being told
- Cove frontend is rebuilt with fewer templates, all using `cove.css` component classes
- No CDN dependencies — all JS/CSS via npm and build pipeline
- All existing Cove data, services, and compliance logic untouched
- pgvector wired up and serving document search, governance precedents, meeting search
- Factory process skills shared, not duplicated
- Post-mortem loop has human gate — agent proposes, Jeffe promotes
