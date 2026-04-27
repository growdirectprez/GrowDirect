# Fox — Case Management & Evidence Locker

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

## Purpose

Fox is Canary's case management and evidence locker domain -- "The Vault" in the mobile UX. It bridges automated anomaly detection (Chirp alerts) and human investigation workflows. When a merchant decides an alert warrants investigation, Fox creates a case, links originating alerts, tracks subjects of interest, stores evidence with cryptographic chain-of-custody integrity, and maintains an append-only audit timeline. Fox handles sensitive investigation data including employee identifiers, investigation narratives, and uploaded evidentiary files.

### Hawk Positioning (Phase 1+)

Fox is an **evidence-based record (EBR)** class inside the Hawk ops-contract system, not a standalone surface. Hawk introduces a card-based investigation model with a wizard FSM, structured card pipeline, and multi-entity tracking that supersedes Fox's flat case lifecycle; Fox's INSERT-only evidence chain, hash-chain integrity, and access-logging disciplines carry forward unchanged as the evidentiary backbone of every Hawk card. See `docs/sdds/canary/hawk.md` for the full ops-contract specification.

## Dependencies

| Dependency | Type | Required | Purpose |
|---|---|---|---|
| PostgreSQL 17 (`canary` DB, `app` schema) | Database | Yes | All Fox tables, INSERT-ONLY triggers, `verify_hash_chain()` function |
| Valkey 8 (DB 0) | Cache | Yes | Session backend for JWT auth |
| Canary Flask (port 5001) | Host process | Yes | Fox blueprints run inside the Canary Flask container |
| `canary.middleware.jwt_auth` | Internal | Yes | JWT authentication and RBAC on all routes |
| `canary.db.session_factory` | Internal | Yes | Database session management |
| `canary.mcp` base kit | Internal | Yes | MCP tool registration and blueprint creation |
| Alert domain (`AlertHistory`) | Internal | Soft | Writes alert history when linking alerts to cases |
| Employee model | Internal | Soft | Entity resolution for employee subjects |

## Data Flow & PII Map

### What enters

| Source | Data | Format |
|---|---|---|
| UI/BFF via REST | Case title, description, priority, assigned_to, alert_id | JSON POST |
| UI/BFF via REST | Evidence files (screenshots, PDFs, video) | Multipart file upload |
| UI/BFF via REST | Subject details (type, entity_id, name, role) | JSON POST |
| Owl action dispatcher | Case creation triggers from automated detection | Internal service call |
| MCP tools (agent) | All case CRUD operations via 8 registered tools | MCP tool invocation |

### What is stored

| Table | PII Fields | Classification | Encryption Status |
|---|---|---|---|
| `fox_cases` | `title`, `description`, `resolution` | internal | **Plaintext** -- may contain employee names, investigation details |
| `fox_cases` | `assigned_to`, `opened_by` | internal | **Plaintext** -- user IDs (email-like strings) |
| `fox_subjects` | `name` | **sensitive** | **Plaintext** -- employee/suspect names stored unencrypted |
| `fox_subjects` | `entity_id` | internal | **Plaintext** -- cross-reference to employee records |
| `fox_subjects` | `role_in_case` | internal | **Plaintext** -- free text describing suspect/witness role |
| `fox_evidence` | `file_name`, `description` | internal | **Plaintext** -- may reveal investigation context |
| `fox_evidence` | `uploaded_by` | internal | **Plaintext** -- investigator identity |
| `fox_evidence` | `file_path` | internal | **Plaintext** -- currently empty (S3 deferred), will hold storage paths |
| `fox_case_timeline` | `actor_id`, `description`, `meta_data` | internal | **Plaintext** -- actor identities and action narratives |
| `fox_case_actions` | `performed_by`, `description`, `outcome` | internal | **Plaintext** -- HR actions (suspend, terminate) with employee context |
| `fox_evidence_access_log` | `accessed_by`, `ip_address` | **sensitive** | **Plaintext** -- who accessed evidence and from where |

### What exits

