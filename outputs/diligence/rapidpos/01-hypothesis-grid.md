# Hypothesis Grid — RapidPOS LLC

> **DEMO RUN — archetype-default placeholders.** Founder's verbatim answers will replace these. Every answer carries a confidence label: **(confirmed)** / **(signal)** / **(guess)** / **(unknown)**. The (guess) placeholders below are not commitments — they are starting hypotheses for the founder to correct.

**Vendor:** RapidPOS LLC
**Run date:** 2026-05-03
**Captured by:** ALX (demo-mode synthesis)
**Skill version:** saas-acquisition-diligence v1.0

---

## Q1 — Revenue & customer mass

**Answer:** ~50 customers across specialty verticals (garden, gun, wine, specialty food, feed-and-tack); ~500-2,500 stores aggregate; ARR ~$2.7M (placeholder mid-point)

**Confidence:** (guess) — archetype default; founder to specify

**Notes:** Memory-bus has Rapid POS as "medium SMB VAR" supporting "boutique H&G chain (~25 stores)" as one engagement. Several similarly-sized customers across verticals would be consistent. Not validated.

---

## Q2 — Stack & deployment reality

**Answer:** Most customers run NCR Counterpoint on-prem at the store; some larger customers run Counterpoint hosted in their own cloud (AWS/Azure VMs). RapidPOS's own engineering and support stack is a mix — likely on-prem fileservers + a few SaaS tools (Salesforce or HubSpot for sales, Atlassian or Monday for project tracking, M365 or G-Suite for email).

**Confidence:** (guess) — archetype default

**Notes:** Founder to confirm RapidPOS's own stack — the ISO 27001 audit applies to *RapidPOS's* operations, not the customer-side Counterpoint instances directly.

---

## Q3 — Engineering team shape

**Answer:** ~6-12 total headcount. ~3-5 senior engineers carrying deep Counterpoint config knowledge (15-20 year tenure typical). ~2-3 mid-level engineers. Junior staff minimal. No dedicated security/IT role; senior engineers wear that hat informally. No compliance-aware ops staff.

**Confidence:** (guess)

**Notes:** This is the load-bearing hypothesis for A1-A4 sizing. Founder must confirm. Especially: who are the 2-3 senior engineers carrying tribal knowledge, and are any flight risks?

---

## Q4 — Customer compliance pressure

**Answer:** Increasing. Firearms dealers (per ATF rules) and wine direct-shippers (per state regs) have active compliance demands flowing upstream. Garden-center customers in regulated states (CA, NY) starting to ask. Some standard PCI-DSS SAQ-A customer questionnaires answered ad-hoc each year. No documented breaches publicly.

**Confidence:** (guess)

**Notes:** The compliance-pressure factor in valuation-impact-formulas (Formula 1) defaults to 0.7 for moderate compliance pressure. If founder reports acute pressure, it goes to 0.85-1.0. If it's all theoretical, drops to 0.5.

---

## Q5 — Existing certifications

**Answer:** Likely none formal. Customers inherit PCI-DSS posture from their Counterpoint deployment + Square/Stripe/Heartland-style payment processors, generally at SAQ-A level. No SOC 2. No ISO. Rapid as the VAR has answered customer questionnaires but never gone through a formal third-party audit.

**Confidence:** (guess)

**Notes:** SAQ-A means card data never touches the merchant's systems (tokenized via the payment terminal directly to the processor). RapidPOS likely has been able to answer customer questions truthfully on this without needing certifications. Founder to confirm.

---

## Q6 — Suitor landscape & deal pressure

**Answer:** Probably 1-2 other interested parties. PE rollup play is the most likely competitive scenario — Counterpoint VAR consolidation by Vista, Insight, or similar mid-market PE firms is a known pattern. NCR Voyix direct interest unlikely but possible. Other Counterpoint VARs (RCS, AMS, Mariner) might also consider tuck-in acquisition. Implicit clock probably 6-12 months — owner is "modernizing to sell" not "thinking about selling someday."

**Confidence:** (guess)

**Notes:** This is critical for deal-pacing. If founder confirms a hot competitive process, we move faster on Phase 1-2 to anchor first.

---

## Q7 — DriftPOS rollout assumptions

