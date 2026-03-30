---
type: workorder
domain: tsp
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor Work Order — B-066: Square SDK Review + TSP Coding Standards
**Work Order:** B-066
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** 🟡 HIGH
**Session type:** Review + AskQuestions + Standards Doc
**Gates:** Jeremy's next TSP build session (B-064 live test → TSP Phase 2 Sprint 6)

---

## Mission

B-065 is done. Jeremy cloned the Square repos, completed OAuth smoke tests, and the stack is live. Before Jeremy writes another line of TSP code, you need to do three things:

1. **Scan** — read what Jeremy built in B-065 and what's in the Square repos
2. **Ask questions** — surface every ambiguity that would slow Jeremy down mid-build
3. **Produce standards** — write the coding standards doc Jeremy follows for all future TSP/Square work

The goal is maximum speed to market. Jeremy should never have to stop mid-session to decide *how* to do something. Your standards doc makes those decisions for him in advance.

---

## Context You Must Understand Before Starting

### What B-065 Produced (read all of these)

```
/Users/geofflyle/GrowDirect/Canary/canary/services/square_webhook_manager.py
/Users/geofflyle/GrowDirect/Canary/canary/services/tsp/validators/square.py
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_SCAN_NOTES.md
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_ASSET_INDEX.txt
```

### Key Square Repos Now on Disk

```
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/
/Users/geofflyle/GrowDirect/Canary/square/connect-api-examples/
/Users/geofflyle/GrowDirect/Canary/square/connect-api-specification/
/Users/geofflyle/GrowDirect/Canary/square/connect-python-sdk/  (deprecated — reference only)
```

### Critical Files in the Square SDK to Read

```
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/src/square/utils/webhooks_helper.py
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/src/square/webhooks/subscriptions/client.py
/Users/geofflyle/GrowDirect/Canary/square/connect-api-examples/connect-examples/oauth/python/oauth-flow.py
/Users/geofflyle/GrowDirect/Canary/square/connect-api-examples/connect-examples/v1/python/webhooks.py
```

### Jeremy's LP Coverage Analysis — READ THIS CAREFULLY

This document is from February 20. It maps every available Square API against the enterprise LP spec. It contains table schemas, Chirp rule recommendations, and a phased implementation roadmap that directly affects what TSP needs to handle.

```
/Users/geofflyle/GrowDirect/Canary_IP/Markdown/Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md
```

Key finding: **we ingest 2 of 14+ available Square data sources, covering ~14% of LP-relevant data.** The roadmap in Section 8 maps directly to TSP Phases 2-4. Your standards must account for this expansion.

### Existing Canary Square Code (pre-B-065)

```
/Users/geofflyle/GrowDirect/Canary/square_client.py           ← root-level, pre-TSP
/Users/geofflyle/GrowDirect/Canary/canary/services/square_service.py
/Users/geofflyle/GrowDirect/Canary/canary/services/square_oauth.py
/Users/geofflyle/GrowDirect/Canary/canary/services/parsers/square_payment_parser.py
/Users/geofflyle/GrowDirect/Canary/canary/services/parsers/square_order_parser.py
/Users/geofflyle/GrowDirect/Canary/canary/services/parsers/square_auxiliary_parsers.py
/Users/geofflyle/GrowDirect/Canary/canary/blueprints/square_oauth.py
/Users/geofflyle/GrowDirect/Canary/canary/blueprints/square_oauth_wired.py
```

