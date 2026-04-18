---
date: 2026-04-14
type: wiki
status: current
tags: [canary, platform, square, loss-prevention]
sources: [Brain/raw/inbox/Canary_Platform_Overview_v1.0_1.docx, Canary/CLAUDE.md]
last-compiled: 2026-04-14
---

# Canary — Platform Overview

Canary is a loss prevention platform built exclusively for Square merchants. It brings the fraud detection, case management, and loss analytics capabilities that enterprise retailers rely on to the independent sellers that Square was built to serve.

The founding team brings over 30 years of direct experience designing and operating retail loss prevention systems at scale — across national grocery, convenience, and specialty retail. Canary is not a technology experiment applied to retail. It is retail operations knowledge expressed as software, rebuilt on Square APIs and priced for the merchant running one or two locations.

> **Built for Square. Committed to Square.** Canary is purpose-built for the Square ecosystem and the 33 million sellers Square serves. Block's mission — economic empowerment for the underdog — is exactly the mission Canary shares. The independent merchant who can't afford enterprise loss prevention is the same seller Square was built to empower.

## The Problem

Retail shrink — loss through theft, fraud, and operational error — costs U.S. retailers approximately $112 billion per year. Large retailers have dedicated LP teams, enterprise software, and analytics platforms. For the small business owner running one or two Square locations, none of those tools are accessible or affordable.

The most common and preventable form of internal loss for Square merchants is refund fraud: employees processing refunds for transactions that never occurred, refunding to cards they control, or processing refunds outside business hours. Square's native reporting surfaces transaction data but does not flag patterns, generate alerts, or create case records.

A Square merchant today has two options: manually review transaction reports — a process that scales poorly — or pay for enterprise LP software built for 500-store chains. Canary fills the gap.

## Platform Modules

Canary is a multi-module platform. Each module addresses a distinct phase of the merchant's loss prevention workflow: detect, investigate, document, and analyze.

| Module | Function | Description |
|--------|----------|-------------|
| **[[canary-detection\|Chirp]]** | Detection Engine | Real-time detection of suspicious patterns. 29 rules across 3 severity tiers with plain-language alerts. The core product. |
| **Fox** | Case Management | Structured incident reporting, evidence locker with immutable chain-of-custody, case timeline, and resolution tracking. Built for HR, legal, and law enforcement use. |
| **Goose** | Bitcoin & Lightning | BTCPay Server integration for Lightning Network payment acceptance, LNURL-auth passwordless login, sat-denominated subscription billing. |
| **[[canary-architecture\|Owl]]** | Analytics Oracle | Total Retail Loss dashboard aggregating shrink, fraud, and operational loss. Benchmarked against industry averages. AI-powered analysis via Ollama. |

**Current scope (MVP):** Chirp detection engine + Fox case management Sprint 1. Goose and Owl follow in Phase 2.

## Square Integration

Canary is built on Square's official Python SDK and integrates with three API surfaces. All communication occurs over HTTPS. No PII is stored beyond what Square's data use policy permits. Access tokens are encrypted at rest using AES-256.

| API | Purpose | Detail |
|-----|---------|--------|
| **OAuth 2.0** | Authorization | Single-click install via standard OAuth flow. Scopes: MERCHANT_PROFILE_READ, PAYMENTS_READ, PAYMENTS_WRITE, ITEMS_READ, CUSTOMERS_READ, ORDERS_READ. |
| **Payments API** | Transaction Ingestion | Fetches transaction and refund data with date-range filtering. Extracts card fingerprint, employee ID, location, and amount. |
| **Webhooks API** | Real-Time Processing | Subscribes to payment.created, payment.updated, refund.created, order.created. HMAC-SHA256 signature verification on every event. |

> **Security:** HMAC-SHA256 webhook signature verification using SQUARE_WEBHOOK_SIGNATURE_KEY. Access tokens and refresh tokens stored AES-256 encrypted. No Square credentials ever logged or included in error responses. HTTPS enforced on all production routes.

## Chirp — Detection Engine

Chirp is a configurable rules framework that evaluates Square transaction data in real time as it arrives via webhook. Each triggered rule generates an alert with a severity grade, linked transaction evidence, and employee attribution. Thresholds are configurable per merchant; defaults are based on industry benchmarks from the team's operational experience.

Card fingerprint — from Square's `payment.card_details.card.fingerprint` field — is used for velocity calculations rather than card last-four digits, ensuring the same physical card is accurately tracked across transactions.

**Detection rules (selected):**

| Rule | Trigger | Default Severity |
|------|---------|-----------------|
| High Refund Velocity | > 3 refunds/day | MEDIUM → CRITICAL (scales with count) |
| Large Refund Amount | > $100 single refund | HIGH |
| After-Hours Activity | 10 PM – 6 AM local time | MEDIUM |
| Rapid Refund Sequence | Multiple refunds < 30 min | MEDIUM |

Every alert is graded LOW, MEDIUM, HIGH, or CRITICAL. HIGH and CRITICAL trigger SMS notification within 30 seconds via Twilio. Alert status follows a tracked lifecycle: open → acknowledged → investigating → resolved → false_positive. Every transition is logged to an immutable audit trail.

→ Full detection engine details: [[canary-detection|Detection Engine wiki]]

## Fox — Case Management

