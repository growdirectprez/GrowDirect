---
type: pitch
domain: business
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# The Architecture

> *"Enterprise bones. SMB skin. Bitcoin spine."*

---

## Platform Overview

Canary LP is built on a three-database architecture descended from enterprise systems that processed hundreds of billions of rows across the world's largest retailers. The platform captures every POS event, seals it instantly, analyzes it for loss patterns, and inscribes the proof permanently on Bitcoin.

The architecture has three layers:

1. **Canary Core** — Webhook capture, event sealing, chirp detection, merchant dashboard
2. **The Flock** — Fox (case management), Goose (Bitcoin payments), Owl (analytics oracle)
3. **elJeffe** — Universal event notarization on Bitcoin via gLog inscription

---

## The Three-Database Model

```
┌─────────────────────────────────────────────────────────────┐
│                    CANARY PLATFORM                           │
├──────────────────┬──────────────────┬──────────────────────┤
│   Operational    │   Transaction    │   Analytics & ML     │
│                  │   Log            │                      │
├──────────────────┼──────────────────┼──────────────────────┤
│ ACID, RLS        │ Append-only      │ Star schema          │
│ Normalized       │ JSONB payloads   │ Pre-aggregated       │
│ Soft deletes     │ Monthly partn.   │ Monthly partn.       │
├──────────────────┼──────────────────┼──────────────────────┤
│ Users, Merchants │ Transactions     │ Daily/Hourly metrics │
│ Locations, Prods │ Line Items       │ Employee metrics     │
│ Employees, Custs │ Tenders          │ Product metrics      │
│ Alerts, Cases    │ Cash Drawer      │ ML features/scores   │
│ Evidence, Audit  │ Inventory        │ Operator actions     │
│ Timecards        │ Gift Cards       │ Scorecards           │
│ Disputes         │ Ingestion log    │ Risk score history   │
│                  │ ETL batches      │ Baselines            │
└──────────────────┴──────────────────┴──────────────────────┘
```

**Operational** handles users, merchants, locations, products, and the application layer. **Transaction Log** is append-only — financial data is a ledger, never updated or deleted. **Analytics** runs the ML models, metrics aggregation, and detection scoring.

---

## The Capture Pipeline

```
Square Webhook → elJeffe API (jeffe.io)
    │
    ├─► SHA-256 hash on receipt (T+0ms)
    ├─► PostgreSQL INSERT-only evidence store (T+15ms)
    ├─► Queryable application store (replicated)
    └─► Merkle batch → Bitcoin Ordinal inscription (~T+10min)
```

Every POS event follows the same path: capture at the API gateway, hash immediately, seal in the evidence store, replicate to the application database for queries, and batch into a Merkle tree for Bitcoin inscription. The evidence store is write-once — no UPDATE, no DELETE. The hash chain links each entry to its predecessor. Break one, the chain breaks downstream.

---

## The gLog Inscription Flow

The gLog is the permanent successor to the IBM 4690 tLog. Where the tLog lived on institutional servers — mutable, deletable, and controlled by whoever owned the hardware — the gLog lives on Bitcoin.

```
POS Event
  │
  ▼
elJeffe API (jeffe.io/glog)
  │
  ├─► Hash PII (cryptographic stripping — personal data never reaches the chain)
  ├─► Seal event (SHA-256, chain-linked, INSERT-only)
  ├─► Batch into Merkle tree
  └─► Inscribe Merkle root as Bitcoin Ordinal
        │
        ├─► Block height = global timestamp (no one controls it)
        ├─► Each inscription references the prior entry
        └─► Result: complete, replayable merchant history on Bitcoin
```

**Two artifacts per event:**
1. A queryable database record (instant — milliseconds)
2. A Bitcoin inscription proving the event occurred at a specific time (~10 minutes)

---

## Immutability Model

Three categories of data integrity, non-negotiable:

| Category | Pattern | Why |
|---|---|---|
| **Financial ledger** | APPEND-ONLY (no UPDATE, no DELETE) | Financial data is a ledger. You don't erase entries. |
| **Evidentiary** | INSERT-ONLY (enforced by DB trigger) | Law enforcement chain of custody. |
| **Audit trail** | APPEND-ONLY + SHA-256 hash chain | Tamper detection. Each entry's hash includes the previous entry's hash. |
| **Operational** | Soft delete with history preservation | Normal application CRUD. |

---

## POS-Agnostic Design

The architecture is built to be POS-agnostic from day one:

```
Square Webhook  ──► Square Parser  ──► Canonical Tables ──► Chirp Detection
Clover Webhook  ──► Clover Parser  ──► Canonical Tables ──► Chirp Detection
Toast  Webhook  ──► Toast  Parser  ──► Canonical Tables ──► Chirp Detection
```

Every POS integration maps to the same canonical schema through a vendor-specific parser. The detection engine, analytics, and inscription pipeline work identically regardless of source POS. Add a new POS by writing a parser — everything downstream is universal.

---

## Security Architecture

| Layer | Mechanism |
|---|---|
| **Multi-tenant isolation** | Row-Level Security (RLS) — tenants cannot see each other's data |
| **Authentication** | OAuth 2.0 + session tokens |
| **Authorization** | Role-Based Access Control (RBAC) — Viewer, Analyst, Manager, Admin |
| **Evidence integrity** | SHA-256 hash chain + database triggers preventing UPDATE/DELETE |
| **PII protection** | Cryptographic hashing before inscription — personal data never reaches Bitcoin |
| **API security** | Rate limiting, webhook signature verification, TLS 1.3 |
| **Validation gate** | Lightning L402 micropayment for external proof verification |

---

## Deployment

| Environment | Purpose |
|---|---|
| **Local** | Developer machines, SQLite single-DB |
| **Dev** | Shared testing, PostgreSQL three-database |
| **Staging** | Pre-production, mirrors production config |
| **Production** | Live merchant data, full security stack |

Current MVP runs SQLite for rapid iteration. PostgreSQL three-database deployment is the target after Square Marketplace certification. Schema design is Postgres-ready — table structures, constraints, and patterns are identical. Only the deployment topology changes.

---

*GrowDirect Confidential*
*Patent Pending — Provisional 63/991,596*
