---
date: 2026-04-27
type: wiki
status: active
tags: [canary, roadmap, mcp, streaming, counterpoint, phases]
sources: [GrowDirect-NCR/agents/roadmap.md]
last-compiled: 2026-04-27
needs-review: 2026-05-11
method-role: Writer
method-stage: close
----


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

---

## Edge Agent Deployment Pattern (NCR Counterpoint)

The edge agent is a Go binary that runs on the retailer's existing Windows Server — the same machine running Counterpoint. No new hardware required. It connects directly to the Counterpoint SQL Server on the local network.

**Core components:**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Counterpoint adapter (Module T) | Go + direct SQL | Reads PS_DOC transaction stream from local Counterpoint DB |
| Local event store | SQLite (append-only) | Transaction queue — survives connectivity loss |
| Local embeddings | Ollama (qwen3-embedding:8b) | On-device vector search for Owl/risk context |
| NATS JetStream | LAN-local | Event bus between edge components |
| Sync daemon | Go | Batch push to cloud ALX when connectivity available, delta-only |
| Heartbeat emitter | Go | Signed node heartbeat every 3–5s; auto-Fox-case on silence >30s |

**Offline resilience contract:** The store must run without internet. SQLite buffers all events locally. The sync daemon handles reconnection and delta push. Cloud ALX receives events in order; gaps are detectable as sequence breaks, not silent data loss.

**Shadow mode discipline:** 7+ days parallel run before cutting LP alerts live. The cloud ALX validates the detection baseline against shadow data. No alert fires until shadow run quality is confirmed. This is the Digital Plumber discipline applied to edge deployment — prove it matches reality before it makes noise.

**Deployment target:** Existing store hardware. No new servers, no new network gear. The edge agent is a Docker container on the Windows Server already running Counterpoint.

---

## NCR Counterpoint Migration Path (Phase 0–4)

Five phases from first connection to full LP pipeline. Each phase has a clear entry criterion and a clear exit criterion. No phase starts until the previous phase's exit criterion is met.

| Phase | Name | Entry | Exit criterion |
|-------|------|-------|---------------|
| **0** | Discovery | Sandbox or test environment access confirmed | CPAPI validated, schema mapped, adapter builds against real endpoint |
| **1** | Shadow | Phase 0 complete, production access granted | 7+ day shadow run with no data integrity failures; baseline detection rate established |
| **2** | Sync | Phase 1 baseline confirmed | Cloud ALX receiving, pgvector memory bus seeded, Chirp rules calibrating against real data |
| **3** | Detection | Chirp calibration complete, false-positive rate at or below threshold | LP alerts live, Fox cases opening, cloud-store bidirectional confirmed |
| **4** | Retire | Phase 3 stable for 30+ days | Legacy polling/export workflows sunset; edge agent is sole data path |

**Phase 0 — Discovery:** Connect to sandbox or test Counterpoint environment. Validate CPAPI access (authentication, rate limits, endpoint availability). Map the PS_DOC transaction schema against the Canary Module T data model. Identify any VAR-specific schema extensions.

**Phase 1 — Shadow:** Edge agent reads live Counterpoint data with no writes and no alerts. Runs in parallel with the retailer's existing LP workflow. Cloud ALX receives the shadow stream and builds the detection baseline. Exit: 7+ days clean, baseline established.

**Phase 2 — Sync:** Cloud ALX receiving full stream. pgvector memory bus seeded with store history. Chirp detection rules running against live data — results visible in Canary dashboard but not yet surfaced to the retailer as alerts. Calibration period: rules tuned to the store's actual transaction patterns before going live.

**Phase 3 — Detection:** LP alerts live. Fox cases open automatically. Retailer LP team receives alerts via Module W work dispatch. Cloud-store bidirectional confirmed — store agent receives policy updates from cloud ALX, cloud ALX receives Fox case evidence from store.

**Phase 4 — Retire:** Legacy export/polling workflows shut down. The edge agent is the sole transaction data path. All historical data migrated to the Canary data model. The store is fully on Canary Go.

**last-compiled:** 2026-04-28
