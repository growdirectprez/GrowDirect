---
card-type: platform-thesis
card-id: platform-property-pack-methodology
card-version: 1
domain: platform
layer: cross-cutting
status: approved
agent: ALX
tags: [property-pack, capability-decomposition, l1-l2-l3, tom-prior-art, tesco, methodology, kpi, interdependency, big-4, differentiation]
last-compiled: 2026-05-02
needs-review: false
---

# Pattern: Property Pack — Capability Decomposition Methodology

## What this is

Every Canary capability — module, registry, agent, integration surface — is documented in **Property Pack format**: a standardized capability-decomposition deck that follows the 2006 Tesco TOM (Target Operating Model) template. Each Pack carries: executive summary, principles, benefits, Level 1 process inventory, Level 2 process decomposition, KPIs per process, dependencies on other capabilities, and outstanding key decisions.

The format is **not invented; adopted.** The Tesco TOM Property Pack template (Seth Lazarus, July 2006, V.5) is the reference implementation, preserved as canonical prior art at `Brain/raw/inbox/tom-top-down-design---property-pack-template-jul-06-v5.md`.

## Purpose

Big 4 / TOM-grade capability documentation methodology, applied at SMB-platform scale. The Property Pack format gives Canary's documentation:

1. **Standard structure** — every capability is documented the same way; readers find what they need at the same section every time
2. **Process decomposition** — each capability decomposes from L1 (what we do) → L2 (how we do it) → L3 (run-time process) with KPIs at every level
3. **Dependency surfacing** — each capability declares its dependencies on other capabilities, making the dependency graph queryable (Brain wiki Bases query renders this directly)
4. **Decision tracking** — outstanding decisions and their owners are first-class artifacts, not buried in meeting notes
5. **Audit trail** — versioned (V.5 in the Tesco original; cards carry `card-version` frontmatter)

This is the same rigor that produced the GSLM canonical model and the TOM interface designs. Adopting it for Canary means our capability documentation reaches the same bar as the largest retail enterprises — at a price point Bart's customers can absorb.

## The Property Pack structure

| Section | Content |
|---|---|
| **Executive Summary** | What this capability covers; key benefits; main dependencies; key decisions to be made |
| **Principles** | The capability's philosophical underpinnings (≤ 12 bullet points, in present-tense first person — *"We always strive to..."*) |
| **Benefits** | Numbered list of business benefits, each with 2–3 supporting actions |
| **L1 Processes** | Table: What we do (short) · What does that mean (detailed) · Why we do it · How we measure it (KPIs) |
| **Key Decisions** | Outstanding decisions: who has the A, when, impact if not decided |
| **Appendix 1: L2 Processes** | Each L1 process decomposes to L2 sub-processes, each with a KPI |
| **Appendix 2: Interdependencies** | Each L1/L2 process declares its upstream/downstream dependencies on other capabilities |

## Mapping to Canary

| Tesco TOM concept | Canary equivalent |
|---|---|
| Property Services | A Canary capability (e.g., loss prevention, OTB, item catalog, geographic compliance) |
| Property Pack template | `Brain/templates/property-pack.md` |
| L1 process | A bounded sub-domain of the capability (e.g., LP detection, LP investigation, LP evidence anchoring) |
| L2 process | An executable workflow (a Canary MCP tool, a case-type, an interface) |
| L3 process | A run-time dispatch (CAN-RES-001-style L3 process flow) |
| KPI per L2 | Meter (per [[platform-thesis]]) |
| Dependency on other capability | `feeds` / `receives` in card frontmatter (already part of card schema) |
| Key decisions | `needs-review: <date>` flag in frontmatter; outstanding-decisions section |

## Composition with existing platform patterns

| Pattern | Role |
|---|---|
| [[platform-architectural-continuity]] | Composition over invention — Property Pack adoption IS this pattern applied to documentation methodology |
| [[platform-thesis]] | Every meter (KPI) lands in a Pack |
| [[platform-case-type-registry-pattern]] | Case-type registry IS an L2 process catalog under the Hawk Pack |
| [[infra-cadence-ladder]] | L2 process cadence aligns to the cadence ladder |
| [[platform-geographic-compliance-resolver]] | Compliance Pack uses Property Pack format; resolver is its L1-process anchor |
| [[platform-parcel-as-anchor]] | Parcel-anchored capabilities each get a Pack |

## When to write a Property Pack

| Trigger | Outcome |
|---|---|
| New module ships (new `cmd/<service>` in the spine) | Property Pack at `Brain/wiki/cards/canary-<module>.md` |
| New registry pattern emerges (case-type, interface, regulation) | Property Pack at `Brain/wiki/cards/platform-<pattern>.md` |
| New cross-cutting concern surfaces | Property Pack at `Brain/wiki/cards/platform-<concern>.md` |
| Capability evolves materially (≥ 3 new L2 processes, or scope reclassification) | New Pack version; old version archived |

The Pack is the deliverable; the work of writing it is the deep-dive that surfaces dependencies and KPIs that wouldn't otherwise be made explicit.

## Differentiation

SMB retail platforms typically document via README files, support knowledge bases, or vendor-supplied PDFs — none of which decompose capability into measurable processes with declared interdependencies. Mid-market platforms (NCR Voyix, Lightspeed) document via service-level agreements that specify outcomes but not processes. Enterprise platforms (Oracle Retail, SAP Retail) use formal capability models — but they are vendor-proprietary, not adopted from the public TOM family.

**Canary adopts the TOM Property Pack methodology directly** — same format Tesco uses, applied to every capability the platform delivers. The differentiation is methodology rigor at SMB price point. Bart's team gets enterprise-grade capability documentation as a free benefit of the joint product. **First-mover advantage at this layer is rigor, not novelty: SMB platforms haven't done this because their markets didn't expect it; Canary changes the expectation.**

## Anti-pattern

Don't document capabilities ad hoc. Don't write README-style documentation for production capabilities. Don't bury dependency relationships in code comments. Every production capability ships a Pack; every Pack lives in the wiki; every Pack declares its frontmatter (dependencies, KPIs, decisions, version).

## See also

- Card: [[platform-architectural-continuity]] — the meta-pattern (composition over invention)
- Card: [[platform-thesis]] — meters belong in Packs
- Card: [[platform-parcel-as-anchor]] — parcel-anchored capabilities each get a Pack
- Card: [[platform-geographic-compliance-resolver]] — example of a Pack-formatted pattern card
- Card: [[platform-case-type-registry-pattern]] — example of a Pack-formatted pattern card
- Source: Tesco TOM Property Services Pack (Seth Lazarus, July 2006, V.5) — `Brain/raw/inbox/tom-top-down-design---property-pack-template-jul-06-v5.md`
- Methodology lineage: BCG / McKinsey / Bain / PwC capability-decomposition deck formats
