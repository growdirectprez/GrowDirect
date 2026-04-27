---
title: CRB–RapidPOS Alignment Notes
type: wiki
project: Canary
created: 2026-04-27
tags: [crb, rapidpos, alignment, hawk-phase-1]
last-compiled: 2026-04-27
needs-review: false
---

# CRB–RapidPOS Alignment Notes

Read pass of the Canary Retail Brain vault (`~/GrowDirect-CRB/`) against the focus question: where does CRB's published module description diverge from what the code actually does today? Which modules are more optimistic or more limited than the live implementation?

## Finding 1: Fox Is Everywhere — Hawk Is Nowhere

Fox appears **72+ times** across CRB as the named case management surface. Every module that produces exceptions routes them to Fox: Q (primary), D (transfer-loss), R (customer investigation), S (bundle abuse), J (PO discrepancy), F (AR collections), C (credit-limit alerts), P (markdown decisions), N (device telemetry), W (cross-domain generalization).

Hawk does not appear in CRB at all. Zero mentions.

**This is the most visible gap for SDD Dispatch 5.** The Hawk migration (`hawk_a00001`) introduces a new entity/investigation model that supersedes Fox's original case management surface. CRB's published module descriptions all reference Fox by name — the fox_cases, fox_subjects, fox_case_actions, fox_case_timeline, fox_evidence tables — and the INSERT-only, hash-chained evidence chain discipline.

**What the SDDs need to clarify:**
- Whether Hawk replaces Fox or extends it (rename vs. restructure)
- Whether the evidence chain discipline (INSERT-only, trigger-enforced, hash-chained) carries forward unchanged
- Whether the fox_* table names change or the schema layer is renamed
- What happens to the W module's dependency on "inherited Fox model" — does W inherit Hawk instead?

## Finding 2: Platform Overview Says "Square Is the First Connector"

`platform/overview.md` line 62: "Square is the first connector, not the core dependency." This is the single most explicit POS-naming in CRB. The statement is architecturally correct (POS-agnostic by design) but factually stale — RapidPOS/Counterpoint is now the primary engagement path per the `project_canary_rapidpos_primary_shift` memory.

**SDD action:** Update the CRB overview to say "Square was the first connector" (past tense) or generalize to "POS adapters are translation layers" without naming a specific first. The Counterpoint adapter is the one being actively built.

## Finding 3: T Module Functional Decomposition Names the Square–Counterpoint Pivot Explicitly

`modules/T-transaction-pipeline.md` governing thesis (line 28): "two architectural pivots that distinguish it from the Square baseline: (1) ingress is poll-only, not webhook-driven, and (2) the inbound payload is Document-shaped omnibus." This is the clearest documentation of the multi-POS architecture in any published artifact.

The T card also explicitly names T.3.9 ("Square-shaped legacy parsing — 16 existing parser modules") and the "Park Square" decision. This is correctly positioned as one provider within a multi-provider dispatch registry.

**No correction needed.** T's functional decomposition is the reference for how multi-POS coexistence works.

## Finding 4: Module D Gating Is Clearly Documented

`modules/D-distribution.md` has the cleanest L2 split of any module card:
- D.1 + D.2: ● Counterpoint-substrate (direct, high-confidence)
- D.3: ◐ Counterpoint-substrate (indirect, via Document omnibus DOC_TYP=XFER)
- D.4 + D.5: ★ Canary-native (transfer-loss reconciliation + multi-store distribution recommendations)

D depends on T.4.7 (XFER routing contract) — if T's type-routing fails, D.3 fails silently. This cross-module dependency is named and must become a contract test.

The Bull module (D.4 transfer-loss + D.5 distribution recommendations) is the Canary-native gap. CRB documents it accurately as "no Counterpoint analog." The SDDs need to formalize Bull's scope against this CRB description.

**Key dependency chain for Hawk Phase 1:**
T (adapter ingress) → T.3.2 (DOC_TYP routing) → T.4.6/T.4.7 (XFER/PO publication) → D.3 (transfer detection) → D.4 (Canary-native loss reconciliation) → Q (Q-IS-03 accumulation)

## Finding 5: Q Rule Catalog Is More Advanced Than Live Code

