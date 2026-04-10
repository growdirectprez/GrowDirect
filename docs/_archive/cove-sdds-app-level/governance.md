# SDD: Governance Module

**Status:** Active
**Last updated:** 2026-03-29
**Blueprints:** `governance_bp` at `/vote`, `election_bp` at `/vote/election`, `proceeding_bp` at `/proceedings`

---

## Overview

Three sub-systems: proposals/voting (secret ballot, yes/no/abstain), board elections (plurality, candidates, acclamation), and defense proceedings (tracker for city/CCC/legal matters). All governed by WPBCA bylaws via `bylaws_config.py` backed by `data/wpbca-bylaws-config.json`.

---

## Routes

### Proposals (`governance_bp`, prefix `/vote`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vote/` | Required | List proposals by status: open, noticed, draft (board only), closed, certified |
| GET/POST | `/vote/create` | Required + `is_board` inline check | Create new proposal in draft status |
| GET | `/vote/<proposal_id>` | Required | Proposal detail: status, quorum, vote button, board transitions |
| POST | `/vote/<proposal_id>/transition` | Required + `is_board` inline check | Advance status: draft->noticed->open->closed |
| GET/POST | `/vote/<proposal_id>/ballot` | Required + eligibility checks inline | Show yes/no/abstain ballot form; cast vote with password re-auth |
| GET | `/vote/<proposal_id>/results` | Required | Results for closed/certified proposals |
| POST | `/vote/<proposal_id>/certify` | Required + `is_board` inline check | Certify closed proposal (closed->certified) |

### Elections (`election_bp`, prefix `/vote/election`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vote/election/` | Required | List all elections |
| GET/POST | `/vote/election/create` | Required + `is_board` inline check | Create election (creates Proposal + Election records) |
| GET | `/vote/election/<proposal_id>` | Required | Election detail: candidates, acclamation status, quorum |
| GET/POST | `/vote/election/<proposal_id>/candidates/add` | Required (any member) | Nominate a candidate — nomination is NOT board-only |
| POST | `/vote/election/<proposal_id>/candidates/<candidate_id>/withdraw` | Required + `is_board` inline check | Withdraw a candidate |
| POST | `/vote/election/<proposal_id>/acclamation` | Required + `is_board` inline check | Declare acclamation (AB 502) |
| GET/POST | `/vote/election/<proposal_id>/ballot` | Required + eligibility checks inline | Show candidate selection form; cast election ballot with password re-auth |
| GET | `/vote/election/<proposal_id>/results` | Required | Ranked candidate results |
| POST | `/vote/election/<proposal_id>/certify` | Required + `is_board` inline check | Certify election results |

### Proceedings (`proceeding_bp`, prefix `/proceedings`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/proceedings/` | Required | List proceedings; accepts `?type=` and `?status=` filters |
| GET/POST | `/proceedings/create` | Required + `is_board` inline check | Create a new proceeding |
| GET | `/proceedings/<proceeding_id>` | Required | Detail view with timeline entries |
| POST | `/proceedings/<proceeding_id>/status` | Required + `is_board` inline check | Update proceeding status |
| GET/POST | `/proceedings/<proceeding_id>/add-entry` | Required + `is_board` inline check | Add a timeline entry |
| GET | `/proceedings/<proceeding_id>/evidence` | Required | Evidence summary with linked proposals |

---

## Access Control

Governance routes currently use inline access checks (`if not current_user.is_board: abort(403)`). Shared decorators (`board_required`, `board_or_admin_required`, `admin_required`, `inspector_required`) now exist in `cove/auth/decorators.py` but are not yet adopted in governance routes — migration is a Phase 2 tech debt item. Voter eligibility (voting weight, status) is checked inside the service layer (`cast_vote`, `cast_election_vote`).

---

## Forms

**`cove/governance/forms.py`**

### `ProposalForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `title` | `StringField` | DataRequired, Length(5-500) | |
| `description` | `TextAreaField` | DataRequired, Length(min=20) | Full proposal text |
| `proposal_type` | `SelectField` | DataRequired | Choices: `resolution`, `bylaw_amendment`, `ccr_amendment`, `operating_rule`, `special_assessment` |

### `BallotForm` (extends `CoveForm`)

NO member identification fields. Davis-Stirling compliance.

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `vote` | `SelectField` | DataRequired | Choices: `yes`, `no`, `abstain` |
| `password` | `PasswordField` | DataRequired | Re-authentication for vote casting |

