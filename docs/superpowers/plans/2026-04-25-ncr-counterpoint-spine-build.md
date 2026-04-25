---
classification: internal
owner: GrowDirect LLC
type: build-plan
date: 2026-04-25
target: ALXjr (laptop-side ALX targeting mini ops) + engineering sessions
follows: Factory process (SDDs → chunked memories → wikis → code) + CATz Phase II workstreams
companion: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
status: scoped-ready-for-review
---

# Build Plan — NCR Counterpoint Retail Spine Integration

## Goal

A fully populated NCR Counterpoint integration covering all 13 retail spine modules. The Boutique Home & Garden chain (Counterpoint with the lawn/garden module) is the first concrete deployment. Deliverables: working TSP adapter against Counterpoint REST API, populated CRDM, MCP tool surfaces per spine module, fixture-tested end-to-end against the public Counterpoint API surface.

## Source corpus

- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — public NCR Counterpoint REST API repo (cloned 2026-04-25)
  - 99 endpoint docs in `Endpoints/`
  - `Basics/` (Requests, Responses, DateFormats)
  - `InstallationAndConfiguration/` (Configuring, Installing, Licensing, TLS, Tokenization)
  - `Release_Notes/` (versions 2.0–2.4)
- `Brain/wiki/canary-module-*.md` — existing per-module spine wiki articles (10+ files)
- `Brain/wiki/canary-tsp-pipeline.md` — current TSP architecture
- `Brain/wiki/canary-data-model.md` — current CRDM definitions
- `CATz/method/phases/phase-2-select-and-implement.md` — CATz Phase II frame

## Architecture frame

**Factory process (per `CLAUDE.md`):**

