#!/usr/bin/env python3
"""
Build the single-site HTML deliverable — restructured around four questions:
1. What we're forming
2. What we're buying
3. What it's worth
4. How we go get it
"""

import markdown
from pathlib import Path
import html as html_lib

OUTPUTS = Path("/sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs")
DECK_DIR = OUTPUTS / "Brain/decks/shore-club-retail-vertical"

NAVY = "#21295C"
DEEP = "#065A82"
TEAL = "#1C7293"
CREAM = "#ECE2D0"
SAND = "#F5F1E8"
WHITE = "#FFFFFF"
CHARCOAL = "#36454F"

# ---------------------------------------------------------------------------
# Section definitions — id, title, source path (or None for inline), category
# ---------------------------------------------------------------------------

SECTIONS = [
    # Cover and exec summary
    ("cover", "Cover", None, "overview"),
    ("executive", "Executive proposal package", None, "overview"),

    # 1. WHAT WE'RE FORMING
    ("memo", "Memo to principals", "memo-to-principals-retail-vertical.md", "forming"),
    ("position", "Position paper — eljeffe Hash and Seal Protocol", "position-paper-eljeffe-io.md", "forming"),
    ("bylaws-skill", "Bylaws skill — namespace governance", None, "forming"),
    ("addendum", "Forward architecture — what the substrate adds next", None, "forming"),

    # 2. WHAT WE'RE BUYING
    ("buying-overview", "RapidPOS — what we're buying (overview)", None, "buying"),
    ("hypothesis-grid", "Hypothesis grid — RapidPOS profile", "diligence/rapidpos/01-hypothesis-grid.md", "buying"),
    ("iso-gap", "ISO 27001 gap assessment", "diligence/rapidpos/02-iso27001-gap-assessment.md", "buying"),
    ("gcp-onramp", "GCP onramp architecture", "diligence/rapidpos/03-gcp-onramp-architecture.md", "buying"),
    ("driftpos-readiness", "DriftPOS launch readiness", "diligence/rapidpos/05-driftpos-launch-readiness.md", "buying"),
    ("deal-memo", "Internal deal memo", "diligence/rapidpos/06-internal-deal-memo.md", "buying"),
    ("glide-path", "Managed-services glide path (external)", "diligence/rapidpos/07-managed-services-glide-path.md", "buying"),

    # 3. WHAT IT'S WORTH
    ("deal-economics", "Deal economics — what it's worth", None, "worth"),
    ("valuation", "Valuation impact (full math)", "diligence/rapidpos/04-valuation-impact.md", "worth"),
    ("investor", "Investor brief — Genesis Pool & Metcalfe model", "investor-brief-eljeffe-io.md", "worth"),

    # 4. HOW WE GO GET IT
    ("hundred-day", "The 100-day plan", None, "execution"),
    ("day1-ops", "Day-1 agentic ops plan (A1-A5)", "diligence/rapidpos/09-day1-agentic-ops-plan.md", "execution"),
    ("burndown", "Burn-down → repeatability flywheel", "diligence/rapidpos/10-burndown-flywheel.md", "execution"),
    ("tim-prep", "Tim conversation prep", None, "execution"),
    ("wyoming", "Wyoming counsel engagement", "dispatches/A1-wyoming-counsel-scope.md", "execution"),
    ("compliance-role", "Compliance-architecture role", "dispatches/B4-compliance-architecture-role.md", "execution"),
    ("dns", "DNS / position-paper publication", "dispatches/A4-dns-publication-scope.md", "execution"),
    ("uw", "UW academic engagement", "dispatches/G1-uw-engagement-scope.md", "execution"),

    # Reference & close
    ("deck", "Deck content — proposal in slides", None, "reference"),
    ("foundation", "Foundation synthesis — corpus inventory", "_session/foundation-synthesis.md", "reference"),
    ("close", "Session close — artifacts, decisions, next", None, "reference"),
]

CATEGORY_LABELS = {
    "overview": "Overview",
    "forming": "1 · What we're forming",
    "buying": "2 · What we're buying",
    "worth": "3 · What it's worth",
    "execution": "4 · How we go get it",
    "reference": "Reference",
}

# ---------------------------------------------------------------------------
# Markdown → HTML helpers
# ---------------------------------------------------------------------------

md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "toc", "meta"])

def md_to_html(text: str) -> str:
    md.reset()
    return md.convert(text)

def read_section(path: str) -> str:
    full = OUTPUTS / path
    if not full.exists():
        return f"<p><em>Source not found: {path}</em></p>"
    text = full.read_text()
    if text.startswith("---"):
        end = text.find("---", 3)
        if end >= 0:
            text = text[end+3:].lstrip()
    return md_to_html(text)

# ---------------------------------------------------------------------------
# Inline content
# ---------------------------------------------------------------------------

