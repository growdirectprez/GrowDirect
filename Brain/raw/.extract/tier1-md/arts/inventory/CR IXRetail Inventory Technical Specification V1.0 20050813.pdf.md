IXRetail Inventory Technical Specification

Version 1.0

September 13, 2005  – Candidate Recommendation

Chairman:
Version 1:
Tim Hood

Work Team Members:
Version 1:

Dan Conway
Reza Attarha
David VanHorn
Dennis Blankenship
Leonid Rubakhin
Paul Faha
Warren Backer
Jeff Sheldon
Dave Moorman
Monty Moncrief
Tony Montgomery-Smith
Bob Baker
Stuart McGrigor

Triversity

Oracle|Retek
QPos
SofTechnics
Clicks and Mortar
NSB
CRS Retail
Target
Datavantage
PCMS
Blockbuster
PCMS-Datafit
CRS Retail Systems
ARTS

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 1

IXRetail Inventory Technical Specification V1.0

Richard Halter

Guests:
Version 1:
Tom Barnes
Graham Hill
Ron McEvoy
Bob Hoblit
Mike Bertrand
Ian Brown
Luciano Contratto
James Easen
Steve Gannon
Judy Grant
John Hervey
Dave Mitchell
Tony Morse
Ian Naylor
David Olsen
David Plotkin
Donald Rome
Swetank Shekhar
David Moorman
Luis Oliveira
Dennis Connelly

MIC

GERS Retail Systems
PCMS
Soft Solutions
IBM
StepUp
BP
Getronics
BP
360 Commerce
McDonald’s Corporation
Nat’l Assoc of Convenience Stores
CRS Retail Systems
Comtrol
Retail Systems Consultancy
CRS Retail Systems
Longs Drug Stores, Inc.
Retek Inc.
ISS Retail
PCMS
360 Commerce
ADS Retail

Copyright © National Retail Federation 2005. All rights reserved.

This document and translations of it may be copied and furnished to others, and derivative works that comment on or otherwise explain it or assist in its implementation may be
prepared, copied, published and distributed, in whole or in part, without restriction of any kind, provided that the above copyright notice and this paragraph are included on all such
copies and derivative works.  However, this document itself may not be modified in any way, such as by removing the copyright notice or references to the NRF, ARTS, or its
committees,  except  as  needed  for  the  purpose  of  developing  ARTS  standards  using  procedures  approved  by  the  NRF,  or  as  required  to  translate  it  into  languages  other  than
English.

The limited permissions granted above are perpetual and will not be revoked by the National Retail Federation or its successors or assigns.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 2

IXRetail Inventory Technical Specification V1.0

TABLE OF CONTENTS

1.

2.

3.

4.

5.

6.

7.

8.

INTRODUCTION .......................................................................................................................................................................... 7
1.1  Document Scope.................................................................................................................................................................. 7
TYPOGRAPHICAL CONVENTIONS .............................................................................................................................. 7
1.2
System Integration............................................................................................................................................................. 11
1.3
1.4  Outstanding Issues............................................................................................................................................................. 15
1.5  Reference Documents........................................................................................................................................................ 16
USE CASE: INVENTORY LOOKUP ......................................................................................................................................... 16
Scenario: Invoker Performs Inventory Lookup through an Operator................................................................................ 17
2.1
2.2
Scenario: Invoker Performs Inventory Lookup without an Operator................................................................................ 20
USE CASE: INVENTORY RESERVATION.............................................................................................................................. 23
Scenario: Invoker Requests an Inventory Reservation Through an Operator ................................................................... 23
3.1
Scenario: Invoker Requests an Inventory Reservation without an Operator..................................................................... 27
3.2
Scenario: Reservation Completion .................................................................................................................................... 30
3.3
Scenario: Reservation Cancellation................................................................................................................................... 33
3.4
Scenario: Partial Completion............................................................................................................................................. 35
3.5
Scenario: Partial Cancellation ........................................................................................................................................... 39
3.6
3.7
Scenario: Reservation Lookup........................................................................................................................................... 42
USE CASE: INVENTORY UPDATE.......................................................................................................................................... 45
4.1
Scenario: Fulfillment of a product which is already sold.................................................................................................. 45
USE CASE: STOCK COUNT...................................................................................................................................................... 48
Scenario: Merchandiser Performs Cycle Count Request .................................................................................................. 49
5.1
Scenario: Stock Count Begin............................................................................................................................................. 52
5.2
5.3
Scenario: Stock Count Complete....................................................................................................................................... 54
USE CASE: INVENTORY POSITION STATEMENT .............................................................................................................. 57
6.1
Scenario: Master Inventory system publishes an inventory position statement................................................................ 57
Scenario: Host system requests an inventory position statement from a store based inventory system ........................... 60
6.2
USE CASE: INVENTORY ADJUSTMENT ............................................................................................................................... 64
7.1
Scenario: Adjustment of quantity based on a shrink event ............................................................................................... 64
USE CASE: TRANSFERS ........................................................................................................................................................... 66
Scenario: Invoker Performs Inventory Transfer Out......................................................................................................... 66
8.1
8.2
Scenario: Invoker Performs Inventory Transfer In............................................................................................................ 70
SCHEMA IMPLEMENTATION ................................................................................................................................................. 73
DOCUMENT HISTORY.............................................................................................................................................................. 73
© 2005 International XML Retail Cooperative.  All rights reserved.
Page 3

9.
10.
Copyr
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

ight

IXRetail Inventory Technical Specification V1.0

11.
GLOSSARY ................................................................................................................................................................................. 73
APPENDIX A:.......................................................................................................................................................................................... 75
USE CASE: SALES ..................................................................................................................................................................... 75
1.
Scenario: Item purchase by Customer at Store.................................................................................................................. 75
1.1
Scenario: Item purchase via Mail Order, Fax or Telephone from Printed Catalog........................................................... 76
1.2
Scenario: Item purchase via WWW or Telephone ............................................................................................................ 77
1.3
1.4
Scenario: Catalogue SHOP................................................................................................................................................ 79
Scenario: Store Sale of Normally Stocked Item Not In Stock .......................................................................................... 81
1.5
USE CASE: RETURNS ............................................................................................................................................................... 83

2.

 Table of Figures
Figure 1: Interaction Diagram Example ..................................................................................................................................................... 8
Figure 2: Sample Domain Model................................................................................................................................................................ 9
Figure 3: Domain Model Legend.............................................................................................................................................................. 10
Figure 4: Sales Interaction Example ......................................................................................................................................................... 11
Figure 5: Customer Order Tracking Example .......................................................................................................................................... 13
Figure 6: Fulfillment of Customer Orders Interaction Example............................................................................................................... 14
Figure 7: Physical Inventory, Cycle Count, Stock Take Interaction Example ......................................................................................... 15
Figure 8: Invoker Performs Inventory Lookup through an Operator Domain Model .............................................................................. 19
Figure 9: Invoker Performs Inventory Lookup without an Operator Domain Model .............................................................................. 22
Figure 10: Invoker Requests an Inventory Reservation Through on Operator Domain Model ............................................................... 25
Figure 11: Invoker Requests an Inventory Reservation without an Operator Domain Model ................................................................. 28
Figure 12: Reservation Completion Domain Model................................................................................................................................. 31
Figure 13: Reservation Cancellation Domain Model ............................................................................................................................... 34
Figure 14: Partial Completion Domain Model ......................................................................................................................................... 37
Figure 15: Partial Cancellation Domain Model ........................................................................................................................................ 40
Figure 16: Reservation Lookup Domain Model ....................................................................................................................................... 43
Figure 17: Fulfillment ships a non-reserved Item from Inventory Domain Model .................................................................................. 47
Figure 18: Merchandiser Performs Cycle Count Request Domain Model ............................................................................................... 50
Figure 19: Stock Count Begin Domain Model ......................................................................................................................................... 53
Figure 20: Stock Count Complete Domain Model ................................................................................................................................... 55
Figure 21: Master inventory system issues synchronization to store inventory system ........................................................................... 59
Figure 22: Store inventory management system requests an inventory position statement from a master inventory system.................. 62
Figure 23: system issues inventory adjustment to store inventory system ............................................................................................... 65
Figure 24: Invoker Performs Inventory Transfer Out Domain Model ..................................................................................................... 68
Figure 25: Invoker Performs Inventory Transfer In Domain Model ........................................................................................................ 71

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 4

IXRetail Inventory Technical Specification V1.0

Figure 28: Item purchase via WWW or Telephone Interaction Diagram Example ................................................................................. 78
Figure 29: Catalogue SHOP Interaction Diagram Example ..................................................................................................................... 80
Figure 30: Store Sale of Normally Stocked Item Not In Stock Interaction Diagram Example................................................................ 82
Figure 31: Returns Interaction Diagram Example .................................................................................................................................... 85

Table of IXRetail XML Samples
1-02-01 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Lookup through an Operator................. 20
1-02-01 IXRetail Conformance XML Instance Doc – Response - Invoker Performs Inventory Lookup through an Operator .............. 20
1-03-02 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Lookup without an Operator................. 23
1-03-02 IXRetail Conformance XML Instance Doc – Response - Invoker Performs Inventory Lookup without an Operator .............. 23
1-03-01 IXRetail Conformance XML Instance Doc – Request - Invoker Requests an Inventory Reservation through an Operator ..... 25
1-03-01 IXRetail Conformance XML Instance Doc – Response - Invoker Requests an Inventory Reservation through an Operator ... 26
1-03-01 IXRetail Conformance XML Instance Doc – Response Failure - Invoker Requests an Inventory Reservation through an

Operator ............................................................................................................................................................................................ 26
1-03-02 IXRetail Conformance XML Instance Doc – Request - Invoker Requests an Inventory Reservation without an Operator...... 28
1-03-02 IXRetail Conformance XML Instance Doc – Response - Invoker Requests an Inventory Reservation without an Operator ... 29
1-03-02 IXRetail Conformance XML Instance Doc – Response Failure - Invoker Requests an Inventory Reservation without an

Operator ............................................................................................................................................................................................ 29
1-03-03 IXRetail Conformance XML Instance Doc – Request - Reservation Completion ..................................................................... 31
1-03-03 IXRetail Conformance XML Instance Doc – Response - Reservation Completion................................................................... 32
1-03-03 IXRetail Conformance XML Instance Doc – Response Failure - Reservation Completion ...................................................... 32
1-03-04 IXRetail Conformance XML Instance Doc – Request - Reservation Cancellation.................................................................... 35
1-03-04 IXRetail Conformance XML Instance Doc – Response - Reservation Cancellation ................................................................. 35
1-03-04 IXRetail Conformance XML Instance Doc – Response Failure - Reservation Cancellation ..................................................... 35
1-03-05 IXRetail Conformance XML Instance Doc – Request - Partial Completion.............................................................................. 38
1-03-05 IXRetail Conformance XML Instance Doc – Response - Partial Completion ........................................................................... 38
1-03-05 IXRetail Conformance XML Instance Doc – Response Failure - Partial Completion ............................................................... 39
1-03-06 IXRetail Conformance XML Instance Doc – Request - Partial Cancellation............................................................................. 40
1-03-06 IXRetail Conformance XML Instance Doc – Response - Partial Cancellation .......................................................................... 41
1-03-06 IXRetail Conformance XML Instance Doc – Response Failure - Partial Cancellation.............................................................. 41
1-03-07 IXRetail Conformance XML Instance Doc – Request - Reservation Lookup............................................................................ 44
1-03-07 IXRetail Conformance XML Instance Doc – Response - Reservation Lookup ......................................................................... 44
1-03-07 IXRetail Conformance XML Instance Doc – Response Failure - Reservation Lookup............................................................. 45
1-04-01 IXRetail Conformance XML Instance Doc – Request - Fulfillment ships a non-reserved Item from Inventory....................... 47
1-04-01 IXRetail Conformance XML Instance Doc – Response - Fulfillment ships a non-reserved Item from Inventory .................... 48
1-04-01 IXRetail Conformance XML Instance Doc – Response Failure - Fulfillment ships a non-reserved Item from Inventory........ 48

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 5

