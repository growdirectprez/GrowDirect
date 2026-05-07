# Day-1 Agentic Ops Plan — RapidPOS

> A1-A5 deployment plan for the first 90 days post-close.

**Vendor:** RapidPOS LLC
**Phase:** A (months 0-6)
**Run date:** 2026-05-03

---

## A1 — Support-queue burndown

**Mission:** Triage every open ticket. Attempt auto-resolution against the contextual wiki. Cluster the residue. Escalate only the genuinely novel issues to the human team.

**Dispatch type:** Continuous, queue-driven.

**Owner:** Growdirect agent ops + RapidPOS senior support engineer (joint).

**Deployment week:** 2 (after initial wiki seeding from existing RapidPOS documentation).

**Scaling:**
- Day 1: monitoring mode (read-only). Builds a baseline of ticket categories.
- Week 2: triage mode (categorize + suggest resolution; human still resolves).
- Month 1: assisted-resolution mode (proposes a resolution; human reviews + sends).
- Month 2: auto-resolution mode for high-confidence categories.
- Month 3: 30-50% of incoming tickets auto-resolved without human touch.
- Month 6: 50-70% auto-resolution rate.

**KPIs:**
- Auto-resolution rate (target 50% by M3, 70% by M6)
- Mean time to first response (target <30 min)
- Customer satisfaction on auto-resolved tickets (>4.0/5 baseline)
- False-positive rate (auto-resolved tickets that re-open) (<5%)

**Failure modes to monitor:**
- Confidence threshold drift (auto-resolving tickets that should escalate)
- Wiki staleness (auto-resolutions referencing outdated info)
- Customer-perception regression (loss of "personal touch" feel)

## A2 — Root-cause analysis

**Mission:** Cluster recurring tickets by symptom and underlying cause. Surface the top 10 repeat-causes. Drive each one to a permanent fix or to a runbook.

**Dispatch type:** Weekly + on-spike.

**Owner:** Growdirect agent ops + RapidPOS engineering lead (joint).

**Deployment week:** 2.

**Scaling:**
- Week 2: first weekly report (categorical clustering only).
- Month 1: top-10 repeat-cause list with symptom→cause mapping.
- Month 3: permanent-fix work-items for top repeat causes; A3 articles for the rest.
- Month 6: monthly trend analysis showing reduction in top-10 cause volumes.

**KPIs:**
- Top-10 repeat-cause volume reduction month-over-month (target -15% by M3, -40% by M6)
- Time from cluster identification to permanent fix or runbook (target <2 weeks)
- Number of permanent fixes shipped (target 5 by M3, 15 by M6)

## A3 — Contextual-wiki builder

**Mission:** Every resolved ticket → wiki article. Every recurring config → playbook. Every undocumented customization → captured fact. Build the wiki the seller never had time for.

**Dispatch type:** Continuous, ticket-resolution-driven.

**Owner:** Growdirect agent ops + RapidPOS senior engineer (knowledge owner).

**Deployment week:** 1 (start seeding from existing docs immediately).

**Scaling:**
- Week 1: seed from existing RapidPOS internal docs (whatever exists — typically email threads, Confluence, file-share documents).
- Week 2-4: write articles from resolved-ticket data + senior-engineer interviews.
- Month 1-3: wiki coverage reaches 30% of incoming-ticket types.
- Month 3-6: wiki coverage reaches 60-80%.
- Ongoing: every resolved ticket evaluated for wiki-article potential.

**KPIs:**
- Wiki articles per week (target 50/week initially, 20/week steady-state)
- Wiki-coverage rate (% of incoming tickets where wiki has a relevant article) — target 30% by M3, 60% by M6
- Article quality score (1-5 rated by senior engineers + customer feedback) (target >3.5)
- Tribal-knowledge capture rate (interviews completed; topics covered)

**Quality gates:**
- New articles reviewed by a senior engineer before going live
- Articles flagged stale after 6 months without verification
- Articles tagged by vertical (garden / gun / wine / specialty food / feed-and-tack)

## A4 — Cloud-onboarding process capture

**Mission:** Ride along on every customer cloud-migration. Capture the seller team's actual config moves, the gotchas, the customer-specific deviations. Codify into repeatable per-vertical onboarding playbooks.

