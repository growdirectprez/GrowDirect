# Secret Ballot Elections

> **Status:** Production-grade ops contract
> **Type:** App Service (Cove)
> **Namespace:** cove
> **Last updated:** 2026-04-13
> **Code location:** `Cove/cove/governance/election_services.py`, `Cove/cove/governance/election_routes.py`, `Cove/cove/governance/election_forms.py`, `Cove/cove/models/election.py`, `Cove/cove/models/governance.py`, `Cove/cove/governance/quorum.py`
> **Split companion:** [[docs/sdds/cove/ballot-security|Ballot Security]] — two-envelope system, RLS policies, ballot anonymity, chain hash

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Compliance|Compliance]] · **Operator role:** [[Canary/docs/profiles/ops/Legal|Legal]]

---

## Purpose

The Secret Ballot Elections service manages board director elections for HOA organizations under the California Davis-Stirling Common Interest Development Act. It handles the full election lifecycle: creation, nomination, optional acclamation declaration (AB 502), electronic secret-ballot voting, tallying, tie resolution, certification, and reconvened elections (AB 2460).

Elections are a specialized form of governance proposal. Every election is backed by a `Proposal` record with `type='election'`, extended by an `Election` record that carries election-specific data (seats, term, nomination window, acclamation flags, reconvene linkage). Candidate management, vote casting, and results tallying all operate on this two-record foundation.

The defining constraint of the entire system is secret ballot separation. See [[docs/sdds/cove/ballot-security|Ballot Security]] for the two-envelope architecture, PostgreSQL RLS policies, and chain hash integrity model.

### Legislative Basis

| Law | Effect |
|-----|--------|
| Davis-Stirling Civil Code SS5100-5145 | Secret ballot mandate for director elections |
| WPBCA Bylaws SS8.12 | Two-envelope ballot system (digital equivalent) |
| WPBCA Bylaws SS8.13 | Tiebreaker by coin flip |
| WPBCA Bylaws SS8.14 | Inspector of elections: 1 or 3 independent persons |
| WPBCA Bylaws SS8.2 | 5 directors, 1-year terms, must reside 35%+ of year |
| AB 502 (2022) | Election by acclamation when candidates <= seats |
| AB 2159 (2024, eff. Jan 1 2025) | Electronic secret ballot voting authorized |
| AB 2460 (2024, eff. Jan 1 2025) | Reconvened election quorum reduced to 20% |

---

## Dependencies

| Dependency | What it provides |
|-----------|-----------------|
| `growdirect_postgres` (cove DB) | All persistence (proposals, elections, candidates, ballots, envelopes, audit_log) |
| `growdirect_valkey` DB 1 | Flask-Login session store (sessions gate ballot access) |
| PostgreSQL RLS | `ballot_envelopes` inspector-only SELECT (see [[docs/sdds/cove/ballot-security|Ballot Security]]) |
| `growdirect_ollama` | `Proposal.embedding` for semantic search on election descriptions (optional, degrades gracefully) |
| `cove/governance/services.py` | `create_proposal()`, `get_eligible_voter_count()`, `has_voted()`, `_audit()` |
| `cove/models/governance.py` | `Proposal`, `Ballot`, `BallotEnvelope` shared with governance engine |
| `cove/governance/quorum.py` | `QuorumCalculator`, `AcclamationResult` shared with governance engine |
| `cove/models/member.py` | `Member` -- voter identity, eligibility, password hash |
| `werkzeug.security` | `check_password_hash` for ballot re-authentication |

### Downstream Consumers

No services depend on the election service layer. Election data is consumed read-only by:

- Board dashboard (`cove/board/`) -- election status summaries
- Member dashboard (`cove/member/`) -- active elections, voted indicators
- Archive (`cove/archive/`) -- certified election records for document chain of custody

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Board member (browser) | Election creation: title, description, seats, term, nomination dates | `ElectionForm` POST |
| Any member (browser) | Candidate nomination: name, statement, write-in flag | `CandidateForm` POST |
| Any member (browser) | Ballot: candidate selections + password for re-auth | `ElectionBallotForm` POST |
| Flask-Login session | Voter identity (`current_user.id`) | Server-side session (Valkey) |
| Browser | IP address (`request.remote_addr`) | HTTP header |

### What's Stored

