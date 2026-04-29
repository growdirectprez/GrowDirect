---
type: dispatch
target: any
agent: ALX or Canary Builder
priority: high
status: ready
created: 2026-04-29
---

# Wave 2 SDD Polish — Enterprise-from-Day-One Posture

## Brief

Polish the Wave 2 platform-primitive SDDs in `docs/sdds/go-handoff/` against a unified enterprise architectural posture: GCP-native, Go monorepo, Postgres-backed, multi-tenant by design, horizontally scalable on demand, and SOC 2 / ISO 27001 / PCI DSS / GDPR / CCPA-ready from day one. Fold the Optional Features discipline (L402, ILDWAC, blockchain anchor, vendor smart contracts — all opt-in via env flag, all default `false`) into every SDD that touches those features, by reference to the canonical section in `platform-overview.md` rather than re-litigating it locally.

This is one comprehensive pass across ~12 SDDs. Each SDD is edited in place. The pass commits per logical batch (3–5 SDDs at a time), with a summary report per batch listing changes, open questions, and any content flagged for IP review before publication.

---

## Architectural Posture (Non-Negotiable)

### Stack Commitment

- **Cloud:** GCP end to end. Per `platform-stack-commitment` — single primary cloud, no multi-cloud, no AWS. Walmart/Target/Kroger anti-Amazon posture.
- **Language:** Go 1.21+. Monorepo. Per `go-module-layout`.
- **HTTP:** Chi. Per `go-runtime`.
- **Database:** Cloud SQL for PostgreSQL 17, with `pgvector` and `pg_trgm` extensions.
- **Cache / sessions / hot path:** Memorystore (Valkey-compatible).
- **Compute:** Cloud Run.
- **Async:** Pub/Sub + Cloud Tasks + Eventarc.
- **AI / inference:** Vertex AI (Anthropic Claude + embeddings).
- **CI/CD:** Cloud Build → Artifact Registry → Cloud Run.
- **Observability:** Cloud Logging, Monitoring, Trace, Profiler, Error Reporting. Per `go-observability`.
- **DNS / TLS / Edge:** Cloud DNS + Certificate Manager + Cloud Load Balancing + Cloud Armor.
- **Identity:** Home-grown. Per `identity.md` — federation broker built on `coreos/go-oidc`, `crewjam/saml`, `go-ldap/ldap`, `elimity-com/scim`. Not Identity Platform.

No legacy ties. Greenfield from `go.mod` up.

### Multi-Tenant Architecture

**Schema-per-tenant is the canonical isolation boundary.** Each merchant gets a dedicated Postgres schema. Application code sets `SET search_path TO {tenant_schema}, public` per request based on the JWT `merchant_id` claim. This produces:

- **Strong isolation** — a query without a tenant context resolves nothing in tenant tables (only the `public` schema for shared reference data)
- **Per-tenant migrations** when needed — schema creation is per-tenant; backfills can run tenant by tenant
- **Schema-level grants** as the primary access control — admin role gets `USAGE` across all schemas; tenant role only gets `USAGE` on its own
- **Backup granularity** — per-tenant restore is `pg_dump --schema=$tenant_schema` then `pg_restore`

**Within a tenant schema:**
- UUID primary keys (`gen_random_uuid()`)
- `created_at` / `updated_at` on every table
- Row-Level Security (RLS) **optional** — used when finer-grained constraints are needed within a tenant (e.g., role-based row visibility for the multi-merchant organization model in ADR-001)
- Column-level constraints via PostgreSQL's column GRANT/REVOKE for the few cases where it matters

**Cross-tenant admin queries:**
- A dedicated admin role with `USAGE` on all schemas; queries use schema-qualified names (`schema_a.table` JOIN `schema_b.table`)
- Cross-tenant analytics queries materialize into a separate `analytics` schema via scheduled rollup jobs — admin queries hit the materialization, not the tenant schemas, to avoid lock contention
- Audit log of every cross-tenant query (admin role activity goes to the `audit` schema)

