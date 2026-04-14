# SDD: Cove Sitemap Redesign

> **Type:** App Service
> **Status:** Pre-build — CSS refresh (Phase 1) complete, remaining phases in backlog
> **Scope:** Information architecture overhaul, route consolidation, role gating
> **Decision:** [2026-04-01-cove-sitemap-redesign](/docs/decisions/2026-04-01-cove-sitemap-redesign.md)
> **Date:** 2026-04-01 (ops upgrade 2026-04-13)

**Wiki:** [[Brain/wiki/cove-governance|Cove Governance]]

---

## 1. Overview

Restructure Cove from 9 member-facing nav sections into 4, merge duplicated document stores, separate research tooling behind a role gate, and make the public landing page a transparent bulletin board that doubles as the login page.

**Core thesis:** Cove exists for secure votes and community confidence. The member experience is: show up, see what's happening, vote, leave.

---

## 2. Architecture Changes

### 2.1 Role Model

No new roles needed. Existing roles map cleanly:

| Role | Sees | Gate |
|------|------|------|
| Anonymous (public) | Public bulletin + Contact the Board widget | None |
| Member | Home, Vote, Documents, Community | `@login_required` |
| Board (`is_board`) | Board Dashboard (all operational tools) | `@board_required` |
| ARC Historian (`is_arc`) | Research Workbench | `@arc_required` (new decorator, checks `member.is_arc`) |

**Note:** Research uses `is_arc` not `is_admin`. The ARC role is narrower and purpose-built for the Historian workbench. `is_admin` grants broader privileges and should not be conflated with research access.

### 2.2 Blueprint Changes

Current → New blueprint registration:

| Current Blueprint | Prefix | Disposition |
|-------------------|--------|-------------|
| `public_bp` | `/` | **Keep** — becomes public bulletin |
| `auth_bp` | `/auth` | **Keep** — no changes |
| `member_bp` | `/member` | **Keep** — Home + profile + notifications + onboarding |
| `governance_bp` | `/vote` | **Rename prefix** from `/vote` (already correct) — becomes Vote section |
| `proceeding_bp` | `/proceedings` | **Keep under Vote** — compliance log |
| `election_bp` | `/vote/election` | **Keep under Vote** — already nested |
| `vault_bp` | `/vault` | **Rename** to `/documents` — becomes Documents section |
| `board_bp` | `/board` | **Expand** — absorbs Treasury admin, Meetings admin, Document publishing |
| `treasury_bp` | `/treasury` | **Relocate** — all routes move behind `/board/treasury` |
| `parcels_bp` | `/parcels` | **Split** — simple view in Community, deep data in Research |
| `meetings_bp` | `/meetings` | **Split** — member views meeting details, board manages scheduling |
| `agent_bp` | `/agent` | **Keep** — no changes |
| `archive_bp` | `/archive` | **Split** — catalog/public docs merge into Documents, deep archive into Research |
| `map_bp` | `/map` | **Split** — simple fixed map in Community, advanced layers in Research |

### 2.3 New Blueprint: `community_bp`

**Prefix:** `/community`

This blueprint replaces the separate Directory, Map, and Parcels member views with a single unified community page.

**Routes:**

```
GET  /community/              → community map-directory page
GET  /community/lot/<apn>     → full community profile page for a lot
GET  /community/profile       → redirect to member.profile (my profile)
GET  /community/api/geojson   → simplified parcel GeoJSON (names, addresses, APNs only)
GET  /community/api/lot/<apn> → lot profile data for popup card (JSON)
```

### 2.4 New Blueprint: `research_bp`

**Prefix:** `/research`

Role-gated to ARC Admin. Absorbs all advanced map, parcel lineage, and archive research features.

**Auth:** `@login_required` + `@arc_required` (checks `member.is_arc`, not `is_admin` — narrower, purpose-built for ARC Historian role)

**Routes (relocated from existing blueprints):**

