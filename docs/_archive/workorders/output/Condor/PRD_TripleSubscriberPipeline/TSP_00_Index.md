---
type: spec
domain: tsp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Triple Subscriber Pipeline — PRD Master Index
**Version:** 1.2
**Date:** February 26, 2026
**Author:** Condor (IP Sanitization Intern), supervised by PhD
**Classification:** CONFIDENTIAL — Internal Engineering
**Architecture source:** PhD Patent Visuals (FIG. 1–3 + Temporal Sequence)
**Supersedes:** Previous dual-subscriber PRD set

---

## Overview

Nine component PRDs defining the complete six-node Triple Subscriber Pipeline for universal webhook notarization. Each PRD is detailed enough for Jeremy + Qwen to code directly without clarifying questions.

The architecture processes any webhook-originated event through three decoupled subscribers — immutable evidence (Sub 1), structured queryable store (Sub 2), and Bitcoin inscription (Sub 3) — producing a dual-form permanent event record: application-ready and Bitcoin-anchored.

---

## PRD Registry

| PRD ID | Component | FIG. Reference | Owner | Sprint | Status |
|--------|-----------|---------------|-------|--------|--------|
| TSP-01 | Webhook Receipt & HMAC Validation | FIG. 1 Node 1+2 top, FIG. 2 T+0→T+5ms, FIG. 3 Ingestion | Jeremy | 6 | DRAFT |
| TSP-02 | Queue Publication & Fan-Out | FIG. 1 Node 2 fan-out, FIG. 2 T+5→T+15ms, FIG. 3 Queue | Jeremy | 6 | DRAFT |
| TSP-03 | Sub 1 — Hash & Seal Evidence Writer | FIG. 1 Sub 1, FIG. 2 T+15ms Sub 1, FIG. 3 Evidence Store | Tom + Jeremy | 6 | DRAFT |
| TSP-04 | Sub 2 — Parse & Route Structured Writer | FIG. 1 Sub 2, FIG. 2 T+15ms Sub 2, FIG. 3 Structured Store | Tom + Jeremy | 6 | DRAFT |
| TSP-05 | Sub 3 — Merkle Batcher & Ordinal Minter | FIG. 1 Sub 3, FIG. 2 T+~10min, FIG. 3 Ordinal Pool | Jeremy | 6 | DRAFT |
| TSP-06 | Detection Engine | FIG. 2 T+100ms, FIG. 3 Application Layer | Jeremy | 6 | DRAFT |
| TSP-07 | L402 Validation API | FIG. 2 T+∞, FIG. 3 Application Layer | Jeremy | 6 | DRAFT |
| TSP-08 | Bilateral Verification Procedure | FIG. 2 Bilateral bar, FIG. 3 External Verification | Jeremy | 6 | DRAFT |
| TSP-09 | Replay & Rebuild Procedure | Sub 2 "Replayable from Sub 1" property | Jeremy | 7 | DRAFT |

---

## Dependency Graph

```
TSP-01 (Webhook Receipt)
  │
  ▼
TSP-02 (Queue Fan-Out)
  │
  ├──────────────┬──────────────┐
  ▼              ▼              ▼
TSP-03         TSP-04         TSP-05
(Sub 1:        (Sub 2:        (Sub 3:
 Hash&Seal)     Parse&Route)   Merkle&Ordinal)
  │              │              │
  │              ▼              │
  │            TSP-06           │
  │            (Detection)      │
  │              │              │
  ├──────────────┼──────────────┤
  ▼              ▼              ▼
TSP-08         TSP-07         TSP-05 output
(Bilateral     (L402           │
 Verify)        Validation)    ▼
                             TSP-07 (validates
                              against inscription)

TSP-09 (Replay) ← reads TSP-03 output, rebuilds TSP-04 output
```

### Critical Path

```
TSP-01 → TSP-02 → TSP-03 (immutability anchor — everything depends on evidence sealed first)
                 → TSP-04 (merchant dashboard path — feeds detection)
                 → TSP-05 (Bitcoin inscription path — feeds validation revenue)
```

### Cross-PRD Dependencies