IXRetail Inventory Technical Specification V1.0

1-05-01 IXRetail Conformance XML Instance Doc – Request - Merchandiser Performs Cycle Count Request.................................... 51
1-05-01 IXRetail Conformance XML Instance Doc – Response - Merchandiser Performs Cycle Count Request ................................. 51
1-05-01 IXRetail Conformance XML Instance Doc – Response Failure - Merchandiser Performs Cycle Count Request..................... 52
1-05-02 IXRetail Conformance XML Instance Doc – Request - Stock Count Begin.............................................................................. 54
1-05-03 IXRetail Conformance XML Instance Doc – Request - Stock Count Complete........................................................................ 56
1-05-03 IXRetail Conformance XML Instance Doc – Response - Stock Count Complete ..................................................................... 56
1-05-03 IXRetail Conformance XML Instance Doc – Response Failure - Stock Count Complete ......................................................... 57
1-06-01 IXRetail Conformance XML Instance Doc – Publish - Master Inventory system publishes an inventory position statement to a
store based inventory system ............................................................................................................................................................ 60
1-06-02 IXRetail Conformance XML Instance Doc – Request - Invoker Requests an Inventory Position Statement ............................ 63
1-06-02 IXRetail Conformance XML Instance Doc – Response - Invoker Requests an Inventory Positon Statement........................... 63
1-06-02 IXRetail Conformance XML Instance Doc – Response Failure - Invoker Requests an Inventory Position Statement ............. 63
1-07-01 IXRetail Conformance XML Instance Doc – Publish - Master Inventory system publishes an inventory adjustment to a store

based inventory system ..................................................................................................................................................................... 66
1-08-01 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Transfer Out .......................................... 69
1-08-02 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Transfer In............................................. 72

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 6

IXRetail Inventory Technical Specification V1.0

1.  INTRODUCTION

1.1  Document Scope

Identify all the common use cases encompassing interactions between Inventory, retail sales and other store applications, including:

•  Point of sale/service in store, eCommerce, mail order, catalogue shop and telephone sales

•  Fulfillment, being the process of ensuring the product purchased reaches the customer

•  Returns of purchased product

•

•

Inter-store transfers

Inventory checking

•  Stock write-off

This phase of the work should not include:

•

Inventory replenishment

•  Any financial aspect, including payment and valuation

Identify the normal information flows, and the messages supporting them within these interactions.

Specify the content of the messages and define the schemas for them.

Ensure that the project builds on and, where possible, is compatible with prior work in this field, in particular that done by Active
Store.

The prime reason for limiting the initial work in this way was facilitate the early delivery of useful schemas.

1.2  TYPOGRAPHICAL CONVENTIONS

The following typographical and diagramming conventions are used in this document.

Interaction Diagram

The following Interaction Diagram shows the following typographical conventions for the interaction diagrams in this document:

•

Interactions shown in blue are those interactions that are covered by the Inventory Schema; any particular interaction shown
may or may not be used in any particular implementation.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 7

IXRetail Inventory Technical Specification V1.0

•

Interactions  shown  in  green  are  not  covered  by  the  Inventory  Schema  and  are  included  to  show  how  Inventory  works  with
POSLog to provide complete functionality.

Sales

Product Selection

Inventory Enquiry

Inventory

Inventory Enquiry

Inventory Reservation

Inventory Reservation

Cancel Reservation

Cancel Reservation

Payment

Post to POSLog

POS-Log

Update Inventory
Release Reservation

Inventory Data

POSLog Data

Figure 1: Interaction Diagram Example

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 8

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 9

Figure 2: Sample Domain Model

IXRetail Inventory Technical Specification V1.0

Key:

Name

Name

Data Element

Data Element (not verified by use cases)

Generalization of complex type by extension

Generalization of element by choice

Inclusion of complex data element (Type Definition)

@Name Name is an attribute in the containing element -

Enumerations are located beside the node.

+Name Name is a mixed content element in the containing
element.

Default Attribute is in Italics

Class1

Common Data in Blue
See Common Data Technical Spec for
Current Details

Figure 3: Domain Model Legend

Example XML

The following Example XML document is shows the following typographical conventions for the Example XML in this document:

•  The XML fragments are a complete XML instance document showing all schema and name space declarations.
•  Comments in navy blue list how the example XML differs from other example XML fragments in this document.
•  The XML elements in red are interesting features of the XML fragment.

<?xml version="1.0" encoding="UTF-8"?>
<InventoryLookupRequest
  xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ Inventory.xsd">
  <ItemID>676623054746</ItemID>
  <Quantity>3</Quantity>
  <Location>

<RetailStoreID>MailOrder</RetailStoreID>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 10

IXRetail Inventory Technical Specification V1.0

<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

  </Location>
  <DateTime>2004-08-13T16:00:00</DateTime>
</InventoryLookupRequest>

1.3  System Integration

Sales

There  is  a  common  pattern  of  information  flow  between  sales,  whether  in-store,  eCommerce,  mail  order  or  any  other  channel,  and
Inventory. Particular use cases only differ in that they omit part of the pattern.

Sales

Product Selection

Inventory Enquiry

Inventory

Inventory Enquiry

Inventory Reservation

Inventory Reservation

Cancel Reservation

Cancel Reservation

Payment

Post to POSLog

POS-Log

Update Inventory
Release Reservation

Figure 4: Sales Interaction Example

There is an initial product selection process, not involving Inventory. This may be physical selection, as in a store, or it may require
access to a catalogue. The process is responsible for precise product identification, and for identification of alternatives.

Once  the  items  are  identified  explicitly  with  an  item  ID  (PLU  or  SKU  code),  there  may  be  an  immediate  stock  availability  check,
comprising a query and response. This activity takes place typically line by line.

The product selection/stock availability process can iterate. The user may only perceive one process, with stock availability shown at
selection time.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 11

IXRetail Inventory Technical Specification V1.0

Once stock is known to be available, it can be reserved, with a reservation request acknowledged by a confirmation. This activity may
be  delayed  until  the  basket  is  believed  complete.  It  is  therefore  quite  possible  that  the  stock  may  no  longer  be  available,  and  the
response may indicate this.

There may then be a payment process, which may fail.

If the payment process fails, there needs to be a cancel reservation process. The norm is that the cancel reservation explicitly states
what  is  to  be  cancelled,  rather  than  relying  on  the  inventory  system  to  remember  what  is  in  the  basket.  Obviously,  particular
organizations could do this differently.

Finally, the transaction is posted to the POS-Log, which is subsequently forwarded to Inventory.

The check availability, reserve stock and cancel stock reservation processes are essentially interactive and synchronous. The post to
POS-Log and subsequently to Inventory is essentially asynchronous. This does not mean that it is slow – it can take from milliseconds
to hours. It means that the sales process does not wait for it to complete, as it does for the other processes.

A transaction in the POS-Log may be asserting different things: it may be an order for subsequent Fulfillment, or it may be a record of
a sale. This difference is quite independent of whether the goods had been paid for.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 12

IXRetail Inventory Technical Specification V1.0

Customer order tracking

Sales

Product Selection

Inventory Enquiry

Inventory

Inventory Enquiry

Inventory Reservation

Inventory Reservation

Cancel Reservation

Cancel Reservation

Payment

Post to POSLog

POS-Log

Customer
Order Tracking

Notify of
Replenishment

Figure 5: Customer Order Tracking Example

When a customer orders a stock item that is not currently in stock, there may be a post-sale process in which the customer orders are
filed. When the item comes into stock, the customer is notified.

There is an issue whether Inventory is responsible for this notification. As an alternative, there can be a separate order tracking system,
with Inventory simply responsible for notifying it when items that were out of stock are replenished.

Once the customer has been notified, he comes back into the regular sales process.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 13

IXRetail Inventory Technical Specification V1.0

Fulfillment of Customer Orders

Although Fulfillment may be a complex process, the team believes that the relationship with Sales and Inventory is fairly clear cut:

Sales

Product Selection

Inventory Enquiry

Inventory

Inventory Enquiry

Inventory Reservation

Inventory Reservation

Cancel Reservation

Cancel Reservation

Payment

Post to POSLog

POS-Log

Fulfillment

Update Inventory
Release Reservation

POS-Log

Update Inventory
Release Reservation

Figure 6: Fulfillment of Customer Orders Interaction Example

As  far  as  Inventory  is  concerned,  the  sole  impact  of  a  Fulfillment  process,  as  opposed  to  immediate  delivery,  is  that  the  POS-Log
record arrives later from a different source.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 14

IXRetail Inventory Technical Specification V1.0

Physical Inventory, Cycle Count, Stock Take

Stock Checking

Inventory

Query book stock for
item

Count

Return physical or delta
count

Deliver book stock
figures

Update book stock
figures

Stock Checking

Inventory

Count

Deliver count list

Return physical count

Update book stock
figures

Return delta count

Demand Recount

Conceptually, there is a stock checking system, separate from Inventory.

Figure 7: Physical Inventory, Cycle Count, Stock Take Interaction Example

There  are  (at  least)  2  schemes  for  managing  this.  The  first  is  driven  from  the  stock  checking  end.  Stock  Checking  possibly  first
requests the book balances of particular items. It submits counts, or calculated delta counts.

The  second  is  driven  by  Inventory.  Stock  Checking  is  sent  instructions  on  what  to  count,  but  not  told  the  balances.  It  returns  the
physical counts. If Inventory finds the results unacceptable, because they differ excessively from book stock, it may demand a recount.

1.4  Outstanding Issues

1.  Item identification. Retail organizations have a choice whether to use the bar codes that are printed on the items sold, or to
devise  an  item  coding  of  their  own.  The  bar  codes  are  often  called  PLU  codes,  and  are  named  POSItemID  in  the  IXRetail
dictionary.  They  typically  need  to  be  supplemented  by  some  internally  generated  codes  for  items  without  bar  codes,  for
instance loose fruit and vegetables. The internal codes are often called SKU (Stock Keeping Unit) codes. There is typically a

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 15

IXRetail Inventory Technical Specification V1.0

