---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-18 — Multi-Tenant Partition Architecture Options Paper

**Issue:** GRO-18
**Prepared By:** ALX (Chief of Staff), referencing Tom (Systems Architect) + PhD (Research Framework)
**Date:** March 2, 2026
**Classification:** Internal — Architecture Decision Record
**Gate:** Tom validates technical accuracy. Syd reviews FCRA implications. Jeffe approves direction.
**Done When:** Architecture decision recorded, DDL drafted, FCRA opinion documented.

---

## 1. Context

Canary LP currently runs on SQLite (single DB, MVP). The CRDM v1.0 specifies a three-database PostgreSQL architecture (`canary_app`, `canary_sales`, `canary_metrics`) as the target post-Square Marketplace certification. The multi-tenant isolation strategy must be decided before Jeremy writes production DDL.

The CRDM mandates: "Every table has `merchant_id`. No exceptions. No cross-tenant queries without explicit admin override." (Pattern 1: Multi-Tenant RLS). This paper evaluates whether RLS alone is sufficient or whether stronger isolation boundaries are required.

---

## 2. The Three Options

### Option A: Shared Schema + Row-Level Security (RLS)

**Architecture:** All merchants share the same tables in the same database. PostgreSQL RLS policies enforce isolation.

```
canary_app (shared)
  merchants  ←── merchant_id on every row
  employees  ←── merchant_id on every row
  ...
canary_sales (shared)
  transactions  ←── merchant_id on every row, monthly partitioned
  ...
canary_metrics (shared)
  daily_metrics  ←── merchant_id on every row
  ...

SET app.current_merchant_id = 'merchant_uuid';
CREATE POLICY tenant_isolation ON transactions
  USING (merchant_id = current_setting('app.current_merchant_id'));
```

**Pros:**
- Simplest implementation — matches CRDM v1.0 exactly as written
- Lowest operational overhead — one database cluster, one migration path, one backup pipeline
- Monthly partitioning (Pattern 5) already scoped per the CRDM
- Aggregation across merchants is trivial (admin analytics, platform-level reporting)
- Cheapest infrastructure (single Postgres instance at MVP scale)
- All ~35 tables already designed with `merchant_id` as the first column in every index (Pattern 6)

**Cons:**
- Noisy neighbor risk — a merchant with 10x transaction volume shares I/O with a merchant with 100 transactions/month
- RLS bypass = full tenant exposure. A single missed policy or misconfigured `SET` exposes all merchants
- FCRA/evidentiary concern: if a case goes to court, opposing counsel could argue that data residing in a shared database is less trustworthy than physically isolated data (see Section 4)
- Cannot offer "dedicated instance" tier for premium merchants without architectural change
- pg_dump/restore granularity is database-level, not merchant-level

**DDL Pattern (already defined in CRDM):**
```sql
-- Every table
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_read ON transactions FOR SELECT
  USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
CREATE POLICY tenant_write ON transactions FOR INSERT
  WITH CHECK (merchant_id = current_setting('app.current_merchant_id')::uuid);
-- Repeat for UPDATE (soft deletes only on operational tables)
```

**Effort:** Low. This is what the CRDM already describes. Jeremy implements Pattern 1 as-is.

---

### Option B: Schema-Per-Tenant

**Architecture:** Each merchant gets their own PostgreSQL schema within the shared database. Tables are identical but namespaced.

```
canary_app
  public.merchants          (shared — platform-level)
  public.users              (shared — auth)
  merchant_abc.employees
  merchant_abc.transactions
  merchant_abc.daily_metrics
  merchant_xyz.employees
  merchant_xyz.transactions
  merchant_xyz.daily_metrics
```

