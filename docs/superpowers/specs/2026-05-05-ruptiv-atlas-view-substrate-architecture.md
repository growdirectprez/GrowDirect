---
title: Ruptiv Atlas View — Substrate Architecture
version: 0.1
date: 2026-05-05
status: draft
audience: Ruptiv technical and founding team
authors: ALX / GrowDirect
---

# Atlas View — The Technical Foundation That Makes Every Promise Keepable

Ruptiv makes three promises that are, underneath the positioning, technical claims. Listening Systems that keep running after the engagement ends. A Patterns library that compounds with every engagement. An invoice model that triggers when the cost line moves. None of these can be kept with a consulting methodology alone. Each requires specific infrastructure. Atlas View is that infrastructure.

This document describes what Atlas View is at the architectural level — its internal layers, how the four Sparring Partners depend on it, how compounding actually works as a mechanism, and what GrowDirect's current R&D delivers toward it.

---

## The Three Technical Claims

| Ruptiv Promise | Technical Requirement | Fails Without |
|---|---|---|
| Listening Systems keep running | Wire substrate stays live post-handoff. Monitor agent reads the running network continuously. Drift surfaces against the baseline fragment. | Bidirectional connectors, baseline as-is fragments, Monitor agent access to both |
| Every engagement compounds the Patterns library | Findings synthesized into Patterns-scoped schema-fragments. Cross-engagement indexing with strict engagement isolation — knowledge accumulates in Patterns without leaking scope. | Fragment substrate, cross-engagement Patterns index, synthesizer imprints |
| Invoice when the cost line moves | As-is baseline captured at Diagnostic. To-be state captured at handoff. The diff between them, with full audit trail, is the invoice evidence. | Append-only fragment store, as-is/to-be diff, immutable audit log |

---

## Atlas View Internal Architecture

Atlas View is the canvas. What makes it a canvas rather than a document is that it is queryable, evolvable, and bidirectional. Three substrate layers compose it.

```
┌─────────────────────────────────────────────────────────────┐
│  ATLAS VIEW                                                 │
│                                                             │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────┐  │
│  │  Index          │  │  Fragment        │  │  Wire     │  │
│  │  Substrate      │  │  Substrate       │  │  Substrate│  │
│  │                 │  │                  │  │           │  │
│  │  recall layer   │  │  organize layer  │  │  act layer│  │
│  │                 │  │                  │  │           │  │
│  │  vector bus     │  │  per-facet       │  │  bidirect-│  │
│  │  scoped by      │  │  structured      │  │  ional    │  │
│  │  engagement     │  │  records         │  │  connectors│  │
│  │                 │  │  append-only     │  │           │  │
│  └─────────────────┘  └──────────────────┘  └───────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### The Differentiation Hierarchy

Stem cells don't decide what to become. The body tells them where to go, the local tissue environment shapes what they can become, and the differentiation signal tells them exactly what to do. Authority flows in one direction. Escalations flow back up. The substrate enforces this at every boundary — it does not trust the layer above it.

```
Engagement Authority   — the body: terminal authority, scope approvals, handoff signing
          │
  Signal Pathway       — dispatches differentiation signals (imprints), observes runs
          │
  The Niche            — local tissue environment: orchestrates differentiation,
          │               enforces authority.read / authority.write per imprint
          │
  Sparring Partners    — undifferentiated agents that specialize on demand
          │               (Reveal, Socratic, Pattern, Monitor + per-engagement builds)
          │
  Cellular Machinery   — MCP tools: scoped operations per imprint authority.tools
