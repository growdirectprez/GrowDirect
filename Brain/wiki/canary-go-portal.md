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
4. Append-only evidence — `protocol.evidence` and `app.audit_log` have DB triggers blocking UPDATE/DELETE/TRUNCATE (`deploy/schema/11_protocol.sql`, `deploy/migrations/031_audit_log_append_only.up.sql`). Note: the prior wording referenced `fox.evidence_records`, which never carried the trigger — invariant claim repaired in Sprint 2 T-F (GRO-851).
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

## evidence · :9201 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/evidence.md  ·  Cells: [B × reference]
cross-tenant  ·  Python prior art: Canary/canary/services/evidence_service.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /v1/protocol/evidence/{event_hash} | GET | reference | B | none | mounted | append-only audit lookup |
| /devops/evidence | GET | reference | B | apikey | proposed | evidence query UI |

## anchor · :9202 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/anchor.md  ·  Cells: [B × reference]
cross-tenant  ·  Python prior art: Canary/canary/services/anchor_service.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /v1/protocol/anchor/{event_hash} | GET | reference | B | none | mounted | Merkle proof for blockchain anchor |
| /devops/anchor | GET | reference | B | apikey | proposed | anchor batch viewer |

## mcp · :9203 · cross-tenant infra · P0

Owner: ALX  ·  Card: Brain/wiki/cards/mcp.md  ·  Cells: [C × change-feed]
cross-tenant  ·  Python prior art: none

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /mcp | POST | change-feed | C | apikey | mounted | MCP JSON-RPC 2.0 invocation surface |
| /.well-known/mcp.json | GET | reference | C | none | mounted | MCP discovery document |
| /devops/mcp | GET | change-feed | C | apikey | proposed | tool catalog + usage drill-down |

## dashboard · :9300 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/dashboard.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/dashboard.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /dashboard | GET | reference | B | session | mounted | LP merchant home — KPI rollup |

## alert · :8087 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/alert.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/alerts.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /alerts | GET | change-feed | B | session | mounted | alert list |
| /alerts/{id} | GET | change-feed | B | session | mounted | alert detail + lineage |

## chirp · :8081 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/chirp.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/chirps.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /chirps | GET | change-feed | B | session | mounted | chirp feed |
| /chirps/{id} | GET | change-feed | B | session | mounted | chirp + transaction detail |

## casemgmt · :9303 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/casemgmt.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/cases.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /cases | GET | change-feed | B | session | mounted | case list |
| /cases/new | GET | change-feed | B | session | mounted | new case form |
| /cases/{id}/correlation | GET | change-feed | B | session | mounted | cross-store correlation |
| /cases/{id}/evidence | GET | change-feed | B | session | mounted | evidence chain viewer |
| /cases/{id}/remediate | GET | change-feed | B | session | mounted | remediation workflow |
| /cases/hawk | GET | change-feed | B | session | mounted | Hawk-flagged case queue |
| /cases/hawk | POST | change-feed | B | session | mounted | escalate Hawk case |
| /cases/hawk/new | GET | change-feed | B | session | mounted | new Hawk case form |
| /cases/hawk/analytics | GET | change-feed | B | session | mounted | Hawk pattern analytics |
| /cases/hawk/patterns | GET | change-feed | B | session | mounted | repeat-offender patterns |
| /cases/hawk/{id} | GET | change-feed | B | session | mounted | Hawk case detail |
| /cases/hawk/{id}/evidence | GET | change-feed | B | session | mounted | Hawk evidence viewer |

## customer · :8091 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/customer.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/customers.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /customers | GET | reference | B | session | mounted | customer list |
| /customers/{id} | GET | reference | B | session | mounted | customer detail |
| /customers/{id}/context | GET | reference | B | session | mounted | purchase + return history |
| /customers/{id}/risk | GET | reference | B | session | mounted | RFM + risk score |

