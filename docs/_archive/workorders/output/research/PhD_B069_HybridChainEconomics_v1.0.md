---
type: research
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Hybrid Chain Economics: Cost-Per-Receipt Model
## Avalanche Subnet + Bitcoin Ordinals — Research Brief B-069

**Author:** PhD (Research Framework)
**Date:** March 1, 2026
**Classification:** MAXIMUM CONFIDENTIAL — Internal R&D only
**Status:** DELIVERED
**Manifesto:** IV.4 (Scaling Model), V.5 (Chain Architecture)

---

## GUARDRAIL ACKNOWLEDGMENT

This is R&D only. The current production architecture (pure Bitcoin Ordinals via OrdinalsBot + Lightning via Strike) is unchanged. This document models economics for Jeffe's strategic decision-making. Nothing in this brief gates Sprint 6 or modifies any active work order.

---

## Executive Summary

Pure per-event Bitcoin inscription is economically nonviable at any meaningful merchant scale. However, **global Merkle batching** (one inscription per day covering all merchants) makes the Genesis Pool viable for 13-68 years of daily anchoring. The hybrid model — Avalanche for real-time receipt finality, Bitcoin for periodic anchoring — delivers sub-second merchant UX at 84-92% gross margin on current pricing tiers. The break-even question is not cost but **finality latency**: pure Ordinals with daily batching imposes a 24-hour confirmation delay that the product cannot tolerate. Hybrid solves this at negligible incremental cost.

**The headline number:** At 1,000 merchants on the hybrid model with a private Avalanche subnet, annual chain costs are approximately $78,600 — against $468,000 in subscription revenue at the $39/mo tier. That is 83% gross margin before any operational cost.

---

## Assumptions

| Parameter | Value | Source |
|---|---|---|
| BTC price | $85,000 | Conservative estimate, March 2026 |
| 1 satoshi | $0.00085 | Derived from BTC price |
| AVAX price | $10 | CoinMarketCap March 2026 (~$9-12 range) |
| Merchant avg transactions/day | 200 | Square SMB median (coffee/retail) |
| Merkle root content size | 32 bytes (SHA-256 hash) | Standard |
| Inscription tx overhead | ~150-200 vbytes total | Bitcoin Optech tx size calculator |
| Low fee rate | 2 sat/vByte | 2025 quiet-period average |
| Medium fee rate | 10 sat/vByte | 2025 normal-period average |
| High fee rate | 50 sat/vByte | Congestion periods |
| Avalanche C-Chain tx cost | $0.005 | Post-Octane upgrade, March 2026 |
| Avalanche private subnet tx cost | $0.001 | Self-configured gas on own subnet |
| Genesis Pool | 0.1 BTC = 10,000,000 sats | B-050 |

---

## SCENARIO A — Pure Bitcoin Ordinals (Current Design)

### A.1: Individual Inscription Per Event (Baseline — Worst Case)

Each merchant event gets its own Bitcoin inscription.

| Metric | Low Fee (2 sat/vB) | Med Fee (10 sat/vB) | High Fee (50 sat/vB) |
|---|---|---|---|
| Cost per inscription (200 vB tx) | 400 sats / $0.34 | 2,000 sats / $1.70 | 10,000 sats / $8.50 |
| Per merchant/year (73K events) | $24,820 | $124,100 | $620,500 |
| **100 merchants/year** | **$2,482,000** | **$12,410,000** | **$62,050,000** |
| **1,000 merchants/year** | **$24,820,000** | **$124,100,000** | — |
| **10,000 merchants/year** | **$248,200,000** | — | — |

**Verdict:** Economically nonviable at any scale. A single merchant at medium fees costs more per year than the entire subscription revenue at the $79/mo tier ($948/year). Individual inscription is not a product.

### A.2: Merkle Batch — Hourly (Per Merchant)

Each merchant's events batched into a Merkle tree every hour. One inscription per merchant per hour.

| Metric | Low Fee | Med Fee | High Fee |
|---|---|---|---|
| Inscriptions/merchant/year | 8,760 | 8,760 | 8,760 |
| Cost/merchant/year | $2,978 | $14,892 | $74,460 |
| **100 merchants** | **$297,840** | **$1,489,200** | — |
| **1,000 merchants** | **$2,978,400** | **$14,892,000** | — |
| **10,000 merchants** | **$29,784,000** | — | — |

