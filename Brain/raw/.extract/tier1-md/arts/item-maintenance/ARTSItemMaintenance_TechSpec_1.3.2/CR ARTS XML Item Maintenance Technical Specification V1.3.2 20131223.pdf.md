ARTS XML Item Maintenance Technical Specification V1.3.0

ARTS XML Item Maintenance

Technical Specification

Version 1.3.2

Dec 23, 2013 – Candidate Recommendation

Copyright © National Retail Federation 2013. All rights reserved.

This  document  and  translations  of  it  may  be  copied  and  furnished  to  others,  and
derivative works that comment on or otherwise explain it or assist in its implementation
may  be  prepared,  copied,  published  and  distributed,  in  whole  or  in  part,  without
restriction  of  any  kind, provided that  the  above  copyright  notice  and this  paragraph  are
included on all such copies and derivative works.  However, this document itself may not
be  modified  in  any  way,  such  as  by  removing  the  copyright  notice  or  references  to  the
NRF,  ARTS,  or  its  committees,  except  as  needed  for  the  purpose  of  developing  ARTS
standards  using  procedures  approved  by  the  NRF,  or  as  required  to  translate  it  into
languages other than English.

The  limited  permissions  granted  above  are  perpetual  and  will  not  be  revoked  by  the
National Retail Federation or its successors or assigns.

Copyright  2013 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 1

ARTS XML Item Maintenance Technical Specification V1.3.2

TABLE OF CONTENTS

1.  ABSTRACT ......................................................................................................................................... 6

1.1  OVERVIEW ........................................................................................................................................ 6

2.

BUSINESS SCOPE ............................................................................................................................. 8

2.1  MESSAGE SCHEMAS .......................................................................................................................... 8
2.2  OUT OF SCOPE .................................................................................................................................. 8

3.  REFERENCED DOCUMENTS ...................................................................................................... 10

3.1  RELATED DOCUMENTS ................................................................................................................... 10

4.  ADD MULTIPLE ITEMS ................................................................................................................ 11

4.1  USE CASE: ITEM PURCHASE (POSLOG) ........................................................................................... 11
SCENARIO: ITEM PURCHASE AT POS (POSLOG) ........................................................................ 11
4.1.1
SCENARIO: ITEM PURCHASE FOR ALTERATION & SUBSEQUENT PICKUP (POSLOG) .................... 13
4.1.2
SCENARIO: ITEM PURCHASE BY RANDOM WEIGHT (POSLOG) .................................................... 15
4.1.3
SCENARIO: ITEM PURCHASE OF SERIALIZED ITEM (POSLOG) ..................................................... 17
4.1.4
SCENARIO: ITEM PURCHASE WITH PART EXCHANGE (POSLOG) ................................................. 19
4.1.5
SCENARIO: ITEM PURCHASE WITH QUANTITY PRICING (POSLOG) .............................................. 21
4.1.6
SCENARIO: ITEM PURCHASE OF MULTI-PACKAGE ITEMS (POSLOG) ........................................... 23
4.1.7
4.1.8
SCENARIO: ADD ITEM WITH MULTIPLE ITEM ID’S ..................................................................... 25
4.2  USE CASE: ITEM PURCHASE OF KIT/COMBO/COLLECTION ITEMS (POSLOG) ................................... 27
SCENARIO KIT/COMBO/COLLECTION PURCHASE WITHOUT SUBSTITUTION (POSLOG) .............. 27
4.2.1
SCENARIO: KIT/COMBO/COLLECTION PURCHASE WITH SUBSTITUTION (POSLOG) ................... 29
4.2.2
SCENARIO: FOODSERVICE COMBO (POSLOG) ............................................................................ 32
4.2.3
4.2.4
SCENARIO: IDENTIFY THE KIT TO WHICH THIS ITEM IS A PART. ................................................... 34
4.3  USE CASE: ITEM PURCHASE & RETURN WITH DEPOSIT (POSLOG) ................................................. 36
4.3.1
SCENARIO: PURCHASE CRATE OF BEER WITH EMPTIES (POSLOG) ............................................ 36
4.4  USE CASE: AVAILABILITY TIMES .................................................................................................... 38
SCENARIO: AVAILABLE TO RECEIVE .......................................................................................... 38
4.4.1
SCENARIO: AVAILABLE TO ORDER ............................................................................................. 40
4.4.2
SCENARIO: AVAILABLE TO SALE ................................................................................................ 42
4.4.3
SCENARIO: AVAILABLE TO END SALE ........................................................................................ 44
4.4.4
SCENARIO: AVAILABLE TO RETURN END DATE/TIME FOR CONSUMER ....................................... 46
4.4.5
4.4.6
SCENARIO: AVAILABLE TO RETURN END DATE/TIME FOR REVERSE LOGISTICS .......................... 48
4.5  USE CASE: DISPLAY ITEM NAMES AND/OR DESCRIPTIONS ............................................................. 50
4.5.1
OPERATOR ................................................................................................................................................ 50
4.5.2
SCENARIO: DISPLAY ITEM NAMES IN DIFFERENT LANGUAGES FOR THE VARIOUS RECEIPT
FORMAT 52
4.5.3
SCENARIO: DEVICE SPECIFIC MESSAGES ................................................................................... 54
4.6  USE CASE: IDENTIFY SALES RESTRICTED ITEMS ............................................................................. 56
SCENARIO: TIME AND DATE RESTRICTIONS ............................................................................... 56
4.6.1
SCENARIO: LICENSE RESTRICTIONS ........................................................................................... 58
4.6.2
SCENARIO: QUANTITY RESTRICTIONS ........................................................................................ 60
4.6.3
SCENARIO: TENDER RESTRICTIONS ............................................................................................ 62
4.6.4
SCENARIO: PURCHASER AGE RESTRICTIONS .............................................................................. 64
4.6.5
4.6.6
SCENARIO: SELLER AGE RESTRICTIONS ..................................................................................... 66
4.7  USE CASE: ASSEMBLY INSTRUCTIONS ............................................................................................ 68
4.7.1
SCENARIO: PRINT RECIPE ON RECEIPT ....................................................................................... 68
SCENARIO: SELL ITEM THAT REQUIRES ASSEMBLY ..................................................................... 70
4.7.2
4.8  USE CASE: ITEM RETURN (POSLOG) ............................................................................................... 72
SCENARIO: RETURN TO STORE (POSLOG) ................................................................................. 72
4.8.1

SCENARIO: DISPLAY ITEM NAMES IN DIFFERENT LANGUAGES FOR BOTH THE CUSTOMER AND

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 2

ARTS XML Item Maintenance Technical Specification V1.3.2

4.9  USE CASE: GIFT CERTIFICATE PURCHASE (POSLOG) ..................................................................... 74
USE CASE: ITEM PURCHASE ON BACKORDER (POSLOG) ............................................................ 76
4.10
SCENARIO: BACK-ORDER ...................................................................................................... 76
4.10.1
4.10.2
SCENARIO: BACK-ORDER FOR DELIVERY (POSLOG) ............................................................ 78
USE CASE: PSEUDO-PRODUCTION (V1 IF SELLING END ITEM) .................................................... 80
4.11
SCENARIO: ITEM TRANSFORMATION FROM BULK TO INDIVIDUAL ITEMS .............................. 80
4.11.1
SCENARIO: UTILIZE RECIPE TO CREATE ITEMS ....................................................................... 82
4.11.2
SCENARIO: EQUIPMENT THAT CAN AFFECT THE END PRODUCT. .......................................... 84
4.11.3

5.  USE CASE: UPDATE MULTIPLE ITEMS .................................................................................. 87

5.1  SCENARIO: UPDATE SEVERAL ITEMS, DELETE SEVERAL, ADD SEVERAL ......................................... 87

6.  USE CASE: TAX (POSLOG) LATER VERSION EXCEPT WHERE NOTED: ....................... 89

6.1  SCENARIO: SELL ITEM WHICH IS SUBJECT TO TAX ........................................................................... 90

7.

SCHEMA IMPLEMENTATION .................................................................................................... 93

8.  DOCUMENT HISTORY ................................................................................................................. 94

9.  GLOSSARY ...................................................................................................................................... 96

Table of Figures
Figure 1: Item Retail Interfaces .......................................................................................... 6
Figure 2: Item Purchase at POS (POSLog)....................................................................... 12
Figure 3: Item purchase for alteration & subsequent pickup (POSLog) .......................... 14
Figure 4: Item purchase by random weight (POSLog) ..................................................... 16
Figure 5: Item purchase of serialized item (POSLog) ...................................................... 18
Figure 6: Item purchase with part exchange (POSLog) .................................................... 20
Figure 7: Item purchase with quantity pricing (POSLog) ................................................ 22
Figure 8: Item purchase of multi-package items (POSLog) ............................................. 24
Figure 9: Add Item with Multiple Item ID’s .................................................................... 26
Figure 10: Kit/Combo/Collection Purchase without Substitution (POSLog) ................... 28
Figure 11: Kit/Combo/Collection Purchase with Substitution (POSLog) ........................ 31
Figure 12: Foodservice Combo (POSLog) ....................................................................... 33
Figure 13: Identify the kit to which this item is a part ...................................................... 35
Figure 14: Purchase Crate of Beer with Empties (POSLog) ............................................ 37
Figure 15: Available to Receive ....................................................................................... 39
Figure 16: Available to Order ........................................................................................... 41
Figure 17: Available to Sale ............................................................................................. 43
Figure 18: Available to End Sale ...................................................................................... 45
Figure 19: Available to Return End date/time for Consumer ........................................... 47
Figure 20: Available to Return End date/time for Reverse Logistics ............................... 49
Figure 21: Display Item Names in Different Languages .................................................. 51
Figure 22: Display Item for Receipts in Different Language ........................................... 53
Figure 23 : Device Specific Messages .............................................................................. 55
Figure 24: Time and Date Restrictions ............................................................................. 57
Figure 25 : License Restrictions ....................................................................................... 59
Figure 26 : Quantity Restrictions ...................................................................................... 61
Figure 27 : Tender Restrictions......................................................................................... 63

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 3

ARTS XML Item Maintenance Technical Specification V1.3.2

Figure 28: Purchaser Age Restriction ............................................................................... 65
Figure 29: Seller Age Restrictions .................................................................................... 67
Figure 30: Print Recipe on Receipt ................................................................................... 69
Figure 31: Identify Assembly Instructions ....................................................................... 71
Figure 32: Return to Store (POSLog) ............................................................................... 73
Figure 33: Gift Certificate Purchase (POSLog) ................................................................ 75
Figure 34: Back-Order Domain Model ............................................................................. 77
Figure 35: Back-Order for Delivery (POSLog) ................................................................ 79
Figure 36: Item Transformation from Bulk to Individual items ....................................... 81
Figure 37: Explode Recipe to Items.................................................................................. 83
Figure 38: Equipment That Can Affect the End Product. ................................................. 85
Figure 39: Update several items, Delete several, Add several ......................................... 88
Figure 40: Sell item which is subject to tax ...................................................................... 91

Table of IXRetail XML Samples
4.1.1 Conformance XML Instance Document – Item Purchase at POS (POSLog) ......... 13
4.1.2 Conformance XML Instance Document — Item purchase for alteration &

subsequent pickup (POSLog) ................................................................................... 15

4.1.3 Conformance XML Instance Document — Item purchase by random weight

(POSLog) .................................................................................................................. 17

4.1.4 Conformance XML Instance Document – Item purchase of serialized item

(POSLog) .................................................................................................................. 19

4.1.5 Conformance XML Instance Document — Item purchase with part exchange

(POSLog) .................................................................................................................. 21

4.1.6 Conformance XML Instance Document — Item purchase with quantity pricing

(POSLog) .................................................................................................................. 23

4.1.7 Conformance XML Instance Document — Item purchase of multi-package items

(POSLog) .................................................................................................................. 25
4.1.8 Conformance XML Instance Document – Add Item with Multiple Item ID’s ....... 27
4.2.1 Conformance XML Instance Document — Kit/Combo/Collection Purchase without
Substitution (POSLog) .............................................................................................. 29

4.2.2 Conformance XML Instance Document — Kit/Combo/Collection Purchase with

Substitution (POSLog) .............................................................................................. 32
4.2.3 Conformance XML Instance Document – Foodservice Combo (POSLog) ............ 34
4.2.4 Conformance XML Instance Document — Identify the kit to which this item is a

part. ........................................................................................................................... 36

4.3.1 Conformance XML Instance Document — Purchase Crate of Beer with Empties

(POSLog) .................................................................................................................. 38
4.4.1 Conformance XML Instance Document — Available to Receive .......................... 40
4.4.2 Conformance XML Instance Document — Available to Order .............................. 42
4.4.3 Conformance XML Instance Document — Available to Sale ................................ 44
4.4.4 Conformance XML Instance Document — Available to End Sale ......................... 46
4.4.5 Conformance XML Instance Document — Available to Return End date/time for

Consumer .................................................................................................................. 48

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 4

ARTS XML Item Maintenance Technical Specification V1.3.2

4.4.6 Conformance XML Instance Document — Available to Return End date/time for

Reverse Logistics ...................................................................................................... 50

4.5.1 Conformance XML Instance Document — Display Item Names in Different

Languages for Both the Customer and Operator ...................................................... 52

4.5.2 Conformance XML Instance Document — Display Item Names in Different

Languages for the Various Receipt Format .............................................................. 54
4.5.3 Conformance XML Instance Document — Device Specific Messages .................. 56
4.6.1 Conformance XML Instance Document — Time and Date Restrictions ................ 58
4.6.2 Conformance XML Instance Document — License Restrictions ........................... 60
4.6.3 Conformance XML Instance Document — Quantity Restrictions .......................... 62
4.6.4 Conformance XML Instance Document — Tender Restrictions ............................ 64
4.6.5 Conformance XML Instance Document – Purchaser Age Restrictions .................. 66
4.6.6 Conformance XML Instance Document – Seller Age Restrictions ......................... 68
4.7.1 Conformance XML Instance Document — Print Recipe on Receipt ...................... 70
4.7.2 Conformance XML Instance Document – Identify Assembly Instructions ............ 72
4.8.1 Conformance XML Instance Document — Return to Store (POSLog) .................. 74
4.9 Conformance XML Instance Document — Gift Certificate Purchase (POSLog) ...... 76
4.10.1 Conformance XML Instance Document — Back-Order (POSLog) ...................... 78
4.10.2 Conformance XML Instance Document — Back-Order for Delivery (POSLog) . 80
4.11.1 Conformance XML Instance Document — Item Transformation from Bulk to

Individual items ........................................................................................................ 82
4.11.2 Conformance XML Instance Document — Explode Recipe to Items .................. 84
4.11.3 Conformance XML Instance Document — Equipment That Can Affect the End

Product. ..................................................................................................................... 86

5.1 Conformance XML Instance Document – Update several items, Delete several, Add

several ....................................................................................................................... 89
6.1 Conformance XML Instance Document – Sell item which is subject to tax .............. 92

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 5

ARTS XML Item Maintenance Technical Specification V1.3.2

1.  ABSTRACT

1.1  Overview

Inventory Accounting

Logistics

Inventory Costing

Warehouse

Inventory Analysis

Retail/Cost
Stock Ledger

Inventory Control/Audit

Stock Locator

Contract Management

Price Management

Price Server

Promotion Management

Ticketing/Signage/
Price Marking

Fraud Detection/
Prevention

Forecasting

Planning

Sales Planning

Item (Merchandise)
Management System

Item Master

Customer Profiling

Layaway

Catalog Management

Fulfillment/
Customer Order
Management

Point of Sale (POS)

Catalog/Web Selling

Rentals

Gift Registry

The ‘item’ is the baseline element of retail; a retail enterprise exists to sell items.

Figure 1: Item Retail Interfaces

There is a very small number of systems in a retail enterprise (usually one) that expect to
‘own’ item data and a very large number of systems that require item data to fulfill their
function. Item data in most retail enterprises changes on a regular basis. Because of the
large  number  of  systems  involved  and  the  frequency  of  change,  a  standard  for

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 6

ARTS XML Item Maintenance Technical Specification V1.3.2

communicating item information between systems in a retail enterprise will provide huge
benefits in system integration efforts applicable to virtually all retailers.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 7

ARTS XML Item Maintenance Technical Specification V1.3.2

2.  Business Scope

The  following  are  to  be  considered  within  the  scope  of  the  team  developing  the  first
version of the item maintenance schema:




Item attributes required for systematic functions
Item attributes required for communications between systems within a retail
enterprise.

  XSL Maps to/from equivalent standards ( for example UCC-EAN, NACS),

Items that are sold, in the past, present or future

relevant to IXRetail target audience
  CRUD  (Create, update, delete) functions

  A Publish-Subscribe paradigm (including file publication)
  Heavy use of extension mechanisms
  Absolute prices that are included as attributes of an item, including but not limited

to:

  Manufacturer’s suggested retail price
  Cost
  Regular price (compare to)
  Selling price (permanent mark down)
  Price levels

2.1  Message Schemas

2.2  Out of Scope

Algorithms or rules which affect the price of an individual or collection of items are out
of scope of the Item Maintenance work team.

Algorithms or rules determining taxation of an individual or collection of items are out of
scope of the Item Maintenance work team.

Future Versions

The following may be considered within the scope of the Item Maintenance work team,
but  are  deferred  for  possible  consideration  in  future  versions  of  this  specification  or
delegation to other IXRetail work teams.



Item attributes require for communications of a B-to-B or Supply chain nature (to
systems outside of the retail enterprise)

  Relationships between items (for example, shipping case vs saleable item within



the case)
Item  attributes  required  for  customer  facing  activity  (for  example  ad  copy,
images, selling message, brand copy)
Item attributes of store fixtures


  A request-response paradigm

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 8

