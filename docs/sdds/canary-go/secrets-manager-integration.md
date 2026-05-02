---
type: sdd
status: draft
date: 2026-05-02
gro: GRO-687
parent: GRO-739
scope: canary-go
component: protocol/secrets
---

# Secrets Manager Integration — Canary Gateway

> **Governing thesis:** v1 stored per-source HMAC secrets as plaintext
> in `protocol.source_secrets.secret`. One accidental dump and every
> webhook on the platform is forgeable. GRO-687 retires the plaintext
> path: secret values move to GCP Secret Manager, Postgres keeps only
> metadata + a resource pointer, and `secrets.Resolver` stays
> shape-stable so the webhook handler doesn't change.

## 1. Scope

| In scope | Out of scope |
|---|---|
| Per-(merchant, source_code) HMAC webhook secrets resolved by the gateway (GRO-746) | Other key classes from GRO-687 brief (`CANARY_ENCRYPTION_KEY`, `JWT_SECRET`, hash keys, OAuth client secrets, MCP API keys) — separate dispatches |
| Postgres schema change (migration 018) | Backfill of existing prod secrets — none exist yet (MVP) |
| Gateway wiring (`SECRET_BACKEND` env var) | Multi-region SM replication strategy |
| Local-dev fallback to PgxResolver | Customer-managed encryption keys (CMEK) — phase 4 |

This SDD covers only the webhook-secret path. The other key classes
listed in the GRO-687 brief follow the same buy-vs-build pattern but
have different consumers and lifecycles; each gets its own SDD when
its dispatch lands.

## 2. Architecture

### 2.1 Decomposition

```
┌─────────────────────────────────────────────────────────────────┐
│                   API Gateway (Node 2)                          │
│                                                                 │
│   ┌──────────────┐      ┌────────────────────────────────┐      │
│   │   webhook    │─────▶│ secrets.Resolver (interface)   │      │
│   │   handler    │      └────────────────────────────────┘      │
│   └──────────────┘             │            │                   │
│                                │            │                   │
│                  PgxResolver◀──┘            └──▶SmResolver      │
│                  (dev)                          (prod)          │
└────────┬───────────────────────────────────────┬────────────────┘
         │                                       │
         ▼                                       ▼
   ┌─────────────────────┐        ┌────────────────────────────┐
   │ Postgres            │        │ Postgres (metadata only)   │
   │ protocol.           │        │ + GCP Secret Manager       │
   │ source_secrets      │        │ canary-source-{m}-{s}      │
   │ (.secret plaintext) │        │ (encrypted, versioned)     │
   └─────────────────────┘        └────────────────────────────┘
```

The interface (`Resolver.Lookup`) is unchanged from v1. Backend
selection happens once at process startup; the handler doesn't know
which one it has.

### 2.2 Interface contract (preserved)

| Element | Shape |
|---|---|
| Method | `Lookup(ctx, merchantID uuid.UUID, sourceCode string) (Secret, error)` |
| Return: success | `Secret{ID, MerchantID, SourceCode, Secret []byte, SignatureAlgo, ReplayWindow}` |
| Return: not found | `secrets.ErrNotFound` (gateway maps to 401) |
| Return: other error | wrapped error (gateway maps to 500) |

`SmResolver` satisfies this contract; the only behavioral difference
is that `Secret.Secret` came from SM rather than from the row.

## 3. SM resource layout

### 3.1 Naming convention

```
projects/{PROJECT}/secrets/canary-source-{merchant_id}-{source_code}/versions/latest
```

| Component | Source | Notes |
|---|---|---|
| `{PROJECT}` | `GCP_PROJECT_ID` env var | `canary-rapidpos` in MVP |
| `{merchant_id}` | UUID, lowercased | matches `app.merchants.id` |
| `{source_code}` | string | matches `app.source_systems.code` (`rapidpos`, `square`, etc.) |
| `versions/latest` | literal | rotation = new version; gateway picks up via cache TTL |

The path is also stored as-is in `protocol.source_secrets.secret_sm_ref`
so seeding tooling, runtime, and ops queries all share one canonical
form. Centralized in `secrets.BuildResourcePath`.

### 3.2 Versioning posture

