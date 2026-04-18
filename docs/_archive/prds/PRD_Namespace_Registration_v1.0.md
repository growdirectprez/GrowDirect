---
type: spec
domain: raas
status: active
created: 2026-03-19
updated: 2026-03-19
---
# PRD — .jeffe Namespace Registration v1.0

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.4.0
**Date:** March 4, 2026
**Change Log:** v1.1.0 — GUID permanence, revocation cost model, cross-PRD interface contract. v1.2.0 — No alias reservation, GUID-only pre-minting, anti-speculation gate. v1.3.0 — Customer offboarding flow, DAO multi-sig key strategy, lifecycle expansion. v1.4.0 — Legal questions positioned with GrowDirect thesis, "exit not transfer" model for Q-11, Syd action items.
**Author:** ALX (Chief of Staff)
**Classification:** MAXIMUM CONFIDENTIAL
**Protocol Reference:** `elJeffe_Protocol_Spec_v1.0.md` (Sections 3.3, 5, 6)
**Source Issues:** GRO-13 (Decisions 1–6), GRO-46, GRO-47, GRO-58 (GUID Namespace Amendment)
**Gate:** Tom (NameRegistry contract), Syd (legal + privacy), Art (merchant UX), Jim (QA)

---

## 1. Problem Statement

Merchants who use Canary LP have no portable, verifiable identity across POS systems, insurers, auditors, or regulators. Their identity is locked to whichever POS platform they use — a Square merchant ID means nothing to a Clover integrator, an insurer, or a compliance auditor. When a merchant switches POS systems, their verification history doesn't follow them.

The .jeffe namespace gives merchants a permanent, Bitcoin-anchored identity that works across all POS platforms, all verification consumers, and all future contexts. It's the domain name for commerce — except the registration is inscribed on Bitcoin, not stored in a registrar database.

**Privacy by design (Jeffe directive, March 3, 2026):** The on-chain identity is a pseudonymous GUID — no human-readable merchant name exists on Bitcoin. Human-readable aliases (e.g., `sunrise-coffee.jeffe`) live exclusively on L2 (Avalanche NameRegistry). This creates an anonymity wall: on-chain data reveals event counts and Merkle roots, never merchant identity. The GUID wall is the commercial moat — anonymized retail sales data from a market with zero existing visibility.

**Who experiences this:** Every merchant using Canary LP (starting with Square, expanding to Clover/Toast). Every external party that needs to look up or verify a merchant's identity.

**Cost of not solving:** Without namespace registration, the RaaS API has no merchant identity layer. Verification requests must use POS-specific merchant IDs, defeating the POS-agnostic design. The "modern wax seal" story collapses — there's no seal without an identity behind it.

---

## 2. Goals

### User Goals
- **G-1:** A merchant can register a .jeffe namespace that permanently identifies them across all POS systems and verification contexts. Registration creates a pseudonymous GUID on Bitcoin (L1) and one or more human-readable aliases on Avalanche (L2).
- **G-2:** A merchant can see their namespace status, receipt count, and verification activity in the Canary dashboard — including their GUID, active aliases, and alias management.
- **G-3:** Any party can resolve a .jeffe alias to confirm the merchant exists and is active, without paying. GUID verification is also public.

### Business Goals
- **G-4:** Establish namespace as a recurring revenue stream (annual registration fee).
- **G-5:** Register 50 namespaces within 90 days of launch (includes pre-registered reserved GUIDs with reserved alias names).
- **G-6:** Create switching cost: merchants who build verification history under their .jeffe GUID are less likely to churn. The GUID is permanent; aliases can change.
- **G-7:** Pre-mint GUID pool for Fortune 500 and top 100 merchant categories — pseudonymous GUIDs only, no alias reservation. When enterprise prospects engage, their identity is already anchored on L1 and ready for alias assignment. Value comes from the closed-loop economy, not speculative namespace hoarding.

---

