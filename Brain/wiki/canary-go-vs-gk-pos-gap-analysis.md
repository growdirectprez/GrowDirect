---
tags: [canary, go, architecture, gap-analysis, gk-pos, benchmark]
last-compiled: 2026-04-30
needs-review: 2026-06-01
related: [canary-go-portal, canary-go-endpoint-library, canary-architecture, canary-long-arc-atlas]
---

# Canary Go vs GK-POS — Gap Analysis

> **Governing thesis.** GK is a transactional engine. Canary is an intelligence layer that observes one. GK's two-axis API model — App Enablement for in-engine plug-ins, Service API for external REST — does not translate 1:1 to Canary, and the inversion is what makes the comparison useful. Canary's right-shape API surface has **three axes**, with a coverage profile that overlaps GK in some places (master data, identity, messaging) and is fundamentally orthogonal in others. The gap analysis is most useful as a **negative-space exercise**: knowing what Canary deliberately does *not* match GK on is as important as knowing what it should.

This article is the structural sense-check that scopes the [[canary-go-endpoint-library|Canary Endpoint Library]]. The endpoint library is the partner-facing canonical reference; this is the analysis that justifies its shape.

## Why GK is the right benchmark

GK Software (Fujitsu subsidiary as of May 2025) sits in the IDC MarketScape Leader category for POS Software Platforms. Customer roster: roughly a quarter of the world's Top 50 retailers, including Walmart International — which is the same Walmart-International data-modeling lineage that produced GSLM (see [[gslm-provenance|GSLM provenance]]). GK's CLOUD4RETAIL platform is what a fully realized enterprise POS API surface looks like. It is a useful reference precisely because it is *upmarket* — the gap between GK and Canary is a deliberate lane separation, not an aspirational ladder.

### What's public

