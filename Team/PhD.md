---
type: research
classification: confidential
owner: GrowDirect LLC
date: 2026-04-27
tags: [canary, edge-architecture, ncr, counterpoint, alx, distributed-systems, strategy]
---

# Canary Distributed Edge Architecture — Research Synthesis

**Governing thesis:** The retail store is not a point-of-sale terminal connected to the cloud. It is a mini data center that must operate independently, with cloud connectivity as a performance enhancer — not a dependency. Canary's architecture is built on this constraint. Every design decision follows from it.

---

## Executive Summary

This document synthesizes the architectural reasoning, historical precedent, deployment strategy, and AI model decisions for the Canary distributed edge platform. It is written for two audiences simultaneously: the engineer who needs to understand why decisions were made (the PhD layer), and the operator or partner who needs to understand what it means and what to do next (the MD layer).

**The architecture in one paragraph:** A Canary Edge Agent runs inside each retail store on the local network — on the same server as NCR Counterpoint or on a co-located device. It polls the Counterpoint REST API locally, evaluates loss prevention rules in real time without cloud dependency, and buffers events for async sync to Canary Cloud. The cloud is the hub: it receives events from all stores, runs cross-store intelligence, manages the rule catalog, and hosts the cloud ALX agent. Store agents and the cloud agent form a hub-and-spoke structure that maps directly to how a traditional retail LP field organization is structured. Rapid POS is the distribution channel — they install the edge agent alongside Counterpoint at every customer site.

**The decisions already made:**
- Do not fine-tune any model. The "ALX knows your operation" story is retrieval (pgvector memory bus) + Claude Sonnet reasoning, not fine-tuning.
- Cloud inference runs on AWS Bedrock (Claude Sonnet). Enterprise procurement posture, NCR-legible.
- Edge inference is deterministic Chirp rules + Ollama embeddings. No LLM at the edge.
- V1 ingestion: API Gateway + REST polling (simple, proven). IoT Core/MQTT is Phase 2.
- V1 hardware: dedicated mini PC (Beelink N100, ~$180, Linux-native) or Counterpoint server with resource-capped Docker container.
- Rapid POS is the install channel. Every Counterpoint install they've ever done is a potential edge node.

**The next move:** Get Module T pointing at Bart's Counterpoint sandbox this week. The pilot IS the diagnostic IS the demo.

---

## I. Historical Precedent — The Secure-Era Architecture

The architecture being built is not new. This is important to understand, because it means the architecture is validated — not theoretical.

The Secure-era xBR (Exception Based Reporting) deployments of 2015–2018 operated on exactly this model: a server in the back office running the POS and local LP detection, a head office aggregating data across the estate, LP analysts working the central view. The Sysrepublic xBR system — which GrowDirect's prior-art lineage documents in detail — was the industry standard for this pattern. It worked. It caught shrink. The reason it never reached SMB retailers was the cost and complexity of deployment: six-figure software licenses, six-month integration projects, "100 hours of consultancy" to tune the rules (their actual pitch).

The Evant EIM work from 2003 is the even earlier precedent: a "centralized system of record repository for retail enterprise data" that Evant sold as a million-dollar integration. Canary ships the equivalent as OAuth SaaS.

The LPMS case management deployments (2015) documented the Action / Incident Type / Source-of-Info taxonomies that map directly to Canary's Fox module. The Green/Yellow/Red shrink tier pattern. The regional org cascade model.

**The conclusion:** the architecture works. The Secure-era implementations proved it. What GrowDirect is doing is making the same architecture deployable at SMB scale without the enterprise software contract. The cost barrier was the problem. The architecture was never the problem.

NCR knows this. NCR has been selling versions of this architecture for twenty years under different product names (NCR Edge, Voyix Connected Services). When GrowDirect shows NCR this architecture, they are not seeing something new — they are seeing their own design choices reflected back at them, delivered at a price point that reaches their SMB install base. That is the credibility argument.

---

## II. The Store as Compute Platform

### Why stores cannot depend on the cloud

Brick-and-mortar retail has a hierarchy of requirements for compute:

1. **Transactions must complete.** The POS cannot depend on internet connectivity. If the internet goes down, the store must ring transactions. Non-negotiable. This is why NCR Counterpoint runs on an on-prem Windows Server — by design, not by legacy.

2. **Loss prevention detection must be real-time.** A 15-minute batch lag is not real-time LP. A cloud-round-trip on every transaction is not acceptable latency. Detection must happen at or near the time of the transaction.

3. **Analytics can be eventual.** Cross-store dashboards, trend analysis, case management — these can sync on a 5-minute delay and nobody notices. The cloud is where eventual intelligence lives, not where real-time detection lives.

