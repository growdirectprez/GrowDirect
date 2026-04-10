# Fox

## Overview

Fox is Canary LP's case management and evidence locker domain -- "The Vault" in the mobile UX. It bridges automated anomaly detection (Chirp alerts) and human investigation workflows. When a merchant decides an alert warrants investigation, Fox creates a case, links originating alerts, tracks subjects of interest, stores evidence with chain-of-custody integrity, and maintains an append-only audit timeline.

**Blueprints:**

| Blueprint | Prefix | Purpose |
|---|---|---|
| `fox_wired` (`canary/blueprints/fox_wired.py`) | `/api/fox` | REST API -- CRUD for cases, evidence, subjects, actions, timeline |
| `fox_mcp` (`canary/blueprints/fox_mcp.py`) | `/fox` | MCP server -- manifest, tools list, tool invocation, health |

**Services:**

| Module | Purpose |
|---|---|
| `canary/services/fox/case_service.py` | `FoxCaseService` -- all Fox business logic, session-injected |
| `canary/services/fox/tools.py` | 8 MCP tool definitions for `canary-fox` server |
| `canary/services/hash_chain.py` | General-purpose chain verification (pipe-delimited, hex strings) |
| `canary/services/evidence_chain.py` | WH-03 BYTEA chain hash (raw bytes, separate data path) |

**Design principles:**

- Evidence tables are INSERT-ONLY -- enforced by PostgreSQL triggers, not application code
- Operational tables (cases, subjects, actions) use soft-delete via `SoftDeleteMixin`
- Hash chain on evidence is computed by a PostgreSQL BEFORE INSERT trigger -- the app cannot forge chain values
- Evidence stores GUID references to RaaS raw data, not copies (Canary is a lens)
- Access logging tracks who viewed what, when, and from where

**Inbound contracts:**

| From | Contract |
|---|---|
| Owl | `FoxCaseService.create_case()` via action dispatcher (case_create) |
| UI/BFF | `FoxCaseService.create_case_from_context()` -- unified case creation from alerts, txns, drill paths (GRO-245) |
| UI/BFF | CRUD on cases, evidence, subjects via REST or MCP |

**Outbound contracts:**

| To | Contract |
|---|---|
| Alert | Reads linked alerts via `fox_case_alerts` junction table |
| Alert | Writes `AlertHistory` (status=case_opened) when linking alerts via `create_case_from_context()` (GRO-245) |

**Dependencies:** SQLAlchemy 2.0 (Mapped[] syntax), Flask blueprints, `canary.mcp` base kit (MCPTool, MCPRegistry, create_mcp_blueprint), `canary.middleware.jwt_auth` (jwt_required, roles_required), `canary.db.session_factory` (get_session).


## API Contracts

### REST Endpoints (`fox_wired` -- `/api/fox/*`)

All require JWT authentication. Write operations require `owner`, `operator`, or `admin` roles.

| Method | Endpoint | Role Gate | Purpose |
|---|---|---|---|
| GET | `/cases` | -- | List cases (paginated, filterable by status/created_after) |
| POST | `/cases` | owner/operator/admin | Create case (title required, optional alert_id link) |
| GET | `/cases/<case_id>` | -- | Get single case details |
| PUT | `/cases/<case_id>` | owner/operator/admin | Update case status (validated transitions) |
| POST | `/cases/<case_id>/subjects` | owner/operator/admin | Add subject (type + entity_id required) |
| POST | `/cases/<case_id>/evidence` | owner/operator/admin | Upload evidence (multipart file) |
| GET | `/cases/<case_id>/evidence` | -- | List evidence for case |
| GET | `/cases/<case_id>/evidence/<eid>` | -- | Get single evidence item (logs access) |
| GET | `/cases/<case_id>/evidence/verify` | -- | Verify evidence hash chain integrity |
| GET | `/cases/<case_id>/timeline` | -- | Get merged timeline (events + access logs) |
| POST | `/cases/<case_id>/actions` | owner/operator/admin | Add investigation action |

**Error responses:** 400 (validation, invalid transition), 404 (not found), 500 (unhandled, logged).

### MCP Tools (`canary-fox` -- `/fox/*`)

8 tools, all DB-dependent. Registered via `MCPRegistry` in `canary/services/fox/tools.py`. Each tool opens its own session via `get_session()` and closes in `finally`.

