---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Technical Requirements

**Version:** 1.0
**Date:** February 21, 2026
**Author:** Eva (Program Manager)
**Directive:** Jeffe — "Rescript our whole thought process into a set of functional and technical requirements from pure .md files — new stack, new DB designs, defined SDKs, defined APIs/endpoints, no scope creep."
**Classification:** Internal — **BLUEPRINT STAGE DOCUMENT**
**Status:** DRAFT — Part of Alpha 3X rehydration. Defines HOW the stack implements each functional requirement.
**Companion:** `Canary_Functional_Requirements_v1.0.md` (defines WHAT)
**Stack Reference:** `Canary_Technology_Blueprint_v1.0.md` (ingredients list)

---

> *"I just want to make sure we start from the top and agree our tech stack, SDKs, licenses, DBs, flavor, etc., as ingredients before we start to cook again."* — Jeffe

---

## Purpose

This document maps every Functional Requirement (FR-1 through FR-11) to specific Alpha 3X stack components, database schemas, APIs, SDKs, and service boundaries. Where the Functional Requirements say WHAT Canary must do, this document says HOW.

The Implementation Notes in each section are guidance for the due diligence team and for Jeremy when coding resumes. They are not final designs — they are starting points that PhD, Tom, and Jeremy will validate or revise during the due diligence exercise.

---

## Service Boundary Map

Before mapping individual FRs, the team must understand which service owns what. This is the fundamental architectural split of Alpha 3X.

| Service | Owns | Does NOT Own |
|---------|------|-------------|
| **PostgreSQL** | All data storage, RLS enforcement, triggers (INSERT-only), hash chain functions, partitioning | Business logic, API routing, authentication |
| **Keycloak** | User identity, authentication, JWT issuance, realm management, SSO, MFA | Data access decisions, business rules |
| **Hasura** | GraphQL API generation, row-level permissions (JWT claims), real-time subscriptions, event triggers | Chirp rule logic, HMAC verification, evidence chain enforcement |
| **Flask** | Chirp rule evaluation, Square webhook processing, HMAC verification, Fox evidence chain, Square OAuth, Ordinal minting | CRUD API, user auth, admin UI, dashboards, scheduling |
| **Directus** | Admin data browsing, custom actions UI, internal operations | Chirp logic, analytics, auth |
| **Superset** | Dashboards, SQL exploration, scheduled reports, embedded analytics | Data writes, authentication, business logic |
| **Airflow** | Job scheduling, DAG orchestration, retry logic, monitoring | Data storage, API serving, UI |

---

## TR-1: Data Ingestion (implements FR-1)

### TR-1.1: Real-Time POS Data Capture (FR-1.1)

**Primary Service:** Flask (webhook receiver) → PostgreSQL (storage)
**Supporting Services:** Hasura (event triggers for downstream processing), Airflow (dead letter replay)

**Implementation:**

| Component | Responsibility |
|-----------|---------------|
| Flask | Receives Square webhooks at `/webhooks/square`. Validates HMAC-SHA256 signature using `cryptography` library. Extracts idempotency key. Stores raw payload. |
| PostgreSQL | `canary_sales.webhook_log` table stores raw JSONB payload + metadata. Idempotency enforced via UNIQUE constraint on `(provider, idempotency_key)`. |
| Hasura Event Trigger | On INSERT to `webhook_log`, triggers Flask endpoint for payload parsing and field extraction into canonical CRDM tables. |
| Airflow | DAG `dead_letter_replay` processes failed ingestion attempts on a 15-minute schedule with exponential backoff. |

**Database Schema:**
```sql
-- canary_sales.webhook_log
CREATE TABLE canary_sales.webhook_log (
    id              BIGSERIAL PRIMARY KEY,
    provider        VARCHAR(50) NOT NULL DEFAULT 'square',
    event_type      VARCHAR(100) NOT NULL,
    idempotency_key VARCHAR(255) NOT NULL,
    raw_payload     JSONB NOT NULL,
    hmac_valid      BOOLEAN NOT NULL,
    processed       BOOLEAN NOT NULL DEFAULT FALSE,
    error_message   TEXT,
    received_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    processed_at    TIMESTAMPTZ,
    UNIQUE (provider, idempotency_key)
);
```

**API Endpoints (Flask):**
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/webhooks/square` | HMAC-SHA256 | Receive Square webhooks |
| POST | `/webhooks/square/replay` | Keycloak JWT (admin) | Replay dead letter items |

**SDK:** `squareup>=35.0.0` for webhook signature verification, `cryptography>=41.0.0` for HMAC.

**AC Mapping:**
- FR-1.1.1 → Flask HMAC validation + PostgreSQL INSERT latency < 5s
- FR-1.1.2 → PostgreSQL UNIQUE constraint on idempotency_key
- FR-1.1.3 → `processed=FALSE` + `error_message IS NOT NULL` = dead letter queue; Airflow replays
- FR-1.1.4 → `raw_payload JSONB` column preserves full webhook

---

### TR-1.2: Seven Canonical Data Sources (FR-1.2)

**Primary Service:** Flask (parser layer) → PostgreSQL (CRDM tables)

**Implementation:** Each CRDM canonical source maps to one or more PostgreSQL tables. The Square parser (`canary/parsers/square_parser.py`) translates Square-native JSON into canonical table INSERTs.

**Source-to-Table Mapping:**

| CRDM Source | PostgreSQL Table(s) | Square API | Parser Method |
|-------------|---------------------|-----------|---------------|
| #1 Transaction Header | `canary_sales.transactions` | Payments API | `parse_payment_to_transaction()` |
| #2 Tender | `canary_sales.transaction_tenders` | Payments API (tenders array) | `parse_tenders()` |
| #3 Line Items | `canary_sales.transaction_line_items` | Orders API | `parse_order_line_items()` |
| #4 Employee | `canary_app.employees`, `canary_sales.employee_timecards` | Team API, Labor API | `parse_employee()`, `parse_timecard()` |
| #5 Product/Article | `canary_app.products` | Catalog API | `parse_catalog_item()` |
| #6 Store/Location | `canary_app.locations` | Locations API | `parse_location()` |
| #7 Customer | `canary_app.customers` | Customers API | `parse_customer()` |

**Parser Interface (Python):**
```python
class POSParser(ABC):
    """Abstract base for all POS vendor parsers."""

    @abstractmethod
    def parse_payment_to_transaction(self, raw: dict) -> dict: ...

    @abstractmethod
    def parse_tenders(self, raw: dict) -> list[dict]: ...

    @abstractmethod
    def parse_order_line_items(self, raw: dict) -> list[dict]: ...

    @abstractmethod
    def parse_employee(self, raw: dict) -> dict: ...

    @abstractmethod
    def parse_timecard(self, raw: dict) -> dict: ...

    @abstractmethod
    def parse_catalog_item(self, raw: dict) -> dict: ...

    @abstractmethod
    def parse_location(self, raw: dict) -> dict: ...

    @abstractmethod
    def parse_customer(self, raw: dict) -> dict: ...

    @abstractmethod
    def coverage_matrix(self) -> dict[str, list[str]]:
        """Return which CRDM fields this parser populates."""
        ...
