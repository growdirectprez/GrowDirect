---
title: GCP Deployment — Canary Protocol API Gateway
sdd-id: canary-go-gcp-deployment-gateway
version: 1
status: draft
domain: canary
layer: infra
last-compiled: 2026-05-02
needs-review: 2026-05-16
linear: GRO-756
parent-dispatch: GRO-739
patent: Application 63/991,596
---

# GCP Deployment — Canary Protocol API Gateway

## Governing thesis

The Canary Protocol API Gateway (Node 2 of Patent Application 63/991,596) deploys to GCP as a Cloud Run service fronted by a global HTTPS Load Balancer at `api.canary.growdirect.io`, backed by Cloud SQL Postgres 17 + Memorystore Redis, with HMAC source secrets in Secret Manager. The deployment substrate is composed entirely of GCP managed services per the platform stack-commitment posture — no hand-rolled infrastructure outside the patent-protected core IP. Target monthly run rate at MVP traffic is **under $100/mo**; the deployment is the operating embodiment of the patent's Node 2 architecture.

## Scope

| In scope | Out of scope |
|---|---|
| Gateway service deployment (Cloud Run) | Sub 1 / Sub 2 / Sub 3 worker deployments (separate dispatches; same substrate) |
| Cloud SQL Postgres 17 + pgvector | Bitcoin signet anchoring (GRO-750) |
| Memorystore Redis (Valkey-compatible) | LNURL-auth (GRO-753) |
| Cloud Load Balancer + Cloud Armor + managed cert + custom domain | L402 verify (GRO-752) |
| Secret Manager + IAM bindings | Multi-region failover (Phase 2) |
| Cloud Build CI/CD trigger | Production-grade CDN tuning (Phase 2) |
| Cloud Logging + Cloud Monitoring (uptime, p99 latency, 5xx, SQL CPU/conn) | OrdinalsBot integration (Phase 1.E) |
| First smoke-test from outside the laptop | Tokenomics layer (Phase 2) |

## Architecture

```
Internet
  │
  ▼  TCP/443
┌─────────────────────────────────────────────────────────────┐
│ Global HTTPS LB (canary-gateway-https-fr)                   │
│   • Static anycast IP (canary-gateway-ip)                   │
│   • Google-managed cert (canary-gateway-cert)               │
│   • Cloud Armor policy (canary-gateway-armor)               │
│       — XSS / SQLi pre-configured rules                     │
│       — Rate limit: 600 req/min per source IP, 5min ban     │
│   • HTTP→HTTPS redirect via canary-gateway-http-redirect    │
└─────────────────────────────────────────────────────────────┘
  │
  ▼  serverless NEG
┌─────────────────────────────────────────────────────────────┐
│ Cloud Run service: canary-gateway-staging                   │
│   • Image: us-central1-docker.pkg.dev/canary-rapidpos/      │
│            canary-go/gateway:$SHORT_SHA                     │
│   • Runtime SA: canary-gateway-rt@canary-rapidpos.iam.gserv │
│   • min=1, max=10, concurrency=80, cpu=1, memory=512Mi      │
│   • timeout=30s, port=8080                                  │
│   • --no-allow-unauthenticated (LB-gated entry only)        │
│   • Egress: VPC connector canary-vpc-conn (private-only)    │
└─────────────────────────────────────────────────────────────┘
  │            │                   │
  │ Cloud SQL  │ VPC connector     │ Secret Manager API
  │ Auth Proxy │                   │
  ▼            ▼                   ▼
┌──────────┐ ┌──────────────┐ ┌─────────────────────────────┐
│ Cloud SQL│ │ Memorystore  │ │ Secret Manager              │
│ Postgres │ │ Redis 7.x    │ │ • canary-gateway-database-* │
│ 17       │ │ (Valkey-     │ │ • canary-gateway-valkey-*   │
│ canary-  │ │  compatible) │ │ • canary-gateway-internal-* │
│ pg       │ │ canary-redis │ │ • canary-gateway-session-*  │
│ db-g1-   │ │ BASIC 1 GB   │ │ • canary-source-*           │
│ small    │ │ private-svc  │ │   (per-merchant HMAC keys,  │
│ private  │ │ access only  │ │    seeded by GRO-687 work)  │
│ IP only  │ │              │ │                             │
└──────────┘ └──────────────┘ └─────────────────────────────┘
  │
  └── Cloud Audit Logs ──► Cloud Logging ──► (optional) BigQuery export
```

