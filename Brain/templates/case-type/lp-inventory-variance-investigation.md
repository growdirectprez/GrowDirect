---
case-type-id: lp-inventory-variance-investigation
name: LP Inventory Variance Investigation
description: An in-depth investigation conducted when an excessive inventory variance is identified, with successful resolution as the closure target.
class: LP
visibility: LP
trigger: scheduled-cadence
cadence-tier: daily-batch
owners:
  corp-side-role: SSC LP Investigator
  store-side-role: Store Manager
sla:
  initial-response: 24h
  resolution: 30d
  escalation-after: 45d
required-fields:
  - name: store-id
    type: string
    required: true
  - name: variance-amount-usd
    type: number
    required: true
  - name: variance-units
    type: number
    required: true
  - name: variance-category
    type: enum
    enum: [shrink, count-error, receiving-error, transfer-mismatch, system-error, other]
    required: true
  - name: source-of-info
    type: enum
    enum: [cycle-counts, lptv, tip-associate, tip-customer, tip-hotline, tip-anonymous, observation, implication, other]
    required: true
  - name: initial-narrative
    type: freetext
    required: true
  - name: video-evidence-attached
    type: boolean
    required: false
  - name: cycle-count-id
    type: string
    required: false
state-machine:
  states: [open, investigating, evidence-review, resolved-with-cause, resolved-unfounded, escalated, canceled]
  transitions:
    - from: open
      to: investigating
      guard: assigned-to-investigator
    - from: investigating
      to: evidence-review
      guard: investigation-complete
    - from: evidence-review
      to: resolved-with-cause
      guard: cause-attested
    - from: evidence-review
      to: resolved-unfounded
      guard: no-finding-attested
    - from: investigating
      to: escalated
      guard: variance-exceeds-threshold OR external-pattern-detected
routing-rules:
  initial-assignment: SSC LP Investigator on rotation; auto-assigned by store region
  escalation-policy: At 45d unresolved → DLPM (District LP Manager); at $50k+ variance → SSC LP Director
closure-criteria:
  required-attestations:
    - investigator-attests-cause-or-unfounded
    - store-manager-acknowledges-finding
    - corrective-action-documented (if applicable)
  outcomes:
    - resolved-with-cause
    - resolved-unfounded
    - escalated-to-external (if criminal pattern detected)
anchor-points:
  - case-create
  - state-transition-investigating
  - state-transition-evidence-review
  - case-close-resolved-with-cause
  - case-close-resolved-unfounded
  - state-transition-escalated
related-modules:
  - canary-hawk
  - canary-fox
  - canary-chirp
  - canary-inventory
  - canary-bull
  - canary-employee
  - canary-blockchain-anchor
sources:
  - Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md (DSG row 64; Class=Incident, Type="Inventory Variance Investigation")
  - Brain/raw/.extract/CaseManagement/Actions.xlsx.md (lifecycle outcomes)
  - Brain/raw/.extract/CaseManagement/Source of Info.xlsx.md (trigger taxonomy)
last-compiled: 2026-05-02
needs-review: false
---

# Case Type: LP Inventory Variance Investigation

## What this is

An investigation triggered when a store's cycle count surfaces an inventory variance exceeding the merchant's threshold. The case carries the variance details, the source of information that flagged it, the investigator's findings, and the resolution outcome. Inheritance from DSG `Incident Types.xlsx` row: *"Incidents where an excessive inventory variance is identified, an in depth investigation is conducted, and a successful resolution is obtained."*

## When it fires

Daily-batch cadence. After overnight cycle counts complete, [[canary-bull]] reconciles physical-vs-system stock; variances exceeding the merchant-configured threshold (default $500 or 5% of category SOH) trigger this case type via `hawk.create_case` from a chirp rule. Manual creation by an LP investigator is also supported via the same MCP tool.

## Who owns it

| Side | Role | Responsibility |
|---|---|---|
| Corp | SSC LP Investigator | Investigates evidence, attests cause, drives resolution |
| Store | Store Manager | Provides operational context, executes corrective action, attests acknowledgement |

## Form fields (required at create time)

