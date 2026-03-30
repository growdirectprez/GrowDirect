---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary Technology Blueprint — The Ingredients List

**Version:** 1.1 (Version Corrections Applied)
**Date:** February 21, 2026 (original) | **Updated:** February 22, 2026
**Author:** Eva (Program Manager)
**Reviewers:** PhD (due diligence lead), Tom (architecture), Jeremy (implementation)
**Directive:** Jeffe — "I just want to make sure we start from the top and agree our tech stack, SDKs, licenses, DBs, flavor, etc., as ingredients before we start to cook again."
**Classification:** Internal — **TEAM REVIEW REQUIRED BEFORE CODING RESUMES**
**Status:** DRAFT — Pending PhD/Tom/Jeremy due diligence sign-off
**Due Diligence Sources:** `Markdown/Research/Canary_Alpha3X_Stack_References_v1.0.md` (300+ URLs, 11 layers)

---

> *"We have spent just over a week making really good progress to see what is possible and have done the research to regroup and attack this from ground up."*
> — Jeffe, February 21, 2026

---

### ✅ VERSION CORRECTIONS APPLIED (v1.1 — Feb 22, 2026)

The following version discrepancies from v1.0 have been **resolved**. All corrections are reflected in-line throughout this document and validated against `devops/docker-compose.alpha3x.yml`. Full audit trail: `Markdown/Specs/Canary_Technology_Blueprint_v1.1_Corrections.md`.

| Component | v1.0 Said | v1.1 Corrected To | Status |
|---|---|---|---|
| Apache Superset | 4.x | **6.0.0** | ✅ Corrected. Docker Compose confirmed. |
| Apache Airflow | 2.x | **3.0.0** (Dec 2025, 2.x EOL April 2026) | ✅ Corrected. Docker Compose confirmed. DAG validation needed (Jeremy). |
| Square Python SDK | v35 (pinned) | **v35 pinned → v43.2.0 target** (R-12 pending) | 🟡 Pin unchanged. Jeremy assessment required. |
| Hasura | "v2/v3 evaluation" | **v2.44.0 CE (Apache-2.0)** — v3 DDN is cloud-only | ✅ Clarified. Evaluation CLOSED. |
| Redis | Standard | **Replaced with Valkey 8 (BSD-3, Linux Foundation)** | ✅ Corrected. Syd approved. |
| Flask vs FastAPI | Open evaluation | **CLOSED: Keep Flask** (R-5 delivered Feb 21) | ✅ Decided. |
| Nginx vs Traefik | Open evaluation | **CLOSED: Nginx selected** | ✅ Decided. |
| Airflow executor | Open evaluation | **CLOSED: LocalExecutor** | ✅ Decided. |

---

## Purpose

This document is the Bill of Materials for Canary's platform. Every technology, SDK, license, database, API, and architectural decision is listed here with its role, version, license, and justification. Nothing enters the stack without appearing in this document first. Nothing gets coded until this document is reviewed and signed off.

This is the Factory Process Blueprint stage applied to the platform itself.

---

## Part 1: Architecture Overview

### The Alpha 3X Stack

The team evaluated 15+ enterprise open-source tools and selected a stack that replaces hand-rolled scaffolding with battle-tested components while preserving Canary's core IP (CRDM, Chirp detection rules, Square parsers, Fox evidence chain).

