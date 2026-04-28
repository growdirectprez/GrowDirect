# Canary Go — Agent PMO Architecture

**Date:** 2026-04-28
**Status:** Approved
**Scope:** Full agent network topology, lifecycle model, Service Introduction protocol, support routing

---

## Governing Thesis

The Canary Go platform is operated by an autonomous agent network organized in three layers: a Controller at the top, 27 domain PMO agents at the L3 subsystem level, and a set of cross-cutting infrastructure agents below. MCP is the connective tissue — the protocol through which every agent exposes its context and capabilities. Service Introduction is the only Human-in-the-Loop change management gate in the system. The founder interfaces with the network through the Controller. Everything else runs without a human in the loop unless an agent determines it cannot resolve a situation and escalates.

This architecture eliminates the Systems Integrator as a dependency. Context that would otherwise live in a consulting team's tribal knowledge lives in the agent network — structured, persistent, callable at any session.

---

## Network Topology

```
                        ┌─────────────────┐
                        │   CONTROLLER    │
                        │  (full network  │
                        │     view)       │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
     ┌────────▼────────┐  ┌──────▼──────┐  ┌───────▼───────┐
     │  DOMAIN AGENTS  │  │   INFRA     │  │     MCP       │
     │  27 L3 nodes    │  │   AGENTS    │  │  (connective  │
     │  (module PMO)   │  │             │  │   tissue)     │
     └─────────────────┘  └─────────────┘  └───────────────┘
```

---

## Controller

The Controller is the only agent with a full network view. It does not own any individual module or infrastructure domain — it owns the system state across all of them.

**Responsibilities:**
- Network state awareness — knows the lifecycle phase and health of every domain and infrastructure agent
- Cross-agent coordination — sequences Service Introduction gates, manages shared dependency conflicts
- Release train cadence — owns the M1→M6 delivery sequence, surfaces blockers
- Founder interface — the PMO agent the founder talks to; translates network state into decisions that need human authority
- Escalation routing — when any agent in the network cannot resolve a situation, it escalates to the Controller before surfacing to the founder

---

## Domain Agents — L3 PMO Layer

One agent per L3 subsystem. Each carries dual authority:

| Mode | Owns |
|------|------|
| **Business** | Retailer domain knowledge, CATz Phase I/II mapping, business case, operator failure modes |
| **Technical** | SDD, Go service, sqlc contracts, data model, upstream/downstream API surface |

### Node Inventory

| Milestone | Nodes | Epics |
|-----------|-------|-------|
| M1 — Foundation | CRDM & Data Model, Identity & Auth, Multi-POS Substrate, Service Skeleton | GRO-638–641 |
| M2 — Detection Core | Webhook & TSP, Chirp Engine, Fox Case Management | GRO-642–644 |
| M3 — Intelligence Layer | Owl & pgvector, Analytics & Risk Scoring | GRO-645–646 |
| M4 — Module Spine | T, R, N, A, Q, C, D, F, J, S, P, L, W | GRO-647–659 |
| M5 — VAR Delivery | Bull (NCR Counterpoint), Edge Agent, RapidPOS Onboarding | GRO-660–662 |
| M6 — Hardening / SI | GCP Deployment, Ops Handoff Package | GRO-663–664 |

### Module Dependency Graph

Each domain agent knows its full adjacency map.

| Module | Receives From | Feeds Into |
|--------|--------------|------------|
| T — Transaction Pipeline | N (device identity), P (price values) | Q, R, F, A |
| N — Device | — | T |
| Q — Loss Prevention | T, A | Fox, Owl |
| R — Customer | T | P (loyalty earn rules) |
| P — Pricing & Promotion | R, C | T, C |
| C — Commercial | S, P | D, F |
| S — Space, Range & Display | — | C, J |
| D — Distribution | C, J | A, F |
| J — Forecast & Order | S, D | C, D |
| F — Finance | T, C, D, A | — |
| A — Asset Management | T, D, Q | F |
| L — Labor & Workforce | — | W |
| W — Work Execution | L | All modules (execution dispatch) |

**Foundation dependency:** All 13 modules depend on CRDM/Data Model, Identity/Auth, and Multi-POS Substrate. The CRDM agent is the schema authority — cross-module schema changes require CRDM agent sign-off and interface versioning before consuming modules advance to Service Introduction.

**Safe-change rule:** Interface changes (sqlc contract, API surface, schema migration) require a new SI cycle for affected modules. Logic-only changes within a module's boundary do not.

---

## Infrastructure Agents

Cross-cutting agents that operate beneath and across all domain agents.

| Agent | Layer | Responsibilities |
|-------|-------|-----------------|
| **DBA** | Data | Schema migrations, query optimization, index health, vacuum/maintenance, query contract enforcement |
| **Storage** | Data | Object storage lifecycle, block storage, backup/restore, data tiering — GCP Cloud Storage + Persistent Disk |
| **Data Governance** | Compliance | PII inventory, hash-chain integrity, data residency, retention policy, right-to-delete, GDPR/CCPA posture |
| **Legal & Compliance** | Compliance | Contract lifecycle, regulatory obligations (PCI DSS, GDPR, CCPA, Prop 65), audit trail authority, VAR agreement compliance |
| **Security** | Compliance | Access control, encryption-at-rest key management, audit trail, threat detection, service-to-service auth |
| **Accountant** | Finance | Business financial layer — cloud spend vs revenue, unit economics, margin per module, P&L |
| **CPA** | Finance | Cost-per-action billing intelligence — GCP transfer metering, egress spend monitoring, cost anomaly alerting |
| **Cloud Ingress/Egress** | Network | Data flow management across cloud boundaries, traffic pattern monitoring, routing optimization |
| **Network** | Infrastructure | VPC, service mesh, DNS, load balancing, inter-service connectivity |
| **Scheduling** | PMO | Job scheduling, release train cadence, sprint rhythm, cron contract management |
| **MCP** | Fabric | Protocol layer — every agent exposes context and capabilities as MCP tools; routes context between agents and sessions |