## GCP services and managed-vs-built decisions

Per `platform-stack-commitment` (memory `project_gcp_commitment_locked`): buy managed services for everything outside core IP. The gateway IS core IP (HMAC verify + payload hash + queue publish — patent-protected) and lives in code; everything around it is bought.

| Concern | GCP service | Why this | Phase 2+ alternative |
|---|---|---|---|
| Compute | Cloud Run | Pay-per-request, auto-scale, zero ops, native containerized Go workload | GKE Autopilot if state requirements outgrow stateless |
| RDBMS | Cloud SQL Postgres 17 | pgvector + pg_trgm + standard `migrate` tool compatibility, point-in-time recovery, managed backups | AlloyDB at >5K tenants |
| Streams / cache | Memorystore Redis 7.x | Valkey-compatible (XADD/XREAD identical); private-IP-only; BASIC tier covers MVP | Memorystore for Redis Cluster at >1 GB working set |
| Edge / WAF | Cloud Load Balancer + Cloud Armor | Anycast IP, managed cert, OWASP CRS pre-configured, native Cloud Run NEG integration | Cloud CDN if static asset traffic warrants |
| Secrets | Secret Manager | Native IAM, automatic Cloud Audit Logs, versioning, KMS-backed | None — this is the right primitive |
| Container registry | Artifact Registry | Same project, same IAM, regional | None |
| CI/CD | Cloud Build | Same project, native Cloud Run deploy, builds-as-code | GitHub Actions if open-source workflow is needed |
| Observability | Cloud Logging + Cloud Monitoring + Cloud Trace | Native zap → structured logs, free tier covers MVP, integrated alerting | Datadog at >$1K/mo log volume |
| DNS | Cloudflare (incumbent) | Already managing growdirect.io | Cloud DNS if Cloudflare relationship changes |

**Cloud Run vs GKE.** Cloud Run for the gateway. The gateway is a stateless HTTP service with sub-5ms p99 latency targets — exactly Cloud Run's sweet spot. GKE adds operational surface (node pools, cluster upgrades, network policies) for no benefit at MVP scale. Re-evaluate at >100 RPS sustained or when stateful workloads enter the picture.

**Cloud SQL vs AlloyDB.** Cloud SQL Postgres 17 for MVP. AlloyDB has a columnar engine and better horizontal scaling but costs ~3× and adds compatibility surprises (some pg extensions differ). Cloud SQL covers up to ~5K tenants comfortably on a single regional instance; the migration target is documented but not Phase 1.

**Memorystore vs self-hosted Redis on GCE.** Memorystore. The tier matrix:
- BASIC 1 GB: ~$30/mo, no replica, fine for MVP staging (Streams events are durable in Postgres via Sub 1, so cache loss is recoverable)
- STANDARD 1 GB: ~$75/mo, HA replica, Phase 2 staging
- BASIC bottlenecks at ~10K ops/s — acceptable for Phase 1 traffic

**Secret Manager vs Vault.** Secret Manager. Vault would require a cluster, an HA story, and disaster recovery. Secret Manager is one IAM grant + an SDK call. Per `feedback_no_hand_rolling_outside_core_ip`.

## IAM model

Two service accounts. Build separate from runtime — least privilege, no shared keys.

