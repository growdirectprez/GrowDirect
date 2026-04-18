# Governance Engine — Proposal Lifecycle

> **Status:** Production-grade ops contract
> **Type:** App Service (Cove)
> **Namespace:** cove
> **Last updated:** 2026-04-13
> **Code location:** `Cove/cove/governance/`, `Cove/cove/models/governance.py`
> **Split companion:** [[docs/sdds/cove/governance-voting|Governance Voting]] — ballot mechanics, tallying, secrecy enforcement

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]

---

## Purpose

The Governance Engine manages HOA proposal lifecycle for the West Portuguese Bend Community Association (81 lots, Rancho Palos Verdes). It enforces Davis-Stirling compliance across six statutory proposal types (resolution, bylaw amendment, CC&R amendment, election, operating rule, special assessment) plus director removal. The engine drives proposals through a `draft > noticed > open > closed > certified > petitioned` state machine, enforcing notice periods, quorum thresholds, and passage ratios loaded from `wpbca-bylaws-config.json`.

This SDD covers proposal lifecycle and proceedings tracking. Voting mechanics, ballot secrecy, tallying, and quorum calculation are in [[docs/sdds/cove/governance-voting|Governance Voting]].

---

## Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| PostgreSQL 17 (`growdirect_postgres:5432/cove`) | Infrastructure | proposals, proceedings, proceeding_entries, audit_log tables |
| pgvector | Infrastructure | Cosine similarity on `proposals.embedding` for semantic search |
| Valkey DB 1 (`growdirect_valkey:6379/1`) | Infrastructure | Flask session backend (all auth goes through it) |
| Ollama (`growdirect_ollama:11434`) | Infrastructure | `qwen3-embedding:8b` (1024d) for proposal embeddings |
| `cove.models.member.Member` | App model | Eligibility, org scoping, `is_board` check, `created_by` FK |
| `cove.models.audit.AuditLog` | App model | Insert-only event log |
| `cove.services.embedding.generate_embedding` | App service | Semantic proposal search |
| `cove.notifications.services.notify_all_members` | App service | Vote-open notifications (fire-and-forget) |
| `wpbca-bylaws-config.json` | Config file | All governance rules, thresholds, legislative citations |

### Downstream Consumers

| Consumer | Uses |
|----------|------|
| `cove/governance/election_routes.py` | `quorum.py` (QuorumCalculator) for election quorum/acclamation |
| `cove/board/routes.py` | `list_proposals()` for board dashboard summary |
| `cove/member/routes.py` | `list_proposals(status="open")` for dashboard voting prompt |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Board member (browser) | Proposal title, description, type | POST form (CSRF-protected) |
| Board member (browser) | Proceeding title, description, type, APN, external ref | POST form |
| Board member (browser) | Timeline entries (title, description, type, source, doc URL) | POST form |

### What Is Stored

| Table | Field | PII Classification | Encryption | Notes |
|-------|-------|-------------------|------------|-------|
| `proposals` | `title`, `description` | internal | **plaintext** | Visible to all authenticated members |
| `proposals` | `created_by` | internal | plaintext | FK to `members.id` |
| `proposals` | `embedding` | none | n/a | Vector representation of text |
| `proceedings` | `title`, `description` | internal | plaintext | Regulatory filings — visible to members |
| `proceedings` | `apn` | public | plaintext | County assessor parcel number |
| `proceedings` | `created_by` | internal | plaintext | FK to `members.id` |
| `proceeding_entries` | `title`, `description`, `source`, `document_url` | internal | plaintext | Evidence timeline |
| `proceeding_entries` | `created_by` | internal | plaintext | FK to `members.id` |
| `audit_log` | `actor_id` | internal | plaintext | Member who performed action |
| `audit_log` | `ip_address` | **sensitive** | **plaintext** | Logged on vote cast — should be hashed |
| `audit_log` | `details` (JSON) | internal | plaintext | Action metadata; never contains vote content |

### What Exits