## transaction · :9305 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/transaction.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/transactions.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /transactions | GET | reference | B | session | mounted | transaction list |
| /transactions/{id} | GET | reference | B | session | mounted | transaction detail |
| /transactions/{id}/proof | GET | reference | B | session | mounted | protocol evidence link |

## rule · :9306 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/rule.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/detection_rules.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /rules | GET | reference | B | session | mounted | detection rule list |
| /rules/{id} | GET | reference | B | session | mounted | rule detail |

## lp-settings · :9307 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/lp-settings.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/settings.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /settings/store | GET | reference | B | session | mounted | LP store config home |
| /settings/store/drawer | GET | reference | B | session | mounted | drawer substrate list |
| /settings/store/drawer | POST | reference | B | session | mounted | add drawer entry |
| /settings/store/drawer/{id}/delete | POST | reference | B | session | mounted | delete drawer entry |
| /settings/store/comp-reasons | GET | reference | B | session | mounted | comp reasons list |
| /settings/store/comp-reasons | POST | reference | B | session | mounted | add comp reason |
| /settings/store/comp-reasons/{id}/delete | POST | reference | B | session | mounted | delete comp reason |
| /settings/store/void-reasons | GET | reference | B | session | mounted | void reasons list |
| /settings/store/void-reasons | POST | reference | B | session | mounted | add void reason |
| /settings/store/void-reasons/{id}/delete | POST | reference | B | session | mounted | delete void reason |
| /settings/store/discounts | GET | reference | B | session | mounted | discount substrate |
| /settings/store/discounts | POST | reference | B | session | mounted | add discount |
| /settings/store/discounts/{id}/delete | POST | reference | B | session | mounted | delete discount |
| /settings/allowlist/voids | GET | reference | B | session | mounted | void allow-list |
| /settings/allowlist/voids | POST | reference | B | session | mounted | add to void allow-list |
| /settings/allowlist/voids/{id}/delete | POST | reference | B | session | mounted | remove from void allow-list |
| /settings/allowlist/discounts | GET | reference | B | session | mounted | discount allow-list |
| /settings/allowlist/discounts | POST | reference | B | session | mounted | add to discount allow-list |
| /settings/allowlist/discounts/{id}/delete | POST | reference | B | session | mounted | remove from discount allow-list |
| /settings/allowlist/comps | GET | reference | B | session | mounted | comp allow-list |
| /settings/allowlist/comps | POST | reference | B | session | mounted | add to comp allow-list |
| /settings/allowlist/comps/{id}/delete | POST | reference | B | session | mounted | remove from comp allow-list |
| /settings/allowlist/dead-count | GET | reference | B | session | mounted | dead-count allow-list |
| /settings/allowlist/dead-count | POST | reference | B | session | mounted | add to dead-count allow-list |
| /settings/allowlist/dead-count/{id}/delete | POST | reference | B | session | mounted | remove from dead-count allow-list |
| /settings/training-mode | GET | reference | B | session | mounted | training-mode flag list |
| /settings/training-mode | POST | reference | B | session | mounted | add training-mode flag |
| /settings/training-mode/{id}/delete | POST | reference | B | session | mounted | clear training-mode flag |
| /settings/alert-routing | GET | reference | B | session | mounted | alert routing rules |
| /settings/alert-routing | POST | reference | B | session | mounted | add alert routing rule |
| /settings/alert-routing/{id}/delete | POST | reference | B | session | mounted | delete alert routing rule |

## owl · :8084 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/owl.md  ·  Cells: [C × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/owl.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /owl | GET | change-feed | C | session | mounted | semantic search home (pgvector + EJ spine) |
| /owl/dashboards | GET | change-feed | C | session | mounted | saved dashboard registry |
| /owl/parties | GET | change-feed | C | session | mounted | party (entity) directory + risk dictionary |
| /owl/lp-performance | GET | change-feed | C | session | mounted | LP rule performance rollup |

## employee · :8095 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/employee.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/employees.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /employees | GET | reference | B | session | mounted | employee directory (stub, W2 wired) |
| /employees/{id} | GET | reference | B | session | mounted | employee detail + risk score |

