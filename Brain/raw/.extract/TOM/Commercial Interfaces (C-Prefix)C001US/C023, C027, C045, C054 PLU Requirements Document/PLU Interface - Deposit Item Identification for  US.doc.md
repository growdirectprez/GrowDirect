
 EMBED Word.Picture.8





Integration Requirements
Deposit Item on the PLU Interface
for the US only























Author: Heather Rennoldson
Version: 0.1
Date: 21/03/2007 
Status: Draft

Table of Contents
 TOC \o "1-2" \h \z \t "Appendix,1"  HYPERLINK \l "_Toc162239206" 1.	Introduction	 PAGEREF _Toc162239206 \h 4
 HYPERLINK \l "_Toc162239207" 2.	Defining deposit items in ORMS	 PAGEREF _Toc162239207 \h 4
 HYPERLINK \L "_TOC162239208" 2.1	Item set-up	 PAGEREF _TOC162239208 \H 4
 HYPERLINK \L "_TOC162239209" 2.2	Reflection in the tables	 PAGEREF _TOC162239209 \H 5
 HYPERLINK \L "_TOC162239210" 2.3	Pricing	 PAGEREF _TOC162239210 \H 5
 HYPERLINK \l "_Toc162239211" 3.	Requirements for the PLU interface	 PAGEREF _Toc162239211 \h 6
 HYPERLINK \l "_Toc162239212" 4.	Derivation of the data from the IDS	 PAGEREF _Toc162239212 \h 7
 HYPERLINK \L "_TOC162239213" 4.1	Full product load	 PAGEREF _TOC162239213 \H 7
 HYPERLINK \L "_TOC162239214" 4.2	Overnight batch update	 PAGEREF _TOC162239214 \H 7
 HYPERLINK \L "_TOC162239215" 4.3	Missing barcodes	 PAGEREF _TOC162239215 \H 7
 HYPERLINK \L "_TOC162239216" 4.4	Emergency Price Changes	 PAGEREF _TOC162239216 \H 8
 HYPERLINK \l "_Toc162239217" 5.	Other Considerations	 PAGEREF _Toc162239217 \h 8
Document Control

Project:
Operating Model – Integration 
Document Title:
Deposit Item Identification  for the PLU Interface for the US only
Document Location:
Docshare : TOM Integration\1 Design


Distribution:
Operating Model Integration Team




Change Record

Date
Version
Change Description
Author
21/03/2007
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

This document is an addendum to the PLU Requirements for Storeline and supplies the business rules for identifying when a product is classed as a deposit item for a store for the US. 

A deposit item is a product that has a portion which is, normally, returnable to the supplier and is sold to the customer with a deposit taken for the returnable portion (e.g. bottle of beer and money returned to customer for returning the bottle).

Within the US:
some states (and therefore stores) will require a product to be classified as a deposit item, whereas other states will not require the same product to be classified as a deposit item. 
the bottle is not actually returned to the supplier but the customer is refunded for the empty bottle. Hence this solution for deposit items is US specific.

This document describes how this will be managed for the PLU Interface to Storeline for the US only.

Defining deposit items in ORMS
Item set-up
Deposit items are set up as two individual items in ORMS – contents & containers.
 
There are 3 fields that have been introduced into the ITEM_MASTER table to accommodate deposit items, and there is a UDA of Return Type Code which will be defined to link the contents to the code used for the container within Storeline.


DEPOSIT_ITEM_TYPE
E = Contents
A= Container
Z= Crate
T = Returned Item (empty bottle)
P = Complex pack (with deposit items), set for the pack only
CONTAINER_ITEM
Only populated if the DEPOSIT_ITEM_TYPE = E i.e. represents the Contents, then this will contain the ITEM of the container 
DEPOSIT_IN_PRICE_PER_UOM
This is used in ORMS to indicate if the price of the deposit should be included in the calculation for the price per UOM of the contents 
UDA for Return Type Code
Will be defined for the contents e.g. when DEPOSIT_ITEM_TYPE = E

It is not envisaged that Tesco will use DEPOSIT_IN_PRICE_PER_UOM. 

The contents will be set up with a level 3 item for the barcode which will be scanned at the till.

The container will be set up with a level 3 ‘price look-up’  number, and the same container may be linked to a variety of products, the key feature being that there will  have be as many containers as there are refundable deposit prices.

The contents will be set up as part of a  simple pack.
 
 The containers will not be set up as part of a pack.

It is assumed that the supplier for the contents will be set up as normal – but not sure about the supplier for the container. (This wouldn’t affect the PLU interface unduly anyway).

Reflection in the tables
This example shows how the container and contents would be set up in ORMS. 
. 

 SHAPE  \* MERGEFORMAT 
For GFO purposes, I assume the contents will be set up as ‘orderable’, and the container as ‘not orderable’. 


Pricing
Pricing is set up at SKU / Location level.

