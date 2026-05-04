---
screen: /settings/store/void-reasons
title: Store Config — Void Reasons
role: ADM
wave: W1
origin: O
cp_equivalent: "frmpscontrol"
---

# Store Config — Void Reasons

**URL:** `/settings/store/void-reasons`  
**Primary role:** ADM  
**Entry points:** Settings nav → Store Config → Void Reasons

**Inherits layout and pattern from `/settings/store/drawer`.** See that brief for the full screen pattern. Delta documented here.

## Delta from Drawer Threshold

**Context panel:** "This list defines the valid void reason codes for each store. Voids using reason codes NOT on this list generate a Q-VO-01 Unauthorized Void Reason alert regardless of the allow-list configuration. Reason codes are synced from Counterpoint via the N-module config sync; ADM can restrict further but cannot add codes that don't exist in CP."

**Rule fed:** Q-VO-01 Void Detection.

**Config field:** Unlike the drawer screen (a single number), this screen manages a list: valid void reason codes per store. Table structure: Store Name, Valid Reason Codes (multi-chip display — codes synced from CP, with enable/disable toggle per code per store).

**Key distinction:** The drawer and discount screens configure thresholds; this screen configures a valid-code whitelist. A void with an unrecognized reason code is always suspicious regardless of amount — this is the mechanism that catches "phantom reason codes" created by someone with CP admin access.

## Navigation Exits

- `/settings/store/discounts` — previous store config LP threshold screen
- `/settings/store/comp-reasons` — next

## Open Questions

None.
