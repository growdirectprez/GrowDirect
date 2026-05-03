---
title: Loop 3 backlog — items from the 7-dispatch SDD run not in Loop 3 Wave 1 scope
type: backlog
status: ready
date: 2026-05-03
linear: GRO-762
parent: GRO-739
last-compiled: 2026-05-03
needs-review: 2026-08-03
---

# Loop 3 backlog

## Mission

Single doc enumerating everything from the seven-dispatch SDD run (GRO-684, GRO-726, GRO-733, GRO-734, GRO-759, GRO-760, GRO-761) that didn't land in Phase B of [GRO-762](https://linear.app/growdirect/issue/GRO-762). Each item carries: title, scope estimate (S/M/L), source dispatch + section, OQ-resolution dependency (now answered per Phase A), configurability impact, and recommended next-dispatch shape.

This is the menu for subsequent marathons. The founder picks the next dispatch from this list; the dispatch text borrows the recommended-shape paragraph as its starting point.

**Read this doc with:** [`docs/superpowers/plans/2026-05-03-oq-resolution-pack.md`](2026-05-03-oq-resolution-pack.md) (the 22 founder-decided OQs that unblock most items below) and [`Brain/wiki/cards/loop3-decimal-standard.md`](../../Brain/wiki/cards/loop3-decimal-standard.md) (the per-module retrofit roadmap that drives item #1).

## Item shape

| Field | Meaning |
|---|---|
| **Title** | Imperative phrase suitable for a Linear issue title |
| **Scope** | **S** (≤4h agent runtime) / **M** (4-12h, single dispatch) / **L** (>12h, requires phasing) |
| **Source** | The originating dispatch + section |
| **OQ deps** | Which OQ Resolution Pack items unblock this; now-answered = no longer a blocker |
| **Configurability** | Knobs introduced + their override paths (per the standing meta-rule) |
| **Recommended dispatch shape** | Starter language for the Linear issue — what the dispatch should ship + how it should verify |

---

## Backlog (15 items, prioritized)

### 1. Loop 3 Wave 2 — decimal retrofit across pricing / inventory / owl / sub2

| | |
|---|---|
| Scope | M |
| Source | GRO-761 finding #9 (decimal scatter); Loop 3 Wave 1 Phase B.4 substrate |
| OQ deps | OQ-2.3 (now-answered: shopspring/decimal adopted) |
| Configurability | None — type-system enforcement |
| Recommended dispatch shape | Per [`Brain/wiki/cards/loop3-decimal-standard.md`](../../Brain/wiki/cards/loop3-decimal-standard.md) §Wave 2 priority targets, retrofit modules in dependency order: square parser, counterpoint parser, chirp cash_variance + voids, q.SignalStrength + LossAmount* fields, ledger.QuantityDelta, pricing module end-to-end. Each module's retrofit is a separate per-package commit + green test gate. Acceptance criteria per the card §Acceptance criteria. |

### 2. ATF eBound + 4473 + 3310 SDD

| | |
|---|---|
| Scope | L |
| Source | GRO-760 finding #2 (RapidPOS sub-brand feature map: gun retail compliance) |
| OQ deps | None |
| Configurability | Per-tenant + per-merchant flags for which compliance modules are active (firearms-vertical merchants only) |
| Recommended dispatch shape | New SDD `docs/sdds/go-handoff/atf-compliance.md`. Spec the ATF eBound (electronic bound book) lifecycle, ATF Form 4473 (firearms transaction record) capture flow, ATF Form 3310 (multiple handgun sale notification) trigger logic. Out of scope for code build until first firearms-retail merchant signs. SDD should reference Counterpoint Gun POS sub-brand for parity (per `rapidpos-subbrand-feature-map.md`). |

### 3. Item attribute model SDD revision

| | |
|---|---|
| Scope | M |
| Source | GRO-760 finding #3 (item attribute scatter across firearms/garden/liquor sub-brands) |
| OQ deps | None |
| Configurability | Per-vertical attribute schemas (firearms requires serial number + caliber; liquor requires ABV + size; garden requires species + USDA zone) |
| Recommended dispatch shape | Revise `docs/sdds/go-handoff/canonical-data-model.md` §Items + `docs/sdds/go-handoff/data-model.md` to formalize the item attribute extension model. JSONB `m.items.attributes` already supports it; spec the per-vertical schema registry + validation hooks. |

### 4. Asset/print orchestration module SDD

| | |
|---|---|
| Scope | M |
| Source | GRO-760 finding #1 (RapidPOS sub-brands all need label/sign/voucher printing) |
| OQ deps | None |
| Configurability | Per-merchant printer driver registry; per-template format (Zebra ZPL, Brother P-touch, ESC/POS 80mm) |
| Recommended dispatch shape | New SDD `docs/sdds/go-handoff/asset-print-orchestration.md`. Spec the print-job lifecycle (queued → assigned-to-printer → printed → confirmed); the template registry; the merchant-side printer driver model. References to `Hawk` SDD for the asset-tracking surface that lives next to print orchestration. |

### 5. POS failover queue SDD

| | |
|---|---|
| Scope | M |
| Source | GRO-684 §M1 + GRO-759 §7 Failure Modes |
| OQ deps | None |
| Configurability | Per-register queue depth (env var default + per-register override); replay batch size (per OQ-4 above, pending Bart's input) |
| Recommended dispatch shape | New SDD `docs/sdds/go-handoff/edge-pos-failover.md`. Spec the SQLite-backed local 24-hour queue, replay protocol on reconnect (with `Idempotency-Key` honor per OQ-3), original-capture timestamp preservation, business-day-rollover handling during extended outage. Referenced by both DriftPOS adapter and any future POS adapter. |

### 6. OpenAPI 3.0 spec generated from driftpos-integration.md

| | |
|---|---|
| Scope | S |
| Source | GRO-759 (DriftPOS integration contract) |
| OQ deps | None |
| Configurability | None (spec generation) |
| Recommended dispatch shape | Build a `services/driftpos-adapter/openapi/` generator that emits an OpenAPI 3.0 spec from the SDD §3 API Surface (47 endpoints across 9 domains). Same pattern as the canonical-data-model.md → openapi.yaml generator already shipped under GRO-740 (`services/canary-protocol/openapi/gen/`). Output drives Bart's .NET adapter scaffolding. |

### 7. internal/adapters/driftpos/parser.go + tests

| | |
|---|---|
| Scope | M |
| Source | GRO-759 (DriftPOS integration contract) |
| OQ deps | OQ-2.3 (decimal substrate now-available); OQ-1, 2, 3, 5, 6, 11 from Phase C (Bart conversation) — gated on Bart's responses |
| Configurability | Per-tenant config of mTLS vs JWT mode (per Bart's response on OQ-1); per-tenant `payment_fingerprint` source (per Bart's response on OQ-2) |
| Recommended dispatch shape | Build the fourth `SourceAdapter` implementation alongside square/counterpoint/clover. Same shape as the existing adapters: parser package with `Parse(env publisher.Event) (*sub2.CanonicalEvent, error)`, registered in the dispatcher, integration test with a real Postgres. Wait until Bart's responses on OQ-1/2/3/5/6/11 land before starting — those determine wire-format details. |

### 8. Per-register mTLS certificate provisioning (ACME-style)

| | |
|---|---|
| Scope | M |
| Source | GRO-759 §8 Security Posture + Phase C OQ-1 |
| OQ deps | Bart's OQ-1 response (deferred until call) |
| Configurability | Per-tenant cert validity window (env var default + tenant override); per-register revocation list |
| Recommended dispatch shape | Spec + implement an internal-CA cert flow for per-register certificates. ACME-style auto-renewal; revocation API; cert distribution via the gateway's bootstrap endpoint. Integrates with mTLS gating in the gateway. Defer until Bart confirms mTLS-readiness; otherwise stays JWT-only for pilot. |

### 9. Field-capture v2 SDD

| | |
|---|---|
| Scope | M |
| Source | GRO-684 §3.1 (naming collision between `field-capture.md` SDD = semantic field-NAME mapping, and `platform-field-capture.md` Brain card = mobile/voice operative event capture) |
| OQ deps | None |
| Configurability | Per-merchant capture-mode preferences (mobile vs voice vs touchscreen); per-process field schemas |
| Recommended dispatch shape | Reconcile the naming collision per GRO-684 §8 dispatch #1 (rename existing `field-capture.md` → `field-mapping.md`). Then spec a new `field-capture-events.md` SDD per GRO-684 §7 #1: process-aware agent at process node; mobile/voice operative input → canonical event template → hash chain entry within 5s. Brain card `platform-field-capture.md` v2 has the architecture; transcribe to SDD format with API surface, table schema, MCP tools, latency targets. |

### 10. l.locations.timezone retroactive backfill for existing tenant locations

| | |
|---|---|
| Scope | S |
| Source | GRO-762 Phase B.1 (column landed with default `'America/Los_Angeles'`) |
| OQ deps | None |
| Configurability | Per-tenant override (already supports per-location override); backfill script reads merchant's billing-address state to assign timezone |
| Recommended dispatch shape | One-time backfill: for every existing `l.locations` row whose `timezone = 'America/Los_Angeles'` (the default — i.e., not yet customized), look up the corresponding merchant's billing-address state and assign the IANA timezone (`America/New_York` for Eastern states, etc.). Uses a small lookup table US-state → IANA tz. Runs as a Cloud Run Job + reports each location's before/after timezone. |

### 11. inventory-as-a-service.md SDD scope reconciliation

| | |
|---|---|
| Scope | M |
| Source | GRO-761 Loop 3 P0 regen target #4 (the IaaS SDD's larger surface — Valkey hot path, BOPIS holds, fulfillment routes, four-eyes auth, MCP tools, `inventory_devices`/`bopis_holds`/`fulfillment_routes` tables — needs to land in canonical schema or get re-scoped) |
| OQ deps | None |
| Configurability | Per-tenant Valkey hot-path enable/disable (latency tradeoff); per-merchant BOPIS-hold TTL |
| Recommended dispatch shape | Architecture decision: split the IaaS SDD into core (`inventory.md` — what's already in Loop 2's inventory module) + extended (`inventory-bopis-fulfillment.md` — the Valkey + BOPIS + fulfillment surface). Add the missing tables (`inventory_devices`, `bopis_holds`, `fulfillment_routes`) to the canonical schema. Use the `engineering:architecture` skill to write an ADR before the schema change lands. |

### 12. q.subjects formal FK declarations + cleanup of soft-FK convention

| | |
|---|---|
| Scope | S |
| Source | GRO-761 finding #2 + Loop 2 cross-module gap "Multi-tenancy key naming" |
| OQ deps | None |
| Configurability | None — schema constraint |
| Recommended dispatch shape | Add formal FK constraints to `q.subjects.related_employee_id` REFERENCES `e.employees(id)`, `related_customer_id` REFERENCES `c.customers(id)`, `related_vendor_id` REFERENCES `m.vendors(id)`. Currently soft-FKs (column with comment "FK to X" but no constraint). Also add the same to `q.detections.cashier_employee_id` (Loop 2 finding). Document the soft-FK pattern in `architecture.md` as the pre-Loop-3 default + the migration path for promoting to formal FK. |

### 13. Wazuh SIEM partner integration architecture

| | |
|---|---|
| Scope | M |
| Source | OQ Resolution Pack §A.1 OQ-4.2 (founder-approved 2026-05-03: SIEM via partner, Wazuh primary) |
| OQ deps | OQ-4.2 (now-answered) |
| Configurability | Per-tenant SIEM partner choice (`app.tenants.attributes->>'siem_partner'`, default null = Wazuh); Wazuh manager endpoint; alerting rule registry |
| Recommended dispatch shape | New SDD `docs/sdds/go-handoff/siem-integration.md`. Spec the integration shape: Canary publishes `protocol.evidence` events + `app.audit_log` rows; Wazuh agent consumes via Beats / Filebeat; Wazuh manager runs the alerting rules. Document open-source alternatives (Sumo Logic OSS, ELK with Wazuh agent). Update `Brain/wiki/cards/store-network-integrity.md` status from DRAFT to approved with the Wazuh §. |

### 14. platform-wyoming-ecosystem card → `_parked/` move

| | |
|---|---|
| Scope | S |
| Source | OQ Resolution Pack §A.1 OQ-4.1 (founder-approved 2026-05-03: shelve) |
| OQ deps | OQ-4.1 (now-answered) |
| Configurability | None — Brain organization |
| Recommended dispatch shape | Single commit: `git mv Brain/wiki/cards/platform-wyoming-ecosystem.md Brain/wiki/cards/_parked/platform-wyoming-ecosystem.md`; add `parked-until: 2026-11-03` and `parked-reason: pre-actionable strategic thesis; revisit when CBDI conversation initiates` to frontmatter. Update any wiki backlinks. Trivially small; can fold into another docs-hygiene dispatch. |

### 15. Cross-module sqlc retrofit (Loop 3 P2 from build report)

| | |
|---|---|
| Scope | L |
| Source | GRO-761 Loop 3 P2 + CanaryGo/CLAUDE.md (which currently says "no raw SQL strings" but Loop 2 shipped with raw SQL throughout) |
| OQ deps | None |
| Configurability | None — code structure |
| Recommended dispatch shape | Decision dispatch first (architecture skill ADR): keep CLAUDE.md's "all queries through sqlc" rule and schedule the retrofit, OR amend the rule to allow direct pgx for read paths and reserve sqlc for writes. Then implementation: write `internal/db/sqlc/<module>.sql` files for all 7 Loop 2 modules (item, pricing, inventory, sub2, chirp, fox, owl); run `make sqlc-gen`; replace direct pgx calls with the generated query functions. Per-module commit. |

---

## What's NOT in this backlog (already shipped or out of scope)

- **OQ Resolution Pack** — shipped Phase A of GRO-762 (`docs/superpowers/plans/2026-05-03-oq-resolution-pack.md`)
- **Bart conversation prep** — shipped Phase C of GRO-762 (`docs/superpowers/plans/2026-05-03-bart-conversation-prep.md`)
- **Schema unblockers (timezone, tender_types seed, Subjects.Resolve)** — shipped Phase B.1-B.3 of GRO-762
- **Decimal substrate (shopspring/decimal + canonical alias)** — shipped Phase B.4 of GRO-762; **retrofit** (item #1 above) is the follow-up
- **PCI/SOC 2/DPA wording** — separate counsel-review track via GRO-693
- **L402-OTB economic parameters** — deferred to GRO-737 business plan + Phase 2 of GRO-739
- **Tokenomics design** — deferred to Phase 2 of GRO-739

---

## Top 3 items needing founder attention next

(Per dispatch §Definition of Done: "Linear closure comment with… top 3 things Phase D flags as needing founder attention next.")

### 1. Schedule the Bart Zoom (Phase C doc is ready; needs a calendar slot)

The Bart conversation prep doc is ready for the call. Six of the 12 OQs gate downstream work (OQ-1 mTLS, OQ-2 network token, OQ-3 idempotency, OQ-5 UUID assignment, OQ-6 receipt reconciliation, OQ-11 PCI scope). Two of those (OQ-3 idempotency + OQ-11 PCI scope) are pilot-blockers. Backlog item #7 (DriftPOS adapter) cannot start until Bart's responses are in. **Recommended: schedule the call within 2 weeks; founder sets agenda from the prep doc.**

### 2. Decide whether item #11 (inventory-as-a-service scope reconciliation) is a Q3 or Q4 dispatch

The IaaS SDD's larger surface (Valkey hot path, BOPIS holds, fulfillment routes, four-eyes auth, MCP tools) is a substantive scope question — does Canary build BOPIS as a v1 capability or wait for a merchant to ask for it? The current Loop 2 inventory module covers the core; the extended surface is the next leap in capability and complexity. **Recommended: founder decides scope before the dispatch is filed; uses the `engineering:architecture` skill to write an ADR first.**

### 3. Choose between item #15 (sqlc retrofit) full vs partial

CanaryGo/CLAUDE.md currently says "no raw SQL strings outside sqlc" but every Loop 2 module shipped with direct pgx + raw SQL (per the dispatch override). Loop 3 has to either honor the rule (large-but-mechanical sqlc retrofit across all 7 modules) or amend the rule (allow direct pgx for read paths). The retrofit is a real engineering investment; the rule amendment is a posture change. **Recommended: founder decides the posture; if retrofit, schedule it as the first dispatch after Loop 3 Wave 2 (decimal retrofit) since both touch the same files.**

---

## Cross-references

- [GRO-762](https://linear.app/growdirect/issue/GRO-762) — this dispatch
- [GRO-739](https://linear.app/growdirect/issue/GRO-739) — parent (ARTS-Native MCP Retail Substrate)
- [`docs/superpowers/plans/2026-05-03-oq-resolution-pack.md`](2026-05-03-oq-resolution-pack.md) — companion (the 22 founder-decided OQs)
- [`docs/superpowers/plans/2026-05-03-bart-conversation-prep.md`](2026-05-03-bart-conversation-prep.md) — companion (the 12 Bart-gated OQs)
- [`Brain/wiki/cards/loop2-build-report.md`](../../Brain/wiki/cards/loop2-build-report.md) — Loop 2 closure report (the source of most of these items)
- [`Brain/wiki/cards/loop3-decimal-standard.md`](../../Brain/wiki/cards/loop3-decimal-standard.md) — driver for backlog item #1