| SA | Purpose | Roles | Created by |
|---|---|---|---|
| `canary-deploy@canary-rapidpos.iam.gserviceaccount.com` | Cloud Build identity | `roles/run.admin`, `roles/cloudsql.client`, `roles/secretmanager.secretAccessor`, `roles/artifactregistry.writer`, `roles/cloudbuild.editor`, `roles/iam.serviceAccountUser` (to act-as runtime SA) | GCP foundation runbook (existing — `Brain/wiki/cards/gcp-foundation-runbook.md`) |
| `canary-gateway-rt@canary-rapidpos.iam.gserviceaccount.com` | Gateway runtime identity | `roles/cloudsql.client`, `roles/secretmanager.secretAccessor` (scoped to `canary-source-*` and `canary-gateway-*`), `roles/logging.logWriter`, `roles/monitoring.metricWriter`, `roles/cloudtrace.agent`, `roles/redis.editor` | `step_sa` in `deploy/scripts/deploy-gateway.sh` |

**Key creation is blocked at the org level** (`iam.disableServiceAccountKeyCreation` per `gcp-foundation-runbook.md`). All auth flows use Workload Identity / impersonation. No JSON key files anywhere.

**Secret access scoping.** The `secretmanager.secretAccessor` role on the runtime SA is project-wide today. Hardening (Phase 2): switch to condition-scoped binding limited to `canary-source-*` and `canary-gateway-*` resource patterns — see `docs/sdds/canary-go/secrets-manager-integration.md` (GRO-687) for the exact `gcloud projects add-iam-policy-binding ... --condition=...` command.

## Networking

| Layer | Decision |
|---|---|
| Cloud Run egress | `--vpc-egress=private-ranges-only` via `canary-vpc-conn` connector (e2-micro, range `10.8.0.0/28`, min 2 max 3 instances) |
| Cloud SQL access | Private IP only (`--no-assign-ip`), via Cloud SQL Auth Proxy sidecar (Cloud Run `--add-cloudsql-instances`) |
| Memorystore access | Private Service Access on the same VPC, reached via the connector |
| Public ingress | Only via the Cloud LB — `--no-allow-unauthenticated` on the Cloud Run service blocks the `*.run.app` URL; LB authenticates as Google's managed identity via `roles/run.invoker` granted to `allUsers` (LB-pass-through pattern) |
| LB → Cloud Run | Serverless NEG (`canary-gateway-neg`) with backend service (`canary-gateway-backend`) |
| WAF | Cloud Armor policy `canary-gateway-armor` — pre-configured XSS-v33 and SQLi-v33 rules + IP rate-limit (600 req/min, 5min ban) |

**Why the connector when Cloud SQL has a built-in proxy?** Two reach paths (SQL via auth proxy, Memorystore via VPC) means two failure modes. One connector, one network mental model.

**Hardening note.** The `allUsers` invoker binding is the standard "Cloud LB to Cloud Run" passthrough idiom; production hardening (Phase 2) replaces it with a specific LB SA principal. Documented in `deploy/scripts/deploy-gateway.sh` step `step_cloudrun` and runbook §13.

## Migrations

- DDL lives at `CanaryGo/deploy/migrations/*.{up,down}.sql`
- Tool: `golang-migrate/migrate` v4 (already used in dev — no new dep)
- Production application: a Cloud Run **job** (not service) that runs `migrate -path=deploy/migrations -database=$DATABASE_URL up`. Triggered manually before each deploy that includes new migrations, OR (Phase 2) wired into the Cloud Build pipeline as a pre-deploy step.

**Why a job, not a CI step?** Migrations need access to Cloud SQL via the same VPC + auth-proxy substrate as the runtime service. Cloud Build doesn't have that substrate by default. A Cloud Run job inherits the VPC connector + Cloud SQL bindings cleanly.

