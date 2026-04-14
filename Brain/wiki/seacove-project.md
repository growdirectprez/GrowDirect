---
date: 2026-04-13
type: wiki
status: current
tags: [seacove, architecture, sketchup, rpv, permits, arc]
last-compiled: 2026-04-13
---

# 25 Seacove Drive — Project Overview

**Wiki:** [[Brain/projects/Seacove|Seacove]]

25 Seacove Drive is a residential property in WPBCA Tract 14649, Rancho Palos Verdes. The Seacove project builds a SketchUp 3D model of the house from original blueprints using ARC, a custom CLI pipeline.

---

## The Property

- **Address:** 25 Seacove Drive, Rancho Palos Verdes, CA 90275
- **Tract:** 14649 (WPBCA, 81 lots)
- **APN:** Within Cove's research_parcels dataset

The house has been modified multiple times since original construction:
1. **Original build** — 6 blueprint sheets (plot plan, foundation, floor plan, exterior elevations, interior elevations, HVAC)
2. **1960 bedroom addition** — 2 sheets
3. **Garage addition** — 3 sheets
4. **Phase 3 (2020)** — Kitchen/JADU remodel, 2 sheets + Visio layout

All blueprints are scanned PDFs in `Seacove/25 Seacove Blueprints/`.

---

## ARC — The Pipeline Tool

ARC is a Python CLI tool that reads blueprints and generates SketchUp Ruby scripts. It is NOT a web app and does not follow the Flask/PostgreSQL pattern used by Canary and Cove.

**Pipeline stages:**
```
arc ingest    — normalize inputs (PDFs, photos, descriptions)
arc extract   — vision AI reads dimensions from blueprints
arc model     — build spatial model from extractions
arc validate  — check model consistency
arc generate  — produce SketchUp Ruby scripts
```

**Key constraints:**
- No MCP, no memory bus, no Linear dispatch, no Flask
- File-based I/O (JSON spatial models, .rb output)
- Can use Ollama for vision and embeddings
- Everything stays inside `Seacove/`

**Core files:**
- `arc/model/spatial_model.py` — core data structure
- `templates/ruby/*.rb.j2` — Ruby code generation templates
- `25-Seacove-As-Built.rb` — generated SketchUp script
- `25-Seacove-As-Built-Model.jsx` — alternative format

---

## RPV Permit Architect Plugin

The `rpv-permit-architect.plugin` provides skills for navigating blueprints, understanding RPV building codes, planning drawing sets for permit submission, translating blueprints to SketchUp, cost estimating, and tracking project history through multiple permit cycles.

---

## Relationship to Cove

Seacove is standalone — not connected to platform infrastructure. However, the property is within WPBCA Tract 14649, so Cove's parcel data, CC&R research, and community governance all apply. The survey source files (field books, tract maps, assessor maps) that were in Brain's inbox have been archived to `Cove/docs/archive/originals/` since they serve both projects.

## Related
- [[Brain/projects/Cove|Cove]] — WPBCA governance (same tract)
- [[Brain/wiki/cove-property-geology|Property & Geology]] — landslide context
