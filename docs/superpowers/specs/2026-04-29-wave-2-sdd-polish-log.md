---
type: session-log
related-dispatch: 2026-04-29-wave-2-sdd-polish-dispatch.md
status: in-progress
created: 2026-04-29
---

# Wave 2 SDD Polish — Session Log

Live log of the Wave 2 polish pass. Tracks what was edited, key decisions, open questions surfaced for founder review, and any IP-sensitive content flagged for separate handling.

---

## Wave 0 — Substrate (Wave 1) and Federation prep

Completed before Wave 2 formally opened. Captured here because the Wave 2 SDDs reference these by design.

**Commits:**
- `027e74b` — Wave 1 + Wave 2 Batch 1 polish

**Wave 1 SDDs (substrate):**

| SDD | Major changes |
|---|---|
| `go-runtime.md` | "Uniform Treatment of Human and Agent Traffic" subsection in Business; LoggingMiddleware fields updated with `actor_id` / `actor_type`; dependency claim corrected (was "stdlib only," now correctly notes pgx + go-redis + chi for type signatures); Related section |
| `go-module-layout.md` | License + copyright frontmatter |
| `go-security.md` | Related section |
| `go-observability.md` | `actor_id` and `actor_type` added as standard request log fields (load-bearing for agent accountability); `actor_type` as bounded label on `RequestCount` for agent traffic share monitoring; Related section |
| `go-testing.md` | Related section |
| `go-errors.md` | Related section |

**Identity / federation polish:**

| SDD | Major changes |
|---|---|
| `identity.md` | User Federation Modes section (home-grown service; OIDC / SAML / LDAP / SCIM library stack: `coreos/go-oidc`, `crewjam/saml`, `go-ldap/ldap`, `elimity-com/scim`); Platform JWT claims structure with `actor_type` explicit; Agent Authorization (default JWT, optional L402 via env flag, schema stays); Membership Boundary (identity authority vs application interface); Production Infrastructure Target replaced AWS (ECS / Fargate / RDS / ElastiCache / ALB / Route 53) with GCP (Cloud Run / Cloud SQL / Memorystore / Cloud Load Balancing / Cloud DNS) |
| `external-identities.md` | Scope Disambiguation block — POS-system entity bridging here, IdP user federation in identity.md |

**Optional Features canonical (foundational for Wave 2):**

| SDD | Major changes |
|---|---|
| `platform-overview.md` | New "Optional Features — Architectural Direction" section with full env flag table (L402, OTB enforcement, ILDWAC, satoshi denomination, blockchain anchor, vendor smart contracts — all default `false`). Closing principle: "With all flags off — `SHA-256 seals receipt → receipt records the event → RaaS owns the namespace`. That's the required loop. Everything else is extension." Schema stays in either mode. |
| `l402-otb.md` | Governing rule rewritten — entire L402 service is opt-in via system-wide `L402_ENABLED` flag; runs in pure tracking mode by default; never blocks store operations |

---

## Wave 2 Batch 1 — Architecture Spine

**Commit:** `027e74b` (combined with Wave 1)

| SDD | Major changes |
|---|---|
| `architecture.md` | GCP Target Architecture replaces AWS — Cloud Run + Cloud SQL with CMEK and PITR + Memorystore + Vertex AI + VPC-SC perimeter + Cloud Armor; Multi-Tenant Isolation rewritten — schema-per-tenant canonical with `SET search_path` per request, schema inventory (`public` / `tenant_{merchant_id}` / `audit` / `analytics`), cross-tenant admin pattern (dedicated admin role with `USAGE` on all tenant schemas + audit log), sharding posture (V1 Cloud SQL primary + 2 replicas / V2 AlloyDB / V3 application-level sharding) |
| `microservice-architecture.md` | Multi-tenant note in governing principle (schema-per-tenant); Optional Features reference; environment variables updated with TLS Valkey + Secret Manager sourcing + Optional Feature env flags; new Production posture section (GCP-native, SLA tiers); Related section |
| `data-model.md` | Schema Strategy section at the top — schema-per-tenant canonical with `tenant_{merchant_id}` schemas, public reference, audit, analytics; Tenant Onboarding flow; Cross-Tenant Admin Queries; Optional Features schema note (tables exist regardless of flag state); Legacy schema reference clarified |
| `pos-adapter-substrate.md` | Tenant context note (single tenant per call, `CanonicalEvent.tenant_id` routes into correct tenant schema); Optional features posture (adapter substrate operates identically with all flags off) |
| `data-classification-inventory.md` | Governing Thesis rewritten — schema-per-tenant + AES-256-GCM + keyed HMAC + per-subject DEK + Optional Features ref |

