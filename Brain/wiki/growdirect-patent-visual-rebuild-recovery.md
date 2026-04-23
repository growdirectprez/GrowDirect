---
date: 2026-04-22
type: wiki
tags: [growdirect, patent-visuals, patent, rebuild, recovery, cockroach]
sources:
  - docs/_archive/ip-vault/patent-visuals/Patent_Rebuild_Recovery_v1.0.html
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Patent Schematic — Rebuild & Recovery Path v1.0 (FIG. 6)

Rendered SVG schematic filed as **FIG. 6** in Patent Application 63/991,596. Version 1.0.

## What the Figure Depicts

The disaster recovery path — a full rebuild of the Evidence Store and Structured Store from the Bitcoin-anchored Ordinals. The figure is captioned **"THE COCKROACH PRINCIPLE"**: if every server, database, and backup in the stack is destroyed, the system can be reconstructed from Bitcoin alone.

The flow:

1. **Loss Event** — catastrophic data loss (ransomware, disaster, operator malfeasance)
2. **Fetch Ordinals** — pull the Merkle-batched Ordinal inscriptions from Bitcoin
3. **Unfold Merkle Batches** — expand each batch back into its constituent event hashes
4. **Rehydrate Evidence Store** — write hashes to a fresh INSERT-only store
5. **Rebuild Structured Store** — re-parse events from the source authorities (Square, etc.) guided by the Evidence Store
6. **Verify** — bilateral hash comparison confirms every event in the rebuilt state matches the original

## Why It Matters

This figure supports patent claims around **self-healing architecture** and **trust minimization**. The cockroach principle is the ultimate answer to "what if you lose your data?" — *we don't lose data, because Bitcoin is our backup*.

It is also the core of the **Sovereignty** pitch: no regulator, bank, or cloud provider can seize or corrupt the evidence layer. The Bitcoin anchor is independently verifiable by anyone, anywhere.

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-sovereignty|Sovereignty]] — independence as moat
- [[Brain/wiki/growdirect-research-worm-exposure|WORM Exposure Sprint]] — immutability posture
- [[Brain/wiki/growdirect-the-patent|The Patent]] — IP strategy

## Sources

- `docs/_archive/ip-vault/patent-visuals/Patent_Rebuild_Recovery_v1.0.html` — the rendered SVG schematic
