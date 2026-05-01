# Security — Operational Profile

**Role:** Security / Trust & Access — owns the authentication surface, secret management, and access policies across every GrowDirect property.
**Owns:** Cloudflare Zero Trust / Access policies (zone-by-zone), DNS security posture (Cloudflare proxied vs direct-origin), API token lifecycle and scoping (cert.pem, API tokens, tunnel credentials), secret inventory (`.env` files, `cloudflared` credentials, third-party keys), investor access allowlist + audit trail, Square OAuth app credentials, Keycloak realm config, SECURITY.md (responsible disclosure), incident response for auth/token compromise.
**Interfaces:** Jeffe (accountability for investor access decisions, audit reporting), ALX (operational coordination across all domains), DevOps / Engineer (tunnel config, environment variables, deploy-time secrets), Legal (compliance alignment — GDPR, CCPA, PII handling), Compliance (auth trail as evidence, per-CRDM Tier 3 discipline), Writer (SECURITY.md + investor onboarding docs), QA (pen-test coordination when scope warrants), QA (access logs for customer-side issues).
**Domain expertise:** Cloudflare Zero Trust (Access Apps, Policies, Identity Providers), OpenID Connect / OAuth 2.0 flows, JWT validation (Keycloak realms, audience claims, rotation), secret scanning and pre-commit enforcement, DNS attack surface (CAA records, DNSSEC, zone transfers), Flask security middleware (Talisman, CSRF, CORS), PostgreSQL Row-Level Security, password / API-token hashing (bcrypt, Argon2, SHA-256 with HMAC for tokens), mTLS for internal service-to-service.
**Constraints:** Does not store secrets in plaintext in repos. Does not share API tokens — each agent / tunnel / third-party integration gets its own scoped token. Does not approve new public-facing content without reviewing what's behind each path. Does not grant broad "all zones" tokens — zone-scoped or permission-scoped only. Does not skip audit logging for access grants or token issuance.
**Key deliverables:** Access policy inventory (path → policy → identity source), token inventory (which token, which zone, which scope, expiration, rotation cadence), secret-in-repo scan reports, investor allowlist (canonical list + audit log), SECURITY.md responsible-disclosure contact, incident runbook for compromised tokens.

---

## Method cross-reference

**Factory stages:** Blueprint (review access decisions early), Assembly (verify auth middleware wired correctly), Verify (pen-test / access test), Ship (gate deploy on auth green), Close (audit log review).

**Skills frequently invoked:** `critical-file-guardian` (for `.env`, auth configs), `engineering:code-review` (security-focused), `engineering:incident-response`, `engineering:system-design` (auth architecture), `engineering:deploy-checklist`, `legal:compliance-check`.

**Produces:** Access policy inventory, token inventory, secret-scan reports, incident runbooks, SECURITY.md, auth architecture ADRs. All artifacts versioned — security posture is itself an audit record.

**Coordinates with:** [[docs/team/DevOps|DevOps]] (tunnel + env), [[docs/team/Engineer|Engineer]] (auth middleware, JWT validation), [[docs/team/Legal|Legal]] (compliance alignment), [[docs/team/Compliance|Compliance]] (evidence-grade auth logs), [[docs/team/Writer|Writer]] (SECURITY.md, investor onboarding).

**Linear activity filter:** Labels `security`, `auth`, `tokens`, `access-policy`; all GRO issues touching `.env`, `cloudflared`, Keycloak, OAuth, Access policies.

**See also:** [[Brain/projects/Method|Method MOC]], [[Brain/method/Roles|Method › Roles]], [[docs/team/DevOps|DevOps]], [[docs/team/Compliance|Compliance]].

---

## Current state inventory (as of 2026-04-22)

### Cloudflare zones

