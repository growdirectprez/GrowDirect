---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/arts/location/CR_ARTS_Location_Technical_Specification_V2.0.0_20170301_final.pdf.md
tags: [canary, arts, retail-data-model, standards-reference, tier1-extract]
project: canary
status: unprocessed
---

# CR_ARTS_Location_Technical_Specification_V2.0.0_20170301_final.pdf

## Source
File: `Brain/raw/.extract/tier1-md/arts/location/CR_ARTS_Location_Technical_Specification_V2.0.0_20170301_final.pdf.md`
Size: 196,823 bytes

## Raw content
ARTS Location Technical Specification 2.0
February 10, 2017

Board Sponsor:
Bart McGlothin

Chair:
Graeme Shaw

Members:
Matthew Kulig
Tai NGoma
Kent Ruesink
Mike Boughton
Andy Mattice
Shannon Byers
Michele Kosow
Dennis Blankenship
John Glaubitz
Tom Sterling
Richard Halter

Cisco

Kogi Services

Aisle411
Canadian Tire
JDA
JDA
Lexmark
Nielsen
Sophelle
Verizon
Vertex Inc
ARTS
ARTS

ARTS Location 2.0 Technical Specification

TABLE OF CONTENTS

1

Abstract .................................................................................................................................. 5

1.1
1.2
1.3
1.4
1.5

OVERVIEW ........................................................................................................................ 5
IN SCOPE V1.0 ................................................................................................................. 5
OUT OF SCOPE V1.0 ......................................................................................................... 5
IN SCOPE FOR VERSION 2.0.0 ........................................................................................... 6
OUT OF SCOPE FOR VERSION 2.0.0 ................................................................................... 7

2

3

4

5

6

7

8

Referenced Documents ........................................................................................................ 8

ARTS Common Header ......................................................................................................... 9

Retail Model Interfaces/Architectural Model .................................................................... 10

ARTS Data Model................................................................................................................. 11

Location Detection .............................................................................................................. 14

Location – Privacy ............................................................................................................... 16

Store Configuration ............................................................................................................. 17

8.1
8.2
8.3
8.4
8.5

USE CASE: SEND STORE DETAILS – V1.0.0 ..................................................................... 17
USE CASE: A STORE IS CLOSED FOR REMODELING – V1.0.0 .............................................. 20
USE CASE: INITIALIZE A NEW STORE WITHIN A CHAIN – V1.0.0 ........................................... 23
USE CASE: UPDATING OPENING HOURS FOR A STORE – V1.0.0 ......................................... 27
USE CASE: A STORE IS OPENING A NEW DEPARTMENT FOR BAKED GOODS. – V1.0.0 .......... 29

9

Near Store ............................................................................................................................ 31

USE CASE: USER IS DRIVING IN A  CAR OR USING A MOBILE PHONE/TABLET TO FIND A RETAILER NEAR

USE CASE: USER IS DRIVING IN A CAR OR USING A MOBILE PHONE/TABLET TO FIND PRODUCT FROM A

9.1
THEM – V1.0.0 ............................................................................................................................. 31
9.2
SPECIFIC RETAILER NEAR THEM. – V1.0.0 ...................................................................................... 36
USE CASE: CHECK IF A NEARBY RETAILER CARRIES ITEMS FROM A SHOPPING LIST – V1.0.0 39
9.3
9.4
USE CASE: USER PHONE VIBRATES WHEN THEY ARE NEAR AN ITEM ON THEIR SHOPPING LISTS OR WISH
LISTS – V1.0.0 ............................................................................................................................. 41
USE CASE: USER WALKS PAST A STORE AND RECEIVES A COUPON OR OFFER – V1.0.0....... 45
9.5
47
9.6
USE CASE: USER GREETED DIGITALLY AT THE DOOR BY RETAILER ON MOBILE DEVICE – V1.0.0
9.7
USE  CASE:  USER  WANTS  TO  CHECK  STORE  TO  SEE  IF  PRODUCT  IS  IN  STOCK  BEFORE  GOING  INTO  A
STORE – V1.0.0 ........................................................................................................................... 49
9.8

USE CASE: USER USES AUGMENTED REALITY TO FIND SPECIALS OR PRODUCTS NEAR THEM – V1.0.0
52

10  Customer Facing ................................................................................................................. 57

