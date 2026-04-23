---
date: 2026-04-22
type: wiki
tags: [growdirect, warchest, first-mover, moat]
sources:
  - docs/_archive/ip-vault/warchest/sources/30-first-mover.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Protection

> *"The blocks are already written. The position is permanent."*

---

## Intellectual Property Strategy

GrowDirect's IP protection operates on three layers: patent, trademark, and trade secret. Each layer reinforces the others. The combination creates a defensive position that strengthens with every inscription.

---

## Patent — Provisional Filing

**Status:** Patent Pending — Provisional Application 63/991,596

The provisional patent application covers the elJeffe universal event notarization system. The core invention is the combination of six architectural elements that, individually, exist in prior art but have never been integrated into a single system:

### Six-Node Pipeline Architecture

```
Node 1: Receiver    → Accepts any webhook from any network
Node 2: Hasher      → SHA-256 on the raw, unnormalized payload
Node 3: Evidence    → INSERT-only sealed evidence store
Node 4: Application → Queryable replicated store
Node 5: Batcher     → Merkle tree aggregation
Node 6: Inscriber   → Bitcoin Ordinal inscription of Merkle root
```

### Triple Subscriber Pattern
Three independent subscribers process the same inbound message simultaneously: sealed evidence store (write-once, never updated), queryable application store (replayable from evidence), and Bitcoin inscription service (batches independently). This three-way fork with distinct persistence and mutability guarantees does not appear in examined prior art.

### Bilateral Verification Method
The merchant retains their payment network's send log. elJeffe retains the received payload with computed hash. Byte-for-byte comparison without mutual trust establishes independent verification — cryptographic proof of message integrity via bilateral log comparison.

### Additional Novel Elements

| Element | What Makes It Novel |
|---|---|
| **Raw payload hashing** | Hash the verbatim received bytes — including transport metadata — without normalization. Prior systems hash summarized or structured data. Normalization breaks the witness chain. |
| **Merkle batching for Ordinals** | Multiple event hashes aggregated into a Merkle tree, root inscribed once, each event independently verifiable via Merkle proof path. Reduces on-chain footprint while preserving individual verifiability. |
| **Sat-gated validation (L402)** | Validation calls against the canonical inscription record are micropayment-gated via Lightning. Revenue is perpetual — flowing to GrowDirect for every verification of every event, indefinitely. |

### Patentability Assessment

| Requirement | Status |
|---|---|
| **Novelty** (35 U.S.C. 102) | The combination of six elements is not anticipated by any single prior art reference |
| **Non-Obviousness** (35 U.S.C. 103) | Incumbent platforms have not achieved this architecture despite competitive need — evidence of non-obviousness |
| **Utility** (35 U.S.C. 101) | Produces specific, verifiable, commercially valuable results |
| **Subject Matter Eligibility** (Alice) | Defensible — system produces physically anchored, cryptographically verifiable results on a proof-of-work blockchain |

---

## Trademark — gLog

**Status:** Filing recommended in Classes 9, 35, 42

"gLog" is a coined term — Geoffrey's Log. Coined marks receive the highest level of trademark protection. No major conflicts identified:

| Potential Conflict | Risk |
|---|---|
| "glog" open-source logging library | Different class (software development tools vs. event notarization services) |
| Google's GLog (C++ logging library) | Different class, lowercase convention, no commercial overlap |

Filing strategy: camelCase "gLog" preserves the distinctive character. Filed across three International Classes covering software (Class 9), business services (Class 35), and technology services (Class 42).

---

## Trade Secret — Operational Moat

Not everything is patented. Some competitive advantages are better protected as trade secrets:

| Trade Secret | Why Not Patent |
|---|---|
| **Chirp detection rules** | 22 specific rules for LP anomaly detection — revealing the exact thresholds helps competitors tune around them |
| **CRDM field mappings** | Enterprise-heritage data model with specific field lineage — operational know-how, not inventive |
| **Merkle batching parameters** | Specific batch sizes, timing windows, and cost optimization curves — operational tuning |
| **Pool management strategy** | When to expand the inscription pool, utilization thresholds, auto-purchase triggers |

Trade secrets are protected through access controls, NDA requirements, and operational security. They complement the patent by protecting the "how we run it" while the patent protects the "what we built."

---

## The Temporal Moat

The strongest protection is not legal — it is mathematical.

GrowDirect's Ordinals exist at specific Bitcoin blocks at specific timestamps. No competitor can go back and mint an Ordinal at Bitcoin block 884,201. That block is mined. It is history. It is math.

First mover on the Bitcoin time chain is permanent:
- The blocks are already written
- The key custody is established
- The founder provenance is on-chain
- The canonical range is claimed

Every day that passes, every block that confirms, the temporal moat widens. A competitor starting today cannot replicate the positional advantage of inscriptions written months or years earlier.

---

## Summary

| Layer | Protection | Scope |
|---|---|---|
| **Patent** | Provisional 63/991,596 | Six-node pipeline, triple subscriber, bilateral verification, Merkle batching, sat-gated validation |
| **Trademark** | gLog (filing recommended) | Coined term, highest protection class |
| **Trade Secret** | Operational controls | Detection rules, data model mappings, batching parameters, pool strategy |
| **Temporal** | Bitcoin inscription history | Blocks already written — cannot be replicated retroactively |

---

*GrowDirect Confidential*
*Patent Pending — Provisional 63/991,596*

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/warchest/sources/30-first-mover.md` — the war-chest source this card summarizes
