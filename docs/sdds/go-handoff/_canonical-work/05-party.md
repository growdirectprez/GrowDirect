# Chunk 4 — Party Domain: Customer + Employee (Schemas `c`, `e`)

**ARTS anchor**: ARTS Party (abstract) → Customer + Employee (Vendor already covered in `m.vendors`, Chunk 2).
**Modules**: C (Customer), L (Labor / People).
**Entities**: 6 (customers · customer_addresses · loyalty_memberships · employees · employee_role_assignments · employee_location_assignments).
**Folded from sources**: GSLM 14 Customer + 4 People entities → 6 SMB-2030 canonical.

## Domain narrative

ARTS Party is an abstract supertype: Customer, Employee, Vendor, and Organization all conform to its base shape (id, name, contact info). For SMB-2030 we don't materialize the Party supertype as a single table (tenant-isolation patterns differ by subtype, and SMB rarely queries "all parties") — but we maintain ARTS naming and the Party-derived attribute conventions so future federation (e.g., a customer who's also an employee) is clean.

Customer is **thin by default** for SMB: most transactions are anonymous, loyalty enrollments are phone-or-email only, full profiles are the exception not the rule. Schema supports the sparse case (most fields nullable) without paying decomposition cost. Loyalty is a sub-domain of Customer (one canonical entity, supports multi-program later).

Employee in SMB-2030 is similarly thin: a small staff (1-50 people typical), most without complex role hierarchies. We keep ARTS-aligned role and location-assignment as many-to-many tables because both are queried structurally (RBAC checks, manager-of-store reports), but neither is over-decomposed.

GSLM gave us 14 Customer entities and 4 People entities — we fold most into the master rows or JSONB. CRDM 1.7.2 had `CRDM_Customer` (dropped in 1.8) — operational customer-touchpoint detail; we capture this via the loyalty/transaction join, not a separate operational customer table.

TOM operational lifecycle: notably **TOM had no P-Prefix or R-Prefix interfaces** (People and Retail folders empty in S9 corpus). Customer and Employee master data lived in separate enterprise systems Tesco didn't expose via the integration layer corpus we have. Canary Go MCP services for these domains are designed fresh — the lifecycle bindings are net-new, not derived from TOM fingerprints.

---

## c.customers

**ARTS reference**: ARTS Customer (Party subtype).
**Module**: C.

### Schema

```sql
CREATE TABLE c.customers (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  customer_code   text,                                  -- merchant-assigned (loyalty number, account number); nullable for anonymous walk-in
  customer_type   text NOT NULL DEFAULT 'individual',    -- individual | business | household | guest
  first_name      text,
  last_name       text,
  display_name    text,                                  -- computed or business name
  email           text,                                  -- primary email (PII tier 2)
  phone           text,                                  -- primary phone (PII tier 2; E.164 format)
  birth_date      date,                                  -- for age-restriction verification + birthday promos (PII tier 3)
  preferred_language text DEFAULT 'en-US',
  marketing_opt_in   boolean NOT NULL DEFAULT false,     -- explicit consent
  primary_address jsonb DEFAULT '{}',                    -- {line1, line2, city, region, postal_code, country}
  attributes      jsonb NOT NULL DEFAULT '{}',           -- demographics, segments, merchant-defined
  status          text NOT NULL DEFAULT 'active',        -- active | inactive | suppressed | merged
  merged_into     uuid REFERENCES c.customers(id),       -- for dedup / merge events
  external_ids    jsonb DEFAULT '{}',                    -- {pos_native_id, square_id, stripe_customer_id, etc.}
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, customer_code) DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX idx_customers_tenant ON c.customers(tenant_id);
CREATE INDEX idx_customers_email ON c.customers(tenant_id, lower(email)) WHERE email IS NOT NULL AND status = 'active';
CREATE INDEX idx_customers_phone ON c.customers(tenant_id, phone) WHERE phone IS NOT NULL AND status = 'active';
CREATE INDEX idx_customers_status ON c.customers(status) WHERE status != 'active';
CREATE INDEX idx_customers_attributes ON c.customers USING gin(attributes);
CREATE INDEX idx_customers_external_ids ON c.customers USING gin(external_ids);
```

