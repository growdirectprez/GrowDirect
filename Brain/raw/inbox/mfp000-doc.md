---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/Mfp000.doc.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# Mfp000.doc

## Source
File: `Brain/raw/.extract/BP/Mfp000.doc.md`
Size: 20,370 bytes

## Raw content
 TOC \o "1-2" I. Merchandise Planning	 GOTOBUTTON _TOC411253714   PAGEREF _TOC411253714 3
A. Objectives	 GOTOBUTTON _TOC411253715   PAGEREF _TOC411253715 3
B. Critical Success Factors	 GOTOBUTTON _TOC411253716   PAGEREF _TOC411253716 3
C. Assumptions	 GOTOBUTTON _TOC411253717   PAGEREF _TOC411253717 3
D. Requirements	 GOTOBUTTON _TOC411253718   PAGEREF _TOC411253718 3
E. Performance Measures	 GOTOBUTTON _TOC411253719   PAGEREF _TOC411253719 6
F. Issues	 GOTOBUTTON _TOC411253720   PAGEREF _TOC411253720 6
G. Better Practices Recommendations	 GOTOBUTTON _TOC411253721   PAGEREF _TOC411253721 7
H. Reports	 GOTOBUTTON _TOC411253722   PAGEREF _TOC411253722 8
II. Create Annual Merchandise/Store Forecast	 GOTOBUTTON _TOC411253723   PAGEREF _TOC411253723 9
A. Objectives	 GOTOBUTTON _TOC411253724   PAGEREF _TOC411253724 9
B. Requirements	 GOTOBUTTON _TOC411253725   PAGEREF _TOC411253725 9
C. Reports	 GOTOBUTTON _TOC411253726   PAGEREF _TOC411253726 10
III. Align Annual Merchandise/Store Plans	 GOTOBUTTON _TOC411253727   PAGEREF _TOC411253727 10
A. Objectives	 GOTOBUTTON _TOC411253728   PAGEREF _TOC411253728 10
B. Requirements	 GOTOBUTTON _TOC411253729   PAGEREF _TOC411253729 10
C. Reports	 GOTOBUTTON _TOC411253730   PAGEREF _TOC411253730 10
IV. Create Vendor Plans	 GOTOBUTTON _TOC411253731   PAGEREF _TOC411253731 10
A. Objectives	 GOTOBUTTON _TOC411253732   PAGEREF _TOC411253732 10
B. Requirements	 GOTOBUTTON _TOC411253733   PAGEREF _TOC411253733 10
C. Reports	 GOTOBUTTON _TOC411253734   PAGEREF _TOC411253734 11
V. Allocate Weekly Plans	 GOTOBUTTON _TOC411253735   PAGEREF _TOC411253735 11
A. Objectives	 GOTOBUTTON _TOC411253736   PAGEREF _TOC411253736 11
B. Requirements	 GOTOBUTTON _TOC411253737   PAGEREF _TOC411253737 11
C. Reports	 GOTOBUTTON _TOC411253738   PAGEREF _TOC411253738 11
VI. Track Progress and Revise Plans	 GOTOBUTTON _TOC411253739   PAGEREF _TOC411253739 11
A. Objectives	 GOTOBUTTON _TOC411253740   PAGEREF _TOC411253740 11
B. Requirements	 GOTOBUTTON _TOC411253741   PAGEREF _TOC411253741 12
C. Reports	 GOTOBUTTON _Toc411253742   PAGEREF _Toc411253742 12


Merchandise Planning
Objectives
To provide actionable plans that drive sales and gross margin in accordance with Company’s business objectives and growth plans

Merchandise Planning is the process that integrates and reconciles financial goals with merchandising objectives.  It translates the strategic merchandising vision into an execution plan for the organization.  It serves as a communication vehicle and a means for integrating important input from other areas of the company.  After development, the plan serves as a tool to measure the success of the merchandising vision and execution plan.

Open-To-Buy (OTB) is the quantity of goods that a store can receive in stock over a stated time without exceeding its planned inventory levels.

Critical Success Factors
Support the corporate merchandising vision
Integrate and reconcile financial goals with merchandising objectives
Translate the strategic merchandising vision into an executable plan for the organization
Increase sales and profits
Redeploy assets in reaction to market changes
Improve inventory control
Track performance of merchandising efforts at corporate, store and individual levels
Provide vision into success or failure of the merchandising strategy

