---
date: 2026-04-24
type: audit-report
classification: confidential
owner: GrowDirect LLC
phase: G2
scope: GrowDirect platform code (devops, services, content-engine, growdirect-platform.plugin, root)
---

# CTO-Readiness Audit — GrowDirect Platform Code

## Summary

- Files audited: 33 source files across SHOW scope (8 devops, 3 services/growdirect-mcp impl + 4 tests, 7 services/memory-bus impl + 5 tests + 4 migrations, 1 services/alx, 1 content-engine impl + 2 tests + 2 shell scripts, 1 root manifest, plus the `growdirect-platform.plugin` zip which contains 5 files)
- HIDE-scope leakage is the dominant finding: explicit references to Cove, Angel, Seacove, WPBCA, Davis-Stirling, and prior retail-LP client material appear across the engine, the seed script, the docker init, the plugin payload, and the factory manifest.
- Confidentiality headers are absent from every Python file in scope.
- No `TODO`/`FIXME`/`HACK`/`NOCOMMIT`/`pdb.set_trace`/`DEBUG=True`/AI-voice patterns were detected — the code itself is well-formed; the issues are scope-leak and confidentiality-marking.

| Severity | Count |
|---|---|
| CRITICAL | 11 |
| HIGH | 5 |
| MEDIUM | 4 |
| LOW | 2 |

## Findings by severity

### CRITICAL (11 findings)

**C1 — HIDE-scope leak: prior-retail-LP client reference in batch-intake script**
`/Users/gclyle/GrowDirect/content-engine/batch-intake.sh` lines 44–49.
The `CORPORA` array enumerates six prior-engagement reference labels (consulting clients and methodology codes from a prior retail-LP / SCM consulting engagement) as project tags for the intake pipeline. Dimension: client / personal / sensitive names. **Recommended action:** move this script out of SHOW scope (e.g., to `Brain/raw/` or a personal-ops location), or rewrite it to drive corpora from an env-var / config file kept outside the repo. Do not ship as-is.

**C2 — HIDE-scope leak: prior-retail-LP client reference echoed in script comment** Same file, line 45 (label inside the `pwc,...,2003` tag string). Same dimension and remediation as C1.

**C3 — HIDE-scope leak: Angel references in cleanup script**
`/Users/gclyle/GrowDirect/content-engine/clean-intake-notes.sh` lines 2–4. Hard-codes paths under `Brain/raw/processed/angel/`. Dimension: current adjacent-project name. **Recommended action:** delete the script (it is a one-shot cleanup artifact per session-discipline rule 10) or relocate out of SHOW scope.

**C4 — HIDE-scope leak: Cove paths in `engine.py` module docstring**
`/Users/gclyle/GrowDirect/content-engine/engine.py` lines 14–17. Usage examples reference `Cove/docs` and `Cove/docs/archive/some-file.md`. Dimension: current adjacent-project name. **Recommended action:** replace examples with a generic `<project>/docs` placeholder.

**C5 — HIDE-scope leak: Cove tag in CLI help text**
`/Users/gclyle/GrowDirect/content-engine/engine.py` line 873. `--project` help string contains "(cove, canary, etc.)". Same dimension; **recommended action:** drop the parenthetical or replace with neutral examples.

**C6 — HIDE-scope leak: Cove governance file referenced in seed script**
`/Users/gclyle/GrowDirect/services/memory-bus/scripts/seed_clean.py` lines 13, 60–64, 92–98. The `SOURCES` array hard-codes `Cove/cove/governance/wpbca-bylaws-config.json` plus globs over `docs/sdds/cove/*.md`, with explicit `cove` layer assignments. Dimension: current adjacent-project name + private HOA work (WPBCA). **Recommended action:** make sources data-driven from an external config; remove the WPBCA-specific entry.

