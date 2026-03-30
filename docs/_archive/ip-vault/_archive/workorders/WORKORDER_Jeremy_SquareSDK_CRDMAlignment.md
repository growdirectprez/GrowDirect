---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order: Square SDK Field Audit — CRDM Alignment Gate
*Owner: Jeremy | Blocks: Tom B-035 DDL | Priority: 🔴 HIGH*
**Date:** February 26, 2026
**Author:** ALX (Chief of Staff)
**Status:** DISPATCHED — must complete before Tom finalizes partition DDL

---

## Why This Exists

The CRDM schema and partition architecture (B-035) have been designed against our internal understanding of what Square delivers. Before Tom writes DDL that we will build production infrastructure on, we need a field-by-field verification that Square's SDK actually delivers what we've assumed — at the granularity, latency, and completeness we need.

If a field we've assumed exists doesn't, or arrives in a shape that requires transformation, Tom's partition design could be wrong from day one.

**This is a gate on Tom's DDL work. Jeremy delivers first, Tom finalizes second.**

---

## The Audit

For each CRDM table below, verify against the Square SDK / webhook payload documentation:

### 1. Timestamp Precision (Critical for Hourly Partitioning)

- Do Square webhook payloads deliver timestamps at millisecond precision?
- Specifically: `payment.created_at`, `cash_drawer_shift.opened_at`, `cash_drawer_shift.closed_at`, `labor.shift.start_at`, `labor.shift.end_at`
- If Square rounds to seconds or coarser: hourly partitioning is unaffected (partition boundary is the hour, not sub-second), but flag any rounding behavior
- **Verdict needed:** timestamp precision is sufficient for hourly sub-partition boundaries — yes or no

### 2. Cash Drawer Events (C-101 to C-104 Chirps)

- Does Square deliver cash drawer events via **webhook** in real time, or is this **polling only** from the Cash Drawers API?
- Specifically: no-sale opens, paid-out events, shift open/close — are these webhook-pushed or pull-only?
- If pull-only: what is the recommended polling interval and does this affect our < 2 minute Chirp latency promise?
- **Verdict needed:** real-time webhook delivery confirmed for all cash drawer event types we depend on

### 3. Timecard Data (C-301, C-302, C-303 Chirps)

- Does Square push timecard events (clock-in, clock-out, break start, break end) via **webhook**?
- Or is Labor API pull-only?
- C-301 (sale while off the clock) requires knowing an employee's current timecard state at the moment a payment is processed. If timecard data is pull-only, what is the realistic lag and does it break the Chirp logic?
- **Verdict needed:** real-time timecard state is accessible for Chirp evaluation — confirm the mechanism (webhook push or acceptable polling interval)

### 4. Card Fingerprint (C-005 Chirp + CRA Isolation Argument)

- Is `card_fingerprint` present on **all** payment webhook payloads?
- Or only on card-present transactions? What about manual key entry, cash, gift card tenders?
- This field is load-bearing for two things: (1) C-005 Chirp logic, (2) Syd's CRA isolation argument (no cross-merchant PAN matching). If it's absent on some tender types, both break.
- **Verdict needed:** `card_fingerprint` availability by tender type — full matrix

### 5. Inventory Adjustments

- Does Square push inventory change events via **webhook** in real time?
- Or is inventory a batch pull from the Inventory API?
- What event type covers inventory adjustments (shrinkage, receiving, manual adjustments)?
- **Verdict needed:** real-time or batch, and what webhook event type to subscribe to

### 6. Line Item Detail (C-201, C-202, C-203 Chirps)

- Does Square's `order.updated` webhook include **full line item detail** (item name, quantity, price, discounts, modifiers)?
- Or just order totals?
- C-201 (heavy discounting) needs line-item-level discount amounts. C-202 (too many voided items) needs individual void events at the line item level, not just order level.
- **Verdict needed:** line item detail completeness in webhook payload — what's present, what's absent

### 7. Gift Card Activity (C-601, C-602 Chirps)

- Does Square push gift card activity events (load, redemption, balance check) via webhook?
- What is the event type and payload shape?
- **Verdict needed:** confirmed webhook event type for gift card activity

### 8. Loyalty Events (C-801 to C-804 Chirps)

- Does Square push loyalty events (point earn, point redeem, new enrollment) via webhook?
- Or is Loyalty API pull-only?
- **Verdict needed:** real-time webhook delivery for loyalty events — yes or no

---

## Output Format

`_ALX/WorkOrders/output/Jeremy/Jeremy_SquareSDK_CRDMAlignment.md`

For each of the 8 items above:

```
### [Field / Event Type]
**Our assumption:** [what CRDM / Chirp logic assumes]
**SDK reality:** [what Square actually delivers]
**Gap:** [none / minor / material]
**Impact:** [none / Chirp logic needs adjustment / partition design affected / Syd needs to know]
**Recommended action:** [none / code change / schema change / route to Tom / route to Syd]
```

Conclude with a **summary gap table** — one row per item, severity, owner, action.

---

## Deadline

**Before Tom's next B-035 session.** Tom should not finalize partition DDL until this audit is complete. Flag ALX immediately if any material gap is found — especially on cash drawer webhooks, timecard state, or card fingerprint completeness.

---

### 9. Raw Payload Storage — Terms of Service Verification

We intend to store the raw Square webhook payload as an immutable, hash-chained JSON blob in a dedicated `raw_events` partition. Before building this into the architecture, verify:

- Does Square's Developer Terms of Service permit storage of raw webhook payloads?
- Are there any data retention restrictions on raw payload storage (e.g., must delete within X days)?
- Are there any field-level restrictions — fields we are permitted to receive but not permitted to persist (e.g., full card numbers, if ever present)?
- Does Square's ToS distinguish between storing parsed/structured data vs. storing the raw payload verbatim?

**If storage is permitted:** raw payload goes into `raw_events` table, JSONB column, partitioned by merchant_id + received_at, hash-chained on INSERT via pgcrypto compute-on-INSERT trigger. Immutable. Same pattern as fox_evidence.

**If storage is restricted:** flag immediately. ALX routes to Syd for legal assessment of what is and isn't storable. Tom holds DDL on `raw_events` until Syd clears it.

**Verdict needed:** raw webhook payload storage permitted under Square ToS — yes, no, or conditional (with conditions specified).

---

## Reference

- Square Webhooks documentation: https://developer.squareup.com/docs/webhooks
- Square Cash Drawers API: https://developer.squareup.com/docs/cash-drawers-api
- Square Labor API: https://developer.squareup.com/docs/labor-api
- Square Inventory API: https://developer.squareup.com/docs/inventory-api
- Square Loyalty API: https://developer.squareup.com/docs/loyalty-api
- CRDM v1.0: `Canary_IP/Markdown/Specs/Canary_CRDM_v1.0.md`
- Chirp rule definitions: `Canary/canary/services/chirp/rule_definitions.py`

---

*ALX | Chief of Staff | February 26, 2026*
*Gates: B-035 Tom DDL work | Routes to: Syd (card_fingerprint gap), Tom (schema gaps)*
