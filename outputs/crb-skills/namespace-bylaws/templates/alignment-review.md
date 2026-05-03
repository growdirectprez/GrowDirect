# [NAMESPACE] Periodic Alignment Review — [REVIEW CYCLE / DATE]

**Review cycle:** [annual default; or on-demand]
**Review block height:** [BLOCK_NNNNNN]
**Reviewer / drafter:** [ordinal address(es); lineage tier]
**Bylaws version under review:** v[N] (ratified at block height [BLOCK_NNNNNN])

---

## Why this review

Per `reference/07-alignment-checks.md`, the namespace runs a periodic alignment review at the cadence specified in its bylaws (default: annually, anchored to the namespace's genesis-block anniversary). The review:

1. Runs all 23 alignment checks against the current ratified bylaws as-they-stand
2. Asks the trusted network: "are these still the right checks?"
3. Asks the trusted network: "are there failure modes we've encountered in operation that don't have a corresponding check yet?"
4. Produces this artifact as input to the next-cycle revision (per `reference/08-iteration-loop.md`)

This is how the bylaws self-correct over time. The substrate doesn't assume the original design was perfect; it assumes the trusted network learns and adjusts the checks as they learn.

## Operational context since last review

[Multi-paragraph narrative — what happened in the namespace since the last review. Notable events: ordinal mints, treasury actions above threshold, amendments ratified, phase transitions (if any), customer/contributor cohort changes. Specific incidents that surfaced potential alignment-check gaps. Specific successes that validate alignment-check coverage. Unfiltered.]

## Check-by-check results

For each of the 23 checks in `reference/07-alignment-checks.md`:

| Check | Category | Current result | Trend since last review | Notes |
| --- | --- | --- | --- | --- |
| 1 | A — Anti-extraction (value flow) | PASS / FAIL / FLAG | improving / stable / degrading | [observations from operation] |
| 2 | A — Anti-extraction (lineage dilution) | PASS / FAIL / FLAG | … | … |
| 3 | A — Anti-extraction (clawback) | PASS / FAIL / FLAG | … | … |
| 4 | A — Anti-extraction (vesting cliff) | PASS / FAIL / FLAG | … | … |
| 5 | B — Customer-data sovereignty (cross-customer sharing) | PASS / FAIL / FLAG | … | … |
| 6 | B — Customer-data sovereignty (resale) | PASS / FAIL / FLAG | … | … |
| 7 | B — Customer-data sovereignty (post-departure access) | PASS / FAIL / FLAG | … | … |
| 8 | C — Trusted-network integrity (lineage bypass) | PASS / FAIL / FLAG | … | … |
| 9 | C — Trusted-network integrity (untrusted acquirers) | PASS / FAIL / FLAG | … | … |
| 10 | C — Trusted-network integrity (consolidation beyond tier) | PASS / FAIL / FLAG | … | … |
| 11 | D — Phase integrity (founder-mint extension) | PASS / FAIL / FLAG | … | … |
| 12 | D — Phase integrity (founder permanent authority) | PASS / FAIL / FLAG | … | … |
| 13 | D — Phase integrity (genesis-stake retroactive removal) | PASS / FAIL / FLAG | … | … |
| 14 | E — Compliance integrity (PCI scope) | PASS / FAIL / FLAG | … | … |
| 15 | E — Compliance integrity (ISO 27001) | PASS / FAIL / FLAG | … | … |
| 16 | E — Compliance integrity (SOC 2) | PASS / FAIL / FLAG | … | … |
| 17 | E — Compliance integrity (department-free posture) | PASS / FAIL / FLAG | … | … |
| 18 | F — Voice and culture (SaaS marketing) | PASS / FAIL / FLAG | … | … |
| 19 | F — Voice and culture (operator-readable) | PASS / FAIL / FLAG | … | … |
| 20 | F — Voice and culture (work-as-play vs work-harder-for-free) | PASS / FAIL / FLAG | … | … |
| 21 | G — Founder/seller-team (lineage stake protection) | PASS / FAIL / FLAG | … | … |
| 22 | G — Founder/seller-team (HR-as-PE-culling) | PASS / FAIL / FLAG | … | … |
| 23 | G — Founder/seller-team (invitation friction) | PASS / FAIL / FLAG | … | … |

**Aggregate:** [N] PASS, [N] FAIL, [N] FLAG.

## Trusted-network responses

The drafter circulated the check results to the trusted network via the iteration loop (per `reference/08-iteration-loop.md`). Comments received:

| Commenter (ordinal address) | Lineage tier | Comment shape | Targeted check | Comment summary | Resolution status |
| --- | --- | --- | --- | --- | --- |
| `[bc1q...]` | 0 | concern | 11 | [summary] | [open / addressed / deferred / overridden] |
| `[bc1q...]` | 1 | suggestion | 18 | [summary] | … |
| … | … | … | … | … | … |

Full comment ledger entries: see `templates/comment-ledger.md` cycle [N].

## New failure modes surfaced

[List of failure modes the trusted network identified during the review that are not yet captured in `reference/09-anti-patterns.md`. For each: name, description, proposed structural correction (if any), proposed alignment check (if any).]

| New failure mode | Description | Proposed correction | Proposed check |
| --- | --- | --- | --- |
| [name] | [description] | [substrate mechanism that would prevent it; cross-ref existing reference doc if applicable] | [specific yes/no question for the alignment-check harness] |

If any new failure modes are accepted by the trusted network, they enter the next-cycle bylaws revision as proposed additions to `reference/09-anti-patterns.md` and corresponding new entries in `reference/07-alignment-checks.md`. The additions themselves go through the amendment process (per `templates/amendment-proposal.md`).

## Recommendations for next-cycle revision

[Drafter's synthesis of the review findings into specific revision recommendations. Reference the comment-ledger entries that motivate each recommendation. Note which recommendations require structural-amendment threshold vs. operational-amendment threshold per `reference/04-lineage-weighted-voting.md`.]

| Recommendation | Targeted bylaws clause | Required threshold | Cross-reference |
| --- | --- | --- | --- |
| [description] | [Article N, Section M] | [operational / structural / founder-mint authority] | [comment-ledger entry, anti-pattern doc reference, etc.] |

## Open items requiring trusted-network discussion

[Items the drafter cannot resolve unilaterally and that need broader discussion before next-cycle drafting. These become discussion-period agenda items per `reference/08-iteration-loop.md`.]

## Block-height anchor

This alignment review artifact is inscribed at block height [BLOCK_NNNNNN]. The content hash `[hex_hash]` becomes the canonical reference for the review cycle. Subsequent amendments referencing this review cite the hash above.

## Cross-references

- `reference/07-alignment-checks.md` — the 23 checks run above
- `reference/08-iteration-loop.md` — the iteration mechanics for next-cycle revisions
- `reference/09-anti-patterns.md` — the failure-mode list this review may add to
- `templates/comment-ledger.md` — the comment-tracking artifact for the trusted network's responses
- `templates/amendment-proposal.md` — the proposal artifact for next-cycle revisions

---

*Periodic alignment review for [NAMESPACE]. Inscribed at block height [BLOCK_NNNNNN].*