```

Every artifact carries a `producer` envelope field identifying which layer produced it. The substrate validates this on write — an artifact claiming Engagement Authority origin that arrives from the Niche is rejected. The audit log captures the rejection. The body cannot be impersonated by a cell.

### Index Substrate (Recall Layer)

The vector bus. Every artifact produced by every Sparring Partner is indexed here — scoped strictly to its engagement. Agents query for context before they act. The quality of what they produce is a direct function of what they can recall.

**What it holds:** Charter, findings, schema-fragments, transcripts, captures, syntheses, decisions — all typed, all enveloped, all validated on write.

**The cell wall:** Every query is pre-filtered by `engagement_id` and the agent's `authority.read` array from its imprint header. `authority.read` declares the artifact types the agent is permitted to query — e.g., `["finding", "schema-fragment", "charter"]`. An agent cannot recall artifact types outside its declared read authority, and cannot reach artifacts from a foreign `engagement_id`. This is not a permission model — it is a structural constraint enforced by the Niche before the query reaches the index. Cross-engagement leakage is architecturally impossible, not policy-blocked.

**Hybrid recall:** Dense semantic search (embedding model) combined with sparse keyword matching, fused via Reciprocal Rank Fusion, reranked before return. This combination outperforms pure dense search on diagnostic artifacts — especially structured data like KPI baselines, process maps, and org charts where terminology matters as much as semantics.

### Fragment Substrate (Organize Layer)

The per-facet structured record. When a synthesizer imprint runs, it reads findings from the vector bus and writes a schema-fragment — one per facet (customer-base, system-map, kpi-extraction, process-mapper output, etc.). These are the cells that express their phenotype. This is what the client keeps.

**Append-only:** No fragment is ever updated. A new version supersedes the prior via a chain reference. The current view is always the latest non-superseded fragment per facet. The historical chain is the audit record.

**The invoice basis:** The as-is baseline is the set of schema-fragments written during the Diagnostic Engagement. The to-be design is the set written during the Disruption Engagement. The diff between them, timestamped and signed, is what moves the invoice.

**Handoff gate:** Engagement Authority signs the handoff. Signing requires all required facets populated and zero open halt-severity escalation triggers outstanding. The gate is enforced by the substrate — it computes facet coverage from the fragment store and open halt-severity items from the open question registry, and refuses to produce the signed handoff artifact until both conditions are satisfied. A signed handoff package is a provable claim, not a consulting deliverable.

### Wire Substrate (Act Layer)

The connectors. The same MCP-based tooling that captured the as-is state is kept live after handoff. This is what makes "Listening Systems keep running" true. Monitor reads the operating network through the same wires Reveal used to map it. Drift is detected against the baseline fragments still in the Index Substrate.

**Connector model:** Each connector is an MCP server scoped to a specific source system (HR, ERP, CRM, ticketing, etc.). Connectors operate in two modes. Read-only during Diagnostic — capture connectors index source system data into the bus; they do not write back. Bidirectional during Disruption and Operating — the to-be fragment diff is the change package pushed through the same connectors. Bidirectional write requires explicit authorization in the engagement charter and a corresponding `authority.write` grant in the agent imprint header.

**Credential scoping:** Connector credentials are stored per-engagement and rotated at handoff. The connector inventory — system, credential reference, rotation plan, access mode — is a required item in the signed handoff package. A client cannot be left with a running Monitor if the connector credentials expire on day 31.

The change package the client executes is the diff between as-is and to-be fragments pushed back through the same connectors. No new integrations. No re-mapping. The wires are already there.

---

## The Agent Stem Cell Protocol

Sparring Partners are not pre-built for specific engagements. They are generic agents that specialize on demand via imprints — the same mechanism as biological cell differentiation.

```
Generic Propagation Agent  ←── immutable binary
        +
Imprint Dispatch           ←── differentiation signal
        ↓
Specialized Agent          ←── e.g., "Reveal / customer-base / engagement-X"
        ↓
Operates against Atlas View ←── cytoplasm: scoped vector bus
        ↓
Emits typed finding         ←── output proteins: validated, enveloped
        ↓
Synthesizer runs            ←── cell division: findings → schema-fragment
        ↓