one-to-many relationship between ItemID and POSItemID. For instance, cans of coke may be all the same as far as inventory
is concerned, but carry different POSItemIDs depending on where they were manufactured. Note also that the UPC or EAN
code may have an extension code which is essential for Inventory. An example is the code needed to specify the day of the
week for a newspaper.

   The schemas presented in this document all allow a choice of POSItemID, ItemID, or both. Obviously, any particular retail

organization needs to have its own rules for deciding which to use.

   Furthermore, items can be grouped in hierarchies, typically called product catalogs.  Inventory assumes that all requests are at
the elemental item level for individual products.  No product catalog requests at levels above the elemental item are considered
to be in scope for Inventory at this time.

2.  Location identification. As far as Inventory is concerned, retail locations may have an internal hierarchical structure.  The top
level in this structure may be stores or warehouses. For instance, a warehouse might be divided into sheds, then aisles, then
shelves. A store might be divided into the display and backup areas. The display area (the store proper), might be divided into
departments, then aisles, then shelves. All Inventory-related messages need one location ID (or 2 location IDs for transfers).
The Inventory schema does not include the ability to interpret the location hierarchy.

3.  Responsibility for product identification. Product identification is in the scope of the Item work team.

4.  Matching  responses  to  queries.  It  is  assumed  that  the  infrastructure  provides  a  mechanism  to  enable  an  application  making
queries to match any responses back to the original query. It is therefore not generally necessary for responses to echo back
information contained in the query.

5.  Kits (or menus in the food business) require that either Inventory or Sales know how to work them. However, while a local
protocol needs to be established for whether messages are in terms of components or complete units, the messages themselves
and the message flow are unaffected.

1.5  Reference Documents

IXRetail POS-Log Technical Specification V2.1

IXRetail Item Technical Specification V1.0

IXRetail Common Data

2.  USE CASE: INVENTORY LOOKUP

One  or  more  inventory  items  may  be  located  at  various  retail  locations  throughout  a  retail  enterprise.    A  query  is  generated  to
determine  information  about  those  retail  items,  including,  but  not  limited  to,  their  retail  locations,  their  quantities,  and  their

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 16

IXRetail Inventory Technical Specification V1.0

dispositions.  Inventory lookup may take place as a freestanding process or, typically, it may be a part of a larger transactional process,
e.g., an item purchase.

2.1  Scenario: Invoker Performs Inventory Lookup through an Operator

Brief Description

Invoker has identified one inventory item upon which to perform an inventory lookup utilizing an operator.  For example, a customer
asks a cashier to check on availability for a particular item at a particular retail location and gets a response for all locations for the
item.

Pre Condition

1.  Invoker knows the Identification of the item

Post Condition

1.  List of item/quantity data elements

Business Error

1.  Item unknown
2.  (unable to resolve other parameters)

Data

o  Inventory Lookup request data, including:
o  ItemID (as defined by common data work team and/or POSLog)

o  Location (Optional: retail location where located, e.g., warehouse, backroom, aisles, bins)
o  Date & Time (Optional): The date & time at which the inventory information is being requested. (e.g How many “in

stock” at 4pm next Friday)

o  Inventory State (Optional: current disposition of inventory item, e.g., available for sale, in transit)
o  Inventory Lookup response data, matrix combining:

o  ItemID
o  Location (Optional: retail location where located, e.g., warehouse, backroom, aisles, bins)
o  Date & Time (Optional)

o  Inventory State (Optional: current disposition of inventory item, e.g., available for sale)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 17

IXRetail Inventory Technical Specification V1.0

o  Quantity (Optional)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 18

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 8: Invoker Performs Inventory Lookup through an Operator Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 19

IXRetail Inventory Technical Specification V1.0

1-02-01 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Lookup through an Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Lookup">

<RequestID>12343465</RequestID>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">Store 72</BusinessUnit>

</InventoryLocation>
<ItemID Type="SKU">12343456</ItemID>

</InventoryAction>

</Inventory>

1-02-01 IXRetail Conformance XML Instance Doc – Response - Invoker Performs Inventory Lookup through an Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Inventory" Action="Lookup">

<Response ResponseCode="OK">

<RequestID>12343465</RequestID>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<ItemLocation State="AvailableToSell">

<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">Store 72</BusinessUnit>
<ExactLocation Level="Bay">Technical Books</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">2</Quantity>

</ItemLocation>
<ItemLocation State="AvailableOnHand">

<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">Store 72</BusinessUnit>
<ExactLocation Level="Area">Loading Dock</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">24</Quantity>

</ItemLocation>

</InventoryAction>

</Inventory>

2.2  Scenario: Invoker Performs Inventory Lookup without an Operator

Brief Description

Invoker has identified one inventory item upon which to perform an inventory lookup without utilizing an operator.  For example, a
customer works directly with a kiosk-based application to check on availability for a particular item at a particular retail location.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 20

IXRetail Inventory Technical Specification V1.0

Pre Condition

1.  Invoker knows the Identification of the item

Post Condition

1.  List of item/quantity data elements

Business Error

1.  Item unknown
2.  (unable to resolve other parameters)

Data

o  Inventory Lookup request data, including:
o  ItemID (as defined by common data work team and/or POSLog)

o  Location (Optional: retail location where located, e.g., warehouse, backroom, aisles, bins)
o  Date & Time (Optional): The date & time at which the inventory information is being requested. (e.g How many “in

stock” at 4pm next Friday)

o  Inventory State (Optional: current disposition of inventory item, e.g., available for sale, in transit)
o  Inventory Lookup response data matrix combining:

o  ItemID
o  Location (Optional: retail location where located, e.g., warehouse, backroom, aisles, bins)
o  Date & Time (Optional)

o  Inventory State (Optional: current disposition of inventory item, e.g., available for sale)
o  Quantity (Optional)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 21

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 9: Invoker Performs Inventory Lookup without an Operator Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 22

IXRetail Inventory Technical Specification V1.0

1-03-02 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Lookup without an Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Lookup" InventoryState="AvailableToSell">

<RequestID>asdfasdf</RequestID>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">Store72</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

</InventoryLocation>
<ItemID Type="SKU">676623054746</ItemID>

</InventoryAction>

</Inventory>

1-03-02 IXRetail Conformance XML Instance Doc – Response - Invoker Performs Inventory Lookup without an Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Inventory" Action="Lookup">

<Response>

<RequestID>asdfasdf</RequestID>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">Store72</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">2</Quantity>

</InventoryAction>

</Inventory>

3.  USE CASE: INVENTORY RESERVATION

An Invoker makes a reservation for one or more inventoried items, this implies intent by the Invoker to buy the inventory items as
well as an undertaking by the retailer to provide some level of guarantee that the reserved items will be available at a particular place
and time.

3.1  Scenario: Invoker Requests an Inventory Reservation Through an Operator

Brief Description

Invoker  has  identified  one  inventory  item  to  reserve  utilizing  an  operator.    For  example,  a  customer  asks  a  cashier  to  reserve  a
particular item at a particular retail location on a particular date for pick up.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 23

IXRetail Inventory Technical Specification V1.0

Pre Condition

1.  Invoker knows the Identification of the item

Post Condition

Business Error

1.  Unknown item
2.  unable to reserve item/amount requested
3.  (unable to resolve other parameters)

Data

o  Inventory Reservation data, including:
o  Item ID - as defined by common data work team and/or POSLog
o  Quantity (Optional)

o  Location (Optional: retail location where the pick up of the inventory should be located, e.g., store number)
o  Reservation ID (Optional: may be the order number generated by Requestor)
o  Requested Pick up date & time (Optional: the date/time stamp that the reservation will be required for pick up)

o  Inventory Reservation response data, including:
o  Reservation accepted (TRUE or FALSE)
o  Reservation ID – may be an echo of the request Reservation ID, or may be a Inventory system generated ID
o  Quantity
o  Actual Pickup date & time. (Optional – may be different from requested)
o  Reservation rejection date & time (Optional).
o  Rejection reason code (Optional: extensible enumeration)
o  Rejection reason text (Optional: free form text)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 24

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Request

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

RequestIDCommonData

ItemIDCommonData

-@RequestorName[0..1]
-@Timestamp[0..1]

-@Qualifier[1]
-@Type[1]

QuantityCommonData

-@Units[1]
-@UnitOfMeasureCode[1]
-@EntryMethod[1]

BusinessUnitCommonData

-@Name[0..1]
-@TypeCode[1]

InventoryLocationType (cType)

-@Location[1]
-+BusinessUnit[0..1]
-SellingLocation[0..*]

1

0..*

ReservationType (cType)

-+BusinessUnit[1]
-WorkstationID[1]
-ReservationID[1]

ExactLocation

-@Level[1]

Response

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

BusinessErrorCommonData

-@Severity[1]
-ErrorID[0..1]
-Code[0..1]
-Description[0..1]
-RelatedError[0..*]

ResponseCommonData

-@ResponseCode[1]
-RequestID[1]
-ResponseTimestamp[0..1]
-ResponseDescription[0..1]
-+BusinessError[0..*]

Item Type (cType)

-Whole Item Type Schema[1]

Figure 10: Invoker Requests an Inventory Reservation Through on Operator Domain Model

1-03-01 IXRetail Conformance XML Instance Doc – Request - Invoker Requests an Inventory Reservation through an
Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Reservation" Action="Create">

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 25

IXRetail Inventory Technical Specification V1.0

 <
 <
 <

RequestID>2345</RequestID>
DateTime TypeCode="Effective">2001-12-17T09:30:47</DateTime>
InventoryLocation>

 <
 <
 <

BusinessUnit TypeCode="RetailStore">MailOrder</BusinessUnit>
SellingLocation>Shelf 23</SellingLocation>
ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

InventoryLocation>
ItemID>6766230544746</ItemID>

 </
 <
 < Operator>12345</Operator>
 < Quantity>2</Quantity>
 <

Reservation>

BusinessUnit TypeCode="RetailStore">eStore</BusinessUnit>

 <
 < WorkstationID>Server2</WorkstationID>
 <

ReservationID>4294967295</ReservationID>

 </
Reservation>
</InventoryAction>

</Inventory>

1-03-01 IXRetail Conformance XML Instance Doc – Response - Invoker Requests an Inventory Reservation through an
Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Create" AcceptedFlag="true">
 <

Response ResponseCode="OK">
RequestID>2345</RequestID>

 <

Response>
DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>

 </
 <
 < Quantity Units="1" UnitOfMeasureCode="EA">2</Quantity>
 <
</InventoryAction>

ReservationID>4294967295</ReservationID>

</Inventory>

1-03-01 IXRetail Conformance XML Instance Doc – Response Failure - Invoker Requests an Inventory Reservation through
an Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Create" AcceptedFlag="false">
 <

Response ResponseCode="Rejected">
RequestID>2345</RequestID>
BusinessError>

 <
 <

<Code>OutOfStock</Code>

 </

BusinessError>

 </
 <
 <

Response>
DateTime TypeCode="Expiration">2001-12-17T09:30:47</DateTime>
InventoryItem State="AvailableToSell">

 < Quantity>10</Quantity>

 </

InventoryItem>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 26

IXRetail Inventory Technical Specification V1.0

</InventoryAction>

</Inventory>

3.2  Scenario: Invoker Requests an Inventory Reservation without an Operator

