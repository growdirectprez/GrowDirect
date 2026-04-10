# Cove — Session Memory (Syd)

Last updated: 2026-03-23

## Project
- **Product:** Cove — DAO governance platform for HOAs
- **First deployment:** WPBCA (West Portuguese Bend Community Association), Rancho Palos Verdes, CA
- **Domain:** abalonecove.org (Cloudflare)
- **Stack:** Python 3.12 / Flask / SQLAlchemy 2.0 / PostgreSQL 17 / Tailwind CSS / Alpine.js
- **Task source:** Linear (GRO-prefixed issues, Cove project)

## Team
- **Jeffe** — CEO, founder, GrowDirect Inc. Email: gclyle@gmail.com / gclyle@growdirect.io
- **Syd** — Dev agent

## Infrastructure
- **Local dev:** Docker Compose (`devops/docker-compose.yml`) — Flask on :5002, Postgres 17 on :5433, MailHog on :8026
- **Dev launcher:** `run_dev.py` (SQLite in /tmp for quick sandbox testing)
- **Seed credentials:** 25SeaCove / c@ve (Jeffe, admin/board), 30SeaCove / c@ve (Test Voter)
- **Vercel team:** team_tPcgVcQMZo0OkQOYH39lBxz5 (growdirectprezs-projects) — no projects deployed yet
- **No tunnel or production deployment configured yet**

## Completed Work

### GRO-335 — Governance Engine (In Progress on Linear)
Built 2026-03-23. Full governance pipeline:

**Files created:**
- `cove/governance/services.py` — Business logic: proposal CRUD, lifecycle state machine, vote casting with re-auth, quorum calc, result determination, audit logging
- `cove/governance/forms.py` — WTForms: ProposalForm, BallotForm (re-auth), TransitionForm
- `cove/governance/routes.py` — 9 routes replacing stubs. Decorators: board_required, voter_eligible
- `cove/governance/templates/governance/` — 7 templates (proposals list, create, detail, ballot, confirmation, results, partials)
- `migrations/versions/c3a1f9b2d4e7_enable_rls_on_ballot_envelopes.py` — RLS policies
- `tests/unit/test_governance_services.py` — 34 unit tests
- `tests/integration/test_governance_routes.py` — 11 integration tests
- `docs/blueprints/GRO-335-governance-engine.md` — Blueprint document

**Test results:** 53/53 passing (34 unit + 11 integration + 8 smoke)

**Config change:** `cove/config.py` — TestConfig now supports TEST_DATABASE_URL env var

**Known issue:** Vote tab error on Docker stack — needs rebuild after new files added.

## Key Decisions
- Secret ballot: Ballot table has NO member_id. BallotEnvelope sealed behind RLS.
- Quorum: §5.9 no quorum for secret ballot, 1/3 general, 1/2 assessments
- Abstains excluded from threshold calculation
- Re-auth (password) required to cast vote
- Audit log records WHO voted but NEVER vote content

## Open Questions / Next
- Vote tab error: likely needs `docker compose build` to pick up new services.py and forms.py
- Deployment target for production
- Tunnel for remote testing
- Need to run Alembic migration for RLS on running Postgres