| Destination | Data | Notes |
|---|---|---|
| REST API responses | Case details, evidence metadata, timeline entries | JSON, no file content in responses |
| MCP tool responses | Same as REST | Agent consumption |
| Alert domain | `AlertHistory` records (status=case_opened) | Cross-domain write when linking alerts |

### PII Classification Summary

- **public:** None -- all Fox data is behind authentication
- **internal:** Case titles, descriptions, user IDs, file names, timeline descriptions
- **sensitive:** Subject names (`fox_subjects.name`), IP addresses (`fox_evidence_access_log.ip_address`), investigator identities, HR action descriptions (suspend/terminate outcomes)
- **restricted:** None currently, but evidence file content (when S3 is implemented) should be restricted

## API Contract

### REST Endpoints (`fox_wired` -- `/api/fox/*`)

All require JWT authentication via `@jwt_required()`. Write operations require `owner`, `operator`, or `admin` roles via `@roles_required()`.

| Method | Endpoint | Role Gate | Purpose |
|---|---|---|---|
| GET | `/cases` | any authenticated | List cases (paginated, filterable by status/created_after) |
| POST | `/cases` | owner/operator/admin | Create case (title required, optional alert_id link) |
| GET | `/cases/<case_id>` | any authenticated | Get single case details |
| PUT | `/cases/<case_id>` | owner/operator/admin | Update case status (validated transitions) |
| POST | `/cases/<case_id>/subjects` | owner/operator/admin | Add subject (type + entity_id required) |
| POST | `/cases/<case_id>/evidence` | owner/operator/admin | Upload evidence (multipart file) |
| GET | `/cases/<case_id>/evidence` | any authenticated | List evidence for case |
| GET | `/cases/<case_id>/evidence/<eid>` | any authenticated | Get single evidence item (logs access) |
| GET | `/cases/<case_id>/evidence/verify` | any authenticated | Verify evidence hash chain integrity |
| GET | `/cases/<case_id>/timeline` | any authenticated | Get merged timeline (events + access logs) |
| POST | `/cases/<case_id>/actions` | owner/operator/admin | Add investigation action |

**Error responses:** 400 (validation, invalid transition), 404 (not found), 500 (unhandled, logged). The generic exception handler logs the error and returns `"Internal server error"` -- does not leak stack traces.

### MCP Tools (`canary-fox` -- `/fox/*`)

8 tools registered via `MCPRegistry`. Each tool opens its own DB session via `get_session()` and closes in `finally`.

| Tool | Category | PII Access | Description |
|---|---|---|---|
| `create_case` | cases | Writes user_id as actor | Open a case with title, description, priority, optional alert link |
| `get_case` | cases | Reads case details | Get full case details by ID |
| `list_cases` | cases | Reads case list | List cases with optional status/date filters (max 50/page) |
| `update_case_status` | cases | Writes actor_id | Transition status through lifecycle state machine |
| `add_subject` | cases | Writes subject name, entity_id | Link employee/vendor/external party to a case |
| `get_timeline` | cases | Reads actor IDs, access logs | Get append-only audit trail |
| `verify_chain` | evidence | No PII | Verify evidence hash chain via PostgreSQL function |
| `link_alert` | cases | Writes user_id | Link an alert to an existing case (idempotent) |

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

**fox_case_alerts:** Junction table linking alerts to cases. PK: `id` (UUID). Fields: `case_id` (FK fox_cases.id), `alert_id` (String, cross-DB reference), `linked_at`, `linked_by`, `notes`. Mixin: AuditMixin.

**fox_subjects:** Persons/entities of interest linked to cases. PK: `id` (UUID). Fields: `merchant_id` (FK), `case_id` (FK), `subject_type` (employee/customer/vendor/unknown), `entity_id` (cross-DB FK), `name`, `role_in_case`, `is_primary_suspect`. Mixins: TenantMixin, AuditMixin, SoftDeleteMixin.

