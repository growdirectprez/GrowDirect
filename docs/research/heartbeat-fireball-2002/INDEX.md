# INDEX — Heartbeat / Fireball (2002) Essential Design Extraction

A 5-file research extraction (plus this index) of the **working
solution** at the centre of the 2001–2003 retail OOS detection +
notification system that ran at one US Tier-1 grocery chain pilot and
one US southeastern multi-state supermarket chain pilot. The system
was branded internally as Heartbeat / Fireball and implemented on a
Microsoft enterprise-integration stack with a third-party statistical
OOS detection algorithm.

This research folder is *signal-only*. It strips out commercial framing,
sales decks, pricing, alliance paperwork, partnership structure, and
client-specific implementation details. What remains is the design DNA
that informs Canary's Chirp module and the Loss Prevention capability
of the canonical
[Retail Capability Model](../../../Canary/docs/retail-capability-model.md).

Per playbook scrub rule, named retail clients are abstracted into NFR
deployment archetypes. Raw intakes at `Brain/raw/inbox/Heartbeat/`
remain intact as the source of record.

## Reading order

| File | What it answers | Length |
|---|---|---|
| [THE_PROBLEM.md](THE_PROBLEM.md) | What NFR profile the system solved for: scale, vertical, latency, regulatory surface, NFRs, what was explicitly out of scope, and what "the problem" really was | ~120 lines |
| [THE_ARCHITECTURE.md](THE_ARCHITECTURE.md) | End-to-end working pipeline: trickle POS feed → integration bus → algorithm cluster → integration bus → notification subsystem. Five-cluster hosted service anatomy. RIO Inputs / RIO Outputs split. Two collection-pattern alternatives evaluated | ~180 lines |
| [THE_ALGORITHM.md](THE_ALGORITHM.md) | The intellectual centre: a statistical-anomaly detector against a learned per-(item, store) Poisson velocity model with 8 merchandising-condition covariates. Five named event types (OOS, Too Fast, Too Slow, New Item, Dropped Item). Tunability and gaps documented | ~140 lines |
| [THE_NOTIFICATION_SYSTEM.md](THE_NOTIFICATION_SYSTEM.md) | The Chirp ancestor. Trigger model, subscription model, delivery channels, report format, XML event schema (with Aug→Jan evolution noted), failure modes, operator workflow. The most directly Canary-parallel artifact in the archive | ~190 lines |
| [CANARY_LINEAGE_MAP.md](CANARY_LINEAGE_MAP.md) | The synthesis. Per-component map of the 2002 design to Canary's current architecture (1:1 / transformed / net-new). What 2002 got right. What 2002 got wrong (or right-for-2002, wrong-for-2026). What the Phase-I retrospective revealed (abstracted to NFR archetype). What Canary inherits, knowingly or not. What is genuinely new in Canary | ~170 lines |

## Source files extracted (signal only)

| Source | Location |
|---|---|
| Background | `Brain/raw/inbox/Heartbeat/MS Overview/Background.htm` |
| Functional Overview | `Brain/raw/inbox/Heartbeat/MS Overview/Functional Overview.htm` |
| Solution Architecture | `Brain/raw/inbox/Heartbeat/MS Overview/Solution Architecture.htm` |
| Process Flows | `Brain/raw/inbox/Heartbeat/MS Overview/Process Flows.htm` |
| Algorithm | `Brain/raw/inbox/Heartbeat/MS Overview/Algorithm.htm` |
| Vision Scope | `Brain/raw/inbox/Heartbeat/MS Overview/Fireball Vision Scope.doc` |
| Approved Heartbeat Data Architecture | `Brain/raw/inbox/Heartbeat/Approved Heartbeat Data Architecture.ppt` |
| Trickle Feed Data Flow | `Brain/raw/inbox/Heartbeat/Trickle Feed Data flow.ppt` |
| Heartbeat OOS Architecture | `Brain/raw/inbox/Heartbeat/Fireball Documentation/.../Heartbeat OOS Architecture.ppt` |
| A4R - Sample Process Flow | `Brain/raw/inbox/Heartbeat/A4R - Sample Process Flow.ppt` |
| Notification Design Spec | `Brain/raw/inbox/Heartbeat/Fireball Documentation/.../Notification Design/Notification design Spec.doc` |
| Notification System Specification1221 | `.../Notification Design/Notification System Specification1221.doc` |
| Notification Subsystem Documentation | `.../Notification Design/Notification Subsystem Documentation.doc` |
| Notification Design Customer Aug 6 | `.../Notification Design/Notification Design Customer Aug 6.doc` |
| Project-Heartbeat XML schema (6 Aug) | `.../Notification Design/Project-Hearbeat_XMLschema_6_Aug[1].doc` |
| Project-Heartbeat XML schema (15 Jan) | `.../Notification Design/Project-Hearbeat_XMLschema_15_Jan.doc` |
| Fireball Notification Storyboard | `.../Notification Design/Fireball_Notification _StoryBoard.ppt` |
| Phase-I Pilot Assessment | `Brain/raw/inbox/Heartbeat/Service Offering/Phase-I Pilot Assessment.doc` |

18 source files extracted out of ~417 in the full archive. The remaining
~399 are commercial framing (sales decks, alliance paperwork, GTM
pricing, client-specific deployment files, marketing material) that
were excluded per the *extract the working solution, not the noise*
playbook rule.

## What got scrubbed as noise (and why)

Four categories of source material in the archive were deliberately
not extracted:

1. **Commercial and sales decks** — version-numbered "Why us" pitches,
   alliance partnership decks, GTM pricing estimates, sales-stage
   collateral. Not the working design.
2. **Client-specific deployment files** — per-pilot configuration
   specifics, named-personnel subscription examples, retailer-specific
   contract paperwork. The Phase-I Pilot Assessment was the one
   commercial-flavored doc worth deep-reading because it's an honest
   technical retrospective; client specifics were abstracted to NFR
   archetype in the synthesis.
3. **Methodology decks (CVCS Diagnostic, Service Offering phase plans)**
   — consulting-engagement frameworks, not product design.
4. **Microsoft Retail BizTalk Resource Kit** — Microsoft's reusable
   integration-pattern library. Mentioned in the architecture file as
   the platform foundation; not deep-read because the working design
   used the platform; understanding the platform doesn't help understand
   the design.

## Downstream destinations

This research folder feeds two downstream artifacts:

- **Brain wiki card** — `Brain/wiki/secure-heartbeat-fireball-2002.md`.
  The 5-minute-read version. Headlines the essential design + the
  Canary-parallel finding. Archetype-scrubbed.
- **Canonical retail capability model — Loss Prevention enrichment** —
  [`Canary/docs/retail-capability-model.md`](../../../Canary/docs/retail-capability-model.md)
  Loss Prevention capability picks up the prior-art design DNA in
  fully-vanilla form (no client names, no vendor product names, no
  archetype labels — just the canonical pattern).

The research folder is the deep source; the wiki card and capability-
model enrichment are derivations.

## Naming relationship — open

The 2002 system carries the name *Heartbeat / Fireball*. Canary's
data-strategy NorthStar describes a *Canary Heartbeat Network* anchored
to Bitcoin's block heartbeat. The two are related; the form of the
relationship (direct homage, conceptual lineage, architectural DNA) is
recorded as an open question in CANARY_LINEAGE_MAP.md and is intended
to be resolved with the founder in a follow-on session before this
folder is treated as final.
