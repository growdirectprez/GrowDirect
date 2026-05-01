---
classification: confidential
type: founder-reference
date: 2026-04-26
event: Monday 2026-04-27 1pm PST — Bart Monahan call
related-linear: GRO-600
sources:
  - case-studies/canary-ncr-product-line-decision.md
  - case-studies/lawn-and-garden-rapidpos-suite.md
  - case-studies/lawn-and-garden-catz-phase1-diagnostic.md
---

# Bart Call Brief — Distilled L&G Strategy

## Page 1: Where We Are

### Canary positioning (one sentence)

Canary is the full SMB operating suite for L&G specialty retail running on the Counterpoint API backbone — delivered through Bart's Rapid POS VAR channel.

### NCR product-line decision (closed 2026-04-25)

**Counterpoint first** over Aloha and Voyix. Three load-bearing arguments:

- **Q-rule portability is ~80% from Square** — specialty retail substrate is the same shape; restaurants need a net-new Q-rule family. Adapter cost: ~26 eng-weeks for Counterpoint vs ~58 for Aloha.
- **A real first customer is in front of us** — the Boutique H&G chain, multi-store, Counterpoint-running. Aloha and Voyix have zero anchor customers in the pipeline.
- **Customer-routed access sidesteps the NCR-Voyix-as-competitor problem.** Counterpoint integration runs through the customer's license-holder + Bart's VAR. NCR Voyix corporate is the direct SMB-analytics competitor, not a partner.

Sequence: Counterpoint Q3 2026 (in flight under GRO-558) → Voyix re-eval gate Q2 2027 → Aloha as a separate restaurant-vertical motion only when independently funded or a concrete Aloha customer enters the pipeline.

### L&G operating reality (3 lines)

- **Apr-Sep produces 70-80% of annual revenue.** Perishable shrink is the dominant cost pressure — industry citation puts perishables at up to 78% of total L&G shrinkage.
- **Three customer tiers** — retail walk-in, landscaper on account, commercial project. Same plant, three prices. Landscaper-tier abuse is unmeasured today.
- **Cash-and-paper culture is the operational baseline.** Alt-payment rails (Zelle, Venmo, Cash App) increasingly normal for landscaper invoicing and back-door vendor payments to specialty growers.

### The prize (one line)

**2-4% of revenue per chain** across three buckets — perishable shrink reduction + multi-store visibility + landscaper-tier B2B AR control. For a $20M chain, $400K-$800K/yr. For a $50M chain, $1M-$2M/yr.

### One quotable line for Bart

> "Counterpoint reports answer 'what happened.' Canary answers 'what's wrong and what's about to go wrong.' These are not the same product."

---

## Page 2: What We Want from Bart

### VAR-channel positioning (one paragraph)

Rapid POS is the delivery channel; Canary is the operating-platform suite layered on top. Bart already carries the Counterpoint reseller relationships across L&G chains in his region — that is the channel asset, and we are not trying to displace it. Canary's value to Bart: a differentiated suite that turns a Rapid POS deployment into a higher-margin, higher-stickiness engagement. Canary's value to merchants: the full 13-module Canary spine (T R N A Q C D F J S P L W) instead of a stitched-together set of point solutions for LP, forecasting, scheduling, and B2B AR. Canonical positioning is already aligned: multi-store merchandising and store ops for SMB on the Counterpoint API backbone. We don't have to renarrate the company to make this work.

### 90-day deployment story (4 bullets)

- **Weeks 1-2 — Counterpoint API access stand-up.** Customer's `registration.ini` API user option enabled (paid Counterpoint add-on). NCR-issued APIKey installed; TLS 1.2 verified; Canary credentials (`<company>.<user>` Basic + APIKey header) bootstrapped.
- **Weeks 3-4 — Data sync.** Counterpoint adapter polling worker stood up; first Document/Customer/Item polls populate CRDM; multi-company resolved if needed.
- **Weeks 5-8 — Phase 1 priority modules online.** T (transactions), R (customer with three-tier resolver), F (tender + day-end close), L (basic), N (devices). First Q rules fire in dry-run; first 30-day VSM-style diagnostic produced.
- **Weeks 9-12 — Phase 2 catalog modules online.** S (perishable flag, mix-and-match groups, plant attributes) + P (derived pricing resolver — three-tier, markdown cadence). Full operating suite functional end-to-end.

### 4-tier packaging shape

- **Tier 1 — LP-Only** (Q + Fox + minimum T/R/N substrate): matches current Canary LP pricing baseline.
- **Tier 2 — Operating Suite** (Phase 1 + 2: T R N F L S P + Q + Fox): the L&G full-stack for single-store and small chains.
- **Tier 3 — Distribution Suite** (adds D + J): for 3-15-store chains running inter-store transfers + seasonal forecasting.
- **Tier 4 — Enterprise** (adds A + C + W): chains with B2B-heavy mix, asset tracking, work-execution rigor.

(Concrete pricing TBD; per-module activation enables a tiered conversation rather than an all-or-nothing pitch.)

### What we want from Bart this call

1. **Pipeline intel.** Which L&G chains in his current Rapid POS pipeline look best-fit for Canary co-deployment after the Boutique H&G chain anchor lands?
2. **Channel mechanics.** What does the VAR-margin conversation look like — standard Rapid POS reseller margin plus a Canary suite-margin layer? Referral split shape?
3. **Joint-customer engagement shape.** When a chain wants both Bart's Counterpoint deployment expertise and Canary's suite, what does the handoff look like? Rapid POS leads on POS deployment, Canary technical co-deploys on the suite layer?
4. **Reference customers.** Any Rapid POS chains in his current book that would be willing to act as Phase 0/1 reference deployments after the Boutique H&G chain proof point lands?

### One quotable line to anchor the ask

> "We're not a loss-prevention point solution. We're the operating platform — and your VAR channel is the highest-leverage path to L&G chains in your region."

---

## Appendix: References

- **NCR product-line ADR (GRO-560):** `Canary-Retail-Brain/case-studies/canary-ncr-product-line-decision.md` — three-option Morrisons-frame evaluation, recommendation, decision gates.
- **L&G RapidPOS Suite playbook (GRO-588):** `Canary-Retail-Brain/case-studies/lawn-and-garden-rapidpos-suite.md` — suite composition, 90-day onboarding, 4-tier packaging.
- **L&G CATz Phase I diagnostic (GRO-596):** `Canary-Retail-Brain/case-studies/lawn-and-garden-catz-phase1-diagnostic.md` — demand-side narrative, as-is per-module pain, prize sizing.
- **Companion script:** `Brain/raw/inbox/monday-call-script.md` (HIDE-scope; gitignored; agenda + speaking script).
