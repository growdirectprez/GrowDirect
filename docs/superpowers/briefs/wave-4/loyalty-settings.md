---
screen: /loyalty/settings
title: Loyalty Settings
role: ADM | MGR
wave: W4
origin: O
cp_equivalent: "None — CP loyalty configuration is minimal; no tier engine, no earn/burn rules"
---

# Loyalty Settings

**URL:** `/loyalty/settings`  
**Primary role:** ADM; MGR  
**Entry points:** Loyalty dashboard → Settings link; Settings → Marketing section

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Loyalty Settings" | |
| Tab bar | Program / Tiers / Earn Rules / Redemption Rules | |
| Tab content | Tab-dependent | |

## Tabs

### Program Tab
High-level program configuration:
- **Program Name:** Displayed to customers ("Garden Rewards")
- **Point Currency Name:** What points are called ("Points", "Seeds", "Petals")
- **Points to $ Value:** Conversion rate (e.g., 100 points = $1 in redemption value)
- **Enrollment Bonus:** Points awarded at enrollment
- **Program Status:** Active / Paused (pausing suspends new point earning; existing balances preserved)

### Tiers Tab
Define loyalty tiers (optional). Each tier: name, annual spend threshold (to qualify or maintain), earn multiplier (Gold members earn 2× points per dollar), and benefits description.

**Example configuration:** Silver = 0-$499/year, 1× earn; Gold = $500-$1,999/year, 1.5× earn; Platinum = $2,000+/year, 2× earn.

If no tiers are configured, all members earn at the base rate with no tier distinction.

### Earn Rules Tab
Configures how points are earned:
- **Base Rate:** Points per dollar spent (e.g., 1 point per $1)
- **Category Multipliers:** Specific categories earn more points (e.g., "Tropicals earn 2× points during spring season")
- **Blackout Categories:** Categories that earn zero points (e.g., Gift Cards, Charitable Donations)
- **Promotion-Linked Earn:** Tie a point-earning bonus to an active promotion period

### Redemption Rules Tab
Configures how points are redeemed:
- **Minimum Redemption:** Minimum points required to redeem (e.g., 500 points minimum)
- **Redemption Increment:** Points redeemable only in multiples of X (e.g., 100-point increments)
- **Max Redemption per Transaction ($):** Cap on the discount value applied per transaction via loyalty redemption
- **Blackout Periods:** Date ranges during which redemption is not allowed (e.g., peak sales days)

**LP interaction with redemption rules:** The max redemption per transaction cap is the primary LP-relevant configuration here. Unlimited loyalty redemption against a single transaction is a potential fraud vector (manufacturing transactions to generate redemption credit). The cap constrains the maximum exposure per event.

**Empty state per tab:** "No [tiers/earn rules/redemption rules] configured."

## Interaction Flows

1. **Launch configuration:** ADM sets up program for the first time → Program tab (name, points value) → Earn Rules (base rate, category multipliers) → Redemption Rules (min 500 points, max $25/transaction) → Tiers (3-tier structure) → activates program
2. **Seasonal bonus rule:** BYR adds Category Multiplier for Tropicals → 2× points on Tropicals purchases → May 1-31 → seasonal earn bonus drives spring sales
3. **LP cap adjustment:** LP identifies a pattern of large loyalty redemptions (members redeeming $100+ in a single transaction repeatedly) → ADM reduces max redemption per transaction cap from $50 to $25 → configures alert if redemption ≥ $20 in a single transaction (via alert routing settings)

## UX Callout

CP's loyalty configuration, where it exists, is a basic setup screen with no tier engine and no earn/burn rule flexibility. Canary's loyalty settings are designed for the same operator who sets up QuickBooks — someone who is not a technologist but needs to configure a program that reflects their business decisions. The earn rules and redemption rules are expressed in plain business terms (points per dollar, minimum redemption, max per transaction) rather than database fields. The LP interaction with redemption caps closes the loop between program design and LP risk management: the operator decides the exposure they're comfortable with when they configure the cap, not after a fraud event reveals the gap.

## Navigation Exits

- `/loyalty` — back to loyalty dashboard

## Open Questions

None.
