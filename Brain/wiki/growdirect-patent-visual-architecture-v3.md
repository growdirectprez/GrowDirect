---
date: 2026-04-22
type: wiki
tags: [growdirect, patent-visuals, patent, architecture, six-node]
sources:
  - docs/_archive/ip-vault/patent-visuals/Patent_Architecture_Visual_v3.0.html
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Patent Schematic — Six-Node Architecture v3.0 (FIG. 1)

Rendered SVG schematic filed as **FIG. 1** in Patent Application 63/991,596 (filed February 26, 2026). Version 3.0 supersedes v2.0 as the canonical architecture visual.

## What the Figure Depicts

A top-down pipeline showing the six-node Universal Event Notarization architecture:

1. **Source Networks** — external event producers (Square, Shopify, Epic, FedEx, Legal, Insurance, Gov). POST webhooks into the system.
2. **API Gateway** — HMAC-verifies, SHA-256 hashes, and publishes to the queue. Returns 200 OK in under 5ms.
3. **Queue** — fan-out of 3 to the three subscribers.
4. **Sub 1 — Hash & Seal** — the Evidence Store. Write-once, INSERT-only, hash-chained.
5. **Sub 2 — Parse & Route** — the Structured Store. Queryable normalized CRDM rows.
6. **Sub 3 — Merkle & Ordinal** — the Notary. Merkle-batches and inscribes on Bitcoin via Ordinal.

Color-coded flows (blue ingress, purple queue, green/amber/red subscribers) plus an upward "rebuild" path showing the cockroach recovery principle — the Evidence Store can be fully reconstructed from the Bitcoin-anchored Ordinals if lost.

## Why This Version

v3.0 aligns the visual with Pitch Spine v0.4 and the Triple Subscriber Pipeline (TSP) PRDs delivered in B-059 (see [[Brain/wiki/growdirect-triple-subscriber|Triple Subscriber Pipeline]]). Changes from v2.0:

- Naming reconciled across Pitch Spine, Manifesto, and PRD docs
- Fan-out shown explicitly as Sub 1 / Sub 2 / Sub 3 with staged-immutability labels
- Upward rebuild arrows added
- Bitcoin timing annotation (T+~10min) on the Ordinal step

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-six-nodes|Six-Node Protocol]] — narrative counterpart
- [[Brain/wiki/growdirect-triple-subscriber|Triple Subscriber Pipeline]] — canonical PRD index
- [[Brain/wiki/growdirect-the-patent|The Patent]] — IP strategy

## Sources

- `docs/_archive/ip-vault/patent-visuals/Patent_Architecture_Visual_v3.0.html` — the rendered SVG schematic
