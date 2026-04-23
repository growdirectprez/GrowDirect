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
- [[Brain/wiki/canary-architecture|Architecture Overview]] — 16 services, MCP layer, data flow, 4 schemas
- [[Brain/wiki/canary-detection|Detection Engine]] — 37 Chirp rules across 10 categories, 3 tiers, threshold system, alert pipeline
- [[Brain/wiki/canary-data-model|Data Model]] — 60+ models across app, sales, fox, metrics schemas
- [[Brain/wiki/canary-sales-strategy|Sales Strategy]] — Gold list rules, adoption ladder, signal-over-noise philosophy
- [[Brain/wiki/canary-tsp-pipeline|TSP Pipeline]] — Webhook ingestion, 4 stream consumers, HMAC validation, hash chain, Merkle batching
- [[Brain/wiki/canary-chirp-rules|Chirp Rules]] — 37-rule catalog (10 categories), 3 evaluation tiers, threshold resolution, risk scoring, auto-casing
- [[Brain/wiki/canary-fox-case-management|Fox Case Management]] — Case lifecycle, evidence hash chain, append-only timeline, DB-enforced immutability

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

## Strategy
- [[Canary/docs/Canary-Blue-Ocean-Strategy-Analysis|Blue Ocean Strategy Analysis]]

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
