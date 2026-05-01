---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/mem000.doc.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# mem000.doc

## Source
File: `Brain/raw/.extract/BP/mem000.doc.md`
Size: 17,740 bytes

## Raw content
 TOC \o "1-2" I. Event Management (Level 2)	 GOTOBUTTON _TOC410015737   PAGEREF _TOC410015737 2
A. Objective and Definition	 GOTOBUTTON _TOC410015738   PAGEREF _TOC410015738 2
B. Critical Success Factors	 GOTOBUTTON _TOC410015739   PAGEREF _TOC410015739 2
C. Assumptions	 GOTOBUTTON _TOC410015740   PAGEREF _TOC410015740 2
D. Requirements	 GOTOBUTTON _TOC410015741   PAGEREF _TOC410015741 3
E. Performance Measures	 GOTOBUTTON _TOC410015742   PAGEREF _TOC410015742 5
F. Issues	 GOTOBUTTON _TOC410015743   PAGEREF _TOC410015743 5
II. Create Ad/Event Budget/Calendar (Out of Scope)	 GOTOBUTTON _TOC410015744   PAGEREF _TOC410015744 6
III. Develop Event/Promo Plan (Out of Scope)	 GOTOBUTTON _TOC410015745   PAGEREF _TOC410015745 6
IV. Plan Single Ad/Event (Level 3)	 GOTOBUTTON _TOC410015746   PAGEREF _TOC410015746 6
A. Requirements	 GOTOBUTTON _TOC410015747   PAGEREF _TOC410015747 7
B. Jobs Analysis	 GOTOBUTTON _TOC410015748   PAGEREF _TOC410015748 8
C. Reports	 GOTOBUTTON _TOC410015749   PAGEREF _TOC410015749 8
V. Execute Ad/Event (Level 3)	 GOTOBUTTON _TOC410015750   PAGEREF _TOC410015750 8
A. Requirements	 GOTOBUTTON _TOC410015751   PAGEREF _TOC410015751 9
VI. Evaluate Ad/Event (Level 3)	 GOTOBUTTON _TOC410015752   PAGEREF _TOC410015752 9
A. Requirements	 GOTOBUTTON _TOC410015753   PAGEREF _TOC410015753 9
B. Jobs Analysis	 GOTOBUTTON _TOC410015754   PAGEREF _TOC410015754 10
C. Reports	 GOTOBUTTON _TOC410015755   PAGEREF _TOC410015755 10
D. Forms	 GOTOBUTTON _TOC410015756   PAGEREF _TOC410015756 10


Event Management (Level 2)
Objective and Definition
The efficient and effective coordination, communication, execution and analysis of events which supports the marketing plan.

Event Management:  the process of creating event calendars, planning events, selecting media, selecting items, producing ads, and reporting on event performance.  The process triggers events such as promotional purchase order creation and item distribution as critical calendar dates are reached.  The process supports the tracking and collection of promotional dollars.
Critical Success Factors
Ability to integrate advertising and store-level promotion with merchandising and financial objectives.

Ability to enhance the customers’ perception of the company brand.

Ability to effectively track and react to event productivity.

Ability to target advertising to individual markets.

Ability to effectively price merchandise to maximize sales.

Assumptions
Ad pagination and calendar creation (both promotional and activity) will occur in advance in the Develop Event/Promo Plan process.

Sales plan information will feed into the Event Management process from  the Corporate Budget process.

Ad layout functionality will be provided by external bolt-on software and support the Advertising Management process.

SAP will store all master data used in Ad/Event Management and will provide interfaces to the external ad layout system as required.  The ad layout system will support/interface with the company’s email system and will be capable of sending proposed Ad Layouts to corporate management for on-line review, comments, and approval.

Store management is responsible for applying and implementing the sell through guidelines for any end caps within their discretionary control.

Coupon transactions will be stored in the Data Warehouse.  The Data Warehouse will support vendor evaluation activities not managed by Accounts Receivable.

In-Store Systems (POS) will support coupons (including BOGO) by  providing:
Automatic scanning
Automatic processing
Interface with coupon clearinghouse

The Plan Single Ad/Event process will provide sufficient lead time for sites to complete promotional SKU, quantity, and price checks.

Before the Plan Single Ad/Event process occurs, the general activity calendar for that single ad/event will be established by Advertising and Presentation.

Stores have insight into on-order.

The product support package which is distributed to the stores within the Execute Ad/Event process contains:  coupons, signage, presentation standards, and event instructions.

Policies and procedures regarding WMS communication will be developed such that:
The high level ad/event calendar, as well as the single ad/event activity calendar will be distributed to the DC.
All events will be communicated at least one week prior to their execution in order to allow ample time for setup receiving, put-away, replenishment, picking, auditing, and shipping processes to occur.

Promotional prices will be managed through the central Price Management process.  The process Plan Single Ad/Event will define parameters of promotional price changes and interface to Price Management.

Promotional profitability analysis includes incremental margin, derived from initial markup on incremental promotional sales less markdown, less internal and external media costs.

Requirements
Note on font usage in this section:  Italic font is used to indicate requirements where there is a potential gap with SAP;  and Bold font is used for known gaps.