```

**AC Mapping:**
- FR-1.2.1 → Source-to-table mapping above
- FR-1.2.2 → `SquareParser(POSParser)` class implements abstract interface
- FR-1.2.3 → Chirp rules query canonical tables only, never parser-specific tables

---

### TR-1.3: POS-Agnostic Parser Architecture (FR-1.3)

**Primary Service:** Flask (parser registry)

**Implementation:** Parser registry pattern. Flask maintains a `PARSER_REGISTRY` dictionary mapping provider name to parser class. New POS integrations register a parser; Chirp rules are unmodified.

```python
PARSER_REGISTRY: dict[str, type[POSParser]] = {
    "square": SquareParser,
    # Future: "clover": CloverParser,
    # Future: "toast": ToastParser,
}
```

**AC Mapping:**
- FR-1.3.1 → `SquareParser` class with full API endpoint mapping
- FR-1.3.2 → `POSParser` ABC defines interface; new parsers implement same methods
- FR-1.3.3 → Each parser's `coverage_matrix()` method returns populated vs. empty CRDM fields

---

### TR-1.4: Canary-Native Data Sources (FR-1.4)

**Primary Service:** Flask (Square API polling + webhook handlers) → PostgreSQL (dedicated tables)

**Implementation:** These sources extend beyond the enterprise ancestor spec. Square provides them via dedicated APIs. Flask handles ingestion; Airflow schedules periodic syncs for non-webhook sources.

| Source | PostgreSQL Table | Square API | Ingestion Method |
|--------|-----------------|-----------|-----------------|
| Cash Drawer Events | `canary_sales.cash_drawer_shifts`, `canary_sales.cash_drawer_events` | Cash Drawers API | Airflow DAG (hourly poll) |
| Inventory Adjustments | `canary_sales.inventory_adjustments` | Inventory API | Webhook + Airflow reconciliation |
| Gift Card Activities | `canary_sales.gift_card_activities` | Gift Cards API | Airflow DAG (hourly poll) |
| Employee Timecards | `canary_sales.employee_timecards` | Labor API | Airflow DAG (shift-boundary poll) |

**Database Schema (Cash Drawer — example):**
```sql
-- canary_sales.cash_drawer_shifts
CREATE TABLE canary_sales.cash_drawer_shifts (
    id                  BIGSERIAL PRIMARY KEY,
    merchant_id         UUID NOT NULL REFERENCES canary_app.merchants(id),
    location_id         UUID NOT NULL REFERENCES canary_app.locations(id),
    square_shift_id     VARCHAR(255) NOT NULL,
    employee_id         UUID REFERENCES canary_app.employees(id),
    opened_at           TIMESTAMPTZ NOT NULL,
    closed_at           TIMESTAMPTZ,
    opened_cash_money   BIGINT,       -- cents
    expected_cash_money BIGINT,
    closed_cash_money   BIGINT,
    cash_variance       BIGINT,       -- computed: closed - expected
    device_name         VARCHAR(255),
    raw_payload         JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- canary_sales.cash_drawer_events
CREATE TABLE canary_sales.cash_drawer_events (
    id                  BIGSERIAL PRIMARY KEY,
    shift_id            BIGINT NOT NULL REFERENCES canary_sales.cash_drawer_shifts(id),
    merchant_id         UUID NOT NULL,
    event_type          VARCHAR(50) NOT NULL,  -- NO_SALE, PAID_IN, PAID_OUT
    employee_id         UUID REFERENCES canary_app.employees(id),
    event_money         BIGINT,       -- cents
    description         TEXT,
    event_at            TIMESTAMPTZ NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Airflow DAGs:**
```
DAG: canary_cash_drawer_sync (hourly)
├── Task: fetch_open_shifts (Square Cash Drawers API)
├── Task: fetch_shift_events (per shift)
├── Task: upsert_to_postgres
└── Task: trigger_chirp_evaluation (HTTP → Flask)

DAG: canary_timecard_sync (every 4 hours)
├── Task: fetch_timecards (Square Labor API)
├── Task: upsert_to_postgres
└── Task: trigger_cross_reference (timecard × transactions)

DAG: canary_gift_card_sync (hourly)
├── Task: fetch_gift_card_activity (Square Gift Cards API)
├── Task: upsert_to_postgres
└── Task: trigger_velocity_check
```

**SDK:** `squareup` — Cash Drawers, Labor, Gift Cards, Inventory API clients. OAuth scopes: `CASH_DRAWER_READ`, `TIMECARDS_READ`, `INVENTORY_READ`, `GIFTCARDS_READ`.

---

## TR-2: Fraud Detection / Chirp (implements FR-2)

### TR-2.1: Rule-Based Detection Engine (FR-2.1)

**Primary Service:** Flask (`canary/chirp.py`) — triggered by Hasura event triggers (real-time) and Airflow DAGs (scheduled)

**Implementation:** Chirp rules are Python functions that query PostgreSQL via SQLAlchemy. Each rule is registered in `canary_app.detection_rules` with configurable thresholds. Rules produce alert records in `canary_sales.alerts`.

**Rule Execution Architecture:**
```
[Real-time path]
  Hasura event trigger (new transaction INSERT)
    → POST Flask /chirp/evaluate
      → Chirp engine loads active rules
        → Each rule queries PostgreSQL for pattern match
          → Matching rules → INSERT into canary_sales.alerts
            → Hasura subscription pushes to connected clients

[Scheduled path]
  Airflow DAG chirp_detection_sweep (hourly)
    → Python operator calls Chirp engine
      → Full sweep of all rules across all merchants
        → Batch INSERT alerts
```

**Rule Configuration Table:**
```sql
-- canary_app.detection_rules
CREATE TABLE canary_app.detection_rules (
    id              SERIAL PRIMARY KEY,
    rule_id         VARCHAR(10) NOT NULL UNIQUE,  -- C-001, C-101, etc.
    rule_name       VARCHAR(100) NOT NULL,
    category        VARCHAR(50) NOT NULL,
    description     TEXT,
    default_threshold JSONB NOT NULL,
    severity        VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    data_sources    TEXT[] NOT NULL,               -- CRDM sources required
    enabled         BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- canary_app.merchant_rule_config (per-merchant overrides)
CREATE TABLE canary_app.merchant_rule_config (
    id              SERIAL PRIMARY KEY,
    merchant_id     UUID NOT NULL REFERENCES canary_app.merchants(id),
    rule_id         VARCHAR(10) NOT NULL REFERENCES canary_app.detection_rules(rule_id),
    threshold       JSONB NOT NULL,
    enabled         BOOLEAN NOT NULL DEFAULT TRUE,
    updated_by      UUID NOT NULL,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (merchant_id, rule_id)
);
```

**Alert Table:**
```sql
-- canary_sales.alerts (append-only)
CREATE TABLE canary_sales.alerts (
    id              BIGSERIAL PRIMARY KEY,
    merchant_id     UUID NOT NULL,
    location_id     UUID,
    rule_id         VARCHAR(10) NOT NULL,
    severity        VARCHAR(20) NOT NULL,
    status          VARCHAR(30) NOT NULL DEFAULT 'NEW',
    employee_id     UUID,
    evidence        JSONB NOT NULL,       -- records that triggered this alert
    summary         TEXT NOT NULL,
    detected_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- Immutability: no UPDATE/DELETE trigger on this table
    CONSTRAINT alerts_append_only CHECK (TRUE)  -- trigger-enforced
);

-- canary_sales.alert_history (status changes)
CREATE TABLE canary_sales.alert_history (
    id              BIGSERIAL PRIMARY KEY,
    alert_id        BIGINT NOT NULL REFERENCES canary_sales.alerts(id),
    previous_status VARCHAR(30),
    new_status      VARCHAR(30) NOT NULL,
    changed_by      UUID NOT NULL,
    changed_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes           TEXT
);
```

**API Endpoints (Flask):**
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/chirp/evaluate` | Hasura event secret | Evaluate rules for new data |
| POST | `/chirp/sweep` | Airflow service token | Full sweep (scheduled) |

**Hasura Configuration:**
- `canary_sales.alerts` exposed as GraphQL type with row-level permissions (merchant_id = JWT claim)
- Real-time subscription on `alerts` table for live dashboard feeds
- `alert_history` exposed for audit trail queries

**AC Mapping:**
- FR-2.1.1 → All 22 rules registered in `detection_rules` table, each with Python evaluation function
- FR-2.1.2 → `merchant_rule_config` table overrides defaults per merchant
- FR-2.1.3 → Hasura event triggers (real-time) + Airflow DAGs (scheduled)
- FR-2.1.4 → Alert record structure includes all required fields

---

### TR-2.2: Multi-Source Detection (FR-2.2)

**Primary Service:** Flask (Chirp rule engine) — SQLAlchemy cross-table JOINs

**Implementation:** Multi-source rules use SQLAlchemy queries that JOIN across canonical tables. Each rule declares its required `data_sources` (stored in `detection_rules.data_sources`). The engine validates source availability before evaluation.

**Example: OFF_CLOCK_TRANSACTION (C-501):**
```python
def evaluate_off_clock_transaction(merchant_id: UUID, window_hours: int = 24) -> list[Alert]:
    """Detect transactions processed by employees outside their clocked shift."""
    query = (
        select(Transaction, EmployeeTimecard)
        .join(EmployeeTimecard, Transaction.employee_id == EmployeeTimecard.employee_id)
        .where(
            Transaction.merchant_id == merchant_id,
            Transaction.transaction_at >= now() - timedelta(hours=window_hours),
            or_(
                Transaction.transaction_at < EmployeeTimecard.clock_in,
                Transaction.transaction_at > EmployeeTimecard.clock_out
            )
        )
    )
    # ... generate alerts for matches
```

**AC Mapping:**
- FR-2.2.1 → SQLAlchemy JOINs across any combination of CRDM + Canary-native tables
- FR-2.2.2 → `evidence JSONB` in alert record contains full record IDs from all contributing tables

---

### TR-2.3: Alert Lifecycle (FR-2.3)

**Primary Service:** Hasura (GraphQL mutations for status changes) + PostgreSQL (append-only enforcement)

**Implementation:** Status changes go through Hasura GraphQL mutations which INSERT into `alert_history` and UPDATE `alerts.status`. The `alerts` table itself uses a trigger that allows UPDATE only on the `status` column — all other columns are immutable after INSERT.

**Hasura Mutation:**
```graphql
mutation UpdateAlertStatus($alertId: bigint!, $newStatus: String!, $notes: String) {
  insert_alert_history_one(object: {
    alert_id: $alertId,
    new_status: $newStatus,
    notes: $notes
  }) {
    id
  }
  update_alerts_by_pk(pk_columns: {id: $alertId}, _set: {status: $newStatus}) {
    id
    status
  }
}
```

**Notification Integration:** Hasura event trigger on `alerts` INSERT → Flask notification service → email/webhook per merchant preference.

**AC Mapping:**
- FR-2.3.1 → PostgreSQL trigger prevents UPDATE on non-status columns
- FR-2.3.2 → `alert_history` table with `changed_by` from JWT claim
- FR-2.3.3 → Hasura event trigger → Flask notification endpoint → merchant channels

---

## TR-3: Case Management / Fox (implements FR-3)

### TR-3.1: Case Creation and Tracking (FR-3.1)

**Primary Service:** Flask (case business logic) + Hasura (CRUD API) + Directus (admin UI)

**Implementation:** Fox case management uses Flask for business logic (case creation rules, evidence linking, status validation) and Hasura for the GraphQL API. Directus provides the admin interface for internal investigators. Merchant-facing case views go through Hasura with row-level permissions.

**Database Schema:**
```sql
-- canary_app.fox_cases
CREATE TABLE canary_app.fox_cases (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID NOT NULL REFERENCES canary_app.merchants(id),
    case_number     VARCHAR(20) NOT NULL UNIQUE,  -- auto-generated: FOX-YYYY-NNNN
    status          VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    priority        VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    case_type       VARCHAR(50) NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    assigned_to     UUID REFERENCES canary_app.users(id),
    created_by      UUID NOT NULL REFERENCES canary_app.users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at       TIMESTAMPTZ,
    resolution      VARCHAR(50),
    resolution_notes TEXT
);

-- canary_app.fox_case_alerts (link alerts to cases)
CREATE TABLE canary_app.fox_case_alerts (
    case_id         UUID NOT NULL REFERENCES canary_app.fox_cases(id),
    alert_id        BIGINT NOT NULL REFERENCES canary_sales.alerts(id),
    linked_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    linked_by       UUID NOT NULL,
    PRIMARY KEY (case_id, alert_id)
);

-- canary_app.fox_subjects (persons of interest)
CREATE TABLE canary_app.fox_subjects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id         UUID NOT NULL REFERENCES canary_app.fox_cases(id),
    employee_id     UUID REFERENCES canary_app.employees(id),
    customer_id     UUID REFERENCES canary_app.customers(id),
    subject_type    VARCHAR(30) NOT NULL,  -- EMPLOYEE, CUSTOMER, EXTERNAL
    role_in_case    VARCHAR(50),
    added_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    added_by        UUID NOT NULL
);
```

**API Endpoints (Flask — business logic):**
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/fox/cases` | Keycloak JWT | Create case (validates alert linkage) |
| POST | `/fox/cases/{id}/escalate` | Keycloak JWT | Escalate to law enforcement |
| POST | `/fox/cases/{id}/export` | Keycloak JWT | Export case packet |

**Hasura:** `fox_cases`, `fox_case_alerts`, `fox_subjects` exposed as GraphQL types with merchant_id row-level permissions.

**Directus:** Custom actions: "Create Case from Alert", "Assign Investigator", "Export Case Packet".

---

### TR-3.2: Evidence Chain of Custody (FR-3.2)

**Primary Service:** Flask (evidence chain enforcement) + PostgreSQL (INSERT-only triggers)

**Implementation:** Evidence tables are INSERT-only, enforced at the database level via triggers. Flask handles the business logic of evidence attachment and hash chain generation. No other service may write to evidence tables.

**Database Schema:**
```sql
-- canary_app.fox_evidence (INSERT-only — trigger enforced)
CREATE TABLE canary_app.fox_evidence (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id         UUID NOT NULL REFERENCES canary_app.fox_cases(id),
    evidence_type   VARCHAR(50) NOT NULL,  -- TRANSACTION, PHOTO, DOCUMENT, VIDEO, SCREENSHOT
    description     TEXT NOT NULL,
    content_hash    VARCHAR(64) NOT NULL,  -- SHA-256 of evidence content
    chain_hash      VARCHAR(64) NOT NULL,  -- SHA-256(content_hash + previous chain_hash)
    storage_ref     TEXT NOT NULL,          -- file path or reference
    metadata        JSONB,
    collected_by    UUID NOT NULL,
    collected_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger: prevent UPDATE and DELETE
CREATE OR REPLACE FUNCTION prevent_evidence_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Evidence records are immutable. INSERT only.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER evidence_immutable_update
    BEFORE UPDATE ON canary_app.fox_evidence
    FOR EACH ROW EXECUTE FUNCTION prevent_evidence_mutation();

CREATE TRIGGER evidence_immutable_delete
    BEFORE DELETE ON canary_app.fox_evidence
    FOR EACH ROW EXECUTE FUNCTION prevent_evidence_mutation();

-- canary_app.fox_evidence_access_log (INSERT-only)
CREATE TABLE canary_app.fox_evidence_access_log (
    id              BIGSERIAL PRIMARY KEY,
    evidence_id     UUID NOT NULL REFERENCES canary_app.fox_evidence(id),
    accessed_by     UUID NOT NULL,
    access_type     VARCHAR(30) NOT NULL,  -- VIEW, DOWNLOAD, EXPORT
    accessed_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ip_address      INET
);
```

**Flask Endpoints:**
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/fox/evidence` | Keycloak JWT | Attach evidence (computes hash chain) |
| GET | `/fox/evidence/{id}` | Keycloak JWT | View evidence (logs access) |
| POST | `/fox/evidence/verify-chain/{case_id}` | Keycloak JWT | Verify hash chain integrity |

**AC Mapping:**
- FR-3.2.1 → PostgreSQL triggers prevent UPDATE/DELETE on `fox_evidence`
- FR-3.2.2 → `fox_evidence_access_log` INSERT on every evidence retrieval
- FR-3.2.3 → `chain_hash` column; Flask `verify-chain` endpoint validates
- FR-3.2.4 → Flask `/fox/cases/{id}/export` generates evidence packet with chain metadata

---

### TR-3.3: Case Timeline (FR-3.3)

**Primary Service:** PostgreSQL (INSERT-only table) + Hasura (read API)

**Database Schema:**
```sql
-- canary_app.fox_case_timeline (INSERT-only)
CREATE TABLE canary_app.fox_case_timeline (
    id              BIGSERIAL PRIMARY KEY,
    case_id         UUID NOT NULL REFERENCES canary_app.fox_cases(id),
    action_type     VARCHAR(50) NOT NULL,
    actor_id        UUID NOT NULL,
    details         JSONB NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- INSERT-only triggers (same pattern as evidence)
CREATE TRIGGER timeline_immutable_update
    BEFORE UPDATE ON canary_app.fox_case_timeline
    FOR EACH ROW EXECUTE FUNCTION prevent_evidence_mutation();

CREATE TRIGGER timeline_immutable_delete
    BEFORE DELETE ON canary_app.fox_case_timeline
    FOR EACH ROW EXECUTE FUNCTION prevent_evidence_mutation();
```

**Hasura:** Exposed as GraphQL type with subscription for live timeline updates.

---

## TR-4: Multi-Tenant Architecture (implements FR-4)

### TR-4.1: Merchant Data Isolation (FR-4.1)

**Defense-in-depth — three layers:**

| Layer | Technology | Enforcement |
|-------|-----------|-------------|
| **Database** | PostgreSQL RLS | Every table with `merchant_id` has an RLS policy: `USING (merchant_id = current_setting('app.current_merchant_id')::uuid)` |
| **API** | Hasura row-level permissions | JWT claim `x-hasura-merchant-id` filters every query automatically |
| **Auth** | Keycloak realms | Merchant users belong to a realm; JWT tokens carry merchant_id claim |

**PostgreSQL RLS Example:**
```sql
ALTER TABLE canary_sales.transactions ENABLE ROW LEVEL SECURITY;

CREATE POLICY merchant_isolation ON canary_sales.transactions
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

**Hasura Permission Rule:**
```json
{
  "table": "transactions",
  "role": "merchant_user",
  "permission": {
    "filter": {
      "merchant_id": { "_eq": "X-Hasura-Merchant-Id" }
    }
  }
}
```

**AC Mapping:**
- FR-4.1.1 → PostgreSQL RLS policies on all tables with `merchant_id`
- FR-4.1.2 → Even if Hasura permissions are misconfigured, PostgreSQL RLS blocks cross-tenant access
- FR-4.1.3 → Penetration test scope documented in E2 PRD

---

### TR-4.2: Role-Based Access Control (FR-4.2)

**Primary Service:** Keycloak (role management) → Hasura (permission enforcement)

**Implementation:** Keycloak manages role assignment within each merchant realm. Roles are embedded in the JWT token as claims. Hasura reads these claims to apply column-level and row-level permissions.

**Role-Permission Matrix (Hasura):**

| Role | Alerts | Cases | Transactions | Employees | Config |
|------|--------|-------|-------------|-----------|--------|
| merchant_owner | Read/Write | Read/Write | Read | Read | Read/Write |
| store_manager | Read | Read/Create | Read (own location) | Read (own location) | Read |
| associate | Read (own) | — | — | — | — |
| analyst | Read | Read | Read | Read | Read |
| viewer | Read | Read | — | — | — |

---

### TR-4.3: Organizational Hierarchy (FR-4.3)

**Primary Service:** PostgreSQL (hierarchy tables) + Hasura (nested queries)

**Database Schema:**
```sql
-- canary_app.location_hierarchy
CREATE TABLE canary_app.location_hierarchy (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID NOT NULL REFERENCES canary_app.merchants(id),
    location_id     UUID NOT NULL REFERENCES canary_app.locations(id),
    parent_id       UUID REFERENCES canary_app.location_hierarchy(id),
    level_type      VARCHAR(30) NOT NULL,  -- REGION, DISTRICT, MARKET, STORE
    level_name      VARCHAR(100) NOT NULL,
    UNIQUE (merchant_id, location_id)
);
```

**Hasura:** Recursive relationship queries for hierarchy traversal. Row-level permissions support scoping by hierarchy level via JWT claims.

---

## TR-5: Analytics & Reporting / Owl (implements FR-5)

### TR-5.1: Dashboard Metrics (FR-5.1)

**Primary Service:** Apache Superset (dashboards) + PostgreSQL `canary_metrics` database

**Implementation:** The `canary_metrics` database stores pre-aggregated metrics computed by Airflow ETL DAGs. Superset connects to `canary_metrics` as a datasource and renders dashboards.

**Metric Tables (canary_metrics):**
```sql
-- Star schema: fact tables
CREATE TABLE canary_metrics.fact_daily_location (
    date_key        DATE NOT NULL,
    merchant_id     UUID NOT NULL,
    location_id     UUID NOT NULL,
    transaction_count   INTEGER,
    refund_count        INTEGER,
    void_count          INTEGER,
    refund_rate         NUMERIC(5,4),
    void_rate           NUMERIC(5,4),
    cash_variance_total BIGINT,
    no_sale_count       INTEGER,
    alert_count         INTEGER,
    PRIMARY KEY (date_key, merchant_id, location_id)
);

CREATE TABLE canary_metrics.fact_daily_employee (
    date_key        DATE NOT NULL,
    merchant_id     UUID NOT NULL,
    employee_id     UUID NOT NULL,
    refunds_issued      INTEGER,
    voids_processed     INTEGER,
    discount_total      BIGINT,
    discount_rate       NUMERIC(5,4),
    off_clock_flags     INTEGER,
    risk_score          NUMERIC(5,2),
    PRIMARY KEY (date_key, merchant_id, employee_id)
);
```

**Airflow DAG:**
```
DAG: canary_metrics_etl (daily at 02:00 UTC)
├── Task: aggregate_location_metrics (SQL → canary_metrics.fact_daily_location)
├── Task: aggregate_employee_metrics (SQL → canary_metrics.fact_daily_employee)
├── Task: aggregate_product_metrics (SQL → canary_metrics.fact_daily_product)
├── Task: compute_risk_scores (Python → ML model scoring)
└── Task: refresh_superset_cache (HTTP → Superset warm-cache API)
```

**Superset Dashboards (Owl):**
- Total Retail Loss — merchant-level aggregate, trend, category breakdown
- Location Scorecard — per-location KPIs with drill-down
- Employee Risk — risk score trends, alert history, timecard anomalies
- Chirp Alert Trends — detection volume by rule, severity distribution

**Superset Row-Level Security:** Configured via Keycloak OIDC integration — Superset reads `merchant_id` from JWT and applies dataset filters.

**AC Mapping:**
- FR-5.1.1 → Pre-aggregated `canary_metrics` fact tables
- FR-5.1.2 → Superset drill-down via dashboard filters + linked charts
- FR-5.1.3 → Superset RLS enforces merchant isolation

---

### TR-5.2: Data Exploration (FR-5.2)

**Primary Service:** Apache Superset SQL Lab

**Implementation:** Superset SQL Lab connects to `canary_metrics` (read-only database user). Superset roles mapped from Keycloak restrict which merchants/datasets the user can query.

**AC Mapping:**
- FR-5.2.1 → Superset SQL Lab with read-only PostgreSQL connection
- FR-5.2.2 → Superset RLS + PostgreSQL read-only user with RLS policies
- FR-5.2.3 → Separate `canary_metrics` database; queries don't touch `canary_sales` transactional tables

---

### TR-5.3: Scheduled Reports (FR-5.3)

**Primary Service:** Airflow (schedule) + Superset (report generation) + Flask (email delivery)

**Implementation:** Airflow DAG triggers Superset's report API to generate PDF/CSV. Flask sends via email or stores for in-app notification.

**AC Mapping:**
- FR-5.3.1 → Airflow DAG `canary_scheduled_reports` with per-merchant configuration
- FR-5.3.2 → Flask email service or Hasura notification table for in-app
- FR-5.3.3 → Superset report template includes all required metrics

---

## TR-6: Square Marketplace Compliance (implements FR-6)

### TR-6.1: OAuth 2.0 Integration (FR-6.1)

**Primary Service:** Flask (OAuth flow handler)

**Implementation:** Flask handles the Square OAuth authorization code flow. Tokens are encrypted at rest in PostgreSQL. A background Airflow task handles token refresh before expiration.

**Database Schema:**
```sql
-- canary_app.square_oauth_tokens (encrypted)
CREATE TABLE canary_app.square_oauth_tokens (
    merchant_id         UUID PRIMARY KEY REFERENCES canary_app.merchants(id),
    access_token_enc    BYTEA NOT NULL,       -- AES-256 encrypted
    refresh_token_enc   BYTEA NOT NULL,       -- AES-256 encrypted
    token_type          VARCHAR(50) NOT NULL,
    expires_at          TIMESTAMPTZ NOT NULL,
    scopes              TEXT[] NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    refreshed_at        TIMESTAMPTZ
);
```

**Flask Endpoints:**
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/square/oauth/authorize` | None (redirect) | Initiate OAuth flow with PKCE |
| GET | `/square/oauth/callback` | Square callback | Exchange code for tokens |
| POST | `/square/oauth/revoke` | Keycloak JWT (admin) | Revoke merchant tokens (uninstall) |

**Airflow DAG:**
```
DAG: canary_token_refresh (every 6 hours)
├── Task: check_expiring_tokens (query tokens expiring within 12 hours)
└── Task: refresh_tokens (Square OAuth refresh endpoint)
```

**SDK:** `squareup` OAuth client for token exchange and refresh.

---

### TR-6.2: Webhook Processing (FR-6.2)

**Primary Service:** Flask (see TR-1.1)

Already covered in TR-1.1. HMAC-SHA256 verification, idempotency, and 200 OK within Square timeout.

---

### TR-6.3: Data Security (FR-6.3)

**Implementation Across Stack:**

| Requirement | Technology |
|-------------|-----------|
| Encryption at rest | PostgreSQL `pgcrypto` for token encryption; disk-level encryption for volumes |
| TLS 1.2+ | Nginx/Traefik terminates TLS; all inter-service communication on Docker internal network |
| Token security | AES-256 encryption in `square_oauth_tokens`; never logged in plaintext; Flask logging sanitizer strips tokens |
| Audit trail | Hasura + PostgreSQL audit triggers log all data access |

---

### TR-6.4: Merchant Experience (FR-6.4)

**Implementation:**
- FR-6.4.1 → Square Marketplace listing → OAuth flow → auto-provisioning (Flask creates merchant, Keycloak realm, default Chirp rules)
- FR-6.4.2 → After OAuth, Flask triggers initial data pull via Square APIs (Airflow `initial_merchant_sync` DAG)
- FR-6.4.3 → Uninstall webhook → Flask revokes tokens, soft-deletes merchant data per retention policy

---

## TR-7: Data Integrity & Audit (implements FR-7)

### TR-7.1: Financial Ledger Immutability (FR-7.1)

**Primary Service:** PostgreSQL (triggers)

**Implementation:** All tables in `canary_sales` that store financial transaction data have triggers preventing UPDATE and DELETE.

**Applicable Tables:** `transactions`, `transaction_tenders`, `transaction_line_items`, `refund_links`, `alerts`

**Trigger Pattern:**
```sql
CREATE OR REPLACE FUNCTION prevent_financial_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Financial records are immutable. Corrections must use adjustment records.';
END;
$$ LANGUAGE plpgsql;

-- Applied to each financial table
CREATE TRIGGER transactions_immutable
    BEFORE UPDATE OR DELETE ON canary_sales.transactions
    FOR EACH ROW EXECUTE FUNCTION prevent_financial_mutation();
```

**Correction Pattern:** Adjustment records reference the original transaction but contain corrected values. Original is never modified.

---

### TR-7.2: Hash-Chain Audit Trail (FR-7.2)

**Primary Service:** PostgreSQL (`pgcrypto`) + Flask (chain validation)

**Database Schema:**
```sql
-- canary_app.audit_log
CREATE TABLE canary_app.audit_log (
    id              BIGSERIAL PRIMARY KEY,
    table_name      VARCHAR(100) NOT NULL,
    record_id       VARCHAR(255) NOT NULL,
    action          VARCHAR(20) NOT NULL,  -- INSERT, UPDATE, DELETE, ACCESS
    actor_id        UUID,
    actor_type      VARCHAR(30),           -- USER, SYSTEM, WEBHOOK
    details         JSONB,
    entry_hash      VARCHAR(64) NOT NULL,  -- SHA-256(this entry)
    previous_hash   VARCHAR(64) NOT NULL,  -- previous entry's entry_hash
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Hash computation trigger
CREATE OR REPLACE FUNCTION compute_audit_hash()
RETURNS TRIGGER AS $$
DECLARE
    prev_hash VARCHAR(64);
    payload TEXT;
BEGIN
    SELECT entry_hash INTO prev_hash FROM canary_app.audit_log
        ORDER BY id DESC LIMIT 1;
    IF prev_hash IS NULL THEN
        prev_hash := '0000000000000000000000000000000000000000000000000000000000000000';
    END IF;
    NEW.previous_hash := prev_hash;
    payload := NEW.table_name || NEW.record_id || NEW.action || COALESCE(NEW.actor_id::text, '') || NEW.created_at::text || prev_hash;
    NEW.entry_hash := encode(digest(payload, 'sha256'), 'hex');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_log_hash
    BEFORE INSERT ON canary_app.audit_log
    FOR EACH ROW EXECUTE FUNCTION compute_audit_hash();
```

**Flask Endpoint:**
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| GET | `/audit/verify-chain` | Keycloak JWT (admin) | Validate entire hash chain integrity |

---

### TR-7.3: Evidentiary Integrity (FR-7.3)

Already covered in TR-3.2. INSERT-only triggers on `fox_evidence` and `fox_evidence_access_log`.

---

## TR-8: Authentication & Authorization (implements FR-8)

### TR-8.1: Identity Management (FR-8.1)

**Primary Service:** Keycloak

**Implementation:** Keycloak handles all identity management. Flask and Hasura validate Keycloak-issued JWT tokens; neither service manages users directly.

| Feature | Keycloak Component |
|---------|-------------------|
| User registration | Keycloak registration page (themed to Canary brand) |
| Login | Keycloak login page (OIDC flow) |
| MFA | Keycloak OTP authenticator |
| Password reset | Keycloak built-in recovery flow |
| SSO | Keycloak broker for Google/Apple (optional) |
| Session management | Keycloak session settings (configurable timeout per realm) |

**JWT Token Structure (issued by Keycloak, consumed by Hasura + Flask):**
```json
{
  "sub": "user-uuid",
  "iss": "https://auth.canary.lp/realms/{merchant}",
  "aud": "canary-api",
  "exp": 1740000000,
  "iat": 1739996400,
  "realm_access": { "roles": ["merchant_owner"] },
  "x-hasura-merchant-id": "merchant-uuid",
  "x-hasura-default-role": "merchant_owner",
  "x-hasura-allowed-roles": ["merchant_owner", "store_manager"],
  "x-hasura-location-ids": "{loc-uuid-1,loc-uuid-2}"
}
```

---

### TR-8.2: API Authentication (FR-8.2)

**Implementation:**

| API Layer | Auth Method |
|-----------|-----------|
| Hasura GraphQL | JWT validation (Keycloak public key) → row-level permissions from claims |
| Flask endpoints | JWT validation via `PyJWT` library + Keycloak public key |
| Airflow internal | Service account token (Keycloak client credentials grant) |
| Directus | Keycloak OIDC client |
| Superset | Keycloak OIDC client |

**Rate Limiting:** Implemented at the reverse proxy layer (Nginx/Traefik) — per-merchant limits based on JWT claim.

---

## TR-9: Administration (implements FR-9)

### TR-9.1: Data Browsing & Management (FR-9.1)

**Primary Service:** Directus

**Implementation:** Directus auto-generates an admin UI from the PostgreSQL schema. All 35+ CRDM tables are browsable with filtering, sorting, search, and inline relationship navigation.

**Directus Configuration:**
- All `canary_app` and `canary_sales` tables registered as Directus collections
- Inline relationship navigation configured (transaction → line items, tenders, refund links)
- Role-based views: admin (all data), merchant (filtered by merchant_id), analyst (read-only)
- Custom actions: "Create Fox Case", "Escalate Alert", "Bulk Export"

**AC Mapping:**
- FR-9.1.1 → Directus collection browser with filters
- FR-9.1.2 → Directus relationship fields for navigation
- FR-9.1.3 → Directus roles mapped from Keycloak
- FR-9.1.4 → Directus custom flows/actions for Fox operations

---

### TR-9.2: Rule Configuration (FR-9.2)

**Primary Service:** Directus (UI) + Hasura (API) + PostgreSQL (storage)

**Implementation:** Merchants configure Chirp thresholds through a Directus custom interface or a merchant portal page. Changes write to `merchant_rule_config` via Hasura mutation. Audit log captures every change.

---

## TR-10: Workflow Orchestration (implements FR-10)

### TR-10.1: Scheduled Detection (FR-10.1)

**Primary Service:** Apache Airflow

**Implementation:**
```
DAG: chirp_detection_sweep
Schedule: @hourly
├── Task: check_new_data (sensor — skip if no new transactions since last sweep)
├── Task: load_active_rules (query detection_rules + merchant_rule_config)
├── Task: evaluate_rules (Python — iterate merchants, run all active rules)
├── Task: generate_alerts (Python — bulk INSERT to canary_sales.alerts)
├── Task: send_notifications (HTTP — Flask notification service)
└── Task: update_sweep_log (Python — log execution metrics)

Retry policy: 3 retries, exponential backoff (60s, 300s, 900s)
Alert on failure: Slack webhook + email to ops
```

**AC Mapping:**
- FR-10.1.1 → Airflow `@hourly` schedule
- FR-10.1.2 → Airflow retry policy with exponential backoff
- FR-10.1.3 → Airflow UI monitoring + failure alerting
- FR-10.1.4 → `sweep_log` table tracks execution time, rules evaluated, alerts generated

---

### TR-10.2: ETL Pipeline (FR-10.2)

**Primary Service:** Apache Airflow

Already covered in TR-5.1 (`canary_metrics_etl` DAG).

**AC Mapping:**
- FR-10.2.1 → `canary_metrics_etl` DAG runs daily at 02:00 UTC
- FR-10.2.2 → All metric aggregations use `INSERT ... ON CONFLICT UPDATE` (upsert) pattern
- FR-10.2.3 → DAG failure triggers Slack alert; metrics from previous successful run preserved

---

## TR-11: Bitcoin & Lightning / Goose (implements FR-11 — Post-MVP)

### TR-11.1: Lightning Payment Processing (FR-11.1)

**Primary Service:** BTCPay Server (Docker container) + Flask (subscription management)

**Implementation Notes (architectural planning only):**
- BTCPay Server deployed as Docker service in the Alpha 3X compose stack
- Flask integration via BTCPay Greenfield API
- Lightning invoices for subscription billing and pay-per-query metering
- Invoice webhook → Flask → update merchant subscription status

---

### TR-11.2: LNURL-Auth (FR-11.2)

**Implementation Notes:**
- Keycloak custom authenticator or identity provider for LNURL-auth protocol
- PhD to evaluate Keycloak extension feasibility
- Fallback: Flask-managed LNURL-auth as a parallel auth path

---

### TR-11.3: Chain of Custody Ordinals (FR-11.3)

**Implementation Notes:**
- Fox evidence export generates a JSON evidence packet
- Flask calls OrdinalsBot API to mint the packet as a Bitcoin Ordinal
- Ordinal transaction ID stored in `fox_evidence.metadata` JSONB
- Cost estimate: ~50 sats per mint via OrdinalsBot/Gamma API

---

## Cross-Cutting Technical Requirements

### CTR-1: Docker Compose Topology

The full Alpha 3X stack runs as a Docker Compose application:

```yaml
# Target docker-compose.yml (simplified)
services:
  postgres:
    image: postgres:17-alpine
    volumes: [pgdata:/var/lib/postgresql/data]
    environment: [POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD]

  keycloak:
    image: quay.io/keycloak/keycloak:26-alpine
    depends_on: [postgres]
    environment: [KC_DB=postgres, KC_DB_URL, ...]

  hasura:
    image: hasura/graphql-engine:v2.latest
    depends_on: [postgres, keycloak]
    environment: [HASURA_GRAPHQL_DATABASE_URL, HASURA_GRAPHQL_JWT_SECRET, ...]

  directus:
    image: directus/directus:11
    depends_on: [postgres, keycloak]
    environment: [DB_CLIENT=pg, DB_HOST=postgres, ...]

  superset:
    image: apache/superset:4
    depends_on: [postgres, keycloak]

  airflow-webserver:
    image: apache/airflow:2
    depends_on: [postgres]

  airflow-scheduler:
    image: apache/airflow:2
    depends_on: [postgres]

  flask-api:
    build: .
    depends_on: [postgres, keycloak, hasura]
    environment: [DATABASE_URL, KEYCLOAK_URL, SQUARE_APP_ID, ...]

  nginx:
    image: nginx:alpine  # OR traefik:v3
    ports: ["80:80", "443:443"]
    depends_on: [hasura, flask-api, directus, superset, keycloak]
```

### CTR-2: Secret Management

| Secret | Storage | Rotation |
|--------|---------|----------|
| PostgreSQL credentials | Docker secrets / environment | Per deployment |
| Keycloak admin password | Docker secrets | Per deployment |
| Hasura admin secret | Docker secrets | Per deployment |
| Square OAuth app credentials | Docker secrets | Per Square rotation policy |
| Merchant OAuth tokens | PostgreSQL (AES-256 encrypted) | Automatic refresh |
| JWT signing keys | Keycloak (auto-managed) | Keycloak rotation policy |
| HMAC webhook secret | Docker secrets | Per Square app configuration |

### CTR-3: Logging & Observability

| Signal | Tool | Storage |
|--------|------|---------|
| Application logs | Flask/Gunicorn → stdout → Docker logs | Docker log driver |
| API access logs | Nginx/Traefik access logs | Docker log driver |
| Audit trail | PostgreSQL `audit_log` table | `canary_app` database |
| DAG execution | Airflow UI + task logs | Airflow metadata DB |
| Container health | Portainer (QA) / Docker healthchecks | Portainer |
| Metrics (future) | Prometheus + Grafana (post-MVP) | Prometheus TSDB |

### CTR-4: Migration Strategy

Existing code and data from the dry run carries forward under "preserve and audit":

| Asset | Migration Path |
|-------|---------------|
| Chirp rules (`chirp.py`) | Refactor as standalone module callable by Flask and Airflow |
| Square parsers | Extract into `canary/parsers/` package implementing `POSParser` ABC |
| SQLAlchemy models | Retain for Flask business logic; Hasura handles CRUD separately |
| Unit tests (Chirp rules) | Keep — they test business logic independent of stack |
| E2E API tests | Rewrite — endpoints change from Flask routes to Hasura GraphQL |
| Browser tests | Rewrite — UI changes from Jinja2 to Directus/Superset |
| PostgreSQL schemas | Migrate via Alembic or Hasura Migrations (due diligence to decide) |
| Auth module | Deprecated — replaced by Keycloak |
| Admin panel | Deprecated — replaced by Directus |
| Polling worker | Deprecated — replaced by Airflow |

---

## Traceability: FR → TR → Stack Component

| FR | TR | Primary Service | Supporting Services |
|----|-----|----------------|-------------------|
| FR-1.1 | TR-1.1 | Flask, PostgreSQL | Hasura (event triggers), Airflow (dead letter) |
| FR-1.2 | TR-1.2 | Flask (parsers), PostgreSQL | — |
| FR-1.3 | TR-1.3 | Flask (parser registry) | — |
| FR-1.4 | TR-1.4 | Flask, PostgreSQL | Airflow (scheduled polls) |
| FR-2.1 | TR-2.1 | Flask (Chirp), PostgreSQL | Hasura (events), Airflow (sweeps) |
| FR-2.2 | TR-2.2 | Flask (SQLAlchemy JOINs) | PostgreSQL |
| FR-2.3 | TR-2.3 | Hasura, PostgreSQL | Flask (notifications) |
| FR-3.1 | TR-3.1 | Flask, Hasura, Directus | PostgreSQL |
| FR-3.2 | TR-3.2 | Flask, PostgreSQL | — |
| FR-3.3 | TR-3.3 | PostgreSQL, Hasura | — |
| FR-4.1 | TR-4.1 | PostgreSQL (RLS), Hasura, Keycloak | — |
| FR-4.2 | TR-4.2 | Keycloak, Hasura | — |
| FR-4.3 | TR-4.3 | PostgreSQL, Hasura | — |
| FR-5.1 | TR-5.1 | Superset, PostgreSQL | Airflow (ETL) |
| FR-5.2 | TR-5.2 | Superset SQL Lab | PostgreSQL |
| FR-5.3 | TR-5.3 | Airflow, Superset | Flask (email) |
| FR-6.1 | TR-6.1 | Flask | Airflow (token refresh) |
| FR-6.2 | TR-6.2 | Flask (TR-1.1) | — |
| FR-6.3 | TR-6.3 | PostgreSQL, Nginx/Traefik | Flask (sanitizer) |
| FR-6.4 | TR-6.4 | Flask | Airflow (initial sync) |
| FR-7.1 | TR-7.1 | PostgreSQL (triggers) | — |
| FR-7.2 | TR-7.2 | PostgreSQL (pgcrypto) | Flask (verification) |
| FR-7.3 | TR-7.3 | PostgreSQL, Flask | — |
| FR-8.1 | TR-8.1 | Keycloak | — |
| FR-8.2 | TR-8.2 | Keycloak, Hasura, Flask | Nginx/Traefik (rate limit) |
| FR-9.1 | TR-9.1 | Directus | PostgreSQL |
| FR-9.2 | TR-9.2 | Directus, Hasura | PostgreSQL |
| FR-10.1 | TR-10.1 | Airflow | Flask (Chirp) |
| FR-10.2 | TR-10.2 | Airflow | PostgreSQL |
| FR-11.x | TR-11.x | BTCPay, Flask | Keycloak (LNURL-auth) |

---

## Due Diligence Validation Points

This document creates specific technical claims that PhD, Tom, and Jeremy must validate:

1. **Hasura event triggers are suitable for real-time Chirp evaluation** (TR-2.1) — latency, reliability, ordering guarantees
2. **PostgreSQL RLS + Hasura permissions + Keycloak realms provide true multi-tenant isolation** (TR-4.1) — verify no bypass path
3. **Airflow on the iMac QA box can run all DAGs simultaneously** (TR-10.1) — resource assessment
4. **Superset embedded dashboards work with Keycloak OIDC** (TR-5.1) — integration proof-of-concept
5. **Directus custom actions can support Fox case management workflows** (TR-9.1) — extension API evaluation
6. **Flask + Hasura remote schema integration is production-viable** (TR-2.1) — performance, error handling
7. **The full Docker Compose stack runs on the iMac** (CTR-1) — memory, CPU, disk requirements
8. **Schema migration strategy supports three-database architecture** (CTR-4) — Alembic vs Hasura Migrations

---

*These requirements define HOW the Alpha 3X stack implements each functional requirement. They are starting points for the due diligence exercise, not final designs.*

*"Do it right, do it once." — Jeffe*
