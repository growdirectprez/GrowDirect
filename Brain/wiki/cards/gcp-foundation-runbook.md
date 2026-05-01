---
card-type: runbook
card-id: runbook-gcp-foundation
card-version: 1
domain: platform
layer: cross-cutting
status: approved
agent: ALX
tags: [gcp, cloud-run, cloud-sql, iam, service-accounts, canary-go]
last-compiled: 2026-05-01
needs-review: false
---

## What this is

Operational record of GCP organization and project foundation provisioned 2026-05-01. Covers org creation, project setup, billing, API enablement, and IAM service account baseline.

## Configuration state (provisioned 2026-05-01)

**Organization:** `growdirect.io` — linked to Google Workspace account `gclyle@growdirect.io`  
**Project name:** `Canary-RapidPOS`  
**Project ID:** `canary-rapidpos`  
**Billing:** Linked (confirmed 2026-05-01)  

## Enabled APIs

| API | Service Name | Purpose |
|-----|-------------|---------|
| Cloud Run | `run.googleapis.com` | Serverless container deployment |
| Cloud SQL Admin | `sqladmin.googleapis.com` | Managed PostgreSQL 17 |
| Secret Manager | `secretmanager.googleapis.com` | Runtime secrets |
| Artifact Registry | `artifactregistry.googleapis.com` | Container image storage |
| Cloud Build | `cloudbuild.googleapis.com` | CI/CD pipeline |
| Pub/Sub | `pubsub.googleapis.com` | Event streaming |

## IAM service accounts

| Account | Email | Roles | Key |
|---------|-------|-------|-----|
| `canary-deploy` | `canary-deploy@canary-rapidpos.iam.gserviceaccount.com` | Cloud Run Admin, Cloud SQL Client, Secret Manager Secret Accessor, Artifact Registry Writer, Cloud Build Editor | None — org policy `iam.disableServiceAccountKeyCreation` enforced (Secure by Default) |

## Auth model

**Local dev (mini, GRO-700):** `gcloud auth application-default login` with `gclyle@growdirect.io`. No key file.  
**CI/CD (Cloud Build):** Service account impersonation within GCP — no key required.  
**Workload Identity Federation:** Target auth pattern for any external workload needing GCP access.

JSON key creation is blocked at the org level (`iam.disableServiceAccountKeyCreation`). This is intentional and correct — do not disable the policy.

## Next steps

| Dispatch | Description | Status |
|----------|-------------|--------|
| GRO-700 | Wipe and rebuild mini as GCP-native dev workstation | Backlog (Urgent) |
| GRO-663 | Epic: GCP Deployment (M6 Hardening) | Backlog |

### GRO-700 setup sequence (mini)
1. Wipe mini, clean macOS install
2. Install gcloud SDK
3. `gcloud auth login` → `gclyle@growdirect.io`
4. `gcloud auth application-default login`
5. `gcloud config set project canary-rapidpos`
6. Install Docker, configure to push to Artifact Registry (`us-central1-docker.pkg.dev`)
7. Clone `growdirect-llc/GrowDirect`, start shared infra stack

## System projects (do not touch)

GCP auto-created these during org setup — leave them alone:
- `Hybrid Connectivity Project` (`cs-hc-0d8acea2c2a6421ab951cd5d`)
- `Hybrid Connectivity Project` (`cs-hc-bcbf1a9b87324c4bac124083`)
- `Cloud Setup Host Project` (`cs-host-69f6bd0e52504f6e8b4a25`)

## Related

- GRO-718 — domain transfer to Cloudflare
- GRO-719 — Google Workspace provisioning
- `Brain/wiki/cards/workspace-admin-runbook.md` — Workspace config state
- GRO-700 — mini rebuild (next dispatch)
- GRO-663 — Epic GCP Deployment
