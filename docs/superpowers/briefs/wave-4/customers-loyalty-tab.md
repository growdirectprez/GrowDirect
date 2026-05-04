---
screen: /customers/:id — Loyalty Tab
title: Customer Loyalty Profile
role: MGR | BYR
wave: W4
origin: O
cp_equivalent: "None — CP has no loyalty profile per customer with earn/redemption history"
---

# Customer Loyalty Profile

**URL:** `/customers/:id` (Loyalty tab)  
**Primary role:** MGR; BYR  
**Entry points:** Customer detail → Loyalty tab

## Layout

This tab renders within `/customers/:id`. The parent header (customer name, ID, risk score badge, KPI row, tab bar) persists. This brief covers the Loyalty tab content only.

| Zone | Content | Notes |
|---|---|---|
| Tab content | Loyalty summary KPIs | |
| Section 1 | Enrollment + tier info | |
| Section 2 | Points activity history | |
| Section 3 | Redemption history | |

## Key Elements

### Loyalty Summary KPIs
- **Current Points Balance:** Unredeemed points at this moment
- **Tier:** Current tier (if tiers configured) + spend-to-next-tier remaining
- **Points Earned (lifetime):** All-time earn total
- **Points Redeemed (lifetime):** All-time redemption total
- **Enrolled Since:** Enrollment date

### Enrollment + Tier Info
Membership card-style display: member ID (or card number), tier badge, enrollment date, tier anniversary date. The visual representation of membership status — what a staff member sees when they look up a customer's loyalty account.

**Tier progress:** If a tiered program is configured, a progress bar shows spend-to-next-tier. "Gold member — $340 more to Platinum." This is the staff service context: a staff member helping a customer can see how close they are to the next tier and mention it as a reason to make a larger purchase today.

### Points Activity History
Table: Date, Transaction ID, Type (Earn / Redemption / Adjustment / Expiry / Enrollment Bonus), Points Change (+/-), Running Balance. All earn and redemption events in reverse chronological order.

**Adjustment entries:** Manual point adjustments by ADM (e.g., customer service recovery — add 500 points for a bad experience). Adjustments are logged with the user who made them.

**LP read:** An unusual pattern in earn history — many small transactions earning points followed by a single large redemption — can indicate points accumulation for fraudulent redemption. This pattern is visible in the activity history without running a separate query.

### Redemption History
Subset of the activity history, filtered to redemption events. Shows when and how much loyalty discount was applied at the register. Used by MGR to verify a customer's claim ("I should have had points to redeem") and by LP to audit high-value redemption events.

**Empty state:** "This customer is not enrolled in the loyalty program. Enroll from this screen." (Enrollment action in action bar — adds customer to loyalty with current date as enrollment date.)

## Interaction Flows

1. **Customer service inquiry:** Customer calls asking about their points balance → MGR opens loyalty tab → current balance = 1,240 points ($12.40 value) → tells customer accurately without needing to access CP or a separate loyalty system
2. **Tier upgrade notification:** MGR sees customer is $45 from Gold → mentions it at checkout → customer makes a qualifying purchase → BYR views tab and confirms tier upgrade occurred
3. **LP points audit:** LP investigating a loyalty fraud suspect → opens loyalty tab → earn history shows 23 transactions in 2 days, all small amounts (just above threshold for earning), followed by 2,300-point redemption → earn pattern is suspicious for manufactured transactions

## UX Callout

The loyalty tab is the per-customer view of the loyalty dashboard's aggregate data. Where the dashboard tells BYR "18% of Platinum members have LP flags," the loyalty tab tells LP "this specific customer has 23 earn events in 2 days before a large redemption." They're the same data at different scopes. The staff service context (tier progress, points balance at a glance) is equally important: a floor associate helping a customer shouldn't have to ask the manager or check a kiosk to answer "how many points do I have?" The answer is one screen open on any device, available to any authorized staff member.

## Navigation Exits

- `/customers/:id` — back to customer overview

## Open Questions

None.
