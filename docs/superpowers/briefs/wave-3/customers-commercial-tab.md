---
screen: /customers/:id — Commercial Tab
title: Customer Commercial Profile
role: MGR | BYR
wave: W3
origin: O
cp_equivalent: "Customer detail in CP — no LTV, no category affinity, no purchase frequency"
---

# Customer Commercial Profile

**URL:** `/customers/:id` (Commercial tab)  
**Primary role:** MGR; BYR  
**Entry points:** Customer detail → Commercial tab

## Layout

This tab renders within `/customers/:id`. The parent header (customer name, ID, risk score badge, KPI row, tab bar) persists. This brief covers the Commercial tab content only.

| Zone | Content | Notes |
|---|---|---|
| Tab content | Commercial KPI summary | |
| Section 1 | Purchase history metrics | |
| Section 2 | Category affinity breakdown | |
| Section 3 | Visit frequency analysis | |

## Key Elements

### Commercial KPI Summary
Four KPIs at the top of the tab:
- **Lifetime Value ($):** Total net sales attributed to this customer account (all time)
- **12-Month Sales ($):** Net sales in the trailing 12 months
- **Avg Transaction Value ($):** Average ticket size for this customer
- **Visit Frequency:** Avg visits per month (rolling 12 months)

These KPIs exist because the customer profile is used by two different roles for two different purposes: LP uses the Risk and Context tabs (W1) to understand threat potential; MGR and BYR use the Commercial tab to understand customer value and buying behavior.

### Purchase History Metrics
- **First Purchase Date:** When this customer first appears in the transaction record
- **Last Purchase Date:** Most recent transaction
- **Total Transactions:** All time
- **Return Rate (%):** Customer's personal return rate vs store average. An elevated personal return rate that also appears in the Risk tab is the convergence of commercial and LP signals.
- **Discount Rate (%):** How often and how much this customer uses discounts. A high discount rate from a commercial perspective might indicate price sensitivity; from an LP perspective, it might indicate discount abuse.

### Category Affinity
Bar chart or table: which departments this customer purchases from, by frequency and value. "This customer spends 72% of their purchase value in Tropicals/Succulents." Used by BYR for targeted promotion design and by MGR for personalized service.

**Top items:** List of this customer's most frequently purchased items (by transaction count). First-order signal for loyalty program personalization.

### Visit Frequency Analysis
Mini chart: visits per month over the past 12 months. A customer who visited 4-5 times per month for a year and then dropped to 0 visits in the past 2 months is a churn candidate. MGR uses this to identify customers worth reaching out to.

**Empty state:** "No purchase history available for this customer."

## Interaction Flows

1. **High-value customer identification:** MGR opens Commercial tab → LTV = $4,200, 12-month = $1,100, visits declining → flags as churn risk → personalizes outreach with category-targeted offer
2. **Loyalty program targeting:** BYR runs customer search by category affinity → filters for high-Tropicals affinity customers → commercial tab confirms 28 customers with > 60% Tropicals spend → designs Tropicals loyalty event for this segment
3. **LP-commercial convergence:** LP investigator looking at a fraud suspect opens Commercial tab → LTV = $180, return rate = 48% → returns exceed purchases; this customer is returning more value than they've bought → commercially incoherent → strengthens fraud hypothesis

## UX Callout

CP's customer detail is a contact record — name, address, and transaction history summary. LTV, category affinity, and visit frequency don't exist as computed fields. A buyer who wants to understand which customers to invite to a category-specific event must export transaction data and do the analysis in Excel. Canary computes these metrics continuously from the perpetual transaction record. The LP-commercial convergence scenario (step 3 above) is only possible when both risk and commercial data live in the same record — an LP investigator who never opens the Commercial tab still benefits from the data being there, because it's visible when the case demands it.

## Navigation Exits

- `/customers/:id` — back to customer overview
- Other tabs: Risk, Context, AR, Loyalty (wave-gated)

## Open Questions

None.
