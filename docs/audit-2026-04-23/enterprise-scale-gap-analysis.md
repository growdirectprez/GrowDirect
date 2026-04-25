---
date: 2026-04-24
type: gap-analysis
classification: confidential
owner: GrowDirect LLC
phase: G2
scope: enterprise-scale benchmark vs current Canary + GrowDirect platform state
---

# Enterprise-Scale Gap Analysis

## Governing thesis

Canary is positioned as an SMB-first SaaS for Square-connected specialty
merchants — single-store and small-multi-store retailers, food-and-beverage
operators, and service businesses where the buyer is the owner, the
deployment is self-serve OAuth, and the unit economics make a four-figure
annual subscription work. The enterprise bar in retail loss prevention is a
separate operating shape: tiered redundant deployment, federated identity,
six-figure annual subscriptions, multi-month implementation engagements,
and a stable schema contract over heterogeneous POS feeds at TB scale.
Canary does not meet that bar today, and is not trying to. The gaps below
are either roadmap items with quarter commitments, or choices-by-design
that follow from the SMB-first positioning. This document distinguishes
the two kinds honestly and cites concrete code and schema where it states
"what we have."

## Executive summary

| Dimension | What we have | Enterprise bar | Gap classification |
|---|---|---|---|
| Aggregate transaction volume | Single Postgres 17 instance ingesting Square webhook events; today's load is small per merchant; design supports horizontal Valkey-streamed pipeline scale-out | Tens of millions of POS transactions per day across the customer base, TB-scale repository | ROADMAP-Q4-2026 (capacity), CHOICE-BY-DESIGN (single-instance defaults) |
| Per-tenant transaction volume | Continuous Square webhook ingest, HMAC-verified, replayable from Valkey; demo merchant runs ~7,300 rows across 11 weeks | Thousands of POS transactions per store per day, continuous ingest | CHOICE-BY-DESIGN (current target tenants) — bar met for SMB tenants, untested for enterprise |
| Data-model abstraction | `sales` schema is a canonical CRDM-shaped layer; multi-POS proof SDD documents how non-Square sources land in the same shape | Stable schema contract between raw heterogeneous POS data and detection / case layer | MET (in design and proof-of-concept; production breadth GAP — only Square live) |
| Persistence decomposition | Three Postgres schemas (`app`, `sales`, `metrics`) with clear ownership; Valkey for sessions, streams, idempotency, cache; separate `growdirect_memory` database for the memory bus | Logically separate stores for sales data, cases, users, hierarchies, reporting, job system | MET in principle (collapsed to fewer stores); CHOICE-BY-DESIGN |
| Identity federation | Magic-link auth via Flask-Login (primary), Square OAuth as POS connection, JWT middleware with development/keycloak modes, sessions in Valkey | SAML 2.0 + OpenID Connect, role mapping via assertions, both self-service and admin-assigned role paths | ROADMAP-Q1-2027 (enterprise-tier feature), CHOICE-BY-DESIGN for SMB tier |
| Deployment redundancy | Single-host Docker Compose dev; Cloudflare Tunnel for ingress; cloud target ECS Fargate; no current redundant tiers in production | Tiered: non-redundant → single-DC-redundant → cross-DC | ROADMAP-Q3-2026 (single-DC redundancy), ROADMAP-Q1-2027 (cross-DC) |
| Self-host / VPC option | SaaS-only by design; container layout is self-host-portable; no published self-host distribution | Enterprise customers expect the option | ROADMAP-Q2-2027 (private VPC tier) |
| Data retention tiering | Detail retention is configurable per merchant via `merchant_settings.lookback_days` (default 30, NULL = unlimited); separate `metrics` schema holds derived aggregates | Detail window + aggregated-metrics window | MET (architecture); GAP on tunable retention windows + automated rolloff |
| Opinionated defaults | Default Chirp ruleset enabled at onboarding (37 rules, 8 categories); default dashboard; OAuth-driven first-run sync; default notification frequency caps | Pre-wired install, not a kit of parts | MET |
| Rule tuning for retailer patterns | Per-merchant `merchant_rule_config` with `is_enabled`, `custom_threshold`, `notify_enabled`, sensitivity presets; threshold cache via Valkey | Per-customer tunable rule engine | MET |
| Delivery organization scale | Self-serve onboarding via Square OAuth; no implementation organization; pricing is monthly subscription tiers in the four-figure-annual range | Enterprise-tier deployments (six-figure first-year subscription, four-to-six-month implementation windows) vs SMB self-serve | CHOICE-BY-DESIGN (positioning) |
| Adjacent-module pricing | Core LP product runs on Chirp + Fox; adjacent modules (e.g., Goose payment middleware) exist in code but not in commercial pricing today | Core product plus adjacent modules at independent pricing | ROADMAP-Q3-2026 (commercial pricing for adjacencies as they ship) |

