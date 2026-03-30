---
type: research
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Universal Event Notarization on the Bitcoin Time Chain
## Architecture, Economics, and Governance of the elJeffe Protocol

**Draft:** Sections 0–4
**Author:** PhD (Research Framework), on behalf of GrowDirect
**Date:** March 1, 2026
**Classification:** MAXIMUM CONFIDENTIAL — Internal Draft
**Status:** DRAFT — Syd review required before any external distribution
**Section 11 (Patent Claims and IP Position): BLOCKED until Syd defines disclosure boundaries**
**Target Length:** Sections 0–4 ≈ 4,400 words (this draft: ~4,500 words)

---

## Section 0 — Abstract

The retail industry generates over $5 trillion in annual transaction volume across millions of merchant locations, yet every transaction record resides on mutable infrastructure controlled by third parties. When disputes arise — chargebacks, audits, insurance claims, regulatory inquiries — the merchant's evidence rests on the same mutable foundation as the counterparty's. The record can be argued with. This paper presents a position on Receipt-as-a-Service (RaaS): a Bitcoin-native protocol for universal event notarization that transforms arbitrary webhook-originated events into permanent, independently verifiable records on the Bitcoin time chain, and exposes that verification capability as a universal API endpoint accessible to any point-of-sale system on earth.

We describe elJeffe, the protocol that implements RaaS through a six-node architecture and Triple Subscriber Pipeline (TSP) processing events in milliseconds while batching cryptographic proofs for periodic Ordinal inscription. We present a seven-layer economic model where validation revenue from past inscriptions funds future inscriptions, achieving protocol self-sufficiency at approximately 17 merchants — a convergence point confirmed independently across three economic models measuring Genesis Pool viability, marginal revenue economics, and permanent historical validation yield. We detail a hybrid chain architecture combining Avalanche sub-second execution with Bitcoin permanent settlement, wherein the Avalanche sidechain provides the real-time receipt layer that merchants require while Bitcoin provides the proof-of-work permanence that auditors demand. We present a Metcalfe's Law valuation model demonstrating that the Genesis Pool — the protocol's founding inscription endowment — compounds as a network asset whose value grows quadratically with merchant adoption, exceeding its static Bitcoin valuation by 69x at 350 merchants.

The protocol's time-dependent moat — inscription at historically low Bitcoin fees during a window that three independent escalation drivers are closing — creates a thermodynamic advantage that cannot be replicated after the window closes. The entity that controls the first canonical inscription pool on the Bitcoin time chain, inscribed during this window, and gates validation via micropayment, holds a permanent economic position that compounds with every merchant event.

RaaS is the thesis. The architecture is the proof.

**Keywords:** Bitcoin, Ordinals, event notarization, receipt verification, L402, micropayments, loss prevention, schema-agnostic, Receipt-as-a-Service

---

## Section 1 — Introduction: The Mutable Record Problem

### 1.1 The Persistence of Mutable Records

For forty years, the retail industry has operated on a fundamental architectural contradiction. The records that adjudicate disputes between merchants, customers, payment processors, insurers, and regulators are stored on infrastructure that any party with administrative access can modify. The IBM 4690 operating system introduced the transaction log (tLog) in the 1980s as a sequential journal of point-of-sale events. It became the canonical record for loss prevention investigations, cash reconciliation, employee performance reviews, and regulatory audits across the global retail industry. It had one flaw that IBM understood and could not solve within the architecture of the era: it was a mutable file on a server controlled by the institution that generated it.

Every loss prevention system built on top of the tLog — and every system built after it — inherited this limitation. Square's transaction logs reside on Square's servers. Clover's on Clover's. Toast's on Toast's. The merchant sees a dashboard. The dashboard shows what the server says. The server is controlled by someone who is not the merchant. The mutable record persists as the foundation of the entire retail data industry, not because the problem is unrecognized, but because until 2009 no technical primitive existed that could solve it at the foundation layer.

### 1.2 The Cost of Mutability

The economic consequences of mutable records are not theoretical. They manifest in three categories that collectively represent the largest unaddressed cost center in retail operations.

