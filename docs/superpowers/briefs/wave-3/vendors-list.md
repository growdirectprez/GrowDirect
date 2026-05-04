---
screen: /vendors
title: Vendor List
role: BYR | MGR
wave: W3
origin: O
cp_equivalent: "frmvendors — Windows-only, no performance metrics, no LP context"
---

# Vendor List

**URL:** `/vendors`  
**Primary role:** BYR; MGR  
**Entry points:** Primary sidebar nav (Purchasing section)

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Vendors", Add Vendor button | |
| Filter bar | Status, Category, On-Time % range | |
| Main content | Vendor table | |

## Key Elements

### Vendor Table
Columns: Vendor ID, Vendor Name, Category, Status (Active / Inactive), Active SKUs (item count), Last PO Date, On-Time Delivery %, Return Rate %, Account Rep, Outstanding Balance ($).

**On-Time Delivery %:** Computed from receiving history — POs received within lead time ÷ total POs. The operational trust signal for a vendor. < 80% should trigger a conversation with the account rep or sourcing review.

**Return Rate %:** Units returned to vendor ÷ units received. High return rates indicate product quality issues that translate directly into customer-facing return events and LP risk (customers returning defective merchandise are sometimes flagged by rules that don't account for vendor quality problems).

**Outstanding Balance ($):** Total open AP balance across all open POs with this vendor. For finance and buyer context — if a vendor's balance is large and they're also late on delivery, that's a leverage conversation.

### Add Vendor
BYR/ADM can create a new vendor record. Required: Vendor ID (matches CP vendor code), Vendor Name. Optional fields complete the profile.

**Empty state:** "No vendors in the system. Add vendors via the Add Vendor button or wait for CP adapter sync."

## Interaction Flows

1. **Vendor sourcing review:** BYR opens vendors → sorts by On-Time Delivery % ascending → 3 vendors below 75% → opens each to review order history before renewal conversations
2. **LP quality correlation:** LP sees high return rate in Tropicals category → opens vendors → filters Category = Tropicals → one vendor at 22% return rate vs 3-5% for others → flags to BYR: vendor quality issue driving return-fraud-adjacent LP activity
3. **AP reconciliation:** Finance opens vendors → reviews Outstanding Balance column → two vendors with balances > 90 days → escalates for payment or dispute resolution

## UX Callout

CP's `frmvendors` is a contact record with payment terms. There are no performance metrics — on-time delivery and return rates don't exist as fields because CP doesn't track them. Canary computes them from PO receiving history and return records that already exist in the system. A buyer using CP to evaluate vendors is working from memory and phone calls; a buyer using Canary's vendor list is working from operational evidence. The return rate field is the LP bridge — vendor quality problems manifest as return patterns, and those patterns deserve a different investigation than coordinated return fraud.

## Navigation Exits

- `/vendors/:id` — vendor detail
- `/orders/new` — create PO for a vendor

## Open Questions

None.
