---
card-type: platform-thesis
card-id: platform-identity-database-boundary
card-version: 1
domain: platform
layer: cross-cutting
status: approved
last-compiled: 2026-05-07
needs-review: false
tags:
  - identity
  - database
  - cross-product
  - atlasview
  - person
  - jwt
feeds:
  - GRO-848
  - canary-go-sprint-3
receives:
  - platform-thesis
  - concept-identity-layer-triad
---

# Platform: Identity Database Boundary

## What this is

The identity service owns its own Postgres database (`canary_identity_gcp` / `canary_identity_gcp_test`) — separate from the per-product databases (`canary_gcp`, future product DBs). Person records, password and MFA credentials, and refresh-token rotation chains live there. Cross-product consumers (AtlasView, Canary, future products) talk to identity over HTTP only — never via direct DB coupling.

## Purpose

GRO-848 surface 5 names Person as cross-product substrate: *"A Person provisioned via Canary's flows is visible to AtlasView through the same Person id. The cross-product user record is the substrate of 'one identity service across the firm.'"* Encoding that contract requires structural separation, not convention. A separate database makes the boundary impossible to shortcut — a service that wants Person data must hit the identity HTTP surface, because its connection string doesn't reach the identity DB.

The wrong shape — putting `persons` in `canary_gcp.app` — would survive code review but fail at the platform-split. The receiving Ruptiv team would have to undo it. Build it right the first time.

## Structure

| Database | Owner | Contents | Connection string |
|----------|-------|----------|-------------------|
| `canary_identity_gcp` | identity service | `public.persons`, `public.person_credentials`, `public.refresh_tokens` | `IDENTITY_DATABASE_URL` |
| `canary_gcp` | canary product | merchant-scoped app data; legacy `app.api_keys`, `app.signing_keys` (will migrate — see below) | `DATABASE_URL` |

The identity binary (`cmd/identity`) opens both pools. Identity-owned tables go to the identity pool; legacy api_keys + signing_keys reads continue against the canary pool until a follow-up dispatch migrates them. New cross-product identity tables always go to the identity DB.

## Invariants

- **No FK from identity DB to product DB.** The identity DB cannot reference `canary_gcp.app.organizations` because it's a different physical database. Person carries `org_id` as a value (UUID v4), and the application enforces referential discipline. This is a feature: it forces the contract to be application-level, not DB-level.
- **No FK from product DB to identity DB either.** Product tables that need to point at a Person carry `person_id` as a value. The identity service is the source of truth for what a `person_id` resolves to (via WhoAmI / `/v1/me`).
- **The identity service does not read product DBs in its hot paths.** Login, refresh, JWKS, WhoAmI all hit only `canary_identity_gcp`. Reading `canary_gcp.app.api_keys` is a legacy artifact, not a pattern to extend.
- **The product services do not read the identity DB.** They consume identity over HTTP — JWT verification via JWKS, Person lookup via WhoAmI. Period.

## Consumers

- **canary.go services** (gateway, web, devops, etc.) — verify JWTs against the identity JWKS endpoint; fetch Person via WhoAmI. They never connect to `canary_identity_gcp`.
- **AtlasView** — same posture. The AtlasView middleware layer is HTTP-only against identity per GRO-848 surfaces 1-3.
- **Future products** (ALX runtime, future digital actors) — inherit the same contract. Identity scales horizontally; products consume the contract.

## Migration path

Two pre-existing identity-shaped tables sit in the wrong place:

- `app.api_keys` (Sprint 1) — landed in `canary_gcp.app` before the boundary was named
- `app.signing_keys` (T-2 / GRO-862, 2026-05-07) — same

Both will move to `canary_identity_gcp` in a follow-up Sprint 4 dispatch (`Move api_keys + signing_keys from canary_gcp.app to canary_identity_gcp`). They stay where they are until then to keep the T-1 minter shipping critical-path. The identity binary's dual-pool wiring is the bridge.

## Related

- [[GRO-848]] — AtlasView identity integration: contract pin
- [[concept-identity-layer-triad]] — three-tier identity model (Person, OrgPerson, Membership)
- [[platform-thesis]] — three accountability rails; identity is the substrate the rails attach to
- [[canary-sprint-3-plan]] — T-1 (mint), T-2 (JWKS, done), T-3 (WhoAmI), T-4 (contract tests)
