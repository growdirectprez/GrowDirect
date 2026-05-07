# GCP Onramp Architecture — RapidPOS LLC (Demo Run)

> **DEMO RUN — derived from cost-model GCP workload blueprint at T0→T1 baseline.**

**Vendor:** RapidPOS LLC
**Run date:** 2026-05-03
**Phase:** 2 — Audit-as-diligence
**Target architecture:** Canary.GO + DriftPOS, hosted on GCP, ramped from T0 (RapidPOS today) to T1 (eager-cohort migrated) over 12 months

---

## Architecture overview

The proposed architecture follows the 18-workload blueprint. Each workload sized for T1 (eager-cohort migrated; ~3,500 stores aggregate; mid-7-figures txn/day). T2/T3 capacity expansion happens in months 18+ as the cohort migration completes and new-logo enterprise wins land.

### Foundational layer — GCP Organization

- **GCP Organization:** Growdirect parent + RapidPOS sub-org (or shared, depending on M&A structure)
- **Folder hierarchy:** `prod` / `nonprod` / `audit` / `shared-services`
- **Project structure per tenant:** one project per merchant for hard isolation; shared `shared-services` project for the agentic ops fabric and telemetry sinks
- **Identity:** Cloud Identity (or Workspace) for staff; Identity Platform for customer-facing auth
- **IAM model:** Group-based; least-privilege defaults; PAM for break-glass

### POS adapter ingress (workload #1)

Five front-ends interchangeable. At T1 the active mix is:
- DriftPOS (.NET) — GKE Autopilot + Pub/Sub topic `pos-driftpos`
- Counterpoint via RapidPOS (HTTP poll) — Cloud Run jobs + Pub/Sub topic `pos-counterpoint`
- Square (webhook) — Cloud Run service + Pub/Sub topic `pos-square` (legacy customers if any)
- Toast / Clover — adapters available, not deployed unless RapidPOS customer requests

Sizing: 12 vCPU GKE / 24 GB / 5 topics / 2 MB/sec Pub/Sub throughput aggregate.

### Transaction streaming pipeline (workload #2)

Pub/Sub fanout → Memorystore Valkey (ordering + dedup) → GKE workers (parsing + CRDM event production).

T1 sizing: Memorystore Standard 5GB HA, GKE workers 24 vCPU / 48 GB.

### CRDM canonical store (workload #3)

T0-T1: **Cloud SQL for PostgreSQL**, 16 vCPU / 64 GB / 2 TB SSD HA + 1 read replica.

Multi-tenant via per-tenant schemas. Plan migration to AlloyDB at T2 when write throughput exceeds Cloud SQL comfort zone.

### ILDWAC service (workload #4)

T1: Cloud SQL PG 8 vCPU / 32 GB / HA + Pub/Sub change-feed (0.5 MB/sec) + GKE pods 8 vCPU / 16 GB.

Patent-protected; deployed in a tightly-scoped IAM perimeter.

### RIB batch + blockchain anchor (workload #5)

T1: 24-96 Cloud Run jobs/day, 200 GB Cloud Storage seal archives, 15-min anchor frequency.

Bitcoin anchoring via managed gateway (Strike or similar; see `cost-model` snapshot).

### Hawk — case management (workload #6)

T1: GKE 8 vCPU / Cloud SQL PG 8 vCPU HA / 500 GB GCS evidence storage.

Hash-chained evidence chain — INSERT-only tables with trigger-enforced integrity.

### Owl — search + RAG (workload #7)

T1: Vertex AI Search (50 QPS) + pgvector on AlloyDB (eventually) for vector search.

### LLM inference (workload #8)

T1: ~100M tokens/day across the customer base. Mix: 80% Haiku / 15% Sonnet / 5% Opus. Spend ~$10k-30k/month.

Vertex AI / Anthropic-on-Vertex. Enterprise commitment for the discount.

### Edge agent (workload #9)

T1: ~1,000 edge nodes (one per migrated customer store). Anthos at the edge.

Local Haiku-class model for sub-100ms in-store decisions; cloud sync 15-min cadence.

### Identity / auth / per-tenant config (workload #10)

T1: GKE 4 vCPU / Cloud SQL HA 4 vCPU / Secret Manager (~5k secrets).

### Notifications / messaging (workload #11)

T1: Pub/Sub + Cloud Tasks + SendGrid Pro + Twilio (~10k SMS/day at peak).

### Reporting / BI / analytics (workload #12)

T1: BigQuery 10 TB storage / 500-slot reservation / Looker (100 users).

### Object / evidence storage (workload #13)

T1: 1 TB Standard / 5 TB Nearline / 10 TB Archive.

### Security & audit (workload #14) — the ISMS evidence layer

- **Security Command Center Premium** — continuous compliance monitoring
- **Cloud Audit Logs** — full data-access logs, sinked to GCS Coldline for 7-year retention
- **Chronicle Standard** — SIEM for the ISMS evidence trail
- **VPC Service Controls** — perimeter enforcement around CRDM + ILDWAC + Hawk

This is the workload that produces the audit evidence ISO 27001 + SOC 2 Type II will need. Stand it up early in Phase A.

