# Burn-down → Repeatability Flywheel — RapidPOS

> How Phase A→B→C unlocks the Year-3 throughput. Internal narrative; aligned with the external glide-path memo.

**Vendor:** RapidPOS LLC
**Run date:** 2026-05-03

---

## The flywheel, in one diagram

```
PHASE A (M0-6) — BURN DOWN
    ↓
A1 absorbs recurring-cause tickets → backlog drops
A3 captures resolutions as wiki articles → coverage rises
A2 drives top causes to permanent fixes → inflow drops
A5 maps schemas in parallel (no team load)
    ↓
Bart team labor mix shifts: 35% break-fix → 25%
    ↓
PHASE B (M6-18) — COHORT ROLLOUT
    ↓
Wiki coverage reaches critical mass (60%+)
A1 auto-resolution rate hits 50%+
A4 starts capturing onboarding playbooks during cohort migrations
    ↓
Bart team time freed → onboarding work expands
DriftPOS GA at month 12 → migration revenue accelerates
ISO 27001 certified at month 18 → enterprise gate cleared
    ↓
Bart team labor mix: 45% onboarding, 15% break-fix
    ↓
PHASE C (M18-36) — SCALE
    ↓
Onboarding is templated execution, not bespoke craft
A4 playbooks cover all 5 verticals
New-logo wins land at multiples of historical pace
T2 → T3 capacity build for anchor accounts
    ↓
Bart team labor mix: 70% onboarding, 5% break-fix
    ↓
Same headcount, multi-fold throughput
VAR #2 deal in active diligence using same playbook
```

## Phase A in detail

The first six months are about converting tribal knowledge into institutional knowledge while reducing the volume of tribal-knowledge-required work.

**The dynamic:**
- Day 1: ~120 open tickets. Senior engineers spending ~60% of their time on tickets. Wiki effectively empty.
- Week 4: A1 categorizing. A3 has 200 articles seeded from existing docs. A2 produces first repeat-cause report.
- Month 1: A1 auto-resolves 15% of inflow. Wiki has 350 articles. Senior engineer time on tickets drops to 50%.
- Month 3: A1 auto-resolves 35%. Wiki at 1,000 articles, 30% coverage rate. A2 has driven 4 permanent fixes. Senior engineers at 35% on tickets.
- Month 6: A1 at 50%. Wiki at 2,000 articles, 60% coverage. Senior engineers at 25% on tickets, the rest available for higher-value work (cloud onboarding, vertical specialization, customer relationship management).

