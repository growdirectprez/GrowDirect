# Cove Functional Sweep — Design Spec

**Date:** 2026-03-31
**Author:** Cove builder (brainstorm with Jeffe + ALX review)
**Sprint type:** Feature-complete, sequential factory pipeline
**Items:** 6 (GRO-369 map overlays tracked separately per ALX recommendation)

---

## Goal

Make Cove functional end-to-end: seed realistic activity data across all 14 blueprints, fix the mobile layout, unify the brand system, add accessibility fundamentals, improve empty states, and clean up the login experience. Every item ships with tests through the full factory pipeline.

---

## Sequencing (ALX-approved)

| Order | Source | Work | Factory Weight |
|-------|--------|------|----------------|
| 1 | New GRO (file first) | Seed realistic activity data | Heavy (1.0) |
| 2 | GRO-382 | Accessibility base layer | Light (0.25) |
| 3 | GRO-363 | Brand system — cove-blue everywhere | Medium (0.5) |
| 4 | GRO-380 | Mobile responsive sidebar | Medium (0.5) |
| 5 | GRO-384 | Empty states | Light (0.25) |
| 6 | GRO-385 | Login UX + kill landing page | Light (0.15) |

**Critical path:** Seed → Accessibility → Brand → Responsive → Empty states → Login

