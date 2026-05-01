---
tags: [canary, go, architecture, endpoint-library, api-contracts, crb-source]
last-compiled: 2026-04-30
needs-review: 2026-06-01
related: [canary-go-portal, canary-go-vs-gk-pos-gap-analysis, canary-architecture, microservice-architecture]
---

# Canary Go Endpoint Library

> **Governing thesis.** Canary Go's API surface organizes along **three axes** — Adapter Substrate (POS → Canary), Resource APIs (Canary → external systems), and Agent Surface (Canary → AI agents). Each axis answers a different integration question and has a different audience. The endpoint library is the partner-facing canonical reference for all three. It lives here in Brain as the source of truth and is curated to [crb.growdirect.io](https://crb.growdirect.io) as the public partner surface. Every endpoint Canary exposes belongs to exactly one axis. Every service in the [[canary-go-portal#13-Module-Spine|13-module spine]] and the extended block contributes endpoints to one or more axes.

The reframe and benchmark behind this structure is in [[canary-go-vs-gk-pos-gap-analysis|Canary Go vs GK-POS — Gap Analysis]].

## The three axes

| Axis | Surface | Direction | Consumers |
|---|---|---|---|
| **A — Adapter Substrate** | Webhook receivers, polling clients, edge agents | POS → Canary | POS vendors, integration partners, merchant IT |
| **B — Resource APIs** | 32-service REST surface | Canary → external | Merchant tools, BI/dashboards, partner platforms, ops engineers |
| **C — Agent Surface** | MCP tools, SSE streams, webhook publishers | Canary → AI agents | Claude Code / Cowork / agent platforms, in-store AI assistants, third-party AI tooling |

Every endpoint in this library is tagged with its axis. Endpoints can serve more than one axis only when the underlying capability is genuinely the same (e.g., a `/search` resource that is reachable as REST and as an MCP tool — same code, two consumers).

---

## Axis A — Adapter Substrate (POS → Canary)

How Canary acquires data from external POSes. The contract every POS adapter must implement is the [[pos-adapter-substrate|POS Adapter Substrate]]. Each adapter is one Go binary in `cmd/`.

### Webhook receivers

| Endpoint | Purpose | Implemented by |
|---|---|---|
| `POST /webhooks/square` | Square webhook receiver | `tsp` (:8080) |
| `POST /webhooks/counterpoint` | Counterpoint event receiver (polling adapter pushes here) | `tsp` (:8080) |
| `POST /webhooks/inbound` | Square OAuth webhook | `hawk` (:8082) |
| `POST /webhooks/{source}` | **Generic pattern for future POS adapters** | TBD per source |

### Polling adapter contracts

| Endpoint | Purpose | Implemented by |
|---|---|---|
| `POST /sync/pull` | Trigger manual pull sync (ops use) | `hawk` (Square), `bull` (Counterpoint) |
| `GET /sync/status` | Last sync watermarks | per-adapter |
| `POST /merchants/:id/sync/pull` | Force immediate poll | per-adapter |
| `GET /merchants/:id/sync/status` | Per-merchant poll watermarks and lag | per-adapter |
| `POST /merchants/:id/connect` | Register API credentials for a merchant | per-adapter |
| `DELETE /merchants/:id/connect` | Remove credentials | per-adapter |

### Edge agent protocol

The edge agent (`cmd/edge`) runs on-prem (Windows Service) at the merchant's back-office server. **Outbound only** — no inbound endpoints. It pushes derived intelligence packets to the cloud `tsp` webhook receiver. See [[bull|Bull SDD]] for the protocol.

### POS Adapter Substrate Interface

The Go interface every adapter implements lives in `internal/pos-adapter/`. It defines:

- `Connect(merchantID, credentials) (Session, error)`
- `Pull(session, since time.Time) ([]ARTSEvent, watermark, error)`
- `Subscribe(session, eventTypes) (<-chan ARTSEvent, error)` (for webhook-capable POSes)
- `Disconnect(session) error`

All output normalizes to **ARTS POSLog** before entering Canary's pipeline. See [[pos-adapter-substrate]].

