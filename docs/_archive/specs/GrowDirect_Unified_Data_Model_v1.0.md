---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# GrowDirect Unified Data Model Specification
## Enterprise Retail Intelligence Platform

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.0
**Date:** February 17, 2026
**Authors:** Tom (Systems Architect), Jeremy (Developer Quant)
**For:** Alex, Jeffe - Strategic Review
**Classification:** Internal - Strategic

---

## Executive Summary

This specification defines the unified data model for the GrowDirect platform, synthesizing 25+ years of Fortune 500 retail data modeling expertise (GSLM, CRDM, Walmart case management) into a modern, blockchain-enabled architecture for SMB retailers.

**Strategic Imperative:** Build once what took Walmart, Kroger, and Tesco decades and billions to develop. Package it for Square merchants at $49/month.

**Architectural Foundation:**
- **GSLM Patterns**: 6-level hierarchies, effective dating, many-to-many junctions, attribute localization
- **CRDM Intelligence**: Point-of-sale aggregation, control tables, logging patterns
- **Walmart Case Management**: Investigation workflows, evidence chains, subject tracking, quality assurance scorecards
- **Modern Enhancements**: Blockchain verification, hash-chained auditability, AVAX smart contract integration

---

## Part 1: Platform Architecture Overview

### 1.1 Product Ecosystem

```
┌─────────────────────────────────────────────────────────────────┐
│                    GROWDIRECT PLATFORM                           │
│                  Unified Data Intelligence Layer                 │
└─────────────────────────────────────────────────────────────────┘

┌────────────── CORE PRODUCTS ────────────────────────────────────┐
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   CANARY    │  │     OWL     │  │     FOX     │             │
│  │ Loss Prevent│  │  Analytics  │  │ Case Mgmt   │             │
│  │   Detection │  │   Oracle    │  │  Evidence   │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                 │                 │                     │
│         └─────────────────┴─────────────────┘                     │
│                           │                                       │
│                  ┌────────▼────────┐                             │
│                  │      GOOSE      │                             │
│                  │  Bitcoin/Money  │                             │
│                  │   Payment Rails │                             │
│                  └─────────────────┘                             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

┌────────────── DATA LAYER ───────────────────────────────────────┐
│                                                                   │
│  PostgreSQL + TimescaleDB (time-series)                          │
│  ├─ Operational Database (OLTP)                                  │
│  ├─ Analytics Warehouse (OLAP)                                   │
│  └─ Blockchain Metadata (AVAX + IPFS references)                 │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

┌────────────── INTEGRATION SOURCES ──────────────────────────────┐
│                                                                   │
│  Square POS → OAuth → Webhooks → Data Pipeline                   │
│  BTCPay Server → Lightning Node → Payment Events                 │
│  AVAX Subnet → Smart Contracts → Blockchain Verification         │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### 1.2 Product-to-Entity Mapping

| Product | Primary Entities | GSLM Influence | Walmart Influence |
|---------|------------------|----------------|-------------------|
| **Canary** | merchants, transactions, alerts, refunds, employees | GSLM Item, GSLM Location | Walmart SRA Scorecards, Exception Detection |
| **Owl** | analytics_snapshots, metrics, predictions, dashboards | GSLM aggregation patterns | Walmart data warehouse |
| **Fox** | cases, subjects, evidence, timeline_events, attachments | GSLM effective dating | Walmart LPCMS case management |
| **Goose** | btc_payments, lightning_invoices, btc_treasury | N/A (blockchain-native) | N/A |
| **Shared** | users, permissions, audit_log, merchant_settings | GSLM Controls/Parameters | All products |

---

## Part 2: Shared/Core Data Model

### 2.1 Merchant Management

**GSLM Pattern:** Organizational hierarchy with effective dating
**Inspiration:** GSLM Location Overview

```sql
-- Core merchant entity
CREATE TABLE merchants (
    id SERIAL PRIMARY KEY,
    merchant_id VARCHAR(255) UNIQUE NOT NULL,  -- Square merchant ID
    merchant_name VARCHAR(255) NOT NULL,
    business_type VARCHAR(100),
    square_access_token TEXT,  -- Encrypted
    square_refresh_token TEXT,  -- Encrypted
    square_token_expires_at TIMESTAMP,

    -- GSLM-style metadata
    effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,  -- NULL = currently active
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- active, suspended, closed

    -- Hierarchy support (franchise/chain)
    parent_merchant_id INTEGER REFERENCES merchants(id),  -- For franchise relationships
    hierarchy_level INTEGER DEFAULT 0,  -- 0=corporate, 1=region, 2=franchisee

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),

    -- Blockchain verification
    blockchain_verified BOOLEAN DEFAULT FALSE,
    blockchain_tx_hash VARCHAR(66),  -- AVAX transaction hash

    CONSTRAINT chk_status CHECK (status IN ('active', 'suspended', 'closed', 'pending'))
);

CREATE INDEX idx_merchants_merchant_id ON merchants(merchant_id);
CREATE INDEX idx_merchants_status ON merchants(status) WHERE status = 'active';
CREATE INDEX idx_merchants_parent ON merchants(parent_merchant_id);
CREATE INDEX idx_merchants_hierarchy ON merchants(hierarchy_level, parent_merchant_id);
```

**Key GSLM Enhancements:**
- Effective dating allows temporal merchant history
- Hierarchy support mirrors GSLM's 6-level merchandise hierarchy
- Status tracking follows GSLM entity lifecycle patterns

### 2.2 Location Management

**GSLM Pattern:** GSLM Location Overview (stores, warehouses, DC)
**Walmart Pattern:** Market → Region → Division → Store hierarchy

```sql
-- Retail locations (stores, warehouses, mobile units)
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    square_location_id VARCHAR(255) UNIQUE,  -- Square location ID

    -- Location identification
    location_code VARCHAR(50) NOT NULL,  -- Store #, DC code, etc.
    location_name VARCHAR(255) NOT NULL,
    location_type VARCHAR(50) NOT NULL,  -- store, warehouse, distribution_center, mobile, corporate

    -- Geographic hierarchy (Walmart-style)
    market VARCHAR(100),  -- Market name (e.g., "Northeast", "SoCal")
    region VARCHAR(100),  -- Region within market
    division VARCHAR(100),  -- Division (broader grouping)

    -- Physical address
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(3) DEFAULT 'USA',

    -- Operating parameters
    timezone VARCHAR(50) NOT NULL DEFAULT 'America/New_York',
    currency VARCHAR(3) DEFAULT 'USD',
    sq_footage INTEGER,  -- For sales per sq ft calculations

    -- Operating hours (JSON array of schedules)
    business_hours JSONB,  -- {"monday": {"open": "09:00", "close": "21:00"}, ...}

    -- GSLM-style lifecycle
    effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'active',  -- active, inactive, temp_closed, renovation

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_location_status CHECK (status IN ('active', 'inactive', 'temp_closed', 'renovation')),
    CONSTRAINT chk_location_type CHECK (location_type IN ('store', 'warehouse', 'distribution_center', 'mobile', 'corporate'))
);

