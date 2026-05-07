---
tags: [canary, go, portal, moc]
last-compiled: 2026-05-04
needs-review: 2026-05-18
---

# Canary Go — Project Portal

The production Go rebuild of the Canary platform. ARTS-native, NCR Counterpoint-first, 13-module spine. The Python prototype (tagged `v0-python-prototype`) is reference only — all active development is here.

**Linear:** [Canary Go](https://linear.app/growdirect/project/canary-go-9fb99af5b6af) · [RapidPOS Inbound](https://linear.app/growdirect/project/rapidpos-inbound-74436ec08ce9) · [RapidPOS Channel Initiative](https://linear.app/growdirect/initiative/rapidpos-channel-b811763ef7e5)

---

## Architecture SDDs

All specs in `docs/sdds/go-handoff/`. Read in this order:

### Product Definition
- [[docs/sdds/go-handoff/platform-overview|Platform Overview]] — what Canary is, who it serves. Read first.
- [[docs/sdds/go-handoff/multi-pos-architecture-proof|Multi-POS Architecture Proof]] — why the design is POS-agnostic

### System Architecture
- [[docs/sdds/go-handoff/microservice-architecture|Microservice Architecture]] — 10 Go services, ports, table ownership, inter-service comms
- [[docs/sdds/go-handoff/architecture|Architecture]] — logical service design, runtime topology

### Data Model
- [[docs/sdds/go-handoff/data-model|Data Model]] — 82 tables across app / sales / metrics schemas (sqlc source of truth)
- [[docs/sdds/go-handoff/external-identities|External Identities]] — POS-native ID → Canary canonical ID mapping
- [[docs/sdds/go-handoff/identity|Identity]] — merchant, user, tenant model; auth + session contracts

### Ingestion Pipeline
- [[docs/sdds/go-handoff/webhook-pipeline|Webhook Pipeline]] — receipt → HMAC → stream → seal → parse → merkle → detect
- [[docs/sdds/go-handoff/tsp|TSP]] — orchestration detail, message envelope, idempotency, backpressure

### Detection and Cases
- [[docs/sdds/go-handoff/chirp|Chirp]] — 37 detection rules across 10 categories with SQL contracts
- [[docs/sdds/go-handoff/alert|Alert]] — alert lifecycle state machine, REST endpoints
- [[docs/sdds/go-handoff/fox|Fox]] — case management, evidence hash chain, append-only invariant

### Intelligence Layer
- [[docs/sdds/go-handoff/owl|Owl]] — pgvector search, Risk Dictionary, EJ Spine entity resolution
- [[docs/sdds/go-handoff/analytics|Analytics]] — metric rollups, risk scoring, baseline computation

### POS Adapters
- [[docs/sdds/go-handoff/pos-adapter-substrate|POS Adapter Substrate]] — interface every POS integration must implement
- [[docs/sdds/go-handoff/hawk|Hawk]] — Square adapter (reference implementation)
- [[docs/sdds/go-handoff/bull|Bull]] — NCR Counterpoint adapter (polling model, REST key auth)

### Store Operations Layer
- [[docs/sdds/go-handoff/store-brain|Store Brain (:9085)]] — presence resolution, session governance, MCP tool permission gating
- [[docs/sdds/go-handoff/ops-dashboard|Ops Dashboard (:9084)]] — device health NOC, MCP health grid, SSE
- [[docs/sdds/go-handoff/store-network-integrity|Store Network Integrity (:9088)]] — cross-location anomaly detection
- [[docs/sdds/go-handoff/compliance|Compliance (:9091)]] — item authorization × regulatory zone × operational blocks; `canary-compliance` MCP (7 tools)

### Module Layout
- [[docs/sdds/go-handoff/go-module-layout|Go Module Layout]] — 20-service monorepo, port map, CRDM package, sqlc conventions

---

## Agent Knowledge Substrate

Cards in `Brain/wiki/cards/` are the semantic knowledge layer for the platform. Agents recall them via the memory bus.

**Platform thesis and mission:** `Brain/wiki/cards/platform-thesis.md`
**Format spec and full index:** `Brain/wiki/agent-card-format.md`
**Key cards:** merchant-org-hierarchy · geography-hierarchy · category-hierarchy · role-binding-model · local-market-agent · platform-retailer-lifecycle-test

**Recall at session start:**
```
memory_recall("platform thesis accountability meter model")
memory_recall("canary go architecture agent PMO spine")
context_assemble(topic="canary go platform")
```

---

## 13-Module Spine

All manifests in `GrowDirect-CRB/modules/`. Each has a `.manifest.yaml` (design spec) and a `.md` (narrative).

| Module | Manifest | Narrative |
|--------|----------|-----------|
| T — Transaction Pipeline | [[GrowDirect-CRB/modules/T-transaction-pipeline.manifest]] | [[GrowDirect-CRB/modules/T-transaction-pipeline]] |
| C — Customer | [[GrowDirect-CRB/modules/R-customer.manifest]] | [[GrowDirect-CRB/modules/R-customer]] |
| N — Device | [[GrowDirect-CRB/modules/N-device.manifest]] | [[GrowDirect-CRB/modules/N-device]] |
| A — Asset Management | [[GrowDirect-CRB/modules/A-asset-management.manifest]] | [[GrowDirect-CRB/modules/A-asset-management]] |
| Q — Loss Prevention | [[GrowDirect-CRB/modules/Q-loss-prevention.manifest]] | [[GrowDirect-CRB/modules/Q-loss-prevention]] |
| M — Merchandising | [[GrowDirect-CRB/modules/C-commercial.manifest]] | [[GrowDirect-CRB/modules/C-commercial]] |
| D — Distribution | [[GrowDirect-CRB/modules/D-distribution.manifest]] | [[GrowDirect-CRB/modules/D-distribution]] |
| F — Finance | [[GrowDirect-CRB/modules/F-finance.manifest]] | [[GrowDirect-CRB/modules/F-finance]] |
| O — Orders | [[GrowDirect-CRB/modules/J-forecast-order.manifest]] | [[GrowDirect-CRB/modules/J-forecast-order]] |
| S — Space, Range & Display | [[GrowDirect-CRB/modules/S-space-range-display.manifest]] | [[GrowDirect-CRB/modules/S-space-range-display]] |
| P — Pricing & Promotion | [[GrowDirect-CRB/modules/P-pricing-promotion.manifest]] | [[GrowDirect-CRB/modules/P-pricing-promotion]] |
| L — Labor | [[GrowDirect-CRB/modules/L-labor-workforce.manifest]] | [[GrowDirect-CRB/modules/L-labor-workforce]] |
| E — Execution | [[GrowDirect-CRB/modules/W-work-execution.manifest]] | [[GrowDirect-CRB/modules/W-work-execution]] |

---

## Wireframe Brief Library

Screen-level design briefs for every Canary Go portal screen — 110 screens across 6 groups. All briefs in `docs/superpowers/briefs/`. Each brief covers: layout, key elements, interaction flows, CP crosswalk (UX displacement target), and open questions.

| Group | Wave | Screens | Directory |
|-------|------|---------|-----------|
| Group 0 — Admin + DevOps | Admin (cross-wave) | ~15 | `docs/superpowers/briefs/admin/` |
| Group 1 — LP Core | W1 | 25 | `docs/superpowers/briefs/wave-1/` |
| Group 2 — Store Ops + Devices | W2 | 30 | `docs/superpowers/briefs/wave-2/` |
| Group 3 — Finance + Purchasing + Planning | W3 | 21 | `docs/superpowers/briefs/wave-3/` |
| Group 4 — Merch + Labor | W4 | 13 | `docs/superpowers/briefs/wave-4/` |
| Group 5 — W-Execution (Dashboard + Settings) | W5 | 9 | `docs/superpowers/briefs/wave-5/` |

**Notable design decisions captured in briefs:**

- **Count entry hidden-expected-quantity** (`wave-2/inventory-count-entry.md`) — counters never see expected quantity; integrity constraint, not a missing feature
- **LP substrate completeness gate** (`wave-1/settings-store-drawer.md`) — missing substrate row = detection rule silent for that location; "Missing — rule silent" state surfaced in settings
- **Exception vs Alert distinction** (`wave-5/exceptions-list.md`) — Exceptions are a curated queue of confirmed anomalies elevated from raw alerts; not the same thing
- **OTB real-time impact panel** (`wave-3/orders-new.md`) — budget impact shows in right rail as the buyer types the PO; L4 structural addition with no CP equivalent
- **Distribution Recommendations proximity weighting** (`wave-3/distribution-recommendations.md`) — rebalancing queue uses store geo-coordinates for routing logic
- **Vertical pack configuration** (`wave-5/settings-vertical-pack.md`) — Garden+Nursery default; "Overridden" labels track manual deviations from pack defaults

**CP crosswalk coverage:** 10 UX displacement targets documented across Wave 1–3 briefs. Every UX Callout section contrasts Canary's approach against the CP equivalent workflow.

---

## Wave 1 Build Track

Wave 1 = LP Core — the 25 screens that form the operational detection + investigation surface. Backend packages are implemented; the build track wires them to the web UI layer.

**Implementation plan:** `docs/superpowers/plans/2026-05-04-canary-go-wave-1-implementation-plan.md`

**Key gaps the plan addresses:**

1. `detection` schema (detection_rules, detections, lp_substrate, allow_list) does not exist in active migrations — gap in 019–023 sequence; plan adds migration 024
2. `web.Handler.New(logger)` accepts only a logger — all handlers return hardcoded stubs; needs `web.Deps` struct with store dependencies
3. New `internal/lp/substrate.go` package needed for LP substrate and allow-list settings pages

**Active dispatches (GRO-788 – GRO-796):**

| Ticket | Title | Depends on |
|--------|-------|------------|
| [GRO-788](https://linear.app/growdirect/issue/GRO-788) | Detection schema migration (024) | — |
| [GRO-789](https://linear.app/growdirect/issue/GRO-789) | Dependency injection refactor — web.Deps + handler.New() | — |
| [GRO-790](https://linear.app/growdirect/issue/GRO-790) | Wire alert handlers — list + detail | GRO-788, GRO-789 |
| [GRO-791](https://linear.app/growdirect/issue/GRO-791) | Wire chirp handlers — live feed + transaction detail | GRO-788, GRO-789 |
| [GRO-792](https://linear.app/growdirect/issue/GRO-792) | Wire detection rules handlers — list + detail | GRO-788, GRO-789 |
| [GRO-793](https://linear.app/growdirect/issue/GRO-793) | Wire Hawk case handlers — list + detail + evidence | GRO-788, GRO-789 |
| [GRO-794](https://linear.app/growdirect/issue/GRO-794) | Wire customer handlers — lookup + risk + context | GRO-788, GRO-789 |
| [GRO-795](https://linear.app/growdirect/issue/GRO-795) | LP substrate package — internal/lp + settings pages | GRO-788, GRO-789 |
| [GRO-796](https://linear.app/growdirect/issue/GRO-796) | Integration smoke tests — all wired handlers | GRO-790–795 |

**Auth gap (not in Wave 1 scope):** GRO-769 — `tenantIDFromCtx` returns `uuid.Nil` until identity middleware is wired. Wave 1 handlers use this stub; multi-tenant isolation is deferred to GRO-769.

---

## Vendor Crosswalks

- [[Brain/wiki/canary-go-square-crosswalk|Canary Go ↔ Square — Vendor Crosswalk]] — adapter, cadence, cost-model mapping for the Square POS

## Key Invariants

1. UUID primary keys everywhere — `gen_random_uuid()` default
2. Schema-qualified writes — `app.`, `sales.`, `metrics.` — never unqualified
3. Tenant isolation — every merchant query has `WHERE merchant_id = $1`
4. Append-only evidence — `fox.evidence_records` has a DB trigger blocking UPDATE/DELETE
5. Idempotent pipeline — duplicate events produce the same result, not duplicate rows
6. pgvector in-database — no external vector store
7. REST throughout — no gRPC
8. Agent-driven by default — HIL is escalation, not the default path

---

## Stack

| Layer | Choice |
|-------|--------|
| Database | PostgreSQL 17 |
| Driver | pgx |
| Query layer | sqlc |
| HTTP router | Chi |
| Internal comms | REST |
| Vector store | pgvector |
| Cache / queue | go-redis (Valkey-compatible) |
| Migrations | golang-migrate or goose |

---

# Service Inventory

Machine-readable inventory consumed by `services/canary-protocol/manifest/gen/parse_manifest.py`. Each `## <name>` block declares a service's port, owner, capability card, cell occupancy on the cadence-ladder grid, and endpoint set. Phase 2 backfills the remaining 28 services (one PR per service); the 5 below are the Phase 1 skeleton.

Grammar (per design spec §"Manifest schema"):

```
## <name> · :<port> · <category> · <P0|P1|P2>

Owner: <agent>  ·  Card: Brain/wiki/cards/<name>.md  ·  Cells: [<axis> × <tier>] [<axis> × <tier>]
<scope>  ·  Python prior art: <path or "none">

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
| /v1/... | METHOD | tier | axis | auth | mounted|proposed|drift | one line |
```

Tier values: `stream` · `change-feed` · `daily-batch` · `bulk-window` · `reference`.
Axis values: `A` (Adapter — POS → Canary) · `B` (Resource — Canary → external) · `C` (Agent — Canary → AI agents).

## catalog · :9100 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/catalog.md  ·  Cells: [B × reference]
cross-tenant  ·  Python prior art: none

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /devops/catalog | GET | reference | B | apikey | proposed | 3×5 grid heat-map UI |
| /v1/catalog/services | GET | reference | B | apikey | proposed | service list (JSON) |
| /v1/catalog/cells | GET | reference | B | apikey | proposed | endpoints per cell |

## manifest · :9101 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/manifest.md  ·  Cells: [B × reference]
cross-tenant  ·  Python prior art: none

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /devops/manifest | GET | reference | B | apikey | proposed | manifest editor + validator |
| /v1/manifest/yaml | GET | reference | B | apikey | proposed | raw manifest.yaml |
| /v1/manifest/history | GET | reference | B | apikey | proposed | version history |

## observability · :9102 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/observability.md  ·  Cells: [B × change-feed] [B × reference]
cross-tenant  ·  Python prior art: none

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /devops/observability | GET | reference | B | apikey | proposed | five-tier health rollup UI |
| /v1/observability/health | GET | change-feed | B | apikey | proposed | per-tier health JSON |
| /v1/observability/lag | GET | change-feed | B | apikey | proposed | queue lag + watermark |

## pipeline · :9103 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/pipeline.md  ·  Cells: [B × change-feed]
cross-tenant  ·  Python prior art: Canary/canary/services/devops_monitor.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /devops/pipeline | GET | change-feed | B | apikey | proposed | TSP pipeline visualization |
| /v1/pipeline/runs | GET | change-feed | B | apikey | proposed | recent webhook → sub3 traces |
| /v1/pipeline/sub3 | GET | change-feed | B | apikey | proposed | anchor batch status |

## qa-agent · :9104 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/qa-agent.md  ·  Cells: [C × change-feed]
cross-tenant  ·  Python prior art: Canary/canary/qa_agent/

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /devops/qa-agent | GET | change-feed | C | apikey | proposed | page-aware operator agent UI |
| /v1/qa-agent/sessions | GET | change-feed | C | apikey | proposed | active session list |
| /v1/qa-agent/sessions | POST | change-feed | C | apikey | proposed | start a QA session |
| /v1/qa-agent/findings | GET | change-feed | C | apikey | proposed | bug findings + Linear filings |
