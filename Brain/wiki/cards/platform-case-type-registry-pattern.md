---
card-type: platform-thesis
card-id: platform-case-type-registry-pattern
card-version: 1
domain: platform
layer: cross-cutting
status: approved
agent: ALX
tags: [case-management, registry-as-data, hawk, schema-as-data, dsg-prior-art, extensibility, agent-friendly, composition]
last-compiled: 2026-05-02
needs-review: false
---

# Pattern: Case-Type Registry as Data

## What this is

Every form, message packet, or structured workflow that flows between corp and store on the platform's ops clock is a **case** — and every case has a **case type** that defines its schema, lifecycle, owners, and anchor points. The set of case types is a registry. **The registry is data, not code.** New case types are added by filling in a wiki template; the platform consumes the schema and instantiates cases on cadence without engineering changes.

## Purpose

The 30-year history of enterprise retail field-case management — from the carbon-copy paper forms of the 1980s, through the wizard-screen UIs of the 2010s, to the JPG-screenshot schemas of the DSG-era LPMS at 2015 — followed the same pattern: a senior business analyst hand-authored a case-type definition, an engineering team built screens for it, an ops team rolled it out store-by-store, and the merchant operated cases through a fixed UI. Adding a case type was a 6–12 week engineering cycle.

The case-type registry pattern collapses that cycle. **Adding a case type is a wiki template fill plus a deployment trigger** — minutes, not months. The merchant gets infinite extensibility; the platform gets a clean abstraction; the agent network gets a consistent surface to operate against.

## The pattern (three layers)

| Layer | What it carries | Where it lives |
|---|---|---|
| **Registry** | The set of all case types available on the platform | `app.hawk_case_types` table; sourced from wiki templates at build/deploy time |
| **Schema** | Per-case-type definition: fields, state machine, owners, SLA, anchor points, routing rules | `Brain/templates/case-type/<name>.md` markdown with frontmatter |
| **Instances** | Live cases of each type — a row in `app.hawk_cases` keyed to a case-type ID | `app.hawk_cases` + `app.hawk_case_events` (append-only event log) |

## The schema (what every case type carries)

| Field | Type | Purpose |
|---|---|---|
| `case-type-id` | string | Stable identifier (e.g., `lp-inventory-variance-investigation`, `audit-quarterly-store-walk`) |
| `name`, `description` | string | Human-readable label and one-line summary |
| `class` | enum | LP / Safety / Operational / Compliance / Service / Marketing / Audit |
| `visibility` | enum | LP / All / Admin / DC LP / SSC LP — who can see / file this case |
| `trigger` | enum | real-time-event / scheduled-cadence / store-initiated / corp-initiated / regulatory-deadline |
| `cadence-tier` | enum | stream / change-feed / daily-batch / bulk-window / reference |
| `owners` | object | Corp-side role + store-side role |
| `required-fields` | array | The form schema — field name, type, validation, required flag |
| `state-machine` | object | States + transitions + guard conditions + entry/exit hooks |
| `routing-rules` | object | Initial assignment, escalation policy, SLA per state |
| `closure-criteria` | object | What counts as resolved; required attestations |
| `anchor-points` | array | Which state transitions emit Fox evidence-chain events |
| `related-modules` | array | Which Canary modules produce or consume case data |

## Why registry-as-data, not code-per-type

Three properties make registry-as-data strictly better than code-per-type:

1. **Composition.** A case type is a composition of primitives (state machine, form schema, routing rules) the platform already implements. Code-per-type duplicates the primitives; data-per-type composes them. This is a direct application of [[platform-architectural-continuity]] — composition over invention.

2. **Auditable.** Every case-type definition is in the wiki, version-controlled, diffable, reviewable. Changes flow through the same review process as any other Brain change. The DSG corpus's `Incident Types.xlsx` was a single file passed between analysts; Hawk's registry is a directory of markdown templates with full git history.

3. **Agent-friendly.** PMO module agents can author and propose new case types via the wiki template. The Controller agent can browse the registry to understand what's flowing across the spine. Humans and agents see the same artifact. The schema is both human-readable and machine-readable.

## Inheritance from DSG-era LPMS

The DSG retail LPMS (~2015) ran a production case-management system at 700+ store scale with 60+ active case types organized into four classes (Critical Smart Alert, External, Internal, Incident). The DSG `Incident Types` xlsx, `Actions` xlsx, and `Source of Info` xlsx are direct schema prior art:

| DSG concept | Hawk concept |
|---|---|
| `Incident Types.xlsx` (Status / Visibility / Class / Type / Definition) | Case-type registry frontmatter |
| JPG wizard screens (Active Shooter, Inventory Variance, Missing 4473, Robbery, etc.) | Case-type schemas as markdown templates |
| `Actions.xlsx` (Closed Unfounded / Final Warning / Phone Interview / Quit During Interview / Terminated-Prosecuted / Released-To Guardian / etc.) | State-machine outcomes per case type |
| `Source of Info.xlsx` (Tip-Anonymous / LPTV / Cycle Counts / Police / SysRepublic Secure Alerts / Implication / etc.) | Trigger taxonomy on the case schema |
| Reports (Open Analyst Investigations, Weekly Recap, Yearly Case Extract) | canary-report standard rollups |

What Hawk exceeds: cryptographic anchoring of close events (DSG had log files; Hawk has Fox + blockchain-anchor); MCP-driven case lifecycle (DSG had a custom UI; Hawk has agent-callable tools); markdown schemas (DSG had JPG screenshots; Hawk has version-controlled templates).

## Cadence coupling

Case instantiation is wired to the [[infra-cadence-ladder|cadence ladder]]:

| Cadence tier | Example case types |
|---|---|
| Stream | Critical Smart Alert (Active Shooter, Robbery, Workplace Violence) — fired in real-time from store-brain or chirp |
| Change-feed | LP detection cases (chirp rule fires → case opens) |
| Daily batch | Cycle-count variance investigation (overnight cycle count → flagged variance → case opens) |
| Bulk window | Quarterly store-walk audit (scheduled for first week of quarter) |
| Reference | Annual compliance attestations (regulatory deadlines) |

The case type declares its expected tier in `cadence-tier`; the cadence ladder governs the timing.

## Composition with the spine

The pattern composes cleanly with five existing platform primitives:

- [[infra-cadence-ladder|cadence ladder]] — case instantiation timing
- [[axis-agent]] — case lifecycle as MCP tools (`hawk.create_case`, `hawk.transition_case`, etc.)
- [[canary-fox]] — evidence-chain anchor for state transitions
- [[canary-blockchain-anchor]] — Bitcoin L2 anchor for close events
- [[canary-raas]] — case namespace + chain hash

## Anti-pattern

Don't add a case type by writing code. The day Hawk has a code path for a specific case type is the day the registry abstraction failed. If a case type genuinely needs platform-level support (new field type, new state-machine pattern, new anchor primitive), extend the registry schema for ALL case types and update the case type itself afterward.

## See also

- Card: [[canary-hawk]] — the module that runs the registry
- Card: [[canary-fox]] — evidence chain
- Card: [[canary-blockchain-anchor]] — Bitcoin L2 close-event anchor
- Card: [[infra-cadence-ladder]] — case firing cadence
- Card: [[platform-architectural-continuity]] — composition-over-invention pattern
- Template: `Brain/templates/case-type.md` — the operational schema template
- Source: `Brain/raw/.extract/CaseManagement/` — DSG LPMS 2015 corpus (Incident Types, Actions, Source of Info)
- SDD: `docs/sdds/go-handoff/hawk-case-management.md`
