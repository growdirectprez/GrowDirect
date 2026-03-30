---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD Index: Staged Immutability Pipeline
**Last Updated:** 2026-02-26
**System Owner:** Jeremy (Development), Tom (Architecture)
**Product North Star:** "We don't want to add to the stress. We want to ease it."

---

## Overview

The Staged Immutability Pipeline is a six-node universal webhook notarization system. Any webhook from any network arrives, gets sealed into an immutable evidence store, parsed into a structured application store, batched into a Merkle tree, and inscribed on Bitcoin as an Ordinal. Every event is permanently retrievable in two forms: application-queryable (fast, indexed) and Bitcoin-permanent (immutable, global).

**Throughput Target:** 100 events/day baseline. 5,000 events/6 hours = 50x spike. All events notarized with zero drops.
**Revenue Model:** Sat-gated validation API. Perpetual micropayment revenue per verification call.

---

## PRD Summary Table

| # | Component | Owner | Sprint | Status | Dependencies | Gates |
|---|-----------|-------|--------|--------|--------------|-------|
| 01 | Webhook Receipt + Queue Ingestion | Jeremy | S6 | Design | HMAC library, Message Queue | All downstream |
| 02 | Sub 1 — Raw Evidence Store Writer | Jeremy | S6 | Design | Queue, Evidence DB (PostgreSQL + triggers), Hash library | Sub 2, Sub 3, Replay, Bilateral Verification |
| 03 | Sub 2 — Structured Store Writer | Jeremy | S6 | Design | Queue, Sub 1 output, Application DB, Detection Engine | Live detection, Replay Procedure |
| 04 | Bilateral Verification Procedure | Jeremy | S6 | Design | Sub 1 output, Hash recomputation, Audit logging | User-facing forensics, Legal discovery |
| 05 | Replay Procedure | Jeremy | S7 | Backlog | Sub 1 output, Sub 2 parser (current version), Progress tracking | Disaster recovery, Schema migration |
| 06 | Volume Spike Handling — Queue Backpressure | Jeremy + Tom | S6 | Design | All Subs, Queue, Load profile, Graceful degradation | Production readiness, SLA compliance |
| 07 | Sub 3 — Ordinal Minter | Jeremy | S6 | Design | Queue, Bitcoin RPC, Ordinals API, Key management, Merkle tree library | Permanent notarization, Validation API revenue |
| 08 | Validation API + L402 Gate | Jeremy | S7 | Design | Sub 3 output, Lightning invoice generation, Rate limiting, Audit logging | Revenue operationalization, User-facing SaaS |

---

## Dependency Graph

```
Webhook Arrival
       ↓
PRD_01: Webhook Receipt + Queue Ingestion
       ↓
    [Message Queue]
       ├─→ PRD_02: Sub 1 — Evidence Store
       │        ├─→ PRD_04: Bilateral Verification
       │        └─→ PRD_05: Replay Procedure
       │
       ├─→ PRD_03: Sub 2 — Structured Store
       │        └─→ Live Detection Engine
       │
       └─→ PRD_07: Sub 3 — Ordinal Minter
                ├─→ Bitcoin Ordinals
                └─→ PRD_08: Validation API (L402)
                        └─→ Revenue Stream

PRD_06: Volume Spike Handling — Cross-cutting
         (applies to all queue consumers)
```

---

## Critical Path to Revenue

1. **S6 Gate:** PRD_01, PRD_02, PRD_03 complete and integrated. Evidence store and structured store running live on production webhook volume.
2. **S6 Gate:** PRD_07 complete. First Ordinals inscriptions successful. Treasury controls all keys.
3. **S7 Gate:** PRD_08 complete and deployed. Validation API accepting Lightning payments. Revenue flowing.

---

## IP Protection Zones

**Crown Jewels (do not document externally):**
- Merkle batching strategy and tree structure
- Two-response API design (sealed hash vs. Bitcoin confirmation)
- Universal webhook source-agnostic claim
- Key custody and management implementation
- Pool scaling automation thresholds

**Safe to Document:**
- Triple subscriber pattern (architectural design, not implementation)
- Evidence-structured dual storage
- Blockchain immutability narrative (public Bitcoin properties)
- Sat-gated micropayment model (public Lightning protocol)

---

## Test Coverage Summary

All PRDs include:
- Happy path (nominal 100 events/day)
- Edge cases (schema variations, partial failures)
- **Toy Store Spike (REQUIRED):** 5,000 events in 6 hours (50x), all notarized, zero data loss
- Failure modes (network, database, Bitcoin downtime, queue saturation)

---

## Glossary

| Term | Definition |
|------|-----------|
| **Evidence Store** | Raw, immutable payload archive with SHA-256 hash chain |
| **Structured Store** | Parsed, indexed, queryable application database |
| **Sub 1, Sub 2, Sub 3** | Three independent queue subscribers with decoupled responsibilities |
| **Bilateral Verification** | Independent recomputation of hash to prove authenticity |
| **Ordinal** | Bitcoin satoshi inscribed with data (permanent, immutable, global) |
| **Merkle Root** | Cryptographic commitment of batch hash tree to Bitcoin |
| **L402** | Lightning + HTTP 402 micropayment gate (proof of payment) |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Event capture rate | 100% | Zero webhook drops under 50x spike |
| Evidence integrity | 100% | Hash chain unbroken, bilateral verification matches |
| Detection SLA | 15 min | Sub 2 detection output available within 15 min of receipt |
| Bitcoin finality | ~10 min | Ordinal inscribed and block-confirmed within 10 minutes |
| API availability | 99.9% | Validation API uptime, excluding scheduled maintenance |
| Revenue per event | TBD | Sat micropayment rate (set by policy, not code) |

---

## Next Steps

1. Read PRD_01 through PRD_08 in order
2. Schedule architecture review with Jeremy + Tom
3. Identify any missing dependencies (external APIs, hardware, credentials)
4. Confirm sprint 6 capacity and spike-test dates
5. Prepare test harness for toy store 50x scenario
