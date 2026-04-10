# SDD: Meetings

**Status:** Active
**Last updated:** 2026-03-29

## Overview

Meeting scheduling, editing, calendar export, and ARC (Architectural Review Committee) application submission. Board creates and edits meetings; members submit ARC applications tied to their parcel; board reviews via `ARCReview` records. All operations write to `audit_log`.

Blueprint: `meetings_bp` at `/meetings`. Services in `cove/meetings/services.py`.

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/meetings/` | login | List upcoming and past meetings (split by date) |
| GET/POST | `/meetings/create` | login + board | Schedule a new meeting; validates type against `MEETING_TYPES` |
| GET/POST | `/meetings/<meeting_id>/edit` | login + board | Edit an existing meeting (rejects if cancelled) |
| GET | `/meetings/<meeting_id>` | login | Meeting detail: title, type, date, time, location, status, Google Calendar link |
| GET | `/meetings/<meeting_id>/calendar.ics` | login | Download iCalendar (.ics) file for a meeting |
| GET | `/meetings/<meeting_id>/attachment` | login | Download the meeting notice/agenda attachment via `send_file` |
| POST | `/meetings/<meeting_id>/cancel` | login + board | Cancel a scheduled meeting (sets `status="cancelled"`) |
| GET/POST | `/meetings/arc/apply` | login | Submit ARC application; pre-fills `apn` from current member |
| GET | `/meetings/arc/<application_id>` | login | View ARC application status and fee; non-board members can only see their own |

Board check is `current_user.is_board or current_user.is_admin`; non-board gets 403 via `abort(403)`.

## Forms

**`cove/meetings/forms.py`**

### `MeetingForm` (extends `CoveFileForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `title` | `StringField` | DataRequired, Length(max=500) | |
| `meeting_type` | `SelectField` | DataRequired | Choices: annual_member, special_member, regular_board, special_board, arc_review, committee |
| `meeting_date` | `DateField` | DataRequired | Format `%Y-%m-%d` |
| `time` | `StringField` | DataRequired, Length(max=10) | Pattern `HH:MM` |
| `location` | `StringField` | DataRequired, Length(max=500) | |
| `description` | `TextAreaField` | Optional, Length(max=5000) | |
| `video_call_url` | `URLField` | Optional, URL, Length(max=1000) | e.g. Zoom link |
| `attachment` | (file field via CoveFileForm) | | Meeting notice/agenda attachment |

### `AgendaItemForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `agenda` | `TextAreaField` | Optional, Length(max=10000) | Full agenda text |

### `MinutesForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `minutes` | `TextAreaField` | DataRequired, Length(max=50000) | Meeting minutes text |

### `ARCApplicationForm` (extends `CoveFileForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `arc_type` | `SelectField` | DataRequired | Choices: new_build ($75), addition ($75), landscaping ($15), facade ($15) |
| `description` | `TextAreaField` | DataRequired, Length(20-5000) | Description of proposed work |
| `parcel_id` | `StringField` | DataRequired | Pre-filled from member's parcel |

## Models

### `Meeting` (`meetings`)

Columns: `id`, `organization_id`, `type` (see constants), `title`, `description`, `date` (Date), `time` (string e.g. `"19:00"`), `location`, `agenda`, `minutes`, `notice_required_days` (default 4), `notice_sent_at`, `status` (`scheduled|noticed|held|cancelled`), `created_by`, `video_call_url`, `attachment_path`, `attachment_filename`, `embedding` (`Vector(1024)`).

No relationships defined on the model — queried by `organization_id`.

### `ARCApplication` (`arc_applications`)

Columns: `id`, `organization_id`, `applicant_id` -> `members.id`, `parcel_id` -> `parcels.id`, `type` (`new_build|addition|landscaping|facade`), `description`, `plans_document_id` -> `documents.id` (nullable), `fee_amount` (float), `fee_paid` (bool), `status` (`submitted|complete|under_review|approved|denied|appealed`), `submitted_at`, `reviewed_at`, `appeal_deadline` (Date, 30 days after review).

### `ARCReview` (`arc_reviews`)

Columns: `id`, `application_id` -> `arc_applications.id`, `meeting_id` -> `meetings.id` (nullable), `decision` (`approved|denied|conditional`), `conditions`, `reviewed_at`.

No routes currently create or display `ARCReview` records — model is present but review creation is not yet wired.

## Services (`cove/meetings/services.py`)

| Function | What it does |
|----------|--------------|
| `create_meeting(org_id, created_by, title, meeting_type, meeting_date, time, location, description, video_call_url, attachment_file)` | Validates type, inserts `Meeting`, writes audit log, commits |
| `update_meeting(meeting, actor_id, title, meeting_type, meeting_date, time, location, description, video_call_url, attachment_file)` | Updates meeting fields, handles attachment replacement, writes audit log |
| `list_meetings(org_id, upcoming_only, meeting_type)` | SELECT with optional date filter (`>= today`, status != cancelled) and type filter; ordered by date desc |
| `get_meeting(meeting_id)` | `db.session.get(Meeting, meeting_id)` |
| `cancel_meeting(meeting_id, actor_id)` | Sets `status="cancelled"`, writes audit log, commits; raises `ValueError` if already cancelled |
| `generate_ics(meeting)` | Generates iCalendar (.ics) content string for a meeting |
| `google_calendar_url(meeting)` | Generates a Google Calendar event creation URL for a meeting |
| `submit_arc_application(org_id, applicant_id, parcel_id, arc_type, description, plans_document_id)` | Validates type, looks up fee from `ARC_FEES`, inserts `ARCApplication`, writes audit log, commits |
| `get_arc_application(application_id)` | `db.session.get(ARCApplication, application_id)` |
| `list_arc_applications(org_id, status)` | SELECT with optional status filter; ordered by `submitted_at` desc |

### Constants

```python
MEETING_TYPES = ["annual_member", "special_member", "regular_board",
                 "special_board", "arc_review", "committee"]

ARC_TYPES     = ["new_build", "addition", "landscaping", "facade"]

ARC_FEES      = {"new_build": 75.00, "addition": 75.00,
                 "landscaping": 15.00, "facade": 15.00}
```

## Templates

| Template | Description |
|----------|-------------|
| `meetings/index.html` | Two sections: upcoming (sorted ascending) and past; links to detail |
| `meetings/create.html` | `MeetingForm` — title, type select, date, time, location, description, video call URL, attachment |
| `meetings/edit.html` | `MeetingForm` pre-filled with existing meeting data; same fields as create |
| `meetings/detail.html` | Shows all meeting fields; Google Calendar link; board sees cancel and edit buttons |
| `meetings/arc_apply.html` | `ARCApplicationForm` — type select, description, parcel_id; shows fee schedule |
| `meetings/arc_status.html` | Shows application status, type, fee amount, submitted_at; board sees all apps |

All extend `base.html`. Forms use `{{ form.hidden_tag() }}` for CSRF.
