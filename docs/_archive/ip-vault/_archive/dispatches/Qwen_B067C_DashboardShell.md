---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Qwen Session Prompt — B-067-C: Square Capability Dashboard Shell
**Work Order:** B-067-C
**Date:** February 28, 2026
**Dispatched by:** ALX (via Jeremy)
**Priority:** HIGH — runs in parallel with Condor and Jeremy

---

## Mission

Build the single-page HTML dashboard that shows Jeffe everything Square exposes. This is a strategic instrument — not a dev tool. When Jeffe clicks a card, he sees real data from his sandbox merchant account.

Jeremy is building the backend endpoint. You build the shell. When both are done, Jeremy wires them together.

---

## Design Language

Match this file exactly:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Art/eljeffe-dev/index.html
```

Core values:
- Background: `#0a0d12`
- Primary accent: `#f59e0b` (Bitcoin amber)
- Success: `#22c55e` (green)
- Warning: `#f59e0b` (amber)
- Muted: `#6b7280` (gray)
- Font — headers: Syne (Google Fonts)
- Font — code/data: JetBrains Mono (Google Fonts)
- Glow effects on active/hover states
- Dark glass morphism cards

---

## Output

```
/Users/geofflyle/GrowDirect/Canary/static/square_explorer.html
```

Single self-contained HTML file. All CSS and JS inline — no external files except Google Fonts and cdnjs.

---

## Page Structure

### Header (fixed top bar)
```
[ elJeffe wordmark ]    Square Capability Explorer    [ SANDBOX ] badge    [ MLE55GCYANCYT ]
```
- SANDBOX badge: amber background, monospace text
- Merchant ID: small, muted, monospace

### Hero Strip (3 stat tiles, full width below header)
```
[ 14 API Families ]    [ Phase 1: 2 LIVE ]    [ Phase 3: 85% LP Coverage ]
```
Hard-coded. Amber numbers, muted labels.

### Capability Grid (main content)

CSS grid: 3 columns on desktop, 1 on mobile. 16 cards total (14 API families + Merchant + Locations).

Each card structure:
```html
<div class="api-card" data-family="payments">
  <div class="card-header">
    <span class="phase-badge live">● LIVE</span>
    <h3>Payments API</h3>
    <code class="sdk-namespace">client.payments</code>
  </div>
  <div class="card-meta">
    <div class="lp-signal">Detects: sale, void, post-void, split tender</div>
    <div class="tsp-component">TSP: Sub 1 → seal → Sub 3 → inscribe</div>
  </div>
  <button class="fetch-btn" onclick="fetchFamily('payments')">
    Fetch Live Data ▸
  </button>
  <div class="response-panel" id="response-payments" hidden>
    <div class="response-header">
      <span class="record-count"></span>
      <code class="sdk-call-used"></code>
    </div>
    <pre class="json-output"></pre>
  </div>
</div>
```

Phase badge variants:
- `● LIVE` — green (`#22c55e`) — Payments, Refunds, Webhooks/Subscriptions
- `◎ PHASE 2` — amber (`#f59e0b`) — Orders, Cash Drawer, Timecards, Inventory, Disputes, Gift Cards
- `○ PHASE 3` — gray (`#6b7280`) — Customers, Loyalty, Team Members, Catalog, Devices, Merchant, Locations

### The 16 Cards (in this order, 3-column grid)

**Row 1 — Phase 1 LIVE**
1. Payments API — `client.payments` — Detects: sale, void, post-void — TSP: Sub 1 LIVE
2. Refunds API — `client.refunds` — Detects: refund, phantom refund — TSP: Sub 1 LIVE
3. Webhooks API — `client.webhooks.subscriptions` — Pipeline entry point — TSP: TSP-01 LIVE

**Row 2 — Phase 2 Priority**
4. Orders API — `client.orders` — Detects: discount abuse, sweet-hearting, void patterns
5. Cash Drawer API — `client.cash_drawers` — Detects: no-sale, cash variance, paid-in/out fraud
6. Labor / Timecards — `client.labor` — Detects: off-clock transactions, break fraud, ghost employees

**Row 3 — Phase 2**
7. Inventory API — `client.inventory` — Detects: shrinkage, manual adjustment fraud
8. Disputes API — `client.disputes` — Detects: chargeback signals, external fraud indicators
9. Gift Cards API — `client.gift_cards` — Detects: gift card velocity, balance transfer laundering

**Row 4 — Phase 3**
10. Customers API — `client.customers` — Detects: return fraud by account, profile deletion cover-up
11. Loyalty API — `client.loyalty` — Detects: point manipulation, promo abuse
12. Team Members API — `client.team_members` — Detects: inactive employee transactions