Cloud-first SaaS LP platforms get requirement #2 wrong. They check cloud availability on every transaction or batch-process with a lag. That is historical reporting dressed as LP. The store is offline sometimes. The store has to run. Any architecture that does not account for this is wrong for the use case.

### What is already in the store

A typical NCR Counterpoint retail installation already contains:

| Component | Role | Compute Available |
|---|---|---|
| Windows Server (back office) | Counterpoint SQL + REST API | 4–16 cores, 8–32 GB RAM, SSD |
| POS terminals | Counterpoint Point (front-end) | Thin clients — not available |
| Router/firewall | Network | Not available |
| NVR (security cameras) | Camera recording | Linux-based on modern systems; potentially available |
| UPS | Power backup | Not compute |

The Windows Server is the edge node. It is already there, already running 24/7, already has the data. The Counterpoint REST API runs as a service on this server — it is already listening on a LAN port. Adding a Docker container alongside Counterpoint is not an infrastructure investment. It is a software deployment to existing hardware.

### The store server of the future

The trajectory is toward explicit store compute platforms. Camera vendors have already built this architecture: Verkada runs inference on the camera itself for people counting and motion detection, syncs metadata to cloud, keeps raw video local. That is the edge-first pattern applied to a specific sensor type.

The generalization: modern retail stores are distributed compute clusters. POS server, NVR, self-checkout kiosks, digital signage, RFID readers, WiFi APs with embedded analytics — each is a compute node. The store is a mini data center that happens to contain products and people. The architecture must be built for this reality, not for the fiction of a single cloud-connected terminal.

---

## III. The Starbucks / NCR Edge Pattern

Starbucks runs Azure IoT Edge on hardware co-located with every espresso machine. The pattern has three layers:

**Edge layer:** Containerized workloads on in-store hardware. Operates fully offline. Runs local inference for real-time decisions (menu personalization, equipment maintenance alerts). Syncs to cloud when connected.

**Cloud layer:** Model training, fleet-wide analytics, cross-store intelligence. The "brain" that sees everything. Does not participate in real-time in-store decisions — it is too far away.

**Management plane:** Azure IoT Hub. Manages the device fleet, pushes model updates down, pulls telemetry up. The connective tissue between edge and cloud.

NCR's own Voyix Connected Services architecture is the same pattern applied to retail POS: Counterpoint server is the edge node, NCR Connect is the management plane, NCR cloud is where cross-store analytics live. NCR built this because they know stores go offline. They built Counterpoint to run without internet for exactly this reason.

**Canary's mapping:**

| Layer | Starbucks | NCR Voyix | Canary |
|---|---|---|---|
| Edge | Azure IoT Edge container | Counterpoint server | Canary Edge Agent (Docker container) |
| Data source | Espresso machine sensors | POS transactions | Counterpoint REST API |
| Local intelligence | Menu AI, maintenance alerts | Local reporting | Chirp rule subset, ALX-mini |
| Management plane | Azure IoT Hub | NCR Connect | API Gateway + polling endpoint (v1), IoT Core (v2) |
| Cloud intelligence | Azure ML, cross-store analytics | NCR cloud analytics | Canary SaaS + ALX + Bedrock |

The architecture is not invented. It is the industry-standard pattern for any serious retail compute deployment. Canary implements it against the NCR Counterpoint install base, delivered through the Rapid POS VAR channel.

---

## IV. Canary Distributed Architecture — Hub and Spoke

### The hub

**Canary Cloud** is the hub. It receives events from all store edge agents, runs the full TSP pipeline (ingestion → detection → intelligence), manages the rule catalog for the entire fleet, hosts the cloud ALX agent (Claude Sonnet via AWS Bedrock), and provides the cross-store dashboard for LP directors.

The hub does what only the hub can do: see across all stores simultaneously, detect cross-store patterns, push calibrated rule updates to the entire fleet, and run the deep inference that requires the full context of a retailer's operation.

Cloud infrastructure: AWS (ECS Fargate for containers, RDS PostgreSQL 17 + pgvector, ElastiCache Valkey, API Gateway for store event ingestion, S3 for tenant exports). Terraform-provisioned, three environments (dev/staging/prod). See GRO-615.

### The spoke

**Canary Edge Agent** is the spoke — one per store. It runs on the store's local network, talks to the Counterpoint REST API over LAN (sub-10ms latency, no internet required), evaluates a subset of Chirp detection rules locally, buffers events in SQLite when offline, and syncs to the cloud hub when connectivity is available.