**Answer:** Bart's team plan is to land first with the most willing eager-cohort customers — likely 3-5 multi-store specialty retailers who've already asked about modernization. DriftPOS launch target: ~6 months post-RapidPOS-close (M6 from acquisition; aligns with Phase A end and the cleared support-queue + initial wiki coverage). Customer commitments in flight: assume the H&G chain mentioned in earlier dispatches is one (the boutique 25-store engagement).

**Confidence:** (guess) — derived from memory-bus references to Bart conversation prep + the H&G chain dispatch

**Notes:** Cross-reference Bart prep doc (GRO-762) for the actual DriftPOS GA target.

---

## Q8 — Modernization appetite of the seller

**Answer:** Senior team likely conservative on modernization but understands that the path forward requires it. Will need to be sold on the GCP onramp narrative — they don't naturally think in cloud-native terms. ISMS is foreign territory; they understand "audits" as in financial/PCI-DSS but not as in continuous-monitoring SOC-2-style ISMS. Will stay through transition under a retention package; they want a clean Y3-5 exit, not abrupt rip-and-replace.

**Confidence:** (guess)

**Notes:** This is the load-bearing assumption for the managed-services glide path. If founder confirms, it validates the 24-month-transition + Y3-5-exit pitch shape.

---

## Q9 — Budget & timeline reality

**Answer:** Cash budget is *what the deal can fund*, not pre-existing. Tolerance for elapsed time post-close before certification: ~12-18 months feels right (M12 DriftPOS GA, M18 ISO 27001 cert). Growdirect FTE willing to dedicate during onramp: ~2-4 senior engineers + founder oversight + Bart's team augmenting on integration work.

**Confidence:** (guess) — Growdirect-side budget is founder's call

**Notes:** The cost-model program_cost numbers should be sized against this Growdirect-side capacity assumption.

---

## Q10 — Legal posture

**Answer:** Likely asset purchase preferred (cleaner liability inheritance, tax structure for both parties). Reps & warranties standard mid-market deal terms — comprehensive but not aggressive. Earnout structure for owner over 12-24 months tied to customer-retention milestones.

**Confidence:** (guess)

**Notes:** Asset vs. stock purchase changes whether RapidPOS LLC's pre-close compliance gaps become Growdirect's post-close liability or stay with the seller's entity. Asset purchase is the cleaner path; founder + counsel to confirm.

---

## Q11 — DriftPOS architectural constraints

**Answer:** DriftPOS's .NET stack constrains where some integration components can run (Anthos GKE supports .NET Core but legacy .NET Framework needs Windows containers — verify which DriftPOS uses). Ingenico pinpad PCI scope means Canary.GO never sees raw cardholder data; only tokenized payment fingerprints. The GCP onramp design must respect this — no cardholder data flows through Pub/Sub or Cloud SQL; tokenization happens at the pinpad.

**Confidence:** (signal) — derived from Bart conversation prep doc memory recall

**Notes:** Bart prep doc OQ-2 (Ingenico network token availability) and OQ-11 (PCI scope) are load-bearing for this answer. Resolution of those two OQs in the Zoom session will tighten this hypothesis.

---

## Q12 — VAR-specific tables / DB extensions

**Answer:** Likely "light to medium" — Rapid's vertical specialization (garden mix-and-match pricing, firearms NICS workflow, wine direct-ship compliance) is mostly in Counterpoint *configuration* and UI customization, not in custom tables. Some customer-bespoke fields may use Counterpoint's stock 5×4 profile slots. Probably 5-15 customer-specific custom tables across the entire book.

**Confidence:** (guess) — from CRB wiki article on Counterpoint-Rapid relationship

**Notes:** This number drives CRDM mapping complexity per `cost-model/reference/02-crdm-mapping-complexity.md`. If founder reports significantly more (say 30+ custom tables), CRDM mapping difficulty per customer rises.

---

## Q13 — Support queue shape

**Answer:** Open ticket count: ~80-150. Weekly inflow: ~30-50 tickets. Avg time-to-resolve: 3-7 days (depends on category). % repeat-cause: high (~60-70%) — this is the load-bearing observation for the agentic-burndown thesis.

