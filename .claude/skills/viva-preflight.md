---
name: viva-preflight
description: |
  VIVA-specific preflight — delegates to factory-preflight and adds
  treasury operations checks. Verifies phase gates, paper mode status,
  legal clearance, and risk parameter sanity before any work begins.
---

# VIVA Preflight

> Delegates to `factory-preflight`. Read that skill first.

**Announce:** "Running VIVA preflight for [GRO issue]."

## VIVA-Specific Checks (on top of factory-preflight)

### Phase Gate Verification
1. Read `Viva/CLAUDE.md` — check current `VIVA_PHASE`
2. If Phase 0 (legal gate): verify legal opinion exists in `docs/legal/viva-regulatory-opinion.md`
   - If missing: STOP. Cannot proceed without legal clearance. File this as a blocker.
3. If Phase 1 (research): verify `VIVA_PAPER_MODE=true` in docker-compose
   - If paper mode is false during research phase: STOP. Fix config.
4. If Phase 2 (validation): verify deployed capital matches approved amount
5. If Phase 3 (factory): proceed with standard factory pipeline

### Risk Parameter Sanity
- `VIVA_KILL_SWITCH_PCT` must be <= 0.15 (not the original -40% from the position doc)
- `VIVA_MAX_POSITION_PCT` must be <= 0.30
- `VIVA_CORRELATION_THRESHOLD` must be <= 0.70
- If any are out of bounds: STOP. Council must approve changes.

### Council Verdict Check
- Check `docs/council/` for most recent VIVA verdict
- If verdict says "do not proceed" or has unresolved blockers: STOP.

### Infrastructure
- Shared stack running (growdirect_postgres, growdirect_valkey, growdirect_ollama)
- VIVA database exists (`viva` / `viva_test`)
- Valkey DB 2 accessible
- No port conflicts on 5003

After all checks pass, proceed with factory-preflight standard checks.