## Per-dimension analysis

### Aggregate transaction volume

**What we have.** Canary runs on a single PostgreSQL 17 instance with three
schemas (`app`, `sales`, `metrics`) plus a separate `growdirect_memory`
database for the memory bus. Webhook ingest is staged through Valkey 8
streams (`canary:events`) consumed by four independent subscribers — Sub 1
seal, Sub 2 parse, Sub 3 Merkle batch, Sub 4 detect — each running as a
standalone process via `python -m canary.services.tsp.run_consumer`. The
Square webhook gateway at `POS /webhooks/<source>` (`canary/blueprints/webhooks_tsp.py`)
performs a strict 10-step sequence: read raw bytes, validate source, check
payload size (1MB max), verify HMAC-SHA256 signature with timing-safe
`hmac.compare_digest()`, compute SHA-256 hash of raw bytes before JSON
parsing, parse for routing, idempotency check via Valkey DB 3 (SET NX, 24h
TTL), generate ULID event_id, fire Tier 1 stateless Chirps non-blocking,
publish 9-field message to `canary:events`, write `ingestion_log`, return
200. Today's production load is small — early-customer scale, not
stress-tested at enterprise transaction rates. The architectural seams for
horizontal scale-out are in place: each `XREADGROUP` consumer group reads
independently with no coordination across groups; the `sales` schema is
write-once with PostgreSQL trigger-enforced immutability on
`evidence_records`; the `metrics` schema is fully re-derivable.

**Enterprise bar.** Tens of millions of POS transactions per day across the
customer base, TB-scale repository at the largest tenants. The reference
shape is a multi-thousand-store retailer ingesting continuously, retaining
detail for multiple quarters and aggregates for years.

**Gap classification.** ROADMAP-Q4-2026 for the capacity-validation work:
load testing the Valkey stream pipeline at multi-million-transactions-per-day
aggregate, partitioning the `sales` schema by merchant + date, provisioning
the read-replica path, validating that the `pg_advisory_xact_lock`
serialization Sub 1 uses for chain-hash writes does not bottleneck at scale.
CHOICE-BY-DESIGN for the single-instance default — the SMB total-cost
target makes a primary-replica Postgres pair an inappropriate baseline.
The architecture supports horizontal scale-out without rewrite; the
deployment shape changes when revenue justifies it.

### Per-tenant transaction volume

**What we have.** Continuous Square webhook ingest with deduplication
(`webhook_events.event_id` UNIQUE), per-tenant idempotency via Valkey
SET NX, schema fingerprint tracking (`schema_fingerprints` keyed on
SHA-256 of sorted field paths) that detects Square-API structure changes
and surfaces them as `schema_drift_alerts` rows. Eighteen Square-specific
parsers under `canary/services/parsers/` (`square_payment_parser`,
`square_order_parser`, `square_loyalty_parser`, `square_payout_parser`,
`square_dispute_parser`, `square_auxiliary_parsers`) write canonical CRDM
records into the `sales` schema. The demo merchant
(`demo-sq-farmers-market-0001`) carries about 7,300 rows over eleven
weeks — modest, but the pipeline shape is the production shape, not a
fixture. The seed reseed (`devops/seeds/level_b_demo.py --wipe`) is
idempotent and runs in roughly three seconds. Tenant scoping is enforced
via `TenantMixin` on every tenant-scoped table and row-level security in
the `app` schema.

**Enterprise bar.** Thousands of POS transactions per store per day,
continuous ingest, with retention horizons measured in years and detail
queryable for the most recent quarters. Multi-thousand-store tenants
generate millions of transactions per day; the per-tenant ingest rate
must sustain continuous burst plus catch-up after planned maintenance.