The spoke does what only the spoke can do: detect in real time at the point of the transaction, operate when the internet is down, and provide the store manager with immediate signal without cloud round-trip latency.

Edge components:
- **Module T adapter** (already built): polls Counterpoint REST API, parses PS_DOC transaction stream
- **Local Chirp subset**: 15–20 highest-value LP rules that run without cross-store context
- **SQLite event buffer**: holds events during connectivity loss, replays with idempotency keys on reconnect
- **Ollama (qwen3-embedding:8b)**: local embedding generation for event classification — already in the stack
- **ALX-mini**: lightweight per-store agent, answers manager questions locally
- **Sync daemon**: `POST /v1/events` to cloud on interval; `GET /v1/commands` polls for rule updates

### The communication model

```
Cloud ALX (fleet intelligence)
    ↕ rule catalog updates (push, acknowledged)
    ↕ events + alerts (async batch, 5-min interval or on reconnect)
    ↕ ALX queries (on-demand, store ALX-mini escalates to cloud ALX)
Store ALX-mini (per-store intelligence)
    ← Counterpoint REST API (local LAN, <10ms, no internet)
    → local Chirp detection (real-time, offline-capable)
    → store manager alerts (email/SMS relay, local)
```

**Offline resilience:** When internet is unavailable, the store agent continues operating. Local Chirp fires. Local alerts generate. SQLite buffer accumulates. On reconnect, the sync daemon replays the buffer with idempotency keys — the cloud receives the events in order, deduplicates, processes. The cloud gets eventual consistency. The store never stops watching.

### Hardware options (in order of preference for v1)

| Option | Hardware | Cost | Install complexity | Risk to POS |
|---|---|---|---|---|
| Dedicated mini PC | Beelink N100, Linux | ~$180 | Plug in, run one command | None — separate device |
| Counterpoint server | Resource-capped Docker on Windows | $0 | Docker Desktop install | Low but non-zero |
| NVR piggyback | Linux-based NVR (Verkada, Axis, Hanwha) | $0 | Varies by NVR platform | None — separate device |

Recommendation for v1 pilot: dedicated mini PC. Clean isolation, Linux-native Docker, Rapid POS can ship pre-configured. The $180 hardware cost is noise against the subscription value. Evaluate Counterpoint server piggyback for retailers where adding hardware is not possible.

---

## V. The Agent Hierarchy as Field Organization

This framing is the clearest articulation of the architecture for a non-technical audience. It should be the lead in any NCR or LP director conversation.

A traditional 31-store retail chain LP organization:

```
LP Director (corporate)
    ↓ policy, rule updates, fleet visibility
Regional LP Managers (2–3, covering 10–15 stores each)
    ↓ regional pattern detection, escalation to director
Store LP Leads (per store)
    ↓ local detection, local alerts, local case management
```

The Canary agent hierarchy maps exactly:

```
Cloud ALX (LP director equivalent)
    — cross-store intelligence
    — fleet-wide rule catalog management
    — "Store 3 and Store 7 showing correlated voids on the same SKU, same shift — coordinated ring"
    — pushes updated rules to all store agents when new shrink vector identified

[Regional ALX — Phase 2, for 50+ store deployments]
    — manages clusters of stores
    — filters regional noise before it reaches cloud ALX
    — maps to how field organizations scale

Store ALX-mini (store LP lead equivalent)
    — watches that store's transactions continuously
    — knows every employee, every transaction pattern
    — fires local alerts, answers manager questions
    — escalates cross-store patterns up to cloud ALX
```

**Why this framing lands:** LP directors have built and managed field organizations. The concept is not abstract to them. "We are giving you a store agent in every location and a director watching the fleet" is a sentence they have used to describe their own teams. The technology disappears; the outcome — LP field coverage without headcount — is what they buy.

**The economics:** A 31-store chain with 2 regional LP managers at $80K each plus a director is $240K/year in field LP headcount, before the LPMS software they run on top. The crossover math from the data-economics analysis makes the case without needing to be aggressive about it.

---

## VI. AI and Model Architecture — The Decision

### What not to do: fine-tuning

Fine-tuning Claude or any foundation model on retail LP domain data costs $10K–50K+ for a training run and produces a model that is worse at general reasoning while being marginally better at domain-specific pattern completion. This is the wrong trade for an agent use case.

The "ALX knows your operation" story does not require fine-tuning. It requires a well-structured knowledge base that ALX can retrieve from. The knowledge base is the retailer's vault: transaction patterns, location profiles, employee roster, vertical context, detection rule history. ALX retrieves from this vault on every query and reasons over retrieved context. The result is indistinguishable from fine-tuning to the user — and it is updateable in real time as the retailer's operation changes, which fine-tuning is not.

