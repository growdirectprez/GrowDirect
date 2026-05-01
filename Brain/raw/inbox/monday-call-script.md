---
classification: HIDE — Geoff eyes only
type: call-script
date: 2026-04-25
call: Monday 2026-04-27 1pm PST
attendees: Geoff (founder) + Tim Mooney (organizer, ex-IBM Fresh & Easy commercial) + Bart (VAR / whitelabel Rapid POS)
status: prep-draft (revise after final fact-checks)
---

# Monday 2026-04-27 1pm PST — Bart Call Script

## Strategic frame (read first; internalize before the call)

### The pitch in three lines (lead with this exact framing):

> **What we do:** Multi-store merchandising and store ops for SMB, on top of the Counterpoint API backbone.
>
> **Who we are:** Rapid POS delivery experts.
>
> **How we do it:** Our method is CATz.

Three lines, in this order. Internalize them. They're the canonical positioning per memory `project_canary_canonical_positioning.md`. Use them when Bart asks "what do you do?"

This is **not** just a sparring-partner-recruitment call (the original Tim framing). Bart is a **VAR with an NCR Counterpoint contract**, specifically a **whitelabel Rapid POS reseller**. His customers run Rapid POS = Counterpoint underneath. **He's our friendly channel into the Counterpoint specialty SMB world.**

Two parallel objectives for the 45 minutes:

