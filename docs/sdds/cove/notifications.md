# SDD: Notifications Module

**Status:** Active
**Last updated:** 2026-03-29
**Module:** `cove/notifications/`

---

## Overview

In-app notification system with optional email delivery. Supports per-member and broadcast notifications with read/unread tracking. Notifications are surfaced in the member dashboard (latest 5), a dedicated notifications page (latest 50), and as an unread count badge via context processor injected into every template.

---

## Model

**Notification** (`notifications` table) -- `cove/models/notification.py`

| Column | Type | Description |
|--------|------|-------------|
| `id` | `String(36)`, PK | UUID, auto-generated |
| `organization_id` | `String(36)`, FK → `organizations.id` | Owning organization |
| `member_id` | `String(36)`, FK → `members.id` | Recipient member |
| `type` | `String(30)` | Notification type: `meeting_invite`, `vote_notice`, `bulletin`, `arc_update`, `election_notice` |
| `title` | `String(500)` | Notification title (required) |
| `body` | `Text`, nullable | Extended message body |
| `link` | `String(500)`, nullable | Relative URL for the notification target |
| `email_sent` | `Boolean`, default `False` | Whether email delivery was attempted |
| `read_at` | `DateTime`, nullable | Timestamp when member read the notification (`None` = unread) |
| `created_by` | `String(36)`, FK → `members.id`, nullable | Member who triggered the notification |
| `created_at` | `DateTime` | Creation timestamp |

---

## Services

**`cove/notifications/services.py`**

| Function | Signature | Description |
|----------|-----------|-------------|
| `notify_member` | `(org_id, member_id, notification_type, title, body=None, link=None, created_by=None, send_email=True)` | Create a notification for one member. Optionally sends email to `personal_email` via lot email forwarding. Returns the `Notification` instance. Calls `db.session.flush()` (not commit). |
| `notify_all_members` | `(org_id, notification_type, title, body=None, link=None, created_by=None, send_email=True)` | Send notification to all active members in the org. Respects `delivery_preference` (electronic/both) for email. Calls `db.session.commit()`. |
| `get_notifications` | `(member_id, unread_only=False, limit=50)` | Fetch notifications for a member, newest first. Optional filter for unread only. |
| `unread_count` | `(member_id)` | Count of unread notifications for a member. Returns `int`. |
| `mark_read` | `(notification_id, member_id)` | Mark a single notification as read. Validates ownership. Returns `bool`. Commits. |
| `mark_all_read` | `(member_id)` | Mark all unread notifications as read. Returns count updated. Commits. |

### Email Delivery

`_send_notification_email(member, notification)` (private):
- Sends to `member.lot_email` (which forwards to `personal_email` via Cloudflare Email Routing)
- Subject: `[Cove] {title}`
- Body: notification body + link (absolute URL with `abalonecove.org` domain)
- Sender: `MAIL_DEFAULT_SENDER` config or `cove@abalonecove.org`
- Failures are logged as warnings, not raised -- email delivery is best-effort

---

## Context Processor

Defined in `cove/__init__.py` (app factory):

```python
@app.context_processor
def inject_notification_count():
    # Returns {"notification_count": N} for authenticated users
    # Returns {"notification_count": 0} for anonymous/errors
```

This makes `notification_count` available in every Jinja2 template for rendering the unread badge in the navigation bar.

---

## Routes (in Member Blueprint)

Notification routes live in `cove/member/routes.py`, not in the notifications module itself.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/member/notifications` | Required | List all notifications (limit 50) |
| POST | `/member/notifications/<notification_id>/read` | Required | Mark one notification as read, redirect back |
| POST | `/member/notifications/read-all` | Required | Mark all notifications as read, redirect to notifications |

The member dashboard (`GET /member/dashboard`) also queries the latest 5 notifications via `get_notifications(current_user.id, unread_only=False, limit=5)`.

---

## Integration Points

Modules that create notifications:

| Module | Function Used | Notification Type | Trigger |
|--------|--------------|-------------------|---------|
| Board (`cove/board/routes.py`) | `notify_all_members` | `bulletin` | Board member sends a bulletin to all active members |

Additional notification types are defined in the model (`meeting_invite`, `vote_notice`, `arc_update`, `election_notice`) but are not yet wired to creation triggers in the current codebase.

---

## Design Notes

- **Flush vs. Commit**: `notify_member` calls `flush()` so it can be composed inside larger transactions. `notify_all_members` calls `commit()` since it is typically a terminal operation.
- **Delivery preference**: Broadcast notifications respect `member.delivery_preference` -- email is only sent if the member has opted for `electronic` or `both`.
- **No deletion**: Notifications are never deleted. `read_at` is the only state transition.
- **Ownership validation**: `mark_read` verifies `notification.member_id == member_id` before updating, preventing cross-member access.
