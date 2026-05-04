---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: complete
tags: [rms, orms, oracle, replenishment, screen-flows, user-stories, canary-context]
created: 2026-05-04
source: Oracle RMS / ORMS Replenishment Training Materials, Fresh & Easy / Tesco US, 2007
---
last-compiled: 2026-05-04
needs-review: false

# RMS Replenishment — Screen Flows & Business Logic

Oracle Retail Merchandising System (ORMS) training corpus from the Fresh & Easy implementation (2007). Seven sessions + step-by-step procedures covering the full supplier→warehouse replenishment lifecycle. This card extracts the screen flows, field-level data model, algorithms, and status machines as raw material for Canary user story development.

---
last-compiled: 2026-05-04
needs-review: false

## System Context

ORMS is a transactional database with a Windows GUI. Supply chain used it exclusively for Supplier→Warehouse replenishment — not store-level. Store replenishment (WH→Store) ran through GFO (Global Forecasting & Ordering).

**Integrations:**

| System | Data flow |
|---|---|
| Oracle Financials | Cost, supplier financial terms |
| Oracle WMS (RWMS) | Warehouse receiving confirmations |
| Oracle ReIM | Invoice matching via EDI |
| GFO | Group Forecasting & Ordering (WH→Store) |
| RDD Storeline | POS / store systems |
| TIMS | Tesco EDI middleware (ASN, PO, invoice, receipts) |
| Space/Range/Display | Item setup shared |

---
last-compiled: 2026-05-04
needs-review: false

## Data Hierarchy

**Organizational:**
Country → Geo-Area (4: N/S/E/W US) → Region → District → Store / Warehouse

**Merchandise:**
Department → Section → Class → Item (3 levels)

**Item Structure — critical for ordering:**

| Level | What it is | Used for |
|---|---|---|
| L1 | Case / orderable unit | Ordering (POs) |
| L2 | SKU — where replenishment params live | Replenishment setup |
| L3 | Barcode / each | POS, store SOH |

- Simple Pack (TPND) replenished but parameters set at L2 of the parent Regular Item
- Variants (flavor/color/scent) live at L2; each links to an L3 SKU
- Ordering quantity unit = Simple Pack (e.g., qty=1 = 24 eaches)

---
last-compiled: 2026-05-04
needs-review: false

## Replenishment Methods

Four methods, increasing complexity. F&E used only Min/Max and Dynamic-Issues.

### 1. Constant
- Maintains a fixed maximum stock level
- No forecast; high parameter maintenance
- Use: very slow sellers, items purchased in multiples

### 2. Min/Max
- Define minimum (order point) and maximum (order-up-to) stock levels
- Order fires when available inventory < minimum
- No forecast, no seasonality, no service level
- Manual parameter maintenance per SKU/location
- Risk: stockouts during promotions and seasonal peaks
- **Key fields:** Minimum Stock, Maximum Stock, Increment Percent

### 3. Time Supply
- Days-of-supply extension of Min/Max
- Calculates FDMIN and FDMAX from forecasts over min/max time supply windows
- **ROQ = FDMAX − NI** (if FDMIN > NI), else 0
- Optional Time Supply Horizon (TSH) shifts to rate-of-sale calculation
- Use: items where steady daily supply level is the objective

### 4. Dynamic — Issues *(primary for high-volume items)*
- Forecast-based, service-level-driven
- "Issues" = warehouse-to-store transfers (not sales)
- Most complex; requires accurate forecasts

**Dynamic algorithm inputs:**

| Field | Description |
|---|---|
| ISD (Inventory Selling Days) | Days of supply to hold to meet forecasted demand |
| Service Level % | % of demand satisfied from in-stock |
| Lost Sales Factor | % of lead-time lost sales fed back into future demand |
| COLT | Current Order Lead Time |
| NOLT | Next Order Lead Time |
| Review Time | Days between replenishment runs |

**Calculation structure:**
```
Safety Stock = f(Service Level %, σ of cumulative forecast over COLT)
Order Point  = Safety Stock + forecast demand over NOLT + review time
Order Up To  = Order Point + forecast demand over ISD
ROQ          = Order Up To - Net Inventory (if NI < Order Point)
```

