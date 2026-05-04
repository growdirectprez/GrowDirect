---
screen: /otb/settings
title: Open-to-Buy Settings
role: BYR | ADM
wave: W3
origin: N
cp_equivalent: "None — OTB is entirely absent from CP"
---

# Open-to-Buy Settings

**URL:** `/otb/settings`  
**Primary role:** BYR; ADM  
**Entry points:** OTB Dashboard → OTB Settings link; Settings → Planning section

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "OTB Settings", period selector | |
| Tab bar | Budgets / Periods / Approval Thresholds | |
| Tab content | Tab-dependent | |

## Tabs

### Budgets Tab
Table: Category, Store, Budget ($), Period, Notes. Edit inline per row.

**Setting a budget:** BYR clicks a row → edits the Budget field → saves. Budget takes effect immediately for the selected period; committed amounts already on POs are not affected.

**Bulk entry:** For seasonal setup, BYR can use a bulk import (CSV upload) to set budgets across all categories and stores at once. Column format: category_id, store_id, period, budget_amount.

**Unbudgeted categories:** If a category has no budget entry for the current period, it shows as "Unbudgeted" in the OTB dashboard — POs in that category bypass the OTB gate (no approval required, no budget tracking). This is intentional: categories with unpredictable purchasing needs should be excluded from OTB rather than given an arbitrary budget.

### Periods Tab
Define buying periods: name (e.g., "Spring 2026"), start date, end date. A period can span any time window — fiscal month, season, or quarter. Budgets are assigned to periods. Multiple overlapping periods are not recommended but are technically allowed.

**Active period:** The current period (today falls within its date range) is the default shown in the OTB dashboard. Future periods can be set up in advance; past periods are read-only.

### Approval Thresholds Tab
Configure who can approve over-budget POs:
- **Threshold:** Dollar amount over-budget that auto-approves (e.g., POs up to $50 over budget are auto-approved without workflow)
- **MGR authority:** Maximum over-budget amount a Store Manager can approve
- **BYR authority:** Maximum over-budget amount the Buyer can approve
- **Escalation path:** Amounts over BYR authority require ADM approval

Thresholds are per-tenant. Default: no auto-approve, all over-budget requires MGR+ approval.

**Empty state per tab:** "No budgets/periods configured. Click Add to create your first OTB budget."

## Interaction Flows

1. **Spring season setup:** BYR creates a new period "Spring 2026 (2026-03-01 → 2026-06-30)" → switches to Budgets tab → uploads CSV with all category budgets for each store → OTB gate activates for all covered categories
2. **Budget adjustment mid-season:** BYR sees Tropicals sell-through is running hot → opens Budgets tab → increases Tropicals budget by $5,000 → OTB dashboard immediately reflects new Available amount
3. **Approval authority configuration:** ADM sets MGR approval authority to $500 over budget, BYR to $2,000 → any over-budget by more than $2,000 requires ADM sign-off → Pending Approvals queue routes accordingly

## UX Callout

The period + budget + approval threshold configuration is the full machinery behind the OTB gate. Its design priority is to be set up once per season and then invisible to the buyer during normal operation — the OTB panel on the PO creation form and the dashboard handle the daily workflow. Settings are the initial configuration pass, not a screen BYR visits frequently. The approval threshold configuration is the governance layer that gives ADMs control over how much purchasing discretion to delegate to buyers and managers without building a full procurement system.

## Navigation Exits

- `/otb` — back to OTB dashboard

## Open Questions

None.