**Dependencies:**
- Seed data (#1) unlocks visual QA for all subsequent items
- Accessibility (#2) goes into `base.html` before brand/responsive touch templates
- Brand sweep (#3) settles nav styling before responsive (#4) restructures it
- Empty states (#5) needs seed data to distinguish empty vs populated pages

---

## Item 1: Seed Realistic Activity Data

### Problem

81 members and 81 parcels exist but zero activity data. Only 1 admin (25SeaCoveDr). No board members, no proposals, no elections, no meetings, no treasury, no documents. Every feature page renders empty.

### Solution

Extend `scripts/seed.py` with a second phase that creates realistic governance activity after the base org/parcels/members phase completes. The script currently has no CLI argument handling — add `argparse` with an `--activity` flag that controls whether to run the activity seed (default: skip, for clean installs). Note: `seed.py` is a protected file per Cove CLAUDE.md — verify changes carefully.

### Seed Manifest

**Roles (extend existing members):**

| Member | Role | Rationale |
|--------|------|-----------|
| 25SeaCoveDr (Lot 69) | admin | Already assigned |
| 4 other Sea Cove lots | board | 5-member board per bylaws §8.2 |
| 1 Barkentine lot | inspector | Independent third party per §8.14 |
| 2 Peppertree lots | committee | ARC committee members |

**Governance — one proposal through full lifecycle:**

| Entity | State | Details |
|--------|-------|---------|
| Proposal: "2026 Annual Assessment Increase" | certified | Type: special_assessment, 50% quorum, secret ballot |
| ~40 ballots | cast | Mixed yes/no/abstain, chain-hashed, no member_id |
| ~40 ballot_envelopes | sealed | Link ballot→member, RLS-protected |
| Certification record | complete | Certified by inspector |

**Election — board election with candidates:**

| Entity | State | Details |
|--------|-------|---------|
| Election: "2026 Board Election" | certified | Type: election, plurality, secret ballot |
| 3 candidates | nominated | From eligible members (§8.2 residency) |
| ~50 election ballots + election_choices | cast | Create `Ballot` rows AND `ElectionChoice` rows (two-table join) |

**Treasury:**

| Entity | Details |
|--------|---------|
| 1 budget | FY 2026, line items for gates, roads, insurance, legal |
| 1 assessment | Annual dues, $200/lot, linked to budget |
| ~20 parcel_payments | Mix of paid/unpaid, some delinquent |

**Meetings:**

| Entity | Details |
|--------|---------|
| 1 past meeting | "January Annual Meeting" — completed, with attachment |
| 1 upcoming meeting | "March Board Meeting" — scheduled |
| 1 ARC application | In review status, from a committee member's lot |
| 1 ARC review | Decision pending |

**Vault:**

| Entity | Details |
|--------|---------|
| 2 documents | "2026 Budget" (PDF category), "Board Meeting Minutes Jan 2026" |
| 2 document_versions | One version each |

**Proceedings:**

| Entity | Details |
|--------|---------|
| 1 proceeding | "Coastal Commission CDP Review" — active |
| 3 proceeding_entries | Filed, response submitted, hearing scheduled |

**Notifications:**

| Entity | Details |
|--------|---------|
| 5 notifications | Mix of types: vote_open, meeting_scheduled, assessment_due, arc_submitted, proceeding_update |

**Other:**

| Entity | Details |
|--------|---------|
| 3 parcel_tags | "Ocean View", "Corner Lot", "Combined Lot" |
| ~10 tag_assignments | Spread across parcels |
| 5 directory_preferences | Mix of visibility settings |
| 1 parcel_profile | For Jeffe's lot (already exists — verify, don't duplicate) |

### Constraints

- Ballot table has NO member_id — ever. Envelopes link them.
- All UUIDs generated fresh (not hardcoded)
- Timestamps realistic (January meeting in January, March meeting in March)
- chain_hash on ballots computed correctly (SHA-256 chain)
- `--activity` flag: `python scripts/seed.py --activity`
- Idempotent: check if activity data exists before inserting

### Test Strategy

- Unit test: verify seed creates expected row counts per table
- Integration test: verify seeded proposal has correct state machine state
- Integration test: verify ballot/envelope separation (query ballots — no member_id)
- Smoke test: hit all 14 blueprint index routes, assert 200 and non-empty content

---

## Item 2: Accessibility Base Layer (GRO-382)

### Problem

No skip-to-content link, no visible focus indicators, no ARIA landmarks. Keyboard users must tab through 10+ sidebar nav items on every page.

### Solution

Three changes in two files, inherited by all templates:

**`templates/base.html`:**
1. Add skip-to-content link as first focusable element: `<a href="#main-content" class="cove-skip-nav">Skip to main content</a>`
2. Add `aria-label="Main navigation"` to the `<nav>` element inside `nav.html` (it already has implicit navigation role)
3. Add `id="main-content" role="main" aria-label="Page content"` to `<main>` tag
4. Add `aria-label="Sidebar"` to the `<aside>` element in `nav.html` (it already has implicit complementary role)

**`static/css/cove.css`:**
1. `.cove-skip-nav` — visually hidden, visible on focus, positioned at top of page
2. `*:focus-visible` — 2px ring in `cove-500`, 2px offset, on all interactive elements
3. Ensure skip-nav uses cove-blue tokens (not cream/teal)

### Constraints

- Skip-nav must be first focusable element in DOM order
- Focus ring must not conflict with existing `focus:ring-*` utilities in component classes
- Test with keyboard tab navigation through sidebar → main content

### Test Strategy

- Unit test: parse base.html, assert skip-nav link present with correct href
- Unit test: parse base.html, assert main element has id="main-content"
- Integration test: render any authenticated page, verify ARIA landmarks in response HTML

---

## Item 3: Brand System — Cove Blue Everywhere (GRO-363)

### Problem

Two competing color systems: cream/ink/teal (~734 occurrences across ~69 HTML files, including docs and landing concept) vs cove-blue (dominant in authenticated pages). The cream/parchment system lives in hardcoded hex values in `cove.css` and in Tailwind utility classes across templates.

### Solution

**Phase 1 — CSS component classes (cove.css):**

Replace the parchment/cream sidebar styling with cove-blue equivalents:
- `.cove-sidebar` background: `#FAF0D9` → cove-50 or white
- Sidebar border: `#C2A46E` gold → `cove-200` border
- Sidebar decorative pseudo-elements (`::before`, `::after`) — remove gold gradients, replace with clean cove-blue accent or remove entirely
- `.cove-page` background: `cream-50` → `gray-50` or `white`
- `.cove-card`, `.cove-card-header` — `cream-*` → `gray-*` or `cove-*` equivalents
- `.cove-nav-active::before` gold bar → `cove-500` bar
- All `cream-*`, `ink-*`, `bluff-*`, `gold-*` Tailwind utilities → `gray-*`, `cove-*`, `slate-*` equivalents
- Keep `rust-*` for danger/error states (maps to red, already semantic)

**Phase 2 — Delete landing page CSS:**

Remove the entire `shore-*` class block (lines 302–580 of cove.css, ~280 lines). This code serves only the landing page which is being killed in item #6.

**Phase 3 — Template sweep:**

Grep all `.html` files for `cream-`, `ink-`, `bluff-`, `gold-`, `shore-` classes. Replace with cove-blue equivalents. The mapping:

| Old Token | New Token | Usage |
|-----------|-----------|-------|
| `cream-50` | `white` or `gray-50` | Backgrounds |
| `cream-100` | `gray-100` | Subtle backgrounds |
| `cream-200` | `gray-200` or `cove-100` | Borders, dividers |
| `cream-300` | `gray-300` or `cove-200` | Borders |
| `ink-400` | `gray-400` | Muted text |
| `ink-500` | `gray-500` | Secondary text |
| `ink-600` | `gray-600` | Labels |
| `ink-700` | `gray-700` | Body text |
| `ink-900` | `gray-900` | Overlay backgrounds |
| `bluff-600` | `cove-600` or `gray-500` | Section labels |
| `gold-400` | `cove-400` | Hover accents |

**Phase 4 — Tailwind config cleanup:**

Remove `cream`, `ink`, `bluff`, `gold` color definitions from `tailwind.config.js` if they exist there. Keep only `cove-*` custom palette plus standard Tailwind colors.

**Phase 5 — Font consolidation:**

The Google Fonts link in `base.html` loads 4 font families (Archivo Black, IBM Plex Mono, Playfair Display, Source Sans 3). After killing the landing page:
- Keep Source Sans 3 (body) and IBM Plex Mono (technical/mono) — these are used in authenticated pages
- Evaluate whether Playfair Display and Archivo Black are still used after shore-* removal. If only in the sidebar brand text, migrate to Source Sans 3 or keep one heading font. Minimize font loads.

### Constraints

- ~69 HTML files, ~734 occurrences — this is mechanical but large
- Must not break any existing component class behavior
- PostCSS build must succeed after changes: `npm run build`
- Visual regression: spot-check dashboard, directory, governance, vault, map pages

### Test Strategy

- Grep-based assertion: zero remaining `cream-|ink-|bluff-|gold-|shore-` in templates after sweep
- Grep-based assertion: zero remaining `cream-|ink-|bluff-|gold-|shore-` in cove.css after sweep
- CSS build test: `npm run build` exits 0
- Smoke test: all authenticated routes return 200 with content

---

## Item 4: Mobile Responsive Sidebar (GRO-380)

### Problem

Sidebar is hardcoded `w-64` with zero responsive breakpoints. No hamburger menu, no mobile toggle. Unusable on phone viewports.

### Solution

**`templates/components/nav.html`:**
- Wrap sidebar in Alpine.js `x-data="{ sidebarOpen: false }"` (or hoist to base.html body)
- Desktop (lg+): sidebar visible as-is (`lg:block`)
- Mobile (<lg): sidebar hidden by default, shown as slide-over overlay on toggle
- Add hamburger button visible only on mobile: `<button @click="sidebarOpen = !sidebarOpen" class="lg:hidden">`
- Sidebar gets: `class="fixed inset-y-0 left-0 z-40 w-64 transform transition-transform lg:relative lg:translate-x-0" :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"`
- Scrim overlay behind sidebar on mobile: `<div x-show="sidebarOpen" @click="sidebarOpen = false" class="fixed inset-0 bg-gray-900/30 z-30 lg:hidden"></div>`

**`templates/base.html`:**
- Add mobile top bar with hamburger icon and app name, visible only `lg:hidden`
- Move `x-data` scope to body or page wrapper to share sidebar state

**`static/css/cove.css`:**
- Remove hardcoded `w-64` from `.cove-sidebar`, use Tailwind responsive utilities in template
- Add `.cove-mobile-bar` component class for the top bar
- Transition: `transition-transform duration-200 ease-in-out`

### Constraints

- Alpine.js is already loaded in base.html — no new dependencies
- Must work with the brand-swept cove-blue nav (depends on item #3)
- Close sidebar on navigation (listen for `click` on nav items)
- Close sidebar on Escape key
- Viewport test: 375px (iPhone SE), 768px (iPad), 1024px+ (desktop)

### Test Strategy

- Unit test: parse base.html, verify hamburger button exists with `lg:hidden`
- Unit test: parse nav.html, verify sidebar has responsive classes
- Integration test: render authenticated page, confirm sidebar markup includes Alpine directives
- Visual: manual check at 375px and 1024px (or preview tool if available)

---

## Item 5: Empty States (GRO-384)

### Problem

Pages with no data show minimal text like "No proposals found." with no context about what the feature does or how to use it.

### Solution

Add contextual empty states to each blueprint's index/list page. Each empty state includes:
1. A short explanation of what the feature is
2. Who can create content (member vs board)
3. A CTA button if the current user has permission to create

**Empty state component pattern** (add to templates as a reusable include or inline per page):

```html
<div class="text-center py-12">
  <h3 class="text-lg font-semibold text-gray-700 mb-2">{title}</h3>
  <p class="text-sm text-gray-500 max-w-md mx-auto mb-4">{description}</p>
  {% if can_create %}
  <a href="{create_url}" class="cove-btn cove-btn-primary">{cta_text}</a>
  {% endif %}
</div>
```

**Per-blueprint empty states:**

| Blueprint | Title | Description | CTA (if board) |
|-----------|-------|-------------|-----------------|
| Governance `/vote/` | No proposals yet | Proposals let members vote on community decisions — from budget changes to bylaw amendments. | Create Proposal |
| Elections `/vote/election/` | No elections scheduled | Board elections are held annually. Eligible members can be nominated as candidates. | Create Election |
| Vault `/vault/` | No documents uploaded | The vault stores community documents — meeting minutes, budgets, contracts — with version history. | Upload Document |
| Meetings `/meetings/` | No meetings scheduled | Board and community meetings appear here with agendas, attachments, and calendar downloads. | Schedule Meeting |
| Treasury `/treasury/` | No treasury activity | Assessments, payments, and budget tracking for the community. | Create Assessment |
| Proceedings `/proceedings/` | No active proceedings | Track regulatory and legal proceedings affecting the community — filings, responses, and hearings. | Create Proceeding |
| Parcels `/parcels/` | Loading parcel data... | (Parcels are always seeded — this state shouldn't appear. Defensive only.) | — |
| Archive `/archive/` | Archive loading... | (Knowledge chunks are seeded — defensive only.) | — |
| Notifications `/member/notifications` | No notifications | You're all caught up. Notifications appear here when there's community activity. | — |
| Directory `/member/directory` | No members found | (Defensive — 81 members always exist.) | — |

### Constraints

- Only show CTA buttons to users with the correct role (board for proposals/elections/meetings/assessments/proceedings)
- Use cove-blue tokens (after brand sweep)
- Empty state text must be factually accurate to Davis-Stirling (e.g., "eligible members" for elections means §8.2 residency requirement)

### Test Strategy

- Integration test per blueprint: render index route with empty database, verify empty state text appears
- Integration test: render with seeded data, verify empty state does NOT appear
- Role test: verify CTA button appears for board user, not for regular member

---

## Item 6: Login UX + Kill Landing Page (GRO-385)

### Problem

- Landing page (`/`) is a separate marketing-style page for an app used by 81 known households — dead weight
- Login placeholder shows "25seacove" — unclear expected format
- No explanation of how magic link authentication works

### Solution

**Kill landing page:**
- Change `public_bp` route for `/` to redirect to `/auth/login`
- Keep `/privacy` and `/terms` routes (legal requirements)
- Delete `cove/public/templates/public/landing.html`
- Delete shore-* CSS classes (done in item #3)

**Login template (`auth/login.html`):**
- Placeholder: `your-lot@abalonecove.org` (clear format hint)
- Add helper text below email field: "Enter your lot email address. We'll send a secure link to sign in — no password needed."
- Add small "Or sign in with password" toggle that reveals the password field (currently both fields always visible)
- Verify privacy/terms links already exist in login template (they do — lines 50-53); enhance if needed rather than duplicate
- Add community name/branding to the login page so it doesn't feel generic

**Public routes (`cove/public/routes.py`):**
- `landing()` → `return redirect(url_for("auth.login"))`
- Import `redirect` and `url_for`

### Constraints

- Privacy and terms must remain accessible without authentication
- Login page must work as the first thing a new member sees
- Magic link flow must still function (itsdangerous token, email via MailHog in dev)
- The redirect must be a 302, not a 301 (in case we ever want a landing page back)

### Test Strategy

- Integration test: GET `/` returns 302 redirect to `/auth/login`
- Integration test: GET `/auth/login` returns 200, response contains placeholder text "your-lot@abalonecove.org"
- Integration test: GET `/privacy` still returns 200
- Integration test: GET `/terms` still returns 200
- Unit test: verify landing.html template file does not exist

---

## Linear Hygiene

| Action | Details |
|--------|---------|
| File new GRO issue | Seed data — title: "Seed realistic activity data across all 14 blueprints" |
| Close GRO-381 | Status: Won't Do. Note: "Landing page killed — `/` redirects to login. See GRO-385." |
| Update GRO-385 | Add scope note: "Also includes killing landing page (redirect to login)" |
| Keep GRO-369 separate | Already In Progress, not part of this sprint |

---

## Out of Scope

- Full WCAG 2.1 AA audit (GRO-382 scoped to base layer only)
- Directory pagination (GRO-383 — separate issue)
- Map overlay rebuild (GRO-369 — tracked separately)
- Blockchain vote certification (GRO-342 — future)
- Test database seed fixtures (test suite creates its own via conftest.py)
