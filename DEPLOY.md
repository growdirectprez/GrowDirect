# DEPLOY — drop-zone CI/CD on GCP

This is the dev-environment deployment workflow for the `canary-rapidpos`
GCP project. **It is not a production runbook.** A separate receiving team
takes the source repo + GCP project forward to production with
Terraform-as-code and their own auth, secrets, and runtime topology.

The dispatch driving this setup is **GRO-700 v3**.

---

## Pipeline shape

```
git push origin main
        ↓
Cloud Build trigger (deploy-main, project: canary-rapidpos)
        ↓
Cloud Build executes /cloudbuild.yaml
        ├── docker build -f CanaryGo/deploy/Dockerfile.<service>
        ├── docker push to Artifact Registry
        │   us-central1-docker.pkg.dev/canary-rapidpos/canary-go/<service>:$SHORT_SHA
        └── gcloud run deploy <service> --image=...:$SHORT_SHA --region=us-central1 --no-allow-unauthenticated
        ↓
Cloud Run service updated (latest revision serves 100% of traffic)
```

---

## Onboard via git (collaborator workflow)

```bash
git clone git@github.com:growdirectprez/GrowDirect.git
cd GrowDirect
# read CLAUDE.md for the broader platform context
# read DEPLOY.md (this file) for the deploy workflow
```

To deploy a code change:

```bash
git checkout -b feat/your-change
# edit code
git add -A && git commit -m "your change"
git push origin feat/your-change
# open PR against main; merge to main triggers the deploy
```

Or for direct push (solo dev):

```bash
git push origin main
```

The trigger fires on every push to `main`. Build takes ~2-3 minutes
(build → push → deploy). New revision routes 100% of traffic; previous
revision is preserved (rollback via traffic split, not redeploy).

---

## Smoke-test services

Two services prove the drop-zone pipeline. Receiving team should delete
both once real services are deploying cleanly.

### `cmd/hello` — pipeline shape

Zero-dep Go binary. Proves git → Cloud Build → Artifact Registry →
Cloud Run.

- `GET /` → 200 "hello from canary-rapidpos drop zone"
- `GET /health` → 200 "ok"
- URL: `https://hello-7n7bal6q7a-uc.a.run.app` (auth required)

### `cmd/dbcheck` — Cloud SQL data path

Connects to Cloud SQL Postgres 17 via the unix socket Cloud Run mounts
when `--add-cloudsql-instances` is set. Reads `DATABASE_URL` from
Secret Manager (`db-url`). Runs `CREATE EXTENSION IF NOT EXISTS vector`
on startup to self-bootstrap pgvector.

- `GET /` → 200 "dbcheck — connect ok"
- `GET /health` → 200 with Postgres version + pgvector status
- URL: `https://dbcheck-7n7bal6q7a-uc.a.run.app` (auth required)

Note: `/healthz` is reserved by Cloud Run's Knative activator — use
`/health` for service health probes.

---

## Adding a new service

The pattern is the same for any `cmd/<service>`:

1. Write the Go service at `CanaryGo/cmd/<service>/main.go`
2. Create `CanaryGo/deploy/Dockerfile.<service>` (mirror
   `Dockerfile.hello` for stateless or `Dockerfile.dbcheck` if it
   needs Cloud SQL)
3. Append three steps to `cloudbuild.yaml` (`build-<service>`,
   `push-<service>`, `deploy-<service>`)
4. Append the image to the `images:` section
5. Push to `main` — Cloud Build builds and deploys automatically

If the service needs Cloud SQL, add to the deploy step:
```yaml
- --add-cloudsql-instances=canary-rapidpos:us-central1:canary-rapidpos-db
- --set-secrets=DATABASE_URL=db-url:latest
```

If the service needs a different secret, create it (`gcloud secrets
create ...`) and grant the runtime SA
(`515966226071-compute@developer.gserviceaccount.com`)
`roles/secretmanager.secretAccessor` on it.

---

## Auth model

The drop zone deploys services with `--no-allow-unauthenticated`. The
org-level **Domain Restricted Sharing** policy blocks `allUsers`
bindings, so public access requires either:

- An exception to the org policy (founder + admin)
- A different IAM model the receiving team chooses (Identity Platform,
  custom IAM, etc.)

To call a service from your laptop:

```bash
URL=https://hello-7n7bal6q7a-uc.a.run.app
TOKEN=$(gcloud auth print-identity-token)
curl -H "Authorization: Bearer $TOKEN" $URL/health
```