Brief Description

Invoker  has  identified  one  inventory  item  to  reserve  without  utilizing  an  operator.    For  example,  a  customer  uses  an  ecommerce
system to place an order – the ecommerce system then reserves the particular inventory item ordered.

Data

o  Inventory Reservation data, including:
o  Item ID - as defined by common data work team and/or POSLog

o  Quantity (Optional)
o  Location (Optional: retail location where the pick up of the inventory should be located, e.g., store number)
o  Reservation ID (Optional: may be the order number generated by Requestor)
o  Requested Pick up date & time (Optional: the date/time stamp that the reservation will be required for pick up)

o  Inventory Reservation response data, including:
o  Reservation accepted (TRUE or FALSE)
o  Reservation ID – may be an echo of the request Reservation ID, or may be a Inventory system generated ID
o  Quantity
o  Actual Pickup date & time. (Optional – may be different from requested)
o  Rejection reason code (Optional: extensible enumeration)
o  Rejection reason text (Optional: free form text)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 27

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Request

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

RequestIDCommonData

-@RequestorName[0..1]
-@Timestamp[0..1]

ItemIDCommonData

-@Qualifier[1]
-@Type[1]

QuantityCommonData

-@Units[1]
-@UnitOfMeasureCode[1]
-@EntryMethod[1]

BusinessUnitCommonData

-@Name[0..1]
-@TypeCode[1]

InventoryLocationType (cType)

-@Location[1]
-+BusinessUnit[0..1]
-SellingLocation[0..*]

ReservationType (cType)

-+BusinessUnit[1]
-WorkstationID[1]
-ReservationID[1]

1

0..*

ExactLocation

-@Level[1]

Response

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

BusinessErrorCommonData

-@Severity[1]
-ErrorID[0..1]
-Code[0..1]
-Description[0..1]
-RelatedError[0..*]

ResponseCommonData

-@ResponseCode[1]
-RequestID[1]
-ResponseTimestamp[0..1]
-ResponseDescription[0..1]
-+BusinessError[0..*]

Item Type (cType)

-Whole Item Type Schema[1]

Figure 11: Invoker Requests an Inventory Reservation without an Operator Domain Model

1-03-02 IXRetail Conformance XML Instance Doc – Request - Invoker Requests an Inventory Reservation without an
Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 28

IXRetail Inventory Technical Specification V1.0

<InventoryAction MessageType="Request" Type="Reservation" Action="Create">

<RequestID>1234</RequestID>
<DateTime TypeCode="Effective">2001-12-17T09:30:47</DateTime>
<DateTime TypeCode="Expiration">2001-12-17T09:30:47</DateTime>
<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">MailOrder</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

</InventoryLocation>
<ItemID Type="SKU">6766230544746</ItemID>
<Quantity>2</Quantity>
<Reservation>

<BusinessUnit TypeCode="RetailStore">eStore</BusinessUnit>
<WorkstationID>Server2</WorkstationID>
<ReservationID>4294967295</ReservationID>

</Reservation>
</InventoryAction>

</Inventory>

1-03-02 IXRetail Conformance XML Instance Doc – Response - Invoker Requests an Inventory Reservation without an
Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Create" AcceptedFlag="true">

<Response ResponseCode="OK">
<RequestID>1234</RequestID>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<Quantity Units="1" UnitOfMeasureCode="EA">2</Quantity>
<ReservationID>4294967295</ReservationID>

</InventoryAction>

</Inventory>

1-03-02 IXRetail Conformance XML Instance Doc – Response Failure - Invoker Requests an Inventory Reservation without
an Operator
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Create" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234</RequestID>
<ResponseDescription>Invalid Request</ResponseDescription>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 29

IXRetail Inventory Technical Specification V1.0

3.3  Scenario: Reservation Completion

Brief Description

Customer picks up or shipping delivers items which were previously reserved.

Pre Condition

1. Invoker knows the reservation ID

Post Condition

1. Reservation updated

Business Error

1.  reservation ID unknown
2.  (unable to resolve other parameters)

Data

Inventory Reservation Completion data including:

•  ReservationID

•  LineItems containing

o  ItemID & Quantity

o  Disposition Code (CustomerPickup or ShippingDispatch)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 30

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Request

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

RequestIDCommonData

-@RequestorName[0..1]
-@Timestamp[0..1]

ItemIDCommonData

-@Qualifier[1]
-@Type[1]

QuantityCommonData

-@Units[1]
-@UnitOfMeasureCode[1]
-@EntryMethod[1]

ItemLocationType (cType)

-@State[0..1]
-+InventoryLocation[1]
-+ItemID[0..1]
-+Quantity[0..1]
-ExpirationDateTime[0..1]
-EffectiveDateTime[0..1]
-DateTime[0..1]

BusinessUnitCommonData

-@Name[0..1]
-@TypeCode[1]

InventoryLocationType (cType)

-@Location[1]
-+BusinessUnit[0..1]
-SellingLocation[0..*]

0..*

1

ExactLocation

-@Level[1]

Response

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

BusinessErrorCommonData

-@Severity[1]
-ErrorID[0..1]
-Code[0..1]
-Description[0..1]
-RelatedError[0..*]

ResponseCommonData

-@ResponseCode[1]
-RequestID[1]
-ResponseTimestamp[0..1]
-ResponseDescription[0..1]
-+BusinessError[0..*]

Item Type (cType)

-Whole Item Type Schema[1]

Figure 12: Reservation Completion Domain Model

1-03-03 IXRetail Conformance XML Instance Doc – Request - Reservation Completion
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 31

IXRetail Inventory Technical Specification V1.0

<InventoryAction MessageType="Request" Type="Reservation" Action="Complete">

<RequestID>1234</RequestID>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<FromLocation>

<ItemID Type="SKU">6766230544746</ItemID>
<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">MailOrder</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

</InventoryLocation>
<Quantity>2</Quantity>
<Disposition>ShipToHome</Disposition>

</FromLocation>
<FromLocation>

<ItemID Type="SKU">6766230544723</ItemID>
<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">Store72</BusinessUnit>

</InventoryLocation>
<Quantity>18</Quantity>
<Disposition>CustomerPickup</Disposition>

</FromLocation>
<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

1-03-03 IXRetail Conformance XML Instance Doc – Response - Reservation Completion
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Complete" AcceptedFlag="true">

<Response ResponseCode="OK">
<RequestID>1243</RequestID>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

1-03-03 IXRetail Conformance XML Instance Doc – Response Failure - Reservation Completion
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Complete" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234</RequestID>
<BusinessError Severity="Error">

<Description>AlreadyComplete</Description>

</BusinessError>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 32

IXRetail Inventory Technical Specification V1.0

<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

3.4  Scenario: Reservation Cancellation

Brief Description

Customer changes their mind about purchasing previously reserved items before Fulfillment and the reservation is cancelled.   This
use case does not include charging of any cancellation fees.

Data

Inventory Reservation Cancellation data including:

•  ReservationID

•  Cancellation ReasonCode

Pre Condition

1. Invoker knows the reservation ID

Post Condition

1.Reservation updated

Business Error

1.  reservation ID unknown
2.  (unable to resolve other parameters)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 33

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 13: Reservation Cancellation Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 34

IXRetail Inventory Technical Specification V1.0

1-03-04 IXRetail Conformance XML Instance Doc – Request - Reservation Cancellation
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Reservation" Action="Cancel">

<RequestID>3254234</RequestID>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<ReservationID>1a2b3c</ReservationID>

</InventoryAction>

</Inventory>

1-03-04 IXRetail Conformance XML Instance Doc – Response - Reservation Cancellation
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Cancel" AcceptedFlag="true">

<Response ResponseCode="OK">

<RequestID>3254234</RequestID>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>1a2b3c</ReservationID>

</InventoryAction>

</Inventory>

1-03-04 IXRetail Conformance XML Instance Doc – Response Failure - Reservation Cancellation
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Cancel" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>3254234</RequestID>
<BusinessError Severity="Information">

<Description>Already Complete</Description>

</BusinessError>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>1a2b3c</ReservationID>

</InventoryAction>

</Inventory>

3.5  Scenario: Partial Completion

Brief Description

Customer orders a dozen of something, and then only takes 8 of them OR Customer orders 3 different things and only two of them are
delivered in first delivery.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 35

IXRetail Inventory Technical Specification V1.0

Data

Inventory Reservation Partial Completion data including:

•  ReservationID

•  Partial Completion ReasonCode

•  LineItems containing

o  ItemID & Quantity

o  DispositionCode (CustomerPickup or ShippingDispatch)

Pre Condition

1.Invoker knows the reservation ID

Post Condition

1.Reservation updated

Business Error

1.  reservation ID unknown
2.  unable to satisfy request
3.  (unable to resolve other parameters)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 36

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 14: Partial Completion Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 37

IXRetail Inventory Technical Specification V1.0

1-03-05 IXRetail Conformance XML Instance Doc – Request - Partial Completion
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">
<InventoryAction MessageType="Request" Type="Reservation" Action="PartialComplete">
 <
 <
 <
 <

RequestID>1234567</RequestID>
DateTime>2001-12-17T09:30:47</DateTime>
Disposition>CustomerPickup</Disposition>
FromLocation>

 <
 <

ItemID>6766230544746</ItemID>
InventoryLocation>

<BusinessUnit TypeCode="RetailStore">MailOrder</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

InventoryLocation>

 </
 < Quantity>8</Quantity>

 </
 <
 <

FromLocation>
ReservationID>2323</ReservationID>
TransactionNumber>

 <
BusinessUnit>eStore</BusinessUnit>
 < WorkstationID>Server2</WorkstationID>
 <

SequenceNumber>4294967295</SequenceNumber>

TransactionNumber>

 </
</InventoryAction>
<InventoryAction MessageType="Request" Type="Reservation" Action="PartialCancel">
 <
 <

RequestID>1234567</RequestID>
Cancellation>

ReasonCode>Don't need these</ReasonCode>

 <
 < Quantity>4</Quantity>

Cancellation>
DateTime>2001-12-17T09:30:47</DateTime>
ReservationID>2323</ReservationID>

 </
 <
 <
</InventoryAction>

</Inventory>

1-03-05 IXRetail Conformance XML Instance Doc – Response - Partial Completion
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="PartialComplete" AcceptedFlag="true">
 <

Response ResponseCode="OK">

 <

RequestID>1234567</RequestID>

Response>
DateTime>2001-12-17T09:30:47</DateTime>
ReservationID>2323</ReservationID>

 </
 <
 <
</InventoryAction>
<InventoryAction MessageType="Response" Type="Reservation" Action="PartialCancel" AcceptedFlag="true">
 <

Response ResponseCode="OK">

 <

RequestID>1234567</RequestID>

 </
 <

Response>
DateTime>2001-12-17T09:30:47</DateTime>
Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 38

IXRetail Inventory Technical Specification V1.0

<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

1-03-05 IXRetail Conformance XML Instance Doc – Response Failure - Partial Completion
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="PartialComplete" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234567</RequestID>
<BusinessError Severity="Error">

<Description>Already Complete</Description>

</BusinessError>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

3.6  Scenario: Partial Cancellation

