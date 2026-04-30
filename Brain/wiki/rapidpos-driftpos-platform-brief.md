---
classification: internal
type: wiki
status: active
sub-type: platform-brief
date: 2026-04-30
last-compiled: 2026-04-30
needs-review: 2026-05-08
source: Brain/raw/inbox/driftpos-summary.docx + Brain/raw/inbox/architecture-modules-and-customization.odt (received 2026-04-30)
source-evidence: dev.azure.com/RapidPOSDevOps/DriftPOS.API and DriftPOS.APP repositories cited throughout the architecture document
companion: Brain/wiki/bart-mccleskey-rapid-garden-pos.md
companion: Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context.md
companion: Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md
---

# Rapid POS — DriftPOS Platform Brief

**Governing thesis.** Rapid POS is no longer just an NCR Counterpoint VAR. They have built (or are building) DriftPOS — their own modern, multi-tenant, modular POS platform on .NET + Angular + Android Kotlin, hosted in their own Azure DevOps tenant. This re-casts the partnership conversation: Rapid POS is becoming a platform vendor, and the Friday meeting needs to negotiate the relationship between *two* platform companies, not a platform company and a delivery channel. The architectural fit between DriftPOS and Canary is unusually clean, but the commercial story has to update before integration choices do.

## Executive summary

| Dimension | Prior assumption (through Monday call) | New ground (after intake) |
|---|---|---|
| Rapid POS's product | Counterpoint deployed/configured for L&G | DriftPOS — own platform, own repos, own database-per-tenant runtime |
| Rapid POS's role | VAR / channel | Platform vendor *and* still a Counterpoint VAR (dual posture, at minimum during transition) |
| Canary's integration target | NCR Counterpoint REST API (95 endpoints) | Counterpoint *and* DriftPOS — the contract for DriftPOS is a separate adapter |
| Architectural fit | Adapter against Counterpoint legacy SQL | Adapter against modern .NET API with per-tenant Postgres — Canary's home turf |
| Customer migration risk | None — Counterpoint is the moat | Real — every Counterpoint customer is a DriftPOS migration candidate |
| Go pivot context (per `project_rapidpos_go_pivot.md`) | "Partner team is Go-only" | DriftPOS API is .NET — contradicts memory; needs resolution at meeting |

**Bottom line:** the technology side is mostly upside (architecture is friendly to Canary). The commercial side has new questions that need answers before any integration commitments are reasonable.

## What DriftPOS actually is

A three-layer modular monolith. Same principle across all three layers: small host, plug-in modules, no per-customer code paths in the core.

| Layer | Stack | Customization surface |
|---|---|---|
| API (`DriftPOS.WebHost`) | .NET / ASP.NET Core | `modules.json` manifest of named module assemblies; `IModuleInitializer` reflection wires services, endpoints, validators, hosted services per module |
| Backoffice (admin web app) | Angular | Forms assembled at runtime from three layers: `AppFieldDefinition` schema metadata (data) → TypeScript `*.rules.ts` cross-field rules (code) → user-saved `FormLayoutConfig` per role (data) |
| Android POS | Kotlin + Compose, `driftpos-corelib` contract module | `DexClassLoader`-loaded interceptors dropped into device cache; KSP-generated overlay registry for new modals/screens |

Tenancy: **per-tenant Postgres database, resolved per request, host instances are fungible.** Each tenant gets its own `NpgsqlDataSource`. Tenant identity is established by the `Tenants` module's middleware. (Source: §13 operational implications — the architecture document is explicit about per-tenant DB isolation.)

Module manifest as of the document: `Tenants, Catalog, Crm, Purchasing, PointOfSale, Sync, Tax, App, Reporting, Ui`. Notable — there is no Loss Prevention module, no Distribution / OTB module, no Labor module. Same gaps Counterpoint has. (See [[ncr-counterpoint-phase-0-context-brief]] §"Modules L and W have NO Counterpoint coverage.")

The `Sync` module is the line item to ask about. It could be cloud-to-Android sync, or it could be the Counterpoint-to-DriftPOS migration sync. Both readings are operationally important.

## Where Canary fits — four scenarios, ranked by leverage

| Scenario | What it looks like | Pros | Cons | Verdict |
|---|---|---|---|---|
| **A — Canary as a DriftPOS module** | `DriftPOS.Module.Canary` ships in `modules.json`, runs in-process, reads the per-tenant Postgres directly | Tightest integration, lowest latency, native to the host | Tenants get the same modules — no per-tenant gating; we are inside their release cycle and their .NET runtime; couples our roadmap to theirs | Architecturally elegant, commercially constraining. Park unless they propose it. |
| **B — Canary alongside DriftPOS, reading Postgres** | Canary runs as a separate service, reads the tenant's DriftPOS Postgres on a logical-replication or read-replica feed | Decoupled deploys, language-neutral, plays to Canary's existing posture as enterprise-layer-on-top | Per-tenant DB connection management is non-trivial at fleet scale; we'd want a sanctioned read pattern, not screen-scraping | **Strongest default.** Mirrors the Counterpoint posture and matches `project_canary_native_labor_module_opportunity.md` framing. |
| **C — Canary integrates via DriftPOS API** | Canary calls DriftPOS's `Catalog`, `PointOfSale`, `Sync`, `Reporting` endpoints; no direct DB access | Cleanest contract, future-proof if their schema evolves | API surface is unknown; rate limits, webhook semantics, auth model all open questions | Best if DriftPOS exposes a public API surface comparable to Counterpoint's. Verify Friday. |
| **D — DriftPOS as a Canary destination** | Canary's plans (POs, transfers, distribution recs) write into DriftPOS via API; DriftPOS executes; Canary watches the result | Operationalizes the "plan in Canary, execute downstream" UX from `ASSUMPTION-J-08` | Same API-surface dependency as C; also requires write authority and idempotency story | Phase-2 / dependent on C. |

