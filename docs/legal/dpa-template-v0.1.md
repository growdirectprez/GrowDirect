# Data Processing Agreement — Canary Protocol (v0.1)

**Status:** v0.1 working document — not executed. Outside-counsel review required before any merchant signature.
**Owner:** GrowDirect LLC (Canary Protocol)
**Last reviewed:** 2026-05-02
**Source dispatch:** GRO-693
**Related:** [Subprocessor List v0.1](./subprocessor-list-v0.1.md) · [Breach Runbook v0.1](./breach-runbook-v0.1.md) · [IR Plan v0.1](./ir-plan-v0.1.md)

---

## 0 · Governing thesis

This DPA reflects three architectural commitments that distinguish Canary from generic SaaS processors:

1. **Canary is the merchant's processor — never their data's controller.** Every clause is written from the position that the merchant is the GDPR Article 28 controller and Canary executes on their instructions.
2. **Card data never crosses the Canary boundary.** PAN/track/CVV flow pinpad → processor (Phase 4 architecture); Canary holds the merchant's operating data, not their card data. The PCI surface is therefore minimal Service Provider scope at Phase 4 — see §7.4.
3. **Evidence is cryptographically anchored.** Every payload received and every record of consequence is hash-anchored to a public Bitcoin L2 (USPTO Application 63/991,596). Tampering with the evidence chain after the fact is detectable. This is a security measure (§7.3) and a forensic asset (breach-runbook-v0.1.md).

This template is GDPR Article 28-compliant by design and adapts to US state regimes via the governing-law variant clauses in §11.

---

## 1 · Parties

| Role | Identity |
|---|---|
| Controller | The merchant entity executing the Canary order form (the **Merchant**) |
| Processor | GrowDirect LLC, a California limited liability company, dba Canary Protocol (**Canary**) |
| Subprocessors | Listed in [`subprocessor-list-v0.1.md`](./subprocessor-list-v0.1.md), incorporated by reference |

[COUNSEL REVIEW] — Confirm the GrowDirect LLC entity is the correct contracting party (vs. Canary-specific subsidiary if one is formed). Confirm DBA registration is current.

---

## 2 · Definitions

Defined terms track GDPR Article 4 and CCPA §1798.140 where they overlap. Material terms:

| Term | Meaning in this DPA |
|---|---|
| Personal Data | Any information relating to an identified or identifiable natural person, as defined in GDPR Art. 4(1) and including "personal information" under CCPA §1798.140(v) |
| Processing | Any operation performed on Personal Data, per GDPR Art. 4(2) |
| Data Subject | The natural person to whom Personal Data relates |
| Service | The Canary Protocol platform as described in the order form |
| Sub-processor | Any third party engaged by Canary to process Personal Data on the Merchant's behalf |
| Merchant Data | All data the Merchant transmits to or generates within the Service, including Personal Data |
| Security Incident | Any breach of security leading to accidental or unlawful destruction, loss, alteration, unauthorized disclosure of, or access to, Personal Data |

---

## 3 · Roles and processing scope

| Element | Specification |
|---|---|
| Controller | Merchant |
| Processor | Canary |
| Categories of Data Subjects | Merchant employees · Merchant customers (when loyalty / receipts / returns flow through) · Vendors of the Merchant (when invoicing / receiving flows through) |
| Categories of Personal Data | Identification (name, employee ID, customer email/phone) · Transaction data (purchase history, basket detail) · Financial (transaction amounts; **never** PAN/track/CVV — see §7.4) · Behavioral (loyalty events, dispute records) · Operational (timestamps, location of transaction, device ID) |
| Processing Purposes | Loss prevention analytics · Inventory and merchandising operations · Open-to-buy financial control · Receipt/transaction routing · Evidence-chain anchoring for audit |
| Processing Duration | Term of the order form plus the deletion window in §10 |
| Nature of Processing | Automated processing including detection rule evaluation, agent-driven decisioning, and cryptographic hash anchoring |
| Cross-border Transfer | Permitted under SCCs (§9) |

---

## 4 · Merchant instructions

Canary processes Personal Data only on documented instructions from the Merchant. The order form, this DPA, and the Service documentation constitute those instructions. Canary informs the Merchant if, in its opinion, an instruction violates applicable law (GDPR Art. 28(3)(h)).

