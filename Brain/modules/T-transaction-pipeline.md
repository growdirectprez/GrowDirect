---
date: 2026-05-03
type: module
module-id: T
module-name: Transaction Pipeline
ring: v1
sdlc_stage: shipping
subsystem: canary-go
owner: Alejandro
last-movement: 2026-04-30
next-milestone: ""
blocker: ""
canonical-wiki: "[[canary-module-t-transactions]]"
sdd: docs/sdds/go-handoff/tsp.md
linear-tracker: ""
nfr_security: implemented
nfr_observability: implemented
nfr_performance: implemented
nfr_reliability: drafted
nfr_auditability: hardened
nfr_cost: drafted
last-compiled: 2026-05-03
needs-review: 2026-06-02
tags: [module, tracker, canary-go, v1, spine]
---

# T — Transaction Pipeline

Publisher of the sale event into the Canary stock ledger. Sits at the head
of the spine — every other v1 module subscribes to or reconciles against
T's stream. The shipping member of the Differentiated-Five.

## Current status

- **SDLC stage:** shipping
- **Ring:** v1
- **Last movement:** 2026-04-30 — chirp rule count corrected to 37 across wiki
- **Next milestone:** none current — module is production
- **Blocker:** none

## NFR posture

| NFR concern | State | Notes |
|---|---|---|
| Security | implemented | Auth/AuthZ wired, secrets from env |
| Observability | implemented | Structured logs + metrics emitted to ops dashboard |
| Performance | implemented | Within SLO at current Square merchant volume |
| Reliability | drafted | Failure-mode runbooks in progress |
| Auditability (evidentiary) | hardened | TSP merkle anchoring proves immutability of the sale event stream |
| Cost / efficiency | drafted | Cost-per-event not instrumented yet |

NFR maturity scale: **none** = not considered · **drafted** = SDD covers it ·
**implemented** = code path exists · **hardened** = tested under failure
modes and instrumented for ops.

## Links

- **Canonical wiki:** [[canary-module-t-transactions]]
- **SDD:** [tsp.md](../../docs/sdds/go-handoff/tsp.md), [tsp-merkle.md](../../docs/sdds/go-handoff/tsp-merkle.md)
- **Linear:** GRO-117 (related — Goose satoshi-cost)
- **Code:** `CanaryGo/internal/tsp/`

## Recent activity

- 2026-04-30 — Documentation drift cleared: chirp rule count corrected to 37 across 6 wiki articles (RetailSpine v0.6 pass).
- 2026-04-24 — RetailSpine v0.6 confirmed T as shipping member of Differentiated-Five.
