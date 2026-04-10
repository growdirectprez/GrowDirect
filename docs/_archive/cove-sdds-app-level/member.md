# SDD: Member Module

**Status:** Active
**Last updated:** 2026-03-29
**Blueprint:** `member_bp`, registered at `/member`

---

## Overview

Manages member-facing pages: dashboard, HOA directory, profile editor (with avatar upload), first-login onboarding, privacy consent, and in-app notifications. Directory listings are parcel-first — every lot is listed whether or not it has a registered Cove account.

---

## Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/member/dashboard` | Required | Member home page with recent notifications and profile summary |
| GET | `/member/directory` | Required | HOA directory, grouped by street; accepts `?q=` search |
| GET | `/member/profile` | Required | Show profile editor with current values |
| POST | `/member/profile` | Required | Update contact info, directory prefs, profile fields, and avatar |
| GET | `/member/uploads/avatars/<filename>` | Required | Serve uploaded avatar image files |
| GET | `/member/directory/<apn>` | Required | APN-centric profile page with household contacts, pets, and profile data |
| GET | `/member/accept-privacy` | Required | Privacy policy acceptance form (redirects to dashboard if already accepted) |
| POST | `/member/accept-privacy` | Required | Record privacy consent timestamp |
| GET | `/member/onboarding` | Required | First-login setup form (redirects to dashboard if already onboarded) |
| POST | `/member/onboarding` | Required | Complete onboarding — sets contact info, assigns member role |
| GET | `/member/notifications` | Required | List all notifications for the current member (up to 50) |
| POST | `/member/notifications/<notification_id>/read` | Required | Mark a single notification as read; 404 if not found or not owned |
| POST | `/member/notifications/read-all` | Required | Mark all unread notifications as read |

---

## Forms

**`cove/member/forms.py`**

### `ProfileForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `display_name` | `StringField` | Optional, Length(max=255) | How the member appears in the directory |
| `bio` | `TextAreaField` | Optional, Length(max=1000) | Short intro visible to neighbors |
| `personal_email` | `StringField` | Optional, Email, Length(max=255) | Used for forwarding and notifications |
| `phone` | `StringField` | Optional, Length(max=20) | |
| `avatar` | `FileField` | FileAllowed(jpg, jpeg, png, gif, webp) | Profile photo upload |
| `share_avatar` | `BooleanField` | | Default True |
| `share_bio` | `BooleanField` | | Default True |
| `show_phone` | `BooleanField` | | Default False |
| `show_email` | `BooleanField` | | Default False |

### `OnboardingForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `display_name` | `StringField` | Optional, Length(max=255) | |
| `personal_email` | `StringField` | Optional, Email, Length(max=255) | |
| `phone` | `StringField` | Optional, Length(max=20) | |
| `show_email` | `BooleanField` | | Default False |
| `show_phone` | `BooleanField` | | Default False |

### `PrivacyAcceptForm` (extends `CoveForm`)

| Field | Type | Validators | Notes |
|-------|------|------------|-------|
| `accepted` | `BooleanField` | (checked manually in route) | Must be True to proceed |

---

## Models Used

**Member** (`members`):
- `personal_email`, `phone` — updated via profile and onboarding forms
- `lot_email` — displayed in directory (always visible; property-based identity)
- `onboarded` — gate for onboarding redirect
- `organization_id` — used to scope all directory queries
- `privacy_consent_at` — timestamp of privacy policy acceptance

**DirectoryPreference** (`directory_preferences`):
- One row per member; created on first update
- `show_name`, `show_address` — default True (set during onboarding)
- `show_email`, `show_phone` — default False; opt-in only
- Board view bypasses all preferences

**ParcelProfile** (`parcel_profiles`):
- One row per parcel (keyed by `parcel_id`, not member)
- `display_name`, `avatar_url`, `bio` — text fields
- `pets` — JSON array (`[{"name": ..., "type": ..., "breed": ...}]`)
- Note: `household_members` was migrated to the `parcel_contacts` table (see `ParcelContact` model); the JSON column on `ParcelProfile` is no longer used
- Share toggles: `share_bio` (default True), `share_avatar` (default True), `share_household` (default False), `share_pets` (default True)

