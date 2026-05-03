# [NAMESPACE] Comment Ledger — Cycle [N]

**Cycle definition:** Comment-collection cycle for bylaws version v[N] (ratified at block height [BLOCK_NNNNNN]) → proposed v[N+1].
**Cycle opened at block height:** [BLOCK_NNNNNN]
**Cycle closes at:** [block height when next discussion period opens]
**Drafter for v[N+1]:** [ordinal address(es); lineage tier; or "open — multiple drafters may submit competing revisions"]

---

## Purpose

Per `reference/08-iteration-loop.md`, comments are the input to bylaws revisions. This ledger captures every comment from the trusted network, in five defined shapes (question / suggestion / concern / counter-proposal / veto-flag), with full provenance. The drafter for v[N+1] reads this ledger when synthesizing the next-version proposal.

The ledger is append-only. Comments are immutable once submitted; corrections are new comments referring back. Resolution status is updated as the drafter (or relevant ordinal-holder) responds.

## How to add a comment

1. Sign your comment with your ordinal's auth-token via the smart-contract comment function
2. The smart contract appends your comment to this ledger with full provenance metadata
3. The drafter (or relevant ordinal-holder) responds in due course; resolution status updates accordingly
4. If your comment is a veto-flag (invocation of a specific alignment-check failure), the relevant proposal cannot proceed to vote without addressing or explicitly overriding

## Comment entries

### Comment #1

| Field | Value |
| --- | --- |
| Block height submitted | [BLOCK_NNNNNN] |
| Block hash | `[hex_hash]` |
| Commenter ordinal address(es) | `[bc1q...]` |
| Commenter lineage tier | [0 / 1 / 2 / …] |
| Auth-token signature | `[hex_sig]` |
| Comment shape | [question / suggestion / concern / counter-proposal / veto-flag] |
| Targeted clause | [Article N, Section M; or "Article XIV — amendment process generally"; or "alignment check 18"] |
| Comment text | [verbatim — do not smooth] |
| Resolution status | [open / addressed-in-revision / deferred / overridden / withdrawn] |
| Resolution provenance | [drafter response, signed by drafter ordinal; or pending; or override-vote provenance if overridden] |
| Resolution block height | [BLOCK_NNNNNN if resolved; else blank] |

### Comment #2

[Repeat structure for each subsequent comment.]

### Comment #3

[…]

---

## Comment shapes — guidance for commenters

Per `reference/08-iteration-loop.md`:

**Question.** "Why does Article VII Section 3 specify a 30% reserve and not 20%?" Seeking rationale, not requesting a change. Resolution: drafter or relevant ordinal-holder responds with rationale.

**Suggestion.** "Article XI's per-period discretionary cash-out cap should be raised from $5k to $10k for tier-1 contributors." Proposed change with specific delta. Resolution: drafter evaluates, may incorporate into next revision.

**Concern.** "Article IV's quorum threshold of 30% is too low; small motivated factions could ratify proposals that broader membership would reject." Flagged risk. Resolution: surfaces an alignment-check failure case if applicable; drafter addresses in next revision or explicitly defers with rationale.

**Counter-proposal.** "Replace Article V Section 2 entirely with the following text: …" Full alternative clause. Resolution: drafter compares vs. status quo; if alternative is preferred or incorporates legitimate concern, becomes the revised clause.

**Veto-flag.** "This revision breaks anti-extraction principle as defined in alignment-check A.1." Invocation of alignment-check failure. Resolution: revision is automatically flagged and cannot proceed to vote without addressing or explicit override. The override is itself a governance event recorded on chain.

## Drafter mechanics for next-version

The drafter for v[N+1]:

1. Reads this entire comment ledger for cycle [N]
2. Synthesizes comments into a proposed revision per `templates/amendment-proposal.md`
3. Runs the alignment checks per `reference/07-alignment-checks.md`
4. Submits the revision artifact to the trusted network for the discussion period
5. May revise in response to discussion-period comments (each revision-of-revision gets its own block-height stamp)
6. The vote period opens after discussion closes per `reference/08-iteration-loop.md`

If multiple drafters submit competing revisions, all enter the discussion period independently. The trusted network votes on which to ratify; ties are resolved by block-height precedence.

## Failed-revision handling

A failed revision (one that didn't reach ratification threshold) goes back to the comment ledger as a non-ratified proposal. Commenters' positions are preserved. A subsequent drafter can use the vote-counts and the comment ledger together to produce a revision that addresses the blocking concerns.

Failed revisions are not erased; they remain in the immutable history.

## Block-height anchor

This comment ledger artifact is inscribed at the cycle's opening block height; updated on each comment addition (each update is a new inscription with a back-reference to the previous version's hash). At cycle close, the ledger is finalized and the canonical hash is referenced in the resulting `templates/amendment-proposal.md`.

## Cross-references

- `reference/08-iteration-loop.md` — the iteration loop these comments operate within
- `reference/07-alignment-checks.md` — the alignment checks veto-flag comments invoke
- `reference/09-anti-patterns.md` — the failure modes the trusted network watches for during commenting
- `templates/amendment-proposal.md` — the artifact the drafter produces from this ledger
- `templates/alignment-review.md` — the periodic review that may add entries here

---

*Comment ledger for [NAMESPACE] cycle [N]. Inscribed at block height [BLOCK_NNNNNN]; updated through cycle close at [BLOCK_NNNNNN].*