**fox_case_actions:** Investigation actions. PK: `id` (UUID). Fields: `case_id` (FK), `merchant_id` (FK), `action_type` (investigate/interview/suspend/terminate/refer_to_le/refer_to_hr/coaching/no_action/status_change), `description`, `performed_by`, `performed_at`, `outcome`. Mixins: TenantMixin, AuditMixin, SoftDeleteMixin.

### Tier 2 -- Immutable Audit Trail (APPEND-ONLY)

**fox_case_timeline:** Append-only event log. PK: `id` (UUID). Fields: `case_id` (FK), `merchant_id` (FK), `event_type` (created/status_change/note_added/evidence_added/assigned/escalated/closed/alert_linked/action_added), `actor_id`, `description`, `meta_data` (JSON), `occurred_at`. No AuditMixin, no SoftDeleteMixin -- the timeline IS the audit trail. Protected by INSERT-ONLY DB trigger.

### Tier 3 -- Evidentiary Chain (INSERT-ONLY, hash-chained)

**fox_evidence:** INSERT-ONLY evidence records with cryptographic hash chain. PK: `id` (UUID). Fields: `merchant_id`, `case_id`, `evidence_type`, `file_name`, `file_path` (storage path -- currently empty, S3 deferred), `file_hash` (SHA-256 of file content), `file_size_bytes`, `content_type`, `description`, `uploaded_by`, `uploaded_at`, `previous_chain_hash` (NULL for genesis), `chain_hash` (SHA-256, computed by DB trigger). DB triggers: `compute_entry_hash()` BEFORE INSERT overwrites chain_hash; immutability trigger blocks UPDATE/DELETE.

**fox_evidence_access_log:** INSERT-ONLY access audit. PK: `id` (UUID). Fields: `evidence_id` (FK), `accessed_by`, `access_type` (view/download/print/export/upload), `accessed_at`, `ip_address` (IPv4/IPv6). DB triggers: immutability trigger blocks UPDATE/DELETE.

### Hash Chain Architecture

Two distinct algorithms coexist in the codebase:

| Module | Algorithm | Storage | Used By |
|---|---|---|---|
| `hash_chain.py` | `sorted_json + "\|" + prev_hash` | 64-char hex string | fox_evidence (via DB trigger), audit_log |
| `evidence_chain.py` | `prev_bytes \|\| event_bytes` (raw concat) | 32 bytes (BYTEA) | evidence_records (WH-03 spec, separate data path) |

The DB trigger (`compute_entry_hash()`) is the single source of truth for fox_evidence chain hashes. The app sends `chain_hash="TRIGGER_WILL_OVERWRITE"` as a placeholder; the trigger overwrites it. After `session.flush()`, the service calls `session.refresh()` to read back the trigger-computed values. Even a compromised application layer cannot forge a valid chain.

**Chain verification** uses PostgreSQL's `verify_hash_chain(table, record_id, merchant_id)` function for server-side validation. If the function is not deployed, verification returns `valid: null` with a diagnostic message rather than failing.

**What breaks the chain:** Direct SQL `UPDATE` or `DELETE` on `fox_evidence` rows (blocked by trigger). Database restore from backup without corresponding chain state. Manual insertion bypassing the trigger. Gap in `previous_chain_hash` linkage.

## Workflows

### Case Lifecycle State Machine

```
open --> investigating --> pending_review --> escalated --> closed
                                         \-> closed      \-> referred_to_le
                                         \-> referred_to_le

closed          (terminal -- no transitions out)
referred_to_le  (terminal -- no transitions out)
```

Enforced by `FoxCaseService.update_case_status()`. Invalid transitions raise `ValueError` (HTTP 400). Every transition writes both a `fox_case_timeline` entry and a `fox_case_actions` record.

### Alert-to-Case Flow

1. Chirp alert detected
2. Merchant taps "Open case" or Owl dispatcher fires `case_create`
3. `FoxCaseService.create_case()` generates case_number, inserts case + timeline, optionally links alert
4. Alert domain writes `AlertHistory` (status=case_opened)

### Evidence Upload and Chain Hash

