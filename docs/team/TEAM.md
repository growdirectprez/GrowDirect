# GrowDirect Agent Topology

## Hierarchy

```
Jeffe (CEO) — real person, not an agent, not in the Factory pipeline
  ↕  conversation — ideation, decisions, direction
ALX (COO) — sole conversational interface
  ↕  dispatch — GRO issues, factory stages, status rollups
  ├── Canary builder (headless, no persona)
  ├── Cove builder (headless, no persona)
  └── Future app builders (same pattern)
```

## Rules

- Jeffe talks to ALX only. Never directly to a builder.
- ALX defaults to ideation mode in Cowork. Only enters dispatch mode on explicit "build this" / "ship this."
- Builders are Claude Code sessions that read their GRO issue and execute the factory pipeline. They post results to Linear. ALX monitors.
- Linear is the message bus between ALX and builders.

## Roster

All profiles live in `docs/team/`. After the 2026-04 rename, team-member names are dropped in favor of functional role names — except **ALX** (agent identity) and **PhD** (analyst on staff). Jeffe is the real person behind the team.

### Real people

| Role | File | Scope |
|------|------|-------|
| CEO / Founder | [Jeffe.md](Jeffe.md) | Product vision, scope, final approval. Real person. **Not in the Factory pipeline.** |

### Factory-pipeline roles (operators)

| Role | File | Primary stage | Scope |
|------|------|---------------|-------|
| ALX | [ALX.md](ALX.md) | Preflight, Close, orchestration | COO / Lead Agent. Sole conversational interface. Roadmap, business ops, ideation, dispatch. |
| Architect | [Architect.md](Architect.md) | Blueprint | Data models, process maps, domain architecture, SDDs. |
| Engineer | [Engineer.md](Engineer.md) | TDD, Assembly, Verify, Ship | All production code, database, APIs, tests, deploys. |
| ProgramManager | [ProgramManager.md](ProgramManager.md) | Preflight + Close (assist) | Sprint planning, release gates, roadmap dependencies. |
| Writer | [Writer.md](Writer.md) | Research + Close (assist), all-stages gate | Documentation, docs-with-code, SDD formatting, wiki. |
| UX | [UX.md](UX.md) | Assembly + QA (assist) | Wireframes, component library, interaction flows, accessibility. |
| QA | [QA.md](QA.md) | Verify + QA (assist), UAT gate | Test scenarios, UAT, production readiness. |
| Compliance | [Compliance.md](Compliance.md) | QA (primary) | Regulated content, audit packages, boundary crossings, SOC/SOX. |
| DevOps | [DevOps.md](DevOps.md) | Verify + Ship (assist) | CI/CD pipeline, deploy automation, infra. |
| Legal | [Legal.md](Legal.md) | Preflight + QA (gate) | IP, contracts, Davis-Stirling, press. |

### Advisors + analysts

| Role | File | Scope |
|------|------|-------|
| PhD | [PhD.md](PhD.md) | Analyst on staff — research methodology, Canary theoretical foundation, Cove legal research, detection scoring rigor. Factory Research stage primary runner. |

### Deprecated

| Name | File | Status |
|------|------|--------|
| SYD | [SYD.md](SYD.md) | Deprecated (GRO-377). Persona removed. File kept as Cove Builder operational description (headless factory executor). |
| Condor | [Condor.md](Condor.md) | Redirect to [[Cove/docs/voices/Condor|Cove Voices › Condor]] — now a narrator voice spec for abalonecove.org, not a team role. |

### App builders (headless)

| Builder | Driven by | Scope |
|---------|-----------|-------|
| Canary builder | Engineer role, factory pipeline | Canary codebase. Picks up GRO issues, runs factory. |
| Cove builder | Engineer role, factory pipeline | Cove codebase. Davis-Stirling compliance mandatory. |
| Angel builder | Engineer role, factory pipeline | Angel codebase. RE intelligence, Compass tools. |

## Functional Roles in the Factory Pipeline

Each stage is performed by the role(s) listed. See [[Brain/projects/Factory|Factory MOC]] for the full stages × roles × skills × work products matrix.

| Function | Stage | Primary Role | Assist |
|----------|-------|--------------|--------|
| Orchestration | Preflight, Close | ALX | ProgramManager |
| Research | Research | PhD | Architect, Writer |
| Architecture | Blueprint | Architect | ALX, Writer |
| Engineering | TDD, Assembly, Verify, Ship | Engineer | Architect, DevOps |
| Documentation | all stages (gate) | Writer | Architect, Engineer |
| UX | Assembly, QA | UX | — |
| QA | Verify, QA, UAT | QA | ProgramManager, Compliance |
| Compliance | QA (gate) | Compliance | Legal |
| Legal | Preflight + QA (gate) | Legal | Compliance |
| DevOps | Verify, Ship | DevOps | Engineer |

## App Coverage

| App | Builder | Domain |
|-----|---------|--------|
| Canary | Canary builder | Retail loss prevention for Square merchants |
| Cove | Cove builder | HOA governance, Davis-Stirling compliance, secret ballot voting |
| Angel | Angel builder | Real estate intelligence, Compass tools, APN-driven lead gen |

## Factory Process

All development follows nine stages in order: Preflight → Research → Blueprint → TDD → Assembly → Verify → QA → Ship → Close.
No issue = no work. GRO number = exact scope.

See [[Brain/projects/Factory|Factory MOC]] for the full operational spec.

## Key Constraints (Platform-Wide)

- No SQLite — PostgreSQL only
- No CDN dependencies — all JS/CSS via npm
- No work without a Linear GRO issue
- No file creation without cause — edit the original
- UUID primary keys on every table
- QA stage gate is absolute — nothing ships without passing

## Role names: where they came from

Before 2026-04-22, roles were named after team members (Tom, Jeremy, Eva, Jess, Art, Jim, Research, Owl). After the rename:

- Named → functional: Tom → Architect, Jeremy → Engineer, Eva → ProgramManager, Jess → Writer, Art → UX, Jim → QA, Research → merged into PhD
- Kept: ALX (agent identity), PhD (analyst on staff), Jeffe (real person), Legal, Compliance, DevOps
- Dropped: Owl (the role profile — Owl is a Canary product system at `Canary/canary/services/owl/`, not a team role; see [[docs/sdds/canary/owl|Canary Owl SDD]])
- Redirected: Condor (to Cove narrator voice spec, see [[Cove/docs/voices/Condor|Cove Voices › Condor]]; the product service `canary-condor` is unrelated)
- Deprecated: SYD (renamed internally to Cove Builder headless factory executor, GRO-377)
