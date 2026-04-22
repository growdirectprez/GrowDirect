---
title: Secure → Canary Handoff
date: 2026-04-21
type: brief
sprint: secure-sprint-1
status: working-draft
---

# Secure → Canary Handoff

## Purpose

Translate 10+ years of Secure IP into concrete ADOPT / ADAPT / REJECT calls for Canary. This is the "what did we already learn 15 years ago that Canary should (or should not) port" brief. Each pattern cites a source file; each gets a specific Canary recommendation and a proposed follow-up action.

Not a design doc — a brief for the person (PhD / Architect) writing the Canary design docs that will act on these patterns. The Owl system consumes these recommendations via PhD methodology; not a reader of this brief.

## Patterns

### 1. CRDM schema abstraction — **ADOPT**

**Source:** `~/secure/Secure 5 Solution Architecture.docx` §2.5 Data Layer + `~/secure/S5 On Premise Solution Architecture.docx`. See also [[Brain/wiki/secure-architecture|Secure Architecture § CRDM + persistence stores]].

**What Secure did.** CRDM (Common Retail Data Model) sits between "raw retailer POS / ERP data" and "detection + case-management logic." Retailer data lands via Standard Data Load, gets ETL'd through the integration tier (Python + transient PostgreSQL), then persists in CRDM-shaped SQL Server tables. Everything upstream is ETL; everything downstream operates on the stable CRDM shape. The detection and case layers never touch retailer-specific data shapes directly.

**Why it matters for Canary.** Canary has the same problem: multiple POS sources (Square today, Clover / Toast / Lightspeed / Shopify tomorrow) with different transaction shapes. Canary's multi-POS adapter pattern is solving exactly what CRDM solved. CRDM is 10 years of prior art to study.

**Recommendation.** Canary's SDD on multi-POS architecture ([[docs/sdds/canary/multi-pos-architecture-proof|Multi-POS Proof]]) should explicitly reference CRDM as a design precedent. Before inventing new abstraction shapes, read what CRDM abstracted and why (transaction, tender, line item, discount, operator override, etc.).

**Follow-up.** File Linear issue under Canary Architecture: "Compare Canary sales schema against Appriss CRDM — identify gaps and naming divergences." Priority medium — unblocks future POS-source work.

---

### 2. Factboard vs Case distinction — **ADOPT**

**Source:** `~/secure/Secure 5 Solution Architecture.docx` §2.5 Data Layer, persistence stores table. See [[Brain/wiki/secure-platform-overview|Platform Overview § Persistence stores]].

**What Secure did.** Secure had **two separate stores** for investigation data: Factboard (pre-case investigation scratchpad — "watching, not yet a case") and Case Management (formal cases with evidence chain). Analysts could collect observations in Factboard without committing to a case; promotion to Case was a deliberate step. This avoided two failure modes: (a) case inflation from speculative observations and (b) lost signals from observations nobody bothered to formalize.

**Why it matters for Canary.** Canary's Fox cases jump directly from alerts to cases. There's no intermediate "I'm watching this employee / merchant, multiple signals are accumulating, not yet actionable" tier. Users either escalate or drop, nothing in between.

**Recommendation.** Add a Factboard analog to Canary Fox. Candidate name: "watchlist" or "monitoring" tier, separate from cases. Requirements: (a) time-boxed observations, (b) accumulates alerts without escalating to case, (c) promotion to case is explicit.

**Follow-up.** File Linear issue: "Fox watchlist tier — pre-case observation store (Factboard analog)." Priority low — Canary Fox cases are working; this is enhancement not gap.

---

### 3. Inbound / Fulfillment / Outbound rule taxonomy — **ADOPT**

**Source:** `~/secure/Secure Omnichannel Overview-Oct2018.pdf` — three-stage shrink decomposition. See [[Brain/wiki/secure-omnichannel|Secure Omnichannel § Inbound/Fulfillment/Outbound]].

**What Secure did.** Every shrink source in retail was grouped under one of three process stages:
- **Inbound** — warehouse shipments, vendor-direct-to-site, positive adjustments
- **Fulfillment** — sales, transfers to store/DC, internal theft, waste
- **Outbound** — customer returns (in-store, online, call center), return to vendor, negative adjustments

