
 EMBED Word.Picture.8





Integration Requirements
PLU Feeds to Storeline 























Author: Heather Rennoldson
Version: 0.3
Date: 25/01/2007 
Status: Draft

Table of Contents
 TOC \o "1-2" \h \z \t "Appendix,1"  HYPERLINK \l "_Toc157327887" 1.	Introduction	 PAGEREF _Toc157327887 \h 4
 HYPERLINK \L "_TOC157327888" 1.1	Background	 PAGEREF _TOC157327888 \H 4
 HYPERLINK \L "_TOC157327889" 1.2	Scope	 PAGEREF _TOC157327889 \H 4
 HYPERLINK \l "_Toc157327890" 2.	Requirements for the Overnight Update	 PAGEREF _Toc157327890 \h 5
 HYPERLINK \L "_TOC157327891" 2.1	Overview	 PAGEREF _TOC157327891 \H 5
 HYPERLINK \L "_TOC157327892" 2.2	Price Changes	 PAGEREF _TOC157327892 \H 7
 HYPERLINK \l "_Toc157327893" 3.	Full item load (for new store openings)	 PAGEREF _Toc157327893 \h 8
 HYPERLINK \l "_Toc157327894" 4.	Emergency Price Changes	 PAGEREF _Toc157327894 \h 8
 HYPERLINK \L "_TOC157327895" 4.1	Requirements	 PAGEREF _TOC157327895 \H 8
 HYPERLINK \l "_Toc157327896" 5.	Not on File (Missing barcodes)	 PAGEREF _Toc157327896 \h 8
 HYPERLINK \L "_TOC157327897" 5.1	Overview	 PAGEREF _TOC157327897 \H 8
 HYPERLINK \l "_Toc157327900" 6.	Technical Considerations	 PAGEREF _Toc157327900 \h 9
 HYPERLINK \l "_Toc157327901" 7.	Data Issues	 PAGEREF _Toc157327901 \h 10
 HYPERLINK \L "_TOC157327902" 7.1	Overview	 PAGEREF _TOC157327902 \H 10
 HYPERLINK \L "_TOC157327903" 7.2	Attributes which need a source	 PAGEREF _TOC157327903 \H 10
 HYPERLINK \L "_TOC157327904" 7.3	Attributes in ORMS/ORPM which do not appear to be captured in RIB messages	 PAGEREF _TOC157327904 \H 11
 HYPERLINK \L "_TOC157327905" 7.4	Attributes which will be provided from S,R & D – but no details known yet	 PAGEREF _TOC157327905 \H 12
 HYPERLINK \L "_TOC157327906" 7.5	Attributes not available for Turkey	 PAGEREF _TOC157327906 \H 13
 HYPERLINK \l "_Toc157327907" Appendix A	PLU File Mappings	 PAGEREF _Toc157327907 \h 14
 HYPERLINK \l "_Toc157327908" Appendix B	Glossary of Terms	 PAGEREF _Toc157327908 \h 35
Document Control

Project:
Operating Model – Integration 
Document Title:
Requirements Definition
Document Location:
team workroom


Distribution:
Operating Model Integration Team
Operating Model BSAs for Storeline.



Change Record

Date
Version
Change Description
Author
04/12/2006
0.1
Initial Draft
Heather Rennoldson
02/01/2007
0.2
Updated following feedback from Storeline and Integration team reps

 REF Date  \* MERGEFORMAT 25/01/2007 
 REF Version  \* MERGEFORMAT 0.3
Updated to cater for Storeline enhancements and as a result of further feedback from Retail BSAs
Heather Rennoldson

References

Document
Version
Date
Author
BRD for pending product and price changes 

02/2006
Gary McLellan
KDD for Group Best Practice – Shelf Edge Label


Ben Malcolm
BRD for SEL production

11/2006
Ben Malcolm
PLU and General Batch Files –Technical Reference 
4.8


FSD9303 SEL Content Enhancements
4.0
8/12/2006
Isaac Menashe
CR1557 – Processing catchweight products
0/c
6/12/2006
Mick Brookes
Introduction
Background

The purpose of this document is to:
confirm the integration requirements for the various Storeline Product & Price (PLU) feeds 
highlight any gaps / issues that need resolution

The information is based on:
the requirements specified in the Business Requirements document for Shelf Edge Label production
the Storeline PLU and General Batch Files Technical Reference
changes planned for Storeline described in CR1557 – Processing Catchweight Products and FSD9303 SEL Content Enhancements
discussions with Storeline experts and other members of the Operating Model team 

There are several different ‘flavours’ of the PLU interface which will be used to satisfy a number of business scenarios:

Overnight update for product details including price 
Full item load (e.g. for new store openings)
Emergency Price Changes
Not on file

The PLU update contains a row for each barcode, with attributes required for Storeline e.g. pricing, Shelf Edge Label (SEL), store ordering. Most of the attributes specified on the PLU feed at barcode level will be held at SKU level in the Integration Data Store (IDS).

Issues are identified in the relevant section of the document.

