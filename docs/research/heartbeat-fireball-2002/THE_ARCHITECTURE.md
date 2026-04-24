# THE_ARCHITECTURE — the working data pipeline

End-to-end working architecture of the 2001–2003 retail OOS detection
and notification system, extracted from the available design artifacts.
The pipeline shape is: **trickle POS feed → enterprise integration bus
→ OOS detection algorithm cluster → enterprise integration bus →
notification subsystem → operator's wireless device.**

## Two functional domains

The system was decomposed into two named functional domains:

1. **Retail Integration & Operations Services (RIO)** — the integration
   layer between the retailer's existing systems and the hosted analytic
   service. RIO had two subsystems:
   - **RIO Inputs** — collected POS, item, and promotional data from the
     retailer; translated into XML; pushed to the hosted service over
     HTTPS or VPN.
   - **RIO Outputs** — routed outbound notification messages to the
     endpoint devices (handheld push-email + alphanumeric pagers via
     SMTP).
2. **Hosted Notification + Detection Service** — a centrally hosted
   web service that received RIO Inputs, ran the OOS detection
   algorithm, and issued notification messages back through RIO
   Outputs. Designed to support multiple retail enterprises with
   thousands of stores against a shared infrastructure footprint.

> *Canary analogue.* Same two-domain split, modernized substrate. RIO
> Inputs ≈ TSP webhook ingest + Sub 1 evidence persistence. Hosted
> Notification + Detection ≈ Sub 2 / Sub 3 / Chirp + alert delivery.
> RIO Outputs ≈ alert notification routing (SMS / email / push / in-
> app).

## The hosted service anatomy

A multi-cluster web service. Five clusters, each playing a distinct
role:

| Cluster | Role |
|---|---|
| Web Cluster | All HTTP/HTTPS connectivity. Interface to the integration bus through receive functions. Customer VPN + FTP. Web interface for managing access to notification subscriptions. |
| Integration Bus Cluster | All message and data routing for the service. Open Channels and Message Ports derive transport and destination from data inside incoming XML. Transport and destination tables in clustered SQL. |
| Application Server Cluster | Business objects for the notification subsystem. Web-interface support objects. |
| SQL + Analysis Services Cluster | Integration-bus state databases. Optional repository for POS + item + promotion data using the standard retail data model fed by an industry-standard XML data model. Optional retail business-intelligence cubes generated and served as a web service to the enterprise customer. |
| OOS Application Server Cluster | The OOS detection algorithm itself + the per-installation models it carries. Receives POS data from the integration bus, processes it, returns OOS messages back to the integration bus for routing. |

> *Canary analogue.* Canary collapses these five clusters into one
> Flask service with named modules and one Postgres database with
> schema-level separation (`app` / `sales` / `fox` / `metrics`). Same
> five logical roles, dramatically less infrastructure.

## The trickle feed pattern

The 2002 design used a **trickle feed** of POS transaction-log (TLOG)
data from the retailer. Salient properties:

- **Granularity.** Minute-by-minute transaction data containing the
  details of what items were observed and at what price for every
  transaction. A "transaction" is a basket-checkout; "observations"
  are item codes scanned by the cashier. Each transaction carries at
  minimum: timestamp, sequence of item codes, quantities, net price
  (regular price + applicable discounts) per line.
- **Cadence.** Continuously trickled (not batch). The data feed was
  the essential prerequisite to the 15-minute model rebuild.
- **Companion master feed.** Daily Item Tables fed product master
  context (PLU, attributes, hierarchy, current promotional status).
- **Failure mode.** A separate **Data Flow Interrupted alarm** existed
  precisely because trickle integrity was operationally fragile — when
  the trickle paused, the OOS reports lost their basis and operators
  needed to know.

> *Canary analogue.* TSP webhook ingest is the modernized trickle feed —
> push-from-source rather than pull, JSON over HTTPS with replay
> tokens rather than XML over VPN. Same role: continuous near-real-time
> POS event arrival as the foundation everything else depends on. The
> Data Flow Interrupted alarm has a direct successor in TSP heartbeat
> monitoring.

## The integration-bus role

The enterprise application integration (EAI) bus did three things:

1. **Receive** XML messages from the retailer (POS, item, promotional
   data) over HTTPS/VPN, validate against published XML schemas.
2. **Route** to the right next-hop based on data inside the message.
   The "Open Channels" pattern meant the bus didn't need a per-trading-
   partner port configuration — destination and transport were derived
   from the message body, against a SQL-backed routing table. One
   messaging port served many retailers.
3. **Deliver** outbound notification messages to SMTP endpoints (pagers)
   based on subscription rules. Same Open Channels pattern in reverse —
   destination came from subscription state, not hardcoded routes.

