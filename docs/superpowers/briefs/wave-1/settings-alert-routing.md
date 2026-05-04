---
screen: /settings/alert-routing
title: Alert Routing Config
role: ADM | MGR
wave: W1
origin: O+L4
cp_equivalent: "None — Counterpoint has no notification system"
---

# Alert Routing Config

**URL:** `/settings/alert-routing`  
**Primary role:** ADM; secondary: MGR (own notification preferences only)  
**Entry points:** Settings nav → Alert Routing; alert detail → "Why wasn't I notified?"

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Alert Routing", Save button | Changes don't auto-save — Save button required |
| Section: Alert Classes | Alert class tabs: LP Fraud / B2B Account (L4) / System | Three distinct alert routing namespaces |
| Main content | Routing rules table for active class | One rule per row |
| Per-store overrides section | Store-specific routing modifications | Below main table |
| Test panel | "Test Notification" button + result log | Below overrides |

## Key Elements

### Alert Class Tabs (L4 Addition)
Three tabs segmenting alert routing by source:
- **LP Fraud** (default): All Q-module rule family alerts (drawer, void, discount, comp, return, item, etc.). Primary LP investigator feed.
- **B2B Account** (L4 addition — Q-M rule family): Credit utilization alerts, AR aging alerts, tier deviation, payment pattern anomalies. Routes to MGR/BYR, not LP. Without this separation, B2B alerts flood the LP queue.
- **System**: Adapter connectivity, config sync failures, backfill progress alerts. Routes to ADM only.

### Routing Rules Table
Columns: Severity Level (Critical / High / Medium), Delivery Channel (In-App / Email / SMS — multi-select), Recipients (by role or individual user — multi-select), Schedule (Immediate / Business Hours Only / Digest), Store Scope (all stores or specific stores).

Default rules shown out of the box:
- Critical → Email + In-App → LP Investigators + LP Manager → Immediate → All stores
- High → Email + In-App → LP Investigators → Business Hours → All stores
- Medium → In-App → LP Investigators → Digest (daily) → All stores

Rules are additive — multiple rules can apply to the same severity. ADM adds rules to route different severity levels to different people; the system delivers to all matching rules.

### Per-Store Overrides
Optional — override routing for specific stores. E.g., "For Store 3 only, route all alerts to Investigator C (not Investigator A who handles the other stores)."

### Test Notification Button
Sends a test alert through the configured routing and shows the delivery result: "Test notification sent to jmartinez@store.com via Email — delivered in 0.3s" or error details. Confirms that email addresses are valid and routing is working before going live.

**Empty state:** Rules table always shows at least the default rules. Cannot be empty.

## Interaction Flows

1. **Configure B2B alert routing (L4):** ADM opens B2B Account tab → adds routing rule: Medium severity → Email → Store Managers → Business Hours → All stores → saves → B2B credit alerts now route to MGR instead of appearing in LP queue
2. **Add store-specific investigator:** ADM adds store override: Store 3 → all severities → routes to Investigator C instead of default → saves → investigator A continues receiving other stores' alerts
3. **Suppress overnight noise:** ADM edits Medium rule → changes Schedule from Immediate to Business Hours → ADM confirms that 2am Medium alerts for a 24-hour store won't wake up the LP manager

## UX Callout

Alert fatigue is the #1 reason LP systems fail in practice. If every medium-severity alert fires an immediate email at 2am, operators stop reading the emails within a week. The routing configuration — severity by channel by schedule — is what keeps the system signal-to-noise ratio healthy. The B2B alert class separation (L4 addition) is specifically motivated by the fact that B2B credit alerts are not LP concerns; routing them to the LP queue creates noise and obscures fraud signals. No CP equivalent exists for any of this because CP generates no automated alerts at all.

## Navigation Exits

- `/settings/alert-routing` — self-referential (test button result stays on page)
- `/settings/training-mode` — adjacent settings screen

## Open Questions

None.