This document covers the interfaces for the US:
C023 Item POS Attributes
C027 Missing Barcodes
C045 Emergency Price Changes

And also covers requirements to amend the C054 Item POS Attributes for the US.
Scope

The following element is still being worked on so have been excluded from this document: 
Space, Rand & Display attributes. Although they have been defined as a requirement for the PLU interface in FSD9303 and are shown in the Appendix, no mapping can be provided as yet since the details of what they will publish to the Integration Layer are not available yet.

The following element is outside the scope of this document:
Sales tax  for the US – this will be provided as a separate feed  direct from Taxware to the store



Requirements for the Overnight Update
Overview
Country and Group requirements 
Turkey, Japan and China
The current PLU overnight update for Turkey, Japan and China is broken down into 3 batches:

Price increases
Price Decreases
Other changes

This enables the store to schedule the daily replacement of Shelf Edge Labels (SELs) so that the more critical are carried out first.
This feed is derived from the ORMS10 POS_MODS interface. In the medium term, an amendment will be made to this interface to add the attributes required for SELs which will be sourced from Space, Range & Display. In the longer term, it will be replaced by the Group solution when ORMS12 is installed.    
 
US 
The PLU interface for the US will only be provided in one batch, since there are a relatively small number of products and so fewer SELs to replace.

This feed will be derived from the data captured in the Integration Data Store, which has been updated via ORMS12 & ORPM12 RIB Messages.

Group
The Group requirement is to have the flexibility to break down the PLU feed into several batches to fit in with in-store SEL procedures e.g. only make description changes for SELs one day a week. The proposal is to break the changes into the following batches:

Price increases
Priority miscellaneous changes which affect legal requirements for SEL
Price Decreases
Non-priority miscellaneous changes which affect the SEL
Changes that do not require a change in SEL (e.g. products not stocked at the store)

It is intended that a change will be made to Storeline so that it will accept one PLU feed from the centre, and will split it down into the appropriate batches. 
This change has not yet been designed or scheduled.

Upgrade of ORMS10 to ORMS12
When Turkey, Japan or China are upgraded from ORMS10 to ORMS12, they will, as a minimum, require that the PLU overnight feed is supplied, as currently, in three batches. So, if the Storeline change has not been implemented, processing within the Integration Layer will have to be amended to provide the three batches.



Only fields that have been changed need to be populated in this interface. Note that in the US & Group solution, integration processing will identify that there has been a change to a product which affects the Storeline interface, but this will be flagged at row (a subset of the Storeline fields) level. As a result products presented on the interface will have changed in some way, but for a product, it will not be possible to identify from the interface itself, precisely what has changed.  
Storeline only expects to receive central product and price changes the night before they are due to become active in store.
Storeline has the functionality to take a promotional price change and then revert to the normal price at the end of the promotion. However, this does not cater for the scenarios where the promotion end date is amended, or where there is a change to regular price during the promotion. This functionality will therefore not be used. Any promotional price changes will have to be presented as a normal price change to Storeline.
In addition IOD Store Operations have requested that a report is produced indicating number of SEL changes by category for a store over the next n days (where n is a flexible number).
 The detail of this can be found in the BRD for SEL production.
(a) Miscellaneous changes are not dated at the centre, but it is assumed that when the Storeline change to split the PLU file into batches is developed, this will incorporate the reporting of the miscellaneous changes. 
(b) Future price changes, Storeline does not have any visibility of future price changes, so this will have to be provided from the Operational Reporting Stream. 

Note: the original requirement was to identify the start and end of offer promotions from the PLU interface. However, this information is not captured within the PLU interface. It is captured in the Storeline Member Promotion Feed, so the requirement to produce a new SEL under these circumstances will be driven directly from Storeline processing of the latter feed. 


Price Changes
Background
ORMS 10 & ORPM12 can hold several different prices for the same SKU (in the same store) concurrently:
Regular price
Clearance price promotion
Simple promotion – fixed price

A regular price for a current or future date should always exist. Logically, it should not be possible to have a clearance price and a simple fixed price promotion overlapping.

Storeline only holds one price for a barcode from the centre.

Note that the other promotion types are handled via the Storeline Member Promotion interface – not the PLU interface.

ORMS10, as used in Turkey, Japan and China

As mentioned before, the PLU feed is provided from the ORMS10 POS_MODS feed and ORMS determines which price to use. In addition there is an ORMS function which prevents clearance and promotions overlapping for the same product.
ORPM12, as proposed for US
The Integration Layer has to identify if there is a change between today’s and tomorrow’s price and present any changes to Storeline in the end of day batch process. If a clearance or simple fixed price promotion is in operation this price will override the regular price. 

It is understood that there will be a process in ORPM12 to ensure that a clearance price and simple promotion cannot overlap.
Feature of  Storeline Drop 2
Note: The business intends to set the ‘Simple promotions – amount-off ‘as Storeline Enhanced Promotions with a  threshold and step of 1. These are currently not supported in Turkey. This will be driven through the Member Promotion File.
For Turkey this will require an amendment to the POS_MODS interface from ORMS10, which then feeds into the Storeline Member Promotion interface.
For the US and Group the Member Promotion Interface will be built from the IDS, so this will be captured with other requirements for that interface. 

