---
card-type: architecture
card-id: gap-backbone-architecture
card-version: 1
domain: canary
layer: infrastructure
status: approved
agent: ALX
tags: [gap-backbone, bigquery, alloydb, tsp, eljeffe, vertex-ai, ingestion, counterpoint, gcp, multi-tenant, architecture]
last-compiled: 2026-05-01
needs-review: false
---

## What this is

The Gap Backbone is the AI-native analytics and operations layer that sits on top of the legacy Counterpoint SQL Server estate and fills the capability gaps that VARs and their customers complain about daily. It is not a replacement for Counterpoint — Counterpoint remains the system of record for transactions and inventory execution. The Gap Backbone is the single source of modern truth: real-time intelligence, AI-driven insights, and a verifiable evidentiary chain, all running on the existing on-prem estate without requiring migration.

## Purpose

Counterpoint cannot natively provide analytics at speed, demand forecasting with agricultural seasonality, pricing optimization, LP anomaly detection, or a conversational store manager interface. VARs know this — it is their most common customer complaint. The Gap Backbone is the answer. It makes the existing Counterpoint investment 3–5× more valuable without touching the POS, the database, or the customer's operational workflow.

## Pipeline Architecture

```
Counterpoint SQL Server (on-prem, Windows Server)
  ↓  Transaction Stream Processor (TSP)
     — Go binary, Docker container, runs on store hardware
     — SQL Server Change Tracking + high-watermark polling fallback
     — Reads: PS_DOC_HDR, PS_DOC_LIN, IM_ITEM, AR_CUST, PS_STR, SY_*, EC_*
     — Primary: Change Tracking (requires VAR enablement on SQL Server tables)
     — Fallback: watermark polling on DOC_DT / updated_at (works on any version, misses deletes)
  ↓  elJeffe Inscription Layer
     — CRDM classification (People / Places / Things / Events / Workflows / Platform)
     — Namespace stamp: {tenant_id}.{source_code}.{module_letter}.{sequence}
     — source_code = 'counterpoint' (multi-source discriminator — Square stays parallel)
     — Receipt hash: SHA256(prev_hash || canonical_payload) at document level
       (PS_DOC_HDR + all PS_DOC_LIN children = one atomic evidentiary unit)
     — Sequence: per-module per-tenant (shardable, matches Pub/Sub topic structure)
  ↓  AVAX Receipt Anchor (see raas-receipt-as-a-service card)
     — Batch accumulator: 60s or N events → Merkle root → C-Chain anchor tx
     — anchor_ref written back into AlloyDB and BigQuery alongside payload
  ↓  GCP Pub/Sub
     — Topic per module per tenant
     — Decouples ingestion from write path; survives downstream backpressure
  ↓  ┌─────────────────────────────┬────────────────────────────┐
     │  BigQuery Storage Write API  │  AlloyDB                   │
     │  — Analytics workloads       │  — Operational reads       │
     │  — ≥100ms latency budget     │  — <10ms latency budget    │
     │  — ML training datasets      │  — Current inventory pos.  │
     │  — Batch reports             │  — Open orders             │
     │  — Demand forecasting        │  — Customer lookup         │
     │  — Historical LP patterns    │  — Virtual Store Manager   │
     │  — Pricing elasticity        │    synchronous queries     │
     └─────────────────────────────┴────────────────────────────┘
  ↓  Vertex AI / Gemini (inference layer)
     — Managed endpoints per tenant (quota isolation, cost attribution)
     — Not direct Gemini API — Vertex AI for multi-tenant SLA and billing
     — Models: anomaly detection, demand forecast, pricing optimization,
       Virtual Store Manager (conversational), multi-modal (live-goods damage)
```

**Critical boundary rule:** If the latency budget is under 50ms, it lives in AlloyDB. Everything else is BigQuery. This boundary must be explicit in every feature design — the moment a synchronous path hits BigQuery, you have a UX problem.

## Build Priority (A → B → D)