| Surface | Access |
|---|---|
| [Omnibasket developer portal](https://omnibasket.com/) | Marketing pages public; Swagger/Postman/sandbox behind login |
| App Enablement v5.25 Functional Description (76pp) | [Public PDF](https://omnibasket.com/images/internal/GK_AppEnablement-525-FD_2025-01-15.pdf) — ingested at `Brain/raw/inbox/gk_appenablement-525-fd_2025-01-15-pdf.md` |
| App Enablement 2.0 spec | [Public PDF](https://omnibasket.com/images/internal/app_enablement_2_516.pdf) — ingested |
| Mobile SDK Selfscanning v6.9.7 | SAP Help PDF — ingested |
| SAP Omnichannel POS by GK ↔ SAP CAR integration | SAP Help PDF — ingested |

400+ REST endpoints in OmniPOS. No public GitHub presence. SAP CAR integration is the canonical outbound flow.

## GK's two axes

| Axis | Surface | Purpose |
|---|---|---|
| **App Enablement** | JS/TS plug-ins running *inside* the POS UI (iFrame + postMessage; pre-2.5 used a `jmc://` URL bridge); 9 namespaces under `comGkSoftwareGkrAppEnablementApi.*` | Third-party functionality embedded in the cashier flow |
| **Service API** | 400+ REST endpoints called *from outside* the POS; three top-level domains (Transactions, Engagement, Security) | External systems consume POS data and capabilities |

### The 9 App Enablement namespaces

| Namespace | What it does |
|---|---|
| `Common` | Session context (tenant, store, workstation, language, currency); event subscribe/unsubscribe |
| `Masterdata` | Internal item/customer master data |
| `ExternalMasterdata` | External master data lookups |
| `Pos` | Register line items (internal/external), customer, coupon; cancel transaction; transaction extensions; printout data — **the cash-register ops surface** |
| `Authorization` | User auth flows |
| `Fuel` | Forecourt integration (fuel/convenience customers) |
| `Function` (TS) | Generic function dispatch |
| `Messaging` (TS) | Pub/sub between embedded apps |
| `Scanner` (TS) | Barcode scanner integration |

Architecture inflection: pre-2.5 used `jmc://` URL-scheme bridge inside JxBrowser. From 2.5 onward, `postMessage`-based, normalized across Full POS Client, Thin Client, MobilePOS, and UltraThin POS (UltraThin uses STOMP/WebSocket to a FlowService backend).

## Canary's three axes

GK has two. Canary has three because it isn't a UI host *and* isn't a single-instance transactional engine *and* publishes to AI agents as a first-class consumer class.

| Canary axis | Surface | Direction | GK analogue |
|---|---|---|---|
| **A — Adapter Substrate** | Webhook receivers, polling clients, edge agents | POS → Canary (inbound) | **Inverse of App Enablement** — Canary runs adapters that pull from external POSes; GK runs plug-ins inside an external POS UI |
| **B — Resource APIs** | 32-service REST surface | Canary → external (outbound) | Direct analogue of **Service API** |
| **C — Agent Surface** | MCP tools, SSE streams, webhook publishers | Canary → AI agents (outbound, AI-native) | **No GK analogue** — Canary's AI-native differentiator |

GK has a fourth surface Canary does not, by design: **In-Canary App Enablement** — third-party plug-ins running inside Canary's own UI (Ops Dashboard, Store Brain). This is probably 18+ months out, possibly never. It is named here so the absence is by design, not by oversight.

## Gap by GK namespace

Walking GK's 9 App Enablement namespaces and mapping each to Canary:

| GK Namespace | Canary Equivalent | Status | Notes |
|---|---|---|---|
| `Common` (session, events) | `identity` (:8086) for session; Valkey pub/sub + SSE for events | **Comparable** | Different transport, equivalent purpose |
| `Masterdata` | `item` (:8090), `customer` (:8096) | **Comparable** | Canary will not duplicate POS-resident master data; the canonical record stays at the POS, Canary mirrors |
| `ExternalMasterdata` | `field-capture` (:9087) semantic registry | **Adjacent, not equivalent** | Canary's model is pgvector-backed schema mapping; GK's is direct external lookup |
| `Pos` (line items, transactions) | None | **N/A by design** | Canary doesn't *run* a register. Phase 4 of the [[canary-long-arc-atlas\|long arc]] adds this; Phases 1-3 deliberately do not |
| `Authorization` | `identity` (:8086) JWT + RBAC | **Comparable** | |
| `Fuel` | None | **Out of scope** | Fuel/convenience not on roadmap |
| `Function` (TS) | MCP tool registry (canary-compliance, canary-raas) | **Different model, comparable purpose** | MCP is more powerful for AI consumers — see Axis C |
| `Messaging` (TS) | Valkey pub/sub + SSE | **Comparable** | |
| `Scanner` (TS) | None | **Out of scope** | Edge concern, not Canary's layer |

**Summary:** 4 comparable, 1 adjacent, 1 different-model-comparable-purpose, 3 N/A-by-design or out-of-scope.

The **Pos namespace gap is the load-bearing one** — and it is the right gap. The day Canary has a Pos namespace is the day Phase 4 kicks in. Naming this absence as deliberate (not as a backlog item) is itself a documentation move that signals architectural intent.

## What Canary has that GK does not

| Canary Capability | GK Equivalent | Why this asymmetry exists |
|---|---|---|
| Chirp — 37-rule detection engine across 10 categories | None public | Loss prevention is observation-side, not transaction-side |
| Fox — append-only hash-chained evidence chain | None | Patent-protected evidentiary rail |
| Owl — pgvector search + Risk Dictionary + EJ Spine | None | Forensic intelligence layer; AI-native |
| Multi-POS adapter substrate | None — GK *is* the POS | Different lane: Canary is POS-agnostic; GK *is* the POS |
| `blockchain-anchor` — Bitcoin L2 hash anchoring | None | Patent-protected accountability rail |
| `l402-otb` — Bitcoin-gated open-to-buy | None | Patent-protected financial rail |
| `ildwac` — provenance-weighted cost model (patent #63/991,596) | None | Patent-protected costing model |
| `compliance` MCP — item × regulatory zone × ops blocks | None | Cross-cutting governance — GK leaves this to merchant systems |
| `store-brain` — presence resolution + AI session governance | None | AI-native context manager |
| `store-network-integrity` — cross-location anomaly detection | None | Multi-store correlation; GK is single-instance per checkout |

These are the moats. None of them need a GK equivalent because they *are* the differentiation. **For the endpoint library, these get equal billing with the resource APIs** — not relegated to a footnote labeled "platform extras."

## Canary current endpoint inventory

From [[microservice-architecture]]:

- ~61 documented endpoints across 11 of 32 services
- Covered: TSP, Chirp, Hawk, Fox, Owl, Bull, Identity, Alert, Analytics
- **21 of 32 services have zero documented endpoints** — this is the immediate gap

Undocumented services:

| Block | Services |
|---|---|
| Spine (8080-8099) | asset, item, inventory, receiving, transfer, pricing, employee, customer, returns, report, raas |
| Extended (9080-9091) | ecom-channel, inventory-as-a-service, ildwac, device-contracts, ops-dashboard, store-brain, blockchain-anchor, field-capture, store-network-integrity, commercial, l402-otb, compliance |

Filling these 21 service contracts is the build-out target. Each becomes its own dispatch.

## What this tells us about priorities

Three load-bearing observations:

1. **The 21 undocumented services are the immediate library gap.** They have port assignments, some have full SDDs, none have published endpoint contracts. Until they do, the [[canary-go-endpoint-library|Endpoint Library]] is half-built.
2. **The MCP surface (Axis C) is Canary's most novel axis and the one with no GK equivalent.** Agents-as-first-class-consumers is the AI-native differentiator. It earns its own canonical chapter, not a footnote.
3. **The Pos namespace gap is right.** Canary deliberately does not have line-item registration, basket calculation, or tender flow endpoints. That is Phase 4 of the long arc, not Phase 1 or 2. Naming this absence as deliberate is itself a documentation move that signals architectural intent to partners reading CRB.

## Useful comparisons across the lane

| Vendor | Surface | Plug-ins | SDK | Tier |
|---|---|---|---|---|
| **GK** | 400+ REST + JS plug-in framework + DSL workflow + partner ecosystem | Yes (App Enablement, 9 namespaces) | Yes (release-compatible) | Top-tier enterprise (Walmart Intl, Coop, Lidl, Aldi, Loblaw) |
| **NCR Counterpoint** | ~50 REST endpoints, no plug-in surface, no SDK | No | No | Mid-market specialty retail |
| **Square** | REST + webhooks, no in-POS plug-ins | Limited | Partial | SMB |
| **Canary Go (target)** | 32-service REST + MCP tool registry + adapter substrate | No (by design — Canary is not a UI host) | No (Canary is not a platform target) | SMB observer/intelligence layer over POS |

GK is what a fully realized enterprise POS platform looks like. Counterpoint by comparison is structurally a closed app with a thin REST veneer — which is exactly the gap Canary exploits at the SMB tier.

## Sources

- [GK OmniPOS](https://www.gk-software.com/us/solutions/gk-cloud4retail/gk-omnipos)
- [Omnibasket developer portal](https://omnibasket.com/)
- App Enablement v5.25 FD — `Brain/raw/inbox/gk_appenablement-525-fd_2025-01-15-pdf.md`
- App Enablement 2.0 spec — `Brain/raw/inbox/gk_appenablement-2-0_v516-pdf.md`
- Mobile SDK Selfscanning v6.9.7 — `Brain/raw/inbox/gk_mobile_sdk_selfscanning_v6-9-7-pdf.md`
- SAP Omnichannel POS by GK ↔ CAR integration — `Brain/raw/inbox/gk_sap_omnichannelpos_integration-pdf.md`
- [GK becomes Fujitsu company (2025-05)](https://www.gk-software.com/us/corporate-news-and-press-releases/en-press-release-20250527-fujitsu-gk)
- [[canary-go-portal]] · [[microservice-architecture]] · [[canary-long-arc-atlas]]
