---
date: 2026-04-26
type: raw
source: /Users/gclyle/Desktop/RETAIL/SAP Retail/Fashion Workshop1.DOC
tags: [retail, sap, apparel, merchandise-planning, allocation, otb, layout-planning]
project: canary
status: processed
method-role: PhD
method-stage: research
---

**Wiki:** [[Brain/Home|Home]]

# SAP Apparel Workshop — Merchandise Planning, OTB, Allocation (1998)

## Source
SAP AG / PricewaterhouseCoopers joint apparel workshop, August 1998. Participants from SAP AG (Walldorf), SAP US, SAP CH, and PwC US. Document authored by Agnes Hall (SAP US) with multi-retailer commentary from Reebok, Pet Smart, Fabri-Centers/Jo-Ann Stores. Workshop protocol — not a development commitment.

## Raw content

Apparel Workshop Preliminary Results and Priority List


Introduction

The workshop discussion was based on the SAP America/Specialty Official Development Document written by Agnes Hall. The purpose of this document was to outline the best practices of the apparel industry, and compare this to the business process applications of the R/3 system. This document was then distributed to the US Retail customers for feedback. Additionally the workshop looked into the results of the “SAP German textile prototyping” initiated by the retail sales and consulting group Walldorf in order to set up a practical prototype for business development in the retail textile sector. This involves establishing which processes can be adopted from the standard SAP Retail system without modification, identifying functional gaps and formulating possible solutions. The aim of the prototype group is to design a prototype that clearly reflects and communicates a specific business orientation to the fashion sector. 



The following main points were discussed: 
Merchandise Planning
Layout Planning
Open to buy
Allocation
Promotion Planning
Pricing
Purchase Order Management
Replenishment
Article Master Data
Pre-packs

We had no discussion about infostructures. To get more information about the  demosystem and to identify the requirements for infostructure please have a look at  the following and at the customizing of the “SAP German textile prototyping”. see exhibit 1-5.



Participants:	B. Bittermann, SAP AG 
Manfred Deindl, SAP CH 
Stefan Dendl, SAP AG
Thomas Eckert, SAP AG 
Frank Freitag, SAP AG 
Agnes Hall, SAP US
Diane Hamilton, PWC US
Andreas Jessen, SAP AG
Markus Müther, SAP AG 	     
Thomas Pickel, SAP AG
Paola Sala, SAP AG 
Cornelia Schinke, SAP-R						
Olaf Schulte, SAP AG 
Carolin Unterstab, SAP-R
Andreas Wormbs, SAP AG 
						 
 
This paper can be considered as a protocol of the workshop, not as a concrete basis of development actions.

In the further document  every section will be spreaded into two parts:
the first contains the document written by Agnes Hall (I),
the second contains the results of our discussions in our workshop (II).

MERCHANDISE PLANNING

SAP America Apparel/Specialty Official Development Document

The purpose of this document is to draft requirements for the apparel/specialty markets specifically in merchandise planning functions.  Authors include Agnes Hall, Joe Paytas, Ozzie Patzmann, and Ted Nowokunski.
Please note that all of the topics below have to be fully integrated.  For example, Planning must be integrated with allocation, replenishment etc. 
 This document will go into detail describing the following business topics, and follow with an explanation of how the current R3 system deals with this process.  In addition, customer comments will proceed in underlined format.


I. Merchandise Planning
Merchandise Planning includes Assortment Planning, Seasonal Planning, and Unit Planning.  Due to the highly seasonal merchandise that softlines retailers sell, the planning functionality is necessary to run their business.  Planning is used in all aspects of the business in order to insure the right product in the right place at the right time.  With the exception of basic merchandise such as socks, under garments, etc.; and pool stock at the distribution center, a softlines retailer does not utilize automatic replenishment.  At any point in time based on changes in the business climate a retailer needs the ability to revise and do “what if” scenarios.  This process is known as the OTB (open to buy) or ROF (rolling operating forecast).  This process needs to be accomplished in a very easy to use method that updates actual information to compare to plan, last year and create a forecast.  All of this information needs to be seen on one screen at different merchandise levels and rolled up to a corporate total.  All planning needs to be done in a central place and fed to other applications, not planned separately and summarized later.   Merchandise Planning is a major part of the day in the life of a buyer.  The following will be a detailed list of functionality and system requirements for seasonal and assortment planning.


Seasonal Merchandise Planning/Assortment Planning

1.  Seasonal Merchandise Planning is the process creating a business workbench by gathering historical and trend Data to interface with all other business practices.  This plan includes but is not limited to:
Sales 
Markdown Dollars (original retail-revised retail)
Markdown Percent (markdown dollars/original retail x 100)
Gross Margin Dollars (sales-gross cost of goods)
Gross Margin Percent (gross margin dollars/sales dollars)
Receipts
Average Stock (total period of stock levels/number of periods)
Markup Dollars (retail dollars-cost dollars)
Markup Percent (markup dollars/retail dollars x 100)
Turnover sales/average stock
Pet Smart Comments:
Comp Store Sales
New Store Sales
Sales per Store Week
Shrinkage
Rebates
Inventory at Cost
Marketing Allowances
GMROI
Performance Measures
Average Retail
Percentage Change to Last Year
Penetration Percentage for Sales, Gross Margin, and Gross Profit
Percent to Sales
Initial Markup
Weeks of Supply
GMROI

This plan is most commonly done at the department level (merchandise hierarchy), but can be done at the classification level (merchandise category).

