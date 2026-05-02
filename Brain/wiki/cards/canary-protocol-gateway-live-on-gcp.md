---
card-type: runbook
card-id: canary-protocol-gateway-live-on-gcp
card-version: 1
domain: canary
layer: infra
status: approved
agent: ALX
tags: [canary, protocol, gateway, gcp, cloud-run, deployed, node-2, patent, blinking]
last-compiled: 2026-05-02
needs-review: 2026-08-02
---

## What this is

Operating record of the Canary Protocol API Gateway deployment to GCP, completed 2026-05-02. The gateway is the operating embodiment of **Patent Application 63/991,596 Node 2** — HMAC verify + payload hash + queue publish. Live at `https://api.canary.growdirect.io`, accepting signed webhooks from outside the laptop, with full audit trail in Cloud SQL.

## Live endpoints

| Endpoint | Purpose | Status |
|---|---|---|
| `GET https://api.canary.growdirect.io/health` | Liveness probe | 200 OK |
| `POST https://api.canary.growdirect.io/v1/protocol/webhook/{source}` | Signed-webhook ingress | 200 OK with `event_id` + `event_hash` |
| `GET https://api.canary.growdirect.io/v1/protocol/evidence/{event_hash}` | Bilateral verification | Reads from `protocol.evidence` (requires Sub 1 worker — see Related) |

## GCP resources

| Layer | Resource | Note |
|---|---|---|
| Project | `canary-rapidpos` (number `515966226071`) | Org `growdirect.io`, billing linked |
| Region | `us-central1` | All resources colocated |
| LB static IP | `34.49.213.18` | Anycast, both 80 + 443 forwarding rules |
| DNS | Cloudflare A-record `api.canary.growdirect.io` → `34.49.213.18` | DNS only / grey cloud (mandatory for managed-cert ACME) |
| Cert | `canary-gateway-cert-v2` (Google-managed) | ACTIVE; auto-renewing |
| Backend service | `canary-gateway-backend` (serverless NEG) | No `--protocol` flag (incompatible with serverless NEG); Armor currently DETACHED (see GRO-758) |
| Cloud Run | `canary-gateway-staging`, image `gateway:5455f88` | min=1, max=10, concurrency=80, cpu=1, memory=512Mi |
| Cloud Run env | `SECRET_BACKEND=sm`, `GCP_PROJECT_ID=canary-rapidpos`, `LOG_LEVEL=info` | Plus `DATABASE_URL`, `VALKEY_URL`, `INTERNAL_SERVICE_SECRET`, `SESSION_SECRET` from Secret Manager |
| Cloud SQL | `canary-pg` (db-g1-small ENTERPRISE, Postgres 17) | Private IP `172.17.0.3`; PITR enabled; daily backups 08:00 |
| Memorystore | `canary-redis` (BASIC 1 GB, Redis 7.2) | Private service access |
| Secret Manager | 4 gateway secrets + per-merchant source HMAC secrets pattern `canary-source-{merchant_id}-{source_code}` | `canary-gateway-rt` runtime SA has `roles/secretmanager.secretAccessor` |
| VPC | `default` + connector `canary-vpc-conn` (e2-micro, range 10.8.0.0/28) + Service Networking peering | Peering allocates `google-managed-services-default` /16 |
| IAM SAs | `canary-deploy@…` (build) · `canary-gateway-rt@…` (runtime) | Org policy `iam.allowedPolicyMemberDomains` overridden to `ALLOW_ALL` at project level — see Invariants |

## Cost (validated 2026-05-02)

~$98/mo MVP run rate. Cloud Run + Cloud SQL + Memorystore + LB + Armor + Secret Manager + VPC connector. Below the $200/mo founder-imposed escalation ceiling.

## Patent-claim verification

| Claim | Implementation evidence on GCP |
|---|---|
| Node 2: HMAC verify + payload hash + queue publish | `cmd/gateway/main.go` running on Cloud Run; smoke-test confirmed |
| Per-source signing key resolution from secrets | `SmResolver` (GRO-687) fetched `canary-source-{merchant}-square` from GCP Secret Manager during the live request |
| Audit trail of every state-mutating invocation | Row in `app.audit_log` with full context: event_id, payload_digest, request_id, latency, status, source IP |
| Append-only event publish to streams | XADD to Memorystore Streams `protocol:events` |
| Bilateral verification surface | `GET /v1/protocol/evidence/{event_hash}` (handler from GRO-748) |

## Smoke-test contract