**Dispatch type:** Continuous, migration-event-driven.

**Owner:** Growdirect agent ops + Bart's onboarding team + RapidPOS senior engineer.

**Deployment week:** Month 3 (after first sandbox migration).

**Scaling:**
- Month 3: first migration captured (eager-cohort customer #1).
- Month 4-5: 2-3 more migrations captured; first vertical-specific playbook drafted (likely garden-center).
- Month 6: vertical playbook v1 complete; subsequent migrations execute against template.
- Month 12: playbooks for all 5 verticals; new migrations are templated execution rather than bespoke craft.
- Month 18: new-logo customers (outside RapidPOS book) onboarded against playbooks at multiples of historical pace.

**KPIs:**
- Onboarding playbooks per vertical (target 5 by M12)
- Per-customer onboarding hours (baseline → -40% by M12)
- New-customer go-live elapsed weeks (baseline 8-16 → 2-4 by M18)
- Playbook reuse rate (% of new onboardings that match a templated playbook) (target 70% by M18)

## A5 — Integration-bus reverse-engineer (internal)

**Mission:** While A1-A4 free the seller team for high-value work, Growdirect's deeper agents work the data spine: map customer Counterpoint schemas onto CRDM, profile each customer's ILDWAC-conversion difficulty, surface what's outside the standard API and needs custom adapter work.

**Dispatch type:** Parallel, founder-directed.

**Owner:** Growdirect engineering (internal — no RapidPOS team load).

**Deployment week:** 2.

**Scaling:**
- Week 2: per-VAR-layer adapter design starts (RapidPOS-specific Counterpoint extensions).
- Month 1-2: per-customer schema discovery via existing customer-DB connections (where permitted).
- Month 3: VAR-layer adapter v1 complete.
- Month 4-6: per-customer adapter specialization for eager cohort.
- Month 6+: adapter library mature; subsequent customers in same vertical get rapid setup.

**KPIs:**
- Customers schema-discovered (target 50 by M3 — full RapidPOS book)
- VAR-layer adapter completeness (target 100% by M3)
- Per-customer adapter specialization time (target <8 hours by M6, <4 hours by M12)
- CRDM-mapping accuracy on first attempt (target 90%+ by M6)

## Day-1 architecture summary

Visual: agentic ops fabric (workload #18 from cost-model GCP blueprint) consists of:

```
[Ticket inflow]
      ↓
[A1 Support burndown agent] ← reads from → [A3 Contextual wiki]
      ↓                                            ↑
[Resolution attempt]                              writes to
      ↓
[Auto-resolved] → [Customer notified]
      ↓
[Escalated] → [Human queue] → [Resolved] → [A3 captures resolution]
                                              ↓
                             [A2 Root-cause analyzer] ← reads tickets
                                              ↓
                             [Top-10 repeat causes] → [Permanent fix or playbook]

[Migration event] → [A4 Onboarding capture] → [Vertical playbook]

[Internal track]
[Customer DB access] → [A5 Integration-bus] → [CRDM mapping] → [ILDWAC scoring]
```

GCP services backing each agent: Vertex AI for inference, Cloud Run / GKE for runtimes, Pub/Sub for triggers, Cloud SQL for state, Cloud Storage for wiki + playbook output.

## Day-1 access requirements

For agents to function, they need (negotiated as part of deal close):
- Read access to RapidPOS's existing ticket system (Zendesk / Freshdesk / whatever)
- Read access to customer Counterpoint deployments (with customer permission, ride-along to A5)
- Edit access to a Wiki destination (start with Confluence or Notion; eventually CRB.ai)
- Memory-bus connectivity for cross-session continuity
- Vertex AI Anthropic access on the Growdirect GCP org (already in place)

## Cross-references

- `crb-skills/cost-model/reference/08-bart-team-labor-trajectory.md` — labor-mix migration the agents enable
- `Brain/diligence/rapidpos/10-burndown-flywheel.md` — Phase A→B→C narrative
- `Brain/diligence/rapidpos/04-valuation-impact.md` — agentic-ops cost in the deal economics