## item · :8090 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/item.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/items.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /items | GET | reference | B | session | mounted | item master list (catalog browse) |
| /items/{id} | GET | reference | B | session | mounted | item detail + UPC + pricing tier |

## transfer · :8093 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/transfer.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/transfers.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /transfers | GET | change-feed | B | session | mounted | inter-store transfer list |
| /transfers/{id} | GET | change-feed | B | session | mounted | transfer detail + line items |
| /transfers/{id}/variance | GET | change-feed | B | session | mounted | variance reconciliation |

## receiving · :8092 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/receiving.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/receiving.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /receiving | GET | change-feed | B | session | mounted | open receiving queue |
| /receiving/{id} | GET | change-feed | B | session | mounted | receiving detail + line items |
| /receiving/{id}/close | GET | change-feed | B | session | mounted | close-receipt confirmation |
| /receiving/{id}/close | POST | change-feed | B | session | mounted | close receipt + post variance |
| /receiving/{id}/lines/{lineID}/discrepancy | POST | change-feed | B | session | mounted | log line-item discrepancy |

## returns · :8097 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/returns.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/returns.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /returns | GET | change-feed | B | session | mounted | returns queue |
| /returns/{id} | GET | change-feed | B | session | mounted | return detail + refund authorization |

## pricing · :8094 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/pricing.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/promotions.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /promotions | GET | reference | B | session | mounted | promotions calendar (W2f) |

## task · :9311 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/task.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: none

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /tasks | GET | change-feed | B | session | mounted | directed-task queue (W5) |
| /tasks/{id}/claim | POST | change-feed | B | session | mounted | claim task for current operator |
| /tasks/{id}/complete | POST | change-feed | B | session | mounted | mark task complete |
| /tasks/{id}/exception | POST | change-feed | B | session | mounted | log task exception |

## asset · :8089 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/asset.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/assets.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /assets | GET | reference | B | session | mounted | asset registry list (W8) |
| /assets/{id} | GET | reference | B | session | mounted | asset detail + lifecycle + location |

## report · :8098 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/report.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/reports.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /reports | GET | reference | B | session | mounted | reports index (stub) |
| /reports/distribution | GET | reference | B | session | mounted | distribution rebalancing report (W2b) |
| /reports/inventory | GET | reference | B | session | mounted | inventory health report (W2b) |
| /reports/category | GET | reference | B | session | mounted | category performance report (W2c) |
| /reports/finance | GET | reference | B | session | mounted | finance summary report (W2e) |
| /reports/payments | GET | reference | B | session | mounted | tender mix report (stub — needs aggregation) |
| /reports/tax | GET | reference | B | session | mounted | tax remit report (W2e) |
| /reports/otb | GET | reference | B | session | mounted | open-to-buy budget report (W2e) |
| /reports/labor | GET | reference | B | session | mounted | labor utilization report (W2g) |
| /reports/cases | GET | reference | B | session | mounted | cases analytics report (W2e) |
| /reports/range | GET | reference | B | session | mounted | range performance report (stub) |
| /reports/pricing | GET | reference | B | session | mounted | pricing position report (stub) |
| /reports/price-history | GET | reference | B | session | mounted | price-history report (stub) |
| /reports/markdowns | GET | reference | B | session | mounted | markdown effectiveness report (stub) |
| /reports/otb/{budgetID}/lock | POST | reference | B | session | mounted | lock OTB budget (W5 action) |

## billing · :9312 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/billing.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/billing.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /billing/overview | GET | reference | B | session | mounted | billing portal home (meter rollup) — W8 |
| /billing/invoices | GET | reference | B | session | mounted | invoice history |
| /billing/payment-method | GET | reference | B | session | mounted | payment-method viewer |

