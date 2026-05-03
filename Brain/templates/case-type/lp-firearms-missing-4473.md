---
case-type-id: lp-firearms-missing-4473
name: LP Firearms — Missing 4473
description: Critical Smart Alert when a store cannot locate a Form 4473 for a firearm sold at that location, triggering immediate investigation and ATF notification per 27 CFR 478.124.
class: LP
visibility: LP
trigger: real-time-event
cadence-tier: stream
owners:
  corp-side-role: SSC LP Investigator
  store-side-role: Store Manager + FFL Compliance Officer
sla:
  initial-response: 4h
  resolution: 30d
  escalation-after: 60d
required-fields:
  - name: store-id
    type: string
    required: true
  - name: firearm-serial
    type: string
    required: true
  - name: firearm-manufacturer
    type: string
    required: true
  - name: firearm-model
    type: string
    required: true
  - name: ebound-book-acquisition-id
    type: string
    required: true
  - name: ebound-book-disposition-id
    type: string
    required: false
  - name: customer-of-record
    type: string
    required: false
  - name: discovery-context
    type: enum
    enum: [atf-audit, internal-cycle-count, customer-complaint, post-incident-trace, voluntary-disclosure]
    required: true
  - name: search-locations-attempted
    type: array
    required: true
  - name: video-evidence-attached
    type: boolean
    required: false
state-machine:
  states: [open, investigating, evidence-review, resolved-form-recovered, resolved-firearm-recovered, escalated-to-atf, canceled]
  transitions:
    - from: open
      to: investigating
      guard: assigned-to-investigator
    - from: investigating
      to: evidence-review
      guard: search-completed-or-traced
    - from: evidence-review
      to: resolved-form-recovered
      guard: form-located-and-validated
    - from: evidence-review
      to: resolved-firearm-recovered
      guard: firearm-located-and-form-reconstructed
    - from: investigating
      to: escalated-to-atf
      guard: form-unrecoverable AND firearm-unrecoverable
routing-rules:
  initial-assignment: SSC LP Investigator on rotation; auto-assigned by store region; Store FFL Compliance Officer immediately notified
  escalation-policy: At 60d unresolved → SSC LP Director + General Counsel; at any "trace request received" event → ATF Liaison immediately
closure-criteria:
  required-attestations:
    - investigator-attests-resolution
    - store-manager-acknowledges-finding
    - ffl-compliance-officer-attests-bound-book-reconciled
    - if-escalated-to-atf-trace-confirmation
  outcomes:
    - resolved-form-recovered
    - resolved-firearm-recovered
    - escalated-to-atf (and ATF case ID recorded)
anchor-points:
  - case-create
  - state-transition-investigating
  - state-transition-evidence-review
  - case-close-resolved-form-recovered
  - case-close-resolved-firearm-recovered
  - state-transition-escalated-to-atf
  - atf-notification-event
related-modules:
  - canary-hawk
  - canary-fox
  - canary-blockchain-anchor
  - canary-compliance
  - canary-item
  - canary-employee
sources:
  - Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md (DSG row 13; Class=Critical Smart Alert; Type="Missing F4473")
  - Brain/templates/regulation-spec/federal-atf-4473.md (federal regulation this enforces)
  - 27 CFR 478.124, 478.125
last-compiled: 2026-05-02
needs-review: false
---

# Case Type: LP Firearms — Missing 4473

## What this is

A Form 4473 — the federal record of a firearm transfer — cannot be located at the FFL premises for a firearm shown as transferred in the eBound Book. Direct adoption of DSG LPMS row 13: *"SMART ALERT: When a store cannot locate a form 4473 for a gun sold at that location."* This is a high-stakes federal compliance event under 27 CFR 478.124 with FFL revocation risk; case opens at Critical Smart Alert tier and routes to FFL Compliance Officer immediately.

## When it fires

Stream-tier real-time event. Fires when:

- ATF compliance audit identifies a missing 4473 (most common context)
- Internal eBound Book cycle count flags an acquisition without matching disposition + form
- Customer complaint or trace request from ATF surfaces a transfer without a recoverable form
- Voluntary disclosure by store staff who discover the gap

## Who owns it

| Side | Role | Responsibility |
|---|---|---|
| Corp | SSC LP Investigator | Drives the investigation, attests resolution, coordinates with General Counsel and ATF Liaison if escalated |
| Store | Store Manager + FFL Compliance Officer | Conducts on-premises search, reconstructs records where possible, attests bound-book reconciliation |

## Form fields (required at create time)