**The leading indicators that say it's working:**
- Wiki-article-write rate sustained >50/week
- Repeat-cause volume down >15% month-over-month
- Senior engineer escalation rate (% of A1-handled tickets they get pulled into) <20%
- Customer satisfaction stable or rising (the modernization shouldn't degrade experience)

**The leading indicators that say it's stalling:**
- Wiki-coverage rate plateaus below 40%
- A1 false-positive rate (auto-resolved → re-opened) >8%
- Senior engineer pushback on agent suggestions (signals quality issues)
- Customer-side complaints about "less personal" responses

If stalling indicators trigger, the response is *more wiki investment*, not less. The agent is only as good as the knowledge it can reference.

## Phase B in detail

Months 6-18 is about converting the freed capacity into customer migrations.

**The dynamic:**
- Month 6: First eager-cohort customer in sandbox migration. A4 captures every config move.
- Month 9: ISO Stage 1 audit clean. Three eager-cohort customers in production on Canary.GO + DriftPOS sandbox.
- Month 12: DriftPOS GA. Stage 2 observation begins. Eager-cohort wave 1 (5-10 customers) in production. A4 has produced first vertical-specific playbook (garden-center).
- Month 15: Eager-cohort wave 2 underway. Steady cohort begins. Garden-center playbook battle-tested; wine-direct-ship playbook drafted.
- Month 18: ISO 27001 certified. All eager-cohort migrated. Steady cohort migrating in volume. 3 of 5 vertical playbooks production-ready.

**The Bart-team labor-mix shift accelerates:**
- Month 6: 25% onboarding, 25% break-fix
- Month 12: 45% onboarding, 15% break-fix
- Month 18: 55% onboarding, 10% break-fix

**The leading indicators:**
- Per-migration elapsed weeks dropping (target: 12 weeks at start of phase, 6 weeks at end)
- Per-migration FTE-hours dropping (target: 60% reduction by end of phase)
- Customer satisfaction post-migration sustained (>4/5)
- New-logo conversations starting to land

## Phase C in detail

Months 18-36 is about scaling the playbook to multi-VAR throughput and landing the anchor account.

**The dynamic:**
- Month 18-24: Steady cohort migration completes. New-logo wins from outside RapidPOS book begin. T2 capacity built. SOC 2 Type II observation begins.
- Month 24-30: Steady cohort migrated. Volume of new-logo wins rises. SOC 2 Type II certified. VAR #2 deal in diligence using the same playbook.
- Month 30-36: New-logo wins at full pace. Anchor account in pre-pilot or pilot. T3 capacity comes online if anchor materializes. VAR #3 candidate identified.

**Bart team labor mix at end of Phase C:**
- 70% onboarding (the "growth-related activity" the founder named)
- 5% break-fix
- 10% customizations (specialty work that's actually rare and valuable)
- 15% other (sales support, internal improvement, vertical R&D)

**Same headcount, multi-fold throughput:**
- Year 0: ~1 customer onboarding per month per team (12/year)
- Year 3: ~10 customer onboardings per month per team (120/year)

This 10× expansion is what makes the strategic horizon (T3 Global-50 footprint, VAR roll-up across 4 VARs) achievable without proportionally scaling Bart's team. It's the operational core of the unit-economics story.

## What breaks the flywheel

- **Wiki coverage stalls.** Phase A's wiki-build is the load-bearing investment. If A3 doesn't reach 60% coverage by M6, A1's auto-resolution stays low, the queue doesn't burn down, the team stays trapped in break-fix, and Phase B can't begin in earnest. Mitigation: prioritize A3 in Phase A; measure coverage as a gate.
- **Senior engineer turnover during Phase A.** The senior engineers carry the tribal knowledge A3 needs to extract. If one or two leave during the burn-down phase, wiki quality collapses. Mitigation: retention package as part of acquisition close; visibility into the better-work-coming-soon trajectory.
- **DriftPOS partnership unwinds.** DriftPOS GA at M12 is the gate to cohort migration in volume. If the partnership stumbles (Bart team turnover; technical disputes; commercial breakdown), the flywheel can't enter Phase B. Mitigation: secure the partnership pre-close; maintain Counterpoint as fallback front-end.
- **Cohort migration slower than modeled.** If eager customers don't actually move when given the option, A4 can't capture playbooks, B's onboarding revenue doesn't materialize, and the team doesn't have growth work to consume the capacity A1 freed up. Mitigation: customer interviews pre-close to validate the cohort hypothesis.
- **Customer-bespoke depth higher than archetype.** If real RapidPOS customers have heavier per-customer customization than expected, A4 captures less reusable content per migration, and the templating efficiency gain in Phase B underperforms. Mitigation: sample several customers' actual configurations during diligence.

## Why the flywheel matters for the deal

The deal's economic viability depends on *throughput expansion*, not *cost reduction*. Bart's team size doesn't shrink; it produces multi-fold more. RapidPOS's senior team doesn't get displaced; their work shifts to where their craft has highest leverage.

The walking price math (per `04-valuation-impact.md`) reflects current-state economics. The strategic upside (per the same doc) reflects the throughput expansion the flywheel enables. The deal pays for itself on current-state alone; the flywheel is the asymmetric upside.

Without the flywheel, this deal is mediocre. With the flywheel, it's the platform investment for the VAR roll-up thesis.

## Cross-references

- `09-day1-agentic-ops-plan.md` — A1-A5 deployment specifics
- `crb-skills/cost-model/reference/08-bart-team-labor-trajectory.md` — labor-mix targets per quarter
- `crb-skills/saas-acquisition-diligence/templates/post-close-roadmap.md` — phase-by-phase milestone schedule
- `Brain/diligence/rapidpos/06-internal-deal-memo.md` — strategic-context section
- `Brain/diligence/rapidpos/07-managed-services-glide-path.md` — external narrative companion