| Destination | Data | Notes |
|-------------|------|-------|
| Browser (Jinja2 templates) | Proposal list, detail, results | Scoped to org |
| Browser | Proceeding list, timeline, evidence summary | Scoped to org |
| Notification service | Vote-open alert (title, link) | Fire-and-forget |
| Audit log | All lifecycle transitions | Insert-only, never deleted |

---

## API Contract

### HTTP Routes -- governance_bp (prefix: `/vote`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vote/` | login_required | List all proposals; `?status=` filter |
| GET | `/vote/faq` | login_required | Governance rules FAQ (from bylaws config) |
| GET | `/vote/create` | board only | Proposal creation form |
| POST | `/vote/create` | board only | Submit new proposal |
| GET | `/vote/<proposal_id>` | login_required | Proposal detail + voted status |
| POST | `/vote/<proposal_id>/transition` | board only | Advance lifecycle state |
| GET | `/vote/<proposal_id>/ballot` | login_required | Ballot form (see governance-voting.md) |
| POST | `/vote/<proposal_id>/ballot` | login_required | Cast vote (see governance-voting.md) |
| GET | `/vote/<proposal_id>/results` | login_required | Results (closed or certified only) |
| POST | `/vote/<proposal_id>/certify` | board only | Advance closed > certified |
| POST | `/vote/<proposal_id>/recount` | board or inspector | Verify denormalized counts |
| GET | `/vote/inspector` | inspector or admin | Inspector dashboard |

The endpoint `governance.index` is an alias for `governance.proposals` at `GET /vote/`.

### HTTP Routes -- proceeding_bp (prefix: `/proceedings`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/proceedings/` | login_required | List proceedings; `?type=`, `?status=` filters |
| GET | `/proceedings/create` | board only | New proceeding form |
| POST | `/proceedings/create` | board only | Submit new proceeding |
| GET | `/proceedings/<proceeding_id>` | login_required | Detail with timeline entries |
| POST | `/proceedings/<proceeding_id>/status` | board only | Update status |
| GET | `/proceedings/<proceeding_id>/add-entry` | board only | Entry form |
| POST | `/proceedings/<proceeding_id>/add-entry` | board only | Add timeline entry |
| GET | `/proceedings/<proceeding_id>/evidence` | login_required | Evidence summary + linked proposals |

### Forms

**ProposalForm** (`governance/forms.py`): `title` (5-500 chars), `description` (min 20), `proposal_type` (SelectField from `PROPOSAL_TYPE_CHOICES`).

**ProceedingForm** (`governance/proceeding_forms.py`): `title`, `description`, `proceeding_type` (required); `external_reference`, `filing_date` (optional).

**ProceedingStatusForm**: Single `status` SelectField.

**ProceedingEntryForm**: `title`, `description`, `entry_type`, `entry_date` (required); `source`, `document_url` (optional).

All forms inherit from `CoveForm` which extends WTForms `FlaskForm`. CSRF is automatic.

---

## Operations

### Proposal State Machine

```
VALID_TRANSITIONS = {
    "draft":    "noticed",
    "noticed":  "open",
    "open":     "closed",
    "closed":   "certified",
}
```

`petitioned` is a terminal absorbing state (CC&R amendments under Civil Code 4275 court petition). No forward transition exists.

**Transition enforcement:**
- `noticed > open`: Requires `noticed_at + notice_period_days <= utcnow()`. Raises `ValueError` with earliest permissible date if violated. This enforces Davis-Stirling 4360 notice requirements.
- `open`: On entry, `notify_all_members()` is called in a try/except. Notification failure does not block the transition.

**Timestamp fields set on transition:**
- `draft > noticed`: `noticed_at`
- `noticed > open`: `opened_at`
- `open > closed`: `closed_at`
- `closed > certified`: `certified_at`

### Proposal Type Defaults (from `wpbca-bylaws-config.json`)

