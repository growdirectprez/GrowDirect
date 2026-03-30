---
type: pitch
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# War Chest Source 56: Competitive Landscape
**Created:** March 1, 2026 by ALX
**Classification:** MAXIMUM CONFIDENTIAL
**Manifesto:** IV.1 (Genesis Pool), IV.7 (Egalitarian Copyright), V.1 (Hybrid Architecture)
**Spine:** Act 6 (The Moat)

---

## The Gap

Nobody occupies the intersection of: Square-native, SMB-focused, loss-prevention-specific, immutable proof layer, and POS-agnostic verification API. Canary LP and RaaS sit in this gap.

Square's App Marketplace has 438+ apps. Zero are dedicated loss prevention tools. That's the market failure.

---

## Tier 1: Enterprise LP Platforms (Not competitors — future customers/partners)

### Agilence (Analytics Plus)
- **What:** Exception-based reporting + LP analytics for retail chains
- **Target:** Enterprise (50+ locations, dedicated LP departments)
- **Data sources:** 200+ integrations (POS, eCommerce, HR, inventory, video)
- **Scale:** 24 million transactions processed daily
- **Pricing:** Enterprise only, no public pricing ($50K+/year range)
- **Gap:** No Bitcoin. No immutability. No SMB. No Square integration. Reports are only as trustworthy as the mutable POS data ingested. If someone changes the transaction log, Agilence doesn't know.
- **RaaS angle:** Agilence could integrate RaaS to give enterprise reports a notarized evidence layer. Partnership play, not competition.

### Verkada
- **What:** AI-powered video + POS overlay for organized retail crime
- **Target:** Enterprise retail, multi-location chains
- **Gap:** Hardware-dependent (cameras required). No SMB. No POS-agnostic verification.

### RetailNext
- **What:** In-store analytics — traffic counting, heat mapping, conversion
- **Target:** Physical retail chains
- **Gap:** Not loss prevention. Analytics only. No transaction-level fraud detection.

### Securitas Technology (TRENDS)
- **What:** Video surveillance + exception-based reporting + shrinkage analytics
- **Target:** Enterprise retail
- **Gap:** Camera + sensor dependent. No data-only LP solution. No SMB.

### Sensormatic IQ (Johnson Controls)
- **What:** Advanced video analytics + transactional data correlation
- **Target:** Large retailers
- **Gap:** Hardware ecosystem lock-in. No API-first approach.

---

## Tier 2: Square's Own Analytics (Direct neighbors)

### Square Dashboard (built-in)
- **What:** Sales trends, customer behavior, inventory performance
- **Pricing:** Free with Square POS
- **Gap:** Tells merchants what sold. Does NOT tell them what was stolen. No shrinkage detection, no refund pattern analysis, no employee theft flagging.

### Square Risk Manager
- **What:** Fraud detection on incoming payments (buyer-side fraud)
- **Pricing:** Included with Square
- **Gap:** Protects against buyer fraud (chargebacks, stolen cards). Does NOT detect internal theft, sweethearting, refund manipulation, cash drawer anomalies. Completely different problem space from Canary.

### Square App Marketplace
- **Stats:** 438+ apps, approaching 1,000 partners
- **Categories:** Marketing, inventory, accounting, loyalty, scheduling, delivery
- **Gap:** ZERO dedicated loss prevention apps. No LP category exists.

---

## Tier 3: POS-Agnostic SaaS LP (Closest to our space)

### Extenda Retail (Self-Service LP)
- **What:** Statistical models on POS data to calculate loss probabilities
- **Target:** Self-checkout fraud at scale retailers
- **Gap:** Not SMB. No Bitcoin. No immutability. No receipt notarization. No Square integration.

### Eposly
- **What:** Predictive analytics for retail shrink (ML on POS data)
- **Target:** UK-focused, own POS ecosystem
- **Gap:** Not Square-native. Not POS-agnostic. No immutability layer.

### Facit Analytics
- **What:** Intelligent LP using ML anomaly detection on transaction data
- **Target:** Mid-market to enterprise
- **Gap:** No immutable proof layer. No micropayment verification. No SMB.

---

## Tier 4: Fraud Prevention Platforms (Adjacent, not direct)

### Stripe Radar
- **What:** ML fraud detection for online payments
- **Gap:** Online only. Not in-person POS. Not loss prevention.

### Kount (Equifax)
- **What:** Identity trust + device analytics, pre-authorization fraud
- **Gap:** Buyer-side fraud only. No merchant-side LP.

### Riskified
- **What:** Chargeback guarantee model — takes liability for approved fraudulent transactions
- **Gap:** eCommerce only. No physical retail.

---

## Our Unique Position

| Capability | Agilence | Square | Extenda | Stripe | **Canary/RaaS** |
|---|---|---|---|---|---|
| Square-native | No | Yes | No | No | **Yes** |
| SMB-focused ($29/mo) | No | Yes | No | Partial | **Yes** |
| Loss prevention specific | Yes | No | Yes | No | **Yes** |
| Immutable proof (Bitcoin) | No | No | No | No | **Yes** |
| POS-agnostic API | Partial | No | Partial | Yes | **Yes (RaaS)** |
| Receipt notarization | No | No | No | No | **Yes** |
| Micropayment verification | No | No | No | No | **Yes (L402)** |

**The five things nobody else does:**
1. Notarize transaction data on Bitcoin (immutable, proof-of-work secured)
2. Sell loss prevention to Square's 4.5M merchants (zero current options)
3. Offer POS-agnostic receipt verification as an API (RaaS)
4. Charge per-verification via L402 micropayments (1 sat = ~$0.001)
5. Create permanent property rights from disposable transaction logs

---

## Key Investor Sentences

- "Square has 4.5 million merchants and zero loss prevention tools in its App Marketplace."
- "Enterprise LP costs $50,000/year and requires cameras. Canary costs $29/month and requires a Square account."
- "Every LP platform on the market analyzes mutable data on mutable servers. We're the only one that makes the record permanent."
- "RaaS turns every POS system into a client. Clover, Toast, Lightspeed — they don't build anything. They hit our API."
- "Agilence isn't our competitor. They're our future customer."

---

## Square Data Retention Note

Square has no published data retention policy for merchant transaction data. Their privacy notice says data is retained "for a period consistent with applicable law" after account closure. Industry floor: PCI DSS requires 1 year audit logs (90 days immediately available). IRS requires 3-7 years for financial records. This ambiguity strengthens the gLog argument: merchants cannot verify that Square hasn't modified or deleted their transaction history. The Bitcoin inscription is the merchant's independent proof.
