---
type: dispatch
status: ready-to-dispatch
date: 2026-04-25
target: claude-code-session (engineer agent, fresh)
priority: high
unblocks: ALXjr Engagement 2 (Boutique H&G chain on RAPID POS)
tags: [rapid-pos, arts-standards, content-engine-ingest, knowledge-corpus]
---

# Dispatch — RAPID POS Knowledge Corpus

A separate Claude Code session ingests RAPID POS public
documentation, SDK references, integration artifacts, and ARTS
POS standards into the GrowDirect content engine. Output: a
queryable corpus that the methodology agents (ALXjr, ALX, future
delivery agents) can recall against.

## Context

ALXjr is producing a Phase-I diagnostic and Phase-II build scope
for a Boutique Home & Garden chain (~25 stores) running RAPID
POS. The methodology side of the work — diagnostic frame,
module priority, MCP tool surface, engagement scope — comes
from CATz + the retail spine.

The integration side — the actual API surface RAPID exposes,
data shapes, webhook contracts, SDK availability, ARTS POSLog
support — requires public documentation we do not currently
hold. Founder's read: he knows nothing concrete about RAPID's
internal interfaces. Starting from scratch.

This dispatch closes that gap.

## Scope — what to find and ingest

### Layer 1 — RAPID POS

Brand: RAPID POS (used by hardware / home & garden / farm-feed-
supply / specialty SMB retailers; vendor: Tri-Tech Systems).
Verify before deeper search.

Targets:
- Public product documentation (features, modules, capabilities)
- API documentation (REST endpoints, authentication, rate limits,
  pagination)
- Webhook specifications (event types, payload shapes, signature
  verification)
- SDK availability per language (Python, JS, Java)
- Integration partner documentation (what third-parties have
  publicly integrated)
- Data export formats (CSV, XML, EDI, ARTS XML)
- Reporting / extract surfaces (what data the back office can
  pull and in what format)
- Hardware inventory the POS supports (terminals, scanners,
  printers, cash drawers, scale integrations)
- Typical deployment shapes (single-store, multi-store, on-
  premise vs cloud, network requirements)

### Layer 2 — ARTS POS standards

Targets:
- POSLog v6 (current version) specification — the XML schema for
  POS transaction logs
- ARTS Customer Model — entity structure for unified customer
- ARTS Device Model — entity structure for POS devices
- ARTS Site Model — entity structure for stores / locations
- ARTS adoption catalog — which POS vendors publicly claim
  POSLog compliance and at what level
- Any open-source ARTS implementations (parsers, validators)

### Layer 3 — H&G specialty retail context

Targets:
- Public NRF / industry research on home & garden specialty
  retail operating patterns
- Common H&G operational challenges at the 10-50 store scale
  (seasonality, perishables for live goods, labor, multi-vendor
  buying patterns)
- Public benchmarks on H&G retail KPIs (sales per square foot,
  inventory turn, gross margin, labor cost as % of sales)
- Competitive landscape — who else sells back-office tooling to
  H&G chains in the SMB tier

Out of scope for this dispatch:

- Anything requiring NDA, paid access, or vendor credentials
- Anything specific to a named potential client retailer
- Strategic positioning or sales material (that's CATz, not
  this)

## Where findings land

### Raw intake

`Brain/raw/inbox/rapid-pos/` — newly created subdirectory. Each
source artifact lands here as either:

- The original file if downloadable (PDF, XML schema, etc.)
- A markdown extract if HTML (use markitdown or similar; preserve
  source URL in frontmatter `source:` field)
- A structured JSON for API references (preserve endpoint, method,
  parameters, response shape)

`Brain/raw/inbox/arts-standards/` — same pattern for ARTS
materials.

`Brain/raw/inbox/hg-retail-context/` — same for H&G context.

### Synthesis

After all three layers are ingested, produce three synthesis
articles in `Brain/wiki/`:

1. `Brain/wiki/rapid-pos-integration-surface.md` — what RAPID
   exposes, scored by usefulness for back-office integration.
   Sections: REST API surface, webhook surface, data export
   surface, ARTS compliance level, gaps.
2. `Brain/wiki/arts-pos-standards-adoption.md` — current ARTS
   landscape: POSLog v6 schema summary, vendor adoption status,
   reference implementations, integration patterns.
3. `Brain/wiki/hg-retail-operating-patterns.md` — H&G specialty
   operating patterns at the 10-50-store scale: KPIs, seasonality,
   labor model, vendor relationships, common back-office gaps.

### Memory bus ingestion

Run `cd ~/GrowDirect/services/memory-bus && python3 -m
memory_bus.cli ingest <path>` for each new wiki article so the
methodology agents (ALXjr, ALX) can recall against the corpus.

## Acceptance criteria

- [ ] At least 20 source artifacts ingested into
      `Brain/raw/inbox/rapid-pos/` (or fewer with documented
      reason — e.g., RAPID has limited public documentation)
- [ ] At least 5 ARTS standard documents in
      `Brain/raw/inbox/arts-standards/`
- [ ] At least 3 H&G context sources in
      `Brain/raw/inbox/hg-retail-context/`
- [ ] Three synthesis wiki articles produced with frontmatter:
      classification, source list, last-compiled date
- [ ] Memory bus ingestion confirmed — agent can recall against
      "rapid-pos webhook contracts" and return relevant chunks
- [ ] Gap register: explicit list of what couldn't be found and
      whether the gap blocks ALXjr's diagnostic

## Tools

The engineer agent operates with:

- `WebSearch` and `WebFetch` for public document discovery
- `Bash` + `markitdown` (already installed via earlier dispatch
  tooling) for binary-to-markdown extraction
- `content-engine` (`engine.py`) for intake / ingest workflow
  if applicable
- Standard Read / Edit / Write for wiki article production

No new dependencies. No paid APIs. No NDA-protected content.

## Estimated time

- Layer 1 (RAPID POS): 1-2 hours of search + extraction
- Layer 2 (ARTS): 1-2 hours
- Layer 3 (H&G context): 30-60 minutes
- Three synthesis articles: 1-2 hours
- Memory bus ingestion: 15-30 minutes

Total: 4-7 hours. Suitable for a single subagent dispatch with
checkpoint at the end of each layer.

## Sequencing

This dispatch can run in parallel with ALXjr's Quartz setup
(Engagement 1) and methodology-side diagnostic work (Engagement 2
section 1-2). It blocks ALXjr's RAPID-specific integration spec
(Engagement 2 section 3 RAPID API integration field).

## Out of scope (do NOT do)

- Do not contact RAPID Systems directly. Public documentation only.
- Do not assume non-public APIs exist without evidence.
- Do not produce a recommendation about whether to partner with
  RAPID. This dispatch is corpus-building, not strategy.
- Do not synthesize a competitive analysis of RAPID vs other POS
  vendors — out of scope for this dispatch.
- Do not modify any code in the Canary repo or elsewhere — pure
  knowledge ingest.

## Related

- `CATz/agents/ALXjr.md` — the analyst agent that depends on this
  corpus for Engagement 2
- `Brain/wiki/canary-tsp-pipeline.md` — internal reference for how
  Canary handles POS webhooks (informs what we'd need from RAPID)
- `Brain/wiki/retail-spine-solex-crosswalk.md` — internal reference
  for what a single-merchant POS-emitting source produces
- `Brain/wiki/canary-data-model.md` — internal reference for CRDM
  entity coverage

---

**Dispatch author:** Founder via Claude Code, 2026-04-25
**Executor:** Claude Code session (engineer agent)
**Review gate:** Founder reviews the three synthesis articles
before they merge to main / land in memory bus
