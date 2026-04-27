---
date: 2026-04-27
type: wiki
tags: [canary, roadmap, mcp, streaming, counterpoint, phases]
sources: [GrowDirect-NCR/agents/roadmap.md]
last-compiled: 2026-04-27
needs-review: 2026-05-11
method-role: Writer
method-stage: close
---


**Wiki:** [[Brain/Home|Home]]

# Canary Agent Roadmap — Batch to Real-Time

## Summary

NCR Counterpoint is batch-first. MCP requires real-time. This roadmap defines four phases (2026–2030) that route around Counterpoint's batch architecture in Phase 1 and progressively replace the batch dependency until ALX operates on a live streaming pipeline independent of NCR's reconciliation cycle.

## Phase 1 — Wrap & Ship (2026)

**Goal:** Get ALX live. Prove the model.

Canary builds the MCP server on top of Counterpoint's existing REST API. Agent queries hit a Redis cache refreshed every 60–300 seconds — near-real-time at approximately 1–5 seconds. Payment via existing Worldpay/NCR integration. "Put it on my account" settles via Counterpoint customer account and stored payment method.

**Honest limitation:** Inventory is near-real-time, not live. Acceptable at this stage — better than any competitor has today.

**Stack:** MCP server (Python), Redis cache, Counterpoint REST API, Worldpay.

## Phase 2 — Event Triggers (2027)

**Goal:** Move from polling to push.

Webhook layer on top of Counterpoint — inventory update events trigger on sale, receive, and adjustment. Cache invalidated by events, not timers. Associate availability connected via store scheduling integration.

**Result:** Inventory accuracy from 60–300 seconds to near-instant on transaction events.

## Phase 3 — Streaming Pipeline (2027–2028)

**Goal:** True real-time layer independent of NCR's batch cycle.

Event streaming (Kafka or Kinesis) as a parallel data pipe. NCR transaction events tap directly into the stream. Store sensor data (RFID, computer vision) feeds in. ALX reads from the stream, not from the NCR API.

**Result:** ALX has live store state. NCR's batch cycle becomes irrelevant to the customer agent experience.

## Phase 4 — Autonomous ALX (2028–2030)

**Goal:** ALX learns the store and anticipates demand.

ALX develops a store-level demand model from streaming history. Predictive inventory signals push to customer agents before they ask. ALX initiates conversations: "Based on your last visit, this item is running low — want me to hold one?" Cross-store network: customer agent queries any enrolled store via a single MCP endpoint.

**Result:** Canary's back office hub becomes a demand prediction network. ALX is not reactive — it is proactive and personalised.

## Technology Stack by Phase

| Phase | Key technology |
|---|---|
| 1 | MCP server, Redis cache, Counterpoint REST API, Worldpay |
| 2 | Webhooks, event bus, scheduling system integration |
| 3 | Kafka/Kinesis, RFID/CV sensor tap, streaming MCP |
| 4 | ML demand model, proactive agent messaging, multi-store ALX network |

## Related

- [[Brain/wiki/canary-mcp-stack-architecture|MCP Stack Architecture]] — the five-layer stack and Layer 4 positioning
- [[Brain/wiki/growdirect-viewpoint-virtual-store-manager|VSM Viewpoint]] — strategic synthesis on the Virtual Store Manager
- [[Brain/wiki/ncr-counterpoint-api-reference|NCR Counterpoint API Reference]] — Phase 1 integration surface
- [[Brain/wiki/ncr-counterpoint-endpoint-spine-map|Endpoint Spine Map]] — Counterpoint REST endpoints backing the cache

## Sources

- NCR companion vault `agents/roadmap.md` (2026-04-27 back-fill from gap analysis)
