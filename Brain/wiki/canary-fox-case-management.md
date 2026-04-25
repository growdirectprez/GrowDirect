---
date: 2026-04-23
type: wiki
tags: [canary, fox, cases, evidence, chain-of-custody, investigation, audit]
sources:
  - Canary/docs/sdds/v2/fox.md
  - Canary/canary/services/fox/
  - Canary/canary/blueprints/fox_wired.py
  - Canary/canary/blueprints/fox_mcp.py
last-compiled: 2026-04-23
needs-review: 2026-05-07
method-role: Writer
method-stage: close
---

# Canary Fox Case Management

## Summary

Fox is Canary's case management and evidence locker. When a merchant decides a Chirp alert warrants investigation, Fox opens a case, links the originating alerts, tracks subjects of interest, stores evidence with a cryptographic chain of custody, and maintains an append-only audit timeline. The evidence table is insert-only at the database level. The hash chain is computed by a PostgreSQL trigger, not by application code, so even a compromised application cannot forge a valid chain.

## What it does

Fox bridges automated detection and human investigation. Chirp produces alerts; Fox turns alerts into cases that people work on. A case tracks status through a state machine, accumulates evidence files with provenance, identifies subjects (employees, customers, vendors), and logs every action an investigator takes. The entire history of a case — every status change, every file uploaded, every view of that file — is preserved in an immutable timeline.

In the mobile UX, Fox surfaces as "The Vault." That framing matters: Fox is not where decisions are made. It's where the record of how decisions were made is kept.

## How it works

### Three tiers of integrity

Fox uses seven tables in the `app` schema, grouped by integrity guarantees:

**Tier 1 — operational (soft-delete).** Cases, alert links, subjects, and actions. These use `SoftDeleteMixin` — they can be updated and marked deleted, but the row persists. This is the working layer where investigators do their work.

**Tier 2 — immutable audit (append-only).** The case timeline. No update, no delete, enforced by a PostgreSQL INSERT-ONLY trigger. This is the ledger of what happened to the case.

**Tier 3 — evidentiary chain (insert-only, hash-chained).** Evidence files and their access log. Not just append-only but hash-chained: each evidence row references the previous row's chain hash. PostgreSQL triggers compute the chain and block updates and deletes. This is the forensic layer.

### Case lifecycle

Cases move through a strict state machine enforced by `FoxCaseService.update_case_status()`:

```
open -> investigating -> pending_review -> escalated -> closed
                                        -> closed
                                        -> referred_to_le

closed          (terminal)
referred_to_le  (terminal)
```

Invalid transitions raise `ValueError` (HTTP 400). Every status transition writes two rows: a `fox_case_timeline` entry (event_type=`status_change`, old and new status in metadata) and a `fox_case_actions` row. The timeline is the audit; the action is the investigator's logged step.

### The seven tables

**fox_cases** — root investigation record. UUID primary key, tenant-scoped by `merchant_id`. Carries `case_number` (`CASE-YYYY-NNNNN`, unique per merchant per year), case type (`theft`, `fraud`, `policy_violation`, `cash_variance`, `return_abuse`, `transaction_review`, `other`), priority (`low` through `critical`), status, assignee, opened/closed timestamps, resolution narrative, and `total_loss_cents`. Uses `TenantMixin`, `AuditMixin`, `SoftDeleteMixin`.