| Table | Field | PII Classification | Encryption Status |
|-------|-------|-------------------|-------------------|
| `proposals` | `title`, `description` | internal | plaintext |
| `proposals` | `created_by` (FK -> members.id) | internal | plaintext |
| `proposals` | `embedding` | internal | plaintext (Vector(1024)) |
| `elections` | `seats`, `term_years`, nomination dates | public | plaintext |
| `candidates` | `name` | internal | plaintext |
| `candidates` | `statement` | internal | plaintext |
| `candidates` | `member_id` (FK -> members.id) | internal | plaintext |
| `candidates` | `nominated_by_id` (FK -> members.id) | internal | plaintext |
| `candidates` | `vote_count` | internal | plaintext |
| `ballots` | `vote`, `method`, `cast_at`, `chain_hash` | **restricted** (anonymous vote content) | plaintext |
| `election_choices` | `ballot_id`, `candidate_id` | **restricted** (anonymous selections) | plaintext |
| `ballot_envelopes` | `ballot_id`, `member_id`, `proposal_id` | **restricted** (voter-ballot link, RLS-gated) | plaintext |
| `audit_log` | `actor_id`, `action`, `details`, `ip_address` | **sensitive** | plaintext |

### What Exits

| Destination | Data | Notes |
|-------------|------|-------|
| Browser (any member) | Candidate list, vote counts, turnout | Public election results after close |
| Browser (voter) | Ballot confirmation page | No ballot content shown after submission |
| Audit log | Who voted, method | **Never** which candidates were selected |
| Board dashboard | Election status summary | No ballot-level data |

### PII Critical Path

The IP address recorded in the audit log for `election_vote.cast` events is the most sensitive non-ballot PII. Combined with the timestamp and member ID in the same audit record, it creates a forensic trail. The IP address is stored plaintext. See Code Review Findings CR-03.

---

## Architecture

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
       +-- create_election()         -> governance/services.create_proposal() + Election
       +-- add_candidate()           -> Candidate + _update_acclamation_status()
       +-- withdraw_candidate()      -> Candidate.status = 'withdrawn'
       +-- check_acclamation()       -> read-only AB 502 check
       +-- declare_acclamation()     -> fast-path certify (no ballot)
       +-- cast_election_vote()      -> atomic: Ballot + ElectionChoice(s) + BallotEnvelope
       +-- tally_election()          -> reads Candidate.vote_count (denormalized)
       +-- resolve_tie()             -> random.choice() + audit
       +-- certify_election()        -> marks winners/losers, certifies Proposal
       +-- create_reconvened_election() -> clones election at 20% quorum (AB 2460)
       |
       v
  PostgreSQL (cove database)
       |
       +-- proposals                 (Proposal -- base record, type='election')
       +-- elections                 (Election -- election-specific data)
       +-- candidates                (Candidate -- nominees, vote_count denormalized)
       +-- election_choices          (ElectionChoice -- anonymous: ballot -> candidate)
       +-- ballots                   (Ballot -- anonymous inner envelope)
       +-- ballot_envelopes          (BallotEnvelope -- identified outer envelope, RLS)
       +-- audit_log                 (all election events)

  quorum.py  (QuorumCalculator -- shared with governance engine)
       |
       +-- calculate("election")    -> quorum_threshold=0.0, secret ballot, no quorum (SS5.9)
       +-- calculate("election", reconvened=True)  -> 20% quorum (AB 2460)
       +-- check_acclamation()      -> AcclamationResult (AB 502)
       +-- wpbca-bylaws-config.json -> all thresholds sourced from config, not hardcoded
```

### Election Lifecycle State Machine

```
  draft --> noticed --> open --> closed --> certified
                                   |
                                   v
                         (reconvened election, AB 2460)
                         draft --> noticed --> open --> closed --> certified

  Acclamation path (AB 502):
  draft --> noticed --> certified  (no ballot period)