---
last-compiled: 2026-05-04
needs-review: false

## Screen Flow 1 — Supplier Inventory Management Setup

*Start Menu → Control → Supplier*

**A. Supplier Search**
1. Highlight Control folder → double-click Supplier
2. Action = Edit → enter search criteria → Search → select supplier → OK

**B. Supplier Maintenance — Inventory Management**
3. Set Inventory Mgmt Level: Supplier / Supplier+Section / Supplier+Location / Supplier+Section+Location
4. Options menu → Inventory Mgmt Info/Totals

**C. SIM Information Screen — fields:**

| Section | Field | F&E Default |
|---|---|---|
| Replenishment | Review Cycle | Weekly (Sunday) |
| Replenishment | Order Control | Semi-Automatic |
| Supplier Minimums | Minimum Level | Order Level |
| Supplier Minimums | Purge Orders Failing Minimums | Unchecked |
| Truck Splitting | Split Orders Into Truckloads | Checked |
| Truck Splitting | Truck Split Method | Item Sequence |
| Truck Splitting | Auto Approve LTL Orders | Unchecked |
| Rounding | Rounding Level | Pallet |
| Rounding | Inner/Case/Layer Threshold | 51% |
| Rounding | Pallet Threshold | 25% |
| Scaling | Scale Orders to Constraints | Checked |
| Scaling | Scaling Objective | Minimum |
| Scaling | Scaling Level | Order Level |

**D. Constraints** (click Constraints button):
- Truck constraint type: Amount / Mass / Volume / Pallet / Case / Each / Stat Case
- Minimum constraint: up to 2 constraints with OR conjunction
- Scaling constraint: primary type + max/min values + tolerance %

**E. Delivery Schedule:**
5. From Supplier Maintenance → Options → Delivery Schedule
6. Select warehouse → set Frequency, delivery days, Start Time=0, End Time=0 → Apply → OK

*Order Control modes:* Manual (buyer creates all POs) · Semi-Automatic (system proposes, buyer approves) · Automatic (system creates and approves without human review) · Buyer Worksheet (buyer manages queue)

---
last-compiled: 2026-05-04
needs-review: false

## Screen Flow 2 — Replenishment Method Setup

*Start Menu → Items → Items*

**A. Item Search**
1. Highlight Items folder → double-click Items
2. Action = Edit → enter search criteria → Search → select item (L2) → OK

**B. Item Maintenance**
3. Check **Forecastable** flag in Attributes section
4. Click **Replenishment** in left nav

**C. Replenishment Attribute Maintenance**
5. Group Type = Warehouse; enter Warehouse = 101
6. Action = Activate
7. Stock Category = Warehouse Stocked
8. Confirm "Default from supplier?" → Yes (pulls Review Cycle, Order Control, Lead Time)
9. Select Primary Replenishment Pack (from LOV)
10. Set Activate Date; Presentation Stock = 0; enter Pick Up to Location Days

**D. Min/Max path:**
11. Replenishment Method = Min/Max
12. Enter Minimum Stock, Maximum Stock, Increment Percent = 100
13. Exempt From Scaling = Yes (Max Scale Amount disabled)
14. OK → OK → Close

**D. Dynamic-Issues path:**
11. Replenishment Method = Dynamic-Issues
12. Enter Inventory Selling Days, Service Level %, Lost Sales Factor
13. Exempt From Scaling = Yes
14. OK → OK → Close

*Note: Simple packs share replenishment params set at parent L2. A warning fires if required fields are unpopulated — cursor lands on the offending field.*

---
last-compiled: 2026-05-04
needs-review: false

## Screen Flow 3 — Manual PO Creation

*Start Menu → Ordering → Orders*

**A. Access**
1. Highlight Ordering folder → double-click Orders

**B. Create PO Header**
2. Action = New Order → OK
3. PO Header Maintenance fields:
   - Order Type: N/B (default)
   - Supplier: enter number or LOV search
   - Location Type: Warehouse; Location: 101
4. Click **Calculate Dates** → Not Before Date = expected WH arrival date

