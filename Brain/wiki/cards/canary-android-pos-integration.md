---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, android-pos, ncr-counterpoint, rapidpos, driftpos, integration, api, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Android POS Integration

Bart's channel runs DriftPOS (whitelabel RapidPOS) on Android, which sits on top of NCR Counterpoint inventory and back-office. This is the primary integration surface for Canary's go-to-market. Getting this right is the product — without a working POS integration, Canary is a standalone inventory app competing with spreadsheets.

The integration is not a reporting layer. It is a live data contract: POS events flow to Canary in real time, Canary intelligence flows back to the POS in real time. Two systems, one operational brain.

---
last-compiled: 2026-05-04
needs-review: false

## What Each System Owns

Clear ownership is the prerequisite for a clean integration. Blurry ownership creates duplication, conflicts, and confusion for the operator.

| Domain | POS owns | Canary owns |
|---|---|---|
| Transaction record | Sale, return, void — the financial record of record | — |
| Payment processing | Card, cash, split tender | — |
| Tax calculation | Line-item and order-level tax | — |
| Item master (commercial) | Price, tax class, PLU/barcode | Item master (operational): location, velocity, replenishment params |
| Inventory position | Running count (decremented at sale) | Authoritative SOH, back-stock, replenishment state |
| Customer record | Loyalty ID, purchase history | — |
| Financial reporting | Daily sales summary, Z-tape | Operational performance (velocity, fill rate, cost-to-serve) |
| Labor time-and-attendance | Shift clock-in/out | Task completion, productivity (tasks per hour) |

**Conflict resolution rule:** when POS SOH and Canary SOH diverge (they will, because POS is decremented at sale and Canary is adjusted at receiving and cycle count), Canary is authoritative for operational decisions (replenishment triggers, order quantities). POS SOH is used for transaction integrity checks. Divergence triggers a cycle count flag — not an automatic override in either direction.

---
last-compiled: 2026-05-04
needs-review: false

## NCR Counterpoint REST API — What Exists

NCR Counterpoint exposes a REST API (`/API/` endpoint, documented publicly). Key endpoints relevant to Canary:

| Resource | Method | Canary use |
|---|---|---|
| `/API/Tickets` | GET | Pull completed sales transactions |
| `/API/IM_INV` | GET | Query current inventory by item |
| `/API/IM_ITEM` | GET/PUT | Item master read and update |
| `/API/SO_HEADER` | GET | Sales order (BOPIS/special order) status |
| `/API/PO_HEADER` | GET/POST | Purchase orders read/create |
| `/API/VI_VENDOR` | GET | Vendor (supplier) master |
| `/API/AR_CUST` | GET | Customer records |
| Webhooks / Events | — | Not native in Counterpoint — polling required |

**The gap:** Counterpoint REST does not offer native webhooks. Real-time sale events are not pushed — they must be polled. Canary's integration layer polls `/API/Tickets` on a configurable interval (default: 60 seconds) and processes new transactions since the last poll timestamp. This is not true real-time, but 60-second latency is operationally acceptable for replenishment trigger purposes.

**For DriftPOS / RapidPOS specifically:** the RapidPOS layer sits above Counterpoint and may expose additional APIs or event hooks not in the base Counterpoint spec. Bart's team will know. Canary's integration should be built against both Counterpoint REST (the stable, documented layer) and RapidPOS-specific extensions where they exist and are useful.

---
last-compiled: 2026-05-04
needs-review: false

## Integration Architecture

```
                    ┌─────────────────────┐
                    │   Android POS       │
                    │   (DriftPOS /       │
                    │    RapidPOS)        │
                    └────────┬────────────┘
                             │
                    NCR Counterpoint REST API
                             │
                    ┌────────▼────────────┐
                    │  Canary POS Bridge  │   ← polling adapter, hosted in Canary Go
                    │  (Go service)       │
                    └────────┬────────────┘
                             │  Events (normalized)
                    ┌────────▼────────────┐
                    │  Canary Event Bus   │   ← RIB-equivalent; MCP junctions
                    └────────┬────────────┘
                    ┌────────┴─────────────────────────┐
                    │                                   │
           ┌────────▼───────┐              ┌───────────▼──────┐
           │  SOH Service   │              │  Replenishment   │
           │  (live inventory)             │  Engine          │
           └────────────────┘              └──────────────────┘
```

**The POS Bridge** is a dedicated Canary Go microservice:
- Connects to the Counterpoint REST API using the store's API credentials
- Polls on configurable interval (default 60s, adjustable to 30s for high-velocity stores)
- Normalizes Counterpoint transaction format into Canary's internal event schema
- Handles authentication, retry, and error logging
- One Bridge instance per store tenant

