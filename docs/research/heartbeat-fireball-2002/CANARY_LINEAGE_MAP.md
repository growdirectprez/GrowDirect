# CANARY_LINEAGE_MAP — the synthesis

The payoff document. What Canary inherits, knowingly or not, from the
2002 OOS detection + notification system; what Canary transforms; what
is genuinely new in Canary with no 2002 analogue; and what the
Phase-I retrospective from 2001 surfaced about whether the design
actually worked in production (abstracted to NFR-profile language per
playbook).

## Component map

| 2002 component | Canary equivalent (2026) | Match | Notes |
|---|---|---|---|
| Trickle POS feed (XML over HTTPS/VPN, retailer-side push) | TSP webhook ingest (JSON over HTTPS, push from Square) | **Transformed** | Same role — continuous near-real-time POS event arrival as foundation. Push-from-source rather than pull-from-source. JSON not XML. Replay semantics via webhook event IDs not custom envelope. |
| Enterprise integration bus (multi-server cluster, Open Channels pattern) | Webhook subscription manager + Sub 1/2/3 worker chain | **Transformed** | Same role: absorb source-system heterogeneity, present canonical event shape downstream. Commodity Flask + RQ + Postgres instead of an enterprise EAI platform. Same separation of routing-state from event-state. |
| OOS detection algorithm (Poisson velocity model, per-store-per-SKU, 8 covariates, 15-min retrain) | Chirp detection rules (27+ named rules, deterministic, severity-scored) | **Transformed** | Single statistical-anomaly algorithm → multi-rule deterministic engine. Both per-(merchant, signal) tunable. Canary broadens the detection surface from "OOS only" to "many exception classes"; the 2002 algorithm sophistication has a future home in the Bayesian / KAP scoring layer Canary's data strategy describes. |
| Algorithm cluster's compressed transaction store (XPDB) | `sales` schema transactions table (Postgres, indexed for chirp queries) | **Transformed** | Same role: fast access to recent transaction stream optimized for the detection layer. Standard Postgres rather than a specialized columnar store; the SMB-scale transaction volumes don't require the specialized store. |
| Events cache server (in-memory, query interface for HTML / XML clients) | Alert table + alert MCP server (DB-backed, query interface for REST + agent) | **Transformed** | Persistent (DB) rather than volatile (in-memory cache); agent surface added; otherwise same role. |
| Notification subsystem (subscription model, multi-channel routing, format-aware rendering, failure-mode awareness) | Alert notification service (severity filter + quiet hours + rate cap + digest batching, multi-channel SMS/email/push/in-app) | **1:1 conceptually** | The single most directly inherited component. Same job, modernized channel set, same operator-as-final-recipient design. |
| XML event schema (Aug → Jan evolution) | Webhook payload + normalized CRDM rows | **Transformed** | XML → JSON, enterprise-schema → commodity/mobile-friendly. Aug-vs-Jan delta in 2002 reflects the same kind of production-driven schema evolution Canary has done across CRDM versions. |
| Pager / handheld notification (SMTP, 8×25 char hard cap, no app to learn) | SMS + push + in-app + email (multi-channel, format-aware per channel) | **Transformed** | Same operator-context discipline (design to the receiving device), updated channel set. Modern infrastructure removes the lowest-common-denominator constraint. |
| Browser-based reports (HTML events formatter, CGI) | In-app dashboard (Flask + Jinja + Alpine) | **1:1 conceptually** | Same role, identical philosophical placement (secondary to push notification, primary for fuller summary). |
| Operator workflow (open → browse → act → delete; no system-tracked acknowledgement) | Alert lifecycle (`new` → `investigating` / `escalated` / `resolved` / `dismissed` / `case_opened` / `archived` with full history) | **Net-new in Canary** | The 2002 design left "did the operator act?" outside the system; Canary brings it inside. One of the largest deltas. |
| Professional-services deployment (consulting engagement to install integration platform + collection routines + notification subsystem per retailer) | OAuth self-service onboarding | **Net-new in Canary** | The single largest design delta. 2002 required consulting; 2026 doesn't. |
| In-store autonomous device variant ("a heartbeat box in every store") | (no equivalent — Canary chose hosted SaaS outright) | **Net-new omission** | The 2002 era kept the in-store device as a hedge against fragile WAN; modern Canary has no such hedge because it doesn't need one. |
| Algorithm-vendor + integration-platform-vendor partnership structure | (no equivalent — Canary owns the entire stack) | **Net-new omission** | The 2002 design depended on two distinct commercial partnerships; the Phase-I retrospective flagged both as friction. Canary's vertical-integration is a deliberate response. |
| (no 2002 equivalent) | Bitcoin Ordinal evidence chain (immutable, cryptographic, write-once) | **Net-new in Canary** | The sovereignty / forensic-integrity moat. No 2002 analogue — wasn't possible until Bitcoin Ordinals shipped. |
| (no 2002 equivalent) | Lightning micro-payment plumbing | **Net-new in Canary** | Pricing / settlement moat. No 2002 analogue. |
| (no 2002 equivalent) | Fox case management with cryptographic evidence chains | **Net-new in Canary** | The investigation-lifecycle layer. The 2002 design left investigation outside the system; Canary brings it inside as a first-class domain. |
| (no 2002 equivalent) | Owl agentic memory + retrieval | **Net-new in Canary** | Agent-side context aggregation. No 2002 analogue — the agent paradigm wasn't yet possible. |

