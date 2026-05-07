# CanaryGo — IP Handover Scan (Ruptiv handover + external-sharing readiness)

Scope: `CanaryGo/` (328 Go files, ~67K LOC) plus immediate satellites — `services/canary-protocol/`, `.github/workflows/`, root LICENSE, and the deploy runbook. The Python `Canary/` prototype is out of scope. Memory files and Brain/ content under `~/.claude/projects/` are out of scope.

Two lenses, applied in tandem on every finding:

- **Firewall** — does this string violate the Ruptiv lineage rule (no GrowDirect, no PwC, no IBM, no Sobol, no UCSF, no methodology label tied to those firms)?
- **External** — would this leak, embarrass, or expose us if a partner, investor, or open-source reader saw it?

A single finding can be Firewall=Block but External=Note (an internal sprint code is a firewall problem but not a leak problem), or vice versa. Tags below say which lens drives the severity.

## Executive summary

The codebase is technically clean and architecturally consistent. There is no live secret, no real customer data, no PwC/IBM/Sobol/UCSF leak, no embedded patent-attribution conflict beyond the Apache-2.0 patent grant clause. The lineage exposure is concentrated in three categories that are tractable inside one sprint: the Go module path (`github.com/growdirect-llc/rapidpos`, 153 files / 383 import lines / one go.mod / one go.sum surface), the dev infrastructure naming (`growdirect_postgres`, `growdirect:growdirect_dev`, the `growdirect` Docker network — all plumbing that flows through compose, Makefile, CI, and integration-test comments), and the brand callouts in user-facing surfaces (LICENSE copyright line, OpenAPI `info.contact`, the Square OAuth dashboard footer, the `/.well-known/mcp.json` discovery doc, and the `https://canary.growdirect.io` link literals). The single hardest item is the module rename — the 383 import-line edit is mechanical, but the corresponding go.mod/go.sum rebuild, the cloudbuild substitutions, the Docker image labels (`patent=63-991-596` is fine; the `_REPO=canary-go` is fine; the `canary-rapidpos` GCP project ID needs a decision), and the staging-env DNS all have to land together. Handover is a one-sprint job (5–10 days of focused work) with the rename, the LICENSE swap, the dev-naming sweep, and the runbook scrub running in parallel; nothing here forces a longer arc.

## Findings by severity

### Block (5)

#### B1 — LICENSE copyright line names GrowDirect LLC
- **Pattern** — `Copyright (c) 2026 GrowDirect LLC`
- **Locations** — `CanaryGo/LICENSE:181`
- **Lens** — Firewall: Block. External: Block. Both rails fail; the LICENSE is the legal anchor of the IP grant.
- **Risk** — On handover, the file claims a non-Ruptiv copyright owner. Apache 2.0 sublicensing flows from this line; the wrong entity here means the wrong entity is granting downstream rights. Visible to every reader of the repo.
- **Remediation** — Replace with `Copyright (c) 2026 Ruptiv` (or the precise Ruptiv legal entity once confirmed by counsel). Date the change in the commit message; do not back-date.
- **Effort** — S (one-line edit; legal sign-off on the entity name is the gating step, not the edit).

