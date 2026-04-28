---
spec-version: 1.0
target-implementation: Go
stack: PostgreSQL 17 + pgx + sqlc | Chi HTTP | REST | go-redis | pgvector-go
source: Curated from Canary Python prototype SDDs (GRO-617)
status: active-build-spec
updated: 2026-04-28
---

# Canary Platform Overview

**Type:** Product Context (top-level product SDD)
**Last reviewed:** 2026-04-28

---

## Purpose

This SDD captures the product-level context for Canary: what it is, who it serves, how it connects to POS systems, the module roadmap, and the security/compliance posture. It is the narrative layer — the architecture SDD covers service topology; this document covers product and market positioning.

Use this document when you need to understand **why** Canary exists and **what** it delivers, not **how** the services are wired together.

---

## Product Definition

Canary is a POS-agnostic retail operations platform for small and mid-size specialty retailers. It delivers loss prevention, case management, and store analytics to independent merchants at a price and operational footprint appropriate for one to thirty locations.

**Core value proposition:** The SMB retailer gets enterprise-grade detection, investigation, and compliance documentation — running on the POS they already have — with near-zero operational overhead. No dedicated LP staff. No manual report review. The platform runs the detection cycle, surfaces findings, and drives investigation workflows autonomously. The merchant reviews outcomes, not process.

**Design principle — agent-driven, minimal HIL:** Every workflow is designed to run without a human operator in the loop unless legally required. Canary's agents handle detection, evidence packaging, case initiation, and compliance tracking. Human-in-the-loop is an escalation path for ambiguous or high-stakes decisions — not the default operating mode. This is the only way Canary is viable for SMB: the merchant can't afford an LP department, so the platform is the LP department.

**Data contract — ARTS-native:** Canary's canonical retail data model is built against the ARTS POSLOG standard. NCR Counterpoint is the reference implementation of that standard — full inventory, receiving, purchase orders, paycode structures, EJ spine, multi-store transfers. Square is a lightweight subset: its entire data surface maps cleanly into the ARTS model Canary already handles. Any POS that speaks ARTS or a subset of it connects as an adapter projection. Building to the full ARTS surface means Square compatibility comes for free; the reverse is not true.

**Target users:** Small and mid-size specialty retailers (1–31 locations). NCR Counterpoint merchants reached via Counterpoint VARs (Rapid POS and others — garden centers, gun, feed-tack, beverage, wine verticals). Square merchants via Marketplace (prototype live, Marketplace-certified). Owner-operators who manage everything from inventory to payroll, often from a single device.

**Distribution model:** VAR co-sell. Counterpoint VARs bring the merchant relationships and domain expertise; Canary provides the product. The VAR becomes the delivery partner for Canary's capabilities into their existing install base. This is not a direct-to-merchant cold-start — it is a channel model with established trust already in place on the merchant side.

---

## The Problem

Retail shrink costs U.S. retailers ~$112B/year. Enterprise retailers address this with dedicated LP departments and six-figure software budgets. The SMB merchant has two options: manually review transaction reports (doesn't scale) or pay for enterprise LP software built for 500-store chains (doesn't fit).

The most common preventable loss for Square merchants is refund fraud: employees processing refunds for transactions that never occurred, refunding to cards they control, or processing refunds outside business hours. Square's native reporting surfaces data but does not flag patterns, generate alerts, or create case records.

---

## Platform Modules

| Module | Function | Status | Description |
|--------|----------|--------|-------------|
| **Chirp** | Detection Engine | **MVP** | Real-time detection via 37 Square rules + 25+ Counterpoint rules across 12 families. Plain-language alerts with transaction evidence and employee attribution. See Chirp SDD. |
| **Fox** | Evidence Chain | **MVP** | INSERT-only evidence locker, SHA-256 hash-chained, append-only timeline. EBR class inside Hawk. See Fox SDD. |
| **Hawk** | Case Management | **Phase 1** | Incident-typed investigation workflow with wizard FSM, dual-track action codes (DE/PV), compliance obligations, card factory. Supersedes Fox flat case lifecycle. See Hawk SDD. |
| **Bull** | Distribution Intel | **Phase 3 stub** | Transfer-loss reconciliation + multi-store distribution recommendations. Gated on Module D. See Bull SDD. |
| **Goose** | Bitcoin & Lightning | **Phase 2** | BTCPay Server, Lightning Network payments, LNURL-auth passwordless login, sat-denominated billing. See Goose SDD. |
| **Owl** | Analytics Oracle | **Phase 2** | Total Retail Loss dashboard, industry benchmarks, AI-powered analysis via local LLM inference. Hawk card corpus as Phase 4 recall surface. See Owl SDD. |