```
┌─────────────────────────────────────────────────────────────────┐
│                     MERCHANT (Browser/Mobile)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ Directus │  │ Superset │  │  Fox UI (TBD)│  │ Merchant  │  │
│  │  Admin   │  │ Dashbrd  │  │  Case Mgmt   │  │  Portal   │  │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘  └─────┬─────┘  │
│       │              │               │                │         │
├───────┴──────────────┴───────────────┴────────────────┴─────────┤
│                        API GATEWAY LAYER                         │
│  ┌──────────────────┐  ┌──────────────────────────────────────┐ │
│  │  Hasura GraphQL  │  │  Flask Business Logic Service        │ │
│  │  (Auto-generated │  │  (Chirp rules, HMAC verification,   │ │
│  │   from Postgres) │  │   Fox evidence chain, parsers)      │ │
│  └────────┬─────────┘  └────────────────┬─────────────────────┘ │
│           │                              │                       │
├───────────┴──────────────────────────────┴───────────────────────┤
│                        AUTH LAYER                                 │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │  Keycloak (OIDC, Multi-Tenant Realms, RBAC, SSO)           ││
│  └──────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────┤
│                      DATA LAYER                                   │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │  PostgreSQL (Three-Database Architecture per CRDM)          ││
│  │  canary_app │ canary_sales │ canary_metrics                 ││
│  │  35 tables  │ Append-only  │ Star schema                    ││
│  └──────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────┤
│                    ORCHESTRATION LAYER                             │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │  Apache Airflow (Chirp scheduled sweeps, ETL, ingestion)    ││
│  └──────────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────┤
│                    EXTERNAL INTEGRATIONS                           │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐  ┌─────────────┐ │
│  │ Square API │  │ BTCPay   │  │ OrdinalsBot│  │ Future POS  │ │
│  │ (Webhooks  │  │ Server   │  │ (Fox Chain │  │ (Clover,    │ │
│  │  + OAuth)  │  │ (Goose)  │  │  of Custody│  │  Toast)     │ │
│  └────────────┘  └──────────┘  └────────────┘  └─────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### What We Keep (IP — This Is Ours)

These are the assets that carry forward from the dry run. They are Jeffe's intellectual product, built from decades of enterprise retail experience. They get audited, not replaced.

| Asset | Description | Status |
|-------|-------------|--------|
| **CRDM** | Canary Retail Data Model. 35 tables, 7 data sources, 3-database architecture. Enterprise bones. | Preserve — audit against ARTS/GSLM |
| **Chirp Rules** | 22 detection rules (C-001 through C-804). The LP intelligence. | Preserve — audit thresholds and logic |
| **Square Parsers** | Vendor-specific webhook/API parsers mapping Square data to CRDM canonical tables. | Preserve — extend for new data sources |
| **Fox Schema** | Case management, evidence chain, INSERT-only evidentiary tables. | Preserve — audit against enterprise ancestor spec |
| **Factory Process** | 6-stage build methodology. How we work. | Preserve — this IS the process |
| **PRDs (E0-E3)** | 4 PRDs, 18 features, 148 acceptance criteria, 34 test scenarios. | Preserve — update for new stack |
| **Brand System** | Colors, typography, templates, brand guide. | Preserve — no changes |

### What We Replace (Scaffolding — These Were Learning Tools)

| Current | Replacement | Why |
|---------|-------------|-----|
| Hand-rolled auth (bcrypt + sessions) | **Keycloak** | Enterprise identity management, OIDC, multi-tenant realms, SSO |
| Hand-rolled RBAC (permissions module) | **Keycloak** + **Hasura** row-level permissions | Defense-in-depth: Keycloak manages roles, Hasura enforces at query level, Postgres RLS at data level |
| Hand-rolled admin panel | **Directus** | Auto-generated from DB schema, custom actions, role-based views |
| SQLAlchemy ORM + raw SQL | **Hasura** (GraphQL) + **SQLAlchemy** (business logic only) | Hasura auto-generates CRUD; Flask/SQLAlchemy retained only for Chirp rules and Fox evidence chain |
| Jinja2 templates (monolith) | **Directus** (admin) + **Superset** (analytics) + TBD merchant portal | Separation of concerns. Each UI serves one audience. |
| Manual Chirp scheduling (polling worker) | **Apache Airflow** | DAG-based scheduling, retry logic, monitoring, dependency management |
| SQLite (dev) | **PostgreSQL** everywhere | One database engine, dev through prod. No more SQLite/Postgres parity issues. |

---

## Part 2: The Stack — Component by Component

### Layer 1: Database — PostgreSQL

| Property | Value |
|----------|-------|
| **Component** | PostgreSQL |
| **Role** | Primary datastore — all three databases (canary_app, canary_sales, canary_metrics) |
| **Version** | 17.x (current LTS, supported through 2029) |
| **License** | PostgreSQL License (BSD-like, fully permissive) |
| **Docker Image** | `postgres:17-alpine` |
| **Why** | Jeffe confirmed. Enterprise-proven. JSONB for webhook payloads. RLS for multi-tenant isolation. Monthly partitioning for transaction scale. ARTS/GSLM aligned. |

**Key capabilities we use:**
- Row-Level Security (RLS) — multi-tenant data isolation at the database layer
- JSONB columns — store raw webhook payloads alongside extracted fields
- Table partitioning — monthly partitions on transaction tables for scale
- SHA-256 hash chain — audit log integrity via `pgcrypto` extension
- Triggers — INSERT-only enforcement on evidentiary tables
- `pgcrypto` extension — cryptographic functions for hash chains

**Schema migration tool:** Alembic (via SQLAlchemy) OR Hasura Migrations — **PhD/Tom to evaluate and recommend.**

**Due diligence questions for PhD/Tom/Jeremy:**
- [ ] Alembic vs Hasura Migrations vs raw SQL migration files — which gives us the most control and auditability?
- [ ] Connection pooling strategy: PgBouncer vs built-in?
- [ ] Backup strategy for three-database architecture?
- [ ] Read replica architecture for Superset analytics queries?

---

### Layer 2: Identity & Auth — Keycloak

| Property | Value |
|----------|-------|
| **Component** | Keycloak |
| **Role** | Identity provider, authentication, authorization, multi-tenant realm management |
| **Version** | 26.x (latest stable) |
| **License** | Apache-2.0 |
| **GitHub Stars** | ~24k |
| **Docker Image** | `quay.io/keycloak/keycloak:26-alpine` |
| **Backed by** | Red Hat / CNCF ecosystem |
| **Why** | Replaces hand-rolled auth. OIDC standard. Per-merchant realm = true multi-tenant isolation. SSO for merchant chains. Admin console included. |

**Key capabilities we use:**
- OIDC / OAuth 2.0 — standard authentication protocol
- Multi-tenant realms — one realm per merchant (or merchant group)
- Role-based access control — merchant_owner, store_manager, associate, admin
- Social login / SSO — optional for merchant convenience
- API token management — JWT tokens consumed by Hasura and Flask
- LNURL-auth integration potential — Bitcoin-native passwordless auth (future)

**Integration points:**
- Keycloak issues JWT → Hasura validates JWT claims → row-level permissions enforced
- Keycloak issues JWT → Flask validates JWT → Chirp/Fox business logic authorized
- Directus configured as Keycloak OIDC client
- Superset configured as Keycloak OIDC client

**Due diligence questions:**
- [ ] Keycloak realm-per-merchant vs single realm with groups — which scales better for 10K+ merchants?
- [ ] JWT token size implications with merchant metadata in claims?
- [ ] Keycloak HA deployment — active/passive or active/active?

---

### Layer 3: API — Hasura GraphQL Engine

| Property | Value |
|----------|-------|
| **Component** | Hasura GraphQL Engine |
| **Role** | Auto-generated real-time GraphQL API from PostgreSQL schema |
| **Version** | **v2.44.0 CE** (Apache-2.0) — ~~v2/v3 evaluation~~ closed in v1.1. **v3 DDN is cloud-only/proprietary, NOT self-hosted.** |
| **License** | Apache-2.0 (Community Edition) |
| **GitHub Stars** | ~31k |
| **Docker Image** | **`hasura/graphql-engine:v2.44.0`** |
| **Why** | Eliminates hand-written CRUD API code. Auto-generates queries, mutations, subscriptions from Postgres tables. Row-level permissions from JWT claims. Real-time subscriptions for live dashboards. |

**Key capabilities we use:**
- Auto-generated GraphQL from PostgreSQL tables — instant API for all 35 CRDM tables
- Row-level permissions — merchant_id filtering enforced at query level via JWT claims
- Real-time subscriptions — live alert feeds, dashboard updates
- Remote schemas — Flask business logic exposed as GraphQL endpoints
- Event triggers — database events trigger Flask webhooks (Chirp rule evaluation)
- Actions — custom business logic (Flask) invoked via GraphQL mutations

**What Hasura does NOT handle (Flask retains):**
- Chirp detection rule evaluation (business logic)
- Square webhook HMAC verification (security)
- Fox evidence chain INSERT-only enforcement (evidentiary integrity)
- Square OAuth token management (vendor-specific)
- Ordinal minting (Bitcoin integration)

**Due diligence questions:**
- [x] ~~Hasura v2 vs v3~~ **CLOSED (v1.1):** v3 DDN is cloud-only/proprietary. Canary uses **v2.44.0 CE (Apache-2.0)**.
- [ ] Hasura event triggers vs Airflow DAGs for Chirp scheduling — overlap or complement?
- [ ] Hasura Console as internal admin tool vs Directus — do we need both?
- [ ] Performance at scale: Hasura connection pooling with 35+ tables and RLS?

---

### Layer 4: Admin & Data Platform — Directus

| Property | Value |
|----------|-------|
| **Component** | Directus |
| **Role** | Admin UI, data management interface, internal operations dashboard |
| **Version** | 11.x (latest stable) |
| **License** | BSL 1.1 (converts to open source after 3 years) |
| **GitHub Stars** | ~28k |
| **Docker Image** | `directus/directus:11` |
| **Why** | Auto-generates admin UI from database schema. Custom actions ("Flag for Review", "Create Fox Case"). Role-based views. Replaces hand-rolled admin panel and gives internal team enterprise-grade data access. |

**Key capabilities we use:**
- Auto-generated UI from PostgreSQL schema — browse all 35 CRDM tables
- Custom actions — "Create Fox Case from Alert", "Escalate to Law Enforcement"
- Role-based views — different data views per role (admin, merchant, analyst)
- Inline relationships — click a transaction → see its line items, tenders, refund links
- Keycloak SSO integration — single sign-on via OIDC
- REST + GraphQL API — programmatic access to managed data

**License note (BSL 1.1):** Directus uses the Business Source License. Free for self-hosted use. The BSL converts to an open-source license (GPL-compatible) after 3 years. Commercial hosting requires a license. For Canary's self-hosted deployment model, this is functionally free. **Syd to review BSL 1.1 terms for any constraints on our use case.**

**Due diligence questions:**
- [ ] BSL 1.1 implications for Square Marketplace app listing?
- [ ] Directus as merchant-facing admin vs internal-only — scope decision needed
- [ ] Directus vs Hasura Console — which is the primary data management tool?
- [ ] Custom Directus extensions for Fox case management workflows?

---

### Layer 5: Analytics — Apache Superset

| Property | Value |
|----------|-------|
| **Component** | Apache Superset |
| **Role** | Analytics dashboards, data exploration, the Owl module's visualization layer |
| **Version** | **6.0.0** (released late 2025) — ~~4.x~~ corrected in v1.1 |
| **License** | Apache-2.0 |
| **GitHub Stars** | ~63k |
| **Docker Image** | **`apache/superset:6.0.0`** |
| **Backed by** | Apache Software Foundation |
| **Why** | Enterprise-grade analytics. SQL Lab for ad-hoc queries. Dashboard builder. Chart types for LP metrics. Row-level security integration. This IS the Owl module's presentation layer. |

**Key capabilities we use:**
- Dashboard builder — Total Retail Loss dashboard, merchant KPIs, Chirp alert trends
- SQL Lab — ad-hoc data exploration for internal analysts
- Row-level security — merchant data isolation (connects to Keycloak roles)
- Embedded dashboards — merchant portal can embed Superset charts
- Scheduled reports — email/Slack alerts for LP metrics
- 40+ chart types — time series, maps, tables, pivot tables, histograms

**Owl module mapping:**
- `canary_metrics` database → Superset datasource
- Pre-aggregated daily/hourly metrics → Superset dashboards
- ML risk scores → visualized as time-series trends
- Employee scorecards → Superset pivot tables with drill-down

**Due diligence questions:**
- [ ] Superset embedded mode for merchant portal — authentication flow?
- [ ] Superset + Keycloak integration — native OIDC or custom security manager?
- [ ] Performance with monthly-partitioned tables — query optimization needed?

---

### Layer 6: Orchestration — Apache Airflow

| Property | Value |
|----------|-------|
| **Component** | Apache Airflow |
| **Role** | Workflow orchestration — scheduled Chirp sweeps, ETL jobs, data ingestion pipelines |
| **Version** | **3.0.0** (released Dec 2025) — ~~2.x~~ corrected in v1.1. **⚠️ Airflow 2.x EOL April 2026.** |
| **License** | Apache-2.0 |
| **GitHub Stars** | ~38k |
| **Docker Image** | **`apache/airflow:3.0.0`** |
| **Backed by** | Apache Software Foundation |
| **Why** | Replaces manual polling worker and cron-based scheduling. DAG-based workflows with retry logic, dependency management, monitoring. Scales from single-node to distributed. |
| **Migration** | Airflow 2.x → 3.0 migration guide: `https://airflow.apache.org/docs/apache-airflow/stable/migration-ref.html`. TaskFlow API changes, new scheduler, UI rewrite. `airflow db migrate` replaces `airflow db upgrade`. |

