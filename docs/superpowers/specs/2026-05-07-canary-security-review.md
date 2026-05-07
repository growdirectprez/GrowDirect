# CanaryGo — Security Audit (sprint 2 input)

## Executive summary

The CanaryGo gateway has an asymmetric security posture: the protocol-edge surfaces (HMAC webhook ingestion, evidence chain integrity, RS256 JWT validation, argon2id API keys, per-tenant Square OAuth state CSRF) are well-engineered and would survive a careful review on their own. The application surface above them — every route mounted by `internal/web` plus several `/v1/protocol/*` and `/admin/*` endpoints — is wide open. `tenantIDFromCtx` is hard-coded to return `uuid.Nil` (CanaryGo/internal/web/handler.go:3420), the gateway mounts the entire UI without any auth middleware, the casemgmt service trusts a `?tenant_id=` query parameter as the tenancy boundary (CanaryGo/internal/casemgmt/handler.go:237), the Square demo session cookie is unsigned plaintext UUID, the `/admin/audit` page returns the global audit log to anyone who knows the URL, and `/v1/protocol/evidence/{event_hash}` is unauthenticated and discloses raw payloads with `merchant_id` attached. Top three risks: (1) the un-gated web UI plus `tenantIDFromCtx → uuid.Nil` collapse the multi-tenant boundary across the entire merchant-facing app, (2) `/admin/audit` and `/v1/protocol/evidence/*` leak cross-tenant data to unauthenticated callers, (3) the demo `/dashboard` cookie can be forged to any merchant UUID. Nothing should onboard a real customer until GRO-769 lands and the protocol-evidence + admin surfaces gain authentication. Compliance posture (PCI Service Provider, SOC 2, GDPR) is currently incompatible with the audit-log immutability claim — the database-level append-only trigger documented in CLAUDE.md does not exist on `app.audit_log` (verified in deploy/schema/01_app_foundation.sql:300–327).

## Findings by severity

### Critical (5)

#### C1. Web UI handlers all run as the "nil tenant" — every page is reachable unauthenticated and returns whatever data lives at `merchant_id = uuid.Nil`

- **Location**: `CanaryGo/internal/web/handler.go:3420`, mounted via `cmd/gateway/main.go:260` with no middleware
- **Evidence**:
  ```go
  // tenantIDFromCtx extracts the tenant UUID from the request context.
  // Returns uuid.Nil until auth middleware (GRO-769) is wired.
  func tenantIDFromCtx(ctx context.Context) uuid.UUID {
      // TODO(GRO-769): replace with identity.TenantIDFromCtx(ctx)
      return uuid.Nil
  }
  ```
  Forty-plus call sites (handler.go:532, 599, 659, 708, 734, 784, 819, 860, 900, 921, 971, 1037, 1140, 1237, 1292, 1360, 1518, 1601, 1667, 1736, 1788, 1835, …) read `tenantID := tenantIDFromCtx(ctx)` and pass it straight to `Store.GetByID(ctx, tenantID, id)`, `Store.List(ctx, ListFilters{TenantID: tenantID})`, etc.
- **Threat model**: Unauthenticated external attacker. The UI is bound to `/dashboard`, `/alerts`, `/cases`, `/transactions`, `/customers`, `/employees`, `/settings/*`, `/admin/*` — none of these routes are wrapped in `auth.BearerMiddleware` or `tenant.RequireMerchant`. Anyone who reaches the gateway hostname (a public HTTP listener, currently only firewalled at the edge) can `curl /dashboard` and the handler will run.
- **Impact**: Today the result is "leaks records with `merchant_id = NULL/uuid.Nil`", which is bounded only by what the seed scripts and tests have written under the nil tenant. As real merchants onboard, the LP settings POST routes (`internal/web/handler_lp_settings.go:115–161`) accept writes attributed to whatever tenant the seed/import places under nil and any future migration that backfills missing merchant_ids becomes a horizontal-escalation footgun. More concretely: an attacker can also POST to `/cases/hawk` (handler.go:281), `/admin/hierarchy` (handler.go:388), and the ten `/settings/*/{id}/delete` paths and silently deface the nil-tenant view. Until GRO-769 lands, every page is "anonymous mode + unrestricted writes".
- **Remediation**: Land GRO-769 — wrap the entire `web.Handler.Mount` call in a session-cookie auth middleware that calls `identity.InjectClaims`, and replace `tenantIDFromCtx` with `identity.ClaimsFromContext(ctx).TenantID`. While that's in flight, mount a temporary deny-all middleware that returns 503 on every UI route except `/web/static/*` and `/health`, gated behind an `ENABLE_WEB_UI=1` env toggle. Reject `uuid.Nil` at every Store entrypoint with a defensive `if tenantID == uuid.Nil { return ErrUnauthorized }` so a future regression cannot reproduce the same silent-leak shape.
- **Sprint estimate**: L. GRO-769 itself is the larger ticket; the defensive `uuid.Nil` rejection across stores is M.