INLINE_EXECUTIVE = """
# Executive proposal package

The whole package on one page. Each of the four questions answered tight. Detail in the sections below.

## 1. What we're forming

A Wyoming-anchored venture (LLC + DAO LLC) running the eljeffe Hash and Seal Protocol — a substrate that hashes commercial events, batches them into Merkle trees, and inscribes the roots on the Bitcoin time chain. Three principals at genesis tier: Domain (founder, brings Canary IP stack and serves as President of Retail / CTO of RapidPOS during transition), Governance (Tim, bylaws steward), Ops/Cloud (TBD — third principal to be named per Tim's calibration). No HR, no shared services, no PE-style mechanisms. Anti-extraction by construction. The structure protects the customer (data sovereignty), the contributor (permanent token-earn), and the operator (un-cullable genesis stake).

The substrate's first commercial application is the retail vertical, anchored at RapidPOS as channel partner — *not* an acquisition target.

## 2. What we're buying

RapidPOS LLC — Counterpoint VAR with ~50 customers across specialty verticals (garden, gun, wine, specialty food, feed-and-tack), ~$2.7M aggregate ARR, 6-12 person team with 2-3 senior engineers carrying 15-20-year Counterpoint configuration knowledge, 20 years of customer relationships, NCR-authorized status. The book is the asset; the team is the second asset; the ATF / wine / state-tax compliance experience is the third.

We are not paying SaaS-modernized multiples for a legacy services business. We are paying the legacy multiple, minus the modernization work we'll absorb, plus a fair earnout for the customer continuity that makes the deal economics work. The 24-month managed-services glide-path lets the seller exit clean by Year 3-5 while customer relationships stay intact through transition. DriftPOS partnership is preserved through the transition; Bart's team becomes our onboarding pipeline once the agentic ops fabric absorbs the support-queue treadmill.

## 3. What it's worth

Three numbers on the deal:

| | Amount | Source |
| --- | --- | --- |
| **Walking price** | $2.41M | Adjusted EBITDA $740k × 4.5x current-state multiple, less $341k ISMS-gap discount, less $370k modernization-premium offset, less $207k opportunity-cost cushion |
| **Target close** | $3.5M total package | $2.7M base + $0.8M earnout over 24 months tied to customer-retention milestones |
| **Anchor upside (Y3 NPV)** | +$11.25M | $50M anchor ARR × 30% landing probability × 0.75 NPV factor — option value, not in base price |

Three numbers on the program (post-close investment over 36 months):

| | Amount | Source |
| --- | --- | --- |
| **ISO 27001 remediation (DriftPOS-blocking)** | $487k all-in | 520 engineering hours for 15 critical controls + ISMS framework + Stage 1/2 audit fees + surveillance |
| **GCP run-rate at T1 (eager-cohort migrated)** | ~$668k/year | 18 workloads sized at T1; ~$55,700/month; scales with revenue |
| **Genesis Pool network value at month 18 (350 merchants)** | $785k (69× static BTC) | Metcalfe model crossover at month 9; conservative k = $0.667 per connection |

Investor allocation: 3M ordinals (30% of the 10M Genesis Pool) sold at BTC market rate × sat allocation per ordinal. No preferred shares. No board control. No exit machinery. Returns come from ordinal appreciation (Metcalfe-driven), validation revenue accrual, treasury participation, and L402 marketplace flow.

## 4. How we go get it

A 100-day intensive in three months, ending with a demonstrably-positioned venture ready to capitalize Phase B.

**Month 1 (Days 1-30) — Foundation.** Engage Wyoming counsel and file LLC + DAO LLC. Configure DNS for `eljeffe.io`; publish the position paper at `/position`; inscribe its content hash on chain. Refine memo + deck for the Tim conversation. Complete the bylaws skill. Founder reviews each artifact before external use.

**Month 2 (Days 31-60) — Communication + Genesis.** Tim conversation executed. Third principal identified and brought in. Bart partnership update. Compliance-architecture lead onboarded. Bylaws v1 ratified. Genesis block inscribed. Founder smart contract deployed. Position paper goes live.

**Month 3 (Days 61-100) — Substrate + first customer.** L402 gates scaffolded around MCP ports. Lightning consume rails live. CRB.ai product surface specified. RapidPOS engagement formalized (founder operational as CTO; channel-partner license terms drafted). PCI scope analysis complete. ISO 27001 readiness assessment complete. First firearms-vertical pilot customer identified.

**Day-100 review.** All Category A dispatches complete. Tim, Bart, compliance-architecture lead aligned. Substrate live. First customers in pipeline. Compliance baseline clean. That's the gate to capitalize Phase B.

## What's missing from this package

The cost-model output (the `.xlsx` with 230 formulas referenced in the prior session epic) is not on disk. The deal economics in section 3 above are synthesized from the valuation-impact, GCP-onramp, and ISO 27001 gap-assessment documents — accurate but not dynamic. To produce a fully-flexible cost model the founder can run sensitivity analysis against, the cost-model skill needs to be built or surfaced. That's a discrete next-wave deliverable.

---

*The proposal continues in the four sections below.*
"""

INLINE_BUYING_OVERVIEW = """
# RapidPOS — what we're buying (overview)

The five sections that follow are the diligence run on RapidPOS-as-target. They were produced by the saas-acquisition-diligence skill in the prior session. The framing is acquisition-cost / valuation-discount / glide-path because that's the skill's posture.

The current venture-instance reframes RapidPOS as **channel partner**, not acquisition target. Most of the diligence content carries forward (the ISO 27001 gap is the same gap; the GCP onramp is the same architecture; the DriftPOS launch readiness is the same gate; the day-1 agentic ops plan is the same plan). What changes is the *commercial frame*: instead of paying acquisition price for the customer book, we license Canary to RapidPOS via channel-partner agreement and the founder serves as CTO during the transition. The economic effect is similar (modernization work happens on the same timeline; revenue flows through the transition); the structural form is partnership-shaped rather than M&A-shaped.

## What's in this section

| Document | What it answers |
| --- | --- |
| Hypothesis grid | What do we think is true about RapidPOS LLC? Confidence labels per assumption |
| ISO 27001 gap assessment | What does it cost to make the platform certifiable? |
| GCP onramp architecture | What does the modernized stack look like at each scale tier? |
| DriftPOS launch readiness | What stands between today and DriftPOS GA at month 12? |
| Internal deal memo | Frank Growdirect-only assessment — thesis, walking price, walk-away conditions |
| Managed-services glide path | External pitch document — peer-to-peer voice, 24-month transition narrative |

## Reconciliation note

The diligence run was produced under the v1 framing (acquire RapidPOS). The v2 venture-instance pivot (channel partner, no acquisition) hasn't been re-run through the diligence skill yet. The financial substance survives the reframe; the legal/structural framing needs adjustment. Treat the docs below as substantive on the operational and economic content, and apply the channel-partnership reframe at the structural level.
"""