CREATE INDEX idx_locations_merchant ON locations(merchant_id) WHERE status = 'active';
CREATE INDEX idx_locations_square_id ON locations(square_location_id);
CREATE INDEX idx_locations_market_region ON locations(market, region, division);
CREATE INDEX idx_locations_status ON locations(status);
```

**Walmart SRA Scorecard Integration:**
- Market/Region/Division hierarchy enables rollup reporting like Walmart SRA scorecards
- Store #/location_code maps to Walmart store identification patterns
- Geographic hierarchy supports drill-down: SUP → Division → Region → Market → Store

### 2.3 User Management & RBAC

**Pattern:** Enterprise role-based access control with data restrictions
**Walmart Influence:** Multi-level user roles (Analyst, Manager, Corporate, LP Director)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name VARCHAR(255) NOT NULL,

    -- Role (simplified from Walmart's complex role matrix)
    role VARCHAR(50) NOT NULL,  -- admin, manager, analyst, viewer, lp_investigator

    -- Account status
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,

    -- Data restrictions (GSLM-style attribute filtering)
    data_restrictions JSONB,  -- {"locations": [1,2,3], "sensitivity_level": "restricted"}

    -- Session management
    last_login_at TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,

    -- Lifecycle
    effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_user_role CHECK (role IN ('admin', 'manager', 'analyst', 'viewer', 'lp_investigator', 'franchisee'))
);

CREATE INDEX idx_users_merchant ON users(merchant_id) WHERE is_active = TRUE;
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role, merchant_id);

-- Permissions table (capability-based permissions)
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,  -- manage_users, view_analytics, create_cases, etc.
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),  -- admin, canary, fox, owl, goose
    is_sensitive BOOLEAN DEFAULT FALSE,  -- Requires elevated privileges
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Role-permission mapping (many-to-many)
CREATE TABLE role_permissions (
    role VARCHAR(50) NOT NULL,
    permission_id INTEGER NOT NULL REFERENCES permissions(id),
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role, permission_id)
);

CREATE INDEX idx_role_permissions_role ON role_permissions(role);
```

### 2.4 Audit Logging

**Pattern:** Comprehensive audit trail for compliance (SOX, HIPAA-style rigor)
**Walmart Influence:** Case management audit requirements, QA documentation

```sql
-- Audit log (immutable, append-only)
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,

    -- Who, What, When
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    user_id INTEGER REFERENCES users(id),  -- NULL for system actions
    action VARCHAR(100) NOT NULL,  -- user.created, case.opened, alert.acknowledged, etc.

    -- Resource identification
    resource_type VARCHAR(50),  -- user, case, alert, transaction, setting
    resource_id VARCHAR(255),

    -- Context
    ip_address INET,
    user_agent TEXT,
    request_path VARCHAR(500),

    -- Details (encrypted for sensitive data)
    metadata JSONB,  -- Flexible metadata storage

    -- Tamper detection (hash chaining like Fox timeline)
    event_hash VARCHAR(64) GENERATED ALWAYS AS (
        encode(sha256(
            (id || merchant_id || COALESCE(user_id::TEXT, '') || action ||
             resource_type || COALESCE(resource_id, '') || timestamp)::bytea
        ), 'hex')
    ) STORED,
    previous_event_hash VARCHAR(64),  -- Hash of previous event (blockchain-style chain)

    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Blockchain anchoring (periodic)
    blockchain_anchored BOOLEAN DEFAULT FALSE,
    blockchain_anchor_tx VARCHAR(66)
);

CREATE INDEX idx_audit_merchant_time ON audit_log(merchant_id, timestamp DESC);
CREATE INDEX idx_audit_user ON audit_log(user_id, timestamp DESC);
CREATE INDEX idx_audit_resource ON audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_action ON audit_log(action, merchant_id);
```

**Key Innovation:** Hash-chained audit log provides tamper-evident history similar to blockchain, but stored in PostgreSQL for query performance.

---

## Part 3: Canary LP - Loss Prevention Core

### 3.1 Transaction Management

**GSLM Pattern:** GSLM Point of Sale tables + CRDM POS aggregation
**Walmart Pattern:** Transaction-level exception detection

