---
type: workorder
domain: raas
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-46 — Sovereign Namespace Architecture: Server-Independent .jeffe Resolution

**Issue:** GRO-46 (Serializable Gate — Ordinal-as-Identity)
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** MAXIMUM CONFIDENTIAL — Core Architecture
**Origin:** Jeffe directive during alignment review of GRO-47/46/13/45 stack
**Routes To:** Tom (architecture), PhD (patent implications), Syd (sovereignty legal review)
**Gate:** Tom validates resolution protocol. Syd reviews self-sustaining entity implications.

---

## 0. Jeffe's Directive

> "It should not rely on a server anywhere."

The .jeffe namespace must be self-sustaining. If every GrowDirect server goes dark, the namespace still resolves. The data is on Bitcoin. The protocol is on Bitcoin. The verification is math. GrowDirect is the first operator — not the only possible operator.

This is the sovereign namespace principle: **the seal doesn't need the seal-maker to still be alive for you to verify it's authentic.**

---

## 1. Three-Layer Resolution Stack

Resolution works at three layers. Each layer is independently functional. Higher layers are faster. Lower layers are more permanent. Any layer can fail without breaking the others.

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 3 — GrowDirect API (Hot Cache)                   │
│  namespace_registrations table in Postgres               │
│  Millisecond resolution. Fully disposable.               │
│  If this dies: fall back to Layer 2.                     │
├─────────────────────────────────────────────────────────┤
│  LAYER 2 — Avalanche Subnet (Fast Operations)           │
│  NameRegistry smart contract                             │
│  Second-scale resolution. Burner minting. Payment gate.  │
│  If this dies: fall back to Layer 1. Burners expire      │
│  naturally. Permanent namespaces still resolve on BTC.   │
├─────────────────────────────────────────────────────────┤
│  LAYER 1 — Bitcoin Ordinals (Permanent Truth)           │
│  Inscriptions with protocol: "jeffe"                     │
│  Anyone with a Bitcoin node can resolve any .jeffe name. │
│  Cannot die unless Bitcoin dies.                         │
└─────────────────────────────────────────────────────────┘
```

### Resolution Priority (Normal Operation)

```
Client calls POST /v1/verify { merchant_id: "sunrise-coffee.jeffe" }
  │
  ├─ Try L3: Postgres namespace_registrations (< 1ms)
  │    └─ Hit? → Return merchant_id UUID → continue verification
  │
  ├─ Try L2: Avalanche NameRegistry contract (< 2s)
  │    └─ Hit? → Return owner + inscription_id → continue verification
  │
  └─ Try L1: Bitcoin Ordinal scan via ord indexer (minutes)
       └─ Hit? → Return inscription data → continue verification
```

### Degraded Operation (GrowDirect Offline)

```
Third party runs their own .jeffe resolver:
  1. Run Bitcoin node + ord indexer
  2. Scan for inscriptions matching protocol: "jeffe"
  3. Build local index of namespace → owner_pubkey mappings
  4. Serve resolution queries from local index
  5. Verify receipts by reconstructing Merkle proofs from on-chain data

No GrowDirect server needed. No Avalanche subnet needed. Just Bitcoin.
```

---

## 2. Genesis Inscription — The Self-Describing Protocol

For the namespace to be truly server-independent, the protocol specification itself must live on Bitcoin. The first inscription — Genesis — contains everything a third party needs to build a resolver:

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "genesis",
  "created": "2026-03-XX",
  "root_authority": "<GrowDirect treasury public key>",
  "spec": {
    "namespace_format": "^[a-z0-9-]+\\.jeffe$",
    "subdomain_format": "^[a-z0-9-]+\\.[a-z0-9-]+\\.jeffe$",
    "inscription_types": [
      "genesis",
      "namespace",
      "merkle_batch",
      "revocation"
    ],
    "verification_method": "sha256_merkle_proof",
    "payment_gate": "L402",
    "chain_rule": "Each inscription links to previous via chain.previous field, forming immutable sequence"
  },
  "resolver_hint": "https://api.eljeffe.io/v1/resolve/",
  "chain": {
    "previous": null,
    "sequence": 0
  }
}
```

