---
title: OQ Resolution Pack — 22 founder-approved decisions + 12 Bart-gated questions
type: plan
status: founder-approved
date: 2026-05-03
author: ALX
linear: GRO-762
parent: GRO-739
governs:
  - docs/sdds/go-handoff/canonical-data-model.md
  - docs/sdds/go-handoff/cloud-architecture-workload.md
  - docs/sdds/go-handoff/party-identity-design.md
  - docs/sdds/go-handoff/canonical-data-model-party-edits.md
  - docs/sdds/go-handoff/driftpos-integration.md
  - Brain/wiki/cards/store-network-integrity.md
  - Brain/wiki/cards/platform-wyoming-ecosystem.md
last-compiled: 2026-05-03
needs-review: 2026-08-03
---

# OQ Resolution Pack — Loop 3 Wave 1

## §1 Mission

This pack converts the open-question pile from the seven-dispatch SDD run (GRO-684, GRO-726, GRO-733, GRO-734, GRO-759, GRO-760, GRO-761) into one of two terminal states for every OQ: **decided + applied** or **explicitly waiting on Bart's DriftPOS team**. The founder pre-approved all 22 decisions in §A.1 on 2026-05-03; this document records them so future agent sessions and downstream SDDs apply the calls without re-confirming each one.

**Why this exists:** carrying TBDs across loops compounds — Loop 4 inherits Loop 3's unresolved questions plus new ones. Resolving 22 OQs in one pass unblocks four Phase B unblockers, the Loop 3 backlog (10+ items), and the Bart conversation prep — all from one founder pass.

**Operating posture:** the dispatch's standing meta-rules apply — open-source / standards-oriented choice at every fork; every threshold/default/cadence configurable; solo-builder norms; founder-approved decisions are not re-litigated.

## §2 Standing meta-rules

These bind every decision in §A.1 and every artifact downstream of it.

### 2.1 Open-source / standards-oriented bias

Every architectural fork defaults to the proven open-source standard. The standard is named explicitly inline with the spec, package, or project URL. There is no wrong in choosing the proven pattern — proprietary tooling needs a load-bearing justification, not the open-source default.