---

## Axis B — Resource APIs (Canary → external)

The 32-service REST surface, organized by domain. Each service owns its endpoint namespace. URLs below are the canonical patterns; full request/response contracts live in each service's SDD.

### Sales & Transactions

| Pattern | Service | Status |
|---|---|---|
| `/transactions/...` | `tsp` (:8080), `analytics` (:8088) | ✅ partial |
| `/returns/...` | `returns` (:8097) | ⚪ undocumented |

### Detection & Cases

| Pattern | Service | Status |
|---|---|---|
| `/alerts/...` (acknowledge, investigate, dismiss, escalate, history) | `alert` (:8087) | ✅ documented |
| `/cases/...` (create, evidence, timeline, chain verify) | `fox` (:8083) | ✅ documented |
| `/rules/...` (Chirp introspection, force-evaluate) | `chirp` (:8081) | ✅ documented |
| `/rollup/...`, `/score/...` | `analytics` (:8088) | ✅ documented |

### Master Data

| Pattern | Service | Status |
|---|---|---|
| `/items/...` | `item` (:8090) | ⚪ undocumented |
| `/customers/...` | `customer` (:8096) | ⚪ undocumented |
| `/employees/...` | `employee` (:8095) | ⚪ undocumented |
| `/vendors/...` | `receiving` (:8092) | ⚪ undocumented |

### Operations

| Pattern | Service | Status |
|---|---|---|
| `/inventory/...` | `inventory` (:8091), `inventory-as-a-service` (:9081) | ⚪ undocumented |
| `/receiving/...` (POs) | `receiving` (:8092) | ⚪ undocumented |
| `/transfers/...` | `transfer` (:8093) | ⚪ undocumented |
| `/pricing/...` | `pricing` (:8094) | ⚪ undocumented |
| `/assets/...` | `asset` (:8089) | ⚪ undocumented |

### Intelligence

| Pattern | Service | Status |
|---|---|---|
| `POST /search` (semantic) | `owl` (:8084) | ✅ documented |
| `/risk-dictionary/...` | `owl` (:8084) | ✅ documented |
| `/ej-spine/...` | `owl` (:8084) | ✅ documented |
| `/embed` | `owl` (:8084) | ✅ documented |
| `/analytics/...` | `analytics` (:8088) | ✅ partial |

### Identity & Tenancy

| Pattern | Service | Status |
|---|---|---|
| `/merchants/...` | `identity` (:8086) | ✅ documented |
| `/users/...` | `identity` (:8086) | ✅ partial |
| `/sessions/...` | `identity` (:8086) | ✅ documented |
| `/oauth/...` | `identity` (:8086) | ✅ documented |

### Reports

| Pattern | Service | Status |
|---|---|---|
| `/reports/...` | `report` (:8098) | ⚪ undocumented |

### Accountability Rails (Canary-unique)

These are the moats. They have **no GK equivalent** — they are the structural differentiation.

| Pattern | Service | Status |
|---|---|---|
| `/ildwac/...` | `ildwac` (:9082) | ⚪ undocumented |
| `/l402-otb/...` | `l402-otb` (:9090) | ⚪ undocumented |
| `/blockchain-anchor/...` | `blockchain-anchor` (:9086) | ⚪ undocumented |
| `/compliance/...` | `compliance` (:9091) | ⚪ undocumented |
| `/device-contracts/...` | `device-contracts` (:9083) | ⚪ undocumented |
| `/store-network-integrity/...` | `store-network-integrity` (:9088) | ⚪ undocumented |
| `/field-capture/...` | `field-capture` (:9087) | ⚪ undocumented |
| `/commercial/...` | `commercial` (:9089) | ⚪ undocumented |
| `/raas/...` | `raas` (:8099) | ⚪ undocumented |
| `/ecom-channel/...` | `ecom-channel` (:9080) | ⚪ undocumented |

### Ops & Health

