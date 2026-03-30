---
type: workorder
domain: canary
status: active
created: 2026-03-02
updated: 2026-03-19
---
# Canary LP — Tech Debt Audit Report
**Date:** March 2, 2026
**Auditor:** ALX (Chief of Staff)
**Scope:** Full codebase scan — `Canary/` directory
**Canonical entry point:** `wsgi.py` on port `:5001`
**Sprint:** 6.5 (Gates 1–4 code complete, Gate 5 runtime 5/8 pass)

---

## Executive Summary

The Canary codebase carries **significant legacy weight** from three architectural generations: the original `app.py` SQLite monolith, the `wsgi_alpha3x.py` transitional entry point, and the current `wsgi.py` PostgreSQL build. The canonical path through `wsgi.py` is clean. Everything else is dead weight that creates confusion, import collisions, and CI noise.

**Total findings: 18 items across 6 categories.**
**Estimated cleanup effort: 2–3 hours (Jeremy), then Jim QA pass.**
**Disk space recoverable: ~500MB+ (.git-old, bundled SDKs, fuse artifacts).**

---

## Category 1: DEAD ENTRY POINTS (Code Debt — CRITICAL)

### TD-001: `app.py` — Legacy SQLite monolith (965 lines)
- **What:** Original Flask app with hardcoded `sqlite3`, imports `square_client`, `chirp`, `nl_query_engine`, `polling_worker` — none of which exist in the clean build
- **Risk:** New devs or automated tools start from wrong entry point. Docker configs still reference it. Rooster test skill warns about it.
- **Impact:** 5 | **Risk:** 5 | **Effort:** 1 | **Priority Score: 50**
- **Action:** DELETE. Move to `archive/legacy/` if Jeffe wants a reference copy.

### TD-002: `wsgi_alpha3x.py` — Transitional entry point (193 lines)
- **What:** The Alpha3X slim entry that bypassed SQLite. Superseded by the March 1 `wsgi.py` rewrite.
- **Risk:** Docker compose files (`docker-compose.alpha3x.yml`, `docker-compose.localhost.yml`) and `.claude/launch.json` still point to it.
- **Impact:** 4 | **Risk:** 4 | **Effort:** 1 | **Priority Score: 40**
- **Action:** DELETE. Update all docker-compose and launch.json references to `wsgi:app`.

### TD-003: `square_client.py` — Standalone Square wrapper (1,278 lines / 55KB)
- **What:** Legacy Square API client used by `app.py`. Alpha3X uses `canary.services.square_service` and the official `squareup` SDK.
- **Risk:** Import confusion. 55KB of dead code at project root.
- **Impact:** 3 | **Risk:** 3 | **Effort:** 1 | **Priority Score: 24**
- **Action:** DELETE.

### TD-004: `chirp.py` — Monolithic detection engine (2,218 lines / 90KB)
- **What:** Original single-file Chirp engine. Alpha3X uses `canary.services.chirp_service.ChirpService` class.
- **Risk:** Largest file in the repo. Causes confusion between root `chirp.py` and `canary/blueprints/chirp.py`.
- **Impact:** 3 | **Risk:** 3 | **Effort:** 1 | **Priority Score: 24**
- **Action:** DELETE.

### TD-005: `init_db.py` — SQLite DB initializer (42 lines)
- **What:** Creates SQLite tables. wsgi.py uses Alembic + PostgreSQL.
- **Impact:** 2 | **Risk:** 2 | **Effort:** 1 | **Priority Score: 16**
- **Action:** DELETE.

---

## Category 2: DUPLICATE BLUEPRINTS (Code Debt — HIGH)

### TD-006: 7 non-wired blueprint files are dead code
- **What:** The registry imports ONLY `_wired` versions. The non-wired originals are orphans:
  - `alerts.py` (stub — all TODO, never wired)
  - `merchants.py` (stub — all TODO, never wired)
  - `locations.py` (stub — all TODO, never wired)
  - `employees.py` (stub — all TODO, never wired)
  - `webhooks.py` (superseded by `webhooks_tsp.py`)
  - `square_oauth.py` (superseded by `square_oauth_wired.py`)
  - `chirp.py` (superseded by `chirp_wired.py`)
  - `fox.py` (superseded by `fox_wired.py`)
- **Risk:** Blueprint name collisions, import confusion, misleading route maps.
- **Impact:** 4 | **Risk:** 4 | **Effort:** 2 | **Priority Score: 32**
- **Action:** DELETE all 8 non-wired files. Verify no imports reference them.