The bus was deliberately the asymmetric load-bearing component: it
absorbed retailer heterogeneity (every retailer had its own POS
controller and its own "method and system for collecting and storing
POS data") and presented the algorithm cluster with one canonical XML
shape.

> *Canary analogue.* Webhook subscription manager + Sub 1/2/3 chain.
> Same role (absorb source heterogeneity, present canonical event
> shape downstream); commodity infrastructure (Flask + RQ + Postgres)
> instead of an enterprise EAI platform; far fewer moving parts.

## The OOS algorithm cluster — what flows in, what flows out

The algorithm cluster was packaged as ten named components:

| Component | Role |
|---|---|
| Data feed handler | Trickled TLOGs + daily Item Tables in |
| Data handlers (RCO, POS-DataSource, XPDataReader, XPIVMDBWrite) | Schema validation + parsing + load |
| High-speed compressed transaction database (XPDB, XPSORT) | Fast columnar-style store of the recent transaction stream |
| Velocity monitoring + OOS detection algorithm | The core (see THE_ALGORITHM.md) |
| Item-movement + velocity/OOS events cache and server | In-memory cache of computed events; query interface |
| Web server (HTTP daemon) | Reporting endpoints |
| HTML events formatter (CGI) | Browser-based reporting client |
| XML events formatter (notification client) | Outbound message formatter to the integration bus |
| Processing scheduler (cron) | Drives the 15-minute model rebuild |
| Batch process script (driver) | Orchestration |

The algorithm cluster had its own internal store (XPDB) — *not*
operating against the integration bus's SQL cluster. The two stores
served different purposes: the algorithm's store held the recent
transaction stream optimized for the velocity computation; the bus's
SQL cluster held routing state, subscription state, and (optionally)
the data-mart copy of POS data.

> *Canary analogue.* Chirp detection rules + the rule-execution worker
> pool ≈ the velocity monitoring + OOS detection layer. The XPDB
> compressed-transaction store has a role-equivalent in the `sales`
> schema (transactions table, indexed for the chirp queries). The
> separation between "raw stream store" and "routing/subscription
> state store" survives in Canary as the separation between `sales`
> and `app` schemas.

## Two collection patterns evaluated

The pilot deliberately compared two architectures:

1. **In-store autonomous device.** Heartbeat box per store, connected
   directly to the POS controller, performing OOS analysis locally,
   serving HTTP-based reports browser-readable on the LAN.
2. **Centralized hosted service.** POS data shipped from each store to
   the central hosted service, OOS analysis run remotely, results
   delivered to operators on wireless devices via SMTP.

The hosted-service architecture won the document footprint — it became
the basis of the architecture described above. The in-store device
remained as a hypothetical product variant ("a heartbeat box in every
store") that the algorithm vendor could continue marketing.

> *Canary analogue.* Canary chose the centralized SaaS pattern outright,
> with no in-store device. The 2002 trade-off was settled in 2026 by
> the maturation of cloud + cellular + ubiquitous IP — the in-store
> autonomous box made sense when WAN was fragile; for SMB SaaS in
> 2026 it doesn't.

## The reporting surface (alongside notifications)

Operators got reports in three shapes:

1. **Pager / handheld notification** — primary delivery (see
   THE_NOTIFICATION_SYSTEM.md). Push to wireless device, SMTP transport.
2. **Browser-based reports** — secondary delivery from the algorithm
   cluster's HTTP daemon + HTML events formatter. Used for fuller
   summary review and for an independent audit pathway (the
   southeastern-chain pilot used browser reports to audit algorithm
   accuracy).
3. **XML events stream** — programmatic consumption from the events
   cache server via XML or HTML client connection. Designed for
   downstream supply-chain integration (the eventual hand-off to
   manufacturer / vendor systems that the broader thesis imagined).

> *Canary analogue.* Same three shapes: in-app alert dashboard
> (browser equivalent), push/email/SMS alerts (notification
> equivalent), and the alert MCP server + REST API (programmatic
> stream equivalent). The 2002 design anticipated a programmatic
> downstream consumer; Canary actually has one (the agent surface).

## Foundation reference

The system was built on a Microsoft enterprise integration platform
(EAI bus + Windows Advanced Server cluster + SQL + Analysis Services)
with the OOS detection algorithm provided by a specialized analytics
vendor. A Microsoft "Retail BizTalk Resource Kit" provided the
foundational integration pattern library. The platform-vendor
relationship and the algorithm-vendor relationship were two distinct
commercial partnerships, both cited as friction points in the
Phase-I retrospective (see CANARY_LINEAGE_MAP.md).

> *Canary analogue.* Canary owns the entire stack — no algorithm
> vendor, no integration platform vendor. The 2002 partnership
> structure is one of the design choices Canary explicitly *doesn't*
> inherit.