```
# From map_bp
GET  /research/map                        → advanced map page (full layer system)
GET  /research/map/api/geojson            → enriched parcel GeoJSON
GET  /research/map/api/lot-h              → Lot H research GeoJSON
GET  /research/map/api/neighborhood       → neighborhood context GeoJSON
GET  /research/map/api/layers/<filename>  → serve layer GeoJSON
GET  /research/map/api/layers             → layer manifest
GET  /research/map/api/overlays           → overlay manifest
GET  /research/map/api/categories         → categories
GET  /research/map/api/presets            → saved presets
POST /research/map/api/boundaries/parse   → parse legal description
GET  /research/map/api/land-divisions     → land divisions GeoJSON
GET  /research/map/api/land-divisions/centroids
GET  /research/map/api/land-divisions/<id>
GET  /research/map/api/land-divisions/<id>/tree
GET  /research/map/api/lot-h/blast-zone
GET  /research/map/api/lot-h/parcel/<apn>
GET  /research/map/api/research/stats
GET  /research/map/api/research/chart-data
GET  /research/map/api/research/<apn>

# From archive_bp
GET  /research/archive/                   → archive landing
GET  /research/archive/timeline           → timeline view
GET  /research/archive/chain              → chain of title
GET  /research/archive/catalog            → full catalog with deep filters
GET  /research/archive/doc/<cat>/<slug>   → view archive document
GET  /research/archive/data/<filename>    → serve CSV/JSON data
GET  /research/archive/originals/<path>   → serve PDF/images
POST /research/archive/request/<path>     → request original
GET  /research/archive/promote/<path>     → promote to documents
POST /research/archive/promote/<path>     → execute promote

# From parcels_bp (deep features)
GET  /research/parcels/                   → full parcels list with tags
POST /research/parcels/tags/create        → create tag
POST /research/parcels/tags/<id>/assign   → assign tag
POST /research/parcels/tags/<id>/remove   → remove tag
GET  /research/parcels/<apn>              → deep parcel detail (research view)
```

---

## 3. Page-by-Page Specifications

### 3.1 Public Bulletin (Landing Page)

**Route:** `GET /` (public_bp)
**Template:** `templates/public/index.html` (replaces current redirect-to-login)
**Auth:** None required

**Layout:**
- Full-width page, no sidebar
- Top bar: Cove logo left, "Sign In" button right
- Single column, max-width 640px, centered

**Content (top to bottom):**
1. **Community header** — "West Portuguese Bend Community Association" + Cove logo
2. **Pinned items** — upcoming vote (title + date + "sign in to vote" link), next meeting (date + location)
3. **Board announcements** — reverse chronological list of published bulletins. Each: title, date, body excerpt. Paginated (10 per page)
4. **Published results** — certified vote results, recent proceedings (title + status + date). Links require login
5. **Contact the Board widget** — collapsible card at bottom

**Data source:** New `Bulletin` model or extend `Notification` with `is_public=True` flag. Board creates bulletins via Board Dashboard; public ones render here.

**Design decision — bulletin data:** Simplest approach is to add a `public` boolean column to the existing `notifications` table plus a `pinned` boolean. Board bulletins with `public=True` render on the landing page. No new model needed.

**Contact the Board widget (public mode):**
- Collapsible card: "Contact the Board"
- Request type selector: "Request Escrow Documents" | "General Question"
- If escrow: APN dropdown (searchable list of 81 lots by address + APN), name, email, escrow company (text)
- If general: name, email, message (textarea)
- Submit creates a `Notification` with `type='board_request'`, `member_id=NULL`, and stores contact info + APN in a JSON `metadata` field or new columns
- Confirmation message: "Your request has been received. The board will respond to {email}."
- CSRF token via hidden form field (WTForms handles this)

**Login integration:**
- "Sign In" button in top bar opens magic link form (inline or modal)
- "Sign in to vote" / "Sign in to participate" links throughout content
- After auth, redirect to `/member/dashboard` (Home)

### 3.2 Home (Member Dashboard)

**Route:** `GET /member/dashboard` (member_bp — existing)
**Template:** `cove/member/templates/member/dashboard.html` (modify existing)
**Auth:** `@login_required`

**Simplify to bulletin format:**
- Remove quick-links card grid (Directory, Profile, Proposals, Notifications cards)
- Remove membership status card (move assessment status inline)

**New layout (single column, max-width 640px):**
1. **Header** — "Welcome, {name}" + lot identifier + assessment status badge inline
2. **Your action items** — open ballots you haven't voted on (direct links to ballot page), ARC applications pending your input. Only shows if items exist
3. **Board announcements** — same feed as public bulletin, but includes member-only notifications. Each: title, date, body. Unread items highlighted
4. **Upcoming** — next meeting (date, location, agenda link), next vote closing date
5. **My requests** — list of your board requests with status (if any exist)

### 3.3 Vote (Governance)

**Routes:** Existing governance_bp, election_bp, proceeding_bp — **no route changes needed**
**Templates:** Existing governance templates — **review during blueprint for visual polish only**

The governance engine is solid. Changes are cosmetic only:
- Proposals list: apply sharp CSS, tighten spacing
- Ballot page: make it feel official and ceremonial — strong border, prominent yes/no/abstain
- Results page: certified results with chain hash visible
- Elections: same treatment
- Proceedings: compliance log, clean table view

**Nav label change:** "Governance" → "Vote" in sidebar

### 3.4 Documents (Merged Vault + Archive public docs)

**Route:** Rename vault_bp prefix from `/vault` to `/documents`
**Template:** Modify existing vault templates

