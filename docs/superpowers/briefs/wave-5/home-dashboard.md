---
screen: /
title: Home Dashboard
role: ALL
wave: W5
origin: N
cp_equivalent: "None — CP has no dashboard; opens to a main menu of form shortcuts"
---

# Home Dashboard

**URL:** `/`  
**Primary role:** ALL (role-scoped content)  
**Entry points:** Default landing page on login; primary nav home link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Platform nav (sidebar or top nav) | Persistent across all screens |
| Main content | Role-scoped widget grid | |

## Key Elements

### Role-Scoped Widget Grid
The dashboard is assembled from wave-gated, role-scoped widgets. Each role sees a different default layout. Widgets come from the modules their role has access to.

**LP default layout:**
- Active Alerts widget (count by severity + open for > 24h indicator)
- Active Cases widget (open cases, days-open distribution)
- Live Chirp ticker (recent transactions, last 5 minutes)
- Training Mode status (store count in training mode — safety valve visibility)

**MGR default layout:**
- Flash Report summary (today's net sales, discount rate, return rate — linked to `/reports/flash`)
- Inventory at Risk widget (items below reorder point or zero-stock)
- Transfers in Transit (inbound transfers today + overdue count)
- Timecards Pending Approval (count awaiting MGR action)

**BYR default layout:**
- OTB Budget summary (overall Available % across all categories)
- Distribution Recommendations count (pending recommendations)
- Markdown Queue count (high-urgency items)
- Category Performance quick-view (top 3 categories by net sales, last 7 days)

**RCV default layout:**
- Receiving Queue — today's expected deliveries (count + vendor names)
- In-Transit Transfers (inbound to their store today)

**EMP default layout:**
- Clock In / Clock Out widget (current status, start break button if clocked in)
- Own timecard summary (this week's hours)

**ADM default layout:**
- Service Health tiles (from `/admin/devops/health`)
- Tenant LP Rollout Phase summary (count per phase across all tenants)
- Agent status roster (any agents in Error state)
- Config health (any missing LP substrate configurations)

### Wave-Gated Widgets
Widgets appear when the module that drives them is active. An LP user at Phase 1 (config sync only) doesn't see case widgets; an LP user at Phase 4 sees the full LP layout. The dashboard grows as the platform is deployed.

### Customization
Each user can drag-and-drop widgets to reorder, collapse widgets they don't use, and pin specific report views as custom widgets. ADM can configure role-default layouts per tenant.

**Empty state:** "Welcome to Canary Go. Your dashboard will populate as data comes in from your stores."

## Interaction Flows

1. **LP morning start:** LP opens dashboard → 3 new alerts overnight + 1 open case approaching 14 days → clicks alert count → opens alert list filtered to new → starts triage
2. **MGR shift start:** MGR opens dashboard → flash summary shows yesterday's discount rate was 11% (above normal 3-6%) → clicks through to `/reports/flash` → investigates by-hour breakdown
3. **BYR planning day:** BYR opens dashboard → OTB Available at 8% (near-limit) → Markdown Queue shows 6 high-urgency items → opens distribution recommendations first, then markdown queue

## UX Callout

CP opens to a static main menu with icons for each module — the equivalent of a Windows Start menu. There is no data on the CP opening screen. Canary's dashboard is the operational state of the business at the moment of login, scoped to what each role needs to act on first. The LP investigator's first screen shows how many alerts need attention and how many cases are aging — no navigation required to assess program health. The MGR's first screen shows whether yesterday was normal before they've walked the floor. This is the design principle that makes Canary feel like an operating layer rather than a forms tool: the system tells you what requires attention rather than waiting to be asked.

## Navigation Exits

- All module entry points — via primary nav

## Open Questions

None.
