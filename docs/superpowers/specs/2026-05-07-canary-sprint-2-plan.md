# CanaryGo — Sprint 2 plan (Ruptiv handover + security + code health)

Synthesis of three independent reviews completed 2026-05-07:
- [Code review](2026-05-07-canary-code-review.md) — 4 P0 / 6 P1 / 5 P2 / 5 P3
- [Security review](2026-05-07-canary-security-review.md) — 5 Critical / 6 High / 5 Medium / 4 Low / 3 Info
- [IP handover scan](2026-05-07-canary-ip-handover-scan.md) — 5 Block / 12 Required / 8 Recommended / 4 Note

Plus a brand-voice directive (2026-05-07): "metered" replaces satoshi/bitcoin/lightning vocabulary on every external-facing surface; protocol/wallet/L402 implementation paths keep native terminology because those terms describe the actual mechanism.

## Executive summary

Three independent audits converge on a single structural finding: **the merchant UI was built to completion before the trust boundary existed.** `tenantIDFromCtx` returns `uuid.Nil`, no auth middleware wraps `internal/web/`, the casemgmt service trusts `?tenant_id=` from the query string, the `/admin/audit` page is unauthenticated, the Square demo cookie is plaintext UUID, and CSRF is absent on 15+ POST routes. Both reviewers — code and security — flagged this as their top theme without coordination. That signals it's the real shape of the problem, not artifact of one reviewer's framing.

Adjacent to that: the protocol layer (HMAC webhook ingestion, evidence chain, Merkle anchor, RS256 JWT, argon2id API keys, Square OAuth state CSRF) is well-engineered and would survive a careful audit on its own. The asymmetry is real and useful — it means **fixing the application surface to match the protocol-edge bar is mechanical, not architectural.** The patterns exist; they need to wrap the right routes.

For handover, the shape is similarly concentrated. Five Block-tier items, two of which are counsel-gated (LICENSE entity, patent posture). The largest single mechanical edit is the Go module path rename — `github.com/growdirect-llc/rapidpos` → `github.com/ruptiv/canary` — touching 153 files and 383 import lines. Once that lands, every other rename + scrub follows in parallel.

**Sprint 2 sizing: one two-week sprint, one engineer can land the handover-critical work plus the auth foundation. A second engineer in parallel can close the brand-surface scrubs.** Wave 5 (code health) slips to Sprint 3 if Sprint 2's load is real. The audit-log append-only trigger (H4) and pgx CVE bump (H3) are afternoon tickets and ship inside the first three days regardless.

The single hardest item is **CanaryGo/CLAUDE.md claims an invariant that does not exist in the schema**: "fox.evidence_records has a DB trigger blocking UPDATE/DELETE" — verified absent. That's a documentation-vs-reality mismatch in a file every agent and engineer reads as ground truth. Fixing the trigger is small. Trusting CLAUDE.md less is harder.

## What the three reviews agree on

The reviews ran independently and converge:

| Finding | Code | Security | Handover |
|---|---|---|---|
| `tenantIDFromCtx` returns `uuid.Nil`, no auth on `/internal/web` | P0 #1 | C1 | — (out of handover scope) |
| `merchantIDFromCtx` from URL query | P0 #2 | C2 | — |
| CSRF absent on UI POSTs | P0 #3 | H2 | — |
| Module path / lineage | — | — | R1 (Block) |
| `app.audit_log` trigger missing | — | H4 + CC7.2 fail | — |
| Brand callouts in user-facing surfaces | — | — | B4 |

Where two reviews flag the same finding, it's a Sprint 2 must-close. Where only one flags it, look at whether the unflagged review was even scoped to find it (e.g., the handover scan didn't review code quality, so its silence on `handler.go:316-319` doesn't lower the priority).

## Sprint 2 wave structure

Five waves. Within each wave, tickets can land in parallel; between waves, there are real dependencies.