Brief Description

Customer orders 3 different things and only two of them are delivered and remaining item reservation is cancelled.

Data

Inventory Reservation Partial Completion & Partial Cancellation data including:

•  ReservationID

•  Partial Completion disposition code

•  Completion LineItem containing

o  ItemID & Quantity

o  DispositionCode (CustomerPickup or ShippingDispatch)

•  Cancellation LineItems containing

o  ItemID & Quantity

o  Cancellation ReasonCode

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 39

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 15: Partial Cancellation Domain Model

1-03-06 IXRetail Conformance XML Instance Doc – Request - Partial Cancellation
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">
<InventoryAction MessageType="Request" Type="Reservation" Action="PartialCancel">

<RequestID>1234</RequestID>
<Cancellation>

<ReasonCode>StockDamaged</ReasonCode>
<ItemID>6766230544746</ItemID>
<Quantity>4</Quantity>

</Cancellation>
<DateTime>2001-12-17T09:30:47</DateTime>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 40

IXRetail Inventory Technical Specification V1.0

<ReservationID>2323</ReservationID>

</InventoryAction>
<InventoryAction MessageType="Request" Type="Reservation" Action="PartialComplete">

<RequestID>1234</RequestID>
<DateTime>2001-12-17T09:30:47</DateTime>
<FromLocation>

<ItemID>6766230544746</ItemID>
<InventoryLocation>

<BusinessUnit TypeCode="RetailStore">MailOrder</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

</InventoryLocation>
<Quantity>8</Quantity>

</FromLocation>
<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

1-03-06 IXRetail Conformance XML Instance Doc – Response - Partial Cancellation
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="PartialCancel" AcceptedFlag="true">

<Response ResponseCode="OK">
<RequestID>1234</RequestID>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>2323</ReservationID>

</InventoryAction>
<InventoryAction MessageType="Response" Type="Reservation" Action="PartialComplete" AcceptedFlag="true">

<Response ResponseCode="OK">
<RequestID>1234</RequestID>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

1-03-06 IXRetail Conformance XML Instance Doc – Response Failure - Partial Cancellation
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="PartialCancel" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234</RequestID>
<BusinessError Severity="Error">

<Description>AlreadyComplete</Description>

</BusinessError>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 41

IXRetail Inventory Technical Specification V1.0

<ReservationID>2323</ReservationID>

</InventoryAction>
<InventoryAction MessageType="Response" Type="Reservation" Action="PartialComplete" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234</RequestID>
<BusinessError Severity="Error">

<Description>AlreadyComplete</Description>

</BusinessError>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

3.7  Scenario: Reservation Lookup

Brief Description

Customer wants to see if their goods are available.

 Data

Inventory Reservation Enquiry Data including:

•  ReservationID

•  Original reservation request LineItems containing

o  Location

o  ItemID & Quantity,

o  EffectiveDate & ExpirationDate

•  Cancellation & Completion actions containing

o  Reason & Disposition Codes

o  Date & Time

Pre Condition

1.Invoker knows the reservation ID

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 42

IXRetail Inventory Technical Specification V1.0

Post Condition

Business Error

1.  reservation ID unknown
2.  (unable to resolve other parameters)

Data Hierarchy Diagram

Request

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

RequestIDCommonData

-@RequestorName[0..1]
-@Timestamp[0..1]

ItemIDCommonData

-@Qualifier[1]
-@Type[1]

QuantityCommonData

-@Units[1]
-@UnitOfMeasureCode[1]
-@EntryMethod[1]

CancellationType (cType)

-DateTime[0..1]
-ReasonCode[1]
-+ItemID[0..1]
-+Quantity[0..1]

BusinessUnitCommonData

-@Name[0..1]
-@TypeCode[1]

InventoryLocationType (cType)

-@Location[1]
-+BusinessUnit[0..1]
-SellingLocation[0..*]

ItemLocationType (cType)

-@State[0..1]
-+InventoryLocation[1]
-+ItemID[0..1]
-+Quantity[0..1]
-ExpirationDateTime[0..1]
-EffectiveDateTime[0..1]
-DateTime[0..1]

0..*

ExactLocation

-@Level[1]

Response

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

BusinessErrorCommonData

-@Severity[1]
-ErrorID[0..1]
-Code[0..1]
-Description[0..1]
-RelatedError[0..*]

ResponseCommonData

-@ResponseCode[1]
-RequestID[1]
-ResponseTimestamp[0..1]
-ResponseDescription[0..1]
-+BusinessError[0..*]

Item Type (cType)

-Whole Item Type Schema[1]

Figure 16: Reservation Lookup Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 43

IXRetail Inventory Technical Specification V1.0

1-03-07 IXRetail Conformance XML Instance Doc – Request - Reservation Lookup
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Reservation" Action="Lookup">
 <
 <
 <
</InventoryAction>

RequestID>2345</RequestID>
DateTime>2001-12-17T09:30:47</DateTime>
ReservationID>2323</ReservationID>

</Inventory>

1-03-07 IXRetail Conformance XML Instance Doc – Response - Reservation Lookup
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Lookup" AcceptedFlag="true">
 <

Response ResponseCode="OK">
RequestID>2345</RequestID>

 <

 </

Response>

<!-- 4 were cancelled due to damage on 14-Aug-->

 <

Cancellation>

DateTime TypeCode="Cancel">2001-08-13T13:44:02</DateTime>
ReasonCode>StockDamaged</ReasonCode>
ItemID>6766230544746</ItemID>

 <
 <
 <
 < Quantity>8</Quantity>

 </

Cancellation>

<!--8 were completed on 14-Aug -->

 <

Completion>

 <
 <

ItemID>6766230544746</ItemID>
InventoryLocation>

<BusinessUnit>MailOrder</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

InventoryLocation>

 </
 < Quantity>8</Quantity>
 <

DateTime TypeCode="Message">2001-08-13T13:44:02</DateTime>

 </
 <

Completion>
DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>

<!-- Original reservation for 12 copies, to be held for 1 week from 13-Aug -->

 <

ItemLocation>

 <
 <

ItemID>6766230544746</ItemID>
InventoryLocation>

<BusinessUnit>MailOrder</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

 </
InventoryLocation>
 < Quantity>12</Quantity>
 <
 <

DateTime TypeCode="Effective">2001-08-13T16:00:00</DateTime>
DateTime TypeCode="Expiration">2001-08-20T20:00:00</DateTime>

ItemLocation>
ReservationID>String</ReservationID>

 </
 <
</InventoryAction>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 44

IXRetail Inventory Technical Specification V1.0

</Inventory>

1-03-07 IXRetail Conformance XML Instance Doc – Response Failure - Reservation Lookup
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Lookup" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>2345</RequestID>
<BusinessError Severity="Error">

<Code>No Such Error</Code>

</BusinessError>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>
<ReservationID>2323</ReservationID>

</InventoryAction>

</Inventory>

4.  USE CASE: INVENTORY UPDATE

4.1  Scenario: Fulfillment of a product which is already sold

Brief Description

Customer  purchases  a  54”  LCD  TV  at  the  Point  of  Sale.  Customer  takes  their  receipt  and  drives  their  car  to  the  loading  dock.
Customer receives their TV from the loading dock and the loading dock management system must update the inventory system

Data

Inventory Update data including:

•  Disposition (CustomerPickUp, ShippingDispatch)

•  Optional Transaction number for RetailTransaction being fulfilled.

•  LineItems containing

o  ItemID & Quantity

Pre Condition

1. Product has been sold, inventory has not been updated

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 45

IXRetail Inventory Technical Specification V1.0

Post Condition

1. Inventory has been updated

Business Error

1.  reservation ID unknown
2.  unable to satisfy request
3.  (unable to resolve other parameters)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 46

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 17: Fulfillment ships a non-reserved Item from Inventory Domain Model

1-04-01 IXRetail Conformance XML Instance Doc – Request - Fulfillment ships a non-reserved Item from Inventory
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Update" InventoryState="AvailableToSell">

<RequestID>124356</RequestID>
<DateTime>2001-12-17T09:30:47</DateTime>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 47

IXRetail Inventory Technical Specification V1.0

<Disposition>Customer Pickup</Disposition>
<InventoryLocation>

<BusinessUnit>MailOrder</BusinessUnit>
<ExactLocation Level="Bay">TechnicalBooks</ExactLocation>

</InventoryLocation>
<ItemID>6766230544746</ItemID>
<Quantity>12</Quantity>
<TransactionNumber>

<BusinessUnit>eStore</BusinessUnit>
<WorkstationID>Server2</WorkstationID>
<SequenceNumber>4294967295</SequenceNumber>

</TransactionNumber>

</InventoryAction>

</Inventory>

1-04-01 IXRetail Conformance XML Instance Doc – Response - Fulfillment ships a non-reserved Item from Inventory
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Update" AcceptedFlag="true">

<Response ResponseCode="OK">

<RequestID>124356</RequestID>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

1-04-01 IXRetail Conformance XML Instance Doc – Response Failure - Fulfillment ships a non-reserved Item from Inventory
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Update" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>124356</RequestID>

</Response>
<DateTime>2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

5.  USE CASE: STOCK COUNT

Brief Description

Inventory system requests physical count of an item at a particular location.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 48

IXRetail Inventory Technical Specification V1.0

5.1  Scenario: Merchandiser Performs Cycle Count Request

Brief Description

Merchandiser wants to validate inventory position of a manufacturer’s product line to determine potential Return to Vendor candidates
or special one time order opportunity. For example, a manufacturer is offering a department store a one time special by on men’s polo
shirts, the merchandise buyer wants to have accurate understanding of the physical inventory position in the stores.

Pre Condition

1. Item ID/merchandise hierarchy ID

Post Condition

1. Physical Count was completed/was not (depending on response)

Business Error

1.  Cannot resolve the merchandise hierarchy ID
2.  Cannot resolve Item ID

Interaction Diagram

Data

o  Physical Count Request data, including:
o  Cycle Count ID
o  Description
o  Requested Start Date (Optional: represents the date at which the count can begin)
o  Requested Due Date (Optional: represents the date at which the count must be completed by)
o  Scope (any combination of Merchandise Classification, ItemID, UPC, Location)
o  Expected Data containing
o  ItemID / UPC
o  Quantit

y

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 49

IXRetail Inventory Technical Specification V1.0

o  Physical Count Response data, including:
o  Acknowledge

Data Hierarchy Diagram

Figure 18: Merchandiser Performs Cycle Count Request Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 50

IXRetail Inventory Technical Specification V1.0

1-05-01 IXRetail Conformance XML Instance Doc – Request - Merchandiser Performs Cycle Count Request
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="StockCount" Action="Initiate">
 <
 <
 <
 <
 <
 <

RequestID>9876</RequestID>
CycleCountID>7878</CycleCountID>
DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
DateTime TypeCode="ExpectedStart">2001-08-13T12:00:00</DateTime>
DateTime TypeCode="ExpectedDue">2001-08-13T18:30:00</DateTime>
ExpectedData>

 <

InventoryItem>

<ItemID>676623054746</ItemID>
<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">TechnicalBooks</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">2</Quantity>

 </
 <