10.1  USE CASE: CUSTOMER IS LOOKING FOR CATEGORY OF ITEMS (CHEESE) – V1.0.0 .............. 57
10.2  USE CASE: CUSTOMER WANTS TO ORDER ON-LINE AND PICKUP IN CLOSEST STORE – V1.0.059
10.3  USE CASE: CUSTOMER RECEIVES TARGETED COMMUNICATION BASED ON THEIR IN-STORE LOCATION
– V1.0.0 ...................................................................................................................................... 66
10.4  USE CASE: CUSTOMER IS LOOKING FOR PHYSICALLY RELATED OBJECTS – V1.0.0 .............. 69

11  Operations ............................................................................................................................ 72

11.1  USE CASE: STORE SETUP – V1.0.0 ................................................................................. 72
11.2  USE CASE: GET STOCK FROM WAREHOUSE – V1.0.0 ....................................................... 76
11.3  USE CASE: RECEIVING ITEMS - WHERE TO PUT PALLETS IN STORE  – V1.0.0 ...................... 80
11.4  USE CASE: SEND FLOOR PLAN – V1.0.0 .......................................................................... 85
11.5  USE CASE: FIND AREA OF INTEREST – V1.0.0 .................................................................. 88

12  Associate Facing ................................................................................................................. 93

Copyright  2017 NRF.  All rights reserved.

Page 2

ARTS Location 2.0 Technical Specification

12.1  USE CASE: LOCATE A SPECIFIC STORE WITHIN A GEOGRAPHIC AREA – V1.0.0 .................... 93
12.2  USE CASE ITEM LOCATIONS – V1.0.0 .............................................................................. 96
12.3  USE CASE: STORE PICKING – V1.0.0 ............................................................................. 100
12.4  USE CASE: LOCATE RETAIL OPERATIONS EQUIPMENT IN STORE  – V1.0.0 ........................ 104

13  Use Case: Find Non Retail Items – V2.0.0 ....................................................................... 107

13.1

SCENARIO: PRINTER HAS RUN OUT OF PAPER – V2.0.0.................................................. 107

14  GLOSSARY ........................................................................................................................ 109

Table of Figures
Figure 1: ARTS Common Header Domain View.............................................................................. 9
Figure 2: ARTS Common Header Representation .......................................................................... 9
Figure 3: Location Relationships .................................................................................................... 11
Figure 4: Item - Planogram - Store - Site Relationships ................................................................ 11
Figure 5 Data Model Location Block Diagram ............................................................................... 12
Figure 6: Retailer Business Unit Site Contact ................................................................................ 13
Figure 7: Initialize a New Store within a Chain BPM ..................................................................... 17
Figure 8: Updating Opening Hours for a Store BPM ..................................................................... 27
Figure 9: Open New Department ................................................................................................... 29
Figure 10: Find Nearest Store BPM ............................................................................................... 31
Figure 11: Find Closest Store with Item BPM ................................................................................ 36
Figure 12: Check if Retailer Carries Items on Shopping List ......................................................... 39
Figure 13: Wish List Notification .................................................................................................... 42
Figure 14: Greet Customer with Coupon BPM .............................................................................. 45
Figure 15: Check Stock Position BPM ........................................................................................... 50
Figure 16: Augmented Reality BPM ............................................................................................... 53
Figure 17: Item Category Search BPM .......................................................................................... 57
Figure 18: Order online - Pickup in Store BPM .............................................................................. 60
Figure 19: Locate Nearest Specific Retailer with this Item BPM ................................................... 63
Figure 20: Special Offer Based on In-Store Location BPM ........................................................... 66
Figure 21: Find Nearest Restroom BPM ........................................................................................ 69
Figure 22: Get a Map of the Store BPM ......................................................................................... 72
Figure 23: Get Stock from Warehouse BPM .................................................................................. 76
Figure 24: Receiving Pallet BPM ................................................................................................... 80
Figure 25: Send Floor Plan BPM ................................................................................................... 85
Figure 26: Find "Area of Interest" BPM .......................................................................................... 88
Figure 27: Locate Multipe Items BPM ............................................................................................ 96
Figure 28: Store Picking BPM ...................................................................................................... 100
Figure 29: Locate Retail Operations Equipment in Store BPM .................................................... 104

