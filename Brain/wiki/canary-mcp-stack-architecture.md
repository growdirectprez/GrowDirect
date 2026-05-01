---
date: 2026-04-27
type: wiki
status: active
tags: [canary, architecture, mcp, counterpoint, layers]
sources: [GrowDirect-NCR/agents/architecture.md]
last-compiled: 2026-04-27
needs-review: 2026-05-11
method-role: Writer
method-stage: close
----


**Wiki:** [[Brain/Home|Home]]

# Canary MCP Stack Architecture

## Summary

Canary's delivery architecture on NCR Counterpoint is a five-layer stack. Canary owns Layer 4 — the MCP server (ALX/VSM) — the only layer in the retail stack that nobody else controls. NCR owns Layers 1–3 (store, hardware, POS software). The customer's Claude agent owns Layer 5. Layer 4 is the business.

## The Five Layers

```
┌─────────────────────────────────────────────┐
│  LAYER 5 — CUSTOMER                         │
│  Claude agent on phone / wearable           │
│  Knows: preferences, history, budget,       │
│  prior research, device ownership           │
└──────────────┬──────────────────────────────┘
               │  MCP protocol
               │  HTTPS + streaming (SSE)
               │  JSON-RPC 2.0
               ▼
┌─────────────────────────────────────────────┐ ◄── Canary owns this
│  LAYER 4 — ALX / VSM                        │
│  RapidPOS MCP Server (Canary-powered)       │
│  • Exposes MCP tools to customer agents     │
│  • Inventory, pricing, LP, diagnostics      │
│  • Payment / settlement trigger             │
│  • Associate deployment signal              │
│  • Back office hub connectivity             │
│  • Module A device heartbeat surface        │
└──────────────┬──────────────────────────────┘
               │  NCR REST API / ODBC
               │  (query-based, not event-driven)
               ▼
┌─────────────────────────────────────────────┐
│  LAYER 3 — NCR COUNTERPOINT                 │
│  POS Software Platform                      │
│  • Inventory (batch-reconciled)             │
│  • Customer / loyalty records               │
│  • Pricing engine + promotions              │
│  • Transaction processing                   │
│  • Document omnibus (all transaction types) │
└──────────────┬──────────────────────────────┘
               │  Store LAN
               ▼
┌─────────────────────────────────────────────┐
│  LAYER 2 — NCR HARDWARE                     │
│  POS terminals, self-checkout, mobile,      │
│  barcode / RFID / CV sensors, Edge node     │
└──────────────┬──────────────────────────────┘
               ▼
┌─────────────────────────────────────────────┐
│  LAYER 1 — THE STORE                        │
│  Products, associates, customers            │
└─────────────────────────────────────────────┘
```

## Why Layer 4 Is the Prize

NCR owns Layers 1–3. They cannot build Layer 4 — their batch architecture cannot deliver the millisecond responses MCP requires, and their payments-focused leadership is not oriented toward agent protocols.

The customer's Claude agent owns Layer 5.

Layer 4 — the MCP server — is the only layer nobody owns yet. Whoever establishes Layer 4 across the NCR VAR channel controls the agent interface for every retailer on Counterpoint.

## Hub and Spoke at Scale

Single-store deployment: ALX runs at Layer 4 for that store.

Multi-store deployment adds the back office hub:

- Aggregates Module Q alerts across all stores
- Monitors Module D transfer positions network-wide
- Reads Module A heartbeat on every device
- Surfaces Module O OTB status by store and category
- Connects upward to corporate if the org requires it

The back office hub adds no new infrastructure — it runs on the same Canary stack as the store agents.

## MCP Tool Surface (Layer 4)

| MCP tool | Counterpoint source | Response time target |
|---|---|---|
| `check_inventory` | `Inventory_ByLocation` | < 200ms |
| `get_pricing` | Price levels + promotions | < 200ms |
| `get_customer_account` | Customer / loyalty records | < 200ms |
| `find_in_store` | Zone / aisle config | < 100ms (cached) |
| `diagnose_plant` | Domain knowledge vault | < 300ms |
| `get_product_recommendation` | Diagnosis tree + inventory | < 300ms |
| `authorise_transaction` | Payment gateway | < 500ms |
| `log_visit` | Customer record update | async |

Counterpoint's batch architecture means some queries hit stale data (last-reconcile-cycle inventory). ALX handles this by caching recent Module T ingest — the last-known inventory state from the Canary perpetual ledger, not the Counterpoint snapshot. This is more accurate than Counterpoint's own reporting surface during high-velocity periods.

## Related

- [[Brain/wiki/canary-architecture|Canary Platform Architecture]] — internal platform architecture (Flask, PostgreSQL, services)
- [[Brain/wiki/growdirect-viewpoint-virtual-store-manager|VSM Viewpoint]] — strategic synthesis on the Virtual Store Manager concept
- [[Brain/wiki/canary-agent-roadmap-batch-to-realtime|Agent Roadmap: Batch to Real-Time]] — phased progression from polling to autonomous ALX
- [[Brain/wiki/ncr-counterpoint-api-reference|NCR Counterpoint API Reference]]

## Sources

- NCR companion vault `agents/architecture.md` (2026-04-27 back-fill from gap analysis)
