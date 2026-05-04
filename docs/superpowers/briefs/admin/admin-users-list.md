---
screen: /admin/users
title: Users List
role: ADM
wave: Cross
origin: O
cp_equivalent: "frmsecuritycodes + user record management (two separate forms in CP)"
---

# Users List

**URL:** `/admin/users`  
**Primary role:** ADM  
**Entry points:** Admin nav item (top-bar, not sidebar); Settings → Users link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Users", Invite New User button | Right-aligned CTA |
| Filter bar | Search (name/email), Role filter dropdown, Status filter (active/inactive) | Persistent; filters apply instantly |
| Main content | Paginated table of all user accounts | Primary working surface |
| Pagination | Page controls, items-per-page selector | Below table |

## Key Elements

### User Table
Columns: Name, Email, Role badge (LP Investigator / Store Manager / Buyer / Receiving Clerk / Admin / Viewer), Last Login (relative time, e.g. "3 days ago"), Status (Active / Inactive), Tenant. Sortable by Name, Last Login, Role. Rows link to `/admin/users/:id`.

**Empty state:** "No users found. Use the Invite New User button to provision access." — shown when search returns no results.

**Never-logged-in indicator:** Users with no login on record show "Never" in Last Login with a yellow badge — provisioned but inactive accounts that may need follow-up.

### Role Badge
Color-coded: LP Investigator (red), Store Manager (blue), Buyer (purple), Admin (orange), Viewer (grey). Visible in search results so ADM can identify distribution at a glance without opening individual records.

### Invite New User Button
Opens an inline slide-over form: Email, display name, role selector, store assignment. Sends invitation email. Does not create a full user record until the invite is accepted.

## Interaction Flows

1. **Search by email:** ADM types in search bar → table filters instantly to matching rows → ADM clicks user row → navigates to `/admin/users/:id`
2. **Filter never-logged-in:** ADM selects "Never Logged In" from status filter → table shows only unactivated accounts → ADM bulk-selects → resends invitations
3. **Invite new user:** ADM clicks "Invite New User" → slide-over form opens → fills email + role + stores → submits → invitation email dispatched → row appears in table with "Invited" status

## UX Callout

Counterpoint manages users and security codes in two completely separate forms (`frmysecuritycodes` and user records), requiring the administrator to navigate between them to connect a person to their permissions. Canary unifies the concept: a user is their role, and the role assignment lives on one screen. The "never logged in" filter is an operational health mechanism that CP has no equivalent for — ADMs can't tell in CP whether provisioned users have actually activated their accounts.

## Navigation Exits

- `/admin/users/:id` — open a user's detail and role assignment
- Email invitation link → user activates account externally

## Open Questions

None — scenarios fully specified in source documents.
