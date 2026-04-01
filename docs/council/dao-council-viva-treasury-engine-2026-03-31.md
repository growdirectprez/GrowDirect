# DAO Council Verdict: VIVA Treasury Operations Engine

**Date:** 2026-03-31
**Delegates:** Strategy Roster (5 independent, anonymized peer review)
**Source:** viva-position.md (internal working document)

## Claim-by-Claim Assessment

| # | Claim | Confidence | Consensus | Key Risk |
|---|-------|------------|-----------|----------|
| 1 | Prediction market arbitrage is viable at stated win rates | SPECULATIVE | 5-0 reject stated rates | Polymarket dynamic fees (3.15%) closed latency edge in early 2026; median trader loses 8% annually |
| 2 | DAO Council provides governance layer | CONTESTED | 3-2 (structural merit vs. performative) | Governance latency (minutes) incompatible with execution window (milliseconds); creates fiduciary liability under Wyoming UCC § 17-31-305 |
| 3 | VIVA fits factory pattern as standard app | UNFOUNDED | 5-0 reject | Flask wrong for real-time WebSocket feeds; VIVA needs 5 microservices not 1 monolith; factory validates code not strategy quality |
| 4 | Self-sustaining economics at $600 start | CONTESTED | 4-1 reject at stated scale | Market making requires $100K+ minimum; $12-30/month absolute return doesn't justify engineering effort |
| 5 | Creates compounding data asset | SPECULATIVE | 5-0 agree concept is interesting, 5-0 agree it's unspecified | No mechanism described; reads as post-hoc rationalization for losses |

## Strongest Ground

**Capital sizing discipline.** Starting at 0.01 BTC ($600-1,000) with max 20% at risk is prudent bet-to-learn. Losing it all is a cheap lesson (~10% of total treasury). The willingness to start small and prove before scaling is the right instinct.

## Most Vulnerable Ground

**The entire financial model depends on win rates from a vanished edge.** The 0x8dxd Polymarket bot ($313 to $2.38M) exploited 12-second latency windows that no longer exist. Polymarket introduced dynamic taker fees in early 2026 that exceed typical arbitrage margins. The article is a case study in survivorship bias from a closed window, not a repeatable playbook. Every downstream projection (self-sustaining economics, data asset growth, treasury contribution) inherits this false premise.

## Blind Spot Report

Three critical gaps no individual delegate caught alone:

1. **Money transmission licensing.** VIVA accepting capital, deploying to Polymarket, settling positions, and returning proceeds is payments activity. Federal FinCEN registration (31 USC § 5330) is required regardless of DUNA status. This is a hard legal gate the position doesn't address.

2. **Opportunity cost against Canary.** Every hour on VIVA is an hour Canary doesn't get. Canary is in its critical Year 1 build phase (revenue starts Q3 2026, target 17 merchants for self-sustainability). 200+ engineering hours on VIVA during Q2-Q3 could delay Canary's merchant acquisition at the worst possible time. No delegate fully quantified this trade-off.

3. **Factory validates code quality, not strategy quality.** The nine-stage factory pipeline (TDD, verify, QA) proves the bot works correctly. It does not prove the bot works profitably. A perfect implementation of a losing strategy still loses money. VIVA needs a separate validation layer: live paper trading for 8+ weeks with performance benchmarks, before any real capital is deployed. The factory has no mechanism for this.

## Strategic Recommendation

**Do not approve VIVA as a factory app in Year 1. Approve as a gated research project.**

### Phase 0: Legal Gate (before any code)
- Obtain formal legal opinion on: CFTC swap classification, SEC investment company rules, FinCEN money transmission, Wyoming DUNA activity scope
- Estimated cost: $15-30K + 4-8 weeks
- If any gate fails, VIVA stops here

### Phase 1: Research Prototype (2 weeks, after Canary Q3 stabilization)
- Paper trading only across all four strategies
- No factory pipeline — this is a research spike
- Success criteria: >70% win rate on historical data after fees and slippage

### Phase 2: Live Validation (Q4 2026, 8 weeks)
- Deploy 0.001 BTC (not 0.01) to live markets
- Kill switch at -15% (not -40%)
- Per-strategy position limits: no strategy >30% of deployed capital
- Monthly post-mortem filed to docs/post-mortems/
- Success criteria: consistent $10-30/month for 8+ consecutive weeks

### Phase 3: Factory Graduation (Year 2, if Phase 2 succeeds)
- Formalize into factory app with full scaffold
- Scale to 0.01 BTC
- Treasury Council roster activated for strategy governance
- Only after Canary is stable at 17+ merchants

## Dissenting Views

**Market Analyst (Response D)** reached the strongest negative conclusion: VIVA has "arrived too late" to the Polymarket latency arbitrage opportunity. The edge is structurally closed by dynamic fees. However, cross-exchange arbitrage (Polymarket + Kalshi + emerging platforms) was identified as a potentially more stable opportunity that the position ignores entirely. If VIVA pivots from single-venue latency arb to cross-venue structural arb, the thesis may still hold — but this is a different product than what was proposed.

**Regulatory Counsel (Response C)** issued the hardest stop: the position is "built on a legal misunderstanding" — DUNA status does not equal regulatory cover. This delegate's recommendation (formal legal opinion before any code) should be treated as a hard prerequisite, not a parallel workstream.

## Full Transcript

See: dao-council-viva-treasury-engine-2026-03-31-transcript.md (delegate responses + peer review)