Issues
Need to confirm the rules for selecting the price when there is a clearance or simple fixed price promotion. E.g. what happens if the regular price is lower than the promotion price?

 
Full item load (for new store openings)
This process needs to run on an ad-hoc basis, for new store openings, store refits etc.   The file will contain all items and their details (including price).
 
Emergency Price Changes
Requirements
Any price change for today made since the last overnight extract to store will have to be provided in this interface. For Turkey, under ORMS10, these are identified via the POS_MODS interface. For the US, these will be identified from the RIB messages by checking for effective dates of ‘today’ for any creation, deletion or update of regular, clearance and simple promotion – fixed prices.
Having identified that there has been change, the same logic as for ‘Price Changes’ needs to be applied to select the correct price. This might not result in an actual change e.g. in the case when a clearance price is in existence, but there has been a change to the regular price with an effective date of today. To this end it might be appropriate to retain the current price in the IDS for direct comparison.
The detail record on this interface need only contain the barcode and the price. 
The Emergency Price Change interface will be scheduled to run hourly, but will only be created if there is data to transmit to store.

Not on File (Missing barcodes)

Overview
A ‘missing barcode’ is recognised by the barcode not being recognised at the till because it is not on the PLU file. There is a requirement to interface these missing details to stores in a timely way (e.g. half-hourly)
For Turkey these are identified when a new barcode is added to an existing SKU, and can be identified by a particular record type on the POS_MODS interface.
For US, a similar process will have to be created by using a combination of the RIB messages and data on the IDS.
Issues
This process cannot distinguish between those barcodes added as a result of ‘not on file’ or those added to a SKU in a timely way. 


Technical Considerations 

The design of the PLU interface must take account of the following issues:
Different stores will be on different version of Storeline. The integration code will have to handle the management of this.
The PLU feed has to be received in time for each store’s ‘end of day’s’ processing. Consideration has to be given as to how this will be managed for stores operating in different time zones. 
The full item load interface should be built so that it can be broken down into batches, to limit the amount of data being transmitted in one hit.

Data Issues
Overview
Appendix A show all the fields that can be included in the PLU interface as specified in the Technical Reference Version 4.8, and the additional attributes which have been added as a result of FSD9303 SEL Content Enhancements and CR 1557 due to be implemented in Storeline release Drop 1.. 
Many of the fields on the interface are not used by Tesco in any of its instances. These are indicated in the ‘Used by Tesco’ column with an ‘N’.
Where attributes are known to be used, and understood to be a requirement for Group, this column is left blank.
Where attributes are known to be required for a local instance, this column is set to ‘L’.
Where it is unknown whether an attribute is required or not, the column is set to ‘?’.

The Integration Data Store will be designed to hold Group and all Local attributes. The interfaces to/from the IDS will be customised to handle the local specifics. At present only the local attributes required for Turkey and the US have been captured in the IDS.

Note: 
(1) need to understand ho we flag GNFR (consumables). Do we use the MD_FG. Is the ORMS equivalent ITEM_MASTER.MERCHANDISE_IND?
(2) Some fields will not be available e.g. if a product has only just been approved, there might not be any information form Space, Range & Display available e.g. label size, and so will not be populated

As a result of analysing the data there are 4 categories of queries which need resolution:
Attributes which are required for Storeline but not yet identified the source of the data
Attributes which are required for Storeline, on ORMS/ORPM, which do not appear to be captured in a RIB message.
Attributes which will come from Space, Range & Display but as yet  we do not have the detail of the interface  


Attributes which need a source

At the time of writing, I am unsure where this data should be sourced from in ORMS


Col. 
Name
Description
Used within Tesco?
N – No
L – Local
Space - Yes 
Comment
60
RTN_CD
Return type code
 
This is used for linked items (e.g. deposit items, return code is linked in Storeline to the linked ‘EAN’)

Used for TV licences for Turkey and set as a UDA

Will be used for deposit items in the US – but will vary with the store location – awaiting confirmation for the source for US
87
OLD_PRC
Old price

It has been agreed that the business will provide this – but have not yet got a source
135
LBL_UOM
Label UOM (Description of the Unit Price Measure)
 
This is the text that has to go on the label e.g. ‘per 100 grams’
148
PRDCT_GRDING
Product Grading




Shelf talker indicator

This will come from marketing – but no source identified yet


Old price indicator




Text for State Redemption Value to be charged




Product texture




Product specification




Attributes in ORMS/ORPM which do not appear to be captured in RIB messages

Note: Nuno is aware of these – and the assumption is that these willl be populated on the RIB message


