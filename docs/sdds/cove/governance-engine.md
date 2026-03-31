# Governance Engine

> **Status:** Complete — written from code
> **Namespace:** cove
> **Last updated:** 2026-03-30
> **Code location:** `Cove/cove/governance/`, `Cove/cove/models/governance.py`

---

## 1. Overview

The Governance Engine is the core voting and deliberation system for Cove. It manages the full lifecycle of association governance actions — from drafting a proposal through notice, voting, result tallying, and certification — while maintaining strict Davis-Stirling compliance at every step.

The engine covers two distinct but co-located subsystems:

**Proposals and Voting** (`governance/`) — Manages the six statutory proposal types (resolution, bylaw amendment, CC&R amendment, election, operating rule, special assessment) plus director removal. Each type carries bylaws-driven defaults for quorum, threshold, notice period, ballot period, and ballot secrecy. A state machine enforces the `draft → noticed → open → closed → certified → petitioned` lifecycle. Voting enforces ballot secrecy by writing vote content and voter identity to separate tables.

**Proceedings Tracker** (`governance/proceeding_routes.py`, `governance/proceeding_services.py`) — A defense timeline system for tracking city, state, and California Coastal Commission proceedings that affect the association's property or easements. Proceedings are independent of proposals and do not drive votes; they are an evidence and status log for external regulatory actions.

The engine is also the home of `quorum.py`, a standalone calculator used by both proposals and elections, and `bylaws_config.py`, which reads governance rules from `wpbca-bylaws-config.json` rather than hardcoding them.

---

## 2. Architecture

### Component Diagram

```
Browser
  │
  ├── GET/POST /vote/*          → governance_bp         (governance/routes.py)
  │                                 └── services.py     (proposals, voting, tallying)
  │
  ├── GET/POST /proceedings/*   → proceeding_bp         (governance/proceeding_routes.py)
  │                                 └── proceeding_services.py
  │
  └── (used by election_bp)     → quorum.py             (QuorumCalculator)
                                 → bylaws_config.py     (load_bylaws_config)

Internal reads
  bylaws_config.py   ─────────→ wpbca-bylaws-config.json  (lru_cache)
  quorum.py          ─────────→ wpbca-bylaws-config.json  (lru_cache)
  services.py        ─────────→ bylaws_config.py (primary)
                              → PROPOSAL_TYPE_DEFAULTS    (fallback)

Storage
  proposals          → PostgreSQL cove.proposals
  ballots            → PostgreSQL cove.ballots            (vote content only)
  ballot_envelopes   → PostgreSQL cove.ballot_envelopes   (voter identity — RLS)
  proceedings        → PostgreSQL cove.proceedings
  proceeding_entries → PostgreSQL cove.proceeding_entries
  audit_log          → PostgreSQL cove.audit_log          (insert-only)
```

### Request / Data Flow

**Creating a Proposal (board only)**

```
POST /vote/create
  → ProposalForm.validate_on_submit()
  → services.create_proposal(org_id, created_by, title, description, type)
      → bylaws_config.get_proposal_defaults(type)      # load JSON defaults
      → Proposal(status="draft", threshold=..., ...)   # bylaw values baked in
      → db.session.flush()                             # get proposal.id
      → AuditLog("proposal.created")
      → db.session.commit()
  → redirect /vote/<proposal_id>
```

**Lifecycle Transition (board only)**

```
POST /vote/<id>/transition
  → services.transition_proposal(id, actor_id)
      → VALID_TRANSITIONS[current_status] → next_status
      → if noticed→open: enforce notice_period_days vs noticed_at
      → proposal.status = next_status
      → proposal.<state>_at = utcnow()
      → AuditLog("proposal.transitioned")
      → db.session.commit()
      → if next_status == "open":
            notifications.notify_all_members("vote_notice")   # fire-and-forget
```

**Casting a Vote (any active member)**

```
POST /vote/<id>/ballot
  → BallotForm.validate_on_submit()          # vote + password only — no member field
  → services.cast_vote(proposal_id, member, vote, password, ip_address)
      → validate vote ∈ {yes, no, abstain}
      → proposal.status == "open"
      → member.voting_weight > 0             # bylaw §5.2
      → member.membership_status == "active"
      → check_password_hash(member.password_hash, password)  # re-auth
      → has_voted(member_id, proposal_id)    # EXISTS on ballot_envelopes
      → Ballot(proposal_id, vote, method="electronic")       # NO member_id
      → db.session.flush()                   # get ballot.id
      → BallotEnvelope(ballot_id, member_id, proposal_id)    # sealed link
      → Proposal.yes_count|no_count|abstain_count += 1       # atomic UPDATE
      → AuditLog("vote.cast", details={method})              # WHO, never WHAT
      → db.session.commit()
  → render vote_confirmed.html
```

