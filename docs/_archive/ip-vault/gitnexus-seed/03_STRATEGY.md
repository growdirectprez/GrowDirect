---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Strategy & Market Position

> **Domain:** Business strategy, investor narrative, competitive landscape, go-to-market
> **Last Updated:** 2026-03-19 | **Classification:** Confidential

---

## Market Thesis

33 million SMB retailers in the US lack access to enterprise-grade loss prevention tools. Enterprise LP software (Appriss, Agilence, StoreNext) costs $50K–$500K/year and requires dedicated LP teams. Small businesses experience the same shrink rates (1.4% of revenue on average) but absorb losses as an invisible cost of doing business.

Canary LP delivers enterprise-caliber loss prevention to SMB merchants through their existing Square POS, starting at $29/month. No hardware, no dedicated staff, no enterprise sales cycle.

---

## Core Narrative: tLog to gLog

**tLog** (IBM 4690, 1986–2017) — The transaction log that powered retail for three decades. Mutable, institutional, database-dependent. When the database is the only source of truth, the truth is corruptible. tLogs live on a server; if the server dies, the proof dies.

**gLog** (elJeffe protocol, 2026–) — The next evolution: immutable, Bitcoin-native, permanent event sourcing. Every commercial event hashed, Merkle-batched, and inscribed on Bitcoin. PII hashed before inscription. Permanence guaranteed by block height, not institutional promise. The gLog doesn't need the company to still exist for someone to verify it's authentic.

This is the transition from trust-the-database to verify-the-math. Canary is the product that makes this transition accessible to every merchant, not just enterprise retailers with dedicated blockchain teams.

---

## Competitive Landscape

### Enterprise LP Software
**Appriss Retail** — Exception-based reporting (EBR) platform for enterprise retailers. Requires data warehouse integration, dedicated LP analysts. Strengths: deep analytics, proven at scale. Weakness: cost ($100K+/year), complexity, no SMB offering.

**Agilence** — Cloud-based LP analytics. Focus on grocery and specialty retail. Strengths: modern UI, cloud-native. Weakness: still enterprise-priced, requires IT integration.

**StoreNext (Zebra)** — Hardware-integrated LP (cameras + POS + analytics). Strengths: physical evidence correlation. Weakness: hardware dependency, installation cost.

### Where Canary Differentiates
1. **Square-native** — No integration project. Connect via OAuth, data flows in minutes.
2. **AI-first** — Owl delivers plain-English insights, not spreadsheet exports.
3. **SMB pricing** — $29–$299/month, not $50K–$500K/year.
4. **Immutable evidence** — elJeffe protocol provides Bitcoin-anchored proof, not database-dependent records.
5. **Real-time** — Alerts on the store floor as events happen, not quarterly reports.

---

## Revenue Model

### Subscription Tiers
- **Starter ($29/mo):** Core detection rules, daily digest, up to 2 locations
- **Professional ($99/mo):** Full Chirp engine, Owl AI, Fox case management, up to 10 locations
- **Enterprise ($299/mo):** Custom rules, API access, Bitcoin inscription, unlimited locations

### Protocol Revenue (elJeffe)
- **Namespace registration:** Annual BTC fee per merchant namespace
- **RaaS API (Rule-as-a-Service):** 1 sat per verification call via L402 micropayment
- **L402 validation:** 1 sat per receipt verification
- **Burner minting:** Disposable sub-addresses for specific use cases

---

## Investor Positioning (War Chest)

Five investment briefs have been developed:

**Block Space** — Why Bitcoin Ordinals as permanent infrastructure. The cost-benefit of inscription vs. traditional database storage for commercial proof.

**Genesis Pool** — Network economics and Canary treasury model. How namespace registrations and verification fees create sustainable protocol revenue.

**VeriSign** — The verification mechanism: SHA-256 Merkle proofs that work without servers. The analogy to VeriSign's role in early internet trust, but decentralized.

**Vertical Integration** — Growth path from SMB loss prevention to enterprise supply chain verification. Cannabis retail as a beachhead market (regulatory compliance + high shrink rates).

**tLog to gLog** — Historical context document. The 40-year arc from IBM 4690 transaction logs to Bitcoin-native event sourcing.

---

## Go-to-Market

### Phase 1: Square Marketplace
Primary distribution channel. Square's app marketplace reaches millions of active merchants. Canary positions as the LP app for Square — connect in minutes, see alerts today.

### Phase 2: Community-Led Growth
Square Seller Community engagement. Pre-identified threads: cash drawer variance, inventory shrinkage, refund abuse, chargebacks, after-hours transactions. Response template: diagnose the problem, validate the pain, position Canary as the solution. Weekly cadence: 2-3 substantive replies per week.

### Phase 3: Content & SEO (WORM Sprint)
12 primary keywords targeted: Employee Theft POS, Square Refund Fraud, AI Loss Prevention SMB, Excessive Refund Rate, Marketplace App, Loss Prevention Small Business, Inventory Shrinkage, Chargeback Prevention, After Hours Transactions, LP Trends, POS Audit, LP Comparison.

Landing page redesign shipping March 28, 2026: hero with $29/mo pricing, pain-point columns (Employee Theft, Refund Fraud, Inventory Shrinkage), 4-step how-it-works visual, schema markup (Organization, SoftwareApplication, FAQ, BreadcrumbList).

### Cannabis Retail Beachhead
Cannabis retailers face unique LP challenges: high shrink rates, regulatory reporting requirements, seed-to-sale tracking compliance. Canary's CRDM is POS-agnostic by design, and the Cannabis Retail Risk Dictionary (part of the research corpus) maps cannabis-specific detection rules to the Chirp engine. This vertical provides high willingness-to-pay and regulatory-driven adoption.

---

## Phase Roadmap

| Phase | Scope | Status |
|-------|-------|--------|
| 0-A | Square OAuth + sandbox credentials | Complete |
| 0-B | Webhook receiver + HMAC verification | Complete |
| 1-A | Sub 1 (Seal) — SHA-256 hashing, evidence_records | In progress |
| 1-B | Sub 2 (Parse) — Vendor parsers → CRDM | In progress |
| 1-C | Sub 3 (Merkle + Inscribe) — Batch + Bitcoin submission | Planned |
| 2 | Verification round-trip (RaaS API) | Planned |
| 3 | Device attestation pipeline | Planned |
| 4 | Square Marketplace submission | Planned |

---

*Canary LP | GrowDirect Inc. | Confidential*
