# Canary Platform Overview

**Wiki:** [[Brain/wiki/canary-platform-overview|Canary Platform Overview]]
**Type:** Product Context (top-level product SDD)
**Last reviewed:** 2026-04-14
**Source:** Canary_Platform_Overview_v1.0_1.docx (Feb 2026, Square Marketplace submission)

---

## Purpose

This SDD captures the product-level context for Canary LP: what it is, who it serves, how it integrates with Square, the module roadmap, and the security/compliance posture. It is the external-facing narrative layer — the architecture SDD covers the service mesh and technical topology; this document covers the product and market positioning.

Use this document when you need to understand **why** Canary exists and **what** it delivers, not **how** the services are wired together.

---

## Product Definition

Canary LP is a loss prevention platform built exclusively for Square merchants. It brings enterprise-grade fraud detection, case management, and loss analytics to independent sellers at a price and complexity level appropriate for one or two locations.

**Core value proposition:** The independent merchant who can't afford enterprise loss prevention gets the same detection, investigation, and documentation capabilities — running entirely on Square APIs, through the Square Marketplace.

**Target users:** Small and mid-size Square merchants (1–5 locations). Owner-operators who manage everything from inventory to payroll, often from a single device.

---

## The Problem

Retail shrink costs U.S. retailers ~$112B/year. Enterprise retailers address this with dedicated LP departments and six-figure software budgets. The SMB merchant has two options: manually review transaction reports (doesn't scale) or pay for enterprise LP software built for 500-store chains (doesn't fit).

The most common preventable loss for Square merchants is refund fraud: employees processing refunds for transactions that never occurred, refunding to cards they control, or processing refunds outside business hours. Square's native reporting surfaces data but does not flag patterns, generate alerts, or create case records.

---

## Platform Modules

| Module | Function | Status | Description |
|--------|----------|--------|-------------|
| **Chirp** | Detection Engine | **MVP** | Real-time detection via 29 rules across 3 severity tiers. Plain-language alerts with transaction evidence and employee attribution. See [[chirp\|Chirp SDD]]. |
| **Fox** | Case Management | **MVP** | Structured investigation workflow. INSERT-only evidence locker, SHA-256 hashed, append-only timeline. Built to evidentiary standards for HR/legal/law enforcement. See [[fox\|Fox SDD]]. |
| **Goose** | Bitcoin & Lightning | **Phase 2** | BTCPay Server, Lightning Network payments, LNURL-auth passwordless login, sat-denominated billing. See [[goose\|Goose SDD]]. |
| **Owl** | Analytics Oracle | **Phase 2** | Total Retail Loss dashboard, industry benchmarks, AI-powered analysis via Ollama. See [[owl\|Owl SDD]]. |

---

## Square Integration

All integration uses Square's official Python SDK. Three API surfaces:

| API | Purpose | Detail |
|-----|---------|--------|
| **OAuth 2.0** | Authorization | Single-click install. Scopes: MERCHANT_PROFILE_READ, PAYMENTS_READ, PAYMENTS_WRITE, ITEMS_READ, CUSTOMERS_READ, ORDERS_READ. See [[identity-square\|Identity-Square SDD]]. |
| **Payments API** | Transaction Ingestion | Date-range filtered fetch. Extracts card fingerprint, employee ID, location, amount. |
| **Webhooks API** | Real-Time Processing | payment.created, payment.updated, refund.created, order.created. HMAC-SHA256 verification on every event. See [[webhook-pipeline\|Webhook Pipeline SDD]]. |

**Security posture:**
- HMAC-SHA256 webhook signature verification
- AES-256 encrypted access/refresh tokens in merchants table
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
| OAuth 2.0 Authorization | Implemented | Square SDK, CSRF state parameter |
| HMAC-SHA256 Webhook Verification | Implemented | Every webhook verified before processing |
| TLS / HTTPS Enforcement | Production | Let's Encrypt, HTTP→HTTPS redirect |
| Encrypted Credential Storage | Implemented | AES-256 encrypted tokens |
| Row-Level Security | Implemented | Database-level RLS, cross-tenant prevention |
| Immutable Audit Log | Implemented | INSERT-only with SHA-256 hash chain |
| No PII Beyond Square Policy | Verified | Only permitted fields stored |
| Startup Config Validation | Implemented | Fails fast on missing env vars |
| Credential Scan | CI/CD Gate | GitHub Actions confirms no keys in code/history |
| Privacy Policy | Pre-launch | Required for Marketplace submission |
| Terms of Service | Pre-launch | Required for Marketplace submission |

---

## Data Integrity Principle

Canary analyzes people's livelihoods. Every accusation must be supported by verifiable facts.

- Evidence tables are INSERT-only at the database level — enforced by triggers, not convention
- No record can be modified or deleted once written, by any actor, including administrators
- SHA-256 hash chain provides cryptographic proof of record integrity
- Three-schema separation (app, sales, fox) isolates operational, transactional, and evidentiary data

See [[data-model|Data Model SDD]] for schema details.

---

## Roadmap

| Phase | Focus | Deliverables |
|-------|-------|-------------|
| **MVP — Now** | Foundation + Chirp + Fox | Square OAuth, Chirp detection, Fox case management, merchant dashboard, Square Marketplace certification |
| **Phase 2 — Q2 2026** | Goose + Owl | BTCPay Server, Lightning payments, LNURL-auth, Total Retail Loss dashboard, AI analysis |
| **Phase 3 — Q3 2026** | Ecosystem Deepening | Advanced webhooks, Team API, Appointments, Square for Restaurants/Retail verticals |
| **Phase 3 — Q3 2026** | Agentic Defense | Behavioral fingerprinting, bot/CUA detection, synthetic identity clustering |
| **Phase 4 — Q4 2026** | Chain of Custody Ordinals | Bitcoin Ordinal minting for evidence packets, blockchain-timestamped chain of custody |

---

## Open Source

Canary will be released as open source. Transparency is the brand; expertise and execution are the moat. Licensing strategy under review with legal counsel.

---

## Related SDDs

- [[architecture|Architecture]] — Service mesh, startup order, dependencies
- [[chirp|Chirp]] — 29 detection rules, 3 tiers
- [[fox|Fox]] — Case management, evidence chain
- [[owl|Owl]] — AI analytics, Ollama
- [[goose|Goose]] — Treasury, Bitcoin/L402
- [[identity-square|Identity-Square]] — Square OAuth, token storage
- [[webhook-pipeline|Webhook Pipeline]] — Ingestion, HMAC validation
- [[data-model|Data Model]] — 60+ models, PII map
