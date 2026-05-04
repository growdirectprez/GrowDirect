---
screen: /loyalty/members
title: Loyalty Members
role: MGR | BYR | LP
wave: W4
origin: O
cp_equivalent: "CP customer lookup — no loyalty KPIs, no points balance, no tier assignment view"
---

# Loyalty Members

**URL:** `/loyalty/members`  
**Primary role:** MGR; BYR; LP  
**Entry points:** Loyalty dashboard → Members link; customer detail → loyalty tab link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Loyalty Members", export button | |
| Filter bar | Tier, LP Flag, Enrollment date, Points balance range | |
| Main content | Members table | |

## Key Elements

### Members Table
Columns: Member ID, Name, Tier, Enrolled Date, Points Balance, Last Transaction Date, 12-Month Spend ($), Redemption Count, LP Flag indicator.

**LP Flag indicator:** A yellow flag icon appears when the member has an open LP alert or active case involving loyalty-member transactions. LP can filter to "LP Flagged" to see all flagged members in one view.

**Points Balance:** Current unredeemed balance. High points balances can indicate hoarding (planning a large redemption) or accumulated earnings from high transaction volume.

**12-Month Spend ($):** From the Customer Commercial tab, pulled into the members list for BYR's segmentation work. Allows BYR to segment by spend tier for targeted communications.

### Member Click-Through
Clicking any member navigates to `/customers/:id` — the full customer record. All tabs (Risk, Context, Commercial, AR, Loyalty) are available from there. The loyalty members list is a filtered view of the customer database with loyalty-specific columns surfaced.

### Export
BYR exports the member list for external campaign tools (email marketing, print, etc.). Export includes member ID, tier, spend, and points balance. PII fields (name, email) are included. No LP data exported — LP flags are Canary-internal only.

**Empty state:** "No loyalty members enrolled."

## Interaction Flows

1. **Tier targeting:** BYR filters to Gold tier → 47 members → exports → sends targeted spring event invitation to Gold-tier customers only
2. **Large balance monitoring:** BYR filters Points Balance > 10,000 → 8 members with large balances → evaluates whether to nudge redemption (drives store visits) or let balances accumulate
3. **LP member audit:** LP filters LP Flagged → 6 flagged members → reviews each: 4 have open cases, 2 have resolved alerts — removes flag from the 2 resolved → opens customer records for the 4 with open cases

## UX Callout

The loyalty members list is the intersection of the merchandising module and the customer record — same underlying customer data, filtered to loyalty-enrolled accounts, with loyalty-specific columns. The LP flag column is the thread from loyalty to loss prevention: loyalty program fraud (fabricating transactions to earn points, colluding with cashiers on point manipulation) is a real theft vector that sits in the loyalty module, not the transaction exception module. Having the LP flag visible to BYR and MGR means the people who manage the loyalty program are also aware of its LP exposure — they don't need to wait for LP to report it.

## Navigation Exits

- `/customers/:id` — from member row click
- `/loyalty` — back to loyalty dashboard
- `/loyalty/settings` — program configuration

## Open Questions

None.