**Row 5 — Phase 3 + Utilities**
13. Catalog API — `client.catalog` — Detects: unauthorized price changes
14. Devices API — `client.devices` — Detects: unauthorized terminals
15. Merchant API — `client.merchants` — Anchor record: merchant profile
16. Locations API — `client.locations` — Required context for cash drawer + inventory

### TSP Pipeline Strip (below the grid)

Horizontal flow diagram showing the full pipeline. Use flexbox or CSS grid.

```
[ Square API ] → [ Sub 2: Parse + Route ] → [ Sub 1: Hash + Seal ] → [ Sub 3: Ordinal Inscribe ] → [ gLog Receipt ]
```

Below the flow, a coverage table:

| API Family     | Sub 2 | Sub 1 | Sub 3 | Status      |
|----------------|-------|-------|-------|-------------|
| Payments       | ✓     | ✓     | ✓     | ● LIVE      |
| Refunds        | ✓     | ✓     | ✓     | ● LIVE      |
| Orders         | —     | —     | —     | ◎ PHASE 2   |
| Cash Drawer    | —     | —     | —     | ◎ PHASE 2   |
| ... (all 14)   |       |       |       |             |

Color code each row by phase. Amber glow on PHASE 2 rows — these are next.

### Footer
```
Sandbox only · No real transactions · Patent Pending · elJeffe by GrowDirect
```

---

## JavaScript

```javascript
async function fetchFamily(family) {
  const btn = document.querySelector(`[data-family="${family}"] .fetch-btn`);
  const panel = document.getElementById(`response-${family}`);
  const countEl = panel.querySelector('.record-count');
  const sdkCallEl = panel.querySelector('.sdk-call-used');
  const jsonEl = panel.querySelector('.json-output');

  // Loading state
  btn.disabled = true;
  btn.textContent = 'Fetching...';
  panel.hidden = false;
  panel.className = 'response-panel loading';
  jsonEl.textContent = '';

  try {
    const res = await fetch(`/explore/${family}`);
    const data = await res.json();

    if (data.status === 'ok') {
      panel.className = 'response-panel success';
      countEl.textContent = `${data.count} records`;
      sdkCallEl.textContent = data.sdk_call;
      jsonEl.textContent = JSON.stringify(data.data, null, 2);
    } else if (data.status === 'scope_not_granted') {
      panel.className = 'response-panel scope-gap';
      countEl.textContent = 'Scope not granted';
      sdkCallEl.textContent = data.sdk_call;
      jsonEl.textContent = data.error + '\n\nRequired for Phase 2. Routes to Syd for OAuth expansion.';
    } else {
      panel.className = 'response-panel error';
      countEl.textContent = 'Error';
      sdkCallEl.textContent = data.sdk_call || '';
      jsonEl.textContent = data.error;
    }
  } catch (err) {
    panel.className = 'response-panel error';
    countEl.textContent = 'Network error';
    jsonEl.textContent = err.toString();
  } finally {
    btn.disabled = false;
    btn.textContent = 'Fetch Live Data ▸';
  }
}

// On page load: fetch merchant and locations automatically (anchors for context)
document.addEventListener('DOMContentLoaded', () => {
  fetchFamily('merchant');
  fetchFamily('locations');
});
```

---

## CSS Notes

Response panel states:
- `.loading` — amber border, pulsing opacity
- `.success` — green border `#22c55e`, green glow
- `.scope-gap` — amber border, amber text on the message
- `.error` — red border `#ef4444`

Card hover: amber glow on border. Active card (after fetch): slight background lift.

JSON output: `white-space: pre-wrap`, `word-break: break-all`, `font-size: 11px`, `color: #a3e635` (lime-ish — data feels alive).

SDK call display: small monospace, muted color, appears above the JSON.

---

## Placeholder Text

Until Condor's capability map arrives, use these placeholders in each card:
- LP Signal: `TODO: Condor B-067-A`
- TSP Component: `TODO: Condor B-067-A`

Leave clear HTML comments: `<!-- CONDOR MAP: paste LP signal here -->`

Jeremy will paste the real values when Condor delivers.

---

## Standing Directives

- Single self-contained HTML file. No separate CSS or JS files.
- Match eljeffe.dev design language exactly. No generic UI kit aesthetics.
- The page works with or without the Flask backend (shows the shell, fetch buttons fail gracefully).

---

*ALX | February 28, 2026 | B-067-C*
*Jeffe sees this. Make it sharp.*