### Operational lifecycle (TOM operational clock)

**Producers**:
- `mcp.customer.create` — at first touchpoint (loyalty enrollment, account creation, B2B onboard)
- `mcp.customer.update` — profile changes
- `mcp.customer.merge` — dedup event (sets `status='merged'` and `merged_into` on duplicate)
- `mcp.customer.from-pos-native-sync` — when POS-native customer record exists (Square Customer, Stripe Customer, Counterpoint AR_CUST)

**Consumers**:
- `mcp.transaction.customer.lookup` — at POS for loyalty redemption, age verification (real-time, p99 < 30ms)
- `mcp.loyalty.points.compute` — earn/redeem at transaction time
- `mcp.marketing.campaign.scope-by-segment` — opt-in audiences
- `mcp.metrics.customer-aggregate` — RFM, LTV, segment rollups
- `mcp.compliance.consent-audit` — GDPR/CCPA consent tracking

**SLA at producer**: real-time, p95 < 200ms, idempotent on `(tenant_id, customer_code)` OR `(tenant_id, lower(email))` OR `(tenant_id, phone)` depending on touchpoint.
**SLA at consumers**: lookup p99 < 30ms; freshness < 5s for transaction-time lookups.

### Provenance

- **ARTS reference**: Customer (Party subtype)
- **GSLM Customer (S0)**: 14 entities folded — Customer master + addresses + contacts + segments + loyalty + preferences (most into JSONB; multi-address gets its own table below; loyalty gets its own table)
- **CRDM 1.7.2**: `CRDM_Customer` (dropped in 1.8) — was operational POS-touch customer record; we don't replicate that operational role (transaction join provides it)
- **TOM junctions**: none (P-Prefix empty); Canary Go customer junctions are net-new
- **Canary current**: `app.customers` — superseded
- **Justification**: Sparse row design (almost all fields nullable) supports anonymous-walk-in through full B2B-account merchants without schema variance. `external_ids` JSONB enables clean federation with POS-native customer records (Square, Stripe, Counterpoint) without per-source columns. Conditional unique indexes on email/phone prevent duplicates only for active rows. DEFERRABLE constraint on `customer_code` allows merge transactions that temporarily violate uniqueness during cleanup.

---

## c.customer_addresses

**ARTS reference**: ARTS Customer Address (multiple per customer).
**Module**: C.

### Schema

```sql
CREATE TABLE c.customer_addresses (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  customer_id     uuid NOT NULL REFERENCES c.customers(id) ON DELETE CASCADE,
  address_type    text NOT NULL DEFAULT 'shipping',      -- shipping | billing | mailing | service | pickup
  recipient_name  text,
  line_1          text NOT NULL,
  line_2          text,
  city            text NOT NULL,
  region          text,                                   -- state/province/county
  postal_code     text,
  country         text NOT NULL DEFAULT 'US',             -- ISO 3166 alpha-2
  latitude        numeric(10,7),
  longitude       numeric(10,7),
  is_default      boolean NOT NULL DEFAULT false,
  attributes      jsonb NOT NULL DEFAULT '{}',
  status          text NOT NULL DEFAULT 'active',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT one_default_per_type EXCLUDE (customer_id WITH =, address_type WITH =) WHERE (is_default = true AND status = 'active')
);

CREATE INDEX idx_addresses_tenant ON c.customer_addresses(tenant_id);
CREATE INDEX idx_addresses_customer ON c.customer_addresses(customer_id);
CREATE INDEX idx_addresses_type_default ON c.customer_addresses(customer_id, address_type) WHERE is_default = true;
```

### Operational lifecycle

**Producers**:
- `mcp.customer-address.add` — when customer adds shipping/billing address
- `mcp.customer-address.from-order-derive` — auto-add shipping address from a delivery order

**Consumers**:
- `mcp.orders.shipping.resolve-address`
- `mcp.financial.invoice.bill-to-address`
- `mcp.marketing.geo-segment`

**SLA at producer**: real-time. EXCLUDE constraint enforces single default per address type per customer.

### Provenance

