---
date: 2026-04-26
type: raw
source: /Users/gclyle/Desktop/RETAIL/SAP Retail/teilprotokol2.doc
tags: [retail, sap, apparel, promotions, pricing, purchase-orders, replenishment, article-master]
project: canary
status: processed
method-role: PhD
method-stage: research
---

**Wiki:** [[Brain/Home|Home]]

# SAP Apparel Workshop — Promotions, Pricing, PO Management (1998)

## Source
SAP AG / PricewaterhouseCoopers apparel workshop, August 1998. Partial protocol covering: Promotions, Pricing, Purchase Order Management, Replenishment/Forecasting, and New Article Creation. Companion to `sap-fashion-workshop-1998.md` (Merchandise Planning, OTB, Allocation).

## Raw content

PROMOTION

I. Promotions

Ability to require approval by designated levels of management.

Currently there are a few status codes at the line and header levels of the Promotion but there is not a formal approval workflow case.  One should be created.

Information needed when building a promotion:
- Current stock on hand
- Sales history of past promotions for the article/category
- Purchase quantities of prior promotions 
- Comparison of past promotion to current plan
- Regular cost, retail and gross margin per article/category
- Promotional cost, retail and gross margin per article/category

A majority of this information is available in the S086 infostructure in the RIS.  However, current retail, cost and profit are not available in the promotion until it is saved.  This needs to be fixed.  Retailers will set the promotional price by taking an absolute or % off from the current retail.  Summary views are also needed on the promotion by store, category and characteristic.  Lastly, when creating a new promotion you need the ability to copy a comparable promotion and make % or absolute changes to relevant pieces of data.  An Example: copy last year's Labor Day promotion, up the new retail by 10% across all large sizes, increase the planned sales quantity in the stores in the North East by 1000 units on the dinnerware department and decrease the new retails by a full price point for all other products that are part of the copied promotion.

  Special instruction text box. I.e. Placement of merchandise at store level

Texts are available at the line level in the Promotion module.

 Plan sales by store in units and dollars

See the merchandise planning and OTB section.  The same tool is used for promotion planning.

Store needs the ability to review suggested allocation quantities and change if necessary. Past sales history needs to be available by store to review.

Allocation Tables can be tied to promotions.  Please see the allocation section of this document for suggestions on methods to improve allocations.  Past sales history can be viewed in the RIS.

Advertising allowances from vendors should be viewable on promotion set-up screen.

Rebates are in the condition sections of the promo. Should have a method to spread the rebate dollars defined in the header to the lines.

Recommended promotional purchase orders should be created by request with the following
Information:
-Current stock on hand
-Current rate of sale
-Previous cost, retail and gross margin
-Recommended quantities per store and total
-Sales history of item/category
-Understock/overstock’s from past promotions
-Timing

Currently, purchase orders have to be manually created from a promotion.  They are not a part of the normal replenishment of an item.  This is a problem. Many retailers would like to create promotions that can be tracked in the promotion module and in the RIS but are a part of the normal replenishment process of an item.  They would like the planned promotional sales quantity to be compared against the normal sales of the item and the replenishment factored to include this "lift".  They would then have to have configuration options on whether or not to build this additional sales into the consumption of item or to smooth the demand that is recorded during the promotion.   Typically, for promotions that occur at the same time every year, they will want the demand to be included into the consumption totals of the item.  If it is a one-time promotion, they will want the promotional "lift" smoothed out of any future forecasts. 

Ability to run a percent off ad for entire category

See number 2 above.

Have the ability to receive promotional retails by entering a desired gross margin.

System should be able to "model" the retails in the promotion entry screen.  Currently, the system forces the user to enter the new retail without even showing them what is the current retail, cost, mark-up and profit % or dollars.

Allocation system to determine suggested quantities to ship from dc to store during promotion based on previous day's sales.
 	
There is no allocation model that will produce an Open-To-Ship.  Once must be produced especially for promotions where increased sales activity must be monitored very closely.

Workflow and early warning system need to be set up to monitor every phase of promotion.

There is currently no workflow to monitor promotional status.  One needs to e created.


II. Promotion Planning