In the current R/3 system, Flexible Planning is the primary tool that is used to satisfy Merchandise Planning requirements.  This includes Seasonal Planning, Unit Planning, OTB and Allocations.   While Flexible Planning does allow for some components of the Retailers' planning requirements to be satisfied, on the whole, the American Retailers who were shown the functionality deemed it to be unacceptable.   They felt it was difficult to set up and maintain, it lacked "what if" modeling capabilities, there are very little (if any) Retail-specific planning features, it was extremely difficult to use and did not provide a retailer the views of the data that they required.  Creating and maintaining planning master data (even with the generator tool) will never work due to the amount of categories, stores and styles that the retailer must incorporate into merchandise plan.   There is also a great deal of concern over the performance of the Flexible Planning (FP) tool.  Even with the changes made to 4.0, the amount of data that a retailer must deal with makes the use FP tool prohibited.   The planning table itself was seen as a major drawback to the tool.   Retailers require the ability to view the planing data across a number of dimensions and times.  As you know, the planning table is extremely inflexible as to the manner in which it presents data to the end user.  (Even the new time variant in 4.0 is not going to solve the problem.)  Lastly, retailers require the ability to create mass changes to the plans that they create.  As an example, they would like to increase the planned stock in all large sizes for the stores in the northeast.  This is impossible to execute with the current FP product.

However, the single biggest criticism concerning the planning product is that it is not tightly integrated into the other Retail modules.  While you can use a planning table to do analysis in the RIS and also to generate an allocation rule, American Retailers are used to Planning modules that actually create transactions in the other key merchandising areas.   The transactions become linked to the plan, so as each is modified the two are kept in synchronization.   As an example, if an allocation plan has been created that will create a Pre-distributed Purchase Order, the system needs to update the plan based on a change to the allocations that have occurred in the distribution center.  This is critical if you are using the planning engine to create an open-to-ship or to create weeks supply allocations to your stores.  Areas that the retailers would like to have a tighter integration within the SAP Retail product include Planning, Allocations, Replenishment, Article Master data, Pricing, Promotions, Assortment Planning and the RIS.




Reebok Comments:
If seasonal merchandising plans will be created and maintained in SAP, the
customer should not be "forced" to include the seasonal characteristic in the planning hierarchy.  This forces you to plan by season.  If you have assigned multiple season codes over the last few seasons and  years, one is forced to plan at that level or not
assign multiple season codes to materials.  This prevents you from
utilizing RIS to perform season code analysis. If one has assigned multiple
season codes and only maintains the plan for one season code, then actual
data is not properly updated.  Retailers need to plan using the material hierarchy.  At the lowest level(material group) a large retailer could easily have 500+ material groups.
Multiply this by number of plants (100+) and you have planning tables with
50,000+ material group/plant combinations.  Even if one is not interested
in maintaining plant level plans, the plan has to be created with plants as
a characteristic in order to capture actuals.  Also, if one is interested
in linking allocation rule generation or allocation strategies that utilize
plan values, the plans must be created at that level.  Very careful thought
has to be paid to the planning environment in SAP, in terms of database
size that would need to be maintained, performance of the planning module
and, most importantly its effect on transactional updates.  As part of the
design process, a careful review of this sizing/performance issue needs to
take place.  Perhaps SAP's merchandise planning module could be run on a
separate "planning server" with asynchronous or automated copy management
updates from the "main" database/transaction servers.

Fabri-Centers/ Jo-Ann Stores Comments:
Average Store
Require the ability to calculate average store.  This typically is a calculation that is used by retailers.  To support this should have store count by week and month

Calendar Shift
Need ability to accommodate calendar shift for :
Holiday date change, e.g., Christmas, Easter
52 week Vs 53 weeks

Planning overlapping seasons
Need the ability to plan for overlapping seasons.

Plan inventory based on various criteria
Inventory turns
Sales plan





The plan is normally done in dollars in a bottom up manner.  

This can be accomplished using Flexible Planning (FP), but typically, retailers are used to having different levels of the plan linked together across different plans.  The reasons for this planning methodology is to improve performance, allow security to control who works on which part of the plan and improve data maintenance. As an example, you may have a top down financial plan that includes regions and departments.  This is then linked to another plan that has class and sub-class.  Lastly, this is linked to a third plan that will actually go down to the assortment and the store.  All three levels are kept in synchronization in both a top down and bottom manner.  In FP, the system forces you to create one huge plan to include all of these levels.  There are a number of problems with this including performance, data maintenance and most importantly, security.

The plan should have capability to be done at the store (site) level and rolled up to a total.

See above.  Again, the system should be able to keep multiple mini-plans in synchronization.

The system should “recommend” sales and average stock plans by department by location based on pre set parameters such as inventory turnover goals.

Currently, there is no ability to conduct "what if" analysis in the FP modules.  The product requires the end user to create macros or to use user exits to write their own optimization routines.  This is not acceptable to the retailers in America.  A major reason that they are purchasing a Merchandise Planing module is so that they can take advantage of the retail specific "best of class" processes that the software vendor has included in the package.  Average inventory goals in a Merchandise Planning module should be a standard "wizard" that can be applied by the end user.

The system recommendations should take in to account sales missed opportunity by too little stock. It should as take into account sales downtrend due to excessive stock, or the wrong assortment.

SAP currently has no method for tracking, recording or analyzing lost sales opportunities.  These must be incorporated into the merchandise planning process so plans can be evaluated in an accurate manner.

At this point the plan needs to be spread by month taking into account the seasonal advertising calendar, historical information, current business trends and new store openings.


This is a major concern of the retailers.  The current planning tool has no concept of an upcoming promotion except the SO86 infostructure.  The use of events in the planning table is not an acceptable alternative.  Ideally, by defining a promotion in the promotion module, the merchandise plans should be able to access and integrate this data.  Also, the current FP product has no concept of new store openings.  They need to have the ability to model a new store after a like-store when creating and modifying current merchandise plans for assortments, allocations or seasonal plans.

Once corporate totals are spread by month, it is then transferred to location level.  The location plans must be spread by month.  The corporate plan is not spread evenly across all stores.

There are currently data distributing functions at the key figure level in FP.   There needs to be more features added to the methods in which the ratios between planning levels are created and maintained.  Currently, there are very little options to effectively handle this data maintenance.  Ratios between planning levels should be able to be created from a variety of key performance indicators, forecasts, weighting profiles and smoothing factors.


Pet Smart Comments:
The ability to allocate down to the weekly level once plans have been approved.  
Also, The ability to define the planning components by level.  For instance, sales may be planned at a daily level, but not inventory.  If this functionality is used, not all roll up/middle out/roll down functionality will be activated.

Location plans by month are rolled up to a corporate total.

See number 2 above.

