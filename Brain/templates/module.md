---
date: <% tp.date.now("YYYY-MM-DD") %>
type: module
module-id: <X>
module-name: <Module Name>
ring: <v1|v2|v3|cross-cutting>
sdlc_stage: <concept|sdd|build|beta|shipping|frozen>
subsystem: <canary-go|cove|angel|memory-bus|factory|companion-vault>
owner: Alejandro
last-movement: <% tp.date.now("YYYY-MM-DD") %>
next-milestone: <YYYY-MM-DD or empty>
blocker: <one-line description or empty>
canonical-wiki: <[[canary-module-x-name]] or empty>
sdd: <docs/sdds/go-handoff/x.md or empty>
linear-tracker: <GRO-XXX or empty>
nfr_security: <none|drafted|implemented|hardened>
nfr_observability: <none|drafted|implemented|hardened>
nfr_performance: <none|drafted|implemented|hardened>
nfr_reliability: <none|drafted|implemented|hardened>
nfr_auditability: <none|drafted|implemented|hardened>
nfr_cost: <none|drafted|implemented|hardened>
last-compiled: <% tp.date.now("YYYY-MM-DD") %>
needs-review: <% tp.date.now("YYYY-MM-DD", 30) %>
tags: [module, tracker]
---

# <Module ID> — <Module Name>

One-paragraph governing thesis: what this module owns and why it exists in
the spine. Keep it tight — the long form lives in the canonical wiki article
linked above.

## Current status

- **SDLC stage:** <concept | sdd | build | beta | shipping | frozen>
- **Ring:** <v1 | v2 | v3 | cross-cutting>
- **Last movement:** <date — what shifted>
- **Next milestone:** <date — what unblocks the next stage>
- **Blocker:** <or "none">

## NFR posture

| NFR concern | State | Notes |
|---|---|---|
| Security | <none/drafted/implemented/hardened> |  |
| Observability | <…> |  |
| Performance | <…> |  |
| Reliability | <…> |  |
| Auditability (evidentiary) | <…> |  |
| Cost / efficiency | <…> |  |

NFR maturity scale: **none** = not considered · **drafted** = SDD covers it ·
**implemented** = code path exists · **hardened** = tested under failure
modes and instrumented for ops.

## Links

- **Canonical wiki:** <[[wiki article]]>
- **SDD:** <docs/sdds/...>
- **Linear:** <GRO-XXX>
- **Code:** <repo path>

## Recent activity
<!-- Auto-populated by `engine.py weekly` when this module appears in
     a week's commit log. Manually maintained otherwise. -->