---

## 5 · Canary obligations

| § | Obligation | GDPR / CCPA reference |
|---|---|---|
| 5.1 | Process only on Merchant's documented instructions | GDPR Art. 28(3)(a) |
| 5.2 | Ensure persons authorized to process are bound by confidentiality | GDPR Art. 28(3)(b) |
| 5.3 | Implement security measures per §7 | GDPR Art. 28(3)(c), Art. 32 |
| 5.4 | Engage subprocessors only per §8 | GDPR Art. 28(3)(d) |
| 5.5 | Assist Merchant in responding to Data Subject requests | GDPR Art. 28(3)(e); CCPA §1798.105 |
| 5.6 | Assist Merchant with DPIAs and consultations | GDPR Art. 28(3)(f), Art. 35-36 |
| 5.7 | Delete or return Personal Data per §10 | GDPR Art. 28(3)(g) |
| 5.8 | Make available information necessary to demonstrate compliance, including audit access | GDPR Art. 28(3)(h); see §6 |

---

## 6 · Audit rights

| Element | Specification |
|---|---|
| Frequency | One audit per calendar year, plus reasonable additional audits triggered by a Security Incident or regulator inquiry |
| Notice | 30 days' written notice for routine audits; immediate access for incident-triggered audits |
| Scope | Canary's compliance with this DPA and with the published security measures (§7) |
| Format | Documentary review of SOC 2 Type II / ISO 27001 reports (when available — see §7.5) is the default. On-site audit available for regulator-driven or incident-driven cases |
| Cost | Merchant bears the cost of audits unless the audit reveals material non-compliance, in which case Canary bears reasonable costs |
| Confidentiality | Auditor must execute Canary's NDA before access |
| **Evidence chain** | Canary's hash-anchored evidence chain (Application 63/991,596) is available to Merchant on request as a continuous attestation surface — every consequential record is anchored to public Bitcoin L2, providing a forensic record independent of either party |

[COUNSEL REVIEW] — Confirm 30-day notice is consistent with industry baseline. Some EU customers ask for 14 days. Confirm "auditor must be a qualified third party not in competition with Canary" language is sufficient.

---

## 7 · Security measures

Canary maintains technical and organizational measures appropriate to the risk, per GDPR Art. 32. The measures below are the contractual floor.

### 7.1 · Technical controls

| Control | Implementation |
|---|---|
| Encryption in transit | TLS 1.3 minimum for all merchant-facing endpoints (`api.canary.growdirect.io` and successors) |
| Encryption at rest | AES-256 for all persistent storage (Cloud SQL Postgres, Cloud Storage, Pub/Sub at-rest encryption) |
| Key management | Google Cloud KMS with HSM-backed keys; access logged via Cloud Audit Logs |
| Network segmentation | VPC with private service connect; service accounts scoped per workload; no public-facing databases |
| Access control | IAM with least-privilege roles; service account JSON key creation blocked at org level (`iam.disableServiceAccountKeyCreation`); admin access via Workload Identity Federation only |
| Logging | Cloud Audit Logs retained per regulatory minimum; immutable application audit log anchored to evidence chain (§7.3) |
| Vulnerability management | Continuous dependency scanning; quarterly penetration testing once SOC 2 program is active (§7.5) |

### 7.2 · Organizational controls

| Control | Implementation |
|---|---|
| Access provisioning | Documented role-based access; reviewed quarterly |
| Background checks | Required for all personnel with production access |
| Confidentiality | All personnel and subprocessors bound by written confidentiality obligations (§5.2) |
| Training | Security and privacy training at onboarding and annually |
| Incident response | Per [`ir-plan-v0.1.md`](./ir-plan-v0.1.md) and [`breach-runbook-v0.1.md`](./breach-runbook-v0.1.md) |

### 7.3 · Evidence-chain integrity (Canary-specific control)

Every consequential record (Fox case generation and status transition, OTB commitment, audit-log entry of regulatory significance) publishes a cryptographic hash to a public Bitcoin Layer-2. This is a security control (tampering detection) and a forensic control (independent timestamping of the chain of custody). Reference: USPTO Application 63/991,596.

