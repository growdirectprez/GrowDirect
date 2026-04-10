# SDD: Treasury Module

**Status:** Active
**Last updated:** 2026-03-29

---

## 1. Blueprint

- **Variable:** `treasury_bp`
- **Prefix:** `/treasury`
- **Module:** `cove/treasury/routes.py`
- **Registration:** `app.register_blueprint(treasury_bp, url_prefix="/treasury")` in `cove/__init__.py`
- **Template folder:** `cove/treasury/templates/` (blueprint-local via `template_folder="templates"`)
- **Imports:** `Assessment`, `Budget` models; `Parcel` model; `AssessmentCreateForm`, `PaymentRecordForm`; `services` module

---

## 2. Routes

| Method | Path | Access | Description |
|--------|------|--------|-------------|
| GET | `/treasury/` | `@login_required` | Treasury overview dashboard. Shows summary stats (total expected, total collected, collection rate, assessment count) and a table of all assessments for the org. Board members see a "New Assessment" button and per-assessment "Payments" links. |
| GET | `/treasury/assessments` | `@login_required` | Full assessments list. Displays all assessments ordered by effective date descending, with columns for name, type, amount/lot, frequency, effective date, and vote-required status. Board members see "New Assessment" button and "Payments" links. |
| GET | `/treasury/budget` | `@login_required` | Budget overview. Lists all `Budget` records by fiscal year descending with income, expense, reserve allocation, net, and approval status. Includes the same treasury summary stats as the index. |
| GET, POST | `/treasury/assessments/create` | `@login_required` + `is_board` (403 otherwise) | Create a new assessment. GET renders `AssessmentCreateForm`. POST validates the form and calls `services.create_assessment()`. If the service raises `ValueError` (regular assessment exceeds bylaws cap), the error is flashed. On success, redirects to the assessments list. |
| GET, POST | `/treasury/assessments/<assessment_id>/pay` | `@login_required` + `is_board` (403 otherwise) | Record a payment against an assessment. Loads the assessment (404 if not found or wrong org). Builds parcel choices from the org's parcels. GET renders `PaymentRecordForm` plus a per-parcel payment status table. POST validates and calls `services.record_payment()`, then redirects back to the same page. |

---

## 3. Models

All models are in `cove/models/treasury.py`. All use UUID string primary keys (`String(36)`, `default=lambda: str(uuid.uuid4())`).

### Assessment (`assessments`)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `String(36)` | PK | UUID |
| `organization_id` | `String(36)` | FK `organizations.id`, NOT NULL | Tenant scoping |
| `name` | `String(255)` | NOT NULL | e.g., "2026 Annual Assessment" |
| `type` | `String(20)` | NOT NULL | `regular` or `special_assessment` |
| `amount_per_lot` | `Float` | NOT NULL | Per-parcel amount in dollars |
| `frequency` | `String(20)` | NOT NULL, default `"monthly"` | `monthly`, `quarterly`, `annual`, `one_time` |
| `effective_date` | `Date` | NOT NULL | When the assessment takes effect |
| `end_date` | `Date` | nullable | Optional end date |
| `approved_by_vote` | `bool` | default `False` | True if backed by a member vote |
| `proposal_id` | `String(36)` | FK `proposals.id`, nullable | Link to governance proposal |
| `created_at` | `DateTime` | default `utcnow` | |

### LedgerEntry (`ledger_entries`)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `String(36)` | PK | UUID |
| `organization_id` | `String(36)` | FK `organizations.id`, NOT NULL | |
| `date` | `Date` | NOT NULL | Transaction date |
| `type` | `String(20)` | NOT NULL | `income` or `expense` |
| `category` | `String(100)` | NOT NULL | dues, maintenance, legal, insurance, etc. |
| `description` | `String(500)` | NOT NULL | |
| `amount` | `Float` | NOT NULL | |
| `payee_or_payer` | `String(255)` | nullable | |
| `created_at` | `DateTime` | default `utcnow` | |

**Note:** LedgerEntry is defined but not referenced by any route, form, or service. It exists for future general-ledger functionality.

### Budget (`budgets`)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `String(36)` | PK | UUID |
| `organization_id` | `String(36)` | FK `organizations.id`, NOT NULL | |
| `fiscal_year` | `Integer` | NOT NULL | e.g., 2026 |
| `total_income` | `Float` | default `0` | |
| `total_expense` | `Float` | default `0` | |
| `reserve_allocation` | `Float` | default `0` | |
| `approved` | `bool` | default `False` | |
| `created_at` | `DateTime` | default `utcnow` | |

**Note:** Budget is read-only in the UI. No create/edit routes exist. Budget records must be created via seed data, shell, or a future admin interface.

