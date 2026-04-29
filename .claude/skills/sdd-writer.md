---
name: sdd-writer
roles-primary: [Architect]
roles-assist: [Engineer]
stage: design
description: |
  Write a go-handoff SDD using the 4-hat methodology. Use when designing a new
  Canary Go service or module. Produces a handoff-ready spec in
  docs/sdds/go-handoff/ with Business, Technical, Ops, and Compliance sections.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# SDD Writer — Canary Go 4-Hat Methodology

The go-handoff SDD is the contract between Architect and Engineer. A well-written
SDD means no verbal translation layer, no ambiguous handoffs, no "what did you mean
by this?" It is the source of truth from design to test to deploy.

**Announce at start:** "I'm using sdd-writer to write this spec."

---

## When to Use This Skill

Any time a new Canary Go service or module needs a design spec. Invoked by the
Architect role. The SDD must exist before any code is written — not after, not
during. Engineering picks up where the SDD ends.

---

## Pre-Flight (Required Before Writing)

Before drafting a single line:

```
1. memory_recall("<domain topic>")          — surface existing wiki cards and prior SDDs
2. memory_recall("canary go module layout") — confirm port assignments and module spine
3. Read one existing SDD from docs/sdds/go-handoff/ to calibrate format
4. Read docs/sdds/go-handoff/go-module-layout.md — claim the next available port
```

If a related SDD exists (e.g., writing a new channel module when ecom-channel.md
exists), read it. Cross-references must be bidirectional when the spec is filed.

---

## Frontmatter Template

Every SDD starts with this block. Fill every field before writing content.

```yaml
---
spec-version: 1.0
target-implementation: Go
stack: PostgreSQL 17 + pgx + sqlc | Chi HTTP | REST | go-redis | pgvector-go
status: draft
binary: <cmd-name>
port: <port>
mcp-server: canary-<name>
license: Apache-2.0
copyright: "Copyright (c) 2026 GrowDirect LLC"
updated: <YYYY-MM-DD>
---
```

Change `status` from `draft` to `handoff-ready` only when all quality gates pass.

---

## Port Registry

Current assignments — update `go-module-layout.md` when claiming a port:

| Port | Service |
|------|---------|
| 8093 | store-brain |
| 8094 | ops-dashboard |
| 8095 | device-contracts |
| 8096 | ildwac |
| 8097 | inventory-as-a-service |
| 8098 | ecom-channel |
| 8099 | raas |
| 8092 and below | next available |

Claim a port before writing the spec. Two services cannot share a port — check
`go-module-layout.md` to confirm availability.

---

## The 4-Hat Structure

Required sections, in this order. Do not reorder. Do not omit.

---

### Hat 1 — Business

**Governing thesis in paragraph 1.** Not a definition. Not a list. A thesis —
one or two sentences that state what problem this service solves commercially and
what breaks without it. This paragraph is what an investor or a skeptical CIO
reads. Make it land.

Then:

- **Business rules** — numbered list. These are invariants the Engineer must
  honor. Each rule should be falsifiable: if a rule can't be violated, it's not
  a rule, it's an implementation detail.
- **Lifecycle or flow diagram** — Mermaid sequence or state diagram. Every service
  with a multi-step flow gets one. No exceptions.
- **Commercial context** — what does this unlock for the ICP? Where does it fit in
  the CATz method?

---

### Hat 2 — Technical

The Engineer's working document. Must be complete enough to implement without
verbal translation.

- **Service boundaries** — what tables this service owns exclusively. If a table
  is shared, name the owning service and document the access contract.
- **Data model** — full DDL with indexes. Not pseudocode. Actual CREATE TABLE
  statements. Every table gets a primary key, `created_at`, `updated_at`.
  UUID primary keys only (`gen_random_uuid()`).
- **API contract** — endpoint table: method, path, auth, request shape,
  response shape, status codes. Include error response schema.