**Getting Results**

```
GET /vote/<id>/results  (only if status in closed|certified)
  → services.get_results(proposal_id)
      → get_eligible_voter_count(org_id)     # active members, voting_weight > 0
      → check_quorum(proposal, eligible)
      → determine_result(proposal, quorum)
      → return {proposal, quorum, result, eligible_voters, total_votes, turnout}
  -- NEVER reads ballot_envelopes --
```

### Key Design Decisions

**Ballot secrecy via table split.** Vote content (`ballots`) and voter identity (`ballot_envelopes`) are in separate tables. The `ballots` table has no `member_id` column — structurally impossible to join them without going through the sealed envelope table, which is protected by PostgreSQL Row-Level Security. The application layer enforces this in code: `services.py` explicitly documents that tallying reads *only* from `proposals.yes_count|no_count|abstain_count`, never from `ballot_envelopes`. The audit log records that a vote was cast and by whom, but never records the vote value.

**Atomic vote counts.** Rather than counting rows in `ballots` at query time (which could produce inconsistent reads), the engine issues a raw SQL `UPDATE proposals SET yes_count = yes_count + 1` immediately after the ballot insert, inside the same transaction. This keeps `proposals.total_votes` consistent under concurrent voting.

**Bylaws-as-config.** All quorum thresholds, notice periods, passage thresholds, and legislative citations live in `wpbca-bylaws-config.json`, loaded once into `lru_cache`. The Python code (`services.py`, `quorum.py`) calls the config loader and falls back to an in-code `PROPOSAL_TYPE_DEFAULTS` dict only when the JSON file is unavailable (e.g., stripped test environments). This means governance rule changes do not require code deployments.

**Notice period enforcement in state machine.** When advancing `noticed → open`, the transition service checks whether `proposal.noticed_at + notice_period_days <= now`. If not, the transition raises `ValueError` with the earliest permissible date. This enforces Davis-Stirling §4360 notice requirements at the application layer.

**QuorumCalculator is Flask-free.** `quorum.py` has no Flask imports and no SQLAlchemy dependency. It reads the JSON config directly and operates on integers passed by the caller. This makes it testable without an application context and reusable by the elections subsystem without coupling.

---

## 3. Data Model

All tables use `String(36)` UUID primary keys (historical pattern — new tables should use native `Mapped[uuid.UUID]`). All timestamps are UTC.

### Proposal

Table: `proposals`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `Mapped[str]` — `String(36)` PK | UUID v4 |
| `organization_id` | `Mapped[str]` — FK `organizations.id` | tenant scope |
| `title` | `Mapped[str]` — `String(500)` | required |
| `description` | `Mapped[str]` — `Text` | full proposal text |
| `type` | `Mapped[str]` — `String(30)` | resolution, bylaw_amendment, ccr_amendment, election, operating_rule, special_assessment, director_removal |
| `threshold` | `Mapped[float]` | pass ratio — e.g. 0.50, 0.67 |
| `quorum_required` | `Mapped[float]` | 0.00 = none, 0.33 = 1/3, 0.50 = 1/2 |
| `requires_secret_ballot` | `Mapped[bool]` | True for most member votes |
| `notice_period_days` | `Mapped[int]` | min days between noticed and open |
| `ballot_period_days` | `Mapped[int]` | 0 = voted at meeting |
| `status` | `Mapped[str]` — `String(20)` | draft, noticed, open, closed, certified, petitioned |
| `created_by` | `Mapped[str]` — FK `members.id` | board member who created |
| `noticed_at` | `Mapped[datetime \| None]` | set on draft→noticed |
| `opened_at` | `Mapped[datetime \| None]` | set on noticed→open |
| `closed_at` | `Mapped[datetime \| None]` | set on open→closed |
| `certified_at` | `Mapped[datetime \| None]` | set on closed→certified |
| `chain_tx_hash` | `Mapped[str \| None]` — `String(100)` | future blockchain anchor |
| `yes_count` | `Mapped[int]` | atomically incremented |
| `no_count` | `Mapped[int]` | atomically incremented |
| `abstain_count` | `Mapped[int]` | atomically incremented |
| `embedding` | `Mapped[list \| None]` — `Vector(1024)` | qwen3-embedding:8b, cosine search |
| `created_at` | `Mapped[datetime]` | |
| `updated_at` | `Mapped[datetime]` | onupdate |

Computed properties:
- `total_votes` → `yes_count + no_count + abstain_count`
- `passed` → `None` unless status is `certified`; computes `yes / (yes + no) >= threshold` (abstains excluded)

Relationships: `ballots` (one-to-many), `envelopes` (one-to-many via backref).

### Ballot

Table: `ballots`

**Critical: no `member_id` column. This is by design and must never change.**