**Key capabilities we use:**
- DAG-based scheduling — Chirp detection sweeps run on configurable intervals
- Retry and alerting — failed jobs retry with exponential backoff, alert on persistent failure
- Task dependencies — ingest data → validate → run Chirp rules → generate alerts (in order)
- Monitoring UI — visual DAG status, task logs, execution history
- Provider packages — PostgreSQL, HTTP, Slack providers for integrations
- Variable/connection management — Square API credentials stored securely

**Chirp integration:**
```
DAG: chirp_detection_sweep (hourly)
├── Task: check_new_transactions (sensor — wait for new data)
├── Task: run_chirp_rules (Python operator — evaluate all 22 rules)
├── Task: generate_alerts (Python operator — create alert records)
├── Task: notify_merchants (HTTP operator — send notifications)
└── Task: update_metrics (Python operator — refresh canary_metrics)
```

**Due diligence questions:**
- [x] ~~Airflow executor type~~ **CLOSED (v1.1):** **LocalExecutor** selected for Alpha/MVP. Sufficient for <50 DAGs. No Redis/Celery dependency. CeleryExecutor for future production scale.
- [ ] Airflow vs Hasura event triggers for real-time detection — complementary or redundant?
- [ ] Airflow resource requirements — memory/CPU for the iMac QA box? Docker Compose allocates 2.5GB total (1.5GB webserver + 1GB scheduler).

