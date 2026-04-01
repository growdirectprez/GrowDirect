---
name: viva-blueprint
description: |
  VIVA-specific blueprint — delegates to factory-blueprint and adds
  treasury operations domain context. Plans strategy modules, signal
  integrations, risk parameters, and council review triggers.
---

# VIVA Blueprint

> Delegates to `factory-blueprint`. Read that skill first.

**Announce:** "Running VIVA blueprint for [GRO issue]."

## VIVA Domain Context

VIVA is an agentic treasury operations engine. It has four layers:

1. **Signal Layer** — WebSocket feeds from CEX, prediction markets, oracles, news
2. **Strategy Engine** — Modules that evaluate signals and produce trade signals
3. **Execution Layer** — Order management, position tracking, risk monitoring
4. **Council Layer** — Strategy approval, risk envelope governance, performance review

### Blueprint Must Address

For any feature touching the **Signal Layer**:
- Which data source? (binance, coinbase, polymarket, kalshi, chainlink, news)
- What signal type? (price_tick, oracle_update, news_event, contract_update)
- What's the expected throughput? (ticks/second)
- Does it run as the signal-worker service or as a Flask endpoint?
- How does it write to Valkey? (stream key, format)

For any feature touching the **Strategy Engine**:
- Which strategy type? (latency_arb, oracle_arb, news_driven, market_maker, cross_venue_arb)
- Does it extend `BaseStrategy`?
- What's the signal input schema?
- What are the entry/exit conditions?
- What are the testable invariants? (these become TDD targets)

For any feature touching the **Execution Layer**:
- Paper mode behavior — what happens differently?
- Kill switch interaction — does this change risk state?
- Position tracking updates — real-time or batch?
- Valkey queue interaction — producer or consumer?

For any feature touching the **Council Layer**:
- What triggers council review? (new strategy, risk change, drawdown, schedule)
- What's the verdict format? (strategy_approval, risk_envelope_change, etc.)
- Is the verdict stored in council_verdicts table?

### Phase-Aware Planning

- **Phase 1 (research):** Only paper trading features. No live execution code.
- **Phase 2 (validation):** Paper + live with 0.001 BTC cap. Kill switch mandatory.
- **Phase 3 (factory):** Full feature set. Scale to 0.01 BTC.

### Key Constraint

VIVA's Flask service is dashboard/API only. Workers (signal, execution, risk)
are separate asyncio processes. Blueprint must specify WHICH service a feature
targets. Never put real-time processing in Flask request handlers.

After domain context is applied, proceed with factory-blueprint standard output.
