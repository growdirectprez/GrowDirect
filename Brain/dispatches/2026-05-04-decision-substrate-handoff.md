---
type: dispatch
status: ready-to-dispatch
date: 2026-05-04
priority: high
target: any
agent: any
unblocks: continued development of the decision substrate methodology and first live engagements
tags: [substrate, methodology, dispatch, handoff, ruptiv, rapidpos]
---

# Dispatch — Decision Substrate handoff

## Context

This dispatch summarizes a working session that defined an agent-native diagnostic methodology — the "decision substrate" — and produced its operating spec, three method execution primers (strategic positioning, information systems planning, SaaS), two audit method primers (ISO 27001, PCI DSS), customer-facing materials, an emailable PDF, a project plan template applied to a RapidPOS engagement, and a generator that produces new method primers from data.

The work assumes execution on GCP Vertex / Gemini Enterprise Agent Engine with A2A inter-agent comms and MCP tool surfaces. Anthropic Claude is the model layer (Sonnet for propagation agents, Opus for synthesis).

This dispatch is the takeover brief. A new agent (or operator) reading this and the referenced artifacts should be able to continue the work without re-litigating the model.

## Operating model — one-paragraph summary

Five-layer chain of command (mission control · astronaut · capsule · propagation agents · tools). Every artifact carries a typed envelope and is validated at write. Every imprint declares scope, authority, escalation rules, and output contract before the agent runs. Findings flow into a per-engagement bus indexed by facet. Synthesizers compose schema-fragments per facet. The same connector substrate that captures the as-is is used to push the to-be back to source systems. Audit log is append-only and traceable end to end.

## Spec cards (the "spine")

| Card | Path | Purpose |
|---|---|---|
| Artifact taxonomy | `Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md` | 10 canonical artifact types, universal envelope, per-type body schemas, naming, storage layout, validation discipline |
| Imprint header spec | `Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md` | Required header per imprint; chain-of-command discipline; input/output contract; tool catalog; validation rules; worked example |
| Execution primer template | `Brain/wiki/cards/execution-primer-template.md` | Method data schema; section order; substrate elements defined once; how to add a new method |
| ISO 27001 audit playbook | `Brain/wiki/cards/iso27001-audit-playbook.md` | Phases, imprints, facets, Annex A coverage, evidence requirements, findings rubric, sampling, sign-offs |
| PCI DSS audit playbook | `Brain/wiki/cards/pci-audit-playbook.md` | Phases, imprints, facets, requirement coverage, ASV / pen test handling, findings rubric, RoC + AoC structure |

## Execution primers (HTML)

All in `Brain/wiki/`. Built by `Brain/templates/execution-primer-generator.py`. Same nine-section structure: title + lead, what it produces, phase structure (diagram), imprints per phase, method overlay (diagram), data points produced, handoff package, companion specs.

| Primer | File |
|---|---|
| Diagnostic substrate (the chassis) | `diagnostic-execution-primer.html` |
| Strategic positioning | `strategic-positioning-execution-primer.html` |
| Information systems planning | `sisp-execution-primer.html` |
| SaaS | `saas-execution-primer.html` |
| ISO 27001 audit | `iso27001-audit-execution-primer.html` |
| PCI DSS audit | `pci-audit-execution-primer.html` |

To add a new method (e.g., SOC 2, HIPAA, GDPR, NIST CSF): append to `METHODS` in `Brain/templates/execution-primer-generator.py` per the spec card schema, run the script, new primer lands in `Brain/wiki/`.

## Customer-facing artifacts

| Artifact | File | Purpose |
|---|---|---|
| Decision substrate cover + 3-method tiles | `Brain/wiki/launch-plan.html` | Single top-view slide for executive read |
| Value case | `Brain/wiki/value-case.html` | What each engagement produces, what stays, why it compounds |
| Engagement overview mini-site | `Brain/wiki/engagement-overview.html` | Cover · why · methods · engagement timing · close |
| Unified mini-site (six sections in one nav) | `Brain/wiki/Mercury.html` | Cover · substrate · positioning · SISP · SaaS · value, sticky top nav |
| Emailable PDF | `Brain/wiki/decision-substrate.pdf` | Single-file deliverable, all six sections, page numbers |
| RapidPOS discovery & diagnostic — project plan | `Brain/wiki/rapidpos-discovery-engagement.html` | Scope · schedule · workstreams · architecture · roles · dependencies · risks · acceptance · commercials · approvals |

## Operational dispatches in flight

| Dispatch | File | Status |
|---|---|---|
| ISO 27001 audit engagement | `Brain/dispatches/2026-05-04-iso27001-audit-engagement.md` | Ready to dispatch — needs charter signature |
| PCI DSS audit engagement | `Brain/dispatches/2026-05-04-pci-audit-engagement.md` | Ready to dispatch — needs charter signature |

