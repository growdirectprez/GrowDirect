---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# ALX Project Manifest v2.0 — Local + Linear
*All operations run local. No iCloud dependency. Linear is the task layer.*

**Version:** 2.0
**Date:** March 19, 2026
**Breaking change:** _ALX/ retired. TRIAGE, HANDOFF, DISPATCH replaced by Linear.

---

## Operational Truth

| Function | Old (_ALX/) | New (Linear + Local) |
|---|---|---|
| Blocker tracking | TRIAGE.md | Linear: filter Urgent/High priority issues |
| Agent routing | HANDOFF.md | Linear: issue assignment + cycles |
| Task dispatch | DISPATCH.md | Linear: labels (Canary App, Infra, Protocol, Legal, Business) |
| Work orders | _ALX/WorkOrders/ | Linear: issues with sub-issues |
| Sprint tracking | Manual in markdown | Linear: Cycles |
| Archival | _ALX/archive/ | Linear: native issue history |

**Linear workspace:** [GrowDirect](https://linear.app/growdirect)
**Team key:** GRO
**MCP connector:** Full read/write via Cowork

---

## Agent Identity

**ALX.md** — Stable identity doc. Lives in Claude Project attachment. Only update when role or team structure changes.

---

## Local Filesystem

Root: `/Users/geofflyle/GrowDirect/`

| Directory | What | Notes |
|---|---|---|
| `Canary/` | Git repo — the product codebase | Local. Dev loop, tests, deploy. |
| `Company/` | Board, Brand, Team, Investors | Profiles, logos, decks. Reference. |
| `IP/` | Specs, research, workorders, warchest | Operational file artifacts |
| `IP/markdown/` | PRDs, ADRs, Guides, Strategy, Specs | Migrated from Canary_IP/Markdown/ |
| `IP/documents/` | Legal, White Papers, Sales, Technical | Migrated from Canary_IP/Documents/ |
| `IP/workorders/` | Work order files (historical) | New work orders → Linear issues |
| `IP/warchest/` | Research papers, published outputs | |
| `IP/specs/` | Technical specifications | |
| `IP/research/` | Research artifacts | |
| `IP/timelogs/` | Time tracking | |
| `docs/` | Deliverables (docx, xlsx, html, pdf) | Patent visuals, product guides, models |
| `PhD/` | Academic research papers | Thesis docs, position papers |

---

## Linear Projects

| Project | Priority | Status | Description |
|---|---|---|---|
| Canary LP | Urgent | In Progress | AI-powered loss prevention for Square merchants |
| Beta Launch Infrastructure | High | Planned | AWS, Terraform, ECS, RDS, landing page |
| elJeffe Protocol | Medium | Planned | Bitcoin Ordinals + Avalanche namespace. CONFIDENTIAL. |
| Owl & AI Modules | Medium | Planned | MCP-connected AI advisor modules |
| GrowDirect Operations | Medium | Planned | Billing, dogfood loop, SEO, internal tools |

---

## Session Protocol

1. ALX reads this manifest (stable — Project attachment)
2. ALX queries Linear for current blockers, priorities, assignments
3. No markdown files to read at session open — Linear IS the triage
4. File artifacts (specs, research, deliverables) live on local disk
5. New tasks → Linear issues. Not markdown work orders.

---

## What NOT to Do

- Do not read TRIAGE.md, HANDOFF.md, or DISPATCH.md — they no longer exist
- Do not write to _ALX/ — that directory is retired
- Do not reference iCloud paths — everything is local
- Do not create new WORKORDER_*.md files — create Linear issues instead

---

*This file versioned manually. Update when paths, team structure, or protocol changes.*
