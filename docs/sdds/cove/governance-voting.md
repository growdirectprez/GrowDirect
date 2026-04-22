# Governance Voting -- Ballot Mechanics & Secrecy

> **Status:** Production-grade ops contract
> **Type:** App Service (Cove)
> **Namespace:** cove
> **Last updated:** 2026-04-13
> **Code location:** `Cove/cove/governance/services.py`, `Cove/cove/governance/quorum.py`, `Cove/cove/models/governance.py`
> **Split parent:** [[docs/sdds/cove/governance-engine|Governance Engine]] -- proposal lifecycle, state machine, proceedings

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Compliance|Compliance]] · **Operator role:** [[Canary/docs/profiles/ops/Legal|Legal]] + [[Canary/docs/profiles/ops/Jeremy|Jeremy]]

---

## Purpose

This SDD covers the voting mechanics of the Cove Governance Engine: ballot casting, ballot/envelope separation for secret ballot compliance, vote tallying, quorum calculation, result determination, and the inspector dashboard. The two-table ballot architecture implements the Davis-Stirling two-envelope system (Civil Code 5100, WPBCA Bylaws 8.12) where vote content and voter identity are structurally separated.

Proposal lifecycle, state machine, and proceedings tracking are in [[docs/sdds/cove/governance-engine|Governance Engine]].

---

## Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| PostgreSQL 17 (`growdirect_postgres:5432/cove`) | Infrastructure | `ballots`, `ballot_envelopes`, `proposals` tables |
| `cove.models.governance.Ballot` | App model | Anonymous vote content (no member_id -- by design) |
| `cove.models.governance.BallotEnvelope` | App model | Sealed voter-to-ballot link (RLS-gated) |
| `cove.models.governance.Proposal` | App model | Denormalized vote counts, status check |
| `cove.models.member.Member` | App model | Eligibility, re-authentication, voting_weight |
| `cove.models.audit.AuditLog` | App model | Insert-only event log |
| `wpbca-bylaws-config.json` | Config file | Quorum thresholds, passage ratios, electronic eligibility |
| `werkzeug.security.check_password_hash` | Library | Password re-authentication at vote time |

---

## Data Flow & PII Map

### What Enters

| Source | Data | Format |
|--------|------|--------|
| Member (browser) | Vote choice (yes/no/abstain) + password re-auth | POST form (CSRF-protected) |
| `request.remote_addr` | IP address | Passed to audit log |
| Flask `current_user` | Member identity (from session) | Used for envelope, never written to ballot |

### What Is Stored

| Table | Field | PII Classification | Encryption | Notes |
|-------|-------|-------------------|------------|-------|
| `ballots` | `vote` | **restricted** | **plaintext** | Vote content -- anonymous by design (no member_id column exists) |
| `ballots` | `method` | none | plaintext | "electronic", "paper", "in_person" |
| `ballots` | `cast_at` | none | plaintext | Timestamp |
| `ballots` | `chain_hash` | none | plaintext nullable | Future blockchain anchor |
| `ballot_envelopes` | `member_id` | **restricted** | **plaintext** | Voter identity -- RLS-gated, inspector-only SELECT |
| `ballot_envelopes` | `ballot_id` | **restricted** | **plaintext** | Links to anonymous ballot -- RLS-gated |
| `ballot_envelopes` | `sealed_at` | internal | plaintext | When vote was cast |
| `proposals` | `yes_count`, `no_count`, `abstain_count` | internal | plaintext | Denormalized aggregate counts |
| `audit_log` | `actor_id` (on vote.cast) | internal | plaintext | Records WHO voted |
| `audit_log` | `details` (on vote.cast) | none | plaintext | Records `{method: "electronic"}` -- **never** the vote value |
| `audit_log` | `ip_address` | **sensitive** | **plaintext** | Voter IP -- should be hashed |

### The Ballot/Envelope Separation -- Non-Negotiable