**Parcel** (`parcels`):
- Directory queries go through `Parcel`, not `Member`
- `is_association_member=True` filter used to exclude non-HOA parcels
- `owner_name`, `street`, `address`, `lot_number`, `apn`, `lot_email` sourced from parcel

---

## Services

**`cove/member/services.py`**

| Function | What it does |
|----------|-------------|
| `get_directory_listings(org_id, board_view=False)` | Returns all `is_association_member` parcels as dicts, sorted street/address. Enriches with member contact and profile data. Privacy prefs applied unless `board_view=True` |
| `search_directory(org_id, query, board_view=False)` | Case-insensitive search across `owner_name`, `street`, `address`, `apn`. Calls `get_directory_listings` if query is empty |
| `update_directory_preferences(member_id, ...)` | Upserts `DirectoryPreference` row |
| `complete_onboarding(member, ...)` | Sets contact fields, marks `onboarded=True`, assigns `member` role if not already assigned, sets directory prefs |

**`cove/member/profile_services.py`**

| Function | What it does |
|----------|-------------|
| `get_or_create_profile(parcel_id)` | Returns existing `ParcelProfile` or creates an empty one |
| `update_profile(parcel_id, **kwargs)` | Sets any combination of allowed profile fields: `display_name`, `avatar_url`, `bio`, `pets`, `share_bio`, `share_household`, `share_pets`, `share_avatar` (note: `household_members` migrated to `parcel_contacts` table) |
| `get_parcel_profile_data(parcel_id)` | Builds complete parcel profile including contacts from `ParcelContact` model, pets, and visibility toggles |
| `get_profile_for_directory(parcel_id)` | Returns only share-toggled-on fields; returns all-None dict if no profile exists |

**`cove/notifications/services.py`** (integrated by member routes)

| Function | What it does |
|----------|-------------|
| `notify_member(org_id, member_id, notification_type, title, ...)` | Creates a Notification and optionally sends email to member's lot email |
| `notify_all_members(org_id, notification_type, title, ...)` | Sends notification to all active members; respects `delivery_preference` |
| `get_notifications(member_id, unread_only, limit)` | Returns notifications newest first |
| `unread_count(member_id)` | Count of unread notifications (used by context processor in `create_app`) |
| `mark_read(notification_id, member_id)` | Marks a notification as read; returns False if not found or not owned |
| `mark_all_read(member_id)` | Marks all unread notifications as read; returns count updated |

---

## Templates

| Template | Description |
|----------|-------------|
| `member/dashboard.html` | Welcome page with navigation cards and recent notifications |
| `member/directory.html` | Street-grouped listing; Alpine.js for search, avatar display |
| `member/onboarding.html` | First-login form: display name, personal email, phone, directory opt-ins |
| `member/profile.html` | Full profile editor: contact, directory prefs, bio, household, pets, avatar upload |
| `member/accept_privacy.html` | Privacy policy acceptance form with checkbox and submit |
| `member/notifications.html` | List of all notifications with read/unread state and mark-all-read action |

---

## Avatar Upload

- Stored at `UPLOAD_FOLDER/avatars/{uuid_hex}.{ext}`
- Allowed extensions: `jpg`, `jpeg`, `png`, `gif`, `webp`
- Max size: `MAX_AVATAR_SIZE` config (default 2 MB)
- Served at `/member/uploads/avatars/<filename>` (login-gated via `@login_required`)
- URL stored in `ParcelProfile.avatar_url` via `url_for("member.serve_avatar", filename=filename)`

---

## Privacy Rules

- Lot email: always shown (property identity, not personal)
- Name and address: shown by default; member can opt out via `DirectoryPreference`
- Personal email and phone: hidden by default; explicit opt-in required
- Profile bio and pets: shared by default via `share_*` toggles
- Household members: hidden by default (`share_household=False`)
- Board view overrides all prefs (passed as `board_view=True` to service functions)
- Privacy consent: `before_request` hook in `cove/__init__.py` redirects onboarded members who haven't accepted to `/member/accept-privacy`
