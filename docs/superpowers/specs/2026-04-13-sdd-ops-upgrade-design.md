# SDD Ops Upgrade — Production Readiness Code Review

**Date:** 2026-04-13
**Status:** Approved
**Scope:** Upgrade all 49 SDDs from design specs to operational contracts with code review findings

---

## Problem

The 49 SDDs describe what each service is designed to do but not how it runs in production, how PII flows through it, or what code gaps need fixing before external customers can use it. Canary handles merchant transaction data from Square. Cove stores member PII and secret ballot elections for an HOA. Angel captures real estate leads with contact info. All three will run on AWS with external customers.

Current state from code audit:
- All PII stored plaintext except Canary OAuth tokens (AES-256-GCM)
- No field-level encryption for member emails, phones, lead contact info
- No data retention policy anywhere
- Encryption keys in .env files
- No audit trail for key operations (lead status changes, token access)
- RLS for ballot secrecy is DB-side only — app code doesn't enforce it
- No key rotation documented

## Decision

**Approach A: SDD-as-Ops-Contract.** Each SDD gets upgraded in-place with operational sections. The SDD becomes the single source of truth — design, operations, PII handling, and remediation findings all in one document per service. If an SDD exceeds ~5K words or covers more than one deployable unit, it splits along deployment boundaries.

---

## SDD Template

Every SDD follows this structure. An agent reads one file and knows: what the service does, how data flows, how to run it, and what's broken.

### Standard Sections (all service types)

```markdown
# {Service Name}

## Purpose
What this service does in 2-3 sentences.

## Dependencies
What it needs running (other services, databases, Valkey, external APIs).

## Data Flow & PII Map
- What enters (sources, formats)
- What's stored (tables, fields, encryption status)
- What exits (to other services, external APIs, UI)
- PII classification per field:
  - public: freely visible (listing price, neighborhood name)
  - internal: visible to authenticated users (member name within HOA)
  - sensitive: encrypted at rest, logged on access (email, phone, SSN)
  - restricted: encrypted, RLS-gated, audited (ballot content, OAuth tokens)

## API Contract
Routes, MCP tools, or internal interfaces this service exposes.

## Operations
- Startup sequence and health checks
- Failure modes (what breaks, what fails safe)
- Monitoring (what to alert on, what's normal)
- Configuration (env vars, feature flags)

## Deployment
- Docker service definition
- AWS target (ECS/Fargate, RDS, Secrets Manager)
- CI/CD requirements

## Code Review Findings
Current gaps vs production requirements. Each finding has:
- Severity: P0 (blocks prod), P1 (before GA), P2 (post-launch)
- Description of the gap
- Recommended fix
- Linear issue reference (GRO-xxx)

## Production Readiness Checklist
- [ ] PII encrypted at rest
- [ ] Secrets in AWS Secrets Manager (not .env)
- [ ] Health check endpoint responds
- [ ] Audit logging for sensitive operations
- [ ] Data retention policy implemented
- [ ] Rate limiting on public endpoints
- [ ] Error responses don't leak internals
```

---

## Service Taxonomy

The template adapts based on service type. Each type adds sections to the standard template.

### Type 1: App Service
Lives inside one app's Docker container. Handles its own routes and models.

**Template emphasis:** PII map, API contract, failure modes.

**Examples:**
- Canary: TSP, Chirp, Fox, Alert, Owl, Identity, Webhooks, UI/BFF, Analytics, Metrics, Ops
- Cove: Governance Engine, Elections, Vault, Treasury, Meetings, Parcels, Board, Auth, Archive, Notifications
- Angel: Content Engine, Web Routes, Agent Sidecar, LP Integration

### Type 2: Platform Service
Shared infrastructure that all apps depend on.

**Additional sections:**
- Multi-tenant isolation model
- Startup order and dependency graph
- Blast radius (what breaks if this goes down)

**Examples:**
- Shared Infrastructure (PostgreSQL, Valkey, Ollama, Docker network)
- Memory Bus (FastMCP on port 8003, pgvector, session memory)
- Factory Pipeline (9-stage build process, skill dispatch)

### Type 3: MCP Server
Tool providers that bridge between apps or between agents and apps.

**Additional sections:**

```markdown
## MCP Tool Registry
| Tool | Auth Required | PII Access | Rate Limit | Description |
|------|:---:|:---:|:---:|-------------|

## Cross-App Data Access
Which apps' data can this MCP server read/write?
What tenant isolation exists?

## Tool Dispatch Security
How are tool calls authenticated?
Can a tool escalate privileges?
What happens if the MCP server is compromised?
```

**Examples:**
- Canary: Owl MCP, QA Agent MCP, TSP Sub1-4 (stream consumers)
- Cove: Knowledge MCP (legal doc search)
- Platform: Memory Bus MCP, MCP Service Layer (SDK wrapper)

### Type 4: External Integration
Webhook receivers, OAuth flows, third-party APIs.

**Additional sections:**
- Signature validation method and key storage
- Retry and idempotency strategy
- Degradation behavior when external service is down

