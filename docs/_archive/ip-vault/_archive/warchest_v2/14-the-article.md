---
type: pitch
domain: business
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# The Article — From tLog to gLog

> *"The institution that owned the log could not be trusted to maintain it."*

---

## Part 1: The tLog Problem

IBM created the transaction log — the tLog — as the universal record of everything that happened at a point-of-sale terminal. For thirty years, the IBM 4690 format defined retail. Every sale, refund, void, and cash event began as a line in the tLog. IBM held the dominant position in grocery, drug, and mass merchant POS infrastructure throughout the 1990s and 2000s. The tLog was the industry standard payload.

It was also fundamentally broken.

The IBM 4690 operating system included a configuration called non-journal mode that dropped sequential transaction records without detection. In normal operation, the system produced gaps in the transaction sequence — records that simply vanished. No error. No alert. No trace. The data was gone, and nobody could tell it had ever existed.

The consequences were human. Loss Prevention departments relied on the tLog as the source of truth for employee activity. When records went missing — due to non-journal mode, hardware failures, or integration errors — LP interpreted the gaps as evidence of fraud. Employees were accused of stealing based on corrupted data. Careers were damaged. Livelihoods were threatened. The accusations were wrong, but the system provided no way to prove it.

One of the most damaging failures occurred when under-basket scanning technology was integrated into the 4690 platform. The integration created field length overflows in the packed hexadecimal BCD format — the encoding the tLog used for transaction data. Fields silently truncated. Records corrupted. Transactions vanished from the log. Loss Prevention flagged the missing records as theft.

It was not theft. It was a crashed field length in a fragile binary format that had never been designed for third-party integration.

The problem was never the people. The problem was the log.

---

## Part 2: The gLog Solution

> *"Event sourcing on the Bitcoin timechain. The transaction log made permanent."*

The gLog — Geoffrey's Log — is the permanent successor to the tLog. Where the tLog lived on institutional servers — mutable, deletable, and controlled by whoever owned the hardware — the gLog lives on Bitcoin.

Every transaction event at the point of sale generates a payload. That payload is processed through the elJeffe API at jeffe.io, where personal identifying information is cryptographically hashed before the event reaches the inscription layer. The sanitized event is then inscribed as an Ordinal on the Bitcoin timechain. Block height serves as a global timestamp that no entity controls. Each inscription references the previous one, creating an ordered chain of events for each merchant — a complete, replayable transaction history anchored to the most secure ledger ever created.

The architecture is event sourcing applied to the Bitcoin base layer:

1. **Event Capture** — POS generates a transaction event
2. **Hash and Seal** — PII is cryptographically hashed; the event is proven, the identity is protected
3. **Inscribe** — The hashed payload is inscribed as a Bitcoin Ordinal via the elJeffe API
4. **Chain** — Each inscription references the prior entry for that merchant
5. **Replay** — Start from any inscription point. Replay every event forward. Reconstruct exact POS state at any moment in history.

The gLog does not depend on any server remaining online. It does not require any institution to maintain it. The Bitcoin network has not experienced a single moment of downtime since January 3, 2009. Every gLog entry exists for the lifetime of the chain — permanently, immutably, and independently verifiable by anyone.

---

## Part 3: Compliance by Construction

> *"The gLog eliminates the mutable record — and with it, the entire class of vulnerabilities that compliance frameworks were designed to address."*

The compliance argument is architectural, not procedural.

Every major compliance framework in retail — PCI-DSS, SOX, CCPA, GDPR — was designed to address risks that arise from mutable records. Data that can be altered, deleted, or tampered with creates the entire class of vulnerabilities those frameworks regulate.

The gLog removes the mutable record from the equation:

- **PII is hashed before inscription.** Personal data never reaches Bitcoin. The on-chain record proves the event occurred without revealing who was involved.
- **The evidence store is INSERT-only.** No UPDATE. No DELETE. Enforced by database triggers. The application cannot alter sealed records even if compromised.
- **The audit trail is hash-chained.** Each entry includes the SHA-256 hash of the previous entry. Tamper with one record, the chain breaks downstream — the same principle that secures Bitcoin.
- **Bitcoin inscription is the final proof.** Block height is a global timestamp. The inscription proves what happened and when. No institutional attestation required.

This is not a claim that the gLog replaces compliance frameworks. Organizational controls, breach notification procedures, and data subject access rights exist independently. What the architecture eliminates is the technical attack surface — the mutable record that those frameworks were designed to protect.

Compliance by architecture, not compliance by policy.

---

## Part 4: The Through-Line

> *"I built the world's largest private database of retail sales data. I watched that data get locked in silos, disputed in courtrooms, and lost when companies changed hands. The problem was never the data — it was that the record was mutable."*

The career arc traces a single thread: thirty years spent understanding why records fail, and what it would take to make them permanent.

**Big Four Consulting** — Learned the discipline of enterprise retail at the feet of practitioners who invented it. First encountered the internet as a practitioner, not a consumer. Recognized the transformation it would bring to retail before most of the industry had a browser.

**Enterprise Systems** — Worked across the full enterprise retail stack. Participated in the US launch of a major international grocery chain's cashierless self-checkout format — a ~$1B build from whiteboard to 200 stores. The first cashierless self-checkout chain in the US.

**SaaS Pioneer** — Co-founded the platform that aggregated one of the largest private databases of retail transaction data in the industry. Built the LP case management, refund anomaly detection, executive analytics, and proximity network that are the direct ancestors of Canary's modules. The factory was acquired in 2016. The process was cut short.

**Bitcoin** — The SHA-256 connection: the same cryptographic standard underlying enterprise security certifications is the foundation of the Bitcoin ledger. For someone who grew up around audit — around the idea that an independent third party's signature on a record is the closest thing to truth — this was not an intellectual leap. It was a homecoming.

**GrowDirect** — The continuation. Give SMB retailers the enterprise-grade loss prevention infrastructure that only the largest chains have ever been able to afford. Built Bitcoin-native from day one. The founder pointed hash power at the network, earned a mining reward, and inscribed it as the Genesis Pool — 10 million permanently addressed slots in the verification layer of the post-AI internet.

The tLog was broken. The gLog fixes it. Not by trusting better institutions, but by removing the need for trust entirely.

The record lives on Bitcoin. Forever.

---

*GrowDirect Confidential*
*Patent Pending — Provisional 63/991,596*
