---
type: project-moc
status: beta
tags: [canary, fraud-detection, saas]
---

# Canary

Merchant fraud detection and analytics platform. Square integration, MCP architecture, AI-powered detection rules.

## Status
Beta / Early Release Candidate

## Wiki Articles
- [[Brain/wiki/canary-platform-overview|Platform Overview]] — What Canary is, Square integration, modules, security, roadmap
- [[Brain/wiki/canary-architecture|Architecture Overview]] — 16 services, MCP layer, data flow, 3 schemas (`app` / `sales` / `metrics`)
- [[Brain/wiki/canary-detection|Detection Engine]] — 37 Chirp rules across 10 categories, 3 tiers, threshold system, alert pipeline
- [[Brain/wiki/canary-data-model|Data Model]] — 60+ models across `app`, `sales`, `metrics` schemas (Fox tables live in `app` despite the `models/fox/` module path)
- [[Brain/wiki/canary-sales-strategy|Sales Strategy]] — Gold list rules, adoption ladder, signal-over-noise philosophy
- [[Brain/wiki/canary-tsp-pipeline|TSP Pipeline]] — Webhook ingestion, 4 stream consumers, HMAC validation, hash chain, Merkle batching
- [[Brain/wiki/canary-chirp-rules|Chirp Rules]] — 37-rule catalog (10 categories), 3 evaluation tiers, threshold resolution, risk scoring, auto-casing
- [[Brain/wiki/canary-fox-case-management|Fox Case Management]] — Case lifecycle, evidence hash chain, append-only timeline, DB-enforced immutability

## Platform Concepts
- [[Brain/wiki/canary-closed-loop-cost-attribution|Closed Loop — Cycle Count as Accountability Clearing]] — The closed-loop model: cycle count as GC across physical, data, network, and compute layers; proportional charging; the full offender taxonomy. Grounds Rail 1 of the platform thesis.

## Module Overviews (post-rename)

Module-level overview cards. Pair with the L1–L4 functional decomposition cards below.

- [[Brain/wiki/canary-module-m-merchandising|Module M — Merchandising]]
- [[Brain/wiki/canary-module-e-execution|Module E — Execution]]
- [[Brain/wiki/canary-module-f-finance|Module F — Finance]]
- [[Brain/wiki/canary-module-l-labor|Module L — Labor]]

## Strategy & Operating Context

- [[Brain/wiki/canary-commercial-context|Commercial Context & Go Build Direction]] — RapidPOS / VAR channel strategy
- [[Brain/wiki/canary-location-item-data-model|Location & Item Data Model]] — canonical L+I model
- [[Brain/wiki/canary-vsm-diagnostic-mode-requirement|VSM Diagnostic Mode Requirement]] — Clarks-frame skill requirement
- [[Brain/wiki/canary-site-update-instructions|canary.growdirect.io — Site Update Instructions]] — content-ops runbook

## Sister Projects

- [[Brain/projects/NCR|NCR — Canary for NCR Counterpoint (VAR Partner Vault)]] — vendor-specific co-sell vault
- [[Brain/projects/CanaryRetailBrain|Canary Retail Brain]] — vendor-neutral product vault
- [[Brain/projects/CATz|CATz]] — method/co-sell vault

## Functional Decomposition (Retail Spine — Module-Level)

L1–L4 decomposition of the 13-module Retail Spine on the NCR Counterpoint / RapidPOS backbone. These are the canonical cross-reference cards for the NCR vault's `modules/` section.

- [[Brain/wiki/canary-module-a-functional-decomposition|Module A — Asset Management (Functional Decomp)]]
- [[Brain/wiki/canary-module-m-functional-decomposition|Module M — Merchandising (Functional Decomp)]]
- [[Brain/wiki/canary-module-d-functional-decomposition|Module D — Distribution (Functional Decomp)]]
- [[Brain/wiki/canary-module-f-functional-decomposition|Module F — Finance / Tenders / Tax (Functional Decomp)]]
- [[Brain/wiki/canary-module-o-functional-decomposition|Module O — Orders (Functional Decomp)]]
- [[Brain/wiki/canary-module-n-functional-decomposition|Module N — Device / Store Config (Functional Decomp)]]
- [[Brain/wiki/canary-module-p-functional-decomposition|Module P — Pricing & Promotion (Functional Decomp)]]
- [[Brain/wiki/canary-module-q-functional-decomposition|Module Q — Loss Prevention (Functional Decomp)]]
- [[Brain/wiki/canary-module-q-counterpoint-rule-catalog|Module Q — Counterpoint Rule Catalog]]
- [[Brain/wiki/canary-module-c-functional-decomposition|Module C — Customer (Functional Decomp)]]
- [[Brain/wiki/canary-module-s-functional-decomposition|Module S — Space (Functional Decomp)]]
- [[Brain/wiki/canary-module-t-functional-decomposition|Module T — Transaction Pipeline (Functional Decomp)]]
- [[Brain/wiki/canary-ej-spine-and-sales-audit|EJ Spine + Sales Audit]] — Canary-native naming for the perpetual layer