```sql
-- Transactions (normalized from Square Payments API)
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    location_id INTEGER REFERENCES locations(id),

    -- Square identifiers
    payment_id VARCHAR(255) UNIQUE NOT NULL,  -- Square payment ID
    order_id VARCHAR(255),  -- Square order ID

    -- Transaction details
    amount_cents BIGINT NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(50) NOT NULL,  -- COMPLETED, CANCELED, FAILED

    -- Payment method
    source_type VARCHAR(50),  -- card, cash, square_gift_card, bank_account
    card_brand VARCHAR(50),  -- VISA, MASTERCARD, AMEX, DISCOVER
    last_4 VARCHAR(4),

    -- Refund tracking
    is_refund BOOLEAN DEFAULT FALSE,
    refund_amount_cents BIGINT DEFAULT 0,
    refunded_at TIMESTAMP,
    refund_reason VARCHAR(255),

    -- Employee/device tracking (Walmart SRA pattern)
    employee_id VARCHAR(255),  -- Square team member ID
    employee_name VARCHAR(255),
    device_id VARCHAR(255),  -- Register/device ID

    -- Timestamps
    transaction_date TIMESTAMP NOT NULL,  -- When transaction occurred
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    synced_at TIMESTAMP,  -- When we pulled from Square

    -- Velocity tracking (Fireball/Canary)
    item_count INTEGER DEFAULT 1,
    discount_amount_cents BIGINT DEFAULT 0,
    tip_amount_cents BIGINT DEFAULT 0,
    tax_amount_cents BIGINT DEFAULT 0,

    -- Full Square payload (for deep analysis)
    raw_data JSONB,

    -- GSLM-style effective dating
    effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_transaction_status CHECK (status IN ('COMPLETED', 'CANCELED', 'FAILED', 'PENDING'))
);

CREATE INDEX idx_transactions_merchant_date ON transactions(merchant_id, transaction_date DESC);
CREATE INDEX idx_transactions_location_date ON transactions(location_id, transaction_date DESC);
CREATE INDEX idx_transactions_payment_id ON transactions(payment_id);
CREATE INDEX idx_transactions_employee ON transactions(employee_id, transaction_date DESC);
CREATE INDEX idx_transactions_refunds ON transactions(merchant_id, is_refund) WHERE is_refund = TRUE;
CREATE INDEX idx_transactions_status ON transactions(status, merchant_id);

-- Transaction line items (GSLM Item pattern)
CREATE TABLE transaction_items (
    id BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),

    -- Item identification
    catalog_item_id VARCHAR(255),  -- Square catalog item ID
    variation_id VARCHAR(255),  -- Square variation ID
    item_name VARCHAR(500) NOT NULL,
    item_sku VARCHAR(255),

    -- Quantity and pricing
    quantity DECIMAL(10,3) NOT NULL,  -- Allow fractional (e.g., 2.5 lbs)
    unit_price_cents BIGINT NOT NULL,
    total_price_cents BIGINT NOT NULL,

    -- Discounts and modifiers
    discount_cents BIGINT DEFAULT 0,
    modifier_cost_cents BIGINT DEFAULT 0,

    -- Item category (GSLM hierarchy lite)
    category VARCHAR(255),
    subcategory VARCHAR(255),

    -- Flags
    is_void BOOLEAN DEFAULT FALSE,
    is_return BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transaction_items_transaction ON transaction_items(transaction_id);
CREATE INDEX idx_transaction_items_merchant ON transaction_items(merchant_id);
CREATE INDEX idx_transaction_items_catalog ON transaction_items(catalog_item_id);
CREATE INDEX idx_transaction_items_sku ON transaction_items(item_sku);
```

**CRDM Integration:** Transaction and transaction_items mirror CRDM POS tables structure with aggregation-ready indexing.

### 3.2 Alert Detection & Management

**Pattern:** Exception-based reporting (EBR) from Walmart Secure platform
**Walmart Influence:** SRA Scorecards, exception workflows, severity classification

```sql
-- Alerts (Canary detection results)
CREATE TABLE alerts (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    location_id INTEGER REFERENCES locations(id),

    -- Alert classification
    alert_type VARCHAR(100) NOT NULL,  -- refund_frequency, large_refund, after_hours, rapid_sequence
    severity VARCHAR(20) NOT NULL,  -- low, medium, high, critical

    -- Subject of alert
    employee_id VARCHAR(255),
    employee_name VARCHAR(255),

    -- Triggering transaction(s)
    transaction_id BIGINT REFERENCES transactions(id),
    related_transaction_ids BIGINT[],  -- Array of related transactions

    -- Metrics
    refund_count INTEGER,
    total_amount_cents BIGINT,
    time_window_minutes INTEGER,  -- For velocity-based alerts

    -- Alert message
    message TEXT NOT NULL,
    metadata JSONB,  -- Detection algorithm details

    -- Status tracking (Walmart case workflow)
    status VARCHAR(50) NOT NULL DEFAULT 'open',  -- open, acknowledged, investigating, resolved, false_positive
    acknowledged_by INTEGER REFERENCES users(id),
    acknowledged_at TIMESTAMP,
    resolved_by INTEGER REFERENCES users(id),
    resolved_at TIMESTAMP,
    resolution_notes TEXT,

    -- Scoring (AI threat scoring for Fox integration)
    risk_score INTEGER,  -- 0-100
    confidence_score DECIMAL(5,2),  -- 0.00-100.00

    -- Timestamps
    detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Blockchain verification
    blockchain_verified BOOLEAN DEFAULT FALSE,
    ipfs_evidence_hash VARCHAR(64),  -- IPFS hash for supporting evidence

    CONSTRAINT chk_alert_severity CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    CONSTRAINT chk_alert_status CHECK (status IN ('open', 'acknowledged', 'investigating', 'resolved', 'false_positive'))
);

CREATE INDEX idx_alerts_merchant_date ON alerts(merchant_id, detected_at DESC);
CREATE INDEX idx_alerts_status ON alerts(merchant_id, status) WHERE status IN ('open', 'acknowledged');
CREATE INDEX idx_alerts_employee ON alerts(employee_id, detected_at DESC);
CREATE INDEX idx_alerts_severity ON alerts(severity, merchant_id) WHERE severity IN ('high', 'critical');
CREATE INDEX idx_alerts_type ON alerts(alert_type, merchant_id);
```

**Walmart SRA Scorecard Alignment:**
- Severity levels map to Walmart's P1-P4 priority system
- Status workflow mirrors Walmart case management (open → investigating → resolved)
- Employee-centric grouping enables scorecard-style rollups

---

## Part 4: Fox - Case Management & Investigations

### 4.1 Case Management

**Pattern:** Walmart LPCMS (Loss Prevention Case Management System)
**Source:** LPCMS Business Requirements Document, Walmart Case Management.docx