Col. 
Name
Description
Comment
ORMS / ORPM source
17
QTY_RQRD_FG
Quantity Required flag
This has been used for CE; not required for US 
It is used where customers take a bottle of water from a 6-pack. The EAN of the bottle is scanned and the quantity entered. So, if they take the whole 6-pack, a quantity of 6 has to be entered.
ITEM_LOC_TRAITS.QTY_KEY_OPTIONS
21
FOOD_STAMP_ FG
Payment by food stamps flag
Some customers can pay for certain products by food stamps. This flag identifies the products that fall into this category.
ITEM_LOC_TRAITS.FOOD_STAMP_IND
20
SLS_AUTH_FG
Prohibit Sales flag
This has been used for Emergency Product Withdrawals but has been superseded by using POS Message Numbers in the UK.
Has been captured in Turkey but …..
Business have decided that EPWs will be dealt with by manual instructions.
ITEM_LOC_TRAITS.STOP_SALE_IND
131
BS_UOM_ID
Basic UOM (Unit of Measure)
This is selling UOM e.g. kg
ITEM_LOC.UOM_OF_PRICE for the SKU 
132
BS_UOM_AMT
Basic UOM Amount (Full weight/volume of item – selling weight)
The content amount for the selling UOM
ITEM_LOC.MEAS_OF_EACH for the SKU l2 item
133
CMPR_UOM_ID
Comparative UOM (Empty in S/D interface)
This is used for showing the unit price on the SEL
ITEM_LOC.UOM_OF_PRICE for the SKU 
Does this assume comparison is in same dimensions as basis i.e. we can’t have grams and kg?
134
CMPR_UOM_AMT
Comparative UOM amount
(Weight/Volume/Length that the unit price is calculated against)
This is used for showing the unit price on the SEL e.g. might want to show unit price as price ‘per 100grams’
ITEM_LOC.MEAS_OF_PRICE for the SKU l2 item
24&30
RTL_PRC & CNTR_PRC
Retail Price
This is required to derive the correct price. 
RPM_CLEARANCE.RESET_DATE

Attributes which will be provided from S,R & D – but no details known yet

Col. 
Name
Description
Used within Tesco?
N – No
L – Local
Space - Yes 
Comment
147
DSCNT_LINE
Product status




Multi-location indicator




Shelf facing




Product range




Planogram



Attributes not available for Turkey
Col. 
Name
Description
Used within Tesco?
N – No
L – Local
Space - Yes 
Comment
143
INVENT_FG
Inventory Flag

Should be derived from ITEM_MASTER.INVENTORY_FLAG – but this is only available in ORMS12. Turkey currently use the ITEM_LOC record to determine this


CatchweightIndicator

Will be derived from ITEM_MASTER.SALE_TYPE but this will only be available in ORMS12

 PLU File Mappings

