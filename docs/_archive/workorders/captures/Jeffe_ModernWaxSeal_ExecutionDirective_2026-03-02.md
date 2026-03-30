---
type: decision
domain: business
status: active
created: 2026-03-02
updated: 2026-03-19
---
# Capture — Jeffe: The Modern Wax Seal + Execution Directive

**Date:** March 2, 2026
**Source:** Jeffe (CEO), live session
**Context:** Follow-up to GRO-46, Namespace Identity Primitive
**Classification:** MAXIMUM CONFIDENTIAL

---

## Raw Intent

> "This can be a whole product unto itself. Verify anything. It's like the modern day wax seal for the individual. How do we mint these? I want this namespace idea firmly defined and how we set up the blockchain architecture. Set up the webhook pumps back and forth using the Square sandbox and our world class data model to prove this out. If we make it work right here in this environment it scales immediately and it's in the culture by Christmas '26."

## What Jeffe Is Saying

1. **The .jeffe Ordinal IS the product.** Not a feature of Canary LP. Not a component of RaaS. It's a standalone product: a universal verification seal for any individual, any business, any event. The modern wax seal.

2. **He wants practical steps.** Not more design docs. How do we actually mint an Ordinal? What are the literal commands, the wallets, the tools, the costs?

3. **Prove it in this environment.** Use the Square sandbox webhooks + the CRDM data model + the TSP pipeline we already built. Hook the inscription layer onto what exists. If a Square webhook flows through the pipeline and results in a verified Ordinal inscription, the architecture is proven.

4. **If it works here, it scales immediately.** The CRDM `external_identities` table (GRO-45 Amendment 1) means any new POS is just a row. The TSP pipeline is POS-agnostic. The polling adapter (GRO-27) handles non-webhook APIs. The architecture is already designed for multi-POS. The inscription layer is the last mile.

5. **In the culture by Christmas '26.** ~10 months. That's the timeline. Not "in production" — "in the culture." People talking about it. "You got jeffe'd" as a phrase. The wax seal as a concept people understand.

## The Wax Seal Analogy

This is the pitch that non-technical people will understand instantly:

- **Medieval wax seal:** A unique impression pressed into hot wax. Proves who sent it. Proves it wasn't opened. Proves it's authentic. Cannot be forged because the seal die is one-of-a-kind.
- **.jeffe Ordinal:** A unique inscription pressed into Bitcoin. Proves who created it. Proves it wasn't altered. Proves it's authentic. Cannot be forged because the proof-of-work cost is prohibitive and the block height is permanent.

The wax seal was the identity layer of commerce for 500 years. The .jeffe Ordinal is its successor.

---

## Execution Plan — How We Mint These

### Phase 0: Foundation (Week 1–2)

**Goal:** Mint the first .jeffe namespace Ordinal. Prove the inscription works.

**Step 1: Wallet Setup**
- Create a dedicated GrowDirect Bitcoin wallet (Sparrow Wallet or Bitcoin Core)
- This is the treasury wallet — all Genesis Pool Ordinals live here
- Fund with minimum BTC for inscription fees (~0.001 BTC should cover initial tests)
- Back up seed phrase. Jeffe + one other keyholder. Never digital. Paper only.

**Step 2: Choose Inscription Tool**
- **ord** (Casey Rodarmor's reference implementation) — the canonical Ordinals CLI
  - Install: `cargo install ord` (requires Rust toolchain)
  - Requires a synced Bitcoin node OR connects to a remote node
  - Commands: `ord wallet create`, `ord wallet inscribe`
- **Alternative for faster start:** Use a hosted inscription service (e.g., Gamma.io, OrdinalsBot) for first test inscriptions, then move to self-hosted `ord` for production
- **Recommendation:** Start with hosted service for proof-of-concept speed, migrate to self-hosted `ord` for production (sovereignty matters)

**Step 3: Define the Namespace Record**
- The inscription content is a JSON payload:

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "namespace",
  "name": "growdirect",
  "root": true,
  "created": "2026-03-XX",
  "owner_pubkey": "<GrowDirect treasury public key>",
  "resolver": "https://api.eljeffe.io/v1/resolve/",
  "chain": {
    "previous": null,
    "sequence": 0
  }
}
```

- This is small — ~300 bytes. Inscription cost at 10 sat/vbyte ≈ ~$0.50–$2.00. Trivial.
- The `chain.previous` field links to the prior inscription, creating the hash chain on Bitcoin itself.

**Step 4: Inscribe the Root**
```bash
# Using ord CLI
ord wallet inscribe --file namespace_root.json --fee-rate 10