---

### Layer 7: Business Logic Service — Flask (Retained)

| Property | Value |
|----------|-------|
| **Component** | Flask |
| **Role** | Thin business logic service — Chirp rules, webhook processing, Fox evidence chain, Square OAuth |
| **Version** | 3.1.x |
| **License** | BSD-3-Clause |
| **GitHub Stars** | ~68k |
| **Why** | The team knows it. It works. In the Alpha 3X stack, Flask is no longer the entire application — it's a focused microservice handling only what the enterprise tools can't: custom business logic, vendor-specific integrations, and evidentiary integrity enforcement. |

**What Flask handles in the new architecture:**
- Square webhook receiver + HMAC verification
- Square OAuth token management + refresh flow
- Chirp rule evaluation engine (`chirp.py`)
- Fox evidence chain INSERT-only enforcement
- Ordinal minting trigger (Bitcoin chain of custody)
- Custom LP business logic that doesn't belong in a generic tool

**What Flask no longer handles:**
- ~~User authentication~~ → Keycloak
- ~~RBAC / permissions~~ → Keycloak + Hasura
- ~~Admin panel~~ → Directus
- ~~Analytics dashboards~~ → Superset
- ~~CRUD API endpoints~~ → Hasura
- ~~Scheduled jobs~~ → Airflow
- ~~Database migrations~~ → Alembic or Hasura Migrations

