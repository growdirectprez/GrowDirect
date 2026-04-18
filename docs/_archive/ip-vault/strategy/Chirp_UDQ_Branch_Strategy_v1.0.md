---
type: strategy
domain: chirp
status: active
created: 2026-03-19
updated: 2026-03-19
---

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

# Chirp UDQ + Lightning Metering — Branch Strategy

**Version:** 1.1 (PaaS Extension)
**Date:** February 20, 2026
**Authors:** Eva (Program Manager), Jeremy (Developer Quant)
**Directive:** Jeffe — "I want to branch off from main and start working the Lightning BTCPay parts of the picture and merge them back into main after we do some primary research." + "Let's think PaaS. Retailers pay for full access to our API gateway, aggregation tables, and modeling power."
**PRD References:**
- `Documents/Product_Guides/Canary_PRD_E9_Chirp_UDQ_Lightning_Metering_v1.0.docx` (Base)
- `Documents/Product_Guides/Canary_PRD_E9_PaaS_API_Gateway_Data_Services_v1.0.docx` (PaaS Extension)

---

## Why a Branch?

This workstream touches three domains that are currently post-MVP (E4 Goose, E5 Owl, E6 Agentic) but Jeffe wants primary research started *now* — in parallel with the main Sprint 2/3 work. The branch strategy lets Jeremy and PhD explore without destabilizing the MVP build.

**The rule:** No modifications to existing modules (Chirp, Fox, auth, Square integration). All new code lives in `canary/udq/`, `canary/l402/`, `canary/llm/`, and `canary/api_gateway/`. New tables only — no existing table alterations.

**The PaaS expansion (Jeffe Feb 20):** On top of the UDQ + Lightning base, we're building the platform layer — a versioned API gateway, pre-computed aggregation tables, model inference endpoints, and tiered subscription billing. Three revenue layers: App (SaaS $49-199/mo), Query (Lightning micropayments 1-100 sats), Platform (API subscriptions 50K-200K sats/mo). The PaaS layer is where the network effects compound.

**Multi-channel business model (Jeffe Feb 20):** Square Marketplace is ONE distribution channel, not THE business. The platform enables three go-to-market motions off the same codebase:

| Channel | Buyer | Model | Margin |
|---------|-------|-------|--------|
| **Square Marketplace** | SMB store owner | Self-serve SaaS ($49-199/mo) | Volume |
| **Enterprise Direct License** | Big retailer LP/AP exec | Standalone wired solution, annual license | High |
| **Consulting + Implementation** | Any retailer | Jeffe + team builds/customizes on-site | Highest |

The consulting channel is the SysRepublic VP of Delivery playbook reborn — same sales motion (sell to AP/LP business, bypass IT), same value prop ("we'll do the rest"), same person delivering it. The PaaS API gateway is what makes the enterprise license channel possible without Square dependency.

---

## Branch Details

| Item | Value |
|------|-------|
| **Branch name** | `feature/chirp-udq-lightning` |
| **Created from** | `main` at current HEAD |
| **Rebase cadence** | Weekly (every Monday, after Sprint standup) |
| **Merge target** | `main` — after R3 gate clears |
| **CI requirement** | All 276 existing tests + new UDQ tests must pass |

---

## New Code Packages

```
canary/
├── udq/                    # NEW — User Defined Query module
│   ├── __init__.py
│   ├── routes.py           # Flask blueprint: /udq/*
│   ├── query_builder.py    # Query definition → SQL generator
│   ├── schema_metadata.py  # CRDM schema introspection for RAG
│   ├── query_executor.py   # Read-only query execution with RLS
│   └── templates/
│       └── udq/            # Query builder UI templates
├── l402/                   # NEW — Lightning micropayment gate
│   ├── __init__.py
│   ├── routes.py           # Flask blueprint: /l402/*
│   ├── btcpay_client.py    # BTCPay Server Greenfield API client
│   ├── invoice_manager.py  # Invoice creation, tracking, expiry
│   ├── macaroon.py         # L402 macaroon encode/decode
│   ├── complexity_scorer.py # Query → tier classification
│   └── payment_gate.py     # HTTP 402 middleware
├── llm/                    # NEW — Local LLM agent
│   ├── __init__.py
│   ├── agent.py            # Main agent loop (query → SQL → execute → synthesize)
│   ├── ollama_client.py    # ollama API client
│   ├── sql_validator.py    # SQL safety checker (read-only, row limits)
│   ├── evidence_builder.py # Builds citation references from query results
│   └── prompts/
│       ├── system.md       # System prompt with CRDM schema context
│       └── tools.md        # Tool definitions for SQL execution
├── api_gateway/            # NEW — PaaS API Gateway (E9-F5 through E9-F8)
│   ├── __init__.py
│   ├── routes.py           # Flask blueprint: /api/v1/*
│   ├── auth.py             # API key validation + HMAC signing
│   ├── rate_limiter.py     # Redis token bucket per API key
│   ├── usage_tracker.py    # Per-request logging to api_usage table
│   ├── aggregation_api.py  # /api/v1/aggregations/* endpoints
│   ├── model_api.py        # /api/v1/models/* endpoints (risk-score, anomaly-detect, etc.)
│   ├── benchmark_api.py    # /api/v1/benchmarks/* (anonymized cross-merchant)
│   ├── subscription_mgr.py # Tier management, provisioning, billing
│   └── openapi_spec.py     # Auto-generated OpenAPI 3.1 from routes
```

