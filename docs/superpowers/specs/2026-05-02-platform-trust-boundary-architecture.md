# Platform Trust Boundary Architecture

**Date:** 2026-05-02
**Status:** Draft v0 — founder review pending
**Scope:** The platform-wide authentication, authorization, and network access posture across every class of caller — POS webhook senders, on-prem edge agents, retailer staff, vendor partners, and platform agents. Not the gateway-level deployment spec ([[gcp-deployment-gateway]] is that); this is the cross-system synthesis that says *which authentication mechanism applies to which caller class and why*.
**Siblings:**
- [[2026-05-02-agent-commissioning-protocol]] — agent identity and commissioning lifecycle
- [[2026-05-02-disaster-recovery-and-continuity]] — data restoration after loss
- [[gcp-deployment-gateway]] — gateway-level deployment substrate (Cloud Run + Cloud Armor + Secret Manager)
- [[ir-plan-v0.1]] — incident response (this doc is the static posture; IR is the dynamic response)
**Builds on:** [[concept-identity-layer-triad]] · [[platform-gateway-thesis]] · [[concept-substrate-discipline]]

---

## Governing Thesis

The platform's trust posture is **identity-first, network-second**. Every caller — human or machine — authenticates as an *identity*; network controls (IP allowlists, VPC scoping, Cloud Armor) are defense-in-depth, never the primary gate. The architectural reason is mechanical: our caller mix spans cloud-hosted POS systems with stable IPs, on-prem POS stations behind unpredictable retailer ISPs, retailer staff on phones in parking lots, and platform agents that authenticate to GCP via Workload Identity. No single network control covers all five. Identity-bound credentials cover all five.

This posture inherits from the [[concept-identity-layer-triad|Identity Layer Triad]]: the substrate carries the identity record once, namespace-resolvable and hash-anchored. Each caller authenticates against that record; consent contracts determine what projection of the record they may read. The trust boundary is therefore not a network perimeter — it is the set of identity-mediated contracts between callers and the substrate.

Network controls remain valuable as a *secondary* hardening layer where the sender is stable enough to make them work (Square's documented webhook IP ranges, contracted vendor partner endpoints, the gateway's Cloud Armor rate limit at 600 req/min per source IP per [[gcp-deployment-gateway]]). They are never the gate. They are the moat around the wall.

---

## Party Taxonomy — Who Is on the Other End

Every authenticated caller — human or machine — resolves to exactly one *party* in the substrate. The party model is the relational layer above the authentication mechanism: authentication answers *can this credential connect*; party resolution answers *who is this, in what role, with what standing*. The party taxonomy tracks the platform's accountability rails ([[platform-thesis]]) — every party type maps onto at least one rail, and the rail determines the substrate's permissioning, evidence-chain treatment, and consent contract semantics.

| Party type | Definition | Rail alignment | Permission model | Evidence-chain treatment |
|---|---|---|---|---|
| **Customer** | The merchant/operator who licenses the platform. The relational anchor every other party permissions against. | Operational + Financial | Owns the tenant; full read/write within tenant scope; admin-tier role grants delegate to staff identities. | Every action anchored; customer-identity binding required on writes. |
| **Vendor** | A partner selling *into* the merchant (supplier, service provider, contracted integrator). Reads merchant data under contract, not ownership. | Vendor accountability | Read scoped to contract terms; writes only to vendor-owned data classes (PO acknowledgments, shipment confirmations); never cross-merchant unless contractually permitted. | Vendor-identity binding on reads of contract-scoped data; writes anchored to vendor identity. |
| **Consumer** | An end shopper buying *from* the merchant. Lightweight identity — receipt-anchored, opt-in for deeper binding (loyalty, account, repeat purchase history). | Financial (transactional) | No platform login by default; identity is the receipt + opt-in account binding. Deeper consumer features (loyalty, returns, history) require account-grade binding under merchant consent. | Receipt anchored; consumer identity (where bound) anchored on consent grant, not on every transaction. |
| **Auditor** | An accountant, third-party verifier, or regulator-aligned party with **standing** scope to a merchant's records. Ongoing read access under contract or regulatory framework. | Evidentiary | Read-only by default; scope per audit engagement contract; cross-merchant only when the audit framework grants it (rare); standing renews per engagement period. | Every read logged to chain (auditor presence is itself an evidentiary event); writes (where permitted, e.g., audit notations) anchored as auditor-identity-bound. |
| **Investigator** | A loss-prevention investigator, insurance investigator, or law enforcement officer with **time-bounded** authority to examine records under a specific incident, claim, subpoena, or court order. | Evidentiary | Read-only; scope per authority instrument (case number, claim ID, subpoena reference); cross-tenant only under explicit authority instrument; auto-expires at the authority instrument's terminus. | Every read logged with authority instrument reference; chain entries cite the authorizing document; investigator identity bound to instrument identity. |
| **MCP Agents** | Platform-resident or external agents per the [[2026-05-02-agent-commissioning-protocol]]. The "runtime context" is the device (Cloud Run revision + runtime SA for hosted agents; Cowork session + agent identity for session-resident agents). | Cross-cutting | Per agent capability tier (T0–T4) per commissioning protocol; hard floors enforced by IAM denial. | Every action anchored to agent identity + runtime context + tier; tripwires fire on contract deviation. |

