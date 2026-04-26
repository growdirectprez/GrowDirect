---
type: index
status: active
date: 2026-04-24
owner: GrowDirect LLC
tags: [canary, architecture, decisions, index]
related:
  - Canary/docs/sdds/v2/architecture.md
  - case-studies/canary-finance-architecture-options.md
  - docs/sdds/consulting/SDD-morrisons-it-architecture-options-v2.md
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Canary Architecture Decisions Index

## What This Is

A running index of **open** and **closed** architecture decisions affecting the Canary platform spine (v2.0 → v3.0 → v4.0). Each decision is tracked as an ADR (Architecture Decision Record) or formal SDD section, with link to the resolution and the rationale.

The Morrisons pattern (Sell/Plan/Move/Buy frame + three-option heat-map evaluation) is the standard method for evaluating architecture decisions here. When a decision involves choosing between competing approaches (build vs. buy, native vs. integrated, single vendor vs. multi-vendor), the Morrisons frame applies: frame once, evaluate symmetric options, recommend.

---

## Open Decisions

| Decision | Description | Status | Owner | Target Resolution |
|----------|-------------|--------|-------|-------------------|
| **v2.F (Finance) Implementation Route** | Should Canary own a native GL, integrate to merchant's GL via API, or build a hybrid perpetual layer + GL bridge? | **DECIDED: Option C** | Geoffrey C. Lyle | GRO-526 (Design complete; implementation Q3 2026) |
| **v2.D (Distribution) Build vs. Buy** | Should Canary build a native distribution-center module or integrate to a 3PL / WMS package? | Open; needs ADR | Product team | Q2 2026 (pre-v2.D planning) |
| **Owl Runtime: VSM Persona Rename or Layering?** | The current Owl personality system uses VSM (Virtual Subject Matter Expert) persona tags. Should VSM be renamed to "Persona" for clarity, or layered as a capability on top of persona? | Partially answered (chose layering in Canary VSM skill). Candidate for formal ADR. | Geoffrey C. Lyle | Q2 2026 if needed |

---

## Closed Decisions

### GRO-526: Canary v2.F Finance — Architecture Decision Record

**Decision:** Canary v2.F (Finance) adopts **Option C — Integrated Hybrid.**

**Why:** Perpetual-layer owned by Canary (inventory cost tracking, 3-way match, COGS movement), period-layer and GL authority owned by merchant's existing accounting package (QBO, Xero, Wave, FreshBooks) via OAuth bridge.

**ADR Link:** [[case-studies/canary-finance-architecture-options|Case Study: Canary v2.F Finance — Architecture Options Evaluation]]

**Key rationale:**
- Fastest to market: 3 months (v2.0 MVP), vs. 4 months (Option B) or 6 months (Option A).
- Lowest engineer-years: 15.7 (Option C) vs. 18.3 (Option B) or 27.9 (Option A).
- Highest merchant adoption: merchants trust their existing GL; Canary is a feeder, not a replacement.
- No GL audit liability: merchant accountant certifies merchant GL; Canary provides prep layer.
- Aspirational-ready: perpetual-vs-period boundary extensible to RIM (v3) and ecosystem integrations.

**Phasing:**
- **v2.0** (Q3 2026): Cost Method only, invoice matching, GL posting via OAuth
- **v2.1** (Q4 2026): PO tracking, exception workflows, reconciliation reporting
- **v3** (Q2 2027): RIM (Real/Integrated Merchandise), advanced cost methods, variance analysis

**Acceptance gates:**
- Post-MVP: <3% GL posting failures (OAuth token, API uptime)
- Pre-v2.1: >30% merchant adoption (goal: 40% within 30 days of onboarding)
- Pre-v3: >10% merchant RIM demand signal (if <10%, defer RIM; prioritize ecosystem integrations)

**Status:** Design complete (SDD signed off). Implementation begins 2026-05-01 (eng-weeks 1–12 of Q3 roadmap).

---

### GRO-560: Canary NCR Product-Line Decision — Architecture Decision Record

**Decision:** Canary's first NCR product-line integration is **Option B — Counterpoint first.**