## User Guides
- [[Brain/wiki/canary-alerts-guide|Alerts Guide]] — Plain-English reference for all 37 rules, tuning dials, throttling controls, and the recommended onboarding sequence

## Architecture (Atlas)

### System Design
- [[Canary/docs/atlas/orchestration/fig-o01-service-mesh|Service Mesh]]
- [[Canary/docs/atlas/orchestration/fig-o02-mcp-tool-composition|MCP Tool Composition]]
- [[Canary/docs/atlas/orchestration/fig-o03-agent-handoff|Agent Handoff]]
- [[Canary/docs/atlas/infrastructure/fig-i01-docker-stack-topology|Docker Stack]]
- [[Canary/docs/atlas/infrastructure/fig-i02-database-schema-architecture|Database Schema]]
- [[Canary/docs/atlas/infrastructure/fig-i04-deploy-pipeline|Deploy Pipeline]]

### Data Pipelines
- [[Canary/docs/atlas/pipeline/fig-p00-tsp-orchestration|TSP Orchestration]]
- [[Canary/docs/atlas/pipeline/fig-p01-sub1-hash-seal|Hash Seal]]
- [[Canary/docs/atlas/pipeline/fig-p02-sub2-parse-route|Parse Route]]
- [[Canary/docs/atlas/pipeline/fig-p03-sub3-merkle-batcher|Merkle Batcher]]
- [[Canary/docs/atlas/pipeline/fig-p04-sub4-chirp-detection|Chirp Detection]]
- [[Canary/docs/atlas/pipeline/fig-p05-valkey-stream-topology|Valkey Streams]]

### Detection & Cases
- [[Canary/docs/atlas/decision/fig-d01-chirp-rule-evaluation|Chirp Rule Evaluation]]
- [[Canary/docs/atlas/decision/fig-d02-risk-score-classification|Risk Score Classification]]
- [[Canary/docs/atlas/decision/fig-d03-fox-case-escalation|Fox Case Escalation]]
- [[Canary/docs/atlas/decision/fig-d04-alert-severity-matrix|Alert Severity Matrix]]

### Lifecycles
- [[Canary/docs/atlas/lifecycle/fig-l01-transaction-lifecycle|Transaction Lifecycle]]
- [[Canary/docs/atlas/lifecycle/fig-l02-alert-lifecycle|Alert Lifecycle]]
- [[Canary/docs/atlas/lifecycle/fig-l03-case-lifecycle|Case Lifecycle]]
- [[Canary/docs/atlas/lifecycle/fig-l04-merchant-data-sync|Merchant Data Sync]]

### User Journeys
- [[Canary/docs/atlas/journey/fig-j01-merchant-end-to-end|Merchant End-to-End]]
- [[Canary/docs/atlas/journey/fig-j02-dashboard-info-architecture|Dashboard Info Architecture]]
- [[Canary/docs/atlas/journey/fig-j03-alert-investigation|Alert Investigation]]

### Protocol / Blockchain
- [[Canary/docs/atlas/protocol/fig-r01-raas-architecture|RaaS Architecture]]
- [[Canary/docs/atlas/protocol/fig-r02-ordinals-inscription-flow|Ordinals Inscription Flow]]
- [[Canary/docs/atlas/protocol/fig-r03-sidechain-hybrid-architecture|Sidechain Hybrid]]

## Team
- [[docs/team/ALX|ALX — COO / Chief of Staff]]
- [[docs/team/ProgramManager|Eva — Technical Ops]]
- [[docs/team/Architect|Tom — Architecture]]
- [[docs/team/Writer|Jess — Documentation]]
- [[docs/team/Engineer|Jeremy — DevOps]]
- [[docs/team/QA|Jim — Customer Sentiment]]
- [[docs/team/Owl|Owl — Product AI]]
- [[docs/team/UX|Art — UX/Creative]]

