---
title: M1/M2/M3 Coverage Assessment — post-Loop-2
type: plan
status: draft
date: 2026-05-03
linear: GRO-684
parent: ""
last-compiled: 2026-05-03
needs-review: 2026-05-17
---

# M1/M2/M3 Coverage Assessment — post-Loop-2

## 1. Purpose

The 2026-04-29 church session shipped eight new Brain cards covering platform thesis (v3), ICP, proof case, Wyoming ecosystem, field capture (v2), performance NFRs, PwC benchmarks, and store network integrity. Loop 2 then put seven Tier-1+2 modules through a Go compiler and shipped a full multi-POS dispatcher. This assessment evaluates whether the SDD set behind those modules reflects what the new cards now describe — and whether the built code matches either. The governing thesis: **the 2026-04-29 church output added thinking the build artifacts have not absorbed yet, and the dispatch's "M1/M2/M3" labeling sits outside the canonical milestone map**, so coverage gaps must be measured against both framings before the next build sprint commits to scope.

## 2. Critical framing finding: dispatch M1/M2/M3 ≠ canonical M1/M2/M3

The dispatch (`GRO-684`, 2026-04-29) names three modules using one labeling scheme. `docs/sdds/go-handoff/go-module-layout.md` (2026-04-29, same day) uses a different scheme. Both are current. Neither is wrong. The reader has to know which label they are reading.

| Label | Dispatch GRO-684 framing | Canonical milestone map (`go-module-layout.md` §Milestone-to-binary) |
|---|---|---|
| **M1** | Transaction Module — POS write path, receipt hashing, field capture event ingestion, chain entry, POS failover queue | Foundation — `identity`, CRDM package, Multi-POS substrate |
| **M2** | Inventory / Receiving Module — ASNaaS, three-way match, receiving discrepancy, dock-door field capture, vendor chargeback routing | Detection Core — `tsp`, `chirp`, `fox` |
| **M3** | Commercial / OTB Module — L402-gated wallet, POaaS, commercial agent commit flow, buyerless buying | Intelligence Layer — `owl`, `analytics` |
| **M4** | (not addressed in dispatch) | Module Spine — `hawk`, `bull`, `asset`, `item`, `inventory`, `receiving`, `transfer`, `pricing`, `employee`, `customer`, `returns`, `report` |
| **M5** | (not addressed in dispatch) | VAR Delivery — `edge`, Bull NCR connector |

The dispatch labels are domain-grouped (what the module does for the merchant). The canonical labels are dependency-ordered (what has to compile first to keep going). The mismatch is itself the headline finding: anyone reading future "M1" references in the repo must check which framing applies. Sections 3 and 4 below cover both.

## 3. Per-module assessment (founder's labeling)

### 3.1 M1 — Transaction Module (per dispatch)

**Scope per dispatch:** POS write path; receipt hashing; field capture event ingestion; chain entry on receive; POS failover queue (24-hour SQLite buffer + replay).