**C7 — HIDE-scope leak: Cove layer enum in DB schema and validators**
- `/Users/gclyle/GrowDirect/devops/init-db/01-create-databases.sql` lines 18–22, 119, 124 (creates `cove` and `cove_test` databases).
- `/Users/gclyle/GrowDirect/devops/README.md` lines 90–91, 140 (documents Cove databases).
- `/Users/gclyle/GrowDirect/devops/pgadmin-servers.json` line 11 (Comment names "Canary, Cove, Angel").
- `/Users/gclyle/GrowDirect/devops/docker-compose.yml` line 17 (comment: "canary, canary_test, cove, cove_test").
- `/Users/gclyle/GrowDirect/services/memory-bus/migrations/versions/001_baseline.py` line 49 (CHECK constraint includes `'cove'`).
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/store.py` lines 21, 273 (`VALID_LAYERS` and docstring).
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/server.py` lines 91, 114 (tool docstrings list `cove` as a layer option).

Dimension: current adjacent-project name baked into platform schema. **Recommended action:** decide whether to drop the `cove` enum value from the platform memory bus contract (preferred for SHOW) or keep it but rename to a generic `app2` placeholder before partner access. Either way, scrub the docs and comments.

**C8 — HIDE-scope leak: Davis-Stirling + WPBCA payload in smoke test**
`/Users/gclyle/GrowDirect/services/memory-bus/tests/test_smoke.py` lines 23–26. Test fixture content reads "Secret ballot separation is required by Davis-Stirling Civil Code 5100" and stores it under `layer: cove`. Dimension: HOA / Foundation private work. **Recommended action:** replace fixture with a neutral content string (e.g., a Canary detection-rule sentence) and a `canary`/`shared` layer.

**C9 — HIDE-scope leak: `cove-knowledge` MCP server inside the platform plugin**
`/Users/gclyle/GrowDirect/growdirect-platform.plugin` (`.mcp.json` lines 7–13). The plugin payload registers a stdio MCP server pointed at `cove_flask` running `cove.mcp.server`. Dimension: current adjacent-project name embedded as a configured MCP. **Recommended action:** strip the `cove-knowledge` server from the plugin manifest; ship a Memory-Bus-only plugin for SHOW.

**C10 — HIDE-scope leak: WPBCA / Cove Knowledge / Angel / Seacove discussion in plugin docs**
`/Users/gclyle/GrowDirect/growdirect-platform.plugin` (`README.md` lines 14–17, 33–34; `skills/knowledge-navigator/SKILL.md` lines 29, 33–35, 39, 51; `skills/knowledge-navigator/references/architecture.md` lines 10, 36–48, 53, 60–66, 76–77). Multiple references to WPBCA legal-document tooling, Cove containers, Angel module, Seacove. Dimension: HIDE-scope project names + private-engagement domain. **Recommended action:** rewrite plugin docs to describe only the Memory Bus tier; remove the layer table rows, project rows, and tool tables that reference Cove/Angel/Seacove/WPBCA.

**C11 — HIDE-scope leak: Cove block in `factory-manifest.json`**
`/Users/gclyle/GrowDirect/factory-manifest.json` lines 65–76. Defines a `cove` app with `compliance: davis-stirling` and a `cove-quorum` domain skill referencing `cove.governance.quorum`. Dimension: HIDE-scope project + named compliance regime. **Recommended action:** remove the `cove` entry from the `apps` map for SHOW scope. (The `apps.canary` block stays.)

### HIGH (5 findings)

**H1 — Confidentiality headers missing on every Python file in SHOW scope**
All 33 `.py` files under `services/`, `content-engine/`, plus root-level scripts lack the standard:
```
# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
```
Sample paths (full list in §"Files audited"):
- `/Users/gclyle/GrowDirect/content-engine/engine.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/store.py`, `server.py`, `config.py`, `embeddings.py`, `__init__.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/growdirect_mcp/{auth,bridge,registry,tool,__init__}.py`
- `/Users/gclyle/GrowDirect/services/alx/__init__.py`
- All test files under both services and content-engine
- All Alembic migration files

Dimension: confidentiality markings missing. **Recommended action:** insert the two-line header on every file in the cleanup pass.

**H2 — Markdown without confidentiality frontmatter**
`/Users/gclyle/GrowDirect/devops/README.md` and the plugin's `README.md`, `SKILL.md`, `architecture.md` lack the required:
```yaml
---
classification: confidential
owner: GrowDirect LLC
---
```
Dimension: confidentiality markings missing. **Recommended action:** add frontmatter; resolve content first (see C10).

