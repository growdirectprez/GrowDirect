---
card-type: domain-module
card-id: canary-hawk
card-version: 1
domain: platform
layer: domain
agent: hawk-agent
feeds:
  - canary-fox
  - canary-alert
  - canary-report
  - canary-blockchain-anchor
receives:
  - canary-identity
  - canary-chirp
  - canary-tsp
  - canary-employee
  - canary-customer
  - canary-receiving
  - canary-returns
  - canary-compliance
tags: [hawk, case-management, universal-envelope, registry-as-data, mcp, dsg-prior-art, lifecycle, m2]
milestone: M2
status: approved
last-compiled: 2026-05-02
needs-review: false
---

# Canary Service: hawk

## What this is

Hawk is the **universal envelope for any form or message packet that flows between home and store** with a defined lifecycle, owner, schema, and audit trail. Loss-prevention case management is one case-type instance — a foundational one — but Hawk's actual scope is every cadence-fired or human-initiated structured workflow that needs to be tracked, owned, escalated, and closed: planogram compliance, audit checklists, training acknowledgments, vendor disputes, cycle-count variance investigations, deposit deviations, customer-complaint escalations, marketing-collateral receipt confirmations, employee corrective actions, regulatory inspections, and the LP/safety/incident catalog inherited from the DSG-era retail LPMS systems.

Hawk holds the envelope; the **case-type registry** holds the schema for each kind of case (see [[platform-case-type-registry-pattern]]); the **wiki templates** at `Brain/templates/case-type.md` make new case types definable without code change.

## Tier mix and axis

| Property | Value |
|---|---|
| Port | `:8082` |
| Axis | B — Resource APIs · C — Agent Surface (MCP) |
| Tier mix | Reference (case-type registry, case search, case detail) · Change-feed (case event log, audit trail) · Stream (case create, state transition, close, escalate) · Bulk window (period close, archive, evidence export) |
| Owned tables | `app.hawk_case_types`, `app.hawk_cases`, `app.hawk_case_events`, `app.hawk_case_attachments`, `app.hawk_case_assignments`, `app.hawk_case_outcomes` |
| MCP server | `canary-hawk` — 8 tools |

## MCP surface (Axis C)

| Tool | Tier | Purpose |
|---|---|---|
| `hawk.list_case_types` | Reference | Discover available case-type schemas (cadence, owner, fields) |
| `hawk.case_type_detail` | Reference | Full schema for one case type — fields, state machine, anchors |
| `hawk.create_case` | Stream | Instantiate a new case from a case-type schema |
| `hawk.search_cases` | Reference | Find cases by type, status, store, date range, owner |
| `hawk.case_detail` | Reference | Full case record + event log |
| `hawk.transition_case` | Stream | Move case to a new state per the case-type state machine |
| `hawk.close_case` | Stream | Resolve case with outcome; emits Fox event for evidence anchor |
| `hawk.escalate_case` | Stream | Route case up the SLA / ownership chain |

## Purpose

Three things Hawk does that nothing else in the spine does:

1. **Universal lifecycle envelope.** Every case carries fields, state machine, owner, SLA, anchor points. Adding a new case type is a wiki-template fill, not a code change. The DSG-era LPMS used JPG screenshots of wizard UIs as the schema spec; Hawk uses markdown templates with frontmatter — same pattern, machine-readable, version-controlled.

2. **Cadence-fired automation.** Cases instantiate on cadence events from the [[infra-cadence-ladder|cadence ladder]] (e.g., daily planogram-compliance check on Monday morning, weekly audit checklist on every store, real-time LP detection from chirp). The agent network owns the firing.

3. **Cryptographically anchored audit trail.** Every state transition emits an event into [[canary-fox]]'s append-only chain, with the close event anchored on Bitcoin L2 via [[canary-blockchain-anchor]]. Insurance underwriters, regulators, and lenders can verify what happened in a store without trusting any party's word.

## Schema (case type as data)

Case types are markdown documents under `Brain/templates/case-type/<name>.md` with frontmatter carrying: `case-type-id`, `name`, `description`, `class`, `visibility`, `trigger`, `cadence-tier`, `owners`, `required-fields`, `state-machine`, `routing-rules`, `closure-criteria`, `anchor-points`, `related-modules`. The schema is registered into Hawk's `app.hawk_case_types` table at deployment; agents and operators discover available case types via `hawk.list_case_types`.

Full schema definition lives in [[platform-case-type-registry-pattern]] and the template at `Brain/templates/case-type.md`.

## Dependencies

- canary-identity (JWT, merchant scope, RBAC for case visibility)
- canary-fox (evidence anchor for case events)
- canary-raas (case namespace + chain hash)
- canary-employee (assignment routing, SLA escalation)

## Consumers

- AI agents (PMO module agents instantiate cases on cadence)
- Cowork / store-brain operator UI (humans fill in case forms)
- canary-alert (high-severity cases trigger alerts)
- canary-report (case extracts feed standard reports — DSG corpus's "Yearly Case Extract" pattern)
- canary-blockchain-anchor (close events get Bitcoin anchored)

## Sources

The universal-envelope reframe is grounded in the DSG-era Loss Prevention Management System (`Brain/raw/.extract/CaseManagement/`, ~2015), which ran a production case-management system at 700+ store scale with 60+ active case types organized into four classes (Critical Smart Alert, External, Internal, Incident). The DSG `Incident Types` schema (Status / Visibility / Class / Type / Definition), `Actions` lifecycle taxonomy (Closed Unfounded / Final Warning / Phone Interview / Quit During Interview / Terminated-Prosecuted / Released-To Guardian / Reported to ATF / etc.), and `Source of Info` trigger taxonomy (Tip-Anonymous / LPTV / Cycle Counts / Police / SysRepublic Secure Alerts / Implication / etc.) carry over as direct prior art for Hawk's case-type schema.

## Milestone reclassification

Originally scoped at M4 (Module Spine) for LP/incident case management. **Reclassified to M2 (Detection Core)** alongside `tsp`, `chirp`, and `fox` because the universal-envelope pattern is foundational to how every other module communicates with operators — not a downstream module add-on. The reclassification reflects the architectural reality that the case-type registry is platform infrastructure, not an LP feature.

## Anti-pattern

Don't build per-case-type custom UIs or per-case-type bespoke services. Every case type goes through the registry. If a domain needs special treatment, the case-type schema gains a new field; the envelope stays universal. The day Hawk has a code path for a specific case type is the day the abstraction failed.

## See also

- Card: [[platform-case-type-registry-pattern]] — the registry-as-data pattern
- Card: [[canary-fox]] — evidence chain anchor
- Card: [[canary-chirp]] — detection rule case-fire pattern
- Card: [[canary-blockchain-anchor]] — Bitcoin L2 close-event anchor
- Card: [[infra-cadence-ladder]] — case firing cadence
- Card: [[axis-agent]] — MCP surface
- Template: `Brain/templates/case-type.md` — operational template for new case types
- SDD: `docs/sdds/go-handoff/hawk-case-management.md`
- Source: `Brain/raw/.extract/CaseManagement/` (DSG LPMS 2015 corpus)
