---
date: 2026-04-21
type: wiki
tags: [method, roles, agent-team, growdirect-method]
sources: []
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Method › Roles

Index of GrowDirect roles — the agent team that runs the Factory pipeline and cross-disciplinary work. Each role has a profile at `Canary/docs/profiles/ops/*.md` that captures identity, responsibilities, and tooling.

## Orchestration

- [[Canary/docs/profiles/ops/ALX|ALX]] — Orchestrator / Program Manager. Runs the Factory from preflight through close. Coordinates the team. Primary owner of session protocol + Linear workflow.

## Core delivery

- [[Canary/docs/profiles/ops/Tom|Tom]] — Architecture. Owns blueprint stage; decides how things get built. Designs SDDs; reviews plans.
- [[Canary/docs/profiles/ops/Jeremy|Jeremy]] — Build + DevOps. TDD, Assembly, Verify, Ship. Owns the deploy pipeline, shared Docker infra, migrations.
- [[Canary/docs/profiles/ops/Eva|Eva]] — Program Management. Tracks cycles, preflight coordination, timelog capture, cost tracking.
- [[Canary/docs/profiles/ops/Jess|Jess]] — Documentation. SDDs, runbooks, onboarding, Brain wiki upkeep.

## Product + UX

- [[Canary/docs/profiles/ops/Art|Art]] — UX / Creative. Design decisions, brand execution, UI review.
- [[Canary/docs/profiles/ops/Owl|Owl]] — Product AI. MCP servers, agent composition, Ollama workloads, embeddings.
- [[Canary/docs/profiles/ops/Jim|Jim]] — Customer sentiment + QA. Uses the product the way a merchant would; flags friction; runs UAT.

## Research + context

- [[Canary/docs/profiles/ops/Research|Research]] — Context gathering. Research-stage owner; prior-art recall; competitive scan.

## Gates + oversight

- [[Canary/docs/profiles/ops/Compliance|Compliance]] — QA gate. Standards enforcement, data handling, RLS, audit trail.
- [[Canary/docs/profiles/ops/Legal|Legal]] — Legal gate. Contracts, NDAs, privacy, IP.
- [[Canary/docs/profiles/ops/DevOps|DevOps]] — Infrastructure gate. Ship stage review, infra cost, security.

## Role → Factory stage affinity

| Stage | Primary | Assist |
|---|---|---|
| 1. Preflight | ALX | Eva, Jeremy |
| 2. Research | Research | Tom, Jess |
| 3. Blueprint | Tom | ALX, Eva |
| 4. TDD | Jeremy | Tom |
| 5. Assembly | Jeremy | Tom, Art |
| 6. Verify | Jeremy | Jim |
| 7. QA | Compliance | Legal, Art |
| 8. Ship | Jeremy | DevOps |
| 9. Close | ALX | Eva, Jess |

(Same matrix as [[Brain/projects/Factory|Factory MOC]] — duplicated here for role-first navigation.)

## Role coverage across domains

Not every role runs every model. Common affinities:

- **Factory pipeline** — all roles (see matrix above)
- **Superpowers workflow** — ALX, Tom (brainstorm/plan), Jeremy (execute)
- **Brand-voice** — Art primary; Jess + Eva assist
- **Legal** — Legal primary
- **Marketing** — Art + Jess + (external marketing role, TBD)
- **Enterprise search** — any role (it's a general tool)

## What's missing

Sprint B (pending) adds to each role profile:

- **Produces** — specific WPDs (plans, SDDs, briefs, wiki articles, commits) this role authors
- **Uses** — specific skills this role invokes most
- **Performs** — Linear issue types / labels / projects this role owns

Today the profiles are free-form prose. After Sprint B, they're queryable nodes in the method graph.

## Related

- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Factory|Factory Pipeline]] — stage-by-role matrix
- [[Brain/method/Techniques|Method › Techniques]] — the skill catalog each role draws from
- [[Brain/method/Activities|Method › Activities]] — Linear views per role
