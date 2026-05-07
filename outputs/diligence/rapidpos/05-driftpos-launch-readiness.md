# DriftPOS Launch Readiness — RapidPOS LLC (Demo Run)

> **DEMO RUN — what stands between today and DriftPOS GA at month 12.**

**Vendor:** RapidPOS LLC
**DriftPOS partner contact:** Bart
**Target GA:** Month 12 post-acquisition close
**Run date:** 2026-05-03

---

## The gate, plainly

DriftPOS cannot ship customer-data-handling features in production until:

1. The 15 critical-mass ISO 27001 controls are passable (per `02-iso27001-gap-assessment.md`)
2. PCI-DSS scope inheritance is verified (Ingenico tokenization → no Canary.GO scope)
3. The 12 Bart OQs are resolved (load-bearing four are: OQ-1, OQ-2, OQ-3, OQ-11)

Phase 2 produces the yes/no on each. This document is the readiness summary.

## Critical-mass 15 ISO 27001 controls — RapidPOS readiness

| Control | RapidPOS current state (hypothesis) | Hours to remediate | Pre-GA required? |
| --- | --- | --- | --- |
| 5.15 Access control | Counterpoint has access; cloud needs Cloud IAM | 32 | YES |
| 5.17 Authentication info | Informal; centralize via Secret Manager | 24 | YES |
| 5.23 Cloud governance | From scratch; deploy Org policies | 32 | YES |
| 5.24 IR planning | Informal IR; need plan + tabletop | 24 | YES |
| 5.34 PII protection | Informal; deploy DLP API + Cloud KMS | 32 | YES |
| 6.5 Off-boarding | Inconsistent; need security checklist | 16 | YES |
| 8.2 Privileged access | Ad-hoc; deploy Cloud IAM + PAM | 32 | YES |
| 8.5 Secure auth (MFA) | Not enforced; deploy Cloud Identity 2SV org-wide | 32 | YES |
| 8.9 Configuration mgmt | No IaC; stand up Terraform + Config Connector | 64 | YES |
| 8.13 Backup | Backups exist; no recovery test; add cross-region + drill | 24 | YES |
| 8.15 Logging | Logs scattered; centralize on Cloud Logging + sinks | 32 | YES |
| 8.16 Monitoring | No SIEM; deploy SCC Premium + Chronicle | 40 | YES |
| 8.20 Networks security | From scratch in cloud; VPC + Cloud Armor | 40 | YES |
| 8.24 Cryptography | Inconsistent; deploy Cloud KMS comprehensively | 40 | YES |
| 8.25 Secure SDLC | No formal SDLC; deploy Cloud Build + Binary Auth | 56 | YES |

**Total: 520 hours / $104k engineering remediation.**

At 3 effective FTEs in Phase A → ~6 weeks of Phase A engineering capacity dedicated to this critical-mass subset. Sequenced parallel to A1-A5 deployment.

## PCI-DSS scope position

DriftPOS uses Ingenico pinpads. Ingenico's P2PE attestation covers cardholder data tokenization at the device. Tokenized payment fingerprints flow to Canary.GO; Canary.GO never touches raw cardholder data.

**Position to validate:**
- Ingenico's P2PE attestation is current and covers DriftPOS's specific deployment shape
- DriftPOS's .NET adapter does not introduce a PCI scope expansion
- Canary.GO's tokenization-handling falls under SAQ-A or SAQ-A-EP (no scope)

