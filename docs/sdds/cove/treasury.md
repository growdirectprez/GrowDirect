# Treasury Module

**Status:** Active
**Type:** App Service
**Last updated:** 2026-04-13
**Blueprint:** `treasury_bp` at `/treasury`
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Tom|Tom]] · **Operator role:** [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

---

## Purpose

Assessment creation, payment recording, budget overview, and delinquency tracking for HOA financial operations. Assessments are tied to parcels (APNs), not members -- a parcel owes regardless of ownership transfer. Enforces WPBCA Bylaws section 13.2 assessment caps and Davis-Stirling delinquency rules.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | Assessments, payments, budgets | Yes |
| `cove.governance.bylaws_config` | Assessment limits (section 13.2 cap) | Yes |
| `cove.models.parcel.Parcel` | Parcel list for payment status | Yes |
| `cove.models.member.Member` | Assessment status updates on members | Yes |

---

## Data Flow & PII Map

### What enters
- Assessment creation: name, type, amount, frequency, effective_date (board only)
- Payment recording: parcel_id (APN), amount, method, paid_date, notes (board only)

### What's stored

| Table | Field | Classification | Encryption |
|-------|-------|---------------|------------|
| `assessments` | `name`, `amount_per_lot`, `frequency` | internal | Plaintext |
| `parcel_payments` | `apn`, `amount`, `method`, `notes` | internal | Plaintext |
| `parcel_payments` | `notes` (may contain check numbers) | sensitive | **Plaintext (P1)** |
| `ledger_entries` | `payee_or_payer` | sensitive | **Plaintext (P1)** |
| `budgets` | Financial totals | internal | Plaintext |

### What exits
- Dashboard stats rendered in templates (authenticated members)
- Per-parcel payment status tables (board only)

**PII note:** Payment notes may contain check numbers or personal references. `ledger_entries.payee_or_payer` could contain member names. Both should be treated as sensitive.

---

## API Contract

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/treasury/` | `login_required` | Dashboard with summary stats and assessment list |
| GET | `/treasury/assessments` | `login_required` | Full assessments list |
| GET | `/treasury/budget` | `login_required` | Budget overview by fiscal year |
| GET/POST | `/treasury/assessments/create` | `login_required` + `is_board` | Create assessment (enforces section 13.2 cap) |
| GET/POST | `/treasury/assessments/<id>/pay` | `login_required` + `is_board` | Record payment against assessment |

### Access Control

| Role | Capabilities |
|------|-------------|
| Any member | View dashboard, assessments list, budget overview |
| Board | All above + create assessments, record payments |

All routes tenant-scoped by `current_user.organization_id`. Payment route additionally verifies assessment belongs to user's org.

---

## Services (`cove/treasury/services.py`)

| Function | Description |
|----------|-------------|
| `create_assessment(...)` | Creates assessment; enforces section 13.2 max for regular type; calls `update_assessment_status` |
| `record_payment(...)` | Records payment; calls `update_assessment_status` for affected parcel |
| `get_assessment_status(org_id, assessment_id)` | Per-parcel payment status (paid/partial/unpaid) |
| `get_delinquent_parcels(org_id, assessment_id, as_of)` | Filters unpaid/partial parcels past effective date |
| `get_treasury_summary(org_id)` | Aggregate metrics: total expected, collected, rate, count |
| `update_assessment_status(org_id, apn)` | Updates `Member.assessment_status` (current/delinquent) based on payment data |

### Bylaws Enforcement

`create_assessment()` reads `max_annual_per_lot` from `wpbca-bylaws-config.json`. Regular assessments exceeding this cap raise `ValueError`. Special assessments require a `proposal_id` linking to a member vote.

**Known discrepancy:** Template references "$240/lot" while config value is `200`. Needs reconciliation.

---

## Operations

### Startup
No module-specific startup.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| DB down | All routes 500 | Automatic reconnect |
| Bylaws config missing | `create_assessment` fails with `FileNotFoundError` | Restore `wpbca-bylaws-config.json` |

### Monitoring
- Alert on: assessment creation failures, collection rate dropping below threshold
- Normal: <10 assessments per year, ~81 parcels per assessment

---

## Deployment

Standard Cove deployment -- no module-specific infrastructure. Financial data lives in the `cove` PostgreSQL database.

- **Backup**: Financial tables (`assessments`, `parcel_payments`, `budgets`) are high-value -- ensure point-in-time recovery
- **AWS**: Same ECS task as Cove Flask app

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P0** | No audit trail for assessment creation or payment recording | Add audit entries via `_audit()` pattern used elsewhere |
| 2 | **P0** | Financial amounts stored as `Float` -- floating point arithmetic can cause rounding errors on currency | Migrate to `Numeric(10, 2)` or integer cents |
| 3 | **P1** | Payment notes may contain check numbers stored plaintext | Encrypt `notes` field |
| 4 | **P1** | `ledger_entries.payee_or_payer` may contain member names, stored plaintext | Encrypt sensitive fields |
| 5 | **P1** | `get_treasury_summary` runs N+1 query per assessment (queries parcel count per assessment) | Single aggregate query |
| 6 | **P1** | Template/$240 vs config/$200 cap discrepancy | Reconcile bylaws config with template text |
| 7 | **P1** | Budget records are read-only with no create/edit UI -- must be seeded manually | Add board-facing budget CRUD |
| 8 | **P2** | `LedgerEntry` model defined but unused by any route or service | Wire up or remove to avoid dead code |
| 9 | **P2** | No automated delinquency notice generation (120-day rule tracked in config but not enforced) | Implement scheduled delinquency notice workflow |

---

## Production Readiness Checklist

- [ ] Financial amounts use decimal type (not Float)
- [ ] Audit logging for all financial operations
- [ ] Payment notes encrypted at rest
- [ ] Secrets in AWS Secrets Manager
- [x] Health check endpoint responds (via app-level `/health`)
- [ ] Data retention policy for financial records (legal minimum: 7 years for HOA)
- [x] Rate limiting (via app-level limiter)
- [x] Error responses don't leak internals
- [ ] Bylaws cap discrepancy reconciled
- [ ] Delinquency notice automation
