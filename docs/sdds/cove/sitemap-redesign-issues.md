# GRO Issue Specs — Cove Sitemap Redesign

**Parent SDD:** [sitemap-redesign.md](sitemap-redesign.md)
**Decision:** [2026-04-01-cove-sitemap-redesign](/docs/decisions/2026-04-01-cove-sitemap-redesign.md)

Issues listed in dependency order. Each is a single factory pipeline run.

---

## GRO-390: CSS Refresh — Sharp Professional Aesthetic

**Priority:** P1 — no dependencies, unblocks visual QA on everything else
**Phase:** 1

### Scope
The Tailwind config and cove.css have already been updated. This issue is: commit the changes, rebuild CSS in the container, and visually verify all existing pages render correctly with the new styles.

### Files already changed
- `tailwind.config.js` — added `cream`, `ink`, `shore`, `rust` color scales; added `font-body`, `font-ui` mappings
- `static/css/cove.css` — full rewrite: sharp edges (no rounded-lg), cream/ink warm neutrals, stronger borders, data-dense table/card/form styling, mono font for labels/badges/status
- `static/css/dist/main.css` — rebuilt (76KB compiled)
- `templates/components/flash.html` — updated to use proper alert styling instead of badge class
- `templates/components/footer.html` — updated to use brand colors

### Acceptance
- [ ] All existing pages render without broken layouts
- [ ] Cards have sharp edges (not rounded)
- [ ] Badges/status use flat square style (not pills)
- [ ] Nav sidebar shows cove teal left-border active indicator
- [ ] Forms use cream/ink colors, not generic gray
- [ ] Tables have cream-100 header row, ink-200 border
- [ ] No visual regressions on governance, board, or map pages

### Notes
The orphaned `cove/static/src/main.css` and `cove/static/css/brand.css` files can be deleted — they are not part of the build pipeline.

---

## GRO-391: Navigation Simplification — 4 Member Items

**Priority:** P1 — small change, high impact
**Phase:** 2
**Depends on:** CSS Refresh (visual consistency)

### Scope
Update `templates/components/nav.html` to show 4 member nav items instead of 9. Add conditional board and research sections.

### Changes

**nav.html** — replace the 9 nav links with:
```
Home        → {{ url_for('member.dashboard') }}
Vote        → {{ url_for('governance.proposals') }}
Documents   → {{ url_for('vault.index') }}     ← will become documents.index later
Community   → {{ url_for('member.directory') }} ← will become community.index later
```

Conditional sections:
```
{% if current_user.is_board %}
── Board ──
Dashboard   → {{ url_for('board.dashboard') }}
{% endif %}

{% if current_user.is_admin %}
── Research ──
Workbench   → {{ url_for('map.index') }}  ← will become research.index later
{% endif %}
```

### Acceptance
- [ ] Member sees exactly 4 nav items: Home, Vote, Documents, Community
- [ ] Board member sees 4 + Board section
- [ ] Admin sees 4 + Board + Research section
- [ ] Active state highlights correctly for each section
- [ ] Mobile nav works (sidebar toggle)

### Notes
Use temporary URLs for Documents and Community that point to existing routes. These get updated when those blueprints land.

---

## ~~GRO-392~~ SUPERSEDED — Notification Model overload

**Replaced by:** GRO-401 (BoardRequest model) + GRO-402 (Notification bulletin fields)
**Reason:** Factory review found 3 critical issues — member_id NOT NULL, N-row bulletin incompatibility, JSON metadata wrong abstraction.

---

## GRO-401: BoardRequest Model — New Table (STUBBED)

**Priority:** P2 — come back with fresh eyes
**Phase:** 4 (with Contact Widget)
**Depends on:** None

Board requests are a separate model. See GRO-401 in Linear for full spec.

---

## GRO-402: Notification Bulletin Support (STUBBED)

**Priority:** P2 — come back with fresh eyes
**Phase:** 3 (with Public Bulletin)
**Depends on:** None

Add `public`, `pinned`, `updated_at` to Notification. Open decision on bulletin creation flow. See GRO-402 in Linear for full spec.

---

## GRO-393: Public Bulletin Landing Page

**Priority:** P2
**Phase:** 3
**Depends on:** GRO-402 (bulletin fields), GRO-390 (CSS Refresh)