#### C2. `casemgmt` HTTP API trusts the `?tenant_id=` query parameter as the tenancy boundary

- **Location**: `CanaryGo/internal/casemgmt/handler.go:237–253`, mounted by `cmd/case/main.go:51–64`
- **Evidence**:
  ```go
  func tenantFromQuery(w http.ResponseWriter, r *http.Request) (uuid.UUID, bool) {
      v := r.URL.Query().Get("tenant_id")
      if v == "" {
          v = r.URL.Query().Get("merchant_id")
      }
      if v == "" {
          writeError(w, http.StatusBadRequest, "missing_tenant",
              "tenant_id (or merchant_id) query parameter is required")
          return uuid.Nil, false
      }
      id, err := uuid.Parse(v)
      ...
  ```
  Every state-mutating handler in the file (`list`, `get`, `appendAction`, `appendEvidence`, `closeCase`) calls this helper to derive the tenant context; the API-key middleware that sits in front of it (`identity.APIKeyMiddleware`, cmd/case/main.go:59) authenticates the caller but the handler ignores `claims.TenantID` and uses the query-string value verbatim.
- **Threat model**: Authenticated low-privilege tenant A holding a valid API key. Tenant A calls `GET /v1/cases/<case-id>?tenant_id=<tenant-B-uuid>`; the SQL store at `internal/casemgmt/store.go:101` runs `WHERE merchant_id = $1 AND id = $2` against tenant B's UUID and returns tenant B's case if the case-id collides on a UUIDv4 guess (~negligible) or if the attacker has obtained a case-id from another channel (timing, log scrape, API enumeration). The append/close paths let tenant A *write* into tenant B's case row.
- **Impact**: Authenticated cross-tenant read+write on the case-management spine. Cases carry investigator notes, evidence references, and resolution dispositions — direct exposure of sensitive LP investigation data and write-side tampering of audit-relevant records.
- **Remediation**: Replace `tenantFromQuery` with `claims, ok := identity.ClaimsFromContext(r.Context()); if !ok { 401 }` and use `claims.TenantID`. If a platform-scope key needs to act on behalf of a tenant, accept the body's `tenant_id` only after `identity.AssertBodyTenantMatches` (already present at `internal/identity/context.go:100`) confirms it matches the authenticated tenant. Add a regression test that calls each handler with a mismatched `tenant_id` query and asserts 403.
- **Sprint estimate**: S. The plumbing already exists in `internal/identity`.

#### C3. `/v1/protocol/evidence/{event_hash}` is unauthenticated and discloses cross-tenant payload + merchant_id

- **Location**: `CanaryGo/internal/protocol/evidence/handler.go:55–113`, mounted at `cmd/gateway/main.go:171` with the comment "read-only, mounted outside the audit group"
- **Evidence**:
  ```go
  func (h *Handler) Mount(r chi.Router) {
      r.Get("/v1/protocol/evidence/{event_hash}", h.ServeHTTP)
  }
  ...
  const q = `
      SELECT event_id, event_hash, chain_hash,
             COALESCE(prev_chain_hash, ''),
             source_code, merchant_id, ingested_at, raw_payload
      FROM protocol.evidence
      WHERE event_hash = $1
  `
  ```
  No middleware on the route group. Response includes `merchant_id` and `raw_payload` (the full inbound webhook body).
- **Threat model**: Unauthenticated attacker. Bilateral verification is the patent's selling point for *cryptographic* trust — knowing a hash should let any party verify a record exists. The current implementation goes much further by returning the merchant_id and the entire raw payload. An attacker who learns or guesses a 64-char event_hash (logged externally, leaked via timing, harvested from the source network's outbound logs, or the source-network's own publicly visible request-id) can read another merchant's POS payloads.
- **Impact**: Direct PII / transaction-data exfil. POS payloads carry transaction line items, customer associations, and payment metadata. Cross-tenant read by an unauthenticated party. Material PCI Service Provider blocker (Phase 4) and GDPR Article 32 incident.
- **Remediation**: Two options. (a) Strip `merchant_id` and `raw_payload` from the public evidence response — return only `event_hash`, `chain_hash`, `prev_chain_hash`, `ingested_at` so the chain is verifiable without leaking content; gate the full record behind `identity.APIKeyMiddleware` with a tenant scope check (`row.MerchantID == claims.TenantID`). (b) Same as (a) but require an HMAC over `event_hash` keyed by the per-merchant secret to prove the caller is entitled to ask. Pick (a) for sprint 2; (b) is a follow-up.
- **Sprint estimate**: M.

#### C4. `/admin/audit` returns the global audit log (every merchant's rows) to any unauthenticated caller

