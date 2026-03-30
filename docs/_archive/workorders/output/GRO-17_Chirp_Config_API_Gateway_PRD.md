---
type: workorder
domain: chirp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-17 — Chirp Config + API Gateway PRD

**Issue:** GRO-17 (B-034)
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** Internal — Product Requirements Document
**Gate:** Jeremy estimates effort. Art designs Config page mockup. Jim writes test plan.
**Done When:** PRD written, effort estimated, design mockup exists.
**Scope:** Planning only. No build.

---

## 1. Problem Statement

Canary LP's Chirp detection engine currently has 22 rules (C-001 to C-602) with hard-coded thresholds. A merchant running a high-volume coffee shop has fundamentally different normal patterns than a boutique clothing store. The "5 refunds/employee/day" threshold (C-101) that triggers `HIGH_REFUND_RATE` might be noise for a 500-transaction/day location but a critical signal for a 20-transaction/day location.

Per the North Star: *"We don't want to add to the stress. We want to ease it."* A loss prevention system that generates false positives because thresholds aren't tuned to the merchant's actual patterns adds stress instead of reducing it.

Additionally, Canary LP needs an API gateway to support:
- Future third-party integrations (RaaS API consumers)
- Mobile app access (merchant on-the-go)
- Webhook delivery to merchant-specified endpoints (alert forwarding)
- Rate limiting and authentication for all external access

---

## 2. What We're Building

Two capabilities, tightly coupled:

### 2A. Chirp Configuration UI
A merchant-facing settings page where authorized users (owner/admin role) can view and adjust Chirp detection thresholds for their locations.

### 2B. API Gateway
A centralized API layer that sits between all external consumers and Canary's internal services.

---

## 3. Chirp Configuration — Requirements

### 3.1 User Stories

**US-1:** As a merchant owner, I want to see all active Chirp rules and their current thresholds so I understand what Canary is monitoring.

**US-2:** As a merchant owner, I want to adjust thresholds per-location so that my high-volume downtown store has different sensitivity than my quiet suburban store.

**US-3:** As a merchant admin, I want to enable/disable individual Chirp rules per-location so I can suppress rules that aren't relevant to my business (e.g., disable gift card rules if I don't sell gift cards).

**US-4:** As a merchant owner, I want to see recommended thresholds based on my actual transaction patterns so I don't have to guess what "normal" is.

**US-5:** As a merchant owner, I want to disable any Chirp rule that isn't relevant to my business, with the understanding that all rules default to enabled and Canary surfaces a health indicator showing how many rules I've turned off.

**US-6:** As a merchant owner, I want to see whether each rule applies globally (all locations) or to a specific location, and I want to set scope when configuring — so a cash variance rule can be location-specific while a refund policy rule applies merchant-wide.

**US-7:** As the Canary system, I want to enforce min/max bounds on threshold values so merchants can't set nonsensical values (e.g., 0 refunds/day), while still allowing them to disable the rule entirely if they choose.

### 3.2 Chirp Rules Configuration Spec

The 22 Chirp rules from CRDM v1.0. All rules default to **enabled**. Merchants can disable any rule. Each rule has a **default scope** (global = all locations, or location = per-location config expected):

