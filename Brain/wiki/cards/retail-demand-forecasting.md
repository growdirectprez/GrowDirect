---
card-type: domain-module
card-id: retail-demand-forecasting
card-version: 1
domain: merchandising
layer: domain
status: approved
agent: ALX
feeds: [retail-replenishment-model, retail-merchandise-financial-planning]
receives: [retail-merchandise-hierarchy, retail-site-management]
tags: [demand-forecasting, forecast, replenishment, seasonal, promotional, collaborative-forecasting, SOQ]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

The demand forecasting model: the components of a retail demand forecast, the parameter structure that drives accuracy, and the process for reviewing, overriding, and feeding forecast output into replenishment and financial planning.

## Purpose

Forecasting exists to enable continuous product availability by projecting demand before it occurs, not by reacting to stockouts after the fact. An accurate forecast drives replenishment quantities, sizes purchase commitments against actual expected demand, and feeds the financial planning process with a demand basis for OTB. A poor forecast — one that ignores seasonality, promotional impact, or new-item dynamics — produces either excess inventory or out-of-stocks, both of which destroy margin.

## Structure

**Forecast components** — A retail demand forecast is built from four independently computed and selectively combined components:

| Component | What it captures |
|-----------|-----------------|
| Basic demand | Baseline sales velocity from historical sell-through, adjusted for trend |
| Seasonal demand | Cyclical sales pattern: peak weeks, off-peak weeks, seasonal uplift factors |
| Promotional demand | Expected sales lift during defined promotional events; isolated so it does not corrupt baseline |
| Shrink factor | Expected loss rate applied as a multiplier to demand to size orders at the gross level |

Forecasts can be computed using any user-selected combination of these components. For most items, all four are relevant; for new items with no history, like-item forecasting uses a reference item's pattern.

**Forecast parameters** — Forecasting parameters are maintained at the item × site level. Key parameters include: the forecasting model in use (demand-based, inventory-based, order-up-to), the historical look-back window (in weeks), the seasonal profile assigned to the item, the promotional event calendar, and the minimum and maximum order constraints. Parameters are mass-maintained across merchandise and site hierarchies with effective dating — a single parameter change can be applied to a class across all stores in a climate region.

**Forecast schedule** — For most items, forecasting runs weekly. The forecast cycle: calculate demand forecast → review exception list (items where forecast variance from actuals exceeds threshold) → buyer or replenishment planner overrides where necessary → approved forecast feeds the replenishment process. Exception-first review keeps the process scalable across tens of thousands of SKUs.

**Promotional demand isolation** — Promotional demand must be isolated from baseline history. A week with a major promotional event should not inflate the baseline demand estimate for future non-promotional weeks. The forecasting system tracks promotional vs. non-promotional sales separately and excludes promotional periods from baseline calculations unless explicitly included.

**Collaborative forecasting** — In a more advanced configuration, vendors receive buyer-level sales forecasts and provide their own forward-looking demand estimates. Collaborative forecasting improves vendor fill rates by giving suppliers earlier visibility into order quantities. EDI 852 (Product Activity Data) enables automated data sharing. Collaborative forecasting is a vendor compliance dimension: vendors who commit to collaborative forecasting and miss it by more than the agreed tolerance are scored accordingly.

**Simulation capability** — Replenishment simulations must be runnable without creating actual purchase orders or deliveries. Simulations use production parameters but produce simulated suggested order quantities (SOQs) only, enabling buyers to test parameter changes before committing.

## Consumers

The Replenishment module reads the approved forecast as the primary input to suggested order quantity calculation. The Merchandise Financial Planning process reads forecast by item and store to build the sales assumption in the financial plan. The Vendor Agent shares forecasts with collaborative-forecasting-enrolled vendors. The Operations Agent monitors forecast accuracy (MAPE — Mean Absolute Percentage Error) by category and site, and alerts when accuracy degrades below a defined threshold.

## Invariants

- Promotional demand must be isolated from baseline forecasting. Allowing promotional events to inflate the baseline is the most common cause of post-promotional inventory excess.
- Forecast simulations must not affect production data. Simulation is a planning tool, not a production process.
- New item forecasting must use a designated like-item profile until sufficient history accumulates (typically 13+ weeks). Forecasting a new item with zero history and no reference produces a zero or noise forecast.

## Related

- [[retail-replenishment-model]] — consumes forecast as the primary demand input for SOQ calculation
- [[retail-merchandise-financial-planning]] — forecast provides the sales assumption for OTB and plan components
- [[retail-event-management]] — promotional event calendar drives promotional demand component
- [[retail-merchandise-hierarchy]] — hierarchy groupings enable mass parameter maintenance and forecast aggregation
