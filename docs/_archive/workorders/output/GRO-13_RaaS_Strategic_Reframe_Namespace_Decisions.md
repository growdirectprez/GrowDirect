---
type: workorder
domain: raas
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-13 — RaaS Strategic Reframe + Namespace Architecture Decisions

**Issue:** GRO-13 (B-073)
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** MAXIMUM CONFIDENTIAL — Architecture + Legal
**Gate:** Tom validates API + contract specs. Syd clears 6 legal questions + regulatory review.
**Done When:** Architecture decision documented, namespace decisions locked, Syd clears regulatory.
**Scope:** Architecture + legal review. No code.

---

## 1. Strategic Reframe: Receipt-as-a-Service (RaaS)

### The Shift

| | Old Frame | New Frame |
|---|---|---|
| **Product** | Canary LP (loss prevention for Square merchants) | Canary LP = beachhead; elJeffe Protocol = layer; RaaS = business model |
| **Customer** | Square merchants (subscription) | Any POS integrator, auditor, insurer, regulator (API call) |
| **Revenue** | Monthly SaaS subscription | Subscription + per-verification micropayment (L402, 1 sat/call) |
| **Moat** | Detection algorithms | First-mover on verified receipt standard + .jeffe namespace |
| **Scale** | Linear (merchant count × subscription) | Network (every verification call compounds Metcalfe value) |

### Why This Works Architecturally

The CRDM (v1.0 + v1.1 amendment) normalizes any POS data into canonical schema. The Triple Subscriber Pipeline seals, parses, and inscribes events regardless of source. The L402 gate (IV.3) charges per verification. The .jeffe namespace resolves merchant identity.

RaaS is not a new product. It is the business model that emerges from schema-agnostic design + universal validation gate. The architecture already described in the Manifesto (Sections III through IV.3) produces RaaS as a natural consequence.

> "RaaS. Receipt-as-a-Service. Anyone can hit this service and we will return the receipt."
> — Jeffe, March 1, 2026

---

## 2. RaaS API Design (Tom Spec)

### 2.1 Endpoint: Verify Receipt

```
POST /v1/verify
Content-Type: application/json
Authorization: L402 [macaroon + preimage]

Request:
{
  "event_hash": "sha256:a3f9...",
  "pos_system": "clover",
  "merchant_id": "sunrise-coffee.jeffe",
  "timestamp": "2026-03-01T14:32:15Z"
}

Flow:
→ 402 Payment Required (Lightning invoice: 1 sat)
→ Client pays invoice
→ 200 OK

Response:
{
  "verified": true,
  "block": 884201,
  "merkle_position": 4721,
  "inscription_id": "i39f7a...",
  "namespace": "sunrise-coffee.jeffe",
  "canonical_authority": "eljeffe.io"
}
```

**What happens internally:**
1. L402 middleware validates macaroon + preimage (payment confirmed)
2. Look up `event_hash` in `canary_sales.evidence_records` (Sub 1 store)
3. If found → return inscription proof from `canary_sales.merkle_batches` (Sub 3 store)
4. If not found → `{ "verified": false, "reason": "hash_not_found" }`
5. No POS-specific logic. Hash is hash. Source-agnostic by design.

**Rate Limiting:** 1,000 req/min per API key. Burst: 100 req/10sec.

### 2.2 Endpoint: Retrieve Receipt History

```
GET /v1/receipt/{merchant_name}?range=2026-03-01&limit=100
Authorization: L402 [macaroon + preimage]

Response:
{
  "merchant": "sunrise-coffee.jeffe",
  "receipts": [
    {
      "event_hash": "sha256:a3f9...",
      "timestamp": "2026-03-01T14:32:15Z",
      "verified": true,
      "inscription_id": "i39f7a...",
      "merkle_proof": ["sha256:b2c4...", "sha256:d8e1..."]
    }
  ],
  "total": 187,
  "anchor_block": 884201,
  "pagination": {
    "cursor": "eyJ0IjoiMjAyNi0wMy0wMVQxNDozMjoxNVoifQ==",
    "has_more": true
  }
}
```

