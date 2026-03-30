---
type: legal
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Patent Utility Prep Brief v1.0

**Prepared by:** Legal Counsel
**Date:** March 3, 2026
**Classification:** CONFIDENTIAL — Attorney Work Product
**Reference:** U.S. Provisional Patent Application No. 63/991,596
**Filed:** February 26, 2026
**Utility Deadline:** February 26, 2027 (12 months from provisional)
**Inventor:** Geoffrey C. Lyle
**Entity Status:** Micro Entity

---

## 1. Claim-to-Diagram Matrix

Each provisional claim is mapped to the specific patent figure(s) that illustrate the claimed invention. All figures are from the patent diagram set produced March 3, 2026.

| Claim | Description | Primary FIG | Supporting FIG(s) | Protocol Spec Reference |
|-------|-------------|-------------|-------------------|------------------------|
| **1** | Universal event notarization via cryptographic hash inscription on a PoW time chain, applied to any webhook-originated event stream | FIG. 1 (Six-Node Architecture v3.0) | FIG. 2 (Data Flow), FIG. 6 (Rebuild/Recovery) | elJeffe Protocol Spec §1–§3: Genesis, Namespace, Merkle Batch inscription types |
| **2** | Cryptographic key custody of a canonical inscription pool; custodying entity controls the authoritative notarization record and validation thereof | FIG. 5 (Namespace Lifecycle) | FIG. 4 (Data Sovereignty Stack) | elJeffe Protocol Spec §4: Namespace authority model, Genesis inscription key binding |
| **3** | Micropayment-gated validation of event notarizations against the canonical inscription record, denominated in native currency of the time chain, processed via L2 payment protocol | FIG. 1 (Verification Service node) | FIG. 4 (Verification tier) | elJeffe Protocol Spec §5: RaaS API, L402 paywall, Lightning micropayments |
| **4** | Programmatic scaling of the inscription pool in response to notarization volume thresholds, using treasury assets to purchase additional block space | FIG. 1 (Inscription Service node) | FIG. 5 (Operational batching) | elJeffe Protocol Spec §6: Treasury protocol, DAO governance, auto-scaling rules |
| **5** | Merkle batching method — multiple event hashes aggregated into a Merkle tree, root inscribed as single canonical record, each event independently verifiable via Merkle proof path | FIG. 3 (Triple Subscriber — Inscribe path) | FIG. 2 (Merkle aggregation step), FIG. 6 (Merkle verification in recovery) | elJeffe Protocol Spec §3.3: merkle_batch inscription type, batch metadata, chain linkage |

### Diagram Coverage Assessment

| Figure | Claims Supported | Utility Filing Role |
|--------|-----------------|-------------------|
| FIG. 1: Six-Node Architecture v3.0 | 1, 3, 4 | Primary system overview — ESSENTIAL for all claims |
| FIG. 2: Single Transaction Data Flow | 1, 5 | Detailed flow for Claims 1 and 5 — shows hash-at-ingress |
| FIG. 3: Triple Subscriber Component | 5 | Core novelty diagram — the TSP fan-out is the architectural innovation |
| FIG. 4: Data Sovereignty Stack | 2, 3 | Trust hierarchy — supports custody claim and verification claim |
| FIG. 5: Namespace Lifecycle | 2, 4 | Genesis → operational batching lifecycle — supports custody and scaling |
| FIG. 6: Rebuild & Recovery Path | 1, 5 | Recovery capability — demonstrates independent verifiability (Claim 1) and Merkle proof (Claim 5) |

**Gap identified:** No standalone figure currently illustrates the L402 Lightning paywall mechanism (Claim 3). Recommend adding FIG. 7 showing the verification request flow: Verifier → L402 Challenge → Lightning Payment → Merkle Proof Response.

---

## 2. Prior Art Differentiation

### Claim 1: Universal Event Notarization

**Known prior art:**
- Blockchain timestamping services (OpenTimestamps, OriginStamp) — timestamp arbitrary data on Bitcoin
- Document notarization platforms (Stampery, Factom) — notarize specific document types

**Differentiation:** The claimed system is *universal* across event sources (any webhook), performs hashing *at the point of ingestion* (before any processing), and maintains a *three-store architecture* where the inscription is one of three independent persistence paths. Existing timestamping services operate as single-path systems: data in → hash → Bitcoin. The claimed system's Triple Subscriber Pattern creates three independent records from a single event, with the inscription being a *consequence* of the evidence pipeline, not the sole purpose of the system.

