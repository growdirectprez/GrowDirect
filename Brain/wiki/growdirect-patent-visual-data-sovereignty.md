---
date: 2026-04-22
type: wiki
tags: [growdirect, patent-visuals, patent, data-sovereignty, crdm]
sources:
  - docs/_archive/ip-vault/patent-visuals/Patent_DataSovereignty_Stack_v1.0.html
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Patent Schematic — Data Sovereignty Stack v1.0 (FIG. 4)

Rendered SVG schematic filed as **FIG. 4** in Patent Application 63/991,596. Version 1.0.

## What the Figure Depicts

A three-layer stack illustrating where merchant data lives and who can touch it:

1. **Application Layer** — the merchant-facing dashboards, Chirps, and wizards. Tenant-isolated, RLS-enforced.
2. **Structured Store** — the CRDM normalized schema. Queryable, indexed, mutable only via append.
3. **Evidence Store** — the hash-chained, INSERT-only forensic layer. The source of truth.

Underneath all three sits the **Bitcoin Anchor** — the Merkle-batched Ordinal inscriptions that make the Evidence Store independently verifiable without trust in the operator.

## Architectural Principle

The figure carries the caption "Architectural Principle" — data sovereignty flows bottom-up: the merchant's transaction history is anchored to Bitcoin and cannot be altered by Canary, by Square, or by any regulator. The structured queryable data is derivative; the evidence is primary; Bitcoin is the terminal guarantor.

## Why It Matters

This figure supports patent claims around **staged immutability** and **bilateral verification**. It also serves as the visual for ISO 27001 and SOC 2 evidence: auditors can see, at a glance, that the Evidence Store is INSERT-only and the Bitcoin anchor makes tampering detectable.

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-the-crdm|The Data Model]] — CRDM narrative
- [[Brain/wiki/growdirect-compliance|Compliance by Construction]] — architecture-as-compliance
- [[Brain/wiki/growdirect-the-patent|The Patent]] — IP strategy

## Sources

- `docs/_archive/ip-vault/patent-visuals/Patent_DataSovereignty_Stack_v1.0.html` — the rendered SVG schematic