| Field | Type | Required | Validation | Notes |
|---|---|---|---|---|
| store-id | string | yes | merchant tenant scope | Auto-populated when chirp fires the case |
| variance-amount-usd | number | yes | ≥ threshold | From bull reconciliation |
| variance-units | number | yes | integer | From bull reconciliation |
| variance-category | enum | yes | shrink / count-error / receiving-error / transfer-mismatch / system-error / other | Initial guess; refined during investigation |
| source-of-info | enum | yes | DSG taxonomy | cycle-counts / lptv / tip-* / observation / implication / other |
| initial-narrative | freetext | yes | ≥ 50 chars | Investigator's first-pass narrative |
| video-evidence-attached | boolean | no | — | Set true if LPTV linked |
| cycle-count-id | string | no | references inventory.cycle_counts | Auto-populated when triggered by cycle count |

## State machine

```
open ─→ investigating ─→ evidence-review ─┬→ resolved-with-cause
                  │                       ├→ resolved-unfounded
                  └─────────────────────→ escalated
                                          └→ canceled (rare; reason required)
```

| Transition | Guard | Anchored to Fox? |
|---|---|---|
| open → investigating | Assigned to investigator | yes |
| investigating → evidence-review | Investigation narrative + evidence attached | yes |
| evidence-review → resolved-with-cause | Investigator attests cause | yes (+ blockchain anchor) |
| evidence-review → resolved-unfounded | Investigator attests no finding | yes (+ blockchain anchor) |
| investigating → escalated | Variance > $50k OR external-pattern detected | yes |

## SLA

| Stage | Time | Escalation |
|---|---|---|
| Initial response (open → investigating) | 24h | Auto-reassign at 24h to next investigator on rotation |
| Resolution (any → resolved-* / escalated) | 30 business days | DLPM notification at 30d |
| Hard escalation | 45 business days | SSC LP Director |

## Closure criteria

| Outcome | Definition | Anchored to Fox + Bitcoin? |
|---|---|---|
| resolved-with-cause | Investigator identifies root cause (shrink, count error, receiving error, transfer mismatch, system error). Corrective action documented if applicable. | yes |
| resolved-unfounded | Investigation completed; no actionable cause identified. Variance written off to expected loss. | yes |
| escalated-to-external | Criminal pattern detected; case referred to law enforcement and/or external counsel. Closure is on external-handoff attestation. | yes |

## Anchor points

- [x] case create → Fox event (variance detected, store, amount, source)
- [x] state transition: open → investigating → Fox event (assigned)
- [x] state transition: investigating → evidence-review → Fox event (evidence attached)
- [x] state transition: evidence-review → resolved-* → Fox event + Bitcoin L2 anchor
- [x] state transition: investigating → escalated → Fox event
- [x] attachment added (video, photo, document) → Fox event

## Related modules

| Module | Relationship |
|---|---|
| canary-hawk | runs this case type |
| canary-fox | evidence anchor on state transitions |
| canary-chirp | fires the case via detection rule on variance threshold |
| canary-inventory | source of cycle-count and variance data |
| canary-bull | reconciliation engine that flagged the variance |
| canary-employee | investigator and store-manager identity / SLA enforcement |
| canary-blockchain-anchor | Bitcoin L2 anchor for close events |

## Reports

- Open Analyst Investigations (DSG corpus prior-art report; weekly rollup of open cases by investigator)
- Weekly Recap (aggregate variance closed by region, week-over-week trend)
- Yearly Case Extract (full case detail export for audit / insurance)
- MTTR by store/region (operational health metric)

## Sources

- DSG `Incident Types.xlsx` row 64: Class=Incident, Type="Inventory Variance Investigation," Definition: *"Incidents where an excessive inventory variance is identified, an in depth investigation is conducted, and a successful resolution is obtained."* (`Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md`)
- DSG `Actions.xlsx` lifecycle outcomes (`Brain/raw/.extract/CaseManagement/Actions.xlsx.md`)
- DSG `Source of Info.xlsx` trigger taxonomy (`Brain/raw/.extract/CaseManagement/Source of Info.xlsx.md`)

## See also

- Card: [[canary-hawk]] — the universal envelope
- Card: [[platform-case-type-registry-pattern]] — the pattern this instance demonstrates
- Card: [[canary-chirp]] — the detection rule that fires this case
- Card: [[canary-bull]] — the reconciliation engine that produces the variance signal
- Template: `Brain/templates/case-type.md` — the schema this instance fills
