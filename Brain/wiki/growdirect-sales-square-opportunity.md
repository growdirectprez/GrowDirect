---
date: 2026-04-22
type: wiki
tags: [growdirect, sales, pitch-deck, canary, square, ceo-briefing]
sources:
  - docs/_archive/ip-vault/sales/Canary_Square_Opportunity.pptx
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Canary Square Opportunity — CEO Briefing (Feb 2026)

**Confidential CEO briefing deck** pitching Canary Loss Prevention as the first-and-only LP app targeting Square's 4M+ merchant base. 17 slides across 6 acts.

## Cover

**CANARY — Early Warning LP**
*Square Market Opportunity: Canary Loss Prevention for 4M+ Merchants*
February 2026 · CEO Briefing · Confidential

## Act 1 — The Opportunity

$132B annual retail shrinkage. 4M Square merchants. **Zero LP tools on the marketplace.**

**Market sizing:**
- 4M Square merchants
- $132B annual shrinkage
- $4.7B U.S. POS TAM 2026
- Square GPV growing 12% YoY. Mid-market sellers (>$125K GPV) growing 20% YoY.

**Product-market fit:**
- What Canary detects — real-time refund fraud, void/cancel abuse, discount manipulation, cash handling anomalies, after-hours activity. Bayesian adaptive baselines per merchant.
- 5 detection domains, 27+ risk metrics
- KAP scoring across employees, consumers, locations
- Self-calibrating — no manual tuning
- Why Square first — 4M active merchants, 80–90% single-location SMBs. Restaurants 30–40%, Retail 25–35%, Beauty 10–15%. No competing LP app on Square Marketplace. OAuth read-only: zero friction.

## Act 2 — Where We Are

**MVP is live.** RefundRadar engine running. Dashboard deployed. All 8 known bugs resolved.

**Built:**
- Real-time refund scanning via Square webhooks
- Responsive Tailwind dashboard with natural-language query
- Receipt detail viewer, SSE live alerts
- Flask + SQLite (migrating to PostgreSQL), OAuth 2.0 read-only, PhD-validated quantitative framework ready

**Next:**
- Production deploy on Railway ($17–32/mo)
- Bayesian RefundRadar upgrade (scipy)
- PostgreSQL migration + Redis cache
- Webhook signature verification
- 5 beta merchants for Square certification gate
- BTCPay Lightning billing integration

## Act 3 — Roadmap

Five phases. Pre-Alpha → Marketplace Launch in 9 months. **$15K total capital to launch.**

| Phase | Dates | Focus |
|---|---|---|
| Pre-Alpha | Now–Mar 2026 | Bayesian engine, PostgreSQL, KAP scoring, legal docs |
| Alpha | Apr–Jun 2026 | 5 beta merchants, webhook hardening, demo video |
| Beta | Jul–Sep 2026 | Square Marketplace submission, XGBoost classifier, BTCPay live |
| Launch | Oct–Dec 2026 | Marketplace live, 200 merchants |
| Scale | 2027 | Federated learning, 500+ merchants |

**Break-even at just 15 paying merchants.**

Strategic focus: Phase 1 restaurants and retail (65% of Square base). Single-location merchants first — lowest friction, highest pain. CAC under $200 via Marketplace organic discovery. Network effect moat. First-mover advantage.

## Act 4 — Competitive Landscape

Enterprise LP tools exist but none serve SMBs through POS marketplaces. **We own the gap.**

- **Appriss Retail (now Sysrepublic):** Enterprise EBR, $50K+ annual, 6-month deployments, dedicated LP teams required
- **Agilence:** Cloud analytics for mid-to-large retailers, $25K+/year min, not on POS marketplaces

**LP legacy requires 50+ locations to justify ROI. None integrate natively with Square, Shopify, or Clover. Zero marketplace-native LP apps exist today.**

Canary advantage — marketplace-native (2-click install, no IT), $49–199/mo vs $25K–50K/yr, adaptive Bayesian vs static rules, cross-merchant anonymized benchmarks, Bitcoin-native billing (zero processing fees), first-and-only LP app on Square Marketplace.

## The Ask

- **$15K** to Marketplace launch
- **88%** gross margin
- **15** merchants to break even
- $160K BTC treasury = 8–12 year runway
- 200 merchants × $99/mo = $19,800/mo recurring (0.2 BTC)
- Network effect compounds with every new merchant

## Act 5 — Conference Roadshow 2026

Six events. LP, retail tech, SMB commerce. Build pipeline face-to-face.

| Date | Event | Location / Focus |
|---|---|---|
| Jan 11–13 | NRF Big Show 2026 | NYC — retail tech ecosystem |
| Apr 19–22 | RILA Asset Protection | TBD — **LP + shrinkage leaders** |
| Jun 8–10 | NRF PROTECT 2026 | Grapevine, TX — **LP decision-makers** |
| Jun 23–24 | CommerceNext GrowthShow | NYC — eCommerce + retail growth |
| Sep 14–16 | Shoptalk Fall 2026 | Nashville — retail innovation |
| Oct (TBD) | Money 20/20 USA | Las Vegas — payments + fintech |

Priority targets: **RILA AP + NRF PROTECT** (LP buyers). Booth not required — demo from tablet + swag.

### Swag Concepts

- Black polo (Canary wordmark, gold embroidered)
- Black long-sleeve button-down (executive meetings)
- Matte black coffee mug (gold logo + "Early Warning LP" tagline)
- Brand: gold #FBBF24 on matte black. Minimal aesthetic. No QR codes / URLs on merch.

## Act 6 — Franchise Channel

**One corporate deal. Hundreds of locations. The multiplier play.**

Square for Franchises gives corporate HQ a centralized dashboard over all franchisee POS terminals. Canary plugs into the same architecture:

1. Corporate signs one deal, adds Canary to approved vendor list
2. Franchisees self-onboard via Marketplace (OAuth, zero friction)
3. Corporate sees cross-location rollup + anonymized benchmarks
4. Network effect compounds

**Why this works:**
- 75% of QSR employees steal at least once
- QSRs lose 4–7% of sales to internal theft
- $3–6B lost annually to restaurant theft
- Most franchises have zero LP plan

**Math:**
- 1 franchise deal × 30 locations = $4.5K MRR
- 5 franchise brands = 150+ merchants fast
- Bypasses the 1-by-1 SMB sales grind entirely

**Targets:** QSR / fast-casual (10–100 locations), bakeries and specialty food concepts, multi-location retail and services.

## Close

**CANARY — EARLY WARNING LP**
**Ship it.**
canary@growdirect.com · Confidential

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-sales-socal-lead-database|SoCal Lead Database]] — prospecting feed
- [[Brain/wiki/growdirect-the-market|The Market]] — 4.5M Square merchants
- [[Brain/wiki/growdirect-the-rollout|The Rollout]] — go-to-market phasing
- [[Brain/wiki/growdirect-revenue|Revenue]] — pricing tiers + unit economics
- [[Brain/wiki/growdirect-competitive-landscape|Competitive Landscape]] — market positioning

## Sources

- `docs/_archive/ip-vault/sales/Canary_Square_Opportunity.pptx` — the source CEO briefing deck (markitdown-extracted)