| Column | Type | Notes |
|--------|------|-------|
| `id` | `Mapped[str]` — `String(36)` PK | UUID v4 |
| `proposal_id` | `Mapped[str]` — FK `proposals.id` | |
| `vote` | `Mapped[str]` — `String(10)` | yes, no, abstain |
| `method` | `Mapped[str]` — `String(20)` | electronic, paper, in_person |
| `cast_at` | `Mapped[datetime]` | |
| `chain_hash` | `Mapped[str \| None]` — `String(100)` | SHA-256 for future audit chain |

### BallotEnvelope

Table: `ballot_envelopes`

The sealed outer envelope. Links ballot to voter. Protected by PostgreSQL Row-Level Security — only the `inspector` role has SELECT permission.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `Mapped[str]` — `String(36)` PK | UUID v4 |
| `ballot_id` | `Mapped[str]` — FK `ballots.id` | the anonymous ballot |
| `member_id` | `Mapped[str]` — FK `members.id` | the voter |
| `proposal_id` | `Mapped[str]` — FK `proposals.id` | denormalized for unique check |
| `issued_at` | `Mapped[datetime]` | |
| `sealed_at` | `Mapped[datetime \| None]` | set when ballot is cast |

Unique constraint: `uq_one_vote_per_member_per_proposal` on `(member_id, proposal_id)`.

### Proceeding

Table: `proceedings`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `Mapped[str]` — `String(36)` PK | UUID v4 |
| `organization_id` | `Mapped[str]` — FK `organizations.id` | |
| `title` | `Mapped[str]` — `String(500)` | |
| `description` | `Mapped[str]` — `Text` | |
| `apn` | `Mapped[str \| None]` — FK `parcels.apn` | optional — some proceedings are org-wide |
| `proceeding_type` | `Mapped[str]` — `String(30)` | city_planning, coastal_commission, legal_challenge, state_legislature, land_acquisition |
| `status` | `Mapped[str]` — `String(30)` | monitoring, active, resolved, archived |
| `external_reference` | `Mapped[str \| None]` — `String(255)` | case #, permit #, CCC docket |
| `filing_date` | `Mapped[datetime \| None]` | |
| `next_hearing_date` | `Mapped[datetime \| None]` | |
| `created_by` | `Mapped[str]` — FK `members.id` | |
| `created_at` | `Mapped[datetime]` | |
| `updated_at` | `Mapped[datetime]` | updated when entries added |

Relationships: `organization`, `parcel`, `created_by_member`, `entries` (cascade delete).

### ProceedingEntry

Table: `proceeding_entries`

| Column | Type | Notes |
|--------|------|-------|
| `id` | `Mapped[str]` — `String(36)` PK | UUID v4 |
| `proceeding_id` | `Mapped[str]` — FK `proceedings.id` | |
| `entry_date` | `Mapped[datetime]` | date of the event (not insert time) |
| `title` | `Mapped[str]` — `String(500)` | |
| `description` | `Mapped[str]` — `Text` | |
| `entry_type` | `Mapped[str]` — `String(30)` | filing, hearing, decision, correspondence, update, evidence |
| `source` | `Mapped[str \| None]` — `String(255)` | e.g. "City of RPV Planning Dept" |
| `document_url` | `Mapped[str \| None]` — `String(500)` | link to external filing |
| `created_by` | `Mapped[str]` — FK `members.id` | |
| `created_at` | `Mapped[datetime]` | |

### Meeting

Table: `meetings` (defined in `cove/models/meetings.py`, relevant to governance scheduling)

| Column | Type | Notes |
|--------|------|-------|
| `id` | `Mapped[str]` — `String(36)` PK | |
| `organization_id` | `Mapped[str]` — FK `organizations.id` | |
| `type` | `Mapped[str]` — `String(30)` | annual_member, special_member, regular_board, special_board, arc_review, committee |
| `title` | `Mapped[str]` — `String(500)` | |
| `date` | `Mapped[date]` | |
| `time` | `Mapped[str]` — `String(10)` | "19:00" |
| `location` | `Mapped[str]` — `String(500)` | |
| `agenda` | `Mapped[str \| None]` — `Text` | |
| `minutes` | `Mapped[str \| None]` — `Text` | |
| `notice_required_days` | `Mapped[int]` | default 4 for board, 10 for member meetings |
| `notice_sent_at` | `Mapped[datetime \| None]` | |
| `video_call_url` | `Mapped[str \| None]` | |
| `status` | `Mapped[str]` — `String(20)` | scheduled, noticed, held, cancelled |
| `embedding` | `Mapped[list \| None]` — `Vector(1024)` | semantic search |

Computed properties: `notice_deadline` (date), `has_sufficient_notice` (bool), `type_display` (str).