| Field | Type | Required | Notes |
|---|---|---|---|
| store-id | string | yes | Auto-populated from event source |
| firearm-serial | string | yes | From eBound Book acquisition record |
| firearm-manufacturer | string | yes | From eBound Book |
| firearm-model | string | yes | From eBound Book |
| ebound-book-acquisition-id | string | yes | The A-record reference |
| ebound-book-disposition-id | string | no | The D-record if exists; missing if disposition itself is unclear |
| customer-of-record | string | no | If the eBound disposition has a customer name; populated by canary-customer if known |
| discovery-context | enum | yes | atf-audit / internal-cycle-count / customer-complaint / post-incident-trace / voluntary-disclosure |
| search-locations-attempted | array | yes | List of physical/digital locations searched |
| video-evidence-attached | boolean | no | If LPTV captured the original transfer |

## State machine

```
open ─→ investigating ─→ evidence-review ─┬→ resolved-form-recovered
                  │                       ├→ resolved-firearm-recovered
                  └─────────────────────→ escalated-to-atf
                                          └→ canceled (rare; reason required)
```

| Transition | Guard | Anchored to Fox + Bitcoin? |
|---|---|---|
| open → investigating | Assigned to investigator + FFL compliance officer notified | yes |
| investigating → evidence-review | Search completed or trace request fully scoped | yes |
| evidence-review → resolved-form-recovered | Form located and field-validated against eBound | yes (+ blockchain anchor) |
| evidence-review → resolved-firearm-recovered | Firearm located and form reconstructed per ATF guidance | yes (+ blockchain anchor) |
| investigating → escalated-to-atf | Both unrecoverable; ATF Liaison engages | yes (+ blockchain anchor) |

## SLA

| Stage | Time | Escalation |
|---|---|---|
| Initial response | 4h | Auto-reassign at 4h to next investigator on rotation |
| Resolution | 30 business days | SSC LP Director notification at 30d |
| Hard escalation | 60 business days | SSC LP Director + General Counsel + ATF Liaison |

## Closure criteria

| Outcome | Definition | Anchored? |
|---|---|---|
| resolved-form-recovered | Form located and field-validated; eBound Book reconciled | yes (Fox + Bitcoin L2) |
| resolved-firearm-recovered | Firearm located and form reconstructed per ATF guidance | yes |
| escalated-to-atf | ATF case ID recorded; trace cooperation; FFL Compliance Officer attests cooperation complete | yes |

## Anchor points

- [x] case create → Fox event (firearm serial, store, eBound ref, discovery context)
- [x] state transition: open → investigating → Fox event
- [x] state transition: investigating → evidence-review → Fox event (search completion)
- [x] state transition: evidence-review → resolved-* → Fox event + Bitcoin L2 anchor
- [x] state transition: investigating → escalated-to-atf → Fox event + ATF notification recorded
- [x] attachment added (video, photo, recovered form scan) → Fox event

## Related modules

| Module | Relationship |
|---|---|
| canary-hawk | runs this case type |
| canary-fox | evidence anchor on every transition |
| canary-compliance | hosts the federal-atf-4473 regulation entry; provides operator prompt |
| canary-item | firearm SKU and serialized inventory record |
| canary-employee | investigator and FFL compliance officer identity / SLA enforcement |
| canary-blockchain-anchor | Bitcoin L2 anchor for close events (audit-grade evidence) |

## Reports

- Open ATF Compliance Cases (real-time dashboard)
- Missing 4473 Resolution MTTR by store (operational health metric)
- Annual ATF Inspection Outcome rollup (audit-ready extract)
- Yearly Case Extract (full case detail export for FFL renewal + insurance)

## Sources

- DSG LPMS `Incident Types.xlsx` row 13: Class=Critical Smart Alert, Type="Missing F4473," Definition: *"SMART ALERT: When a store cannot locate a form 4473 for a gun sold at that location."* (`Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md`)
- 27 CFR 478.124 + 478.125 — federal recordkeeping requirements
- `Brain/templates/regulation-spec/federal-atf-4473.md` — the regulation this enforces
- DSG `Actions.xlsx` — closure outcome taxonomy (Reported to ATF)

## See also

- Card: [[canary-hawk]]
- Card: [[platform-case-type-registry-pattern]]
- Card: [[platform-federal-compliance-spine]]
- Regulation: `federal-atf-4473.md`
- Card: [[canary-compliance]]
- Card: [[canary-fox]]
- Card: [[canary-blockchain-anchor]]