**Key design decisions:**

- `spec` field contains the full protocol grammar. A developer reading this JSON can build a resolver.
- `resolver_hint` is a convenience pointer to GrowDirect's API, not a dependency. It's a "start here" for clients, not a requirement.
- `root_authority` is the GrowDirect treasury public key. This establishes provenance — all subsequent .jeffe inscriptions must chain back to this key (directly or via delegation).
- `inscription_types` is the complete vocabulary. Any inscription with `protocol: "jeffe"` and a `type` not in this list is invalid.

---

## 3. Namespace Inscription (Expanded for Sovereignty)

The namespace inscription from the Wax Seal capture needs additional fields for self-sufficient resolution:

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "namespace",
  "name": "sunrise-coffee",
  "owner_pubkey": "<merchant's public key>",
  "resolver_hint": "https://api.eljeffe.io/v1/resolve/sunrise-coffee",
  "registered_by": "<GrowDirect registrar pubkey>",
  "tier": "standard",
  "metadata": {
    "display_name": "Sunrise Coffee Co.",
    "category": "food_and_beverage",
    "pos_systems": ["square"]
  },
  "chain": {
    "previous": "<genesis inscription_id OR prior namespace inscription_id>",
    "sequence": 1
  }
}
```

**What makes this self-sufficient:**

- `owner_pubkey` — Anyone can verify the owner without calling a server. The pubkey IS the identity.
- `registered_by` — Proves GrowDirect (the registrar) authorized this registration. Third parties can verify the registrar's signature chains back to the Genesis `root_authority`.
- `metadata` — Optional enrichment. Makes the index useful without a database lookup.
- `chain.previous` — Links every inscription into an immutable sequence. Anyone can reconstruct the full history by following the chain.

---

## 4. Merkle Batch Inscription (Updated with Sovereignty Fields)

```json
{
  "protocol": "jeffe",
  "version": "1.1",
  "type": "merkle_batch",
  "namespace": "sunrise-coffee",
  "batch_id": "<uuid>",
  "merkle_root": "<sha256 hash of event Merkle tree>",
  "event_count": 42,
  "time_range": {
    "first": "2026-03-01T00:00:00Z",
    "last": "2026-03-01T01:30:00Z"
  },
  "attestation": {
    "device_integrity": true,
    "device_count": 3,
    "device_root": "<sha256 hash of device Merkle tree>",
    "flags": []
  },
  "proof_data": {
    "tree_depth": 6,
    "leaf_count": 42,
    "algorithm": "sha256"
  },
  "chain": {
    "previous": "<prior inscription_id>",
    "sequence": 47
  }
}
```

**New `proof_data` block:** Tells a third-party verifier everything they need to reconstruct the Merkle tree. Without this, they'd need to guess the tree structure. With it, verification is deterministic from on-chain data alone.

---

## 5. Revocation Inscription (New Type)

For namespaces that expire or are suspended (GRO-13 Decision 3: annual renewal), the on-chain record needs a revocation mechanism:

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "revocation",
  "target": "<inscription_id of the namespace being revoked>",
  "reason": "expired",
  "revoked_by": "<GrowDirect registrar pubkey>",
  "effective_at": "2027-03-15T00:00:00Z",
  "chain": {
    "previous": "<prior inscription_id>",
    "sequence": 48
  }
}
```

**Why this matters for sovereignty:** If a namespace expires, third-party resolvers need to know. Without a revocation inscription, they'd assume every namespace is still active. The revocation is on-chain, permanent, and verifiable — no server needed to check expiry status.

**Historical receipts remain valid.** The revocation affects namespace resolution, not receipt verification. Merkle proofs inscribed before the revocation are still mathematically valid. The receipts were sealed when the namespace was active. The seal doesn't break because the seal-holder's subscription lapsed.

This directly answers GRO-13 Syd Question N-3 (expired namespace receipt validity) at the architecture level.

---

## 6. Resolution Without GrowDirect — Step by Step