| Type | Threshold | Quorum | Secret Ballot | Notice Days | Ballot Days | Electronic |
|------|-----------|--------|---------------|-------------|-------------|------------|
| resolution | 50% | 33% | No | 4 | 0 (at meeting) | Yes |
| bylaw_amendment | 50% | None (5.9) | Yes | 28 | 30 | Yes |
| ccr_amendment | 67% | None (5.9) | Yes | 28 | 30 | Yes |
| election | Plurality | None (5.9) | Yes | 28 | 30 | Yes |
| operating_rule | 50% | None | No | 28 | 0 (board only) | No |
| special_assessment | 50% | 50% (6.6) | Yes | 28 | 30 | No (AB 2159) |
| director_removal | 50% | 33% | Yes | 35 | 30 | Yes |

### Bylaws-as-Config Architecture

All governance rules live in `wpbca-bylaws-config.json`, loaded once into `lru_cache` by `bylaws_config.py`. The Python code calls the config loader and falls back to a hardcoded `PROPOSAL_TYPE_DEFAULTS` dict in `services.py` only when the JSON file is unavailable. This means governance rule changes do not require code deployments.

**Config API (`bylaws_config.py`):**
- `load_bylaws_config()` -- raw config dict
- `get_proposal_defaults(proposal_type)` -- threshold, quorum, notice, ballot period, electronic eligibility
- `get_quorum_threshold(context)` -- contexts: general, assessment, secret_ballot, reconvened, board
- `is_electronic_eligible(proposal_type)` -- AB 2159 compliance check
- `get_notice_periods()` -- all notice period rules
- `get_assessment_limits()` -- annual cap, delinquency notice period
- `get_legislative_info(law_id)` -- citation for AB 502, AB 2159, etc.

### Service Layer -- Proposals

| Function | Purpose |
|----------|---------|
| `create_proposal(org_id, created_by, title, description, proposal_type)` | Creates draft with bylaw defaults |
| `get_proposal(proposal_id)` | Single-row fetch |
| `list_proposals(org_id, status=None)` | List by org, optional status filter, newest first |
| `search_proposals_semantic(org_id, query, limit=10)` | pgvector cosine similarity search |
| `transition_proposal(proposal_id, actor_id)` | Advance state machine |

### Service Layer -- Proceedings

| Function | Purpose |
|----------|---------|
| `create_proceeding(org_id, created_by, title, description, type, ...)` | Creates with status="monitoring" |
| `get_proceeding(proceeding_id)` | Single-row fetch |
| `list_proceedings(org_id, type=None, status=None, apn=None)` | Composable filters |
| `update_proceeding_status(proceeding_id, status, actor_id)` | Free-form status update |
| `add_entry(proceeding_id, created_by, title, description, entry_type, ...)` | Add timeline entry |
| `list_entries(proceeding_id)` | Chronological timeline |
| `generate_evidence_summary(proceeding_id)` | Proceeding + entries + linked proposals |

### Proceeding Types and Statuses

**Types:** city_planning, coastal_commission, legal_challenge, state_legislature, land_acquisition

**Statuses:** monitoring, active, resolved, archived

No enforced state machine -- status transitions are free-form via board discretion.

### Startup Sequence

1. Flask app factory registers `governance_bp` at `/vote` and `proceeding_bp` at `/proceedings`
2. `bylaws_config.py` loads `wpbca-bylaws-config.json` on first call (lazy, `lru_cache`)
3. No background tasks or workers -- all operations are synchronous request-response

### Health Checks

No governance-specific health endpoint. Platform health at `/health` covers Flask + DB connectivity. Governance readiness depends on:
- PostgreSQL reachable (proposals, proceedings, audit_log tables)
- `wpbca-bylaws-config.json` readable (fails loudly if missing in production, falls back silently in dev)

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| PostgreSQL down | All governance operations fail | 500 error, Flask error handler |
| `wpbca-bylaws-config.json` missing | Proposal creation uses stale fallback defaults | Silent fallback -- **gap** (see Findings) |
| Notification service down | Members not notified of open votes | Swallowed by bare except -- vote still transitions |
| Ollama down | Semantic search returns empty | `generate_embedding` returns None, query skips null embeddings |

### Monitoring

