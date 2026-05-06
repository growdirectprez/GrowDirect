---
classification: internal
type: wiki
sub-type: playbook
status: draft
date: 2026-05-04
last-compiled: 2026-05-04
needs-review: 2026-05-18
engines: [platform, compliance]
companion: Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md
companion: Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md
companion: Brain/wiki/cards/iso27001-audit-playbook.md
companion: Brain/wiki/cards/execution-primer-template.md
owner: ALX
---

# PCI DSS Audit Playbook

## Engagement assumption

Annual PCI DSS v4.0.1 assessment of the customer's cardholder data environment (CDE). Default deliverable is a Report on Compliance (RoC) culminating in an Attestation of Compliance (AoC) signed by the QSA team and the customer. Scope is the CDE and connected systems as confirmed at charter signing. If the customer is eligible for a Self-Assessment Questionnaire (SAQ) variant per merchant level / transaction volume / card brand, the playbook substitutes the SAQ-eligibility imprint and shortens the synthesis phase to the SAQ deliverable. Substrate is the standard diagnostic capsule deployed in the customer's GCP environment.

## Phases

| Phase | Purpose | Output |
|---|---|---|
| 0 — Provision | Engagement scoped, QSA team credential-verified, infra live | Signed charter, capsule deployed, QSA credentials confirmed, scoped customer credentials issued |
| 1 — Scope (CDE) | Cardholder data environment boundary, segmentation, flow, system inventory | `cde-boundary`, `payment-flow-map`, `system-component-inventory`, `segmentation-validation`, `saq-or-roc-determination` fragments |
| 2 — Documentation | Security policies, procedures, service provider register, compensating controls | `pci-policy`, `service-provider-register`, `compensating-controls-register`, `incident-response-plan` fragments |
| 3 — Technical evidence | Per requirement design + operating effectiveness; ASV scans, internal scans, pen test review | `requirement-implementation` fragments per Req 1–12; `asv-scan-results`, `pen-test-results`, `cardholder-data-discovery` |
| 4 — Findings synthesis | Findings classification, RoC drafting, compensating-control validation | `pci-finding` fragments, `roc-document` synthesis |
| 5 — Closeout | AoC issuance, remediation plan, annual schedule, acquirer notification | `aoc-document`, `remediation-plan`, surveillance schedule |

## Imprints per phase

### Phase 0 — Provision
- `imprint-pci-charter-signing`
- `imprint-pci-environment-provisioning`
- `imprint-pci-qsa-team-credential-verification`

### Phase 1 — Scope
- `imprint-pci-cde-boundary-mapping`
- `imprint-pci-payment-flow-mapping`
- `imprint-pci-system-component-inventory`
- `imprint-pci-segmentation-validation`
- `imprint-pci-saq-or-roc-determination`

### Phase 2 — Documentation
- `imprint-pci-policy-procedure-review`
- `imprint-pci-service-provider-register-review`
- `imprint-pci-compensating-controls-review`
- `imprint-pci-incident-response-plan-review`

### Phase 3 — Technical evidence
Per PCI DSS Requirement (1 through 12), dispatch the four-step pattern:
- `imprint-pci-requirement-design-review`
- `imprint-pci-requirement-evidence-collection`
- `imprint-pci-requirement-operating-effectiveness-test`
- `imprint-pci-requirement-finding-classification`

PCI-specific technical tests:
- `imprint-pci-external-asv-scan-review` — verify four quarterly ASV scans in the assessment period
- `imprint-pci-internal-vulnerability-scan-review`
- `imprint-pci-penetration-test-review` — annual application + network pen test
- `imprint-pci-segmentation-pen-test-review` — required when segmentation is used to reduce scope
- `imprint-pci-network-security-control-test`
- `imprint-pci-cardholder-data-discovery` — verifies no unaccounted-for cardholder data exists outside the CDE

Cross-cutting interviews:
- `imprint-pci-control-owner-interview` per requirement area
- `imprint-pci-incident-response-tabletop-review`

### Phase 4 — Findings synthesis
- `imprint-pci-findings-aggregation`
- `imprint-pci-nonconformity-classification`
- `imprint-pci-compensating-control-validation`
- `imprint-pci-customized-approach-validation` — only if Customized Approach used
- `imprint-pci-roc-synthesis`

### Phase 5 — Closeout
- `imprint-pci-aoc-issuance`
- `imprint-pci-remediation-plan-review`
- `imprint-pci-annual-surveillance-schedule-set`
- `imprint-pci-acquirer-notification` — when acquirer notification is required

## Schema-fragment facets

| Facet | What it captures |
|---|---|
| `cde-boundary` | CDE perimeter; included systems; excluded systems with justification |
| `payment-flow-map` | End-to-end flow of cardholder data: entry, processing, storage, transmission, deletion |
| `system-component-inventory` | Every in-scope system component with role, OS/version, owner, network location |
| `segmentation-validation` | Segmentation design + pen test results verifying isolation |
| `saq-or-roc-determination` | Eligibility per merchant level / transaction volume / card brand requirements |
| `pci-policy` | Information security policy + supporting policies; approval chain |
| `service-provider-register` | Third parties that store/process/transmit CHD or impact security; PCI DSS responsibility matrix |
| `compensating-controls-register` | Compensating controls in use; risk analysis; QSA validation |
| `requirement-implementation` | Per requirement: approach (Defined/Customized), design, evidence, operating effectiveness, conclusion |
| `asv-scan-results` | Quarterly external scans by Approved Scanning Vendor; passing posture |
| `pen-test-results` | Annual application + network pen test; segmentation pen test |
| `cardholder-data-discovery` | Discovery scan results verifying no CHD outside CDE |
| `pci-finding` | Per requirement: classification, evidence, remediation if needed |
| `roc-document` | Synthesized Report on Compliance per PCI DSS RoC Reporting Template |
| `aoc-document` | Attestation of Compliance signed by QSA + customer authorized signer |
| `remediation-plan` | Per finding: action, owner, target date, retest method |

