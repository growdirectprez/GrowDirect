---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/arts/inventory/CR IXRetail Inventory Technical Specification V1.0 20050813.pdf.md
tags: [canary, arts, retail-data-model, standards-reference, tier1-extract]
project: canary
status: unprocessed
---

# CR IXRetail Inventory Technical Specification V1.0 20050813.pdf

## Source
File: `Brain/raw/.extract/tier1-md/arts/inventory/CR IXRetail Inventory Technical Specification V1.0 20050813.pdf.md`
Size: 141,822 bytes

## Raw content
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


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