| Rule ID | Rule Name | Default Threshold | Default Scope | Threshold Adjustable? | Min | Max | Unit |
|---------|-----------|-------------------|---------------|----------------------|-----|-----|------|
| C-001 | `HIGH_REFUND_RATE` | 5/employee/day | Global | YES | 1 | 50 | count/employee/day |
| C-002 | `EXCESSIVE_DISCOUNT` | >20% of line total | Global | YES | 5% | 50% | percentage |
| C-003 | `REFUND_WITHOUT_RETURN` | any (fires on occurrence) | Global | NO (boolean) | — | — | boolean |
| C-004 | `SAME_CARD_REFUND_PATTERN` | 3 refunds/card/7days | Global | YES | 1 | 20 | count/card/period |
| C-005 | `SPLIT_TENDER_ANOMALY` | >3 tenders/transaction | Global | YES | 2 | 10 | count/transaction |
| C-101 | `EXCESSIVE_DISCOUNT_EMPLOYEE` | >$50 total discounts/shift | Location | YES | $10 | $500 | currency/shift |
| C-102 | `SELECTIVE_SCANNING` | >10% void rate on line items | Location | YES | 2% | 30% | percentage |
| C-201 | `CASH_VARIANCE` | >$10 over/short at close | Location | YES | $1 | $100 | currency |
| C-202 | `EXCESSIVE_PAID_OUT` | >3 paid-outs/shift | Location | YES | 1 | 20 | count/shift |
| C-203 | `HIGH_NO_SALE_FREQUENCY` | >5 no-sales/shift | Location | YES | 1 | 30 | count/shift |
| C-301 | `OFF_CLOCK_TRANSACTION` | any (fires on occurrence) | Global | NO (boolean) | — | — | boolean |
| C-302 | `BREAK_TRANSACTION` | any (fires on occurrence) | Global | NO (boolean) | — | — | boolean |
| C-303 | `WRONG_LOCATION_ACTIVITY` | any (fires on occurrence) | Global | NO (boolean) | — | — | boolean |
| C-401 | `HIGH_VOID_RATE` | >5 voids/employee/day | Location | YES | 1 | 50 | count/employee/day |
| C-402 | `POST_VOID_ALERT` | any (fires on occurrence) | Global | NO (boolean) | — | — | boolean |
| C-501 | `SHRINKAGE_SPIKE` | >2% variance in category | Location | YES | 0.5% | 10% | percentage |
| C-502 | `MANUAL_ADJUSTMENT_VELOCITY` | >3 manual adj/day | Location | YES | 1 | 20 | count/day |
| C-601 | `GIFT_CARD_LOAD_VELOCITY` | >5 loads/employee/day | Location | YES | 1 | 30 | count/employee/day |
| C-602 | `RETURN_TO_GIFT_CARD` | any (fires on occurrence) | Global | NO (boolean) | — | — | boolean |

**Key design decisions:**

- **All rules default to enabled.** Merchants can disable any rule — including boolean rules like POST_VOID_ALERT. Their choice, their risk. Canary surfaces a "Detection Health" indicator: "17/22 rules active" with a warning if critical rules are off.
- **Scope = Global vs. Location.** Global rules apply the same config to all locations. Location-scoped rules expect per-location tuning (volume-dependent thresholds). Merchants can override the default scope — e.g., set a refund policy as location-specific if their downtown store has a different return policy.
- **Boolean rules have no threshold to adjust** but can still be enabled/disabled and scoped. When enabled, they fire on every occurrence.
- **Threshold-adjustable rules (16):** Merchant can adjust value within min/max bounds. Changes logged to `audit_log` with hash chain integrity.
- **Resolution order:** Location override → Merchant global override → System default. If a rule is set to Global scope, there are no location overrides — the merchant-level setting applies everywhere.

### 3.3 Data Model Extension

The existing `canary_app.detection_rules` table needs augmentation:

```sql
-- Existing table, extended
CREATE TABLE canary_app.detection_rule_overrides (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  merchant_id UUID NOT NULL REFERENCES merchants(id),
  location_id UUID REFERENCES locations(id),  -- NULL = merchant-wide (global scope)
  rule_id TEXT NOT NULL,                       -- e.g., 'C-001'
  scope TEXT NOT NULL DEFAULT 'global' CHECK (scope IN ('global', 'location')),
  threshold_value NUMERIC,                     -- NULL for boolean rules
  threshold_unit TEXT,                          -- NULL for boolean rules
  enabled BOOLEAN NOT NULL DEFAULT true,
  changed_by UUID NOT NULL REFERENCES users(id),
  change_reason TEXT,
  previous_value NUMERIC,
  previous_enabled BOOLEAN,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  record_hash TEXT NOT NULL,
  previous_hash TEXT
);

-- Index: merchant + rule lookup
CREATE INDEX idx_rule_overrides_merchant_rule
  ON detection_rule_overrides(merchant_id, rule_id, location_id);

-- Constraint: global-scoped rules should not have location_id set
ALTER TABLE detection_rule_overrides
  ADD CONSTRAINT chk_scope_location
  CHECK (
    (scope = 'global' AND location_id IS NULL)
    OR (scope = 'location')
  );
```

