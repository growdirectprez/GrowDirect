# GrowDirect

The GrowDirect platform — a solo-founder operation building SaaS tools
with AI assistance. This repo is the monorepo root. Product apps,
shared infrastructure, the Brain (Obsidian vault), and the content
engine all live here.

## What's inside

| Path | Contents |
|---|---|
| `Canary/` | Loss prevention analytics for Square merchants (near-beta). |
| `Cove/` | HOA governance platform for WPBCA (81 lots, Abalone Cove, RPV). Early dev. |
| `Cove/cove/angel/` + `Angel/` | Real-estate intelligence + lead generation for Compass agents. Code in Cove, knowledge in Angel. |
| `Seacove/` | SketchUp model-building pipeline for 25 Seacove Drive. Standalone. |
| `Brain/` | Obsidian second brain — project MOCs, wiki articles, method cards, raw source material. |
| `devops/` | Shared Docker Compose stack — Postgres, Valkey, pgAdmin, Ollama. |
| `services/memory-bus/` | Platform memory MCP — pgvector over curated knowledge. |
| `content-engine/` | CLI that extracts, ingests, and indexes source material into Brain. |
| `docs/` | Platform SDDs, ADRs, dispatches, playbooks, team profiles. |
| `factory-manifest.json` | Factory stage definitions. |

## Products at a glance

- **[Canary](Canary/)** — loss prevention. 29 detection rules, TSP
  pipeline, evidence hash chain, MCP agent mesh. **Near-beta.** Live
  demo: https://canary.growdirect.app
- **[Cove](Cove/)** — HOA governance for the Whites Point Beach Club
  Association. Parcel GIS, governance documents, contact roster.
  Early dev.
- **[Angel](Angel/)** — real-estate intelligence layer inside Cove.
  pgvector over MLS + market memory, agent sidecar for workflow
  assistance. Early dev.
- **[Seacove](Seacove/)** — a one-off SketchUp pipeline for a single
  project. Not connected to platform infra.

Roadmap and backlog live in Linear (GRO-prefixed issues).

## The Method

GrowDirect is built on a documentation-as-code factory:

```
SDD  ─▶  chunked memories  ─▶  Brain/wiki/  ─▶  code
                                    │
                                    ▼
                             Factory pipeline
                             (every layer traceable)
```

The Architect writes the SDD. ALX chunks it into memory. The Writer
narrates it in Brain/wiki/. The Engineer implements it. The Factory
pipeline keeps everything in sync.

See [Brain/projects/Method.md](Brain/projects/Method.md) for the full
explanation, [Brain/projects/Canary.md](Brain/projects/Canary.md) for
the Canary MOC, and [Canary/docs/sdds/v2/](Canary/docs/sdds/v2/) for
16 subsystem design documents.

## Stack

- Python 3.12 (always `python3`, never `python`)
- Flask 3+ with Jinja2 templates — server-rendered, not SPA
- SQLAlchemy 2.0 with `Mapped[]` annotations
- PostgreSQL 17 with pgvector — no SQLite, anywhere
- Valkey 8 — sessions, cache, streams
- Gunicorn with `--reload` in dev
- Alembic for migrations
- pytest for testing
- Tailwind 3.x + Alpine.js 3.x (npm-built, no CDN)
- Ollama with `qwen3-embedding:8b` for embeddings

## Shared infrastructure

All apps share one Docker Compose stack at `devops/docker-compose.yml`:

```
growdirect_postgres   :5432   — all databases (canary, cove, memory)
growdirect_valkey     :6379   — sessions + cache
growdirect_pgadmin    :5050   — DB admin UI
growdirect_ollama     :11434  — embeddings and inference
growdirect_memory_bus :8003   — platform memory MCP (pgvector)
```

## Quick start

```bash
# Clone + pull
git clone git@github.com:growdirectprez/GrowDirect.git
cd GrowDirect

# Shared infra up
cd devops && docker compose up -d && cd ..

# Canary (reference product)
cd Canary && ./devops/scripts/dev.sh up
curl -s http://localhost:5001/health   # → {"ok": true}
```

For full Canary onboarding see [Canary/README.md](Canary/README.md) and
[Canary/CLAUDE.md](Canary/CLAUDE.md).

## Repo conventions

- **Build, don't organize.** Ship features, not scaffolding.
- **One deliverable per session.** Commit or revert — no sprawl.
- **Describe what is, not what should be.** Docs reflect the current
  state of the code.
- **Check Brain before creating.** Brain is the canonical index of
  domain knowledge; update existing articles rather than parallel docs.
- **No loose files in the repo root.** Project docs belong in the
  project; research belongs in `Brain/`.

Full rules: [CLAUDE.md](CLAUDE.md).

## Built by

One founder plus AI agents. Claude Code for development, Cowork for
strategy and content, a growing mesh of MCP servers for tool access.
The Canary Goes Primetime rollout is the first public proof that a
solo operator with deep domain expertise can ship what used to
require a 50-person engineering org.

## License

Proprietary — see `LICENSE`. All rights reserved.

For licensing, partnership, or authorized evaluation:
contact@growdirect.io

## Security

See `SECURITY.md`. Report vulnerabilities privately to
security@growdirect.io.

---

*GrowDirect Inc. | Confidential*