- **ARTS reference**: Customer Address (multiple per Customer)
- **GSLM folded**: GSLM Customer domain had separate `CustomerAddress` entities — preserved (most SMB merchants need it for B2B accounts and ship-to)
- **TOM junctions**: none (no Customer-domain TOM interfaces)
- **Justification**: Separate table because SMB B2B customers genuinely have multiple ship-to addresses (corporate office, multiple warehouses, multiple stores). Pure B2C merchants can skip this table — `c.customers.primary_address` JSONB covers the single-address case.

---

## c.loyalty_memberships

**ARTS reference**: ARTS Loyalty (Membership + Program).
**Module**: C.

### Schema

```sql
CREATE TABLE c.loyalty_memberships (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  customer_id         uuid NOT NULL REFERENCES c.customers(id) ON DELETE CASCADE,
  program_code        text NOT NULL DEFAULT 'default',   -- merchant may run multiple programs
  membership_number   text NOT NULL,                     -- the loyalty card / member ID
  enrollment_date     date NOT NULL DEFAULT CURRENT_DATE,
  tier                text DEFAULT 'standard',           -- standard | silver | gold | platinum | etc.
  points_balance      bigint NOT NULL DEFAULT 0,         -- current available points
  points_lifetime     bigint NOT NULL DEFAULT 0,         -- cumulative earned (informational)
  birth_date          date,                              -- for birthday promos (denormalized from customer for query speed)
  preferences         jsonb DEFAULT '{}',                -- communication prefs, category interests
  attributes          jsonb NOT NULL DEFAULT '{}',
  status              text NOT NULL DEFAULT 'active',    -- active | suspended | expired | closed
  expires_at          timestamptz,                        -- if program has expiration
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, program_code, membership_number),
  UNIQUE (tenant_id, customer_id, program_code)            -- one membership per customer per program
);

CREATE INDEX idx_loyalty_tenant ON c.loyalty_memberships(tenant_id);
CREATE INDEX idx_loyalty_customer ON c.loyalty_memberships(customer_id);
CREATE INDEX idx_loyalty_member_lookup ON c.loyalty_memberships(tenant_id, membership_number) WHERE status = 'active';
CREATE INDEX idx_loyalty_tier ON c.loyalty_memberships(tier) WHERE status = 'active';
```

### Operational lifecycle

**Producers**:
- `mcp.loyalty.enroll` — at sign-up
- `mcp.loyalty.points-earn` — at transaction completion
- `mcp.loyalty.points-redeem` — at transaction completion when points used as tender
- `mcp.loyalty.tier-evaluate` — periodic (monthly) tier recalc
- `mcp.loyalty.expire` — when membership lapses

**Consumers**:
- `mcp.transaction.loyalty.lookup` — at POS, p99 < 30ms (every loyalty-tender or earn)
- `mcp.marketing.tier-segment` — campaign targeting by tier
- `mcp.metrics.loyalty-engagement`

**SLA at producer**: real-time for earn/redeem; idempotent (use transaction_id for earn deduplication).

### Provenance

