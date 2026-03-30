---
type: spec
domain: raas
status: active
created: 2026-03-19
updated: 2026-03-19
---
# PRD — Receipt-as-a-Service (RaaS) API v1.0

**Version:** 1.2.0
**Date:** March 4, 2026
**Change Log:** v1.1.0 — Jeffe decisions: Phase 1 API-key-only auth, resolution resilience + graceful degradation, dynamic call pricing, API versioning strategy. v1.2.0 — Legal questions positioned with GrowDirect thesis, L402 precedent research, Syd action items.
**Author:** ALX (Chief of Staff)
**Classification:** MAXIMUM CONFIDENTIAL
**Protocol Reference:** `elJeffe_Protocol_Spec_v1.0.md` (Sections 7, 8)
**Source Issues:** GRO-13, GRO-47, GRO-58 (GUID Namespace Amendment)
**Gate:** Tom (API architecture), Jim (test plan), Syd (regulatory)

---

## 1. Problem Statement

There is no universal, POS-agnostic API for verifying retail receipt authenticity. When an insurer needs to verify a claim receipt, an auditor needs to confirm transaction history, or a regulator needs an evidence chain — they must trust the merchant's database. There is no independent, mathematically verifiable proof. Each POS system (Square, Clover, Toast) has its own API, its own data format, and its own trust model. No single endpoint says: "This receipt is real, and here's the Bitcoin proof."

This affects insurers (fraudulent claim detection), auditors (compliance verification), regulators (evidence chain), POS integrators (cross-platform verification), and franchise operators (multi-location consistency). Without RaaS, each of these consumers builds a bespoke integration to each POS — or they trust paper receipts.

**GUID namespace model (Jeffe directive, March 3, 2026):** RaaS accepts both pseudonymous GUIDs (the permanent L1 identity) and human-readable aliases (the L2 convenience layer). All verification is ultimately resolved to the GUID — the alias is a lookup shortcut. This means external consumers never need to know a merchant's real name to verify their receipts; they can use the GUID directly. The privacy wall is preserved end-to-end: Bitcoin stores GUIDs and Merkle roots, never merchant identity.

**Business impact of not solving:** Canary LP remains a single-POS subscription product with linear revenue. RaaS transforms it into a protocol-level service with network-effect revenue (every verification call compounds Metcalfe value) and recurring per-call income that survives merchant churn.

---

## 2. Goals

### User Goals
- **G-1:** Any party can verify any receipt's authenticity with a single API call, regardless of which POS generated it. The caller can identify the merchant by GUID (permanent) or alias (human-readable).
- **G-2:** Verification response includes cryptographic proof (Bitcoin block height, Merkle path, inscription ID) — not just "true/false."
- **G-3:** Namespace resolution is public and free — anyone can check if a merchant exists in the .jeffe registry by alias or GUID without paying.

### Business Goals
- **G-4:** Establish per-verification revenue stream via dynamic pricing that scales with call complexity — lightweight gateway checks cost less than full data retrieval or high-insight responses. Revenue is independent of merchant subscription count.
- **G-5:** Achieve 1,000 daily API calls within 90 days of launch with first external integrator.
- **G-6:** Demonstrate to investors that RaaS revenue model works before Series A — verified call volume + unit economics.

---

## 3. Non-Goals

- **NG-1: Raw transaction data retrieval.** RaaS verifies receipts; it does not return line-item detail, customer names, or payment methods. Privacy by design.
- **NG-2: Real-time streaming.** v1 is request/response. Webhook push or streaming subscriptions are Phase 2.
- **NG-3: Multi-POS write path.** RaaS is read-only verification. Ingesting events from non-Square POS systems requires separate POS adapters (GRO-27 pattern), not a RaaS feature.
- **NG-4: Client SDK or libraries.** v1 is raw HTTP + JSON. Language-specific SDKs are a nice-to-have after the API stabilizes.
- **NG-5: Self-service API key provisioning.** v1 API keys are manually issued. Self-service developer portal is Phase 2.
- **NG-6: Alias management via RaaS.** RaaS is read-only. Alias creation/deletion is a Canary dashboard function, not a RaaS endpoint.

---

## 4. User Stories

### External Integrator (POS vendor, auditor, insurer)