**`cove/governance/election_forms.py`**

### `ElectionForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `title` | `StringField` | DataRequired, Length(5-500) | |
| `description` | `TextAreaField` | DataRequired, Length(min=20) | |
| `seats` | `IntegerField` | DataRequired, NumberRange(1-20) | Default 5 (WPBCA) |
| `term_years` | `IntegerField` | DataRequired, NumberRange(1-5) | Default 1 |
| `nomination_opens_at` | `DateField` | Optional | |
| `nomination_closes_at` | `DateField` | Optional | |

### `CandidateForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `name` | `StringField` | DataRequired, Length(2-255) | Full legal name |
| `statement` | `TextAreaField` | Optional, Length(max=2000) | Candidate statement |
| `is_write_in` | `BooleanField` | | Write-in candidate flag |

### `ElectionBallotForm` (extends `CoveForm`)

NO member identification fields. Davis-Stirling compliance.

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `candidate_ids` | `SelectMultipleField` | DataRequired | Choices populated dynamically from election candidates |
| `password` | `PasswordField` | DataRequired | Re-authentication for ballot casting |

**`cove/governance/proceeding_forms.py`**

### `ProceedingForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `title` | `StringField` | DataRequired, Length(5-500) | |
| `description` | `TextAreaField` | DataRequired, Length(min=20) | |
| `proceeding_type` | `SelectField` | DataRequired | Choices: `city_planning`, `coastal_commission`, `legal_challenge`, `state_legislature`, `land_acquisition` |
| `external_reference` | `StringField` | Optional, Length(max=255) | Case/permit number |
| `filing_date` | `DateField` | Optional | |

### `ProceedingStatusForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `status` | `SelectField` | DataRequired | Choices: `monitoring`, `active`, `resolved`, `archived` |

### `ProceedingEntryForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `title` | `StringField` | DataRequired, Length(5-500) | |
| `description` | `TextAreaField` | DataRequired, Length(min=10) | |
| `entry_type` | `SelectField` | DataRequired | Choices: `filing`, `hearing`, `decision`, `correspondence`, `update`, `evidence` |
| `entry_date` | `DateField` | DataRequired | |
| `source` | `StringField` | Optional, Length(max=255) | |
| `document_url` | `StringField` | Optional, Length(max=500) | |

---

## Models Used

**Proposal** (`proposals`):
- `type`: `resolution`, `bylaw_amendment`, `ccr_amendment`, `election`, `operating_rule`, `special_assessment`, `director_removal`
- `status`: `draft -> noticed -> open -> closed -> certified`; also `petitioned`
- `threshold`, `quorum_required`, `requires_secret_ballot`, `notice_period_days`, `ballot_period_days` — set at creation from bylaws config
- `yes_count`, `no_count`, `abstain_count` — atomically incremented; `yes_count` repurposed as total ballots cast for elections
- `total_votes` property: `yes + no + abstain`
- `passed` property: computes pass/fail on certified proposals (abstains excluded from threshold calc)
- `embedding`: `Vector(1024)` — for semantic search via cosine distance

**Ballot** (`ballots`) — NO `member_id`:
- `vote`: `yes`, `no`, `abstain`, or `election` (marker for election ballots)
- `method`: `electronic`, `paper`, `in_person`
- `chain_hash`: reserved for blockchain anchoring

**BallotEnvelope** (`ballot_envelopes`) — PostgreSQL RLS sealed:
- Links `ballot_id` -> `member_id` -> `proposal_id`
- Unique constraint: one vote per member per proposal
- Application layer only does EXISTS checks; never SELECTs content
- Only `inspector` role can SELECT via RLS

**Election** (`elections`):
- `seats` (default 5, WPBCA), `term_years` (default 1, S8.2)
- `is_reconvened`, `reconvened_from_id` — AB 2460 support
- `acclamation_eligible`, `acclamation_declared` — AB 502 support
- `can_declare_acclamation` property: `len(active_candidates) <= seats`

**Candidate** (`candidates`):
- `vote_count` — denormalized; atomically incremented on ballot cast
- `status`: `nominated`, `accepted`, `withdrawn`, `elected`, `defeated`
- `is_write_in` flag
- `member_id` nullable (candidates can be non-members)

