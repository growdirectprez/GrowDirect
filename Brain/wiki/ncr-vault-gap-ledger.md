---
date: 2026-04-27
type: wiki
status: active
tags: [canary, ncr, infrastructure, gap-analysis]
sources: [docs/superpowers/specs/2026-04-27-ncr-vault-framework-wiring-design.md]
last-compiled: 2026-04-27
needs-review: 2026-05-11
method-role: Writer
method-stage: close
----


**Wiki:** [[Brain/Home|Home]]

# NCR Vault Gap Ledger

## Summary

Decision record for the NCR companion vault wiring (2026-04-27). Cross-references every NCR vault section against Brain/wiki coverage and records the outcome: Covered (Brain backs it), Forward-only (audience-specific, no generic equivalent needed), or Missing (back-fill required).

## Gap Ledger

| NCR Section | File | Brain Article | Outcome | Notes |
|---|---|---|---|---|
| agents | index.md | — | Forward-only | Navigation hub (hub-and-spoke diagram + links to vsm/architecture/roadmap). No substantive content. |
| agents | architecture.md | `canary-architecture.md` | **Missing** | Brain article covers Canary platform architecture (Flask, PostgreSQL, 16 services). NCR file covers MCP stack (5 layers), Layer 4 positioning, and tool surface. Different scope — back-fill needed. → `canary-mcp-stack-architecture.md` |
| agents | vsm.md | `growdirect-viewpoint-virtual-store-manager.md` | Covered | Brain has strategic/architectural synthesis. NCR adds operational detail (interaction model, MCP tool surface, L&G domain knowledge). Complementary — no back-fill required. |
| agents | roadmap.md | — | **Missing** | No Brain equivalent. NCR file has 4-phase batch-to-real-time progression (2026–2030) with tech stack per phase. → `canary-agent-roadmap-batch-to-realtime.md` |
| modules | index.md | — | Forward-only | L1–L4 hierarchy navigator with coverage key and module stubs. Navigation scaffolding only. |
| modules | D-distribution.md | `canary-module-d-functional-decomposition.md` | Covered | Brain functional decomposition is the source; NCR is the projection. |
| modules | W-work-execution.md | `canary-module-w-work-execution.md` | Covered | NCR is a 16-line stub; Brain has 295-line full spec. |
| modules | Q-loss-prevention.md | `canary-module-q-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | Q-loss-prevention-rule-catalog.md | `canary-module-q-counterpoint-rule-catalog.md` | Covered | Brain has full rule catalog with parameters and allow-lists. |
| modules | N-device.md | `canary-module-n-functional-decomposition.md` | Covered | Brain has functional decomposition. |
| modules | EJ-spine-and-sales-audit.md | `canary-ej-spine-and-sales-audit.md` | Covered | NCR is 13-line stub; Brain has 292-line full spec. |
| modules | F-finance.md | `canary-module-f-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | C-commercial.md | `canary-module-c-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | L-labor-workforce.md | `canary-module-l-labor-workforce.md` | Covered | NCR is 12-line stub; Brain has 295-line full spec. |
| modules | P-pricing-promotion.md | `canary-module-p-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | J-forecast-order.md | `canary-module-j-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | S-space-range-display.md | `canary-module-s-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | R-customer.md | `canary-module-r-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | T-transaction-pipeline.md | `canary-module-t-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| modules | A-asset-management.md | `canary-module-a-functional-decomposition.md` | Covered | Brain has full functional decomposition. |
| ncr-context | index.md | `ncr-counterpoint-phase-0-context-brief.md`, `voyix-counterpoint-rapid-pos-engagement-context.md`, `ncr-counterpoint-rapid-pos-relationship.md` | Covered | Three Brain articles back the NCR ecosystem context. |
| integration | index.md | `ncr-counterpoint-api-reference.md`, `ncr-counterpoint-endpoint-spine-map.md`, `ncr-counterpoint-connection-runbook.md`, `ncr-counterpoint-document-model.md` | Covered | Four Brain articles back the integration surface. |
| deployment | index.md | `engagement-shape-100-day-deployment.md` | Covered | Brain has project shape; NCR has module activation spec. Complementary, different audiences (PM vs engineer). |
| verticals | lawn-garden.md | `garden-center-operating-reality.md`, `socal-home-garden-target-customers-brief.md`, `bart-mccleskey-rapid-garden-pos.md`, `rapid-pos-counterpoint-market-research-tam.md`, `rapid-pos-counterpoint-user-pain-points.md` | Covered | Five Brain articles back the lead vertical. |
| verticals | armstrong.md | — | **Missing** | No Brain coverage. NCR has 85-line proof case (31 stores, ESOP, 136 years, ALX feature set). → `armstrong-garden-centers-proof-case.md` |
| verticals | feed-tack.md | — | Forward-only | Stub referencing L&G lead playbook. No substantive content. |
| verticals | beverage.md | — | Forward-only | Stub referencing L&G lead playbook. |
| verticals | gun.md | — | Forward-only | Stub referencing L&G lead playbook. |
| verticals | wine-spirits.md | — | Forward-only | Stub referencing L&G lead playbook. |
| sandbox | index.md | `ncr-counterpoint-sandbox-setup-checklist.md` | Covered | Brain has sandbox setup checklist. |
| why-canary | index.md | `canary-raas-positioning.md`, `canary-sales-strategy.md` | Covered | Brain articles back the positioning and co-sell story. |
| pitch | index.md | — | Forward-only | VAR leave-behind collection. Intentionally external, audience-specific. |
| root | canary-data-model.md | `canary-data-model.md` | Covered | NCR copy is an empty stub. Brain has the authoritative data model. |

## Summary Counts

| Outcome | Count |
|---|---|
| Covered | 25 |
| Forward-only | 7 |
| **Missing** | **3** |

## Back-fill Articles Required

1. `canary-mcp-stack-architecture.md` — MCP 5-layer stack, Layer 4 positioning, ALX tool surface
2. `canary-agent-roadmap-batch-to-realtime.md` — 4-phase progression from Counterpoint REST polling to autonomous ALX (2026–2030)
3. `armstrong-garden-centers-proof-case.md` — 31-store ESOP nursery, ALX feature set, strategic fit assessment

## Related

- [[Brain/projects/Canary|Canary MOC]]
- [[docs/superpowers/specs/2026-04-27-ncr-vault-framework-wiring-design|NCR Vault Wiring Spec]]
- [[Brain/wiki/canary-functional-decomp-gap-ledger|Canary Functional Decomp Gap Ledger]]

## Sources

- NCR vault: `~/GrowDirect-NCR/` (all sections audited 2026-04-27)
- Brain/wiki: full `canary-*`, `ncr-*`, `rapid-*`, `engagement-*`, `garden-*`, `socal-*`, `bart-*`, `voyix-*`, `growdirect-viewpoint-*` slug families checked