Assumptions
Sales and Margin report should be created on main system and not through data warehouse.
Rebates should be figured into the bottom line at the buyer level instead of only at the company level.

Requirements
Although certain segments of this process are available within SAP, they do not seem to be linked together into a single integrated process.  In creating our target process we have attempted to link the best of current and "best" retail practices with new techniques made possible by the Forecasting Module in SAP.  Retailers need the ability to systemically link these components.

Components of the plan include, but are not limited to:
Sales at retail
Total Sales
Comp Store Sales
New Store Sales
Sales per Store Week
Cost of Goods Sold
Gross Margin
Inventory at cost
Net Receipts at cost
Markdowns
Shrinkage
Rebates
Marketing Allowances
Performance Measures include, but are not limited to:
Average Retail
Percentage Change to Last Year
Penetration Percentage for Sales, Gross Margin, and Gross Profit
Percent to Sales
Initial Markup
Gross Margin %
Gross Profit %
Turnover
Weeks of Supply
GMROI
Multidimensional Environment:
Allows plans to be developed in a three-dimensional environment where merchandise hierarcy, site hierarchy, and time increment plans are all developed in concert.

Allows plans to be viewed and analyzed based on "people reporting" alternative hierarchies (buyers, planners, inventory managers, and distributors), as well as merchandising hierarchies.  This is only a reporting requirement.
Allows the development of annual merchandise plans by month, developed at the division, department, class, and/or merchandise category level with the ability to allocate down to the weekly level once plans have been approved.
Allows the development of annual store plans by month, developed at the division, department, class, and merchandise category level with the ability to allocate down to the weekly and daily level once plans have been approved.
Ability to "slice" time history any way a merchant deems necessary for comparison purposes, for example an adjustment for 53 vs. 52 week year, and Easter.  This allows seasonal sales to be based on relative time frames.
Allows plans to be developed at varying levels based on business requirements (i.e. Consumables will plan to the article level and Hardgoods to the Merchandise Category level).
Allows plans to be developed with "partial" details.  For instance, only key items need to be planned at the article level.  The remainder of the plan can be lumped into a "other" bucket.
Ability to define the planning components by level.  For instance, sales may be planned at the daily level, but not inventory.  If this functionality is used, not all roll up/middle out/roll down functionality will be activated.
Ability to view and utilize last year history at all levels of the plan.

Calculation Requirements:
Ability to enter either the component or the performance measure (i.e. enter gross margin dollars or percentage) and have the system calculate the missing variable.
Ability to plan and review plans in units and dollars as needed.
Ability to enter values in units or dollars and have the system automatically calculate the missing variable.
Ability to define the specific calculations and performance measures used.
Ability to allocate universal dollar/percent volume spreads.
Ability to roll up plans to a higher level (based on user-defined parameters) when lower level changes are applied.
Ability to roll down plans to lower levels (based on user-defined parameters) when high level changes are made.
Ability to middle out plans to both higher and lower levels (based on user-defined parameters) when changes are made to middle layers.
Ability to reconcile store and merchandise plans, based on user-defined parameters, when changes are made to either component.
Plan Versions:
Maintain a proposed and working plan, in addition to the original plan, for comparison purposes.
Ability to report on the actual and forecasted results against the proposed, working, and original plans.
Ability to require management approval before a plan can be formally changed from proposed to the working plan.
Provide the ability to lock plans at any level.  When plans are locked the system notifies the user of its inability to resolve imbalances through the use of roll up or roll down functionality.

Reporting Requirements:
Provides merchandise category and store location views.
Ability to create exception reporting when individual plan performance measures fall above or below user-defined plan tolerances.
Ability ot utilize drill down functionality in all reporting.
Ability to support graphical displays of plan and history components and performance measures.

Misc. Requirements:
Plan information feeds the OTB process.
Performance Measures
See above.
Jobs Analysis
All jobs will be primarily performed by buyers, merchandise managers, and merchandising management, although additional input will be provided by the executive committee, pricing analysts, inventory managers, divisional inventory managers, space management, and financial budgeting.

Issues
Is it practical / within scope to pursue a true merchandise planning process as part of the target system?
Is the new-store opening/planning process in the scope of the PAWS2000 implementation? Does new-store opening/planning require its own process? In any case, don't forget about these sub-processes.  How will new store plans be entered into the merchandise/store plan?  How will we enter the effects of cannabalization and increase competition?
Is co-op part of the merchandise plan? Can we put rebates into the merchants' bottom line?
Phil Murphy has requested that we save 6 years of daily sales information at a high-level in order to support the planning of holiday sales.

