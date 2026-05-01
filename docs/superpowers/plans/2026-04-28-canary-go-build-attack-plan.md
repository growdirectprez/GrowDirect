# Canary Go Build Attack Plan
**GRO-668 · 2026-04-28 · Canary Go**

The Go build has a clear critical path: Docker → Foundation → Detection Core → first demo → Intelligence → Module spine → VAR delivery. Every other sequence is slower. The CATz engagement funnel determines what must be demo-able and when — a VAR (RapidPOS/Bart) needs to see webhook-to-alert working before they commit; an NCR Counterpoint merchant needs to see the Bull adapter running the same detection chain before they sign. This plan sequences to those two demo gates, not to a feature list. Everything that does not serve the nearest gate is deferred. Everything that serves it is urgent.

---

## Section 1: Linear State as of 2026-04-28

27 open epics across 6 milestones. One issue is currently active (Todo); the rest are Backlog. The table below is the authoritative dispatch queue — all priority assignments come from the original GRO filing.

| GRO | Title | Milestone | Priority |
|---|---|---|---|
| GRO-665 | Docker stack | M1 — Foundation | Urgent / **Todo** |
| GRO-638 | CRDM & Data Model | M1 — Foundation | Urgent |
| GRO-639 | Identity, Auth & Tenant Model | M1 — Foundation | Urgent |
| GRO-640 | Multi-POS Adapter Substrate | M1 — Foundation | Urgent |
| GRO-641 | Service Skeleton, Monorepo | M1 — Foundation | Urgent |
| GRO-642 | Webhook Pipeline & TSP | M2 — Detection Core | Urgent |
| GRO-643 | Chirp Detection Engine | M2 — Detection Core | Urgent |
| GRO-644 | Fox Case Management | M2 — Detection Core | Urgent |
| GRO-645 | Owl & pgvector | M3 — Intelligence Layer | High |
| GRO-646 | Analytics, Risk Scoring | M3 — Intelligence Layer | High |
| GRO-647 | Module T — Transaction Pipeline | M4 — Module Spine | Urgent |
| GRO-648 | Module C — Customer | M4 — Module Spine | High |
| GRO-649 | Module N — Device | M4 — Module Spine | High |
| GRO-650 | Module A — Asset Management | M4 — Module Spine | High |
| GRO-651 | Module Q — Loss Prevention | M4 — Module Spine | Urgent |
| GRO-652 | Module M — Merchandising | M4 — Module Spine | High |
| GRO-653 | Module D — Distribution | M4 — Module Spine | High |
| GRO-654 | Module F — Finance | M4 — Module Spine | High |
| GRO-655 | Module O — Orders | M4 — Module Spine | High |
| GRO-656 | Module S — Space, Range & Display | M4 — Module Spine | High |
| GRO-657 | Module P — Pricing & Promotion | M4 — Module Spine | High |
| GRO-658 | Module L — Labor | M4 — Module Spine | High |
| GRO-659 | Module E — Execution | M4 — Module Spine | High |
| GRO-660 | Bull — NCR Counterpoint Adapter | M5 — VAR Delivery | Urgent |
| GRO-661 | Edge Agent & Hub | M5 — VAR Delivery | Urgent |
| GRO-662 | RapidPOS Onboarding Flow | M5 — VAR Delivery | Urgent |
| GRO-663 | GCP Deployment | M6 — Hardening | High |
| GRO-664 | Ops Handoff Package | M6 — Hardening | High |

GRO-668 (this SDD corpus v1.1 pass) closes when this plan is committed and the SDD gaps in Section 4 are filed as child issues.

---

## Section 2: CATz Funnel — What Must Be Demo-able and When

CATz is a two-phase engagement model: Assess & Design (Phase I) then Select & Implement (Phase II). The channel model means Bart at RapidPOS is the distribution layer — he brings Counterpoint merchants; Canary must demo on their stack, not on a sanitized sandbox. This has direct implications for sequencing: multi-POS credibility is not a nice-to-have for Phase II, it is the unlock for Bart's VAR signature.

| Engagement phase | What the client or VAR needs to see | Modules required |
|---|---|---|
| Phase I entry — any retailer | Canary ingests their data and fires something real | Webhook / TSP, Chirp, one alert on screen |
| Phase I exit — sign vision + BC | Full detection coverage, evidence chain, human-readable case | Fox (case + evidence), Owl (recommendation) |
| Phase II — architecture review | Multi-POS works — same rules, different connector | Bull adapter, same Chirp ruleset fires |
| VAR contract — Bart signs | Counterpoint-native flow, VAR onboarding, ops handoff | RapidPOS Onboarding (GRO-662), Edge Agent (GRO-661), Ops Package (GRO-664) |

Two demo gates drive the build order. Everything else is subordinate to reaching them:

**Demo Gate 1 — Square end-to-end:** Square webhook → TSP seal/parse → CRDM record → Chirp alert → Fox case → Owl recommendation. This is the CATz Phase I exit demo. Requires M1 + M2 + M3 to be functional.

**Demo Gate 2 — Counterpoint parity:** NCR Counterpoint poll cycle → same TSP pipeline → same Chirp rules → same Fox/Owl output. This proves multi-POS to a skeptical VAR partner. Requires Bull (GRO-660) against a running M1+M2+M3 stack. This is Bart's gate before he signs.

Both gates must work on live infrastructure, not against mocked responses. That is what makes Docker the hard prerequisite — the stack underpins both.

---

## Section 3: Build Sequence — The Attack

### Phase 0 — Environment (~1 day)

**GRO-665: Docker stack.** `CanaryGo/devops/docker-compose.yml` with isolated databases (`canary_go`, `canary_go_test`), own Valkey DB, own pgvector extension. No shared state with the Python prototype — the clean break established at the v0-python-prototype tag is a design invariant, not a preference. Until this is up and verified (`curl http://127.0.0.1:8003/mcp` equivalent for Canary Go health), no other Go work starts. This is the only hard sequential dependency in the plan.

### Phase 1 — Foundation (~1–2 weeks, parallel after Docker)

All four M1 epics can run in parallel once Docker is up. They have no schema-level dependencies on each other — only on the runtime existing.

**GRO-638 — CRDM & Data Model:** Run all 82 table migrations. sqlc generates Go from SQL; the migrations are the schema authority. This is the bedrock — everything reads and writes through CRDM. Start here on day 1 of M1.

**GRO-639 — Identity, Auth & Tenant Model:** Tenant isolation, JWT issuance, role binding, geography/category hierarchy. Do not start this without `raas-go.md` — the Go RaaS SDD is a prerequisite (see Section 4). The Python RaaS design informed the model; the Go implementation spec needs its own document before a line is written.

**GRO-640 — Multi-POS Adapter Substrate:** Interface contract, rate limit/retry envelope, dead-letter queue, poll watermark, connection pooling. No POS implementation goes here — this is the interface only. Hawk (Square) and Bull (NCR Counterpoint) implement against this substrate. Getting the substrate right in M1 is what makes Demo Gate 2 achievable in M5 without rework.

**GRO-641 — Service Skeleton, Monorepo:** Chi routing pattern, shared middleware stack, go-redis wiring, module layout. This is the frame everything else bolts to. It can proceed in parallel with GRO-638 once the DB container is running.

### Phase 2 — Detection Core (~2 weeks, dependency-ordered)

Dependency order is strict inside this phase. Shortcuts will require rework.

**Step 1 — GRO-642: Webhook Pipeline & TSP.** Square webhook receiver, 4-stage TSP pipeline (receive → seal → parse → store). End state: a Square sandbox webhook arrives, passes through all four stages, and a sealed CRDM record exists in the database. This is the on-ramp for everything downstream.

**Step 2 — GRO-643: Chirp Detection Engine.** Detection rule evaluator, alert lifecycle state machine, alert persistence. End state: a CRDM record triggers a rule evaluation, an alert is written, and state transitions (new → open → resolved) work correctly. Chirp cannot start until GRO-642 produces records.

**Step 3 — GRO-644: Fox Case Management.** Case open/close, evidence chain append-only trigger, hash chain validation. End state: an alert auto-opens a Fox case, evidence attaches, and the hash chain is valid. Fox cannot start until GRO-643 produces alerts.

**Demo Gate 1 checkpoint** falls here. Fire a Square sandbox webhook. Trace it through TSP. Confirm a Chirp alert fires. Confirm a Fox case opens with a valid evidence hash. If this sequence does not work, nothing in M3, M4, or M5 matters — fix it before moving forward.

### Phase 3 — Intelligence Layer (~1 week, parallel)

Both GRO-645 and GRO-646 can run in parallel after Detection Core is solid.

**GRO-645 — Owl & pgvector:** Risk Dictionary seed, EJ Spine entity resolution, semantic alert clustering, pgvector index. Owl upgrades Demo Gate 1 from "alert fired" to "recommended action surfaced."

**GRO-646 — Analytics, Risk Scoring:** Baseline metrics, rollup jobs, TransactionFact scoring substrate, risk score persistence. This feeds both Owl and Module Q downstream.

After Phase 3, Demo Gate 1 reaches CATz Phase I exit quality: Square data → alert → evidence → Owl recommendation → risk score. That is a signable Phase I deliverable.

### Phase 4 — Module Spine (~4–6 weeks, dependency graph)

13 modules. The dependency graph is not optional — it reflects actual data flow. Violating it produces modules that cannot read their own inputs.

