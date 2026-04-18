# Fox Case Management

> **Status:** Complete — written from code
> **Namespace:** canary
> **Last updated:** 2026-03-30
> **Code location:** `Canary/canary/services/fox/`, `Canary/canary/models/fox/`

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

---

## 1. Overview

Fox is Canary's investigation case management system. It gives loss prevention teams a structured, tamper-evident workspace to track suspected incidents from initial alert through resolution — including referring cases to law enforcement when warranted.

Fox receives cases in two ways: automatically, when Chirp detection rules fire (Owl's `create_case_from_context` bridge), and manually, when an investigator opens a case from the Fox UI or via the MCP agent interface. Every case carries a lifecycle state machine, an append-only timeline, an evidence locker with a cryptographic hash chain enforced by a PostgreSQL trigger, and a complete chain-of-custody access log.

The core design principle is **evidentiary integrity**: evidence cannot be modified or deleted after upload. The hash chain proves insertion order and detects tampering. This makes Fox records defensible in HR proceedings and law enforcement referrals.

**Supported case types:** theft, fraud, policy violation, cash variance, return abuse, transaction review, other.

**Status lifecycle:** open → investigating → pending review → escalated → closed / referred to law enforcement.

---

## 2. Architecture

### Component Diagram

```
┌───────────────────────────────────────────────────────────────┐
│  Canary Flask App                                             │
│                                                               │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │ fox_wired   │    │  fox_mcp     │    │  owl_api       │  │
│  │ Blueprint   │    │  Blueprint   │    │  Blueprint     │  │
│  │ /api/fox/*  │    │  /fox/*      │    │ (bridge)       │  │
│  └──────┬──────┘    └──────┬───────┘    └───────┬────────┘  │
│         │                  │                     │            │
│         └──────────────────┼─────────────────────┘            │
│                            ↓                                  │
│                  ┌─────────────────┐                          │
│                  │ FoxCaseService  │                          │
│                  │ case_service.py │                          │
│                  └────────┬────────┘                          │
│                           │                                   │
│       ┌───────────────────┼────────────────────┐             │
│       ↓                   ↓                    ↓             │
│  ┌─────────┐      ┌───────────────┐     ┌──────────┐        │
│  │FoxCase  │      │ FoxEvidence   │     │FoxSubject│        │
│  │Timeline │      │ AccessLog     │     │          │        │
│  │Action   │      │               │     │          │        │
│  │Alert    │      └───────┬───────┘     └──────────┘        │
│  └─────────┘              │                                   │
│                           ↓                                   │
│                  ┌────────────────────┐                       │
│                  │ PostgreSQL Trigger │                       │
│                  │ compute_entry_hash │                       │
│                  │ verify_hash_chain  │                       │
│                  └────────────────────┘                       │
└───────────────────────────────────────────────────────────────┘
```

**MCP server:** `canary-fox` — registered at port 8001 within the Canary Owl MCP layer. The `fox_mcp_bp` blueprint wires the `MCPRegistry` (from `canary.services.fox.tools`) to HTTP endpoints via `create_mcp_blueprint`.

**REST API:** `fox_wired.py` registers the `fox` Flask blueprint at `/api/fox/*`. This is the primary human-facing interface.

**Bridge from Chirp/Owl:** `canary/blueprints/owl_api.py` calls `FoxCaseService.create_case_from_context()` when an agent or automation decides a Chirp alert warrants a formal case.

### Request / Data Flow

**Manual case creation (REST):**
```
POST /api/fox/cases
  → jwt_required() + roles_required(owner|operator|admin)
  → FoxCaseService.create_case(merchant_id, data)
    → Validate case_type, priority against frozensets
    → Generate case_number: CASE-{year}-{sequence:05d}
    → INSERT fox_cases
    → INSERT fox_case_timeline (event_type=created)
    → INSERT fox_case_alerts if alert_id provided
  → 201 {case_id, case_number, status}
```

**Evidence upload:**
```
POST /api/fox/cases/<case_id>/evidence (multipart/form-data)
  → jwt_required() + roles_required(owner|operator|admin)
  → Read file bytes → compute SHA-256 file_hash in Python
  → FoxCaseService.add_evidence(case_id, file_data, metadata)
    → INSERT fox_evidence (chain_hash="TRIGGER_WILL_OVERWRITE")
    → PostgreSQL BEFORE INSERT trigger fires:
        compute_entry_hash() computes:
          previous_chain_hash = chain_hash of last evidence in case
          chain_hash = SHA-256(previous_chain_hash + file_hash)
        Overwrites chain_hash and previous_chain_hash before commit
    → db.flush() → db.refresh(fox_evidence)  [reads trigger result]
    → INSERT fox_case_timeline (event_type=evidence_added)
    → FoxCaseService.log_evidence_access(evidence_id, user_id, "upload", ip)
  → 201 {evidence_id, file_hash, chain_hash, previous_chain_hash}
```

**Status transition:**
```
PUT /api/fox/cases/<case_id>  {"status": "investigating"}
  → jwt_required() + roles_required(owner|operator|admin)
  → FoxCaseService.update_case_status(case_id, new_status, actor_id, notes)
    → Validate new_status against VALID_STATUSES
    → Validate transition via valid_transitions dict
    → UPDATE fox_cases.status
    → INSERT fox_case_timeline (event_type=status_change, metadata={old,new})
    → INSERT fox_case_actions (action_type=status_change)
  → 200 {case_id, status, previous_status}
```

**Auto-case from Chirp (Owl bridge):**
```
Chirp fires detection rule (e.g., C-301, C-502)
  → Owl alert created in canary.app schema
  → owl_api.py calls FoxCaseService.create_case_from_context(
        merchant_id, user_id,
        alert_ids=[...],
        txn_ids=[...],
        drill_filters=[...]
    )
    → Derives title and description from context inputs
    → Calls create_case() with case_type=transaction_review
    → Links first alert at creation time, subsequent alerts via FoxCaseAlert
    → Writes AlertHistory records (status=case_opened) for each linked alert
  → Returns {ok, case_id, case_number, evidence_count}
```

### Key Design Decisions

**Hash chain in the database, not in application code.** The `compute_entry_hash()` PostgreSQL BEFORE INSERT trigger is the sole authority for `chain_hash` and `previous_chain_hash`. Application code explicitly passes `chain_hash="TRIGGER_WILL_OVERWRITE"` as a placeholder. After flush, `db.refresh()` reads back the trigger-computed values. This prevents application bugs or concurrent inserts from breaking the chain. Reference: `TOM_SESSION_OUTPUT_B-001_2026-02-24.md`, migration P0-3.

**INSERT-only evidence and access log tables.** `FoxEvidence` and `FoxEvidenceAccessLog` have no `update()` or `delete()` methods. The database has triggers enforcing this. Any attempt to UPDATE or DELETE a row fails at the database layer. This is not a convention — it is a hard constraint.

**Append-only timeline.** `FoxCaseTimeline` intentionally omits `AuditMixin` (which adds `modified_by`/`modified_at`). The timeline IS the audit trail; it uses only `occurred_at`. No rows are ever modified.

**State machine enforced in the service layer.** The valid transition graph is a dict in `FoxCaseService.update_case_status()`. Attempts to skip states (e.g., `open → closed`) raise `ValueError` before any database write. Terminal states (`closed`, `referred_to_le`) have empty allowed-transition lists.

**Timeline metadata schema validation.** `validate_timeline_metadata()` enforces per-event-type required keys: `status_change` requires `{old_status, new_status}`, `evidence_added` requires `{evidence_id}`, `assigned` requires `{assigned_to}`. Called before every timeline INSERT.

**Case number generation.** Case numbers are formatted `CASE-{year}-{sequence:05d}`, scoped per merchant per year. The sequence is derived from a `COUNT()` query — uniqueness is enforced by the `UNIQUE` index on `fox_cases.case_number`, not by a lock. Concurrent case creation for the same merchant in the same second may result in a uniqueness conflict, which the caller must retry.

**Dual interface.** Fox exposes both a REST API (`fox_wired.py`) and an MCP tool registry (`fox_mcp.py`). The MCP tools are consumed by the Owl agent for conversational case management. Both interfaces delegate to the same `FoxCaseService`.

---

## 3. Data Model

All Fox tables live in the `app` schema of the `canary` database.

---

### FoxCase

Root investigation record. Implements `AppBase`, `TenantMixin`, `AuditMixin`, `SoftDeleteMixin`.

```python
class FoxCase(AppBase, TenantMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = "fox_cases"

    id: Mapped[str]                         # UUID PK (String 36)
    merchant_id: Mapped[str]                # FK → merchants.id
    case_number: Mapped[str]                # CASE-{year}-{seq:05d}, UNIQUE
    title: Mapped[str]                      # Short description
    description: Mapped[str]               # Full narrative (Text)
    case_type: Mapped[str]                  # theft|fraud|policy_violation|
                                            #   cash_variance|return_abuse|
                                            #   transaction_review|other
    priority: Mapped[str]                   # low|medium|high|critical, default=medium
    status: Mapped[str]                     # open|investigating|pending_review|
                                            #   escalated|closed|referred_to_le
    assigned_to: Mapped[Optional[str]]      # User ID, nullable
    opened_by: Mapped[str]                  # User ID or "system"
    opened_at: Mapped[datetime]             # server_default=now()
    closed_at: Mapped[Optional[datetime]]   # Set on terminal status transition
    resolution: Mapped[Optional[str]]       # Final narrative (Text)
    total_loss_cents: Mapped[int]           # Aggregate loss, default=0

    subjects: Mapped[list["FoxSubject"]]    # cascade all, delete-orphan
    timeline: Mapped[list["FoxCaseTimeline"]]
    actions: Mapped[list["FoxCaseAction"]]
    alerts: Mapped[list["FoxCaseAlert"]]
    evidence: Mapped[list["FoxEvidence"]]   # viewonly
```

**Indexes:** `(merchant_id, status)`, `(merchant_id, case_type)`, `(merchant_id, assigned_to)`, UNIQUE on `case_number`.

---

### FoxCaseAlert

Junction table linking cases to Chirp alerts. Implements `AppBase`, `AuditMixin`.

```python
class FoxCaseAlert(AppBase, AuditMixin):
    __tablename__ = "fox_case_alerts"

    id: Mapped[str]             # UUID PK
    case_id: Mapped[str]        # FK → fox_cases.id
    alert_id: Mapped[str]       # Cross-DB string reference to alert.id
    linked_at: Mapped[datetime] # server_default=now()
    linked_by: Mapped[str]      # User ID
    notes: Mapped[Optional[str]]
```

`alert_id` is a string cross-schema reference — `fox_case_alerts` and the `alerts` table live in the same database but Alembic does not enforce a foreign key constraint across schemas. Lookup is by string equality.

**Indexes:** `alert_id`, `case_id`.

---

### FoxCaseTimeline

Append-only event log. No `AuditMixin`. INSERT-only by convention (no DB trigger on this table, but no application code modifies rows).

```python
class FoxCaseTimeline(AppBase):
    __tablename__ = "fox_case_timeline"

    id: Mapped[str]                     # UUID PK
    case_id: Mapped[str]                # FK → fox_cases.id
    merchant_id: Mapped[str]            # FK → merchants.id (denormalized for partition-ready queries)
    event_type: Mapped[str]             # created|status_change|note_added|
                                        #   evidence_added|assigned|escalated|
                                        #   closed|action_added
    actor_id: Mapped[str]               # User ID or "system"
    description: Mapped[str]           # Human-readable summary (Text)
    meta_data: Mapped[Optional[str]]    # JSON blob, column name = "metadata"
    occurred_at: Mapped[datetime]       # server_default=now()
```

**Required metadata keys by event type:**
- `status_change`: `{old_status, new_status}`
- `evidence_added`: `{evidence_id}`
- `assigned`: `{assigned_to}`
- `created`, `note_added`, `escalated`, `closed`, `action_added`: no required keys

**Indexes:** `case_id`, `merchant_id`, `event_type`, `occurred_at`.

---

### FoxCaseAction

Investigation outcome record. Implements `AppBase`, `TenantMixin`, `AuditMixin`, `SoftDeleteMixin`.

```python
class FoxCaseAction(AppBase, TenantMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = "fox_case_actions"

    id: Mapped[str]                     # UUID PK
    case_id: Mapped[str]                # FK → fox_cases.id
    merchant_id: Mapped[str]            # FK → merchants.id
    action_type: Mapped[str]            # investigate|interview|suspend|terminate|
                                        #   refer_to_le|refer_to_hr|coaching|
                                        #   no_action|status_change
    description: Mapped[str]           # What was done (Text)
    performed_by: Mapped[str]           # User ID
    performed_at: Mapped[datetime]      # server_default=now()
    outcome: Mapped[Optional[str]]      # Result of the action (Text, nullable)
```

**Indexes:** `case_id`, `merchant_id`, `action_type`.

---

### FoxEvidence

INSERT-ONLY evidence file record. No `AuditMixin`, no `SoftDeleteMixin`. DB trigger enforces immutability.

```python
class FoxEvidence(AppBase):
    __tablename__ = "fox_evidence"

    id: Mapped[str]                         # UUID PK
    merchant_id: Mapped[str]                # FK → merchants.id
    case_id: Mapped[str]                    # FK → fox_cases.id
    evidence_type: Mapped[str]              # document|photo|video|receipt|
                                            #   screenshot|export|other
    file_name: Mapped[str]                  # Original filename (String 512)
    file_path: Mapped[str]                  # Storage path (Text) — DEFERRED: S3
    file_hash: Mapped[str]                  # SHA-256 of file content (hex, 64 chars)
    file_size_bytes: Mapped[int]
    content_type: Mapped[Optional[str]]     # MIME type
    description: Mapped[Optional[str]]      # Evidence description
    uploaded_by: Mapped[str]                # User ID
    uploaded_at: Mapped[datetime]           # server_default=now()
    previous_chain_hash: Mapped[Optional[str]]  # chain_hash of prior evidence row
                                                 # NULL for first evidence in case
    chain_hash: Mapped[str]                 # SHA-256(previous_chain_hash + file_hash)
                                            # Set by DB trigger, NOT by application code

    access_log: Mapped[list["FoxEvidenceAccessLog"]]
```

**Hash chain computation (PostgreSQL trigger `compute_entry_hash`):**
1. On BEFORE INSERT, the trigger reads the most recent `chain_hash` from `fox_evidence` for the same `case_id` → this becomes `previous_chain_hash`.
2. Computes `chain_hash = SHA-256(previous_chain_hash || file_hash)`. For the first record, `previous_chain_hash` is NULL and the hash covers only `file_hash`.
3. Overwrites the application-supplied placeholder values before the row is written.

**Indexes:** `case_id`, `merchant_id`, `uploaded_at`, `file_hash`.

---

### FoxEvidenceAccessLog

INSERT-ONLY chain-of-custody access record. No `AuditMixin`. DB trigger enforces immutability.

```python
class FoxEvidenceAccessLog(AppBase):
    __tablename__ = "fox_evidence_access_log"

    id: Mapped[str]             # UUID PK
    evidence_id: Mapped[str]    # FK → fox_evidence.id
    accessed_by: Mapped[str]    # User ID or external identity
    access_type: Mapped[str]    # view|download|print|export
    accessed_at: Mapped[datetime]   # server_default=now()
    ip_address: Mapped[Optional[str]]   # IPv4/IPv6, String 45
```

**Indexes:** `evidence_id`, `accessed_at`, `accessed_by`.

---

### FoxSubject

A person or entity of interest. Implements `AppBase`, `TenantMixin`, `AuditMixin`, `SoftDeleteMixin`.

```python
class FoxSubject(AppBase, TenantMixin, AuditMixin, SoftDeleteMixin):
    __tablename__ = "fox_subjects"

    id: Mapped[str]                         # UUID PK
    merchant_id: Mapped[str]                # FK → merchants.id
    case_id: Mapped[str]                    # FK → fox_cases.id
    subject_type: Mapped[str]               # employee|customer|vendor|unknown
    entity_id: Mapped[Optional[str]]        # FK to actual entity, cross-DB
    name: Mapped[str]                       # Display name
    role_in_case: Mapped[Optional[str]]     # Free text, e.g., "Cashier, drawer #3"
    is_primary_suspect: Mapped[bool]        # default=False
```

For `subject_type=employee`, `entity_id` is resolved against `canary.models.app.employees.Employee` before insert. Customer and vendor resolution is deferred pending canonical lookup tables.

**Indexes:** `case_id`, `merchant_id`, `entity_id`, `is_primary_suspect`.

---

## 4. Interfaces

### REST API — `fox_wired.py` Blueprint (`/api/fox`)

All routes require `@jwt_required()`. Mutation routes additionally require `@roles_required("owner", "operator", "admin")`. Merchant scope is taken from `g.merchant_id` (set by JWT middleware). Actor identity is taken from `g.user_id`.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/cases` | jwt | List cases, filter by `status`, `created_after`, paginate with `page`/`limit` |
| POST | `/cases` | jwt + role | Create case. Body: `{title, description?, priority?, assigned_to?, alert_id?, case_type?}` |
| GET | `/cases/<case_id>` | jwt | Get case by ID |
| PUT | `/cases/<case_id>` | jwt + role | Update case. Only `status` transitions are handled today |
| POST | `/cases/<case_id>/subjects` | jwt + role | Add subject. Body: `{type, entity_id, name?, role?}` |
| POST | `/cases/<case_id>/evidence` | jwt + role | Upload evidence. Multipart: `file` + form fields `evidence_type`, `description` |
| GET | `/cases/<case_id>/evidence` | jwt | List all evidence for a case, ordered by `uploaded_at` asc |
| GET | `/cases/<case_id>/evidence/<evidence_id>` | jwt | Get single evidence record. Logs `view` access. |
| GET | `/cases/<case_id>/evidence/verify` | jwt | Verify hash chain integrity |
| GET | `/cases/<case_id>/timeline` | jwt | Get merged timeline + access log, sorted by timestamp, paginated |
| POST | `/cases/<case_id>/actions` | jwt + role | Add action. Body: `{action_type, description}` |

**Response shapes:**

`GET /cases` → `{cases: [FoxCase.to_dict()], pagination: {page, limit, total, pages}}`

`POST /cases` → 201 `{case_id, case_number, status}`

`POST /cases/<id>/evidence` → 201 `{evidence_id, file_hash, chain_hash, previous_chain_hash}`

`GET /cases/<id>/evidence/verify` → `{valid: bool|null, total_evidence: int, broken_at: int|null}`

`GET /cases/<id>/timeline` → list of `FoxCaseTimeline` and `FoxEvidenceAccessLog` objects, merged and sorted.

**Error handling:** `ValueError` → 400. `NoResultFound` → 404. Unhandled exceptions → 500 with logged traceback.

---

### MCP Tool Registry — `fox_mcp.py` Blueprint (`/fox`)

Server name: `canary-fox`, version `0.1.0`. Registered via `create_mcp_blueprint`. Health endpoint returns `{service, healthy, tools_count}`.

Each tool opens and closes its own DB session via `_open_service()`. Context is injected as `{merchant_id, user_id}`.

| Tool | Category | Description |
|------|----------|-------------|
| `create_case` | cases | Open a new case. Required: `title`. Optional: `merchant_id`, `description`, `priority`, `assigned_to`, `alert_id`. |
| `get_case` | cases | Fetch case by `case_id`. |
| `list_cases` | cases | List with `status`, `created_after`, `page`, `limit` (max 50). |
| `update_case_status` | cases | Transition status. Validates state machine. Writes timeline + action entries. |
| `add_subject` | cases | Link employee/vendor/external party. Required: `case_id`, `subject_type`, `entity_id`. |
| `get_timeline` | cases | Merged audit trail. Returns `{case_id, entries, count}`. Each entry has `type` (`timeline` or `evidence_access`). |
| `verify_chain` | evidence | Verify hash chain integrity. Returns `{valid, total_evidence, broken_at}`. |
| `link_alert` | cases | Associate an alert with an existing case. Idempotent (returns `already_linked` if already associated). |

---

### Internal Service API — `FoxCaseService`

`FoxCaseService(db_session: Session)` — instantiated per request with a scoped session.

| Method | Signature | Description |
|--------|-----------|-------------|
| `create_case` | `(merchant_id, data: Dict) -> Dict` | Validate, generate case number, INSERT case + timeline. Optional alert link. |
| `create_case_from_context` | `(merchant_id, user_id, *, alert_ids?, txn_ids?, drill_filters?, title?, description?, priority?) -> Dict` | Unified entry point for automated case creation. Derives title/description from context. Links all alerts. Writes AlertHistory records. |
| `get_case_by_id` | `(case_id, merchant_id) -> FoxCase` | `one()` — raises `NoResultFound` if not found or merchant mismatch. |
| `get_cases` | `(merchant_id, status?, created_after?, page, limit) -> (List[FoxCase], dict)` | Paginated query ordered by `opened_at` desc. |
| `update_case_status` | `(case_id, new_status, actor_id, notes?) -> Dict` | Validates state machine. Updates status. Writes timeline + action. |
| `add_evidence` | `(case_id, file_data: bytes, metadata: Dict) -> Dict` | Computes SHA-256. Inserts evidence (trigger computes chain hash). Refreshes record. Writes timeline entry. |
| `log_evidence_access` | `(evidence_id, accessed_by, access_type, ip_address?) -> None` | Inserts `FoxEvidenceAccessLog`. |
| `get_case_evidence` | `(case_id) -> List[FoxEvidence]` | Ordered by `uploaded_at` asc. |
| `get_evidence_by_id` | `(evidence_id, case_id) -> FoxEvidence` | `one()`. |
| `get_case_timeline` | `(case_id, page, per_page) -> List` | Merges `FoxCaseTimeline` and `FoxEvidenceAccessLog`, sorts by timestamp, paginates in Python. |
| `add_subject` | `(case_id, subject_type, entity_id, name?, role?) -> Dict` | Validates subject_type. Resolves employee entity_id. Inserts subject. |
| `add_action` | `(case_id, action_type, description, user_id) -> Dict` | Validates action_type. Inserts action + timeline entry. |
| `verify_evidence_chain` | `(case_id) -> Dict` | Calls PostgreSQL `verify_hash_chain()` function. Returns `{valid, total_evidence, broken_at}`. Falls back to count-only if function not deployed. |

---

## 5. Service Layer

### Enum Validation

All string-typed classification fields are validated against frozensets before any database write. This catches bad inputs at the service boundary with a `ValueError`, not at the database constraint layer, which produces cleaner error messages.

```python
VALID_PRIORITIES    = frozenset({"low", "medium", "high", "critical"})
VALID_CASE_TYPES    = frozenset({"theft", "fraud", "policy_violation",
                                  "cash_variance", "return_abuse",
                                  "transaction_review", "other"})
VALID_STATUSES      = frozenset({"open", "investigating", "pending_review",
                                  "escalated", "closed", "referred_to_le"})
VALID_ACTION_TYPES  = frozenset({"investigate", "interview", "suspend",
                                  "terminate", "refer_to_le", "refer_to_hr",
                                  "coaching", "no_action", "status_change"})
VALID_SUBJECT_TYPES = frozenset({"employee", "customer", "vendor", "unknown"})
VALID_TIMELINE_EVENT_TYPES = frozenset({"created", "status_change", "note_added",
                                         "evidence_added", "assigned", "escalated",
                                         "closed", "action_added"})
```

### State Machine

Status transitions are enforced by a dict in `update_case_status`. Only the listed transitions are allowed:

```
open            → [investigating]
investigating   → [pending_review]
pending_review  → [escalated, closed, referred_to_le]
escalated       → [closed, referred_to_le]
closed          → []  (terminal)
referred_to_le  → []  (terminal)
```

Attempting any other transition raises `ValueError` before any database write.

### Case Number Generation

```python
year = time.localtime().tm_year
existing_count = COUNT(fox_cases WHERE merchant_id=X AND YEAR(created_at)=year)
sequence = existing_count + 1
case_number = f"CASE-{year}-{sequence:05d}"
```

This is optimistic: the UNIQUE index on `case_number` is the actual uniqueness guard. Under concurrent case creation for the same merchant, application code must handle `IntegrityError` and retry.

### Unified Case Creation (`create_case_from_context`)

Used by the Owl agent bridge and automation. Accepts any combination of `alert_ids`, `txn_ids`, and `drill_filters`. Derives a human-readable title and description when not explicitly provided. Links the first alert at case creation time (passed to `create_case` as `alert_id`). Subsequent alerts are linked via additional `FoxCaseAlert` rows. Writes `AlertHistory` records with `status=case_opened` for all linked alerts so the alert log reflects the case linkage.

Returns `{ok, case_id, case_number, evidence_count}` where `evidence_count` is the count of directly linked alerts and transactions (not uploaded files).

### Timeline Merge

`get_case_timeline` fetches `FoxCaseTimeline` rows and `FoxEvidenceAccessLog` rows (joined through `FoxEvidence.case_id`) in separate queries, combines them into a single list, sorts by timestamp using `occurred_at` (timeline) or `accessed_at` (access log), then paginates in Python. This avoids a UNION query across heterogeneous schemas. For cases with large evidence access volumes, this may become a memory concern — see Known Issues.

---

## 6. Configuration

Fox has no dedicated configuration keys. It inherits all Canary application configuration:

| Setting | Description |
|---------|-------------|
| `SQLALCHEMY_DATABASE_URI` | Points to `canary` PostgreSQL database. Fox tables are in the `app` schema. |
| `SECRET_KEY` | Used by JWT middleware for `@jwt_required()` on all Fox routes. |
| `SESSION_TYPE = "redis"` | Valkey session backend — not used directly by Fox, but required for auth. |

The PostgreSQL `compute_entry_hash` and `verify_hash_chain` functions are database-side objects deployed by migration P0-3. There is no application-level configuration for the hash algorithm — it is SHA-256, hardcoded in the trigger.

---

## 7. Security & Compliance

### Authentication and Authorization

All REST routes require a valid JWT via `@jwt_required()`. The JWT middleware populates `g.merchant_id` and `g.user_id` before any Fox handler runs. Tenant isolation is enforced by filtering all queries on `merchant_id = g.merchant_id` — a case from one merchant is never visible to another.

Mutation routes (create, update, add subject, add evidence, add action) additionally require `@roles_required("owner", "operator", "admin")`. Read-only routes (list, get, evidence list, timeline, verify) require only a valid JWT.

### Evidence Tampering Detection

The hash chain makes tampering detectable:

1. **File integrity:** `file_hash = SHA-256(file_bytes)` is computed in Python before INSERT. A change to the stored file content would produce a different hash on re-verification.

2. **Insertion order integrity:** `chain_hash = SHA-256(previous_chain_hash || file_hash)` links each evidence record to its predecessor. Deleting or reordering records breaks the chain.

3. **Verification:** `FoxCaseService.verify_evidence_chain()` calls the PostgreSQL `verify_hash_chain("fox_evidence", record_id, merchant_id)` function, which walks the chain from the first to the last evidence record and reports the position of the first broken link, if any.

Application code cannot write a valid `chain_hash` — it always passes the placeholder `"TRIGGER_WILL_OVERWRITE"`. The trigger is the only code path that computes chain hashes, eliminating the possibility of a client forging a valid chain.

### Chain of Custody Audit

Every access to an evidence record is logged in `FoxEvidenceAccessLog`:
- Upload: logged automatically at `POST /cases/<id>/evidence` with `access_type="upload"`.
- View: logged automatically at `GET /cases/<id>/evidence/<eid>` with `access_type="view"`.
- Download/print/export: must be logged by the caller via `FoxCaseService.log_evidence_access()`.

Access log rows are INSERT-only. The IP address of the accessor is recorded.

### Immutability Enforcement

Two tables are INSERT-only at the database layer: `fox_evidence` and `fox_evidence_access_log`. PostgreSQL triggers reject UPDATE and DELETE on these tables. There are no `update()` or `delete()` methods on these models.

`FoxCaseTimeline` is INSERT-only by application convention. No mutation methods exist; there are no DB triggers preventing UPDATE/DELETE on the timeline (a future hardening item).

### Soft Delete

`FoxCase`, `FoxCaseAction`, and `FoxSubject` use `SoftDeleteMixin`. Deleted records remain in the database; the `deleted_at` timestamp is set. This preserves the investigation record even after cases are administratively removed from active views.

---

## 8. Error Handling

### Service Layer

`FoxCaseService` raises `ValueError` for all application-level validation failures:
- Invalid `case_type`, `priority`, `status`, `action_type`, or `subject_type`
- Invalid status transition
- Referenced `Employee` entity not found
- Malformed or missing required keys in timeline metadata JSON

SQLAlchemy's `NoResultFound` propagates upward from `one()` calls (e.g., `get_case_by_id`) when a case does not exist or belongs to a different merchant.

### Blueprint Layer

`fox_wired.py` registers three error handlers on the blueprint:

| Exception | HTTP Status | Response |
|-----------|-------------|----------|
| `ValueError` | 400 | `{error: <message>}` |
| `NoResultFound` | 404 | `{error: "Not found"}` |
| `HTTPException` (Werkzeug) | pass-through code | `{error: <description>}` |
| Any other `Exception` | 500 | `{error: "Internal server error"}` + logged |

### MCP Layer

MCP tool handlers catch `ValueError` and return `{error: <message>}` to the agent. Unhandled exceptions propagate to the MCP framework. Each tool opens its own DB session in a `try/finally` block, guaranteeing session close even on error.

### Hash Chain Fallback

`verify_evidence_chain()` wraps the `verify_hash_chain()` DB function call in a try/except. If the function has not been deployed (migration P0-3 not yet run), it returns:
```json
{
  "valid": null,
  "total_evidence": <count>,
  "broken_at": null,
  "message": "DB verify_hash_chain() not available — run P0-3 migration"
}
```
This prevents the route from returning 500 when the DB function is missing.

---

## 9. Testing

Test files: `Canary/tests/` — marked with `pytest.mark.fox` and `pytest.mark.critical`.

### Unit Tests

**`tests/unit/test_fox_validation.py`** — GRO-246. Tests all enum frozensets and `validate_timeline_metadata()`:
- All values in `VALID_CASE_TYPES` pass without error
- Invalid `case_type` raises `ValueError` with message matching `"Invalid case_type"`
- Invalid `priority` raises `ValueError`
- Invalid `status` raises `ValueError`
- `status_change` event without `old_status`/`new_status` in metadata raises `ValueError`
- `evidence_added` event without `evidence_id` in metadata raises `ValueError`
- JSON string metadata is parsed before validation
- Invalid JSON string raises `ValueError`

**`tests/unit/test_fox_unified_create.py`** — GRO-245. Tests `create_case_from_context()` with mocked DB session:
- `alert_ids` provided → title derived as "Case from N alert(s)"
- `txn_ids` provided → `case_type=transaction_review`
- Empty context → title = "New investigation"
- Multiple alert IDs → first linked at creation, rest via additional `FoxCaseAlert` rows
- `AlertHistory` rows written for all linked alerts

**`tests/unit/test_fox_tools.py`** — Tests MCP tool handlers with mocked service:
- `create_case` returns error if `title` missing
- `update_case_status` returns `{error}` dict on `ValueError` (not exception)
- `link_alert` returns `{already_linked: True}` when alert already associated
- `verify_chain` delegates to service without modification

### Integration Tests

**`tests/integration/test_fox_lifecycle.py`** — Full lifecycle against real PostgreSQL. Marked `postgres`, `fox`, `critical`:
- Case creation persists all fields correctly
- `case_number` uniqueness constraint raises `IntegrityError` on duplicate
- Status transition writes timeline and action records
- Invalid transition raises `ValueError` before any write
- Subject added with `subject_type=employee`, entity resolved correctly
- `to_dict()` output includes `subject_count` and `evidence_count` when set

**`tests/integration/test_fox_evidence_chain.py`** — Evidence chain against real PostgreSQL. Marked `postgres`, `fox`, `critical`:
- Single evidence upload persists `file_hash`, `evidence_type`, `file_name`, `file_size_bytes`
- `chain_hash` is set by trigger (not "TRIGGER_WILL_OVERWRITE") after flush + refresh
- First evidence record has `previous_chain_hash = NULL`
- Second evidence record has `previous_chain_hash` equal to first record's `chain_hash`
- Multiple evidence records produce a valid chain verified by `verify_evidence_chain()`
- Access log row inserted on upload
- `get_case_timeline()` returns merged timeline + access log in chronological order

### Running Tests

```bash
# Unit (no database required)
python3 -m pytest tests/unit/test_fox_validation.py tests/unit/test_fox_tools.py \
    tests/unit/test_fox_unified_create.py -v

# Integration (requires growdirect_postgres running)
python3 -m pytest tests/integration/test_fox_lifecycle.py \
    tests/integration/test_fox_evidence_chain.py -v -m postgres
```

---

## 10. Dependencies

### Upstream

**Chirp detection rules → Fox (auto-case creation)**

When Chirp fires an alert, the Owl agent bridge in `canary/blueprints/owl_api.py` calls `FoxCaseService.create_case_from_context()`. The following detection rules are known to trigger this path:

| Rule | Description |
|------|-------------|
| C-009 | Transaction hold / delay action |
| C-104 | Sale anomaly pattern |
| C-204 | Policy violation flag |
| C-301 | Post-timecard transaction (employee off-clock) |
| C-502 | Self-refund pattern |
| C-602 | Gift card load/drain velocity |

Rule-to-case linkage is tracked via `FoxCaseAlert` (junction between `fox_cases` and Chirp alert IDs). When a case is auto-created, `AlertHistory` records are written back to the `alerts` table with `status=case_opened`.

**Owl search → Fox (drill-to-case)**

`canary/services/owl/search/builder.py` includes the `(fox_cases, alerts)` join path `(id, case_id)` via `fox_case_alerts`. This allows Owl search results to surface existing case context alongside alert and transaction records.

### Downstream

Fox has no downstream consumers currently. Case records are terminal — once referred to law enforcement or closed, no other Canary service reads Fox data in a processing pipeline. Future integrations (HR notification, LE case export) are deferred.

### Shared Infrastructure

| Component | Role |
|-----------|------|
| `growdirect_postgres` (canary DB, app schema) | Primary data store for all Fox tables |
| `canary.db.session_factory.get_session()` | Session factory used by service and MCP tools |
| `canary.middleware.jwt_auth` | `jwt_required()` and `roles_required()` decorators |
| `canary.mcp.MCPRegistry` / `MCPTool` | MCP tool registration framework |
| `canary.mcp.blueprint.create_mcp_blueprint` | Mounts the registry as Flask blueprint endpoints |
| `canary.models.base` — `AppBase`, `TenantMixin`, `AuditMixin`, `SoftDeleteMixin` | Base classes for all Fox models |
| `canary.models.app.detection.AlertHistory` | Written by `create_case_from_context()` to record case linkage |
| `canary.models.app.employees.Employee` | Queried by `resolve_entity()` for employee subject type validation |

---

## 11. Known Issues & Reconciliation

**Case number generation race condition.** Case numbers are derived from a `COUNT()` query, not from a sequence or lock. Under concurrent case creation for the same merchant in the same calendar second, two workers may compute the same sequence number. The UNIQUE index on `fox_cases.case_number` will reject the second INSERT with `IntegrityError`. The blueprint does not currently retry — the caller receives a 500. This is unlikely in practice (most merchants create cases infrequently) but is not resilient. A PostgreSQL sequence scoped per merchant per year, or an advisory lock, would eliminate the race.

**Timeline pagination is in-process, not in-database.** `get_case_timeline()` fetches all timeline and access log rows for the case, merges them in Python, then slices the page. For cases with very large access log volumes (e.g., evidence accessed thousands of times), this loads all rows into memory. A UNION query ordered by timestamp with LIMIT/OFFSET would be more efficient but requires a common result shape.

**`file_path` is not used.** `FoxEvidence.file_path` is always persisted as an empty string (`""`). Blob storage integration (S3 or equivalent) is deferred. Evidence file bytes are accepted at the API layer but not stored — only the hash and metadata are persisted. Until blob storage is wired, the chain proves hash integrity of received content, but the file itself cannot be retrieved.

**No virus scanning on upload.** Evidence files are accepted and hashed without scanning. ClamAV or cloud-based scanning is deferred.

**`FoxCaseTimeline` immutability is by convention only.** Unlike `fox_evidence` and `fox_evidence_access_log`, the timeline table does not have a PostgreSQL trigger preventing UPDATE/DELETE. Immutability relies on the application never calling update or delete on these rows. A DB-level trigger matching the evidence tables would harden this.

**`verify_hash_chain()` DB function may not be deployed.** Migration P0-3 deploys the `compute_entry_hash` BEFORE INSERT trigger and the `verify_hash_chain()` function. If a database is initialized without running this migration (e.g., a fresh test environment), evidence uploads will fail (the placeholder `chain_hash` value is stored permanently) and `verify_evidence_chain()` falls back to returning `valid: null`. All environments must run P0-3.

**Employee entity resolution only.** `resolve_entity()` validates `subject_type=employee` against the `Employee` table. Customer and vendor subject types skip resolution — `entity_id` is stored as-is without verification. Cross-DB lookup tables for customers and vendors do not exist yet.

**HR/LE referral notifications are deferred.** `FoxCaseAction` with `action_type=refer_to_le` or `refer_to_hr` creates a record but does not trigger any notification workflow. Integration with a notification service is a future item.

**Priority auto-escalation is deferred.** The `FoxCase` model has a comment noting planned auto-escalation logic (escalate to `critical` if unresolved beyond N days). This requires a background scheduler and is not implemented.