```
                  +-----------------+
                  |    ballots      |
                  |-----------------|
                  | id              |
                  | proposal_id     |   <-- NO member_id column.
                  | vote            |       This is by design and
                  | method          |       must NEVER change.
                  | cast_at         |
                  | chain_hash      |
                  +-----------------+
                         |
                         | ballot_id (FK)
                         |
                  +-----------------+
                  | ballot_envelopes|   <-- PostgreSQL RLS
                  |-----------------|       cove_app: INSERT only
                  | id              |       cove_inspector: SELECT only
                  | ballot_id       |
                  | member_id       |   <-- Voter identity sealed here
                  | proposal_id     |
                  | issued_at       |
                  | sealed_at       |
                  +-----------------+
```

The `ballots` table is the anonymous inner envelope (vote content only). The `ballot_envelopes` table is the sealed outer envelope (voter identity). The application never joins these tables for tallying. Results are read from the denormalized `yes_count/no_count/abstain_count` on `proposals`.

**Unique constraint:** `uq_one_vote_per_member_per_proposal` on `(member_id, proposal_id)` in `ballot_envelopes` prevents duplicate votes at the database level.

### What Exits

| Destination | Data | Notes |
|-------------|------|-------|
| Browser | Vote confirmation + receipt | Receipt contains ballot ID prefix, timestamp -- never vote content |
| Browser | Aggregated results | `yes_count`, `no_count`, `abstain_count`, quorum, pass/fail |
| Audit log | `vote.cast` event | WHO voted and method -- never WHAT they voted |

---

## API Contract

### Voting Routes (within governance_bp at `/vote`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/vote/<proposal_id>/ballot` | login_required | Ballot form (redirects if already voted or not open) |
| POST | `/vote/<proposal_id>/ballot` | login_required | Cast vote with password re-auth |
| GET | `/vote/<proposal_id>/results` | login_required | Aggregated results (closed/certified only) |
| POST | `/vote/<proposal_id>/recount` | board or inspector | Verify denormalized counts against ballot rows |
| GET | `/vote/inspector` | inspector or admin | Inspector dashboard with recount data |

### BallotForm

```
vote     -- SelectField: yes | no | abstain
password -- PasswordField for re-authentication
```

**No member identification fields.** This is by design (Davis-Stirling 5100-5145). Identity linkage is handled exclusively by the service layer via `ballot_envelopes`.

---

## Operations

### Vote Casting Flow

```
POST /vote/<id>/ballot
  -> BallotForm.validate_on_submit()
  -> services.cast_vote(proposal_id, member, vote, password, ip_address)

     Pre-conditions (checked in order):
     1. vote in {yes, no, abstain}
     2. proposal.status == "open"
     3. member.voting_weight > 0          (bylaw 5.2 -- combined lots excluded)
     4. member.membership_status == "active"
     5. Password re-auth via check_password_hash
     6. has_voted(member_id, proposal_id)  (EXISTS on ballot_envelopes)

     Atomic transaction:
     1. INSERT Ballot (no member_id) -> flush to get ballot.id
     2. INSERT BallotEnvelope (ballot_id + member_id) -> sealed link
     3. UPDATE proposals SET <vote>_count = <vote>_count + 1  (raw SQL for atomicity)
     4. INSERT AuditLog("vote.cast", {method}) -> WHO, never WHAT

  -> render vote_confirmed.html with receipt
```

### Ballot Receipt

`generate_ballot_receipt(ballot)` returns:
- `receipt_id` -- first 8 chars of ballot UUID
- `proposal_title` -- human reference
- `cast_at` -- ISO timestamp
- `chain_hash_prefix` -- first 12 chars (if present)
- `method` -- "electronic"
- `verification_note` -- confirms ballot recorded without revealing vote

### Quorum Calculation

**QuorumCalculator** (`quorum.py`) is Flask-free and SQLAlchemy-free. It reads the JSON config directly and operates on integers passed by the caller. This makes it testable without an application context and reusable by the elections subsystem.

| Method | Purpose |
|--------|---------|
| `calculate(proposal_type, members_present=None, reconvened=False)` | Full quorum result with thresholds and citations |
| `calculate_board_quorum()` | Board meeting: 3 of 5 directors (9.13) |
| `check_acclamation(candidates, seats)` | AB 502: acclamation when candidates <= seats |

**Quorum rules:**

| Context | Threshold | Citation |
|---------|-----------|----------|
| General business | 33% | 6.6.1.c |
| Special assessment | 50% | 6.6.1.a |
| Secret ballot votes | 0% (none) | 5.9 |
| Reconvened election | 20% | AB 2460 (eff. 2025) |
| Board meeting | 50% of 5 directors | 9.13 |

