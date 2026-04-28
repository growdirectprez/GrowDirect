---
card-type: format-spec
card-id: agent-card-format
card-version: 1
domain: platform
layer: cross-cutting
status: approved
last-compiled: 2026-04-28
needs-review: false
---

# Agent Card Format

The agent card format is the standard for knowledge units that agents consume via the memory bus. It replaces relational lookup tables with flat files that embed into pgvector through the existing seed pipeline. No new DB schema is required — the `growdirect_memory` vector store is the only persistence layer.

## Design Principles

**One concept per card.** A card holds exactly one idea — a signal, an agent, a hierarchy axis, a lifecycle gate. If a card needs subsections for multiple concepts, split it.

**Every section embeds independently.** The memory bus seeder chunks by heading. Each section must make sense when retrieved without the rest of the card. Write sections as if they will be read cold.

**Frontmatter is machine data.** All relational facts (what feeds what, which agent owns this, which module consumes it) live in frontmatter arrays. The body is prose that embeds well. Agents can filter on frontmatter fields before running semantic search.

**No volatile data.** Row counts, live metrics, and current-state summaries do not belong in cards. Cards capture structure, relationships, constraints, and context.

---

## Frontmatter Schema

### Required fields

| Field | Type | Values |
|-------|------|--------|
| `card-type` | enum | `signal-feed` · `agent-profile` · `org-layer` · `field-hierarchy` · `role-binding` · `domain-module` · `lifecycle-gate` · `infra-capability` · `platform-thesis` · `format-spec` |
| `card-id` | string | kebab-case unique identifier, stable across versions |
| `card-version` | integer | Increment on any substantive change |
| `domain` | enum | `lp` · `merchandising` · `finance` · `labor` · `platform` · `local-market` · `cross-cutting` |
| `layer` | enum | `domain` · `infra` · `local-market` · `cross-cutting` |
| `status` | enum | `draft` · `approved` |

### Optional fields

| Field | Type | Purpose |
|-------|------|---------|
| `agent` | string | Agent that owns or primarily uses this card |
| `feeds` | array | card-ids or module codes this concept feeds into |
| `receives` | array | card-ids or module codes that feed into this concept |
| `tags` | array | Search terms for memory bus recall |
| `milestone` | string | M1–M6 PMO milestone (domain modules only) |
| `last-compiled` | date | ISO 8601, set by content-engine lint |
| `needs-review` | boolean | Set by content-engine lint on frontmatter issues |

---

## Body Conventions

### Section headings (use these in order, omit any that don't apply)

```
## What this is
One-sentence definition. This is the identity chunk — retrieved first by semantic search.

## Purpose
Agent-facing "why this exists." What problem does it solve, what decision does it inform.

## Structure
For hierarchies, role models, org layers: the data shape, constraints, enumerations.

## Signal
For signal feeds: what the signal contains, frequency, format, quality characteristics.

## Consumers
Which agents or modules use this. What they do with it. Be specific about the action, not just the name.

## Sources
Where the data comes from. External systems, feeds, human inputs.

## Routing
How it flows through the agent network. Show the chain explicitly.

## Invariants
Hard constraints. What must always be true. What must never happen. Agents enforce these.

## Related
Links to related cards using [[card-id]] syntax. One line per related card with a brief note.
```

---

## How Cards Enter the Memory Bus

Cards in `Brain/wiki/` (including subdirectories) are picked up by the seed pipeline:

```bash
python3 services/memory-bus/scripts/seed_standalone.py
```

The seeder chunks each card at heading boundaries and embeds each chunk with `qwen3-embedding:8b` (1024-dim). Chunks are stored in `growdirect_memory` with the file path and heading as metadata.

**Agent recall:**
```
memory_recall("social threat detection signal local market")
memory_recall("merchant org hierarchy head office role")
memory_recall("geography hierarchy LP district")
```

**Filtered recall (frontmatter fields):** The seeder stores frontmatter as chunk metadata. Future memory bus versions will support pre-filter by `card-type`, `domain`, or `layer` before vector search.

---

## Versioning

Increment `card-version` on any substantive change. The seed pipeline is incremental by mtime — a version bump forces re-embedding even if the file timestamp doesn't change (when using `--force`). Do not reset `card-version` to 1 on edits; that signals a rewrite, not an update.

---

## Card Directory

All agent cards live in `Brain/wiki/cards/`. Subdirectories are permitted for large domains but the flat directory is preferred until there are more than ~50 cards.

| Card | ID | Type |
|------|----|------|
| [Merchant Org Hierarchy](cards/merchant-org-hierarchy.md) | merchant-org-hierarchy | org-layer |
| [Geography Hierarchy](cards/geography-hierarchy.md) | geography-hierarchy | field-hierarchy |
| [Category Hierarchy](cards/category-hierarchy.md) | category-hierarchy | field-hierarchy |
| [Role Binding Model](cards/role-binding-model.md) | role-binding-model | role-binding |
| [Local Market Agent](cards/local-market-agent.md) | local-market-agent | agent-profile |
| [Signal: Seasonality](cards/signal-seasonality.md) | signal-seasonality | signal-feed |
| [Signal: Weather + Zone SEO](cards/signal-weather-seo.md) | signal-weather-seo | signal-feed |
| [Signal: Social Threat Detection](cards/signal-social-threat.md) | signal-social-threat | signal-feed |
| [Signal: Civil Services](cards/signal-civil-services.md) | signal-civil-services | signal-feed |
| [Signal: Community Intelligence](cards/signal-community-intel.md) | signal-community-intel | signal-feed |
| [Signal: Property & Landlord](cards/signal-property-landlord.md) | signal-property-landlord | signal-feed |
| [Infra: Blockchain Evidence Anchor](cards/infra-blockchain-evidence-anchor.md) | infra-blockchain-evidence-anchor | infra-capability |
| [Infra: L402 OTB Settlement](cards/infra-l402-otb-settlement.md) | infra-l402-otb-settlement | infra-capability |
| [Platform Thesis](cards/platform-thesis.md) | platform-thesis | platform-thesis |
| [Platform: Retailer Lifecycle Test](cards/platform-retailer-lifecycle-test.md) | platform-retailer-lifecycle-test | infra-capability |
| [Platform: ALX as VSM](cards/platform-alx-vsm.md) | platform-alx-vsm | platform-thesis |