CRB publishes a 25-rule catalog across 12 families (including compliance and commercial/B2B families added beyond the original 23/10). The live code has 37 frozen Chirp rules against Square. The Counterpoint-specific rules (Q-IS-02 cash-paid receivers, Q-IS-04 dead-count tracking, Q-MM-01/02 mix-and-match, Q-RESTRICTED-ITEM-SALE compliance, Q-C-01 through Q-C-05 commercial/B2B) are documented in CRB but not yet implemented.

**SDD drift assessment:**
- CRB is aspirational-but-realistic for Counterpoint rules — they're well-specified, have assumption markers, and have explicit resolution paths
- Live code has Square-shaped rules that will coexist (T.3.9)
- The gap is in implementation, not in specification quality

## Finding 6: EJ Spine + Sales Audit Naming Is CRB-Authoritative

`modules/EJ-spine-and-sales-audit.md` is the definitive naming article. The TSP Mermaid diagram (fig-p00) is Square-specific in its external entry node ("Square Webhooks / HMAC-SHA256 Signed") but the pipeline architecture is provider-agnostic from the Valkey stream onward.

**SDD action:** When the TSP SDD is updated for multi-adapter, the fig-p00 diagram needs a second entry path for Counterpoint polling alongside the Square webhook path. Both feed the same `canary:events` stream.

## Finding 7: Case Studies Are Square-Denominated

All three case studies use Square as the assumed POS:
- `canary-retail-diagnostic-archetype.md` — "Square POS transactions, 142,847 line items"
- `canary-finance-architecture-options.md` — "Square POS" as the transaction source, Option C OAuth bridge
- `canary-iot-vendor-strategy.md` — references Square integration in current state

These are proof-case artifacts, not live documentation. They correctly demonstrate the methodology. A Counterpoint-denominated proof case would complement them but isn't blocking.

## Finding 8: Module Manifest Schema and Perpetual-vs-Period Boundary Are POS-Agnostic

`platform/module-manifest-schema.md` and `platform/perpetual-vs-period-boundary.md` are cleanly generic. The perpetual-vs-period article references "Chirp+Fox" but the staged migration pattern (parallel-observer → modular-cutover → full-cutover) is POS-independent.

The per-module perpetual/period split table (line 181 onward) is the reference for what Canary owns vs what the merchant's existing tools own. This table doesn't mention any POS — it's about the boundary between perpetual and period accounting, which is a property of the module, not the POS.

## Summary — SDD Actions from CRB Read

| Finding | CRB State | SDD Priority | Owner |
|---|---|---|---|
| Fox → Hawk rename/restructure | Fox everywhere, Hawk absent | **Hawk Phase 1 — blocking** | SDD Dispatch 5 |
| Evidence chain discipline (INSERT-only, hash-chained) | Thoroughly documented for Fox | Confirm carries to Hawk | SDD Dispatch 5 |
| "Square is the first connector" | Factually stale | Update overview — low priority | Phase 2+ CRB refresh |
| T multi-adapter documentation | Excellent (T card) | Reference in TSP SDD | SDD Dispatch 3 |
| D gating + Bull scope | Accurately documented | Formalize in Bull SDD | SDD Dispatch 4 |
| Q rule catalog vs live code | CRB ahead of implementation | Implementation catches up | Ongoing |
| EJ/TSP diagram Square-specific entry | fig-p00 needs second entry path | Update when TSP SDD lands multi-adapter | SDD Dispatch 3 |
| Case studies Square-denominated | Correct for proof-case era | Add Counterpoint proof case later | Phase 2+ |

**The Fox → Hawk gap is the single most important CRB alignment issue.** Every module references Fox by name. The SDD pass must define Hawk's relationship to Fox explicitly so that CRB can be updated in a single sweep afterward.

## Related

- [[catz-rapidpos-alignment-notes]] — companion read pass (CATz vault)
- [[canary-architecture]] — platform architecture
- [[canary-fox-case-management]] — current Fox documentation in Brain
- [[canary-detection]] — Module Q detection rules
- [[canary-tsp-pipeline]] — TSP ingestion pipeline
- `docs/superpowers/plans/2026-04-27-hawk-phase-1.md` — Hawk Phase 1 plan