Assortment planning needs to be done as low as the merchandise category level.

See number 2 above.

All planning should be done in the same place in the system and be integrated with all other functions such as allocation, purchase order management, replenishment, and open to buy. 

See Number 1 above.  Currently there is minimal integration between replenishment and planning.  There is no integration between Purchasing and Planning.



Reebok Comments:
In the planning screens in SAP, a planner needs to see the effect on
calculated key figures,  as planning values are being entered/maintained,
without having to go to RIS to review turnover for example.  RIS needs to
be more integrated with the planning screens.
Other wizards can be forward weeks of supply, markdown % instead of
planning markdown dollars, being able to plan mark-up% and mark-down %,
and see the effect on gross margin %.  Location level planning needs to be extremely flexible & "intelligent, in order to allow effective planning of a limited # of key figures across hundreds of plants & material groups.  The system should offer a first
pass, based on total plans and last year ratios.  Planners then need to be
able to quickly modify specific plants for total year plans, and/or modify
at a monthly level.  If sales plans are adjusted for a specific plant, the
system needs to re-calculate needed stock coverage, based on target figure
for the material group or the specific plants.  Planning screens need to
quickly shift from one view to another, depending on the changes a planner
needs to make.


Top-down and bottom-up planning must be supported.

See number 2 above.

Plans need to feed any transactions in the system automatically.

See Number 1 above.

Changes to plans need to update the independent transactions that they created if still open.

This is extremely important.  This is currently not available in the FP module.  (With the exception of being able to re-generate an allocation rule.  However this is an extremely manual and laborious process. )  If a transaction has been created from a Plan (an allocation and or replenishment), it must be updated automatically based upon a change to the plan.  As an example, if an allocation table has been created from a planning table, and the table is changed due to a change in selling patterns or distribution requirements, the allocation table needs to be updated in real time.

Assortment planning is multi-dimensional, over department class/plan/time, with each dimensions set by the user based on receipt flow of merchandise.

The planning module should have the ability to effectively create assortment ranges and owners.  Based upon a season merchandise plan for a category or styles, the planning module should feed the Assortment module and create the appropriate listing range grades for the merchandise to be sent down to the store POS.  The current system is not integrated in any way.  Also, there are no multi-dimensional views of the data in the planning table.  The user is forced to view the current planning level with time as the columns and the key figures as the rows.  The Retailers require much more flexibility in this area.  Most of the retailers we spoke with indicated that the planning table should work very much like an Excel pivot table.

The user defines planning rules.  Selected key figures such as markup % can be set as fixed or variable figures.

Fixing is allowed in the planning table currently.  However, if the user desired to use master data concerning a planning element in the plan, this should be allowed.  Currently, if the user wants to create a plan with the item's final retail, this is impossible because there is no integration between the planning item and the rest of the master data.  (Especially condition records.  This is why it is almost impossible to accurately convert between unit and dollar plans.)  The planning system should have the capability to read the current prices and markup percentages of the items and bring them into the plan.  Maintaining the Average Price Bands in the IMG is very time consuming and is not as accurate as many retailers require. 

Based on the selected key figures the user performs what-if calculations by locking selected key figures and re-calculating dependant variables until desired results are achieved.

There are no what-if models available.  Users are forced to write complex macros or ABAP.  See number 4 above.  The best planning products on the market come with pre-defined retail "wizards" which allow the end user a very user-friendly method for creating replenishment, allocations, assortment plans  and merchandise plans.

17.  Plan variables should be adjustable by percentage change, or an absolute value.

Changes can be made in the current planning table in this manner but at only one level if the planning hierarchy at a time.  What retailers are really looking for is the ability to create changes of this sort ACROSS planing hierarchy levels.  Again, such as in changing the desired stock by a percentage using characteristics and store groups.

Automated new store model generation, based on a selected comparable stores or Store groups.

There is absolutely nothing in the current package will allow for a "new store planning" generation to take place.  There is no ability to create comp or like-stores in any feature of the planning modules.  This is very important for large retailers in the United States, some of which are opening a store a day.  In addition, the classification object that is used by SAP retail for store group (which is how we define comp vs. non-comp stores) can not be put into a FP planning hierarchy without considerable work.  This is important because at any time, the retailer requires the ability to create, copy and maintain plans for groups of stores.  In addition, they need the ability to conduct analysis that will compare different store groups against each other during and after the planning process. If you cannot put the 030-classification object (store group) into a planning hierarchy, it makes this method of planning impossible.

Plan sales for comp vs. non-comp stores.

See above.

Plan by store groups either by region, or store size.

See number 18 above.


Ability to “lock” certain stores or values in a plan to exclude from any changes or auto balancing to a top side plan.

Fixing is currently supported in the FP module.  Improvements have been made with 4.0.

Multi-versions of a plan supported.  For example, test vs. final approved plan.

Multiple versions of the plan are supported however, there needs to be better security, copying and analysis features incorporated in to the module to make it acceptable for the retailers.  Currently, there is no security in the system for locking a user out of editing or viewing different levels of a plan.  This is required.  Lastly, they analysis features need to be improved so that multiple version of the plan can be compared at the same time.

Ability to copy parts of or an entire plan.

Copy rules are supported.

Ability to copy test plans in to a final plan.

Copy rules are supported.   However, the retailers also need the ability to merge multiple versions together to form a master plan.

Optional re-statement of history/plan, when a change to the hierarchy is made.

Very important!  Because retailers create re-organizations of merchandise hierarchies from time to time, the reorganization process must be integrated with the merchandise planning functions.  If a retailer moves a certain style to a new category, today the FP system would have no knowledge of this event.  Thus all merchandise plans, allocations and Open-To-Ship replenishments would be inaccurate.

Options to view plan, last year, and actual all on the same screen.

This is available currently.  However, what is not available is the ability to rotate the dimensions in the planning table.  Users very much require Excel-like pivot table capabilities when viewing and working with merchandise planning tables.

The ability to require plan review and approval by designated levels of management.