```
Wave 1: Handover blockers          ── days 1-2
   ├─ T-A  Module path rename                     M    blocker for everything import-touching
   └─ T-R  LICENSE entity swap                    S    counsel-gated; can run async

Wave 2: Auth foundation            ── days 2-7
   ├─ T-B  Identity middleware + uuid.Nil reject  L    unlocks 5+ findings
   ├─ T-F  Audit log append-only trigger          S    compliance fix
   └─ T-G  pgx v5.6.0 → v5.9.0 + govulncheck CI   S    one-line + CI

Wave 3: Auth surface lock-down     ── days 5-9   (depends on T-B for the contextual claims)
   ├─ T-C  Protocol evidence + admin auth         M    closes C3 + C4 + H1
   ├─ T-D  Sign Square demo cookie                S    closes C5
   ├─ T-H  DLQ tenant-scope                       S    closes H5
   └─ T-E  CSRF + body-size on UI POSTs           M    closes P0#3 + H2 + M3

Wave 4: Brand + handover scrubs    ── days 3-9   (parallel with Waves 2-3)
   ├─ T-S  Brand callout sweep                    M    closes B4 + R7 + R8 (needs domain decision)
   ├─ T-U  Runbook + cloudbuild + mirror scrub    M    closes B2 + R3-R6
   ├─ T-V  Internal positioning scrub             S    closes B5 + R11
   ├─ T-T  Dev infra naming sweep                 M    closes R2 (~25 files)
   ├─ T-W  Seed secret literal → generator        M    closes B3
   └─ T-AA Metered terminology on brand surfaces  M    NEW — brand-voice directive

Wave 5: Code health                ── days 8-12  (post-handover hygiene)
   ├─ T-J  Delete stub-shadow + W16 file extract  S    closes P0#4 + P2#2
   ├─ T-K  Tag integration tests properly         M    closes P1#2 (65 tests)
   ├─ T-I  Fail-open hardening                    S    closes M1 + M5 + L2
   ├─ T-L  API key prefix index                   M    closes P1#3
   ├─ T-N  reportCategory SQL aggregation         S    closes P1#5
   ├─ T-M  .env.example + CLAUDE.md sweep         S    closes P3#1 + P2#1
   ├─ T-P  Dockerfile golang:1.24 → 1.25          S    closes P1#6
   ├─ T-O  Trim ecom Adapter interface            S    closes P2#3
   └─ T-Q  routewalk gitignore + timestamp        S    closes P2#4

Deferred to Sprint 3:
   ├─ T-X  GRO ticket reference cleanup           L    252 refs / 80 files
   ├─ T-Y  Devops console phase-1 cleanup         S    R9 + N2 + N4
   └─ T-Z  Sprint terminology sweep               L    333 comments
```

## Critical path

The single chain that, if any link slips, slips the sprint:

```
T-A (rename) → T-B (identity) → T-E (CSRF) → board package can demo with a real tenant
   ↓
T-R (LICENSE) → board package can be legally transferred
   ↓
T-S (brand) + T-U (runbook) + T-AA (metered) → board package can be read by the board
```

Everything else is parallel work that improves the package but doesn't gate it.

## Ticket inventory

### Wave 1 — Handover blockers

**T-A: Go module path rename** — `github.com/growdirect-llc/rapidpos` → `github.com/ruptiv/canary`. Mechanical sweep of 153 Go files, 383 import lines, `go.mod`, `go.sum`, cloudbuild substitutions, mirror script (review whether it ships at all), gateway link literals. Single PR, single commit, branch tip; do not interleave with code changes. Closes: HANDOVER R1. Effort: M.

**T-R: LICENSE entity swap + license posture decision** — Replace `Copyright (c) 2026 GrowDirect LLC` (LICENSE:181) with the precise Ruptiv legal entity. Counsel sign-off gates the entity name. Confirm Apache-2.0 stays; confirm patent 63/991,596 grant is intentional; if posture changes, propagate to `cmd/sub1-*`, `cmd/sub2-*`, `cmd/sub3-*`, `cmd/gateway`, OpenAPI YAML, cloudbuild label, runbook. Closes: B1, R12. Effort: S coding, counsel-gated.