INLINE_DEAL_ECONOMICS = """
# Deal economics — what it's worth

Tight summary. Detail in `Valuation impact (full math)` below. The investor brief covers the Genesis Pool / Metcalfe network valuation separately.

## Deal pricing

The acquisition (or channel-partnership equivalent) is priced as: current-state value − cost we'll incur to make the asset productive − opportunity-cost cushion. Anchor-account upside is option value, *not* in the base price.

**Inputs (founder verification needed before walking-price commits):**

- Annual revenue: ~$3-6M (target-profile midpoint $4.5M)
- EBITDA margin: ~22%
- Current-state EBITDA: $4.5M × 22% = **$990k**
- Owner compensation in EBITDA: yes (founder-owned operator). Adjusted EBITDA after replacement-CEO comp ($250k): **$740k**

**The negotiation:**

| Framing | Multiple | Implied price (at adjusted EBITDA $740k) |
| --- | --- | --- |
| Legacy SMB services VAR | 3-4× | $2.2M-$3.0M |
| Legacy specialty-retail VAR | 4-5× | $3.0M-$3.7M |
| Modernized retail platform | 6-10× | $4.4M-$7.4M |
| Platform-SaaS comparable | 8-15× ARR | $36M-$67M |

Sellers like the bottom row. Buyers price toward the top. Our positioning: **legacy specialty-retail VAR at 4.5× adjusted EBITDA, minus modernization cost we absorb, plus fair earnout for customer continuity.**

**Walking price math:**

| Line | $ |
| --- | --- |
| Base value ($740k × 4.5×) | $3,330,000 |
| Less: ISMS-gap discount (Formula 1: $487k × 0.7 compliance-pressure factor) | -$341,000 |
| Less: modernization-premium offset (Formula 2: $740k × 2.5 multiple delta × 0.2 prob without us) | -$370,000 |
| Less: opportunity-cost cushion (Formula 3: 6-month delay × $450k incremental ARR × 0.92 NPV) | -$207,000 |
| **Walking price** | **$2,412,000** |

**Negotiation positions:**

| Scenario | Base | Earnout | Total package |
| --- | --- | --- | --- |
| **Walking** | $2.4M | $0 | $2.4M |
| **Floor** | $2.4M | $0.6M | $3.0M |
| **Target** | $2.7M | $0.8M | $3.5M |
| **Stretch** | $3.0M | $1.2M | $4.2M |

Seller's likely opening: $4M-$6M. Anchor near floor; let seller close themselves toward target after seeing the gap math.

**Anchor upside (Y3 option value, NOT in base):**

$50M hypothetical anchor ARR × 30% landing probability × 0.75 Y3 NPV factor = **+$11.25M of NPV-adjusted Y3 upside**.

## Program cost (post-close, 36 months)

The investment to make the asset productive — what we're absorbing on top of the purchase price.

**ISO 27001 remediation:**

| Component | Hours | $ |
| --- | --- | --- |
| 15 critical-mass DriftPOS-blocking controls | 520 | $104k |
| Remaining 78 Annex A controls | ~1,164 | $233k |
| ISMS framework (policy + governance) | 200-400 | $40-80k |
| Stage 1 + Stage 2 audit fees | — | $20-50k |
| Surveillance (annual ongoing) | — | $10-20k/year |
| **Total all-in over 18 months** | **~1,684** | **~$487k** |

Compliance-pressure factor 0.7 (moderate — specialty retail with growing pressure but not acute). The seller absorbs ~$341k as a price reduction; the rest (~$146k) is our investment in modernization.

**GCP run-rate (steady-state per scale tier):**

| Tier | Profile | Customers | Stores | Monthly | Annualized |
| --- | --- | --- | --- | --- | --- |
| T0 | RapidPOS today | ~50 | ~500-2,500 | — | — |
| **T1** | **Eager-cohort migrated** | **~T0 × 25-40%** | **~thousands** | **~$55,700** | **~$668k** |
| T2 | Steady cohort + new-logo | ~T0 + new | ~5K-15K | ~$120-180k | ~$1.4-2.2M |
| T3 | Global-50 anchor | ~T2 + 1 anchor | ~50K+ at peak | ~$1.5M+ | ~$18M+ |

T3 only triggers if a Global-50 anchor lands. Without anchor, we stay at T2 steady-state and the math also works (~$7.6M net 3-year per the internal deal memo).

**Day-1 agentic ops cost (workload #18 in the GCP onramp):**

| Component | Phase A monthly |
| --- | --- |
| Vertex AI inference (A1-A5 agents) | ~$3-5k |
| GKE / Cloud Run agent runtimes | ~$2k |
| Pub/Sub event triggers + Cloud SQL state | ~$500 |
| Cloud Storage (wiki + playbook output) | ~$500 |
| **Subtotal** | **~$8k/month** |

This compute spend substitutes for FTE-hours across the support queue per the burndown flywheel — the cost-model shows the substitution explicitly.

## Total package economics (illustrative 3-year)

| Year | Revenue | Cost | Net | What's happening |
| --- | --- | --- | --- | --- |
| Y1 | $1-2M | ~$1.5-2M | ~breakeven | Eager-cohort migrating; first Square-BTC merchants; ISO Phase A |
| Y2 | $5-10M | ~$3-6M | $1-4M positive | Steady cohort migrating; ISO 27001 cert; DriftPOS GA; new-logo wins |
| Y3 | $15-40M | ~$8-18M | $7-22M positive | Full cohort migration; possible first anchor; channel-partner momentum; multi-cohort revenue |

Why these numbers work where typical SaaS doesn't:

- **No acquisition cost.** RapidPOS is channel partner. ~$2-3M not paid (the walking price above is the M&A frame; the channel-partner frame avoids it entirely).
- **No HR overhead.** ~$1M+/year structurally avoided.
- **Variable contributor comp.** L402 pay-per-use; low-revenue periods don't burn fixed payroll.
- **No T3 forced ramp.** GCP scales with revenue.
- **Five customer cohorts.** VAR roll-up, DriftPOS pilots, Square BTC, future channel partners, direct independent retail. Diversified.

## Genesis Pool valuation (separate accounting)

The Genesis Pool — 10,000,000 satoshis from the founder's F2Pool mining reward — is a network asset, not a treasury holding. Static BTC value at $85K/BTC ≈ $8,500. Metcalfe network value at month 18 (350 merchants) ≈ **$785,409 — a 69× multiple**. Crossover happens at ~50 merchants (month 9). After that, the network valuation accelerates quadratically while BTC appreciation remains roughly linear.

Investor allocation: 3M ordinals (30% of the Genesis Pool) sold at BTC market rate × sat allocation per ordinal. Same satoshis, different frame. Investors are not buying BTC at market rate — they are buying first-mover network position in a namespace whose value compounds with adoption.

See `Investor brief` and `Valuation impact (full math)` for the full math and sensitivity analysis.

## What's not in this summary

The cost-model `.xlsx` with 230 formulas (referenced in the prior session epic) — would let the founder flex assumptions live (revenue, EBITDA, cohort split, GCP scale tier, ISO remediation pace) and watch deal price + program cost re-cross-foot. **Not on disk.** Would be produced by running the cost-model skill against the venture-instance — discrete next-wave work. Until that ships, the numbers above are the synthesized point-estimates.
"""

