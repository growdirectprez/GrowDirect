---
title: CanaryGo Readiness Audit — Factory-Stage Classification
type: audit
status: complete
date: 2026-05-05
linear: GRO-685 (superseded — original spec exhaustion mission redirected to this audit)
author: ALX (laptop, Opus 4.7 [1M])
scope: CanaryGo build (cmd/ + internal/) + the SDD corpus + Brain wiki cards (canary/platform/infra/retail prefixes)
methodology: Two parallel inventory agents (code + spec); synthesis on Opus
---

# CanaryGo Readiness Audit — Factory-Stage Classification

## 1. Governing Thesis

**The CanaryGo spec corpus is roughly 3× the size of the build, and the build is roughly 14× the size of what is actually scheduled to run.** The platform has a deep specification layer (~60 SDDs, ~99 Brain cards), a substantial code layer (28 binaries, 39 internal packages, ~24K lines of Go), but only a thin operational surface — exactly two binaries (`gateway`, `identity`) are referenced in the deploy compose file and the Cloud Build pipeline. Everything else either runs in-process inside the gateway, builds-but-never-deploys, or exists only on paper.

This is not a failure. It is a snapshot of a build at a specific phase: post-Loop-2 architectural consolidation, pre-deployment-discipline, with a spec library that intentionally describes a target larger than the current binary set. The job of this audit is to mark each module's factory stage honestly, classify each into CORE / SUPPORT / EXPERIMENT / DRIFT against principle (not against any retailer or release date), and surface the cross-cutting findings that the per-module entries don't carry on their own.

The four tiers, restated for clarity:

- **CORE** — works, has callers, defended by tests, would break the platform if removed
- **SUPPORT** — required by CORE to function; deletion cascades into CORE failure
- **EXPERIMENT** — built and runs, but no consumer relies on it; could be parked without operational consequence
- **DRIFT** — code without a current spec, or spec without code — the gap between the SDD library and the binary set

The factory stage ladder, restated:

| Stage | Criteria |
|---|---|
| `preflight` / `research` | Brain card exists; problem identified; no spec |
| `blueprint` | SDD `status: handoff-ready` and current (`updated:` 2026-04-28 or later) |
| `tdd` | Tests exist (real fixtures, not just `/health`) |
| `assembly` | Non-trivial code in cmd/ or internal/ |
| `verify` | Code complete, unit + integration tests pass |
| `qa` | End-to-end validated, schema applied, code matches spec |
| `ship` | Referenced in a deployment artifact (compose, cloudbuild, Dockerfile) |
| `close` | Running in production with real traffic |

A module's **highest cleared stage** is its position. A module that has assembly without blueprint is DRIFT no matter how clean the code is. A module that has blueprint without assembly is DRIFT no matter how comprehensive the spec is.

---

## 2. Headline Findings

These are the cross-cutting facts the per-module entries don't carry. Read these first; the rest of the document is supporting evidence.

### Finding 1 — Deployment surface is two binaries

`deploy/docker-compose.yml` schedules `canarygo-gateway` and `canarygo-identity`. Nothing else. `cloudbuild.gateway.yaml` deploys gateway only. There are 26 other cmd/ binaries with real handlers and no place to run. The platform thesis describes a 13-module spine; the operational surface is 2.

This is the most important fact in the audit. Most of the per-module classifications below are answering a different question than "does this work in production?" — they're answering "is this real Go code that compiles, has tests, and matches a spec?" Those are necessary conditions for shipping; they are not sufficient.

### Finding 2 — Gateway is doing the work of fifteen services

The gateway binary imports 22 internal packages and registers 8 route trees: namespace, alert, MCP surface, dev console, LNURL auth, evidence/anchor read APIs, webhook ingestion, devops console. It is the only HTTP-facing service on Cloud Run staging. Effectively, every "Mount(r chi.Router)" handler in CanaryGo is wired into one process today.

This is fine for a phase-1 deploy and would be a problem if multi-tenant scaling pressure arrived. It is not a problem now. It is a fact to know.

### Finding 3 — Three internal packages are dead code

`internal/arts`, `internal/crdm`, `internal/tsp` have zero importers. `crdm/types.go` claims "All services use these types for cross-service data contracts" — that comment is false. Nothing imports it. Same for `arts` (POSLOG field constants) and `tsp` (ingest pipeline primitives). All three are removable today with no impact.

The interesting one is `crdm`. The canonical retail data model is allegedly the foundation of the platform's POS-agnosticism. The actual canonical types are in `internal/db/types/` (1788 LOC, generated from `deploy/schema/*.sql`) — that's what the adapters and protocol packages actually use. The `crdm` package is an abandoned earlier attempt.

### Finding 4 — Eljeffe is live in production gateway, not dead code

Earlier in this session I suspected `internal/protocol/namespace/` might be dead code. The wiring trace shows otherwise. `cmd/gateway/main.go:114` constructs `nsHandler := namespace.New(pool, inscriber, logger)` and `:161` mounts it on the chi router. The `.jeffe` namespace registration endpoints (`POST /v1/protocol/namespace`, `GET /v1/protocol/namespace/{name}`) are exposed on the staging Cloud Run service today.

This is louder than I implied earlier. The eljeffe-as-Bitcoin-namespace product is shipped — at least in the sense of being deployed to staging on a route that anyone with the URL can hit. It has 3 test files (the highest test density in the protocol/ tree). It is a built, deployed, tested product that has no SDD describing it.

### Finding 5 — sub3-merkle-ordinal is built but never deployed

`cmd/sub3-merkle-ordinal/main.go` is a complete worker (175 lines) with OrdinalsBot integration. Nothing in the repo schedules it: no compose entry, no Dockerfile, no cloudbuild. The `ORDINALSBOT_API_KEY` environment variable is read by both the worker and the gateway (gateway uses `protocol/sub3` for read-side anchor verification — that part runs), but no deployment artifact starts the worker process.

