---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/arts/inventory/ARTS XML Inventory Charter.pdf.md
tags: [canary, arts, retail-data-model, standards-reference, tier1-extract]
project: canary
status: unprocessed
---

# ARTS XML Inventory Charter.pdf

## Source
File: `Brain/raw/.extract/tier1-md/arts/inventory/ARTS XML Inventory Charter.pdf.md`
Size: 16,436 bytes

## Raw content
IXRetail
Inventory Charter

September 13, 2005

Abstract:
This document serves as the IXRetail Inventory Work Team Charter.  The contents of the
charter are defined in the IXRetail Technical Report, IXRetail Development Process (LC-
Development-Process-20011011.doc on the ARTS/IXRetail web board).

Status of this Document
This document is an IXRetail Last Call Working Draft of the Inventory Work Team that
has  been  approved  by  the  IXRetail  Technical  Committee  and  promoted  to  Candidate
Recommendation  for  member  and  public  review  for  content  and  intellectual  property.
This document is release under the ARTS IP Policy.

Open Issues: None

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
2 of 11

Copyright © National Retail Federation 2005. All rights reserved.  This document may be copied or used by and for
ARTS Members for purposes consistent with adoption of the ARTS Standards.  However, any changes or inconsistent
uses must be pre-approved in writing by the National Retail Federation.  As such, this document may not be furnished
to others, and derivative works (the term “derivative works” does not include functional additions that do not modify or
change the base standard as written) that comment on or otherwise explain it or assist in its implementation may not
cite  or  refer  to  the  standard,  in  whole  or  in  part,  without  such  permission.    Moreover,  this  document  may  not  be
modified  in any  way,  such  as  by  removing  the copyright  notice  or  references  to  the  NRF,  ARTS,  or  its committees,
except as needed for the purpose of developing ARTS standards using procedures approved by NRF, or as required to
translate it into languages other than English.

1.  Introduction

This document serves as the IXRetail Inventory Work Team Charter document.  Per the
IXRetail  Technical  Report,  IXRetail  Development  Process,  this  document  is  to  be
produced by the IXRetail work team upon formation and is to include:

•  Team Name
•  Team Mission
•  Membership Roster
•  Business Justification
•  Mission Scope
•  Use Case Survey
•  Planned Deliverables
•  Revision History
•  Domain Glossary

2.  Team Name

The name of this IXRetail Work Team is Inventory.

3.  Team Mission

The mission of the IXRetail Inventory work-team:

Build  XML  schemas  that  support  transactions  between  systems  that  query,  reserve  and
record  real  time,  store  level  units  and  financial  value  inventory,  as  defined  within  the
common retail standards based on the ARTS data model.

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
3 of 11

4.  Membership Roster

Chairman
Author(s)

Contributor(s)

Tim Hood, Triversity
Bob Baker, CRS Retail Systems
Stuart McGrigor, ARTS
Tony Montgomery-Smith, PCMS-Datafit
Richard Halter, ARTS
Tom Barnes, GERS Retail Systems
Ian Brown, BP
Luciano Contratto, Getronics
James Easen, BP
Steve Gannon, 360Commerce
Judy Grant, McDonald’s Corporation
John Hervey, Nat’l Assoc of Convenience Stores
Dave Mitchell, CRS Retail Systems
Tony Morse, Comtrol
David Olsen, CRS Retail Systems
David Plotkin, Longs Drug Stores, Inc.
Donald Rome, Retek Inc.
Ralph Schaeftlein, Karstadt/Itellium
Swetank Shekhar, ISS Retail
David Van Horn, SofTechnics
Monty Moncrief, Blockbuster
Dennis Blankenship, Clicks and Mortar
Warren Backer, Target
Dan Conway, Oracle Retail
Leonid Rubakhin, NSB
Jeff Sheldon, Datavantage

5.  Business Justification

Inventory  is  typically  the  largest  asset  on  a  retailer’s  balance  sheet.  In  order  for  that
inventory to be sold as finished goods and turned into revenue or to be utilized in daily
retail operations, it must be planned, sourced, purchased, allocated, tracked, replenished,
and available when needed to meet customer or business demand. As a result, data about
inventory  plays  a  major  role  in  efficiently  managing  a  retail  business,  and  systems  that
support  inventory  transactions  have  many  touch-points  to  various  other  systems,
functions, and business processes throughout the retail supply chain.

Specifically focusing on finished goods inventory, industry research clearly suggests that
efficient, real time inventory management drives revenue and profits:

•  15%  of  a  retailer’s  potential  revenue  is  lost  due  to  merchandise  marked  down