**Strength:** Strong. The combination of source-agnostic ingestion, hash-at-gateway, and three-store independence is not anticipated by any single prior art reference.

### Claim 2: Key Custody of Canonical Inscription Pool

**Known prior art:**
- Blockchain-based identity systems (Sovrin, ION, Handshake) — namespace management on chain
- Certificate authorities — centralized key custody for identity validation

**Differentiation:** The claimed system uses a *pseudonymous GUID namespace on Layer 1* with *optional human-readable aliases on Layer 2*. The custodying entity controls the inscription authority (via the genesis inscription's public key) but does not control or even know the merchant's real-world identity. The namespace system operates as a *privacy-by-default identity layer* where participants are pseudonymous unless they opt in to disclosure. Existing blockchain identity systems (Sovrin, ION) are designed to *establish* identity; this system is designed to *protect* identity while still providing verification capability.

**Strength:** Strong. The L1 GUID / L2 alias split is architecturally distinct from all examined prior art.

### Claim 3: Micropayment-Gated Validation

**Known prior art:**
- L402 (formerly LSAT) protocol for Lightning-gated APIs — exists as protocol standard
- Pay-per-query APIs — common in data services

**Differentiation:** The combination of L402 Lightning micropayments with *verification of cryptographic proof against a canonical inscription record* is novel. Existing L402 implementations gate access to content or APIs. This system gates access to a *verification service* that produces a cryptographic proof response (Merkle proof path) derived from on-chain data. The revenue from verification funds inscription, creating a self-sustaining loop. No examined prior art implements this closed economic circuit.

**Strength:** Moderate-Strong. The L402 protocol itself is prior art, but its application to inscription verification with treasury reinvestment is novel. Counsel should strengthen the language around the closed economic loop.

### Claim 4: Programmatic Scaling via Treasury

**Known prior art:**
- DAO treasury management (MakerDAO, Compound) — algorithmic treasury operations
- Auto-scaling cloud infrastructure — programmatic resource allocation

**Differentiation:** The claimed system uses a *protocol-governed treasury* that purchases Bitcoin *block space* (a physically constrained resource) in response to notarization volume. This is not cloud auto-scaling (elastic, virtual). Block space is a real physical constraint created by proof-of-work mining. The treasury's purchasing decision is governed by transparent protocol rules, not administrative discretion. No examined prior art implements programmatic block space acquisition for commercial notarization purposes.

**Strength:** Moderate. This claim may face obviousness challenges. Recommend strengthening by emphasizing the physical constraint aspect (PoW block space is non-elastic, unlike cloud resources) and the protocol governance mechanism.

### Claim 5: Merkle Batching Method

**Known prior art:**
- Merkle tree aggregation — fundamental computer science (Merkle, 1979)
- Batch inscription on Bitcoin — OpenTimestamps uses Merkle aggregation

**Differentiation:** The claimed method combines Merkle batching with *chain linkage* (each batch inscription references its predecessor, creating a verifiable chain), *self-describing inscription format* (all verification metadata is embedded in the inscription itself), and *independence from any server for verification* (a verifier needs only the Bitcoin chain and the genesis public key). OpenTimestamps requires calendar servers for proof retrieval. The claimed system's inscriptions are self-contained.

**Strength:** Moderate. The Merkle batching alone is well-known. The strength is in the *self-describing, server-independent* property combined with chain linkage. Counsel should emphasize these differentiators in the utility claims.

---

## 3. Alice Defense Strategy

### 35 U.S.C. § 101 — Subject Matter Eligibility

The most significant risk to this patent is an Alice/Mayo challenge arguing the claims are directed to an abstract idea (data storage, record-keeping) implemented on generic computer hardware.

### Step 1: Is the Claim Directed to an Abstract Idea?

**Defense position:** No. The claims are directed to a *specific technical solution* that produces *physically anchored results*. The system does not merely "store data" — it creates a *thermodynamically irreversible cryptographic proof* by inscribing on a proof-of-work blockchain. The proof-of-work requirement means each inscription represents a measurable expenditure of physical energy. The claimed system converts commercial events into *physical artifacts* on the Bitcoin time chain — artifacts whose existence is guaranteed by the cumulative hash rate of the Bitcoin network (currently ~700 EH/s).

**Key argument:** The inscription is not a database entry. It is a record secured by the largest computational network in human history, requiring billions of dollars in mining hardware and energy to maintain. The act of inscription transforms an ephemeral digital event into a *physically anchored proof* that cannot be altered without re-doing the work of every subsequent block — a thermodynamic impossibility at scale.

### Step 2: Even if Abstract, Is There an Inventive Concept?

**Defense position:** Yes. Multiple inventive concepts:

1. **Triple Subscriber Pattern** — A novel architectural pattern that creates three independent records from a single event, with distinct mutability guarantees at each tier. This is not a generic "store data in three places" instruction. The three subscribers have specifically defined persistence properties (write-once, replayable, batched inscription) and independent failure domains.

2. **Self-describing inscription format** — The protocol produces inscriptions that contain all metadata required for verification without reference to any external server. This is a specific technical improvement over prior art timestamping services that require server cooperation for proof retrieval.

3. **Pseudonymous namespace with opt-in identity** — The L1 GUID / L2 alias architecture creates a specific technical mechanism for privacy-by-default commercial participation with controlled disclosure.

4. **Closed economic loop** — The system produces a measurable, physically verifiable economic result: micropayment revenue from verification services funds inscription costs, creating a self-sustaining system. This is not an abstract business method — it is a specific technical implementation using Lightning Network payment channels and L402 protocol gating.

### Recommended Claim Strengthening for Utility Filing

- Add specific technical detail to each claim: hash algorithm (SHA-256), inscription protocol (Ordinals), payment protocol (Lightning/L402), database enforcement mechanism (PostgreSQL triggers)
- Include dependent claims that narrow to specific architectural choices (e.g., the evidence store uses INSERT-only tables with trigger-enforced immutability)
- Reference the physical properties of PoW explicitly in Claim 1 language
- Add claims covering the recovery method (FIG. 6) — ability to reconstruct from chain alone is a specific technical capability

---

## 4. GUID Namespace Amendment (GRO-58 Impact)

### What Changed

The protocol was amended (GRO-58, March 2026) to use a GUID-based namespace on Layer 1 instead of a human-readable namespace. Human-readable aliases now exist only on Layer 2 (application layer).

### IP Implications

**Positive:**
- Strengthens the privacy claim — GUID on L1 means *no personally identifiable information* exists on the Bitcoin chain, period
- Strengthens Alice defense — the GUID namespace is a *specific technical mechanism*, not an abstract concept
- Expands Claim 2 — the custody claim now covers *pseudonymous identity management*, a more defensible position than named identity management

**Action Required:**
- The utility filing MUST incorporate the L1 GUID / L2 alias architecture as the primary namespace implementation
- The provisional may reference human-readable namespaces; the utility should clarify that L1 namespaces are GUID-only
- Consider adding a new dependent claim specifically covering the two-layer identity architecture (L1 pseudonymous, L2 opt-in disclosure)

**Risk:**
- None identified. The GUID amendment *strengthens* the patent position. No prior art implications.

---

## 5. Utility Filing Priorities

### Must-Have Before Filing (Priority 1)

1. **Expanded claim set** — The provisional has 5 independent claims. The utility should add 15–20 dependent claims that narrow each independent claim to specific technical implementations. This is standard practice and significantly strengthens the patent.

2. **Detailed specification** — The utility requires a full technical specification at a level of detail that would allow a person skilled in the art to reproduce the invention. The Protocol Spec (elJeffe_Protocol_Spec_v1.0.md) and the Academic Research Paper (GRO-59) provide this material. Patent counsel will reformat.

3. **Formal drawing set** — The 7 HTML patent diagrams must be converted to formal patent drawing format (black and white, numbered reference elements, figure descriptions). This is a mechanical process that patent counsel or a patent illustrator will handle.

4. **Prior art search** — A professional prior art search covering USPTO, EPO, WIPO, and relevant non-patent literature. This should be conducted by patent counsel or a dedicated search firm. Budget estimate: $2,000–$5,000.

### Should-Have (Priority 2)

5. **Working prototype documentation** — Canary LP serves as the working prototype. QA test results, integration test logs, and acceptance criteria verification provide evidence of reduction to practice. Compile before filing.

6. **Additional embodiment detail** — The provisional names six embodiments (Retail, Healthcare, Supply Chain, Legal, Insurance, Government). The utility should include 1–2 paragraphs per embodiment with specific examples of event types, source networks, and verification scenarios.

### Nice-to-Have (Priority 3)

7. **International filing strategy** — PCT application to preserve international rights. Must be filed within 12 months of provisional (same deadline as utility). Consider if international protection is warranted given the business plan.

8. **Continuation-in-part** — If significant new claims emerge from the Canary LP implementation, a CIP may be appropriate. Discuss with counsel.

---

## 6. Counsel Engagement Recommendation

### Attorney Profile

**Required specialization:** Patent prosecution in software/systems architecture, preferably with blockchain or cryptography patent experience. Must understand:
- 35 U.S.C. § 101 Alice/Mayo analysis for software patents
- Ordinals/Bitcoin as a technical substrate (not just "blockchain")
- System architecture claims (not just algorithm claims)

**Preferred:**
- Experience with micro entity filings (cost structure matters)
- Track record of successfully prosecuting software patents post-Alice
- Willingness to work from detailed technical specifications (we provide the substance; they provide the legal formatting)

### What NOT to Look For

- Do not engage a generalist IP attorney who "also does patents"
- Do not engage a patent mill that files high-volume, low-quality applications
- Do not engage counsel who immediately recommends broadening claims without reading the technical specification first

### Engagement Timeline

| Milestone | Target Date | Notes |
|-----------|-------------|-------|
| Identify 3–5 candidates | April 2026 | Initial outreach, confirm blockchain patent experience |
| Selection + engagement | May 2026 | NDA, retainer, share technical package |
| Prior art search commissioned | May–June 2026 | Professional search, 4–6 week turnaround |
| Claim drafting + specification review | June–September 2026 | Iterative process, expect 3–4 rounds |
| Internal review | October 2026 | Inventor review of final claims |
| Utility filing | November–December 2026 | Buffer before February 2027 deadline |
| PCT filing (if pursuing) | Before February 26, 2027 | Same 12-month window |

### Budget Estimate

| Item | Estimate | Notes |
|------|----------|-------|
| Prior art search | $2,000–$5,000 | Professional search firm |
| Utility patent prosecution | $8,000–$15,000 | Drafting + filing + prosecution (micro entity) |
| USPTO filing fees (micro) | $800–$1,200 | Micro entity rates |
| Patent drawings | $500–$1,500 | 7 figures, formal format |
| PCT filing (optional) | $3,000–$5,000 | If international protection desired |
| **Total (without PCT)** | **$11,300–$22,700** | |
| **Total (with PCT)** | **$14,300–$27,700** | |

### Technical Package for Counsel

The following documents should be provided to patent counsel at engagement:

1. U.S. Provisional Application 63/991,596 (as filed)
2. elJeffe Protocol Spec v1.0 (`Canary_IP/Markdown/Specs/elJeffe_Protocol_Spec_v1.0.md`)
3. Academic Research Paper v1.0 (`_ALX/WorkOrders/output/PhD/GrowDirect_AcademicResearchPaper_v1.0.docx`)
4. This Patent Utility Prep Brief
5. All 7 patent diagrams (HTML format; counsel will commission formal drawings)
6. Canary LP acceptance criteria and QA results (when available)

---

## Appendix: Quick Reference — Claims to Source Material

| Claim | War Chest Source | Protocol Spec Section | Academic Paper Section |
|-------|-----------------|----------------------|----------------------|
| 1 | 33-the-patent.md | §1–§3 | Part B §7 (Six-Node Pipeline) |
| 2 | 33-the-patent.md, 42-sovereignty.md | §4 (Namespace) | Part A §4 (Opt-In Identity), Part B §10 (elJeffe Protocol) |
| 3 | 48-investment-thesis.md | §5 (RaaS API) | Part A §5 (Economic Loop), Part B §7 (Verification Service) |
| 4 | 55-dao-treasury-protocol.md | §6 (Treasury) | Part A §5 (Self-Sustaining Loop) |
| 5 | 33-the-patent.md | §3.3 (merkle_batch) | Part B §8 (Triple Subscriber), Part B §12 (Rebuild) |

---

*GrowDirect Inc. | Canary LP | Confidential — Attorney Work Product*