1. `POST /api/fox/cases/<id>/evidence` with multipart file
2. App computes `SHA-256(file_data)` for `file_hash`
3. Inserts `FoxEvidence` with `chain_hash="TRIGGER_WILL_OVERWRITE"`
4. PostgreSQL BEFORE INSERT trigger fires, computes real chain_hash linking to previous evidence
5. `session.flush()` + `session.refresh()` reads trigger values back into Python
6. Timeline entry created (event_type=evidence_added)
7. Access log entry created (access_type=upload, IP captured)

### Case Number Generation

Format: `CASE-{year}-{sequence:05d}` per merchant per year. Sequence derived from `SELECT count(*)` of existing cases for that merchant/year. Uniqueness enforced by database unique index on `case_number`. Not globally unique -- unique per merchant.

### Unified Case Creation from Context (GRO-245)

Entry point: `FoxCaseService.create_case_from_context()`. Single method for case creation from alerts, transactions, or drill path filters. Auto-generates title and description from context. Links multiple alerts, writes `AlertHistory` for each.

### Enum Validation (GRO-246)

All enums enforced as module-level `frozenset` constants in `case_service.py`: `VALID_PRIORITIES`, `VALID_CASE_TYPES`, `VALID_STATUSES`, `VALID_ACTION_TYPES`, `VALID_SUBJECT_TYPES`, `VALID_TIMELINE_EVENT_TYPES`. Validation raises `ValueError` with the invalid value and sorted valid options.

## Operations

### Startup Sequence

Fox has no independent startup. It loads as two Flask blueprints (`fox_bp` at `/api/fox`, `fox_mcp_bp` at `/fox`) registered in `wsgi.py` during Canary Flask boot. The MCP registry (`canary-fox`, 8 tools) is initialized at module import time.

### Health Checks

| Endpoint | What it checks | Expected response |
|---|---|---|
| `GET /fox/health` | MCP server alive, tool count | `{"service": "canary-fox", "healthy": true, "tools": 8}` |
| `GET /health` (Canary-wide) | Flask process alive | Checked by Docker healthcheck every 30s |

Fox has no independent database health probe. If PostgreSQL is down, all Fox operations fail with 500 errors.

### Failure Modes

| Failure | Impact | Behavior |
|---|---|---|
| PostgreSQL down | All Fox operations fail | 500 errors on all endpoints |
| `verify_hash_chain()` DB function missing | Chain verification degraded | Returns `valid: null` with message, does not crash |
| INSERT-ONLY triggers missing | Evidence integrity compromised | No runtime error -- silent data integrity loss |
| Valkey down | Auth fails, sessions lost | 401 on all requests (JWT session backend) |
| Evidence file too large | Potential OOM | **No file size limit enforced** -- see P1-FOX-01 |
| Concurrent case creation | Duplicate case numbers possible | Unique index catches it, but no retry logic |

### Configuration

| Env Var | Purpose | Default |
|---|---|---|
| `CANARY_DEV_JWT_SECRET` | Dev-mode JWT validation token | None (required in dev) |
| `CANARY_MCP_API_KEY` | API key for agent-to-agent calls | None |
| `CANARY_ENV` | Environment (development/production) | `development` |
| `SQUARE_MERCHANT_ID` | Default merchant for API key auth | `demo-merchant` |

No Fox-specific configuration. All config inherited from Canary Flask.

### Monitoring

| Metric | Alert Threshold | Notes |
|---|---|---|
| Hash chain verification failures | Any `valid: false` | Indicates evidence tampering or DB corruption |
| Evidence access from unusual IPs | Anomaly detection needed | **Not implemented** -- see P2-FOX-04 |
| Cases stuck in `open` > 30 days | Operational alert | **Not implemented** -- needs background scheduler |
| 500 error rate on `/api/fox/*` | > 1% of requests | Standard Flask error logging |

## Deployment

### Docker Service

Fox runs inside the Canary Flask container (Layer 7 in docker-compose). No separate container.

```yaml
# In Canary docker-compose
flask:
  image: canary-flask
  ports: ["5001:5001"]
  command: gunicorn wsgi:app --bind 0.0.0.0:5001
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
```

### AWS Target

