---
status: private-working-thesis
date: 2026-04-20
audience: Greg (founder), GrowDirect strategy
not-for: HOA board packet, public site, Angelique's client channel
---

# HOA Platform — Commercial Viability Thesis

Private working doc. Not for the Community of Abalone Cove board packet. Captures the business-plan thread that emerged from the CoAC reference-customer build: **Cove the platform can be a productized, multi-tenant HOA SaaS, and the CoAC instance is the 0→1 case**.

## Observation

Building the CoAC instance exposes that Cove already has:
- Multi-org architecture (`organization_id` on every table)
- Role-based access (admin, board, inspector, member, public, ARC, and now president)
- Governance engine (proposals, ballots, elections, proceedings) with Davis-Stirling compliance baked in (AB 502/2159/2460/130, SB 900)
- Secret-ballot separation (`ballots` has no `member_id`; `ballot_envelopes` under RLS) — this is **the hard part** of a compliant HOA voting platform, and it is already built
- Vault + compliance dashboard mapped to §4525, §5300, §5310, §4950/4955, §5550, §4765, §5650, §4530 — the full disclosure surface
- APN-first data model (every entity resolves to a parcel) — matches how HOAs actually think
- Lot-based email identity with Cloudflare Email Routing — generalizable
- ARC module (meetings + reviews) — most small HOAs don't have a usable one
- Parcel map with GeoJSON and Leaflet — high-value differentiator

The CoAC deployment's production-mode gate (`COVE_DEPLOYMENT_MODE=production`) is the first white-label flag. Every HOA tenant is a packaging decision on top of the same codebase.

## Market

Rough sizing:
- ~370,000 HOAs in the U.S. (CAI 2024)
- ~55% under 100 units (target segment): ~200,000
- Of those, large fraction are self-managed by volunteer boards using email + Dropbox + paper ballots — the exact problem set Cove solves
- California alone: ~50,000 HOAs under Davis-Stirling; most with the same bylaw-modernization, §4525, paper-ballot challenges CoAC faces

Commercial HOA software is dominated by Buildium, AppFolio, Condo Control, PayHOA, TownSq, Vantaca. Of those:
- AppFolio / Vantaca target professional management companies (enterprise)
- Buildium targets landlords/property managers (adjacent)
- PayHOA, Condo Control target small HOAs directly but lead with dues collection
- **No dominant player leads with governance + compliance + document disclosure for self-managed small HOAs**

That gap is the wedge.

## Pricing thesis

User's working instinct: "probably all could pay a few $4 a month for an app and website, same way Luxury Presence dominates real estate."

Model comparison:

| Tier | Target | Monthly (per HOA) | Features |
|---|---|---|---|
| Starter | 20–100 units, self-managed | $49 | Vault + directory + §4525 + publish cascade + paper tally |
| Standard | 100–500 units | $99 | + elections + meetings + ARC + basic treasury |
| Pro | 500–2,000 units | $249 | + audit log export + custom domain + advisor seats |
| Enterprise | 2,000+ or management companies | custom | + white-label + SLA + integration |

Compare: Luxury Presence real estate websites at $400–$1,200/mo dominate a market that once thought "$20/month Weebly is enough." Professional, compliant, well-designed platforms win the budget line once the board sees the alternative (management company at $150+/mo, or a breach).

At $49/mo × even 500 HOAs = $24.5k MRR / ~$300k ARR. 1,000 HOAs = $49k MRR / $588k ARR. These are realistic multi-year targets from inbound + referral, not aggressive.

## Architecture path — reference customer → SaaS

**Phase 0 (now):** CoAC as single-tenant production deployment. Hand-held.

**Phase 1:** Multi-tenant on the same Postgres with stronger `organization_id` enforcement everywhere. Per-tenant subdomain (`<hoa>.abalonecove.org` or `<hoa>.cove.app`). Per-tenant Cloudflare route. Manual onboarding.

**Phase 2:** Self-service onboarding wizard. Per-tenant database (not just row-level) via Postgres schema-per-tenant or DB-per-tenant. Billing via Stripe. Tenant provisions governing docs, imports parcels, seeds directory, configures their own president/board/ARC.

**Phase 3:** White-label. Management companies license Cove to run N HOAs. Different brand per customer. SSO.

The CoAC work advances Phase 0 → Phase 1. The production-mode gate is the first Phase-1 primitive.

## Adjacent vertical — builder/contractor project sites

User note: "I know a few other builders need websites for their projects."

Observation: the blueprints Cove gates off in production mode (`map_bp`, `parcels_bp`, `archive_bp`, `research_bp`, `agent_bp`) are **exactly what a builder running a residential-development project needs**:
- Parcel map + APN data for the site
- Document archive (permits, grading plans, ARC applications, inspection reports)
- Timeline (proceeding entries)
- Ownership history / title records

