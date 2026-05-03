---
case-type-id: lp-firearms-straw-purchase
name: LP Firearms — Straw Purchase
description: Critical Smart Alert when a person attempts to purchase a firearm for someone who is unable to purchase it themselves; case opens for investigation and (if confirmed) ATF notification per 18 U.S.C. § 922(a)(6) and 27 CFR 478.124.
class: LP
visibility: LP
trigger: real-time-event
cadence-tier: stream
owners:
  corp-side-role: SSC LP Investigator + General Counsel (if confirmed)
  store-side-role: Store Manager + FFL Compliance Officer
sla:
  initial-response: 1h
  resolution: 14d
  escalation-after: 21d
required-fields:
  - name: store-id
    type: string
    required: true
  - name: incident-datetime
    type: datetime
    required: true
  - name: subject-identification
    type: object
    required: true
    notes: Name, ID details for the apparent purchaser
  - name: accomplice-identification
    type: object
    required: false
    notes: Name, ID details for the suspected actual recipient (if known)
  - name: firearm-attempted
    type: object
    required: true
    notes: Manufacturer, model, serial (if assigned), type, caliber
  - name: transaction-outcome
    type: enum
    enum: [refused-by-store, sale-completed-then-flagged, customer-departed, atf-intervention]
    required: true
  - name: straw-indicators-observed
    type: array
    required: true
    notes: e.g., third-party-paying, accomplice-direction, accomplice-pointing-out-firearm, unusual-knowledge-gap, prior-pattern
  - name: video-evidence-attached
    type: boolean
    required: false
  - name: form-4473-completed
    type: boolean
    required: false
  - name: nics-result
    type: enum
    enum: [proceed, delay, denied, not-run, n-a]
    required: false
state-machine:
  states: [open, investigating, evidence-review, confirmed-straw, unfounded, reported-to-atf, canceled]
  transitions:
    - from: open
      to: investigating
      guard: assigned-to-investigator + counsel-notified-if-sale-completed
    - from: investigating
      to: evidence-review
      guard: investigation-complete + counsel-review-complete
    - from: evidence-review
      to: confirmed-straw
      guard: investigator-attests-confirmed + counsel-attests-supportable
    - from: evidence-review
      to: unfounded
      guard: investigator-attests-not-confirmed
    - from: confirmed-straw
      to: reported-to-atf
      guard: atf-notification-submitted
routing-rules:
  initial-assignment: SSC LP Investigator on rotation; FFL Compliance Officer immediately notified; if sale completed → General Counsel notified within 1h
  escalation-policy: At 21d unresolved → SSC LP Director + General Counsel; on confirmed-straw → mandatory ATF notification within 14 days
closure-criteria:
  required-attestations:
    - investigator-attests-finding
    - if-confirmed-straw: counsel-attests-supportable AND atf-notification-submitted
    - if-unfounded: investigator-attests-no-finding + store-manager-acknowledges
  outcomes:
    - reported-to-atf (and ATF case ID recorded)
    - unfounded
anchor-points:
  - case-create
  - state-transition-investigating
  - state-transition-evidence-review
  - state-transition-confirmed-straw
  - state-transition-reported-to-atf
  - case-close-unfounded
  - atf-notification-event
related-modules:
  - canary-hawk
  - canary-fox
  - canary-blockchain-anchor
  - canary-compliance
  - canary-customer
  - canary-employee
sources:
  - Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md (DSG row 19; Class=Critical Smart Alert; Type="Straw Purchase")
  - 18 U.S.C. § 922(a)(6) — false statements in firearm transactions
  - 27 CFR 478.124 — Form 4473 questions on actual transferee
  - Brain/templates/regulation-spec/federal-atf-4473.md
last-compiled: 2026-05-02
needs-review: false
---

# Case Type: LP Firearms — Straw Purchase

## What this is

A potential straw purchase — a person attempting to purchase a firearm on behalf of someone who is prohibited from purchasing or wishes to evade the background-check process. Direct adoption of DSG LPMS row 19: *"SMART ALERT: Any purchase wherein a person attempts or purchases a firearm for someone who is unable to purchase the firearm themselves."* Federal violation under 18 U.S.C. § 922(a)(6) (false statement on Form 4473 about being the actual transferee) and 27 CFR 478.124. Case opens at Critical Smart Alert tier and routes to FFL Compliance Officer + General Counsel immediately if a sale was completed.

## When it fires

Stream-tier real-time event. Fires when:

- Cashier identifies straw indicators during transaction (most common: third-party paying, accomplice direction, unusual customer knowledge gap)
- LP analyst identifies straw pattern in post-transaction review (video, transaction record analysis)
- ATF trace request links a recovered firearm to a transaction with straw indicators
- Customer complaint or staff tip post-transaction

## Who owns it

