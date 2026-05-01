---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: laptop-side Claude Code (this conversation OR a fresh laptop session) — drives mini deployment via SSH
priority: high
phase: 1 of 5 in NCR Counterpoint retail spine integration
prerequisite: Phase 0 foundation dispatch must be complete (Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md retargeted for laptop-driven execution)
sdd: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
build-plan: docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md
modules: [T, R, F, L, N]
inputs:
  - SDD §6.1 (Module T), §6.2 (Module R), §6.3 (Module N), §6.8 (Module F), §6.12 (Module L)
  - Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/ — Counterpoint REST API repo
  - Brain/wiki/canary-tsp-pipeline.md, Brain/wiki/canary-data-model.md
  - Existing wiki for each module: canary-module-{n,t,r,f,l}.md (some may need creation)
tags: [canary, ncr-counterpoint, priority-modules, phase-1, ssh-driven]
---

# Dispatch — NCR Counterpoint Phase 1: Priority Modules (T R F L N)

## Operational discipline (read first)

Executes on the laptop. Mini is the eventual production target via SSH (per `project_sandbox_vs_mini_separation` memory). Mini is not running this dispatch — laptop is. Founder reviews at every gate. No production deployment until Phase 5 (cutover).

## Why this exists

Phase 0 establishes the TSP+CRDM+adapter shell. Phase 1 brings the **five priority spine modules** to production-ready: every retailer needs them, they're highest data-volume + highest data-value, and they unblock detection (Phase 4) and operations (Phase 3).

**Modules in this phase:**

- **N — Device** (stores, stations, device config)
- **T — Transactions** (sales tickets, returns, voids — the data backbone)
- **R — Customer** (customer entity, history, segmentation)
- **L — Labor / Workforce** (employees, time clock)
- **F — Finance** (payments, tenders, taxes, day-end)

**Sequence within phase:**

```
Sub-phase 1a:  N (Device)         ◄── prerequisite for T, R, L (all are store/station-context)
                       │
Sub-phase 1b:  T, R, L (parallel) ◄── each can use N populated; T+R+L feed Phase 4 (Q)
                       │
Sub-phase 1c:  F (Finance)        ◄── needs T's tender detail
```

## Pre-flight reading (required before any code)

Before touching code:

1. Master SDD `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — read §1–7 (architecture, source-of-truth, auth, CRDM alignment, ARTS alignment, cross-cutting concerns) AND §6.1, 6.2, 6.3, 6.8, 6.12 (per-module sections for T R N F L)
2. Master build plan `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` — Phase 1 row + acceptance criteria
3. Phase 0 dispatch outcome (when available) — adapter shell + CRDM extensions in place
4. Counterpoint API endpoint docs for the priority endpoints:
   - **N**: `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Endpoints/GET_Store.md`, `GET_Store_Station.md`, `GET_Device_Config.md`, `GET_StoresTokenized.md`, `GET_StoreTokenizeInfo.md`
   - **T**: `GET_Document.md` + any other Document* endpoints (sales tickets, returns, voids — verify in Endpoints/)
   - **R**: `GET_Customer.md`, `GET_Customers.md`, `GET_Customers_EC.md`, `GET_Customer_Address.md`, `GET_Customer_Note.md`, `GET_Customer_OpenItems.md`, `GET_CustomerControl.md`
   - **F**: `GET_PayCode.md`, `GET_PayCodes.md`, `GET_GiftCard.md`, `GET_GiftCards.md`, `GET_GiftCardCode.md`, `GET_GiftCardCodes.md` (plus tax endpoints — scan Endpoints/ for Tax* entries)
   - **L**: scan `Endpoints/` for Employee* / Timeclock* / Schedule* (may not exist via REST per SDD §6.12 open question)

Produce a one-page pre-flight summary covering: confirmed endpoint list per module, any gaps vs SDD's hypothesized endpoints, auth/key requirements per endpoint group.

## Scope clarification questions ALXjr asks BEFORE starting code

Surface these and wait for founder answers:

1. **Module L coverage** — does Counterpoint expose Employee + Timeclock via REST in the version we're targeting? If NOT, is L sourced from a separate system (e.g., a workforce-management tool) and Counterpoint contributes only what's in Roles/RoleUsers? Or is L deferred from Phase 1?
2. **Tax detail level** — are tax authority + rate detail required in Phase 1, or is aggregate per-transaction tax sufficient until Phase 5?
3. **Multi-tier customer pricing** — does this surface in Module R (CustomerControl tier field) or in Module P (Phase 2)? Phase 1 R captures the tier ID; Phase 2 P captures the tier semantics. Confirm the boundary.
4. **Test environment** — NCR provides a test database via `files165.cyberlynk.net` per their README. Do we provision one, or use a customer's sandbox, or pure mocks for Phase 1?
5. **Timeline** — is Phase 1 a single commit window, or modular gates per sub-phase (1a → 1b → 1c)? Default: modular gates with founder review between sub-phases.

Wait for founder answers. Do not improvise.

## Operating procedure

### Sub-phase 1a — Module N (Device)

1. Read SDD §6.3 + Counterpoint Store/Station/Device endpoint docs
2. Implement TSP adapter for Store / Station / Device_Config endpoints
3. CRDM mapping: Places.stores, Places.stations, Places.devices
4. MCP tool surface: `get_stores`, `get_store(id)`, `get_store_stations(store_id)`, `get_device_config(store_id, station_id)`
5. Test: fixture-based against public Counterpoint API surface
6. Wiki: update `Brain/wiki/canary-module-n-device.md` with Counterpoint-mapping section
7. Founder review gate

### Sub-phase 1b — Modules T, R, L (in parallel where safe)

For each module:

1. Read SDD section + Counterpoint endpoints
2. Implement TSP adapter (build on N's foundation — every event/customer/employee has a store + station context)
3. CRDM upserts (idempotent, keyed on Counterpoint primary keys)
4. MCP tool surface (per SDD §6.1, 6.2, 6.12)
5. Test: fixture-based, including edge cases for the open questions above
6. Wiki update
7. Founder review gate per module

**Module T specifics:**
- Document* endpoint family — verify line-item granularity (nested vs separate endpoint)
- Void-of-sale vs return distinction
- Backfill capability for historical sync (timestamp-filtered)

**Module R specifics:**
- Customer + Customer_Address + Customer_Note as a unified entity with sub-records
- CustomerControl for tier + B2B flags
- Customer_OpenItems for AR balance (touches F too, scope cleanly)

**Module L specifics:**
- Verify endpoint availability first (open question above)
- If REST endpoints are absent: scope L to "what Roles/RoleUsers exposes" + flag deferred work
- If REST endpoints exist: full Employee + Timeclock implementation

### Sub-phase 1c — Module F (Finance)

1. Read SDD §6.8 + PayCode + GiftCard + Tax endpoints
2. Implement TSP adapter — depends on T (transactions provide tender + tax detail per ticket)
3. CRDM upserts: Events.payments, Events.taxes, Events.gift_card_transactions
4. MCP tool surface: `get_payments`, `get_tax_summary`, `get_gift_card_balance`, `get_day_end_close`
5. Test: fixture suite covering all tender types + tax scenarios
6. Wiki update: `Brain/wiki/canary-module-f-finance.md`
7. Founder review gate

## Cross-cutting work (within this phase)

- **Auth bootstrap** — establish per-customer credential storage pattern (per SDD §3); rotation via `docs/audit-2026-04-23/secret-rotation-runbook.md`
- **Sync telemetry table** — CRDM `sync_telemetry` for per-endpoint timestamp + record count (per SDD §7.4)
- **Error-handling middleware** — 401/403/404/429/5xx handling per SDD §7.2
- **Pagination wrapper** — skip/take per SDD §7.3
- **Multi-version support** — version detection via `DB_CTL.DB_VER` (per Counterpoint README); Canary's adapter switches behavior on detected version (v8.5 / v8.6)

## Out of scope (do NOT do)

- Do NOT touch downstream Canary modules (Chirp, Fox, analytics, dashboards) — that's Phase 4 and beyond
- Do NOT integrate against the Boutique H&G chain's specific Counterpoint instance — Phase 1 builds against the public API surface; customer-specific deployment is Phase 5
- Do NOT spec or implement Phase 2-5 modules in this dispatch. Stay scoped.
- Do NOT deviate into free-form exploration. If scope ambiguity arises, surface it for founder decision and wait.
- Do NOT commit code without founder review per phase. Each sub-phase is a review gate.

## Acceptance criteria (Phase 1 program-level)

Per module (N, T, R, L, F):

- [ ] CRDM mapping confirmed against actual Counterpoint API responses
- [ ] TSP adapter implemented + integration-tested (fixture or NCR sandbox)
- [ ] At least one MCP tool surface exposed per SDD §6
- [ ] Fixture suite: happy path + 5 edge cases
- [ ] Wiki article updated with Counterpoint-mapping section
- [ ] Founder review approved

Phase-level:

- [ ] All five priority modules complete per per-module criteria
- [ ] Cross-cutting work landed (auth, telemetry, error handling, pagination, multi-version)
- [ ] Phase 1 wrap-up document produced summarizing decisions made + open questions surfaced for Phases 2-4
- [ ] SDD updated if Phase 1 work surfaced corrections (e.g., open questions answered, endpoint mappings refined)
- [ ] Memory-bus chunked for the SDD (per-module recall enabled — depends on memory-bus drift fix being in place)

## Reporting cadence

- Sub-phase checkpoint at end of 1a, 1b (per module), 1c. Founder reviews.
- Surface blockers immediately. Do not grind through ambiguity.
- Report format per checkpoint: one-page status — modules done, modules in flight, blockers, decisions that need founder input.

## Risks (Phase-1 specific, beyond program-level in build plan)

- **Module L gap** — if Counterpoint doesn't expose timeclock via REST, L is partially deferred
- **Tax complexity** — tax detail in Counterpoint may require multiple endpoints to fully model; F may exceed initial scope estimate
- **Customer + tier modeling** — multi-tier customer pricing has historically been a B2B-heavy area in Counterpoint deployments; CRDM model may need extension
- **Document granularity** — if Counterpoint nests line items differently than expected, T adapter complexity grows

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — companion SDD (read §6.1, 6.2, 6.3, 6.8, 6.12)
- `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` — Phase 1 row in the build plan
- `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — Phase 0 foundation (prerequisite)
- `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — source corpus
- `Brain/wiki/canary-module-n-device.md`, `canary-module-r-customer.md`, `canary-module-f-finance.md`, `canary-module-l-labor.md` — per-module wikis (verify Module T wiki exists; create if missing)
- `docs/audit-2026-04-23/secret-rotation-runbook.md` — per-customer credential rotation procedure

---

**Dispatch author:** Senior ALX (laptop), 2026-04-25
**Executor:** Laptop-side Claude Code (this conversation OR a fresh laptop session)
**Review gate:** Founder reviews pre-flight summary, scope answers, and each sub-phase output before next sub-phase begins