- **US-1:** As an insurance claims analyst, I want to verify a receipt hash against the Bitcoin record using either the merchant's GUID or their human-readable alias so that I can confirm the transaction is authentic before approving a claim.
- **US-2:** As a POS integrator, I want to query a merchant's receipt history by GUID for a date range so that I can cross-reference against my own records without needing to know the merchant's alias.
- **US-3:** As a compliance auditor, I want to verify that a merchant's namespace GUID is active and has been consistently inscribing receipts so that I can assess their verification coverage.
- **US-4:** As an API consumer, I want to receive a 402 Payment Required with a Lightning invoice so that I can programmatically pay and receive the verification result in one flow.
- **US-5:** As a developer, I want the resolve endpoint to accept either a GUID or an alias and return the same canonical response so that I don't need separate code paths for each identifier type.

### Merchant (Canary LP subscriber)

- **US-6:** As a merchant, I want external parties to be able to verify my receipts through RaaS using my GUID or any of my aliases so that my insurance premiums reflect my verified transaction history.
- **US-7:** As a merchant, I want to see how many verification calls have been made against my namespace GUID so that I understand the value of my .jeffe registration.

### Developer (Internal / GrowDirect)

- **US-8:** As a developer integrating with RaaS, I want clear error responses with machine-readable codes so that I can handle edge cases programmatically.
- **US-9:** As an operations engineer, I want rate limiting to protect the API from abuse so that paying customers get consistent response times.

---

## 5. Requirements

### Must-Have (P0)

| ID | Requirement | Acceptance Criteria |
|----|-------------|-------------------|
| **R-1** | `POST /v1/verify` accepts `event_hash` + `identifier` (GUID or alias), returns verification result with Bitcoin proof | Given a valid event_hash and an identifier (UUID v4 GUID or human-readable alias), when the caller is authenticated (API key in Phase 1; L402 when Lightning infra is live), then: (a) if identifier is a GUID, verify directly against L1; (b) if identifier is an alias, resolve alias → GUID via L2/L3, then verify against L1. Response includes `verified: true/false`, `block`, `inscription_id`, `merkle_position`, and `namespace_guid` (always the canonical GUID, regardless of which identifier was used). |
| **R-2** | `GET /v1/resolve/{identifier}` accepts GUID or alias, returns namespace status (public, no payment required) | Given any identifier string, when a GET request is made (no auth required), then: (a) if identifier matches UUID v4 format, treat as GUID and verify directly; (b) otherwise, treat as alias and resolve via L2 `NameRegistry` → GUID. Response includes `registered: true/false`, `namespace_guid`, `tier`, `receipt_count`, `last_receipt`, and `identifier_type: "guid" | "alias"`. |
| **R-3** | Phase 1: API-key authentication on all paid endpoints. L402 payment gate deferred to post-UAT sign-off. | **Phase 1 (current):** All paid endpoints (`/v1/verify`, `/v1/receipt`) require a valid API key via `Authorization: Bearer <key>` header. No Lightning dependency. API keys are manually issued. **Phase 2 (post-UAT):** L402 payment gate replaces API-key auth on paid endpoints. Given an unauthenticated request, a 402 response is returned with a Lightning invoice. Given the invoice is paid, the response is served via macaroon + preimage. **Transition plan:** L402 implementation is replanned after full UAT sign-off. API key auth remains available as a fallback for consumers that cannot use Lightning. |
| **R-3a** | Dynamic call pricing — cost scales with call complexity and response payload | Call pricing is tiered by endpoint and response complexity: (a) **Gateway check** (e.g., `/v1/resolve`) — free, no payment required; (b) **Standard verification** (`/v1/verify` single hash) — base rate; (c) **Data retrieval** (`/v1/receipt` with pagination, `/v1/verify/batch`) — higher rate reflecting payload size and compute; (d) **Insight endpoints** (future: analytics, risk scoring) — premium rate reflecting data value. Pricing tiers are defined in a `pricing_schedule` config, not hardcoded. L402 invoices (Phase 2) dynamically generate amounts based on the pricing schedule. In Phase 1, pricing tiers are tracked in usage analytics for future billing but not enforced (API-key auth, metered but free during beta). |
| **R-4** | Two-path namespace resolution with L3 cache, L2 timeout, and graceful degradation | Given a GUID identifier, when resolution is attempted, then: L3 `namespace_registrations` cache returns `merchant_id` directly (< 1ms warm). Given an alias identifier, when resolution is attempted, then: L3 `namespace_aliases` cache resolves `alias → namespace_guid`, then L3 `namespace_registrations` resolves `GUID → merchant_id` (< 2ms warm, two-hop). L2 `NameRegistry` is the fallback for cache misses on alias resolution. **Resilience requirements:** (a) L2 NameRegistry fallback has a hard timeout of 2,000ms. If L2 exceeds timeout, the request fails with `503 Service Unavailable` and `error_code: "resolution_timeout"`, `Retry-After` header, and `degraded: true` flag. (b) Resolution health is continuously monitored — if L2 error rate exceeds 5% over a 60-second window, a circuit breaker trips and alias-path resolution returns `503` immediately with `error_code: "resolution_circuit_open"` until health recovers. (c) GUID-path resolution is unaffected by L2 outages — it never touches Avalanche. (d) All resolution failures emit structured health warnings to the monitoring pipeline (`/devops/monitor`) with severity, latency, and error classification. (e) No partial or stale data is returned — if resolution cannot complete, the entire request rolls back and the caller gets a clean error with instructions to retry. |
| **R-5** | Rate limiting: 1,000 req/min per API key, burst 100 req/10sec | Given a caller exceeding the rate limit, when the next request arrives, then a 429 Too Many Requests response is returned with `Retry-After` header |
| **R-6** | Error responses with machine-readable error codes | Given any error condition, when the API returns a non-2xx response, then the body includes `error_code` (string enum), `message` (human-readable), and `detail` (optional context). Error codes include `namespace_not_found`, `alias_not_found`, `guid_not_found`, `namespace_expired`, `invalid_identifier`, `invalid_hash`, `payment_required`, `rate_limited`, `resolution_timeout`, `resolution_circuit_open`. |
| **R-7** | `/v1/docs` serves OpenAPI 3.0 specification with versioning metadata | Given any unauthenticated request to /v1/docs, then a valid OpenAPI 3.0 spec is returned describing all endpoints, schemas, error codes, the GUID/alias identifier model, dynamic pricing tiers, and API version lifecycle (current, deprecated, sunset). The spec is the source of truth for the external-facing Swagger documentation site and API gateway descriptions. |

