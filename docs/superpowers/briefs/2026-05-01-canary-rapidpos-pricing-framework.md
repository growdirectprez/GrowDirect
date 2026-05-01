# Canary on Counterpoint — Pricing Framework

**Two-tier model: Canary Connect (entry) and Canary Platform (full spine), priced as an enterprise layer above the POS rather than competing with it. Visible recurring license plus a payment-volume revenue split that compounds with customer scale.**

For Tim Mooney · 2026-05-01

---

## Where Canary sits in the comp set

NCR Voyix Commerce Platform at $25/lane/month is priced for the transaction layer — register UI, payment processing, basic store config. Canary is the enterprise layer above it: perpetual ledger, multi-store ops, loss prevention, OTB enforcement, agentic interface. The relevant comp set is LP and multi-store ops platforms, not POS:

| Comp set | Per store / month |
|---|---|
| Tyco / Sensormatic / Accuvision / Agilence (LP analytics at SMB to enterprise tier) | $200 – $700 SMB · $1K – $3K enterprise |
| RetailNext and multi-store inventory analytics | $300 – $800 |
| Zenput / Reflexis store-ops platforms (per module) | $50 – $200 |

Canary's 13-module spine delivers what 4 to 6 of those tools do, on a unified data model.

## Two-tier pricing

| Tier | Phase coverage | License / store / month | Payment-volume rev split | Customer profile |
|---|---|---|---|---|
| **Canary Connect** | Phase 0 — read-side observer, MCP layer | **$75 – $150** | **0.10 – 0.15%** | Three-store pilot, six-month commit, no migration risk |
| **Canary Platform** | Phases 1 – 3 — perpetual ledger, OTB enforcement, MCP gateway, module takeover | **$300 – $600** | **0.20 – 0.30%** | Multi-year production engagement, full spine |

The license is the visible recurring number procurement compares against alternatives. The payment-volume rev split is the compounding tail — small in year 1, dominant by year 3 as the customer base grows. Stripe Connect / Toast economic pattern. Both streams align Canary's incentives with same-store-sales growth.

## Customer LTV at scale — year 1 estimates

| Customer profile | Stores | Avg revenue / store | License y1 | Payment-vol y1 | Total y1 |
|---|---:|---:|---:|---:|---:|
| L&G chain on Connect (Armstrong archetype) | 25 | $5M | $30K | $125K (0.10%) | **$155K** |
| L&G chain on Platform | 25 | $5M | $90K | $250K (0.20%) | **$340K** |
| Multi-vertical specialty on Platform (Murdoch's archetype) | 30 | $7M | $108K | $420K (0.20%) | **$528K** |
| NCR Voyix Commerce reference ($25/lane × 5 lanes × 25 stores) | 25 | — | $37K | $0 | **$37K** |

Canary Platform delivers approximately **10× NCR's per-customer revenue**. Justified by category, not by overlap. Canary is additive to NCR's transaction layer, not competitive with it.

## RapidPOS partnership economics

Three revenue streams for the VAR:

| Stream | VAR take | Cadence |
|---|---|---|
| Customer license | 20 – 30% partner margin on Canary MRR | Recurring monthly |
| Customer payment volume rev split | 20 – 30% partner margin on Canary's split | Recurring with sales |
| Implementation services per phase | 100% to VAR (VAR runs delivery) | One-time per phase |
| Customer support tier 1 + training | 100% to VAR if VAR owns it; Canary handles tier 2 escalation | Recurring or per engagement |

Worked example — L&G chain on Platform tier, year 1:
- Canary platform revenue $340K → VAR partner margin at 25% = **$85K recurring**
- Plus implementation services across the 5-phase migration over 36 months: **$200K – $500K** of one-time services revenue
- Net per-customer LTV with Canary substantially exceeds Counterpoint VAR-only economics, because Counterpoint's per-customer revenue ceiling is largely the implementation fee plus a small ongoing support retainer

## What this is not

- **Not a Counterpoint replacement.** Counterpoint stays as the transaction layer for as long as the customer wants. Phases 0 – 2 require zero Counterpoint changes.
- **Not finalized.** The numbers above are ranges, not commitments. Both customer pricing and the VAR margin structure refine in the partnership conversation that follows the architecture review.

## Inputs that would let us converge on specific numbers

1. Average per-customer LTV across the RapidPOS L&G book today (sets the price ceiling)
2. Whether RapidPOS sells payment processing directly or takes a referral fee from the NCR-side processor (determines whether the payment-volume rev split is even available, or whether RapidPOS already owns it)
3. Average store revenue across the customer base ($3M / $5M / $10M tier)
4. Customer pricing tolerance for layered products — whether anyone in the book has paid $300+/store/month for a non-POS layer before, and what the friction was
