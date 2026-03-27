# GrowDirect Team Registry

Role registry for GrowDirect's agent team and human leadership. All agent profiles are operational — not bios.

| Role | Name | Profile | Apps | Function |
|------|------|---------|------|----------|
| CEO / Founder | Jeffe | [Jeffe.md](Jeffe.md) | All | Product vision, scope, final approval. Real person. |
| COO / Lead Agent (Canary) | ALX | [ALX.md](ALX.md) | Canary + Platform | Roadmap, business ops, Canary codebase |
| Lead Agent (Cove) | SYD | [SYD.md](SYD.md) | Cove | Cove codebase, HOA governance, factory process |
| Lead Engineer | Jeremy | [Jeremy.md](Jeremy.md) | Canary + Cove | All production code, database, APIs |
| Program Manager | Eva | [Eva.md](Eva.md) | Canary + Cove | Sprint planning, factory gates, release readiness |
| Legal Counsel | Legal | [Legal.md](Legal.md) | Canary + Cove | IP, corporate, regulatory, Davis-Stirling (Cove) |
| UX/Creative Director | Art | [Art.md](Art.md) | Canary + Cove | UX design, wireframes, component library, accessibility |
| QA Manager | Jim | [Jim.md](Jim.md) | Canary + Cove | Test scenarios, UAT sign-off, compliance verification |
| Systems Architect | Tom | [Tom.md](Tom.md) | Canary + Cove | Data models, process maps, domain architecture |
| Research Director | PhD | [PhD.md](PhD.md) | Canary + Cove | Legal research, domain methodology, legislative tracking |

## App Coverage

| App | Lead Agent | Domain |
|-----|-----------|--------|
| Canary | ALX | Retail loss prevention for Square merchants |
| Cove | SYD | HOA governance, Davis-Stirling compliance, secret ballot voting |

## Factory Process

All development follows six stages in order: Blueprint → TDD → Assembly → Verify → QA → Ship.
No issue = no work. GRO number = exact scope.

## Key Constraints (Platform-Wide)

- No SQLite — PostgreSQL only
- No CDN dependencies — all JS/CSS via npm
- No work without a Linear GRO issue
- No file creation without cause — edit the original
- UUID primary keys on every table
- Jim's QA veto is absolute — nothing ships without sign-off