### TD-007: `parser_registry.py` — Dead abstract stub
- **What:** Empty `PosParser` ABC + empty `SquareParser`. Real parsers live in `canary/services/parsers/`. Already flagged in Jeremy's HANDOFF as "kill it."
- **Impact:** 2 | **Risk:** 2 | **Effort:** 1 | **Priority Score: 16**
- **Action:** DELETE `canary/services/parser_registry.py`.

---

## Category 3: LEGACY SQLite LAYER (Architecture Debt — HIGH)

### TD-008: `canary/database.py` — Full SQLite connection manager
- **What:** 200+ lines of `sqlite3.connect()`, `sqlite_master` queries, migration helpers. wsgi.py uses SQLAlchemy via `db_factory`.
- **Risk:** B-016 in TRIAGE (CRITICAL). Test files still import from it.
- **Impact:** 5 | **Risk:** 4 | **Effort:** 3 | **Priority Score: 27**
- **Action:** Phase 1 — mark with `# DEPRECATED: scheduled for removal Sprint 7`. Phase 2 — migrate tests to SQLAlchemy fixtures, then delete.

### TD-009: `canary/ingestion.py` — SQLite-based data ingestion
- **What:** All functions take `sqlite3.Connection`. Not referenced by wsgi.py or any wired blueprint.
- **Impact:** 3 | **Risk:** 3 | **Effort:** 2 | **Priority Score: 24**
- **Action:** DELETE after confirming zero imports from wired code.

### TD-010: `canary/fox/models.py` + `fox/services.py` + `fox/test_data.py` — SQLite Fox layer
- **What:** Raw sqlite3 case management. `fox_wired.py` uses `FoxService` which bridges to SQLAlchemy.
- **Risk:** B-016 shadow models. fox/test_fox.py imports from here.
- **Impact:** 3 | **Risk:** 3 | **Effort:** 3 | **Priority Score: 18**
- **Action:** Phase 2 with TD-008 test migration.

### TD-011: `canary/config.py` still defaults to SQLite
- **What:** `Config.DATABASE_URL` defaults to `sqlite:///data/canary.db`. `TestConfig` uses `:memory:`.
- **Risk:** Any fallback path lands on SQLite instead of failing fast.
- **Impact:** 3 | **Risk:** 4 | **Effort:** 1 | **Priority Score: 28**
- **Action:** Change default to empty string with `Config.validate()` enforcement. wsgi.py already does this.

---

## Category 4: FILESYSTEM CRUFT (Infrastructure Debt — MEDIUM)

### TD-012: `.git-old/` — 346MB dead git directory
- **What:** Orphaned `.git` copy with lockfiles (`HEAD.lock`, `HEAD.lock.y`, `index.lock.dead`, `packed-refs.lock`, `gc.pid`). Not used by current `.git/`.
- **Impact:** 2 | **Risk:** 2 | **Effort:** 1 | **Priority Score: 16**
- **Action:** DELETE entire directory.

### TD-013: `data/` — 3.3MB with 105 `.fuse_hidden*` artifacts + `canary.db`
- **What:** FUSE mount artifacts from Docker volume operations. `canary.db` is the old SQLite database. Both are gitignored but clutter the workspace.
- **Impact:** 2 | **Risk:** 1 | **Effort:** 1 | **Priority Score: 12**
- **Action:** DELETE all `.fuse_hidden*` files and `canary.db`.

### TD-014: `:memory:` and `:memory:-journal` — SQLite artifacts at project root
- **What:** Accidentally created files from a SQLite `:memory:` URL being treated as a filename.
- **Impact:** 1 | **Risk:** 1 | **Effort:** 1 | **Priority Score: 10**
- **Action:** DELETE both files.

### TD-015: `square/` — 156MB of bundled SDK repos
- **What:** Full git clones of 4 Square repos (`connect-api-examples` 104MB, `connect-api-specification` 11MB, `connect-python-sdk` 11MB, `square-python-sdk` 30MB). The actual dependency is the `squareup` pip package.
- **Impact:** 2 | **Risk:** 2 | **Effort:** 1 | **Priority Score: 16**
- **Action:** DELETE all 4 repo directories. Keep `SQUARE_ASSET_INDEX.txt` and `SQUARE_SCAN_NOTES.md` as reference.

### TD-016: Root `__pycache__/` — stale bytecode for deleted files
- **What:** Contains `.pyc` for `app`, `chirp`, `nl_query_engine`, `polling_worker`, `square_client`, `wsgi_b075`, `wsgi_alpha3x` — most of which are deleted or about to be.
- **Impact:** 1 | **Risk:** 1 | **Effort:** 1 | **Priority Score: 10**
- **Action:** DELETE entire `__pycache__/` directory.

