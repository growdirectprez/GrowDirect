> **Platform parent:** Read ~/GrowDirect/CLAUDE.md first.

# ARC — AI Draftsman

ARC is a CLI pipeline tool, NOT a web app. It does not follow the Flask/PostgreSQL
pattern used by Canary and Cove.

## What ARC Is

- Python CLI tool that reads blueprints and generates SketchUp Ruby scripts
- File-based I/O between pipeline stages (JSON spatial models, .rb output)
- Single-user tool for Jeffe's projects — no multi-tenancy

## Hard Rules

1. **No MCP** — ARC never registers as an MCP server. Invisible to platform.
2. **No memory bus** — ARC does not participate in the platform memory bus.
3. **No Linear/GRO dispatch** — ARC is not managed by ALX or factory pipeline.
4. **No Flask** — No web server, no routes, no templates (except Jinja2 for Ruby codegen).
5. **No shared database** — File-based storage only (JSON). May use Postgres later.
6. **Directory boundary** — Everything stays inside `GrowDirect/Seacove/`.

## What ARC CAN Use

- Ollama (vision + embeddings) via localhost:11434
- Local filesystem
- pytest for testing

## Pipeline

```
arc ingest <project>    — normalize inputs (PDFs, photos, descriptions)
arc extract <project>   — vision AI reads dimensions from blueprints
arc model <project>     — build spatial model from extractions
arc validate <project>  — check model consistency
arc generate <project>  — produce SketchUp Ruby scripts
```

## Protected Files

- `arc/model/spatial_model.py` — core data structure
- `templates/ruby/*.rb.j2` — Ruby code templates
