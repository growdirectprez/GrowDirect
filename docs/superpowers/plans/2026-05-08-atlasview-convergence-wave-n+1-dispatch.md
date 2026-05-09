---
plan-version: 1.0
date: 2026-05-08
phase: AtlasView Convergence
wave: N+1 (substrate plane)
mode: autonomous session
brainstorm-session: keen-hugle-563a44
companion-spec: docs/superpowers/specs/2026-05-08-atlasview-convergence-design.md
---

# Wave N+1 — SDD Authoring Session Dispatch

## Charter

Author **SDD-001 — AtlasView Structural Backbone** as a substrate artifact. Methodology-side authoring only. No Go code. No platform-repo touch. The SDD is the only deliverable.

The SDD is the precondition for Wave N+2 (Go implementation) but Wave N+2 is not part of this session.

## Working directory

`~/GrowDirect/` (firm umbrella). Brain context loaded; memory bus accessible at `http://127.0.0.1:8003/mcp`; canary.go and Cove sources reference-readable.

**Not** `~/GrowDirect-viggo/` — this wave does not touch the AtlasView platform code.

## Session-start required reads (in order)

1. `~/GrowDirect/CLAUDE.md` — firm umbrella standards
2. `~/CanaryGo/CLAUDE.md` — Canary Go agent rules + stack
3. `~/GrowDirect/docs/sdds/go-handoff/identity.md` — tenancy + identity pattern source (lift hierarchy-scoped role binding shape; lift federation broker pattern; lift platform JWT shape)
4. `~/GrowDirect/docs/sdds/go-handoff/data-model.md` — canary.go data conventions (sqlc patterns; two-tier migration model; column-level conventions)
5. `~/Cove/docs/bylaws-as-config.md` — bylaws-as-config worked example
6. `~/Cove/cove/models/organization.py` — Org-as-config-envelope reference shape
7. `/Users/gclyle/GrowDirect/Brain/raw/inbox/Viggo Platform Prompt_20251031.pdf` — Tim PDF v3:
   - §3 Principle Statements (five canonical principles)
   - §5 Relationship Definitions (sixteen named relationships)
   - §6 Object Definitions (Structure Objects data-field catalog)
8. Existing Sparring Partner cards: `zone.md`, `team.md`, `role.md`, `position.md`, `person.md`, `organization.md`, `orgunit.md` (location TBD — query memory bus or Brain wiki)
9. Existing SDDs in `~/GrowDirect/docs/sdds/canary-go/` or `~/GrowDirect/docs/sdds/cove/` (for SDD-shape pattern, lineage, frontmatter conventions — the `atlasview/` folder is empty until this SDD lands)
10. AtlasView decisions register — record this SDD as the first AtlasView entry. SDD number is **SDD-001** (the `atlasview/` folder is fresh; no prior AtlasView SDDs exist)

## Deliverable

`~/GrowDirect/docs/sdds/atlasview/SDD-001-structural-backbone.md` — first SDD in a fresh `atlasview/` SDD folder.

## SDD specification requirements

The SDD must specify each of the following. Each is a section header; every section has a "What" (the spec) and a "Why" (the substrate or pattern source it inherits from).

### 1. Tenant boundary

