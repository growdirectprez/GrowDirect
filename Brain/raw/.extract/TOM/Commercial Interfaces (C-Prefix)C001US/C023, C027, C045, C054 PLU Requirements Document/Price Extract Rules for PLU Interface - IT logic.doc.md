Publishing of price / promotion changes
For background information only:

(my understanding of the process – so needs to be sense checked by an ORPM expert)

Within ORPM clearance and regular price changes and promotions can be set up at different levels e.g. using zone (store) groups, or individual stores, and against subclasses of products or individual products. It is also possible to set up a promotion for a zone group and exclude a store or for a subclass, but exclude certain items. 

These are all presented on RIB messages, and therefore to the Integration Layer, fully exploded to ‘item in store’ level, so for example, the Integration Layer would be unaware of excluded stores / items and the original groupings for the change/promotion. The ‘item’ in this case is the transaction level item, the SKU in IDS terminology.

There are several statuses that these changes may move through:
Worksheet, Submitted, Approved, Executed and Rejected
but these statuses are not published via the RIB.

Only ‘approved’ prices and promotions will be presented. Note: the changes will be presented well ahead of their effective date.

If the user wishes to amend a clearance or regular price or promotion after it has been approved, it has to be moved into worksheet status, amended and then submitted for approval again. This will result in the following:
A message create after the first approval
A message delete when the change is moved back to worksheet status
A message create when the change is re-approved

This is perhaps not critical for future dated changes. However, the design of the IDS load will have to consider how to handle apparent deletions of current clearance and promotion changes, which might be followed by a creation shortly afterwards.

 The same issue does not affect regular price changes in the same way, since they have no end date associated with them. To change a regular price (which is currently active), the user just has to create a new regular price change. It is possible to create more than one regular price change for the current day, so the IDS needs to be aware of the order these changes are presented.  

IT logic for identifying correct price

(a) Identify events which trigger a price change
Note: 
This is just an indication of the logic for applying the rules to the IDS, the technical design might approach this in a different way (e.g. by holding yesterday’s price and making a comparison to today’s price)
See appendix for the IDS tables which will be accessed  

First identify all the ‘SKU in Store’ which have a change in price.
 
Identify all clearance promotions with a start date of ‘tomorrow’ 
Select ClearanceID from ClearPriceChangeEvent where PriceChangeEffectiveDate=’tomorrow’
Select StoreID, SKUID from StoreSKU.ItemClearPriceChange for these ClearanceID’s

Identify all fixed price promotions with a start date of ‘tomorrow’ 
Select PromotionID, PromoComponentID,PromoComponentDetailID from PromoComponentDetail where StartDate=’tomorrow’ and .DetailTypeID=S (simple)
Select StoreID, SKUID from StoreSKU.ItemPromoCompDetail where PromoChangeType = 2 (fixed price) & PromotionID, PromoComponentID, PromoComponentDetailID = that of PromoComponentDetail

Identify all clearance prices  with a ‘reset date’ of  ‘tomorrow’ 
Select ClearanceID from ClearPriceChangeEvent where ResetDate=’tomorrow’
Select StoreID, SKUID from StoreSKU.ItemClearPriceChange for these ClearanceID’s

Identify all fixed price promotions which end ‘today’ 
Select PromotionID, PromoComponentID,PromoComponetDetailID from PromoComponentDetail where EndDate=’today’ and .DetailTypeID=S (simple)
Select StoreID, SKUID from StoreSKU.ItemPromoCompDetail where PromoChangeType = 2 (fixed price) & PromotionID, PromoComponentID, PromoComponentDetailID = that of PromoComponentDetail  

Identify  regular price changes with a start date of ‘tomorrow’ 
Select PriceChangeID from RegularPriceChangeEvent where PriceChangeEffectiveDate=’tomorrow’
Select StoreID, SKUID from StoreSKU.ItemRegPriceChange for these PriceChangeID’s


(b) Obtain the correct price for the SKU/Store

Obtain the current clearance price, promotion price and/or regular price for each Store/SKU which has been identified as having a price change tomorrow. It is possible that only the regular price will be found.

Identify  clearance price  for the SKU/Store 
Merge ClearPriceChangeEvent and StoreSKUItemClearPriceChange tables, and select  SellingUnitClearRetailPrice, PriceChangeResetDate where PriceChangeEffectiveDate <= tomorrow & SKUID / StoreID = those identified
Only select one for each StoreID / SKUID, by choosing the one with the PriceChangeEffectiveDate closest to tomorrow. 
Exclude  rows where the PriceChangeResetDate  is before tomorrow

Note there can be zero or one row returned which satisfies this condition for each StoreID/SKUID.

Identify  fixed price promotion for the SKU/Store 
Merge PromoComponentDetail and StoreSKUItemPromoComp Detail tables, and select  PromoChangeAmount where PromoComponentDetail.StartDate <= tomorrow, PromoComponentDetail.EndDate >=tomorrow, PromoChangeType=2, PromoDetailTypeId=S & SKUID / StoreID  = those identified

Note there can be zero or one row returned which satisfies this condition for each StoreID/SKIUID.

Identify the  regular prices for the SKU/Store 
Merge RegularPriceChangeEvent and StoreSKUItemRegPriceChange tables, and select StoreID, SKUID, SellingUnitRetailPrice where PriceChangeEffectiveDate <= tomorrow & SKUID / StoreID = those identified. 
Only select one for each Store / SKUID, by choosing the one with a PriceChangeEffectiveDate closest to tomorrow. It is possible to have several for the same day (as a result of emergency price changes) – but the PriceChangeEffectiveDate actually captures the date and time, so select the latest.  

If a regular price is not found, obtain the OriginalRegRetailPrice from the SKUItemInStore 
(Note: this attribute does not exist in the IDS currently but needs to be added – sourced from ITEM_LOC.UNIT_RETAIL (tbc))

Then identify the cheapest price by selecting the minimum of SellingUnitClearRetailPrice, PromoChangeAmount, SellingUnitRetailPrice (or OriginalRegRetailPrice if no SellingUnitRetailPrice was found)

Data Model Tables 