### Result Determination

`determine_result(proposal, quorum)`:
- Elections: return `{type: "election", passed: None}` -- plurality resolved by elections subsystem
- All others: if quorum not met, `passed=False`. Otherwise `yes_ratio = yes / (yes + no)` (abstains excluded), compare to `proposal.threshold`.

`get_results(proposal_id)`: Assembles full results payload. Reads **only** from `proposals` table -- never touches `ballot_envelopes`.

### Recount

`recount_proposal(proposal_id)`: Independently counts `Ballot` rows by vote value and compares against denormalized `yes_count/no_count/abstain_count` on `Proposal`. Returns `{match: bool, actual: {...}, recorded: {...}}`. Logs to audit trail.

### Inspector Dashboard

`GET /vote/inspector` (inspector or admin only): For each open/closed/certified proposal, computes recount and full results. Displays integrity status per proposal.

### Atomic Vote Count Design

Rather than counting rows in `ballots` at query time (inconsistent reads under concurrency), the engine issues `UPDATE proposals SET yes_count = yes_count + 1` via raw SQL immediately after the ballot insert, inside the same transaction. `recount_proposal()` exists as a verification mechanism to detect any divergence.

### Re-Authentication at Vote Cast

`cast_vote()` requires password re-authentication before recording a ballot. This prevents session hijacking from translating into fraudulent votes. Uses `werkzeug.security.check_password_hash` against `member.password_hash`.

### Bylaw 5.2 -- One Vote Per Lot

`get_eligible_voter_count()` filters for `voting_weight > 0`. Combined lots have `voting_weight = 0` on the subordinate record. `cast_vote()` also checks `member.voting_weight > 0` directly.

### Row-Level Security (RLS) on ballot_envelopes

Migration `c3a1f9b2d4e7` enables PostgreSQL RLS on `ballot_envelopes`:

| Policy | Role | Permission | Rule |
|--------|------|-----------|------|
| `envelope_no_read` | `cove_app` | SELECT | `USING (false)` -- denied |
| `envelope_insert` | `cove_app` | INSERT | `WITH CHECK (true)` -- allowed |
| `envelope_inspector_read` | `cove_inspector` | SELECT | `USING (true)` -- allowed |

The application connects as `cove_app` (INSERT-only access to envelopes). The inspector role `cove_inspector` has read access for verification.

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| Duplicate vote attempt (race condition) | `uq_one_vote_per_member_per_proposal` constraint catches it | IntegrityError, 500 (unhandled -- see Findings) |
| Wrong password | Vote rejected | ValueError, flash message |
| Proposal not open | Vote rejected | ValueError, flash message |
| Vote count divergence | Incorrect results displayed | Detected by `recount_proposal()`, manual fix required |

---

## Data Model

### Ballot

Table: `ballots`

**Critical: NO `member_id` column. This is by design and must never change.**

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID v4 |
| `proposal_id` | FK `proposals.id` | |
| `vote` | `String(10)` | yes, no, abstain |
| `method` | `String(20)` | electronic, paper, in_person |
| `cast_at` | `DateTime` | |
| `chain_hash` | `String(100)` nullable | SHA-256 for future audit chain |

### BallotEnvelope

Table: `ballot_envelopes`

The sealed outer envelope. Links ballot to voter. Protected by PostgreSQL RLS -- only the `cove_inspector` role has SELECT permission.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `String(36)` PK | UUID v4 |
| `ballot_id` | FK `ballots.id` | the anonymous ballot |
| `member_id` | FK `members.id` | the voter |
| `proposal_id` | FK `proposals.id` | denormalized for unique check |
| `issued_at` | `DateTime` | |
| `sealed_at` | `DateTime` nullable | set when ballot is cast |

Unique constraint: `uq_one_vote_per_member_per_proposal` on `(member_id, proposal_id)`.

---

## Deployment

Voting runs inside the `cove_flask` container. No separate service. See [[docs/sdds/cove/governance-engine|Governance Engine]] for deployment details.

### RLS Deployment Requirement

