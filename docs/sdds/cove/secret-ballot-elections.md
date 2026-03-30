# Secret Ballot Elections

> **Status:** Complete — written from code
> **Namespace:** cove
> **Last updated:** 2026-03-30
> **Code location:** `Cove/cove/governance/election_services.py`, `Cove/cove/governance/election_routes.py`, `Cove/cove/governance/election_forms.py`, `Cove/cove/models/election.py`, `Cove/cove/models/governance.py`, `Cove/cove/governance/quorum.py`

---

## 1. Overview

The Secret Ballot Elections service manages board director elections for HOA organizations under the California Davis-Stirling Common Interest Development Act. It handles the full election lifecycle: creation, nomination, optional acclamation declaration, electronic secret-ballot voting, tallying, tie resolution, and certification.

Elections are a specialized form of governance proposal. Every election is backed by a `Proposal` record with `type='election'`, extended by an `Election` record that carries election-specific data (seats, term, nomination window, acclamation flags, reconvene linkage). Candidate management, vote casting, and results tallying all operate on top of this two-record foundation.

The defining constraint of the entire system is secret ballot separation: a voter's identity must never be linkable to their candidate selections in normal operations. This is enforced by a two-table design (anonymous `Ballot` + identified `BallotEnvelope`) combined with PostgreSQL Row-Level Security that grants `SELECT` on envelopes to the inspector role only.

### Legislative basis

| Law | Effect |
|-----|--------|
| Davis-Stirling Civil Code §5100–5145 | Secret ballot mandate for director elections |
| WPBCA Bylaws §8.12 | Two-envelope ballot system (digital equivalent) |
| WPBCA Bylaws §8.13 | Tiebreaker by coin flip |
| WPBCA Bylaws §8.14 | Inspector of elections: 1 or 3 independent persons |
| WPBCA Bylaws §8.2 | 5 directors, 1-year terms, must reside 35%+ of year |
| AB 502 (2022) | Election by acclamation when candidates ≤ seats |
| AB 2159 (2024, eff. Jan 1 2025) | Electronic secret ballot voting authorized |
| AB 2460 (2024, eff. Jan 1 2025) | Reconvened election quorum reduced to 20% |

---

## 2. Architecture

### Component Diagram

```
  Browser / Member
       |
       | HTTPS (login_required)
       v
  election_routes.py  (Blueprint: election_bp, prefix /vote/election)
       |
       | delegates all business logic
       v
  election_services.py
       |
       +-- create_election()         → governance/services.create_proposal() + Election
       +-- add_candidate()           → Candidate + _update_acclamation_status()
       +-- withdraw_candidate()      → Candidate.status = 'withdrawn'
       +-- check_acclamation()       → read-only AB 502 check
       +-- declare_acclamation()     → fast-path certify (no ballot)
       +-- cast_election_vote()      → atomic: Ballot + ElectionChoice(s) + BallotEnvelope
       +-- tally_election()          → reads Candidate.vote_count (denormalized)
       +-- resolve_tie()             → random.choice() + audit
       +-- certify_election()        → marks winners/losers, certifies Proposal
       +-- create_reconvened_election() → clones election at 20% quorum (AB 2460)
       |
       v
  PostgreSQL (cove database)
       |
       +-- proposals                 (Proposal — base record, type='election')
       +-- elections                 (Election — election-specific data)
       +-- candidates                (Candidate — nominees, vote_count denormalized)
       +-- election_choices          (ElectionChoice — anonymous: ballot → candidate)
       +-- ballots                   (Ballot — anonymous inner envelope)
       +-- ballot_envelopes          (BallotEnvelope — identified outer envelope, RLS)
       +-- audit_log                 (all election events)

  quorum.py  (QuorumCalculator — shared with governance engine)
       |
       +-- calculate("election")    → quorum_threshold=0.0, secret ballot, no quorum (§5.9)
       +-- calculate("election", reconvened=True)  → 20% quorum (AB 2460)
       +-- check_acclamation()      → AcclamationResult (AB 502)
       +-- wpbca-bylaws-config.json → all thresholds sourced from config, not hardcoded
```

### Request / Data Flow

**Creating an election (board member):**

1. `GET /vote/election/create` — renders `ElectionForm`
2. `POST /vote/election/create` — `create_election()`:
   - Calls `governance/services.create_proposal()` with `type='election'`
   - Creates linked `Election` record with seats, term, nomination window
   - Commits; redirects to detail view

**Nominating a candidate (any authenticated member):**

