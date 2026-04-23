---
date: 2026-04-22
type: wiki
tags: [growdirect, warchest, protocol-pipe, architecture]
sources:
  - docs/_archive/ip-vault/warchest/sources/22-the-pipe.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# The Protocol Pipe
*Spine: ACT 5C | Manifesto: V.4*

**Status:** 📝 DRAFT — Extracted from Sprint 6 WO B-052 + Manifesto V.4. Awaiting Jeffe review.

---

## The Full Vertical Slice

The protocol pipe is the proof that the system works end to end. Not a simulation. Not a mock. Not seeded data. Real merchant authorization. Real Square webhooks. Real Bitcoin inscription. Real receipt.

The pipe has six stages:

1. **Square OAuth 2.0** — The merchant authorizes Canary to access their Square data. Standard OAuth flow. One click. The merchant's Square account is now connected.

2. **Webhook Receipt** — Square sends signed webhooks to Canary's endpoint. Every payload is HMAC-verified before any processing begins. If the signature does not match, the payload is rejected. No exceptions.

3. **Chirp Rule Evaluation** — The parsed event runs through the detection engine. Twenty-six rules across eight fraud categories. If a rule fires — for example, a refund exceeding ten dollars — a Chirp is generated and delivered to the merchant's phone.

4. **PostgreSQL Seal (Sub 1)** — The raw payload is hashed and written to the append-only evidence store. INSERT-only. Hash-chained. Immutable. The seal happens in milliseconds, independent of whether a Chirp fired. Every event is sealed, not just flagged ones.

5. **Bitcoin Inscription (Sub 3)** — Event hashes accumulate into a Merkle batch. When the batch threshold is reached — 100 events or 10 minutes, whichever comes first — the Merkle root is inscribed as an Ordinal on the Bitcoin time chain via the OrdinalsBot API. Bitcoin confirms in approximately ten minutes.

6. **TX ID Receipt** — The merchant receives the Bitcoin transaction ID, block number, and block explorer URL. The notarization is complete. The event exists on the most secure computational network ever built.

## Why the Pipe Matters

The protocol pipe is not a feature. It is the entire product compressed into a single flow. Every component that matters — authorization, ingestion, detection, immutability, inscription, proof — is exercised in one merchant's refund.

When the pipe is complete, the system is proven. An investor can watch a real transaction flow from a real Square merchant's register to the Bitcoin time chain in real time. There is nothing to explain. There is nothing to imagine. It works, and the proof is on the chain.

## What Exists vs. What Is Being Built

The evidence seal layer (Sub 1) is complete — built and tested in Sprint 5. The Chirp detection engine exists. The protocol pipe in Sprint 6 adds three new components: OAuth flow, webhook signature verification, and the inscription bridge to Bitcoin. When those three pieces connect to the existing infrastructure, the pipe is end to end.

---

**Source:** Sprint 6 WO B-052 + Manifesto V.4
**Manifesto tag:** `Manifesto: V.4`
**Filled:** February 27, 2026 — ALX (B-059 Phase 1)

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/warchest/sources/22-the-pipe.md` — the war-chest source this card summarizes