Standards exercised in this pack:
- [`github.com/shopspring/decimal`](https://github.com/shopspring/decimal) — decimal math in Go (OQ-2.3)
- Application-state-machine + Postgres advisory locks ([`pg_advisory_lock`](https://www.postgresql.org/docs/17/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS)) — replaces Cloud Workflows (OQ-3.2)
- [Wazuh](https://wazuh.com/) — open-source SIEM partner (OQ-4.2); alternatives: Sumo Logic OSS, ELK with Wazuh agent
- [IANA timezone identifiers](https://www.iana.org/time-zones) per [RFC 6557](https://datatracker.ietf.org/doc/html/rfc6557) — `l.locations.timezone` (Phase B.1, OQ derivative)
- [OpenTelemetry](https://opentelemetry.io/) — observability collection
- [OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749) + [OIDC](https://openid.net/connect/) — identity federation

### 2.2 Configurability discipline

No hardcoded thresholds, defaults, tiers, or cadences. Each becomes one of:
- **(a)** row in a config table (e.g., `f.markup_envelope_tiers`)
- **(b)** tenant feature flag in `app.tenants.attributes` JSONB or per-tenant settings table
- **(c)** env var with documented default (boot-time), or
- **(d)** per-merchant override (`app.merchant_settings`)

Every knob introduced by §A.1 appears in §A.3 with its mechanism. The founder must be able to tune any rule per merchant per situation — that's the load-bearing property of "Canary serves your store, not the other way around."

### 2.3 Solo-builder norms

Single primary working clone (laptop main); no parallel-clone coordination required; force-push acceptable when history-rewrite is required (with backup branch first). Phase 0 of GRO-762 exercised this — NSF history strip + force-push completed cleanly with `backup-pre-nsf-strip-20260502` retained as the safety net.

### 2.4 Founder-approved OQ posture

The 22 decisions in §A.1 are pre-approved 2026-05-03. Agent applies them as-decided. Do not re-confirm; do not propose alternatives. If a future session believes a decision needs revisiting, raise it in a separate Linear dispatch — not as a re-litigation in mid-flight.

---

## §A.1 Founder-approved decisions (22)

Decisions group into four clusters: identity/privacy (5), pricing/commercial (3), cloud architecture (6), and DRAFT cards (2). Reading note: each row maps OQ → decision → configurability mechanism. Full implementation linkage in §A.4.

### Cluster 1 — Identity / Privacy posture (GRO-734)

| OQ | Question | Decision | Configurability mechanism |
|---|---|---|---|
| **1.1** | Anonymous historical backfill yes/no | **YES** — retro-fingerprint existing `t.transactions` to populate `party_id` at party schema deploy. Avoids cold-start where merchant onboards Canary with N years of pre-Canary transactions and has zero party history. | Per-tenant flag `app.tenants.attributes->>'party_backfill_enabled'` (default `true`); set to `false` only when explicit founder/legal review demands no retro-processing |
| **1.2** | Self-computed fingerprint posture | **KEEP at quality 0.4** with the hard rule: a self-computed fingerprint **never auto-creates a Rule-3 weak match**. Clustering signal only — operates as a multiplier on existing party signals (network token, loyalty card, magstripe), never as standalone primary identifier. | Config constant `PARTY_SELF_COMPUTED_FP_QUALITY` (default `0.4`); per-tenant override `app.tenants.attributes->>'party_self_computed_quality'`; range 0.0–0.7 (0.7 ceiling enforces never-Rule-3 invariant in code) |
| **1.3** | Households opt-in vs opt-out | **OPT-IN** — tenant-admin must explicitly enable household auto-detection. Default-off honors privacy-conservative posture; opt-in preserves all the household-decisioning capability for merchants who want it. | Per-tenant feature flag `app.tenants.attributes->>'households_enabled'` (default `false`); UI toggle in tenant-admin settings panel |
| **1.4** | De-merge audit visibility | **LP-only by default** — per-merchant configurable to expand to all internal users; external-user visibility hardcoded `false` (cannot be toggled on, ever — no tenant override). | Per-merchant feature flag `app.merchant_settings.de_merge_audit_visibility` (new column, enum `lp_only` default \| `all_internal`); external-user gate enforced at handler level via auth-claim check |
| **1.5** | Subjects.Resolve eager vs lazy | **LAZY** — resolve at Fox case-escalation time, not on Chirp detection write. Detection volume is 100×–1000× case volume; eager resolve would burden the hot path with FK lookups for signals that 99% never escalate. | Config constant `SUBJECTS_RESOLVE_MODE` (env var, default `lazy`); per-tenant override `app.tenants.attributes->>'subjects_resolve_mode'` (values: `lazy` \| `eager`); evaluator at OpenCase reads tenant attribute first, env-var fallback |

### Cluster 2 — Pricing / Commercial posture (GRO-733 + decimal)

| OQ | Question | Decision | Configurability mechanism |
|---|---|---|---|
| **2.1** | Markup envelope | **TIER-BASED inverse-volume ladder — Small: cost+50%, Medium: cost+30%, Large: cost+15%.** Smaller merchants need fatter margins to survive operating overhead spread across fewer transactions; large operators get scale-driven ratio compression. | Config table `f.markup_envelope_tiers` (rows: `archetype`, `markup_pct`, `effective_at`, `expires_at` — historicized so retroactive analysis is possible). Per-tenant override `app.tenants.attributes->>'markup_envelope_pct'` (numeric, overrides archetype default). Loop 3 schema add: `f.markup_envelope_tiers` table seed |
| **2.2** | Small-archetype ILDWAC cadence default | **HOURLY default for Small; minute opt-in. Medium/Large stay minute.** Small merchants have low-volume slow-burn signal; minute-cadence ILDWAC produces too many micro-positions and creates Postgres write churn that doesn't pay for itself. Hourly is honest at Small scale. | Per-tenant setting `app.tenants.attributes->>'ildwac_cadence'` enum (`minute`/`hourly`/`daily`); seeded by archetype on tenant creation (Small→hourly, Medium→minute, Large→minute); seed function reads `app.tenants.attributes->>'archetype'` |
| **2.3** | Decimal handling — adopt `shopspring/decimal`? | **YES** — open-source standard for Go decimal math, [github.com/shopspring/decimal](https://github.com/shopspring/decimal). Eliminates the `int64` cents / `string` numeric / `float64` / `numeric(14,4)` scatter that Loop 2 flagged. Phase B.4 lands the dependency + canonical type alias; Loop 3 Wave 2 retrofits each module. | **Type-system enforcement** — code-level standard, no per-tenant config. The standard is the type; conformance is a code review item, not a runtime knob |

### Cluster 3 — Cloud / Architecture posture (GRO-733)

| OQ | Question | Decision | Configurability mechanism |
|---|---|---|---|
| **3.1** | Multi-region Cloud Run pattern | **ACTIVE-PASSIVE** with Cloud SQL cross-region replica for Tier 1 only; Cloud Run stays single-region until traffic warrants. Active-active doubles operating cost without adding meaningful resilience until we cross the threshold where single-region failover RTO becomes business-critical. | Per-deployment env var `MULTI_REGION_MODE` (`single` / `active_passive` / `active_active`); default `single`; deploy IaC reads it to choose replica + Cloud Run multi-region config |
| **3.2** | Cloud Workflows replace or isolate | **REPLACE before Phase 4 PCI scope.** Application-state-machine in Go using Postgres advisory locks ([`pg_advisory_lock`](https://www.postgresql.org/docs/17/functions-admin.html#FUNCTIONS-ADVISORY-LOCKS)) + new schema substrate `app.workflow_executions` (open-source standard pattern). Cloud Workflows reserved for internal-only non-load-bearing automation (alert routing, etc.). PCI auditors deeply distrust proprietary YAML state machines for evidentiary chains. | New schema substrate `app.workflow_executions` (Loop 3+ schema add); per-workflow registration in `app.workflow_definitions` config table (config-driven; no code change for new workflows after substrate lands) |
| **3.3** | Phase 4 dedicated Cloud SQL per Large tenant | **DEDICATED** for Phase 4 + Large; **shared multi-tenant** for Small/Medium. Threshold $50K/yr platform revenue per tenant triggers eval to dedicated. Below the threshold the cost of a dedicated instance dominates the marginal isolation benefit. | Config constant `DEDICATED_INSTANCE_REVENUE_THRESHOLD_USD` (env var, default `50000`); per-tenant `app.tenants.attributes->>'dedicated_instance'` boolean override (force-on for sensitive verticals — gun retailers, federal compliance — even below threshold) |
| **3.4** | Lightning anchor cadence | **HOURLY batch for evidence chain; DAILY batch for ILDWAC positions; per-tenant configurable.** Evidence-chain anchoring is the patent-architecture rail — hourly is sub-day for compliance dashboards while keeping Lightning fees bounded. ILDWAC positions roll up to daily because intra-day ladder drift below a day's resolution is operating noise. | Per-tenant settings `app.tenants.attributes->>'lightning_anchor_cadence_evidence'` (default `hourly`); `app.tenants.attributes->>'lightning_anchor_cadence_ildwac'` (default `daily`); allowed values: `realtime` / `hourly` / `daily` / `weekly` (validation in Sub 3 anchor service) |
| **3.5** | Party schema service tier | **TIER 2** (operational, hot replica + 5-min RPO) for `party.parties`, `party.households`, `party.household_members`, `party.household_evidence`, `party.identifier_links`. **TIER 1** (synchronous replica + 1-min RPO + cross-region) for `party.identifiers` (the fingerprint table — PII Tier 2 + load-bearing for every party-resolution call). `party.decisioning_facts` materialized view is **TIER 3** (async refresh, 1-hour RPO acceptable). | Tier classification documented in `party-identity-design.md` SDD §NFRs (text); per-table backup config in `cloud-architecture-workload.md` §6 (deploy IaC reads it) |
| **3.6** | Cross-region egress trade-offs | **YES (cross-region replica, RPO 5min)** for `ledger.*` + `q.case_evidence` + `protocol.evidence` — these are the patent-architecture evidentiary tables; loss = legal exposure. **DAILY GCS SNAPSHOT only** for `app.audit_log` + `t.transactions` — these are high-volume but recoverable from upstream stream replay if disaster strikes. Saves ~$1.5K/mo at Medium tier. | Per-table replication mode in `cloud-architecture-workload.md` §6 expanded table; deploy IaC reads it; config not per-tenant (cluster-wide policy — flipping per-tenant breaks the cost model) |

### Cluster 4 — Strategic DRAFT cards (GRO-684)

| OQ | Question | Decision | Action |
|---|---|---|---|
| **4.1** | `platform-wyoming-ecosystem.md` (DRAFT) | **SHELVE** — move to `Brain/wiki/cards/_parked/` with 6-month review marker. The CBDI / Frontier Coin / Custodia / Murdoch's thesis is intellectually coherent but no Linear issue tracks the academic conversation that would make it actionable. Dragging a DRAFT-status card across loops adds noise without adding velocity. | `git mv` to `Brain/wiki/cards/_parked/`; add `parked-until: 2026-11-03` and `parked-reason: pre-actionable strategic thesis; revisit when CBDI conversation initiates` to frontmatter |
| **4.2** | `store-network-integrity.md` (DRAFT platform variant) | **PARTNER via SIEM** — Wazuh as the open-source primary ([wazuh.com](https://wazuh.com/)) for Phase 1-3. Build the data spine (`protocol.evidence` already exists; that's the upstream feed); partner for alerting/compliance dashboard. Hand-rolling a SIEM violates the "no hand-rolling outside core IP" memory rule — store-network-integrity is not core IP, it's a delivery-layer concern. | Update card status to `approved`; add new §"Wazuh integration architecture" with the integration shape; document open-source SIEM alternatives (Sumo Logic OSS, ELK with Wazuh agent); reconcile with the sibling `canary-store-network-integrity.md` (approved, multi-store correlation) per §6 of the M1/M2/M3 coverage assessment |

---

## §A.2 Bart-gated open questions (12)

The 12 "DriftPOS-team confirmation required" OQs from `driftpos-integration.md` §10 are pulled into the Bart conversation prep doc. Each is structured as: question / why Canary needs the answer / Canary's recommendation if forced unilateral / Bart's expected position per founder context / decision space.

→ See [`docs/superpowers/plans/2026-05-03-bart-conversation-prep.md`](2026-05-03-bart-conversation-prep.md) (Phase C of GRO-762).

---

## §A.3 Configurability registry

Every threshold / default / tier / cadence introduced by §A.1, with its configuration mechanism. This table is the canonical answer to "where do I tune X for merchant Y?" Format: knob / type / default / override path / documented in.

| OQ | Knob | Type | Default | Override path | Documented in |
|---|---|---|---|---|---|
| 1.1 | `party_backfill_enabled` | bool | `true` | `app.tenants.attributes->>'party_backfill_enabled'` | `party-identity-design.md` §NFRs |
| 1.2 | `PARTY_SELF_COMPUTED_FP_QUALITY` | numeric (0.0–0.7) | `0.4` | env var; per-tenant `app.tenants.attributes->>'party_self_computed_quality'` | `party-identity-design.md` §B fingerprint quality matrix |
| 1.3 | `households_enabled` | bool | `false` | `app.tenants.attributes->>'households_enabled'` | `party-identity-design.md` §Part D household formation |
| 1.4 | `de_merge_audit_visibility` | enum (`lp_only`/`all_internal`) | `lp_only` | `app.merchant_settings.de_merge_audit_visibility` (new column — Loop 3 schema add) | `party-identity-design.md` §De-merge audit |
| 1.5 | `SUBJECTS_RESOLVE_MODE` | enum (`lazy`/`eager`) | `lazy` | env var; per-tenant `app.tenants.attributes->>'subjects_resolve_mode'` | `fox.md` §Subjects.Resolve (Loop 3 SDD edit) |
| 2.1 | markup envelope per archetype | numeric pct | Small 50, Medium 30, Large 15 | row in `f.markup_envelope_tiers` (new table — Loop 3 schema add); per-tenant `app.tenants.attributes->>'markup_envelope_pct'` | `pricing-as-a-service.md` §Markup envelope |
| 2.2 | `ildwac_cadence` | enum (`minute`/`hourly`/`daily`) | Small=`hourly`, Medium=`minute`, Large=`minute` | seeded on tenant creation by archetype; `app.tenants.attributes->>'ildwac_cadence'` override | `cloud-architecture-workload.md` §ILDWAC sizing + `pricing-as-a-service.md` |
| 2.3 | `shopspring/decimal` | type-system | n/a (code-level standard) | n/a — type enforcement | `Brain/wiki/cards/loop3-decimal-standard.md` (Phase B.4) |
| 3.1 | `MULTI_REGION_MODE` | enum (`single`/`active_passive`/`active_active`) | `single` | env var per deployment | `cloud-architecture-workload.md` §Multi-region |
| 3.2 | `app.workflow_definitions` registry | config table (rows) | seed-empty (workflows registered as built) | row insert per workflow | `cloud-architecture-workload.md` §A8 application-state-machine substrate (Loop 3+ SDD add) |
| 3.3 | `DEDICATED_INSTANCE_REVENUE_THRESHOLD_USD` | int | `50000` | env var; per-tenant `app.tenants.attributes->>'dedicated_instance'` bool override | `cloud-architecture-workload.md` §Phase 4 archetype |
| 3.4 | `lightning_anchor_cadence_evidence` | enum (`realtime`/`hourly`/`daily`/`weekly`) | `hourly` | `app.tenants.attributes->>'lightning_anchor_cadence_evidence'` | `blockchain-anchor.md` §Cadence |
| 3.4 | `lightning_anchor_cadence_ildwac` | enum (`realtime`/`hourly`/`daily`/`weekly`) | `daily` | `app.tenants.attributes->>'lightning_anchor_cadence_ildwac'` | `blockchain-anchor.md` §Cadence |
| 3.5 | per-table backup tier | enum (Tier 1/2/3) | per `cloud-architecture-workload.md` §6 | deploy IaC table classification | `cloud-architecture-workload.md` §6 expanded |
| 3.6 | per-table replication mode | enum (`cross_region_replica`/`daily_snapshot`) | `daily_snapshot` (default for high-volume non-evidentiary); `cross_region_replica` for ledger/evidence | `cloud-architecture-workload.md` §6 | `cloud-architecture-workload.md` §6 expanded table |
| 4.1 | wyoming-ecosystem card status | parked | `parked-until: 2026-11-03` | revisit on date or founder action | `Brain/wiki/cards/_parked/platform-wyoming-ecosystem.md` |
| 4.2 | SIEM partner | choice (Wazuh primary; Sumo Logic OSS, ELK alt) | Wazuh | `app.tenants.attributes->>'siem_partner'` (default null = Wazuh) when partner-of-record varies | `Brain/wiki/cards/store-network-integrity.md` §Wazuh integration |

**17 knobs** across 22 decisions; some decisions introduce multiple knobs (e.g., 3.4 has two cadence dimensions).

---

## §A.4 Implementation linkage

For each MEDIUM/LOW-impact decision, the dispatch / file / next step that operationalizes it. HIGH-impact decisions (Phase B targets) link to the Phase B section; everything else gets its own next-step pointer.

### High-impact (Phase B of GRO-762)

| OQ | Operationalization | Phase B reference |
|---|---|---|
| 1.5 | `SUBJECTS_RESOLVE_MODE` lazy default lands with `internal/fox/subjects.go:Resolve()` | Phase B.3 |
| 2.3 | `shopspring/decimal` dep + `internal/db/types/decimal.go` substrate | Phase B.4 |

### Medium-impact (file edits + Loop 3 backlog dispatches)

| OQ | Operationalization | Where |
|---|---|---|
| 1.1 | Backfill job spec + party schema deploy → bundled with party-edits SDD merge | `canonical-data-model-party-edits.md` §Backfill (existing); follow-up dispatch in Loop 3 backlog |
| 1.2 | Quality-score constant + ceiling-enforcement code | `party-identity-design.md` §B fingerprint quality matrix; constant lives in `internal/party/fingerprint.go` (built in M2 dispatch) |
| 1.3 | Tenant-admin UI toggle + flag wiring | tenant-admin frontend (out of CanaryGo scope); `app.tenants.attributes` JSONB read in `internal/party/household.go` |
| 1.4 | New schema column `app.merchant_settings.de_merge_audit_visibility` enum | Loop 3 schema dispatch |
| 2.1 | New table `f.markup_envelope_tiers` + seed; per-tenant override read in pricing module | Loop 3 schema dispatch + pricing-as-a-service.md SDD edit |
| 2.2 | Tenant-creation seeder reads archetype → assigns cadence | `internal/admin/tenant_seeder.go` (Loop 3 build); env var read in `pricing` package |
| 3.1 | Deploy IaC env var + cross-region replica spec | `cloud-architecture-workload.md` §Multi-region (existing); IaC change Loop 3+ |
| 3.4 | Anchor service reads tenant attribute on every batch flush | `internal/protocol/sub3/scheduler.go` (Loop 4+ — Sub 3 not yet built) |
| 3.5 | Tier classification table edit in SDD | `party-identity-design.md` §NFRs (this Loop) |
| 3.6 | Per-table replication mode column in §6 expanded table | `cloud-architecture-workload.md` §6 (this Loop) |

### Low-impact (single doc edit each)

| OQ | Operationalization | Where |
|---|---|---|
| 3.2 | SDD note on `app.workflow_executions` substrate as Phase 4 prerequisite | `cloud-architecture-workload.md` §A8 — existing portability note already calls Cloud Workflows out as #1 lock-in risk |
| 3.3 | Threshold + override documented in archetype sizing | `cloud-architecture-workload.md` §Phase 4 archetype |
| 4.1 | `git mv` of card to `_parked/` + frontmatter update | this Loop |
| 4.2 | Card status promotion + Wazuh integration §; sibling card reconciliation | this Loop + Loop 3 docs-hygiene dispatch |

---

## §A.5 What this pack does NOT decide

The following are explicitly **not** in scope of this pack, so future agents don't assume otherwise:

- **The 12 Bart-gated OQs** (DriftPOS contract specifics — see Phase C doc).
- **The 47 Loop 2 SDD findings** (most are documentation regen for `canonical-data-model.md`, `chirp.md`, `fox.md`, `pricing-as-a-service.md`, `owl.md`, `inventory-as-a-service.md`); they show up in the Loop 3 backlog (Phase D doc) and get worked in Loop 3 Wave 2+.
- **PCI / SOC 2 / DPA wording** — drafted in GRO-693, separate counsel-review track.
- **Tokenomics/L402 economic parameters** — deferred to GRO-737 business plan + Phase 2 of GRO-739.
- **The `inventory-as-a-service.md` SDD's bigger surface** (Valkey hot path, BOPIS holds, fulfillment routes, four-eyes auth, MCP tools, `inventory_devices`/`bopis_holds`/`fulfillment_routes` tables) — needs scope decision (land in canonical schema vs re-scope as separate SDD); flagged in Loop 3 backlog.

---

## §A.6 Cross-references

**Source dispatches (the seven SDDs that produced these OQs):**

- [GRO-684](https://linear.app/growdirect/issue/GRO-684) — M1/M2/M3 SDD coverage assessment (DRAFT card review → OQ-4.1, 4.2)
- [GRO-726](https://linear.app/growdirect/issue/GRO-726) — Counterpoint VAR landscape (no OQs landed here; informs Phase D backlog)
- [GRO-733](https://linear.app/growdirect/issue/GRO-733) — Cloud architecture + workload SDD + portability review (OQ-2.1, 2.2, 3.1–3.6)
- [GRO-734](https://linear.app/growdirect/issue/GRO-734) — Party identity + fingerprinting + householding (OQ-1.1–1.5)
- [GRO-759](https://linear.app/growdirect/issue/GRO-759) — DriftPOS integration contract (12 Bart-gated OQs in Phase C doc)
- [GRO-760](https://linear.app/growdirect/issue/GRO-760) — RapidPOS sub-brand feature map (no OQs landed here; informs Phase D backlog — ATF eBound + 4473 + 3310 SDD)
- [GRO-761](https://linear.app/growdirect/issue/GRO-761) — Loop 2 build report (informs OQ-2.3 decimal + Phase B.1–B.4 unblockers)

**Memory drivers cited:**

- `feedback_no_hand_rolling_outside_core_ip` → OQ-4.2 (Wazuh primary)
- `feedback_flag_dependency_changes` → OQ-2.3 (explicit `shopspring/decimal` approval)
- `feedback_publish_facts_not_gossip` → OQ-1.4 (LP-only de-merge default)
- `project_engine_map_and_main_street_archetype` → drives the Small/Medium/Large archetype split in OQ-2.1, 2.2, 3.3

**Dispatch governance:**

- [GRO-739](https://linear.app/growdirect/issue/GRO-739) — parent dispatch (ARTS-Native MCP Retail Substrate)
- [GRO-762](https://linear.app/growdirect/issue/GRO-762) — this dispatch (Loop 3 Wave 1)