Better Practices Recommendations
Merchandise Planning:
Develop an approved high-level Merchandise Plan which serves as the basis for:
Merchandise plans at the class / sub-class level
Store plans
Assortment plans
Vendor plans
Develop the merchandise plan using the following steps:
Generate plan targets from history and financial targets.
Develop tops-down plan from historical and trend data.
Develop bottoms-up plan using store plans and assortment plans.
Reconcile tops-down and bottoms-up plans.
Utilize the merchandise plan as the basis for performance monitoring (subject to later revisions)
Develop merchandise plans at the sub-class / class level within the context of the high-level Merchandise Plan.
Utilize Open-to-Buy Planning.
Generate store plans for categories with stable assortments from replenishment and planogram input.  Roll up chain-wide plans from store-category and reconcile with tops-down plan.
Update plans with actuals for tracking actual performance to plan and for open-to-buy purposes.
Develop store category / sub-category plans to link space planning, drive corporate growth opportunities and monitor store inventories.
Conduct weekly reviews of actual performance vs. plan.  Variances outside pre-established parameters, caused by business conditions become the basis for considering a plan revision.
Conduct a formal plan review at the end of each fiscal period.  As required, the following should be done:
Revise assortment plan for forward periods.
Update merchandise plan while retaining the original approved plan for reference and incentive purposes.
Integrate merchandise, assortment and store planning.
Integrate space planning (visuals and marketing) with merchandise and assortment planning.
Merchandise plans are selectively developed below the department level to focus on opportunity categories and items.
The level of detail in the Merchandise Plan may vary based on the category ; for example replenishment categories are typically planned in greater detail.
Planning elements include:
Sales ($ + units) - including promotions (tracked separately as well)
Gross Margin ($ + %)
Inventory ($ + units)
Receipts ($ + units)
Comp-Store Sales
Maintained or cumulative markup
Initial markup
Markdowns
Shrink

Open-to-Buy:

Directly integrate OTB with the merchandise planning process at the chain level and the purchase order management process, as well as, with up-to-date information on inventory status to provide the initial open-to-buy calculation.
OTB guides the approval process which can range from as minor a role as monitoring and flagging certain orders and conditions to an:
Auto approval process based on a pre-defined rule set (e.g. hold orders for higher level approval, reject orders (based on rules) and refer them back to originator for adjustment).
Approval is handled as follows:
All replenishment orders receive automatic approval, subject to certain department limits of being “overbought.”
All orders within divisions that are within OTB limits are approved subject to certain screening rules that departments/divisions may want to impose.
Non-replenishment overbought conditions must be resolved and orders approved individually.
Forward Buys that satisfy guidelines are approved subject to preset overall parameters and limits.
OTB should “look ahead” so unusually large orders placed early in the OTB period can not lock out important orders that may come up later in the period, particularly basic replenishment item orders.
OTB is generated weekly based on the weekly sales and inventory plan at the class level.  (assumes weekly merchandise planning)
OTB is monitored at the class level and enforced at the department level.
OTB is adjusted to incorporate approved forward buys.

Reports
Merchandise Plan
See components and performance measures above.
Create Annual Merchandise/Store Forecast
Objectives
To create a merchandise/store forecast utilizing the methodology provided by SAP.
In this step, SAP forecasting functionality is utilized to create an article/site level forecast for the coming year.  This forecast is summarized into relevant categories and compared to last year history.  Then, the forecast is adjusted based on proposed assortment changes, and new store and remodel plans.

Requirements
Ability to utilize the SAP forecasting module to produce article/site forecast for the upcoming planning period, usually one year.
Ability to utilize or not utilize promotional demand as part of the base forecast based on user definition.  Frequently, the same promotion occurs every year at the same time.  This demand should be included in the base forecast.
Ability to move demand in response to changes in the calendar.  This would be used in to change the timing of events and advertising, to adjust from a 53 to 52 week year, and to move a holiday, such as Easter.
Ability to summarize the individual article/site forecasts into a total company within the merchandise categories and across categories into the divisions, departments, and classes.
Ability to summarize the individual article/site forecasts for each location within and across merchandise categories.
Ability to summarize the daily/weekly forecasts and history into months.
Ability to roll down changes at the month level into the daily/weekly details based on user-defined parameters.
Ability to present the base forecast in a structured report that includes similarly summarized history from last year and performance measure calculations.
Ability to utilize the high-level assortment strategy to adjust the forecast at all levels (article, merchandise category, class, department, division, total company) and to perform roll up and roll down reconciliation as required.
Ability to utilize the store opening and remodel strategy to adjust the forecast at the site level and to reconcile to the merchandise category as needed.
Ability to simulate new store opening sales based on a similar sites or the average new opening performance last year.
Ability to define the store roll up/roll down reconciliation process.  Historical sales would be the most likely characteristic, other characteristics, such as size, location, surrounding market, climate, etc., may be used.
Ability to recognize and adjust for store opening, remodel, and closure dates in the store forecast.
Ability to adjust store forecasted sales based on anticipated cannibalization from our own stores, as well as, changes in the competitive environment.

