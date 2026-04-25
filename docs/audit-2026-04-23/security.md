---
date: 2026-04-24
type: security-audit-report
classification: confidential
owner: GrowDirect LLC
phase: G2
scope: GrowDirect platform repo (full git history)
audited-path: /Users/gclyle/GrowDirect
branch: fix/solex-live-debug-pass
---

# CTO-Readiness Audit — GrowDirect Platform Security

## Summary

| Severity | Count |
|---|---|
| CRITICAL | 4 |
| HIGH | 6 |
| MEDIUM | 9 |
| LOW | 134 |

**Committed-secret status: YES — separate rotate-and-rewrite-history workstream required.** Four real-looking credentials are reachable from the current `HEAD` of the platform repo and from history: a Firecrawl API key + Obsidian REST API key in `.mcp.json`, a GitHub PAT in an archived timelog, and a `CANARY_ENCRYPTION_KEY` Fernet-shaped value duplicated in archived plans + an SDD. The Square sandbox token + curl-Bearer pattern from the Canary report (S-3/S-4) is also reachable from this repo's history under `docs/_archive/ip-vault/_archive/dispatches/` and `docs/_archive/ip-vault/timelogs/`.

Top 10 highest-priority findings:

1. **CRITICAL** — `.mcp.json` is tracked in `HEAD` (commit `4c0c47dbb2`) with a real Firecrawl API key (`fc-fec9...8821e`) and a real Obsidian REST API key (`75a1...2d5b`). Both are live local credentials. **`.mcp.json` is not in the repo `.gitignore`.**
2. **CRITICAL** — GitHub PAT `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` committed at `docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-25.md:383` (commit `a7790832c4`, 2026-03-30). The line in context says "rotate after demo week" — confirm whether rotation happened and whether this token still grants any access. Token is currently in `HEAD`.
3. **CRITICAL** — `CANARY_ENCRYPTION_KEY: BHDJWBeEEtNrcqqONlNbyVdLjec4vP0SymY-X5sPQic=` (Fernet-shaped) committed in **two** locations in this repo: `docs/sdds/canary/architecture.md:517` and `docs/_archive/plans/2026-03-26-growdirect-platform-and-cove-rebuild.md`. Same value flagged in the Canary audit (S-8 / S-9). Production-shaped symmetric key in plain text.
4. **CRITICAL** — Square sandbox OAuth access token `EAAAl3ns-vSWSv...wyj693Rl` committed in 6 docs under `docs/_archive/ip-vault/_archive/dispatches/` (commit `a7790832c4`, 2026-03-30). Same token as Canary S-3/S-4 — already flagged there, but reachable from this repo's history too. Sandbox is low-blast-radius but rotate to remove the pattern from partner-diligence surface.
5. **HIGH** — `services/memory-bus/Dockerfile` and `Solex/devops/Dockerfile` (final stage) run as root. No `USER` directive in either. Same class of finding as Canary HIGH #6.
6. **HIGH** — 5 `sqlalchemy.text(...)` uses in `services/memory-bus/memory_bus/store.py` (lines 293, 310, 329, 394, 587) flagged by Semgrep `avoid-sqlalchemy-text` (ERROR severity). All use f-string interpolation into the query body. Reviewed: f-strings only inject column names / table names from configuration, never user input — but the pattern needs explicit hardening + a comment per call.
7. **HIGH** — `Solex/solex/config.py` `BaseConfig` and `ProdConfig` do **not** set `SESSION_COOKIE_SECURE`. Means production deployment serves session cookies without the Secure flag unless an env-level override is added. Easy fix.
8. **HIGH** — Solex magic-link auth uses `url_for(..., _external=True)` with no allowlist on `Host` header (`Solex/solex/routes/admin_auth.py:28`, `account_auth.py:28`). If the Flask app is reachable behind a misconfigured reverse proxy, an attacker controlling the Host header can poison the magic link recipients receive. Add an `ALLOWED_HOSTS` check or set a `SERVER_NAME` config in production.
9. **MEDIUM** — `services/memory-bus/memory_bus/server.py:19` binds `host="0.0.0.0"` (Bandit B104). Acceptable for an in-network MCP server reachable on the docker-compose `growdirect` network, but the compose binding is `127.0.0.1:8003:8003` so the actual exposure is loopback-only. Document this.
10. **MEDIUM** — `Solex/solex/services/placeholder_gen.py:30` uses `hashlib.md5` (Semgrep `insecure-hash-algorithm-md5`). Confirmed non-cryptographic use (placeholder image keying); add an inline `# nosec / non-crypto` comment to silence future scanners.