because of overstocks.1

•  8 – 12% of any given item in a retailer’s merchandise mix is out of stock when

and where the customer wants to purchase that item.2

1 Attributed to The Planning Factory, Ltd., www.planfact.co.uk.

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
4 of 11

While  the  benefits  of  more  efficient  retail  supply  chains  are  clear,  it  is  rare  that  one
vendor or one in-house developed solution will provide all of the required functionality to
fully manage all aspects of that supply chain. As a result, integration within and between
disparate inventory and supply chain systems, both internal and external to the retailer, is
required to better manage inventory. This type of systems integration can be challenging
for  any  retailer  because  there  are  significant  complexities  with  the  consistency  and
definition of inventory data as it passes from one supply chain system to another.

The  IXRetail  Inventory  standard  provides  the  required  data  definition  and  structure  for
real  time  inventory  management  through  the  use  of  pre-defined  XML  integration
schemas.  By utilizing these schemas, which are based on the ARTS standard data model,
vendors and in-house providers of inventory management and supply chain systems can
more effectively integrate disparate systems. Standards-based integration will reduce the
cost of systems deployment and maintenance and increase the performance of real-time
inventory visibility, perpetual inventory control, and collaborative planning with supply
chain partners.

6.  Mission Scope

Identify  all  the  common  use  cases  encompassing  interactions  between  Inventory,  retail
sales and other retail location applications, including:

•  Multi-Channel ordering & selling (Retail Transaction) including:

(cid:131)  Point of sale/service in a retail location
(cid:131)  eCommerce
(cid:131)  Mail order
(cid:131)  Catalogue shop
(cid:131)  Telephone sales

•  Fulfillment,  being  the  process  of  ensuring  that  the  product  purchased  reaches  the

customer.

•

Inventory replenishment, being the process of restocking Inventory at a retail location

•  Customer-based returns of purchased product

•

Inter-store transfers or transfers between retail locations

•  Physical inventory or Inventory counts

•

Inventory adjustments

•  Query of Inventory availability and locations

•  Valuation of Inventory

2 Doug Bade of Deloitte Consulting, Supply Chain Strategy, as quoted in the Los Angeles
Times, 2001.

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
5 of 11

•  Vendor payment for inventory items (also known as “receipting”)

•  Any other Inventory transaction that affects units or financial value not already shown

above in the first phase of work

The above list of applications is the complete definition of the mission of the Inventory
Work  team,  which  equates  to  an  almost  overwhelming  effort  and  one  that  has  many
potential overlaps with other IXRetail schemas and Work Teams.  For example POSlog
contains  all  the  data  required  to  update  inventory  with  a  sale  or  return.    The  recently
created Warehouse Management Work Team will deal with data about transfers, receipts
and vendor returns.

Accordingly to provide retailers and vendors a standard schema to communicate current
inventory  on  hand  data,  the  initial  scope  of  the  Inventory  Work  Team  was  reduced  to
provide  this  information.    The  Inventory  Work  Team  will  coordinate  with  other  work
teams to ensure the data required to maintain an accurate store level on hand inventory is
available in standard IXRetail schemas.  Data not include in the schemas of other work
teams will be provided in future schemas developed by Inventory.

Figure 1: Sample of Inventory Retail Interfaces

7.  Use Case Survey

•  After review of sales and returns use cases from POS-Log appropriate inventory

related use-cases & scenarios were chosen:

o  Customer Sale
o  Customer Return

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
6 of 11

o  Customer Exchange
o  Customer Order

•

Inventory query, response and fulfillment

o  Inventory lookup
o  Inventory Reservation
o  Fulfillment

•

Inventory Count

o  Cycle counts
o  Physical Inventory
o  Inventory Adjustments
•  Recording of Inventory Flow

o  Transfer In & Out of Retail Locations

•

Interface  with  a  Warehouse  Management  System  (this  work  will  be  tied  to  the
Warehouse Management Work team)

o  Receiving Inventory
o  Return to Vendor
o  Purchase Order/Requisition
o  Manufacturer Return / Recall
o  Salvage/Liquidate/Donate to Charity

•  Valuation updates & queries (financials are reserved for a future version)

o  Pricing updates for retail valuation of Inventory
o  Cost updates from Receiving & Returns for Inventory
o  Payment to vendor for Inventory

All  use  cases  and  scenarios  will  be  documented  in  a  standard  format  as  shown  below:

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
7 of 11

USE CASE: ITEM PURCHASE