InventoryItem>
InventoryItem>

<ItemID>676623054701</ItemID>
<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">TechnicalBooks</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">16</Quantity>

 </

InventoryItem>

 </
 <

ExpectedData>
Scope>

 <

InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">TechnicalBooks</ExactLocation>

InventoryLocation>

 </
 < MerchandiseHierarchy Level="Class">C++ For Dummies</MerchandiseHierarchy>

 </
Scope>
</InventoryAction>

</Inventory>

1-05-01 IXRetail Conformance XML Instance Doc – Response - Merchandiser Performs Cycle Count Request
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="StockCount" Action="Initiate" AcceptedFlag="true">
 <

Response ResponseCode="OK">
RequestID>9876</RequestID>

 <

Response>
CycleCountID>7878</CycleCountID>
DateTime>2001-12-17T09:30:47</DateTime>

 </
 <
 <
</InventoryAction>

</Inventory>
Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 51

IXRetail Inventory Technical Specification V1.0

1-05-01 IXRetail Conformance XML Instance Doc – Response Failure - Merchandiser Performs Cycle Count Request
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="StockCount" Action="Initiate" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>9876</RequestID>
<BusinessError Severity="Error">
<Code>ScopeInvalid</Code>

</BusinessError>

</Response>
<CycleCountID>7878</CycleCountID>
<DateTime>2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

5.2  Scenario: Stock Count Begin

Brief Description

Requestor sends a message to the Inventory system indicating that a stock count has begun for certain items in certain locations.

(potential NEAR candidate)

Data

o  Begin Physical Count Request data, including:
o  Operator / Employee ID (Optional)
o  Cycle Count ID
o  Actual Start Date & Time
o  Scope (any combination of Merchandise Classification, ItemID, UPC, Location)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 52

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

MerchandiseHierarchyCommonData

-@Level[1]
-@ID[1]

BusinessUnitCommonData

-@Name[0..1]
-@TypeCode[1]

ScopeType (cType)

-+Location[1]
-+MerchandiseHierarchy[1]

InventoryLocationType (cType)

-@Location[1]
-+BusinessUnit[0..1]
-SellingLocation[0..*]

1

0..*

ExactLocation

-@Level[1]

Figure 19: Stock Count Begin Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 53

IXRetail Inventory Technical Specification V1.0

1-05-02 IXRetail Conformance XML Instance Doc – Request - Stock Count Begin
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="StockCount" Action="Begin">

<RequestID>4567</RequestID>
<CycleCountID>7878</CycleCountID>
<DateTime>2001-12-17T09:30:47</DateTime>
<DateTime TypeCode="ActualStart">2001-12-17T09:30:47</DateTime>
<Operator>56743</Operator>
<Scope>

<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">Technical Books</ExactLocation>

</InventoryLocation>
<MerchandiseHierarchy Level="Class">C++ For Dummies</MerchandiseHierarchy>

</Scope>
</InventoryAction>

</Inventory>

5.3  Scenario: Stock Count Complete

Brief Description

Requestor sends sets of physical count records to Inventory system.

Data

o  Physical Count data, including:
o  Operator / Employee ID
o  Cycle Count ID
o  Actual Start Date & Time
o  Scope (any combination of Merchandise Classification, ItemID, UPC, Location)
o  Detail Data containing
o  Date & Time of actual line item count (optional)
o  Item ID / UPC
o  Quantity
o  Physical Count Response data, including:
o  Acknowledge

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 54

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 20: Stock Count Complete Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 55

IXRetail Inventory Technical Specification V1.0

1-05-03 IXRetail Conformance XML Instance Doc – Request - Stock Count Complete
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="StockCount" Action="Complete">
 <
 <
 <
 <

RequestID>2345</RequestID>
CycleCountID>7878</CycleCountID>
DateTime>2001-12-17T09:30:47</DateTime>
InventoryItem>

 <
 <

ItemID>676623054746</ItemID>
ItemLocation>

<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">Technical Books</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">2</Quantity>
<DateTime TypeCode="Effective">2001-12-17T09:30:47</DateTime>

 </
 <

ItemLocation>
ItemLocation>

<InventoryLocation>

<BusinessUnit>Store 72</BusinessUnit>
<ExactLocation Level="Department">Technical Books</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">10</Quantity>
<DateTime TypeCode="Effective">2001-12-17T09:30:47</DateTime>

 </

ItemLocation>

 </
 <

InventoryItem>
InventoryItem>

 <
 <

ItemID>676623054701</ItemID>
ItemLocation>

<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">Technical Books</ExactLocation>

</InventoryLocation>
<Quantity Units="1" UnitOfMeasureCode="EA">16</Quantity>
<DateTime TypeCode="Effective">2001-12-17T09:30:47</DateTime>

 </

ItemLocation>

InventoryItem>

 </
 < Operator>13763</Operator>
</InventoryAction>

</Inventory>

1-05-03 IXRetail Conformance XML Instance Doc – Response - Stock Count Complete
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="StockCount" Action="Complete" AcceptedFlag="true">
 <

Response ResponseCode="OK">
RequestID>2345</RequestID>

 <

 </

Response>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 56

IXRetail Inventory Technical Specification V1.0

<CycleCountID>7878</CycleCountID>
<DateTime>2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

1-05-03 IXRetail Conformance XML Instance Doc – Response Failure - Stock Count Complete
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="StockCount" Action="Complete" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>2345</RequestID>
<BusinessError Severity="Error">

<Code>Past Due Date</Code>

</BusinessError>

</Response>
<CycleCountID>7878</CycleCountID>
<DateTime>2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

6.  USE CASE: INVENTORY POSITION STATEMENT

This use case describes the ability for one system to communicate inventory position to another system. The scenarios in this use case
demonstrate both an unsolicited statement and a more targeted, solicited statement.

6.1  Scenario: Master Inventory system publishes an inventory position statement

Brief Description

A store based inventory system is used for perpetual inventory. The store system publishes an inventory position statement on a
periodic basis.

Pre Condition

1.  Publisher holds the master inventory position for the store

Post Condition

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 57

IXRetail Inventory Technical Specification V1.0

Business Error

Data

o  Inventory Position
o  Business Unit (common data)
o  Item ID (common data)
o  Inventory Location
o  Inventory state (optional)
o  Quantity
o  (notes to reflect final schema structure)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 58

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

BusinessUnitCommonData

-@Name[0..1]
-@TypeCode[1]

InventoryPositionType (cType)

-+BusinessUnit[1..*]
-+Item[1..*]

ItemLocationType (cType)

-@State[0..1]
-+InventoryLocation[1]
-+ItemID[0..1]
-+Quantity[0..1]
-ExpirationDateTime[0..1]
-EffectiveDateTime[0..1]
-DateTime[0..1]

Figure 21: Master inventory system issues synchronization to store inventory system

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 59

IXRetail Inventory Technical Specification V1.0

1-06-01 IXRetail Conformance XML Instance Doc – Publish - Master Inventory system publishes an inventory position
statement to a store based inventory system
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Event" Type="Inventory" Action="Information">
 <
 <
 <

RequestID>12343465</RequestID>
DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
InventoryPosition>

 <
 <

BusinessUnit TypeCode="RetailStore">1234</BusinessUnit>
Item State="AvailableToSell">

<ItemID Type="SKU">1234</ItemID>
<Quantity>100</Quantity>

 </

Item>

InventoryPosition>

 </
</InventoryAction>

</Inventory>

6.2  Scenario: Host system requests an inventory position statement from a store based
inventory system

Brief Description

A store based inventory system is used for perpetual inventory. A host system requests an inventory position statement on a periodic
basis.

Pre Condition

Post Condition

Business Error

Unable to resolve query parameters

Data

Inventory Position Statement Request data
o  Business Unit (common data)

(cid:131)
Inventory Location (optional)
national XML Retail Cooperative.  All rights rese
Copyright © 2005 Inter
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

rved.

Page 60

IXRetail Inventory Technical Specification V1.0

Item ID (optional, common data)

o  One of
o
o
o
o  Inventory state (optional, default to ALL)

  Merchandise hierarchy (optional, common data)
  Default to ALL

Inventory Position statement data
o  Inventory Position
o  Business Unit (common data)
o  Item ID (common data)
o  Inventory Location
o  Inventory state (optional)
o  Quantity
o  (notes to reflect final schema structure)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 61

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 22: Store inventory management system requests an inventory position statement from a master inventory system

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 62

IXRetail Inventory Technical Specification V1.0

1-06-02 IXRetail Conformance XML Instance Doc – Request - Invoker Requests an Inventory Position Statement
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Update" InventoryState="All">

<RequestID>12343465</RequestID>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<ItemID Type="SKU">345</ItemID>

</InventoryAction>

</Inventory>

1-06-02 IXRetail Conformance XML Instance Doc – Response - Invoker Requests an Inventory Positon Statement
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Update" InventoryState="All">

<Response ResponseCode="OK">

<RequestID>12343465</RequestID>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<InventoryPosition>

<BusinessUnit TypeCode="RetailStore">1234</BusinessUnit>
<Item State="AvailableToSell">

<ItemID Type="SKU">1234</ItemID>
<InventoryLocation>

<ExactLocation>Shelf23</ExactLocation>

</InventoryLocation>
<Quantity>100</Quantity>

</Item>

</InventoryPosition>

</InventoryAction>

</Inventory>

1-06-02 IXRetail Conformance XML Instance Doc – Response Failure - Invoker Requests an Inventory Position Statement
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Update" InventoryState="All">

<Response ResponseCode="Rejected">
<RequestID>12343465</RequestID>
<BusinessError Severity="Information">

<Code>Unable to resolve query parameters</Code>

</BusinessError>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 63

IXRetail Inventory Technical Specification V1.0

7.  USE CASE: INVENTORY ADJUSTMENT

This use case describes the ability for one system to communicate an adjustment in inventory position to another system.

7.1  Scenario: Adjustment of quantity based on a shrink event

Brief Description

A store based inventory system is used for perpetual inventory. A shrink event occurs (breakage, shoplifting etc) and the inventory
position in the store based system is adjusted to reflect the shrink event. The store based system publishes a message recording the
adjustment to a host system.

Pre Condition

Post Condition

Business Error

Data

o  Business Unit (common data)
o  Item ID (common data)
o  Inventory Location
o  Inventory state (optional)
o  Adjustment Quantity (plus or minus, amount)
o  Reason (optional)
o  Date/time (optional)
o  Operator ID (optional)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 64

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 23: system issues inventory adjustment to store inventory system

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 65

IXRetail Inventory Technical Specification V1.0

1-07-01 IXRetail Conformance XML Instance Doc – Publish - Master Inventory system publishes an inventory adjustment to
a store based inventory system
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Request" Type="Inventory" Action="Update">

<RequestID>12343465</RequestID>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>
<InventoryAdjustment Action="Set">

<InventoryPosition>

<BusinessUnit TypeCode="RetailStore">100</BusinessUnit>
<Item>

<ItemID Type="SKU">1234</ItemID>
<InventoryLocation>

<ExactLocation>Shelf23</ExactLocation>

</InventoryLocation>

</Item>

</InventoryPosition>
<AdjustmentQuantity>10</AdjustmentQuantity>

