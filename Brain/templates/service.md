---
type: service
status: active
service-id: <slug>
owner: <person-or-team>
engines: []  # which engine primitives this service belongs to
modules: []  # spine module letters (Q, T, F, etc.) if applicable
repo: <github-org/repo>
runtime: <python|go|node|...>
deploy-target: <gcp|aws|on-prem>
public-domain: <optional — e.g. ncr.growdirect.io>
last-deployed: <YYYY-MM-DD>
last-compiled: <YYYY-MM-DD>
needs-review: <YYYY-MM-DD + 60 days>
tags: [service, devops]
---

# <Service Name>

One-paragraph governing thesis: what this service is, what it does, why it exists.

## What it owns

- Capability 1
- Capability 2

## Dependencies

| Dependency | Address | Required |
|---|---|---|
| <e.g. growdirect_postgres> | <host:port> | Yes |

## Deployment

- Environments: <dev | staging | prod | per-tenant>
- Build: <CI workflow ref>
- Deploy: <runbook link>
- Rollback: <runbook link>

## Health

- Heartbeat / health check: <endpoint>
- Metrics: <dashboard link>
- Alerts: <alert config>

## Related

- SDDs: [[link to canonical SDD]]
- Runbooks: [[link to relevant runbooks]]
- Engineers: [[link to owners]]