---

## Category 5: BROKEN CONFIGS (Infrastructure Debt — HIGH)

### TD-017: `.claude/launch.json` — references deleted files
- **What:** Two configs:
  - `canary-dev` → references `wsgi_alpha3x` (dead)
  - `canary-b075` → references `wsgi_b075.py` (deleted March 1)
- **Risk:** Devs launching via Claude get errors or wrong entry point.
- **Impact:** 4 | **Risk:** 4 | **Effort:** 1 | **Priority Score: 40**
- **Action:** Replace both with single `canary` config pointing to `wsgi:app` on port 5001.

### TD-018: Docker compose files reference wrong entry points
- **What:**
  - `docker-compose.alpha3x.yml` → `gunicorn wsgi_alpha3x:app`
  - `docker-compose.localhost.yml` → `gunicorn wsgi_alpha3x:app`
  - `docker-compose.yml` → `python app.py`
- **Risk:** Docker stack fails to boot. QA deploys break.
- **Impact:** 4 | **Risk:** 5 | **Effort:** 2 | **Priority Score: 36**
- **Action:** Update all three to `gunicorn wsgi:app`. Or consolidate to one docker-compose with environment overrides.

---

## Prioritized Remediation Plan

### Phase 1: "Strip to Bone" — Immediate (2 hours Jeremy, 1 hour Jim QA)

| Order | ID | Action | Files |
|-------|-----|--------|-------|
| 1 | TD-017 | Fix `.claude/launch.json` → `wsgi:app` | 1 file |
| 2 | TD-018 | Fix all docker-compose → `wsgi:app` | 3 files |
| 3 | TD-001 | Delete `app.py` | 1 file |
| 4 | TD-002 | Delete `wsgi_alpha3x.py` | 1 file |
| 5 | TD-003 | Delete `square_client.py` | 1 file |
| 6 | TD-004 | Delete `chirp.py` (root) | 1 file |
| 7 | TD-005 | Delete `init_db.py` | 1 file |
| 8 | TD-006 | Delete 8 non-wired blueprint files | 8 files |
| 9 | TD-007 | Delete `parser_registry.py` | 1 file |
| 10 | TD-012 | Delete `.git-old/` | 1 directory (346MB) |
| 11 | TD-013 | Delete `data/.fuse_hidden*` + `canary.db` | 106 files |
| 12 | TD-014 | Delete `:memory:` artifacts | 2 files |
| 13 | TD-015 | Delete `square/` SDK repos | 4 directories (156MB) |
| 14 | TD-016 | Delete root `__pycache__/` | 1 directory |

**Total deletions:** ~25 files/dirs, ~500MB reclaimed
**Verification:** `make run` boots cleanly on `:5001`, Jim runs Gate 5 steps 5.1–5.4 + 5.8

### Phase 2: SQLite Exorcism — Sprint 7 (4–6 hours Jeremy)

| Order | ID | Action | Dependency |
|-------|-----|--------|-----------|
| 1 | TD-011 | Config defaults → PostgreSQL, fail-fast on empty | None |
| 2 | TD-008 | Migrate fox tests to SQLAlchemy fixtures | TD-011 |
| 3 | TD-009 | Delete `ingestion.py` | Verify zero wired imports |
| 4 | TD-010 | Delete `fox/models.py`, `fox/services.py`, `fox/test_data.py` | TD-008 |
| 5 | TD-008 | Delete `database.py` | All above complete |

---

## Team Routing

| Agent | Action |
|-------|--------|
| **Jeremy** | Execute Phase 1 deletions + config fixes. Phase 2 in Sprint 7. |
| **Jim** | QA Phase 1: boot test, route matrix, Gate 5 regression. |
| **Eva** | Track Phase 1 as Sprint 6.5 cleanup gate. Phase 2 in Sprint 7 backlog. |
| **Tom** | Review Phase 2 plan (SQLAlchemy test migration approach). |
| **Hawk** | Update CI pipeline to verify `wsgi:app` is the only entry point. |

---

## Disposition of `devops/scan/` Reports

The entire `devops/scan/` directory contains stale analysis referencing `app.py` routes. After Phase 1 deletions, these reports become misleading. **Recommendation:** Archive to `devops/scan/archive-pre-cleanup/` and regenerate post-cleanup.

---

*Report filed to: `_ALX/WorkOrders/output/ALX/TechDebt_Audit_2026-03-02.md`*
*Next action: Jeffe approval → Jeremy executes Phase 1 → Jim QA*
