---
screen: /admin/audit
title: Audit Log
role: ADM | LP
wave: Cross
origin: O
cp_equivalent: "None — Counterpoint has no audit trail"
---

# Audit Log

**URL:** `/admin/audit`  
**Primary role:** ADM; secondary: LP  
**Entry points:** Admin nav; Case detail → "View system events for this case"

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Audit Log", Export button | Export triggers CSV download |
| Filter bar | Actor (user), Action type, Entity type, Date range picker | Multiple filters combinable |
| Main content | Time-ordered log table | Newest first; infinite scroll or pagination |

## Key Elements

### Audit Log Table
Columns: Timestamp (absolute, hover for relative), Actor (user name + role badge), Action Type (e.g., RULE_ENABLED, CASE_CLOSED, ALLOWLIST_ENTRY_ADDED, USER_ROLE_CHANGED, EVIDENCE_SEALED), Affected Entity (linked — e.g., "Rule: Q-VO-01" links to `/rules/:id`), Record Hash (SHA-256 of the state after the action, truncated to 12 chars + copy icon).

**Action type vocabulary (key entries):** RULE_ENABLED / RULE_DISABLED, ALLOWLIST_ENTRY_CREATED / MODIFIED / DEACTIVATED, CASE_STATUS_CHANGED, EVIDENCE_SEALED, USER_ROLE_ASSIGNED, TRAINING_MODE_ENABLED / DISABLED, CONFIG_SYNC_TRIGGERED, ALERT_ACKNOWLEDGED.

**Empty state:** "No audit events match the current filters." — never shown without filters active; the log always has entries from system initialization.

### Record Hash Column
The SHA-256 hash of the entity state at the moment of the action. Used by ADM to confirm that a record (e.g., a detection rule's configuration) has not changed since a specific audit event. Pairs with the hash displayed on `/transactions/:id/proof` for full chain verification.

### Export
Exports the filtered result set as CSV. Includes all columns plus full hash (not truncated). Used for compliance review (SOC 2, loss-prevention audit, HR proceedings).

## Interaction Flows

1. **Investigate config tamper:** ADM suspects a detection rule was disabled without authorization → filters by Action Type = RULE_DISABLED, Date range = last 7 days → finds the entry → sees Actor + timestamp → clicks Affected Entity link to open the rule → confirms or escalates
2. **Confirm case integrity for HR:** LP investigator filters by Case ID (via entity search) → retrieves all events on the case → exports to CSV for HR proceedings
3. **Export for compliance:** ADM selects date range for the audit period → clicks Export → CSV downloaded → sent to auditor

## UX Callout

Counterpoint has zero audit capability. No form in CP records who changed what configuration or when. LP teams currently have no mechanism to prove that a rule was active at the time an alert fired, or that case evidence was not modified after the fact. Canary's audit log — where every mutation carries actor + timestamp + record hash — is both a compliance instrument and an operational trust mechanism. The hash column transforms the log from a narrative record into a cryptographically verifiable chain.

## Navigation Exits

- `/rules/:id` — linked from RULE_ENABLED/DISABLED events
- `/cases/hawk/:id` — linked from CASE_STATUS_CHANGED events
- `/admin/users/:id` — linked from USER_ROLE_ASSIGNED events
- `/settings/allowlist/*` — linked from ALLOWLIST_ENTRY events

## Open Questions

None.