## What the 2002 design got right

1. **The trickle feed as foundation.** Continuous near-real-time POS
   event arrival as the *only* viable substrate for live detection.
   Canary's TSP design starts from the same axiom 25 years later
   without re-litigating it.
2. **Operator as final recipient, not system as final actor.** The
   2002 design routed alerts to a human at the physical point of
   action and trusted them to act. Canary preserves this choice — Chirp
   alerts the merchant, Fox helps them investigate, but humans close
   the loop. No automated remediation in the data path.
3. **Subscription / filter / sort tunable per user.** The pager
   subscription system already understood that one alert shape per
   organization fails — different roles need different filters and
   sort orders. Canary's per-user notification preferences and
   role-based dashboards inherit this.
4. **The "Data Flow Interrupted" alarm.** The non-suppressible
   pipeline-health alert is structurally important — an operator
   needs to distinguish "no alerts because nothing's wrong" from "no
   alerts because we lost visibility." Canary's TSP heartbeat /
   pipeline-health monitoring carries this forward.
5. **Open-routing pattern (destination derived from message body).**
   The integration bus's "Open Channels" pattern of deriving routing
   from message content is exactly the design choice that makes
   modern multi-tenant SaaS routing work. The 2002 designers got it
   right; the modern equivalent (event-content-aware routing) is
   load-bearing in any SaaS event pipeline.
6. **Per-(item, store) baseline.** The choice to learn velocity at
   per-store-per-SKU granularity rather than aggregating across the
   chain is the right one for detection — and it's the choice
   Canary's per-merchant rule configuration mirrors.

## What the 2002 design got wrong (or right-for-2002, wrong-for-2026)

1. **The deployment cost.** Every retailer onboarding required a
   paid integrator engagement to install the EAI platform, the POS
   collection routines, and the notification subsystem. The Phase-I
   retrospective explicitly flagged "the pilot project has not yielded
   a turnkey solution that would allow rapid adoption." Right-for-2002
   (the infrastructure required it), wrong-for-2026 (commodity SaaS
   makes self-service onboarding the default).
2. **The two-vendor partnership structure.** Algorithm vendor +
   integration-platform vendor + the manufacturer sponsor meant three
   parties had to align commercially before any retailer could deploy.
   The Phase-I retrospective lists this as a top-line risk. Canary's
   single-vendor stack is the deliberate inverse.
3. **Notification delivery to a single device family at a time.**
   Pilot-era constraint (8 lines × 25 chars), but the design didn't
   anticipate that delivery channels would multiply faster than the
   subscription system could keep up. Modern channel sets (SMS, push,
   in-app, email, voice, agent surface) need the channel router to be
   first-class, not a "future filters" item.
