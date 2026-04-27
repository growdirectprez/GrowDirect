---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source-archive: /Volumes/My Passport/CLIENTS/DELIVERY/ + /Volumes/My Passport/macpro/Users/geoff/Documents/ (sanitized)
provenance: Brain/wiki/founder-context-secure-engagement-archive.md
----

# Engagement Resource Model — FTE × Week

The companion to the 100-day deployment shape. This is the staffing pattern Geoffrey ran on the same Phase 1 — the resource curve, the role split between vendor and customer, and the swap-out points where a role hands the baton. The numbers below come from the same engagement source as the deployment shape; treat them as one consistent model viewed from the people angle.

## Headline numbers

For a 100-day Phase 1 of a hosted loss-prevention deployment at a national multi-unit retailer:

- **Vendor side total: ~1,920 hours** ≈ 12 FTE-weeks at 40h/week ≈ 2.4 FTEs averaged across 100 days.
- **Customer side total: ~778 hours** ≈ 4.9 FTE-weeks ≈ ~1 FTE averaged across 100 days, but heavily concentrated in 4-5 specific roles.
- **Combined: ~2,700 hours** for the 100-day phase.

This is the resource budget for one business release on a hosted analytics platform with a single POS feed and three master data feeds. Adjust upward for additional feeds, additional POS variants, or non-hosted topology.

## Vendor-side roles

Six recurring vendor roles plus a transient handover role.

| Role | Hours | Pattern | Peak |
|---|---|---|---|
| Tech Developer 1 | ~525 | The "lead dev" of the two-pizza pair | 40h/wk weeks 6-12 |
| Tech Developer 2 | ~525 | The mirror dev (pair-programmed transforms and adapter work) | 40h/wk weeks 6-12 |
| Tech Lead | ~210 | Architecture, integration test oversight, UI finalization | spikes ~28h/wk in design weeks |
| Project Management | ~190 | Continuous low allocation | flat ~8h/wk weeks 1-20, spike to 40h in week 1 |
| Customer Services | ~145 | Workshops, training, validation | bursts at workshops, training |
| Tech Infrastructure | ~80 | Provisioning bursts | weeks 6-7 (QA), 17-18 (Prod) |
| Support Desk (handover) | ~120 | Last 3 weeks only | flat 40h/wk for the handover ramp |

### Curve shape, vendor side

The vendor curve has a characteristic profile:

```
Hours/week
60 │
50 │                              ████████
40 │                          ████████████████
30 │                      ████████████████████
20 │            ██████████████████████████████████████
10 │ ██████████                                       ████████████
 0 └────────────────────────────────────────────────────────────────
   Wk 1  3  5  7  9 11 13 15 17 19  20
   ↑     ↑       ↑                ↑       ↑
   kickoff design  development    validation  go-live
```

- **Weeks 1-3 (kickoff, analysis):** light vendor footprint — mostly PM and Tech Lead in workshops with the customer. Customer Services lead also engaged for kickoff.
- **Weeks 4-5 (design):** vendor architects ramp; Tech Lead and both Devs participate in solution-architecture documentation. Customer-side LP roles converge for workshops in the same window.
- **Weeks 6-12 (development):** the heavy plateau. Two devs at 40h/week, Tech Lead at ~50% supervising. PM continues at 8h/week. Infrastructure has an early spike (QA build).
- **Weeks 13-14 (integration test):** Tech Lead resumes ~50%, devs drop to ~25% (issue-fix mode), customer IT-development re-engages to send/receive test data.
- **Weeks 15-18 (validation):** vendor dips. Tech Lead stays involved at low allocation for issue triage. Customer Services lead runs the validation workshop. Devs at ~10-25% on retest.
- **Weeks 17-19 (production infrastructure, parallel):** Infrastructure spikes again. Tech Lead returns for install/configure.
- **Week 20 (deploy + go-live):** all-hands. Tech Lead and both Devs at 40h/week for UI finalization and production data load. Customer Services runs training. Support Desk fully online for the handover ramp.

### The two-pizza dev pair pattern

Tech Developer 1 and Tech Developer 2 carry ~50% of vendor hours combined and run as a pair throughout development. Their work is symmetric in the source plan — they shared all the develop-the-data-transforms tasks and the deploy/install tasks. This is deliberate — pair-programming the integration code keeps a backup hot when one dev is pulled into customer-side debugging. The pair becomes a single dev for Integration Test (issue resolution rarely needs both at once).

### The lead at 50%, not 100%

The Tech Lead role is at ~50% allocation across the technical phases, not 100%. The Lead is the architect, the gate-decision-maker, and the customer-side technical interface — none of those need full-time hands-on coding. Hours peak in design and at integration/deploy. Modeling the Lead at 100% is a common over-estimation that inflates the budget by 200+ hours.

### PM as a steady drumbeat

Project Management runs at 8h/week (one day a week) for the full 100 days, plus a 40h kickoff burst in week 1. This is a deliberately low allocation — the PM is running cadence, not running activities. Activities are owned by the Tech Lead or the workstream owners.

### Infrastructure and Support Desk as transient roles

These are the swap-out points:

