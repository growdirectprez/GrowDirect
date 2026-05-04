---
screen: /loyalty
title: Loyalty Dashboard
role: MGR | BYR
wave: W4
origin: O
cp_equivalent: "CP loyalty module — minimal; no tier management, no program-level analytics, no LP risk view"
---

# Loyalty Dashboard

**URL:** `/loyalty`  
**Primary role:** MGR; BYR  
**Entry points:** Primary sidebar nav (Marketing section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Loyalty", date range selector | |
| Top section | Program KPI tiles | |
| Main content | Tier performance table + enrollment trend | |
| Right rail | Recent activity feed | |

## Key Elements

### Program KPI Tiles
Five tiles:
- **Active Members:** Loyalty members who've transacted in the last 90 days
- **New Enrollments (period):** New members in the selected date range
- **Redemption Rate (%):** % of loyalty transactions that included a reward redemption
- **Avg Points Balance:** Average unredeemed point balance per active member
- **Program Revenue Contribution ($):** Net sales from loyalty transactions vs non-loyalty (proxy for program lift)

### Tier Performance Table
If a tiered loyalty program is configured (e.g., Silver / Gold / Platinum): one row per tier. Columns: Tier Name, Member Count, Avg Annual Spend, Avg Points Balance, Redemption Rate, Upgrade Rate (% of members who moved up a tier in the period), LP Risk (% of members with LP flags in the period).

**LP Risk column on tiers:** A loyalty tier where 15% of members have active LP flags is an abnormal concentration. High-tier members with LP flags are a specific risk pattern — loyalty program abuse (earning points through fraudulent transactions, redeeming against illegitimate purchases). The tier view surfaces this concentration without requiring LP to query individual member records.

### Recent Activity Feed
Real-time feed of loyalty events: new enrollments, tier upgrades, large point redemptions, and LP flags raised against loyalty-member transactions.

**Large redemption events:** Redemptions above a configured point threshold appear in the feed with a flag. A member redeeming 5,000 points ($50 value) is normal; a member redeeming 50,000 points ($500 value) in one transaction warrants a look, especially if the points were earned in an unusual pattern.

**Empty state:** "No loyalty program configured. Add a loyalty program in Loyalty Settings to enable this dashboard."

## Interaction Flows

1. **Monthly program review:** BYR opens loyalty dashboard → 340 active members, 12% redemption rate, program contributing 38% of net sales → healthy program → identifies Gold tier has 3x the redemption rate of Silver → considers Silver upgrade incentive
2. **LP tier risk check:** LP opens dashboard → Platinum tier LP Risk = 18% → queries member list with LP flags → finds 4 Platinum members with open cases → reviews redemption history for each
3. **Enrollment analysis:** MGR opens dashboard → enrollment trend chart shows sharp spike in enrollments 2 weeks ago → correlates with in-store promotion → promotional enrollment acquisition was effective

## UX Callout

CP's loyalty module, where it exists, is a points ledger — balance in, balance out. Program-level analytics (tier performance, redemption rates, LP risk concentration) don't exist in CP. Canary's loyalty dashboard is the operator view of whether their investment in loyalty program management is paying off, and whether the loyalty program is being used as a fraud vehicle (a non-obvious risk that brick-and-mortar operators rarely think about until it's too late). The LP Risk column on the tier table is an example of LP intelligence embedded in a non-LP screen: a buyer reviewing loyalty program health sees the LP signal without having to open a separate investigation module.

## Navigation Exits

- `/loyalty/members` — member list
- `/loyalty/settings` — program configuration
- `/customers/:id` — from recent activity feed member links

## Open Questions

None.