**Changes:**
- Vault index becomes Documents index — add category filters that include archive document types
- Add categories: "Bylaws & CC&Rs", "Meeting Minutes", "Board Resolutions", "Operating Rules", "Financial Reports"
- Archive's public-facing catalog documents (bylaws view, promoted docs) render here alongside vault uploads
- Upload route: board-only (move upload behind `@board_required` check if not already)
- Member view is read-only: browse, search, download
- Remove separate archive landing, timeline, chain pages from member nav (those go to Research)

**Route changes:**
```
GET  /documents/                    → document list with category filters + search
GET  /documents/<doc_id>            → document detail
GET  /documents/<doc_id>/download   → download latest
GET  /documents/<doc_id>/download/<version_id> → download version
GET  /documents/bylaws              → filtered view: bylaws & CC&Rs category
GET  /documents/minutes             → filtered view: meeting minutes category
```

Board-only routes (relocate to board_bp or keep with `@board_required`):
```
GET|POST /documents/upload          → upload document (board only)
POST     /documents/<doc_id>/version → upload new version (board only)
```

### 3.5 Community (Map-as-Directory)

**Route:** New `community_bp` at `/community`
**Template:** New `templates/community/index.html`

**Layout:** Full-bleed map, no sidebar padding on this page. Sidebar still visible but content area extends edge-to-edge.

**Map component:**
- Fixed zoom level showing all of WPBCA tract — no user zoom/pan (or constrained to tract bounds)
- All 81 lots rendered as clickable polygons
- Lot polygons colored by status: active member (cove teal fill), no account (cream fill), board member (accent border)
- On lot click: popup card appears anchored to the lot

**Lot profile card (popup):**
- Compact card: lot number, street address, APN (mono)
- Resident/owner name
- Lot email (clickable mailto)
- Member since date (if account exists)
- "View full profile →" link to `/community/lot/<apn>`
- If no account: "No registered member" + address only

**Slide-out directory panel:**
- Triggered by a "Directory" button/tab on the right edge of the map (same as layers panel trigger)
- Panel slides from right, 380px wide (same as `cove-slide-panel`)
- Alphabetical tabs along the right edge (A-Z, clickable)
- Entries: compact lot cards — address number, street, resident name, lot email
- Tap entry → map pans/highlights the lot, popup card appears
- Tap lot on map → directory panel scrolls to that entry, highlights it
- Search bar at top of panel

**"My Profile" link** in the panel header → redirects to `/member/profile`

**API endpoints:**
```
GET /community/api/geojson   → simplified GeoJSON (lot polygons + basic data only, no research fields)
GET /community/api/lot/<apn> → JSON: name, address, lot_email, member_since, avatar_url, bio
```

**Data source:** Existing `parcels` table + `members` table (joined via `Member.apn` → `Parcel.apn`, NOT `parcel_id`) + `parcel_profiles` + `directory_preferences`. No new models. The simplified GeoJSON endpoint returns only what's needed for the community view — no research data, no temporal fields, no tag data.

**Privacy controls:** The GeoJSON and lot data endpoints MUST respect `DirectoryPreference` visibility settings. If a member has `show_name=False`, the resident name is not included in GeoJSON or popup cards. Same for `share_bio`, `share_avatar`, etc. This matches the existing directory behavior and avoids a privacy regression.

**Null geometry handling:** Parcels without geometry data (`geometry=None`) produce features with `null` geometry. The Leaflet client must skip rendering for null-geometry features gracefully — they still appear in the directory panel by address.

### 3.6 Board Dashboard (Expanded)

**Route:** Existing board_bp at `/board`
**Template:** Modify `cove/board/templates/board/dashboard.html`

**Absorbs:**
1. **Treasury** — all treasury routes move to `/board/treasury/*` (re-register treasury_bp under board prefix or add routes directly)
2. **Meeting management** — create, edit, cancel routes move to `/board/meetings/*`
3. **Document publishing** — upload and version routes gated to board
4. **Request inbox** — filtered view of `board_request` type notifications
5. **Bulletin composer** — existing bulletin route, enhanced with `public` and `pinned` toggles

**Board Dashboard home (`GET /board/`):**
- Stats row: total members, active votes, pending requests, delinquent count
- Quick actions: "New Announcement", "New Proposal", "New Meeting"
- Recent requests (from Contact the Board widget)
- Upcoming meetings
- Active proposals with vote counts