### DR / backup / cross-region (workload #15)

T1: regional HA Cloud SQL + 30-day backups + cross-region read replica for the analytics tier.

### Networking / interconnect (workload #16)

T1: VPC + Cloud Armor managed rules + Cloud Load Balancing 10k TPS. No dedicated interconnect at T1.

### Tax & regulatory compliance service (workload #17)

T1: 51 Cloud Run jobs (federal IRS + 50 state DORs) + state regulatory body pollers + 500 forms in library + 5k rules in cache.

This workload is the same cost at T0/T1/T2 — constant-cost dominated. It's the compliance moat the cost-model surfaces as a competitive differentiator vs. Avalara-paying incumbents.

### Agentic ops fabric — A1-A5 (workload #18)

T1: ~5k agent attempts/day. Vertex AI model serving + Cloud Run agent runtimes + Pub/Sub event triggers + Cloud SQL for state + Cloud Storage for wiki/playbook output.

This is the workload that absorbs the seller-team support queue and converts it into wiki/playbook capital.

## Per-workload sizing summary at T1

| Workload | T1 monthly cost (placeholder) |
| --- | --- |
| 1. POS adapter ingress | $1,500 |
| 2. TSP | $1,200 |
| 3. CRDM (Cloud SQL HA) | $3,500 |
| 4. ILDWAC | $1,000 |
| 5. RIB + anchor | $600 |
| 6. Hawk | $900 |
| 7. Owl | $1,500 |
| 8. LLM inference | $20,000 |
| 9. Edge agent | $5,000 |
| 10. Identity | $700 |
| 11. Notifications | $1,500 |
| 12. Reporting | $3,000 |
| 13. Storage | $500 |
| 14. Security & audit | $2,500 |
| 15. DR / backup | $1,000 |
| 16. Networking | $1,500 |
| 17. Tax / compliance | $1,800 |
| 18. Agentic ops | $8,000 |
| **TOTAL T1 monthly** | **~$55,700** |

Annualized T1: ~$668k. The cost-model cross-foots this into the `program_cost` tab.

## Architecture decisions worth flagging

### What we do at T1

- **Multi-tenant via per-tenant projects** for hard data isolation (vs. shared schemas with row-level security). Costlier in GCP project sprawl but materially safer for ISO 27001 5.23 (cloud governance) and 8.22 (network segregation).
- **Cloud SQL → AlloyDB at T2.** Defer AlloyDB until throughput requires it; Cloud SQL is cheaper at T0-T1 and the migration is straightforward.
- **Vertex AI Search + pgvector hybrid for Owl** until query volume justifies dedicated Vector Search at T2.
- **GKE Autopilot, not Standard.** Autopilot's per-pod billing is more predictable for the SMB-customer-mix workload shape; Standard's cluster-fee economics work better at T2+.
- **Cloud Run for batch jobs (RIB, tax pollers).** Lower cold-start tax than GKE for low-frequency work.

### Where third-party tooling enters

- **EDR (8.7):** CrowdStrike or SentinelOne for endpoints (RapidPOS office + remote staff).
- **Vulnerability depth (8.8):** Wiz or Snyk on top of Container Analysis.
- **GRC dashboards (5.36):** Vanta or Drata for the ongoing-compliance evidence layer (also accelerates SOC 2 Type II).
- **Email (workload #11):** SendGrid (third-party).
- **SMS/voice (workload #11):** Twilio (third-party).
- **Bitcoin anchor gateway (workload #5):** Strike or similar managed LN provider.

### What we do NOT do

- **Dedicated interconnect at T1.** Customer demands at this scale don't require it; defer to T2 for any specific enterprise-customer requirement.
- **Multi-region active-active.** Premature for SMB customers; revisit at T3 anchor-account level.
- **Self-hosted observability (Prometheus/Grafana).** GCP-native monitoring + Chronicle is sufficient through T2.

## Cost-model linkage

The 18-workload sizing flows directly into `02-cost-model-output.xlsx::gcp_infra` tab. T1 monthly aggregate ≈ $55,700 is what the model uses for its T1 column.

## Open questions for Phase 2 refinement

- What are RapidPOS's customer-side contractual obligations on data residency? (Some specialty retail customers may insist on US-only data — affects multi-region strategy)
- Does any RapidPOS customer require dedicated VPC peering or interconnect that would shift workload #16 sizing?
- Bart's team has decided on .NET Framework vs .NET Core for DriftPOS adapters — answers whether GKE supports natively or needs Windows containers
- Is there a contractual or regulatory reason to use a specific GCP region (e.g., us-central1 for Iowa-based customers, us-east1 for east-coast customers, multi-region from start)?

## Cross-references

- `crb-skills/cost-model/reference/03-gcp-workload-blueprint.md` — the load-bearing 18-workload reference
- `crb-skills/cost-model/reference/04-gcp-pricing-snapshot-2026-05-03.md` — current SKU pricing
- `crb-skills/saas-acquisition-diligence/reference/03-gcp-control-mapping.md` — ISO 27001 → GCP service mapping per control
- `Brain/cost-models/rapidpos/02-cost-model-output.xlsx::gcp_infra` — costed view of this architecture