**H3 — Hardcoded dev passwords in committed config**
- `/Users/gclyle/GrowDirect/devops/docker-compose.yml` line 31 (`POSTGRES_PASSWORD: growdirect_dev`), line 48 (`valkey-server --requirepass valkey_dev`), line 64 (`PGADMIN_DEFAULT_PASSWORD: admin`), line 107 (`MCP_API_KEY: ${MCP_API_KEY:-growdirect-memory-dev-key}` — defaulted, not env-only).
- `/Users/gclyle/GrowDirect/devops/init-db/01-create-databases.sql` lines 46, 54 (`canary_app_dev_2026`, `canary_tsp_dev_2026`).
- `/Users/gclyle/GrowDirect/devops/README.md` line 62, 69 (documents the password).
- `/Users/gclyle/GrowDirect/services/memory-bus/migrations/env.py` line 10, `tests/conftest.py` line 5, `tests/test_store.py` line 18, `scripts/seed_clean.py` line 17 (all hardcode `growdirect:growdirect_dev` in default DSNs).

Dimension: configuration hygiene. These are dev-only credentials, but ship-state should still: (a) move secrets to env-only with no in-file default, (b) document that these dev creds are not used in any deployed environment, (c) confirm the security pass that no production DSNs have been committed to history. **Recommended action:** convert defaults to env-required, add a `.env.example`, and document the dev-only intent in `SECURITY.md`.

**H4 — Missing `.env.example` for the platform services**
Neither `services/memory-bus/` nor `services/growdirect-mcp/` ships an `.env.example` despite both reading required env vars (`DATABASE_URL`, `OLLAMA_URL`, `MCP_API_KEY`, `MCP_JWT_SECRET`, `MCP_BRIDGE_SERVERS`). Dimension: configuration hygiene. **Recommended action:** add `services/memory-bus/.env.example` and `services/growdirect-mcp/.env.example` listing every env var with safe placeholders.

**H5 — `growdirect-platform.plugin` is a binary zip in SHOW scope**
`/Users/gclyle/GrowDirect/growdirect-platform.plugin` is a committed `.zip` archive (`mode -rw-------`, 5918 bytes). Built artifacts in SHOW scope are not auditable in normal review and bypass the confidentiality-header sweep. Dimension: factory-process compliance + confidentiality markings. **Recommended action:** remove the binary from the repo; either keep the source tree under `growdirect-platform.plugin/` as a directory or build into `dist/` (gitignored). Currently the source for the plugin's contents lives nowhere in the repo — only the zip — which is a build-without-source compliance gap.

### MEDIUM (4 findings)

**M1 — Orphan / unused `services/alx/__init__.py` package**
`/Users/gclyle/GrowDirect/services/alx/__init__.py` declares the package as the "GrowDirect COO platform service" with future-looking responsibilities, but the package contains no other code, no Dockerfile, no `pyproject.toml`, and is not imported by any other SHOW-scope module. Dimension: orphan code / sloppy stubs. **Recommended action:** either delete the package or apply the thoughtful-stub five-point test (named interface, docstring, `# Future:` rationale, `NotImplementedError` with GRO ref, defensible cold-read justification). At minimum, the docstring's "future specs" wording should reference a concrete GRO issue.

**M2 — `class AuthError(Exception): pass`**
`/Users/gclyle/GrowDirect/services/growdirect-mcp/growdirect_mcp/auth.py` line 12. Idiomatic exception subclass — borderline but acceptable; flagging because the audit dimension lists `pass` as a sloppy-stub trigger. **Recommended action:** either keep as-is (idiomatic) or add a one-line docstring expansion ("Raised when MCP authentication fails: missing key, wrong key, missing JWT secret, invalid JWT.").

**M3 — Bare `pass` in three Click group definitions**
`/Users/gclyle/GrowDirect/content-engine/engine.py` lines 261, 956, 1350. These are `@click.group()` declarations and `pass` is the standard idiom. Flagging only because the audit dimension names `pass` as a trigger. **Recommended action:** keep — idiomatic Click usage.