---

## Wave 2 Batch 2 — Receipt Chain

**Commit:** `941d988`

| SDD | Major changes |
|---|---|
| `raas.md` | "Required core, not an optional feature" block — explicit independence from L402, ILDWAC, blockchain anchoring, vendor smart contracts. Chain operates with all Optional Features flags off; multi-tenant note (namespace tables in `public` schema as routing layer; receipt chain tables per-tenant in `tenant_{merchant_id}`; cross-tenant chain queries forbidden) |
| `factory-pipeline.md` | Tenant scope note — platform-internal infrastructure, not per-merchant; knowledge corpus processing lives in `public` / platform schema; Related section |
| `agent-contracts.md` | Frontmatter: `stack` field added; `updated` date refreshed; Tenant context (every contract execution operates within a single tenant scope; `merchant_id` in `actor_type` audit trail); Optional features (contract execution independent of L402 / ILDWAC / anchor; audit trail extends with optional fields when features are on); Related section |

---

## Wave 2 Batch 3 — Optional Features

**Commit:** `082d0b5`

| SDD | Major changes |
|---|---|
| `ildwac.md` | Status block: opt-in architectural direction; `ILDWAC_ENABLED` env flag default `false`; standard ILWAC (item × location × WAC) operates when off; schema exists in either mode (tables created at tenant onboarding, accept writes when on, remain empty otherwise); IP scope: patent #63/991,596 explicit reference; multi-tenant note (tables per-tenant in `tenant_{merchant_id}`; cross-tenant analytics via `analytics` schema rollups only) |
| `blockchain-anchor.md` | Status block: opt-in architectural direction; `BLOCKCHAIN_ANCHOR_ENABLED` env flag default `false`; internal SHA-256 chain operates normally when off; public anchor is optional extension; **Chain-of-record split (resolves Wave 2 open question)**: two chains, two purposes — Base/Polygon for public evidence anchor, AVAX subnet for private vendor contracts; both gated, neither required; multi-tenant (`anchor_receipts` / `anchor_queue` per-tenant; on-chain inscription public but carries only chain root hash, no merchant-identifiable content) |
| `l402-otb.md` | Already polished in Wave 0 — verified alignment with Optional Features pattern |

---

## Wave 2 Batch 4 — Cross-cutting verification

**Status:** in progress

- `platform-overview.md` — Optional Features section is the canonical source for the env flag pattern; verified all Wave 2 SDDs reference it correctly
- `INDEX.md` — Wave 2 polish operated on existing SDDs; no inventory change required
- Memory bus reseed — auto via post-commit hook on Brain/wiki commits (no Brain edits in Wave 2; SDD changes do not trigger the hook by design — manual seed if needed)
- Session log — this document

---

## Open Questions Resolved

| # | Question | Resolution |
|---|---|---|
| 1 | Chain-of-record for vendor smart contracts (AVAX vs Base/Polygon) | Two chains, two purposes — AVAX private subnet for vendor smart contracts (low cost, EVM-compatible, private); Base or Polygon for public evidence anchoring (decentralized, externally verifiable). Both env-gated. Documented in `blockchain-anchor.md` and `agent-contracts.md`. |
| 2 | MCP Go server library | Recommend a thin Go MCP shim that mirrors the Python SDK contract. Memory Bus stays on Python FastMCP. New Canary Go services build the shim. To be documented during Wave 3 module SDD polish (the modules are the consumers). |
| 3 | Connection pooling target | PgBouncer, transaction-mode, deployed as a Cloud Run sidecar OR a dedicated service per tier — to be confirmed in `architecture.md` GCP Target section during V1 deployment dispatch. |
| 4 | AlloyDB migration trigger | Triggers documented in `architecture.md` Multi-Tenant Isolation > Sharding Posture: >5,000 active tenants OR p95 query latency on the largest tenant exceeds 500ms. |