Top issue categories (archetype-default):
1. Counterpoint config questions ("how do I add a new department / vendor / pricing rule")
2. Receipt printer / scanner / scale device issues
3. End-of-day cash drawer reconciliation problems
4. Vendor-portal sync errors (PO/EDI)
5. Tax-rate updates after state changes
6. User permission / role assignment requests
7. Backup verification / restore questions
8. Integration glitches with payment processor or e-comm platform
9. Reporting questions (Crystal Reports tweaks)
10. New-employee training requests

**Confidence:** (guess) — typical Counterpoint VAR support queue shape

**Notes:** A1 (Support-queue burndown) sizing assumes 60-80% of these are auto-resolvable once wiki coverage hits critical mass. Founder must confirm category mix and repeat-cause percentage.

---

## Q14 — Configuration knowledge concentration

**Answer:** Likely 2-3 senior engineers carrying the deep Counterpoint config + vertical-tuning expertise. ~1 of them is likely a 15-20-year-tenured "go-to" person whose departure would be a major risk. Documentation is sparse — internal wiki probably exists but is incomplete; most knowledge is in heads + email threads + ticket comments.

**Confidence:** (guess) — archetype default

**Notes:** A3 (Wiki builder) and A4 (Onboarding capture) target this directly. Retention package for the senior engineers is critical to the deal.

---

## Q15 — Onboarding shape today

**Answer:** New customer go-live: 8-16 weeks elapsed. Top three sources of delay:
1. Counterpoint license procurement + hardware ordering (can be 3-6 weeks)
2. Customer-side data migration (existing POS → Counterpoint export → import)
3. Customer-specific configuration (their vertical-specific tuning)

% bespoke vs. silently-repeating: likely 30% genuinely bespoke per customer, 70% silently-repeating across customers in the same vertical (especially within garden centers or firearms dealers). A4 (Onboarding capture) targets the 70%.

**Confidence:** (guess)

**Notes:** This is the leverage point for "Bart's team takes on more onboarding projects, less support projects" — once A4 has captured the silently-repeating 70% as templated playbooks, onboarding throughput goes up multiple-fold.

---

## Q16 — Break-fix vs. proactive ratio

**Answer:** Approximate split (archetype default):
- Break-fix incidents: ~35%
- Customer-specific customizations: ~25%
- New-customer onboarding: ~15%
- Internal improvement / docs / refactors: ~5%
- Sales support / discovery: ~10%
- DriftPOS integration spec + adapter dev: ~10% (if this is part of the team's hours; check whether DriftPOS team is separate)

The leverage point per the founder's framing: shift break-fix from 35% to <10% and onboarding from 15% to 50%+. That's the burn-down → repeatability flywheel.

**Confidence:** (guess)

**Notes:** Founder said this directly: "more onboarding projects and less support projects with the same people." This Q16 answer + Q13 + Q14 are the operational core of the managed-services value prop.

---

## Founder ↔ analyst disagreements

(None — this is a demo run by the analyst alone. Will populate during real founder review.)

---

## Archetype assignment

- [x] **Archetype A — SysRepublic 2015** (default for Counterpoint VARs)

**Where RapidPOS LLC may diverge from the archetype:**

- Vertical concentration is broader than typical (5 verticals vs. 1-2). This means more A4 playbook variants needed, but also more cohort-prioritization optionality.
- Active DriftPOS partnership pre-close is unusual — most archetype-A targets don't have a modern POS partner already lined up.
- "In my backyard" + personal founder relationship suggests the relationship advantage is stronger than typical archetype-A targets.

---

## Open questions for Phase 2 discovery

1. Specific top-5 customers and their cohort placement (drives valuation; drives DriftPOS first-wave selection)
2. Actual support-queue category mix and repeat-cause percentage (drives A1+A2 sizing)
3. RapidPOS LLC's own internal IT / engineering stack details (drives ISO 27001 scope-of-audit definition)
4. Whether Rapid-specific custom tables exist beyond Counterpoint stock (drives CRDM mapping difficulty)
5. Owner exit pacing — 24-month, 36-month, 60-month preferred? (drives glide-path articulation)
6. Bart's team headcount and current allocation (drives labor-trajectory math)

---

## Cost-model linkage

After this hypothesis grid is captured, populate `Brain/cost-models/rapidpos/00-target-profile.md` (already done in demo mode) with the same answers in the structured 20-field form. Re-run the cost-model with these inputs to produce `02-cost-model-output.xlsx` and `03-cost-model-output.docx`.