**Migration list at deploy time.** As of merge into main 2026-05-02:
- 015 protocol_source_secrets (GRO-746)
- 016 protocol_audit_log (GRO-694)
- 017 protocol_evidence (GRO-748)
- 018 protocol_source_secrets_sm_ref (GRO-687)
Plus all migrations 001–014 from the M1 foundation (already in repo).

## Observability

### Logs

- **Source.** Application logs from `zap` JSON output → stdout → Cloud Run agent → Cloud Logging
- **Retention.** 30 days default (free tier covers MVP)
- **Structured query examples** (saved in `runbook-gateway-deploy.md`):
  - All gateway 5xx in last 1h: `resource.type="cloud_run_revision" AND resource.labels.service_name="canary-gateway-staging" AND severity>=ERROR`
  - p99 latency by endpoint: requires log export to BigQuery (Phase 2 nice-to-have)

### Metrics + alerts

| Alert | Condition | Severity |
|---|---|---|
| `gateway-up` | Uptime check fails > 1 minute (HTTPS GET `/healthz`, 60s interval) | S0 page |
| `gateway-p99-latency` | p99 > 5ms over rolling 5min window | S1 |
| `gateway-5xx-rate` | 5xx > 1% of total requests over 5min | S0 page |
| `sql-cpu` | Cloud SQL CPU > 80% for 5min | S2 |
| `sql-connections` | Open connections > 80% of `max_connections` | S2 |
| `redis-memory` | Memorystore memory > 80% used | S2 |