**Verdict:** Still nonviable as a per-merchant inscription model. At 100 merchants with medium fees, chain costs exceed total revenue.

### A.3: Merkle Batch — Daily (Per Merchant)

One inscription per merchant per day.

| Metric | Low Fee | Med Fee | High Fee |
|---|---|---|---|
| Inscriptions/merchant/year | 365 | 365 | 365 |
| Cost/merchant/year | $124 | $621 | $3,103 |
| **100 merchants** | **$12,410** | **$62,050** | **$310,250** |
| **1,000 merchants** | **$124,100** | **$620,500** | **$3,102,500** |
| **10,000 merchants** | **$1,241,000** | **$6,205,000** | — |

**Verdict:** Viable at low fees for small scale. Breaks at 1,000+ merchants or medium+ fees. Not scalable.

### A.4: Global Merkle Batch — Daily (All Merchants, Single Inscription)

The key optimization: all merchant Merkle roots aggregated into a single root-of-roots tree. **One Bitcoin inscription per day regardless of merchant count.** Individual merchants verified via Merkle proof path.

| Metric | Low Fee | Med Fee | High Fee |
|---|---|---|---|
| Inscriptions/year (total, all merchants) | 365 | 365 | 365 |
| Annual Bitcoin cost (ALL merchants) | **$124** | **$621** | **$3,103** |
| Cost per merchant (100 merchants) | $1.24 | $6.21 | $31.03 |
| Cost per merchant (1,000 merchants) | $0.12 | $0.62 | $3.10 |
| Cost per merchant (10,000 merchants) | $0.01 | $0.06 | $0.31 |

**Verdict:** Economically excellent. Bitcoin anchoring at $621/year for unlimited merchants. But: **24-hour finality delay.** The merchant cannot verify their receipt against Bitcoin until the daily batch commits. This is the latency problem that drives the hybrid model.

### A.5: Genesis Pool Viability (Pure Ordinals)

Genesis Pool: 0.1 BTC = 10,000,000 sats.

| Strategy | Low Fee (400 sats/inscription) | Med Fee (2,000 sats) | High Fee (10,000 sats) |
|---|---|---|---|
| Total inscriptions affordable | 25,000 | 5,000 | 1,000 |
| Years of daily global batching | 68.5 years | 13.7 years | 2.7 years |
| Years of hourly global batching | 2.85 years | 0.57 years | 0.11 years |

**Key finding:** Under global daily batching, the Genesis Pool funds **13-68 years** of Bitcoin anchoring. The pool is viable — but only if the batching strategy is global (one inscription/day for ALL merchants) rather than per-merchant.

The "10 million Ordinals" framing should be reinterpreted: the Genesis Pool funds **the inscription budget**, not 10 million individual mints. Under stacked inscription (Directive 3), the pool funds thousands of merchant gLog address activations plus decades of append operations.

---

## SCENARIO B — Hybrid (Avalanche Subnet + Bitcoin Rollup)

### B.1: Architecture Overview

```
Merchant Event → elJeffe API Gateway
    ↓
Sub 1: PostgreSQL evidence seal (milliseconds)
    ↓
Avalanche Private Subnet: receipt minted as on-chain event (sub-second finality)
    ↓ (configurable frequency)
Merkle Aggregation: all receipts since last anchor
    ↓
Bitcoin Ordinal: Merkle root inscribed (10-min Bitcoin finality)
    ↓
Receipt complete: Avalanche TX hash (instant) + Bitcoin inscription ID (deferred)
```

### B.2: Avalanche Receipt Layer — Cost Model

**Shared C-Chain (public Avalanche network):**

| Merchants | Events/Year | Cost/Event | Annual Cost |
|---|---|---|---|
| 100 | 7,300,000 | $0.005 | $36,500 |
| 1,000 | 73,000,000 | $0.005 | $365,000 |
| 10,000 | 730,000,000 | $0.005 | $3,650,000 |

**Private Avalanche Subnet (GrowDirect validator):**

| Merchants | Events/Year | Cost/Event | Annual Cost |
|---|---|---|---|
| 100 | 7,300,000 | $0.001 | $7,300 |
| 1,000 | 73,000,000 | $0.001 | $73,000 |
| 10,000 | 730,000,000 | $0.001 | $730,000 |

Gas fees on a private subnet are self-configured. GrowDirect sets the gas price. The $0.001 estimate is conservative — on a fully owned subnet with no external validators, effective cost approaches the hardware amortization only.