**ElectionChoice** (`election_choices`) — NO `member_id`:
- Links anonymous `ballot_id` to `candidate_id`; one row per selection
- Unique constraint: one choice per candidate per ballot

**Proceeding** (`proceedings`):
- `proceeding_type`: `city_planning`, `coastal_commission`, `legal_challenge`, `state_legislature`, `land_acquisition`
- `status`: `monitoring`, `active`, `resolved`, `archived`
- `parcel_id` nullable — proceedings may be org-wide, not lot-specific
- `external_reference` — case/permit number

**ProceedingEntry** (`proceeding_entries`):
- `entry_type`: `filing`, `hearing`, `decision`, `correspondence`, `update`, `evidence`
- `entry_date`, `source`, `document_url`

---

## Services

**`cove/governance/services.py`**

| Function | What it does |
|----------|-------------|
| `create_proposal(org_id, created_by, title, description, proposal_type)` | Creates Proposal with bylaws-config defaults; audits |
| `get_proposal(proposal_id)` | Fetch by ID |
| `list_proposals(org_id, status=None)` | Filter by status, most recent first |
| `search_proposals_semantic(org_id, query, limit=10)` | Semantic search over proposals using `Vector(1024)` embedding and cosine distance (`<=>` operator). Calls `generate_embedding()` on the query, orders by similarity. Returns list of `Proposal` objects |
| `transition_proposal(proposal_id, actor_id)` | Advances status per `VALID_TRANSITIONS`; timestamps each stage; audits |
| `has_voted(member_id, proposal_id)` | EXISTS check on `ballot_envelopes` only |
| `cast_vote(proposal_id, member, vote, password, ip_address)` | Validates eligibility, re-auths password, creates Ballot + BallotEnvelope + atomic count increment; audits action only (not vote content) |
| `get_eligible_voter_count(org_id)` | Count active members with `voting_weight > 0` |
| `check_quorum(proposal, eligible_count)` | Returns quorum dict; secret ballot proposals always return `quorum_met=True` (S5.9) |
| `determine_result(proposal, quorum)` | Pass/fail: `yes / (yes+no) >= threshold`; abstains excluded |
| `get_results(proposal_id)` | Assembles full results dict for template |
| `get_proposal_type_defaults(proposal_type)` | Reads bylaws JSON via `bylaws_config`; falls back to hardcoded `PROPOSAL_TYPE_DEFAULTS` |

**`cove/governance/election_services.py`**

| Function | What it does |
|----------|-------------|
| `create_election(org_id, created_by, title, description, seats, ...)` | Creates `election` type Proposal + Election record |
| `add_candidate(election_id, name, nominated_by_id, ...)` | Adds Candidate; updates `acclamation_eligible`; audits |
| `withdraw_candidate(candidate_id, actor_id)` | Sets `status="withdrawn"`; re-checks acclamation |
| `check_acclamation(election_id)` | Returns dict; `eligible=True` if `active_candidates <= seats` |
| `declare_acclamation(election_id, actor_id)` | Marks all active candidates elected; fast-tracks proposal to `certified` (AB 502) |
| `cast_election_vote(proposal_id, member, candidate_ids, password, ip_address)` | Validates selections <= seats, re-auths, creates Ballot + ElectionChoices + BallotEnvelope; atomically increments candidate `vote_count` |
| `tally_election(election_id)` | Ranks by `vote_count` from `candidates` table only; detects ties |
| `_detect_ties(ranked, seats)` | Finds candidates straddling the seat cutoff at the same vote count |
| `resolve_tie(election_id, tied_candidate_ids, actor_id)` | `random.choice` tie-break (S8.13 coin flip); audits with all candidates and winner |
| `certify_election(election_id, actor_id)` | Marks winners `elected`, losers `defeated`; refuses if ties unresolved |
| `create_reconvened_election(original_election_id, ...)` | Creates new Election with `is_reconvened=True`, 20% quorum (AB 2460); carries over non-withdrawn candidates |
| `get_reconvened_quorum(election, eligible_count)` | Returns quorum dict; reconvened: 20% threshold |

**`cove/governance/proceeding_services.py`**

