---
name: viva-qa
description: |
  VIVA-specific QA — delegates to factory-qa and adds trading domain
  quality checks. Strategy performance validation, risk scenario
  testing, and council audit trail verification.
---

# VIVA QA

> Delegates to `factory-qa`. Read that skill first.

**Announce:** "Running VIVA QA for [GRO issue]."

## VIVA-Specific QA

### Strategy Performance QA
- If paper trading data exists: check win rate against threshold (>70%)
- If win rate < 70%: flag for council review before phase advancement
- Check for outlier trades (P&L > 3 standard deviations from mean)
- Verify no strategy has been running in paper mode for > 8 weeks without review

### Risk Scenario QA
Run these scenarios against the kill switch:
1. **Flash crash:** Simulate -10% BTC drop in 60 seconds. Does kill switch fire?
2. **Correlation cascade:** Two strategies losing simultaneously. Does correlation check fire?
3. **Stale data:** Signal feed goes dark for 30 seconds. Does strategy pause?
4. **Zero liquidity:** Attempt to close position with no counterparty. What happens?

### Council Audit Trail QA
- Every strategy change has a corresponding council_verdict record
- Every phase gate transition has a verdict
- No strategy moved from proposed → live without an approved verdict
- Emergency halts are logged with full context

### Dashboard QA
- Dashboard reflects current portfolio state accurately
- P&L calculations match sum of individual trade records
- Win rate matches actual wins/total from trades table
- No stale data (dashboard updates within 60 seconds of trade)

### What QA Cannot Validate
- Whether the strategy will be profitable in live markets
- Whether the market conditions from paper trading will persist
- Whether the legal opinion (Phase 0 gate) is still current

These are human judgment calls. Flag them for Jeffe's review.

After VIVA-specific QA, proceed with factory-qa standard checks.
