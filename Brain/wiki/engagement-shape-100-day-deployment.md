---
classification: internal
type: wiki
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source-archive: /Volumes/My Passport/CLIENTS/DELIVERY/ + /Volumes/My Passport/macpro/Users/geoff/Documents/ (sanitized)
provenance: Brain/wiki/founder-context-secure-engagement-archive.md
---

# Engagement Shape — 100-Day Deployment

The 100-day shape is the planning archetype Geoffrey ran on a national multi-unit retailer for a loss-prevention platform's Phase 1 (point-of-sale exception-based reporting). It is reusable for any first-phase deployment where the data side dominates, the product is a hosted analytics platform, and a single business release lands at day 100. Use this shape as the skeleton; tune the durations to the data complexity, not the store count.

## What "100 days" means

100 working days, calendar-aligned to a single business release. The engagement runs on a Mon→Fri week. Day 0 is the on-site kickoff. Day 100 is go-live for the first business release. Project Administration runs continuously for all 100 days as a parallel workstream, not a phase.

The 100 days assumes: (1) the customer has functioning IT/networking/dev capacity, (2) one POS data feed and three master data feeds, (3) one production tenant, (4) one functional business area for Phase 1 (in the source case, exception-based reporting). Add days, do not add parallel tracks, when any of these change.

## Phase structure

Phase 1 nests inside the 100 days. The numbering inside the source artifact assumes Phase 2/3+ exist outside this window. Treat "100 days" as the unit of one business release, repeatable for subsequent phases.

```
Day  1───────10──────20──────30──────40──────50──────60──────70──────80──────90─────100
     │                                                                              │
     │ Project Administration (continuous, low allocation)                           │
     ├─POS Analysis (17d)                                                            │
     │       ├─Functional Design (5d)                                                │
     │       ├─Technical Design (11d)                                                │
     │                ├─Development (32d) ────────────────────────┤                  │
     │                                                            ├─Integration (5d) │
     │                                                                  ├─Validation │
     │                                                                  │  (22d)     │
     │                                                                  ├─Production │
     │                                                                  │   Infra    │
     │                                                                  │   (20d,    │
     │                                                                  │   parallel)│
     │                                                                            ├──┤
     │                                                                            Deploy
     │                                                                              (10d)
     │                                                                              │
                                                                                    Go Live
```

### Sub-phase anatomy

**Project Administration (Days 1-100, continuous)**
The PM channel. On-site kickoff in Days 1-2. Agree baseline project plan in Days 3-4. Then weekly status cadence with the customer's PM through Day 100. Vendor PM at ~20% allocation, customer PM at ~10%.

**POS Analysis (Days 1-17)**
The discovery sub-phase. Two streams in parallel:
- Point-of-sale analysis (13 days): collect process guides, identify the POS data source and modifications needed for external sharing, write a technical specification for the POS feed, establish SFTP, agree the data format and Tlog sample.
- External data feed analysis (3 days): item master, store master, employee master — source, spec, sample data, historical availability.
- Estimate customer development effort for the external feeds (1 day, gates the design phase).

**Functional Design (Days 21-25)**
Five days, mostly workshops: solution strategy workshop, define high-level workflow, define roles and permissions, identify dashboards and report requirements. Customer LP roles and customer-services lead together. This phase produces the business-side "what does the platform do for us" answer.

**Technical Design (Days 22-30)**
Overlaps the back end of Functional Design. Eleven days. Two halves:
- Define solution architecture (8.5d): capacity planning, hardware for QA, network and connectivity requirements, data transport and load mechanism.
- Document solution architecture (2.5d): four sub-documents — solution overview, POS Tlog feed, master data feeds, employee master data.
Approve Phase 1 Design at the close. This is one of the gates.

**Development (Days 31-62)**
The longest single sub-phase, 32 days. Two parallel tracks:
- Customer-side data extracts (16d): POS Tlog extract, master data, send test data for development.
- Vendor-side data transforms (32d, runs full sub-phase): data transport and load mechanism, SFTP connectivity, POS, master data feeds, system alerts and monitors.

**Integration Test (Days 63-67)**
Five days, end-to-end. Receive Tlog and reference data files via the production method. End-to-end test of the Tlog load process. End-to-end test of the other data feeds. Integration test complete is a gate.

**Customer POS Data Validation (Days 67-88)**
22 days. Configure the platform application and reference-data module in QA. Load data for a validation workshop. Run the workshop with customer LP analyst, LP manager, and vendor customer-services lead. Resolve data validation issues and retest (this is the long tail — 15+ days). Sign-off data validation is a gate.

**Production Infrastructure (Days 76-96, parallel to Validation)**
20 days, runs in parallel with the second half of Validation. Establish customer tenant network. Provision production database storage. Provision production application servers. Install and configure the platform in production. Support-desk handover is also part of this stream. Production infrastructure setup complete is a gate.