**Pros:**
- Stronger isolation — no RLS required per table; schema search path controls access
- pg_dump per schema = merchant-level backup/restore/export
- Noisy neighbor mitigation — can set per-schema resource limits (though Postgres doesn't natively support this without connection pooling tricks)
- Evidentiary strength — "this merchant's data lives in a physically separate schema" is a stronger courtroom argument
- Can migrate individual merchants to dedicated infrastructure without application changes

**Cons:**
- Schema proliferation — at 350 merchants × ~35 tables = 12,250 tables in the database. Postgres catalog performance degrades above ~10,000 objects
- Migration complexity — every `ALTER TABLE` must execute across all schemas. Tooling required (Tom would need a migration orchestrator)
- Cross-merchant analytics requires explicit `UNION ALL` across schemas — breaks simple aggregate queries
- Connection pooling (PgBouncer) interacts poorly with `SET search_path` — requires session-level pooling, not transaction-level
- Monthly partitioning (CRDM Pattern 5) within each schema = even more objects

**DDL Pattern:**
```sql
CREATE SCHEMA merchant_abc;
SET search_path TO merchant_abc;
CREATE TABLE transactions ( ... );  -- No merchant_id column needed
-- Repeat for all ~35 tables
```

**Effort:** Medium-High. Requires migration orchestrator, modified connection handling, and new backup tooling. Tom estimates 2-3 sprints for infrastructure alone.

---

### Option C: Database-Per-Tenant

**Architecture:** Each merchant gets a fully separate PostgreSQL database (or dedicated Postgres instance).

```
canary_platform   (shared — auth, billing, platform config)
canary_merchant_abc  (canary_app + canary_sales + canary_metrics for abc)
canary_merchant_xyz  (canary_app + canary_sales + canary_metrics for xyz)
```

**Pros:**
- Maximum isolation — no shared state, no RLS complexity, no catalog bloat
- Trivial backup/restore/export per merchant
- Can place high-volume merchants on dedicated hardware
- Strongest possible evidentiary claim — physically separate database, separate backup chain, separate access log
- Eliminates noisy neighbor entirely

**Cons:**
- Operational nightmare at scale — 350 databases × 3 environments = 1,050 database instances
- Connection pooling doesn't scale (each DB needs its own pool)
- Cross-merchant analytics requires federated queries (postgres_fdw) or a separate analytics pipeline
- Migration complexity — every schema change deploys to 350+ databases
- Infrastructure cost at scale is 10-50x Option A
- Completely incompatible with the RaaS API model (which needs to query across all merchants for verification)

**Effort:** Very High. Requires dedicated infrastructure automation, migration orchestration, and fundamentally changes the deployment model. Not recommended for MVP or even Series A scale.

---

## 3. Recommendation

**Option A (Shared Schema + RLS) with hardened safeguards.**

The CRDM already specifies this architecture. The ~35 tables already have `merchant_id` as the first column in every index. Monthly partitioning already segments data by time. The RaaS API model requires cross-merchant query capability that Options B and C fundamentally break.

### Hardening Measures (address Option A's cons):

1. **RLS audit trigger:** Every `SET app.current_merchant_id` call logs to `audit_log` with the calling user, session, and timestamp. Any unset or mismatched `merchant_id` fires an alert.

2. **Defense-in-depth policy:** Application layer AND database layer enforce isolation. The API gateway validates `merchant_id` on every request before it reaches Postgres. RLS is the backup, not the primary gate.

3. **Connection pooling with context:** Use PgBouncer in session mode with middleware that sets `app.current_merchant_id` on session checkout. Never transaction mode for tenant-scoped connections.

4. **Noisy neighbor monitoring:** Postgres `pg_stat_statements` per `merchant_id` (via custom logging). Alert if any merchant exceeds 10x average query cost. Scale to read replicas before schema separation.

5. **FCRA mitigation:** See Section 4 below.

6. **Escape hatch to Option B:** Design the application layer to be schema-path-aware from day one. If a premium merchant needs schema isolation, the migration is additive (create schema, copy data, update routing) rather than architectural.

---

## 4. FCRA and Evidentiary Considerations

**For Syd's review.**

The Fair Credit Reporting Act (FCRA) and state-level evidentiary standards may be relevant when Canary LP data is used in employee termination or law enforcement proceedings. The key question: **does shared-database multi-tenancy undermine the evidentiary weight of the data?**

### Analysis:

**The case for RLS being sufficient:**
- The data itself is identical regardless of isolation method — the same `transactions` row, the same `audit_log` hash chain, the same SHA-256 record hash
- RLS policies are mathematically equivalent to separate databases in terms of access control — a properly configured policy provably prevents cross-tenant reads
- The hash chain (CRDM Pattern 4) provides tamper-evident integrity regardless of where the data physically resides
- Bitcoin inscription (the RaaS layer) provides an external, independent proof that is completely separate from the database architecture
- PostgreSQL RLS is used by HIPAA-compliant healthcare platforms, SOC 2 certified SaaS, and FedRAMP-authorized government systems

**The case for stronger isolation:**
- An opposing attorney could argue (regardless of technical merit) that shared-database architecture creates "risk of contamination" — a rhetorical, not technical, argument
- If a database backup is subpoenaed, the entire database (all merchants) would be included unless merchant-level export tooling exists
- Chain of custody documentation is simpler when data is physically isolated

### Syd Action Items:
1. **Assess likelihood** that Canary LP data will be used in formal legal proceedings (employee termination, fraud prosecution) within the first 2 years
2. **Determine if RLS + hash chain + Bitcoin inscription** is sufficient evidentiary integrity for the expected use cases
3. **If stronger isolation is needed**, recommend Option B (schema-per-tenant) for merchants who escalate to legal proceedings — this can be a per-merchant migration, not a platform-wide change
4. **Draft a data integrity certification** that Canary LP can provide to merchants, documenting the RLS, hash chain, and Bitcoin inscription layers

---

## 5. Decision Matrix

| Criterion | Weight | Option A (RLS) | Option B (Schema) | Option C (DB) |
|-----------|--------|----------------|-------------------|---------------|
| Implementation effort | 25% | **5** (CRDM-ready) | 3 (2-3 sprints) | 1 (massive) |
| Operational cost | 20% | **5** (single cluster) | 3 (manageable) | 1 (10-50x) |
| Tenant isolation | 15% | 3 (RLS + audit) | **4** (schema path) | **5** (physical) |
| Evidentiary strength | 15% | 3 (hash chain compensates) | **4** (schema isolation) | **5** (full isolation) |
| RaaS compatibility | 15% | **5** (cross-tenant queries) | 2 (UNION ALL) | 1 (federated) |
| Scalability to 10K merchants | 10% | **4** (read replicas) | 2 (catalog bloat) | 1 (ops nightmare) |
| **Weighted Score** | | **4.25** | **3.05** | **2.00** |

**Recommendation: Option A with hardened safeguards. Revisit if Syd identifies FCRA risk requiring schema isolation for specific merchants.**

---

## 6. Partitioning Strategy

The CRDM specifies monthly partitioning (Pattern 5) on `transaction_date`. Within Option A (shared schema), all merchants share the same monthly partition set. The question: does this need to be merchant-aware?

### Approach 1: Monthly Partitioning, Shared (Recommended for Launch)

All merchants live in the same monthly partitions (`transactions_2026_01`, `transactions_2026_02`, etc.). The `merchant_id` index (Pattern 6) ensures queries only scan relevant rows within each partition. PostgreSQL's query planner handles this efficiently: partition pruning narrows by date range, then the `(merchant_id, ...)` index narrows by tenant.

```
transactions_2026_03  ← all merchants, March 2026
  └─ idx_merchant_date(merchant_id, transaction_date)  ← fast per-tenant scan
```

This is the simplest model. It matches the CRDM exactly. It works for launch and well beyond it.

### Approach 2: Composite Partitioning (Merchant + Time) — Future Escape Hatch

If a specific merchant hits volume where shared monthly partitions cause performance issues, PostgreSQL supports sub-partitioning:

```sql
-- First level: partition by merchant (or merchant group)
CREATE TABLE canary_sales.transactions (...) PARTITION BY LIST (merchant_id);

-- Second level: per-merchant time partitions
CREATE TABLE transactions_merchant_abc PARTITION OF transactions
  FOR VALUES IN ('abc-uuid') PARTITION BY RANGE (transaction_date);

-- High-volume merchant gets daily sub-partitions
CREATE TABLE transactions_merchant_abc_2026_03_01 ...

-- Low-volume merchant gets monthly sub-partitions
CREATE TABLE transactions_merchant_xyz_2026_03 ...
```

This lets different merchants have different partition granularity. The tradeoff: each merchant needs its own partition set created and managed. At 350 merchants it's workable but operationally heavier.

### Recommendation

**Start with Approach 1 (monthly, shared).** It's what the CRDM specifies and it handles the expected load. If a merchant crosses a volume threshold where monthly partitions are too large for efficient queries, migrate that specific merchant to composite sub-partitioning. The data model doesn't change — it's a DDL-level operation, transparent to the application layer. Jeremy doesn't need to code for this now; Tom documents it as the scaling path.

---

## 7. DDL Draft (Option A — Ready for Tom's Review)

The full DDL is derived from CRDM v1.0 Part 7 (Design Patterns) and Part 6 (Table Inventory). Key structural elements:

```sql
-- 1. Enable RLS on every tenant-scoped table
ALTER TABLE canary_sales.transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE canary_sales.transactions FORCE ROW LEVEL SECURITY;

-- 2. Tenant isolation policies
CREATE POLICY tenant_select ON canary_sales.transactions
  FOR SELECT USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
CREATE POLICY tenant_insert ON canary_sales.transactions
  FOR INSERT WITH CHECK (merchant_id = current_setting('app.current_merchant_id')::uuid);

-- 3. Monthly partitioning (Pattern 5)
CREATE TABLE canary_sales.transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  merchant_id UUID NOT NULL REFERENCES canary_app.merchants(id),
  external_id TEXT NOT NULL,
  transaction_date DATE NOT NULL,
  transaction_type TEXT NOT NULL CHECK (transaction_type IN (
    'SALE','RETURN','VOID','POST_VOID','NO_SALE','PAID_IN','PAID_OUT','EXCHANGE'
  )),
  amount_cents BIGINT NOT NULL,
  currency TEXT NOT NULL DEFAULT 'USD',
  employee_id UUID REFERENCES canary_app.employees(id),
  location_id UUID NOT NULL REFERENCES canary_app.locations(id),
  customer_id UUID REFERENCES canary_app.customers(id),
  device_id TEXT,
  square_product TEXT,
  card_fingerprint TEXT,
  payload JSONB NOT NULL,
  scrub_version INTEGER NOT NULL DEFAULT 1,
  record_hash TEXT NOT NULL,
  previous_hash TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(merchant_id, external_id)
) PARTITION BY RANGE (transaction_date);

-- 4. Merchant-first indexing (Pattern 6)
CREATE INDEX idx_transactions_merchant_date
  ON canary_sales.transactions(merchant_id, transaction_date);
CREATE INDEX idx_transactions_merchant_employee
  ON canary_sales.transactions(merchant_id, employee_id);
CREATE INDEX idx_transactions_merchant_type
  ON canary_sales.transactions(merchant_id, transaction_type);

-- 5. Audit trigger for RLS context setting
CREATE OR REPLACE FUNCTION audit_tenant_context() RETURNS trigger AS $$
BEGIN
  INSERT INTO canary_app.audit_log (
    merchant_id, action, table_name, record_id,
    session_user_name, tenant_context, record_hash, previous_hash
  ) VALUES (
    NEW.merchant_id, TG_OP, TG_TABLE_NAME, NEW.id,
    session_user, current_setting('app.current_merchant_id', true),
    NEW.record_hash, NEW.previous_hash
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Tom:** Please review the DDL against CRDM v1.0 and flag any divergences. The full DDL for all ~35 tables should follow this pattern. Jeremy implements after Tom's sign-off.

---

## 8. Routing

- **Tom:** Validate DDL patterns, confirm PgBouncer session mode recommendation, review noisy neighbor monitoring approach
- **Syd:** FCRA evidentiary assessment (Section 4), data integrity certification draft
- **Jeremy:** Implement after Tom + Syd sign-off. Start with canary_sales (highest isolation criticality)
- **Jim:** QA plan for RLS policy verification — test cross-tenant isolation with multiple merchant sessions
- **PhD:** If RaaS API design (GRO-13) requires cross-merchant query patterns, confirm Option A supports them

---

*ALX | GRO-18 | March 2, 2026*