A `COVE_DEPLOYMENT_MODE=builder` variant would:
- Enable: map, parcels, archive, research
- Disable: governance, voting, elections, directory
- Simplify: single-project scope rather than whole-community

Same codebase, different deployment mode. Different customer.

Value prop for a builder:
- Transparent project page for neighbors, city staff, investors
- Document-of-record archive for the life of the project
- Cloudflare-fronted, secure, professional
- ~$99/month vs. $3,000+ for a custom WordPress build

Greg already has a builder network via Angelique's Compass relationships + the RPV permit-architect work. The sales channel exists.

## Sales and channel

Zero paid acquisition initially. Channels:

1. **Angelique's Compass network (CoAC reference)**. Compass agents list homes in HOA-governed communities constantly. Every listing triggers a §4525 package request from the HOA. Angelique can introduce Cove to any HOA board where she's listing — the platform solves a problem the selling agent experiences directly.

2. **RPV / South Bay HOAs (CoAC proximity)**. Rolling Hills, PV Estates, PV Country Club, and a dozen others have similar Davis-Stirling constraints and similar volunteer-board dynamics. A public CoAC success story becomes the case study.

3. **Builder network (builder vertical)**. Greg's contacts in the RPV permit-architect world become the inbound for Phase-2 builder deployments.

4. **CAI (Community Associations Institute) chapters**. CA North, CA South, Orange County — small sponsorship budgets, high signal-to-noise for target personas.

5. **Davis-Stirling legal Twitter / substacks**. Adrian Adams, Beverly Anderson, the handful of HOA attorneys who publish — they are the gatekeepers.

## Unit economics (back of envelope)

Per-tenant marginal infra cost:
- Compute: shared across tenants; ~$0.50–$2.00 per tenant at scale
- Storage: ~$0.50 per tenant (documents, backups)
- Bandwidth: negligible with Cloudflare
- Email: ~$0.01 per message; ~80 lots × 10 notices/year = 800 msgs × $0.01 = $8/year = $0.67/mo
- **Total marginal: ~$2–$4/tenant/month**

At $49 MSRP → ~$45 gross margin per tenant per month → ~$540/year per tenant contribution margin.

Fixed costs (platform team, compliance counsel retainer, marketing): absorb at ~200 tenants.

## Risks

- **Compliance liability.** If a Cove-run election is challenged, platform gets named. Mitigation: paper-ballot primary (already spec'd), Inspector-of-Elections keeps authority, platform stays non-binding. Insurance: E&O policy before onboarding tenant #2.
- **Multi-tenancy bugs leak PII between HOAs.** Mitigation: per-tenant database at Phase 2; security audit + penetration test before GA.
- **HOA buying behavior is slow.** Boards don't adopt software quickly. Mitigation: free-for-first-year for reference customers; case studies; Angelique channel.
- **Enterprise players move down-market.** Mitigation: focus on the un-served small-HOA segment; small HOAs don't want enterprise complexity.
- **Regulatory changes.** AB XYZ could require something Cove doesn't do. Mitigation: retainer with a Davis-Stirling-literate attorney; built-in quarterly legislative review.

## Explicitly not in the HOA board packet

Nothing in this document goes to the CoAC board. The board's concern is their association. The commercial thesis is a founder concern. Mixing them risks the perception that the CoAC deployment is a sales play rather than a community-first volunteer contribution — and it is categorically not. The board packet names hosting cost as a transparent line item; nothing more.

## Next moves (for Greg)

Short term (coupled to the CoAC deployment):
- Ship CoAC to production (this plan)
- Document the HOA case study (neutral: operational outcomes, not commercial)
- Stay disciplined on feature gating so production mode truly is the product

Medium term:
- Add `COVE_DEPLOYMENT_MODE=builder` as a second packaging (after CoAC is stable)
- Land one builder customer (Greg's network)
- Publish a bylaw-modernization template package (marketing asset)

Long term:
- Multi-tenant onboarding wizard
- Stripe billing
- First non-Greg customer

## Related docs

- [docs/superpowers/specs/2026-04-20-coac-president-demo-tenant-design.md](../superpowers/specs/2026-04-20-coac-president-demo-tenant-design.md) — CoAC reference-customer spec
- [docs/superpowers/plans/2026-04-20-coac-hoa-qa-instance.md](../superpowers/plans/2026-04-20-coac-hoa-qa-instance.md) — the 10-chunk implementation plan
- [Cove/docs/proposals/2026-04-20-hosting-cost-brief.md](../../Cove/docs/proposals/2026-04-20-hosting-cost-brief.md) — the public-facing hosting-cost brief for the HOA board

---

*Confidential working thesis · GrowDirect strategy · 2026-04-20*