**Sharding posture (V2 path, not V1):**
- V1: Cloud SQL primary + 2 read replicas. ~1,000 tenants is comfortable on a single regional instance.
- V2: When tenant count exceeds 5,000 OR query latency on the largest tenants degrades, evaluate AlloyDB for Postgres (drop-in compatibility, columnar read engine, better horizontal scaling).
- V3: When AlloyDB read replicas no longer suffice, application-level sharding by `org_id` range. Schemas physically distribute across multiple primaries; routing layer in the identity service.

### Scale-Out Posture

- **Horizontal compute:** Cloud Run scales every service independently to demand. No fixed instance count.
- **Horizontal database reads:** Cloud SQL read replicas for analytics + tenant-scoped reads. Writes go to primary.
- **Connection pooling:** PgBouncer fronting Cloud SQL — required from day one. Transaction-mode pooling.
- **Cache:** Memorystore for hot path. Tenant namespace prefix every key (`{merchant_id}:{domain}:{key}` per `raas.md`).
- **Async work:** Pub/Sub for fan-out, Cloud Tasks for delayed/scheduled work, Eventarc for cross-service event routing.
- **Per-merchant blast radius:** Every query carries `WHERE merchant_id = $1` (or hits the tenant schema). No service touches another tenant's rows by default.

### Security Baseline

**Encryption everywhere.**

| Layer | Mechanism |
|---|---|
| At rest (DB) | Cloud SQL CMEK (Cloud KMS) — customer-managed keys |
| At rest (object storage) | Cloud Storage CMEK (Cloud KMS) |
| At rest (field-level Restricted/Sensitive) | AES-256-GCM via `internal/security` per `go-security` |
| In transit (external) | TLS 1.3 only via Cloud Load Balancing |
| In transit (service-to-service) | mTLS via Cloud Run service mesh |
| Secrets | GCP Secret Manager (never env files in production) |
| Per-subject keys (PII) | Cryptographic erasure pattern per `platform-cryptographic-erasure` |
| PII lookup hashes | HMAC-SHA256 with per-domain keyed-hash secrets per `platform-pii-hashing` |

**Network perimeter:**
- VPC-SC perimeter around Cloud SQL + Memorystore + Cloud Storage + Vertex AI + Secret Manager
- Cloud Armor at the edge — DDoS protection + WAF rules
- All ingress through Cloud Load Balancing → Cloud Run
- Egress via VPC NAT for external dependencies (Lightning, Square, NCR, OrdinalsBot)
- **Cloud SQL on private IP only** — public IP never enabled

**IAM:**
- Principle of least privilege — every Cloud Run service has its own service account with minimum required IAM bindings
- No service has cross-tenant default access. Cross-tenant grants are explicit, audited, and time-bounded.
- IAM database authentication for human admin access; service accounts use IAM auth or Cloud SQL Auth Proxy with per-service IAM identity.

**Audit:**
- Cloud Audit Logs enabled at Admin Activity, Data Access, and System Event tiers
- Application-level audit logs to the `audit` schema (per-tenant)
- Authentication events, role changes, cross-tenant queries, key rotations, encryption key operations — all written to `audit`
- Audit log access itself is audited (audit-of-audit)

### Backup, DR, and SLA

**Backup:**
- PITR enabled with **7-day continuous recovery window**
- Daily automated backups, **35-day retention**
- Weekly logical export (`pg_dump`) to Cloud Storage with **7-year retention** for financial data, **35 days** for non-financial
- Per-tenant restore via `pg_dump --schema={tenant_schema}` + `pg_restore` to a recovery instance

**Disaster recovery:**
- Cross-region read replica in a different GCP region (e.g., primary `us-central1`, replica `us-east1`)
- **RPO: 5 minutes** (continuous WAL streaming)
- **RTO: 30 minutes** (failover + DNS swap)
- Quarterly DR drill — actually fail over, actually serve from replica, actually fail back. Documented in runbook.

**Production SLAs:**

| Surface | Uptime | RPO | RTO | Notes |
|---|---|---|---|---|
| Platform overall | 99.95% | 5 min | 30 min | ~4.4 hours/year downtime budget |
| Customer-facing API (`api.canary`) | 99.9% | 5 min | 30 min | ~8.76 hours/year |
| POS write path (`tsp` + `webhook-pipeline`) | 99.95% | 5 min | 15 min | Highest tier — store operations depend on this |
| Internal services (analytics, reporting) | 99.5% | 1 hour | 4 hours | Lower tier — degraded service is acceptable |
| Audit log ingestion | 99.99% | 0 (sync) | 5 min | Compliance-critical |