```

---

## API Contract

### HTTP Routes (Blueprint: `election_bp`, prefix `/vote/election`)

All routes require `@login_required`. Tenant isolation is enforced in each route handler by comparing `election.proposal.organization_id` to `current_user.organization_id`.

| Method | Path | Role | Purpose |
|--------|------|------|---------|
| GET | `/` | any member | List all elections for the organization |
| GET/POST | `/create` | board (`is_board`) | Create a new election |
| GET | `/<proposal_id>` | any member | Election detail: candidates, acclamation status, voted flag |
| GET/POST | `/<proposal_id>/candidates/add` | any member | Nominate a candidate |
| POST | `/<proposal_id>/candidates/<candidate_id>/withdraw` | board | Withdraw a candidate |
| POST | `/<proposal_id>/acclamation` | board | Declare election by acclamation (AB 502) |
| GET/POST | `/<proposal_id>/ballot` | any member | Display and submit secret ballot |
| GET | `/<proposal_id>/results` | any member | View tally (only when status in `closed`, `certified`) |
| POST | `/<proposal_id>/certify` | board | Certify results and declare winners |

Routes are thin wrappers. All business logic is in `election_services.py`. Routes catch `ValueError` from the service layer and surface them as `flash()` messages with redirect; they do not catch unexpected exceptions (those bubble to the Flask error handler).

### WTForms

**ElectionForm** -- create election:

| Field | Type | Validators |
|-------|------|-----------|
| `title` | `StringField` | `DataRequired`, `Length(5, 500)` |
| `description` | `TextAreaField` | `DataRequired`, `Length(min=20)` |
| `seats` | `IntegerField` | `DataRequired`, `NumberRange(1, 20)` |
| `term_years` | `IntegerField` | `DataRequired`, `NumberRange(1, 5)` |
| `nomination_opens_at` | `DateField` | `Optional` |
| `nomination_closes_at` | `DateField` | `Optional` |

**CandidateForm** -- nominate a candidate:

| Field | Type | Validators |
|-------|------|-----------|
| `name` | `StringField` | `DataRequired`, `Length(2, 255)` |
| `statement` | `TextAreaField` | `Optional`, `Length(max=2000)` |
| `is_write_in` | `BooleanField` | -- |

**ElectionBallotForm** -- secret ballot (Davis-Stirling compliant):

| Field | Type | Validators | Notes |
|-------|------|-----------|-------|
| `candidate_ids` | `SelectMultipleField` | `DataRequired` | Choices populated from election candidates at request time; IDs only |
| `password` | `PasswordField` | `DataRequired` | Re-authentication; value never persisted |

The `ElectionBallotForm` intentionally contains no member identification fields. Voter identity is established by the active Flask-Login session, not by form input.

### Service Layer Functions

| Function | Signature | Returns |
|----------|-----------|---------|
| `create_election()` | `(org_id, created_by, title, description, seats=5, term_years=1, nomination_opens_at=None, nomination_closes_at=None)` | `Election` |
| `add_candidate()` | `(election_id, name, nominated_by_id, member_id=None, statement=None, is_write_in=False)` | `Candidate` |
| `withdraw_candidate()` | `(candidate_id, actor_id)` | `Candidate` |
| `check_acclamation()` | `(election_id)` | `dict` (eligible, seats, active_candidates, candidates, note) |
| `declare_acclamation()` | `(election_id, actor_id)` | `Election` |
| `cast_election_vote()` | `(proposal_id, member, candidate_ids, password, ip_address=None)` | `Ballot` (anonymous) |
| `tally_election()` | `(election_id)` | `dict` (election, ranked, winners, ties, seats, total_ballots, eligible_voters, turnout) |
| `resolve_tie()` | `(election_id, tied_candidate_ids, actor_id)` | `Candidate` (winner) |
| `certify_election()` | `(election_id, actor_id)` | `Election` |
| `create_reconvened_election()` | `(original_election_id, created_by, title=None, description=None)` | `Election` |
| `get_reconvened_quorum()` | `(election, eligible_count)` | `dict` (quorum_met, required, actual, eligible, note) |

---

## Data Model

### Election (`elections`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID, historical pattern |
| `proposal_id` | `String(36)` FK -> proposals.id | Unique (1:1) |
| `seats` | `Integer` | Board seats up for election (WPBCA default: 5) |
| `term_years` | `Integer` | Director term (WPBCA default: 1) |
| `nomination_opens_at` | `DateTime` nullable | Optional nomination window start |
| `nomination_closes_at` | `DateTime` nullable | Optional nomination window end |
| `is_reconvened` | `Boolean` | True if created via AB 2460 reconvene |
| `reconvened_from_id` | `String(36)` FK -> elections.id | Self-referential link to original |
| `acclamation_eligible` | `Boolean` | Recomputed on every add/withdraw |
| `acclamation_declared` | `Boolean` | True once `declare_acclamation()` called |
| `created_at` | `DateTime` | UTC |

Properties: `active_candidates` (list), `can_declare_acclamation` (bool).

### Candidate (`candidates`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID |
| `election_id` | `String(36)` FK -> elections.id | |
| `member_id` | `String(36)` FK -> members.id, nullable | Null for non-member nominees |
| `name` | `String(255)` | Full legal name |
| `statement` | `Text` nullable | Candidacy statement (max 2000 chars) |
| `nominated_by_id` | `String(36)` FK -> members.id | Who submitted nomination |
| `is_write_in` | `Boolean` | Write-in vs. formal nomination |
| `vote_count` | `Integer` | Denormalized -- incremented atomically at vote time |
| `status` | `String(20)` | nominated / accepted / withdrawn / elected / defeated |
| `created_at` | `DateTime` | UTC |

### ElectionChoice (`election_choices`)

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID |
| `ballot_id` | `String(36)` FK -> ballots.id | Anonymous ballot link |
| `candidate_id` | `String(36)` FK -> candidates.id | |
| `created_at` | `DateTime` | UTC |

Unique constraint: `(ballot_id, candidate_id)`. **No `member_id` column -- secret ballot compliance.**

### Table Relationships (Election Domain)

```
proposals (1) --- (1) elections
                       |
                   (1..N) candidates
                       |
