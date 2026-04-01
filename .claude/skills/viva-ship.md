---
name: viva-ship
description: |
  VIVA-specific ship — delegates to factory-ship and adds treasury
  operations deployment safety. Phase-aware deployment, paper mode
  enforcement, and kill switch health check.
---

# VIVA Ship

> Delegates to `factory-ship`. Read that skill first.

**Announce:** "Running VIVA ship for [GRO issue]."

## VIVA-Specific Ship Checks

### Pre-Deploy Safety
1. **Phase gate:** Verify deployment matches current phase
   - Phase 1 deploy: VIVA_PAPER_MODE must be true, VIVA_DEPLOYED_CAPITAL_SATS must be 0
   - Phase 2 deploy: VIVA_DEPLOYED_CAPITAL_SATS must be <= 100_000 (0.001 BTC)
   - Phase 3 deploy: Council-approved capital amount
2. **Kill switch health:** Run kill switch smoke test in staging
3. **Config diff:** Compare deployed config against CLAUDE.md requirements
4. **No hot deploys during open positions:** If positions are open, wait for close or manually close first

### Deployment Sequence
1. Deploy API service first (dashboard must stay available)
2. Gracefully stop workers (signal, execution, risk)
3. Run migrations if needed
4. Restart workers
5. Verify health endpoint returns ok
6. Verify dashboard reflects current state

### Rollback Trigger
- Kill switch fires within 5 minutes of deploy → automatic rollback
- Dashboard shows stale data (>5 minutes old) → investigate before proceeding
- Any worker fails to start → rollback, do not run with partial service

After VIVA-specific ship checks, proceed with factory-ship standard process.