**Board sub-sections (in board nav, not member nav):**
```
/board/                          → dashboard home
/board/members                   → roster management (existing)
/board/members/invite            → invite member (existing)
/board/delinquent                → delinquent tracking (existing)
/board/treasury/                 → treasury overview (relocated)
/board/treasury/assessments      → assessments (relocated)
/board/treasury/budget           → budget (relocated)
/board/treasury/assessments/create → create assessment (relocated)
/board/meetings/                 → meetings management
/board/meetings/create           → create meeting (relocated)
/board/meetings/<id>/edit        → edit meeting (relocated)
/board/meetings/<id>/cancel      → cancel meeting (relocated)
/board/arc/pending               → ARC review queue (relocated)
/board/arc/<id>/review           → ARC decision (relocated)
/board/bulletin                  → compose announcement (existing, add public/pinned)
/board/requests                  → request inbox (new route)
/board/documents/upload          → upload document (relocated)
/board/parcels/<apn>/contacts    → parcel contacts (existing)
/board/diagrams                  → diagrams (existing)
```

### 3.7 Contact the Board Widget (Member Mode)

**Location:** Appears on Home page (member dashboard) as a collapsible card

**Behavior:**
- Pre-filled: member name, lot email, APN
- Request type: "Question" | "Request Escrow Documents" | "Report an Issue"
- If escrow: APN dropdown defaults to their own lot but can select any of 81
- Message textarea
- Submit creates `Notification` with `type='board_request'`, `member_id=current_user.id`, APN reference
- Shows "Your request has been submitted" confirmation
- Member can see their request history in a "My Requests" section on Home

### 3.8 Research Workbench (ARC Historian)

**Route:** New `research_bp` at `/research`
**Auth:** `@login_required` + `@admin_required` (or new `@arc_required` decorator)
**Template:** New `templates/research/index.html`

**Landing page:** Links to three sub-sections:
- **Map** — full advanced map with layers, overlays, tract history, boundary calibration
- **Archive** — timeline, chain of custody, document provenance, catalog
- **Parcels** — tags, deep parcel profiles, research data

**Implementation approach (simplified per factory review):** Gate the existing map, archive, and parcels blueprints in place using a `@arc_required` decorator and `before_request` hook. No need to wrap view functions in a new blueprint — just add the role check to existing blueprints. The `research_bp` provides a landing page at `/research/` that links to `/map/`, `/archive/`, `/parcels/` (existing URLs, now gated). Templates stay unchanged. This is simpler than relocating routes under a new prefix.

The map template stays the same (already has all the layer/overlay/calibration UI). Archive templates stay the same. Parcels deep view stays the same.

---

## 4. Navigation Changes

### 4.1 Member Sidebar (`templates/components/nav.html`)

**Before (9 items):**
Dashboard, Directory, Governance, Vault, Meetings, Parcels, Map, Treasury, Archive

**After (4 items):**
```
Home        → /member/dashboard
Vote        → /vote (governance.proposals)
Documents   → /documents (vault.index, renamed)
Community   → /community (new)
```

Board section (if `current_user.is_board`):
```
── Board ──
Dashboard   → /board/
```

Research section (if `current_user.is_admin`):
```
── Research ──
Workbench   → /research/
```

### 4.2 Member-facing Meeting Access

Meetings no longer have their own nav item. The `meetings_bp` stays registered at `/meetings` for member-facing routes. Board-only routes (create, edit, cancel) are duplicated under `/board/meetings/*` and the original routes get `@board_required` added.

**Member-accessible routes (stay in meetings_bp):**
- `GET /meetings/<id>` — meeting detail (linked from Home page)
- `GET /meetings/<id>/calendar.ics` — calendar download
- `GET /meetings/arc/apply` — ARC application form (member-facing)
- `GET /meetings/arc/<id>` — ARC application status (member-facing)

**Board-only routes (move to board_bp, originals get @board_required):**
- `POST /meetings/create` → also at `/board/meetings/create`
- `POST /meetings/<id>/edit` → also at `/board/meetings/<id>/edit`
- `POST /meetings/<id>/cancel` → also at `/board/meetings/<id>/cancel`

Members access meetings via:
- Home page: "Next meeting" card with date, location, agenda link
- Direct links to `/meetings/<id>` from notifications and Home
- ARC application: `/meetings/arc/apply` — linked from Home or Community

### 4.3 Board Sub-navigation

The Board Dashboard gets its own sub-nav (within the board template, not the main sidebar):
```
Overview | Members | Treasury | Meetings | Documents | ARC | Requests | Compliance
```

---

## 5. Data Model Changes

### 5.1 Notification Table — Bulletin Support Only

**Factory review finding:** The original design overloaded Notification for both bulletins and board requests. This caused three critical issues: `member_id` is NOT NULL, `notify_all_members()` creates N rows per bulletin (incompatible with single public row), and JSON metadata is wrong abstraction for structured request data. Board requests are now a separate model (§5.2).

```python
# Add to existing Notification model
public: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false')
pinned: Mapped[bool] = mapped_column(Boolean, default=False, server_default='false')
updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())  # platform standard — was missing
```

