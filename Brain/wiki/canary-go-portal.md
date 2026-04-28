---
tags: [canary, go, portal, moc]
last-compiled: 2026-04-28
needs-review: 2026-05-12
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

### Module Layout
- [[docs/sdds/go-handoff/go-module-layout|Go Module Layout]] — 19-service monorepo, port map, CRDM package, sqlc conventions

---

## 13-Module Spine

All manifests in `GrowDirect-CRB/modules/`. Each has a `.manifest.yaml` (design spec) and a `.md` (narrative).

| Module | Manifest | Narrative |
|--------|----------|-----------|
| T — Transaction Pipeline | [[GrowDirect-CRB/modules/T-transaction-pipeline.manifest]] | [[GrowDirect-CRB/modules/T-transaction-pipeline]] |
| R — Customer | [[GrowDirect-CRB/modules/R-customer.manifest]] | [[GrowDirect-CRB/modules/R-customer]] |
| N — Device | [[GrowDirect-CRB/modules/N-device.manifest]] | [[GrowDirect-CRB/modules/N-device]] |
| A — Asset Management | [[GrowDirect-CRB/modules/A-asset-management.manifest]] | [[GrowDirect-CRB/modules/A-asset-management]] |
| Q — Loss Prevention | [[GrowDirect-CRB/modules/Q-loss-prevention.manifest]] | [[GrowDirect-CRB/modules/Q-loss-prevention]] |
| C — Commercial | [[GrowDirect-CRB/modules/C-commercial.manifest]] | [[GrowDirect-CRB/modules/C-commercial]] |
| D — Distribution | [[GrowDirect-CRB/modules/D-distribution.manifest]] | [[GrowDirect-CRB/modules/D-distribution]] |
| F — Finance | [[GrowDirect-CRB/modules/F-finance.manifest]] | [[GrowDirect-CRB/modules/F-finance]] |
| J — Forecast & Order | [[GrowDirect-CRB/modules/J-forecast-order.manifest]] | [[GrowDirect-CRB/modules/J-forecast-order]] |
| S — Space, Range & Display | [[GrowDirect-CRB/modules/S-space-range-display.manifest]] | [[GrowDirect-CRB/modules/S-space-range-display]] |
| P — Pricing & Promotion | [[GrowDirect-CRB/modules/P-pricing-promotion.manifest]] | [[GrowDirect-CRB/modules/P-pricing-promotion]] |
| L — Labor & Workforce | [[GrowDirect-CRB/modules/L-labor-workforce.manifest]] | [[GrowDirect-CRB/modules/L-labor-workforce]] |
| W — Work Execution | [[GrowDirect-CRB/modules/W-work-execution.manifest]] | [[GrowDirect-CRB/modules/W-work-execution]] |

---

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