## Field Registry
- [[Canary/docs/field-registry|Field Registry Index]]
- [[Canary/docs/field-registry/extraction-sales-schema|Sales Schema]]
- [[Canary/docs/field-registry/extraction-detection-rules|Detection Rules]]
- [[Canary/docs/field-registry/extraction-app-fox-schema|Fox Schema]]
- [[Canary/docs/field-registry/square-coverage-matrix|Square Coverage Matrix]]

## System Design Documents (SDDs)

### Core
- [[docs/sdds/canary/platform-overview|Platform Overview]] — Product context, Square positioning, modules, roadmap, compliance
- [[docs/sdds/canary/architecture|Architecture]] — Platform overview, service mesh, deployment
- [[docs/sdds/canary/data-model|Data Model]] — 60+ models, PII map, cross-schema reference
- [[docs/sdds/canary/identity|Identity]] — JWT, sessions, RBAC
- [[docs/sdds/canary/identity-square|Identity-Square]] — Square OAuth, AES-256-GCM token storage
- [[docs/sdds/canary/external-identities|External Identities]] — Entity resolution, PII abstraction
- [[docs/sdds/canary/ops|Ops]] — Health checks, feature flags, config service
- [[docs/sdds/canary/ui-bff|UI/BFF]] — Frontend, session auth, feature flags

### TSP Pipeline
- [[docs/sdds/canary/tsp|TSP Pipeline]] — 10-step transaction pipeline, 4 stream consumers
- [[docs/sdds/canary/tsp-sub1|TSP Sub1 — Hash-Seal]] — Evidence hashing and sealing
- [[docs/sdds/canary/tsp-sub2|TSP Sub2 — Parse-Route]] — Transaction parsing and routing
- [[docs/sdds/canary/tsp-sub3|TSP Sub3 — Merkle]] — Merkle tree batching
- [[docs/sdds/canary/tsp-sub4|TSP Sub4 — Chirp]] — Detection rule execution
- [[docs/sdds/canary/webhook-pipeline|Webhook Pipeline]] — Square webhook ingestion, HMAC validation

### Detection & Cases
- [[docs/sdds/canary/chirp|Chirp Detection]] — 37 detection rules (10 categories), 3 tiers
- [[docs/sdds/canary/alert|Alerts]] — Alert lifecycle, notification routing
- [[docs/sdds/canary/fox|Fox Cases]] — Case management, evidence chain
- [[docs/sdds/canary/owl|Owl Analytics]] — AI analysis, Ollama, MCP server

### Analytics & Metrics
- [[docs/sdds/canary/analytics|Analytics]] — KPI dashboard, risk scoring
- [[docs/sdds/canary/metrics-analytics|Metrics]] — Star schema, ETL, risk snapshots
- [[docs/sdds/canary/metrics-risk-scoring|Risk Scoring]] — Employee risk scoring engine

### Protocol & Agent
- [[docs/sdds/canary/goose|Goose]] — Treasury/payment layer, Bitcoin/L402
- [[docs/sdds/canary/raas|RaaS]] — Namespace resolution, onboarding
- [[docs/sdds/canary/alx|ALX Agent]] — Knowledge store, pgvector
- [[docs/sdds/canary/qa-agent|QA Agent]] — QA orchestration, 30+ MCP tools
- [[docs/sdds/canary/multi-pos-architecture-proof|Multi-POS Proof]] — Multi-source adapter pattern