INLINE_HUNDRED_DAY = """
# The 100-day plan

Three months. Solo. Founder full-in. Day 100 = either demonstrably-positioned (Phase B capitalization gate) or honestly-not (everyone's learned without burning runway).

## Month 1 (Days 1-30) — Foundation

| Dispatch | What | Owner | Acceptance |
| --- | --- | --- | --- |
| **A1** | Wyoming entity formation engagement (LLC + DAO LLC) | Founder + Wyoming counsel | Both entities in good standing; banking relationship live |
| **A4** | DNS for `eljeffe.io`; minimal site stand-up; position paper at `/position` | Founder | Site live; block-height anchor in footer |
| **A5** | Position paper drafted | Claude | Passes founder review; ready for A4 publication |
| **D5** | Memo + deck final refinement | Claude | Both pass ranch test; ready for Tim conversation |
| **B1** | Tim conversation prep package | Founder + Claude | Conversation scheduled; collated single-site HTML in Tim's hands |
| **C1** | Bylaws skill completion (8/9 → 9/9 + 5 templates) | Claude | Skill complete; runs cleanly against synthetic second namespace |

## Month 2 (Days 31-60) — Communication + Genesis

| Dispatch | What | Owner | Acceptance |
| --- | --- | --- | --- |
| **B1** | Tim conversation executed (week 5-6) | Founder | Tim's stated alignment / pushback / counter-proposals captured |
| **B2** | Third principal identification + outreach (week 6-8) | Founder | Third principal candidate named; preliminary commitment |
| **B3** | Bart partnership update (week 7-8) | Founder | Bart aligned on partnership shape; OQ resolution path agreed |
| **B4** | Compliance-architecture lead onboarding (week 6) | Founder | Role agreed and documented; first deliverables scoped |
| **A2** | Genesis block inscription (week 8, after bylaws v1 ratified) | Founder + tech | Namespace identifier live on chain; founder ordinals in principal wallets |
| **A3** | Founder smart contract deployment (week 8-9) | Tech contributor | Smart contract addressable; first test transaction stamped |
| **A5 → A4** | Position paper published at eljeffe.io/position (week 8-9) | Founder | Site live with content hash inscribed; block-height anchor recorded |

## Month 3 (Days 61-100) — Substrate + First Customer

| Dispatch | What | Owner | Acceptance |
| --- | --- | --- | --- |
| **C2** | eljeffe Hash and Seal Protocol formal specification | Claude (drafts); founder reviews | Spec complete; ready for publication adjacent to position paper |
| **C3** | L402 gate scaffolding for MCP ports | Tech contributor | At least one MCP port gated by L402; sat payment routes to wallet |
| **C5** | Lightning consume setup | Tech contributor | Rails live; first L402 transaction confirmed |
| **D1** | CRB.ai product surface spec (v0) | Founder + Claude | Spec complete; reviewed by founder |
| **D4** | RapidPOS engagement plan formalized | Founder + RapidPOS | Dual-role agreement documented; channel-partner license drafted |
| **E1** | PCI-DSS scope analysis | Compliance-architecture lead | PCI scope position documented; auditor-readable |
| **E2** | ISO 27001 readiness assessment | Compliance-architecture lead | Gap inventory complete; critical-mass 15 sequenced |
| **D2** | Firearms-vertical beachhead plan + first-pilot customer | Founder | Beachhead plan complete; first-pilot customer identified |

## Day-100 review — Phase B capitalization gate

If the day-100 state looks like the table above, the venture is *demonstrably positioned*: entity formed, principals aligned, substrate live, first customers in pipeline, compliance baseline clean. That's the gate to capitalize Phase B (months 4-12).

If it doesn't, we've learned something honestly. The eljeffe wallet contribution stays on chain; nobody's runway has been burned; the architecture and the corpus persist for whatever comes next.

## Open decisions still pending founder calibration

The 8 items from the company-formation epic Part 5, plus the 4 from the addendum. Tim's calibration on items 1, 5, 8 (third principal, Heal's role, founder compensation) is the priority for the first conversation. Items 9-12 (lease vs subdivision, Council Port liability, bridged-officer precedence, Audit Port admission) wait for the formation-documents skill.
"""