election_choices (N) --- (1) candidates
election_choices (N) --- (1) ballots --- (1) ballot_envelopes
                                               |
                                           members (outer envelope, RLS)
```

For the `Ballot`, `BallotEnvelope`, and `Proposal` table definitions, see [[docs/sdds/cove/ballot-security|Ballot Security]].

---

## Request / Data Flows

### Creating an Election (Board Member)

1. `GET /vote/election/create` -- renders `ElectionForm`
2. `POST /vote/election/create` -- `create_election()`:
   - Calls `governance/services.create_proposal()` with `type='election'`
   - Creates linked `Election` record with seats, term, nomination window
   - Commits; redirects to detail view

### Nominating a Candidate (Any Authenticated Member)

1. `POST /vote/election/<proposal_id>/candidates/add` -- `add_candidate()`:
   - Validates election is not closed/certified
   - Checks for duplicate nomination (by `member_id` if a member, by name otherwise)
   - Creates `Candidate` with status `nominated`
   - Calls `_update_acclamation_status()` to recompute `Election.acclamation_eligible`
   - Writes audit record

### Declaring Acclamation (Board, AB 502)

1. `POST /vote/election/<proposal_id>/acclamation` -- `declare_acclamation()`:
   - Validates `can_declare_acclamation` (active candidates <= seats)
   - Sets all active candidates to `elected`
   - Fast-tracks `Proposal.status` to `certified`
   - No ballots created; no ballot period opened

### Casting a Ballot (Authenticated Member)

See [[docs/sdds/cove/ballot-security#Vote Casting Transaction|Ballot Security -- Vote Casting Transaction]] for the full 12-step atomic sequence.

Summary: Voter selects candidates, re-authenticates with password, system creates anonymous `Ballot` + `ElectionChoice` rows, atomically increments `Candidate.vote_count`, creates sealed `BallotEnvelope`, writes audit record (who voted, never which candidates).

### Tallying Results (After Election Closes)

1. `GET /vote/election/<proposal_id>/results` -- `tally_election()`:
   - Reads `Candidate.vote_count` (denormalized -- **never joins to `ballot_envelopes`**)
   - Ranks candidates by vote count descending
   - Detects ties at the last available seat boundary
   - Computes turnout from `Proposal.yes_count` and `get_eligible_voter_count()`

### Tie Resolution (Board, Bylaws SS8.13)

1. `resolve_tie()` -- `random.choice()` over tied candidates
   - Writes detailed audit record: all tied candidates, winner ID, winner name, bylaw citation
   - Does not update candidate statuses -- `certify_election()` handles that

### Certifying (Board)

1. `POST /vote/election/<proposal_id>/certify` -- `certify_election()`:
   - Blocks if unresolved ties remain
   - Marks winners `elected`, losers `defeated`
   - Sets `Proposal.status = 'certified'` and `Proposal.certified_at`

### Reconvened Election (AB 2460)

1. `create_reconvened_election()` -- creates new election linked to original
   - Sets `is_reconvened = True`, `reconvened_from_id`
   - Carries over all non-withdrawn candidates as new `Candidate` records
   - Quorum reduced to 20% via `get_reconvened_quorum()`

---

## Configuration

Elections inherit their proposal defaults from `cove/governance/services.py`:

| Field | Value | Source |
|-------|-------|--------|
| `threshold` | plurality (winner by vote rank, not percentage) | governance services |
| `quorum_required` | 0.0 | bylaws SS5.9 -- no quorum for secret ballot |
| `requires_secret_ballot` | `True` | hardcoded for elections |
| `notice_period_days` | 28 | `wpbca-bylaws-config.json` |
| `ballot_period_days` | 30 | `wpbca-bylaws-config.json` |

WPBCA-specific defaults at `Election` creation:

| Field | Default | Bylaw |
|-------|---------|-------|
| `seats` | 5 | SS8.2 |
| `term_years` | 1 | SS8.2 |

`QuorumCalculator` reads all thresholds from `Cove/cove/governance/wpbca-bylaws-config.json`. No quorum values are hardcoded in Python. The config file is a protected file.

---

## Operations

### Startup Sequence

The election service has no independent startup. It is loaded as part of the Cove Flask app (`election_bp` registered in `cove/__init__.py`). Dependencies:

1. `growdirect_postgres` must be running with the `cove` database and all migrations applied (including RLS migration `c3a1f9b2d4e7`)
2. `growdirect_valkey` DB 1 must be running (session store)
3. `growdirect_ollama` is optional (embedding generation degrades gracefully)

### Health Checks

No election-specific health check. The Cove `/health` endpoint confirms database connectivity. Election functionality depends on:

- Database connectivity (checked by `/health`)
- Session store (checked implicitly by `@login_required`)
- RLS policies active on `ballot_envelopes` (not checked at runtime -- see CR-05)

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Database down | All election operations fail | Flask error handler returns 500 |
| Valkey down | Sessions invalid, `@login_required` redirects to login | No votes can be cast; no data loss |
| Ollama down | Proposal embedding not generated | Election still functions; semantic search unavailable |
| Mid-transaction crash during `cast_election_vote()` | Transaction rolls back | Ballot, choices, envelope, vote count increments all roll back atomically |
| RLS policies missing | `ballot_envelopes` readable by app role | **Davis-Stirling violation** -- see CR-01 |

### Monitoring

| Metric | Alert Threshold | Notes |
|--------|----------------|-------|
| Election proposals in `open` status | None (informational) | Board monitors via dashboard |
| Ballot cast rate during open election | > 5 per minute (unusual for 81-lot HOA) | Possible automation/abuse |
| Failed password re-auth attempts | > 10 per hour per member | Possible credential stuffing |
| `certify_election` without prior `tally_election` | Any occurrence | Logic bypass attempt |

### Environment Variables

No election-specific env vars. All configuration is via `wpbca-bylaws-config.json` and the standard Cove config (`DATABASE_URL`, `VALKEY_URL`, `SECRET_KEY`, etc.).

---

## Deployment

### Docker Service

Election routes run inside the `cove_flask` container. No separate container.

```yaml
# Cove/devops/docker-compose.yml
services:
  cove_flask:
    image: cove-flask
    build:
      context: ..
      dockerfile: devops/Dockerfile
    ports:
      - "5002:5000"
    environment:
      - DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
      - VALKEY_URL=redis://growdirect_valkey:6379/1
    networks:
      - growdirect
