---
date: 2026-04-29
type: founder-intent
status: active
classification: confidential
tags: [meter-model, token-plan, payroll-to-revenue, l402, monetization, saas, bitcoin-standard, canary]
last-compiled: 2026-04-29
needs-review: 2026-07-29
---

**Wiki:** [[Brain/Home|Home]] · [[Brain/wiki/cards/ilwac-extended-bitcoin-standard|IL(Device/MCP/Port/)WAC]] · [[Brain/wiki/cards/canary-cost-center-cross-charge|Cost Center Cross-Charge]]

# Canary Meter Model — Token Plan and Payroll-to-Revenue

> **Scope.** Founder intent and architectural direction. The meter model is the monetization logic of the platform. Not yet fully implemented. Captures the design decision before it evaporates.

---

## The Problem With SaaS Seat Pricing

Seat pricing has no relationship to value delivered. A retailer paying for 10 seats gets the same bill whether Canary recovered $50K in shrink or did nothing. The platform's revenue is decoupled from the merchant's outcome. That is a misalignment the merchant will eventually notice and resent.

Per-transaction pricing couples revenue to volume, not value — a high-volume, low-margin retailer pays more than a low-volume, high-margin one, regardless of what the platform actually improved.

---

## The Model

**Every account gets a token plan (fixed allocation) and a budget ceiling (L402 wallet).**

The base tier is predictable and plannable. The merchant knows their cost floor before a single endpoint is called. No surprise bills. No usage anxiety below the threshold.

**The meter — variable billing above the base plan — runs on one ratio: payroll to revenue.**

| Billing layer | Mechanism | Merchant control |
|---|---|---|
| Token plan | Fixed allocation per billing period | Choose plan tier |
| Budget ceiling | L402 wallet funded to the ceiling | Finance funds the wallet |
| Meter (variable) | Runs on payroll/revenue ratio improvement | Improve the ratio, meter earns |

---

## Why Payroll-to-Revenue

Payroll-to-revenue is the one ratio that:

1. **Touches every module.** Labor scheduling (L) affects payroll. Shrink recovery (Q/E) affects revenue retention. OTB efficiency (M) affects margin. ILWAC accuracy (V) affects cost basis. Every module's work either improves or degrades the ratio.

2. **Aligns platform and merchant revenue.** The platform wins when the merchant wins. If payroll/revenue does not improve, the meter does not run hard. No outcome, no overage bill.

3. **The CIO and CFO read the same ledger.** The CIO controls endpoint spend (the token plan). The CFO tracks payroll/revenue (the ratio that runs the meter). Same system, same unit, same hash chain.

4. **It is not gameable by volume.** A high-volume retailer with a bad payroll/revenue ratio does not generate more meter revenue than a low-volume retailer who has tightened the ratio. Value delivered drives billing, not throughput.

---

## IT Project Self-Funding

The payroll/revenue meter solves the IT ROI problem structurally.

**Project costs are in satoshis from day one.** Every MCP call, every agent action, every endpoint used during implementation debits the project wallet. The wallet balance is the project cost — live, sealed, not reconstructable after the fact.

**Results are in satoshis from the same system.** Shrink recovery, OTB savings, labor efficiency gains — all measured through the ILWAC layer, the Fox case evidence chain, and the payroll/revenue ratio tracked by the meter. Same unit, same sealing, same source of truth.

**Net position is real-time.** Project wallet outflows = endpoint fees (cost). Inflows = meter credits from ratio improvement (return). The ROI model is not a deck — it is a wallet balance with a hash chain behind every line.

This is the SI firm's differentiation: run a Canary-backed transformation project and the client sees real-time ROI, not a post-hoc justification built to survive a CFO review six months after go-live.

---

## Franchise Application

Franchisors set the payroll/revenue target as a brand standard. The meter enforces it commercially.

| Franchisee performance | Billing outcome |
|---|---|
| Beats the brand standard ratio | Earns credits against the next billing period |
| Hits the brand standard ratio | Pays the base plan only |
| Misses the brand standard ratio | Pays the overage (meter runs above base) |

The fee schedule is the brand standard. Compliance is no longer a reporting exercise — it is a billing outcome.

---

## Subscription Expansion Model

Once Canary is a SaaS with revenue covering ops, the token plan model scales outward:

- **Square merchants** added back at a square-specific token plan tier
- **Fujitsu POS customers** on a port-specific plan (Port = Fujitsu connector)
- **ACE Hardware network** on a franchise-tier plan (franchisor sets the fee schedule)
- **Any POS source** that registers a RaaS connector endpoint gets a plan tier

The base infrastructure is POS-agnostic. The token plan is the commercial layer that organizes which sources pay which rates. Adding a new POS source is adding a new Port dimension and pricing it.

---

## What Does Not Exist Yet

- Payroll data integration (Module L — labor data — is Phase 6+)
- Payroll/revenue ratio computation engine (requires L + V data joined)
- Meter trigger on ratio improvement (billing logic not implemented)
- Token plan management surface (account setup, plan tier selection)
- L402 wallet per account funded to budget ceiling (Goose exists; account-level scoping not implemented)

The design pass that produces GRO tickets for these items has not happened.

---

## Related

- [[Brain/wiki/cards/ilwac-extended-bitcoin-standard|IL(Device/MCP/Port/)WAC]] — the cost model the meter reads
- [[Brain/wiki/cards/canary-cost-center-cross-charge|Cost Center Cross-Charge]] — the intra-account fee layer below the meter
- [[Brain/wiki/canary-franchise-play|Franchise Play]] — franchise meter application
- [[Brain/wiki/cards/platform-thesis|Platform Thesis]] — the three accountability rails this meter enforces
- `docs/sdds/canary/goose.md` — L402 payment middleware (settlement mechanism)