| Operation | Mechanism |
|---|---|
| Initial provisioning | Create secret resource + version 1 + insert Postgres row referencing the resource path |
| Rotation | Create new SM version; existing row unchanged; gateway picks up new value within `cacheTTL` (default 60s) |
| Revocation | Set Postgres row `status` to `revoked`; gateway returns ErrNotFound (401) within cacheTTL on the metadata side. Disable old SM version separately. |
| Hard kill | Disable the SM version; existing cached values continue to verify until expiry. Add a forced-invalidation API only if MTTR demands it. |

### 3.3 Region pinning

MVP: SM secrets are **automatic-replication** (default). No region
pinning. Future: pin to `us-west1` to match GKE region once the
gateway runs in production.

## 4. IAM policy

### 4.1 Required roles

| Principal | Role | Resource scope |
|---|---|---|
| Gateway service account (e.g., `canary-gateway@canary-rapidpos.iam.gserviceaccount.com`) | `roles/secretmanager.secretAccessor` | Filtered to `canary-source-*` secrets |
| Deployment SA (`canary-deploy@canary-rapidpos.iam.gserviceaccount.com`) | `roles/secretmanager.admin` | Same filter |
| Audit log readers | `roles/logging.viewer` on the project | Cloud Audit Logs are project-scoped |

### 4.2 Granting access (copy-paste)

Grant the gateway SA accessor on a single secret:

```bash
gcloud secrets add-iam-policy-binding \
  "canary-source-${MERCHANT_ID}-${SOURCE_CODE}" \
  --project="canary-rapidpos" \
  --member="serviceAccount:canary-gateway@canary-rapidpos.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

For project-wide grant scoped via condition (preferred at scale):

```bash
gcloud projects add-iam-policy-binding canary-rapidpos \
  --member="serviceAccount:canary-gateway@canary-rapidpos.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --condition='expression=resource.name.startsWith("projects/canary-rapidpos/secrets/canary-source-"),title=canary_source_secrets_only'
```

## 5. Rotation flow

| Step | Action | Mechanism |
|---|---|---|
| 1 | Generate new HMAC secret | 32 random bytes, base64url |
| 2 | Add SM version | `gcloud secrets versions add canary-source-{m}-{s} --data-file=-` |
| 3 | (no schema change) | Postgres row already points at `versions/latest` |
| 4 | Wait `cacheTTL` (60s default) | Gateway warm-cache flushes naturally |
| 5 | Disable previous SM version | `gcloud secrets versions disable {N-1} --secret=...` |
| 6 | Update merchant's webhook config (out of band) | Source network starts signing with new secret |

The cutover is graceful: during the cache-flush window both old and
new SM versions are active. Once the previous version is disabled,
only the new value verifies.

## 6. Audit logging

GCP Secret Manager **automatically** writes Cloud Audit Logs for every
`AccessSecretVersion` call. No application-side instrumentation
needed. Find them at:

```
gcloud logging read \
  'resource.type="secretmanager.googleapis.com/Secret" AND protoPayload.methodName="google.cloud.secretmanager.v1.SecretManagerService.AccessSecretVersion"' \
  --project=canary-rapidpos --limit=100