**Bulletin creation flow:** Board creates announcement → `notify_all_members()` creates per-member rows as before. Public visibility is handled by querying member notifications with `public=True` flag. The `member_id` NOT NULL constraint stays intact — no nullable FK migration needed.

**Open decision (GRO-402):** Whether public bulletin page queries per-member rows with `public=True` (simple but N rows per bulletin) or needs a separate flow. Parked for fresh eyes.

**Migration:** Single Alembic migration adding `public`, `pinned`, `updated_at` columns.

### 5.2 BoardRequest Table — New Model

Board requests from the Contact the Board widget are a dedicated model, not Notification.

```python
class BoardRequest(BaseModel):
    __tablename__ = "board_requests"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    request_type: Mapped[str] = mapped_column(String(30))    # escrow, question, complaint
    status: Mapped[str] = mapped_column(String(30), default="new")  # new, read, in_progress, resolved
    apn: Mapped[str | None] = mapped_column(String(20), ForeignKey("parcels.apn"), nullable=True)
    member_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("members.id"), nullable=True)
    requester_name: Mapped[str] = mapped_column(String(120))
    requester_email: Mapped[str] = mapped_column(String(255))
    escrow_company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
```

**Why separate:** APN is a real FK (queryable, indexable). Status lifecycle is clean. No nullable FK hack on Notification. Standard SQL for all filtering — no JSON extraction.

### 5.3 No Other Model Changes

The existing models support the redesign without modification:
- `Parcel`, `Member`, `ParcelProfile`, `DirectoryPreference` → Community map-directory
- `Proposal`, `Ballot`, `BallotEnvelope`, `Election`, `Candidate` → Vote (unchanged)
- `Document`, `DocumentVersion` → Documents (unchanged, just renamed routes)
- `Meeting`, `ARCApplication`, `ARCReview` → Board Meetings admin (member detail stays accessible)
- All research models → Research workbench (unchanged)
- `Notification` → bulletins and member notifications (NOT board requests)

---

## 6. Implementation Phases

Factory review simplified from 10 phases to 8. Notification migration folds into Public Bulletin. Home Page Simplification folds into Contact Widget (same template). Cleanup is QA on every phase, not a separate phase.

### Phase 1: CSS Refresh (GRO-390)
**Status:** Complete — Tailwind config updated, cove.css rewritten, compiled.
**Files changed:** `tailwind.config.js`, `static/css/cove.css`, `static/css/dist/main.css`
**Risk:** Low — visual only, no logic changes
**Test:** Visual inspection of all existing pages. Delete orphaned `static/src/main.css` and `static/css/brand.css`.

### Phase 2: Navigation Simplification (GRO-391)
**Scope:** Update nav.html to 4 member items + board/research sections. No route changes yet — just the nav links. Use temporary URLs pointing to existing routes.
**Files:** `templates/components/nav.html`
**Test:** All nav links resolve. Board/research sections show/hide by role. Mobile nav toggle works.

### Phase 3: Public Bulletin Landing Page (GRO-393, includes GRO-402 migration)
**Scope:** Replace `public_bp` index with bulletin page. Add `public`, `pinned`, `updated_at` columns to Notification. Create standalone public template (no base_public.html needed — standalone HTML with CSS include). Integrate login prompt.
**Files:** `cove/public/routes.py`, `templates/public/index.html`, `cove/models/notification.py`, new migration
**Test:** Anonymous user sees bulletin. Login flow still works. Board can create public bulletins. Empty state handled gracefully.

### Phase 4: Contact Widget + Home Simplification (GRO-394, GRO-401, GRO-398)
**Scope:** BoardRequest model + migration. Public and member request forms. Board request inbox. Rewrite member dashboard to bulletin format with action items and request history.
**Files:** New `cove/models/board_request.py`, `cove/public/forms.py`, routes in `public_bp` + `member_bp` + `board_bp`, `member/dashboard.html` rewrite
**Test:** Public user submits escrow request with APN. Member submits question. Board sees inbox. Dashboard is single-column bulletin format with action items.

### Phase 5: Documents Consolidation (GRO-395)
**Scope:** Rename vault_bp prefix to `/documents`. Add category filters. Gate upload to board. Add 301 redirects from `/vault/*`.
**Files:** `cove/__init__.py` (prefix), `cove/vault/routes.py`, vault templates, redirect routes
**Test:** All document links work at new prefix. Upload restricted to board. Categories filter correctly.

### Phase 6: Community Map-Directory (GRO-396)
**Scope:** New `community_bp`. Fixed map view with privacy-aware GeoJSON. Slide-out directory panel. Lot profile cards and lot profile page. Simplified GeoJSON respecting `DirectoryPreference`. Handle null geometry parcels.
**Files:** New blueprint `cove/community/`, new templates, new GeoJSON route
**Dependencies:** Existing parcel GeoJSON, member data, parcel profiles, directory preferences
**Test:** Map renders 81 lots. Click lot → popup card. Directory panel. Privacy preferences respected. Null geometry parcels in directory only. `/member/directory` redirects 301.