The RLS migration (`c3a1f9b2d4e7`) must run before first production deployment. Post-migration verification:
1. Confirm `cove_app` role exists and is the application connection role
2. Confirm `cove_inspector` role exists
3. Confirm `SELECT * FROM ballot_envelopes` returns 0 rows when connected as `cove_app` (even if rows exist)
4. Confirm `INSERT INTO ballot_envelopes` succeeds as `cove_app`

---

## Code Review Findings

### VOT-F01: RLS Is DB-Side Only -- Application Code Bypasses It

**Severity:** P0 (blocks prod)

The RLS migration creates policies for `cove_app` and `cove_inspector` roles. However, the application likely connects to PostgreSQL as the `growdirect` superuser (the dev credential in `DATABASE_URL`), which bypasses RLS entirely. PostgreSQL RLS does not apply to table owners or superusers. This means the ballot/envelope separation exists in code discipline only -- any code change that adds a JOIN would expose voter-ballot links.

**Evidence:** `DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove` connects as `growdirect`, not `cove_app`. The `cove_app` role is created in the migration but never used by the Flask application.

**Recommended fix:**
1. Configure the Flask application to connect as `cove_app` role (not `growdirect`)
2. Grant `cove_app` appropriate permissions on all tables (not just `ballot_envelopes`)
3. Verify with integration test: connect as `cove_app`, attempt `SELECT * FROM ballot_envelopes`, expect 0 rows
4. Add a CI test that asserts the application connection role is not a superuser

**Linear issue:** TBD

### VOT-F02: `has_voted()` SELECT on ballot_envelopes Contradicts RLS Intent

**Severity:** P1 (before GA)

`has_voted()` runs `SELECT EXISTS ... FROM ballot_envelopes WHERE member_id=... AND proposal_id=...`. This is a SELECT on the RLS-protected table. If the application connects as `cove_app` with the `envelope_no_read` policy active, `has_voted()` would always return False (the policy returns no rows), allowing unlimited duplicate votes.

The current system works because the application bypasses RLS (see VOT-F01). When VOT-F01 is fixed, `has_voted()` will break.

**Recommended fix:** Either:
(a) Change the RLS policy to allow `cove_app` to execute `EXISTS` checks on `ballot_envelopes` (add a policy for SELECT with `USING (member_id = current_setting('app.current_member_id'))`) -- complex, requires session variables.
(b) Track "has voted" status separately -- add a `voted_proposal_ids` array on Member or a lightweight `vote_receipts` table that the app role can read.
(c) Keep the `has_voted()` query but grant limited SELECT to `cove_app` with column restrictions (only `member_id` and `proposal_id`, not `ballot_id`).

**Linear issue:** TBD

### VOT-F03: Electronic Ballot Opt-In Not Enforced (AB 2159)

**Severity:** P1 (before GA)

AB 2159 requires member opt-in for electronic secret ballots. `Member.delivery_preference` exists (electronic | paper | both), but `cast_vote()` does not check it. The `is_electronic_eligible()` check in `bylaws_config.py` covers the proposal type but not the individual member's consent.

**Recommended fix:** In `cast_vote()`, after eligibility checks, verify `member.delivery_preference in ("electronic", "both")` when the ballot method is electronic. Members who have not opted in should be directed to paper ballot procedures.

**Linear issue:** TBD

### VOT-F04: Duplicate Vote Constraint Violation Not Caught

**Severity:** P1 (before GA)

If `has_voted()` races with a concurrent insert (two requests for the same member), the `uq_one_vote_per_member_per_proposal` constraint raises `IntegrityError`. The route handler catches `ValueError` but not `IntegrityError`, resulting in a 500 error instead of a user-friendly message.

**Recommended fix:** Catch `sqlalchemy.exc.IntegrityError` in `cast_vote()` and raise `ValueError("You have already voted on this proposal")`.

**Linear issue:** TBD

### VOT-F05: Ballot Vote Content Stored Plaintext

**Severity:** P1 (before GA)

The `ballots.vote` column stores "yes", "no", or "abstain" in plaintext. While the table has no `member_id` column, the ballot can be correlated to a voter through timing analysis (compare `ballots.cast_at` with `ballot_envelopes.sealed_at` for rows with the same `proposal_id`). Encrypting the vote value would add defense-in-depth.