### ARCApplication / ARCReview

Tables: `arc_applications`, `arc_reviews` (defined in `cove/models/meetings.py`).

`ARCApplication` records member requests for architectural modifications, linked to a parcel via `apn`. Statuses: submitted, complete, under_review, approved, denied, appealed. Fee: $75 (new build/addition) or $15 (landscaping/facade). `ARCReview` records the board decision, optionally linked to a `Meeting` where it was reviewed.

---

## 4. Interfaces

### HTTP Routes — governance_bp (prefix: `/vote`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vote/` | login_required | List all proposals; `?status=` filter |
| GET | `/vote/create` | board only | Proposal creation form |
| POST | `/vote/create` | board only | Submit new proposal |
| GET | `/vote/<proposal_id>` | login_required | Proposal detail + voted status |
| POST | `/vote/<proposal_id>/transition` | board only | Advance lifecycle state |
| GET | `/vote/<proposal_id>/ballot` | login_required | Ballot form (redirects if voted or not open) |
| POST | `/vote/<proposal_id>/ballot` | login_required | Cast vote (password re-auth) |
| GET | `/vote/<proposal_id>/results` | login_required | Results (closed or certified only) |
| POST | `/vote/<proposal_id>/certify` | board only | Advance closed→certified |

The endpoint `governance.index` is an alias for `governance.proposals` at `GET /vote/`, registered so `url_for('governance.index')` resolves in navigation templates.

### HTTP Routes — proceeding_bp (prefix: `/proceedings`)

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

**ProposalForm** (`governance/forms.py`)
- `title` — StringField, 5–500 chars, required
- `description` — TextAreaField, min 20 chars, required
- `proposal_type` — SelectField from `PROPOSAL_TYPE_CHOICES`

**BallotForm** (`governance/forms.py`)
- `vote` — SelectField: yes | no | abstain
- `password` — PasswordField for re-authentication
- No member identification fields — by design (Davis-Stirling §5100-5145)

**ProceedingForm** (`governance/proceeding_forms.py`)
- `title`, `description`, `proceeding_type` — required
- `external_reference` — optional case/docket number
- `filing_date` — optional DateField

**ProceedingStatusForm** — single `status` SelectField

**ProceedingEntryForm** — `title`, `description`, `entry_type`, `entry_date` (required); `source`, `document_url` (optional)

All forms inherit from `CoveForm` which extends WTForms `FlaskForm`. CSRF is automatic.

---

## 5. Service Layer

### services.py — Proposal and Voting Services

**`get_proposal_type_defaults(proposal_type: str) -> dict`**

Loads defaults from `bylaws_config.get_proposal_defaults()` (JSON). Falls back to the hardcoded `PROPOSAL_TYPE_DEFAULTS` dict if the JSON file is unavailable. Returns a dict with keys: `threshold`, `quorum_required`, `requires_secret_ballot`, `notice_period_days`, `ballot_period_days`.

**`create_proposal(org_id, created_by, title, description, proposal_type) -> Proposal`**

Creates a `Proposal` in `draft` status with bylaw-compliant defaults applied from the JSON config. Calls `db.session.flush()` before committing to ensure the UUID is populated for the audit log.

**`get_proposal(proposal_id) -> Proposal | None`**

Single-row fetch by primary key via `db.session.get()`.

**`list_proposals(org_id, status=None) -> list[Proposal]`**

Returns proposals for an org ordered by `created_at DESC`. Optional status filter.

**`search_proposals_semantic(org_id, query, limit=10) -> list[Proposal]`**

Generates an embedding via `cove.services.embedding.generate_embedding(query)` and performs cosine similarity search using the pgvector `<=>` operator on `proposals.embedding`. Returns proposals ordered by similarity. Skips rows where `embedding IS NULL`.

**`transition_proposal(proposal_id, actor_id) -> Proposal`**

Advances the proposal state machine using `VALID_TRANSITIONS`:

```
draft → noticed → open → closed → certified
```

`petitioned` is a valid status (set externally for CC&R amendments under Civil Code §4275 court petition) but has no forward transition — it is a terminal absorbing state. The `noticed → open` transition enforces the notice period: if `noticed_at + notice_period_days > utcnow()`, a `ValueError` is raised with the earliest permissible open date. On transition to `open`, `notify_all_members()` is called in a try/except so notification failures do not block the transition.

**`has_voted(member_id, proposal_id) -> bool`**

EXISTS query against `ballot_envelopes` only. This is the only SELECT the application ever executes on that table.

**`cast_vote(proposal_id, member, vote, password, ip_address=None) -> Ballot`**

Pre-conditions checked in order:
1. `vote ∈ {yes, no, abstain}`
2. `proposal.status == "open"`
3. `member.voting_weight > 0` (bylaw §5.2 — combined lots not eligible)
4. `member.membership_status == "active"`
5. Password re-authentication via `check_password_hash`
6. Duplicate vote check via `has_voted`

