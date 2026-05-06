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
companion: Brain/wiki/cards/execution-primer-template.md
owner: ALX
---

# ISO 27001 Audit Playbook

## Engagement assumption

Stage 1 + Stage 2 ISO/IEC 27001:2022 audit of the customer's ISMS. Scope is the full ISMS as defined in the customer's Statement of Applicability (SoA). Output is a signed audit report and a certification recommendation (certify, conditionally certify, or not certify). The standard diagnostic substrate is deployed in the customer's GCP environment and persists post-audit for surveillance and recertification reuse.

## Phases

| Phase | Purpose | Output |
|---|---|---|
| 0 — Provision | Engagement scoped and infrastructure live | Signed charter, capsule deployed, scoped credentials |
| 1 — Context & scope (Stage 1) | Verify ISMS scope, context, interested parties, policy framework | `isms-scope`, `interested-parties`, `context-issues`, `isms-policy` fragments |
| 2 — Risk assessment & treatment | Verify risk methodology, register, treatment plan, SoA coverage | `risk-register`, `risk-treatment-plan`, `statement-of-applicability` fragments |
| 3 — Control evidence (Stage 2) | Per-control design adequacy + operating effectiveness | One `control-implementation` fragment per Annex A control in scope |
| 4 — Findings synthesis | Classify findings, draft report, capture management response | `audit-finding` fragments, `audit-report` synthesis, `nonconformity-register` |
| 5 — Closeout | Corrective action plan, certification recommendation, surveillance schedule | `corrective-action-plan`, `certification-recommendation`, surveillance schedule |

## Imprints per phase

### Phase 0 — Provision
- `imprint-iso-charter-signing`
- `imprint-iso-environment-provisioning`

### Phase 1 — Context & scope (Stage 1)
- `imprint-iso-isms-scope-verification`
- `imprint-iso-interested-parties-review`
- `imprint-iso-context-issue-mapping`
- `imprint-iso-isms-policy-review`
- `imprint-iso-stage1-readiness-judgment`

### Phase 2 — Risk assessment & treatment
- `imprint-iso-risk-methodology-review`
- `imprint-iso-risk-register-validation`
- `imprint-iso-risk-treatment-plan-review`
- `imprint-iso-soa-coverage-validation`

### Phase 3 — Control evidence (Stage 2)
Per Annex A control in scope, dispatch the four-step pattern:
- `imprint-iso-control-design-review` — read control documentation, judge design adequacy
- `imprint-iso-control-evidence-collection` — gather artifacts (policies, procedures, screenshots, logs, tickets)
- `imprint-iso-operating-effectiveness-test` — sample-test that the control runs as designed
- `imprint-iso-control-finding-classification` — conformity / observation / minor NC / major NC

Phase 3 also runs cross-cutting interviews:
- `imprint-iso-control-owner-interview` — per control area
- `imprint-iso-management-review-evidence` — clauses 4-10 evidence (leadership, planning, support, operation, performance evaluation, improvement)

### Phase 4 — Findings synthesis
- `imprint-iso-findings-aggregation`
- `imprint-iso-nonconformity-classification`
- `imprint-iso-audit-report-synthesis`
- `imprint-iso-management-response-capture`

### Phase 5 — Closeout
- `imprint-iso-corrective-action-plan-review`
- `imprint-iso-certification-recommendation`
- `imprint-iso-surveillance-schedule-set`

## Schema-fragment facets (additions to diagnostic schema)

| Facet | What it captures |
|---|---|
| `isms-scope` | ISMS boundary, included sites, included assets, exclusions with justification |
| `interested-parties` | Internal and external parties, their requirements, evidence of capture |
| `context-issues` | Internal/external issues affecting ISMS (clause 4.1) |
| `isms-policy` | Information security policy + supporting policies; approval chain |
| `risk-register` | Identified risks with likelihood, impact, owner, status |
| `risk-treatment-plan` | Treatment options selected, residual risk, owner, target date |
| `statement-of-applicability` | All 93 Annex A controls marked applicable / not applicable with justification |
| `control-implementation` | Per control: design description, evidence, sample test, conclusion |
| `audit-finding` | Per control or clause: finding, classification, evidence references |
| `nonconformity-register` | All non-conformities with classification, owner, target close date |
| `corrective-action-plan` | Per non-conformity: root cause, action, owner, target date, verification method |
| `audit-report` | Synthesized full audit report |
| `certification-recommendation` | Certify / conditional / not certify with rationale |

## Annex A coverage (ISO/IEC 27001:2022 — 93 controls across 4 themes)

