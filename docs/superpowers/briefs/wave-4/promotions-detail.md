---
screen: /promotions/:id
title: Promotion Detail
role: MGR | BYR | LP
wave: W4
origin: O
cp_equivalent: "frmimpromotions detail — no performance tracking, no LP alert correlation"
---

# Promotion Detail

**URL:** `/promotions/:id`  
**Primary role:** MGR; BYR; LP  
**Entry points:** Promotions list row

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Promo name, status badge, type, date range | Breadcrumb back to /promotions |
| Top section | Promotion definition | |
| Tab bar | Performance / LP Context / Configuration | |
| Tab content | Tab-dependent | |
| Action bar | Activate, Pause, Deactivate, Edit (Draft/Scheduled only) | Status-dependent |

## Key Elements

### Promotion Definition (top section)
What the promotion does: Type (Discount % / Buy X Get Y / Fixed Price / Bundle), discount value or structure, qualifying items/categories, qualifying customer segments (if restricted), store applicability, date/time range, usage limits (if any — e.g., "max 1 use per customer per day"), coupon code (if code-required).

### Performance Tab
KPIs since activation:
- **Transactions using promo:** Count
- **Total Discount Value ($):** All discounts applied via this promo
- **Avg Discount Per Transaction ($)**
- **Incremental Units (est.):** If baseline data is available, an estimate of additional units sold due to the promotion (vs pre-promotion average for those items)
- **Net Revenue Impact (est.):** Incremental revenue − discount cost

By-day chart: discount value and transaction count per day for the promotion's duration. Shows adoption curve (ramp-up) and identifies anomalous spikes.

### LP Context Tab
LP-specific view of this promotion's alert activity:
- **Alerts associated with this promo:** Count of alerts where the triggering transaction used this promotion code/rule
- **Alert types:** Breakdown by rule family (Discount / Void / Comp)
- **Cashiers with highest promo alert volume:** Table of top 5 cashiers by alert count while applying this promotion
- **Flagged transactions:** Transactions using this promotion that also triggered alerts — direct link to `/transactions/:id` and `/alerts/:id` for each

**LP read:** A promotion with 200 transactions and 3 alerts is normal. A promotion with 200 transactions and 47 alerts on discounts is not — the promotion may have a design flaw (discount % exceeds the rule threshold it was intended to stay below) or is being abused.

### Configuration Tab
Full promotion parameters as configured. Editable when status is Draft or Scheduled. Read-only when Active or Expired.

**Deactivate action:** Immediately removes the promotion from POS. Cashiers can no longer apply the discount. Status → Paused or Deactivated. Used when LP identifies active abuse of a running promotion.

**Empty state per tab:** No empty states — promotion always has configuration; performance and LP context populate as the promotion runs.

## Interaction Flows

1. **Promotion performance review:** BYR opens active promotion → Performance tab → incremental units = 140, net revenue impact = +$820 → promotion is working → notes for future use
2. **LP abuse investigation:** LP opens promotion → LP Context tab → 47 alerts, top cashier applied the promotion 38 times in 2 days on non-qualifying items → LP opens cases for each flagged transaction → deactivates promotion pending review
3. **Rule overlap fix:** New promotion triggers excess discount alerts → ADM opens promotion configuration → discount % set to 25% → LP's discount cap rule fires at 20% → BYR reduces promotion to 19% or LP adjusts the allow-list for this promotion period

## UX Callout

The LP Context tab is the feature that makes promotions operationally safe rather than just commercially executed. In CP, there is no connection between the promotions module and the transaction exception reports. A promotion that is being systematically abused by a cashier stays active until someone manually correlates promotion transaction history with exception reports — a process that might take days or weeks. Canary surfaces the alert correlation on the promotion record itself. A running promotion with a spike in LP alerts is visible the moment LP opens the promotion detail, not after a quarterly audit.

## Navigation Exits

- `/promotions` — back to promotions list
- `/transactions/:id` — from LP context flagged transactions
- `/alerts/:id` — from LP context alert links

## Open Questions

None.
