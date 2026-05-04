---
screen: /transfers/:id/receive
title: Transfer Receipt
role: RCV | MGR
wave: W2
origin: N
cp_equivalent: "frmimtransferin — Windows-only, no auto-alert on variance"
---

# Transfer Receipt

**URL:** `/transfers/:id/receive`  
**Primary role:** RCV; MGR  
**Entry points:** Transfer detail → "Receive This Transfer" button (destination store); transfer list → In Transit row action

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Receiving Transfer #[id] from [Store X]", expected receipt date | |
| Main content | Receipt line entry table | Mobile-optimized: large tap targets, barcode scan |
| Damage notation section | Free text + per-line damage flags | Below line table |
| Action bar | Confirm Receipt, Save Progress (resume later), Flag for LP Review | |

## Key Elements

### Receipt Line Entry Table
Columns: Item # (with scan icon), Description, Expected Qty (from transfer — locked), Received Qty (editable — enter actual), Variance (auto-computed: received − expected), Damage Flag (toggle per line).

Barcode scan entry: RCV taps the scan icon → scans item → item row highlights → enters received qty on a large numeric keypad. Mobile-first interaction — RCV is physically at the receiving dock, not at a desk.

**Variance auto-computation:** As RCV enters received quantities, variance column updates in real-time. Variance = 0: green check. Variance < 0: orange (short-shipped). Variance > 0: blue (over-received — unusual but possible with loose packs).

### Damage Flag
Per-line toggle. When flagged: damage description field appears on that line. Notes: "5 units received, 2 with cracked pots — not saleable." Damaged quantities are still counted as received but flagged for inventory adjustment after receipt.

### Auto-Variance Alert
When Confirm Receipt is clicked and any variance exists: system computes total variance value (variance qty × average cost) → if variance > configured LP threshold → auto-generates LP alert: "Transfer T-1049: Variance of $127 detected (12 units short). From: Store 1 → To: Store 3." LP is notified without the RCV having to take any separate action.

This is the mechanism that eliminates the CP workflow of: "RCV discovers variance → writes on paper → tells manager → manager tells LP — days later."

### Save Progress
If interrupted (delivery truck arrives during entry), RCV can save progress and resume from where they left off. Session preserves entered quantities.

**Empty state:** All Received Qty fields are blank at start — RCV enters each from scratch.

## Interaction Flows

1. **Standard receipt:** RCV scans each item → enters received qty → all quantities match expected → Confirm Receipt → status → Received → inventory at destination increases → LP not alerted (no variance)
2. **Short-ship discovery:** RCV enters qty for item #4721 → received 18, expected 20 → variance shows −2 (orange) → RCV completes rest of form → Confirms → variance alert generated → LP investigates
3. **Damage notation:** RCV receives 5 units of a fragile item → 2 are damaged → enters 5 received, flags 2 as damaged → notes "2 units cracked — cannot stock" → confirms → MGR sees damage note → creates adjustment to write off 2 units

## UX Callout

In CP, transfer receipt (Transfer In) requires a PC at the receiving dock — in most warehouse environments, that means RCV writes counts on paper at the dock, then keys them into CP at the office PC later. Canary's mobile-web form is used on a phone or tablet at the dock, where the receiving actually happens. The auto-variance alert eliminates the manual LP notification step entirely. This is a physical workflow improvement, not just a UI refresh: the receiving event and the LP notification happen at the same moment, by the same person, with no separate escalation step.

## Navigation Exits

- `/transfers/:id` — back to transfer detail
- `/transfers/:id/variance` — redirected here after confirm if variance > threshold

## Open Questions

None.