When a merchant identifies a suspicious pattern — from a Chirp alert or direct observation — Fox provides the structured workflow to investigate, document, and resolve it. Fox is built to evidentiary standards: records suitable for HR proceedings, civil litigation, and law enforcement referrals. Once evidence is written, it cannot be altered by any actor at any level.

**Fox Sprint 1 (MVP) capabilities:**

- **Incident Report Creation** — Structured form: incident type, severity, location, date/time, involved parties, initial evidence. Cases from Chirp alerts are pre-populated with transaction data.
- **Evidence Locker** — INSERT-only enforcement at the database level. Each evidence record is SHA-256 hashed on upload. Every access logged with actor, timestamp, and IP.
- **Case Timeline** — Append-only chronological record. Cannot be edited or deleted.
- **Case Resolution** — Structured options: verbal warning, written warning, suspension, termination, ban, police report filed, insurance claim, no action. Closure requires a documented resolution note.

> **Data integrity principle:** This platform analyzes people's livelihoods. Every accusation must be supported by verifiable facts. Evidence tables are INSERT-only at the database level — enforced by triggers, not convention. No record can be modified or deleted once written, by any actor, including administrators.

## Technical Architecture

See [[canary-architecture|Architecture wiki]] and [[canary-data-model|Data Model wiki]] for full details.

| Layer | Technology | Detail |
|-------|-----------|--------|
| Backend | Python 3.12 / Flask | REST API, webhook ingestion, detection engine, multi-tenant RBAC, audit logging |
| Database | PostgreSQL 17 | Single database, 4 schemas: app, sales, fox, metrics. 60+ models. |
| Square | Square Python SDK | OAuth 2.0, Payments API, Webhooks API with HMAC-SHA256 |
| Frontend | Tailwind CSS + Alpine.js | Merchant dashboard, case management UI, alert detail views |
| Infrastructure | Docker Compose | Gunicorn, PostgreSQL, Valkey 8, Ollama |
| Auth | Flask-Login + RBAC | Five roles: owner, admin, manager, analyst, viewer. Permission enforcement at API layer. |

**Three-schema architecture:** Canary separates operational data (`app`), transaction records (`sales`), investigation data (`fox`), and analytics (`metrics`). High-volume webhook ingestion does not compete with dashboard queries. The transaction log maintains INSERT-only integrity for evidentiary purposes.

## Security

| Control | Status | Detail |
|---------|--------|--------|
| OAuth 2.0 Authorization | Implemented | Square SDK, standard OAuth flow, CSRF state parameter |
| HMAC-SHA256 Webhook Verification | Implemented | Every webhook verified before processing |
| TLS / HTTPS Enforcement | Production | Let's Encrypt, HTTP → HTTPS redirect |
| Encrypted Credential Storage | Implemented | AES-256 encrypted access/refresh tokens |
| Row-Level Security | Implemented | Database-level RLS prevents cross-tenant access |
| Immutable Audit Log | Implemented | INSERT-only audit_log with SHA-256 hash chain |
| No PII Beyond Square Policy | Verified | Only permitted fields stored |
| Startup Config Validation | Implemented | Fails fast on missing env vars |

## Merchant Experience

Canary is designed for merchants who are not technologists. Zero-configuration: connect Square, receive alerts.

**Installation flow:**
1. Merchant finds Canary in Square App Marketplace and clicks Install
2. Canary redirects to Square OAuth — merchant approves permissions
3. Canary ingests past 30 days of transaction data from Payments API
4. Merchant sees first dashboard with Chirp alerts already generated
5. Total time from discovery to first alert: under 5 minutes

The dashboard shows all active alerts sorted by severity. Each alert shows the triggering transaction, detection rule, employee ID, and amount. Merchants acknowledge, investigate, or resolve alerts without leaving Canary.

## Roadmap

| Phase | Focus | Deliverables |
|-------|-------|-------------|
| **MVP — Now** | Foundation + Chirp + Fox | Square OAuth, Chirp detection, Fox case management, merchant dashboard, Square Marketplace certification |
| **Phase 2 — Q2 2026** | Goose: Bitcoin & Lightning | BTCPay Server, Lightning payments, LNURL-auth, sat-denominated billing |
| **Phase 2 — Q2 2026** | Owl: Analytics Oracle | Total Retail Loss dashboard, industry benchmarks, AI-powered analysis |
| **Phase 3 — Q3 2026** | Square Ecosystem Deepening | Advanced webhooks, Team API, Appointments, Square for Restaurants / Retail verticals |
| **Phase 3 — Q3 2026** | Agentic Threat Defense | Behavioral fingerprinting, bot/CUA detection, synthetic identity clustering |
| **Phase 4 — Q4 2026** | Chain of Custody Ordinals | Bitcoin Ordinal minting for evidence packets — blockchain-timestamped chain of custody |

## Open Source Commitment

Canary will be released as open source. Transparency is the brand. Expertise and execution are the moat. Any merchant, developer, or retailer can inspect exactly how Canary detects fraud, manages evidence, and protects their data.

## Related

- [[canary-architecture|Architecture]] — 16 services, MCP layer, data flow
- [[canary-detection|Detection Engine]] — 29 Chirp rules, threshold system, alert pipeline
- [[canary-data-model|Data Model]] — 60+ models across 4 schemas
- [[canary-sales-strategy|Sales Strategy]] — Gold list rules, adoption ladder