The process of promotion planning is utilized in two ways:

To plan the promotional sales and stock requirements for a specific promotional time frame designated by the user at any level in the merchandise hierarchy.  This step is utilized for the system to forecast sales and stock requirements for the promotion period.  

2.  At this point the system should recommend a purchase order for the promotion in order to achieve the sales goal.  Either by new order creation or stock transfers from other stores or the distribution center.  If necessary at this point the planning system would link to an allocation table and create a recommended purchase order based on user designated goals by store or store group utilizing the same methods outlined above in the allocation requirements.  If there is stock available in another store or the distribution center the system should create a stock transfer automatically.  This should also be done at any level in the merchandise hierarchy.

After the promotion is planned we will utilize the promotion to recap the sales performance of a specific promotion to utilize for future analysis.  The key figures involved include, but are not limited to sales in currency and in units, gross margin, and stock levels.  The system should begin to monitor the results of the promotion immediately to react to actual sales information and either transfer goods if available or suggest another order from the vendor.  If the specific stle is no longer available from the vendor we can choose to utilize this data for a similar item for substitution.

The process can be included in merchandise planning, however it should be an independent transaction.  There must be a tight link to the merchandise planning process specifically markdown planning.  

The requirements are as follows:

The ability to create a promotion plan by utilizing mass maintenance.  In other words create a promotion plan by site group, merchandise category, color, size, or any level the user designates within the merchandise hierarchy. 

The ability to create the promotional plan in currency or in units.

The ability to do “what if” analysis or simulation for the promotional plan with the same methods outlined in the merchandise planning requirements above.

Standard workflow and early warning system set up to monitor the following user designated phases of the promotion.

High sell-through
Low sell-through
Actual sales higher or lower than plan sales

PRICING

I. Pricing

The capability to do mass price changes (either temporary or permanent) by the following key figures: category, size, color, style, vendor, department, and buying group.

This is a major need of the SAP retail-pricing module.  Currently, there is some ability to execute mass price changes but the retailers requires capabilities that are much more granular.  
Price changes can be made as a percentage plus or minus for a category, site, vendor, sales area, season and one or two others.  However, the ability to execute price changes across characteristics is currently not supported.  As an example, a common retail price change might be up the price by a price point on all large women's barn jackets in the stores in the Northeast.   Also, the ability to absolute price changes is not supported using mass maintenance tools.  Retailers would like the ability to create $1.00-offs without having to make the change for every item. 

In addition, there a number of price fields that the SAP retail system needs to capture in order to provide retailers the functionality they are looking for.  These include, but are not limited to, "was/is" price, "compare at" price and competitor's price.  These prices should be made available in the retail-pricing schema and should be able to influence EKNN.  For each of these new prices, the system needs the ability to present these as additional prices in the purchase order, pricing, sales order and labeling programs.   Specifically, in the case of entering and tracking competitor's prices, the SAP retail system needs the ability to create shopping lists of items that will be priced by shoppers at regular intervals.  Typically, these are then uploaded from a handheld unit or flat file into the host system and the new competitors prices are now stored in the system.  SAP has no functionality to accommodate this situation.

Lastly, the SAP retail-pricing module needs the ability to link items together for pricing purposes.  This occurs when items in across categories need to be treated similar for pricing purposes.  The common fashion retail example is that if the retailer has a women's outfit, that consists of a jacket, a blouse, and a skirt, these articles need to be marked down all the same when a markdown is initiated.  The items are obviously in different categories and may be from different vendors.  Thus, they need to be linked so that of a buyer marks one of the items down, he/she is immediately prompted that there are linked items to this item and they also must be marked down as well.

The capability to do prices changes either by percentage off, dollars off, or new price.

See above.


The ability for the system to forecast the sales and margin of a price change to understand the effects if the markdown.  For example for a promotional price change, the system could look at the last time the item or category was promoted at that price and the effect.  If it is a new item on promotion, compare with a like item to calculate the forecast.  In the case of a clearance markdown calculate the sales and margin forecast based on the new markdown price and use current rate of sale to determine the estimated time the item or category will sell out.