**Why it matters for Canary.** Canary's Chirp rules are grouped operationally (by tier, by risk score) but not by **where in the operational process they fire**. A merchant asking "what rules cover my return process?" has to scan the full rule list to find the answer.

**Recommendation.** Add Inbound/Fulfillment/Outbound as a first-class grouping dimension for Chirp rules. Not a replacement for tier — an additional tag. Make rule intent legible by operational stage.

**Follow-up.** File Linear issue: "Chirp rule taxonomy — add operational-stage grouping (Inbound / Fulfillment / Outbound)." Priority medium — discoverability win with low implementation cost.

---

### 4. "Configuration surface is the enemy of onboarding" — **ADOPT**

**Source:** `~/secure/Secure Lite Overview.docx` — the Lite product specifically removes configuration surface. See [[Brain/wiki/secure-lite|Secure Lite]].

**What Secure did.** Secure 5 was enterprise-capable but required weeks of consulting to stand up. Secure Lite removed: designer access, permission groups, data policy editing, export manager, user tasks, teams, file app, developer mode, metric manager, job system console. What's left: three fixed roles, pre-baked dashboards, standard risk dictionary, out-of-box Instant Analytics. Onboarding went from weeks of consulting to turnkey.

**Why it matters for Canary.** Canary is SMB-first. Every preference toggle, every "Advanced settings" section, every optional step is onboarding friction. The Canary onboarding loop should be measured by "how many config decisions does a merchant face before they see their first dashboard?" Each decision is a potential drop-off.

**Recommendation.** Audit every Canary config surface. For each toggle, ask: "Does the default serve 80% of merchants correctly? If yes, hide the toggle behind an Advanced section. If no, change the default." Target: a merchant can go from Square-OAuth to populated-dashboard with zero config decisions.

**Follow-up.** File Linear issue under Canary Product: "Onboarding config audit — count decisions required before first dashboard." Priority high — directly impacts conversion.

---

### 5. Pre-baked defaults (Factory + Lite) — **ADOPT**

**Source:** `~/secure/Factory Overview v2.pptx` + `~/secure/Secure Lite Overview.docx`. See [[Brain/wiki/secure-architecture|Secure Architecture § The Factory]] and [[Brain/wiki/secure-lite|Secure Lite]].

**What Secure did.** The Factory was a single consolidated pre-wired install of all Secure 3.5 apps working together — EBR + Cashier Performance + Audit & Survey + Refund Management + Foundation Management + Incident Management + Risk Management. The philosophy: ship opinionated defaults, not a la carte; standardize what "Secure 3.5" means across clients.

**Why it matters for Canary.** Canary has 29 Chirp rules across 3 tiers. Are the defaults tuned to produce useful alerts out of the box for a typical merchant, or do they require per-merchant tuning? If every merchant needs tuning before they see value, the "pre-baked defaults" discipline is missing.

**Recommendation.** Establish explicit default personas for Canary Chirp tuning (e.g., "small single-location retail," "multi-location retail," "food service," "service business"). Each persona gets a tuned threshold set that's known to produce useful alerts without tuning. Applied automatically at onboarding based on Square merchant data.

**Follow-up.** File Linear issue: "Chirp rule persona packs — default tunings by merchant type." Priority medium — feeds into onboarding audit above.

---

### 6. Three-role operator model — **ADAPT**

**Source:** `~/secure/Secure Lite Overview.docx` (same three roles in Lite as in Secure 5). See [[Brain/wiki/secure-platform-overview|Platform Overview § Three-role operator model]].

**What Secure did.** Executive / Analyst / Investigator. Every variant of Secure shipped the same three roles. Executive = dashboards + rollups, no investigation. Analyst = search composer + risk-dictionary + case routing. Investigator = works cases.

**Why it matters for Canary.** Canary's current operator model is flatter (merchant admin → standard user). That's right for small merchants. Multi-location retailers with dedicated LP functions will want a role split.