Atomic transaction:
1. Insert `Ballot` (no member_id), flush to get `ballot.id`
2. Insert `BallotEnvelope` linking `ballot_id` to `member_id`
3. Raw SQL `UPDATE proposals SET <vote>_count = <vote>_count + 1` for atomicity
4. Insert `AuditLog("vote.cast")` with method only — vote value is never logged

**`get_eligible_voter_count(org_id) -> int`**

Counts members where `voting_weight > 0 AND membership_status = 'active' AND is_active = True`. Combined lots (two APNs, one member) have `voting_weight = 0` on the subordinate record, so they contribute exactly one eligible voter per bylaw §5.2.

**`check_quorum(proposal, eligible_count) -> dict`**

If `proposal.quorum_required == 0`, returns `quorum_met=True` with a note. Otherwise, computes `required = int(eligible_count * quorum_required) + 1` and checks `proposal.total_votes >= required`.

Returns: `{quorum_met, required, actual, eligible, note?}`.

**`determine_result(proposal, quorum) -> dict`**

Elections return `{type: "election", passed: None}` — plurality is resolved separately by the elections subsystem. For all other types: if quorum not met, returns `passed=False`. Otherwise computes `yes_ratio = yes / (yes + no)` (abstains excluded) and compares to `proposal.threshold`. Returns `{passed, yes_ratio, threshold, yes, no, abstain}`.

**`get_results(proposal_id) -> dict`**

Assembles the full results payload: proposal, quorum dict, result dict, eligible voter count, total votes, turnout ratio. Reads only from the `proposals` table — never touches `ballot_envelopes`.

### proceeding_services.py — Defense Tracker Services

**`create_proceeding(org_id, created_by, title, description, proceeding_type, apn=None, external_reference=None, filing_date=None) -> Proceeding`**

Validates `proceeding_type ∈ PROCEEDING_TYPES`. Creates with `status="monitoring"`. APN is optional — some proceedings (e.g., state legislature bills) apply to the whole association, not a specific parcel.

**`get_proceeding(proceeding_id) -> Proceeding | None`**

Single-row fetch.

**`list_proceedings(org_id, proceeding_type=None, status=None, apn=None) -> list[Proceeding]`**

Composable filters using SQLAlchemy `select()` + `.where()` chaining. Ordered by `updated_at DESC`.

**`update_proceeding_status(proceeding_id, status, actor_id) -> Proceeding`**

Validates `status ∈ PROCEEDING_STATUSES`. Updates `proceeding.updated_at` explicitly.

**`add_entry(proceeding_id, created_by, title, description, entry_type, entry_date=None, source=None, document_url=None) -> ProceedingEntry`**

Validates `entry_type ∈ ENTRY_TYPES`. Defaults `entry_date` to now. Also bumps `proceeding.updated_at` so the parent surfaces at the top of the list view.

**`list_entries(proceeding_id) -> list[ProceedingEntry]`**

Ordered by `entry_date ASC` (chronological timeline order).

**`generate_evidence_summary(proceeding_id) -> dict`**

Returns `{proceeding, entries, linked_proposals}`. If the proceeding has an `apn`, fetches proposals scoped to the same org (for cross-referencing). Currently returns all org proposals rather than APN-filtered ones — a known gap (see Section 11).

### bylaws_config.py — Governance Rule Loader

Loads `wpbca-bylaws-config.json` once into `lru_cache`. Provides:

- `load_bylaws_config() -> dict` — raw config
- `get_proposal_defaults(proposal_type) -> dict` — threshold, quorum, notice, ballot period, electronic eligibility
- `get_quorum_threshold(context) -> float` — contexts: general, assessment, secret_ballot, reconvened, board
- `is_electronic_eligible(proposal_type) -> bool` — AB 2159 compliance check
- `get_notice_periods() -> dict` — all notice period rules
- `get_assessment_limits() -> dict` — annual cap, delinquency notice period
- `get_legislative_info(law_id) -> dict | None` — citation for AB 502, AB 2159, etc.

### quorum.py — QuorumCalculator

A Flask-free, SQLAlchemy-free calculator instantiated with `total_lots: int` and driven by the JSON config. See Section 2 (Key Design Decisions) for architectural rationale.

**`QuorumCalculator.calculate(proposal_type, members_present=None, reconvened=False) -> QuorumResult`**

Returns a `QuorumResult` dataclass with: `quorum_needed`, `quorum_threshold`, `approval_threshold`, `requires_secret_ballot`, `electronic_eligible`, `notice_period_days`, `bylaw_section`, `quorum_citation`. If `members_present` is provided, also populates `quorum_met` and `votes_needed_to_pass`.

