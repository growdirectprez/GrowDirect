# Valuation Impact — RapidPOS LLC (Demo Run)

> **DEMO RUN — illustrative deal pricing math.** Numbers are placeholders; actual founder hypotheses will tighten this. Companion to `02-iso27001-gap-assessment.xlsx::valuation_impact` tab.

**Vendor:** RapidPOS LLC
**Run date:** 2026-05-03
**Phase:** 2-3 — Audit-as-diligence + valuation impact

---

## The deal pricing logic

Acquisition price = current-state value − cost we'll incur to make the asset productive − opportunity-cost cushion.

Anchor-account upside is *option value*, not in the base price.

## Inputs (placeholder)

From the hypothesis grid:
- **Annual revenue:** ~$3-6M (target-profile midpoint $4.5M)
- **EBITDA margin:** ~22% (midpoint of 20-25% range)
- **Current-state EBITDA:** $4.5M × 0.22 = **$990k**
- **Owner compensation in EBITDA:** Yes (founder-owned operator). For valuation, *adjusted EBITDA* deducts replacement-CEO comp. Assume $250k replacement comp → adjusted EBITDA = $740k.

Founder Q1 will refine these. Worst case: real revenue is $3M and EBITDA is $400k. Best case: $6M revenue, $1.4M EBITDA.

## Multiple framing

| Framing | Multiple | Implied price (EBITDA $740k) |
| --- | --- | --- |
| Legacy SMB services VAR | 3-4x | $2.2M-$3.0M |
| Legacy specialty-retail VAR | 4-5x | $3.0M-$3.7M |
| Modernized retail platform | 6-10x | $4.4M-$7.4M |
| Platform-SaaS comparable | 8-15x ARR | $36M-$67M (if you call $4.5M revenue "ARR" — the seller might) |

Sellers like the bottom row. Buyers price toward the top row. The negotiation is which framing wins.

Our positioning: **"This is a legacy SMB specialty-retail VAR. We will pay 4.5x adjusted EBITDA, minus the cost we incur to modernize, plus a fair earnout for the customer continuity."**

## Formula 1 — gap-to-discount

ISO 27001 remediation total: ~$337k engineering + ~$150k ISMS framework / audit fees / surveillance = **~$487k all-in over 18 months**.

Compliance-pressure factor: 0.7 (moderate — specialty retail with growing pressure but not acute today).

```
discount_for_isms_gap = $487k × 0.7 = $341k
```

The seller absorbs ~$341k of the ISMS work as a price reduction. The rest (~$146k) is our investment in the asset's modernization.

## Formula 2 — modernization-premium offset

Seller might ask for the modernized-platform multiple ($4.4M-$7.4M range) because "look how good this could be after Growdirect modernizes it."

Our offset:
- Proposed modernized multiple: 7x (midpoint of 6-10x SaaS-ish range)
- Current-state multiple: 4.5x
- Multiple delta: 2.5x
- EBITDA: $740k
- Probability of modernization without us: 0.2 (seller has plans but no capital/team to execute solo)

```
modernization_premium_offset = ($740k × 2.5) × 0.2 = $370k
```

We deduct this from the ask. The seller cannot get credit for our future work.

## Formula 3 — opportunity cost of slow migration (worst-case stress)

If eager-cohort migration runs 6 months slower than expected:

- Eager-cohort current ARR: $900k
- Expansion multiple: 1.5x → $450k incremental ARR
- 6-month delay × 0.92 NPV factor = ~$207k delayed-revenue cost

This is the worst-case cushion. Subtract another **$207k** from our walking price for the worst-case scenario.

## Formula 4 — anchor-account upside (separate, not in base)

Y3 Global-50 anchor:
- Hypothetical anchor ARR: $50M (revised up from $5M placeholder per `03-cost-model-output.docx` recommendation; tier-1 retail-spine subscription range)
- P(landing such an anchor in Y3): 0.3 for first VAR (rises with subsequent VARs)
- Y3 NPV factor: 0.75

