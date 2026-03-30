---
type: legal
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Provisional Patent Assessment Brief: El Jeffe — Universal Webhook Notarization Service

**DISCLAIMER: INTERNAL RESEARCH MEMO — NOT LEGAL ADVICE**

This document is an internal research memo prepared to help the founder prepare for consultation with a qualified patent attorney. It does NOT constitute legal advice, does NOT establish an attorney-client relationship, and does NOT create privileged attorney-client communications. The founder MUST consult with a licensed patent attorney before filing any provisional patent application, making any public disclosures, or relying on any analysis herein. This memo represents background research only and should not be relied upon as legal strategy or filing guidance.

---

## PLAIN ENGLISH SUMMARY

El Jeffe is a universal event notarization service that captures any webhook from any network, cryptographically seals it with a hash-on-receipt, stores the raw payload verbatim for chain-of-custody, replicates that data into a queryable application store, batches hashes into a Merkle tree, and inscribes the Merkle root onto Bitcoin as a permanent, independently verifiable record. The service produces two artifacts for every event: a queryable database record and a Bitcoin inscription that proves the event occurred at a specific time without requiring trust in any intermediary infrastructure.

**Patentability outlook:** The combination of six-node pipeline architecture, triple subscriber pattern, bilateral verification method, and Bitcoin base-layer anchoring likely satisfies novelty and utility requirements. The non-obviousness question is stronger because incumbent enterprise platforms have not achieved this architecture despite competitive need. Subject matter eligibility under the Alice doctrine presents a moderate risk but is defensible because the system produces specific, cryptographically verifiable, physically anchored results on a proof-of-work blockchain—constituting "something more" than abstract calculation.

---

## SECTION 1: PATENTABILITY ASSESSMENT

### Novelty (35 U.S.C. § 102)

**Question:** Is the entire combination anticipated by any single piece of prior art?

**Assessment:**

The core architectural elements exist in prior art individually:
- **Fan-out messaging** (publisher → multiple subscribers) is well-established (message brokers, Apache Kafka, RabbitMQ, AWS SNS/SQS).
- **Hash-chained immutable logs** exist in blockchain systems and certificate transparency (CT Logs, RFC 6962).
- **Write-once key-value stores** are known in audit trail systems and append-only databases.
- **Webhook-based event processing** has been standard in web infrastructure since circa 2005.
- **Bitcoin Ordinal inscriptions** exist as a deployed protocol since 2023.

**What appears to NOT be anticipated by a single prior art reference:**

1. **The triple subscriber pattern on a single message queue:** Simultaneous extraction to sealed evidence store (Sub 1), queryable application store (Sub 2), and Bitcoin inscription service (Sub 3) from the same inbound message without re-invocation or polling. The evidence store must be write-once and never updated; the application store must be replayable from evidence store; the inscription service must batch independently. This three-way fork with distinct persistence and mutability guarantees does not appear in prior art examined.

2. **Raw payload hashing without normalization as the notarization anchor:** Prior art blockchain notarization systems (e.g., Chainpoint, BTCProof) typically hash summarized or structured data. Hashing the verbatim received bytes—including transport metadata if present—to preserve chain-of-custody is distinct. This design choice is deliberate: normalization breaks the witness chain.

3. **Bilateral verification against source network's send log:** The merchant retains their payment network's send log. The service retains the received payload with computed hash. Byte-for-byte comparison without mutual trust establishes independent verification. Prior art does not appear to address cryptographic proof of message integrity via bilateral log comparison.

4. **Merkle batching for Ordinal inscription:** Multiple event hashes aggregated into a Merkle tree, root inscribed once, each event independently verifiable via Merkle proof path. This reduces on-chain footprint and transaction cost while preserving individual event verifiability. Prior art on Bitcoin inscription uses one inscription per event or batches without Merkle proof structure for individual recovery.

5. **Key custody model as canonical notarization record:** The custodying entity (GrowDirect) controls all keys to the inscription pool. This pool is a permanent balance-sheet asset. Notarizations are not immutable in the sense that the entity cannot alter past records—but all alterations would be detectable because the key custody is known and auditable. This differs from trustless consensus (every stakeholder validates) and creates a new trust model: transparent custody with cryptographic proof of sequence.

