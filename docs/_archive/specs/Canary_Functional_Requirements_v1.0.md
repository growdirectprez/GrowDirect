---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Functional Requirements

**Version:** 1.0
**Date:** February 21, 2026
**Author:** Eva (Program Manager)
**Directive:** Jeffe — "Rescript our whole thought process into a set of functional and technical requirements from pure .md files."
**Classification:** Internal — **BLUEPRINT STAGE DOCUMENT**
**Status:** DRAFT — Part of Alpha 3X rehydration. Technology-agnostic. Defines WHAT, not HOW.
**Companion:** `Canary_Technical_Requirements_v1.0.md` (defines HOW for the Alpha 3X stack)

---

> *"If the soil is barren our little farm won't grow anything."* — Jeffe

---

## Purpose

This document defines everything Canary must DO — independent of technology choices. If we replaced every component in the stack tomorrow, these requirements would still be valid. They derive from the CRDM, the enterprise ancestor spec, the Factory Process, and Jeffe's directives.

The companion Technical Requirements document maps each FR to specific Alpha 3X stack components.

---

## FR-1: Data Ingestion

### FR-1.1: Real-Time POS Data Capture
The platform SHALL ingest transaction data from Square POS in real time via webhooks. Ingestion SHALL be idempotent — processing the same webhook twice produces no duplicate records.

**Acceptance Criteria:**
- FR-1.1.1: Webhook payloads are received, validated (HMAC signature), and stored within 5 seconds of Square dispatch
- FR-1.1.2: Duplicate webhook delivery does not create duplicate records (idempotency key enforcement)
- FR-1.1.3: Failed ingestion attempts are stored in a dead letter queue for manual replay
- FR-1.1.4: Raw payload is preserved in full (JSONB) alongside extracted fields

### FR-1.2: Seven Canonical Data Sources
The platform SHALL ingest data from all seven CRDM canonical sources as they become available from the POS provider.

| Source | Description | CRDM Reference |
|--------|-------------|---------------|
| Transaction Header | One record per POS transaction | Source #1 |
| Tender | Payment method detail per transaction | Source #2 |
| Line Items | Per-item detail per transaction | Source #3 |
| Employee | Operator records + timecard data | Source #4 |
| Product/Article | Sellable item reference data | Source #5 |
| Store/Location | Physical location + hierarchy | Source #6 |
| Customer | Customer identification + LTV | Source #7 |

**Acceptance Criteria:**
- FR-1.2.1: Each data source maps to one or more canonical tables per CRDM
- FR-1.2.2: A vendor-specific parser translates POS-native formats to canonical schema
- FR-1.2.3: The canonical schema is POS-agnostic — Chirp rules operate identically regardless of source POS

### FR-1.3: POS-Agnostic Parser Architecture
The platform SHALL support multiple POS providers via vendor-specific parsers that all output to the same canonical schema.

**Acceptance Criteria:**
- FR-1.3.1: Square parser exists and maps all available API endpoints to CRDM tables
- FR-1.3.2: Parser interface is documented — a new POS (Clover, Toast) can be added without modifying Chirp rules
- FR-1.3.3: Each parser declares which CRDM fields it populates and which remain empty (coverage matrix)

### FR-1.4: Canary-Native Data Sources
The platform SHALL ingest data sources not present in the enterprise ancestor spec but enabled by real-time API access.

| Source | Description | LP Significance |
|--------|-------------|-----------------|
| Cash Drawer Events | No-sales, paid in/out, shift close | #1 traditional LP signal |
| Inventory Adjustments | Count changes, manual adjustments | Shrinkage measurement |
| Gift Card Activities | Load, activate, redeem, deactivate | Top-3 LP loss category |
| Employee Timecards | Clock in/out, breaks, location | Ghost employee detection |

**Acceptance Criteria:**
- FR-1.4.1: Cash drawer events ingested with shift-level and event-level granularity
- FR-1.4.2: Inventory adjustments captured with employee attribution and reason codes
- FR-1.4.3: Gift card lifecycle tracked (load → activate → redeem → deactivate)
- FR-1.4.4: Employee timecards ingested with break periods and location

---

## FR-2: Fraud Detection (Chirp)

### FR-2.1: Rule-Based Detection Engine
The platform SHALL evaluate configurable detection rules against ingested data to identify potential loss events.

**Acceptance Criteria:**
- FR-2.1.1: All 22 Chirp rules (C-001 through C-802) are evaluable
- FR-2.1.2: Each rule has a configurable threshold that merchants can adjust
- FR-2.1.3: Rules execute on a configurable schedule (real-time event trigger or periodic sweep)
- FR-2.1.4: Rule evaluation produces an alert record with: rule ID, severity, merchant, location, employee (if applicable), evidence payload, timestamp

