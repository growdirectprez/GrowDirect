---
type: runbook
status: active   # draft | active | retired
runbook-id: <slug>
issue-shape: <one-line description of the symptom this fixes>
service: <service-id-or-list>
engines: []  # engine primitives this runbook belongs to
modules: []  # spine letters
owner: <person-or-team>
last-verified: <YYYY-MM-DD>   # last time someone confirmed the steps work
last-compiled: <YYYY-MM-DD>
needs-review: <YYYY-MM-DD + 90 days>
tags: [runbook, devops]
---

# <Runbook title>

One-paragraph statement of the issue this runbook addresses.

## When to use this

Symptoms that mean this runbook applies:

- <symptom 1>
- <symptom 2>

If the symptom is similar but not exact, check related runbooks first: [[]]

## Prerequisites

- Access to <env / dashboard / credential>
- <CLI tool> installed
- Authority level: <on-call / engineer / lead>

## Steps

1. **<First action>** — exact command or click path
   ```
   <command>
   ```
   Expected: <what success looks like>

2. **<Next action>**
   ```
   <command>
   ```

3. **<Verify>**
   ```
   <verification command>
   ```
   Expected: <PASS condition>

## If it doesn't work

- Symptom A → Try [[runbook-x]]
- Symptom B → Escalate to <owner>

## Why this works

Brief architectural note linking to the SDD that explains the underlying behavior.

## Related

- SDDs: [[]]
- Service: [[]]
- Recent incidents using this runbook: (Bases query in the actual file)
