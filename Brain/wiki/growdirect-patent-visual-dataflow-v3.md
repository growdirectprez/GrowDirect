---
date: 2026-04-22
type: wiki
tags: [growdirect, patent-visuals, patent, data-flow, single-transaction]
sources:
  - docs/_archive/ip-vault/patent-visuals/Patent_DataFlow_Visual_v3.0.html
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Patent Schematic — Single-Transaction Data Flow v3.0 (FIG. 2)

Rendered SVG schematic filed as **FIG. 2** in Patent Application 63/991,596. Version 3.0. The companion data-flow figure to the Six-Node Architecture diagram in FIG. 1.

## What the Figure Depicts

A single transaction's end-to-end journey through the pipeline, annotated with time markers and provenance tags:

- **T+0ms** — webhook arrives at API Gateway, HMAC-verified, hashed, published
- **T+1ms** — queue fan-out to 3 subscribers
- **T+5ms** — Sub 1 writes to Evidence Store (write-once, hash-chained)
- **T+15ms** — Sub 2 parses into Structured Store (CRDM normalized)
- **T+60s** — Sub 3 adds to Merkle batch
- **T+~10min** — Ordinal inscription on Bitcoin confirmed

## Why It Matters

This is the forensic provenance trace that makes a single transaction a defensible evidence artifact. Every state transition writes a hash link, so a downstream query against the Structured Store can always be verified against the Evidence Store, which itself anchors to Bitcoin via the Ordinal inscription. The figure is the visual proof that the architecture delivers the three Pitch properties:

- **Real-time** (T+0ms capture, no polling gaps)
- **Immutable** (write-once, hash-chained)
- **Permanent** (Bitcoin Ordinal anchor)

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-the-pipe|The Protocol Pipe]] — narrative counterpart
- [[Brain/wiki/growdirect-patent-visual-architecture-v3|Architecture Visual v3.0]] — FIG. 1 companion
- [[Brain/wiki/growdirect-the-patent|The Patent]] — IP strategy

## Sources

- `docs/_archive/ip-vault/patent-visuals/Patent_DataFlow_Visual_v3.0.html` — the rendered SVG schematic