### ParcelPayment (`parcel_payments`)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | `String(36)` | PK | UUID |
| `organization_id` | `String(36)` | FK `organizations.id`, NOT NULL | |
| `assessment_id` | `String(36)` | FK `assessments.id`, NOT NULL | Which assessment this pays toward |
| `parcel_id` | `String(36)` | FK `parcels.id`, NOT NULL | Which parcel is paying |
| `amount` | `Float` | NOT NULL | Dollar amount paid |
| `method` | `String(20)` | NOT NULL | `check`, `electronic`, `cash`, `other` |
| `paid_date` | `Date` | NOT NULL, default `date.today` | |
| `notes` | `Text` | nullable | Check number, reference, etc. |
| `created_at` | `DateTime` | default `utcnow` | |

---

## 4. Forms

All forms are in `cove/treasury/forms.py` and inherit from `CoveForm` (which extends `FlaskForm` with automatic CSRF).

### AssessmentCreateForm

Creates a new assessment. Used by the `create_assessment` route.

| Field | Widget | Validators | Notes |
|-------|--------|------------|-------|
| `name` | `StringField` | `DataRequired`, `Length(3, 255)` | CSS class `cove-input` |
| `type` | `SelectField` | `DataRequired` | Choices: `regular` ("Regular -- annual (section 13.2 max $240/yr)"), `special_assessment` ("Special Assessment -- requires member vote") |
| `amount` | `FloatField` | `DataRequired`, `NumberRange(min=0.01)` | Label: "Amount per Lot ($)" |
| `frequency` | `SelectField` | `DataRequired` | Choices: `annual`, `quarterly`, `monthly`, `one_time` |
| `effective_date` | `DateField` | `DataRequired` | Default: `date.today` |
| `proposal_id` | `StringField` | `Optional` | Paste a proposal ID for special assessments backed by a member vote |

### PaymentRecordForm

Records a payment from a parcel against an assessment. Parcel choices are populated dynamically in the route.

| Field | Widget | Validators | Notes |
|-------|--------|------------|-------|
| `parcel_id` | `SelectField` | `DataRequired` | Choices set dynamically from org parcels (value=parcel UUID, label=address + APN) |
| `amount` | `FloatField` | `DataRequired`, `NumberRange(min=0.01)` | Label: "Amount Paid ($)" |
| `method` | `SelectField` | `DataRequired` | Choices: `check`, `electronic`, `cash`, `other` |
| `paid_date` | `DateField` | `DataRequired` | Default: `date.today` |
| `notes` | `TextAreaField` | `Optional`, `Length(max=500)` | Check number, reference, etc. |

---

## 5. Services

All service functions are in `cove/treasury/services.py`. The module imports `get_assessment_limits` from `cove/governance/bylaws_config` for bylaws enforcement.

### `create_assessment(org_id, name, type, amount, frequency, effective_date, proposal_id=None) -> Assessment`

Creates and commits an `Assessment`. For `regular` type assessments, enforces the bylaws cap: if `amount` exceeds `assessment_limits.max_annual_per_lot` (currently $200 per the config), raises `ValueError` with a message directing the user to use `special_assessment` with a member vote. Sets `approved_by_vote=True` if `proposal_id` is provided.

### `record_payment(org_id, assessment_id, parcel_id, amount, method, paid_date=None, notes=None) -> ParcelPayment`

Creates and commits a `ParcelPayment`. Defaults `paid_date` to `date.today()` if not provided.

### `get_assessment_status(org_id, assessment_id) -> list[dict]`

Returns one entry per parcel in the org with payment status against a specific assessment. Each entry contains: `parcel_id`, `apn`, `address`, `street`, `lot_number`, `amount_due`, `amount_paid`, `balance`, `status`. Status is `paid` (balance <= 0), `partial` (some payment, balance > 0), or `unpaid` (no payment). Payments are aggregated via `SUM` grouped by `parcel_id`.

### `get_delinquent_parcels(org_id, assessment_id, as_of=None) -> list[dict]`

Filters `get_assessment_status` results to parcels with status `unpaid` or `partial` where the assessment's effective date has passed. Returns empty list if the assessment doesn't exist or `as_of` is before the effective date. Not currently called by any route -- available for future delinquency reporting.

### `get_treasury_summary(org_id) -> dict`

Computes aggregate treasury metrics across all assessments for the org. Returns: `total_expected` (sum of `amount_per_lot * parcel_count` across all assessments), `total_collected` (sum of all `ParcelPayment.amount`), `collection_rate` (percentage), `assessment_count`. Used by the `index` and `budget` routes.

---

## 6. Templates

All templates are in `cove/treasury/templates/treasury/` and extend `base.html`.