| Component | AWS Service | Notes |
|---|---|---|
| Flask container | ECS/Fargate | Fox runs in same task as all Canary services |
| Database | RDS PostgreSQL 17 | `canary` database, `app` schema |
| Evidence files | S3 | **Not implemented** -- `file_path` is empty string |
| Secrets | AWS Secrets Manager | JWT secrets, API keys |
| Session cache | ElastiCache (Valkey) | DB 0 |

### CI/CD Requirements

- INSERT-ONLY triggers must be deployed before any evidence operations
- `verify_hash_chain()` function must be deployed for chain verification
- Migration order: tables first, then triggers, then DB functions

## Code Review Findings

### P0 -- Blocks Production

**P0-FOX-01: Subject names stored plaintext.**
`fox_subjects.name` stores employee/suspect names without encryption. In loss prevention investigations, these names are legally sensitive. A database breach exposes every person ever investigated.
- **Impact:** Legal liability, employee privacy violation
- **Fix:** Field-level AES-256-GCM encryption using Canary's existing `crypto.py` pattern. Encrypt `name` and `role_in_case` at write, decrypt at read.
- **Linear:** Needs GRO issue

**P0-FOX-02: Investigation narratives stored plaintext.**
`fox_cases.description`, `fox_cases.resolution`, `fox_case_actions.description`, and `fox_case_actions.outcome` contain free-text investigation details that may reference employees by name, describe suspected criminal activity, or document HR actions (suspend/terminate). All stored plaintext.
- **Impact:** Database breach exposes investigation details and HR decisions
- **Fix:** Encrypt `description`, `resolution`, `outcome` fields at rest. Evaluate which fields need field-level encryption vs relying on RDS encryption at rest.
- **Linear:** Needs GRO issue

**P0-FOX-03: No evidence file storage.**
`file_path` is hardcoded to empty string `""`. Evidence file content is read into memory during upload (`file.read()`) but never persisted to disk or object storage. The file hash is stored but the actual evidence is lost after the request completes.
- **Impact:** Evidence locker is non-functional for file retrieval. Chain of custody exists for metadata only.
- **Fix:** Implement S3 upload in `add_evidence()`. Store file to S3 with server-side encryption (SSE-S3 or SSE-KMS). Populate `file_path` with S3 key. Add download endpoint.
- **Linear:** Needs GRO issue

**P0-FOX-04: Secrets in .env files.**
JWT secrets (`CANARY_DEV_JWT_SECRET`) and API keys (`CANARY_MCP_API_KEY`) are loaded from environment variables set in `.env` files. Production requires AWS Secrets Manager.
- **Impact:** Credential exposure in version control or container images
- **Fix:** AWS Secrets Manager retrieval at startup for production. `.env` acceptable for dev only.
- **Linear:** Cross-cutting (affects all Canary services)

### P1 -- Before GA

**P1-FOX-01: No file size limit on evidence upload.**
The `add_evidence` endpoint reads the entire uploaded file into memory with `file.read()` and no size validation. An attacker or misconfigured client could upload a multi-GB file, causing OOM in the Flask worker.
- **Impact:** Denial of service via memory exhaustion
- **Fix:** Add `MAX_CONTENT_LENGTH` to Flask config (e.g., 50MB). Validate `file_size_bytes` before reading. Stream large files to S3 without buffering in memory.
- **Linear:** Needs GRO issue

**P1-FOX-02: No tenant isolation on evidence access.**
The `get_evidence` endpoint (`GET /cases/<case_id>/evidence`) does not filter by `merchant_id`. It queries `FoxEvidence.filter_by(case_id=case_id)` only. If a user guesses a `case_id` UUID from another merchant, they could access that merchant's evidence list. The `get_case_by_id` method does filter by merchant_id, but `get_case_evidence` does not.
- **Impact:** Cross-tenant data leakage of evidence metadata
- **Fix:** Add `merchant_id` filter to `get_case_evidence()` and `get_evidence_by_id()`. Or validate case ownership before evidence queries.
- **Linear:** Needs GRO issue