**Examples:**
- Canary: Square OAuth, Square Webhooks
- Angel: LP Webhooks, Compass CRM sync, ATTOM API
- Cove: Cloudflare Email Routing

---

## Size Rule

If an SDD exceeds ~5K words or covers more than one deployable unit, it splits. The split follows the deployment boundary — if it's a separate Docker container or could be, it gets its own SDD. The parent SDD becomes an index that links to the children.

Known splits based on current file sizes:
- `tsp.md` (59K, 9500 words) → TSP Core + Sub1 + Sub2 + Sub3 + Sub4
- `metrics-analytics.md` (43K, 7000 words) → Metrics ETL + Analytics Dashboard
- `factory-pipeline.md` (44K, 7000 words) → Pipeline Stages + Skill Architecture
- `governance-engine.md` (38K, 6200 words) → Proposal Lifecycle + Voting/Tallying
- `secret-ballot-elections.md` (37K, 6000 words) → Election Orchestration + Ballot Security
- `parcel-map-engine.md` (47K, 7500 words) → Parcel Identity + Map Rendering

Expected total: ~55 production-grade SDDs (up from 49 design docs).

---

## Work Order

### Phase 1: Canary (20 SDDs → ~25 after splits)

Canary goes to production first. Start with the data pipeline — highest PII volume.

| Order | SDD | Rationale | Expected Splits |
|-------|-----|-----------|-----------------|
| 1 | `tsp.md` | Highest PII flow, 4 consumers, 10-step pipeline | TSP Core, Sub1 (Hash-Seal), Sub2 (Parse-Route), Sub3 (Merkle), Sub4 (Chirp) |
| 2 | `webhook-pipeline.md` | Entry point for all external data, HMAC validation | None (may merge into TSP Core) |
| 3 | `identity-square.md` | OAuth tokens, AES-256-GCM — the reference implementation | None |
| 4 | `identity.md` | JWT, sessions, RBAC — auth for everything | None |
| 5 | `data-model.md` | Cross-schema reference — becomes PII map anchor | None |
| 6 | `chirp.md` | Detection engine, touches every transaction | None |
| 7 | `fox.md` | Case management, evidence chain, hash integrity | None |
| 8 | `alert.md` | Alert lifecycle, notification routing | None |
| 9 | `owl.md` | AI analysis, Ollama integration, MCP server | None |
| 10 | `analytics.md` | KPI dashboard, risk scoring | None |
| 11 | `metrics-analytics.md` | Star schema, ETL, risk snapshots | Metrics ETL + Analytics Dashboard |
| 12 | `ops.md` | Health checks, feature flags, config service | None |
| 13 | `ui-bff.md` | Frontend, session auth, feature flags | None |
| 14 | `qa-agent.md` | QA orchestration, 30+ MCP tools | None |
| 15 | `goose.md` | Treasury/payment layer, Bitcoin/L402 | None |
| 16 | `raas.md` | Namespace resolution, onboarding | None |
| 17 | `external-identities.md` | Entity resolution, PII abstraction | None |
| 18 | `multi-pos-architecture-proof.md` | Multi-source adapter pattern | None |
| 19 | `architecture.md` | Platform overview — becomes Canary index SDD | None |
| 20 | `alx.md` | Knowledge store, pgvector | None |

### Phase 2: Platform (4 SDDs → ~7)

Platform services that all apps depend on.

| Order | SDD | Rationale | Expected Splits |
|-------|-----|-----------|-----------------|
| 1 | `shared-infrastructure.md` | Everything depends on this | Docker Stack + AWS Target Architecture |
| 2 | `memory-bus.md` | MCP server, cross-app data | None |
| 3 | `mcp-service-layer.md` | SDK wrapper, auth model | None |
| 4 | `factory-pipeline.md` | Build/deploy loop | Pipeline Stages + Skill Architecture |
| 5 | `test-lab.md` | Scenario testing, sandbox | None |

### Phase 3: Cove + Angel (23 SDDs → ~28)

Cove and Angel are one deployment unit.