Implication: the L2 anchor pipeline does not actually anchor anything. Evidence rows accumulate in `protocol.evidence` with `chain_hash` values; nothing ever batches them into a Merkle root and inscribes the root onto Bitcoin. The verify_chain story is intact at the chain-hash level (every row has its predecessor's hash baked in); the public-blockchain anchor story is aspirational until the worker is actually scheduled.

### Finding 6 — cmd/raas does not exist; raas.md is a 5-table 9-tool SDD with zero implementing code

The `raas.md` SDD describes a comprehensive standalone service on `:8099` with `raas_namespaces`, `raas_source_registrations`, `raas_events`, `raas_chain_state`, `raas_subject_keys` tables and 9 MCP tools. None of those tables exist in the migrations. Nothing in `cmd/` matches `raas`. The functions the SDD describes (`ensure_namespace`, `resolve_namespace`, `register_source`, `append_event`, `verify_chain`, `return_eligible`, `event_stream`, `receipt_hash`, `receiver_attribution`) are not implemented anywhere.

What actually plays the role the SDD describes:
- `cmd/sub1-hash-seal` (the consumer worker) does the chain-hash-on-INSERT into `protocol.evidence`
- `cmd/gateway`'s embedded namespace handler does the `.jeffe` registry (different concept entirely)
- The merchant-to-POS bridge function (`raas:{merchant_id}`) is **not** implemented anywhere

The "RaaS as namespace authority for multi-POS resolution" is a spec on the shelf. The `.jeffe` namespace is something else that landed in the same general semantic space and got conflated.

### Finding 7 — Three different chain-hash algorithms are documented as the patent-critical primitive

Patent Application #63/991,596 is cited as covering "the" chain hash. Three algorithms exist:

| Source | Formula |
|---|---|
| `tsp-seal.md` SDD | `SHA-256(prev_chain_hash_bytes ‖ event_hash_bytes)` (raw byte concat, no timestamp) |
| `raas.md` SDD | `SHA-256(payload_hash + "\|" + occurred_at + "\|" + sequence_num + "\|" + prior_hash)` (pipe-delimited string with sequence_num) |
| Shipped code (`internal/protocol/sub1/seal.go:63-69`) | `SHA-256(event_hash ‖ prev_chain_hash ‖ ts.UTC().Format(RFC3339Nano))` (with timestamp, no sequence_num) |

`tsp-seal.md` claims its algorithm is "identical to the chain hash algorithm in raas.md." It is not. The shipped code matches neither SDD.

This is the highest-stakes single finding in the audit. The patent claim references a specific algorithm; the documented architecture references a different one; the shipped code references a third. Whichever is filed in #63/991,596 is canonical; the other two need to be retired before the inconsistency surfaces in a patent challenge or a customer audit. **Action: pull the patent application text and confirm the filed algorithm before any further protocol work.**

### Finding 8 — POS failover queue is unspecified

`platform-performance-nfrs.md` Brain card asserts "if the platform event endpoint is unreachable, the local POS adapter queues events locally (SQLite, capped at 24 hours of nominal transaction volume) and replays on reconnect." This is the field-capture invariant extended to POS — the timestamp is when the event happened, not when the network recovered.

No SDD covers this. `cmd/edge` exists as a directory but its current implementation is a Counterpoint REST poller, not a write-side resilience buffer. Any pilot retailer with a flaky network connection would lose receipts during an outage. This is a real-world readiness gap that the spec corpus does not address.

### Finding 9 — Test depth is uneven; most cmd/ binaries have zero tests

Across the 28 cmd/ binaries, exactly **one** has any test files (`cmd/identity`, with `main_test.go`). Across the 39 internal/ packages, the highest test density is `internal/web` (5 tests), `internal/fox` (3), `internal/owl` (3), `internal/protocol/sub3` (3), `internal/protocol/namespace` (3). Most packages have 0–2 test files. The largest internal package by line count, `internal/db/types/` (1788 LOC of schema-aligned types), has **zero** tests.

This is not a bad smell on its own — many packages are thin handlers around well-tested DB queries — but it does mean the `verify` factory stage is achievable for very few modules using strict criteria. Either the criteria flex (smoke + integration suffices) or most modules are stuck at `assembly`.

### Finding 10 — Spec library is intentionally larger than the build, but a meaningful portion is shelf-spec

41 SDDs of ~60 have no implementing binary. Some of those are meta/architecture documents that don't expect a binary (`architecture.md`, `microservice-architecture.md`, `platform-overview.md`, `factory-pipeline.md`, the `go-*.md` library cards) and that's fine. But others describe specific services that simply do not exist:

- `blockchain-anchor.md` (cmd/blockchain-anchor :9086) — no binary
- `commercial.md` (cmd/commercial :9089) — no binary
- `compliance.md` (cmd/compliance :9091) — no binary
- `device-contracts.md` (cmd/device-contracts :9083) — no binary
- `field-capture.md` (cmd/field-capture :9087) — no binary
- `ildwac.md` (cmd/ildwac :9082) — no binary
- `l402-otb.md` (cmd/l402-otb :9090) — no binary
- `ops-dashboard.md` (cmd/ops-dashboard :9084) — no binary
- `party-identity-design.md` (cmd/party :8094) — no binary
- `raas.md` (cmd/raas :8099) — no binary
- `store-brain.md` (cmd/store-brain :9085) — no binary
- `store-network-integrity.md` (cmd/store-network-integrity :9088) — no binary

These are all `status: handoff-ready` with `updated: 2026-04-29` or later. They describe a target architecture larger than the current build. Whether to build any specific one of them is a roadmap question this audit doesn't answer; the fact that they exist as `handoff-ready` SDDs without code is a DRIFT signal at the corpus level.

---

## 3. Front-Page Classification Table

One row per cmd/ binary plus the significant internal/ packages. Skim this top-to-bottom in 5 minutes; the per-tier sections below carry the rationale.

### 3.1 cmd/ binaries

| binary | stage | tier | one-line note |
|---|---|---|---|
| `gateway` | `ship` | **CORE** | Live on Cloud Run staging; 22 internal pkg imports; only HTTP front door |
| `identity` | `ship` | **CORE** | Live on Cloud Run staging; per-agent API key auth substrate |
| `sub1-hash-seal` | `verify` | **CORE** | Loop 2 keystone; `protocol.evidence` write path; chain-hash-on-INSERT |
| `sub2-parse-route` | `verify` | **CORE** | Loop 2 keystone; multi-POS substrate (Square + Counterpoint + Clover) |
| `sub3-merkle-ordinal` | `assembly` | EXPERIMENT | Builds; never deployed; ORDINALSBOT_API_KEY unset; L2 anchor aspirational |
| `chirp` | `verify` | **CORE** | Loop 2; 7 stateless detection rules; on_event invocation |
| `fox` | `verify` | **CORE** | Loop 2; case management; 3 test files; reads detections, writes cases |
| `owl` | `verify` | **CORE** | Loop 2; read-only analytics; 3 test files; surfaces schema gaps |
| `item` | `verify` | **CORE** | Loop 2; item master CRUD; UPSERT-in-tx pattern; 2 test files |
| `pricing` | `verify` | **CORE** | Loop 2; price + promotion + tax resolver; 2 test files |
| `inventory` | `verify` | **CORE** | Loop 2; SOH consumer; 2 test files; large pkg (1145 LOC) |
| `transaction` | `assembly` | SUPPORT | Real handler; canonical write path for transaction.* tables; 0 tests |
| `analytics` | `assembly` | EXPERIMENT | Real Mount, no tests, no consumer running today (gateway uses internal/analytics directly) |
| `alert` | `assembly` | EXPERIMENT | Real Mount; alerts on detections; not deployed; 0 tests |
| `asset` | `assembly` | EXPERIMENT | Real Mount; reads inventory + items; 0 tests; not deployed |
| `bull` | `assembly` | EXPERIMENT | NCR/replenishment scaffold; reads ledger.ildwac_positions; 0 tests; not deployed |
| `case` | `assembly` | EXPERIMENT | Workflow registration + Mount; 0 tests; redundant with hawk |
| `customer` | `assembly` | EXPERIMENT | Real Mount; reads customers + loyalty; 0 tests; not deployed |
| `employee` | `assembly` | EXPERIMENT | Real Mount; reads employees + detections; 0 tests; not deployed |
| `hawk` | `assembly` | EXPERIMENT | 5 routes for case management; 0 tests; not deployed |
| `report` | `assembly` | EXPERIMENT | Real Mount; report job queue; 0 tests; not deployed |
| `returns` | `assembly` | EXPERIMENT | Real Mount; reads transactions + detections; 0 tests; not deployed |
| `edge` | `assembly` | EXPERIMENT | Counterpoint REST poller worker; 0 tests; not deployed; NOT the POS failover edge |
| `dbcheck` | `verify` | SUPPORT | Smoke probe; verifies pgvector extension; has Dockerfile; not in compose |
| `hello` | `assembly` | EXPERIMENT | Smoke service; `/health` only; has Dockerfile; not in compose |
| `receiving` | `preflight` | DRIFT | `/health` stub only; comprehensive SDD with no implementing code |
| `transfer` | `preflight` | DRIFT | `/health` stub only; no SDD |
| `tsp` | `preflight` | DRIFT | `/health` stub only; supplanted by sub1/sub2/sub3 |

### 3.2 internal/ packages — load-bearing only

The trivial packages (`config`, `db`, `obs`, `pagination`, `tenant`, `testutil`) are utility infrastructure and aren't classified individually; they're all `assembly` stage and SUPPORT tier by definition. The packages below are the ones with strategic weight.

| package | stage | tier | one-line note |
|---|---|---|---|
| `adapters` (+ square/counterpoint/clover) | `verify` | **CORE** | POS adapter substrate; the multi-POS thesis lives here |
| `chirp` (+ chirp/rules) | `verify` | **CORE** | Detection engine; 1140 + 796 LOC |
| `db/types` | `verify` | SUPPORT | 1788 LOC of schema-aligned Go types; **0 tests** but generated from SQL |
| `fox` | `verify` | **CORE** | Case management core; 1529 LOC; 3 test files |
| `identity` | `verify` | **CORE** | API key middleware; 38 importers — most-imported package in repo |
| `inventory` | `verify` | **CORE** | SaleConsumer; SOH decrement; 1145 LOC |
| `item`, `pricing`, `customer`, `employee`, `transaction`, `analytics`, `asset`, `returns`, `report` | `verify` or `assembly` | **CORE** or SUPPORT | Domain CRUD; each consumed by its cmd/ binary and by gateway |
| `mcp` | `assembly` | SUPPORT | Wraps domain packages for the MCP surface; 916 LOC; mounted only on gateway |
| `owl` | `verify` | **CORE** | Analytics + dashboard; 1037 LOC; 3 test files |
| `protocol/anchor` | `assembly` | SUPPORT | Read-side anchor verification API; mounted on gateway |
| `protocol/audit` | `verify` | SUPPORT | Audit log middleware; 2 test files; chi-compatible |
| `protocol/cockroach` | `tdd` | EXPERIMENT | Test-only build tag; validates Cockroach Principle (no production callers) |
| `protocol/evidence` | `assembly` | SUPPORT | Read-side L1 evidence API; mounted on gateway |
| `protocol/hmac` | `verify` | **CORE** | HMAC-SHA256 webhook signature verification; patent Node 2 |
| `protocol/namespace` (eljeffe) | `assembly` | DRIFT | LIVE in gateway; **no SDD covers this**; `.jeffe` registry on Bitcoin |
| `protocol/publisher` | `verify` | **CORE** | Valkey publish abstraction; 23 callers (highest fan-in) |
| `protocol/secrets` | `verify` | SUPPORT | Per-source webhook secret resolution |
| `protocol/sub1` | `verify` | **CORE** | Sub-1 hash-seal; chain-hash-on-INSERT; 2 test files; **chain hash variant problem** |
| `protocol/sub2` | `verify` | **CORE** | Sub-2 parse-route; calls adapter.ParseAndRoute; 2 test files |
| `protocol/sub3` | `verify` | EXPERIMENT | Merkle + Ordinal; package wired into gateway read API; worker not scheduled |
| `protocol/validate` | `assembly` | SUPPORT | L402 verification token store; 612 LOC |
| `protocol/webhook` | `verify` | **CORE** | Gateway POST handler; patent Node 2; 2 test files |
| `auth/lnurl` | `assembly` | EXPERIMENT | LNURL-auth login surface (GRO-753); mounted on gateway; 2 test files |
| `billing` | `assembly` | DRIFT | Bull L402-OTB satoshi rollup; reads ledger.ildwac_positions but no `cmd/l402-otb` consumes it |
| `casemgmt` | `assembly` | DRIFT | Standalone case mgmt API; **no SDD** uses this name; redundant with fox |
| `lp` | `assembly` | SUPPORT | Read-only access to detection.lp_substrate + allow_list |
| `poller` | `assembly` | EXPERIMENT | NCR Counterpoint poll loop for cmd/edge; not deployed |
| `replenishment` | `assembly` | EXPERIMENT | Min/Max trigger; subscribes to inventory:replenish stream; not deployed |
| `task` | `assembly` | EXPERIMENT | /v1/tasks queue for mobile operators; not deployed |
| `web` | `verify` | SUPPORT | Server-rendered web UI; 5 test files (highest density); mounted on gateway |
| `webhook` | `verify` | SUPPORT | Per-(merchant,source) rate limiting; 1 test file |
| `workflow` | `assembly` | EXPERIMENT | Investigation lifecycle workflow definition; not deployed |
| `arts` | (n/a) | DRIFT | **0 callers** — DEAD CODE candidate |
| `crdm` | (n/a) | DRIFT | **0 callers** — DEAD CODE candidate; comment falsely claims "all services use these types" |
| `tsp` | (n/a) | DRIFT | **0 callers** — DEAD CODE candidate; supplanted by protocol/sub1/sub2/sub3 |
| `devops` | `assembly` | SUPPORT | Devops console at /devops; mounted on gateway |
| `party` | `assembly` | EXPERIMENT | Party-substrate identity; consumed by fox only; design from GRO-734 |

---

## 4. CORE — Working, Defended, Load-Bearing

These are the modules that constitute the actual platform-as-it-runs-today, plus the modules that Loop 2 verified end-to-end (even where deployment hasn't followed).

### 4.1 The shipped surface

**`cmd/gateway`** — `ship` stage, CORE.

The HTTP front door. Live on Cloud Run staging via `cloudbuild.gateway.yaml`. Imports 22 internal packages and registers 8 route trees (namespace, alert, MCP, dev console, LNURL auth, evidence/anchor read APIs, webhook ingestion, devops console). Carries the entire user-facing and webhook-facing surface area in one process. 378-line `main.go`.

This is the "everything is currently here" service. That's an architectural choice, not a problem. It will become a problem only when scaling pressure forces a decomposition; at current load it's fine.

**`cmd/identity`** — `ship` stage, CORE.

The auth substrate. Live on Cloud Run staging. Owns API key validation (`/v1/identity/keys` CRUD), session validation, and the platform JWT contract per `go-security.md`. Imports `internal/auth` and `internal/identity`. The most-depended-upon package in the repo (`internal/identity` has 38 importers).

Has the only `_test.go` file in any cmd/ directory (`cmd/identity/main_test.go`). Other cmd binaries inherit their test coverage from the internal packages they import; `identity` is the only one with a binary-level smoke test.

### 4.2 The Loop-2-verified pipeline (built but mostly not scheduled)

These six binaries (`item`, `pricing`, `inventory`, `chirp`, `fox`, `owl`) were the Loop 2 keystone — Tier-1+2 modules forced through a Go compiler against the SDD corpus. Plus `sub1-hash-seal` and `sub2-parse-route` which are the protocol pipeline's data-plane workers.

All eight have:
- Real `Mount(r chi.Router)` handlers or real worker loops
- Internal package code that exercises non-trivial schema (multi-table queries, transactions, UPSERT patterns)
- Unit and/or integration tests in the corresponding internal packages
- Documented Loop 2 build report evidence (`Brain/wiki/cards/loop2-build-report.md`) that the code matches its SDD

None of them have a Dockerfile or a compose entry. They all run as `go run` commands during development; in the current deployment topology they don't run anywhere. **Promoting any of them to actually-running is a deployment exercise, not a code exercise.**

The chain pipeline pair deserves separate attention:

**`cmd/sub1-hash-seal`** — `verify` stage, CORE — but with a P0 flag.

The Loop 2 evidence sealer. Consumes `protocol:events` from Valkey, computes per-merchant chain hash, INSERTs into `protocol.evidence`, ACKs. 78-line main; the `internal/protocol/sub1/seal.go` package (351 LOC, 2 test files) is where the work happens.

**P0 issue:** the chain hash formula in shipped code (`SHA-256(event_hash ‖ prev_chain_hash ‖ timestamp)`) does not match either of the two algorithms documented in the SDD library (see Headline Finding 7). Patent Application #63/991,596 covers "the" chain hash; whichever formula was filed is the one that needs to be in code. Until that's resolved, every event sealed today is sealed against an algorithm of unclear provenance.

**`cmd/sub2-parse-route`** — `verify` stage, CORE.

The multi-POS parser. 155-line main; registers Square + Counterpoint + Clover adapters into the substrate; the `internal/protocol/sub2` package (968 LOC, 2 test files) drains the events stream and writes parsed transactions to the schema-correct tables.

This is the binary that demonstrates the multi-POS thesis works. Three structurally different POS systems share one parser pipeline. No SDD work needed here; it's already correct against `pos-adapter-substrate.md` and `multi-pos-architecture-proof.md`.

### 4.3 The internal substrate

Several internal packages are CORE without having a corresponding cmd/ binary because they're consumed everywhere. The big ones:

- **`internal/identity`** — 38 importers. The auth substrate. If this changes shape, every binary recompiles.
- **`internal/db`** — 24 importers. The pgxpool wrapper.
- **`internal/config`** — 26 importers. Env-driven config loader.
- **`internal/protocol/publisher`** — 23 callers. The Valkey publish abstraction. 157 LOC for the entire fan-in.
- **`internal/db/types`** — 1788 LOC of schema-aligned types, generated (or hand-written) from `deploy/schema/*.sql`. Imported by 8 internal packages including all adapters and protocol/sub2.

All of these are load-bearing. None of them have meaningful test coverage at the package level (most are 0-1 test files), but they're tested transitively by every package that imports them.

---

## 5. SUPPORT — Required for CORE to Function

SUPPORT modules are the things CORE depends on but that don't independently deliver value. Removing them cascades into CORE failure; replacing them is feasible if the contract is preserved.

### 5.1 Operational SUPPORT

**`cmd/dbcheck`** — `verify`, SUPPORT.

Smoke probe. Reads `pg_extension`, runs `CREATE EXTENSION IF NOT EXISTS vector`. Has its own Dockerfile but isn't in compose. Used as a one-shot to verify a fresh database is provisioned correctly. Should stay; small, useful, no operational footprint.

**`cmd/transaction`** — `assembly`, SUPPORT.

The canonical write path for `transaction.transactions` and child tables (line items, tenders, discounts). Real Mount handler, no tests. Critical for the receiving and sales-audit downstream flows. Promote to `verify` by adding tests; don't park.

### 5.2 Substrate SUPPORT

These are internal packages that hold the platform's contracts:

- **`db/types`** — schema → Go type mapping. Untested but generated.
- **`protocol/secrets`** — per-source webhook signing key resolution. Critical to the HMAC validation chain. Has tests.
- **`protocol/audit`** — audit log middleware on every state-mutating route. Has tests.
- **`protocol/anchor`** + **`protocol/evidence`** — read-side APIs for the L1 evidence store and L2 anchor records. Mounted on gateway; both serve the public verify_chain interface.
- **`protocol/validate`** — L402 verification token store. 612 LOC, currently not exercised in the running gateway (no L402-gated tools served), but the contract is in place.
- **`mcp`** — wraps domain packages for the MCP tool surface. 916 LOC, mounted only on gateway. Has tests.
- **`web`** — server-rendered UI (Tailwind/Alpine.js). 5 test files. Mounted on gateway.
- **`webhook`** — per-(merchant,source) rate limiting backed by Valkey rolling window. 677 LOC, has tests.
- **`lp`** — read-only access to `detection.lp_substrate` and `detection.allow_list`. Mounted on gateway.

### 5.3 Schema SUPPORT

`deploy/migrations/` runs 019 → 027 (live). 001 → 018 are archived (folded into `deploy/schema/00–12_*.sql` baseline). A fresh database needs the baseline applied first, then the live migration sequence. There is no SDD documenting this dual-track schema bootstrap; an operator coming in cold would need to discover it from the README or by reading the Dockerfile. **Documentation gap, not a correctness gap.**

---

## 6. EXPERIMENT — Built But Nobody Calls It Yet

These modules are real Go code that compiles, has handlers, and in some cases has tests — but no consumer in the running platform depends on them. They could be parked behind a feature flag with no operational consequence.

### 6.1 The domain-CRUD scaffold

`cmd/analytics`, `cmd/alert`, `cmd/asset`, `cmd/customer`, `cmd/employee`, `cmd/hawk`, `cmd/report`, `cmd/returns` all follow the same pattern: a thin `cmd/<name>/main.go` (43–201 lines) that imports the corresponding `internal/<name>` package and Mounts its handler. The internal packages have non-trivial code (200–700 LOC each, sometimes more for `casemgmt` at 774 LOC). None have test files at the cmd/ layer; most have 1 test file in the internal/ package.

These exist because the SDD library expected each domain to be its own service on its own port. The current deployment runs all of them inside the gateway by importing the internal package directly. Whether they ever get promoted to standalone services is a deployment-topology decision.

For the audit: they're EXPERIMENT because no production deployment artifact uses them. The functionality is delivered by the same internal packages mounted into the gateway. That's not a bad thing — it's a perfectly defensible monolith-first deployment posture. But it does mean we're carrying ~25 cmd/main.go files that no one runs.

### 6.2 sub3-merkle-ordinal

`cmd/sub3-merkle-ordinal` is the one EXPERIMENT that hurts to keep on the shelf. The L2 anchor pipeline is the evidentiary rail's external-verifiability story. Until the worker is scheduled, the platform's "any auditor can verify" claim is intact for the chain hash but not for the Bitcoin anchor. The story is: events get sealed, chain hashes get computed, but no Merkle root is ever inscribed.

This is the highest-priority EXPERIMENT to graduate. Adding a compose entry plus an `ORDINALSBOT_API_KEY` configured for signet would move it from `assembly` to `ship`. The code is there; the operational decision isn't.

### 6.3 Edge / poller / replenishment / task / workflow

`cmd/edge` runs the Counterpoint REST poller (`internal/poller`). `internal/replenishment` is a Min/Max trigger that subscribes to a Valkey stream. `internal/task` is the directed-task queue. `internal/workflow` is investigation lifecycle definitions.

All four are real code that exercises real schema. None are scheduled to run. The supply-chain and field-operator flows they support are not in production.

### 6.4 LNURL-auth

`internal/auth/lnurl` (553 LOC, 2 test files) implements LNURL-auth login (GRO-753). Mounted on gateway. Tests pass. **Live in the gateway routes**, technically — but nobody is actually using LNURL to log into a Canary tenant today. Sits between SUPPORT and EXPERIMENT depending on whether you count "wired into the production binary" as enough.

### 6.5 Cockroach test package

`internal/protocol/cockroach` is a test-only package validating the "Cockroach Principle" (losing any single storage tier doesn't destroy evidence). It has `//go:build integration` build tag and runs only under integration test conditions. Useful as a regression guard, not load-bearing for the platform.

---

## 7. DRIFT — Spec Without Code, Code Without Spec

DRIFT is where the spec library and the build disagree. Two flavors: spec-without-code and code-without-spec. Both are real; the second is the more uncomfortable one because it means production runs on contracts no SDD describes.

### 7.1 Spec-without-code (the shelf)

41 SDDs have no implementing binary. The structurally important ones — services that the platform thesis explicitly relies on:

| SDD | Stated binary | Stated port | Actual state |
|---|---|---|---|
| `raas.md` | `cmd/raas` | :8099 | No code; functionality split between sub1 (chain) and namespace (eljeffe — different concept) |
| `l402-otb.md` | `cmd/l402-otb` | :9090 | No code; `internal/billing` does part of the satoshi rollup but no L402 wallet |
| `commercial.md` | `cmd/commercial` | :9089 | No code; vendor finance / chargeback / 3WM-payment-gating absent |
| `compliance.md` | `cmd/compliance` | :9091 | No code; item-eligibility × site-zone × operational-blocks absent |
| `field-capture.md` | `cmd/field-capture` | :9087 | No code; semantic field mapping absent (note: also a Brain card v2 about a different surface — naming collision) |
| `ildwac.md` | `cmd/ildwac` | :9082 | No code; cost rollup absent |
| `device-contracts.md` | `cmd/device-contracts` | :9083 | No code; device SLA enforcement absent |
| `ops-dashboard.md` | `cmd/ops-dashboard` | :9084 | No code; real-time device health surface absent |
| `store-brain.md` | `cmd/store-brain` | :9085 | No code; presence resolution + session governance absent |
| `store-network-integrity.md` | `cmd/store-network-integrity` | :9088 | No code; multi-store anomaly detection absent |
| `blockchain-anchor.md` | `cmd/blockchain-anchor` | :9086 | No code; sub3-merkle-ordinal partially fills this role but isn't deployed |
| `party-identity-design.md` | `cmd/party` | :8094 | No code; `internal/party` exists, consumed only by fox |
| `three-way-match.md` | (internal package, no binary) | n/a | Spec describes `internal/threeway`; that package doesn't exist; `cmd/receiving` is `/health` stub |
| `receiving.md` | `cmd/receiving` | :8092 | `cmd/receiving` is `/health` stub only |

That's 14 services on the SDD shelf. Each has a comprehensive specification — most are 200-600 lines of detailed contract — and zero implementing code. The cost of writing those specs was real; the cost of leaving them on the shelf is documentation drift (every passing month makes them slightly less accurate to the platform's current state) and decision fatigue (every architectural conversation gets pulled into "what about the OTB service").

### 7.2 Code-without-spec (the surprises)

Three internal packages are running in the gateway with no SDD describing them:

**`internal/protocol/namespace` (eljeffe)** — `assembly`, DRIFT.

The `.jeffe` namespace registry. Live in production gateway. Bitcoin ordinals integration. Three test files. **No SDD covers this.** The semantic confusion with `raas.md` (which describes a `raas:{merchant_id}` namespace, not `.jeffe` Bitcoin names) is a documentation problem this audit can't solve on its own.

**`internal/casemgmt`** — `assembly`, DRIFT.

774 LOC standalone case-management API. Owns `q.cases`, `q.case_actions`, `q.case_evidence` as a separate API surface from `internal/fox`. **No SDD uses the name `casemgmt` or describes a separate case-management API alongside fox.** The hawk SDD (`hawk-case-management.md`) describes "incident-typed case management where Fox had generic cases" — possibly this is what casemgmt is, but the SDD doesn't reference the package name and the implementation predates the hawk SDD.

**`internal/billing`** — `assembly`, DRIFT.

Bull L402-OTB satoshi cost rollup over `ledger.ildwac_positions`. 568 LOC. The `l402-otb.md` SDD describes a separate `cmd/l402-otb` service on :9090 with `otb_wallets`, `otb_transactions`, `otb_alerts` tables. None of those tables exist in the current schema. The `internal/billing` package reads from `ledger.ildwac_positions` instead. Different table set, different shape, no SDD covers what's actually built.

### 7.3 Pure dead code

`internal/arts`, `internal/crdm`, `internal/tsp` have zero callers via grep. All three should be removable. The `crdm` removal is the most interesting because the doc comment claims it's used everywhere — that comment is false; the actual canonical types live in `internal/db/types/`. Removing `crdm` is therefore also a documentation correction.

**Action:** delete in a single PR with `git rm -r internal/arts internal/crdm internal/tsp`. Watch CI. Should be uneventful.

### 7.4 Code with stale spec

A separate failure mode: the SDD exists and describes the right concept, but the implementation diverged. The chain-hash variants (Headline Finding 7) is the canonical example. The `protocol.evidence` table name (vs `evidence_records` in tsp-seal.md vs `raas_events` in raas.md) is another. The `cmd/identity` implementation matches `identity.md` reasonably well but the federation-broker section of identity.md is aspirational — the actual identity service does not implement OIDC/SAML/LDAP/SCIM yet.

These are not catastrophic but they erode SDD trustworthiness. A future engineer reading `tsp-seal.md` and looking at `internal/protocol/sub1/seal.go` should see them agree. They don't.

---

## 8. SDD Library — Per-Topic Status

The SDD corpus is a separate audit surface. Below is the topic-level state derived from Agent B's match-up table, with code/spec alignment called out:

| Topic | SDDs | Cards | Code | Status |
|---|---|---|---|---|
| RaaS | raas.md | canary-raas, raas-receipt-as-a-service | `protocol/sub1` (chain only); no namespace authority | **DRIFT** — spec describes service that doesn't exist |
| Three-Way Match | three-way-match.md | retail-three-way-match | `cmd/receiving` is /health stub; no `internal/threeway` package | **DRIFT** — spec-only |
| L402 / OTB | l402-otb.md | canary-l402-otb, infra-l402-otb-settlement, platform-l402-ildwac-moat | `internal/billing` partial (satoshi rollup, not L402 wallet) | **DRIFT** — code for one piece, spec for another |
| Field Capture | field-capture.md | canary-field-capture, platform-field-capture | none | **DRIFT** — naming collision: SDD covers semantic field-name mapping; v2 Brain card covers process-node operative event capture (different surface) |
| Multi-POS Adapter | multi-pos-architecture-proof, pos-adapter-substrate, driftpos-integration | canary-android-pos-integration | `internal/adapters/{square,counterpoint,clover}` LIVE | **CORE** — built and verified |
| TSP Pipeline | tsp, tsp-seal, tsp-parse, tsp-merkle, tsp-detect | (none directly) | sub1 + sub2 LIVE; sub3 builds-not-deployed; tsp-detect = chirp | **PARTIAL** — pipeline real, naming inconsistent |
| Identity | identity, party-identity-design, external-identities | canary-employee, canary-customer | `cmd/identity` LIVE; `internal/party` exists; external-identities folded into adapters | **PARTIAL** — partial, with federation aspirational |
| Inventory-as-a-Service | inventory-as-a-service | canary-inventory-as-a-service, canary-inventory, platform-inventory-2026-04 | `cmd/inventory` LIVE | **CORE** — built |
| ILDWAC / Cost Rollup | ildwac, satoshi-cost-rollup | canary-ildwac, infra-satoshi-cost-rollup | `internal/billing` reads `ledger.ildwac_positions`; `cmd/ildwac` absent | **DRIFT** — partial |
| Hawk | hawk-case-management | canary-hawk | `cmd/hawk` real handler, not deployed | **PARTIAL** |
| Owl | owl, analytics | (none) | `cmd/owl` LIVE | **CORE** |
| Chirp | chirp | (none) | `cmd/chirp` LIVE | **CORE** |
| Fox | fox | (none) | `cmd/fox` LIVE | **CORE** |
| Bull / NCR | bull | (none) | `cmd/bull` real but not deployed; `internal/billing` reads ledger | **PARTIAL** |
| Edge / POS Failover | (no SDD for failover) | platform-performance-nfrs (asserts the requirement) | `cmd/edge` polls Counterpoint, doesn't queue receipts | **DRIFT** — Brain card asserts requirement, no SDD, no implementing code |
| Receiving | receiving | canary-receiving, retail-receiving-disposition | /health stub | **DRIFT** — spec-only |
| Returns | returns | canary-returns | `cmd/returns` real handler, not deployed | **PARTIAL** |
| Pricing | pricing | canary-pricing | `cmd/pricing` LIVE | **CORE** |
| Item / Catalog | item | canary-item, canary-item-master-and-catalog | `cmd/item` LIVE | **CORE** |
| Customer | (no SDD) | canary-customer | `cmd/customer` real handler, not deployed | **DRIFT** (code-without-spec) |
| Asset | (no SDD) | canary-asset | `cmd/asset` real handler, not deployed | **DRIFT** (code-without-spec) |
| Employee | (no SDD) | canary-employee, canary-labor-shift-management | `cmd/employee` real handler, not deployed | **DRIFT** (code-without-spec) |
| Transfer | (no SDD) | canary-transfer | `cmd/transfer` /health stub | **DRIFT** — neither side built |
| Report | (no SDD) | canary-report | `cmd/report` real handler, not deployed | **DRIFT** (code-without-spec) |
| Alert | alert | (none) | `cmd/alert` real handler, not deployed | **PARTIAL** |
| Webhook Pipeline | webhook-pipeline | (none) | `internal/protocol/webhook` LIVE in gateway | **CORE** |
| Compliance / Evidentiary | compliance, blockchain-anchor | canary-compliance, canary-blockchain-anchor, canary-evidentiary-rail, infra-blockchain-evidence-anchor | none of the binaries; `protocol/anchor` is read-side only | **DRIFT** |
| Commercial | commercial | canary-commercial, canary-meter-model-token-plan | none | **DRIFT** |
| Device Contracts | device-contracts | canary-device-contracts | none | **DRIFT** |
| Settings | settings | (none) | none | **DRIFT** — spec-only |
| Ecom Channel | ecom-channel | canary-ecom-channel | none | **DRIFT** |
| Ops Dashboard | ops-dashboard | canary-ops-dashboard, canary-operations-hub | none | **DRIFT** |
| Cloud Architecture | cloud-architecture-workload | (none) | (deploy artifacts only) | **PARTIAL** — gateway + identity on Cloud Run |
| Agent Contracts / PMO | agent-contracts | (none) | none | **DRIFT** |
| MCP Service Junctions | mcp-service-junctions | (none) | `internal/mcp` (916 LOC, gateway-mounted) | **PARTIAL** — SDD describes ~171 junctions; ~30 implemented |
| Canonical Data Model | canonical-data-model + 3 companions | (none) | `deploy/schema/*.sql` + `internal/db/types/` | **CORE-ish** — schema is the implementation |
| Feed Tier Contract | feed-tier-contract | infra-feed-tier-contract, infra-cadence-ladder | none | **DRIFT** — spec-only |
| Microservice Layout | go-module-layout, microservice-architecture, go-* (5 library cards) | (none) | partially followed | **PARTIAL** — libraries partially exist |

### 7.5 DRAFT cards needing review

Six Brain cards are `status: draft` or `needs-review: true`. These are unsettled positions:

- `canary-os-thesis.md` — draft. Cross-cutting platform identity.
- `infra-dns-topology.md` — draft, needs-review:true. URL strategy across partner conversations.
- `infra-l402-otb-settlement.md` — draft. Settlement specifics.
- `platform-gateway-thesis.md` — draft, needs-review:true. Why gateway is the only HTTP front door.
- `platform-wyoming-ecosystem.md` — draft, needs-review:true. CBDI/Custodia/Frontier Coin layer thesis.
- `store-network-integrity.md` — draft, needs-review:true. VSM-as-security-sensor (different surface than the approved domain card).

None of these are blockers for the build today; they're strategic items that need founder attention when the cycle slows.

---

## 9. Cross-Cutting Findings (Beyond Per-Module)

Synthesizing the per-module entries surfaces patterns that don't live in any single row:

### 9.1 The deployment ladder is the binding constraint

Every per-module classification assumes that "running in the gateway as a mounted handler" counts as deployment. By that lenient definition, ~15 modules are deployed. By the stricter "has its own Dockerfile + compose entry + Cloud Build" definition, 2 are. Choosing which definition to use is itself an architectural decision.

For monolith-first deployment posture: the lenient definition is correct, and the audit's CORE/SUPPORT classifications stand.

For a microservices target: the strict definition is correct, and most CORE entries downgrade to "verified but not deployed" — which is closer to "ready to ship" than "shipping."

The audit doesn't pick one. The decision affects the next dispatches: monolith-first means most work is in adding test coverage and validating the gateway mounts; microservices means most work is adding Dockerfiles and compose entries.

### 9.2 The chain-hash divergence is the highest-leverage single fix

Resolving Headline Finding 7 — picking the patent-canonical chain hash and aligning the two SDDs and the shipped code to it — is one focused dispatch's worth of work. It removes the most consequential drift in the corpus. Until it's resolved, every conversation about RaaS, evidence, anchors, or the patent claim has to navigate the inconsistency.

**Recommended action:** Dispatch — pull patent #63/991,596 application text, confirm the filed algorithm, edit `tsp-seal.md` and `raas.md` to match, edit `internal/protocol/sub1/seal.go` to match if it differs, add a property test that asserts chain-hash determinism against a fixed test vector.

### 9.3 The eljeffe/RaaS conflation is documentation, not code

Earlier in the session the eljeffe vs RaaS distinction looked like a build problem. After the wiring trace it's a documentation problem. The `.jeffe` namespace is a real, deployed, tested product (`internal/protocol/namespace`); it just has no SDD. The RaaS-as-namespace-authority is a real, comprehensive SDD; it just has no code. The two are not duplicates — they solve different problems. They got semantically tangled because both used the word "namespace."

**Recommended action:**
1. Write `docs/sdds/go-handoff/jeffe-namespace.md` covering the shipped service (the `.jeffe` registry, Bitcoin ordinal anchoring, the chi-mounted handler). 1-2 pages.
2. Either build `cmd/raas` per `raas.md` (decision point — see 9.4) or rewrite `raas.md` to describe whatever embedded pattern the platform actually wants for merchant resolution and chain authority.

### 9.4 The RaaS-or-not decision is now the gating architectural question

The platform thesis treats RaaS as foundational: "a merchant with Square today and Counterpoint next year is one business; the namespace persists." Today, that function is partially served by:
- `internal/identity` (merchants table; per-tenant context injection)
- `internal/db/types` (canonical types)
- `internal/adapters/*` (per-POS credential storage)
- `internal/protocol/sub1/seal.go` (the chain, keyed by `merchant_id` directly without an intermediate namespace)

There is no `raas:{merchant_id}` token anywhere in the running code. The chain is keyed by `merchant_id` UUID directly. If a merchant migrates from Square to Counterpoint, the chain continuity story works — same merchant_id, same chain, different `source_code` on each event row. The RaaS namespace token is **not currently load-bearing.**

That suggests the SDD's RaaS service is over-specified for the platform's actual needs. Two paths:

- **(a) Keep it on the shelf.** The SDD describes a service that might be needed at scale, isn't needed now. Mark it aspirational in the frontmatter; defer.
- **(b) Build the minimal version.** A `cmd/raas` with `ensure_namespace`, `resolve_namespace`, `register_source`, `append_event` (4 tools, not 9) would make the chain authority explicit and centralize a function currently implicit in `internal/protocol/sub1`. ~1 week of work; resolves the "why doesn't `cmd/raas` exist?" question permanently.

The audit doesn't pick. It surfaces the choice.

### 9.5 SDD library is intentionally larger than the build, but the corpus has a hygiene problem

The 14-services-on-the-shelf situation (§7.1) is partly intentional: the SDD library was authored ahead of the build to give Loop sessions a target. That's a defensible posture. But several of those SDDs are detailed enough (with full table schemas, MCP tool surfaces, SLA tables) that a future engineer reading them might assume they're more current than they are.

**Recommended hygiene pass:**
1. Add a `code_status:` field to every SDD frontmatter (`built` / `partial` / `spec-only`).
2. Update each entry based on the audit table in §7.
3. For specs that are spec-only, add a one-line "implementation status" callout near the top so a reader doesn't get 200 lines into a comprehensive contract before realizing nothing implements it.

Low-cost, high-leverage. Can be done in a single dispatch.

### 9.6 Test coverage is the silent risk

The audit classifies modules into `verify` factory stage based partly on test presence. By that criterion, exactly 8 cmd/ binaries qualify (fox, owl, item, pricing, inventory, sub1, sub2, sub3 via their internal packages). The 1788 LOC of `internal/db/types/` has zero tests. Most internal packages have 1 test file.

Loop 2's evidence is that the modules it built were forced through a Go compiler against the SDD corpus and emerged with passing unit tests. That's enough to call them `verify`. It's not enough for `qa`. Promoting any of them to `qa` requires end-to-end validation against real schema and real data — which is a separate sprint, not a side effect of the build sprints.

**Recommended action:** before the next deployment promotion, add a thin integration test layer that validates the gateway's read APIs against a fresh database with seeded data. Not exhaustive — just the chain verify endpoint, the ops-dashboard read paths, the namespace registration round-trip. ~3 days of work; catches schema drift and route-mounting regressions before they hit staging.

---

## 10. Recommended Actions, Ranked by Leverage

These are not roadmap items. They're the actions that fall out of the audit findings, ordered by impact-per-effort.

### High leverage, low effort

1. **Delete `internal/arts`, `internal/crdm`, `internal/tsp`** — three dead packages. One PR. (Maybe 1 hour.)
2. **Add `code_status:` to SDD frontmatter** — bulk metadata update across 60 SDDs based on this audit's §7 table. (Maybe 4 hours.)
3. **Write `jeffe-namespace.md` SDD** — document the shipped `.jeffe` registry. Removes one DRIFT entry; eliminates the eljeffe/RaaS confusion permanently. (1 day.)
4. **Cancel GRO-685 with a pointer to this audit** — the spec exhaustion mission is superseded; the audit is the artifact.

### High leverage, moderate effort

5. **Resolve the chain-hash divergence** — pull patent #63/991,596, pick the canonical formula, align two SDDs and one Go file, add property test. (1-2 days.)
6. **Schedule sub3-merkle-ordinal in compose** — graduate the L2 anchor pipeline from EXPERIMENT to SHIP. Add Dockerfile, compose entry, ORDINALSBOT_API_KEY for signet. (1 day.)
7. **Decide RaaS-or-not** — strategic call (§9.4). One conversation; days of build work either way.
8. **Spec POS failover queue** — Brain NFR card asserts the requirement; no SDD covers it. Write `edge-pos-failover.md` describing the 24-hour SQLite buffer + replay protocol. (2 days for spec; build is later.)

### Strategic, larger effort

9. **Pick monolith-first vs microservices** — affects every per-module classification's "deployed" interpretation. Until decided, the deployment ladder ambiguity persists.
10. **Mark draft Brain cards** — the 6 cards in §7.5 need founder review or explicit deferral.
11. **Hygiene sweep on SDD library** — beyond #2, the broader question of which spec-only SDDs to retire vs keep aspirational vs build.

---

## 11. What This Audit Does Not Cover

For honesty, the explicit out-of-scope:

- **Cove, Angel, Canary (Python frozen), Seacove.** Separate apps with their own readiness questions. The factory pipeline applies; the audit doesn't.
- **The Brain wiki at large.** The audit covered cards matching CanaryGo-relevant prefixes (~99 cards). Other domain cards (Cove governance, real estate, etc.) are out of scope.
- **External vault projections** (CATz, Canary Retail Brain, NCR). These are publication surfaces, not platform components.
- **The Python prototype** (`Canary/`). Frozen at v0-python-prototype tag per CLAUDE.md. Not a CanaryGo concern.
- **Commercial / pricing / GTM positioning.** This audit is technical-readiness only.
- **Performance characterization.** No load tests, no actual latency measurements. The platform's NFR card asserts targets; whether the running code meets them at scale is unmeasured.
- **Security review.** No penetration test or threat model. The `data-classification-inventory.md` and `compliance.md` SDDs describe a target security posture; alignment between target and current state is not audited here.

---

## 12. Cross-References

- `docs/superpowers/plans/2026-04-29-m1-m2-m3-coverage-assessment.md` — the GRO-684 coverage assessment that informed this audit's scope.
- `Brain/wiki/cards/loop2-build-report.md` — Loop 2 evidence for the modules classified `verify` here.
- `Brain/wiki/cards/platform-thesis.md` (v3) — the thesis this audit's classification is measured against.
- `Brain/wiki/cards/platform-performance-nfrs.md` — the NFR card asserting POS failover, 5s field-capture invariant, 99.9% durability, 500K events/hour per merchant.
- `factory-manifest.json` — the canonical pipeline definition this audit's stage ladder is derived from.
- Linear: GRO-685 (this audit supersedes it); GRO-684 (parent coverage assessment); GRO-700 (GCP rebaseline); GRO-739/GRO-761 (Loop 2 mission).

---

*End of audit.*