**P1-FOX-03: Timeline serialization returns raw ORM objects.**
`GET /api/fox/cases/<case_id>/timeline` calls `service.get_case_timeline()` which returns a mixed list of `FoxCaseTimeline` and `FoxEvidenceAccessLog` ORM objects, then passes them directly to `jsonify()`. Flask's default JSON encoder cannot serialize SQLAlchemy model instances.
- **Impact:** 500 error on timeline endpoint in production (works only if custom serializer exists)
- **Fix:** Add `to_dict()` methods or explicit serialization in the blueprint before `jsonify()`. The MCP tool handler (`_handle_get_timeline`) already does manual serialization -- the REST endpoint should match.
- **Linear:** Needs GRO issue

**P1-FOX-04: IP addresses stored plaintext in access log.**
`fox_evidence_access_log.ip_address` stores raw IPv4/IPv6 addresses. For regulatory compliance (GDPR treats IP addresses as PII), these should be hashed or masked.
- **Impact:** GDPR compliance risk
- **Fix:** Hash IP addresses before storage (one-way). Or mask to /24 subnet for IPv4, /48 for IPv6.
- **Linear:** Cross-cutting (also affects audit_log)

**P1-FOX-05: No data retention policy.**
No mechanism to purge old cases, evidence, or access logs. Investigation data accumulates indefinitely. Many jurisdictions have data retention limits for employee investigation records.
- **Impact:** Regulatory non-compliance, storage cost growth
- **Fix:** Implement retention policy: closed cases > 7 years archived, access logs > 24 months purged. Requires careful handling of hash chain -- archived evidence breaks the chain unless the chain terminal hash is preserved.
- **Linear:** Cross-cutting

**P1-FOX-06: No rate limiting on Fox endpoints.**
No Flask-Limiter or equivalent on any Fox REST endpoint. An attacker could enumerate case IDs or flood evidence uploads.
- **Impact:** Brute-force case enumeration, resource exhaustion
- **Fix:** Apply Flask-Limiter: 60/min on reads, 10/min on writes, 5/min on evidence upload.
- **Linear:** Cross-cutting

**P1-FOX-07: INSERT-ONLY triggers not in Alembic migration.**
The triggers (`prevent_modify_chain_of_custody`, `compute_entry_hash`) exist as a devops prompt (`devops/prompts/21_insert_only_triggers_fox.md`) but are not in the consolidated Alembic migration (`56fb3923c13a`). They must be manually deployed. If forgotten, evidence integrity is silently unprotected.
- **Impact:** Silent loss of evidence tamper protection if triggers are not manually applied
- **Fix:** Add triggers to a versioned Alembic migration. Verify triggers exist on startup with a SQL check.
- **Linear:** Needs GRO issue

### P2 -- Post-Launch

**P2-FOX-01: Case number race condition.**
`create_case()` generates the case number from `SELECT count(*)` of existing cases. Under concurrent requests for the same merchant/year, two sessions could get the same count and generate duplicate case numbers. The unique index catches this as an IntegrityError, but there is no retry logic -- the second request gets a 500 error.
- **Impact:** Rare 500 errors under concurrent case creation
- **Fix:** Use a PostgreSQL sequence per merchant/year, or add retry-with-increment logic on IntegrityError.
- **Linear:** Needs GRO issue

**P2-FOX-02: No virus scanning on evidence upload.**
Uploaded evidence files are not scanned for malware. Comment in code: "DEFERRED: Virus scanning on upload -- needs ClamAV or cloud scanning service."
- **Impact:** Malicious files could be stored and re-downloaded by other users
- **Fix:** Integrate ClamAV or AWS GuardDuty S3 malware scanning after S3 upload.
- **Linear:** Needs GRO issue

**P2-FOX-03: No key rotation documentation.**
Evidence chain relies on SHA-256 which does not use keys, so key rotation does not apply to the hash chain itself. However, JWT secrets and MCP API keys have no documented rotation procedure.
- **Impact:** Long-lived secrets increase blast radius of compromise
- **Fix:** Document rotation procedure for JWT and API key secrets. Implement scheduled rotation.
- **Linear:** Cross-cutting