### Scope
Replace the current `GET /` (redirect to login) with a public bulletin page that shows board announcements, pinned items, and a login prompt.

### Changes

**`cove/public/routes.py`** — rewrite index route:
```python
@public_bp.route('/')
def index():
    pinned = Notification.query.filter_by(public=True, pinned=True).order_by(Notification.created_at.desc()).limit(5).all()
    bulletins = Notification.query.filter_by(public=True, type='bulletin').order_by(Notification.created_at.desc()).limit(10).all()
    return render_template('public/index.html', pinned=pinned, bulletins=bulletins)
```

**`templates/public/index.html`** — new template:
- No sidebar (public layout variant)
- Top bar: Cove logo + "Sign In" button (links to `/auth/login`)
- Pinned items section (if any)
- Bulletin feed (reverse chron, paginated)
- Login call-to-action: "Sign in to vote, view documents, and connect with your community"

**`templates/base_public.html`** — new base template for unauthenticated pages:
- Same `<head>` as base.html (fonts, CSS)
- No sidebar, no mobile nav toggle
- Simple top bar with logo + sign in
- Full-width content area

### Acceptance
- [ ] Anonymous visitor sees bulletin at `/`
- [ ] Pinned items appear at top
- [ ] Bulletins render with title, date, body
- [ ] "Sign In" links to `/auth/login`
- [ ] After login, user lands on `/member/dashboard`
- [ ] No sidebar or member nav visible to anonymous users

---

## GRO-394: Contact the Board Widget

**Priority:** P2
**Phase:** 4
**Depends on:** GRO-401 (BoardRequest), GRO-393 (Public Bulletin)

### Scope
Add a "Contact the Board" form to the public bulletin (anonymous mode) and member dashboard (authenticated mode). Requests create notifications visible to the board.

### Public mode (`cove/public/`)

**Form class** (`cove/public/forms.py`):
```python
class BoardRequestForm(CoveForm):
    request_type = SelectField('Request Type', choices=[('escrow', 'Request Escrow Documents'), ('question', 'General Question')])
    apn = SelectField('Property (APN)', choices=[])  # populated from parcels
    requester_name = StringField('Your Name', validators=[DataRequired()])
    requester_email = EmailField('Your Email', validators=[DataRequired(), Email()])
    escrow_company = StringField('Escrow Company')
    message = TextAreaField('Message')
```

**Route** — `POST /contact`:
- Validate form
- If escrow: APN required
- Create Notification: `type='board_request'`, `member_id=None`, `public=False`, `metadata={requester_name, requester_email, apn, escrow_company, request_type, message}`
- Flash success, redirect to `/`

**APN choices:** Query all 81 parcels, format as "25 Sea Cove Dr (7573-025-001)" for the dropdown.

### Member mode (`cove/member/`)

**Route** — `POST /member/contact-board`:
- Similar form but pre-filled with member's name, email, APN
- Create Notification: `type='board_request'`, `member_id=current_user.id`, `metadata={apn, request_type, message}`

**My Requests** — add to dashboard template:
```python
my_requests = Notification.query.filter_by(member_id=current_user.id, type='board_request').order_by(Notification.created_at.desc()).limit(5).all()
```

### Board inbox (`cove/board/`)

**Route** — `GET /board/requests`:
```python
requests = Notification.query.filter_by(type='board_request').order_by(Notification.created_at.desc()).all()
```

**Template:** Table view — date, requester (name or member link), type, APN, status (read/unread), message preview. Click to expand.

### Acceptance
- [ ] Public user can submit escrow request with APN selection
- [ ] Public user can submit general question without APN
- [ ] Escrow request requires APN selection (validation)
- [ ] Member form pre-fills name/email/APN
- [ ] Board sees all requests at `/board/requests`
- [ ] Member sees their request history on dashboard
- [ ] CSRF protection on both forms

---

## GRO-395: Documents Consolidation

**Priority:** P2
**Phase:** 5
**Depends on:** Nav Simplification

### Scope
Rename vault blueprint prefix from `/vault` to `/documents`. Add category filters. Gate uploads to board only. Add redirects from old URLs.

### Changes

**`cove/__init__.py`** — change blueprint registration:
```python
app.register_blueprint(vault_bp, url_prefix='/documents')  # was '/vault'
```

