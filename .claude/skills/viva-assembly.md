---
name: viva-assembly
description: |
  VIVA-specific assembly — delegates to factory-assembly and adds
  trading domain implementation patterns. Covers async workers,
  Valkey queue patterns, and paper mode implementation.
---

# VIVA Assembly

> Delegates to `factory-assembly`. Read that skill first.

**Announce:** "Running VIVA assembly for [GRO issue]."

## VIVA Implementation Patterns

### Async Workers (NOT Flask)

Signal and execution workers use Python asyncio, not Flask:

```python
# Pattern for signal worker
import asyncio
import json
import redis.asyncio as aioredis

async def run_signal_worker():
    valkey = await aioredis.from_url("redis://growdirect_valkey:6379/2")

    async def handle_price_tick(data: dict):
        await valkey.xadd("viva:signals:price", data)

    # WebSocket connection loop
    while True:
        try:
            async with connect_websocket() as ws:
                async for message in ws:
                    await handle_price_tick(json.loads(message))
        except Exception:
            await asyncio.sleep(1)  # Reconnect backoff

if __name__ == "__main__":
    asyncio.run(run_signal_worker())
```

### Valkey Queue Pattern

Workers communicate via Valkey streams:

```
viva:signals:price    — Price ticks from CEX feeds
viva:signals:oracle   — Oracle updates
viva:signals:news     — News events
viva:trades:pending   — Trade signals waiting for execution
viva:trades:executed  — Completed trades (for dashboard)
viva:risk:state       — Current risk snapshot (overwritten)
```

### Paper Mode Implementation

Paper mode is NOT "skip the trade." Paper mode is:
1. Evaluate signal → produce TradeSignal (same as live)
2. Check risk envelope (same as live)
3. Record trade in database with `paper_mode=True` (same schema)
4. Calculate P&L using real market prices at the time (same math)
5. DO NOT call external API to place order (only difference)

This means paper mode generates real performance data for validation.

### Satoshi Arithmetic

ALL money values are stored as integers (satoshis). Never use float for money.

```python
# CORRECT
size_sats: int = 100_000  # 0.001 BTC
pnl_sats: int = 1_500     # +1500 sats

# WRONG
size_btc: float = 0.001   # floating point drift
```

Display conversion happens at the dashboard layer only.

### Kill Switch Integration

Every execution path must check kill switch BEFORE placing a trade:

```python
from viva.execution.kill_switch import check_strategy_drawdown, check_portfolio_drawdown

# Before any trade
event = check_strategy_drawdown(strategy.current_drawdown_pct, ...)
if event:
    # Halt strategy, log verdict, alert Jeffe
    return

event = check_portfolio_drawdown(total_deployed, current_value, ...)
if event:
    # Halt ALL strategies, log verdict, alert Jeffe
    return

# Only then execute trade
```

After domain patterns are applied, proceed with factory-assembly standard implementation.