Col. NameDescriptionTypeUsed within Tesco?
N – No
L – Local
Space - Yes SizeTermsCommentORMS / ORPM sourceSpace,Range and Display source – for Turkey and US and GroupIDS source for US and GroupTurkey specific notes1PLU_BTCH_NBRPLU Batch numberNumeric  6NOT NULL   2Record OpCode to be performed when the batch is executed for each item:
0  Ignore record 
1  Add New item  
2  Update 
3  Price – Price update
4  Delete 
5  Sale – Batch that includes items on promotion, and specifies the reduced price for a limited time. When the batch runs, it creates a counter batch that will run when the sale ends
6  New/Update – Adds or updates an item.  If a new item exists in the database, it will be updated.  If the item does not exist, it will insert a new item
Numeric1NOT NULLOpcode will always be set to 6 for ‘new/update’  regardless of the type of interface.
Will be set to 4 for ‘delete’3ITM_IDPLU Item NumberNumeric 14NOT NULLKey field – mandatory ITEM_MASTER.ITEM for the level 3 barcodeArticleItem.ArticleID4STR_HIER_IDDepartment NumberNumeric  4NOT NULLThis is used for to identify departments for Clubcard promotions, and those excluded from Clubcard. Also, to identify if these products are managed by concessions. ITEM_MASTER.DEPT for the SKUSKUItem.Section of the parent SKU5DFLT_RTN_LOC_ IDDefault return location IDNumeric N4NULL   6MSG_CDLinked Message number Numeric N2NULLThis has been superseded by POS_MSG_NO  7DSPL_DESCRItem DescriptionChar 40NULLSEL descriptionITEM_MASTER.ITEM_DESC  for the SKUSKUItem.ItemDesc of the parent SKU8SLS_RESTRICT_GRPRestriction layout numberNumeric N2NULL   9RCPT_DESCRPOS Item DescriptionChar 20NULLTill Roll descriptionITEM_MASTER.SHORT_DESC for the SKU SKUItem.ItemDescShort of the parent SKU10TAXABILITY_CDTaxability CodeNumeric N4NULL   11MDSE_XREF_IDMerchandise cross reference IDNumeric N4NULL   12NON_MDSE_ IDNone Merchandise FlagNumeric N1NULL,1,0   13UOMUnit of measureChar 4NULLThis is the Stock UOM
Will need conversion from ORMS to Storeline formatITEM_MASTER.STANDARD_UOM for the SKUSKUItem.StandardUOM of the SKU14UNT_QTYUnit QuantityNumeric  2NULLThis is used for multi –selling units, used mainly in US, where selling price is set up as ‘3 for 1$’ – and rules to split price across 3 products are held in  RDD - so might be 1st product = 33c, 2nd=33c, 3rd=34c. Not required for day 1, but likely to come into scope later.
If there are no multi-selling units for this product this will be set to 1.TICKET_REQUEST.MULTI_UNITSSKUItem.TicketTypeID15LIN_ITM_CDLine Item codeNumeric N4NULL   16MD_FGMerchandise flagNumeric N1NULLAlthough identified as ‘not used’ it has been captured in Turkey  17QTY_RQRD_FGQuantity Required flagNumeric L1NULL,1,0This has been used for CE; not required for US 
It is used where customers take a bottle of water from a 6-pack. The EAN of the bottle is scanned and the quantity entered. So, if they take the whole 6-pack, a quantity of 6 has to be entered.ITEM_LOC_TRAITS.QTY_KEY_OPTIONS.18SUBPRD_CNTSub product countNumeric N4NULL   19QTY_ALLOWED_ FGQuantity allowed flagNumeric N1NULL,1,0   20SLS_AUTH_FGProhibit Sales flagNumeric  L1NULL,1,0This has been used for Emergency Product Withdrawals but has been superseded by using POS Message Numbers in the UK.
Has been captured in Turkey but …..
Business have decided that EPWs will be dealt with by manual instructions.ITEM_LOC_TRAITS.STOP_SALE_IND 21FOOD_STAMP_ FGPayment by food stamps flagNumeric  L1NULL,1,0Some customers can pay for certain products by food stamps. This flag identifies the products that fall into this category.
Used in USITEM_LOC_TRAITS.FOOD_STAMP_INDSKUItemInStore.FoodStampInd
22WIC_FGWomen Infant Children flagNumeric N1NULL,1,0  23PERPET_INV_ FGPerpetual invoice flagNumeric N1NULL,1,0   24RTL_PRCItem PriceMoney  13NULLAssumes this value is in cents for US, pence for UK This will need to be derived in the IL to understand when a promotional price takes precedence over the regular price and when we revert to the regular price at end of a promotion. Will have to be derived for Group from Store_Item_Regular_Price_Change.Selling_Unit_Price or equivalent fields for clearance and promotion prices.
Will not be provided for consumable items.25UNT_CSTUnit costMoney N13NULLNot used at present but might get switched on.

Will not be captured.  26MAN_PRC_LVLManual price levelNumeric N2NULL   27MIN_MDSE_AMTMin Merchandise amountMoney N13NULL   28RTL_PRC_DATERetail price dateDate Time N NULL   29SERIALIZED_ MDSE_ FGSerialized merchandise flagNumeric N1NULL,1,0   30CNTR_PRCCenter priceMoney 13NULLWill be populated as for retail price  for all instances apart from Thailand(Note retail price field can be amended in store – centre price can’t)
For Thailand this field is used for the Government price where VAT is calculated on that price – not the retail price  31MAX_MDSE_AMTMaximum merchandise amountMoney N13NULL   32CNTR_PRC_ DATECenter price dateDate Time NSizeNULL   33NG_ENTRY_FGNegative Entry flagNumeric L1NULL,1,0Used in CE for bottle returns. 
Assume not required for Group.  34STR_CPN_FGStore coupon flagNumeric N1NULL,1,0Storeline functionality allows products to be set up  as coupons (so that coupon can be treated as a discount rather than a tender).
Not being used for Group  35VEN_CPN_FGVendor coupon flagNumeric N1NULL,1,0Supported by Storeline but not used by Tesco  36MAN_PRC_FGManual price flagNumeric L1NULL,1,0Used in Turkey – held as a UDA in ORMS. Also used in China & Japan. UDASKUItem.ManualPriceEntryInd37WGT_ITM_FGWeighted item flagNumeric  1NULL,1,0This is used to identify if item should be weighed. ‘sell by weight’ line.ITEM_MASTER.CATCHWEIGHT_IND but ITEM_MASTER for the SKUSKUItem.CatchWeightInd for the parent SKU38NON_DISC_FGNone discount flagNumeric N1NULL,1,0   39COST_PLUS_FGCost plus flagNumeric N1NULL,1,0   40PRC_VRFY_FGPrice verify flagNumeric N1NULL,1,0   41PRC_OVRD_FGPrice override flagNumeric N1NULL,1,0   42SPLR_PROM_FGSupplier promotion flagNumeric N1NULL,1,0   43SAVE_DISC_FGSave discount flagNumeric N1NULL,1,0   44ITM_ONSALE_FGItem on sale flagNumeric N1NULL,1,0   45INHBT_QTY_FGProhibit Quantity flagNumeric N1NULL,1,0This flag would be used to prevent operator entering a quantity.  46DCML_QTY_FGDecimal Quantity flagNumeric L1NULL,1,0This is used in CE to allow operator to enter quantity with a decimal point – used specifically for selling cloth..  47SHELF_LBL_ RQRD_ FGShelf label req. flagNumeric N1NULL,1,0   48TAX_RATE1_FGTax Rate 1 flagNumeric L1NULL,1,0There will be separate proposal for sales tax – will vary by country because Turkey holds VAT here; US holds sales tax  No requirement to capture in the IDS for US.49TAX_RATE2_FGTax Rate 2 flagNumeric L1NULL,1,0   50TAX_RATE3_FGTax Rate 3 flagNumeric L1NULL,1,0   51TAX_RATE4_FGTax Rate 4 flagNumeric L1NULL,1,0   52TAX_RATE5_FGTax Rate 5 flagNumeric L1NULL,1,0   53TAX_RATE6_FGTax Rate 6 flagNumeric L1NULL,1,0   54TAX_RATE7_FGTax Rate 7 flagNumeric L1NULL,1,0   55TAX_RATE8_FGTax Rate 8 flagNumeric L1NULL,1,0   56COST_CASE_ PRCCost per caseNumeric L7NULL Used for tenants in Japan  57DATE_COST_ CASE_ PRCCost per case price dateDate Time N NULLNot used at present   58UNIT_CASEUnit Per CaseNumeric L3NULLThis is the unit size of the case. This format is being reviewed because it does not allow for dec points for catchweight products.
Used in Japan
Out of scope at present.59MIX_MATCH_CDMix and Match CodeNumeric N2NULLUsed originally in Cplus days – not now!  60RTN_CDReturn type codeNumeric  2NULLThis is used for linked items (e.g. deposit items, return code is linked in Storeline to the a linked ‘EAN’)