#### B2 — Personal email hard-coded in mirror script as commit author
- **Pattern** — `git -c user.email="bonsallprotea@gmail.com" -c user.name="GrowDirect"`
- **Locations** — `CanaryGo/scripts/mirror-public.sh:48`
- **Lens** — Firewall: Block. External: Block. Personal Gmail in a script that runs against a public mirror is both a firewall violation and a leak.
- **Risk** — Every mirror commit pushed to the public `growdirect-llc/canary-go` repo carries a personal Gmail address as committer email. Visible in `git log` of the public mirror and recoverable from any clone.
- **Remediation** — Two parts: (a) script edits to use a Ruptiv-owned bot identity (e.g., `ruptiv-bot@ruptiv.com` once provisioned, or a noreply per the company's git policy); (b) the mirror script itself is purpose-built to push to `growdirect-llc/canary-go` and pulls from `CanaryGo/../services/canary-protocol`, both growdirect-anchored — re-evaluate whether the script ships at all in the handover bundle. The cleanest answer is to delete it; the mirror target won't exist in Ruptiv-land.
- **Effort** — S (delete file or rewrite with new identity).

#### B3 — Dev secrets in seed file with `dev-only-do-not-ship` placeholders are fine, but the Acme test merchant carries `dev-only-do-not-ship-this-secret-1234567890abcdef` as a literal HMAC secret in source-controlled SQL
- **Pattern** — `dev-only-do-not-ship-this-secret-1234567890abcdef`
- **Locations** — `CanaryGo/deploy/schema/99_seed.sql:64`
- **Lens** — Firewall: Note. External: Block.
- **Risk** — The string is labelled "do not ship" and is clearly a dev placeholder, but it is committed plaintext in seed SQL that ships in the repo. If any environment ever loads `99_seed.sql` and forgets to rotate, this string becomes a live HMAC secret that anyone with the repo can replay. It also looks like a real secret to a casual reader — investor, auditor, or partner who clones the repo.
- **Remediation** — Replace literal with a placeholder reference (`'__SEED_HMAC_PLACEHOLDER__'`), generate the dev secret in a setup script, and document the rotation path. Add a CI guard that fails if the placeholder ever leaks. Apply the same treatment to the `argon2id$DEV_PLATFORM_PLACEHOLDER` and `argon2id$DEV_TENANT_PLACEHOLDER` rows in the same file — those are already placeholders, so just confirm.
- **Effort** — M (refactor seed pipeline to source secrets from a generator).

#### B4 — User-facing UI strings hard-code `GrowDirect LLC` and `https://canary.growdirect.io`
- **Pattern** — `GrowDirect LLC · sandbox · token storage encrypted at rest`, `https://canary.growdirect.io`, `https://canary.growdirect.io/sdds/`, `https://github.com/growdirect-llc/canary-go`
- **Locations** — `CanaryGo/internal/squareauth/handler.go:280`, `:282`, `:284`, `:286`, `:393`, `:395`, `:397` (Square OAuth landing + dashboard footers); `CanaryGo/cmd/gateway/main.go:300` (OpenAPI repo URL), `:330–331` (discovery doc `links.vault` and `links.sdds`)
- **Lens** — Firewall: Block. External: Required (it's published already, but it ties Canary's discovery surface to a brand we're firewalling).
- **Risk** — Any merchant who completes the Square OAuth flow sees "GrowDirect LLC" in the UI footer. Any agent fetching `/.well-known/mcp.json` follows the link to `https://canary.growdirect.io`. The discovery payload is the publicly-advertised entry point to the platform.
- **Remediation** — Two-track: (a) replace the company-name string with the entity that owns Canary post-handover; (b) decide the long-term home for the architecture vault and SDDs (Ruptiv subdomain, dedicated Canary domain, or Confluence-style internal-only). Update all link literals in one pass. The OpenAPI remote URL also needs a target — either the Ruptiv-owned mirror, or remove it from the discovery doc until a public spec lives somewhere stable.
- **Effort** — M (templates + handler + discovery doc + decision on the destination domain).

#### B5 — Internal stakeholder name embedded in a doc comment
- **Pattern** — `This is the keystone for Bart's wedge`
- **Locations** — `CanaryGo/internal/adapters/counterpoint/parser.go:2`
- **Lens** — Firewall: Block. External: Block. Names a real partner and uses internal positioning language.
- **Risk** — "Bart's wedge" is internal strategic shorthand naming a specific partner. Visible at the top of the file in any IDE, in any code search, and in any reader's first contact with the Counterpoint adapter. Both a firewall violation (firewalled prior-relationship language) and an external leak (names a partner who hasn't agreed to be named).
- **Remediation** — Rewrite the package comment to describe what the adapter does, not who it's strategically meant to enable. Drop the "wedge" framing — that's internal positioning, not engineering documentation. One-paragraph rewrite focused on the adapter contract.
- **Effort** — S (single comment block).

### Required (12)

#### R1 — Go module path is `github.com/growdirect-llc/rapidpos`
- **Pattern** — `module github.com/growdirect-llc/rapidpos` (go.mod) plus 383 import lines across 153 Go files
- **Locations** — `go.mod:1`; representative imports: `cmd/gateway/main.go`, `cmd/identity/main.go`, `cmd/transaction/main.go`, `internal/auth/middleware.go`, `internal/identity/jwt.go`, `internal/db/query/transaction/models.go`, `internal/protocol/webhook/handler.go`, `internal/protocol/sub3/merkle.go`, `internal/web/handler.go`, `internal/squareauth/squareauth.go` — and 143 more.
- **Lens** — Firewall: Required. External: Required (every recursive import resolves through GitHub once the org name routes anywhere).
- **Risk** — The module path bakes the GitHub org name into every Go file's import surface. Any agent or developer who reads the source sees `growdirect-llc/rapidpos` 383 times. Beyond firewall, the `rapidpos` half is a partner-facing alias from a separate deal — Ruptiv won't own it either way.
- **Remediation** — Pick the new module path now (suggested `github.com/ruptiv/canary` — short, Ruptiv-owned, no partner brand, descriptive). Run `find . -name "*.go" -exec sed -i '' 's|github.com/growdirect-llc/rapidpos|github.com/ruptiv/canary|g' {} \;` plus matching edits to `go.mod`, `sqlc.yaml` (if any package paths are pinned), and the cloudbuild file. Run `go mod tidy` and the full test suite. The string change is mechanical; the gating decision is the path itself.
- **Effort** — M (mechanical sweep + verification; the bottleneck is verifying nothing else hard-codes the path — checked: cloudbuild, dockerfiles, scripts/ are clean of literal `rapidpos` references outside the secrets test path which uses `rapidpos` as a SourceCode value, not an import path).

#### R2 — Database user, password, and container name baked into Makefile, compose, CI, and integration-test comments
- **Pattern** — `growdirect:growdirect_dev`, `growdirect_postgres`, `growdirect_valkey`, `growdirect` (network), `PG_USER ?= growdirect`
- **Locations** — `Makefile:7,8,11,12`; `deploy/docker-compose.yml:4,10,13,14,17,21,26,37,41,42,74,78,79`; `.env.example:10,13`; `.github/workflows/canary-go-ci.yml:55–80` (7 hits); plus integration-test file headers in 11 packages — `internal/fox/integration_test.go`, `internal/chirp/integration_test.go`, `internal/owl/integration_test.go`, `internal/protocol/webhook/integration_test.go`, `internal/protocol/audit/integration_test.go`, `internal/protocol/cockroach/cockroach_test.go`, `internal/item/integration_test.go`, `internal/inventory/integration_test.go`, `internal/protocol/sub1/integration_test.go`, `internal/protocol/sub2/integration_test.go`, `internal/pricing/integration_test.go` — each as a comment header block.
- **Lens** — Firewall: Required. External: Recommended (these are dev-only credentials, but the brand-tagged container name leaks into every developer's `docker ps`).
- **Risk** — Every developer who clones the repo runs `docker compose` against a network and database whose names anchor to GrowDirect. The string also appears in CI logs, integration test boilerplate, and the `.env.example` developers copy on day one.
- **Remediation** — Pick the new dev brand (`ruptiv_postgres`, `ruptiv:ruptiv_dev`, `ruptiv` network) and sweep. The compose file also references `external: true` on the network, which means the Ruptiv-renamed devops/docker-compose.yml has to land first or the network has to be re-anchored. This is one of the more boring sweeps but touches enough files that it needs its own ticket.
- **Effort** — M (mechanical, but ~25 files; the integration-test comment headers are the long tail).

#### R3 — Internal Linear ticket URL committed in deploy runbook
- **Pattern** — `https://linear.app/growdirect/issue/GRO-756`
- **Locations** — `CanaryGo/deploy/runbook-gateway-deploy.md:438`
- **Lens** — Firewall: Required. External: Block (a public-facing runbook should not link to a private project tracker).
- **Risk** — Anyone reading the runbook gets a direct link to the internal Linear workspace. The link is broken for everyone outside the workspace, but it discloses the workspace name and the ticket numbering.
- **Remediation** — Strip the Linear links from the runbook footer. Replace with internal references that don't depend on Linear (commit SHAs, design-doc paths). The 250+ `GRO-` ticket references in Go file comments are a separate, lower-severity issue (R10 below); only the explicit `linear.app` URL is at this severity.
- **Effort** — S (one line).

#### R4 — Personal email expectation in deploy runbook
- **Pattern** — `# Expected: gclyle@growdirect.io`
- **Locations** — `CanaryGo/deploy/runbook-gateway-deploy.md:50`
- **Lens** — Firewall: Required. External: Required.
- **Risk** — Names the founder and the GrowDirect domain in the same line, in a runbook that documents production deployment. Less load-bearing than the personal Gmail in B2 but still a transfer artifact.
- **Remediation** — Replace with the canonical Ruptiv operator identity once known. If unknown at handover time, use a placeholder like `# Expected: <your-ruptiv-account>@ruptiv.com`.
- **Effort** — S (one line).

#### R5 — Path references to founder home directory and GrowDirect worktree in runbook
- **Pattern** — `cd /Users/gclyle/GrowDirect/.worktrees/gro-756`, `cd /Users/gclyle/GrowDirect`, branch name `gclyle/gro-756-phase-1j-deploy-canary-protocol-gateway-to-gcp-cloud-run`
- **Locations** — `CanaryGo/deploy/runbook-gateway-deploy.md:71,73,76,98,199,270,383`; `CanaryGo/deploy/cloudbuild.gateway.yaml:8`
- **Lens** — Firewall: Required. External: Recommended.
- **Risk** — The runbook is a step-by-step deploy guide. It currently assumes a specific home directory layout, a specific worktree, and a specific git branch naming convention tied to founder username and GRO ticket numbering. None of that survives handover.
- **Remediation** — Rewrite the runbook to use repository-root-relative paths and generic branch placeholders (`<your-feature-branch>`). The cloudbuild trigger comment can drop the `gclyle/gro-746-*` filter or be reframed against Ruptiv's branching convention.
- **Effort** — M (full pass over the 440-line runbook).

#### R6 — GCP project ID `canary-rapidpos` baked into cloudbuild and tests
- **Pattern** — `canary-rapidpos`, `projects/canary-rapidpos/serviceAccounts/...`
- **Locations** — `CanaryGo/deploy/cloudbuild.gateway.yaml:9,15,25,34`; `CanaryGo/deploy/runbook-gateway-deploy.md:52,54,55,87`; `CanaryGo/internal/protocol/secrets/sm_resolver_test.go:80,91,92,317`
- **Lens** — Firewall: Recommended (rapidpos is a partner alias, not a firewalled prior-firm brand). External: Required (the GCP project ID will need to migrate to Ruptiv-owned cloud accounts on handover).
- **Risk** — The cloudbuild substitutions, service account ARN, and Cloud SQL instance string all anchor to `canary-rapidpos`. After handover, the new owner will run their own GCP project; every reference to `canary-rapidpos` becomes wrong.
- **Remediation** — Parameterize `_PROJECT_ID` in cloudbuild substitutions; never hard-code the project name. Replace the test fixtures with a synthetic project ID (`test-project`). Document in the runbook how to set the deploy target to a Ruptiv-owned project.
- **Effort** — M (parameterize cloudbuild, fix tests, document migration).

#### R7 — `Bart's wedge`-equivalent strategic-positioning leakage in subdomain link literals
- **Pattern** — `https://demo.growdirect.io`, `https://canary.growdirect.io`, `https://api.canary.growdirect.io`, `https://api.canary-staging.growdirect.io`
- **Locations** — `CanaryGo/cmd/gateway/main.go:293,330,331`; `CanaryGo/cmd/gateway/discovery_test.go:14,41,42`; `CanaryGo/internal/config/config.go:17`; `CanaryGo/internal/squareauth/squareauth.go:15`; `CanaryGo/deploy/runbook-gateway-deploy.md:13,89,163,164,304`; `services/canary-protocol/openapi/openapi.yaml:16,18`; `services/canary-protocol/openapi/gen/generate.py:882,887,891`
- **Lens** — Firewall: Required. External: Required.
- **Risk** — The subdomains anchor Canary to GrowDirect at the DNS layer. Discovery payloads, OpenAPI servers list, runbook curl commands, and OAuth redirect docs all hard-code these URLs. When Canary moves to a Ruptiv-owned domain, every literal flips.
- **Remediation** — Two-step: (a) decide the new home (suggested: `canary.ruptiv.com` or a dedicated `canary-protocol.com` if Canary stays a separate product surface); (b) sweep all literal URLs to env-driven config. The discovery doc handler in `cmd/gateway/main.go` already has a `cfg.PublicURL` fallback path — extend it so links to vault and SDDs are also configurable, not literal.
- **Effort** — M (sweep + add config keys for vault/SDD link targets).

#### R8 — OpenAPI `info.contact.name` field is `GrowDirect LLC`
- **Pattern** — `name: GrowDirect LLC` / `name: GrowDirect, LLC`
- **Locations** — `CanaryGo/internal/devops/static/canary-api-v1.yaml:14`; `services/canary-protocol/openapi/openapi.yaml:11`; `services/canary-protocol/openapi/gen/generate.py:879`
- **Lens** — Firewall: Required. External: Required.
- **Risk** — The OpenAPI spec is the developer-facing surface for the protocol. The contact field shows up in every Swagger UI / Redoc render and in any API gateway that ingests the spec. It tells the world who owns the API.
- **Remediation** — Replace with the new entity name. The generator (`generate.py:879,882,887,891`) is the canonical source for the protocol-level OpenAPI; update it and regenerate. The static stub in `internal/devops/static/canary-api-v1.yaml` is a separate file and needs the same edit.
- **Effort** — S (string swap in two YAMLs and one Python).

#### R9 — `Python prior art` field in devops console references the frozen Python prototype path
- **Pattern** — `Canary/canary/services/devops_monitor.py`, `Canary/canary/qa_agent/`, `Canary/canary/services/evidence_service.py`, `Canary/canary/services/anchor_service.py`
- **Locations** — `CanaryGo/internal/web/devops/devops.go:96,140,148,163,171`; `CanaryGo/internal/web/devops/devops_test.go:100`
- **Lens** — Firewall: Required. External: Recommended (it tells anyone reading the devops console that there's a prior Python codebase, which invites the question "where is it"). The Python prototype is GrowDirect-anchored and not part of the handover bundle.
- **Risk** — Every service entry in the devops catalog points at a Python file path that doesn't exist in the handover bundle. A reader who doesn't know the history will see broken links to an unknown codebase.
- **Remediation** — Drop the `PythonPriorArt` field from the `Service` struct. It's a Phase-1 context aid that has done its job; the comments in the live Go service tell the story going forward.
- **Effort** — S (delete a struct field + its references; ~6 files).

#### R10 — 252 `GRO-NNN` ticket references in Go source comments
- **Pattern** — `GRO-687`, `GRO-693`, `GRO-694`, `GRO-739`, `GRO-746`, `GRO-756`, `GRO-762`, `GRO-763`, `GRO-764`, `GRO-765`, `GRO-766`, `GRO-768`, `GRO-799`, `GRO-800`, `GRO-802`, `GRO-836`, `GRO-838`, `GRO-839` — and many more
- **Locations** — 252 `.go` lines, 21 `.md`/`.yaml` lines (273 total). Concentrated in `cmd/*/main.go` (top-of-file context comments) and the `internal/protocol/*` package.
- **Lens** — Firewall: Required. External: Note (the ticket IDs themselves are opaque without access to the Linear workspace, so they leak less than the URL pattern in R3).
- **Risk** — The ticket IDs reference an internal Linear project that doesn't transfer. They make the code less readable to a new owner who can't resolve them. They also imply a project-management style that may differ from Ruptiv's.
- **Remediation** — Convert `GRO-NNN` to an opaque internal-spec reference scheme that survives the move (e.g., `WAVE-A-PHASE-2`, or just rewrite the comment without a ticket ID at all — most don't need one). Run a sweep that strips the IDs and cleans up the now-dangling sentences. This is mechanical drudgery but high-volume; consider scoping it as its own ticket.
- **Effort** — L (~250 edits, many with adjacent prose that needs touching up).

#### R11 — `OQ Resolution Pack` and `founder-approved` framing in Go comments
- **Pattern** — `Per OQ Resolution Pack §A.1 OQ-1.5 (founder-approved 2026-05-03)`, `the founder-approved 2026-05-03 default`, `per the founder's prior context`
- **Locations** — `CanaryGo/internal/fox/handler.go:536,545`; `CanaryGo/internal/fox/subjects.go:9,44`; `CanaryGo/internal/db/types/decimal.go:5`; `CanaryGo/internal/party/party.go:14`
- **Lens** — Firewall: Required. External: Required.
- **Risk** — "OQ Resolution Pack" is internal sprint-planning vocabulary tied to GrowDirect's planning rhythm. "Founder-approved" reads as a single-person-decision-making style that doesn't fit the Ruptiv firm voice. Both are firewalled idiom and external-tone problems.
- **Remediation** — Rewrite each comment to state the decision in the engineering plain — what the rule is and why — without naming the source document or the role that approved it. The decision can be cited; the approval ritual cannot.
- **Effort** — S (5 files, one-line edits each).

#### R12 — Apache 2.0 patent grant clause auto-licenses Patent 63/991,596 downstream
- **Pattern** — Section 3 of Apache 2.0 — "each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable patent license to make, have made, use, offer to sell, sell, import..."
- **Locations** — `CanaryGo/LICENSE` (Section 3); patent reference in `CanaryGo/cmd/gateway/main.go`, `cmd/sub1-hash-seal/main.go`, `cmd/sub2-parse-route/main.go`, `cmd/sub3-merkle-ordinal/main.go`, `internal/devops/static/canary-api-v1.yaml`, `deploy/cloudbuild.gateway.yaml:103` (label `patent=63-991-596`), `deploy/runbook-gateway-deploy.md:17,439`, `internal/protocol/webhook/handler.go`, `internal/protocol/evidence/handler.go`
- **Lens** — Firewall: Note. External: Block. Legal advice required.
- **Risk** — The Apache 2.0 license auto-grants a royalty-free patent license to every user of the source. The codebase explicitly identifies Patent Application 63/991,596 as covering "the operating embodiment of Node 2." If this is the intended posture (open-source, free-to-use protocol with a defensive patent grant), no action is needed. If the patent is meant to be commercially licensed separately or held as a proprietary asset, Apache 2.0 is the wrong license — and the file headers that proudly cite the patent number need to be reconciled with the licensing model.
- **Remediation** — This is a counsel call, not an engineering call. Confirm with Ruptiv counsel: (a) does the new owner intend to keep Apache 2.0 with the patent grant?; (b) if yes, the LICENSE entity name fix in B1 covers it; (c) if no, switch to a proprietary or dual-license posture and excise patent-attribution language from public surfaces. Until clarified, this is a Block from the legal-exposure angle, even though it's not a string to redact.
- **Effort** — Counsel-gated. Coding effort once decided: S (license file swap) to M (license-grant-clean rewrite of patent-attribution comments).

### Recommended (8)

#### N1 — Sprint terminology (`Loop N`, `Wave A`, `Phase B.2`) in 333 Go comment lines
- **Pattern** — `Loop 2`, `Loop 3`, `Wave A`, `Wave B`, `Phase A.1`, `Phase B.2`, etc.
- **Locations** — 333 lines across the `cmd/` and `internal/` trees.
- **Lens** — Firewall: Recommended (not a firewalled brand, but it's GrowDirect's planning vocabulary). External: Note (a new reader has to learn the vocabulary, but it doesn't break anything).
- **Risk** — The vocabulary is dense and unfamiliar. A new owner reading the codebase has to decode "Loop 4 Wave A Phase A.1" before they can place a comment in time. Style mismatch with Ruptiv brand voice (which prefers calm, intelligent, no-padding sentences with mechanism, measurement, or timeline — sprint codes give a timeline but in a code only insiders read).
- **Remediation** — On a future cleanup pass, rewrite to date-anchored decisions ("decided 2026-05-03") or absolute references ("see commit abc123"). Not a handover-blocker.
- **Effort** — L (333 edits, but they can be amortized across normal maintenance).

#### N2 — `BodyTODO` field name and the implementation-status story in devops console
- **Pattern** — `BodyTODO string`, `// time. T2.0 ships only the chrome — every service body says "TODO".`
- **Locations** — `CanaryGo/internal/web/devops/devops.go:12,97,119,...`
- **Lens** — Firewall: Note. External: Recommended.
- **Risk** — The devops console literally renders "TODO" tags for unimplemented services. A partner or investor browsing the console will see "TODO" all the way down. This is consistent with a Phase-1 build, but if it ships in a handover demo, it tells the wrong story.
- **Remediation** — Either rename the field to `Status` and use enumerated values (`shipped`, `wired`, `planned`), or hide the status column from the prod build via a feature flag. Apply Ruptiv brand voice to the strings — calm, no exclamation, mechanism-focused.
- **Effort** — S (rename + a feature flag).

#### N3 — `acme-store.jeffe`, `lookup-test.jeffe`, `duplicate.jeffe` test fixtures
- **Pattern** — `.jeffe`-suffixed namespace test data
- **Locations** — `CanaryGo/internal/protocol/namespace/store_test.go`, `handler_test.go`, `register_test.go` — many lines.
- **Lens** — Firewall: Note. External: Note.
- **Risk** — The `.jeffe` namespace is an intentional Canary protocol design (see `cmd/gateway/main.go:120` — ".jeffe namespace registration"). It's not a personal-name leak; it's a TLD-style identifier. Worth a confirmation that the spelling is intentional (not a transcription of a person's name).
- **Remediation** — Confirm protocol-level intent of `.jeffe`. If intentional, document it explicitly as a protocol identifier in the OpenAPI spec and the README. If unintentional, rename to a neutral suffix.
- **Effort** — S (documentation pass, no code change required if intent is confirmed).

#### N4 — `internal/web/devops/` references `Brain/wiki/cards/...` paths
- **Pattern** — `Brain/wiki/cards/catalog.md`, `Brain/wiki/cards/manifest.md`, etc. (12 occurrences in Go)
- **Locations** — `CanaryGo/internal/web/devops/devops.go:91,116,123,130,137,145,153,160,168,176`; `CanaryGo/internal/web/devops/devops_test.go:98`; `CanaryGo/internal/db/types/decimal.go:15`
- **Lens** — Firewall: Recommended. External: Recommended.
- **Risk** — The devops console renders a `Card` field that points at a path inside the Obsidian vault (`Brain/wiki/cards/...`). The Obsidian vault doesn't transfer with the codebase — it's part of the founder's personal knowledge environment. After handover, every card link is dead.
- **Remediation** — Either ship the cards as in-repo Markdown (under `docs/cards/` or similar) and update the path, or remove the `Card` field from the public devops console and keep it as a developer-only annotation. The latter is cleaner.
- **Effort** — S (refactor or remove the field).

#### N5 — `dev-internal-secret` and `dev-session-secret` literals in compose
- **Pattern** — `INTERNAL_SERVICE_SECRET: dev-internal-secret`, `SESSION_SECRET: dev-session-secret`
- **Locations** — `CanaryGo/deploy/docker-compose.yml:43,44,80,81`
- **Lens** — Firewall: Note. External: Recommended.
- **Risk** — Dev-only literals, clearly named, and the surrounding files document them as such. Low risk in practice but a Big-4-eye-roll moment if seen out of context.
- **Remediation** — Read from `.env.local` instead of inline literals; update `.env.example` to make this the canonical pattern.
- **Effort** — S.

#### N6 — `Acme Test Org` / `Acme Main Street` test merchant in seed SQL and generated models
- **Pattern** — `Acme Test Org`, `Acme Main Street`, UUIDs `33333333-...`, `acme-main-square-001`
- **Locations** — `CanaryGo/deploy/schema/99_seed.sql:25–52`; comments in generated `internal/db/query/transaction/models.go:184`, `identity/models.go:184`, `tsp/models.go:184`
- **Lens** — Firewall: Note. External: Note.
- **Risk** — `Acme` is the canonical placeholder name in technical writing. No real customer leak. The note about it being Square-connected is correct for the test scenario.
- **Remediation** — None required.
- **Effort** — N/A.

#### N7 — Sprint-planning vocabulary in `docs/conventions.md`
- **Pattern** — `OQ Resolution Pack`, `loop3-decimal-standard`, `loop2-build-report`, `Loop 2 closure`, `22 founder-approved decisions`
- **Locations** — `CanaryGo/docs/conventions.md:233–238`
- **Lens** — Firewall: Recommended. External: Recommended.
- **Risk** — Same family as R11 and N1 — internal vocabulary that doesn't translate.
- **Remediation** — Rewrite the cross-references section to point at concrete in-repo decisions or strip the brain/ references entirely. Same engineering effort as N4.
- **Effort** — S.

#### N8 — `LNURL_STUB=true`, `DEV_CONSOLE=1` flags in compose
- **Pattern** — `LNURL_STUB: "true"`, `DEV_CONSOLE: "1"`
- **Locations** — `CanaryGo/deploy/docker-compose.yml:48,51`
- **Lens** — Firewall: Note. External: Note.
- **Risk** — Per project convention these are intentional dev settings (per `feedback_dont_change_redirects` and the LNURL_STUB pattern). Not a flag.
- **Remediation** — None.
- **Effort** — N/A.

### Note (4)

#### O1 — Apache 2.0 license file (text only, separate from B1 entity issue)
- The Apache 2.0 license body is fine on the merits. The only Block-level edit is the entity line at L181 (covered in B1). Section 3 patent grant is a policy question for counsel (covered in R12).

#### O2 — `canary-rapidpos` GCP project name, `rapidpos` as a SourceCode value
- The string `rapidpos` is used in two distinct ways in the codebase: as a partial name in the GCP project ID `canary-rapidpos` (covered in R6), and as a `SourceCode` literal value passed to `BuildResourcePath`, `Invalidate`, `cacheGet`, etc. The latter is a protocol-level identifier representing a POS source type. It's not a brand or a partner reference at the protocol layer. Can stay.

#### O3 — `Bitcoin`, `Lightning`, `L402`, `LNURL`, satoshi, `.jeffe` namespace
- These are protocol-design vocabulary, not lineage leakage. 277 references across the codebase are consistent with the Patent 63/991,596 architecture. No remediation.

#### O4 — Distroless base image `gcr.io/distroless/static-debian12:nonroot`
- Public Google distroless image. No Ruptiv/GrowDirect anchor. Stays.

## The big rename

`github.com/growdirect-llc/rapidpos` is the Go module path. It anchors:

- 1 line in `go.mod`
- 153 Go files importing the module
- 383 import lines (many files import multiple subpackages)
- ~67K LOC of Go behind those imports
- `go.sum` has no `growdirect`-anchored entries (verified) — only third-party deps. Good news.
- `sqlc.yaml` does not appear to pin the module path (clean).
- `cloudbuild.gateway.yaml` does not literal-match `rapidpos` outside the GCP project ID `canary-rapidpos` (separate finding R6).
- Dockerfiles do not reference the module path (they `COPY` from build context).

**Proposed target: `github.com/ruptiv/canary`.**

Justification:

- Short, Ruptiv-owned, brand-clean.
- Drops `rapidpos` (a partner alias, not a Ruptiv asset).
- Names the product (`canary`) directly — symmetric with how the codebase already self-identifies (the binary names, the API titles, the patent attribution).
- Leaves room for sibling modules (`github.com/ruptiv/canary-go`, `github.com/ruptiv/canary-edge`, etc.) without confusion.

Mechanical execution:

```
find . -name "*.go" -exec sed -i '' 's|github.com/growdirect-llc/rapidpos|github.com/ruptiv/canary|g' {} \;
sed -i '' 's|github.com/growdirect-llc/rapidpos|github.com/ruptiv/canary|' go.mod
go mod tidy
go build ./...
go test ./...
```

The risk surfaces during `go mod tidy` — if any dep was previously vendored or replaced via a `replace` directive against the old path, it'll surface there. Quick scan: `grep replace go.mod` is empty.

The companion edits:

- `services/canary-protocol/openapi/openapi.yaml` — the `info.contact` block (R8) and the `servers` URLs (R7).
- `scripts/mirror-public.sh` — the `REPO="growdirect-llc/canary-go"` constant; either retarget to a Ruptiv-owned mirror or delete.
- `internal/squareauth/handler.go` — the `https://github.com/growdirect-llc/canary-go` link (B4).
- `cmd/gateway/main.go:300` — `openAPIRepo` constant.

Estimated rename + companion-edit time: **half a day of focused work**, gated on (a) the destination module path being decided, and (b) the destination domain (vault/sdds links) being decided. The actual edits are mechanical.

## Lineage firewall scrub manifest

Flat work order, grouped by category. Every line is "path → change". Scope is the handover sprint.

### Module path (R1)
- `CanaryGo/go.mod:1` — `module github.com/growdirect-llc/rapidpos` → `module github.com/ruptiv/canary`
- `CanaryGo/go.sum` — regenerate via `go mod tidy` after sed sweep
- 153 Go files (full list available via `grep -rl github.com/growdirect-llc/rapidpos --include=*.go`) — sed-replace import lines

### Dev infrastructure (R2)
- `CanaryGo/Makefile:7,8,11,12` — `growdirect:growdirect_dev`, `growdirect_postgres`, `PG_USER ?= growdirect` → `ruptiv:ruptiv_dev`, `ruptiv_postgres`, `PG_USER ?= ruptiv`
- `CanaryGo/.env.example:10,13` — DATABASE_URL, VALKEY_URL placeholders
- `CanaryGo/deploy/docker-compose.yml` — 13 lines: network name, container name in entrypoints, env vars
- `.github/workflows/canary-go-ci.yml` — 7 lines: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `PG_USER`, `PG_PASSWORD`, all DATABASE_URL strings
- 11 integration-test file headers — leading comment block in `internal/{fox,chirp,owl,item,inventory,pricing}/integration_test.go`, `internal/protocol/{webhook,audit,cockroach,sub1,sub2}/*_test.go`
- `CanaryGo/docs/conventions.md:148` — sample DATABASE_URL string

### Brand callouts in user-facing surfaces (B1, B4, R8)
- `CanaryGo/LICENSE:181` — `Copyright (c) 2026 GrowDirect LLC` → `Copyright (c) 2026 Ruptiv`
- `CanaryGo/internal/squareauth/handler.go:280,282,284,286,393,395,397` — three link literals + footer "GrowDirect LLC" string
- `CanaryGo/cmd/gateway/main.go:293,300,330,331` — `PUBLIC_URL` example, `openAPIRepo` constant, discovery doc `links.vault` and `links.sdds`
- `CanaryGo/cmd/gateway/discovery_test.go:14,41,42` — test expectations for the discovery URL
- `CanaryGo/internal/config/config.go:17` — comment example for PublicURL
- `CanaryGo/internal/squareauth/squareauth.go:15` — SQUARE_REDIRECT_URI comment example
- `CanaryGo/internal/devops/static/canary-api-v1.yaml:14` — `name: GrowDirect LLC`
- `services/canary-protocol/openapi/openapi.yaml:11,14,16,18` — `name: GrowDirect, LLC`, vendor URL, server URLs
- `services/canary-protocol/openapi/gen/generate.py:879,882,887,891` — same fields in the generator

### Internal positioning leakage (B5, R11)
- `CanaryGo/internal/adapters/counterpoint/parser.go:1–5` — drop "Bart's wedge" framing; rewrite to engineering documentation
- `CanaryGo/internal/fox/handler.go:536,545` — drop "OQ Resolution Pack §A.1 OQ-1.5 (founder-approved 2026-05-03)" framing
- `CanaryGo/internal/fox/subjects.go:9,44` — same
- `CanaryGo/internal/db/types/decimal.go:5` — same
- `CanaryGo/internal/party/party.go:14` — same

### Personal email + path (B2, R4, R5)
- `CanaryGo/scripts/mirror-public.sh:48` — delete file or replace identity with Ruptiv bot
- `CanaryGo/deploy/runbook-gateway-deploy.md:50,71,73,76,87,98,163,164,199,270,304,383,438` — strip founder username, GrowDirect domain, Linear URLs, founder home dir paths
- `CanaryGo/deploy/cloudbuild.gateway.yaml:8,9,15,25,34` — parameterize project ID, drop founder branch filter

### GCP project (R6)
- `CanaryGo/deploy/cloudbuild.gateway.yaml:9,15,25,34` — parameterize `_PROJECT_ID`
- `CanaryGo/internal/protocol/secrets/sm_resolver_test.go:80,91,92,317` — replace literal `canary-rapidpos` with `test-project`
- `CanaryGo/deploy/runbook-gateway-deploy.md` — document Ruptiv project setup

### Internal references (R3, R10, N4, N7)
- `CanaryGo/deploy/runbook-gateway-deploy.md:438` — strip `linear.app/growdirect/...` URL line
- 252 GRO ticket references across `cmd/*` and `internal/*` Go comments — sweep
- 12 `Brain/wiki/cards/...` references in `internal/web/devops/devops.go` and `internal/db/types/decimal.go` — drop or relocate
- `CanaryGo/docs/conventions.md:230–238` — strip Brain/ references, rewrite Linear/Loop/Wave references

### Dev-status markers (N2, N9)
- `CanaryGo/internal/web/devops/devops.go` — rename `BodyTODO` to `Status`, gate display
- `CanaryGo/deploy/docker-compose.yml:43,44,80,81` — move secret literals to `.env.local`

### Test seed (B3)
- `CanaryGo/deploy/schema/99_seed.sql:64` — replace literal HMAC secret with placeholder + generation script
- Same file — confirm `argon2id$DEV_*_PLACEHOLDER` rows are real placeholders (already are)

## External sharing classification

### Safe to share publicly (after handover sprint completes)
- `internal/protocol/*` — webhook validation, evidence chain, Merkle anchor, namespace registration. Cleanly engineered, no embedded business strategy, well-suited to becoming a public open-source protocol surface. Today's surface lives at `services/canary-protocol/openapi/openapi.yaml` and is already mirrored to a public repo via `mirror-public.sh`.
- `internal/db/types/*` — decimal type, ledger types, ltree wrapper. Generic Go infrastructure.
- `internal/auth/lnurl/*` — LNURL-auth implementation per spec. Useful reference implementation; spec is public.
- `cmd/sub1-hash-seal`, `cmd/sub2-parse-route`, `cmd/sub3-merkle-ordinal` — protocol pipeline subscribers. Patent attribution comments need to be reconciled with whatever licensing posture wins (R12), but the engineering itself is shareable.
- The OpenAPI spec at `services/canary-protocol/openapi/openapi.yaml` (with B1, R7, R8 fixed) — already designed for public consumption.

### Safe to share with partners under NDA
- `internal/squareauth/*` — Square OAuth flow. Once the brand callouts (B4) are scrubbed, fine for partners.
- `internal/adapters/counterpoint/*` — NCR Counterpoint adapter. Once the "Bart's wedge" comment is rewritten (B5), this is technical adapter code, fine under NDA.
- `internal/fox/*` — case management module. Once the "founder-approved" framing is scrubbed (R11), shareable.
- `cmd/gateway`, `cmd/identity`, `cmd/transaction`, `cmd/inventory`, `cmd/receiving`, etc. — service binaries. Generic store-ops infrastructure.
- `deploy/*` (Dockerfiles, compose, cloudbuild) — once the dev naming sweep (R2) and project ID parameterization (R6) land.

### Internal only
- `deploy/runbook-gateway-deploy.md` until the founder-username, Linear-URL, and home-dir-path scrubs land (R3, R4, R5). Even after, this is operational documentation that bakes in deployment topology — keep behind partner walls.
- `scripts/mirror-public.sh` — internal tooling for an internal sync target. Should not survive handover in its current form.
- `internal/web/devops/*` — devops console with `BodyTODO`, Brain/ paths, Python prior-art markers. Phase-1 transitional artifact (N2, N4, R9) — don't show externally until cleaned up.

## Sprint-2 ticket-shape recommendations

Ordered by priority. Each is one ticket-shape; together they form the handover sprint.

1. **HANDOVER-01: Module path rename** — Rename `github.com/growdirect-llc/rapidpos` → `github.com/ruptiv/canary`. Sweep 153 Go files, go.mod, go.sum, cloudbuild substitutions, mirror script, gateway link literals. Scope: ~155 files. Effort: M (½ day). Severity: Required (R1). Blocks all downstream tickets; landing this first reduces merge conflicts.

2. **HANDOVER-02: LICENSE entity swap + license-policy decision** — Confirm with counsel: Apache 2.0 stays? Patent 63/991,596 grant intentional? Update `LICENSE:181` to Ruptiv copyright. If patent posture changes, re-evaluate the patent-attribution comments in `cmd/sub1-*`, `cmd/sub2-*`, `cmd/sub3-*`, `cmd/gateway`, the OpenAPI YAML, the cloudbuild label, and the runbook. Scope: 1 file + counsel call + downstream attribution sweep. Effort: S coding, counsel-gated. Severity: Block (B1) + Required (R12).

3. **HANDOVER-03: Brand callouts in user-facing surfaces** — Sweep all user-facing strings: Square OAuth handler footers, OpenAPI `info.contact`, discovery doc links (`vault`, `sdds`), runbook footer URLs. Decide destination domain (suggested: `canary.ruptiv.com`). Update both static YAML and the `generate.py` source. Scope: ~10 files. Effort: M. Severity: Block (B4) + Required (R7, R8).

4. **HANDOVER-04: Dev infrastructure naming sweep** — Rename `growdirect:growdirect_dev`, `growdirect_postgres`, `growdirect_valkey`, `growdirect` Docker network → Ruptiv-owned equivalents. Sweep Makefile, compose, .env.example, GitHub Actions, 11 integration-test file headers. Coordinate with the parent `devops/docker-compose.yml` (out of CanaryGo scope but referenced via `external: true` network). Scope: ~25 files. Effort: M. Severity: Required (R2).

5. **HANDOVER-05: Runbook + cloudbuild + scripts scrub** — Strip founder username, founder home dir paths, Linear URLs, founder Gmail commit identity. Parameterize GCP project ID. Decide whether `scripts/mirror-public.sh` ships at all (recommend: delete). Scope: 3 files (runbook, cloudbuild, mirror script). Effort: M. Severity: Block (B2) + Required (R3, R4, R5, R6).

6. **HANDOVER-06: Internal positioning + sprint vocabulary scrub** — Rewrite `Bart's wedge` comment in `counterpoint/parser.go`. Rewrite "OQ Resolution Pack / founder-approved" framing in 5 files. Scope: 6 files. Effort: S. Severity: Block (B5) + Required (R11).

7. **HANDOVER-07: Test seed secret literal** — Replace `dev-only-do-not-ship-this-secret-1234567890abcdef` with a generator-produced placeholder. Add a CI guard. Scope: 1 file + 1 CI rule. Effort: M. Severity: Block (B3).

8. **HANDOVER-08: GRO ticket reference cleanup** — Sweep 252 `GRO-NNN` references in Go comments. Convert to opaque internal-spec references or strip entirely. Lower-priority but mechanical and high-volume. Scope: ~250 lines, ~80 files. Effort: L. Severity: Required (R10). Can be deferred one sprint if HANDOVER-01 through 07 land.

9. **HANDOVER-09: Devops console phase-1 cleanup** — Remove `PythonPriorArt` field from `Service` struct. Drop `Brain/wiki/cards/...` paths or relocate to in-repo docs. Rename `BodyTODO` to `Status` and gate display. Scope: 2 files + 6 references. Effort: S. Severity: Required (R9) + Recommended (N2, N4).

10. **HANDOVER-10: Sprint terminology sweep** — Lower-priority cleanup of `Loop N`, `Wave A`, `Phase B.2` vocabulary in 333 Go comments. Defer to post-handover maintenance. Scope: ~333 lines. Effort: L. Severity: Recommended (N1).

Sprint sizing: HANDOVER-01 through 07 fit comfortably in one two-week sprint with one engineer. HANDOVER-08 is the wildcard — if it slips, defer. HANDOVER-09 and 10 are post-handover quality-of-life work and don't block transfer.

## What I did NOT scan

- **Git history.** Commit messages and author emails carry founder-personal-Gmail and `bonsallprotea@gmail.com` author lines (confirmed in `mirror-public.sh:48` as a deliberate identity). A history rewrite (`git filter-repo` or `git filter-branch`) would be needed to clean these. That is destructive work and out of scope for a research scan. Recommend: handover sprint includes a decision on whether to ship the existing history (with author scrubbing) or start a fresh root commit on the Ruptiv side.
- **Secret-scanning tools.** Did not run gitleaks, trufflehog, or detect-secrets. Manual pattern scans for `sk_live_`, `pk_live_`, `BEGIN PRIVATE KEY`, `EAAAE`, `xoxb-`, `ghp_`, JWT-shaped strings returned zero hits. A real secret scanner pass should land in the handover sprint as a CI gate.
- **Frozen Python `Canary/` directory.** Out of scope per the prompt — frozen at `v0-python-prototype` tag, not part of the handover bundle. The Python prior-art comments in `internal/web/devops/devops.go` reference paths there but the destination doesn't transfer.
- **`Brain/` Obsidian vault.** Out of scope. The vault is the founder's personal knowledge environment and explicitly does not transfer. References from CanaryGo into Brain/ paths are flagged in N4.
- **Upstream `go.sum` dependencies.** Did not perform a full SBOM / license audit on indirect dependencies. The Apache 2.0 / MIT / BSD distribution looks normal at a glance, but a formal SBOM run (e.g., `go-licenses`) should land before handover. No copyleft (AGPL/GPL) was spotted in the imports list.
- **Generated code.** `internal/db/query/<service>/` is sqlc-generated. Not hand-edited; the seed comments propagate from `99_seed.sql`. Covered in the seed remediation (B3, N6) since the source is the SQL.
- **Test fixtures across the wider repo.** Scanned only what's reachable from `CanaryGo/`. The `services/canary-protocol/coverage/` and `manifest/` directories were spot-checked but not exhaustively.
- **Non-text binary artifacts.** No images, screenshots, or PDFs in the CanaryGo tree (verified). Generated diagrams and assets that ship with documentation surfaces (e.g., the OpenAPI rendered page) were not opened — string scan only.