## PCI DSS v4.0.1 requirement coverage

| Goal | Requirements | Focus |
|---|---|---|
| Build and Maintain a Secure Network and Systems | 1, 2 | Network security controls; secure configurations |
| Protect Account Data | 3, 4 | Protect stored data; protect transmission with strong cryptography |
| Maintain a Vulnerability Management Program | 5, 6 | Anti-malware; secure development and change control |
| Implement Strong Access Control Measures | 7, 8, 9 | Need-to-know; authentication; physical access |
| Regularly Monitor and Test Networks | 10, 11 | Logging + monitoring; testing (scans + pen test) |
| Maintain an Information Security Policy | 12 | Security policy + program |

PCI DSS v4.0 introduces the Customized Approach (CA) alongside the Defined Approach Requirements (DAR). Each requirement may be satisfied via either approach. Customized Approach requires:
- Documented targeted risk analysis (TRA)
- Customized control implementation document
- QSA-validated equivalence to the requirement objective

## Evidence requirements per requirement

Each `requirement-implementation` fragment must include:

- Requirement reference (e.g., `Req 8.3.1`)
- Approach (Defined / Customized)
- Design description (how the control is intended to work)
- Implementation evidence (policies, configurations, screenshots, logs, scan results, training records)
- Operating effectiveness evidence (sample tested with method, dates, results)
- Sample size with selection rationale
- Source attribution per evidence item
- Conclusion: `In Place` / `In Place with Compensating Control` / `Not Applicable` / `Not Tested` / `Not in Place`
- Confidence (high / medium / low) with reason if not high

## Findings classification (PCI standard)

| Class | Definition | Effect on assessment |
|---|---|---|
| In Place | Requirement met as designed | Compliant for that requirement |
| In Place with Compensating Control | Met via compensating control with QSA validation | Compliant; compensating control documented |
| Not Applicable | Requirement does not apply, with documented justification | Documented exclusion |
| Not Tested | Requirement could not be tested (rare); must be justified | Reported; not compliant |
| Not in Place | Requirement not met | Non-compliant; remediation required |

A single `Not in Place` makes the overall assessment non-compliant. Compensating controls allow compliance via alternative means but require documented risk analysis and QSA validation.

## Sampling discipline

- Sample sizes guided by PCI SSC QSA Program Guide
- Population-based: typically 5–15% of population, minimum 5
- Risk-weighted: high-risk requirements (cryptography, access management, logging, change control) sampled at higher rates
- Time-distributed: drawn across the assessment period
- Documented rationale per requirement: sample size, selection method, period covered, exclusions
- Sample integrity: captures stored as `capture` artifacts in the engagement record with audit hash

## RoC structure (per PCI DSS v4.0 RoC Reporting Template)

The `roc-document` synthesis follows the official template, in order:

1. Executive summary
2. Description of scope of work and approach taken
3. Details about reviewed environment
4. Quarterly external ASV scan summary
5. Penetration test summary
6. Findings and observations per requirement (1.1.x through 12.x)
7. Compensating controls worksheets
8. Customized approach worksheets (when CA used)
9. Action plan for non-compliant items (if any `Not in Place`)
10. Attestation of Compliance (AoC)

## Approvals & sign-offs

| Gate | Signer | Form |
|---|---|---|
| Charter | Customer security lead + QSA lead | Signed JSON charter |
| Scope confirmation (Phase 1 close) | QSA lead + customer | Decision artifact |
| Documentation phase close | QSA lead | Decision artifact |
| Technical evidence phase close | QSA lead | Decision artifact |
| RoC sign-off | QSA lead | Signed `roc-document` |
| AoC sign-off | QSA lead + customer authorized signer | Signed `aoc-document` |
| Remediation plan acceptance | Customer security lead | Signed `remediation-plan` |
| Acquirer notification (where required) | Customer compliance officer | Per acquirer requirements |

## Acceptance criteria

Engagement is complete when all of the following hold:

- All 12 PCI DSS requirements have `requirement-implementation` fragments with classifications
- All findings registered with classification
- All compensating controls validated by QSA
- All quarterly ASV scans in the assessment period reviewed (4)
- Annual pen test reviewed (plus segmentation pen test if scope reduction is claimed)
- Cardholder data discovery scan reviewed
- RoC drafted and signed by QSA lead per the v4.0 RoC Reporting Template
- AoC signed by QSA lead and customer authorized signer
- Remediation plan accepted (if any `Not in Place` findings)
- Decision and audit logs complete and exported to immutable storage
- Annual surveillance schedule set in the engagement record

## QSA independence and qualification (per PCI SSC QSA Program Guide)

- QSA company qualified and current with PCI SSC
- QSA individuals on the engagement qualified for the engagement type
- Independence: no security consulting on the in-scope environment in the prior 12 months
- Conflict of interest declaration captured on charter
- Customer right to request QSA team change at engagement start

These declarations are recorded in the charter and linked to the QSA credential register.

## Open

- Per-card-brand specifics (Visa, MasterCard, Amex, Discover, JCB) where requirements differ
- SAQ variant playbooks (SAQ A, A-EP, B, B-IP, C, C-VT, D, P2PE)
- P2PE assessment variant (where customer is P2PE merchant)
- Per-requirement imprint headers (the four-step pattern as concrete imprint specs)
- Sampling table — recommended sample sizes per requirement category
- Customized Approach risk-analysis template
- Service provider PCI DSS responsibility matrix template
- Network segmentation test design guidance
