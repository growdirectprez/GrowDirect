---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor Research Brief — B-069: Hybrid Chain Architecture (Avalanche Subnet + Bitcoin Ordinals)
**Work Order:** B-069 — Hybrid L1/Bitcoin Architecture Research
**Date:** March 1, 2026
**Dispatched by:** ALX
**Priority:** 🟠 MEDIUM — R&D only. Does NOT change current architecture.
**Session type:** Research Brief (no code, no design changes)

---

## GUARDRAILS — READ FIRST

**THIS IS R&D ONLY.**
- The current elJeffe architecture (pure Bitcoin Ordinals via OrdinalsBot + Lightning via Strike) is the production design.
- This research does NOT propose changes to the current design.
- This research does NOT gate any Sprint 6 work.
- Output is a research brief for Jeffe's strategic decision-making. Nothing more.
- **IP RULES APPLY:** This is maximum confidential. No external references to GrowDirect, Canary, or elJeffe in the output. Frame as a generic "retail POS notarization system" if needed for abstraction.

---

## Context

Jeffe is exploring whether a **private Avalanche subnet** could serve as the real-time receipt minting layer for elJeffe, with Bitcoin Ordinals as the permanent anchor. The thesis: merchant POS events mint as smart contract receipts on a GrowDirect-operated Avalanche subnet (sub-second, near-zero cost), then batch Merkle roots are periodically inscribed as Bitcoin Ordinals (permanent, immutable).

**Key design points from Jeffe:**
1. **GrowDirect as subnet validator** — own the chain, not just the app. Private subnet = permissioned validators, custom gas economics, merchant data isolation at the chain level.
2. **Smart contract governance** — the entire receipt → seal → inscribe flow governed by on-chain logic, not just application code. Auditable, deterministic, tamper-proof.
3. **Chain-agnostic model** — Avalanche is the reference implementation (preferred for Wyoming alignment, private subnets, AVAX holdings), but the architecture should work with any EVM-compatible L1.
4. **Wyoming regulatory alignment** — Avalanche (Ava Labs) is a Wyoming-incorporated entity. GrowDirect is targeting Wyoming formation (B-004/Syd). Regulatory harmony matters.

---

## Condor Deliverables

### Deliverable 1: Architecture Feasibility Brief
`_ALX/WorkOrders/output/Condor/Condor_B069_HybridArchitecture_v1.0.md`

Map how a hybrid Avalanche subnet + Bitcoin Ordinals architecture fits into the existing elJeffe six-node schematic. Address each component:

**1. Receipt Minting Layer (Avalanche Subnet)**
- Smart contract design: what does a "receipt mint" transaction look like on-chain?
- Data model: which CRDM fields go on-chain vs. off-chain (PII NEVER on-chain)
- Event types: which Square webhook events trigger a mint?
- Gas economics on a private subnet: can gas be set to zero or near-zero if GrowDirect is sole validator?
- Subnet configuration: validator count (minimum 1 for private), staking requirement, custom VM options

**2. Rollup/Anchoring Layer (Bitcoin Ordinals)**
- Merkle tree construction: batch N Avalanche receipts → compute root → inscribe one Ordinal
- Rollup frequency options: time-based (every hour), count-based (every N receipts), hybrid
- Inscription payload: what goes in the Ordinal? (Merkle root + metadata, NOT raw receipt data)
- Verification path: how does a merchant prove their receipt is in a specific Bitcoin-anchored batch?

**3. Smart Contract Specification (Conceptual)**
- Receipt mint contract: struct definition, event emission, access control
- Rollup contract: batch accumulator, Merkle root computation, Bitcoin anchor reference
- Verification contract: Merkle proof verification, receipt lookup by hash
- Upgrade pattern: proxy or immutable? (immutable preferred for trust model)

**4. TSP Pipeline Impact**
- What changes in the current TSP-01 through TSP-09 pipeline if receipts mint to Avalanche first?
- Which TSP components stay identical? Which need a new "Avalanche subscriber"?
- Does the triple-subscriber model (PostgreSQL + Merkle + Receipt) become a quad-subscriber?

**5. Chain-Agnostic Abstraction**
- Define an interface/adapter pattern so the receipt minting layer is swappable (Avalanche today, Base/Arbitrum/Solana tomorrow)
- What is chain-specific vs. chain-agnostic in the design?