- **Infrastructure** appears for two distinct bursts: ~24h around week 6-7 to build QA (architecture handoff), ~56h around week 17-18 to build Production. These are different people, possibly different teams. Plan them as two engagements, not one continuous allocation.
- **Support Desk** appears only for the last 3 weeks (the handover ramp). 120 hours total, ~40h/week. This is the team that will own the platform after Day 100; their engagement begins when Production Infrastructure stands up.

## Customer-side roles

Seven recurring customer roles. These are the seats the customer must staff to make 100 days.

| Role | Hours | Pattern | Peak |
|---|---|---|---|
| POS SME | ~245 | The heaviest customer role | weeks 5-8 (extract dev), trickle to week 18 (mapping guidance) |
| LP Management | ~130 | Workshops, sign-offs | weeks 5-6 workshops, week 13 validation |
| LP Analyst | ~115 | Workshops, validation, training | weeks 5-6, weeks 13-15, week 19 |
| IT Development | ~95 | Data feeds, integration test | weeks 4-5 (item/store/employee feeds), weeks 13-14 (integration test) |
| IT Management | ~90 | Continuous low allocation | flat ~4h/wk |
| Process/Systems SME | ~30 | Process guides, master data feeds | week 1, weeks 4-5 |
| IT Networking | ~30 | SFTP and network bursts | weeks 2-3 (SFTP), week 7 (production network) |

### POS SME is the burden role

The POS subject-matter expert carries the most customer hours of any role — more than the customer's own PM or LP manager. This is the single biggest staffing risk on the customer side, because POS SMEs are usually the customer's senior store-systems engineers and are perpetually under-supplied. Three separate commitments stack on this role: POS Tlog technical specification (week 1-2), POS Tlog extract development (weeks 4-7), and ongoing POS mapping guidance (weeks 5-18). Failing to secure this person's calendar is the single most common reason a Phase 1 slips.

### Workshop-cluster pattern

LP Management, LP Analyst, and Customer Services lead converge for ~3 day-long workshops in weeks 5-6 (Strategy, High-Level Workflow, Roles and Permissions, Dashboards/Reports), and again for the Validation Workshop in week 13. ~40 hours of LP time falls inside one calendar week each cluster. This concentrates the customer's senior LP staff time and lets the rest of the engagement run with lower customer load. Block these calendars 4 weeks in advance.

### Customer PM mirrors vendor PM

Customer IT Management runs at 4h/week — half the vendor PM allocation — for the full 100 days. This is the customer's escalation channel and the cadence partner. If the customer cannot supply this allocation, the engagement defaults to the vendor PM running both sides; this works for 30 days and breaks at the first scope or schedule conflict.

## Role swap-out points

Five places where a role hands off:

1. **Architect → Devs (end of Technical Design, ~Day 30).** Tech Lead's hours-per-week drops; Devs go to 40h/week. The Tech Lead retains a supervisory ~50% but is no longer the bottleneck.
2. **Devs → Tech Lead (Integration Test, ~Day 63).** Devs drop to fix-mode allocation; Tech Lead resumes ~50% to run the integration test cycle.
3. **Vendor → Customer Services (Validation, ~Day 67).** The Customer Services lead becomes the primary vendor face during validation. The Tech Lead and Devs become reactive resources.
4. **Architecture → Infrastructure (~Day 76).** Production environment build is owned by Infrastructure team, not by the Tech Lead. The Tech Lead returns for install/configure but does not run provisioning.
5. **Delivery → Support Desk (Day 100 - 21 = ~Day 79).** Support Desk's three-week handover begins when Production Infrastructure stands up. By Day 100, Support Desk is the production owner and Delivery is in warranty mode.

## Resource pattern: deviation from the source archetype

The source engagement is a national multi-unit retailer with a Tier-1 IT department. For a 25-store mid-market chain on a packaged retail-management platform:

- **Vendor side**: same shape, ~10-15% fewer hours total (tighter scope on data feeds and reports). Pair-dev pattern still holds.
- **Customer side**: dramatically thinner. Customer IT Development hours often drop to ~30 (the customer's IT is reseller-supported, not in-house). POS SME hours drop because the POS data model is shipped by the platform vendor, not bespoke. LP roles may not exist as named seats — a single "store operations" person plays both LP Management and LP Analyst. Process/Systems SME and IT Networking may collapse into a single contractor.
- **Net effect**: customer hours fall to ~400-450, vendor hours rise to ~2,000 (more done for the customer because they cannot supply the seats). Engagement total rises modestly to ~2,400-2,500 hours. The 100-day schedule must extend to ~110 days to absorb the customer's lower throughput.

## What to staff explicitly, what to staff loosely

Staff explicitly (named individuals, calendars blocked):
- Tech Lead, Tech Dev 1, Tech Dev 2 (vendor)
- PM, both sides
- Customer Services lead
- Customer POS SME
- Customer LP Management + LP Analyst (for workshops and validation)

Staff loosely (group ownership, not named seat):
- Tech Infrastructure (vendor team allocation, not a person)
- Support Desk (vendor team)
- Customer IT Development (a team queue, not a named dev)
- Customer IT Networking (often a ticket-based handoff, not a named engineer)

Naming the loose roles too early creates a false sense of staffing. Leaving the explicit roles unnamed at kickoff is the single most reliable predictor of slip.
