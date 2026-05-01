---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/arts/item-maintenance/ARTSItemMaintenance_TechSpec_1.3.2/CR ARTS XML Item Maintenance Technical Specification V1.3.2 20131223.pdf.md
tags: [canary, arts, retail-data-model, standards-reference, tier1-extract]
project: canary
status: unprocessed
---

# CR ARTS XML Item Maintenance Technical Specification V1.3.2 20131223.pdf

## Source
File: `Brain/raw/.extract/tier1-md/arts/item-maintenance/ARTSItemMaintenance_TechSpec_1.3.2/CR ARTS XML Item Maintenance Technical Specification V1.3.2 20131223.pdf.md`
Size: 189,408 bytes

## Raw content
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

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
