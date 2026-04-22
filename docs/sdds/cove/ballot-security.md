# Ballot Security

> **Status:** Production-grade ops contract
> **Type:** App Service (Cove)
> **Namespace:** cove
> **Last updated:** 2026-04-13
> **Code location:** `Cove/cove/models/governance.py`, `Cove/cove/governance/services.py`, `Cove/cove/governance/election_services.py`, `Cove/migrations/versions/c3a1f9b2d4e7_enable_rls_on_ballot_envelopes.py`
> **Parent SDD:** [[docs/sdds/cove/secret-ballot-elections|Secret Ballot Elections]] -- election orchestration, lifecycle, API contract

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[Canary/docs/profiles/ops/Compliance|Compliance]] · **Operator role:** [[Canary/docs/profiles/ops/Legal|Legal]]

---

## Purpose

This SDD documents the most sensitive data handling in the Cove platform: the two-envelope ballot system that enforces secret ballot compliance under the California Davis-Stirling Act. It covers:

1. The two-table architecture that separates voter identity from vote content
2. PostgreSQL Row-Level Security policies that seal the voter-ballot link
3. Application-level enforcement (and its current gaps)
4. The chain hash integrity model
5. The inspector role and its scoped access

This is the security-critical companion to [[docs/sdds/cove/secret-ballot-elections|Secret Ballot Elections]]. Any code change touching `ballots`, `ballot_envelopes`, `election_choices`, or RLS policies must be reviewed against this document.

---

## Dependencies

| Dependency | What it provides |
|-----------|-----------------|
| `growdirect_postgres` (cove DB) | `ballots`, `ballot_envelopes`, `election_choices` tables + RLS policies |
| PostgreSQL RLS engine | Row-level policy enforcement on `ballot_envelopes` |
| `cove_app` PostgreSQL role | Application connection role (INSERT only on envelopes) |
| `cove_inspector` PostgreSQL role | Inspector connection role (SELECT on envelopes) |
| `cove/governance/services.py` | `has_voted()` -- the only permitted SELECT-adjacent operation on envelopes |
| `cove/governance/election_services.py` | `cast_election_vote()` -- the atomic vote-casting transaction |
| Migration `c3a1f9b2d4e7` | RLS policy definitions |

---

## Data Flow & PII Map

### The Two-Envelope Model

The Davis-Stirling Act (Civil Code SS5100-5145) and WPBCA Bylaws SS8.12 require a two-envelope ballot process:

- **Inner envelope** (anonymous): contains the vote. No identifying information.
- **Outer envelope** (identified): contains the voter's identity. Sealed and handed to the inspector.

The digital implementation:

```
INNER ENVELOPE (anonymous)              OUTER ENVELOPE (identified, RLS-sealed)
+----------------------------+          +-----------------------------------+
| ballots                    |          | ballot_envelopes                  |
|   id (UUID)                |<---------|   ballot_id (FK)                  |
|   proposal_id (FK)         |          |   member_id (FK) -- VOTER ID      |
|   vote ('election' marker) |          |   proposal_id (FK)                |
|   method (electronic)      |          |   sealed_at (timestamp)           |
|   cast_at (timestamp)      |          +-----------------------------------+
|   chain_hash (SHA-256)     |                    |
+----------------------------+                    | RLS: SELECT denied to cove_app
        |                                         | RLS: SELECT granted to cove_inspector
        |
+----------------------------+
| election_choices           |
|   ballot_id (FK) --------->|  (linked to ballot, NOT to member)
|   candidate_id (FK)        |
+----------------------------+
```

### PII Classification

