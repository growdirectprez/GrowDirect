---
type: dispatch
status: ready-to-dispatch
date: 2026-05-04
priority: high
target: any
agent: mission-control
unblocks: PCI DSS audit engagement
tags: [pci, dss, compliance, audit, dispatch]
playbook: Brain/wiki/cards/pci-audit-playbook.md
---

# Dispatch — PCI DSS audit engagement

## Context

We have been retained to perform an annual PCI DSS v4.0.1 assessment of the customer's cardholder data environment (CDE). Method follows `Brain/wiki/cards/pci-audit-playbook.md` exactly. Default deliverable is a Report on Compliance (RoC) and Attestation of Compliance (AoC) signed by the QSA team and customer. If SAQ eligibility is determined in Phase 1, the playbook collapses to the SAQ deliverable and Phase 5 closes earlier.

Pre-engagement evidence (prior assessments, current ASV scans, prior pen test reports, policy set) enters the bus as `capture` artifacts at provisioning. The playbook proceeds from a non-empty starting state.

## Steps

The six-phase sequence below runs against the playbook. Each phase has an explicit gate. Mission control signs each gate. No phase advances on incomplete inputs.

### Step 1 — Charter and provision (Phase 0)

1. Confirm engagement scope (entity, sites, CDE boundary, assessment period) with customer security lead.
2. Confirm assessment type (RoC default; SAQ variant if eligible).
3. Verify QSA team qualification per PCI SSC QSA Program Guide (company current, individuals qualified).
4. Verify QSA independence (no consulting on the in-scope environment in prior 12 months); capture conflict of interest declaration.
5. Provision GCP project per engagement; deploy capsule; issue scoped credentials per system.
6. Sign charter. Engagement begins on charter signature.

Gate: charter signed, capsule operational, QSA team qualification and independence recorded.

### Step 2 — Scope (Phase 1)

1. Dispatch `imprint-pci-cde-boundary-mapping`. Establish the CDE perimeter; identify connected systems; document exclusions with justification.
2. Dispatch `imprint-pci-payment-flow-mapping`. Trace cardholder data end to end: entry, processing, storage, transmission, deletion.
3. Dispatch `imprint-pci-system-component-inventory`. Inventory every in-scope system component.
4. Dispatch `imprint-pci-segmentation-validation`. If segmentation is used to reduce scope, validate the segmentation design and request the segmentation pen test.
5. Dispatch `imprint-pci-saq-or-roc-determination`. Confirm RoC vs SAQ based on merchant level, transaction volume, and card brand requirements.

Gate: CDE scope confirmed by QSA lead and customer security lead. Any unaccounted-for cardholder data path escalates to mission control before proceeding.

### Step 3 — Documentation (Phase 2)

1. Dispatch `imprint-pci-policy-procedure-review`. Read security policy and supporting policies; verify approval chain and currency.
2. Dispatch `imprint-pci-service-provider-register-review`. Verify all third parties that store/process/transmit CHD; confirm PCI DSS responsibility matrix per service provider.
3. Dispatch `imprint-pci-compensating-controls-review`. Read existing compensating-control worksheets; flag for QSA validation in Phase 4.
4. Dispatch `imprint-pci-incident-response-plan-review`. Verify the incident response plan covers cardholder data exposure scenarios.

Gate: documentation set complete; service provider register reconciled with payment flow map.

### Step 4 — Technical evidence (Phase 3)

For each PCI DSS requirement (1–12), dispatch the four-step pattern:

1. `imprint-pci-requirement-design-review` — read documentation; judge design adequacy; identify approach (Defined or Customized).
2. `imprint-pci-requirement-evidence-collection` — gather artifacts per the playbook's evidence requirements.
3. `imprint-pci-requirement-operating-effectiveness-test` — sample-test per the sampling discipline (minimum 5 per requirement; risk-weighted scaling).
4. `imprint-pci-requirement-finding-classification` — In Place / In Place with Compensating Control / Not Applicable / Not Tested / Not in Place.

