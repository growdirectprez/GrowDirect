---
type: pitch
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# References & Bibliography

> *Sources, standards, and prior art referenced throughout the GrowDirect Private Briefing.*

---

## Retail Loss Prevention Industry

### Market & Scale

- **National Retail Federation (NRF)** — *2024 National Retail Security Survey*. Annual shrinkage estimated at $112.1 billion in the US retail sector, with organized retail crime (ORC) accounting for a growing share.
- **Loss Prevention Research Council (LPRC)** — Ongoing research into retail crime patterns, detection methodologies, and technology adoption in loss prevention.
- **D&D Daily** — *Daily reporting on retail crime, loss prevention technology, and industry trends.*

### Enterprise Systems Heritage

- **IBM tLog (Transaction Log)** — The enterprise retail transaction logging standard that originated at IBM's retail division. Deployed across major retailers globally for point-of-sale audit and exception-based reporting. The conceptual ancestor of GrowDirect's gLog architecture.
- **Tesco TDS (Transaction Data Store)** — Tesco's proprietary evolution of the IBM tLog framework, incorporating supplier-facing analytics and loyalty program integration. The largest single-retailer implementation of transaction-level loss prevention analytics.
- **GSLM (Global Stock Loss Model)** — Academic and industry framework for classifying retail shrinkage by root cause (external theft, internal theft, process failure, supplier fraud). Informed CRDM's canonical source taxonomy.

---

## Bitcoin & Timechain Technology

### Protocol & Standards

- **Nakamoto, S. (2008)** — *Bitcoin: A Peer-to-Peer Electronic Cash System*. The foundational whitepaper establishing SHA-256 proof-of-work, UTXO model, and the timechain's immutability guarantees that underpin gLog inscription.
- **BIP-174 (Partially Signed Bitcoin Transactions)** — Standard for multi-party transaction construction relevant to Goose payment channel architecture.
- **Ordinals Protocol (Casey Rodarmor, 2023)** — Theory and specification for inscribing arbitrary data onto individual satoshis. The technical mechanism enabling gLog's permanent evidence inscription on the Bitcoin timechain.
- **Lightning Network (Poon & Dryja, 2016)** — *The Bitcoin Lightning Network: Scalable Off-Chain Instant Payments*. Payment channel network enabling Goose's micro-fee settlement layer.
- **L402 Protocol** — HTTP 402-based machine-to-machine payment protocol using Lightning macaroons. Proposed as gLog's API metering and data access control mechanism.

### Inscription & Data Integrity

- **Merkle, R. (1979)** — *Secrecy, Authentication, and Public Key Systems*. The Merkle tree data structure used in gLog's batch inscription model for aggregating multiple evidence hashes into a single timechain commitment.
- **RFC 6962 (Certificate Transparency)** — Merkle tree-based append-only log structure. Architectural parallel for gLog's evidence chain design.

---

## Data Architecture & Standards

### Retail Data Standards

- **ARTS (Association for Retail Technology Standards)** — *POSLog XML Standard*. Industry-standard schema for point-of-sale transaction data. CRDM's canonical source mapping draws from ARTS field definitions.
- **GS1** — *Global Standards for Business Communication*. Product identification (GTIN), location identification (GLN), and event tracking (EPCIS) standards referenced in CRDM's multi-POS translation layer.
- **Square Developer Platform** — *Square API Documentation*. Primary POS integration target. Webhook events, OAuth 2.0 authentication, and transaction data models inform Canary's capture pipeline design.

### Database & Architecture

- **Event Sourcing Pattern** — Architectural pattern where state changes are stored as an immutable sequence of events rather than mutable current-state records. Core design principle for gLog and the evidence chain.
- **CQRS (Command Query Responsibility Segregation)** — Separation of read and write operations into distinct models. Applied in Canary's three-database architecture (transactional, analytical, immutable).
- **Row-Level Security (RLS)** — PostgreSQL-native tenant isolation mechanism used in Canary's multi-tenant architecture to enforce merchant data boundaries at the database level.

---

## Legal & Compliance

### Regulatory Frameworks

- **Sarbanes-Oxley Act (SOX) Section 302/404** — Internal control and audit trail requirements. CRDM's INSERT-only evidence tables and hash chain verification are designed to satisfy SOX-equivalent data integrity standards.
- **GDPR (General Data Protection Regulation)** — EU privacy regulation. gLog's PII-hashing-before-inscription architecture directly addresses GDPR's right to erasure by ensuring no personal data reaches the timechain.
- **CCPA (California Consumer Privacy Act)** — California privacy law with similar PII protection requirements to GDPR. Canary's compliance-by-construction approach addresses both frameworks simultaneously.
- **PCI DSS (Payment Card Industry Data Security Standard)** — Cardholder data protection requirements. Relevant to Goose payment processing module design.

### Intellectual Property

- **US Provisional Patent Application No. 63/991,596** — Filed with the United States Patent and Trademark Office. Covers the staged immutability pipeline, triple-subscriber architecture, and bilateral verification methods described in these Materials.

---

## Industry Analogies Referenced

| Analogy | Context | Reference |
|---|---|---|
| VeriSign / DNS | gLog as a trust registry, analogous to VeriSign's role in internet certificate authority | Investment thesis — digital trust infrastructure |
| IP Address Ranges | Early block space acquisition compared to early internet IP range allocation — scarce, appreciating digital real estate | Investment thesis — block space moat |
| Guard Dog for Small Business | Canary LP as an always-on loss prevention system that SMBs can afford | Pitch narrative — product positioning |

---

## Internal Research Documents

The following internal research briefs inform the content of this briefing. These documents are not included in external distributions but are available for due diligence review upon request under NDA.

| Document | Scope |
|---|---|
| CRDM v1.0 Specification | Full schema specification — 7 canonical sources, field definitions, migration history |
| Staged Immutability Pipeline Analysis | Patent-relevant technical deep dive on the 6-node capture pipeline |
| Bitcoin Protocol Position Paper | Strategic analysis of Bitcoin as enterprise infrastructure |
| Competitive Landscape Analysis | Detailed competitive positioning against enterprise LP vendors |
| Micropayment Strategy Position Paper | Lightning Network fee economics and metering model |
| Volume Analysis (Inscription Economics) | Cost modeling for gLog inscription at scale |

---

*Last updated: February 27, 2026*
*GrowDirect Confidential — Patent Pending — Provisional 63/991,596*