INLINE_TIM_PREP = """
# Tim conversation prep

This single-site HTML *is* the collation. Tim opens it, reads top-to-bottom or jumps via the navigation, arrives at the conversation with the context the founder has.

## What Tim should read before the conversation

In priority order (skip-allowed if Tim is short on time):

1. **Executive proposal package** (`#executive`) — the four answers in one page. Read this first.
2. **Memo to principals** (`#memo`) — the full proposed approach and ask. This is the document the conversation is about.
3. **Deal economics** (`#deal-economics`) — what the deal costs and what it's worth.
4. **Position paper** (`#position`) — the protocol the venture operationalizes.
5. **Compliance-architecture role** (`#compliance-role`) — Tim's read on this shapes the third-principal candidate decision.
6. **Wyoming counsel scope** (`#wyoming`) — the engagement Tim approves at conversation close, if alignment is reached.

The 100-day plan (`#hundred-day`) is the execution map; reference during the conversation.

## Conversation agenda (90 minutes recommended)

- **0-10 min — context.** Founder briefly: where the thinking has landed since the last conversation
- **10-30 min — the structure.** Walk through the proposed structure, three-pillar genesis, dual-role founder commitment, eljeffe wallet contribution, 100-day intensive frame
- **30-50 min — the open decisions.** Eight items below. Tim's calibration on each shapes downstream dispatches
- **50-70 min — Tim's questions.** Open the floor for what Tim wants to push back on, deepen, redirect, or veto
- **70-85 min — alignment check.** Where are we — proceed to formalization, iterate, or pause?
- **85-90 min — wrap.** Confirm next checkpoint date; confirm any specific artifacts Tim wants in his hands before B3 or B2

## Open decisions for Tim's calibration

| # | Decision | Affects |
| --- | --- | --- |
| 1 | Third principal identity — Tim's existing partner / separate cloud-architecture recruit / compliance-architecture lead elevated? | Cap-table mechanics; B2 outreach |
| 2 | Per-pillar mint authority vs. multi-sig joint mints during Phase 1 | Smart contract design (A3); bylaws (C1) |
| 3 | `jefe.io` vs. `eljeffe.io` as primary canonical namespace identifier | Position paper publication (A4); DNS configuration |
| 4 | Open-source vs. proprietary line | Protocol formal specification (C2); IP contribution agreement |
| 5 | Heal's role and audience inclusion | B5 (Heal conversation + King Harbor mailing-address registration) |
| 6 | Lightning operator commitment timing — Phase 1 internal-only at month 12+, or earlier? | C5; partner-evaluation strategy |
| 7 | DriftPOS naming evolution — Bart's call | B3 |
| 8 | Founder compensation specifics — RapidPOS-CTO salary range, GrowDirect-equity vesting terms | D4 (RapidPOS engagement plan) |

## What success looks like at conversation close

- Tim has read the executive package, memo, position paper, and deal economics
- Tim's stated alignment / pushback / counter-proposals are captured in writing
- Open decisions 1, 5, 8 have at least preliminary answers
- A specific next-checkpoint date is set
- Tim approves engaging Wyoming counsel (A1) and the third-principal outreach (B2)

If alignment is reached, the wave moves from staging into execution within 48 hours.
"""

INLINE_DECK_CONTENT = """
# Deck content — proposal in slides

The .pptx version is at `outputs/Brain/decks/shore-club-retail-vertical/shore-club-retail-vertical-deck.pptx` for the in-person walk-through. Content rendered below; deck and HTML serve different read postures.

## Slide 1 — Cover
**Retail vertical.** Proposed approach, structure, and 100-day plan. eljeffe Hash and Seal Protocol — Wyoming-anchored. BTC-native. Anti-extraction by construction. *Tell me where I'm wrong.*

## Slide 2 — The moment
A once-in-a-decade inflection. Square pushes BTC. Counterpoint VARs aging out. Compliance fragmenting. Operators want sovereignty.

## Slide 3 — What the substrate does
Hash → Batch → Inscribe → Verify. The proof is the proof.

## Slide 4 — The structure
Parent → GrowDirect → IP → RapidPOS license. Substrate underneath.

## Slide 5 — Three-pillar genesis
Domain principal (founder). Governance principal (Tim). Ops/Cloud principal (TBD).

## Slide 6 — Economics
Y1 ~breakeven on $1-2M. Y2 $1-4M positive on $5-10M. Y3 $7-22M positive on $15-40M.

## Slide 7 — Compliance-by-architecture
The substrate produces audit-defensible evidence by construction. NICS attestation as concrete instantiation.

## Slide 8 — How we recruit and operate
No HR. Trusted-network model. Two contributor segments. King Harbor / Redondo Beach.

## Slide 9 — What this protects
Customer (data sovereignty). Contributor (permanent token-earn). Operator (un-cullable genesis stake).

## Slide 10 — Appendix A: Throwaway-key / agent-mediated interaction
Persistent identity at the ordinal; ephemeral capability via leased keys.

## Slide 11 — Appendix B: Lightning operator forward path
Phase 0 consume → Phase 1 internal → Phase 2 external service.
"""

INLINE_BYLAWS_INDEX = """
# Bylaws skill — namespace governance

The complete skill at `outputs/crb-skills/namespace-bylaws/`:

- **`SKILL.md`** — entry point; trigger phrases; voice rules; reference contents map
- **`reference/01-shore-club-lineage.md`** — Article-by-Article modernization (canonical from prior session)
- **`reference/02-genesis-ordinal-mechanics.md`** — substrate primitives; DAO-action stamping; founder-mint authority
- **`reference/03-dao-treasury-patterns.md`** — categorized cash-out; thresholds; multi-sig
- **`reference/04-lineage-weighted-voting.md`** — formula `w(d) = 1 / (1 + α·d)`; quorum mechanics
- **`reference/05-phase-transitions.md`** — four-phase progression
- **`reference/06-cultural-technical-mapping.md`** — two-layer mapping
- **`reference/07-alignment-checks.md`** — 23 checks across 7 categories
- **`reference/08-iteration-loop.md`** — comment-and-revision loop; Cove as reference engine
- **`reference/09-anti-patterns.md`** — *NEW.* Ten failure modes (HR-as-PE-culling, vesting-cliff dilution, etc.)
- **`templates/bylaws-document.md`** — Articles I-XIV in two-layer form
- **`templates/namespace-genesis-record.md`** — birth-event record
- **`templates/amendment-proposal.md`** — clause delta with alignment-check table
- **`templates/alignment-review.md`** — periodic review (all 23 checks)
- **`templates/comment-ledger.md`** — comment tracking with five shapes

The skill is complete (9/9 reference docs + 5 templates). Forward design for Articles XV/XVI/revised V/VIII/XI/XIV-or-XVII lives in the addendum (`#addendum`).
"""