---

## Tool results

### pip-audit

- `content-engine/requirements.txt`: **0 vulnerabilities** across `click 8.3.3`, `markitdown 0.1.5`, `magika 0.6.3`, `mammoth 1.11.0`, `cobble 0.1.4`, `numpy 2.4.4`, `onnxruntime 1.25.0`, `charset-normalizer 3.4.7`. Clean.
- Solex `requirements.txt` / `requirements-dev.txt` not pip-audited in this pass per scope-narrowing instruction (Solex was in spec excludes via `Cove/Angel/Seacove/ownpalosverdes`-pattern thinking, but Solex is NOT excluded — included Solex Dockerfile + Solex config in manual review and in semgrep). Re-run pip-audit on Solex requirements before merge.

### bandit

- 136 findings on `services/` + `content-engine/`.
- 6 MEDIUM (5 × B608 hardcoded SQL with f-string `text()` in `memory-bus/store.py` — see HIGH #6 above; 1 × B104 bind-all-interfaces in `memory-bus/server.py`).
- 130 LOW: 120 × B101 (test asserts), 10 × subprocess use in `content-engine/engine.py` (legitimate — engine spawns markitdown/etc to extract files).

### semgrep

10 blocking findings across 251 rules / 846 files (rulesets `p/python`, `p/flask`, `p/owasp-top-ten`, `p/jwt`).

| Severity | Count | Rule | Location |
|---|---|---|---|
| ERROR | 1 | `dockerfile.security.missing-user` | `Solex/devops/Dockerfile:31` |
| ERROR | 1 | `dockerfile.security.missing-user` | `services/memory-bus/Dockerfile:16` |
| ERROR | 5 | `python.sqlalchemy.security.audit.avoid-sqlalchemy-text` | `services/memory-bus/memory_bus/store.py:{293,310,329,394,587}` |
| WARNING | 2 | `python.flask.security.audit.flask-url-for-external-true` | `Solex/solex/routes/{account_auth.py:28,admin_auth.py:40}` |
| WARNING | 1 | `python.lang.security.insecure-hash-algorithm-md5` | `Solex/solex/services/placeholder_gen.py:30` |

No JWT findings. No OWASP Top 10 high/critical findings outside the Dockerfile + SQL ones above. Notable absence: no semgrep p/owasp-top-ten findings that aren't already covered.

### gitleaks

20 findings, full git history (364 commits, 52 MB scanned). Each requires disposition.

| ID | File | Commit | Pattern | Disposition |
|---|---|---|---|---|
| P-1 | `.mcp.json:8` (in HEAD) | `4c0c47dbb2` | `generic-api-key` / Firecrawl `fc-fec9...8821e` | **CRITICAL — rotate** in Firecrawl dashboard, move to env var, add `.mcp.json` to `.gitignore`, scrub history |
| P-2 | `.mcp.json:17` (in HEAD) | `4c0c47dbb2` | `generic-api-key` / Obsidian REST `75a1...2d5b` | **CRITICAL — rotate** in Obsidian Local REST API plugin, move to env var, scrub history |
| P-3 | `docs/sdds/canary/architecture.md:517` (in HEAD) | `50abeb7cd9` | `generic-api-key` / `CANARY_ENCRYPTION_KEY` Fernet | **CRITICAL — rotate** the Fernet (same as Canary S-8/S-9), replace literal in SDD with placeholder |
| P-4 | `Brain/wiki/growdirect-research-cannabis-retail-risk.md:241` (in HEAD) | `0de15da32b` | `generic-api-key` / `metrc_user_key": "API-KEY-ABC123"` | **False positive** — placeholder in research doc; add `.gitleaksignore` entry |
| P-5 | `docs/_archive/ip-vault/Cannabis_Retail_Risk_Dictionary_v1.0.md:234` (in HEAD) | `a7790832c4` | `generic-api-key` / same `API-KEY-ABC123` | **False positive** — placeholder; same scrub as P-4 |
| P-6 | `docs/superpowers/plans/2026-04-15-canary-account-credit-system.md:1926` (in HEAD) | `68c15af7b4` | `generic-api-key` / `wrong-key-wrong-key-32bytesXXXX` | **False positive** — negative-test fixture; add `.gitleaksignore` |
| P-7…P-12 | `docs/_archive/ip-vault/_archive/dispatches/{Jeremy_B065_Combined_MaxSession.md, Jeremy_LiveWebhook_SessionPrompt.md, Jeremy_SquareOAuth_SessionPrompt.md}` and `docs/_archive/ip-vault/_archive/workorders/WORKORDER_B067_SquareCapabilityDashboard.md` and `docs/_archive/ip-vault/_archive/dispatches/B067_SquareCapabilityDashboard_MasterDispatch.md` (all in HEAD) | `a7790832c4` | `square-access-token` / `EAAAl3ns-vSWSv...wyj693Rl` (×9) + `curl-auth-header` (×4) | **CRITICAL** — same token as Canary S-3. Revoke in Square sandbox dashboard. Tokens are reachable from this repo's HEAD AND history; consider scrub or repo-archival of `_archive/ip-vault/`. |
| P-13 | `docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-25.md:383` (in HEAD) | `a7790832c4` | `github-pat` / `ghp_2FwZ...AAX` | **CRITICAL** — verify rotation status with `gh auth token` test; if still valid, rotate at github.com/settings/tokens. Note in the file says "rotate after demo week" — track that this happened. |

### trufflehog (filesystem + git)

- **Filesystem scan: 1,798 raw findings**, of which 19 verified. Verified findings break down:
  - 18 × Anthropic verified — **all under `/Users/gclyle/GrowDirect/Canary/`** (`.env`, `.git/objects/`, and Canary's own audit output files). Out-of-scope for this report; covered by Canary's S-1.
  - 1 × SquareApp verified — `Canary/.env` `sandbox-sq0idb-SduFLmiaE43X0BeFC37Taw`. Same — Canary scope. (Solex `.env` was not flagged because it's properly gitignored and its secrets are loaded at runtime.)
  - **In platform scope (excluding Canary/Cove/Angel/Seacove/ownpalosverdes/security-tool-output/.git-objects), 0 verified findings**. 57 unverified: 50 × Postgres DSN (all `growdirect:growdirect_dev@growdirect_postgres` documented dev creds), 5 × EightxEight false-positive (a string of 8s in a Lotus Notes binary), 1 × PrivateKey (`.obsidian/plugins/obsidian-local-rest-api/data.json` — gitignored, local-only), 1 × GitHub PAT (same as gitleaks P-13).
- **Git scan: 60 findings**, 0 verified. 59 × Postgres DSN (all dev creds), 1 × GitHub PAT (same as P-13). No additional surfaces beyond gitleaks.

### trivy

- `trivy config /Users/gclyle/GrowDirect/devops` → **0 misconfigurations**. Trivy's checks bundle didn't recognize `docker-compose.yml` as a config target (compose files outside Dockerfile syntax are matched only with the Compose-specific check pack). Manual review of `devops/docker-compose.yml`:
  - `pgadmin` admin password hardcoded (`PGADMIN_DEFAULT_PASSWORD: admin`) — dev-only, acceptable.
  - `valkey` password hardcoded (`--requirepass valkey_dev`) — dev-only, acceptable; not in production compose.
  - All ports bound `127.0.0.1:*` — loopback-only. Good.
  - `MCP_API_KEY` env var has a default `growdirect-memory-dev-key` — dev fallback, fine. Production must override.

### Container/Dockerfile review (manual)

- `services/memory-bus/Dockerfile`: no `USER` — runs as root. **HIGH #5.**
- `Solex/devops/Dockerfile` final stage: no `USER` — runs as root. **HIGH #5.**

---

## Manual OWASP Top 10 review

### A01: Broken Access Control

- `services/memory-bus`: every `@mcp.tool()` calls `validate_api_key(api_key)` first. Auth gate consistent across the surface. ✅
- `services/growdirect-mcp`: same pattern (provides the `validate_api_key` helper). ✅
- `content-engine`: CLI tool; no HTTP surface. N/A.
- `Solex`: magic-link admin + customer auth in `Solex/solex/routes/{admin,account}_auth.py`. Per-blueprint review needed but not in scope of this audit pass — flag for Solex-side audit.

**Severity:** LOW (platform). Solex auth surface deferred.

### A02: Cryptographic Failures

- `CANARY_ENCRYPTION_KEY` Fernet duplicated in docs (P-3). HIGH severity but already covered above.
- No password storage in platform code (Solex uses magic-link only; memory-bus uses static API key).
- Bandit + Semgrep flagged 1 × MD5 use in `Solex/solex/services/placeholder_gen.py` — non-crypto, acceptable with a marker comment.

**Severity:** HIGH (encryption key in docs). Otherwise LOW.

### A03: Injection

- 5 × `sqlalchemy.text(f"...")` in `memory-bus/store.py`. Reviewed inline:
  - All five interpolate `memory_type` (column-name selector) and similar internal config strings, not user payloads.
  - User-payload values (`session_id`, `content`, embeddings) are passed via SQLAlchemy bind parameters (`:session_id`, `:content`).
  - **Hardening recommendation:** wrap the column selector in a hardcoded allowlist (`assert memory_type in {"sdd","decision","wiki",...}`) before substitution to make the safety property obvious to future readers. Currently safe-by-convention.
- No raw `format()` / `%` SQL detected.
- `content-engine` CLI uses parameterized SQL only.

**Severity:** MEDIUM — explicit allowlist hardening warranted.

### A04: Insecure Design

- Webhook handling: only Solex has a webhook surface in scope. Solex Square webhook signature verification not audited in detail this pass — defer to Solex audit.
- Magic-link entropy / expiration / one-time-use: not audited in detail this pass; flag.
- OAuth state parameter: Solex Square OAuth surface not audited; flag.

**Severity:** MEDIUM — defer Solex auth to dedicated pass.

### A05: Security Misconfiguration

- 2 Dockerfiles run as root (HIGH #5).
- Solex `BaseConfig` / `ProdConfig` missing `SESSION_COOKIE_SECURE` (HIGH #7).
- Solex `_external=True` `url_for` without Host allowlist (HIGH #8).
- `growdirect_pgadmin` exposes `127.0.0.1:5050` with `admin/admin` — dev-only, acceptable.
- No security-headers framework on memory-bus MCP (Talisman / similar). Acceptable for an MCP-protocol service — not a browser surface.
- No security headers on Solex (Flask-Talisman not installed). Solex serves browser content (templates/, Alpine.js, Tailwind) — should add Talisman with CSP, HSTS, frame-options before production.

**Severity:** HIGH (Dockerfile root + missing Secure cookie + Talisman-on-Solex).

### A06: Vulnerable Components

- pip-audit: 0 vulns on content-engine. Re-run on Solex.
- No SCA on JS deps (Solex `package.json` has Alpine.js, Tailwind, Leaflet, postcss). `npm audit` not run this pass — recommend adding to CI.

**Severity:** LOW — re-scan Solex Python + JS before partner access.

### A07: Identification & Authentication Failures

- memory-bus uses static API key (`MCP_API_KEY` env). No rotation policy, no multi-key support, no audit log. For a sidecar that only Canary's ALX queries, acceptable; document the threat model.
- Solex magic-link not audited in detail — flag.

**Severity:** LOW.

### A08: Software & Data Integrity Failures

- No commit signing enforced.
- No Dependabot / Renovate (observation, not in scope).
- `.mcp.json` integrity: HEAD blob contains live keys; CI is not currently scanning `.mcp.json` for credentials in pre-commit.

**Severity:** MEDIUM — add `.gitleaks` to CI and a pre-commit hook before next external review.

### A09: Logging & Monitoring Failures

- `services/memory-bus/memory_bus/server.py` uses Python `logging`. Not audited for credential disclosure in log lines.
- `content-engine` writes activity logs to `Brain/raw/.logs/` (gitignored).

**Severity:** LOW — formal logging review out of scope.

### A10: SSRF

- `content-engine` makes HTTP calls only to user-specified inputs (markdown extraction is filesystem-bound). No SSRF surface.
- `services/memory-bus` calls `http://growdirect_ollama:11434` (intra-compose, hardcoded host). No user-controlled URL.
- Solex Square client makes outbound calls to `connect.squareupsandbox.com` / production — hardcoded host. No SSRF surface.

**Severity:** LOW.

---

## Multi-tenant isolation review

The platform layer (memory-bus + content-engine + growdirect-mcp) does not have a multi-tenant model — memory-bus is a single shared knowledge graph; the MCP API key is the only auth boundary. Solex has tenant-like models (`SolexAccount`, `SolexOrder`) but Solex isolation is out of scope of the platform audit; flag for Solex-side audit.

**Severity:** N/A for platform; deferred for Solex.

---

## Webhook handling

Only Solex has webhook handlers in this scope. Square webhook signature verification + replay protection on Solex are deferred to a Solex-specific audit pass. The pattern Canary uses (HMAC `compare_digest` + Valkey-backed dedup) is a known-good template — verify Solex matches.

---

## Data handling

- No PII inventory exists for the platform layer beyond what Canary documents (which is out of scope here).
- `Brain/wiki/` has narrative content describing customer/peninsula real estate detail (Cove / Angel project material) — no live PII; archival.
- `docs/_archive/ip-vault/` contains historical timelog narratives that may include personal references; archive-only and not accessed by code.

**Severity:** LOW (platform). Solex PII surface (account names, addresses, payment metadata) deferred.

---

## Infra config

- `devops/docker-compose.yml`: ports bound `127.0.0.1:*` — Postgres, Valkey, pgAdmin, Ollama, memory-bus all loopback-only on the host. ✅
- Postgres / Valkey / Ollama not internet-exposed at the docker level. ✅
- `.env`: not present in repo root; not in `.gitignore` (potential gap — recommend adding `.env` and `*.env` to platform `.gitignore` for defense in depth even though no platform-root `.env` is currently committed). The Solex subdir handles its own `.env` correctly.
- Containers run non-root: ❌ — see HIGH #5.
- Prod vs dev config distinct: Solex has `BaseConfig`/`DevConfig`/`TestConfig`/`ProdConfig` separation. ✅ memory-bus has `Config` (single class with env-driven values). Acceptable for a single-purpose sidecar.

**Severity:** HIGH (root containers); otherwise OK.

---

## Dependency freshness

- content-engine: pinned versions all current (Apr 2026).
- memory-bus: uses `pyproject.toml` install — not version-locked at the lockfile level; recommend adding `uv.lock` or pip-tools-generated `requirements.txt`.
- Solex: `requirements.txt` + `requirements-dev.txt` present; not audited in this pass.

**Severity:** LOW — add Solex pip-audit to CI.

---

## Rate limiting

- memory-bus: no rate limiting on MCP tool calls (single-tenant, single-key, low risk). Acceptable.
- Solex: not audited in this pass.

**Severity:** LOW (platform).

---

## Security headers

- memory-bus: no Flask web surface — N/A.
- Solex: no Flask-Talisman / no manual CSP / HSTS / X-Frame-Options / X-Content-Type-Options / Referrer-Policy headers. **Browser-facing app needs these before production.** (Counts as HIGH for Solex audit; flagged here as observation since Solex is in the platform repo but typically gets its own audit.)

**Severity:** HIGH (Solex browser surface) — defer to Solex audit.

---

## Findings by severity

### CRITICAL

| # | Finding | Location | Disposition |
|---|---|---|---|
| C-1 | Firecrawl API key in `.mcp.json` (HEAD) | `.mcp.json:8` | Rotate + gitignore + history rewrite |
| C-2 | Obsidian REST API key in `.mcp.json` (HEAD) | `.mcp.json:17` | Rotate + gitignore + history rewrite |
| C-3 | GitHub PAT in committed timelog | `docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-25.md:383` | Verify rotated; if not, rotate; history rewrite optional |
| C-4 | `CANARY_ENCRYPTION_KEY` Fernet in SDD + plan | `docs/sdds/canary/architecture.md:517` + `docs/_archive/plans/2026-03-26-...md` | Rotate (with Canary S-8/S-9); replace with placeholder |

### HIGH

| # | Finding | Location |
|---|---|---|
| H-1 | Square sandbox tokens in archived dispatches (×9 + 4 curl) | `docs/_archive/ip-vault/_archive/dispatches/` and `_archive/workorders/` |
| H-2 | Dockerfiles run as root | `services/memory-bus/Dockerfile`, `Solex/devops/Dockerfile` |
| H-3 | 5 × `sqlalchemy.text(f"...")` in memory-bus | `services/memory-bus/memory_bus/store.py:{293,310,329,394,587}` |
| H-4 | `SESSION_COOKIE_SECURE` not set in Solex `BaseConfig`/`ProdConfig` | `Solex/solex/config.py` |
| H-5 | `_external=True` magic links without Host allowlist | `Solex/solex/routes/{admin,account}_auth.py` |
| H-6 | No security headers (Talisman / CSP / HSTS) on Solex | `Solex/solex/__init__.py` |

### MEDIUM

| # | Finding | Location |
|---|---|---|
| M-1 | `0.0.0.0` bind in memory-bus server (Bandit B104) | `services/memory-bus/memory_bus/server.py:19` |
| M-2 | MD5 hash for placeholder gen | `Solex/solex/services/placeholder_gen.py:30` |
| M-3 | `.mcp.json` not in `.gitignore` (after C-1/C-2 rotation) | `.gitignore` |
| M-4 | `.env` / `*.env` not blanket-ignored at platform root | `.gitignore` |
| M-5 | memory-bus has no pip lockfile | `services/memory-bus/pyproject.toml` |
| M-6 | No CI gitleaks pre-commit hook | repo |
| M-7 | No Dependabot / Renovate config | repo |
| M-8 | Solex auth surface not audited in this pass | `Solex/solex/routes/` |
| M-9 | Hardening: explicit allowlist around `text()` column-name interpolation | `services/memory-bus/memory_bus/store.py` |

### LOW

- 120 × Bandit B101 (test asserts) — expected.
- 10 × Bandit subprocess findings in `content-engine/engine.py` — legitimate use of markitdown.
- 50 × trufflehog Postgres DSN findings — all documented dev credentials in CLAUDE.md; not secrets.
- 1 × trufflehog `EightxEight` false positive in a Lotus Notes archive binary.
- 1 × trufflehog `PrivateKey` in `.obsidian/plugins/obsidian-local-rest-api/data.json` — gitignored, local-only RSA key for the Obsidian REST API; not committed.
- 1 × Brain wiki + 1 × archived risk dictionary `API-KEY-ABC123` placeholders — not real secrets.
- 1 × `wrong-key-wrong-key-32bytesXXXX` negative-test fixture in plan doc — not real.
- 2 × Anthropic + 1 × Square verified findings under `Canary/.env` — Canary scope, covered in their report.

---

## Committed secrets — disposition required

Per spec SC10: documented is NOT sufficient — must rotate AND purge from history before partner access.

| ID | Surface | File / Commit | Pattern | Currently in HEAD? | Action required |
|---|---|---|---|---|---|
| C-1 | Firecrawl API | `.mcp.json:8` / `4c0c47dbb2` | `fc-fec9...8821e` | YES | 1) Rotate in Firecrawl dashboard 2) Move to env var (`FIRECRAWL_API_KEY` from shell env) 3) Add `.mcp.json` to platform `.gitignore` 4) Optional: `git filter-repo` blob purge |
| C-2 | Obsidian Local REST | `.mcp.json:17` / `4c0c47dbb2` | `75a1...2d5b` | YES | Same as C-1 — rotate in Obsidian Local REST API plugin settings, move to env var, gitignore, optional history rewrite |
| C-3 | GitHub PAT | `docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-25.md:383` / `a7790832c4` | `ghp_2FwZ...AAX` | YES | 1) Test if token still valid (`curl -H "Authorization: token ghp_..."  https://api.github.com/user`) 2) If valid: revoke at `github.com/settings/tokens` 3) Replace with `<rotated-pat>` placeholder in the timelog 4) Optional: history rewrite |
| C-4 | Canary Fernet | `docs/sdds/canary/architecture.md:517` and `docs/_archive/plans/2026-03-26-growdirect-platform-and-cove-rebuild.md` | `BHDJWBeEEtNrcqq...` | YES | 1) Coordinate with Canary S-8/S-9 rotation (single key shared across both repos) 2) Generate new Fernet, deploy via env, re-encrypt any QA/prod tokens 3) Replace literal in SDD + plan with `<generate-with-Fernet>` placeholder |
| H-1 | Square sandbox token | `docs/_archive/ip-vault/_archive/dispatches/{Jeremy_B065_Combined_MaxSession.md, Jeremy_LiveWebhook_SessionPrompt.md, Jeremy_SquareOAuth_SessionPrompt.md}`, `docs/_archive/ip-vault/_archive/workorders/WORKORDER_B067_SquareCapabilityDashboard.md`, `docs/_archive/ip-vault/_archive/dispatches/B067_SquareCapabilityDashboard_MasterDispatch.md` / `a7790832c4` | `EAAAl3ns-vSWSv...wyj693Rl` | YES | 1) Revoke in Square sandbox developer dashboard (single rotation covers both Canary S-3 and platform H-1) 2) Replace literal with `<sandbox-token>` placeholder 3) Sweep `docs/_archive/ip-vault/_archive/` for any other token patterns |