1. `POST /vote/election/<proposal_id>/candidates/add` — `add_candidate()`:
   - Validates election is not closed/certified
   - Checks for duplicate nomination (by `member_id` if a member, by name otherwise)
   - Creates `Candidate` with status `nominated`
   - Calls `_update_acclamation_status()` to recompute `Election.acclamation_eligible`
   - Writes audit record

**Declaring acclamation (board, AB 502):**

1. `POST /vote/election/<proposal_id>/acclamation` — `declare_acclamation()`:
   - Validates `can_declare_acclamation` (active candidates ≤ seats)
   - Sets all active candidates to `elected`
   - Fast-tracks `Proposal.status` to `certified`
   - No ballots are created; no ballot period is opened

**Casting an election ballot (authenticated member):**

1. `GET /vote/election/<proposal_id>/ballot` — renders `ElectionBallotForm`
   - Form contains `candidate_ids` (checkboxes, populated from election data) and `password` only
   - No member identity fields on the form
2. `POST /vote/election/<proposal_id>/ballot` — `cast_election_vote()` in one atomic transaction:
   1. Validate proposal is open and type is `election`
   2. Validate candidate selections (count ≤ seats, no duplicates, all active)
   3. Validate member eligibility (`voting_weight > 0`, `membership_status == 'active'`)
   4. Re-authenticate via password hash check
   5. Check for duplicate vote via `BallotEnvelope` (`has_voted()`)
   6. `db.session.flush()` after creating `Ballot` to obtain `ballot.id`
   7. Create one `ElectionChoice` per selected candidate (links to `ballot.id`, not `member.id`)
   8. Atomically increment `Candidate.vote_count` for each selected candidate
   9. Atomically increment `Proposal.yes_count` (repurposed as total ballots cast)
   10. Create `BallotEnvelope` linking `ballot.id` → `member.id`
   11. Write audit record (records that member voted; never records which candidates)
   12. `db.session.commit()`
3. Returns anonymous `Ballot` to the route; route renders `ballot_confirmed.html`

**Tallying results (after election closes):**

1. `GET /vote/election/<proposal_id>/results` — `tally_election()`:
   - Reads `Candidate.vote_count` (denormalized — never joins to `ballot_envelopes`)
   - Ranks candidates by vote count descending
   - Detects ties at the last available seat boundary
   - Computes turnout from `Proposal.yes_count` and `get_eligible_voter_count()`

**Certifying (board, after any tie resolution):**

1. `POST /vote/election/<proposal_id>/certify` — `certify_election()`:
   - Blocks if unresolved ties remain
   - Marks winners `elected`, losers `defeated`
   - Sets `Proposal.status = 'certified'` and `Proposal.certified_at`

### Key Design Decisions

**Two-record election structure.** Elections sit on top of the governance engine's `Proposal` model rather than being a standalone table. This gives elections access to the proposal lifecycle (draft → noticed → open → closed → certified), the audit infrastructure, and the quorum calculator without duplication. The `Election` record carries only what proposals don't have: seats, term, nomination window, acclamation state, and reconvene linkage.

**Denormalized vote_count on Candidate.** Vote tallying reads `Candidate.vote_count`, which is atomically incremented at vote-cast time using a `table.update().values({col: col + 1})` statement. This avoids a full `COUNT(*)` scan over `election_choices` on every tally request and means the tally operation never needs to touch `ballot_envelopes`. The trade-off is that vote counts are immutable once committed — there is no delete-vote path.

**yes_count repurposed as total_ballots_cast for elections.** `Proposal.yes_count` is incremented once per ballot cast in an election, regardless of which candidates were selected. The field name is a governance-engine artifact; in election context it serves as the total ballot counter used for turnout calculation.

**Inner envelope / outer envelope separation.** See Section 7 for full detail. The short version: `Ballot` is the inner envelope (content, anonymous), `BallotEnvelope` is the outer envelope (identity, RLS-sealed). Normal service code — including `tally_election()` — never touches `ballot_envelopes`. Only the inspector role, via a dedicated query path, can open the outer envelope.

---

## 3. Data Model

### Election

