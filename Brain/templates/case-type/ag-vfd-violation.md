---
case-type-id: ag-vfd-violation
name: AG — VFD Violation (Veterinary Feed Directive)
description: Compliance case opens when a VFD-class medicated feed is sold without a valid Veterinary Feed Directive on file, or when a recordkeeping gap is discovered for a previously distributed VFD feed under 21 CFR 558.
class: Compliance
visibility: All
trigger: real-time-event
cadence-tier: stream
owners:
  corp-side-role: SSC Compliance Officer + Feed-Vertical Lead
  store-side-role: Store Manager + Feed Department Lead
sla:
  initial-response: 4h
  resolution: 14d
  escalation-after: 21d
required-fields:
  - name: store-id
    type: string
    required: true
  - name: incident-datetime
    type: datetime
    required: true
  - name: feed-product-sku
    type: string
    required: true
  - name: feed-product-name
    type: string
    required: true
  - name: vfd-class-antimicrobial
    type: string
    required: true
  - name: customer-of-record
    type: string
    required: false
    notes: Livestock owner; populated by canary-customer
  - name: violation-type
    type: enum
    enum: [no-vfd-on-file, vfd-expired, vfd-product-mismatch, vfd-recordkeeping-gap, vfd-acknowledgment-letter-missing]
    required: true
  - name: discovery-context
    type: enum
    enum: [register-block, post-sale-cycle-review, fda-inspection, state-feed-control-inspection, internal-audit, customer-complaint]
    required: true
  - name: quantity-distributed
    type: number
    required: false
state-machine:
  states: [open, investigating, evidence-review, resolved-vfd-recovered, resolved-with-corrective-action, escalated-to-fda, canceled]
  transitions:
    - from: open
      to: investigating
      guard: assigned-to-compliance-officer
    - from: investigating
      to: evidence-review
      guard: investigation-complete
    - from: evidence-review
      to: resolved-vfd-recovered
      guard: vfd-located-and-validated
    - from: evidence-review
      to: resolved-with-corrective-action
      guard: corrective-action-documented (training, process change, recordkeeping fix)
    - from: investigating
      to: escalated-to-fda
      guard: severity-warrants-fda-notification
routing-rules:
  initial-assignment: SSC Compliance Officer; Feed-Vertical Lead notified
  escalation-policy: At 21d unresolved → SSC Compliance Director; on `vfd-acknowledgment-letter-missing` → mandatory FDA pre-distribution disclosure
closure-criteria:
  required-attestations:
    - compliance-officer-attests-resolution
    - store-manager-acknowledges-corrective-action
    - if-recordkeeping-gap: 2-year retention validated for all distributions in the gap window
  outcomes:
    - resolved-vfd-recovered
    - resolved-with-corrective-action
    - escalated-to-fda (and FDA case ID recorded)
anchor-points:
  - case-create
  - state-transition-investigating
  - state-transition-evidence-review
  - case-close-resolved-*
  - state-transition-escalated-to-fda
  - fda-notification-event
related-modules:
  - canary-hawk
  - canary-fox
  - canary-blockchain-anchor
  - canary-compliance
  - canary-item
  - canary-customer
  - canary-employee
sources:
  - Brain/templates/regulation-spec/federal-fda-vfd.md (the regulation this enforces)
  - 21 CFR 558 (federal regulatory text)
  - FDA Guidance for Industry #213
  - RapidPOS feed-tack-pet-pos page — state/federal feed-product compliance reference
last-compiled: 2026-05-02
needs-review: false
---

# Case Type: AG — VFD Violation (Veterinary Feed Directive)

## What this is

A Veterinary Feed Directive (VFD) compliance event — most commonly, a VFD-class medicated feed product was distributed without a valid VFD on file, or a recordkeeping gap was discovered for a previously distributed VFD feed. Federal violation under 21 CFR 558. Adapted from the DSG case-management pattern; new case type for the AG vertical (feed & tack, pet, garden-nursery selling livestock feed). Connects to the Murdoch's-class proof case (gun + feed + AG combined retailer) where firearms compliance and feed compliance both have to operate cleanly.

## When it fires

Stream-tier real-time event. Fires when:

- Register attempts a sale of a VFD-class feed item and no valid VFD is on file (most common)
- Post-sale cycle review identifies a distribution where VFD records cannot be validated
- FDA inspection identifies a missing or invalid VFD
- State feed control inspection identifies a gap (joint federal/state enforcement)
- Internal audit cycle review identifies a recordkeeping gap
- Customer complaint or veterinarian inquiry surfaces a documentation gap

## Who owns it

