---
screen: /chirps/:id
title: Chirp Detail
role: LP
wave: W1
origin: O
cp_equivalent: "frmpstickethistory — read-only, no hash, no rule context"
---

# Chirp Detail

**URL:** `/chirps/:id`  
**Primary role:** LP  
**Entry points:** Chirp feed row click; alert detail → "View source chirp"

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Chirp type badge, store, terminal, cashier, timestamp | Breadcrumb back to /chirps |
| Top panel | Hash seal status — full-width prominent banner | Green (verified) / Red (tampered) — most critical element |
| Left column | Transaction card — full ticket detail | ~65% width |
| Right column | Rules evaluated panel + evidence action + customer card | ~35% width |

## Key Elements

### Hash Seal Status (Top Panel)
Full-width banner, always at top. Two states:
- **Verified (green):** "This transaction record has not been modified since ingestion. Hash: [SHA-256 truncated] · Ingested: [timestamp]"
- **Tampered (red):** "ALERT: This transaction record does not match its original hash. Possible data manipulation after ingestion. [SHA-256 original] vs [SHA-256 current]"

The tampered state is itself an LP event — it warrants immediate case creation and escalation. The banner is positioned above all other content because if a tamper is detected, nothing else matters.

### Transaction Card
Full ticket: every line item (item #, description, quantity, unit price, discount amount, reason code, extended price), tender section (each tender line: type, amount, change), totals (subtotal, total discounts, tax, total). Compact table layout — complete, not summarized. This is a legal-quality transaction record.

### ARTS Event Panel
Expandable. Shows the raw ARTS POSLog representation of this chirp. Relevant for: technical audit, LP expert wanting to verify the parsed data against the canonical event format, compliance documentation. Collapsed by default; LP investigators rarely need this.

### Rules Evaluated Panel
List of every detection rule that evaluated this transaction, with outcome:
- Pass (did not fire): rule name + "Transaction did not exceed threshold"
- Fire (alert generated): rule name + "Alert #[id] generated" (linked to `/alerts/:id`)
- Dry-run (observation mode): rule name + "Dry-run mode — no alert"

Covers the case where an LP investigator wants to know: "why didn't this trigger an alert?" or "which alert does this transaction explain?"

### Evidence Link Action
Button: "Attach to Case as Evidence." Opens a modal: select case (search by case ID or subject) → preview evidence record → confirm → evidence is sealed (hash computed, immutable). Also shows existing evidence attachments if this chirp has already been attached to a case.

## Interaction Flows

1. **Verify ticket integrity:** LP reviewing a suspicious transaction → checks hash seal → green banner → confirms the ticket hasn't been altered post-close → proceeds with confidence
2. **Discover tampered record:** LP opens a chirp from a flagged cashier → hash seal shows red (tampered) → LP creates a case immediately with the tamper event as the primary evidence record → escalates to management
3. **Attach to existing case:** LP identifies this chirp as corroborating evidence for an open case → clicks "Attach to Case" → searches for the open case → attaches → returns to feed

## UX Callout

The hash seal status is the entire reason `/chirps/:id` exists as a separate screen from a standard transaction view. Counterpoint's `frmpstickethistory` shows the same ticket data (line items, tender, totals) but with no integrity guarantee. A CP operator cannot tell whether a ticket record was altered after close — deliberately (by someone with database access) or accidentally (by a sync corruption). Canary's hash-before-parse seal (T.2.3) means every chirp detail screen is a mini-audit. When the seal is green, it's proof. When it's red, it's an alert that no existing LP system can generate.

## Navigation Exits

- `/chirps` — back to live feed
- `/transactions/:id` — full transaction detail (same data, different navigation context)
- `/transactions/:id/proof` — full cryptographic proof certificate
- `/cases/hawk/:id` — case the evidence was attached to
- `/customers/:id` — customer profile (from customer card, if present)
- `/alerts/:id` — alert linked from rules evaluated panel

## Open Questions

None.
