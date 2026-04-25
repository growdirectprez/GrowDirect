---
classification: confidential
owner: GrowDirect LLC
date: 2026-04-21
type: wiki
tags: [method, activities, linear, gro, growdirect-method]
sources: []
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Method › Activities

Live work. **Activities are tracked in Linear, not in Brain.** This page is the index to Linear views + conventions. Do not duplicate issue state here — it goes stale.

## Linear workspace

- Workspace: [GrowDirect](https://linear.app/growdirect)
- Team key: `GRO`
- MCP connector: Full read/write via Cowork / Claude Code
- Projects (current, from PROJECT_MANIFEST v2.0):
  - **Canary LP** — Urgent, In Progress. AI-powered loss prevention for Square merchants.
  - **Beta Launch Infrastructure** — High, Planned. AWS, Terraform, ECS, RDS, landing page.
  - **elJeffe Protocol** — Medium, Planned. Bitcoin Ordinals + Avalanche namespace. Confidential.
  - **Owl & AI Modules** — Medium, Planned. MCP-connected AI advisor modules.
  - **GrowDirect Operations** — Medium, Planned. Billing, dogfood loop, SEO, internal tools.

## Issue labels (for filtering)

Layer labels used across projects:
- `Canary App` — app-layer Canary work
- `Infra` — shared infrastructure (Docker, Postgres, Valkey, Ollama, memory bus)
- `Protocol` — elJeffe / Bitcoin / ordinals
- `Legal` — legal work
- `Business` — revenue, ops, billing
- `Platform` — cross-app platform work

## Activity views per role

Recommended Linear saved views (Sprint B will codify these in the role profiles):

| Role | View filter |
|---|---|
| [[Canary/docs/profiles/ops/ALX\|ALX]] | All GRO issues by priority; cycle-aligned; unassigned triage |
| [[Canary/docs/profiles/ops/Tom\|Tom]] | Label=Platform OR Canary App; type=Architecture/Design |
| [[Canary/docs/profiles/ops/Jeremy\|Jeremy]] | Label=Infra OR Canary App; status=In Progress / Ready |
| [[Canary/docs/profiles/ops/Eva\|Eva]] | All issues; grouped by cycle; status overview |
| [[Canary/docs/profiles/ops/Jess\|Jess]] | Labels include doc updates; SDD / runbook work |
| [[Canary/docs/profiles/ops/Compliance\|Compliance]] | Type=QA / Standards / Audit |
| [[Canary/docs/profiles/ops/Legal\|Legal]] | Label=Legal |
| [[Canary/docs/profiles/ops/DevOps\|DevOps]] | Label=Infra; deploy + shared infra work |
| [[Canary/docs/profiles/ops/Art\|Art]] | Type=UX / Design / Brand |
| [[Canary/docs/profiles/ops/Jim\|Jim]] | Type=UAT / Customer feedback |
| [[Canary/docs/profiles/ops/Owl\|Owl]] | Label=AI / MCP |
| [[Canary/docs/profiles/ops/Research\|Research]] | Label=Research OR context-gathering |

## Conventions

- **One GRO issue per discrete deliverable.** Not one per task — break tasks into sub-issues.
- **Plans live in `docs/superpowers/plans/` + linked from the issue.** Don't paste plan content into Linear descriptions; link to the plan file.
- **Status transitions** via the factory pipeline: Todo → In Progress (preflight) → In Review (qa) → Done (ship).
- **Cycles** = sprints. Typical cycle = 1-2 weeks.
- **Sub-issues** for multi-task work so each sub-issue gets its own Factory run.

## What's missing

- **Linear-issue template in Brain/templates/** — Sprint C candidate. Fields + convention doc.
- **Role → saved-view-ID mapping** — once saved views exist in Linear, capture their IDs/URLs here so the table above becomes clickable.
- **Activity analytics** — throughput per role, cycle velocity. Not yet instrumented.

## Related

- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Factory|Factory Pipeline]] — stages produce GRO issues and consume them
- [[Brain/method/Roles|Method › Roles]] — role-owned work
- [[docs/_archive/ip-vault/PROJECT_MANIFEST|ALX Project Manifest v2.0]] — historical manifest (archived)
