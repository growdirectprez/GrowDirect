---
classification: confidential
owner: GrowDirect LLC
date: 2026-04-22
type: wiki
tags: [method, orchestration, platform, mcp, claude, linear, obsidian]
sources: [CLAUDE.md, Brain/wiki/growdirect-workflow.md, Brain/projects/Method.md, docs/sdds/platform/skill-architecture.md]
last-compiled: 2026-04-22
needs-review: 2026-05-06
method-role: Writer
method-stage: close
---

**Wiki:** [[Brain/Home|Home]] · [[Brain/projects/Method|Method MOC]]

# Method › Orchestration

The GrowDirect method described in terms of the stack that runs it. The [[Brain/projects/Method|MOC]] catalogs the structure — Models, Roles, Techniques, Work Products, Activities, CommDocs. This article describes what's actually happening when those categories operate: Claude as the dispatcher, MCP as the connective tissue, Linear as the activity system, Obsidian as the knowledge graph.

## The stack

Three substrates and one dispatcher.

The **dispatcher** is Claude, running in two surfaces. Cowork — a desktop surface for strategy, writing, operations, and anything touching SaaS systems of record. Claude Code — a terminal surface for building software, running tests, editing the repo, managing Docker. Both read the same rules file (`CLAUDE.md`) and the same knowledge graph (`Brain/`). They can tag-team work without a meeting because they share context, not conversation.

The three substrates underneath:

- **Linear** — the activity layer. Every unit of work is a `GRO-` issue. Sprints, priorities, ownership, state.
- **Obsidian vault** (`Brain/`) — the knowledge layer. Plain markdown in git, wiki-linked, topic-indexed. Vendor-portable by construction.
- **Code repositories** — the execution layer. Four product trees plus shared infrastructure.

**MCP (Model Context Protocol)** is the glue. An open standard for exposing tools and data to an AI agent through one interface. Linear, Gmail, Figma, Canva, a memory bus, a vector-indexed legal store — all MCP endpoints the agent calls the same way it reads a file. New SaaS means a new connector, not a new integration project.

## How a session runs

A session — Cowork or Code — loads context from three places, in order:

1. `CLAUDE.md` — the non-negotiable rulebook. Tech stack, code standards, session discipline. Short by design.
2. Brain — the project MOC and the wiki articles the task references. A registry (`REGISTRY.json`) lets the agent check "do we already cover this?" before creating new notes.
3. Linear — the issues the session is scoped to. Each issue names its deliverable and what "done" looks like.

The agent then dispatches to **skills** — executable playbooks in plugins (brand-voice, legal, marketing, engineering, enterprise-search, project-specific factories). A skill isn't documentation about how to do something; it's a runnable workflow. Skills compose — one skill can invoke another. Institutional know-how becomes a callable API.

At close, outputs route to their natural home: code to the repo, tasks to Linear, knowledge to Brain. A content engine handles the knowledge leg — ingest, registry update, template enforcement — so the graph stays queryable instead of decaying into a landfill.

## Why it holds together

Four properties do most of the work.

**Activity and knowledge are separated on purpose.** Linear answers "what needs to happen." Obsidian answers "what do we know." Tools that try to be both — wikis with task plugins, trackers with document features — leave tasks with buried context and docs with stale priorities. Keeping the layers apart lets each stay good at its job and lets the agent route between them cleanly.

**Markdown is the knowledge substrate.** Plain files in git, wiki-linked. Not a SaaS, not a database. That trades interface polish for portability, agent-readability, and durability. The agent reads, edits, and links across it without a vendor SDK. Exit cost is zero.

**MCP is the integration layer, not bespoke code.** Most integration debt is glue between two tools. Putting an agent in the middle with MCP to both, the glue becomes a prompt plus a skill. Swapping a vendor is swapping a connector.

**Skills are versioned playbooks.** A legal NDA triage, a marketing brief, a factory pipeline stage — each a file the agent loads, runs, composes. Domain expertise ships the way code ships: reviewed, versioned, diffable, reusable. It doesn't walk out the door.

## Domain independence

GrowDirect runs four products that share nothing domain-wise: loss-prevention analytics on Square POS data, HOA governance, real estate intelligence, construction documents. One orchestration shape, four domains. The pattern isn't tied to the solo-founder scale either — the coordination it absorbs (many concurrent initiatives, many systems of record, operational knowledge that needs to stay fresh) is a bigger problem at enterprise scale, not a smaller one. Activity layer, knowledge layer, and orchestrator stay the same; what fills each slot is whatever the organization already runs.

## What it costs

Honest limits.

Sessions don't share memory natively. Cowork and Claude Code each start fresh. The bridge is the knowledge graph and the activity tracker — not a shared scratchpad. That forces explicit handoffs. It's a feature, but it costs effort.

Agent quality tracks tool and context curation. Badly scoped MCP access or a stale knowledge graph drops output quality fast. The agent is only as good as what it can reach and what it's told to care about.

Markdown requires discipline. Templates, a registry, naming conventions. Without them, the graph becomes unfindable and the agent picks up garbage.

The bridge is the hard engineering problem. Not the agent, not the connectors — the curation layer that keeps knowledge current and typed. GrowDirect runs a lightweight content engine for that. At larger scale it's a staffed function or a vendor, not an afterthought.

## Fit

Three or more distinct domains with their own expertise. A mix of systems of record no one wants to rewrite. Operational knowledge that's already an asset but hard to keep current. In that shape, this pattern is a force multiplier on the tools already in place. In a shape where everything wants to live in one suite, it's not the argument against consolidation.

## Related

- [[Brain/projects/Method|Method MOC]] — the structural catalog this article describes
- [[Brain/wiki/growdirect-workflow|GrowDirect Workflow]] — the inward operating manual (session lifecycle, anti-patterns)
- [[Brain/projects/Factory|Factory Pipeline]] — the dominant model running on this stack
- [[Brain/method/Models|Method › Models]] — other models running on the same stack
- [[Brain/method/Techniques|Method › Techniques]] — the skills catalog
- [[docs/sdds/platform/skill-architecture|Skill Architecture SDD]] — how skills compose
- [[docs/sdds/platform/memory-bus|Memory Bus SDD]] — Claude Code-side persistence

## Sources

- `CLAUDE.md` — platform rules, tech stack, knowledge architecture
- `Brain/wiki/growdirect-workflow.md` — internal operating manual
- `Brain/projects/Method.md` — method MOC
- `docs/sdds/platform/skill-architecture.md` — skill composition model
- Model Context Protocol — public standard for agent-tool interfaces