</InventoryAdjustment>

</InventoryAction>

</Inventory>

8.  USE CASE: TRANSFERS

An entity (store, warehouse, dept, etc. within the organization) with appropriate authority requests another entity (store, warehouse,
dept, etc. within the organization) to transfer certain items and quantities known to be in their inventory to theirs. The shipping entity
picks and dispatches the goods, and creates a transfer transaction to record this. The receiving store receives the goods, unpacks them
and puts them in appropriate stock locations, and updates the transfer transaction. Inventory system receives a copy of the transaction
at each stage and updates its records accordingly.

Note: there are requests/retry but this work product covers only physical movement.

8.1  Scenario: Invoker Performs Inventory Transfer Out

Brief Description

Invoker initiates transfer of inventoried items from one entity to another within the organization and records the action in an inventory
system. The inventory system issues a notification of the initiation of the transfer.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 66

IXRetail Inventory Technical Specification V1.0

Precondition(s)

Post Condition

Business Error

Data

o  Inventory Transfer Out notification data, including:
o  Header

o  Transfer ID
o  Transfer Type
o  From entity (providing item) (business unit, location)
o  To entity (receiving item) (business unit, location)
o  Attention (optional)
o  Reason Code (optional)
o  Description (optional)
o  Date/Time Detail
o  Carrier (optional)
o  Operator ID (optional)

o  Item ID (common data)

o  Quantity (common data, complex element)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 67

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Figure 24: Invoker Performs Inventory Transfer Out Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 68

IXRetail Inventory Technical Specification V1.0

1-08-01 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Transfer Out
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Event" Type="StockTransfer" Action="Instruction">
 <
 <
 <

RequestID>1234</RequestID>
DateTime>2001-12-17T09:30:47</DateTime>
InventoryItem>

 <
 <

ItemID>8734008754</ItemID>
FromLocation>

<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

FromLocation>
 </
 <
PlannedDate>1967-08-13</PlannedDate>
 < Quantity UnitOfMeasureCode="EA">1</Quantity>
 <
 <

ReasonCode>Customer Order</ReasonCode>
ToLocation>

<InventoryLocation>

<BusinessUnit Name="String" TypeCode="RetailStore">Back Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

 </

ToLocation>

 </
 <

InventoryItem>
InventoryItem>

 <
 <

ItemID>8734008754</ItemID>
FromLocation>

<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

FromLocation>
 </
 <
PlannedDate>1967-08-13</PlannedDate>
 < Quantity UnitOfMeasureCode="EA">1</Quantity>
 <
 <

ReasonCode>RTV</ReasonCode>
ToLocation>

<InventoryLocation>

<BusinessUnit Name="String" TypeCode="RetailStore">Back Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

 </

ToLocation>

InventoryItem>

 </
 < Operator>awse54</Operator>
 <

TransactionNumber>

BusinessUnit>High Street</BusinessUnit>

 <
 < WorkstationID>WS02</WorkstationID>
 <

SequenceNumber>4294967295</SequenceNumber>

TransactionNumber>

 </
</InventoryAction>

</Inventory>
Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 69

IXRetail Inventory Technical Specification V1.0

8.2  Scenario: Invoker Performs Inventory Transfer In

Brief Description

Actor executes Transfer receipt of inventoried items from another entity to another within the organization and records the action in an
inventory system. The inventory system issues a notification of the initiation of the transfer.

Precondition(s)

Post Condition

Data

o  Inventory Transfer out notification data, including:
o  Header

o  Transfer ID
o  Transfer Type
o  From entity (providing item) (business unit, location)
o  To entity (receiving item) (business unit, location)
o  Attention (optional)
o  Reason Code (optional)
o  Description (optional)
o  Date/Time Detail
o  Carrier (optional)
o  Operator ID (optional)

o  Item ID (common data)

o  Quantity (common data, complex element)
o  Package ID (optional)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 70

IXRetail Inventory Technical Specification V1.0

Data Hierarchy Diagram

Inventory

-@MajorVersion[1]
-@MinorVersion[0..1]
-@FixVersion[0..1]
-+InventoryAction[1..*]

Inventory Type (cType)

-@MessageType[1]
-@Type[1]
-@Action[1]
-@InventoryState[0..1]
-@AcceptedFlag[0..1]
-+RequestID[0..1]
-+Response[0..1]
-+Cancellation[0..1]
-+Completion[0..1]
-+CycleCount[0..*]
-CycleCountID[0..1]
-+DateTime[1..*]
-DeliveryMethod[0..1]
-Disposition[0..1]
-+ExpectedData[0..1]
-+FromLocation[0..*]
-+Fulfillment[0..*]
-+InventoryAdjustment[0..*]
-+InventoryItem[0..*]
-+InventoryLocation[0..*]
-+InventoryPosition[0..*]
-+Item[0..*]
-+ItemID[0..*]
-+ItemLocation[0..*]
-+Operator[0..*]
-+Quantity[0..1]
-+QuantityDispatched[0..1]
-ReservationID[0..1]
-+Reservation[0..*]
-+Scope[0..1]
-+ToLocation[0..1]
-TrackingNumber[0..1]
-+TransactionNumber[0..1]

QuantityCommonData

-@Units[1]
-@UnitOfMeasureCode[1]
-@EntryMethod[1]

BusinessUnitCommonData

-@Name[0..1]
-@TypeCode[1]

InventoryItemType (cType)

-@State[1]
-+ItemID[0..1]
-+ItemLocation[0..*]
-+InventoryLocation[0..*]
-+FromLocation[0..1]
-PlannedDate[0..1]
-+Quantity[0..1]
-ReasonCode[0..1]
-+ToLocation[0..1]

InventoryLocationType (cType)

-@Location[1]
-+BusinessUnit[0..1]
-SellingLocation[0..*]

0..*

ExactLocation

-@Level[1]

Figure 25: Invoker Performs Inventory Transfer In Domain Model

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 71

IXRetail Inventory Technical Specification V1.0

1-08-02 IXRetail Conformance XML Instance Doc – Request - Invoker Performs Inventory Transfer In
<?xml version="1.0" encoding="UTF-8"?>
<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Event" Type="StockTransfer" Action="Request">

<RequestID>1234</RequestID>
<DateTime>2001-12-17T09:30:47</DateTime>
<InventoryItem>

<ItemID>8734008754</ItemID>
<FromLocation>

<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

</FromLocation>
<PlannedDate>1967-08-13</PlannedDate>
<Quantity UnitOfMeasureCode="EA">1</Quantity>
<ReasonCode>Customer Order</ReasonCode>
<ToLocation>

<InventoryLocation>

<BusinessUnit>Back Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

</ToLocation>

</InventoryItem>
<InventoryItem>

<ItemID>8734008754</ItemID>
<FromLocation>

<InventoryLocation>

<BusinessUnit>High Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

</FromLocation>
<PlannedDate>1967-08-13</PlannedDate>
<Quantity UnitOfMeasureCode="EA">1</Quantity>
<ReasonCode>RTV</ReasonCode>
<ToLocation>

<InventoryLocation>

<BusinessUnit>Back Street</BusinessUnit>
<ExactLocation Level="Department">Books</ExactLocation>

</InventoryLocation>

</ToLocation>

</InventoryItem>

</InventoryAction>

</Inventory>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 72

IXRetail Inventory Technical Specification V1.0

9.  Schema Implementation

Inventory.xsd – core item data

Common Data.xsd – data common to more than one schema

CountryCode.xsd – Country Code enumeration

CurrencyCode.xsd – Currency Code enumeration

LanguageCode.xsd – Language Code enumeration

ServiceLevelCode.xsd – Service Level enumeration

UnitOfMeasureCode.xsd – Unit Of Measure enumeration

ItemLibrary.xsd – Detailed item information

10.  Document History

Sections  Description of Change
All

Initial Release

-

Version History

Ver  Date
1

9-13-2005

11.  GLOSSARY

1.  Site is a geographical entity – Business Unit is organizational entity

a.  BU can be at multiple sites
b.  Site can have multiple BU

Term

Definition

Adjustment  Tells you what to do

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 73

IXRetail Inventory Technical Specification V1.0

POS

An acronym for Point of Sale or Point of Service

POS-Log   An abbreviation for the Transaction Log, an application that stores transactions received from other applications for

future reference, and makes them available to other applications in the system.

Synchroniz
ation

Tells you what the value is. You have to decide what you’re going to do with the information

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 74

The following Use Cases/Scenarios do not provide unique insights into the Inventory Schema but are useful in understanding its
relationships to other IXRetail schemas.

The sequences are meant to be illustrative only and do not represent any implementation requirements.

Appendix A:

1.  USE CASE: SALES

1.1  Scenario: Item purchase by Customer at Store

(Cf: IXRetail POS-Log V2.1 Vol. 1, Section 4-1)

Brief Description

Customer  selects  an  item  from  the  store  and  proceeds  to  check  out  for  payment  process.    The  Item  Inventory  is  updated  from  the
record of the sale.  There is no need to perform any direct Inventory operations because the customer has selected the goods from the
shelves.
Customer selects one or more items and purchases them. The number of those items available in inventory is decremented.

Data

Transaction header data, including:

o  Identifiers for Store, Workstation, & Operator performing the transaction.
o  The date & time the transaction was performed
o  A workstation assigned sequence number identifying the transaction

Item sale data, including:

o  An identifier for the item being sold.
o  The number of multiples of the item being sold.
o  Unit price for the item being sold.
o  The extended amount (i.e. Unit price * the number of items being sold)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 75

IXRetail Inventory Technical Specification V1.0

1.2  Scenario: Item purchase via Mail Order, Fax or Telephone from Printed Catalog

Brief Description

Customer selects one or more items for purchase from a mail-order catalogue or printed advertisement and sends a completed order
form  to  the  retailer  via  Fax  or  Mail.    The  items  purchased  are  shipped  to  the  customer,  and  the  inventory  count  for  the  items  is
decremented.

Note: With a mail order transaction, both the check on availability and the stock reservation may be omitted, with the consequence
that Fulfillment is more likely to fail. Since no promise has been made to the customer, this is an inconvenience for the retailer rather
than a failure to do the business.

Note: If a reservation is made, there needs to be a mechanism for re-accessing it later. This may be achieved by having Inventory (or
some associated system) store the transaction number, or by having Inventory allocate a reservation tracking number, which is then
attached to the transaction.

Note: POS-Log may forward the transaction to Inventory and Fulfillment simultaneously at step 9, or the transaction may be daisy
chained  via  Fulfillment  to  Inventory.  The  former  arrangement  means  that  the  success  of  Fulfillment  is  assumed,  and  makes  better
sense if stock availability has been checked and/or stock reserved.

Inventory Interactions:

•

•

Inventory Lookup (Cf: 2.1: Scenario: Invoker Performs Inventory Lookup through an Operator on page 17)

Inventory Reservation (Cf: 3.1: Scenario: Invoker Requests an Inventory Reservation Through an Operator on page 23)

•  Transaction: (Cf: IXRetail POS-Log Vol. 1, Section 4-2)

•

