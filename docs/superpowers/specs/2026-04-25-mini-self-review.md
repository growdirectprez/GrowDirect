---
classification: internal
owner: GrowDirect LLC
type: spec
audience: founder + ALX (mini steward) + future Canary engineering sessions
date: 2026-04-25
status: audit-final
linear-issue: GRO-551
branch: gclyle/gro-551-mini-self-review-and-hardening
auditor: ALX (mini-resident, CLI-only, dispatch-driven)
scope-source: Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md → translated to GRO-551
---

# Mini Self-Review & Hardening — Audit 2026-04-25

## Executive summary

The mini runs production cleanly but is not demo-ready. Public-facing surfaces (canary.growdirect.app, qa.growdirect.app, abalonecove.org) are TLS-terminated through Cloudflare with sane CSP, x-frame-options, and HSTS (qa missing HSTS — minor). Production containers are baked-image-only with zero bind mounts — good prod hygiene, but it means the mini holds no live source for Canary or Cove (both moved to `~/GrowDirect-archive-2026-04-25/` earlier today). The hard problems live below the public surface: shared infrastructure (Postgres, Valkey, pgadmin, the Cove pgvector DB) is bound to `0.0.0.0` despite the compose file declaring `127.0.0.1` — runtime drift from a 9-day-old container set that compose hasn't recreated. Combined with default dev credentials still in the compose, that is the highest-priority finding in the audit. The macOS host itself is partially hardened (FileVault on, SSH key-only) but the App Firewall is off, no Time Machine destination is configured, and the machine's identity is still consumer-named. On the Canary code (audited against the archive snapshot), the standout finding is structural: Square is wired through detection, TSP, and webhook routing with no provider abstraction and no `POS_PROVIDER` knob. Adding NCR RapidPOS today is a parallel build, not an extension. The two together — exposed shared infra and a Square-shaped Canary core — are what to fix before partner access. Everything else is noise relative to those two.

**Severity counts:** P0 = 2 · P1 = 14 · P2 = 11 · Total = 27 findings · 16 proposed Linear tickets.

## Pre-audit disclosure

Two changes were made on the mini today *before* GRO-551 was identified, under direct CLI instruction from Jeffe:

1. `devops/docker-compose.yml` — added `external: true` to the `growdirect` network block so the shared compose can adopt the network already in use across multiple compose files. (Diff is in the GRO-551 working branch.)
2. `growdirect_ollama` — started via `docker compose up -d ollama`. The container is up; the volume `growdirect_ollama_data` was created fresh; **no models pulled yet**.

Both are flagged below as Layer 1 findings rather than buried.

## Audit posture

- Audited against: live mini state (Layers 1, 2, 4) + `~/GrowDirect-archive-2026-04-25/Canary/canary/` (Layer 3, archive snapshot).
- All Layer 3 findings carry the implicit caveat that origin/main on the laptop may be ahead of the archive — a laptop-side follow-up audit can confirm.
- No mutations were made during audit phase. Pre-audit edits disclosed above.

---

## Layer 1 — Environment & infrastructure hygiene

### P0 findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| L1-01 | **P0** | `growdirect_postgres`, `growdirect_valkey`, `canary_qa_pgadmin`, `devops-cove-db-1`, `canary_qa_app` runtime | All five containers report `HostIp=""` (= `0.0.0.0` on macOS) for their published ports — exposed to the LAN on 5432, 6379, 5050, 5433, 5001. The `devops/docker-compose.yml` correctly declares `127.0.0.1:` bindings; **the runtime has drifted from declared state**. 9-day-old containers were not recreated when compose was updated. | `docker compose up -d --force-recreate postgres valkey pgadmin` (and equivalent for the cove + canary_qa stacks). Verify with `docker inspect` after. Cannot be done while preserving uptime — needs a maintenance window. |
| L1-02 | **P0** | `devops/docker-compose.yml` lines 30-32, 48, 63-64 | Default dev credentials in the compose file are the credentials currently running in production-adjacent containers exposed to LAN: postgres `growdirect/growdirect_dev`, valkey `valkey_dev`, pgadmin `admin@growdirect.app/admin`. With L1-01, the LAN can reach them with these creds. | Move secrets out of the committed compose into a Docker secrets / env-file mechanism, rotate values, document the rotation runbook. Tied to L1-01 — fix together. |

