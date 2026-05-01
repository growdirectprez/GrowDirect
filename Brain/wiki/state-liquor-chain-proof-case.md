---
date: 2026-04-29
type: wiki
status: active
tags: [canary, target, archetype, regulated-beverage, control-state, liquor, mcp, vsm, counterpoint, vertical, item-authorization, regulatory-zone, ttb, abc]
sources: [Brain/wiki/counterpoint-market-gtm-proposal.md, Brain/wiki/rapid-pos-counterpoint-market-research-tam.md]
last-compiled: 2026-04-29
needs-review: 2026-05-13
method-role: Writer
method-stage: close
---


**Wiki:** [[Brain/Home|Home]]

# State Liquor Chain — Proof Case (Archetype)

> **Framing.** This page describes the canonical Ideal Customer Profile for Canary's Regulated Beverage vertical, framed as a deployment archetype rather than a named control-state authority. The capability set was designed against this profile; specific named-customer engagements may be added under signed reference agreements as the program matures.

## Summary

The state liquor chain archetype is the lead proof case for Canary's Regulated Beverage vertical on NCR Counterpoint. A control-state alcoholic beverage authority — a quasi-governmental entity operating somewhere between 100 and 600+ retail outlets, multi-billion-dollar gross receipts, and a regulatory exposure surface that includes federal TTB, state ABC, county/municipal ordinance, state auditor, legislative auditor, and (depending on the state) the office of the governor. No private-sector retailer in any vertical carries this much regulatory weight per dollar of revenue.

This is the hardest evidentiary-rail customer in the Counterpoint installed base. The platform that solves it has solved every regulated-beverage retailer simultaneously.

## Archetype Profile

| Dimension | Detail |
|---|---|
| Entity type | Control-state alcoholic beverage authority (quasi-governmental) |
| Scale | 100–600+ retail outlets, $500M–$3B+ gross receipts |
| Ownership | State agency or state-chartered authority |
| Markets | Single state, multi-county, every population density from urban to remote rural |
| Format | State-operated liquor stores · agency stores · licensee distribution · direct shipping where authorized |
| Regulatory layer | Federal TTB · State ABC · county/municipal · state auditor · legislative auditor · executive oversight · public records / FOIA |

The archetype is not theoretical. Seventeen US states operate as control states with some form of state authority over wholesale or retail alcoholic beverage distribution. Several of these states' retail networks run on Counterpoint or comparable specialty SMB ERPs because the existing footprint predates the migration to enterprise platforms — and the political and procurement complexity of a wholesale replacement is prohibitive.

## Why This Archetype

The control-state authority has every problem private retail has, plus four that no private retailer carries:

1. **Excise tax accuracy is a public records exposure.** Every transaction is a tax event. Every reconciliation discrepancy is potentially a published audit finding. The state auditor and legislative auditor both have unconditional access. A single uncategorized SKU can trigger a multi-month inquiry.

2. **Cash handling is a structural loss-prevention problem at scale.** Some stores in remote regions are 60%+ cash. Cash variances at this scale, across this many stores, are a top-of-fold operational concern that the existing POS parameter file approach cannot solve.

3. **Item authorization is mandated by law, not policy.** Age gating, hours-of-sale restrictions, day-of-week restrictions, county-by-county wet/dry/limited rules, and special-order authorization all encode in state statute. The system either enforces them or the state is in non-compliance with its own law.

4. **Procurement decisions are public.** Every vendor relationship is procurement-bid. Every system replacement is procurement-bid. The conversation is not with a CIO; it is with a procurement officer and a steering committee that includes the state auditor's office.

This is the operating environment Canary's evidentiary rail was built for. The hash-anchored receipt chain is not a feature; it is the answer to "show me your records" from an auditor who can subpoena them.

## What ALX Does at the State Liquor Chain

A store associate in a county that just shifted from "limited" to "wet" needs to know: which SKUs are now sellable here, what hours, with what age verification protocol? A district manager needs to reconcile yesterday's till variance across forty stores before the daily close. The state auditor's office requests every transaction in a five-store region for the past quarter, with the till reconciliation at end of day.

Without ALX: the question routes through a regional supervisor, an HQ compliance officer, and the IT operations team. The audit request becomes a six-week records production. The till reconciliation is a manual spreadsheet against the daily POS extract.

With ALX:
- The county wet/dry change updates the site regulatory zone configuration in bulk. Every authorization query for affected stores reflects the new rule on the next transaction.
- The till variance reconciliation runs continuously against the receipt chain. Variances surface in the LP queue at the moment they occur, not at end of day.
- The audit request is a query against the receipt chain. Hash-verified evidence is producible in minutes, not weeks. The auditor can verify the chain without trusting the authority — or trusting Canary.

## VSM Feature Set

| Feature | What it does |
|---|---|
| Statutory item authorization | Encode state alcoholic beverage code, county ordinances, hours/days of sale, age thresholds as a single contract query. Enforced at every transaction touchpoint. |
| Wet/dry/limited zone management | County- and municipality-level regulatory zone configuration. Statutory or ordinance change → bulk site update → next transaction enforces it. |
| Excise tax reconciliation | Tax category attached to every transaction at write time. Daily, monthly, and quarterly excise tax accruals computed from the receipt chain, not from a downstream extract. |
| Special-order workflow | Customer special-order intake, approval, allocation, and delivery. Persistent customer context across the network for multi-store fulfillment. |
| Cash handling and variance | Real-time till reconciliation against the receipt chain. Variance surfaces at the moment it occurs. LP investigator gets context, not a spreadsheet. |
| Hours-of-sale enforcement | POS will not accept a transaction outside authorized hours. Holiday and special-day exceptions encoded once at the authority level, applied to all sites. |
| Audit-ready receipt chain | Hash-anchored, sequenced event log. State auditor, legislative auditor, TTB inspector, FOIA requester — all served from the same chain with cryptographic verification. |
| Public records compliance | FOIA-class queries against transaction history are computationally trivial; the receipt chain is the system of record. |
| Vendor procurement contract integration | EDS three-way match against vendor procurement contracts. PO/ASN/receipt/invoice reconciled at write time. Vendor disputes become evidentiary, not adversarial. |