Inventory Completion (Cf: 0: <?xml version="1.0" encoding="UTF-8"?>

<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Create" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234</RequestID>
<ResponseDescription>Invalid Request</ResponseDescription>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 76

IXRetail Inventory Technical Specification V1.0

•  Scenario: Reservation Completion on page 29)

1.3  Scenario: Item purchase via WWW or Telephone

Brief Description

Customer  selects  one  or  more  items  to  add  to  a  virtual  shopping  cart  –  selection  is  either  (WWW)  from  an  on-line  catalogue  or
(Telephone) from a selection offered orally.  Customer proceeds to payment. Either the sale is processed successfully, or Customer is
notified of non-availability of stock. Customer is able to cancel the reservation.  After payment, goods are delivered to the required
location.   Note that the reservations may be cancelled for any of the following reasons:

•  Customer logs out – goes offline or hangs up

•  The payment is not accepted, e.g. because the credit card is invalid

•  One or more reservations are not accepted (because of inventory being unavailable) so the customer wants to cancel the others

Main Flow Description

1.  Customer selects item(s) from Sales (the web site, or in conversation with the telephone sales person)
2.  Sales checks with Inventory for item availability.
3.  Inventory returns item availability.
4.  Sales displays pricing and availability
5.  Customer typically confirms choice. If the item is not available, or Customer feels like it, Customer may restart by selecting

another item or abandon the transaction

6.  Sales optionally requests Inventory to reserve the item(s)
7.  Inventory confirms the reservation, possibly with a reservation tracking number
8.  Sales creates the transaction and posts it to POS-Log.
9.  POS-Log forwards the transaction to Fulfillment.
10. Fulfillment processes the order and notifies Inventory of the Inventory Reservation Completion.

Note: The stock reservation may be made for each item ordered, or may be postponed until the order is ready to check out. The latter
arrangement  possibly  makes  the  reservation  process  simpler,  but  increases  the  chance  that  another  customer  may  take  the  last
available stock of an item between selection and order completion.

Note: The main difference, in system terms, between ordering by mail order and ordering on the web or by telephone is that an order
on  the  web  carries  an  implied  promise  of  successful  Fulfillment.  It  is,  therefore,  essential  to  check  stock  availability,  and  highly

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 77

IXRetail Inventory Technical Specification V1.0

desirable  to  make  a  real-time  reservation  to  prevent  other  orders  taking  the  goods  in  the  period  between  order  taking  and  order
picking.

Note: Inventory does not maintain any data about the Customer, Delivery Address or any other Fulfillment related data that may be
acquired during this use-case.

Sequence Diagram

C u s to m e r

S a le s

T L o g

In ve n to ry

F u lfilm e n t

S e le ct ite m s

D isp la y s p ricin g  &  a v a ila b ility

C o n firm  ch o ic e

Q u e ry  a v a ila b ility

R e tu rn  a v a ila b ility

M a y m a ke  re a l-tim e  re se rv a tio n

C o n firm  re se rv a tio n  w ith  o p tio n a l tra ckin g  n u m b e r

C o m p le te  p a y m e n t a n d  d e live ry  a rra n g e m e n ts

C re a te  a n d  p o st tra n sa c tio n

1 :F o rw a rd  tra n s a ctio n

1 F o rw a rd  tra n s a ctio n

2 :F o rw a rd  tra n sa ctio n

2 :C o m p le te  &  p o st tra n sa ctio n

2  F o rw a rd  tra n s a c tio n

D e cre m e n ts in v e n to ry

Figure 26: Item purchase via WWW or Telephone Interaction Diagram Example

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 78

IXRetail Inventory Technical Specification V1.0

Inventory Interactions:

•

•

Inventory Lookup (Cf: 2.1: Scenario: Invoker Performs Inventory Lookup through an Operator on page 17)

Inventory Reservation (Cf: 3.1: Scenario: Invoker Requests an Inventory Reservation Through an Operator on page 23)

•  Transaction: (Cf: IXRetail POS-Log Vol. 1, Section 4-2)

•

Inventory Completion (Cf: 0: <?xml version="1.0" encoding="UTF-8"?>

<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Create" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234</RequestID>
<ResponseDescription>Invalid Request</ResponseDescription>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

•  Scenario: Reservation Completion on page 29)

1.4  Scenario: Catalogue SHOP

Brief Description

Customer selects one or more items to from a catalogue or by reference to display-only items on shelves. Customer proceeds to the
sales counter.  The sale is either processed successfully, or Customer is notified of non-availability of stock.   After payment, goods
are picked up from a designated location in the store. If Customer is subsequently dissatisfied with the product, they may return it

Main Flow Description

1.  Customer selects item from on-shelf sample or a printed catalogue
2.  Customer may check item availability at a stock checker terminal
3.  Customer completes an order-form, and presents it to the Cashier together with payment
4.  Cashier validates the order, enters it into Sales, processes the payment and gives Customer a receipt
5.  Sales creates a transaction and posts it to POS-Log
6.  POS-Log forwards the transaction to Fulfillment & Inventory.
7.  Fulfillment picks the item from the back storeroom
8.  Customer presents receipt to Fulfillment and receives item.
9.  Fulfillment completes the transaction.
10. Inventory Decrements available stock from completed transactions.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 79

IXRetail Inventory Technical Specification V1.0

Note:  In this scenario, the stock is not reserved when the order is entered. There is thus a small but real possibility that Fulfillment
may fail. There needs to be further processes, not shown here, to reverse the Inventory decrement if this happens. However, Inventory
update is typically a daily batch process in such an organization, which means, only those

Sequence Diagram

Customer

Stock check terminal

Cashier

Sales

T-Log

Inventory

Fulfilment

Select item

May check availability

Return availability

Present completed order-form with payment

Present receipt

Check availability

Return availability

Process order and payment

Print receipt

Create & post transaction

Forward transaction

Decrement inventory

Forward transaction

Present receipt

Deliver goods

Post completed transaction

Figure 27: Catalogue SHOP Interaction Diagram Example

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Pick item

Page 80

IXRetail Inventory Technical Specification V1.0

Inventory Interactions:

•  Transaction: (Cf: IXRetail POS-Log Vol. 1, Section 4-2)

1.5  Scenario: Store Sale of Normally Stocked Item Not In Stock

Brief Description

Customers ask for goods.  Sales system queries Inventory to discover that the goods are not available.  Customer makes a reservation,
possibly with a payment.  Customer is informed when the goods arrive and collects the goods, paying for them then if not already
done.

Main Flow Description

1.  Customer asks for item(s) that are not available.
2.  Sales queries Inventory for availability
3.  Inventory returns a message indicating lack of availability
4.  Customer requests Sales to raise a backorder, and possibly pays a deposit or in full for the goods
5.  Sales creates a transaction and posts it to POS-Log
6.  POS-Log forwards the transaction to Order Tracking
7.  Order tracking files the order
8.  POS-Log forwards the transaction to Inventory
9.  Inventory increments stock backordered
10. (At some later time) Supplier delivers goods
11. Inventory increases stock on hand
12. Inventory notifies Order Tracking that the previously backordered goods have arrived
13. Order Tracking locates the back orders affected and notifies Sales
14. Sales notifies Customer (typically by telephone, post card or eMail)
15. Customer re-initiates the purchase, which then proceeds in the normal fashion.

Note:    In  a  bricks  and  mortar  store,  there  may  be  no  stock  availability  check  with  Inventory,  since  immediate  availability  can  be
checked on the shelves. However, many stores will make such a check, and thus discover stock that is simply misplaced.

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 81

IXRetail Inventory Technical Specification V1.0

Sequence Diagram

Customer

Sales

TLog

Inventory

Order tracking

Supplier

Select items

Query availability

Return non-availability

Notify not available

Request to order, possibly with payment

Create and post transaction

Forward transaction

Forward transaction

File order

Increment stock backordered

Deliver goods

Increment stock

Notify stock arrival

Notify that order can be delivered

Identify backorders affected

Notify available

Proceed with purchase

Figure 28: Store Sale of Normally Stocked Item Not In Stock Interaction Diagram Example

Inventory Interactions:

•

•

Inventory Lookup (Cf: 2.1: Scenario: Invoker Performs Inventory Lookup through an Operator on page 17)

Inventory Reservation (Cf: 3.1: Scenario: Invoker Requests an Inventory Reservation Through an Operator on page 23)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 82

IXRetail Inventory Technical Specification V1.0

•  Transaction (Cf: IXRetail POS-Log Vol. 1, Section 4-2)

•

Inventory Completion (Cf: 0: <?xml version="1.0" encoding="UTF-8"?>

<Inventory xmlns="http://www.nrf-arts.org/IXRetail/namespace/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.nrf-
arts.org/IXRetail/namespace/ Inventory.xsd" MajorVersion="1" MinorVersion="0" FixVersion="0">

<InventoryAction MessageType="Response" Type="Reservation" Action="Create" AcceptedFlag="false">

<Response ResponseCode="Rejected">
<RequestID>1234</RequestID>
<ResponseDescription>Invalid Request</ResponseDescription>

</Response>
<DateTime TypeCode="Message">2001-12-17T09:30:47</DateTime>

</InventoryAction>

</Inventory>

•  Scenario: Reservation Completion on page 29)

2.  USE CASE: RETURNS

Brief Description

Customer returns item(s) or the store collects them from him.  Sales make a decision whether to accept the goods, and, if so decided,
pay Customer. There is then a, usually, separate process to decide what to do with the goods. Inventory is updated appropriately.

Pre-Conditions

Actors

Actor

Customer

Sales

Fulfillment

POS-Log

Inventory

Return decision
process

Description

The person that makes the return

The application that initially processes the return and makes any payment

The application that is used to arrange delivery of items purchased.

The application that forwards transactions to the appropriate applications

The application that maintains stock balances

The application or process that decides how to dispose of the returned goods

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 83

IXRetail Inventory Technical Specification V1.0

Main Flow Description

1.  Customer returns the goods to Sales, or the retailer collects the goods from the customer and delvers them to Sales
2.  Sales decides to accept the goods
3.  Sales makes a refund to Customer
4.  Sales creates a transaction and posts it to POS-Log
5.  POS-Log forwards the transaction to Return Decision Process
6.  Return Decision Process decides how to dispose of the goods, eg return to new stock, write off or return to stock as marked-

down items.

7.  Return Decision Process posts the updated transaction to POS-Log
8.  POS-Log forwards the transaction to Inventory
9.  Inventory increments the stock of the appropriate item

Note: Return Decision Process may be an integral part of either Sales or Inventory.
Sequence Diagram

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 84

IXRetail Inventory Technical Specification V1.0

Customer

Sales

TLog

Inventory

Return decision process

Returned goods

Refund

Decide to accept

Create and post transaction

Forward transaction

Updated transaction

Decide what to do with goods

Forward transaction

Increment appropriate stock

Figure 29: Returns Interaction Diagram Example

Inventory Interactions:

o  Transaction: (Cf: IXRetail POS-Log Vol. 1, Section 12-1)

Copyright © 2005 International XML Retail Cooperative.  All rights reserved.
Verbatim reproduction and distribution of this document is permitted in any medium, provided this notice is preserved.

Page 85