**Deploy (Days 90-100)**
10 days, overlapping the back end of Production Infrastructure. Phase 1 training (3 days, scheduled 5 days before validation completes). Load data to production environment (5 days). Finalize UI configuration and reports (5 days). Exception-based reporting POS go-live is the day-100 gate.

## Gate cadence

The deployment is governed by seven named gates. Each is a binary observable transition (a deliverable signed off, an environment built, or a meeting held with explicit decision). Gates own the schedule, not the activities.

| # | Gate | Day | What it gates |
|---|---|---|---|
| 1 | Analysis complete | ~17 | Authority to enter design |
| 2 | Phase 1 Technical Design complete | ~30 | Authority to enter development |
| 3 | Phase 1 Development complete | ~62 | Authority to enter integration test |
| 4 | Integration Test complete | ~67 | Authority to enter validation |
| 5 | Sign-off Data Validation | ~88 | Authority to load production data |
| 6 | Production infrastructure setup complete | ~96 | Authority to deploy |
| 7 | Go Live | 100 | End of Phase 1 |

Gates 5 and 6 must both clear before Deploy starts. They are independent — Validation depends on the QA environment, Infrastructure depends on the production environment. They can therefore run in parallel for the last 12 days, and almost always must to make 100 days.

## Parallel workstreams

Three workstreams run in parallel through the deployment:

1. **Project Administration** — continuous, full 100 days, low allocation. Owns cadence, status reporting, escalation, change requests.
2. **Production Infrastructure** — 20-day parallel sub-phase that overlaps Validation by ~12 days. Owns provisioning, install, support handover prep.
3. **Ongoing POS mapping guidance** — the customer's POS subject-matter expert is on call from Day 22 through Day 50+ at ~10% allocation, supporting the development team as questions surface. This is not a sub-phase; it's a standing commitment.

Underestimating any of these three is the most common reason 100-day deployments slip to 130.

## Milestone cadence (deliverables, not gates)

Inside the gates are smaller, observable milestones the PM tracks weekly:

- Agree baseline project plan (Day 4)
- POS technical specification provided (Day 6)
- SFTP for data sharing established (Day 9)
- Data format and POS Tlog sample (Day 17)
- All three master data feeds spec'd (Day 19)
- Solution architecture documented (Day 30)
- POS Tlog extract delivered (Day 50)
- Master data extract delivered (Day 40)
- Test data sent for development (Day 50)
- All four solution-architecture sub-docs (overview, Tlog feed, master data, employee master) signed off (Day 30)
- QA environment loaded with customer data (Day 70)
- Validation workshop run (Day 73)
- Production tenant network established (Day 78)
- Production database storage provisioned (Day 80)
- Production application servers provisioned (Day 83)
- Platform installed in production (Day 86)
- Phase 1 training delivered (Day 91)
- Production data loaded (Day 96)
- UI configuration and reports finalized (Day 100)

## Typical adjustments by archetype

The 100-day shape was built for a national multi-unit retailer with a Tier-1 IT operation. Common adjustments:

- **Mid-market retailer (25-100 stores) with thin IT.** Add 15-20 days into Analysis (the customer's POS SME availability and data-feed maturity are the long pole). Compress Production Infrastructure (single-tenant cloud, 7-10 days vs 20). Net: ~110 days.
- **Multi-banner / multi-POS retailer.** Add 20+ days into Development for parallel POS adapter work. Add a second Validation cycle. Net: ~125-140 days.
- **Customer with mature data lake.** Compress Analysis to 10 days (data feeds already exist as queryable tables). Net: ~90 days.
- **Customer with no LP team yet.** Add 10 days into Functional Design and Training. Net: ~110 days.

For a 25-store mid-market retailer running a packaged retail-management platform (the Boutique Home & Garden archetype), expect ~110 days for Phase 1 with the same gate structure.

## What this shape does not cover

- Subsequent phases (Phase 2, 3+) — each is its own 100-day shape with reduced Analysis and Architecture, expanded Development.
- Multi-region deployment — adds a tenancy/data-residency stream not modeled here.
- Custom POS adapter development — modeled here as customer-side data-extract work, not vendor product development.
- Hardware procurement on the customer side — assumed parallel and pre-existing.

## Why this shape works

Three structural choices make the 100 days hold:

1. **Project Administration as continuous parallel.** It is not a phase that "ends" — the PM channel is the engagement's spine. Treating it as a phase would create a false gate at handover.
2. **Production Infrastructure parallels Validation, not Deploy.** This is what compresses the back end. If you serialize them you blow out by 15-20 days.
3. **Gates are binary, milestones are continuous.** Seven gates, ~20 milestones. The PM tracks milestones weekly; the steering group convenes only on gates.