```sql
-- Cases (investigation master record)
CREATE TABLE fox_cases (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),

    -- Case identification
    case_number VARCHAR(50) UNIQUE NOT NULL,  -- Human-readable case ID (e.g., "LP-2026-001")
    case_title VARCHAR(500) NOT NULL,
    case_type VARCHAR(100) NOT NULL,  -- employee_theft, customer_fraud, vendor_fraud, organized_retail_crime

    -- Classification (Walmart LPCMS pattern)
    incident_category VARCHAR(100),  -- refund_fraud, cash_theft, merchandise_theft, policy_violation
    loss_type VARCHAR(100),  -- shrinkage, cash_shortage, property_damage, time_theft

    -- Financial impact
    estimated_loss_cents BIGINT,
    recovered_amount_cents BIGINT DEFAULT 0,
    restitution_amount_cents BIGINT DEFAULT 0,

    -- Location and scope
    primary_location_id INTEGER REFERENCES locations(id),
    affected_locations INTEGER[],  -- Array of location IDs

    -- Case ownership
    assigned_investigator INTEGER REFERENCES users(id),
    assigned_team VARCHAR(100),  -- LP, HR, Legal, Corporate

    -- Status workflow (Walmart case lifecycle)
    case_status VARCHAR(50) NOT NULL DEFAULT 'open',
    -- open, under_investigation, suspended, closed_resolved, closed_unsubstantiated, closed_unfounded

    priority VARCHAR(20) NOT NULL DEFAULT 'medium',  -- low, medium, high, critical

    -- Dates
    incident_date TIMESTAMP,  -- When incident occurred
    reported_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    opened_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_date TIMESTAMP,

    -- Effective dating (GSLM pattern)
    effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,

    -- Investigation summary
    description TEXT,
    findings_summary TEXT,
    corrective_actions TEXT,

    -- Legal/HR flags
    law_enforcement_notified BOOLEAN DEFAULT FALSE,
    law_enforcement_case_number VARCHAR(100),
    hr_action_taken BOOLEAN DEFAULT FALSE,
    hr_action_type VARCHAR(100),  -- verbal_warning, written_warning, suspension, termination

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),

    -- Hash chaining (tamper-evident)
    case_hash VARCHAR(64) GENERATED ALWAYS AS (
        encode(sha256((id || case_number || merchant_id || case_status || opened_date)::TEXT::bytea), 'hex')
    ) STORED,

    CONSTRAINT chk_case_type CHECK (case_type IN ('employee_theft', 'customer_fraud', 'vendor_fraud', 'organized_retail_crime', 'policy_violation', 'other')),
    CONSTRAINT chk_case_status CHECK (case_status IN ('open', 'under_investigation', 'suspended', 'closed_resolved', 'closed_unsubstantiated', 'closed_unfounded')),
    CONSTRAINT chk_priority CHECK (priority IN ('low', 'medium', 'high', 'critical'))
);

CREATE INDEX idx_fox_cases_merchant ON fox_cases(merchant_id, opened_date DESC);
CREATE INDEX idx_fox_cases_status ON fox_cases(case_status, merchant_id);
CREATE INDEX idx_fox_cases_investigator ON fox_cases(assigned_investigator);
CREATE INDEX idx_fox_cases_location ON fox_cases(primary_location_id);
CREATE INDEX idx_fox_cases_case_number ON fox_cases(case_number);
```

### 4.2 Subject Management

**Pattern:** Walmart subject profiles, threat scoring
**Innovation:** AI-powered risk scoring based on historical patterns

```sql
-- Subjects (individuals/entities under investigation)
CREATE TABLE fox_subjects (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),

    -- Subject identification
    subject_type VARCHAR(50) NOT NULL,  -- employee, customer, vendor, external_entity

    -- Personal identification (encrypted PII)
    full_name VARCHAR(255),
    employee_id VARCHAR(255),  -- Square team member ID or internal EE#
    email VARCHAR(255),
    phone VARCHAR(50),

    -- Physical description
    date_of_birth DATE,
    address_line1 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),

    -- Employment details (if employee)
    hire_date DATE,
    termination_date DATE,
    job_title VARCHAR(255),
    department VARCHAR(100),

    -- Threat assessment
    risk_level VARCHAR(20) DEFAULT 'unknown',  -- unknown, low, medium, high, extreme
    threat_score INTEGER,  -- 0-100 calculated by AI

    -- Status
    subject_status VARCHAR(50) NOT NULL DEFAULT 'active',  -- active, terminated, banned, cleared, deceased

    -- Case history
    total_cases INTEGER DEFAULT 0,
    active_cases INTEGER DEFAULT 0,
    total_loss_cents BIGINT DEFAULT 0,

    -- Hierarchical relationships (GSLM pattern)
    parent_subject_id INTEGER REFERENCES fox_subjects(id),  -- For organized crime networks

    -- Notes and alerts
    investigator_notes TEXT,
    alert_flags JSONB,  -- {"violence_risk": true, "flight_risk": false}

    -- Lifecycle (GSLM effective dating)
    effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),

    -- Privacy/compliance
    data_retention_date TIMESTAMP,  -- When to purge (GDPR/CCPA)

    CONSTRAINT chk_subject_type CHECK (subject_type IN ('employee', 'customer', 'vendor', 'external_entity', 'unknown')),
    CONSTRAINT chk_subject_status CHECK (subject_status IN ('active', 'terminated', 'banned', 'cleared', 'deceased')),
    CONSTRAINT chk_risk_level CHECK (risk_level IN ('unknown', 'low', 'medium', 'high', 'extreme'))
);

CREATE INDEX idx_fox_subjects_merchant ON fox_subjects(merchant_id);
CREATE INDEX idx_fox_subjects_employee ON fox_subjects(employee_id) WHERE subject_type = 'employee';
CREATE INDEX idx_fox_subjects_risk ON fox_subjects(risk_level, merchant_id) WHERE risk_level IN ('high', 'extreme');
CREATE INDEX idx_fox_subjects_status ON fox_subjects(subject_status, merchant_id);
CREATE INDEX idx_fox_subjects_parent ON fox_subjects(parent_subject_id);  -- Network analysis
```

### 4.3 Evidence Management

**Pattern:** Chain of custody from law enforcement evidence management
**Walmart Influence:** Secure 3.2 evidence attachment system

