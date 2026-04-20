---
status: draft
date: 2026-04-20
topic: CoAC Board President Demo Tenant
audience: cove builders, CoAC board sponsor (Angel), ARC librarian (Greg)
deployment-target: qa.abalonecove.org on the mini (192.168.10.102)
branch: feat/coac-hoa-qa-instance (from main)
related: [Brain/wiki/coac-bylaws-moc, Brain/wiki/coac-reactivation-framework, Brain/wiki/wpbca-third-director-recruitment, Cove/CLAUDE.md]
---

# CoAC Board President Demo Tenant — Design

## 1. Problem

The Community of Abalone Cove board has 2 of 5 director seats filled. The 2026-03-21 annual meeting failed quorum (51% of 80 lots required; not reached). Minutes from that meeting enumerated open compliance gaps: indemnification clause, dues framework, ARC procedure, quorum bylaws amendment. Until a fully-seated board certifies an election, the association cannot bind itself to corrective action. Meanwhile, §4525 disclosure packet assembly, §5200 member inspection rights, and §5300 annual budget reporting rely on paper records scattered across former directors' personal files.

This spec describes a configured instance of the Cove platform that the ARC librarian (acting with sponsor Angel, a current CoAC board member, and in consultation with two former board presidents) can demo in person to the sitting Board president. The asks of the Board president are narrow: (a) upload the 2026-03-21 minutes through the platform, which publishes them to 81 lots through multiple channels; (b) review a pre-drafted paper-ballot board-election notice; (c) let us populate the §4525 compliance dashboard with what the HOA already has.

## 2. Scope and Constraints

### In scope
- Configure the existing `dev.abalonecove.org` tenant with a curated preload (vault, directory, map, one proposal).
- Add five net-new features to the Cove codebase: President's Desk, multi-channel publish cascade, Inspector's paper-ballot tally sheet, consulted-advisor e-acknowledgement, §4525 disclosure packet builder + SD compliance checklist.
- Enforce a sensitivity filter so the President-facing surface contains zero reactivation (Article II §5), Lot H, 0 Clipper, ocean-path, or modernization-package-in-full content.

### Explicitly out of scope
- **Blueprints not registered in production mode:** `map_bp`, `parcels_bp`, `research_bp` (if present), `agent_bp`, `archive_bp`, `knowledge-mcp` container. The mini runs Cove with `COVE_DEPLOYMENT_MODE=production`, which short-circuits registration of these blueprints and the associated container services.
- Ollama / embeddings / `knowledge_chunks` retrieval — not required for the HOA community app.
- Binding digital balloting. Paper ballots remain the legal vote of record; the Inspector of Elections retains authority. The platform is a communication tool, a community directory, a proposal-as-survey creator, and a digital tally aide — no greater legal weight than a spreadsheet.
- SMS or outbound phone — the cascade is architected with a pluggable channel hook, but no SMS provider is wired in this scope (would introduce a new dependency per platform convention).
- §4525 fee collection / invoicing.
- Public Article II §5 content, coac-* Brain cards, Foundation 501(c)(3)/(c)(4) surfaces.
- Changes to the secret-ballot separation (`ballots` table never gets `member_id`; Davis-Stirling rule).

### Sensitivity filter (deny-list)
Applies to vault category filters, knowledge-module retrieval, agent responses, and all seeded documents/proposals:
- `coac-*` Brain content
- Any document/proposal tagged: `reactivation`, `article-ii-s5`, `lot-h`, `0-clipper`, `ocean-path`, `parcel-106`, `modernization-package`, `blitz`
- `seed_first_vote.py` (Lot H enforcement) — do not run for this tenant
- `seed_modernization_proposals.py` — use a curated subset (only the election-notice proposal) or a new `seed_demo_president_tenant.py`

## 3. Preload Manifest

### 3.1 Vault — operational documents only
Categories: `governing` (current/active), `reference` (sample/historical).

| Doc | Category | Source |
|---|---|---|
| 2009 Restated Declaration (CC&Rs) | governing | `/Volumes/My Disc/ProtectiveRestrictionsRestated-AsRecorded090529.pdf` |
| 2012 Amended & Restated Bylaws | governing | `Cove/docs/archive/originals/governance/WPBCA-Bylaws-2012.pdf` |
| Articles of Incorporation | governing | `/Volumes/My Disc/ArticlesOfIncorporation.pdf` |
| 2026-03-21 AGM Minutes | governing | **empty slot, awaiting President upload** |
| 2010 Sample §4525 Disclosure Package | reference | `/Volumes/My Disc/` (all 7 files bundled as one labeled exemplar) |