Table of ARTS XML Samples
8.1.1 ARTS XML Instance Document: Send Store Detail Request ............................................................ 18
8.1.1 ARTS XML Instance Document: Send Store Detail Response ......................................................... 19
8.2.1 ARTS XML Instance Document: Store Closed for Remodeling ........................................................ 21
8.2.2 ARTS XML Instance Document: Remodel of Store Request ............................................................ 21
8.2.2 ARTS XML Instance Document: Remodel of Store Response ......................................................... 21
8.3.1 ARTS XML Instance Document: Setup New Store at Head Office ................................................... 24
8.4.1 ARTS XML Instance Document:  Update Open Hours ...................................................................... 27
8.5.1 ARTS XML Instance Document: Opening New Department ............................................................. 30
9.1.1 ARTS XML Instance Document: Find Nearest Store Request .......................................................... 32
9.1.1 ARTS XML Instance Document: Find Nearest Store Response ....................................................... 33
9.1.2 ARTS XML Instance Document: Find closest Store while Driving Request ...................................... 34
9.1.2 ARTS XML Instance Document: Find closest Store while Driving Response ................................... 35

Copyright  2017 NRF.  All rights reserved.

Page 3

ARTS Location 2.0 Technical Specification

9.2.1 ARTS XML Instance Document: Find Closest Store with Item Request ........................................... 37
9.2.1 ARTS XML Instance Document: Find Closest Store with Item Response ........................................ 38
9.3.1 ARTS XML Instance Document: Which items are carried by nearby retailer request ....................... 40
9.3.1 ARTS XML Instance Document: Which items are carried by nearby retailer response .................... 41
9.4.1 ARTS XML Instance Document - Item Location Near Store Notification Request ............................ 43
9.4.1 ARTS XML Instance Document - Item Location Near Store Notification Response ......................... 43
9.5.1 ARTS XML Instance Document - Receive Coupon in Vicinity of Store Request............................... 46
9.5.1 ARTS XML Instance Document - Receive Coupon in Vicinity of Store Response ............................ 47
9.6.1 ARTS XML Instance Document - Receive Greeting on Phone Request ........................................... 48
9.6.1 ARTS XML Instance Document - Receive Greeting on Phone Response ........................................ 49
9.7.1 ARTS XML Instance Document: Check Stock Position Request ...................................................... 51
9.7.1 ARTS XML Instance Document: Check Stock Position Response ................................................... 52
9.8.1 ARTS XML Instance Document: Using Augmented Reality for Location Request ............................ 54
9.8.1 ARTS XML Instance Document: Using Augmented Reality for Location Response ......................... 55
10.1.1 ARTS XML Instance Document - Item Category Search Request .................................................. 58
10.1.1 ARTS XML Instance Document - Item Category Search Response ............................................... 58
10.2.1 ARTS XML Instance Document - Order Online – Pickup in Store Request .................................... 61
10.2.1 ARTS XML Instance Document - Order Online – Pickup in Store Response ................................. 62
10.2.2 ARTS XML Instance Document - Locate Specific Brand Request .................................................. 64
10.2.2 ARTS XML Instance Document - Locate Specific Brand Response ............................................... 64
10.3.1 ARTS XML Instance Document - Special Offer Based on In-Store Location Request ................... 67
10.3.1 ARTS XML Instance Document - Special Offer Based on In-Store Location Response ................. 68
10.4.1 ARTS XML Instance Document - Find the restroom Request ......................................................... 70
10.4.1 ARTS XML Instance Document - Find the restroom Response ...................................................... 70
11.1.1 ARTS XML Instance Document - Get a Map of the Store Request ................................................. 74
11.1.1 ARTS XML Instance Document - Get a Map of the Store Response .............................................. 74
11.2.1ARTS XML Instance Document - Get Stock from Warehouse Request ........................................... 77
11.2.1ARTS XML Instance Document - Get Stock from Warehouse Response ........................................ 78
11.3.1 ARTS XML Instance Document - Where to put pallets in store ....................................................... 83
11.4.1 ARTS XML Instance Document: Send Floor Plan Request ............................................................ 87
11.4.1 ARTS XML Instance Document: Send Floor Plan Response .......................................................... 87
11.5.1 ARTS XML Instance Document: Find Area of Interest Request ...................................................... 89
11.5.1 ARTS XML Instance Document: Find Area of Interest Response ................................................... 89
11.5.2 ARTS XML Instance Document: Locate Concession Area Request ............................................... 91
11.5.2 ARTS XML Instance Document: Locate Concession Area Response ............................................ 91
12.1.1 ARTS XML Instance Document: Locate a specific store: geographic area Request ...................... 94
12.1.1 ARTS XML Instance Document: Locate a specific store: geographic area Response ................... 94
12.2.1 ARTS XML Instance Document: Locate Multiple Items Request .................................................... 98
12.2.1 ARTS XML Instance Document: Locate Multiple Items Response ................................................. 98
12.3.1 ARTS XML Instance Document: Store Picking Request ............................................................... 102
12.3.1 ARTS XML Instance Document: Store Picking Response ............................................................ 103
12.4.1 ARTS XML Instance Document: Find Shelf Label Printer Request ............................................... 105
12.4.1 ARTS XML Instance Document: Find Shelf Label Printer Response ............................................ 106
13.1ARTS XML Instance Document: Printer has Run Out of Paper Request .......................................... 107
13.1ARTS XML Instance Document: Printer has Run Out of Paper Response ....................................... 107

