---
name: viva-tdd
description: |
  VIVA-specific TDD — delegates to factory-tdd and adds trading domain
  test patterns. Covers strategy logic, risk calculations, kill switch
  behavior, and paper mode verification.
---

# VIVA TDD

> Delegates to `factory-tdd`. Read that skill first.

**Announce:** "Running VIVA TDD for [GRO issue]."

## VIVA Test Domain

Trading engines have unique test challenges. Factory TDD validates code
correctness. VIVA TDD must also validate:

### Strategy Logic Tests (unit)
- Entry condition evaluation with known market states
- Exit condition evaluation with known position + market states
- Daily trade limit enforcement
- Risk envelope compliance (position size within max_position_pct)
- Edge cases: zero spreads, negative spreads, missing data, stale signals

### Kill Switch Tests (unit — CRITICAL)
- Per-strategy drawdown triggers at exactly -15%
- Portfolio-wide drawdown triggers at exactly -15%
- Correlation detection with known correlated loss sequences
- Single-loss threshold triggers
- Kill switch CANNOT be overridden by strategy logic
- Kill switch fires even if council hasn't voted
- Kill switch fires in paper mode (for validation)

### Risk Calculation Tests (unit)
- Position exposure percentage calculated correctly
- Drawdown percentage calculated correctly from peak
- P&L calculation with fees and slippage
- Satoshi arithmetic — no floating point for money

### Paper Mode Tests (integration)
- Paper mode trades don't hit external APIs
- Paper mode trades ARE recorded in database
- Paper mode P&L IS tracked (for validation data)
- Switching from paper to live requires explicit config change
- Live mode is impossible if VIVA_PAPER_MODE=true

### Council Verdict Tests (integration)
- Verdict creates append-only record
- Strategy status changes on approval/rejection
- Risk envelope updates on council decision
- Emergency halt creates verdict + pauses all strategies

### Signal Processing Tests (unit)
- Signal model stores correctly
- Stale signal detection (configurable age threshold)
- Malformed payload handling (don't crash on bad data)

### What You CANNOT Test Locally
- Real market latency and slippage
- Actual API connectivity to Polymarket/Binance
- Strategy profitability in live markets
- Multi-day drawdown patterns

For these, use the Phase 1/2 paper trading period as the test environment.
Log everything. Post-mortem monthly.

### Test Fixtures

```python
# conftest.py patterns for VIVA

@pytest.fixture
def sample_strategy(db_session):
    """A paper-mode latency arb strategy with default risk envelope."""
    ...

@pytest.fixture
def market_state_bullish():
    """Market state: BTC up 0.6% in 30 seconds, Polymarket lagging."""
    return {
        "cex_price": 84500.00,
        "prediction_price": 0.50,  # 50-50 odds, hasn't repriced
        "spread": 0.15,
        "latency_ms": 3200,
    }

@pytest.fixture
def market_state_crash():
    """Market state: BTC down 5% in 2 minutes, flash crash."""
    ...
```

After domain-specific tests are written, proceed with factory-tdd standard checks.