**Gap classification.** CHOICE-BY-DESIGN. The bar is met for our current
target tenant — single-store and small-multi-store specialty retailer,
roughly 50–500 transactions per store per day. The pipeline shape (HMAC
verify, idempotent stream publish, fan-out consumer groups, append-only
`sales` writes) does not change at higher rates; what changes is the
provisioning of the components. For a four-figure-store enterprise
tenant, the design supports the rate but the schema is unpartitioned and
the per-tenant retention default is 30 days. Both surface in the
retention-tiering and capacity items elsewhere in this analysis;
per-tenant volume itself is not the constraint.

### Data-model abstraction

**What we have.** The `sales` schema is the canonical relational data
model (CRDM) that Square webhooks normalize into. The TSP Sub 2 parser
(`canary/services/tsp/consumers/sub2_parse.py`) dispatches via
`webhook_dispatch.resolve_route(event_type)` to the parser suite and
writes canonical records — not Square shapes — into `sales`. The CRDM
columns are source-agnostic by design: `card_fingerprint`, `entry_method`,
`tender_type`, `business_date`, `employee_id`, `location_id`. The
`source_code` discriminator on transactions identifies which POS the
record came from. Two registry tables make the source explicit:
`app.source_systems` (PK: `code`, columns: `display_name`, `category`)
catalogs known sources; `app.merchant_sources` (`merchant_id`,
`source_code`, `raas_namespace`, `status`) records which pipes are live
for which tenant.

The `multi-pos-architecture-proof.md` SDD walks the abstraction against
two structurally different POS systems (Toast, Clover) and lands a
12-row layer scorecard: identity resolution, source registry, merchant
connection, webhook entry, signature validation, event dispatch, parser
suite, CRDM models, Chirp detection, OAuth/onboarding, initial sync,
evidence chain. Five layers are READY without code changes; one needs
generalization (event dispatch — current flat `event_type → EventRoute`
becomes compound `(source_code, event_type) → EventRoute`); five need
new code (signature validator strategy, parser suite, OAuth adapter,
initial sync adapter, plus minor `card_fingerprint` handling); one
degrades gracefully (Tier 2 Chirp rules that depend on
`card_fingerprint` lose precision when the source POS does not expose
fingerprints).

Detection (Chirp) and case management (Fox) read from `sales`, never from
Square shapes. The Chirp engine catalog (`canary/services/chirp/rule_definitions.py`)
defines 37 rules across 8 categories as frozen `ChirpRuleDefinition`
dataclass instances; rule logic queries the CRDM, not raw payloads.

**Enterprise bar.** A stable schema contract between raw, heterogeneous
POS data and the detection / case layer above it — so that a new POS
source becomes a new ETL adapter, not a refactor of the rule engine or
the case schema. The reference is a 14-store decomposition where
upstream is ETL and downstream operates on the canonical shape, with
the canonical layer carrying its own DDL and partition strategy.

**Gap classification.** MET in design and proof-of-concept. GAP on
production breadth — only Square is live in production today. The
multi-POS proof is a SDD-documented architecture validation, not a
shipped second source. Adding a second POS is a five-component sprint
per the proof's adapter pattern (auth adapter, signature validator,
event registry, parser suite, sync adapter). The first non-Square
source is the production proof; until then, the contract is documented
and structurally exercised but not commercially live. Trigger is
demand-driven, not roadmap-driven.

### Persistence decomposition

**What we have.** Three Postgres schemas inside one `canary` database:

- `app` — about 43 tables across eight domain owners. Identity (14
  tables: `organizations`, `merchants`, `merchant_settings`, `users`,
  `roles`, `user_roles`, `employees`, `locations`, `location_hierarchy`,
  `customers`, `products`, `square_oauth_tokens`, `source_systems`,
  `merchant_sources`). Chirp (2 tables: `detection_rules`,
  `merchant_rule_config`). Alerts (4 tables: `alerts`, `alert_history`,
  `notification_log`, `notification_schedule`). Owl (4 tables:
  `owl_sessions`, `owl_findings`, `owl_merchant_memory`, `owl_action_log`).
  Fox case management (7 tables: `fox_cases`, `fox_case_alerts`,
  `fox_case_timeline` with SHA-256 hash chain, `fox_case_actions`,
  `fox_evidence`, `fox_evidence_access_log`, `fox_subjects`). Webhook
  pipeline state (3 tables: `webhook_events`, `schema_fingerprints`,
  `schema_drift_alerts`). UI/BFF (5 tables: `feature_flags`,
  `merchant_feature_flags`, `app_config`, `card_profiles`,
  `blocked_entities`). RaaS (2 tables: `namespace_registrations`,
  `namespace_aliases`). Cross-cutting (2 tables: `audit_log` with
  SHA-256 hash chain, `interest_signups`).