**Recommended fix:** Encrypt `ballots.vote` with AES-256-GCM using a key held only by the inspector role. The application writes an encrypted value; tallying reads from the denormalized counts (which are in memory during the transaction). The inspector can decrypt for recount verification.

**Linear issue:** TBD

### VOT-F06: Timing Correlation Between Ballot and Envelope

**Severity:** P2 (post-launch)

`Ballot.cast_at` and `BallotEnvelope.sealed_at` are set within the same transaction (same second). A database admin with access to both tables can correlate rows by matching `proposal_id` + timestamp. This degrades ballot secrecy for low-turnout votes where timestamps are unique.

**Recommended fix:** Add random jitter (0-60 seconds) to `BallotEnvelope.sealed_at` or remove the column entirely (its value is redundant with `Ballot.cast_at`). Alternatively, batch envelope inserts at the end of the voting period.

**Linear issue:** TBD

### VOT-F07: Dual Route Registration for Ballot POST

**Severity:** P2 (post-launch)

`routes.py` registers two POST handlers for `/<proposal_id>/ballot`: `ballot_form()` (handles GET and POST) and `cast_vote()` (POST-only alias for tests). Flask resolves this by using the last-registered route. This works but is fragile -- reordering registrations could change behavior silently.

**Recommended fix:** Remove the duplicate `cast_vote()` route. Update tests to use `ballot_form` endpoint.

**Linear issue:** TBD

### VOT-F08: Inspector Dashboard Runs Recount on Every Page Load

**Severity:** P2 (post-launch)

`GET /vote/inspector` calls `recount_proposal()` for every open/closed/certified proposal on each page load. Each recount runs 3 COUNT queries against `ballots`. For a small association (81 lots) this is fine, but the pattern does not scale. Each recount also writes an audit log entry, polluting the log.

**Recommended fix:** Cache recount results in Valkey with a 5-minute TTL. Only write audit entries on explicit recount requests, not dashboard loads.

**Linear issue:** TBD

---

## Production Readiness Checklist

- [ ] RLS enforced at connection level (application connects as `cove_app`, not superuser) -- **P0** (VOT-F01)
- [ ] `has_voted()` compatible with RLS policy -- **P1** (VOT-F02)
- [ ] AB 2159 electronic opt-in enforced -- **P1** (VOT-F03)
- [ ] Duplicate vote IntegrityError caught gracefully -- **P1** (VOT-F04)
- [ ] Ballot vote content encrypted -- **P1** (VOT-F05)
- [ ] IP addresses hashed in audit log -- **P1** (see governance-engine.md GOV-F03)
- [ ] Timing correlation mitigated -- **P2** (VOT-F06)
- [x] Ballot table has NO member_id column -- verified in model and migration
- [x] BallotEnvelope has unique constraint preventing duplicate votes -- `uq_one_vote_per_member_per_proposal`
- [x] RLS migration exists -- `c3a1f9b2d4e7` creates policies for cove_app and cove_inspector
- [x] Tallying reads only from `proposals` denormalized counts -- verified in `get_results()`
- [x] Audit log records WHO voted but never WHAT -- verified in `_audit()` call
- [x] Password re-authentication required at vote time
- [x] CSRF protection on BallotForm
- [x] Org isolation on all voting routes
- [x] Quorum calculator is Flask-free and independently testable

---

## Testing

### Key Test Cases

**Ballot secrecy test:** After `cast_vote()`:
1. A `Ballot` row exists with the correct vote value and no `member_id` column
2. A `BallotEnvelope` row exists linking `ballot_id` to `member_id`
3. `get_results()` output does not reference `ballot_envelopes`

**Vote precondition tests:**
- Closed proposal: ValueError
- Already voted: ValueError
- Inactive member: ValueError
- Combined lot (voting_weight=0): ValueError
- Wrong password: ValueError

**Quorum calculator tests** (Flask-free):
- All seven proposal types return correct `quorum_needed` for `total_lots=81`
- `reconvened=True` returns 20% threshold (AB 2460)
- `check_acclamation(3, 5)` returns `acclamation=True`
- `check_acclamation(6, 5)` returns `acclamation=False`
- `calculate_board_quorum()` returns `quorum_needed=3`

**Recount tests:**
- After N votes, recount returns `match=True`
- After manual count manipulation, recount returns `match=False`
