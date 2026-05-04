---
screen: /rules/:id
title: Detection Rule Detail + Enable/Disable
role: LP | ADM
wave: W1
origin: O+L4
cp_equivalent: "None"
---

# Detection Rule Detail + Enable/Disable

**URL:** `/rules/:id`  
**Primary role:** LP; secondary: ADM  
**Entry points:** Rules list row; alert detail → rule name link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Rule name, family badge, enabled/disabled state badge | Breadcrumb back to /rules |
| Top section | Rule card (description + detection logic) | Full-width |
| Left column | Alert history (30 days) | ~60% width |
| Right column | Parameters panel + allow-list summary | ~40% width |
| Action bar | Enable/Disable with reason, Edit Parameters | Bottom |

## Key Elements

### Rule Card
- **Description:** What this rule is designed to detect and why it matters. Human-readable paragraph. E.g., "Detects cashiers who apply discounts exceeding the store-configured cap on any transaction. High-volume discounting may indicate collusion with customers, unauthorized markdown behavior, or a misconfigured POS reason code."
- **Detection Logic:** Human-readable predicate — not SQL, not code. E.g., "Fires when: a cashier applies a discount reason code on a transaction where the total discount amount exceeds [discount_cap]% of the transaction subtotal, as configured for the store in `/settings/store/discounts`."
- **Last modified by / when:** Shows who last changed this rule's configuration and when (audit trail surface).

### Parameters Panel (L4 addition — P1)
Editable threshold fields for rules that support configuration. Fields vary by rule family:
- Drawer rules: variance threshold (dollar amount), shift window (hours)
- Discount rules: discount cap %, reason code exclusions
- Void rules: max voids per shift, amount threshold per void

Each field shows current value + "Last changed by [user] on [date]." Edit → requires reason → audited. This panel implements Q.4.1 from the L4 gap delta.

### Dry-Run Status Control (L4 addition — P1)
Status selector: Dry Run → Observation → Alert (three states, per Q.4.5 L4 gap).
- **Dry Run:** Rule evaluates transactions but generates no alerts. Results visible in a "Dry-run Results" tab (what would have fired).
- **Observation:** Rule generates alerts but they're routed to a separate "Observation" queue visible only to ADM — not LP investigator's main feed.
- **Alert:** Full alert generation — default operating mode.

Dry-run → Observation transition requires ADM approval. Observation → Alert requires ADM approval.

### Alert History (30 days)
Table: date, cashier, store, transaction amount, alert status (acknowledged/escalated/case-linked). Shows the 30 most recent alerts from this rule. Clicking a row opens `/alerts/:id`.

### Allow-List Summary
Links to all allow-list entries that suppress this rule. Each entry shows: who/what is allow-listed, at which store, expiry date. "Add Allow-List Entry" button → navigates to the relevant `/settings/allowlist/*` screen with this rule pre-selected.

## Interaction Flows

1. **Adjust threshold:** ADM opens rule → finds Q-DR-01 firing too frequently for a specific store (threshold too tight) → opens Parameters panel → changes discount cap from 20% to 25% for that store → adds reason "MGR Kim confirmed 25% is standard for weekend clearance events" → saves → change audited
2. **Enable dry-run:** LP wants to test a new rule before it goes live → changes status from Disabled to Dry Run → runs for one week → reviews dry-run results tab → satisfied → ADM approves transition to Observation → LP reviews observation queue → promotes to Alert
3. **Review alert pattern:** LP opens rule → sees alert history → 80% of alerts in the last 30 days are from Cashier J. Martinez at Store 3 → clicks through to the cashier's alerts → opens a case

## UX Callout

Detection logic must be human-readable. The Parameters panel and Dry-Run status control (L4 P1 additions) transform this screen from a read-only reference into an operational tuning surface. LP investigators are not engineers — they need to understand what a rule does, whether it's calibrated correctly for their store's operational patterns, and whether a particular pattern should be allow-listed vs investigated. CP operators have no equivalent concept: there are no rules, there is no tuning, there is no dry-run. LP teams in CP shops rely entirely on institutional knowledge and manual report-reading.

## Navigation Exits

- `/rules` — back to rules list
- `/alerts/:id` — from alert history table
- `/settings/allowlist/*` — from allow-list summary
- `/admin/audit` — to review all changes to this rule's configuration

## Open Questions

None.