### Nice-to-Have (P1)

| ID | Requirement | Acceptance Criteria |
|----|-------------|-------------------|
| **R-8** | `GET /v1/receipt/{identifier}` endpoint returns paginated receipt history | Given a valid GUID or alias and date range, when the caller pays L402, then paginated receipts with Merkle proofs are returned. The `identifier` follows the same GUID/alias auto-detection as R-2. |
| **R-9** | `include_device: true` parameter on `/v1/verify` returns device attestation when available | Given a namespace with device_attestation ON, when `include_device: true` is passed, then the response includes `device_attestation` block with `integrity`, `device_count`, and `flags` |
| **R-10** | API usage metrics visible to namespace owner | Given an authenticated merchant, when they check their dashboard, then they see total verification calls against their GUID, unique callers, and calls per day for the last 30 days |
| **R-11** | Batch verification: `POST /v1/verify/batch` for up to 100 hashes per request | Given an array of `{event_hash, identifier}` pairs, when the caller is authenticated, then verification results are returned for all hashes. Each identifier is independently resolved (mix of GUIDs and aliases allowed in one batch). Pricing is dynamic per R-3a — each hash in the batch is priced at the data-retrieval tier, and the total is the sum of individual hash costs. |

### Future Considerations (P2)

| ID | Requirement | Notes |
|----|-------------|-------|
| **R-12** | Webhook push: notify merchant when their receipts are verified | Requires event subscription model. Phase 2. |
| **R-13** | Self-service API key provisioning via developer portal | Requires identity verification and payment setup. Phase 2. |
| **R-14** | GraphQL API alongside REST | Depends on query patterns observed in v1 usage data. Phase 2. |
| **R-15** | Cross-namespace verification: verify a hash across ALL namespaces | Privacy implications — Syd must review. Phase 3. |
| **R-16** | Alias history endpoint: list all aliases ever associated with a GUID | Useful for audit trail when merchants rebrand. Phase 2. |

---

## 6. Success Metrics

### Leading Indicators (Days to Weeks)

| Metric | Target | Stretch | Measurement |
|--------|--------|---------|-------------|
| API uptime | 99.5% | 99.9% | Healthcheck endpoint + monitoring |
| p95 response time (`/v1/verify` — GUID path) | < 500ms | < 200ms | API gateway logs |
| p95 response time (`/v1/verify` — alias path) | < 600ms | < 300ms | API gateway logs (alias adds one resolution hop) |
| p95 response time (`/v1/resolve`) | < 100ms | < 50ms | API gateway logs |
| L402 payment completion rate (Phase 2) | > 90% | > 95% | Lightning node payment logs |
| Resolution health (L2 availability) | > 99% | > 99.9% | Circuit breaker + health monitor |
| Resolution p95 latency (alias L2 fallback) | < 1,500ms | < 500ms | API gateway logs (must stay under 2s hard timeout) |
| Error rate (5xx) | < 1% | < 0.1% | API gateway logs |
| L3 cache hit rate (alias resolution) | > 95% | > 99% | Cache analytics |