**P2-FOX-04: Evidence access anomaly detection not implemented.**
Comment in code: "DEFERRED: Access anomaly detection (unusual IP, rapid access patterns) -- needs analytics pipeline." No alerting on suspicious evidence access patterns.
- **Impact:** Insider threats accessing evidence could go undetected
- **Fix:** Implement access pattern analysis in the analytics pipeline. Alert on: rapid sequential access, access from new IPs, access outside business hours.
- **Linear:** Needs GRO issue

**P2-FOX-05: MCP tools lack merchant_id validation on some operations.**
`_handle_update_case_status` and `_handle_get_timeline` do not validate `merchant_id` -- they operate on `case_id` alone. If an agent provides a case_id from another merchant, the operation succeeds without tenant isolation.
- **Impact:** Cross-tenant operations possible via MCP tools
- **Fix:** Add merchant_id validation to all MCP tool handlers that modify or read case data.
- **Linear:** Needs GRO issue

## Production Readiness Checklist

- [ ] PII encrypted at rest -- **FAIL.** Subject names, investigation narratives, IP addresses all plaintext. (P0-FOX-01, P0-FOX-02, P1-FOX-04)
- [ ] Secrets in AWS Secrets Manager (not .env) -- **FAIL.** JWT and API key secrets in env vars. (P0-FOX-04)
- [x] Health check endpoint responds -- `GET /fox/health` returns `{"healthy": true}`
- [x] Audit logging for sensitive operations -- Evidence access logged (INSERT-ONLY). Timeline tracks all case state changes. Access log captures who/when/where.
- [ ] Data retention policy implemented -- **FAIL.** No purge mechanism. (P1-FOX-05)
- [ ] Rate limiting on public endpoints -- **FAIL.** No rate limiting. (P1-FOX-06)
- [x] Error responses don't leak internals -- Generic exception handler returns `"Internal server error"`, logs the real error server-side.
- [ ] Evidence file storage functional -- **FAIL.** Files not persisted. (P0-FOX-03)
- [x] Hash chain integrity enforced -- DB trigger computes chain hashes. Immutability triggers block UPDATE/DELETE.
- [ ] INSERT-ONLY triggers in versioned migration -- **FAIL.** Triggers require manual deployment. (P1-FOX-07)
- [ ] Tenant isolation on all queries -- **FAIL.** Evidence list and MCP tools missing merchant_id filter. (P1-FOX-02, P2-FOX-05)
- [x] Case lifecycle state machine validated -- Strict transition enforcement with enum validation (GRO-246).
- [x] Timeline metadata schema validation -- Per-event-type required keys validated before insert (GRO-246).

## Source Files

| File | Purpose |
|---|---|
| `canary/services/fox/case_service.py` | `FoxCaseService` -- all Fox business logic |
| `canary/services/fox/tools.py` | 8 MCP tool definitions for `canary-fox` server |
| `canary/services/hash_chain.py` | General-purpose chain verification |
| `canary/services/evidence_chain.py` | WH-03 BYTEA chain hash (separate data path) |
| `canary/blueprints/fox_wired.py` | REST API blueprint (`/api/fox`) |
| `canary/blueprints/fox_mcp.py` | MCP blueprint (`/fox`) |
| `canary/models/fox/cases.py` | FoxCase, FoxCaseAlert, FoxCaseTimeline, FoxCaseAction models |
| `canary/models/fox/evidence.py` | FoxEvidence, FoxEvidenceAccessLog models |
| `canary/models/fox/subjects.py` | FoxSubject model |
| `canary/middleware/jwt_auth.py` | JWT auth + RBAC decorators |
| `tests/unit/test_fox_validation.py` | Enum validation unit tests (GRO-246) |
| `tests/unit/test_fox_unified_create.py` | Unified case creation tests (GRO-245) |
| `tests/integration/test_fox_evidence_chain.py` | Evidence chain integration tests |

---
*Canary LP | GrowDirect Inc. | Confidential*