## Decisions pending from the founder

1. **Billing units in the rate card.** Principal stated as $2,000/day. Senior remote / on-site stated as $200 / $250 — confirm whether these are hourly or daily-equivalent. (See `rapidpos-discovery-engagement.html` Section 9.)
2. **Expense cap percentage.** Stated as ".05%" — confirm whether 5%, 0.5%, or 0.05% is intended. (Same section.)
3. **RapidPOS charter prerequisites.** Customer security lead identity, full engagement scope statement, SoA / merchant level / card brand confirmation (where applicable to method) before any audit dispatch can pick up.
4. **Ruptiv working papers ingestion.** Four files referenced (`Ruptiv Positioning IM v5.docx`, `Ruptiv Blue Ocean Strategy IM v6.docx`, `Ruptiv Brand Guide IM v5.pdf`, `Ruptiv Naming Architecture IM v4.docx`) were dropped as paths under `/Users/gclyle/Downloads/` — that path is not in the workspace mount. Files need to be moved to `/Users/gclyle/GrowDirect/Brain/raw/inbox/` (or uploaded via chat) before intake can run.
5. **Substrate name in customer-facing materials.** "Mercury Capsule" was dropped as marketing. The Rapid POS engagement plan refers to "the diagnostic platform" / "the deployment" / "the agent fleet" generically. Confirm whether a non-marketing internal codename is wanted, or keep generic.

## Open engineering work (when commit is made)

Not started. These are the build items that the methodology presupposes but has not yet implemented:

- Imprint authoring framework — JSON Schema validators for the header spec, plus a loader at runtime
- Tenant-scoped memory bus — productize `services/memory-bus` for per-engagement deployment
- Customer-side connector library — read-only first, architected for bidirectional write
- Engagement console — Cloud Run web UI showing fleet status, findings rate, open decisions, audit trail
- Per-engagement Terraform module — provisions GCP project, IAM, Workload Identity, Agent Engine, Secret Manager, Cloud Logging
- Per-method imprint catalog — concrete imprint headers for each playbook's listed imprints

## Open methodology work

- SOC 2 audit playbook (parallel to ISO 27001 / PCI structure)
- HIPAA audit playbook
- GDPR / data protection audit playbook
- NIST CSF audit playbook
- Surveillance audit (annual) variants of ISO 27001 and PCI
- Recertification audit (3-year) variants
- Per-control imprint headers as concrete YAML files
- Sampling tables per control / requirement category

## Voice and aesthetic standards (founder-set)

- Plain business English in customer-facing materials. No insider vocabulary at the front cover. Insider terms acceptable in spec cards and dispatches only.
- No marketing copy. No "ready to launch?" closes. No badges. No emoji. No hero "show off" framing.
- Clinical NOC aesthetic in HTML: dark theme (`#0d1117` background, `#58a6ff` accent), monospace for headings and code, generous whitespace, color = state (green/yellow/red, no decoration).
- IT-project-delivery voice for project plans (scope · schedule · roles · risks · acceptance · approvals).
- "No company names" in spec content body. File names and references can carry codenames operationally.

## How to take this forward

Three valid next moves, depending on priority:

1. **Move on engineering** — pick one open engineering item (imprint authoring framework is the lowest-cost highest-leverage starting point), commit a Linear issue, build.
2. **Move on a real engagement** — pick the most urgent of RapidPOS / ISO 27001 / PCI, pin the charter prerequisites, dispatch the relevant dispatch document.
3. **Move on additional methodology** — pick SOC 2 / HIPAA / GDPR / NIST CSF, draft the playbook spec card, add a `METHODS` entry, run the primer generator.

Whatever the next move, the operating model and substrate are stable. Edit the spec cards if the model shifts, regenerate primers from the updated `METHODS` data, and dispatch from the playbook directly.

## References

- Substrate operating spec: `Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md`, `Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md`
- Method playbooks: `Brain/wiki/cards/iso27001-audit-playbook.md`, `Brain/wiki/cards/pci-audit-playbook.md`
- Primer template: `Brain/wiki/cards/execution-primer-template.md`
- Generator: `Brain/templates/execution-primer-generator.py`
- All execution primers: `Brain/wiki/*-execution-primer.html`
- Customer-facing: `Brain/wiki/launch-plan.html`, `Brain/wiki/value-case.html`, `Brain/wiki/engagement-overview.html`, `Brain/wiki/Mercury.html`, `Brain/wiki/decision-substrate.pdf`
- Project plan: `Brain/wiki/rapidpos-discovery-engagement.html`
- Live dispatches: `Brain/dispatches/2026-05-04-iso27001-audit-engagement.md`, `Brain/dispatches/2026-05-04-pci-audit-engagement.md`
