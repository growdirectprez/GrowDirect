---
date: 2026-04-10
type: wiki
tags: [cove, platform, development, flask, architecture]
sources: [docs/sdds/cove/architecture, Cove/docs/plans/2026-03-24-foundation-rebuild]
last-compiled: 2026-04-10
needs-review: 2026-05-26
---

# Cove Platform Development

Cove is a Flask-based community governance platform being built to serve WPBCA and eventually other HOAs. Server-rendered (Jinja2), PostgreSQL, Valkey for sessions/cache.

## Tech Stack

Flask 3.1, SQLAlchemy 2.0 (Mapped[] syntax), PostgreSQL 17 (with pgvector), Valkey 8, Gunicorn, Alembic migrations. Tailwind 3.x with PostCSS build. Alpine.js for interactivity, Leaflet.js for maps. Port 5002 (Flask).

## Architecture

**App factory** with 14 blueprints: public, auth, member, governance, proceeding, vault, board, treasury, parcels, meetings, election, agent, archive, map.

**28 model classes** across 16 files covering: Organization, Parcel, Member, Governance, Election, Treasury, Vault, Meetings, ARC, Audit, Proceeding, ParcelProfile, ParcelTag, Notification, Knowledge.

**Extensions:** SQLAlchemy, LoginManager, Mail, CSRF, Valkey session, Talisman (CSP/HSTS), Rate Limiter.

## Key Modules

| Module | Purpose |
|--------|---------|
| **auth** | Magic link + password login, Flask-Login sessions |
| **member** | Member directory, profiles, lot associations |
| **board** | Board of directors management |
| **governance** | CC&R management, Davis-Stirling compliance |
| **election** | Secret ballot elections (two-envelope system) |
| **treasury** | Assessment tracking, financial management |
| **parcels** | Parcel registry, APN management, mapping |
| **meetings** | Board/member meeting management |
| **vault** | Document vault (the digital archive) |
| **archive** | Historical document access |
| **map** | Parcel mapping, Leaflet integration |
| **agent** | AI agent integration |

## Current Priority: Foundation Rebuild

GRO-346. Replace 93-row BlockShopper seed data with verified 81-lot Tract 14649 registry. All APNs start with 7573. 4 streets only: Sea Cove Dr, Clipper Rd, Barkentine Rd, Packet Rd. Lot email format: `{address_num}{StreetCompact}@abalonecove.org`.

## SDDs

Full system design documents at:
- [[docs/sdds/cove/architecture|Architecture SDD]]
- [[docs/sdds/cove/member-auth|Member Auth SDD]]
- [[docs/sdds/cove/governance-engine|Governance Engine SDD]]
- [[docs/sdds/cove/secret-ballot-elections|Secret Ballot Elections SDD]]
- [[docs/sdds/cove/treasury|Treasury SDD]]
- [[docs/sdds/cove/vault|Vault SDD]]
- [[docs/sdds/cove/parcel-map-engine|Parcel Map Engine SDD]]
- [[docs/sdds/cove/meetings|Meetings SDD]]
- [[docs/sdds/cove/archive-system|Archive System SDD]]

## Related
- [[Brain/wiki/cove-governance|Governance & Operations]] — what the platform serves
- [[Brain/projects/Cove|Cove Project MOC]]