This is perhaps the biggest complaint of the SAP retail-pricing module.  The system is not really designed to execute price modeling before making price changes.  Price modeling is the capability to do "what if" scenarios to obtain a desired financial result based upon forecasted and historical sales of articles or categories.  This would be very similar to the markdown-planning module in the system however, it would available in the pricing and promotions modules as well.  This would allow the buyer or planner to simulate the effects of changing the price of an article before actually executing the price change or finalizing the promotion.  Items of interest to the buyer include effect on margins, sell through, gross sales, net sales and GMROI.  

After the desired pricing or promotion model is created, the system would then route the price changes via workflow to the appropriate users for approval.  (As part of the workflow case, the system needs to understand the maximum price change that a certain user can make without approval.  If the user makes a change that is larger then his tolerance, the workflow approval process is initiated.)

The ability to have several future price changes for the same item/category.

This is possible as long as the dates do not overlap.  


The ability to enter price changes at the store level, region level or store group level.

This is supported.


The ability to recap sales by price change to determine the best selling price and period.

The system currently keeps a history of the condition VKP0, so the user can see the number of different prices that the condition record has had.  However, what is missing is the ability to sales analysis at these different condition record values.  A very common request from retailers is the ability to see " the sales of article x-y-z when the price point was $19.99 as compared to when the price point was $24.99."  This type of analysis helps the retailer to determine if certain markdowns (temporary) were profitable.


If a category or department is “low owned” the ability to trigger the ownership price with a check mark.  Low ownership is simply the price that the inventory is valued at.  This is also the price that the item is most commonly sold.  

This is not supported by the system.



II. Price Management

The development plans for price management satisfy the main requirements that we outlined.  These include price modeling and competitive pricing analysis.  The only additional requirements we would like to request are as follows:

The integration of the price management module with the planning process, specifically markdown planning.  This is needed to compare the actual results of a specific price change to the plan.

The ability to link items in different categories together to alert the buyer that a related article is being marked down  For example, If a jacket in a merchandise group is being marked down the buyer would like the system to alert them of the other articles that are linked to this article to determine if the other articles need to be marked down as well.

The ability to view pricing history by any level in the merchandise hierarchy when conducting price models.

The ability to execute price changes by any level in the merchandise hierarchy, and in addition by store groups, or regions.

Allow pricing codes to be entered by price change to deferentiate promotional price changes from markdowns due to poor performance.  Some examples could include poor color, poor size, poor fabric etc.








PURCHASE ORDER MANAGEMENT

I. Purchase Order Management

Purchase order management is also a large part of a buyer’s job.  The following functionality is imperative.

PO created from assortment plan for season and month

This is currently not supported.  The system needs to be able to automatically feed the merchandise plan into the PO module and create the purchase order to the vendor for an upcoming season.  Then, the system needs to automatically assign the allocations based upon the stores in the plan.   To accomplish this currently, the user has to copy SOP information to Demand Management and then run MRP to create the purchase orders.  This is two many steps for the retailer. They want to create PO's directly from the merchandise planning modules.

  PO updates automatically if plan is changed.

The purchase module and the planning module are currently not integrated. They need to be.  See the merchandise planning section above.

OTB impact prior to release of PO to vendor.

This is supposed to be supported with the creation of the PO status functionality. 

Should contain all of the following:  
-Total cost
-Total retail
-Total dollars spent with this vendor for month/year by merchandise category.
-Gross margins per item and total PO
-Distribution information for DC
-Ability to change cancellation dates and re-allocates PO by month.
-Terms

The system currently does not display some needed information in the Purchase Order.  These include: total retail in the header, retail at the line level, markup at the line level, profit % at the line level, Distribution Center information in the header for a pre-distributed cross-docked PO and line item cancellation date.

Early warning system to:
-Notify you that the document is being sent to the vendor
-Cancellation date of PO is near
-Vendor shipment of PO
-PO was being received at the DC and percent completes
-Ability to accept back-orders or ship complete/cancel balance
-Acknowledgment of PO receipt by vendor

All the above are possible using SAP workflow with the exception of the PO line cancel date.  The retailers require a cancellation date at the line level at the PO that will automatically cancel the remaining quantity of a line if it has not been received.  This also has to be integrated with a change PO EDI document to notify the vendor.

