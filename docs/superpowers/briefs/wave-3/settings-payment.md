---
screen: /settings/payment
title: Payment Settings
role: ADM
wave: W3
origin: O
cp_equivalent: "CP payment configuration (multiple forms) — no tokenization status, no PCI scope visibility"
---

# Payment Settings

**URL:** `/settings/payment`  
**Primary role:** ADM  
**Entry points:** Settings → Payment section

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Payment Settings" | |
| Tab bar | Tender Types / Tokenization / AR Settings | |
| Tab content | Tab-dependent | |

## Tabs

### Tender Types Tab
Lists all accepted payment methods: Cash, Credit Card, Debit Card, Check, Gift Card, Charge (AR), Store Credit. Each has a toggle (Enabled / Disabled per store) and a minimum/maximum transaction amount (if applicable).

**CP crosswalk:** Synced from CP's tender type configuration. Canary displays for reference and LP context — LP investigators need to know which tender types are accepted to evaluate tender manipulation alerts (e.g., a void/re-ring to switch a cash tender to a charge tender).

### Tokenization Tab
Shows the tokenization/PCI status for each store:
- **Tokenization Status:** Active / Not Configured
- **Processor:** Payment processor name (for reference — Canary never handles card data)
- **Last Token Event:** Timestamp of the most recent tokenized transaction event received by Canary
- **PCI Scope Note:** "Canary receives tokenized transaction data only. Card numbers do not pass through or are stored in this system."

**Important design constraint:** Canary is intentionally outside PCI scope for card data. This tab documents that fact. ADM sees it; it's the compliance reference point. The "PCI scope" section in `admin/config` references this tab.

### AR Settings Tab
- **AR Enabled:** Toggle per store (charge sales require this enabled)
- **Default Credit Limit ($):** Applied to new customer accounts unless manually overridden
- **Finance Charge Rate (%):** Applied to past-due balances (if applicable — some operators don't use finance charges)
- **Statement Cycle:** How often AR statements are generated (monthly / 15-day / on demand)
- **Auto-suspend Threshold:** If a customer's AR balance exceeds a configured amount, new charge sales are automatically blocked pending manual override. Prevents runaway AR exposure.

**Empty state per tab:** "No payment configuration found. Sync from CP adapter or configure manually."

## Interaction Flows

1. **Tender type audit:** LP wants to understand which tenders are enabled before investigating a tender-manipulation alert → opens Payment Settings → Tender Types → confirms Cash + Credit + Charge are all enabled at Store 2 → returns to alert investigation with correct context
2. **PCI documentation:** ADM needs to document PCI scope for an audit → opens Tokenization tab → confirms tokenization active at all stores → screenshots tab for compliance documentation
3. **AR auto-suspend:** Finance notices a B2B customer approaching credit limit repeatedly → ADM sets auto-suspend threshold to match credit limit → future transactions that would exceed limit are blocked at point of sale automatically

## UX Callout

Payment settings in Canary are primarily a reference surface — tender types and tokenization status are configured in CP and the payment processor, not in Canary. The value is context for LP and compliance: an LP investigator investigating a tender-manipulation alert needs to know the legitimate tender options at the store; a compliance officer verifying PCI scope needs documentation that Canary receives tokenized data only. The AR settings tab is the one area where Canary has operational control rather than just display — AR is a Canary-managed financial ledger, not a CP-synced value.

## Navigation Exits

- `/settings/catalog` — neighboring settings section
- `/admin/config` — for sync and adapter settings

## Open Questions

None.
