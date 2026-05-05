---
classification: internal
type: wiki
sub-type: decision
status: approved
date: 2026-05-04
last-compiled: 2026-05-04
needs-review: 2026-06-04
engines: [platform, substrate]
companion: Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md
owner: ALX
---

# Decision — GrowDirect as Ruptiv Architecture Platform

## What was decided

GrowDirect's architecture is the technical substrate that Ruptiv's End-to-End Workflow Disruptor methodology runs on. The platform is generic — not retail-specific, not domain-specific. Any Ruptiv vertical engagement deploys against the same substrate.

This is a structural commitment, not a roadmap item. It changes what gets built next and why.

## The two layers

| Layer | Entity | What it is |
|---|---|---|
| Methodology | Ruptiv | Five-D System · Listening Systems · Sparring Partners · Responsive Framework (Tim Mooney IP) |
| Platform | GrowDirect | Agent PMO · memory bus · imprint authoring · tenant deployment · MCP-native connector substrate · blockchain anchor |

The layers are distinct. Ruptiv sells the methodology and holds the client relationship. GrowDirect provides the execution infrastructure. Neither layer can be collapsed into the other.

## What changes

**Before:** Platform built for Canary retail. Architecture decisions driven by NCR Counterpoint integration and SMB store ops.

**After:** Platform built generically. Canary retail is Ruptiv Retail Studio — one vertical application of the substrate. The substrate serves any domain Ruptiv enters (Retail first, then Finance, Healthcare, Supply Chain per the Blue Ocean positioning).

The open engineering items from the prior session are now the priority build — in this order:

1. Imprint authoring framework (JSON Schema validators + runtime loader)
2. Tenant-scoped memory bus (per-engagement deployment of `services/memory-bus`)
3. Customer-side connector library (read-only first, bidirectional write architecture)
4. Engagement console (Cloud Run web UI — fleet status, findings rate, open decisions, audit trail)
5. Per-engagement Terraform module (GCP project, IAM, Workload Identity, Agent Engine, Secret Manager)

These are not Canary features. They are substrate components that every Ruptiv engagement instance requires.

## What does not change

The Canary Go retail build continues. The RapidPOS channel is the first live vertical. The retail domain knowledge in `Brain/wiki/cards/` remains accurate and applicable. Store ops capability model, GSLM, ILDWAC, accountability rails — none of this is discarded.

Retail is where the substrate proves itself. The platform earns the right to generalize by shipping one vertical correctly.

## The Responsive Framework relationship

Tim Mooney's Responsive Framework is the diagnostic foundation Ruptiv operates from. It is Ruptiv-published IP. The Five-D System and the Listening Systems surface-expose its six-element structure.

The substrate does not own or replicate the Framework. The substrate executes against it. Imprints are authored to Framework elements. Findings are indexed by Framework facet. The schema-fragment synthesis composes against Framework structure.

The relationship is: Framework defines what to measure. Substrate executes the measurement. Ruptiv synthesizes and invoices the result.

## Baseline (Five-D: Diagnose)

Agreed before further build:

- **What is being measured:** Cost line movement in enterprise workflows redesigned from headcount-executed to agent-executed
- **How savings are measured:** Baseline established in Diagnostic Engagement before Sparring Partners are built. Metric agreed bilaterally. Invoice follows documented movement.
- **Where GrowDirect's architecture enters:** The substrate executes the Diagnostic Listening System. It does not define the method. It does not hold the client relationship. It does not set the commercial terms.

## Constraints

- The substrate never touches card data, PII in cleartext, or regulated data outside the connector boundary. The merchant holds the encryption key. Canary/GrowDirect holds ciphertext only.
- The substrate remains cloud-agnostic in architecture even if GCP is the deployment target. No GCP-proprietary lock-in at the imprint or bus layer.
- Vertical-specific knowledge (retail domain, audit control libraries) lives in vertical-scoped imprint catalogs, not in the generic substrate. The substrate does not know what it is running.

## Decision authority

Founder. Recorded here. No further approval required.

## References

- Ruptiv Positioning IM v5: `Brain/raw/inbox/Screenshot 2025-06-27 at 3/Ruptiv Positioning IM v5.docx`
- Ruptiv Blue Ocean Strategy IM v6: `Brain/raw/inbox/Screenshot 2025-06-27 at 3/Ruptiv Blue Ocean Strategy IM v6.docx`
- Ruptiv Brand Guide IM v5: `Brain/raw/inbox/Screenshot 2025-06-27 at 3/Ruptiv Brand Guide IM v5.pdf`
- Ruptiv Naming Architecture IM v4: `Brain/raw/inbox/Screenshot 2025-06-27 at 3/Ruptiv Naming Architecture IM v4.docx`
- Substrate artifact taxonomy: `Brain/wiki/cards/ruptiv-diagnostic-artifact-taxonomy.md`
- Substrate imprint header spec: `Brain/wiki/cards/ruptiv-diagnostic-imprint-header-spec.md`
- Prior session handoff: `Brain/dispatches/2026-05-04-decision-substrate-handoff.md`
