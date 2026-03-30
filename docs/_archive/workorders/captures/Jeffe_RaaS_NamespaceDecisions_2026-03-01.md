---
type: decision
domain: raas
status: active
created: 2026-03-01
updated: 2026-03-19
---
# Jeffe Capture: RaaS + Namespace Business Decisions
**Date:** March 1, 2026
**Context:** Follow-up to B-072 Symbiosis Thesis dispatches. Jeffe reviewed Tom's .jeffe Namespace Architecture (10 open questions) and made 6 business decisions. Additionally captured a strategic reframing: Receipt-as-a-Service (RaaS).

---

## Strategic Reframe: RaaS — Receipt-as-a-Service

**Jeffe's words (paraphrased):**
> "RaaS. Receipt-as-a-Service. It's an industry standard in the making. Anyone can hit this service and we will return the receipt. That's what I would market to Clover, Toast, even just the standalone thing."

**What this means:**
- Canary LP = beachhead product (Square-specific loss prevention)
- elJeffe Protocol = the notarization layer (Bitcoin + Avalanche)
- **.jeffe namespace = the addressing layer** (DNS for receipts)
- **RaaS = the business model** (verification endpoint as a service)

**The shift:**
- Old framing: "We sell a namespace to merchants"
- New framing: "We sell a verification endpoint to every POS system on earth"
- Clover, Toast, Lightspeed, Shopify POS, any standalone terminal — they don't build anything. They hit the API, pay a sat via L402, get a verified receipt back.
- The .jeffe namespace is the addressing layer underneath, but the product is the API call.

**Implications:**
1. **Go-to-market widens massively** — not Square-only. Any POS integration is a customer.
2. **Pricing simplifies** — per-verification micropayment (L402). No subscription required for the base service.
3. **Standard adoption accelerates** — auditors/insurers can mandate "RaaS-verified receipts" without caring which POS the merchant uses.
4. **Moat deepens** — first mover on the standard. When regulators require verified receipts, they require RaaS. When they require RaaS, they require .jeffe.

---

## 6 Namespace Business Decisions (Locked)

### 1. Reserved Names
**Decision:** PRE-REGISTER
- Fortune 500 + top 100 Square merchant categories reserved before launch
- When enterprise shows up, name is already minted and waiting — sales leverage
- Everything else is first-come-first-served

### 2. Subdomain Depth
**Decision:** ONE LEVEL AT LAUNCH
- Ship with one level (`store-42.walmart.jeffe`)
- No arbitrary depth until an enterprise customer actually asks
- Reduces parsing complexity, delegation chains, attack surface

### 3. Pricing Lock-in
**Decision:** ANNUAL RENEWAL ONLY
- No perpetual ownership at launch
- Protects recurring revenue and repricing flexibility
- 3-year prepay at discount is the maximum lock-in offered

### 4. Resale Market
**Decision:** NON-TRANSFERABLE AT LAUNCH
- No secondary market until 100+ registered names
- Prevents speculation and squatting in early market
- Flip the switch later with 10% transfer fee

### 5. Secondary Registrars
**Decision:** NO — GROWDIRECT ONLY THROUGH PHASE 2
- Single registrar (GrowDirect) controls the namespace
- No licensing to Unstoppable Domains or others
- Phase 3 DAO conversation at earliest

### 6. Public vs. Private Subnet
**Decision:** PRIVATE THROUGH PHASE 2
- Full control over validator set, fee policy, upgrade cadence
- Public Avalanche C-Chain is a Phase 3 credibility play
- Premature decentralization is a distraction during market fit

---

## Routing

| Agent | Action |
|---|---|
| **Tom** | Incorporate 6 decisions into NameRegistry contract spec. Design RaaS API endpoint (POST /verify, GET /receipt/{name}). Answer his own 6 technical questions. |
| **Syd** | Answer 6 legal questions (trademark disputes, UDRP, money transmitter, L402 taxation, liability). Review RaaS model for regulatory exposure. |
| **PhD** | Add RaaS framing to Manifesto. This is a new section — "Layer 8: Receipt-as-a-Service" or expansion of existing Layer 7. |
| **Jess** | Update investor language: RaaS is the business model sentence. War Chest source update. Investor site v4.0 framing. |
| **Will** | RaaS changes lead gen messaging. "Any POS, any merchant, one API call" is the new hook. |
| **Art** | Investor deck v1.1 needs a RaaS slide (between Solution and Architecture). |

---

## Classification
**MAXIMUM CONFIDENTIAL** — Contains strategic business decisions and product positioning.