**SLO posture (per `project_cloud_provider_accountability_stance` — fourth accountability rail).** We hold GCP to:
- Cloud Run availability: 99.95% (per Google's published SLA)
- Cloud SQL availability: 99.95% (zonal HA → upgrade to regional at Phase 2)
- Memorystore availability: 99.9% (BASIC) — Sub 1 ensures durable replay path

If GCP misses an SLA, we calculate the credit and apply it. The exit posture (multi-cloud fallback or cooperative-controlled infrastructure) is documented in the platform stack-commitment card; not a Phase 1 concern, but the measurement starts now.

### Traces (Phase 2)

Cloud Trace integration is wired (the runtime SA has `roles/cloudtrace.agent`); enabling sampling is a Phase 2 task once we have enough traffic to justify the volume.

## Cost estimate at MVP

Working-document: actual numbers, monthly.

| Component | Tier / SKU | Monthly cost |
|---|---|---|
| Cloud Run | min-instance=1 (always-on), ~10K req/mo at MVP | ~$8 (mostly the always-on instance hour) |
| Cloud SQL | db-g1-small, 10 GB SSD, point-in-time-recovery | ~$25 |
| Memorystore Redis | BASIC, 1 GB, us-central1 | ~$30 |
| Cloud LB | 1 forwarding rule + 1 backend | ~$18 |
| Cloud Armor | Up to 10M requests inspected | ~$5 (free at MVP volume) |
| Secret Manager | ~10 secrets × $0.06 + 100K accesses × $0.03/10k | ~$1 |
| Artifact Registry | ~5 GB images | ~$0.50 |
| Cloud Build | <2K build-minutes/mo | $0 (free tier) |
| Cloud Logging | <50 GiB ingest/mo | $0 (free tier) |
| Cloud Monitoring | Standard metrics | $0 (free tier) |
| VPC connector | 2 e2-micro instances always running | ~$10 |
| **Total** | | **~$98 / month** |

**Cost discipline.** Solo-founder economics. If any line item drifts above its target, the runbook escalation triggers a founder check before scaling further. The $200/mo cost ceiling per session escalation criteria is the hard line.

**Where the next dollar goes.** Memorystore is the chunkiest line item. Phase 2 alternative: skip Memorystore for staging and use Cloud SQL `LISTEN/NOTIFY` as the queue substrate (free, but less throughput). Not pursued for Phase 1 because the `redis/v9` client is already wired into the gateway code.

## Patent-claim verification

The gateway deployment is the operating embodiment of Node 2 (Patent Application 63/991,596, FIG. 1 and FIG. 4):

| Patent claim | Implementation evidence |
|---|---|
| Node 2 = HMAC verification, payload hashing, queue publish | `CanaryGo/cmd/gateway/main.go` + `internal/protocol/{hmac,publisher,webhook}/` (commits 8d1fb09, 733a665) |
| Per-source signing key resolution | `internal/protocol/secrets/secrets.go` interface + `sm_resolver.go` (GRO-687) |
| Append-only event publish | Valkey Streams (Memorystore Redis) — `XADD` is append-only at the data-structure level |
| Bilateral verification surface | `GET /v1/protocol/evidence/{event_hash}` (GRO-748 wires the handler) |

The deployment substrate (Cloud Run, Cloud SQL, Memorystore, LB, Secret Manager) is commodity infrastructure — no patent claims live there. The patent IS the architecture; the substrate is the execution venue.

## Cross-track integration

This SDD assumes the parallel Wave 1 tracks land in the merge order specified in the session plan §Wave 2:

1. **GRO-694 audit middleware** — modifies `cmd/gateway/main.go` to mount audit middleware. Migration 016 lands first.
2. **GRO-687 Secret Manager** — adds `SmResolver` and migration 018; gateway picks up via `SECRET_BACKEND=sm` env var (set in `cloudbuild.gateway.yaml`).
3. **GRO-748 L1 Evidence Store** — adds migration 017 + `cmd/sub1-hash-seal` worker (separate Cloud Run service, deployed in a follow-up dispatch) + `GET /v1/protocol/evidence/{event_hash}` handler in the gateway.
4. **GRO-693 legal docs** — pure documentation; doesn't affect deployment substrate.

The runbook §10 sequences the migration applications and Cloud Run deploys to honor this order.

## Outstanding questions for founder

1. **DNS provider for `api.canary.growdirect.io`.** The `gcp-foundation-runbook` doesn't explicitly state Cloudflare vs Cloud DNS for this subdomain. Default assumption per CLAUDE.md is **Cloudflare** (Cloudflare manages `growdirect.io`). The `step_lb` script outputs the LB static IP; founder enters the A-record manually in Cloudflare (proxy disabled / grey-cloud, since we want Google-managed cert end-to-end). Cloudflare API access is flagged in the session escalation criteria — **founder confirmation needed before runbook §12 executes**.
2. **Region.** us-central1 chosen for cost (cheapest tier) and proximity to Bay Area users. If founder has a strong preference (us-west2 for latency, eu-west1 for GDPR posture), runbook §1 substitutions accommodate.
3. **Initial seed merchant + secret.** Runbook §11 seeds one test secret (`canary-source-{TEST_MERCHANT_UUID}-square`) for the smoke-test webhook. Founder picks the test merchant_id (or it's a fresh UUID per first-deploy).
4. **Cost-confirmation gate.** $98/mo projected; well under the $200 ceiling. Runbook §0 includes an explicit cost confirmation step before any provisioning runs.

## Related

- `Brain/wiki/cards/gcp-foundation-runbook.md` — already-provisioned substrate (org, project, IAM)
- `Brain/wiki/cards/platform-stack-commitment.md` — buy-vs-build posture
- `docs/sdds/canary-go/secrets-manager-integration.md` (GRO-687) — Secret Manager integration design
- `CanaryGo/deploy/Dockerfile.gateway` — container image definition
- `CanaryGo/deploy/cloudbuild.gateway.yaml` — CI/CD pipeline
- `CanaryGo/deploy/scripts/deploy-gateway.sh` — idempotent provisioning script
- `CanaryGo/deploy/runbook-gateway-deploy.md` — Wave 4 execution runbook
- Linear: [GRO-756](https://linear.app/growdirect/issue/GRO-756) (this dispatch) · [GRO-739](https://linear.app/growdirect/issue/GRO-739) (parent)
- Patent: Application 63/991,596