For locations which operate deposit items, both the contents and the container will be assigned prices. The customer will be charged for both (i.e. the price of the contents excludes the price of the container). 

For locations which do not operate with deposit items, we would expect a price for the contents, but would expect the price for the container to be zero.


Requirements for the PLU interface
The PLU interface will contain a row for the contents and a row for the container (both at barcode level).
The contents row will also hold the Return Type Code for the container, if the location handles deposit items.

Within RDD (Storeline parameter system), the Return Type Code is linked to the PLU number (barcode) of the container. This will be set up directly in RDD. There is no system link between RDD and ORMS to ensure that valid Return Type Codes and PLU code for the containers are set up. 

So for example:

(a)  For a store operating with deposit items we would expect to see:

PLU interface:

Barcode
Price
Return Type Code
Text for State Redemption Value
(used for SEL)
nnnnnnnnnn
$2.00
zz
+ CRV
mmmmmmmm
$0.30




RDD system:

Return Type Code
PLU code for the container
zz
mmmmmmmm

When the contents are scanned at the till, the PLU number for the linked contents is identified by doing a look-up of the Return Type Code (from the contents) against the RDD table. This will result in the till receipt showing a line for the sale of the contents followed by a line for the sale of the container, which is also flagged as being a returnable item.  

(For information: then from a sales perspective, a row for the sale of the contents and a row for the sale of the container will be captured) 

(b) For a store operating without deposit items we would expect to see:

PLU interface:

Barcode
Price
Return Type Code
Text for State Redemption Value
nnnnnnnnnn
$2.00


mmmmmmmm
$0.00




RDD system:

Return Type Code
PLU code for the container
zz
mmmmmmmm

When the contents are scanned at the till, there is no Return Type Code associated so no sale of the container will be generated.
Derivation of the data from the IDS
Note the approach for this will depend very much on the overall design for the PLU interface – the following is just an indication of the rules.
Full product load
When extracting the detail for the full product load for an individual store, the following process should be invoked:

If the SKU is a ‘contents’ product (DEPOSIT_ITEM_TYPE =E), then obtain the related container (CONTAINER_ITEM and the UDA Return Type Code).

Then to determine if the store operates with deposit items we could:
check if the container has a price for the store, by checking for the current regular price for the item / store or 
have a look-up table, within the Integration Layer,  of stores with a flag to indicate if they handle deposit items 

If, the store does not handle deposit items, then the ReturnTypeCode should be set to nulls on the interface.

If the store does handle deposit items, the ReturnTypeCode should be set as specified, but we also need to obtain the text for the State Redemption Value. It has been proposed that a table of States and text is maintained in the Integration Layer, and a look-up is made from the state for the store (as held in the store address in ORMS and the IDS) to this table to obtain the text.
It might however be simpler to maintain the table at store level. If this is done, the presence / absence of the text could also determine if the store operates deposit items – and then whether ReturnTypeCode should be populated. . 

Overnight batch update
Any of the following changes might affect the link between the contents and container items as provided for Storeline:
Create of a new SKU which is a contents product
Amend, Create, Delete of Return Type Code and / or the Deposit Item Type (to or from E) linked to a SKU
Change of price for a  container item for a location (from or to zero)

For (a) and (b) the process for identifying the data will follow that in 4.1
For (c), it will be very difficult to identify the contents products related to the container (short of a scan of the full item file). We could of course, assume that the zero price is set up correctly initially and will never change. 

If we chose to do implement a store look-up, rather than rely on the container having a zero price, we would probably be reliant on a store not changing its redemption rules…and having to run special processing if this occurs.
Missing barcodes
If a new barcode is added then checks will have to be made to see if the product is the contents of a deposit item, and the rules specified in 4.1 will have to be applied.

Emergency Price Changes
This interface will not be affected by the rules for deposit items. 

Other Considerations

The GFO interface will need to be amended to exclude the sales of container items.








	 Integration Team: Requirements Definition




PAGE  


Date:  REF Date  \* MERGEFORMAT 21/03/2007 , Version  REF Version  \* MERGEFORMAT 0.		Page  PAGE 5 of  NUMPAGES 8
Author : Heather Rennoldson


	
Integration Team : Requirements Definition







Date: 21/03/2007, Version 0.1		Page  PAGE 2 of  NUMPAGES 8
Author : Heather Rennoldson




















ITEM = nnnnnnnnnnnnn
		  

ITEM_MASTER for barcode


ITEM_MASTER for barcode





ITEM = mmmmmmmmmmm

ITEM_MASTER for SKU






















ITEM = 234567890
DEPOSIT_ITEM_TYPE = E
CONTAINER_ITEM=345678901
UDA (for Return Code)=20			  

PACKITEM

PACK_NO= 123456789
ITEM=234567890
PACK_QTY=12 




ITEM_MASTER for SKU



ITEM = 345678901
DEPOSIT_ITEM_TYPE =A 











 EMBED Word.Picture.8  