1929 / 1949 / 1950 predecessor recorded instruments are not loaded into vault. They remain in `Brain/wiki/` and `Cove/docs/archive/` for researcher access but are not surfaced to the President-facing UI.

### 3.2 Directory
81 lots, 93 addresses (some combined-lot memberships per Bylaws §5.2). Seeded via existing `seed.py` + `seed_members.py`. Every account is unclaimed: `password_hash IS NULL`, `last_login_at IS NULL`, `privacy_consent_at IS NULL`. Lot emails follow `{lot#}{Street}@abalonecove.org` per existing `generate_lot_email()`.

### 3.3 Parcel Map — out of scope (this release)
Map blueprint does not register in production mode. Parcels remain in the database (required for the APN → member → vote chain) but are not visually rendered. Follow-up release may add a read-only Tract 14649 overlay; not required for the Board president demo.

### 3.4 Proposals
One seeded `draft` proposal:

- **Title:** "Notice of Board Election — Paper Ballot Primary, Electronic Delivery under Civ §4040"
- **Type:** `election`
- **Status:** `draft`
- **Description:** Pre-drafted notice invoking Bylaws §5.9 (secret ballot, no quorum), §8.2 (5 directors), §8.12 (two-envelope), §8.14 (Inspector); AB 502 acclamation option; AB 2460 20% reconvened quorum as fallback.
- **Inspector of Elections field:** blank (board fills)
- **Vote method:** paper ballot primary; platform used for §4040 electronic notice delivery and non-binding member preference survey.

No other proposals seeded. No `Resolution 2026-01` (Lot H). No full modernization set.

### 3.5 Consulted Advisors
Two slots pre-created on the President's Desk for two former board presidents (names/emails supplied by Greg during tenant bring-up). Each has a pending magic-link e-acknowledgement. When each advisor completes the acknowledgement, their attestation renders publicly on the President's Desk.

## 4. Net-New Features

### 4.1 President's Desk (`/board/president`)

**Route:** `GET /board/president` on `board_bp`, role-gated to `president`.

**Role model:** Extend `cove/models/member.py` role check. Existing `is_board` / `is_admin` flags are insufficient because multiple directors can be board without being president. Two options:
- (a) Add a `president` role to the `roles` table. Assign through existing `MemberRole` association.
- (b) Add a column `organization.president_member_id` FK to `members`.
- **Recommendation:** (a) — role-based is extensible; other role-scoped desks (ARC chair, Secretary, Treasurer, Inspector) follow the same pattern.

**Template:** `cove/board/templates/board/president.html`. Uses `cove-card` components per CSS convention. Three-item checklist:
1. Upload 2026-03-21 AGM Minutes — links to `/vault/upload?category=governing&publish=true`.
2. Review Board Election Notice — links to the seeded draft proposal detail page.
3. Consulted Advisor Status — shows two advisors with pending / acknowledged state; button to resend magic-link if pending.

Below the checklist, a "Compliance Snapshot" panel links to `/vault/compliance` (see 4.5) with a rollup count of ✅ / ⚠️ / ❌ across §4525 categories.

### 4.2 Multi-Channel Publish Cascade

**Why multi-channel:** email-only notice is insufficient in 2026. §4040 permits broader electronic delivery; the platform layers channels to maximize actual receipt.

**Channels shipped in this scope:**
1. **In-app notification** — written to existing `notifications` table; appears on member dashboard.
2. **Lot-email** — sent to `{lot#}{street}@abalonecove.org`, forwarded via Cloudflare Email Routing to member's personal email.
3. **Printable door-hanger PDF** — generated on demand, printed by Greg, hand-delivered door-to-door. PDF contains a QR code that deep-links to the member's magic-link signup for their specific lot.

**Channel hook** — pluggable channel interface under `cove/notifications/channels/` with adapters `InAppChannel`, `LotEmailChannel`, `DoorHangerPDFChannel`. Adds `SMSChannel` stub that no-ops until Twilio is provisioned (separate future scope).

**Trigger contract:** `vault.services.publish_document(document, announcement_text, channels=['in_app', 'email', 'door_hanger'])`:
- Sets `Document.published_at`, `Document.publish_to_members = True` (new columns).
- Writes one `Notification` row per member per selected channel.
- Enqueues email send (dev: MailHog; prod: Cloudflare).
- Generates door-hanger PDFs for lots where `delivery_preference IN ('paper', 'both')` or where `last_login_at IS NULL`, zipped for download.
- Idempotent — re-publishing a document with an existing `published_at` produces a delta-only notice.