| Side | Role | Responsibility |
|---|---|---|
| Corp | SSC Compliance Officer | Drives investigation, attests resolution |
| Corp | Feed-Vertical Lead | Provides domain expertise; informs corrective action |
| Store | Store Manager + Feed Department Lead | Provides operational context; preserves records; executes corrective action |

## Form fields (required at create time)

| Field | Type | Required | Notes |
|---|---|---|---|
| store-id | string | yes | Auto-populated |
| incident-datetime | datetime | yes | Sale or discovery time |
| feed-product-sku | string | yes | The VFD-class feed item |
| feed-product-name | string | yes | Manufacturer + product label |
| vfd-class-antimicrobial | string | yes | Active ingredient of concern |
| customer-of-record | string | no | Livestock owner (if known) |
| violation-type | enum | yes | no-vfd-on-file / vfd-expired / vfd-product-mismatch / vfd-recordkeeping-gap / vfd-acknowledgment-letter-missing |
| discovery-context | enum | yes | register-block / post-sale-cycle-review / fda-inspection / state-feed-control-inspection / internal-audit / customer-complaint |
| quantity-distributed | number | no | Pounds / units distributed without compliance |

## State machine

```
open ─→ investigating ─→ evidence-review ─┬→ resolved-vfd-recovered
                  │                       ├→ resolved-with-corrective-action
                  └─────────────────────→ escalated-to-fda
                                          └→ canceled (rare; reason required)
```

| Transition | Guard | Anchored to Fox + Bitcoin? |
|---|---|---|
| open → investigating | Compliance officer assigned + feed-vertical lead notified | yes |
| investigating → evidence-review | Investigation + counsel review (if escalation likely) complete | yes |
| evidence-review → resolved-vfd-recovered | VFD located, validated, recordkeeping reconciled | yes (+ blockchain anchor) |
| evidence-review → resolved-with-corrective-action | Corrective action documented; training delivered; process changed | yes (+ blockchain anchor) |
| investigating → escalated-to-fda | Severity warrants federal notification (e.g., systematic gap) | yes (+ blockchain anchor) |

## SLA

| Stage | Time | Escalation |
|---|---|---|
| Initial response | 4h | Auto-reassign at 4h to next compliance officer on rotation |
| Resolution | 14 business days | SSC Compliance Director notification at 14d |
| Hard escalation | 21 business days unresolved | SSC Compliance Director + General Counsel + Feed-Vertical Lead |

## Closure criteria

| Outcome | Definition | Anchored? |
|---|---|---|
| resolved-vfd-recovered | VFD located + field-validated + 2-year retention reconciled | yes (Fox + Bitcoin L2) |
| resolved-with-corrective-action | Corrective action (training, process change, recordkeeping fix) documented; future violations prevented | yes |
| escalated-to-fda | FDA notified + FDA case ID recorded + corrective action plan submitted | yes |

## Anchor points

- [x] case create → Fox event (feed SKU, store, violation type, discovery context)
- [x] state transition: open → investigating → Fox event
- [x] state transition: investigating → evidence-review → Fox event
- [x] state transition: evidence-review → resolved-* → Fox event + Bitcoin L2 anchor
- [x] state transition: investigating → escalated-to-fda → Fox event + FDA notification recorded
- [x] attachment added (VFD scan, photo, recordkeeping document) → Fox event

## Related modules

| Module | Relationship |
|---|---|
| canary-hawk | runs this case type |
| canary-fox | evidence anchor on every transition |
| canary-compliance | hosts the federal-fda-vfd regulation entry; provides operator prompt |
| canary-item | feed SKU and VFD-class flagging |
| canary-customer | livestock owner identity |
| canary-employee | compliance officer + feed lead identity / SLA enforcement |
| canary-blockchain-anchor | Bitcoin L2 anchor for close events (audit-grade evidence) |

## Reports

- Active VFD Compliance Cases (real-time)
- VFD Violation Resolution MTTR by store + feed-product (operational health metric)
- Annual VFD Compliance Rollup (FDA inspection-ready extract)
- Yearly Case Extract — escalated-to-FDA subset for federal filings + audit-ready

## Sources

- `Brain/templates/regulation-spec/federal-fda-vfd.md` — the regulation this enforces
- 21 CFR 558 (regulatory text)
- FDA Guidance for Industry #213
- RapidPOS feed-tack-pet-pos page — vertical compliance reference
- DSG LPMS pattern: case-type registry approach (this case type extends DSG's pattern to AG vertical, which DSG didn't cover but the architecture supports natively)

## See also

- Card: [[canary-hawk]]
- Card: [[platform-case-type-registry-pattern]]
- Card: [[platform-federal-compliance-spine]]
- Regulation: `federal-fda-vfd.md`
- Card: [[canary-compliance]]
- Card: [[canary-fox]]
- Card: [[canary-blockchain-anchor]]