| Capability | SDD coverage | Built-code status | Gap |
|---|---|---|---|
| POS write path (multi-source) | `multi-pos-architecture-proof.md`, `pos-adapter-substrate.md`, `tsp.md` | **Shipped Loop 2.** Dispatcher + Square + Counterpoint + Clover (stub) routing through `internal/protocol/sub2/`; cmd binaries `gateway`, `sub1-hash-seal`, `sub2-parse-route` live | `f.tender_types` seed missing — Counterpoint adapter inserts with `uuid.Nil` and FK fails (Loop 2 finding #7) |
| Receipt hashing | `tsp-seal.md`, `raas.md` | **Shipped Loop 2.** Sub-1 hash-seal binary live; `internal/protocol/hmac/` and `internal/protocol/sub1/` packages present | `cmd/raas` does NOT exist as a binary; raas.md SDD describes a service that has not been built. Hash-seal works without it because Loop 2's sub-1 reimplements the hash-before-parse primitive directly |
| Field capture event ingestion | **Naming collision.** SDD `field-capture.md` covers semantic field-NAME mapping (CSV import discovery via pgvector). Brain card [[Brain/wiki/cards/platform-field-capture]] (v2) covers mobile/voice/process-node operative event capture — a completely different concept | **Not built.** No `cmd/field-capture` binary; no mobile capture pipeline; the "agent at the process node" pattern from the v2 card has no SDD home | **HIGH IMPACT.** The two artifacts share a name but describe different surfaces. Either rename the card, rename the SDD, or write a new SDD for the v2 capability. See §7 |
| Chain entry on receive | `raas.md` (append_event), `tsp-seal.md` (chain hash primitive) | **Partial.** Loop 2's sub-1 hash-seal computes the chain hash; no separate `cmd/raas` binary holds the namespace authority. Append is in-process, not a service call as raas.md specifies | RaaS as a separate service does not exist. Either build it or amend raas.md to acknowledge the embedded model |
| POS failover queue (24-hour SQLite + replay) | **No SDD covers this.** `tsp-seal.md` has server-side DLQ replay (admin-gated). `pos-adapter-substrate.md` and `multi-pos-architecture-proof.md` say nothing about edge-side buffering. The 24-hour invariant is asserted in [[Brain/wiki/cards/platform-performance-nfrs]] only | **Not built.** `cmd/edge/` exists as a directory but contains no SQLite-backed queue logic per Loop 2 inventory | **NEW SDD STUB NEEDED.** "Edge POS adapter local persistence + replay protocol" — see §7 |

**Brain cards mapped to dispatch-M1:**
- [[Brain/wiki/cards/platform-thesis]] (v3) — Rail 3 (no unanchored record) is the chain entry guarantee
- [[Brain/wiki/cards/platform-field-capture]] (v2) — process-node agent thesis; **no SDD**
- [[Brain/wiki/cards/platform-performance-nfrs]] — defines the 5-second field-capture latency invariant, the 24-hour POS failover queue, the <2s MCP write SLA; **no SDD references these targets**
- [[Brain/wiki/cards/platform-proof-case]] — three demonstrations include a hash-chained POS receipt
- [[Brain/wiki/cards/loop2-build-report]] — canonical evidence for what is built

**Top dispatch-M1 gaps:**
1. Field-capture-card vs field-capture-SDD naming collision (highest priority — confuses any future reader and any Loop 3 dispatch).
2. POS failover queue spec missing entirely from the SDD set.
3. RaaS-as-a-service is in the SDD but not in the binaries.
4. NFR targets in [[Brain/wiki/cards/platform-performance-nfrs]] (P99 <2s MCP write, <5s field-capture, 99.9% event durability, 500K events/hour per merchant) are not referenced by any SDD's "Performance Requirements" section.

### 3.2 M2 — Inventory / Receiving Module (per dispatch)

**Scope per dispatch:** ASNaaS; receiving discrepancy event capture; three-way match trigger; receiving field capture at dock door; receiving variance → automatic vendor chargeback routing.

| Capability | SDD coverage | Built-code status | Gap |
|---|---|---|---|
| Three-way match | `three-way-match.md` (334 lines, internal package, no HTTP service) | **Not built.** `internal/threeway` package does not exist; `cmd/receiving` is a `/health` stub per Loop 2 report | SDD is good; build is deferred to Loop 3+ |
| Receiving discrepancy event | `receiving.md` covers `receiving_discrepancies` table, tolerance check, dispute window | **Not built.** Tier-3 module deferred per Loop 2 plan | None — SDD is current |
| Dock-door field capture | **Implied** in `receiving.md` ("dock scan is the truth") but the *mechanism* — voice/photo on phone, process-aware agent, structured event — is in [[Brain/wiki/cards/platform-field-capture]] only | **Not built.** Same root gap as M1 — no field-capture-as-event-capture pipeline exists | Update `receiving.md` §Field Capture or block on the new field-capture-events SDD (§7) |
| ASNaaS | Mentioned in `receiving.md` Multi-tenant context (`asn_documents` table) and depends-on graph; no SDD called `asnaas.md` | **Not built.** No ASN service in cmd/ | Decide whether ASNaaS is a separate service or a feature of receiving. The PwC benchmarks card asserts it as a discrete capability ("ASNaaS is the intake mechanism; EDI is a legacy synonym for what we do via MCP") |
| Receiving variance → vendor chargeback (auto) | **Partial.** `receiving.md` routes discrepancy → Hawk LP alert (not chargeback). `commercial.md` defines chargeback workflow but takes input from invoice deductions, not receiving variance | **Not built.** Both modules are stubs | Auto-routing receiving discrepancy → commercial chargeback is **specified in neither SDD**. The PwC card asserts the platform does it ("70% AP headcount reduction"). Needs a sequence diagram in receiving.md or commercial.md |

**Brain cards mapped to dispatch-M2:**
- [[Brain/wiki/cards/platform-pwc-benchmarks]] — evaluated receipt settlement, 100% automated matching, 70% AP headcount reduction; the proof structure for why the M2 capabilities matter
- [[Brain/wiki/cards/platform-field-capture]] — "47 out of 50" dock-door pattern is the worked example
- [[Brain/wiki/cards/icp-murdochs-reference]] — Murdoch's plant/seed quarantine and live animal listing examples drive the regulatory dimension of receiving
- [[Brain/wiki/cards/loop2-build-report]] — confirms `cmd/inventory` shipped (different from receiving) with UPSERT-in-tx pattern

**Top dispatch-M2 gaps:**
1. The auto-route from receiving variance to vendor chargeback is asserted by the platform thesis but specified in no SDD — neither receiving.md nor commercial.md describes the trigger.
2. ASNaaS as a discrete service vs. as a feature of receiving is unresolved.
3. Field capture at the dock door has the same naming-collision problem as dispatch-M1.

### 3.3 M3 — Commercial / OTB Module (per dispatch)

**Scope per dispatch:** OTB as L402-gated wallet; POaaS; commercial agent commit flow; buyerless buying (agent executes against contracted terms, buyer reviews exceptions only).

| Capability | SDD coverage | Built-code status | Gap |
|---|---|---|---|
| OTB as L402-gated wallet | `l402-otb.md` (389 lines, comprehensive) — wallet schema, scope hierarchy, enforcement levels, satoshi accounting, idempotent set-budget | **Not built.** `cmd/l402-otb` does not exist | SDD is current and detailed; no work needed before build |
| POaaS (Purchase-Order-as-a-Service) | **No SDD called `poaas.md` or `purchasing.md`.** `commercial.md` references vendor relationships; `receiving.md` references PO objects; `l402-otb.md` references PO debits. Nothing owns PO creation as a service | **Not built.** No `cmd/purchasing` or `cmd/poaas` binary | **NEW SDD STUB NEEDED.** PO lifecycle, MCP tool surface, OTB-debit handshake, EDS canonicalization. See §7 |
| Commercial agent commit flow | **Not specified.** `l402-otb.md` describes wallet debits but the *agent* on the other side of those debits — what tool it calls, what context it holds, how it is gated by L402 — is in [[Brain/wiki/cards/platform-thesis]] Rail 2 prose only | **Not built.** No commercial agent exists in cmd/ or as an MCP server | Spec gap. The agent PMO architecture doc (`docs/superpowers/specs/2026-04-28-canary-go-agent-pmo-architecture-design.md`) defines the role but not the commit-flow contract |
| Buyerless buying | **Not specified in any SDD.** Cited in [[Brain/wiki/cards/platform-pwc-benchmarks]] as a 1998 best practice (Fortune 500 electronics manufacturer ran 60% of requisitions buyerless) and asserted in [[Brain/wiki/cards/platform-thesis]] Rail 2 | **Not built.** No exception-routing logic, no auto-commit pathway | **NEW SDD STUB NEEDED.** Buyerless commit policy: thresholds, exception types, escalation routing, buyer-review surface |

**Brain cards mapped to dispatch-M3:**
- [[Brain/wiki/cards/platform-thesis]] v3 — Rail 2 (no unauthorized spend); "Every spend is a settled payment. Every approval is a funded wallet."
- [[Brain/wiki/cards/platform-pwc-benchmarks]] — every benchmark in the AP table maps to an L402-OTB or buyerless-buying capability
- [[Brain/wiki/cards/icp-murdochs-reference]] — multi-state vendor procurement at $200-400M scale is the test case
- [[Brain/wiki/cards/platform-wyoming-ecosystem]] (DRAFT) — Custodia + Frontier Coin as the banking rail for the L402 settlement layer

**Top dispatch-M3 gaps:**
1. POaaS is named in cards (PwC, thesis) and referenced in `l402-otb.md` (debit_otb takes PO scope) but has no SDD home.
2. Buyerless buying as a workflow has no SDD.
3. The commercial agent — what it does, how it commits, what L402 tools it calls — is described as PMO role only, not as an interface contract.
4. L402 settlement against Custodia/Frontier Coin in Wyoming is in the wyoming-ecosystem DRAFT card; no integration SDD exists.

## 4. Per-milestone assessment (canonical labeling)

### 4.1 M1 — Foundation (`identity`, CRDM package, Multi-POS substrate)
- SDDs: `pos-adapter-substrate.md`, `multi-pos-architecture-proof.md`. No standalone `identity.md` or `crdm.md` SDD; CRDM is documented inline in `go-module-layout.md` §CRDM Package.
- Built: Multi-POS substrate ✅ (Loop 2 KEYSTONE — Sub 2 + Square + Counterpoint + Clover). CRDM package present (`internal/db/types/`, 14 schema files, 88 tables). `cmd/identity` ❌ (broken — pre-existing TestHealthEndpoint gated under `//go:build integration` per Loop 2).
- Gap: identity service is on the critical path for tenant isolation and not currently building. Loop 3 dispatch needed.

### 4.2 M2 — Detection Core (`tsp`, `chirp`, `fox`)
- SDDs: `tsp.md`, `tsp-seal.md`, `tsp-parse.md`, `tsp-merkle.md`, `tsp-detect.md`, `chirp.md`, `fox.md` (or implied in canonical-data-model.md per Loop 2 Top-10 #4).
- Built: Sub 1 hash-seal ✅, Sub 2 parse-route ✅, chirp ✅ (all 7 baseline rules, on_event), fox ✅ (29 unit tests, hash chain implemented). All shipped in Loop 2.
- Gap: Subject clustering deferred (fox); `q.subjects` upsert pattern is a Loop 3 prerequisite per Loop 2 report regen P0 #3.

### 4.3 M3 — Intelligence Layer (`owl`, `analytics`)
- SDDs: `owl.md`, `analytics.md`.
- Built: Owl ✅ (read-only, 6 metrics, 14 unit tests, surfaces schema gaps). `cmd/analytics` ❌ (`/health` stub only).
- Gap: Owl SDD has known issues — joins against legacy `app.locations` instead of canonical `l.locations` (Loop 2 Top-10 #10); regen target P1 #6.

### 4.4 M4 — Module Spine (12 binaries)
- SDDs: One SDD per binary in `docs/sdds/go-handoff/` — `hawk-case-management.md`, `bull.md`, `asset.md`, `item.md`, `inventory-as-a-service.md` (note: M4's `inventory` slot is canonically the 8091 binary, but the IaaS SDD is for the 9081 superset), `receiving.md`, `transfer.md` (not present at this path — verify), `pricing.md`, `employee.md`, `customer.md`, `returns.md`, `report.md`.
- Built: Item ✅, Pricing ✅, Inventory ✅ (Loop 2 Wave 2 Tier-1+2). All other Tier-3 binaries are `/health` stubs as planned.
- Gap: Three-way match SDD exists as internal package, but `cmd/receiving` not built. Bull NCR connector is part of M5.

### 4.5 M5 — VAR Delivery (`edge`, Bull NCR connector)
- SDDs: `edge`-specific SDD not present at `docs/sdds/go-handoff/edge.md`; deployment context in `go-module-layout.md` §Edge Agent. Bull SDD covers the NCR connector substrate.
- Built: `cmd/edge/` directory exists but contents per Loop 2 inventory are not Wave-2 scope; Bull is Tier-3 stub.
- Gap: **POS failover queue (24-hour SQLite buffer + replay) belongs here architecturally and is unspec'd.** This is the same gap surfaced under dispatch-M1.

## 5. Cross-cutting findings

These span both framings and need centralized resolution rather than per-module patches.

| Finding | Source | Recommended action |
|---|---|---|
| **`merchant_id` ↔ `tenant_id` divergence** universal across all 7 Loop 2 modules | Loop 2 Top-10 #1 — every module hand-rolls translation at API boundary | Decide: harmonize at SDD level or normalize at gateway. Until then, document the rule in `internal/tenant/` and `architecture.md` |
| **Decimal handling: `amount_cents` int vs `numeric(14,4)`** | Loop 2 Top-10 #9 — every module converts at boundary | Loop 3: pick one. Recommend NUMERIC end-to-end with `shopspring/decimal` |
| **sqlc retrofit deferred** | Loop 2 — all 7 modules used direct pgx + raw SQL strings, contradicting `CanaryGo/CLAUDE.md` rule | Either schedule sqlc retrofit explicitly or amend CLAUDE.md to allow direct pgx for read paths |
| **Field capture has SDD but no built service**, AND the SDD describes a different surface than the v2 Brain card | §3.1 above | Either rename one or write a second SDD. See §7 |
| **Store network integrity card is DRAFT, no built code, AND has TWO Brain cards with different scopes** | [[Brain/wiki/cards/store-network-integrity]] (DRAFT, platform-thesis VSM/security sensor) vs [[Brain/wiki/cards/canary-store-network-integrity]] (approved, domain-module multi-store correlation). The SDD `store-network-integrity.md` matches the *second* card, not the DRAFT | Reconcile the two cards. The DRAFT covers a meaningfully different capability (device manifest, network monitoring, compliance agent) that may warrant its own SDD |
| **L402-OTB SDD is comprehensive, no built code** | l402-otb.md gated by `L402_ENABLED` flag (default false) | No urgent gap; SDD is ready when build sprint reaches it |
| **Wyoming ecosystem card is DRAFT** | [[Brain/wiki/cards/platform-wyoming-ecosystem]] | Pre-pilot strategic context; do not promote to SDD until Lupien/CBDI relationship advances per the card's own "right sequence" |
| **NFR targets are stated in a Brain card, not in any SDD** | [[Brain/wiki/cards/platform-performance-nfrs]] vs zero references in SDDs | Add a §Performance Requirements stub to each module SDD pointing at the card |
| **Schema corrections deferred from Loop 2** | Loop 2 §Schema changes during Loop 2 | Loop 3 should batch: `l.locations.timezone`, `q.cases.closed_at`, `q.detections.cashier_employee_id` FK, `f.tender_types` seed, `app.merchants.tenant_id` non-null, `t.transaction_line_items` partial index |

## 6. DRAFT card review

Two cards from the 2026-04-29 batch carry `status: draft` and `needs-review: true`. Both need founder review before any state-mode dispatch operationalizes them.

### [[Brain/wiki/cards/platform-wyoming-ecosystem]]

**What's there:** four ecosystem layers (CBDI / Frontier Coin / Custodia / Murdoch's), the thesis that Wyoming may be the only place every layer aligns, a five-step right-sequence (academic conversation first, prototype second, paper third, pilot fourth, banking integration fifth).

**What it needs before becoming a build target:**
- Confirmation from founder that the CBDI conversation with Steve Lupien (slupien@uwyo.edu) is being initiated or deferred. The card says "an academic research conversation with CBDI" is the right first move; no Linear issue tracks this yet.
- Decision on whether the Wyoming pilot is a Loop-3-or-later target or a "track strategically, don't build for it yet" item.
- Card explicitly self-identifies as "not a near-term GTM commitment" — that should be preserved if it stays a strategic-track-only artifact.

### [[Brain/wiki/cards/store-network-integrity]] (the platform-thesis variant)

**What's there:** the VSM as security sensor — device manifest, continuous network monitoring (DHCP/ARP), card-skimmer detection pattern, rogue AP detection, default-credential checks, compliance monitoring (SOX, PII, HIPAA, GDPR with tombstoning).

**What it needs before becoming a build target:**
- Reconciliation with the *other* `canary-store-network-integrity` card (approved, domain-module). The two are not duplicates — the DRAFT covers store-side device + compliance monitoring, the approved card covers multi-store transaction correlation. Either rename to clarify scope (e.g., `platform-store-device-integrity` vs `canary-store-network-correlation`) or merge with explicit subsections.
- Decision on whether device manifest / network monitoring is in scope for the platform at all, vs. a third-party SIEM integration. The card asserts it as a unified capability the SMB can't otherwise access; the "right sequence" question is whether GrowDirect builds it or partners.
- Build dependency: requires either store-side agent with local network access OR integration with the store router/switch management API. Neither exists in any SDD. This is a substantial scope decision.

## 7. New SDD stubs needed

These are gaps where a Brain card or dispatch language has no SDD home. Listed in priority order.

| # | Proposed SDD path | Source card / driver | One-line scope |
|---|---|---|---|
| 1 | `docs/sdds/go-handoff/field-capture-events.md` (or rename existing field-capture.md → `field-mapping.md` and reuse the original name) | [[Brain/wiki/cards/platform-field-capture]] v2 | Process-aware agent at process node; mobile/voice operative input → canonical event template → hash chain entry within 5s |
| 2 | `docs/sdds/go-handoff/edge-pos-failover.md` | [[Brain/wiki/cards/platform-performance-nfrs]] §POS write path failover | Edge POS adapter local persistence (24-hour SQLite buffer) + replay protocol on reconnect; original-capture timestamp preservation |
| 3 | `docs/sdds/go-handoff/poaas.md` (or `purchasing.md`) | [[Brain/wiki/cards/platform-pwc-benchmarks]], dispatch M3 | PO lifecycle as a service; MCP tool surface; OTB debit handshake with l402-otb; EDS canonicalization for vendor consumption |
| 4 | `docs/sdds/go-handoff/buyerless-buying.md` | [[Brain/wiki/cards/platform-pwc-benchmarks]], [[Brain/wiki/cards/platform-thesis]] Rail 2 | Auto-commit policy; threshold and exception classification; buyer-review escalation surface; integration with commercial agent |
| 5 | `docs/sdds/go-handoff/commercial-agent-commit-flow.md` | dispatch M3, [[Brain/wiki/cards/platform-thesis]] Rail 2 | The commit-side interface contract for the commercial PMO agent — what tools, what context, what L402 gating. Could fold into commercial.md as a §Agent Interface section |
| 6 | `docs/sdds/go-handoff/asnaas.md` (decision: standalone or fold into receiving.md) | [[Brain/wiki/cards/platform-pwc-benchmarks]] | Vendor ASN intake; "100% via EDI / MCP" claim; ASN hash for three-way match input |
| 7 | `docs/sdds/go-handoff/store-device-integrity.md` (if DRAFT card promotes) | [[Brain/wiki/cards/store-network-integrity]] DRAFT | Device manifest, network monitoring, compliance agent — DISTINCT from the existing store-network-integrity.md SDD which is correlation. Pending §6 reconciliation |

## 8. State-mode follow-up dispatches recommended

These are dispatch ideas, not drafts. Each is one paragraph describing scope; the actual dispatch text is for the founder to write per the dispatch protocol (Linear issue, Target/<machine> label, agent label, priority).

1. **Reconcile field-capture naming collision** — Decide whether the SDD `field-capture.md` (semantic field-NAME mapping) and the Brain card `platform-field-capture.md` (mobile/process-node event capture) keep the shared name with disambiguation, or one renames. Update affected SDDs (receiving.md, raas.md cross-references) accordingly. Module: docs hygiene. Scope: doc-only, no code.
2. **Reconcile two store-network-integrity cards** — Rename one of [[Brain/wiki/cards/store-network-integrity]] (DRAFT, platform thesis) or [[Brain/wiki/cards/canary-store-network-integrity]] (approved, domain module) so the scope difference is unambiguous. Update SDD cross-references. Module: docs hygiene. Scope: card frontmatter + cross-refs.
3. **Document the merchant_id/tenant_id contract** — Add a §Multi-tenant identifier convention to `architecture.md` or `internal/tenant/CLAUDE.md` so future modules don't re-discover this at every boundary. Reference Loop 2 Top-10 #1. Module: cross-cutting. Scope: doc-only.
4. **Write field-capture-events SDD** — Per §7 #1. The Brain card v2 has the architecture; transcribe to SDD format with API surface, table schema, MCP tools, latency targets. Module: new SDD. Scope: doc + future build.
5. **Write edge-pos-failover SDD** — Per §7 #2. Required before any merchant pilot that has unreliable connectivity (which is most of them). Module: new SDD. Scope: doc + future build.
6. **Write POaaS SDD** — Per §7 #3. Currently the PO object is referenced by receiving.md, l402-otb.md, and commercial.md without a single SDD owning its lifecycle. Module: new SDD. Scope: doc + future build.
7. **Add Performance Requirements section to each module SDD** — Cross-reference [[Brain/wiki/cards/platform-performance-nfrs]] with the per-tool SLA targets. Each SDD's section is short (a table + cross-link). Module: docs hygiene across ~20 SDDs. Scope: doc-only.
8. **Decide POaaS / ASNaaS standalone vs. folded** — Architecture decision dispatch before §7 #3 and §7 #6 SDDs commit to layout. Module: architecture decision (ADR candidate). Scope: decision doc, possibly an `engineering:architecture` skill ADR.
9. **Loop 3 schema batch** — Roll the deferred schema additions from Loop 2 §Schema changes during Loop 2 into a single migration: timezone, q.cases.closed_at, q.detections FK, f.tender_types seed, app.merchants.tenant_id non-null, t.transaction_line_items partial index. Module: schema. Scope: code.
10. **L402 + Custodia/Frontier Coin integration scoping** — Block until the wyoming-ecosystem card promotes from DRAFT. When it does, pair l402-otb.md with a Custodia integration SDD. Module: new SDD. Scope: gated on §6 founder decision.

## 9. Definition of Done check (against dispatch evaluation criteria)

| Dispatch criterion | Status |
|---|---|
| For each module: SDD exists and is current; reflects current architecture including EDS/RaaS namespace model | **Partial.** Receiving SDD ✅ current. l402-otb SDD ✅ current. Commercial SDD ✅ current but commit-flow not specified. Field-capture SDD covers the wrong surface relative to dispatch intent. RaaS SDD describes a service that is not built. POaaS, buyerless buying, edge-failover, field-capture-events have no SDD at all. |
| For each module: code matches SDD; check CanaryGo/ for implemented vs specified | **Mixed.** Loop 2 shipped 7 Tier-1+2 modules (item, pricing, inventory, sub2, chirp, fox, owl) that match their SDDs with the cross-cutting findings noted. All M2-Receiving and M3-Commercial code is unbuilt; gap is at the spec/decision level, not at code-vs-spec divergence. |
| For each module: gaps — what is in Brain cards but not in any SDD | **Documented in §7.** Seven new SDD stubs listed. |
| New card integration: do new cards need corresponding SDD sections before build work can begin | **Yes for: field-capture v2 (rename or new SDD), performance-NFRs (per-SDD section), pwc-benchmarks (POaaS, buyerless), store-network-integrity DRAFT (post-reconciliation). No for: thesis v3 (cross-cutting governance), proof-case (governance), icp-murdochs (reference, not buildable), wyoming-ecosystem (DRAFT, gated).** |
| Flag DRAFT cards for founder review | **Done in §6.** wyoming-ecosystem and store-network-integrity DRAFT both flagged with what each needs before becoming a build target. |
| Output deliverable at `docs/superpowers/plans/2026-04-29-m1-m2-m3-coverage-assessment.md` | ✅ this document. |

## 10. Cross-references

**Brain cards (8 from 2026-04-29 batch + supporting):**
- [[Brain/wiki/cards/platform-thesis]] (v3, latest — note: dispatch said v2)
- [[Brain/wiki/cards/icp-murdochs-reference]]
- [[Brain/wiki/cards/platform-proof-case]]
- [[Brain/wiki/cards/platform-wyoming-ecosystem]] (DRAFT)
- [[Brain/wiki/cards/platform-field-capture]] (v2)
- [[Brain/wiki/cards/platform-performance-nfrs]]
- [[Brain/wiki/cards/platform-pwc-benchmarks]]
- [[Brain/wiki/cards/store-network-integrity]] (DRAFT — platform-thesis variant)
- [[Brain/wiki/cards/canary-store-network-integrity]] (approved — domain-module variant)
- [[Brain/wiki/cards/loop2-build-report]] (gold-standard "code matches SDD" evidence as of 2026-05-02)

**SDDs reviewed:**
- `docs/sdds/go-handoff/go-module-layout.md` — canonical milestone-to-binary mapping (§4 source)
- `docs/sdds/go-handoff/receiving.md` — M2 receiving + three-way-match trigger
- `docs/sdds/go-handoff/three-way-match.md` — internal package, no HTTP service
- `docs/sdds/go-handoff/l402-otb.md` — wallet, scope hierarchy, satoshi accounting
- `docs/sdds/go-handoff/field-capture.md` — semantic field-NAME mapping (NOT event capture)
- `docs/sdds/go-handoff/commercial.md` — vendor relationship layer
- `docs/sdds/go-handoff/multi-pos-architecture-proof.md` — M1 substrate
- `docs/sdds/go-handoff/pos-adapter-substrate.md` — adapter contract
- `docs/sdds/go-handoff/raas.md` — namespace + chain authority
- `docs/sdds/go-handoff/tsp.md`, `tsp-seal.md` — receipt hashing pipeline
- `docs/sdds/go-handoff/store-network-integrity.md` — multi-store correlation (NOT device monitoring)
- `docs/sdds/go-handoff/inventory-as-a-service.md` — IaaS superset of M4 inventory slot

**Built code references:**
- `CanaryGo/cmd/` — 24 binary directories; 10 have real handlers (gateway, sub1-hash-seal, sub2-parse-route, identity[broken], item, pricing, inventory, chirp, fox, owl, hello, dbcheck), rest are `/health` stubs
- `CanaryGo/internal/adapters/{adapter,square,counterpoint,clover}/` — Loop 2 multi-POS substrate
- `CanaryGo/internal/protocol/{audit,evidence,hmac,publisher,secrets,sub1,sub2,webhook}/` — protocol pipeline
- `CanaryGo/internal/db/types/` — 14 schema-aligned Go struct files (Loop 1 Wave 1)
- `CanaryGo/deploy/schema/00-11_*.sql + 99_seed.sql` — declarative schema, 88 tables, 14 schemas

**Linear:**
- GRO-684 — this assessment (parent dispatch)
- GRO-739 — Canary protocol gateway live on GCP (parent of Loop 2)
- GRO-761 — Loop 2 mission

**Specs / plans:**
- `docs/superpowers/specs/2026-04-28-canary-go-agent-pmo-architecture-design.md` — agent PMO network architecture
- `docs/superpowers/plans/2026-04-28-canary-go-m1-foundation.md` — M1 (canonical) foundation plan
- `docs/superpowers/plans/2026-05-02-canary-protocol-phase1-execution-plan.md` — Phase 1 execution