**Recommendation.** Not an immediate Canary change. When a merchant customer crosses a scale threshold (multiple locations or dedicated LP headcount), introduce the three-role split as the Enterprise tier feature. Do NOT force the split on small merchants.

**Follow-up.** File Linear issue under Canary Product: "Enterprise tier roles — three-role split (Executive / Analyst / Investigator) for multi-location merchants." Priority low — wait until Canary has enterprise-scale demand.

---

### 7. Expansion-path pricing — **ADAPT**

**Source:** `~/mnt/nas-archive/Work/Clients/KROGER/Max Replacement Appriss follow-up.docx` — POS T-log @ $660K/y + $450K install, with DSD @ $350K and Pharmacy @ $500K as post-install add-ons. See [[Brain/wiki/secure-client-kroger|Kroger § Pricing structure]].

**What Secure did.** Core product (POS T-log EBR) carried the install + first-year discount. Module expansions (DSD, Pharmacy, eCommerce) priced as standalone additions post-install. Enterprise agreement structure, no user/data limits. Annual subscription + one-time install.

**Why it matters for Canary.** Canary's pricing today is Square-merchant-tier based on transaction volume. Future Canary modules (payroll risk, inventory risk, ecommerce-channel integration) will need a pricing shape. The Secure "core plus expansion" model is one pattern.

**Recommendation.** When Canary adds a second or third Chirp pack (or adjacent capability like payroll-risk scoring), consider the Secure shape: core pricing covers the base product + install + core rules; new packs are additive modules with their own pricing. Do not require re-negotiating the full contract to add one module.

**Follow-up.** Not actionable until Canary adds its second distinct pack. Note in business-model brief for future reference.

---

### 8. Workaround catalog as detection signal — **ADOPT**

**Source:** `~/mnt/nas-archive/Work/Projects/Kroger CRP/Workarounds.doc` — 2001 Kroger Retek workaround catalog (dummy classes, new-store hold buckets, separate POs per OTB month, etc.). See [[Brain/wiki/secure-client-kroger|Kroger § Workarounds catalog]].

