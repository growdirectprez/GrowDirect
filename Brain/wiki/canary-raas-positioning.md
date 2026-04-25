---
date: 2026-04-24
type: positioning-guardrail
status: active
owner: GrowDirect LLC
classification: confidential
tags: [raas, eljeffe, attestation, positioning, guardrail, unaudited, do-not-claim]
sources:
  - Canary/docs/sdds/v2/raas.md
  - canary-architecture (wiki)
  - canary-module-t-transactions (wiki)
last-compiled: 2026-04-24
needs-review: 2026-07-24
---

# Canary RaaS — Positioning Guardrail

> **Hard constraint.** RaaS is currently **unaudited** infrastructure.
> It cannot be cited in any merchant-facing claim, sales pitch, ADR
> rationale, substrate primitive, regulatory positioning, or audit-grade
> trust narrative until it has cleared a formal third-party security
> audit (SOC 2 Type 2 minimum; jurisdiction-specific certifications
> for any regulated claim).

## What RaaS is today

- A planned attestation layer that anchors batched perpetual-ledger
  Merkle roots to Bitcoin L1 ordinals (with Avalanche L2 NameRegistry
  and Postgres L3 hot cache per the elJeffe protocol stack)
- An SDD at `Canary/docs/sdds/v2/raas.md` describing the design
- T pipeline implementation produces the inputs RaaS needs (Sub 1
  raw-byte hash + Sub 3 Merkle batch); the production anchor is
  currently a mock per the T module crosswalk
- Internally useful as a research / chain-of-custody scaffold for
  Canary's own forensic LP work (Fox cases benefit from the
  hash-chain integrity even without external attestation)

## What RaaS is NOT today

- **NOT** a substrate primitive in the Canary Retail Spine. The five
  CATz substrate articles are: stock-ledger, retail-accounting-method,
  satoshi-cost-accounting, satoshi-precision-operating-model,
  perpetual-vs-period-boundary. RaaS is not the sixth.
- **NOT** what makes the perpetual-vs-period boundary's Phase 3
  (stock-ledger swap) trust-able to merchants' auditors / lenders /
  insurers. Phase 3 trust is established by operational reconciliation
  history + standard accounting review of Canary's reports — the same
  way merchants today trust QuickBooks or Xero. RaaS is not yet part of
  that trust path.
- **NOT** a regulatory-grade audit upgrade. Until audited, citing RaaS
  as the basis for any regulated claim risks misrepresentation.
- **NOT** a sales claim. Sales / marketing copy must not reference RaaS
  as a feature, a moat, or a differentiator until audit lands.
- **NOT** a substrate that downstream code or SDDs should declare a
  hard dependency on. T's pipeline can produce RaaS-ready output, but
  no other module should be designed assuming RaaS attestation is
  available.

## What changes when RaaS is audited

If and when RaaS clears a formal audit (SOC 2 Type 2 minimum), this
guardrail revisits and likely promotes RaaS to a sixth substrate
primitive at `Canary-Retail-Brain/platform/raas-attestation-layer.md`.
At that point — and only at that point — the perpetual-vs-period
boundary's Phase 3 trust narrative can incorporate RaaS as a
regulator-grade attestation upgrade.

The audit gate is binary. Pre-audit: research / internal-use only.
Post-audit: substrate primitive, sales claim, trust amplifier.

## Why this guardrail exists

This article was written because in the spine substrate sweep of
2026-04-24, RaaS was nearly added to CATz as a sixth substrate
primitive with cross-references positioning it as the audit-grade
trust amplifier for Phase 3 cutover. The proposal was caught and
walked back at user direction. The risk repeats every time someone
re-reads the substrate articles + the elJeffe SDD + the satoshi-cost
work and sees the obvious-looking-but-wrong placement.

This guardrail exists so future sessions hit the constraint before
shipping language that overclaims.

## Practical rules

When working on the spine, the substrate, the viewpoint, sales material,
or any merchant-facing copy:

1. Do not introduce RaaS as a substrate primitive
2. Do not cite RaaS as the basis for any trust / audit / regulatory claim
3. Do not propose that downstream modules depend on RaaS attestation
4. Do not add `raas_attestation` fields to module manifests
5. Do not link the perpetual-vs-period boundary's Phase 3 trust path
   to RaaS
6. Do not extend the satoshi-precision-operating-model's audit-trail
   promise to mean "Bitcoin-anchored" — the audit-trail there means
   data-trace audit (drill from P&L line to originating event), not
   cryptographic attestation
7. **Do** reference RaaS internally for forensic / chain-of-custody work
   on Fox cases where the integrity guarantee benefits Canary's own
   investigation discipline (not the merchant's regulatory posture)
8. **Do** keep the T pipeline's raw-byte hash + Merkle batch
   producing RaaS-ready output so that when audit lands, the substrate
   work is already done

## Related

- `Canary/docs/sdds/v2/raas.md` — the design SDD (internal)
- [[canary-architecture|Canary Architecture]] — wider context
- [[canary-module-t-transactions|T Transaction Pipeline]] — produces RaaS-ready inputs
- [[canary-fox-case-management|Fox Case Management]] — internal beneficiary of the chain-of-custody work
- [[Canary-Retail-Brain/platform/perpetual-vs-period-boundary|Perpetual-vs-Period Boundary]] — Phase 3 trust path explicitly does NOT depend on RaaS
- [[Canary-Retail-Brain/platform/satoshi-precision-operating-model|Satoshi-Precision Operating Model]] — audit-trail claim explicitly means data-trace, not cryptographic attestation
- elJeffe protocol track (Linear; archived as a project but the protocol work persists) — RaaS lives in this track until audited

## Sources

- Direct user correction, 2026-04-24 — "the RaaS is unaudited"
- Canary RaaS SDD (design state, mock anchor)
- T module crosswalk noting RaaS anchor as currently mock