A third party who wants to resolve .jeffe names and verify receipts with zero GrowDirect involvement:

### Setup (One Time)
1. Run a Bitcoin full node (or connect to a trusted node)
2. Install `ord` indexer (or equivalent Ordinals indexer)
3. Configure indexer to filter for `"protocol": "jeffe"` inscriptions
4. Build local database: index all namespace, merkle_batch, and revocation inscriptions

### Resolve a Namespace
1. Query local index for `type: "namespace"` WHERE `name = "sunrise-coffee"`
2. Verify `chain` links back to Genesis inscription (trust chain)
3. Check for any `type: "revocation"` targeting this inscription
4. If no revocation: namespace is active. Return `owner_pubkey`.
5. If revocation exists and `effective_at` is past: namespace is expired.

### Verify a Receipt
1. Receive `event_hash` from the party requesting verification
2. Query local index for `type: "merkle_batch"` WHERE `namespace = "sunrise-coffee"`
3. For each batch: check if `event_hash` exists as a leaf in the Merkle tree
4. Reconstruct Merkle proof using `proof_data` (tree_depth, leaf_count, algorithm)
5. Verify the reconstructed `merkle_root` matches the on-chain inscription
6. If match: receipt is verified. Return block height + inscription_id.

### Charge for Verification (Optional)
1. Stand up an L402 endpoint in front of the resolver
2. Charge whatever fee the market will bear
3. GrowDirect charges 1 sat. A competitor could charge 0.5 sat. Or 2 sat.
4. The protocol doesn't enforce pricing. The market does.

**This is the self-sustaining model.** GrowDirect operates the fastest, most complete resolver (L3 + L2 + L1). But the protocol is open. The data is public. Anyone can compete on resolution speed and price. GrowDirect's moat is first-mover advantage + the deepest index + the only registrar (through Phase 2).

---

## 7. What This Means for Each Layer

### Layer 3 — Postgres `namespace_registrations` (Reclassified)

The table designed in the Alignment Amendment is **not** the source of truth. It's a hot cache. Reclassification:

| Field | Old Role | New Role |
|-------|----------|----------|
| `namespace_name` | Primary key for resolution | Cache key (rebuildable from L1) |
| `merchant_id` | Bridge to CRDM | Operational mapping (GrowDirect-specific) |
| `inscription_id` | Cross-reference | **Pointer to L1 source of truth** |
| `status` | Authoritative state | **Derived from L1** (check for revocation inscriptions) |
| `expires_at` | Authoritative expiry | **Derived from L1** (check for revocation or renewal inscriptions) |

The table stays exactly as designed. The DDL doesn't change. Only its architectural classification changes: from "bridge" to "cache."

### Layer 2 — Avalanche NameRegistry (Reclassified)

The NameRegistry contract is the **operational layer** — fast reads, burner minting, payment gating. It's not the source of truth either. It's an accelerator.

| Function | Dependency | Fallback |
|----------|-----------|----------|
| Namespace resolution | Contract query | Fall back to L1 Bitcoin scan |
| Burner minting | Contract transaction | Not available without L2 (burners are L2-native) |
| Payment gating | Contract + Lightning | Fall back to direct L1 verification (no payment gate) |
| Expiry enforcement | Contract state | Fall back to L1 revocation inscriptions |

**Burners are the one thing that truly requires L2.** Permanent namespaces survive L2 failure. Burners don't — they're designed to be ephemeral, and their operational home is the subnet. This is architecturally correct: permanent things on L1, ephemeral things on L2.

### Layer 1 — Bitcoin Ordinals (Source of Truth)

| Inscription Type | Permanence | Verifiable Without Server |
|-----------------|------------|--------------------------|
| Genesis | Forever | Yes — it's the root of the trust chain |
| Namespace | Forever | Yes — pubkey + chain link proves ownership |
| Merkle Batch | Forever | Yes — Merkle proof is math, not a service |
| Revocation | Forever | Yes — proves a namespace was expired/suspended |

---

## 8. Implications for GRO-47 (Namespace PoC)

