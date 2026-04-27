---
date: 2026-04-22
type: wiki
status: active
tags: [growdirect, warchest, chirp, alerts, wizard]
sources:
  - docs/_archive/ip-vault/warchest/sources/05-the-chirp.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
----

**Wiki:** [[Brain/Home|Home]]

# The Chirp
*Spine: ACT 3C | Manifesto: III.3*

**Status:** 📝 DRAFT — Extracted from Manifesto III.3 + Strategic Thesis v1.0. Awaiting Jeffe review.

---

## The Interface Between Detection and Action

Loss prevention has always had a last-mile problem. Enterprise systems detect anomalies. They generate reports. They populate dashboards. Then they wait — for someone with the training, the time, and the analytical fluency to interpret the data and decide what to do. For a single-location merchant running a restaurant or retail shop, that person does not exist. There is no loss prevention department. There is no data analyst. There is the owner, and there are the eighteen other things the owner is already doing.

The Chirp solves the last mile.

A Chirp is a plain-language alert delivered to the merchant's phone. It does not say "anomaly detected." It does not present a chart. It says: *Your drawer was short $18 on the morning shift. Maria Santos was on register. Want to look into it?*

Concrete. Specific. Actionable. The merchant knows what happened, who was involved, and what to do about it — in a single sentence.

## One Tap to Resolution

One tap on the Chirp launches a guided investigation wizard. Six steps. Under eight minutes from alert to documented resolution. The wizard walks the merchant through the entire process:

- Acknowledge the alert
- Review the detection details
- Capture the merchant's response
- Document evidence or notes
- Record the outcome
- Close the investigation

Every action is timestamped. Every step writes to the Fox evidence chain — INSERT-only, hash-chained, and anchored to the Bitcoin time chain via Ordinal inscription. The merchant finishes the wizard. The investigation is documented. The evidence is permanent and tamper-proof. No legal pad. No memory. No "I'll deal with it later."

The merchant does not need training. They do not need to understand forensic accounting. They follow the wizard and produce an evidence-grade record that would hold up in any employment dispute, insurance claim, or legal proceeding.

## The Product Is the Analyst

Enterprise loss prevention requires specialists to interpret data — analysts who translate statistical outputs into business actions. That model works at scale, where the cost of a dedicated LP team is a rounding error on revenue. It does not work for the 3.7 million Square merchants who operate at thin margins and cannot justify a single additional headcount for shrinkage.

Canary's Chirps use AI to collapse the interpretation layer. The detection engine evaluates 26 rules across eight fraud categories — payment anomalies, cash drawer variances, refund patterns, void abuse, timecard irregularities, gift card manipulation, discount abuse, and loyalty fraud. When a rule fires, the system does not output a statistical alert. It translates the detection event into plain English, identifies the who, what, when, and where, and delivers a Chirp that requires no interpretation.

The merchant does not need to be a data analyst. The product is the analyst.

## Connect, Toggle, Watch

Onboarding to Chirps is frictionless by design. The merchant connects their Square account via OAuth — a single authorization flow. They toggle on the alert categories they care about. Canary starts watching.

There is no BI tool to learn. No reports to configure. No dashboards to build. No IT department to call. The detection engine runs continuously against the merchant's live transaction data, evaluating every webhook event against the active rule set. When something fires, a Chirp appears on the merchant's phone. When nothing fires, the system is silent.

This is not a monitoring platform the merchant logs into. It is a guardian that speaks up only when something needs attention.

## What Sits Underneath

The Chirp is the surface. Underneath it sits the Canary Retail Data Model — a three-database PostgreSQL architecture that normalizes Square's raw API events into a canonical retail data warehouse. Every transaction, every refund, every timecard punch, every cash drawer event flows through the Triple Subscriber Pipeline: hashed and sealed for immutability, parsed and routed for detection, batched and inscribed for permanent anchoring.

The detection engine is the first application on this foundation. But the CRDM enables everything that comes after: demand forecasting, labor optimization, inventory management, vendor analysis, menu engineering, seasonal trend detection. The merchant signs up for loss prevention alerts. They stay for the data platform.

The Chirp is how they walk in the door.

---

**Source:** Strategic Thesis v1.0 + Manifesto III.3
**Manifesto tag:** `Manifesto: III.3`
**Filled:** February 27, 2026 — ALX (B-059 Phase 1)

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/warchest/sources/05-the-chirp.md` — the war-chest source this card summarizes