```sql
-- Evidence (photos, videos, documents, recordings)
CREATE TABLE fox_evidence (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    case_id BIGINT REFERENCES fox_cases(id) ON DELETE RESTRICT,  -- Cannot delete evidence if case exists

    -- Evidence identification
    evidence_number VARCHAR(50) UNIQUE NOT NULL,  -- E-2026-001
    evidence_type VARCHAR(100) NOT NULL,  -- photo, video, document, audio, physical_item, digital_screenshot

    -- File storage
    file_path VARCHAR(500),  -- Local/S3 path
    ipfs_hash VARCHAR(64),  -- IPFS content hash (immutable storage)
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),

    -- Description
    title VARCHAR(500) NOT NULL,
    description TEXT,

    -- Chain of custody
    collected_by INTEGER NOT NULL REFERENCES users(id),
    collected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    collection_location VARCHAR(255),

    chain_custody_log JSONB,  -- Array of custody transfers
    chain_custody_status VARCHAR(50) NOT NULL DEFAULT 'secure',  -- secure, transferred, compromised, destroyed

    -- Versioning (GSLM pattern - evidence can be updated/enhanced)
    version_number INTEGER DEFAULT 1,
    previous_version_id BIGINT REFERENCES fox_evidence(id),

    -- Admissibility (legal)
    is_admissible BOOLEAN DEFAULT TRUE,
    inadmissibility_reason TEXT,

    -- Retention
    retention_required_until TIMESTAMP,
    destruction_date TIMESTAMP,
    destruction_authorized_by INTEGER REFERENCES users(id),

    -- Hash verification (tamper detection)
    content_hash VARCHAR(64) NOT NULL,  -- SHA-256 of file content
    hash_verified_at TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_evidence_type CHECK (evidence_type IN ('photo', 'video', 'document', 'audio', 'physical_item', 'digital_screenshot', 'other')),
    CONSTRAINT chk_custody_status CHECK (chain_custody_status IN ('secure', 'transferred', 'compromised', 'destroyed'))
);

CREATE INDEX idx_fox_evidence_case ON fox_evidence(case_id);
CREATE INDEX idx_fox_evidence_merchant ON fox_evidence(merchant_id);
CREATE INDEX idx_fox_evidence_type ON fox_evidence(evidence_type);
CREATE INDEX idx_fox_evidence_ipfs ON fox_evidence(ipfs_hash);
CREATE INDEX idx_fox_evidence_version ON fox_evidence(previous_version_id);
```

### 4.4 Timeline Events

**Pattern:** Walmart case management chronological audit log
**Innovation:** Hash-chained events for tamper detection

```sql
-- Timeline events (chronological case activity log)
CREATE TABLE fox_timeline_events (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    case_id BIGINT NOT NULL REFERENCES fox_cases(id) ON DELETE CASCADE,

    -- Event details
    event_type VARCHAR(100) NOT NULL,  -- observation, interview, evidence_collected, status_change, note
    event_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Content
    title VARCHAR(500),
    description TEXT NOT NULL,

    -- Participants
    created_by INTEGER NOT NULL REFERENCES users(id),
    participants INTEGER[],  -- Array of user IDs who were involved

    -- Related entities
    related_subject_id BIGINT REFERENCES fox_subjects(id),
    related_evidence_ids BIGINT[],  -- Array of evidence IDs
    related_transaction_ids BIGINT[],  -- Array of transaction IDs

    -- Metadata
    location_of_event VARCHAR(255),
    metadata JSONB,

    -- Hash chaining (blockchain-inspired tamper detection)
    event_hash VARCHAR(64) GENERATED ALWAYS AS (
        encode(sha256((id || case_id || event_type || event_date || description)::TEXT::bytea), 'hex')
    ) STORED,
    previous_event_hash VARCHAR(64),  -- Links to previous event in chain

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_event_type CHECK (event_type IN ('observation', 'interview', 'evidence_collected', 'status_change', 'note', 'action_taken', 'law_enforcement_contact'))
);

CREATE INDEX idx_fox_timeline_case ON fox_timeline_events(case_id, event_date DESC);
CREATE INDEX idx_fox_timeline_merchant ON fox_timeline_events(merchant_id, event_date DESC);
CREATE INDEX idx_fox_timeline_type ON fox_timeline_events(event_type, case_id);
CREATE INDEX idx_fox_timeline_subject ON fox_timeline_events(related_subject_id);
```

**Key Innovation:** Hash chaining creates an immutable audit trail. Each event's hash is based on its content + previous event's hash, making it impossible to alter history without detection.

---

## Part 5: Owl - Analytics & Intelligence

### 5.1 Metrics & Snapshots

**Pattern:** GSLM aggregation tables + CRDM aggregate patterns
**Walmart Influence:** SRA Scorecard metrics, Total Retail Loss framework

```sql
-- Analytics snapshots (time-series aggregations)
CREATE TABLE owl_analytics_snapshots (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    location_id INTEGER REFERENCES locations(id),  -- NULL = merchant-wide

    -- Time dimension
    snapshot_date DATE NOT NULL,
    snapshot_hour INTEGER,  -- 0-23 for hourly snapshots, NULL for daily
    granularity VARCHAR(20) NOT NULL,  -- hourly, daily, weekly, monthly

    -- Sales metrics
    transaction_count INTEGER DEFAULT 0,
    gross_sales_cents BIGINT DEFAULT 0,
    net_sales_cents BIGINT DEFAULT 0,  -- After refunds/voids
    refund_count INTEGER DEFAULT 0,
    refund_amount_cents BIGINT DEFAULT 0,

    -- Loss prevention metrics (Walmart SRA pattern)
    total_shrinkage_cents BIGINT DEFAULT 0,
    detected_fraud_events INTEGER DEFAULT 0,
    prevented_loss_cents BIGINT DEFAULT 0,

    -- Operational metrics
    avg_transaction_cents BIGINT,
    items_sold INTEGER DEFAULT 0,
    unique_customers INTEGER,

    -- Employee metrics
    active_employees INTEGER,
    high_risk_employees INTEGER,  -- Employees with active alerts

    -- Velocity metrics (Fireball pattern)
    velocity_anomaly_count INTEGER DEFAULT 0,
    oos_predictions INTEGER DEFAULT 0,  -- Out of stock predictions

    -- Performance indicators (Walmart SRA rollup style)
    refund_rate DECIMAL(5,2),  -- % of transactions that are refunds
    shrinkage_rate DECIMAL(5,2),  -- % of sales
    productivity_score DECIMAL(5,2),  -- Sales per employee hour

    -- Context (GSLM contextual adjustments)
    day_of_week INTEGER,  -- 0=Sunday, 6=Saturday
    is_holiday BOOLEAN DEFAULT FALSE,
    weather_conditions VARCHAR(100),  -- sunny, rainy, snow, etc.

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Composite unique constraint
    UNIQUE(merchant_id, location_id, snapshot_date, snapshot_hour, granularity)
);

CREATE INDEX idx_owl_snapshots_merchant_date ON owl_analytics_snapshots(merchant_id, snapshot_date DESC);
CREATE INDEX idx_owl_snapshots_location_date ON owl_analytics_snapshots(location_id, snapshot_date DESC);
CREATE INDEX idx_owl_snapshots_granularity ON owl_analytics_snapshots(granularity, merchant_id);

-- Convert to TimescaleDB hypertable for time-series optimization
SELECT create_hypertable('owl_analytics_snapshots', 'snapshot_date', if_not_exists => TRUE);
```

