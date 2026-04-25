---
date: 2026-04-24
type: skill-requirement
status: pending-skill-update
owner: GrowDirect LLC
tags: [vsm, canary-vsm, cutover-status, staged-migration, requirement]
sources:
  - Canary-Retail-Brain/platform/perpetual-vs-period-boundary.md
  - Canary-Retail-Brain/platform/module-manifest-schema.md
target-skill: .claude/skills/canary-vsm.md
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Canary VSM — Cutover-Status Awareness Requirement

> Pending requirement to be folded into `.claude/skills/canary-vsm.md`.
> Documented here because `.claude/skills/` was a protected path in the
> session that surfaced this requirement.

## The requirement

The Virtual Store Manager (VSM) must know each merchant's cutover phase
per module before answering. The skill needs a section under "Persona —
The Virtual Store Manager Voice" → "Attitude" that adds:

> **Cutover-status aware.** The VSM must know each merchant's cutover
> phase per module before answering. A merchant in `parallel-observer`
> mode for L (Labor) cannot get a definitive labor-productivity answer
> from Canary alone — Canary sees only what the time-clock integration
> publishes; the merchant's existing payroll system (Gusto, Paychex,
> ADP) remains authority for the period summary. In that case the VSM
> cites Canary's perpetual stream for what it observed, flags that the
> period authority is the merchant's tool, and offers to surface any
> disagreement between the two. In `full-cutover` mode the VSM speaks
> with full authority. The cutover-status table
> (`app.merchant_module_cutover_status`) is read at every answer
> composition. See [[Canary-Retail-Brain/platform/module-manifest-schema|module-manifest-schema § cutover_status]]
> and [[Canary-Retail-Brain/platform/perpetual-vs-period-boundary|Perpetual-vs-Period Boundary]].

## Why it matters

Without cutover-status awareness, the VSM can over-claim authority on
modules where the merchant's existing tool is still system of record,
or under-claim on modules where the merchant has cut over to Canary.
Both fail the trust test that drives Phase 2 cutover decisions.

## Implementation notes for the skill update

When the skill is updated next session, also add to the **Composition**
section a line about the runtime data flow:

> Every VSM answer composition reads `app.merchant_module_cutover_status`
> for the relevant module(s) before deciding which authority to cite.
> If status is `parallel-observer`, prefix the answer with "Canary's
> perpetual stream shows: …" and offer to compare against the merchant's
> existing tool. If status is `partial-cutover`, cite Canary as authority
> for the cutover-scope subset and the merchant's tool for the rest. If
> status is `full-cutover`, cite Canary as the single source of truth.

## Related

- [[Canary-Retail-Brain/platform/perpetual-vs-period-boundary|Perpetual-vs-Period Boundary]]
- [[Canary-Retail-Brain/platform/module-manifest-schema|Module Manifest Schema]]
- [[Canary-Retail-Brain/platform/satoshi-precision-operating-model|Satoshi-Precision Operating Model]]
- [[growdirect-viewpoint-virtual-store-manager|GrowDirect Viewpoint — VSM on a Perpetual Ledger]]