**Recommended pre-position for the meeting:** scenario B as the default ("Canary reads, doesn't replace; lives alongside, not inside"), with C as the medium-term direction if they have an API.

## The strategic re-frame

Three things change because DriftPOS exists.

1. **Bart's company is now a peer, not just a channel.** Treat the meeting as a vendor-to-vendor partnership conversation, not a channel-recruitment pitch. The CATz pitch ("we are Rapid POS delivery experts using the Canary spine") still works, but it sits on top of a strategic alliance discussion that has to happen first.

2. **The Counterpoint moat is time-limited.** Every Rapid Garden POS customer running Counterpoint today is a candidate to migrate to DriftPOS tomorrow. Canary's integration value compounds if it spans both — i.e., a customer migrating from Counterpoint to DriftPOS keeps their Canary continuity. That is a real story to tell. It also justifies double-track adapter work (Counterpoint adapter ships now; DriftPOS adapter is the bridge).

3. **The Go pivot memory needs resolution.** `project_rapidpos_go_pivot.md` says "partner team is Go-only" and "Go pivot is a commercial necessity, not a preference." DriftPOS is .NET + Kotlin. Either (a) DriftPOS is the answer to "what they wanted Go for" and the memory was a misread of the brief, or (b) Go applies to a different layer (sync backbone, NCR adapter, infra) not yet visible. Ask directly.

## Open questions to resolve at the meeting

Ranked by decision-leverage on the next 30 days of Canary work.

| # | Question | Why it matters |
|---|---|---|
| 1 | What is DriftPOS's deployment status? Live customers today? Pilot? Internal? | Determines whether DriftPOS adapter work is Q3 / Q4 / 2027 priority |
| 2 | Counterpoint customer migration roadmap — committed timelines? | Sizes how long the Counterpoint adapter remains the primary integration target |
| 3 | Does DriftPOS expose a public REST API surface, or are Backoffice + Android the only API consumers? | Decides scenario B vs C vs D in the table above |
| 4 | What does the `Sync` module do? | Reveals whether Counterpoint→DriftPOS migration tooling already exists |
| 5 | Where does the "Go pivot" actually live? | Resolves the contradiction with memory `project_rapidpos_go_pivot.md` and clarifies whether Canary has a Go-language constraint |
| 6 | Per-tenant code is not supported on the API — how do they handle customer-specific server logic today? | Frames whether Canary-as-module (scenario A) is even on the table |
| 7 | Loss prevention, OTB, distribution, labor — DriftPOS gaps. Plan to fill them, partner to fill them, or leave them? | This is Canary's white space. Direct test of partnership appetite. |
| 8 | Database access patterns — are tenant DBs accessible to partner services (read replica, logical replication, sanctioned read API)? | Operational feasibility of scenario B |

## Risks and unknowns

- **DriftPOS may already have a partner / module that overlaps Canary.** The architecture document mentions an `Ai` configuration section bound at module init. Worth probing — Canary and an in-house AI module compete for the same surface.
- **Per-tenant compilation isn't supported.** Customer-specific behavior must be data, gated logic, or device-side interceptors. This rules out clean per-customer Canary pricing/feature tiers if we go scenario A.
- **Document is one-sided.** Both files describe DriftPOS from inside Rapid POS's perspective. We have not seen the customer-facing surface, the marketing, or the migration playbook. Friday is the chance to fill that.
- **Audience boundary.** The architecture document is engineering-detailed and was shared with us — that's a trust signal, but treat it as confidential until told otherwise. Do not propagate to CRB / NCR / public surfaces without Bart's explicit go-ahead.

## What this changes in existing assets

- [[bart-mccleskey-rapid-garden-pos]] — needs an addendum: Bart now controls *two* platform decisions, not one
- [[ncr-counterpoint-rapid-pos-relationship]] — relationship table needs a fourth row for DriftPOS
- [[ncr-counterpoint-phase-0-context-brief]] — Phase 5 cutover assumption ("real-customer Counterpoint instance") may be partially superseded if Bart steers us at DriftPOS instead
- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — risks section should add "Counterpoint customers may migrate to DriftPOS during Canary delivery; adapter portability matters"
- Memory `project_rapidpos_go_pivot.md` — flag for review post-meeting

Defer the actual edits to those files until after Friday. Confirmed answers update them; speculation does not.

## References

- `Brain/raw/inbox/driftpos-summary.docx` — Business analyst summary, ~1500 words
- `Brain/raw/inbox/architecture-modules-and-customization.odt` — Full technical architecture, ~14 sections, source-of-truth
- Source URLs in the architecture document: `dev.azure.com/RapidPOSDevOps/DriftPOS.API` and `dev.azure.com/RapidPOSDevOps/DriftPOS.APP` (Rapid POS Azure DevOps tenant — internal repos, not public)
- Extracted markdown working copies: `Brain/raw/.extract/rapidpos-2026-04-30/`
