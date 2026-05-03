# [NAMESPACE] Bylaws Amendment Proposal — [PROPOSAL ID / SHORT NAME]

**Drafter:** [ordinal address(es); lineage tier]
**Proposal block height:** [BLOCK_NNNNNN]
**Discussion-period close:** [BLOCK_NNNNNN ≈ proposal_block + 14 days]
**Vote-period close:** [BLOCK_NNNNNN ≈ discussion_close + 7 days]
**Bylaws version targeted:** v[N] → proposed v[N+1]
**Amendment scope:** [operational / treasury threshold / structural / founder-mint authority]
**Required threshold:** [simple majority / super-majority / structural-amendment threshold / founder-consent + structural threshold]
**Required quorum:** [30% / 40% / 50% / 67%]

---

## Summary

[One-paragraph statement of what this proposal changes and why. Plain language, ranch-tested. The trusted network reads this paragraph first; the rest of the document supports it.]

## The clause delta

### Before (current bylaws v[N])

> [Verbatim quote of the current cultural-layer clause(s) being amended]

> [Verbatim quote of the current technical-layer clause(s) being amended]

### After (proposed bylaws v[N+1])

> [Verbatim text of the proposed cultural-layer clause(s)]

> [Verbatim text of the proposed technical-layer clause(s)]

### Diff (machine-readable)

```diff
- [removed line from cultural layer]
+ [added line to cultural layer]
```

```diff
- [removed line from technical layer]
+ [added line to technical layer]
```

## Rationale

[Multi-paragraph explanation of why this change. Reference the specific failure mode being prevented (cite `reference/09-anti-patterns.md`) or the specific operational gap being closed. If the change responds to comments from the trusted network, cross-reference the comment-ledger entries that informed it.]

## Alignment-check results

Per `reference/07-alignment-checks.md`, the 23 checks are run against the proposed delta. Results below.

| Check | Category | Result | Notes |
| --- | --- | --- | --- |
| 1 | A — Anti-extraction (value flow) | PASS / FAIL / N/A | [if FAIL: specific reason; override rationale or proposed correction] |
| 2 | A — Anti-extraction (lineage dilution) | PASS / FAIL / N/A | … |
| 3 | A — Anti-extraction (clawback) | PASS / FAIL / N/A | … |
| 4 | A — Anti-extraction (vesting cliff) | PASS / FAIL / N/A | … |
| 5 | B — Customer-data sovereignty (cross-customer sharing) | PASS / FAIL / N/A | … |
| 6 | B — Customer-data sovereignty (resale) | PASS / FAIL / N/A | … |
| 7 | B — Customer-data sovereignty (post-departure access) | PASS / FAIL / N/A | … |
| 8 | C — Trusted-network integrity (lineage bypass) | PASS / FAIL / N/A | … |
| 9 | C — Trusted-network integrity (untrusted acquirers) | PASS / FAIL / N/A | … |
| 10 | C — Trusted-network integrity (consolidation beyond tier) | PASS / FAIL / N/A | … |
| 11 | D — Phase integrity (founder-mint extension) | PASS / FAIL / N/A | … |
| 12 | D — Phase integrity (founder permanent authority) | PASS / FAIL / N/A | … |
| 13 | D — Phase integrity (genesis-stake retroactive removal) | PASS / FAIL / N/A | … |
| 14 | E — Compliance integrity (PCI scope) | PASS / FAIL / N/A | … |
| 15 | E — Compliance integrity (ISO 27001) | PASS / FAIL / N/A | … |
| 16 | E — Compliance integrity (SOC 2) | PASS / FAIL / N/A | … |
| 17 | E — Compliance integrity (department-free posture) | PASS / FAIL / N/A | … |
| 18 | F — Voice and culture (SaaS marketing) | PASS / FAIL / N/A | … |
| 19 | F — Voice and culture (operator-readable) | PASS / FAIL / N/A | … |
| 20 | F — Voice and culture (work-as-play vs work-harder-for-free) | PASS / FAIL / N/A | … |
| 21 | G — Founder/seller-team (lineage stake protection) | PASS / FAIL / N/A | … |
| 22 | G — Founder/seller-team (HR-as-PE-culling) | PASS / FAIL / N/A | … |
| 23 | G — Founder/seller-team (invitation friction) | PASS / FAIL / N/A | … |

**Overall result:** [PASS / FAIL]
**FAIL count:** [N]
**Failures requiring override-or-correction before ratification:** [list]

## Proposal-impact analysis

If ratified, this proposal:

- **Affects clauses in Articles:** [list — Article numbers]
- **Affects substrate primitives:** [yes/no; if yes, which — voting formula, mint authority, treasury thresholds, phase transitions]
- **Affects compliance posture:** [yes/no; if yes, which audit frameworks — PCI / ISO 27001 / SOC 2]
- **Affects member economics:** [yes/no; if yes, which — token-earn rate, treasury distribution rules, transfer rules]
- **Requires smart-contract redeployment:** [yes/no; if yes, deployment block height target]

## Cross-references

- `reference/07-alignment-checks.md` — the 23 checks run above
- `reference/08-iteration-loop.md` — the iteration loop this proposal is operating within
- `reference/09-anti-patterns.md` — the failure modes any proposed amendment must not reintroduce
- `templates/comment-ledger.md` — the comment-ledger entries from prior bylaws cycles that informed this proposal
- Bylaws v[N] (the version being amended) at `[path or IPFS reference]`

---

*Amendment proposal for [NAMESPACE] bylaws v[N] → v[N+1]. Inscribed at block height [BLOCK_NNNNNN].*