### Phase 7: Board Dashboard Expansion (GRO-397)
**Scope:** Relocate treasury, meetings admin, document upload routes behind `/board`. Add board sub-nav. Add bulletin public/pinned toggles. Meetings detail routes stay in `meetings_bp` for members.
**Files:** `cove/board/routes.py` (expand), board templates, redirect routes
**Test:** Treasury at `/board/treasury`. Meeting create at `/board/meetings/create`. Old URLs redirect. Member still accesses `/meetings/<id>` and `/meetings/arc/apply`.

### Phase 8: Research Workbench Gate (GRO-399, GRO-400 cleanup)
**Scope:** Gate existing map, archive, parcels blueprints with `@arc_required` decorator + `before_request` hook. New `research_bp` landing page. Role-dependent redirects (302). Final cleanup: orphaned templates, full test suite, visual QA all roles.
**Files:** New `cove/research/` blueprint, `@arc_required` decorator, redirect routes, cleanup pass
**Test:** Non-ARC cannot access `/research/*`. All research features work. Role-dependent redirects correct. Full pytest passes. No dead links.

---

## 7. Route Redirect Map

Old URLs that need redirects to maintain bookmarks or external links.

**Fixed redirects (301):**

| Old Path | New Path |
|----------|----------|
| `/vault/` | `/documents/` |
| `/vault/<id>` | `/documents/<id>` |
| `/vault/<id>/download` | `/documents/<id>/download` |
| `/vault/<id>/download/<ver>` | `/documents/<id>/download/<ver>` |
| `/member/directory` | `/community/` |
| `/member/directory/<apn>` | `/community/lot/<apn>` |
| `/treasury/` | `/board/treasury/` |
| `/treasury/assessments` | `/board/treasury/assessments` |
| `/treasury/budget` | `/board/treasury/budget` |

**Role-dependent redirects (302 — cannot be cached):**

| Old Path | Logic |
|----------|-------|
| `/map/` | If `is_arc` → `/research/map`, else → `/community/` |
| `/archive/` | If `is_arc` → `/research/archive/`, else → `/documents/` |
| `/archive/timeline` | If `is_arc` → `/research/archive/timeline`, else → `/documents/` |
| `/archive/chain` | If `is_arc` → `/research/archive/chain`, else → `/documents/` |
| `/archive/catalog` | If `is_arc` → `/research/archive/catalog`, else → `/documents/` |
| `/parcels/` | If `is_arc` → `/research/parcels/`, else → `/community/` |
| `/parcels/<apn>` | If `is_arc` → `/research/parcels/<apn>`, else → `/community/lot/<apn>` |

**Routes that stay (not redirected):**

| Path | Reason |
|------|--------|
| `/meetings/<id>` | Member-accessible meeting detail — stays in meetings_bp |
| `/meetings/arc/apply` | Member-accessible ARC application — stays in meetings_bp |
| `/meetings/arc/<id>` | Member-accessible ARC status — stays in meetings_bp |
| `/map/api/*` | API routes stay until community GeoJSON replaces them; research routes proxy to originals |

---

## 8. Files Changed Summary

### New files:
- `cove/models/board_request.py` — BoardRequest model
- `cove/community/__init__.py` — community blueprint
- `cove/community/routes.py` — community routes
- `cove/community/templates/community/index.html` — map-directory page
- `cove/community/templates/community/lot.html` — lot profile page
- `cove/research/__init__.py` — research blueprint
- `cove/research/routes.py` — research landing + role gate
- `cove/research/templates/research/index.html` — research landing
- `cove/auth/decorators.py` — `@arc_required` decorator (if not already present)
- `migrations/versions/xxxx_add_bulletin_fields.py` — notification public/pinned/updated_at
- `migrations/versions/xxxx_create_board_requests.py` — board_requests table
- `cove/public/templates/public/index.html` — standalone bulletin page (no base template)
- `cove/public/forms.py` — contact the board form

### Modified files:
- `cove/__init__.py` — register new blueprints, rename vault prefix
- `templates/components/nav.html` — 4 member items + board/research sections
- `cove/member/templates/member/dashboard.html` — bulletin format with action items
- `cove/vault/routes.py` — renamed prefix, board-gated uploads
- `cove/board/routes.py` — absorb treasury, meetings admin, request inbox
- `cove/board/templates/board/dashboard.html` — expanded with sub-nav
- `cove/models/notification.py` — add public, pinned, updated_at fields

### Unchanged (reused at new paths):
- All governance templates (Vote)
- Map/archive/parcels templates (gated to ARC role, not relocated)
- Auth templates
- Meeting detail + ARC apply templates (still member-accessible in meetings_bp)