### Wave 2 — Auth foundation

**T-B: Identity middleware + nil-tenant rejection** — Wire `identity.ClaimsFromContext(ctx).TenantID` through `internal/auth/middleware.go`; mount over `web.Handler.Mount`'s root; replace `tenantIDFromCtx` (handler.go:3420) and delete `merchantIDFromCtx` (handler_w10.go:37). **Add defensive `if tenantID == uuid.Nil { return ErrUnauthorized }` to every store entrypoint** so a future regression cannot reproduce the silent-leak shape. Closes: Code P0 #1, P0 #2; Sec C1, C2 (partial). Files: `internal/web/handler.go`, `cmd/gateway/main.go`, `internal/auth/middleware.go`, all 30+ store entrypoints. Effort: L. **This is the long pole of Sprint 2.**

**T-B-1: AtlasView identity contract pin** — sister ticket to T-B. [GRO-848](https://linear.app/growdirect/issue/GRO-848) asks the identity-service team to confirm or amend the six contract surfaces AtlasView consumes (JWT mint, JWKS verify, WhoAmI, per-org SSO, JIT provisioning, operational SLA). The contract surfaces are the design input for T-B's implementation choices — closing the contract early in Sprint 2 lets T-B converge with AtlasView's expectations rather than diverge and reconcile later. AtlasView D-134 chose to delegate auth to canary.go's `internal/identity` (port 8086) rather than re-implement; this ticket closes the gaps. Substrate at `CanaryGo/docs/decisions/gro-848-atlasview-identity-integration.md`. Effort: S (review + sign-off, not implementation). Estimated AtlasView-side implementation post-contract: 4-7 days (separate engineer, parallel track).

**T-F: Audit log append-only trigger** — Migration mirroring the protocol.evidence trigger pattern, applied to `app.audit_log`. CLAUDE.md claims this trigger exists; the schema does not have it. Migration `031_audit_log_append_only.{up,down}.sql`. Closes: H4 + SOC2 CC7.2 + GDPR Art 30. Effort: S.

**T-G: pgx v5.6.0 → v5.9.0 + govulncheck in CI** — One-line `go.mod` bump, regenerate `go.sum`, add a `.github/workflows/` step running `govulncheck ./...`. Closes: H3 (CVE-2026-33815, CVE-2026-33816). Effort: S.

### Wave 3 — Auth surface lock-down

**T-C: Protocol evidence + admin endpoint auth** — Strip `merchant_id` and `raw_payload` from public `/v1/protocol/evidence/{event_hash}` response, OR gate the full record behind API-key + tenant-match. Require API-key + ownership proof on `POST /v1/protocol/namespace`. Add `RequireAdmin` predicate; pass `claims.TenantID` into `audit.ListByMerchant`. Closes: C3, C4, H1. Effort: M.

**T-D: Sign Square demo session cookie** — Replace plaintext UUID cookie with HS256-signed JWT or `securecookie`. Force `Secure: true`. Closes: C5. Effort: S.

**T-H: DLQ admin endpoints — tenant scope** — Force `f.MerchantID = &claims.TenantID` for tenant-scoped keys in `cmd/gateway/admin.go`. Closes: H5. Effort: S.

**T-E: CSRF + body-size caps on UI POSTs** — Wrap merchant UI route group with chi-compatible CSRF middleware (decision in an ADR — gorilla/csrf vs double-submit cookie). 64 KiB body cap unless evidence upload. Emit token in templates. Update every POST handler test. Closes: Code P0 #3, Sec H2 + M3. Files: `cmd/gateway/main.go`, new `internal/web/middleware.go`, every form template + test. Depends on T-B landing first. Effort: M.

### Wave 4 — Brand + handover scrubs (parallel with Waves 2-3)

**T-S: Brand callouts in user-facing surfaces** — Sweep Square OAuth handler footers (handler.go:280, 282, 284, 286, 393, 395, 397), OpenAPI `info.contact`, discovery doc links (`vault`, `sdds` at gateway/main.go:330-331), runbook footer URLs. **Decision required: destination domain.** Suggested: `canary.ruptiv.com`. Update both the static YAML and the `generate.py` source. Closes: B4, R7, R8. Effort: M.

**T-U: Runbook + cloudbuild + scripts scrub** — Strip founder username, founder home dir paths, Linear URLs, founder Gmail commit identity (mirror-public.sh:48). Parameterize GCP project ID. **Recommend deleting `scripts/mirror-public.sh` entirely** — its mirror target won't exist post-handover. Closes: B2, R3, R4, R5, R6. Effort: M.

**T-V: Internal positioning scrub** — Rewrite "Bart's wedge" comment in `internal/adapters/counterpoint/parser.go:2` to describe the adapter's contract, not its strategic positioning. Rewrite "OQ Resolution Pack / founder-approved" framing in 5 files (TBD per scan). Closes: B5, R11. Effort: S.

**T-T: Dev infrastructure naming sweep** — Rename `growdirect:growdirect_dev`, `growdirect_postgres`, `growdirect_valkey`, `growdirect` Docker network → Ruptiv-owned equivalents. ~25 files: Makefile, compose, .env.example, GitHub Actions, 11 integration-test file headers. Coordinate with parent `devops/docker-compose.yml`. Closes: R2. Effort: M.

**T-W: Seed secret literal → generator** — Replace `dev-only-do-not-ship-this-secret-1234567890abcdef` (deploy/schema/99_seed.sql:64) with a placeholder reference (`'__SEED_HMAC_PLACEHOLDER__'`); generate dev secret in setup script; document rotation; add CI guard that fails if placeholder leaks. Apply same treatment to `argon2id$DEV_PLATFORM_PLACEHOLDER` / `argon2id$DEV_TENANT_PLACEHOLDER`. Closes: B3. Effort: M.

**T-AA: Metered terminology on brand surfaces** *(new — from the 2026-05-07 brand directive)* — Flip user-facing strings from satoshi/bitcoin/lightning vocabulary to metered/protocol terminology. Scope:
- `internal/web/handler_w8.go` — billing page renders "satoshi cost meter" + variables `TotalSatoshis`, `StorageSatoshis`, `WorkloadSatoshis`, `CaptureSatoshis` to merchants. Flip to `TotalUnits` / `StorageUnits` / etc., keep underlying schema columns.
- `internal/devops/static/canary-api-v1.yaml` — "Returns a Lightning invoice (or stub)" — rewrite as "Returns a metered protocol challenge."
- `cmd/gateway/main.go` comments — "Lightning wallet calls" — rewrite where customer-/partner-readable.
- ~10 cards under `Brain/wiki/cards/` that are positioning documents (`platform-l402-ildwac-moat.md`, `satoshi-cost-model.md`, `canary-tokenomics-anonymous-protocol.md`, etc.) — full rewrites in metered framing before they ship in the board package.

What stays:
- DB column names (`*_satoshis`) — internal implementation. Add a translation layer that maps to "metered units" at any boundary that crosses out of the engine.
- `internal/wallet/`, `goose/`, `internal/auth/lnurl/`, `cmd/sub3-merkle-ordinal` — technical implementation; the mechanism IS Bitcoin/Lightning, naming it something else would be misleading.
- Migration files (historical record).

Effort: M (brand surfaces are concentrated; the bulk of total hits — ~3,400 in Brain + docs — is positioning content that gets rewritten as part of the board package preparation, not code).

### Wave 5 — Code health (Sprint 3 if Sprint 2 is full)

**T-J: Stub-shadow + W16 extraction + dead stubs** — Delete duplicate `/reports/category` registration (handler.go:317-319). Delete `stubChirps`, `stubAlerts`, `stubRules`, `stubHawkList`. Move W16 case-management handlers (handler.go:3184-3415) into `internal/web/handler_w16.go`. Closes: Code P0 #4, P2 #2, P1 #1 partial. Effort: S.

**T-K: Tag integration-shaped tests** — Add `//go:build integration` to all 65 `testutil.MustConnect` test files in `internal/web/` and `internal/lp/`. Migrate from `DATABASE_URL` to `GATEWAY_TEST_DATABASE_URL`. Update `Makefile` + `docs/conventions.md`. Closes: Code P1 #2. Effort: M.

**T-I: Production fail-open hardening** — `ENV=production`-aware fatals for `LNURL_JWT_SECRET`, `VALIDATOR_SECRET`, `LNURL_SCHEME`, `SECRET_BACKEND`. Closes: Sec M1, M5, L2. Effort: S.

**T-L: API key lookup — prefix-indexed verification** — Add `key_prefix` column to `app.api_keys` (migration 032), populate on creation, index it. Change `AuthenticateAPIKey` to `WHERE key_prefix = $1` filter so each request runs at most one argon2id verify. Closes: Code P1 #3. Effort: M.

**T-N: `reportCategoryPage` SQL aggregation** — `ItemStore.AggregateByCategory(ctx, tenantID)` returning per-category counts + avg margin in one query. Replace 500-row truncated in-memory aggregate. Closes: Code P1 #5. Effort: S.

**T-M: `.env.example` + CLAUDE.md sweep** — Cover all 30 referenced env vars with dev defaults. Update `CanaryGo/CLAUDE.md` to describe the actual two-tier migration model (declarative schema + 019+ incremental). **Critical: fix the audit-log invariant claim** so future agents read accurate ground truth. Closes: Code P3 #1, P2 #1. Effort: S.

**T-P: Dockerfile Go version sweep** — Bump four Dockerfiles `golang:1.24-alpine` → `golang:1.25-alpine`. Drop `GOTOOLCHAIN=auto` once verified. Closes: Code P1 #6. Effort: S.

**T-O: Trim `internal/ecom`** — Remove unreferenced `Adapter` interface, `Order`, `ChannelHealth`. Re-add when first real adapter ships. Closes: Code P2 #3. Effort: S.

**T-Q: routewalk timestamp + gitignore** — Add `build/` to `CanaryGo/.gitignore`. Drop `GeneratedAt` from `routewalk.Output`. Closes: Code P2 #4. Effort: S.

### Deferred to Sprint 3

- **T-X: GRO reference cleanup** — 252 `GRO-NNN` references across 80 Go comments. Mechanical but high-volume. Effort: L.
- **T-Y: Devops console phase-1 cleanup** — Remove `PythonPriorArt`, drop `Brain/wiki/cards/...` paths, rename `BodyTODO` → `Status`. Effort: S.
- **T-Z: Sprint vocabulary sweep** — `Loop N`, `Wave A`, `Phase B.2` in 333 Go comments. Effort: L.

### Architectural assessments awaiting decision (post-Sprint 2 roadmap)

Two assessments landed at `CanaryGo/docs/decisions/` 2026-05-07. Each is decision-gated — **NOT** Sprint 2 work. Each will get its own sprint allocation if/when the team votes adopt or pilot.

- **[GRO-846](https://linear.app/growdirect/issue/GRO-846) — Neo4j MDM read-adjunct.** Whether to introduce Neo4j alongside Postgres for graph-shaped reads (Customer 360, product variants, location hierarchies, reporting structures, merchant org). Substrate at `CanaryGo/docs/decisions/gro-846-neo4j-mdm-adjunct.md`. AtlasView already runs this pattern in production. Recommended next step per the doc: 2-week PoC on Customer 360 dedup, decide post-PoC. Pilot effort: ~1 engineer, 6-10 weeks for first domain plus ongoing Neo4j ops cost.
- **[GRO-847](https://linear.app/growdirect/issue/GRO-847) — SQLite-on-device offline + sync layer for POS.** Whether to add on-device SQLite + sync layer for POS terminals during connectivity loss. Substrate at `CanaryGo/docs/decisions/gro-847-sqlite-offline-sync.md`. Tooling shortlist: PowerSync recommended (Postgres-native, SQL-based sync rules). Recommended next step per the doc: 4-week PoC on item-catalog read surface. Production-ready effort: 1-2 engineers, 12-16 weeks. Payment-offline policy decided ahead of PoC: queue intent, never offline-finalize.

These two are **forward-looking architecture work**, not handover prep. They get scheduled separately once the Sprint 2 sprint ships and the Canary team holds the decision-gate review on each.

## Open decisions (board / counsel before sprint kickoff)

1. **Module path target.** `github.com/ruptiv/canary` is suggested. Confirm the org name (`ruptiv` vs `ruptiv-platform` vs other) and that the GitHub org exists or will exist before Sprint 2 starts.
2. **LICENSE entity name.** Counsel-gated. T-R can't ship without this.
3. **Patent posture.** Apache-2.0 stays? Patent 63/991,596 grant intentional? If posture changes, T-R has downstream attribution sweep.
4. **Destination domain.** `canary.ruptiv.com` is suggested. T-S blocked until decided.
5. **Brand-naming tier (per the rename-risk discussion).** Tier 1 (module path only), Tier 2 (top-level brand stripped), or Tier 3 (full generic incl. bird metaphors)? Sprint 2 defaults to Tier 1; Tier 2/3 land in subsequent sprints if the board prefers.
6. **`scripts/mirror-public.sh` policy.** Recommend delete. Confirm.

## Compliance posture after Sprint 2

After T-B, T-C, T-D, T-E, T-F, T-G, T-H land:
- **PCI Service Provider** — closes Req 6 (vulnerability mgmt), Req 7-8 (network access), Req 10 (audit-trail integrity). Path to a real Service Provider readiness assessment opens.
- **SOC 2 Type II** — closes CC6 (logical access) and CC7.2 (system monitoring). The audit observation window can begin once these stabilize.
- **GDPR / CCPA** — closes Article 32 (security of processing) by virtue of removing the unauthenticated PII disclosure path. Article 30 (records of processing) closes via T-F.

## What's NOT in Sprint 2

- The Phase 2 manifest backfill grind ([GRO-836](https://linear.app/growdirect/issue/GRO-836) sub-tickets) — paused until handover stabilizes. The 137 unaccounted endpoints stay unaccounted; the catalog grid stays sparse on those cells.
- The W-series UI deepening (turning "TODO" service bodies in `/devops/<svc>` shells into real operator workflows). That's Phase 3 of the sysadmin module epic regardless.
- AtlasView / Canary mesh layer work in `/Users/gclyle/Ruptiv/`. Lives in the Ruptiv repo's dispatch system, not in CanaryGo's sprint plan.
- New features. Sprint 2 is hardening + handover.

## Sprint 2 success criteria

1. `git clone <ruptiv-org>/canary && go build ./... && go test ./...` succeeds against a fresh checkout with no GrowDirect references in the working tree (history excluded).
2. `make manifest && make manifest-strict` succeeds with the existing manifest still valid post-rename.
3. `tenantIDFromCtx` returns claims, never `uuid.Nil`. Every store entrypoint defensively rejects nil tenants.
4. `app.audit_log` has the append-only trigger that CLAUDE.md claims; CLAUDE.md is corrected if the trigger differs from what was claimed.
5. `pgx` is at v5.9.0; `govulncheck` runs in CI and is green.
6. The five Block-tier handover findings (B1-B5) are closed with PRs landed.
7. Brand surfaces — UI strings, OpenAPI, discovery doc, runbook footers — read as Ruptiv-owned property. The Square OAuth dashboard shows "Ruptiv" not "GrowDirect LLC".
8. Brain wiki cards that ship in the board package are rewritten in metered terminology; cryptocurrency vocabulary is confined to wallet/L402/protocol code.
9. The board package — a tagged release of the Ruptiv repo with CanaryGo absorbed — exists and a one-page README points the reader at the right entry points.

That last criterion is the actual handover deliverable. Everything else is the work that lets it pass a careful read.
