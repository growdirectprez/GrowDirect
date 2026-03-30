---
type: pitch
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# The Patent
*Spine: ACT 6D | Manifesto: VI.4*

**Status:** 📝 DRAFT — Extracted from Manifesto VI.4 + Provisional 63/991,596 + ElJeffe Addendum. Awaiting Jeffe review.

---

## Patent Pending — Provisional Application 63/991,596

Filed February 26, 2026. Inventor: Geoffrey C. Lyle. Micro entity. The provisional patent application covers the elJeffe universal event notarization system.

GrowDirect can mark all products "Patent Pending" immediately. The utility application deadline is February 26, 2027 — twelve months from provisional filing. Patent counsel engagement is the next step.

## The Core Invention

The provisional covers the combination of six architectural elements that, individually, exist in prior art but have never been integrated into a single system for universal event notarization on a proof-of-work time chain.

**Six-Node Pipeline Architecture.** Receiver accepts any webhook from any network. Hasher computes SHA-256 on the raw, unnormalized payload. Evidence store writes to an INSERT-only sealed database. Application store provides a queryable replicated view. Batcher aggregates event hashes into a Merkle tree. Inscriber writes the Merkle root as a Bitcoin Ordinal.

**Triple Subscriber Pattern.** Three independent subscribers process the same inbound message simultaneously: sealed evidence store (write-once, never updated), queryable application store (replayable from evidence), and Bitcoin inscription service (batches independently). This three-way fork with distinct persistence and mutability guarantees does not appear in examined prior art.

**Bilateral Verification Method.** The merchant retains their payment network's send log. elJeffe retains the received payload with computed hash. Byte-for-byte comparison without mutual trust establishes independent verification — cryptographic proof of message integrity via bilateral log comparison.

## Five Claims

1. Universal event notarization via cryptographic hash inscription on a proof-of-work time chain, applied to any webhook-originated event stream.
2. Cryptographic key custody of a canonical inscription pool, wherein the custodying entity controls the authoritative notarization record and validation thereof.
3. Micropayment-gated validation of event notarizations against the canonical inscription record, denominated in the native currency of the time chain, processed via a Layer 2 payment protocol.
4. Programmatic scaling of the inscription pool in response to notarization volume thresholds, using treasury assets to purchase additional block space.
5. Merkle batching method — multiple event hashes aggregated into a Merkle tree, root inscribed as single canonical record, each event independently verifiable via Merkle proof path.

## Six Embodiments

The claims are filed across six vertical embodiments: Retail, Healthcare, Supply Chain, Legal, Insurance, and Government. Each embodiment demonstrates the same architecture applied to a different source network and event type. The universality of the claims is the strength — the patent does not protect a retail product. It protects a protocol.

## Patentability Assessment

| Requirement | Status |
|---|---|
| **Novelty** (35 U.S.C. 102) | The combination of six elements is not anticipated by any single prior art reference |
| **Non-Obviousness** (35 U.S.C. 103) | Incumbent platforms have not achieved this architecture despite competitive need |
| **Utility** (35 U.S.C. 101) | Produces specific, verifiable, commercially valuable results |
| **Subject Matter Eligibility** (Alice) | Defensible — system produces physically anchored, cryptographically verifiable results on a proof-of-work blockchain |

---

**Source:** Provisional 63/991,596 + Manifesto VI.4 + ElJeffe Business Model Addendum
**Manifesto tag:** `Manifesto: VI.4`
**Filled:** February 27, 2026 — ALX (B-059 Phase 1)