**What happens internally:**
1. L402 middleware validates payment (1 sat per call, not per receipt)
2. Resolve `merchant_name` → `merchant_id` via `.jeffe` NameRegistry
3. Query `canary_sales.evidence_records` by merchant_id + date range
4. Join to `canary_sales.merkle_batches` for inscription proof
5. Return paginated results with Merkle proofs

**Rate Limiting:** 1,000 req/min per API key. Pagination required for >100 results.

### 2.3 Endpoint: Namespace Resolution (Public)

```
GET /v1/resolve/{merchant_name}

Response:
{
  "name": "sunrise-coffee.jeffe",
  "registered": true,
  "owner_since": "2026-02-15",
  "tier": "standard",
  "receipt_count": 12847,
  "last_receipt": "2026-03-01T14:32:15Z"
}
```

**No L402 gate.** Public resolution endpoint. Establishes the namespace as a lookup service. Drives traffic to the paid verification endpoints.

### 2.4 API Versioning

Per Jeffe's directive (GRO-17 feedback): all endpoints use `/v1/` prefix. Breaking changes get `/v2/`. No sunset without 6-month notice. Swagger/OpenAPI spec published at `/v1/docs`.

---

## 3. Six Namespace Business Decisions (Locked)

These were decided by Jeffe on March 1, 2026. They are LOCKED. Tom incorporates into NameRegistry contract spec. Syd reviews for legal implications.

### Decision 1: Reserved Names → PRE-REGISTER

- Fortune 500 + top 100 Square merchant categories reserved before launch
- When enterprise shows up, name is already minted and waiting — sales leverage
- Everything else is first-come-first-served

**Tom action:** NameRegistry contract needs `reserved_names` table. Reservation state: `reserved` (pre-minted, unassigned), `claimed` (assigned to merchant), `active` (in use with receipts).

**Syd question:** Can we reserve names for companies that haven't engaged with us? Is there squatting liability exposure if we pre-register `.walmart.jeffe` without Walmart's consent?

### Decision 2: Subdomain Depth → ONE LEVEL AT LAUNCH

- Ship with one level: `store-42.walmart.jeffe`
- No arbitrary depth until an enterprise customer actually asks
- Reduces parsing complexity, delegation chains, attack surface

**Tom action:** NameRegistry parser validates single-level only. Regex: `^[a-z0-9-]+\.[a-z0-9-]+\.jeffe$`

**Syd question:** If a franchise operator registers `mcdonalds.jeffe`, does our one-level constraint prevent the franchisee from subdividing? Who has authority to approve name registration for franchise brands?

### Decision 3: Pricing Lock-in → ANNUAL RENEWAL ONLY

- No perpetual ownership at launch
- Protects recurring revenue and repricing flexibility
- 3-year prepay at discount is the maximum lock-in offered

**Tom action:** NameRegistry expiry logic. Fields: `registered_at`, `expires_at`, `renewal_price_sats`. Grace period: 30 days after expiry before release.