```python
class Election(db.Model):
    __tablename__ = "elections"

    id: Mapped[str]                          # UUID primary key (String(36))
    proposal_id: Mapped[str]                 # FK → proposals.id (unique — 1:1)
    seats: Mapped[int]                       # number of board seats up for election
    term_years: Mapped[int]                  # director term in years (WPBCA default: 1)
    nomination_opens_at: Mapped[datetime | None]
    nomination_closes_at: Mapped[datetime | None]
    is_reconvened: Mapped[bool]              # True if created via AB 2460 reconvene path
    reconvened_from_id: Mapped[str | None]   # FK → elections.id (self-referential)
    acclamation_eligible: Mapped[bool]       # recomputed on every add/withdraw
    acclamation_declared: Mapped[bool]       # True once declare_acclamation() is called
    created_at: Mapped[datetime]

    # Relationships
    proposal: Mapped["Proposal"]             # backref "election" on Proposal
    candidates: Mapped[list["Candidate"]]    # ordered by vote_count DESC
    reconvened_from: Mapped["Election | None"]

    # Properties
    active_candidates -> list[Candidate]     # status != 'withdrawn'
    can_declare_acclamation -> bool          # len(active_candidates) <= seats
```

### Candidate

```python
class Candidate(db.Model):
    __tablename__ = "candidates"

    id: Mapped[str]                          # UUID primary key
    election_id: Mapped[str]                 # FK → elections.id
    member_id: Mapped[str | None]            # FK → members.id (null for non-member nominees)
    name: Mapped[str]                        # String(255) — full legal name
    statement: Mapped[str | None]            # Text — optional candidacy statement (max 2,000 chars)
    nominated_by_id: Mapped[str]             # FK → members.id — who submitted nomination
    is_write_in: Mapped[bool]                # write-in vs. formal nomination
    vote_count: Mapped[int]                  # denormalized — incremented atomically at vote time
    status: Mapped[str]                      # nominated | accepted | withdrawn | elected | defeated
    created_at: Mapped[datetime]

    # Relationships
    election: Mapped["Election"]
    member: Mapped["Member | None"]          # foreign_keys=[member_id]
    nominated_by: Mapped["Member"]           # foreign_keys=[nominated_by_id]
```

### ElectionChoice

```python
class ElectionChoice(db.Model):
    """One row per candidate selected on a ballot. Links ballot → candidate. No member_id."""
    __tablename__ = "election_choices"
    __table_args__ = (
        UniqueConstraint("ballot_id", "candidate_id", name="uq_one_choice_per_candidate_per_ballot"),
    )

    id: Mapped[str]                          # UUID primary key
    ballot_id: Mapped[str]                   # FK → ballots.id
    candidate_id: Mapped[str]                # FK → candidates.id
    created_at: Mapped[datetime]

    # Relationships
    ballot: Mapped["Ballot"]
    candidate: Mapped["Candidate"]
```

### Ballot (shared from governance.py — inner envelope)

```python
class Ballot(db.Model):
    """Vote content only — NO member_id column. Ever."""
    __tablename__ = "ballots"

    id: Mapped[str]                          # UUID primary key
    proposal_id: Mapped[str]                 # FK → proposals.id
    vote: Mapped[str]                        # 'election' (marker) for election ballots
    method: Mapped[str]                      # electronic | paper | in_person
    cast_at: Mapped[datetime]
    chain_hash: Mapped[str | None]           # SHA-256 hash for blockchain anchoring
```

### BallotEnvelope (shared from governance.py — outer envelope, RLS-sealed)

```python
class BallotEnvelope(db.Model):
    """Sealed link between voter and ballot — inspector access only via PostgreSQL RLS."""
    __tablename__ = "ballot_envelopes"
    __table_args__ = (
        UniqueConstraint("member_id", "proposal_id", name="uq_one_vote_per_member_per_proposal"),
    )

    id: Mapped[str]                          # UUID primary key
    ballot_id: Mapped[str]                   # FK → ballots.id
    member_id: Mapped[str]                   # FK → members.id
    proposal_id: Mapped[str]                 # FK → proposals.id
    issued_at: Mapped[datetime]
    sealed_at: Mapped[datetime | None]       # set when ballot is cast
```

### Proposal (shared from governance.py — base record)

For elections, the relevant `Proposal` fields are:

| Field | Election usage |
|-------|---------------|
| `type` | always `'election'` |
| `status` | lifecycle: `draft → noticed → open → closed → certified` |
| `requires_secret_ballot` | always `True` for elections |
| `yes_count` | repurposed: total ballots cast (not yes votes) |
| `no_count` | unused for elections |
| `abstain_count` | unused for elections |
| `certified_at` | set on `certify_election()` or `declare_acclamation()` |
| `embedding` | `Vector(1024)` — available for semantic search |

### Table relationships (election domain)