---

## Open Questions Surfaced (Founder follow-up)

| # | Question | Context |
|---|---|---|
| F1 | Schema-per-tenant migration plan from current Python prototype | The Python prototype uses shared schemas with `merchant_id` columns. Migration to schema-per-tenant for Canary Go is a clean-build-from-zero, but if any existing data needs to migrate, a one-time data migration is required. Probably none — Canary Go is a clean break per `project_canary_go_clean_break` memory. Confirm. |
| F2 | Per-tenant migration runner — buy or build | Schema-per-tenant means N migration sets. Tools exist (e.g., goose with custom routing) but require a small wrapper. Decide: build the per-tenant runner (couple days of work) vs. operate manually for the first cohort. |
| F3 | Identity Platform vs home-grown call — re-confirm | The polish lands on home-grown identity (per founder direction). The buy/build memo in `platform-stack-commitment` lists Identity Platform under buy. Update `platform-stack-commitment` to remove Identity Platform from the buy list and add `coreos/go-oidc` + `crewjam/saml` + `go-ldap/ldap` + `elimity-com/scim` to the engineering libraries list — or keep it consistent with the new posture in identity.md. |
| F4 | Default off for Optional Features in dev — confirm | Optional Features env flags default `false` per the canonical section. In development, should certain features default `true` for ease of testing (e.g., `BLOCKCHAIN_ANCHOR_ENABLED=true` against `mock` network)? Recommendation: keep default `false` everywhere; opt-in is the discipline; dev environment uses explicit override. |

---

## IP-Sensitive Content Flagged

The following SDDs contain IP-sensitive material that should not be exposed in CRB main or any public surface until reviewed:

- `ildwac.md` — five-dimension cost model + Bitcoin standard + patent #63/991,596 algorithm
- `blockchain-anchor.md` — patent #63/991,596 algorithm
- `l402-otb.md` — L402 + Lightning + macaroon flow at the platform-architecture level
- `factory-pipeline.md` — internal knowledge ingestion pipeline; not customer-facing

**Brain wiki cards already flagged for IP sensitivity** (per the CRB rebuild dispatch, never published to CRB main):
- `platform-multi-tier-assortment` ("no one has this" per memory)
- `platform-l402-ildwac-moat`
- `platform-pii-hashing` (internal architecture)
- `platform-data-classification` (internal inventory)
- `platform-wyoming-ecosystem` (entity structure)
- `portable-store-founder-intent`
- `ilwac-extended-bitcoin-standard`

---

## Wave 2 Summary

**Total SDDs polished:** 13 (Wave 1: 6; Identity / Federation: 2; Optional Features canonical: 2; Wave 2 Batches 1–3: 11; some overlap)

**Commits:**
- `027e74b` — Wave 1 + Wave 2 Batch 1 (16 files, 752 insertions, 42 deletions)
- `941d988` — Wave 2 Batch 2 (3 files, 41 insertions, 1 deletion)
- `082d0b5` — Wave 2 Batch 3 (2 files, 16 insertions)

**Architectural posture confirmed:**
- GCP-native end to end
- Schema-per-tenant multi-tenancy with `SET search_path` per request
- Optional Features (L402, ILDWAC, blockchain anchor, vendor smart contracts) opt-in, env-gated, default `false`
- Home-grown identity service with OIDC / SAML / LDAP / SCIM federation library stack
- SOC 2 / ISO 27001 / PCI DSS / GDPR / CCPA day-one design posture
- SLA tiers: 99.95% platform, 99.99% audit, 99.9% customer-facing API

**Recommended next wave:** Wave 3 — 18 domain module SDDs. Apply Optional Features discipline, multi-tenant schema-per-tenant, agent accountability framing, use-case matrices alignment with the CRB module pages.