**Syd question:** What happens to verified receipts anchored to a namespace that expires and is re-registered by a different merchant? Are the historical proofs still valid? (Answer should be yes — proofs are hash-based, not name-based — but Syd needs to confirm there's no legal ambiguity.)

### Decision 4: Resale Market → NON-TRANSFERABLE AT LAUNCH

- No secondary market until 100+ registered names
- Prevents speculation and squatting in early market
- Flip the switch later with 10% transfer fee

**Tom action:** NameRegistry transfer function exists in contract but is disabled (admin gate). Transfer fee parameter configurable.

**Syd question:** If we later enable transfers, does the 10% fee constitute a securities transaction? Does the namespace itself become a "digital asset" under SEC guidance if it's transferable with a fee structure?

### Decision 5: Secondary Registrars → NO — GROWDIRECT ONLY THROUGH PHASE 2

- Single registrar (GrowDirect) controls the namespace
- No licensing to Unstoppable Domains or others
- Phase 3 DAO conversation at earliest

**Tom action:** NameRegistry has single `registrar_address` in contract. No multi-registrar logic until Phase 3.

**Syd question:** If we're the sole registrar for a naming system, does that create antitrust exposure when the system scales? What's our defensible position if a competitor claims we're gatekeeping a public standard?

### Decision 6: Public vs. Private Subnet → PRIVATE THROUGH PHASE 2

- Full control over validator set, fee policy, upgrade cadence
- Public Avalanche C-Chain is a Phase 3 credibility play
- Premature decentralization is a distraction during market fit

**Tom action:** Avalanche subnet with GrowDirect-controlled validator set. Upgrade path to C-Chain documented but not built.

**Syd question:** Does running a private subnet (even on Avalanche) make GrowDirect a "centralized service provider" rather than a "protocol operator"? If so, does this change our liability profile for data accuracy claims?

---

## 4. Legal Questions for Syd (6 from Jeffe + 6 from Namespace Decisions)

### From Jeffe (March 1 capture):

| # | Question | Context |
|---|----------|---------|
| L-1 | Trademark disputes on .jeffe names | What's our liability if a merchant registers a trademarked name? Do we need UDRP-equivalent dispute resolution? |
| L-2 | UDRP applicability | Does ICANN's Uniform Domain-Name Dispute-Resolution Policy apply to .jeffe names, or is this a private namespace outside UDRP jurisdiction? |
| L-3 | Money transmitter classification | Does charging 1 sat per API call via Lightning Network make GrowDirect a money transmitter? |
| L-4 | L402 micropayment taxation | How do we report revenue from sub-cent Lightning payments? Is each sat a taxable event? |
| L-5 | Liability for verification accuracy | If a RaaS consumer relies on a "verified: true" response and the underlying inscription has an error, what's our liability? |
| L-6 | RaaS regulatory classification | Is "Receipt-as-a-Service" a financial service, a data service, or something else? Does it require any specific license? |

### From Namespace Decisions (above):

| # | Question | Decision |
|---|----------|----------|
| N-1 | Pre-registration squatting liability | Decision 1 (Reserved Names) |
| N-2 | Franchise name authority | Decision 2 (Subdomain Depth) |
| N-3 | Expired namespace receipt validity | Decision 3 (Annual Renewal) |
| N-4 | Transferable namespace = digital asset / security | Decision 4 (Non-Transferable) |
| N-5 | Sole registrar antitrust exposure | Decision 5 (No Secondary Registrars) |
| N-6 | Private subnet centralization liability | Decision 6 (Private Subnet) |

**Syd deliverable:** Written opinion on all 12 questions. Flag any that require outside counsel.

---

## 5. RaaS Revenue Model

### Three-Tier Service Architecture

Per Jeffe's feature flag decision (March 1), the service runs three tiers:

| Tier | Domain | Auth | Hash Chain | Inscription | Price |
|------|--------|------|------------|-------------|-------|
| **Free** | eljeffe.org | API key | Postgres hash only | None | $0 |
| **Standard** | eljeffe.io | L402 | Postgres + Merkle | Bitcoin Ordinal | 1 sat/verification |
| **Enterprise** | eljeffe.io | L402 + SLA | Postgres + Merkle + Avalanche | Bitcoin + Avalanche dual-anchor | Custom |

**Domain routing logic:**
- `eljeffe.org` → Free tier. No L402 gate. Postgres hash chain only. No Bitcoin inscription. This is the "try before you buy" tier — POS integrators can validate the API works before committing to paid.
- `eljeffe.io` → Paid tiers. L402 gate. Full inscription chain. Production SLA.

**Unit economics (from PhD B-077):**
- 1 sat = $0.00085 at $85,000/BTC
- 1M calls/day = $850/day = $310,250/year — pure margin
- At 10K+ merchants with multiple integrators querying, RaaS overtakes subscription as primary revenue

### Revenue Streams (Additive)

1. **Subscription revenue:** Canary LP merchants pay monthly SaaS fee. Stops on churn.
2. **Validation revenue (IV.3):** Anyone querying past inscriptions. Continues after merchant churn.
3. **RaaS revenue:** External POS integrators and third parties. New stream requiring zero additional infrastructure.
4. **Namespace revenue:** Annual .jeffe name registration fees.

---

## 6. Integration with Existing Architecture

### How RaaS Maps to TSP

```
External POS (Clover, Toast, etc.)
  │
  ▼
RaaS Ingestion Adapter (new — converts POS-specific format to canonical)
  │
  ▼
TSP-01 (Webhook Receipt) ← already source-agnostic with CRDM v1.1
  │
  ▼
TSP-02 (Queue Fan-Out) ← no change
  │
  ├─→ TSP-03 (Sub 1: Seal) ← no change
  ├─→ TSP-04 (Sub 2: Parse) ← new parser per POS, same interface
  └─→ TSP-05 (Sub 3: Inscribe) ← no change
```

**Key insight:** The TSP doesn't need to change. Only the ingestion layer (TSP-01) and parse layer (TSP-04) need per-POS adapters. Sub 1, Sub 3, and the queue are source-agnostic by design.

### How RaaS Maps to CRDM v1.1

The `external_identities` table (Amendment 1 of GRO-45) is the bridge:

```
Clover payment_id → external_identities (source='clover') → canonical transaction_id
Toast order_id → external_identities (source='toast') → canonical transaction_id
Square payment_id → external_identities (source='square') → canonical transaction_id
```

The CRDM v1.1 POS-agnostic entity model was designed specifically for this. Every RaaS integration is an `external_identities` row, not a schema change.

---

## 7. Go-to-Market Implications

### New Positioning

- **Hook:** "Any POS. Any merchant. One API call."
- **Elevator:** "We verify every retail receipt against Bitcoin. Square today, every POS tomorrow. One sat per verification."
- **Investor sentence:** "Canary LP is the beachhead. elJeffe is the protocol. RaaS is the product every POS integrator buys."

### Integration Targets (Priority Order)

| POS | Market Share | Integration Complexity | Notes |
|-----|-------------|----------------------|-------|
| **Square** | 30% SMB | Done (Phase 1) | Beachhead. Webhook-dense. |
| **Clover** | 25% SMB | Medium (REST API, webhooks) | Fiserv subsidiary. Large SMB install base. |
| **Toast** | 15% restaurant | Medium (REST API, webhooks) | Restaurant-focused. High transaction volume. |
| **Shopify POS** | 10% retail | Low (well-documented API) | E-commerce + physical crossover. |
| **Lightspeed** | 8% retail/restaurant | Medium (REST API) | Multi-vertical. International. |
| **Standalone terminals** | 12% | High (varies by manufacturer) | Long tail. Custom adapters needed. |

### What Changes in Investor Materials (→ GRO-16)

1. **Hero section:** RaaS framing replaces "loss prevention" as lead
2. **TAM/SAM:** Expand from Square-only to all POS ($4.5T global retail)
3. **Architecture slide:** Add RaaS API layer above TSP
4. **Revenue model:** Three streams (subscription + validation + RaaS + namespace)
5. **Moat slide:** First-mover on verified receipt standard

---

## 8. Open Questions for Tom

1. **L402 middleware implementation:** Use LND REST API? CLN? Or Lightning Service Provider (LSP) like Voltage? What's the minimum viable L402 gate?
2. **NameRegistry contract language:** Solidity on Avalanche subnet? Or off-chain registry in Postgres until volume justifies on-chain?
3. **API gateway for RaaS:** Express.js middleware (per GRO-17 recommendation) or dedicated Kong instance for external traffic?
4. **RaaS ingestion adapter pattern:** Same TSP-01 webhook receiver with POS-specific signature verification? Or separate ingestion service per POS?
5. **Batch verification endpoint:** Should we offer `POST /v1/verify/batch` for auditors who need to verify 10,000 receipts at once? Different pricing?
6. **Free tier rate limiting:** How aggressive? If `eljeffe.org` is free, what prevents abuse? IP-based rate limiting? API key required even for free?

---

## 9. Routing

| Agent | Action | Deliverable |
|-------|--------|-------------|
| **Tom** | Validate API spec, answer 6 technical questions, design NameRegistry contract, L402 middleware selection | Architecture decision record |
| **Syd** | Answer 12 legal questions (6 Jeffe + 6 namespace), RaaS regulatory review | Legal opinion memo |
| **Jeremy** | Review RaaS ingestion adapter pattern, estimate per-POS parser effort | Effort estimate |
| **Jess** | Update investor language with RaaS framing (feeds GRO-16) | Content brief |
| **Will** | Pivot lead gen messaging: "Any POS, any merchant, one API call" | LEO playbook update |
| **Art** | Investor deck v1.1: add RaaS architecture slide | Design mockup |

---

*ALX | GRO-13 | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