| Table | Field | Classification | Who Can Read | Notes |
|-------|-------|---------------|-------------|-------|
| `ballots.id` | Ballot receipt identifier | restricted | Any code with DB access | Anonymous -- no identity attached |
| `ballots.vote` | Vote content marker | restricted | Any code with DB access | Set to 'election' for elections, 'yes'/'no'/'abstain' for proposals |
| `ballots.chain_hash` | Integrity hash | restricted | Any code with DB access | SHA-256, nullable |
| `election_choices.ballot_id` | Anonymous ballot link | restricted | Any code with DB access | Links to candidate selections without voter identity |
| `election_choices.candidate_id` | Candidate selected | restricted | Any code with DB access | Combined with ballot_id, reveals vote content (anonymously) |
| `ballot_envelopes.ballot_id` | Ballot link | **restricted** | `cove_inspector` only (RLS) | The join key that connects identity to vote |
| `ballot_envelopes.member_id` | Voter identity | **restricted** | `cove_inspector` only (RLS) | **THE MOST SENSITIVE FIELD IN THE PLATFORM** |
| `ballot_envelopes.proposal_id` | Election identifier | **restricted** | `cove_inspector` only (RLS) | Used for duplicate-vote prevention |
| `ballot_envelopes.sealed_at` | Seal timestamp | **restricted** | `cove_inspector` only (RLS) | When the vote was committed |

### The Critical Join

The join `ballot_envelopes.ballot_id -> ballots.id -> election_choices.candidate_id` would reveal which candidates a specific member voted for. **This join must never be executed in normal application operation.** The RLS policies exist to prevent it at the database level. Application-level discipline exists to prevent it at the code level.

---

## PostgreSQL Row-Level Security

### Migration: `c3a1f9b2d4e7_enable_rls_on_ballot_envelopes.py`

The migration creates two database roles and three RLS policies:

#### Roles

| Role | Purpose | Created |
|------|---------|---------|
| `cove_app` | Application connection role | Migration (safety net; should exist from provisioning) |
| `cove_inspector` | Inspector-only read access | Migration |

#### Policies

| Policy | Target | Operation | Rule | Effect |
|--------|--------|-----------|------|--------|
| `envelope_no_read` | `cove_app` | SELECT | `USING (false)` | App role cannot read any envelope rows |
| `envelope_insert` | `cove_app` | INSERT | `WITH CHECK (true)` | App role can insert envelopes (vote casting) |
| `envelope_inspector_read` | `cove_inspector` | SELECT | `USING (true)` | Inspector role can read all envelopes |

#### Grants

```sql
GRANT INSERT ON ballot_envelopes TO cove_app;
GRANT SELECT ON ballot_envelopes TO cove_inspector;
```

### RLS Enforcement Gap (CR-01 in parent SDD)

**Current state:** The Flask application connects as the `growdirect` superuser role, which owns the `ballot_envelopes` table. PostgreSQL RLS does not apply to table owners or superusers. The three policies defined above are therefore **not enforced** in the current deployment.

This is the single most critical security finding in the platform. See Code Review Findings below for the full remediation plan.

---

## Application-Level Enforcement

### Rules (Non-Negotiable)

These rules exist as code discipline enforced by developer awareness and code review. They are documented in `Cove/CLAUDE.md` as hard rules.

1. **`ballots` table has NO `member_id` column.** This is a schema-level guarantee. No migration may add a member identifier to the ballots table.

2. **`election_choices` table has NO `member_id` column.** Same schema-level guarantee.

3. **`tally_election()` reads ONLY from `candidates.vote_count`.** It does not query `ballots`, `election_choices`, or `ballot_envelopes`. Tallying uses the denormalized count.

4. **Governance services NEVER JOIN `ballots` to `ballot_envelopes`.** This is stated in the module docstring of `services.py` line 3.

5. **`ElectionBallotForm` contains no member identity fields.** Member identity is established exclusively via Flask-Login session.

6. **Audit records for vote events record WHO voted but NEVER which candidates.** The `election_vote.cast` audit entry contains `{"method": "electronic"}` only.

7. **`has_voted()` is the ONLY normal-path query on `ballot_envelopes`.** It uses EXISTS (returns boolean only, not row data). It checks `(member_id, proposal_id)` to prevent duplicate votes.

### Enforcement Gaps (CR-02 in parent SDD)

There is no automated enforcement of rules 3-7. A developer could write a SQLAlchemy query like `BallotEnvelope.query.join(Ballot).all()` and it would execute successfully. The `BallotEnvelope` model is importable from `cove.models.governance` by any module.