**Due diligence question:**
- [x] ~~Flask vs FastAPI~~ **CLOSED (v1.1, R-5 delivered Feb 21):** Keep Flask for Alpha 3X. Evaluate FastAPI post-E2 (April 2026). Analysis: `Markdown/Specs/Flask_vs_FastAPI_Service_Layer_Analysis_v1.0.md`. Migration prep (service layer decoupling, Pydantic models) can proceed in parallel.

---

### Layer 8: Square Integration

| Property | Value |
|----------|-------|
| **Component** | Square Python SDK |
| **Role** | Official SDK for Square API integration — OAuth, webhooks, API calls |
| **Current Version** | squareup v35.x (pinned in requirements.txt: `>=35.0.0,<42.0.0`) |
| **Latest Version** | **v43.2.0** (2025-10-16 API version) — 8 major versions ahead. R-12 migration assessment pending (Jeremy). |
| **License** | MIT |
| **Why** | Official SDK. Required for Square Marketplace certification (E2). |

**OAuth scopes required (full LP coverage per CRDM):**
- `PAYMENTS_READ` — Transaction headers, tenders
- `ORDERS_READ` — Line items, discounts, taxes
- `CASH_DRAWER_READ` — No-sales, paid in/out, variance
- `TIMECARDS_READ` — Employee clock-in/out, break compliance
- `INVENTORY_READ` — Shrinkage tracking, count adjustments
- `GIFTCARDS_READ` — Gift card load/redeem velocity
- `CUSTOMERS_READ` — Customer profiles
- `EMPLOYEES_READ` — Employee records
- `ITEMS_READ` — Product catalog
- `MERCHANTS_READ` — Merchant/location metadata

