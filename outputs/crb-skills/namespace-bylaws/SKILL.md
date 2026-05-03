---
name: namespace-bylaws
description: Generate, iterate, and ratify bylaws for a namespace (a discrete governance domain — a venture, a vertical, a partner-licensed substrate) running on the eljeffe Hash and Seal Protocol. Produces a two-layer bylaws document (cultural-layer reading like a 1963 nonprofit charter modernized, technical-layer reading like a protocol specification), supporting templates (genesis record, amendment proposal, alignment review, comment ledger), and an alignment-check harness that fires on every revision.
trigger phrases:
  - "draft bylaws for [namespace]"
  - "draft a namespace bylaws document"
  - "generate the genesis record"
  - "amendment proposal for [namespace]"
  - "alignment review for [namespace]"
  - "open the comment ledger"
  - "ratify bylaws v[N]"
  - "run the alignment checks"
  - "what would the bylaws look like for [venture]"
status: complete (9/9 reference docs + 5 templates)
---

# namespace-bylaws — skill entry point

The substrate runs on bylaws. This skill produces them.

## What this skill exists for

Every namespace this platform spawns — a venture, a vertical, a partner-licensed substrate, a customer cohort with DAO governance — needs a bylaws document. Without one, the substrate has no rules; with the wrong one, the substrate quietly reintroduces the failure modes the architecture was built to prevent.

This skill produces bylaws that:

- Read in plain operator language — recognizable to a non-technical member on a single read; no jargon, no theater
- Specify the substrate primitives precisely — lineage-weighted voting, DAO-action stamping, treasury mechanics, phase transitions, alignment checks
- Cross-reference both layers explicitly — every cultural clause has a technical counterpart; every technical mechanism has a cultural rationale
- Encode the corrections to prior-run failure modes structurally — not as flavor text in a values section
- Iterate cleanly through the comment-and-revision loop — every comment lineage-tracked, every revision block-height-anchored, every ratified version inscribed

## When to invoke

- A new namespace is being formed (the founder is preparing the genesis block; bylaws v1 must exist before genesis inscription per `02-genesis-ordinal-mechanics.md`)
- A namespace's bylaws need amendment (a clause is no longer fit; a new failure mode has surfaced; a phase transition is approaching)
- An alignment review is due (annually by default per `07-alignment-checks.md`; or on-demand when the trusted network requests one)
- A second namespace is being spun up and the founder wants the bylaws scaffolded against the canonical structure with namespace-specific tuning

## How the skill operates

1. **Read the canonical reference set first.** The 9 reference documents in `reference/` are the substrate's load-bearing knowledge. Do not draft bylaws against memory; draft against the references.
2. **Identify the namespace's specifics.** Genesis-tier holder set, lineage-decay coefficient (default α = 0.5), phase-1 duration (default 18 months from genesis), treasury thresholds, transfer rules, fiscal-year choice. The templates have explicit fields for each.
3. **Produce the two-layer bylaws document.** Cultural layer plain; technical layer precise. Use `templates/bylaws-document.md` as the structure.
4. **Run the alignment checks.** All 23 from `reference/07-alignment-checks.md`; the appendix lists pass/fail per check.
5. **Open the comment ledger** if the bylaws are entering the iteration loop. Use `templates/comment-ledger.md`.
6. **For amendments**, use `templates/amendment-proposal.md` and re-run alignment checks against the proposed delta.
7. **For the genesis moment**, capture the namespace's birth in `templates/namespace-genesis-record.md` and inscribe the bylaws v1 hash + the namespace identifier on the chosen genesis block.

## Voice and posture (non-negotiable)

- **Two-layer discipline.** Cultural-layer clauses read like operator language. Technical-layer clauses read like protocol specification. Both are present for every clause; neither is decoration. See `reference/06-cultural-technical-mapping.md`.
- **Ranch-test enforced.** Every cultural-layer clause: would a 60-year-old gun-store owner or third-generation rancher recognize it on a single read? If not, rewrite.
- **No SaaS-marketing copy.** No "best-in-class," no "industry-leading," no "comprehensive solution." Operator language. Plain numbers. Plain consequences.
- **No theater language in the values section.** Liberty / Justice / The American Way appear plainly when they appear; never as decoration.
- **Anti-extraction is structural, not a bullet point.** The substrate enforces the principle by construction. The bylaws name what the substrate enforces, not what the bylaws aspire to.
- **Every clause cross-references its layer counterpart and the relevant reference doc.** No floating clauses; no "see appendix A" without a specific anchor.

## Reference contents

| File | Purpose |
| --- | --- |
| `reference/01-shore-club-lineage.md` | The 1963 Abalone Shore Club bylaws Article-by-Article, with modern equivalents |
| `reference/02-genesis-ordinal-mechanics.md` | Substrate primitives (genesis block, ordinals, lineage tracking, DAO-action stamping, founder-mint authority, transfer rules) |
| `reference/03-dao-treasury-patterns.md` | Treasury mechanics (categorized cash-out, approval thresholds, multi-sig, transparency-by-default, reserve, appreciation) |
| `reference/04-lineage-weighted-voting.md` | Voting formula `w(d) = 1 / (1 + α·d)`, quorum mechanics, vote types, edge cases |
| `reference/05-phase-transitions.md` | Four-phase progression (pre-genesis → founder-mint → DAO-ratified → multi-vertical/network) |
| `reference/06-cultural-technical-mapping.md` | Two-layer mapping table; layer divergence handling |
| `reference/07-alignment-checks.md` | 23 self-questioning prompts across 7 categories; how the checks fire on revisions |
| `reference/08-iteration-loop.md` | Comment-and-revision loop; comment shapes; drafter mechanics; Cove as reference proposal engine |
| `reference/09-anti-patterns.md` | Prior-run failure modes named explicitly; structural corrections cross-referenced |

## Template contents

| File | Purpose |
| --- | --- |
| `templates/bylaws-document.md` | The primary deliverable — Articles I-XIV in two-layer form, namespace-specific fields fillable |
| `templates/namespace-genesis-record.md` | The namespace's birth-event record — block height, founding ordinals, bylaws v1 hash, founding-cohort roster |
| `templates/amendment-proposal.md` | The amendment-proposal artifact — clause delta, rationale, alignment-check results |
| `templates/alignment-review.md` | The periodic-review artifact — all 23 checks against current bylaws state, trusted-network responses |
| `templates/comment-ledger.md` | The comment-tracking artifact — per-comment provenance, resolution status, revision linkage |

## Quality bar — the second-namespace test

After running this skill against the first namespace, run it against a synthetic second namespace with different specifics (different lineage-decay coefficient, different phase-1 duration, different treasury thresholds, different fiscal-year choice). If anything required modifying the skill scaffold to accommodate it, the skill is not done. Specifics live in the per-namespace bylaws output; the skill stays target-agnostic.

## Cross-references

- The eljeffe Hash and Seal Protocol — formal substrate name; bylaws are the governance specification; substrate is the technical foundation
- Wyoming DAO LLC statute — Wyo. Stat. Ann. § 17-31-101 et seq.; the legal substrate that gives the bylaws regulatory standing
- Cove (Python/Flask proposal engine; currently running WPBCA HOA governance under Davis-Stirling Act) — the reference implementation of the iteration loop specified in `reference/08-iteration-loop.md`; per company-formation epic dispatch C6
- Company-formation epic — `outputs/session-summary-and-company-formation-epic.md`; this skill produces the C1 deliverable

---

*The substrate runs on bylaws. This skill produces them.*