| Side | Role | Responsibility |
|---|---|---|
| Corp | SSC LP Investigator | Drives investigation, evidence review, ATF coordination |
| Corp | General Counsel | Reviews evidence; attests supportability before ATF notification |
| Store | Store Manager + FFL Compliance Officer | Provides operational context; preserves video; coordinates with corp |

## Form fields (required at create time)

| Field | Type | Required | Notes |
|---|---|---|---|
| store-id | string | yes | Auto-populated |
| incident-datetime | datetime | yes | Original transaction or attempt time |
| subject-identification | object | yes | The apparent purchaser (name, DOB, ID type/#) |
| accomplice-identification | object | no | The suspected actual recipient (if identifiable) |
| firearm-attempted | object | yes | Manufacturer, model, type, caliber, serial (if assigned) |
| transaction-outcome | enum | yes | refused-by-store / sale-completed-then-flagged / customer-departed / atf-intervention |
| straw-indicators-observed | array | yes | List of specific behaviors observed |
| video-evidence-attached | boolean | no | LPTV preservation flag |
| form-4473-completed | boolean | no | If sale was begun |
| nics-result | enum | no | proceed / delay / denied / not-run |

## State machine

```
open ─→ investigating ─→ evidence-review ─┬→ confirmed-straw ─→ reported-to-atf
                  │                       ├→ unfounded
                  └─────────────────────→ canceled (rare; reason required)
```

| Transition | Guard | Anchored to Fox + Bitcoin? |
|---|---|---|
| open → investigating | Assigned to investigator + counsel notified if sale completed | yes |
| investigating → evidence-review | Investigation + counsel review complete | yes |
| evidence-review → confirmed-straw | Investigator + counsel both attest supportable | yes (+ blockchain anchor) |
| evidence-review → unfounded | Investigator attests no actionable finding | yes (+ blockchain anchor) |
| confirmed-straw → reported-to-atf | ATF notification submitted; ATF case ID received | yes (+ blockchain anchor) |

## SLA

| Stage | Time | Escalation |
|---|---|---|
| Initial response | 1h | Auto-page on-call investigator if not picked up; counsel paged if sale completed |
| Resolution | 14 business days | SSC LP Director notification at 14d |
| ATF notification | 14d after confirmed-straw (mandatory) | General Counsel ensures compliance |
| Hard escalation | 21 business days unresolved | SSC LP Director + General Counsel |

## Closure criteria

| Outcome | Definition | Anchored? |
|---|---|---|
| reported-to-atf | Confirmed straw + ATF notified + ATF case ID recorded + counsel attests filing complete | yes (Fox + Bitcoin L2) |
| unfounded | Investigation completed; no actionable straw indicators substantiated | yes |
| canceled | Rare administrative cancellation (e.g., duplicate case); reason required | no |

## Anchor points

- [x] case create → Fox event (subject ID, indicators, firearm, store)
- [x] state transition: open → investigating → Fox event
- [x] state transition: investigating → evidence-review → Fox event
- [x] state transition: evidence-review → confirmed-straw → Fox event + Bitcoin L2 anchor
- [x] state transition: confirmed-straw → reported-to-atf → Fox event + Bitcoin L2 anchor + ATF notification recorded
- [x] attachment added (video, photo, ID copy) → Fox event

## Related modules

| Module | Relationship |
|---|---|
| canary-hawk | runs this case type |
| canary-fox | evidence anchor on every transition |
| canary-compliance | federal-atf-4473 regulation entry; ATF notification submission |
| canary-customer | identity records for subject + accomplice |
| canary-employee | investigator + counsel + FFL compliance officer identity / SLA |
| canary-blockchain-anchor | Bitcoin L2 anchor for close events (audit-grade evidence for ATF) |

## Reports

- Active Straw Purchase Investigations (real-time)
- Confirmed Straw Outcomes by Region (quarterly trend)
- ATF Notification Compliance (mandatory 14-day window adherence)
- Yearly Case Extract — confirmed-straw subset for ATF filings + audit-ready

## Sources

- DSG LPMS `Incident Types.xlsx` row 19: Class=Critical Smart Alert, Type="Straw Purchase," Definition: *"SMART ALERT: Any purchase wherein a person attempts or purchases a firearm for someone who is unable to purchase the firearm themselves."* (`Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md`)
- 18 U.S.C. § 922(a)(6) — false statement in firearm transaction
- 27 CFR 478.124 — Form 4473 actual-transferee question
- `Brain/templates/regulation-spec/federal-atf-4473.md`
- DSG `Actions.xlsx` — closure outcomes (Reported to ATF)

## See also

- Card: [[canary-hawk]]
- Card: [[platform-case-type-registry-pattern]]
- Card: [[platform-federal-compliance-spine]]
- Regulation: `federal-atf-4473.md`
- Case type: `lp-firearms-missing-4473.md` (related; sometimes co-occurs)
- Card: [[canary-compliance]]
- Card: [[canary-fox]]