There is currently no approval process linked to the FP modules.  All retail merchandise plans must go through a multiple tiered approval process for the upcoming season.  This is most notable in the case of the Open to Buy process.  The SAP workflow module needs to be integrated into the approval process for the new merchandise plans.

Unit Planning

In order to complete unit plans, the seasonal merchandise plan will need to be converted to units.

Currently, the OTB system converts the dollars to units based on a hard coded macro that uses the Average Price Bands defined in the IMG.  The system does not look at the actual master data of an item or item conditions records.  This needs to be remedied.  The planning system should have the capability to read the current prices and markup percentages of the items and bring them into the plan.  Maintaining the Average Price Bands in the IMG are very time consuming and not as accurate as many retailers require. Typically, the retailer will plan in dollars and then need the plan broken down into units based on the average retail of the category or the actual condition records of the items in the category.  

Create unit plans by store group, by category, by month.

The classification object that is used by SAP retail for store group (which is how we define comp vs. non-comp stores) can not be put into a FP planning hierarchy without considerable work.  This is important because at any time, the retailer requires the ability to create, copy and maintain plans for groups of stores.  In addition, they need the ability to do analysis that will compare different store groups against each other during and after the planning process.

System recommends the following based on pre set parameters by store: minimum unit allocation quantity, and advertising minimum unit allocation quantity.

The system must be able to have a section of the article master devoted to the allocation of an item in a store.  The allocation rules and allocation models currently can not read the logistics data of the article master.  In addition, it is difficult to work with multiple infostructures for regular stock requirements and promotional stock requirements.  These should be merged into one planning infostructure.

System recommends an allocation based on actual selling parameters to determine a ratio of stock a store should receive relative to sales.

This is a method of allocation that the user should have at their disposal via an "allocation wizard".  By choosing this option, the system should consider all relative data and propose an in-stock quantity for the item in a store across a certain number of weeks.  The allocation should then generate the proper transaction (either Purchase Orders or Stock Transports for the item depending on the source of supply.) automatically.  The actual selling patterns need to be constantly monitored by the system and the future allocations adjusted accordingly.  After the adjustments, the transactions that they have created need to be adjusted to reflect the change to the allocations.  In the case of a pre-distributed cross-docked or DSD Purchase Order, the change of allocations need to be communicated to the vendor so they can pack and label the merchandise properly.

Flexible unit planning levels from department down to department/vendor/style combination.

Supported as master data in the planning hierarchy. However, the retailer desires the ability to break the plan up into mini-plans that are linked together.  This is done for performance, security and data maintenance.

Capability to utilize a unit plan in another planning level.  For example: allocate a dept/vendor/style based on the unit plan established by department/class.

Copying across infostructures and versions is currently supported in FP.

Capability to create a unit department class plan based on percentages of the department plan.

Ratios between planning levels are currently supported by the FP module. Enhanced methods to calculate and maintain the ratios are required.

The ability to revise the plans as necessary.  Also the ability to have several versions, for example a test plan and a final plan.

Versions are supported.  Revisions are supported.  However, security and revision approvals are required.

The ability to view the unit plans for previous periods.

This is supported.  However, more flexibility is needed when viewing the planning tables.  The retailers require Excel-like pivot table functionality.

View actual sales, stock, & receipt history for previous periods.

This is supported in the FP module.

Access sales and stock history for at least 52 weeks, by day, week, or month.

This is not supported by the system.  Currently, the user is forced to view the key figures in the default time of the infostructure (Month, Week or Day) or use a time variant within the planning table.  Retailers require the ability to look at planned and actual data in multiple times in the same planning table!  They would like to see sales YTD, then by month, and finally by day.  To do this today in the same planning table is impossible.  The user is forced to use three different planning tables from three different infostructures.  This is a MAJOR problem with the current SAP retail planning system.

Execute comparisons between plan vs. actual, plan vs. plan and actual vs. actual for different periods.

This can not be done for a key figure in the planning table.  The user is forced to create a report from the planning table and then choose the edit->comparisons feature.  This is extremely difficult to work with as a merchandise planner.

Compare different planning levels.

See above.

View a chain plan as compared to a sum of stores.  (A chain plan will exclude the stock from the distribution center to prevent store stocks to be planned too high relative to sales for selling locations).

This can be accomplished if the user can define the groups of stores into multiple distribution chains and then put them into the planning hierarchy of the FB plan.   However, retailers want the ability to use store groups in the merchandise planning process.  Currently, SAP Retail can not put store groups into the planning hierarchy of a FB plan without a great deal of work.  Store groups need to be integrated with planning.

Combine multiple plan/unit levels together in order to view as a group.

This can be accomplished using Flexible Planning with one huge plan, but typically, retailers are used to having different levels of the plan linked together across different plans.  As an example, you may have a top down financial plan that includes their regions and departments.  This is then linked to another plan that has class and sub- class.  Lastly, this is linked to a third plan that will actually go down to the assortment and the store.  All three levels are kept in synchronization in both a top down and bottom manner. 

Once the plan is complete convert back to sales and stock dollars to compare.

To the best of my knowledge, converting units to dollars is not currently supported in the system.  The current OTB infostructure (S110) has a hard coded macro, which will convert dollars to units based on the Average Price Bands defined in the IMG.  But to convert from a random FB table that it is in units to dollars is not an option.  This needs to be remedied.