Copyright  2017 NRF.  All rights reserved.

Page 4

ARTS Location 2.0 Technical Specification

1  Abstract

1.1  Overview

The Location Technical Standard provides a definition of where things are located, to enable
mapping algorithms to guide a customer or associate to proper areas of the store.

Increasing widespread use of mobile devices by both employees and consumers makes
location information extremely important to retailers. The ARTS Location technical standard
intent is to provide a common interface to access location information that can be used by
higher-level applications such as Store Locator, Product Locator, Shelf Restocking, Geo-Fenced
Marketing, etc.

Standardized common interfaces to access information between retail mobile applications and
systems reduce TCO of innovative solutions.

The purpose of location starts by describing the geographic location of the store and what is
available at the store.  Once the customer finds the store, they can be directed to the
department or category within the store which may include directing the customer to the
aisle/bay/shelf/side of the aisle where the selected item is stored.

Customer location inside or outside a store may be a privacy issue even if the customer has
opted-in.  These issues may vary by country, state or city.  The issues around privacy are
outside the scope of this work and should be managed by the individual retailer.

1.2  In Scope V1.0

For Version 1.0, the primary scope is to enable consumers to interact with the retailer’s location
based apps and influence higher basket, increase sales, consumer retention. That is items
which are displayed, where they are located and how presented on a shelf.  Identify Store
Location, Customer presence near the store or within the store.

•  Location in terms of store, floor, dept./category, aisle, fixture bay, orientation, shelve,

XYZ floor coordinates which would enable a 2d overview of what the store interior looks
like.

•  Detailed item information (most specifically unit size)
•  Fixed dimension products only
•  Unit inventory
•
•  Basic linear display and pegs
•  Effective date of planogram and store layout changes

Item placement within a set of fixtures

1.3  Out of Scope V1.0

•  Turn by turn directions (way finding) from point A to point B
•  Path of travel from point A to point B
•  Point in time stationary location of entities – movement (path) of customers, products

and associates

•  Define a store layout (macro store space) (store video)

o  Apparel, random weight products
o  Contractual information.
o  Detailed shelf construction information

Copyright  2017 NRF.  All rights reserved.

Page 5

ARTS Location 2.0 Technical Specification

o  Requires MFG coupon standards for personalized promotions

•  Physical location of lights, security cameras, restrooms, escalators etc.
•  Way finding path obstructions
•  Detailed Planogram information

1.4  In Scope for Version 2.0.0

Feature
Planogram
Detail

Description

•  Detailed fixture/shelf/equipment construction and location
•  Product item details (assortment, with core and optional,

add/keep/drop, brand, dimensions etc.)

•  Product positions
•
•  User defined attributes (for product items, planograms, equipment,

Inventory model & replenishment methods/periods

product positions, planogram segment)

•  Labels/Signage/Promotional
•  Localization (units, languages, tax codes)
•  Financial Plan/ Reconciliation (to act as an input target to help the

Visual Merchandiser design the planogram)
•  Descriptions (source, author etc., version, dates)
•  Drawing elements (red-lining, notes, text, revision clouds)
•
•  Technology to support Planograms (such as RFID & smart fixtures)

Include Fashion and Random weight categories

Way Finding

•  Provide directions for a path between two points, or several points if

given a shopping list of items to pick.