---

## Vote Casting Transaction

The `cast_election_vote()` function in `election_services.py` is the only code path that writes ballot data. It executes as a single atomic transaction:

```
Step  1: Validate proposal exists, type='election', status='open'
Step  2: Validate candidate selections (non-empty, count <= seats, no duplicates)
Step  3: Validate all candidates exist, belong to this election, not withdrawn
Step  4: Validate member eligibility (voting_weight > 0, membership_status == 'active')
Step  5: Re-authenticate via check_password_hash(member.password_hash, password)
Step  6: Check has_voted(member.id, proposal_id) returns False
Step  7: CREATE Ballot (anonymous -- proposal_id, vote='election', method='electronic')
Step  8: db.session.flush() to obtain ballot.id
Step  9: CREATE ElectionChoice rows (one per candidate -- ballot_id + candidate_id, NO member_id)
Step 10: ATOMIC INCREMENT Candidate.vote_count for each selected candidate
Step 11: ATOMIC INCREMENT Proposal.yes_count (repurposed as total_ballots_cast)
Step 12: CREATE BallotEnvelope (ballot_id, member_id, proposal_id, sealed_at)
Step 13: AUDIT (records member.id + method, never candidate selections)
Step 14: db.session.commit()
```

If any step raises an exception, the entire transaction rolls back. Steps 7-12 are the critical section where the anonymous ballot, its choices, the vote count increments, and the sealed envelope are all created atomically.

### Transaction Isolation Concern

The current code uses SQLAlchemy's default transaction isolation (READ COMMITTED in PostgreSQL). Steps 10-11 use `table.update().values({col: col + 1})` which is an atomic increment at the SQL level. However, two concurrent voters could theoretically interleave their transactions. For an 81-lot HOA with elections lasting 30 days, this is not a practical concern. For larger deployments, SERIALIZABLE isolation or explicit row locking on candidate vote_count updates would be advisable.

---

## Chain Hash Integrity

### Current Implementation

`Ballot.chain_hash` is a `String(100)` nullable column intended for SHA-256 hash anchoring. In the current code:

- **The field exists in the schema** but `cast_election_vote()` does not populate it
- No hash is computed during vote casting
- No blockchain or Merkle tree integration exists
- `Proposal.chain_tx_hash` (for blockchain anchoring of certified results) is also unpopulated

### Intended Design

The chain hash is meant to create a tamper-evident log of ballots:

```
ballot_1.chain_hash = SHA-256(ballot_1.id + ballot_1.proposal_id + ballot_1.cast_at)
ballot_2.chain_hash = SHA-256(ballot_2.id + ballot_2.proposal_id + ballot_2.cast_at + ballot_1.chain_hash)
...
```

This would allow verification that no ballots were inserted, deleted, or modified after casting. The `Proposal.chain_tx_hash` would anchor the final chain hash to an external source of truth.

### Implementation Status: Not Started

See Code Review Findings CR-BS-03 below.

---

## Inspector Role

### Access Model

The `Member.is_inspector` property (role check, not a column) identifies members with the inspector role. In the RLS model:

- Inspectors access `ballot_envelopes` via a separate database connection using the `cove_inspector` role
- Inspectors can confirm ballot receipt and validate envelope counts
- Inspectors cannot reconstruct vote choices from envelopes alone (choice data is on the anonymous `ballot` side, linked via `ballot_id`)

### What the Inspector Can Do

1. Verify that `ballot_envelopes` count matches `Proposal.yes_count` for a given election
2. Confirm that a specific member's envelope exists (ballot receipt verification)
3. Access `ballot_id` values -- but without joining to `election_choices` (which the inspector role has no special access to), the inspector cannot determine which candidates a member voted for

### What the Inspector Cannot Do (By Design)

1. The inspector cannot modify ballot or envelope records (SELECT only, no UPDATE/DELETE grants)
2. The inspector cannot determine vote content without a separate query joining `ballot_id -> election_choices -> candidates`, which requires access to the `ballots` and `election_choices` tables. These tables have no RLS restrictions (they contain no PII), but the application should not provide a UI or API that performs this join for the inspector.

