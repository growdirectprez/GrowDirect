---
title: Co-sell Assets
tags: [pitch, leave-behind, co-sell]
last-updated: 2026-04-30
---

# Co-sell Assets

Leave-behinds, talking points, and conversation frames for VAR co-sell conversations. These assets are designed for the Counterpoint VAR who is introducing Canary to an existing merchant account.

---

## Co-sell talking points — for the VAR conversation

**The one-sentence version for the merchant**

> "Counterpoint is your transaction engine. Canary is the intelligence layer that tells you what the engine is actually doing — and where the losses are."

**The problem statement that lands**

Every Counterpoint merchant generates more data than they see. Cost-of-goods on every line item, tender classification on every transaction, AR balances on every customer account, inventory snapshots, drawer flags — all of it is in the system. Most of it has never been wired to a detection layer. The result: shrink gets written off to plant death. Margin erosion happens at the item level and shows up in the P&L, not at the register. Cash discrepancies accumulate across sessions before they appear in the bank.

Canary closes that gap. No changes to the POS workflow. No cashier retraining. No migration.

**The ask that fits the VAR relationship**

Lead with the four-week audit. It is non-disruptive, bounded in scope, and produces a documented baseline the merchant owns regardless of what they do next. It gives the VAR a professional-services engagement with a clear deliverable. And it almost always surfaces a finding the merchant was not expecting.

---

## Three-pillar targeting — which merchants to call first

### Pillar 1 — Lawn & Garden

**Why first:** Lead vertical. RapidPOS / Rapid Garden POS footprint in SoCal. Armstrong Garden Centers (31 stores, ESOP, 136 years) is the target proof case.

**Dominant pain:** Tribal horticultural knowledge that walks out the door every season. ALX as the store's expert — plant diagnosis, zone-aware recommendations, live inventory match. The knowledge vault is the competitive moat.

**Qualifying question:** "When a seasonal employee leaves, does that knowledge stay in the business?"

**Pitch trigger:** Any multi-store garden center whose staff turnover is seasonal, whose shrinkage is attributed to plant death, or whose customers are already asking AI assistants what to plant.

### Pillar 2 — Farm / Ranch / Firearms / Hardware

**Why second-highest priority:** 3,800-store TAM (US). Deep regulatory complexity (ATF, NICS, EPA, state ABC, CDFA) that Counterpoint POS flags can't manage alone.

**Dominant pain:** Multi-state regulatory compliance managed through manual POS parameter files. One override on a federally licensed firearm is an FFL violation. One below-floor sale on a controlled item is a legal event.

**Qualifying question:** "How does your system handle a sale that needs age verification, state compliance check, and federal NICS in the same transaction?"

**Pitch trigger:** Any Counterpoint merchant with firearms, ag chemicals, OTC pharmaceuticals, or quarantine-sensitive live goods that ships across state lines.

### Pillar 3 — Regulated Beverage

**Why:** Highest margin premium of the three verticals. State-auditor accountability is a forcing function; audit-defensibility is not a nice-to-have, it's a statutory requirement.

**Dominant pain:** Cash-heavy LP exposure + compliance burden + audit record gaps that create legal liability for the operator.

**Qualifying question:** "If a state auditor walked in tomorrow and asked to trace every cash transaction this week back to a verified receipt, how long would that take your team?"

**Pitch trigger:** Any large independent wine / spirits chain, high-volume liquor retailer, or control-state system operation on Counterpoint.

---

## The engagement progression

The product is not a feature. It is a three-stage commercial model the VAR sells as a progression:

| Stage | Duration | What the merchant gets | What the VAR bills |
|---|---|---|---|
| **Audit / Health Check** | 4 weeks | Documented baseline — every Counterpoint data gap mapped, every module gap identified, shrinkage estimate, OTB overrun estimate | Professional services engagement; Canary-assisted but VAR-delivered |
| **Transformation Engagement** | 4–9 months | Full Phase 1 activation (S → I → F → R → D → Q), detection live, Chirp alerts running, Fox case management operational, ALX agent in place | Delivery margin on the engagement; Canary provides platform + SDD library |
| **Operating System Mode** | Ongoing | Continuous detection, LP visibility, OTB enforcement, vendor scorecard, domain knowledge vault active | Platform subscription share; low VAR support burden; high merchant stickiness |

**Lead with the audit.** It is the lowest-friction entry. It produces a concrete deliverable. And it converts to transformation at high rates once the baseline is documented.

---

## Objection responses

**"My customer already has Counterpoint reports."**

Counterpoint reporting is a snapshot. It tells you what happened at end-of-day. Canary tells you what's happening now — and flags the specific events that don't match expected patterns. The difference is detection versus documentation.

**"My customer can't afford another subscription."**

The audit produces an ROI estimate before any subscription starts. In every garden center engagement to date, the identified shrinkage and OTB overrun exceeds the platform cost before the audit is complete. The merchant pays with recovered margin, not new budget.

**"We already have a custom LP module."**

Custom LP modules catch what they were programmed to catch. Canary catches pattern deviations across all five signal families (tender, inventory, discount, return, account) simultaneously. They're not the same problem space.

**"We don't want to change the POS workflow."**

Canary does not touch the POS workflow. It reads Counterpoint data via the REST API. Cashiers, store managers, and customers see nothing different. The detection layer runs above the POS, not inside it.

---

## Quick reference — Phase 1 module activation sequence

For the VAR who is running their first installation. The sequence enforces substrate dependencies — do not attempt to activate Q without S, I, F, and R in place.

```
S  → Store & Device        (operational context — first)
I  → Item Catalog          (cost and margin floor)
F  → Finance / Tender      (money classification)
R  → Customer              (who is buying, AR status)
D  → Distribution/Inventory (on-hand vs. what the register says)
Q  → Loss Prevention       (detection fires when S/I/F/R/D diverge from expected)
```

Full activation guide: [Deployment Guide](../deployment/index)

---

## Contact

Canary on Counterpoint is available through your Counterpoint VAR relationship. To schedule an audit engagement or request a sandbox access, contact gclyle@growdirect.io.
