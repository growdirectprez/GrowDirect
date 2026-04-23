---
date: 2026-04-23
type: wiki
tags: [secure, omnichannel, customer-order, data-flow, ship-from-store, bopis, 2017]
sources:
  - Brain/raw/inbox/secure-data-flow.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Secure — Customer Order Management Data Flow (2017)

## Summary

A **Customer Order Management** data-flow diagram from 2017 showing the omnichannel order-fulfilment decision tree Secure EBR was designed to monitor. Walks through how an online order flows from origination (Webstore, Kiosk, or Call Center) through fulfilment (Ship-from-Store or Ship-to-Customer or customer pickup in-store) to completion (delivered, picked up, returned, or problem-flagged).

Complements the broader [[Brain/wiki/secure-omnichannel|Secure Omnichannel]] wiki card — this artefact is the specific data-flow diagram, while secure-omnichannel covers the product positioning.

## The Flow (consolidated from the extracted diagram)

**Origination nodes:**
- Webstore → Online Order
- Kiosk
- Call Center
- Call Center Intervention

**Fulfilment branch (decision after order placed):**
- Ship from Store
- Ship from Store → Customer
- Delivery to Customer
- Delivery to Pick Up Location

**Terminal states:**
- Order Picked (and Packed)
- Customer Pick up in Store
- Order Picked Up
- Order Delivered
- Order Adjusted (No / Yes branches)
- Order Pending Fulfillment → order-line-item fulfilled → Order Delivered by Retailer

**Exception nodes:**
- Item Damaged
- Item Returned
- Item Missing
- Wrong Item

## What Secure Monitored

Each node in this flow is a data capture point. Secure EBR was expected to ingest events from POS, OMS (Order Management System), WMS (Warehouse Management System), and fulfilment partners and correlate them against the expected state transitions. An order that enters fulfilment but never reaches a terminal state is an exception. An order that terminates in "Item Missing" or "Wrong Item" at disproportionate rates against peer stores is a loss-prevention signal.

## Why This Matters

- **Pre-empts the BOPIS fraud surface.** By 2017, ship-from-store and buy-online-pickup-in-store (BOPIS) were the two fastest-growing fulfilment modes in US retail — and they introduced new fraud vectors (false "item missing" claims, ship-to-store diversion, picker substitution). The Secure data flow captures these nodes explicitly.
- **Omnichannel is where Secure extended beyond store-only LP.** Traditional EBR was a store-POS tool. This flow makes the product's scope explicit: the moment the order originates online, Secure follows it through every handoff until terminal state.
- **Pattern for Canary.** Canary's current scope is Square-merchant POS. Canary's future omnichannel extension (when Square merchants add BOPIS, delivery apps, third-party marketplaces) will need exactly this kind of cross-system flow monitoring. This 2017 diagram is a useful reference.

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-omnichannel|Secure Omnichannel]] — product positioning (existing card)
- [[Brain/wiki/secure-5-inventory|Secure 5 Inventory]] — inventory-side of the same product family
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/projects/Canary|Canary]] — forward lineage (omnichannel extension is future scope)

## Sources

- `Brain/raw/inbox/Secure Data Flow.pdf` — Customer Order Management data-flow diagram, 2017

Extraction path: `.pdf` → markitdown.