---

## Purpose

Restructure Cove's information architecture from 9 member-facing navigation
sections into 4, merge duplicated document stores, separate research tooling
behind a role gate, and make the public landing page a transparent bulletin
board. The member experience becomes: show up, see what's happening, vote, leave.

---

## Dependencies

| Dependency | Type | Required |
|------------|------|----------|
| Cove Flask (port 5002) | Host app | Yes |
| PostgreSQL (`cove` database) | All data storage | Yes |
| Valkey DB 1 | Sessions | Yes |
| Existing blueprints (14) | Routes being reorganized | Yes |
| Leaflet.js | Community map-directory | Yes (already installed) |

---

## Data Flow & PII Map

### PII in New Features

| Field | Location | Classification | Encryption |
|-------|----------|---------------|------------|
| Board request — requester name | `board_requests.requester_name` | **internal** | Plaintext |
| Board request — requester email | `board_requests.requester_email` | **sensitive** | **Plaintext (P0)** |
| Board request — escrow company | `board_requests.escrow_company` | internal | Plaintext |
| Community GeoJSON — resident name | API response | **internal** (respects DirectoryPreference) | N/A (not stored separately) |
| Community GeoJSON — lot email | API response | **internal** (respects DirectoryPreference) | N/A |

### Privacy Controls

The community map-directory GeoJSON and lot data endpoints MUST respect
`DirectoryPreference` visibility settings. If `show_name=False`, name is excluded.
Same for `share_bio`, `share_avatar`. This matches existing directory behavior.

---

## Operations

### Startup Sequence

No separate startup — all changes are within the Cove Flask app.
Blueprint registration order in `cove/__init__.py` determines route precedence.

### Health Checks

- `GET /health` — existing Cove health check covers all blueprints
- Community GeoJSON: `GET /community/api/geojson` returns valid FeatureCollection
- Role gates: 403 on `/research/*` for non-ARC users

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| Null geometry parcels | Appear in directory panel only, not on map | Leaflet client skips null-geometry features |
| Missing DirectoryPreference | Names shown by default (existing behavior) | Create preference records during member onboarding |
| Board request form CSRF fail | Form submission rejected, user sees error | Standard Flask-WTF CSRF handling |
| Old URL bookmarks | 301 redirects serve correct new path | Redirect map covers all old paths |

### Monitoring

| Metric | Alert Threshold |
|--------|----------------|
| 301 redirect volume | If high 30+ days after launch, update external links |
| Community GeoJSON response time | > 2 seconds |
| Board request submission rate | N/A (informational) |

### Configuration

No new env vars. All configuration uses existing Cove settings.

---

## Deployment

No separate deployment — part of Cove Flask container. Each phase ships
as a standard Cove deployment (Docker image rebuild + restart).

### Migration Requirements

- Phase 3: Alembic migration adding `public`, `pinned`, `updated_at` to `notifications`
- Phase 4: Alembic migration creating `board_requests` table

---

## Code Review Findings

### P0 — Blocks Production

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | `BoardRequest.requester_email` stored plaintext — PII from anonymous visitors | Field-level encryption for requester_email | — |
| 2 | Public contact form (`POST /contact`) has no rate limiting — DoS vector | Flask-Limiter: 5 submissions per IP per hour | — |

### P1 — Before GA

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | Community GeoJSON endpoint returns all 81 parcels in a single response — no pagination | Acceptable for 81 lots; add pagination if lot count exceeds 200 | — |
| 2 | Role-dependent redirects (302) cannot be cached — repeated redirect overhead | Acceptable trade-off for correct role enforcement; monitor redirect volume | — |
| 3 | `@arc_required` decorator exists in `decorators.py` but SDD originally referenced `is_admin` — now correctly uses `is_arc` | Verify all Research routes use `@arc_required`, not `@admin_required` | — |
| 4 | Board request inbox (`GET /board/requests`) has no pagination | Add pagination when request volume exceeds 50 per month | — |
| 5 | `community_bp` GeoJSON route queries all parcels + all members in a loop (N+1 potential) | Use joined query: `Parcel` LEFT JOIN `Member` in single SQL | — |

### P2 — Post-Launch

| # | Finding | Recommended Fix | Linear |
|---|---------|----------------|--------|
| 1 | SVG tract map tracing (post-v1) — lot boundaries from assessor PDF not yet traced | Trace from `docs/maps/LACA-Parcel-Maps-Tract-14649.pdf` when map-directory ships | — |
| 2 | No automated test coverage for 301 redirect map | Add pytest fixtures that verify all old URLs redirect to correct new paths | — |
| 3 | Board sub-navigation component not yet styled | Apply consistent nav tab styling during Phase 7 | — |

