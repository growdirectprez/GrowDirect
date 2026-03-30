---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Jim QA Report — B-067-C: Square Capability Dashboard Shell
**Work Order:** B-067-C QA
**Date:** February 28, 2026
**File Under Test:** `Canary/static/square_explorer.html`
**Validated Against:** `_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md`
**Verdict:** **PASS**

---

## Checklist Results

### 1. Page Load & Structure — PASS
- [x] Page loads without console errors (zero errors in console)
- [x] Title: "Square Capability Explorer — elJeffe"
- [x] Background is dark (`#0a0d12` via `--bg` CSS variable)
- [x] Fonts load: Syne (headers), JetBrains Mono (code/data) — Google Fonts CDN

### 2. Header Bar (fixed top) — PASS
- [x] "ELJEFFE" wordmark — amber gradient, left-aligned (CSS `text-transform: uppercase` on "elJeffe")
- [x] "Square Capability Explorer" — center
- [x] "SANDBOX" badge — amber background, monospace
- [x] "MLE55GCYANCYT" — muted gray, monospace, right side

### 3. Hero Strip (3 stat tiles) — PASS
- [x] "16" — API FAMILIES
- [x] "4" — PHASE 1 LIVE
- [x] "85%" — PHASE 3 LP COVERAGE
- [x] Numbers are amber, labels are muted gray

**Note:** 85% is a design-choice metric. Cannot derive exact formula from Condor map. Not a blocking issue — it's a forward-looking coverage estimate.

### 4. Phase 1 Cards (4 cards) — PASS
- [x] Payments — green "LIVE" badge, `client.payments`, LP signal populated
- [x] Refunds — green "LIVE" badge, `client.refunds`, Chirp C-004 reference ("C-004: refund >$10")
- [x] Merchant Profile — green "LIVE" badge, `client.merchants`
- [x] Locations — green "LIVE" badge, `client.locations`
- [x] All four have "Fetch Live Data" buttons
- [x] Merchants + Locations auto-fetched on page load — error panel appears with "Backend not running" message (graceful failure confirmed)

### 5. Phase 2 Cards (8 cards) — PASS
- [x] Orders, Cash Drawers, Labor & Timecards, Inventory, Catalog, Customers, Team Members, Gift Cards — all present
- [x] All have amber "PHASE 2" badges
- [x] Cash Drawers: "POLL-ONLY (B-047) — needs polling adapter" in TSP component
- [x] Labor: "POLL-ONLY (B-047) — needs polling adapter" in TSP component
- [x] Catalog: "Reference data — supports Sub 2 parsing" in TSP component
- [x] Customers: "Reference data — supports card fingerprint correlation"
- [x] Team Members: "Reference data — supports employee attribution in detections"
- [x] All LP signals are populated (no "TODO" text anywhere)

### 6. Phase 3 Cards (4 cards) — PASS
- [x] Loyalty — gray "PHASE 3" badge
- [x] Invoices — gray "PHASE 3" badge
- [x] Disputes — gray "PHASE 3" badge
- [x] Subscriptions — dim "NOT PLANNED" badge
- [x] All LP signals populated

### 7. Fetch Button Behavior — PASS
- [x] Clicked "Fetch Live Data" on Payments card
- [x] Button showed "Fetching..." while loading (confirmed via JS: `btn.textContent = 'Fetching…'`)
- [x] Error panel appeared with red border (`response-panel error` class)
- [x] Count label: "NETWORK ERROR" (uppercase via CSS `text-transform`)
- [x] Message includes: "Backend not running. Start Flask app or wait for Jeremy B-067-B."
- [x] Button returns to "Fetch Live Data ▸" after error

**Note:** Error detail shows `SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON` because the static server returns HTML for the `/explore/` path. This is cosmetically noisy but functionally correct — the catch block handles it and shows the right guidance message. When Jeremy's Flask backend is live, this path will return real JSON.

### 8. TSP Pipeline Flow — PASS
- [x] 5 nodes: Square API → Sub 2: Parse + Route → Sub 1: Hash + Seal → Sub 3: Ordinal Inscribe → gLog Receipt
- [x] All nodes have green borders/glow (`active-node` class)
- [x] Arrows between nodes (→ entities)