**The Event Bus** is the MCP junction layer — each event traverses a junction, is hash-stamped, and routed to downstream services. The Evidentiary Rail starts here: every POS transaction that flows through Canary gets a hash at ingestion.

---
last-compiled: 2026-05-04
needs-review: false

## Event Schema — Sale Event (Core)

The most frequent event type. Everything downstream depends on this being correct.

```json
{
  "event_type": "pos.sale",
  "event_id": "uuid-v4",
  "store_id": "store-001",
  "pos_transaction_id": "12847",
  "timestamp": "2026-05-04T10:32:17Z",
  "lines": [
    {
      "sku": "0000012847",
      "qty_sold": 2,
      "unit_price": 4.99,
      "line_total": 9.98,
      "discount": 0.00,
      "pos_item_id": "CNTRPNT-0000012847"
    }
  ],
  "tender_type": "credit",
  "cashier_id": "emp-042",
  "source": "ncr_counterpoint",
  "source_version": "9.4.0",
  "bridge_ingested_at": "2026-05-04T10:32:19Z"
}
```

**Canary actions on sale event:**
1. Decrement SOH for each line item × quantity
2. Update velocity rolling window for each SKU
3. Check replenishment trigger: if new SOH < display minimum → generate replenishment task
4. Check Watch List: recalculate days-of-stock-remaining
5. Append to evidentiary log (hash + timestamp)
6. Aggregate into daily sales summary

---
last-compiled: 2026-05-04
needs-review: false

## Event Schema — Return Event

```json
{
  "event_type": "pos.return",
  "event_id": "uuid-v4",
  "store_id": "store-001",
  "original_transaction_id": "12841",
  "lines": [
    {
      "sku": "0000012847",
      "qty_returned": 1,
      "return_reason": "customer_changed_mind",
      "condition": "resalable"
    }
  ]
}
```

**Canary actions on return:**
- Increment SOH if condition = resalable
- Flag for inspection if condition = damaged (do not auto-increment SOH; inspection task generated)
- Update velocity (a return is negative demand signal — weight it accordingly, not as zero)
- Check if return pushes SOH above display maximum (unusual but possible — flag)

---
last-compiled: 2026-05-04
needs-review: false

## Event Schema — Void Event

```json
{
  "event_type": "pos.void",
  "event_id": "uuid-v4",
  "voided_transaction_id": "12846",
  "void_reason": "operator_error"
}
```

**Canary actions on void:**
- Reverse all SOH decrements from the voided transaction
- Remove the voided sale from the velocity rolling window
- Note: voids are more common than expected (fat-finger at register, scan errors, customer changes mind before tender). Canary should track void rate by cashier — high void rate may indicate training issue.

---
last-compiled: 2026-05-04
needs-review: false

## POS → Canary: Additional Events

| Event | Trigger | Canary action |
|---|---|---|
| `pos.end_of_day` | Z-tape / end-of-day close in POS | Reconcile POS running SOH vs. Canary SOH; flag discrepancies > threshold for cycle count |
| `pos.price_change` | Price update in Counterpoint | Update Canary item record (unit price affects cost-to-serve calculation) |
| `pos.item_added` | New PLU created in Counterpoint | Prompt operator: "New item detected in POS — add to Canary inventory?" |
| `pos.item_deactivated` | Item deactivated in Counterpoint | Auto Phase-Out status in Canary range; stop replenishment |
| `pos.special_order` | Customer special order placed | Create BOPIS / special order record in Canary; generate pick task when inventory confirmed |

---
last-compiled: 2026-05-04
needs-review: false

## Canary → POS: Outbound Events

Canary is not purely a consumer. It pushes back to the POS:

| Push event | When | POS receives |
|---|---|---|
| **Item master add** | New item inducted in Canary | New PLU record: SKU, description, unit price, tax class, barcode. Operator confirms before activating. |
| **SOH sync** | After cycle count or receiving adjustment | Updated SOH for affected items. POS reconciles against its running count. |
| **Location data** | When item location changes in planogram | Item's zone/aisle/shelf position. Used for POS location lookup ("where is this item?") |
| **BOPIS ready** | Customer pick order fulfilled | Order status update → POS customer notification |
| **Price update** | If Canary-calculated pricing changes (markdown, promotion) | Price update to POS — requires operator confirmation before applying |