### Deliverable 2: Comparison Matrix
`_ALX/WorkOrders/output/Condor/Condor_B069_ChainComparison_v1.0.md`

One-page comparison table:

| Dimension | Pure Ordinals (Current) | Hybrid: Avalanche + Ordinals | Hybrid: Lightning + Ordinals |
|---|---|---|---|
| Real-time confirmation | | | |
| Cost per receipt | | | |
| Data isolation | | | |
| Smart contract capability | | | |
| Validator control | | | |
| Wyoming regulatory fit | | | |
| Patent claim strength | | | |
| Implementation complexity | | | |
| Chain dependency risk | | | |
| Merchant UX (speed to "sealed") | | | |

---

## JEFFE DESIGN DIRECTIVES (March 1, 2026) — Incorporate into architecture

**Directive 1: User-Defined Inscription Frequency (Smart Contract Parameter)**
The smart contract governing each merchant's elJeffe instance exposes an inscription frequency parameter. Options include: every transaction, every N events, every N time units, or manual trigger. The Merkle tree seals every event in real time regardless — the inscription frequency only controls when the accumulated root gets committed to a destination chain. **Condor must specify:** the smart contract interface for this parameter (setter, getter, event emission on trigger), the rollup accumulator pattern, and how the TSP pipeline interacts with this trigger (TSP-05 Merkle logic adapts to variable batch size).

**Directive 2: Chain-Agnostic Destination (Chain as Parameter)**
The user selects their destination chain(s) for inscription: Bitcoin Ordinals, Avalanche, both, or any future supported L1. elJeffe is the notarization API — the chain is a configuration parameter, not an architectural constraint. **Condor must specify:** the adapter/plugin interface for chain targets, the registration pattern for new chains, and how the TSP-07/TSP-08 inscription and receipt stages become chain-polymorphic. Include a minimal interface definition (TypeScript or Solidity pseudocode).

**Directive 3: Stacked Inscriptions on a Single Satoshi**
Instead of consuming a new satoshi per inscription, the architecture supports **appending serialized Merkle roots to the same satoshi** — creating an infinite-capacity, append-only ledger on one token. The satoshi becomes the merchant's permanent gLog address. Serialization: each inscription is sequenced (index 0, 1, 2, ...) and the sequence order IS the timeline. The owning satoshi is transferable: business sale = sat transfer = full gLog history transfer. **Condor must specify:** the inscription data format (header: sequence index, timestamp, chain references; body: Merkle root + metadata), the serialization schema, and the verification algorithm (given sat + sequence index → retrieve specific Merkle root → verify any leaf via proof path). Research question for Condor: does the current Ordinals protocol (BIP envelope, OP_FALSE OP_IF) support multiple inscriptions on the same sat? If not, what is the closest achievable pattern?

---

## Reference Materials

- Six-Node Patent Schematic: `_ALX/WorkOrders/output/PhD/`
- TSP PRDs (all 10): `_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/`
- TSP Consolidated Review: `_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md`
- CRDM v1.0: `Canary_IP/Markdown/Specs/CRDM_v1.0.md`
- ElJeffe Business Model Addendum: `_ALX/ElJeffe_BusinessModel_Addendum.md`
- B-041 Sub 3 Ordinal Minter Assessment: `_ALX/WorkOrders/output/Jeremy/`
- Source PDF: `_ALX/WorkOrders/input/B069_HybridChain_SourceConversation.pdf`

---

## PhD Supervision Note

PhD is running a **parallel economics brief** on B-069. Condor's architecture brief should be self-contained — do not wait for PhD. If architectural choices have cost implications, note them as "PhD to validate" and move on.

---

## Session Close

Update HANDOFF.md Condor section with:
- B-069 Architecture Brief: DELIVERED or BLOCKED (with reason)
- Key finding: one-sentence summary of feasibility assessment
- Flag any patent implications for Syd
- Flag any smart contract patterns that strengthen the provisional (63/991,596)

Log timelog per TRIAGE Step 0.

---

*ALX | March 1, 2026 | B-069 Condor — Hybrid Chain Architecture Research*
*R&D only. Pure play unchanged. IP rules enforced.*