**Resolution order:** Location override → Merchant global override → System default. If `scope = 'global'`, the merchant-level setting applies to all locations (no per-location rows created).

### 3.4 Baseline Recommendations (US-4)

Canary should compute recommended thresholds from the merchant's actual data:

```
recommended_threshold = mean + (2 × std_dev)
```

Using `canary_metrics.metric_baselines` (already exists in CRDM). The Config UI shows:
- Current threshold (what's active)
- Recommended threshold (computed from 30-day baseline)
- System default (the hard-coded value from the table above)

This is the "guided, not dashboard" philosophy — we tell them what's normal for their business, not just show them knobs.

### 3.5 UX Brief for Art

**Page:** Settings → Detection Rules (or "Chirp Settings" in merchant-facing language)

**Layout concept:**
- Card-per-rule-category (Refund/Discount, Cash Handling, Employee Timing, Void/Post-Void, Inventory, Gift Card)
- Each card expands to show individual rules with slider + number input
- Every rule has an enable/disable toggle (default: on). Disabled rules show grayed with "Off" badge
- Boolean rules (no threshold) show as "Fires on occurrence" with just the enable toggle
- Scope indicator per rule: "All Locations" (global) or location picker dropdown (location-scoped)
- "Detection Health" banner at top: "17/22 rules active" — turns amber if <15, red if <10
- "Reset to Recommended" button per rule and per category
- Change preview: "If you lower this from 5 to 3, you would have seen 12 additional alerts last week"
- Guided onboarding: first-time setup walks through each category with recommendations

**Art:** Please create wireframe mockup. Priority: mobile-first (merchants check from their phone). Reference Canary's existing design system.

---

## 4. API Gateway — Requirements

### 4.1 Architecture

```
Internet
  │
  ▼
┌─────────────────────────────┐
│  API Gateway (Kong / custom) │
│  - Rate limiting             │
│  - Auth (JWT + L402)         │
│  - Request validation        │
│  - Tenant context injection  │
│  - Logging                   │
└─────────────────────────────┘
  │          │          │
  ▼          ▼          ▼
Canary    RaaS       Webhook
  API     API        Delivery
(internal) (external)  (outbound)
```

### 4.2 Authentication Layers

| Consumer | Auth Method | Rate Limit | Notes |
|----------|------------|------------|-------|
| Canary web app | JWT (merchant session) | 100 req/min | Standard merchant access |
| Canary mobile app | JWT (merchant session) | 60 req/min | Lower limit for mobile |
| RaaS API consumers | L402 (Lightning micropayment) | 1000 req/min | Per-API-key, pay-per-call |
| Square webhooks (inbound) | HMAC signature verification | Unlimited | Square controls the rate |
| Merchant webhook delivery (outbound) | API key per endpoint | 10 req/min per endpoint | Canary → merchant systems |

### 4.3 Internal API Endpoints (Canary App)

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/dashboard` | GET | Home/Canary module data | JWT |
| `/api/alerts` | GET | Active alerts for merchant | JWT |
| `/api/alerts/:id/acknowledge` | POST | Acknowledge an alert | JWT (admin+) |
| `/api/detection-rules` | GET | Current Chirp config | JWT |
| `/api/detection-rules` | PATCH | Update threshold/enable | JWT (owner/admin) |
| `/api/employees` | GET | Employee list with risk scores | JWT |
| `/api/transactions` | GET | Transaction search | JWT |
| `/api/cases` | GET/POST | Fox investigation module | JWT (admin+) |
| `/api/metrics/daily` | GET | Daily metrics summary | JWT |
| `/api/webhooks/config` | GET/POST | Merchant webhook endpoints | JWT (owner) |

### 4.4 External API Endpoints (RaaS — Future)

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/verify` | POST | Verify receipt hash against inscription | L402 |
| `/receipt/:name` | GET | Retrieve receipt history by .jeffe name | L402 |

These are defined in PhD's B-077 RaaS Manifesto Section IV.3.1. Implementation deferred until RaaS strategic reframe (GRO-13) is resolved.

### 4.5 Gateway Technology Decision

**Options under evaluation:**

| Option | Pros | Cons | Effort |
|--------|------|------|--------|
| **Kong (open source)** | Battle-tested, plugin ecosystem, L402 plugin feasible | Heavyweight for MVP, Lua plugin development | Medium |
| **Express.js middleware** | Already in stack (if Node.js), simple, fast to implement | No built-in rate limiting, auth, or logging | Low (but grows) |
| **Caddy + custom middleware** | Lightweight, automatic HTTPS, extensible | Less community support for API gateway patterns | Medium |
| **Custom Go gateway** | Maximum performance, custom L402 integration | Build from scratch, maintenance burden | High |

**Recommendation for Tom:** Express.js middleware for MVP (Canary app API only). Migrate to Kong when RaaS API goes live and external consumers need production-grade rate limiting. The gateway is a routing + auth layer, not application logic.

---

## 5. Effort Estimation Framework (for Jeremy)

### Chirp Config

| Component | Estimate | Dependencies |
|-----------|----------|--------------|
| `detection_rule_overrides` table + migrations | 0.5 days | GRO-18 (multi-tenant decision) |
| API endpoints (GET/PATCH detection rules) | 1 day | Auth middleware |
| Threshold resolution logic (location → merchant → default) | 0.5 days | — |
| Baseline recommendation computation | 1 day | `metric_baselines` populated |
| "Impact preview" query (alerts last 7 days with new threshold) | 1 day | Alert history |
| **Subtotal** | **4 days** | |

### API Gateway (MVP)

| Component | Estimate | Dependencies |
|-----------|----------|--------------|
| Express.js middleware setup (auth, rate limit, logging) | 1 day | — |
| JWT auth for merchant sessions | 1 day | User/session model |
| Tenant context injection (`SET app.current_merchant_id`) | 0.5 days | GRO-18 |
| Rate limiting (in-memory for MVP, Redis later) | 0.5 days | — |
| Request validation middleware | 0.5 days | — |
| Internal API endpoint scaffolding (10 endpoints) | 2 days | Models exist |
| **Subtotal** | **5.5 days** | |

### Art Design

| Component | Estimate |
|-----------|----------|
| Chirp Config wireframe (mobile-first) | 2 days |
| Guided onboarding flow mockup | 1 day |
| **Subtotal** | **3 days** |

**Total estimated effort: ~12.5 days (roughly 2.5 sprint weeks)**

Jeremy: Please review and adjust. These are ALX estimates based on CRDM complexity, not your assessment of the actual codebase.

---

## 6. Acceptance Criteria

1. Merchant owner can view all 22 Chirp rules with current thresholds, scope (global/location), and enabled state
2. Merchant owner can adjust configurable rules within min/max bounds
3. Merchant owner can enable/disable any rule (including boolean rules). All default to enabled
4. Each rule displays whether it applies globally or per-location. Merchant can set scope
3. Non-configurable rules display as "Always Active" and cannot be modified
4. Per-location overrides work correctly (location > merchant > default resolution)
5. Baseline recommendations computed from 30-day data display alongside current thresholds
6. All threshold changes logged to audit_log with hash chain integrity
7. API gateway enforces JWT authentication on all Canary endpoints
8. Rate limiting prevents > 100 req/min per merchant session
9. Jim: Write QA plan covering cross-tenant isolation, threshold boundary testing, and audit log integrity

---

## 7. Routing

- **Jeremy:** Review effort estimates, flag anything that's off by >2x
- **Art:** Chirp Config wireframe — mobile-first, guided onboarding, "impact preview" interaction
- **Tom:** API gateway technology decision — confirm Express.js for MVP or propose alternative
- **Jim:** QA plan for threshold configuration + API gateway auth testing
- **Syd:** No legal gate on this PRD unless threshold configuration creates liability (e.g., merchant lowers thresholds, misses fraud, blames Canary)

---

*ALX | GRO-17 | March 2, 2026*