- `sales` — about 19 tables, the canonical CRDM. Append-only with
  immutability enforced by Postgres triggers on `evidence_records`. 44
  FK constraints enforced.
- `metrics` — about 20 tables. Daily and hourly rollups, employee
  rollups, entity risk scores, baselines. Fully re-derivable from
  `sales`; never the source of truth.

Plus `growdirect_memory` (separate database, pgvector + HNSW cosine,
1024-dimension qwen3 embeddings) for the memory bus, and the in-process
session factory `get_db_session(db_name)` routes by string key
(`app`, `sales`, `metrics`, `memory`).

Valkey 8 carries sessions (DB 0, 3600s TTL), TSP event stream
(`canary:events` on DB 4, plus `canary:detection`, `canary:dead_letter`),
idempotency (DB 3, 24h TTL), threshold cache (300s TTL), velocity
counters (rule-driven TTL), rate limits (60s TTL), notification caps
(varies), Merkle-batch accumulator (`canary:batch:current`). Eight
namespaces with distinct TTLs.

Two SHA-256 hash chains — one on `audit_log`, one on `fox_case_timeline`
plus `evidence_records` — provide tamper-evident write trails on the
case-management and admin-action surfaces. No UPDATE / DELETE permitted
on either chain.

**Enterprise bar.** Logically separate stores for sales data, cases,
users, hierarchies, reporting, job system. The reference shape is a
14-store decomposition where each concern carries its own physical
store with its own access pattern, write semantics, and retention.
The point is bounded ownership and independently-scalable persistence
per concern.

**Gap classification.** MET in principle, with a deliberately smaller
surface than the enterprise reference. The 14-store decomposition is
collapsed to three Postgres schemas plus one separate memory database.
Users / hierarchies / cases live in the `app` schema together because
the SMB tenant doesn't need independent scaling between them, and one
fewer database is one fewer operational concern. The CRDM (`sales`) and
the analytics tier (`metrics`) are separated because their access
patterns and write semantics differ — append-only versus periodically-
recomputed. Job-system equivalent is the Valkey stream pipeline plus
subscriber groups; there is no separate job-DB, by choice. The
hash-chained audit and case-timeline surfaces are tamper-evident
patterns the enterprise reference also expects, kept rather than
collapsed.

### Identity federation

**What we have.** Magic-link authentication via Flask-Login is the
primary user-facing login path; password fallback exists for ops
accounts. Square OAuth is the POS-connection identity (`square_oauth_tokens`
table, access_token and refresh_token encrypted at rest with AES-256-GCM
via `canary/utils/crypto.py`, `CANARY_ENCRYPTION_KEY` env var holding a
base64-encoded 32-byte key, transparent Fernet-to-GCM migration on next
token store, hard fail in production if the key is missing). The
Identity domain (`canary/blueprints/auth.py`,
`canary/blueprints/square_oauth_wired.py`,
`canary/services/square_oauth.py`) owns merchant registration, user
authentication, RBAC (`roles`, `user_roles` with global role catalog:
admin, owner, manager, operator, member, viewer), tenant-context
injection (`g.merchant_id`, `g.user_id`, `g.roles` set by middleware).
Sessions live in Valkey-backed Flask sessions
(`SESSION_TYPE = "redis"`, Valkey-compatible). JWT middleware
(`canary/middleware/jwt_auth.py`) exposes `jwt_required`, `role_required`,
`roles_required`, `load_session_user`, `has_any_role`, with two modes —
`keycloak` (RS256 signature validation against JWKS) and `development`
(any Bearer accepted with admin role). API-key bypass (`X-API-Key`
matching `CANARY_MCP_API_KEY`) supports agent-to-agent calls inside the
mesh.

OAuth state CSRF parameter is generated on `/oauth/authorize` and
verified on `/oauth/callback` before token exchange. Token revocation
on `/oauth/disconnect` (JWT + owner/admin) calls Square's revocation
endpoint and triggers
`RaaSNamespaceResolver.disconnect_source()`.

