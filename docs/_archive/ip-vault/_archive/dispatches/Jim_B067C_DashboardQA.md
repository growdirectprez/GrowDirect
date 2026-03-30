---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jim Session Prompt — B-067-C QA: Square Capability Dashboard Shell
**Work Order:** B-067-C QA
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** HIGH — Qwen delivered, Jim validates before Jeremy wires backend

---

## Mission

QA the Square Capability Explorer dashboard shell. Qwen built it. It's on disk. You validate it before Jeremy hooks up the backend endpoints.

This is a **static HTML review** — the Flask backend (B-067-B) is not wired yet. Fetch buttons will show graceful "Backend not running" errors. That's expected. You're validating the shell, not the data.

---

## File Under Test

```
/Users/geofflyle/GrowDirect/Canary/static/square_explorer.html
```

Open it directly in a browser: `file:///Users/geofflyle/GrowDirect/Canary/static/square_explorer.html`

Or start the static server and navigate to `http://127.0.0.1:8082/square_explorer.html`:
```bash
cd /Users/geofflyle/GrowDirect/Canary/static && python3 -m http.server 8082
```

---

## QA Checklist

### 1. Page Load & Structure
- [ ] Page loads without console errors (font loading errors OK)
- [ ] Title: "Square Capability Explorer — elJeffe"
- [ ] Background is dark (#0a0d12 range)
- [ ] Fonts load: Syne (headers), JetBrains Mono (code/data)

### 2. Header Bar (fixed top)
- [ ] "ELJEFFE" wordmark — amber gradient, left-aligned
- [ ] "Square Capability Explorer" — center
- [ ] "SANDBOX" badge — amber background, monospace
- [ ] "MLE55GCYANCYT" — muted gray, monospace, right side

### 3. Hero Strip (3 stat tiles)
- [ ] "16" — API FAMILIES
- [ ] "4" — PHASE 1 LIVE
- [ ] "85%" — PHASE 3 LP COVERAGE
- [ ] Numbers are amber, labels are muted gray

### 4. Phase 1 Cards (4 cards)
- [ ] Payments — green "LIVE" badge, `client.payments`, LP signal populated
- [ ] Refunds — green "LIVE" badge, `client.refunds`, Chirp C-004 reference
- [ ] Merchant Profile — green "LIVE" badge, `client.merchants`
- [ ] Locations — green "LIVE" badge, `client.locations`
- [ ] All four have "Fetch Live Data" buttons
- [ ] Merchants + Locations auto-fetched on page load → show error panel with "Backend not running" message (expected — this is graceful failure)

### 5. Phase 2 Cards (8 cards)
- [ ] Orders, Cash Drawers, Labor & Timecards, Inventory, Catalog, Customers, Team Members, Gift Cards
- [ ] All have amber "PHASE 2" badges
- [ ] Cash Drawers + Labor show "POLL-ONLY (B-047)" warning in TSP component
- [ ] Catalog, Customers, Team Members show "Reference data" in TSP component
- [ ] All LP signals are populated (no "TODO" text anywhere)

### 6. Phase 3 Cards (4 cards)
- [ ] Loyalty — gray "PHASE 3" badge
- [ ] Invoices — gray "PHASE 3" badge
- [ ] Disputes — gray "PHASE 3" badge
- [ ] Subscriptions — dim "NOT PLANNED" badge
- [ ] All LP signals populated

### 7. Fetch Button Behavior
- [ ] Click any "Fetch Live Data" button on a card that didn't auto-fetch
- [ ] Button should say "Fetching..." while loading
- [ ] Error panel should appear with red border
- [ ] Message: "Backend not running. Start Flask app or wait for Jeremy B-067-B."
- [ ] Button returns to "Fetch Live Data ▸" after error

### 8. TSP Pipeline Flow
- [ ] 5 nodes: Square API → Sub 2: Parse + Route → Sub 1: Hash + Seal → Sub 3: Ordinal Inscribe → gLog Receipt
- [ ] Nodes have green borders/glow (active)
- [ ] Arrows between nodes

### 9. Coverage Matrix (16 rows)
- [ ] 6 columns: API Family, Webhook Events, Sub 1, Sub 2, Sub 3, Status
- [ ] Payments + Refunds rows: green text, green checkmarks (✓) in Sub 1/2/3, "LIVE" status
- [ ] Phase 2 rows: amber text, dashes (—) in Sub columns
- [ ] Cash Drawers + Labor: show "POLL-ONLY (B-047)" in webhook column
- [ ] Phase 3 rows: gray text
- [ ] Subscriptions: dim "NOT PLANNED"
- [ ] Merchants + Locations: dim "INFRA"
- [ ] Table fits on screen without horizontal scroll at 1280px+

### 10. Footer
- [ ] "Sandbox only · No real transactions · Patent Pending · elJeffe by GrowDirect"
- [ ] Centered, muted text

### 11. Responsive
- [ ] Resize browser to ~640px width
- [ ] Cards collapse to single column
- [ ] Pipeline flow stacks vertically
- [ ] Header adapts (center title may hide on mobile)

### 12. Zero TODO Placeholders
- [ ] Search page source (Ctrl+F / Cmd+F) for "TODO" — should find ZERO results
- [ ] All LP signals come from Condor B-067-A capability map (real data)

---

## Pass / Fail Criteria

**PASS** if all 12 sections check out. Minor cosmetic notes (spacing, alignment preferences) are logged but don't block.

**FAIL** if:
- Any card missing or showing wrong phase badge
- TODO placeholders present anywhere
- Fetch button doesn't fail gracefully
- Coverage matrix has wrong data (check against Condor B-067-A: `_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md`)
- Page has JS console errors (font loading warnings OK)

---

## Output

Write your QA report to:
```
_ALX/WorkOrders/output/Jim/Jim_B067C_DashboardQA_Report.md
```

Format: checklist with PASS/FAIL per section, plus any notes. Keep it tight — Jeremy reads this before wiring the backend.

---

*ALX | February 28, 2026 | B-067-C QA*
*Jeffe sees the dashboard. Jim makes sure it's right.*