INLINE_ADDENDUM = """
# Forward architecture — what the substrate adds next

Forward design for the formation-documents skill. Bylaws skill ships now with what's needed for Phase A; the addendum specifies the architectural extensions for the next wave. Full design notes at `outputs/addendum-substrate-port-and-officer-architecture.md`.

## Architectural decisions (10)

**1. Three port classes — Member, Council, Audit.** Same physical mechanism (an MCP service plugged into a port) routes to three different financial and constitutional rails. Member ports L402-gated, packets-served compensation. Council ports treasury-paid (oversight is not metered). Audit ports for external compliance entities (regulators, security firms) holding no ordinal but with defined inspection rights.

**2. Introduction-accountability-revocation contract.** Every entity plugging into a port emits a port declaration with identity / provenance commitment / intent stream / revocation conformance. Three revocation tiers: Pause / Revoke / Quarantine.

**3. Packets-served equity model — formalized via Article XI.** Three principles: acceptance signal, packet-type definitions (platform-wide), retroactive unwinding.

**4. Annexation Article (XVI) — substrate-namespace relationship.** Two valid models, namespace electing at constitution: lease (operationally independent) or subdivision-with-root-operating-company (substrate retains active operational presence).

**5. Officer Ordinal class — held by namespace contract address.** New ordinal class held by the namespace's smart contract address rather than by individuals. Solves agentic-officer constitutional standing cleanly.

**6. Bridged-accountability — officers serving substrate-and-namespace simultaneously.** Officer operates two officer ordinals. Accountable to namespace board for operational performance, to substrate bylaws for structural conformance. Structural safeguard against rogue subDAOs.

**7. Agentic Secretary — canonical bridged-officer instance.** Secretary role implemented agentically: continuous on-chain ledger maintenance, conclusive-evidence certificates, delinquency notices, periodic disclosures.

**8. Reversion-on-material-breach — added to Article VIII.** Strongest enforcement mechanism. Defined material breach categories, adjudication procedure, high invocation threshold.

**9. Voided-but-preserved documentary discipline.** Preserve verbatim; mark visibly void; inscribe override rationale; cite override authority; do not erase. Amendment never overwrites.

**10. External-validation council loop — active operational pattern.** External review continuous via Audit Ports. Findings route through triage by operator-of-record, inscription, multi-reviewer reconciliation, acceptance loop.

## Drafting order recommended

XVI → V → XV → VIII → XI extension → XIV extension or new XVII.

## Open questions (4)

| # | Question | Default lean |
| --- | --- | --- |
| Q1 | Lease vs subdivision — substrate-default or namespace-choice? | Mandatory election at constitution |
| Q2 | Operator-of-record liability for Council Ports | Open |
| Q3 | Bridged-officer revocation when substrate and namespace disagree | Substrate (with explicit precedence per role) |
| Q4 | Audit Port admission — voluntary and required paths | Both paths specified |

## Why this matters for the wave

Three of the wave's open decisions are materially affected: third principal identity (open #1 — bridged-officer model changes role definition), open-source vs proprietary line (open #4 — Service Ports schema candidate for open-source), Heal's role (open #5 — principal-tier vs Council Port advisory).
"""

INLINE_SESSION_CLOSE = """
# Session close — artifacts, decisions, next

## Artifacts produced this wave

| # | Artifact | Path |
| --- | --- | --- |
| 1 | Wave deliverable HTML (this document) | `outputs/wave-deliverable.html` |
| 2 | Claude.ai design-mode prompt | `outputs/wave-deliverable-claude-design-prompt.md` |
| 3 | Position paper (A5) | `outputs/position-paper-eljeffe-io.md` |
| 4 | Memo to principals (D5a — refined) | `outputs/memo-to-principals-retail-vertical.md` |
| 5 | Investor brief (F1-F2) | `outputs/investor-brief-eljeffe-io.md` |
| 6 | Shore Club deck (D5b) | `outputs/Brain/decks/shore-club-retail-vertical/shore-club-retail-vertical-deck.pptx` |
| 7 | Bylaws skill (C1 — 9/9 + 5 templates) | `outputs/crb-skills/namespace-bylaws/` |
| 8 | RapidPOS diligence run (10 docs from prior session, integrated) | `outputs/diligence/rapidpos/` |
| 9 | B4 — Compliance-architecture role | `outputs/dispatches/B4-compliance-architecture-role.md` |
| 10 | A1 — Wyoming counsel scope | `outputs/dispatches/A1-wyoming-counsel-scope.md` |
| 11 | A4 — DNS / publication scope | `outputs/dispatches/A4-dns-publication-scope.md` |
| 12 | G1 — UW engagement scope | `outputs/dispatches/G1-uw-engagement-scope.md` |
| 13 | Substrate-port-and-officer architecture addendum | `outputs/addendum-substrate-port-and-officer-architecture.md` |
| 14 | Foundation synthesis | `outputs/_session/foundation-synthesis.md` |

## What's still missing

- **Cost-model `.xlsx` with 230 formulas.** Referenced in the prior session epic; not on disk. Would let the founder flex assumptions live (revenue, EBITDA, cohort split, GCP scale tier, ISO remediation pace) and watch deal price + program cost re-cross-foot. Discrete next-wave deliverable — requires the cost-model skill on disk first.
- **Diligence run reframed for v2 venture-instance.** Current diligence docs were produced under the v1 acquisition framing. Substantive content survives the channel-partnership reframe; structural framing needs adjustment. Worth a delta-pass when bandwidth allows.
- **Formation-documents skill.** Operationalizes the addendum's 10 architectural decisions into bylaws Articles XV/XVI/revised V/VIII/XI/XIV-or-XVII. Separate Cowork session per the addendum's own handoff note.

## Reconciliation list — when prior-session outputs surface

- D5b Shore Club deck v1
- B1 Tim conversation prep v1 (collated as HTML this wave)
- C1 SKILL.md and 5 templates v1 (built this wave)
- D5a memo v1 reconciled (the v1 surfaced; this wave's version is a refinement)
- Diligence run reconciled (the prior session's 10 docs surfaced and are integrated)
- Bylaws skill 8 reference docs reconciled (canonical from prior session; not modified)

## Open decisions

12 items total — 8 from the company-formation epic, 4 from the addendum. Tim's calibration on items 1, 5, 8 is the priority for the first conversation. See `#tim-prep` for the full list.

## Next-session priorities

**Month 1 finishing items** (Phase A weeks 4-8): Tim conversation; Wyoming counsel selection; DNS configuration + position paper publication; UW outreach; compliance-architecture lead candidate identification.

**Month 2 setup** (Phase A weeks 9-12): Third principal outreach; Bart partnership update; Genesis block inscription; founder smart contract deployment; eljeffe Hash and Seal Protocol formal specification; first investor outreach.

**Cross-wave priorities:**
- Build (or surface) the cost-model skill → produce the cost-model `.xlsx`
- Build the formation-documents skill → operationalize the addendum's architectural decisions

## Session close

Fourteen artifacts shipped, organized around the four questions: what we're forming, what we're buying, what it's worth, how we go get it. The 100-day intensive begins on Tim's go.
"""

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def section_html(sec_id: str, title: str, body_html: str, category: str) -> str:
    return f'''
<section id="{sec_id}" data-category="{category}">
  <header class="section-header">
    <span class="cat-pill">{html_lib.escape(CATEGORY_LABELS[category])}</span>
    <h2>{html_lib.escape(title)}</h2>
  </header>
  <div class="section-body">
    {body_html}
  </div>
</section>
'''