## The Domain Knowledge Vault

The control-state archetype encodes regulatory knowledge that today lives in agency directives, compliance memoranda, and the institutional memory of long-tenured store managers:

- State alcoholic beverage code: every statute as a structured rule set
- County and municipal ordinance library: wet/dry/limited × hours × days × special restrictions
- Excise tax rules: federal TTB schedules + state schedules + local override
- Vendor licensing database: which suppliers are authorized for which categories at which sites
- Hours-of-sale calendar: standard schedule + holiday/election-day/special-event overrides
- Age verification protocols: ID type by transaction type by jurisdiction
- Special-order workflow: customer authorization, fulfillment, restricted-allocation enforcement
- Cash handling protocols: counting, reconciliation, deposit, variance escalation
- Audit response playbook: standard query patterns from auditors and how to fulfill them

## Strategic Fit

| Dimension | Assessment |
|---|---|
| NCR Counterpoint probability | Moderate-to-high — Counterpoint and comparable specialty SMB ERPs are common in control-state retail networks that predate enterprise consolidation |
| VAR channel coverage | Mixed — depends on state; some control states use specialty Counterpoint VARs (RBMS, AMS Retail), others use direct enterprise vendor relationships |
| Domain knowledge depth | Exceptional — every transaction is a regulated event; every store is a public records surface |
| MCP gap | Total — no agent layer exists in control-state retail; compliance lives in directives, memoranda, and HQ phone trees |
| Ownership | Mixed — quasi-governmental entities operate with steering committees, procurement officers, and political stakeholders rather than CIOs |
| Multi-location scale | Right — 100–600+ stores is a real distribution, LP, and audit problem |
| Procurement complexity | High — engagement is procurement-bid, not direct contract; engagement timeline is months to years, not weeks |
| Strategic value | Maximum — a control-state reference closes every regulated-beverage retailer in the Counterpoint installed base |

## Engagement Path

The state liquor chain archetype is not a self-service signup, not a 90-day pilot, and not a conventional transformation engagement. The path:

1. **Procurement entry** — engagement initiates through a state procurement process, an agency RFI/RFP, or an existing-vendor channel partnership. Direct CIO outreach is rarely the entry point.
2. **Audit/health check (8–12 weeks)** — diagnostic against the authority's transaction history, inventory positions, AP records, and audit-finding history. Surfaces the current evidentiary exposure. Quantifies the audit production cost.
3. **Constrained pilot (3–6 stores, 6 months)** — in-state, single-region pilot to demonstrate the receipt chain, the till reconciliation, and the statutory authorization enforcement. The pilot site selection is political; expect the steering committee to drive it.
4. **Transformation engagement (12–24 months, SI-partner-led)** — implement Canary against the audit baseline. The SI partner owns delivery; the platform stays after the project closes.
5. **Operating-system mode (year 3+)** — Canary becomes the retail backbone. The on-premise backoffice infrastructure is retired. The authority operates from the platform's dashboard. Public records production becomes a query.

Engagement timelines are longer than private-sector targets. Engagement values are larger by an order of magnitude. The reference value of a successful control-state engagement is the highest in the Counterpoint installed base.

## Sensitivities and Constraints

The control-state archetype carries sensitivities that private-sector targets do not:

- **No named-entity content in published material** until a signed reference agreement is in place
- **Procurement neutrality** — discussion of platform capabilities must avoid implying any predisposition toward a named state authority
- **Political stakeholder visibility** — engagement may surface in legislative sessions, governor's office briefings, and public records
- **Data residency** — many control states require data residency within the state or within the United States. Canary's GCP-native posture supports this; the requirement is non-negotiable
- **Vendor due diligence** — expect extensive financial, security, and operational due diligence as part of any procurement process

Per the platform's content policy, this proof case remains archetype-framed. Specific named-customer engagements will be added only under signed reference agreements.

## Open Questions

- Which control states currently operate retail networks on NCR Counterpoint or comparable specialty SMB ERPs?
- Which Counterpoint VARs (RBMS, AMS Retail, others) currently serve control-state customers, and which relationships are warm?
- Is there a state procurement entry path through an existing GrowDirect or VAR partner relationship?
- Which control states have published or in-flight modernization initiatives that align with the platform's GCP-native, evidentiary-rail posture?
- Is there a friendly steering-committee or auditor-office contact who could shape an early-stage RFI?

## Related

- [[Brain/wiki/counterpoint-market-gtm-proposal|Counterpoint Market GTM Proposal]]
- [[Brain/wiki/armstrong-garden-centers-proof-case|Armstrong Garden Centers — Proof Case]]
- [[Brain/wiki/murdochs-ranch-home-supply-proof-case|Murdoch's Ranch & Home Supply — Proof Case]]
- [[Brain/wiki/rapid-pos-counterpoint-market-research-tam|Rapid POS Counterpoint TAM]]
- [[Brain/wiki/canary-mcp-stack-architecture|MCP Stack Architecture]]

## Sources

- `Brain/wiki/counterpoint-market-gtm-proposal.md` (Pillar 3 of three-pillar GTM motion)
- `Brain/wiki/rapid-pos-counterpoint-market-research-tam.md` (TAM analysis — control state retail networks within Counterpoint installed base)
- Public domain regulatory references: federal TTB schedules, state ABC structures, control-state organizational filings (no named-entity engagement content)