**Due diligence questions:**
- [ ] Upgrade from v35 to v43 SDK — breaking changes assessment needed
- [ ] Square Marketplace certification requirements — does the Alpha 3X architecture comply?
- [ ] Webhook delivery reliability — do we need a dead letter queue at the Flask layer or Airflow?

---

### Layer 9: Bitcoin / Lightning Integration

| Property | Value |
|----------|-------|
| **Component** | BTCPay Server (Goose module) |
| **Role** | Bitcoin/Lightning payment processing, invoice generation |
| **Version** | Latest stable |
| **License** | MIT |
| **Why** | Bitcoin-native payment rail. Self-hosted. No third-party payment processor. Lightning for micropayments (pay-per-query metering). |

| Component | Role | License |
|-----------|------|---------|
| **BTCPay Server** | Payment processing, Lightning invoicing | MIT |
| **OrdinalsBot API** | Fox chain of custody — evidence minting as Bitcoin Ordinals | Commercial API |
| **LNURL-auth** | Passwordless authentication via Lightning wallet (future) | Open protocol |

**Due diligence questions:**
- [ ] BTCPay Server deployment topology — same Docker network or separate?
- [ ] OrdinalsBot API pricing and reliability for evidence minting at scale
- [ ] LNURL-auth integration with Keycloak — is there a provider/plugin?

---

### Layer 10: Testing Stack

| Component | Role | Version | License |
|-----------|------|---------|---------|
| **pytest** | Test runner | 8.x | MIT |
| **requests** | HTTP client for E2E tests | 2.31+ | Apache-2.0 |
| **Playwright** | Browser automation | Latest | Apache-2.0 |
| **Chromium** | Browser engine for Playwright | Bundled | BSD |
| **Factory Boy** | Test fixtures (evaluate) | 3.x | MIT |
| **Faker** | Test data generation (evaluate) | Latest | MIT |

**Current test inventory (from dry run):**
- Unit tests: 177
- E2E API tests: 52
- Browser tests (Playwright): 47
- **Total: 276+ tests**

**Due diligence question:**
- [ ] Which tests survive the rehydration? Unit tests for Chirp rules = yes. Flask route tests = rewrite. Browser tests = rewrite for new UI.

---

### Layer 11: Infrastructure & DevOps

| Component | Role | Version | License |
|-----------|------|---------|---------|
| **Docker** | Containerization | Latest CE | Apache-2.0 |
| **Docker Compose** | Multi-container orchestration | v2.x | Apache-2.0 |
| **Portainer** | Container management UI (iMac QA box) | CE | Zlib |
| **GitHub Actions** | CI/CD pipeline | N/A | GitHub service |
| **Gunicorn** | WSGI server for Flask | 21.x | MIT |
| **Nginx** | Reverse proxy, TLS termination — **SELECTED (v1.1)** | Latest (`nginx:alpine`) | BSD-2-Clause |
| ~~**Traefik**~~ | ~~Alternative reverse proxy~~ — **EVALUATION CLOSED (v1.1). Nginx selected.** | — | MIT |

**Docker Compose topology (target):**
```yaml
services:
  postgres:        # PostgreSQL 17
  keycloak:        # Identity/auth
  hasura:          # GraphQL API
  directus:        # Admin UI
  superset:        # Analytics
  airflow:         # Orchestration (webserver + scheduler + worker)
  flask-api:       # Business logic service
  nginx:           # Reverse proxy + TLS (selected — v1.1)
  # Optional:
  btcpay:          # Bitcoin/Lightning (Goose)
  valkey:          # Cache/broker (BSD-3, replaces Redis — v1.1)
```

**Due diligence questions:**
- [x] ~~Nginx vs Traefik~~ **CLOSED (v1.1):** Nginx selected. Docker Compose uses `nginx:alpine`. Proven, documented, team has config patterns.
- [x] ~~Redis requirement~~ **CLOSED (v1.1):** Redis replaced with **Valkey 8** (BSD-3, Linux Foundation). Used by: Superset cache, Directus cache, Airflow CeleryExecutor (future). LocalExecutor selected for Alpha — Valkey not strictly required by Airflow in current config but available for Superset/Directus caching.
- [ ] Resource requirements — can the iMac (Intel, 2TB) run all 12 services simultaneously for QA? Docker Compose allocates ~8.8GB total memory limits.