•  The standard wouldn’t define how to calculate the shortest path, but

would define how the path would be described.

•  Localization of path description (Path description could be
floor/aisle/bay, or turn left at a landmark, i.e. using different
terminology based on recipient)
Inclusion of obstructions, elevators, escalators, stairs

•
•  Require assistance: Item is on top shelf, too heavy, wheelchair route,

aisle widths
•  Alternate paths
•  Sorting method for pick lists, e.g. heavy/frozen items last
•
•  Picking for multiple lists (compare with warehouse standard)
•  Take account of IoT standard with reference to movable objects, such

Include outside yards/backroom

as:
o  Person location
o  Customer
o  Employee
o  Fork lift
o  Shopping Cart
o  Floor waxer
o  Portable Equipment, e.g. product pallets

Copyright  2017 NRF.  All rights reserved.

Page 6

ARTS Location 2.0 Technical Specification

Both planogram and way finding require a map or floorplan context.  The floorplan or map
contextual data consists of:

•  A raster image of the store floor plan, as an output
•  A vector image, comprising of Cartesian coordinate values to define areas and objects,
including building architectural elements, such as elevators, stairs, common areas,
bathrooms, etc., as well as features that identify, name and describe areas of interest to
the business, such as fixturing and equipment.

•  Planogram and SKU performance data, for analytical purposes.

1.5  Out of Scope for Version 2.0.0

Feature

Description
Virtual worlds
Calculate shortest path
Warehouse Inventory Allocation

Copyright  2017 NRF.  All rights reserved.

Page 7

ARTS Location 2.0 Technical Specification

2  Referenced Documents

•  ARTS Technical Committees Development Process V6.0.4
•  ARTS Coordinate System Insertion Points Best Practices V1.0.0
•  ARTS XML Best Practices V2.2
•  ARTS Best Practice for Process Modeling V1.0.0
•  ARTS SOA Best Practices Technical Report V1.2
•  ARTS Best Practices for Services Implementation V1.0.0
•  ARTS XML Interface Conformance Tool Manual V1.0

These documents are available for download from https://nrf.com/standards

•  http://www.gs1.org/sites/default/files/docs/epc/TDS_1_8_Standard_20140203.pdf
•  https://nrf.com/resources/retail-library/shoporg-think-tank-what-the-internet-of-things-

promises-retailers

•  https://nrf.com/news/tour-of-the-possible

Copyright  2017 NRF.  All rights reserved.

Page 8

ARTS Location 2.0 Technical Specification

3  ARTS Common Header

Figure 1: ARTS Common Header Domain View

The ARTS common header is used in all service name schemas.  It provides the ability to set
session level information and return business error information in one standard format to all
SOA implementations.

Figure 2: ARTS Common Header Representation

Since this structure is common to all service name schemas, it will not be replicated below.  In
place of the details, the attached box will be used to represent this complex type structure.

Copyright  2017 NRF.  All rights reserved.

Page 9

-@ActionCode[0..1]-@MessageType[0..1]-MessageID[1]-DateTime[0..1]-+Response[0..1]-+Requestor[0..1]-+BusinessUnit[0..*]-+OrganizationalHierarchy[0..*]-WorkstationID[0..1]-TillID[0..1]ARTSHeaderCommonData-@Severity[0..1]-ErrorID[0..1]-Code[0..1]-Description[0..1]-RelatedErrorID[0..*]BusinessErrorCommonData-@Name[0..1]-@TypeCode[1]BusinessUnitCommonData-@Level[0..1]-@ID[0..1]OrganizationHierarchyCommonData-@ResponseCode[0..1]-RequestID[1]-ResponseTimestamp[0..1]-ResponseDescription[0..1]-+BusinessError[0..*]ResponseCommonDataARTS Common Header

ARTS Location 2.0 Technical Specification

4  Retail Model Interfaces/Architectural Model

Copyright  2017 NRF.  All rights reserved.

Page 10

LocationReplenishmentPrice Optimization(Digital)SignageFixturingProduct Lifecycle ManagementAsset ManagementAssortment PlanningVideo AnalyticsFloorplanPlanogramStore OperationsData Warehouse BIDirect Store DeliveryLoss PreventionMobileIn-Store FulfillmentWEB Orders

ARTS Location 2.0 Technical Specification

5  ARTS Data Model

Figure 3: Location Relationships

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