### Inspector Connection Not Implemented

There is currently no mechanism in the Flask application to switch database connections based on the inspector role. All queries run through the `growdirect` superuser connection. See CR-BS-01 below.

---

## Operations

### Startup Requirements

1. Migration `c3a1f9b2d4e7` must be applied
2. `cove_app` and `cove_inspector` PostgreSQL roles must exist
3. Flask application must connect as `cove_app` in production (currently connects as `growdirect` -- **gap**)

### Failure Modes

| Failure | Impact | Behavior |
|---------|--------|----------|
| RLS policies dropped | Ballot-voter link exposed to application queries | **Davis-Stirling violation** -- election results may be legally challenged |
| `cove_inspector` role deleted | Inspector cannot verify ballots | Election certification may be blocked |
| `cove_app` role has SELECT on envelopes | Application code can read voter-ballot links | Silent compliance failure |
| `ballot_envelopes` table corrupted | Duplicate vote prevention (`has_voted()`) fails | Members could vote multiple times |

### Monitoring

| Check | Method | Frequency |
|-------|--------|-----------|
| RLS enabled on `ballot_envelopes` | Query `pg_class.relrowsecurity` | Startup + daily |
| Expected policies exist | Query `pg_catalog.pg_policies` | Startup + daily |
| `cove_app` role has no SELECT on `ballot_envelopes` | Query `information_schema.role_table_grants` | Startup |
| Envelope count matches ballot count per election | `SELECT COUNT(*) FROM ballot_envelopes WHERE proposal_id = X` vs `Proposal.yes_count` | After each election close |

---

## Deployment

Ballot security is not a separate deployable -- it runs inside the Cove Flask container. However, it has production deployment requirements beyond the standard Cove deployment:

### Database Role Provisioning

In production (AWS RDS), the following must be provisioned before the first election:

```sql
-- Application role: INSERT only on envelopes
CREATE ROLE cove_app LOGIN PASSWORD '<from-secrets-manager>';
GRANT USAGE ON SCHEMA public TO cove_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO cove_app;
REVOKE SELECT ON ballot_envelopes FROM cove_app;
GRANT INSERT ON ballot_envelopes TO cove_app;

-- Inspector role: SELECT only on envelopes
CREATE ROLE cove_inspector LOGIN PASSWORD '<from-secrets-manager>';
GRANT USAGE ON SCHEMA public TO cove_inspector;
GRANT SELECT ON ballot_envelopes TO cove_inspector;

-- Force RLS even for table owner (defense in depth)
ALTER TABLE ballot_envelopes FORCE ROW LEVEL SECURITY;
```

### AWS Target Additions

| Component | Service | Notes |
|-----------|---------|-------|
| `cove_app` credentials | AWS Secrets Manager | Separate secret from admin connection |
| `cove_inspector` credentials | AWS Secrets Manager | Used only for inspector-role operations |
| RLS verification | CloudWatch custom metric | Alert if `relrowsecurity = false` |

---

## Code Review Findings

### CR-BS-01: No inspector-role database connection in Flask (P0)

**Severity:** P0 -- blocks production

**Description:** The Flask application has a single database connection (`DATABASE_URL`) used for all operations. There is no mechanism to execute queries as the `cove_inspector` role. The `Member.is_inspector` property exists but only controls UI access, not database-level access. An inspector-role member currently has no way to perform their verification duties through the application.

**Recommended fix:**
1. Create a second SQLAlchemy engine/session factory bound to the `cove_inspector` connection string
2. Add an inspector-specific query module (`cove/governance/inspector_queries.py`) that uses this session
3. Add inspector routes that use the inspector session for envelope verification
4. Store the `cove_inspector` connection string in a separate env var / Secrets Manager secret

**Linear issue:** GRO-xxx (to be created)

### CR-BS-02: `has_voted()` bypasses RLS intent (P1)

**Severity:** P1 -- before GA