---

## Square Integration

Three API surfaces:

| API | Purpose | Detail |
|-----|---------|--------|
| **OAuth 2.0** | Authorization | Single-click install. Scopes: MERCHANT_PROFILE_READ, PAYMENTS_READ, PAYMENTS_WRITE, ITEMS_READ, CUSTOMERS_READ, ORDERS_READ. See Identity-Square SDD. |
| **Payments API** | Transaction Ingestion | Date-range filtered fetch. Extracts card fingerprint, employee ID, location, amount. |
| **Webhooks API** | Real-Time Processing | payment.created, payment.updated, refund.created, order.created. HMAC-SHA256 verification on every event. See Webhook Pipeline SDD. |

**Security posture:**
- HMAC-SHA256 webhook signature verification on every inbound event
- AES-256-GCM encrypted access/refresh tokens in merchant sources table
- No Square credentials logged or in error responses
- HTTPS enforced on all production routes

---

## Merchant Experience

Zero-configuration: connect Square, receive alerts.

1. Merchant finds Canary in Square App Marketplace → clicks Install
2. Square OAuth authorization → merchant approves permissions
3. Canary ingests past 30 days of transaction data
4. First dashboard with Chirp alerts already generated
5. **Time from discovery to first alert: under 5 minutes**

Dashboard shows active alerts sorted by severity. Each alert: triggering transaction, detection rule, employee ID, amount. Merchants acknowledge, investigate, or resolve without leaving Canary.

HIGH and CRITICAL alerts trigger SMS notification within 30 seconds via Twilio.

---

## Security and Compliance

| Control | Status | Detail |
|---------|--------|--------|
| OAuth 2.0 Authorization | Implemented | Square OAuth, CSRF state parameter |
| HMAC-SHA256 Webhook Verification | Implemented | Every webhook verified before processing |
| TLS / HTTPS Enforcement | Production | Let's Encrypt, HTTP→HTTPS redirect |
| Encrypted Credential Storage | Implemented | AES-256-GCM encrypted tokens |
| Row-Level Security | Implemented | Database-level RLS, cross-tenant prevention |
| Immutable Audit Log | Implemented | INSERT-only with SHA-256 hash chain |
| No PII Beyond Square Policy | Verified | Only permitted fields stored |
| Startup Config Validation | Implemented | Fails fast on missing env vars |
| Credential Scan | CI/CD Gate | CI pipeline confirms no keys in code/history |
| Privacy Policy | Pre-launch | Required for Marketplace submission |
| Terms of Service | Pre-launch | Required for Marketplace submission |

---

## Data Integrity Principle

Canary analyzes people's livelihoods. Every accusation must be supported by verifiable facts.

- Evidence tables are INSERT-only at the database level — enforced by triggers, not application convention
- No record can be modified or deleted once written, by any actor, including administrators
- SHA-256 hash chain provides cryptographic proof of record integrity
- Three-schema separation (`app`, `sales`, `fox`) isolates operational, transactional, and evidentiary data

See Data Model SDD for schema details.

---

## Roadmap

| Phase | Focus | Deliverables |
|-------|-------|-------------|
| **Phase 1 — Go Foundation** | Core pipeline + Counterpoint-first | TSP ingestion (Counterpoint poll + Square webhook), Chirp detection engine, Fox evidence chain, Hawk case management, merchant dashboard, multi-tenant auth |
| **Phase 2 — Agent Layer** | Autonomous operations | ALX MCP server, agent-driven investigation workflows, Owl analytics oracle, automated Hawk card generation |
| **Phase 3 — Distribution Intel** | Bull + multi-store | Bull distribution analytics, multi-store reconciliation, VAR multi-tenant management surface |
| **Phase 4 — Ecosystem** | Vertical depth + payments | Vertical rule expansions (gun, feed-tack, beverage, wine), Goose payment layer, Chain of Custody Ordinals |

---

## Open Source

Canary will be released as open source. Transparency is the brand; expertise and execution are the moat. Licensing strategy under review with legal counsel.

---

## Related SDDs

- **Architecture** — Service mesh, startup order, dependencies
- **Chirp** — Detection rule catalog, 3 tiers
- **Fox** — Case management, evidence chain
- **Owl** — AI analytics, LLM inference
- **Goose** — Treasury, Bitcoin/L402
- **Identity-Square** — Square OAuth, token storage
- **Webhook Pipeline** — Ingestion, HMAC validation
- **Data Model** — 60+ models, PII map
