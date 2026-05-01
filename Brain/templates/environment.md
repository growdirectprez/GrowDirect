---
type: environment
status: active
env-id: <slug>
kind: <dev|staging|prod|tenant>
host: <laptop|mini|gcp-region|customer-site>
services: []  # list of service-ids running here
tenants: []   # list of tenant-ids if multi-tenant
public-domains: []
last-deployed: <YYYY-MM-DD>
last-compiled: <YYYY-MM-DD>
needs-review: <YYYY-MM-DD + 60 days>
tags: [environment, devops]
---

# <Environment Name>

What this environment is, who uses it, what runs here.

## Topology

| Service | Version | Status |
|---|---|---|
| <service-id> | <semver> | running / stopped / degraded |

## Access

- Console: <url>
- SSH / kubectl: <how>
- Secrets: <where>

## Recent deployments

(Bases query in the actual file, populated automatically; placeholder text in the template.)

## Related

- Services: [[]]
- Tenants: [[]]
- Runbooks: [[]]
