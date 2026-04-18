# GrowDirect — Platform Context

This is the working repo for GrowDirect, a solo-founder operation building SaaS
tools with AI assistance (Claude Code for development, Cowork for strategy and
content). Read this file first. App-specific CLAUDE.md files add domain context.

**Rule zero:** Build something that runs. Don't reorganize files. Don't create
scaffolding. Ship features.

---

## Projects

| Project | Directory | Status | What it is |
|---------|-----------|--------|------------|
| Canary | `Canary/` | **Near-beta** | Loss prevention analytics for Square merchants. |
| Cove | `Cove/` | **Early dev** | HOA governance platform for WPBCA (81 lots, Abalone Cove, RPV). |
| Angel | `Cove/cove/angel/` + `Angel/` | **Active (Cove module)** | Real estate intelligence + lead gen for Compass agents. Code in Cove, knowledge in Angel/. |
| Seacove | `Seacove/` | **Standalone** | SketchUp model-building pipeline for 25 Seacove Drive. Not connected to platform infra. |

**Roadmap and backlog live in Linear** (GRO-prefixed issues). Don't duplicate
task lists or priorities here — check Linear for what's next.

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
| `cove` / `cove_test` | Cove + Angel (Angel is a Cove module, same DB) |
| `growdirect_memory` / `growdirect_memory_test` | Platform memory bus |

Dev credentials: `growdirect / growdirect_dev`

Valkey: DB 0 = Canary, DB 1 = Cove + Angel

### Ports

| Service | Port |
|---------|------|
| Canary Flask | 5001 |
| Cove Flask (includes Angel) | 5002 |
| Angel Agent sidecar | 8004 |
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
5. **No scaffolding without a Linear issue.** Don't create skills, migrations,
   or infrastructure speculatively. If it's not tied to a GRO issue, it shouldn't
   be built.
6. **Flat archives.** Research files go in `<project>/docs/archive/` with a flat
   or shallow structure. No 8-layer folder nesting. If you can't find a file,
   the structure is wrong.
7. **Commit or revert.** Don't leave 100+ uncommitted changes across sessions.
   Each session commits its own work or reverts it.
8. **Check Brain before creating.** Search Brain wiki before writing new docs.
   If Brain covers it, update the existing article — don't create a parallel doc.
9. **Route knowledge through Brain.** If a session produces knowledge (research,
   analysis, decisions), it goes into `Brain/wiki/` — not dumped as a loose file.
10. **Clean up your own artifacts.** Reports, manifests, and one-shot scripts
    created during a session get deleted before the session ends. The content
    engine itself stays; its output doesn't.

---

## Brain — Domain Knowledge

GrowDirect/ is the Obsidian vault. Brain/ holds the curated knowledge.

**Before domain work:** Read the project MOC (`Brain/projects/<Project>.md`).
It links to all wiki articles and source material for that project.

**Before creating docs:** Search Brain first — `mcp__obsidian__obsidian_simple_search`
or `engine.py registry check "<topic>"`. If it exists, update it.

**Reading/writing Brain content:** Use `mcp__obsidian__*` tools (search, get,
patch, append). Use `Read`/`Edit` for code files, not Brain content.

**After producing knowledge:** New wiki articles or updates go directly in
`Brain/wiki/`. Use Brain templates in `Brain/templates/` for structure.

**No volatile data in wiki.** Row counts, record numbers, and stats belong in
the database, not flat files. Wiki articles capture structure, relationships,
decisions, and context that can't be derived from code or queries.

---

## File Layout

```
GrowDirect/
├── CLAUDE.md              ← you are here (platform rules + standards)
├── Brain/                 — Obsidian second brain (read MOCs first for domain context)
├── Canary/                — loss prevention app (near-beta)
├── Cove/                  — HOA governance + Angel module (early dev)
├── Angel/                 — Angel knowledge repo (code lives in Cove/)
├── Seacove/               — SketchUp pipeline (standalone)
├── content-engine/        — CLI: scan, dupes, triage, ingest, registry
├── devops/                — shared Docker infra (postgres, valkey, ollama)
├── docs/                  — platform docs (SDDs, decisions, team)
├── .claude/skills/        — Claude Code factory skills (not used in Cowork)
├── services/              — growdirect-mcp (memory bus)
└── factory-manifest.json  — factory stage definitions
```