### Lagging Indicators (Weeks to Months)

| Metric | Target (90 days) | Stretch | Measurement |
|--------|------------------|---------|-------------|
| Daily verification calls | 1,000 | 10,000 | API analytics |
| Unique API consumers | 5 | 20 | API key registry |
| Validation revenue (daily) | Tracked (dynamic pricing, see R-3a) | — | Usage analytics × pricing schedule. Phase 1 is metered-free; Phase 2 generates Lightning revenue. |
| Namespace resolution calls (daily) | 5,000 | 50,000 | API analytics (free tier, no L402) |
| External integrator conversion | 1 paid integrator | 3 | CRM tracking |
| GUID-vs-alias usage split | Tracked | — | API analytics (understand consumer preference) |

---

## 7. Open Questions

### Blocking

| # | Question | Owner |
|---|----------|-------|
| ~~Q-1~~ | ~~L402 middleware: LND REST, CLN, or Voltage LSP?~~ **DEFERRED** — L402 replanned after UAT sign-off. Phase 1 uses API-key auth only. | Tom + Jeremy (Phase 2) |
| Q-2 | API key format and issuance process for v1 (manual) | Jeremy |
| Q-3 | CORS policy for browser-based API consumers | Jeremy |

### Non-Blocking

| # | Question | Owner |
|---|----------|-------|
| Q-4 | Should `/v1/resolve` return `inscription_id` for public consumers? (GUID inscription — not alias data) | Tom (security review) |
| ~~Q-5~~ | ~~Batch verification pricing: 1 sat per hash or 1 sat per request?~~ **RESOLVED** — Dynamic pricing per R-3a. Batch is per-hash at data-retrieval tier. Some calls are gateway checks, some are full data requests with large payloads or high-insight responses. Pricing schedule is config-driven. (Jeffe, March 4) | ✅ |
| Q-6 | Rate limit tiers: should Enterprise tier get higher limits? | Jeffe |
| Q-7 | Should alias-path verify responses include the resolved alias name in the response, or only the canonical GUID? | Tom (privacy review) |

### Legal — Positioned (March 4 Session)

All legal questions below have a **GrowDirect position** (our thesis) and a **Syd action** (what we need confirmed or challenged). None of these block technical progress — they are recorded assumptions that Syd validates when the protocol approaches GA.

| # | Question | GrowDirect Position | Syd Action |
|---|----------|-------------------|------------|
| Q-8 | Is RaaS a financial service, data service, or something else? | **Data verification service.** RaaS is a lookup. It answers "is this receipt real?" and returns the cryptographic proof. It's open to anyone with an API key — it's their data, we just make it accessible and provable. GrowDirect is not involved in the relationship between any parties that share public keys. We are a neutral verification layer, not a financial intermediary. Classification: SaaS / data-as-a-service. | Syd: confirm that the Bitcoin proof layer doesn't reclassify us. Does "cryptographic attestation" create a different regulatory category than "data lookup" in any jurisdiction? |
| Q-9 | Does dynamic pricing via Lightning (Phase 2) make GrowDirect a money transmitter? | **No.** GrowDirect is the service provider, not a transmitter. The consumer pays GrowDirect for API access — money flows one direction (consumer → GrowDirect). No custody of consumer funds, no pass-through to third parties. This is commerce, not transmission. **Production precedent:** Lightning Labs has operated Lightning Loop (L402-gated, non-custodial swap service via Aperture proxy) since 2020 without money transmitter classification. Nansen API now supports x402 pay-per-request. Lightning Labs open-sourced full agent commerce stack (Feb 2026) explicitly designed for this pattern. Braumiller Law analysis (Nov 2025) confirms no US statute singles out L402/x402 — evaluated under existing MSB frameworks based on who moves assets and how. Phase 1 uses API-key auth with no payment, so this question is deferred but needs an answer before L402 goes live. | Syd: review Lightning Loop/Aperture precedent as operating model. Confirm one-directional fee-for-service via Lightning doesn't trigger FinCEN MSB classification. Flag any state-level variations. Dynamic pricing (variable invoice amounts per R-3a) — does that change analysis vs. flat fee? |
| Q-10 | Liability for `verified: true` when underlying inscription has an error? | **The protocol cannot sustain liability here — the entire theory is flawed if we do.** RaaS returns what the Bitcoin record says. If the inscription was created with bad data, RaaS faithfully reports what's on-chain. We are a mirror, not a guarantor. The response should include a `proof_disclaimer` field: "Verification reflects on-chain record as of [timestamp]. GrowDirect attests to the accuracy of the lookup, not the accuracy of the underlying inscription." ToS caps liability at the cost of the API call. This is architecturally identical to how DNS resolvers report what's in the zone file — they're not liable for the content. | Syd: draft the ToS liability limitation language. Evaluate whether we need a "dispute a verification" process (similar to credit report disputes) to strengthen the limitation. Is the DNS resolver analogy legally defensible? |