# Returns:
# inscription_id: <txid>i0
# Block height: XXXXXX  ← THIS IS THE MOAT
```

- Once confirmed (~10 min for next block), the .jeffe root namespace exists on Bitcoin permanently.
- Record the inscription ID and block height. This is Genesis.

### Phase 1: Webhook → Inscription Pipeline (Week 2–4)

**Goal:** Square sandbox webhook flows through TSP pipeline and produces an Ordinal inscription.

**Step 5: Square Sandbox Webhook Setup**
- We already have the Square sandbox connected (B-085 sandbox toolbar)
- Square sandbox generates test webhooks: `payment.created`, `refund.created`, etc.
- These already flow into `canary:events` Valkey Stream via TSP-01

**Step 6: Wire Sub 3 (Merkle Inscribe) to Ordinal Minting**
- Sub 3 currently batches events into Merkle trees (TSP design, not yet implemented)
- Wire the Merkle root output to an inscription command:

```
Square Webhook → Gateway → Valkey Stream → Sub 1 (Seal) → Sub 2 (Parse) → Sub 3 (Merkle)
                                                                                    ↓
                                                                          Merkle Root
                                                                                    ↓
                                                                     ord wallet inscribe
                                                                                    ↓
                                                                        Bitcoin Ordinal
```

- The inscription payload for a Merkle batch:

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "merkle_batch",
  "namespace": "growdirect",
  "batch_id": "<uuid>",
  "merkle_root": "<sha256 hash>",
  "event_count": 42,
  "time_range": {
    "first": "2026-03-XX T00:00:00Z",
    "last": "2026-03-XX T01:30:00Z"
  },
  "chain": {
    "previous": "<prior inscription_id>",
    "sequence": 1
  }
}
```

- Still small (~400 bytes). Still cheap. But now it anchors 42 events (or however many are in the batch) to a single Ordinal.

**Step 7: Verification Round-Trip**
- After inscription, verify the round-trip:
  1. Take any event from the batch
  2. Recompute its hash
  3. Reconstruct the Merkle path
  4. Verify the Merkle root matches the on-chain inscription
  5. Verify the inscription exists at the claimed block height
- This is the `POST /v1/verify` flow. If this works, RaaS works.

### Phase 2: Avalanche Side-Chain + Burner Layer (Week 4–8)

**Goal:** Stand up the Avalanche subnet for fast operations. Mint the first burner.

**Step 8: Avalanche Subnet Setup**
- Deploy a private Avalanche subnet (per GRO-13 Decision 6: private subnet through Phase 2)
- Subnet nodes run on GrowDirect infrastructure (local-first, per Principle 9)
- Deploy NameRegistry smart contract:

```solidity
// Simplified — Tom to architect the full contract
contract NameRegistry {
    mapping(string => NameRecord) public names;

    struct NameRecord {
        address owner;
        string btcInscriptionId;  // Links to Bitcoin Ordinal
        uint256 registeredAt;
        uint256 expiresAt;        // Annual renewal
        bool transferable;        // false through Phase 2
    }

    function register(string name, string btcInscriptionId) external;
    function mintBurner(string parentName, string burnerLabel, uint256 ttl) external;
    function revokeBurner(string burnerName) external;
}
```

**Step 9: Bridge Bitcoin Ordinal ↔ Avalanche**
- The Bitcoin inscription ID is stored in the Avalanche NameRegistry
- This is the bridge: the Ordinal on Bitcoin is the root of trust, the Avalanche contract is the operational layer
- Tom to design the attestation flow: how does the Avalanche contract verify the Bitcoin inscription exists?

**Step 10: Mint First Burner**
```
mintBurner("sunrise-coffee", "july-promo", ttl=30 days)
→ Creates: july-promo.sunrise-coffee.jeffe
→ Resolves for 30 days
→ After TTL: stops resolving, record marked expired
→ Root Ordinal on Bitcoin: unchanged, permanent
```

### Phase 3: End-to-End Proof (Week 6–10)

**Goal:** Full loop working in the dev environment. Webhook in, Ordinal out, verify round-trip, burner minting.

**Step 11: Prove the Full Loop**
1. Square sandbox fires `payment.created` webhook
2. TSP pipeline: Seal → Parse → Merkle batch
3. Merkle root inscribed as Bitcoin Ordinal (testnet for dev, mainnet for production)
4. Namespace owner mints a burner on Avalanche
5. External party calls `POST /v1/verify` with a receipt hash
6. System verifies against Merkle tree → confirms against on-chain inscription
7. Returns: `{ "verified": true, "block": XXXXXX, "namespace": "sunrise-coffee.jeffe" }`
8. "You got jeffe'd."

**Step 12: L402 Payment Gate**
- Wire Lightning micropayment to the verify endpoint
- Caller pays 1 sat → receives 402 → pays invoice → gets verification result
- This is revenue stream #2 (validation) and #3 (RaaS) activated