| Wave | Modules | Rationale |
|---|---|---|
| 1st | N (Device) | Feeds T; no upstream dependencies |
| 2nd | T (Transaction Pipeline) | Core revenue event; feeds Q, R, F, A |
| 3rd (parallel) | C (Customer), A (Asset Management) | Both read from T; independent of each other |
| 4th | Q (Loss Prevention) | Depends on T + A; primary LP product — the CATz sellable unit |
| 5th (parallel) | P (Pricing), S (Space / Range / Display) | Relatively independent; feed C and J |
| 6th (parallel) | C (Commercial), J (Forecast & Order) | Depend on S + P |
| 7th | D (Distribution) | Depends on C + J |
| 8th | F (Finance) | Depends on T + C + D + A; settlement layer |
| Last | L (Labor), W (Work Execution) | W dispatches to all modules; build last so the dispatch surface is stable |

N before T: device identity is a dimension on every transaction record. T before Q: loss prevention rules operate against transaction data. W last: a work execution module that dispatches to incomplete modules produces incorrect outputs. These are not stylistic preferences — they reflect schema foreign keys.

### Phase 5 — VAR Delivery (~2 weeks)

This is the commercial unlock milestone. M5 converts the technical build into a deployable VAR product.

**GRO-660 — Bull (NCR Counterpoint Adapter):** Polling model against the Counterpoint REST API. Implement to the pos-adapter-substrate interface established in GRO-640 — the interface contract is what makes this a two-week effort instead of a six-week one.

**GRO-661 — Edge Agent & Hub:** Store-level deployment artifact, hub aggregation, offline-resilient data buffer.

**GRO-662 — RapidPOS Onboarding Flow:** VAR-delivered onboarding, not self-serve. The flow reflects Bart's delivery model — he installs, configures, and hands off. Canary's UX here serves the VAR, not the merchant directly.

**Demo Gate 2 checkpoint** after GRO-660. Fire a Counterpoint poll cycle against a test store. Confirm the same Chirp rules evaluate. Confirm the same Fox/Owl output appears. This is the demo Bart needs to see before signing. Without this working on real Counterpoint data, the VAR agreement has no technical foundation.

### Phase 6 — Hardening (~2 weeks)

**GRO-663 — GCP Deployment:** Cloud Run or GKE, Cloud SQL, Memorystore, Terraform baseline. This is not a stretch goal — it is the production surface for the VAR delivery model.

**GRO-664 — Ops Handoff Package:** Runbooks, SLA baseline, monitoring config, incident response playbook. Bart's team takes ownership of store-level deployments; they need documentation that does not require a phone call to interpret.

---

## Section 4: SDD Gaps — What Needs to Be Written Before Certain Services Can Be Built

The v1.1 SDD corpus pass surfaced six gaps. Each blocks a specific phase. Filing these as child GRO issues before the relevant phase begins is not optional — starting GRO-639 without `raas-go.md` produces an identity service that diverges from the platform tenant model, which is rework.

| Missing SDD | Blocks | What to write |
|---|---|---|
| `agent-contracts.md` | All agent-driven workflows | Contract schema, four reference contracts, MCP tool pattern — close this as part of GRO-668 |
| `raas-go.md` | GRO-639 (Identity), GRO-642 (Webhook) | Go implementation spec: REST endpoints, DB migrations, MCP tools in Go — prerequisite before M1 Identity work starts |
| `goose-go.md` | Phase 4+ (any L402-gated endpoint) | Go L402 middleware spec — Lightning payment gate for metered endpoint fees |
| `ildwac-go.md` | Phase 4 (Module F / cost model) | Formal design for ILDWAC ledger schema, RIB batch processor, WAC recalculation engine |
| `eljeffe-anchor-go.md` | Phase 5+ (evidentiary rail) | Go implementation of elJeffe Bitcoin inscription anchor for Fox evidence chain hash |
| `agent-topology.md` | All agent-driven sessions | Full topology with MCP tool catalog per agent, memory substrate, session instantiation scripts |

Recommend filing one GRO child issue per gap, tagged against the milestone they block. The only one that must close before any M1 build work starts is `raas-go.md`. `agent-contracts.md` closes as part of GRO-668.

---

## Section 5: Next Three Dispatches

Given this plan, the next three dispatches in execution priority:

**1. GRO-665 — Docker stack (already filed, pick it up now).** Mini-resident, Target/mini label. Nothing else ships until the Go stack is up. The entire critical path starts here.

**2. `raas-go.md` SDD — file before M1 Identity begins.** Author the Go RaaS SDD as a church-session deliverable on the laptop. File a Dispatch issue (Target/laptop, Agent/ALX) before the mini picks up GRO-639. This is the only blocking dependency between the two machines.

**3. M1 Foundation — four parallel child issues under GRO-638/639/640/641.** Once Docker is verified up, file four child dispatch issues (one per service, Target/mini, Agent/ALXjr) and start all four in parallel. The sub-issue model keeps Linear's sprint board clean while preserving the ability to track each service independently.

Everything after M1 follows the phase order above. Adjust only if a demo gate reveals a blocking gap — the plan is stable enough to commit to as written.
