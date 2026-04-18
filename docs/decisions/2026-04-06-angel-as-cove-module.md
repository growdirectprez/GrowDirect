# ADR: Angel as Cove Module

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

> **Date:** 2026-04-06
> **Status:** Accepted
> **Decision makers:** Jeffe (CEO), ALX (COO)
> **Supersedes:** Original Angel standalone app architecture (docs/sdds/angel/ initial drafts)

---

## Context

Angel is a real estate intelligence and lead generation platform for Compass
agent Angelique Lyle on the Palos Verdes peninsula. The initial design spec
(April 6, 2026) proposed Angel as a standalone Flask app with its own database
(`angel`), its own Docker container on port 5004, and a dblink bridge to read
Cove's parcel data.

During spec review, we identified that this architecture was wrong. Angel's
entire data model is built on the same foundation as Cove: APN-keyed parcels,
property ownership, community membership, and communication workflows. The
proposed "bridge" to Cove's data was an engineering workaround to avoid
acknowledging that Angel IS Cove with a different lens.

## Decision

**Angel is a module within Cove, following the same pattern as ARC
(Architectural Review Committee).**

Specifically:

1. **Angel tables live in the `cove` database** — `listings`, `listing_events`,
   `leads`, `market_snapshots` are Cove tables, not a separate database.

2. **Angel routes are a Cove blueprint** — `cove/angel/routes.py` registers
   as a blueprint with URL prefix, gated by an `angel` permission on the
   Role model (same pattern as `can_access_arc`).

3. **TheHillPV.com is a public-facing Cove blueprint** — a separate blueprint
   within the same Flask app that serves unauthenticated content. It reads
   from the same database, same parcel model, same listing data.

4. **Angel Agent sidecar remains a separate container** — the Claude-powered
   chatbot (port 8004) is still its own Docker container, but it connects to
   the `cove` database directly. No bridge views.

5. **No `angel` database** — eliminated entirely. No dblink. No cross-database
   queries. Parcel → Listing is a native JOIN.

6. **LP webhook feeds into Cove's leads table** — Luxury Presence's Custom
   Webhook integration (confirmed in LP dashboard) sends lead events to a
   Cove API endpoint. LP leads, Angel chatbot leads, and future Compass leads
   all converge in one table.

## Rationale

### The data model is identical

| Cove HOA | Angel CRM | Shared Infrastructure |
|----------|-----------|----------------------|
| Member directory | Contact database | People linked to parcels |
| Parcel ownership | Property pipeline | APN → owner → status |
| Board notices | Follow-up sequences | Push comms to people |
| ARC applications | Listing intake | Submissions with review workflow |
| Meeting scheduling | Showings / callbacks | Calendar + notifications |
| Dues tracking | Transaction tracking | Money tied to parcels |
| Community membership | Sphere of influence | Relationship graph |

The parcel is the atom in both cases. An HOA board member and a real estate
agent are looking at the same property through different lenses. There is no
reason for these lenses to live in different databases.

### The ARC pattern already works

ARC is not a separate app — it's a permission-gated set of Cove blueprints
(archive, map, parcels, research) that share Cove's models, database, and
infrastructure. Angel follows the same pattern: a set of blueprints (listings,
leads, market reports, Angel chat API) gated by an `angel` role, sharing the
same parcel data.

### Eliminates the bridge problem

The original design required either dblink views or a parcel_bridge HTTP
service to read Cove data from Angel. Both add latency, complexity, and
failure modes. As a Cove module, Angel queries are native JOINs:

```sql
-- Before (cross-database bridge)
SELECT l.*, cp.*
FROM angel.listings l
JOIN dblink('dbname=cove', 'SELECT apn, address, ... FROM research_parcels')
  AS cp(apn text, address text, ...) ON l.apn = cp.apn

-- After (native Cove query)
SELECT l.*, rp.*
FROM listings l
JOIN research_parcels rp ON l.apn = rp.apn
```

### Luxury Presence confirmed the integration path

LP's dashboard shows Custom Webhook as an integration option. This means LP
lead events can POST directly to a Cove API endpoint. Combined with LP's
public API for agent/office management, the full integration stack is:

- **Webhook** → LP leads → Cove `leads` table
- **API** → Agent profile sync (bio, headshot, office)
- **Dashboard** → Custom script injection (Angel chat widget)
- **Dashboard** → Lead routing rules

## Consequences

### What changes

| Component | Before | After |
|-----------|--------|-------|
| Database | `angel` (separate) | Tables in `cove` database |
| Flask app | Standalone on port 5004 | Cove blueprints (port 5002) |
| Parcel access | dblink bridge views | Native JOINs |
| Valkey | DB 3 (Angel) | DB 1 (Cove, shared) |
| Docker | `angel-flask` + `angel-agent` | `angel-agent` only (new container) |
| Models | `Angel/angel/models/` | `Cove/cove/models/` (new files) |
| Migrations | `Angel/migrations/` | `Cove/migrations/` (new revisions) |
| Import scripts | `Angel/scripts/` | `Cove/scripts/` |
| TheHillPV.com | Separate Flask app | Cove public blueprint |

### What stays the same

- Angel Agent sidecar (port 8004, separate container)
- Chat widget (JS embed, works on any domain)
- Angel knowledge base and skills (`Angel/knowledge/`, `Angel/.claude/skills/`)
- Angel CLAUDE.md (updated to reflect module architecture)
- MCP tool design (parcel_lookup, listing_search, etc.)
- Brand strategy, pitch to Angelique
- LP API integration approach

### What gets simpler

- No bridge views or cross-database queries
- No separate database to create/migrate/backup
- No separate Flask app to scaffold, configure, and deploy
- Listing → Parcel → Owner → Lead is one query path
- TheHillPV.com reads from the same DB as Cove's dashboard
- One Alembic migration chain, one test database (`cove_test`)

### What gets more complex

- Cove's database grows (4 new tables, MLS data)
- Cove's app factory registers additional blueprints
- TheHillPV.com is a public-facing blueprint within an otherwise
  authenticated app (needs careful route/auth separation)
- Cove's CLAUDE.md and Angel's CLAUDE.md both need updating

### Risks

- **Cove coupling** — Angel's development pace is now tied to Cove's
  migration chain. Mitigation: Angel tables are additive (new tables, no
  changes to existing Cove tables).
- **Public routes in an auth-gated app** — TheHillPV.com serves public
  content from Cove's Flask app. Mitigation: separate blueprint with no
  `@login_required`, clear URL prefix separation.
- **Database size** — 2,368 listing rows + raw_data JSON column adds volume.
  Mitigation: negligible compared to Cove's survey embeddings (Vector(1024)
  on thousands of rows).

---

## Port Allocation (Revised)

| Service | Port | Change |
|---------|------|--------|
| Cove Flask | 5002 | No change — Angel blueprints serve here |
| Angel Agent sidecar | 8004 | New container |
| ~~Angel Flask~~ | ~~5004~~ | Eliminated |

## Valkey Allocation (Revised)

| DB | App | Change |
|----|-----|--------|
| 1 | Cove + Angel | Angel uses Cove's DB (was DB 3) |
| ~~3~~ | ~~Angel~~ | Eliminated |

---

*Architecture Decision Record — GrowDirect Inc.*