View document and line items by:
-Item total (summary)
-Single item with allocation
-Total units on purchase order
-Total dollars on purchase order
-Allocation of all styles to one store

They PO needs to have multiple views for the retail buyer.  These include all of the summary levels listed above.  Currently the user has to run reports to obtain this information.  The retailers would like to be able to get this summary information while working with the Purchase Order module.  Also, if a pre or post allocation is going to be attached to the Purchase Order, the buyer needs to be able to drill down to this information.

Ability to view PO allocation by color/size etc.

Currently the retailer has the ability to view the color/size matrix at a style level only.  Two additional requirements are to have a matrix appear when the generic article has more then 2 characteristics and to have the ability to view summaries of the PO ACROSS styles.  For instance, the buyer will want to see all the color red article variants across a number of generic articles.

System creates a markdown automatically after designated time by user after PO received for special purchase merchandise.

I believe that this can be accomplished by the workflow markdown requirement that was written for the USA demo system. Should be incorporated into the core Retail product.

After PO sent to vendor all changes to item master update PO automatically.
i.e. cost, retail

There currently limited functionality to change the item data from a Purchase Order.  This is accomplished primarily through the creation of the information record.  This needs to be expanded to include all master data.  More importantly however, is the need to have the system automatically create Articles from their inclusion on the Purchase Order.  If a new style is entered on the PO, it should automatically be created in the article database with the default data from the Merchandise Reference Article and the data from the PO.  This is due to the fact that the buyers do not have the time to enter the master data and then create the Purchase Orders. In the apparel industry, both are done art the same time.  The retail software competitors in the USA have this feature.

The  ability to view PO by specified time period for :
-Vendor
-Category
-Article

Supported.

View past due Purchase Orders.

Supported.

View open Purchase Orders by status to include:
-Open
-Pending
-Canceled

Need PO status.  This was supposed to be a new feature in the 4.5 product.

Acknowledge confirmation of PO by vendor

Supported.

Status of PO at header level to include:
-Open
-Receipt
-Canceled

Need PO status.  This was supposed to be a new feature in the 4.5 product.

Automatic approval of Purchase Orders by OTB receipt plan.  Early warning if additional approval is needed.

This was supposed to be a new feature in the 4.5 product.

16.   Market purchase orders- In the US, retailers attend markets or trade shows where the vendor’s present new merchandise for the next season and retail buyers must give vendors purchase orders on site.  For this business practice, there needs to be a process that allows the creation of purchase orders off line accessing a data base with information needed for analysis such as sales history by style, season, category etc.  Once this purchase order is created, there must be a process to download into the R/3 system.

We do not have anything like this.  The competition does.


II. Purchase Order Management

For the process of when and how a purchase order is entered, see the same exhibits mentioned above in allocation.




The requirements for purchasing are as follows:

The most important requirement for purchasing is the integration with allocation and merchandise planning (OTB).  

The integration with allocation is necessary to allow the allocation to be sent on the purchase order to the vendor, and allow the buyer to view the allocation from the purchase order.  

The integration with merchandise planning (OTB) is necessary for the updating of actual on order information on the (OTB).   The ability to view the impact of the purchase order to the (OTB) before being released to the vendor. 

The purchase order should include the following information in the header:
Total Cost, Total Retail, Mark up information for allocation, Terms, and Cost, Retail, and Cost, Retail, Markup by item.

The ability to view the purchase order by:
Item total
Single item with allocation
Total units on the purchase order
Total currency on the purchase order
Complete allocation by individual line item
Status, either open, pending, or cancelled
The ability to view this by any level in the merchandise hierarchy, and any period of time.



The following early warning requirements for workflow:

Show all purchase orders that are pending cancellation
Show all purchase orders that are being received at the DC
Show all purchase orders that are received by the vendor
Show all purchase orders that were received incomplete

The ability to create a purchase order remotely or on a notebook solution. 

The notebook application should have access the plan data used to create the purchase order. 
				


The functionality that should be included are:	-  new fashion order entry
							- purchase order creation
							- allocation module as an option as well.
