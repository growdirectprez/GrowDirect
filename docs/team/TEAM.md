# GrowDirect Agent Topology

## Hierarchy

```
Jeffe (CEO)
  ↕  conversation — ideation, decisions, direction
ALX (COO)
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

## Roles

| Role | Identity | Profile | Scope |
|------|----------|---------|-------|
| CEO / Founder | Jeffe | [Jeffe.md](Jeffe.md) | Product vision, scope, final approval. Real person. |
| COO / Lead Agent | ALX | [ALX.md](ALX.md) | Sole conversational interface. Roadmap, business ops, ideation, dispatch. |
| Canary Builder | (headless) | — | Canary codebase. Picks up GRO issues, runs factory pipeline. |
| Cove Builder | (headless) | — | Cove codebase. Picks up GRO issues, runs factory pipeline. |

## Functional Roles (Factory Pipeline)

These roles are performed by builders as part of the factory process — they are not separate agents.

| Function | Performed By | Scope |
|----------|-------------|-------|
| Engineering | Builders | All production code, database, APIs |
| QA | Builders (verify + qa stages) | Test scenarios, compliance verification |
| Architecture | Builders (blueprint stage) | Data models, process maps, domain architecture |
| Research | Builders (research stage) | Legal research, domain methodology, legislative tracking |
| Documentation | Builders (close stage) | SDDs, post-mortems, session summaries |

## App Coverage

| App | Builder | Domain |
|-----|---------|--------|
| Canary | Canary builder | Retail loss prevention for Square merchants |
| Cove | Cove builder | HOA governance, Davis-Stirling compliance, secret ballot voting |

## Factory Process

All development follows nine stages in order: Preflight → Research → Blueprint → TDD → Assembly → Verify → QA → Ship → Close.
No issue = no work. GRO number = exact scope.

## Key Constraints (Platform-Wide)

- No SQLite — PostgreSQL only
- No CDN dependencies — all JS/CSS via npm
- No work without a Linear GRO issue
- No file creation without cause — edit the original
- UUID primary keys on every table
- QA stage gate is absolute — nothing ships without passing