4. **No system-tracked operator acknowledgement.** Leaving "did the
   operator act?" outside the system means the system can't measure
   its own effectiveness. Canary brings this inside — explicit
   alert lifecycle states, time-to-acknowledge, time-to-resolve.
5. **Algorithm tunability hidden from operators.** End-users had
   subscription knobs but no detection knobs. Canary exposes detection
   thresholds to merchants via `merchant_rule_configs` — the operator
   can adapt the system to their actual business, not just adapt their
   subscriptions to the system's defaults.
6. **No event store / no replay.** The 2002 architecture stored events
   in an in-memory cache. If the cache evicted, the historical record
   was the integration bus's optional SQL data mart — a separate
   system, not authoritative. Canary's append-only `evidence_records`
   table makes the event stream the durable, replayable, forensic-grade
   ground truth.

## What the Phase-I Pilot Assessment revealed (abstracted)

The April 2001 retrospective by the integration vendor's consulting
arm carried the following technical / operational findings, abstracted
to NFR archetype:

- **Algorithm scalability and performance** were named as risks. The
  per-(store, SKU) Poisson model with 15-minute retrain and 8
  covariates is computationally non-trivial; performance under
  full-store SKU coverage (vs the 1,000-SKU pilot scope) was open.
  *NFR-profile observation*: at US Tier-1 grocery scale with
  super-format stores carrying ~120k SKUs, the algorithm's per-store
  computation cost was a real design constraint.
- **Algorithm tuning time per retailer** was named as adoption-rate
  drag. Each new retailer required model tuning by the algorithm
  vendor before the OOS detection was production-quality. *NFR-profile
  observation*: at the per-retailer onboarding tempo of the Tier-1
  + multi-state-southeastern deployment archetype, this was viable;
  at SMB / long-tail retailer scale it would be prohibitive.
- **Notification subsystem itself** was on track to ship by end of
  March 2001 against a Phase-I deadline; **independent algorithm
  audit** by the southeastern-chain pilot was on track for the same
  week. The notification half of the system worked under the
  retrospective; the algorithm half was tunable but per-retailer
  expensive.
- **Business-model risks** dominated the retrospective's risk list
  more than technical risks: ROI schedule communication, commitments
  to next-round pilots, recoupment of investment, escalating
  requirements without clear ROI. The technical system worked; the
  go-to-market did not.

## What Canary inherits — knowingly or not

- The trickle-feed-as-foundation axiom
- The operator-as-final-recipient design
- The per-(merchant, signal) baseline
- The subscription / filter / sort tunability per user
- The non-suppressible pipeline-health alarm
- The open-routing pattern (event content drives routing)
- The notification-subsystem shape (trigger → subscription → channel-
  aware render → operator)
- The split between fast-detection store and routing/state store

## What is genuinely new in Canary

- Self-service OAuth onboarding (the largest single delta)
- Single-vendor stack with no algorithm-or-integration-vendor
  dependency
- System-tracked operator acknowledgement and full alert lifecycle
- Investigation lifecycle (Fox) as a first-class domain
- Cryptographic evidence chain (Bitcoin Ordinal anchoring)
- Lightning micro-payment plumbing
- Agent surface (Owl + MCP) that didn't exist as a paradigm in 2002
- Per-merchant detection threshold tuning exposed to the operator

## Open questions

- **The naming relationship.** The 2002 system was called Heartbeat /
  Fireball; Canary's data-strategy NorthStar describes a "Canary
  Heartbeat Network" anchored to Bitcoin's block heartbeat. The
  founder has confirmed the two are related; the form of the
  relationship (direct homage, conceptual lineage, or architectural
  DNA) is recorded as a Phase-5 research item in the parent playbook.
- **The XML schema delta.** The Aug → Jan schema evolution in the
  2002 archive is documented but the specific deltas weren't extracted
  in this research pass. Worth a follow-up if Canary's webhook payload
  evolution would benefit from the prior-art lessons.
- **The in-store autonomous device variant.** The 2002 design held
  open the option of a per-store device. Modern infrastructure makes
  this clearly unnecessary, but the question of edge-deployable Canary
  components is worth keeping open as a future architectural option
  rather than a closed door.
