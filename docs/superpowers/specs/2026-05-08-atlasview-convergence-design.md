---
spec-version: 1.0
date: 2026-05-08
status: design — awaiting first-wave execution
phase: AtlasView Convergence
target-implementation: Go (sibling to canary.go)
brainstorm-session: keen-hugle-563a44
---

# AtlasView Convergence — Design

## Governing thesis

The AtlasView platform is rebuilt on the firm's canary.go-aligned Go stack as a derivative of the methodology substrate (Tim PDF v3 + Sparring Partner cards + SDDs), inheriting the firm-level Tenant + Hierarchy + Config-Envelope pattern that Canary Go and Cove already express. The rebuild is the proof-text of methodology-precedes-technology: SDDs author the platform's structure before the platform's code does. The React frontend is preserved; the Python + Node backend is replaced.

## Phase scope

Two waves planned concretely. Wave N+1.5 and N+2 enumerated for context but not pre-executed — they re-plan from what N+1 produces.

| Wave | Plane | Deliverable | Working dir |
|---|---|---|---|
| N+1 | Substrate | SDD-NNN — Structural Backbone | `~/GrowDirect/Brain/` + `~/GrowDirect/docs/sdds/atlasview/` |
| N+1.5 | Substrate | SDD-NNN+1 — Identity (sibling, mirrors canary.go's `identity.md`) | same |
| N+2 | Technology | `atlasview` Go monorepo, Structural Backbone service + Identity service | `~/AtlasView/` (new repo) |

## Architectural decisions

| Decision | Choice | Rationale |
|---|---|---|
| Migration path | **Path C** — React stays, backend rebuilt | Frontend rewrites are expensive and orthogonal to the methodology-derivative claim. Backend is where entity model, relationship taxonomy, governance config live. Tim's UX directives can land incrementally on existing React. |
| First Go slice | **Structural backbone** (Org / OrgUnit / Zone / Team / Role / Position / Person + 16 relationships) | Methodology-honest ordering. Activity objects (Decision / Objective / Agreement / Risk) hang off structural objects via the relationship taxonomy. Pattern-sets the rest of the rebuild. |
| Substrate driver | **SDD-first** | Methodology-precedes-technology proof-text requires the SDD to exist independent of implementation. The SDD survives the implementation; if AtlasView is reimplemented in Rust in five years, the SDD still works. |
| Multi-tenancy | **Row-level via `organization_id` FK + Postgres RLS defense-in-depth + hierarchy-scoped role binding + Org-as-config-envelope** | Row-level matches Canary Go's `merchant_id` pattern. RLS lifts from Cove's ballot-envelope pattern. Hierarchy-scoped role binding lifts from canary.go's `identity.md`. Org-as-config-envelope generalizes Cove's bylaws-as-config. |
| Identity boundary | **AtlasView builds its own sibling identity service mirroring canary.go's `identity.md` wholesale** | Federation broker (OIDC / SAML / LDAP / SCIM), platform JWT HS256 with `actor_type` (human / agent / system), per-tenant claim-to-role mapping, AES-256-GCM PII field encryption. Sovereignty argument applies equally. Methodology especially needs `actor_type` for Decision provenance. |
| Stack | **Inherit canary.go**: Go 1.22+ · Chi v5 · pgx/v5 · sqlc v2 · golang-migrate v4 · PostgreSQL 17 · Valkey 8 | Firm-level technical baseline. Already locked in wave-26 standards alignment. |
| Graph layer | **Neo4j retained as AtlasView extension** | The 16-relationship taxonomy IS graph-shaped. Already locked as "AtlasView-only Go service with a Neo4j layer." Postgres remains system-of-record on OLTP path; CDC stream projects to Neo4j for traversal-shaped queries. |
| Repo | **Sibling**: new `~/AtlasView/` repo, module path `github.com/ruptiv/atlasview` | Matches firm pattern (Canary Go and Cove are each their own repos). Keeps legacy code visibly separate during transition. Clean methodology-derivative git history. |
| SDD home | `~/GrowDirect/docs/sdds/atlasview/` | Sibling to `go-handoff/`, `canary/`. Firm umbrella convention. |
| Database | New `atlasview` / `atlasview_test` on shared `growdirect_postgres` | Same firm pattern as `canary_gcp` and `cove`. |
| Valkey | DB ≥ 3 (DB 0 = Python Canary frozen, DB 1 = Cove, DB 2 = Canary Go) | Avoids collision. |
| Two-mode deployment | **Production-mode** (customer org tenant, narrow surface) vs **workspace-mode** (Ruptiv-internal, full surface — substrate authoring, agent transparency, methodology forge) | Lifts Cove's pattern. Substrate authoring lives in workspace-mode; runtime executes substrate in production-mode. |

## Pattern inheritance — Tenant + Hierarchy + Config-Envelope

The firm has a five-layer pattern across products that AtlasView adopts:

| Layer | Canary Go | Cove | AtlasView (target) |
|---|---|---|---|
| Tenant entity | `app.merchants` | `organizations` | `organizations` |
| Org-above-tenant | `app.organizations` (multi-merchant chains) | n/a | n/a |
| Config envelope | `merchant_settings` | Bylaws fields on `organizations` + `PROPOSAL_TYPES` | Methodology config on `organizations` (governance_model, decision_types_config, role_pattern_defaults, team_typing_defaults, funding_model_enabled, person_extended_fields) |
| Hierarchy trees | GEOGRAPHY, CATEGORY, LEGAL_ENTITY | Parcels (flat, APN-keyed) | STRUCTURE (Org→Zone→Team→Role→Position→Person); ACTIVITY later |
| Role binding | `(merchant_id, hierarchy_type, hierarchy_node_id, role)` with subtree inheritance | `roles` + `member_roles` (flat) | `(organization_id, hierarchy_type, hierarchy_node_id, role)` with subtree inheritance |

## Methodology-ahead-of-source fields

Tim PDF v3 §6 specifies fields the legacy AtlasView platform does not implement. The Go rebuild lands these from day one — substrate-derivative, not legacy-parity.

| Object | Methodology-ahead field | Source |
|---|---|---|
| Zone | Funding | Tim §6 |
| Team | Funding, Capacity | Tim §6 |
| Role | Voting Rights, Eligibility Constraints | Tim §6 + Cove `BOARD_CONFIG.residency_requirement` generalized |
| Person | Skills, Credentials, Badges | Tim §6 |
| Risk (later wave) | Categories enum, Planned Response enum, Likelihood/Impact, Mitigation Plan, Response Plan | Tim §6 |

## Cross-platform impact assessment

| Product | Impact | Direction |
|---|---|---|
| Canary Go | None — read-only inheritance | AtlasView reads canary.go's CLAUDE.md, identity.md, data-model.md, microservice-architecture.md as standards source. Canary Go does not read AtlasView. No shared code, no shared deploy lifecycle, no shared identity plane. |
| Cove | None — pattern-source-only | AtlasView lifts bylaws-as-config, RLS-for-tenant-isolation, two-mode deployment, Organization-as-config-envelope as patterns. Cove itself unchanged. |
| Shared infra | New tenant on `growdirect_postgres` and `growdirect_valkey` (dev) | Operational load only. Production targets are per-product. |
| Brain substrate | New SDDs land at `~/GrowDirect/docs/sdds/atlasview/` | Net-additive; existing canary.go and Cove SDDs unchanged. |

## Stop conditions and replan triggers

- Wave N+1 hits a methodology question the substrate genuinely doesn't answer → session captures the question and exits. No fake-gating; no phantom-input planning.
- Wave N+1 spec review loop exceeds 5 iterations → surface to user for guidance.
- Tim files a v4 PDF mid-flight → re-read; substrate amends; SDD revs. No reserved future-wave queue for hypothetical inputs.

## Open questions (deliberately unresolved)

| Question | When it lands |
|---|---|
| Legacy data migration shape (Postgres + Neo4j → new AtlasView databases) | Later wave; no current need to specify |
| Multi-org-per-tenant pattern (e.g., Ruptiv-as-its-own-AtlasView-tenant alongside customer orgs) | Wave N+2 implementation surface; punted |
| Specific JSON shape for `decision_types_config` (Sociocracy consent / Holacracy integrative / etc.) | Decision-substrate SDD (later wave) |
| Production runtime target (GCP-native like canary.go vs. retain AWS+Cloudflare from legacy) | Wave N+2 |
| Frontend ↔ backend auth boundary (JWT shape consumed by React from AtlasView identity service) | Identity SDD (Wave N+1.5) |

## References

- `~/GrowDirect/CLAUDE.md` — firm umbrella standards
- `~/CanaryGo/CLAUDE.md` — Canary Go agent rules + stack
- `~/GrowDirect/docs/sdds/go-handoff/identity.md` — identity service architecture (Tenant + Hierarchy + role binding source)
- `~/GrowDirect/docs/sdds/go-handoff/data-model.md` — canary.go data conventions
- `~/Cove/docs/bylaws-as-config.md` — bylaws-as-config worked example
- `~/Cove/cove/models/organization.py` — Org-as-config-envelope reference shape
- `/Users/gclyle/GrowDirect/Brain/raw/inbox/Viggo Platform Prompt_20251031.pdf` — Tim PDF v3 (methodology canon)
- Wave N+1 dispatch envelope: `docs/superpowers/plans/2026-05-08-atlasview-convergence-wave-n+1-dispatch.md`