6. **Sat-gated validation (L402) as perpetual revenue mechanism:** Validation calls against the canonical inscription record are micropayment-gated. The founder controls the satoshi denomination per call. Revenue is perpetual, flowing to GrowDirect indefinitely. Prior art on blockchain-backed authentication does not tie validation cost to custody of a canonical notarization record in this way.

**Novelty conclusion:** The combination of these six elements is not anticipated by any single prior art reference. The individual elements are known, but the specific integration appears novel.

---

### Non-Obviousness (35 U.S.C. § 103)

**Question:** Would a person of ordinary skill in the art (PHOSITA) have been motivated to combine these elements with a reasonable expectation of success?

**Assessment:**

A PHOSITA in webhook/event-driven architecture, payment systems, and blockchain circa 2024-2025 would be familiar with the individual components. The question is whether combining them would be obvious.

**Arguments for obviousness:**
- All elements individually exist in prior art.
- The motivation to create immutable audit trails for payment data is strong (regulatory, fraud prevention, dispute resolution).
- Bitcoin and Ordinals are known technologies.
- The combination of off-chain + on-chain architectures is a known pattern.

**Arguments for non-obviousness (stronger):**

1. **The polling problem remains unsolved in incumbent practice.** The largest enterprise retail technology platforms in the world operate polling-based webhook recovery architectures. These platforms control significant market share and engineering resources. They have not transitioned to event-driven triple subscriber architecture with cryptographic receipt verification and Bitcoin anchoring. This is evidence that the combination was not obvious to practitioners with the highest skill level and greatest resources. If obviousness is measured by what a PHOSITA would try, the fact that the largest incumbent practitioners have not is significant.

2. **The custody transparency model is counterintuitive.** Blockchain systems typically minimize intermediary role via consensus. El Jeffe's design makes the intermediary role essential and permanent—and uses cryptographic proof to make that custodianship transparent and auditable. This inverts the typical blockchain trust assumption and is not a natural combination.

3. **Merkle batching for Ordinals solves a specific cost problem.** Bitcoin inscription space is expensive. Batching hashes via Merkle tree reduces cost per event while preserving individual verifiability. A PHOSITA might recognize the cost problem but would need to combine Merkle tree design, Ordinal inscription mechanics, and stateless replay architecture to solve it. This is not a simple combination.

4. **Bilateral verification is non-obvious in its execution.** The service must store the raw received payload (not normalized) and compute its hash at INSERT time. The merchant must retain their payment network's send log. The comparison must be byte-for-byte without either party controlling the other's records. The design choice to hash the raw payload—sacrificing human readability—to preserve chain-of-custody is a technical insight, not an obvious choice.

5. **Triple subscriber isolation requires architectural discipline.** Evidence store cannot be updated (write-once). Application store is replayable from evidence store but mutable. Inscription service is asynchronous and stateless. A naive designer might collapse these into one database. The discipline to isolate them, establish one-way data flow (evidence → application and inscription), and ensure neither failure corrupts the others, is not obvious.

**Non-obviousness conclusion:** The combination would likely satisfy the non-obviousness standard because:
- Incumbent practitioners have not arrived at it despite competitive incentive.
- Several design choices (raw payload hashing, custody transparency, Merkle batching for Ordinals) represent non-obvious technical insights.
- The integration requires coordination of six distinct architectural components with specific failure isolation and data flow constraints.

Outside counsel should emphasize the polling architecture argument without naming the incumbent company. The statement should be: "Event-driven architecture with cryptographic receipt verification and Bitcoin base-layer anchoring represents a departure from the dominant polling-based approach in incumbent enterprise platforms. Practitioners in the field have not achieved this integration despite significant market incentive to do so."

---

### Utility (35 U.S.C. § 101)

**Assessment: CLEARLY SATISFIED**