```
proposals (1) ——— (1) elections
                       |
                   (1..N) candidates
                       |
election_choices (N) ——— (1) candidates
election_choices (N) ——— (1) ballots ——— (1) ballot_envelopes
                                               |
                                           members (outer envelope, RLS)
```

---

## 4. Interfaces

### HTTP Routes (Blueprint: `election_bp`, prefix `/vote/election`)

All routes require `@login_required`. Tenant isolation is enforced in each route handler by comparing `election.proposal.organization_id` to `current_user.organization_id`.

| Method | Path | Role required | Purpose |
|--------|------|--------------|---------|
| GET | `/` | any member | List all elections for the organization |
| GET / POST | `/create` | board (`is_board`) | Create a new election |
| GET | `/<proposal_id>` | any member | Election detail: candidates, acclamation status, voted flag |
| GET / POST | `/<proposal_id>/candidates/add` | any member | Nominate a candidate |
| POST | `/<proposal_id>/candidates/<candidate_id>/withdraw` | board | Withdraw a candidate |
| POST | `/<proposal_id>/acclamation` | board | Declare election by acclamation (AB 502) |
| GET / POST | `/<proposal_id>/ballot` | any member | Display and submit secret ballot |
| GET | `/<proposal_id>/results` | any member | View tally (only when `status` in `closed`, `certified`) |
| POST | `/<proposal_id>/certify` | board | Certify results and declare winners |

Routes are thin wrappers. All business logic is in `election_services.py`. Routes catch `ValueError` from the service layer and surface them as `flash()` messages with redirect; they do not catch unexpected exceptions (those bubble to the Flask error handler).

### WTForms

**ElectionForm** — create election

| Field | Type | Validators |
|-------|------|-----------|
| `title` | `StringField` | `DataRequired`, `Length(5, 500)` |
| `description` | `TextAreaField` | `DataRequired`, `Length(min=20)` |
| `seats` | `IntegerField` | `DataRequired`, `NumberRange(1, 20)` |
| `term_years` | `IntegerField` | `DataRequired`, `NumberRange(1, 5)` |
| `nomination_opens_at` | `DateField` | `Optional` |
| `nomination_closes_at` | `DateField` | `Optional` |

**CandidateForm** — nominate a candidate

| Field | Type | Validators |
|-------|------|-----------|
| `name` | `StringField` | `DataRequired`, `Length(2, 255)` |
| `statement` | `TextAreaField` | `Optional`, `Length(max=2000)` |
| `is_write_in` | `BooleanField` | — |

**ElectionBallotForm** — secret ballot (Davis-Stirling compliant)

| Field | Type | Validators | Notes |
|-------|------|-----------|-------|
| `candidate_ids` | `SelectMultipleField` | `DataRequired` | Choices populated from election candidates at request time; IDs only |
| `password` | `PasswordField` | `DataRequired` | Re-authentication; value never persisted |

The `ElectionBallotForm` intentionally contains no member identification fields. Voter identity is established by the active Flask-Login session, not by form input.

---

## 5. Service Layer

All public functions are in `Cove/cove/governance/election_services.py`. The module also imports from `cove/governance/services.py` for shared primitives (`create_proposal`, `get_eligible_voter_count`, `has_voted`, `_audit`).

### create_election

```python
def create_election(
    org_id: str,
    created_by: str,
    title: str,
    description: str,
    seats: int = 5,
    term_years: int = 1,
    nomination_opens_at: datetime | None = None,
    nomination_closes_at: datetime | None = None,
) -> Election
```

Creates a `Proposal` (type `'election'`) via `create_proposal()`, then creates the linked `Election` record. Raises `ValueError` if `seats < 1`.

### add_candidate

```python
def add_candidate(
    election_id: str,
    name: str,
    nominated_by_id: str,
    member_id: str | None = None,
    statement: str | None = None,
    is_write_in: bool = False,
) -> Candidate
```

Creates a `Candidate`. Guards: election must not be closed/certified; if `member_id` is provided, member must not already have a non-withdrawn candidacy in this election. Calls `_update_acclamation_status()` after adding. Writes audit record with `candidate_name` and `is_write_in` flag. Strips whitespace from name and statement.

### withdraw_candidate

```python
def withdraw_candidate(candidate_id: str, actor_id: str) -> Candidate
```

Sets `Candidate.status = 'withdrawn'`. Calls `_update_acclamation_status()` to recompute whether acclamation is now eligible. Writes audit record.

### check_acclamation

```python
def check_acclamation(election_id: str) -> dict
```