Provide a single, secure, central location for all ad/event activities.

Provide the capability to identify an ad/event based on name and event type. Systematically support the management, tracking, and reporting of ad/events based on the following types/fields:
/event name
Media type (ROP, circular, direct mail, etc.)
Placement type (location on page/quadrant)
Display type (end cap, etc.)

Support the ability to interface with a third party or store printer and send an ad/event notification (Idoc) based on an ad/event attribute outside of an article's variants.

Systematically model the effects of an ad/event through a separate modeling capability. Leverage articles that exist in the system that have past event history and based on past event measures produce a listing of potential ad/event merchandise.

Support the ability to build/copy a new ad/event template from a completed ad/ event.

Provide the capability to easily modify the start and stop dates for an active event.  An active event is defined as an approved promotion that has already triggered pricing related functions and vendor notification related functions, but has not actually started running in the stores.  There may be situations where we want to change the ad/event dates of a promotion before it has actually begun.

Provide the ability to support the following activities:
Plan Events
Manage Events
Price Promotional Merchandise
Evaluate Event Performance to Event Plan
Report on exceptions for high/low sales and inventory
Evaluate Event Performance to pre-event and post-event periods

Provide an interface or link capability to:
Pricing
Purchase Orders
Forecasting
Warehouse Management (EXE)
Assortment Planning
Advertising Management

Allow for Store Operations to plan and manage those end caps and promotional displays within their discretionary control.


Support the ability to manage, track and report using coupon-based promotions.  The system must track coupons by UPC and interface with vendors once coupon redemption has occurred.
The system must manage, track and report coupon promotional activity by the following coupon types:
Vendor (paid for by vendor for any retailer)
Vendor Paid (paid for entirely by vendor for PETsMART only)
In Whole (free with this coupon)
Proportional (buy 1 get the 2nd one 50% off)
In Kind (buy one get one free)
PETsMART Account (paid for by PETsMART)
Ad Certificates (paid for by PETsMART and found in circulars or ROPs)
Item Specific (paid for by PETsMART and used for specific merchandise category)
Based on the above coupon types the system must support the systematic determination of Accounts Receivable coupon treatment and processing based on coupon type.  Vendor coupons must be treated as receivable, while PETsMART coupons must be treated as discounts.

Support the systematic determination of Accounts Receivable coupon treatment and processing based on the coupon’s UPC.  Vendor coupons must be treated as receivable, while PETsMART coupons must be treated as discounts.

Provide the capability to segregate promotional demand from store replenishment demand.   Stores must have the ability to manage discretionary endcaps that may be used to liquidate overstocks.  These endcaps must be treated as “events” in the system and managed as such.

The system must allow users to vary promotional retail prices by article by site. Articles impacted may be defined at any level in the merchandise hierarchy and/or based on user-defined article attribute values (e.g., all dry cat goods less than 10 pounds).  Sites may be defined at any level in the organizational hierarchy and/or based on user defined store attribute values (e.g., all K-Mart competition stores).  The system should permit the use of mass maintenance to define a promotional price structure and application. The user should also be permitted to selectively change prices based on user-defined criteria (e.g., 1 promotion with group A pricing and group B pricing).

Provide the ability to account for promotional quantities in demand forecasting.

Support the segmentation of promotional on-order from regular on-order in replenishment forecast (part of demand problem).

Support the ability to separate promotional sales quantities from regular demand when calculating the forecast.

Support the management of a company-wide promotional event when many users need simultaneous access to promotional material in order to make changes and contributions.

Performance Measures
Adherence to a single ad/event calendar.

Number of price change requests.

Number of inventory issues communicated from stores to SSG.

Timeliness of the store notification regarding upcoming ad/event.

Timeliness of SSG delivery to stores of ad/event support package.

Total cost of ad/event vs. total incremental revenue.

Incremental gross margin vs. planned gross margin.

Amount of residual inventory.


Issues

Does the promotional vs. presentation quantities issue need to be re-examined?  Event Management team was unclear as to why presentation quantity was driving inventory position.  RESOLVED -  VP Meeting confirmed Presentation Quantity Driver.

How does the SAP support multiple promotions on the same item occurring at the same time? Assigned to SAP.

What subsequent processing needs to be completed prior to activation of the event from a business point of view.  Assigned to Patricia G.

What process will deal with the re-allocation of event merchandise (leftovers) once the ad/event is over?  Assigned to Patricia G.


Create Ad/Event Budget/Calendar (Out of Scope)

Develop Event/Promo Plan (Out of Scope)

Plan Single Ad/Event (Level 3)
Requirements
Support ad/event planning at the individual article/site level and at a summarized article/site level for all ad/event articles in a single ad/event, all ad/event articles by any merchandise hierarchy, and all ad/event articles in a given time period.

Provide the ability to account for promotional quantities in demand forecasting.

Support the allocation of generic article variants in an ad/event allocation.

Provide the capability to update an ad/event at the line item or header level.

Support the ability to flag an order at the header and line item level as an ad/event.  This facilitates tracking and reporting during all steps of an ad/event process.

