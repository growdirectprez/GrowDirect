---
screen: /settings/allowlist/comps
title: Allow-List — Comps
role: ADM
wave: W1
origin: O
cp_equivalent: "None"
---

# Allow-List — Comps

**URL:** `/settings/allowlist/comps`  
**Primary role:** ADM  
**Entry points:** Settings nav → Allow-Lists → Comps

**Inherits layout and pattern from `/settings/allowlist/dead-count`.** See that brief for the full screen pattern. Delta documented here.

## Delta from Dead Count Allow-List

**Context panel:** "Comp allow-list entries pre-approve complimentary transaction patterns that would otherwise trigger Q-CO-01 Comp Detection. Use for employee meals, service recovery comps authorized by management, and wholesale demo items that are legitimately given away."

**Rule fed:** Q-CO-01 Comp Detection.

**Key field difference — entry form:**

| Field | Dead Count | Comps |
|---|---|---|
| Threshold override | Max dead count events per shift | Max dollar amount per ticket — blank = no limit |
| Scope | Cashier + Store | Reason Code + Max $ Per Ticket + Authorized Role + Store + Date Range |

Comp allow-list entries are scoped to reason codes and dollar limits: "Reason Code EC (Employee Comp) is approved up to $15.00 per ticket for employees at any store. Amounts > $15 generate an alert regardless of reason code."

The dollar threshold override is the critical constraint: even an authorized comp reason code can be abused if there's no limit. The allow-list enforces the cap.

## UX Callout (delta)

The dollar threshold on comps is the distinction between "service recovery is authorized" and "service recovery as a mechanism for giving away large amounts of merchandise." A $5 comp on a $50 transaction to apologize for a wait is normal; a $200 comp on a $210 transaction to a regular customer is a signal regardless of what reason code was used. The allow-list enforces the dollar boundary automatically, so LP investigators see only comps that exceed the authorized limit.

## Navigation Exits

- `/settings/allowlist/voids` — previous allow-list
- `/settings/store/drawer` — next settings family (LP substrate config)
- `/rules/:id` (Q-CO-01) — rule this allow-list feeds

## Open Questions

None.
