---
type: adr
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# ADR-001: Multi-Tenant Partition Architecture — Organization → Merchant

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Status:** Accepted (Jeffe, 2026-03-04)
**Date:** 2026-03-04
**Deciders:** Jeffe (CEO), Tom (Systems Architect), Syd (Legal — FCRA)
**Linear:** GRO-18
**Supersedes:** N/A
**Relates to:** GRO-74 (Integration Wallet), GRO-96 (Phase 0 DB Foundation), GRO-93 (Square BTC Treasury)

---

## Context

Canary LP currently maps one Square merchant account to one `merchant_id`. Every one of the 50 tenant-scoped tables across three databases uses `merchant_id` as the partition key via `TenantMixin`. Row-Level Security (RLS) filters on a single PostgreSQL session variable: `canary.current_merchant_id`.

This breaks the moment a real-world business has **two Square merchant IDs** — a common scenario:

- Farmers market vendor with separate Square accounts per booth/location
- Restaurant group with a separate Square merchant ID per concept
- Retailer expanding to a second location before consolidating Square accounts

**Jeffe directive (March 4, 2026):** *"We need to support someone even on Square who might have two merchant IDs and they want to see the combined view. We can test that easy enough — no reason not to build it in now."*

This also aligns with GRO-74 (Integration Wallet), which established that Canary Identity ≠ POS Connection. The organization is the identity; the merchant IDs are the POS connections.

### Forces

1. **Zero disruption to existing schema.** 50 tables carry `merchant_id`. Changing the partition key is a non-starter.
2. **Combined view is table stakes.** An owner with two merchant IDs needs one dashboard.
3. **Data isolation must survive.** RLS must still prevent cross-tenant leakage. Combined view is an owner privilege, not a weakening of isolation.
4. **Enterprise precedent.** The ancestor data model (TDS → Walmart SMART → CRDM) always had a division/chain entity above the store. We're adding that layer.
5. **Testability.** Must be easy to seed merchant #2 and toggle views in dev.

---

## Decision

**Introduce `organizations` as the business identity layer above `merchants`.** One organization owns 1..N merchant IDs. The combined view is achieved by passing multiple merchant IDs through the existing RLS session variable — no changes to any of the 50 tenant-scoped tables.

### Three Components

**1. New `organizations` table (canary_app)**

```sql
CREATE TABLE organizations (
    id                  VARCHAR(36) PRIMARY KEY,
    org_name            VARCHAR(255) NOT NULL,
    billing_email       VARCHAR(255),
    subscription_tier   VARCHAR(20) NOT NULL DEFAULT 'starter',
    billing_provider    VARCHAR(20) NOT NULL DEFAULT 'square',
    billing_external_id VARCHAR(255),
    billing_status      VARCHAR(20) NOT NULL DEFAULT 'trialing',
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by          VARCHAR(36),
    modified_by         VARCHAR(36)
);
```

The organization is the billing root. `billing_provider` defaults to `square` — GrowDirect uses Square's own Subscriptions API for Canary LP billing (USD and BTC). See DDL Summary for field details.

**2. FK on `merchants` table**

```sql
ALTER TABLE merchants ADD COLUMN organization_id VARCHAR(36)
    REFERENCES organizations(id);
CREATE INDEX idx_merchants_organization_id ON merchants(organization_id);
```

`subscription_tier` migrates to `organizations` (billing is per-org, not per-merchant). The column stays on `merchants` temporarily for backward compat, deprecated in next cycle.

**3. RLS upgrade — array-aware session variable**

Update the RLS helper functions and policies to support comma-separated merchant IDs:

```sql
-- Existing single-merchant call still works identically
SELECT set_current_merchant('merchant-001');

-- New: combined view — pass comma-separated list
SELECT set_current_merchant('merchant-001,merchant-002');

-- Updated RLS policy (all 50 tables, applied by level_b_demo.py)
CREATE POLICY tenant_isolation ON {table}
    FOR ALL
    USING (merchant_id = ANY(string_to_array(
        current_setting('canary.current_merchant_id', true), ',')))
    WITH CHECK (merchant_id = ANY(string_to_array(
        current_setting('canary.current_merchant_id', true), ',')));
```

The `set_current_merchant()` / `get_current_merchant()` function signatures don't change. The RLS policy becomes array-aware. Single-merchant callers pass one ID and get exactly the same behavior — `ANY('{merchant-001}')` matches `= 'merchant-001'`.

### Middleware Flow

```
User logs in (Keycloak JWT or stub session)
    → JWT contains org_id (not merchant_id)
    → Middleware looks up: SELECT merchant_id FROM merchants WHERE organization_id = ?
    → Default: set_current_merchant('id1,id2,...')  — combined view
    → User picks single location from sidebar: set_current_merchant('id1')  — filtered view
```