When the user returns to the office, the new article information, purchase order , and the allocation will be automatically up-loaded into the R/3 system.





Replenishment/Forecasting (not discussed in the workshop)

Replenishment is the automatic reordering of basic assortment items.  These are items a retailer need never be out of stock in.  In most cases these are items with a number of colors and sizes that are difficult and timely to reorder manually.  For example: women’s hosiery, socks, undergarments, etc.
In addition, these items are promoted regularly.  
A replenishment system needs to have the following functionality:

Replenishment done at store-article level, however there should be ability to group stores together with similar selling patterns.

This can be accomplished at using the 'Replenishment' functionality in the 4.5 system.  It is important to have the capability to run forecasting by a group of stores.  In the current system, the S130 infostructure is used for forecasting.  Store group is not a characteristic of the planning hierarchy.



Reebok Comments:
In order to run standard MRP retailers need to apply profiles to material
master, logistics screen, at a variant & plant level.  This implies many
thousands of records to be applied to maintain a few generic materials.
SAP needs to be able to provide a transaction to dynamically apply either
planning or forecasting profiles across selected materials and plants.

The replenishment structure S032 needs to include reorder point values,
on-order and sales key figures for MRP flagged styles.  This would allow
planners the ability to analyze the reorder points against actual inventory
on-hand, on-order, sales, and a performance-type key figure such as weeks
of supply.  it now includes only safety stock.
MRP planning needs to be able to be run across selected materials and
plants, not only an entire plant all materials.
MRP results (stock requirements list) need to be run by selected range/list
of materials and plants, with sub-totals at material and plant levels.

In order to offer maximum in stock position, minimum order up to levels must be set.  This will enable the item to never have less than this number on hand at any time.

Supported via standard consumption based planning methods.

Counter Stocks to be entered if needed.  This is essentially blocked stock.  The system will not acknowledge it in order to keep a certain amount as fixture fill at all times.

Counter stocks are currently not supported by the system.  The work around is to create above normal safety stock levels or place the articles into blocked stock.   The ability to define counter stocks needs to be supported.

Forecasting functions to estimate future sales based on the current trend.  This function should be dynamic and that adjusts accordingly.

Supported via standard consumption based planning methods.

In order to promote replenishment items there must be functionality to create promotion orders within certain parameters.  For example, if you are planning to promote a specific category only in only a number of stores the system needs to flexible enough to allow this.

Currently, the system stores promotional demand in a separate consumption bucket from the regular demand of the item.   In 4.5, there will be a user exit that can be used to combine these two demands.  Most retailers feel that is a lot of work that they should not have to do.  There should be an IMG option on whether regular demand should be merged with the promotional demand for an item in a store.  Also, the replenishment system as a whole should be modified to be able to consider upcoming promotions when recognizing future replenishment requirements.  Today, if a promotion has been created but not turned into a PO or stock transport order, the replenishment system has no knowledge of its existence.  This could potentially lead to the creation of an overstock situation if normal replenishment includes the item in its RP run.

 System must enable buyer to set SKUS to auto reorder on basic merchandise that generally sells year-around.

Supported via standard consumption based planning methods.

A reorder point would initially be set by the buyer for new items based on anticipated sales possibly using the reorder point of an item it is replacing or a similar item.

Supported via standard consumption based planning methods.

A reorder quantity would be the quantity the system would buy when the item sold down to the reorder point level.  This would be based on such factors and minimum unit pack or minimum dollar order.

Supported with the exception of minimum $ order.  The system will look at quantity minimums.  I believe this is sufficient.

After an established period, for example, three months, the system would use the sales trend to update the reorder point.  Months, which contain no beginning on-hand, could be discarded so that stock outs would not affect the reorder point.

Supported via standard consumption based planning methods.

Seasonal peaks would be accounted for and estimates for the items would be adjusted for them based on the sales curve either manually entered into the system or already calculated by the system based on the merchandise category.

This is supported via standard consumption based planning methods with the exception of creating a sales forecast at a merchandise category level. 

The system would establish weekly sales estimates for each SKU and have the ability to place automated buys at least weekly.

