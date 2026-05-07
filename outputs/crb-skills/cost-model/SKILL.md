---
name: cost-model
description: Reusable cost-modeling skill that takes a target retailer (or fleet of retailers) and produces a defensible $ + weeks + FTE estimate for migrating their stack onto Canary.GO + GCP. Three load-bearing instruments inside the skill — ILDWAC conversion difficulty, CRDM mapping complexity, GCP workload blueprint at four scale tiers (T0–T3). Output is `cost-model-output.xlsx` with 8 named tabs that any consuming skill (acquisition diligence, partner evaluation, anchor-account sizing) can ingest as a single artifact. Standalone — anyone running a single-customer cost estimate for a Canary.GO sale should use this skill.
trigger phrases:
  - "cost model this customer"
  - "size the migration for [target]"
  - "what does it cost to land [customer]"
  - "Canary.GO onramp cost"
  - "ILDWAC + CRDM sizing"
  - "cost basis conversion estimate"
  - "score this VAR / partner / cohort"
  - "ramp the unit economics"
status: rebuilt 2026-05-03 from prompt-crb-saas-acquisition-skill.md spec
---

# cost-model — skill entry point

Producing the financial estimate for any Canary.GO migration target. Reusable, scenario-flexible, scale-tier-aware.

## What this skill exists for

Every migration of a customer (or fleet of customers) onto Canary.GO + GCP needs a cost estimate that cross-foots three lenses simultaneously:

1. **ILDWAC conversion lift** — converting the target's current Counterpoint MAC-only inventory cost basis to the Canary.GO ILDWAC five-dimension basis (item × location × device × MCP × port × weighted-average-cost; patent #63/991,596). Per-customer difficulty is a function of device count, port mix (single-vendor RapidPOS-deployed Counterpoint vs. multi-vendor), and serialized-inventory share. Output: satoshi-denominated lift per cohort, expressed in fiat at the report layer.

2. **CRDM mapping complexity** — mapping the target's installed Counterpoint schemas plus VAR-proprietary tables onto the Canary Retail Data Model (anchored on GSLM, the Walmart International data model from 2009). Output: rows × columns × adapter-complexity × cohort → per-customer migration cost and elapsed-weeks.

3. **GCP workload blueprint at scale tier** — the fully-blueprinted, totally-costed GCP footprint Canary.GO runs, decomposed by workload type (18 workloads) × volume tier (T0 RapidPOS-today through T3 Global-50-anchor). The blueprint translates a target's current scale into projected GCP run-cost at each migration milestone.

The three lenses produce a single artifact — `cost-model-output.xlsx` with eight named tabs — that any consuming skill ingests for sizing. The `target-profile.md` template captures inputs; the `cohort-segmentation.md` template splits the customer base into eager / steady / laggard cohorts; the workbook re-cross-foots when assumptions flex.

## When to invoke

- Sizing the migration for any single Canary.GO customer (a direct sale)
- Sizing the migration for a target VAR's customer book (an acquisition diligence run, channel-partner evaluation, or anchor-account scoping)
- Comparing multiple VAR candidates side-by-side via the `vars-pipeline.xlsx` template (the portfolio view)
- Stress-testing whether T3 (Global-50 anchor) economics work under best/expected/worst scenarios
- Updating the cost model when GCP pricing or workload sizing changes (refresh `reference/04-gcp-pricing-snapshot-YYYY-MM-DD.md` quarterly)

## How the skill operates

1. **Capture target inputs** with `templates/target-profile.md` — 20-field form covering revenue, EBITDA, customer count, store count, vertical mix, team shape, deployment posture, modernization appetite, suitor landscape, etc.
2. **Segment the target's customers** with `templates/cohort-segmentation.md` — eager / steady / laggard split with sizing inputs per cohort.
3. **Compute the three lenses** against the inputs:
   - ILDWAC conversion lift per `reference/01-ildwac-conversion-difficulty.md`
   - CRDM mapping complexity per `reference/02-crdm-mapping-complexity.md`
   - GCP workload sizing per `reference/03-gcp-workload-blueprint.md` and `reference/04-gcp-pricing-snapshot-YYYY-MM-DD.md`
4. **Apply the cohort archetypes** from `reference/05-cohort-profile-archetypes.md` to project per-cohort migration sequencing.
5. **Convert engineering hours to calendar weeks** per `reference/06-fte-to-weeks-conversion.md` (capacity assumptions, dependency graph, parallelism limits).
6. **Surface the labor-trajectory shift** for the seller team per `reference/08-bart-team-labor-trajectory.md` (break-fix → onboarding → growth-related work over Y0→Y3).
7. **Cross-foot into `templates/cost-model-output.xlsx`** — eight tabs (target / customers / ildwac_lift / crdm_lift / gcp_infra / program_cost / glide_path / assumptions). Three scenarios: best / expected / worst.
8. **Pair with narrative companion** `templates/cost-model-output.docx` — what the numbers mean, where the sensitivity is, what's load-bearing.
9. **For VAR-pipeline scoring**, use `templates/vars-pipeline.xlsx` — score multiple targets side-by-side, prioritize sequence.

