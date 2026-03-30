---
type: research
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Pool Relationship + Solo Mining — The Vertical Integration Thesis
*PhD Research Framework | Layer 5 Deliverable 5 | February 26, 2026*
*Classification: MAXIMUM CONFIDENTIAL*

---

## Thesis Statement

GrowDirect's business model improves at every level of vertical integration between hash rate and inscription. The base case — purchasing block space on the open fee market — is already viable. A mining pool relationship transforms the economics permanently. Solo mining adds asymmetric optionality. The full vertical stack — hash rate to block production to inscription to key custody to validation revenue — is the most capital-efficient deployment path in the Bitcoin inscription economy. Each level up is additive. None is required for the base case to work. All are available.

---

## 1. The Vertical Stack

The El Jeffe system requires one thing from the Bitcoin network: write access. The ability to inscribe data into a block. Today, that access is purchased on the open fee market. But the fee market is not the only path to a block.

**The full stack, from raw input to revenue:**

```
Level 0:  Electricity → Hash Rate
Level 1:  Hash Rate → Block Production (when you win a block)
Level 2:  Block Production → Inscription (your data goes into your block)
Level 3:  Inscription → Key Custody (you hold the keys to the inscribed range)
Level 4:  Key Custody → Validation Gate (anyone who needs proof pays sats)
Level 5:  Validation Revenue → Treasury → More Inscriptions
```

GrowDirect currently operates Levels 3–5. The mining reward from F2Pool (Level 0–1) provided the Genesis Pool, but ongoing inscriptions are purchased on the fee market (Level 2 via market). The vertical integration thesis is about collapsing Levels 0–2 into the same entity.

---

## 2. The Pool Relationship — Permanent Economic Upgrade

### 2.1 How It Works

A mining pool aggregates hash power from many miners and distributes block rewards proportionally when the pool wins a block. The pool operator assembles the block template — deciding which transactions go into each block the pool produces.

If GrowDirect establishes a relationship with a major mining pool — whether through direct participation, hash rate leasing, or commercial partnership — the model upgrades:

- When the pool wins a block, GrowDirect's inscription transactions are included **first, at cost** — before the fee market determines priority
- The fee market competition is eliminated for GrowDirect's transactions
- The cost of inscription approaches the marginal cost of the transaction data itself (effectively zero beyond the pool relationship cost)
- The inscription queue runs continuously — every block the pool wins is another inscription opportunity

### 2.2 The Economic Difference

**Without pool relationship (current state):**

| Component | Cost |
|---|---|
| Inscription fee (200 vbyte tx at 3 sat/vB) | 600 sats per inscription |
| Fee variability | High — spikes to 50–100+ sat/vB during congestion |
| Queue management | Must wait for low-fee windows |
| Throughput | Limited by budget and fee market conditions |

**With pool relationship:**

