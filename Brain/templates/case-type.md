---
case-type-id: <% tp.file.title.toLowerCase().replace(/\s+/g, '-') %>
name: <% tp.file.title %>
description: ""
class: ""
visibility: ""
trigger: ""
cadence-tier: ""
owners:
  corp-side-role: ""
  store-side-role: ""
sla:
  initial-response: ""
  resolution: ""
  escalation-after: ""
required-fields: []
state-machine:
  states: ["open", "in-progress", "review", "resolved", "escalated", "canceled"]
  transitions: []
routing-rules:
  initial-assignment: ""
  escalation-policy: ""
closure-criteria:
  required-attestations: []
  outcomes: []
anchor-points: []
related-modules: []
sources: []
last-compiled: <% tp.date.now("YYYY-MM-DD") %>
needs-review: false
---

# Case Type: <% tp.file.title %>

> Operational template for instantiating a Hawk case type. Fill every section. Filled instances live at `Brain/templates/case-type/<case-type-id>.md` — flat directory, one file per case type, registered into `app.hawk_case_types` at build/deploy time.

## What this is

<!-- One paragraph: what kind of event or workflow does this case type cover? Match the DSG-style "Definition" field — concise, operational, not marketing. ≤ 60 words. -->

## When it fires

<!-- The trigger condition. If scheduled, the cadence (cite the cadence tier). If event-driven, the event source and rule. If human-initiated, the role and circumstance. If regulatory, the citation. -->

## Who owns it

| Side | Role | Responsibility |
|---|---|---|
| Corp | <role> | <e.g., "investigates and closes," "reviews and approves," "audits annually"> |
| Store | <role> | <e.g., "files initial report," "executes corrective action," "attests completion"> |

## Form fields (required at create time)

| Field | Type | Required | Validation | Notes |
|---|---|---|---|---|
| <name> | <string / enum / date / number / file / freetext> | yes/no | <regex / range / enum values> | <notes> |

## State machine

```
open ─→ in-progress ─→ review ─┬→ resolved
                                ├→ escalated
                                └→ canceled
```

| Transition | Guard | Notes |
|---|---|---|
| open → in-progress | Assignment accepted | |
| in-progress → review | Required fields complete | |
| review → resolved | Approver attests outcome | |
| review → escalated | Approver rejects or SLA breached | |
| any → canceled | Founder / corp-side override | Rare; requires reason |

<!-- Override the default if the case type needs domain-specific states (e.g., LP investigations might add "interview-scheduled," "interview-completed"). -->

## SLA

| Stage | Time | Escalation |
|---|---|---|
| Initial response | <e.g., "1 hour"> | <to whom> |
| Resolution | <e.g., "5 business days"> | <to whom> |

## Closure criteria

| Outcome | Definition | Anchored to Fox? |
|---|---|---|
| <e.g., "Closed Unfounded"> | <definition> | yes/no |
| <e.g., "Resolved with Corrective Action"> | <definition> | yes |
| <e.g., "Escalated to External"> | <definition> | yes |

## Anchor points

<!-- Which state transitions emit a Fox event for the evidence chain. Default minimum: case create + case close. Add others as needed for evidentiary depth. -->

- [x] case create → Fox event
- [x] case close → Fox event + blockchain anchor (Bitcoin L2)
- [ ] state transition: <transition> → Fox event
- [ ] attachment added → Fox event
- [ ] reassignment → Fox event

## Related modules

| Module | Relationship |
|---|---|
| canary-hawk | runs this case type |
| canary-fox | evidence anchor on state transitions |
| canary-<module> | <produces / consumes / triggers> |

## Reports

<!-- Standard reports that include this case type. Default: case-type rollup (count by status), period summary, open-cases list, MTTR by store/region. List any case-type-specific reports. -->

## Sources

<!-- Citation: where this case type is grounded. DSG LPMS prior art (cite the Incident Types row), regulatory mandate, vendor requirement, internal policy doc. -->

## See also

- Card: [[canary-hawk]] — the universal envelope
- Card: [[platform-case-type-registry-pattern]] — the pattern this template instantiates
- Filled instances: `Brain/templates/case-type/`
