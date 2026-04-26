---
classification: internal
type: wiki
sub-type: relationship-profile
date: 2026-04-26
last-compiled: 2026-04-26
needs-review: 2026-06-26
source: Grok team update 2026-04-26 (SaaS PM — Canary / RapidPOS L&G Initiative)
companion: Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context.md
companion: Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md
---

# Bart McCleskey — Rapid Garden POS (Relationship Profile)

Primary VAR contact and decision-maker for any partnership bundling Canary as the enterprise backend layer for Rapid POS's lawn & garden customer base. **Monday call: 2026-04-27 1:00 PM PST.**

## Identity

| Field | Value |
|---|---|
| Name | Bart McCleskey |
| Title | Owner / President |
| Company | Rapid Garden POS (sub-brand of Rapid POS LLC) |
| Location | San Diego, CA — 8555 Aero Dr, Ste 310 |
| Email | bart@rapidpos.com |
| Phone | (619) 754-4100 / (619) 309-8001 |
| Website | rapidgardenpos.com |

## Background

- **Tenure.** Owner since ~April 2007 — 18+ years in the role. Long-tenured operator, not a recent hire or a pivot exec.
- **Education.** Texas A&M University.
- **Prior work.** Business management and consulting background before Rapid POS.
- **Track record.** Has produced training content (EMV webinars, Counterpoint University adjacent). Credible inside the Counterpoint ecosystem — not just a reseller, but a practitioner who teaches it.
- **Company scale.** 11-50 employees. Rapid POS founded 1985; green-industry vertical focus under the Rapid Garden POS brand.

## What Rapid Garden POS actually does

Rapid Garden POS is Rapid POS's garden-center specialization — **NCR Counterpoint deployed and configured for the green industry**, with vertical-specific customizations layered on top. The platform includes:

- Mix-and-match pricing (pots + plants + accessories)
- Fractional unit tracking (partial flats, cut quantities)
- Grow-care instruction printing (customer-facing, at POS)
- Retail + wholesale workflows on the same system
- "Connected Commerce" branding — their phrase for the integrated H&G stack

All of this sits on top of Counterpoint's API surface — the same Document omnibus, Item master, and REST endpoints Canary has been mapping. Rapid Garden POS's value is configuration and training, not a separate codebase.

**Other Rapid POS verticals** (not Bart's primary focus, but context for the org): gun stores, feed & tack, beverage, wine & spirits.

## Why he is the right person

Bart controls the full VAR bundle: hardware, implementation, training, and support for L&G Counterpoint deployments. Any Canary partnership that goes to market through a Rapid POS channel goes through Bart. Specifically:

1. **He owns the retailer relationships.** The L&G retailers Canary targets (Armstrong Garden Centers archetype, 10-100 location independents) are Rapid Garden POS customers. Bart is their incumbent trusted advisor — not a cold prospect.
2. **He controls the integration narrative.** When Bart tells a customer that Canary is the "enterprise layer on top" — non-disruptive, doesn't touch their Counterpoint — he carries credibility that a cold Canary pitch does not.
3. **He has the vertical domain depth to evaluate the build plan.** 18 years in garden-center POS means he will immediately validate or push back on the Canary module assumptions. The Bart Monday call is the highest-leverage assumption-resolution opportunity we have before Phase 1 adapter work starts.

## Canary fit for his customer base

| Canary capability | Why it fits Rapid Garden POS customers |
|---|---|
| Perpetual ledger over Counterpoint API | Customers are on Counterpoint; Canary adds the inventory-position and movement-audit layer they don't have today |
| LP rules (Q module) | Garden-center operators have loss-prevention blind spots — transfer loss, live-goods write-offs, discount abuse — that Counterpoint doesn't surface |
| OTB guardrails (J + C modules) | Multi-location H&G buyers need spend constraints; Counterpoint's OTB is UI-only |
| Distribution recommendations (D module) | Rebalancing stock across 3-8 locations is a whiteboard exercise for Rapid Garden POS customers today |
| B2B commercial intelligence (C module) | Landscaper / wholesale / project-tier accounts are 20-40% of revenue; Counterpoint doesn't surface B2B risk or credit posture |

## Monday call agenda relevance

Two load-bearing questions for the Bart call (per dispatch `2026-04-26-spine-functional-decomposition-remaining.md`):

1. **L and W strategic decision** — Does Bart's customer base want native labor scheduling or do they pay separately for Homebase / Deputy / TimeForge? His answer shapes whether L is a ★ Canary-native build or a ◯ vendor-integration cell.
2. **Assumption-resolution agenda** — 71 assumption markers across 11 completed module cards; highest-priority gaps needing real-customer input: transfer workflow conventions (ASSUMPTION-D-03/04), AR module usage (ASSUMPTION-C-05), live-goods write-off Document type (ASSUMPTION-J-12), buyer tolerance for "plan in Canary, execute in Counterpoint" UX (ASSUMPTION-J-08).

## Positioning for the call

Per memory `project_canary_canonical_positioning.md`:

- **WHAT:** Multi-store merchandising and store ops for SMB, on top of the Counterpoint API backbone
- **WHO:** Rapid POS delivery experts
- **HOW:** Our method is CATz

Frame: non-disruptive enterprise layer. Canary doesn't replace Counterpoint — it adds the analytics, LP rules, OTB enforcement, and distribution intelligence that Counterpoint's UI doesn't surface. Bart's customers don't have to change their POS workflow. The pitch is additive.

**Do NOT** mention LP/analytics framing when positioning to NCR — but with Bart, the LP and analytics language is fine. Bart is the customer-side channel; the NCR-as-competitor framing applies to any communication that could reach Voyix.

## Related

- `Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context.md` — full three-actor engagement context (NCR Voyix / Rapid POS / H&G retailer)
- `Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md` — Counterpoint vs. Rapid Garden POS technical relationship clarification
- `Brain/wiki/rapid-pos-counterpoint-market-research-tam.md` — TAM ~1,200 US garden centers / ~9,000 SMB across Counterpoint VAR verticals
- `Brain/wiki/rapid-pos-counterpoint-user-pain-points.md` — 10 pain themes + 10 FAQs from public-community research
- `Brain/wiki/garden-center-operating-reality.md` — vertical domain context
- `Brain/wiki/socal-home-garden-target-customers-brief.md` — call-prep brief (if present)
- `Brain/raw/inbox/monday-call-script.md` — HIDE-scope founder script (gitignored, local only)