## Voice and posture

- **Hypothesis-first.** Founder's verbatim answers to the target-profile fields, with confidence labels: (confirmed) / (signal) / (guess) / (unknown). Don't smooth the founder's exact words; they're the audit baseline.
- **Numbers do the talking.** No editorializing in cell comments. Each line shows the input, the formula, the result. The voice is in the absence of voice.
- **Three-pronged differentiation surfaced.** Better retail capability (CRDM + ILDWAC depth vs. Clover/Toast/Square shallow back-office); front-end interchangeability (Counterpoint + DriftPOS + Square + Toast + Clover all valid front-ends); native multi-jurisdiction tax + regulatory compliance (no Avalara/Vertex bolt-ons; substrate connects directly to gov APIs).
- **Strategic horizon explicit.** RapidPOS is Patient Zero; the methodology is the asset; the cost-model template stays target-agnostic and gets re-run against subsequent VARs (RCS, AMS, Mariner, regional resellers).

## Reference contents

| File | Purpose |
| --- | --- |
| `reference/01-ildwac-conversion-difficulty.md` | How to score a target's ILDWAC-conversion lift |
| `reference/02-crdm-mapping-complexity.md` | How to score a target's CRDM-mapping lift |
| `reference/03-gcp-workload-blueprint.md` | 18-workload architecture at every scale tier (T0-T3) |
| `reference/04-gcp-pricing-snapshot-YYYY-MM-DD.md` | Current GCP pricing for the relevant SKUs (refreshed quarterly) |
| `reference/05-cohort-profile-archetypes.md` | Eager / steady / laggard cohort definitions |
| `reference/06-fte-to-weeks-conversion.md` | How engineering hours convert to calendar weeks |
| `reference/07-var-landscape-map.md` | Known Counterpoint VARs (RapidPOS, RCS, AMS, Mariner, regional) + identifying signals |
| `reference/08-bart-team-labor-trajectory.md` | How the seller team's labor mix shifts from break-fix to onboarding-led across Y0→Y3 |

## Template contents

| File | Purpose |
| --- | --- |
| `templates/target-profile.md` | 20-field input form for one target VAR |
| `templates/cohort-segmentation.md` | How to split a target's customer base into cohorts |
| `templates/cost-model-output.xlsx` | Standard report-card spreadsheet — ILDWAC + CRDM + GCP, three scenarios, 8 named tabs |
| `templates/cost-model-output.docx` | Narrative companion to the spreadsheet |
| `templates/vars-pipeline.xlsx` | PORTFOLIO view — score multiple VARs side-by-side, prioritize sequence |

## Standard output — `cost-model-output.xlsx`

Eight named tabs that any consuming skill (acquisition diligence, partner evaluation, anchor-account sizing) ingests as a single artifact:

| Tab | Contents |
| --- | --- |
| `target` | Target identity, hypothesis confidence levels |
| `customers` | Customer cohort segmentation (eager / steady / laggard) with sizing inputs per customer |
| `ildwac_lift` | Per-cohort ILDWAC conversion lift in satoshis + fiat |
| `crdm_lift` | Per-cohort CRDM mapping lift in adapter-hours + dollars |
| `gcp_infra` | Steady-state GCP run cost per cohort post-migration |
| `program_cost` | All-in program cost: people + GCP + ILDWAC + CRDM, three scenarios (best / expected / worst) |
| `glide_path` | 24-month migration sequence with cohort waves and milestones |
| `assumptions` | Every assumption that drives the math, with founder-editable cells |

Lock the tab structure. Consuming skills depend on this contract.

## Quality bar — the second-target test

Run the skill against a second target (real or synthetic) after the first run completes. If anything required modifying the skill scaffold to accommodate the second target's specifics, the skill is not done. Per-target facts live in `Brain/cost-models/<vendor-slug>/`; the skill scaffold stays target-agnostic.

## Cross-references

- ILDWAC: `Brain/wiki/cards/canary-ildwac.md`; SDD: `docs/sdds/go-handoff/ildwac.md`
- CRDM: `Brain/wiki/` retail-* card family; Linear project "Canary Data Model" (44986f35-8362-42f1-90b4-9b808ad412cd)
- GSLM (CRDM's anchor): founder's Walmart International 2009 model
- Bart's team labor trajectory: cross-references the diligence skill's day-1 agentic ops plan (A1-A5)
- The acquisition-diligence skill (`crb-skills/saas-acquisition-diligence/`) is the primary consumer of this skill's output

---

*The cost model is the substrate of every venture-economic decision. This skill produces it.*