| Function | What it does |
|----------|-------------|
| `create_proceeding(org_id, created_by, title, description, proceeding_type, ...)` | Creates Proceeding with `status="monitoring"`; audits |
| `list_proceedings(org_id, proceeding_type=None, status=None, parcel_id=None)` | Filtered list, ordered by `updated_at DESC` |
| `update_proceeding_status(proceeding_id, status, actor_id)` | Validates against `PROCEEDING_STATUSES`; audits transition |
| `add_entry(proceeding_id, created_by, title, description, entry_type, ...)` | Creates ProceedingEntry; bumps `proceeding.updated_at`; audits |
| `list_entries(proceeding_id)` | Ordered by `entry_date ASC` (chronological timeline) |
| `generate_evidence_summary(proceeding_id)` | Returns proceeding + entries + linked proposals (if `parcel_id` set) |

**`cove/governance/bylaws_config.py`**

Loads `data/wpbca-bylaws-config.json` with `@lru_cache`. Exposes: `get_proposal_defaults`, `get_quorum_threshold`, `is_electronic_eligible`, `get_notice_periods`, `get_assessment_limits`, `get_legislative_info`.

---

## Templates

Templates use a **subdirectory structure** under `governance/`:

### Proposals

| Template | Description |
|----------|-------------|
| `governance/proposals.html` | Tabbed list: open, noticed, drafts (board), closed, certified |
| `governance/create_proposal.html` | Proposal creation form with type selector |
| `governance/proposal_detail.html` | Status, description, quorum gauge, vote/transition actions |
| `governance/ballot.html` | Yes/No/Abstain form with password re-auth field |
| `governance/vote_confirmed.html` | Success page after casting vote |
| `governance/results.html` | Vote counts, threshold, pass/fail verdict |
| `governance/_proposal_card.html` | Reusable proposal card component |
| `governance/_status_badge.html` | Reusable status badge component |

### Elections (`governance/elections/` subdirectory)

| Template | Description |
|----------|-------------|
| `governance/elections/index.html` | Election list |
| `governance/elections/create.html` | New election form (title, description, seats, term, nomination dates) |
| `governance/elections/detail.html` | Candidates, acclamation notice, reconvened quorum, board actions |
| `governance/elections/nominate.html` | Add candidate form (any member can access) |
| `governance/elections/ballot.html` | Multi-select candidate ballot with password re-auth |
| `governance/elections/ballot_confirmed.html` | Success page after casting election ballot |
| `governance/elections/results.html` | Ranked candidates, winners, ties |

### Proceedings (`governance/proceedings/` subdirectory)

| Template | Description |
|----------|-------------|
| `governance/proceedings/index.html` | Filtered proceedings list |
| `governance/proceedings/create.html` | New proceeding form |
| `governance/proceedings/detail.html` | Proceeding info + chronological timeline |
| `governance/proceedings/add_entry.html` | Add timeline entry form |
| `governance/proceedings/evidence.html` | Evidence summary with linked proposals |

---

## Davis-Stirling Compliance

| Rule | Implementation |
|------|---------------|
| Secret ballot (S5.9, AB 2159) | `Ballot` has no `member_id`; `BallotEnvelope` holds voter link; PostgreSQL RLS restricts envelope SELECT to `inspector` role |
| No quorum for secret ballot (S5.9) | `check_quorum` returns `quorum_met=True` unconditionally when `requires_secret_ballot=True` |
| 1/2 quorum for assessments (S6.6) | `special_assessment` type sets `quorum_required=0.50` in bylaws config |
| 1/3 quorum for general business (S6.6) | `resolution` type sets `quorum_required=0.33` |
| 67% supermajority for CC&R (S4275) | `ccr_amendment` type sets `threshold=0.67` |
| Plurality for elections | `election` type sets `threshold=0.00`; `determine_result` returns `type="election"` |
| One vote per lot (S5.2) | Combined lot members have `voting_weight=0`; eligibility check and `cast_vote` both enforce |
| Election by acclamation (AB 502) | `declare_acclamation` fast-tracks to certified when candidates <= seats |
| Reconvened quorum 20% (AB 2460) | `create_reconvened_election` sets `is_reconvened=True`; `get_reconvened_quorum` applies 20% threshold |
| Tie-break by coin flip (S8.13) | `resolve_tie` uses `random.choice`; full audit trail with all candidates and winner |
| Audit trail | Every vote, transition, and certification writes to `audit_log`; vote content never logged |
| Electronic ballots (AB 2159) | `is_electronic_eligible` in bylaws config; `special_assessment` excluded |