Supported via standard consumption based planning methods.

The automatic ordering system would for example index, out 10 weeks of sales estimates for that SKU, subtract the current on hand and on order and place a buy for the difference of this number if it equals or falls short of the reorder point.  Example: We plan to sell 60 size 16 x 34 men’s 100% cotton white dress shirts in the next 10 weeks. We currently have 40 on hand and 12 on order. They are ordered in boxes of 3. The system would buy 9 additional dress shirts. A week later this same process would take place.

Supported via standard consumption based planning methods.

An example of how the system would trend would be as follows: For the first 4 months of this year, we sold an average of 6 of these dress shirts per week. Moreover, during the past three months we have sold and average of 10 per month.  If the user had put into the system for this category to re trend future estimated sales if there was a deviation of more than 30% in sales in a 3 month period then at the next automatic buy, the new buy would look at sales of 100 for the next 10 weeks.  This is all if this SKU was neither out of stock or did not go through a peak during this period.

This is partially supported by the system via the setting of the tracking limits and calculation of the Mean Absolute Deviation.  However, this tracks the accuracy of the forecast after it has been created.  This is different then actually doing tests on items prior to the running of the forecast to determine if the forecast should be re-executed. Testing for items to re-forecast is not supported.

The buyer would initially enter sales curve percentages into the system and then at some point have the system generate its own sales curves.  This would vary by merchandise hierarchy and location hierarchy, with some of these grouped.

At a higher level then store and article, this could only be accomplished in the planning tool.  As far as grouping stores, this is not supported in the planning tool.   At a store and article level, the buyer can make corrections to the forecasts and period totals can be manually entered.

The system would not only trend during non-peak periods, but also peak periods where the item was deviating from the sales curve.

Supported via standard consumption based planning methods.

Be able to drill down all hierarchies to determine sales trends.

This can only be accomplished in the planning tool.  See the Merchandise Planning section above.

View exception reports to determine merchandise outs, merchandise missing or exceeding trends.

This analysis is supported in the RIS.  However, the system needs a new Key Figure called "Days out of Stock".  They system needs to track the number of days the stock equals 0 in a store.  This of course will be rolled up the organizational and merchandise hierarchies.

Tied in with the open to buy system, showing current on hands and on orders.

This is currently supported with one MAJOR problem.  Buyers typically want to see the effect on OTB BEFORE they create a purchase order.  In the SAP system, as soon as you create a purchase order from a group of purchase requisitions, the OTB is hit.  Creating statuses on the PO may be helpful, but the buyers still want to see the effect a potential purchase will have on OTB before they create a PO.  They do not want to have to go to the OTB table and enter data to see this effect.  I would envision when the 'Assign and Process' purchase requisition program is run in test mode, they system should supply a number of retail and cost totals.  These should be by buyer, category, department and store.  These should be compared to the current OTB released budget and allow the buyer to see what the effect of converting the purchase requisitions to Purchase Orders will have on OTB.

Easily updated through physical inventories to correct on hands.

Supported.

The ability to create a new store purchase order of line merchandise automatically using a like stores assortment and sales trends.

Can be supported through the "Create PO via Reference' feature.  However, the retailer should have the option to take a "percentage copy" of the store order.  As example: copy store 120's typical store replenishment order but only take 75% of the line item quantities to build the store order for store 150 which is a new store.


Pet Smart Comments:

 Ability to utilize the SAP forecasting module to produce article/site forecast for the upcoming planning period, usually one-year.
Ability to move demand in response to changes in the calendar.  This would be used in to change the timing of events and advertising, to adjust from a 53 to 52 week year, and to move a holiday, such as Easter.
Ability to summarize the individual article/site forecasts into a total company within the merchandise categories and across categories into the divisions, departments, and classes. 
Ability to summarize the individual article/site forecasts for each location within and across merchandise categories.
Ability to summarize the daily/weekly forecasts and history into months. 
Ability to roll down changes at the month level into the daily/weekly details based on user-defined parameters.
Ability to present the base forecast in a structured report that includes similarly summarized history from last year and performance measure calculations.
Ability to utilize the high-level assortment strategy to adjust the forecast at all levels (article, merchandise category, class, department, division, total company) and to perform roll up and roll down reconciliation as required.
Ability to utilize the store opening and remodel strategy to adjust the forecast at the site level and to reconcile to the merchandise category as needed  
Ability to recognize and adjust for store opening, remodel, and closure dates in the store forecast.
Ability to adjust store forecasted sales based on anticipated cannibalization from our own stores, as well as, changes in the competitive environment.
The ability to recognize variances between the Financial Plan and the Merchandising/Store Forecast.