**Why:** Closest merchant-profile fit to Canary's existing Square SMB sweet-spot. Specialty retail vertical where Canary's loss-prevention and store-ops substrate already produces value. Real first customer (Boutique Home & Garden chain) is in front of us. Friendly VAR channel (Bart Monahan / Rapid POS) is a Counterpoint reseller. Public API documentation already extracted into validated OpenAPI spec. ~80% Q-rule portability from Square. Customer-routed access strategy sidesteps NCR-Voyix-as-competitor friction.

**ADR Link:** [[../../Canary-Retail-Brain/case-studies/canary-ncr-product-line-decision|Case Study: Canary NCR Product-Line Decision — Architecture Options]]

**Sequence:** Counterpoint Q3 2026 → Voyix re-eval Q2 2027 → Aloha as separate restaurant-vertical motion only when independently funded.

**Why not Aloha first:** ~58 adapter eng-weeks (vs Counterpoint's ~26). Vertical mismatch — restaurants need a net-new Q rule family + CRDM extensions for modifiers/checks/tip pools. Different merchant motion.

**Why not Voyix first:** Smallest installed base today. NCR Voyix is the direct SMB-analytics competitor — partnership friction is highest of the three. Re-evaluate Q2 2027 when API maturity and installed base catch up.

**Phasing:**
- **Q3 2026:** Phase 0 substrate (in flight under GRO-558) + Phase 1 priority modules (T R F L N)
- **Q4 2026:** Phase 2 catalog modules (P S — H&G-critical)
- **Q1 2027:** Phase 3 operations modules (D J; W out of scope per SDD §6.13)
- **Q2 2027:** Phase 4 tertiary (A C Q) + Voyix product-line re-eval gate

**Acceptance gates:**
- Post-Phase-0: substrate scaffolds shipped, Square pipeline untouched, ~25 priority endpoints adapter-covered
- Post-MVP: first Boutique H&G chain deployment completes Phases 0–4 successfully
- Pre-Voyix-re-eval (Q2 2027): Counterpoint adapter has ≥3 production deployments with ≥80% Q-rule portability proven

**Status:** Decision recorded 2026-04-25. Implementation in flight (mini's `feat/pos-substrate` branch shipped Cycle 7 / 7.2 + 7.3 — POS adapter substrate scaffold + contract test suite).

---

## How to Use the Morrisons Frame

When Canary faces a decision between competing architecture approaches:

1. **Frame once:** Define the business targets (Optimisation programme) and the shared requirement taxonomy (e.g., Sell/Plan/Move/Buy or an equivalent).
2. **Inventory the current state:** Heat-map the existing Canary architecture against the targets using 4-color legend (Green / Yellow / Amber / Red).
3. **Evaluate options symmetrically:** For each option (A, B, C, ...), render the seven-slide skeleton: title, two heat-maps (org view + process view), effort estimate, aspirational heat-maps, advantages/disadvantages, target architecture.
4. **Compare side-by-side:** Architecture comparison, implementation comparison (timescale, risk, lock-in, phasing), recommendation.
5. **Recommend with reasoning:** Chosen option explicitly mapped to the Section 2 business targets.

This enforces **symmetric comparison**, **evidence transparency**, and **defensible judgment**.

Reference: [[docs/sdds/consulting/SDD-morrisons-it-architecture-options-v2|SDD — Morrisons IT Architecture Options: Method as Executable Frame]]

---

## Related

- **Architecture SDD:** [[Canary/docs/sdds/v2/architecture|Canary Architecture (v2 SDD)]]
- **Methodology wiki:** [[Brain/wiki/methodology-ibm-it-architecture-options|Methodology · IBM IT Architecture Options (Morrisons pattern)]]
- **Consulting skills SDD:** [[docs/sdds/consulting/SDD-consulting-skills|SDD · Consulting Skills (Retail Diagnostic + IT Architecture Options)]]
- **Method MOC:** [[Brain/projects/Method|Method MOC]]
- **Canary project MOC:** [[Brain/projects/Canary|Canary MOC]]

