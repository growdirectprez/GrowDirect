
 EMBED Word.Picture.8





Integration Requirements
Price Extract Rules for the PLU Interface























Author: Heather Rennoldson
Version: 0.1
Date: 02/03/2007 
Status: Draft

Table of Contents
 TOC \o "1-2" \h \z \t "Appendix,1"  HYPERLINK \l "_Toc160620072" 1.	Introduction	 PAGEREF _Toc160620072 \h 4
 HYPERLINK \l "_Toc160620073" 2.	Scope	 PAGEREF _Toc160620073 \h 4
 HYPERLINK \l "_Toc160620074" 3.	Issues/Assumptions	 PAGEREF _Toc160620074 \h 4
 HYPERLINK \l "_Toc160620075" 4.	Business Rules	 PAGEREF _Toc160620075 \h 4
 HYPERLINK \L "_TOC160620076" 4.1	Overview	 PAGEREF _TOC160620076 \H 4
 HYPERLINK \L "_TOC160620077" 4.2	Scenarios for price changes	 PAGEREF _TOC160620077 \H 6
 HYPERLINK \l "_Toc160620078" 5.	PLU Overnight batch	 PAGEREF _Toc160620078 \h 10
 HYPERLINK \L "_TOC160620079" 5.1	Price changes	 PAGEREF _TOC160620079 \H 10
 HYPERLINK \L "_TOC160620080" 5.2	New products	 PAGEREF _TOC160620080 \H 10
 HYPERLINK \l "_Toc160620081" 6.	Emergency Price Changes	 PAGEREF _Toc160620081 \h 10
 HYPERLINK \L "_TOC160620082" 6.1	Business rules	 PAGEREF _TOC160620082 \H 10
 HYPERLINK \L "_TOC160620083" 6.2	Technical considerations	 PAGEREF _TOC160620083 \H 10
 HYPERLINK \L "_TOC160620084" 6.3	Assumptions	 PAGEREF _TOC160620084 \H 11
 HYPERLINK \l "_Toc160620085" 7.	PLU Full Refresh	 PAGEREF _Toc160620085 \h 12
 HYPERLINK \l "_Toc160620086" 8.	Missing Barcodes	 PAGEREF _Toc160620086 \h 12
Document Control

Project:
Operating Model – Integration 
Document Title:
Price Extract Rules for the PLU Interface
Document Location:
Docshare : TOM Integration\1 Design


Distribution:
Operating Model Integration Team
Operating Model BSAs for Price & Promotions, Storeline .



Change Record

Date
Version
Change Description
Author
02/03/2007
0.1
Initial Draft
Heather Rennoldson

References

Document
Version
Date
Author
Integration Requirements PLU Feeds to storeline 


Heather Rennoldson
Introduction

This document is an addendum to the PLU Requirements for Storeline and supplies the business rules for identifying the prices which have to be extracted from the Integration Data Store and interfaced via the PLU file to Storeline.

 There are several different flavours of the PLU interfaces. This document captures the pricing requirements for each flavour:
Overnight batch feed – which includes changes to products and prices
Missing barcodes – capturing all details for a specific Articles
Full refresh file – all products and prices
Emergency price changes – capturing Article identifier and price only

Scope

In Scope:
Clearance, Retail and Simple Promotions –fixed price maintained in ORPM

Out of Scope:
Pricing maintained in ORMS10 – the PLU feed is based on POS_MODS 
Other types of promotion maintained in ORPM – these will be handled via the Storeline promotions interface.
Multi pricing   (i.e. Storeline functionality to sell 3 products for $1, as set up via the PLU interface)
Capture of other product attributes, including sales tax – the former is included in the Integration requirements PLU Feeds to Storeline, and the requirements for the latter are yet to be worked.

Issues/Assumptions

It is assumed that there will be a mechanism in place within ORPM for defaulting a regular price for an item/location  for an item not ranged in that location, but as far as the Integration Layer is concerned, these will not be distinguishable from other prices.

The clearance reset date is not currently included in the Clearance RIB message. This interface is dependent upon the RIB message being amended to capture this.  

Business Rules
Overview 

Within ORPM12, retail prices can be set in a number of ways:
Regular pricing
Clearance pricing
Pricing within Simple ‘fixed price’ promotions 

ORPM prevents an item being on both promotion and clearance at the same time.

A regular price will always exist, but an item can also be on clearance or  part of a ‘fixed price’ promotion. If there is more than one price for a particular date the cheapest price has to be used (except in the case of Emergency price Changes). Normally one would expect the clearance or promotional price to override the regular price. 

Pricing is maintained at the transaction level of the item (SKU) and has to be exploded to Article (barcode) level for interfacing to Storeline.

Although ORPM allows a date and time stamp for any of the start and end dates, apart from Emergency Price Changes, it is only the date element that will be reflected in the interface to Storeline. 

The processing within any of the PLU interfaces will have to identify the ‘correct’ price for a product. 






Scenarios for price changes 
(Purely hypothetical examples)
 Regular Price Change (for one product in one store)
The user sets up a regular price of £2.00 to start on 10/2, and then changes the price to £1.50 from 24/2.

 SHAPE  \* MERGEFORMAT 
Thus the intention is to show the following prices in store:


Start date
End date
Price In Store
10/2
23/2
£2.00
24/2
Open ended
£1.50
Promotional Price Change (for Simple, Fixed price promotions) 

If a promotional price of £1.00 is also applied with a start date of 17/2 and an end date of 21/2, this will override the regular price for that period:

 SHAPE  \* MERGEFORMAT 

Thus the intention is to show the following prices in store:

