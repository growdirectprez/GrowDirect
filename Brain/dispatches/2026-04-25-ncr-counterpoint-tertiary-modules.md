---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: laptop-side Claude Code
priority: medium-high (Q is Canary core)
phase: 4 of 5 in NCR Counterpoint retail spine integration
prerequisite: Phase 3 operations modules (D J) complete; Phases 1+2 must also be complete (Q depends on T R F L N + S substrate)
sdd: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
build-plan: docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md
modules: [A, C, Q]
inputs:
  - SDD §6.4 (A), §6.6 (C), §6.5 (Q)
  - All Phase 1+2+3 outputs (Q depends on rich event data; A + C depend on Customer + Item data)
  - Brain/wiki/ncr-counterpoint-document-model.md §"Audit log" + §"Original document references"
tags: [canary, ncr-counterpoint, tertiary-modules, phase-4, a, c, q]
---

# Dispatch — Phase 4: Tertiary Modules (A C Q)

## Operational discipline

Executes on the laptop. **Q is Canary's core module** — this phase is where the loss-prevention layer activates. Q depends on Phase 1 (T R N F L) + Phase 2 (S) + Phase 3 (D J) being populated; without that substrate, Q has nothing to detect against. A and C are derived modules with light Counterpoint coverage.

## Why

Tertiary modules close out spine coverage:
- **A — Asset Management** (derived from Item flags; no dedicated endpoints)
- **C — Commercial / B2B** (derived from Customer fields; tier + AR + terms)
- **Q — Loss Prevention** (Canary core; substrate = all prior phases' CRDM events)

**Sub-phase sequence:** 4a (A) → 4b (C) → 4c (Q). A and C are quick (derived); Q is the heaviest sub-phase in the entire build.

## Pre-flight reading

1. SDD §6.4 (A), §6.5 (Q), §6.6 (C)
2. `Brain/wiki/ncr-counterpoint-document-model.md` — §"Audit log" + §"Original document references" (Q substrate: PS_DOC_AUDIT_LOG, PS_DOC_HDR_ORIG_DOC, PS_DOC_LIN_PRICE pricing-rule trail)
3. `Brain/wiki/ncr-counterpoint-api-reference.md` — Store config thresholds (MAX_DISC_AMT, MAX_DISC_PCT, USE_VOID_COMP_REAS) + category margin targets (MIN_PFT_PCT, TRGT_PFT_PCT)
4. `Brain/wiki/garden-center-operating-reality.md` §"vendor / grower side" — Q rules must allow-list cash-vendor-payments (legitimate, not fraud)
5. Existing Canary loss-prevention rule catalog (path: `Brain/wiki/canary-detection.md` if available; else equivalent in Canary repo)

## Scope clarification questions ALXjr asks BEFORE code

1. **Q rule catalog source** — is Canary's existing detection-rule catalog suitable as-is, or does it need Counterpoint-specific tuning? (Canary's existing rules were built for Square; Counterpoint substrate is richer — audit log per Document, multi-authority tax breakdown, drawer-session correlation, line-level pricing rules.)
2. **A scope depth** — how deep does Asset Management coverage need to be? Tracking non-saleable items as derived from IM_ITEM with status flags — sufficient for Phase 4? Full asset lifecycle (depreciation, maintenance, retirement) is out of POS scope.
3. **C scope depth** — B2B / commercial coverage derived from Customer fields. Sufficient if Module R already captured tier + AR + terms? Or does C need additional surface (custom B2B reporting, account-management workflows)?
4. **Garden-center allow-listing** — Q detection rules need allow-list patterns for legitimate cash-vendor-payments + manual-entry data noise + item-code drift. How are these encoded — rule parameters, separate allow-list table, both?

## Operating procedure

### Sub-phase 4a — Module A (Asset Management — derived)

1. Read SDD §6.4 + Item endpoint surface for asset-flag patterns
2. CRDM mapping (derived): `Things.assets` — view over `Things.items` filtered by ITEM_TYP / status / non-saleable flags
3. TSP adapter: no new endpoint polling — purely a CRDM materialization layer over Module S data
4. MCP tool surface: `get_assets()`, `get_asset(id)` — derived views
5. Wiki: update `Brain/wiki/canary-module-a-asset-management.md`
6. Founder review gate (light)

### Sub-phase 4b — Module C (Commercial / B2B — derived)

1. Read SDD §6.6 + Customer / Customer_OpenItems endpoints (already covered in Phase 1 R)
2. CRDM mapping (derived): `People.commercial_accounts` (filtered Customer view), `Workflows.purchase_orders_by_account`, `Events.ar_aging`
3. TSP adapter: no new endpoint polling — derives from Modules R + J data
4. MCP tool surface: `get_commercial_accounts()`, `get_account_balance(customer_id)`, `get_account_purchase_history(customer_id)`, `get_ar_aging_by_account()`
5. Test: fixture suite with B2B scenarios (landscaper accounts, monthly invoicing, terms-based collection)
6. Wiki: update `Brain/wiki/canary-module-m-merchandising.md`
7. Founder review gate

### Sub-phase 4c — Module Q (Loss Prevention — Canary core)

This is the heaviest sub-phase. Detailed work:

1. Read SDD §6.5 + Document audit log + original-doc references + Store config thresholds + category margin targets
2. CRDM mapping (Canary-internal): `Events.detections`, `Events.alerts`, `Configs.detection_rules`, `Configs.allow_lists`
3. **Counterpoint substrate consumption** — Q rules read against:
   - `Events.transactions` + nested lines (suppressed-sale, void patterns, refund-without-original)
   - `Events.audit_log_entries` (per-Document audit trail; user / drawer / station / timestamp on every state change)
   - `Events.pricing_decisions` (markdown abuse, manual-override patterns)
   - `Events.payments` (tender-mix anomalies, cash-vs-card patterns)
   - `Things.item_categories.MIN_PFT_PCT/TRGT_PFT_PCT` (margin-anchored thresholds — out-of-the-box, no tribal-knowledge config)
   - `Places.stores.PS_STR_CFG_PS.MAX_DISC_*` (per-store discount caps)
   - `People.employees.USR_ID` from Documents (employee-on-ticket; Module L is gappy in Counterpoint but Document.USR_ID + SLS_REP still link transactions to API users)
4. **Counterpoint-specific rule extensions** (beyond Canary's Square-side rules):
   - **Cash-vendor-payment allow-list** — Documents with PayCode CASH on vendor-side workflows (RECVR with cash payment) classified separately from sale-side fraud
   - **Drawer-session anomalies** — DRW_SESSION_ID + cash-drawer reconciliation patterns
   - **Multi-authority tax discrepancies** — PS_DOC_TAX rows that don't match expected jurisdiction stack (catch tax-evasion or misconfiguration)
   - **Mix-and-match abuse** — MIX_MATCH_COD usage that produces below-cost margins
   - **Item-code drift signal** — when items churn rapidly without clear reason
5. **Garden-center allow-listing** — encoded in `Configs.allow_lists` (vertical-aware): cash-vendor-payment, manual-entry noise tolerance, item-code drift baseline
6. MCP tool surface: `query_detections(rule, date_range, store?)`, `get_detection_detail(detection_id)`, `list_active_rules()`, `tune_rule_threshold(rule_id, params)`, `get_allow_list(rule_id)`
7. Test: fixture suite with positive (real fraud signatures) + negative (legitimate operations that look fraud-like — cash-vendor-payments, manual-entry typos, garden-center-specific flat pricing)
8. Wiki: update `Brain/wiki/canary-module-q-loss-prevention.md` with Counterpoint substrate consumption + Counterpoint-specific rules + garden-center allow-listing
9. Founder review gate (heavy)

## Cross-cutting work (within this phase)

- **Allow-list framework** — vertical-aware. Garden-center allow-list ≠ general retail. Configurable per-tenant.
- **Substrate-consumption pattern** — Module Q is the first downstream consumer of CRDM at scale. The pattern (read CRDM events, apply detection rules, write detections back) becomes the template for future Canary modules.
- **Rule tuning surface** — operators need to adjust thresholds based on customer-specific reality. MCP tools expose this for the agent layer.

## Out of scope

- New Counterpoint endpoint integration — Q reuses substrate from Phases 1-3
- Module L native build (workforce / scheduling) — that's option (d), separate strategic decision
- Module W native build — same
- Customer-specific Q tuning — happens during Phase 5 cutover per-customer

## Acceptance criteria

Per module:
- [ ] A (derived): CRDM view + MCP tools
- [ ] C (derived): CRDM views + MCP tools + B2B fixture suite
- [ ] Q: detection rule catalog adapted for Counterpoint substrate; Counterpoint-specific rules added (cash-vendor allow-list, drawer-session anomalies, multi-authority tax discrepancies, mix-match abuse); garden-center allow-list framework; fixture suite (positive + negative)
- [ ] All three modules: wiki articles updated

Phase-level:
- [ ] Allow-list framework documented + tested
- [ ] Substrate-consumption pattern documented as reusable
- [ ] Rule tuning surface exposed via MCP

## Risks (Phase 4 specific)

- **Q complexity** — adapting Canary's existing detection rules to Counterpoint's richer substrate is real engineering. Risk: time-budget overrun. Mitigate by phasing within 4c (start with Counterpoint-equivalent of existing Square rules; add Counterpoint-specific rules incrementally).
- **Garden-center allow-listing** — requires real-customer data to tune. Initial allow-lists from public domain knowledge; refine during Phase 5 cutover.
- **Rule false-positive rate** — Counterpoint substrate is richer = more potential signals = higher false-positive risk if rules aren't tuned. Plan: dry-run mode for first weeks of customer deployment, tune before alerts fire.

## Reporting cadence

Sub-phase checkpoint at 4a, 4b, 4c. Founder review heaviest at 4c (Canary core).

## Related

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — §6.4, §6.5, §6.6
- `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` — Phase 4 row
- `Brain/dispatches/2026-04-25-ncr-counterpoint-operations-modules.md` — Phase 3 (prerequisite)
- `Brain/wiki/ncr-counterpoint-document-model.md` — audit log + original doc + pricing-decision substrate
- `Brain/wiki/ncr-counterpoint-api-reference.md` — Store config thresholds + category margin targets
- `Brain/wiki/garden-center-operating-reality.md` — allow-list domain reality

---

**Dispatch author:** Senior ALX (laptop), 2026-04-25
**Executor:** Laptop-side Claude Code
**Review gate:** Founder review at each sub-phase; heaviest at 4c (Canary core)