def cover_html() -> str:
    return '''
<section id="cover" data-category="overview" class="cover">
  <div class="cover-inner">
    <p class="cover-eyebrow">Wave session deliverable · 2026-05-03</p>
    <h1>Retail vertical</h1>
    <p class="cover-sub">A complete proposal package answering four questions:<br/>
    <strong>what we&rsquo;re forming · what we&rsquo;re buying · what it&rsquo;s worth · how we go get it.</strong></p>
    <p class="cover-tag"><em>Tell me where I&rsquo;m wrong.</em></p>
    <p class="cover-meta">Anchored to BTC block height: <span class="block-anchor">TBD</span></p>
  </div>
</section>
'''

# Assemble nav
nav_groups = {}
for sec_id, title, _path, category in SECTIONS:
    if sec_id == "cover":
        continue
    nav_groups.setdefault(category, []).append((sec_id, title))

nav_html = '<nav class="sidebar"><div class="brand"><strong>Wave</strong><br/><span>2026-05-03</span></div>\n<ul class="nav">\n'
nav_html += '<li class="nav-cat-cover"><a href="#cover">Cover</a></li>\n'
for cat in ["overview", "forming", "buying", "worth", "execution", "reference"]:
    if cat not in nav_groups:
        continue
    nav_html += f'<li class="nav-cat"><span>{CATEGORY_LABELS[cat]}</span><ul>\n'
    for sec_id, title in nav_groups[cat]:
        nav_html += f'    <li><a href="#{sec_id}">{html_lib.escape(title)}</a></li>\n'
    nav_html += '</ul></li>\n'
nav_html += '</ul></nav>\n'

# Sections
sections_html = cover_html()
for sec_id, title, source, category in SECTIONS:
    if sec_id == "cover":
        continue
    if source is not None:
        body = read_section(source)
    else:
        if sec_id == "executive":
            body = md_to_html(INLINE_EXECUTIVE)
        elif sec_id == "buying-overview":
            body = md_to_html(INLINE_BUYING_OVERVIEW)
        elif sec_id == "deal-economics":
            body = md_to_html(INLINE_DEAL_ECONOMICS)
        elif sec_id == "hundred-day":
            body = md_to_html(INLINE_HUNDRED_DAY)
        elif sec_id == "tim-prep":
            body = md_to_html(INLINE_TIM_PREP)
        elif sec_id == "deck":
            body = md_to_html(INLINE_DECK_CONTENT)
        elif sec_id == "bylaws-skill":
            body = md_to_html(INLINE_BYLAWS_INDEX)
        elif sec_id == "addendum":
            body = md_to_html(INLINE_ADDENDUM)
        elif sec_id == "close":
            body = md_to_html(INLINE_SESSION_CLOSE)
        else:
            body = "<p>(content forthcoming)</p>"
    sections_html += section_html(sec_id, title, body, category)