Reports
Merchandise Plan
See components and performance measures above.
Align Annual Merchandise/Store Plans
Objectives
During this process, the Merchandise/Store Forecasts are aligned with the Financial Plan and adjusted for any input from the Executive level.
Requirements
Ability to recognize variances between the Financial Plan and the Merchandising/Store Forecast.  The Financial Plan may not be developed within SAP, but may need to be imported from an external software package.
Ability to allocate universal dollar/percent volume spreads.
Ability to have multiple levels of field staff review plans and suggest changes.
Ability to automatically approve suggestions (as defined above) within user-defined parameters.
Ability to review unapproved changes and approve or disallow as necessary.
Ability to lock plans based on Executive approval.
Reports
Merchandise Plan
See components and performance measures above.

Create Vendor Plans
Objectives
During this process, vendor plans are developed within the merchandise categories.  These vendor plans are then summarized across the merchandise category into company-wide vendor plans.
Requirements
Ability to automatically create vendor forecasts at the merchandise category level based on last year history.
Ability to manually adjust vendor forecasts using inputs from Assortment Planning, Vendor Management, and Merchandise Plan developed above.
Ability to plan for all the components of the Merchandise Plan and for several new components, including:  Purchases, Customer Returns, Returns to Vendor, and Full Cost (see gap #MIV040).
Ability to track plan using the performance measures defined for the Merchandise Plan and for additional measures including:  Percentage of COGS, and Secondary Cost Margin.
Ability to summarize Vendor Plans at the merchandise category level across the merchandise category, class, department, division.
Ability to review plans at the all levels, to make adjustments, and to perform roll up and roll down reconciliation as required.
Ability to define the vendor plan roll up/roll down reconciliation process based on user-defined algorithms.
Ability to allocate universal dollar/percent volume spreads.
Ability to lock plans based on Executive approval.
Reports
Merchandise Plan
See components and performance measures above.
Allocate Weekly Plans
Objectives
During this step, the finalized monthly Merchandise Plans developed in Align Annual Merchandise/Store Plans are allocated into weeks.

Requirements
Ability to define company-wide weekly percentages at the various levels in the hierarchy (company, division, department, class, merchandise category) and apply the percentages to the monthly sales.
Ability to review plans at levels, to make adjustments, and to perform roll up and roll down reconciliation as required.
Ability to manually adjust the resulting weekly sales.
Ability to create exception reporting when individual plan performance measures fall above or below user-defined plan tolerances.
Ability to define the weekly plan roll up/roll down reconciliation process based on user-defined algorithms.
Ability to allocate universal dollar/percent volume spreads.
Ability to lock plans based on Executive approval.

Reports
See components and performance measures above.
Track Progress and Revise Plans
Objectives
During this process, actual performance is tracked and measured against the plan and forecasts are developed.  If necessary, the plans are revised to reflect changes in the direction of the business.

Requirements
Ability to summarize the individual article/site forecasts into a total company within the merchandise categories and across categories into the divisions, departments, and classes.
Ability to summarize the individual article/site forecasts for each location within and across merchandise categories.
Ability to summarize the daily/weekly forecasts and history into months.
Ability to track actual performance against the components of the plan and the forecast.
Ability to calculate performance measures using actual results and forecasts, and compare against plan performance measures.
Ability to develop exception reporting that highlights problem areas based on user-defined parameters.
Ability to provide reporting that allows analysis by the merchandising hierarchy (article, merchandise category, class, department, division, and company) and the "people reporting" hierarchy.
Ability to allow default "views" based on user definition.
Ability to define and produce standard reports for use during the formal weekly review process.
Reports
Merchandise Plan
See components and performance measures above.

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