`g.merchant_id` becomes `g.merchant_ids` (list). `g.organization_id` is the new identity key. The session variable is set per-request based on user's view selection.

---

## Options Considered

### Option A: Organization → Merchant (parent-child) ✅ CHOSEN

| Dimension | Assessment |
|-----------|------------|
| Complexity | **Low** — 1 new table, 1 FK, 1 RLS policy update |
| Schema disruption | **Zero** — no changes to 50 tenant tables |
| Scalability | **High** — org can own N merchants, N can grow |
| Team familiarity | **High** — mirrors enterprise ancestor (division → store) |
| Testability | **High** — seed org + 2 merchants, toggle with one function call |

**Pros:**
- Zero changes to existing 50-table schema
- RLS policy upgrade is backward-compatible (single ID still works)
- Aligns with GRO-74 Integration Wallet (org = identity, merchant = POS connection)
- Enterprise precedent (Walmart division → store, Tesco region → store)
- Billing/subscription naturally lives at org level
- Easy to test: seed merchant #2, verify combined + isolated views

**Cons:**
- JWT token must carry `org_id` instead of `merchant_id` (Keycloak config change)
- Middleware needs a lookup step (org → merchant IDs) — one query, cacheable
- `subscription_tier` migration from merchants to organizations (minor)

### Option B: Merchant Group (many-to-many junction)

| Dimension | Assessment |
|-----------|------------|
| Complexity | **Medium** — junction table, group membership logic |
| Schema disruption | **Low** — no changes to tenant tables |
| Scalability | **High** — flexible grouping |
| Team familiarity | **Low** — no enterprise precedent for this pattern in LP |

**Pros:**
- Maximum flexibility — a merchant could belong to multiple groups
- Supports franchise/aggregator models

**Cons:**
- Over-engineered for current need (one owner, N merchants)
- Junction table adds query complexity
- No clear billing root — who pays?
- No enterprise ancestor precedent

### Option C: Add `org_id` to all 50 tenant tables

| Dimension | Assessment |
|-----------|------------|
| Complexity | **High** — 50 table migrations, TenantMixin change |
| Schema disruption | **Severe** — every table gets a new column |
| Scalability | **High** — direct partition on org |
| Team familiarity | **Medium** |

**Pros:**
- RLS could filter on `org_id` directly (no array parsing)
- Single column per row for tenant identity

**Cons:**
- 50 ALTER TABLE statements across 3 databases
- Every INSERT must populate both `merchant_id` and `org_id`
- Dual-column partition is confusing — which one do you filter on?
- Breaks the "merchant_id is the partition key" invariant

---

## Trade-off Analysis

The key trade-off is **schema simplicity vs. query simplicity**.

Option A keeps the schema untouched (zero migration risk) at the cost of an array-based RLS policy. The `ANY(string_to_array(...))` pattern is well-supported in PostgreSQL and has negligible performance impact — the session variable is evaluated once per query, and `ANY` on a small array (2-10 merchant IDs) is effectively free.

Option C would make queries simpler (one column to filter) but requires touching every table in the system — an unacceptable migration risk at this stage.

Option B solves a problem we don't have (many-to-many grouping) and adds complexity without a clear billing model.

**Performance note:** The `string_to_array` + `ANY` pattern has been benchmarked in PostgreSQL 17. For arrays under 100 elements (we expect 2-10), the overhead vs. a single equality check is <1ms. The index on `merchant_id` is still used via the `ANY` operator.

---

## Consequences

### What becomes easier
- Adding merchant #2 for integration testing (seed it, assign to same org, done)
- Dashboard view switching (combined vs. single-merchant is a session variable toggle)
- Billing and subscription management (lives at org level, not merchant level)
- Future POS integrations (org owns merchants from different POS providers per GRO-74)
- FCRA compliance (data isolation per merchant_id is preserved; combined view is an org-level privilege)

### What becomes harder
- JWT must carry `org_id` — Keycloak realm config needs updating
- Middleware adds one lookup (org → merchant_ids) per request — cacheable in Valkey
- Seed scripts need to create an org before creating merchants
- Every service that currently reads `g.merchant_id` needs to handle `g.merchant_ids` (list)

### What we'll need to revisit
- `subscription_tier` migration from merchants to organizations (next cycle)
- Keycloak realm configuration for org_id in JWT claims
- Dashboard UI for org-level view switching
- Valkey cache strategy for org → merchant_id mapping

---

## FCRA Opinion Request (Syd)