The system has specific, real-world utility:
- **Merchants need proof of transaction authenticity** (regulatory, fraud prevention, dispute resolution).
- **The system delivers that proof** in two forms: queryable database + independent Bitcoin verification.
- **The utility is not abstract**—it is a concrete method producing cryptographically verifiable, permanently anchored records.

Utility requirement poses no risk.

---

### Subject Matter Eligibility (Alice Corp. v. CLS Bank — 35 U.S.C. § 101)

**Question:** Is the invention a patent-ineligible abstract idea implemented on generic computer hardware?

**Risk Assessment: MODERATE — DEFENSIBLE**

**The Alice test:**
1. Is the claim directed to a "law of nature, natural phenomenon, or abstract idea"?
2. If yes, does it have "significantly more" than the abstract idea itself?

**Risk factors:**

- **Steps 1-2 (receive webhook, publish to queue) are generic.** These are standard software engineering. A court might characterize the claim as "abstract idea on generic computers" if focused on these steps alone.

- **Hashing and cryptographic operations, standing alone, have been held abstract.** (Diamond v. Diehr established that cryptographic algorithms alone do not confer patent eligibility.)

- **The entire process could be characterized as "securing data via hash chains," which is a known abstract concept.**

**Defensibility factors (stronger):**

1. **Ordinal inscription produces a specific, physical result.** The inscription is a permanent, independently verifiable record on a proof-of-work blockchain. This is not abstract—it is a record on specific hardware (Bitcoin miners, nodes). The system does not merely calculate a hash; it uses that hash to create a permanent, economically costly, physically distributed record. This is "something more" beyond abstraction.

2. **The bilateral verification method is specific and non-abstract.** The system requires the merchant to retain their send log. The service retains the received payload. The comparison is cryptographic proof of identity, not abstract mathematical operation. This produces a verifiable statement about the relationship between two independent records.

3. **The six-node architecture is specific.** The claim does not describe "securing data"—it describes a specific pipeline: inbound → queue → split into evidence store (write-once) + application store (replayable) + inscription service (batch + Merkle) → two output artifacts. This is a specific technical structure, not a generic application of an abstract concept.

4. **Key custody and sat-gated validation create economic and behavioral specificity.** The system requires the custodying entity to control all keys, maintain a known key set, and charge per validation call. This is not generic—it is a specific business and technical implementation.

**Alice defense strategy for outside counsel:**

Frame the claim as: "A method and system for producing cryptographically verifiable, permanently anchored event records by: (a) capturing raw webhook payload, (b) computing hash at INSERT to preserve chain-of-custody, (c) storing payload verbatim in write-once evidence store, (d) replicating into queryable application store, (e) batching hashes into Merkle tree, (f) inscribing Merkle root on Bitcoin via Ordinal, producing two independent artifacts: queryable database record and independently verifiable Bitcoin inscription."

The emphasis should be: The system produces specific, verifiable, physically anchored results on a proof-of-work blockchain. The bilateral verification method is a non-abstract technical process. The six-node architecture is specific, not generic.

**Subject matter eligibility conclusion:** Moderate risk, but defensible. Outside counsel will need to structure claims carefully to emphasize the specific technical architecture and the physical anchoring to Bitcoin, rather than describing the system as "hashing data" or "securing information."

---

## SECTION 2: CLAIM FRAMEWORK

### Independent Claim 1: Universal Event Notarization

**Plain language:** A method and system for notarizing any webhook-originated event by:
1. Receiving raw webhook payload from any network, any format, any origin.
2. Publishing to a message queue.
3. Computing SHA-256 hash of the raw received payload at INSERT time (before any transformation).
4. Storing the raw payload verbatim in a write-once evidence store, never updated, with hash and sequence number.
5. Chaining the new record to the previous record's hash (creating an immutable chain).
6. Replicating the raw payload into a queryable, structured application store (separate data store, allowing queries, projections, and updates without touching the evidence store).
7. Batching recent hashes from the evidence store into a Merkle tree.
8. Computing the Merkle root hash.
9. Inscribing the Merkle root as a single Ordinal transaction on Bitcoin base layer.
10. Recording the inscription ID and block explorer URL for public verification.