Read-only. Returns:

```python
{
    "eligible": bool,           # True if active_candidates <= seats
    "seats": int,
    "active_candidates": int,
    "candidates": [{"id": str, "name": str}, ...],
    "note": str | None,         # AB 502 message if eligible, else None
}
```

### declare_acclamation

```python
def declare_acclamation(election_id: str, actor_id: str) -> Election
```

AB 502 fast-path. Validates `can_declare_acclamation`. Marks all active candidates `elected`. Sets `Election.acclamation_declared = True`. Sets `Proposal.status = 'certified'` and `Proposal.certified_at`. No ballot period is opened. Writes audit record listing elected names.

### cast_election_vote

```python
def cast_election_vote(
    proposal_id: str,
    member: Member,
    candidate_ids: list[str],
    password: str,
    ip_address: str | None = None,
) -> Ballot
```

The core voting transaction. See Section 2 (Request / Data Flow) for the full atomic sequence. Returns the anonymous `Ballot`. The `member` object is used for eligibility and re-authentication checks; it is not stored in the ballot or its choices.

Raises `ValueError` for all validation failures. These messages are user-facing; the route renders them via `flash()`.

Validation sequence:

1. Proposal exists and `type == 'election'`
2. `Proposal.status == 'open'`
3. `candidate_ids` is non-empty
4. `len(candidate_ids) <= election.seats`
5. No duplicate candidate IDs in selection
6. All selected candidates exist, belong to this election, and are not withdrawn
7. `member.voting_weight > 0` (combined lots — §5.2)
8. `member.membership_status == 'active'`
9. Password re-authentication via `check_password_hash`
10. `has_voted(member.id, proposal_id)` returns `False`

### tally_election

```python
def tally_election(election_id: str) -> dict
```

Returns:

```python
{
    "election": Election,
    "ranked": list[Candidate],      # all non-withdrawn, sorted by vote_count DESC
    "winners": list[Candidate],     # top N by seats
    "ties": list[Candidate],        # candidates tied at the last-seat boundary
    "seats": int,
    "total_ballots": int,           # Proposal.yes_count (repurposed)
    "eligible_voters": int,
    "turnout": float,               # 0.0–1.0, 4 decimal places
}
```

Reads only `Candidate.vote_count`. Never queries `ballot_envelopes`.

### resolve_tie

```python
def resolve_tie(
    election_id: str,
    tied_candidate_ids: list[str],
    actor_id: str,
) -> Candidate
```

Implements bylaws §8.13 tiebreaker: random selection via `random.choice()`. Requires at least 2 candidates. Writes a detailed audit record including all tied candidates, the winning ID, winning name, and the bylaw citation. Returns the winning `Candidate` (does not update any statuses — `certify_election` handles that).

### certify_election

```python
def certify_election(election_id: str, actor_id: str) -> Election
```

Blocks if `tally["ties"]` is non-empty. Requires `Proposal.status in ('closed', 'certified')`. Marks top-N candidates `elected`, remaining `defeated` (skipping withdrawn). Sets `Proposal.status = 'certified'` and `Proposal.certified_at`. Writes audit record.

### create_reconvened_election

```python
def create_reconvened_election(
    original_election_id: str,
    created_by: str,
    title: str | None = None,
    description: str | None = None,
) -> Election
```

AB 2460 path. Creates a new election record linked to the original via `reconvened_from_id`. Sets `is_reconvened = True`. Carries over all non-withdrawn candidates by creating new `Candidate` records. Title defaults to `"Reconvened: {original.title}"`.

### get_reconvened_quorum

```python
def get_reconvened_quorum(election: Election, eligible_count: int) -> dict
```

Returns quorum status for the election. For non-reconvened elections, always returns `quorum_met=True` with a note citing §5.9 (no quorum required for secret ballot). For reconvened elections, applies AB 2460: `required = max(1, ceil(eligible * 0.20))`. Returns `quorum_met`, `required`, `actual`, `eligible`, and a note.

### Internal helpers

| Function | Purpose |
|----------|---------|
| `_update_acclamation_status(election)` | Sets `election.acclamation_eligible` based on active candidate count vs. seats. Called on every add/withdraw. |
| `_detect_ties(ranked, seats)` | Returns the list of candidates tied at the last-seat vote count, if and only if some are inside the cutoff and some are outside. |

---

## 6. Configuration

Elections inherit their proposal defaults from `cove/governance/services.py`. The relevant defaults for `type='election'`:

| Field | Value | Source |
|-------|-------|--------|
| `threshold` | plurality (winner by vote rank, not percentage) | governance services |
| `quorum_required` | 0.0 | bylaws §5.9 — no quorum for secret ballot |
| `requires_secret_ballot` | `True` | hardcoded for elections |
| `notice_period_days` | 28 | `wpbca-bylaws-config.json` |
| `ballot_period_days` | 30 | `wpbca-bylaws-config.json` |

`QuorumCalculator` reads all thresholds from `Cove/cove/governance/wpbca-bylaws-config.json`. No quorum values are hardcoded in Python. The config file is a protected file — changes require explicit approval.

WPBCA-specific defaults used at `Election` creation:

| Field | Default | Bylaw |
|-------|---------|-------|
| `seats` | 5 | §8.2 |
| `term_years` | 1 | §8.2 |

---

## 7. Security & Compliance

### Two-Envelope Digital System

The Davis-Stirling Act and WPBCA §8.12 require a two-envelope ballot process: the inner envelope contains the vote (anonymous), the outer envelope contains the voter's identity (sealed, handed to inspector). This system is implemented digitally as follows:

**Inner envelope — `Ballot` table:**
- Contains `proposal_id`, `vote` (set to `'election'` as a marker), `method`, and `cast_at`
- Has no `member_id` column
- Is what gets counted. `ballot.id` is the ballot receipt identifier
- One `ElectionChoice` row per candidate selected, linked to `ballot.id`

**Outer envelope — `BallotEnvelope` table:**
- Contains `ballot_id`, `member_id`, `proposal_id`, `sealed_at`
- PostgreSQL Row-Level Security restricts `SELECT` to the `inspector` role
- The `growdirect` application user (used by Flask) does not have `SELECT` on `ballot_envelopes` in production
- Flask-Login sessions for inspector-role members are the only normal path to envelope data

### RLS Enforcement Rules

These rules are non-negotiable. Any violation breaks Davis-Stirling compliance and invalidates the election:

1. `tally_election()` reads ONLY from `candidates.vote_count`. It does not query `ballots`, `election_choices`, or `ballot_envelopes`.
2. Governance services (`cove/governance/services.py`) never JOIN `ballots` to `ballot_envelopes`.
3. The `ElectionBallotForm` contains no member identity fields. Member identity is established exclusively via the Flask-Login session.
4. The audit record for `election_vote.cast` records WHO voted and the method. It never records which candidates were selected.
5. The `has_voted()` check queries `ballot_envelopes` by `member_id + proposal_id`. This is the only normal-path use of `ballot_envelopes` in the election service — and it returns a boolean only, not ballot content.

### AB 502 — Election by Acclamation

When active candidates ≤ available seats, the election may be declared by acclamation without a ballot period. This is a legitimate AB 502 (2022) path, not a bypass of secret ballot requirements — acclamation applies only when there is no contest to keep secret. The `declare_acclamation()` function fast-tracks the proposal to `certified` status.

### AB 2159 — Electronic Secret Ballot (eff. Jan 1, 2025)

Electronic voting is authorized for secret ballot elections. The `method` field on `Ballot` is set to `'electronic'` for web-submitted votes. The form enforces password re-authentication (identity confirmation without storing identity alongside the vote). Paper ballot support is modeled (`method='paper'`) but import tooling is not yet implemented.

### AB 2460 — Reconvened Election Quorum (eff. Jan 1, 2025)

If an election fails (or a board determines reconvening is needed), `create_reconvened_election()` creates a new election with `is_reconvened=True`. The `get_reconvened_quorum()` function applies the 20% threshold for these elections. Note that standard (non-reconvened) elections have NO quorum requirement per §5.9 — the reconvened path is only needed when a prior quorum-gated proceeding failed.

### Password Re-authentication

Before a ballot is accepted, `cast_election_vote()` calls `check_password_hash(member.password_hash, password)` from werkzeug. This confirms the submitter controls the account without creating a new session or modifying any session state. The password value is never written to the database at this point.

### Member Eligibility

Two eligibility conditions are enforced in `cast_election_vote()`:

- `member.voting_weight == 0`: combined lots (WPBCA §5.2 — two APNs share one vote). The member record with `voting_weight=0` exists for informational purposes but has no voting rights.
- `member.membership_status != 'active'`: suspended or inactive members cannot vote.

### Inspector Role