### NCR Counterpoint Integration
- [[docs/sdds/canary/canary-counterpoint-solution-guide|Solution Guide]] — Frame/People/Agents/Model/Blueprint across all 6 Phase 1 modules ← start here
- [[docs/sdds/canary/pos-adapter-substrate|POS Adapter Substrate]] — POSAdapter ABC, CanonicalEvent, Fixture, PollResult, adapter registry, pos_tenant_credentials
- [[docs/sdds/canary/ncr-counterpoint-auth-adapter|Module A — Auth]] — CounterpointBasicAuthFlow, HTTP client wrapper, credential lifecycle
- [[docs/sdds/canary/ncr-counterpoint-merchant-onboarding|Module O — Onboarding]] — Phase A→B→C activation orchestrator, wizard UI, vertical profile seeding
- [[docs/sdds/canary/ncr-counterpoint-store-station-adapter|Module S — Store & Station]] — cp_store_config, cp_station_config, walk-in sentinel, timezone lookup
- [[docs/sdds/canary/ncr-counterpoint-customer-adapter|Module C — Customer]] — AR_CUST → external_identities + cp_customer_profiles, PII strip
- [[docs/sdds/canary/ncr-counterpoint-item-catalog-adapter|Module I — Item Catalog]] — IM_ITEM → cp_item_catalog + cp_item_categories, Module Q margin substrates
- [[docs/sdds/canary/ncr-counterpoint-paycode-adapter|Module F — PayCode]] — PAY_TYP taxonomy, tender normalization, Q-TM/Q-DS substrates
- [[docs/sdds/canary/ncr-counterpoint-inventory-adapter|Module D — Inventory]] — cp_inventory_snapshots, Q-IS shrinkage substrates
- [[docs/sdds/canary/ncr-counterpoint-tsp-adapter|Module T — TSP (Documents)]] — PS_DOC pipeline, DOC_TYP routing, Sub2 compound dispatch
- [[docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring|Module Q — Chirp Wiring]] — C-1001+ rule scheme, garden-center allow-lists, dry-run deployment
- [[docs/sdds/canary/ncr-counterpoint-open-questions|Open Questions Register]] — 30+ questions triaged for Bart call / sandbox / deferred

### NCR Counterpoint — Brain Wiki
- [[Brain/wiki/ncr-counterpoint-api-reference|API Reference]] — Endpoint catalog, auth scheme, pagination, error codes
- [[Brain/wiki/ncr-counterpoint-document-model|Document Model]] — PS_DOC structure, DOC_TYP taxonomy, payment and line item fields
- [[Brain/wiki/ncr-counterpoint-endpoint-spine-map|Endpoint Spine Map]] — Entity-to-endpoint mapping across all modules
- [[Brain/wiki/ncr-counterpoint-connection-runbook|Connection Runbook]] — Server setup, API console, test steps
- [[Brain/wiki/ncr-counterpoint-sandbox-setup-checklist|Sandbox Setup Checklist]] — Pre-flight checklist before first API call
- [[Brain/wiki/ncr-counterpoint-phase-0-context-brief|Phase 0 Context Brief]] — Engagement background, Rapid POS relationship, go/no-go criteria
- [[Brain/wiki/ncr-counterpoint-rapid-pos-relationship|Rapid POS Relationship]] — VAR structure, Bart partnership context, whitelabel dynamics
- [[Brain/wiki/canary-module-q-counterpoint-rule-catalog|Module Q — Counterpoint Rule Catalog]] — Full C-1001+ rule catalog with garden-center vertical annotations

## Strategy
- [[Canary/docs/Canary-Blue-Ocean-Strategy-Analysis|Blue Ocean Strategy Analysis]]
- [[Brain/wiki/prototype-prep-master-dispatch|Prototype Prep Master Dispatch]] — pre-prototype session coordination
- [[Brain/wiki/socal-home-garden-target-customers-brief|SoCal Home & Garden Target Customers]] — sales brief for Rapid Garden POS channel
- [[Brain/wiki/video-integration-solution-pattern|Video Integration Solution Pattern]] — LP video evidence integration reference

## Prior-Art Lineage

Light references into the [[Brain/projects/Secure|Secure MOC]] for the pre-Secure / Secure-era retail-consulting IP that Canary's current design draws on. Primary home for these cards is the Secure MOC; this section is the Canary-side entry point so the forward project isn't orphaned from its heritage.

All referenced cards use deployment-archetype language per `feedback_scrub_client_names.md` — no named clients.

### Operating-model doctrine

- [[Brain/wiki/secure-retail-operating-model-2006|Retail Operating Model 2006]] — 8-domain Target Operating Model (UK global grocer, IBM 2006). Level-0/1/2 process decomposition, Dependencies + Key Decisions template. Precedent for Canary's Factory Pipeline SDD layering.
- [[Brain/wiki/secure-property-services-operating-model-2002|Property Services Operating Model 2002]] — earlier UK dept-store + grocery group operating model with RACI tables. RACI pattern informs Canary team responsibility mapping.

### Data / integration pattern precedents