## 3. Non-Goals

- **NG-1: Self-service registration portal.** v1 registration is merchant-requests-via-Canary, ALX/admin provisions. Self-service portal is Phase 2.
- **NG-2: Namespace transfer or resale.** Non-transferable through Phase 2 (GRO-13 Decision 4). Transfer logic exists in contract but is admin-gated.
- **NG-3: Multi-level subdomains.** One level only at launch: `store-42.walmart.jeffe`. No `dept.store-42.walmart.jeffe`. (GRO-13 Decision 2).
- **NG-4: Custom namespace roots.** `.jeffe` only. No `.canary`, `.growdirect`, or custom TLDs.
- **NG-5: Secondary registrars.** GrowDirect is the sole registrar through Phase 2 (GRO-13 Decision 5).
- **NG-6: Burner endpoint minting.** Burner.jeffe is a separate product with its own PRD (Phase 2).

---

## 4. User Stories

### Merchant

- **US-1:** As a Canary LP merchant, I want to register a .jeffe namespace for my business so that insurers, auditors, and customers can verify my receipts using a human-readable alias or my permanent GUID.
- **US-2:** As a merchant, I want to see my namespace status (active, expires on, GUID, aliases, receipt count) in my Canary dashboard so that I know my verification identity is current.
- **US-3:** As a merchant, I want to renew my .jeffe namespace annually so that I maintain my verification history and public identity.
- **US-4:** As a merchant who didn't renew, I want a 30-day grace period before my namespace is suspended so that a billing mistake doesn't destroy my verification identity. My GUID and historical receipts are preserved regardless — only my aliases stop resolving.
- **US-5:** As a multi-location merchant, I want to register subdomain aliases for each location (`downtown.sunrise-coffee.jeffe`, `airport.sunrise-coffee.jeffe`) so that verification is location-specific.
- **US-6:** As a merchant, I want to manage my human-readable aliases (add new ones, remove old ones) without changing my on-chain GUID so that I can rebrand without losing verification history.

### Merchant Offboarding (Deactivation / Churn)

- **US-12:** As a merchant who is closing my business, I want to voluntarily deactivate my namespace so that my aliases stop resolving, but my historical receipts remain verifiable under my GUID for any outstanding insurance claims, audits, or legal holds.
- **US-13:** As a merchant who is switching POS systems (e.g., Square → Clover), I want my .jeffe namespace to survive the switch so that my verification identity is POS-agnostic and my history is unbroken. (This is the core value proposition of the GUID.)
- **US-14:** As a merchant whose subscription lapsed, I want to understand exactly what happens next — what stops working immediately, what continues during grace period, and what happens after grace period expires — so that I can make an informed decision about renewing.
- **US-15:** As a merchant who was suspended for a dispute, I want a clear appeals process so that a false report doesn't permanently damage my verification identity.

### GrowDirect Admin — Offboarding

- **US-16:** As a GrowDirect admin processing a voluntary deactivation, I want a checklist workflow that covers: alias removal from L2, GUID status change to `deactivated`, revocation batch inscription on L1, notification to the merchant confirming what's preserved and what's not, and a data retention summary.
- **US-17:** As a GrowDirect admin, I want to see all merchants in grace period or recently deactivated so that the CSM team can attempt win-back outreach before the namespace is fully suspended.

### GrowDirect Admin

- **US-7:** As a GrowDirect admin, I want to pre-mint reserved GUIDs for enterprise prospect categories (no alias reservation) so that when a prospect engages, their pseudonymous L1 identity is already anchored and they choose their own human-readable alias at onboarding.
- **US-8:** As a GrowDirect admin, I want to suspend a namespace if there's a dispute or abuse report so that the registry maintains integrity.
- **US-9:** As a GrowDirect admin, I want to see all registered namespaces with their GUID, aliases, status, owner, tier, and expiry date so that I can manage the registry.

### External Party

