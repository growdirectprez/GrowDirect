---
date: 2026-04-22
type: wiki
status: active
tags: [growdirect, warchest, notary, merkle, inscription]
sources:
  - docs/_archive/ip-vault/warchest/sources/11-the-notary.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
----

**Wiki:** [[Brain/Home|Home]]

# The Notarization Service
*Spine: ACT 4B | Manifesto: IV.2*

**Status:** 📝 DRAFT — Extracted from Manifesto IV.2 + ElJeffe Business Model Addendum Layer 2. Awaiting Jeffe review.

---

## Layer 2: The Operation

When any network transmits a webhook — Square, Epic MyChart, FedEx, any source — elJeffe receives the raw payload, seals it, and notarizes it on the Bitcoin time chain. The operation is the same regardless of the source network. The protocol does not care whether the event is a refund, a prescription, a shipment, or a legal filing. It cares that the event happened, and it makes that fact permanent.

The process is six steps:

1. **Receive** the raw payload at the API gateway
2. **Seal** it instantly in the PostgreSQL evidence store — milliseconds, not minutes
3. **Batch** recent hashes into a Merkle tree
4. **Inscribe** the Merkle root into GrowDirect's Ordinal pool
5. **Map** every event hash to its position in the tree
6. **Return** two responses: instant hash confirmation, and Bitcoin block confirmation within approximately ten minutes

The merchant sees two moments. The first is immediate: the event is sealed, the chain position is assigned, the evidence is immutable in GrowDirect's database. The second arrives when Bitcoin confirms: the inscription ID, the block number, the block explorer URL. At that point, the notarization exists on the most secure computational network ever built.

## The Canonical Record

Every Ordinal inscription is a cryptographic commitment. It says: this event occurred. We notarized it. Here is the proof. Block 884,201. Hash a3f9c7. Timestamp 2:17 PM UTC, February 27, 2026.

The canonical record is not a database. It is the Bitcoin time chain. It cannot be altered retroactively. Cannot be forked in a way that changes the past. Cannot be consensus-attacked. Cannot be erased. The notarization is permanent.

Who holds the keys to create that Ordinal? GrowDirect. That control — foundational — is the moat. Every other notarization service is a database with an archive feature. GrowDirect is the Bitcoin time chain itself.

## Source Agnostic by Design

The notarization service is not a retail product. It is a universal event notarization protocol. Square is the beachhead — the first source network, the first vertical. But the architecture is source-agnostic from day one. The same pipeline that notarizes a Square refund can notarize an insurance claim, a healthcare encounter, a supply chain handoff, a legal signature.

The webhook arrives. The hash is computed on the raw, unnormalized payload — before any transformation, before any parsing. The hash is the witness. The inscription is the proof. The source network is irrelevant to the cryptographic guarantee.

---

**Source:** ElJeffe Business Model Addendum Layer 2 + Manifesto IV.2
**Manifesto tag:** `Manifesto: IV.2`
**Filled:** February 27, 2026 — ALX (B-059 Phase 1)

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/warchest/sources/11-the-notary.md` — the war-chest source this card summarizes