| Pattern | Service | Status |
|---|---|---|
| `GET /health` | every service | ✅ standard |
| `GET /status` | most services | ✅ partial |
| `/ops-dashboard/...` | `ops-dashboard` (:9084) | ⚪ undocumented |
| `/store-brain/...` | `store-brain` (:9085) | ⚪ undocumented |

---

## Axis C — Agent Surface (Canary → AI agents)

The MCP tool registry, SSE streams, and webhook publishers that make Canary AI-native.

### MCP tool registry

Each agent-facing service exposes an MCP server with named tools. JWT-gated. REST internally; MCP at the edge.

| MCP Server | Service | Tools | Status |
|---|---|---|---|
| `canary-compliance` | `compliance` (:9091) | 7 tools (item authorization × regulatory zone × ops blocks) | ✅ documented |
| `canary-raas` | `raas` (:8099) | 7 tools (namespace resolution, key construction) | ✅ documented |
| `canary-fox` | `fox` (:8083) | TBD (case management for AI agents) | ⚪ undocumented |
| `canary-chirp` | `chirp` (:8081) | TBD (rule introspection, force-evaluate) | ⚪ undocumented |
| `canary-owl` | `owl` (:8084) | TBD (search, risk lookup, EJ spine query) | ⚪ undocumented |
| `canary-store-brain` | `store-brain` (:9085) | TBD (presence resolution, session governance) | ⚪ undocumented |
| `canary-ops` | `ops-dashboard` (:9084) | TBD (device health queries) | ⚪ undocumented |

### SSE streams

| Stream | Service | Purpose |
|---|---|---|
| `GET /ops-dashboard/sse` | `ops-dashboard` (:9084) | Real-time device health, MCP observability |
| `GET /store-brain/sse` | `store-brain` (:9085) | Presence events, session state changes |

### Webhook publishers

| Pattern | Trigger |
|---|---|
| `POST {merchant-configured-url}` | Alert created · Case escalated · Detection rule fired |

Each merchant configures outbound webhook destinations through `/merchants/:id/webhooks` (TBD).

---

## Coverage status

Counts as of 2026-04-30:

| Status | Services | Endpoints |
|---|---|---|
| ✅ Documented | 11 | ~61 |
| ⚪ Undocumented | 21 | TBD |

The 21 undocumented services are the build-out target. Each becomes a Linear dispatch — see the dispatch list in the Dispatch project under `Target/laptop` + `Agent/Architect`.

## Conventions

- **URL shape:** `/{resource}` for collections, `/{resource}/{id}` for single items, `/{resource}/{id}/{subresource}` for related records. Verbs on the action: `/alerts/:id/acknowledge`, not `/alerts/:id/status`.
- **Tenant isolation:** Every endpoint scopes by `merchant_id` — either as a path parameter, a query parameter, or implicit via the JWT claim.
- **Response shape:** JSON. Errors as `{"error": {"code": "...", "message": "..."}}`. Pagination cursor-based via `?cursor=...&limit=...`.
- **Auth:** JWT Bearer for all non-`/health` endpoints. MCP tools authenticated via the MCP protocol's session header plus tenant-scoped JWT.
- **Versioning:** No URL versioning. Breaking changes go through the Hardening phase per the [[canary-go-portal#agent-lifecycle|agent PMO lifecycle]].
- **Schema-qualified DB writes:** `app.`, `sales.`, `metrics.` always; never unqualified.

## Where this lives

- **Source of truth:** this article + per-service SDDs in `docs/sdds/go-handoff/`
- **Partner-facing publication:** [crb.growdirect.io](https://crb.growdirect.io) — curated subset, no internal-only details
- **Internal cross-references:** [[canary-go-portal]], [[microservice-architecture]], [[canary-go-vs-gk-pos-gap-analysis]]
- **Curation flow:** Brain wiki → Brain/dispatches → CRB push (per [[canary-go-portal|three-vault architecture]])

## Sources

- [[canary-go-vs-gk-pos-gap-analysis]] — the analysis behind this structure
- [[microservice-architecture]] — current per-service endpoint detail
- [[canary-go-portal]] — project portal and SDD index