- **US-10:** As an insurer, I want to resolve a .jeffe alias to its GUID to confirm the merchant is real and active so that I can trust the receipts they reference in a claim.
- **US-11:** As a developer building on RaaS, I want to programmatically check if a namespace GUID or alias exists before submitting verification requests so that I handle unknown merchants gracefully.

---

## 5. Requirements

### Must-Have (P0)

| ID | Requirement | Acceptance Criteria |
|----|-------------|-------------------|
| **R-1** | Namespace GUID inscription on Bitcoin (L1) | Given an approved registration, when the inscription is submitted, then a Bitcoin Ordinal is created with `type: "namespace"`, `namespace_guid` (UUID v4), `owner_pubkey`, and `registered_by` fields. No human-readable name is inscribed on L1. The inscription chains to the Genesis inscription via `chain.previous`. |
| **R-2** | Human-readable alias registration on Avalanche (L2) | Given a GUID inscription on L1, when the merchant selects a human-readable name, then an alias is registered in the NameRegistry smart contract mapping `alias_name → namespace_guid`. Aliases follow the format rules in Protocol Spec §6.2. |
| **R-3** | `namespace_registrations` table in CRDM (L3 cache) | Given a new GUID inscription, when it is confirmed on Bitcoin, then a row is created in `namespace_registrations` with `merchant_id`, `namespace_guid`, `inscription_id`, `status: 'active'`, and `expires_at` (1 year from registration). |
| **R-4** | `namespace_aliases` table in CRDM (L2 cache) | Given a new L2 alias, when it is registered on Avalanche, then a row is created in `namespace_aliases` caching `alias_name → namespace_guid` for fast L3 resolution. |
| **R-5** | GUID validation | Given a registration request, when the GUID is generated, then it is validated as UUID v4 format (`^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`). GUIDs are system-generated, not user-chosen. |
| **R-6** | Alias name validation (L2) | Given an alias registration request, when the name is submitted, then it is validated against: length (3–63), format (`^[a-z0-9][a-z0-9-]*[a-z0-9]$`), no reserved prefix (`xn--`), and not already registered. Invalid names return a specific error. |
| **R-7** | Namespace lifecycle: registered → active → expired → suspended → deactivated | Given any namespace, when its status changes, then the `namespace_registrations` table reflects the new status, and (for expiry/suspension/deactivation) a revocation inscription is batched on Bitcoin per R-10. **Full lifecycle states:** (a) `registered` — GUID minted on L1, awaiting first receipt inscription; (b) `active` — receiving inscriptions, aliases resolving; (c) `expired` — past `expires_at`, in 30-day grace period, aliases still resolve, new inscriptions paused; (d) `suspended` — grace period elapsed without renewal OR admin suspension, aliases stop resolving, GUID permanently burned, historical receipts verifiable; (e) `deactivated` — voluntary merchant offboarding, same outcome as suspended but merchant-initiated with structured offboarding flow (US-12, US-16). |
| **R-8** | Annual expiry with 30-day grace period — GUIDs are permanent, aliases are releasable | Given an active namespace approaching expiry, when `expires_at` is reached, then status transitions to `expired`. Given the 30-day grace period elapses without renewal, then: (a) The GUID is **permanently burned** — it is never released or reassigned. The Bitcoin inscription is immutable; the GUID's Merkle chain must remain unbroken for all previously inscribed receipts. Status transitions to `suspended` (not deleted). (b) All L2 aliases for that GUID stop resolving and their alias names are released for re-registration by other merchants. (c) The GUID continues to exist on L1 with a revocation inscription marking it as suspended. Historical receipts under this GUID remain verifiable — `verified: true` with `namespace_status: "suspended"` in the response. |
| **R-9** | Public resolution via `GET /v1/resolve/{identifier}` | Given an alias or GUID string, when a GET request is made (no auth required), then: alias mode resolves via L2/L3 to GUID; GUID mode verifies directly. Response includes `registered`, `tier`, `receipt_count`, `last_receipt`, `namespace_guid`. |
| **R-10** | Revocation inscription for expired/suspended namespaces with batched cost model | Given a namespace that expires or is suspended, when the status change occurs, then a `type: "revocation"` inscription is created on Bitcoin with the target GUID inscription_id, reason, and effective_at. **Cost model:** Revocation inscriptions are batched — similar to Merkle batching for receipts. A daily revocation batch job collects all GUIDs that completed grace period or were admin-suspended, inscribes a single batch revocation on L1 listing all affected GUIDs. Cost is borne by GrowDirect as an operational expense (the expired merchant has no active subscription). Batch revocation amortizes L1 inscription cost across all revocations in the batch window. Single-GUID revocations (admin emergency suspension) are inscribed immediately and the cost is absorbed as a security expense. |
| **R-11** | Alias uniqueness enforcement | Given an alias registration request for a name that is already `active` or `reserved`, then the request is rejected with error `alias_taken`. GUID uniqueness is inherent (UUID v4). |

