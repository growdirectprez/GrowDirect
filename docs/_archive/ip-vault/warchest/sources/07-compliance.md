---
type: pitch
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Compliance

> *"The gLog eliminates the mutable record — and with it, the entire class of vulnerabilities that compliance frameworks were designed to address."*

---

## Compliance by Construction

Traditional compliance is a policy exercise. Hire auditors. Write policies. Run assessments. Maintain documentation. Hope the system works as described. When it does not, remediate.

The gLog architecture takes a different approach: **eliminate the attack surface at the architecture level**, so the entire class of vulnerabilities that compliance frameworks address cannot occur.

---

## The Architecture Argument

Every compliance framework in retail — PCI-DSS, SOX, CCPA, GDPR — was designed to address risks that arise from mutable records. Specifically:

| Risk | Framework | gLog Architecture Response |
|---|---|---|
| **Data can be altered after the fact** | SOX Section 302/404 | Transaction records are inscribed on Bitcoin. The inscription is permanent and independently verifiable. |
| **PII can be exposed in storage** | PCI-DSS, CCPA, GDPR | PII is cryptographically hashed before the event reaches the inscription layer. Personal data never touches Bitcoin. |
| **Audit trails can be tampered** | SOX, PCI-DSS | Every audit entry includes the SHA-256 hash of the previous entry. Break one, the chain breaks downstream. |
| **Records can be deleted** | GDPR Right to Erasure | On-chain records contain hashed data only — no PII to erase. The operational database handles erasure requests independently. |
| **Chain of custody can be disputed** | Legal/evidentiary | Block height serves as a global timestamp. The inscription proves what happened and when. No institutional attestation required. |

---

## How PII Protection Works

The gLog does not put personal data on Bitcoin. It puts proof on Bitcoin.

```
POS Event (contains PII: customer name, card last-4, employee ID)
    │
    ▼
elJeffe API receives the raw payload
    │
    ▼
Privacy Module: SHA-256 hash strips all PII
    │
    ├─► Hashed event → sealed in evidence store (INSERT-only)
    ├─► Hashed event → batched into Merkle tree
    └─► Merkle root → inscribed as Bitcoin Ordinal
         │
         └─► On-chain: cryptographic proof, zero PII
```

The privacy module is not optional. It is a mandatory step in the six-node pipeline. Every event is hashed before it reaches the inscription layer. The result: the on-chain record proves the event occurred, when it occurred, and in what sequence — without revealing who was involved.

---

## What This Means for Specific Frameworks

### PCI-DSS
The gLog stores no cardholder data on-chain. The evidence store uses SHA-256 hashing on all PII fields. The operational database implements encryption at rest and in transit per PCI requirements. The architecture separates the proof layer (Bitcoin) from the data layer (encrypted PostgreSQL).

### SOX (Sarbanes-Oxley)
Financial transaction records are append-only — no UPDATE, no DELETE. The hash chain provides cryptographic tamper detection. Bitcoin inscription provides an independent timestamp that no internal system can alter. This addresses the internal controls requirements of Sections 302 and 404.

### CCPA / GDPR
PII exists only in the operational database, where standard erasure and access request workflows apply. The on-chain record contains hashed proofs only — no personal data to erase, no data subject access request to fulfill. The architecture is designed so that right-to-erasure compliance and proof-of-event permanence are not in conflict.

---

## What This Does NOT Claim

The gLog addresses data integrity and retention at the architecture level. It does not:

- Replace organizational compliance controls
- Eliminate the need for compliance officers or auditors
- Satisfy all requirements of any framework automatically
- Replace breach notification procedures
- Address data subject access rights (those are handled by the operational database)

Compliance by architecture addresses the technical controls. Organizational, procedural, and disclosure requirements exist independently and must be maintained.

---

## The Bottom Line

Most compliance programs are retroactive — they detect problems after the fact and remediate. The gLog architecture is proactive — it eliminates the class of problems those programs were designed to detect.

The mutable record is the root cause. Remove it, and the entire attack surface changes.

---

*GrowDirect Confidential*
*Patent Pending — Provisional 63/991,596*
