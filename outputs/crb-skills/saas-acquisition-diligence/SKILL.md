---
name: saas-acquisition-diligence
description: Three-phase audit-as-diligence workflow for evaluating a SaaS / VAR acquisition (or channel-partnership) target. Phase 1 hypothesis grid (16 founder questions); Phase 2 ISO 27001:2022 audit-as-diligence with workload-estimator xlsx; Phase 3 valuation-impact and post-close-roadmap. Wraps the cost-model skill (which it calls for sizing) and adds the audit framework + the buy-in voice + the glide-path artifacts. First concrete run is RapidPOS LLC; methodology generalizes to any Counterpoint VAR (RCS, AMS, Mariner, regional resellers) or analogous SaaS target. Output is simultaneously the audit report, the M&A valuation discount math, and the post-close modernization roadmap.
trigger phrases:
  - "run [company] through CRB acquisition"
  - "audit [company] for ISO 27001"
  - "diligence [company]"
  - "SaaS buy diligence"
  - "what's the workload to make [company] compliant"
  - "GCP onramp playbook for [target]"
  - "is [company] DriftPOS-ready"
  - "managed-services glide path for [target]"
  - "evaluate this VAR / channel partner"
status: rebuilt 2026-05-03 from prompt-crb-saas-acquisition-skill.md spec
---

# saas-acquisition-diligence — skill entry point