---

## Part 3: Python Dependencies (Revised)

### Core Dependencies (requirements.txt — new stack)

```
# Web framework (thin business logic service)
Flask>=3.1.0

# Database
SQLAlchemy>=2.0.23
psycopg2-binary>=2.9.9      # PostgreSQL adapter
alembic>=1.13.0              # Schema migrations (if not using Hasura Migrations)

# Square SDK
squareup>=35.0.0,<42.0.0    # Pinned until v43 migration assessment complete

# HTTP
requests>=2.31.0

# Auth
PyJWT>=2.8.0                 # JWT validation (Keycloak tokens)
cryptography>=41.0.0         # For HMAC verification

# Environment
python-dotenv>=1.0.0

# Production server
gunicorn>=21.0.0

# Data (for Chirp rule evaluation)
pandas>=2.0.0

# Utilities
bcrypt>=4.0.0                # Legacy — migrate to Keycloak
openpyxl>=3.1.0              # Excel import/export
```

### Dev Dependencies (requirements-dev.txt — new stack)

```
# Testing
pytest>=8.0.0
pytest-cov>=4.1.0
playwright>=1.40.0
factory-boy>=3.3.0           # Test fixtures
faker>=20.0.0                # Test data generation

# Code quality
ruff>=0.1.0                  # Linting + formatting (replaces flake8 + black)
mypy>=1.7.0                  # Type checking

# Documentation
mkdocs>=1.5.0                # API documentation (evaluate)
```

---

## Part 4: License Audit

Every component's license must be compatible with our open-source positioning and Square Marketplace listing.

| Component | License | OSI Approved | Square-Compatible | Notes |
|-----------|---------|:---:|:---:|-------|
| PostgreSQL | PostgreSQL (BSD-like) | ✅ | ✅ | Fully permissive |
| Keycloak | Apache-2.0 | ✅ | ✅ | Red Hat backed |
| Hasura | Apache-2.0 | ✅ | ✅ | Core engine |
| Directus | BSL 1.1 | ❌ | ⚠️ | Free for self-hosted. **Syd to review.** |
| Superset | Apache-2.0 | ✅ | ✅ | Apache Foundation |
| Airflow | Apache-2.0 | ✅ | ✅ | Apache Foundation |
| Flask | BSD-3-Clause | ✅ | ✅ | Fully permissive |
| Square SDK | MIT | ✅ | ✅ | Official SDK |
| BTCPay Server | MIT | ✅ | ✅ | Self-hosted |
| pytest | MIT | ✅ | ✅ | Dev only |
| Playwright | Apache-2.0 | ✅ | ✅ | Dev only |
| Docker CE | Apache-2.0 | ✅ | ✅ | Infrastructure |
| Portainer CE | Zlib | ✅ | ✅ | Infrastructure |

**Flag:** Directus BSL 1.1 is the only non-OSI-approved license in the stack. Syd must confirm this doesn't create issues for Square Marketplace certification or our open-source positioning.

**Fallback if Directus BSL is problematic:** NocoDB (AGPLv3, ~50k stars) or AdminJS (MIT, ~8k stars) are alternatives. Both are fully open source.

---

## Part 5: Due Diligence Checklist — PhD/Tom/Jeremy

This is the formal audit that must be completed before coding resumes. PhD leads. Tom validates architecture. Jeremy validates implementation feasibility.

### Database Layer (Tom)
- [ ] PostgreSQL 17 vs 16 — any features we need from 17 specifically?
- [ ] Three-database architecture — separate Postgres instances or separate schemas in one instance?
- [ ] Connection pooling strategy (PgBouncer vs native)
- [ ] Backup and disaster recovery plan
- [ ] Read replica for analytics (Superset) queries
- [ ] Migration tool decision: Alembic vs Hasura Migrations vs raw SQL

### Auth Layer (PhD + Tom)
- [ ] Keycloak realm strategy: per-merchant vs per-tenant-group
- [ ] JWT claim structure for Hasura row-level permissions
- [ ] Keycloak + Hasura + Flask triple-handshake auth flow
- [ ] Session management: token refresh, logout propagation
- [ ] LNURL-auth feasibility with Keycloak (future)

