---
classification: confidential
owner: GrowDirect LLC
date: 2026-04-21
type: wiki
tags: [method, commdocs, sdds, briefs, growdirect-method]
sources: []
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Method › Communication Documents

Cross-agent and client-facing artifact structures. CommDocs are the **communication layer** — they describe what happens to other roles, to stakeholders, or to future sessions.

Distinct from Work Products in that:
- WPs are internal deliverables (plans, intake notes, wiki articles).
- CommDocs are shared artifacts (SDDs, briefs, handoffs) with a defined audience.

## SDDs (Subsystem Design Documents)

`docs/sdds/<app>/<subsystem>.md` — the canonical cross-agent description of a platform subsystem. Every major subsystem has an SDD.

**Audience:** any agent or operator who needs to understand / modify / depend on the subsystem.

**Structure (standard):**
- Header — status, type, namespace, code location, companion, wiki links, related
- Purpose — what it does
- Dependencies — what it requires, startup order, blast radius
- Data Flow — including PII classification
- Operations — how it runs day-to-day
- (subsystem-specific sections)

**Current Canary SDDs:** [[docs/sdds/canary/platform-overview|Platform Overview]], [[docs/sdds/canary/architecture|Architecture]], [[docs/sdds/canary/data-model|Data Model]], [[docs/sdds/canary/identity|Identity]], [[docs/sdds/canary/tsp|TSP Pipeline]], [[docs/sdds/canary/chirp|Chirp Detection]], [[docs/sdds/canary/fox|Fox Cases]], [[docs/sdds/canary/owl|Owl Analytics]], [[docs/sdds/canary/goose|Goose]], [[docs/sdds/canary/raas|RaaS]], [[docs/sdds/canary/alx|ALX Agent]], [[docs/sdds/canary/qa-agent|QA Agent]], plus TSP subs 1–4, webhook-pipeline, metrics-analytics, analytics, ops, ui-bff.

**Current platform SDDs:** [[docs/sdds/platform/factory-pipeline|Factory Pipeline]], [[docs/sdds/platform/skill-architecture|Skill Architecture]], [[docs/sdds/platform/memory-bus|Memory Bus]], [[docs/sdds/platform/shared-infrastructure|Shared Infrastructure]], [[docs/sdds/platform/aws-target-architecture|AWS Target Architecture]].

## Design specs (`docs/superpowers/specs/`)

Per-sprint design artifacts produced by `superpowers:brainstorming`. Spec is the upstream of a plan.

**Audience:** the agent who'll write the plan + any reviewer.

**Structure:**
- Frontmatter — title, date, project, related, status
- Problem — what + why now
- Goal — what success looks like
- Scope — in / out
- Design — by subsystem
- Success criteria
- Risks + unknowns
- Non-goals / explicit deferrals
- Open questions

## Working briefs (`docs/superpowers/briefs/`)

Sprint-close synthesis artifacts. Not wiki (too in-flight), not plans (backward-looking).

**Audience:** the roles who'll act on the recommendations.

**Structure:**
- Purpose — why this brief exists
- Findings — what was learned
- Recommendations — tagged ADOPT / ADAPT / REJECT with source citations
- Follow-up Linear issues to file

Example: [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]] (10 patterns).

## Plans (`docs/superpowers/plans/`)

Executable sprint plans produced by `superpowers:writing-plans`.

**Audience:** executing agent(s). Designed for "implementer has zero context for this codebase."

**Structure:** Goal / Architecture / Tech Stack / Chunks (each with Files, Steps, Verification, Commit boundaries).

## Handoff documents (ad-hoc)

When work transfers between roles / sessions, a handoff document captures the transition. Not strictly templated today. Candidate for Sprint B.

Typical contents:
- What was accomplished
- What's outstanding
- Known issues / blockers
- Context for next agent

## Postmortems (planned — not yet templated)

Skill `factory-postmortem` exists but no standard template lives in Brain. Sprint C candidate.

## What's missing

- `author-role:` frontmatter on SDDs (which role owns the doc)
- `audience:` frontmatter on briefs (who should read)
- Explicit handoff template in `Brain/templates/`
- Postmortem template

## Related

- [[Brain/projects/Method|Method MOC]]
- [[Brain/projects/Factory|Factory Pipeline]]
- [[Brain/method/WorkProducts|Method › Work Products]] — internal deliverables (vs these cross-agent communications)
- [[Brain/method/Roles|Method › Roles]] — who authors / receives which CommDoc