**Item master sync protocol:** new items created in Canary should NOT automatically appear in the POS without operator review. The push creates a "pending" PLU in Counterpoint back-office; the operator (or store manager with POS access) activates it. This prevents a misconfigured item from being scannable at the register before it's ready.

---
last-compiled: 2026-05-04
needs-review: false

## Android POS Register Screen — Canary Overlay

Where the integration becomes visible to the associate at the register:

**Inventory lookup (customer query):**
The register has a search function. When an associate searches for an item to answer a customer question, Canary's location data appears alongside the POS item data:

```
[Item Name]            PLU: 0000012847
Price: $4.99           On Hand: 14 units

📍 Location: Aisle 4 / Shelf B / Position 3
   (Canary live SOH: 14 ✓ matches)
```

This surfaces in the POS search results if Counterpoint's API supports custom data fields on the item record (it does — Counterpoint allows user-defined fields). The location string is pushed from Canary into a UDF on the Counterpoint item record during the outbound location sync.

**Special order / BOPIS:**
When a customer requests an item that's out of stock at the register, the cashier can initiate a special order without leaving the POS:

```
[Item] — OUT OF STOCK

  Customer wants this item?
  ○ Check back — no commitment
  ● Special order — expected [delivery date from Canary next PO]
  ○ Back-order — we'll call when in

  [ Create special order ]
```

This creates a special order record in both Counterpoint and Canary simultaneously. The cashier stays in the POS flow. Canary generates the pick task when the item arrives.

---
last-compiled: 2026-05-04
needs-review: false

## Offline Mode — What Happens When Connectivity Fails

**POS behavior (no Canary connectivity):**
The POS never depends on Canary being available to process a sale. If the Bridge is down, the POS continues transacting normally. Canary processes the missed events when connectivity restores — the polling bridge replays from the last successful timestamp.

**Canary mobile behavior (no connectivity):**
The mobile app operates in offline mode:
- Tasks in progress can be completed and confirmed locally (queued events)
- Receiving can be performed offline (scan + confirm, queued)
- SOH reads show "last synced X minutes ago" rather than live
- Hub exceptions are not refreshed (cached view shown)
- Events sync automatically when connectivity returns — no operator action required

**Conflict resolution on reconnect:** if an offline receiving event conflicts with a POS event processed while offline (e.g., the POS sold the last unit of something the app thought was still there), Canary flags the discrepancy and generates a cycle count task for that item. It does not auto-resolve — the physical count is the tiebreaker.

---
last-compiled: 2026-05-04
needs-review: false

## Credentials and Security

**API key architecture:**
- One API key pair per store (Counterpoint API key + Canary API key)
- Keys stored in Canary's secrets manager (never in client code or logs)
- Canary Bridge authenticates with Counterpoint using store-specific credentials
- Canary mobile authenticates with Canary using per-employee tokens (not store-level keys)

**Scope isolation:**
- The Bridge service only reads what it needs: Tickets, Inventory, Items, Vendors
- Write operations from Canary to Counterpoint (item master add, SOH sync) are scoped separately and require explicit operator authorization per action
- No bulk write access — the integration cannot mass-update Counterpoint records autonomously

**Per-store tenancy:**
Each store is a distinct tenant in Canary. Store A's POS events never appear in Store B's data. The Bridge, the SOH state, the task queue, the planogram — all are tenanted per store. Multi-store operators get a consolidated view in the Hub analytics, but execution is always store-scoped.

---
last-compiled: 2026-05-04
needs-review: false

## Integration Onboarding — Setup Wizard

For Bart's team deploying to a new store:

```
Step 1: Connect POS
  ○ NCR Counterpoint
  ○ Square
  ○ Clover
  ○ Manual (no integration — enter data manually)

Step 2: Enter Counterpoint API credentials
  Store URL: [ _________________ ]
  API Key:   [ _________________ ]
  [ Test connection ]   → "✓ Connected to [Store Name] Counterpoint 9.4"

Step 3: Item sync
  Canary found 847 items in Counterpoint.
  [ Import all items ]
  [ Import active items only (recommended) ]

Step 4: Historical data
  Pull last 8 weeks of sales for velocity calculation?
  [ Yes — this takes ~5 minutes ]   [ Skip — start from today ]

Step 5: Done
  POS integration active. Syncing every 60 seconds.
```

The 8-week historical pull is critical for the demand sensing to have enough data to set Auto replenishment parameters. Without it, the velocity model starts cold and takes 8 weeks to become useful. With it, the replenishment engine is ready to generate intelligent proposed orders on day one.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-operations-hub]] · [[Brain/wiki/cards/canary-demand-sensing-smb]] · [[Brain/projects/Canary]]