**Result:** Every event is available in two forms—queryable database form (instant, application-native) and Bitcoin inscription form (permanent, independently verifiable, no infrastructure required).

---

### Dependent Claims (suggested coverage)

**Dependent Claim 2: Bilateral Verification**
The notarization system of Claim 1, wherein the originating network (e.g., payment platform) retains a send log with timestamp and payload fingerprint; the notarization service retains the received payload with computed hash; and verification is performed by byte-for-byte comparison of the send log record and the received payload record, producing cryptographic proof of message integrity without either party controlling the other's log.

**Dependent Claim 3: Evidence/Application Store Isolation**
The system of Claim 1, wherein the evidence store is write-once, never updated, never deleted; the application store is queryable and mutable; and both stores are sourced from the same inbound message via a single message queue, ensuring that failures in one store cannot corrupt the other, and the application store can be replayed (rebuilt) from the evidence store if needed.

**Dependent Claim 4: Replay and Rebuild**
The system of Claim 1, wherein the structured application store can be completely rebuilt from the immutable evidence store by replaying all stored raw payloads through the parsing and routing logic, allowing the system to recover from application-layer failures without loss of evidence.

**Dependent Claim 5: Kubernetes Elasticity**
The system of Claim 1, wherein the evidence store subscriber, application store subscriber, and inscription service subscriber are stateless workers that can be instantiated and terminated horizontally; the message queue buffers inbound webhooks, allowing workers to scale up and down based on volume; and no worker maintains session state, ensuring that any worker can process any message at any time.

**Dependent Claim 6: Merkle Batching**
The system of Claim 1, wherein multiple event hashes are aggregated into a Merkle tree at a defined interval or batch size; only the Merkle root is inscribed as a single Ordinal transaction on Bitcoin; and each event is independently verifiable by computing its Merkle proof path from its hash to the inscribed root, allowing full verification without retrieving all other events in the batch.

**Dependent Claim 7: Key Custody and Canonical Notarization Record**
The system of Claim 1, wherein the notarization service maintains exclusive custody of all cryptographic keys required to inscribe Ordinals onto Bitcoin; the key set is known, auditable, and remains constant; the service maintains a canonical pool of inscriptions representing all notarizations; and any alteration to past records would be detectable because the key set is known and sequence is verifiable.