### FR-2.2: Multi-Source Detection
Chirp rules SHALL correlate data across multiple canonical sources to detect patterns invisible in any single source.

**Key cross-source rules:**
- OFF_CLOCK_TRANSACTION: transactions + timecards
- SWEET_HEART_PATTERN: line items + customer + employee
- AFTER_HOURS_REFUND: transactions + location business hours
- CROSS_STORE_RETURN: transactions + refund links + locations

**Acceptance Criteria:**
- FR-2.2.1: Cross-source rules can join across any combination of the 7 canonical sources + 4 Canary-native sources
- FR-2.2.2: Detection results include the complete evidence chain (which records from which tables triggered the alert)

### FR-2.3: Alert Lifecycle
Each alert SHALL follow a lifecycle from detection through resolution.

**States:** NEW → REVIEWED → INVESTIGATING → ESCALATED → RESOLVED (with resolution reason: confirmed_fraud, false_positive, inconclusive, no_action)

**Acceptance Criteria:**
- FR-2.3.1: Alert records are immutable once created (append-only)
- FR-2.3.2: Status changes are tracked in alert_history with timestamp and user
- FR-2.3.3: Merchants receive notifications for new alerts (configurable: email, webhook, in-app)

---

## FR-3: Case Management (Fox)

### FR-3.1: Case Creation and Tracking
The platform SHALL support creating investigation cases from one or more alerts, with full lifecycle tracking.

**Acceptance Criteria:**
- FR-3.1.1: A case can be created from a single alert or by grouping multiple related alerts
- FR-3.1.2: Cases track: subject(s), status, priority, assigned investigator, timeline, evidence, resolution
- FR-3.1.3: Case status lifecycle: OPEN → UNDER_INVESTIGATION → PENDING_REVIEW → CLOSED

### FR-3.2: Evidence Chain of Custody
All evidence attached to a case SHALL be immutable and auditable.

**Acceptance Criteria:**
- FR-3.2.1: Evidence records are INSERT-only (enforced at database level, not application)
- FR-3.2.2: Every evidence access is logged (who viewed what, when)
- FR-3.2.3: Evidence hash chain provides tamper detection
- FR-3.2.4: Evidence packets can be exported for law enforcement in a standard format

### FR-3.3: Case Timeline
Every action on a case SHALL be recorded in a chronological, immutable timeline.

**Acceptance Criteria:**
- FR-3.3.1: Timeline entries include: action type, actor, timestamp, details
- FR-3.3.2: Timeline is INSERT-only
- FR-3.3.3: Timeline is exportable as a report for legal/HR proceedings

---

## FR-4: Multi-Tenant Architecture

### FR-4.1: Merchant Data Isolation
The platform SHALL guarantee that no merchant can access another merchant's data under any circumstance.

**Acceptance Criteria:**
- FR-4.1.1: Data isolation is enforced at the database layer (not just application code)
- FR-4.1.2: A bug in application code cannot leak data across merchants
- FR-4.1.3: Multi-tenant isolation passes a formal penetration test before Square Marketplace listing

### FR-4.2: Role-Based Access Control
The platform SHALL support role-based access within each merchant tenant.

**Roles:** merchant_owner, store_manager, associate, analyst, viewer

**Acceptance Criteria:**
- FR-4.2.1: Each role has a defined permission set (what data they can see, what actions they can take)
- FR-4.2.2: Permissions are enforced at both the API layer and database layer (defense-in-depth)
- FR-4.2.3: Role assignment is managed by the merchant_owner

### FR-4.3: Organizational Hierarchy
The platform SHALL support merchant organizational structures (multi-location, districts, regions).

**Acceptance Criteria:**
- FR-4.3.1: A merchant can have multiple locations
- FR-4.3.2: Locations can be grouped into hierarchy levels (district, region, market)
- FR-4.3.3: Access can be scoped by hierarchy level (district manager sees all district locations)

---

## FR-5: Analytics & Reporting (Owl)

### FR-5.1: Dashboard Metrics
The platform SHALL provide pre-computed LP metrics at multiple granularity levels.

**Metric domains:**
- Location-level: daily/hourly transaction counts, refund rates, void rates, cash variance
- Employee-level: refunds issued, voids, discount rates, off-clock activity, risk score trend
- Product-level: return rates, shrinkage rates, discount abuse
- Merchant-level (aggregate): Total Retail Loss, loss by category, trend analysis

