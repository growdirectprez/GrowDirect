---
screen: /settings/store/comp-reasons
title: Store Config — Comp Reasons
role: ADM
wave: W1
origin: O
cp_equivalent: "frmpscontrol"
---

# Store Config — Comp Reasons

**URL:** `/settings/store/comp-reasons`  
**Primary role:** ADM  
**Entry points:** Settings nav → Store Config → Comp Reasons

**Inherits layout and pattern from `/settings/store/drawer`.** See that brief for the full screen pattern. Delta documented here.

## Delta from Drawer Threshold

**Context panel:** "This list defines the valid comp reason codes for each store. Comps using reason codes NOT on this list generate a Q-CO-01 Unauthorized Comp Reason alert. Valid reason codes are synced from Counterpoint; ADM can restrict which codes are recognized per store."

**Rule fed:** Q-CO-01 Comp Detection.

**Config field:** Same multi-chip list structure as Void Reasons. Valid comp reason codes per store — enabled/disabled per code per store. Codes synced from CP N-module.

**Cross-reference:** Dollar threshold per comp (above which an alert always fires even for valid reason codes) is set in the Comp Allow-List (`/settings/allowlist/comps`). The reason code list and the dollar threshold are complementary controls: a comp with an invalid reason code is always suspicious; a comp with a valid reason code but a high dollar amount is suspicious if it exceeds the allow-list threshold.

## UX Callout (delta)

Together, the four store config LP threshold screens (Drawer, Discount, Void Reasons, Comp Reasons) form the LP substrate: the data that detection rules evaluate against. A tenant with all four configured is a tenant with full LP coverage. A tenant missing any of them has gaps. The Admin Config Health screen (`/admin/config`) rolls these four up into a single "LP Substrate: complete / missing" indicator — these four settings screens are where ADM fills in the gaps that the health screen flags.

## Navigation Exits

- `/settings/store/void-reasons` — previous store config LP threshold screen
- `/admin/config` — config health rolls up these 4 fields into LP Substrate status

## Open Questions

None.
