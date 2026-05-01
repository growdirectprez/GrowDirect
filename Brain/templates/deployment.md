---
type: deployment
status: active   # active | rolled-back | superseded
deployment-id: <YYYY-MM-DD-HHMM-service-env>
service: <service-id>
environment: <env-id>
version: <semver-or-sha>
released-at: <YYYY-MM-DD HH:MM TZ>
released-by: <person-or-agent>
linear-issue: <GRO-XXX>
build-run: <CI run URL>
rollback-of: <prior-deployment-id-if-this-is-a-rollback>
last-compiled: <YYYY-MM-DD>
tags: [deployment, devops]
---

# <Service> → <Env> @ <version>

One-line release summary.

## What changed

Concise list of changes. Link to the Linear issue and PR.

- [[]]
- [[]]

## Verification

- [ ] Smoke test passed
- [ ] Health check returning 200
- [ ] No regressions in <metric>

## Rollback plan

How to roll back if needed.

## Related

- Service: [[]]
- Environment: [[]]
- Linear issue: [external link]
- Build run: [external link]