# CSS
css = f"""
:root {{
  --navy: {NAVY};
  --deep: {DEEP};
  --teal: {TEAL};
  --cream: {CREAM};
  --sand: {SAND};
  --white: {WHITE};
  --charcoal: {CHARCOAL};
  --serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Calibri, Roboto, sans-serif;
  --mono: "SF Mono", Menlo, Monaco, Consolas, monospace;
  --col: 760px;
}}

* {{ box-sizing: border-box; }}

html, body {{
  margin: 0; padding: 0;
  font-family: var(--sans);
  background: var(--white);
  color: var(--charcoal);
  line-height: 1.55;
  font-size: 16px;
  scroll-behavior: smooth;
}}

a {{ color: var(--deep); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.15s; }}
a:hover {{ border-bottom-color: var(--deep); }}

.layout {{
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
}}

@media (max-width: 900px) {{
  .layout {{ grid-template-columns: 1fr; }}
  .sidebar {{ position: static !important; height: auto !important; border-right: none !important; border-bottom: 1px solid #e0e0e0; }}
}}

.sidebar {{
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  background: var(--navy); color: var(--cream);
  padding: 32px 24px; border-right: 1px solid #e0e0e0;
  font-size: 14px;
}}
.sidebar .brand {{
  font-family: var(--serif);
  font-size: 22px; line-height: 1.1; color: var(--white);
  margin-bottom: 24px; padding-bottom: 16px;
  border-bottom: 1px solid rgba(236, 226, 208, 0.2);
}}
.sidebar .brand span {{
  font-family: var(--sans); font-size: 11px;
  color: var(--cream); opacity: 0.7;
  letter-spacing: 0.05em;
}}
.sidebar ul {{ list-style: none; margin: 0; padding: 0; }}
.sidebar .nav > li {{ margin-bottom: 16px; }}
.sidebar .nav-cat > span {{
  display: block; font-size: 10px; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--cream); opacity: 0.6;
  margin-bottom: 6px;
}}
.sidebar .nav-cat ul {{ padding-left: 0; }}
.sidebar .nav-cat ul li {{ margin: 2px 0; }}
.sidebar .nav-cat-cover {{ margin-bottom: 24px; }}
.sidebar a {{
  display: block; color: var(--cream); padding: 4px 8px;
  border-radius: 4px; border-bottom: none !important;
  font-size: 13px; line-height: 1.35;
}}
.sidebar a:hover {{ background: rgba(236, 226, 208, 0.1); color: var(--white); }}
.sidebar .nav-cat-cover a {{ font-family: var(--serif); font-size: 16px; color: var(--white); font-weight: bold; }}
.sidebar a.active {{ background: var(--cream); color: var(--navy); font-weight: bold; }}

main {{ padding: 0; }}

section {{
  max-width: var(--col); margin: 0 auto; padding: 64px 32px;
  border-bottom: 1px solid #f0f0f0;
}}
section:last-child {{ border-bottom: none; }}

.section-header {{ margin-bottom: 32px; }}
.cat-pill {{
  display: inline-block; font-size: 10px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--teal); font-weight: bold;
  margin-bottom: 8px;
}}

.cover {{
  background: var(--navy); color: var(--cream);
  max-width: none; min-height: 80vh; padding: 0;
  display: flex; align-items: center; justify-content: center;
  border-bottom: none; margin: 0;
}}
.cover-inner {{ max-width: 720px; padding: 64px 32px; text-align: left; width: 100%; }}
.cover-eyebrow {{ font-size: 12px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--cream); opacity: 0.7; margin: 0 0 24px; }}
.cover h1 {{ font-family: var(--serif); font-size: 72px; line-height: 1.0; color: var(--white); margin: 0 0 24px; font-weight: bold; }}
.cover-sub {{ font-family: var(--serif); font-size: 22px; line-height: 1.4; color: var(--cream); margin: 0 0 32px; }}
.cover-tag {{ font-family: var(--serif); font-size: 18px; color: var(--cream); opacity: 0.85; margin: 0 0 48px; }}
.cover-meta {{ font-size: 12px; color: var(--cream); opacity: 0.6; letter-spacing: 0.05em; margin: 0; }}
.block-anchor {{ font-family: var(--mono); }}

section h1 {{
  font-family: var(--serif); font-size: 36px; line-height: 1.15;
  color: var(--navy); margin: 0 0 16px; font-weight: bold;
}}
section h2 {{
  font-family: var(--serif); font-size: 30px; line-height: 1.2;
  color: var(--navy); margin: 0; font-weight: bold;
}}
.section-body h1 {{
  font-family: var(--serif); font-size: 28px; color: var(--navy);
  margin: 40px 0 16px; padding-top: 8px;
}}
.section-body h2 {{
  font-family: var(--serif); font-size: 24px; color: var(--navy);
  margin: 32px 0 12px;
}}
.section-body h3 {{
  font-family: var(--serif); font-size: 18px; color: var(--deep);
  margin: 24px 0 8px;
}}
.section-body p {{ margin: 0 0 14px; }}
.section-body ul, .section-body ol {{ margin: 0 0 16px; padding-left: 24px; }}
.section-body li {{ margin-bottom: 6px; }}
.section-body strong {{ color: var(--navy); }}
.section-body em {{ color: var(--teal); font-style: italic; }}

.section-body code {{
  font-family: var(--mono); font-size: 0.88em;
  background: var(--sand); color: var(--navy);
  padding: 1px 5px; border-radius: 3px;
}}
.section-body pre {{
  background: var(--sand); padding: 16px; border-radius: 6px;
  overflow-x: auto; font-size: 13px; line-height: 1.45;
  border-left: 3px solid var(--teal);
}}
.section-body pre code {{ background: transparent; padding: 0; }}

.section-body blockquote {{
  border-left: 3px solid var(--teal); margin: 16px 0;
  padding: 12px 16px; color: var(--charcoal);
  font-style: italic; background: var(--sand); border-radius: 0 4px 4px 0;
}}

.section-body table {{
  border-collapse: collapse; margin: 16px 0; width: 100%;
  font-size: 14px;
}}
.section-body th {{
  background: var(--navy); color: var(--white);
  padding: 8px 12px; text-align: left; font-family: var(--serif);
  font-weight: bold;
}}
.section-body td {{
  border: 1px solid #e5e5e5; padding: 8px 12px;
  vertical-align: top;
}}
.section-body tr:nth-child(even) td {{ background: var(--sand); }}

.section-body hr {{
  border: none; border-top: 1px solid #e0e0e0;
  margin: 32px 0;
}}

footer {{
  text-align: center; padding: 48px 32px;
  font-size: 12px; color: var(--charcoal); opacity: 0.7;
  border-top: 1px solid #f0f0f0; background: var(--sand);
  font-style: italic;
}}

@media print {{
  .sidebar {{ display: none; }}
  .layout {{ grid-template-columns: 1fr; }}
  section {{ break-inside: avoid; padding: 32px; max-width: none; }}
  .cover {{ min-height: auto; padding: 64px 32px; }}
}}
"""

js = """
(function() {
  var sections = Array.from(document.querySelectorAll('section[id]'));
  var navLinks = Array.from(document.querySelectorAll('.sidebar a'));
  if (!('IntersectionObserver' in window)) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        var id = e.target.getAttribute('id');
        navLinks.forEach(function(a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
  sections.forEach(function(s) { obs.observe(s); });
})();
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Retail vertical — proposal package · 2026-05-03</title>
<style>{css}</style>
</head>
<body>
<div class="layout">
{nav_html}
<main>
{sections_html}
<footer>
Wave session 2026-05-03 · eljeffe Hash and Seal Protocol · King Harbor — Redondo Beach — pier
</footer>
</main>
</div>
<script>{js}</script>
</body>
</html>
"""

out = OUTPUTS / "wave-deliverable.html"
out.write_text(html)
print(f"WROTE: {out}")
print(f"Size: {len(html):,} bytes")
print(f"Sections: {len(SECTIONS)}")