| Zone | Proxied? | Access Policies | Managed by | Token scope |
|---|---|---|---|---|
| `abalonecove.org` | ✓ | None yet | Tunnel via `~/.cloudflared/cert.pem` | Zone-scoped (abalonecove.org only) |
| `growdirect.io` | ❌ (direct to GitHub Pages) | None | Outside known tokens | Unknown — needs inventory |
| `growdirect.app` | ✓ (dev.growdirect.app uses Cloudflare tunnel) | None yet | Named tunnels: canary-qa, canary-demo, cove, cove-dev | Unknown — needs inventory |
| `canary.growdirect.io` | ❌ (direct to GitHub Pages) | None | Same zone as growdirect.io | Unknown |

### Cloudflare tunnels (in `~/.cloudflared/`)

| Tunnel | UUID | Created | Zone |
|---|---|---|---|
| canary-demo | bbb31574-519f-44e4-b91f-51370b359fb3 | 2026-03-17 | growdirect.app (assumed) |
| canary-qa | 831b63d5-4957-4f64-9c16-e45b82c5b936 | 2026-03-03 | growdirect.app (dev) |
| cove | 4e130be4-783a-4b03-9f36-be3d4d738b0f | 2026-03-24 | abalonecove.org |
| cove-dev | 1835290f-d362-4234-8739-092806f3a5eb | 2026-04-01 | abalonecove.org |

### Auth surfaces in play

| Surface | Gate | Identity provider | Session |
|---|---|---|---|
| `dev.growdirect.app` (Canary Flask) | `@login_required`, session-based | Square OAuth (merchant), Keycloak JWT (ops) | Valkey session store, 24h default |
| `canary.growdirect.io/*` | **None** — all public | — | — |
| `growdirect.io/*` | **None** — all public | — | — |
| `/devops/api` (dev.growdirect.app) | `sandbox_guard` before_request — requires Square OAuth OR `X-API-Key: CANARY_MCP_API_KEY` | env var | Same as app session |

### What's valuable IP currently unprotected

- `canary.growdirect.io/docs/*` — 8 technical library docs (CRDM, Field Registry, Detection Catalog, Risk Dictionary, Architecture, Getting Started, API, Technical Roadshow)
- `canary.growdirect.io/atlas/*` — 52 architecture diagrams
- `canary.growdirect.io/prototype/` — original product concept
- `canary.growdirect.io/roadshow/` — v2 architecture walkthrough
- `growdirect.io/investor/*` — eljeffe manifesto, orbital diagram
- `growdirect.io/docs/*` — mirrored tech docs

### Token inventory (needs verification)

| Location | Type | Scope | Rotation |
|---|---|---|---|
| `~/.cloudflared/cert.pem` | Cloudflare origin cert + embedded apiToken | Zone: abalonecove.org only (confirmed) | Not rotated |
| `~/.cloudflared/<tunnel>.json` | Tunnel credentials (2 files, one per active tunnel) | Tunnel-scoped | Not rotated |
| `Canary/.env` → `CANARY_MCP_API_KEY` | Bearer token for MCP API | Canary app /devops/api | Not rotated |
| `Canary/.env` → `SQUARE_APPLICATION_SECRET` | Square OAuth app secret | Square sandbox | Sandbox key, live rotation needed before prod |
| `Canary/.env` → `SEED_PG_PASS` | Postgres password | Local dev DB | Dev-only |

### Known gaps

1. No Cloudflare Access policies on any zone — no real protection for IP-bearing static content.
2. No per-user investor identity — cannot answer "who accessed what and when".
3. No centralized secret rotation cadence or audit log.
4. `growdirect.io` zone ownership / Cloudflare account identity not confirmed in terminal-accessible state.
5. No `SECURITY.md` at repo root.
6. No pre-commit secret-scan hook (but see `devops/git-hooks/` — partially wired).

---

## First-90-days backlog

*Priority order — surface as GRO issues.*