| Component | Cost |
|---|---|
| Inscription fee | ~0 sats marginal (included in pool's own blocks) |
| Fee variability | Zero — not subject to fee market |
| Queue management | Every block win is a write opportunity |
| Throughput | Limited only by pool's block win rate |

### 2.3 Pool Economics

A top-10 mining pool wins approximately 10–15% of all Bitcoin blocks. At ~144 blocks per day, that is 14–22 blocks per day. Each block provides ~4MB of witness-discounted space for inscriptions.

If GrowDirect's inscription transactions consume a small fraction of each block (a few KB per block for Merkle root inscriptions), the pool's revenue impact is negligible — while the value to GrowDirect is transformative.

**The deal structure:** GrowDirect could offer the pool a share of validation revenue in exchange for priority block inclusion. This aligns incentives: the pool earns ongoing revenue from GrowDirect's success, GrowDirect gets zero-fee inscription access, and both parties benefit from the growth of the notarization protocol.

### 2.4 The Provenance Chain Becomes Unbroken

With a pool relationship, the full provenance chain is under GrowDirect's operational umbrella:

```
Hash rate (leased or contributed)
  → Block production (pool wins block)
    → Inscription (GrowDirect's data inscribed first)
      → Key custody (GrowDirect holds all keys)
        → Validation revenue (sats flow to GrowDirect)
```

Every link in this chain is either controlled by GrowDirect or governed by a direct commercial relationship. No intermediary has discretionary power over the inscription. No fee market determines priority. The path from hash power to revenue is direct, measurable, and permanent.

---

## 3. Solo Mining — The Asymmetric Optionality

### 3.1 The Setup

A single ASIC miner running independently (not connected to a pool) has a very small probability of winning a Bitcoin block. But the expected value calculation is different when block space — not the coin reward — is the prize.

**Current hardware (February 2026):**

| Miner | Hashrate | Cost | Power | Efficiency |
|---|---|---|---|---|
| Antminer S21 Pro | 234 TH/s | ~$5,000–7,000 | 3,510W | 15 J/TH |
| Antminer S21 XP | 270 TH/s | ~$7,000–9,000 | 3,645W | 13.5 J/TH |
| Upcoming U3S23H | 1,160 TH/s | TBD (shipping Feb 2026) | 11,020W | 9.5 J/TH |

**Network hashrate:** ~622 EH/s (622,000,000 TH/s)

### 3.2 The Probability Calculation

For a single S21 Pro (234 TH/s) against a 622 EH/s network:

- Share of network hashrate: 234 / 622,000,000 = 0.0000376%
- Expected blocks per day: 144 × 0.000000376 = 0.0000542
- Expected days between blocks: ~18,450 days (~50.5 years)
- Expected blocks per year: ~0.020

For the upcoming U3S23H (1,160 TH/s):

- Share of network: 1,160 / 622,000,000 = 0.000187%
- Expected blocks per day: 0.000269
- Expected days between blocks: ~3,717 days (~10.2 years)
- Expected blocks per year: ~0.098

### 3.3 Why the Expected Value Calculation Is Different

A traditional miner evaluates solo mining as: expected revenue per day vs. electricity cost per day. At these probabilities, the daily expected revenue is far below the daily electricity cost. Solo mining is "irrational" by traditional metrics.

**GrowDirect's calculation is fundamentally different:**

The prize is not 3.125 BTC in coin revenue. The prize is **full write access to a Bitcoin block with zero fee competition.** A single block win gives GrowDirect:

- ~4MB of witness-discounted inscription space
- Tens of thousands of Merkle root inscriptions in a single block
- All inscriptions at zero marginal fee cost
- Full provenance: "this block was mined by GrowDirect's own hash power"

**Value of a solo-mined block to GrowDirect:**

| Component | Value |
|---|---|
| Block reward (3.125 BTC) | ~$265,000 at $85K BTC |
| Inscription space (at market fee rates) | 10,000–50,000+ Merkle root inscriptions at zero fee |
| Saved inscription fees (at 3 sat/vB) | ~6M–30M sats in fees avoided |
| Provenance value (mined by founder entity) | Incalculable — narrative asset |

The block reward alone more than covers years of electricity. But the real prize — the inscription space and the provenance — has no traditional financial analog. It is infrastructure, minted from hash power, permanently on the chain.

### 3.4 The Optionality Frame

Solo mining for GrowDirect is not a business plan. It is an option. The cost of the option is the electricity to run one ASIC (~$0.07/kWh × 3.51 kW × 24h × 365d = ~$2,150/year for an S21 Pro). The payoff, if the option hits, is a quarter-million dollars in BTC plus unlimited inscription space in a self-mined block.

Traditional miners would call this irrational because the expected value of daily revenue is below daily cost. But GrowDirect is not running a mining business. GrowDirect is running a notarization business that benefits from write access. The ASIC is a lottery ticket where the jackpot includes something no one else is valuing: block space.

**The investor story:** GrowDirect has one ASIC running. The electricity costs $2,150 per year. If it hits a block — even once — the company gets $265,000 in Bitcoin and enough inscription space to extend the Genesis Pool by tens of thousands of canonical records. The probability is low. The payoff is asymmetric. And the narrative — "we mine our own blocks and inscribe our own protocol" — is worth more to a Bitcoin-native investor than the expected value calculation.

---

## 4. The Compounding Moat

### 4.1 Why Vertical Integration Creates Escape Velocity

Each level of vertical integration strengthens every other level:

- **More hash power → more blocks won → more inscription opportunities → larger canonical range → more validation revenue → more capital for hash power**

This is a flywheel. The moat compounds with each revolution:

1. Pool relationship provides zero-fee inscription access
2. Zero-fee access allows aggressive inscription during every block win
3. More inscriptions extend the canonical range
4. Larger range generates more validation revenue
5. More revenue funds deeper pool relationship or additional hash power
6. Return to step 1

A competitor entering the market faces the full accumulated cost of replicating this flywheel — at market fee rates, without pool priority, without provenance, and without the accumulated notarization history.

### 4.2 The Three Moats That Stack

**Moat 1: Temporal (cannot be replicated)**
The Genesis Pool inscriptions exist at specific Bitcoin block heights. Those blocks are mined. They are history. A competitor inscribing today is permanently later.

**Moat 2: Economic (increasingly expensive to challenge)**
Fee rates rise over time (see Fee Window Model). The cost to replicate GrowDirect's position increases with every halving cycle and every increase in block space demand.

**Moat 3: Operational (flywheel advantage)**
Pool relationship + accumulated history + network effect create a cost advantage that widens with scale. GrowDirect inscribes at cost. Competitors inscribe at market rate. The margin difference compounds.

---

## 5. Summary — The Vertical Integration Argument

GrowDirect's base case works without vertical integration: purchase block space on the open fee market, inscribe Merkle roots, charge validation fees. But the business model improves at every level of hash rate integration. A pool relationship eliminates fee market risk and provides predictable inscription access. Solo mining adds asymmetric optionality — a lottery ticket whose jackpot includes write access to the most permanent ledger ever created. The full stack, from electricity to validation revenue, is achievable incrementally and each level compounds the moat. The investor argument is clean: this is the only business model in the Bitcoin ecosystem where mining hash rate feeds directly into a perpetual revenue-generating inscription protocol, and every block won makes the position permanently harder to replicate.

---

*PhD Research Framework | February 26, 2026*
*Output: `_ALX/WorkOrders/output/PhD/PhD_Layer5_VerticalIntegration_Thesis.md`*
*Routes to: Jeremy (pool queue architecture), ALX (investor deck), Syd (regulatory classification of pool relationship)*