Reconvened meetings use the AB 2460 threshold (20%) instead of the standard type threshold.

**`QuorumCalculator.calculate_board_quorum() -> QuorumResult`**

Board meeting: 3 of 5 directors required (§9.13), majority-of-quorum to pass, no secret ballot.

**`QuorumCalculator.check_acclamation(candidates, seats) -> AcclamationResult`**

AB 502 (2022): if `candidates <= seats`, the election is decided by acclamation without a ballot. Returns `{candidates, seats, acclamation: bool, citation}`.

---

## 6. Configuration

### Proposal Type Defaults (from `wpbca-bylaws-config.json`)

| Type | Threshold | Quorum | Secret Ballot | Notice Days | Ballot Days | Electronic |
|------|-----------|--------|---------------|-------------|-------------|------------|
| resolution | 50% | 33% | No | 4 | 0 (at meeting) | Yes |
| bylaw_amendment | 50% | None (§5.9) | Yes | 28 | 30 | Yes |
| ccr_amendment | 67% | None (§5.9) | Yes | 28 | 30 | Yes |
| election | Plurality | None (§5.9) | Yes | 28 | 30 | Yes |
| operating_rule | 50% | None | No | 28 | 0 (board only) | No |
| special_assessment | 50% | 50% (§6.6) | Yes | 28 | 30 | No (AB 2159) |
| director_removal | 50% | 33% | Yes | 35 | 30 | Yes |

### Quorum Rules

| Context | Threshold | Citation |
|---------|-----------|----------|
| General business | 33% | §6.6.1.c |
| Special assessment | 50% | §6.6.1.a |
| Secret ballot votes | 0% (none) | §5.9 |
| Reconvened election | 20% | AB 2460 (eff. 2025) |
| Board meeting | 50% of 5 directors | §9.13 |

### State Machine Transitions

```
VALID_TRANSITIONS = {
    "draft":    "noticed",
    "noticed":  "open",
    "open":     "closed",
    "closed":   "certified",
}
```

`petitioned` is a valid terminal status (no forward transition in the map). It is applied externally for CC&R amendments that proceed to court under Civil Code §4275.

### Notice Period Enforcement

The transition from `noticed → open` requires `utcnow() >= proposal.noticed_at + timedelta(days=proposal.notice_period_days)`. If this condition is not met, the transition raises `ValueError` with the earliest permissible date formatted as `"Voting can open on or after <Month Day, Year>"`.

### Proceeding Types and Statuses

**Types:** city_planning, coastal_commission, legal_challenge, state_legislature, land_acquisition

**Statuses:** monitoring, active, resolved, archived

No enforced state machine for proceedings — status transitions are free-form via board discretion.

---

## 7. Security & Compliance

### Davis-Stirling Compliance

**Civil Code §5100–5145 (Elections and Secret Ballots)**

The two-table ballot architecture directly implements the two-envelope system required by §5100 and §8.12 of the WPBCA bylaws. The `ballots` table is the anonymous inner envelope (vote content only). The `ballot_envelopes` table is the sealed outer envelope (voter identity). The inspector of elections is the only role with SELECT permission on `ballot_envelopes`, enforced at the PostgreSQL layer via Row-Level Security. The application never joins these tables for tallying.

**Civil Code §4340–4370 (Operating Rules)**

Operating rule proposals require 28 days' advance notice to members before a board vote. The `operating_rule` type in the config encodes this. Electronic voting is not available for operating rules (`electronic_eligible: false`).

**Corp Code §7512 (Quorum)**

General meetings require 1/3 quorum; assessment votes require 1/2 quorum. Secret ballot votes (bylaw §5.9) require no quorum. The `check_quorum()` function in `services.py` and `QuorumCalculator` both implement this logic, reading the threshold from the `quorum_required` field baked into the proposal at creation time.

**Civil Code §4275 (CC&R Petition)**

CC&R amendments that fail to pass but are pursued via court petition are placed in `petitioned` status. This is a terminal state — the platform records the outcome but does not attempt to drive a legal process.

### AB 502 (2022) — Acclamation

`QuorumCalculator.check_acclamation(candidates, seats)` returns `acclamation=True` when `candidates <= seats`. The elections subsystem is responsible for calling this and skipping the ballot phase when acclamation applies.

### AB 2159 (2024, eff. 2025-01-01) — Electronic Secret Ballots

Electronic voting is permitted for: bylaw_amendment, ccr_amendment, election, director_removal, resolution. It is explicitly excluded for `special_assessment` per the statute. The `electronic_eligible` field in the JSON config encodes this per type. `bylaws_config.is_electronic_eligible(type)` provides a named check.

### AB 2460 (2024, eff. 2025-01-01) — Reconvened Quorum