### Rotation priority order (separate remediation PR)

1. **C-1 + C-2** — `.mcp.json` keys are reachable from a public clone; rotate first.
2. **C-3** — GitHub PAT confirmation; rotate if not already done.
3. **C-4 + H-1** — coordinate with Canary's matching rotations (S-8/S-9 + S-3).
4. **`.gitleaksignore` + `.gitignore` updates** — same PR as the rotations.
5. **Optional: `git filter-repo` history rewrite** — defer until pre-public-clone moment per Canary report's same recommendation; rotation alone is sufficient near-term.

---

## Judgment calls

1. **`.mcp.json` history rewrite** — the file currently sits in `HEAD` with two real keys. After rotation, the keys are dead but the pattern remains in history. For a pre-public solo-founder repo, rotation alone is sufficient near-term. Defer history rewrite until ready to make the repo external. Same call as the Canary `.env.openclaw` decision.

2. **GitHub PAT scope** — the line context says "rotate after demo week". Need to verify whether rotation actually happened; if the timelog was written 2026-02-25 and the demo week followed shortly, the token may already be dead. Test before scheduling the rotation work.

3. **`docs/_archive/ip-vault/_archive/`** — this directory contains a substantial volume of historical work-order dispatches that include the Square sandbox token in 6 files. Two paths:
   - (a) Sweep + replace inline. Manual but precise.
   - (b) Move the entire `docs/_archive/ip-vault/_archive/` subtree into a separate private archive repo and `.gitignore` it here, rotating the token regardless. Cleaner long-term.
   - Recommend (b) for partner-readiness; (a) as a stopgap.