**Description:** `has_voted()` performs an EXISTS query on `ballot_envelopes` to check for duplicate votes. This is necessary for correctness but contradicts the RLS design where `cove_app` has `USING (false)` on SELECT. In practice, since the app connects as superuser, this works. If the app is migrated to `cove_app`, this query will fail due to the `envelope_no_read` policy.

**Recommended fix:** Add a fourth RLS policy specifically for EXISTS checks:

```sql
CREATE POLICY envelope_exists_check ON ballot_envelopes
    FOR SELECT TO cove_app
    USING (
        -- Allow EXISTS checks but return minimal columns
        -- This policy must be carefully scoped
        current_setting('app.check_mode', true) = 'exists_only'
    );
```

Alternatively, implement `has_voted()` as a database function that runs with SECURITY DEFINER privileges, checking existence without exposing row data to the calling role.

**Linear issue:** GRO-xxx (to be created)

### CR-BS-03: Chain hash not implemented (P1)

**Severity:** P1 -- before GA

**Description:** `Ballot.chain_hash` and `Proposal.chain_tx_hash` columns exist but are never populated. The chain hash is documented as a tamper-evidence mechanism but no code computes or verifies it. Without chain hashing, there is no way to detect if ballot records are silently modified or deleted after casting.

**Recommended fix:**
1. Implement hash computation in `cast_election_vote()`: `SHA-256(ballot_id + proposal_id + cast_at + previous_ballot_chain_hash)`
2. Add a verification function that walks the chain and confirms integrity
3. Populate `Proposal.chain_tx_hash` at certification time with the final chain hash
4. Consider external anchoring (timestamped signature from a third-party service) for legal defensibility

**Linear issue:** GRO-xxx (to be created)

### CR-BS-04: No envelope count reconciliation (P2)

**Severity:** P2 -- post-launch

**Description:** There is no automated check that the number of `ballot_envelopes` for an election matches `Proposal.yes_count` (the repurposed ballot counter). A discrepancy would indicate either a transaction integrity failure or tampering.

**Recommended fix:** Add a reconciliation check in `certify_election()` that compares `BallotEnvelope.query.filter_by(proposal_id=X).count()` against `Proposal.yes_count`. Block certification if they differ.

**Linear issue:** GRO-xxx (to be created)

### CR-BS-05: No DELETE/UPDATE policies on ballot tables (P2)

**Severity:** P2 -- post-launch

**Description:** RLS policies only cover `ballot_envelopes`. The `ballots` and `election_choices` tables have no RLS policies at all. While these tables contain no PII (they are anonymous), unauthorized DELETE or UPDATE operations on them would corrupt election results. The `cove_app` role should have INSERT-only access to `ballots` and `election_choices` during elections.

**Recommended fix:** Add RLS policies or GRANT restrictions that prevent UPDATE and DELETE on `ballots` and `election_choices` for the `cove_app` role. Only a migration admin role should be able to modify these records.

**Linear issue:** GRO-xxx (to be created)

---

## Production Readiness Checklist

- [ ] Flask connects as `cove_app` role, not superuser (CR-BS-01, also CR-01 in parent)
- [ ] Inspector connection via `cove_inspector` role implemented (CR-BS-01)
- [ ] RLS policies enforced (not bypassed by superuser) -- `FORCE ROW LEVEL SECURITY` applied
- [ ] `has_voted()` works under `cove_app` role with scoped RLS policy (CR-BS-02)
- [ ] Chain hash computed and verified for ballot integrity (CR-BS-03)
- [ ] Envelope count reconciliation at certification (CR-BS-04)
- [ ] `ballots` and `election_choices` protected from UPDATE/DELETE (CR-BS-05)
- [ ] `cove_app` and `cove_inspector` credentials in AWS Secrets Manager
- [ ] RLS presence verified at startup (CR-05 in parent)
- [ ] Integration tests verify RLS enforcement with `cove_app` role
- [ ] `ballot_envelopes` cannot be joined to `election_choices` via application code (linting/test guard)
- [ ] No `member_id` column on `ballots` or `election_choices` (schema invariant test)
