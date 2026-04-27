---
date: 2026-04-10
type: wiki
tags: [canary, architecture, mcp, services]
sources: [Canary/docs/atlas/INDEX.md, Canary/canary/services/, Canary/canary/blueprints/]
last-compiled: 2026-04-10
needs-review: 2026-05-26
---

# Canary Architecture

## Summary

Canary is a loss prevention analytics platform for Square merchants built on Flask 3, PostgreSQL 17, and Valkey 8. It uses a service-oriented architecture with 16 canonical services composed through an MCP (Model Context Protocol) layer, a four-stage ingestion pipeline (TSP), and a three-tier detection engine (Chirp). The system processes Square webhook events in real time and produces alerts, cases, and risk analytics.

## System Design

The architecture has four layers, each with distinct responsibilities:

**Ingestion Layer** — TSP (Triple Subscriber Pipeline), Parsers (18 Square entity parsers), and Onboarding (OAuth flow, initial sync, baseline establishment). Square webhooks arrive HMAC-signed, get validated at the TSP gateway, and are published to Valkey Streams. Three independent consumer groups (Sub 1: hash & seal, Sub 2: parse & route, Sub 3: merkle batcher) read from `canary:events` without coordinating. Sub 2's output feeds a detection stream consumed by Sub 4 (Chirp evaluation).

**Detection Layer** — Chirp (rule engine with 37 rules across 3 tiers), Alerts (lifecycle management with impact scoring), and Metrics (dimension loading and ETL). Chirp evaluates every parsed transaction against its rule catalog and produces alert dicts that flow into the alert lifecycle.

**Intelligence Layer** — Owl (retail intelligence engine), Fox (case management and evidence collection), Vault (merchant memory locker), and Condor (external intelligence gateway). Fox escalates clusters of related alerts into cases. Owl synthesizes merchant-level intelligence. Vault stores per-merchant configuration, history, and risk profiles.

**Infrastructure** — Identity (auth, RBAC, sessions), Health Check (liveness and readiness), Analytics (dashboard queries and chart generation), BFF (browser frontend aggregator), Atlas (architecture diagram browser), and RaaS (Bitcoin ordinals anchoring for forensic immutability).

## The 16 Services

Each service exposes an MCPRegistry with typed tools, meaning Claude agents can interact with any service programmatically. The services are: TSP, Parsers, Onboarding, Chirp, Alerts, Metrics, Owl, Fox, Vault, Condor, Identity, Health Check, Analytics, BFF, Atlas, and RaaS.

MCP blueprints live in `Canary/canary/blueprints/` with the naming convention `<service>_mcp.py`. Traditional HTML routes use `<service>_wired.py`. This dual-interface pattern means every service is accessible both from the browser dashboard and from AI agents.

## Data Flow

The end-to-end flow for a single Square event:

1. Square sends an HMAC-SHA256 signed webhook to the TSP gateway
2. TSP validates the signature, computes an event hash, and publishes to `canary:events` (Valkey Stream)
3. Sub 1 (hash & seal) recomputes the hash, chains it to the previous event, and writes an immutable evidence record
4. Sub 2 (parse & route) dispatches to one of 18 domain parsers, writes the structured data to the CRDM (canonical relational data model) in the `sales` schema
5. Sub 3 (merkle batcher) accumulates events into Merkle trees for periodic Bitcoin ordinals inscription
6. Sub 4 (chirp detection) evaluates the parsed transaction against all active rules, producing alerts for any violations
7. Alerts enter the alert lifecycle (created → acknowledged → escalated → resolved)
8. Fox monitors alert clusters and escalates them into cases when patterns emerge
9. Owl synthesizes merchant-level intelligence from cases, alerts, and metrics
10. The BFF serves dashboard views to the merchant browser client

## Database Architecture

Four PostgreSQL schemas in the `canary` database:

- **app** — Core entities: merchants, users, locations, employees, OAuth tokens, feature flags, notifications, subscriptions. 20+ models.
- **sales** — Square CRDM: transactions, tenders, line items, orders, timecards, cash drawers, gift cards, loyalty, inventory, invoices, payouts, disputes. The canonical representation of everything Square sends.
- **fox** — Case management: cases, evidence records, subjects. Links back to alerts and sales entities.
- **metrics** — Analytics: dimension tables (merchant, location, employee, time), fact tables (period metrics, risk scores). Powers the dashboard.

All models use UUID primary keys, `created_at`/`updated_at` timestamps, and SQLAlchemy 2.0 `Mapped[]` annotations.

## Atlas

The architecture is documented in 52 Mermaid diagrams organized into 8 categories: Legacy (14 research-era figures), Orchestration (5 service composition diagrams), Lifecycle (5 entity state machines), Pipeline (6+ TSP internals), Decision (4 Chirp rule evaluation flows), Infrastructure (4 Docker/deploy diagrams), Journey (3 user experience flows), and Protocol (3 Bitcoin anchoring diagrams). The atlas browser service renders these in the dashboard at `/atlas/`.

## Related

- [[Brain/wiki/canary-detection|Canary Detection Engine]] — Deep dive on Chirp rules, tiers, and alert pipeline
- [[Brain/wiki/canary-data-model|Canary Data Model]] — Schema details, key entities, and relationships
- [[Brain/projects/Canary|Canary MOC]] — Project hub with links to all atlas diagrams and team profiles

## Sources

- `Canary/docs/atlas/INDEX.md` — Full figure index (52 diagrams)
- `Canary/docs/atlas/orchestration/fig-o01-service-mesh.md` — Service mesh diagram
- `Canary/docs/atlas/pipeline/fig-p00-tsp-orchestration.md` — TSP pipeline overview
- `Canary/canary/services/` — All 16 service implementations
- `Canary/canary/blueprints/` — MCP and wired route registrations
- `Canary/canary/config.py` — Environment configuration