```

Operationally: route these logs to BigQuery for retention + anomaly
detection (rate spikes per principal, unusual source IPs). Out of
scope for this SDD — covered by the platform observability dispatch.

## 7. Cost model

GCP Secret Manager pricing (us-pricing as of 2026-05):

| Item | Rate |
|---|---|
| Active secret versions | $0.06 / version / month |
| Access operations | $0.03 / 10,000 operations |
| Rotation notifications | $0.05 / month (not used in MVP) |

### MVP scale estimate

| Driver | Value | Cost |
|---|---|---|
| 10 merchants × 1 source | 10 secrets | $0.60 / mo |
| Webhooks @ 1 per second @ 50% cache miss | ~1.3M accesses / mo per merchant; with cache → ~22k / mo | $0.07 / mo |
| **Total MVP** | | **~$0.67 / mo** |

The cache TTL is the single biggest knob for cost at scale.

## 8. Local dev fallback

| Var | Default | Effect |
|---|---|---|
| `SECRET_BACKEND` | `pgx` | Use plaintext `secret` column |
| `SECRET_BACKEND` | `sm` | Use SM; falls back to `pgx` on construct failure unless required |
| `GCP_PROJECT_ID` | (unset) | Required when `SECRET_BACKEND=sm` |
| `SECRET_BACKEND_REQUIRE_SM` | `0` | Set to `1` in production; makes SM construct failure fatal (no silent fallback) |

Behavior matrix:

| `SECRET_BACKEND` | `GCP_PROJECT_ID` | `REQUIRE_SM` | Result |
|---|---|---|---|
| (unset) or `pgx` | — | — | `PgxResolver` (dev default) |
| `sm` | set | `0` | `SmResolver`; falls back to `PgxResolver` with warn if construct fails |
| `sm` | set | `1` | `SmResolver`; **fatal** if construct fails |
| `sm` | unset | `0` | `PgxResolver` with warn |
| `sm` | unset | `1` | **fatal** at startup |

Production deployment manifests must set both `SECRET_BACKEND=sm` and
`SECRET_BACKEND_REQUIRE_SM=1`. The fallback is a developer
convenience, not a production safety net.

## 9. Schema changes

Migration `018_protocol_source_secrets_sm_ref` (idempotent):

| Change | SQL |
|---|---|
| `secret` → nullable | `ALTER TABLE protocol.source_secrets ALTER COLUMN secret DROP NOT NULL` |
| Add `secret_sm_ref text` | `ADD COLUMN IF NOT EXISTS secret_sm_ref TEXT` |
| Constraint: at least one of {secret, secret_sm_ref} populated | `CHECK (secret IS NOT NULL OR secret_sm_ref IS NOT NULL)` |
| Column comments | document deprecation of `secret` |

A follow-up migration drops the `secret` column once SM is the only
production backend. Tracked in this SDD; no GRO ticket yet.

## 10. Code layout

| File | Purpose |
|---|---|
| `internal/protocol/secrets/secrets.go` | `Resolver` interface + `Secret` struct + `PgxResolver` (unchanged) + `Memory` (unchanged) |
| `internal/protocol/secrets/sm_resolver.go` | `SmResolver`, `secretManagerClient` interface, cache, `BuildResourcePath` |
| `internal/protocol/secrets/sm_resolver_test.go` | Unit tests with mock SM client + log-sanitization assertion |
| `cmd/gateway/main.go` | `buildResolver(ctx, pool, logger)` selects backend by env vars |
| `deploy/migrations/018_*` | Schema changes |

## 11. Testing strategy

| Layer | Coverage |
|---|---|
| Unit | `sm_resolver_test.go` — mock SM client; cache hit/miss/expiration; NotFound mapping; PermissionDenied propagation; log sanitization (asserts secret value never appears in any captured zap entry) |
| Integration | Existing `webhook/integration_test.go` continues to use `secrets.Memory`; no change |
| End-to-end | Smoke test against real GCP project will land with the deployment dispatch (out of scope here) |

Log sanitization is enforced by `TestLogs_DoNotContainSecretValue`,
which scans every `Entry.Message`, `Field.String`, and
`Field.Interface` for the secret bytes after exercising success,
NotFound, and PermissionDenied paths.

## 12. Dependencies added

| Module | Version | Reason | Build cost |
|---|---|---|---|
| `cloud.google.com/go/secretmanager` | latest | SM client | indirect: gax-go, grpc, googleapis genproto, oauth2 — sizable but unavoidable for any GCP integration |

The transitive set is the standard GCP-Go footprint and is shared by
every other GCP-touching service in the build (per platform-stack-commitment).
First service to add it pays the up-front cost; subsequent services
amortize.

## 13. Open questions / follow-ups

| Question | Owner | Disposition |
|---|---|---|
| When does the legacy `secret` column get dropped? | Engineering | After all envs cut over to `SECRET_BACKEND=sm`; file follow-up GRO ticket |
| Multi-region SM replication policy? | Platform | Defer until prod region commitment |
| Customer-managed encryption keys (CMEK) for tier-1 merchants? | Product | Phase 4 (PCI scope dispatch) |
| Forced cache invalidation API for emergency rotation? | Engineering | Add when MTTR target is set |

## 14. References

- Linear: GRO-687 (this dispatch), GRO-739 (parent), GRO-746 (gateway baseline)
- Plan: `docs/superpowers/plans/2026-05-03-canary-gcp-blinking-multi-track-kickoff.md` §1.4
- Brain: `Brain/wiki/cards/gcp-foundation-runbook.md`, `Brain/wiki/cards/platform-stack-commitment.md`
- Migration: `CanaryGo/deploy/migrations/018_protocol_source_secrets_sm_ref.up.sql`
- Code: `CanaryGo/internal/protocol/secrets/sm_resolver.go`, `CanaryGo/cmd/gateway/main.go`
- GCP docs: <https://cloud.google.com/secret-manager/docs/overview>
