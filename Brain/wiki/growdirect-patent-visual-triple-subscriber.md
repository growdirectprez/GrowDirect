---
date: 2026-04-22
type: wiki
tags: [growdirect, patent-visuals, patent, triple-subscriber, tsp, component]
sources:
  - docs/_archive/ip-vault/patent-visuals/Patent_TripleSubscriber_Component_v2.0.html
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Patent Schematic — Triple Subscriber Component v2.0 (FIG. 3)

Rendered SVG schematic filed as **FIG. 3** in Patent Application 63/991,596. Version 2.0. Zooms in on the queue fan-out from FIG. 1 and shows the internal structure of each subscriber.

## What the Figure Depicts

Three parallel subscribers consuming from a single queue, each with distinct storage and processing semantics:

- **Sub 1 — Hash & Seal** (Evidence Store)
  - INSERT-only, hash-chained, SHA-256 linked-list integrity
  - Tamper-evident: any mutation breaks the chain
  - The forensic spine — survives even if Sub 2/3 are compromised

- **Sub 2 — Parse & Route** (Structured Store)
  - CRDM-normalized rows — merchants, transactions, refunds, timecards, cash events
  - Queryable via SQL, indexed for Chirp detection rules
  - The operational surface — what the dashboard reads

- **Sub 3 — Merkle & Ordinal** (Notary)
  - Batches event hashes into Merkle trees
  - Inscribes Merkle root on Bitcoin as an Ordinal
  - The permanence layer — makes the Evidence Store independently verifiable

## Why It Matters

This figure supports the patent's core architectural claim: **three parallel subscribers on a single queue, producing staged immutability**. The TSP PRDs (TSP-00 through TSP-09, delivered in work order B-059) are the engineering realization of this figure.

Also supports claims around **bilateral verification** — any event in Sub 2 can be verified against Sub 1, which can be verified against Sub 3's Ordinal inscription on Bitcoin.

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-triple-subscriber|Triple Subscriber Pipeline]] — narrative counterpart
- [[Brain/wiki/growdirect-patent-visual-architecture-v3|Architecture Visual v3.0]] — FIG. 1 parent
- [[Brain/wiki/growdirect-the-patent|The Patent]] — IP strategy

## Sources

- `docs/_archive/ip-vault/patent-visuals/Patent_TripleSubscriber_Component_v2.0.html` — the rendered SVG schematic