### 5.2 Predictions & Forecasts

**Pattern:** Fireball velocity prediction + ML models
**Walmart Influence:** Demand signal processing

```sql
-- Predictions (ML model outputs)
CREATE TABLE owl_predictions (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    location_id INTEGER REFERENCES locations(id),

    -- Prediction target
    prediction_type VARCHAR(100) NOT NULL,  -- oos_risk, fraud_likelihood, churn_risk, demand_forecast
    target_entity_type VARCHAR(50),  -- item, employee, customer, location
    target_entity_id VARCHAR(255),

    -- Prediction output
    predicted_value DECIMAL(10,2),  -- Numeric prediction
    predicted_class VARCHAR(100),  -- Categorical prediction
    confidence_score DECIMAL(5,2),  -- 0-100

    -- Model metadata
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(20),
    features_used JSONB,  -- Array of feature names/values

    -- Time dimensions
    prediction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    prediction_horizon_days INTEGER,  -- How far into future (e.g., 7 days)

    -- Validation (when actual outcome is known)
    actual_value DECIMAL(10,2),
    actual_class VARCHAR(100),
    prediction_error DECIMAL(10,2),
    is_accurate BOOLEAN,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_prediction_type CHECK (prediction_type IN ('oos_risk', 'fraud_likelihood', 'churn_risk', 'demand_forecast', 'shrinkage_forecast'))
);

CREATE INDEX idx_owl_predictions_merchant ON owl_predictions(merchant_id, prediction_date DESC);
CREATE INDEX idx_owl_predictions_location ON owl_predictions(location_id, prediction_date DESC);
CREATE INDEX idx_owl_predictions_type ON owl_predictions(prediction_type, merchant_id);
CREATE INDEX idx_owl_predictions_target ON owl_predictions(target_entity_type, target_entity_id);
```

---

## Part 6: Goose - Bitcoin/Lightning Payments

### 6.1 Bitcoin Treasury

**Pattern:** Bitcoin treasury management (native to GrowDirect)

```sql
-- Bitcoin treasury (UTXO tracking)
CREATE TABLE goose_btc_treasury (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER REFERENCES merchants(id),  -- NULL = GrowDirect corporate treasury

    -- UTXO identification
    txid VARCHAR(64) NOT NULL,  -- Bitcoin transaction ID
    vout INTEGER NOT NULL,  -- Output index

    -- Amount
    amount_sats BIGINT NOT NULL,
    amount_btc DECIMAL(16,8) NOT NULL,

    -- Address
    address VARCHAR(100) NOT NULL,
    address_type VARCHAR(20),  -- p2pkh, p2wpkh, p2sh, p2wsh

    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'unspent',  -- unspent, spent, pending
    spent_txid VARCHAR(64),  -- Transaction that spent this UTXO
    spent_at TIMESTAMP,

    -- Classification
    utxo_type VARCHAR(50) NOT NULL,  -- subscription_payment, lightning_channel, cold_storage, operational

    -- Timestamps
    received_at TIMESTAMP NOT NULL,
    block_height INTEGER,
    confirmations INTEGER DEFAULT 0,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(txid, vout),
    CONSTRAINT chk_utxo_status CHECK (status IN ('unspent', 'spent', 'pending')),
    CONSTRAINT chk_utxo_type CHECK (utxo_type IN ('subscription_payment', 'lightning_channel', 'cold_storage', 'operational', 'routing_fees'))
);

CREATE INDEX idx_goose_treasury_merchant ON goose_btc_treasury(merchant_id);
CREATE INDEX idx_goose_treasury_status ON goose_btc_treasury(status) WHERE status = 'unspent';
CREATE INDEX idx_goose_treasury_address ON goose_btc_treasury(address);
CREATE INDEX idx_goose_treasury_txid ON goose_btc_treasury(txid, vout);
```

### 6.2 Lightning Network

**Pattern:** Lightning Network invoice and payment tracking

```sql
-- Lightning invoices (BTCPay Server integration)
CREATE TABLE goose_lightning_invoices (
    id BIGSERIAL PRIMARY KEY,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),

    -- BTCPay Server identifiers
    btcpay_invoice_id VARCHAR(255) UNIQUE NOT NULL,
    btcpay_store_id VARCHAR(255) NOT NULL,

    -- Invoice details
    amount_sats BIGINT NOT NULL,
    amount_usd_cents BIGINT,  -- USD equivalent at creation
    currency VARCHAR(3) DEFAULT 'SATS',

    -- Subscription linkage
    subscription_tier VARCHAR(50),  -- free, pro, enterprise
    billing_period VARCHAR(20),  -- monthly, annual

    -- Payment request
    payment_request TEXT,  -- BOLT11 invoice string
    payment_hash VARCHAR(64),

    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'pending',  -- pending, paid, expired, invalid

    -- Payment details (when paid)
    paid_at TIMESTAMP,
    preimage VARCHAR(64),  -- Lightning payment preimage
    fee_sats BIGINT,

    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,

    CONSTRAINT chk_ln_invoice_status CHECK (status IN ('pending', 'paid', 'expired', 'invalid', 'cancelled'))
);

CREATE INDEX idx_goose_lightning_merchant ON goose_lightning_invoices(merchant_id, created_at DESC);
CREATE INDEX idx_goose_lightning_status ON goose_lightning_invoices(status, merchant_id);
CREATE INDEX idx_goose_lightning_btcpay ON goose_lightning_invoices(btcpay_invoice_id);
CREATE INDEX idx_goose_lightning_hash ON goose_lightning_invoices(payment_hash);
```

---

## Part 7: Junction Tables (Many-to-Many Relationships)

**GSLM Pattern:** PackItemBreakout-style junction tables with metadata

### 7.1 Case-Subject Junction

