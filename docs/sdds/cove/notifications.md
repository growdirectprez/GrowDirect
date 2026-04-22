# Notifications Module

**Status:** Active
**Type:** App Service
**Last updated:** 2026-04-13
**Module:** `cove/notifications/`
**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]
**Architecture:** [[docs/sdds/cove/architecture|Cove Architecture]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

---

## Purpose

In-app notification system with optional email delivery. Supports per-member and broadcast notifications with read/unread tracking, public bulletin visibility, and pinning. Notifications are surfaced in the member dashboard, a dedicated notifications page, and as an unread count badge injected into every template via context processor.

---

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| PostgreSQL (`cove` database) | Notification records | Yes |
| Flask-Mail (`cove.extensions.mail`) | Email delivery | No (fails silently) |
| Cloudflare Email Routing (prod) / MailHog (dev) | SMTP transport | No |
| `cove.models.member.Member` | Recipient lookup, delivery preference check | Yes |

---

## Data Flow & PII Map

### What enters
- Notification creation: org_id, member_id, type, title, body, link, created_by
- Broadcast: same, repeated per active member with delivery preference check

### What's stored

| Table | Field | Classification | Encryption |
|-------|-------|---------------|------------|
| `notifications` | `member_id` (FK) | internal | Plaintext (UUID ref) |
| `notifications` | `title` | internal | Plaintext |
| `notifications` | `body` | internal | Plaintext (may contain governance details) |
| `notifications` | `link` | internal | Plaintext (relative URL) |
| `notifications` | `created_by` (FK) | internal | Plaintext (UUID ref) |

### What exits
- In-app notification display (authenticated member only)
- **Email delivery**: subject line `[Cove] {title}`, body text + absolute URL link
  - Sent to `member.lot_email` (forwards to `personal_email` via Cloudflare)
  - Sender: `cove@abalonecove.org`
  - **PII in transit**: lot_email address visible in SMTP headers

### PII Classification

| Data | Classification | Notes |
|------|---------------|-------|
| `lot_email` in email headers | sensitive | Lot email is semi-public within org but reveals member association |
| `personal_email` (forwarding target) | sensitive | Never in notification records; only in Cloudflare routing config |
| Notification body content | internal | May reference governance actions, no direct PII |

---

## API Contract

Notification routes live in `cove/member/routes.py`, not in the notifications module itself.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/member/notifications` | `login_required` | List all notifications (limit 50) |
| POST | `/member/notifications/<id>/read` | `login_required` | Mark one notification as read |
| POST | `/member/notifications/read-all` | `login_required` | Mark all as read |

The member dashboard (`GET /member/dashboard`) displays the latest 5 notifications.

### Context Processor

`inject_notification_count()` in `cove/__init__.py` -- makes `notification_count` available in every Jinja2 template. Returns 0 on any error.

---

## Services (`cove/notifications/services.py`)

| Function | Description |
|----------|-------------|
| `notify_member(...)` | Create notification for one member; optionally send email to `personal_email` via lot email; calls `flush()` (composable in transactions) |
| `notify_all_members(...)` | Broadcast to all active members; respects `delivery_preference`; calls `commit()` |
| `get_notifications(member_id, unread_only, limit)` | Fetch notifications newest first |
| `unread_count(member_id)` | Count unread notifications |
| `mark_read(notification_id, member_id)` | Mark single notification read; validates ownership |
| `mark_all_read(member_id)` | Mark all unread as read |
| `get_public_bulletins(org_id, limit)` | Deduplicated public bulletins for landing page |
| `get_pinned_bulletins(org_id)` | Pinned public notifications |

### Email Delivery

`_send_notification_email(member, notification)`:
- Sends to `member.lot_email` (which forwards via Cloudflare Email Routing)
- Best-effort: failures logged as warnings, not raised
- Uses Flask-Mail `Message` with `MAIL_DEFAULT_SENDER` config

### Integration Points

| Module | Function | Type | Trigger |
|--------|----------|------|---------|
| Board | `notify_all_members` | `bulletin` | Board sends bulletin |
| Meetings | `notify_member` | `arc_decision` | ARC review decision recorded |

Additional types defined but not yet wired: `meeting_invite`, `vote_notice`, `arc_update`, `election_notice`.

---

## Operations

### Startup
No module-specific startup.

### Failure Modes

| Failure | Impact | Recovery |
|---------|--------|----------|
| DB down | Notification creation fails, badge returns 0 | Automatic reconnect |
| SMTP down | Email delivery fails silently; in-app notifications still created | Emails lost permanently (no retry queue) |
| Context processor exception | Badge returns 0; app continues normally | Self-healing |

### Monitoring
- Alert on: SMTP delivery failure rate, notification table growth rate
- Normal: <100 notifications/month for 81-member HOA

---

## Deployment

Standard Cove deployment. Email routing:
- **Dev**: MailHog at `cove_localhost_mailhog` (SMTP 1026, Web 8026)
- **Prod**: Cloudflare Email Routing (lot_email -> personal_email forwarding)
- **SMTP config**: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_DEFAULT_SENDER`

---

## Code Review Findings

| # | Severity | Finding | Recommended Fix |
|---|----------|---------|----------------|
| 1 | **P1** | No email retry mechanism -- failed emails are permanently lost | Add retry queue (Valkey-backed) or at minimum a `delivery_failed` flag |
| 2 | **P1** | SMTP transport in production must use TLS -- not enforced in config | Set `MAIL_USE_TLS=True` in ProdConfig; verify Cloudflare SMTP supports it |
| 3 | **P1** | Notification body content could contain sensitive governance details sent via email | Add content classification; strip sensitive details from email body |
| 4 | **P1** | Broadcast creates N notification rows for N members -- no deduplication model | Acceptable for 81 members; add broadcast_id FK if scaling beyond ~500 |
| 5 | **P2** | Notifications are never deleted -- table grows indefinitely | Implement retention policy: archive read notifications >90 days |
| 6 | **P2** | `get_public_bulletins` deduplication is in-memory with O(N) scan | Acceptable for current scale; add DB-level deduplication if bulletin volume grows |
| 7 | **P2** | Only `bulletin` and `arc_decision` types are wired -- 4 other types remain unwired | Wire `meeting_invite`, `vote_notice`, `arc_update`, `election_notice` |

---

## Production Readiness Checklist

- [x] No directly stored PII (references member_id FK only)
- [ ] SMTP TLS enforced in production
- [ ] Secrets in AWS Secrets Manager
- [x] Health check endpoint responds (via app-level `/health`)
- [x] Ownership validation on mark_read (prevents cross-member access)
- [ ] Email delivery retry mechanism
- [ ] Data retention policy for old notifications
- [x] Rate limiting (via app-level limiter)
- [x] Error responses don't leak internals
- [ ] All notification types wired to triggers
