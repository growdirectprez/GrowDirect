---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor Combined Session — B-066 + B-067-A: SDK Review, Coding Standards, and Capability Map
**Work Orders:** B-066 + B-067-A (combined for efficiency — same reading list)
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** 🔴 HIGH — gates Jeremy's next TSP session AND his B-067-B wiring pass
**Session type:** Review + Standards + Capability Map

---

## Why Combined

B-066 (SDK review + coding standards) and B-067-A (capability map) read the same sources: the Square SDK repos, Jeremy's LP coverage analysis, TSP PRDs, and B-065 output. Running them as separate sessions would duplicate 80% of the reading. One session, three deliverables, two gates cleared.

---

## Mission

You have three deliverables this session, in this order:

1. **Questions doc** (B-066 Phase 1) — surface every ambiguity before Jeremy builds
2. **Capability Map** (B-067-A) — the 16-family map that Jeremy and Qwen both read from
3. **Coding Standards** (B-066 Phase 2) — Jeremy's bible for all TSP/Square work

The capability map comes second because it feeds the standards doc — you need to know what Square offers before you can set rules for how Jeremy uses it.

---

## Context — What Changed Since These Were Written

**Sprint 6 code branch executed today (Feb 28).** The TSP pipeline is committed:
- Branch: `sprint-6-tsp` at `996562f` (33 files, 3,247 lines)
- Baseline: `sprint-5-baseline` tagged at `72d0082`
- Sandbox gate CLEARED: 26 real Square webhooks processed, all 200 OK
- HMAC verification passing against real Square signatures
- Valkey Streams publisher + consumer framework operational

This means your standards doc applies to **live production code**, not hypothetical architecture. Be concrete.

---

## Read First (in this order)

### B-065 Output — What Jeremy Built
```
/Users/geofflyle/GrowDirect/Canary/canary/services/square_webhook_manager.py
/Users/geofflyle/GrowDirect/Canary/canary/services/tsp/validators/square.py
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_SCAN_NOTES.md
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_ASSET_INDEX.txt
```

### Sprint 6 TSP Pipeline (new — committed today)
```
/Users/geofflyle/GrowDirect/Canary/canary/blueprints/webhooks_tsp.py
/Users/geofflyle/GrowDirect/Canary/canary/blueprints/receipt_tsp.py
/Users/geofflyle/GrowDirect/Canary/canary/services/evidence_chain.py
/Users/geofflyle/GrowDirect/Canary/canary/services/tsp/consumers/sub1_seal.py
/Users/geofflyle/GrowDirect/Canary/canary/services/tsp/consumers/sub3_merkle.py
/Users/geofflyle/GrowDirect/Canary/canary/services/tsp/merkle.py
/Users/geofflyle/GrowDirect/Canary/canary/services/tsp/stream_publisher.py
/Users/geofflyle/GrowDirect/Canary/canary/models/sales/evidence.py
/Users/geofflyle/GrowDirect/Canary/canary/models/sales/inscription.py
```

### Square SDK Repos
```
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/
/Users/geofflyle/GrowDirect/Canary/square/connect-api-examples/
/Users/geofflyle/GrowDirect/Canary/square/connect-api-specification/
/Users/geofflyle/GrowDirect/Canary/square/connect-python-sdk/  (deprecated — reference only)
```

### Critical SDK Files
```
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/src/square/utils/webhooks_helper.py
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/src/square/webhooks/subscriptions/client.py
/Users/geofflyle/GrowDirect/Canary/square/connect-api-examples/connect-examples/oauth/python/oauth-flow.py
```

### LP Coverage Analysis (the 14% finding)
```
/Users/geofflyle/GrowDirect/Canary_IP/Markdown/Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md
```