**Breach notification SLA:** 72 hours per GDPR. Internal target: 24 hours from confirmed breach to merchant notification.

### Compliance Posture

| Standard | Posture | Audit Target |
|---|---|---|
| SOC 2 Type 2 | Day-one design — controls baked in; readiness audit at month 6, full audit at month 12 | Month 12 |
| ISO 27001 | Alignment from day one; certification optional for early customers, required for enterprise tier | Month 24 |
| PCI DSS | Level 4 minimum (small merchants); Level 2 architecture readiness | Continuous |
| GDPR | Cryptographic erasure pattern, DSAR pipeline, data classification — all designed in. No retrofit. | Continuous |
| CCPA | Subset of GDPR controls — same plumbing | Continuous |
| HIPAA-adjacent | For verticals with health-adjacent merchandise (pet pharma, OTC) — controls map to the same data classification scheme | As required per merchant |

---

## Files to Load for Context

A fresh session must load these in order before editing any SDD. Each file establishes a constraint the SDDs operate under.

**Platform context:**
- `CLAUDE.md` — platform rules, session discipline
- `.claude/skills/sdd-writer.md` — 4-hat methodology, frontmatter template, quality gates, voice standards

**Engineering substrate (Wave 1 — already polished, this is reference):**
- `docs/sdds/go-handoff/INDEX.md` — full SDD inventory
- `docs/sdds/go-handoff/go-runtime.md` — lifecycle, middleware stack, actor type discrimination
- `docs/sdds/go-handoff/go-module-layout.md` — port registry, package layout, repo structure
- `docs/sdds/go-handoff/go-security.md` — JWT, AES-256-GCM, HMAC, PII hashing
- `docs/sdds/go-handoff/go-observability.md` — slog, Prometheus, OTel hooks
- `docs/sdds/go-handoff/go-errors.md` — error taxonomy
- `docs/sdds/go-handoff/go-testing.md` — test infrastructure
- `docs/sdds/go-handoff/identity.md` — federation modes, L402 (opt-in), membership boundary
- `docs/sdds/go-handoff/external-identities.md` — POS entity bridging
- `docs/sdds/go-handoff/platform-overview.md` — **Optional Features section is the canonical source for env-flag pattern**

**Brain wiki — architectural posture cards:**
- `Brain/wiki/cards/platform-thesis.md` — three rails, meter model, closed-loop economy
- `Brain/wiki/cards/platform-stack-commitment.md` — vendor commitment, no AWS, GCP-native
- `Brain/wiki/cards/platform-architectural-continuity.md` — six properties (statelessness, federation, idempotency, content addressability, layered abstraction, cryptographic verification)
- `Brain/wiki/cards/platform-data-classification.md` — Restricted / Sensitive / Internal / Public scheme
- `Brain/wiki/cards/platform-pii-hashing.md` — keyed HMAC standard
- `Brain/wiki/cards/platform-cryptographic-erasure.md` — per-subject DEK pattern
- `Brain/wiki/cards/platform-performance-nfrs.md` — Retek-era principles, modern stack
- `Brain/wiki/cards/platform-pwc-benchmarks.md` — financial NFR reference

**Memory bus queries to run before editing each SDD:**
- `memory_recall("{module-name} {primary concern}")` — surface prior decisions
- `memory_recall("multi-tenant schema postgres")` — confirm tenant isolation pattern
- `memory_recall("backup retention RPO RTO")` — confirm DR commitments
- `memory_recall("data classification {field-name}")` — confirm PII handling per field

---

## SDD Polish Scope (Wave 2)

Twelve SDDs, in this order. Each batch commits separately.

### Batch 1 — Architecture Spine (5 SDDs)

| SDD | Polish focus |
|---|---|
| `architecture.md` | Service mesh topology, startup order, dependency graph, multi-tenant schema strategy at the architecture level |
| `microservice-architecture.md` | REST contract patterns, idempotency, retry semantics, mTLS posture |
| `data-model.md` | Schema-per-tenant pattern, public-schema reference data, audit schema, materialization schema for cross-tenant analytics. Field-level encryption + classification per data class. |
| `data-classification-inventory.md` | Already current per the wiki card; verify SDD reflects the four-tier scheme + treatment matrix |
| `pos-adapter-substrate.md` | Multi-POS abstraction; how new sources plug in without schema migration |