### The correct architecture: RAG + Bedrock

**Edge inference:** Ollama (qwen3-embedding:8b) for embedding generation. Deterministic Chirp rules for LP detection. No LLM at the edge — it is overkill and adds GPU dependency to Windows Server hardware.

**Cloud inference:** Claude Sonnet via AWS Bedrock. Same model as the Anthropic direct API, different endpoint and auth (AWS SigV4). Bedrock is the credibility move for NCR and SBX: it is an AWS enterprise service, SOC2 compliant, procurement teams know how to buy it, and it means ALX's reasoning happens on the same AWS infrastructure as the retailer's data.

**Retrieval:** pgvector memory bus (already built). The `qwen3-embedding:8b` model generates 1024-dimension vectors. Chunks are: retailer entity cards, location profiles, employee context, Chirp rule documentation, historical alert patterns, vertical knowledge. ALX retrieves the most relevant chunks on every query and reasons over them.

**What this means for the "trained AI" narrative:** The training story is a retrieval story. ALX is trained on this retailer's operation in the sense that its knowledge base is populated with context from the CATz engagement — not in the sense that the model weights have been modified. This is the right answer and it is defensible under technical scrutiny from an NCR or SBX engineering team.

---

## VII. Counterpoint Integration — How It Actually Works

### The existing polling landscape (as-is)

A typical Counterpoint store today extracts data through one of four mechanisms:

1. **ODBC direct query**: Crystal Reports or Excel connected to Counterpoint SQL Server via VPN or site-to-site link. Head-office reporting server pulls nightly. Latency: 12–24 hours. Coverage: whatever the report template captures.

2. **Counterpoint report scheduler**: Built-in scheduler generates CSV or PDF on a configurable cadence, drops to a network share or emails. Latency: configurable but typically daily. Coverage: Counterpoint's canned reports.

3. **Manual UI export**: Manager pulls a report from the Counterpoint UI at end of day or end of week. Latency: days. Coverage: whatever the manager remembered to pull.

4. **NCR Connected Services**: For retailers on the NCR cloud contract, NCR's own polling agent pulls from Counterpoint. Latency: varies. Coverage: NCR's analytics product scope.

None of these produce real-time LP detection. None aggregate cross-store automatically. None give a store manager immediate alert on a suspicious transaction pattern.

### The Canary integration (to-be)

Module T polls the Counterpoint REST API on the local LAN. The API runs as a Windows service on the Counterpoint server, typically on port 52000+. The relevant endpoints:

- `GET /documents` — PS_DOC transaction records (the primary LP data source)
- `GET /items` — IM_ITEM item master
- `GET /customers` — AR_CUST customer records
- `GET /paycode` — PAY_TYP tender taxonomy
- `GET /employees` — employee roster (time clock integration via TIM_CLK)
- `GET /inventory` — inventory snapshots

Module T polls on a configurable interval (default: 60 seconds for live detection; 5-minute batch for historical backfill). Each poll returns only new or modified records since the last poll timestamp — delta-based, not full table scans. Idempotency keys on every event prevent double-processing during replay.

### What we are not doing

Canary does not modify Counterpoint. It does not write to the Counterpoint database. It does not require Counterpoint configuration changes beyond enabling the REST API (which Rapid POS typically enables as part of their standard install). It is a read-only integration. This matters for the NCR conversation: we are not competing with Counterpoint. We are adding a capability layer on top of it.

---

## VIII. Migration Path — Old Polling to Canary Edge

The migration has four phases, each with a defined validation gate before proceeding.

**Phase 0 — Discovery:** Map the as-is polling topology. What is currently pulling from this Counterpoint instance? ODBC connections? Report scheduler? NCR Connected Services? Establish the baseline before adding Canary. The existing polling is not retired yet — it runs in parallel during the transition.

**Phase 1 — Shadow install:** Canary Edge Agent installed, running in shadow mode. Polls Counterpoint REST API. Generates events to SQLite buffer. Does NOT sync to cloud or fire alerts. Goal: validate that Module T works against this tenant's Counterpoint configuration and data shape. Duration: 1–3 days.

**Phase 2 — Cloud sync live:** Enable sync to Canary Cloud. Historical backfill begins (Module T pulls PS_DOC history, minimum 12 months). Rule catalog seeded for the tenant's vertical. Dashboard starts populating. No live alerts yet — LP lead reviews first week's output for calibration. Duration: 5–7 days.

**Phase 3 — Detection active:** Local Chirp rules enabled. Cloud Chirp active. Alert routing configured. LP lead reviews first 5 business days of alerts for tuning. This is the go-live gate. Old polling still running in parallel. Duration: 5 business days of active validation.