| Tool | Category | Description |
|---|---|---|
| `create_case` | cases | Open a case with title, description, priority, optional alert link. Returns case_id + case_number. |
| `get_case` | cases | Get full case details by ID -- status, priority, subjects, evidence count. |
| `list_cases` | cases | List cases with optional status/date filters. Paginated (max 50/page). |
| `update_case_status` | cases | Transition status through lifecycle state machine. Validates transitions. Writes timeline + action. |
| `add_subject` | cases | Link employee/vendor/external party to a case with type, entity_id, optional name and role. |
| `get_timeline` | cases | Get append-only audit trail -- case events merged with evidence access logs, chronological. |
| `verify_chain` | evidence | Verify evidence hash chain via PostgreSQL `verify_hash_chain()`. Returns valid/invalid + broken_at position. |
| `link_alert` | cases | Link an alert to an existing case. Idempotent -- returns already_linked if duplicate. |

### MCP Blueprint Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /fox/manifest` | Server manifest (name, version, tool count) |
| `GET /fox/tools` | List all 8 tools with schemas |
| `POST /fox/tools/<name>` | Invoke a tool by name |
| `GET /fox/health` | Health check (service name, healthy flag, tool count) |


## Data Model

All tables live in the `app` schema of the `canary` database. Seven tables in three logical tiers.

### Tier 1 -- Investigation Records (CRUD + soft-delete)

**fox_cases:** Root investigation record. PK: `id` (UUID). Tenant-scoped by `merchant_id` (FK merchants.id). Key fields: `case_number` (CASE-YYYY-NNNNN, unique per merchant per year), `title`, `description`, `case_type` (theft/fraud/policy_violation/cash_variance/return_abuse/transaction_review/other), `priority` (low/medium/high/critical), `status` (see Workflows), `assigned_to`, `opened_by`, `opened_at`, `closed_at`, `resolution`, `total_loss_cents`. Mixins: TenantMixin, AuditMixin, SoftDeleteMixin. Indexes: (merchant_id, status), (merchant_id, case_type), (merchant_id, assigned_to), (case_number UNIQUE).

**fox_case_alerts:** Junction table linking alerts to cases. PK: `id` (UUID). Fields: `case_id` (FK fox_cases.id), `alert_id` (String, cross-DB reference), `linked_at`, `linked_by`, `notes`. Mixin: AuditMixin. Indexes: (case_id), (alert_id).

**fox_subjects:** Persons/entities of interest linked to cases. PK: `id` (UUID). Fields: `merchant_id` (FK), `case_id` (FK), `subject_type` (employee/customer/vendor/unknown), `entity_id` (cross-DB FK), `name`, `role_in_case`, `is_primary_suspect` (default False). Mixins: TenantMixin, AuditMixin, SoftDeleteMixin. Indexes: (case_id), (merchant_id), (entity_id), (is_primary_suspect).

**fox_case_actions:** Investigation actions. PK: `id` (UUID). Fields: `case_id` (FK), `merchant_id` (FK), `action_type` (investigate/interview/suspend/terminate/refer_to_le/refer_to_hr/coaching/no_action/status_change), `description`, `performed_by`, `performed_at`, `outcome`. Mixins: TenantMixin, AuditMixin, SoftDeleteMixin. Indexes: (case_id), (merchant_id), (action_type).

### Tier 2 -- Immutable Audit Trail (APPEND-ONLY)

**fox_case_timeline:** Append-only event log. PK: `id` (UUID). Fields: `case_id` (FK), `merchant_id` (FK), `event_type` (created/status_change/note_added/evidence_added/assigned/escalated/closed/alert_linked/action_added), `actor_id`, `description`, `meta_data` (JSON, Python column mapped to DB column `metadata`), `occurred_at` (authoritative timestamp). No AuditMixin, no SoftDeleteMixin -- the timeline IS the audit trail. Indexes: (case_id), (merchant_id), (event_type), (occurred_at). Protected by INSERT-ONLY DB trigger (no UPDATE, no DELETE).

### Tier 3 -- Evidentiary Chain (INSERT-ONLY, hash-chained)