### Batch 2 — Receipt Chain (3 SDDs)

| SDD | Polish focus |
|---|---|
| `raas.md` | Receipt chain backbone — required core. Hash chain, sequence integrity, namespace resolution, MCP surface. Verify the chain operates **independently** of L402 (no L402 dependency) and **independently** of blockchain anchoring (anchor is async, non-blocking). |
| `factory-pipeline.md` | TSP pipeline (hash-before-parse, chain hash, Merkle batching). Verify SHA-256 sealing is required core; Merkle anchoring is optional (env flag). |
| `agent-contracts.md` | Agent topology contract spec — every `cmd/<service>/` boundary. Tie to use-case matrices in the CRB module pages. |

### Batch 3 — Optional Features (3 SDDs — IP-sensitive)

These are architectural direction. The SDDs document the design but every runtime behavior is env-gated.

| SDD | Polish focus |
|---|---|
| `ildwac.md` | Five-dimension cost model. Patent #63/991,596. **Default off via `ILDWAC_ENABLED`**. When off, standard ILWAC (Item × Location × WAC) operates. Mark IP scope clearly per sdd-writer Compliance hat requirements. |
| `l402-otb.md` | Already polished; verify the Optional Features reference is in place and the env-flag pattern is consistent. |
| `blockchain-anchor.md` | Public Bitcoin L2 anchoring of chain hashes. **Default off via `BLOCKCHAIN_ANCHOR_ENABLED`**. Anchor failures are non-blocking — internal SHA-256 chain operates regardless. |

### Batch 4 — Cross-cutting (1 SDD)

| SDD | Polish focus |
|---|---|
| `platform-overview.md` | Verify the Optional Features canonical section is the single source of truth. Add the multi-tenant strategy summary, the DR/SLA table from this dispatch, and the compliance posture table. |

---

## Polish Standards (per SDD)

Every Wave 2 SDD must satisfy:

1. **Frontmatter complete** — `spec-version`, `target-implementation: Go`, `stack: PostgreSQL 17 + pgx + sqlc | Chi HTTP | REST | go-redis | pgvector-go`, `status: handoff-ready` (after polish), `binary` and `port` (where applicable), `mcp-server`, `license: Apache-2.0`, `copyright: "Copyright (c) 2026 GrowDirect LLC"`, `updated: 2026-04-29`.

2. **4-Hat structure** — Business, Technical, Ops, Compliance, in that order. Per `sdd-writer.md`.

3. **Governing thesis** — first paragraph of Business is the thesis. What problem this solves commercially. What breaks without it.

4. **Multi-tenant strategy** — every SDD that owns tables documents how it operates under schema-per-tenant. Search-path pattern. Tenant-vs-public-vs-audit schema split. Cross-tenant admin query path (where applicable).

5. **Optional Features discipline** — anywhere L402, ILDWAC, blockchain anchor, or vendor smart contracts are referenced, link to `platform-overview.md` "Optional Features" instead of re-stating the env-flag pattern. Never describe these features as required.

6. **Encryption posture per data class** — per-table or per-field, reference `platform-data-classification`. Restricted → AES-256-GCM. Sensitive → AES or keyed HMAC depending on lookup needs. Internal → DB-level encryption only. Public → integrity controls (hashes), no encryption.

7. **SLA table** — Hat 3 (Ops) includes the SLA table with P50, P99, hard limit, breach action. Per `sdd-writer.md`. Align with the platform SLA tier in this dispatch.

8. **Failure modes table** — Hat 3 (Ops) includes failure modes with detection, recovery, blast radius.

9. **Backup + retention table** — Hat 4 (Compliance) includes per-data-class retention schedule and backup posture.

10. **Patent scope note** — required in Hat 4 (Compliance) for any SDD that implements hash-chain anchoring, WAC computation with provenance weighting, IL(Device/MCP/Port/)WAC, Bitcoin ordinal, or L402 gating. Per `sdd-writer.md`.