First, chargeback fraud. The global cost of chargebacks exceeded $117 billion in 2023 (Chargebacks911, 2024). The merchant's defense in a chargeback dispute is a transaction record. That record lives on a server the merchant does not control. The payment processor adjudicates the dispute by comparing the merchant's record (mutable, on the processor's infrastructure) against the customer's claim. The asymmetry is structural: the entity adjudicating the dispute controls the evidence. Merchants lose approximately 60% of chargeback disputes they contest, not because the transactions did not occur, but because they cannot produce evidence with independent verifiability.

Second, internal loss. The National Retail Federation estimates $112.1 billion in retail shrink for 2023, of which employee theft accounts for approximately 29%. Loss prevention investigations depend on transaction logs to establish patterns — missing voids, excessive discounts, suspicious refund sequences. When the transaction log itself can be modified, edited, or selectively deleted, the evidentiary chain breaks. An employee accused of theft based on tLog analysis has no independent record to refute the accusation. The institution that generates the accusation controls the evidence. This is not a hypothetical failure mode — it is the daily reality of every loss prevention department in retail.

Third, regulatory and audit exposure. Tax authorities, financial regulators, insurance adjusters, and legal proceedings all depend on transaction records as evidence. Every one of these use cases assumes the record is a faithful representation of what occurred. None of them can independently verify that assumption. The record is accepted on trust. Trust in the institution. Trust in the server. Trust in the administrator who has write access to the database. This trust model has persisted for four decades because no alternative existed.

### 1.3 Bitcoin as the Missing Primitive

Bitcoin's proof-of-work consensus mechanism, operational since January 3, 2009, solved the mutable record problem for financial transactions. The same mechanism — cryptographic hashing, append-only chain, no administrative override — solves it for arbitrary events. The Bitcoin time chain is a neutral, permanently accessible, independently auditable record that no single party controls.

The Ordinals protocol (Casey Rodarmor, January 2023) extended Bitcoin's data layer by enabling arbitrary data inscription on individual satoshis. For the first time, non-financial data — including cryptographic hashes of business events — could be permanently inscribed on the Bitcoin base layer with the same security guarantees as Bitcoin transactions themselves.

This paper presents elJeffe, a protocol that combines these primitives into a complete event notarization system: webhook-originated events are received, hashed, sealed in a legal-evidence store, batched into Merkle trees, and inscribed as Ordinal roots on Bitcoin. The result is a receipt that any party — merchant, auditor, insurer, regulator, court — can independently verify by querying the Bitcoin blockchain, without trusting elJeffe, without trusting the merchant, without trusting anyone. The verification is mathematical.

### 1.4 Receipt-as-a-Service

The architecture described in this paper produces an emergent capability that extends beyond the initial loss prevention application. Because the protocol normalizes any point-of-sale data into canonical schema through a schema-agnostic data model (the Canonical Retail Data Model, or CRDM), the notarization service is not bound to any single POS system. Square, Clover, Toast, Lightspeed, Shopify POS, standalone terminals — any system that generates webhook events can submit them for notarization.

This capability is Receipt-as-a-Service (RaaS): a universal verification endpoint where any POS integrator calls the API, pays a satoshi via Lightning micropayment, and receives a verified receipt backed by Bitcoin proof-of-work. RaaS is not a separate product built on top of the protocol. It is the natural consequence of schema-agnostic design combined with a universal validation gate. The architecture described in Sections 2–4 is the proof that RaaS is technically achievable. The economics described in subsequent sections demonstrate that it is commercially viable. The governance model ensures it scales without centralized control.

Canary LP, GrowDirect's initial product, is the beachhead — proving the protocol on Square merchants in the most webhook-dense vertical in retail POS. elJeffe is the protocol. RaaS is the product every POS integrator buys.

---

## Section 2 — The gLog: From Transaction Log to Time Chain

### 2.1 The tLog Legacy

The transaction log (tLog) was IBM's answer to the question: "How do we record what happened at the register?" It answered the question within the constraints of 1980s computing — a sequential, mutable file on a locally attached server. For its era, it was remarkable. It enabled an entire industry of loss prevention, cash management, and regulatory compliance. But its mutability was not a bug; it was an architectural constraint that could not be overcome with the technology available.

The tLog's descendants — the transaction databases of Square, Clover, Toast, and every modern POS system — inherited the same fundamental limitation. The storage medium changed (local disk to cloud database). The access model changed (physical console to API). The scale changed (single register to millions of merchants). The mutability persisted. Every transaction record in every modern POS system can be modified, deleted, or reinterpreted by the party that controls the database.

### 2.2 The gLog Principle

The gLog (GrowDirect Log) replaces the tLog's mutable foundation with an immutable one. It does not improve the tLog. It replaces the layer on which the tLog sits.

The gLog principle is simple: every event that would have been written to a tLog is instead hashed (SHA-256), sealed in an append-only evidence store with immutability triggers, batched into a Merkle tree with other events, and inscribed on the Bitcoin time chain as an Ordinal. The event still reaches the merchant's dashboard in milliseconds. But the cryptographic proof of that event now lives on a chain that no one controls, that no one can edit, and that anyone can verify.

The tLog recorded what happened. The gLog proves what happened, to anyone, forever, without asking anyone to trust anyone.

### 2.3 Schema Agnosticism: The CRDM

The Canonical Retail Data Model (CRDM) is the normalization layer that makes the gLog universal. POS systems emit events in proprietary formats — Square's webhook schema differs from Clover's, which differs from Toast's. The CRDM maps all proprietary event schemas into a canonical representation that the protocol pipeline can process uniformly.

The CRDM does not interpret events. It normalizes them. A payment event from Square and a payment event from Clover both produce the same canonical representation: merchant ID, timestamp, amount, line items, payment method, and associated metadata. The canonical representation is what gets hashed, sealed, and inscribed. The original proprietary payload is preserved in the evidence store (Sub 1) as the legal witness.

This design choice — normalize first, process uniformly — is what enables RaaS. Any POS system that can emit a webhook can participate in the protocol. The CRDM is the adapter. The protocol pipeline does not know or care where the event originated. It knows that the event conforms to canonical schema, that the hash is computed, and that the Merkle batch is ready.

---

## Section 3 — Protocol Architecture

### 3.1 Six-Node Architecture

The elJeffe protocol is a six-node pipeline where each node is stateless, independently deployable, and connected by a durable message queue (Valkey Streams). The six nodes are:

**Node 1 (API Gateway):** Receives webhook events from external POS systems. Validates OAuth 2.0 authorization scope. Verifies HMAC-SHA256 signature integrity. Generates a correlation ID for end-to-end traceability. Publishes the validated event to the Valkey Streams queue. All operations are asynchronous — the POS system receives a 200 OK response within milliseconds.

**Node 2 (Event Normalizer):** Consumes events from the queue. Computes the SHA-256 hash of the raw payload. This hash becomes the permanent identity of the event — it is the value that will ultimately be inscribed on Bitcoin. Publishes (payload + hash + correlation ID) back to the queue for consumption by three independent subscribers.

**Node 3 (Hash Engine — Subscriber 1):** Consumes from the queue. Performs INSERT-only storage of the raw payload and its hash into the evidence store (PostgreSQL, append-only schema with immutability triggers). This is the legal witness. No transformation. No interpretation. The raw event as received, hashed, and sealed. If every other component fails, Sub 1's record is sufficient to reconstruct the truth.

**Node 4 (Evidence Store — Subscriber 2):** Consumes the same event from the queue. Parses the payload according to CRDM canonical schema. Evaluates 26 detection rules (Chirps) against the parsed data. Fires alerts to the merchant's mobile companion (Today's View). Routes evidence to the Fox case management system. This is the business intelligence layer — it makes the data useful. If Sub 2 fails, it can be reindexed from Sub 1's raw evidence without data loss.

