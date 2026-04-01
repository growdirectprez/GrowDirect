---
name: viva-close
description: |
  VIVA-specific close — delegates to factory-close and adds treasury
  operations post-ship reporting. P&L snapshot, strategy performance
  summary, and council notification.
---

# VIVA Close

> Delegates to `factory-close`. Read that skill first.

**Announce:** "Running VIVA close for [GRO issue]."

## VIVA-Specific Close

### Performance Snapshot
Record at close time:
- Total strategies active / paused / killed
- Portfolio P&L since last ship (satoshis)
- Win rate across all strategies since last ship
- Current phase and any phase gate progress

### Council Notification
If any of these occurred during the sprint:
- Kill switch fired → council must review before next sprint
- Strategy win rate dropped below 70% → flag for council
- New strategy proposed → needs council approval
- Drawdown exceeded 10% → post-mortem required

### Post-Mortem Trigger
If any trade lost >1% of deployed capital:
- Write post-mortem to `docs/post-mortems/YYYY-MM-DD-viva-{description}.md`
- Include: what happened, market conditions, strategy state, kill switch response
- This is mandatory per VIVA CLAUDE.md hard rules

### Memory Bus Update
Record session results to memory bus for cross-app learning:
- Strategy performance data
- Risk parameter effectiveness
- Market condition observations

After VIVA-specific close, proceed with factory-close standard process.