**A — Data layer (foundation).** High-speed ingestion from Counterpoint on-prem SQL Server into BigQuery + AlloyDB. Structured tables (PS_DOC_HDR, PS_DOC_LIN, IM_ITEM, AR_CUST) + unstructured (audit logs, notes, Rapid POS custom fields, vendor PDFs, live-goods photos). This is the "always-on" spine. Nothing else is credible without it.

**B — AI capability layer (differentiation).** Gemini / Vertex AI embedded on top of the data layer:
- Anomaly detection: LP rules, pricing abuse, margin erosion
- Demand forecasting: seasonality + weather + promotion lift isolation
- Pricing / markdown optimization: elasticity at item × store × week
- Virtual Store Manager: conversational insights, root-cause, next-best-action
- Multi-modal: image of damaged perennials → shrink classification

**D — Scale and security (production-readiness).** Multi-tenant isolation, zero-downtime schema evolution (Counterpoint upgrades + Rapid POS custom tables), full audit trail, VAR-friendly deployment (secure read-only connector, on-prem agent or secure tunnel), compliance readiness.

**Note on demo priority:** A < B < D is the correct build order. For the VAR sales asset, demo B first — the Virtual Store Manager and the four L&G queries. A is invisible to the VAR; they care about what their customers can do. Open with B, let A be the infrastructure that makes it possible.

## The Four L&G Demo Queries (Prototype Spec)

These four questions are the entire prototype. Answer them beautifully on real Counterpoint data and you have the sales asset:

1. "Which categories are running below target margin this week?"
2. "Show me live-goods shrinkage by supplier and store"
3. "What should I order for next weekend's promotion?"
4. "Which employees have unusual void/refund patterns after 8pm?"

Each query exercises a different backbone capability: margin analytics (BigQuery), shrink classification (AI layer + multi-modal), demand forecasting (Vertex AI), and LP anomaly detection (elJeffe receipt chain + behavioral rules). Together they demonstrate the full stack without requiring a complete implementation.

## Core IP Boundary

The TSP and elJeffe inscription layer are hand-rolled. They are the only parts of the stack where the logic is Counterpoint-aware, CRDM-native, and LP-evidentiary. No generic CDC connector understands PS_DOC_HDR or knows to emit a receipt hash at the document level. Everything else (GCP, BigQuery, AlloyDB, Pub/Sub, Vertex AI) is bought. Hand-roll only the core IP; buy the infrastructure.

## Multi-Tenant Design

Designed from day one for multi-VAR, multi-tenant operation: hundreds of garden-center chains, thousands of stores. Tenant isolation at Pub/Sub topic, BigQuery dataset, AlloyDB schema, and Vertex AI endpoint level. Per-tenant cost attribution via source_code + tenant_id stamped on every event. VAR-level rollup available for channel analytics and billing.

## Offline Contract

The store must run without internet. Counterpoint does. The TSP must also. Cloud connectivity enables fleet telemetry, model updates, and cross-chain LP patterns — but store-level detection, receipt chain generation, and work dispatch all run locally. Internet outage is a sync delay, not an outage. The SQLite event buffer on the store hardware holds events until the WAN path recovers.

## Related

- [[raas-receipt-as-a-service]] — the AVAX anchor layer; receipt chain as a standalone product
- [[var-acquisition-thesis]] — how the Gap Backbone changes VAR partnership and acquisition economics
- [[counterpoint-product-state-2026]] — the .NET/SQL Server architecture the TSP reads from
- [[ncr-ecosystem-2026]] — why Counterpoint is in maintenance mode and why the displacement window exists
- [[icp-murdochs-reference]] — canonical enterprise-scale ICP; every backbone capability simultaneously necessary
- Brain/wiki/ncr-counterpoint-phase-0-context-brief.md — Phase 0 technical dispatch; CRDM×spine mapping
- docs/sdds/canary/ncr-counterpoint-openapi.yaml — 71 paths, 95 operations; the REST surface above the SQL layer