**Node 5 (Merkle Batcher — Subscriber 3):** Consumes hashes from the queue. Accumulates them in a buffer. Periodically (configurable: every 10 minutes, hourly, or daily depending on merchant tier) constructs a Merkle tree from accumulated hashes. Computes the Merkle root — a single 32-byte value that cryptographically represents every event since the last batch.

**Node 6 (Ordinal Inscriber):** Consumes the Merkle root from Node 5. Calls the OrdinalsBot API to inscribe the root as a Bitcoin Ordinal on mainnet. Returns the inscription ID, block height, and transaction ID. This is the permanent anchor — the 32 bytes that prove every event in the batch occurred, verifiable by anyone who can query the Bitcoin blockchain.

### 3.2 The Triple Subscriber Pipeline (TSP)

The three subscribers (Nodes 3, 4, and 5) are competing consumers on the same Valkey Streams queue. They process the same event in parallel, performing three orthogonal functions:

Sub 1 seals the legal witness (raw truth, hash chain, append-only evidence). Sub 2 makes data useful (parsed schema, detection rules, alerts, case routing). Sub 3 anchors to Bitcoin (Merkle batching, Ordinal inscription, permanent settlement).

This separation is not merely architectural — it is jurisdictional. Sub 1's output is the evidence an attorney presents in court. Sub 2's output is the dashboard a merchant sees on their phone. Sub 3's output is the proof that both are anchored to a record no one controls. Each serves a different audience (legal, operational, cryptographic) and operates independently.