### B.3: Bitcoin Anchor Layer — Cost Model

Using global daily batching (Scenario A.4):

| Frequency | Inscriptions/Year | Annual Bitcoin Cost (Med Fee) |
|---|---|---|
| Daily | 365 | $621 |
| Hourly | 8,760 | $14,892 |
| Every 10 min (per Bitcoin block) | 52,560 | $89,352 |

For Tier 1-3 pricing, daily anchoring at $621/year is sufficient. Hourly anchoring adds $14,271 — still negligible against revenue.

### B.4: Validator Operations — Cost Model

Post-Avalanche9000 (ACP-77, live December 2024):

| Item | Annual Cost | Notes |
|---|---|---|
| Subnet validator staking | $0 on Primary Network | ACP-77 eliminated 2,000 AVAX requirement |
| Self-defined subnet staking | Minimal (GrowDirect defines) | Can be 1 AVAX or custom token |
| Server hardware (dedicated) | $2,400-4,800 | 16GB RAM, 8-core, 1TB SSD, 5Mbps |
| Bandwidth + hosting | $1,200-2,400 | Co-located or cloud VM |
| Redundancy (2nd validator) | $2,400-4,800 | Production minimum: 2 validators |
| **Total validator ops** | **$6,000-12,000/year** | Conservative estimate |

**Critical update:** The Avalanche9000 upgrade (December 2024) eliminated the 2,000 AVAX staking requirement for subnet validators. This removes the ~$20,000 capital lockup that previously gated subnet deployment. GrowDirect can launch a private subnet with minimal AVAX exposure.

### B.5: Total Hybrid Cost — Combined

| Merchants | Avalanche (Private Subnet) | Bitcoin (Daily Anchor) | Validator Ops | **Total Annual** |
|---|---|---|---|---|
| 100 | $7,300 | $621 | $10,000 | **$17,921** |
| 1,000 | $73,000 | $621 | $10,000 | **$83,621** |
| 10,000 | $730,000 | $621 | $10,000 | **$740,621** |

### B.6: Revenue vs. Cost — Margin Analysis

At $39/mo (Standard tier):

| Merchants | Annual Revenue | Annual Chain Cost | **Gross Margin** |
|---|---|---|---|
| 100 | $46,800 | $17,921 | **62%** |
| 1,000 | $468,000 | $83,621 | **82%** |
| 10,000 | $4,680,000 | $740,621 | **84%** |

At $79/mo (Pro tier):

| Merchants | Annual Revenue | Annual Chain Cost | **Gross Margin** |
|---|---|---|---|
| 100 | $94,800 | $17,921 | **81%** |
| 1,000 | $948,000 | $83,621 | **91%** |
| 10,000 | $9,480,000 | $740,621 | **92%** |

**The margin improves with scale because the Bitcoin anchor and validator costs are fixed, while Avalanche per-tx costs are fractions of a penny.**

---

## SCENARIO C — Lightning-Only (Current Strike Design)

Lightning Network is a payment channel protocol, not a data inscription layer. It cannot:

- Store arbitrary data permanently on-chain
- Provide a canonical notarization record
- Serve as an event receipt layer
- Offer Merkle-verifiable proof of event occurrence

Lightning IS the correct payment rail for L402 validation gate (sat collection). It IS the correct settlement layer for Strike-based wallet funding. It is NOT a substitute for either Bitcoin Ordinals (permanent anchoring) or Avalanche (real-time receipts).

**Verdict:** Lightning occupies a complementary role — it collects the sats. It does not mint, seal, or notarize.

---

## DIRECTIVE 1: User-Defined Inscription Frequency — Five-Tier Model

The merchant selects their Bitcoin anchoring SLA. Avalanche handles real-time for all tiers — every event hits the subnet instantly regardless of tier. The tier controls how often the Merkle root gets committed to Bitcoin.

### Cost Curve Per Merchant Per Year (at 10 sat/vB medium fee)

| Tier | Name | Bitcoin Frequency | BTC Cost Share/Merchant (1K merchants) | Avalanche Cost/Merchant | Total Chain Cost | Subscription | Margin |
|---|---|---|---|---|---|---|---|
| 1 | Entry | Annual | $0.002 | $73 | $73 | $228/yr ($19/mo) | 68% |
| 2 | Standard | Daily | $0.62 | $73 | $74 | $468/yr ($39/mo) | 84% |
| 3 | Pro | Hourly | $14.89 | $73 | $88 | $948/yr ($79/mo) | 91% |
| 4 | Enterprise | Per-block (~10 min) | $89.35 | $73 | $162 | Custom (est $199/mo) | 93% |
| 5 | Realtime | Per-event | $124,100* | $73 | $124,173* | Custom premium | N/A |