The reference signed-webhook smoke test (matches the verifier in `internal/protocol/hmac/hmac.go`):

```bash
PAYLOAD='{"event_type":"order.created","occurred_at":"...","data":{...}}'
TIMESTAMP=$(date +%s)
NONCE=$(openssl rand -hex 16)
SIG=$(printf '%s.%s.%s' "$TIMESTAMP" "$NONCE" "$PAYLOAD" \
  | openssl dgst -sha256 -hmac "$SECRET" -hex | awk '{print $2}')

curl -i -X POST https://api.canary.growdirect.io/v1/protocol/webhook/square \
  -H "Content-Type: application/json" \
  -H "X-Canary-Merchant: $MERCHANT_UUID" \
  -H "X-Canary-Timestamp: $TIMESTAMP" \
  -H "X-Canary-Nonce: $NONCE" \
  -H "X-Canary-Signature: $SIG" \
  -d "$PAYLOAD"
```

Expected: HTTP 200 + `{"event_id": "...", "event_hash": "...", "status": "accepted"}`. Canonical signed string is `<unix_ts>.<nonce>.<payload>` with dot separators.

## Operational gotchas

1. **Cloud SQL is private-IP only.** Laptop can't reach it via `cloud-sql-proxy` (private IP needs to be in-VPC). Workaround: temporarily `gcloud sql instances patch canary-pg --assign-ip` + add laptop public IP to authorized networks, then `--no-assign-ip` after. Long-term: bastion VM or Cloud Run jobs.
2. **Cloud Armor currently DETACHED.** Default policy false-positives on `Content-Type: application/json` POSTs. Tracked in GRO-758. Gateway is running without WAF until that's tuned.
3. **`allUsers` invoker required for LB→Cloud Run pass-through.** Org policy `iam.allowedPolicyMemberDomains` overridden to `ALLOW_ALL` at project level. Revisit if this project takes customer data.
4. **Cert-recreation is the way to retry FAILED_NOT_VISIBLE.** First cert provisioning attempt fails because DNS lags. After DNS resolves, recreate the cert (delete + create) — Google retries the ACME challenge fresh and provisions in 5-15 min.
5. **Service Networking peering is a hidden prerequisite for private-IP Cloud SQL.** The `servicenetworking.googleapis.com` API enable isn't enough — you also need to allocate `google-managed-services-default` IP range and `vpc-peerings connect`. Now in `deploy/scripts/deploy-gateway.sh` step_vpc.

## Invariants

- The `--no-allow-unauthenticated` flag on Cloud Run + the org-policy `ALLOW_ALL` override + the explicit `allUsers` invoker binding together form the LB→Run pass-through. Removing any one breaks public access.
- Per-merchant source secrets follow the pattern `canary-source-{merchant_id}-{source_code}` in Secret Manager. SmResolver naming is hardcoded to this; changing the pattern requires both code + data migration.
- The runtime SA `canary-gateway-rt` must NEVER be granted broader Secret Manager access than `secretAccessor` scoped to `canary-source-*` and `canary-gateway-*` patterns. Project-wide accessor is the current state — production hardening narrows it.
- `protocol.evidence` writes only via Sub 1 worker (separate Cloud Run service, code in `cmd/sub1-hash-seal/`). Gateway never writes to `protocol.evidence` directly. UPDATE/DELETE blocked by DB triggers.

## Related

- Patent: Application 63/991,596 (FIG. 1, FIG. 4 — Node 2 + Triple Subscriber)
- SDD: `docs/sdds/canary-go/gcp-deployment-gateway.md`
- Runbook: `CanaryGo/deploy/runbook-gateway-deploy.md` (executable cold)
- Provisioning script: `CanaryGo/deploy/scripts/deploy-gateway.sh` (idempotent; 9-step gcloud)
- Cloud Build config: `CanaryGo/deploy/cloudbuild.gateway.yaml`
- Dockerfile: `CanaryGo/deploy/Dockerfile.gateway` (Go 1.25-alpine → distroless static)
- Foundation: `Brain/wiki/cards/gcp-foundation-runbook.md`
- Stack commitment: `Brain/wiki/cards/platform-stack-commitment.md`
- Linear: GRO-756 (this deploy, Done) · GRO-739 (parent, Phase 1 substrate ship)
- Follow-ups: GRO-758 (Armor tuning), Sub 1 worker deploy (TBD)
- Smoke-test commit: `gateway:5455f88` (image), `a272ede` (script fixes)
