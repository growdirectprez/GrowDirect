# SDD Build-Out — Full Platform Documentation Pass

> **Date:** 2026-03-30
> **Status:** Approved
> **Scope:** All 17 SDD stubs across 4 namespaces
> **Goal:** Produce canonical spec-quality SDDs from working code, audit for misplacements and duplication, update memory for GitNexus knowledge graph ingestion

---

## Context

GrowDirect has 18 files in `docs/sdds/`. One (`skill-architecture.md`) is a complete reference document — it uses its own structure (skill taxonomy, eval strategy, pipeline) and is **not** an SDD in the template sense. It is excluded from this build-out and should not be rewritten to match. The remaining 17 are SDD stubs with placeholder sections. All 17 services are fully built in code — the SDDs need to be written from implementation, not designed ahead of it.

These SDDs are the **canonical knowledge layer** for the platform. They feed into:
- **Memory bus** — semantic search across platform knowledge
- **GitNexus** — knowledge graph for codebase maintenance
- **Builder agents** — context for factory pipeline execution

They must be authoritative, correctly scoped (platform vs app), and deduplicated.

---

## Scope — 17 SDDs

### Platform (3)
| File | Service | Code Location |
|------|---------|---------------|
| `platform/factory-pipeline.md` | 9-stage build process | Skills, CLAUDE.md, factory-manifest.json |
| `platform/memory-bus.md` | Organizational knowledge store | `growdirect_memory` DB, Canary `services/alx/`, Cove `mcp/` |
| `platform/shared-infrastructure.md` | Docker, Postgres, Valkey, Ollama | `devops/docker-compose.yml`, configs |

### Canary (6)
| File | Service | Code Location |
|------|---------|---------------|
| `canary/tsp.md` | Transaction Stream Processor | `canary/services/tsp/`, `canary/blueprints/webhooks_tsp.py` |
| `canary/fox.md` | Case Management | `canary/services/fox/`, `canary/models/fox/` |
| `canary/chirp.md` | Detection Engine | `canary/services/chirp/` |
| `canary/metrics-analytics.md` | Metrics ETL & Analytics | `canary/services/metrics/`, `canary/models/metrics/` |
| `canary/identity-square.md` | OAuth & Square Integration | `canary/services/identity/`, `canary/services/parsers/` |
| `canary/owl.md` | Intelligence Brain | `canary/services/owl/` |

### Cove (5)
| File | Service | Code Location |
|------|---------|---------------|
| `cove/archive-system.md` | Document Archive | `cove/archive/` |
| `cove/parcel-map-engine.md` | Parcel & Map Engine | `cove/parcels/`, `cove/map/`, `cove/models/parcel.py` |
| `cove/governance-engine.md` | Governance Engine | `cove/governance/`, `cove/models/governance.py` |
| `cove/secret-ballot-elections.md` | Secret Ballot Elections | `cove/governance/election_*`, `cove/models/election.py` |
| `cove/member-auth.md` | Member Auth & Privacy | `cove/auth/`, `cove/member/` |

### ALX (3)
| File | Service | Code Location |
|------|---------|---------------|
| `alx/qa-agent.md` | QA Agent | `canary/services/qa_agent/` |
| `alx/mcp-service-layer.md` | MCP Service Layer | `canary/mcp/` |
| `alx/test-lab.md` | Test Lab & Scenario Runner | Scripts, test fixtures |

---

## Process

### Phase 1 — Deep Code Audit

Parallel agents read all code for all 17 services simultaneously (3 agents: platform+ALX, canary, cove). ALX services live in the Canary codebase (`canary/services/qa_agent/`, `canary/mcp/`), so the platform+ALX agent reads both the shared infra and the ALX code within Canary to avoid overlap with the Canary agent. Each agent produces a structured findings report covering:

- **Inventory:** Every model, service module, route, config, and test file
- **Scope check:** Is this correctly placed at app vs platform level?
- **Duplication check:** Same logic in multiple apps that should be shared?
- **Gap check:** Referenced but unbuilt, or built but undocumented?
- **Dependency map:** What does this service depend on? What depends on it?

**Deliverable:** Single consolidated audit findings report. User reviews before Phase 2.

### Phase 2 — SDD Authoring

Parallel agents write SDDs per namespace from audit findings + direct code reading. All follow the approved template (see below). Each SDD replaces the existing stub in place.