**Phase 4 — Old polling retired (optional):** After 30 days of stable Canary operation, the existing reporting tools (Crystal Reports, xBR if present) can be decommissioned. This is the rewiring step — not required for Canary to work, but eliminates the redundant polling load on the SQL Server.

**The pilot acceleration path:** For a Rapid POS sandbox or a first-store pilot, Phases 0–2 can compress to 48 hours. Module T pointed at a known Counterpoint instance with existing transaction history produces meaningful Chirp output within one business day of first connection. The 48-hour diagnostic is the demo.

---

## IX. Deployment and Distribution — Rapid POS as the Channel

### Why Rapid POS is structurally different from a typical VAR

A typical VAR reselling a SaaS LP platform introduces a dependency the merchant will eventually resent. The SaaS vendor takes the subscription revenue, the VAR takes a referral fee, the merchant's data sits on the SaaS vendor's servers, and the VAR has no leverage in the relationship after the sale.

Rapid POS deploying Canary Edge Agent is structurally different:

- **Physical install footprint**: Rapid POS techs have already been inside every customer's back office. They know where the server is. The edge agent install is one additional step in a workflow they already own.
- **Ongoing relationship**: Rapid POS does remote monitoring and support via RMM. Canary fleet monitoring surfaces store health through the same operational lens. They can see "Store 7 edge agent hasn't heartbeated in 2 hours" as part of their existing monitoring posture.
- **Economics**: Rapid POS controls the relationship. They bundle the edge agent into their install package. They set the margin. GrowDirect earns on the platform and support; Rapid POS earns on the deployment and ongoing service.
- **The pitch to Bart**: "Every Counterpoint install you've ever done can have Canary running in the back office by end of week. You install it the same way you install Counterpoint."

### The immediate pilot path

1. Bart provides sandbox Counterpoint endpoint + REST API credentials (Monday call)
2. Module T pointed at sandbox — shadow run, first events flowing (this week)
3. Chirp rules evaluating, dashboard populating, first ALX diagnostic output (within 48 hours of connection)
4. That output is the artifact — the thing we walk NCR into the room with
5. One production store (Rapid POS customer) — same playbook, 2–3 days
6. Full chain rollout — Rapid POS RMM enables remote install at each store (2–4 weeks for 31 stores)

The Terraform fleet infrastructure (GRO-615) is the scale story. It follows the pilot. The sandbox connection is the validation story that makes the scale story credible.

---

## X. Open Questions and Next Decisions

| Question | Decision Required | Owner | Timeline |
|---|---|---|---|
| Does Bart's sandbox have real transaction history or thin test data? | Determines how quickly Chirp produces meaningful signal | Bart (Monday call) | Monday |
| What Windows Server versions are in the Rapid POS install base? | Determines Docker Desktop compatibility for Counterpoint server piggyback option | Bart (Monday call) | Monday |
| Does Rapid POS RMM have sufficient access to push and run Docker Compose remotely? | Determines whether fleet rollout requires truck rolls or can be done remotely | Bart (Monday call) | Monday |
| What camera systems do Rapid POS customers typically run? | Determines whether NVR piggyback is a viable hardware option | Bart (Monday call) | Monday |
| API Gateway v1 vs. IoT Core for event ingestion | Architecture decision for GRO-615 | Architect | Before Terraform build |
| Polling endpoint v1 vs. SQS for store relay | Architecture decision for GRO-615 | Architect | Before Terraform build |
| Aurora Serverless v2 vs. RDS per-tenant for staging | Database decision for GRO-615 | Architect | Before Terraform build |

---

## Related

- [[Brain/projects/Canary|Canary MOC]] — project hub
- [[Brain/wiki/canary-architecture|Canary Architecture]] — platform architecture (16 services, MCP layer)
- [[Brain/wiki/ncr-counterpoint-api-reference|NCR Counterpoint API Reference]] — endpoint catalog
- [[Brain/wiki/secure-sysrepublic-xbr-2016|xBR Replacement 2016]] — prior-art: Foundation Objects / Lead Development / Case Management
- [[Brain/wiki/secure-lpms-case-management-2015|Sporting-Goods Chain LPMS 2015]] — prior-art: Green/Yellow/Red shrink tiers, regional org cascade
- GRO-612: Canary Edge Agent architecture (strategic backlog)
- GRO-613: Edge agent SDD + Bedrock integration spec (dispatch)
- GRO-614: NCR Brain deep-dive + Mermaid diagrams (dispatch)
- GRO-615: Terraform cloud receiving infrastructure (dispatch)