**Discovery items for Phase 2:**
- Confirm Ingenico's most recent P2PE attestation (annual)
- Validate DriftPOS deployment topology against the attestation (sometimes attestations don't cover all configurations)
- Verify VAR customers' inherited scope doesn't change with the Canary.GO integration

If any of these is not yet confirmed, add it to the Bart OQ list.

## The 12 Bart OQs — readiness mapping

From the 2026-05-03 Bart conversation prep doc. Load-bearing for posture:

| OQ | Topic | DriftPOS-blocking? | Phase 2 stance |
| --- | --- | --- | --- |
| OQ-1 | mTLS vs JWT for register↔back-half | Affects 8.5 + 8.24 | Accept JWT for pilot; require mTLS by GA |
| OQ-2 | Ingenico network token availability | Affects PCI scope + party-resolution latency | Self-computed fallback acceptable for v1 |
| OQ-3 | Idempotency-Key honor on retry | Affects 8.20 + offline-replay correctness | Required for any reliable wire spec |
| OQ-4 | Queue cap | Pilot-config | Defer to pilot config |
| OQ-5 | UUID assignment | Wire-spec correctness | Required for contract |
| OQ-6 | (per Bart prep doc — verify) | (per Bart prep doc) | Verify at meeting |
| OQ-7 | UI button | Pilot-config | Defer to pilot config |
| OQ-8 | (per Bart prep doc — verify) | (per Bart prep doc) | Verify at meeting |
| OQ-9 | (per Bart prep doc — verify) | (per Bart prep doc) | Verify at meeting |
| OQ-10 | (per Bart prep doc — verify) | (per Bart prep doc) | Verify at meeting |
| OQ-11 | PCI scope inheritance position | Direct PCI scope | Required for GA |
| OQ-12 | (per Bart prep doc — verify) | (per Bart prep doc) | Verify at meeting |

The four load-bearing OQs (1, 2, 3, 11) need landing decisions before contract publication. The others can be deferred to pilot-config-time without blocking.

## Pre-GA / Pilot-only / Post-GA acceptable splits

### Blockers (must resolve before DriftPOS GA at month 12)

- All 15 critical-mass ISO 27001 controls passable
- OQ-1 mTLS path defined (mTLS by GA, JWT for pilot acceptable)
- OQ-2 Ingenico tokenization position settled
- OQ-3 Idempotency-Key semantics wire-spec'd
- OQ-11 PCI scope inheritance documented and customer-comfortable
- ISO 27001 Stage 2 audit observation period started (month 12 launch concurrent with observation)
- DriftPOS production environment passes a sandbox-tier penetration test
- IR plan + tabletop exercise complete

### Pilot-only acceptable (GA later)

- OQ-4 queue cap (pilot config; per-customer flexibility)
- OQ-7 UI button (pilot config)
- ISO 27001 certificate not yet issued (Stage 2 observation in progress at GA — acceptable for early customers; required for enterprise customers)

### Post-GA acceptable (during Stage 2 observation period 12-18 months)

- The remaining 78 ISO 27001 controls reach passable state
- SOC 2 Type II observation begins (target start month 18)
- Surveillance audit cadence established
- Vanta/Drata GRC tooling stood up for ongoing-compliance monitoring

## DriftPOS-launch sequence

| Month | Milestone | Gate |
| --- | --- | --- |
| 0 | Acquisition close; A1-A5 deployment kickoff; ISO Phase 2 remediation underway | — |
| 3 | First 8 of 15 critical-mass controls remediated; sandbox infra live | Internal review |
| 6 | All 15 critical-mass controls remediated; sandbox DriftPOS deployment | Pre-Stage-1 dry run |
| 9 | ISO Stage 1 audit clean; first eager-cohort customer in sandbox migration | Stage 1 sign-off |
| 12 | **DriftPOS GA**; Stage 2 observation start; eager-cohort wave 1 in production | Stage 2 observation triggered |
| 18 | ISO 27001 certified; eager-cohort wave 2 complete | Certificate in hand |

## What kills DriftPOS GA at month 12

- Bart team turnover during Phase A
- Ingenico changes their attestation in a way that pushes Canary.GO into PCI scope
- Critical-mass control remediation runs behind schedule (>8 weeks late)
- Discovery surfaces a previously-unknown compliance issue at RapidPOS LLC level (e.g., past breach not disclosed in Phase 1)
- A1 + A2 don't reach burn-down targets, so the seller team is still 60%+ on break-fix and unavailable for migration onboarding work

## Cross-references

- `02-iso27001-gap-assessment.md` — full 93-control assessment with the critical-mass 15 highlighted
- `02-iso27001-gap-assessment.xlsx` — control-by-control workload estimator
- `03-gcp-onramp-architecture.md` — proposed target GCP architecture
- `crb-skills/saas-acquisition-diligence/reference/07-driftpos-readiness-gate.md` — full readiness-gate methodology
- `docs/superpowers/plans/2026-05-03-bart-conversation-prep.md` — Bart OQ source
- Linear: GRO-762 (Bart conversation prep), GRO-739 (DriftPOS integration parent)