1. **SDD** — `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` (this plan's companion). Architectural spec, module-by-module endpoint mappings, ARTS alignment, MCP tool surfaces, cross-cutting concerns.
2. **Chunked memory** — Senior ALX runs memory-bus chunking on the SDD after it merges to main. Future ALX sessions recall against module-level chunks.
3. **Wiki narratives** — Per-module updates to `Brain/wiki/canary-module-{T,R,N,A,Q,C,D,F,J,S,P,L,W}.md`. Each gets a "Counterpoint mapping" section.
4. **Code** — Canary repo. TSP adapter, CRDM extensions where authorized, per-module MCP tool surfaces, integration tests.

**CATz Phase II workstreams covered:**

- W2.1 Architecture decisions — captured in the SDD
- W2.2 Data model alignment — Counterpoint → CRDM mapping per module
- W2.3 Integration spec — TSP adapter contract
- W2.4 Build sequence — phased dispatches (below)
- W2.5 Test plan — fixture suite + acceptance per module
- W2.6 Cutover plan — Phase 5 deliverable

## Phasing + dispatch sequence

| Phase | Title | Dispatch | Modules covered | Status |
|---|---|---|---|---|
| 0 | Foundation | `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` | TSP rebuild + CRDM + adapter shell | ready, on main |
| 1 | Priority modules | `Brain/dispatches/2026-04-25-ncr-counterpoint-priority-modules.md` (TO WRITE) | T, R, F, L, N | not started |
| 2 | Catalog modules | `Brain/dispatches/2026-04-25-ncr-counterpoint-catalog-modules.md` (TO WRITE) | P, S | not started |
| 3 | Operations modules | `Brain/dispatches/2026-04-25-ncr-counterpoint-operations-modules.md` (TO WRITE) | D, W, J | not started |
| 4 | Tertiary modules | `Brain/dispatches/2026-04-25-ncr-counterpoint-tertiary-modules.md` (TO WRITE) | A, C, Q | not started |
| 5 | Cutover + monitoring | `Brain/dispatches/2026-04-25-ncr-counterpoint-cutover.md` (TO WRITE) | runbook + alerting + capacity | not started |

**Phase reasoning:**

- **Phase 0 first** because nothing else flows without an adapter + CRDM-target.
- **Priority modules (Phase 1)** are the modules every retailer needs and that produce the highest-volume + highest-value data: Transactions (T), Customer (R), Finance (F), Labor (L), Device (N). Five modules, batched to amortize the per-module ramp cost.
- **Catalog modules (Phase 2)** are H&G-critical: Pricing/Promotion (P) for the multi-tier customer pricing common in lawn/garden; Space/Range/Display (S) for item / inventory hierarchy. These unlock the H&G-specific value.
- **Operations modules (Phase 3)** are multi-store + workflow: Distribution (D) for inter-store transfers; Work Execution (W) for daily operating tasks; Forecast/Order (J) for replenishment.
- **Tertiary modules (Phase 4)** depend on earlier-phase event richness: Loss Prevention (Q) is Canary's core but it needs T+R+L populated first so detection rules have substrate; Asset Management (A) needs N populated; Commercial (C) for B2B/account customers needs R populated.
- **Cutover (Phase 5)** ships the per-customer deployment runbook + alerting + capacity-planning artifacts. Comes last because it generalizes from what was built.

## Per-phase acceptance gate

Before moving to the next phase:

- All modules in the phase have: CRDM mapping confirmed, TSP adapter section implemented, MCP tool surface exposed, fixture test suite passing
- Phase output reviewed by founder (or delegated reviewer)
- Linear ticket(s) for the phase moved to Done
- Wiki updates landed
- SDD updated if phase work surfaced corrections

## Linear ticket structure (suggested)

- **1 epic**: "Canary × NCR Counterpoint integration"
- **5 phase sub-epics**: one per phase above
- **13 module tickets**: one per spine module under the relevant phase
- **5 cross-cutting tickets**: auth + APIKey provisioning, logging, monitoring/alerting, SDK packaging, per-customer deployment runbook
- **Total: 24 Linear items.** Search Linear before filing — there may already be a Counterpoint epic. If so, hang the sub-epics + tickets there.

## Source-of-truth assignments

- **SDD** owns: architecture, module mappings, MCP tool surfaces (the menu), risks, open questions
- **Build plan (this doc)** owns: phasing, dispatch sequence, Linear structure, acceptance gates
- **Per-dispatch** owns: detailed operating procedure, scope clarification questions, per-phase acceptance criteria
- **Per-module wiki** owns: narrative explanation of the module's role + where Counterpoint covers / doesn't
- **Code** owns: implementation + tests

## Acceptance criteria (program-level)

- [ ] All 13 spine modules have a documented Counterpoint endpoint mapping in the SDD
- [ ] All 13 modules have a TSP adapter section implemented and tested against the public Counterpoint API
- [ ] All 13 modules expose at least one MCP tool surface that the agent layer can read
- [ ] ARTS POSLog 2.x parser handles all transaction-shaped entities; v4/v6 handled as fallback / forward-compat
- [ ] Fixture test suite covers happy path + 5+ edge cases per module
- [ ] Per-customer deployment runbook covers: Counterpoint license API-option enablement, auth setup, first sync, monitoring
- [ ] First production deployment (Boutique H&G chain — lawn/garden module activated) completes Phases 0–4 successfully
- [ ] Memory-bus has the SDD chunked + recallable per module
- [ ] Wiki articles for all 13 modules updated with Counterpoint-mapping section

## Risks

- **Customer license gating.** The Counterpoint API is gated by the per-customer `registration.ini` "API user option" — paid add-on. Without it, the integration can't pull data. This is a customer-side dependency, not a Canary engineering blocker — but it determines deployment ordering.
- **Windows-on-prem assumption.** The Counterpoint REST API server requires Windows 7+ / Server 2012 R2+, .NET 4.5.2. Customer sites that don't already have Windows infrastructure suitable for hosting this need a deployment plan (either customer-provided host or Canary-provided edge box).
- **POSLog version drift.** ARTS POSLog 2.x is current per NCR; older deployments may emit v4. Canary's parser plans for 2.x as primary, v4 backward-compat. v6 (mentioned in the original obsolete RAPID dispatch) is forward-compat hypothetical — NCR ecosystem is anchored on 2.x today.
- **Endpoint surface scope.** 99 endpoints exist; only ~20-25 are operationally relevant for analytics ingestion. Need disciplined pruning per phase to avoid over-scoping.
- **Multi-version Counterpoint.** API server is multi-version capable (8.4.6.12 / 8.5 / 8.6). Canary tests need to cover at least v8.5 + v8.6 baselines.

## Out of scope (do NOT do under this plan)

- NCR Aloha (restaurant-side product) — separate plan if/when needed
- NCR Advanced Store / Advanced Checkout Solution (enterprise product line) — separate plan
- Square → Counterpoint reconciliation (different conversation)
- Customer-specific configuration (lawn/garden module specifics for Boutique H&G chain) — that's a deployment-time concern, separate from this build plan
- ALXjr persona / mini reconfig — handled by `Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md`
- Bart Monday-call-prep work — handled by `Brain/dispatches/2026-04-25-monday-bart-call-prep.md`

## How ALXjr / a future session uses this plan

1. Read this plan first — understand the goal + phasing
2. Read the companion SDD — understand the per-module endpoint mappings
3. Read the foundation dispatch (`Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md`)
4. Confirm Phase 0 status with founder before any execution
5. Execute phases in order. Each phase's dispatch references the SDD for the technical spec.
6. Founder gate at end of each phase.

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — companion SDD (the technical spec this plan operationalizes)
- `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — Phase 0 foundation dispatch
- `Brain/wiki/canary-module-*.md` — per-module spine wikis (T R N A Q C D F J S P L W)
- `Brain/wiki/canary-tsp-pipeline.md` — TSP architecture
- `Brain/wiki/canary-data-model.md` — CRDM
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — source corpus (99 endpoints)
- `CATz/method/phases/phase-2-select-and-implement.md` — CATz Phase II workstream definitions
- Memory: `project_sandbox_vs_mini_separation.md` — laptop = Claude Code host, mini = hosting target