GRO-47's Phase 0 now has an additional deliverable: **the Genesis inscription must be self-describing.** The namespace record JSON from the Wax Seal capture needs the `spec` field. This is the one inscription we cannot get wrong — it's permanent, it's the root, and it defines the protocol for all future inscriptions.

**Updated Phase 0 checklist:**
1. ~~Wallet setup~~ (unchanged)
2. ~~Choose inscription tool~~ (unchanged)
3. **Define Genesis inscription** (UPDATED — must include full `spec` block)
4. **Define namespace inscription format** (UPDATED — must include `owner_pubkey`, `registered_by`, `metadata`)
5. ~~Inscribe the root~~ (unchanged, but now inscribing a richer payload)

**Updated Phase 1 addition:**
- After first Merkle batch inscription, **verify the round-trip using ONLY Bitcoin data.** No Postgres lookup. No Avalanche query. Pure L1 verification. This proves the sovereign architecture works.

---

## 9. Patent Implications (PhD Action)

The sovereign namespace architecture may contain novel claims beyond the serializable gate:

1. **Self-describing protocol inscription** — A protocol whose specification is inscribed on Bitcoin L1, enabling permissionless resolver construction. Prior art search needed.
2. **Three-layer degradation-tolerant resolution** — A naming system that functions at three independent layers with automatic fallback. Each layer failure is non-fatal.
3. **On-chain revocation for off-chain state** — Using Bitcoin inscriptions to revoke/expire namespace registrations without requiring any server to enforce the expiry.

PhD should evaluate whether these are patentable claims or obvious extensions of existing Ordinals work.

---

## 10. Syd Questions (New)

| # | Question | Context |
|---|----------|---------|
| S-1 | If .jeffe is designed to be server-independent, does GrowDirect have any legal obligation to keep operating the resolver? | Self-sustaining design may create an argument that GrowDirect's operational role is optional. Does this affect our duty to namespace holders? |
| S-2 | Does a self-describing on-chain protocol create open-source obligations? | The spec is public on Bitcoin. Does publishing it as an inscription constitute a public license? |
| S-3 | If a third party builds a competing .jeffe resolver, do we have IP claims? | The protocol is on Bitcoin. The implementation is ours. Where's the line? |
| S-4 | Does the revocation inscription model satisfy "notice" requirements for expired namespaces? | If a merchant's name expires and we inscribe a revocation, is that legally sufficient notice? |

---

## 11. Routing

| Agent | Action |
|-------|--------|
| **Tom** | Validate three-layer resolution architecture. Design the chain verification protocol (how does a third party prove an inscription chains back to Genesis?). Confirm Merkle proof reconstruction from `proof_data` is deterministic. |
| **PhD** | Patent evaluation: self-describing protocol inscription, three-layer degradation-tolerant resolution, on-chain revocation. Prior art search for each. |
| **Syd** | Answer S-1 through S-4. Particularly S-3 — this is the IP vs. open protocol tension. |
| **Jeremy** | Estimate: what does it take to build an `ord` indexer filter for `protocol: "jeffe"` inscriptions? Is it a config change or custom code? |
| **Jess** | The sovereign framing is investor material: "The protocol outlives the company." This belongs in GRO-16 investor site. Draft the language. |

---

## 12. The Wax Seal, Complete

> The medieval wax seal didn't need the seal-maker to still be alive. You could verify it a hundred years later — the impression in the wax was the proof. The seal-maker's workshop could burn down. The proof survived.
>
> .jeffe works the same way. The inscription is on Bitcoin. The protocol is on Bitcoin. The Merkle proof is mathematics. GrowDirect is the seal-maker — we mint the seals, we operate the fastest verification service, we're the only registrar. But the seals themselves don't need us. They're permanent. They're self-verifying. They outlive the company that made them.
>
> That's what makes this different from every other identity system. OAuth tokens expire. API keys get rotated. ENS names stop resolving if Ethereum's contract is abandoned. SSL certs last two years. A .jeffe inscription lasts forever.
>
> It's the modern wax seal. And the seal doesn't need the seal-maker.

---

*ALX | GRO-46 Sovereign Namespace Architecture | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
