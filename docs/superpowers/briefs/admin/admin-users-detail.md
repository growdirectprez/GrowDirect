---
screen: /admin/users/:id
title: User Detail + Role Assignment
role: ADM
wave: Cross
origin: O
cp_equivalent: "User record maintenance + security code assignment (two separate CP screens)"
---

# User Detail + Role Assignment

**URL:** `/admin/users/:id`  
**Primary role:** ADM  
**Entry points:** Users list row click

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | User name, email, status badge, back link to Users List | Breadcrumb navigation |
| Left column | User profile card + store assignment checklist | ~40% width |
| Right column | Login history log + audit events | ~60% width |
| Action bar | Save Changes, Reset Access, Deactivate (danger zone) | Bottom of left column |

## Key Elements

### User Profile Card
Fields: Display name, Email (read-only after invite), Role selector (dropdown: LP Investigator / Store Manager / Buyer / Receiving Clerk / Admin / Viewer), Status toggle (Active / Inactive).

### Store Assignment Checklist
Multi-select checklist of all tenant stores. For single-store tenants: one option, pre-checked. For multi-store: ADM selects which stores this user can see data for. Controls sidebar nav scoping and data filtering tenant-wide. Required field — a user without store assignment cannot access any data.

### Login History
Last 10 login events: timestamp, IP address, device/browser (abbreviated). Entries are read-only. Provides forensic visibility for account compromise investigation. ADM cannot delete login history.

### Reset Access
Forces re-authentication on next visit (invalidates all active sessions). Used when: password suspected compromised, user leaves and account not yet deactivated, suspected session hijack.

## Interaction Flows

1. **Promote role:** ADM opens user → changes role dropdown to "LP Investigator" → saves → user's sidebar nav updates on their next page load (no logout required)
2. **Restrict store access:** ADM unchecks stores from assignment checklist → saves → user immediately loses visibility of unchecked stores' data
3. **Deactivate user:** ADM clicks Deactivate → confirmation modal ("This will immediately end all active sessions") → confirms → user's status → Inactive, all sessions terminated, user cannot log in

## UX Callout

Counterpoint's model requires an administrator to navigate to `frmysecuritycodes` to configure what a user *can do* at the POS, then navigate to the user record to link the security code to the person — two separate forms, two separate navigations, no unified view. Canary collapses this: role = permission set, assigned in one place, effective immediately. Store-scoped access (which stores a user sees) has no CP equivalent at all — CP's security model is per-register, not per-store in a cloud-tenant sense.

## Navigation Exits

- `/admin/users` — back to Users List

## Open Questions

None.
