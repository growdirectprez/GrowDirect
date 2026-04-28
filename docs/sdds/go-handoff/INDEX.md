---
spec-version: 1.0
target-implementation: Go
stack: PostgreSQL 17 + pgx + sqlc | Chi HTTP | REST | go-redis | pgvector-go
source: Curated from Canary Python prototype SDDs (GRO-617)
status: active-build-spec
updated: 2026-04-28
---

# Canary — Go Build Specification

This corpus is the complete functional specification for the Canary production build. It was derived from a working Python prototype (GRO-617), scrubbed of all implementation-language specifics, and extended with spec additions the prototype left implicit. Every SDD here describes **what the system does** — not how any particular language does it.

**Commercial context:** Canary is being built as an agent-driven retail operations platform targeting SMB merchants on NCR Counterpoint via VAR co-sell (Rapid POS and other Counterpoint VARs). The Python prototype proved the detection model and evidence chain. The Go build is the production product — clean from design, built to run with minimal human-in-the-loop intervention. Square remains a supported connector (Marketplace-certified prototype exists); NCR Counterpoint is the primary engagement path for the Go build.

The implementation is Go. Stack decisions are final:

| Layer | Choice |
|---|---|
| Database | PostgreSQL 17 |
| Driver | pgx (native Go) |
| Query layer | sqlc (type-safe Go from SQL) |
| HTTP router | Chi |
| Internal comms | REST |
| Vector store | pgvector (in-database, via pgvector-go) |
| Cache / queue | go-redis (Valkey-compatible) |
| Migrations | golang-migrate or goose |

---

## Read in this order

### 1. Product definition
- **[platform-overview.md](platform-overview.md)** — What Canary is, who it serves, what it does. Read this first. Everything else is the implementation of this document.
- **[multi-pos-architecture-proof.md](multi-pos-architecture-proof.md)** — Why the design is POS-agnostic. Read before touching any adapter code.

### 2. System architecture
- **[microservice-architecture.md](microservice-architecture.md)** — 10 Go microservices: ports, REST APIs, table ownership, inter-service communication, deployment topology. Read this before any other architecture doc.
- **[architecture.md](architecture.md)** — Logical service design, runtime topology, communication patterns.

### 3. Data model
- **[data-model.md](data-model.md)** — All 82 tables across app / sales / metrics schemas. Schema contracts (column names, types, constraints, indexes). This is the source of truth for sqlc queries.
- **[external-identities.md](external-identities.md)** — How POS-native IDs map to Canary canonical IDs. Critical for multi-POS correctness.
- **[identity.md](identity.md)** — Merchant, user, and tenant model. Auth contract. Session contract.

### 4. Ingestion pipeline
- **[webhook-pipeline.md](webhook-pipeline.md)** — Full pipeline: webhook receipt → HMAC verify → stream → seal → parse → merkle → detect. Read this before tsp.md.
- **[tsp.md](tsp.md)** — TSP orchestration detail. 4 pipeline stages with message envelope schema, idempotency contract, consumer group semantics, and backpressure contract.

### 5. Detection and cases
- **[chirp.md](chirp.md)** — 37 detection rules across 10 categories. Every rule has: detection logic, SQL contract, threshold table, alert fields produced.
- **[alert.md](alert.md)** — Alert lifecycle state machine. REST endpoints for each transition.
- **[fox.md](fox.md)** — Case management. Evidence hash chain. Append-only invariant enforced by DB trigger (trigger DDL is included — deploy it).

### 6. Intelligence layer
- **[owl.md](owl.md)** — pgvector search, Risk Dictionary, EJ Spine entity resolution.
- **[analytics.md](analytics.md)** — Metric rollups, risk scoring, baseline computation. Scheduled job contracts.

### 7. POS adapters
- **[pos-adapter-substrate.md](pos-adapter-substrate.md)** — The adapter interface every POS integration must implement. Read this before hawk.md or bull.md.
- **[hawk.md](hawk.md)** — Square adapter. Reference implementation of the substrate. 8 tables.
- **[bull.md](bull.md)** — NCR Counterpoint adapter. Reference implementation. REST API key auth, polling model (no native webhooks).

---

## Key invariants — never violate these

1. **UUID primary keys everywhere.** `gen_random_uuid()` default. Never use POS-native IDs as Canary row identifiers.
2. **Schema-qualified writes.** Every INSERT is `app.table`, `sales.table`, or `metrics.table`. Never unqualified.
3. **Tenant isolation.** Every query that touches merchant data has `WHERE merchant_id = $1`. Row-level security is a backstop, not a substitute.
4. **Append-only evidence.** `fox.evidence_records` has a DB trigger that blocks UPDATE and DELETE. Do not remove it.
5. **Idempotent pipeline.** Every TSP stage is idempotent. Duplicate events produce the same result, not duplicate rows.
6. **pgvector in-database.** Vectors live in PostgreSQL via pgvector. No external vector database.
7. **REST throughout.** No gRPC. Internal service calls are REST, same pattern as external POS API calls.
8. **Agent-driven by default.** No workflow should require a human operator in the loop unless legally mandated. Alerts surface to humans; investigations are driven by agents. HIL is an escalation path, not the default path.

---

## Spec additions

Sections marked `[SPEC ADDITION — not in prototype]` were added during curation to fill gaps the prototype left implicit. These are authoritative — implement them.

Key additions:
- `tsp.md` / `webhook-pipeline.md` — message envelope schema, idempotency key strategy, backpressure contract, consumer group semantics
- `pos-adapter-substrate.md` — rate limit/retry contract, dead-letter contract, poll watermark table
- `chirp.md` — SQL contracts for all 37 rules (derived from prototype code, not just the SDD)

---

## What is NOT in this corpus

These are intentionally excluded — internal tooling, not part of the Go rebuild:

- Agent memory system (ALX) — rebuild separately
- Namespace resolution (RaaS) — rebuild separately
- Ops console — rebuild separately
- Payment middleware (Goose) — rebuild separately
- MCP server layer — rebuild separately
- Python prototype-specific infra (Docker Compose, Gunicorn config, Alembic scripts)