**fox_evidence:** INSERT-ONLY evidence records with cryptographic hash chain. PK: `id` (UUID). Fields: `merchant_id` (FK), `case_id` (FK), `evidence_type` (document/photo/video/receipt/screenshot/export/other), `file_name`, `file_path` (storage path), `file_hash` (SHA-256 of file content, computed by app), `file_size_bytes`, `content_type`, `description`, `uploaded_by`, `uploaded_at`, `previous_chain_hash` (NULL for genesis), `chain_hash` (SHA-256, computed by DB trigger). Indexes: (case_id), (merchant_id), (uploaded_at), (file_hash). DB triggers: `compute_entry_hash()` BEFORE INSERT overwrites chain_hash; immutability trigger blocks UPDATE/DELETE.

**fox_evidence_access_log:** INSERT-ONLY access audit. PK: `id` (UUID). Fields: `evidence_id` (FK fox_evidence.id), `accessed_by`, `access_type` (view/download/print/export/upload), `accessed_at`, `ip_address` (IPv4/IPv6). Indexes: (evidence_id), (accessed_at), (accessed_by). DB triggers: immutability trigger blocks UPDATE/DELETE.

### Hash Chain Pattern

Two distinct algorithms coexist in the codebase:

| Module | Algorithm | Storage | Used By |
|---|---|---|---|
| `hash_chain.py` | `sorted_json + "\|" + prev_hash` | 64-char hex string | fox_evidence (via DB trigger), audit_log |
| `evidence_chain.py` | `prev_bytes \|\| event_bytes` (raw concat) | 32 bytes (BYTEA) | evidence_records (WH-03 spec, separate data path) |

The DB trigger (`compute_entry_hash()`) is the single source of truth for fox_evidence chain hashes. The app sends `chain_hash="TRIGGER_WILL_OVERWRITE"` as a placeholder; the trigger overwrites it. Even a compromised application cannot forge a valid chain.


## Workflows

### Case Lifecycle State Machine

Cases follow a strict state machine enforced by `FoxCaseService.update_case_status()`. Invalid transitions raise `ValueError` (returned as HTTP 400).

```
open --> investigating --> pending_review --> escalated --> closed
                                         \-> closed      \-> referred_to_le
                                         \-> referred_to_le

closed          (terminal -- no transitions out)
referred_to_le  (terminal -- no transitions out)
```

Every status transition writes both a `fox_case_timeline` entry (event_type=status_change, with old/new status in metadata) and a `fox_case_actions` record.

### Alert-to-Case Flow

1. Chirp alert detected (status: new)
2. Merchant taps "Open case" in UI, or Owl action dispatcher fires `case_create`
3. `POST /api/fox/cases` or MCP `create_case` tool
4. `FoxCaseService.create_case()`:
   - Generates case_number: `CASE-{year}-{sequence:05d}` (per merchant per year)
   - Inserts `FoxCase` (status=open)
   - Inserts `FoxCaseTimeline` (event_type=created)
   - If alert_id provided: inserts `FoxCaseAlert` junction record
5. Alert domain writes `AlertHistory` (status=case_opened) via its own action dispatcher

### Evidence Upload and Chain Hash

1. `POST /api/fox/cases/<id>/evidence` (multipart file) or MCP tool
2. `FoxCaseService.add_evidence()`:
   - Python computes `SHA-256(file_data)` -> `file_hash`
   - Inserts `FoxEvidence` with `chain_hash="TRIGGER_WILL_OVERWRITE"`
   - PostgreSQL BEFORE INSERT trigger fires:
     - Finds previous evidence for this case (ordered by uploaded_at DESC)
     - Genesis: `chain_hash = SHA-256(file_hash)`, `previous_chain_hash = NULL`
     - Subsequent: `chain_hash = SHA-256(prev_chain_hash + file_hash)`, links previous
   - `session.flush()` commits trigger values; `session.refresh()` reads them back
   - Inserts `FoxCaseTimeline` (event_type=evidence_added)
   - Blueprint also inserts `FoxEvidenceAccessLog` (access_type=upload)

### Evidence Access Logging

Every `GET /api/fox/cases/<id>/evidence/<eid>` inserts a `FoxEvidenceAccessLog` record (access_type=view, ip_address captured). The access log is INSERT-ONLY -- no mechanism exists to hide or delete access records.

### Chain Verification

`GET /api/fox/cases/<id>/evidence/verify` or MCP `verify_chain` tool:

1. Finds most recent evidence for the case
2. If none: returns `{valid: true, total_evidence: 0}`
3. Calls PostgreSQL `verify_hash_chain(table, record_id, merchant_id)` for server-side verification
4. Returns `{valid: bool, total_evidence: int, broken_at: int|null}`
5. Graceful degradation: if DB function not deployed, returns `valid: null` with explanatory message