### API Layer (Jeremy + Tom)
- [ ] Hasura v2 vs v3 evaluation
- [ ] Hasura event triggers vs Airflow for Chirp — design the boundary
- [ ] Remote schema design for Flask business logic
- [ ] GraphQL subscription architecture for real-time alerts
- [ ] Rate limiting and abuse prevention

### Admin Layer (PhD)
- [ ] Directus BSL 1.1 legal review (coordinate with Syd)
- [ ] Directus vs Hasura Console — do we need both? Role of each?
- [ ] Custom Directus extensions needed for Fox case management
- [ ] Merchant-facing vs internal-only scope decision

### Analytics Layer (Tom + Jeremy)
- [ ] Superset data source configuration for three-database architecture
- [ ] Embedded dashboard architecture for merchant portal
- [ ] Superset + Keycloak OIDC integration
- [ ] Dashboard template design for Owl module

### Orchestration Layer (Jeremy)
- [ ] Airflow executor selection (Local vs Celery)
- [ ] DAG design for Chirp detection pipeline
- [ ] Airflow resource requirements on iMac QA box
- [ ] Monitoring and alerting configuration

### Business Logic Layer (Jeremy + PhD)
- [ ] Flask vs FastAPI evaluation for thin service
- [ ] Chirp rule engine architecture in new stack
- [ ] Fox evidence chain enforcement in new stack
- [ ] Square webhook receiver design with Airflow integration

### Square Integration (Jeremy)
- [ ] SDK v35 → v43 migration assessment
- [ ] Square Marketplace certification compliance with Alpha 3X architecture
- [ ] Webhook delivery guarantees and dead letter queue design
- [ ] OAuth scope bundle for full CRDM coverage

### Infrastructure (Jeremy + Tom)
- [ ] Docker Compose for full Alpha 3X stack — resource requirements
- [ ] iMac QA box capacity for all services
- [ ] CI/CD pipeline redesign for multi-service architecture
- [ ] Reverse proxy selection (Nginx vs Traefik)
- [ ] Secret management strategy

### Testing (Jim — after stack decisions)
- [ ] Test survival audit: which of the 276+ tests carry forward?
- [ ] New test strategy for multi-service architecture
- [ ] The Rooster adaptation for Alpha 3X
- [ ] Integration test design for service-to-service communication

---

## Part 6: Sign-Off

| Reviewer | Role | Status | Date |
|----------|------|--------|------|
| **Jeffe** | CEO/Founder | ⬜ PENDING | |
| **PhD** | Due Diligence Lead | ⬜ PENDING | |
| **Tom** | Systems Architect | ⬜ PENDING | |
| **Jeremy** | Developer Quant | ⬜ PENDING | |
| **Syd** | Legal (license review) | ⬜ PENDING | |
| **Eva** | Program Manager | ⬜ PENDING | |

**Rule:** No coding resumes until at least PhD + Tom + Jeremy have signed off. Jeffe gives final approval.

---

## Part 7: Open Questions (Parking Lot)

These need answers but are not blocking the due diligence exercise:

1. **Merchant portal frontend framework** — React? Next.js? Server-rendered? Or is Directus + embedded Superset sufficient for V1?
2. **Mobile app** — native or PWA? Not MVP, but architecture should not preclude it.
3. **Multi-POS abstraction** — the canonical parser interface design. Tom to spec before any Clover work.
4. **Data lake / warehouse** — do we need a separate analytical store, or does `canary_metrics` + Superset cover it?
5. **Observability** — Prometheus + Grafana? Or is Airflow + Portainer + Superset enough monitoring for V1?
6. **Cache layer** — Valkey (Redis replacement) for anything besides Airflow/Superset/Directus caching? API response caching? Session store? *(v1.1: Redis→Valkey swap complete)*

---

*This document follows the Factory Process Blueprint stage. It is the ingredients list. The team reviews it, the due diligence exercise validates it, and then — and only then — we start cooking again.*

*"Do it right, do it once." — Jeffe*

---

*v1.1 Corrections applied February 22, 2026 by Eva. 8 version/decision corrections. Full audit trail: `Markdown/Specs/Canary_Technology_Blueprint_v1.1_Corrections.md`.*