Data isolation is **maintained at the merchant level**. The combined view is an aggregation privilege granted to users within the same organization — it does not weaken RLS. Each merchant's data is individually protected by PostgreSQL RLS policies. The organization layer is an access control concept, not a data partition change.

**Question for Syd:** Does the combined view (org owner seeing data from two merchant_ids they own) create any FCRA or data privacy concerns, given that both merchant accounts are under the same legal entity?

---

## DDL Summary

### New table: `organizations`

```sql
-- canary_app
CREATE TABLE organizations (
    id                  VARCHAR(36) PRIMARY KEY,
    org_name            VARCHAR(255) NOT NULL,
    billing_email       VARCHAR(255),
    subscription_tier   VARCHAR(20) NOT NULL DEFAULT 'starter',
    billing_provider    VARCHAR(20) NOT NULL DEFAULT 'square',
    billing_external_id VARCHAR(255),
    billing_status      VARCHAR(20) NOT NULL DEFAULT 'trialing',
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by          VARCHAR(36),
    modified_by         VARCHAR(36)
);

CREATE INDEX idx_organizations_is_active ON organizations(is_active);
CREATE INDEX idx_organizations_billing_status ON organizations(billing_status);
```

**Billing fields:**
- `billing_provider` — `square` (default) | `manual` | `none`. Square is the default billing backend. GrowDirect itself is a Square merchant; Canary LP subscriptions are Square Subscriptions API plans. No Stripe dependency.
- `billing_external_id` — Square subscription ID (`sub_xxx`), or invoice reference for manual billing. Links to the external billing system.
- `billing_status` — `trialing` | `active` | `past_due` | `canceled` | `comped`. Synced via Square webhooks. Gates feature access at the middleware level.

**Payment rails supported via Square:**
- **USD** — Square Subscriptions API. Card on file, recurring billing. 2.9% + $0.30.
- **BTC** — Square Lightning-powered Bitcoin payments. Fee-free through 2026, then 1% flat. Auto-convert to USD or hold as BTC (per GRO-93 treasury config).
- **Manual/Enterprise** — Square Invoices API. Net-30, PO-based for large accounts.

**Dog-food note:** GrowDirect IS a Square merchant. Canary LP monitors its own Square account. The same platform we protect is the platform we bill through. The `organizations` row for GrowDirect has `billing_provider = 'square'` and `billing_external_id` pointing at GrowDirect's own subscription catalog.

### Alter: `merchants`

```sql
ALTER TABLE merchants ADD COLUMN organization_id VARCHAR(36)
    REFERENCES organizations(id);
CREATE INDEX idx_merchants_organization_id ON merchants(organization_id);
```

### Updated RLS policy (applied by level_b_demo.py to all 50 tables)

```sql
CREATE POLICY tenant_isolation ON {table}
    FOR ALL
    USING (merchant_id = ANY(string_to_array(
        current_setting('canary.current_merchant_id', true), ',')))
    WITH CHECK (merchant_id = ANY(string_to_array(
        current_setting('canary.current_merchant_id', true), ',')));
```

### Updated helper functions (01-create-databases.sql) — no signature change

Functions `set_current_merchant(mid TEXT)` and `get_current_merchant()` remain identical. The caller passes either `'id1'` or `'id1,id2'`. The RLS policy handles both.

---

## Merchant #2 Provisioning (Test Path)

To validate multi-tenant in dev:

1. Create org in seed script → assign existing demo merchant to it
2. Seed merchant #2 (new Square sandbox merchant or synthetic ID)
3. Assign merchant #2 to same org
4. Verify: `set_current_merchant('merchant-1')` → sees only merchant-1 data
5. Verify: `set_current_merchant('merchant-1,merchant-2')` → sees combined data
6. Verify: `set_current_merchant('merchant-2')` → sees only merchant-2 data (empty if no data seeded)

---

## Action Items

1. [ ] **Tom:** Review architecture — confirm org → merchant parent-child is sound
2. [ ] **Syd:** FCRA opinion on combined view across merchant_ids within one org
3. [ ] **Jeremy:** Create Alembic migration for `organizations` table + `merchants.organization_id` FK
4. [ ] **ALX:** Update `level_b_demo.py` — create org, assign demo merchant, seed merchant #2
5. [ ] **ALX:** Update RLS policy in `level_b_demo.py` to use `ANY(string_to_array(...))`
6. [ ] **ALX:** Update `jwt_auth.py` middleware — `g.merchant_ids` (list), `g.organization_id`
7. [ ] **Jim:** QA test plan — single view, combined view, cross-tenant isolation verification
8. [ ] **Jeffe:** Approve architecture before code begins

---

*Canary LP | GrowDirect Inc. | Confidential*