1. **Sparring** (Tim's original goal) — pressure-test Canary's offering against Bart's experience; harden the pitch through his scrutiny
2. **VAR-partnership exploration** (the upgrade) — surface whether Canary fits inside Bart's offering as a value-add for his customer base

**The pattern:** Square + Canary at the small-merchant tier → NCR Counterpoint + Canary at the specialty-SMB tier. Same architecture. Same value prop. More headroom because Counterpoint's data substrate is richer (per-Document audit log, multi-authority tax, drawer sessions, line-level pricing-rule capture, category margin targets).

**Why "Rapid POS delivery experts" is the right WHO for Bart:** Bart is a Rapid POS reseller (sales/relationship side). We're delivery experts (execution side). Complementary, not competitive. The positioning lets him hear "this is the missing piece I don't deliver well" rather than "this competes with what I sell." The 25-year arc, the Secure 3.5 archive (now sanitized into CATz Phase III templates), the Solution Map matrix — all underwrite the delivery-expertise claim.

**Competitive context Bart will recognize:**

- **NCR Voyix is the competitor**, not the partner. They have their own LP/analytics surface; Canary plays in that surface. Bart understands this — VARs know their platform vendor's product portfolio.
- **Rapid POS is the friendly channel** — they're a Voyix VAR like Bart. Canary inside Bart's offering doesn't displace Rapid POS; it extends it.
- **The customer is the principal** for integration access. Not NCR. Not Rapid. The customer's Counterpoint license + their VAR's API option enablement is what Canary plugs into.

**Pitch register: soft + invite pushback.** Per Tim's framing. Don't pitch this as a finished product seeking a customer; pitch it as "we built something that should fit your world; help us validate it."

## 45-minute call shape

| Time | Phase |
|---|---|
| 0–5 | Tim opens; intros; frame (sparring-partner + offering exploration) |
| 5–15 | 25-year arc — quick (PwC/Monday → IBM BCS → today's CATz/Canary). The architectural rationale for what Canary is. |
| 15–25 | Live demo or screenshare — Counterpoint integration capability + Module Q rule catalog + Solution Map matrix. **Material:** the wikis + SDD landed today. |
| 25–35 | Bart's reactions / questions / pushback. **Listen mode.** |
| 35–42 | Specific asks — graceful, not transactional |
| 42–45 | Close — leave-behind, next-step framing |

## Lines that must land

**Opening frame (use the canonical three lines):**

> "What we do is multi-store merchandising and store ops for SMB, on top of the Counterpoint API backbone. Who we are is Rapid POS delivery experts. How we do it is CATz — our method."
>
> "Tim suggested you'd be the right person to pressure-test this with."

**On the architectural rationale (the IBM BCS thread):**

> "When IBM BCS made its big bet on horizontal services, it solved one problem and opened another — integration always lagged. The market never solved that lag. CATz is the methodology that addresses it; Canary is what shipping looks like when you actually do."

**On Counterpoint substrate vs. what Voyix offers:**

> "Counterpoint exposes more than most platform vendors' standard analytics surfaces capture. Per-Document audit log, multi-authority tax breakdown per ticket, drawer-session correlation, line-level pricing-rule capture. There's a real LP layer to be built on that substrate that Voyix doesn't deliver well. We've been mapping it module-by-module against the retail spine."

**On the customer being the principal:**

> "Integration access routes through the customer's Counterpoint license, not through Voyix's good will. The customer enables their API option; we plug into that. Their data, their authority, our analytics. That's the architecture."

**On VAR-channel fit (when the conversation opens to it):**

> "We've been thinking about how this lands. We don't displace Rapid POS or Counterpoint; we ride alongside. For a VAR, Canary is a value-add — analytics + LP that strengthens your offering without overlapping with what Rapid does. Same way Square partners get value from Canary on the lower tier."

## Specific asks (graceful, in priority order)

These are the asks. Drop them naturally during 35-42 — don't list them like a checklist:

1. **Tell us about your Voyix contract structure.** What you have access to, what Rapid permits you to do, where the boundaries sit. Helps us understand the landscape we'd be plugging into.
2. **Tell us about your customer base.** Verticals, store counts, store sizes. Patterns. We've been working from public data; ground truth from a real VAR is gold.
3. **Developer credentials situation.** If we wanted to test Canary against a real Counterpoint instance — even a lightly-used customer or a sandbox you operate — what's the path? Are you registered for an APIKey? Could we operate under your VAR umbrella as an integrated app, vs. applying to NCR directly?
4. **Your whitelabel agreement with Rapid.** Does it permit you to sub-package additional offerings (like Canary) to your customers? Or is the whitelabel scope tighter than that?

**The frame for these asks:** we're not asking him to commit. We're asking him to teach us what's possible. He's the expert; we're the new entrants. Information-flowing-toward-us is the dynamic.

## Demo path (for the 15-25 slot)

What to show. What to skip.

**Show:**

- **Solution Map matrix** (CATz `proof-cases/specialty-smb-counterpoint-solution-map.md`) — the spine × platform-coverage matrix. Visual. Land that Canary thinks at the level of "where's the gap in your stack" rather than "buy our product."
- **Module Q rule catalog** (`Brain/wiki/canary-module-q-counterpoint-rule-catalog.md`) — 23 rules grouped into 10 categories, all Counterpoint-substrate-aware. Pick 2-3 rules to walk through. Best candidates: Q-IS-02 (cash-vendor-payment allow-list — shows we get specialty-retail reality) + Q-DM-01 (discount-cap exceeded — universally relatable) + Q-AT-01 (Document-edit-after-payment — shows we read the audit trail Voyix doesn't expose well).
- **OpenAPI spec** (`docs/sdds/canary/ncr-counterpoint-openapi.yaml`) — 95 operations across 71 paths. Don't open the YAML; show that it exists, validates, is the contract Canary's adapter will be built against.
- **Live Canary on Solex** (the working Square pipeline) — proves the architecture isn't theoretical. Same architecture lifts to Counterpoint.

**Skip:**

- Long architecture lectures. Bart is framework-fluent (Accenture / IBM / Gartner / Starbucks background). He'll get it from one diagram + a few rule examples.
- Sales-deck framing. Direct, serious, tangible. No corny / AI-sounding language.
- Pricing. Not Monday. He'll ask; deflect: "we'll work that out when we know what shape this takes for your world."

## Bart-specific objection bank

Pattern-matched to his pedigree (Accenture / IBM / Gartner / Starbucks / NCR-Rapid era) per Tim's profile.

**"How is this different from what Voyix's analytics layer does?"**

Voyix's standard analytics is reporting + dashboards over the same data. Canary is detection-rule-driven loss prevention with a real-time substrate-consumption pattern that fires on patterns, not just reports them. Plus: vertical-aware allow-listing (cash-vendor payments, plant-write-offs, item-code drift) that off-the-shelf retail analytics can't tune for specialty SMB.

**"Counterpoint has been around forever. What's the moat?"**

The moat isn't "we figured out how to call the API." It's the substrate-consumption pattern + the rule catalog + the vertical-aware allow-lists + the agent-layer interface. Voyix doesn't deliver this because it would compete with their own offerings; we deliver it because we don't have that conflict.

**"Why would a VAR like me sell another vendor's product alongside my own?"**

Because it strengthens YOUR offering. Customers are increasingly sophisticated; SMB retailers want LP + analytics + scheduling without 5 separate tools. If your offering bundles Canary, your win rate goes up, your contract size goes up, your churn goes down. We're not competing with you; we're a multiplier.

**"What about the customer's data — privacy, security, legal?"**

Per-tenant isolation. Read-only against the customer's Counterpoint API. Customer's authority for access; their VAR (you) for the API option. Standard SaaS data-protection stack (encryption at rest, customer-controlled deletion). We don't take ownership; we operate.

**"Sounds early. Why should I share my customer base?"**

You're not. We're asking what verticals you serve, what scales — patterns. Specifics come later, only if/when you decide there's something here. Today is information-flow toward you; tomorrow can be partnership-shape if it makes sense.

**"How do I know you'll be around in 3 years?"**

Honest answer: you don't, and neither do we for sure. But: solo-founder runway, substantive product already in production for one POS, methodology vault that's been 25 years in the making. Track record + work shipped. Not vapor.

## Lines to AVOID

- Hype. ("Game-changing.") — Bart will tune out.
- Mystery. ("There's something we can't talk about.") — kills trust.
- Vague TAM. ("Massive market.") — Bart will ask for specifics; if you don't have them, don't claim them. We have ranges (~1,200 garden centers on Counterpoint; ~9,000 across all SMB verticals), say the ranges.
- Promises about NCR. ("We're going to partner with Voyix.") — they're a competitor; this would either be wrong (if we don't) or weak-positioning (if we do).
- Anything that sounds like a sales pitch in the first 25 minutes. Soft register; let him drive.

## Leave-behind

The Bart 1-pager (CATz `welcome-journey/companion-onepager.md` — to be produced separately if not done yet). Plus: live URLs to CATz, Canary-Retail-Brain, the Solution Map proof case (per Gate 2 = A: live URLs).

Send via email after the call with a one-line: "Thanks for today; here's the package we walked through. Take a look at your pace; happy to follow up whenever."

## Sunday-evening checklist

- [ ] Tim has the prebrief in his inbox (so it's there Monday morning)
- [ ] Bart 1-pager ready as PDF + link version
- [ ] Demo path tested locally (Canary running, Solex emitting, Chirp/Fox detecting; Counterpoint deep-dive wikis/SDDs accessible)
- [ ] Live URLs working if Gate 2 = A (`growdirect-llc` org or equivalent stood up + repos pushed)
- [ ] This script reread; key lines internalized, not memorized

## Post-call

- Capture Bart's reactions in `Brain/projects/<bart-slug>.md` (memory-bus ingestion ready)
- If developer credentials offered: store in Canary's secret-store per rotation runbook; treat as first production Counterpoint test surface
- Send leave-behind email
- Tim debrief

## Related

- `Brain/dispatches/2026-04-25-monday-bart-call-prep.md` — original Saturday-resume dispatch (now superseded by this script + companion materials)
- Memory `project_bart_var_partnership.md` — Bart-as-VAR / whitelabel-Rapid-POS context
- Memory `project_ncr_voyix_is_competitor.md` — competitive framing
- Memory `project_tim_mooney_contact.md` — Tim's contact + Cloudflare allowlist status
- `Brain/wiki/ncr-counterpoint-api-reference.md` — Counterpoint substrate detail
- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — rule examples for the demo
- `CATz/proof-cases/specialty-smb-counterpoint-solution-map.md` — Solution Map for the demo
- `Brain/wiki/rapid-pos-counterpoint-market-research-tam.md` — TAM ranges if Bart asks
- `Brain/wiki/rapid-pos-counterpoint-user-pain-points.md` — pain themes if Bart probes "what's wrong with the current state"