**`cove/vault/routes.py`**:
- Add category filter parameter to index: `?category=bylaws|minutes|resolutions|rules|financial`
- Add `@board_required` to upload and version routes (if not already)
- Add convenience routes: `/documents/bylaws`, `/documents/minutes` → filtered index

**Add 301 redirects:**
```python
@app.route('/vault/')
@app.route('/vault/<path:path>')
def vault_redirect(path=''):
    return redirect(url_for('vault.index') if not path else f'/documents/{path}', code=301)
```

**Update nav.html** — Documents link points to `/documents/`

### Acceptance
- [ ] `/documents/` shows all documents with category filters
- [ ] `/vault/` redirects to `/documents/` (301)
- [ ] Upload restricted to board role
- [ ] Member can browse, search, download — not upload
- [ ] Category filter works

---

## GRO-396: Community Map-Directory

**Priority:** P2 — the signature UX change
**Phase:** 6
**Depends on:** Nav Simplification, CSS Refresh

### Scope
New `community_bp` blueprint. Fixed community map with clickable lot cards and slide-out address book directory panel.

### New files

**`cove/community/__init__.py`:**
```python
from flask import Blueprint
community_bp = Blueprint('community', __name__, template_folder='templates')
from cove.community import routes
```

**`cove/community/routes.py`:**
```python
@community_bp.route('/')
@login_required
def index():
    return render_template('community/index.html')

@community_bp.route('/lot/<apn>')
@login_required
def lot_profile(apn):
    parcel = Parcel.query.filter_by(apn=apn).first_or_404()
    member = Member.query.filter_by(apn=parcel.apn).first()
    profile = ParcelProfile.query.filter_by(apn=parcel.apn).first()
    return render_template('community/lot.html', parcel=parcel, member=member, profile=profile)

@community_bp.route('/api/geojson')
@login_required
def community_geojson():
    # Simplified GeoJSON — lot polygons with basic member data only
    # No research fields, no temporal data, no tags
    parcels = Parcel.query.all()
    features = []
    for p in parcels:
        member = Member.query.filter_by(parcel_id=p.id).first()
        features.append({
            "type": "Feature",
            "properties": {
                "apn": p.apn,
                "address": p.address,
                "lot_number": p.lot_number,
                "resident_name": member.name if member else None,
                "lot_email": member.lot_email if member else None,
                "has_account": member is not None,
                "is_board": member.is_board if member else False,
            },
            "geometry": p.geometry  # existing GeoJSON geometry
        })
    return jsonify({"type": "FeatureCollection", "features": features})

@community_bp.route('/api/lot/<apn>')
@login_required
def lot_data(apn):
    parcel = Parcel.query.filter_by(apn=apn).first_or_404()
    member = Member.query.filter_by(apn=parcel.apn).first()
    profile = ParcelProfile.query.filter_by(apn=parcel.apn).first()
    return jsonify({
        "apn": parcel.apn,
        "address": parcel.address,
        "lot_number": parcel.lot_number,
        "resident_name": member.name if member else None,
        "lot_email": member.lot_email if member else None,
        "member_since": member.created_at.isoformat() if member else None,
        "avatar_url": profile.avatar_url if profile else None,
        "bio": profile.bio if profile else None,
        "has_account": member is not None,
    })
```

**`cove/community/templates/community/index.html`:**
- Extends base.html
- Full-bleed map container (override cove-content padding for this page)
- Leaflet map initialized at fixed zoom covering WPBCA tract
- `maxBounds` and `minZoom`/`maxZoom` constrained to tract
- Lot polygons loaded from `/community/api/geojson`
- Click handler: fetch `/community/api/lot/<apn>`, show popup card
- Directory button on right edge → toggles `cove-slide-panel`
- Slide panel: search bar + alphabetical lot list, loaded from GeoJSON data
- Click entry in directory → map `flyTo` lot centroid + open popup
- Click lot on map → scroll directory panel to entry + highlight

**Popup card HTML (generated in JS):**
```html
<div class="cove-parcel-popup">
  <p class="cove-apn">{apn}</p>
  <p class="font-semibold text-ink-700">{resident_name || 'No registered member'}</p>
  <p class="text-sm text-ink-500">{address}</p>
  <p class="text-sm"><a href="mailto:{lot_email}" class="text-cove-600">{lot_email}</a></p>
  <a href="/community/lot/{apn}" class="cove-btn cove-btn-sm cove-btn-secondary mt-2">View profile →</a>
</div>
```