The TSP's resilience guarantee: if any single subscriber fails, the other two continue to function. Sub 2 can crash without losing evidence (Sub 1 holds the raw record). Sub 3 can be delayed by Bitcoin fee spikes without affecting merchant operations (Sub 2 has already fired alerts). The protocol degrades gracefully because no single subscriber is on the critical path for all functions.

### 3.3 The Protocol Pipe

The complete end-to-end flow — from a Square merchant processing a transaction to a Bitcoin inscription — is the Protocol Pipe. It is the integration test of the entire system:

A merchant processes a transaction. Square fires a webhook to the elJeffe API Gateway. Node 1 validates OAuth scope and HMAC signature. Node 2 computes the SHA-256 hash. Sub 1 seals the evidence in milliseconds. Sub 2 parses the event, evaluates 26 Chirp rules, and fires an alert to the merchant's phone. Sub 3 batches the hash. When the batch is full or the timer expires, Node 5 builds the Merkle tree, computes the root, and Node 6 inscribes it on Bitcoin.

Total latency: sub-second for merchant-visible operations (Chirp alert, Today's View update). Approximately 10 minutes for Bitcoin confirmation (one block). The merchant does not wait for Bitcoin. They see their alert instantly. The Bitcoin inscription is a background operation that provides permanent, independently verifiable proof.

As of Sprint 5 baseline (February 2026), all six nodes are built. Twenty-six real Square webhooks have been processed through the pipeline. All returned 200 OK. Sprint 6 targets the first production heartbeat: a real merchant event sealed, inscribed, and receipted on Bitcoin.

---

## Section 4 — Hybrid Chain Design

### 4.1 The Latency-Permanence Tradeoff

The six-node architecture described in Section 3 anchors events to Bitcoin with approximately 10-minute finality (one block confirmation). For loss prevention and audit purposes, this is sufficient — no investigation operates on a 10-minute clock. But for merchant experience, it is not. Merchants need instant confirmation that their transaction was recorded and their receipt is valid. They need sub-second feedback.

Bitcoin's proof-of-work consensus produces blocks every ~10 minutes by design. This interval cannot be reduced without compromising the security model that makes Bitcoin permanent in the first place. Any protocol that requires both permanence and speed faces an irreducible tension: the chain that provides permanence cannot provide speed, and the chain that provides speed cannot provide permanence.

### 4.2 The Hybrid Architecture

The elJeffe hybrid chain architecture resolves this tension by operating across two complementary layers:

**Avalanche (The Execution Layer):** A private subnet on the Avalanche network provides sub-second receipt finality. Every merchant event processed through the TSP is minted as an on-chain receipt on Avalanche. The merchant receives instant confirmation. Receipts are queryable, searchable, and verifiable against the Avalanche chain in real time. Cost: approximately $0.001 per event on a private subnet.

**Bitcoin (The Settlement Layer):** Periodically (daily, hourly, or per-block depending on merchant tier), all Avalanche receipts since the last anchor are aggregated into a Merkle tree. The root is inscribed on Bitcoin as an Ordinal. The inscription is permanent — proof-of-work immutability. Every individual receipt can be independently verified against the Bitcoin anchor via its Merkle proof path.

The architecture is symbiotic, not redundant. Bitcoin provides permanence that Avalanche cannot guarantee (Avalanche depends on active validators; Bitcoin depends on proof-of-work). Avalanche provides speed that Bitcoin cannot deliver (sub-second vs. 10 minutes). Neither chain is sufficient alone. Together, they deliver both guarantees simultaneously.

### 4.3 Economic Viability of the Hybrid Model

The hybrid architecture is not merely an engineering preference — it is an economic necessity. Pure Bitcoin inscription at per-event granularity is nonviable at any merchant scale: a single merchant generating 200 transactions per day would incur $124,100 per year in inscription fees at medium Bitcoin fee rates (10 sat/vB). Even with global daily batching (one inscription per day for all merchants combined), the Bitcoin anchor costs only $621 per year regardless of merchant count — but imposes a 24-hour finality delay that the product cannot tolerate.

The hybrid model resolves this: Avalanche handles real-time receipt creation at $0.001 per event (approximately $73 per merchant per year on a private subnet), while Bitcoin provides daily settlement at $621 per year total. At 1,000 merchants, the combined annual chain cost is approximately $83,600 against subscription revenue of $468,000 (at the $39/month tier) — delivering 82% gross margin.

The private Avalanche subnet breaks even against the shared Avalanche C-Chain at approximately 35 merchants, where the 5x per-transaction cost reduction ($0.001 vs. $0.005) exceeds the fixed annual validator cost of $10,000. Post-Avalanche9000 (December 2024), the 2,000 AVAX staking requirement for subnet validators was eliminated, reducing the capital barrier from ~$20,000 to minimal AVAX exposure.

### 4.4 The Fee Window

Three independent escalation drivers are converging to close the current low-fee window on Bitcoin L1:

**The halving cycle.** Bitcoin's block reward halves every four years. The next halving (2028) reduces miner subsidy by 50%, forcing miners to shift revenue reliance toward transaction fees. The fee floor rises structurally.

**Adoption demand.** Layer 2 protocols, DeFi applications, and inscription demand compete for Bitcoin's limited block space (~4 MB per block, ~7 transactions per second). As adoption grows, the mempool fills and fees rise.

**Inscription competition.** The Ordinals ecosystem is growing. More entities discovering inscription-based applications means more transactions competing for the same block space.

At 50–100 sat/vB sustained fees (realistic within 12–24 months), the cost of per-event inscription becomes prohibitive for all but the highest-value, lowest-frequency use cases. The entity that has already inscribed a canonical record pool during the current 1–3 sat/vB window holds a permanent cost advantage. That record pool exists. The block space that carried those inscriptions has been mined and is gone. A competitor entering the market after the window closes faces structurally higher inscription costs — not because of GrowDirect's pricing, but because of Bitcoin's fee market physics.

### 4.5 Genesis Pool as Network Asset

The Genesis Pool — 0.1 BTC (10,000,000 satoshis) derived from an original F2Pool mining reward — funds the protocol's inscription operations. Under the hybrid model with stacked reinscription (append-only Merkle roots on a single satoshi per merchant), the pool funds 1,000 merchant gLog activations (2,000,000 sats), 13.7 years of daily global Bitcoin anchoring (5,000,000 sats at medium fee rates), and a 30% reserve for fee volatility (3,000,000 sats).

The pool's value is not its Bitcoin price. Under Metcalfe's Law (V ∝ n²), the pool's network value grows quadratically with the number of merchants, inscriptions, validation requests, and namespace registrations it anchors. At 50 merchants (approximately month 9), the network valuation crosses above the static BTC valuation. At 350 merchants (month 18), the network valuation exceeds the static BTC valuation by approximately 69x. The pool is not a holding. It is the substrate of a network whose value compounds with every participant.

The protocol reaches self-sufficiency at approximately 17 merchants — a convergence point where the Genesis Pool becomes permanently self-replenishing, historical validation revenue covers ongoing infrastructure costs, and the DAO treasury allocation exceeds marginal chain cost per merchant by more than 3x. This number is robust: sensitivity analysis across BTC price swings (±50%), fee rate changes (±100%), and subscription price variations (±25%) yields a convergence range of 12–24 merchants, with 17 as the central tendency.

---

## Continuation Notice

**Sections 5–12 are drafted separately per the Research Paper Roadmap (Section C).** Section 5 (Economic Model) incorporates the "Why 17" convergence analysis and Metcalfe's Law Genesis Pool model from Tasks 1 and 2 of this work order. Sections 6–10 draw from Manifesto Parts IV–VII. **Section 11 (Patent Claims and IP Position) remains BLOCKED until Syd defines disclosure boundaries.** Section 12 (Conclusion) will be written after all preceding sections are complete.

---

## Internal Notes (Not for Publication)

### Sources Referenced in Sections 0–4

| Source | Manifesto Section | Used In |
|---|---|---|
| IBM 4690 tLog architecture | I.1 | Section 1.1, 2.1 |
| LaneHawk incident | I.2 | Background context (not cited directly — Syd to advise on disclosure) |
| Chargebacks911 2024 report | External | Section 1.2 (chargeback cost figure) |
| NRF 2023 Retail Shrink Survey | External | Section 1.2 (shrink figure) |
| Ordinals Protocol (Rodarmor, 2023) | V.1 | Section 1.3 |
| CRDM specification | III.2 | Section 2.3 |
| Six-node architecture | V.1 | Section 3.1 |
| TSP design | V.2 | Section 3.2 |
| Protocol Pipe | V.4 | Section 3.3 |
| B-069 Hybrid Chain Economics | IV.4 | Section 4.2, 4.3 |
| Fee Window analysis | VI.3 | Section 4.4 |
| Genesis Pool | IV.1 | Section 4.5 |
| "Why 17" Convergence (Task 1) | IV.7 | Section 0, 4.5 |
| Metcalfe Genesis Pool (Task 2) | IV.1 | Section 0, 4.5 |
| RaaS framing (Task 3) | IV.3.1 | Section 0, 1.4 |

### IP Sensitivity Review (for Syd)

Sections 0–4 describe:
- The mutable record problem (public knowledge, no IP concern)
- The gLog principle (covered by provisional patent 63/991,596)
- The CRDM (described at concept level, no schema details disclosed)
- The six-node architecture (described at concept level, no code or implementation details)
- The TSP (described at concept level, Claim 1 coverage)
- Hybrid chain design (described at concept level, Claim 7 coverage)
- Fee window economics (public Bitcoin fee data + GrowDirect's interpretation)
- Genesis Pool (described at concept level, Claim 2 coverage)
- Metcalfe's Law application (novel application, not patentable per se)
- "Why 17" convergence (derived analysis, not patentable per se)

**PhD assessment:** Sections 0–4 describe architecture and economics at a level appropriate for investor communication and do not disclose implementation details that would enable a competitor to replicate the system. No patent claim is disclosed in a way that would compromise utility filing. Syd should confirm.

---

## Routing

- **Syd:** IP sensitivity review before any external distribution. Confirm Sections 0–4 are safe.
- **Jess:** Sections 0–4 will feed investor site copy, War Chest updates, and companion guide revisions.
- **Art:** Figures referenced in Sections 0–4 (Figs. 1–5) exist as Mermaid diagrams in the Manifesto. Art should prepare publication-quality versions for the paper.
- **Jeremy:** Validate Section 3 (architecture) and Section 4.3 (economics) against running code.
- **Tom:** Validate Section 4.2 (hybrid architecture) against B-072 namespace architecture.

---

*PhD | Research Framework | March 1, 2026*
*B-077 Task 4 — Position Paper Sections 0–4 DRAFT*
*"Universal Event Notarization on the Bitcoin Time Chain"*