Used for TV licences for Turkey

Although a group requirement it will be set up linked to location in US but inot in Turkey, so need to have local specific code for thisThis is a UDA for Turkey, but will be an ITEM_LOCATION _TRAIT for US
(awaiting confirmation)For US, 
???????
For Turkey (on move to ORMS12):
SKUItem.ReturnCode 61FAMILY_CDFamily codeNumeric N3NULLWould be used for manufacture coupons to indicate what ‘family’ the product falls into and similarly for attribute 72.  62SUBDEP_IDSub department codeNumeric  12NULLThis is used for reporting in Storeline.DEPT,CLASS&SUBCLASS concatenated for the SKUSKUItem.Section, Class & Subclass concatenated63DISC_CDDiscount numberNumeric N2NULL   64LBL_QTYLabel quantityNumeric 2NULL Set to 1 until S, R & D provide it Expect to be provided from S,R & D 65SCALE_FGScale flagNumeric N1NULL Is not used –WGT_SCALE_FG is used to indicate product should be broadcast to the counter  66LOCAL_DEL_FGLocal delivery flagNumeric N1NULL   67HOST_DEL_FGHost delivery flagNumeric N1NULL   68HEAD_OFFICE_ DEPHead office departmentNumeric N NULL   69WGT_SCALE_FGWeight on scale flagNumeric ?1NULLThis is used to indicate that the details have to be transmitted to the counter tills – so covers Scotch eggs as well as weighed items UDA SKUItem.CounterScaleInd70FREQ_SHOP_ TYPEFrequent Shopper discount typeNumeric N1NULL   71FREQ_SHOP_ VALFrequent Shopper discount amountNumeric N13NULL   72SEC_FAMILYSecond familyNumeric N4NULLSee FAMILY_CD (attribute 61)  73POS_MSGLinked message numberNumeric  2NULL UDA SKUItem.LinkPOSMessage74SHELF_LIFE_DAYShelf life timeNumeric N4NULL Might be used in future for Drop 3 possibly  75PROM_NBRPromotion numberNumeric N NULLUsed for promotions some time ago  76BCKT_NBRBucket numberNumeric N NULLUsed for promotions some time ago  77EXTND_PROM_
NBRExtended promotion numberNumeric N NULLUsed for promotions some time ago  78EXTND_BCKT_NBRExtended bucket numberNumeric N NULLUsed for promotions some time ago  79RCPT_DESCR1Receipt description 1Char N20NULL   80RCPT_DESCR2Receipt description 2Char N20NULL   81RCPT_DESCR3Receipt description 3Char N20NULL   82RCPT_DESCR4Receipt description 4Char N20NULL   83CPN_NBRCoupon numberFloat N13NULL   84TAR_WGT_NBRTare weight numberNumeric N2NULL   85RSTRCT_ LAYOUTRestriction layoutNumeric N2NULL   86INTRNL_IDInternal IDNumeric  13NULLThis is the SKU (item level 2 number) ITEM_MASTER.ITEM_PARENT for the ITM_IDArticleItem.SKUID87OLD_PRCOld priceMoney 13NULLCaptured for Turkey in POS_MODS, but should be provided from Marketing. Source yet to be identified .
  	88QDX_FREQ_ SHOP_ VALQDX Frequent Shopper valueNumeric N13NULL   89VND_IDVendor IDMoney N8NULL   90VND_ITM_IDVendor item IDNumeric N25NULL   91VND_ITM_SZVendor item sizeChar N10NULL   92CMPRTV_UOMComparative UOMNumeric N3NULL   93CMPR_QTYComparative quantityNumeric N12NULL   94CMPR_UNTComparative unitNumeric N12NULL   95BNS_CPN_FGBonus CouponNumeric N1NULL   96EXCLUD_MIN_ PURCH_ FGExclude min perchNumeric N1NULL,1,0   97FUEL_FG* Not used *Numeric N1NULL,1,0   98SPR_AUTH_ RQRD_ FGSupervisor  authority. required.Numeric L3NULL,1,0Is captured for Turkey. Held as UDA on ORMS. UDASKUItem.SupervisorAuthReqdInd99SSP_PRDCT_FG*Not used*Numeric N1NULL,1,0   100NU06_FG* Not used *Numeric N3NULL   101NU07_FG* Not used *Numeric N3NULL   102NU08_FG* Not used *Numeric N3NULL   103NU09_FG* Not used *Numeric N3NULL   104NU10_FG* Not used *Numeric N3NULL   105FREQ_SHOP_ LMTFrequent Shopper limitNumeric N3NULL  106ITM_STATUSItem statusNumeric N3NULL   107DEA_GRPDEA GroupNumeric  N2NULLFlag for drug enforcement agency.
