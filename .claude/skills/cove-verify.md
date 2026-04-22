---
name: cove-verify
roles-primary:[Engineer]
stage: verify
description: |
  Verify work before claiming done. Use before committing, creating PRs, or
  claiming a feature works. Evidence before assertions — run checks, show output.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Cove Verify — Verification Before Completion

> Delegates to: `factory-verify` for standard verification gates.

Run the factory-verify skill, then apply the Cove-specific verification steps below.

**Announce:** "I'm using cove-verify to confirm [what]."

## Cove-Specific Verification

### Ballot Integrity Check (required if touching governance)

```bash
docker exec devops-cove-db-1 psql -U cove -d cove -c "
  SELECT column_name FROM information_schema.columns
  WHERE table_name = 'ballots' ORDER BY ordinal_position;"
```

Verify NO `member_id` column exists in the output.

### Route Verification (Cove ports)

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/
curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/auth/login
curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/member/dashboard
```

Note: Cove runs on port **5002** (not 5001 — that's Canary).

### Data Landing Check

```bash
docker exec devops-cove-db-1 psql -U cove -d cove -c "SELECT count(*) FROM <table>;"
```

Show count before, run operation, show count after.

### Davis-Stirling Compliance Check (if governance feature)

For each acceptance criterion involving governance:
- Which Civil Code section covers it?
- Is quorum calculated correctly for the proposal type?
- Is secret ballot separation preserved?
- Is the inspector-only RLS on `ballot_envelopes` intact?

State the compliance conclusion explicitly — do not leave it implicit.

---

*Cove Verify v1.0 — Verification Before Completion*
*Delegates to: factory-verify*