ARTS XML Item Maintenance Technical Specification V1.3.2

Item attributes related to the design and development of product


  Definition or communication of the merchandise hierarchy (taxonomy)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 9

ARTS XML Item Maintenance Technical Specification V1.3.2

3.  REFERENCED DOCUMENTS

IXRetail

IXRetail Item Maintenance Charter, Version 1.00
IXRetail Extending Schemas Technical Report
IXRetail XML Best Practices, 2001-7-31
IXRetail XML Dictionary, Version 3.0 Build 04





  ARTS Data Model, Version 4.0.1
  ARTS UnifiedPOS, Version 1.9 (ScanDataType Property R)
  WD IXRetail Infrastructure Technical Specification, Version 1.0
  CR IXRetail POSLog Technical Specification, Version 2.1

  NRF PAS© Product Attribute System

IXRetail Common Data Technical Specification, Version 1.0

3.1  Related Documents

The following were researched in the creation of this technical specification
  UCCNet

  ProductTradeItem.xsd
  TradeItem.xsd
  TradeItemComponents.xsd
  HardlinesTradeItem.xsd
  OTCTradeItem.xsd

  NACS POS/Back Office Interface Guidelines Version 3.0

  NAXML-PBIMaintenance33.xsd
  NAXML-PBIMovement33.xsd
  NAXML-PBIUnits33.xsd
  NAXML-PBIBaseTypes33.xsd
  NAXML-PBIUtility33.xsd
  NAXML-FuelTankStockReport33.xsd
  NAXML-AutoSafeReport33.xsd

  EAN International,
  FMGCItem.xsd

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 10

ARTS XML Item Maintenance Technical Specification V1.3.2

4.  ADD MULTIPLE ITEMS

Multiple item add notification from item management system to consuming system .

4.1  Use case: Item purchase (POSLog)

One  or  more  items  are  purchased  via  any  one  of  a  number  of  sales  channels.  The
transaction  is  entered  in  via  an  appropriate  application,  and  is  sent  using  the  POS-Log
schema  to  the  POS-Log  application,  which  may  forward  to  the  transaction  to  other
applications in the enterprise.

4.1.1  Scenario: Item Purchase at POS (POSLog)

Brief Description

Customer  selects  one  or  more  items  and  purchases  them.  The  number  of  those  items
available in inventory is decremented.
The Item Maintenance provides the data necessary to support selling this item. This is a
tax free environment.
 Data



Item sale data, including:
  An identifier for the item being sold.
  Unit price for the item being sold.

Sale ItemType=”Stock
ItemID
MerchandiseHierarchy Level=”Department”
Description
TaxIncludedInPriceFlag
Price Common Data

RegularSalesUnitPrice

UnitCostPrice
UnitListPrice
RegularSalesUnitPrice
InventoryValuePrice