No governance-specific monitoring. Recommended alerts:
- Audit log insert failure (governance actions recorded but not committed)
- Proposal stuck in `noticed` past notice_period_days + 7 (possible forgotten transition)
- Recount mismatch (denormalized counts diverge from ballot rows)

### Configuration (Environment Variables)

No governance-specific env vars. All governance config comes from `wpbca-bylaws-config.json`. The engine inherits:
- `DATABASE_URL` -- PostgreSQL connection
- `VALKEY_URL` -- session store
- `OLLAMA_URL` -- embedding service

### Davis-Stirling Compliance Summary

| Statute | Requirement | Implementation |
|---------|------------|----------------|
| Civil Code 5100-5145 | Two-envelope secret ballot | `ballots` (no member_id) + `ballot_envelopes` (RLS-gated) |
| Civil Code 4340-4370 | 28-day notice for operating rules | `notice_period_days=28` in config |
| Corp Code 7512 | Quorum: 1/3 general, 1/2 assessments | `quorum_required` field per proposal type |
| Civil Code 4275 | CC&R court petition | `petitioned` terminal status |
| AB 502 (2022) | Acclamation for uncontested seats | `QuorumCalculator.check_acclamation()` |
| AB 2159 (2024) | Electronic secret ballots (excludes assessments) | `electronic_eligible` in config |
| AB 2460 (2024) | Reconvened quorum at 20% | `QuorumCalculator.calculate(reconvened=True)` |

### Error Handling

Services raise `ValueError` (invalid input, bad state, failed precondition) and `LookupError` (entity not found). Routes catch both with `except (ValueError, LookupError) as exc: flash(str(exc), "error")` and redirect.

HTTP errors: 404 (entity not found), 403 (not board member, or org mismatch).

### Security -- Org Isolation

Every route that fetches a proposal or proceeding by ID checks `obj.organization_id == current_user.organization_id` and returns HTTP 403 on mismatch. Listing functions filter at the query level using `org_id` parameter.

### Audit Trail

All governance actions write insert-only records to `audit_log`:
- `proposal.created` -- title, type
- `proposal.transitioned` -- from/to status
- `proposal.recount` -- actual vs recorded counts
- `proceeding.created`, `proceeding.status_updated`, `proceeding_entry.created`

Entries include `organization_id`, `actor_id`, `action`, `entity_type`, `entity_id`, `details` (JSON), `ip_address`, `timestamp`.

---

## Data Model

All tables use `String(36)` UUID primary keys (historical pattern -- new tables should use native `Mapped[uuid.UUID]`). All timestamps are UTC.

### Proposal

Table: `proposals`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID v4 |
| `organization_id` | FK `organizations.id` | tenant scope |
| `title` | `String(500)` | required |
| `description` | `Text` | full proposal text |
| `type` | `String(30)` | resolution, bylaw_amendment, ccr_amendment, election, operating_rule, special_assessment, director_removal |
| `threshold` | `Float` | pass ratio (0.50, 0.67) |
| `quorum_required` | `Float` | 0.00 = none, 0.33 = 1/3, 0.50 = 1/2 |
| `requires_secret_ballot` | `Boolean` | |
| `notice_period_days` | `Integer` | min days between noticed and open |
| `ballot_period_days` | `Integer` | 0 = voted at meeting |
| `status` | `String(20)` | draft, noticed, open, closed, certified, petitioned |
| `created_by` | FK `members.id` | board member who created |
| `noticed_at` / `opened_at` / `closed_at` / `certified_at` | `DateTime` nullable | set on state transition |
| `chain_tx_hash` | `String(100)` nullable | future blockchain anchor (unused) |
| `yes_count` / `no_count` / `abstain_count` | `Integer` | atomically incremented |
| `embedding` | `Vector(1024)` nullable | semantic search |
| `created_at` / `updated_at` | `DateTime` | |

Computed: `total_votes` (sum of counts), `passed` (None unless certified, then yes/(yes+no) >= threshold).

### Proceeding