The merchant retains audit access to the chain via the merchant portal. Hash verification can be performed independently — Canary's cooperation is not required to validate the chain.

### 7.4 · PCI-DSS scope (Phase 4 posture)

Cardholder data (PAN, track data, CVV) **does not flow through Canary.** Card data flows pinpad → payment processor directly; Canary receives only the post-authorization transaction record (amount, tender type, last-4, fingerprint).

At Phase 4 of the Canary build (full SaaS scope — see GRO-700 series), Canary becomes a PCI Service Provider with **minimal scope** — the processing-environment boundary excludes cardholder data. The annual SAQ-D for Service Providers will reflect this minimal scope.

[COUNSEL REVIEW] — Confirm "minimal Service Provider scope" framing is acceptable to a QSA before publishing this clause to merchants. Coordinate with GRO-695 (QSA engagement).

### 7.5 · Compliance certifications

| Certification | Status | Target |
|---|---|---|
| SOC 2 Type II | Not yet certified | Phase 4 launch (per GRO-733) |
| ISO 27001 | Not yet certified | Phase 4 launch |
| PCI-DSS Service Provider (SAQ-D) | Not yet attested | Phase 4 launch |
| GDPR Article 32 self-assessment | Documented in §7.1-7.3 | Continuous |

[COUNSEL REVIEW] — Confirm whether to include "intent to certify" language or only certifications actually held. EU customers will press on this; conservative position is to claim only what we can prove.

---

## 8 · Sub-processors

| § | Term |
|---|---|
| 8.1 | The Merchant authorizes Canary to engage the sub-processors listed in [`subprocessor-list-v0.1.md`](./subprocessor-list-v0.1.md) |
| 8.2 | Canary will provide **30 days' prior written notice** of any new or replacement sub-processor by updating the subprocessor list and notifying the Merchant via the contact on the order form |
| 8.3 | The Merchant may object to a new sub-processor on reasonable data-protection grounds within 14 days. If the parties cannot resolve the objection, the Merchant may terminate the affected portion of the Service with pro-rated refund |
| 8.4 | Canary remains liable for sub-processor performance |
| 8.5 | Canary will execute a written agreement with each sub-processor imposing data-protection obligations no less protective than those in this DPA |

[COUNSEL REVIEW] — 30-day notice is the industry baseline for SaaS DPAs (Salesforce, Stripe, etc.). Some EU regulators prefer 60 days. Confirm 30 days is defensible.

---

## 9 · International transfers

For transfers of Personal Data from the EEA, UK, or Switzerland to a country without an adequacy decision:

| § | Term |
|---|---|
| 9.1 | The parties incorporate the Standard Contractual Clauses (Module 2: Controller-to-Processor) adopted by the European Commission on 4 June 2021 by reference |
| 9.2 | The UK International Data Transfer Addendum applies to UK transfers |
| 9.3 | Annex I (parties / data subjects / categories) is populated from §1 and §3 of this DPA |
| 9.4 | Annex II (technical and organizational measures) is populated from §7 of this DPA |
| 9.5 | Annex III (sub-processors) is populated from `subprocessor-list-v0.1.md` |
| 9.6 | Where Swiss data is involved, references to GDPR are read to include the Swiss FADP |

[COUNSEL REVIEW] — SCCs are referenced rather than reproduced. Confirm reference-by-incorporation is acceptable in target EU jurisdictions vs. requiring full SCC text appended as Annex.

---

## 10 · Deletion and return

| § | Term |
|---|---|
| 10.1 | Within 30 days of termination, the Merchant may export Merchant Data via the Service's standard export mechanism |
| 10.2 | Within 90 days of termination, Canary will delete or return all Merchant Data, including from active systems and routine backups |
| 10.3 | Backup tapes / immutable storage layers are purged on the standard rotation schedule (no longer than 365 days post-termination) |
| 10.4 | **Evidence-chain anchor records** persist permanently on the public Bitcoin L2 by design. The chain stores cryptographic hashes only — no Personal Data. The Merchant acknowledges that hash anchors are not deletable and do not constitute Personal Data under GDPR Art. 4 |
| 10.5 | Canary will provide written confirmation of deletion within 14 days of completion |