- **ARTS reference**: ARTS Loyalty (Membership + Program — we fold both into single membership entity; multi-program supported via `program_code`)
- **GSLM folded**: GSLM Customer domain loyalty entities collapsed (~3 entities → 1 + JSONB preferences)
- **CRDM**: `CRDM_LoyaltyCard` is the operational POS-touch event (lives in T schema as part of transaction); not the master record
- **TOM junctions**: none for master; J035 Actual Sales TDS→GFO carries loyalty signals downstream (we'll cross-reference in Chunk 7)
- **Justification**: `points_balance` denormalized on the membership row (not summed from a points-transaction log) — read performance at every POS scan beats audit-trail purity. Points-transaction log lives in `t.loyalty_events` (Chunk 7) for audit/recompute.

---

## e.employees

**ARTS reference**: ARTS Employee (Party subtype).
**Module**: L.

### Schema

```sql
CREATE TABLE e.employees (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  user_id             uuid REFERENCES app.users(id),         -- if employee has a Canary login (managers, supervisors); nullable for cashiers without login
  employee_code       text NOT NULL,                          -- POS cashier number, badge ID
  first_name          text NOT NULL,
  last_name           text NOT NULL,
  display_name        text,
  email               text,                                   -- work email (PII tier 2)
  phone               text,                                   -- (PII tier 2)
  hire_date           date NOT NULL,
  termination_date    date,
  employment_status   text NOT NULL DEFAULT 'active',        -- active | on_leave | terminated | seasonal | applicant
  pay_type            text,                                   -- hourly | salaried | contract | tipped (no actual pay rate stored — sensitive)
  attributes          jsonb NOT NULL DEFAULT '{}',           -- merchant-defined fields (badge color, training certs)
  external_ids        jsonb DEFAULT '{}',                    -- payroll system ID, POS-native cashier ID
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, employee_code)
);

CREATE INDEX idx_employees_tenant ON e.employees(tenant_id);
CREATE INDEX idx_employees_user ON e.employees(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_employees_status ON e.employees(employment_status) WHERE employment_status != 'active';
CREATE INDEX idx_employees_external_ids ON e.employees USING gin(external_ids);
```

### Operational lifecycle

**Producers**:
- `mcp.employee.hire` — onboard event
- `mcp.employee.update` — profile change
- `mcp.employee.terminate` — soft-terminate (sets `employment_status='terminated'`, `termination_date=today`)
- `mcp.employee.from-pos-native-sync` — sync from POS (Counterpoint USR_FILE / Square Team Member)

**Consumers**:
- `mcp.transaction.employee.lookup` — every POS transaction tagged with cashier_id
- `mcp.audit.employee-action.attribute` — for OperatorAction (CRDM equivalent), shrink investigations
- `mcp.scheduling.employee-roster` — labor scheduling (future)
- `mcp.metrics.employee-performance` — sales per hour, transactions per shift

**SLA at producer**: real-time, p95 < 200ms.

### Provenance

- **ARTS reference**: Employee (Party subtype)
- **GSLM folded**: 4 People entities collapsed (most fields into employee row + role/location assignments below)
- **CRDM operational**: `CRDM_OperatorAction` and `CRDM_StaffDiscount` reference cashier_no — we tie into `e.employees.employee_code` for cashier identification
- **TOM junctions**: none (P-Prefix empty); Canary Go is greenfield here
- **Canary current**: `app.employees` — superseded
- **Justification**: No pay rate stored (sensitive — separate payroll system, not retail platform's role). Employee-to-Canary-user link nullable because cashiers may not have logins (just clock in via POS). Soft-termination preserves audit trail.

---

## e.employee_role_assignments

**ARTS reference**: ARTS Employee Role.
**Module**: L.

### Schema

```sql
CREATE TABLE e.employee_role_assignments (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  employee_id     uuid NOT NULL REFERENCES e.employees(id) ON DELETE CASCADE,
  role_code       text NOT NULL,                              -- cashier | shift_lead | manager | gm | inventory_lead | etc.
  effective_start date NOT NULL DEFAULT CURRENT_DATE,
  effective_end   date,                                       -- NULL = current
  attributes      jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, employee_id, role_code, effective_start)
);

CREATE INDEX idx_emp_roles_tenant ON e.employee_role_assignments(tenant_id);
CREATE INDEX idx_emp_roles_employee ON e.employee_role_assignments(employee_id);
CREATE INDEX idx_emp_roles_active ON e.employee_role_assignments(employee_id, role_code) WHERE effective_end IS NULL;
```

### Operational lifecycle

**Producers**:
- `mcp.employee-role.assign` — at promotion / role change
- `mcp.employee-role.expire` — when role ended (sets `effective_end`)

**Consumers**:
- `mcp.access-control.role-check` — RBAC at every Canary action
- `mcp.transaction.role-validate` — e.g., "manager override" requires manager role
- `mcp.audit.role-change-history`

**SLA at producer**: real-time.

### Provenance

- **ARTS reference**: Employee Role (with effective dating)
- **GSLM**: not richly modeled in People domain (4 entities only)
- **TOM junctions**: none
- **Justification**: Effective-dated role assignments support audit ("who was a manager on date X?"). Role code is a string, not a FK to a roles table — RBAC permissions are configured per-role in `app.roles` (already exists in current Canary spec); this table is the assignment relation.

---

## e.employee_location_assignments

**ARTS reference**: ARTS Employee-Store assignment.
**Module**: L.

### Schema

```sql
CREATE TABLE e.employee_location_assignments (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  employee_id     uuid NOT NULL REFERENCES e.employees(id) ON DELETE CASCADE,
  location_id     uuid NOT NULL REFERENCES l.locations(id) ON DELETE CASCADE,
  assignment_type text NOT NULL DEFAULT 'home',                 -- home | rotating | temporary | floating
  effective_start date NOT NULL DEFAULT CURRENT_DATE,
  effective_end   date,
  is_primary      boolean NOT NULL DEFAULT false,
  attributes      jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, employee_id, location_id, effective_start),
  CONSTRAINT one_primary_per_employee EXCLUDE (employee_id WITH =) WHERE (is_primary = true AND effective_end IS NULL)
);

CREATE INDEX idx_emp_loc_tenant ON e.employee_location_assignments(tenant_id);
CREATE INDEX idx_emp_loc_employee ON e.employee_location_assignments(employee_id);
CREATE INDEX idx_emp_loc_location ON e.employee_location_assignments(location_id);
CREATE INDEX idx_emp_loc_active ON e.employee_location_assignments(employee_id, location_id) WHERE effective_end IS NULL;
```

### Operational lifecycle

**Producers**:
- `mcp.employee-location.assign` — at hire / transfer
- `mcp.employee-location.expire` — at transfer-out / termination

**Consumers**:
- `mcp.transaction.employee-at-location.validate` — was this cashier authorized to ring up at this store?
- `mcp.scheduling.location-staff-roster`
- `mcp.metrics.location-staff-headcount`

**SLA at producer**: real-time.

### Provenance

- **ARTS reference**: Employee-Location assignment
- **GSLM**: 4 People entities — folded
- **TOM junctions**: none
- **Canary current**: `app.employee_location_assignments` already exists — preserved as-is, ARTS-aligned name retained
- **Justification**: EXCLUDE constraint enforces single primary location per active employee. Effective-dating supports transfer history. `assignment_type` discriminates "home store" from "covers shifts elsewhere."

---

## Domain summary

**6 entities, 2 schemas (c, e), 2 modules (C + L)**:
- `c.customers` (~22 cols) — sparse-by-default master
- `c.customer_addresses` (~16 cols) — multi-address (optional for B2B)
- `c.loyalty_memberships` (~16 cols) — denormalized points balance, multi-program
- `e.employees` (~16 cols) — no pay rate stored
- `e.employee_role_assignments` (~9 cols) — effective-dated
- `e.employee_location_assignments` (~10 cols) — primary-location EXCLUDE constraint

**Folded from sources**:
- GSLM 14 Customer entities → 3 (customer master + addresses + loyalty)
- GSLM 4 People entities → 3 (employee master + role assignments + location assignments)
- CRDM 1.7.2 `CRDM_Customer` was operational POS-touch — covered by transaction join, not separate operational table

**Net new** (no source has):
- `c.loyalty_memberships` multi-program support — most sources assumed single program; SMB-2030 may need program-per-channel or program-per-banner
- Effective-dated role and location assignments — TOM never modeled this (P-Prefix empty); designed fresh

**MCP service junctions defined for this domain (~16)**:
- Producers: customer create/update/merge/from-pos-sync, customer-address add/from-order, loyalty enroll/earn/redeem/tier-evaluate/expire, employee hire/update/terminate/from-pos-sync, employee-role assign/expire, employee-location assign/expire
- Consumers: transaction customer-lookup, loyalty points-compute, marketing campaign-scope, metrics aggregate, compliance consent-audit, transaction employee-lookup, audit role-change-history, access-control role-check, scheduling roster

## Status

- **Chunk 4 complete.** 6 ARTS-Party-aligned entities (Customer + Employee). Vendor already in Chunk 2's `m.vendors`.
- **Resume**: Chunk 5 — Inventory + Distribution domain (i schema). ARTS Inventory V2 anchor (we have full PDF spec) + D-Prefix lifecycle. Target ~6-8 entities.