| Order | SDD | Rationale | Expected Splits |
|-------|-----|-----------|-----------------|
| 1 | `member-auth.md` | PII entry point, magic links | None |
| 2 | `architecture.md` | Cove platform overview | None |
| 3 | `governance-engine.md` | Ballot secrecy, Davis-Stirling | Proposal Lifecycle + Voting/Tallying |
| 4 | `secret-ballot-elections.md` | Most sensitive data handling | Election Orchestration + Ballot Security |
| 5 | `parcel-map-engine.md` | 5500 APNs, GeoJSON, Leaflet | Parcel Identity + Map Rendering |
| 6 | `angel-agent.md` | MCP sidecar, lead capture | None |
| 7 | `lp-integration.md` | External webhook, PII ingestion | None |
| 8 | `vault.md` | Document storage, access tiers | None |
| 9 | `treasury.md` | Assessments, payments | None |
| 10 | `meetings.md` | Meeting management, ARC | None |
| 11 | `board.md` | Board-only operations | None |
| 12 | `notifications.md` | Delivery routing, email | None |
| 13 | `knowledge.md` | pgvector legal search | None |
| 14 | `archive-system.md` | Document viewer, path traversal prevention | None |
| 15 | `agent.md` | AI Q&A assistant | None |
| 16 | `angel-overview.md` | Angel index SDD | None |
| 17 | `data-platform.md` | CRMLS, ATTOM, APN bridge | None |
| 18 | `web-strategy.md` | Flask content engine, SEO | None |
| 19 | `brand-and-launch.md` | Brand spec | None |
| 20 | `execution-plan.md` | Timeline, phases | None |
| 21 | `sitemap-redesign.md` | Role-gated navigation | None |
| 22 | `sitemap-redesign-issues.md` | Issue specifications | May merge into sitemap-redesign |
| 23 | `seacove-site-plan.md` | Property survey (standalone, no PII) | None |

---

## Code Review Process (Per SDD)

Each SDD upgrade follows this process:

```
1. Agent reads current SDD + relevant source code files
2. Classifies service type (App / Platform / MCP / External Integration)
3. Fills in new template sections:
   - PII map: every field that holds or touches personal data
   - Operations: startup, health checks, failure modes
   - Deployment: Docker definition, AWS target
4. Writes Code Review Findings with severity:
   - P0: Blocks production (plaintext PII, no secrets management, no auth)
   - P1: Before GA (no audit logging, no rate limiting, no retention policy)
   - P2: Post-launch (key rotation, monitoring dashboards, perf optimization)
5. Each P0/P1 finding becomes a Linear issue (GRO-xxx)
6. Updated SDD committed to git
7. Brain wiki article updated if the service has one
8. Brain Health Dashboard reflects the new article
```

---

## Known P0 Findings (From Code Audit)

These will appear across multiple SDDs. Documenting them here so the upgrade sessions have a head start:

| Finding | Severity | Affected Apps | Recommended Fix |
|---------|----------|---------------|-----------------|
| Email/phone/name stored plaintext | P0 | All | Field-level AES-256-GCM encryption using Canary's `crypto.py` pattern |
| Encryption keys in .env files | P0 | All | AWS Secrets Manager + `boto3` retrieval at startup |
| No field-level encryption for leads | P0 | Angel | Extend Canary encryption pattern to lead model |
| Raw webhook payloads preserved with PII | P0 | Angel | Redact sensitive fields before storage |
| No data retention policy | P1 | All | Automated purge: leads >12mo, audit logs >24mo, sessions >30d |
| No audit trail for lead status changes | P1 | Angel | Audit log entries for pipeline transitions |
| RLS for ballot_envelopes DB-side only | P1 | Cove | Application-level enforcement + integration tests |
| IP addresses logged plaintext | P1 | Cove | Hash or mask IPs in audit log |
| No rate limiting on webhook endpoint | P1 | Angel | Flask-Limiter on `/lp` endpoint |
| No key rotation documented | P2 | Canary | Documented rotation procedure + scheduled rotation |
| Session keys unencrypted in Valkey | P2 | All | Enable Valkey AUTH + TLS in production |

---

## Integration with Factory Pipeline

The SDD upgrade changes how the factory pipeline uses SDDs:

**Current:** SDDs are referenced at Blueprint (design compliance) and Verify (contract validation) stages.

**After upgrade:** SDDs are the operational contract at every stage:

| Stage | How SDD is used |
|-------|----------------|
| Preflight | Check that service dependencies listed in SDD are running |
| Research | Read SDD for PII map and current findings |
| Blueprint | Design against SDD's API contract and PII classification |
| TDD | Write tests that validate SDD's production readiness checklist |
| Assembly | Implement against SDD's operational requirements |
| Verify | Validate all checklist items in SDD pass |
| QA | Confirm no new P0 findings introduced |
| Ship | SDD's deployment section defines the deploy process |
| Close | Update SDD with any new findings from the session |

---

## Integration with Brain

SDDs are indexed in Brain/Home.md and visible in Obsidian. After upgrade:

- Brain Health Dashboard gets a new Dataview query: "SDDs with open P0 findings"
- Each project MOC links to its SDDs with operational status
- The content engine registry indexes SDD topics so `registry check` finds them

---

## Success Criteria

- All 49+ SDDs follow the standard template for their service type
- Every PII field in the platform is classified and documented
- P0 findings have Linear issues and are tracked to resolution
- An agent starting a session on any service can read one SDD and know: what it does, how data flows, how to run it, what's broken, and what the production deployment looks like
- Factory pipeline stages reference SDDs as operational contracts, not just design docs

---

## Timeline Estimate

- Phase 1 (Canary): ~10-15 sessions (2 SDDs per session average, code review included)
- Phase 2 (Platform): ~4-5 sessions
- Phase 3 (Cove + Angel): ~12-15 sessions
- Total: ~30-35 sessions, no fixed calendar deadline