Pet Smart Addition:
Create Vendor Plans
A.	Objectives
During this process, vendor plans are developed within the merchandise categories.  These vendor plans are then summarized across the merchandise category into company-wide vendor plans.
B.	Requirements
Ability to automatically create vendor forecasts at the merchandise category level based on last year history.
Ability to manually adjust vendor forecasts using inputs from Assortment Planning, Vendor Management, and Merchandise Plan developed above.
Ability to plan for all the components of the Merchandise Plan and for several new components, including:  Purchases, Customer Returns, Returns to Vendor, and Full Cost (see gap #MIV040). 
Ability to track plan using the performance measures defined for the Merchandise Plan and for additional measures including:  Percentage of COGS, and Secondary Cost Margin.
Ability to summarize Vendor Plans at the merchandise category level across the merchandise category, class, department, division.  
Ability to review plans at the all levels, to make adjustments, and to perform roll up and roll down reconciliation as required.
Ability to define the vendor plan roll up/roll down reconciliation process based on user-defined algorithms.  
Ability to allocate universal dollar/percent volume spreads.
Ability to lock plans based on Executive approval.

II. Merchandise Planning





The standard merchandise planning process is as follows:


Step 1:   The creation of the seasonal merchandise plan at department/merchandise category level.  
The key figures involved in the planning process include sales, average stock, markdown, markup, gross margin, turnover, shrinkage, inflation rate, end of month stock and receipts. All of these key figures are summarized by season.  The basis of the plan creation is on last year information as well as the current trend information of the category/department.  This plan is done by period taking into account the flow of new merchandise and the seasonal advertising calendar.



Step 2:  The creation of the store plans at the department/merchandise category level are done simultaneously to compare both top down and bottoms up plans. 
This locational plan is only done at the total season level at this point for sales and average stock only.  At the completion of this plan it will be rolled up to the total merchandise hierarchy level.


Step 3:  The seasonal merchandise plan and the stores plan are compared to decide the total season plan to be used to spread the location plans by month.
The location plans are spread by month taking  into account the data at location level.  This will allow regional peaks in sales and markdowns to be taken into account.  At this point the additional key figures (see step 1) are planned.  


Step 4:  At this point within each category vendor/classification/and or /article category plans are completed. 
Article categories would be fashion (seasonal), basic (NOS), and promotional (specifically purchased for a promotion).  These plans may be completed at the location level, or only at the corporate level.  The same key figueres are planned.  These plans must be rolled up to the department/merchandise category level plan.

Step 5:  Now that we have completed the department, class, and vendor plans we are ready to create the assortment plans.  
This can be done at the article level if they are known, or at the category level with percentages of the article classifications.  The plan is now done by period to take into account the first order receipt, and the subsequent orders of the season.

Step 6:  At this point the unit plans are created.  The purpose of creating unit plans is to complete allocations.  
If the articles in the category are known, the average retail is used to divide into the plan in dollars/marks to create the plan in units.  If the articles are not known we can use historical average retail to create the unit plans.





Overall requirements for this merchandise planning process include:

The linkage between all plans in the merchandise hierarchy.  
For example, the vendor and class plans that are created in the same merchandise category/department must equal the total merchandise category/department plan.  If changes are made at the vendor or class level, the change to the overall department/merchandise category plan is also made.  All plans should be independent with only a linkage to the appropriate merchandise hierarchy.

The ability to do „what if“ analysis or simulations to demonstate the effect of changing one key figure and the result on the entire plan. 

 The ability to lock or fix selected key figures and re-calculate dependent variables until the desired results are achieved.  This was demonstrated in the Leather and Shoe planning project by Frank Freitag.  This project could be the basis for further merchandise planning for the core R/3 product with the other requirements mentioned in this document, and any further plans they have for this project.

The ability to plan in either absolute values, or percentages.

The ability to plan store groups, store regions, and comp vs. non-comp sales by store.

The ability to merge different versions of the lower level plan to the total merchandise hierarchy plan.

The optional re-statement of history when a change to the hierarchy is made.

The ability to view plan, last year, and actual all on the same screen.

The system should make clear, which steps in the planning process are necessary and which steps are optional.

The system should not force to create merchandise planning by season. There should be a time- period-code, that can be defined by the customer (e.g. month, season).  This code should be connected with the article.

The ability to require plan approval by designated levels of mangement.  Once plans are approved, the ability to lock them to prevent any changes to the plan.


Layout Planning (discussed in the workshop only)

This is the process of planning on the basis of the actual square footage/square meters and fixtures in the individual sites.  This will allow you to plan the stock in the sites with the actual capacity of the fixtures to determine if your planned assortment will fit.  This should be combined with the seasonality valid for each fixture.  For example, this information will also be given to the department manager to assist them in the monthly floor moves based on new product introduction.

Requirements include:

A graphical interface for the user to see an image of the actual sales floor and fixtures.  Collage could be a product to recommend for a partnership 


OPEN TO BUY

I. Open to Buy
Open to buy is simply a means to monitor the seasonal financial plan and make forecasts to compare to the plan.  The most important process needed in an OTB system is the constant and consistent update of actual information and the automatic feed of all plan data.
 Open to buy is also known as a ROF (Rolling Operating Forecast).   A ROF is a flexible plan that allows proactive revisions to the plan.
A flexible planning system allows you to plan the receipts by merchandise category over a set period of time (for example, a season) and to allocate funds by month.
The receipt plan is made up of two elements: purchase orders already received for the period and receipts reserved for additional purchases. The latter can act as a buffer against; for example, unexpected cost increases or can be used to cover unforeseen demand for a particular style.
How much you buy depends on how much you intend to sell as well as on opening and closing stock levels. Further factors influencing your purchasing budget may include reevaluations, such as markdowns, gross margin, turnover and inventory differences due to deterioration or theft.

The difference between the total receipt plan for a period and the commitments already made for that period is known as open-to-buy (OTB). In other words, Open to buy is the purchasing power still available in a period after the deduction all receipts that may fall within the planning period.

Events that lead to a change in open-to-buy include:

· Change in planned sales
· Change in planned markdowns
· Change in planned stock
· Change in planned receipts
		
Moreover, a flexible planning system allows you to plan proactively; that is, you not only plan open-to-buy, you also monitor and constantly revise it with reference to the actual data situation. This is a separate forecast than the plan.  A buyer will still compare his or her forecast to actual last year and plan information.  The following list will go into more detail. 

The ability to plan in different periods – Days, Weeks, Months, Quarters, Years, Phases of Seasons, Total Seasons.

This is not supported by the system.  Currently, the user is forced to view the key figures in the default time of the infostructure (Month, Week or Day) or use a time variant within the planning table.  Retailers require the ability to look at planned and actual data in multiple times in the same planning table!  They would like to see this years sales YTD, then by month, and finally by day.  To do this today in the same planning table is impossible.  The user is forced to use three different planning tables from three different infostructures.  This is a MAJOR problem with the current SAP retail planning system.

OTB creation for various merchandise levels including category, department, division, and buying group.

This is supported.

Ability to create OTB in units and dollars by store, region, or total company.

Currently, the OTB system converts the dollars to units based on a hard coded macro that uses the Average Price Bands defined in the IMG.  The system does not look at the actual master data of an item or item conditions records.  This needs to be remedied.  The planning system should have the capability to read the current prices and markup percentages of the items and bring them into the plan.  Maintaining the Average Price Bands in the IMG is very time consuming and is not as accurate as many retailers require. Typically, the retailer will plan in dollars and then need the plan broken down into units based on the average retail of the category or the actual condition records of the items in the category.  


Reebok Comments:
In converting OTB from $$ to units, and vice-versa: need to distinguish
between selling average retail and inventory ownership average retail.

Tie in with the corporate level turnover objective building from both top down and bottom up.

This is supported in FB consistent planning.

Planning as much as a year out, with revisions made periodically.

This is supported.

Ability to plan and switch between dollars, units, and percents.

Currently, the OTB system converts the dollars to units based on a hard coded macro that uses the Average Price Bands defined in the IMG.  The system does not look at the actual master data of an item or item conditions records.  This needs to be remedied.  The planning system should have the capability to read the current prices and markup percentages of the items and bring them into the plan.  Maintaining the Average Price Bands in the IMG are very time consuming and not as accurate as many retailers require. Typically, the retailer will plan in dollars and then need the plan broken down into units based on the average retail of the category or the actual condition records of the items in the category.

Automatic calculation of average unit retails and markup percents for hierarchy levels.

See above.  Average Markup percentages are not supported.

Using sales, markup, markdowns, and planned shrinkage, calculate merchandise gross profit for the hierarchy levels.

The current OTB macros in S110 do not calculate the gross profit at any level.

Sales, markups, markdowns, planned shrinkage, receipt, and merchandise transfers updating open to buy on a daily basis for each hierarchy level.

These all updated in the S110 OTB infostructure.

Open to buy being calculated based on inventory turnover objective.  Taking into consideration order frequency, total replenishment time, average unit retails, in stock goals to establish an average weeks on hand.

Order frequency, total replenishment time, average unit retails, and in stock goals to establish an average weeks on hand are not part of the current s110 macros.  Because the planning system does not read the master data from the other areas, it can not look at many key pieces of data including the total replenishment time.  The forecasting methods in the planning table may be able to be used to derive some of this information, but average weeks supply should really be a part of the standard OTB macro.

Open to Buy End of the Month Stock Driven.  In other words, all other key figures are variable and dependable on the EOM stock plan.

EOM is supported via a macro in the S110 planning table.

Compare projected on hand each month to determine the open to buy or overbuy for each month.

Actual OTB is calculated per month with a standard macro in S110

An overbuy or not buying up the full open to buy for one particular month would affect the calculation for the open to buy for the next month.

This can be configured in the planning system.

Reserves would be made for new items or later developing categories.

This can be configured in the planning system.

 Be able to show last years on hands the first of each month for each hierarchy.

This is called opening stock and is a standard part of the S110 infostructure.

User has capability to customize OTB reports in addition to standard reports.

This is capable.

Exception reports produced showing greatest variances of OTB and over/stocked and under-stocked hierarchies.

This is capable using the Early Warning System in the RIS.

Show actual Merchandise turnover compared to planned turnover.

This is a standard key figure.

Reebok Comments:
Besides seeing planned and actual key figures, a planner needs to see "last
year".  SAP currently lumps every transaction as an issue or receipt.  This means
that if a retailer issues a mark-up, the receipt  key figure goes up in
value.  If a retailer issues a markdown, issues go up in value.  The same
with inventory adjustments (either an issue or receipt depending on the
type), POS mark-downs (issues),  An inventory shrink represents an issue,
an overage a receipt.  Planners need to plan net sales, all the different
types of markdowns, "true merchandise receipts".  Adding mark-downs and
sales as issues is unnecessary.  Lumping real merchandise receipts
with mark-ups and stock adjustments and inventory overages is also
unnecessary and confusing.  Considering a mark-up a receipt is not proper
retail merchandising.


Be able to display current open to buy for each of the next 12 months.

This is a standard key figure.

Pet Smart Comments:

Forward Buys that satisfy guidelines are approved subject to preset overall parameters and limits.

21.  OTB should “look ahead” so unusually large orders placed in the early in the OTB period ca not lock out important orders that may come up later in the period, particularly basic replenishment item orders.



II. Open to Buy

The standard Open to Buy process is as follows:

The process is to compare the plan values of sales, average stock, receipts, mark up, mark downs, gross margin and turnover to the actual situation.  The process of  Open to Buy is identical to the merchandise planning process with the exception of updating actual results to monitor the plan.   

The requirement of Open to Buy are as follows:

The ability to create an Open to Buy plan at the same levels as the merchandise plan.




Priorities for Merchandise Planning Development:

The integration of merchandise planning with allocation, purchasing, and the merchandise hierarchy, article master data, and RIS data. 
The “what if” analysis capability or simulation functionality.
 The ability to complete sub plans independently and be totaled at a high level of the merchandise hierarchy.
The ability to complete an assortment plan with the completed higher level plan.


ALLOCATION

I.  Allocation

The most common approaches are allocation based on:

Actual selling- this allocation is done solely on the basis of the sales history of a particular item at a particular location.  This is most commonly used to fill in merchandise on an existing item.

The concept of the allocation is critical for the Apparel retailer in the Americas.  It is the main mechanism for both the initial stocking of merchandise in a group of stores as well as for the continual flow of seasonal merchandise from the DC to the stores.  Most retailers will make seasonal buys months before season via Purchase Orders.  These Purchase Orders will then have an allocation assigned to them in order to facilitate the distribution of merchandise out to the stores.  Therefore, the retailer requires an extremely tight integration between the item master, planning, allocation, purchasing and information systems modules.  This integration simply does not exist in SAP retail today.  The allocation module barley speaks to the item master and can only utilize planned and actual data via the Allocation Generation program.  This program is very hard to use and especially difficult to maintain.  Because it sits outside of the planning modules, the user is forced to create and keep detailed knowledge of thousands of allocation rules and rule changes.  There is no real link between the item being distributed and the allocation rule that will be used to spread the quantities across the stores.  (Except one table in the IMG). Of particular concern is the allocation rule having to be assigned for every item in an allocation table.  This was meet with considerable pushback from the retailers to which it was shown.  The system should inherently know which allocation rule will be used based upon the seasonal merchandise plan.  In addition, model allocation rules were a major concern to the prospective retailers.  They require too much manual intervention to create and maintain,  and the logic that creates stores groupings is extremely "fuzzy" at best.   Overall the allocation module was shown to many retailers and was deemed to lack the robust functionality that is required in this area.

The allocation process should not be a separate component of the SAP system, but should be a part of the planning process as a whole.  The better niche merchandise planning products in the marketplace allow allocations to be a part of the merchandise planning tables themselves.  In fact, after the merchandise plan is set at the assortment level, the other systems produce "Allocation Wizards" which allow the user to schedule the creation of allocations based upon pre-set algorithms like weeks supply, average inventory in dollars or units and sell through %.  The user can easily access these models and the appropriate distributions are created across characteristics and store groups.  Purchase orders can then be automatically generated in either a pre or post distribution format.  There is a tight link between the merchandise plan, the allocation distribution and the purchase order.  If any item or piece of data is edited in the any of the modules, the others are updated automatically.  This is critical for creating re-allocations based on held back merchandise at the distribution when there are very short lead times.  The allocation process needs to be completely reworked in the SAP Retail system to ensure that the apparel retailers have a robust and feature rich product to distribute their merchandise.



Fabri-Centers/Jo-Ann Stores Comments:
Allocation algorithms
The allocation algorithms should be flexible to spread information at various levels:
Stores
Week
Attributes of a department


Plan need- this is an allocation done on plan need only in order to ensure that each location is on stock plan in all categories.  This approach is mostly used for new items or programs.

Allocations tied to the merchandise plan must be able to utilize planned data, actuals or a combination of both.  In addition, allocation data elements need to have the ability to be modeled after like objects.  This is particularly important when introducing a new style or store.

Plan need and actual selling- this approach layers the two above instructions in order to achieve both results.  This is a case where the individual item must be in stock at all locations, and the stock plan is important as well.

See above.

Weeks of supply-this approach allows the user to have a target weeks of supply at all stores and the system will allocate the proper units to achieve this taking into account on hands, on order, and sales trend of the style.

This is a method of allocation that the user should have at their disposal via an "allocation wizard".  By choosing this option, the system should consider all relative data and propose an in-stock quantity for the item in a store across a certain number of weeks.  The allocation should then generate the proper transaction (either Purchase Orders or Stock Transports for the item depending on the source of supply.) automatically.  The actual selling patterns need to be constantly monitored by the system and the future allocations adjusted accordingly.  After the adjustments, the transactions that the plans have created need to be adjusted to reflect the change to the allocations.  In the case of a pre-distributed, cross-docked or DSD Purchase Order, the change of allocations need to be communicated to the vendor so they can pack and label the merchandise properly.

In all approaches, the system must take into account on hands, on order, and sales trend of either the style being allocated, or a like item.

The like item from the item master must be made available to the planning modules and the allocation modules so that distributions can be created for new items. 

Reebok Comments:
Allocation table screens such as plants/view 2 need to be modified to
include additional key figures.  An allocator, after splitting" quantity to
many plants, need to review the allocation quantities by plant by comparing
against on-hand, sales, on-order, weeks of supply.  Currently the system
only provides unrestricted stock

To do anything dynamic in allocation, a retailer needs to develop the
strategy function module.  The other choice, allocation rule generation,
only looks at one key figure at a time, the rules have to be continually
"re-generated", really creating new rules.  Even then, the system simply
assigns a proportional quota based on the key figure analyzed. To develop
allocation strategies that can assign quotas based on analysis of multiple
key figures at the same time in an algorithm, a retailer is forced to hard
code strategies.  In effect, a retailer is building its own
allocation system from scratch.  SAP should offer a set of
industry-standard allocation algorithms that retailers would only need to
customize.  A retailer could then develop business specific additional
rules only.   Also, if allocation strategies could be developed via a
customizing "formula toolkit" (as the competition offers) instead of hard
coding the entire function module.

Performance, as in merchandise planning, is also a large obstacle in SAP.
100+ plants and variant materials (18 shoe sizes) create 1200 line plus
follow-on document generation runtimes that are not acceptable.  Large
tables dump, and multiple users (as most companies have) using follow-on
document generation cause short dumps. This will not be acceptable to a
1000 stores plus  fashion speciality /dept  chain.



 In addition, the system must be flexible enough to allow re-allocation of merchandise based on vendor short shipments or a trend change in the items on the purchase order.  

Again, this speaks to the need of a tight integration between planning, allocations and Purchasing.  If the vendor has short shipped an item, the allocations need be adjusted at the time of goods receipt.  Just as the inventory module can generate a PO from a goods receipt, the retail system should have the ability to automatically adjust an allocation table for a PO receipt if an allocation is tied to the PO and the PO has a quantity discrepancy.  Currently, the system requires the user to manually adjust the allocation table based upon a short ship.  In addition, there needs to be robust functionality to accommodate the splitting of pre-packs in this instance. The business process is as follows: if a partial shipment occurs from the vendor, there needs to be logic in the allocation rule that will determine what quantities of a style are sent to which stores.  The easiest thing to do on a partial is to just use the normal ratios from the allocation rule to distribute the merchandise.  But this may result in the C-stores receiving little if any merchandise at all.  Why?  Because if you always give the product to the A and B stores and ignore the C stores, then a C category or C store will always remain a C in the rankings.  Thus, there needs to be logic to determine how much quantity to distribute to the stores on a partial, and to determine when the pre-packs should be split to adequately distribute certain variants to the C stores. The current rounding rules defined in the IMG are not sufficient to accommodate this requirement.

 On line changes to the OTB (Open to Buy) would be converted to units, using an average retail and sent to the allocation system.

Currently, the OTB system converts the dollars to units based on a hard coded macro that uses the Average Price Bands defined in the IMG.  The system does not look at the actual master data of an item or item conditions records.  This needs to be remedied.  The planning system should have the capability to read the current prices and markup percentages of the items and bring them into the plan.  Maintaining the Average Price Bands in the IMG is very time consuming and not as accurate as many retailers require. Typically, the retailer will plan in dollars and then need the plan broken down into units based on the average retail of the category or the actual condition records of the items in the category.  

The ability to create an allocation without a purchase order.  Once the purchase order is created the ability to attach the allocation.  This step needs to allow the transfer of the allocation to the purchase order, which enables the vendor to pack the order by store.  For example, this process is normally done in fashion when you want to create a “bottoms up” purchase order for a new item based on a like item’s sales history.  

Currently, you can create a PO from allocation table, and in 4.5, you will have the ability to create an allocation table directly from the purchase order.  This functionality needs to be enhanced to allow the Purchase Order to be cross-docked at the DC but still communicate the store packing and labeling requirements to the vendor at the line level.  Currently, noted are used in the header of the PO to indicate the DC to which the vendor should ship the pre-packed merchandise.  I believe that a more elegant solution should be designed to accommodate this requirement.  (EDI should be considered during the design of this modification.) 

The ability to allocate a purchase orders that be already created in bulk, and modify the quantities.  This step allows an allocation of an existing purchase order.  For example, in fashion there are cases where an item is re-ordered that is NOT on replenishment.  In this case, there is a purchase order created that is not pre-allocated.  Once the ship date approaches the order then needs to be allocated.  There must be functionality that allows the planner to access the purchase order, allocate it, and attach the allocation to the order.  This will facilitate the same process as above, allowing the vendor to pack by store.

See above.

The ability to plan the allocation at merchandise category level, however allocate at style, color size level incorporating pre packs assigned by the vendor.  The system should recommend color and size ratios based on past selling history of a like item.  

There is no current functionality to accommodate this requirement but in 4.5 allocation rules will be able to go across the variants of a style using ratios.  This may work, for some pre-packs, but it will need to be greatly expanded to accommodate the concept of the master pack.  This is where multiple pre-packs across multiple styles are considered as a group for distribution.  An example of this would be where a blouse and a skirt are considered as a part of the same pre-pack ratio.  Simply creating two pre-packs will not work.  The user would have to remember to but them both in the allocation table.  The system needs to be modified to accommodate the "master-pack" concept and correctly create planning and allocation distributions accordingly.

The ability to plan at the merchandise category level, and transfer that to an assortment plan, which will allow allocation of each item in the category without creating a plan for every item.  

This speaks to the ability to create multiple mini-plans that are linked together and kept in synchronization.  The category plan will link to the assortment plan which can then have an "allocation wizard" attached to it to create the allocations of the styles in the assortment across the store groups and stores.  Currently in SAP Retail, the user is forced to create one huge plan down to the article and store level.  Store groups would not be available nor would assortment ranges.  The allocation module would then have to read this table to create multiple allocation rules.  Those allocation rules would then have to be placed into a manually created allocation table that is not connected to the date at which the seasonal merchandise must be in the stores.  If anything changes, the user must manually update all the different modules and transactions.  This will not work for apparel retailers.

12.  The ability to view the allocation matrix of style, colors, and size on one screen.

This can be done only within one style at a time.  Retailers require the ability to view the allocations across characteristics of multiple styles and within multiple store groups.  They would like to view the size XL items, in color black across the stores that are 5,000 sq. feet or larger.  This is the type of analysis they are looking for in an allocation system. 

Once the system has recommended an allocation, the ability to modify on one screen to see recommended quantities and new quantities.  

A central area to view planned data and allocation transactions is needed.  

Once the allocation is complete and the purchase order is approved there should be an immediate update of the styles on order at location level to have accurate inventory information.

Purchase Orders currently are visible as on order at the store locations.  If an allocation is tied to the PO the retailer requires the ability to drill down from the PO and see the future allocation.

If the purchase order is cancelled or altered, there should also be an immediate update to inventory levels.

See number 1 above.

16.  The ability to link a store to a distribution center.  The primary reason for this is to allow the vendor to bar code each box shipped with the dc address and the store number.  This will allow the boxes to be cross-docked at the dc.  In other words, the box is scanned into the dc, and then scanned to the appropriate outbound truck to be sent to the store.  As mention above, the vendor needs to have all of this information on the PURCHASE ORDER.  Again, the purchase order should include each line item; both in summary format and allocated format, with a link between stores and dc’s.

See number 8 above.


II. Allocation


The Standard Allocation processes are outlined below:





















Process type 1 and 2 for New Merchandise :




Process type 3 and 4 for Subsequent Deliveries 




The overall requirements for allocation include the following most common standard  methods:

The ability to allocate utilizing actual selling information at any level in the merchandise hierarchy.  

The ability to allocate based on the unit plan at any level in the merchandise hierarchy.

The ability to allocate based on a user defined weeks of supply target.

The ability to allocate based on the sales history of the specific item being allocated, or the history of a like item.

The ability to create site groups based on selling history of the specific item, the history of a like item, or at any higher level in the merchandise hierarchy.

In all of the methods mentioned above, the calculation of determining the proper  allocation must include on hand, on order, and sales in the time period designated by the user.

The ability to re-allocate an order based on actual goods receipt quantity if there is an overage or shortage.

The ability to view the allocation matrix of style, color, and size on the same screen.

The ability to modify the recommended system quantities in a separate column on the same screen.

SAP –PWC  apparel workshop

 AKTUALDAT \@ "tt.MM.jj" 31.08.98 	 SEITE 26





 EINBETTEN PowerPoint.Slide.8  




 EINBETTEN PowerPoint.Slide.8  

 EINBETTEN PowerPoint.Slide.8  

 EINBETTEN PowerPoint.Slide.8  

 EINBETTEN PowerPoint.Slide.8  

 EINBETTEN PowerPoint.Slide.8  



