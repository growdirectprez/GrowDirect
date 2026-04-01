# ADR: Cove Sitemap Redesign — Simplification and Role Separation

**Date:** 2026-04-01
**Status:** Accepted
**Author:** Jeffe (CEO) + ALX (COO)
**Context:** Ideation session in Cowork

---

## Decision

Redesign Cove's information architecture from a 9-section member nav to a 4-section member experience, with clear role separation between public visitors, members, board operators, and the ARC Historian (research) role.

## Core Thesis

Cove exists for **secure votes and community confidence**. Everything else either supports that or is noise. The platform should feel like official governance infrastructure — not a social app, not a feature maze. Impartial, on the record, transparent. If anyone gets sued, the records are already public.

## Context

The current Cove app has:
- 9 member-facing nav items (Dashboard, Directory, Governance, Vault, Meetings, Parcels, Map, Treasury, Archive)
- Duplicated document stores (Vault for uploads, Archive for historical narrative)
- Overlapping geographic features (Parcels for data, Map for visualization)
- Research tooling (parcel lineage, temporal overlays, boundary calibration) mixed into the member experience
- Feature density that feels clunky for 81 households

Jeffe is also using Cove as a research platform for APN parcel lineage and temporal land data — a distinct use case from HOA governance that needs its own space.

## New Information Architecture

### Tier 1: Public (no auth) — The Front Door

**abalonecove.org lands on the public bulletin.** No separate login page. The landing page IS the bulletin board showing board announcements, pinned items (upcoming votes, next meeting), and published certified results. This is both the entry point and the transparency layer.

A **"Contact the Board" widget** appears on this page with two modes:
- **Request Escrow Documents** — requires selecting an APN from the list of 81 lots. Name, email, escrow company.
- **Ask a General Question** — name, email, message. APN optional.

Both create a notification to the board with an audit trail. No account needed.

"Sign in to participate" prompt sits alongside the content, not blocking it.

### Tier 2: Member Experience (4 sections)

After magic link authentication, the bulletin becomes personalized and the full member experience opens.

**Home** — The official bulletin board, personalized. Board announcements (same as public, plus member-specific notifications), upcoming votes with direct links to ballots, next meeting date and agenda, assessment status. No social feed, no widgets, no engagement metrics. Just "here's what you need to know."

**Vote** — The core product. Active proposals with ballot casting, elections with candidate slate, certified results, proceedings and compliance log. Everything on the record. This is the entire point of the platform.

**Documents** — Single document store, board-published, read-only for members. Replaces both Vault and Archive from the member's perspective. Bylaws, CC&Rs, operating rules, meeting minutes, board resolutions. Categorized and searchable. The board controls what's published here.

**Community** — The map IS the directory. A fixed, zoomed-in view of the WPBCA tract showing all 81 lots. Tap a lot to see a profile card popup (name, lot email, address). A slide-out directory panel (like the existing map layers panel) provides an address-book-style alphabetical listing. Tap a name in the directory, map highlights the lot. Tap a lot, directory scrolls to match. Click through to a full community-facing profile page. Member's own profile and contact info management lives here.

The **"Message the Board" widget** appears for logged-in members — tied to their account and parcel, with request types (question, escrow, complaint). Creates a notification to the board with full member context. Members can see their own request history.

### Tier 3: Board Dashboard (role-gated)

The operational control room. Members never see this.

- Compose and pin announcements
- Create proposals and elections
- Publish and manage documents (controls what members see in Documents)
- Treasury — budget, assessments, ledger
- Member roster and verification
- ARC review queue
- Meeting scheduling and minutes
- Compliance — publish proceedings publicly
- Request inbox — filtered view of board notifications from both public and member requests

### Tier 4: ARC Historian (role-gated, Jeffe only)

Research workbench. Same database, same APN spine, completely different interface for deep exploration.

- Parcel lineage and temporal data
- Advanced map — layers, overlays, tract history
- Document provenance and chain of custody
- APN deep-dive — subdivisions, title history
- Boundary calibration tools
- Archive narratives and timelines

## Key Design Decisions

### The map is the directory
No separate Directory and Map sections. The Community page is a full-bleed map with a slide-out address book panel (same pattern as the existing map layers menu). Two entry points to the same data, spatially connected.

### One document store, board-curated
Vault and Archive merge into a single member-facing Documents section. The board decides what's published. The research layer (ARC Historian) retains the deep archive with chain of custody, provenance, and narrative — but members see a clean, categorized, searchable document library.

### Public bulletin as landing page and login page
No separate login screen. The public sees the board's communications, the login prompt sits alongside. Transparency is the default. The "Contact the Board" widget gives public visitors (realtors, prospective buyers) a way to request escrow documents or ask questions without an account.

### Board requests via notifications engine
The "Contact the Board" / "Message the Board" widget uses the existing notifications system. No new tables or workflow engine. A request is a notification with a type, optional APN reference, and a status. Board sees them in a filtered view. Escrow requests require an APN from the list of 81. General questions do not. Future expansion: board attaches documents to a response and pushes it back.

### Research separated by role, not by app
Jeffe's ARC Historian work (parcel lineage, temporal maps, boundary calibration) stays in Cove behind a role gate rather than becoming a separate application. Same APN data spine, different interface. This avoids duplicating infrastructure while keeping the member experience clean.

## What Gets Removed or Relocated

| Current | Disposition |
|---------|-------------|
| Dashboard (member) | Becomes **Home** — simplified to bulletin format |
| Directory (member) | Merged into **Community** map — slide-out address book |
| Governance | Becomes **Vote** — same core, tighter name |
| Vault | Merged into **Documents** — single store |
| Meetings (member-facing) | Upcoming meetings on **Home**; ARC applications via board; scheduling in **Board Dashboard** |
| Parcels | Simple view in **Community** map; deep data in **ARC Historian** |
| Map | Simple fixed view in **Community**; advanced layers in **ARC Historian** |
| Treasury | Moved to **Board Dashboard** |
| Archive | Member-facing docs in **Documents**; deep archive in **ARC Historian** |
| Board Dashboard | Expanded — absorbs Treasury, Meetings admin, Document publishing, Request inbox |

## Visual Direction

Separate from this ADR, a CSS refresh is in progress targeting "sharp and professional" — crisp edges, strong borders, data-dense layout, IBM Plex Mono for UI elements, warm cream/ink/teal palette. The Tailwind config and component layer have been updated but not yet rebuilt.

## Next Steps

- Scope GRO issues for each major change
- Blueprint the Community map-as-directory interaction
- Blueprint the public bulletin / login page merge
- Review Vote and Documents during blueprint (existing code is solid)
- CSS rebuild after sitemap changes land

---

*Permanent record — do not modify after creation.*