Provide the capability to manage store ad/event article ordering.  System must be able to track as a percentage or unit comparison of presentation quantity min/max quantity tolerances.  Tolerances must be defined based on replenishment parameters.  System must automatically send the ad/event article tolerances for an display (i.e., endcap) to the stores for order quantity input.  The stores then return to corporate the quantity they believe can be supported on their display.

Support system calculations which analyze and define promotional over capacity of potential ad/event articles and promotional residual inventory from potential ad/event articles.
Based on the item forecast, support the ability to calculate expected "over capacity" of in-line items and the "left-over" quantity (weeks of supply) expected after an event has run.  Both calculations will be utilized to analyze which items would be most profitable for use in the ad/event.
The calculations are defined as follows:
Expected Over Capacity In-line =
      Lowest Inventory Level Allowed for End Cap / In-line Holding Power
Left-over Quantity =
      Lowest Inventory Level Allowed for End Cap / Weeks of Supply

Support the creation and management of a single ad/event activity calendar which manages the timeline of activities included in ad/event set-up.  The calendar must track activities by date from planning through execution of the ad/event.  Activities that must be tracked by date are as follows:
Theme/pagination creation
Preliminary item planning
Executive management approval of preliminary items
Preliminary item turn-in
Executive management approval of item turn-in
Final item turn-in
Pricing by market
Ad proof completion
Final pricing updates
Ad printing and creation
Vendor notification of ad items
Site notification of ad items
Item receipt in the DC
Item receipt in the stores
Ad break


Provide the capability to identify an ad/event based on name and event type. Systematically support the management, tracking, and reporting of ad/events based on the following types/fields:
Ad/event name
Media type (ROP, circular, direct mail, etc.)
Placement type (location on page/quadrant)
Display type (end cap, etc.)

Jobs Analysis
See process map for job delegation.

Reports
Reports Added
Combined Turn-in/Sales and Inventory Report - details the sales plan, inventory plan, presentation quantity by article/site, coupon types utilized, Accounts Receivable reimbursements, signage requirements.

Execute Ad/Event (Level 3)
Requirements
Support the creation of ad/event price tags and signage through an interface with the store’s ticketing equipment, and/or interface with a third party.

Support an interface with WMS systems regarding ad/event items, quantities, and due dates.

Support a two-way interface with an Advertising Management bolt-on (third party printer).  Advertising must be able to receive the following fields from SAP:  SKU, UPC, merchandise category, department, grouped variants (i.e., Wiskas - chicken, tuna, etc. flavors), vendor information, item description, and pricing information.  SAP must be able to receive updated prices from the Advertising Management third party which automatically update current promotional prices once pricing approval has been granted.

Evaluate Ad/Event (Level 3)
Requirements
Support the ability to plan performance for an event and then measure event performance against that plan at the article/site and aggregated levels.  The promotion analysis period can be defined and reported in several phases, including pre-promotion, promotion and post promotion.

Ability to track and evaluate pre, during and post ad/event sales for different monthly ads/events running in the same time period, all against plan.

Support the capability to view markdown planning summary values, promotional planning values, and their sum totals by document (e.g., promotion) and time period.

Support the ability to track and report an ad/event or group of ads/events at any level of a merchandise hierarchy or user-defined department.

Provide the capability to input an article number and see the promotional sales history of that article including the following information:
Item Description
Market(s)
Event Dates
Sales
Gross Margin
Opening inventory
Closing inventory



Support the tracking and reporting of a single ad/event and/or a group of ads/events at any level of a merchandise hierarchy or user-defined department.  Provide the ability to record and report on the following aspects of a single ad/event or summarized group of ads/events:
Ad/event name (promotion code)
Media type (ROP, circular, promotion, display)
Placement type (location of ad page / quadrant)
Display type (end cap, off shelf, etc.)
Time period
Organizational hierarchy (store, market, nationwide)
Merchandise category, department, class, or single article
Sell through in units
Sell through in retail dollars
Sell through in cost dollars
Incremental sales
Total gross margin and sales vs. the total cost of an event
Total promotional sales vs. total planned sales
Customer count (number of transactions)
Average transaction amount (sales/number of transactions)
Non-promoted “ad track” item lift (based on those items which have been found to be  linked from prior analysis)
Market basket (analysis of other articles that were purchased in conjunction with the    ad/event item.)
Total cost of event media utilized (newspapers, radio spots, etc.)
Total additional revenues driven by event (co-op, rebates, gross margin)
Redemption rate for internally generated coupons (number of coupons redeemed/total    number of coupons)
Residual inventory vs. planned inventory for that period
Trended vs. seasonalized sales
Weather conditions associated with an ad/event
Out-of-stock position before, during, and after an event

Jobs Analysis
See process map for job delegation.
Reports
Added:
Ad/Event Evaluation Report - Summarizes ad/event return vs. plan.  Information and sort is based on any or all of the information listed above.

Ad/Event Merchandise Category Evaluation Report - Summarizes ad/event return by merchandise category vs. plan.  Information and sort is based on any or all of the information listed above.

Forms
Added:
Store Feedback/Comment form - details issues stores have regarding ad/event.

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