| Theme | Controls | Count | Focus |
|---|---|---|---|
| Organizational | 5.1 – 5.37 | 37 | Policies, roles, third-party, asset classification, access governance, incident mgmt |
| People | 6.1 – 6.8 | 8 | Screening, terms of employment, awareness, disciplinary, remote work, NDAs |
| Physical | 7.1 – 7.14 | 14 | Perimeters, entry, equipment, secure areas, clean desk, supporting utilities |
| Technological | 8.1 – 8.34 | 34 | User devices, access mgmt, cryptography, malware, secure dev, logging, monitoring, network security |

Plus ISMS clauses 4–10 (mandatory):
- Clause 4 — Context of the organization
- Clause 5 — Leadership
- Clause 6 — Planning
- Clause 7 — Support
- Clause 8 — Operation
- Clause 9 — Performance evaluation
- Clause 10 — Improvement

## Evidence requirements per control

Each `control-implementation` fragment must include:

- Control reference (Annex A number, e.g., `A.5.15`)
- Design description (how the control is supposed to work)
- Implementation evidence (links/snapshots of policies, procedures, configurations, training records)
- Operating effectiveness evidence (sample tested with method, dates, results)
- Sample size with selection method and rationale
- Source attribution per evidence item (system, owner, date)
- Conclusion (effective / partially effective / not effective)
- Confidence (high / medium / low) and reason if not high

## Findings classification

| Class | Definition | Effect on certification |
|---|---|---|
| Conformity | Control operates as designed and meets requirement | None |
| Observation | Improvement opportunity, not a non-conformity | None; noted in report |
| Minor non-conformity | Isolated lapse or single control gap, not systemic | Corrective action plan required, not blocking |
| Major non-conformity | Systemic failure, missing control, or breach of mandatory clause | Blocking. Must be closed before certification |

## Sampling discipline

- Population-based sampling — minimum 5 items per control where population permits, scaled to 10–25% of population size
- Risk-weighted sampling — increase sample size for high-risk controls (e.g., access management, cryptography, incident response)
- Time-distributed sampling — samples drawn across the full audit period, not concentrated
- Documented rationale per control — sample size, selection method, period covered, exclusions
- Sample integrity — captures stored in the engagement record under `capture` artifact type

## Audit report structure

The `audit-report` synthesis contains, in order:

1. Executive summary (recommendation, headline findings)
2. Audit scope and methodology (per ISO 19011)
3. ISMS context (scope statement, interested parties, key issues)
4. Risk treatment summary (methodology, register sample, SoA coverage)
5. Per-clause findings (clauses 4–10)
6. Per-Annex-A-control findings, organized by theme
7. Findings classification register (conformities, observations, minor NCs, major NCs)
8. Management response per finding
9. Recommendation (certify / conditionally certify / not certify) with rationale
10. Corrective action plan reference
11. Surveillance schedule (annual surveillance, 3-year recertification)

## Approvals & sign-offs

| Gate | Signer | Form |
|---|---|---|
| Charter | Customer ISMS owner + auditor lead | Signed JSON charter artifact |
| Phase 1 close (Stage 1 readiness judgment) | Auditor lead | Decision artifact |
| Phase 2 close | Auditor lead + customer ISMS owner | Decision artifact |
| Phase 3 close (Stage 2 evidence complete) | Auditor lead | Decision artifact |
| Audit report | Auditor lead | Signed `audit-report` synthesis |
| Certification recommendation | Certification body authority | Signed `certification-recommendation` artifact |
| Corrective action plan | Customer ISMS owner | Signed `corrective-action-plan` artifact |

## Acceptance criteria

Engagement is complete when all of the following hold:

- All Annex A controls in scope have a `control-implementation` fragment with classification
- All clauses 4–10 have evidence and a finding classification
- All findings registered in `nonconformity-register` with class
- Audit report synthesized, signed by auditor lead
- Management response captured per finding
- Certification recommendation issued
- Corrective action plan accepted by customer ISMS owner if non-conformities exist
- Decision and audit logs complete and exported to immutable storage
- Surveillance and recertification schedule set in the engagement record

## Independence and competence (per ISO 17021)

Per certification body requirement, the audit team must satisfy:

- Independence from the customer (no consulting in the prior 24 months on ISMS in scope)
- Competence per the certification body's competency matrix (lead auditor qualification, sector experience)
- Conflict of interest declaration on charter
- Customer right to challenge audit team composition

These are recorded in the charter and linked to the auditor lead's credential register.

## Open

- Surveillance audit (annual) playbook variant — narrower scope, follow-up on prior findings
- Recertification audit (3-year) playbook variant — full re-audit
- Per-control imprint headers (the four-step pattern as concrete imprint specs)
- Sampling table — recommended sample sizes per control category
- Pre-audit interview guide for ISMS owner (charter calibration)
- Customer self-assessment intake (if pre-engagement self-assessment exists)