```sql
-- Many-to-many: Cases can have multiple subjects, subjects can appear in multiple cases
CREATE TABLE fox_case_subjects (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT NOT NULL REFERENCES fox_cases(id) ON DELETE CASCADE,
    subject_id BIGINT NOT NULL REFERENCES fox_subjects(id) ON DELETE RESTRICT,

    -- Relationship metadata (GSLM junction pattern)
    role_in_case VARCHAR(100) NOT NULL,  -- primary_suspect, accomplice, witness, victim, reporting_party
    involvement_level VARCHAR(50),  -- high, medium, low

    -- GSLM effective dating
    effective_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,

    -- Notes specific to this relationship
    relationship_notes TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),

    UNIQUE(case_id, subject_id),
    CONSTRAINT chk_role_in_case CHECK (role_in_case IN ('primary_suspect', 'accomplice', 'witness', 'victim', 'reporting_party', 'other'))
);

CREATE INDEX idx_fox_case_subjects_case ON fox_case_subjects(case_id);
CREATE INDEX idx_fox_case_subjects_subject ON fox_case_subjects(subject_id);
CREATE INDEX idx_fox_case_subjects_role ON fox_case_subjects(role_in_case);
```

### 7.2 Evidence-Case Junction

```sql
-- Many-to-many: Evidence can be linked to multiple cases (organized crime, related incidents)
CREATE TABLE fox_evidence_cases (
    id BIGSERIAL PRIMARY KEY,
    evidence_id BIGINT NOT NULL REFERENCES fox_evidence(id) ON DELETE RESTRICT,
    case_id BIGINT NOT NULL REFERENCES fox_cases(id) ON DELETE CASCADE,

    -- Relationship metadata
    relevance VARCHAR(50) NOT NULL,  -- primary, supporting, background
    relevance_description TEXT,

    -- Who linked it and when
    linked_by INTEGER NOT NULL REFERENCES users(id),
    linked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(evidence_id, case_id),
    CONSTRAINT chk_relevance CHECK (relevance IN ('primary', 'supporting', 'background', 'tangential'))
);

CREATE INDEX idx_fox_evidence_cases_evidence ON fox_evidence_cases(evidence_id);
CREATE INDEX idx_fox_evidence_cases_case ON fox_evidence_cases(case_id);
```

### 7.3 Alert-Case Junction

```sql
-- Many-to-many: Alerts can trigger cases, cases can reference multiple alerts
CREATE TABLE canary_alert_cases (
    id BIGSERIAL PRIMARY KEY,
    alert_id BIGINT NOT NULL REFERENCES alerts(id) ON DELETE RESTRICT,
    case_id BIGINT NOT NULL REFERENCES fox_cases(id) ON DELETE CASCADE,

    -- How alert relates to case
    relationship_type VARCHAR(50) NOT NULL,  -- triggering_alert, related_pattern, supporting_evidence

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id),

    UNIQUE(alert_id, case_id),
    CONSTRAINT chk_relationship_type CHECK (relationship_type IN ('triggering_alert', 'related_pattern', 'supporting_evidence'))
);

CREATE INDEX idx_alert_cases_alert ON canary_alert_cases(alert_id);
CREATE INDEX idx_alert_cases_case ON canary_alert_cases(case_id);
```

---

## Part 8: Cross-Product Data Flows

### 8.1 Canary → Fox Integration

**Flow:** Alert detection triggers case creation

```
Square Transaction Data
         ↓
    Canary Detection
         ↓
    Alert Generated (alerts table)
         ↓
    [If severity = high/critical AND employee_id present]
         ↓
    Fox Case Auto-Created (fox_cases)
         ↓
    Subject Record Created/Updated (fox_subjects)
         ↓
    Alert Linked to Case (canary_alert_cases junction)
         ↓
    Timeline Event Created (fox_timeline_events)
```

**Implementation:** Trigger or application-level logic in Canary detection engine.

### 8.2 Owl → Canary/Fox Integration

**Flow:** Analytics predictions feed back into detection and case prioritization

```
Owl Prediction Model
         ↓
    Risk Score Calculated (owl_predictions)
         ↓
    [If prediction_type = fraud_likelihood AND confidence > 80%]
         ↓
    Update Subject Threat Score (fox_subjects.threat_score)
         ↓
    Prioritize Active Alerts (alerts.risk_score updated)
         ↓
    Dashboard Surfaces High-Risk Subjects
```

### 8.3 Goose → All Products Integration

**Flow:** Bitcoin subscription payments unlock product access

```
BTCPay Lightning Invoice Created
         ↓
    Invoice Paid (goose_lightning_invoices.status = 'paid')
         ↓
    Merchant Subscription Tier Updated (merchants table)
         ↓
    Quota Limits Adjusted (canary/billing module)
         ↓
    Access Granted to Owl Analytics Dashboard
         ↓
    Fox Case Management Unlocked (if Enterprise tier)
```

---

## Part 9: GSLM Pattern Implementation Summary

### 9.1 GSLM Patterns Applied

| GSLM Pattern | GrowDirect Implementation | Tables Using Pattern |
|--------------|---------------------------|----------------------|
| **Effective Dating** | All major entities have effective_date + expiry_date | merchants, locations, fox_cases, fox_subjects, fox_evidence |
| **Hierarchical Relationships** | Parent/child relationships with hierarchy_level | merchants (franchise), fox_subjects (crime networks), locations (market/region/division) |
| **Many-to-Many Junctions** | Junction tables with relationship metadata | fox_case_subjects, fox_evidence_cases, canary_alert_cases |
| **Status Tracking** | Lifecycle status with constrained values | ALL tables (active/inactive, open/closed, etc.) |
| **Attribute Localization** | JSONB fields for flexible attributes | transaction.raw_data, alert.metadata, owl_predictions.features_used |
| **Temporal Validity** | Effective dating tracks entity history over time | Supports "as-of" queries for historical reporting |
| **6-Level Hierarchy** | Market → Region → Division → Store (4 levels sufficient for SMB) | locations table |
| **Versioning** | Track changes with version_number + previous_version_id | fox_evidence (chain of evidence versions) |

### 9.2 Walmart/CRDM Patterns Applied

| Walmart/CRDM Pattern | GrowDirect Implementation | Business Value |
|----------------------|---------------------------|----------------|
| **SRA Scorecards** | Analytics snapshots with geographic rollup | Executive dashboards like Walmart SRA |
| **Exception-Based Reporting** | Alerts table with severity classification | Real-time fraud detection |
| **Case Management Workflow** | Fox case lifecycle (open → investigating → closed) | Structured investigation process |
| **Subject Profiles** | Fox subjects with risk scoring | Threat intelligence database |
| **Chain of Custody** | Evidence table with custody log | Legal admissibility |
| **POS Aggregation** | Transaction + transaction_items structure | CRDM-style data model |
| **Control Tables** | Permissions, role_permissions, merchant_settings | GSLM Controls/Parameters equivalent |

