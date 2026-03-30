---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Condor B-069: Hybrid Chain Architecture Feasibility Brief
**Version:** 1.0
**Date:** March 1, 2026
**Author:** Condor (IP Sanitization Intern)
**Classification:** MAXIMUM CONFIDENTIAL — No external references to product names
**Status:** DELIVERED
**Manifesto:** IV.4 (Chain Architecture), V.5 (Inscription Economics)

---

## Executive Summary

A hybrid architecture placing a private Avalanche subnet as the real-time receipt minting layer — with Bitcoin Ordinals as the permanent anchor — is **technically feasible and architecturally sound**. The existing six-node pipeline and TSP PRD structure accommodate a hybrid model with surgical modifications: TSP-05 (Merkle batcher) gains an Avalanche subscriber, TSP-07/TSP-08 become chain-polymorphic via an adapter interface, and a new rollup contract bridges the two chains. The triple-subscriber model does not become a quad — instead, Sub 3 gains a pluggable chain target behind an abstraction layer.

Three Jeffe design directives are fully incorporable: user-defined inscription frequency (smart contract parameter), chain-agnostic destination (chain as configuration), and stacked inscriptions on a single satoshi (confirmed supported by the Ordinals protocol — each inscription gets a unique ID; none are overwritten).

**Feasibility verdict:** GREEN. No architectural blockers. Implementation complexity is MEDIUM (4-6 sprint effort for full hybrid, vs. 2-sprint effort for pure Ordinals pipeline already in progress). Recommend completing Sprint 6 pure Ordinals pipeline first, then layering Avalanche subnet as a Phase 2+ enhancement.

---

## 1. Receipt Minting Layer (Avalanche Subnet)

### 1.1 Smart Contract Design: Receipt Mint Transaction

A "receipt mint" on the Avalanche subnet is a single smart contract call that creates an immutable on-chain record of a POS event. The contract emits an event log that serves as the real-time confirmation to the merchant.

**Transaction structure (Solidity pseudocode):**

```solidity
// ReceiptMinter.sol — deployed on GrowDirect private Avalanche subnet

struct Receipt {
    bytes32 eventHash;        // SHA-256 of canonical CRDM payload
    bytes32 merchantId;       // Hashed merchant identifier (never plaintext)
    uint64  eventTimestamp;   // Unix epoch from Square webhook
    uint8   eventType;        // Enum: PAYMENT=1, REFUND=2, CASH_DRAWER=3, TIMECARD=4, etc.
    bytes32 previousHash;     // Chain link to prior receipt (per-merchant sequence)
    uint32  sequenceIndex;    // Monotonic counter per merchant
}

event ReceiptMinted(
    bytes32 indexed eventHash,
    bytes32 indexed merchantId,
    uint32  sequenceIndex,
    uint64  eventTimestamp
);

function mintReceipt(
    bytes32 _eventHash,
    bytes32 _merchantId,
    uint64  _eventTimestamp,
    uint8   _eventType,
    bytes32 _previousHash
) external onlyAuthorizedNode returns (uint32 sequenceIndex) {
    // Increment per-merchant sequence
    sequenceIndex = ++merchantSequence[_merchantId];

    // Store receipt (write-once — no update function exists)
    receipts[_eventHash] = Receipt({
        eventHash: _eventHash,
        merchantId: _merchantId,
        eventTimestamp: _eventTimestamp,
        eventType: _eventType,
        previousHash: _previousHash,
        sequenceIndex: sequenceIndex
    });

    // Emit event for indexers and rollup accumulator
    emit ReceiptMinted(_eventHash, _merchantId, sequenceIndex, _eventTimestamp);
}
```

**Access control:** `onlyAuthorizedNode` restricts minting to the TSP pipeline nodes. No merchant or external party can mint directly. The subnet's PoA validator set enforces this at the consensus level.

### 1.2 Data Model: On-Chain vs. Off-Chain