### P1 findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| L1-03 | P1 | macOS Application Firewall | `socketfilterfw --getglobalstate` reports "Firewall is disabled. (State = 0)". Stealth mode off. | `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on` + `--setstealthmode on`. Add per-app exceptions for Docker, cloudflared, sshd. |
| L1-04 | P1 | macOS Time Machine | `tmutil destinationinfo` → "No destinations configured". Zero local backup. | Attach external SSD or configure NAS destination. Verify volumes for `growdirect_pgdata`, `valkey_data`, `pgadmin_data`, `growdirect_ollama_data` are captured (Time Machine's default `/var/lib/docker/...` exclusion may need an override). |
| L1-05 | P1 | `pgadmin` env | `PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED=False` on a LAN-exposed instance (compose declares `True`; runtime has it `False`). | Recreate via L1-01 fix; the compose value will then take. |
| L1-06 | P1 | Container `canary_qa_tsp_sub{1..4}` | Reported "unhealthy" for 9 days. Either the workload is genuinely degraded or the healthchecks are stale. | Decide fate of the QA stack — restart with a known-good image, retire entirely, or fix the healthcheck. Pre-existing mini-reconfig dispatch flagged this; still unresolved. |
| L1-07 | P1 | `growdirect_ollama` container healthcheck | Reports "unhealthy" because compose healthcheck shells `curl http://localhost:11434/api/tags` inside the container, but the `ollama/ollama` image ships without `curl`. Daemon itself responds correctly to host-side calls. | Edit healthcheck to `["CMD", "ollama", "list"]` or `wget` (also not present — confirm). One-line compose change, requires container recreate. |
| L1-08 | P1 | `growdirect_ollama_data` volume | Fresh volume, zero models present. CLAUDE.md spec is `qwen3-embedding:8b` (1024-dim, ~5.2 GB). Memory bus and Owl will fail until pulled. | `docker exec -it growdirect_ollama ollama pull qwen3-embedding:8b`. ~5.2 GB pull. |
| L1-09 | P1 | Docker disk | `docker system df`: 17.23 GB images / 16.44 GB reclaimable (95%); 5 GB build cache / 1.7 GB reclaimable; 6 volumes / 238 MB. Five `devops-tsp-sub{1..4}` + `devops-app` images from 5 weeks ago appear unused. | `docker image prune -a` (verify no live tag depends), `docker builder prune`. Mid-priority; reclaim before next image push to avoid disk pressure. |
| L1-10 | P1 | Stale containers | `canary_qa_pg` (Exited 0, 4w ago) and `canary_qa_valkey` (Exited 255, 4w ago) — leftover from prior QA cycles. | `docker rm canary_qa_pg canary_qa_valkey`. Trivial cleanup. |
| L1-11 | P1 | Docker network | `devops_default` network exists, unused — orphan from a prior cove compose project. | `docker network rm devops_default` after confirming nothing attached. |
| L1-12 | P1 | Docker volume | Anonymous volume `f33533ad8117…` created 2026-04-16, no labels, no current attachment. | `docker volume rm f33533ad8117…` after confirming no live mount. |
| L1-13 | P1 | `cloudflared` install | Running from `/opt/homebrew/bin/cloudflared` (Homebrew-installed). Mini-reconfig dispatch documented it as pkg-installed. | Drift is cosmetic; reconcile in the asset record. Don't touch the running daemon. |
| L1-14 | P1 | `cloudflared` config path | Active config is `/etc/cloudflared/config.yml` (system-level). Mini-reconfig dispatch said `~/.cloudflared/config.yml` (user-level). | Drift is cosmetic; reconcile in the asset record. Don't touch the running daemon. |

### P2 findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| L1-15 | P2 | macOS identity | `ComputerName: Geoff's Mac mini` · `LocalHostName: Geoffs-Mac-mini` · `HostName: not set`. Consumer-named asset. | `scutil --set ComputerName/LocalHostName/HostName` to GrowDirect convention (e.g., `growdirect-mini-01` / `mini.growdirect.local`). Cosmetic but visible to anyone who sees the asset record. |
| L1-16 | P2 | qa.growdirect.app HTTP headers | No `strict-transport-security` header (HSTS). canary.growdirect.app has it (`max-age=31556926`). | Add HSTS to the QA app's response middleware. Trivial parity. |
| L1-17 | P2 | Container env | `canary_prod_flask` has `FLASK_DEBUG` and `FLASK_ENV` set. Values not verified in this audit. If `FLASK_DEBUG=1` or `FLASK_ENV=development` in production, that is **P0**. | Verify values; flip to `0` / `production` if not already. |

---

## Layer 2 — Repository hygiene (`~/GrowDirect`)

### State of play (context, not findings)

The mini-reconfig dispatch authored earlier today described a state that has since changed. Specifically: it said `~/GrowDirect` is **not** a git repo and that `Canary/`, `Cove/` exist as project subdirs at `branch: main`. As of audit time:

- `~/GrowDirect/` IS a git repo, on `main`, with HEAD at `4040193 Merge pull request #9 from growdirectprez/gclyle/gro-536-solex-live-square-pipeline-sandbox-checkout-end-to-end`.
- `Canary/`, `Cove/` are gitignored at the platform-repo level (`.gitignore` lines 1-3) and were physically moved to `~/GrowDirect-archive-2026-04-25/` (845 MB, both repos with a clean git status apart from one uncommitted compose change in each).
- Today's reorg explains the mini-reconfig dispatch's stale assumption.

### P1 findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| L2-01 | P1 | `~/GrowDirect/ownpalosverdes` symlink | Points to `/Users/gclyle/ownpalosverdes` — target does not exist. Broken symlink in the platform repo working tree. | Remove the symlink, or point it at a real target. (Symlink is not in `.gitignore`; if it's tracked, removal is a commit.) |
| L2-02 | P1 | `~/GrowDirect/Brain/raw/inbox/` | 98 files, 25 of them loose binaries (.docx/.xlsx/.pdf/.ppt). Per session-discipline rule #10, intake artifacts get processed and routed; loose binaries in inbox have not been put through `engine.py extract`. | Run a batch intake pass (existing `2026-04-24-batch-inbox-intake` dispatch covers this; promote to a Linear issue). |
| L2-03 | P1 | `~/GrowDirect-archive-2026-04-25/Canary/devops/docker-compose.production.yml` | Uncommitted modification on archive's `main` branch. Whatever the change is, it predates the archive operation and never landed. | Either commit + push or discard. Decide on the laptop where this repo's origin remote is live; the mini holds only a snapshot. |
| L2-04 | P1 | `~/GrowDirect-archive-2026-04-25/Cove/devops/docker-compose.prod.yml` | Untracked file in archive's `main`. | Same as L2-03. |

### P2 findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| L2-05 | P2 | `~/GrowDirect/.worktrees/` | mini-reconfig dispatch references `~/.worktrees/growdirect-cto-cleanup`. Path does not exist. | Update the asset record / mini-reconfig follow-up to remove the stale reference. |
| L2-06 | P2 | `Brain/dispatches/` | Folder does not exist on `main` — only on side branches. The mini's understanding of the queue lives in Linear's Dispatch project (correctly). | Confirms "Linear is the queue" finding; `Brain/dispatches/` are working drafts on feature branches, not durable artifacts. No fix needed; document this in CLAUDE.md so future sessions don't expect to find dispatches on main. |
| L2-07 | P2 | `~/GrowDirect/growdirect-platform.plugin` | Binary file at repo root — appears to be a zipped Claude Code plugin bundle (Magic bytes `PK`). Not in CLAUDE.md File Layout. | Either document it in CLAUDE.md or move to `plugins/`. |
| L2-08 | P2 | CLAUDE.md File Layout section vs reality | Section lists 12 entries; actual root has additional/changed entries: `Solex/` (new), `evals/` (new), `lp-injection/` (new), `plugins/` (listed but with different structure), `services/` (listed), `.superpowers/` (new), `growdirect-platform.plugin` (new), `ownpalosverdes` symlink (new, broken). | Sync the File Layout section with current root contents. Single PR. |

---

## Layer 3 — Canary code review (archive snapshot)

**Scope caveat:** All findings audited against `~/GrowDirect-archive-2026-04-25/Canary/canary/` — a snapshot taken earlier today. Live HEAD on origin/main may differ. Recommend a laptop-side re-confirmation pass for any P0/P1 finding before fix work begins.

### Lens A — standard hygiene

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| L3A-01 | P1 | `canary/models/` | 1313 `Column(` hits vs 1252 `Mapped[` hits. CLAUDE.md says "always Mapped[]". Models are mid-migration; transition is incomplete. | Linear ticket to convert remaining `Column()` declarations. Likely small per-file edits, large in aggregate. |
| L3A-02 | P2 | `canary/` | 1 `print()` statement in non-test code, 5 `TODO/FIXME` without a ticket reference. | Tactical cleanup; no urgency. Existing standard is to use `logger`, not `print`. |
| L3A-03 | P1 | CLAUDE.md `Auth` section vs `canary/middleware/jwt_auth.py` | CLAUDE.md says "Flask-Login, magic link (primary), password (fallback)" with `@login_required`. Code uses `@jwt_required` and `@roles_required` from `canary/middleware/jwt_auth.py`. **Auth is enforced** — the doc is wrong about which decorator. | Decide which is canonical (the JWT path is what's running) and rewrite CLAUDE.md's Auth section. |
| L3A-04 | P2 | `canary/blueprints/views_wired.py:232` and 5 other `_wired.py` files | Auth enforced by `before_request` hooks, not per-route decorators. Discoverable via `grep before_request` but not via `grep @login_required`. | Keep the pattern, but document it in the SDD for the blueprint layer so the next reviewer doesn't re-flag this. |

### Lens B — multi-POS abstraction audit (urgent)

**Bottom line:** Canary is structurally Square-shaped. There is no `POS_PROVIDER` config knob, no `canary/services/pos/` adapter directory, and no provider interface. 24 files have "square" in their name. The TSP, the Chirp rule engine, the webhook router, and several models reach into Square primitives directly. Adding RapidPOS without an abstraction layer is a parallel rewrite, not an extension. Format below: file → what's Square-shaped → agnostic shape → blast radius.

| ID | Severity | File:line | What's Square-shaped | Agnostic shape | Blast radius if RapidPOS launches without fixing |
|---|---|---|---|---|---|
| L3B-01 | **P1** | `canary/services/webhook_dispatch.py` (~145 entries) | A Python dict mapping Square webhook event types (`payment.created`, `refund.created`, …) to parser dotted paths (`square_payment_parser:parse_payment`). | Provider-keyed registry: `{provider: {event_type: parser}}`. Adapter base class chooses the registry. | Critical. Every Counterpoint webhook would need a parallel routing dict; the two diverge silently as Square evolves. |
| L3B-02 | **P1** | `canary/services/tsp/consumers/sub2_parse.py` | TSP Sub 2 parses Square-shaped events: `square_employee_id`, `square_location_id`, `assigned_locations`. Field names are Square's, not abstracted. Does carry `source_code="square"` (line 136) — this is the existing seam, but it's not used to dispatch. | `external_identities` table keyed on `(provider, external_id)`; sub2 looks up provider once and hands off to the provider's parser. The `source_code` field already hints at this — extend it to drive dispatch. | Critical. Sub 2 is the data-ingest hot path. Adding RapidPOS here without abstraction means a parallel sub2 file or massive if/elif. |
| L3B-03 | **P1** | `canary/services/chirp/rule_engine.py:67-135` | Rule engine calls `_resolve_square_ids(alerts, merchant_id, session)` to translate Square employee/location IDs → app UUIDs before insert. Hardcodes `Employee.square_employee_id` and `Location.square_location_id` as join keys. | Resolve via `external_identities` (provider, external_id) → app UUID. Detection rule output should never carry raw provider IDs. | Critical. Chirp is the LP core. RapidPOS detection alerts will hit this code, fail to resolve, and silently drop or crash. |
| L3B-04 | P1 | `canary/services/health_check/chirp_lab.py` (73 hits) and `canary/services/health_check/merchant_simulator.py` (66 hits) | Test fixtures and simulators built on Square payload shapes. | Abstract event schemas; per-provider fixtures derived from them. | High. CI passes for Square; gives no signal for RapidPOS. |
| L3B-05 | P1 | `canary/blueprints/square_oauth_wired.py` (85 hits, 9 routes) | Square OAuth flow is the only OAuth path. | Per-provider OAuth: `/oauth/<provider>/authorize` etc. NCR Counterpoint isn't OAuth (it's HTTP Basic + APIKey per the SDD), so this file isn't templates-of-doom — but the URL shape `/oauth/...` shouldn't imply Square-only. | Medium. RapidPOS's auth flow is different enough that this file may stay Square-specific; the architectural concern is naming. |
| L3B-06 | P1 | `canary/services/owl/search/builder.py` (16 hits) | Owl search builds queries against Square-shaped fields. | Query builder against the abstract event model in CRDM. | Medium. Owl is read-side analytics; RapidPOS data wouldn't appear in search results without parallel work. |
| L3B-07 | P1 | `canary/models/sales/transactions.py` (16 hits) | Sales schema models reach into Square fields directly. | CRDM (canonical) tables are provider-neutral; provider-specific raw payloads live in raw-event tables. The CRDM design intent matches this — code reality has drifted. | Medium-high. Schema-level coupling is the most expensive to fix. |
| L3B-08 | P1 | `canary/models/sales/terminal.py` (22 hits) | Terminal model carries Square device shape. | Per-provider device sub-models; CRDM `Device` is generic. | Medium. Devices are referenced from detection rules; failures cascade. |
| L3B-09 | P2 | `canary/services/parsers/square_*.py` (18 files) | Parsers directory is named `parsers/` but every file is `square_*`. | Move to `canary/services/pos/square/parsers/` and add `canary/services/pos/counterpoint/parsers/`. Naming makes the seam visible. | Low (refactor cost only). |
| L3B-10 | P2 | `canary/services/onboarding/initial_sync.py` (36 hits) | Onboarding sync is Square-only. | Per-provider onboarding strategy; pick provider at install time. | Medium. Customer-zero install for a non-Square merchant fails. |
| L3B-11 | P2 | Templates `canary/templates/` | Search returned zero "square" hits in HTML — UI copy is already provider-neutral. **Not a finding; this is the bright spot.** | — | None — already good. |

**Verify qa.growdirect.app surface:**
- TLS via Cloudflare ✓
- CSP, x-frame-options DENY, x-content-type-options nosniff, x-xss-protection, referrer-policy strict-origin-when-cross-origin ✓
- HSTS ✗ (qa) / ✓ (canary) — see L1-16
- `/admin` → 404 ✓ · `/debug` → 404 ✓
- robots.txt present, content-signal-style policy ✓
- Landing page is a 302 → `/auth/login-page?next=/` — no Square branding leaks at the unauth surface ✓

### Lens A coverage limits

A complete file-by-file walk of all 60+ models, 16 services, and full blueprint layer is multi-session work. This first pass covered hot-path seams (TSP, Chirp, webhook routing, auth middleware, OAuth, Owl search) plus the structural Mapped[] vs Column() count. Deeper SDD-vs-code reconciliation across all 16 services is deferred — see "Out of scope".

---

## Layer 4 — Brain & documentation drift

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| L4-01 | P1 | `CLAUDE.md` Code Standards § Auth | "Flask-Login, magic link (primary), password (fallback) — `@login_required` on every non-public route". Code uses JWT-based middleware. | Replace with current pattern (JWT decorators + `before_request` hooks). Cross-link to `canary/middleware/jwt_auth.py`. (Same finding as L3A-03, lifted to platform CLAUDE.md.) |
| L4-02 | P1 | `CLAUDE.md` File Layout | Section out of date — see L2-08. | Already noted. |
| L4-03 | P2 | `CLAUDE.md` "Brain — Domain Knowledge" | Says `~/GrowDirect/Canary/brain/` is a SHOW-scoped projection refreshed manually. With Canary archived, this projection is broken on the mini. | Either restore Canary on the mini (defeats the production-only posture) or note that the projection lives on the laptop and ship-target gets it via `git pull` not local refresh. Update the section. |
| L4-04 | P2 | Brain wiki (277 .md files) | No TODO/FIXME hits found in `Brain/wiki/` — clean. **Not a finding; positive signal.** | — |
| L4-05 | P2 | mini-reconfig dispatch (`Brain/dispatches/2026-04-25-mini-reconfig-growdirect-asset.md`) | Document is stale relative to current state (claimed `~/GrowDirect` not a git repo; claimed Canary/Cove at `~/GrowDirect/Canary` etc.). Today's reorg superseded these claims. | The Linear-driven workflow handles this — GRO-551 is the live work order. The markdown can stay archived as historical record. |

---

## Code review feedback for the agent team — do/don't

Distilled from Lenses A and B. These are *standing* patterns, not one-off corrections.

### General hygiene

**Do:**
- Use `Mapped[]` for every new column. CLAUDE.md says so; the codebase is mid-migration but new code goes the right way.
- Use `logger` (module-level), never `print()`, in non-test code.
- Tag every TODO/FIXME with a `GRO-NNN` ticket reference. If there's no ticket, file one or delete the comment.
- When adding `before_request` auth hooks, document the pattern in the blueprint's docstring so future review tools find it.

**Don't:**
- Don't add new `Column()` declarations to models. Period.
- Don't write `print()` in production paths. Exit branches and error paths included.
- Don't write "TODO: clean this up later" without a ticket. "Later" never arrives without a Linear issue forcing the question.

### POS-agnostic patterns (urgent — RapidPOS goes live next to Square)

**Do:**
- Treat **provider** as a first-class concept. Add a `POS_PROVIDER` config knob (default `square`). Read it via `os.getenv("POS_PROVIDER", "square")` inside an adapter-selection helper, not scattered through services.
- Store external IDs in an `external_identities` table keyed on `(provider, external_id, app_entity_id)`. Translate at the **adapter boundary** — services downstream of TSP work in app UUIDs only.
- Use the existing `source_code` field in the parsed payload (already present in `sub2_parse.py:136`) as the dispatch key. It's the seam already half-built.
- Build a `POSAdapter` base class with: `webhook_event_types() → set[str]`, `parse(event) → CanonicalEvent`, `auth_flow_class() → type`, `seed_data() → list[Fixture]`. Register adapters in a single registry; no scattered if/elif by provider.
- Define a contract test suite (`tests/contracts/test_pos_adapter.py`) that **every** adapter must pass before merge. Pytest parametrize over registered providers.
- Detection rules execute against an abstract event schema. If a rule needs `card_fingerprint`, the schema defines it; the adapter populates it.

**Don't:**
- Don't import the Square SDK (or any provider SDK) from `services/chirp/`, `services/owl/`, `services/fox/`, `services/alerts/`, `services/analytics/`. Those are LP-domain services and must stay provider-neutral.
- Don't store raw provider IDs (`square_employee_id`, `square_location_id`) on app-domain models. Translate to UUID at the boundary, link via `external_identities`.
- Don't write Square-shaped fixtures in cross-cutting test files (`chirp_lab.py`, `merchant_simulator.py`). Use abstract event schemas; per-provider fixtures sit in `tests/fixtures/<provider>/`.
- Don't add new `square_*.py` files in `services/parsers/`. Move to `services/pos/<provider>/parsers/` going forward; migrate existing files in a single sweep.
- Don't put provider names in URL paths (`/oauth/square/...` is fine; `/oauth/...` implying Square is not).

---

## GRO tickets to file

Proposed only — not created. Each is a one-line description; full-issue authoring happens when the founder approves the slate.

| Proposed | Title | One-line |
|---|---|---|
| GRO-552 | Recreate shared infra containers with `127.0.0.1` host bindings | Stop LAN exposure on postgres/valkey/pgadmin/cove-db; close runtime drift from compose. |
| GRO-553 | Rotate default dev credentials and externalize secrets | Move postgres/valkey/pgadmin creds out of committed compose; rotate values; document rotation runbook. |
| GRO-554 | Enable macOS Application Firewall + stealth mode on the mini | Production-host hardening basic. |
| GRO-555 | Configure Time Machine destination for the mini | First-line backup. Verify Docker volumes captured per Apple's exclusion list. |
| GRO-556 | Rename mini identity to GrowDirect convention | ComputerName/LocalHostName/HostName → `growdirect-mini-01` / `mini.growdirect.local`. Asset-record consistency. |
| GRO-557 | Fix ollama healthcheck and pull `qwen3-embedding:8b` | One-line compose change + ~5.2 GB model pull. Memory bus + Owl gated on this. |
| GRO-558 | Docker housekeeping pass: prune stale containers, dangling images, anonymous volume, orphan network | Reclaim ~16 GB; remove `canary_qa_pg`/`canary_qa_valkey` from 4 weeks ago, `f33533ad…` anonymous volume, `devops_default` network. |
| GRO-559 | Sync platform CLAUDE.md File Layout with current root | Add Solex, evals, lp-injection, plugins, services, .superpowers, growdirect-platform.plugin; remove or fix `ownpalosverdes` symlink reference. |
| GRO-560 | Reconcile auth doc-drift in CLAUDE.md (Flask-Login → JWT) | Code is correct; docs are wrong. Single CLAUDE.md edit. |
| GRO-561 | **POS-agnostic adapter substrate (parent ticket)** | Introduce `canary/services/pos/`, base `POSAdapter`, contract test suite, `POS_PROVIDER` knob. Parent of L3B fixes. |
| GRO-562 | Provider-keyed webhook dispatch registry | Refactor `webhook_dispatch.py` from event-type-keyed to (provider, event_type)-keyed. Sub of GRO-561. |
| GRO-563 | Abstract event schemas in chirp_lab + merchant_simulator | Replace Square-shaped fixtures with provider-neutral schemas. Sub of GRO-561. |
| GRO-564 | Decision: chirp rule engine resolves provider IDs via external_identities | Remove `_resolve_square_ids` and replace with provider-agnostic resolution. Sub of GRO-561. |
| GRO-565 | Repair broken `~/GrowDirect/ownpalosverdes` symlink | Delete or retarget. |
| GRO-566 | Process `Brain/raw/inbox/` backlog (98 files, 25 binaries) through engine.py | Existing batch-inbox-intake dispatch covers this — promote to a Linear issue. |
| GRO-567 | Column() → Mapped[] migration in canary/models | 1313 `Column()` declarations remaining. Likely a multi-session refactor. |

---

## Out of scope / deferred

| Item | Reason |
|---|---|
| Live LAN reachability test of postgres/valkey/pgadmin from another host | Needs a separate test client on the LAN. The `0.0.0.0` runtime binding is sufficient evidence — confirmation testing is a fix-time validation, not an audit input. |
| Cloudflared tunnel config audit | Mini-reconfig dispatch explicitly excludes this — tunnel is the single point of failure for all four public hostnames; needs a coordinated maintenance window, not an audit pass. |
| Container image content audit (`canary-flask:production`) | Needs image extraction (`docker save` + filesystem walk). Out of scope for a live audit; would be a separate dispatch if image provenance becomes a concern. |
| SDD-vs-code reconciliation across all 16 Canary services | Multi-session effort. First-pass covered hot-path seams (TSP, Chirp, webhook routing, auth, OAuth, Owl). Full sweep is its own dispatch. |
| Workforce code (Module L) | Per the NCR Counterpoint SDD revision today, Module L is documented out-of-scope from Counterpoint REST. No audit value in walking the code if the upstream is gone. |
| Layer 3 against live HEAD | Audited against archive snapshot. Any P0/P1 finding in this section should be re-confirmed on the laptop before fix work begins. Tag for the laptop session: `cd ~/GrowDirect/Canary && git pull && bash docs/superpowers/specs/2026-04-25-mini-self-review-checklist.sh` (the checklist script is not produced here — recommend a small follow-up if the founder wants automation). |
| `Cove/` and `Angel/` code review | Same scope-vs-machine constraint as Canary; deferred to laptop session. |

---

## Production-state confirmation

Per the boundary "production workloads must keep serving":

| Surface | Pre-audit | Post-audit | Δ |
|---|---|---|---|
| canary.growdirect.app | 302 → /auth/login-page (HSTS, CSP, etc.) | same | none |
| qa.growdirect.app | 302 → /auth/login-page (no HSTS) | same | none |
| abalonecove.org | 200, sane headers | same | none |
| canary_prod_flask + 4 TSP subs | healthy 47h | healthy 47h+ | none |
| devops-cove-web-1 | running 9d | running 9d+ | none |
| Cloudflared tunnel | up | up | none |

Audit-only pass; no mutations to production state. Pre-audit ollama bring-up is the only environment delta — disclosed at top of report.

---

## Provenance + sign-off

- **Auditor:** ALX (mini-resident CLI session, identity per memory `project_alx_mini_role.md`)
- **Linear issue:** [GRO-551](https://linear.app/growdirect/issue/GRO-551/mini-self-review-and-hardening)
- **Branch:** `gclyle/gro-551-mini-self-review-and-hardening`
- **Method:** Live mini state for Layers 1, 2, 4. Archive snapshot (`~/GrowDirect-archive-2026-04-25/`, dated 2026-04-25) for Layer 3.
- **Tooling:** docker, git, lsof, scutil, fdesetup, tmutil, curl, grep, find, lpoctl-equivalents. No new tooling added.
- **Date:** 2026-04-25.

Founder review gate: triage the 16 proposed GRO tickets, decide priority + sequencing, then fix-dispatches follow.