Forces warning message and/or locks sales of products on reaching certain thresholds that fall into this category.
Note can have different groups with different parameters.
Not required for US currently – so have assumed out of scope  108BNS_BY_ OPCODEBonus Buy OP CODE Numeric N2NULL   109BNS_BY_DESCRBonus Buy DescriptionChar N20NULL   110COMP_TYPEComparison TypeNumeric N2NULL   111COMP_PRCComparison PriceNumeric N8NULL   112COMP_QTYComparison QuantityNumeric N4NULL   113ASSUME_QTY_ FGAssume Quantity flagNumeric N1NULL,1,0   114EXCISE_TAX_ NBRExcise tax numberNumeric N3NULL   115RTL_PRICE_ DATERetail price dateDate Time N26 Presumably Storeline can have changes for prices on different dates in the same batch  116PRC_RSN_IDPrice change reason IDNumeric N3    117ITM_POINTItem PointsNumeric N4NULL   118PRC_GRP_IDPrice Group ID for member promotionsNumeric N2NULL   119SWW_CODE_FGInternal PLU Code (Item in System)Numeric L1NULL,1,0Used in Poland for invoicing – assume not required for group solution  120SHELF_STOCK_ FGStore keeps the items in a storage room, and not on shelves.NumericN1NULL,1,0   121UPD_ORIGINUpdate Original itemASCIIN20NULL   122UPD_BATCH_IDUpdate Original IDASC_NN12NULL   123UPD_USER_IDUpdate User IDASCIIN32NULL   124CENTRAL_ITEMCentral ItemASC_NN3NULLBlocks store from amending the product.   125NO_MMBR_CRD_ POINTS_FGNo Member Card Points ASC_NN3NULL   126PRNT_PLU_ID_ RCPT_FGPrint PLU ID receipt flagASC_NN3NULL   127BLK_GRPBulk GroupASC_NN3NULL   128TRSHOLD_ MULTPLRThreshold MultiplierASC_NN3NULL   129LBL_SIZELabel SizeASC_N 4 Had thought this would come from 
ITEM_TICKET.TICKET_TYPE_ID … but now am told it will be sourced from SRDTo be identifiedSKUItem.TicketTypeID  of the parent SKU 
Need to identify the transformation rules130PRINT_LABEL_ FGPrint label flagASC_YN 1 Always set to ‘1’ (yes)  131BS_UOM_IDBasic UOM (Unit of Measure)ASC_N 4 This is selling UOM e.g. kgITEM_LOC.UOM_OF_PRICE for the SKU  - note ITEM_LOC is not published via RIB from ORMS10SKUIteminLoc.PricingUOM132BS_UOM_AMTBasic UOM Amount (Full weight/volume of item – selling weight)ASC_N 13 The content amount for the selling UOMITEM_LOC.MEAS_OF_EACH for the SKU l2 item  - note ITEM_LOC is not published via RIB from ORMS10SKUIteminLoc.MeasureOfEach133CMPR_UOM_IDComparative UOM (Empty in S/D interface)ASC_N 4 This is used for showing the unit price on the SELITEM_LOC.UOM_OF_PRICE for the SKU 
does this assume comparison is in same dimensions as basis i.e. we can’t have grams and kg?SKUIteminLoc.PricingUOM134CMPR_UOM_AMTComparative UOM amount
(Weight/Volume/Length that the unit price is calculated against)ASC_N 13 This is used for showing the unit price on the SEL e.g. might want to show unit price as price ‘per 100grams’ITEM_LOC.MEAS_OF_PRICE for the SKU l2 item  - note ITEM_LOC is not published via RIB from ORMS10SKUIteminLoc.MeasureOfPrice135LBL_UOMLabel UOM (Description of the Unit Price Measure)ASCII 25 This is the text that has to go on the label e.g. ‘per 100 grams’Awaiting confirmation that this will be set up as a UDA136POS_RFND_MSGPos Refund messageASCIIN1    137FORECOURT_SERVICES_FGForecourt services flgASC_YNN1    138VND_ITM_ID2Vendor item ID 2CharN24    139WEEKS_SUPPLYWeeks supplyNumericL2 Required for Japan for ordering  140MIN_ORDER_QTYMinimum order qtyNumericL6   141MAX_ORDER_QTYMaximum order qty NumericL6   142ORDERABLEOrderable flgASC_YNL1 Indicates if the item is orderable & receivable in store. Captured in TurkeyITEM_MASTER. ORDERABLE_IND 143INVENT_FG
Believe that is actually a non-inventory flagInvent flgASC_YN1 Indicator to show if Storeline is to maintain the stock transactions etc. e.g. Storeline will not keep an inventory for newspapers.
 ITEM_MASTER.INVENTORY_FLAG –