---

## 8. Timeline

| Phase | Depends On | What Ships |
|-------|-----------|------------|
| Protocol Phase 1 (Week 2–4) | Genesis inscription | `/v1/verify` (GUID path only) against Merkle batches from Square sandbox. **API-key auth only — no L402 dependency.** Dynamic pricing metered but not enforced (free beta). |
| Protocol Phase 3 (Week 6–10) | Avalanche subnet | `/v1/resolve` public endpoint with GUID/alias auto-detection. `/v1/receipt` history. Full three-layer resolution with circuit breaker and graceful degradation. Alias path enabled on `/v1/verify`. |
| Protocol Phase 4 (Week 10–16) | First real merchant + UAT sign-off | API under real load. Performance baseline for both GUID and alias paths. **UAT sign-off gates L402 implementation.** |
| L402 Monetization (Post-UAT) | Phase 4 UAT signed off | L402 payment gate replaces API-key auth on paid endpoints. Dynamic pricing enforced. Lightning infra decision (Q-1) made and implemented. API-key fallback remains available. |
| RaaS GA | L402 QA'd | OpenAPI docs published with versioning metadata. Swagger site and external API gateway descriptions updated. First external integrator onboarded. Batch endpoint if demand warrants. |

---

## 9. Resolution Architecture (GRO-58)

```
Identifier Auto-Detection:
  Input string matches UUID v4 regex?
    → Yes: GUID path — resolve directly
    → No:  Alias path — resolve via L2/L3

GUID Path (direct):
  identifier (GUID)
    → L3: namespace_registrations[namespace_guid] → merchant_id, status, tier
    → L1: Bitcoin scan for inscription with namespace_guid → on-chain proof
    → Response: verified, block, inscription_id, merkle_position, namespace_guid

Alias Path (two-hop):
  identifier (alias)
    → L3: namespace_aliases[alias_name] → namespace_guid (cache)
    → L3: namespace_registrations[namespace_guid] → merchant_id, status, tier
    → L1: Bitcoin scan → on-chain proof
    → Response: same fields + identifier_type: "alias"
  Cache miss fallback:
    → L2: NameRegistry.resolve(alias_name) → namespace_guid
    → Populate L3 cache, then continue as above

Privacy Wall:
  API consumer sees: GUID + proof + tier + receipt_count
  API consumer never sees: merchant_id, merchant name, POS credentials
  Bitcoin sees: GUID + Merkle roots — never merchant identity
```

---

## 10. API Versioning Strategy

RaaS follows industry-standard API versioning to protect consumers from breaking changes:

**URL-path versioning:** All endpoints are prefixed with `/v{major}` (e.g., `/v1/verify`, `/v2/verify`). Major version increments indicate breaking changes — removed fields, changed response shapes, or altered authentication flows.

**Version lifecycle:**

| State | Meaning | Duration |
|-------|---------|----------|
| **Current** | Actively developed and supported. All new features land here. | Indefinite |
| **Deprecated** | Still functional but no new features. Consumers receive `Sunset` header with EOL date. `X-API-Deprecated: true` header on every response. | Minimum 6 months from deprecation announcement |
| **Sunset** | Endpoint returns `410 Gone` with migration guide URL. | Permanent after sunset date |

**Non-breaking changes** (added fields, new optional parameters, new endpoints) do NOT increment the major version. These are additive and backward-compatible.

**Swagger / OpenAPI alignment:** The `/v1/docs` OpenAPI spec includes version lifecycle metadata (`x-api-version`, `x-api-status`, `x-sunset-date`). The external-facing Swagger documentation site and API gateway descriptions are generated from this spec — they are never manually edited. Any PRD change that affects the API surface triggers an OpenAPI spec update, which flows to the Swagger site and gateway automatically.

**API gateway headers:** Every response includes `X-API-Version: v1`, `X-RateLimit-Remaining`, and (when applicable) `X-API-Deprecated` and `Sunset` headers.

---

*PRD — RaaS API v1.2.0 | March 4, 2026*
*MAXIMUM CONFIDENTIAL*
*GRO-58 GUID Namespace Amendment applied*
*v1.1.0 — Jeffe decisions: API-key Phase 1, resolution resilience, dynamic pricing, API versioning*
*v1.2.0 — Legal questions positioned with GrowDirect thesis + Syd action items. L402 precedent research documented.*