**Register in `cove/__init__.py`:**
```python
from cove.community import community_bp
app.register_blueprint(community_bp, url_prefix='/community')
```

**Update nav.html** — Community link: `{{ url_for('community.index') }}`

**Add redirects:**
```python
@app.route('/member/directory')
def directory_redirect():
    return redirect(url_for('community.index'), code=301)
```

### Acceptance
- [ ] `/community/` renders full-bleed map of 81 lots
- [ ] Map is zoom/pan constrained to WPBCA tract
- [ ] Click lot → popup card with name, address, APN, email
- [ ] "View profile →" links to `/community/lot/<apn>`
- [ ] Directory panel slides out from right (same as layers panel)
- [ ] Directory entries sorted alphabetically by address
- [ ] Alphabetical tab index along panel edge
- [ ] Click directory entry → map highlights lot + opens popup
- [ ] Click map lot → directory scrolls to entry
- [ ] Search bar in directory filters entries
- [ ] `/member/directory` redirects to `/community/`
- [ ] DirectoryPreference privacy settings respected (show_name, share_bio, share_avatar)
- [ ] Null-geometry parcels appear in directory panel but not on map
- [ ] Lot profile page (`/community/lot/<apn>`) shows full community profile

### Notes (factory review fixes)
- Member FK is `Member.apn` → `Parcel.apn`, NOT `parcel_id`
- GeoJSON and lot API must check `DirectoryPreference` before exposing name/bio/avatar
- Handle `Parcel.geometry = None` gracefully in Leaflet client

### SVG Tract Map — Parcel Map Tracing (post-v1)
- Reference document: `docs/maps/LACA-Parcel-Maps-Tract-14649.pdf` (LA County Assessor official parcel map, Tract 14649)
- The SVG tract map (`tract-map.svg`) lot sizes and positions MUST match the official assessor map
- **Orientation:** rotate to landscape — the map should be wider than tall, matching how you'd view the neighborhood from Palos Verdes Dr South
- Trace lot boundaries from the assessor PDF pages (3 sheets covering the full tract)
- Each lot group retains `data-apn` attribute and `.lp` class for interactivity

### Interaction behaviors
- Click a lot → popup card appears anchored near click position
- Click empty map space, press Escape, or open directory → popup card dismisses
- Directory panel slides from right on "Directory" button click
- Click scrim (behind directory panel) → directory retreats
- Click directory entry → map highlights lot + card appears
- Click lot on map → directory scrolls to matching entry

---

## GRO-397: Board Dashboard Expansion

**Priority:** P3
**Phase:** 7
**Depends on:** Contact Widget, Documents Consolidation

### Scope
Relocate treasury, meeting management, and ARC review behind `/board` prefix. Add sub-navigation. Add request inbox. Add public/pinned toggles to bulletin composer.

### Changes

**`cove/board/routes.py`** — add routes that proxy to existing service logic:
- `/board/treasury/` → treasury overview (reuse template)
- `/board/treasury/assessments` → assessments list
- `/board/treasury/budget` → budget view
- `/board/treasury/assessments/create` → create assessment
- `/board/treasury/assessments/<id>/pay` → record payment
- `/board/meetings/` → meetings management list
- `/board/meetings/create` → create meeting
- `/board/meetings/<id>/edit` → edit meeting
- `/board/meetings/<id>/cancel` → cancel meeting
- `/board/arc/pending` → pending ARC list
- `/board/arc/<id>/review` → ARC decision
- `/board/requests` → board request inbox

**Board sub-nav component** — `templates/board/components/subnav.html`:
Tab bar: Overview | Members | Treasury | Meetings | Documents | ARC | Requests | Compliance

**Bulletin form update** — add checkboxes:
- `public` — "Publish on public bulletin (visible without login)"
- `pinned` — "Pin to top of bulletin"

**Add 301 redirects** from old `/treasury/*` and `/meetings/create` etc. to new `/board/*` paths.