---

## Part 10: Implementation Recommendations

### 10.1 Phased Rollout

**Phase 1: Core Foundation (Months 1-2)**
- Implement shared/core tables: merchants, locations, users, permissions, audit_log
- Build Canary tables: transactions, transaction_items, alerts
- Test Square integration end-to-end

**Phase 2: Fox Case Management (Months 3-4)**
- Implement Fox tables: cases, subjects, evidence, timeline_events
- Build junction tables for case-subject-evidence relationships
- Integrate Canary alerts → Fox cases workflow

**Phase 3: Owl Analytics (Months 5-6)**
- Implement Owl tables: analytics_snapshots, predictions
- Build ETL pipeline for aggregation
- Deploy TimescaleDB for time-series optimization

**Phase 4: Goose Payments (Month 7)**
- Implement Goose tables: btc_treasury, lightning_invoices
- Integrate BTCPay Server webhooks
- Connect subscription tier management

### 10.2 Data Migration Strategy

**From SQLite (MVP) to PostgreSQL (Production):**

1. **Export schema from SQLite** → Convert to PostgreSQL DDL
2. **Migrate existing merchants/users** → Preserve IDs with SERIAL starting values
3. **Re-sync Square transaction data** → Historical backfill (30-90 days)
4. **Recreate alerts** → Re-run detection algorithms on historical data
5. **Validate data integrity** → Row counts, foreign key validation

### 10.3 Performance Optimization

**Indexing Strategy:**
- **B-tree indexes** on foreign keys, status columns, date ranges
- **Partial indexes** on filtered queries (e.g., WHERE status = 'active')
- **Composite indexes** on common query patterns (merchant_id + date)
- **GIN indexes** on JSONB columns for metadata search

**Partitioning:**
- **Transactions table**: Partition by transaction_date (monthly partitions)
- **Audit_log**: Partition by timestamp (quarterly partitions)
- **Analytics_snapshots**: Use TimescaleDB hypertables (automatic partitioning)

**Caching:**
- **Redis** for merchant settings, user sessions, alert counts
- **Materialized views** for slow aggregations (daily refresh)

---

## Part 11: Security & Compliance

### 11.1 Data Encryption

**At Rest:**
- PII fields encrypted using pgcrypto (AES-256)
- Square access tokens encrypted
- Evidence files encrypted on disk (S3 server-side encryption)

**In Transit:**
- TLS 1.3 for all API calls
- Square SDK uses HTTPS
- BTCPay Server uses SSL certificates

### 11.2 Access Controls

**Row-Level Security (RLS):**
- Enable PostgreSQL RLS on all tenant tables
- Policy: Users can only access rows WHERE merchant_id = current_user.merchant_id
- Admin override for GrowDirect corporate access

**Audit Logging:**
- ALL write operations logged to audit_log
- Includes IP address, user agent, request path
- Hash-chained for tamper detection

### 11.3 Compliance Frameworks

**GDPR/CCPA:**
- Data retention policies (fox_subjects.data_retention_date)
- Right to erasure (soft delete + scheduled purge)
- Data portability (export API endpoints)

**SOX (for future enterprise customers):**
- Immutable audit trails
- Role-based access control
- Financial transaction reconciliation

---

## Part 12: Next Steps for Jeremy & Tom

### Tom's Responsibilities:
1. **Review this spec with Jeffe/Alex** - strategic alignment check
2. **Validate GSLM pattern applications** - ensure retail correctness
3. **Create entity-relationship diagrams** - visual documentation
4. **Define data dictionary** - column-level documentation

### Jeremy's Responsibilities:
1. **Create PostgreSQL migration scripts** - DDL for all tables
2. **Build Alembic migrations** - version-controlled schema changes
3. **Implement SQLAlchemy models** - Python ORM layer
4. **Write integration tests** - validate foreign keys, constraints

### Joint Deliverables:
1. **Data flow documentation** - sequence diagrams for key workflows
2. **Performance benchmarks** - test with 1M+ transactions
3. **Backup/recovery procedures** - operational runbook
4. **API documentation** - REST endpoints for each entity

---

## Appendix A: Table Summary

| Product | Table Count | Primary Tables |
|---------|-------------|----------------|
| **Shared/Core** | 6 | merchants, locations, users, permissions, role_permissions, audit_log |
| **Canary** | 3 | transactions, transaction_items, alerts |
| **Fox** | 5 | fox_cases, fox_subjects, fox_evidence, fox_timeline_events, fox_case_subjects |
| **Owl** | 2 | owl_analytics_snapshots, owl_predictions |
| **Goose** | 2 | goose_btc_treasury, goose_lightning_invoices |
| **Junctions** | 2 | fox_evidence_cases, canary_alert_cases |
| **Settings** | 1 | merchant_settings |
| **TOTAL** | **21 tables** | Full platform data model |

---

## Appendix B: GSLM vs. GrowDirect Comparison

| GSLM Entity | GrowDirect Equivalent | Notes |
|-------------|----------------------|-------|
| GSLM Item | transaction_items | Simplified for SMB (no 6-level hierarchy needed) |
| GSLM Location | locations | 4-level hierarchy (market/region/division/store) |
| GSLM Customer | Future Vignette CRM module | Not in scope for Fox/Canary MVP |
| GSLM People | users, fox_subjects | Split into system users vs. investigation subjects |
| GSLM Finance | Goose (Bitcoin treasury) | Blockchain-native replacement for traditional GL |
| GSLM Supply Chain | Future Inventory Intelligence | Phase 3 roadmap |
| GSLM Controls | permissions, merchant_settings | RBAC + configuration |

---

**END OF SPECIFICATION**

---

**Document Status:** Draft for Review
**Next Review:** February 18, 2026 with Alex & Jeffe
**Implementation Start:** February 19, 2026 (Jeremy + Tom pairing)
**Target Completion:** March 31, 2026 (Fox + Owl MVP)

---

*"Build once what Fortune 500 retailers spent decades perfecting. Package it for the 33M SMB retailers who can't afford enterprise solutions. That's the GrowDirect mission."*

— Tom & Jeremy