### TSP PRDs (the specs Jeremy builds from)

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md
```

Focus on TSP-01 (Webhook Receipt), TSP-02 (Sub 2 Parser/Router), and the Consolidated Review. These define the current heartbeat pipeline. Your standards must extend them, not contradict them.

### Also Relevant

```
/Users/geofflyle/GrowDirect/Canary_IP/Archive/growdirect-v0/canary-rd/square_comprehensive_dataset/COMPREHENSIVE_SQUARE_SCHEMA_GUIDE.md
```

This is the v0 Square schema guide from the original prototype. May contain field-level detail not in Jeremy's LP analysis. Worth a scan.

---

## Phase 1 — AskQuestions (produce BEFORE the standards doc)

After reading the above, surface your questions and observations as a structured document. Don't hold anything back. These questions go to Jeffe and ALX for resolution before Jeremy builds.

Organize your questions into these buckets:

### Bucket 1: Ring-Fencing Architecture
The directive: use Square sample code as-is, clearly marked, as an academic exercise first — before committing to an architectural pattern. Questions to answer:
- Where does the Square SDK boundary sit? (What does Canary own vs. what does Square own?)
- The existing parsers (`square_payment_parser.py`, `square_order_parser.py`) — are these Canary code or should they be replaced/wrapped by Square samples?
- `square_client.py` at root level — dead code? Superseded by TSP? Or still in play?
- `validators/square.py` uses manual HMAC. `square-python-sdk` has `verify_signature()`. Which wins and why?

### Bucket 2: TSP Structure vs. What Square Actually Sends
Cross-reference the TSP PRDs against the Square SDK and LP coverage analysis:
- TSP-01 handles `refund.created` as the heartbeat event. Does the PRD correctly model the full Square refund object? Any fields in the SDK that TSP-01 doesn't account for?
- TSP-02 Sub 2 routes by event type. Jeremy's LP analysis shows 14+ data sources. Which event types does Sub 2 need to handle in Phase 1 vs. Phase 2? Is the current routing table in TSP-02 accurate and complete for heartbeat?
- Cash Drawer API is poll-only (B-047 standing blocker). Does TSP have a polling adapter design? If not, flag it.
- The LP analysis says we're at ~14% data coverage. The TSP PRDs were written at a point in time. Which PRDs need an addendum before Jeremy builds Phase 2?

### Bucket 3: Speed-to-Market Risks
Where could Jeremy lose a day mid-session because something wasn't decided?
- OAuth token scope: which permissions are active on the sandbox token? Does the LP expansion (cash drawer, timecards, inventory) require new OAuth scope requests that block Sprint 6?
- The `oauth-flow.py` sample uses the old `Client` class. The current SDK uses `Square`. Is there any place in our code still using the old pattern that will break?
- `connect-python-sdk` is deprecated. Any of our current code importing from it?
- SDK version: confirmed at 44.0.1.20260122 in Docker. But `requirements.txt` is unpinned (`squareup`). What happens when Square ships 45.x mid-sprint?

### Bucket 4: Coding Standards Gaps
What decisions has the team NOT made that Jeremy will have to make on the fly?
- Error handling pattern for Square API calls (retry logic, rate limits, idempotency keys)
- How to handle Square's paginators in the new SDK (the `.list()` methods return iterables)
- Naming conventions for Square-sourced fields vs. Canary-normalized fields
- Where does Square sample code live vs. Canary TSP code? (the ring-fencing question)
- Test data strategy: sandbox event types vs. real event types — what's the standard for smoke tests?

---

## Phase 2 — Coding Standards Document

After questions are answered (or flagged as needing Jeffe resolution), produce:

**File:** `/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/Square_TSP_CodingStandards_v1.0.md`

### Required Sections

**1. The Ring-Fence Rule**
Define exactly where Square code ends and Canary code begins. Use the "clearly marked" approach Jeffe specified. Every file, function, or pattern that comes directly from Square sample code must be identified as such. Propose a concrete convention (header comment, directory convention, or both). Be specific enough that Jeremy can apply it without asking.

**2. SDK-First Policy**
Square has a Python SDK with typed responses, built-in retries, webhook verification helpers, and pagination. The standard: use the SDK for everything it supports. Manual implementation only when the SDK demonstrably can't do it. Cite specific SDK methods where relevant. Document the one known exception: `validators/square.py` manual HMAC (and whether to keep it or migrate to `verify_signature()`).

**3. Event Type Handling Standard**
How Jeremy handles each event type in Sub 2. Template for adding a new event type handler. What happens to unknown/unsupported event types (drop with log, pass through, DLQ). How to add a new data source (e.g., cash drawer polling) without breaking the existing pipeline.

**4. Error Handling and Resilience**
Square API error classes, retry behavior, idempotency key standard (when and how). Rate limit handling. What to do when Square returns a partial response. How to surface errors to TSP without losing the event.

**5. Pagination Standard**
The new SDK returns paginators, not raw lists. Standard for consuming them. How to handle interruption mid-page. Whether to materialize fully or stream.

**6. Field Naming and Normalization**
Square uses `snake_case` but with Square-specific names (`team_member_id` vs. `employee_id`, `amount_money.amount` in cents vs. our `amount_cents`). Define the normalization boundary: where Square field names live vs. where Canary normalized names take over. This is critical for the parsers.

**7. OAuth Scope and Permission Standard**
Which scopes are needed for each TSP phase. How to request scope expansion. What to do when a scope isn't granted (graceful degradation, not crash). Flag the permissions needed for Jeremy's LP analysis Phase 2 expansion.

**8. Test Data Standard**
What constitutes a passing smoke test for a Square integration. Which Square sandbox event types to use. How to replay a webhook for testing. What the standard test fixture looks like for a `refund.created` event (the heartbeat event).

**9. The Academic Exercise Results**
This section is the output of your ring-fence academic exercise. You took Square's base code as-is and compared it to what we have. Document:
- What Square provides that we've re-implemented (and whether to switch)
- What Square provides that we haven't used yet
- What we've built that has no Square equivalent (our value-add layer)
- Verdict: which Square patterns should Jeremy adopt directly vs. wrap vs. ignore

**10. PRD Addenda Required**
List any TSP PRDs that need a formal addendum based on this review. Don't write the addenda here — just flag them with a one-line description of what changed and why. ALX routes these back to Condor for a follow-up session.

---

## Deliverables

| File | Purpose |
|---|---|
| `Condor_B066_Questions_v1.0.md` | Phase 1 questions — routes to Jeffe/ALX for resolution |
| `Square_TSP_CodingStandards_v1.0.md` | Phase 2 standards doc — Jeremy's bible for all TSP Square work |

Both files go to:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/
```

---

## Standing Directives

- No external comms. This is internal architecture review only.
- MVP scope is frozen. Standards must support the 27-feature MVP without adding scope.
- B-064 is still the critical path: Jeffe's phone triggers a live `refund.created`. Your standards must not gate this test.
- Data integrity is non-negotiable. Any standard that creates ambiguity in the evidence chain is wrong.
- B-063: SDK unpinned. Any standard that touches `requirements.txt` must flag the version risk.

---

## Session Close

Update HANDOFF.md:
- Questions document location and which questions need Jeffe resolution vs. which are Condor's call
- Standards doc location and version
- Any PRD addenda flagged — routes back to Condor for follow-up

---

*ALX | February 28, 2026 | B-066*
*Jeffe directive: ring-fence Square base code, clearly marked, academic exercise first.*
*Feeds: Jeremy next TSP build session | B-035 (Tom: schema alignment) | B-036 (Jeremy: CRDM alignment)*
