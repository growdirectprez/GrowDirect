---
screen: /settings/store/drawer
title: Store Config — Drawer Threshold
role: ADM
wave: W1
origin: O
cp_equivalent: "frmpscontrol — POS Control (one field among 200; no connection to alert logic)"
---

# Store Config — Drawer Threshold

**URL:** `/settings/store/drawer`  
**Primary role:** ADM  
**Entry points:** Settings nav → Store Config → Drawer Threshold; Admin Config Health → "LP Substrate missing" link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Store Config: Drawer Threshold" | Clear, single-purpose |
| Context panel | What this threshold controls + which rule it feeds | Above the config table |
| Main content | Store threshold table | One row per store |
| Audit trail | Last changed by / when per store | Below table |

## Key Elements

### Context Panel
"This threshold sets the maximum acceptable cash variance in a cashier's drawer before Canary generates a Q-DC-01 Drawer Cash Variance alert. Stores with higher cash volume or busier cash-handling practices may need a higher threshold to avoid excessive false positives."

Rule fed: Q-DC-01. Threshold is required — if blank, Q-DC-01 cannot evaluate this store's transactions and will silently not fire.

### Store Threshold Table
Columns: Store Name, Max Drawer Variance ($), Last Changed By, Last Changed Date.

Edit inline — click a value → enters edit mode → number input → save on blur or Enter key. Each save is audited.

**Empty / missing state:** Stores with no threshold configured show a red "Not Set" badge. This is the LP Substrate missing indicator surfaced in `/admin/config`. Not setting a value = the rule will not fire for this store.

**Default recommendation:** "Industry average: $5–$15 depending on cash volume. High-traffic cash stores may need $20–$25." Shown as helper text below the table.

### Audit Trail
Last 5 changes per store: old value, new value, changed by, timestamp. Collapsible per row. Allows LP manager to trace when a threshold was changed and by whom — relevant if a change coincided with a spike or drop in alerts.

## Interaction Flows

1. **Set threshold for new store:** ADM provisions new store → navigates here → Store 4 shows "Not Set" → ADM sets to $10 → saves → Q-DC-01 can now evaluate Store 4 transactions
2. **Adjust for high-cash store:** LP manager reviews Store 3 alerts → 80% are false positives (Store 3 is a high-volume garden center with frequent cash transactions) → ADM raises threshold from $10 to $20 → alert volume drops to manageable levels
3. **Check before escalating config complaint:** MGR says "we're getting too many drawer alerts at Store 2" → ADM opens this screen → sees Store 2 threshold is $5 → notes that $5 is very tight for their volume → raises to $12 → monitors next week

## UX Callout

Counterpoint's `frmpscontrol` is a 200-field form used primarily by system integrators to configure the POS. The drawer variance threshold is one field on one tab with no label connecting it to any alert behavior. Canary's screen has one purpose: set the threshold, see which rule it feeds, see who changed it last. ADM doesn't need to know where the POS Control form is or what drawer variance even means in CP context. The "Not Set = rule silent" warning is the critical operational guard: a new tenant whose thresholds aren't configured will have no LP coverage, and neither the ADM nor the LP investigator will know without this explicit indicator.

## Navigation Exits

- `/settings/store/discounts` — next store config LP threshold screen

---

**Pattern note:** The three remaining store config LP threshold screens (`/settings/store/discounts`, `/settings/store/void-reasons`, `/settings/store/comp-reasons`) inherit this exact layout and pattern. Each has a different context panel, a different rule reference, and a different configurable field type. Differences are documented in their individual briefs.

## Open Questions

None.