### Phase 4: Scale + Culture (Week 10–40, through Christmas '26)

**Goal:** Production deployment. Real merchants. "In the culture."

**Step 13: Mainnet Migration**
- Move from Bitcoin testnet to mainnet for inscriptions
- Fund treasury wallet with production BTC
- First mainnet inscription = Genesis Block for .jeffe namespace

**Step 14: First Real Merchant**
- One Square merchant, live webhooks, real transactions
- Their receipts inscribed on Bitcoin
- Their .jeffe namespace live and resolvable
- They can mint burners for promotions

**Step 15: "In the Culture"**
- "You got jeffe'd" as the verification notification
- burner.jeffe as the disposable endpoint product
- The wax seal analogy in every pitch, every demo, every conversation
- Will's LEO playbook + Pi demo station running the full loop live
- Investor site v4.0 (GRO-16) telling this story

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    THE .JEFFE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Square   │    │ Clover   │    │ Toast    │  ... Any POS  │
│  │ Webhooks │    │ Webhooks │    │ Webhooks │              │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘              │
│       │               │               │                     │
│       └───────────────┼───────────────┘                     │
│                       ▼                                      │
│              ┌────────────────┐                              │
│              │  API Gateway   │  ← L402 / JWT / HMAC        │
│              └───────┬────────┘                              │
│                      ▼                                       │
│              ┌────────────────┐                              │
│              │ canary:events  │  ← Valkey Stream             │
│              │ (TSP-01 v1.1) │                              │
│              └───────┬────────┘                              │
│                      ▼                                       │
│         ┌────────────┼────────────┐                         │
│         ▼            ▼            ▼                          │
│    ┌─────────┐ ┌──────────┐ ┌──────────┐                   │
│    │ Sub 1   │ │ Sub 2    │ │ Sub 3    │                   │
│    │ SEAL    │ │ PARSE    │ │ MERKLE   │                   │
│    │ (hash)  │ │ (route)  │ │ (batch)  │                   │
│    └─────────┘ └──────────┘ └────┬─────┘                   │
│                                   ▼                          │
│                          ┌────────────────┐                  │
│                          │  Merkle Root   │                  │
│                          └───────┬────────┘                  │
│                                  ▼                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              BITCOIN L1 (Permanent)                  │    │
│  │                                                      │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  Ordinal Inscription                         │    │    │
│  │  │  • Namespace root (.jeffe)                   │    │    │
│  │  │  • Merkle batch roots                        │    │    │
│  │  │  • Chain links (previous → current)          │    │    │
│  │  │  • Block height = permanent timestamp        │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│                    inscription_id                             │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │          AVALANCHE SIDE-CHAIN (Operational)          │    │
│  │                                                      │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │    │
│  │  │ NameRegistry│  │   Burner    │  │  Payment   │  │    │
│  │  │  Contract   │  │   Minting   │  │   Gate     │  │    │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │    │
│  │                                                      │    │
│  │  sunrise-coffee.jeffe  ← permanent (links to BTC)   │    │
│  │  july-promo.sunrise-coffee.jeffe  ← burner (TTL)    │    │
│  │  returns.sunrise-coffee.jeffe  ← burner (TTL)       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│                         ▼                                    │
│              ┌────────────────┐                              │
│              │  RaaS API      │                              │
│              │  POST /verify  │  ← L402 (1 sat)             │
│              │  GET /receipt  │  ← L402 (1 sat)             │
│              │  GET /resolve  │  ← Public                    │
│              └────────────────┘                              │
│                                                              │
│              "You got jeffe'd." 🔏                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Timeline to Christmas '26

| Phase | Weeks | What Ships |
|-------|-------|------------|
| **0: Foundation** | 1–2 | First .jeffe Ordinal inscribed. Wallet + tools + namespace record defined. |
| **1: Webhook → Inscription** | 2–4 | Square sandbox webhooks produce Ordinal inscriptions via TSP pipeline. Verification round-trip works. |
| **2: Avalanche + Burners** | 4–8 | Private subnet live. NameRegistry contract deployed. First burner.jeffe minted. |
| **3: End-to-End Proof** | 6–10 | Full loop: webhook → seal → parse → merkle → inscribe → verify. L402 payment gate live. |
| **4: First Merchant** | 10–16 | One real Square merchant, live webhooks, real inscriptions, real .jeffe namespace. |
| **5: Multi-POS** | 16–28 | Clover or Toast connected via polling adapter + external_identities. Same pipeline, different source. |
| **6: Culture** | 28–40 | "You got jeffe'd" in the wild. Pi demo station. LEO playbook. Investor site v4.0 live. In the culture by Christmas. |

---

*Captured by ALX | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
