# Meetings Module

**Status:** Active
**Type:** App Service
**Last updated:** 2026-04-13
**Blueprint:** `meetings_bp` at `/meetings`
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]

---

## Purpose

Meeting scheduling, editing, calendar export (iCal + Google Calendar), and ARC (Architectural Review Committee) application lifecycle including submission, board review, and fee tracking. Board creates/edits meetings; members submit ARC applications tied to their parcel; board reviews and records decisions.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | Meetings, ARC applications, ARC reviews | Yes |
| Filesystem (`UPLOAD_FOLDER/meetings/`) | Meeting attachment storage | Yes |
| `cove.services.file_security.validate_file_path` | Path traversal prevention on attachment downloads | Yes |
| `cove.models.audit.AuditLog` | Audit trail for meeting and ARC operations | Yes |
| `cove.notifications.services.notify_member` | ARC decision notifications to applicant | No (fails silently) |

---

## Data Flow & PII Map

### What enters
- Meeting creation: title, type, date, time, location, description, video_call_url, attachment (board only)
- ARC applications: arc_type, description, parcel reference (member)
- ARC reviews: decision, conditions, meeting reference (board)

### What's stored

| Table | Field | Classification | Encryption |
|-------|-------|---------------|------------|
| `meetings` | `title`, `description`, `location` | internal | Plaintext |
| `meetings` | `video_call_url` | internal | Plaintext |
| `meetings` | `attachment_path` | internal | Plaintext |
| `meetings` | `embedding` | internal | Vector(1024) |
| `arc_applications` | `applicant_id` (FK), `apn` | internal | Plaintext |
| `arc_applications` | `description` (property work details) | internal | Plaintext |
| `arc_reviews` | `conditions` | internal | Plaintext |

### What exits
- iCalendar (.ics) files (meeting title, time, location, description)
- Google Calendar URLs (same data, URL-encoded)
- Meeting attachment downloads
- ARC decision notifications (via notification service)

**PII note:** Meeting data is organizational, not personal. ARC applications link to a member but the content describes property work, not personal data. Low PII risk.

---

## API Contract

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/meetings/` | `login_required` | List upcoming and past meetings |
| GET/POST | `/meetings/create` | `login_required` + board | Schedule new meeting |
| GET/POST | `/meetings/<id>/edit` | `login_required` + board | Edit existing meeting |
| GET | `/meetings/<id>` | `login_required` | Meeting detail |
| GET | `/meetings/<id>/calendar.ics` | `login_required` | Download iCalendar file |
| GET | `/meetings/<id>/attachment` | `login_required` | Download meeting attachment |
| POST | `/meetings/<id>/cancel` | `login_required` + board | Cancel a meeting |
| GET/POST | `/meetings/arc/apply` | `login_required` | Submit ARC application |
| GET | `/meetings/arc/<app_id>` | `login_required` | View ARC application status |
| GET | `/meetings/arc/pending` | `login_required` + board | Pending ARC applications |
| GET/POST | `/meetings/arc/<app_id>/review` | `login_required` + board | Record ARC review decision |
| POST | `/meetings/arc/<app_id>/fee` | `login_required` + board | Mark ARC fee as paid |

### Access Control

Board check: `current_user.is_board or current_user.is_admin`. Non-board gets 403 on create/edit/cancel/review routes. ARC status: members see only their own; board sees all.

---

## Services (`cove/meetings/services.py`)

### Meeting Operations

| Function | Description |
|----------|-------------|
| `create_meeting(...)` | Validates type, auto-sets notice period from Davis-Stirling, saves attachment, audits |
| `update_meeting(...)` | Updates fields, replaces attachment if new one uploaded, audits |
| `list_meetings(org_id, upcoming_only, meeting_type)` | Filtered query, ordered by date desc |
| `cancel_meeting(meeting_id, actor_id)` | Sets status=cancelled, audits |
| `generate_ics(meeting)` | RFC 5545 iCalendar string |
| `google_calendar_url(meeting)` | Google Calendar event creation URL |
| `search_meetings_semantic(org_id, query, limit)` | Cosine distance search via pgvector |

### ARC Operations

| Function | Description |
|----------|-------------|
| `submit_arc_application(...)` | Validates type, looks up fee, creates application, audits |
| `record_arc_review(...)` | Validates decision, creates ARCReview, updates application status, notifies applicant |
| `mark_fee_paid(application_id)` | Sets `fee_paid=True` |
| `list_arc_applications(org_id, status)` | Filtered query |

### Constants

- `MEETING_TYPES`: annual_member, special_member, regular_board, special_board, arc_review, committee
- `ARC_FEES`: new_build=$75, addition=$75, landscaping=$15, facade=$15
- `NOTICE_DAYS_BY_TYPE`: Davis-Stirling notice requirements per meeting type (2-10 days)

---

## Operations

### Startup
No module-specific startup. Upload directory `meetings/` created on first attachment save.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| DB down | All routes 500 | Automatic reconnect |
| Filesystem full | Attachment upload fails | Manual cleanup |
| Notification service fails | ARC decision notification silently drops | Retry manually or check audit log |

### Monitoring
- Alert on: meeting creation failures, ARC review notification failures
- Normal: <20 meetings/year, <10 ARC applications/year

---

## Deployment

Standard Cove deployment. Meeting attachments stored in `UPLOAD_FOLDER/meetings/` subdirectory, mounted as Docker volume.

- **AWS**: Attachment files on EFS alongside vault uploads
- **Backup**: Meeting attachments are governance records -- must be included in backups

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P1** | Meeting attachment validation uses `ALLOWED_EXTENSIONS` constant but no MIME type verification | Verify MIME type matches extension on upload |
| 2 | **P1** | No audit trail for ARC fee payment marking | Add audit entry for `arc.fee_paid` |
| 3 | **P1** | ARC application `appeal_deadline` (30 days post-review) exists in model but is never set in code | Set `appeal_deadline` in `record_arc_review` |
| 4 | **P1** | No notification sent when meetings are created or cancelled -- only ARC decisions trigger notifications | Add `meeting_invite` and `meeting_cancelled` notification types |
| 5 | **P2** | ICS generation uses naive datetimes (no timezone) -- may cause calendar offset issues | Use timezone-aware datetimes with `America/Los_Angeles` |
| 6 | **P2** | No pagination on meeting list | Add pagination for past meetings |
| 7 | **P2** | `ARCReview` has no `reviewed_by` field -- reviewer identity tracked only in audit log | Add `reviewed_by` FK to `arc_reviews` table |

---

## Production Readiness Checklist

- [x] No sensitive PII in this module (meeting data is organizational)
- [ ] Secrets in AWS Secrets Manager
- [x] Health check endpoint responds (via app-level `/health`)
- [x] Audit logging for meeting CRUD and ARC submission (partial -- fee payment not audited)
- [ ] Data retention policy for meeting records
- [x] Rate limiting (via app-level limiter)
- [x] Error responses don't leak internals
- [ ] ICS timezone handling corrected
- [ ] ARC appeal deadline computed and stored
- [ ] Meeting lifecycle notifications wired