```
anchor_upside = $50M × 0.3 × 0.75 = $11.25M of NPV-adjusted Y3 upside
```

This is option value of the deal. **Don't add it to the base price.** Mention in deal narrative as the asymmetric upside scenario.

## Formula 5 — VAR-roll-up amortization (strategic context)

VAR #2's modernization cost is ~70% of VAR #1's cost. VAR #3 is ~55%. VAR #4+ is ~40%.

For RapidPOS-the-deal, this doesn't change the price we pay. It's the *strategic rationale* for paying *anything* — RapidPOS is the platform investment that makes the next 2-4 VAR deals cheaper.

## Formula 6 — total deal pricing

Putting it together:

| Line | $ |
| --- | --- |
| Base value (adjusted EBITDA $740k × 4.5x) | $3,330,000 |
| Less: ISMS-gap discount | -$341,000 |
| Less: modernization-premium offset | -$370,000 |
| Less: opportunity-cost cushion (worst-case) | -$207,000 |
| **Walking price** | **$2,412,000** |

Anchor-account upside (NPV-adjusted, Y3): +$11.25M (option value, not in base)

Strategic-rationale (subsequent VAR amortization): VAR #2 is roughly $1M cheaper than RapidPOS would be without RapidPOS as Patient Zero.

## Negotiation positions

| Scenario | Base price | Earnout | Total package |
| --- | --- | --- | --- |
| **Walking** | $2.4M | $0 | $2.4M |
| **Floor** | $2.4M | $0.6M (24-month earnout on customer-retention milestones) | $3.0M |
| **Target** | $2.7M | $0.8M | $3.5M |
| **Stretch** | $3.0M | $1.2M | $4.2M |

The seller's likely opening ask sits in the $4M-$6M range. Anchor near the floor; let the seller close themselves toward our target after seeing the gap math.

## Why this price structure works for the seller

- They were going to need the ISMS work done by *some* buyer; we're the cheapest credible path
- The earnout structure preserves their customer-retention income for 24 months (motivates a clean handoff)
- The Y3-5 founder-exit pacing matches their stated retirement timeline
- Bart-team partnership pre-loaded means immediate integration readiness (vs. PE rollup waiting for a tech partner)
- We let them keep their team; they're our onboarding pipeline (A4) not redundancy

## Walk-away condition (RapidPOS-specific)

We walk if:
- Seller insists on >5.5x adjusted EBITDA (no compliance discount accepted), OR
- Eager-cohort fraction comes in below 15% (validated in due diligence), OR
- Bart team turnover risk surfaces during diligence, OR
- Discovery surfaces undisclosed compliance issues (breach history, state regulatory action, customer-disclosed PII incidents)

Founder confirms genuinely-willing-to-walk: ☐ (for actual run; demo placeholder)

## Sensitivity to founder Q1 (revenue/EBITDA)

The base value scales linearly with EBITDA. If real EBITDA is materially different from $740k:

| Adjusted EBITDA | 4.5x base | Walking price | Notes |
| --- | --- | --- | --- |
| $400k | $1.8M | $0.9M | Worst case — barely above gap-cost; deal marginal |
| $740k | $3.3M | $2.4M | Expected case |
| $1.4M | $6.3M | $5.4M | Best case — strong economics |

The deal's economic viability is most sensitive to the EBITDA hypothesis. Founder Q1 + Q3 (revenue + team shape) should tighten this in the real run.

## Cross-references

- `02-iso27001-gap-assessment.xlsx::valuation_impact` tab — the math above in spreadsheet form
- `crb-skills/saas-acquisition-diligence/reference/06-valuation-impact-formulas.md` — the formula library
- `Brain/diligence/rapidpos/06-internal-deal-memo.md` — the founder-facing deal memo (Phase 3)
- `Brain/cost-models/rapidpos/02-cost-model-output.xlsx` — program cost cross-foot