### Nice-to-Have (P1)

| ID | Requirement | Acceptance Criteria |
|----|-------------|-------------------|
| **R-12** | Subdomain alias registration for multi-location merchants | Given an active parent alias, when a subdomain is requested, then a new L2 alias is registered with the subdomain format linking to the same GUID. |
| **R-13** | Dashboard widget showing namespace status + verification activity | Given an authenticated merchant, when they view the Canary dashboard, then they see: GUID (truncated), active aliases, status, expires_at, total receipts inscribed, total verification calls this month. |
| **R-14** | Renewal notification (30 days, 7 days, 1 day before expiry) | Given an active namespace approaching expiry, when the notification threshold is reached, then the merchant receives an alert via the Canary dashboard (and email if configured). |
| **R-15a** | Customer offboarding flow — voluntary deactivation, involuntary suspension, win-back | Given a merchant deactivation event (voluntary close, subscription lapse, admin suspension), then a structured offboarding workflow executes: (a) **Immediate:** aliases removed from L2 resolution (stop resolving within 60s); (b) **Batched:** GUID status updated to `deactivated` or `suspended` in L3, revocation inscription queued for daily L1 batch per R-10; (c) **Notification:** merchant receives confirmation email/dashboard notice explaining: aliases released, GUID preserved, historical receipts still verifiable, data retention period; (d) **Win-back window:** for subscription-lapse cases, CSM team has a 30-day grace period view (US-17) to attempt recovery before final suspension; (e) **Appeals:** suspended-for-dispute merchants can submit an appeal that routes to admin review (US-15). **Cost model:** Same as R-10 — revocation inscriptions batched daily, GrowDirect operational expense. No cost to the departing merchant. |
| **R-15** | Pre-minted GUID pool (no alias reservation) | Given the Fortune 500 + top 100 category list, when pre-registration is executed, then GUID inscriptions are created on L1 with `status: 'reserved'` and no `owner_pubkey` yet assigned. **No human-readable aliases are reserved.** GUIDs are pseudonymous — they carry no trademark risk because they contain no recognizable names. When an enterprise prospect engages, they choose their own alias at registration time. This preserves the opt-in/opt-out anonymity that is fundamental to the protocol's value proposition. The protocol creates economic value through its closed-loop fee structure and proof-of-work verification — not through speculative namespace hoarding. **Anti-speculation gate (Syd + Tom):** Before alias registration opens to any merchant, design a gate-check mechanism that prevents .com-style speculative land-grabs. The .com namespace race was an unintended consequence of open registration — learn from it. Potential approaches: require active Canary LP subscription to hold an alias, tie alias count to verified transaction volume, implement a cooldown/dispute window on new alias claims, or price aliases based on demand signal rather than flat fee. Syd to evaluate which approach best protects the protocol without creating antitrust exposure (Q-12). |