The CRDM defines 7 canonical data sources with 107+ fields. The on-chain receipt stores ONLY the cryptographic commitment — never raw data.

| Layer | What goes there | Why |
|---|---|---|
| **On-chain (Avalanche)** | `eventHash` (SHA-256 of full payload), `merchantId` (hashed), `eventTimestamp`, `eventType` enum, `previousHash` (chain link), `sequenceIndex` | Immutable proof of existence. Minimal footprint. No PII ever. |
| **Off-chain (PostgreSQL / Sub 1)** | Full CRDM payload: transaction details, tenders, line items, employee data, location data, cash drawer events, timecards | Application logic, Chirp detection, dashboards. Protected by RLS + encryption at rest. |
| **Off-chain (Merkle tree / Sub 3)** | Leaf hashes, tree structure, proof paths | Verification infrastructure. Feeds both Avalanche minting and Bitcoin anchoring. |

**PII boundary rule:** The `merchantId` stored on-chain is a one-way hash of the Square merchant ID, not the plaintext. No field in the on-chain receipt can be reversed to identify a person, business, or location without access to the off-chain mapping table (which lives in `canary_app` behind RLS).

### 1.3 Event Types: Square Webhook → Mint Triggers

Every Square webhook event that currently triggers the TSP pipeline (TSP-01 receipt → TSP-02 fan-out) also triggers an Avalanche mint. The event type enum maps directly to the CRDM source taxonomy:

| Event Type | Enum | Square Webhook | CRDM Source |
|---|---|---|---|
| `PAYMENT` | 1 | `payment.completed` | C-100 series |
| `REFUND` | 2 | `refund.created`, `refund.updated` | C-200 series |
| `CASH_DRAWER` | 3 | `cash_drawer.shift.ended` | C-300 series |
| `TIMECARD` | 4 | Polled (B-047: Labor API is poll-only) | C-301 series |
| `INVENTORY` | 5 | `inventory.count.updated` | C-400 series |
| `GIFT_CARD` | 6 | `gift_card.activity` | C-500 series |
| `LOYALTY` | 7 | `loyalty.event.created` | C-600 series |
| `ORDER` | 8 | `order.fulfillment.updated` | C-700 series |

### 1.4 Gas Economics on Private Subnet

On a GrowDirect-operated private Avalanche subnet with PoA consensus:

- **Validator count:** Minimum 1 (GrowDirect is sole validator in Phase 1). Recommended 3 for fault tolerance in Phase 2+ (GrowDirect + 2 trusted nodes).
- **Gas price:** Configurable to zero or near-zero. Avalanche Subnet-EVM allows custom `feeConfig` via genesis or dynamic upgrade. On a private subnet where GrowDirect is the sole validator, gas is effectively an internal accounting unit — not a real cost.
- **Throughput:** Single-tenant subnet with dedicated validators. No competition for block space. Estimated capacity: 1,000+ TPS (far exceeding any retail POS volume — PhD's model peaks at 4,167 events/hour for 1,000 merchants at busy-hour spike).
- **Block time:** Avalanche subnets achieve sub-second finality. A receipt mint confirms in <1 second vs. ~10 minutes for Bitcoin.
- **Storage cost:** On-chain receipt is ~160 bytes. At 1,000 merchants × 100 events/day = 100,000 receipts/day = ~16 MB/day = ~5.8 GB/year. Manageable for a dedicated validator node.

**Net cost per receipt on private subnet: effectively zero** (infrastructure cost only — the validator hardware/cloud instance). PhD's model estimates this at ~$0.0015 per receipt amortized across Avalanche infrastructure costs.

### 1.5 Subnet Configuration

| Parameter | Phase 1 (GrowDirect Lab) | Phase 2 (Production) |
|---|---|---|
| Consensus | PoA (Proof of Authority) | PoA (permissioned) |
| Validators | 1 (GrowDirect node) | 3 (GrowDirect + 2 trusted partners) |
| VM | Subnet-EVM (EVM-compatible) | Subnet-EVM or custom VM |
| Gas price | 0 (free minting) | 0 or nominal (internal accounting) |
| Block gas limit | 8M (default) — adjustable upward | Dynamic per ACP-224 |
| Staking | Minimum AVAX stake on P-Chain | Same |
| Data visibility | Private (validators only) | Private (permissioned read access) |

---

## 2. Rollup/Anchoring Layer (Bitcoin Ordinals)

### 2.1 Merkle Tree Construction

The rollup layer aggregates N Avalanche subnet receipts into a single Merkle root, then inscribes that root as a Bitcoin Ordinal. This is an extension of the existing TSP-05 Merkle batcher — not a replacement.

**Batch accumulation flow:**

```
Avalanche ReceiptMinted events (continuous)
    ↓
RollupAccumulator (smart contract on Avalanche OR off-chain service)
    ↓
Collects eventHashes into ordered list
    ↓
When trigger fires (time-based, count-based, or manual):
    ↓
Compute Merkle root over all accumulated hashes
    ↓
Emit RollupReady event with: root, leafCount, startSequence, endSequence
    ↓
TSP-05 picks up → inscribes root as Bitcoin Ordinal via OrdinalsBot API
```

**Tree construction algorithm:** Identical to TSP-05 v1.2 specification. Binary Merkle tree, SHA-256 at each node, leaves sorted by `eventHash` for deterministic ordering. Odd leaf count handled by duplicating the last leaf.

### 2.2 Rollup Frequency Options

Per Jeffe Directive 1, inscription frequency is a **smart contract parameter** configurable per merchant:

| Frequency Tier | Trigger Condition | Typical Use Case | PhD Pricing Tier |
|---|---|---|---|
| Tier 1: Per-event | Every receipt mints an individual Ordinal | High-security, low-volume | $79/mo |
| Tier 2: Hourly | Time-based: every 60 minutes | Standard retail | $39/mo |
| Tier 3: Daily | Time-based: every 24 hours | Cost-conscious SMB | $19/mo |
| Tier 4: Count-based | Every N events (configurable: 100, 500, 1000) | Variable volume | Custom |
| Tier 5: Manual | Merchant or admin triggers inscription | Audit/compliance on-demand | Base tier |

**Smart contract interface for frequency parameter:**

```solidity
// InscriptionGovernor.sol

enum FrequencyType { PER_EVENT, TIME_BASED, COUNT_BASED, MANUAL }

struct InscriptionPolicy {
    FrequencyType freqType;
    uint64 intervalSeconds;   // For TIME_BASED: seconds between inscriptions
    uint32 eventThreshold;    // For COUNT_BASED: N events before trigger
    bool   active;
}

event PolicyUpdated(bytes32 indexed merchantId, FrequencyType freqType, uint64 interval, uint32 threshold);
event InscriptionTriggered(bytes32 indexed merchantId, bytes32 merkleRoot, uint32 leafCount, uint64 timestamp);

function setInscriptionPolicy(
    bytes32 _merchantId,
    FrequencyType _freqType,
    uint64 _intervalSeconds,
    uint32 _eventThreshold
) external onlyAdmin {
    policies[_merchantId] = InscriptionPolicy({
        freqType: _freqType,
        intervalSeconds: _intervalSeconds,
        eventThreshold: _eventThreshold,
        active: true
    });
    emit PolicyUpdated(_merchantId, _freqType, _intervalSeconds, _eventThreshold);
}

function checkAndTrigger(bytes32 _merchantId) external {
    InscriptionPolicy memory policy = policies[_merchantId];
    require(policy.active, "Policy not active");

    if (policy.freqType == FrequencyType.TIME_BASED) {
        require(block.timestamp >= lastInscription[_merchantId] + policy.intervalSeconds, "Too early");
    } else if (policy.freqType == FrequencyType.COUNT_BASED) {
        require(pendingCount[_merchantId] >= policy.eventThreshold, "Below threshold");
    } else if (policy.freqType == FrequencyType.MANUAL) {
        // Manual trigger — always allowed when called by admin
    }
    // PER_EVENT triggers inline at mint time, not here

    bytes32 root = computeMerkleRoot(_merchantId);
    emit InscriptionTriggered(_merchantId, root, pendingCount[_merchantId], block.timestamp);

    // Reset accumulator
    pendingCount[_merchantId] = 0;
    lastInscription[_merchantId] = block.timestamp;
}
```

### 2.3 Inscription Payload

The Bitcoin Ordinal inscription contains ONLY the Merkle root plus minimal metadata. Raw receipt data NEVER touches Bitcoin.

**Inscription data format (per Jeffe Directive 3 — stacked on single sat):**

```json
{
    "header": {
        "version": 1,
        "sequenceIndex": 42,
        "timestamp": 1709337600,
        "chainSource": "avalanche:subnet-growdirect",
        "chainAnchor": "bitcoin:ordinals"
    },
    "body": {
        "merkleRoot": "a1b2c3d4...64hex",
        "leafCount": 1000,
        "startSequence": 41001,
        "endSequence": 42000,
        "hashAlgorithm": "SHA-256",
        "treeType": "binary-merkle"
    },
    "verification": {
        "avaxBlockHash": "0xabc...def",
        "avaxBlockNumber": 123456,
        "rollupContractAddress": "0x..."
    }
}
```

**Size:** ~450 bytes per inscription. At daily frequency (Tier 3), this is ~164 KB/year per merchant — well within Ordinal inscription limits.

### 2.4 Verification Path

A merchant proving their receipt exists in a Bitcoin-anchored batch:

```
1. Merchant provides: eventHash + approximate timestamp
2. System looks up: which Merkle batch contains this eventHash
   → Queries Avalanche subnet event logs OR PostgreSQL index
3. System retrieves: Merkle proof (sibling hashes from leaf to root)
4. System retrieves: Bitcoin Ordinal inscription containing the root
   → Looks up the merchant's designated satoshi
   → Finds the inscription at the correct sequenceIndex
5. Verification:
   a. Recompute root from eventHash + proof path
   b. Compare computed root to inscribed root
   c. Confirm inscription exists on Bitcoin (independent verification via any Ordinals indexer)
6. Result: cryptographic proof that this specific POS event was sealed
   at a specific time and anchored to Bitcoin block N
```

This is the bilateral verification flow from TSP-08, extended with the Avalanche intermediate layer as an additional verification point.

---

## 3. Smart Contract Specification (Conceptual)

### 3.1 Contract Architecture

Three contracts deployed on the Avalanche subnet:

| Contract | Purpose | Mutability |
|---|---|---|
| **ReceiptMinter** | Mint receipt records from POS events | Immutable (no proxy) |
| **InscriptionGovernor** | Manage inscription frequency policies and trigger rollups | Upgradeable (admin-controlled — GrowDirect only) |
| **MerkleVerifier** | Verify Merkle proofs and receipt existence | Immutable (trust model requires deterministic verification) |

**Upgrade pattern decision:** ReceiptMinter and MerkleVerifier are **immutable** (no proxy pattern). Once deployed, the verification logic cannot change — this is essential for the trust model. If a merchant or law enforcement needs to verify a receipt from 5 years ago, the verification contract must produce the same result as the day it was sealed. InscriptionGovernor is upgradeable because business logic (pricing tiers, frequency options) will evolve.

### 3.2 MerkleVerifier Contract

```solidity
// MerkleVerifier.sol — immutable, deployed once

function verifyReceipt(
    bytes32 _eventHash,
    bytes32[] calldata _proof,
    uint256 _leafIndex,
    bytes32 _expectedRoot
) external pure returns (bool) {
    bytes32 computedHash = _eventHash;
    for (uint256 i = 0; i < _proof.length; i++) {
        if (_leafIndex % 2 == 0) {
            computedHash = sha256(abi.encodePacked(computedHash, _proof[i]));
        } else {
            computedHash = sha256(abi.encodePacked(_proof[i], computedHash));
        }
        _leafIndex /= 2;
    }
    return computedHash == _expectedRoot;
}

function verifyReceiptWithBitcoinAnchor(
    bytes32 _eventHash,
    bytes32[] calldata _proof,
    uint256 _leafIndex,
    bytes32 _expectedRoot,
    bytes32 _inscriptionId
) external view returns (bool verified, bytes32 bitcoinAnchor) {
    bool merkleValid = this.verifyReceipt(_eventHash, _proof, _leafIndex, _expectedRoot);
    // _inscriptionId is stored in the rollup log — cross-reference
    bitcoinAnchor = inscriptionAnchors[_expectedRoot];
    return (merkleValid && bitcoinAnchor == _inscriptionId, bitcoinAnchor);
}
```

### 3.3 Rollup Accumulator

The rollup accumulator can live on-chain (Avalanche smart contract) or off-chain (TSP-05 service). Recommendation: **on-chain accumulator** for auditability, with off-chain fallback for performance at scale.

On-chain accumulator: every `ReceiptMinted` event appends the `eventHash` to a per-merchant list. When `InscriptionGovernor.checkAndTrigger()` fires, the accumulator computes the Merkle root over the pending list and emits `InscriptionTriggered`. TSP-05 listens for this event and submits to OrdinalsBot.

---

## 4. TSP Pipeline Impact

### 4.1 Component-by-Component Assessment

| TSP Component | Change Required | Description |
|---|---|---|
| **TSP-01 (Webhook Receipt)** | NONE | Unchanged. Square webhook → Valkey queue. Avalanche is downstream. |
| **TSP-02 (Queue Fan-Out)** | MINOR | Add Avalanche subscriber to fan-out targets. One additional Valkey stream consumer. |
| **TSP-03 (Sub 1: Hash & Seal)** | NONE | Unchanged. PostgreSQL seal is independent of chain minting. |
| **TSP-04 (Sub 2: Parse & Route)** | NONE | Unchanged. Chirp detection operates on parsed data, not chain state. |
| **TSP-05 (Sub 3: Merkle & Ordinal)** | MODERATE | Gains chain-agnostic adapter. Merkle tree construction unchanged. Inscription target becomes pluggable (Bitcoin direct OR Avalanche-first-then-Bitcoin-rollup). |
| **TSP-06 (Detection Engine)** | NONE | Unchanged. Chirp rules operate on Sub 2 parsed data. |
| **TSP-07 (L402 Validation API)** | MODERATE | Verification endpoint gains Avalanche proof path in addition to Bitcoin proof. L402 macaroon caveats may include chain source. |
| **TSP-08 (Bilateral Verification)** | MODERATE | Verification procedure gains step 2.5: check Avalanche subnet receipt before Bitcoin anchor. Two-layer verification strengthens evidentiary chain. |
| **TSP-09 (Replay & Rebuild)** | MINOR | Replay source can include Avalanche subnet event logs as an additional recovery vector. |

### 4.2 Triple-Subscriber Model: Does It Become Quad?

**No.** The triple-subscriber model remains intact. The Avalanche minting layer is an **enhancement to Sub 3**, not a fourth subscriber. Sub 3's responsibility expands from "compute Merkle tree and inscribe on Bitcoin" to "compute Merkle tree, optionally mint on Avalanche, and inscribe Merkle root on Bitcoin."

The fan-out from TSP-02 still produces exactly three streams: Sub 1 (seal), Sub 2 (parse), Sub 3 (mint + inscribe). Sub 3 internally routes to the appropriate chain target(s) based on the merchant's `InscriptionPolicy`.

### 4.3 New Component: Avalanche Gateway Service

One new service sits between TSP-02 fan-out and the Avalanche subnet:

```
TSP-02 Fan-Out
    ↓ (Valkey Stream: stream:sub3)
Sub 3 Service
    ↓
ChainAdapter.mint(eventHash, merchantId, ...)
    ↓ (dispatches to configured chain)
    ├── AvalancheAdapter → ReceiptMinter contract → ReceiptMinted event
    ├── BitcoinAdapter → OrdinalsBot API → Inscription ID
    └── (future adapters)
```

The Avalanche Gateway is a lightweight RPC client that submits transactions to the subnet. In Kubernetes, it runs as a sidecar to the Sub 3 pod or as an independent deployment behind the ChainAdapter interface.

---

## 5. Chain-Agnostic Abstraction

### 5.1 Adapter Interface

Per Jeffe Directive 2, the chain is a configuration parameter. The abstraction layer:

```typescript
// chain-adapter.ts — TypeScript interface definition

interface ChainTarget {
    chainId: string;              // e.g. "bitcoin:ordinals", "avalanche:subnet-gd", "base:l2"
    name: string;                 // Human-readable: "Bitcoin Ordinals", "GrowDirect Subnet"
    type: "l1" | "l2" | "subnet" | "sidechain";
    capabilities: ChainCapability[];
}

enum ChainCapability {
    REAL_TIME_RECEIPT = "real_time_receipt",    // Sub-second confirmation
    PERMANENT_ANCHOR = "permanent_anchor",      // Immutable, censorship-resistant
    SMART_CONTRACT = "smart_contract",          // Programmable logic
    NATIVE_VERIFICATION = "native_verification" // On-chain proof verification
}

interface ChainAdapter {
    // Core operations
    mintReceipt(receipt: ReceiptPayload): Promise<MintResult>;
    inscribeMerkleRoot(root: MerkleRootPayload): Promise<InscriptionResult>;
    verifyReceipt(proof: VerificationRequest): Promise<VerificationResult>;

    // Configuration
    getCapabilities(): ChainCapability[];
    getChainTarget(): ChainTarget;
    estimateCost(operation: OperationType): Promise<CostEstimate>;

    // Health
    isHealthy(): Promise<boolean>;
    getLatency(): Promise<number>;  // ms
}

interface ReceiptPayload {
    eventHash: string;          // hex-encoded SHA-256
    merchantId: string;         // hashed merchant identifier
    eventTimestamp: number;     // Unix epoch
    eventType: number;          // Enum value
    previousHash: string;       // Chain link
    sequenceIndex: number;      // Per-merchant monotonic counter
}

interface MintResult {
    success: boolean;
    chainId: string;
    transactionHash: string;    // Chain-specific tx identifier
    blockNumber?: number;
    confirmationTime: number;   // ms to confirmation
    cost: CostEstimate;
}

interface MerkleRootPayload {
    root: string;               // hex-encoded Merkle root
    leafCount: number;
    startSequence: number;
    endSequence: number;
    sourceChain?: string;       // If rollup from another chain
    sequenceIndex: number;      // For stacked inscriptions (Directive 3)
    targetSatoshi?: string;     // For Bitcoin: specific sat ordinal number
}
```

### 5.2 Registration Pattern for New Chains

```typescript
// chain-registry.ts

class ChainRegistry {
    private adapters: Map<string, ChainAdapter> = new Map();

    register(chainId: string, adapter: ChainAdapter): void {
        // Validate adapter implements required interface
        const caps = adapter.getCapabilities();
        if (caps.length === 0) throw new Error("Adapter must declare capabilities");
        this.adapters.set(chainId, adapter);
    }

    getAdapter(chainId: string): ChainAdapter {
        const adapter = this.adapters.get(chainId);
        if (!adapter) throw new Error(`No adapter registered for chain: ${chainId}`);
        return adapter;
    }

    getAdaptersByCapability(cap: ChainCapability): ChainAdapter[] {
        return Array.from(this.adapters.values())
            .filter(a => a.getCapabilities().includes(cap));
    }
}

// Merchant configuration: which chains to target
interface MerchantChainConfig {
    merchantId: string;
    primaryChain: string;       // Real-time receipts go here
    anchorChain: string;        // Merkle roots inscribed here
    rollupPolicy: InscriptionPolicy;
    targetSatoshi?: string;     // For Bitcoin stacked inscriptions
}
```

### 5.3 What Is Chain-Specific vs. Chain-Agnostic

| Component | Chain-Agnostic | Chain-Specific |
|---|---|---|
| Receipt hashing (SHA-256) | YES | — |
| Merkle tree construction | YES | — |
| Inscription frequency policy | YES | — |
| Verification algorithm (Merkle proof) | YES | — |
| L402 macaroon structure | YES | — |
| Transaction submission | — | YES (each chain has its own RPC/API) |
| Gas/fee estimation | — | YES (Avalanche gas vs. Bitcoin sats) |
| Confirmation model | — | YES (sub-second vs. ~10 min) |
| Smart contract deployment | — | YES (EVM vs. non-EVM) |
| Inscription format | — | YES (Ordinal envelope vs. EVM event log) |
| Block explorer verification | — | YES (Ordinals indexer vs. Snowtrace) |

---

## 6. Stacked Inscriptions on a Single Satoshi (Directive 3)

### 6.1 Protocol Support

**Confirmed:** The Ordinals protocol (BIP envelope, OP_FALSE OP_IF) supports multiple inscriptions on the same satoshi. Each inscription receives a unique inscription number and ID. Earlier inscriptions are NOT overwritten — they persist permanently. This is not "reinscription" (which implies replacement) but rather "stacked inscription" (append-only).

**How it works technically:**
- Each inscription is a separate Bitcoin transaction that moves the target satoshi
- The sat accumulates inscriptions over its lifetime
- Inscription order is determined by the block height and transaction index of each inscribing transaction
- Any Ordinals indexer can enumerate all inscriptions on a given sat

### 6.2 Inscription Data Format (Stacked Model)

Each inscription appended to the merchant's designated satoshi follows this schema:

```json
{
    "protocol": "glog-v1",
    "header": {
        "sequenceIndex": 0,
        "timestamp": 1709337600,
        "previousInscriptionId": null,
        "chainSources": ["avalanche:subnet-gd"],
        "chainAnchor": "bitcoin:ordinals"
    },
    "body": {
        "merkleRoot": "a1b2c3d4e5f6...64hex",
        "leafCount": 1000,
        "startSequence": 0,
        "endSequence": 999,
        "hashAlgorithm": "SHA-256",
        "treeType": "binary-merkle"
    }
}
```

For subsequent inscriptions on the same sat:

```json
{
    "protocol": "glog-v1",
    "header": {
        "sequenceIndex": 1,
        "timestamp": 1709424000,
        "previousInscriptionId": "abc123...inscription_id_0",
        "chainSources": ["avalanche:subnet-gd"],
        "chainAnchor": "bitcoin:ordinals"
    },
    "body": {
        "merkleRoot": "f6e5d4c3b2a1...64hex",
        "leafCount": 1200,
        "startSequence": 1000,
        "endSequence": 2199,
        "hashAlgorithm": "SHA-256",
        "treeType": "binary-merkle"
    }
}
```

### 6.3 Serialization and Verification

**Serialization:** The `sequenceIndex` field provides total ordering. `previousInscriptionId` creates an explicit chain link (in addition to the implicit ordering from the Ordinals protocol). This dual-link (protocol-native ordering + application-level chaining) provides defense-in-depth against indexer discrepancies.

**Verification algorithm:**

```
Given: satoshi ordinal number S, target sequence index N
1. Query Ordinals indexer: get all inscriptions on sat S
2. Sort by inscription number (protocol ordering)
3. Locate inscription at position N in sorted list
4. Parse inscription content → extract merkleRoot
5. Given target eventHash + Merkle proof:
   a. Recompute root from proof path
   b. Compare to extracted merkleRoot
6. Verify chain integrity:
   a. Check previousInscriptionId matches inscription at N-1
   b. Check sequenceIndex == N
   c. Check timestamp is monotonically increasing
7. Return: VERIFIED or FAILED (with specific failure reason)
```

### 6.4 Business Transfer (Sat Transfer = gLog Transfer)

When a business is sold, the designated satoshi is transferred to the new owner. The entire inscription history (every Merkle root, every sequence entry) transfers with it. The new owner inherits the complete, verifiable transaction history.

**Transfer mechanics:**
- Standard Bitcoin transaction: current owner sends the specific sat to new owner's address
- All stacked inscriptions travel with the sat (this is inherent to the Ordinals protocol)
- The new owner can continue appending inscriptions (new sequence indices)
- No data migration, no API calls, no database export — the chain IS the history

### 6.5 Patent Implications — Route to Syd

**Novel claim identified:** Stacked Merkle roots on a single satoshi as a transferable business identity. Specifically:

1. **Append-only ledger on a single token:** Using a designated Bitcoin satoshi as an infinite-capacity, sequenced append-only log where each entry is a Merkle root covering N business events. No prior art in the Ordinals ecosystem for this specific pattern (business event notarization via stacked inscription).

2. **Business identity as satoshi ownership:** The satoshi ordinal number becomes a permanent, transferable business address. Business sale = sat transfer = complete history transfer. This is distinct from NFT-based identity systems because it carries cryptographic proof of all historical business events, not just metadata.

3. **Dual-chain verification path:** The combination of real-time Avalanche subnet receipt + periodic Bitcoin Ordinal anchor creates a two-layer verification model where the Avalanche layer provides speed and the Bitcoin layer provides permanence. Each layer independently verifiable.

**Recommendation:** These claims strengthen the provisional (63/991,596). Syd should evaluate as dependent claims in the utility filing. The stacked inscription pattern in particular appears to have no direct prior art — PhD should validate this assessment.

---

## 7. Key Findings and Recommendations

### 7.1 Feasibility: GREEN

The hybrid architecture is technically feasible with no architectural blockers. The existing TSP pipeline accommodates it with moderate modifications (TSP-02 fan-out, TSP-05 chain adapter, TSP-07/TSP-08 verification extensions).

### 7.2 Recommended Phasing

| Phase | Scope | Effort | Dependency |
|---|---|---|---|
| **Current (Sprint 6)** | Pure Ordinals via OrdinalsBot + Lightning via Strike | 2 sprints | In progress — do not modify |
| **Phase 2** | Add Avalanche subnet as real-time layer | 3-4 sprints | Subnet deployment, smart contract dev, adapter wiring |
| **Phase 3** | Chain-agnostic abstraction (support any EVM L1) | 1-2 sprints | Phase 2 adapter pattern proven |
| **Phase 4** | Stacked inscriptions on designated sat | 1 sprint | OrdinalsBot API support for targeting specific sats |

### 7.3 PhD to Validate

- Cost model for Avalanche subnet operation (validator node hosting, AVAX staking requirement)
- Break-even merchant count for hybrid vs. pure Ordinals (PhD preliminary: 35 merchants)
- Genesis Pool allocation under stacked inscription model (PhD preliminary: 13+ years viability)

### 7.4 Open Questions for Jeremy

1. Does OrdinalsBot API support inscribing on a specific satoshi (targeting a designated sat for stacked inscriptions)?
2. What is the minimum AVAX stake required for a private subnet validator on mainnet?
3. Can Valkey Streams fan-out handle the additional Avalanche subscriber without backpressure issues?

---

*Condor | March 1, 2026 | B-069 Hybrid Architecture Feasibility Brief v1.0*
*R&D only. Pure Ordinals pipeline unchanged. IP rules enforced throughout.*
*Manifesto: IV.4, V.5*
