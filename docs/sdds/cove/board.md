# Board Module

**Status:** Active
**Type:** App Service
**Last updated:** 2026-04-13
**Blueprint:** `board_bp` at `/board`
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]

---

## Purpose

Board-only administrative interface covering the dashboard, member roster, delinquent member reporting, board request inbox, bulletin notifications, parcel contact management, and member invitation/transfer workflows. All routes restricted to board members via `@board_required` decorator.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | Members, parcels, contacts, board requests | Yes |
| `cove.notifications.services.notify_all_members` | Bulletin broadcast | Yes |
| `cove.treasury.services.get_delinquent_parcels` | Delinquency reporting | Yes |
| `cove.board.services` | Member invitation and transfer logic | Yes |
| `cove.models.parcel_contact.ParcelContact` | Contact CRUD | Yes |

---

## Data Flow & PII Map

### What enters
- Bulletins: title, body (board creates, delivered to all members)
- Parcel contacts: name, email, phone, contact_type, relationship, is_minor, notes (board manages)
- Member invitations: APN, personal_email, name (board invites)
- Board request status updates: status transitions

### What's stored

| Table | Field | Classification | Encryption |
|-------|-------|---------------|------------|
| `parcel_contacts` | `name` | sensitive | **Plaintext (P0)** |
| `parcel_contacts` | `email` | sensitive | **Plaintext (P0)** |
| `parcel_contacts` | `phone` | sensitive | **Plaintext (P0)** |
| `parcel_contacts` | `is_minor` | restricted | **Plaintext (P0)** -- minor status requires extra protection |
| `parcel_contacts` | `notes` | internal | Plaintext |
| `board_requests` | Request content | internal | Plaintext |
| `notifications` | Bulletin content | internal | Plaintext |

### What exits
- Bulletin notifications delivered to all active members (in-app + email)
- Member roster displayed in board dashboard (names, lot emails, status)
- Parcel contact details visible to board members

**PII risk:** High. Parcel contacts store personal information including minor status flags. The member roster view exposes all member names and lot emails to board members.

---

## API Contract

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/board/` | `board_required` | Dashboard with member count |
| GET | `/board/members` | `board_required` | Full member roster |
| GET | `/board/delinquent` | `board_required` | Delinquent member report |
| GET | `/board/requests` | `board_required` | Board request inbox |
| GET | `/board/requests/<id>` | `board_required` | Request detail (auto-marks as read) |
| POST | `/board/requests/<id>/status` | `board_required` | Update request status |
| GET | `/board/diagrams` | `board_required` | Diagrams page |
| GET/POST | `/board/bulletin` | `board_required` | Send bulletin to all members |
| GET | `/board/parcels/<apn>/contacts` | `board_required` | List parcel contacts |
| POST | `/board/parcels/<apn>/contacts/add` | `board_required` | Add contact |
| GET/POST | `/board/parcels/<apn>/contacts/<id>/edit` | `board_required` | Edit contact |
| POST | `/board/parcels/<apn>/contacts/<id>/delete` | `board_required` | Delete contact |
| GET/POST | `/board/members/invite` | `board_required` | Invite or transfer member |

### Access Control

All routes use `@login_required` + `@board_required` (from `cove/auth/decorators.py`). Non-board members receive 403 on every route. No member-facing routes exist in this module.

---

## Operations

### Startup
No module-specific startup.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| DB down | All routes 500 | Automatic reconnect |
| Notification service fails | Bulletin silently fails to send emails (in-app still created) | Retry via bulletin form |

### Monitoring
- Alert on: bulletin send failures, member invitation errors
- Normal: <5 bulletins/month, <10 contact changes/month

---

## Deployment

Standard Cove deployment. No module-specific infrastructure.

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P0** | Parcel contact PII (name, email, phone) stored plaintext | Field-level AES-256-GCM encryption |
| 2 | **P0** | `is_minor` flag stored plaintext -- minor status is COPPA-sensitive and requires extra protection | Encrypt and restrict access logging |
| 3 | **P1** | Parcel contact CRUD operates directly on `db.session` in routes -- no service layer, no audit trail | Extract to `cove/board/services.py` with audit logging |
| 4 | **P1** | Contact delete is hard delete (`db.session.delete`) -- no soft delete, no audit, no undo | Implement soft delete with audit trail |
| 5 | **P1** | Board request auto-read on detail view has no audit trail | Add audit entry for status transitions |
| 6 | **P1** | Member roster exposes all member data to any board member -- no column-level access control | Consider hiding personal_email column, show only lot_email |
| 7 | **P2** | No confirmation step for bulletin send -- board member can accidentally broadcast to all members | Add preview/confirm step before commit |
| 8 | **P2** | Parcel contact form allows empty email AND empty phone -- at least one should be required | Add cross-field validation |

---

## Production Readiness Checklist

- [ ] Parcel contact PII encrypted at rest
- [ ] Minor status (`is_minor`) encrypted and access-logged
- [ ] Secrets in AWS Secrets Manager
- [x] Health check endpoint responds (via app-level `/health`)
- [ ] Audit logging for all contact CRUD operations
- [ ] Soft delete for contacts (no hard deletes in production)
- [x] Rate limiting (via app-level limiter)
- [x] Error responses don't leak internals
- [x] Board-only access enforced on all routes
- [ ] Bulletin send confirmation step
