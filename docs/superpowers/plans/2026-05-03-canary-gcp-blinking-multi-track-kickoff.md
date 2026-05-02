# Canary Protocol — GCP-API-Blinking MVP — Multi-Track Kickoff

**Plan ID:** `2026-05-03-canary-gcp-blinking-multi-track-kickoff`
**Author:** ALX · Date: 2026-05-02 (for next session execution)
**Mode:** state · autonomous · subagent-driven where parallelizable

---

## Mission for this session

End the session with the Canary Protocol Gateway **deployed to GCP, reachable at a real URL, accepting signed webhooks from outside the laptop, and staging the events into a real Cloud SQL Postgres** — with the legal/permissions posture explicitly documented and at least drafted so we can point at it in partner conversations.

Stretch: also have the L1 Evidence Store (`protocol.evidence` write-once table) consuming from the events stream so submitted webhooks land as durable evidence rows, not just queue entries.

**This is the "GCP-API-blinking-receiving-staging" MVP** per founder direction 2026-05-02. See [GRO-739](https://linear.app/growdirect/issue/GRO-739) for the strategic reorder context.

---

## Pre-flight (≤5 minutes, before spawning anything)

Run these in parallel to confirm state:

1. `git status` and `git log --oneline -5` from `/Users/gclyle/GrowDirect` — confirm no orphaned uncommitted work; expect to see `733a665` (GRO-746 integration) as the most recent dispatch commit.
2. `docker ps --filter "name=growdirect" --format "table {{.Names}}\t{{.Status}}"` — confirm `growdirect_postgres` and `growdirect_valkey` are healthy and Up.
3. `gh auth status` — confirm GitHub CLI is authenticated (we'll need it for branch pushes).
4. `gcloud auth list` and `gcloud config list` — confirm GCP CLI is authenticated and the right project is set. **If gcloud isn't authenticated, stop and tell the founder.**
5. Read this file's referenced predecessor: `docs/superpowers/plans/2026-05-02-canary-protocol-phase1-execution-plan.md` — the original Phase 1 plan; this session's plan supersedes the priority order but inherits the dispatch inventory.
6. Read parent dispatch [GRO-739](https://linear.app/growdirect/issue/GRO-739) latest comments — the strategic reorder is captured there.
7. `memory_recall("project_canary_is_customer_of_protocol")` and `memory_recall("project_gcp_commitment_locked")` — load architectural context into working memory.

**Hard stop conditions:** if (1) Docker stack is down, (2) gcloud isn't authenticated, or (3) `git status` shows surprise uncommitted work in `CanaryGo/` — stop, ask the founder, do not proceed autonomously.

---

## Strategy: 4 waves, parallel where dependencies permit

```
Wave 1 ──► Spawn 5 design/implementation subagents in parallel
   │
   ▼
Wave 2 ──► Coordinator reviews; sequences any required follow-ups
   │
   ▼
Wave 3 ──► Wire tracks together; per-dispatch commits on topic branches
   │
   ▼
Wave 4 ──► GCP deploy the gateway; verify api.canary.growdirect.io blinks
```

Time budget — be explicit about it. Total session: ~6-8 focused hours. Per wave:
- Wave 1: ~2-3 hours subagent work in parallel (each subagent budgets independently)
- Wave 2: ~30 min coordination + integration planning
- Wave 3: ~1-2 hours per-track commits and integration
- Wave 4: ~1-2 hours GCP deploy + smoke test
- Buffer: ~1 hour for surprises and the founder's interrupts

If a subagent's work falls behind budget, **commit what's done**, leave handoff notes in the dispatch comment, and move on. Don't perfect when you can ship.

---

## Wave 1 — File the new dispatch + spawn 5 parallel subagents

### 1.0 — Coordinator-only setup (10 min)

Before spawning anything, the coordinator (you) does:

1. **File the new GCP-deployment dispatch** as `Phase 1.J` under [GRO-739](https://linear.app/growdirect/issue/GRO-739) via Linear MCP `save_issue`. Title: `Phase 1.J — Deploy Canary Protocol Gateway to GCP (Cloud Run + Cloud SQL + Memorystore + Secret Manager + custom domain)`. Use the same `["any","Canary Builder","Feature"]` labels as the others. Description should reference: this plan, the gateway code at `CanaryGo/cmd/gateway/`, and the patent (Application 63/991,596).
2. **Update priorities on the compliance dispatches** — bump GRO-687, GRO-693, GRO-694, and GRO-748 to High (priority=2) since they're now on the MVP critical path.
3. **Create five worktrees** so each subagent can work in isolation without stepping on others. Use `git worktree add` from `/Users/gclyle/GrowDirect`. Branch names should be the Linear-generated ones (e.g., `gclyle/gro-693-...`).

### 1.1 — Subagent A: GRO-693 — Compliance & Legal documentation track

**Subagent type:** `general-purpose`. Run in background.

**Self-contained prompt to give the subagent:**

> You're working on GRO-693 of the Canary Protocol GCP-MVP push. Mission: produce the legal-acceptance documentation needed to receive merchant data on `api.canary.growdirect.io` with proper permissions.
>
> Context to load before starting:
> - `Brain/wiki/cards/platform-thesis.md` (the four accountability rails)
> - `Brain/wiki/canary-closed-loop-cost-attribution.md` (governance principles)
> - `docs/_archive/ip-vault/Canary_Bitcoin_Architecture_Research_Paper_v1.0.md` (PhD position paper)
> - The patent visuals at `docs/_archive/ip-vault/patent-visuals/Patent_DataSovereignty_Stack_v1.0.html` (sovereignty model that supports the DPA framing)
> - Memory: `project_pci_scope_phase4`, `project_data_hosting_compliance_phase4`, `feedback_working_documents_not_pitch_decks`
>
> Deliverables (commit per file):
> 1. `docs/legal/dpa-template-v0.1.md` — Data Processing Agreement template, GDPR-aligned, customizable per-merchant. Working-document discipline: clauses are tables not prose where possible. Cover: roles (controller / processor), categories of data, processing purposes, sub-processor list, security measures, breach notification SLAs, audit rights, deletion guarantees, governing law variants.
> 2. `docs/legal/subprocessor-list-v0.1.md` — Current subprocessor list (GCP, OrdinalsBot if/when active, Lightning provider TBD, Cloudflare DNS). Per-subprocessor: legal name, role, data categories accessed, region, link to their DPA.
> 3. `docs/legal/breach-runbook-v0.1.md` — IR plan for data-breach scenarios: detection, triage, notification timeline (72-hour GDPR), forensic evidence preservation, stakeholder comms templates. Reference Canary's evidence-chain immutability as a forensic asset.
> 4. `docs/legal/ir-plan-v0.1.md` — Broader incident response plan covering security incidents beyond data breach (DDoS, key compromise, infrastructure failure). Reference the Cockroach Principle (rebuild paths) as a recovery asset.
>
> Working norms:
> - These are working documents (per memory `feedback_working_documents_not_pitch_decks`). No marketing copy. Tables, references, named owners, named timelines.
> - All four documents are v0.1 drafts; flag clauses requiring outside counsel review.
> - Cite specific regulations (GDPR articles, CCPA sections) where they apply.
> - Patent claims (Bitcoin-anchored evidence chain, .jeffe global identity, Cockroach Principle rebuild paths) are competitive advantages — document them in the security-measures sections.
>
> Commit on the `gclyle/gro-693-...` branch. On completion, post a Linear comment on GRO-693 with: file paths, brief one-paragraph summary of each deliverable, and a flag list of clauses requiring outside-counsel review.
>
> Budget: 90 minutes. If you fall behind, commit what's done and note remaining work in the comment.

### 1.2 — Subagent B: GRO-694 — Audit logging design + middleware implementation

**Subagent type:** `general-purpose`. Run in background.

**Self-contained prompt:**

> You're working on GRO-694 of the Canary Protocol GCP-MVP push. Mission: design and implement structured audit logging that records every state-mutating MCP tool / handler invocation into a Postgres audit log.
>
> Context to load:
> - `CanaryGo/cmd/gateway/main.go` (existing structure; you'll add middleware here)
> - `CanaryGo/internal/protocol/webhook/handler.go` (the handler to wrap)
> - `CanaryGo/deploy/migrations/009_identity_sessions_audit.up.sql` (existing audit_log schema — read first before designing yours)
> - Memory: `feedback_just_commit_no_three_card_monte`, `project_canary_is_customer_of_protocol`
>
> Deliverables:
> 1. `CanaryGo/deploy/migrations/016_protocol_audit_log.up.sql` — extends or augments `app.audit_log` with protocol-specific fields if needed (decision: prefer reusing `app.audit_log` over creating a parallel table).
> 2. `CanaryGo/internal/protocol/audit/audit.go` — Go middleware that captures: actor (merchant_id from header), action (HTTP method + path), entity_type, entity_id (event_id once minted), payload digest, source IP, user agent, request_id, latency_ms, status_code. Insert per-request into `app.audit_log`.
> 3. `CanaryGo/internal/protocol/audit/audit_test.go` — unit tests with a mock writer.
> 4. Update `CanaryGo/cmd/gateway/main.go` to mount the middleware on the protocol routes.
>
> Working norms:
> - The middleware must NOT block on insert failure — log a warning and continue (audit gaps are recoverable; refusing webhooks is not).
> - Insert via the existing `pgxpool.Pool` from main.go.
> - Honor `request_id` if present in headers (X-Request-ID), generate UUID if absent.
> - Run `go vet ./...` and `go test ./internal/protocol/audit/...` before committing.
>
> Commit on `gclyle/gro-694-...` branch. Post Linear comment on GRO-694 with: commit SHA, paths, sample audit_log row screenshot, test output.
>
> Budget: 90 minutes.

### 1.3 — Subagent C: GRO-748 — L1 Evidence Store schema + Sub 1 worker

**Subagent type:** `general-purpose`. Run in background.

**Self-contained prompt:**

> You're working on GRO-748 of the Canary Protocol GCP-MVP push. Mission: build the L1 Evidence Store — write-once Postgres table with hash chaining — and the Sub 1 worker that consumes from the gateway's Valkey Streams `protocol:events` and writes to it.
>
> Context to load:
> - The patent: `docs/_archive/ip-vault/patent-visuals/Patent_SixNode_Architecture_v2.0.html` (Sub 1 = Node 3, Hash & Seal)
> - `docs/_archive/ip-vault/patent-visuals/Patent_DataSovereignty_Stack_v1.0.html` (L1 Index, immutable JSONB)
> - `CanaryGo/internal/protocol/publisher/publisher.go` (Event envelope you'll consume)
> - `CanaryGo/deploy/migrations/015_protocol_source_secrets.up.sql` (the protocol schema you're extending)
> - `CanaryGo/internal/protocol/webhook/integration_test.go` (pattern for integration tests)
> - Memory: `project_canary_is_customer_of_protocol`, `project_canary_chain_is_storage`
>
> Deliverables:
> 1. `CanaryGo/deploy/migrations/017_protocol_evidence.up.sql` — `protocol.evidence` table: `(event_id uuid PK, event_hash text NOT NULL UNIQUE, chain_hash text NOT NULL, prev_chain_hash text, source_code text NOT NULL, merchant_id uuid NOT NULL, raw_payload jsonb NOT NULL, ingested_at timestamptz NOT NULL DEFAULT now())` plus Postgres TRIGGER blocking UPDATE and DELETE on this table (append-only enforcement at the DB level).
> 2. `CanaryGo/cmd/sub1-hash-seal/main.go` — new service binary. Reads events from Valkey Streams `protocol:events` consumer group `sub1-hash-seal`. For each: compute `chain_hash = SHA-256(event_hash || prev_chain_hash || timestamp)`, INSERT into `protocol.evidence`, ACK the message. Per-merchant chain (one chain per merchant_id).
> 3. `CanaryGo/internal/protocol/sub1/seal.go` — the chain-hash logic, separated for unit testability.
> 4. `CanaryGo/internal/protocol/sub1/seal_test.go` — unit tests for chain integrity, idempotency on duplicate event_hash, UPDATE/DELETE-blocked regression test.
> 5. `CanaryGo/internal/protocol/sub1/integration_test.go` — integration test (build tag `integration`) that runs the full pipeline: gateway accepts a signed webhook → event lands in Valkey Streams → Sub 1 consumes → evidence row appears in Postgres.
>
> Working norms:
> - DDL must enforce append-only via Postgres TRIGGER, not application code (defense in depth).
> - Sub 1 worker must be safe to restart mid-stream (consumer group offset recovery).
> - Bilateral verification API surface (`GET /v1/protocol/evidence/{event_hash}`) is reserved in the OpenAPI spec already (GRO-740) — implement the handler in `CanaryGo/cmd/gateway/main.go` mounting the read query on the existing chi router.
> - Run `go vet ./...` and `go test -tags=integration ./internal/protocol/sub1/...` before committing.
>
> Commit on `gclyle/gro-748-...` branch. Post Linear comment with commit SHA, test output, sample chain_hash sequence verifying integrity.
>
> Budget: 2 hours.

### 1.4 — Subagent D: GRO-687 — GCP Secret Manager integration

**Subagent type:** `general-purpose`. Run in background.

**Self-contained prompt:**

> You're working on GRO-687 of the Canary Protocol GCP-MVP push. Mission: replace plaintext secret storage in `protocol.source_secrets` with GCP Secret Manager-backed envelope encryption, while preserving the existing `secrets.Resolver` interface.
>
> Context to load:
> - `CanaryGo/internal/protocol/secrets/secrets.go` (the interface you preserve)
> - `CanaryGo/deploy/migrations/015_protocol_source_secrets.up.sql` (the table; note the GRO-687 callout in the comments)
> - GCP Secret Manager docs: https://cloud.google.com/secret-manager/docs/overview
> - Memory: `project_gcp_commitment_locked`, `project_no_hand_rolling_outside_core_ip`
>
> Deliverables:
> 1. `CanaryGo/internal/protocol/secrets/sm_resolver.go` — `SmResolver` type that satisfies `secrets.Resolver` but reads secrets from GCP Secret Manager. Secret naming convention: `projects/{PROJECT}/secrets/canary-source-{merchant_id}-{source_code}/versions/latest`. Look up `protocol.source_secrets` row for metadata (signature_algo, replay_window_seconds, status), then fetch the actual secret value from SM.
> 2. `CanaryGo/internal/protocol/secrets/sm_resolver_test.go` — unit tests with a mocked SM client.
> 3. `CanaryGo/deploy/migrations/018_protocol_source_secrets_sm_ref.up.sql` — adds `secret_sm_ref text` column (full SM resource path) and makes existing `secret` column nullable. Migration plan documented.
> 4. `docs/sdds/canary-go/secrets-manager-integration.md` — design doc explaining: SM resource layout, IAM policy required (the gateway SA needs `roles/secretmanager.secretAccessor` on the canary-source-* secrets), rotation flow, audit logging of secret accesses (Cloud Audit Logs are automatic), cost model (~$0.06/secret/month + $0.03/10k accesses).
> 5. Update `CanaryGo/cmd/gateway/main.go` to optionally use `SmResolver` based on env var `SECRET_BACKEND=sm` (default: `pgx` for dev, `sm` for prod).
>
> Working norms:
> - The interface stays — only the implementation changes.
> - Secrets fetched from SM should be cached in-memory with short TTL (~60s) to avoid hammering SM on every request.
> - Secret value MUST NOT be logged. Sanitize zap output explicitly.
> - For local dev (no GCP creds), fall back to PgxResolver gracefully — print warning at startup if SECRET_BACKEND=sm but no GCP creds.
>
> Commit on `gclyle/gro-687-...` branch. Post Linear comment with commit SHA, design doc summary, and the IAM policy needed for production.
>
> Budget: 2 hours.

### 1.5 — Subagent E: Phase 1.J — GCP deployment of the gateway

**Subagent type:** `Plan` (the architect agent — this is design-heavy). Run in background.

**Self-contained prompt:**

> You're designing Phase 1.J of the Canary Protocol GCP-MVP push: deploy the existing API Gateway (`CanaryGo/cmd/gateway/`) to GCP so `api.canary.growdirect.io` lights up. Other subagents are building L1 Evidence Store, Secret Manager integration, and audit logging in parallel — your design must accommodate them.
>
> Context to load:
> - `CanaryGo/cmd/gateway/main.go` (the service to deploy)
> - `CanaryGo/deploy/` directory (existing Dockerfile patterns — peek at `Dockerfile.identity`)
> - `CanaryGo/Makefile` (existing build/migrate targets)
> - GRO-700 (drop-zone CI/CD on GCP — already done; reuse this substrate) — fetch via Linear MCP
> - Memory: `project_gcp_commitment_locked`, `project_cloud_provider_accountability_stance`, `feedback_no_hand_rolling_outside_core_ip`
>
> Deliverables (no code yet — pure design + actionable runbook):
> 1. `docs/sdds/canary-go/gcp-deployment-gateway.md` — full GCP deployment design covering:
>    - **Cloud Run service** for the gateway (containerized via existing Dockerfile pattern; min instances 1 for warmup, max 10 initially)
>    - **Cloud SQL Postgres 17** with pgvector — replication topology, backup schedule, connection pooling via Cloud SQL Auth Proxy or private IP
>    - **Memorystore Redis** for the Valkey Streams substitute (Valkey isn't on GCP; we use Redis + the same go-redis client — verify XADD/XREAD compatibility)
>    - **Cloud Load Balancer** + Cloud Armor + custom domain `api.canary.growdirect.io` (managed cert, HTTP→HTTPS redirect, basic WAF rules)
>    - **Secret Manager** holding HMAC source secrets (per GRO-687) — list the required secrets at deploy time
>    - **IAM** — service accounts (one per service), least-privilege bindings, Workload Identity for Cloud Run if applicable
>    - **Cloud Logging** — structured logs from zap → Log Analytics; export to BigQuery for SQL queries; retention policy
>    - **Cloud Monitoring** — uptime checks, latency alerts (p99 > 5ms over 5min), 5xx rate alerts, Cloud SQL CPU/connections alerts
>    - **Cloud Build** trigger on `gclyle/gro-746-...` push → build container → deploy to Cloud Run staging
>    - **Migration runner** — Cloud Run job that runs `migrate up` against Cloud SQL on deploy
>    - **Cost estimate** — monthly bill at low traffic (target: <$100/mo for the MVP; this becomes the "is this production-grade" pressure test)
> 2. `CanaryGo/deploy/Dockerfile.gateway` — Dockerfile for the gateway service (multi-stage Go build, distroless final image).
> 3. `CanaryGo/deploy/cloudbuild.gateway.yaml` — Cloud Build config that pushes to Artifact Registry and deploys to Cloud Run.
> 4. `CanaryGo/deploy/terraform/gateway/` OR `CanaryGo/deploy/scripts/deploy-gateway.sh` — your call: Terraform if the founder has Terraform state already, otherwise gcloud scripts. Either way, idempotent so we can re-run safely.
> 5. `CanaryGo/deploy/runbook-gateway-deploy.md` — step-by-step human runbook: what to run, in what order, how to verify, how to roll back. The coordinator (next session) will execute this in Wave 4.
>
> Working norms:
> - Per memory `feedback_no_hand_rolling_outside_core_ip`: prefer GCP managed services over hand-rolled. Cloud Run > GKE for this. Cloud SQL > self-managed Postgres. Secret Manager > Vault.
> - Per memory `project_cloud_provider_accountability_stance`: bake in active SLA enforcement. Document the SLOs we're holding GCP to and how we'll measure them.
> - Per `project_gcp_commitment_locked`: this is the production target, not a sandbox. Treat it that way.
> - Cost discipline: this is solo-founder economics. Every dollar of cloud spend needs justification. Free tiers and minimum-instance configs where they don't compromise the mission.
> - The runbook is the deliverable. The next-session coordinator picks up the runbook and executes it. Make it executable cold by someone who hasn't been in this conversation.
>
> Commit on `gclyle/gro-deploy-...` branch (file the dispatch first to get the GRO number). Post Linear comment on the new dispatch with: design doc summary, cost estimate, deployment runbook entry-point command.
>
> Budget: 2.5 hours.

---

## Wave 2 — Coordinator review + integration sequencing (~30 min)

When all 5 subagents have reported back, the coordinator (you):

1. **Read each subagent's commit** — `git log --oneline` on each branch, scan the diffs.
2. **Identify integration conflicts** — does the audit middleware step on the gateway main.go in a way that breaks the L1 worker's wiring? Does the SM resolver land before the L1 worker tries to use it?
3. **Sequence the merges** — build a tiny merge-order plan:
   - First: GRO-694 audit middleware (touches only `cmd/gateway/main.go` route registration)
   - Second: GRO-687 Secret Manager (touches `secrets/` and `cmd/gateway/main.go` config wiring)
   - Third: GRO-748 L1 Evidence Store (new service binary + new migration; doesn't touch gateway except for the read-handler addition)
   - Fourth: GRO-693 legal docs (no code; merge to main directly)
   - Fifth: Phase 1.J GCP deployment (design + scripts only at this point)
4. **Resolve any subagent confusion** — if a subagent left handoff notes ("I couldn't figure out X, please review"), address them directly.

**If a subagent failed cleanly** (committed partial work + clear handoff): note the gap, decide whether to (a) push through with what's done, (b) spawn a follow-up subagent, or (c) drop to next session. Don't perfect.

**If a subagent failed messily** (uncommitted state, contradictory work): roll back that worktree, file a Linear comment on the dispatch with what went wrong, drop to next session.

---

## Wave 3 — Per-track commits + branch hygiene (~1-2 hours)

For each completed track (in the merge order above):

1. Switch to the topic branch.
2. Run full test suite: `go test ./...` (unit), then `go test -tags=integration ./...` (integration, against running Docker stack).
3. Run `go vet ./...` and `gofmt -l ./...` — fix any flagged issues.
4. **If green:** transition Linear dispatch to Done, post ship comment with commit SHA + test output. Push the branch via `git push -u origin <branch>` if not already pushed.
5. **If red:** capture the failure, post a comment with the diagnosis, leave dispatch In Progress, move on.
6. Update `MEMORY.md` if anything strategically novel emerged.
7. Reseed memory bus if `Brain/wiki/` changed: `python3 services/memory-bus/scripts/seed_standalone.py`.

---

## Wave 4 — GCP deployment (the blinking moment) (~1-2 hours)

**Pre-condition:** Phase 1.J subagent's runbook is committed and reviewed.

1. **Provision** — execute the runbook from `CanaryGo/deploy/runbook-gateway-deploy.md` step-by-step. If the runbook says "create a GCP project," that's an interactive step — pause and ask the founder to confirm the project name + region.
2. **Cloud SQL setup** — create the instance, run all migrations 001-018 (or however many we have post-Wave-3), confirm `protocol.evidence` and `protocol.source_secrets` exist.
3. **Memorystore Redis** — provision, capture connection string.
4. **Secret Manager** — create one test secret for a sample merchant (`canary-source-{merchant_id}-square`); store the HMAC key.
5. **Cloud Run** — deploy the gateway image; wire DATABASE_URL, VALKEY_URL (will be Memorystore Redis URL), SECRET_BACKEND=sm, GCP_PROJECT.
6. **Custom domain** — wire `api.canary.growdirect.io` (Cloudflare DNS → Cloud LB → Cloud Run). Wait for managed cert provisioning (5-30 min).
7. **Smoke test from outside** — from the laptop, send a signed webhook to the live URL. Verify 200 OK, verify Cloud SQL row exists in `protocol.evidence`, verify Memorystore stream `protocol:events` has the entry.
8. **Capture screenshots** — Cloud Run dashboard, Cloud SQL row, Memorystore monitoring, the actual `curl` response. Attach to GRO-1.J ship comment.
9. **Fire it off**: Linear comment on GRO-739 announcing **`api.canary.growdirect.io` is live and accepting signed webhooks**. Tag it strategically.

**If something breaks at step N:** capture the exact error, capture the runbook line where it failed, post on GRO-1.J with full repro, leave it In Progress, drop to next session. Don't panic-debug GCP issues at hour 7 of the session — they compound.

---

## Success criteria (what "good" looks like at session end)

The session is a **major win** if:

- ✅ `api.canary.growdirect.io` returns a 200 OK to a signed webhook from outside the laptop
- ✅ The event landed in Cloud SQL `protocol.evidence` with hash chain integrity
- ✅ The DPA template + subprocessor list + breach runbook are committed and reviewable
- ✅ All 5 dispatches (746/687/693/694/748/1.J) shipped or progressed-with-handoff
- ✅ Cost estimate documented; we know what GCP is costing us

The session is a **minor win** if:

- ✅ All Wave 1-3 work shipped to topic branches with test coverage
- ✅ Phase 1.J runbook is ready for execution
- ⏸ GCP deployment itself is partially done OR deferred to next session

The session is a **failure** (rare; should require a real obstacle) if:

- ❌ Multiple subagents committed broken work that requires rollback
- ❌ Less than 50% of the work shipped
- ❌ Code in main is broken

**Per founder feedback:** ship what you have, don't perfect. A 70% delivered + clear handoff beats 100% scoped + nothing landed.

---

## Working norms (founder preferences encoded)

These are non-negotiable. They come from saved memories.

1. **No three-card monte** (`feedback_just_commit_no_three_card_monte`). When work is done and the next step is obvious, just do it. Don't surface trivial decisions for ceremonial confirmation. Reserve questions for genuine reversibility/risk.
2. **Working documents not pitch decks** (`feedback_working_documents_not_pitch_decks`). Any docs produced this session — design docs, runbooks, DPA templates — are working documents. Tables, references, named owners, no marketing copy in the body. McKinsey associate handed it on day 1 should have what they need.
3. **Files are for agents** (`feedback_files_are_for_agents`). Default audience for any vault file is the next agent. Concise, actionable, machine-readable. External-facing artifacts (DPA, public-site copy) keep human polish.
4. **Don't change OAuth redirects** (`feedback_dont_change_redirects`). N/A this session, but be aware.
5. **Flag dependency changes** (`feedback_flag_dependency_changes`). If a subagent adds a new Go dependency, the diff must include the new module + a note in the commit message. No silent additions.
6. **Patent claims are the spine** — every dispatch's DoD includes a patent-claim verification step. Drift from the patent → file a comment, not a silent change.
7. **No agent identity names externally** ("No Names Leave the Building" rule). Internal codenames stay internal. The `.jeffe` namespace IS external (per founder direction); ALX/Owl/etc. are NOT.
8. **Memory bus reseed** when `Brain/wiki/` changes: `python3 services/memory-bus/scripts/seed_standalone.py`. Commit hook handles it but verify after each push.
9. **Per-dispatch comments on pickup AND completion** — pickup comment with ETA; ship comment with commit SHA + paths + DoD verification.
10. **Brand voice** (`feedback_no_hype_copy`, `feedback_brain_content_principles`): direct, technical, no hype, no AI-sounding prose. This applies to all docs the founder will read.

---

## Files and references for the next-session coordinator

| Topic | Path |
|---|---|
| This plan | `docs/superpowers/plans/2026-05-03-canary-gcp-blinking-multi-track-kickoff.md` |
| Predecessor plan (still authoritative for dispatch inventory) | `docs/superpowers/plans/2026-05-02-canary-protocol-phase1-execution-plan.md` |
| Patent visuals | `docs/_archive/ip-vault/patent-visuals/Patent_*.html` |
| PhD research paper | `docs/_archive/ip-vault/Canary_Bitcoin_Architecture_Research_Paper_v1.0.md` |
| Closed-loop wiki | `Brain/wiki/canary-closed-loop-cost-attribution.md` · `Brain/wiki/cards/platform-closed-loop-attribution.md` |
| Platform thesis card | `Brain/wiki/cards/platform-thesis.md` |
| Gateway code | `CanaryGo/cmd/gateway/main.go` · `CanaryGo/internal/protocol/{hmac,publisher,secrets,webhook}/` |
| OpenAPI spec | `services/canary-protocol/openapi/openapi.yaml` (generated; regen via `services/canary-protocol/openapi/gen/generate.py`) |
| Linear parent dispatch | [GRO-739](https://linear.app/growdirect/issue/GRO-739) |
| Linear MVP dispatches | GRO-687 · GRO-693 · GRO-694 · GRO-748 · (Phase 1.J — to be filed) |
| Memories most relevant to this session | `project_canary_is_customer_of_protocol` · `project_gcp_commitment_locked` · `project_canary_chain_is_storage` · `project_satoshi_cost_model` · `feedback_just_commit_no_three_card_monte` · `feedback_working_documents_not_pitch_decks` |

---

## When to call the founder back (escalation triggers)

- gcloud isn't authenticated or wrong project is set
- Docker stack is down and won't come up cleanly
- Cloud SQL provisioning needs a paid project (project must already exist; founder confirms)
- Custom domain DNS — Cloudflare API access needed; founder confirms
- Cost estimate exceeds $200/mo for the MVP — back-off discussion
- A subagent committed something that contradicts a prior dispatch's assumptions in a way that needs strategic adjudication
- Patent-claim drift — anything that materially weakens an Application 63/991,596 claim
- Anything legally consequential (DPA wording that needs counsel sign-off, a regulatory question)

For everything else: ship it, log it, move.

---

## Final note to the next-session coordinator

The founder's energy on 2026-05-02 was clear: **make GCP blink**. Everything in this plan is in service of that. The OpenAPI spec, the gateway code, the Triple Subscriber pattern, the patent architecture — they all exist on disk already. What's missing is the public URL and the legal cover that lets you use it. This session ships those.

Bias toward action. Bias toward shipping. Bias toward reporting what's done over what's perfect.
