---
name: cove-blueprint
roles-primary:[Architect]
roles-assist:[ALX]
stage: blueprint
description: |
  Factory Process plan-writing skill for Cove governance platform. Use when you
  have a GRO issue or Jeffe directive for a multi-step task — before touching
  code. Creates implementation plans with Davis-Stirling compliance checks,
  ballot integrity flags, and APN chain verification.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Edit
  - Write
  - TodoWrite
---

# Cove Blueprint — Factory Process Plan Writing

> Delegates to: `factory-blueprint` for standard plan structure.

Run the factory-blueprint skill, then apply the Cove-specific additions below.

**Announce at start:** "I'm using cove-blueprint to write the Factory Process implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Cove-Specific Additions

### Cove UUID Warning

Every existing Cove table uses `String(36)` UUIDs. This is a **historical holdover** — do NOT copy this pattern. All new tables must use `Mapped[uuid.UUID]` per platform standard. New FKs pointing to existing Cove tables use `String(36)` for compatibility only — document this as tech debt in the plan.

### Compliance Pre-Flight

Before writing the plan, check Davis-Stirling compliance if this feature touches governance:

```
-> Which Davis-Stirling sections apply?
-> Does it affect secret ballot separation (ballots.member_id must stay absent)?
-> Does it change quorum calculations?
   - General business: 1/3 of members
   - Assessment increase: 1/2 of members
   - Secret ballot votes: NO quorum required (§5.9)
-> Does it touch ballot_envelopes (PostgreSQL RLS — inspector-only)?
-> Does it affect the APN chain: Parcel (APN) -> Member -> Vote?
```

### APN Chain Check

Every new entity must connect back to a parcel via APN. Verify:

```
-> Does every new entity connect back to a parcel via APN?
-> Are lookups APN-first, address-second, member-name-third?
-> Does the lot email derive correctly from the parcel?
```

### Cove Plan Header Addition

Add to the standard factory plan header:

```markdown
**Compliance:** [Davis-Stirling sections affected, if any]
**APN Impact:** [How this connects to parcel data]
```

### Ballot Integrity Flag

If the plan touches vote data:

```
BALLOT INTEGRITY: This plan touches vote data.
- ballots table has NO member_id — verify this is preserved
- ballot_envelopes are sealed (RLS) — verify access controls
- One vote per member per proposal — verify UNIQUE constraint
- INSERT-only on vote tables — no UPDATE, no DELETE
```

### Quality Checklist Additions

- [ ] Davis-Stirling compliance checked (if governance-related)
- [ ] APN chain verified for new entities
- [ ] Ballot integrity flag added (if touching governance)
- [ ] File paths use `cove/` prefix
- [ ] Commits reference GRO issue number

---

*Cove Blueprint v1.0 — Factory Process Plan Writing*
*Delegates to: factory-blueprint*
