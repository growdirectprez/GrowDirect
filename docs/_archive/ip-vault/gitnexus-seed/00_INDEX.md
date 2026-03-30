---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary IP — GitNexus Contextual Memory Index

> **Purpose:** Master manifest for seeding GitNexus semantic search and contextual memory.
> **Generated:** 2026-03-19 | **Source:** iCloud Canary_IP + GrowDirect/IP + Canary codebase
> **Scope:** All curated intellectual property for the Canary LP platform by GrowDirect Inc.

---

## Document Set

| File | Domain | Semantic Coverage |
|------|--------|-------------------|
| `01_PRODUCT.md` | Product vision, services, features, detection rules | What Canary is and does |
| `02_ARCHITECTURE.md` | Stack, data model, schemas, protocols, pipeline | How Canary is built |
| `03_STRATEGY.md` | Market positioning, investor narrative, competitive landscape | Why Canary wins |
| `04_RESEARCH.md` | IBM lineage, LP patterns, academic references, industry context | Where Canary comes from |
| `05_OPERATIONS.md` | Deployment, infrastructure, testing, team, workflow | How Canary ships |
| `06_GLOSSARY.md` | Terms, acronyms, entity definitions, enum values | What terms mean |
| `07_DATA_GAPS.md` | CRDM v1.1 gap-to-target map, migration sequence, blocked rules | What needs building next |

---

## Source Asset Map

### GrowDirect/Canary (Codebase)
- `CLAUDE.md` — Agent instructions, hard rules, workflow, coding standards
- `README.md` — Stack overview, quick start, service directory
- `docs/sdds/` — Service Design Documents (per-service specs)
- `docs/profiles/` — Team member profiles (Owl, ALX, etc.)
- `docs/field-registry.md` — 130+ searchable fields, enums, join paths
- `docs/field-registry.json` — Machine-readable field catalog
- `.gitnexus/meta.json` — Repository index (1,323 files, 6,791 nodes, 17,036 edges)

### GrowDirect/IP (Curated IP)
- `adr/ADR-001` — Multi-Tenant Partition Architecture
- `specs/elJeffe_Protocol_Spec_v1.0.md` — Core verification protocol
- `specs/Inscription_Pipeline_Design_Spec_v1.0.md` — Merkle batching pipeline
- `specs/CRDM_v1.1_Addendum.md` — Schema migration (namespace, device attestation)
- `specs/field_mappings.md` — Square webhook → CRDM field transforms
- `infra/deployment_pipeline.md` — Deploy scripts, environments, tunnels
- `infra/lab_network.md` — Lab topology, hardware, Docker inventory
- `infra/infra_roadmap.md` — Phase 1–4 infrastructure plan
- `research/lp-dashboard-pattern-catalog.md` — 197 figures, 52 high-relevance patterns
- `research/WORM_Exposure_Sprint_Deliverables.md` — SEO, landing page, community plan
- `research/ibm_retail_bi/` — IBM BI V7 lineage research
- `warchest/` — Investor briefs, one-pager, site content, published materials
- `testing/MERCHANT_PROFILE.md` — Square sandbox test data
- `workorders/` — 60+ work orders (GRO-prefixed Linear issues)

### iCloud Canary_IP (Archive)
- `Markdown/Strategy/` — Attack plan, MVP epics, roadmap (26 docs)
- `Markdown/Specs/` — Tech blueprint, CRDM, functional requirements (35 docs)
- `Markdown/Research/` — Alpha3X stack, cannabis risk dictionary, reference library (7 docs)
- `Markdown/PRDs/` — Product requirements documents
- `Markdown/ADRs/` — Architectural decision records
- `Markdown/Modules/` — Module-level documentation
- `Markdown/Alpha3X/` — Alpha3X infrastructure docs
- `Markdown/Guides/` — Developer and user guides
- `Markdown/Sessions/` — Session summaries and logs
- `Documents/` — Legal, sales decks, white papers, product guides (80+ files)
- `Archive/` — ARTS Standards, Heartbeat, legacy docs, Walmart SRA
- `CLAUDE_LEGACY.md` — 97KB historical project context

---

## Semantic Search Optimization

These documents are structured for chunk-based retrieval. Each section is self-contained with:
- Clear H2/H3 headers as chunk boundaries
- Keyword-dense opening sentences per section
- Entity names, GRO issue references, and technical terms inline
- Cross-references to source files where applicable

**Recommended chunk size:** 512–1024 tokens per section
**Embedding model:** Compatible with any text embedding (Ada-002, Cohere, local)
**Deduplication:** Each document covers a distinct domain; minimal overlap by design

---

*Canary LP | GrowDirect Inc. | Confidential*