`QuorumCalculator.calculate(proposal_type, reconvened=True)` applies the 20% reconvened quorum threshold instead of the standard type threshold.

### Re-Authentication at Vote Cast

`cast_vote()` requires password re-authentication before recording a ballot. This prevents session hijacking from translating into fraudulent votes. The password check uses `werkzeug.security.check_password_hash` against the member's stored hash.

### Bylaw §5.2 — One Vote Per Lot

`get_eligible_voter_count()` filters for `voting_weight > 0`. Combined lots (where two APNs are owned by the same household and merged for governance purposes) are represented as one member with `voting_weight = 1`; the subordinate record has `voting_weight = 0` and cannot vote. The `cast_vote()` service also checks `member.voting_weight > 0` directly before recording the ballot.

### Audit Log

All governance actions write insert-only records to `audit_log`:
- `proposal.created` — title, type
- `proposal.transitioned` — from/to status
- `vote.cast` — method only; vote value is never in the audit log
- `proceeding.created`, `proceeding.status_updated`, `proceeding_entry.created`

Audit entries include `organization_id`, `actor_id`, `action`, `entity_type`, `entity_id`, `details` (JSON), and `ip_address`.

### CSRF

All forms inherit from `CoveForm`, which extends WTForms `FlaskForm`. The `csrf` extension (`CSRFProtect`) is initialized globally and applies to all forms.

### Org Isolation

Every route that fetches a proposal or proceeding by ID checks `obj.organization_id == current_user.organization_id` and returns HTTP 403 if the org does not match. Listing functions accept `org_id` as an explicit parameter and filter at the query level.

---

## 8. Error Handling

### Service Layer Errors

Services raise typed Python exceptions that routes catch and translate to flash messages:

| Exception | Raised by | Meaning |
|-----------|-----------|---------|
| `ValueError` | `cast_vote`, `transition_proposal`, `create_proceeding`, `add_entry`, `update_proceeding_status` | Invalid input, bad state, failed precondition |
| `LookupError` | `update_proceeding_status`, `add_entry`, `generate_evidence_summary` | Entity not found |

Routes catch `ValueError` and `LookupError` with `except (ValueError, LookupError) as exc: flash(str(exc), "error")` and redirect back to the detail page. They do not catch `Exception` broadly.

### HTTP Errors

- 404: returned when `get_proposal` or `get_proceeding` returns `None`
- 403: returned when `current_user.is_board` is False on board-only routes, or when org_id mismatch is detected

### Notification Failure Isolation

The `notify_all_members()` call inside `transition_proposal` is wrapped in a bare `except Exception: pass`. Notification failures do not roll back the lifecycle transition. This is intentional — a broken notification service must not prevent governance operations.

### Database Constraint Violations

The `BallotEnvelope` unique constraint (`uq_one_vote_per_member_per_proposal`) is the last line of defense against duplicate votes. `has_voted()` checks this before the insert, but the constraint ensures that a concurrent duplicate cannot succeed even if the application check races.

---

## 9. Testing

### Test Layers

**Unit tests** — test service functions in isolation using a test database (`cove_test`). No Flask context required for `quorum.py` (it is Flask-free).

**Integration tests** — test routes via the Flask test client with a populated test database. Cover:
- ProposalForm validation (title length, description length, valid type)
- BallotForm validation (valid vote value, password required)
- `cast_vote` preconditions (closed proposal, already voted, inactive member, combined lot, wrong password)
- `transition_proposal` notice period enforcement (advance clock, check error message)
- Org isolation (403 on cross-org proposal access)
- Results only available after close

**Smoke tests** — `GET /vote/`, `GET /proceedings/` return 200 for authenticated users.

### Key Fixtures

- `org` — Organization with WPBCA profile
- `board_member` — Member with board role, active, voting_weight=1
- `regular_member` — Active member, voting_weight=1
- `combined_lot_member` — Active member, voting_weight=0 (should not be able to vote)
- `open_proposal` — Proposal in `open` status with all required fields populated
- `draft_proposal` — Proposal in `draft` status

### Ballot Secrecy Test

A dedicated test verifies that after `cast_vote()`:
1. A `Ballot` row exists with the correct vote value and no member_id column
2. A `BallotEnvelope` row exists linking ballot_id to member_id
3. `Ballot` joined to `BallotEnvelope` does NOT appear in any result set produced by `get_results()`

### QuorumCalculator Tests

Because `quorum.py` has no Flask dependency, its tests run without an app context. Cover:
- All seven proposal types return correct `quorum_needed` for `total_lots=81`
- `reconvened=True` returns 20% threshold (AB 2460)
- `check_acclamation(3, 5)` → `acclamation=True`; `check_acclamation(6, 5)` → `acclamation=False`
- `calculate_board_quorum()` returns `quorum_needed=3` for board of 5