### Future Considerations (P2)

| ID | Requirement | Notes |
|----|-------------|-------|
| **R-16** | Self-service registration portal | Developer portal where merchants register and pay for namespaces directly. Requires Stripe + Lightning integration. |
| **R-17** | Namespace transfer (admin-gated, 10% fee) | Contract function exists but disabled. Enable when 100+ names registered. Syd must review SEC implications. |
| **R-18** | Multi-level subdomains | `dept.store-42.walmart.jeffe`. Only if enterprise customer requests it. |
| **R-19** | NameRegistry on public Avalanche C-Chain | Move from private subnet to public chain. Phase 3 credibility play. |
| **R-20** | Namespace analytics API | External consumers can query namespace statistics (receipt count, uptime, verification volume). Paid endpoint. |
| **R-21** | Alias management self-service | Merchant can add/remove L2 aliases via dashboard without admin intervention. |

---

## 6. Success Metrics

### Leading Indicators

| Metric | Target | Stretch | Measurement |
|--------|--------|---------|-------------|
| Namespaces registered (first 90 days) | 50 | 100 | `namespace_registrations` table count |
| Namespace resolution calls/day | 500 | 5,000 | API analytics on `/v1/resolve` |
| Registration-to-first-inscription time | < 24 hours | < 1 hour | Timestamp delta: `registered_at` → first `merkle_batch` with namespace GUID |
| Inscription success rate | 100% | 100% | Bitcoin mempool monitoring (no failed inscriptions) |

### Lagging Indicators

| Metric | Target (6 months) | Stretch | Measurement |
|--------|-------------------|---------|-------------|
| Renewal rate | > 80% | > 95% | Renewed / (Expired + Renewed) |
| Namespace revenue (annual) | $10K ARR | $50K ARR | Registration fee × active namespaces |
| Reserved-to-claimed conversion | 5% | 15% | Claimed / Reserved (Fortune 500 outreach) |
| Merchant churn rate (with namespace) | < 5% monthly | < 2% | Namespace creates switching cost |

---

## 7. Open Questions

### Blocking

| # | Question | Owner |
|---|----------|-------|
| Q-1 | Registration pricing: flat fee or tiered by alias name length/category? | Jeffe |
| Q-2 | Pre-registration list: which Fortune 500 + categories? Who builds the list? | Jeffe + Will |
| ~~Q-3~~ | ~~Key ceremony for Genesis inscription: who holds the treasury key?~~ **REFRAMED** — This is a DAO governance question, not just a key ceremony. See Q-3a below. (Jeffe, March 4) | ✅ |
| Q-3a | **DAO multi-sig key strategy.** Long-term: the Genesis inscription treasury key is governed by the DAO smart contract. Board-voted members hold multi-sig keys. The key custody model is embedded in the DAO governance structure — whoever the board decides, whatever the voting membership determines. This is where the protocol becomes real. **Phase 1 prototype:** Use a GrowDirect Strike wallet for L402 setup and sandbox validation. This is a working prototype of the full structure — not the final governance model. Strike wallet proves the plumbing works before DAO governance is formalized. **Tom action item:** Design the multi-sig key architecture that can start as a Strike wallet and graduate to DAO-governed multi-sig without re-keying the Genesis inscription. | Jeffe + Tom + Syd |

### Non-Blocking

| # | Question | Owner |
|---|----------|-------|
| Q-4 | Should merchants choose their own `owner_pubkey` or should GrowDirect generate it? | Tom (UX vs. sovereignty tradeoff) |
| Q-5 | Dispute resolution: what happens when two parties claim the same alias? | Syd |
| Q-6 | Configurable anti-spam floor per namespace (owner sets minimum sat cost to be contacted) | Tom + Jeffe |
| Q-7 | Should alias creation require additional fee beyond the base GUID registration? | Jeffe |

### Legal — Positioned (March 4 Session)