No SAML 2.0. No OpenID Connect. No assertion-based role mapping. No
admin SCIM provisioning.

**Enterprise bar.** SAML 2.0 service-provider-initiated flow plus
OpenID Connect, with the application as the SP and the customer's IdP
as the source of truth for identity. Assertion claims carry attributes
that map to internal role names; both self-service (claim-driven) and
admin-assigned (post-bind) role paths are supported. Modern enterprise
IdPs (Okta, Azure AD, Ping, OneLogin) expect at least one of these
protocols, and IT governance treats federated identity as a buying-
criterion line item, not a feature request. Legacy on-prem identity
managers wrap into the SAML 2.0 framework as IdPs.

**Gap classification.** ROADMAP-Q1-2027 for the enterprise-tier feature.
CHOICE-BY-DESIGN for the SMB tier — the merchant-buyer profile is one
person, not an IT department, and magic-link is the right friction
profile. The buyer doesn't have a directory, doesn't have an IdP,
doesn't want to configure a service-provider metadata XML. Adding
SAML/OIDC is a tier-not-a-replacement: the SMB tier keeps magic-link;
the enterprise tier adds federated identity as an on-by-default option,
with admin-assigned role mapping as the primary configuration surface
and assertion-claim mapping for tenants that have it set up. The
Keycloak mode in JWT middleware is the seam — the same
`@jwt_required(role="admin")` decorator works whether the upstream
identity is magic-link, Keycloak, or a SAML/OIDC IdP.

### Deployment redundancy

**What we have.** Local development runs on Docker Compose (single host,
single Postgres, single Valkey, single Ollama, single Flask via
Gunicorn with 1 worker / 4 threads on port 5001). The shared infra
compose file at `~/GrowDirect/devops/docker-compose.yml` brings up
postgres (`growdirect_postgres:5432`), Valkey (`growdirect_valkey:6379`),
pgAdmin (`growdirect_pgadmin:5050`), and Ollama
(`growdirect_ollama:11434`); each app's compose file joins the shared
`growdirect` external network. Dev and QA reach the internet through
Cloudflare Tunnel — outbound-only, no inbound ports on the dev-side
router; Cloudflare handles TLS termination, DDoS protection, WAF. Dev
runs at `dev.growdirect.app` (Mac Mini, local config); QA at
`qa.growdirect.app` (iMac, token-based Docker service). Deploy scripts
(`canary_deploy.sh --full`, `remote_deploy.sh`) drive a pull-build-
migrate-test sequence and gate on test results: unit tests block
merge, integration tests block QA push, smoke tests run after every
rebuild. Three Alembic migration chains
(`canary/migrations/alembic.ini` for `app`, `canary/migrations/sales/alembic.ini`,
`canary/migrations/metrics/alembic.ini`) keep schema migrations
chain-isolated. The cloud production target is ECS Fargate. Production
today is pre-revenue; there is no current redundant tier.

**Enterprise bar.** A tiered ladder — non-redundant for development and
non-mission-critical, single-DC redundant for production with uptime
requirements (typically a primary-replica Postgres pair or always-on
group, multi-AZ application tier, replicated cache), cross-DC redundant
for production with disaster-recovery requirements (replicated VMs
across sites, cross-site availability group, single HA group spanning
DCs). The reference deployments at the largest tenants run multi-CPU
Postgres primaries with NVMe storage, fiber-channel SAN, RAID-protected
spindle arrays for IO optimization, with redundant 10GbE networking.

**Gap classification.** ROADMAP-Q3-2026 for single-DC redundancy —
primary-replica Postgres, multi-AZ ECS, replicated Valkey, multi-AZ
ALB. Tied to the first revenue tier that justifies the infrastructure
spend. ROADMAP-Q1-2027 for cross-DC redundancy — second region with
async replication, automated failover testing. Tied to the first
contract that requires it. Cloudflare Tunnel solves ingress and edge
protection, not durability or data-tier redundancy. The compose-based
shared-infra model is appropriate for development and the current
production load; the migration to a redundant production tier is a
provisioning shift, not a code rewrite.

### Self-host / VPC option