Table: `proceedings`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID v4 |
| `organization_id` | FK `organizations.id` | |
| `title` | `String(500)` | |
| `description` | `Text` | |
| `apn` | FK `parcels.apn` nullable | org-wide if null |
| `proceeding_type` | `String(30)` | city_planning, coastal_commission, etc. |
| `status` | `String(30)` | monitoring, active, resolved, archived |
| `external_reference` | `String(255)` nullable | case/permit/docket number |
| `filing_date` / `next_hearing_date` | `DateTime` nullable | |
| `created_by` | FK `members.id` | |
| `created_at` / `updated_at` | `DateTime` | |

### ProceedingEntry

Table: `proceeding_entries`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID v4 |
| `proceeding_id` | FK `proceedings.id` | |
| `entry_date` | `DateTime` | date of event (not insert time) |
| `title` | `String(500)` | |
| `description` | `Text` | |
| `entry_type` | `String(30)` | filing, hearing, decision, correspondence, update, evidence |
| `source` | `String(255)` nullable | e.g. "City of RPV Planning Dept" |
| `document_url` | `String(500)` nullable | link to external filing |
| `created_by` | FK `members.id` | |
| `created_at` | `DateTime` | |

---

## Deployment

### Docker Service

Governance runs inside the `cove_flask` container (Gunicorn on 5002:5000). No separate service.

```yaml
# Cove/devops/docker-compose.yml
cove_flask:
  build: ..
  image: cove-flask
  ports: ["5002:5000"]
  networks: [growdirect]
  environment:
    DATABASE_URL: postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
    VALKEY_URL: redis://growdirect_valkey:6379/1
    OLLAMA_URL: http://growdirect_ollama:11434
```

### AWS Target

- **Compute:** ECS/Fargate (cove_flask task definition)
- **Database:** RDS PostgreSQL 17 with pgvector extension
- **Secrets:** AWS Secrets Manager for `DATABASE_URL`, `SECRET_KEY`
- **Config:** `wpbca-bylaws-config.json` baked into container image (not a secret)

### CI/CD Requirements

- Alembic migration runs before container swap
- RLS policies on `ballot_envelopes` verified post-migration
- `wpbca-bylaws-config.json` present in image (build fails without it)

---

## Code Review Findings

### GOV-F01: Fallback Defaults Diverge from JSON Config

**Severity:** P1 (before GA)

`services.py` contains a hardcoded `PROPOSAL_TYPE_DEFAULTS` dictionary used when `wpbca-bylaws-config.json` fails to load. The fallback sets `resolution.notice_period_days = 10`, but the JSON config (the authoritative source) sets it to `4`. If the JSON file fails to load, resolution proposals silently get 10-day notice periods instead of 4. The fallback should fail loudly in production or be regenerated from current JSON values.

**Recommended fix:** Remove silent fallback. In production, if `wpbca-bylaws-config.json` is unreadable, raise a startup error. In test environments, use a `test-bylaws-config.json` fixture.

**Linear issue:** TBD

### GOV-F02: `proposal.proposal_type` AttributeError in Notification Path

**Severity:** P1 (before GA)

In `transition_proposal()`, the notification call references `proposal.proposal_type.replace('_', ' ')` but the column is named `type`, not `proposal_type`. This raises `AttributeError` at runtime. The error is currently suppressed by the bare `except Exception: pass` wrapper on the notification block. Members are never notified when voting opens.

**Recommended fix:** Change `proposal.proposal_type` to `proposal.type` on line 224 of `services.py`. Consider narrowing the bare except to specific notification errors.

**Linear issue:** TBD

### GOV-F03: IP Addresses Logged Plaintext in Audit Log

**Severity:** P1 (before GA)

`audit_log.ip_address` stores raw IP addresses as `String(45)`. Vote-cast events include the voter's IP, which is PII under CCPA. IPs should be hashed or masked before storage.

**Recommended fix:** Hash IP with HMAC-SHA256 using a rotating salt before inserting into audit log. Retain prefix (e.g., `192.168.x.x`) for debugging if needed.

**Linear issue:** TBD

### GOV-F04: No Data Retention Policy

**Severity:** P1 (before GA)

