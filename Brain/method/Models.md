---
date: 2026-04-21
type: wiki
tags: [method, models, factory, growdirect-method]
sources: []
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Method › Models

Index of the methods GrowDirect uses. A **model** is a repeatable top-level workflow — a sequence of stages with defined inputs, outputs, and roles. The Factory Pipeline is the dominant model for code work; other models serve other disciplines.

## Operational models

### [[Brain/projects/Factory|Factory Pipeline]] — 9 stages

`preflight → research → blueprint → tdd → assembly → verify → qa → ship → close`

The default code-work method. Every Linear GRO issue runs this shape. Full MOC at [[Brain/projects/Factory|Factory.md]].

## Process models (meta — how agents think about work)

### Superpowers workflow — 4 stages

`brainstorm → spec → plan → execute (+ review)`

Invoked via `superpowers:` skills. Drives the creative / design-judgment side of work. Brainstorming surfaces the idea, writing-plans formalizes it, executing-plans / subagent-driven-development runs it.

**Skills:** `superpowers:brainstorming` → `superpowers:writing-plans` → `superpowers:executing-plans` or `superpowers:subagent-driven-development`. Review via `superpowers:requesting-code-review` + `superpowers:receiving-code-review`. Worktree isolation via `superpowers:using-git-worktrees`. Completion via `superpowers:finishing-a-development-branch`.

### Debug workflow

`systematic-debugging → verification-before-completion`

Invoked when something breaks. Rigid discipline: reproduce → isolate → fix → verify.

## Domain models

### Brand-voice generation — 4 stages

`discover-brand → conversation-analysis → generate-guidelines → enforce-voice`

For building + applying brand guidelines.

**Skills:** `brand-voice:discover-brand`, `brand-voice:generate-guidelines`, `brand-voice:enforce-voice`.

### Legal triage — multi-model

- Contract review: `legal:review-contract`
- NDA triage: `legal:triage-nda` → GREEN/YELLOW/RED
- Compliance: `legal:compliance-check`
- Vendor check: `legal:vendor-check`
- Legal response templates: `legal:legal-response`
- Signature routing: `legal:signature-request`

### Marketing workflow — per-deliverable

Campaign planning, email sequences, content creation, competitive briefs, SEO audits, performance reports, brand reviews. Skills: `marketing:campaign-plan`, `marketing:email-sequence`, `marketing:content-creation`, `marketing:draft-content`, `marketing:brand-review`, `marketing:competitive-brief`, `marketing:seo-audit`, `marketing:performance-report`.

### Enterprise search + digest

`search → knowledge-synthesis → digest`

Invoked for cross-source information retrieval. Skills: `enterprise-search:search`, `enterprise-search:digest`, `enterprise-search:knowledge-synthesis`, `enterprise-search:search-strategy`, `enterprise-search:source-management`.

### Engineering-discipline models

Architecture decision records, system design, code review, testing strategy, incident response, tech debt tracking, standup, deploy checklist, documentation. Skills in the `engineering:` plugin.

### Domain specialists

- **RPV permit architect** — archive-navigator, rpv-building-codes, drawing-set-planner, project-history, cost-estimating, sketchup-guide
- **Anthropic skills** — pdf, docx, xlsx, pptx, schedule, skill-creator, setup-cowork, consolidate-memory
- **Claude API** — SDK best practices for Claude integrations

## When to invoke which model

| You're doing... | Use |
|---|---|
| Code work tied to a GRO issue | [[Brain/projects/Factory\|Factory Pipeline]] |
| Exploring an idea before building | `superpowers:brainstorming` |
| Writing a formal design | `superpowers:brainstorming` → `superpowers:writing-plans` |
| A bug or test failure | `superpowers:systematic-debugging` |
| Generating brand content | `brand-voice:*` chain |
| Legal triage | `legal:*` per document type |
| Marketing deliverable | `marketing:*` per channel |
| Cross-source info lookup | `enterprise-search:search` or `digest` |

## Related

- [[Brain/projects/Method|Method MOC]] — parent navigation
- [[Brain/method/Techniques|Method › Techniques]] — the skill catalog that implements these models
- [[Brain/method/Roles|Method › Roles]] — who runs which model