**Migration:** `documents.published_at` (nullable datetime), `documents.publish_to_members` (bool default false).

### 4.3 Inspector's Paper Tally Sheet

**Route:** `GET/POST /vote/paper-tally/<proposal_id>` on `governance_bp`, role-gated to `inspector`.

**Why new, alongside existing `inspector_dashboard.html`:** the existing Inspector Dashboard audits digital-ballot chain-hash + turnout for ballots cast through the platform. The paper tally sheet is for an Inspector manually counting physical ballots; it does not touch the `ballots` table.

**Form:** for each choice on the proposal, an integer input "ballots counted." Real-time auto-sum shows total ballots tallied. Validation: totals must reconcile before "Certify Result" is clickable.

**Data model:** new table `proposal_tally_certifications`:
- `id` (UUID String(36) per Cove convention)
- `proposal_id` FK → proposals
- `inspector_member_id` FK → members (must have `inspector` role)
- `per_choice_counts` JSON {choice_id: integer}
- `total_ballots` integer
- `certified_at` datetime
- `certification_pdf_path` string (generated on certify)

**Output:** "Certify Result" generates a PDF with Inspector name, date, per-choice counts, total, and a signature block. Stored in `documents` table with category = `election-certification`. Visible under a new vault view: "Election Certifications."

**Hard rule:** the paper tally sheet never writes to `ballots` or `ballot_envelopes`. DB-level: no FK or trigger connects the two. Code-level: tests assert that `ProposalTallyCertification` cannot be inserted alongside `Ballot` rows for the same proposal without explicit Inspector dual-entry mode (out of scope here).

### 4.4 Consulted Advisor E-Acknowledgement

**Routes:** `GET /advisor/acknowledge/<token>` (public magic-link landing), `POST /advisor/acknowledge/<token>` (record ack).

**Data model:** new table `advisor_acknowledgements`:
- `id` UUID String(36)
- `organization_id` FK → organizations
- `advisor_name` string
- `advisor_email` string (does not have to be a lot email)
- `advisor_role_label` string (e.g., "Former Board President, 2018–2020")
- `magic_link_token` string (itsdangerous-signed, single-use)
- `nonce` string (rotates on resend)
- `reviewed_at` datetime nullable
- `attestation_text` text (pre-filled; advisor may amend)

**Flow:**
1. President's Desk shows two pending advisors.
2. "Resend magic-link" button re-generates token + sends email.
3. Advisor clicks link → lands on review page showing the platform's primary sections (vault, directory, map, compliance dashboard) with their name pre-filled.
4. Advisor clicks "I have reviewed this platform" → `reviewed_at` recorded, attestation locked.
5. President's Desk shows "Acknowledged on [date]" with a link to the attestation.

Advisor acknowledgement is a **trust artifact, not a legal approval**. The UI copy states this explicitly.

### 4.5 §4525 Disclosure Packet Builder + SD Compliance Checklist

**Route:** `GET /vault/compliance` on `vault_bp`, accessible to `board`, `president`, `inspector`, `admin`.

**Purpose:** visible record-keeping. Davis-Stirling requires the association to maintain specific records and deliver them on demand. This dashboard makes the HOA's compliance state inspectable at a glance and assembles a deliverable packet on request.

**Checklist categories** (mapped to Civil Code references):

| Category | Civ Code | What it requires |
|---|---|---|
| Governing documents | §4525(a)(1)(A) | CC&Rs, bylaws, articles, operating rules |
| Annual budget report | §5300 | Pro-forma budget, reserve summary, collection policy, assessment/fee schedule |
| Annual policy statement | §5310 | General info on rights, procedures, contact |
| Insurance disclosures | §5300(b)(9), §5555 | Current policy summary |
| Minutes | §4950, §4955 | Annual meeting + last 12 months of board minutes |
| Reserve study | §5550, §5565, §5570 | Current reserve study + funding plan |
| ARC guidelines | §4765 | Written procedure, timelines, appeal rights |
| Collection / delinquency | §5650, §5730 | Policy + active-delinquency disclosure |
| Pending litigation / claims | §4530 | Lawsuits affecting the association |
| Inspection rights | §5200–§5240 | Member rights to access association records |

**Per-category UI state:**
- ✅ Current — most recent version is ≤ 12 months old (or ≤ required-refresh cadence per the specific code section) and linked.
- ⚠️ Stale — exists but is past refresh cadence.
- ❌ Missing — no document of this category in the vault.

