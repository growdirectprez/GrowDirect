---
type: spec
title: Counterpoint → Canary Go UX Crosswalk
status: draft
date: 2026-05-04
source: Brain/wiki/ncr-counterpoint-functional-decomposition.md × docs/superpowers/specs/2026-05-03-canary-go-ui-wave-plan.md
gro: TBD
purpose: Map every Counterpoint functional area to Canary Go wave-plan screens; identify gaps, deliberate skips, and UX displacement targets; produce wave plan amendments
---

# Counterpoint → Canary Go UX Crosswalk

**Governing thesis:** Counterpoint's ~600 features decompose into four categories against the Canary Go wave plan: Covered (already in the wave plan), Gap-Add (Counterpoint has it, wave plan doesn't, Canary should), Gap-Skip (Counterpoint has it, Canary deliberately doesn't — out of scope or positioned differently), and Displacement (Canary builds the same capability but does it better). This document is the product design source for wave plan amendments and UX design briefs.

**Input:** 95 Counterpoint maintenance forms × 70 Canary Go wave-plan screens.

**Output:** Gap registry, displacement target list, wave plan amendment recommendations.

---

## Status Legend

| Status | Meaning |
|---|---|
| ✅ Covered | Wave plan already addresses this |
| ➕ Gap — Add | Counterpoint has it; Canary wave plan does not; should add |
| ⏭ Gap — Skip | Counterpoint has it; Canary deliberately does not (out of scope / above-the-POS positioning) |
| 🔁 Displacement | Canary builds the same capability but redesigns the UX |
| ⚠️ Partial | Wave plan touches this but incompletely |

---

## 1. Point of Sale (Register UI)

Counterpoint's register/cashier surface is explicitly out of Canary's scope. Canary is *above* the POS — the register stays as Counterpoint/RapidPOS. However, Canary must observe, audit, and analyze everything that happens at the register.

| Counterpoint Feature | Status | Canary Equivalent / Note |
|---|---|---|
| Ticket Entry — standard and touchscreen | ⏭ Gap — Skip | Canary reads tickets; never writes them. POS session is CP/RapidPOS territory |
| Orders (sales order create/edit/release) | ⏭ Gap — Skip | Order data flows into Canary via T-module feed; Canary doesn't originate orders |
| Layaways (create/payment/pickup/cancel) | ⏭ Gap — Skip | Same — Canary reads layaway activity; no origination |
| Quotes and Holds | ⏭ Gap — Skip | Read-only via T module |
| Drawer management (activate/open/close/payin/payout) | ⚠️ Partial | Wave 2 N-module: drawer threshold config (`/settings/store/drawer`) exists. Missing: live drawer session status, X/Z-tape equivalent view |
| End of Day / X-Tape / Z-Tape | ➕ Gap — Add | No Canary equivalent. Operators need a daily financial close view. Add: **EOD summary dashboard** (`/reports/eod`) — shows day totals, tender mix, variance vs prior period. Wave 3 F-module scope |
| Credit card settlement | ⏭ Gap — Skip | CPGateway handles settlement; Canary sees tender totals, not processor batch |
| Validated returns | ✅ Covered | Q-module: return anomaly detection covers this from LP side |
| Gift certificates — sell/redeem | ⏭ Gap — Skip | Canary reads gift cert lines on tickets; no origination |
| Stored value cards — activate/recharge/redeem | ⏭ Gap — Skip | Same |
| Pay-in / pay-out transactions | ⚠️ Partial | Q Q-DC-01 (drawer cash detection) covers anomalies; no Canary UI for initiating pay-in/out |
| Receipt printing | ⏭ Gap — Skip | Hardware-side; not a web portal concern |
| Price Exceptions report | ✅ Covered | Q-module: discount cap detection (Q-DR-01) is the analytical equivalent |
| Alcohol verification / ID scan | ⏭ Gap — Skip | Register-side; not a Canary surface |

**POS net gap to add:** EOD summary dashboard (Wave 3 F extension).

---

## 2. Inventory

The largest gap domain. Counterpoint's inventory surface has deep workflow UI (physical count, transfers, adjustments, label printing) that the wave plan barely touches.

| Counterpoint Feature | Status | Canary Equivalent / Note |
|---|---|---|
| Item maintenance — full record (all tabs) | ⚠️ Partial | Wave 2: `/items/:id` shows display attributes and margin target. Missing: edit item, create item, manage barcodes, manage alternate units |
| Quick Items (add-on-the-fly) | ➕ Gap — Add | No Canary UI to create or edit items. Add: **Item create/edit form** (`/items/new`, `/items/:id/edit`) — Wave 2 S extension |
| Item categories / sub-categories | ⚠️ Partial | Category performance (`/reports/category`) reads categories; no category management UI |
| Item attributes (6 configurable) | ➕ Gap — Add | No management UI. Add: **Attribute config** (`/settings/catalog/attributes`) — Wave 2 admin scope |
| Item profile codes (5×4 = 20 custom fields) | ➕ Gap — Add | No UI. Add: **Catalog config** (`/settings/catalog`) — consolidate all catalog setup. Wave 2 admin |
| Barcode management | ➕ Gap — Add | No Canary barcode UI. Add: **Barcode management** tab on `/items/:id/edit`. Wave 2 S |
| Pricing — regular / location-specific | ⚠️ Partial | Wave 4: Price change history (`/reports/price-history`). Missing: edit prices. Add: **Item price edit** on item detail |
| Special prices (date-ranged) | ➕ Gap — Add | No Canary UI. Add to: **Promotion calendar** (`/promotions`) as special price entry — Wave 4 P |
| Contract prices (customer-specific) | ➕ Gap — Add | No equivalent. Add: **Customer contract prices** tab on `/customers/:id`. Wave 4 P |
| Promotional prices + planned promotions | ✅ Covered | Wave 4: `/promotions` (promotion calendar). Needs edit capability, not just read |
| Mix-and-match codes and rules | ➕ Gap — Add | No Canary UI. Add: **Price rules** (`/settings/pricing/rules`) — Wave 4 P. CP has this buried in 2 separate forms; Canary unifies |
| BOGO / twofer rules | ➕ Gap — Add | Same — price rules management |
| Price Test (simulate price for item × customer × qty) | 🔁 Displacement | Counterpoint: standalone `frmpricetest` form. Canary: **unified price simulator** embedded in item detail — shows all applicable prices in one view. Major UX win |
| **Physical Count — Create batch** | ➕ Gap — Add | No Canary UI. **Critical workflow gap.** Add: `/inventory/count/new` — filter by location, item selection, date |
| **Physical Count — Enter counts** | ➕ Gap — Add | No Canary UI. Add: `/inventory/count/:id` — mobile-friendly count entry (CP's version is Windows-only) |
| **Physical Count — Post** | ➕ Gap — Add | No Canary UI. Add: `/inventory/count/:id/post` — confirm and post with GL distributions |
| Physical Count — Import from file | ➕ Gap — Add | No Canary UI. Add: file upload on count session. Wave 2 D extension |
| **Transfer Out — initiate** | ➕ Gap — Add | Wave 2 has `/transfers/:id` (detail) and variance review but **no create**. Add: `/transfers/new` — select items, quantities, source/destination location |
| Transfer In — receive | ➕ Gap — Add | No separate receive UI in wave plan. Add: `/transfers/:id/receive` — confirm receipt quantities |
| Transfer variance — review and post | ✅ Covered | Wave 2: `/transfers/:id/variance` |
| Inventory adjustments entry | ➕ Gap — Add | No Canary UI for manual adjustments. Add: `/inventory/adjustments/new` — Wave 2 D |
| Import inventory adjustments | ➕ Gap — Add | No UI. Add: file import on adjustment screen |
| Committed Inventory (reserved by orders) | ➕ Gap — Add | No Canary equivalent. Add: **Committed inventory view** on `/items/:id` — shows on-hand vs committed vs available. Wave 2 S |
| Bills of Material / Quick Assembly | ⏭ Gap — Skip | Enterprise-only option; not in Canary Phase 1–3 scope |
| Serial / Lot tracking | ⚠️ Partial | T-module reads serial numbers on tickets; no Canary UI for serial management |
| Label printing | ⏭ Gap — Skip | Hardware-side; web portal doesn't print thermal labels. Note: Canary can trigger print jobs via MCP (future) |
| Location / Location group management | ➕ Gap — Add | No Canary UI. Add: **Location config** (`/settings/store/locations`) — Wave 2 N extension |
| Tare weight codes | ⏭ Gap — Skip | Specialized; not a priority |
| Renumber Items utility | ⏭ Gap — Skip | Admin utility; not a frequent operation |

**Inventory net gaps to add (critical path):** Physical count workflow (3 screens), Transfer initiation + receipt (2 screens), Inventory adjustment entry (1 screen), Item create/edit (2 screens), Committed inventory view (1 view on existing screen).

---

## 3. Customers

Wave 1 covers the *investigator* view of customers (LP context). Missing: the *operator* view (A/R management, loyalty management, relationship maintenance).

| Counterpoint Feature | Status | Canary Equivalent / Note |
|---|---|---|
| Customer record — full form (all tabs) | ⚠️ Partial | Wave 1: `/customers/:id` shows purchase history and risk score. Missing: edit customer, manage ship-to addresses, manage contacts, A/R status |
| Quick Customers (add-on-the-fly) | ➕ Gap — Add | No Canary UI to create customers. Likely Phase 2+ scope but should be planned |
| Customer categories | ➕ Gap — Add | No Canary UI. Add: **Customer categories** config (`/settings/customers/categories`) |
| Ship-to addresses (multiple) | ➕ Gap — Add | No Canary UI. Add: Ship-to tab on `/customers/:id/edit` |
| Credit limit / credit rating management | ➕ Gap — Add | No Canary UI. Add: A/R tab on customer detail |
| **A/R Account Management** (view open items, history) | ➕ Gap — Add | No Canary equivalent. Add: `/customers/:id/ar` — open items, balance, aging. Wave 3 F |
| **Cash Receipts entry** | ⏭ Gap — Skip | Full A/R workflow is accountant territory; Canary is analytics layer. Canary reads cash receipts; doesn't write them. Flag for Phase 3+ |
| **Customer Adjustments** (debit/credit memos) | ⏭ Gap — Skip | Same — A/R write operations deferred |
| Finance charges calculation | ⏭ Gap — Skip | A/R write operation; deferred |
| Statements printing | ➕ Gap — Add | Canary can generate PDF statements. Add: **Statement generation** (`/customers/:id/statement`) — Wave 3 F |
| Merge customers | ⏭ Gap — Skip | Admin utility |
| Import customers | ➕ Gap — Add | No Canary UI. Add: bulk import on customers list — Wave 2+ |
| **Loyalty programs — define programs** | ➕ Gap — Add | No Canary management UI. Add: `/settings/loyalty/programs` — configure earning rules, redemption rules per program. Wave 4 |
| **Loyalty — enroll customer** | ➕ Gap — Add | No Canary UI. Add: Loyalty tab on customer detail — enroll, view balance, history |
| **Loyalty — manual point adjustments** | ➕ Gap — Add | No Canary UI. Add: point adjustment form on loyalty tab |
| Loyalty — view point balance and history | ✅ Covered | Implied by customer detail; needs explicit loyalty history section |
| Gift registry | ⏭ Gap — Skip | Niche feature; not in Canary scope Phase 1–3 |
| Commission codes | ⏭ Gap — Skip | Not in Canary scope |

**Customer net gaps to add (critical path):** A/R balance view on customer detail, Loyalty program configuration screens, Loyalty enrollment + adjustment on customer detail, Customer A/R open items view.

---

## 4. Purchasing

Wave 3 covers receiving and RTV. Missing: the upstream PO workflow and vendor management.

| Counterpoint Feature | Status | Canary Equivalent / Note |
|---|---|---|
| **Vendor record management** | ➕ Gap — Add | No Canary UI for vendor create/edit. Add: `/vendors` list + `/vendors/:id` detail + `/vendors/new` — Wave 3 J |
| Vendor categories | ➕ Gap — Add | Add: Vendor categories config (`/settings/purchasing/vendor-categories`) |
| **Purchase Order — create** | ➕ Gap — Add | Wave 3 has suggested orders but **no PO creation UI**. Add: `/orders/new` (buyer approves suggested → creates PO) — Wave 3 J |
| **Purchase Order — edit / cancel / reissue** | ➕ Gap — Add | No Canary UI. Add: `/orders/:id/edit`, cancel action on order detail |
| Purchase Order — print / email | ➕ Gap — Add | Add: PDF export on order detail |
| **Purchasing Advice / replenishment** | ✅ Covered | Wave 3: `/orders/suggested` (Suggested orders list). Maps to CP's Purchasing Advice |
| Purchasing Advice — by Days of Supply | ⚠️ Partial | Suggested orders exist; Days of Supply calculation needs to be in the algorithm |
| Purchasing Advice — cell-level (matrix items) | ⚠️ Partial | Suggested orders need to handle grid items |
| Customer-specific purchases (buy for a customer) | ➕ Gap — Add | No Canary UI. Add: "Order for customer" flag on PO creation — Wave 3 |
| **Receiving — entry** | ✅ Covered | Wave 3: `/receiving/:id` (line entry, close) |
| Receiving — without a PO (blind receiving) | ➕ Gap — Add | No Canary UI. Add: "Receive without PO" option on receiving sessions list |
| Receiving — import from file | ➕ Gap — Add | Add: file import on receiving session |
| Miscellaneous charges on receiving (freight) | ⚠️ Partial | Wave 3 receiving screens exist; misc charges tab needs to be in the receiving form |
| Purchasing Adjustments (post-receive cost correction) | ➕ Gap — Add | No Canary UI. Add: `/receiving/:id/adjust` — cost correction after vouchering |
| **Return-to-Vendor (RTV)** | ✅ Covered | Wave 3: `/returns/:id` (RTV detail, qty confirmation, credit reconciliation) |
| RTV — create | ⚠️ Partial | Wave 3 has RTV list (`/returns`) but initiation UI unclear. Add: `/returns/new` |
| Vouchering receivings (approve for A/P) | ➕ Gap — Add | No Canary UI. Add: **Voucher action** on receiving close — marks receiving as approved for accounting |
| Unvouchered / Vouchered Receivings reports | ✅ Covered | Implied by receiving reports in Wave 3 |

**Purchasing net gaps to add (critical path):** Vendor list + detail + create (3 screens), PO create + edit (2 screens), Blind receiving option, Vouchering action on receiving close.

---

## 5. Sales History & Reporting

| Counterpoint Feature | Status | Canary Equivalent / Note |
|---|---|---|
| View Ticket History (search + filter) | ✅ Covered | Wave 2: `/transactions` (list) + `/transactions/:id` (detail) |
| Reprint ticket | ➕ Gap — Add | Add: PDF export on transaction detail |
| Management History (aggregated) | ✅ Covered | Wave 2: `/reports/distribution`, Wave 3: `/reports/finance` — covers this |
| MarketBasket / basket analysis | ➕ Gap — Add | No Canary UI. Add: **Basket analysis view** (`/reports/basket`) — co-purchase frequency. Wave 4 or Wave 5 |
| Sales Analysis by Color/Size (matrix) | ➕ Gap — Add | No Canary equivalent for matrix-item drill. Add: **Grid sales report** (`/reports/grid`) — Wave 4 S |
| Flash Sales report (intraday pacing) | ➕ Gap — Add | No Canary equivalent. Add: **Intraday sales pacing** widget on dashboard or `/reports/flash` — Wave 2 |
| Tax History report | ✅ Covered | Wave 3: `/reports/tax` |
| Price Exceptions History | ✅ Covered | Q-module: Q-DR-01 is the analytical equivalent |
| Purge Ticket History | ⏭ Gap — Skip | Admin utility; data lifecycle managed at infrastructure level |
| Markdown History | ✅ Covered | Wave 4: `/reports/markdowns` |

---

## 6. Finance

| Counterpoint Feature | Status | Canary Equivalent / Note |
|---|---|---|
| Financial summary (daily/weekly/period P&L) | ✅ Covered | Wave 3: `/reports/finance` |
| Payment method report (tender mix) | ✅ Covered | Wave 3: `/reports/payments` |
| Tax liability report | ✅ Covered | Wave 3: `/reports/tax` |
| **EOD close summary** | ➕ Gap — Add | See POS section. Add: `/reports/eod` — daily close with settlement totals, variance vs plan |
| GL distributions — view per transaction type | ➕ Gap — Add | No Canary UI. Add: **Distribution audit** (`/transactions/:id/distributions`) — shows GL impact per ticket. Wave 3 F |
| Accounting Interface (export to QuickBooks/MAS 90) | ➕ Gap — Add | No Canary export UI. Add: **Accounting export** (`/settings/integrations/accounting`) — Wave 3 or admin |
| Finance charges | ⏭ Gap — Skip | A/R write operation; deferred |
| Cash receipts journal | ⏭ Gap — Skip | A/R write; deferred |
| Purge distributions | ⏭ Gap — Skip | Admin utility |

---

## 7. Timecards / Labor

Counterpoint's timecard surface is thin (clock in/out, maintain, export). Canary Wave 4 goes deeper on analytics but misses the transactional side.

| Counterpoint Feature | Status | Canary Equivalent / Note |
|---|---|---|
| Clock in / clock out | 🔁 Displacement | Counterpoint: Windows desktop time clock station. Canary: **mobile-web clock-in** via `/timeclock` — no Windows dependency. Major UX win |
| Maintain timecards (edit entries — manager) | ➕ Gap — Add | No Canary UI. Add: **Timecard editor** (`/timecards`) — manager view with edit capability. Wave 4 L |
| Timecards report | ✅ Covered | Wave 4: `/reports/labor` (productivity dashboard subsumes this) |
| Export timecard entries (payroll) | ➕ Gap — Add | No Canary UI. Add: **Payroll export** (`/timecards/export`) — CSV/flat file for payroll systems. Wave 4 L |
| Employee record management | ⚠️ Partial | Wave 4: `/employees/:id` (detail) — read-only. Add: employee edit |
| Timecard settings per user | ➕ Gap — Add | Add: Timecard settings on employee detail |

---

## 8. System / Setup / Configuration

Counterpoint has 95 maintenance forms. Most are configuration that Canary handles through its own settings. This section separates what Canary needs vs what's CP-internal plumbing.

| Counterpoint Area | Status | Canary Equivalent / Note |
|---|---|---|
| Company settings | ⏭ Gap — Skip | This is CP configuration; Canary has tenant config |
| **Tenant / store config** (N-module setup) | ✅ Covered | Wave 2: `/settings/store` (store config viewer, N.1–N.3) |
| Tax codes / tax authorities | ➕ Gap — Add | No Canary UI. Add: **Tax config** (`/settings/tax`) — Canary needs to know tax rules for cost modeling. Wave 3 |
| Pay codes (tender types) | ➕ Gap — Add | No Canary UI for pay code management. Add: `/settings/paycodes` — Wave 3 admin |
| Security codes / user roles | ✅ Covered | Admin (cross-wave): `/admin/users`, role assignment |
| User records | ✅ Covered | Admin: `/admin/users/:id` |
| Menu codes (CP menu customization) | ⏭ Gap — Skip | CP-internal; not relevant to Canary |
| Inventory Control settings | ⚠️ Partial | `/settings/store` partially covers this; need dedicated inventory settings |
| Customer Control settings | ➕ Gap — Add | No Canary equivalent for loyalty program defaults and A/R settings. Add: `/settings/customers` — Wave 4 admin |
| POS Control settings | ⏭ Gap — Skip | CP-internal configuration |
| Purchasing Control settings | ➕ Gap — Add | Add: `/settings/purchasing` — min/max logic, receiving defaults. Wave 3 admin |
| Commission codes | ⏭ Gap — Skip | Not in Canary scope |
| Ship-via codes | ➕ Gap — Add | Add: to purchasing settings (`/settings/purchasing/ship-via`). Wave 3 |
| Calendars (seasonal date ranges) | ➕ Gap — Add | Canary needs calendars for promotion scheduling and reporting. Add: `/settings/calendar` — Wave 4 P |
| Batches (workgroup defaults) | ⏭ Gap — Skip | CP workflow concept; Canary doesn't use batch processing |
| Data Verify / Database utilities | ⏭ Gap — Skip | Admin-level; infrastructure |
| Data migration | ⏭ Gap — Skip | One-time; handled via ETL, not portal UI |
| Audit log | ✅ Covered | Admin: `/admin/audit` (identity events + T.2.6 mutation-lock) |
| Multi-Site replication config | ⏭ Gap — Skip | CP-internal; Canary's cloud architecture supersedes this |
| Offline Ticket Entry (CPServices) | ⏭ Gap — Skip | CP-internal offline sync; Canary handles connectivity differently |

---

## 9. Gap Registry — Screens to Add

Consolidated list of new screens the wave plan should add, organized by priority:

### Priority 0 — Operational Blockers (add to Wave 2–3)

| Screen | URL | Module | Wave |
|---|---|---|---|
| Physical Count — create | `/inventory/count/new` | D / inventory | Wave 2 |
| Physical Count — enter counts | `/inventory/count/:id` | D / inventory | Wave 2 |
| Physical Count — post | `/inventory/count/:id/post` | D / inventory | Wave 2 |
| Transfer — initiate | `/transfers/new` | D | Wave 2 |
| Transfer — receive | `/transfers/:id/receive` | D | Wave 2 |
| Inventory adjustment — create | `/inventory/adjustments/new` | D | Wave 2 |
| Vendor list | `/vendors` | J | Wave 3 |
| Vendor detail + edit | `/vendors/:id` | J | Wave 3 |
| Purchase Order — create | `/orders/new` | J | Wave 3 |
| Purchase Order — detail + edit | `/orders/:id` | J | Wave 3 |
| Blind receiving (no PO) | option on `/receiving` | J | Wave 3 |
| EOD summary dashboard | `/reports/eod` | F | Wave 3 |

### Priority 1 — Operator Completeness (add to Wave 3–4)

| Screen | URL | Module | Wave |
|---|---|---|---|
| Item create | `/items/new` | S | Wave 2–3 |
| Item edit | `/items/:id/edit` | S | Wave 2–3 |
| Customer A/R open items | `/customers/:id/ar` | C / F | Wave 3 |
| Customer statement PDF | `/customers/:id/statement` | C / F | Wave 3 |
| Timecard editor (manager) | `/timecards` | L | Wave 4 |
| Payroll export | `/timecards/export` | L | Wave 4 |
| Mobile clock-in | `/timeclock` | L | Wave 4 |
| Loyalty program config | `/settings/loyalty/programs` | C | Wave 4 |
| Loyalty enrollment + adjustment (customer) | `/customers/:id/loyalty` | C | Wave 4 |
| Price rules management | `/settings/pricing/rules` | P | Wave 4 |
| Calendar management | `/settings/calendar` | P | Wave 4 |
| Contract prices (per customer) | `/customers/:id/prices` | P | Wave 4 |

### Priority 2 — Analytics Completeness (add to Wave 4–5)

| Screen | URL | Module | Wave |
|---|---|---|---|
| Intraday sales pacing (Flash Sales) | `/reports/flash` | T | Wave 2 |
| Grid sales report (Color/Size) | `/reports/grid` | S | Wave 4 |
| Basket analysis | `/reports/basket` | Q / analytics | Wave 4–5 |
| GL distribution audit (per ticket) | `/transactions/:id/distributions` | F | Wave 3 |
| Accounting export config | `/settings/integrations/accounting` | F | Wave 3–4 |
| Committed inventory view (on item detail) | `/items/:id` tab | D / S | Wave 2 |

---

## 10. UX Displacement Targets

Where Canary doesn't just match Counterpoint but explicitly redesigns the experience. These are the UX wins to make explicit in the design brief.

### 1. Unified Price Simulator
**CP approach:** 7 separate forms (Regular prices, Special prices, Contract prices, Promotional prices, Planned promotions, Mix-and-match codes, Price test) — no unified view.  
**Canary approach:** Single **Price Intelligence** surface on item detail. Input: item × customer × quantity × date × store. Output: all applicable prices ranked by precedence, final price shown. Includes price history sparkline and margin impact.

### 2. Physical Count — Mobile-First
**CP approach:** Windows desktop only. Create batch → print paper worksheets → enter counts at a PC → post.  
**Canary approach:** Mobile-web count session. Scan barcode, enter count on phone, auto-save. Manager reviews exceptions on portal. Eliminates paper entirely.

### 3. Real-Time Inventory Truth
**CP approach:** Multi-Site replication is batch (DataXtend engine). Cross-store inventory is always stale.  
**Canary approach:** Perpetual ledger (D-module) continuously updated via TSP feed. `/inventory/:id` shows real-time position across all locations. Transfer recommendations fire as the position changes.

### 4. Purchasing Advice as Continuous Signal
**CP approach:** Purchasing Advice is a report you run manually. Output is a static printout.  
**Canary approach:** `/orders/suggested` is a live queue — items surface automatically when min thresholds are breached or Days of Supply drops below target. Buyer reviews queue, approves/adjusts, creates PO in one flow.

### 5. Loyalty Configuration — Live Preview
**CP approach:** Configure earning rules, redemption rules, program parameters across 3+ separate setup screens with no preview of how rules interact.  
**Canary approach:** Loyalty program builder with rule preview. Add an earning rule, see instantly what a $50 purchase earns. Add a redemption rule, see what points buy. Configuration and simulation in one screen.

### 6. Timecard — Mobile Clock-In
**CP approach:** Dedicated Windows time clock station (physically installed hardware). Employees clock in on Windows PC.  
**Canary approach:** Mobile-web `/timeclock` — employees clock in on any phone or shared tablet. Manager reviews and edits on portal. Eliminates dedicated hardware requirement.

### 7. Audit Trail on Every Transaction
**CP approach:** No audit trail. Ticket history is read-only; no cryptographic integrity.  
**Canary approach:** Every transaction carries hash-before-parse seal (T.2.3) + Merkle anchor (T.5.x). `/transactions/:id/proof` shows cryptographic audit proof. Operator can prove to an auditor that a ticket was not altered after close.

### 8. Transfer Variance as Automatic Alert
**CP approach:** Transfer variance (in-transit shrink) is discovered only when the Transfer In is manually entered and compared. No automatic detection.  
**Canary approach:** D-module detects variance the moment Transfer In is posted. `/transfers/:id/variance` surfaces automatically with shrink amount and LP context. Q-module picks up repeat patterns.

### 9. Cross-Store Visibility Without Multi-Site
**CP approach:** Multi-Site option costs extra, requires DataXtend installation, and is still batch. Single-store operators have no cross-store view.  
**Canary approach:** All stores feed into the same perpetual ledger. Cross-store comparisons (inventory, sales, LP risk) are native — no additional configuration.

### 10. Reporting — Ad-Hoc vs Crystal Reports Lock-In
**CP approach:** Every report is pre-built Crystal Reports. No ad-hoc query. Customization requires a developer.  
**Canary approach:** Reports are parameterized surfaces backed by live data. Owl (semantic query surface) handles ad-hoc questions in natural language. No Crystal Reports dependency.

---

## 11. Navigation Architecture Amendment

The wave plan's sidebar proposal needs amendments for the new screens:

```
Dashboard
──────────────
Alerts              (Q — Wave 1)
Chirps              (Q — Wave 1)
Rules               (Q — Wave 1)
Cases               (Q hawk — Wave 1 + W Wave 5)
Customers           (C — Wave 1)
Exceptions          (W — Wave 5)
──────────────
Transactions        (T — Wave 2)
Transfers           (D — Wave 2)
  └ New Transfer    [NEW]
  └ Receive Transfer [NEW]
Inventory           [NEW SECTION]
  ├ Items           (S — Wave 2)
  ├ Physical Count  [NEW — Wave 2]
  └ Adjustments     [NEW — Wave 2]
Receiving           (J — Wave 3)
  └ New Receiving   [NEW]
Orders / POs        [NEW SECTION — Wave 3]
  ├ Purchase Orders [NEW]
  └ Suggested Orders (J — Wave 3)
Returns / RTV       (J — Wave 3)
Vendors             [NEW — Wave 3]
──────────────
Reports
  ├ EOD Summary     [NEW — Wave 3]
  ├ Finance         (F — Wave 3)
  ├ Flash Sales     [NEW — Wave 2]
  ├ Category        (S — Wave 2)
  ├ Grid (Color/Size) [NEW — Wave 4]
  ├ Range           (S — Wave 4)
  ├ Distribution    (D — Wave 2)
  ├ OTB             (J — Wave 3)
  ├ Labor           (L — Wave 4)
  ├ Pricing         (P — Wave 4)
  ├ Basket Analysis [NEW — Wave 5]
  └ Cases           (W — Wave 5)
Employees           (L — Wave 4)
Timecards           [NEW — Wave 4]
Promotions          (P — Wave 4)
──────────────
Settings
  ├ Store Config    (N — Wave 2)
  ├ Locations       [NEW — Wave 2]
  ├ Devices         (N — Wave 2)
  ├ Tax             [NEW — Wave 3]
  ├ Pay Codes       [NEW — Wave 3]
  ├ Purchasing      [NEW — Wave 3]
  ├ Loyalty         [NEW — Wave 4]
  ├ Pricing Rules   [NEW — Wave 4]
  ├ Calendar        [NEW — Wave 4]
  ├ Integrations    [NEW — Wave 3–4]
  ├ Alert Routing   (Q — Wave 1)
  ├ Allow-lists     (Q — Wave 1)
  ├ LP Thresholds   (N.4 — Wave 1)
  └ Training Mode   (Q — Wave 1)
──────────────
Owl                 (semantic — existing)
Admin               (identity — GRO-770)
  └ Time Clock      [NEW — Wave 4]
```

---

## 12. Wave Plan Amendment Summary

| Addition | Screens | Priority | Recommended Wave |
|---|---|---|---|
| Physical Count workflow | 3 | P0 | Wave 2 |
| Transfer initiation + receipt | 2 | P0 | Wave 2 |
| Inventory adjustments create | 1 | P0 | Wave 2 |
| Flash Sales / intraday pacing | 1 | P0 | Wave 2 |
| Committed inventory view (tab on item detail) | 1 tab | P0 | Wave 2 |
| Item create + edit | 2 | P1 | Wave 2–3 |
| Vendor list + detail + create | 3 | P1 | Wave 3 |
| PO create + detail + edit | 2 | P1 | Wave 3 |
| Blind receiving option | 1 option | P1 | Wave 3 |
| Vouchering action on receiving | 1 action | P1 | Wave 3 |
| EOD summary dashboard | 1 | P1 | Wave 3 |
| Customer A/R open items view | 1 | P1 | Wave 3 |
| Customer statement PDF | 1 | P2 | Wave 3 |
| Tax config | 1 | P1 | Wave 3 |
| Pay code management | 1 | P1 | Wave 3 |
| Accounting export config | 1 | P2 | Wave 3–4 |
| Timecard editor (manager) | 1 | P1 | Wave 4 |
| Mobile clock-in | 1 | P1 | Wave 4 |
| Payroll export | 1 | P1 | Wave 4 |
| Loyalty program config | 1 | P1 | Wave 4 |
| Loyalty tab on customer detail | 1 tab | P1 | Wave 4 |
| Contract prices tab on customer | 1 tab | P2 | Wave 4 |
| Price rules management | 1 | P1 | Wave 4 |
| Calendar management | 1 | P2 | Wave 4 |
| Grid sales report (Color/Size) | 1 | P2 | Wave 4 |
| GL distribution audit (per ticket) | 1 tab | P2 | Wave 3 |
| Basket analysis | 1 | P3 | Wave 5 |
| **Total new screens** | **~30** | | |

**Revised screen count:** 70 (original) + ~30 (additions) = **~100 screens** across 5 waves + admin.

---

*Source: Brain/wiki/ncr-counterpoint-functional-decomposition.md × docs/superpowers/specs/2026-05-03-canary-go-ui-wave-plan.md*  
*~600 Counterpoint features mapped. 10 UX displacement targets identified.*
