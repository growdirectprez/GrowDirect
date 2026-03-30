---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# DISPATCH: Multi-Tenant Partition Architecture — Code Drop
*Issued by ALX · March 4, 2026 · Priority: HIGH*
*Linear: GRO-18 (Multi-Tenant), GRO-96 (Phase 0 DB Foundation)*
*ADR: `docs/adr/ADR-001_Multi_Tenant_Partition_Architecture.md`*

**Context:** Jeffe directed that Canary support merchants with multiple Square accounts under one business identity. A restaurant group with 3 locations, each with its own Square merchant ID, needs a combined view. This is table stakes for any serious multi-location customer.

**Decision:** Organization → Merchant parent-child model with array-aware RLS. One org owns 1..N merchants. Session variable holds comma-separated merchant IDs. RLS uses `ANY(string_to_array(...))` to support both single and combined views through the same policy.

**Strategic Bonus:** Square is the billing backend. GrowDirect registers as a Square merchant, uses Square Subscriptions API for USD billing and Square Lightning for BTC payments. We dog-food: the platform we protect is the platform we bill through.

---

## FILES CHANGED — 7 Total (2 New, 5 Modified)

### New Files

| File | Purpose |
|---|---|
| `canary/models/app/organizations.py` | Organization model — billing root entity above merchants. Fields: `org_name`, `billing_email`, `subscription_tier`, `billing_provider` (default 'square'), `billing_external_id`, `billing_status` (default 'trialing'), `is_active`. Uses AppBase, AuditMixin, SoftDeleteMixin. |
| `docs/adr/ADR-001_Multi_Tenant_Partition_Architecture.md` | Full ADR with context, decision, options considered (A: org table, B: jsonb, C: separate schema), trade-off analysis, consequences, FCRA opinion request, DDL summary, merchant #2 provisioning test path, action items. |

### Modified Files

| File | Change |
|---|---|
| `canary/models/app/merchants.py` | Added `organization_id` FK to organizations.id (nullable for backward compat). Marked `subscription_tier` as DEPRECATED — billing moves to organizations. Updated docstring. |
| `canary/models/__init__.py` | Added `from canary.models.app.organizations import Organization` and `"Organization"` to `__all__`. |
| `devops/seeds/level_b_demo.py` | Added org seed (step 0), merchant #2 seed ("GrowDirect Online Store", SYNTHETIC_MERCHANT_002). Both merchants assigned to same org. RLS policy changed from equality to array-aware: `ANY(string_to_array(current_setting('canary.current_merchant_id', true), ','))`. |
| `canary/middleware/jwt_auth.py` | All three auth paths (JWT, stub API, session browser) updated: `g.organization_id`, `g.merchant_ids` (list), `g.merchant_id` (backward compat). Stub reads `CANARY_DEFAULT_ORG` and `CANARY_DEFAULT_MERCHANTS` env vars. |
| `devops/sql/rls_policies.sql` | Updated header to document ADR-001 array-aware pattern. Reference doc only — actual application is by level_b_demo.py. |

---

## REBUILD + VERIFY PROCEDURE

This is a **code COPY** architecture. Files are on disk but not live until rebuilt.

### Step 1: Rebuild Flask Container

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml up -d --build flask
```

### Step 2: Reseed (Full Reset)

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml exec flask python devops/seeds/level_b_demo.py
```

### Step 3: Verify Organization + Merchants

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml exec postgres psql -U canary_user -d canary_app -c "
SELECT o.org_name, m.merchant_name, m.merchant_id
FROM organizations o
JOIN merchants m ON m.organization_id = o.id
ORDER BY m.merchant_name;
"
```

Expected: 2 rows — GrowDirect Flagship + GrowDirect Online Store, both under "GrowDirect Inc."

### Step 4: Verify Array-Aware RLS — Single View

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml exec postgres psql -U canary_user -d canary_app -c "
SET canary.current_merchant_id = 'test-merchant-001';
SELECT count(*) AS single_view FROM merchants;
"
```

Expected: 1 row (only test-merchant-001).

### Step 5: Verify Array-Aware RLS — Combined View

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml exec postgres psql -U canary_user -d canary_app -c "
SET canary.current_merchant_id = 'test-merchant-001,demo-sq-online-store-000001';
SELECT count(*) AS combined_view FROM merchants;
"
```

Expected: 2 rows (both merchants visible — org-level view).

### Step 6: Verify Cross-Tenant Isolation

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml exec postgres psql -U canary_user -d canary_app -c "
SET canary.current_merchant_id = 'attacker-merchant-xyz';
SELECT count(*) AS should_be_zero FROM merchants;
"
```

Expected: 0 rows (unknown merchant sees nothing).

### Step 7: GRO-96 — Detection Rules Count

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml exec postgres psql -U canary_user -d canary_app -c "
SELECT count(*) FROM detection_rules;
"
```

Expected: 26 rules.

---

## OPEN GATES

| Gate | Owner | Status |
|---|---|---|
| Architecture review | Tom | Pending — review ADR-001 |
| FCRA opinion + BTC regulatory | Syd | Pending — flagged in ADR-001 |
| QA test plan (single/combined/isolation) | Jim | Pending — test procedure above |
| Env vars in .env | Jeremy | Add `CANARY_DEFAULT_ORG` and `CANARY_DEFAULT_MERCHANTS` if not present |

---

## GRO-96 STATUS

Phase 0 DB Foundation code is complete in the codebase:
- `set_current_merchant()` / `get_current_merchant()` in `01-create-databases.sql` ✓
- 26 detection rules in `level_b_demo.py` ✓
- Conflicting `rls_policies.sql` moved to `devops/sql/` as reference doc ✓

Needs: live rebuild + seed + `SELECT count(*)` verification on Mac Mini.

---

## SEED IDS

```
ORG_GROWDIRECT_ID  = "org-growdirect-000000000001"
MERCHANT_1_ID      = "test-merchant-001"           (GrowDirect Flagship)
MERCHANT_2_ID      = "demo-sq-online-store-000001"  (GrowDirect Online Store)
```

---

*Canary LP | GrowDirect Inc. | Confidential*