One  or  more  items  are  purchased  via  any  one  of  a  number  of  sales  channels.  The
transaction  is  entered  in  via  an  appropriate  application,  and  is  sent  using  the  Inventory
schema  to  the  Inventory  application,  which  may  forward  to  the  transaction  to  other
applications in the enterprise.

Scenario: Item Purchase at POS

Brief Description

Customer  selects  one  or  more  items  and  purchases  them.  The  number  of  those  items
available in inventory is decremented.

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
8 of 11

 Data

Identifiers for Store, Workstation, & Operator performing the transaction.

(cid:131)  Transaction header data, including:
(cid:131)
(cid:131)  The date & time the transaction was performed
(cid:131)  A workstation assigned sequence number identifying the transaction
(cid:131)
(cid:131)  An identifier for the item being sold.
(cid:131)  The number of multiples of the item being sold.
(cid:131)  Unit price for the item being sold.
(cid:131)  The extended amount (i.e. Unit price * the number of items being sold)

Item sale data, including:

Data Hierarchy Diagram

POSLog

1

1..*

Transaction

-@CancelFlag
-@TrainingModeFlag
-@OfflineFlag
-RetailStoreID
-WorkstationID
-SequenceNumber
-BusinessDayDate
-BeginDateTime
-EndDateTime
-OperatorID
-CurrencyCode

Total

-@TotalType
-Amount

0..1

1

-@OutsideSalesFlag
-@SuspendFlag
-TillID
-SpecialOrderNumber
-ReceiptDateTime

1..*

1

LineItem

-@VoidFlag
-@EntryMethod
-SequenceNumber
-BeginDateTime
-EndDateTime

0..1

1

1

POSIdentity

-@POSIDType
-POSItemID
-Qualifier

Quantity

1

-@Units
-@UnitOfMeasureCode

Sale

-@ItemType
-ItemID
-MerchandiseHierarchy
-Description
-UnitCostPrice
-UnitListPrice
-RegularSalesUnitPrice
-InventoryValuePrice
-ActualSalesUnitPrice
-ExtendedAmount
-SerialNumber
-ItemLink

1

1

IXRetail Inventory Charter

Revision Date:
September 13, 2005

Page
9 of 11

Example XML

<?xml version="1.0" encoding="UTF-8"?>
<!-- UseCase: Item Purchase from shelf                -->
<!-- Note: This example includes all optional fields  -->
<POSLog xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
POSLogRetailTransactionStockView.xsd">
  <Transaction
    xsi:type="RetailTransactionStockView"
    Version="1.0"
    CancelFlag="false"
    TrainingModeFlag="false"
    OfflineFlag="false"
    OutsideSalesFlag="false"
    SuspendFlag="false">
    <RetailStoreID>HighStreet</RetailStoreID>
    <WorkstationID>POS5</WorkstationID>
    <SequenceNumber>4294967295</SequenceNumber>
    <BusinessDayDate>2001-08-13</BusinessDayDate>
    <BeginDateTime>2001-08-13T09:03:00</BeginDateTime>
    <EndDateTime>2001-08-13T09:05:00</EndDateTime>
    <OperatorID>John</OperatorID>
    <CurrencyCode>USD</CurrencyCode>
    <LineItem VoidFlag="false">
      <SequenceNumber>1</SequenceNumber>
      <BeginDateTime>2001-09-16T09:04:00</BeginDateTime>
      <Sale ItemType="Stock">
        <POSIdentity>
          <POSItemID>01234567890123</POSItemID>
        </POSIdentity>
        <ItemID>CA7865</ItemID>
        <MerchandiseHierarchy
Level="Department">Chocolates</MerchandiseHierarchy>
        <Description>4oz Dark Chocolate</Description>
        <UnitListPrice>1.79</UnitListPrice>
        <RegularSalesUnitPrice>1.63</RegularSalesUnitPrice>
        <ActualSalesUnitPrice>1.63</ActualSalesUnitPrice>
        <ExtendedAmount>4.89</ExtendedAmount>
        <Quantity>3</Quantity>
      </Sale>
    </LineItem>
  </Transaction> </POSLog>
8.  Planned Deliverables

Deliverable

Updated working draft
Completed working draft
Submitted to technical committee for review
Resubmitted to technical committee for review
Publish for public comment

Estimated Date  Actual Date
12-Sep-02
15-Aug-02
11-Feb-03
10-Feb-03
12-Feb-03
12-Feb-03
11-Nov-03
11-Nov-03
13-Sept-05
01-Dec-03

9.  Revision History

Initial working draft
Updated working draft

Event

Date

15-Jul-02
12-Sep-02

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
