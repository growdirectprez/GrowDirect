# Atlas View — Deployment Posture Decision Brief
**INTERNAL · 2026-05-05**

---

## The Problem

The Brand Guide makes three claims that require infrastructure to be true. Without it, they are marketing copy.

| Brand Claim | What It Requires |
|---|---|
| "Listening Systems that keep the operating model intelligent" | Compute that runs continuously. Not a spreadsheet. A scheduler, a data store, a wire substrate. |
| "We invoice when the cost line moves" | A baseline captured before work starts, a diff engine comparing after, and an audit trail that survives the engagement. |
| "We agree the baseline before any work starts" | A structured artifact stored, versioned, and queryable. A schema-fragment in AlloyDB, not a slide. |

If Ruptiv delivers on these claims without infrastructure, it does it manually — which means it cannot scale, cannot compound, and cannot prove the outcome to a skeptical CFO.

---

## Deployment Options

| Option | What It Is | Pros | Cons |
|---|---|---|---|
| **A — GrowDirect SaaS** | Shared GCP project; all engagements run on a single AlloyDB + Cloud Run stack | Cheapest to operate. Patterns index compounds across all clients. Fastest to stand up. | Ruptiv carries the security posture. Client data co-mingled (schema isolation, not tenant isolation). Procurement friction at enterprise clients. |
| **B — Customer GCP** | Deploy Atlas View into the client's own GCP project for each engagement | Clean data residency. No Ruptiv infra costs for that engagement. Enterprise-friendly. | Ruptiv loses the Patterns index (cross-engagement compounding breaks). Each engagement is an island. Deployment overhead per client. |
| **C — Hardened Workstation** | AlloyDB-local equivalent (Postgres + pgvector on a MacBook Pro); no cloud | Zero cloud spend. Works air-gapped. Fully portable — carry it on the plane. | No Listening System heartbeat (laptop has to be open). No cross-engagement index. Data dies when the workstation dies unless explicitly synced. |

---

## Decision

**Two-tier posture: GrowDirect control plane + portable execution tier.**

| Tier | Where It Lives | What It Holds |
|---|---|---|
| **Control Plane** | GrowDirect GCP (shared, always-on) | Patterns index only. Cross-engagement synthesis. Imprint registry. No raw engagement data. |
| **Execution Tier** | Per-engagement: customer GCP preferred, workstation fallback | Fragment store. Vault. Listening System heartbeats. Transcript + schema-fragment records for that engagement. |

**Why this works:**
- The Patterns index is the compounding moat. It must live on a persistent surface GrowDirect controls. It only holds abstract patterns — no client-identifiable data.
- Raw engagement data (fragments, transcripts, decisions) stays in the client's perimeter. Customer GCP is the target; workstation is acceptable for Phase 1 or air-gapped clients.
- Ruptiv never co-mingles raw client data across engagements. The Patterns index is the only cross-engagement write surface, and it holds only synthesized abstractions.

---

## Minimum Viable Footprint

**Control Plane (GrowDirect GCP) — always running:**
- AlloyDB Serverless (non-prod) → ~$30-50/month while no active synthesizer jobs
- Cloud Run (Synthesizer imprint) → zero when idle
- Pub/Sub (pattern event bus) → negligible
- **Total holding cost: ~$50/month**

**Per-Engagement Execution — stood up at engagement start:**
- Option 1: Customer's GCP project — Ruptiv deploys AlloyDB + Cloud Run + Scheduler; client pays the bill
- Option 2: MacBook Pro running Postgres + pgvector (Docker) — zero cloud cost; works anywhere
- Engagement teardown: fragment store exported to cold archive (BigQuery or GCS), workstation wiped

**Travel kit for Option 2:**
- MacBook Pro M-series (32GB RAM minimum)
- Docker Desktop running: postgres:17-pgvector, cloud-run-emulator, ollama (text-embedding-005 or local equivalent)
- One-command engagement bootstrap: `make engagement-init SLUG=clientname-2026-Q2`

---

## What GrowDirect Owns vs. What Ruptiv Owns

| Component | Owner | Rationale |
|---|---|---|
| Atlas View substrate (AlloyDB schema, Cloud Run services, imprint format) | GrowDirect | Core IP. The technical substrate. |
| Patterns index (cross-engagement compounding) | GrowDirect | Compounds across every Ruptiv engagement. This is the moat. |
| Engagement execution (per-client fragment store, vault, Listening System) | Ruptiv (delivered to client perimeter) | Client data stays in client's hands. |
| Method, Sparring Partner definitions, Five-D System | Ruptiv | Methodology IP. GrowDirect implements; Ruptiv defines. |
| Brand surface (Atlas View UI, Sparring Partner cards) | Ruptiv brand-compliant; GrowDirect built | Deep Ink ground. Signal Yellow active nodes. Per Brand Guide. |

---

## Decision Gate

Before Phase 1 engagement, answer these two questions:

1. **Is the client GCP-capable?** → Yes: deploy into their project. No: use workstation tier.
2. **Is the client air-gapped or high-security?** → Yes: workstation only, no control plane sync. No: sync pattern abstractions to control plane after engagement closes.

No other decisions are required. The architecture handles both paths.

---

*Companion to: `docs/superpowers/specs/2026-05-05-ruptiv-atlas-view-substrate-architecture.md`*
