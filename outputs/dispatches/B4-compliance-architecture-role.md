# B4 — Compliance-Architecture Lead Role Scope

**Dispatch:** B4 in `outputs/session-summary-and-company-formation-epic.md` (Category B — Communication / Buy-in)
**Status:** Role definition — to be filled by named lead in Phase A
**Reporting line:** Founder, in capacity as CTO of RapidPOS (transition window) and President of Retail at GrowDirect (long-term)
**Tier:** Contributor-tier; principal-tier elevation possible per the trusted network's evolution
**Compensation:** Substrate-native — token-earn + L402 + relevant cash for runway (detail below)

---

## Why this role exists structurally

The eljeffe Hash and Seal Protocol substrate produces audit-defensible evidence by construction. The substrate's evidence trail — block-height-anchored decisions, hash-chained transaction pipeline, lineage-tracked governance, transparent treasury — exceeds what conventional ISMS frameworks specify because it produces immutable evidence by mathematics rather than by retained custody.

What the substrate cannot do by itself is *translate*. ISO 27001 auditors expect documentation patterns built for institutional record-keepers. PCI-DSS QSAs expect cardholder-data-flow diagrams that look like SaaS deployments. SOC 2 examiners expect continuous-monitoring evidence that maps to the AICPA trust services criteria. The substrate's mathematical evidence has to be presented in their language, against their frameworks, with their expected artifacts.

That translation is the compliance-architecture lead's work. The role is not "do compliance" — the substrate already does compliance. The role is to make the substrate's compliance posture legible to auditors, regulators, and customers who measure compliance by conventional standards.

This is why "compliance officer" is the wrong title. The conventional compliance officer enforces a process layered on top of an organization that doesn't natively produce evidence; the role defaults to documenting what people are doing wrong and asking them to do it differently. The compliance-architecture lead works in the other direction — they document what the substrate is doing right, and they help auditors recognize it.

## Scope of work

### Substrate-to-auditor translation

For each major audit framework the namespace engages with (ISO 27001:2022, PCI-DSS, SOC 2 Type II, plus relevant state privacy laws): produce the artifacts the framework expects, sourced from the substrate's existing on-chain evidence and adjacent off-chain operational artifacts.

For ISO 27001:2022 specifically:

- Map each of the 93 Annex A controls to the substrate's mechanism that satisfies it (per the diligence-skill reference at `crb-skills/saas-acquisition-diligence/reference/03-gcp-control-mapping.md` for the GCP-side mapping; per `crb-skills/namespace-bylaws/reference/07-alignment-checks.md` for the substrate-side checks)
- For controls where the substrate's mechanism exceeds the standard's expectation, produce the explanatory artifact that demonstrates why
- For controls where remediation is genuinely required, scope the engineering work, attach the cost (per `crb-skills/saas-acquisition-diligence/templates/workload-estimator.xlsx`), sequence into the program plan
- Maintain the ISMS framework documentation (policy framework + governance structure that ties the controls together — roughly 200-400 hours separate from per-control remediation per the gap-assessment artifact)
- Coordinate Stage 1 audit (gap analysis), Stage 2 observation period start, certificate issuance, surveillance audit cadence

For PCI-DSS:

- Confirm Ingenico tokenization keeps cardholder data out of the namespace's scope (out of Canary.GO, out of CRDM, out of any cloud workload that isn't the pinpad device itself)
- Produce the SAQ-A or SAQ-A-EP attestation as appropriate
- Maintain the position document for any customer questionnaire response
- For any customer that requires a higher SAQ level (or full Level 1 attestation for a Global-50 anchor), scope the additional engineering work and price into the deal

For SOC 2 Type II:

- Identify the Trust Services Criteria relevant to the substrate (Security and Availability minimum; Processing Integrity, Confidentiality, Privacy as customer demand surfaces)
- Coordinate observation-period setup (target start: M18 per the program sequence in `crb-skills/saas-acquisition-diligence/Brain/diligence/rapidpos/02-iso27001-gap-assessment.md`)
- Maintain the continuous-compliance evidence layer (Vanta or Drata as the GRC-dashboard tool; SCC Premium + Cloud Audit Logs + Chronicle as the evidence sources per the GCP onramp architecture)

For state privacy laws (CCPA / CPRA / VCDPA / CPA / CDPA, etc.):

- The substrate is structurally easier to defend because customer-as-owner is the answer to most of these laws' core asks (per the v2 prompt's "data-sovereignty-architecture" companion-skill scope)
- The lead's work is to produce the documentation pattern that a state attorney general's office or a customer's outside counsel will recognize as compliant

### PCI scope ownership

Direct ownership of the PCI-DSS scope position. The substrate's structural commitment is that no cloud workload other than the pinpad device touches cardholder data; the lead's work is to maintain that commitment as the substrate evolves. Specifically:

- Review every new cloud workload before deployment for any potential cardholder-data exposure
- Maintain the cardholder-data-flow diagram in PCI-acceptable form
- Coordinate with Ingenico (via Bart's team for DriftPOS deployments) on the P2PE attestation lifecycle (annual; verify each renewal covers all production deployment shapes)
- Review every customer questionnaire response that touches PCI scope before it goes back to the customer
- Defer to engaged outside QSA counsel for any genuinely novel scope question; the lead is not a QSA but is the in-substrate authority on what the substrate's PCI position is

### ISO 27001 + SOC 2 prep

Per the program sequencing in the diligence run:

- M0-M6 Phase A: drive remediation of the 15 DriftPOS-blocking critical-mass controls (~520 hours / ~$104k engineering); draft ISMS policy framework
- M6 internal readiness review; M9 Stage 1 audit (gap analysis); ISO27001 certificate target M18
- M18+ SOC 2 Type II observation period start; SOC 2 Type II certified target M30
- Annual surveillance audits thereafter; integrate into the namespace's annual alignment-review cadence (per `crb-skills/namespace-bylaws/templates/alignment-review.md`)

### GCP control mapping

Per the GCP onramp architecture (`crb-skills/saas-acquisition-diligence/Brain/diligence/rapidpos/03-gcp-onramp-architecture.md`), the substrate runs on 18 workloads on GCP. Each workload's IAM, encryption, logging, and monitoring posture maps to specific ISO 27001 + SOC 2 + PCI controls.

The lead maintains:

- The control-to-GCP-service mapping (e.g., Annex A 5.15 Access Control → Cloud IAM + Cloud Identity 2SV; 8.13 Information Backup → Cloud SQL HA + cross-region snapshots + drill log)
- The evidence-collection plan (which Cloud Audit Logs / SCC Premium findings / Chronicle alerts feed which control's evidence requirement)
- The per-workload security review at deployment (every new workload reviewed before production deployment; any finding requiring remediation flagged as a dispatch under the relevant control)

### NICS-attestation regulatory engagement (federal + Wyoming)

Per epic dispatch G4, the namespace pursues ATF / FBI-CJIS acknowledgment that zero-knowledge cryptographic attestations satisfy 27 CFR 478 record-keeping requirements. This is a 12-24-month parallel-compliance track (paper Form 4473 continues during transition; substrate attestations run alongside; eventual ATF/CJIS recognition replaces the paper requirement where granted).

The lead's role:

- Coordinate with Wyoming counsel + ATF/CJIS counsel (point-in-time engagements) on regulatory submissions
- Maintain the technical specification of the NICS-attestation mechanism (the zero-knowledge proof construction, the substrate's role in the attestation lifecycle, the ATF-defensible evidence trail)
- Coordinate with UW academic partners (per epic dispatch G1) on the academic-edition treatment of the NICS-attestation framework — peer-reviewed publication strengthens the regulatory engagement
- Maintain parallel-compliance posture during the transition window; coordinate with firearms-vertical pilot customers (per epic dispatch D2) on the dual-record period

## Deliverables in Phase A (months 0-6)

By the close of Phase A, the lead has produced:

1. **PCI scope position document** — substrate-wide cardholder-data flow diagram; SAQ eligibility analysis; first formal customer-questionnaire response template (E1 dispatch acceptance criterion)
2. **ISO 27001 readiness assessment** — 93-control gap inventory using the workload-estimator from the diligence skill; critical-mass 15 sequenced into Phase A; full 93 sequenced into Phase B (E2 dispatch acceptance criterion)
3. **ISMS policy framework v1** — documented per ISO 27001 expectation; ratified through the bylaws iteration loop where the policy intersects governance
4. **GCP control-mapping reference document** — every Annex A control mapped to its GCP-native implementation per the diligence-skill reference + adjacent reference artifacts
5. **NICS-attestation regulatory submission v0** — initial communication to ATF + CJIS scoping the attestation framework; Wyoming counsel coordination plan
6. **First compliance-architecture-operations runbook** — how the lead's work integrates with the bylaws iteration loop, the alignment-check harness, and the namespace's annual review cadence

In Phase B (months 6-18):

7. **ISO 27001 Stage 1 audit pass** (M9)
8. **DriftPOS GA compliance gate cleared** (M12)
9. **ISO 27001 certificate issued** (M18)
10. **SOC 2 Type II observation period started** (M18)

In Phase C (months 18+):

11. **SOC 2 Type II certified** (target M30)
12. **NICS-attestation ATF/CJIS recognition track milestone** (target M24-M36)
13. **Surveillance-audit cadence stable** (annual; integrated into namespace alignment review)

## Compensation structure

Per the substrate's no-shared-services posture (per `crb-skills/namespace-bylaws/reference/09-anti-patterns.md` Pattern A and Pattern D), the lead is not a salaried department head. Compensation is substrate-native:

**Token-earn.** The lead earns tokens for contribution to the namespace per the L402 marketplace mechanism. Each compliance-architecture deliverable (PCI scope document, ISO 27001 gap assessment, control-mapping reference, audit prep coordination, etc.) is published as an MCP-able output and earns tokens proportional to its consumption by the namespace and its trusted-network counterparties.

**L402 micropayment flow.** Specific compliance-architecture services published by the lead (e.g., "review this customer questionnaire response," "validate this new cloud workload against ISO controls," "produce a SAQ-A response for this customer's PCI questionnaire") are L402-gated MCP ports. Customers and partner-network entities pay sat to invoke; payment routes to the lead's wallet; service is delivered.

**Cash for runway.** The lead's compensation is not all sat. A cash component sized to support personal runway is part of the engagement — paid from the namespace's treasury (per `crb-skills/namespace-bylaws/reference/03-dao-treasury-patterns.md` Operations cash-out category, where applicable; or Personal-compensation cash-out for the contributor-tier portion). The cash component reflects what the lead needs to commit fully without burning personal runway — same logic the founder applies to the dual-role founder-CTO compensation in `outputs/memo-to-principals-retail-vertical.md`.

**Lineage tier.** The lead enters as contributor-tier (lineage depth 1 by default; specific tier set at engagement). Phase 2 elevation to principal-tier (genesis-equivalent voting weight) is possible if the trusted network ratifies it, with the lead's stake protected per `crb-skills/namespace-bylaws/reference/05-phase-transitions.md` (lineage permanence; founder-removal protections apply once at principal tier).

**No vesting cliff.** Token-earn is permanent at contribution per `crb-skills/namespace-bylaws/reference/03-dao-treasury-patterns.md`. There is no four-year vesting; there is no cliff; there is no clawback (per `09-anti-patterns.md` Patterns B and I).

## Reporting and accountability

- **Reports to:** Founder, in capacity as CTO of RapidPOS during the transition window; transitions to reporting to the President of Retail at GrowDirect for the long-term role
- **Coordinates with:** Ops principal (third principal, TBD per epic open decision #1) on cloud architecture; Domain principal (founder) on substrate-to-auditor translation specifics; Governance principal (Tim) on bylaws-intersecting policy work
- **Engages externally:** Point-in-time engaged ISO/SOC 2 audit firm; QSA for PCI-related questions; Wyoming counsel + ATF/CJIS counsel for NICS-attestation regulatory work; UW academic partners for the academic-edition treatment
- **Visibility:** All compliance-architecture work product is on chain or in the namespace's transparent operational store; the trusted network sees what is being produced and at what cadence

## Termination and transition

The lead can step away at any time per the substrate's no-cliff design. Their token-earned position remains theirs (lineage permanence; cash-out per the categorized taxonomy). The role does not have a non-compete (the substrate's anti-extraction posture per `09-anti-patterns.md` Pattern J prevents one).

If the trusted network determines a different lead is needed (per the founder-removal protections in `crb-skills/namespace-bylaws/reference/05-phase-transitions.md` if the lead has been elevated to principal-tier), the process follows the same lineage-weighted-vote + notice-period + cause-documentation pattern as any role removal. The lead's stake remains theirs; the operational role transitions cleanly.

## Open items requiring resolution before role is filled

1. **Specific candidate identification.** The role is defined here; the named individual is not. Founder + Tim alignment required (per epic dispatch B2, B4 dependency on B1).
2. **Cash-component sizing.** The runway-supporting cash component needs a specific dollar range. Tied to the namespace's treasury position at engagement; revisit at Phase 1 close.
3. **Tier elevation timing.** Default contributor-tier entry. If the lead is genuinely the third principal candidate (epic open decision #1), the role enters at principal-tier from day one; if not, contributor-tier with Phase 2 elevation possible.
4. **Compliance-officer-vs-architect lexical choice.** "Compliance-architecture lead" is the working title that captures the substrate-native posture. "Compliance officer" is the conventional title that would map cleanly in an external audit context. The role's external-facing title may differ from its substrate-internal title; founder + lead resolve before any external-facing artifact references the role.

## Cross-references

- `outputs/session-summary-and-company-formation-epic.md` — Category B dispatches (B1 Tim conversation precedes; B2 third principal identification adjacent; B4 this dispatch)
- `outputs/memo-to-principals-retail-vertical.md` — the no-shared-services posture and the substrate-as-HR-replacement framing
- `outputs/position-paper-eljeffe-io.md` — the substrate the lead operationalizes against external frameworks
- `crb-skills/namespace-bylaws/reference/{02, 03, 05, 07, 09}.md` — the substrate primitives the lead references in compliance work
- `crb-skills/saas-acquisition-diligence/Brain/diligence/rapidpos/{02, 03, 05}.md` — the ISO 27001 gap, GCP onramp architecture, and DriftPOS launch readiness this lead operationalizes
- `crb-skills/saas-acquisition-diligence/reference/{02, 03, 06}.md` — the ISO 27001 control library, GCP control mapping, and valuation-impact formulas the lead works with

---

*Compliance-architecture lead role scope. Ready for the named candidate.*
*King Harbor — Redondo Beach — pier.*