### 9. Coverage Matrix (16 rows) — PASS
- [x] 6 columns: API Family, Webhook Events, Sub 1, Sub 2, Sub 3, Status
- [x] Payments + Refunds rows: green text, green checkmarks (✓) in Sub 1/2/3, "LIVE" status
- [x] Phase 2 rows: amber text, dashes (—) in Sub columns
- [x] Cash Drawers + Labor: show "POLL-ONLY (B-047)" in webhook column
- [x] Phase 3 rows: gray text
- [x] Subscriptions: dim "NOT PLANNED"
- [x] Merchants + Locations: dim "INFRA"
- [x] Table fits on screen without horizontal scroll at 1280px

**Row count:** 16 rows confirmed (Payments, Refunds, Orders, Catalog, Inventory, Customers, Cash Drawers, Labor, Team Members, Gift Cards, Loyalty, Invoices, Disputes, Subscriptions, Merchants, Locations).

### 10. Footer — PASS
- [x] "Sandbox only · No real transactions · Patent Pending · elJeffe by GrowDirect"
- [x] Centered, muted text

### 11. Responsive — PASS
- [x] At 375px (mobile): cards collapse to single column
- [x] Pipeline flow stacks vertically (arrows rotate 90° to point downward)
- [x] Header adapts: center title ("Square Capability Explorer") hides on mobile
- [x] Hero strip stacks vertically (single column)

### 12. Zero TODO Placeholders — PASS
- [x] `grep -i "TODO"` on source: zero matches
- [x] All LP signals populated with real data from Condor B-067-A capability map

---

## Condor B-067-A Cross-Validation

All 16 API families validated against `B067_SquareCapabilityMap_v1.0.md`:

| Family | SDK Namespace | Phase | LP Signal | Webhook Events | Match |
|---|---|---|---|---|---|
| Payments | client.payments | Phase 1 LIVE | Core transaction record | payment.created, payment.updated | MATCH |
| Refunds | client.refunds | Phase 1 LIVE | C-004 trigger | refund.created, refund.updated | MATCH |
| Orders | client.orders | Phase 2 | Line item detail | order.created, order.updated | MATCH |
| Catalog | client.catalog | Phase 2 | Reference data | N/A (reference) | MATCH |
| Inventory | client.inventory | Phase 2 | Shrinkage detection | inventory.count.updated | MATCH |
| Customers | client.customers | Phase 2 | Reference data | N/A (reference) | MATCH |
| Cash Drawers | client.cash_drawers.shifts | Phase 2 | Cash variance | POLL-ONLY (B-047) | MATCH |
| Labor | client.labor | Phase 2 | Ghost employee | POLL-ONLY (B-047) | MATCH |
| Team Members | client.team_members | Phase 2 | Reference data | N/A (reference) | MATCH |
| Gift Cards | client.gift_cards | Phase 2 | Load/redeem anomalies | gift_card_activity.created | MATCH |
| Loyalty | client.loyalty | Phase 3 | Point fraud | loyalty.event.created (TBD) | MATCH |
| Invoices | client.invoices | Phase 3 | Invoice manipulation | invoice.* (TBD) | MATCH |
| Disputes | client.disputes | Phase 3 | Chargeback patterns | dispute.* | MATCH |
| Subscriptions | client.subscriptions | Not Planned | Minimal LP relevance | N/A | MATCH |
| Merchants | client.merchants | Phase 1 LIVE (infra) | Merchant identity | N/A (infrastructure) | MATCH |
| Locations | client.locations | Phase 1 LIVE (infra) | Multi-location patterns | N/A (infrastructure) | MATCH |

**Result:** 16/16 families match. Zero discrepancies.

---

## Cosmetic Notes (non-blocking)

1. **Error panel SyntaxError detail:** When served from static server, `/explore/` paths return HTML 404 → JSON parse fails → shows `SyntaxError: Unexpected token...` before the "Backend not running" guidance. Functionally correct but visually noisy. Will resolve naturally when Jeremy's Flask backend (B-067-B) is wired.

2. **85% LP Coverage stat:** Forward-looking estimate. Cannot be derived from Condor map alone. Consider adding a tooltip or footnote explaining the calculation methodology when the backend is live.

3. **Coverage matrix on mobile:** Table requires horizontal scroll at 375px to see Sub 2/3/Status columns. This is expected behavior for a data-dense table — the `overflow-x: auto` wrapper handles it correctly.

---

## Verdict

**PASS — All 12 sections check out.** Dashboard shell is ready for Jeremy to wire the B-067-B backend endpoints. Zero blocking issues. Three cosmetic notes logged above for tracking.

---

*Jim | QA Manager | February 28, 2026 | B-067-C QA*
*Validated: source review + live browser QA (static server on port 8082) + Condor B-067-A cross-check*
