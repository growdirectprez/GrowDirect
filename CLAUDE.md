# GrowDirect — Platform Context

This is the working repo for GrowDirect, a solo-founder operation building SaaS
tools with AI assistance (Cowork sessions). Read this file first. App-specific
CLAUDE.md files add domain context.

**Honest status as of April 2026 — 8 weeks in:**
This project has more scaffolding than shipping code. Sessions tend to build
frameworks, folder structures, and config rather than delivering features. If
you're an AI agent reading this: build something that runs, don't reorganize files.

---

## Active Projects

| Project | Directory | Status | What it is |
|---------|-----------|--------|------------|
| Canary | `Canary/` | **Near-beta** | Loss prevention analytics for Square merchants. 293 Python files, 20+ blueprints, 213 tests. Needs docker-compose + migrations to boot. |
| Cove | `Cove/` | **Early dev** | HOA governance app for WPBCA (81 lots, Abalone Cove, RPV). 109 Python files, 25 migrations, 10 templates. Has a working docker-compose. Massive research archive (773 docs) that needs cleanup. |
| Angel | `Angel/` | **Parked** | Website builder / technical consultant for realtors. 11 Python files, no templates. Concept only — not active. |
| Seacove | `Seacove/` | **Standalone hobby** | SketchUp model-building pipeline for 25 Seacove Drive. Has CLI, Ruby generation, tests. Not connected to platform infra. Has its own plugin (`rpv-permit-architect`). |

**Removed:** Viva (crypto treasury engine) — was pure scaffolding with zero business logic. Skills and references should be deleted.

---

## What Needs to Happen Next

1. **Canary boot** — Create docker-compose.yml, generate Alembic migrations from existing models, get `/health` responding. Then find a beta customer.
2. **Cove v1 scope** — Member directory (81 lots), document vault (founding instruments + governance docs), basic meeting/election tools. Stop researching, start shipping.
3. **Cove archive cleanup** — Flatten the 8-layer folder trees, remove duplicate paths, delete empty directories. The `Cove/docs/` structure has triple-layered duplicates from multiple reorganization sessions.
4. **Content engine** — Build a reusable intake pipeline: raw files in → process/summarize → archive with flat structure → index. Every project needs this. Should be a Cowork skill.

---

## Tech Stack

- Python 3.12 (`python3`, never `python`)
- Flask 3+ with Jinja2 templates — server-rendered, not SPA
- SQLAlchemy 2.0 with `Mapped[]` syntax — no `Column()`
- PostgreSQL 17 with pgvector — no SQLite
- Valkey 8 — sessions, cache, task queue
- Gunicorn with `--reload` in dev
- Alembic for migrations
- pytest for testing
- Tailwind 3.x with PostCSS build — no CDN
- Alpine.js 3.x via npm for interactivity
- Leaflet.js via npm for maps (Cove parcels)
- Ollama with `qwen3-embedding:8b` (1024-dim vectors)

---

## Shared Infrastructure

All apps share one Docker Compose stack at `devops/docker-compose.yml`:

```
growdirect_postgres   :5432   — all databases
growdirect_valkey     :6379   — sessions and cache
growdirect_pgadmin    :5050   — DB admin UI
growdirect_ollama     :11434  — embeddings and inference
```

Network: `growdirect` (external). App compose files join this network.

```bash
# Start shared infra
cd ~/GrowDirect/devops && docker compose up -d

# Start an app
cd ~/GrowDirect/<App>/devops && docker compose up -d
```

### Databases

| Database | Purpose |
|----------|---------|
| `canary` / `canary_test` | Canary (schemas: app, sales, metrics) |
| `cove` / `cove_test` | Cove |
| `angel` / `angel_test` | Angel (when active) |
| `growdirect_memory` / `growdirect_memory_test` | Platform memory bus |

Dev credentials: `growdirect / growdirect_dev`

Valkey: DB 0 = Canary, DB 1 = Cove, DB 3 = Angel

### Ports

| Service | Port |
|---------|------|
| Canary Flask | 5001 |
| Cove Flask | 5002 |
| Angel Flask | 5004 |
| Cove MailHog SMTP / Web | 1026 / 8026 |

### Docker Rules

- Every `build:` block needs `image: <appname>-<service>` to prevent collisions
- Every compose file needs top-level `name: <appname>` to prevent orphan conflicts
- `ModuleNotFoundError` = rebuild the image, don't hack the code
- Dev: mount code dirs. Never mount `.env`, `requirements.txt`, `node_modules/`

---

## Code Standards

### Models
- UUID primary keys (`Mapped[uuid.UUID]`, default `uuid.uuid4`)
- `created_at` and `updated_at` on every table
- `Mapped[]` annotations, never `Column()`

### Auth
- Flask-Login, magic link (primary), password (fallback)
- `@login_required` on every non-public route
- Session backend: Valkey

### Config
- Env-based: `BaseConfig`, `DevConfig`, `TestConfig`, `ProdConfig`
- No hardcoded secrets
- `SESSION_TYPE = "redis"` (Valkey-compatible)

### Testing
- pytest with `conftest.py` fixtures
- Layers: unit, integration, smoke
- Separate test database (`<appname>_test`)

---

## Session Discipline

These rules exist because past sessions created sprawl. Follow them.

1. **Build, don't organize.** If a session produces folders and configs but no
   running code, it failed. Prefer one working feature over ten planned ones.
2. **One deliverable per session.** Scope to something that can be committed and
   verified. "Organize all docs" is not a deliverable. "Get Canary booting in
   Docker" is.
3. **Delete before creating.** If something is empty, broken, or duplicated,
   remove it. Don't build around it. Don't create a v2 next to the v1.
4. **Describe what is, not what should be.** SDDs, CLAUDE.md, and docs should
   reflect the current state of the code. Don't write architecture docs for
   systems that don't exist.
5. **No scaffolding for parked projects.** Angel is parked. Don't create skills,
   migrations, or infrastructure for it until it's active.
6. **Flat archives.** Research files go in `<project>/docs/archive/` with a flat
   or shallow structure. No 8-layer folder nesting. If you can't find a file,
   the structure is wrong.
7. **Commit or revert.** Don't leave 100+ uncommitted changes across sessions.
   Each session commits its own work or reverts it.

---

## Known Debt

- `Cove/docs/` has triple-layered duplicate folders (archive/originals/founding,
  admin/research/founding, archive/founding). Needs flattening.
- Canary has no docker-compose.yml and zero Alembic migration files despite 20+ models.
- 52 skills in `.claude/skills/`, many for apps that are parked or don't exist. Prune to what's actually used.
- `docs/` root has 520+ markdown files outside the SDD/decisions/post-mortem structure. Most are session artifacts that were never filed properly.
- Brain/ Obsidian vault was set up but wiki articles contain broken links from multiple reorganizations.
- 112 uncommitted git changes from previous sessions.

---

## File Layout

```
GrowDirect/
├── CLAUDE.md              ← you are here
├── Canary/                — loss prevention app (near-beta)
├── Cove/                  — HOA governance app (early dev)
├── Angel/                 — realtor tools (parked)
├── Seacove/               — SketchUp hobby project (standalone)
├── Brain/                 — Obsidian second brain (wiki, templates, MOCs)
├── devops/                — shared Docker infra (postgres, valkey, ollama)
├── docs/                  — platform docs (SDDs, decisions, team, research)
├── .claude/skills/        — factory and app skills (needs pruning)
├── services/              — growdirect-mcp (memory bus)
└── factory-manifest.json  — factory stage definitions
```