**M4 — SDD ancestry / factory-process compliance gap**
The four SHOW-scope modules — `services/memory-bus`, `services/growdirect-mcp`, `services/alx`, `content-engine/engine.py` — are not enumerated as factory-tracked products in `factory-manifest.json` (the manifest is stage-oriented, not module-oriented). The audit dimension names this "code lacking SDD ancestry" — assess whether each module has a corresponding SDD under `docs/sdds/platform/` or `docs/sdds/alx/` and document gaps. Dimension: factory-process compliance. **Recommended action:** document the gap honestly in the cleanup report; do not attempt to close in this pass.

### LOW (2 findings)

**L1 — `print()` calls in `seed_clean.py` script**
`/Users/gclyle/GrowDirect/services/memory-bus/scripts/seed_clean.py` lines 258, 270, 281, 290, 296. These are user-facing CLI output for an operational script, not committed debug residue. The audit dimension lists "committed `print(` debug" as HIGH; these are not debug. **Recommended action:** either keep (CLI output is appropriate) or migrate to `logging` for consistency with the rest of the platform.

**L2 — `pgadmin` master password is `admin`**
`/Users/gclyle/GrowDirect/devops/docker-compose.yml` line 64 (`PGADMIN_DEFAULT_PASSWORD: admin`). Local-dev only and `pgadmin` is bound to `127.0.0.1:5050`, so blast radius is confined to localhost. Dimension: configuration hygiene. **Recommended action:** document in `SECURITY.md` that all credentials in this compose are dev-loopback-only; rotate before any non-loopback exposure.

## Findings by dimension

| Dimension | IDs | Notes |
|---|---|---|
| Client / personal / sensitive names | C1, C2, C3, C4, C5, C6, C8, C9, C10, C11 | Two prior-retail-LP client names in `batch-intake.sh`; pervasive Cove/Angel/Seacove/WPBCA leakage across plugin, seed script, docker init, factory manifest, engine docstring/help, smoke test, MCP layer enum |
| HIDE-scope schema-baked enum | C7 | `cove` value baked into Postgres CHECK + Python `VALID_LAYERS` + tool docstrings — needs rename or removal |
| Confidentiality markings missing | H1, H2 | All Python files; key markdown |
| Configuration hygiene | H3, H4, L2 | Hardcoded dev creds, missing `.env.example`, pgadmin default password |
| Factory-process compliance | H5, M4 | Plugin shipped as binary with no source; modules lack tracked SDD ancestry |
| Orphan / sloppy stubs | M1, M2, M3 | `services/alx/` has no consumers; `pass` patterns are idiomatic but trigger the dimension |
| Print/debug residue | L1 | CLI output, not debug |
| Unresolved markers | none | No `TODO`/`FIXME`/`XXX`/`HACK`/`WIP`/`NOCOMMIT`/`pdb.set_trace`/`DEBUG=True` found in SHOW scope |
| AI-voice commentary | none | No matches against the trigger list |
| Hardcoded URLs / tokens | none beyond H3 | All URLs are localhost / docker-internal |

## Judgment calls

1. **`cove` layer in the platform memory-bus contract (C7).** The memory bus is platform-level infrastructure; `cove` is currently a first-class layer in the schema, the validators, the seed script, the smoke test, and the tool docstrings. Three options for the SHOW-state branch:
   - **Drop the value entirely.** Cleanest for SHOW; requires a migration to remove the CHECK-constraint value and a code change to `VALID_LAYERS`. Risk: any extant `growdirect_memory` rows tagged `cove` would fail the constraint — needs a data-clean step.
   - **Rename `cove` to a generic `app2` placeholder.** Preserves the multi-app shape the bus was designed for without naming the second app. Cheaper migration. Slightly ugly in code.
   - **Keep as-is, redact only docs/comments.** Fast but leaks the project name to anyone who runs `\d alx_memories` or reads the source. Not recommended.
   Surface to founder for the call.

2. **`growdirect-platform.plugin` zip (H5, C9, C10).** The committed binary contains heavy Cove/WPBCA references. Two coupled questions: (a) does the plugin ship as part of SHOW at all, or is it a personal-ops artifact? (b) if it ships, should there be a Memory-Bus-only variant for partner access? If kept in SHOW scope, the source needs to live in the repo (not just the zip), the WPBCA/Cove pieces stripped, and the binary regenerated.