Start date
End date
Price In Store
Type of price
10/2
16/2
£2.00
Regular
17/2
21/2
£1.00
Promotion
22/2
23/2
£2.00
Regular
24/2
Open ended
£1.50
Regular

Clearance Price Change

Clearance prices operate in a similar way to promotion price changes but, unlike promotional changes, these are not given an end date, but may be given a ‘reset date’ i.e. the date at which the regular price will start.  So we could add a clearance price change which runs from 24/2 with a reset date of 3/3.

 SHAPE  \* MERGEFORMAT 
Start date
End date
Price In Store
Type of price
10/2
16/2
£2.00
Regular
17/2
21/2
£1.00
Promotion
22/2
23/2
£2.00
Regular
24/2
2/3
£0.75
Clearance
3/3
Open ended
£1.50
Regular


If in the above example the clearance had been broken down into two stages, we could have a clearance price starting on 24/2 of 0.75, and another clearance starting on 28/2 of 0.50 but no reset date. So this would result:

  SHAPE  \* MERGEFORMAT 

Start date
End date
Price In Store
Type of price
10/2
16/2
£2.00
Regular
17/2
21/2
£1.00
Promotion
22/2
23/2
£2.00
Regular
24/2
27/2
£0.75
Clearance
28/2
Open ended
£0.50
Clearance

Promotional Price higher than regular price 

If the user had:
set up a regular price of £2.00 from 10/2 
then introduced a promotional price of £1.75 from 21/2 t0 25/2
then set up a new regular price starting on 24/2 of £1.50 (lower than the promotional price):

 SHAPE  \* MERGEFORMAT 
Start date
End date
Price In Store
Type of price
10/2
16/2
£2.00
Regular
17/2
23/2
£1.75
Promotion
24/2
Open ended
£1.50
Regular




PLU Overnight batch
The overnight batch process has to capture a price for a product under two scenarios :
(a) where there has been a price change for a Store/SKU
(b) where a Store/SKU relationship has been created for the first time today

In both cases the data  needs to be merged with other changes made to the SKU during the day and exploded from SKU to Article (barcode) level to create the full PLU interface.

When referring to ‘today’ and ‘tomorrow’ through the body of this document, it is assumed that control dates will be used.

 Price changes
.For an item (SKU) in store this can be recognised by checking for the following events:
If it is on a clearance price change starting on the following day
If it is on a fixed price promotion starting on the following day
If it is on a fixed price promotion which ends today (so will revert to regular price tomorrow)
If it is on a clearance price change with a ‘reset date’ of tomorrow (so will  revert to regular price tomorrow)
If there is a regular price change which starts tomorrow 

If any of these events are identified then it is necessary to extract all the prices (promotion, clearance, regular)  that apply tomorrow for that SKU/Store and select the cheapest.

  
New products
The products will be identified from all new SKU / Store entries created today and the price for these products will be the obtained as above, by selecting all the prices that apply tomorrow and selecting the cheapest. 
     
Emergency Price Changes
Business rules
These will be identified when a superuser sets up a regular price change today with a start date of ‘today’ for a SKU/Store. This price will override any clearance or fixed price promotional price (even if those are lower) and be included in the next Emergency Price Change PLU interface to Storeline.

Note the superuser can set up many Emergency Price Changes for the same SKU/Store via this mechanism, so the integration process will have to be mindful of the order in which these are captured, and ensure that only the latest is included in the interface.

Technical considerations
These will be identified from the RIB message by checking for a ‘create’ of the RegPrcChgDtl message where the effective date within that message = ‘today’.

Having identified this event, it is necessary to capture the location Store, SKU and retail price being passed on the message and include this information in the Storeline interface.
Assumptions
It is assumed that the users cannot cancel a promotion or clearance that is currently active. If they wish to ‘cancel’ a promotion, they will set the end date to today, or for a clearance, set a reset date of tomorrow. These changes would then be picked up in the normal PLU overnight batch. 

PLU Full Refresh
This will have to be provided by extracting all ‘item in store’ records and obtaining a price following the same rules as in 5.2  for the required date for each of these.

Missing Barcodes
New barcodes will be identified from the Item RIB message, where when there is a ‘Create’ for a item_level = 3. The integration processing will then have to identify if its parent SKU has been created prior to ‘today’. If so, then the barcode is a missing barcode and needs to be interfaced to store, with all the relevant attributes as described in the  PLU Interface requirements document..

To obtain the correct price for the missing barcode, apply similar rules to those in 5.2 for prices in effect today & taking account of emergency price changes. 








	 Integration Team: Requirements Definition




PAGE  


Date:  REF Date  \* MERGEFORMAT 02/03/2007 , Version  REF Version  \* MERGEFORMAT 0.1		Page  PAGE 3 of  NUMPAGES 12
Author : Heather Rennoldson


	
Integration Team : Requirements Definition







Date: 02/03/2007, Version 0.1		Page  PAGE 2 of  NUMPAGES 12
Author : Heather Rennoldson





10/2



10/2



10/3




£2.00



Date

Regular
Price

£1.50



23/2 24/2



10/3



Regular Price 

£1.50



Date


£2.00



23/2 24/2



21/2



£0.50



Promotion
Price


Promotion
Price


17/2



£1.00



£1.00



£1.50



£2.00



21/2



£2.00



21/2



17/2



23/2 24/2



Date

10/3



10/2



Regular Price 

17/2



23/2 24/2



Date

10/3



10/2



£0.75



2/3



Clearance Price 

£175



Promotion
Price

£1.00



£1.50




£2.00



21/2



17/2




23/2 24/2



10/2



Date

10/3



£0.75



2/3



Promotion
Price

Clearance Price 

£1.50





 EMBED Word.Picture.8  







