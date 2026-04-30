---
title: Specs — NCR Counterpoint Retail Spine Integration
tags: [specs, counterpoint, integration, sdd]
nav_order: 50
audience: NCR Counterpoint VARs
last-updated: 2026-04-30
---

# Specs — NCR Counterpoint Retail Spine Integration

Architecture and integration depth for VAR principals and lead architects evaluating Canary against the NCR Counterpoint REST API surface. The specs below cover the master integration architecture, endpoint catalog, document data model, per-endpoint spine mapping, deployment runbook, and the OpenAPI 3.0 contract.

| Spec | What it covers |
|---|---|
| [Retail Spine Integration](retail-spine-integration) | The master SDD. Architecture, source-of-truth refs, auth, CRDM alignment, ARTS conformance, 13 module maps, cross-cutting concerns, phasing, risks, open questions. |
| [API Reference](api-reference) | Catalog overview — endpoint groupings, spine coverage summary by module letter. The map of which Counterpoint endpoints power which Canary capabilities. |
| [Document Model](document-model) | The Document/transaction model deep-dive — `PS_DOC_HDR`, line items, voids, returns, and `DOC_TYP` routing across modules. |
| [Endpoint × Spine Map](endpoint-spine-map) | Per-endpoint × CRDM × spine table — 97 rows in 12 grouped sub-tables, plus a four-section coverage gap report. The authoritative per-endpoint mapping. |
| [Connection Runbook](connection-runbook) | Windows-host stand-up — prerequisites, install, configure, smoke tests. Auth bootstrap (APIKey + `<company>.<user>` Basic). 401/403/404 disambiguation. |
| [OpenAPI Spec](openapi.yaml) | Derived OpenAPI 3.0 spec — 71 paths, 95 operations, 49 schemas. Counterpoint table prefixes preserved (`AR_CUST`, `IM_ITEM`, `PS_DOC_HDR`, `PS_STR`, `EC_*`, `SY_*`). |

## Source provenance

The Counterpoint REST API surface (95 documented endpoints across 71 paths, v2.4) was extracted from the public NCRCounterpointAPI/APIGuide repository, mapped against Canary's CRDM and 13-module spine, and turned into the architecture and integration specs above. Sample-derived schemas in the OpenAPI spec are tagged `x-source: sample-derived` for traceability.

## How to read these in order

1. Start with **Retail Spine Integration** for the architectural picture — what gets integrated, why, and how the modules fit together.
2. Use **API Reference** to see the endpoint catalog at module-letter granularity.
3. Drop into **Document Model** when you need to understand how Counterpoint's transaction omnibus actually behaves.
4. Use **Endpoint × Spine Map** for per-endpoint detail — the authoritative reference when scoping a specific adapter.
5. Use **Connection Runbook** when standing up an integration against a real Counterpoint instance.
6. Reference **OpenAPI Spec** as the working contract for adapter development — it's the machine-readable form of everything above.