4. **Solex audit** — Solex has multiple high-severity findings (no `SESSION_COOKIE_SECURE`, no Host allowlist on magic links, no Talisman for browser headers, missing Dockerfile USER) and an unaudited webhook surface. **Recommend a Solex-specific audit pass before partner access.** Out of scope here, but flagged.

5. **memory-bus `text(f"...")` hardening** — currently safe by convention. Adding an explicit allowlist before each f-string interpolation site is a small defensive change that makes the safety property obvious to a code reviewer / Semgrep. Schedule as a standalone hardening PR.

6. **CI tooling gap** — no gitleaks pre-commit hook, no Dependabot. Even with rotation done, the next leak could land just as easily without these. Recommend a `.pre-commit-config.yaml` + GitHub Action wiring before partner access.

---

## Out-of-scope observations

- **DAST / authenticated endpoint scan** — not run; recommend ZAP / Nuclei before external partner diligence on Solex.
- **Container image scan (trivy image)** — not run on the built `growdirect-memory-bus` image; run after next push.
- **`npm audit`** on Solex JS deps — not run.
- **Solex security audit** — Solex code was reachable via the platform-scope semgrep / bandit runs but warrants a dedicated audit (auth surface, webhook signature verification, OAuth state, Talisman, CSRF).
- **Commit signing** not enforced.
- **`docs/_archive/`** is a substantial historical archive (37 dispatches, multiple timelog directories) — sweeping for embedded credentials in archived material is itself a workstream.

---

## Methodology Notes

- Tools run from branch `fix/solex-live-debug-pass` against `/Users/gclyle/GrowDirect`.
- Git history: 364 commits scanned by gitleaks, ~52 MB.
- All raw tool JSON outputs in `/Users/gclyle/GrowDirect/docs/audit-2026-04-23/security-tool-output/`.
- Trufflehog filesystem walked subdirs (Canary/, etc.) — those are reported but excluded from the platform-scope finding counts; Canary findings are documented in Canary's separate audit report.
- Manual review covered: `.gitignore`, `.mcp.json`, `devops/docker-compose.yml`, `services/memory-bus/Dockerfile`, `Solex/devops/Dockerfile`, `Solex/solex/config.py`, `services/memory-bus/memory_bus/server.py`, `services/memory-bus/memory_bus/store.py`, `content-engine/engine.py`, plus targeted greps for auth gates, `_external=True`, `text()` use, and PII patterns.
- Nothing in this audit modified source files. No secrets were rotated; that is a separate workstream.