*Tier 5 per-event Bitcoin inscription is included for completeness only. It is not a viable offering except for extremely high-value, low-volume use cases (legal filings, regulatory submissions). Even then, batching at 1-minute intervals is preferable.*

**The pricing architecture maps cleanly:** Avalanche cost is flat across all tiers (~$73/merchant/year on private subnet). The variable cost is Bitcoin anchoring frequency. Higher tiers pay more for faster Bitcoin finality. The product markup covers the Avalanche flat cost + Bitcoin variable cost + margin.

### Merkle Tree Behavior Across Tiers

- **Tier 1 (Annual):** Merchant events accumulate for 365 days. One Merkle tree. One Bitcoin inscription. Any event is verifiable via proof path, but only after the annual commit.
- **Tier 2 (Daily):** Tree seals every 24 hours. Events verifiable against Bitcoin within one business day.
- **Tier 3 (Hourly):** Tree seals every hour. Near-real-time Bitcoin verification for any event.
- **Tier 4 (Per-block):** Tree seals every ~10 minutes (every Bitcoin block). Practical maximum for batch anchoring.
- **Tier 5 (Per-event):** No batching. Individual inscription per event. Extreme premium.

**In all tiers, the Avalanche receipt is instant.** The tier only governs Bitcoin finality. The merchant always gets an Avalanche TX hash in sub-second time. The Bitcoin inscription ID follows on the tier-defined schedule.

---

## DIRECTIVE 2: Chain-Agnostic Minting — Cost Differential

Same Merkle root inscribed on different chains:

| Destination | Cost Per Inscription | Finality | Permanence |
|---|---|---|---|
| Bitcoin Ordinal only | $1.70 (med fee) | ~10 min (1 confirmation) | Permanent — proof-of-work immutability |
| Avalanche Subnet only | $0.001 | Sub-second | Permanent while subnet operates (validator-dependent) |
| Dual-chain (both) | $1.70 | Sub-second (AVAX) + 10 min (BTC) | Maximum — both guarantees |
| Avalanche C-Chain (public) | $0.005 | Sub-second | Permanent while Avalanche network operates |

### Dual-Chain Anchoring at Scale

| Merchants | Frequency | BTC Cost/Year | AVAX Cost/Year | Dual Total | Single-chain BTC | Single-chain AVAX |
|---|---|---|---|---|---|---|
| 1,000 | Daily batch | $621 | $73,000 | $73,621 | $621 | $73,000 |
| 1,000 | Hourly batch | $14,892 | $73,000 | $87,892 | $14,892 | $73,000 |
| 10,000 | Daily batch | $621 | $730,000 | $730,621 | $621 | $730,000 |

**Key insight:** The dual-chain premium is negligible. Bitcoin anchoring at daily frequency adds only $621/year regardless of merchant count. The Avalanche cost dominates. Running dual-chain costs essentially the same as Avalanche-only, while gaining Bitcoin's proof-of-work permanence guarantee.

**The recommendation is always dual-chain.** There is no economic reason to run Avalanche-only. The Bitcoin anchor is too cheap to omit.

---

## DIRECTIVE 3: Stacked Inscriptions (Reinscription) on a Single Satoshi

### Protocol Status

**Reinscription is a supported Ordinals protocol feature since September 11, 2023.** It allows inscribing additional data onto an already-inscribed satoshi. The new data appends chronologically alongside existing data. Combined with recursive inscription, this enables infinite append-only data on a single sat.

Post-Jubilee (block 824,544), all reinscriptions receive positive inscription numbers ("blessed"). There are no protocol-level size limits on the number of reinscriptions per sat — only the standard Bitcoin transaction size limits apply per individual inscription (~400KB witness data maximum per transaction, ~4MB block weight limit).

### The gLog Address Model

Under reinscription, each merchant receives ONE satoshi as their permanent gLog address:

```
Satoshi #[ordinal_number] → Merchant "Offset Coffee" gLog address

  Inscription 0: gLog genesis (protocol header, merchant_id, activation timestamp)
  Inscription 1: Merkle root — Day 1 (200 events)
  Inscription 2: Merkle root — Day 2 (187 events)
  Inscription 3: Merkle root — Day 3 (215 events)
  ...
  Inscription N: Merkle root — Day N
```

The satoshi IS the account. The inscriptions ARE the ledger entries. The serialization order IS the timeline. The private key IS the proof of ownership.

**Transferability:** Sell the business, transfer the sat. New owner receives the complete, immutable, chronologically ordered history of every event ever recorded. No migration. No database export. No trust required. The chain is the record.

### Cost Model — Stacked vs. New-Sat Inscriptions

| Operation | Cost (Med Fee, 10 sat/vB) | Notes |
|---|---|---|
| New inscription on new sat | ~2,000 sats ($1.70) | Standard: 200 vB tx |
| Reinscription on existing sat | ~2,000 sats ($1.70) | Same tx structure — no discount |
| Initial gLog activation (genesis) | ~2,000 sats ($1.70) | One-time per merchant |
| Each subsequent Merkle root append | ~2,000 sats ($1.70) | Per-frequency-tier schedule |

**Reinscription does not reduce per-append transaction cost.** Each append is a new Bitcoin transaction with the same fee structure. The savings are structural, not transactional:

1. **Address permanence:** The sat never changes. No new UTXO creation for each merchant batch.
2. **Data locality:** All merchant history on one sat — queryable by ordinal number.
3. **Transferability:** Business sale = single sat transfer. Entire history moves atomically.
4. **Namespace scarcity:** Early gLog addresses on low ordinal numbers become premium (like low IP addresses or short domain names).

### Revised Genesis Pool Math — Stacked Model

The Genesis Pool (0.1 BTC = 10,000,000 sats) under reinscription:

| Allocation | Sats | Purpose |
|---|---|---|
| gLog address activation (10,000 merchants × 2,000 sats) | 20,000,000 | **Exceeds pool** — need 0.2 BTC for 10K merchants |
| gLog address activation (5,000 merchants × 2,000 sats) | 10,000,000 | Uses entire pool for activation only |
| gLog address activation (1,000 merchants × 2,000 sats) | 2,000,000 | 20% of pool — leaves 8M sats for appends |
| Remaining for appends (8M sats ÷ 2,000 per append) | 4,000 appends | ~10.9 years of daily global batching |

**Recommended allocation (1,000-merchant Phase 2 target):**

| Item | Sats | % of Pool |
|---|---|---|
| 1,000 merchant gLog activations | 2,000,000 | 20% |
| Daily global Merkle root appends (5,000 days = 13.7 years) | 5,000,000 | 50% (at low fees) |
| Reserve (fee spikes, additional merchants) | 3,000,000 | 30% |
| **Total** | **10,000,000** | **100%** |

Under hybrid model, the Bitcoin cost is only the daily global batch append — one reinscription per day on a designated "master gLog" sat, plus periodic per-merchant reinscriptions at the tier-defined frequency.

**The Genesis Pool is viable under the stacked/hybrid model.** It funds 1,000 merchant activations plus 13+ years of daily anchoring with 30% reserve.

### Patent Implications — Route to Syd

Stacked reinscription on a single satoshi as a permanent, transferable, append-only business ledger address is a novel application not present in any existing Ordinals use case. This strengthens:

- **Claim 2 (key custody):** Custody of the sat IS custody of the business record
- **Claim 5 (Merkle batching):** Each reinscription is a Merkle root — the sat accumulates roots chronologically
- **New potential claim:** Transferable business identity via satoshi transfer, wherein the complete operational history is atomically conveyed with the cryptographic asset

**Flag for Syd:** Review reinscription-as-business-address for dependent claim in utility filing.

---

## BREAK-EVEN ANALYSIS

### Question 1: At what merchant scale does pure Ordinals become economically nonviable?

Per-event inscription: nonviable at 1 merchant.
Per-merchant daily batch: nonviable above ~500 merchants at medium fees (cost exceeds $39/mo subscription).
Global daily batch: **never nonviable** — cost is fixed at $621/year regardless of merchant count.

The constraint is not cost but **latency**. Global daily batching imposes 24-hour finality delay. Acceptable for Tier 1 (annual) and Tier 2 (daily). Unacceptable for Tier 3+ (hourly/real-time).

### Question 2: At what scale does the Avalanche subnet validator cost justify itself vs. shared C-Chain?

