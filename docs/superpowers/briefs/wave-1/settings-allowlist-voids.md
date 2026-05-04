---
screen: /settings/allowlist/voids
title: Allow-List — Voids
role: ADM
wave: W1
origin: O
cp_equivalent: "None"
---

# Allow-List — Voids

**URL:** `/settings/allowlist/voids`  
**Primary role:** ADM  
**Entry points:** Settings nav → Allow-Lists → Voids

**Inherits layout and pattern from `/settings/allowlist/dead-count`.** See that brief for the full screen pattern. Delta documented here.

## Delta from Dead Count Allow-List

**Context panel:** "Void allow-list entries pre-approve specific void reason codes and authorized roles that are expected to generate high void volume without LP investigation. Use for training cashiers, managers with void override authority, and scheduled administrative void procedures."

**Rule fed:** Q-VO-01 Void Detection.

**Key field difference — entry form:**

| Field | Dead Count | Voids |
|---|---|---|
| Threshold override | Max dead count events per shift | Max voids per shift (integer) — blank = no limit |
| Scope | Cashier + Store | Reason Code + Max Per Shift + Authorized Role + Store + Date Range |

Void allow-list entries are scoped to reason codes and authorized roles: "Reason Code MV (Manager Void) is approved for up to 10 voids per shift for any user in the 'Manager' or 'LP Manager' role."

**Role scoping:** Unlike dead-count (per specific cashier), voids can be allow-listed by CP security role — "all users with Manager role." This prevents the allow-list from becoming a per-person exception list for every manager in the system.

## UX Callout (delta)

Void allow-lists are the most operationally sensitive of the four allow-list screens. An overly permissive void allow-list means the rule never fires; an overly restrictive one generates constant false positives for managers doing legitimate administrative voids. The role-scoped approach (vs cashier-specific for dead count) reflects the operational reality: void authority is a role-based permission in CP, so allow-list entries should mirror that.

## Navigation Exits

- `/settings/allowlist/discounts` — previous allow-list
- `/settings/allowlist/comps` — next allow-list
- `/rules/:id` (Q-VO-01) — rule this allow-list feeds

## Open Questions

None.