Each row has an inline "Upload" CTA that routes to `/vault/upload?category=<category>&compliance=<civ-code>`.

**Generate §4525 Packet:** action button that assembles a zip of the current version of each category's document(s), plus a cover sheet noting the request date, the list of included documents, their Civ Code mapping, and gap disclosures for any ❌ items. The zip is recorded in the `documents` table as category = `disclosure-packet` with `generated_at` timestamp.

**Sample reference:** the 2010 Sample §4525 Disclosure Package is displayed adjacent to the checklist as a collapsed reference card: "what a complete 2010 packet looked like." Members hovering over each checklist row see a tooltip linking to the corresponding section of the 2010 sample.

## 4.6 Production-Mode Feature Gating

**New env var:** `COVE_DEPLOYMENT_MODE` with values `workspace` (default on dev.abalonecove.org / laptop) and `production` (on qa.abalonecove.org / mini).

**Behavior in production mode:**
- `cove/__init__.py` conditionally registers blueprints. In production: `map_bp`, `parcels_bp`, `research_bp`, `agent_bp`, `archive_bp` are NOT registered (routes 404).
- `cove_knowledge_mcp` and `cove_angel_agent` containers are not started by the mini's docker-compose variant.
- `cove/services/embedding.py` imports and `knowledge_chunks` retrieval paths are gated off. No Ollama dependency.
- Templates rendered to board/member/inspector roles do not reference routes from the gated blueprints.

**Behavior in workspace mode (dev):** all blueprints register; full platform behavior; no change from today.

**Hard rule:** a production-mode deployment must fail fast at startup if any gated blueprint is detected to be registered, or if Ollama is queried. Startup assertion runs in `create_app()`.

## 5. Data Model Summary

New columns:
- `documents.published_at` datetime nullable
- `documents.publish_to_members` bool default false
- `documents.category` enum expanded to include: `governing`, `reference`, `disclosure-packet`, `election-certification`, `compliance-annual`, `compliance-reserves`, `compliance-insurance`, `compliance-arc`, `compliance-minutes`, `compliance-collection`, `compliance-litigation`

New tables:
- `advisor_acknowledgements` (see 4.4)
- `proposal_tally_certifications` (see 4.3)

New role:
- `president` in `roles` table

New seed script:
- `Cove/scripts/seed_coac_president_demo_tenant.py`

## 6. Compliance References

Davis-Stirling Act (Civ Code): §§ 4040 (member electronic delivery), 4525 (escrow-triggered disclosure), 4530 (pending litigation), 4765 (ARC), 4950–4955 (minutes), 5100–5145 (elections and secret ballot), 5200–5240 (inspection rights), 5300 (annual budget report), 5305 (annual financial review), 5310 (annual policy statement), 5550 / 5565 / 5570 (reserves), 5650 / 5730 (delinquency and disclosure).

Corporations Code: § 7512 (quorum).

Recent amendments: AB 502 (2022, acclamation), AB 2159 (2024, electronic secret ballots), AB 2460 (2024, 20% reconvened quorum), AB 130 (2024, fine cap), SB 900 (2025, emergency utility repair).

## 7. Open Decisions (confirm during implementation, not blocking)

1. Door-hanger PDF tool — weasyprint (preferred, pure-Python) vs. wkhtmltopdf (external bin). Default to weasyprint unless the Cove image already has wkhtmltopdf.
2. Advisor acknowledgement token expiry — 30 days vs. 180 days. Default 30 with "resend" available.
3. Inspector paper tally PDF — CoAC letterhead vs. neutral Inspector-certified form. Default to neutral until the board approves a letterhead.
4. Disclosure packet format — zip with cover PDF, or single merged PDF. Default to zip (inspectors and title companies prefer individual files).
5. Who owns bringing up the two consulted-former-president records (names, emails, role labels) — Greg supplies during tenant bring-up.

## 8. Acceptance Criteria

Tenant boot:
- [ ] `seed.py` + `seed_members.py` + `seed_coac_president_demo_tenant.py` run cleanly against a fresh `cove` database.
- [ ] 81 lots exist; all accounts unclaimed.
- [ ] Vault contains exactly the 4 governing docs listed in 3.1 + the 2010 Sample Package bundle. No 1929/1949/1950 docs.
- [ ] Proposals contains exactly one draft: the Board Election Notice.
- [ ] No document, proposal, or route returns `coac-*` reactivation content for the `president` role.