**What we have.** Canary is SaaS-only by design today. The container
layout (Flask, Postgres, Valkey, Ollama as images, plus the four TSP
consumer processes) is portable: each service is a standard image, no
proprietary runtime, no machine-bound license. The shared-infra compose
plus per-app compose pattern at `devops/docker-compose.yml` and
`Canary/devops/docker-compose.localhost.yml` is the same shape that
would land in a customer VPC. There is no published self-host
distribution, no installer, no per-customer licensing mechanism, no
in-product key custody UI, no audit-log forwarding pipeline. Encryption-
key custody is via env var (`CANARY_ENCRYPTION_KEY`) which is operator-
managed today.

**Enterprise bar.** Enterprise customers, particularly those with IT
governance constraints around data residency, vendor risk, or PII
handling, expect a self-host or single-tenant VPC option. The
expectation extends to encryption-key custody (HSM or KMS), network-
egress controls (private link or VPN-only), audit-log forwarding (SIEM
integration), and a path to break-glass administrative access that
survives a vendor outage.

**Gap classification.** ROADMAP-Q2-2027 for a private-VPC deployment
tier — a single-tenant managed install in the customer's cloud account,
managed through a control plane the customer agrees to, not a true
self-host install. The VPC tier addresses data-residency and
vendor-risk objections at lower support cost than full self-host. Full
self-host distribution (bring-your-own-Kubernetes installer, customer-
operated upgrades, customer-driven incident response) is not on the
roadmap; the support-cost economics don't fit the SMB-first business
model, and the VPC tier covers the enterprise objection set.

### Data retention tiering

**What we have.** Detail retention is per-merchant.
`merchant_settings.lookback_days` (Integer, nullable, default 30,
GRO-258) controls history-pull depth at OAuth-initial-sync time; NULL
means unlimited. The `metrics` schema holds derived rollups — daily,
hourly, employee, entity risk scores, baselines — produced by the
analytics tier and fully re-derivable from `sales`. The architectural
separation of detail (`sales`, write-once with trigger-enforced
immutability) from aggregates (`metrics`, periodically recomputable) is
in place. What isn't in place is the automated detail-rolloff job, the
aggregate-promotion job, and the per-tenant two-window configuration
surface. The audit-log and case-timeline hash chains are append-only
and have no rolloff path by design — those are evidence, not detail.

**Enterprise bar.** A two-window retention model: a detail window
(transactions queryable at line level, supporting forensic
investigation, case management, and regulator response) and an
aggregated-metrics window beyond detail expiry (where summary
statistics survive longer than the underlying line-level data, for
trend analysis and historical benchmarking). Enterprise contracts
negotiate both windows; the resolution path involves both physical
architecture (storage tiering, partition pruning) and aggregate-
strategy (which dimensions survive into the long window).

**Gap classification.** MET on architecture — the schema separation
that the two-window model requires is already in place. GAP on
operational tooling — no automated rolloff job, no aggregate-window-
versus-detail-window per-tenant configuration UI. ROADMAP-Q4-2026 for
the rolloff job, the per-tenant two-window settings on
`merchant_settings`, and the partition-pruning DDL on `sales` that
makes detail rolloff a metadata operation rather than a row-level
DELETE.

### Opinionated defaults

**What we have.** Onboarding via Square OAuth is the only path in. The
OAuth callback runs the RaaS `OnboardingCoordinator.run_inline()` —
webhook registration plus initial sync. The default Chirp ruleset (37
rules across 8 categories, sensitivity presets) is enabled out of the
box. The dashboard (BFF + Flask/Jinja2 today, Next.js target) is
pre-wired with default views. Notification frequency caps and per-category
schedules ship with sane defaults (`notification_schedule.freq_critical`,
`hourly_cap`, `daily_cap`). Owl personalities, ALX session-context, and
Fox case lifecycle are all pre-installed.

There is no kit-of-parts feel: the merchant connects Square and lands
on `/home` with everything wired.

**Enterprise bar.** Pre-wired install, not a kit of parts. The reference
is a consolidated build artifact that ships features, dashboards,
reports, and searches working together on a common foundation, so the
implementation labor is configuration, not integration.

**Gap classification.** MET. The opinionated-defaults posture is one of
Canary's stronger choices and aligns directly with the enterprise
delivery-philosophy that every optional configuration step costs labor.

### Rule tuning for retailer patterns

**What we have.** The Chirp engine
(`canary/services/chirp/rule_engine.py` plus
`canary/services/chirp/stateless_engine.py`) evaluates 37 detection
rules across three tiers:

- Tier 1 (stateless) — six rules in `stateless_engine.py`, no DB access,
  pure-function evaluation: C-004, C-007, C-009, C-010, C-011, C-502.
- Tier 2 (lightweight) — nine rules using Valkey velocity counters for
  windowed aggregation.
- Tier 3 (full DB) — fourteen rules running SQLAlchemy queries against
  the `sales` schema for cross-entity correlation.

Categories: payment (C-001 through C-011), cash_drawer (C-101–C-104),
order (C-201–C-204), timecard (C-301–C-303), void (C-501, C-502),
gift_card (C-601, C-602), loyalty (C-801–C-804). Six critical-severity
rules auto-create Fox investigation cases on fire (C-009, C-104, C-204,
C-301, C-502, C-602).

Per-merchant tuning lives in `merchant_rule_config` — `is_enabled`
(per-rule on/off), `custom_threshold` (override the default in
`detection_rules.default_threshold`), `notify_enabled` (per-rule
notification toggle, GRO-254). Threshold resolution is cached in Valkey
(`chirp:thresholds:{merchant_id}:{rule_id}`, 300-second TTL); velocity
counters live under
`chirp:velocity:{merchant_id}:{rule_id}:{window}` with rule-driven TTL.
Sensitivity presets give a UX-grade abstraction over individual
threshold values; templates apply preset bundles to all rules in one
write. Cache invalidation is hooked to config writes and deletes via
`canary/services/chirp/threshold_manager.py`. The
`canary-chirp` MCP server exposes 10 tools for programmatic rule
configuration and inspection. Sensitivity preview, validate-before-save,
and per-rule estimate APIs ship in `canary/blueprints/chirp_wired.py`
under `/api/chirp/*` (JWT + admin/owner).

**Enterprise bar.** A per-customer tunable rule engine, where retailer-
specific patterns (a category that always carries high-discount lines,
a register layout that produces frequent voids, a department-level
manual-entry exception) can be tuned without custom code. The reference
model is rule packs plus per-customer overrides plus suppression lists,
all configurable through admin UI rather than support engineering.

**Gap classification.** MET. The Chirp model maps directly to the bar.
What is not in production today is a rule-pack-by-vertical concept
(grocery pack vs specialty-retail pack vs F&B pack) — but the per-rule
configurability, the threshold cache, the sensitivity-preset abstraction,
and the validate-before-save flow are all in place. Vertical packs are
an SKU-and-defaults exercise, not an engine change. Suppression lists
have an analogue in `blocked_entities` (merchant-blocked cards,
customers, employees) which Chirp consults during evaluation.

### Delivery organization scale

**What we have.** No delivery organization. Canary's go-to-market is
self-serve onboarding through Square OAuth — the merchant clicks
"Connect with Square" on the landing page, completes the OAuth flow,
and lands on `/home` with the demo or live data depending on environment.
There is no implementation engagement, no kickoff meeting, no resource
plan, no Gantt. Pricing is monthly subscription tiers in the four-figure
annual range targeted at SMB unit economics.

**Enterprise bar.** Enterprise-tier deployments at six-figure first-year
subscription, four-to-six-month implementation windows, dedicated account
manager, third-line 24/7 help desk, integration consulting hours, onsite
training. The SMB / mid-market / enterprise split is a tier-and-buying-
motion split, not a feature split.

**Gap classification.** CHOICE-BY-DESIGN. The SMB-self-serve buying motion
is the deliberate positioning, and it implies a different cost structure
than enterprise. The enterprise delivery shape is on the roadmap as a
separate tier, not as a replacement for the self-serve motion. The
question for the enterprise tier is when, not whether — and the answer
is when the first prospect with the budget shape is in the pipeline,
not before.

### Adjacent-module pricing

**What we have.** The core product is loss prevention via Chirp + Fox.
Adjacent code surface in the repository:

- Goose — account/credit/L402 payment middleware (Strike, Lightning).
  Live code, not commercially priced today.
- Owl — AI-merchant-assistant with retail intelligence; ships as part
  of the core product UX.
- Atlas, Condor, ALX, RaaS — internal mesh / observability / namespace
  / memory-bus services; not separately priced.

Subscription is single-bundle today.