1. **Inventory Cloudflare account** — confirm which account owns `growdirect.io`, `growdirect.app`; confirm admin email; confirm whether a consolidated account + API token with `Zone:Read, Access:Apps:Edit, Access:Policies:Edit` scope can be issued.
2. **Stand up Cloudflare Access on `canary.growdirect.io`** — proxy the CNAME, create Access App covering `/docs/*`, `/atlas/*`, `/prototype/*`, `/roadshow/*`; policy = email allowlist; identity provider = email OTP (no IdP dependency).
3. **Stand up Cloudflare Access on `growdirect.io/investor/*`** — same account, same policy shape.
4. **Investor allowlist** — canonical list of investor emails, versioned, reviewed monthly.
5. **SECURITY.md** — responsible disclosure contact, scope, response SLA.
6. **Pre-commit secret scan** — `git-secrets` or equivalent wired into `devops/git-hooks/` for all four repos.
7. **Token rotation runbook** — for cert.pem, tunnel credentials, CANARY_MCP_API_KEY, Square app secret.

---

## Key storage — proposed architecture

GrowDirect operates as a single-founder shop with several secret surfaces (Cloudflare
zone tokens, tunnel credentials, Square OAuth, Keycloak realms, Postgres passwords,
investor allowlists, SMTP credentials, SendGrid/Postmark keys once added). Today
these live in a mix of `.env` files, `~/.cloudflared/`, shell history, and ad-hoc
one-time pastes. That's not a posture we can ship investor access on top of.

**Two-layer pattern:**

### Layer 1 — Human vault (1Password)

Canonical store for anything a human touches directly: API tokens, admin passwords,
recovery codes, domain registrar login, Cloudflare account login, Square developer
console, investor contact list.

- CLI: `op` — lets us read + inject secrets programmatically without exposing them
  in shell history.
- Shared vaults per property ("GrowDirect Platform", "Canary", "Abalone Cove",
  "Angel") so access can be granted surgically.
- Recovery kit printed and stored offline.
- Rotation cadence: tokens → 90 days; passwords → 180 days or on incident.

### Layer 2 — Git-committed encrypted secrets (sops + age)

For secrets that need to live in the repo (deploy configs, `.env` files, Cloudflare
tunnel creds when checked in for reproducibility):

- `sops` (Mozilla) encrypts individual values in YAML/JSON/ENV files.
- `age` (modern file encryption) provides the key; the age public key is in the
  repo, the private key lives in 1Password.
- Files on disk: `canary/.env.enc`, `cove/.env.enc`, etc. — encrypted at rest,
  decrypted on demand locally and at deploy time.
- `.agekey` and decrypted `.env` are `.gitignore`d.
- `.sops.yaml` at the repo root declares which files are encrypted and which
  age public keys can decrypt them.

### Runtime secrets (Docker / Flask)

- `docker compose` reads from `.env` — but that file is the sops-decrypted product
  of `.env.enc`. Local dev: `sops -d .env.enc > .env`.
- Production (Mac Mini / cloud host): `cloudflared` tunnel credentials unchanged
  (they're device-scoped files); app secrets injected via the same sops flow at
  deploy time.

### What NOT in this pattern

- **Cloudflare Workers Secrets** — good for Worker scripts, not relevant until we
  have one.
- **AWS Secrets Manager** — over-indexed for our footprint; we're not on AWS.
- **HashiCorp Vault** — cluster-grade; overkill for single-founder.

### Adoption path

| Step | Cost | What it unlocks |
|---|---|---|
| 1. Sign up for 1Password Business (or reuse personal) | $8/mo | Vault + `op` CLI + shared-vault model |
| 2. Import current `.env` files + `cert.pem` + tunnel creds to vault | 1 hr | Single source of truth, audit log starts |
| 3. Install `sops` + `age`; generate age keypair per repo | 30 min | Encrypted secrets in git become safe |
| 4. Migrate `.env` → `.env.enc` across Canary, Cove, canary-site, growdirectprez.github.io | 1 hr/repo | `git diff` stops leaking secrets |
| 5. Pre-commit hook — reject commits with unencrypted secrets | 30 min | Enforcement, not just policy |
| 6. Document the dance in `docs/security/secret-handling.md` | 30 min | Reproducibility, onboarding-ready |

Total: ~5–6 hours of focused work to flip to this posture. Doable in one session
once a GRO is filed for it.