President's Desk:
- [ ] Logging in as the president role lands on `/board/president`.
- [ ] Three-item checklist renders.
- [ ] Clicking item 1 routes to the minutes-upload form.
- [ ] Clicking item 2 routes to the seeded proposal detail.
- [ ] Advisor status cards render (both pending initially).

Publish cascade:
- [ ] Uploading a document with `publish_to_members=true` writes one `Notification` row per active member per enabled channel.
- [ ] MailHog receives one email per lot with a magic-link.
- [ ] Door-hanger PDF zip downloads with one page per lot.
- [ ] Re-uploading the same document does not duplicate notifications.

Inspector paper tally:
- [ ] Inspector (role-gated) can enter counts per choice on any `open` or `closed` proposal.
- [ ] Auto-sum updates live.
- [ ] "Certify Result" generates a PDF; test verifies it lands in `documents` with category `election-certification`.
- [ ] No rows are written to `ballots` or `ballot_envelopes` by the paper-tally flow.

Advisor e-ack:
- [ ] Magic-link flow works end-to-end (email → click → attest → stored).
- [ ] Each token is single-use; re-clicking after attestation shows "already acknowledged."
- [ ] Resending rotates nonce.

§4525 compliance dashboard:
- [ ] All 10 categories render with ✅/⚠️/❌ state.
- [ ] Inline upload CTA per row routes to `/vault/upload` with category pre-filled.
- [ ] "Generate §4525 Packet" produces a downloadable zip recorded in vault as `disclosure-packet`.
- [ ] Gap categories appear in the cover sheet as explicit ❌ disclosures.

Sensitivity:
- [ ] Automated test asserts no response body served to the `president` role contains any of: `Article II §5`, `reactivation`, `Lot H`, `0 Clipper`, `ocean path easement`, `Parcel 106`, `15-owner`, `trustee slate`, `blitz`.

## 9. Test Plan

**Unit tests:**
- `AdvisorAcknowledgement`, `ProposalTallyCertification` models: CRUD, uniqueness, token rotation.
- `Document.publish_to_members` / `published_at` default behavior.
- `publish_document()` idempotency.
- Role check: `member.is_president`.
- Channel interface: in-app, email, door-hanger adapters.

**Integration tests:**
- Full upload → cascade → notification delivery (MailHog assertion).
- Paper tally create → certify → PDF artifact exists.
- §4525 packet generation against a seeded vault state.
- Advisor magic-link full cycle.
- Sensitivity filter: GET every known route as president role, grep response bodies.

**Smoke tests:**
- Fresh tenant boot: seed → login as `2BarkentineRd@abalonecove.org` → President's Desk renders.
- Demo dry-run: `pytest -m demo` walks the five beats of the platform state.

## 10. Implementation Sequence

Branch: `feat/coac-hoa-qa-instance` from `main`. All work happens on this laptop; deployed to the mini via `git pull` + `docker compose build + up -d` once the branch merges (or lands on its own branch for mini-side testing).

1. Cut branch `feat/coac-hoa-qa-instance` from `main`.
2. Add `COVE_DEPLOYMENT_MODE` env handling in `cove/config.py` + conditional blueprint registration in `cove/__init__.py` (with startup assertion).
3. Alembic migration: new tables + columns + `president` role.
4. Models: `AdvisorAcknowledgement`, `ProposalTallyCertification`.
5. Role check: `member.is_president` property.
6. Vault service: `publish_document()` + channel interface + 3 adapters (in-app, lot-email, door-hanger PDF).
7. Route + template: President's Desk (`/board/president`).
8. Route + template: Paper Tally Sheet (`/vote/paper-tally/<proposal_id>`).
9. Route + template: Advisor E-Ack (`/advisor/acknowledge/<token>`).
10. Route + template: §4525 Compliance Dashboard + Packet Generator (`/vault/compliance`).
11. Seed script: `Cove/scripts/seed_coac_president_demo_tenant.py` (curated preload, no map/research/agent data).
12. Production-mode assertion tests + blueprint gate tests.
13. Copy pass: compliance category text, advisor attestation text, notice templates.
14. Laptop dev bring-up: boot locally in production mode; smoke test as Board president.
15. Deploy runbook for the mini: tag commit → `git pull` on mini → `docker compose build cove_flask` → `up -d` → run migration + new seed → restart cloudflared tunnel → verify `qa.abalonecove.org` responds 200.
16. Cutover handoff: board proposal packet (cover letter, §4525 memo, request-for-approval, demo script, printed vault index).