The sale unit monetary value of the
item which is the original retail
minus permanent markdowns taken
against this item.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 11

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 2: Item Purchase at POS (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 12

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.1 Conformance XML Instance Document – Item Purchase at POS (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit TypeCode="RetailStore">100</BusinessUnit>
<Item Action="AddItem">

<ItemID Type="SKU">12345678</ItemID>
<MerchandiseHierarchy Level="Department">Men’s clothing</MerchandiseHierarchy>
<ItemPrice Currency="USD" ValueTypeCode="RegularSalesUnitPrice" >2.60</ItemPrice>

</Item>

</ItemMaintenance>

4.1.2  Scenario:  Item  purchase  for  alteration  &  subsequent
pickup (POSLog)

Brief Description

Customer selects some kitchen cabinets from unpainted models on shop floor, and selects
color  for  them  to  be  painted.    The  paint-shop  takes  the  cabinets  from  inventory,  paints
them and makes them available for the customer to pickup.
Data



Item sale data, including:
  An identifier for the item being sold.
  Unit price for the item being sold.
  Alteration details

  Alteration tracking number
  need to know this item is customizable – alterable
  can be altered by these other item (possible service)

Inventory reservation tracking number

SaleForPickup ItemType=”Stock
MerchandiseHierarchy Level=”Department
ItemID
Alteration Flag
Description
Price Common Data
Kit
Member Action=”IsPartOf
SaleForPickup ItemType=”Alteration
MerchandiseHierarchy Level=”Department
Description
Additional Item

ItemID
Price
AlterationInstructions

Is it alterable?

Identifies the items that can be used to
modify this item 1..*
1..*

Related to the alteration item.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 13

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 3: Item purchase for alteration & subsequent pickup (POSLog)
Page 14

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.2 Conformance XML Instance Document — Item purchase for alteration &
subsequent pickup (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit TypeCode="RetailStore">100</BusinessUnit>
<Item AlterableFlag="true" Action="ChangeItem">
<ItemID Type="SKU">12345678</ItemID>
<MerchandiseHierarchy Level="Division">Kitchen</MerchandiseHierarchy>
<AlterationItem>

<Item>

<!-- White Paint -->
<ItemID Type="SKU">4567</ItemID>

</Item>
<Price Currency="USD" ValueTypeCode="RegularSalesUnitPrice">30</Price>
<AlterationInstructions>Paint the cabinets whhite</AlterationInstructions>
<SpecialOrderNumber>1</SpecialOrderNumber>

</AlterationItem>
<ItemPrice Currency="USD" ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>

</Item>

</ItemMaintenance>

4.1.3  Scenario: Item purchase by random weight (POSLog)

Brief Description

Customer purchases an item from the delicatessen, which is sold by weight.
Data



Item sale data, including:
  An identifier for the item being sold.
  The amount of the item being sold.
  The units of measure that the weight is expressed in.
  Price per unit of measure being charged for the item.

Alternate scenario: sell by non-random measurement
Sell curtains by nearest quarter inch (width of window)

Sale ItemType=”Stock
MerchandiseHierarchy Level=”Department
Item and Price common Data

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 15

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 4: Item purchase by random weight (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 16

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.3 Conformance XML Instance Document — Item purchase by random weight
(POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock" WeightEntryFlag="true" Action="ChangeItem">

<ItemID Type="SKU">12345678</ItemID>
<MerchandiseHierarchy Level="Department">delicatessen</MerchandiseHierarchy>
<ItemPrice UnitOfMeasureCode="LBR"

ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>

</Item>

</ItemMaintenance>

4.1.4  Scenario: Item purchase of serialized item (POSLog)

Brief Description

Customer  buys  one  or  more  items  some  of  which  require  that  the  serial  number  of  the
unit sold be recorded.
Data

Item sale data, including:

  An identifier for the item being sold.
  The unit price for the item being sold.
  The serial number of each item being sold

Prompt for serial number(s) when I buy it
Sell in lots and batches
Need flag and place to put serial number(s)

Sale ItemType=”Stock
Serialized flag
Multiple serial numbers

Item and Price common Data
ItemID

Count of multiple serial numbers in
one box

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 17

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 5: Item purchase of serialized item (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 18

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.4 Conformance XML Instance Document – Item purchase of serialized item
(POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit TypeCode="RetailStore">100</BusinessUnit>
<Item ItemCategory="Stock" SerialNumberFlag="true" Action="ChangeItem">

<ItemID Type="SKU">12345678</ItemID>
<ItemPrice Currency="USD" ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>
<SerializedItem>

<Count>40</Count>

</SerializedItem>

</Item>

</ItemMaintenance>

4.1.5  Scenario: Item purchase with part exchange (POSLog)

Brief Description

Customer purchases an item, such as a car battery, where an accompanying dead battery
will reduce the price of the new battery. There is no refundable amount on a dead battery
without a corresponding purchase.

Data

Item sale data, including:

  An identifier for the battery being sold.
  Unit price for the battery.

Item return data, including:

  An identifier for the battery being returned.
  Price reduction on new battery because of dead battery return.

-

record part exchange is possible

Sale ItemType=”Stock
MerchandiseHierarchy Level=”Department
Description
Exchangeable flag

ItemLink
ItemID
Disposal Method=”ReturnToManufacturer

Indicates a core can be taken for
this item
Links to the core

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 19

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 6: Item purchase with part exchange (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 20

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.5 Conformance XML Instance Document — Item purchase with part exchange
(POSLog)

NOTE: the core charge is stored with the ItemID for the battery being returned
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit TypeCode="RetailStore">100</BusinessUnit>
<Item ExchangeableFlag="true" Action="ChangeItem">

<ItemID Type="SKU">12345678</ItemID>
<MerchandiseHierarchy Level="Department">Men's Clothing </MerchandiseHierarchy>
<ExchangeItemID DisposalMethod="ReturnToStock" Type="SKU">String</ExchangeItemID>
<ItemPrice Currency="USD" ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>

</Item>

</ItemMaintenance>

4.1.6  Scenario: Item purchase with quantity pricing (POSLog)

Brief Description

Candy bars are priced at $0.59 each or 2 for $.99.   This is not a promotion; this is the
normal pricing for the collection of items.
Data

Item data, including:

  An identifier for the item being sold.
  The quantity that applies to the unit-price.
  The unit-price of the item

Sale ItemType=”Stock
MerchandiseHierarchy Level=”Department
Description
Price common data
ItemID
The other categories in this mix match

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 21

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 7: Item purchase with quantity pricing (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 22

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.6 Conformance XML Instance Document — Item purchase with quantity
pricing (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit TypeCode="RetailStore">100</BusinessUnit>
<Item Action="ChangeItem">

<ItemID Type="SKU">12345678</ItemID>
<MerchandiseHierarchy Level="Department">Candy</MerchandiseHierarchy>
<ItemPrice Currency="USD" ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>
<MixMatch>

<MixMatchID>1234</MixMatchID>
<MixMatchPrice Quantity="2">.99</MixMatchPrice>

</MixMatch>

</Item>

</ItemMaintenance>

4.1.7  Scenario: Item purchase of multi-package items (POSLog)

Brief Description

Customer purchases a can of a popular soft drink.  The can is scanned into the POS.  The
UPC code on the can is for both a can and a 6 pack. Some distinction between the single
can and the 6-pack must be made.

Data

Item data, including:

  An identifier for the item being sold.
  The number of multiples of the item being sold.
  The unit-price of the item

Sale ItemType=”Stock
Standard Item and Price Data
ItemID
Quantity UOMCode=”6Pack

1..* to describe
Different price for each option

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 23

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 8: Item purchase of multi-package items (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 24

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.7 Conformance XML Instance Document — Item purchase of multi-package
items (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">
<ItemID Type="SKU">12345678</ItemID>
<ItemPrice Quantity="6" UnitOfMeasureCode="EA"
ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>

</Item>

</ItemMaintenance>

4.1.8  Scenario: Add Item with Multiple Item ID’s

Brief Description

We have to receive both SKU and barcode(s) item identifiers from Head Office with all
other data of the article.
 Data



Item sale data, including:
  An identifiers for the item being sold.

Sale ItemType=”Stock
ItemID
AlternativeItemID

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 25

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Figure 9: Add Item with Multiple Item ID’s
Page 26

ARTS XML Item Maintenance Technical Specification V1.3.2

4.1.8 Conformance XML Instance Document – Add Item with Multiple Item ID’s
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit TypeCode="RetailStore">100</BusinessUnit>
<Item Action="AddItem">

<ItemID Type="SKU">12345678</ItemID>
<AlternativeItemID Type="UPC">221341234</AlternativeItemID>

</Item>
</ItemMaintenance>

4.2  Use case: Item purchase of kit/combo/Collection items
(POSLog)

For  some  retailers  an  item  may  actually  be  a  Kit,  Combination  or  Collection  of  other
items,  e.g.  A  garden  furniture  set  may  be  comprised  of  a  table,  four  chairs  and  a  sun
umbrella.  Retailers may allow some items in some kit items to be substituted; others may
not.

4.2.1  Scenario
Substitution (POSLog)

Kit/Combo/Collection

Purchase

without

Brief Description

Customer  buys  a  kit  of  garden  furniture  comprising  a  table,  four  chairs  and  a  sun
umbrella.    The  POS  sells  this  kit  as  if  it  was  a  single  item,  and  no  substitutions  are
permitted.
Data



Item sale data, including:
  An identifier for the kit item being sold.
  Unit price for the kit item being sold.

Sale ItemType=” ItemCollection
MerchandiseHierarchy Level=”Department
Description
Standard item and price Data
Kit
Kit Item ID
Member Action=”IsPartOf

List of items in the kit 1..*

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 27

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 10: Kit/Combo/Collection Purchase without Substitution (POSLog)
Page 28

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

ARTS XML Item Maintenance Technical Specification V1.3.2

4.2.1 Conformance XML Instance Document — Kit/Combo/Collection Purchase
without Substitution (POSLog)
NOTE: There are multiple ways to identify a kit.  For almost everybody, the item id on
the item for the kit is the identifier.  But there are those who wanted to have a KitID.
Eventually the alternate method (KitID) will go away and there will only be one itemid
for the kit.
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item Action="ChangeItem">

<ItemID Type="SKU">12345678</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">130.00</ItemPrice>
<Kit Action="IsPartOf" ModifiableFlag="false">

<KitID Type="SKU">987</KitID>
<Members>

<!-- Table -->
<ItemID Type="SKU">6789</ItemID>
<!-- Umbrella -->
<ItemID Type="SKU">3456</ItemID>
<!-- 4 Chairs -->
<ItemID Type="SKU" Quantity="4">1324</ItemID>

</Members>

</Kit>

</Item>

</ItemMaintenance>

4.2.2  Scenario:
Substitution (POSLog)

Kit/Combo/Collection

Purchase

with

Brief Description

Customer  buys  a  kit  of  garden  furniture  set  but  wants  to  replace  the  sun  umbrella with
another brand of equal value.  The system removes one brand of sun umbrella from the
kit and adds the desired brand of sun umbrella to the kit.
The alternate item is for the umbrella, not the kit.
Data

Item sale data, including:

  An identifier for the kit item being sold.
  The normal unit price for the kit item being sold.

Substitution data, including:

  An identifier for the item being removed from the kit item.
  The monetary amount the item being removed contributes to the kit price.
  An identifier for the item being added to the kit item.
  The monetary amount the item being added is contributing to the kit price.

Sale ItemType=” ItemCollection
MerchandiseHierarchy Level=”Department

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 29

ARTS XML Item Maintenance Technical Specification V1.3.2

Description
RegularSalesUnitPrice
Common item and price Data
Alternate Item

1..*

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 30

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 11: Kit/Combo/Collection Purchase with Substitution (POSLog)
Page 31

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

ARTS XML Item Maintenance Technical Specification V1.3.2

4.2.2 Conformance XML Instance Document — Kit/Combo/Collection Purchase
with Substitution (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit Name="String" TypeCode="RetailStore">100</BusinessUnit>
<Item Action="ChangeItem">

<!-- Lawn Furniture Kit ID -->
<ItemID Type="SKU">12345678</ItemID>
<ParentItemID Type="SKU">987</ParentItemID>
<AlternativeItem Action="Substitute">

<!-- Red Umbrella -->
<ItemID Qualifier="String" Type="SKU">1acdse</ItemID>
<AdjustmentAmount TypeCode="EvenExchange">00</AdjustmentAmount>

</AlternativeItem>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">130.00</ItemPrice>

</Item>

</ItemMaintenance>

4.2.3  Scenario: Foodservice Combo (POSLog)

Brief Description

Customer buys a combination meal.
Data

Item sale data, including:

  An identifier for the kit item being sold.
  The normal unit price for the kit item being sold.

Substitution data, including:

  An identifier for the item being removed from the kit item.
  The monetary amount the item being removed contributes to the kit price.
  An identifier for the item being added to the kit item.
  The monetary amount the item being added is contributing to the kit price.

Sale ItemType=” ItemCollection
MerchandiseHierarchy Level=”Department
RegularSalesUnitPrice
Standard item and price Data
Kit
Member Action=”IsPartOf,
IsRemovedFrom, AddsTo
Need flag to indicate one can not change any
of the items in this kit

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 32

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Figure 12: Foodservice Combo (POSLog)
Page 33

ARTS XML Item Maintenance Technical Specification V1.3.2

4.2.3 Conformance XML Instance Document – Foodservice Combo (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="ItemCollection" KitOnlyFlag="false" Action="ChangeItem">

<ItemID Type="SKU">12345678</ItemID>
<MerchandiseHierarchy Level="Department">Men's Clothing </MerchandiseHierarchy>
<ItemPrice Currency="USD" ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>
<Kit Action="IsPartOf" ModifiableFlag="true">

<Members>

<!-- Hamburger -->
<ItemID Type="SKU">23</ItemID>
<!-- Fries -->
<ItemID Type="SKU">87</ItemID>
<!-- Coke -->
<ItemID Type="SKU">ad</ItemID>

</Members>

</Kit>

</Item>

</ItemMaintenance>

4.2.4  Scenario: Identify the kit to which this item is a part.

Brief Description

Customer has all 3 items in a kit at the checkout stand.  When the third item is scanned,
the kit is recognized.
Data

Item sale data, including:

  An identifier for the kit item being sold.
  The normal unit price for the kit item being sold.

Sale ItemType=” ItemCollection
MerchandiseHierarchy Level=”Department
RegularSalesUnitPrice
Standard item and price Data
Parent item id

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 34

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 13: Identify the kit to which this item is a part

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 35

ARTS XML Item Maintenance Technical Specification V1.3.2

4.2.4 Conformance XML Instance Document — Identify the kit to which this item is
a part.
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Straw Broom -->
<ItemID Type="SKU">12345678</ItemID>
<MerchandiseHierarchy Level="Department">Men's Clothing </MerchandiseHierarchy>
<!-- part of Cleaning Kit -->
<ParentItemID Type="SKU">486</ParentItemID>
<ItemPrice Currency="USD" ValueTypeCode="RegularSalesUnitPrice">2.60</ItemPrice>

</Item>

</ItemMaintenance>

4.3  Use Case: Item Purchase & Return with deposit (POSLog)

Brief Description

Many items are sold in a container that has a deposit. This deposit is included in the retail
price of the item, and is refunded to the customer when the empty container is returned.
Examples include soft drink bottles & crates, bread crates, milk bottles & crates, etc. The
examples in this use case use a wooden crate holding 12 bottles of beer, to show how an
item with multiple deposits would be handled.

4.3.1  Scenario: Purchase Crate of Beer with Empties (POSLog)

Brief Description

Customer brings a wooden crate containing 12 empty beer bottles, and purchases another
wooden  crate  containing  12  full  bottles  of  beer.    Customer  does  not  have  to  pay  any
deposit on the crate & bottles, because he is returning a complete set.
Data

Item sale data for the full crate of beer, including:
  An identifier for the item being sold.
  The unit price for the item being sold.

Item return data for the wooden crate and the 12 bottles, including:

  An identifier for the items being returned.
  The unit price for the empties being returned.

Sale ItemType=” Stock
Description
Quantity UnitOfMeasureCode=”Crate of 12
@DepositFlag
Deposit Item
Common Item and Price Data

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 36

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 14: Purchase Crate of Beer with Empties (POSLog)
Page 37

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

ARTS XML Item Maintenance Technical Specification V1.3.2

4.3.1 Conformance XML Instance Document — Purchase Crate of Beer with
Empties (POSLog)
 NOTE: in this example, the deposit is for both the bottles and the crate.
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item DepositFlag="true" Action="ChangeItem">

<!-- New Zealand Crate of Beer -->
<ItemID Type="SKU">1234</ItemID>
<MerchandiseHierarchy Level="Department">Liquor</MerchandiseHierarchy>
<Deposit>

<Amount Currency="USD">3.14</Amount>

</Deposit>
<ItemPrice Quantity="12" UnitOfMeasureCode="EA" ValueTypeCode="RegularSalesUnitPrice"
>3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.4  Use Case: Availability Times

Item only available at a particular time

4.4.1  Scenario: Available to Receive

Brief Description

The store is not allowed to receive the fall fashion collection until August.
Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item &
price Data
Dates:
startavailability
date/time

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 38

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 15: Available to Receive

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 39

ARTS XML Item Maintenance Technical Specification V1.3.2

4.4.1 Conformance XML Instance Document — Available to Receive
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock" StatusCode="Pending" Action="ChangeItem">

<!-- Fall Fashion Shirt -->
<ItemID Type="SKU">2345</ItemID>
<Dates>

<Accessibile TypeCode="Receive" Action="Start">

<Date>1967-08-13</Date>
<Time>14:20:00-05:00</Time>

</Accessibile>

</Dates>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.4.2  Scenario: Available to Order

Brief Description

The store manager can order the Christmas gifts starting in June.
Data

Item:

  An identifier for the items.
  The unit price for the item.

Description

Name
Common item &
price Data
Dates:
startavailability
date/time

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 40

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Figure 16: Available to Order
Page 41

ARTS XML Item Maintenance Technical Specification V1.3.2

4.4.2 Conformance XML Instance Document — Available to Order
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock" StatusCode="Pending" Action="ChangeItem">

<!-- Fall Fashion Shirt -->
<ItemID Type="SKU">2345</ItemID>
<Dates>

<Accessibile TypeCode="Order" Action="Start">

<Date>1967-08-13</Date>
<Time>14:20:00-05:00</Time>

</Accessibile>

</Dates>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.4.3  Scenario: Available to Sale

Brief Description

Next children’s book in the series is available to sale starting at midnight.
Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common Item and
Price Data
ConsumerAvailability
Start date time

Note:Need to extend schema to have start and end date/time
(currently just has one)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 42

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 43

Figure 17: Available to Sale

ARTS XML Item Maintenance Technical Specification V1.3.2

4.4.3 Conformance XML Instance Document — Available to Sale
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock" StatusCode="Active" Action="ChangeItem">

<!-- Fall Fashion Shirt -->
<ItemID Type="SKU">2345</ItemID>
<Dates>

<Accessibile TypeCode="Consumer" Action="Start">

<Date>1967-08-13</Date>
<Time>14:20:00-05:00</Time>

</Accessibile>

</Dates>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.4.4  Scenario: Available to End Sale

Brief Description

Seasonal merchandise is not available for sale after midnight tonight.
Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common Item and
Price Data
ConsumerAvailability
End date time

Note schema needs to be extended to have start and end date/time

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 44

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 18: Available to End Sale

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 45

ARTS XML Item Maintenance Technical Specification V1.3.2

4.4.4 Conformance XML Instance Document — Available to End Sale
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit Name="String" TypeCode="RetailStore">String</BusinessUnit>
<Item ItemCategory="Stock" StatusCode="Active" Action="ChangeItem">

<!-- Fall Fashion Shirt -->
<ItemID Type="SKU">2345</ItemID>
<Dates>

<Accessibile TypeCode="Consumer" Action="End">

<Date>1967-08-13</Date>
<Time>14:20:00-05:00</Time>

</Accessibile>

</Dates>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.4.5  Scenario: Available to Return End date/time for consumer

Brief Description

The consumer is allowed to return the item only until a specified date time. Not allowed
to return Christmas decorations after January 10.

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item &
price Data
Dates:
ReturnavailabilityEnd
date/time

New schema element required to control absolute date/time after
which the item cannot be returned by the consumer (This does not
cover a ’30 days to return’ policy)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 46

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 19: Available to Return End date/time for Consumer

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 47

ARTS XML Item Maintenance Technical Specification V1.3.2

4.4.5 Conformance XML Instance Document — Available to Return End date/time
for Consumer
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock" StatusCode="Active" Action="ChangeItem">

<!-- Fall Fashion Shirt -->
<ItemID Type="SKU">2345</ItemID>
<Dates>

<Accessibile TypeCode="ConsumerReturn" Action="End">

<Date>1967-08-13</Date>
<Time>14:20:00-05:00</Time>

</Accessibile>

</Dates>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.4.6  Scenario:  Available  to  Return  End  date/time  for  reverse
logistics

Brief Description

The retailer is allowed to return the item to the supplier/distributor only until a specified
date time. Not allowed to return Christmas decorations after January 10.

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item &
price Data
Dates:
RetailerReturnavailab
ilityEnd date/time

New schema element required to control absolute date/time after
which the item cannot be returned by the consumer (This does not
cover a ’30 days to return’ policy)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 48

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 20: Available to Return End date/time for Reverse Logistics

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 49

ARTS XML Item Maintenance Technical Specification V1.3.2

4.4.6 Conformance XML Instance Document — Available to Return End date/time
for Reverse Logistics
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock" StatusCode="Active" Action="ChangeItem">

<!-- Chirstmas Decorations -->
<ItemID Type="SKU">2345</ItemID>
<Dates>

<Accessibile TypeCode="RetailerReturn" Action="End">

<Date>1967-08-13</Date>
<Time>14:20:00-05:00</Time>

</Accessibile>

</Dates>

</Item>

</ItemMaintenance>

4.5  Use Case: Display Item Names and/or Descriptions

4.5.1  Scenario: Display Item Names in Different Languages for
Both the Customer and Operator

Brief Description

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item and
price Data
DisplayType
Description

The complex type description (also common data element) has
Language field

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 50

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 21: Display Item Names in Different Languages

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 51

ARTS XML Item Maintenance Technical Specification V1.3.2

4.5.1 Conformance XML Instance Document — Display Item Names in Different
Languages for Both the Customer and Operator
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<ItemID Type="SKU">2345</ItemID>
<Display Language="eng">
<Name>Shirt</Name>
<ShortName>Shirt</ShortName>
<Description Language="eng">Cowboy Shirt</Description>
<ShelfLabel Format="String">Shirt</ShelfLabel>

<TradeItemDescription>123456789012345678901234567890123456789012345678901234567890123
45678901234567890123456789012345678901234567890123456789012345678901234567890123</Trade
ItemDescription>
</Display>

</Item>

</ItemMaintenance>

4.5.2  Scenario: Display Item Names in Different Languages for
the Various Receipt Format

Brief Description

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item and
price Data
DisplayType
Description

The complex type description (also common data element) has
Language field

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 52

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 22: Display Item for Receipts in Different Language

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 53

ARTS XML Item Maintenance Technical Specification V1.3.2

4.5.2 Conformance XML Instance Document — Display Item Names in Different
Languages for the Various Receipt Format
<?xml version=”1.0” encoding=”UTF-8”?>
<ItemMaintenance

xmlns=”http://www.nrf-arts.org/IXRetail/namespace/”
xmlns:xsi=”http://www.w3.org/2001/XMLSchema-instance”
xsi :schemaLocation= »http://www.nrf-arts.org/IXRetail/namespace/ ItemMaintenance.xsd »>
<Item ItemCategory=”Stock” Action=”ChangeItem”>

<ItemID Type=”SKU”>2345</ItemID>
<Display Language=”eng”>
<Name>Shirt</Name>
<ShortName>Shirt</ShortName>
<Description Language=”eng”>Cowboy Shirt</Description>

<ShelfLabel Format="String">Shirt</ShelfLabel>

<TradeItemDescription>123456789012345678901234567890123456789012345678901234567890123
45678901234567890123456789012345678901234567890123456789012345678901234567890123</Trade
ItemDescription>

</Display>

</Item>

</ItemMaintenance>

4.5.3  Scenario: Device Specific Messages

Brief Description

Different I/O devices have different capabilities. Scales may have different capabilities
than a POS receipt. Electronic shelf labels.

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item and
price Data
DisplayType

Need to include description common data (shared with PCM)

Item communicates the different description types; the application has to know which

one to use.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 54

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 23 : Device Specific Messages

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 55

ARTS XML Item Maintenance Technical Specification V1.3.2

4.5.3 Conformance XML Instance Document — Device Specific Messages
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<ItemID Type="SKU">4563456</ItemID>
<Display Language="eng">
<Name>Purse</Name>
<Description Language="eng">Fancy Purse</Description>
<Device>Customer Receipt</Device>

<TradeItemDescription>123456789012345678901234567890123456789012345678901234567890123
45678901234567890123456789012345678901234567890123456789012345678901234567890123</Trade
ItemDescription>
</Display>

</Item>

</ItemMaintenance>

4.6  Use Case: Identify Sales Restricted Items

Identify sales restricted items and the rules associated with them. Sell cigarettes to
someone over 18 but liquor to someone over 21 (including the operator’s age)

4.6.1  Scenario: Time and Date Restrictions

Brief Description

Can’t sell liquor before 1pm on Sundays.

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name
Common item and
price data
New Schema element
in DateType

Description

Need to be able to express time of day restrictions and day of week
restrictions and combination of the two. (meant to express a
recurring schedule)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 56

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 24: Time and Date Restrictions

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 57

ARTS XML Item Maintenance Technical Specification V1.3.2

4.6.1 Conformance XML Instance Document — Time and Date Restrictions
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Ricks Home Brew -->
<ItemID Type="SKU">234</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>
<SellingRules>

<DateTimeRestriction Day="Sunday" When="Between">

<Span>

<StartEndDate>1967-08-13</StartEndDate>
<StartTime>00:00:00-00:00</StartTime>
<EndTime>13:00:00-00:00</EndTime>

</Span>

</DateTimeRestriction>

</SellingRules>

</Item>

</ItemMaintenance>

4.6.2  Scenario: License Restrictions

Brief Description

Fred is required to have a license to sell drugs in the pharmacy.

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 58

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 25 : License Restrictions

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 59

ARTS XML Item Maintenance Technical Specification V1.3.2

4.6.2 Conformance XML Instance Document — License Restrictions
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Aspirin -->
<ItemID Type="SKU">1234</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>
<SellingRules>

<LicenseRestriction>Pharmacist</LicenseRestriction>

</SellingRules>

</Item>

</ItemMaintenance>

4.6.3  Scenario: Quantity Restrictions

Brief Description

Allowed to sell no more than X of this item in a transaction

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item and
price data
Limited quantity

In Selling Rules type

Note that the price schema should be able to express quantity restrictions associated

with promotions.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 60

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 26 : Quantity Restrictions

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 61

ARTS XML Item Maintenance Technical Specification V1.3.2

4.6.3 Conformance XML Instance Document — Quantity Restrictions
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock"  Action="ChangeItem">

<!-- Socks -->
<ItemID Type="SKU">2345</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>
<SellingRules>

<LimitedQuantity Range="Maximum">10</LimitedQuantity>

</SellingRules>

</Item>

</ItemMaintenance>

4.6.4  Scenario: Tender Restrictions

Brief Description

WIC tender can only be applied against eligible items in the transaction

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item and
price data
WICEligibilityFlag

In Selling Rules Type

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 62

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 27 : Tender Restrictions

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 63

ARTS XML Item Maintenance Technical Specification V1.3.2

4.6.4 Conformance XML Instance Document — Tender Restrictions
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Diapers -->
<ItemID Type="SKU">1234</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>
<SellingRules WICEligibilityFlag="true"/>

</Item>

</ItemMaintenance>

4.6.5  Scenario: Purchaser Age Restrictions

–  Purchaser must be over 21 to purchase alcohol.

Brief Description

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item and
price data
MinimumPurchaser
Age

In selling rules type. Need to rename element to make use more
explicit (was minimum age)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 64

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 28: Purchaser Age Restriction

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 65

ARTS XML Item Maintenance Technical Specification V1.3.2

4.6.5 Conformance XML Instance Document – Purchaser Age Restrictions
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Ricks Home Brew  -->
<ItemID Type="SKU">2345</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice" >3.14</ItemPrice>
<SellingRules>

<MinimumPurchaserAge>21</MinimumPurchaserAge>

</SellingRules>

</Item>

</ItemMaintenance>

4.6.6  Scenario: Seller Age Restrictions

–  POS operator must be over 21 to sell alcohol.

Brief Description

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common item and
price data
MinimumWorker
Age

New element required In selling rules type (may be common data
with WFM)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 66

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 29: Seller Age Restrictions

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 67

ARTS XML Item Maintenance Technical Specification V1.3.2

4.6.6 Conformance XML Instance Document – Seller Age Restrictions
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<ItemID Type="SKU">1243</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>
<SellingRules>

<MinimumWorkerAge>18</MinimumWorkerAge>

</SellingRules>

</Item>

</ItemMaintenance>

4.7  Use Case: Assembly Instructions

4.7.1  Scenario: Print Recipe on Receipt

Brief Description

Buy this item get a recipe printed on receipt

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common Item and
Price data
DocumentDisplayID

In DisplayType

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 68

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 30: Print Recipe on Receipt

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 69

ARTS XML Item Maintenance Technical Specification V1.3.2

4.7.1 Conformance XML Instance Document — Print Recipe on Receipt
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Cake -->
<ItemID Type="SKU">2345</ItemID>
<Display Language="eng">

<Name>Cake Recipe</Name>
<DocumentDisplayID>Cook Cake at 350 Degrees</DocumentDisplayID>

<TradeItemDescription>123456789012345678901234567890123456789012345678901234567890123
45678901234567890123456789012345678901234567890123456789012345678901234567890123</Trade
ItemDescription>
</Display>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.7.2  Scenario: Sell item that requires assembly

Brief Description

Sell item that requires assembly

Data

Item:

  An identifier for the items.
  The unit price for the item.

Name

Description

Common Item and
Price data
AssemblyRequiredFl
ag
DocumentDisplayID

New attribute, boolean

In DisplayType

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 70

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Figure 31: Identify Assembly Instructions
Page 71

ARTS XML Item Maintenance Technical Specification V1.3.2

4.7.2 Conformance XML Instance Document – Identify Assembly Instructions
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item AssemblyRequiredFlag="true" ItemCategory="Stock" Action="ChangeItem">

<!-- Bike -->
<ItemID Type="SKU">12345</ItemID>
<Display Language="eng">

<Name>Bike Assembly Instructions</Name>
<DocumentDisplayID>sdfg</DocumentDisplayID>

<TradeItemDescription>123456789012345678901234567890123456789012345678901234567890123
45678901234567890123456789012345678901234567890123456789012345678901234567890123</Trade
ItemDescription>
</Display>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.8  Use case: Item return (POSLog)

Items  are  returned  to  a  retailer  for  various  reasons,  and  the  return  process  may  be
conducted  over  the  www  or  via  a  Tele-Sales  center.  The  scenarios  in  this  use-case
illustrate  the  fact  that  the  resultant  XML  follows  the  pattern  established  by  the  sale  of
items via the various channels.

(reference use cases around time restrictions for return time restriction scenario)

4.8.1  Scenario: Return to Store (POSLog)

Brief Description

Customer returns an item to a store, gets a refund

Common item and price
ReturnableFlag
Restockingfee

Optional element

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 72

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Figure 32: Return to Store (POSLog)
Page 73

ARTS XML Item Maintenance Technical Specification V1.3.2

4.8.1 Conformance XML Instance Document — Return to Store (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ItemCategory="Stock" RestockableFlag="true" Action="ChangeItem">

<!-- Living Room Couch -->
<ItemID Type="SKU">32456</ItemID>
<RestockingFee Currency="USD">31.50</RestockingFee>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">315.00</ItemPrice>

</Item>

</ItemMaintenance>

4.9  Use case: Gift Certificate Purchase (POSLog)

For most retailers Gift Certificates, Money Order, Stored Value Card or Voucher are not
items, so the sale of a Gift Certificate must explicitly state that the transaction is selling a
Gift Certificate rather than an Item.

Common item and price data
Activationflag

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 74

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 33: Gift Certificate Purchase (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 75

ARTS XML Item Maintenance Technical Specification V1.3.2

4.9 Conformance XML Instance Document — Gift Certificate Purchase (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item ActivationRequiredFlag="false" ItemCategory="Stock" Action="ChangeItem">

<!-- Gift Certificate -->
<ItemID Type="SKU">asdf12345</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.10  Use case: Item Purchase on Backorder (POSLog)

When  a  Customer  wishes  to  purchase  an  item  that  is  temporarily  out  of  stock  a  Back-
Order is entered at the POS, the customer may pay some of or the entire purchase price of
the item as a deposit. When the item is back in stock, arrangements will be made for the
customer to complete the purchase.

4.10.1  Scenario: Back-Order

Brief Description

Customer wishes  to purchase  an item that is temporarily out of  stock.  A Back-Order is
entered in at the POS; the customer may pay some or the entire purchase price of the item
as a deposit.

Common item and price data
Backorderflag

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 76

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 34: Back-Order Domain Model

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 77

ARTS XML Item Maintenance Technical Specification V1.3.2

4.10.1 Conformance XML Instance Document — Back-Order (POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item CustomerOrderFlag="true" ItemCategory="Stock" Action="ChangeItem">

<!-- Red Shirt -->
<ItemID Type="SKU">2345</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.10.2  Scenario: Back-Order for Delivery (POSLog)

Brief Description

Customer wishes  to purchase  an item that is temporarily out of  stock.  A Back-Order is
entered in at the POS; the customer may pay some or the entire purchase price of the item
as a deposit. When the item is back in stock, fulfillment will arrange for the item to be
delivered to the customer.

Common item and price
@DeliverableType

1)  Not deliverable
2)  Can be delivered
3)  Must be delivered

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 78

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 35: Back-Order for Delivery (POSLog)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 79

ARTS XML Item Maintenance Technical Specification V1.3.2

4.10.2 Conformance XML Instance Document — Back-Order for Delivery
(POSLog)
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<Item CustomerOrderFlag="true" DeliverableType="CanBeDelivered" ItemCategory="Stock"

Action="ChangeItem">

<ItemID Type="SKU">String</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

4.11  Use Case: Pseudo-Production (V1 if selling end item)

4.11.1  Scenario:  Item  Transformation  from  Bulk  to  Individual
items

Brief Description

Cut side of beef into steaks, hamburger, …
Data

Item data, including:
Name

Description

Common item and
price data
ComponentID

New schema element(0..*), counterpart to ParentID.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 80

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 36: Item Transformation from Bulk to Individual items

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 81

ARTS XML Item Maintenance Technical Specification V1.3.2

4.11.1 Conformance XML Instance Document — Item Transformation from Bulk to
Individual items
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Side of Beef -->
<ItemID Type="SKU">2345</ItemID>
<!-- Steaks -->
<ComponentID Type="SKU">089098</ComponentID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">314</ItemPrice>

</Item>

</ItemMaintenance>

4.11.2  Scenario: Utilize recipe to create Items

Brief Description

Take pickle and put it into a hamburger

Data

Item data on the pickle
Name
Common item and
price data
ParentID

Description

On the recipe element items

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 82

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 37: Explode Recipe to Items

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 83

ARTS XML Item Maintenance Technical Specification V1.3.2

4.11.2 Conformance XML Instance Document — Explode Recipe to Items
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Pickle -->
<ItemID Type="SKU">2345</ItemID>
<!-- Hamburger -->
<ParentItemID Type="SKU">657856</ParentItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">.14</ItemPrice>

</Item>

</ItemMaintenance>

4.11.3  Scenario: Equipment That Can Affect the End Product.

Brief Description

Print job on which printer changes the cost.

The item needs to specify which other items can be used in conjunction with this item

Data

Item data, including:
Name
Common item and
price data
AssociatedItemID

Description

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 84

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 38: Equipment That Can Affect the End Product.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 85

ARTS XML Item Maintenance Technical Specification V1.3.2

4.11.3 Conformance XML Instance Document — Equipment That Can Affect the
End Product.
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">
<Item ItemCategory="Stock" Action="ChangeItem">

<!-- Black and White Printer -->
<ItemID Type="SKU">345643</ItemID>
<AlternativeItem Action="Substitute">

<!-- color plotter -->
<ItemID Type="SKU">09870987</ItemID>
<AdjustmentAmount TypeCode="IncreaseAmount">3.14</AdjustmentAmount>

</AlternativeItem>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</ItemMaintenance>

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 86

ARTS XML Item Maintenance Technical Specification V1.3.2

5.  USE CASE: UPDATE MULTIPLE ITEMS

  Multiple item update notification from item management system to consuming

system

Brief Description

Data

Data Hierarchy Diagram

5.1  Scenario: Update several items, Delete several, Add several

Brief Description

The retailer wishes to update several items on the POS in a single batch/XML instance
document, delete a few others and add new items

Description

New element, common data, name and level (eg New York store,
store level or Western Region, region level)

Data

Name
IM
Batch ID
Batch Description
Execution Date/Time
Location

Item
Actioncode
Common item and
price data
Attributes specific to
the individual updates

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 87

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 39: Update several items, Delete several, Add several
Page 88

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

ARTS XML Item Maintenance Technical Specification V1.3.2

5.1 Conformance XML Instance Document – Update several items, Delete several,
Add several
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../Schema/ItemMaintenanceV1.3.2.xsd"
 xmlns="http://www.nrf-arts.org/IXRetail/namespace/">

<BusinessUnit Name="My Special Store" TypeCode="RetailStore">100</BusinessUnit>
<Batch>

<BatchID>1</BatchID>
<ExecutionDateTime>2001-12-17T09:30:47-05:00</ExecutionDateTime>
<Item ItemCategory="Stock" Action="DeleteItem">

<!-- Summer Shirt -->
<ItemID Type="SKU">3456</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>
<Item ItemCategory="Stock" Action="AddItem">

<!-- Winter Shirt -->
<ItemID Type="SKU">45634</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>
<Item ItemCategory="Stock" Action="DeleteItem">

<!-- Summer Shorts -->
<ItemID Type="SKU">2345234</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>
<Item ItemCategory="Stock" Action="AddItem">

<!-- Winter Pants -->
<ItemID Type="SKU">345435</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>

</Item>

</Batch>

</ItemMaintenance>

6.  USE CASE: TAX (POSLOG) LATER VERSION EXCEPT WHERE
NOTED:

Brief Description

Customer selects one or more items and purchases them with various tenders.
Data



Item sale data, including:
  An identifier for the item being sold.
  The number of multiples of the item being sold.
  Unit price for the item being sold.
  The extended amount (i.e. Unit price * the number of items being sold)

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 89

ARTS XML Item Maintenance Technical Specification V1.3.2

6.1  Scenario: Sell item which is subject to tax

Brief Description:

Sell item which is subject to one or more tax authorities
Minimal piece of information is Tax Group ID
Data

Name

Description

Common item and
price data
Tax common data

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 90

ARTS XML Item Maintenance Technical Specification V1.3.2

Data Hierarchy Diagram

Figure 40: Sell item which is subject to tax

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 91

ARTS XML Item Maintenance Technical Specification V1.3.2

6.1 Conformance XML Instance Document – Sell item which is subject to tax
<?xml version="1.0" encoding="UTF-8"?>
<ItemMaintenance xmlns="http://www.nrf-arts.org/IXRetail/namespace/"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/

../Schema/ItemMaintenanceV1.3.2.xsd">

<Item ItemCategory="Stock" Action="ChangeItem">

<ItemID Type="SKU">String</ItemID>
<ItemPrice ValueTypeCode="RegularSalesUnitPrice">3.14</ItemPrice>
<TaxInformation TaxType="Sales">
<TaxGroupID>D</TaxGroupID>
<TaxPercent>10</TaxPercent>

</TaxInformation>

</Item>

</ItemMaintenance>

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 92

ARTS XML Item Maintenance Technical Specification V1.3.2

7.  SCHEMA IMPLEMENTATION

ItemMaintenance.xsd – core item data

Common Data.xsd – data common to more than one schema
CountryCode.xsd – Country Code enumeration
CurrencyCode.xsd – Currency Code enumeration
LanguageCode.xsd – Language Code enumeration
ServiceLevelCode.xsd – Service Level enumeration
UnitOfMeasureCode.xsd – Unit Of Measure enumeration

Version 1.2.1
Chairman:
Tim Hood

Members:
Tim Hood
Richard Halter
Monty Moncreif
Frank May
Loenid Rubakhin
Dave Van Horne
Ronald McEvoy
Maroun Atallah
Rainer Kramer
Dave Parr
Alan Lipson
Peter Rush
Ronald Scholz
Maria Borelli
Jerry Rightmer
Warren Backer
Dave Moorman
H Paul Gay

Contributors:
Jay Heavilon
John Hervey
Doug Jones
Stuart McGrigor
John Fluke
Julia Rockwell

Triversity, Inc.

Triversity
MIC
Blockbuster
Microsoft
NSB-STS
Softechniques
Soft Solutions Co.
Soft Solutions Co.
Wincor Nixdorf International Gmbh
Unipower Solutions Europe Ltd.
Hewlett-Packard
Harrods Limited
GK Software AG
Logware
360 Commerce
Target
PCMS Datafit
Epson

Mars Interactive
PCATS
Target
ARTS
IBM
IBM

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 93

ARTS XML Item Maintenance Technical Specification V1.3.2

8.  DOCUMENT HISTORY

Version History

Ver
1
1.0.1

Date
12-21-2004  All
12-16-2005  All

Sections  Description of Change

Initial Release

-
-  Fixed problems with Common Data
-  Added Extension Point to ItemType

complex type

-  Added Extension Point to DisplayType
-  Added AlternativeItemID to ItemType to
allow the reporting of multiple id’s from
Home Office.

-  Move @RelativeOrder from Territory to

Deposit.

-  Changed TradeItemDescription length to

143 characters.

-  Changed  Group Cardinality to

repeatable

-  Corrected spelling of TaxedAtDestination
enumeration in TaxAtOrigin attribute

1.0.1   05-19-2006  All

-  Removed non-core elements from use

1.2.0

6-12-2006

Schema

cases/scenario examples.

-  Made Description repeatable in Display
Type to allow for multiple languages

-  Added TypeCode to Description

Common Data with enumeration Short,
Long, Web, Supplier

-  Made Description repeatable in

KitCommonData to allow for multiple
languages

-  Added SupplierID to OrderInformation to
synchronize with the ARTS datamodel
-  Added NameAndAddressRequiredFlag
to ItemUnitIndicatorType to indicate a
name and address is required for this
item

1.2.1

2-28-2007

Schema

-  Made SupplierInformation element

1.3.0

12-25-2011

repeatable to match the domain model
-  Relaxed requirement for height, width
and depth in item measurements
common data.

-  Updated in conjunction with Self-Service

Order Interface

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 94

ARTS XML Item Maintenance Technical Specification V1.3.2

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 95

ARTS XML Item Maintenance Technical Specification V1.3.2

9.  GLOSSARY

@ - identifies attributes (XPath nomenclature)
Italics indicate default value
Term
ItemMaintenance
BusinessUnit
Item
ItemType
ItemID

Definition
IXRetail Item Maintenance Schema
extension base="BusinessUnitCommonData default RetailStore
ItemType" maxOccurs="unbounded

extension base="ItemIDType
The retailers SKU or unique item identifier for items sold or
returned
Allows the reporting of multiple itemid's for a single item from
Head office, for example both the SKU and the barcode.  One is
the main and reported as the ItemID above, the others are
reported here
type="ItemUnitIndicatorType" minOccurs="0
extension base="ItemIDCommonData
If this item is part of a kit, this indicates the parent item.  This is
useful if this item can be sold individually or as a part of a kit and
discount pricing is applied as a part of a kit
EAN.UCC Definition: Indicates the trade item identification of an
item that is being permanently replaced by this trade item.
Examples: "01234567890128"
Business Rules: The trade item identification that is being
permanently replaced must already be in the home data pool in
order to ensure data integrity. The old trade item identification
specified in this field should be discontinued.
extension base="ItemIDCommonData
Indicates the fee that should be applied when an item is returned
extension base="MonetaryAmountCommonData
type="xs:decimal" minOccurs="0"/>
Default number of individual units in a transaction at the time of
sale, for example 6 for a 6 pack. Or 2 speakers
This code defines how this item may be used within a store.
Usage is a function of how an item may be consumed or
disposed of by the store
type=AdditionalItemsType
type=AlternativeItemType
type =ApparelItemType
type="AssemblyInstructionsType
" type="BrandOwnerType
type="BulkType
type="ColorCodeType
type="CommissionType
type="CouponType
type="DatesType
extension base="AmountCommonData
type="DisplayType
type="FuelGradeType
type="FuelProductType

AlternativeItemID

ItemUnitIndicator
ParentItemID

ReplacedItemID

RestockingFee

SellingUnits

UsageCode

AdditionalItems
AlternativeItem
ApparelItem
AssemblyInstructions
BrandOwner
Bulk
Color
Commission
Coupon
Dates
DepositAmount
Display
FuelGrade
FuelProduct

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 96

ARTS XML Item Maintenance Technical Specification V1.3.2

FuelPosition
Group
Handling
HazardousInformation
InformationProvider
ItemMeasurements
ItemPalletHierarchy
ItemPrice
Kit
Lot
Manufacturer
Marketing
MerchandiseHierarchy
MixMatch
OrderInformation
OrganicCharacteristics
Pack
Packaging
PalletInformation
PreparedItem
SellingLocation
SellingRules
ServiceItem
ShelfInformation
Size
StockItem
Style
SupplierInformation
TankProduct
TargetMarket
TaxInformation
TemperatureInformation
Warranty
Waste
@ Action

type="FuelPositionType
type="GroupType
type="HandlingType
type="HazardousInformationType
type="InformationProviderIDType
type="ItemMeasurementsType
type="ItemPalletHierarchyType
type="ItemPriceType
type="KitType
type="LotType"
type="ManufacturerType
type="MarketingType
extension base="MerchandiseHierarchyCommonData
type="MixMatchType
type="OrderInformationType
type="OrganicCharacteristicsType
type="PackType
type="PackagingType
type="PalletInformationType
type="PreparedItemType
type="StoreStructureType
type="SellingRulesType
type="ServiceItemType
type="ShelfInformationType
type="SizeCodeType
type="StockItemType
" type="StyleCodeType
type="SupplierInformationType
type="TankProductType
type="TargetMarketType
type="TaxInformationType
type="TemperatureInformationType
type="WarrantyType
type="WasteType
type="ItemTypeActions" use="optional" default="ChangeItem

  Add Item
  Change Item

@ ActivationRequiredFlag

@ AllowInLayawayFlag
@ AllowManualWeighFlag
@ AllowQuantityKeyedFlag
@ AuthorizedForSaleFlag

@ CustomerOrderFlag
@
DangerousGoodsAMarginNu
mber

Delete Item
Indicates that the item needs to be activated when sold. The
example would be a stored value card or gift certificate that would
require the POS to send an activation request when the item is
sold.

Indicates whether the quantity of an item is modifiable at the POS
A flag to indicate that the RETAIL STORE is authorized to sell
this particular ITEM.
Indicates whether a customer can order this item
type="DangerousGoodsAMarginNumberTypeCode"
use="optional" default="NotPossible
EAN.UCC Definition: Information, whether for the base trade item
or further packaging trade item a dangerous goods a-margin
number does exist in the European dangerous goods
agreements (and in the respective national dangerous goods

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 97

ARTS XML Item Maintenance Technical Specification V1.3.2

legislation), thus facilitations for the transport of defined limited
quantity by road or rail are possible or not. If they are possible,
they must be indicated, whether they are used by the data
supplier.
Examples: "not possible"
Business Rules: Information required when
dangerousGoodsIndicator equals Y.
Repeatable per dangerousGoodsRegulation code.
List of authorized values :
not possible
possible( but not used)
used (by the data supplier)
Hazardous attributes relate to supply chain handling (e.g.,
transport, storage, handling).</
EAN.UCC Definition: Indication, whether the trade item and/or at
least one of its packaging components because of its properties -
according to the respective national or international legislation for
transport by road, rail, river, sea or air (e.g. the European
dangerous goods agreements (ADR/RID) for transport by road
and rail) - must be classified as dangerous good, and thus is
subject to the respective regulations.
Examples:
Business Rules: Boolean Y/N
Hazardous attributes relate to supply chain handling (e.g.,
transport, storage, handling).
Indicates that deposit is required. Other rules would dictate the
amount of the deposit
Indicates whether this item can be directly ordered from the store
by a customer
Flag to indicate this is part of a promotion
Indicates that food stamps can be used with this item
Definition: Indication, whether the trade item and/or at least one
of its packaging components because of its properties -
according to the respective national or international legislation for
transport by road, rail, river, sea or air (e.g. the European
dangerous goods agreements (ADR/RID) for transport by road
and rail) - must be classified as dangerous good, and thus is
subject to the respective regulations

Item Collection

  Stock
  Service
  Alteration
  Fee
  Deposit
  Deposit Refund
  Tare

Warranty
Indicates whether the drawer needs opened when the item is
referenced during a transaction. An example would be the sale of
postage stamps that are stored in a POS drawer
EAN.UCC Definition: Indicates whether there exists a material
safety data sheet for the trade item. This is a data sheet with the
most important characteristics,  protected measures and
regulations to be adhered to when handling this trade item. It is
relevant above all for dangerous substances.

@ DangerousGoodsFlag

@ DepositFlag

@ DirectOrderFlag

@ DiscountableFlag
@FoodStampFlag
@HazardousItemFlag

@ ItemCategory

@ OpenDrawerFlag

@
MaterialSafetyDataSheetFla
g

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 98

ARTS XML Item Maintenance Technical Specification V1.3.2

@
NonSoldItemReturnableFlag

@PriceEntryRequired

@ PromotionableFlag
@ QuantityRequiredFlag
@ RestockableFlag

@ ReturnableFlag
@ SecondsFlag
@ SecurityRequiredFlag
@ SerialNumberFlag

@ SpecialOrderableFlag
@ StatusCode

@ SubstituteFlag

@ TaxIncludedInPriceFlag
@WeightEntryFlag
@WICFlag

CountryOfOrigin

Business Rules: Boolean Y/N

Information required when dangerousGoodsIndicator equals

Y
EAN.UCC Definition: Indicates that the buyer can return the
articles that are not sold. Used, for example; with magazines and
bread. This is a y/n (Boolean) where y equals right of return. This
is at least relevant to General Merchandise, Publishing industries
and for some FMCG trade item.

Business Rules: This attribute applies to certain industries, and
applies to return of salable goods. This indicator identifies the
general rule, and is not transaction based.
type="PriceEntryRequiredCodes" use="optional"
default="Optional
Indicates whether manual price entry is required for this item

  Required
  Prohibited

Optional
Indicates that this is a promotional item
Indicates a quantity must be entered.
Indicates the inventory disposition of this item when it is returned
(reverse logistics).
Indicates whether this item can be returned
Indicates this is a second - targeted for an outlet store
Indicates this item must be secured, I.e. diamonds
Indicates whether this item has a serial number associated with it
that the operator must enter
Available for special orders
type="ItemStatusCodes" use="optional" default="Active
Item status code for this item; valid codes:
ACTIVE (can be sold at the moment and forever),
INACTIVE (not sold at the moment),
PENDING (not sold at the moment but can be sold after the
effective date and time),
DISCONTINUED (Can not be sold and will never be sold again)
An ITEM for which there is a substitute available for sale within
the RETAIL STORE.
indicates the tax is included, i.e. VAT
Indicates whether a weight entry is required to process this item
Indicates that WIC can be used with this item

EAN.UCC Definition: The country code (codes) in which the
goods have been produced or manufactured, according to criteria
established for the
purposes of application of the value may or may not be presented
on the trade item label.
Examples: "124" = Canada, "840" United States
Business Rules: This information is for customs purpose in case
of
importation or legal requirements regarding customer information
for some categories of trade item (e.g. meats and fruits)
Information can be repeated if multiple countries are valid. In this
case, the buyer will only know the actual country of origin at the
time of delivery. Code list ISO

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 99

ARTS XML Item Maintenance Technical Specification V1.3.2

@ CountryCode
@ CountryName
AdditionalItemsType
ItemID

AlternativeItemType

ItemID

AdjustmentAmount

SubstitutionReasonDescripti
on

@ Action

ApparelItemType

SilhouetteDescription

FabricDescription
Lifestyle

Ornament

Pattern

Material

MaterialIntrinsicType

MaterialPopularFamily

3166-1 code.
type="CountryCode" use="optional" default="US
type="xs:string" use="optional

:extension base="ItemIDType
@ CostInclusiveFlag
@ MaxQuantity type="xs:integer" use="optional" default="1
Items which can be added to the base item up to a point without
charge, i.e. screwdriver with assembly of furniture
extension base="ItemIDType
The alternate item for which this is a substitute or for which can
be substituted for this item

Max Quantity

CostInclusiveFl
ag

The  maximum  free  quantity  of  this  item  befor
charge is incurred
Indicates the cost is included
true

extension base="MonetaryAmountCommonData
@ TypeCode" type="AdjustmentAmountTypeCode"
use="optional" default="EvenExchange
The amount added to the base price to replace the item with this
alternate item.

  Even Exchange


Increase Amount

Decrease Amount
A narrative describing the circumstances under which one item
can be substituted for another.  For instance, one item may be
offered as an alternative in a gift registry scenario, but not in a
clearance or promotional scenario
type="EquivalentItemActionType" use="optional"
default="Substitute

  Substitute (This alternate item may be substituted for the

original item)

Substituted for (the original item may be substituted for this
alternate item)
A cross reference of items that may be substituted or offered in
place of the base item
Describes the cut or fit of the APPARELL ITEM. For example,
shirts may be sold as slim or standard fit
Describes the material used to make the APPAREL ITEM
extension base="LifestyleIDCommonData
Lifestyle code for this item
A decorative detail that may be created on a Component (e.g.
monogram on a Pocket) for a Style.
An optional classification of a Style as a solid, broad stripe,
narrow stripe, plaid, floral print, tropical print, geometric shape,
etc
A specific substance used to manufacture products (garments,
shoes, jewelry, etc) sold,  e.g. cotton, wool, silk, canvas, gold,
silver. Cotton, wool, silk and canvas would belong to the Fabric
family, while gold and silver would belong to the Metal (precious
or semi-precious) family
A grouping of materials based on their intrinsic constitution, e.g.
natural vs. man-made (or synthetic)
An optional grouping of materials based on popular
characteristics, e.g. Egyptian Cotton.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 100

ARTS XML Item Maintenance Technical Specification V1.3.2

MaterialType

Weave

WeaveDescription
CollectionName

CollectionCreationDate

AssemblyInstructionsType
BrandOwnerType

BulkType
BulkToSellingUnitWasteType
Code
BulkToSellingUnitWasteFact
orPercent
ChildOfTradeItem
QuantityOfNextLowerLevelTr
adeItem

ChildTradeItem

ColorCodeType

A grouping of materials based on their primary characteristics,
e.g. Fabric, Leather, Precious Metal, Stone, Blend
A process used to form fabric on a loom which determines the
strength and surface of the fabric, e.g. twill, satin, rib, jacquard,
pile, cable, ribbed, etc
Text which names or describes a particular weave
A merchandising term created by the manufacturer, a title or
description for a Collection
The date that a Collection was first defined.  (season - e.g. Spring
98 that Collection is promoted?)
extension base="DescriptionCommonData
EAN.UCC Definition: Unique location number identifying the
brand owner. May or may not be the same entity as the
information provider, which actually enters and maintains data in
data pools.
Examples: GLN, DUNS_PLUS_FOUR
Business Rules: The brand owner is the source of the data
relating to the trade item, but is not necessarily responsible for
providing and
maintaining the data in the catalogue. This is the responsibility of
the information provider
@ Name" type="xs:string" use="optional
EAN.UCC Definition: Name of the party who owns the brand of
the trade item.
Examples: Manufacturer of branded trade item - Can also be
distributor or retailer that licenses a brand name to various private
label manufacturers.
Business Rules: Mandatory when brandOwner Party
identification is provided

The code to denote the type of waste associated with the BULK
ITEM when breaking down to retail selling units
The pre-defined waste factor percentage, e.g. boning allowance.

from EAN.UCC
EAN.UCC Definition: The number of next lower level trade item
that this trade item contains.
Business Rules: This trade item may repeat if the GTIN of the
lower level configuration repeats (e.g. if a combo-pack (mixed
trade item) such as an assortment of crisps contains both chicken
and cheese packets, the lowest level GTIN is that of each trade
item in the assortment, not the GTIN of the assortment)</
extension base="ItemIDCommonData
EAN.UCC Definition: A reference to the GTIN of the next lower
level of trade item that this trade item contains.
Examples: GTIN "00037000123415" contained in GTIN
00037000123330.
Business Rules: Allowed for more than 1 reference to lower
levels to allow for the registration of Mixed Assortments. The
sequence of entering GTINs is important when a next lower level
GTIN is to be linked. The next lower level GTIN must already
exist, therefore the order of trade items to be entered should be
from lowest to highest e.g. consumer, then intermediate, then
traded, etc
from EAN.UCC

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 101

ARTS XML Item Maintenance Technical Specification V1.3.2

extension base="ColorCodeCommonData

CommissionType
CommissionCode
SpiffCode

CouponType
CouponFamilyCode

@ CouponFlag
@ MultipleFlag
@ GenerateCouponFlag
@
ElectronicCouponAllowedFla
g
DatesType
EffectiveDate

ExpirationDate
StartAvailabilityDateTime

EndAvailabilityDateTime

Employee sales incentive. Refers to the SPIFF code of the SPIFF
record to associate with this item

EAN.UCC Definition: A code assigned by the vendor to a single
trade item or to families of consumer trade items that can be used
by in store scanners in conjunction with a U.P.C. coupon value
code for coupon value discount when the proper trade item has
been purchased.
Business Rules: It only applies to the consumer unit
Indicates that coupons can be used with this item
Indicates whether multiple coupons are allowed on this item
Indicates if the store can issue/generate an  in-store coupon

from EAN.UCC
EAN.UCC Definition: The date on which the information contents
of the master data version are valid. Valid = correct or true. This
effective date can be used for initial trade item offering, or to
mark a change in the information related to an existing trade
item. This date would mark when these changes take effect.
Examples: "2002-02-05" February 5th 2002
Business Rules: This date will be used for version management.
The effective date can be different from publication date. If a new
user begins to synchronize data on this GTIN after the original
effective date, the effective date = the publication date for the
new user. Time zone of the information provider may be noted in
future drafts of the GDD. ISO 8601 date format CCYY-MM-DD

EAN.UCC Definition: The date (CCYY-MM-DDTHH:MM:SS) from
which the trade item becomes available from the supplier,
including seasonal or temporary trade item and services.
Examples: "2002-02-05T17:00:00" February 5th 2002 5:00:00pm
Business Rules: If the trade item is public only one date (CCYY-
MMDDTHH:MM:SS) is valid per GTIN, GLN, TM combination. If
Item is private there can be more than 1 value per TM. Needs to
be earlier than end availability date This date indicates when the
trade item can first be ordered by the buyer from the information
provider. This date can be trading partner dependent if the trade
item or service is defined as private. It is trading partner neutral if
the trade item/service is public. It does not indicate when this
trade item becomes available to the end consumer (see first sale
date) There is only one start availability date per GTIN/GLN/TM
combination. Date format is ISO8601 – CCYY-
MMDDTHH:MM:SS
EAN.UCC Definition: The date from which the trade item is no
longer available from the information provider, including seasonal
or temporary trade item and services.
Examples: "2002-02-05T17:00:00" February 5th 2002 5:00:00pm
Business Rules: If the trade item is public only one date is valid
per GTIN, GLN, TM combination. If Item is private there can be

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 102

ARTS XML Item Maintenance Technical Specification V1.3.2

more than 1 value per TM. There is only one "end availability
date" per GTIN/GLN/TM combination at any given time. In the
case of seasonal trade items, only one start/end cycle can be in
the data set version being synchronized.
Therefore, a trade item cannot have multiple start/stop availability
dates associated with it at any given time. Field is optional since
most trade items are offered in an open ended environment. Is
trading partner neutral for public trade items, trading partner
dependent for private trade items. Date format is CCYY-MM-
DDTHH:MM:SS.
EAN.UCC Definition: The first date/time that the buyer is allowed
to sell the trade item to consumers. Usually related to a specific
geography. ISO 8601 date format CCYY-MM-DDTHH:MM:SS.
Examples: "2002-02-05T17:00:00" February 5th 2002 5:00:00pm
Business Rules: Time is expressed in the time zone of the target
market where the trade item is intended for resale to consumers.
ISO 8601 date format CCYY-MM-DDTHH:MM:SS

type="DiscountEnumeration" use="optional" default="Either
Indicates whether an item can be sold at discount, and if so, how
Enumeration

  NotAllowed
  PercentOnly
  AmountOnly

ConsumerAvailabilityDateTi
me

DiscountType
@DiscountCode

@CustomerDiscountCode

Either
type="DiscountEnumeration" use="optional" default="Either
Indicates  whether  an  item  can  be  discounted  based  on  the
affiliation of the customer purchasing it, and if so, how
Enumeration

  NotAllowed
  PercentOnly
  AmountOnly

@WorkerDiscountCode

Either
type="DiscountEnumeration" use="optional" default="Either
Indicates  whether  an  item  can  be  discounted  if  the  purchaser  is
an employee, and if so, how
Enumeration

  NotAllowed
  PercentOnly
  AmountOnly

@ThresholdDiscountCode

Either
type="DiscountEnumeration" use="optional" default="NotAllowed
Indicates  whether  an  item  can  be  discounted  using  a  threshold
pattern;
Enumeration

  NotAllowed
  PercentOnly
  AmountOnly

@MarkdownCode

Either
type="DiscountEnumeration" use="optional" default="NotAllowed
Indicates  whether  an  item  can  be  marked  down  at  POS,  using
manual discounting
Enumeration

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

  NotAllowed
  PercentOnly
Page 103

ARTS XML Item Maintenance Technical Specification V1.3.2

@BusinessDiscountCode

DisplayType
Name
BrandName

SubBrandName

ShortName

Description

ShelfLabel

DocumentDisplayID

ImageName

  AmountOnly

Either
type="DiscountEnumeration" use="optional" default="Either
Indicates  whether  an  item  can  be  discounted  based  on  the
affiliation of the business purchasing it, and if so, how
Enumeration

  NotAllowed
  PercentOnly
  AmountOnly

Either
Derived from ISO-639-2 Language Codes
The name by which the ITEM is known
A unique name to denote a class of ITEMs as a product of a
single supplier or manufacturer. The brand can include private
label ITEMs.  EAN.UCC Definition: The recognizable name used
by a brand owner to uniquely identify a line of trade item or
services. This is recognizable by the consumer.
Examples: ACME
Business Rules: Free form text field, but not necessarily tied to
language. Brands are more likely to be language independent. If
a trade item does not have a brand, Use ‘unbranded’ in the
description. This is a Mandatory field. If a trade item is changed
from being "Unbranded" to a brand, this requires a new GTIN.
GTIN allocation rules may vary by industry.
EAN.UCC Definition: Second level of brand. Can be a trademark.
It is the primary differentiating factor that a brand owner wants to
communicate to the consumer or buyer. E.g. Yummy-Cola
Classic. In this example Yummy-Cola is the brand and Classic is
the subBrand
EAN.UCC Definition: A free form short length description of the
trade item that can be used to identify the trade item at point of
sale.
Examples: Kel CrnF750g.
Business Rules: Free form text field, this data element is
repeatable for each language used and must be associated with
a valid ISO language code
EAN.UCC Definition: Describes use of the product or service by
the consumer.  Should help clarify the product classification
associated with the GTIN.
Examples: drill, salad dressing, soup, beer.
Business Rules: Free form text field, this data element is
repeatable for each language used and must be associated with
a valid ISO language.
Text to appear on the shelf label (physical or electronic)
@Format - Masking or other information to indicate the format of
the label to be used by the system which generates the label
information (physical or electronic)
A system dependent identifier which is used by the consuming
application to trigger the display of a form or document when the
item is referenced within the consuming application. An example
is a document that is displayed telling the operator to ask for
government identification when a gun is sold. Should be 0..n. In
future versions we may want to try to enumerate common set of
values.
Image name for the item

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 104

ARTS XML Item Maintenance Technical Specification V1.3.2

InvoiceName

TradeItemDescription

TradeItemFormDescription

Variant

@ Language
DisplayUnitType
ShelfItemsHeldCapacityCou
nt
SetupDate

TakeDownDate

@ TypeCode

EAN.UCC Definition: Free form information provider assigned
trade item description designed to match trade item/service
description as noted on invoices.
Business Rules: Free form text field, this data element is
repeatable for each language used and must be associated with
a valid ISO language code from the attached table. Most likely
will include several abbreviations
EAN.UCC Definition: The concatenated product description of a
product or service. See business rules.
Examples*: When a supplier sends all information in maximum
size the retailer will get for example following information: Yummy
Cola_________________________
Yummy______________________________
Drink______________________________ Big
Size__________________________  For automatic use of this
information, e.g. on a tag, a separator should be given between
all elements. E.g: Yummy-Cola; Yummy; Drink; Big Size.
Business Rules*: This field is automatically generated by the
concatenation of the "brand"," sub-brand", "functional name" and
variant. Free form text field, this data element is repeatable for
each language used and must be associated with a valid ISO
language code .
* This is a derived attribute resulting from the concatenation of 4
other attributes of up to 35 characters each (see Business Rules
above). When implemented, these four attributes may be
concatenated as appropriate. Item description is part of the set of
core data that will be stored in the Registry
EAN.UCC Definition: The physical form or shape of the product.
Used, for example, in pharmaceutical industry to indicate the
formulation of the trade item. Defines the form the trade item
takes and is distinct from the form of the packaging.
Examples: "tablet", "powder", "gel", "shredded", "liquid",
"granules"
Business Rules: Optional field that can be used to further
describe a trade item's benefit delivery method. Free form text.
(See examples)
EAN.UCC Definition: Free text field used to identify the variant of
the product. Variants are the distinguishing characteristics that
differentiate products with the same brand and size including
such things as the particular flavor, fragrance, taste.
Examples: Examples: Bananna, Strawberry, Lemon Scented.
Business Rules: This is different from the Global EAN.UCC
product classification variant. Free form text field, this data
element is repeatable for each language used and must be
associated with a valid ISO language code
type="LanguageCode" use="optional" default="eng

The maximum number of SHELF ITEMS that can be stocked on
the DISPLAY UNIT
The date on which the DISPLAY UNIT can be setup within the
RETAIL STORE
The date on which the display unit can be taken down by the
RETAIL STORE
type="DisplayUnitTypeCode –
A code to denote the type of display unit, i.e. free-standing, shelf

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 105

ARTS XML Item Maintenance Technical Specification V1.3.2

@ DispositionCode

FuelGradeType

FuelGradeID
Description
FuelProductID

FuelProductIDHigh

FuelPositionID

MerchandiseHierarchy
FuelPositionType

FuelGradeID
FuelPositionID

TankID

FuelProductType
FuelProductID

Description
GroupType

GroupID

GroupType

TradeItemGroupIdentification
Code

end, refrigerator,  etc
type="DispositionTypeCode
A code to denote how the DISPLAY UNIT is to be disposed, ie
returned to the supplier, destroyed, or retained until the next
promotion
The data to support sale of fuel grades – The wet stock being
dispensed into the retail consumer’s tank
The wet stock being dispensed at this fuel position

The fuel product id for the fuel grade.  If it is a dispenser blended
fuel grade then it is the fuel product id of the fuel product with the
lowest octane in the blend
The fuel product id for the highest-octane fuel in a dispenser
blended product
The physical location where the fuel is dispensed to one vehicle
at a time.
extension base="MerchandiseHierarchyCommonData
The data used to establish the selling parameters for fuel grades
at the fueling position, including time tier, price tier and service
level
The wet stock being dispensed at this fuel position
The physical location where the fuel is dispensed to one vehicle
at a time.
The assigned identification for a fuel product tank.  If it is a
dispenser blended fuel grade then it is the Tank Id of the fuel
product with the lowest octane in the blend

The fuel product id for the fuel grade.  If it is a dispenser blended
fuel grade then it is the fuel product id of the fuel product with the
lowest octane in the blend
Description of the fuel product indicated by the fuel product Id
Much like the datamodel, A group is an abstracted to be just
about anything with some sort of relationship.  With this
concept a kit could be a group or a mix match could be a
group.  These (kit and mix match) are used often enough,
they have their own node.  A group to handle other types of
relationships not definitively identified.
A user defined field used to enable arbitrary grouping of items.
The ID field combined with the type allows the implementation of
mulitple programs of the same type.
A user defined field used to indicate to consuming systems the
type of group. This would allow the consuming application to
determine the context of the group and behave accordingly.
Examples would be Mixmatch, discount, suggestive selling,
prerequisite tools, price optimization, substitution, loyalty
programs, incompatible items, quantity restrictions, time
restrictions, premium eligible item, parking validation
EAN.UCC Definition: A code assigned by the supplier or
manufacturer to logically group trade item independently from the
Global trade item Classification.
Examples: Code representing a group of GTINs for all 501 Blue
Jeans sizes and colors
123=
GTIN1 501 Blue/38

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 106

ARTS XML Item Maintenance Technical Specification V1.3.2

TradeItemGroupIdentification
Description

LinkItem

ProductRange

@ Category
@ TypeCode

HandlingType
HandlingInstructionsCode

StackingFactor

StackingWeightMaximum

GTIN2 501 Blue/40
GTIN3 501 Black/38
GTIN4 501 Black/40
Business Rules: Manufacturer assigned. This code is typically
assigned to multiple GTINs
extension base="DescriptionCommonData
EAN.UCC Definition: The text description of the value
represented by the tradeitemGroupIDCode
Examples: "501 Blue Jeans", represent all sized and colors of this
trade item
Business Rules: If trade itemGroupIDCode is present, description
must be present. A description text field, this data element is
repeatable for each language used and linked to data element
"Description language".
extension base="ItemIDCommonData
The items that are linked to this item and are added to the
transaction when this item is sold. An example would be the
bottle deposit item which would be linked to the beverage item
EAN.UCC Definition: A name, used by a BrandOwner, that span
multiple consumer categories or uses. E.g. (Waist Watchers)
Examples: The waist watcher product range includes salad
dressings, receipt books, kitchen utensils, etc.
type="ItemCategoryTypeCode
type="GroupTypeCodeEnumeration
A user defined field used to indicate to consuming systems the
type of group. This would allow the consuming application to
determine the context of the group and behave accordingly.
Examples would be Mixmatch, discount, suggestive selling,
prerequisite tools, price optimization, substitution, loyalty
programs, incompatible items, quantity restrictions, time
restrictions, premium eligible item, parking validation
from EAN.UCC
EAN.UCC Definition: Defines the information and processes
needed to safely handle the trade item. Handling instructions is
composed of both text and a language code.  The language for
text is specified using the two digit ISO 639-1988 list, for
example, English is EN and French is FR.
Examples:
DNF – Do Not Freeze
“FTD” – Frost danger
“HS” – Heat sensitive
“HWC” – Handle with care
Business Rules: Repeatable values are accepted
EAN.UCC Definition: A factor that determines the maximum
stacking for the product. Indicates the number of levels the
product may be stacked.
Examples: Factor of "2" = trade item is stackable 2 high
Business Rules: Factor will indicate how many levels the
particular product may be stacked in. The counting of the levels
will always commence at 1 not 0
extension base="MeasurementCommonData
Definition: The maximum admissible weight that can be stacked
on the trade item. This uses a measurement consisting of a unit
of measure and a value. This will be used for transport or storage
to allow user to know by weight how to stack different trade item

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 107

ARTS XML Item Maintenance Technical Specification V1.3.2

HazardousInformationType
MaterialSafetyDataSheetNu
mber

ClassOfDangerousGoods

DangerousGoodsHazardous
Code

DangerousGoodsPackingGr
oup

DangerousGoodsRegulation
Code

DangerousGoodsShippingN
ame

one on top of the other.
Business Rules: Used in conjunction with unit of measure.
from EAN.UCC
EAN.UCC Definition: Manufacturer's identification number for the
material safety data sheet for a trade item.
Examples: "4711", "ag34784", "zruifk"
Business Rules: This is an internal number which is distributed by
the manufacturer. Can be in any format. This attribute is
mandatory if the Material Safety Data Sheet attribute is “Y”
EAN.UCC Definition: Dangerous goods classification of the trade
item. There are 9 danger classes, some classes are further
subdivided into subclasses. Class number explains in general
terms the nature and properties of the goods and serves to
classify them together in terms of their most significant risk.
Examples: Class “4.2”: Substances liable to spontaneous
combustion. Class “6.1”: Toxic substances
Business Rules: Information required when
dangerousGoodsIndicator equals Y. Subsidiary risks given by
repeating attribute value. Repeatable per
dangerousGoodsRegulation code. Refer to UNECE code list.
Hazardous attributes relate to supply chain handling (e.g.,
transport, storage, handling).
EAN.UCC Definition: Dangerous goods hazard ID number, which
must be applied to the vehicle, when transporting this trade item
(dangerous good) by road or rail, to inform the police, the fire
brigade and others in case of an accident about the kind of
danger caused by the cargo.
Business Rules: Information required when
dangerousGoodsIndicator equals Y. Repeatable per
dangerousGoodsRegulation code. Hazardous attributes relate to
supply chain handling (e.g., transport, storage, handling)
EAN.UCC Definition: Identifies the degree of risk these
dangerous goods present during transport according to
IATA/IMDG/ADR/RID regulations.
Examples: Group I : Great danger - Packaging meeting criteria to
pack hazardous materials with great danger.
Business Rules: Information required when
dangerousGoodsIndicator equals Y. Repeatable per
dangerousGoodsRegulation code.
http://www.unece.org/trade/untdid/d99b/tred/tred8339.htm
Hazardous attributes relate to supply chain handling (e.g.,
transport, storage, handling).
EAN.UCC Definition: Code indicating the classification system(s)
of dangerous goods and/or the Agency(ies) responsible for it.
Examples: "ADR" European agreement on the international
carriage of dangerous goods on roads.
Business Rules: Various systems (ADR, RID, US49, IATA, etc.)
exist and are used for hazard classification and identification.
Information required when dangerousGoodsIndicator equals Y.
Repeatable field
http://www.unece.org/trade/untdid/d99b/tred/tred8273.htm
Hazardous attributes relate to supply chain handling (e.g.,
transport, storage, handling)
EAN.UCC Definition: Shipping name of the trade item (dangerous
goods). The recognized agencies (see

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 108

ARTS XML Item Maintenance Technical Specification V1.3.2

DangerousGoodsTechnicalN
ame

FlashPointTemperature

UnitedNationsDangerousGo
odsNumber

InformationProviderIDType

dangerousGoodsRegulationsCodes), in their regulations, provide
a list of all acceptable proper shipping names.
Examples: "Flammable Liquid"
Business Rules: Information required when
dangerousGoodsIndicator equals Y. Repeatable per
dangerousGoodsRegulation code. Hazardous attributes relate to
supply chain handling (e.g., transport, storage, handling).
EAN.UCC Definition: Chemical term of the trade item, listed by
name and allowed in the substance list of GGVS (Dangerous
Goods Ordinance for Roads) or GGVE (Dangerous Goods
Ordinance for Rail). This is composed of both text and a
language code. The language for text is specified using the two-
digit ISO 639 list.
Examples: "TRINITROCHLORO-BENZENE (PICRYL
CHLORIDE), WETTED"
Business Rules: Information required when
dangerousGoodsIndicator equals Y. The technical names are
listed in the order that they contribute to the danger (main hazard,
not necessarily the highest concentration).  Repeatable per
dangerousGoodsRegulation code. Hazardous attributes relate to
supply chain handling (e.g., transport, storage, handling)
extension base="MeasurementCommonData
EAN.UCC Definition: The lowest temperature at which a
substance gives off a sufficient vapor to support combustion. This
uses a measurement consisting of a unit of measure and value.
Business Rules: Information required when
dangerousGoodsIndicator equals Y.  Expressed in Celsius (or
Centigrade) or Fahrenheit  Format defined by UN/EDIFACT 7106
Has to be associated with valid UoM. Hazardous attributes relate
to supply chain handling (e.g., transport, storage, handling).
EAN.UCC Definition: The four-digit number assigned by the
United Nations Committee of Experts on the Transport of
Dangerous Goods to classify a substance or a particular groups
of substances. Abbreviation: UNDG Number
Examples: UN "1155" ETHYLENEGLYCOLDIETHYLETHER
Business Rules: Information required when
dangerousGoodsIndicator equals Y.  Repeatable per
dangerousGoodsRegulation code.
http://www.unece.org/trans/danger/publi/adr/adr2001/English/
Hazardous attributes relate to supply chain handling (e.g.,
transport, storage, handling).
from EAN.UCC - EAN.UCC Definition: Unique location number
identifying the information owner. E.g. Distributor, broker,
Manufacturer, Franchisee. This is not a third party service
provider. The purpose of this field is to identify the originator of
the data.
Example Trade Item A - is availavble to retailer B from
manufacter C or distributor D. The retailer could receive
information from both sellers and this field declares the
information owner.
Examples: Refer to the following websites for specific directions
on how to construct global location numbers - www.uc-council.org
or www.eanint.org
Business Rules: Combination of this field (gln) + gtin + target
market is not necessarily the source of the data, but has the
responsibility to provide and maintain the data in the catalogue.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 109

ARTS XML Item Maintenance Technical Specification V1.3.2

@ TypeCode
@ Name

ItemMeasurementsType

Ingredients
IngredientStrength

GenericIngredient

GenericIngredientStrength

ItemPalletHierarchyType
QuantityOfCompleteLayersC
ontainedInATradeItem

QuantityOfLayersPerPallet

QuantityOfTradeItemsContai
nedInACompleteLayer

This field is mandatory within the Global Data Synchronization
work process.
type="InformationProviderTypeCodeEnumeration
EAN.UCC Definition: Name of the party who owns the data.
Name of the information provider on the trade item.
Examples: Names of suppliers, wholesalers, manufacturers,
distributors, or retailers
Business Rules: Mandatory when Information Provider is
provided
from EAN.UCC
:extension base="ItemMeasurementCommonData

extension base="MeasurementCommonData
EAN.UCC Definition: Used for pharmaceutical trade item to
define the strength of each ingredient in a trade item or unit
volume of the trade item.
Examples: "100mg" for a tablet, "2%" for a liquid or ointment,
where 100 and 2 represent the value, and mg and % are the
units of measure
Business Rules: Sector specific extension pharmaceutical trade
item.  Can be locally mandatory based on each country's laws.
Has to be associated with a valid unitBasisOfMeasure
extension base="MeasurementCommonData
EAN.UCC Definition: Used, for pharmaceutical trade item to
describe 1 or many generic ingredients within the trade item.
Examples: "Paracetamol", "Codeine"
Business Rules: Sector specific and local extension. Can be
repeated
extension base="MeasurementCommonData
EAN.UCC Definition: Used, for pharmaceutical trade item to
define the strength of each generic ingredient in a trade item or
unit volume of the trade item.
Examples:
Business Rules: Sector specific and local extension. Repeated
per generic Substance  Needs to be associated with a valid UoM.
from EAN.UCC
EAN.UCC Definition: The number of layers of the base trade item
found in a trade item. Does not apply to the base trade item unit
Business Rules: Only applies to logistic units (e.g. pallet, case,
etc)
EAN.UCC Definition: The number of layers that a pallet contains.
Only used if the pallet has no GTIN. It indicates the number of
layers that a pallet contains, according to supplier or retailer
preferences.
Business Rules: Only used if the pallet has no GTIN. In this case
it applies to the highest level of the item hierarchy and only 1
pallet configuration can be provided. It is highly recommended to
use GTIN for Pallet identification
EAN.UCC Definition: The number of trade items contained in a
complete layer of a higher packaging configuration. Used in
hierarchical packaging structure of a trade item. Cannot be used
for trade item base unit.
Business Rules: Only applies to logistic units (e.g. pallet, case,
etc)

QuantityOfTradeItemsPerPal EAN.UCC Definition: The number of trade items contained in a

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 110

ARTS XML Item Maintenance Technical Specification V1.3.2

let

QuantityOfTradeItemsPerPal
letLayer

QuantityOfInnerPack

QuantityOfNextLevelTradeIte
mWithinInnerPack

GrossWeightOfPallet
CubeVolume
ItemPriceType
PriceLineID
RetailPriceOnTradeItem

@ LevelPricingFlag
@ PriceOnPackFlag

ItemUnitIndicatorType
UnitDescriptor
@ BaseUnitFlag

pallet. Only used if the pallet has no GTIN. It indicates the
number of trade items placed on a pallet according to supplier or
retailer preferences.
Business Rules: Only used if the pallet has no GTIN. In this case
it applies to the highest level of the item hierarchy and only 1
pallet configuration can be provided. It is highly recommended to
use GTIN for Pallet identification.
EAN.UCC Definition: The number of trade items contained on a
single layer of a pallet. Only used if the pallet has no GTIN. It
indicates the number of trade items placed on a pallet layer
according to supplier or retailer preferences.
Business Rules: Only used if the pallet has no GTIN. In this case
it applies to the highest level of the item hierarchy. It is highly
recommended to use GTIN for Pallet identification
EAN.UCC Definition: Indicates the number of non-coded physical
groupings (innerpacks) of next lower level trade items within the
current GTIN level.
Examples: Case of 12 bottles of shampoo contains two non-
coded plastic wrapped bundles each with six bottles. Value = "2"
Business Rules: An inner pack can only contain the same GTIN,
and inner pack sizing must be constant. Change of inner pack
doesn't change higher or lower level GTINs
EAN.UCC Definition: Indicates the number of next lower level
trade items contained within the physical non-coded grouping
(innerpack)
Examples: Case of 12 bottles of shampoo contains two non-
coded plastic wrapped bundles each with six bottles. Value = "6"
Business Rules: An inner pack can only contain the same GTIN,
and inner pack sizing must be constant. Change of inner pack
doesn't change higher or lower level GTINs
extension base="MeasurementCommonData
extension base="MeasurementCommonData
extension base="PriceCommonData

extension base="UnitPriceCommonData
EAN.UCC Definition: The retail price as marked on the trade item
package. This field is dependent on a value of "yes" for field
priceOnPackIndicator.
Examples: "USD 1.00", "EUR 36", “USD 17.45”
Business Rules: As monetary amount field, this data element
must be associated with a valid unit of measure.  Becomes
mandatory when priceOnPackIndicator = "Y". In this case, the
priceOnPack becomes Global (can not vary per Target Market).

EAN.UCC Definition: Indication of whether there is a retail price
physically on or attached to the trade item packaging of the trade
item by the manufacturer or information provider. This is a y/n
(Boolean) where y equals pricing on the trade item. If marked
yes, then the retailPriceOnTradeItem must also be given
Business Rules: Boolean Y/N where Y = there is a retail price on
the trade item; N = not pre-priced
from EAN.UCC
extension base="DescriptionCommonData
Definition: An indicator identifying the trade item as the base unit
level of the trade item hierarchy.

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 111

ARTS XML Item Maintenance Technical Specification V1.3.2

@ ConsumerUnitFlag

@ DespatchUnitFlag

@InvoiceUnitFlag

@ OrderableUnitFlag

@ VariableUnitFlag

KitType

Members

Examples: A bundle pack of product is composed of packages
without GTINs that cannot be sold individually. This bundle pack
would then be a base item. If that same bundle pack contained
individual packages that have a GTIN + could be individually sold
it would not
Definition:  Identifies  whether  the  current  hierarchy  level  of  a
trade item is intended for a ultimate consumption. For retail, this
trade  item  will  be  scanned  at  point  of  sale.  At  retail,  this  data  is
commonly  used  to  select  which  GTINs  should  be  used  for  shelf
planning and for front-end POS databases. This value reflects the
intention  of  the  Information  Provider  which  may  not  necessarily
be the intention of the retailer.
Examples: A multi-pack of paper towels and the individual paper
towels  contained  in  the  multi-pack  are  both  identified  as  a
consumer unit.
Business Rules:
There can be more than one consumer unit in one hierarchy
Definition:  An  indicator  identifying  that  the  information  provider
considers  the  trade  item  as  a  dispatch (shipping) unit.  This  may
be Trading Partner dependent based on channel of trade or other
point-to-point agreement.
True indicates the trade item is a dispatch unit..
Business Rules:
There can be more than one logistic unit in one hierarchy
Definition:  An  indicator  identifying  that  the  information  provider
will include this trade item on their billing or invoice. This may be
Trading  Partner  dependent  based  on  channel  of  trade  or  other
point-to-point  agreement.  True  indicates  the  trade  item  is  an
invoicing unit.
Business Rules:
There can be more than one invoicing unit in one hierarchy
Definition:  An  indicator  identifying  that  the  information  provider
considers this trade item to be at a hierarchy level where they will
accept  orders  from  customers.  This  may  be  different  from  what
the  information  provider  identifies  as  a  despatch  unit.  This  may
be  relationship  dependent  based  on  channel  of  trade  or  other
point  to  point  agreement.  True  indicates  the  trade  item  is  an
ordering unit
Business  Rules:  There  can  be  more  than  one  ordering  unit  in
one hierarchy
Definition: Indicates that an article is not a fixed quantity, but that
the quantity is variable. Can be weight, length, volume. trade item
is used or traded in continuous rather than discrete quantities.
Examples: Wheel of Cheese: The weight is about 25 kilograms,
but it can be 24 kilogram or 27 kilogram.
Business Rules: Boolean True=variable, False=fixed. Applies to
EAN.UCC bricks: Meat, Cheese, Fruits, Dairy trade item.
extension base="KitCommonData
A collection of items that is priced & sold as a single item, but
which is exploded into its constituent items for the purposes of
tracking inventory.
Items which are components of this item, i.e. stereo speakers,
amplifier are members of the Stereo Item

@Cost Inclusive Flag

Indicates  the  cost  of  this  member
included in the base item

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 112

ARTS XML Item Maintenance Technical Specification V1.3.2

ItemID

Kit
LotType
LotID
Item
@ BatchNumber

ManufacturerType
Manufacturer

Name

MarketingType
Season

FiscalYear
AgeGroup
Gender
LifestyleID

MixMatchType
MixMatchID
Item

MixMatchPrice

extension base="ItemIDCommonData
@ CostInclusiveFlag
type="KitType

An identifier for a LOT of specific ITEMs
type=" ItemIDCommonData
type="LotCodes
EAN.UCC Definition: Indication whether the base trade item is
batch or lot number requested by law, not batch or lot number
requested by law but batch or lot number allocated, or not batch
or lot number allocated. A batch or lot number is a manufacturer
assigned code used to identify a trade item's trade item on batch
or lot. Differs from Serial Number which is a manufacturer
assigned code during the trade item on cycle to identify a unique
trade item.
Business Rules: Local legal requirement (E.g. Austria). Relevant
only for certain industries
from EAN.UCC
EAN.UCC Definition: GLN (or AlternatePartyIdenfication)
identifying the manufacturer of a trade item. May or may not be
the brand owner, could be a contract manufacturer. GLN (or
AlternatePartyIdentification) identifying manufacturer of a trade
item: this is repeatable field.
Examples: Brand owner A uses contract manufacturers B and C
to produce trade item D. This field would provide a GLN (or
AlternatePartyIdentification) for manufacturers B and or C
@TypeCode type="ManufacturerTypeCode
EAN.UCC Definition: Descriptive name of the manufacturer of the
trade item.
Business Rules: May or may not be the brand owner. This is not
the name of a party that assembles trade item. It is an optional
field, manually maintained, that can identify the company that
manufactures the product. This is a repeatable field.

Season code; along with the Fiscal Year attribute, describes
when the Item is available for sale. Christmas, back to school,
Easter, spring. These fields could be used to allow price
derivation rules to act on appropriate items

extension base="LifestyleIDCommonData
An optional descriptor of a Style that sends a message for the
image conveyed by the product, e.g. Casual, Traditional,
Professional, Fashion, Modern, Comfort, Extreme, Athletic,
Exotic, European, Designer.

Unique id for this particular mix match
type="MixMatchItemType
This is the list of items that are involved in the absolute Mixmatch.
The example is from Japanese retail where a shirt and a tie have
a different absolute price (combined) than the two items
separately. The difference in price is not considered a price
reduction/discount
extension base="UnitPriceCommonData

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 113

ARTS XML Item Maintenance Technical Specification V1.3.2

MinimumQuantity

MaximumQuantity

MixMatchPriceDerivationRul
eID
MixMatchItemType
ItemID

Price

NextLowerTradeItemInforma
tionType
TotalQuantityOfNextLowerTr
adeItem

NextLowerTradeItemInforma
tion

ChildTradeItem
OrderInformationType
OrderingLeadTime

OrderQuantityMaximum

This is the new absolute price of the mixmatch. There is no
markdown/price reduction, this is the price of the combination.
The total price for this quantity purchased level, i.e. 3 candy bars
for $1.00.
extension base="QuantityCommonData
The minimum quantity of like items to be purchased for Mix
Match pricing to go into effect
extension base="QuantityCommonData
The maximum quantity of like items that can be purchased for
Mix Match pricing to stay in effect.
This is the reference to the price derivation rule(s) that apply to
this item

extension base="ItemIDType
Alternate items which can be mixed with this item
extension base="UnitPriceCommonData
The price of this item when included in this mix match deal.  This
allows one to purchase a shirt and pants in one mix match where
when purchased together the price for both is defined
from EAN.UCC - Relates to packaging

EAN.UCC Definition: This represents the Total quantity of next
lower level trade items that this trade item contains.
Business Rules: e.g. in a mixed module, with 2 x five different
types of nail varnish, this number = 10.  Where this differs from
“QuantityofNextLowerLevelTradeItem” is that this field is used in
conjunction with each GTIN identified in the field
‘NextLowerLevelTradeItem’. E.g. in the example of 2 x five
different types of nail varnish, this number = 2.If the item is not
mixed, then this number will equal the value submitted for the
QuantityofNextLowerLevelTradeItem” field
EAN.UCC Definition: Value indicates the number of unique next
lower level trade items contained in a complex trade item. A
complex trade item can contain at least 2 different GTINs.
Examples: Ready to sell display of cosmetics contains 2 bottles
each of five different colors (each with their own GTIN) of blush
The value for this field would be "5".
Business Rules: Only applies to dispatch units (cases, pallets,
etc.)
type="ChildOfTradeItem
from EAN.UCC
extension base="MeasurementCommonData
EAN.UCC Definition: The normal delivery time measured from
receipt of order by the seller until trade item is shipped by the
seller.
Examples: 12 hours, 48 hours, 4 days.
Business Rules: Geographic distance from
manufacturing/distribution point to delivery point may impact this
value. Related to time unit field.  Must be associated with valid
unit of measure
EAN.UCC Definition: The maximum quantity of the trade item that
can be ordered. A number or a count. This value can represent
the total number of units ordered over a set period of time with
multiple orders.
Examples: - “when a manufacturer chooses to control

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 114

ARTS XML Item Maintenance Technical Specification V1.3.2

manufacturing costs by limiting the amount of product that a
customer can buy per order
– example – Geneva watchmaker only allows orders of 10
watches per customer per order so as to control their production
for quality control reasons, and to ensure that all of his customers
receive some product.”
Business Rules: Value can vary on Trading Partner dependent
basis. Quantity means number of this trade item level hierarchy.
This field is relevant at any trade item hierarchy level, but does
not need to be populated for all levels.
EAN.UCC Definition: Represent an agreed to minimum quantity
of the trade item that can be ordered. A number or a count. This
applies to each individual order. Can be a fixed amount for all
customers in a target market.
Business Rules: Value refers to the minimum order for this trade
item hierarchy level. Cannot be a monetary figure. E.g. minimum
order = $100 of goods at cost. This field is relevant at any trade
item hierarchy level, but does not need to be populated for all
levels
EAN.UCC Definition: The order quantity multiples in which the
trade item may be ordered. If the Order Quantity Minimum is 100,
and the Order Quantity Multiple is 20, then the trade item can
only be ordered in quantities which are divisible by the Order
Quantity Multiple of 20.
Examples:100, 120, 140, 200. A number or a count.
Business Rules: If the order quantity minimum is 100, and the
order quantity multiple is 20, then the product can only be
ordered in quantities which are divisible by the order quantity
multiple of 20, eg 100, 120, 140, 200 etc.
extension base="MeasurementCommonData
EAN.UCC Definition: A trade item specification other than gross,
net weight, or cubic feet for a line trade item or a transaction,
used for order sizing and pricing purposes. For example, factors
may be used to cube a truck, reflecting different weights, and
dimensions of trade item.
Business Rules: Assumes a standard size truck or lorry
signify that this ITEM is ordered as part of a collection of ITEMs
form EAN.UCC
EAN.UCC Definition: A governing body  that creates and
maintain standards related to organic products./Brules: only
registered values may be used. It's a repeatable field.
type="OrganicCharacteristicsTypeCode use="optional"
default="Unknown
EAN.UCC Definition: Used to indicate the organic status of a
trade item or of one or more of its components.

  100percentOrganic
  Organic
  MadeWithOrganicIngredients
  SomeOrganicIngredients
  NotOrganic

Unknown

The number of units within the PACK ITEM
extension base="MeasurementCommonData
The volume of the PACK ITEM

OrderQuantityMinimum

OrderQuantityMultiple

OrderSizingFactor

@OrderKitFlag
OrganicCharacteristicsType
ClaimAgency

@ TypeCode

PackType
UnitNumberCount
PackVolume

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 115

ARTS XML Item Maintenance Technical Specification V1.3.2

PackWeight

@ PackMethod
PackagingType
PackagingMaterialCode

PackagingMaterialCodeList
MaintenanceAgency

PackagingMaterialCompositi
onQuantity

PackagingMaterialDescriptio
n

PackagingTermsAndConditio
ns

Packing
@ BarCodeOnPackageFlag

extension base="MeasurementCommonData
The actual weight of the PACK ITEM including tare
type="PackMethodCodes" use="optional" default="Flat
from EAN.UCC
EAN.UCC Definition: Code source needs to be defined. Currently
a European Union table of code lists exists for this requirement.
The code list required to identify the packaging material of the
trade item.
Examples: "GL" (glass) "AL" (Aluminum)
Business Rules: Can be repeated for multi-material packaging
and linked to packaging weight
EAN.UCC Definition: Agency needs to be defined. The agency or
agencies controlling the packaging code lists of each country.
Mandatory if packaging material code is populated.
Business Rules: Dependent on field packagingMaterialCode
extension base="MeasurementCommonData
EAN.UCC Definition: The quantity of the packaging of the trade
item. Can be weight, volume or surface, can vary by country.
Examples: "15 grm", Value, amount, eaches, etc.
Business Rules: Can be repeated for multi-material packaging
and must be associated with a valid ISO language code from the
attached table.  Has to be associated with valid UOM
EAN.UCC Definition: The system generated text description
equivalent of the packaging material code.
Examples: "Glass" "Aluminum"
Business Rules: Can be repeated for multi-material packaging
and linked to packaging weight. As a description text field, this
data element is repeatable for each language used and must be
associated with a valid ISO language code from the attached
table. Dependent on the field packagingMaterialCode
EAN.UCC Definition: Indicates if the packaging given in the
described packaging configuration is a rented, exchangeable,
against deposit or one way/not reusable.
Examples: Codes to be defined.
Business Rules: List of authorized values based on EANCOM
7073, X12 DE102 and X12 DE399
type="PackingType
EAN.UCC Definition: Indication if the trade item is physically bar-
coded with the primary trade item identification number.  This is a
y/n (Boolean) where Y equals trade item is bar-coded.
Business Rules: Boolean Y/N; Y= bar-coded N= not bar-coded
Technical Note: This Boolean question is answered by the
application of class Bar Code Type List. If the Bar Code Type List
class (telling which barcodes are on the package) exists, then
there is a barcode on the package. The attribute is derived from
the Bar Code Type List and is not in the model

@ MarkedAsRecyclableFlag  EAN.UCC Definition: The package of this GTIN is marked to
indicate that it is recyclable.
Examples: Aluminum can marked as recyclable
Business Rules: Boolean field Y/N = marked recyclable, N = not
marked recyclable. Applies to recyclable packaging with or
without deposit.

@ MarkedAsReturnableFlag  EAN.UCC Definition: trade item has returnable packaging. This is

a yes/no (Boolean) where yes equals package can be returned.
Business Rules: Boolean Y/N; Y= marked returnable, N= not

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 116

ARTS XML Item Maintenance Technical Specification V1.3.2

@
MarkedWithExpirationDateFl
ag

returnable.  Attribute applies to returnable packaging with or
without deposit.
EAN.UCC Definition: Indicates if the packaging of the trade item
has a freshness date, sell by date, or use by date stamped on or
imprinted. This is a y/n (Boolean) where y equals packaging of
the trade item has a freshness date stamped on or imprinted.
Examples: Use by date - batteries; sell by date - milk
Business Rules: Boolean Y/N Y = marked with date N= not
marked with date

@ MarkedWithGreenDotFlag  EAN.UCC Definition: Trade item packaging marked with green

point indicator. Law in several European countries mandates the
green point indicator. This is a yes/no (Boolean) where yes
equals marked with green point indicator.
Business Rules: Boolean Y/N, Y = marked with the green dot
Legal requirement in limited number of countries. See:
ProEurope s.p.r.l Av de Tervuren 35 Etterbeck- B 1040 Brussels.
Countries concerned as of Nov 01:
AT,BE,CZ,FR,DE,HU,IE,LT,LU,NO,PT,ES,SE
EAN.UCC Definition: trade item packaging contains information
pertaining to its ingredients. trade item ingredients are required to
be shown on the trade item (normally at base trade item level).
This is a yes/no (Boolean) where yes equals marked with
ingredients.
Business Rules: Boolean Y/N where Y=marked with ingredients ,
N=not marked with ingredients. trade item ingredients are
required to be shown on the trade item (normally consumer unit
level) Sector specific and geographical extension. List of
ingredients can be legally required in some countries for limited
trade item sectors
from EAN.UCC
EAN.UCC Definition: The code identifying the type of package
used as a container of the trade item.
Examples: Codes to be defined.
Business Rules: List of authorized code values based on UN-
ECE 21 Can be repeated
EAN.UCC Definition: System generated text description of the
type of packaging used for the trade item. For example, box or
carton. Examples: "Box", "Bottle"
Business Rules: List of authorized text description values based
on UNECE 21 Recommendations - EANCOM 7065. Can be
repeated. System generated field
from EAN.UCC
EAN.UCC Definition: Indicates whether the described dispatch
unit is delivered on a pallet and on which type of pallet, or if it is
non-palletized. If the dispatch unit is delivered on a pallet the
pallet type must be given here.  The range of the pallet
types/codes is listed in code sets.
Examples: "200" = pallet ISO 0, 1/2 Euro pallet.
Business Rules: Only used if the pallet has no GTIN. In this case
it applies to the highest level of the item hierarchy and only 1
pallet configuration can be provided. It is highly recommended to
use GTIN for Pallet identification
EAN.UCC Definition: Indicates if the pallet in the prescribed pallet
configuration is rented, exchangeable, against deposit or one
way (not reusable).

@
MarkedWithIngredientsFlag

PackingType
TypeCode

TypeDescription

PalletInformationType
TypeCode

TermsAndConditions

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 117

ARTS XML Item Maintenance Technical Specification V1.3.2

PreparedItemType
FoodItemHoldingTime

CookingMessage
IngredientMessage
NutritionalMessage
DegreeOfOriginalWort

FatPercentageInDryMatter

PercentageOfAlcoholByVolu
me

@
ItemGeneticallyModifiedFlag
@ ItemIrradiatedFlag
@ IngredientIrradiatedFlag

@
RawMaterialirradiatedFlag

SellingRulesType

SellingRuleID

MinimumAge

AgeRestriction

SpecialRestriction

SecurityRequiredTypeCode

Examples: "7E" for non-returnable pallet
Business Rules: Used in conjunction with a pallet GTIN. List of
authorized values based on EANCOM 7073, X12 DE102 and
X12 DE399

The number of minutes that a prepared food item may be held
ready for sale.  At the end of this time, the item must not be sold
to a customer

EAN.UCC Definition: Specification of the degrees of original wort.
Examples: The beer degree for the allocation of different original
wort proportions in different kinds of beer to the respective beer
tax group and beer tax rate
Business Rules: Sector specific extension (alcoholic beverages)
Local legal requirement (Austria)
EAN.UCC Definition: The amount of fat contained in the base
product expressed in percentage.
Examples: ‘10’
Business Rules: Mainly concerns cheese and dairy trade items.
Percentage is implicit
EAN.UCC Definition: Percentage of alcohol contained in the base
unit trade item.
Examples: ‘12’
Business Rules: Sector specific extension. Percentage is implicit
EAN.UCC Definition: Used to indicate whether trade item
contains genetically modified contents.

EAN.UCC Definition: Indicates if radiation has been applied to a
trade item’s ingredient.
Business Rules: Should only be submitted if a claim is made on
the trade item
EAN.UCC Definition: Indicates if radiation has been applied to a
trade item’s raw material
Business Rules: Should only be submitted if a claim is made on
the trade item. This field is trade item specific, indicating that
radium has been applied to the trade item
Indicates  the  restriction  the  sale  of  an  item  to  customers  that
must  be  a  minimum  age  and  by  the  worker  that  must  be  a
minimum age.
A unique system assigned identifier for the Item Selling Rules
(The set of rules/behaviours defined in the system that are
enacted when the item is sold.
The  minimum  age  under  which  the  customer  is  prohibited  from
purchasing the item and the worker is prohibited from selling the
item.
Indicates whether the customer's account limit is restricted by the
operator or customer's age. Please include the age restrict
message id in this field
Indicates whether the selling of an item is restricted by a waiting
period or required license, i.e. gun purchase
A code that defines the security environment and procedures
required for receiving, displaying and selling the item.  This is for
high-priced merchandise like jewelry, certain prescription drugs,

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 118

ARTS XML Item Maintenance Technical Specification V1.3.2

LimitedQuantity

@ AllowDiscountFlag
@ ClearanceFlag
@ ExclusiveFeatureFlag

@ FoodStampEligibilityFlag
@ GiftRegistryEligibilityFlag

@ WICEligibilityFlag
ServiceItemType
BaseCostAmount

CostsEstablishedDate

Description

NetCostAmount

ServiceTermsCode
StoreFinancialLedgerAccoun
tID
ShelfInformationType
FacingCount

ShelfLifeDayCount

@ TypeCode

@ UnitPricingRequiredFlag

@DirectStoreDeliveryAuthori
zedFlag

ordinance, fireworks, etc.
Indicates the maximum number of these items that can be sold in
a single transaction

An optional flag to indicate a special feature that implies
exclusive quality when quality is a distinctive characteristic of the
product, e.g. Wine Vintage could be Exclusive Feature
Identifies this item as being eligible for food stamps
Indicates whether this item is eligible to be included in gift
registries
identifies this item as being eligible for WIC

extension base="AmountCommonData
The base cost amount of the SERVICE ITEM. This cost excludes
all promotional allowances
The effective date of the current cost price for the SERVICE
ITEM
extension base="DescriptionCommonData
A textual description of the SERVICE ITEM
extension base="AmountCommonData
The net cost price of the SERVCE ITEM. this cost includes all
promotional allowances.
The type of service terms and conditions
The reference for the STORE FINANCIAL LEDGER ACCOUNT

The number of units that can be containied in one facing. For
example, if you can fit 30 units of a product on a shelf and there
are 3 facings, then the units per facing is 10
The number of business days the SHELF ITEM may be displayed
for sale to customers  and after which must be removed. This
attribute is for perishable produce items, drugs, and other time
sensitive items (like newspapers). -- EAN.UCC --
minimumTradeItemLifespanFromTimeOfArrival
EAN.UCC Definition: The period of days, guaranteed by the
manufacturer, before the expiration date of the trade item, based
on arrival to a mutually agreed to point in the buyers distribution
system. Can be repeatable upon use of GLN.
Examples: "35"
Business Rules: This field is indicative of the normal Minimum
Shelf Life.  It is recognized that this figure may vary slightly
depending upon locations
of DC or Stores, therefore it is repeatable. This information is
linked to the Target Market. Must be expressed in number of
days
type="ShelfInformationTypeCode" use="optional" default="Staple
A code to indicate whether the SHELF ITEM is a staple or
perishable product.
An indicator to identify if the SHELF ITEM needs to be
individually priced rather than conveyed through a shelf label.
Examples include high priced merchandise and variable weight
products
An indicator used to identify whether the RETAIL STORE is
authorized to accept the SHELF ITEM as a direct store delivery

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 119

ARTS XML Item Maintenance Technical Specification V1.3.2

SizeCodeType

SizeSchemeType

SizeScheme

EquivalentSize

SizeGroup

@ ListAgency
StockItemType
CustomerPickup

UnitPriceFactor

SaleUnitLastReceivedBaseC
ostAmount

SaleUnitLastReceivedNetCo
stAmount

SaleUnitLandedCostAmount

SaleUnitLastReceivedCosts
EstablishedDate
@ TypeCode

@ StockType

@ WeightOrUnitCountCode

@ SwellFlag

(DSD) item
from EAN.UCC
extension base="SizeCommonData
A grouping of size schemes based on the specifics of a particular
geographic region, such as US, Europe or Japan
A.k.a. Size Family or Size Range. A domain of sizes that get
administered together, e.g. 2-14, S-XXL. Size Scheme 2-14
includes sizes 2, 4, 6, 8, 10, 12, and 14, i.e. a Size Scheme is
inclusive of the end points as well as all sizes in between. All
sizes available for a particular Style.  Each Size Scheme may be
assigned to one of the nine NRF Size tables

Contains equivalent European, Japanese, etc. sizes for every US
size defined in the Size entity
Contains a groups of sizes that are commonly used together, e.g.
Men's Shirt Sleeve size group

A code that defines where and how a customer may pickup this
item.  For examples a refrigerator may have to be picked up at
the shipping dock or at the retailers warehouse.
The number of units of measure per selling unit. Used as the
divisor when calculating the STOCK ITEMs  unit retail price, eg
$1.67 per pound or $2.59 for 32 floz.
extension base="AmountCommonData
The base cost per sell unit derived from the last receipt of this
item.  The base cost excludes allowances, discounts, charges
and other amounts that may change the item cost
extension base="AmountCommonData
The net cost per sell unit derived from the last receipt of this item.
The base cost includes allowances, discounts, charges and other
amounts that may change the item cost.  Where there are no
allowances, etc. the net cost will equal the base cost
extension base="AmountCommonData
The cost of the item plus the insurance, drayage, cartage,
delivery, insurance, customs duties, etc. which add up to the full
delivered cost of an imported item to the store.
The date the last received costs (net and base) were established.

type="StockItemTypeCode" use="optional" default="ShelfItem
A code to indicate the STOCK ITEM type, ie
SHELF ITEM,
APPAREL ITEM,
SERIALIZED ITEM
type="StockTypeCode" use="optional" default="DryStockDiscrete
DrystockDiscrete - Product is a discrete item that is sold by the
each, DrystockBulk - Product is an item purchased in Bulk and
sold by weight or other dry measure, Wetstock - Product is
purchased in Bulk and sold by volume using a dispensing device.
(E.g. Petrol, Diesel, Kerosine) dispensed at a service station.
type="WeightOrUnitCountCodeType" use="optional"
default="Unit
A code to indicate whether the STOCK ITEM is sold by weight or
as an unit
A flag used to indicate if the STOCK ITEM may gain weight or

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 120

ARTS XML Item Maintenance Technical Specification V1.3.2

@ ShrinkFlag

@
InventoryAccountingMethod

StoreStructureType

swell from time of order to time of receipt
A flag to denote if the STOCK ITEM could loose weight from the
time of order until the time of receipt.
type="InventoryAccountingMethodType" use="optional"
default="CostMethod
A code to define the inventory accounting method to be used for
the item.  Examples of methods include the retail method, cost
method,

  CostMethod

RetailMethod
extension base="StoreStructureHierarchyCommonData

StyleCodeType

extension base="StyleCommonData

SupplierInformationType
ResponsibleBuyerID
SupplierID
SupplierRetailSaleUnitCode

SupplierLinearMeasureCode

Description

AvailabilityStatus
SupplierItemID
CaseEANUCCNumber
ModelNumber
ModelYear
Brand

SalesUnitPerPackUnitQuanti
ty

ColorCode

SizeCode

StyleCode

SupplierItemCostPerUnitTyp
eCode

@ StoreOrderAllowedFlag

A code assigned by the retailer to uniquely identify the supplier
The code used to specify the units in which a value is being
expressed, or manner in which a measurement has been taken.
type="UnitOfMeasureCode
The code used to specify the units in which a value is being
expressed, or manner in which a measurement has been taken.
extension base="DescriptionCommonData
The description of the SUPPLIER ITEM
A code to signify the availability of the SUPPLIER ITEM
The code assigned by the supplier to uniquely identify the ITEM
The UPC/EAN case code, eg UPC/EAN-14, EAN-128.
The model reference for a specific ITEM.
The year of release or production of the ITEM
Unique name to denote the item as a product of a single
manufacturer or supplier
The number of retail sale units in the supplier item pack.  For
example 24 cans of Coke (the retail sale units) in a case (supplier
item pack) or 4 six packs (the retail sale units) in a case (supplier
item pack).
extension base="ColorCodeCommonData
@ ListAgency
The supplier's color description of the SUPPLIER ITEM
extension base="SizeCommonData
@ ListAgency
The size dimensions of the SUPPLIER ITEM
extension base="StyleCommonData
The style description of the SUPPLIER ITEM
Defines the unit type the owned attribute costs are assigned to
for this item.  Valid unit types include: SALE UNIT, PACK UNIT
and SHIP UNIT.  A single SUPPLIER ITEM may in effect have 1
to three SUPPLIER ITEM BASE COST entities associated with it
A flag to indicate that the RETAIL STORE is permitted to order a
particular SUPPLIER ITEM

@ StoreReceiptAllowedFlag  An indicator to signify whether the RETAIL STORE is permitted to

@
MarketCostOverridAllowedFl
ag

receive the SUPPLIER ITEM
A flag that indicates (if true) that this SUPPLIER ITEM catalog
cost may be superceded by a market cost (known only when the
item is received).  This flag is intended to support produce, fresh
seafood and other perishable items with market costs that vary

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 121

ARTS XML Item Maintenance Technical Specification V1.3.2

TankProductType
TankID

Description
FuelProductID
TankChartID
TankInstallDate
TankManifoldID
TankManufacturer
TankModelNumber
TankSerialNumber
TankDepth

TankLowInventoryVolume

TankMaximumOperatingVolu
me

TankReorderVolume

TankVolume

ReferenceDensity

ProductGroupCode

TargetMarketType
CountryCode

Description

Subdivision

The assigned identification for a fuel product tank.  If it is a
dispenser blended fuel grade then it is the Tank Id of the fuel
product with the lowest octane in the blend
A description of the tank
Identifier for the fuel product
The identification of the tank capacity chart
The date the fuel product tank was installed
The identification of the fuel product tank manifold
The name of the manufacturer of the fuel product tank
The model number of the fuel product tank
The serial number of the fuel product tank
The maximum depth of the fuel product
@ UnitOfMeasure
Indicates critically low inventory condition
@ UnitOfMeasure
The maximum amount of product which can safely be put into a
tank
@ UnitOfMeasure
The volume at which fuel product should be reordered
@ UnitOfMeasure
The volumetric capacity of the fuel product tank
@ UnitOfMeasure
The reference density at reference temperature of the product,
used for calculating the volume correction factor. Cf. ASTM D
1250 table 54 or American Petroleum Institute (API) Std 2540
table 6
@ UnitOfMeasureCode
Specifies the product group of the Item for calculation of
temperature corrected volume.  Defined by ASTM D 1250 table
54 or American Petroleum Institute (API) Std 2540 table 6
from EAN.UCC
EAN.UCC Definition: The target market code indicates the
country level or higher geographical definition in which the
information provider will make the GTIN available to buyers. This
Indicator does not in any way govern where the buyer may re-sell
the GTIN to consumers.
Examples: “036”=Australia, “300” = Greece, “524”= Nepal  --
Business Rules:ISO 3166-1 format 3 digit numerical; following
AIDC guidelines. This information drives data synchronization
rules linked to global/local, local status. Combination of this field
+GTIN+GLN uniquely identifies a set of attributes or a trade item.
This is a repeatable field. This field is mandatory within the Global
Data Synchronization process.
EAN.UCC Definition: The name for the specific target market
identified with the Target Market Country Code . Target market
description is composed of both text and a language code. The
description will be generated from the ISO 3166-1 code list. The
language code will be generated from the ISO 639 code list.
Examples: ISO 3166-1 840= "United States", 276= "Federal
Republic of Germany, 156 = "China"
Business Rules: This is the textual indication of the target market
code
EAN.UCC Definition: The Target Market Subdivision Code is the
secondary code of the Target Market and must be a subdivision

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 122

ARTS XML Item Maintenance Technical Specification V1.3.2

of a Target Market Country Code. The Target Market Subdivision
Code describes the "geo-political subdivision of a country" where
the trade item is available for sale, as determined by the
information provider. For example, "State" in the US, Land in
Germany, "Region" in France, or "Province" in Canada. Not all
countries have subdivisions. This code is represented by the
three character ISO 3166-2 code. This Target Market Subdivision
Code is a dependent attribute. It is important to note that the lack
of the Target Market Subdivision code implies that the trade item
is available in the entire target market country.
Examples: “ “208-025” where “208” represents Denmark from the
ISO 3166-1 and 025 represents the Danish county of Roskilde
from the ISO 3166-2.  “554-BOP” where “554” represents New
Zealand from the ISO 3166-1 and “BOP’ represents the Bay of
Plenty.  Business Rules: ISO 3166-2 format 3 digit numerical/3
character alpha which represents country and subcountry code;
following AIDC guidelines. This information drives data
synchronization rules linked to global/local, local status. This
optional field helps further define trade item optional subdivision
code. A subdivision code must be used in tandem with a
corresponding higher level country code. (e.g. Ohio with US).
This is a repeatable field.
from EAN.UCC
xs:extension base="TaxCommonData
A code to denote the tax exemption status from sales and use
tax.
from EAN.UCC

TaxInformationType

TaxExemptCode

TemperatureInformationType
DeliveryToDistributionCenter  EAN.UCC Definition: Permitted maximum/minimum temperature

of the trade item on transport to the distribution center
Examples: "+6 C" or degrees F, value
Business Rules: Temperature information is important for dairy
trade item, dangerous goods and other trade items for which
certain temperature limits are necessary during transport or
storage, for quality or safety reasons. Has to be associated with
valid UoM.
EAN.UCC Definition: Permitted maximum/minimum temperature
of the trade item during delivery to market.
Examples: "+7 C" or degrees F, value
Business Rules: Temperature information is important for dairy
trade item, dangerous goods and other trade items for which
certain temperature limits are necessary during transport or
storage, for quality or safety reasons. Has to be associated with
valid UoM.
EAN.UCC Definition: The maximum temperature at which the
trade item can bestored. This uses a measurement consisting of
a unit of measure and a value.
Examples: "+15 F" or degrees C, value
Business Rules: When no other information is provided
(temperatures to market or/and distribution center), this value
applies at any point of the supply chain. Temperature information
is important for fresh trade item, dangerous goods and other
trade items for which certain temperature limits are necessary for
quality or safety reasons. Has to be associated with a valid UoM.
from EAN.UCC
extension base="MeasurementCommonData

DeliveryToMarket

StorageHandling

TemperatureType
Maximum

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 123

ARTS XML Item Maintenance Technical Specification V1.3.2

Minimum

WarrantyType
Description

Length

@ TypeCode

WasteType
TypeCode

FactorPercent
Enumerations
ItemStatusCodes

ItemTypeActions

GroupTypeCode

Definition: Permitted maximum temperature of the trade item on
transport.
Examples: "+6 C" or degrees F, value
extension base="MeasurementCommonData
Definition: Permitted minimum temperature of the trade item on
transport.
Examples: "+2 C" or degrees F, value

extension base="DescriptionCommonData
A code to signify the type of warranty offered by the RETAIL
STORE. This warranty normally supplements the warranty
offered by the MANUFACTURER
extension base="xs:duration
@ UnitOfMeasure
WarrantyTypeCode
Enumeration

  Manufacturer

Store

The code to denote the type of waste associated with the BULK
ITEM when breaking down to retail selling units.
The pre-defined waste factor percentage, e.g. boning allowance.

Active
Inactive
Pending"

AddItem
ChangeItem
DeleteItem

Discount
SuggestiveSelling
PrerequisiteTools
PriceOptimization
LoyaltyPrograms
IncompatibleItems
QuantityRestrictions
TimeRestrictions
PremiumEligibleItem
ParkingValidation

PackMethodCodes

LotCodes

PriceEntryRequiredCodes

Hanging
Flat

Hanging
Flat

Required
Prohibited
Optional

EquivalentItemActionType

Substitute
SubstitutedFor

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 124

ARTS XML Item Maintenance Technical Specification V1.3.2

AdjustmentAmountTypeCod
e

EvenExchange
IncreaseAmount
DecreaseAmount

DiscountEnumeration

StockItemTypeCode

StockTypeCode

NotAllowed
PercentOnly
AmountOnly
Either

ShelfItem
ApparelItem
SerializedItem

DryStockDiscrete
DryStockBulk
WetStock

WeightOrUnitCountCodeTyp
e

Unit
Weight

InventoryAccountingMethod
Type

RetailMethod
CostMethod

DisplayUnitTypeCode

DispositionTypeCode

ShelfInformationTypeCode

WarrantyTypeCode

ManufacturerTypeCode

FreeStanding
ShelfEnd
Refrigerator

ReturnToSupplier
Destroyed
RetainUntilNextPromotion

Staple
Perishable

Manufacturer
Store

BuyerAssignedIdentifierForAParty
DEADrugEnforcementAgency
DUNS
DUNSPlusFour
GLN
HINCanadianHealthCardIdentificationNumber
SCAC
SellerAssignedIdentifierForAParty
TDLineTradeDimensions
UCCCommunicationIdentification
UNLocationCode

OrganicCharacteristicsType
Code

110percentOrganic
Organic
MadeWithOrganicIngredients
SomeOrganicIngredients
NotOrganic
Unknown

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 125

ARTS XML Item Maintenance Technical Specification V1.3.2

InformationProviderTypeCod
e

DangerousGoodsAMarginNu
mberTypeCode

Distributor
Broker
Manufacturer
Franchisee

NotPossible
Possible
Used

Copyright  2011 ARTS XML.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 126