To grant another developer access:

```bash
gcloud run services add-iam-policy-binding hello \
  --region=us-central1 \
  --project=canary-rapidpos \
  --member="user:OTHER_DEV@growdirect.io" \
  --role="roles/run.invoker"
```

---

## Viewing logs

**Cloud Run service logs:**
```bash
gcloud run services logs read <service> \
  --region=us-central1 \
  --project=canary-rapidpos \
  --limit=50
```

**Cloud Build build logs:**
```bash
# list recent builds
gcloud builds list --project=canary-rapidpos --limit=5

# describe a specific build
gcloud builds describe <BUILD_ID> --project=canary-rapidpos

# read the log (requires gcloud beta component)
gcloud beta builds log <BUILD_ID> --project=canary-rapidpos
```

Or open the build URL in the GCP console:
```
https://console.cloud.google.com/cloud-build/builds?project=canary-rapidpos
```

---

## What's provisioned in the drop zone

| Resource | Identifier |
|---|---|
| GCP organization | `growdirect.io` |
| Project | `canary-rapidpos` (number `515966226071`) |
| Region | `us-central1` |
| Cloud Build trigger | `deploy-main` (1st gen, GitHub: `growdirectprez/GrowDirect`, branch `^main$`, config `/cloudbuild.yaml`) |
| Artifact Registry repo | `us-central1-docker.pkg.dev/canary-rapidpos/canary-go` (Docker format) |
| Cloud Run services | `hello` · `dbcheck` (smoke tests) |
| Cloud SQL instance | `canary-rapidpos-db` (Postgres 17, db-f1-micro, us-central1, ~10GB SSD, ~$8/mo) |
| Cloud SQL connection name | `canary-rapidpos:us-central1:canary-rapidpos-db` |
| Database | `canary_go` (with pgvector extension installed) |
| Secret Manager secrets | `db-url` (Postgres connection string for `postgres` superuser) |
| Build / deploy SA | `canary-deploy@canary-rapidpos.iam.gserviceaccount.com` (the trigger runs as this SA) |
| Runtime SA (default) | `515966226071-compute@developer.gserviceaccount.com` |
| Enabled APIs | Cloud Run, Cloud SQL Admin, Secret Manager, Artifact Registry, Cloud Build, Pub/Sub |

### Service account roles (`canary-deploy`)

- `roles/cloudbuild.editor` — run builds
- `roles/artifactregistry.writer` — push images
- `roles/run.admin` — deploy Cloud Run services
- `roles/iam.serviceAccountUser` — act-as the runtime SA when deploying
- `roles/logging.logWriter` — write Cloud Build logs to Cloud Logging
- `roles/cloudsql.client` — connect to Cloud SQL
- `roles/secretmanager.secretAccessor` — read secrets

### Runtime SA roles (default Compute SA)

- `roles/cloudsql.client` — connect to Cloud SQL from Cloud Run
- `roles/secretmanager.secretAccessor` (on specific secrets) — read
  mounted secrets at runtime

### Org policy quirks the receiving team should know

- `iam.disableServiceAccountKeyCreation` is enforced — no static SA
  keys; use Workload Identity Federation
- Domain Restricted Sharing blocks `allUsers` in IAM bindings — public
  Cloud Run requires either an exception or a non-`allUsers` auth model
- `/healthz` is reserved by the Cloud Run frontend (Knative activator);
  use `/health` for in-app health probes

---

## What's deferred to the receiving team

Per **GRO-700 v3** (out of scope for this drop zone):

- Production project (`-prod`) — receiving team creates clean
- Terraform / infra-as-code for everything described in this file
- Identity Platform / production auth runtime
- Vertex AI integration (Anthropic Claude on Vertex, embedding model)
- Stripe billing / satoshi cost rollup
- First merchant onboarding
- PCI / SOC 2 / GDPR / data residency / cyber liability
- Multi-region deployment, prod org policies, scaled billing alerts
- Cloud Workstations cluster (laptop + gcloud is sufficient for solo
  dev today)
- Cloud SQL HA (this drop zone is zonal; receiving team picks regional /
  HA tier in prod)
- Database migrations framework (dbcheck self-bootstraps pgvector
  inline; receiving team should move to a proper migration tool —
  goose, atlas, sqlc with migration support, etc.)
- VPC peering / private IP for Cloud SQL (drop zone uses the unix
  socket via Cloud Run's `--add-cloudsql-instances`; in prod,
  receiving team likely wants private IP + Cloud SQL Auth Proxy)