**C. Add Items**
5. Click Items button → Order Distribution Worksheet
6. Enter As = Item (radio button)
7. Enter Item # (or LOV) — order at L1 (Simple Pack / case level)
8. Country of Origin, Unit of Purchase, Supplier Case Size auto-default
9. Enter Quantity (in Simple Packs — qty 1 = one full case)
10. Click Apply Item → item moves to matrix above
11. Repeat for additional items → OK

**D. Apply Deals**
12. From PO Header → Apply Process → check Apply Deals → Online → OK
13. PO costs update based on active deal

**E. Submit and Approve**
14. Options → Submit → Yes
15. Options → Approve → Yes → Yes (update estimated in-stock date) → OK

---
last-compiled: 2026-05-04
needs-review: false

## PO Status Machine

```
New → Worksheet → Submitted → Approved → Closed
                                       ↘ Cancelled
```

**Edit permissions by status:**

| Action | Worksheet | Approved |
|---|---|---|
| Edit delivery dates | ✓ | ✓ |
| Add items | ✓ | ✓ (bring back to Worksheet first) |
| Delete items | ✓ | ✗ (must Cancel item) |
| Increase quantity | ✓ | ✓ (bring back to Worksheet) |
| Decrease quantity | ✓ | Cancel item only |
| Delete entire PO | ✓ | Cancel PO |
| Reinstate closed PO | — | Only if not yet received |

*Rule: Only bring an Approved PO back to Worksheet when increasing quantities or adding items. Never for decreases — use Cancel.*

---
last-compiled: 2026-05-04
needs-review: false

## Scaling

Optional facility to automatically scale orders up or down against truck/order constraints.

- **Dynamic items:** scaled by days-of-supply (demand-based)
- **Min/Max items:** scaled by eaches (stock-based)
- Scaling objective: Minimum (scale to minimum constraint) or Maximum
- Constraint types: Amount ($) · Mass · Volume · Case · Pallet · Each · Stat Case
- Gross weight only (not net/tare) for mass scaling
- Manual scaling available in the PO editing flow (Session 7)

---
last-compiled: 2026-05-04
needs-review: false

## Key Glossary — Fields That Map to Canary

| ORMS Term | Definition | Canary Analogue |
|---|---|---|
| Issues | WH→Store transfers | Store replenishment orders |
| ISD | Days of supply to hold vs. forecast | Inventory target horizon |
| Service Level % | % of demand met from stock | Fill rate target |
| Lost Sales Factor | Lead-time stockout demand fed back | Demand inflation for safety stock |
| COLT / NOLT | Current / Next order lead time | Supplier lead time (current vs. next cycle) |
| ROQ | Recommended Order Quantity (system output) | Suggested order qty |
| Order Control | Manual / Semi-Auto / Auto | Approval mode per supplier |
| Review Cycle | Frequency of replenishment run | Replenishment cadence |
| Forecastable flag | Item eligible for Dynamic method | Forecast-enabled toggle |
| Presentation Stock | Minimum display units (shelf face) | Visual minimum / display floor |
| Pick Up to Location Days | Transit days from supplier to WH | Lead time component |

---
last-compiled: 2026-05-04
needs-review: false

## Canary Screen Flow Implications

**Three workflows to implement directly:**

1. **Supplier setup** — SIM + delivery schedule + truck constraints as a wizard sequence. Order Control is the key mode selector (Semi-Auto is the SMB default).

2. **Item replenishment activation** — Method selection (Min/Max vs. Dynamic) with branching field set. The Forecastable flag is the gate to Dynamic. Canary should surface this as a method selector with inline explanation of trade-offs.

3. **PO lifecycle** — Status machine with edit-permission enforcement. The Worksheet→Approved gate is where human review happens in Semi-Auto mode. Canary's "pending orders" view is this queue.

**What RMS doesn't do that Canary should:**
- Real-time inventory (RMS was batch-loaded; Canary has live POS feeds)
- Store-level replenishment parameters (RMS delegated to GFO; Canary owns the full chain)
- Mobile / API-native access (RMS was thick-client Windows only)
- Algorithm transparency (RMS showed results, not the calculation; Canary should show the math)

[[Brain/wiki/cards/rpas-planning-paradigm]] · [[Brain/wiki/canary-go-portal]] · [[Brain/projects/Canary]]
