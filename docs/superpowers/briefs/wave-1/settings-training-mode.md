---
screen: /settings/training-mode
title: Training Mode Toggle
role: ADM | MGR
wave: W1
origin: O
cp_equivalent: "None — CP has no mechanism to suppress LP detection during training"
---

# Training Mode Toggle

**URL:** `/settings/training-mode`  
**Primary role:** ADM; MGR (for their own stores)  
**Entry points:** Settings nav → Training Mode

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Training Mode" | |
| Main content | Store list — one row per store | |
| History panel | Recent training mode events | Below store list |

## Key Elements

### Store List
One row per store. Columns: Store Name, Training Mode Status (ON/OFF badge), Start Date (if ON), End Date (if ON — can be blank for open-ended), Enabled By (user who turned it on), Notes.

Toggle per store: clicking "Enable" opens a configuration modal (see below). Clicking "Disable" confirms and turns off immediately.

**Empty state:** Not applicable — always shows at least one store.

### Enable Training Mode Modal
Fields:
- Start date (defaults to today)
- End date (optional — training mode auto-disables at midnight on this date)
- Notes (free text: who is being trained, which rules are expected to be noisy)

On save: training mode activates for the selected store. All LP rule alerts are suppressed — rules still evaluate transactions and log to the dry-run queue, but no alerts are generated. Configuration is audited.

### Auto-Disable Behavior
If end date is set: system disables training mode automatically at 00:01 on the end date. No manual action required. A day-before reminder appears on the Settings screen: "Training mode for [Store X] ends tomorrow."

### History Panel
Last 10 training mode events across all stores: store name, action (enabled/disabled), actor, start date, end date, notes. Provides audit trail for LP manager to confirm training periods were appropriately bounded.

## Interaction Flows

1. **Enable for onboarding week:** MGR clicks Enable for Store 3 → sets start = today, end = Friday, notes = "New cashier J. Martinez onboarding, rule noise expected on Discount and Void families" → saves → LP alert generation suspended for Store 3 until Friday
2. **Early disable:** Training completed Thursday → MGR clicks Disable → confirmation modal → disabled → LP monitoring resumes immediately
3. **Review history:** LP manager sees an unexpected gap in alerts for Store 5 last week → opens Training Mode → checks history → confirms training mode was active Thu–Fri → alert gap is explained

## UX Callout

Training mode is a safety valve that prevents the system from destroying its own credibility with LP investigators during new-cashier onboarding. Without it, a new cashier's first week generates hundreds of false-positive alerts on voids and discounts — the investigator learns to ignore alerts, and that habit persists long after the training period ends. CP operators had no option but to tolerate this: either they ran all LP detection and got flooded, or they didn't run LP at all. Canary makes training suppression precise (per-store, time-bounded, audited) rather than a binary all-or-nothing decision.

## Navigation Exits

- `/settings/alert-routing` — adjacent settings
- `/rules` — to review which rules will fire when training mode ends

## Open Questions

None.