### TSP PRDs + Consolidated Review
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md
```

### Existing Canary Square Code (pre-B-065)
```
/Users/geofflyle/GrowDirect/Canary/square_client.py
/Users/geofflyle/GrowDirect/Canary/canary/services/square_service.py
/Users/geofflyle/GrowDirect/Canary/canary/services/square_oauth.py
/Users/geofflyle/GrowDirect/Canary/canary/services/parsers/square_payment_parser.py
/Users/geofflyle/GrowDirect/Canary/canary/services/parsers/square_order_parser.py
/Users/geofflyle/GrowDirect/Canary/canary/services/parsers/square_auxiliary_parsers.py
```

### v0 Square Schema Guide (optional — field-level detail)
```
/Users/geofflyle/GrowDirect/Canary_IP/Archive/growdirect-v0/canary-rd/square_comprehensive_dataset/COMPREHENSIVE_SQUARE_SCHEMA_GUIDE.md
```

---

## Deliverable 1: Questions Document (B-066 Phase 1)

**File:** `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/Condor_B066_Questions_v1.0.md`

Organize into four buckets:

### Bucket 1: Ring-Fencing Architecture
- Where does the Square SDK boundary sit?
- Existing parsers — Canary code or replace/wrap with Square samples?
- `square_client.py` at root — dead code? Superseded by TSP?
- `validators/square.py` manual HMAC vs SDK `verify_signature()` — which wins?

### Bucket 2: TSP Structure vs. What Square Actually Sends
- Does TSP-01 correctly model the full Square refund object?
- Which event types does Sub 2 handle Phase 1 vs Phase 2?
- Cash Drawer API poll-only (B-047) — does TSP have a polling adapter?
- Which PRDs need addenda before Jeremy builds Phase 2?

### Bucket 3: Speed-to-Market Risks
- OAuth token scope: which permissions are active? Do LP expansion scopes block Sprint 6?
- Old `Client` vs new `Square` class — any legacy patterns in our code?
- `connect-python-sdk` deprecated — any imports from it?
- SDK unpinned (`squareup`) — what happens when Square ships 45.x mid-sprint?

### Bucket 4: Coding Standards Gaps
- Error handling pattern for Square API calls
- Paginator handling in new SDK
- Field naming: Square names vs Canary normalized names
- Test data strategy: sandbox vs real event types

---

## Deliverable 2: Capability Map (B-067-A)

**File:** `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md`

For each of the 16 API families (14 core + Merchant + Locations), one block:

```
### [N]. [API Family Name]

SDK Namespace:            client.[namespace]
Sandbox Permission:       [OAuth scope]
Canary Phase:             [Phase 1 LIVE | Phase 2 | Phase 3 | Not planned]
TSP Component:            [TSP-01 through TSP-09, or N/A]
LP Signal:                [one sentence — what fraud/loss this catches]
Key Read Methods:         [3-5 actual SDK method names from v44]
Sample Call (Python):     [one line — real v44 syntax]
Dashboard Section Title:  [what Jeffe sees as the card header]
Fetch Button Label:       Fetch Live Data
Phase Badge:              [LIVE | PHASE 2 | PHASE 3]
explore_ function name:   [e.g. explore_payments]
```

Then a TSP coverage table:

| API Family | Sub 2 Parser | Sub 1 Seal | Sub 3 Inscribe | Status |
|---|---|---|---|---|
| Payments | parse_payment | hash + seal | ordinal | LIVE |
| Refunds | parse_refund | hash + seal | ordinal | LIVE |
| ... | ... | ... | ... | PLANNED / NOT STARTED |

**Rules:**
- Verify SDK method names against cloned repo — do not guess
- Use `from square import Square` / `client = Square(...)` v44 syntax only
- Phase 1 LIVE = Payments + Refunds + Webhooks (operational today)
- Phase 2 = Jeremy's LP analysis Tier 1 + Tier 2
- Phase 3 = everything else

---

## Deliverable 3: Coding Standards (B-066 Phase 2)

**File:** `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/Square_TSP_CodingStandards_v1.0.md`

Ten required sections:

1. **The Ring-Fence Rule** — where Square code ends and Canary code begins
2. **SDK-First Policy** — use SDK for everything it supports, manual only when it can't
3. **Event Type Handling Standard** — Sub 2 routing, templates for new handlers, unknown event policy
4. **Error Handling and Resilience** — retries, idempotency keys, rate limits, partial responses
5. **Pagination Standard** — paginator consumption, interruption handling, stream vs materialize
6. **Field Naming and Normalization** — Square names vs Canary names, normalization boundary
7. **OAuth Scope and Permission Standard** — scopes per phase, expansion process, graceful degradation
8. **Test Data Standard** — smoke test definition, sandbox events, replay protocol, test fixtures
9. **The Academic Exercise Results** — what Square provides vs what we've built, adopt/wrap/ignore verdicts
10. **PRD Addenda Required** — flags only (one-line each), ALX routes back for follow-up

---

## Standing Directives

- No external comms. Internal architecture review only.
- MVP scope is frozen. Standards must support the 27-feature MVP without adding scope.
- B-064 is the critical path. Standards must not gate the production heartbeat test.
- Data integrity is non-negotiable. Any standard that creates evidence chain ambiguity is wrong.
- B-063: SDK unpinned. Flag version risk explicitly.

---

## Session Close

Update HANDOFF.md:
- Questions doc location + which need Jeffe resolution vs Condor's call
- Capability map location + confirmation it covers all 16 families
- Standards doc location and version
- Any PRD addenda flagged — routes back to Condor follow-up

---

*ALX | February 28, 2026 | B-066 + B-067-A Combined*
*Gates: Jeremy next TSP session + Jeremy B-067-B wiring pass + Qwen B-067-C dashboard*