- **Location**: `CanaryGo/internal/web/handler_w9.go:27–58`, mounted at `internal/web/handler.go:381`
- **Evidence**:
  ```go
  if h.deps.AuditReader != nil {
      ctx := r.Context()
      rows, err := h.deps.AuditReader.ListByMerchant(ctx, audit.ListFilters{
          SourceCode: source,
          Action:     action,
          Limit:      limit,
      })
  ```
  `ListFilters.MerchantID` is omitted, so the SQL at `internal/protocol/audit/audit.go:319–342` skips the `AND merchant_id = $N` clause and selects every audit row up to limit 500 (default 100). The route is bound to `r.Get("/admin/audit", h.adminAuditPage)` with no middleware — the `IsAdmin` flag (handler.go:84) is set on `UserData` but never checked in any handler; `stubUser()` at handler.go:2762 returns `IsAdmin: false` unconditionally and the result is rendered into the page, not used as a guard.
- **Threat model**: Unauthenticated attacker GETs `/admin/audit` and reads the cross-tenant audit log including action, resource, source_code, payload_digest (sha256 of inbound payload), and merchant_id. The `ip_address` column is also surfaced indirectly through the row scan.
- **Impact**: Cross-tenant disclosure of system activity, request volumes per merchant, action timing, and partial payload fingerprints (digest enables targeted enumeration if an attacker has the original payload). Also reveals which merchants are integrated with which source networks (Square, RapidPOS, etc.) — a competitive-intelligence leak. PCI Service Provider audit-trail integrity claim is broken.
- **Remediation**: Mount the `/admin/*` route group inside an `auth.BearerMiddleware` that calls a new `RequireAdmin(claims)` predicate (true when `claims.TenantID` resolves to a row in `app.users` with `is_admin = true` *and* `claims.AuthMethod == identity.AuthMethodJWT` so API keys can't escalate). Plumb `claims.TenantID` into the `ListByMerchant` call so a non-platform admin sees only their tenant's rows. Add a 403 path test.
- **Sprint estimate**: M (depends on the user-admin model being decided; plug-in `RequireAdmin` against a config-driven allowlist of UUIDs as a stop-gap).

#### C5. Square demo session cookie is an unsigned plaintext UUID — forge it to any merchant_id and hit `/dashboard`

- **Location**: `CanaryGo/internal/squareauth/handler.go:135–145, 232–242`
- **Evidence**:
  ```go
  http.SetCookie(w, &http.Cookie{
      Name:     sessionCookieName,           // "demo_merchant"
      Value:    internalMerchantID.String(), // raw UUID, no MAC
      Path:     "/",
      MaxAge:   sessionMaxAge,
      HttpOnly: true,
      Secure:   r.TLS != nil || r.Header.Get("X-Forwarded-Proto") == "https",
      SameSite: http.SameSiteLaxMode,
  })
  ...
  func (s *Service) merchantFromCookie(r *http.Request) (uuid.UUID, bool) {
      c, err := r.Cookie(sessionCookieName)
      if err != nil || c.Value == "" {
          return uuid.Nil, false
      }
      id, err := uuid.Parse(c.Value)
      ...
  }
  ```
  No HMAC, no signed value, no JWT — the cookie is the merchant_id verbatim. The dashboard handler at handler.go:150 reads it, `LoadToken(ctx, mID)` (squareauth.go:303) reads `app.pos_tenant_credentials` keyed by that ID, decrypts the OAuth token, and uses it to call Square on behalf of "that" merchant.
- **Threat model**: Any user who has connected Square at least once knows their own internal merchant ID is `uuid.NewSHA1(deriveDemoMerchantID-namespace, "square:"+squareMerchantID)` — derivation is in squareauth.go:357 and the namespace is hard-coded — but more importantly, an attacker who can guess or harvest *any* internal merchant_id (via logs, the audit page from C4, the evidence endpoint from C3, or simply by enumerating UUIDv5 over a list of Square merchant IDs) can set `Cookie: demo_merchant=<victim-uuid>` and load `/dashboard` to see the victim's Square merchant data, locations, and recent payments — including last-4 of card.
- **Impact**: Cross-tenant takeover of the Square demo dashboard. Even though the demo is sandbox-only by default, the same code path will run in production once `SQUARE_ENVIRONMENT=production` flips. PCI implication: card last-4 is rendered server-side in the dashboard template (handler.go:372), and the rendered HTML will leak to whoever forges the cookie.
- **Remediation**: Sign the cookie. Either issue a short-lived JWT (HS256 keyed by a new `DEMO_SESSION_SECRET`, claims `{sub: merchant_id, exp}`) or use `gorilla/securecookie`'s authenticated-encryption pattern. Reject any cookie value that doesn't validate. While in flight, set `Secure: true` unconditionally (the current ternary lets the cookie ride over plain HTTP if the request is HTTP and `X-Forwarded-Proto` is missing — Cloudflare/GLB usually set the header but in dev or behind a misconfigured proxy this defaults to insecure transport).
- **Sprint estimate**: S.

### High (6)

#### H1. `POST /v1/protocol/namespace` accepts caller-supplied `owner_id` with no auth — anyone can claim any name on behalf of any owner

- **Location**: `CanaryGo/internal/protocol/namespace/handler.go:40–113`, mounted at `cmd/gateway/main.go:178` outside any auth middleware
- **Evidence**: The handler reads `req.OwnerID` (the wallet UUID the caller claims to be) directly from the JSON body and writes it into the namespace registration row. There's no proof-of-ownership step (sign the name with a key registered to `owner_id`), no HMAC, and no API-key gate.
- **Threat model**: Unauthenticated attacker POSTs with any `owner_id`, locking namespace claims for legitimate owners (denial-of-service on the `.jeffe` ordinals naming surface) or impersonating named owners on the inscribed namespace.
- **Impact**: Namespace squatting + impersonation. Patent claim integrity for Node identity is undermined.
- **Remediation**: Require API-key auth on the POST and resolve `owner_id` from the authenticated tenant rather than the body, OR require a secp256k1 signature over `(name, owner_id, network)` keyed by the owner's ed25519/secp256k1 wallet key.
- **Sprint estimate**: M.

#### H2. State-mutating `/settings/*` POSTs accept unauthenticated form submissions and have no CSRF defense

- **Location**: `CanaryGo/internal/web/handler_lp_settings.go:102–162` and `CanaryGo/internal/web/handler.go:281` (`r.Post("/cases/hawk", ...)`), `:388` (`r.Post("/admin/hierarchy", ...)`)
- **Evidence**: Each LP-settings POST handler calls `r.ParseForm()` and writes to `AllowListStore.Create`/`Delete`. No `X-CSRF-Token` validation, no `Origin` / `Referer` check, no SameSite-strict cookie. There is no auth middleware in front of the route group — see C1.
- **Threat model**: Unauthenticated attacker can directly POST. Once GRO-769 lands and these routes become session-authenticated, a malicious site visited by an authed merchant can submit the form via cross-origin POST (default cookie SameSite=Lax allows top-level POSTs from external pages with `<form action="https://canary/.../delete">`).
- **Impact**: Today: anonymous mutation of LP settings, alert routing, and hierarchy as nil-tenant. After GRO-769: cross-site request forgery against authenticated merchants — silent allow-list pollution, alert-routing redirection (alerts diverted to attacker-controlled emails), and hierarchy modification.
- **Remediation**: Add CSRF middleware (e.g. `gorilla/csrf` or chi-csrf) keyed by the session secret; emit a token via `csrf.TemplateField(r)` in every form template; reject POSTs without a matching token. Pair with C1's auth middleware. Use SameSite=Strict for the post-GRO-769 session cookie.
- **Sprint estimate**: M.

#### H3. `pgx/v5 v5.6.0` carries two known CVEs — CVE-2026-33815 + CVE-2026-33816 — fixed in v5.9.0

- **Location**: `CanaryGo/go.mod:11` (`github.com/jackc/pgx/v5 v5.6.0`)
- **Evidence**: `govulncheck` output:
  ```
  Vulnerability #1: GO-2026-4772
      CVE-2026-33816 in github.com/jackc/pgx
    Module: github.com/jackc/pgx/v5
      Found in: github.com/jackc/pgx/v5@v5.6.0
      Fixed in: github.com/jackc/pgx/v5@v5.9.0
  Vulnerability #2: GO-2026-4771
      CVE-2026-33815 in github.com/jackc/pgx
      Found in: github.com/jackc/pgx/v5@v5.6.0
      Fixed in: github.com/jackc/pgx/v5@v5.9.0
  ```
  Govulncheck reports the project does not currently call the affected symbols, but the dependency is in the build.
- **Threat model**: Future code added to the project may invoke the affected pgx paths (specific issue details require pulling the advisory). Any reachable invocation immediately becomes exploitable.
- **Impact**: Latent risk; closing it costs one line in go.mod plus a regression test pass.
- **Remediation**: `go get github.com/jackc/pgx/v5@v5.9.0 && go mod tidy && make test`. Add a govulncheck step to CI so further drift is caught.
- **Sprint estimate**: S.

#### H4. Audit log is not append-only — `app.audit_log` lacks the UPDATE/DELETE blocking trigger documented in CLAUDE.md

- **Location**: `CanaryGo/deploy/schema/01_app_foundation.sql:300–327`
- **Evidence**: The schema for `app.audit_log` defines columns and indexes but no trigger. The append-only triggers exist for `protocol.evidence` (deploy/schema/11_protocol.sql:42–53) but not for `app.audit_log`. The CanaryGo CLAUDE.md and the audit middleware comments both treat `app.audit_log` as the gateway audit trail; integrity claim is unbacked at the DB layer.
- **Threat model**: A compromised application credential or DB-admin role can rewrite audit history. PCI DSS Requirement 10 (audit trail integrity), SOC 2 CC7.2, and ISO 27001 A.8.15 / A.5.28 each require demonstrable tamper-resistance.
- **Impact**: The "evidentiary rail" claim — central to platform thesis — is unbacked for the application audit log. Regulators / auditors will write this up.
- **Remediation**: Add a migration mirroring the `protocol.evidence` pattern:
  ```sql
  CREATE OR REPLACE FUNCTION app.no_mutate_audit_log() RETURNS trigger LANGUAGE plpgsql AS $$
  BEGIN
      RAISE EXCEPTION 'app.audit_log is append-only — % blocked', TG_OP;
  END $$;
  CREATE TRIGGER audit_log_no_update BEFORE UPDATE ON app.audit_log
      FOR EACH ROW EXECUTE FUNCTION app.no_mutate_audit_log();
  CREATE TRIGGER audit_log_no_delete BEFORE DELETE ON app.audit_log
      FOR EACH ROW EXECUTE FUNCTION app.no_mutate_audit_log();
  CREATE TRIGGER audit_log_no_truncate BEFORE TRUNCATE ON app.audit_log
      FOR EACH STATEMENT EXECUTE FUNCTION app.no_mutate_audit_log();
  ```
  Pair with a partition + cold-archive plan if retention growth is a concern.
- **Sprint estimate**: S.

#### H5. `/v1/webhooks/dlq` admin endpoints surface every merchant's DLQ to any caller holding the `dlq:read` scope

- **Location**: `CanaryGo/cmd/gateway/admin.go:48–113`
- **Evidence**: The `list` and `get` handlers check `RequireScope("dlq:read")` and accept an *optional* `merchant_id` query param to filter — but if a tenant-scoped API key omits the param, the handler returns rows across all merchants:
  ```go
  if v := q.Get("merchant_id"); v != "" {
      id, err := uuid.Parse(v)
      ...
      f.MerchantID = &id
  }
  ```
  The `webhook.DLQ.List` SQL (visible in `internal/webhook/dlq.go`) only filters when `MerchantID` is non-nil. The middleware authenticated the API key but the handler never reads `claims.TenantID` to constrain the result.
- **Threat model**: Authenticated tenant A with a `dlq:read`-scoped API key calls `GET /v1/webhooks/dlq` without `?merchant_id=` and receives tenant B's failed/replayable webhook payloads — including the original raw body stored in the DLQ row.
- **Impact**: Cross-tenant payload disclosure for the failed-delivery channel. Same severity shape as C3 but gated behind an API key.
- **Remediation**: In each handler, before executing the query, read `claims, _ := identity.ClaimsFromContext(r.Context())` and force `f.MerchantID = &claims.TenantID` for tenant-scoped keys (i.e. `claims.TenantID != uuid.Nil`). Platform-scope keys (TenantID = uuid.Nil) may pass an explicit `merchant_id` filter; otherwise return only their tenant's rows.
- **Sprint estimate**: S.

#### H6. `cdn.tailwindcss.com` loaded over public CDN with no SRI — supply-chain MITM on every demo page render

- **Location**: `CanaryGo/internal/squareauth/handler.go:259, 297` and any other demo template loading the same script
- **Evidence**:
  ```html
  <script src="https://cdn.tailwindcss.com"></script>
  ```
  No `integrity=` (SRI) attribute, no Content Security Policy header set on the response.
- **Threat model**: A compromised CDN edge or an attacker with TLS interception capability against the user's path to the CDN can inject arbitrary JS into every demo page load.
- **Impact**: Full takeover of the demo session (read cookies subject to SameSite, post arbitrary forms, exfil session state). For the Anthropic-facing demo specifically, a compromised render is reputationally severe even if no real merchant data is exposed.
- **Remediation**: Either bundle Tailwind into the embedded `static/` tree (build step) or add `integrity="sha384-..." crossorigin="anonymous"` to the CDN script tag. Add a `Content-Security-Policy: default-src 'self'; script-src 'self' 'sha256-...' https://cdn.tailwindcss.com` header to the demo handler.
- **Sprint estimate**: S.

### Medium (5)

#### M1. LNURL session JWT uses HS256 with a *random* ephemeral secret when `LNURL_JWT_SECRET` is unset — every restart invalidates every issued session, but more importantly, the prod fail-open is silent

- **Location**: `CanaryGo/cmd/gateway/main.go:442–470`
- **Evidence**:
  ```go
  if secretHex != "" {
      decoded, err := hex.DecodeString(secretHex)
      if err != nil || len(decoded) != 32 {
          logger.Warn("LNURL_JWT_SECRET invalid; generating ephemeral random key", ...)
      } else {
          copy(secret, decoded)
      }
  } else {
      _, _ = cryptoRand.Read(secret)
      logger.Warn("LNURL_JWT_SECRET not set; using ephemeral random key (dev only)")
  }
  ```
  Same shape for `VALIDATOR_SECRET`.
- **Threat model**: Operator deploys to prod with the env var unset. The gateway boots, logs a `warn` (operators rarely block on warns), serves traffic, and silently rotates the JWT secret on every restart — every wallet logged in mid-restart sees its session revoked. Worse, if a deploy pipeline restarts pods more often than expected, sessions become unusable in production.
- **Impact**: Silent degradation, not a direct disclosure. But the same fail-open pattern is one bug away from "ephemeral random key gets reused across instances thanks to a future global var" or "key gets logged for debugging".
- **Remediation**: When `LNURL_REQUIRE_SECRET=1` (or `ENV=production`) and the env var is missing/invalid, `logger.Fatal` instead of `logger.Warn` — same pattern as `SECRET_BACKEND_REQUIRE_SM` for the secrets resolver. Document the env var as required in deployment runbooks.
- **Sprint estimate**: S.

#### M2. Logout is a cookie clear, not a server-side session revocation — JWTs and demo cookies remain valid until expiry

- **Location**: `CanaryGo/internal/squareauth/handler.go:217–228`, `internal/auth/jwt.go:21–33`
- **Evidence**: `handleDisconnect` only deletes the token row and clears the cookie; nothing invalidates a session at the server side. The JWT path (auth/jwt.go) has no revocation list — `TokenHash` exists at jwt.go:54 but is unused. There is no Valkey-backed allow/deny list keyed by token hash.
- **Threat model**: Token theft followed by logout. The user clicks "Disconnect" believing they've ended the session, but a stolen JWT or cookie copy continues to authenticate until natural expiry (24h for LNURL JWTs, 7 days for the demo cookie).
- **Impact**: Standard logout-doesn't-revoke gap. Failure mode for SOC 2 CC6.3.
- **Remediation**: Add a Valkey-backed revocation list keyed by `TokenHash(token)` with TTL = JWT TTL. Bearer middleware checks the deny list before accepting; logout puts the token hash on the list.
- **Sprint estimate**: M.

#### M3. No request-body size cap on UI POSTs — only `MaxBytesReader(1<<20)` on protocol webhook; LP settings forms read with `r.ParseForm()` only

- **Location**: `CanaryGo/internal/web/handler_lp_settings.go:104` (`r.ParseForm()`)
- **Evidence**: `r.ParseForm()` honors Go's default `http.DefaultMaxHeaderBytes` and the request body is bounded only by chi's defaults (no explicit cap). The protocol-webhook path correctly caps at 1 MiB (`internal/protocol/webhook/handler.go:47`); the UI does not.
- **Threat model**: Memory-exhaustion DoS by sending an enormous POST body to `/settings/*`, `/cases/hawk`, `/admin/hierarchy`, `/auth/square/disconnect` — the handler will buffer the entire body before validating.
- **Impact**: Single-instance DoS; recoverable.
- **Remediation**: Wrap every `r.Body` read with `http.MaxBytesReader(w, r.Body, ...)` at a sensible cap per route (32 KiB for form posts, 1 MiB for evidence uploads). Or add a global `chi/middleware.AllowContentEncoding` + `middleware.RequestSize(64<<10)` at the router root.
- **Sprint estimate**: S.

#### M4. No rate limiting anywhere — neither per-IP, per-tenant, nor per-API-key

- **Location**: Project-wide. `app.api_keys.rate_limit_rpm` exists at `internal/identity/apikey.go:282–288` and is stored on the row, but is never enforced — no `rate_limit_rpm` reader in `APIKeyMiddleware`.
- **Evidence**: Search for `RateLimit` in `internal/identity/`: the column is read in `ListAPIKeysByTenant` (apikey.go:325–339) but never compared to a request count.
- **Threat model**: Credential brute force against the API-key authenticator (which scans all active keys per request — apikey.go:155–202 — meaning each call costs an argon2id verify per row, ~64MB×rows of CPU) is a self-inflicted DoS amplifier. An unauthenticated attacker firing 1000 RPS at `POST /mcp` with an invalid key can trigger a full table scan with argon2id verifies on every row.
- **Impact**: Both DoS amplification and auth-time hot path. Bigger issue at production key counts (the SDD comment at apikey.go:139–144 acknowledges the 10⁴-per-tenant ceiling).
- **Remediation**: Add a per-IP token bucket (chi has `httprate`) on the `/mcp`, `/v1/auth/*`, and `/admin/*` route groups; enforce `rate_limit_rpm` on the API-key middleware via Valkey INCR. Add a key-prefix shard so the lookup doesn't scan every active key — generate plaintext keys with a 4-byte prefix that maps to a hashed-prefix index column, and `WHERE key_prefix = $1` before iterating.
- **Sprint estimate**: M.

#### M5. `LNURL_SCHEME` defaults to `https` but accepts `http` from env — production accidental-downgrade risk

- **Location**: `CanaryGo/cmd/gateway/main.go:460–467`
- **Evidence**: `scheme := os.Getenv("LNURL_SCHEME"); if scheme == "" { scheme = "https" }` — but a deploy that sets `LNURL_SCHEME=http` (e.g. carried over from dev compose) will produce LNURL callback URLs over plain HTTP, which leaks the k1 challenge + signature in transit.
- **Threat model**: Misconfiguration → wallet round-trip over HTTP → MITM steals the signed challenge.
- **Impact**: Wallet signature compromise per affected session.
- **Remediation**: Reject `LNURL_SCHEME=http` when `ENV=production` (or any non-dev signal). `logger.Fatal` if mismatched.
- **Sprint estimate**: S.

### Low (4)

#### L1. `requestLogger` (cmd/gateway/main.go:474–487) logs only method, path, status, and bytes — it does NOT log secrets, but adding any future field that includes headers (`r.Header.Get("Authorization")` etc.) will silently leak

- **Location**: `CanaryGo/cmd/gateway/main.go:474–487`
- **Remediation**: Document a logging policy in `internal/obs/` and add a regression test that asserts the request log line never includes `password`, `secret`, `key`, `token`, or `Authorization` substrings even on error paths.
- **Sprint estimate**: S.

#### L2. `SECRET_BACKEND=pgx` (default) reads source secrets from a plaintext column — fine for dev, but the code path is identical in prod unless `SECRET_BACKEND_REQUIRE_SM=1` is set

- **Location**: `CanaryGo/cmd/gateway/main.go:359–396`
- **Remediation**: Add a startup check that errors when `ENV=production` and `SECRET_BACKEND != sm`. Same pattern as M1.
- **Sprint estimate**: S.

#### L3. `pendingTokens sync.Map` in LNURL handler has no TTL — abandoned sessions accumulate until process restart

- **Location**: `CanaryGo/internal/auth/lnurl/handler.go:34–39` (the comment acknowledges this)
- **Remediation**: Move `pendingTokens` into Valkey with a 5-minute TTL keyed by k1, so accumulation is bounded and the session is cluster-safe.
- **Sprint estimate**: S.

#### L4. `btcd v0.20.1-beta` and `btcutil v1.0.2` (transitive via the LNURL secp256k1 path) are stale — last release ~2020

- **Location**: `CanaryGo/go.mod:29–31`
- **Remediation**: Move to `github.com/btcsuite/btcd/btcec/v2` directly + `github.com/btcsuite/btcd/btcutil` v1.1.x; drop the standalone `btcutil v1.0.2` dependency. govulncheck didn't flag a CVE today, but the module is well past its sell-by date.
- **Sprint estimate**: S.

### Info (3)

- **I1. JWT validator (RS256, identity/jwt.go) is well-designed**: rejects non-RSA `alg`, requires `kid`, requires `exp`, and validates issuer + audience. Good. Consider adding an explicit `iat` skew tolerance (default 0).
- **I2. HMAC webhook verifier is well-designed**: constant-time compare, dot-byte canonical signed string, replay window + nonce single-use. Per-(merchant, source) secret. Match against the Stripe / Square / GitHub webhook signature designs and you'd find few faults.
- **I3. argon2id API-key hashing is well-designed**: RFC 9106 parameters, salt-per-row, constant-time verify. The full table scan is the scalability concern, not the cryptography.

## Compliance readiness deltas

### PCI Service Provider (Phase 4, ~12–24 months out)

The platform thesis carefully keeps card data out of Canary's flow (pinpad → processor), which is the right architectural call. But the current code state has several findings that are hard NO-GOs for a Service Provider audit even without card data:

- **Audit-trail integrity (Req 10)** — H4 (no append-only trigger on app.audit_log) and C4 (audit log readable unauthenticated) both fail. The protocol.evidence chain is well-designed and would pass on its own, but the application audit log is what regulators will inspect.
- **Network access controls (Req 7, 8)** — C1 (web UI unauthenticated), C2 (casemgmt query-param tenancy), C3 (evidence endpoint), and H5 (DLQ cross-tenant) all fail least-privilege and authorization-by-need-to-know tests.
- **Vulnerability management (Req 6)** — H3 (pgx CVEs) is trivially closeable but currently open.

### SOC 2 Type II

- **CC6 (Logical access)** — C1, C2, C5, H5 all fail "logical access is restricted to authorized users". Type II requires this to hold *over the audit period*, not just at a point in time, so closing them needs to land before the observation window opens.
- **CC7.2 (System monitoring)** — H4 (audit log mutability) is the most material gap. SOC 2 specifically asks about controls that detect tampering with audit records.
- **CC6.3 (User access removal / logout)** — M2 (logout doesn't revoke).

### GDPR / CCPA

- **Article 32 (Security of processing) / CCPA §1798.150** — C3 (unauthenticated payload disclosure including `merchant_id`) is a direct exfil path for personal data, since POS payloads carry customer transaction records that frequently qualify as personal data.
- **Article 30 (Records of processing)** — H4 makes it impossible to attest that audit records are tamper-evident.
- **Cross-border transfer / data minimization** — the evidence endpoint (C3) returns the *raw* payload to anyone who asks; data minimization fails by construction.

## Sprint-2 ticket-shape recommendations

Prioritized; severity rollup in parens.

1. **GRO-769 — wire identity middleware to web UI** (Critical: C1). Scope: replace `tenantIDFromCtx` body with `identity.ClaimsFromContext(ctx).TenantID`; mount `auth.BearerMiddleware` (or session-cookie equivalent) over the `web.Handler.Mount` root; add `if tenantID == uuid.Nil { return ErrUnauthorized }` to every store entrypoint as a defensive belt. Files: `internal/web/handler.go`, `cmd/gateway/main.go`, `internal/auth/middleware.go`, every `internal/<module>/store.go`. Effort: L.
2. **Lock down protocol-evidence and namespace endpoints** (Critical: C3 + High: H1). Scope: Strip `merchant_id` and `raw_payload` from the public `/v1/protocol/evidence/{event_hash}` response or gate the full record behind API-key auth + tenant match; require API-key auth + ownership proof on `POST /v1/protocol/namespace`. Files: `internal/protocol/evidence/handler.go`, `internal/protocol/namespace/handler.go`, `cmd/gateway/main.go`. Effort: M.
3. **Fix casemgmt query-param tenancy** (Critical: C2). Scope: Replace `tenantFromQuery` with `identity.ClaimsFromContext`; add cross-tenant regression tests. Files: `internal/casemgmt/handler.go`, `internal/casemgmt/handler_test.go`. Effort: S.
4. **Sign the Square demo session cookie** (Critical: C5). Scope: Replace plaintext UUID cookie with HS256-signed JWT or `securecookie`; force `Secure: true`. Files: `internal/squareauth/handler.go`. Effort: S.
5. **Gate `/admin/*` behind admin auth + tenant scope** (Critical: C4). Scope: Add `RequireAdmin` predicate; pass `claims.TenantID` into `audit.ListByMerchant`; add 403 path tests. Files: `internal/web/handler.go`, `internal/web/handler_w9.go`. Effort: M.
6. **Add append-only trigger on app.audit_log** (High: H4). Scope: Migration mirroring `protocol.evidence`. Files: `deploy/migrations/031_audit_log_append_only.up.sql` (+ down). Effort: S.
7. **Bump pgx to v5.9.0 + add govulncheck to CI** (High: H3). Scope: One-line `go.mod` bump + new GitHub Action step. Files: `go.mod`, `go.sum`, `.github/workflows/`. Effort: S.
8. **Tenant-scope the DLQ admin endpoints** (High: H5). Scope: Force `f.MerchantID = &claims.TenantID` for tenant-scoped keys. Files: `cmd/gateway/admin.go`. Effort: S.
9. **CSRF + body-size caps on all UI POSTs** (High: H2 + Medium: M3). Scope: Wrap router with chi-compatible CSRF middleware; emit token in templates; cap each POST at 64 KiB unless evidence upload. Files: `internal/web/handler.go`, all template files with forms. Effort: M.
10. **Production-fail-open hardening for env vars** (Medium: M1, M5; Low: L2). Scope: Add `ENV=production`-aware fatals for `LNURL_JWT_SECRET`, `VALIDATOR_SECRET`, `LNURL_SCHEME`, `SECRET_BACKEND`. Files: `cmd/gateway/main.go`. Effort: S.

## What I did NOT review

- **No dynamic/runtime testing**. Findings are static-analysis only — no curl, no fuzzing, no live exploitation against a running instance. Several of the cross-tenant claims (C2, C3, C4, C5, H5) need an integration test to confirm the exact response body shape an attacker would see.
- **No frontend XSS sweep**. I scanned for `template.HTML`, `template.JS`, etc. (zero hits — Go's `html/template` contextual escaping is in force), but didn't render every template against malicious data. A targeted XSS pass on the 70+ templates is worth a half-day.
- **No review of the Python prototype at `Canary/`** per scope.
- **No review of Cove, Angel, or Seacove**.
- **No review of the 28 cmd/* binaries individually** beyond the gateway. Each service binary mounts its own router (`cmd/case/main.go` and `cmd/hawk/main.go` both use `casemgmt`, so C2 affects them too); the other 25 binaries deserve the same handler-level audit pass before any ship to production.
- **No review of CI / deployment manifests** (`deploy/` outside migrations and schema). Production env-var injection, secret rotation, and the GCP Secret Manager integration (`internal/protocol/secrets`) deserve their own review.
- **No review of the OpenAPI spec at `services/canary-protocol/openapi/`** for documentation/reality drift — relevant for partner integrations but not load-bearing for security.
- **No threat model for the L402 / Lightning settlement path** beyond the boot-time secret hygiene. The validate handler's HMAC scheme should get its own pass before that surface goes paid.
- **No SAST tool run beyond `go vet ./...`** (clean) **and `govulncheck`** (two pgx CVEs reported above). Tools like `gosec`, `staticcheck`, and `semgrep` would surface additional findings.