- [[Brain/wiki/secure-merchandising-rfp-evant-response-2003|Merchandising RFP — Evant Response 2003]] — "centralized system of record repository for retail enterprise data" (Evant EIM) is the 2003 precursor to Canary's CRDM. Evant sold it as a million-dollar integration; Canary ships it as OAuth SaaS.
- [[Brain/wiki/secure-integrated-maps-2003|Integrated Maps 2003]] — retail-tech landscape map. Context for interpreting earlier engagement docs.
- [[Brain/wiki/secure-customer-order-management-flow-2017|Secure Customer Order Management Flow 2017]] — omnichannel order-fulfilment flow. Reference for Canary's future BOPIS / ship-from-store extensions.

### LP / EBR product lineage

- [[Brain/wiki/secure-sysrepublic-xbr-2016|xBR Replacement — Sysrepublic Response 2016]] — Foundation Objects / Lead Development / Case Management taxonomies directly map to Canary's tenant + Chirp + Fox architecture. "100 hours of consultancy" is the anti-pattern Canary's SaaS model rejects.
- [[Brain/wiki/secure-lpms-case-management-2015|Sporting-Goods Chain LPMS 2015]] — Action / Incident Type / Source-of-Info taxonomies. Direct reference for Canary's Fox module case taxonomies, Green/Yellow/Red shrink tier pattern, regional org cascade model.
- [[Brain/wiki/secure-5-inventory|Secure 5 Inventory]] — BOH/RTN/ADJ/RCT/EOH ledger model is the direct precursor to Canary's inventory module.
- [[Brain/wiki/secure-dsd-ired-analytics|DSD iRED Analytics]] — vendor-credit variance analysis at a US grocery chain. Cross-merchant benchmark pattern (industry-avg variant ratio) = the network-intelligence moat Canary is building.
- [[Brain/wiki/secure-eagle-eye-fnr-2018|Eagle Eye FR/NFR 2018]] — traceability-matrix requirements template. Pattern reference for future Canary PRDs / SDDs that need SDLC-grade traceability.

## Sprint Prompts
- [[Canary/devops/prompts/00_README|Prompt Library Index]]
- [[Canary/devops/prompts/sprint2/00_README_Sprint2|Sprint 2 Index]]

---

## Platform Architecture — Canary Go (Active Build)

**Status as of 2026-04-28:** Clean break from Python prototype. Go stack, GCP, ARTS-native, NCR Counterpoint-first. Python prototype frozen at `v0-python-prototype` tag. All active development is Canary Go.

- [[Brain/wiki/canary-go-portal|Canary Go Portal]] — project portal, SDD index, Linear links. Start here.
- [[Brain/wiki/cards/platform-thesis|Platform Thesis — Every Entity Has a Meter]] — three accountability rails (Operational / Financial / Evidentiary), meter model, SMB ICP positioning, the sentence
- [[docs/superpowers/specs/2026-04-28-canary-go-agent-pmo-architecture-design|Agent PMO Architecture]] — Controller + 27 domain PMO agents + infra agents; MCP connective tissue; SI gate

### Edge Architecture (2026-04-28)

- [[Brain/wiki/cards/edge-fabric-overview|Edge Fabric Overview]] — IoT heartbeat layer, MAP agents on LAN, NATS JetStream, Temporal mesh. Closes the closed graph at the physical device.
- [[Brain/wiki/cards/map-agent-l3|MAP Agent — L3 Domain Expert at the Edge]] — Go binary on store LAN; dual authority; self-metering; identical card format to cloud agents
- [[Brain/wiki/cards/heartbeat-protocol|Heartbeat Protocol]] — signed node heartbeat every 3–5s; auto Fox case on silence >30s
- [[Brain/wiki/cards/shelf-edge-demand-heartbeat|Shelf Edge Demand Heartbeat]] — Nano inference at shelf; demand signal IS the heartbeat; feeds Module S + J directly
- [[Brain/wiki/cards/temporal-retail-mesh|Temporal Retail Mesh]] — durable workflows at intersecting retail decision points; N+Q+W first
- [[Brain/wiki/cards/packet-cost-tracking|Packet Cost Tracking]] — atomic cost accounting at every event; eliminates shrink alibi
- [[Brain/wiki/cards/edge-fox-case|Edge Fox Case]] — LP lifecycle at physical speed; <500ms detection-to-case
- [[Brain/wiki/cards/agent-gitops-autonomy|Agent Gitops Autonomy]] — self-sustaining operational model; the agent that built it runs it