---

## New Docker Services (docker-compose.udq.yml)

```yaml
services:
  canary-llm:
    image: ollama/ollama:latest
    container_name: canary-llm
    volumes:
      - ollama_models:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        limits:
          memory: 8G
    networks:
      - canary-net

  btcpay-server:
    image: btcpayserver/btcpayserver:1.13
    container_name: canary-btcpay
    environment:
      BTCPAY_NETWORK: signet
      BTCPAY_ROOTPATH: /btcpay
    volumes:
      - btcpay_data:/datadir
    ports:
      - "14142:49392"
    networks:
      - canary-net
    depends_on:
      - btcpay-postgres

  btcpay-postgres:
    image: postgres:15
    container_name: canary-btcpay-db
    environment:
      POSTGRES_DB: btcpay
      POSTGRES_USER: btcpay
      POSTGRES_PASSWORD: ${BTCPAY_DB_PASSWORD}
    volumes:
      - btcpay_pgdata:/var/lib/postgresql/data
    networks:
      - canary-net
```

---

## Research Sprint Schedule

| Sprint | Dates | Focus | Jeremy | PhD | Gate |
|--------|-------|-------|--------|-----|------|
| **R1** | Feb 24 – Mar 3 | Query builder + LLM POC | UI prototype, ollama integration, NL→SQL pipeline | Model benchmarks, CRDM RAG prompt engineering | Demo: NL query → SQL → result |
| **R2** | Mar 3 – Mar 10 | BTCPay + L402 + API Gateway | BTCPay Docker, L402 middleware, API gateway scaffold, aggregation ETL pipeline | Pricing model (sat tiers), multi-step reasoning, k-anonymity benchmarks | Demo: metered deep-think query via API |
| **R3** | Mar 10 – Mar 17 | PaaS hardening + merge prep | Model API endpoints, subscription management, OpenAPI docs, test coverage, rebase | Prompt optimization, benchmark validation, quantization testing | MERGE GATE |

---

## Merge Gate Checklist

All items must be checked before merge to main:

- [ ] All 276 existing tests pass (zero regressions)
- [ ] New UDQ + PaaS test suite: 50+ tests covering 65 acceptance criteria
- [ ] E2E demo: NL query → L402 payment → LLM inference → result with evidence
- [ ] E2E demo: API key → aggregation query → usage metered → dashboard shows consumption
- [ ] Browser test: query builder UI flow in Playwright
- [ ] Browser test: developer portal (Swagger UI) renders with try-it-out
- [ ] Security: RLS tenant isolation verified via UDQ path AND API gateway
- [ ] Security: API key HMAC signing prevents replay attacks
- [ ] Performance: CPU-only inference < 30 seconds
- [ ] Performance: API gateway serves 1,000 req/min with < 200ms p95
- [ ] Performance: aggregation tables refresh within 15 minutes of source change
- [ ] Syd: L402 legal review complete (money transmitter assessment)
- [ ] Syd: AI regulation review (EU AI Act, state-level implications of model API)
- [ ] Tom: API design review sign-off
- [ ] Eva sign-off
- [ ] Jim QA sign-off
- [ ] Jeffe approval

---

## Team Routing

| Who | What | When |
|-----|------|------|
| **Jeremy** | Create branch, scaffold packages, query builder prototype, ollama integration | R1 Day 1 |
| **PhD** | Benchmark Llama 3.2 / Mistral / Phi-3 on CRDM SQL generation. Design pricing model. | R1 |
| **Tom** | Review all 7 new table schemas + 5 aggregation table schemas. Design API versioning strategy. | R1–R2 |
| **Jim** | Design test scenarios for UDQ features. Expand Rooster suite. | R1 Week 1 |
| **Eva** | Track R-sprint delivery. Manage rebase cadence. Enforce merge gate. | Continuous |
| **Syd** | L402 money transmitter legal analysis. Must complete before R3 merge. | R2 |
| **Jess** | Document new API endpoints, UDQ user guide, Lightning metering FAQ. | R3 |

---

## Relationship to Main MVP Sprints

This branch runs **in parallel** with the main build:

```
Main:    Sprint 2 (Feb 24–Mar 10) → Sprint 3 (Mar 10–14) → Sprint 4 (Mar 17–28)
Branch:  R1 (Feb 24–Mar 3) → R2 (Mar 3–10) → R3 (Mar 10–17) → MERGE → Sprint 4
```

**Key coordination point:** The branch merges back at the start of Sprint 4. By then, all Sprint 2/3 schema changes are in main, and the UDQ tables (which are additive-only) slot in cleanly.

---

*This is a working document. Updated as research sprints progress.*
