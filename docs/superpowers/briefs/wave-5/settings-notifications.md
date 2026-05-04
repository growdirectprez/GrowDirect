---
screen: /settings/notifications
title: Notification Preferences
role: ALL
wave: W5
origin: N
cp_equivalent: "None — CP has no notification system"
---

# Notification Preferences

**URL:** `/settings/notifications`  
**Primary role:** ALL (per-user; ADM can set tenant defaults)  
**Entry points:** Settings → Account section; user profile → notification settings

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Notification Preferences" | |
| Tab bar | In-App / Email / Mobile Push | |
| Tab content | Notification event table with per-channel toggles | |

## Key Elements

### Notification Event Table
Rows: each notification event type. Columns: Event, In-App, Email, Mobile Push, Frequency.

**Event types (role-filtered — users see only their applicable events):**
- LP Alert created (LP role)
- LP Alert — High severity (LP role)
- Case status changed (LP role)
- Alert assigned to me (LP role)
- Transfer arrived — my store (MGR / RCV role)
- Transfer variance detected — my store (MGR / LP role)
- Timecard exception — my store (MGR role)
- Physical count assigned to me (CNT role)
- PO received — my store (MGR / RCV role)
- OTB over-budget PO submitted (BYR role)
- Markdown queue high-urgency item (BYR role)
- Distribution recommendation created (BYR role)
- Agent error detected (ADM role)
- Service health degraded (ADM role)

### Frequency Options (for digest-style events)
For events like "Distribution recommendation created" or "Markdown queue high-urgency item" — options are: Immediately / Daily digest (8am) / Weekly digest (Monday 8am) / Off.

**High-priority events** (LP Alert — High severity, Service health degraded) are Immediately-only and cannot be set to digest or Off.

### Mobile Push
Requires the Canary mobile app or browser push permission. If push is not configured on the device, this column shows "Not configured" with a setup link.

**ADM tenant defaults:** ADM can set default notification preferences for each role across the tenant. Individual users can override the defaults for their own account (except admin-enforced events that cannot be turned off).

**Empty state:** Not applicable — notification events are always present.

## Interaction Flows

1. **LP alert fatigue:** LP investigator is getting too many email notifications → opens notification preferences → sets LP Alert (normal severity) to In-App only → keeps LP Alert (High severity) on all channels → email volume drops
2. **MGR morning digest:** MGR prefers a single daily summary → sets Timecard exception, Transfer variance, PO received all to Daily digest → opens dashboard in the morning, one email in their inbox covering everything
3. **ADM enforcement:** ADM sets "Agent error detected" as In-App + Email, non-overridable → all ADMs receive this notification regardless of personal preferences → ensures no critical service errors go unnoticed

## UX Callout

Notification preferences are a W5 feature because the earlier waves establish the signal types before configuring how they're delivered. An LP investigator working through Wave 1 may want every alert immediately; after Wave 4, with the full system running and many alert types active, they may want to triage in-app and receive only high-severity alerts on email. The notification preferences screen is the control point for alert fatigue management — a problem that becomes real only when the system is generating meaningful signal volume. Building it in W5 respects the sequencing: configure delivery after the signals are established, not before.

## Navigation Exits

- `/settings` — back to settings menu

## Open Questions

None.
