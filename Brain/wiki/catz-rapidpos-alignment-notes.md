---
title: CATz–RapidPOS Alignment Notes
type: wiki
project: Canary
created: 2026-04-27
tags: [catz, rapidpos, alignment, hawk-phase-1]
last-compiled: 2026-04-27
needs-review: false
---

# CATz–RapidPOS Alignment Notes

Read pass of the CATz vault (`~/GrowDirect-CATz/`) against the focus question: where does the methodology assume Square-specific behavior, and where do the SDDs need to close gaps for RapidPOS/Counterpoint?

## Finding 1: CATz Method Layer Is Already POS-Agnostic

Zero mentions of "Square" anywhere in the CATz vault. The five-layer frame (Frame / People / Agents / Model / Blueprint), the CDF phases (Scaffold / Seed / Show), the five workstreams (Architecture, Data & Integration, Analytics & Detection, Knowledge & Enablement, Program Management), and all three role playbooks (ALX, Data Detective, Digital Plumber) speak in terms of "POS," "source system," "connector," and "substrate" — never a specific vendor.

This is correct. The method is the method regardless of which POS sits underneath.

**No SDD changes required at the method layer.**

## Finding 2: Counterpoint Is the Only Named POS Substrate

NCR Counterpoint appears in three places:

1. **`method/data-economics.md`** — transaction volume assumptions and data type tables use Counterpoint table names (`PS_DOC`, `IM_ITEM`, `AR_CUST`). Section titled "Why This Matters to a VAR (Rapid POS, MSP Model)" explicitly positions the VAR argument.
2. **`method/cloud-architecture-options.md`** — two references to "Rapid POS" as the VAR/MSP deployment example in the tenant isolation model.
3. **`proof-cases/specialty-smb-counterpoint-solution-map.md`** — the worked Solution Map proof case. Counterpoint is the incumbent POS column. Coverage assessments reference the Counterpoint REST API surface.

All three are correctly scoped: data-economics uses Counterpoint as a concrete example (with "or a comparable POS system" qualifier), cloud-architecture uses Rapid POS as a VAR archetype, and the proof case is explicitly a Counterpoint-specific proof case.

**No corrections needed. Counterpoint references are examples, not assumptions.**

## Finding 3: The Module Functional Decomposition Artifact Is Substrate-Aware by Design

The `module-functional-decomposition.md` artifact already has:

- Coverage-aware L2 splits (● Full direct / ◐ Partial / ★ Canary native / ◯ External)
- Substrate contract registry (producer-side and consumer-side)
- Assumption markers with platform-knowable vs engagement-knowable distinction
- Customer-specific overrides section (empty until engagement starts)
- Actor discipline tied to module posture (observer / bidirectional / substrate)

The contract test suite concept — "every entry in the substrate contract registry becomes a test that runs against every registered POS adapter" — is the multi-POS conformance bar. Adding a Square adapter or any other POS adapter means passing all existing contract tests.

**This is the architectural hook that makes multi-POS work. SDDs should reference this conformance bar explicitly.**

## Finding 4: The Gap Is Not in CATz — It Is in the Canary SDDs

CATz is clean. The methodology doesn't assume Square. The gaps that Hawk Phase 1 needs to close are in the Canary implementation layer:

1. **Adapter abstraction in the TSP pipeline** — the SDDs need to formalize the multi-adapter pattern. CATz's "connector design per source" (WS2) and the functional decomposition's contract registry both assume this exists at the platform level. The Hawk migration (`hawk_a00001`) introduces `vendor_type` on entities, which is the schema-level expression of this.
2. **Detection rules must be substrate-neutral** — Module Q's functional decomposition positions rules as running "on top of the Counterpoint substrate," but the rule catalog itself should evaluate against canonical model fields, not Counterpoint-specific field names. The CRDM is the abstraction layer.
3. **Data economics need a second worked example** — the current data-economics article uses Counterpoint table names and payload sizes. A Square-equivalent column (or a generic "cloud POS with webhook push" column) would make the economics argument POS-agnostic in presentation, not just in principle.
4. **Proof case for Square (or generic cloud POS)** — the only proof-case Solution Map is Counterpoint-specific. A second proof case showing a cloud-native POS (Square, Clover, Lightspeed) with webhook-push ingestion vs Counterpoint's poll-based REST would demonstrate the multi-POS thesis concretely.

## Finding 5: ALXjr Profile References CATz Correctly

The ALXjr operating profile (`agents/ALXjr.md`) correctly positions itself as a target-aware namespace (not a separate agent), references CATz as the governing method, and lists the CRDM as the substrate. The knowledge section includes "The retail spine — 13 modules" and "CATz methodology." No Square-specific assumptions.

**No changes needed to ALXjr for Hawk alignment.**

## Summary — What the SDDs Need to Do

| Area | CATz State | SDD Action Required |
|---|---|---|
| Method layer | POS-agnostic | None |
| CDF phases/workstreams | POS-agnostic | None |
| Role playbooks | POS-agnostic | None |
| Module functional decomposition | Substrate-aware by design | Reference conformance bar in SDD adapter specs |
| Data economics | Counterpoint-specific example | Add cloud-POS column (Phase 2+ polish, not blocking) |
| Proof-case Solution Map | Counterpoint only | Add cloud-POS proof case (Phase 2+, not blocking) |
| TSP adapter pattern | Implied by CATz connector design | Formalize multi-adapter in TSP SDD (Hawk Phase 1 scope) |
| Detection rules | Positioned as substrate-neutral | Confirm rules reference CRDM fields, not POS-native fields |
| ALXjr identity | Clean | None |

The methodology is structurally ready for multi-POS. The work is in the platform SDDs, not the method docs.

## Related

- [[canary-architecture]] — platform architecture (adapter layer lives here)
- [[canary-detection]] — Module Q detection rules
- [[canary-tsp-pipeline]] — TSP ingestion pipeline (adapter pattern)
- [[ncr-counterpoint-api-reference]] — Counterpoint REST surface
- `docs/superpowers/plans/2026-04-27-hawk-phase-1.md` — Hawk Phase 1 plan