All legal questions below have a **GrowDirect position** (our thesis) and a **Syd action** (what we need confirmed or challenged). None of these block technical progress — they are recorded assumptions that Syd validates when the protocol approaches GA.

| # | Question | GrowDirect Position | Syd Action |
|---|----------|-------------------|------------|
| ~~Q-8~~ | ~~Squatting liability~~ | **RESOLVED** — No aliases reserved. GUID-only pre-minting. No trademark exposure. (Jeffe, March 4) | ✅ |
| Q-8a | Anti-speculation gate design | **Require active Canary LP subscription + minimum transaction volume to hold an alias.** You can't squat on a name unless you're a paying merchant with real transaction history. Dead aliases (no transactions for 90 days) get flagged for review. The protocol creates value through the closed-loop economy, not namespace speculation. | Syd: evaluate antitrust implications of tying alias registration to subscription (tying arrangement?). Would a standalone alias product be safer? Recommend cooldown/dispute window as complementary mechanism. |
| Q-9 | Franchise name authority (who registers `mcdonalds.jeffe`?) | **Corporate franchisor has first right to parent alias. Franchisees register subdomains.** McDonald's Corp → `mcdonalds.jeffe`. Franchise locations → `store-1234.mcdonalds.jeffe`. Mirrors real-world trademark authority. If no corporate entity has claimed the parent, individual franchisees can register but are notified the parent may be claimed later. | Syd: define the dispute mechanism when franchisee registers first and franchisor arrives later. Do we need trademark verification for high-value aliases? Is first-come-first-served with dispute process sufficient? |
| Q-10 | Expired namespace receipt validity (legal) | **Historical receipts remain legally valid regardless of namespace status.** The Bitcoin proof is immutable and timestamped. Namespace status at verification time is irrelevant to proof validity at inscription time. RaaS returns `verified: true` with `namespace_status: "suspended"` — the proof existed before the namespace expired. | Syd: any jurisdictions where proof validity is tied to ongoing status of the attesting entity? Do we need explicit language in verification responses: "proof created at [timestamp] under active namespace — current status does not affect proof validity"? |
| Q-11 | Non-transferable → transferable SEC implications | **Namespaces don't transfer within .jeffe — they exit.** The mechanism for "transfer" is: the merchant burns their GUID, the satoshi (inscription) leaves the .jeffe universe, and whatever happens to it outside is not our concern. There is no secondary market within the protocol because there is no transfer mechanism — only exit. The GUID stays permanently burned in .jeffe. This sidesteps the Howey test because there is no "expectation of profit from the efforts of others" when the only option is to leave the ecosystem entirely. The value accrues from usage (verification calls, receipt inscriptions), not from holding and reselling a namespace. | Syd: evaluate the "exit not transfer" model against Howey test. Does burning-and-minting-elsewhere avoid investment contract classification? Does the 10% admin fee on the dormant transfer function (R-17, Phase 2) change the analysis? Recommendation: keep the transfer function disabled and reframe it as "exit" if/when enabled. |
| Q-12 | Sole registrar antitrust exposure | **Low risk at current scale, design for openness.** GrowDirect as sole registrar for a brand-new namespace with zero market share is not an antitrust concern. The NameRegistry contract is designed for eventual multi-registrar support (GRO-13 Decision 5, Phase 3+). Public roadmap commitment: "we're the first registrar, not the only one." | Syd: at what user/revenue threshold does sole-registrar status become problematic? Does the roadmap commitment to multi-registrar provide sufficient legal cover? Should the contract include a registrar-slot mechanism from day one? |
| Q-13 | GUID anonymity wall: GDPR? | **L1 (Bitcoin) is not personal data** — GUIDs + Merkle roots, no re-identification possible without GrowDirect's L3. **L3 (Postgres) is personal data** — GUID → merchant_id mapping, subject to GDPR. **L2 (Avalanche) is the gray zone** — alias → GUID mapping may or may not be personal data depending on whether the alias contains a business name (sole proprietors blur the line). | Syd: is L2 alias mapping personal data when alias contains a business name vs. an arbitrary string? Do we need a DPA with merchants? What's our GDPR Article 17 (right to erasure) position given Bitcoin inscription immutability? |