| File | Route | Description |
|------|-------|-------------|
| `index.html` | `treasury.index` | Treasury dashboard. Four summary stat cards (total expected, collected, collection rate, assessment count). Assessment table with name, type badge, amount/lot, frequency, effective date, and Payments link (board only). "New Assessment" button for board. Links to budget and assessments views. Davis-Stirling compliance note in footer. |
| `assessments.html` | `treasury.assessments` | Full assessments list. Table with name, type badge, amount/lot, frequency, effective date, vote-required badge, and Payments link (board only). "New Assessment" button for board. Empty state row if no assessments. |
| `budget.html` | `treasury.budget` | Budget overview. Three summary stat cards (expected, collected, collection rate). Fiscal year budgets table with income, expense, reserve allocation, net (color-coded), and approval status badge. Empty state if no budgets. Davis-Stirling note in footer. |
| `create_assessment.html` | `treasury.create_assessment` | Assessment creation form. Yellow notice box citing section 13.2 cap. Form fields: name, type, frequency, amount, effective date, proposal ID. Inline field-level error display. Cancel link returns to assessments list. |
| `record_payment.html` | `treasury.record_payment` | Payment recording. Header shows assessment name, amount/lot, frequency, and effective date. Payment form with parcel selector, amount, method, date, and notes. Below the form: per-parcel payment status table showing address, APN, amount due, amount paid, balance (color-coded), and status badge (paid/partial/unpaid). |

---

## 7. Access Control

| Role | Capabilities |
|------|-------------|
| **Any authenticated member** | View treasury index (summary + assessment list), assessments list, and budget overview. All three read routes require `@login_required` only. |
| **Board member** (`current_user.is_board`) | All of the above, plus: create assessments, record payments, see "Payments" links on assessment rows, see "New Assessment" buttons. The `create_assessment` and `record_payment` routes check `is_board` and return `abort(403)` if the user is not a board member. |
| **Non-board member** | Cannot access create or payment routes (HTTP 403). Cannot see "New Assessment" buttons or "Payments" links in templates (Jinja conditional on `current_user.is_board`). |

All routes are tenant-scoped by `current_user.organization_id`. The `record_payment` route additionally verifies the assessment belongs to the user's organization (404 if not).

---

## 8. Bylaws Config Integration

The treasury module reads assessment limits from `cove/governance/wpbca-bylaws-config.json` via `cove/governance/bylaws_config.get_assessment_limits()`.

**Config section used:**

```json
"assessment_limits": {
    "max_annual_per_lot": 200,
    "bylaw_section": "§13.2",
    "delinquency_notice_days": 120,
    "delinquency_bylaw": "Davis-Stirling §5660"
}
```

**How it is used:**

- `services.create_assessment()` calls `get_assessment_limits()` and reads `max_annual_per_lot`. If the assessment type is `regular` and the amount exceeds this value, a `ValueError` is raised, preventing creation. This enforces WPBCA Bylaws section 13.2 at the service layer.
- The `delinquency_notice_days` (120) and `delinquency_bylaw` values are available for future delinquency notice enforcement but are not currently referenced in code.
- Template compliance notes reference "$240/lot" (the original bylaws text), while the config value is `200`. This discrepancy should be reconciled -- either the config or the template references need updating to reflect the current maximum.

---

## 9. Davis-Stirling Compliance

| Civil Code Section | Relevance | Implementation |
|--------------------|-----------|----------------|
| **Bylaws §13.2** | Maximum annual regular assessment per lot without member vote. | `services.create_assessment()` enforces the cap from bylaws config. Regular assessments exceeding the limit are rejected with a `ValueError`. Special assessments require a proposal ID linking to a member vote. |
| **Civil Code §5660** | 120-day written notice required before recording a lien for delinquent assessments. | `services.get_delinquent_parcels()` identifies parcels with unpaid/partial balances past the effective date. The 120-day notice period is stored in config (`delinquency_notice_days: 120`) but automated notice generation is not yet implemented. |
| **Civil Code §5600** | Regular assessments may not exceed the amount specified in the governing documents without a member vote. | Enforced by the `max_annual_per_lot` check in `create_assessment`. The form UI labels regular assessments with the section 13.2 cap and directs users to special assessment type for amounts above the limit. |
| **Civil Code §5605** | Special assessments require approval by a majority vote of the membership at a duly noticed meeting (quorum of 50%). | The `AssessmentCreateForm` includes a `proposal_id` field to link special assessments to an approved governance proposal. The `special_assessment` proposal type in bylaws config requires 50% quorum and secret ballot. |
| **SB 900 (2026)** | Emergency assessments for utility repairs within 14 days without member vote. | Not yet implemented. Config includes `SB_900` in `legislative_compliance` for tracking. |

**APN-based assessment identity:** Assessments are tied to parcels, not members. A parcel owes regardless of ownership transfer. This mirrors property tax semantics and is consistent throughout the module -- models use `parcel_id` foreign keys, services iterate over org parcels, and templates display APN alongside address.