### The auditor/investigator distinction

This is the distinction that does not exist anywhere else in our docs and needs naming explicitly. Both are evidentiary parties; their permission models are different.

- **Auditor has standing scope.** A merchant's accountant has ongoing read access for tax purposes. Standing scope renews per audit engagement, has a defined permission envelope, and the auditor's identity is registered to the substrate as a long-lived party. Their access is *expected*; it is part of the merchant's normal operations.
- **Investigator has time-bounded scope.** A loss-prevention investigator on a Fox case, an insurance fraud investigator, law enforcement under a subpoena. Their access is incident-driven, bound to a specific authority instrument (case ID, claim number, court order), and auto-expires at the instrument's terminus. Their access is *exceptional*; it is the substrate acknowledging an external authority that supersedes normal operations.

Both anchor every read into the evidence chain. The difference matters because their consent contracts ([[concept-identity-layer-triad]]) are shaped differently — auditors operate under merchant-granted standing consent; investigators operate under externally-granted time-bounded authority. Cross-tenant scope is rare for auditors (a regulator examining a category of merchants is the exception); cross-tenant scope for investigators is the norm under the right authority (subpoenas, court orders, regulatory examinations).

### Multi-party authorization (where it matters)

Some actions require *multiple* party identities in the same authorization envelope. Examples:
- A vendor write to merchant data requires the vendor's identity AND a merchant-side consent contract permitting the write
- A cross-tenant investigator query requires the investigator identity AND the authority instrument's reference AND (where the framework demands) the affected merchants' notification record
- An MCP agent's escalation to the founder requires the agent identity AND the founder's confirmation through the chat interface (per the commissioning protocol's escalation discipline)

Multi-party authorization is the substrate's mechanism for high-stakes operations. The chain entry carries every contributing identity; the operation is non-repudiable for each.

---

## Device Registration & Attestation

**Every device that touches the platform is registered to exactly one party at exactly one trust level.** This is the architectural floor for non-repudiation, the basis of risk scoring, and the prerequisite for device-level revocation. Financial platforms have done this for decades; we adopt the discipline platform-wide on day one because the evidentiary rail demands it.

### Device record — substrate schema

```
device_id            UUID PRIMARY KEY            -- stable across sessions
party_type           ENUM(customer, vendor, consumer, auditor,
                          investigator, mcp-agent)
party_id             UUID NOT NULL REFERENCES <party-table>
device_fingerprint   JSONB                       -- hardware signature, OS,
                                                 -- browser, attestation
                                                 -- substrate (TPM, Secure
                                                 -- Enclave, Play Integrity,
                                                 -- Cloud Run revision ID
                                                 -- for agents)
enrollment_event     JSONB                       -- when, how, by whom,
                                                 -- with what attestation
trust_level          ENUM(provisional, verified, trusted)
last_seen            TIMESTAMPTZ
revocation_status    ENUM(active, suspended, revoked)
revocation_reason    TEXT
revocation_at        TIMESTAMPTZ
evidentiary_anchor   TEXT                        -- L2 chain hash anchored
                                                 -- at enrollment
created_at           TIMESTAMPTZ NOT NULL
updated_at           TIMESTAMPTZ NOT NULL
```

Every chain entry carries `(device_id, party_id, party_type)` as substrate-required fields. The chain query "show me every action that touched this case" returns the device and party for each action, by construction.

### Trust levels — graduation criteria

| Trust level | What it means | Default permissioning | Graduation to next |
|---|---|---|---|
| **Provisional** | Device has been seen but enrollment is incomplete. First-time browser, freshly-installed station, agent in commissioning. | Read-only or scoped-write per party type; sensitive actions require step-up auth (re-confirm credential, MFA challenge, founder approval for agents). | Verified after first complete authentication ceremony (MFA confirmation for humans, attestation success for stations, probation-period clean record for agents). |
| **Verified** | Device is enrollment-complete, attestation passes, identity is bound. | Default permissioning per party type and (for agents) capability tier. | Trusted after sustained clean operation over a defined window (90 days for human devices; per commissioning graduation for agents). |
| **Trusted** | Device has earned reduced friction. Risk scoring weights toward "this is normal." | Reduced step-up frequency for routine actions; sensitive actions still require fresh auth. | Re-verification on suspicious signals (geo anomaly, fingerprint drift, party role change). |

### Device registration ceremony — by party type

| Party | Enrollment ritual | Attestation substrate | Re-enrollment trigger |
|---|---|---|---|
| **Customer staff** (browser, mobile) | First sign-in: OIDC + MFA confirmation; device fingerprint captured; device record created with `party_id = staff identity`. Email/SMS notification to admin at enrollment. | Browser fingerprint (FingerprintJS or equivalent), WebAuthn where supported, optional TPM attestation on managed devices. | Major fingerprint drift (browser change, OS upgrade beyond threshold), 12-month silence, admin revocation. |
| **Customer station** (on-prem POS) | Edge agent installation ceremony: per-station mTLS cert OR per-station HMAC issued, device record created with attestation hash, founder/VAR confirms enrollment via dashboard. | mTLS cert chain, optional TPM/Secure Enclave attestation if station hardware supports it, station serial number. | Hardware change, cert rotation cycle, station decommission. |
| **Vendor system** (partner backend) | Per-partner enrollment via signed onboarding agreement; device record represents the partner *system*, not individual operators within it; mTLS cert + IP allowlist. | mTLS cert chain, contracted IP allowlist as attestation supplement, partner identity in OAuth client metadata. | Partner contract renewal, cert rotation, IP range change (notification + re-attestation). |
| **Consumer device** (browser/mobile, opt-in) | Lightweight: receipt fingerprint (no required enrollment); deeper enrollment opt-in via merchant-prompted account creation; device record created on opt-in only. | Browser fingerprint, optional WebAuthn for deeper account binding. | Account-binding event, fingerprint drift past threshold. |
| **Auditor / Investigator device** | Enrollment by a *party authority* — for auditors, the merchant admin enrolls the auditor; for investigators, the founder (or designated authority) enrolls under the authority instrument reference. | OIDC + MFA mandatory; device fingerprint captured; for investigators, authority instrument hash anchored alongside the device record. | Audit engagement renewal (auditors), authority instrument expiry (investigators). |
| **MCP agent device** | Per-agent commissioning per [[2026-05-02-agent-commissioning-protocol]]; "device" is the runtime context: Cloud Run revision ID + runtime SA for hosted agents, Cowork session ID + agent identity for session-resident agents. | Workload Identity Federation attestation, Cloud Run revision SHA, runtime SA email; for Cowork agents, the founder's OIDC identity + per-session memory bus credential. | Agent re-commissioning, capability tier change, runtime substrate change (image rebuild, session start). |

### Device-level revocation

A compromised station does not require revoking the entire merchant. A compromised agent does not require freezing the entire agent class. Device-level revocation is the substrate primitive that makes incident response surgical instead of catastrophic.

- **Customer admin can revoke any device registered to their tenant** via the dashboard. Revocation is immediate at the substrate; in-flight sessions are terminated within the next request cycle.
- **Founder can revoke any device platform-wide** (all party types) via an emergency revocation API. Used for compromise events, agent freeze per commissioning protocol tripwires, and incident response.
- **Authority instruments can include device revocation requirements** (e.g., a court order requiring preservation may also require revocation of read access until preservation is verified).
- **Revocation is itself an evidentiary event.** Anchored to the chain with the revoking party identity, the reason, and the timestamp. A revoked device cannot be silently un-revoked; restoration requires a new enrollment ceremony.

### Attestation substrates — the depth ladder

| Attestation depth | Substrate | When applied |
|---|---|---|
| Network-only | IP allowlist | Defense-in-depth on stable senders (Square webhooks, contracted vendors) |
| Credential-bound | OIDC token, HMAC signature | Every authenticated request |
| Browser-bound | Browser fingerprint, WebAuthn | Customer staff, consumer opt-in |
| Hardware-bound | TPM attestation, Secure Enclave, Play Integrity | Customer staff on managed devices, future hardened station deployments |
| Cert-bound | mTLS with hardware-anchored key | On-prem stations, vendor systems |
| Runtime-bound | Workload Identity Federation, Cloud Run revision SHA, runtime SA | All MCP agents on GCP |
| Authority-bound | Authority instrument hash (court order ID, case number, claim ID) | Investigator devices |

The depth ladder is *additive*. Customer staff on a managed device might present credential-bound + browser-bound + hardware-bound attestation; an investigator device under subpoena presents credential-bound + browser-bound + authority-bound. The substrate records every attestation layer; risk scoring weights them; revocation can be triggered at any layer.

---

## The Asymmetry — Why Uniform Network Policy Fails

| Caller class | What we know about their network | Why uniform IP allowlist fails | Right primary control |
|---|---|---|---|
| Square webhooks | Documented, stable IP ranges published by Square | n/a — works here | HMAC-signed payload (per-merchant secret in Secret Manager) + IP allowlist as defense-in-depth |
| NCR Counterpoint stations (on-prem) | Egress IP is whatever the store's ISP hands out — cable, cellular failover, occasional dynamic | Store IPs change without notice; cellular failover lands on completely different ranges; merchants do not control their NAT egress | mTLS with per-station certificate, OR HMAC-signed payload with per-station secret, issued at edge agent provisioning |
| RapidPOS stations / future on-prem POS | Same as Counterpoint | Same | Same — per-station mTLS or per-station HMAC |
| Edge Agent (our install at the retailer) | Authenticates outbound from inside their NAT to our endpoint | Their IP is variable and irrelevant — connection is initiated from inside their firewall | Workload Identity Federation (preferred) or per-tenant service account credential |
| Retailer staff dashboard access | Phones in parking lots, tablets at vendor meetings, home laptops at 11pm | Locking to store IP defeats the product; the retailer wears every hat across every location | Identity Platform multi-tenant + magic link / SSO + MFA |
| Vendor partner APIs (Bull/NCR, future contracted partners) | Stable, contracted IP from a partner data center | n/a — works here | mTLS (preferred) + IP allowlist + per-partner OAuth/JWT |
| Platform agents (per [[2026-05-02-agent-commissioning-protocol]]) | GCP-resident or Cowork/Claude Code session | Mixed surface; some on Cloud Run, some on developer workstations | Workload Identity Federation per agent identity; capability tier dictates surface |

The mental model: **humans get identity-anywhere, machines get identity-with-network-hardening-where-feasible.**

---

## Authentication Mechanisms Inventory

The platform standardizes on five authentication mechanisms across the caller classes. Each is bound to an identity, not a network location. No mechanism stands alone — every active gate is mechanism + audit log + revocation path.

### 1. Workload Identity Federation (machine → GCP)

Used for every machine identity that needs GCP resources without holding a credential file. Edge agents at retailer sites, platform agents on Cloud Run, CI builders, sub-services calling each other across Cloud Run. Per [[gcp-deployment-gateway]] §IAM model, key creation is blocked at the org level (`iam.disableServiceAccountKeyCreation`) — Workload Identity is the only sanctioned path.

Per-identity service account, role-scoped (no broad project-wide grants except where explicitly justified), Workload Identity binding to the runtime context. The runtime SA on the gateway today (`canary-gateway-rt@`) has narrow roles: `cloudsql.client`, `secretmanager.secretAccessor` scoped to `canary-source-*` and `canary-gateway-*`, `logging.logWriter`, `monitoring.metricWriter`, `cloudtrace.agent`, `redis.editor`. The same scoping discipline applies to every new runtime SA.

### 2. mTLS (machine → machine, identity-bound)

Used when a machine caller's network position is variable and we need to authenticate the *machine itself*. On-prem POS stations talking to the gateway, contracted vendor partner endpoints, future cross-cloud federation.

Certificate issuance is a *commissioning event* — the cert is the identity. Per-station, per-partner, per-machine. Revocation is operational (CRL or short-lived certs with automated renewal); a compromised station's cert is revoked, not the entire merchant's access. Cert rotation cadence: TBD per Open Question 3.

### 3. HMAC-signed payloads (sender → ingress endpoint)

Used at every webhook ingress where the sender authenticates the *payload* rather than the channel. Square webhooks (per-merchant HMAC), Counterpoint station events (per-station HMAC, fallback when mTLS is operationally heavier than warranted), generic third-party event sources.

The per-merchant HMAC keys live in Secret Manager under the `canary-source-*` naming convention established by GRO-687. Key rotation is operational (rotate without downtime via overlapping key validity windows); compromise revocation is per-merchant, never platform-wide. The HMAC signature plus a payload-bound timestamp and nonce defends against replay.

### 4. OIDC / OAuth 2.0 (human → platform surface)

Used for every retailer staff identity. Identity Platform multi-tenant per merchant; SSO into the merchant's existing identity provider (Google Workspace, Microsoft 365, Okta) where the merchant has one; magic-link fallback where they don't. MFA required at first admin enrollment; recommended at staff enrollment; enforced at admin-tier role grants.

The retailer's identity is *theirs*, not ours. We never issue platform-side passwords to retailer staff. The OIDC subject claim is the substrate identity binding; consent contracts ([[concept-identity-layer-triad]] §Consent) determine what projection of the merchant's data each authenticated user may read.

### 5. Per-tenant API tokens (programmatic access by retailer)

Used when a retailer's own systems need to call our API (e.g., custom reports, in-house dashboards, third-party tools the retailer authorizes). Token issued via the dashboard by an authenticated admin; token scoped to a specific projection (read-only by default, write requires explicit role); token expiration mandatory (max 90 days, rotation enforced at issuance).

Tokens are bound to the merchant identity *and* to the issuing admin. Revocation is one-click in the dashboard. Tokens never grant cross-tenant access — the substrate's tenant isolation (next section) holds even if a token leaks.

---

## Tenant Isolation Strategy

The platform is multi-tenant from day one. Tenant isolation is a substrate-layer guarantee, not a per-query reminder.

### The recommendation: PostgreSQL Row-Level Security (RLS) with rigorously enforced `tenant_id`

Every tenant-scoped table carries `tenant_id UUID NOT NULL`. RLS policies enforce `tenant_id = current_setting('app.current_tenant_id')::uuid` on every row. The application sets `app.current_tenant_id` once per request, derived from the authenticated identity claim, and the database enforces the rest. A query that forgets a `WHERE tenant_id = ?` clause cannot leak across tenants because the database itself rejects the rows.

This is the operationally simpler choice than schema-per-tenant for our scale and trajectory. Schema-per-tenant adds operational surface (per-tenant migrations, per-tenant connection pools, per-tenant backup discipline) for a hardness improvement that RLS provides at the database layer. RLS is the GCP-friendly choice; Cloud SQL Postgres 17 supports it natively without extension.

### The hard rules

1. Every tenant-scoped table has `tenant_id UUID NOT NULL` *and* an RLS policy. No exceptions. Tables that are explicitly platform-global (e.g., schema versions, ARTS POSLOG reference data) are documented as such and audited.
2. The application sets `app.current_tenant_id` from the authenticated identity claim on every connection checkout. This is a middleware-level concern, not a per-handler concern.
3. The runtime SA's database role does not have `BYPASSRLS`. The only role that does is the migration role, used at deploy time, never at runtime.
4. Tests fail closed: any integration test that queries without setting `app.current_tenant_id` errors out. The CI pipeline catches missing `tenant_id` in new tables via a static check on migrations.
5. Cross-tenant data reads are an architectural event, not a query parameter. They require explicit consent contracts ([[concept-identity-layer-triad]] §Consent) and produce evidence chain entries. There is no "admin override" that quietly reads across tenants.

### Consent-bounded cross-projection

Per the Identity Layer Triad, an operator may authorize their own substrate identity to project across legs (e.g., a clinic owner who is also a retail operator authorizes the retail module to read their health-leg identity). This is a *consent contract* in the substrate, signed and evidenced. It is not a tenant isolation bypass — both projections still enforce RLS against their respective tenant scopes; the consent is what permits the join.

---

## Network Controls — Defense in Depth

Network controls are the moat, not the wall. Applied where they earn their keep without becoming the gate.

| Control | Where applied | Why |
|---|---|---|
| Cloud Armor rate limit (600 req/min/source IP, 5min ban) | Gateway ingress per [[gcp-deployment-gateway]] | Webhook flood mitigation; abuse defense |
| Cloud Armor OWASP CRS pre-configured rules | Gateway ingress | XSS/SQLi pattern blocking; baseline web hygiene |
| Cloud Armor IP allowlist | Square webhook endpoint specifically (where source IPs are documented) | Defense-in-depth on top of HMAC; stops trivial spoofing |
| VPC Service Controls | Cloud SQL, Memorystore, Secret Manager | Private-IP-only; no public surface for data stores |
| VPC connector | Cloud Run → private services | Egress through controlled connector, not public internet |
| Per-tenant rate limit (in-application) | All authenticated endpoints | Per-tenant budget on requests/sec; protects against runaway client or compromised token |
| TLS 1.3 minimum | All public ingress | No legacy cipher acceptance; Google-managed certs |
| mTLS at the application layer | Vendor partner endpoints, on-prem station authentication | Identity-bound, not network-bound |
| Service-to-service auth | Inter-service calls within VPC | Cloud Run service-to-service auth via OIDC tokens — no implicit trust on the private network |

Network controls do **not** replace identity. A request that passes Cloud Armor and the IP allowlist still must present a valid HMAC, OIDC token, or mTLS cert. A request that fails the identity check is rejected regardless of where it came from.

---

## Encryption Posture

| Layer | Default | Hardening path |
|---|---|---|
| In transit (public) | TLS 1.3 via Cloud Load Balancer + Google-managed cert | Customer-managed cert at Phase 2 if a partner contract demands |
| In transit (internal, Cloud Run → Cloud SQL) | TLS via Cloud SQL Auth Proxy | mTLS extension at Phase 2 |
| At rest (Cloud SQL) | Google-managed encryption keys (GMEK), AES-256 | CMEK via Cloud KMS at Phase 2; required if a regulated customer demands key custody |
| At rest (Cloud Storage — evidence chain anchors) | GMEK, AES-256, Object Versioning enabled | CMEK + Object Lock for evidentiary tier (worth scoping as its own SDD per Open Question 5) |
| At rest (Secret Manager) | KMS-backed | Already CMEK-equivalent |
| At rest (Memorystore) | GMEK | CMEK option available; not yet required |

**The CMEK decision threshold:** when a single customer or regulatory regime demands key custody (likely the SMB Health vertical per [[vertical-smb-health-hypothesis]] under HIPAA), the platform graduates to CMEK across the relevant data tiers. CMEK is operationally heavier (rotation ceremony, KMS IAM, restore complications under key loss), so we don't pre-pay the cost.

---

## Per-Tenant Secret Management

Secrets are scoped to identities, never shared across tenants. The naming and IAM patterns established by [[gcp-deployment-gateway]] §Secrets and GRO-687 are the canonical pattern.

| Secret class | Naming pattern | IAM scope | Rotation cadence |
|---|---|---|---|
| Per-merchant HMAC source secret | `canary-source-<merchant_id>` | Runtime SA, condition-scoped | Operational rotation via overlapping key windows; mandatory rotation on suspected compromise |
| Per-station credential (mTLS or HMAC) | `canary-station-<station_id>` | Runtime SA, condition-scoped | At edge agent re-provisioning; revocation on station decommission |
| Per-tenant API token (issued by retailer admin) | Stored in Cloud SQL with per-tenant encryption envelope; never in Secret Manager | n/a (not a Secret Manager record) | Max 90-day expiration enforced at issuance |
| Service-to-service auth secrets | `canary-internal-<purpose>` | Per-service runtime SA | Quarterly minimum; on personnel change |
| Database connection credentials | `canary-gateway-database-<role>` | Runtime SA per role | Quarterly; on personnel change |
| Vendor partner OAuth client secrets | `canary-partner-<partner>-<purpose>` | Per-partner-integration runtime SA | Per partner contract terms |

**Key creation prohibition holds.** Service account JSON keys are blocked at the org level. All auth flows use Workload Identity Federation or the IAM token endpoint. The gateway SDD documents this; it applies platform-wide.

---

## Agent-to-Platform Authentication

Platform agents (per [[2026-05-02-agent-commissioning-protocol]]) authenticate as identities subject to their commissioned tier. The commissioning protocol defines *who they are and what they may do*; this section defines *how they prove it to the platform*.

| Agent runtime | Authentication | Tier-keyed scope |
|---|---|---|
| Cloud Run-resident agent (e.g., Auditor as Vertex AI service) | Workload Identity Federation, per-agent runtime SA | Tier-defined IAM role grants per agent card |
| Cloud Build-triggered agent (CI-time review, post-commit hook) | Cloud Build SA → impersonate per-agent runtime SA | Read-only by default (Tier T0 commissioning baseline) |
| Cowork / Claude Code session-resident agent (e.g., ALX) | Founder OIDC identity + per-session memory bus credential | Inherits founder privileges in current state; will graduate to per-agent identity at Controller v1 |
| External MCP server (third-party) | OAuth 2.0 to the MCP provider; per-MCP allowlist in `.mcp.json`; never embedded credentials | MCP allowlist is the gate; credentials scoped per MCP provider's docs |
| Vertex AI inference call (synchronous) | Cloud Run SA → Vertex AI; no separate credential | Caller's tier governs what the inference is allowed to do with the result, not the call itself |

The commissioning protocol's hard floors (no IAM modification, no secret rotation, no money movement, no permanent deletes, no security policy changes — at every tier including T4) are enforced by IAM denial, not by agent compliance. If an agent's runtime SA does not have the role, the action is rejected at the GCP layer. Trust the IAM, not the prompt.

---

## Open Questions

These are the choices I cannot make for you. v1 of this doc resolves them.

1. **mTLS vs HMAC for on-prem station authentication — operational vs hardness tradeoff.** mTLS is the harder primitive; HMAC is operationally lighter. For the first VAR rollout (RapidPOS / Counterpoint stations), the operational reality is that VARs install agents on stations they don't centrally manage. HMAC with per-station secrets in Secret Manager is the v0 default; mTLS is a Phase 2 hardening once the VAR commissioning ritual is mature enough to handle cert distribution. Founder confirmation requested.
2. **Identity Platform IdP provisioning — do we lead with Google Workspace SSO, or magic-link first?** Both work. Magic-link is friction-free for the smallest merchants who don't have an IdP. SSO is the defensible answer for any merchant with employees beyond the owner. Recommend: ship both, default magic-link, surface "connect your IdP" prominently in the dashboard onboarding.
3. **mTLS certificate lifecycle — rotation cadence and renewal substrate.** Short-lived certs (e.g., 30-day) with automated renewal via SPIFFE/SPIRE-style attestation is the modern pattern; long-lived certs (1-2 year) with manual rotation is the operationally simpler v0. Recommend: long-lived for v0 with documented manual rotation, graduate to short-lived at the SMB Health vertical or once we have >50 stations.
4. **Cross-tenant consent contract substrate — where does the contract live?** Per the Identity Layer Triad, consent is a substrate-layer record. The mechanical question is whether that record lives in Cloud SQL with the rest of the substrate data, in Secret Manager (because it gates access), or in a dedicated consent service. Recommend: Cloud SQL with hash-chain anchoring per the evidentiary rail. Worth a dedicated SDD before HIPAA rolls in.
5. **CMEK threshold — when do we graduate from Google-managed to customer-managed keys?** Triggered by the first customer or regulatory regime that demands it. SMB Health vertical under HIPAA is the most likely first trigger. Worth pre-scoping the migration runbook so we can promise a 30-day cutover when asked.
6. **Cloud Armor IP allowlist for Square webhooks — automated sync against Square's published IP ranges, or quarterly manual update?** Square publishes their webhook IP ranges; they update them. Manual quarterly updates risk an outage; automated sync risks accepting a hijacked range if Square's documentation is compromised. Recommend: automated sync with a 24h staging window where a new range is logged but not yet allowlisted, surfacing in the dashboard for founder approval.
7. **Per-tenant rate limit defaults — where do they live and how does a merchant negotiate them?** Defaults in code (e.g., 100 req/sec/tenant) with per-tenant override in the merchant config table. Worth surfacing in the dashboard so the merchant sees their consumption against the limit. Recommend: starting limits are a sales/onboarding conversation; runtime override is a self-service dashboard control.
8. **Device fingerprinting substrate — FingerprintJS Pro, open-source FingerprintJS, custom WebAuthn-only, or none for v0?** Browser fingerprinting is operationally and ethically loaded. FingerprintJS Pro is the commercial standard; open-source is a credible v0 substrate with reduced accuracy; custom WebAuthn-only avoids the fingerprint-as-tracking concern entirely but loses risk-scoring fidelity. Recommend: open-source FingerprintJS for v0, document the privacy posture explicitly, graduate to commercial substrate when risk-scoring fidelity becomes a sales conversation.
9. **Hardware attestation requirement threshold — when do we require TPM / Secure Enclave / Play Integrity?** Currently optional everywhere. Worth becoming required for SMB Health vertical (HIPAA pressure on identity assurance) and for any customer admin role granting cross-tenant visibility (auditor-merchant binding, investigator authorization). Recommend: required for SMB Health and admin-tier role grants; optional elsewhere.
10. **Authority instrument verification for investigator devices — how does the substrate confirm a court order or subpoena is real?** v0 default: founder verifies and registers the authority instrument; substrate trusts the founder's verification. Phase 2: integration with court-order verification services (where available); cryptographic verification of authority instruments via signed government APIs (where they exist). Recommend: v0 founder-mediated; document the founder's verification ritual (call the court clerk, verify the docket); plan Phase 2 once the volume warrants automation.
11. **Trust level graduation timing — 90 days proposed for human devices; right number?** Financial platforms often use 30 days for trusted-device promotion. 90 days is conservative. Recommend: 30 days for routine actions, 90 days for sensitive actions; tunable per-tenant via the rate-limit / risk-tolerance dashboard.
12. **Consumer device opt-in framing — how do we present deeper consumer device binding without privacy alarm?** The opt-in is for consumer features (loyalty, returns, history) under merchant consent. Framing matters — "we recognize this device for your loyalty rewards" vs "we are tracking your device" lands very differently. Recommend: merchant-customizable opt-in copy with a platform-default that emphasizes consumer benefit and consumer control (one-click forget-this-device).
13. **Cross-tenant authority for investigators — substrate-level enforcement?** When an investigator presents a multi-tenant authority instrument (e.g., a regulator examining all merchants in a category), the substrate needs to enforce the scope of the instrument. Recommend: authority instrument carries explicit tenant list; substrate validates per-query that the queried tenant is in the list; chain entry per query cites the instrument.

---

## Related

- [[concept-identity-layer-triad]] — substrate identity model and consent contract architecture
- [[platform-gateway-thesis]] — the gateway substrate this trust posture lives within
- [[concept-substrate-discipline]] — fractal rule for what lives in substrate vs modules
- [[gcp-deployment-gateway]] — gateway-level deployment substrate (Cloud Run, Cloud Armor, Secret Manager, IAM)
- [[secrets-manager-integration]] — per-merchant HMAC secrets lifecycle (GRO-687)
- [[2026-05-02-agent-commissioning-protocol]] — agent identity and capability tier model
- [[2026-05-02-disaster-recovery-and-continuity]] — sibling SDD for data restoration
- [[ir-plan-v0.1]] — incident response (this doc is the static posture; IR is the dynamic response)
- [[docs/team/Security|Security operational profile]] — the platform agent that owns trust boundary policy
- [[platform-thesis]] — three accountability rails plus vendor accountability
