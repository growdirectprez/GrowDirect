---
type: dispatch
status: ready-to-dispatch
date: 2026-05-04
priority: high
target: any
agent: mission-control
unblocks: ISO 27001 audit engagement
tags: [iso27001, compliance, audit, dispatch]
playbook: Brain/wiki/cards/iso27001-audit-playbook.md
---

# Dispatch — ISO 27001 audit engagement

## Context

We have been retained to perform a Stage 1 + Stage 2 ISO/IEC 27001:2022 audit of the customer's ISMS. Method follows `Brain/wiki/cards/iso27001-audit-playbook.md` exactly. Scope is the full ISMS per the customer's SoA (to be confirmed at charter signing).

Pre-engagement evidence already gathered enters the bus as `capture` artifacts at provisioning; the playbook proceeds from a non-empty starting state.

## Steps

The five-phase sequence below runs against the playbook. Each phase has an explicit gate. Mission control signs each gate. No phase advances on incomplete inputs.

### Step 1 — Charter and provision (Phase 0)

1. Confirm engagement scope (entity, sites, ISMS boundary, period) with customer ISMS owner.
2. Confirm audit type (Stage 1 + Stage 2 / surveillance / recertification).
3. Confirm SoA version under audit.
4. Verify auditor independence per ISO 17021 (no ISMS consulting in prior 24 months in scope).
5. Provision GCP project per engagement, deploy capsule, issue scoped credentials per system.
6. Sign charter. Engagement begins on charter signature.

Gate: charter signed, capsule operational, audit team competence and independence recorded.

### Step 2 — Context and scope verification (Phase 1, Stage 1)

1. Dispatch `imprint-iso-isms-scope-verification`. Read the customer's ISMS scope statement; confirm boundary, exclusions, and justifications.
2. Dispatch `imprint-iso-interested-parties-review`. Verify register against clause 4.2 requirements.
3. Dispatch `imprint-iso-context-issue-mapping`. Verify internal/external issues per clause 4.1.
4. Dispatch `imprint-iso-isms-policy-review`. Read security policy and supporting policy framework; verify approval chain.
5. Dispatch `imprint-iso-stage1-readiness-judgment`. Synthesizer composes Stage 1 readiness conclusion: ready / not ready / ready with observations.

Gate: Stage 1 readiness signed by auditor lead. Major scope or context gaps escalate; Stage 2 does not start until resolved.

### Step 3 — Risk assessment and SoA validation (Phase 2)

1. Dispatch `imprint-iso-risk-methodology-review`. Verify the risk methodology meets clause 6.1 requirements.
2. Dispatch `imprint-iso-risk-register-validation`. Sample the risk register; verify identification, analysis, evaluation.
3. Dispatch `imprint-iso-risk-treatment-plan-review`. Verify treatment options, residual risk acceptance, owners.
4. Dispatch `imprint-iso-soa-coverage-validation`. Confirm every Annex A control is marked applicable or not applicable with justification.

Gate: SoA coverage complete. Any control marked not applicable without documented justification escalates.

### Step 4 — Control evidence (Phase 3, Stage 2)

For each Annex A control in scope, dispatch the four-step pattern:

1. `imprint-iso-control-design-review` — read documentation, judge design adequacy.
2. `imprint-iso-control-evidence-collection` — gather artifacts per the playbook's evidence requirements.
3. `imprint-iso-operating-effectiveness-test` — sample test per the sampling discipline (minimum 5 per control where population permits; risk-weighted scaling).
4. `imprint-iso-control-finding-classification` — conformity / observation / minor NC / major NC.

In parallel:

- Dispatch `imprint-iso-control-owner-interview` per control area (organizational, people, physical, technological) and per ISMS clause owner (clauses 4–10).
- Dispatch `imprint-iso-management-review-evidence` for clauses 4–10 documentation and records.

Gate: every Annex A control in scope has a `control-implementation` fragment with classification. Every clause 4–10 has an evidence-backed finding.

### Step 5 — Findings synthesis (Phase 4)

1. Dispatch `imprint-iso-findings-aggregation`. Compose all findings into one register.
2. Dispatch `imprint-iso-nonconformity-classification`. Apply the playbook's classification rules. Major NCs are blocking; minor NCs require corrective action plan.
3. Dispatch `imprint-iso-audit-report-synthesis`. Produce the audit report per the playbook's structure.
4. Dispatch `imprint-iso-management-response-capture`. Capture the customer ISMS owner's response per finding.

Gate: audit report drafted, management response captured per finding.

### Step 6 — Closeout (Phase 5)

1. Dispatch `imprint-iso-corrective-action-plan-review`. Read customer's corrective action plan; verify root cause, action, owner, target date, verification method.
2. Dispatch `imprint-iso-certification-recommendation`. Synthesizer composes recommendation: certify, conditionally certify, not certify.
3. Dispatch `imprint-iso-surveillance-schedule-set`. Configure annual surveillance and 3-year recertification schedule in the engagement record.

Gate: audit report signed by auditor lead, recommendation signed by certification body authority, corrective action plan accepted (if non-conformities), surveillance schedule set.

## Reporting cadence

- Daily — operating lead summarizes finding rate, open decisions, blocked imprints to mission control via the engagement console.
- Weekly — mission control issues a status update to the customer ISMS owner: phase, controls covered, classified findings, open decisions, schedule status.
- Phase-gate — formal decision artifact signed by auditor lead and emailed to customer ISMS owner.

## Out of scope

- Implementation of corrective actions (customer responsibility)
- Certification body decision (we issue the recommendation; the certification body issues the certificate)
- Consulting on ISMS design (independence requirement)
- Audit of customer's own customers, suppliers, or third parties beyond what is required by Annex A controls

## References

- Playbook: `Brain/wiki/cards/iso27001-audit-playbook.md`
- Artifact taxonomy: `Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md`
- Imprint header spec: `Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md`
- ISO/IEC 27001:2022, ISO/IEC 27002:2022, ISO/IEC 17021-1, ISO 19011

## Charter requirements before pickup

- Customer ISMS owner identified
- Engagement scope statement (entity, sites, ISMS boundary, period)
- SoA version under audit
- Audit team composition with independence and competence declarations
- Steering committee membership (customer side)
- Reporting cadence agreed
- GCP project provisioning ownership identified

## Acceptance

Per the playbook's acceptance criteria. Engagement closes on signed audit report, signed recommendation, accepted corrective action plan (if applicable), and a surveillance schedule active in the engagement record.