```

### AWS Target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Application | ECS/Fargate | Cove Flask container |
| Database | RDS PostgreSQL 17 | With RLS policies applied |
| Sessions | ElastiCache (Valkey-compatible) | DB 1 |
| Secrets | AWS Secrets Manager | `SECRET_KEY`, `DATABASE_URL`, `ENCRYPTION_KEY` |
| RLS roles | RDS IAM or SQL provisioning | `cove_app`, `cove_inspector` roles |

### CI/CD Requirements

- Migration `c3a1f9b2d4e7` must be applied before any election functionality is used
- RLS policy verification test must pass in CI (see CR-05)
- Database connection must use `cove_app` role (not superuser) in production

---

## Error Handling

The service layer uses `ValueError` for all user-correctable validation failures. Routes catch `ValueError` and surface them via `flash(str(exc), "error")`.

| Error Condition | Message |
|----------------|---------|
| Election not found | `"Election not found"` |
| Candidate not found | `"Candidate not found"` |
| Seats < 1 | `"Election must have at least 1 seat"` |
| Add candidate to closed election | `"Cannot add candidates to a closed election"` |
| Duplicate candidate | `"{name} is already a candidate"` |
| Candidate already withdrawn | `"Candidate already withdrawn"` |
| Acclamation not eligible | `"Cannot declare acclamation -- more candidates than seats"` |
| Proposal not found | `"Proposal not found"` |
| Not an election proposal | `"Not an election proposal"` |
| Voting not open | `"Voting is not open for this election"` |
| No candidates selected | `"Must select at least one candidate"` |
| Too many selections | `"Cannot select more than {seats} candidates"` |
| Duplicate candidate in selection | `"Duplicate candidate selections"` |
| Invalid or foreign candidate | `"Invalid candidate: {cid}"` |
| Candidate withdrawn (at vote time) | `"Candidate '{name}' has withdrawn"` |
| Combined lot -- no voting weight | `"Combined lot -- not eligible to vote (bylaw SS5.2)"` |
| Inactive membership | `"Membership is not active"` |
| Password incorrect | `"Password incorrect -- re-authentication failed"` |
| Already voted | `"You have already voted in this election"` |
| Election not closed for certification | `"Election must be closed before certification"` |
| Unresolved ties at certification | `"Unresolved ties -- resolve before certifying"` |
| Fewer than 2 for tie resolution | `"Need at least 2 candidates to resolve a tie"` |

Routes guard against cross-organization access (`organization_id` comparison) and return `abort(403)`. Missing elections return `abort(404)`.

---

## Key Design Decisions

**Two-record election structure.** Elections sit on top of the governance engine's `Proposal` model. This gives elections access to the proposal lifecycle, audit infrastructure, and quorum calculator without duplication. The `Election` record carries only what proposals don't have: seats, term, nomination window, acclamation state, and reconvene linkage.

**Denormalized `vote_count` on Candidate.** Vote tallying reads `Candidate.vote_count`, atomically incremented at vote-cast time using a `table.update().values({col: col + 1})` statement. This avoids a `COUNT(*)` scan over `election_choices` on every tally and means the tally operation never needs to touch `ballot_envelopes`. Vote counts are immutable once committed -- there is no delete-vote path.

**`yes_count` repurposed as `total_ballots_cast`.** `Proposal.yes_count` is incremented once per ballot cast in an election, regardless of which candidates were selected. In election context it serves as the total ballot counter for turnout calculation. `tally_election()` exposes it as `total_ballots` in the return dict.

**Election code co-located in `governance/`.** Elections share the `Proposal` base record, `Ballot`/`BallotEnvelope` infrastructure, `QuorumCalculator`, `_audit()`, and `has_voted()`. Separating into a top-level module would require duplicating or re-exporting all of these.

---

## Known Issues

### UUID stored as `String(36)`

All election models use `String(36)` for UUIDs rather than the platform-standard native `Mapped[uuid.UUID]`. Documented in Cove CLAUDE.md as a historical holdover. Consistent within Cove but should be migrated if tables are meaningfully modified.

### `BallotEnvelope.issued_at` vs. `sealed_at`

Both are set within the same transaction during `cast_election_vote()`. The two fields exist to support a future paper ballot workflow where an envelope might be issued at one time and received/sealed later.

### Paper ballot import not implemented

`Ballot.method` supports `'paper'` and `'in_person'` values but no import path exists. When added, it must use the same `Ballot` + `BallotEnvelope` + `ElectionChoice` path -- no shortcut that bypasses inner/outer envelope separation.

### `random.choice()` in `resolve_tie()`

Uses Python's `random.choice()` (OS entropy seeded). Not cryptographically secure but sufficient -- the audit record captures the full decision for inspector review.

---

## Code Review Findings

### CR-01: Flask app uses superuser DB connection, bypassing RLS (P0)

**Severity:** P0 -- blocks production

**Description:** The RLS migration (`c3a1f9b2d4e7`) creates `cove_app` and `cove_inspector` roles and applies policies to `ballot_envelopes`. However, the Flask application connects to PostgreSQL as `growdirect` (the superuser role defined in `DATABASE_URL`). PostgreSQL RLS policies do not apply to superusers or table owners. In the current configuration, the Flask app can SELECT from `ballot_envelopes` freely, making the RLS policies decorative rather than enforcing.

**Evidence:** `DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove` in `.env` and `docker-compose.yml`. The `growdirect` role owns all tables (created the schema). RLS `USING` clauses only apply to non-owner roles.

**Recommended fix:**
1. In production, connect Flask as `cove_app` role (not superuser)
2. Run migrations and schema changes as a separate admin role
3. Add `ALTER TABLE ballot_envelopes FORCE ROW LEVEL SECURITY` to enforce even on table owner as a defense-in-depth measure
4. Add integration test that verifies `cove_app` role cannot SELECT from `ballot_envelopes`

**Linear issue:** GRO-xxx (to be created)

### CR-02: Application-level envelope access not enforced (P0)

**Severity:** P0 -- blocks production

**Description:** Even if RLS were properly enforced at the DB level, the application code can still construct SQLAlchemy queries that SELECT from `ballot_envelopes`. The `has_voted()` function in `services.py` performs an EXISTS query against `ballot_envelopes` using the same DB session as all other queries. There is no application-level guard preventing a developer from writing `BallotEnvelope.query.filter_by(member_id=x).all()` and obtaining the ballot-to-voter mapping.

**Evidence:** `has_voted()` in `services.py` line 238-248 successfully queries `ballot_envelopes`. If a new route or service function were to join `ballots` to `ballot_envelopes`, nothing in the application layer would prevent it.

**Recommended fix:**
1. Create a dedicated `EnvelopeWriteOnly` proxy that exposes only `insert()` and `exists_check()` methods
2. Remove the `BallotEnvelope` model import from all modules except the write proxy and the inspector-specific query module
3. Add a linting rule or test that scans governance code for `BallotEnvelope.query` or `select(BallotEnvelope)` outside the permitted modules
4. The `has_voted()` function should use a raw EXISTS query via the `cove_app` role connection (which RLS permits for INSERT, not SELECT -- so this needs a targeted policy addition for EXISTS-only checks)

**Linear issue:** GRO-xxx (to be created)

### CR-03: IP addresses logged plaintext in audit trail (P1)

**Severity:** P1 -- before GA

**Description:** `cast_election_vote()` passes `request.remote_addr` to `_audit()`, which stores it as-is in the `audit_log.details` JSON field. For election vote events, this creates a linkable record: (member_id, timestamp, IP address). While the audit log does not record which candidates were selected, the IP combined with timing could be used to correlate voter identity with external network logs.

**Evidence:** `election_routes.py` line 264 passes `ip_address=request.remote_addr`. `_audit()` stores it in the `details` dict.

**Recommended fix:** Hash or truncate IP addresses before storage. Use `hashlib.sha256(ip + salt).hexdigest()[:16]` for a one-way identifier that supports duplicate detection without exposing the actual IP. Apply to all audit log entries, not just elections.

**Linear issue:** GRO-xxx (to be created)

### CR-04: No audit trail for election lifecycle transitions (P1)

**Severity:** P1 -- before GA

**Description:** While vote casting and certification write audit records, several election lifecycle transitions do not:
- Opening voting (proposal status `draft -> noticed -> open`) is handled by governance services, not election services, and may not audit the transition
- Closing voting (proposal status `open -> closed`) -- same issue
- Reconvened election creation writes no audit record specific to the reconvene action

**Recommended fix:** Add `_audit()` calls for `election.opened`, `election.closed`, and `election.reconvened` events in the service layer or governance lifecycle hooks.

**Linear issue:** GRO-xxx (to be created)

### CR-05: No runtime verification of RLS policy presence (P1)

**Severity:** P1 -- before GA

**Description:** The application has no check at startup or health-check time that RLS is actually enabled on `ballot_envelopes` and that the expected policies exist. If a migration rollback or manual intervention removes RLS, elections would proceed without ballot secrecy.

**Recommended fix:** Add a startup check (or health-check sub-check) that queries `pg_catalog.pg_policies` for the expected policies on `ballot_envelopes`. Log a CRITICAL error and refuse to serve election routes if policies are missing.

**Linear issue:** GRO-xxx (to be created)

### CR-06: No data retention policy for ballot data (P1)

**Severity:** P1 -- before GA

**Description:** Ballot records, election choices, and ballot envelopes are stored indefinitely. Davis-Stirling requires election records to be maintained for a minimum of 12 months (Civil Code SS5125). There is no automated purge or archival process, and no documented retention policy.

**Recommended fix:** Implement retention policy: ballots and envelopes retained 24 months, then archived (election results preserved, individual ballot records purged). Document in compliance artifacts.

**Linear issue:** GRO-xxx (to be created)

### CR-07: No rate limiting on ballot submission endpoint (P1)

**Severity:** P1 -- before GA

**Description:** The `POST /vote/election/<proposal_id>/ballot` endpoint has no rate limiting. While the `has_voted()` check prevents duplicate votes, a compromised session could submit rapid requests attempting credential stuffing (trying different passwords) or causing DB load.

**Recommended fix:** Add Flask-Limiter on the ballot POST endpoint. Suggested: 5 attempts per minute per session, 20 per hour per IP.

**Linear issue:** GRO-xxx (to be created)

### CR-08: Candidate name stored plaintext, no input sanitization beyond strip() (P2)

**Severity:** P2 -- post-launch

**Description:** `Candidate.name` is stripped of whitespace but not sanitized for HTML/JS injection. The name is rendered in templates via Jinja2 (which auto-escapes), so XSS risk is low. However, the name is also stored in audit log `details` JSON, which may be rendered differently in admin views.

**Recommended fix:** Add explicit `bleach.clean()` or equivalent to candidate name and statement inputs at the service layer. Ensure audit log detail rendering also auto-escapes.

**Linear issue:** GRO-xxx (to be created)

### CR-09: `certify_election()` calls `tally_election()` internally -- redundant DB reads (P2)

**Severity:** P2 -- post-launch

**Description:** `certify_election()` calls `tally_election()` to get the ranked list, which re-queries candidates. For the 81-lot WPBCA with 5 seats, this is negligible. For larger HOAs it could be optimized.

**Recommended fix:** Accept pre-computed tally results as an optional parameter to `certify_election()`.

---

## Production Readiness Checklist

- [ ] PII encrypted at rest -- ballot data plaintext, envelope data plaintext (CR-01, CR-02 block this)
- [ ] Secrets in AWS Secrets Manager (not .env) -- `SECRET_KEY`, `DATABASE_URL` still in `.env`
- [ ] Health check endpoint responds -- `/health` exists but does not verify RLS (CR-05)
- [ ] Audit logging for sensitive operations -- vote casting audited, lifecycle transitions missing (CR-04)
- [ ] Data retention policy implemented -- no retention policy (CR-06)
- [ ] Rate limiting on public endpoints -- no rate limiting on ballot submission (CR-07)
- [ ] Error responses don't leak internals -- `ValueError` messages are user-facing, no stack traces exposed
- [ ] RLS enforced at database level -- policies exist but superuser bypasses them (CR-01)
- [ ] Application-level ballot secrecy enforced -- no guard against envelope queries (CR-02)
- [ ] IP addresses masked in audit log -- stored plaintext (CR-03)
- [ ] Election lifecycle fully audited -- partial coverage (CR-04)
- [ ] RLS presence verified at runtime -- no check (CR-05)

---

## Testing

Tests live under `Cove/tests/` following the three-layer GrowDirect test standard.

### Unit Tests

- `Election.can_declare_acclamation` property with varying candidate/seat ratios
- `Election.active_candidates` filters withdrawn correctly
- `_update_acclamation_status()` recomputes `acclamation_eligible` after add and withdraw
- `_detect_ties()` with: no tie, exact fill, tie spanning the cutoff, all tied
- `check_acclamation()` returns correct `eligible` flag and note text
- `get_reconvened_quorum()` for reconvened vs. standard elections

### Integration Tests

- Create election as board member; verify Proposal + Election records created
- Create election as non-board member; expect 403
- Nominate candidate; verify Candidate row and audit log entry
- Nominate duplicate member; expect ValueError
- Withdraw candidate; verify status transition and acclamation recompute
- Declare acclamation when candidates <= seats; verify all elected, proposal certified
- Declare acclamation when candidates > seats; expect ValueError
- `cast_election_vote()` happy path: verify atomic write of Ballot, ElectionChoice, BallotEnvelope, incremented vote_count, incremented yes_count
- Cast vote with wrong password; expect ValueError
- Cast vote when already voted; expect ValueError
- Cast vote with `voting_weight == 0`; expect ValueError
- Cast vote selecting more than seats; expect ValueError
- Cast vote on closed proposal; expect ValueError
- `tally_election()` returns correct ranking and turnout
- `certify_election()` with no ties; verify winner/loser statuses
- `certify_election()` with unresolved ties; expect ValueError
- `resolve_tie()` writes audit record with all required fields
- `create_reconvened_election()` carries over candidates; sets is_reconvened

### Smoke Tests

- `GET /vote/election/` returns 200 for authenticated member
- `GET /vote/election/<id>/ballot` for open election returns 200
- `GET /vote/election/<id>/results` before close returns redirect

### Critical Invariant Tests

- `tally_election()` SQL does NOT reference `ballot_envelopes` table
- `ElectionChoice` rows have no `member_id` column (schema inspection)
- `Ballot` rows have no `member_id` column
- Creating a `Ballot` never passes `member.id` to it
- RLS policies exist on `ballot_envelopes` (query `pg_catalog.pg_policies`)
