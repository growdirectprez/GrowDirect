---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Product & Services

> **Domain:** Product vision, service architecture, detection rules, AI capabilities
> **Last Updated:** 2026-03-19 | **Classification:** Confidential

---

## Product Identity

Canary LP is an AI-powered loss prevention platform for Square merchants. It targets the 33 million SMB retailers who lack access to enterprise-grade loss prevention tools. The product ingests real-time POS data via Square webhooks, runs detection rules against every transaction, and surfaces actionable intelligence through a mobile-first dashboard.

The core value proposition: real-time shrink detection, delivered to the store floor, not quarterly reports delivered to the executive suite. Pricing starts at $29/month for the base tier.

---

## Service Architecture

Canary is composed of eight core services. Each service follows a standardized microservice delivery pattern: routes (Flask blueprint) → service (business logic) → models (SQLAlchemy 2.0) → tests (unit, route, integration).

### TSP — Triple Subscriber Pipeline
The data ingestion backbone. Square POS webhooks arrive at Flask, pass HMAC verification, and enter Valkey Streams. Three subscribers process sequentially: Sub 1 (Seal) hashes the raw payload and stores evidence records; Sub 2 (Parse) transforms vendor-specific data into the canonical CRDM format; Sub 3 (Merkle) batches events into Merkle trees and submits roots to Bitcoin via the elJeffe protocol.

Pipeline flow: Square POS → Webhook → HMAC verify → Valkey Streams → Sub1 (Seal) → Sub2 (Parse) → Sub3 (Merkle) → PostgreSQL → Sub4 (Detect) → Chirp sweep → Alert → Dashboard → Fox case.

### Chirp — Detection Engine
Real-time anomaly detection with 26+ rules across 8 categories. Rules evaluate at three tiers: Tier 1 (per-webhook stateless checks), Tier 2 (velocity engine for pattern trending), and Tier 3 (future AI-driven contextual analysis).

**Detection Categories (Active):**
- Payment anomalies (C-001–C-009): excessive refund rates, high-value voids, split tender patterns
- Cash drawer (C-063–C-068): variance per shift, expected vs. actual, employee patterns
- Void patterns (C-010–C-019): rapid voids, post-void timing, void-after-close
- Gift card (C-020–C-029): activation anomalies, reload patterns, cross-location usage
- Loyalty abuse (C-030–C-039): point inflation, redemption without sale, velocity
- Timecard (C-040–C-042): off-clock transaction correlation, ghost shifts
- Order integrity (C-050–C-059): discount stacking, below-cost pricing, price override frequency
- Composite (C-070+): multi-signal employee risk scoring
- Inventory (C-080–C-085): adjustment anomalies, discrepancy detection
- Device integrity (C-901–C-909): device attestation flags for Merkle batches

**Detection Rules Blocked by Data Gaps (GRO-266):**
- C-201 (excessive discount): requires line_item_discounts table — discount name, type, percentage, scope not captured
- C-203 (sweethearting): requires line_item_modifiers — modifier identity and price delta not captured
- C-009 (delay hold): requires payment.delay_action field — currently dropped by parser
- C-010 (partial auth): requires payment.approved_money field — currently dropped by parser
- C-602 (gift card drain): requires gift card activity fields (order_id, line_item_uid, payment_id) — currently dropped

These rules are designed but cannot fire until the corresponding data expansions from GRO-266 are implemented.

Each rule has a severity level, threshold configuration, and produces structured alerts with evidence references.

### Fox — Case Management
Investigation workflow engine with an evidence locker backed by hash-chain integrity. Fox cases aggregate related alerts, attach evidence records, and track investigation timeline. Case subjects can be employees, customers, or locations. The evidence chain uses SHA-256 hashing to maintain tamper-evident integrity.

Key entities: fox_cases, case_subjects, case_evidence, case_timeline, case_actions. Case statuses progress through: open → investigating → pending_review → resolved → closed.

### Owl — AI Intelligence Layer
Natural language search, drill analysis, and reporting powered by qwen3:14b via local Ollama inference. Owl is the "Retail Intelligence Engine" — it connects data streams, applies research rigor, and delivers plain-English insights.

**Core capabilities:**
- The One Thing: daily digest identifying the single most important insight
- Heartbeat: real-time business health metric
- Heatmap: location/employee/product performance visualization
- Velocity trends: sales trends, discount rates, cash variance over time
- Natural language search across all Canary data (transactions, alerts, cases, employees)

Output types: memo, number, alert_set, comparison, trend. Every insight answers "So what should I do?" with confidence levels (high/medium/low).

### ALX — Agent Memory
pgvector knowledge graph with 954+ curated memories covering every SDD, service domain, and architectural decision. Provides contextual recall via `memory_recall("topic")` and domain-level context via `domain_context("service_name")`. Stored in a separate `canary_memory` database.

### Identity — OAuth & Session Management
Square OAuth2 onboarding flow for merchant registration. Manages sandbox and production credentials, session lifecycle, and JWT-based authentication. Keycloak integration carries org_id in JWT claims.

### Analytics — Dashboard Metrics
Star schema metrics layer in the `metrics` PostgreSQL schema. Computes daily/hourly aggregates, fiscal calendar alignment, and employee scoring. Powers the merchant-facing dashboard with location comparisons, trend analysis, and benchmarking.

### RaaS — Rule-as-a-Service
Namespace registry and source system mapping. Provides the public verification API for the elJeffe protocol: POST /v1/verify, GET /v1/receipt/{namespace_guid}, GET /v1/resolve/{identifier}. Each API call costs 1 sat via L402 micropayment.

---

## Data Model Overview

Single PostgreSQL database (`canary`) with three schemas:

| Schema | Purpose | Write Path | Key Tables |
|--------|---------|------------|------------|
| `app` | Merchants, users, alerts, Fox cases, audit log | Flask (canary_app role) | merchants, employees, locations, detection_rules, alerts, fox_cases, namespace_registrations |
| `sales` | Transactions, refunds, line items, tenders | TSP pipeline only (canary_tsp role) | transactions, transaction_line_items, transaction_tenders, refund_links, evidence_records, merkle_batches |
| `metrics` | Daily/hourly metrics, employee analytics | Flask (canary_app role) | daily_metrics, hourly_metrics, employee_scores |

Separate database: `canary_memory` (ALX pgvector knowledge graph).

### Canonical UUID Principle (GRO-237)
Every entity uses Canary's own UUID as the primary identifier. Square's external_id is stored for source system reconciliation only. Lookups: UUID first, external_id fallback. API responses: "id" = our UUID, "external_id" = Square's ID. Frontend links: /txn/<uuid>, /alert/<uuid>, /case/<uuid>.

---

## Frontend Architecture

Mobile-first 3-panel UI: Chirps (alert feed) + Owl (intelligence/search) + Vault (evidence/cases). Built with Jinja2 templates extending base.html, styled with CSS design tokens. 27 Flask blueprints organized as *_wired (route handlers) and *_mcp (MCP tool endpoints).

---

## Multi-Tenant Architecture (ADR-001)

Organization → Merchant hierarchy enables merchants with multiple Square merchant IDs to see combined dashboards. Organizations are the billing root; each org owns 1..N merchant accounts. RLS (Row-Level Security) is array-aware: `merchant_id = ANY(string_to_array(current_setting(...), ','))`. Session flow: JWT carries org_id → middleware lookups merchant IDs → combined or filtered view.

---

*Canary LP | GrowDirect Inc. | Confidential*
