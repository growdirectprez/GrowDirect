---
name: cove-quorum
roles-primary: [Compliance]
roles-assist: [Legal]
description: |
  Calculate quorum requirements for WPBCA governance votes. Given a proposal type
  and optional member count, returns quorum needed, approval threshold, secret ballot
  requirement, notice period, and bylaw citations. Covers all 7 vote types plus
  reconvened elections (AB 2460) and acclamation (AB 502).
---

# cove-quorum — Quorum Calculator

> Layer 2 skill — Cove domain (HOA governance)

## When to use

- Any question about quorum requirements for a WPBCA vote
- Calculating whether a meeting has quorum
- Determining approval thresholds for a proposal
- Checking if an election qualifies for acclamation (AB 502)
- Verifying secret ballot requirements
- Computing reconvened election quorum (AB 2460)

## Source material

- `Cove/cove/governance/wpbca-bylaws-config.json` — authoritative governance rules
- `Cove/cove/governance/quorum.py` — QuorumCalculator module
- WPBCA Bylaws §5.9, §6.6, §8.9, §8.20, §9.13, §13.2, §18.1
- AB 502 (2022), AB 2159 (2024), AB 2460 (2024)

## How to calculate

### Step 1: Identify proposal type

| Type | Description | Bylaw § |
|------|-------------|---------|
| `resolution` | General business resolution | §9.1-9.15 |
| `bylaw_amendment` | Amend association bylaws | §18.1 |
| `ccr_amendment` | Amend CC&Rs (Declaration) | §4270-4275 |
| `election` | Board of Directors election | §8.9 |
| `operating_rule` | Operating rule adoption | §4340-4370 |
| `special_assessment` | Special assessment requiring vote | §13.2 |
| `director_removal` | Remove a board director | §8.20 |

### Step 2: Look up quorum rules

| Action | Quorum | Threshold | Secret Ballot | Notice |
|--------|--------|-----------|---------------|--------|
| Resolution | 1/3 (27 of 81) | Majority (50%) | No | 4 days |
| Bylaw amendment | None (§5.9) | Majority (50%) | Yes | 28 days |
| CC&R amendment | None (§5.9) | Supermajority (67%) | Yes | 28 days |
| Election | None (§5.9) | Plurality | Yes | 28 days |
| Operating rule | Board only | Board majority | No | 28 days |
| Special assessment | 1/2 (41 of 81) | Majority (50%) | Yes | 28 days |
| Director removal | 1/3 (27 of 81) | Majority (50%) | Yes | 35 days |

### Step 3: Check special conditions

- **Reconvened election (AB 2460):** If original election fails quorum, reconvened
  meeting drops to 20% (17 of 81 lots).
- **Acclamation (AB 502):** If candidates ≤ seats, election decided without ballot.
- **Electronic voting (AB 2159):** Members may opt into electronic ballots for all
  secret ballot votes EXCEPT special assessments.

### Step 4: Calculate votes needed

"Majority" means strictly more than half (§5.14):
- 50 members present, 50% threshold → need 26 yes votes (floor(50 × 0.5) + 1)
- Plurality (elections): highest vote count wins, no minimum

## Key citations

- **§5.9:** "A quorum is not required for votes with respect to which use of
  written secret ballot procedures... are mandatory pursuant to Civil C. 1363.03."
- **§6.6.1.a:** Assessment quorum = "a majority of the Members"
- **§6.6.1.c:** General quorum = "one third of the Members"
- **§9.13:** Board quorum = "a majority of the number of directors authorized"
- **AB 2460:** Reconvened election quorum = 20%

## Output format

When answering a quorum question, always include:

1. **Quorum needed** — exact number of members (e.g., "27 of 81 lots")
2. **Approval threshold** — percentage and meaning (e.g., "50% — majority of quorum")
3. **Secret ballot** — yes/no and why
4. **Notice period** — days required
5. **Bylaw citation** — exact section number
6. **Legislative compliance** — any applicable AB/SB laws

## Python module

The `QuorumCalculator` class in `Cove/cove/governance/quorum.py` implements all
calculations. It reads from `wpbca-bylaws-config.json` — no hardcoded values.

```python
from cove.governance.quorum import QuorumCalculator

calc = QuorumCalculator(total_lots=81)

# Basic quorum check
result = calc.calculate("election")
# result.quorum_needed → 0 (secret ballot, §5.9)
# result.requires_secret_ballot → True
# result.electronic_eligible → True (AB 2159)

# With members present
result = calc.calculate("special_assessment", members_present=50)
# result.quorum_met → True (50 >= 41)
# result.votes_needed_to_pass → 26

# Reconvened election
result = calc.calculate("election", reconvened=True)
# result.quorum_needed → 17 (AB 2460, 20% of 81)

# Board meeting
result = calc.calculate_board_quorum()
# result.quorum_needed → 3 (majority of 5)

# Acclamation check
result = calc.check_acclamation(candidates=3, seats=5)
# result.acclamation → True (AB 502)
```