PCI-specific technical tests in parallel:

- `imprint-pci-external-asv-scan-review` — confirm four passing quarterly ASV scans in the assessment period.
- `imprint-pci-internal-vulnerability-scan-review`
- `imprint-pci-penetration-test-review` — annual application + network pen test.
- `imprint-pci-segmentation-pen-test-review` — required if segmentation is used to reduce scope.
- `imprint-pci-network-security-control-test`
- `imprint-pci-cardholder-data-discovery` — verify no CHD outside the documented CDE.

Cross-cutting:

- `imprint-pci-control-owner-interview` per requirement area.
- `imprint-pci-incident-response-tabletop-review`.

Gate: every PCI DSS requirement has a `requirement-implementation` fragment with classification. Every required scan and pen test is captured. Cardholder data discovery is clean or every exception accounted for.

### Step 5 — Findings synthesis (Phase 4)

1. Dispatch `imprint-pci-findings-aggregation`. Compose all findings into one register.
2. Dispatch `imprint-pci-nonconformity-classification`. Apply the playbook's classification rules.
3. Dispatch `imprint-pci-compensating-control-validation`. QSA validates each compensating control: risk analysis sufficient, control equivalence demonstrated, monitoring in place.
4. If any requirement uses Customized Approach, dispatch `imprint-pci-customized-approach-validation`. Validate targeted risk analysis and equivalence.
5. Dispatch `imprint-pci-roc-synthesis`. Produce the RoC per the v4.0 RoC Reporting Template.

Gate: RoC drafted; all compensating controls validated; any Customized Approach validated; classification register complete.

### Step 6 — Closeout (Phase 5)

1. Dispatch `imprint-pci-aoc-issuance`. Generate the Attestation of Compliance for QSA lead and customer signature.
2. Dispatch `imprint-pci-remediation-plan-review` (if any `Not in Place` findings). Verify root cause, action, owner, target date, retest method.
3. Dispatch `imprint-pci-annual-surveillance-schedule-set`. Configure next annual assessment, quarterly ASV scan reminders, and annual pen test reminders.
4. Dispatch `imprint-pci-acquirer-notification` if required by the customer's acquirer.

Gate: RoC signed by QSA lead, AoC signed by QSA lead and customer authorized signer, remediation plan accepted (if applicable), acquirer notified (if required), surveillance schedule set.

## Reporting cadence

- Daily — operating lead summarizes finding rate, open decisions, blocked imprints to mission control via the engagement console.
- Weekly — mission control issues a status update to the customer security lead: phase, requirements covered, classified findings, open decisions, schedule status.
- Phase-gate — formal decision artifact signed by QSA lead and shared with customer security lead.

## Out of scope

- Implementation of remediation actions (customer responsibility)
- Acquirer's compliance acceptance decision
- Security consulting on requirement design (independence requirement)
- Audit of customer's downstream merchants or service providers beyond the in-scope CDE relationship

## References

- Playbook: `Brain/wiki/cards/pci-audit-playbook.md`
- Companion playbook: `Brain/wiki/cards/iso27001-audit-playbook.md`
- Artifact taxonomy: `Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md`
- Imprint header spec: `Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md`
- PCI DSS v4.0.1, PCI SSC RoC Reporting Template, PCI SSC QSA Program Guide

## Charter requirements before pickup

- Customer security lead identified
- Engagement scope statement (entity, sites, CDE boundary, assessment period)
- Merchant level / transaction volume / card brand confirmed
- Prior assessment artifacts available (RoC if applicable, current ASV scan results, current pen test report)
- QSA team composition with qualification + independence declarations
- Steering committee membership (customer side)
- Reporting cadence agreed
- GCP project provisioning ownership identified

## Acceptance

Per the playbook's acceptance criteria. Engagement closes on signed RoC, signed AoC, accepted remediation plan (if applicable), acquirer notification (if required), and an annual surveillance schedule active in the engagement record.