11. **Related section** — bidirectional cross-references to upstream and downstream SDDs. Every Wave 2 SDD references the Wave 1 substrate it depends on (`go-runtime`, `go-security`, etc.) and the upstream / downstream services in the spine.

12. **Voice** — Big 4 polish. Confident. Direct. Tables for facts. Prose only for narrative. No prose walls without a governing idea.

---

## Quality Gates (per SDD, before commit)

- [ ] Frontmatter complete with license + copyright
- [ ] Status promoted to `handoff-ready` only when all gates pass
- [ ] Governing thesis in first paragraph of Business
- [ ] Multi-tenant strategy documented (or N/A with explicit reason)
- [ ] All Optional Features references go through `platform-overview.md`, not re-stated
- [ ] Encryption + retention per data class
- [ ] SLA table aligned with platform tier
- [ ] Patent scope noted in Compliance where applicable
- [ ] `healthz` and `readyz` separate (per `go-runtime`)
- [ ] Cross-references bidirectional (this SDD references X; X references this SDD)
- [ ] Related section at the end
- [ ] Port claimed in `go-module-layout.md` (where applicable)
- [ ] No prose walls without a governing idea

---

## Output Expectations

**Per batch (3–5 SDDs):**

1. Edits committed in a single batch commit per Wave-2-batch.
2. Commit message: `sdds: Wave 2 batch N polish — <scope>` with bulleted summary of changes per SDD.
3. Status report appended to a session log at `docs/superpowers/specs/2026-04-29-wave-2-sdd-polish-log.md` listing:
   - SDDs polished
   - Major changes per SDD (1–2 lines each)
   - Open questions surfaced (founder decision required)
   - Any IP-sensitive content flagged for review before publication

**At completion of Wave 2:**

1. Final commit with INDEX.md update if SDD inventory changed.
2. Memory bus reseeded (post-commit hook handles incremental).
3. Summary memory stored via `memory_store` capturing:
   - Wave 2 scope completed
   - Architectural posture confirmed
   - Optional Features discipline applied across the library
   - Open questions list with founder follow-ups
4. Status reported back to founder with:
   - Total files edited
   - Commit hashes
   - Open questions (numbered, prioritized)
   - Recommended next wave

**Branch policy:** edits go directly to `main` for SDDs in `docs/sdds/go-handoff/`. These are internal engineering specifications; no PR review process is required at this stage. The post-commit hook handles memory bus seeding.

---

## Open Questions Inherited from Wave 1 (resolve in Wave 2)

1. **Chain-of-record for vendor smart contracts.** AVAX vendor private subnet vs. Base / Polygon for public anchor — reconcile the conflict between `ilwac-extended-bitcoin-standard` (says AVAX) and `infra-blockchain-evidence-anchor` (says Base / Polygon). Recommendation: **two chains, two purposes** — AVAX private subnet for vendor contracts (low cost, EVM-compatible, private); Base or Polygon for public evidence anchoring (decentralized, externally verifiable). Document the split in `blockchain-anchor.md` and `ildwac.md`. **Both behind env flags; neither required.**

2. **MCP Go server library.** Memory Bus is on Python FastMCP. New Canary Go services need their own MCP server impl. Recommendation: **build a thin Go MCP shim** that mirrors the Python SDK contract. Don't fork a community library — protocol is small and stable. Document in `microservice-architecture.md`.

3. **Connection pooling target.** PgBouncer is required for Cloud SQL at scale. Decide: self-hosted PgBouncer on Cloud Run sidecar vs. Cloud SQL Connector with built-in pooling vs. a third option. Recommendation: **PgBouncer on Cloud Run as a separate service**, transaction-mode pooling, exposed only on the VPC private network.

4. **AlloyDB migration trigger.** When does V2 (AlloyDB) kick in? Recommendation: **>5,000 active tenants OR p95 query latency on the largest tenant exceeds 500ms** — whichever comes first. Document the trigger in `data-model.md`.

---

## Done Criteria for This Dispatch

- All 12 Wave 2 SDDs polished against the standards above
- All quality gates passed per SDD
- All four open questions answered or escalated to founder
- Memory bus reseeded with the polished content
- Wave 2 status report delivered

When done: status → `Done`, comment listing artifact paths, commit SHAs, summary, and any GRO tickets recommended for filing.