**Deliverable:** 17 complete SDDs committed to `docs/sdds/{namespace}/{service}.md`.

### Phase 3 — Memory & Knowledge Update

- Update `MEMORY.md` with SDD completion status
- Save memory entries for key architectural findings:
  - Platform vs app scope decisions
  - Duplication patterns discovered
  - Cross-service dependency insights
- SDDs committed to git for GitNexus ingestion

**Deliverable:** Updated memory, clean git history.

---

## SDD Template

Every SDD follows this structure:

```markdown
# {Service Name}

> **Status:** Complete — written from code
> **Namespace:** {platform|canary|cove|alx}
> **Last updated:** YYYY-MM-DD
> **Code location:** {primary directory path(s)}

## 1. Overview

What the service does, why it exists, where it fits in the platform.
One paragraph, no fluff.

## 2. Architecture

### Component Diagram
How the service is structured internally — modules, their responsibilities,
how they connect.

### Request / Data Flow
The primary flows through the service — what triggers processing,
what path data takes, what the output is.

### Key Design Decisions
Why the service is built this way. Reference ADRs where they exist.

## 3. Data Model

Every table owned by this service, using SQLAlchemy 2.0 `Mapped[]` notation
to match codebase conventions (never `Column()`):
- Table name, columns with `Mapped[type]` annotations, constraints
- Relationships (foreign keys, `back_populates`)
- Indexes
- Mixins applied (audit, tenant, etc.)
- Relevant Alembic revision IDs (which migrations created/modified these tables)

## 4. Interfaces

### Routes
Every endpoint — HTTP method, path, auth requirement, request/response shape.
Grouped by blueprint (MCP vs wired).

### Webhook Schemas (if applicable)
Inbound webhook payloads the service handles.

### CLI / Scripts (if applicable)
Management commands or utility scripts.

## 5. Service Layer

Business logic modules:
- Module name, responsibility
- Key functions with signatures and behavior
- Orchestration patterns (how modules call each other)

## 6. Configuration

Environment variables, config class fields, feature flags.
What each controls and its default value.

## 7. Security & Compliance

Auth requirements, data sensitivity classification, and regulatory constraints:
- What auth is required (JWT, session, API key, none)
- Sensitive data handled (PII, tokens, financial data, votes)
- Compliance requirements (PCI awareness for Canary, Davis-Stirling for Cove)
- Data isolation patterns (RLS, schema separation, encryption at rest)
- Mark N/A with reason for services with no security-sensitive surface

## 8. Error Handling

Failure modes the service handles:
- What can go wrong
- How it's detected
- What happens (retry, fallback, alert, fail-open/closed)

## 9. Testing

- Test files that cover this service
- Fixture patterns used
- How to run tests for this service
- Coverage notes (what's tested, what's not)

## 10. Dependencies

### Upstream (this service depends on)
Services, databases, external APIs this service calls.

### Downstream (depends on this service)
Services that call into or consume from this service.

### Shared Infrastructure
Postgres, Valkey, Ollama, Docker network dependencies.

## 11. Known Issues & Reconciliation

Findings from the audit:
- Scope issues (app-level code that should be platform, or vice versa)
- Duplication with other services
- Gaps (referenced but unbuilt, or built but undocumented)
- Recommended actions
```

---

## Audit Checklist — Per Service

For each of the 17 services, the audit agent must answer:

- [ ] What models does this service own? (list files + table names)
- [ ] What service modules exist? (list files + primary functions)
- [ ] What routes are exposed? (list endpoints + auth requirements)
- [ ] What config does it consume? (env vars, config class fields)
- [ ] What tests exist? (list test files + fixture patterns)
- [ ] Is this scoped correctly? (platform vs app level)
- [ ] Is any logic duplicated in another app/service?
- [ ] Are there references to unbuilt features?
- [ ] What are the upstream and downstream dependencies?

---

## Success Criteria

1. All 17 SDDs are complete, following the template, written from code
2. No stub sections remain — every section is populated or explicitly marked N/A with reason
3. Scope issues, duplication, and gaps are documented in Section 10 of each SDD
4. Memory updated with architectural findings
5. All SDDs committed to git in a single clean commit
6. SDDs are self-contained — a developer or AI agent can understand each service from its SDD alone
