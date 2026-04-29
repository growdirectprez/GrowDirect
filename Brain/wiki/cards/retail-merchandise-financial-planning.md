---
card-type: domain-module
card-id: retail-merchandise-financial-planning
card-version: 1
domain: finance
layer: domain
status: approved
agent: ALX
feeds: [retail-purchase-order-model, retail-replenishment-model, retail-operations-kpis]
receives: [retail-demand-forecasting, retail-inventory-valuation-mac]
tags: [OTB, open-to-buy, merchandise-planning, financial-planning, gross-margin, inventory-turn, MFP, budget]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

Merchandise financial planning (MFP): the process that integrates financial goals with merchandising objectives, produces the OTB (Open-to-Buy) that gates purchase commitments, and provides the measurement framework for tracking merchandising execution against plan.

## Purpose

MFP translates strategic business objectives — growth targets, margin goals, inventory efficiency targets — into a purchasing plan that buyers can execute. Without MFP, buyers operate on intuition and historical habit; OTB is either unconstrained (leading to inventory excess) or non-existent (leading to stockouts). MFP is also the accountability mechanism: the plan is the commitment, and variance to plan is the signal that something is wrong in execution or in the original assumption.

## Structure

**OTB definition** — Open-to-Buy is the quantity and cost value of goods a location can receive over a defined period without exceeding planned inventory levels. OTB = Planned Net Sales + Planned End-of-Period Inventory + Planned Markdowns − Beginning Inventory − Open Orders not yet received. OTB is maintained at the buyer × department × week level. It is a financial constraint on purchasing, not a replenishment suggestion.

**Plan components** — A complete merchandise financial plan includes, at minimum:

| Component | What it captures |
|-----------|-----------------|
| Sales at retail | Total sales, comp-store sales, new-store sales, sales per store-week |
| Cost of goods sold | Receipts at cost, adjusted for all allowances and freight |
| Gross margin | Sales − COGS, at % and $ |
| Inventory at cost | Beginning and end-of-period book inventory |
| Net receipts | Planned incoming merchandise at cost |
| Markdowns | Planned permanent and promotional markdowns |
| Shrinkage | Planned shrink factor applied to inventory |
| Rebates | Vendor rebates expected at the buyer level, not just company level |
| Marketing allowances | Co-op and promotional funding from vendors |

**Planning hierarchy** — Plans are developed top-down from corporate financial targets, then reconciled bottom-up from buyer-level build-ups. The reconciliation produces the working plan. Plans exist at corporate, division, department, class, and vendor levels. Weekly plans are allocated from seasonal plans.

**Performance measures:**

| Measure | Definition |
|---------|-----------|
| Average retail | Average selling price per unit |
| Initial markup % | (Retail − Cost) ÷ Retail |
| Gross margin % | Gross profit ÷ Net sales |
| Inventory turnover | Net sales ÷ Average inventory at retail |
| Weeks of supply | On-hand units ÷ Average weekly sales rate |
| Comp-store sales % | Sales growth vs. prior year, same-store base |
| Penetration % | Department/class sales as % of total, for margin and gross profit |

**Revision cycle** — Plans are not static. MFP requires a regular revision cadence: weekly OTB reconciliation, monthly plan update, and a full seasonal reforecast at defined milestones. A plan that is not revised as actual data accumulates is not a plan — it is a historical artifact. The revision trigger is variance to plan, not the calendar.

## Consumers

The Buyer uses OTB as the gate before committing to a purchase order. The Replenishment module reads planned weeks-of-supply targets to calibrate suggested order quantities. The Finance module reads plan components for period-end gross margin reporting. The Operations Agent monitors OTB utilization by department and alerts when buyers are consistently under-utilizing OTB (leaving sales on the table) or over-utilizing it (risking inventory excess). Pricing analysts read weeks-of-supply and turn rates to identify markdown candidates.

## Invariants

- OTB is a hard constraint on PO creation for planned purchases. Buyers may not exceed OTB without buyer-level authorization. The authorization creates an audit trail.
- Rebates must be figured into gross margin planning at the buyer level, not just at the company financial roll-up. A buyer who ignores vendor rebates in their plan is understating their true margin.
- Plan components must be consistent with the retail accounting method in use (cost method or retail method). Mixing accounting methods within a plan produces meaningless margin metrics.

## Related

- [[retail-purchase-order-model]] — OTB gates every PO commitment
- [[retail-demand-forecasting]] — forecast provides the sales assumption that drives plan components
- [[retail-inventory-valuation-mac]] — MAC is the cost basis for plan components
- [[retail-operations-kpis]] — turnover, weeks of supply, and GM% feed the KPI dashboard
