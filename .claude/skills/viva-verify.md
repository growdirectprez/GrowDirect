---
name: viva-verify
description: |
  VIVA-specific verify — delegates to factory-verify and adds
  trading domain verification. Kill switch, paper mode, risk
  parameters, and phase gate compliance.
---

# VIVA Verify

> Delegates to `factory-verify`. Read that skill first.

**Announce:** "Running VIVA verify for [GRO issue]."

## VIVA-Specific Verification

### Kill Switch Verification (MANDATORY)
1. Run kill switch unit tests — ALL must pass. No exceptions.
2. Verify kill_switch.py has not been modified without council approval
3. Check that kill switch thresholds match CLAUDE.md (default -15%)
4. Confirm kill switch fires BEFORE trade execution, not after

### Paper Mode Verification
1. If current phase is research or validation: verify VIVA_PAPER_MODE=true
2. Verify paper mode trades are recorded in database
3. Verify paper mode does NOT call external APIs
4. Verify paper mode P&L uses real market prices

### Risk Parameter Verification
1. All strategies have risk envelopes set
2. No strategy exceeds max_position_pct (30%)
3. Kill switch threshold <= 15% on all strategies
4. Correlation monitoring is active if >1 strategy is live

### Phase Gate Compliance
1. Read current VIVA_PHASE from config
2. Verify no code exceeds phase permissions:
   - Phase 1: paper trading only, no external API calls
   - Phase 2: live trading with 0.001 BTC cap
   - Phase 3: full operation within council-approved envelopes

### Data Integrity
1. council_verdicts table is append-only (no UPDATE or DELETE migrations)
2. trades table records are never modified after close
3. All money values stored as integer satoshis, not float

After VIVA-specific verification, proceed with factory-verify standard checks.