---

## 8. Timeline

| Phase | Depends On | What Ships |
|-------|-----------|------------|
| Protocol Phase 0 (Week 1–2) | Genesis inscription | Root namespace GUID inscribed. GUID format validated on-chain. |
| Protocol Phase 1 (Week 2–4) | First Merkle batch | First GUID namespace receiving live receipt inscriptions. |
| Protocol Phase 2 (Week 4–8) | Avalanche subnet | NameRegistry contract deployed. First alias registered on L2. Resolution at L2 speed. |
| Namespace GA | Phase 4 QA'd | Registration available to Canary LP merchants. Dashboard widget live. Alias management available. |
| Reserved names | Namespace GA | Fortune 500 + top 100 GUIDs pre-minted, alias names reserved. Sales team has namespace leverage. |

---

## 9. Architecture Summary (GRO-58)

```
Registration Flow:
  Merchant requests namespace
    → GrowDirect generates UUID v4 (namespace_guid)
    → L1: Inscribe type:"namespace" with namespace_guid on Bitcoin (permanent, pseudonymous)
    → L2: Register alias(es) in NameRegistry on Avalanche (human-readable, owner-managed)
    → L3: Cache namespace_guid → merchant_id in namespace_registrations
    → L3: Cache alias → namespace_guid in namespace_aliases

Resolution:
  By alias:  L3 cache → L2 NameRegistry → namespace_guid → L1 verification
  By GUID:   L3 cache → L1 Bitcoin scan → on-chain verification

Privacy wall:
  L1 (Bitcoin):    GUID + event counts + Merkle roots — never merchant identity
  L2 (Avalanche):  alias → GUID mapping — owner-controlled visibility
  L3 (Postgres):   GUID → merchant_id cache — internal ops only
```

---

## 9. Cross-PRD Interface Contract

**Dependency:** The RaaS API (GRO-49) consumes namespace resolution as a service. This PRD defines the data model and lifecycle; RaaS defines the external API surface. Tom must design a clear internal service interface between the two:

| Provider (this PRD) | Consumer (GRO-49 RaaS) | Contract |
|---------------------|----------------------|----------|
| `namespace_registrations` table (L3) | `/v1/resolve`, `/v1/verify` | GUID → merchant_id, status, tier. Must return < 1ms warm. |
| `namespace_aliases` table (L3) | `/v1/resolve`, `/v1/verify` (alias path) | alias → namespace_guid. Must return < 2ms warm (two-hop). |
| L2 NameRegistry (Avalanche) | RaaS alias-path fallback | alias → namespace_guid. Hard timeout 2,000ms. Circuit breaker at 5% error rate (per RaaS R-4). |
| Revocation status | RaaS verify response | Suspended/expired GUIDs return `verified: true` with `namespace_status: "suspended"` — historical receipts remain verifiable. |

**Tom action item:** Define the internal resolution service API (function signatures, error types, timeout contracts) before either PRD moves to implementation. This is the handshake between GRO-49 and GRO-50.

---

*PRD — Namespace Registration v1.4.0 | March 4, 2026*
*MAXIMUM CONFIDENTIAL*
*GRO-58 GUID Namespace Amendment applied*
*v1.1.0 — GUID permanence fix, revocation cost model, cross-PRD interface contract*
*v1.2.0 — No alias reservation (GUID-only pre-minting), anti-speculation gate design*
*v1.3.0 — Customer offboarding flow, DAO multi-sig key strategy, lifecycle expansion*
*v1.4.0 — Legal questions positioned with GrowDirect thesis, "exit not transfer" model, Syd action items*
