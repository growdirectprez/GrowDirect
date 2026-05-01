---
type: incident
status: active   # active | resolved | postmortem-pending
incident-id: <YYYY-MM-DD-HHMM-shortname>
severity: <P0|P1|P2|P3>
opened-at: <YYYY-MM-DD HH:MM TZ>
resolved-at: <YYYY-MM-DD HH:MM TZ if resolved>
service: <service-id>
environment: <env-id>
customer: <customer-id if customer-impacting, else null>
engines: []  # affected engine primitives
modules: []  # affected spine letters
root-cause: <one-line categorical>
runbook: <runbook-slug if one applied>
linear-issue: <GRO-XXX>
related-deployments: []
related-incidents: []   # for repeat-pattern detection
last-compiled: <YYYY-MM-DD>
tags: [incident, devops]
---

# <Incident shortname>

One-paragraph summary: what broke, who was affected, when, current state.

## Timeline

| Time | Event |
|---|---|
| <HH:MM> | First signal — <how detected> |
| <HH:MM> | Triage owner assigned |
| <HH:MM> | Root cause identified |
| <HH:MM> | Mitigation applied |
| <HH:MM> | Resolved / monitoring |

## Root cause

What actually caused this. Categorical (config drift, regression, capacity, dependency, etc.) plus the specific instance.

## Customer impact

If customer-facing — which customers, what symptom, how long.

## Resolution

What was changed to resolve. Link to the deploy or PR.

## Follow-ups

- [ ] Postmortem authored
- [ ] Runbook updated / created
- [ ] Detection improved (alert added / threshold tuned)
- [ ] Test added that would have caught this

## Related

- Service: [[]]
- Runbook: [[]]
- SDDs: [[]]
- Prior incidents (same shape): [[]]
