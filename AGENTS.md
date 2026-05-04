# AGENTS.md — GrowDirect Platform

Canonical context file for any coding agent (Claude Code, Codex, Gemini CLI) working in this repo.
Read this before touching anything. It tells you what you're building, where to find context, and how to work.

---

## What This Is

**Canary** is a store operations platform for SMB retailers on NCR Counterpoint / RapidPOS.
It sits above the POS — not against it. Merchants use POS AND Canary.

Three accountability rails govern everything:
- **Operational** — no unknown inventory loss; directed task queue; real-time SOH
- **Financial** — satoshi-denominated cost-to-serve; L402-gated open-to-buy
- **Evidentiary** — every event hashed, batched, anchored on Bitcoin L2

Primary channel: Bart's VAR operation (DriftPOS / whitelabel RapidPOS on NCR Counterpoint Android).
ICP: private retail, up to ~$50M revenue, owner-operator wearing every hat.

Active build: **CanaryGo/** — Go 1.25, GCP, ARTS-native, 29 services.
Python prototype (`Canary/`) is frozen at `v0-python-prototype`. Do not extend it.

---

## Step 0 — Get Context Before Coding

**Call memory_recall before reading files.** The memory bus has 385+ documents embedded.
It surfaces the exact card or SDD chunk you need in one call, cited and scored.

```
memory_recall("velocity model decay weighting min max")
memory_recall("PO status machine order control modes COLT NOLT")
memory_recall("evidentiary rail 4-tier storage Bitcoin L2")
memory_recall("NCR Counterpoint REST endpoint polling bridge")
memory_recall("task queue directed work replenishment trigger")
domain_context(domain="canary", topic="purchase orders", token_budget=4000)
context_assemble(topic="canary retail spine")
```

Memory bus MCP: `http://127.0.0.1:8003/mcp` — requires Docker stack up.
If it's unreachable, start the stack before proceeding: `cd ~/GrowDirect/devops && docker compose up -d`

---

## Tool Stack

### Obsidian — Brain/
The knowledge vault. Every design decision, capability spec, and domain model lives here.

**Read Brain content:** `mcp__obsidian__read_note_tool`, `mcp__obsidian__search_notes_tool`
**Write Brain content:** `mcp__obsidian__update_note_tool`, `mcp__obsidian__append_to_note_fs_tool`
**Never:** use `Read`/`Edit` tools on Brain/ markdown — use Obsidian MCP

Key entry points:
- `Brain/projects/Canary.md` — full MOC with all wiki links
- `Brain/wiki/cards/store-ops-capability-model.md` — 7-layer capability synthesis, build priority
- `Brain/wiki/cards/canary-android-pos-integration.md` — NCR Counterpoint event schemas
- `Brain/wiki/canary-go-portal.md` — project portal, SDD index, Linear links
- `Brain/wiki/cards/` — 18 store ops capability spec cards (committed 2026-05-04)

Card format: frontmatter (`type`, `status`, `tags`, `created`, `last-compiled`, `needs-review`) + structured content.
Run `python3 content-engine/engine.py lint --all` before committing Brain/ changes.

### Linear — Dispatch Project
The control plane. Operational instructions are Linear issues, not chat messages.

**Pick up work:**
```
list_issues({project: "Dispatch", labels: ["laptop"], status: "Todo"})
```

**Lifecycle:** Todo → In Progress (comment: picked up + ETA) → Done (comment: artifact paths + commit SHA)

Labels: `Target/laptop`, `Target/mini`, `Target/any` | `Agent/ALX` | Priority: Urgent/High/Normal/Low
GRO-prefixed issues are product/engineering tickets (not dispatches).

**Never put** strategy, client names, or internal positioning in Linear descriptions — keep issue titles imperative and brief.

### Claude — Primary Agent
Claude Code CLI is the primary development agent. Model: `claude-sonnet-4-6`.

Session modes — **never mixed**:
- **Church (laptop):** Brain/wiki cards, design docs, specs. Never touches CanaryGo/ code.
- **State (dispatch-driven):** Code execution only. Opens by listing open Linear dispatches. Commits on completion.

If you're in state mode and architectural questions arise — capture as a church note, redirect.

Memory files: `/Users/gclyle/.claude/projects/-Users-gclyle-GrowDirect/memory/`
MEMORY.md is the index. Write new memories when you learn non-obvious things.

### GCP — Deployment Target
Canary runs on GCP end-to-end. No hand-rolling outside core retail-domain IP.

- **Cloud Run** — each `cmd/<service>/` binary deploys as a Cloud Run service
- **Cloud SQL (PostgreSQL 17)** — primary DB: `canary_gcp`
- **Cloudflare R2** — S2 warm storage tier
- **Cloud Storage** — S3 cold archive (merchant-key encrypted)
- **Bitcoin L2 (OpenTimestamps)** — S4 chain anchor

Deploy config: `CanaryGo/deploy/`
Do not target AWS or Azure. GCP is locked per `project_gcp_commitment_locked.md`.

---

## Codebase Map — CanaryGo/

Module: `github.com/growdirect-llc/rapidpos`
Single `go.mod` at `CanaryGo/` root. All imports use this module path.

### Service Ports

| Service | Port | Domain |
|---|---|---|
| gateway | 443/8443 | API gateway, routing |
| identity | 8086 | Auth, JWT, tenant |
| tsp | 8080 | Transaction pipeline |
| chirp | 8081 | Detection rules |
| hawk | 8082 | Watch list, alerts |
| fox | 8083 | Case management |
| owl | 8084 | AI analytics |
| bull | 8085 | Task queue, directed work |
| alert | 8087 | Notification routing |
| analytics | 8088 | KPI dashboard |
| asset | 8089 | Asset management |
| item | 8090 | Item master, catalog |
| customer | 8091 | Customer records |
| employee | 8092 | Associates, shifts |
| returns | 8093 | Returns processing |
| report | 8094 | Reporting |
| receiving | — | Inbound, ASN, putaway |
| inventory | — | SOH, cycle count |
| pricing | — | Price management |
| transfer | — | Inter-store transfers |
| edge | — | MAP agent, LAN heartbeat |

### Internal Packages

```
internal/
├── adapters/     POS adapter substrate — CounterpointBasicAuthFlow, CanonicalEvent
├── alert/        Alert lifecycle
├── analytics/    KPI, velocity metrics
├── arts/         ARTS standard constants
├── asset/        Asset management
├── auth/         JWT, session auth
├── billing/      Satoshi cost model, L402
├── casemgmt/     Case lifecycle (Fox)
├── chirp/        37 detection rules, 3 tiers
├── config/       Env-based config
├── crdm/         Canonical Retail Data Model
├── customer/     AR_CUST → external identities
├── db/           pgx pool, sqlc generated queries
├── devops/       Health checks, feature flags
├── employee/     Associate profiles, shift model
├── fox/          Evidence hash chain, case management
├── identity/     Tenant isolation, RBAC
├── inventory/    SOH, cycle count, adjustments
├── item/         Item master, 3-level hierarchy
├── mcp/          MCP junction layer, hash-on-arrival
├── obs/          Observability (traces, metrics)
├── owl/          AI analysis, Ollama
├── pagination/   Cursor pagination
├── party/        Entity resolution
├── pricing/      Price, promotion
├── protocol/     Bitcoin L2, OpenTimestamps
├── report/       Report generation
├── returns/      Returns, RMA
├── tenant/       Middleware, per-store isolation
├── transaction/  PS_DOC pipeline, Sub2 dispatch
├── tsp/          4 stream consumers
├── web/          HTTP helpers, middleware
├── webhook/      Backpressure, idempotency, DLQ
└── workflow/     Temporal durable workflows
```

### Stack Rules

| Rule | Detail |
|---|---|
| pgx version | pgx/v5 only — never v4 |
| SQL queries | sqlc for complex writes; inline pgx acceptable for reads and simple writes |
| sqlc input | `internal/db/sqlc/<service>.sql` |
| sqlc output | `internal/db/query/<service>/` — do not hand-edit |
| Generate | `make sqlc-gen` |
| Database | `canary_gcp` (prod) / `canary_gcp_test` (test) — never `canary` or `canary_test` |
| Valkey | DB 2 — never DB 0 (Python Canary) or DB 1 (Cove) |
| Router | Chi v5 |
| Migrations | golang-migrate v4 |
| No imports from | `Canary/` — frozen Python prototype |

---

## Event Architecture

Every POS event flows through the MCP junction layer:

```
POS (NCR Counterpoint REST, polled 60s)
  → POS Bridge (per-store Go service)
  → Event Bus (MCP junctions — hash on arrival)
  → SOH Service + Replenishment Engine + Evidentiary Log
```

Hash-on-arrival is non-negotiable. Every event gets SHA-256 at ingestion.
Daily Merkle batch → S3 (merchant-key encrypted) → OpenTimestamps anchor → Bitcoin block.

Satoshi toll at each junction = billing record = evidentiary proof. Same act, unified model.

---

## Key Capability Specs (cards in memory bus)

Before implementing any of these domains, recall the card:

| Domain | Card | memory_recall query |
|---|---|---|
| Item master | `canary-item-master-and-catalog` | "3-level hierarchy scan-to-lookup dimension types" |
| Replenishment | `canary-demand-sensing-smb` | "velocity model decay weighting auto min max" |
| Task queue | `canary-mobile-task-ux-flows` | "directed task replenishment receiving cycle count" |
| PO lifecycle | `canary-purchase-order-lifecycle` | "PO status machine COLT NOLT order control" |
| Space/range | `canary-space-range-display-on-floor` | "planogram range status display min max facing" |
| Operations hub | `canary-operations-hub` | "morning briefing exception queue watch list" |
| POS integration | `canary-android-pos-integration` | "NCR Counterpoint REST poll bridge event schema" |
| Labor/shifts | `canary-labor-shift-management` | "shift model task assignment time standards productivity" |
| Evidentiary rail | `canary-evidentiary-rail` | "4-tier storage Bitcoin L2 anchor satoshi proof" |
| Multi-store | `canary-multi-store-intelligence` | "portfolio hub transfer order cross-store" |
| Supplier ordering | `canary-supplier-profile-and-ordering` | "supplier wizard COLT NOLT scorecard lead time" |
| Store ops model | `store-ops-capability-model` | "7-layer capability Android POS integration build priority" |

---

## Anti-Patterns — What Kills Sessions

- **Coding without memory recall** — you'll reimplement what's already spec'd
- **Touching Canary/ (Python)** — frozen; do not extend
- **Using pgx/v4** — breaking import; always v5
- **Writing to Brain/ with Read/Edit tools** — use Obsidian MCP
- **Creating dispatches in chat** — dispatches are Linear issues, not messages
- **Free-form exploration in state mode** — church only; state is dispatch-driven
- **Volatile data in wiki** — row counts and live stats belong in the DB
- **Hand-rolling anything not core retail IP** — buy the package
- **Committing without `engine.py lint --all`** — pre-commit hook will block it
- **Adding packages without flagging** — always tell the founder, get approval, commit, rebuild image

---

## Commit Protocol

1. `python3 content-engine/engine.py lint --all` — must be clean
2. Stage specific files — never `git add -A`
3. Commit message: imperative, present tense, scoped (`feat(item):`, `docs(brain):`, `fix(tsp):`)
4. Post-commit hook auto-seeds memory bus on Brain/ changes

---

## First 5 Minutes in This Repo

```bash
# 1. Confirm Docker stack
curl -s http://127.0.0.1:8003/mcp | head -1   # memory bus reachable?

# 2. Load domain context
memory_recall("platform thesis accountability rails meter model")
memory_recall("canary retail spine module layout")

# 3. Read the project MOC
# Brain/projects/Canary.md

# 4. Read CanaryGo/CLAUDE.md for service-level rules

# 5. Pick up your dispatch from Linear
# list_issues({project: "Dispatch", labels: ["laptop"], status: "Todo"})
```

---

*Last updated: 2026-05-04 — Tools: Obsidian · Linear · Claude Code · GCP*