### Acceptance
- [ ] All treasury routes work at `/board/treasury/`
- [ ] All meeting admin routes work at `/board/meetings/`
- [ ] ARC review works at `/board/arc/`
- [ ] Board dashboard shows sub-nav tabs
- [ ] Request inbox shows all board requests
- [ ] Bulletin can be marked public and/or pinned
- [ ] Old URLs redirect with 301
- [ ] Non-board members get 403 on all `/board/*` routes

---

## GRO-399: Research Workbench Gate

**Priority:** P3
**Phase:** 8
**Depends on:** Nav Simplification

### Scope
New `research_bp` blueprint. Relocate advanced map, archive research, and parcels deep features behind `/research` with ARC admin role gate.

### Changes

**`cove/research/__init__.py`** + **`cove/research/routes.py`**:
- Landing page at `/research/` — links to Map, Archive, Parcels sections
- Delegate to existing route logic — import and reuse existing view functions or re-register them under the new prefix
- All routes decorated with `@login_required` and `@arc_required`

**Approach:** The simplest implementation is to create the research blueprint that imports and wraps the existing map, archive, and parcels view functions. The existing blueprints can remain registered (for backwards compat redirects) but the nav only links to `/research/*`.

**Register in `cove/__init__.py`:**
```python
from cove.research import research_bp
app.register_blueprint(research_bp, url_prefix='/research')
```

### Acceptance
- [ ] `/research/` shows landing page with Map, Archive, Parcels links
- [ ] Only admin role can access `/research/*`
- [ ] Regular member gets 403 on `/research/*`
- [ ] Advanced map (layers, overlays, calibration) works at `/research/map`
- [ ] Archive (timeline, chain, catalog) works at `/research/archive`
- [ ] Parcels (tags, deep detail) works at `/research/parcels`
- [ ] Nav shows Research section only for admin

---

## GRO-398: Home Page Simplification

**Priority:** P3
**Phase:** 9
**Depends on:** Public Bulletin, Contact Widget

### Scope
Rewrite member dashboard template to bulletin format. Remove card grid. Add action items and request history.

### Template rewrite (`member/dashboard.html`)

**Layout (single column, max-w-2xl):**
1. Header: "Welcome, {name}" + assessment status badge
2. Action items card (only if items exist): open ballots, pending ARC
3. Board announcements: member notifications + public bulletins, reverse chron
4. Upcoming: next meeting, next vote closing
5. Message the Board widget (collapsible)
6. My Requests (if any exist)

### Acceptance
- [ ] Dashboard is single-column bulletin format
- [ ] No quick-link card grid
- [ ] Action items show only when they exist
- [ ] Announcements feed includes public bulletins
- [ ] Message the Board widget works
- [ ] My Requests shows request history

---

## GRO-400: Cleanup and Redirect Verification

**Priority:** P4 — final pass
**Phase:** 10
**Depends on:** All previous phases

### Scope
Remove orphaned templates, verify all redirects, run full test suite, delete unused CSS files.

### Checklist
- [ ] Delete `cove/static/src/main.css` (orphaned)
- [ ] Delete `cove/static/css/brand.css` (orphaned)
- [ ] Verify all 301 redirects: `/vault/*`, `/member/directory*`, `/treasury/*`, `/archive/*`, `/parcels/*`
- [ ] Remove old nav items from any remaining templates
- [ ] Run `pytest` — all tests pass
- [ ] Visual QA: every page, every role (public, member, board, admin)
- [ ] No dead links in any template
- [ ] No orphaned route registrations

---

## Dependency Graph (revised — 8 phases)

```
GRO-390: CSS Refresh ──────────────────────────┐
GRO-391: Nav Simplification ───────────────────┤
GRO-402: Bulletin fields (stub) ──┐            │
                                  ├→ GRO-393: Public Bulletin ──┐
GRO-401: BoardRequest (stub) ────┤                              │
                                  └→ GRO-394: Contact Widget ───┤ (includes GRO-398 Home)
GRO-395: Documents Consolidation ──────────────┤
GRO-396: Community Map-Directory ──────────────┤
GRO-397: Board Dashboard Expansion ────────────┤
GRO-399: Research Workbench Gate ──────────────┤ (includes GRO-400 Cleanup)
```

Phases 1–2 are structural. Phases 3–4 are the data/bulletin layer (stubbed models come back later). Phases 5–8 can run in parallel. Each phase owns its own cleanup.
