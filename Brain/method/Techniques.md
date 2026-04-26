---
classification: confidential
owner: GrowDirect LLC
date: 2026-04-21
type: wiki
tags: [method, techniques, skills, plugins, growdirect-method]
sources: []
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Method › Techniques

The skill catalog. Every skill is an **executable technique** — not documentation *about* how to do something, but a runnable workflow that produces an output.

Invoked via `Skill` tool in Claude Code / Cowork sessions.

## Platform factory skills (`.claude/skills/factory-*`)

Stage implementations for the [[Brain/projects/Factory|Factory Pipeline]]:

- `factory-preflight` — preflight stage contract
- `factory-research` — research stage
- `factory-blueprint` — blueprint stage
- `factory-assembly` — assembly stage
- `factory-qa` — QA stage
- `factory-ship` — ship stage
- `factory-close` — close stage
- `factory-linear` — Linear MCP operations across stages
- `factory-newapp` — scaffolding for a new app
- `factory-postmortem` — incident aftermath

## App-specific factory skills

- **Canary** (`.claude/skills/canary-*`) — preflight, blueprint, tdd, assembly, verify, qa, ship, close, plus extensions: data-expansion, debug, deploy, review, scenario, uat
- **Cove** (`.claude/skills/cove-*`) — archive (only one today; other stages pending)

## superpowers — process discipline

Process skills — determine HOW work happens.

- `brainstorming` — explore ideas before building
- `writing-plans` — turn a spec into an executable plan
- `executing-plans` — run a plan in a dedicated session
- `subagent-driven-development` — same-session fresh-subagent-per-task execution
- `test-driven-development` — failing test → implement → pass → commit
- `systematic-debugging` — reproduce → isolate → diagnose → fix
- `verification-before-completion` — evidence before assertions
- `requesting-code-review` — structured review dispatch
- `receiving-code-review` — disciplined response to feedback
- `using-git-worktrees` — isolated workspaces
- `finishing-a-development-branch` — merge / PR / cleanup
- `dispatching-parallel-agents` — multiple independent tasks in parallel
- `writing-skills` — creating + editing skills themselves
- `using-superpowers` — skill-system primer

## engineering — implementation

- `architecture` — ADRs, system design decisions
- `system-design` — API design, data modeling, service boundaries
- `code-review` — PR/diff review checklist
- `debug` — structured debugging session
- `testing-strategy` — test planning + coverage
- `deploy-checklist` — pre-deployment verification
- `documentation` — technical writing (READMEs, runbooks, API docs)
- `tech-debt` — debt identification + prioritization
- `incident-response` — triage, communicate, postmortem
- `standup` — daily standup generation

## brand-voice

- `discover-brand` — search connected platforms for brand materials
- `generate-guidelines` — synthesize guidelines from documents / transcripts
- `enforce-voice` — apply guidelines to new content

## legal

- `review-contract` — clause-by-clause analysis against playbook
- `triage-nda` — GREEN / YELLOW / RED classification
- `compliance-check` — regulation mapping + required approvals
- `legal-response` — templated response generation
- `legal-risk-assessment` — severity × likelihood classification
- `signature-request` — e-signature routing
- `vendor-check` — consolidated vendor agreement status
- `meeting-briefing` — legal-relevant meeting prep
- `brief` — daily / topic / incident briefing

## marketing

- `campaign-plan` — full campaign brief with calendar
- `content-creation` / `draft-content` — blog, social, email, landing pages
- `email-sequence` — multi-email flows with timing + branching
- `brand-review` — voice + messaging compliance
- `competitive-brief` — positioning + messaging comparison
- `seo-audit` — keyword + content gap + technical audit
- `performance-report` — metrics + trends + recommendations

## enterprise-search

- `search` — multi-source query
- `digest` — daily / weekly activity digest
- `knowledge-synthesis` — deduplicated answers with attribution
- `search-strategy` — query decomposition + ranking
- `source-management` — MCP source inventory + priority

## anthropic-skills (document handling + meta)

- `pdf`, `docx`, `xlsx`, `pptx` — document format skills
- `schedule` — scheduled task creation
- `skill-creator` — build / optimize skills
- `consolidate-memory` — memory file hygiene
- `setup-cowork` — Cowork onboarding

## rpv-permit-architect

- `archive-navigator` — blueprint archive navigation
- `rpv-building-codes` — RPV-specific code reference
- `drawing-set-planner` — permit drawing set organization
- `project-history` — multi-phase permit timeline
- `cost-estimating` — rough cost estimates (RPV area)
- `sketchup-guide` — blueprint → SketchUp + LayOut

## claude-api

- `claude-api` — Anthropic SDK best practices, caching, model migration

## How skills compose

- **Process skills before implementation skills** — e.g., `brainstorming` before `frontend-design`.
- **Rigid skills (TDD, debugging) follow exactly.** Flexible skills (patterns) adapt principles.
- **User instructions override default behavior; skills override default behavior.**
- Skills can invoke other skills (a skill's SKILL.md can reference `@superpowers:brainstorming` etc.).

## What's missing

Sprint C (pending) adds `roles:` frontmatter to each skill, linking techniques to roles. Example:

```yaml
---
name: writing-plans
roles: [Tom, ALX]  # Tom primary (architecture), ALX assist (orchestration)
stage: blueprint
---
```

## Related

- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Factory|Factory Pipeline]] — which skills run at which stage
- [[Brain/method/Models|Method › Models]] — which skill chains constitute each model
- [[Brain/method/Roles|Method › Roles]] — who invokes which skills
- [[docs/sdds/platform/skill-architecture|Skill Architecture SDD]]