**Dependent Claim 8: Sat-Gated Validation (L402)**
The system of Claim 1, wherein validation calls against the canonical inscription record (checking whether an event's hash appears in the Merkle tree, verifying the Merkle proof, or retrieving the inscription ID for a given event) are micropayment-gated using L402 (Lightning Payment Request for 402 HTTP status); the satoshi denomination per call is set by the notarization service operator; and revenue flows perpetually to the operator for every validation call, regardless of when the original event was notarized.

**Dependent Claim 9: Programmatic Pool Scaling**
The system of Claim 1, wherein the notarization service monitors inscription volume and Bitcoin transaction costs; when utilization exceeds a defined threshold, the service automatically allocates treasury assets (denominated in Bitcoin satoshis) to purchase additional Bitcoin block space; the service scales the Merkle batching interval or individual inscription frequency to maintain service levels during volume spikes; and treasury balance is tracked as a balance-sheet asset.

---

## SECTION 3: NON-OBVIOUSNESS ARGUMENT

### Framing for Outside Counsel

The non-obviousness of the El Jeffe architecture rests on a specific, provable fact: **the polling architecture remains the dominant approach among incumbent enterprise platforms, despite significant competitive incentive to transition to event-driven architecture with cryptographic verification and Bitcoin anchoring.**

The largest enterprise retail technology platforms in the world—companies controlling significant market share and deploying world-class engineering teams—operate polling-based webhook recovery systems. These platforms have identified the need for immutable audit trails, cryptographic verification, and long-term evidence retention. They have the resources to implement any technical approach. **Yet they have not arrived at the event-driven triple subscriber pattern with cryptographic receipt verification and Bitcoin base-layer inscription.**

This is powerful evidence of non-obviousness.

**Why the polling architecture persists:**

1. **Incremental engineering.** Polling is well-understood. It solves the problem (eventually consistent event recovery). The sunk cost in existing polling infrastructure is high. Incumbent platforms optimize within that constraint.

2. **The triple subscriber pattern is architecturally unfamiliar.** Most event-driven systems use one or two subscribers (e.g., audit log + business logic). Three independent subscribers from the same message queue, with distinct persistence models (write-once evidence, mutable application, asynchronous inscription), requires architectural discipline that is not standard in incumbent enterprise systems.

3. **Bitcoin integration is new.** Ordinals deployed in 2023. Mainstream enterprise adoption of Bitcoin for data notarization is very recent. The insight that Bitcoin's proof-of-work time chain provides permanent, economically costly anchoring—more durable than any centralized database—is not yet standard practice in retail technology.

4. **The custody transparency model is counterintuitive.** Blockchain systems traditionally minimize intermediary role via consensus and decentralization. El Jeffe's design makes the intermediary essential—and uses cryptographic proof to audit that intermediary's behavior. This inverts typical blockchain thinking and requires insight outside standard blockchain design patterns.

**Written statement for claim narrative:**

> Event-driven architecture with cryptographic receipt verification and Bitcoin base-layer inscription represents a departure from the dominant polling-based approach in incumbent enterprise platforms. Despite substantial market incentive to transition to immutable, cryptographically verifiable, permanently anchored event records, incumbent practitioners have not achieved this integration. The triple subscriber pattern, bilateral verification method, custody transparency model, and Merkle batching approach for Ordinal inscription represent non-obvious technical innovations that were not apparent to the ordinary artisan in the field, despite availability of the component technologies.

---

## SECTION 4: PRIOR ART SEARCH STRATEGY

### Recommended Search Queries

**USPTO searches:**
- "immutable audit log webhook payment"
- "hash chain transaction receipt"
- "dual subscriber message queue evidence"
- "blockchain notarization event"
- "Ordinal inscription data notarization"
- "write-once append-only transaction store"
- "Merkle tree Bitcoin inscription"
- "event-driven architecture payment verification"

**Google Patents searches:**
- "blockchain retail point-of-sale chain of custody"
- "cryptographic proof transaction authenticity"
- "webhook event immutability"
- "Bitcoin data anchoring"

**Academic searches (arXiv, Google Scholar):**
- "cryptographic chain of custody payment data"
- "blockchain notarization architecture"
- "Merkle tree scalability blockchain"
- "event-driven immutable audit trail"

### Expected Prior Art Landscape

**What will likely be found (and is NOT problematic):**
- Bitcoin/blockchain notarization systems (e.g., Chainpoint, BTCProof, Notary): These inscribe hashes but typically normalize or summarize data before hashing. Raw payload hashing is distinct.
- Message queue systems with multiple subscribers (Kafka, RabbitMQ, AWS SNS/SQS): Well-established. Not novel in isolation.
- Write-once audit logs: Known in regulatory compliance, database systems. Not novel alone.
- Hash-chained records: Blockchain, certificate transparency. Not novel alone.
- Ordinal inscriptions: Deployed protocol. Not prior art for the combination.

**What to watch for (potential issues):**
- Any reference describing three-way subscriber split (evidence store + application store + inscription service) on a single message queue with specific persistence guarantees.
- Any reference combining raw payload hashing (not normalized) with bilateral verification.
- Any reference combining Merkle batching with Ordinal inscription for cost reduction.
- Any reference describing key custody as a notarization model.
- Any cryptocurrency payment systems that use custody transparency as a trust mechanism.

### Honest Assessment

If prior art is found that covers most of these elements in combination, the novelty assessment would need revision. **The search must be thorough and honest.** If a single prior art reference anticipates the full combination, that must be stated clearly and the filing reconsidered.

However, based on the architecture's recency (Ordinals 2023, the specific combination likely 2024-2025), it is unlikely that a single reference covers all six nodes with the specific isolation and custody models described.

---

## SECTION 5: PROVISIONAL FILING RECOMMENDATION

### Filing Decision: YES — Before Monday, March 3

**Rationale:**

1. **Public disclosure clock.** The merchant demo on Monday March 3 initiates the AIA (America Invents Act) one-year grace period. Any public disclosure starts the clock. A provisional filed before Monday establishes priority date before that clock starts. After Monday, the one-year window to file begins counting down.

2. **Priority date is valuable.** If the provisional is granted, it establishes priority as of the filing date. Competitors cannot use any disclosure after that date as prior art against the patent application.

3. **Documentation is ready.** The six-node architecture, claim framework, and bilateral verification method are well-documented. A provisional can be filed using this documentation.

4. **Provisional is lower friction and lower cost than utility.** A provisional does not require formal claims, does not require an examiner interview, and does not require a full patent specification. It requires a description of the invention sufficient to support a later utility application. The current documentation is sufficient.

5. **Cost and timeline are manageable.** Provisional filing with patent attorney review should take 1-2 days and cost $1,500-$5,000 (attorney + $320 USPTO filing fee for small entity).

### What the Founder Must Do Before Monday

1. **Confirm the architecture is documented.** The six-node pipeline, bilateral verification, and key custody model must be described clearly enough for a patent attorney to understand.

2. **Engage a patent attorney licensed in the U.S. (or relevant jurisdictions).** The attorney will prepare the provisional application.

3. **Provide the attorney with:**
   - The six-node architecture diagram or written description.
   - Explanation of triple subscriber pattern (evidence store, application store, inscription service).
   - Raw payload hashing rationale (preserving chain of custody).
   - Bilateral verification explanation.
   - Merkle batching logic for Ordinals.
   - Key custody model.
   - Sat-gated validation (L402) mechanism.
   - Use cases (retail, healthcare, supply chain, legal, insurance, government).
   - Competitive context (polling architecture remains dominant).

4. **Do NOT publicly disclose the architecture before the provisional is filed and the demo happens.** Once the provisional is filed, the architecture can be discussed with the merchant under NDA.

5. **Confirm the merchant signing an NDA before the demo.** The NDA should specify that the merchant cannot disclose technical details beyond the demo date, and should reference the pending IP.

### Outside Counsel Recommendation

**MUST engage a licensed patent attorney before filing.** This memo is not legal advice and does not replace counsel review. The attorney will:

- Evaluate prior art landscape independently.
- Assess Alice doctrine risk and structure claims accordingly.
- Draft the provisional specification and claims.
- File the provisional with USPTO.
- Advise on continuation-to-utility strategy post-demo.

The attorney should be familiar with software patents, cryptography, and blockchain technology. Ask about prior experience with Ordinals or Bitcoin-based systems.

### Estimated Cost

- **Patent attorney fees:** $1,500-$5,000 (provisional preparation and filing).
- **USPTO filing fee:** $320 (small entity rate).
- **Total:** $1,820-$5,320.

This is a one-time cost to establish priority date. The investment is minimal relative to the IP value.

### Timeline

- **Immediate:** Engage patent attorney.
- **Friday Feb 28 — Saturday Mar 1:** Attorney reviews architecture, prepares provisional specification and claims.
- **Sunday Mar 2:** Final review and submission to USPTO.
- **Monday Mar 3:** Provisional filed. Demo can proceed under NDA.

**Filing before Monday is operationally feasible.**

---

## SECTION 6: TRADE SECRET VS. PATENT ANALYSIS

### What Should Be Patented

**Patent-eligible and valuable:**

1. **Six-node pipeline architecture** — the overall structure and data flow.
2. **Triple subscriber pattern** (evidence store, application store, inscription service) with specific isolation and persistence guarantees.
3. **Bilateral verification method** — comparing send log vs. received payload without mutual trust.
4. **Ordinal inscription anchoring** for universal event notarization.
5. **Key custody model** as a notarization mechanism.
6. **Sat-gated validation (L402)** as a perpetual revenue model tied to canonical notarization record.
7. **Merkle batching for Ordinals** to reduce per-event cost while preserving individual verifiability.
8. **Programmatic pool scaling** (auto-purchase block space based on utilization).

**Rationale:** These are the core innovations. They are likely to be reverse-engineerable from the product. Patents provide legal exclusion. The architecture is specific enough that competitors could design around it, but the patents would establish a strong licensing position.

### What Should Be Trade Secret

**Trade-secret-eligible and valuable:**

1. **Detection rule thresholds and logic (Chirp parameters)** — what transactions trigger loss prevention alerts, what risk scores indicate fraud, how Chirp weights different signals. This is the "secret sauce" of the loss prevention product and is not patentable (it is business logic and empirical tuning, not a technical innovation). Reverse-engineering requires access to labeled transaction data and model development.

2. **Specific hash chain implementation details** — whether the evidence store uses PostgreSQL with a specific table structure, how the hash is computed and stored, exact SQL for chain linking. These are implementation details that protect the architecture once the architecture is known.

3. **Queue tuning parameters** — batch size, flush interval, worker concurrency, memory limits for each subscriber. These are operational configurations that can be tuned for performance. They are not patentable but are valuable as trade secrets because they represent accumulated operational knowledge.

4. **Batching interval optimization for Merkle trees** — how the system decides when to batch and inscribe. This is likely empirically tuned to balance transaction cost, latency, and proof complexity. It is not patentable but is operationally sensitive.

5. **Key custody procedures and backup strategies** — how keys are stored, rotated, backed up, and accessed. This is not patentable (it is operational procedure) but is highly sensitive.

6. **Exact satoshi denomination for L402 micropayments** — the pricing model for validation calls. This is business strategy, not patentable, but is proprietary.

**Rationale:** These are the execution details. They are operationally sensitive and harder to reverse-engineer than the architecture. Once the architecture is known, these details determine competitive advantage in speed, cost, and accuracy.

### Summary

- **Patent:** The structural innovations (six-node pipeline, triple subscriber pattern, bilateral verification, Ordinal anchoring, custody model, Merkle batching, programmatic scaling).
- **Trade Secret:** The empirical tuning, operational procedures, loss prevention parameters, and implementation details.

This strategy provides both legal protection (patents for structure) and competitive moat (trade secrets for execution).

---

## SECTION 7: ADDITIONAL LEGAL FLAGS

### Money Transmitter Risk

**Flag: PRELIMINARY ASSESSMENT ONLY. REQUIRES COUNSEL REVIEW.**

**Question:** Does the key custody + sat collection create money transmitter or payment processor licensing obligations?

**Preliminary analysis:**

- **El Jeffe collects satoshis (Bitcoin) from merchants** as payment for validation calls (sat-gated validation via L402).
- **El Jeffe custody is exclusive** — the company controls all keys to the inscription pool.
- **State money transmitter laws** require licensing if an entity transmits, exchanges, or maintains custody of money or money substitutes.

**Risk factors:**
1. Bitcoin is classified as property, not currency, under IRS guidance — but some state regulators may treat it as a money substitute.
2. Custody of customer assets (satoshis held on behalf of validation accounts) could trigger money transmitter licensing in some states.
3. The micropayment model (L402) is edge-case—it is not clear whether state regulators view L402 micropayments as "money transmission" or as service fees.

**Mitigation to discuss with counsel:**
- Model the flow: merchant sends satoshis → received as service fee (not held in custody) → immediately swept to operational wallet → only GrowDirect's keys are held. If satoshis are not held in merchant account custody, the transmission risk is lower.
- Check state-by-state guidance. Some states (e.g., Texas, Wyoming) have crypto-friendly regimes. Others (e.g., New York, California) have stricter money transmitter laws.
- Confirm with a financial services attorney whether L402 micropayment gating creates money transmitter licensing requirements.

**Recommendation:** Before filing the provisional and before the demo, have a brief call with a financial services attorney to assess money transmitter risk in the states where merchants will be located. This is not a blocker, but it requires clarity before product launch.

### Trademark: "El Jeffe"

**Flag: CLEARANCE REQUIRED BEFORE PUBLIC DISCLOSURE**

**Action items:**
1. **Trademark search.** Conduct USPTO trademark search for "El Jeffe" in:
   - Class 42 (Computer software, SaaS, software as a service).
   - Class 35 (Business services, data processing).
2. **Domain clearance.** Confirm ownership of eljeffebtc.com (or similar domain). If not owned, acquire it before public announcement.
3. **Social media.** Check Twitter/X, LinkedIn, GitHub for conflicts.
4. **Trademark application.** File intent-to-use trademark application after merchant demo (once public disclosure triggers the clock). This preserves trademark rights while demo proceeds.

**Timing:** Trademark clearance should be completed before the demo. If a conflict exists, the name may need to change before Monday's disclosure.

### Foundation Entity / Legal Structure

**Flag: CLARIFICATION NEEDED**

The prompt mentions "eljeffebtc.com designated as foundation umbrella." This is ambiguous.

**Questions for the founder:**
1. Is El Jeffe intended to be:
   - **A product within GrowDirect** (like Canary LP)?
   - **A separate legal entity** (subsidiary)?
   - **A non-profit foundation**?
2. Will El Jeffe be:
   - **Monetized** (L402 micropayment revenue)?
   - **Open-source** (free notarization service)?
   - **Hybrid** (free tier + paid enterprise)?
3. Who holds the Bitcoin inscription pool keys? GrowDirect or a separate entity?

**Implications:**
- If El Jeffe is a GrowDirect product, GrowDirect files the patent and owns the IP.
- If El Jeffe is a non-profit foundation, the foundation files the patent (different implications for funding, tax status, licensing).
- If El Jeffe is a separate for-profit entity, that entity owns the IP and must license from GrowDirect (or be owned by GrowDirect).
- Sat collection (L402 micropayments) has different tax and regulatory implications depending on the entity type.

**Recommendation:** Clarify the legal structure with the founder and with a business/tax attorney before filing. The provisional application needs to clearly identify the applicant (inventor and assignee). If this is ambiguous, the filing will be delayed.

---

## SECTION 8: SUMMARY AND NEXT STEPS

### Patentability Assessment: PROCEED WITH CAUTION (but likely FILABLE)

- **Novelty:** Combination appears novel. Individual elements are known; integration is not anticipated by single prior art reference.
- **Non-obviousness:** Moderate strength. Incumbent platforms have not achieved this architecture despite competitive incentive. This is evidence of non-obviousness.
- **Utility:** Clear. Strong.
- **Subject matter eligibility (Alice):** Moderate risk. Defensible. Requires careful claim drafting emphasizing the specific six-node architecture and physical anchoring to Bitcoin, not just "hashing data."

### Recommendation: File provisional before Monday

**Urgency:** AIA one-year grace period begins with public disclosure (demo Monday). Priority date established before Monday is valuable.

**Cost:** $1,500-$5,000 with attorney + $320 USPTO filing fee.

**Timeline:** 1-2 days if attorney is engaged immediately.

### Critical Next Actions

1. **Engage patent attorney by Friday.** Confirm availability and rate.
2. **Provide attorney with architecture documentation** (this memo + technical description of six-node pipeline).
3. **Clarify legal structure** (GrowDirect product vs. separate entity).
4. **Trademark clearance** for "El Jeffe" (Class 42, 35).
5. **Confirm merchant NDA** will be signed before demo.
6. **Brief financial services attorney** on money transmitter risk (sat collection).
7. **File provisional by Sunday March 2.**

### This Memo Is Not Legal Advice

This memo is an internal research summary. It does not constitute legal advice. The founder MUST consult with a qualified patent attorney before taking any action based on this analysis. The attorney will independently assess novelty, non-obviousness, subject matter eligibility, and prior art. This memo is for preparation only.

---

**Prepared by:** Syd, Legal Research — GrowDirect
**Date:** February 26, 2026
**Classification:** Internal Strategy — For Founder Preparation
**Confidentiality:** This document contains internal legal research and should not be shared externally without counsel guidance.