**Acceptance Criteria:**
- FR-5.1.1: Metrics are pre-aggregated for dashboard performance (not computed on every page load)
- FR-5.1.2: Drill-down from aggregate to detail is supported (merchant → location → employee → transaction)
- FR-5.1.3: All metrics are tenant-isolated (merchant sees only their data)

### FR-5.2: Data Exploration
Internal analysts and advanced merchants SHALL have ad-hoc query capability against their data.

**Acceptance Criteria:**
- FR-5.2.1: SQL-based exploration of analytics data (read-only)
- FR-5.2.2: Query results respect tenant isolation
- FR-5.2.3: Query performance does not impact transactional ingestion

### FR-5.3: Scheduled Reports
The platform SHALL support scheduled delivery of LP summary reports.

**Acceptance Criteria:**
- FR-5.3.1: Daily and weekly LP summary reports configurable per merchant
- FR-5.3.2: Reports delivered via email or in-app notification
- FR-5.3.3: Report content includes: new alerts, open cases, metric trends, anomaly flags

---

## FR-6: Square Marketplace Compliance

### FR-6.1: OAuth 2.0 Integration
The platform SHALL implement Square's OAuth 2.0 flow per Marketplace certification requirements.

**Acceptance Criteria:**
- FR-6.1.1: Authorization code flow with PKCE
- FR-6.1.2: Token refresh handled automatically before expiration
- FR-6.1.3: Token revocation supported (merchant uninstalls)
- FR-6.1.4: Minimal OAuth scopes requested (only what's needed for LP detection)

### FR-6.2: Webhook Processing
The platform SHALL receive and validate Square webhook notifications per Marketplace requirements.

**Acceptance Criteria:**
- FR-6.2.1: HMAC-SHA256 signature verification on all incoming webhooks
- FR-6.2.2: Webhook endpoint responds within Square's timeout requirements
- FR-6.2.3: Webhook processing is idempotent (safe to replay)

### FR-6.3: Data Security
The platform SHALL meet Square's data security requirements for Marketplace apps.

**Acceptance Criteria:**
- FR-6.3.1: All merchant data encrypted at rest (AES-256)
- FR-6.3.2: All API communication over TLS 1.2+
- FR-6.3.3: Access tokens encrypted at rest, never logged in plaintext
- FR-6.3.4: Audit log tracks all data access events

### FR-6.4: Merchant Experience
The platform SHALL provide a merchant onboarding experience that meets Square Marketplace UX requirements.

**Acceptance Criteria:**
- FR-6.4.1: One-click install from Square Marketplace
- FR-6.4.2: Merchant sees data within 5 minutes of installation (initial data pull)
- FR-6.4.3: Merchant can uninstall cleanly (data retention per policy, tokens revoked)

---

## FR-7: Data Integrity & Audit

### FR-7.1: Financial Ledger Immutability
Transaction data SHALL be append-only. No UPDATE or DELETE on financial records.

**Acceptance Criteria:**
- FR-7.1.1: Database-level triggers prevent UPDATE/DELETE on transaction tables
- FR-7.1.2: Application cannot bypass immutability (no admin override for financial data)
- FR-7.1.3: Corrections are handled via adjustment records, not by modifying originals

### FR-7.2: Hash-Chain Audit Trail
All audit log entries SHALL be hash-chained for tamper detection.

**Acceptance Criteria:**
- FR-7.2.1: Each audit entry includes SHA-256 hash of (current entry + previous entry hash)
- FR-7.2.2: Chain integrity is verifiable via a validation function
- FR-7.2.3: Any break in the chain is detectable and reportable

### FR-7.3: Evidentiary Integrity
Case evidence SHALL maintain chain-of-custody standards suitable for law enforcement and HR proceedings.

**Acceptance Criteria:**
- FR-7.3.1: Evidence records are INSERT-only (database-enforced)
- FR-7.3.2: Every evidence access is logged (viewer, timestamp, access type)
- FR-7.3.3: Evidence export includes full chain-of-custody metadata

---

## FR-8: Authentication & Authorization

### FR-8.1: Identity Management
The platform SHALL provide enterprise-grade identity management for merchants and their team members.

**Acceptance Criteria:**
- FR-8.1.1: Secure user registration and login (password-based + SSO)
- FR-8.1.2: Multi-factor authentication available for merchant owners
- FR-8.1.3: Password reset and account recovery flows
- FR-8.1.4: Session management with configurable timeout

### FR-8.2: API Authentication
All API access SHALL require authentication via industry-standard tokens.

**Acceptance Criteria:**
- FR-8.2.1: JWT-based API authentication
- FR-8.2.2: Token expiration and refresh mechanism
- FR-8.2.3: API rate limiting per merchant

---

## FR-9: Administration

### FR-9.1: Data Browsing & Management
Internal administrators SHALL be able to browse and manage all platform data through a web interface.

**Acceptance Criteria:**
- FR-9.1.1: Browse all 35+ CRDM tables with filtering, sorting, and search
- FR-9.1.2: Inline relationship navigation (click transaction → see line items, tenders, refund links)
- FR-9.1.3: Role-based data views (admin sees all, merchant sees theirs)
- FR-9.1.4: Custom admin actions (create Fox case from alert, escalate, bulk operations)

### FR-9.2: Rule Configuration
Merchants SHALL be able to configure Chirp detection thresholds through the admin interface.

**Acceptance Criteria:**
- FR-9.2.1: Each of the 22 Chirp rules has a merchant-configurable threshold
- FR-9.2.2: Changes are logged in the audit trail
- FR-9.2.3: Default thresholds are provided (merchants don't have to configure anything to get value)

---

## FR-10: Workflow Orchestration

### FR-10.1: Scheduled Detection
Chirp detection rules SHALL run on configurable schedules in addition to real-time event triggers.

**Acceptance Criteria:**
- FR-10.1.1: Hourly sweep of all active rules across all merchants
- FR-10.1.2: Failed sweeps retry with exponential backoff
- FR-10.1.3: Sweep execution is monitored with alerting on persistent failure
- FR-10.1.4: Sweep results are logged for debugging and performance tracking

### FR-10.2: ETL Pipeline
The platform SHALL support scheduled data transformations from transaction log to analytics metrics.

**Acceptance Criteria:**
- FR-10.2.1: Daily metric aggregation (location, employee, product levels)
- FR-10.2.2: ETL jobs are idempotent (safe to re-run)
- FR-10.2.3: ETL failure alerts operators and does not corrupt existing metrics

---

## FR-11: Bitcoin & Lightning Integration (Goose — Post-MVP)

### FR-11.1: Lightning Payment Processing
The platform SHALL support Bitcoin Lightning payments for merchant subscriptions and pay-per-query metering.

### FR-11.2: LNURL-Auth
The platform SHALL support passwordless authentication via Lightning wallet signature.

### FR-11.3: Chain of Custody Ordinals
Fox evidence packets SHALL be mintable as Bitcoin Ordinals for tamper-proof, timestamp-verified chain of custody.

> **Note:** FR-11 requirements are post-MVP. They are documented here for architectural planning — the stack must not preclude these capabilities.

---

## Traceability Matrix

| FR | CRDM Source(s) | Epic(s) | Priority |
|----|---------------|---------|----------|
| FR-1.1 | All | E0, E1 | P0 |
| FR-1.2 | Sources 1-7 | E1 | P0 |
| FR-1.3 | — | E0, E7 | P1 |
| FR-1.4 | Canary-native | E1 | P0 |
| FR-2.1 | All | E1 | P0 |
| FR-2.2 | Cross-source | E1 | P0 |
| FR-2.3 | — | E1 | P1 |
| FR-3.1 | — | E3 | P1 |
| FR-3.2 | — | E3 | P1 |
| FR-3.3 | — | E3 | P1 |
| FR-4.1 | All | E0 | P0 |
| FR-4.2 | — | E0 | P0 |
| FR-4.3 | Source #6 | E0 | P2 |
| FR-5.1 | canary_metrics | E5 | P1 |
| FR-5.2 | canary_metrics | E5 | P2 |
| FR-5.3 | canary_metrics | E5 | P2 |
| FR-6.1 | — | E2 | P0 |
| FR-6.2 | — | E2 | P0 |
| FR-6.3 | — | E2 | P0 |
| FR-6.4 | — | E2 | P1 |
| FR-7.1 | canary_sales | E0 | P0 |
| FR-7.2 | audit_log | E0 | P0 |
| FR-7.3 | Fox tables | E3 | P1 |
| FR-8.1 | — | E0 | P0 |
| FR-8.2 | — | E0 | P0 |
| FR-9.1 | All | E0 | P1 |
| FR-9.2 | detection_rules | E1 | P1 |
| FR-10.1 | All | E1 | P0 |
| FR-10.2 | canary_metrics | E5 | P1 |
| FR-11.x | — | E4 | Post-MVP |

---

*These requirements define WHAT Canary does. The Technical Requirements document defines HOW the Alpha 3X stack implements each one.*

*"Do it right, do it once." — Jeffe*
