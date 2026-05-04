---
screen: /settings/pricing-rules
title: Pricing Rules
role: BYR | MGR | ADM
wave: W4
origin: N
cp_equivalent: "Partial — CP has pricing matrix and price levels; no conditional rule engine, no LP interaction"
---

# Pricing Rules

**URL:** `/settings/pricing-rules`  
**Primary role:** BYR; MGR; ADM  
**Entry points:** Settings → Merchandising section

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Pricing Rules", New Rule button | |
| Filter bar | Status (Active / Inactive), Type, Store | |
| Main content | Rules table | |

## Key Elements

### Pricing Rules Table
Columns: Rule Name, Type, Applies To (items/categories/customers), Conditions, Resulting Price/Discount, Stores, Status, Priority, Last Modified.

**Rule Types:**
- **Price Level:** Customer-segment-based pricing (Retail / Wholesale / Contractor / Employee). Assigns a price level to a customer segment; transactions from those customers use the level's pricing.
- **Quantity Break:** Buy N → price per unit decreases. E.g., "1-5 units at $12.99 each; 6+ units at $10.99 each."
- **Time-Based:** Different prices during specified date ranges or times of day. Used for seasonal pricing changes.
- **Category Margin Floor:** Auto-reject discounts that would bring a category's line-item margin below a configured floor. Applied at the POS level.

**Priority:** When multiple rules apply to the same transaction, priority determines which rule takes effect. Lower number = higher priority (Priority 1 fires before Priority 5). Rules at the same priority level that conflict generate a configuration warning.

### LP Interaction
Pricing rules define the legitimate discount structure. When LP's detection rules evaluate transactions, the pricing rules determine the baseline expectation. A 30% discount is flagged by the Discount rule if the discount cap is set at 20% — but if there's a Wholesale price level for that customer that legitimately produces a 30% discount, the pricing rule provides the allow-list context.

**Rule change audit:** Every pricing rule modification is logged: changed by / timestamp / previous configuration. This audit trail is accessible from rule detail and from `/reports/price-history` (rule-generated changes appear in the price history).

**Empty state:** "No pricing rules configured. Add rules to define customer segment pricing and discount structures."

## Interaction Flows

1. **Wholesale price level setup:** BYR creates Price Level rule for Wholesale customers → 20% off retail → assigns to B2B customer segment → all Wholesale accounts now receive Canary-computed prices at POS
2. **Category margin floor:** BYR sets a margin floor rule for Tropicals at 40% gross margin → any discount that would breach 40% margin on a Tropicals item is auto-blocked at POS with a message: "Discount not allowed — below category margin floor"
3. **LP rule calibration:** LP sees excess alert volume from Wholesale transactions → opens pricing rules → confirms Wholesale = 20% off → adjusts LP's discount cap allow-list for Wholesale customer segment to 25% (buffer for rounding) → alert volume normalizes

## UX Callout

CP's pricing structure is a matrix of price levels and codes configured in a Windows form. It works, but it has no connection to the LP detection layer and no audit trail for changes. Canary's pricing rules have three additions: the category margin floor (which enforces pricing discipline at the POS level — a rule CP has no equivalent to), the LP interaction model (rules as the legitimate baseline against which LP detections are calibrated), and the change audit trail (who changed what and when). The margin floor is the operationally valuable one for a small business buyer: it prevents accidental margin destruction at the register without requiring the manager to review every discount manually.

## Navigation Exits

- `/settings/catalog` — neighboring settings section

## Open Questions

None.