**What Secure did (and Canary doesn't).** Real retailers run real workarounds around ERP limitations. A "dummy class for dollar inventory adjustments" is a legitimate accounting workaround, not fraud — but it can look like fraud to a detection rule that doesn't know the context.

**Why it matters for Canary.** Canary Chirp rules flag anomalies. Square merchants run their own workarounds (test-mode transactions, training transactions, end-of-day corrections, cash-drawer moves, dummy items for float accounting). Without a reference of known-workaround patterns, Chirp rules will produce false positives on legitimate operational practice, which trains merchants to ignore alerts.

**Recommendation.** Build a "known retailer workarounds" reference dataset that Canary consults when scoring alerts. An alert matching a known-workaround pattern gets de-prioritized (shown but not escalated) unless it deviates from the typical workaround shape.

**Follow-up.** File Linear issue: "Chirp rule context — workaround-aware scoring (reference dataset of legitimate operational anomalies)." Priority medium — directly impacts Canary's "signal over noise" philosophy.

---

### 9. Data retention is a negotiation, not a fixed number — **ADOPT**

**Source:** `~/mnt/nas-archive/Work/Clients/KROGER/Max Replacement Appriss follow-up.docx` — Appriss opened at 7 weeks retention, Kroger demanded significantly more, resolution was two-tier (detail + aggregated metrics). See [[Brain/wiki/secure-client-kroger|Kroger § Data retention]].

**What Secure did.** Offered a default detail-retention window tuned to the infrastructure cost, plus a data-aggregation strategy for longer-term metrics. Retention was an architecture decision tied to storage cost and compliance, not a fixed product parameter.

**Why it matters for Canary.** Canary's retention policy today is implicit (Valkey for hot data, Postgres for persistent). There's no explicit merchant-visible retention commitment. Enterprise merchants will eventually ask "how long do you keep my transactions?" — the answer needs to be documented, tiered, and negotiable.

**Recommendation.** Two-tier retention policy: (a) **detail retention window** — full transaction + alert + case data available for a specified period (candidate: 90 days for standard tier, 1 year for enterprise); (b) **aggregate retention** — risk metrics, trend data, rolled-up case statistics retained longer for benchmarking. Document explicitly in Canary's compliance / privacy page.

**Follow-up.** File Linear issue under Canary Ops: "Retention policy documentation + tier structure." Priority medium — compliance-relevant, needed before enterprise sales.

---

### 10. On-premise deployment model — **REJECT**

**Source:** `~/secure/Secure 5 Solution Architecture.docx` §3+4 — Secure was architected for on-premise enterprise retail IT, HP hardware, SQL Server Enterprise, Windows Server, on-retailer-premises. Kroger chose self-hosted over SaaS.

**What Secure did.** Sold on-premise as the default, SaaS as the alternative. Retailers wanted self-hosted for IT governance, data residency, PCI compliance reasons. Each install was a capital-project-shaped engagement: hardware procurement, IT cooperation, multi-week rollout.

**Why Canary should NOT adopt this.** Canary is SaaS-only by design. The target merchant (Square-connected, SMB or mid-market) is SaaS-native. On-premise is a wrong turn.

**But what Canary SHOULD consider.** Enterprise merchants will eventually ask for data residency or dedicated-VPC deployment. The path is **private-cloud / single-tenant VPC**, not full self-host. Deploy Canary into a dedicated AWS account + VPC per enterprise customer, managed by Canary ops. The customer gets isolation; Canary keeps the operational model.

**Follow-up.** File Linear issue under Canary Infra: "Enterprise VPC deployment tier — single-tenant isolation without full self-host." Priority low — wait until enterprise demand materializes.

---

### 11. Microsoft-centric stack — **REJECT**

**Source:** `~/secure/Secure 5 Solution Architecture.docx` §2 — ASP.NET MVC, Windows Services, MSMQ, SQL Server, IIS, Windows Integrated Authentication.

**What Secure did.** Full Microsoft stack. Made sense for its era + enterprise retail IT norms (Windows-heavy shops, .NET developer market, SQL Server licensing relationships).

**Why Canary should NOT adopt this.** Canary's Python/Flask/Postgres/Valkey/Ollama stack is correct for its target market. SaaS-native, open-source, Linux-friendly, AI-composable. Revisiting the stack decision is not on the table.

**Follow-up.** No action. Noted for completeness because "what Secure did" should not be confused with "what Canary should do."

---

## Explicitly NOT ported

- **14-store persistence decomposition** — too many boundaries for a multi-tenant SaaS. Canary's 4-schema model (app / sales / fox / metrics) is the right grain for Canary's scale. Don't copy Secure's 14.
- **Secure Lite as a SKU** — Canary is already the simplified product by design. There's no "Canary Enterprise" to strip down to make a "Canary Lite." Skip the variant pricing play until there's a Canary Enterprise to differentiate from.

## Summary count

10 patterns tagged: **6 ADOPT, 2 ADAPT, 2 REJECT**. Plus 2 "explicitly NOT ported" for clarity.

Linear issues to file (future — not yet created):
- Canary Arch: Compare Canary sales schema against Appriss CRDM (Pattern 1)
- Canary Fox: Factboard watchlist tier (Pattern 2)
- Canary Chirp: Inbound/Fulfillment/Outbound taxonomy (Pattern 3)
- Canary Product: Onboarding config audit (Pattern 4)
- Canary Chirp: Persona-based default tunings (Pattern 5)
- Canary Product: Enterprise three-role split (Pattern 6, low priority)
- Canary Chirp: Workaround-aware scoring (Pattern 8)
- Canary Ops: Retention policy tiers (Pattern 9)
- Canary Infra: Enterprise VPC tier (Pattern 10, low priority)

## Sources

See individual pattern citations. Primary source wiki articles:
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/wiki/secure-architecture|Secure Architecture]]
- [[Brain/wiki/secure-lite|Secure Lite]]
- [[Brain/wiki/secure-omnichannel|Secure Omnichannel]]
- [[Brain/wiki/secure-client-kroger|Secure Client: Kroger]]