**fox_case_alerts** — junction table linking alerts to cases. Cross-database reference (alert_id is a string FK because alerts live in a different schema's write boundary). Records who linked the alert and when.

**fox_subjects** — persons or entities of interest. Types: `employee`, `customer`, `vendor`, `unknown`. Links to the entity table via `entity_id` (validated for employees, deferred for customer/vendor until canonical lookup tables exist).

**fox_case_actions** — investigation actions taken. Types include `investigate`, `interview`, `suspend`, `terminate`, `refer_to_le`, `refer_to_hr`, `coaching`, `no_action`, `status_change`. Soft-deletable.

**fox_case_timeline** — append-only event log. Event types: `created`, `status_change`, `note_added`, `evidence_added`, `assigned`, `escalated`, `closed`, `alert_linked`, `action_added`. No mixins — the timeline IS the audit trail. Protected by an insert-only DB trigger.

**fox_evidence** — insert-only evidence with hash chain. Each row stores a file reference (path, name, size, content type), a SHA-256 of the file content (computed by the application), and a chain hash (computed by a DB trigger). Types: `document`, `photo`, `video`, `receipt`, `screenshot`, `export`, `other`. Insert-only and update/delete-blocked by triggers.

**fox_evidence_access_log** — insert-only access audit. Every view, download, print, export, and upload of an evidence item gets a row here. Captures actor and IP address. No mechanism exists to hide or delete access records.

### The hash chain

The evidence chain is computed by a PostgreSQL `BEFORE INSERT` trigger named `compute_entry_hash()`. The application sends `chain_hash="TRIGGER_WILL_OVERWRITE"` as a placeholder. The trigger:

1. Finds the most recent evidence row for this case, ordered by `uploaded_at DESC`
2. For the first evidence in a case: `chain_hash = SHA-256(file_hash)`, `previous_chain_hash = NULL`
3. For subsequent rows: `chain_hash = SHA-256(prev_chain_hash + file_hash)`, `previous_chain_hash` links to the prior row

After the insert, the app calls `session.flush()` to commit the trigger-computed value and `session.refresh()` to read it back. The chain verification endpoint (`GET /api/fox/cases/<id>/evidence/verify`) calls `verify_hash_chain()` — a PostgreSQL function that walks the chain server-side and returns `{valid, total_evidence, broken_at}`. If the DB function isn't deployed, the endpoint degrades gracefully with `valid: null`.

Two chain algorithms exist in the codebase and intentionally do not share code:

| Module | Algorithm | Storage | Used by |
|---|---|---|---|
| `hash_chain.py` | `sorted_json + "\|" + prev_hash` | 64-char hex string | `fox_evidence`, `audit_log` |
| `evidence_chain.py` | `prev_bytes \|\| event_bytes` (raw concat) | 32 bytes (BYTEA) | `evidence_records` (TSP seal path) |

The Fox chain is hex-string-based because it's viewed by humans. The TSP chain is raw BYTEA because it's a closed machine-to-machine path. See [[canary-tsp-pipeline|Canary TSP Pipeline]] for the seal-side chain.

### Alert-to-case flow

1. Chirp fires an alert (status=`new`). For six critical rules (C-009, C-104, C-204, C-301, C-502, C-602), Chirp auto-creates the case via `FoxCaseService.create_case()`. For other rules, the case is created when a merchant taps "Open case" in the UI.
2. `create_case()` generates the case number, inserts `FoxCase` (status=`open`), inserts a `created` timeline entry, and — if an `alert_id` was provided — a `FoxCaseAlert` junction row.
3. The Alert domain writes `AlertHistory` with status=`case_opened`, linking the case number in the notes. This closes the loop from Chirp's side.

### Unified case creation from context (GRO-245)

`FoxCaseService.create_case_from_context()` is the single entry point for case creation from any UI touchpoint — an alert, a list of transactions, or a drill-path filter. It:

- Auto-generates a title if none is given ("Case from 3 alert(s)", "Transaction review: 2 txn(s)", "Drill path investigation")
- Auto-fills a description from linked context
- Sets case type to `transaction_review` when transactions are linked, else `other`
- Links the first alert at creation, then adds subsequent alerts as individual `FoxCaseAlert` rows
- Writes `AlertHistory` (status=`case_opened`) for every linked alert
- Returns `{ok, case_id, case_number, evidence_count}` where `evidence_count` sums linked alerts and transactions

This collapses what used to be three code paths into one.

### Evidence upload

1. `POST /api/fox/cases/<id>/evidence` with a multipart file (or MCP `add_evidence` tool)
2. `FoxCaseService.add_evidence()` computes `SHA-256(file_data)` as `file_hash`
3. Inserts `FoxEvidence` with placeholder `chain_hash`
4. The BEFORE INSERT trigger overwrites the chain hash using the previous evidence row's chain hash
5. `session.flush()` + `session.refresh()` to read back the trigger values
6. Inserts a `FoxCaseTimeline` row (event_type=`evidence_added`)
7. Inserts a `FoxEvidenceAccessLog` row (access_type=`upload`)

### Evidence access and timeline

Every `GET /api/fox/cases/<id>/evidence/<eid>` inserts a `FoxEvidenceAccessLog` row (access_type=`view`). The timeline endpoint merges two streams: case events from `fox_case_timeline` and evidence access rows from `fox_evidence_access_log` (joined through `fox_evidence`). The merged stream is sorted by timestamp and paginated.

### Case number generation

Format: `CASE-{year}-{sequence:05d}`. Per merchant per year. Generated by counting existing cases for this merchant in the current year under `SELECT ... FOR UPDATE` to serialize concurrent creates. The sequence is derived from a row count, not a DB sequence — no gaps, but the row-level lock is required.

### Validation

Enum validation is enforced as module-level `frozenset` constants in `case_service.py`. Invalid values raise `ValueError` with the offending value and the sorted valid options. The sets cover priorities, case types, statuses, action types, subject types, and timeline event types. Timeline metadata is validated per event type before insert — `status_change` requires `old_status` and `new_status`, `evidence_added` requires `evidence_id`, `assigned` requires `assigned_to`.

## Key decisions

**Database-enforced immutability.** The evidence chain is computed by a PostgreSQL trigger, not by application code. The application literally cannot forge a chain hash that passes server-side verification. This matters for chain-of-custody defensibility: the integrity guarantee does not depend on the application being uncompromised.

**Three tiers of integrity.** Operational tables allow the work to happen. The timeline preserves how it happened. The evidence chain proves what was collected. Each tier's guarantees are enforced at the layer below the ORM so they cannot be bypassed from Python.

**Evidence stores references, not copies.** The evidence table holds file paths and SHA-256 content hashes, not binary blobs. The files themselves live in object storage (RaaS raw data), with the GUID reference in the row. Canary is a lens over the evidence, not the storage system. This keeps the database small and lets the storage layer evolve independently.

**Access log is insert-only.** Every view of every evidence item leaves a row. There is no mechanism to hide that a file was viewed. This is deliberate — access patterns are themselves evidence.

**Two hash chain algorithms, kept separate.** The Fox chain and the TSP evidence chain solve different problems and use different algorithms. They are intentionally not refactored into a shared module. The Fox chain is human-readable (hex, sorted JSON); the TSP chain is machine-readable (BYTEA). Merging them would force one compromise on the other.

**Best-effort auto-casing from Chirp.** When Chirp tries to auto-create a case for a critical alert, failures log a warning and move on. The alert still fires. The investigator still sees it. The case can be opened manually. Chirp never blocks on Fox.

**Entity resolution is enum-gated.** Adding a subject to a case validates the subject type (`employee`, `customer`, `vendor`, `unknown`). Employee linking hits the `Employee` table; other types currently return `True` without a lookup table. The frozenset is the boundary — unknown subject types are rejected, not silently accepted.

**Unified context entry point.** `create_case_from_context()` absorbs alert-origin, transaction-origin, and drill-filter-origin case creation into one method. Prior to GRO-245, each UI touchpoint had its own path; consolidating means title generation, description building, and AlertHistory writes are consistent regardless of where the case came from.

## Code pointers

- [canary/services/fox/case_service.py](../../Canary/canary/services/fox/case_service.py) — `FoxCaseService`, all business logic, enum validation, state machine enforcement, unified context creation
- [canary/services/fox/tools.py](../../Canary/canary/services/fox/tools.py) — 8 MCP tool definitions for `canary-fox`
- [canary/services/hash_chain.py](../../Canary/canary/services/hash_chain.py) — Fox-style hex-string chain (pipe-delimited, sorted JSON)
- [canary/services/evidence_chain.py](../../Canary/canary/services/evidence_chain.py) — TSP-style BYTEA chain (referenced here for contrast)
- [canary/blueprints/fox_wired.py](../../Canary/canary/blueprints/fox_wired.py) — REST API at `/api/fox/*`, JWT + role-gated writes
- [canary/blueprints/fox_mcp.py](../../Canary/canary/blueprints/fox_mcp.py) — MCP blueprint at `/fox/*`, 8 tools
- [canary/models/fox/](../../Canary/canary/models/fox/) — SQLAlchemy models: cases, case_alerts, subjects, actions, timeline, evidence, evidence_access_log

## Related

- [[canary-chirp-rules|Canary Chirp Rules]] — What produces the alerts that become cases (including the six auto-case rules)
- [[canary-tsp-pipeline|Canary TSP Pipeline]] — The other evidence chain (TSP seal path)
- [[canary-data-model|Canary Data Model]] — Fox tables (in `app` schema) and mixins
- [[canary-architecture|Canary Architecture]] — Where Fox sits in the service mesh
- [[Brain/projects/Canary|Canary MOC]]

## Sources

- `Canary/docs/sdds/v2/fox.md` — Source SDD (design authority)
- `Canary/canary/services/fox/` — Implementation (code authority)
- `Canary/canary/blueprints/fox_wired.py`, `fox_mcp.py` — HTTP and MCP surfaces
- `Canary/canary/models/fox/` — SQLAlchemy models