3. **`factory-manifest.json` `cove` block (C11).** Removing it changes platform-level behavior (no more Cove-app stage overrides). The block can stay in a `factory-manifest-private.json` if needed, but should not appear in the SHOW manifest.

4. **`services/alx/__init__.py` (M1).** It's a stub package whose docstring promises future capability. The thoughtful-stub five-point test is borderline pass — name+description is given, but there's no `NotImplementedError` with a GRO ref and no defined interface. Surface to founder: keep as a "this is the seam for future ALX coordination" stub (with cleanup) or delete entirely.

5. **Hardcoded dev DSNs (H3).** The dev creds (`growdirect_dev`, `canary_app_dev_2026`, etc.) are loopback-only and pose no production risk, but a CTO reader will pattern-match them as "credentials in source." Cleanup options range from a docstring at the top of `SECURITY.md` ("all credentials in this repo are loopback-dev-only and not used in deployed environments") through to making every default require an env override. Recommend the docstring + env-required approach.

## Files audited

### devops/ (8 files)
- `/Users/gclyle/GrowDirect/devops/README.md`
- `/Users/gclyle/GrowDirect/devops/docker-compose.yml`
- `/Users/gclyle/GrowDirect/devops/pgadmin-servers.json`
- `/Users/gclyle/GrowDirect/devops/init-db/01-create-databases.sql`
- `/Users/gclyle/GrowDirect/devops/init-db/02-create-memory-db.sql`
- `/Users/gclyle/GrowDirect/devops/git-hooks/pre-commit`
- `/Users/gclyle/GrowDirect/devops/git-hooks/install.sh`

### services/alx/ (1 file)
- `/Users/gclyle/GrowDirect/services/alx/__init__.py`

### services/growdirect-mcp/ (8 files)
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/pyproject.toml`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/growdirect_mcp/__init__.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/growdirect_mcp/auth.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/growdirect_mcp/bridge.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/growdirect_mcp/registry.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/growdirect_mcp/tool.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/tests/test_auth.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/tests/test_bridge.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/tests/test_registry.py`
- `/Users/gclyle/GrowDirect/services/growdirect-mcp/tests/test_tool.py`

### services/memory-bus/ (16 files)
- `/Users/gclyle/GrowDirect/services/memory-bus/Dockerfile`
- `/Users/gclyle/GrowDirect/services/memory-bus/pyproject.toml`
- `/Users/gclyle/GrowDirect/services/memory-bus/alembic.ini`
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/__init__.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/config.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/embeddings.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/server.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/memory_bus/store.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/migrations/env.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/migrations/versions/001_baseline.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/migrations/versions/002_drop_seed_embeddings.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/migrations/versions/003_hnsw_index.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/migrations/versions/004_session_fk.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/scripts/seed_clean.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/tests/conftest.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/tests/test_config.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/tests/test_embeddings.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/tests/test_smoke.py`
- `/Users/gclyle/GrowDirect/services/memory-bus/tests/test_store.py`

### content-engine/ (5 files)
- `/Users/gclyle/GrowDirect/content-engine/engine.py`
- `/Users/gclyle/GrowDirect/content-engine/requirements.txt`
- `/Users/gclyle/GrowDirect/content-engine/batch-intake.sh`
- `/Users/gclyle/GrowDirect/content-engine/clean-intake-notes.sh`
- `/Users/gclyle/GrowDirect/content-engine/tests/test_extract.py`
- `/Users/gclyle/GrowDirect/content-engine/tests/test_method.py`
- `/Users/gclyle/GrowDirect/content-engine/tests/__init__.py`

### growdirect-platform.plugin (zip; 5 entries)
- `/Users/gclyle/GrowDirect/growdirect-platform.plugin` (binary)
  - `.mcp.json`
  - `README.md`
  - `.claude-plugin/plugin.json`
  - `skills/knowledge-navigator/SKILL.md`
  - `skills/knowledge-navigator/references/architecture.md`

### Root-level (1 file in scope)
- `/Users/gclyle/GrowDirect/factory-manifest.json`
