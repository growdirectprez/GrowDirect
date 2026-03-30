---
type: decision
domain: business
status: active
created: 2026-03-01
updated: 2026-03-19
---
# Jeffe — Manifesto v1.2 Review Answers
**Date:** March 1, 2026
**Session:** ALX review with Jeffe, PhD Manifesto factual accuracy + voice
**Captured by:** ALX

---

## Q1: LaneHawk Incident (I.2) — CORRECTED
**Original:** PhD wrote it as a direct false accusation of an employee.
**Jeffe's correction:** It didn't cause a direct false accusation. What happened:
- The integration issue (field-length overflow in packed hex BCD) had NOT been discovered in any previous testing
- Every time it happened, the transaction was left in a **suspended state and never journaled** — unreported sales
- LP initially suspected an employee was entering training mode or somehow putting the POS into suspend
- It caused an **internal escalation from LP to IT that involved the executive committee**
- They discovered the real cause: unreported sales from a silent integration failure
- The system's silence (missing journal entries) pointed suspicion at the person standing at the register

**Action taken:** I.2 rewritten in the Manifesto to reflect this accurately. Key shift: from "accused the wrong person" to "the system's silence became an accusation by default — missing data in LP context points at people."

---

## Q2: Through-Line (I.3) — MOSTLY CORRECT
**Jeffe:** "Mostly correct. I will word-edit the MD directly for some details."
**Action:** Jeffe to edit I.3 directly. No ALX changes.

---

## Q3: Three Statements (I.4) — CONFIRMED VERBATIM
**Jeffe:** "Yes."
**Action:** Locked. No changes.

---

## Q4: Genesis Pool Pricing — NEW DIRECTION
**Original:** PhD pinned Genesis Pool value to "$430,000 at ~$4,300/BTC."
**Jeffe's direction:** "I'd rather see the theoretical growth of the Genesis Ordinal mint over time according to Metcalfe's Law."
**Action:** PhD task — model the Genesis Pool's network value growth using Metcalfe's Law (value proportional to n² where n = network participants/inscriptions). Replace static BTC price reference with a dynamic value growth model. This becomes a section in IV.1 or a new figure.

---

## Q5: Tier Mix (V.3) — CONFIRMED
**Jeffe:** "Seems OK for now."
**Action:** No changes. 40% Basic / 40% Treasury / 20% Full Node mix stands.

---

## Q6: $500K Seed Ask (VIII.1) — CONFIRMED
**Jeffe:** "Yes OK."
**Action:** No changes. $500K with 40/30/20/10 allocation stands.

---

## Q7: RaaS Placement — DIRECTIVE
**Jeffe:** "Fit in where you think it's best. It's a side benefit of the TSP and the schema-agnostic approach."
**Action:** PhD to position RaaS as an emergent capability of the existing architecture (TSP + schema-agnostic CRDM), not a separate product layer. Best fit: expand IV.3 (Validation Gate) to include RaaS framing, or add as IV.3.1. The key insight: because the CRDM normalizes any POS data into canonical schema, any POS system can hit the validation API. RaaS is the business model name for what the architecture already does.

---

## Q8: Why 17 Merchants — DIG DEEPER
**Jeffe:** "Why 17? It's prime? Why is it showing up? Dig deeper and embrace."
**Action:** PhD task — investigate WHY the number 17 recurs as the self-sustainability convergence point across multiple independent economic models. PhD noted in the Research Paper Roadmap that "the number 17 recurs across multiple independent economic models — it is not an assumption but a convergence point." Jeffe wants PhD to:
1. Identify every model where 17 appears independently
2. Determine if there's a mathematical reason (prime number properties, network topology, economic equilibrium)
3. If the convergence is real and explainable, make it a headline metric with the mathematical backing
4. If it's coincidence, provide the range instead
This could become a powerful investor talking point: "17 is not a target. It's a convergence."

---

## Q9: Appendix C Commit Hash — UPDATED
**Action taken:** Updated from `72d0082` (Sprint 5) to `996562f` (Sprint 6 `sprint-6-tsp` HEAD).

---

## New PhD Tasks Generated from Review

| # | Task | Deliverable | Priority |
|---|------|-------------|----------|
| 1 | Metcalfe's Law model for Genesis Pool value growth | New figure + section in IV.1 or standalone brief | HIGH — investor-facing |
| 2 | RaaS framing as emergent TSP + schema-agnostic capability | Manifesto section (IV.3 expansion or new IV.3.1) | HIGH — Jeffe directive |
| 3 | "Why 17" deep dive — convergence analysis | Brief with mathematical backing | HIGH — headline metric |
| 4 | Jeffe to word-edit I.3 directly | Jeffe owns | WAITING on Jeffe |