- Organization is the tenant entity.
- `organization_id` UUID FK on every tenant-scoped table.
- Postgres RLS policy template per tenant-scoped table (defense-in-depth on top of application-layer query filtering, lifted from Cove's ballot-envelope pattern).
- Tenant boundary at Organization, not at Team or Zone.

### 2. Seven Structure Object tables

For each table — `organizations`, `org_units`, `zones`, `teams`, `roles`, `positions`, `persons` — specify:

- Column-level schema (UUID PK; `organization_id` FK except for `organizations` itself; `created_at`/`updated_at` per firm convention; soft-delete column where appropriate)
- Methodology-as-source fields per Tim PDF v3 §6
- Methodology-ahead-of-source fields, explicitly flagged:
  - **Zone:** Funding
  - **Team:** Funding, Capacity, team_type enum (Community / Delivery / Governance)
  - **Role:** Voting Rights, Eligibility Constraints (generalized from Cove's `BOARD_CONFIG.residency_requirement`), role_pattern enum (Standard / Link / Representative / Governance)
  - **Person:** Skills, Credentials, Badges
- Indexes (especially on `organization_id` and any FK)
- RLS policy per table

### 3. Organization-as-config-envelope

Specify the methodology-config columns on `organizations`:

- `governance_model` enum (sociocracy / holacracy / board / custom)
- `default_voting_threshold` numeric
- `default_quorum` numeric
- `decision_types_config` JSONB — reserved column; full shape lands in the Decision-substrate SDD (later wave)
- `role_pattern_defaults` JSONB
- `team_typing_defaults` JSONB
- `funding_model_enabled` bool
- `person_extended_fields` JSONB (toggles for Skills / Credentials / Badges enabled per org)

Inheritance citation: Cove's `organizations` model + `PROPOSAL_TYPES` config dict, generalized.

### 4. Sixteen-relationship taxonomy expressed in Postgres + Neo4j

For each of Tim PDF v3 §5's sixteen relationships — `<Accountable Role>`, `<Accountable Team>`, `<Accountable To>`, `<Assignment>`, `<Associated To>`, `<Contains>` (multi-pattern), `<Contributes To>`, `<Dependent On>` (three sub-patterns), `<Fills>`, `<Governed By>`, `<Impacted>`, `<Interested In>`, `<Related Position>`, `<Reports To>`, `<Represents>`, `<Supported By>` — specify:

- Postgres join table (`<relationship_name>_links` or domain-natural name) with FKs and constraints
- Neo4j edge type (projected from CDC stream off Postgres; nodes mirror Postgres rows)
- Cardinality and uniqueness rules per Tim's substrate

Pattern: Postgres is system-of-record on OLTP path; CDC stream projects MDM-shaped graph to Neo4j; reads route to Neo4j for traversal-shaped queries; writes never go directly to Neo4j.

### 5. Hierarchy-scoped role binding

Lift directly from canary.go's `identity.md` §"Merchant Org Hierarchy — Role Binding Model":

- Schema: `(organization_id, hierarchy_type, hierarchy_node_id, role)`
- Hierarchy types: STRUCTURE (Zone / Team / Role nodes); ACTIVITY reserved for later wave
- Subtree inheritance enforced at query time, not by duplicating rows
- Index: `idx_user_roles_hierarchy ON (organization_id, hierarchy_type, hierarchy_node_id)`

### 6. Sibling-SDD callouts (in-scope to name; out-of-scope to specify)

- **SDD-002 (Identity)** — auth, JWT shape, federation broker (OIDC / SAML / LDAP / SCIM), RBAC enforcement, PII field encryption. AtlasView's identity service mirrors canary.go's `identity.md` wholesale. Not specified in this SDD; named as the load-bearing sibling.
- **SDD-003 (Decision substrate)** — Activity-object substrate (Decision lifecycle, voting flows, petition, cooldown, secret-ballot RLS architecture). Lifts patterns from Cove's `proposals` model, generalized. Hangs off structural objects via the relationship taxonomy specified in this SDD.

### 7. Migration strategy

Lift canary.go's two-tier model:
- Declarative: `~/AtlasView/deploy/schema/*.sql` (full schema, source-of-truth at HEAD)
- Incremental: `~/AtlasView/deploy/migrations/NNN_<slug>.{up,down}.sql` (golang-migrate format)
- Both must agree at HEAD.

### 8. Open questions section

Capture deliberately unresolved questions:
- Legacy data migration shape (Postgres + Neo4j → new AtlasView database) — punted to later wave
- Multi-org-per-tenant pattern — punted to Wave N+2 implementation
- Specific JSON shape for `decision_types_config` — Decision-substrate SDD
- Production runtime target — Wave N+2

## Stop conditions

Any one of these ends the session:

1. **SDD authored, committed, spec-document-reviewer subagent approved it.** Per the brainstorming skill's spec review loop (max 5 iterations).
2. **Substantive question requires user input.** A methodology question the substrate doesn't answer, or a stack decision genuinely unresolved. Capture the question, exit the session, surface for resolution. Style/wording questions do NOT trigger this — only methodology / architectural blockers.
3. **Spec review loop exceeds 5 iterations.** Surface to user.

## Out-of-scope (do not do in this session)

- Author the Identity SDD (sibling, separate session — Wave N+1.5)
- Author the Decision-substrate SDD (later wave)
- Touch the AtlasView platform repo (`~/GrowDirect-viggo/`)
- Touch any Go code
- Create the `atlasview.go` repo (Wave N+2)
- Plan Wave N+1.5 or N+2 in detail (replan from N+1 outputs)
- Reserve future-wave entries for hypothetical inputs (e.g., "Tim PDF v4 reconciliation reserve" — phantom-gate, not allowed)

## What landing this wave produces

- A committed SDD in `~/GrowDirect/docs/sdds/atlasview/` that any reader (human or future Claude session) can use to author the AtlasView Structural Backbone Go service without further design conversation.
- A decisions register entry in the AtlasView dispatches register naming this SDD and citing its sources.
- Substrate readiness for Wave N+1.5 (Identity SDD) and Wave N+2 (Go implementation).

## Memory artifacts already in place

The brainstorm session that produced this dispatch wrote two memory updates:
- `reference_canary_go_path.md` — corrected Go module path (`github.com/ruptiv/canary`), added DB assignments
- `project_firm_tenancy_hierarchy_pattern.md` — names the cross-platform Tenant+Hierarchy+Config-Envelope pattern that AtlasView inherits

These are session-state for any future Claude instance that picks up Wave N+1.