Fragment re-seeds Index     ←── next agent draws from richer context
```

**The imprint is the punch card.** The agent is the reader. Swap the imprint, get a different specialized computation from the same runtime. The sophistication is in the imprint design — the declared inputs, tool catalog, and output schema. The agents are commodity.

**Honest-Voice is structural, not instructional.** A Sparring Partner that sounds agreeable has either been given an imprint that permits sycophancy, or has recalled context that validates the assumption rather than stress-testing it. The cell wall and the imprint header enforce Honest-Voice at the architecture level. An agent cannot agree with something it has not been given the authority to confirm.

---

## Sparring Partner Power Map

For each of the four flagship Sparring Partners, what the substrate enables versus what they can deliver without it.

### Reveal — Network Mapper (Diagnostic Listening System)

*Captures the implicit operating network as explicit Atlas View structure.*

| Without substrate | With substrate |
|---|---|
| One-time mapping exercise. Output is a document. | Findings indexed immediately. Next Reveal run on the same org starts from prior context. Lines Distinction patterns recognized from prior engagements. |
| Cannot distinguish administrative lines from accountability lines without manual analysis | Queries prior schema-fragments on org structure, cross-references with Lines Distinction patterns from Ruptiv Patterns library |
| Interview notes are unstructured. Synthesis is manual. | Transcripts indexed, entities extracted, stakeholder map built incrementally across interviews |

### Socratic — Assumption Challenger (Diagnostic Listening System)

*Surfaces the load-bearing assumptions the organization has been operating under.*

| Without substrate | With substrate |
|---|---|
| Assumption surfacing is conversation-dependent. No memory between sessions. | Queries findings from Reveal, cross-references with assumption patterns from prior engagements in Patterns library |
| Cannot know which assumptions are structurally load-bearing without full org context | Reads stakeholder map + system map + KPI baseline from prior Reveal run. Targets assumptions that, if wrong, break the most downstream processes |
| Each Socratic run is cold-start | Fragment store provides warm-start context. Socratic already knows the Lines Distinction gap before the first interview |

### Pattern — Engagement Listening System

*Proposes structural moves grounded in the Patterns library.*

| Without substrate | With substrate |
|---|---|
| Patterns library is a static document consulted manually | Ruptiv Patterns library is vectorized and queryable. Pattern recalls the most relevant structural building blocks for this org's specific diagnostic findings |
| Structural proposals are generic. No grounding in what worked at comparable organizations. | Cross-engagement Patterns index surfaces org-structure moves with evidence from prior deployments — scoped to Patterns layer, never leaking engagement-level data |
| Proposals cannot be traced to evidence | Every proposed move traces to a finding, which traces to a source, which traces to the audit log |

### Monitor — Operating Listening System

*Watches the running operating network and surfaces drift before it becomes failure.*

| Without substrate | With substrate |
|---|---|
| Monitoring requires re-integration after handoff. Listening stops when the engagement ends. | Wire substrate is live. Monitor reads the running network through the same connectors Reveal used to map it. No re-integration required. |
| Drift detection is periodic review against a static report | Drift detection is continuous comparison against live baseline fragments in the Index Substrate. Drift surfaces as a finding, which opens an issue, which routes to the right stakeholder |
| No way to distinguish intentional change from degradation | Fragment versioning provides a full history of the operating model. Monitor can distinguish "this changed because of a deliberate to-be push" from "this drifted without authorization" |

---

## The Compounding Mechanism

Ruptiv's brand attribute "Compounding" is technically specific. Every engagement should deepen the Patterns library, extend the Studios, and grow the Sparring Partner roster. Here is exactly how that happens.

```
Engagement N                     Engagement N+1
     │                                 │
     ▼                                 ▼
Findings emitted              Patterns library
     │                         queryable — richer
     ▼                         than Engagement N
Schema-fragments                      │
written (engagement-scoped)           ▼
     │                        Pattern agent proposes
     ▼                        moves with evidence
Synthesizer identifies         from N prior orgs
patterns → writes to
Ruptiv Patterns index
(cross-engagement,
 no engagement data,
 structural patterns only)
