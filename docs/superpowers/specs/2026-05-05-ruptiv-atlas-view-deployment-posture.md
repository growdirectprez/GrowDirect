# Atlas View — Deployment Posture
INTERNAL BRIEF · 2026-05-05

Three brand claims require infrastructure to be true. Without it, they are marketing copy.

---

## THE PROBLEM

| Brand Claim | What It Requires |
|---|---|
| "Listening Systems that keep the operating model intelligent" | Compute that runs continuously. A scheduler, a data store, a wire substrate. Not a spreadsheet. |
| "We invoice when the cost line moves" | A baseline captured before work starts. A diff engine comparing after. An audit trail that survives the engagement. |
| "We agree the baseline before any work starts" | A structured artifact stored, versioned, and queryable. A schema-fragment in AlloyDB, not a slide. |

Deliver these claims manually and Ruptiv cannot scale, cannot compound, and cannot prove the outcome to a skeptical CFO.

---

## DEPLOYMENT OPTIONS

| Option | What It Is | Pros | Cons |
|---|---|---|---|
| **A — GrowDirect SaaS** | Shared GCP project; all engagements run on a single AlloyDB + Cloud Run stack | Cheapest to operate. Patterns index compounds across all clients. Fastest to deploy. | Ruptiv carries the security posture. Client data co-mingled (schema isolation, not tenant isolation). Procurement friction at enterprise clients. |
| **B — Customer GCP** | Deploy Atlas View into the client's own GCP project per engagement | Clean data residency. No Ruptiv infra costs. Enterprise-friendly. | Patterns index breaks. Each engagement is an island. Deployment overhead per client. |
| **C — Hardened Workstation** | Postgres + pgvector on MacBook Pro; no cloud | Zero cloud spend. Works air-gapped. Fully portable. | No Listening System heartbeat without the laptop open. No cross-engagement index. Data requires explicit sync or it is lost. |

---

## DECISION

**Two-tier posture: GrowDirect control plane + per-engagement execution tier.**

| Tier | Where It Lives | What It Holds |
|---|---|---|
| **Control Plane** | GrowDirect GCP (shared, always-on) | Patterns index only. Cross-engagement synthesis. Imprint registry. No raw engagement data. |
| **Execution Tier** | Per-engagement: customer GCP preferred, workstation fallback | Fragment store. Vault. Listening System heartbeats. Transcript and schema-fragment records for that engagement. |

The Patterns index is the compounding moat. It must live on a surface GrowDirect controls. It holds abstract patterns only — no client-identifiable data.

Raw engagement data stays in the client's perimeter. Customer GCP is the target. Workstation is acceptable for Phase 1 or air-gapped clients.

Ruptiv never co-mingles raw client data across engagements. The Patterns index is the only cross-engagement write surface.

---

## DEPLOYMENT FOOTPRINT

**Control Plane (GrowDirect GCP) — always running:**
- AlloyDB Serverless (non-prod) → ~$30-50/month while no active synthesizer jobs
- Cloud Run (Synthesizer imprint) → zero when idle
- Pub/Sub (pattern event bus) → negligible
- **Total holding cost: ~$50/month**

**Per-Engagement Execution — deployed at engagement start:**
- Option 1: Customer's GCP project — Ruptiv deploys AlloyDB + Cloud Run + Scheduler; client pays the bill
- Option 2: MacBook Pro running Postgres + pgvector (Docker) — zero cloud cost; works anywhere
- Engagement teardown: fragment store exported to cold archive (BigQuery or GCS), workstation wiped

**Travel kit (Option 2):**
- MacBook Pro M-series, 32GB RAM minimum
- Docker: postgres:17-pgvector, cloud-run-emulator, ollama (text-embedding-005 or local equivalent)
- One-command bootstrap: `make engagement-init SLUG=clientname-2026-Q2`

---

## ARCHITECTURE LAYERS

| Layer | What It Is | Where It Lives |
|---|---|---|
| Atlas View substrate | AlloyDB schema, Cloud Run services, imprint format | GCP control plane |
| Patterns index | Cross-engagement synthesis. The compounding surface. | GCP control plane — persistent |
| Engagement execution | Fragment store, vault, Listening System heartbeats | Client perimeter — per engagement |
| Method layer | Five-D System, Sparring Partner definitions, Listening System logic | Delivered as imprints at engagement start |
| Brand surface | Atlas View UI, Sparring Partner cards | Deep Ink ground. Signal Yellow active nodes. Per Brand Guide. |

---

## DECISION GATE

Two questions at engagement start. No other decisions required.

1. **Is the client GCP-capable?** → Yes: deploy into their project. No: workstation tier.
2. **Is the client air-gapped or high-security?** → Yes: workstation only, no control plane sync. No: sync pattern abstractions to control plane after engagement closes.

---

*Companion to: `docs/superpowers/specs/2026-05-05-ruptiv-atlas-view-substrate-architecture.md`*