### Timeline Assembly

`get_case_timeline()` merges two data sources into a single chronological stream:

1. `FoxCaseTimeline` entries (case events, sorted by `occurred_at`)
2. `FoxEvidenceAccessLog` entries (evidence access, joined through `FoxEvidence`, sorted by `accessed_at`)

Both are combined and sorted by timestamp for a unified audit view. Paginated (default 50 per page).

### Case Number Generation

Auto-generated per merchant per year: `CASE-{year}-{sequence:05d}`. The sequence counts existing cases for the merchant in the current year. Not globally unique -- unique per merchant.

- Uses `SELECT count(*) ... WITH FOR UPDATE` to prevent race conditions on concurrent case creation within a single merchant/year partition
- Sequence is derived from row count, not a DB sequence -- no gaps but requires row-level lock

### Unified Case Creation from Context (GRO-245)

Entry point: `FoxCaseService.create_case_from_context()`. Single method for case creation from any UI touchpoint -- alerts, transactions, or drill path filters.

- **Params:** `merchant_id`, `user_id`, plus optional `alert_ids`, `txn_ids`, `drill_filters`, `title`, `description`, `priority`
- **Auto-title:** generates contextual title if none provided (e.g. "Case from 3 alert(s)", "Transaction review: 2 txn(s)", "Drill path investigation")
- **Auto-description:** builds description from linked context counts
- **Case type:** sets `transaction_review` when `txn_ids` present, otherwise `other`
- **Alert linking:** first alert linked at creation via `create_case()`, additional alerts linked individually as `FoxCaseAlert` records
- **AlertHistory updates:** writes `AlertHistory` (status=`case_opened`) for every linked alert, with case number in notes
- **Returns:** `{ok, case_id, case_number, evidence_count}` where `evidence_count` = len(alert_ids) + len(txn_ids)
- **Delegates to:** `create_case()` internally -- inherits all validation (case_type, priority, case number generation)

### Subject Entity Resolution (GRO-246)

Entry point: `resolve_entity(db_session, subject_type, entity_id)`. Called by `add_subject()` before linking a subject to a case.

- **employee:** queries `Employee.id` -- raises `ValueError` if not found
- **customer/vendor:** resolution deferred -- no canonical lookup table yet, returns `True`
- **unknown:** no resolution needed, returns `True`
- Validated against `VALID_SUBJECT_TYPES` frozenset: `{employee, customer, vendor, unknown}`

### Timeline Metadata Validation (GRO-246)

Entry point: `validate_timeline_metadata(event_type, metadata)`. Validates JSON schema per event type before timeline insert.

- Accepts `dict`, JSON string, or `None` (treated as `{}`)
- Raises `ValueError` on malformed JSON or missing required keys
- Required keys per event_type:
  - `status_change`: `old_status`, `new_status`
  - `evidence_added`: `evidence_id`
  - `assigned`: `assigned_to`
  - `created`, `note_added`, `escalated`, `closed`, `action_added`: no required keys
- Called by: `add_evidence()`, `update_case_status()` -- validates before timeline insert

### Enum Validation (GRO-246)

All enums enforced as module-level `frozenset` constants in `case_service.py`. Validation raises `ValueError` with the invalid value and sorted valid options.

| Frozenset | Values | Validated By |
|---|---|---|
| `VALID_PRIORITIES` | low, medium, high, critical | `create_case()` |
| `VALID_CASE_TYPES` | theft, fraud, policy_violation, cash_variance, return_abuse, transaction_review, other | `create_case()` |
| `VALID_STATUSES` | open, investigating, pending_review, escalated, closed, referred_to_le | `update_case_status()` |
| `VALID_ACTION_TYPES` | investigate, interview, suspend, terminate, refer_to_le, refer_to_hr, coaching, no_action, status_change | `add_action()` |
| `VALID_SUBJECT_TYPES` | employee, customer, vendor, unknown | `add_subject()` |
| `VALID_TIMELINE_EVENT_TYPES` | created, status_change, note_added, evidence_added, assigned, escalated, closed, action_added | Reference only (timeline inserts use literal strings) |

- `transaction_review` added to `VALID_CASE_TYPES` for `create_case_from_context()` flows
- `status_change` added to `VALID_ACTION_TYPES` for status transition action records

---
*Canary LP | GrowDirect Inc. | Confidential*