The audit-as-diligence workflow that turns a SaaS / VAR target into three simultaneous outputs: an audit report (what's the gap), valuation discount math (what we pay), and a post-close modernization roadmap (what we do).

## What this skill exists for

Every Counterpoint VAR (and analogous SaaS target) has the same operational state at the moment a buyer or channel partner shows up: 15-25 years of accumulated configuration knowledge in 2-3 senior heads; informal-or-absent ISMS posture; a support queue eating the team's growth capacity; customers driving compliance pressure that's not yet formal; a 20-year owner-operator looking to exit clean within the next 36 months. The financial gap (cost to make the asset productive at modern customer-data-in-cloud standards) is the load-bearing variable in deal pricing. This skill produces that number — defensibly, with hypothesis-first transparency, in three scenarios.

## When to invoke

- Diligencing a Counterpoint VAR for acquisition or channel partnership (RapidPOS first; RCS, AMS, Mariner, regional resellers after)
- Evaluating any SaaS target where the owner-operator is exiting and the asset needs ISO 27001 / SOC 2 readiness work
- Producing a managed-services glide-path proposal for a target where acquisition is one path among several
- Assessing DriftPOS launch readiness for a target's customer book
- Comparing multiple targets side-by-side via the cost-model skill's `vars-pipeline.xlsx`

## How the skill operates — three phases

**Phase 1 — Hypothesis grid.** Capture founder's verbatim answers to the 16 hypothesis questions in `templates/hypothesis-grid.md`. Confidence labels per answer: (confirmed) / (signal) / (guess) / (unknown). Founder's exact words become the audit baseline; do not smooth.

**Phase 2 — Audit-as-diligence.** Run all 93 ISO 27001:2022 Annex A controls (per `reference/02-iso27001-2022-control-library.md`) against the hypothesis grid. For each control, map current-state hypothesis → gap severity → engineering hours → $ → calendar weeks. Map each gap to the GCP-native remediation per `reference/03-gcp-control-mapping.md`. Surface the 15 critical-mass DriftPOS-blocking controls (per `reference/07-driftpos-readiness-gate.md`) as the Phase A subset. Output: `templates/workload-estimator.xlsx` with 230 formulas across 93 control rows × hypothesis × hours × $ × weeks columns; flexible to founder-driven assumption changes.

**Phase 3 — Valuation impact + glide path.** Convert the gap inventory to deal pricing using the formulas in `reference/06-valuation-impact-formulas.md`. Three scenarios (best / expected / worst). Produce `templates/diligence-report.docx` (auditor-facing internal output), `templates/deal-narrative-onepager.md` (founder-facing strategic summary), and `templates/post-close-roadmap.md` (24-month migration sequence). The external-facing artifacts — `managed-services-glide-path.md` and `glide-path-deck.pptx` — operate per the buy-in voice rules below.

## Posture and voice — the buy-in mechanics

The posture is not pitch atmospherics. **The posture is the mechanism by which the seller buys in.** Every seller-facing artifact executes this mechanism. Hard rule.

The stance is peer-to-peer. Expert to expert. No patronizing, no adversarial.

**Five moves, in order:**

1. **Establish the gate.** ISO 27001 is the floor for any serious customer-data-in-the-cloud conversation. State it as landscape, not as our requirement. We didn't invent it; the world ran ahead.
2. **Grant peer status inside the conversation.** *We both know this.* The seller either nods (he knew, we just confirmed alignment) or he updates silently (he didn't, and we let him without losing face).
3. **Make non-action visible as a choice.** Without certifiable posture, no DriftPOS rollout, no Global-50 anchor, no acquisition at the price he wants. Status quo is not stable.
4. **Position transformed Growdirect as the credible, cheapest, fastest path.** We are the auditor. We are the modernizer. We have the agentic workload. We have ILDWAC and CRDM. We have the GCP blueprint at every scale tier. The TCO of using us is below alternatives.
5. **Let him conclude.** Lay out math, glide path, price band; let the operator do the arithmetic himself. Operators close themselves when the standard is clear and the path is cheaper.

**Voice rules from this stance:**

- **"We both know."** Use this construction; invites shared expertise instead of explaining down.
- **State standards as facts, not threats.** ISO 27001, PCI-DSS, SOC 2 Type II are the landscape, not our invention.
- **Name the gate plainly.** Without certifiable posture, the conversations the seller wants don't happen.
- **Position dual hat acknowledged honestly.** Auditor and partner who solves it. *You can pick another auditor and another modernizer if you want — and you should price that path against ours.*
- **Never lecture.** No paragraph that reads like a compliance primer.
- **No theater language.** No "best-in-class," no "industry-leading," no "comprehensive solution." Operators detect filler immediately.
- **Acknowledge what he already knows.** Counterpoint knowledge real, customer relationships real, vertical-specialty instincts real. Lead with what he brings, not what he's missing.
- **Be willing to walk.** The pitch is strong because we don't need this deal at any price. Direct, unhurried, factual.

**Internal-only artifacts (`06-internal-deal-memo.md`, hypothesis-grid notes):** drop the diplomacy. Direct operator language: "He doesn't know about ISMS." "Probably no inherited PCI scope past SAQ-A." "Suitor X will lowball; we should anchor first." This is the room where we say what we actually think.

## Strategic horizon — Patient Zero, not the deal

This skill is being built because the same problem exists across every Counterpoint VAR. RapidPOS is the first run because we have the relationship and the DriftPOS partnership lined up — but the playbook is designed to be re-run against every VAR in the same posture.

1. Get in at RapidPOS. Burn down the queue, capture the wikis, modernize the eager cohort, certify the posture, land DriftPOS.
2. Generalize from the first run. Every reference doc, every template, every parameter must be re-runnable against another VAR with minimal customization. RapidPOS-specific facts live in `Brain/diligence/rapidpos/`, not in the skill scaffold.
3. Find the others — RCS, AMS, Mariner, regional resellers. Run the skill on each, score the pipeline (via cost-model `vars-pipeline.xlsx`), prioritize.
4. Repoint the partner team. After RapidPOS proves the model, the partner team's trajectory shifts: same headcount, *more onboarding work, less support work, more growth-related activity, less life-support.* Each VAR sends a wave of customer onboardings to the partner team; each onboarding is a templated execution (A4 captured playbook), not a bespoke project.

**Reusability is a quality bar, not a nice-to-have.** After the RapidPOS run is complete, exercise the skill against a second target (real or synthetic) to prove the bar held. If anything required rewriting the skill, the skill is not done.

## Implementation model — agentic workflows over the seller team

The commercial value to the seller is not "buy you and replace your people." It is "deploy agents alongside your people so your people can do the work that's actually valuable, while we burn down the work that's eating them alive."

**Day-1 agentic workflows ship within 90 days post-close. Five dispatches:**

| # | Agent / workflow | Mission | Dispatch type |
| --- | --- | --- | --- |
| A1 | Support-queue burndown | Triage every open ticket; auto-resolve against contextual wiki; escalate genuinely novel | continuous, queue-driven |
| A2 | Root-cause analysis | Cluster recurring tickets; surface top 10 repeat-causes; drive each to permanent fix or runbook | weekly + on-spike |
| A3 | Contextual-wiki builder | Every resolved ticket → wiki article; every recurring config → playbook; every undocumented customization → captured fact | continuous, ticket-driven |
| A4 | Cloud-onboarding process capture | Ride along on every customer cloud-migration; capture seller team's actual config moves; codify into per-vertical onboarding playbooks | continuous, migration-driven |
| A5 | Integration-bus reverse-engineer (internal) | Map customer Counterpoint schemas onto CRDM; profile each customer's ILDWAC-conversion difficulty; surface what's outside standard API | parallel, founder-directed |

**Burn-down → repeatability flywheel.** Phase A (M0-6): burn down the queue; A1+A2 absorb recurring causes; A3 builds wiki capital. Phase B (M6-18): wiki coverage hits critical mass; A1 auto-resolution scales; A4 captures onboarding craft as repeatable playbooks; cohort migrations begin in volume. Phase C (M18-36): onboarding playbooks scale; new-logo wins land at multiples of historical pace; Global-50 anchor becomes feasible.

## Reference contents

| File | Purpose |
| --- | --- |
| `reference/01-crb-method-three-phases.md` | The three-phase methodology: hypothesis / audit-as-diligence / valuation-and-glide-path |
| `reference/02-iso27001-2022-control-library.md` | Full Annex A 93 controls grouped by 4 themes (Organizational 37, People 8, Physical 14, Technological 34) |
| `reference/03-gcp-control-mapping.md` | ISO control → GCP-native service & evidence; gaps where no GCP-native answer exists |
| `reference/04-ncr-counterpoint-substrate.md` | What RapidPOS-deployed Counterpoint looks like operationally; what lives outside the standard API |
| `reference/05-saas-buyout-archetypes.md` | SysRepublic-2015 archetype + others; how to specialize |
| `reference/06-valuation-impact-formulas.md` | Gap-to-discount math; FTE-to-weeks conversion; six valuation formulas |
| `reference/07-driftpos-readiness-gate.md` | Post-close DriftPOS launch criteria mapped to controls; the 15 critical-mass subset |

## Template contents

| File | Purpose |
| --- | --- |
| `templates/hypothesis-grid.md` | Phase 1 fillable grid (16 founder questions) |
| `templates/workload-estimator.xlsx` | Phase 2 — 93 controls × hypothesis × hours × $ × weeks; ~230 formulas |
| `templates/diligence-report.docx` | Phase 3 — auditor-facing internal output template |
| `templates/deal-narrative-onepager.md` | Phase 3 — founder-facing strategic summary |
| `templates/post-close-roadmap.md` | Phase 3 — 9-24-month sequenced work plan |

## Quality bar

- **SKILL.md ≤ 200 lines.** Discoverable by the trigger phrases above without ambiguity.
- **Control library reference must list the actual 93 ISO 27001:2022 Annex A controls** (not Annex A from the 2013 version — they collapsed). Group by 4 themes: organizational (37), people (8), physical (14), technological (34).
- **GCP mapping must name specific GCP service** + the audit-evidence artifact that satisfies each control. Where no GCP-native answer exists, name the gap and propose third-party tooling (e.g., Vanta, Drata) only as fallback.
- **Workload estimator xlsx must have formulas, not constants.** Founder will flex assumptions live and watch the schedule and discount move.
- **Counterpoint substrate doc must be technically honest** about what Counterpoint exposes and what RapidPOS's proprietary layer adds outside the API.
- **Deal narrative one-pager is internal-use first.** Never assume it goes to the seller.

## Anti-goals

- Do not generate generic SaaS-acquisition consulting content. The CRB family is sharper than that.
- Do not blur RapidPOS and DriftPOS. They're separate companies in this story.
- Do not optimize for "compliance theater." Every control gap is a real engineering / process item with cost + calendar.
- Do not assume the seller has answers. Treat hypothesis-first as a feature, not a placeholder.
- Do not write a Stage-1 audit prep document. Write a Stage-2-readiness diligence + remediation plan.

## Cross-references

- This skill calls `crb-skills/cost-model/` for sizing (ILDWAC + CRDM + GCP); the cost-model output `.xlsx` feeds Phase 2's workload estimator and Phase 3's valuation impact
- Output for any target lives at `Brain/diligence/<vendor-slug>/`; first run populates `rapidpos/`
- The bylaws skill (`crb-skills/namespace-bylaws/`) operates the substrate's governance; this skill targets external entities (acquisition or partnership candidates)
- Linear: `Canary.GO` project; `RapidPOS Channel` initiative; GRO-762 (Bart conversation prep); GRO-739 (DriftPOS integration parent)

---

*Three phases. One target. The audit is the diligence. The diligence is the deal.*
