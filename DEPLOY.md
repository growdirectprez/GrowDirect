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

## Hello smoke-test service

`CanaryGo/cmd/hello` is a dependency-free Go binary used to verify the
pipeline. It has no domain logic. Receiving team should delete
`cmd/hello/`, `deploy/Dockerfile.hello`, and the deploy steps in
`cloudbuild.yaml` once real services are deploying.

Endpoints:
- `GET /` → 200 "hello from canary-rapidpos drop zone"
- `GET /health` → 200 "ok"

(Note: `/healthz` is reserved by Cloud Run's Knative activator — use
`/health` for service health probes.)

Live URL (authenticated only):
```
https://hello-7n7bal6q7a-uc.a.run.app
```

---

## Adding a new service

The pattern is the same for any `cmd/<service>`:

1. Write the Go service at `CanaryGo/cmd/<service>/main.go`
2. Create `CanaryGo/deploy/Dockerfile.<service>` (mirror
   `Dockerfile.identity` or `Dockerfile.hello`)
3. Append three steps to `cloudbuild.yaml` (`build-<service>`,
   `push-<service>`, `deploy-<service>`)
4. Append the image to the `images:` section
5. Push to `main` — Cloud Build builds and deploys automatically

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
| Cloud Run service | `hello` (smoke test) |
| Build / deploy SA | `canary-deploy@canary-rapidpos.iam.gserviceaccount.com` (the trigger runs as this SA) |
| Runtime SA (default) | `515966226071-compute@developer.gserviceaccount.com` |
| Enabled APIs | Cloud Run, Cloud SQL Admin, Secret Manager, Artifact Registry, Cloud Build, Pub/Sub |

### Service account roles (`canary-deploy`)

- `roles/cloudbuild.editor` — run builds
- `roles/artifactregistry.writer` — push images
- `roles/run.admin` — deploy Cloud Run services
- `roles/iam.serviceAccountUser` — act-as the runtime SA when deploying
- `roles/logging.logWriter` — write Cloud Build logs to Cloud Logging
- `roles/cloudsql.client` — connect to Cloud SQL (when added)
- `roles/secretmanager.secretAccessor` — read secrets (when added)

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