**Enterprise bar.** A core product (in the reference, point-of-sale
exception-based reporting) plus adjacent modules (DSD analytics,
pharmacy, eCommerce, audit-and-survey, refund management) at independent
pricing — the core gets the deep discount, adjacent modules carry their
own pricing because they extend into adjacent operating surfaces.

**Gap classification.** ROADMAP-Q3-2026 for the first adjacent-module
SKU separation, conditional on which module ships next as a discrete
buyer-facing product. The architecture supports it (each module is a
bounded context with its own MCP server); the commercial structure
isn't there yet because there isn't a second product to price.

## What the SMB-first choice means

Three of the dimensions above are CHOICE-BY-DESIGN, not GAP, and they
deserve to be named clearly so the framing isn't ambiguous.

**Magic-link auth, not SAML / OIDC.** The SMB merchant is one person,
typically the owner. Magic-link via Flask-Login is the right friction
profile — no password to forget, no IdP to configure, and the buyer
profile doesn't have an IT department to evaluate the federation
question. Adding SAML and OIDC for the enterprise tier is on the
roadmap, but it is additive, not a replacement. The SMB tier keeps
magic-link.

**Single-instance Postgres, not redundant tier ladder.** The SMB
total-cost target makes a primary-replica Postgres pair an inappropriate
baseline. The architecture supports horizontal scale-out (Valkey-streamed
multi-subscriber pipeline, three-schema separation, fully-derivable
metrics tier) without a rewrite. The deployment shape changes when the
revenue tier justifies the operational cost — not before.

**Self-serve onboarding, not implementation engagement.** The Square
OAuth callback runs the entire onboarding pipeline inline. No kickoff
meeting, no resource plan, no Gantt. This is the deliberate cost
structure of an SMB-self-serve buying motion. The enterprise delivery
shape (six-figure first-year subscription, four-to-six-month
implementation, dedicated account manager) is a separate tier on the
roadmap, not a replacement for self-serve.

These choices are coherent with each other. They follow from a single
positioning decision — the buyer is the merchant owner, not the IT
department — and they would be wrong choices if the positioning were
different.

## What the roadmap closes

The GAP-classified dimensions and their target windows.

**Q3 2026.**
- Adjacent-module pricing — first SKU separation, dependent on which
  adjacent module ships next as a discrete commercial product.
- Single-DC redundancy — primary-replica Postgres, multi-AZ ECS,
  replicated Valkey. Triggered by the first revenue tier that justifies
  the infrastructure spend.

**Q4 2026.**
- Aggregate transaction volume — capacity-validation pass on the Valkey
  stream pipeline, partitioning the `sales` schema, provisioning the
  read-replica path. Load testing at multi-million-transactions-per-day
  aggregate.
- Data retention tiering — automated detail-rolloff + aggregate-promotion
  job, per-tenant two-window retention configuration.

**Q1 2027.**
- Identity federation — SAML 2.0 + OpenID Connect for the enterprise
  tier. Keycloak mode in JWT middleware is the seam. Magic-link
  remains the SMB-tier default.
- Cross-DC redundancy — second site, replicated availability group.
  Triggered by the first contract that requires it.

**Q2 2027.**
- Self-host / VPC option — single-tenant managed install in the
  customer's cloud account. Not full self-host distribution; the VPC
  tier is the answer to the data-residency question.

**No current commitment.**
- Full self-host distribution (bring-your-own-Kubernetes installer).
  Out of scope; the VPC tier covers the data-residency case at lower
  support cost.
- Multi-POS production breadth — second POS source is engineering work
  whose timing is demand-driven, not roadmap-driven. The architecture
  is ready (the multi-POS proof SDD); the trigger is a customer or a
  partnership.

## Reading guide for the partner

This document is a forward-honest read of where Canary stands relative
to the enterprise-retail-LP bar. It is not a feature roadmap and not a
defense. The dimensions are calibrated against an explicit reference
shape — tiered redundant deployment, federated identity, six-figure
implementation engagement, TB-scale repository — and the gaps are
either named with a quarter target or named as choices with a stated
reason. The point of the artifact is to give a technical partner the
real surface to react to. Where we say MET, we mean it; where we say
ROADMAP, we mean we plan to close it; where we say CHOICE-BY-DESIGN, we
mean we will not close it for the SMB tier and we will close it as a
separate tier when the enterprise tier ships. None of the three
positions is a hedge.