### Infrastructure Agent Relationships

Data Governance and Security produce evidence. Legal & Compliance interprets it against obligations — the compliance authority layer sits above both.

CPA watches the infrastructure cost signal per action. Accountant synthesizes it into business impact — unit economics, module-level margin, P&L. Same technical-to-business stack as DBA (technical) → Finance module (business).

---

## Lifecycle Model

```
Spec → Build → VAR Delivery → Hardening → [SERVICE INTRODUCTION] → Support
  ↑       ↑          ↑              ↑                ↑                  ↑
Agent   Agent      Agent          Agent          HIL gate only       Agent
owned   owned      owned          owned          (founder sign-off)  owned
```

| Phase | Owner | Output |
|-------|-------|--------|
| **Spec** | Domain agent | SDD, module manifest, acceptance criteria |
| **Build** | Domain agent | Go service, sqlc queries, migrations, tests |
| **VAR Delivery** | Domain agent | Deployed to RapidPOS channel, Counterpoint connected |
| **Hardening** | Domain agent + ops team | Scale verified, SLA baselined, runbooks authored |
| **Service Introduction** | Founder (HIL) | Formal acceptance: module is live, supported, ops-owned |
| **Support** | Domain agent (support mode) | Bug triage, regression, dependency coordination |

---

## Service Introduction Protocol

The **only HIL change management gate** in the system.

### Gate Criteria (all must be true)

1. Module passes hardening checklist — SLA baseline met, monitoring live, runbooks complete
2. Ops team confirms operational readiness
3. Acceptance criteria from original SDD verified against live deployment
4. Dependency nodes in Support mode or confirmed ready; CRDM agent confirms no pending interface changes
5. RapidPOS Inbound routing for this module is configured and tested
6. Legal & Compliance agent confirms no outstanding regulatory obligations for this module

### Gate Authority

The founder signs off. The Controller surfaces the gate — presents the checklist, confirms all criteria, requests human authority. This is not a rubber stamp; it is the moment the platform partner formally accepts operational ownership.

### Module Sequencing

Modules gate independently in dependency order. Foundation first, then Detection Core, then in module dependency sequence (T before Q, N before T, etc.). The ops team receives modules as they clear — not a monolithic handoff.

### What Changes at the Gate

| Before SI | After SI |
|-----------|----------|
| Domain agent in build mode | Domain agent in support mode |
| GrowDirect holds operational context | Ops team holds operational ownership |
| Issues → Canary Go project | Issues → RapidPOS Inbound, routed to module agent |
| Acceptance criteria are targets | Acceptance criteria are the SLA |

---

## Support Mode

After Service Introduction the domain agent shifts from building to owning.

**Triage:** First responder for RapidPOS Inbound issues tagged to this module.

**Classification:** Bug (GrowDirect owns fix) vs config issue (VAR delivery) vs feature request (new GRO epic).

**Dependency coordination:** If a bug crosses a module boundary, the agent coordinates with the adjacent node agent. The Controller mediates if both agents cannot resolve.

**Regression authority:** Interface changes re-gate through SI. Logic-only changes within module boundary do not.

**Ops team boundary:** Ops owns operations — deployment, monitoring, scaling, incident response, SLA adherence. Domain agent retains authority over domain logic, detection rules, module architecture, and dependency interfaces.

---

## Memory Substrate

Each agent's context lives in the memory bus (pgvector, `growdirect_memory`). Session instantiation:

```
memory_recall("Module Q agent context")
memory_recall("Module Q dependency surface")
memory_recall("Controller network state")
```

Agent profiles are seeded documents, not ad-hoc prompts. Each contains: module identity, business context, technical context, dependency map, current lifecycle phase, SI status.

**Profile location:** `Brain/wiki/agent-profiles/` — one file per agent, seeded into memory bus on creation.

---

## What This Replaces

The SI model depends on consulting teams to hold context across phases — business analysts, architects, developers, and support engineers who hand off to each other with inevitable fidelity loss at every boundary.

In this model the agent carries that context. Handoffs are between lifecycle phases of the same agent. The ops team receives productionized modules with context-loaded agents ready to support them.

**Founder role:** PMO authority via the Controller, Service Introduction sign-off, strategic direction. Not operational execution.

---

## Related

- `Brain/wiki/canary-go-portal.md` — project portal and SDD index
- `docs/sdds/go-handoff/` — 19 Go build SDDs
- `GrowDirect-CRB/modules/` — 13 module manifests (transient clone: `gh repo clone growdirect-llc/canary-retail-brain`)
- Linear: [Canary Go](https://linear.app/growdirect/project/canary-go-9fb99af5b6af) · [RapidPOS Inbound](https://linear.app/growdirect/project/rapidpos-inbound-74436ec08ce9) · [RapidPOS Channel](https://linear.app/growdirect/initiative/rapidpos-channel-b811763ef7e5)
- `docs/superpowers/specs/2026-04-27-hawk-bull-design.md` — POS adapter substrate design