But not available in ORMS10 SKUItem.InventoryFlag
To be added 

Uses presence of item_loc row for the location – y if ranged, n, otherwise. 
144SPECIAL_ORD_QTYSpecial order qtyNumericN3   145FREE_QTYFree qtyNumericN3   146HO_INSTRUCTUsed for DC IndicatorChar?6 Used for labelling to indicate whether the item is supplied from a DC.  147DSCNT_LINEDscnt line ASC_YN1 Product Status
0 – Standard
1 – New
2 – Discontinued
Functionality for this introduced in FSD9303 Will be provided from Space, Range & DisplayTo be defined when SRD interface is designed148PRDCT_GRDINGProduct grading  Char40 Product grading
Functionality for this introduced in FSD9303
Change in field length from original field Will be provided from Space, Range & Display To be defined when SRD interface is designedWill not be used149LOCATION1Location 1CharN6    150LOCATION2Location 2CharN6    151VAT_ON_CENTER_PRICEVat on center priceASC_YNL1 Used for Thailand – VAT is calculated on the ‘government’ price (not the store price which might be a lower value). In this case ‘government price is recorded as the centre price on the PLU file.  152PRIMARY_PLU_FGPrimary PLU ASC_YN 1 Primary EAN for the SKUITEM_MASTER.PRIMARY_REF_ITEM_INDArticleitem.PrimaryRefItemInd153IMPORTED_FGImported ASC_YN L1 Used in Turkey UDASKUItem.ImportitemInd 154SUB_GROUP_IDSub Group IdCharN5 Used in the UK but not required for Group  155ORGN_PLCOrigin PlaceCharL40 Used for China for labelling  SKUItem.PlaceOfOrigintbaTo be advised for the remaining fieldsShelf talker indicatorASC_YN1Functionality for this introduced in FSD9303
Marketing are meant to provide this – but no system source yet available
Multi-location indicatorASC_YN1Functionality for this introduced in FSD9303
Will be provided from Space, Range & Display To be defined when SRD interface is designedOld price indicatorASC_YN1Functionality for this introduced in FSD9303
No source identified
Shelf facingASC_N3Functionality for this introduced in FSD9303
Will be provided from Space, Range & Display To be defined when SRD interface is designedText for State Redemption Value to be chargedASCII20Functionality for this introduced in FSD9303
Bo source identified
Will not be usedProduct textureASCII40Functionality for this introduced in FSD9303
No source identified
Will not be usedProduct specificationASCII120Functionality for this introduced in FSD9303
No source identified
Will not be usedProduct rangeASC_N1Functionality for this introduced in FSD9303
0 – Not ranged
1 – centrally ranged
2 – locally ranged
Will be provided from Space, Range & Display To be defined when SRD interface is designedPlanogramASCII25Functionality for this introduced in FSD9303
Will be provided from Space, Range & Display To be defined when SRD interface is designedCatchweight_Indicator1Functionality for this introduced in CR1557
If SaleType = ‘V’, then set CatchweightIndicator to ‘1’, else set to ‘0’
ITEM_MASTER.SALE_TYPESKUID.SaleTypeWill not be used




Glossary of Terms

Mnemonic
Description
IDS
Integration Data Store
ORMS
Oracle Retail Management System
ORPM
Oracle Retail Price Management
PLU
Product & Price File
RIB
Retek Integration Bus
SEL
Shelf Edge Label











	 Integration Team: Requirements Definition




PAGE  


Date:  REF Date  \* MERGEFORMAT 25/01/2007 , Version  REF Version  \* MERGEFORMAT 0.3		Page  PAGE 34 of  NUMPAGES 35
Author : Heather Rennoldson


	
Integration Team : Requirements Definition







Date:  REF Date  \* MERGEFORMAT 25/01/2007 , Version  REF Version  \* MERGEFORMAT 0.3		Page  PAGE 35 of  NUMPAGES 35
Author : Heather Rennoldson







 EMBED Word.Picture.8  