## supplier · :9313 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/supplier.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/suppliers.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /suppliers | GET | change-feed | B | session | mounted | supplier directory (W11) |
| /suppliers | POST | change-feed | B | session | mounted | create supplier |
| /suppliers/{id} | GET | change-feed | B | session | mounted | supplier detail |
| /suppliers/{id}/scorecard | GET | change-feed | B | session | mounted | supplier performance scorecard |

## po · :9314 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/po.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/po.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /po | GET | change-feed | B | session | mounted | purchase-order list (W11) |
| /po | POST | change-feed | B | session | mounted | create PO |
| /po/{id} | GET | change-feed | B | session | mounted | PO detail |
| /po/{id}/match | GET | change-feed | B | session | mounted | three-way match viewer |
| /po/{id}/status | POST | change-feed | B | session | mounted | advance PO status |

## order · :9315 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/order.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/orders.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /orders/suggested | GET | change-feed | B | session | mounted | replenishment suggestions queue |
| /orders/suggested/{id}/approve | POST | change-feed | B | session | mounted | approve suggested order |
| /orders/suggested/{id}/reject | POST | change-feed | B | session | mounted | reject suggested order |
| /orders/suggested/{id}/send | POST | change-feed | B | session | mounted | send approved order to supplier |

## onboarding · :9316 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/onboarding.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: none

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /onboarding | GET | reference | B | session | mounted | onboarding wizard index (W13) |
| /onboarding/connect | GET | reference | B | session | mounted | POS connection step |
| /onboarding/import | GET | reference | B | session | mounted | data import step |
| /onboarding/rules | GET | reference | B | session | mounted | rule selection step |
| /onboarding/rules/enable | POST | reference | B | session | mounted | enable selected rule pack |
| /onboarding/welcome | GET | reference | B | session | mounted | onboarding completion |

## ecom · :9317 · merchant-facing · P1

Owner: ALX  ·  Card: Brain/wiki/cards/ecom.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: none

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /ecom/orders | GET | reference | B | session | mounted | ecom channel order list (W15) |
| /ecom/sync | GET | reference | B | session | mounted | ecom sync status |

## audit · :9320 · tenant-scoped · P1

Owner: ALX  ·  Card: Brain/wiki/cards/audit.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/admin.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /admin/audit | GET | reference | B | session | mounted | append-only audit log viewer (W9) |

## compliance · :9091 · tenant-scoped · P1

Owner: ALX  ·  Card: Brain/wiki/cards/compliance.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/admin.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /admin/iso27001 | GET | reference | B | session | mounted | ISO 27001 control evidence dashboard (W9) |

## users · :9321 · tenant-scoped · P2

Owner: ALX  ·  Card: Brain/wiki/cards/users.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/admin.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /admin/users | GET | reference | B | session | mounted | tenant user roster (blocked on GRO-769 identity middleware + GRO-770 admin module) |

## config · :9322 · tenant-scoped · P1

Owner: ALX  ·  Card: Brain/wiki/cards/config.md  ·  Cells: [B × reference]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/admin.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /admin/config | GET | reference | B | session | mounted | tenant configuration viewer (W9) |

## hierarchy · :9323 · tenant-scoped · P1

Owner: ALX  ·  Card: Brain/wiki/cards/hierarchy.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/admin.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /admin/hierarchy | GET | change-feed | B | session | mounted | merchant org hierarchy editor (W10) |
| /admin/hierarchy | POST | change-feed | B | session | mounted | create hierarchy node |

## network-integrity · :9088 · tenant-scoped · P1

Owner: ALX  ·  Card: Brain/wiki/cards/network-integrity.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/admin.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /admin/network-integrity | GET | change-feed | B | session | mounted | cross-location anomaly detection (W10) |

## cross-store · :9324 · tenant-scoped · P1

Owner: ALX  ·  Card: Brain/wiki/cards/cross-store.md  ·  Cells: [B × change-feed]
tenant-scoped  ·  Python prior art: Canary/canary/blueprints/dashboards.py

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /dashboards/cross-store | GET | change-feed | B | session | mounted | multi-store intelligence dashboard (W10) |