### Origin

- [[Brain/wiki/cards/fireball-demand-signal-origin|Fireball — Origin of the Demand Signal Architecture]] — PwC + Microsoft + M&S + P&G, 2001. The thesis Canary Go completes. Source: `Brain/raw/inbox/Heartbeat/`

### Hub-and-Spoke Agent Model

- [[Brain/wiki/ncr-counterpoint-rapid-pos-relationship|NCR Counterpoint / Rapid POS Relationship]] — includes hub-and-spoke LP org (store / regional / cloud ALX), VAR fleet deployment pattern
- [[Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context|Voyix / Counterpoint Engagement Context]] — includes store-as-mini-data-center, field org framing
- [[Brain/wiki/canary-agent-roadmap-batch-to-realtime|Agent Roadmap — Batch to Real-Time]] — includes edge agent deployment pattern, NCR migration path Phase 0–4

### Store Ops Capability Specs (Enterprise Intelligence Synthesis)

Source intelligence — enterprise WMS/planning reference:
- [[Brain/wiki/cards/rpas-planning-paradigm|RPAS Planning Paradigm]] — workbook model, spread methods, 4-tuple measure taxonomy, deferred calculation
- [[Brain/wiki/cards/rms-replenishment-screen-flows|RMS Replenishment Screen Flows]] — ORMS supplier SIM, 4 replenishment methods, PO status machine
- [[Brain/wiki/cards/rdm-wms-core-concepts|RDM WMS Core Concepts]] — container/LP model, 3-level location hierarchy, Foundation engine
- [[Brain/wiki/cards/rdm-inbound-and-receiving|RDM Inbound & Receiving]] — ASN, First Time SKU, QA/VA, opportunistic replenishment, putaway algorithms
- [[Brain/wiki/cards/rdm-picking-and-outbound|RDM Picking & Outbound]] — wave planning, 6 pick methods, order status machine, FIFO/FEFO
- [[Brain/wiki/cards/rdm-task-and-labor|RDM Task & Labor]] — task queue, directed work, RLM labor standards, Visibility Workbench

Application capability specs — Canary build reference:
- [[Brain/wiki/cards/store-ops-capability-model|Store Ops Capability Model]] — 7-layer synthesis, Android POS integration points, build priority
- [[Brain/wiki/cards/canary-purchase-order-lifecycle|Purchase Order Lifecycle]] — PO status machine, 3 order control modes, supplier minimums, COLT/NOLT
- [[Brain/wiki/cards/canary-mobile-task-ux-flows|Mobile Task UX Flows]] — receiving, replenishment, cycle count, new item onboarding — screen by screen
- [[Brain/wiki/cards/canary-demand-sensing-smb|Demand Sensing for SMB]] — velocity model, decay weighting, auto Min/Max derivation, 8 exception types
- [[Brain/wiki/cards/canary-supplier-profile-and-ordering|Supplier Profile & Ordering]] — 5-step setup wizard, delivery schedule, auto scorecard, lead time calibration
- [[Brain/wiki/cards/canary-space-range-display-on-floor|Space Range Display — On the Floor]] — live planogram, range status lifecycle, POS location lookup, 1-week feedback loop
- [[Brain/wiki/cards/canary-operations-hub|Operations Hub]] — morning briefing, exception queue, watch list, shift task dashboard
- [[Brain/wiki/cards/canary-android-pos-integration|Android POS Integration]] — NCR Counterpoint REST, event schemas, POS Bridge microservice, 5-step onboarding wizard
- [[Brain/wiki/cards/canary-labor-shift-management|Labor & Shift Management]] — shift model, activity group routing, time standards, productivity tracking, skip audit
- [[Brain/wiki/cards/canary-evidentiary-rail|Evidentiary Rail]] — 4-tier storage (S1/S2/S3/S4 chain), Bitcoin L2 anchor, satoshi-as-proof, privacy architecture
- [[Brain/wiki/cards/canary-multi-store-intelligence|Multi-Store Intelligence]] — portfolio hub, transfer orders, A/B planogram testing, network effect
- [[Brain/wiki/cards/canary-item-master-and-catalog|Item Master & Catalog]] — 3-level hierarchy, scan-to-lookup, e-catalog import, 5 dimension types

**last-compiled: 2026-05-04**