---

## 10. Dependencies

### Upstream

| Dependency | Purpose |
|------------|---------|
| `cove.models.member.Member` | Eligibility checks, re-authentication, voting_weight, org scoping |
| `cove.models.audit.AuditLog` | Insert-only governance event log |
| `cove.services.embedding.generate_embedding` | Semantic proposal search |
| `cove.notifications.services.notify_all_members` | Vote-open notifications (fire-and-forget) |
| `cove.extensions.db` | SQLAlchemy session |
| `wpbca-bylaws-config.json` | All governance rules and legislative citations |

### Downstream

| Consumer | Uses |
|----------|------|
| `cove/governance/election_routes.py` | `quorum.py` (QuorumCalculator) for election quorum/acclamation |
| `cove/board/routes.py` | `list_proposals()` for board dashboard summary |
| `cove/member/routes.py` | `list_proposals(status="open")` for dashboard voting prompt |

### Shared Infrastructure

| Resource | Details |
|----------|---------|
| PostgreSQL 17 | `growdirect_postgres:5432/cove` — tables: proposals, ballots, ballot_envelopes, proceedings, proceeding_entries |
| pgvector | `embedding <=> query_vector` cosine similarity on `proposals.embedding` |
| Valkey DB 1 | Session store (Flask-Session) — not directly used by governance, but all authenticated requests go through it |
| Ollama | `growdirect_ollama:11434` — `qwen3-embedding:8b` (1024d) for proposal semantic search |

---

## 11. Known Issues & Reconciliation

### Intentional Co-location: governance/ and Elections

The `governance/` directory is shared by two functional areas:
- **Proposals and voting** — the core governance workflow
- **Elections** — a specialized flow with candidates, seats, and acclamation

`quorum.py` and `bylaws_config.py` serve both. `election_routes.py` and (if it exists) `election_services.py` live in `governance/` alongside `routes.py` and `services.py`. This is intentional — quorum and bylaw configuration are shared primitives, and splitting them into separate packages would require either duplication or a shared utility package. The co-location is preferred while both subsystems remain tightly coupled through `wpbca-bylaws-config.json`.

### evidence_summary Linked Proposals Not APN-Scoped

`generate_evidence_summary()` fetches all proposals for the org when the proceeding has an APN, rather than filtering to proposals related to that specific parcel. This is a gap: the function comment implies parcel-scoped linkage, but the query does not filter by APN. A future revision should add a `parcel_id` or `apn` foreign key to `proposals` (or a linking table) to enable genuine parcel-scoped cross-referencing.

### proposal_type Column Named type

`Proposal.type` is named `type` in Python (column `type` in PostgreSQL), which shadows Python's built-in `type()` function on model instances. A code comment in `services.py` references `proposal.proposal_type` in one place (the notification call: `proposal.proposal_type.replace(...)`) which will raise `AttributeError` at runtime — the correct attribute is `proposal.type`. This is a latent bug in the notification path, which is suppressed by the bare `except Exception: pass` wrapper. The attribute should be corrected to `proposal.type` and the column renamed to `proposal_type` in a migration.

### UUID Storage as String(36)

All governance models use `String(36)` for UUID primary keys rather than the platform-standard `Mapped[uuid.UUID]` with a native `UUID` column type. This is a historical holdover from early Cove development. It is functional but suboptimal (string comparison vs. native UUID comparison, 36 bytes vs. 16 bytes per value). New tables should use native UUID. Existing tables should be migrated opportunistically.

### chain_hash / chain_tx_hash — Blockchain Anchoring Placeholder

Both `Ballot.chain_hash` and `Proposal.chain_tx_hash` are nullable columns intended for a future blockchain audit trail. No implementation exists yet. These columns have no effect on current operation.

### PROPOSAL_TYPE_DEFAULTS Fallback Diverges from JSON Config

`services.py` contains a hardcoded `PROPOSAL_TYPE_DEFAULTS` dictionary used as a fallback when `wpbca-bylaws-config.json` fails to load. The fallback sets `resolution.notice_period_days = 10`, but the JSON config (the authoritative source) sets it to `4`. If the JSON file ever fails to load, resolution proposals silently get 10-day notice periods instead of 4-day. The fallback should be regenerated from the current JSON values, or the loading mechanism should fail loudly rather than falling back to stale defaults.

### Electronic Ballot Opt-In Not Yet Enforced

AB 2159 requires member opt-in for electronic secret ballots. The `delivery_preference` column exists on `Member` (electronic | paper | both), but `cast_vote()` does not check whether the member has opted in. The `is_electronic_eligible()` check in `bylaws_config.py` covers the proposal type, but not the member's individual consent. Member-level consent enforcement is a gap.