The `Member.is_inspector` property (role check, not a column) grants access to `ballot_envelopes` via RLS. Inspectors can confirm ballot receipt and validate that `ballot_envelopes` has the expected count for a given election, without being able to reconstruct which candidate any member voted for (since the inner/outer link is one-way via `ballot_id`, and choice data is on the anonymous inner side).

---

## 8. Error Handling

The service layer uses `ValueError` for all user-correctable validation failures. Messages are written to be user-facing. Routes catch `ValueError` and surface them via `flash(str(exc), "error")` followed by a redirect or re-render.

| Error condition | Message |
|----------------|---------|
| Election not found | `"Election not found"` |
| Candidate not found | `"Candidate not found"` |
| Seats < 1 | `"Election must have at least 1 seat"` |
| Add candidate to closed election | `"Cannot add candidates to a closed election"` |
| Duplicate candidate | `"{name} is already a candidate"` |
| Candidate already withdrawn | `"Candidate already withdrawn"` |
| Acclamation not eligible | `"Cannot declare acclamation — more candidates than seats"` |
| Proposal not found | `"Proposal not found"` |
| Not an election proposal | `"Not an election proposal"` |
| Voting not open | `"Voting is not open for this election"` |
| No candidates selected | `"Must select at least one candidate"` |
| Too many selections | `"Cannot select more than {seats} candidates"` |
| Duplicate candidate in selection | `"Duplicate candidate selections"` |
| Invalid or foreign candidate | `"Invalid candidate: {cid}"` |
| Candidate withdrawn (at vote time) | `"Candidate '{name}' has withdrawn"` |
| Combined lot — no voting weight | `"Combined lot — not eligible to vote (bylaw §5.2)"` |
| Inactive membership | `"Membership is not active"` |
| Password incorrect | `"Password incorrect — re-authentication failed"` |
| Already voted | `"You have already voted in this election"` |
| Election not closed for certification | `"Election must be closed before certification"` |
| Unresolved ties at certification | `"Unresolved ties — resolve before certifying"` |
| Fewer than 2 for tie resolution | `"Need at least 2 candidates to resolve a tie"` |
| Original election not found (reconvene) | `"Original election not found"` |

Routes guard against cross-organization access (`organization_id` comparison) and return `abort(403)`. Missing elections return `abort(404)`.

---

## 9. Testing

Tests live under `Cove/tests/` following the three-layer GrowDirect test standard.

### Unit tests (models and service logic)

- `Election.can_declare_acclamation` property with varying candidate/seat ratios
- `Election.active_candidates` filters withdrawn correctly
- `_update_acclamation_status()` recomputes `acclamation_eligible` after add and withdraw
- `_detect_ties()` with: no tie, exact fill (no tie), tie spanning the cutoff, all tied
- `check_acclamation()` returns correct `eligible` flag and note text
- `get_reconvened_quorum()` for reconvened vs. standard elections

### Integration tests (routes + database)

- Create election as board member; verify Proposal + Election records created
- Create election as non-board member; expect `403`
- Nominate candidate; verify `Candidate` row and audit log entry
- Nominate duplicate member; expect `ValueError`
- Withdraw candidate; verify status transition and acclamation recompute
- Declare acclamation when candidates ≤ seats; verify all candidates `elected`, proposal `certified`
- Declare acclamation when candidates > seats; expect `ValueError`
- `cast_election_vote()` happy path: verify atomic write of `Ballot`, `ElectionChoice` rows, `BallotEnvelope`, incremented `vote_count` on each candidate, incremented `Proposal.yes_count`
- Cast vote with wrong password; expect `ValueError`
- Cast vote when already voted (second attempt); expect `ValueError`
- Cast vote with `voting_weight == 0`; expect `ValueError`
- Cast vote selecting more than `seats` candidates; expect `ValueError`
- Cast vote on closed proposal; expect `ValueError`
- `tally_election()` returns correct ranking and turnout after votes cast
- `certify_election()` with no ties; verify winner/loser statuses and certified timestamp
- `certify_election()` with unresolved ties; expect `ValueError`
- `resolve_tie()` writes audit record with all required fields
- `create_reconvened_election()` carries over non-withdrawn candidates; sets `is_reconvened`

### Smoke tests

- `GET /vote/election/` returns 200 for authenticated member
- `GET /vote/election/<id>/ballot` for an open election returns 200
- `GET /vote/election/<id>/results` before close returns redirect
- Health check does not expose ballot data

### Critical invariant tests

These tests verify the secret ballot separation is maintained:

- `tally_election()` SQL does NOT reference `ballot_envelopes` table (inspect query plan or mock)
- `ElectionChoice` rows have no `member_id` column (schema inspection)
- `Ballot` rows have no `member_id` column
- Creating a `Ballot` never passes `member.id` to it

---

## 10. Dependencies

### Upstream

| Dependency | What it provides |
|-----------|-----------------|
| `cove/governance/services.py` | `create_proposal()`, `get_eligible_voter_count()`, `has_voted()`, `_audit()` |
| `cove/models/governance.py` | `Proposal`, `Ballot`, `BallotEnvelope` — shared with governance engine |
| `cove/governance/quorum.py` | `QuorumCalculator`, `AcclamationResult` — shared with governance engine |
| `cove/models/member.py` | `Member` — voter identity, eligibility, password hash |
| `cove/extensions.py` | `db` (SQLAlchemy session) |
| `werkzeug.security` | `check_password_hash` — password re-authentication |

### Downstream

No services depend on the election service layer. Election data is consumed by:

- Board dashboard (`cove/board/`) — election status summaries
- Member dashboard (`cove/member/`) — active elections, voted indicators
- Archive (`cove/archive/`) — certified election records for document chain of custody

### Shared Infrastructure

| Service | Usage |
|---------|-------|
| `growdirect_postgres` (cove DB) | All persistence |
| `growdirect_valkey` DB 1 | Session store (Flask-Login sessions gate ballot access) |
| PostgreSQL RLS | `ballot_envelopes` inspector-only access |
| `growdirect_ollama` | `Proposal.embedding` — semantic search on election descriptions (optional, degrades gracefully) |

---

## 11. Known Issues & Reconciliation

### Election code lives in `governance/`

Election services, routes, and forms are located in `Cove/cove/governance/` alongside the core governance engine (proposal services, quorum calculator, proceedings). The models live in `Cove/cove/models/election.py` as a separate file from `governance.py`.

This is intentional co-location, not a scope issue. Elections share:

- The `Proposal` base record and its lifecycle state machine
- The `Ballot` / `BallotEnvelope` two-envelope infrastructure
- The `QuorumCalculator` and `wpbca-bylaws-config.json`
- The `_audit()` primitive and the governance audit log
- The `has_voted()` duplicate-vote guard

Separating elections into their own top-level module would require duplicating or re-exporting all of these. The current structure reflects that elections are a specialized form of governance proposal, not a standalone domain.

### `yes_count` repurposed for election ballot count

`Proposal.yes_count` is incremented once per ballot cast in an election, regardless of candidate selections. In normal proposal voting, `yes_count` tallies explicit yes votes. For elections, it serves as `total_ballots_cast` because elections use plurality (vote-for-N) rather than yes/no framing. The field name is a governance-engine artifact. Code using this value for elections must apply this interpretation. `tally_election()` exposes it as `total_ballots` in the return dict to make the context explicit at call sites.

### `BallotEnvelope.issued_at` vs. `sealed_at` semantics

`issued_at` defaults to `datetime.utcnow` at row creation. `sealed_at` is set to `datetime.utcnow()` explicitly in `cast_election_vote()` at the moment the ballot is committed. In the current implementation these are always within milliseconds of each other (both set in the same transaction). The two fields exist to support a future paper ballot workflow where an envelope might be issued at one time and received/sealed later.

### UUID stored as `String(36)` throughout election models

All election models (`Election`, `Candidate`, `ElectionChoice`) store UUIDs as `String(36)` rather than the platform-standard native `Mapped[uuid.UUID]`. This is a historical holdover from early Cove development, documented in the Cove CLAUDE.md. The pattern is consistent within Cove and does not cause runtime issues, but should be flagged and migrated if these tables are ever meaningfully modified. Do not propagate `String(36)` UUID columns to new tables.

### `random.choice()` in `resolve_tie()`

The tie-resolution coinflip uses Python's `random.choice()` which is seeded from OS entropy (`os.urandom`) and is suitable for this purpose. It is not a cryptographically secure random but does not need to be — the audit record captures the full decision for inspector review. If a bylaw challenge arises, the audit log entry (`election.tiebreaker`) contains all tied candidates, the winning ID, and the bylaw citation.

### Paper ballot import not implemented

`Ballot.method` supports `'paper'` and `'in_person'` values. There is no current import path for paper ballots received by the inspector. When paper ballot support is added, it must write through the same `Ballot` + `BallotEnvelope` + `ElectionChoice` path used by electronic votes — no shortcut that bypasses the inner/outer envelope separation is acceptable.