```

**The scoping rule that makes this safe:** Findings and schema-fragments are strictly engagement-scoped — never queryable outside that engagement. The Patterns library is the only cross-engagement surface. Synthesizer imprints are authorized to read engagement findings and write to the Patterns index, but not to write engagement data into the cross-engagement surface. The imprint header enforces this. It is not a policy. It is an authority boundary.

**What compounds:** Structural patterns (org design moves, process redesign moves, Lines Distinction gap types). Not client data. Not engagement findings. The intelligence compounds. The evidence stays scoped.

---

## Engagement Lifecycle

An engagement moves through five states. Transitions are substrate-enforced — the system prevents out-of-order progression.

| State | Entered when | Who can advance |
|---|---|---|
| `active` | Charter artifact signed and indexed | Mission Control |
| `synthesizing` | All phase findings present for at least one complete phase | Capsule (auto) |
| `handoff_eligible` | All required facets populated, zero open halt-severity questions | Substrate (auto, computed) |
| `signed` | Mission Control signs the handoff artifact | Mission Control only |
| `closed` | Signed handoff delivered and connector credentials rotated | Mission Control |

Engagements cannot move backward. A `signed` engagement cannot reopen. If post-handoff issues surface, a new engagement opens against the existing Atlas View instance — the prior fragments are the baseline.

**Open question registry:** During every agent run, unresolved items are logged as open questions — structured records with a facet, severity (`warn` or `halt`), originating imprint and run, and resolution status. Halt-severity questions block `handoff_eligible`. The open question half-life (median age of unresolved questions per engagement) is the primary metabolism indicator — a rising half-life means synthesis is stalled or agents are surfacing questions faster than Mission Control is resolving them.

---

## Patterns Library Data Model

The compounding surface. A Pattern is a cross-engagement structural building block — not client data, not a finding, not a schema-fragment. It is a distilled structural move that applies across organizations.

```
Pattern
├── pattern_id        TEXT  — stable identifier, e.g. "pat-lines-distinction-gap"
├── name              TEXT  — "Lines Distinction Gap Pattern"
├── category          TEXT  — org-structure | process | role | integration | governance
├── description       TEXT  — what the pattern is and when it applies
├── evidence_count    INT   — how many engagements contributed to this pattern
├── applicability     JSONB — conditions under which this pattern applies
├── structural_moves  JSONB — recommended interventions, scoped to Five-D phase
├── schema_version    TEXT
└── last_updated      TIMESTAMPTZ
```

Patterns are written by synthesizer imprints that are explicitly authorized to access the cross-engagement Patterns index (`authority.write: ["pattern"]`). Patterns do not contain client data. They contain structural logic — the kind of thing a senior practitioner carries between engagements. Pattern agents query this index via the vector bus using the Patterns-scoped query surface, which is separated from the engagement-scoped query surface by index partition. A Pattern query cannot inadvertently return a finding from a live engagement.

---

## Current GrowDirect R&D → Production Atlas View

GrowDirect's memory bus is the prototype substrate. It is a research-grade vector index — powerful for internal recall, not yet hardened to Atlas View production requirements.

| Current capability | Atlas View requirement | Delta |
|---|---|---|
| pgvector + qwen3-embedding dense index | Index substrate with engagement scoping, hybrid (dense+sparse), rerank | Add engagement_id partitioning, sparse vector column, reranker |
| `memory_type` enum (10 types) | Full artifact taxonomy with typed envelopes, validated on write | Extend enum, add envelope schema validation on write |
| `layer` + `engines` filters | Engagement-scoped isolation (cell wall) | Replace with engagement_id primary partition |
| Session lifecycle (start/close) | Engagement lifecycle with charter, required facets, handoff gate | Add charter artifact, required_facets tracking, signing gate |
| Seed pipeline (whole-doc, 6000-char truncation) | Semantic + hierarchical chunking pipeline | Replace truncation with semantic chunker, parent-child indexing |
| `memory_recall()` | Scoped hybrid recall with audit emission | Add scope pre-filter, hybrid fusion, reranker, audit event on every query |
| Brain wiki cards (166 cards) | Schema-fragments with typed envelopes + supersedes chain | Add envelope validation, facet field, supersedes chain |
| — | Fragment substrate (append-only per-facet records) | Net new |
| — | Wire substrate (bidirectional MCP connectors) | Net new |
| — | Imprint library (Ruptiv Patterns + Lenses as versioned punch cards) | Net new — this is where Ruptiv's IP lives |
| — | Open question registry | Net new |
| — | Cross-engagement Patterns index | Net new — the compounding surface |

GrowDirect's Brain wiki + memory bus is the dogfood deployment. The same architecture that powers GrowDirect's internal knowledge compound is what gets deployed as Atlas View for clients. We prove the substrate on ourselves before we promise it to anyone else.

**What is running today — GrowDirect as Engagement N=1:**

| GrowDirect R&D (running) | Atlas View analogue | Notes |
|---|---|---|
| Brain wiki cards (166 cards) | Schema-fragments | Cards are per-domain structured knowledge — same shape as fragments, missing typed envelopes and supersedes chain |
| `memory_recall()` over pgvector | Scoped index query | Dense-only, no hybrid, no engagement scope filter — but the recall mechanism is proven |
| Post-commit seed hook (Brain/wiki/ → pgvector) | Synthesizer imprint → index re-seed | Same event pattern: knowledge written → bus updated automatically |
| Session lifecycle (session_start / session_close) | Engagement lifecycle | Engagement ID, status machine, and handoff gate are the delta |
| `domain_context()` | Capsule loading charter + prior fragments | Same intent: assemble scoped context before agent acts |
| Linear dispatches (Dispatch project) | Imprint dispatch + issue tracker | Operational instructions as issues, lifecycle tracked — same model |
| CLAUDE.md + capability cards | Imprint header | System context + declared authority — same conceptual role, not yet formalized as JSON schema |

---

## SLA Surface

Five signals that tell you Atlas View is operating. These are observable, not aspirational.

| Signal | Target | What breaks if missed |
|---|---|---|
| Recall freshness | < 30s from finding emission to queryable | Next agent in the run-loop starts with stale context |
| Scope isolation | 0 cross-engagement results | Client data leaks between engagements. Engagement-as-Agent-Equivalence collapses. |
| Schema validation rate | 100% on write | Malformed findings propagate downstream into schema-fragments. Invoice evidence is corrupted. |
| Handoff eligibility gate fires correctly | Blocks when required facets unpopulated or halt-severity issues open | Handoff is signed against an incomplete engagement. The invoice has no evidence basis. |
| Open question half-life | Trending down per engagement | Synthesis is stalled. Engagement is accumulating unresolved issues. Listening Systems have blind spots. |

---

## What This Enables Ruptiv to Promise

| Ruptiv says | Atlas View makes it true |
|---|---|
| "The operating model becomes queryable in Atlas View" | Index substrate + fragment store = queryable, structured record of the operating model |
| "Listening Systems keep running after we leave" | Wire substrate live post-handoff + Monitor agent reading continuously |
| "Every engagement compounds the Patterns library" | Cross-engagement Patterns index + synthesizer imprints that write structural patterns without leaking client data |
| "We invoice when the cost line moves" | As-is/to-be fragment diff + audit trail = provable invoice basis |
| "The next engagement starts where the last one left off" | Patterns library queryable by Pattern agent from day one of each new engagement |
| "Honest-Voice is structural" | Imprint authority boundaries + scope isolation = agent cannot confirm what it has not been authorized to assess |

---

## Companion Documents

- `Brain/wiki/Mercury.html` — Decision Substrate primer v1
- `Brain/raw/inbox/Screenshot 2025-06-27 at 3/Ruptiv Naming Architecture IM v4.docx` — Naming architecture
- `Brain/raw/inbox/Screenshot 2025-06-27 at 3/Ruptiv Positioning IM v5.docx` — Positioning v5
- `Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md` — Artifact types and envelope spec
- `Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md` — Imprint header schema
- `services/memory-bus/` — GrowDirect prototype substrate (current R&D)
