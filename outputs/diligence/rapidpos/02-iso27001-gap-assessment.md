# ISO 27001:2022 Gap Assessment — RapidPOS LLC (Demo Run)

> **DEMO RUN — archetype-default current-state hypothesis.** Companion to `02-iso27001-gap-assessment.xlsx`. The spreadsheet is authoritative.

**Vendor:** RapidPOS LLC
**Run date:** 2026-05-03
**Phase:** 2 — Audit-as-diligence

---

## Headline numbers

At archetype-default current-state hypothesis (none-formal ISMS, typical Counterpoint-VAR posture):

- **Total remediation: ~1,684 engineering hours = ~$337k**
- **DriftPOS-blocking subset (15 critical-mass controls): ~520 hours = ~$104k**
- **Calendar weeks at 3 effective FTE: ~19 weeks** (close to the M6 Phase A end target)

Theme breakdown:
- Organizational (37 controls): ~664 hours / $133k
- People (8 controls): ~88 hours / $18k
- Physical (14 controls): ~84 hours / $17k (mostly inherited from GCP for cloud workloads)
- Technological (34 controls): ~848 hours / $170k (the dominant cost)

These are *engineering remediation hours*. They do not include the broader Phase-A program (A1-A5 deployment, GCP infra ramp, onboarding-playbook development, customer-cohort migration). Those live in the cost-model `program_cost` tab as separate lines.

## Where the work concentrates

### High-effort gaps (DriftPOS-blocking, must clear before GA)

These 15 controls are the critical-mass for any cloud-customer-data handling. RapidPOS will need *all* of them passable before DriftPOS GA at month 12.

| Control | Title | Hours | $ | Notes |
| --- | --- | --- | --- | --- |
| 5.15 | Access control | 32 | $6.4k | Counterpoint has access; modernization adds Cloud IAM |
| 5.17 | Authentication info | 24 | $4.8k | Centralize secrets via Secret Manager |
| 5.23 | Cloud governance | 32 | $6.4k | Org policies from scratch |
| 5.24 | IR planning | 24 | $4.8k | Plan + tabletop exercise |
| 5.34 | PII protection | 32 | $6.4k | DLP API + Cloud KMS |
| 6.5 | Off-boarding | 16 | $3.2k | Security checklist + automation |
| 8.2 | Privileged access rights | 32 | $6.4k | Cloud IAM + PAM (just-in-time) |
| 8.5 | Secure authentication (MFA) | 32 | $6.4k | Cloud Identity 2SV org-wide |
| 8.9 | Configuration management | 64 | $12.8k | Terraform + Config Connector |
| 8.13 | Information backup | 24 | $4.8k | Cross-region snapshots + drill |
| 8.15 | Logging | 32 | $6.4k | Cloud Logging + sinks |
| 8.16 | Monitoring | 40 | $8k | SCC Premium + Chronicle |
| 8.20 | Networks security | 40 | $8k | VPC + Cloud Armor |
| 8.24 | Use of cryptography | 40 | $8k | Cloud KMS comprehensive |
| 8.25 | Secure SDLC | 56 | $11.2k | Cloud Build + Binary Auth |

**Subtotal: 520 hours / $104k.** This is the work that *must* be done before DriftPOS GA. Sequenced into Phase A (months 0-6).

### Moderate-effort gaps (must clear for ISO 27001 cert at month 18)

The remaining 78 controls. Most are partial (some practice exists; needs documentation + formalization) rather than absent (must build from scratch). These are sequenced into Phase A end → Phase B.

### Low-effort wins (already moderate or compliant)

A handful of controls are already in roughly compliant state for a 20-year operating business: NDAs (6.6), basic equipment maintenance (7.13), GCP-inherited NTP (8.17). These contribute zero or near-zero remediation cost.

## What the model can't see at archetype-default

This assessment uses *archetype-default* current-state hypothesis. Founder verification of the 16 questions (especially Q4 on customer compliance pressure, Q5 on existing certifications, and Q14 on tribal knowledge concentration) will refine each control's hypothesis individually.

**Likely refinements after founder review:**
- Several Org controls may move from "absent" to "weak" (some informal practice exists). Reduces hours.
- Some Tech controls may move from "weak" to "absent" if the founder confirms tooling is genuinely zero. Increases hours.
- Customer-driven compliance work that RapidPOS has done ad-hoc (vendor questionnaire responses, PCI-SAQ inheritance support) may show up as documented evidence we can leverage. Reduces hours.

The expected delta from archetype-default is ±20-30%. Real number sits in the $250k-$425k range.

## What's NOT remediated by this gap assessment alone

ISO 27001 certification requires not only the controls being passable but also:
- **An ISMS (Information Security Management System):** the policy framework + governance that ties the controls together. Roughly 200-400 hours separate from the per-control remediation. Not in the spreadsheet.
- **Stage 1 + Stage 2 audit fees:** $20k-$50k for a credentialed audit firm.
- **Stage 2 observation period:** typically 3-6 months between Stage 1 and Stage 2.
- **Surveillance audits:** annual after certification; ~$10k-$20k/year ongoing.

Adding ISMS framework work + audit fees + ongoing surveillance: roughly +$100k-$150k beyond the per-control gap engineering. Total binding cost sits closer to **$450k-$575k** for the ISO 27001 work end-to-end.

## Sequencing into the program

| Phase | Months | ISO work performed | Audit milestone |
| --- | --- | --- | --- |
| Phase A | 0-6 | All 15 critical-mass controls remediated. ISMS policy framework drafted. | Internal readiness review |
| Phase A end | 6 | Critical-mass passable. Sandbox-tier DriftPOS deployed. | Pre-Stage-1 dry run |
| Phase B early | 6-9 | Remaining 78 controls remediated to passable state. | Stage 1 audit (gap analysis) |
| Phase B mid | 9-12 | Stage 2 observation begins. DriftPOS GA at month 12. | Stage 2 observation in progress |
| Phase B end | 12-18 | Observation continues. Eager cohort fully migrated. | Certificate issued at month 18 |
| Phase C | 18+ | Surveillance audits annually. SOC 2 Type II observation in parallel. | Continuous compliance monitoring |

## Cross-references

- `02-iso27001-gap-assessment.xlsx` — control-by-control workload estimator (authoritative)
- `crb-skills/saas-acquisition-diligence/reference/02-iso27001-2022-control-library.md` — full Annex A library
- `crb-skills/saas-acquisition-diligence/reference/03-gcp-control-mapping.md` — GCP-native implementation per control
- `Brain/diligence/rapidpos/03-gcp-onramp-architecture.md` — proposed GCP target architecture
- `Brain/diligence/rapidpos/04-valuation-impact.md` — gap-to-discount math
- `Brain/diligence/rapidpos/05-driftpos-launch-readiness.md` — DriftPOS-blocking subset detail