| PRD | Depends On | Gates |
|-----|-----------|-------|
| TSP-01 | None (entry point) | TSP-02 |
| TSP-02 | TSP-01 | TSP-03, TSP-04, TSP-05 |
| TSP-03 | TSP-02 | TSP-08 (verification), TSP-09 (replay source), TSP-05 (hash input) |
| TSP-04 | TSP-02 | TSP-06 (detection), TSP-09 (rebuild target) |
| TSP-05 | TSP-02, TSP-03 (event_hash) | TSP-07 (inscription for validation), TSP-08 (Merkle proof) |
| TSP-06 | TSP-04 | Merchant dashboard (Today's View) |
| TSP-07 | TSP-03 (evidence lookup), TSP-05 (inscription proof) | Revenue layer |
| TSP-08 | TSP-03 (evidence), TSP-05 (inscription) | Forensic procedure |
| TSP-09 | TSP-03 (read source), TSP-04 (rebuild target) | Upgrade safety |

---

## External References

| Document | Path | Used By |
|----------|------|---------|
| PRD E1-F14 (Chirp Config + API Gateway) | `_ALX/WorkOrders/PRD_ChirpConfig_APIGateway_v1.0.md` | TSP-06 |
| CRDM v1.0 | `Canary_IP/Markdown/Specs/Canary_CRDM_v1.0.md` | TSP-04 |
| B-035 Addendum (Temporal Partition) | `_ALX/WorkOrders/B035_Addendum_TemporalPartition_QueryGovernor.md` | TSP-04 |
| Jeremy SDK Audit | `_ALX/WorkOrders/output/Jeremy/Jeremy_SquareSDK_CRDMAlignment.md` | TSP-04, TSP-01 |
| El Jeffe Business Model Addendum | `_ALX/ElJeffe_BusinessModel_Addendum.md` | TSP-05, TSP-07 |
| FIG. 1 Six-Node Architecture | `_ALX/WorkOrders/output/PhD/Patent_SixNode_Architecture_v1.0.html` | All |
| FIG. 2 Data Flow Visual | `_ALX/WorkOrders/output/PhD/Patent_DataFlow_Visual_v2.0.html` | All |
| FIG. 3 Component Interaction | `_ALX/WorkOrders/output/PhD/Patent_TripleSubscriber_Component_v1.0.html` | All |
| FIG. 2 Temporal Sequence | `_ALX/WorkOrders/output/PhD/Patent_DataFlow_Sequence_v1.0.html` | All |

---

## IP Protection Summary

Each PRD contains an IP Protection Notes section. Crown Jewels flagged across the set:

| Crown Jewel | PRD | Protection |
|------------|-----|------------|
| Hash-before-parse ordering | TSP-01 | Describe requirement, not implementation trick |
| Chain hash computation mechanism | TSP-03 | Describe behavior, not trigger SQL |
| Merkle batching strategy | TSP-05 | Describe contract, not tree construction algorithm |
| L402 pricing model | TSP-07 | Describe flow, not economics |
| Triple subscriber decoupling pattern | All | Describe independence, not coupling mechanism |

No internal schema names in external-facing language. No threshold values or rule logic details. No agent names in any PRD.

---

## Monitoring & Alerting

**Monitoring & Alerting:** Prometheus metrics + Grafana dashboards for consumer lag, stream
memory usage, hash chain gap detection. Specification deferred — Jeremy defines during
implementation. Ops appendix to follow.

---

## Integration Test Strategy

**Integration Test Strategy:** End-to-end test covering webhook receipt → stream → 3 consumers
→ detection → alert. Specification deferred to Jim (QA). Test plan required before Sprint 6
QA gate.

---

## Pre-Build Consolidated Review Document

Before Sprint 6 coding begins, Condor produces a single consolidated review document
structured as follows:

1. **Executive Summary** (1 page) — What TSP is, business value, key deferrals, biggest
   risks, desired outcome of review
2. **Architecture Flow Diagram** — Mermaid diagram showing webhook → HMAC → XADD → fan-out
   → 3 subscribers → detection → future Bitcoin/L402. Color-coded: green (existing reuse),
   blue (new Sprint 6), yellow (deferred Sprint 7+), red (persistent storage)
3. **PRD Inventory Table** — All 10 PRDs: title, status, dependencies, sprint target, notes
4. **Execution Plan** — Dependency graph, Week 0 prerequisites, 4 parallel tracks, reuse matrix
5. **Consolidated Design Feedback** — All issues by priority tier + cross-PRD sync gaps
6. **Riskiest Seams** — Deep-dive on: replay + advisory locks + triggers, Sub 3 90-min claim,
   detection trigger mechanism, Valkey sizing under load, future L402/Bitcoin seams
7. **Week 1 Smoke Tests** — Per-track validation criteria
8. **Decisions Needed** — Explicit yes/no list for Sprint 6 kickoff meeting

**Output file:** `_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md`
**Timing:** Delivered AFTER Pass 6 of this work order (revised PRDs must be final first)
**Feeds:** Sprint 6 kickoff meeting. Jeremy reads this before writing any code.

---

## Review Gates

| Gate | Owner | Scope |
|------|-------|-------|
| Architecture validation | PhD | All nine PRDs trace to FIG. references |
| IP safety | Condor + PhD | Crown Jewels flagged, no leakage |
| Legal alignment | Syd | Patent claim coverage, ToS compliance |
| Readability | Jess | Jeremy + Qwen can execute without questions |
| Schema correctness | Tom | DDL in TSP-03, TSP-04, TSP-05 aligned with CRDM |

---

## Revision Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-26 | Condor | Initial index |
| 1.2 | 2026-02-27 | ALX (B-059) | Added Monitoring & Alerting placeholder (Prometheus + Grafana, spec deferred). Added Integration Test Strategy placeholder (end-to-end test, deferred to Jim). Added Pre-Build Consolidated Review Document section. Standardized formatting. |

---

*Condor | IP Sanitization | February 27, 2026*
*Supervised by PhD | Legal gate: Syd | Quality gate: Jess*