| Metric | Shared C-Chain ($0.005/tx) | Private Subnet ($0.001/tx + $10K ops) |
|---|---|---|
| 100 merchants (7.3M events) | $36,500 | $17,300 |
| 500 merchants (36.5M events) | $182,500 | $46,500 |
| **Break-even** | **~35 merchants** | Subnet cheaper above ~35 merchants |
| 1,000 merchants | $365,000 | $83,000 |

The private subnet breaks even at approximately **35 merchants** (where the 5x per-tx savings exceed the $10K fixed validator cost). Above 35 merchants, the subnet saves progressively more.

### Question 3: What is the break-even where hybrid becomes cheaper than pure Ordinals?

This question inverts. Pure Ordinals (global daily batch) is always cheaper in raw chain cost ($621/year vs. $83K+ for hybrid at 1,000 merchants). But pure Ordinals cannot deliver real-time receipts.

The correct frame: **hybrid is the only model that delivers the product.** The merchant needs instant receipt confirmation. Pure Ordinals with daily batching cannot provide it. The hybrid cost ($83K at 1,000 merchants) is not compared against pure Ordinals — it is compared against subscription revenue ($468K at 1,000 merchants on the $39 tier). At 82% margin, the hybrid model is the product.

### Question 4: Does the Genesis Pool become viable under hybrid batching?

**Yes.** Under hybrid with stacked inscriptions:

- Avalanche handles real-time receipts (funded by subscription revenue, not the Genesis Pool)
- Bitcoin anchoring via reinscription on master gLog sat: ~2,000 sats/day (daily batch)
- Genesis Pool funds: 1,000 merchant activations (2M sats) + 13.7 years of daily anchoring (5M sats) + 30% reserve (3M sats)

The Genesis Pool was never meant to fund 10 million individual inscriptions. It funds the **address space** — the permanent gLog namespace on Bitcoin — plus decades of anchoring operations. Under the hybrid model, the pool is not just viable; it is generous.

---

## SUMMARY TABLE — All Three Scenarios at 1,000 Merchants

| Metric | A: Pure Ordinals (Global Daily) | B: Hybrid (Subnet + BTC Daily) | C: Lightning Only |
|---|---|---|---|
| Real-time receipt | No (24h delay) | Yes (sub-second) | No (not a data layer) |
| Annual chain cost | $621 | $83,621 | N/A |
| Bitcoin permanence | Yes | Yes | No |
| Merchant UX | Poor (delayed confirmation) | Excellent (instant + permanent) | N/A |
| Revenue at $39/mo | $468,000 | $468,000 | N/A |
| Gross margin | 99.9% (but unusable product) | 82% (shippable product) | N/A |
| Genesis Pool viability | 13-68 years | 13-68 years (BTC layer) | N/A |
| Scalability ceiling | Latency-limited | Subnet-limited (horizontal scaling) | N/A |

---

## RECOMMENDATIONS FOR JEFFE

1. **The hybrid model is the product.** Pure Ordinals global batching is economically elegant but fails the UX test — merchants need instant confirmation. Hybrid delivers both instant UX and Bitcoin permanence.

2. **Launch the private subnet early.** Post-Avalanche9000, the barrier is $10K/year in hardware — not $20K+ in staked AVAX. The subnet breaks even at 35 merchants and saves $282K/year at 1,000 merchants vs. shared C-Chain.

3. **Reframe the Genesis Pool.** The pool funds the gLog address space (1,000 merchant activations) plus decades of Bitcoin anchoring. The "10 million Ordinals" language should evolve to "10 million satoshi address slots in the verification namespace" — which is accurate under stacked reinscription.

4. **Price tiers map to Bitcoin frequency.** Avalanche is flat-cost across all tiers. Bitcoin frequency is the variable. This makes the pricing model clean and the margin expansion predictable.

5. **Always run dual-chain.** The Bitcoin anchor costs $621/year regardless of merchant count. There is no economic case for Avalanche-only. Dual-chain is default.

6. **Route to Syd:** Reinscription-as-transferable-business-address is a novel patent claim. Stacked Merkle roots on a single sat as a business identity primitive has no prior art in the Ordinals ecosystem.

---

*PhD | Research Framework | March 1, 2026*
*B-069 Hybrid Chain Economics — Deliverable 1 of 2*
*R&D only. Current architecture unchanged.*