No automated purge for audit logs, completed proposals, or archived proceedings. Davis-Stirling requires certain records to be retained (4 years for election materials per Civil Code 5125), but there is no mechanism to purge stale data or enforce retention windows.

**Recommended fix:** Implement retention policy: audit logs > 7 years archived to cold storage, ballot records retained 4 years minimum (statutory), proceedings retained indefinitely (legal defense records).

**Linear issue:** TBD

### GOV-F05: evidence_summary Linked Proposals Not APN-Scoped

**Severity:** P2 (post-launch)

`generate_evidence_summary()` fetches all proposals for the org when the proceeding has an APN, rather than filtering to proposals related to that specific parcel. The function comment implies parcel-scoped linkage, but the query does not filter by APN.

**Recommended fix:** Add a `parcel_id` or `apn` FK to `proposals` or create a linking table for genuine parcel-scoped cross-referencing.

**Linear issue:** TBD

### GOV-F06: UUID Storage as String(36)

**Severity:** P2 (post-launch)

All governance models use `String(36)` for UUID primary keys instead of native `Mapped[uuid.UUID]`. This is functional but suboptimal (36 bytes vs 16 bytes, string comparison vs native). New tables should use native UUID. Existing tables migrated opportunistically.

**Recommended fix:** Migration to `UUID` column type for governance tables during a maintenance window.

**Linear issue:** TBD

### GOV-F07: `PROPOSAL_TYPE_DEFAULTS` Fallback Missing `director_removal`

**Severity:** P2 (post-launch)

The hardcoded fallback dict in `services.py` does not include `director_removal`. If the JSON config fails to load and someone creates a director removal proposal, the service raises `ValueError("Unknown proposal type")`. The JSON config does include it.

**Recommended fix:** Either add `director_removal` to the fallback dict or (preferred) eliminate the fallback per GOV-F01.

**Linear issue:** TBD

### GOV-F08: Bare `except Exception: pass` on Notification

**Severity:** P2 (post-launch)

The notification call in `transition_proposal()` swallows all exceptions silently. Combined with GOV-F02 (AttributeError), this means members are never notified and no one knows. At minimum, log the exception.

**Recommended fix:** Replace `except Exception: pass` with `except Exception: logger.exception("Notification failed for proposal %s", proposal_id)`.

**Linear issue:** TBD

---

## Production Readiness Checklist

- [ ] PII encrypted at rest -- `ip_address` in audit_log stored plaintext (GOV-F03)
- [ ] Secrets in AWS Secrets Manager (not .env) -- pending AWS deployment
- [ ] Health check endpoint responds -- `/health` exists (platform-level)
- [ ] Audit logging for sensitive operations -- all lifecycle transitions logged; vote.cast logged without vote content
- [ ] Data retention policy implemented -- not implemented (GOV-F04)
- [ ] Rate limiting on public endpoints -- no public endpoints (all behind `@login_required`)
- [ ] Error responses don't leak internals -- ValueError messages are user-facing strings, no stack traces
- [x] CSRF protection on all forms -- CoveForm base class
- [x] Org isolation enforced -- every route checks `organization_id` match
- [x] State machine transitions enforced -- `VALID_TRANSITIONS` dict, notice period check
- [x] Bylaws config loaded from JSON (not hardcoded) -- `lru_cache` loader
- [x] Audit trail for all governance actions -- insert-only audit_log
- [ ] Notification failure logged (not silently swallowed) -- GOV-F08
- [ ] Fallback defaults match authoritative config -- divergence detected (GOV-F01)

---

## Known Issues (Non-Finding)

### Intentional Co-location: governance/ and Elections

The `governance/` directory is shared by proposals/voting and elections. `quorum.py` and `bylaws_config.py` serve both. This is intentional -- splitting would require duplication or a shared utility package.

### chain_hash / chain_tx_hash -- Blockchain Anchoring Placeholder

Both `Ballot.chain_hash` and `Proposal.chain_tx_hash` are nullable columns intended for a future blockchain audit trail. No implementation exists. These columns have no effect on current operation.