New Article Creation (discussed in the workshop only)

The process of creating new articles should be incorporated in the initial ordering process. If a  new style is entered on the PO,  it should automatically be created in the database with the default data form the merchandise reference article and the data form the PO. This process is necessary to allow fast purchase order entry for new items.

We would recommend an new transaction „New Fashion Item Order“. This transaction would allow the automatic creation of the articles at the time of purchase order entry, incorporated in one process.

Future uses of this process would be a notebook application, and internet processing to allow order entry at a remote location and later uploaded to the R/3 system. (see above)

The article entry process is different for fashion items and basic or NOS articles in all cases the vendor UPC/EAN number will be cross referenced to the appropriate style whether you are purchasing an NOS, Fashion, or High Fashion Article. The onluy difference is the level that the UPC/EAN is linked.

The standard process for fashion article entry is as follows:
Entry of department/merchandise category, vendor, season code/out-date, purchase price, selling price 1, selling price 2, vendor style, vendor color, internal style number at any level in the merchandise category.
For example:

Fashion Article
We are buying a  new dress style from our vendor. We enter the vendor number which included all colors and sizes that the vendor offers. However we also assign an internal number to the merchandise either by color, size, or some other level. 
IMPORTANT
We do not want to assign an article number at the color-size-level for this merchandise. Since, this merchandise is seasonal we are not interested in the selling by individual article only by style/ident number

				Ident number
				size
	
Ident number  color         or





High Fashion Article
We are buying merchandise with a very high retail value, for coats or diamond jewelry. In this case we need to assign a style/ident number for every item in our inventory. This is done because this merchandise has individual qualities that are necessary to monitor. For example, the origin of the mink on the coat, or the clarity/imperfections of a diamond. This will also allow you to store customer data as well for marketing purpose.

	
				size
	
color    		Ident number




NOS/Basic Article
We are buying merchandise that is to be never out of stock. In this case we need to track the articles by color and size. The article structure would be identical to the fashion article above with the following exceptions. We need to add both a color and a size code to track by individual color and size. This structure would be identical to the vendor UPC/EAN number.

				Ident number
				size
	
Ident number  color         and			 UPC/EAN





Pre-packs
In branded merchandise pre-packs are determined by the vendor. The pre-pack number is the same as the article style/ident number. Within the pre-pack usually are either different sizes of the same style or different colors and sizes in the same style. In this case retailers are only interested in the RIS data of the total style not the individual sizes and colors. This also allows cross docking at the DC. A pre-pack is only created at the style level with the same retail items.

In private label merchandise it is most common to maintain the articles at the color and size level. In this case you well break the pre-pack at the DC and ship individual quantities to the stores/sites. You may have a vendor “lot number” assigned to the pack, but it is in  no way used for item tracking or analyzing. In this case you enter each article with a separate number, or a generic article with variants.

In both cases above there is a separate pre-pack number, and item number. There is no need to maintain any data at the pre-pack level. 


Summarize

The overall requirement that was identified in the workshop was to integrate all of the R/3 modules including merchandise planning, allocation, purchasing, the RIS data, and the article master data.

We didn´t found out big differences between the work of German and American apparel retailers.

On comparing the main points of the SAP America/Specialty Official Development Document with the identified gaps by the prototyping group, the team found out that the representatives of both identified nearly the same gaps.


SAP –PWC  apparel workshop

 AKTUALDAT \@ "tt.MM.jj" 31.08.98 	 SEITE 1






 EINBETTEN PowerPoint.Slide.8  

 EINBETTEN PowerPoint.Slide.8  

 EINBETTEN PowerPoint.Slide.8  