[COUNSEL REVIEW] — Confirm the position that "hashes are not Personal Data" is defensible in EU jurisdictions. A hash of a hash of an event record, with no possibility of reversal to PII, should not be Personal Data — but EU regulators have taken expansive views on this. Counsel should confirm or recommend a hash-only-of-hashes-of-non-PII structure.

---

## 11 · Governing law variants

The order form selects one of the following variants. The selected variant supersedes any conflicting term in the order form.

### 11.1 · US (default — Delaware)

This DPA is governed by the laws of the State of Delaware, USA, without reference to conflict-of-law principles. Disputes are resolved in the state and federal courts of Wilmington, Delaware. Each party waives jury trial.

### 11.2 · California (when Merchant has California operations)

For Personal Data subject to CCPA / CPRA: Canary acts as a "service provider" or "contractor" as defined in §1798.140. Canary will not (i) sell or share Personal Data, (ii) retain, use, or disclose Personal Data outside the direct business purpose, or (iii) combine Personal Data with data from other sources. Disputes governed by California law per §11.1 election.

### 11.3 · EU/EEA (when Merchant is established in EEA)

This DPA is governed by the laws of Ireland. Disputes are resolved in the courts of Dublin. The SCCs in §9 are governed by the law of the EU member state in which the Merchant is established.

### 11.4 · UK

Governed by the laws of England and Wales; courts of London.

[COUNSEL REVIEW] — Delaware default is conventional for US SaaS. EU default (Ireland) is conventional for SCC enforcement. UK separation is post-Brexit standard. Confirm with counsel that we are not creating a tax nexus by selecting Ireland (we are not establishing operations there, only contractual jurisdiction).

---

## 12 · Liability

Liability is governed by the master agreement (order form). This DPA does not create independent caps. Where the master agreement is silent, liability for breach of this DPA is capped at fees paid in the 12 months preceding the claim, except for breaches of confidentiality, breaches caused by gross negligence or willful misconduct, or amounts owed to regulators or Data Subjects under GDPR Art. 82.

[COUNSEL REVIEW] — Cap structure must be coordinated with the master agreement. Counsel should review whether the GDPR Art. 82 carve-out is enforceable and whether confidentiality should also be uncapped.

---

## 13 · Term and termination

This DPA is co-terminous with the order form. §10 (deletion) survives termination. §6 (audit) survives for 12 months post-termination. §7.3 (evidence chain) survives indefinitely as to records anchored during the term — the chain is by design immutable.

---

## 14 · Notices

Notices to Canary: `legal@growdirect.io` with copy to the contact on the order form.
Notices to Merchant: contact on the order form, with copy to any address designated in writing.

[COUNSEL REVIEW] — Confirm `legal@growdirect.io` is provisioned and monitored. If not, route to founder + counsel until provisioned.

---

## Counsel Review Required (consolidated)

The following clauses require outside-counsel review before this template is offered to merchants:

1. **§1 entity confirmation** — GrowDirect LLC vs. Canary subsidiary, DBA registration
2. **§6 audit notice period** — 30 days vs. EU baseline of 14
3. **§7.4 PCI scope language** — coordinate with QSA engagement (GRO-695)
4. **§7.5 compliance certifications** — "intent to certify" vs. only-what-we-hold
5. **§8 sub-processor notice period** — 30 days vs. EU baseline of 60
6. **§9 SCCs by reference** — reference-vs.-reproduce in target jurisdictions
7. **§10.4 hashes-not-PII** — defensibility in EU jurisdictions
8. **§11 governing law variants** — Ireland tax nexus risk
9. **§12 liability cap** — coordination with master agreement; GDPR Art. 82 carve-out enforceability
10. **§14 notices** — `legal@growdirect.io` provisioned and monitored

Counsel should also confirm:
- That §3's "Categories of Personal Data" is exhaustive for the Merchant's intended use (per-merchant tailoring expected)
- That the cross-border transfer mechanism (§9 SCCs) is current — SCCs are revised periodically
- Whether any state-specific addenda are needed (Texas TDPSA, Virginia VCDPA, Colorado CPA, Connecticut CTDPA — all 2026)

---

## Change log

| Version | Date | Changes |
|---|---|---|
| v0.1 | 2026-05-02 | Initial working template — GRO-693 |
