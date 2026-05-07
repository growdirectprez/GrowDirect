# CanaryGo — Sprint 3 plan (AtlasView contract + brand cleanup + code health)

Drafted 2026-05-07, on the wrap of Sprint 2. Sprint 2 shipped the auth-surface lockdown (T-A, T-B Phase 1+2, T-C, T-E, T-H — all closing [GRO-849](https://linear.app/growdirect/issue/GRO-849) child tickets) plus the doable-now batch from the three reviews. What remains is **counsel/brand-gated cleanup**, **integration readiness for AtlasView**, and the **code-health backlog deferred from Sprint 2**.

The shape of Sprint 3 is different from Sprint 2's. Sprint 2 was security-driven — three independent reviews converging on the same trust-boundary gap. Sprint 3 is **integration-driven**: the Ruptiv board package needs to demonstrate AtlasView ↔ canary.go talking through a real identity contract, not just two repos sitting next to each other. The integration story is what makes the package legible.

## Executive summary

Three workstreams, roughly equal weight:

1. **AtlasView identity contract** ([GRO-848](https://linear.app/growdirect/issue/GRO-848) surfaces 1-3) — the integration-readiness anchor. JWT mint, JWKS verify, WhoAmI RPC. Closes the AtlasView-side blocking dependency for middleware ship. ~5-7 days for one engineer once the contract closes (per the GRO-848 doc estimate).
2. **Counsel/brand carryover** (T-R, T-S, T-T, T-U) — gated on decisions, not engineering. Land them in Sprint 3 if/when the gates clear; otherwise carry to Sprint 4. The brand decisions need to come down from Ruptiv's side, not invented by Canary.
3. **Code health deferred from Sprint 2** (T-X, T-Y, T-Z) — mechanical, high-volume, low-risk. The kind of work that makes the receiving team's first read clean. T-X is 252 GRO refs across 80 files; T-Z is 333 Loop/Wave/Phase comments. Land in any-order during the sprint.

**Sprint 3 sizing: one two-week sprint, one engineer can land the AtlasView contract plus the code-health backlog. A second engineer in parallel closes the brand-surface scrubs as their gates open.** AtlasView contract surfaces 4-6 (per-org SSO, JIT, operational SLAs) move to Sprint 4 unless surfaces 1-3 land in the first week with margin.

The single hardest item is **two-key rotation on the JWKS endpoint with a ≥24h overlap window**. That's not a coding problem; it's an operational discipline question — does the gateway carry rotation state across restarts? Does Cloud Run instance scale-out propagate the new key? Sprint 2's `CSRF_SECRET` / `VALIDATOR_SECRET` / `LNURL_JWT_SECRET` pattern of "fatal in production if absent" is the wrong model here — JWKS rotation needs *both* keys live simultaneously, not "one key, fatal if missing."

## Sprint 3 wave structure

```
Wave 1: AtlasView contract — surfaces 1-3   ── days 1-7   (the anchor)
   ├─ T-1  JWT minting endpoints                  M    login / refresh / MFA
   ├─ T-2  JWKS endpoint + two-key rotation       L    operational discipline
   ├─ T-3  WhoAmI RPC GET /v1/me                  S    bearer auth wrapper
   └─ T-4  Contract test fixtures + test vectors  M    shared with AtlasView

Wave 2: Counsel/brand carryover            ── parallel (gated, not blocking)
   ├─ T-R  LICENSE entity swap                    S    counsel-gated (decision live)
   ├─ T-S  Brand callout sweep                    M    needs destination-domain decision
   ├─ T-T  Dev infra naming sweep                 M    ~25 files; needs Ruptiv conventions
   └─ T-U  Runbook + cloudbuild + mirror scrub    M    needs Ruptiv ops conventions

Wave 3: Code health backlog                ── days 5-12  (deferred from Sprint 2)
   ├─ T-X  GRO ticket reference cleanup           L    252 refs / 80 files
   ├─ T-Y  Devops console phase-1 cleanup         S    R9 + N2 + N4
   └─ T-Z  Sprint terminology sweep               L    333 comments — Loop/Wave/Phase

Wave 4: AtlasView surfaces 4-6 (stretch)   ── days 8-12  (if Wave 1 lands clean)
   ├─ T-5  Per-org SSO config admin endpoints     M    Microsoft Entra OIDC
   ├─ T-6  JIT provisioning + audit event publish S    Person creation on first SSO
   └─ T-7  Operational SLA hardening              M    revocation, latency budgets
```

## Critical path

```
T-1 (JWT mint) → T-2 (JWKS) → T-3 (WhoAmI) → T-4 (contract tests)
                                                    ↓
                                  AtlasView middleware can ship
                                                    ↓
                                     integration story demonstrable
                                                    ↓
                                       board package legible
```

T-R / T-S / T-T / T-U are independent of T-1-4 — they unblock as soon as their counsel / brand decisions arrive. T-X / T-Y / T-Z slot into any week.

## Ticket inventory

### Wave 1 — AtlasView contract (the anchor)

**T-1: JWT minting endpoints.** Implement `/auth/login`, `/auth/refresh`, `/auth/mfa` on `internal/identity` per the GRO-848 contract. Access TTL 30 min, refresh TTL 12 hr, family-id tracking on rotation, reuse-detection invalidates the family. Audience claim includes `atlasview` and `canary` (audience-narrowing for inter-service tokens). RS256 / ES256 / EdDSA only — `none` algorithm rejected at the parser. Files: `internal/identity/jwt.go` (existing), new `internal/identity/auth/login.go`, new `internal/identity/auth/refresh.go`. Closes: [GRO-848](https://linear.app/growdirect/issue/GRO-848) surface 1. Effort: M.

**T-2: JWKS endpoint + two-key rotation.** Public `GET /.well-known/jwks.json` returning the active key set. Two-key rolling window during rotation: previous key stays valid for ≥24h after a new key is published, both keys serve token verification, only the newest mints. State must survive restarts (Postgres `app.signing_keys` table) and Cloud Run scale-out (instances re-read the table on a TTL cache). Required claims on every token: `iss`, `aud`, `exp`, `iat`, `sub`. Operational requirement: rotation runbook + alerting if both keys expire. **The hardest item in this sprint** — not because it's much code, but because it's where operational discipline gets exercised. Closes: GRO-848 surface 2. Effort: L.

**T-3: WhoAmI RPC.** `GET /v1/me` with bearer auth. Response shape: `{id, email, name, first_name, last_name, phone, picture_*, system}`. Latency budget p99 < 50ms (warm). AtlasView caches per JWT `jti` for 60s, so the endpoint can be Postgres-backed without a hot-path Redis layer. Closes: GRO-848 surface 3. Effort: S.

**T-4: Contract test fixtures.** Shared test-vector repo for cross-service contract tests — fixtures for happy path, expired token, bad audience, bad issuer, bad signature, mid-rotation request hitting old vs new key. Lives in either Ruptiv repo or a shared `ruptiv/identity-contract` repo. Per-platform contract test runners (Go side at `internal/identity/contract_test.go`, AtlasView side wherever they prefer). The contract tests are the ratchet that keeps the two services from drifting. Closes: GRO-848 contract-test-home open question. Effort: M.

### Wave 2 — Counsel/brand carryover (gated, not blocking)

**T-R: LICENSE entity swap.** Replace `GrowDirect LLC` with whatever the counsel decision lands on (Ruptiv Inc. / Ruptiv Holdings / TBD). Update LICENSE file, package headers if any reference the entity, README. Re-run any fingerprinting / audit dependent on the prior name. Decision lands from counsel; engineering work is ~30 min once the name is known. Closes: HANDOVER B1. Effort: S.

**T-S: Brand callout sweep.** External-facing surfaces (UI strings, OpenAPI discovery doc, runbook footers, error messages) read Ruptiv-owned. Square OAuth dashboard footer reads "Ruptiv" not "GrowDirect LLC" (Sprint 2 already updated GitHub link to `ruptiv/canary`). Needs the destination-domain decision (`canary.ruptiv.com` is the working assumption). Closes: HANDOVER B4 + R7 + R8. Effort: M.

**T-T: Dev infra naming sweep.** Docker image names, compose service names, helm chart names, build-pipeline scripts — anything carrying `growdirect-llc` or `growdirect`. ~25 files. Mechanical once Ruptiv conventions are confirmed (kebab-case `ruptiv-canary-gateway` vs camelCase `RuptivCanaryGateway` etc.). Closes: HANDOVER R2. Effort: M.

**T-U: Runbook + cloudbuild + mirror scrub.** Runbooks reference GrowDirect domain names, internal Slack channels, ops contacts. Cloud Build YAML references the GrowDirect GCP project. Mirror script (already deleted in T-A) needs follow-up grep to confirm no callers. Needs Ruptiv ops conventions on Slack channel names, paging rotation, etc. Closes: HANDOVER B2 + R3 + R4 + R5 + R6. Effort: M.

### Wave 3 — Code health backlog (deferred from Sprint 2)

**T-X: GRO ticket reference cleanup.** 252 `GRO-NNN` references across ~80 Go comments. These are scaffolding from the implementation phase ("GRO-832 wired the onboarding flow", "Loop 3 W7 introduced the protocol portal"). The receiving team doesn't know what GRO-832 is — these are GrowDirect Linear ticket numbers, not durable comments. Sweep removes the references; the *intent* of the comment, where worth keeping, gets rewritten to describe what the code does, not what ticket added it. High-volume mechanical — easiest with a Python script that flags every `GRO-` for human review. Closes: deferred from Sprint 2. Effort: L.

**T-Y: Devops console phase-1 cleanup.** Remove the `PythonPriorArt` field on the catalog struct (referenced the frozen Python prototype). Drop `Brain/wiki/cards/...` paths from the catalog config (Brain content stays in GrowDirect, doesn't ship to Ruptiv). Rename `BodyTODO` → `Status` for clarity. Closes: HANDOVER R9 + R-tier N2 + N4. Effort: S.

**T-Z: Sprint terminology sweep.** 333 Go comments reference `Loop N`, `Wave A`, `Phase B.2`, `Sub 1/2/3` — internal Canary build vocabulary that has no meaning to a receiving engineer. Sweep removes references where the surrounding comment is about the code; rewrites where the comment explains a still-relevant boundary. Same pattern as T-X — mechanical with human review. Closes: deferred from Sprint 2. Effort: L.

### Wave 4 — AtlasView surfaces 4-6 (stretch — only if Wave 1 lands clean)

**T-5: Per-org SSO config admin endpoints.** Admin-only `POST /v1/sso/config` / `PUT /v1/sso/config/{org_id}` / `DELETE /v1/sso/config/{org_id}`. Stores Microsoft Entra OIDC config per Organization (keyed on `org_id` UUID v4 shared with AtlasView). Identity service runs the OIDC dance on `/auth/sso/callback`, mints AtlasView-audience JWTs. Closes: GRO-848 surface 4. Effort: M.

**T-6: JIT provisioning + audit event publish.** On first successful SSO login, create a Person record attached to the Organization the SSO config belongs to. Default `user_type` set per config. Audit event published to `audit.identity` topic (Pub/Sub) so AtlasView and downstream observers see the provisioning. Closes: GRO-848 surface 5. Effort: S.

**T-7: Operational SLA hardening.** Availability ≥99.9%, latency 5ms warm verify / 50ms WhoAmI. Revocation semantics: refresh-token revoked → access valid until `exp` (or introspection topic if shorter-than-`exp` revocation is needed). Health check endpoint that reports both keys' status during rotation. Closes: GRO-848 surface 6. Effort: M.

## Open decisions (board / counsel before sprint kickoff)

The same five decisions Sprint 2 listed remain open. Sprint 3 inherits the ones that didn't clear:

1. **LICENSE entity name** — counsel-gated. T-R blocked.
2. **Destination domain.** `canary.ruptiv.com` is the working assumption. T-S blocked.
3. **Brand-naming tier.** Sprint 2 defaulted to Tier 1 (module path only). Sprint 3 defaults to "carry the same posture" — Tier 2/3 requires a separate decision and changes T-S/T/U scope significantly.
4. **Ruptiv ops conventions.** Slack channel names, paging rotation, GCP project naming. T-T and T-U need this.
5. **JWKS rotation cadence.** 90-day default? 30-day? Per the operational SLAs in surface 6. Affects the operational runbook attached to T-2.

## Compliance posture after Sprint 3

After T-1, T-2, T-3, T-4 land:

- **SOC 2 Type II CC6.1 (logical access)** — federated SSO with revocation closes the "centralized identity provider" control. The audit observation window (which began conceptually after Sprint 2's auth-surface lockdown stabilized) gains a real federated story.
- **OAuth 2.1 / OIDC compliance** — the JWKS endpoint + JWT shape conforms to RFC 7517 and OIDC Core. AtlasView consumes this contract; future enterprise SSO consumers (the Phase 4 SaaS tier per the platform thesis) inherit it without re-architecture.
- **Tenant isolation audit trail** — combined with Sprint 2's `audit.ListByMerchant` clamp (T-C) and DLQ tenant fence (T-H), every cross-service call now leaves an audit-loggable claim trail. Closes the SOC 2 CC7.2 chain end-to-end.

## What's NOT in Sprint 3

- **GRO-846 (Neo4j MDM read-adjunct)** — post-handover. Trigger conditions on the ticket's scheduling comment.
- **GRO-847 (SQLite-on-device offline)** — Sprint 4+. Mobile surface (W14 / [GRO-833](https://linear.app/growdirect/issue/GRO-833)) stability is the prerequisite.
- **Phase 2 manifest backfill** ([GRO-836](https://linear.app/growdirect/issue/GRO-836) sub-tickets) — the 137 unaccounted endpoints stay unaccounted. Sprint 4+.
- **W-series Phase 3 UI deepening** — turning "TODO" service bodies in `/devops/<svc>` shells into real operator workflows. Sprint 5+.
- **CRB endpoint-library publish** (T2.36) — depends on the AtlasView contract closing first; could land late Sprint 3 if there's room.
- **New product features.** Sprint 3 is integration readiness + brand cleanup + code health.

## Sprint 3 success criteria

1. AtlasView's middleware implementation can run against canary.go's identity service end-to-end. Login → JWT mint → AtlasView verifies via JWKS → WhoAmI returns the Person record.
2. JWKS rotation tested end-to-end: publish a new key, both keys serve verification for ≥24h overlap, AtlasView's JWKS cache picks up the new key on TTL expiry without a restart.
3. Contract test fixtures live in a shared repo, both services run the test vectors in CI, fixtures are versioned.
4. Brand surfaces (LICENSE, runbooks, cloudbuild, dev infra naming) read Ruptiv-owned where the decisions have unblocked. Where decisions remain gated, no ticket has been forced through with a guess.
5. `grep -rn "GRO-" CanaryGo/` returns refs only in commit messages and decision docs (where they're load-bearing). No `GRO-NNN` left in active Go code comments.
6. `grep -rn "Loop\|Wave\|Sub [0-9]\|Phase [A-Z]\." CanaryGo/internal/ CanaryGo/cmd/` returns no internal-vocabulary references in code.
7. The board package shipping at the end of Sprint 3 includes a one-page "AtlasView ↔ canary.go integration" README with a sequence diagram, fixture table, and runbook link.

That last criterion is what makes Sprint 3 legible. Sprint 2 made the auth surface defensible; Sprint 3 makes the integration story tellable.