---

## Production Readiness Checklist

- [ ] PII encrypted at rest (board request requester_email)
- [ ] Rate limiting on public contact form
- [ ] Community GeoJSON respects DirectoryPreference privacy settings
- [ ] Null geometry parcels handled gracefully in Leaflet client
- [ ] All 301 redirects verified (vault, directory, treasury, archive, parcels)
- [ ] Role-dependent 302 redirects tested for all roles (member, board, ARC)
- [ ] `@arc_required` decorator on all Research workbench routes
- [ ] Board request CSRF protection working on public and member forms
- [ ] All existing pytest tests pass after route prefix changes
- [ ] No dead links in any template after navigation simplification

---

## GRO Issue Specifications

Issues listed in dependency order. Each is a single factory pipeline run.
Full acceptance criteria and implementation details for each phase.

### GRO-390: CSS Refresh — Complete

**Phase 1** | **Priority:** P1 | **Status:** Complete

Tailwind config updated, `cove.css` rewritten, compiled. Files changed:
`tailwind.config.js`, `static/css/cove.css`, `static/css/dist/main.css`.
Added `cream`, `ink`, `shore`, `rust` color scales. Sharp edges (no rounded-lg),
cream/ink warm neutrals.

### GRO-391: Navigation Simplification

**Phase 2** | **Priority:** P1 | **Depends on:** GRO-390

Update `templates/components/nav.html` to 4 member items (Home, Vote, Documents,
Community) + conditional board and research sections. Use temporary URLs pointing
to existing routes until new blueprints land.

**Acceptance:** Member sees 4 nav items. Board member sees 4 + Board. Admin
sees 4 + Board + Research. Mobile nav works.

### GRO-401: BoardRequest Model (Stubbed)

**Phase 4** | **Priority:** P2

Separate model for board requests. See Linear for full spec.

### GRO-402: Notification Bulletin Support (Stubbed)

**Phase 3** | **Priority:** P2

Add `public`, `pinned`, `updated_at` to Notification. Open decision on
bulletin creation flow. See Linear for full spec.

### GRO-393: Public Bulletin Landing Page

**Phase 3** | **Priority:** P2 | **Depends on:** GRO-402, GRO-390

Replace `GET /` redirect-to-login with public bulletin page showing board
announcements, pinned items, and login prompt.

### GRO-394: Contact Widget + Home Simplification

**Phase 4** | **Priority:** P2 | **Depends on:** GRO-401, GRO-393

BoardRequest model + migration. Public and member request forms. Board request
inbox. Rewrite member dashboard to bulletin format.

### GRO-395: Documents Consolidation

**Phase 5** | **Priority:** P2 | **Depends on:** GRO-391

Rename vault_bp prefix `/vault` to `/documents`. Add category filters. Gate
uploads to board. Add 301 redirects.

### GRO-396: Community Map-Directory

**Phase 6** | **Priority:** P2 | **Depends on:** GRO-391, GRO-390

New `community_bp`. Fixed map view with privacy-aware GeoJSON. Slide-out
directory panel. Lot profile cards and pages.

### GRO-397: Board Dashboard Expansion

**Phase 7** | **Priority:** P3 | **Depends on:** GRO-394, GRO-395

Relocate treasury, meeting management, ARC review behind `/board` prefix.
Add sub-navigation. Add request inbox. Add public/pinned toggles to bulletin.

### GRO-399: Research Workbench Gate

**Phase 8** | **Priority:** P3 | **Depends on:** GRO-391

Gate existing map, archive, parcels blueprints with `@arc_required`. New
`research_bp` landing page. Final cleanup pass.

### GRO-398: Home Page Simplification

**Phase 9** | **Priority:** P3 | **Depends on:** GRO-393, GRO-394

Rewrite member dashboard to bulletin format. Remove card grid. Add action
items and request history.

### GRO-400: Cleanup and Redirect Verification

**Phase 10** | **Priority:** P4 | **Depends on:** All previous

Remove orphaned templates, verify all redirects, run full test suite,
delete unused CSS files.

### Dependency Graph

```
GRO-390: CSS Refresh (DONE) ──────────────────────┐
GRO-391: Nav Simplification ──────────────────────┤
GRO-402: Bulletin fields (stub) ──┐               │
                                  ├→ GRO-393 ─────┤
GRO-401: BoardRequest (stub) ────┤                │
                                  └→ GRO-394 ─────┤ (includes GRO-398)
GRO-395: Documents ───────────────────────────────┤
GRO-396: Community Map-Directory ─────────────────┤
GRO-397: Board Dashboard ────────────────────────┤
GRO-399: Research Gate ──────────────────────────┤ (includes GRO-400)
```

---

*This SDD describes systems as they will exist after implementation. Update in place as phases ship.*