- **MCP tool surface** — table format:

  | Tool | Input | Output | SLA | Notes |
  |------|-------|--------|-----|-------|

- **Go implementation notes** — package layout, key interfaces, sqlc query files,
  middleware chain. Enough to orient a Go engineer who hasn't read the prior art.

---

### Hat 3 — Ops

Production posture. The service doesn't ship without this section complete.

- **SLA table:**

  | Metric | P50 | P99 | Hard limit | Breach action |
  |--------|-----|-----|-----------|---------------|

- **Health endpoints** — `GET /healthz` (shallow: process alive) and
  `GET /readyz` (deep: DB + Valkey reachable). These are always separate.
  Never combine them. Never return 200 from readyz when dependencies are down.
- **Failure modes table:**

  | Failure | Detection | Recovery | Blast radius |
  |---------|-----------|----------|--------------|

- **Valkey key space** — key pattern, TTL, eviction policy, owner service.
- **Monitoring alerts** — what fires, at what threshold, who owns it.
- **Graceful shutdown** — signal handling (SIGTERM), drain timeout, in-flight
  request behavior.

---

### Hat 4 — Compliance

Closes the loop on data handling and IP posture.

- **PII classification table:**

  | Field | Classification | Retention | Notes |
  |-------|---------------|-----------|-------|

- **Append-only invariants** — if the service uses immutable records (tLog, gLog,
  anchored hashes), state the invariant explicitly. Include the REVOKE statement
  that enforces it at the DB layer if applicable.
- **Retention schedule** — per data class, what's kept, for how long, how purged.
- **Patent scope note** — required if the service implements any of:
  - Hash-chain anchoring or blockchain commit
  - WAC (Weighted Average Cost) computation with provenance weighting
  - IL(Device/MCP/Port/)WAC cost model
  - Bitcoin ordinal or L402 gating
  
  Note the scope, the priority date, and what aspects are novel. Do not skip this
  for services that touch these algorithms — the IP record depends on it.

---

## Quality Gates

Check every item before changing `status` to `handoff-ready`:

- [ ] Every table in the data model has at least one index beyond the primary key
- [ ] `healthz` and `readyz` are separate endpoints — never combined
- [ ] Any blockchain, L402, or Bitcoin anchor feature defaults to `false` — no service
      blocks store operations on external infra being unavailable
- [ ] Cross-references to related SDDs are bidirectional (if this SDD references
      `raas.md`, `raas.md` should reference this SDD — flag for update if not)
- [ ] License frontmatter present: `license: Apache-2.0` and
      `copyright: "Copyright (c) 2026 GrowDirect LLC"`
- [ ] Patent note in Compliance if the service uses hash-chain, WAC computation,
      or cost-model algorithms
- [ ] Port claimed in `go-module-layout.md`
- [ ] Governing thesis in first paragraph of Business section — not a definition

---

## Voice and Polish Standards

Every SDD ships at Big 4 delivery standard. These are not aspirational notes —
they are gate criteria.

- **Governing thesis in first paragraph of Business.** The reader should understand
  the commercial stakes before they read a single technical detail.
- **Confident and direct.** Opinions where warranted. If a design choice has a
  rationale, state it — don't just describe what it is.
- **Tables for structure-heavy content.** Data models, SLA commitments, failure
  modes, MCP tools, PII classifications — all tabular. Prose for narrative;
  tables for facts.
- **No prose walls without a governing idea.** Every paragraph has a point. If
  you can remove it without losing meaning, remove it.
- **Dry, not cute.** Humor is a rounding error. Clarity is the job.

The test: could a Go engineer at a Big 4 SI pick this up cold and implement it
without a kickoff call? If yes, it's done. If no, it's not.

---

## File Location

All SDDs land at `docs/sdds/go-handoff/<service-name>.md`. Filename is the
service binary name, kebab-case. Update `docs/sdds/go-handoff/INDEX.md` when
filing a new SDD.

---

*SDD Writer v1.0 — Canary Go 4-Hat Methodology*
