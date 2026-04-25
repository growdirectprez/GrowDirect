---
classification: confidential
owner: GrowDirect LLC
date: 2026-04-21
type: wiki
tags: [method, work-products, templates, wpd, growdirect-method]
sources: []
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Method › Work Products

Deliverable templates. A **Work Product (WP)** is a typed artifact an agent produces in the course of work. A **Work Product Descriptor (WPD)** is the template + structure spec for that artifact.

## Brain templates (`Brain/templates/`)

- [[Brain/templates/wiki-article|wiki-article]] — standard wiki format (frontmatter: date, type, tags, sources, last-compiled, needs-review; sections: Summary, Details, Related, Sources)
- [[Brain/templates/raw-intake|raw-intake]] — `Brain/raw/inbox/` intake note format (source, raw content, key takeaways, links to existing knowledge)
- [[Brain/templates/card|card]] — atomic knowledge card (claim + evidence + context)
- [[Brain/templates/claim|claim]] — a specific claim with evidence / counter-evidence
- [[Brain/templates/decision|decision]] — ADR-style decision record
- [[Brain/templates/meeting|meeting]] — meeting notes template
- [[Brain/templates/daily-note|daily-note]] — day-level log

## docs/ templates (superpowers workflow)

- **Spec** — `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` — produced by `superpowers:brainstorming`. Structure: Problem / Goal / Scope / Design / Success Criteria / Risks / Non-goals.
- **Plan** — `docs/superpowers/plans/YYYY-MM-DD-<topic>.md` — produced by `superpowers:writing-plans`. Structure: Goal / Architecture / Tech Stack / Chunks of Tasks (each with Files / Steps / Verification).
- **Brief** — `docs/superpowers/briefs/YYYY-MM-<topic>.md` — produced at the close of a sprint. Structure: Purpose / Findings / Recommendations / Follow-ups.

## Canary / app SDDs (`docs/sdds/<app>/`)

SDD = Subsystem Design Document. Each major subsystem has one. Structure convention:

- Header — Status, Type, Namespace, Code location, Companion, Wiki links, Related
- Purpose
- Dependencies
- Data Flow (with PII notes)
- Operations
- Failure modes
- (App-specific sections)

Examples: [[docs/sdds/canary/platform-overview|Platform Overview]], [[docs/sdds/canary/architecture|Architecture]], [[docs/sdds/canary/data-model|Data Model]], [[docs/sdds/canary/tsp|TSP Pipeline]], [[docs/sdds/platform/factory-pipeline|Factory Pipeline]].

## Linear issue (intake)

Linear GRO issues are the formal Activity container. Convention:

- Title — short imperative (`Add X`, `Fix Y`, `Investigate Z`)
- Description — user-facing problem statement
- Labels — project (Canary / Cove / Angel / Platform), layer (infra / app / protocol / legal / business)
- Priority — Urgent / High / Medium / Low
- Sub-issues for multi-task work
- Cycle assignment for time-boxed batches

No Linear template file lives in Brain today. Candidate for Sprint C — add `Brain/templates/linear-issue.md` describing the fields + conventions.

## Session artifacts (per-stage Factory outputs)

These live in git + Linear, not Brain. Their **formats** are defined in stage skills:

- `preflight_report` — `factory-preflight` skill output
- `context_bundle` — `factory-research` skill output
- Plan — see "Plan" above
- `verify_report` — `factory-verify` skill output
- `qa_report` — `factory-qa` skill output
- `session_summary` — `factory-close` skill output

## Wiki articles (`Brain/wiki/`)

The persistent domain knowledge layer. Each wiki article is a Work Product with a stable identity. Frontmatter schema enforced by `engine.py lint`: `last-compiled`, `needs-review` required.

## Project MOCs (`Brain/projects/`)

Navigation hubs per project. Current: Angel, Canary, Cove, Factory, Method, Seacove, Secure.

## What's missing

Sprint C (pending) adds to each WP template:

- `stage:` — which Factory stage produces this WP (if any)
- `role:` — which role authors this WP
- `upstream:` — WPs consumed to produce this one
- `downstream:` — WPs this one feeds into

Today the template frontmatter is schema-minimal. After Sprint C, the template itself encodes its place in the method graph.

## Related

- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Factory|Factory Pipeline]] — stage outputs
- [[Brain/method/Roles|Method › Roles]] — who authors which WP
- [[Brain/method/Techniques|Method › Techniques]] — which skills produce which WP
