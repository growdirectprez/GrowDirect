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

Outside the store use either the physical address of the store or the geophysical address.  But
once one goes into the store use the X, Y, Z coordinates relative to the specific store.

Figure 4: Item - Planogram - Store - Site Relationships

Site – the physical location of the business unit

Store – the content with the business unit.

One locates the site where one wishes to shop and then locate the items one wishes to
purchases within the store.

Planogram – box with description of where to place items

Item Meta-Data – the detailed description of the items placed within the planogram.

Copyright  2017 NRF.  All rights reserved.

Page 11

Business Process Location RelationshipsStoreWorldOriginX, Y, Z CoordinatesPhysical AddressGeophysical AddressBusiness Process Item - Planogram - Store RelationshipsItem Meta-DataPuts the Item at a Location in a PlanogramPlanogramPuts a Planogram at a location within one or more storesOne or more stores are locatedat a site

ARTS Location 2.0 Technical Specification

Figure 5 Data Model Location Block Diagram

•  Geographical Area Hierarchy describes a hierarchy of geographical information to locate

•

a store.
ISO Standard Designations for Countries and Primary Political Subdivisions provides a
link between ISO 3166-2 country codes and geographic segments

•  Retailer Designated Geographic Segment identifies the geographic segment for a

retailer

•  Retailer Business Unit Site Contact Data identifies site contact information
•  Party Contact Data is an abstraction of how to contact an individual or company
•  Postal Code links the geographic segment information with the contact information
•  Geophysical Location ties the geophysical coordinate system with the geophysical

location of a business unit

•  The Geophysical location defines the location of the store.

Copyright  2017 NRF.  All rights reserved.

Page 12

Geographic Area (Segment) HierarchyISO Standard Designations for Countries and Primary Political SubdivisionsRetailer Designated Geographic SegmentRetail Business Unit Site Contact DataPostal CodeCustomer Geographic SegmentGeophysical Location (Latitude and Longitude)Association between Geophysical Location and Contact AddressParty Contact Data

ARTS Location 2.0 Technical Specification

Figure 6: Retailer Business Unit Site Contact

Location defines areas inside a Site.  It retains its recursive join to allow retailers to nest
locations within higher-level locations.  A Location may be classified as a floor, floor section,
fixture or other physical category using LocationType.  Note the concept of LocationType is
separate from FunctionCode.  FunctionCode designates the intended business use for a
location.  LocationType classifies the location based on its physical properties.

To enable navigation services that place merchandise at a Location within a Site a new join
entity has been, MerchandiseHierarchyGroupLocation.  MerchandiseHierarchyGroup provides
the relationships necessary to tie an individual item or named category of items to a location.
This affords retailers with the flexibility to choose the level of granularity they want to use to
implement merchandise location services.  For example, Google Maps typically identifies
departments, not individual item locations.  This solution gives retailers a wide range of options.

The LocationCoordinate entity establishes the insertion point of a Location within the Site or
within another higher-level Location.  The issues around local coordinate systems, mapping
them to building plans and site plans, scaling and other pertinent data designed to place points
is to be addressed in a future version.

LocationVertex identifies individual points for a location.  In this version, the vertex is primarily
the back-left origin for the entity being located.  For example, a store’s origin is the back-left
corner of the store (can be outside the 4 walls).  From there a display case can have its origin
relative to this store origin.  Then the coordinates where the origin of any shelves on the display
case is located with respect to the origin of the display case.  Finally, the coordinates of the
origin of any items on the shelf are located with respect to the display case.

The subtype of NonSellingPublicArea is a way to reflect locations that are publicly accessible
but not used for sales, inventory or work.  They include areas like stairwells, lobbies, restrooms,
foyers, etc.

This model is not designed to model any sort of shapes but simply the location of each entity
within the context of the containing entity.

Copyright  2017 NRF.  All rights reserved.

Page 13

ARTS Location 2.0 Technical Specification

6  Location Detection

Near Store:

If end user provides zip-code, cross-streets or other region-based non-geographic coordinate
system, that should go to a different service first to derive Lat/Long, then use Lat/Long in the call
to this service.

In-Store:

The tech spec needs a few paragraphs describing technology examples for how coordinates in
the store may be derived.  A quick review list of…

Methods and technology to derive “In-Store Coordinate Location”

•  Wi-Fi
•  Bluetooth
•  Ultrasonic
•  RFID
•  Video Analytics
•  Fixture / product location:  UPC scanning (sign / product correlation to inventory

planogram floorplan)

•  User input.  Select a department from a list.
•  Sensor technology in mobile devices (e.g. MEMS)
•  Visible Light Communication (LED lighting)
•  Computer Vision
•  Floor Sensors

Accuracy

With each method, there are different accuracy constraints.

UPC scanning might find multiple locations for the product.  In this case accuracy is 50% for
each of two fine-grained locations, and consumer may have carried the product elsewhere and
scanned later to compare with a different product in another aisle.

Current Wifi triangulation range has a wide error range depending on the environment and
technologies being used.

One form of RFID is implemented as a gate sensor.  In this case, it might provide only a store
department or aisle as a location… consumer (or tracked item) entered aisle 5.

Use of a combination of methods can achieve higher accuracy than reliance on one method
alone.

Range

Range-finding for closest stores.  We are leaving it up to the implementation to decide what is
meant by “closest”.  As-the-crow-flies?  Driving distance?  Walking distance?  The implementer
can pick how they wish to calculate “closest”.  We are not defining what it means to be “the
closest store”, just that there is a way to find closest and the implementation will return whatever
it decides is closest.

Search Radius could be implemented with a type to support finer granularity:  Search within 1
mile or 50km?  Search for fast walking distance, driving distance along known paths or as-the-
crow-flies?

Copyright  2017 NRF.  All rights reserved.

Page 14

ARTS Location 2.0 Technical Specification

Best Path Algorithm

ARTS defines the message to communicate the best path but the algorithm used to calculate
the best path is the vendor’s responsibility

Copyright  2017 NRF.  All rights reserved.

Page 15

ARTS Location 2.0 Technical Specification

7  Location – Privacy

Privacy is the domain of the application that delivers the data.  This would normally require an
opt in policy.

Copyright  2017 NRF.  All rights reserved.

Page 16

ARTS Location 2.0 Technical Specification

8  Store Configuration

BPMN Diagram:

Figure 7: Initialize a New Store within a Chain BPM

8.1  Use Case: Send Store Details – V1.0.0

8.1.1  Scenario: Send Store Detail – V1.0.0

There is a need to send details about one or multiple stores between systems.
Brief Description
The reasons for sending updated store details may include:

•  A new store is opening
•  An existing store is closing (either permanently or for refurbishment)
•  The opening hours have changed
•  Various store attributes or services have changed

Scenario Description
A new store is about to open and its details need to be sent to another system.

Data Request
Description
Date of Request
Retailer
Store Codes
Level of Detail

Optional  Sample

Comments

x

1 Jun 2013 09:15:47
ACME
0002, 0003
All

Header, opening
times, services,
attributes

Copyright  2017 NRF.  All rights reserved.

Page 17

Business Process Send Store DetailsStoreHead OfficeTransafer Store Master DataTransafer Store Master DataUpdate Store SystemUpdate Store SystemARTS DataModelARTS DataModelBusinessUnitConfiguration

ARTS Location 2.0 Technical Specification

Data Response
Description
Store Number
Store Name
Store Manager
Email Address
Phone Number
Store Address

Cluster

Comments

Sample
0002
St Albans
Mrs Anne Other
A.Other@Retail.com
+44 1727 776655
6 Retail Park,
 St Albans, UK

Country

Region

District

UK
South East
Hertfordshire

Geographic Position

Open Date
Close Date
Type

Prototype Store

Is a Prototype Store
Number of Floors

Store Size
Time Zone
List of Opening Times

List of Services

List of Attributes

1 March 2009

Standard

0001

No
1

5000
GMT
Mon-Fri 8:00 – 18:00
Sat 9:00 – 17:00
Sun 10:00 – 16:00
Bakery
ATM
Deli
Pharmacy
Floral

Region=South
Units=mm
Demographic=A
Parking Lot
Spaces=80

Latitude,
Longitude

Not closed
Bricks and Mortar
store
Warehouse?
Prototype store
Indicates which
template s this
store is based on
Yes or No
>1 if a multi-
storey building
Sqft, or m2

Attribute Name &
Value
Because these
are company
unique. This is an
xs:any extension
point.

8.1.1 ARTS XML Instance Document: Send Store Detail Request
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"

Copyright  2017 NRF.  All rights reserved.

Page 18

ARTS Location 2.0 Technical Specification

    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Request">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit TypeCode="RetailStore" Name="ACME">002</BusinessUnit>
    </ARTSHeader>
    <BusinessUnitConfiguration>
        <BusinessUnit>002</BusinessUnit>
        <BusinessUnit>003</BusinessUnit>
        <Request>All</Request>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

8.1.1 ARTS XML Instance Document: Send Store Detail Response
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Request">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit TypeCode="RetailStore" Name="ACME">002</BusinessUnit>
    </ARTSHeader>
    <BusinessUnitConfiguration TimeZone="GMT">
        <BusinessUnit Name="St Albans">002</BusinessUnit>
        <HoursOfOperation Day="Friday" When="Between">
            <Span>
                <StartTime>20:00:00.032+01:00</StartTime>
                <EndTime>20:00:00.032+01:00</EndTime>
            </Span>
        </HoursOfOperation>
        <ContactInformation>
            <Telephone>
                <LocalNumber>1727776655</LocalNumber>
                <ITUCountryCode>44</ITUCountryCode>
            </Telephone>
            <Address>
                <AddressLine>6 Retail Park</AddressLine>
                <City>St Albans</City>
                <Territory>UK</Territory>
            </Address>
            <EMail>A.Other@Retail.com</EMail>
        </ContactInformation>
        <StoreType>Virtual</StoreType>
        <StoreType>Prototype</StoreType>
        <OrganizationHierarchy Level="Country">UK</OrganizationHierarchy>
        <OrganizationHierarchy Level="Region">South East</OrganizationHierarchy>
        <OrganizationHierarchy Level="District">Hertfordshire</OrganizationHierarchy>

Copyright  2017 NRF.  All rights reserved.

Page 19

ARTS Location 2.0 Technical Specification

        <Manager>
            <Name>
                <Name>Mrs Anne Other</Name>
            </Name>
        </Manager>
        <OpenDate>1970-01-01</OpenDate>
        <CloseDate>1970-01-01</CloseDate>
        <FloorCount>1</FloorCount>
        <StoreSize UnitOfMeasure="FTK">5000</StoreSize>
        <StoreService>
            <TypeCode>Bakery</TypeCode>
        </StoreService>
        <StoreService>
            <TypeCode>ATM</TypeCode>
        </StoreService>
        <StoreService>
            <TypeCode>Deli</TypeCode>
        </StoreService>
        <Location>
            <Location>
                <Coordinates>
                    <Latitude>
                        <Degrees>101</Degrees>
                        <Minutes>40</Minutes>
                    </Latitude>
                    <Longitude>
                        <Degrees>10</Degrees>
                    </Longitude>
                </Coordinates>
            </Location>
        </Location>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

8.2  Use Case: A store is closed for remodeling – V1.0.0

8.2.1  Scenario:  Store Closed for Remodeling – V1.0.0

Because the store concept dictates that an upgrade is needed the must store stay closed for a
while.
Brief Description:
Head office has determined that the store needs to be upgraded. Because of this the store must
shut down for a short period. This information must include sent to WMI systems so ordering
takes this into account.
Pre-condition:
Scenario Description:
The central management determines that this store needs a large reconstruction.  This because
of new marketing appearances.   This means that the store is closed for a period.  It is important
to send this info to the WMI vendors so that they stop the automatic ordering system.
Data:
Sending a message on a queue.

Copyright  2017 NRF.  All rights reserved.

Page 20

ARTS Location 2.0 Technical Specification

8.2.1 ARTS XML Instance Document: Store Closed for Remodeling
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Update">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit TypeCode="RetailStore" Name="ACME">002</BusinessUnit>
    </ARTSHeader>
    <BusinessUnitConfiguration Status="ClosedForRemodeling">
        <BusinessUnit>002</BusinessUnit>
        <OpenDate>2004-01-01</OpenDate>
        <CloseDate>2004-01-01</CloseDate>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

8.2.2  Scenario: Remodel of Store – V1.0.0

BPMN Diagram
Brief Description
Take stock of the gondolas that are already there – delta calculation

Data
•  Current planogram
•  Planogram Changes

8.2.2 ARTS XML Instance Document: Remodel of Store Request
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Request">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit TypeCode="RetailStore" Name="ACME">002</BusinessUnit>
    </ARTSHeader>
    <BusinessUnitConfiguration>
        <!-- Send me the planograms for ths store -->
        <BusinessUnit>100</BusinessUnit>
        <Planogram TypeCode="Current"/>
        <Planogram TypeCode="New"/>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

8.2.2 ARTS XML Instance Document: Remodel of Store Response
<?xml version="1.0" encoding="UTF-8"?>
<Planogram xmlns="http://www.nrf-arts.org/IXRetail/namespace/"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

Copyright  2017 NRF.  All rights reserved.

Page 21

ARTS Location 2.0 Technical Specification

xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../PlanogramV1.0.0.xsd"
MajorVersion="1" MinorVersion="0" FixVersion="0">
<ARTSHeader ActionCode="Add" MessageType="Response">

<MessageID>ABCDEFG</MessageID>
<DateTime>2006-05-04T19:00:51.0</DateTime>
<Response ResponseCode="OK">

<RequestID>12432134</RequestID>
<ResponseTimestamp>2006-05-04T18:13:51.0</ResponseTimestamp>

</Response>
<BusinessUnit>My Store</BusinessUnit>

</ARTSHeader>
<!-- Current planogram -->
<Planogram Status="Applied">

<PlanogramID>ABCD123</PlanogramID>
<Revision>00</Revision>
<DateTime>2006-05-04T18:13:51.0</DateTime>
<Fixture>

<Fixture>

<FixtureID TypeCode="Bay">01</FixtureID>
<!-- Defines where this fixture fits in the hierarchy -->
<ParentID>0</ParentID>
<ChildID Name="Shelf">101</ChildID>
<!-- Location within the store for this fixture -->
<Location TypeCode="Bay">

<SequenceNumber>1</SequenceNumber>
<!-- the location of this fixture with respect to its parent in the store -->
<OriginLocation>

<X-Coordinate>-23</X-Coordinate>
<Y-Coordinate>-45</Y-Coordinate>
<Z-Coordinate>0</Z-Coordinate>

</OriginLocation>

</Location>

</Fixture>

</Fixture>
<Fixture>

<Fixture>

<FixtureID TypeCode="Shelf">101</FixtureID>
<ParentID>01</ParentID>
<ChildID>0</ChildID>
<Location TypeCode="Shelf">

<OriginLocation>

<SequenceNumber>1</SequenceNumber>

</OriginLocation>

</Location>

</Fixture>
<!-- Blue Shirts -->
<Item ActionCode="Add">

<ItemID Type="SKU">12341243124</ItemID>
<PositionSequence>1</PositionSequence>
<Quantity>10</Quantity>

</Item>

</Fixture>
<FixtureCount>1</FixtureCount>

</Planogram>
<!-- changed planogram -->
<Planogram Status="Approved">

Copyright  2017 NRF.  All rights reserved.

Page 22

ARTS Location 2.0 Technical Specification

<PlanogramID>ABCD123</PlanogramID>
<Revision>00</Revision>
<DateTime>2006-05-04T18:13:51.0</DateTime>
<Fixture>

<Fixture>

<FixtureID TypeCode="Bay">01</FixtureID>
<!-- Defines where this fixture fits in the hierarchy -->
<ParentID>0</ParentID>
<ChildID Name="Shelf">101</ChildID>
<!-- Location within the store for this fixture -->
<!-- move this fixture to this new location -->
<Location TypeCode="Bay">

<SequenceNumber>1</SequenceNumber>
<!-- the location of this fixture with respect to its parent in the store -->
<OriginLocation>

<X-Coordinate>-50</X-Coordinate>
<Y-Coordinate>-75</Y-Coordinate>
<Z-Coordinate>0</Z-Coordinate>

</OriginLocation>

</Location>

</Fixture>

</Fixture>
<Fixture>

<Fixture>

<FixtureID TypeCode="Shelf">101</FixtureID>
<ParentID>01</ParentID>
<ChildID>0</ChildID>
<Location TypeCode="Shelf">

<OriginLocation>

<SequenceNumber>1</SequenceNumber>

</OriginLocation>

</Location>

</Fixture>
<!-- Red Pants -->
<Item ActionCode="Add">

<ItemID Type="SKU">asdfasf</ItemID>
<PositionSequence>1</PositionSequence>
<Quantity>10</Quantity>

</Item>

</Fixture>
<FixtureCount>1</FixtureCount>

</Planogram>

</Planogram>

8.3  Use Case: Initialize a new store within a chain – V1.0.0

8.3.1  Scenario:  Setup New Store at Head Office – V1.0.0

A new is needs a transfer from the master data system at head office to the chain main system.
Brief Description:
A new store is about to start up.  The chain system needs a complete dump of all information
about this store.  This is sent from over to the chain system.
Pre-condition:

Copyright  2017 NRF.  All rights reserved.

Page 23

ARTS Location 2.0 Technical Specification

The computer system within the chain office does not have any info about the new store.
Scenario Description:
A new store is about to open on 15. May 2013.  To be able start operations, the store systems
need to be initiated from the head office.
Data:

•  <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
•  <Location Action="Update" ResponseCode="OK">
•  <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
•  <LocationID>7080001081676</LocationID>
•  <LocationAccount>
•  <TypeCode>DiscountTransferAccountNo</TypeCode>
•  <ChargeAccount>

o  <Number>0</Number>
o  <CheckDigit>0</CheckDigit>

•  <Affiliation>

o  <Relationship>UniqueLocationId</Relationship>
o  <PartyID>16599</PartyID>

•  <LocationStatus>
•  <StartDate>2004-10-01</StartDate>
•  <EndDate>2004-10-01</EndDate>
•  <OpeningHour>

o  <HoursTypeCode>Saturday</HoursTypeCode>
o  <DateTo>2999-12-31</DateTo>
o  <DateFrom>2006-11-27</DateFrom>
o  <TimeToOpen>09:00:00</TimeToOpen>
o  <TimeToClose>23:00:00</TimeToClose>
o  <Closed>false</Closed>
•  <Services> - services provided by store
o  <Code>Season</Code>

▪  <StartDate>2004-10-01</StartDate>
▪  <EndDate>2004-10-01</EndDate>

o  <Name>Fall</Name>
o  </Services>

•  <Admin> - floor space

o  <Code>Square Meters</Code>
o  <Name>A</Name>
o  <Txt>320</Txt>

•  <Demogratic> - store location

o  <Code>Geographic location</Code>
o  <Name>A</Name>
o  <Txt>City center</Txt>

•  <Technical UpdateType="Exiting"> - equipment

o  <Code>Cash machines ID</Code>
o  <Name>227105</Name>

8.3.1 ARTS XML Instance Document: Setup New Store at Head Office
<?xml version="1.0" encoding="UTF-8"?>
<Businessbu xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Update">
        <MessageID>9876</MessageID>

Copyright  2017 NRF.  All rights reserved.

Page 24

ARTS Location 2.0 Technical Specification

        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit TypeCode="RetailStore" Name="ACME">002</BusinessUnit>
    </ARTSHeader>
    <BusinessUnitConfiguration Status="OpenForBusiness">
        <BusinessUnit Name="Kiwi 309 Bjolsen" TypeCode="RetailStore">100</BusinessUnit>
        <HoursOfOperation Day="Saturday">
            <Span>
                <StartDate>2999-12-31</StartDate>
                <StartTime>09:00:00</StartTime>
                <EndTime>23:00:00</EndTime>
                <EndDate>2006-11-27</EndDate>
            </Span>
        </HoursOfOperation>
        <HoursOfOperation Day="Sunday">
            <Span>
                <StartDate>2999-12-31</StartDate>
                <StartTime>08:00:00</StartTime>
                <EndTime>08:00:00</EndTime>
                <EndDate>2006-11-27</EndDate>
            </Span>
        </HoursOfOperation>
        <DoesBusinessAs>NG Kiwi Oslo Akershus AS</DoesBusinessAs>
        <ContactInformation>
            <Telephone TypeCode="Work">
                <LocalNumber>22181531</LocalNumber>
            </Telephone>
            <Telephone TypeCode="WorkFax">
                <LocalNumber>22181532</LocalNumber>
            </Telephone>
            <Address AddressType="Work" AddressLocationType="Permanent">
                <AddressLine TypeCode="Street">Bergensgata 28 B</AddressLine>
                <City>OSLO</City>
                <Territory>Oslo</Territory>
                <PostalCode>0468</PostalCode>
            </Address>
            <Address AddressType="Delivery" AddressLocationType="Permanent">
                <AddressLine TypeCode="Street">Bergensgata 28 b</AddressLine>
                <AddressLine TypeCode="Street"/>
                <City>OSLO</City>
                <Territory>Oslo</Territory>
                <PostalCode>0468</PostalCode>
            </Address>
            <EMail TypeCode="Work">kiwi.bjolsen@ngbutikk.net</EMail>
        </ContactInformation>
        <Manager>
            <Name>
                <Name TypeCode="PreferredName">Richard Selmer</Name>
            </Name>
            <ContactInformation>
                <Telephone TypeCode="Mobile">
                    <LocalNumber>48042212</LocalNumber>
                </Telephone>
            </ContactInformation>
        </Manager>
        <OpenDate>2004-10-01</OpenDate>
        <CloseDate>2004-10-01</CloseDate>

Copyright  2017 NRF.  All rights reserved.

Page 25

ARTS Location 2.0 Technical Specification

        <FloorSize Floor="1" UnitOfMeasure="FTK">320</FloorSize>
        <StoreService>
            <Name>A</Name>
            <TypeCode>Fresh cheese</TypeCode>
            <StartDate>2004-10-01</StartDate>
        </StoreService>
        <StoreService>
            <Name>BIB Full</Name>
            <TypeCode>Bank in shop</TypeCode>
            <StartDate>2008-06-16</StartDate>
            <LicenseNo>161024</LicenseNo>
        </StoreService>
        <Affiliation Name="ASKO NORGE AS" Relationship="WholesalePartyNo" PartyID="1"/>
        <Affiliation Name="KIWI NORGE" Relationship="StoreChain" PartyID="1100"/>
        <ChargeAccounts CheckDigit="0"
Organization="DiscountTransferAccountNo">0</ChargeAccounts>
        <ChargeAccounts CheckDigit="0" Organization="BankGrioNr">82000211008</ChargeAccounts>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

Copyright  2017 NRF.  All rights reserved.

Page 26

ARTS Location 2.0 Technical Specification

8.4  Use Case: Updating opening hours for a store – V1.0.0

BPMN Diagram:

Figure 8: Updating Opening Hours for a Store BPM

8.4.1  Scenario:  Update Open Hours – V1.0.0

All the opening hours for a store are sent from the master data system and to the chain head
office system.
Scenario Description:
An opening hour for a store has changed.   This is transmitted to the chain head office system.
This system is feeding the local internet application with this data for display out to customers.
Pre-condition:
The main office system is ready and able to receive this info.   Logic is built around the principle
that all hours are sent every time.

Data:

8.4.1 ARTS XML Instance Document:  Update Open Hours
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Update" MessageType="Publish">
        <MessageID>1234</MessageID>

Copyright  2017 NRF.  All rights reserved.

Page 27

Business Process Update CorporateHead OfficeStoreUpdate Open HoursUpdate Open HoursARTS DataModelBusiness UnitConfigurationUpdate Store DetailsUpdate Store DetailsARTS DataModel

ARTS Location 2.0 Technical Specification

        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <BusinessUnitConfiguration Status="ChangeHours">
        <BusinessUnit Name="Kiwi 309 Bjølsen"/>
        <HoursOfOperation Day="Weekday" Status="Open">
            <Span>
                <StartDate>2999-12-31</StartDate>
                <StartTime>09:00:00</StartTime>
                <EndTime>23:00:00</EndTime>
                <EndDate>2006-11-27</EndDate>
            </Span>
        </HoursOfOperation>
        <HoursOfOperation Day="Sunday" Status="Closed">
            <Span>
                <StartDate>2999-12-31</StartDate>
                <StartTime>08:00:00</StartTime>
                <EndTime>19:00:00</EndTime>
                <EndDate>2006-11-27</EndDate>
            </Span>
        </HoursOfOperation>
        <DoesBusinessAs>NG Kiwi Oslo Akershus AS</DoesBusinessAs>
        <OpenDate>2004-10-01</OpenDate>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

Copyright  2017 NRF.  All rights reserved.

Page 28

ARTS Location 2.0 Technical Specification

8.5  Use Case: A store is opening a new department for baked goods.

– V1.0.0

BPMN Diagram:

Figure 9: Open New Department

8.5.1  Scenario:  Opening New Department – V1.0.0

The local top end supermarket is opening a new department for baked goods.  This info is sent
from the local store to the master data system.

Brief Description:
The local supermarket has just opened a reconstruction with a department where it bakes fresh
bread.  Information about this and when this new department opens is sent from the local back
office system in the store over to the central master data system.

Scenario Description:
Kiwi Bjolsen in Oslo, Norway has been through a large reconstruction.  The store has been
given a large new space.  Parts of this space have been used to install large bakery oven.  They
have hired a French baker.  This new department is producing about 100 bread of different
types every day.   The project manager of the reconstruction told the store manager that this
department can open on Friday 14. of June.   The store manager logs into his store
management system and tells the system that this new department is to be opened on the date
above. This information is transmitted to the central master data system.   The web pages for
this store chain are then updated.

Data:

Copyright  2017 NRF.  All rights reserved.

Page 29

Business Process Store SetupMaster Data SystemStoreOpen BakeryOpen BakeryBusiness UnitConfigurationUpdate Master DataUpdate Master DataARTS DataModel

ARTS Location 2.0 Technical Specification

8.5.1 ARTS XML Instance Document: Opening New Department
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Update" MessageType="Publish">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <BusinessUnitConfiguration>
        <BusinessUnit>123345</BusinessUnit>
        <StoreService Status="New">
            <TypeCode>Bakery</TypeCode>
            <StartDate>2999-12-31</StartDate>
        </StoreService>
        <StoreService Status="Existing">
            <Name>161024</Name>
            <TypeCode>PostInShop</TypeCode>
            <StartDate>2008-06-16</StartDate>
        </StoreService>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

Copyright  2017 NRF.  All rights reserved.

Page 30

ARTS Location 2.0 Technical Specification

9  Near Store

9.1  Use Case: User is driving in a car or using a mobile phone/tablet

to find a retailer near them – V1.0.0

9.1.1  Scenario: Find Nearest Store – V1.0.0

A retail customer with a retailer’s smartphone application would like to find the store closest to
them.  User would use the application to find the nearest store.

Figure 10: Find Nearest Store BPM

Brief Description
The purpose of this function is to leverage the user’s proximity to find the closest location to the
user.

Pre-conditions

•  The user’s mobile device is on and the user has the retailer’s application
•  The user is opted-in to Location Services for the application
•  The user’s mobile device currently has data connectivity
•  User’s phone Locate me (GPS) needs to be turned on to show users location
•  Or possible enter in a zip code for the location where store search is requested

Scenario Description
Jean wants to pick up double sided tape and wants to find the closest location for her favourite
retailer.  Using her location, the retailer app shows her the closest store to her.

Prerequisites
#

Description
1.   Retailer App open

Optional  Sample
N

XYZ Retailer App

Comments
GPS Location
needs to be turned
on

Copyright  2017 NRF.  All rights reserved.

Page 31

Business Process Find Nearest StoreLocation ServiceCustomerNear Store SearchNear Store SearchNear Store SearchNear Store SearchLocationARTS DataModelReport Nearest StoreReport Nearest StoreDisplay Nearest StoreDisplay Nearest StoreLocationCurrentLocation

ARTS Location 2.0 Technical Specification

2.   Search for Retailer

N

location

Where is closest
location.

Data Request

#

Description
1.   Current Customer

Optional  Sample
N

40° 45′ 0″ N

Latitude

2.   Current Customer

N

14° 29′ 10″ E

Longitude

Data Response

Using location app
shows closest
location

Comments
Jean’s Latitude
provided by GPS
Jean’s Longitude
provided by GPS

This is an example of results included in a list/map of the closest locations.

#

Description
1.   Store Number

Optional  Sample
Y

101

Comments

2.   Address

3.   Street Name

4.   Unit

5.   City

6.   State

7.   Zip code

Y

Y

Y

Y

Y

Y

4145

Forest Park

Chicago

Illinois

60125

Assumptions
Retrieval of map and wayfinding are assumed to be a separate call after store locations are
found.

9.1.1 ARTS XML Instance Document: Find Nearest Store Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Request" ActionCode="Inquiry">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit Name="Halter's Emporium">100</BusinessUnit>
    </ARTSHeader>
    <Location>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>

Copyright  2017 NRF.  All rights reserved.

Page 32

ARTS Location 2.0 Technical Specification

                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
            <SearchRange UOM="SMI">5</SearchRange>
        </SourceLocation>
    </Location>
</Location>

9.1.1 ARTS XML Instance Document: Find Nearest Store Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Response" ActionCode="Inquiry">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
        <BusinessUnit Name="Halter's Emporium">100</BusinessUnit>
    </ARTSHeader>
    <Location>
        <DestinationLocation>
            <Address>
                <AddressLine>4145 Forest Park</AddressLine>
                <City>Chicago</City>
                <Territory>Illinois</Territory>
                <PostalCode>60125</PostalCode>
            </Address>
            <BusinessUnit>101</BusinessUnit>
        </DestinationLocation>
    </Location>
</Location>

9.1.2  Scenario: Find closest Store while Driving – V1.0.0

A retail customer with a retailer’s smartphone application would like to find the store closest
while driving.  User would use the car IVR (Interactive Voice Response) system to access
application to find the nearest store.

Brief Description
The purpose of this function is to leverage the user’s proximity to find the closest location to the
user using the cars IVR system.

Pre-conditions

•  The user’s car has a IVR system and it is on and the user can access the retailer’s

application through the IVR system

•  The user is opted-in to Location Services for the application
•  The user’s mobile device currently has data connectivity

Copyright  2017 NRF.  All rights reserved.

Page 33

ARTS Location 2.0 Technical Specification

•  The Users car has a locate me (GPS) function that needs to be turned on to show users

location

Description
Car IVR system is on  N

Optional  Sample
DeSoto

Retailer App can be
accessed from IVR
system
Search for Retailer
location

N

N

XYZ Retailer App

Where is closest
location.

Comments
IVR should access
retailer database
for locations
GPS Location
needs to be turned
on
Using location app
shows closest
location

Scenario Description
Jean’s wants to pick up double sided tape and is driving a car with IVR built in and wants to find
the closest location for her favourite retailer.  Using the car’s IVR and her location the retailer
app tells her the closest store to her.

Data Request

Description
Current Customer
Latitude
Current Customer
Longitude

Optional  Sample
N

40° 45′ 0″ N

N

14° 29′ 10″ E

Comments
Jean’s Latitude
provided by GPS
Jean’s Longitude
provided by GPS

Data Response
This is an example of results included in a list/map of the closest locations.

Description
Store Number
Address
Street Name
Unit
City
State
Zip code

101
4145
Forest Park

Optional  Sample
Y
Y
Y
Y
Y
Y
Y

Chicago
Illinois
60125

Comments

Assumptions:
IVR tells her location    N

IVR system

Tells driver where
store is and
distance from Jean

9.1.2 ARTS XML Instance Document: Find closest Store while Driving Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Request" ActionCode="Inquiry">

Copyright  2017 NRF.  All rights reserved.

Page 34

ARTS Location 2.0 Technical Specification

        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit Name="Halter's Emporium">100</BusinessUnit>
    </ARTSHeader>
    <Location>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
            <SearchRange UOM="SMI">5</SearchRange>
        </SourceLocation>
    </Location>
</Location>

9.1.2 ARTS XML Instance Document: Find closest Store while Driving Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Response" ActionCode="Inquiry">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
        <BusinessUnit Name="Halter's Emporium">100</BusinessUnit>
    </ARTSHeader>
    <Location>
        <DestinationLocation>
            <Address>
                <AddressLine>4145 Forest Park</AddressLine>
                <City>Chicago</City>
                <Territory>Illinois</Territory>
                <PostalCode>60125</PostalCode>
            </Address>
            <BusinessUnit>101</BusinessUnit>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 35

ARTS Location 2.0 Technical Specification

9.2  Use Case: User is driving in a car or using a mobile phone/tablet

to find product from a specific retailer near them. – V1.0.0

9.2.1  Scenario: Find Closest Store with Item – V1.0.0

Figure 11: Find Closest Store with Item BPM

A retail customer with a trusted retailer smartphone application would like to find the product
closest to them.  User would use the application to find the nearest store that stocks the
product.

Brief Description
The purpose of this function is to leverage the user’s proximity to find the closest Product
location to the user.

Pre-conditions

•  The user’s mobile device is on and the user has the retailer’s trusted application
•  The user is opted-in to Location Services for the application
•  The application has access to retailer’s store product information and location systems
•  The user’s mobile device currently has data connectivity
•  User’s phone Locate me (GPS) needs to be turned on to show users location
•  Or possible enter in a zip code for the location where store search is requested

Scenario Description
Jean wants to pick up thyme for a recipe and wants to find the closest location for the product.
Using her location, the app shows her the closest store that carries the product from her
location.

Data Request

Copyright  2017 NRF.  All rights reserved.

Page 36

Business Process Find Store with ItemInventory ServiceLocation ServiceCustomerIdentify ItemIdentify ItemSearch for Nearest Store with this ItemSearch for Nearest Store with this ItemLocationLookup LocationLookup LocationARTS DataModelSearch InventorySearch InventoryInventoryLocation ItemLocation ItemARTS DataModelReport Store with ItemReport Store with ItemInventoryDisplay Store LocationDisplay Store LocationLocationCurrentLocation

ARTS Location 2.0 Technical Specification

Description
Item identifier

Optional  Sample
678743
N

Current Customer
Latitude
Current Customer
Longitude

N

N

40° 45′ 0″ N

14° 29′ 10″ E

Comments
Item sku is
expected to be
found by an earlier
service or scanned
(entered).
Jean’s Latitude
provided by GPS
Jean’s Longitude
provided by GPS

Data Response
This is an example of results included in a list/map of the closest locations that carry the product.

Description
Store Number
Address
Street Name
Unit
City
State
Zip code

101
4145
Forest Park

Optional  Sample
Y
Y
Y
Y
Y
Y
Y

Chicago
Illinois
60125

Comments

9.2.1 ARTS XML Instance Document: Find Closest Store with Item Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Request" ActionCode="Inquiry">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
            <ItemID>67843</ItemID>
        </SourceLocation>
    </Location>

Copyright  2017 NRF.  All rights reserved.

Page 37

ARTS Location 2.0 Technical Specification

</Location>

9.2.1 ARTS XML Instance Document: Find Closest Store with Item Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Response" ActionCode="Inquiry">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
        <BusinessUnit Name="Halter's Emporium">100</BusinessUnit>
    </ARTSHeader>
    <Location>
        <DestinationLocation>
            <Address>
                <AddressLine>4145 Forest Park</AddressLine>
                <City>Chicago</City>
                <Territory>Illinois</Territory>
                <PostalCode>60125</PostalCode>
            </Address>
            <BusinessUnit>101</BusinessUnit>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 38

ARTS Location 2.0 Technical Specification

9.3   Use Case: Check if a nearby retailer carries items from a

shopping list – V1.0.0

Figure 12: Check if Retailer Carries Items on Shopping List

9.3.1  Scenario:  Which items (multiple) are carried by nearby retailer

User would like to find out which items from their shopping list are carried by nearby retailers,
retrieve the retailers’ locations and be directed to the items.

Brief Description:
A mobile user has a shopping list of items they wish to purchase.  The user wants to find items
near them from the list available for purchase.

Pre-condition:
The customer has installed and opted-in to the retailer’s application or the aggregator’s
application and has the app loaded on their mobile device.

The mobile device provides customer location.  If the device does not provide customer
location, the use may enter their location (e.g. zip code or cross streets).

Items in the shopping list have UPC codes or other unique ItemID, preferably a collection of
POSLog item entities.

Scenario Description:
Susan constructs a shopping list.  This may involve keyword searches and item browsing, but
the result is a shopping list of unique IDs for the items (e.g. UPC).

This interface supports the call from the mobile app server to a retailer’s item location service.
The retailer’s item inventory location service responds with the locations of outlets that carry the
items in the list, which items can be found.

Data Request:

1.  Customer Location:  Lat/Long.
2.  Item Collection:  PLU codes, preferably POSLog item entities.

Copyright  2017 NRF.  All rights reserved.

Page 39

Business Process Find Items in StoreInventory ServiceLocationServiceCustomerSelect StoreSelect StoreSend List of ItemsSend List of ItemsFind Items in ListFind Items in ListLocationLook up ItemsLook up ItemsInventoryARTS DataModelReport Items Found in StoreReport Items Found in StoreInventoryDisplay Found ItemsDisplay Found ItemsLocation

ARTS Location 2.0 Technical Specification

3.  Search Radius (value or abstract, left to implementation).

Data Response:

1.  Store locations that carry items from the shopping list.
2.  For each store location in the response, collection of items found at that location.  Can

include extended item properties.

Assumptions:
Retailer may decide to replace items with substitutions or add comparison items, i.e. private
label price comparison.

Retailer may also want to offer marketing promotions.  These promotions may include
incentives like immediate order and in-home delivery, branding statements and graphics.

The retailer might keep track of the customer’s LoyaltyID and attach the appropriate customer
info to the request so the retailer can present special offers based on loyalty.

The retailer might attach manufacturer coupon promotions to the list.

The items may be ordered or categorized by the retailer or later by the aggregator for instance
to place refrigerated items later in the pick-list.

9.3.1 ARTS XML Instance Document: Which items are carried by nearby retailer request
<?xml version="1.0" encoding="UTF-8"?>
<!-- Find the nearest store from my location containing these items  -->
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Request" ActionCode="Inquiry">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <SourceLocation>
            <!-- Here is where I am -->
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
            <!-- search within 5 miles -->
            <SearchRange UOM="SMI">5</SearchRange>
            <!-- find these items -->
            <ItemID>67843</ItemID>
            <ItemID>234234</ItemID>

Copyright  2017 NRF.  All rights reserved.

Page 40

ARTS Location 2.0 Technical Specification

            <ItemID>567</ItemID>
        </SourceLocation>
    </Location>
</Location>

9.3.1 ARTS XML Instance Document: Which items are carried by nearby retailer response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Response" ActionCode="Inquiry">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <DestinationLocation>
            <Address>
                <AddressLine>200 N Main</AddressLine>
                <City>Chicago</City>
                <Territory>Illinois</Territory>
                <PostalCode>60125</PostalCode>
            </Address>
            <BusinessUnit Name="Halter's Emporium">202</BusinessUnit>
            <!-- find these items -->
            <ItemID>67843</ItemID>
            <ItemID>234234</ItemID>
        </DestinationLocation>
        <DestinationLocation>
            <Address>
                <AddressLine>4145 Forest Park</AddressLine>
                <City>Chicago</City>
                <Territory>Illinois</Territory>
                <PostalCode>60125</PostalCode>
            </Address>
            <BusinessUnit Name="My Store">101</BusinessUnit>
            <!-- find these items -->
            <ItemID>567</ItemID>
        </DestinationLocation>
    </Location>
</Location>

9.4  Use Case: User phone vibrates when they are near an item on

their shopping lists or wish lists – V1.0.0

9.4.1  Scenario: Wish List Notification – V1.0.0

While walking through the audio section of an electronics store, a consumer’s smartphone
vibrates and displays a push notification that says, “You are near the headphones on your
shopping list/wish list, tap for directions."

Copyright  2017 NRF.  All rights reserved.

Page 41

ARTS Location 2.0 Technical Specification

Figure 13: Wish List Notification

Brief Description:
Need to have ability to interact with the consumer based on a known location. Depending on the
customer’s in-store location in relation to their shopping list/wish list, a context relevant
notification is displayed on their smartphone when they become within a specific distance of
items on their shopping list/wish list.

1.  Pre-conditions

Assumes consumer’s mobile device has GPS and it is turned on
Assumes mobile device is turned on and Wi-Fi communications is enabled

Scenario Description:

Peter is a consumer with a common smartphone with a previously downloaded Joe’s
Electronics application and registered personal information. Joe’s Electronics knows Peter’s
shopping list and wish list. They also know the contact policy based on Peter’s submitted
preferences for message and notification frequency.

Peter walks through Joe’s Electronics, as he has regularly done, and begins his shopping and
browsing. As Peter walks near the audio section, his smartphone vibrates and he notices a
visual notification display, “You are near the headphones on your shopping list/wish list, tap for
directions." The targeted notification remains in display until Peter enters the next proximity
triggered area tailored for him.

Data Request

1.  Customer ID
2.  Data
3.  Business Unit ID
4.  Customer-Location Coordinate

Copyright  2017 NRF.  All rights reserved.

Page 42

Business Process Check Inventory AvailabilityCustomer ServicLocation ServiceCustomerLocate CustomerLocate CustomerLocate CustomerLocate CustomerLocationLookup CustomerLookup CustomerCustomerCustomerLookup Wish ListLookup Wish ListARTS DataModelDisplay Wish List ItemsDisplay Wish List ItemsCurrentLocation

ARTS Location 2.0 Technical Specification

Data Response

1.  Customer ID
2.  Communication Content (“The Creative”) – add marketing information – add url to

location of marketing information

a.  Notification - of proximity to item on shopping/wish list (Application shows product

location and tap for more information)

b.  If customer taps for location - second message is sent showing location in the

store

9.4.1 ARTS XML Instance Document - Item Location Near Store Notification Request
<?xml version="1.0" encoding="UTF-8"?>
<!-- Notify me of any items on my wish list that are within 25 feet of my current location -->
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Request" ActionCode="Suggest">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
            <SearchRange UOM="FOT">25</SearchRange>
        </SourceLocation>
    </Location>
</Location>

9.4.1 ARTS XML Instance Document - Item Location Near Store Notification Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">

Copyright  2017 NRF.  All rights reserved.

Page 43

ARTS Location 2.0 Technical Specification

    <ARTSHeader MessageType="Response" ActionCode="Inquiry">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <!-- These items are at this location and are this close to the customer -->
    <Location>
        <DestinationLocation>
            <!-- the items are at this location -->
            <Axis>
                <X-Axis>1</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>3</Z-Axis>
            </Axis>
            <!-- They are this close to the customer -->
            <Distance UnitOfMeasure="FOT">2</Distance>
            <!-- These are the items -->
            <ItemID>67843</ItemID>
            <ItemID>234234</ItemID>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 44

ARTS Location 2.0 Technical Specification

9.5  Use Case: User walks past a store and receives a coupon or offer

– V1.0.0

9.5.1  Scenario:  User receives a coupon while walking past store – V1.0.0

While walking past the mall electronics store, a consumer’s smartphone beeps and displays a
push notification that says “50% off up to $100 for all store purchases.”

Figure 14: Greet Customer with Coupon BPM

Brief Description:
The purpose of this function is to leverage the retailer’s user information as well as their smartphone
application, to provide customized offers to their customers.

Pre-conditions

1.  Assumes consumer’s mobile device has GPS and it is turned on
2.  While consumer privacy is a sensitive element to be considered, however, assumed satisfied if

consumer installs retailer application and agrees purchasing behavior will be analyzed.
3.  The user is opted-in to Location Services and Push Notifications for the application
4.  The user’s mobile device currently has data connectivity

Scenario Description
John is a consumer with a common smartphone and had previously downloaded the Mall electronics
store’s application and registered his account. Since the account has been registered, the Mall electronics
store knows John’s shopping frequency, category and item preferences. They also know the contact
policy based on John’s submitted preferences for message and offer notification frequency.

John walks through his local mall, as he has regularly done, and begins his shopping and browsing. As
John walks near the electronics store, an audible beep from his smartphone sounds out and he notices a
visual message displaying, “50% off up to $100 for all store purchases.” The specially targeted offer for

Copyright  2017 NRF.  All rights reserved.

Page 45

Business Process Greet customer with couponLoyalty ServiceLocation ServicCustomerIdentify Current LocationIdentify Current LocationCompare LocationCompare LocationLocationARTS DataModelSelect CouponSelect CouponPOSLogARTS DataModelReturn CouponReturn CouponPOSLogDisplay CouponDisplay CouponPOSLogCurrentLocation

ARTS Location 2.0 Technical Specification

John is then processed at the point-of-sale automatically without user burden to acknowledge or accept
on his phone.

Data Request

1.  Customer ID
2.  Date
3.  Store ID
4.  Customer-Location Coordinate

Data Response

1.  Customer ID
2.  Communication Content (“The Creative”)

a.  Text
b.  Image
c.  Audio

9.5.1 ARTS XML Instance Document - Receive Coupon in Vicinity of Store Request
<?xml version="1.0" encoding="UTF-8"?>
<!-- If I am in the store, notify me of any coupons -->
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Request" ActionCode="Notify">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
        </SourceLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 46

ARTS Location 2.0 Technical Specification

9.5.1 ARTS XML Instance Document - Receive Coupon in Vicinity of Store Response

<?xml version="1.0" encoding="UTF-8"?>
<!-- If I am in the store, notify me of any coupons -->
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader MessageType="Response" ActionCode="Notify">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <DestinationLocation>
            <URI Type="URL">www.mystore.com</URI>
            <Promotion>
                <PromotionID TypeCode="Coupon">123123</PromotionID>
            </Promotion>
        </DestinationLocation>
    </Location>
</Location>

9.6  Use Case: User greeted digitally at the door by retailer on mobile

device – V1.0.0

9.6.1  Scenario: Receive Greeting on Phone – V1.0.0

Customer enters a retailer’s store and receives a greeting on their mobile device.

Brief Description:
The purpose of this function is to leverage the retailer’s user information as well as their
smartphone application, to provide customized greetings to their customers.

Pre-condition:
•  The user’s mobile device is on and the user has downloaded the retailer’s application
•  The user is opted-in to Location Services for the application
•  The customer has registered their account with the application
•  The user’s mobile device currently has data connectivity
•  User’s phone Locate me (GPS) needs to be turned on to let the store know the user’s

location

Scenario Description:
As John approaches the local Acme Batteries store, the Acme Batteries app activates GPS or
Cell Tower triangulation to find his current location. As John proceeds to walk into the store, the

Copyright  2017 NRF.  All rights reserved.

Page 47

ARTS Location 2.0 Technical Specification

app continues to track his location until he enters the store. Once John has entered the store,
the app sends John a personalized push notification based off the store location and John’s
account information.

Data Request

Description
Customer ID

Optional  Sample
145622
N

Current Customer
Latitude

N

40° 45′ 0″ N

Current Customer
Longitude

N

14° 29′ 10″ E

Data Response

Description
Customer ID

Push Notification
Content

Optional  Sample
145622
N
Welcome to Acme
Batteries John! Open this
message for a Special
Offer!

N

Comments

This data must be
continuously updated
until John enters the
store.
This data must be
continuously updated
until John enters the
store.

Comments

Rich Promotion
Content

Y

<html>Save 25% off any 1
item today only!</html>

Does not include
image or video
assets, which are
linked externally

9.6.1 ARTS XML Instance Document - Receive Greeting on Phone Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Suggest" MessageType="Request">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>

Copyright  2017 NRF.  All rights reserved.

Page 48

ARTS Location 2.0 Technical Specification

                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
        </SourceLocation>
    </Location>
</Location>

9.6.1 ARTS XML Instance Document - Receive Greeting on Phone Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Suggest" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <DestinationLocation>
            <Description>Welcome to Acme Battries John! Open this message for a Special
Offer!</Description>
            <Promotion>
                <PromotionID TypeCode="Coupon">123123</PromotionID>
                <Description>Save 25% off any 1 item today only!</Description>
            </Promotion>
        </DestinationLocation>
    </Location>
</Location>

9.7  Use Case: User wants to check store to see if product is in stock

before going into a store – V1.0.0

9.7.1  Scenario: Check Stock Position – V1.0.0

A retail customer with a retailer’s smartphone application would like to use the application to find
the nearest store that has a product in stock before going to an actual store.

Copyright  2017 NRF.  All rights reserved.

Page 49

ARTS Location 2.0 Technical Specification

Figure 15: Check Stock Position BPM

Brief Description
The purpose of this function is to leverage the retailer’s Inventory Management System as well
as their smartphone application, to direct the customer to the retailer’s nearest store that has the
item that the customer is looking for in stock.

Pre-conditions

•  The user’s mobile device is on and the user has the retailer’s application
•  The user is opted-in to Location Services for the application
•  The application is connected to a database that has real time access to each store’s

Inventory Management System

•  The user’s mobile device currently has data connectivity
•  User’s phone Locate me (GPS) needs to be turned on to show users location
•  Or enter in a zip code for the location where store search is requested

Scenario Description
Bob’s watch battery has died and he wants to find the closest location that has a replacement.
Before leaving for the store, Bob opens the retailer’s application and searches for the battery
type. Once he has found the desired battery, he uses the application to show him the nearest
locations that have the battery in stock.

Data Request

Description
Product SKU

Optional  Sample
N

SKU # 45456645

Search for Brand or

Y

CY8822 (model and

Comments
The product Bob is
searching for.
The product Bob is

Copyright  2017 NRF.  All rights reserved.

Page 50

Business Process Check Stock PositionInventory ServiceLocation ServiceCustomerSelect ItemSelect ItemCurrentLocationLocationSelect ItemSelect ItemCheck Stock PositionCheck Stock PositionInventoryCheck Stock PositionCheck Stock PositionARTS DataModelInventoryReport Stock PositionReport Stock PositionDisplay Stock PositionDisplay Stock PositionLocation

ARTS Location 2.0 Technical Specification

type of battery
Current Customer
Latitude
Current Customer
Longitude

N

N

Data Response

type of battery)
40° 45′ 0″ N

14° 29′ 10″ E

searching for.
Bob’s Latitude
provided by GPS
Bob’s Longitude
provided by GPS

This is an example of 1 store that would be included in a list/map of locations that has the product in
stock.

Comments
Value must be
greater than 0 or
less than specified
in the request.

Description
Inventory Quantity

Optional  Sample
N

2

Store Number
Address
Street Name

Unit
City
State
Zip code

Y
Y
Y

Y
Y
Y
Y

341
3801
S. Capital of Texas
Hwy
Suite 100
Austin
Texas
78704

9.7.1 ARTS XML Instance Document: Check Stock Position Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Inquiry" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
            <ItemID Type="SKU" Name="CY8822">45456645</ItemID>
        </SourceLocation>

Copyright  2017 NRF.  All rights reserved.

Page 51

ARTS Location 2.0 Technical Specification

    </Location>
</Location>

9.7.1 ARTS XML Instance Document: Check Stock Position Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Inquiry" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <DestinationLocation>
            <Address>
                <AddressLine>3801 S. Capital of Texas Hwy</AddressLine>
                <AddressLine TypeCode="Unit">Suite 100</AddressLine>
                <City>Austin</City>
                <Territory>Texas</Territory>
                <PostalCode>78704</PostalCode>
            </Address>
            <BusinessUnit>341</BusinessUnit>
            <ObjectOfInterest>
                <Item>
                    <ItemID Type="SKU" Name="CY8822">45456645</ItemID>
                    <Quantity>2</Quantity>
                </Item>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

9.8  Use Case: User uses augmented reality to find specials or

products near them – V1.0.0

9.8.1  Scenario: Using Augmented Reality for location – V1.0.0

A retail customer with a “coupon aggregator A” smartphone application accesses an augmented
reality feature that allows them to use the device’s camera and screen to view the world around
them with an overlay of specials or products near them.

Copyright  2017 NRF.  All rights reserved.

Page 52

ARTS Location 2.0 Technical Specification

Figure 16: Augmented Reality BPM

Brief Description
Augmented reality is a feature of many smartphone applications that takes the view from the
camera and by using location services, the device compass, and sometimes image recognition,
layers visuals over the camera image that are fixed to physical objects. This allows the app to
“augment” what the camera sees with descriptive pieces of information.
Pre-conditions

•  The user’s mobile device is on and the user has the application with an augmented

reality feature open

•  The user is opted-in to Location Services for the application
•  The user’s mobile device currently has data connectivity

Scenario Description
Susan is a consumer with a common smartphone with a previously downloaded ‘Coupon
Aggregator A’ application. Susan is out running errands and would like to know which specials
or products of interest are nearby. Rather than simply doing a list search, she’d like to see the
specials or products layered on to the retailers’ locations around her. This helps her not only
know what’s around, but also understand which direction to head to get to the special or
product. She activates the augmented reality feature and holds it up, looking at the screen to
see what the app is telling her about her immediate vicinity.

Data

Copyright  2017 NRF.  All rights reserved.

Page 53

Business Process Augmented RealityProduct ContentManagement ServiceItem ServiceLocation ServiceCameraIdentify Camera DirectionIdentify Camera DirectionLocate View DirectionLocate View DirectionLocationARTS DataModelIdentify Items in ViewIdentify Items in ViewIdentify Items at LocationIdentify Items at LocationLocationARTS DataModelRetrieve Item ImagesRetrieve Item ImagesItemPCMRetrieve ImagesRetrieve ImagesARTS DataModelDisplay ImagesDisplay ImagesPCM

ARTS Location 2.0 Technical Specification

It is assumed that the system would make one request to learn about the immediate vicinity,
and then would calculate the direction in which local items of interest lie within the app code.
The app would map another identical request if the user were to move any significant distance.

Data Request

Description
Current Customer
Latitude
Current Customer
Longitude
Customer ID

Data Request

Description
Current Customer
Latitude
Current Customer
Longitude
Customer ID
Points of Interest
(Nested, Multiple)
Point of Interest ID
Point of Interest
Latitude
Point of Interest
Longitude
Point of Interest
Name
Point of Interest
Description

Comments

Optional  Sample
N

40° 45′ 0″ N

N

Y

14° 29′ 10″ E

239810

Optional  Sample
N

40° 45′ 0″ N

Comments

N

Y

Y
Y

Y

Y

14° 29′ 10″ E

239810

103
40° 47′ 2″ N

14° 32′ 7″ E

“Target’s 50% off sale”

“Come by today only to
enjoy 50% off
everything”

Notes:
Assumptions:  Aggregator is aggregating information in the back system and not in the app.
Retailer can determine low bandwidth and high bandwidth content and the aggregator can
determine which content to send based upon device bandwidth.

9.8.1 ARTS XML Instance Document: Using Augmented Reality for Location Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Suggest" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>

Copyright  2017 NRF.  All rights reserved.

Page 54

ARTS Location 2.0 Technical Specification

        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>
            </Coordinates>
        </SourceLocation>
        </Location>
</Location>

9.8.1 ARTS XML Instance Document: Using Augmented Reality for Location Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Suggest" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <!-- the location of the customer -->
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>40</Degrees>
                    <Minutes>45</Minutes>
                    <Seconds>0</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>14</Degrees>
                    <Minutes>29</Minutes>
                    <Seconds>10</Seconds>
                    <Direction>E</Direction>
                </Longitude>

Copyright  2017 NRF.  All rights reserved.

Page 55

ARTS Location 2.0 Technical Specification

            </Coordinates>
        </SourceLocation>
        <!-- a special Shirt -->
        <DestinationLocation>
            <SequenceNumber>1</SequenceNumber>
            <URI Type="URL">www.mystore.com/specialshirt</URI>
            <ObjectOfInterest>
                <Item>
                    <ItemID>1234</ItemID>
                </Item>
                <!-- the location of the item -->
                <Location>
                    <Location>
                        <OriginLocation>
                            <X-Coordinate>1</X-Coordinate>
                            <Y-Coordinate>2</Y-Coordinate>
                            <Z-Coordinate>3</Z-Coordinate>
                        </OriginLocation>
                    </Location>
                </Location>
                <!-- 5 feet away -->
                <Proximity>
                    <Distance UnitOfMeasure="FOT">5</Distance>
                </Proximity>
            </ObjectOfInterest>
        </DestinationLocation>
        <!-- and the pants to go with the shirt -->
        <DestinationLocation>
            <SequenceNumber>2</SequenceNumber>
            <URI Type="URL">www.mystore.com/specialpants</URI>
            <ObjectOfInterest>
                <Item>
                    <ItemID>3456</ItemID>
                </Item>
                <!-- the location of the item -->
                <Location>
                    <Location>
                        <OriginLocation>
                            <X-Coordinate>11</X-Coordinate>
                            <Y-Coordinate>22</Y-Coordinate>
                            <Z-Coordinate>33</Z-Coordinate>
                        </OriginLocation>
                    </Location>
                </Location>
                <!-- 15 feet away -->
                <Proximity>
                    <Distance UnitOfMeasure="FOT">15</Distance>
                </Proximity>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 56

ARTS Location 2.0 Technical Specification

10  Customer Facing

10.1 Use Case: Customer is looking for category of items (cheese) –

V1.0.0

10.1.1  Scenario: Item Category Search – V1.0.0

A retail customer with a retailer's smartphone application would like to find a specific category in
a store using their mobile device (the customer wants to buy cheese and there are many brands
of cheese). This search request will return a list of brands. From there the customer can refine
their search eventually leading to a specific location or multiple locations.  Needs to support
multiple levels of a hierarchy.

Figure 17: Item Category Search BPM

Brief Description:
The customer is in a store and needs to find cheese relative to their mobile GPS or Wi-Fi
location.  The customer does a character search for cheese or navigates a hierarchy of items.

Pre-conditions

•  The user's mobile device is on and the has the retailer's application open (user needs to opt

in).

•  Assumes consumer’s mobile device has GPS, WIFI, and location services enabled and on.
•  Assumes that the item has been supplied in a supported format and that a specific store is

identified.

Scenario Description

Copyright  2017 NRF.  All rights reserved.

Page 57

Business Process Lookup Category of ItemsInventory ServiceLoocation ServiceCustomerIdentify CategoryIdentify CategoryLocate CustomerLocate CustomerARTS DataModelLocate CategoryLocate CategoryLocationLocate CategoryLocate CategoryInventoryARTS DataModelGuide Customer to CategoryGuide Customer to CategoryInventoryGuide CustomerGuide CustomerLocation

ARTS Location 2.0 Technical Specification

As an anonymous customer enters a store, he/she verbally asks their mobile device to find
cheese or dairy products. If the consumer searches for cheese, the mobile device provides a
graphic/list of where the items are located. If the consumer searches for dairy products, the
mobile device provides a graphic/list of where all the dairy products are located.

Data Request

1.  Character (name) search or Category Search (Presenting hierarchy for user to navigate

what type of dairy/cheese)
2.  Consumer location: x, y, z
3.  Date of Request ISO 8601:  2013-11-06 T12:57
4.  Time of Request
5.  General location of the device in the store
6.  Format of data response (floor map or just description, middle aisle 2)

Data Response

1.  Store floor plan graphic highlighting location (graphic first then list, coordinate, aisle, etc.)
2.  Verbal message of where category of items is located.
3.  Floor plan showing customer location and category location.

10.1.1 ARTS XML Instance Document - Item Category Search Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <!-- my current location -->
        <SourceLocation>
            <Axis>
                <X-Axis>0</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>2</Z-Axis>
            </Axis>
            <MerchandiseHierarchy Level="Category">gouda cheese</MerchandiseHierarchy>
            <MerchandiseHierarchy Level="Category">american cheese</MerchandiseHierarchy>
        </SourceLocation>
    </Location>
</Location>

10.1.1 ARTS XML Instance Document - Item Category Search Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"

Copyright  2017 NRF.  All rights reserved.

Page 58

ARTS Location 2.0 Technical Specification

    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <DestinationLocation>
            <Axis>
                <X-Axis>2</X-Axis>
                <Y-Axis>-72</Y-Axis>
                <Z-Axis>31</Z-Axis>
            </Axis>
            <URI Type="URL">www.mystorelayout.com</URI>
            <MerchandiseHierarchy Level="Category">gouda cheese</MerchandiseHierarchy>
        </DestinationLocation>
        <DestinationLocation>
            <Axis>
                <X-Axis>1</X-Axis>
                <Y-Axis>-43</Y-Axis>
                <Z-Axis>22</Z-Axis>
            </Axis>
            <URI Type="URL">www.mystorelayout.com</URI>
            <MerchandiseHierarchy Level="Category">american cheese</MerchandiseHierarchy>
        </DestinationLocation>
    </Location>
</Location>

10.2 Use Case: Customer wants to Order On-line and pickup in closest

store – V1.0.0

10.2.1  Scenario: Order Online – Pickup in Store – V1.0.0

A retail customer with a retailer's smartphone application would like to locate the closest stores
to their mobile device location with ordered item in stock.

Copyright  2017 NRF.  All rights reserved.

Page 59

ARTS Location 2.0 Technical Specification

Figure 18: Order online - Pickup in Store BPM

Brief Description:
Need to find named retailer’s closest locations with ordered item in stock relative to a
consumer’s mobile GPS location. We need to think about closest locations relative to mode of
transportation (driving, bicycle, walking, public transportation (train routes & schedules, bus
routes & schedules), fastest time, least distance, most use of freeways anything that influences
time to location. If location is in a mall, response needs to include name of mall, mall location,
mall entrance and floor. Requested information could be entered verbally or keyed depending
on device, operating system and application.

Pre-conditions
1.  The user's mobile device is on and has the retailer's application open
2.  Assumes consumer’s mobile device has GPS, WIFI, and location services enabled and on
3.  Assumes consumer's mobile device has voice recognition and translation to text
4.  Default settings for preferred modes of transportation (walk, drive, public transportation) for

consumer may be available

Copyright  2017 NRF.  All rights reserved.

Page 60

Business Process Order online, pickup in storeCustomer Order ServiceInventory ServiceLocation ServiceCustomerLocate Store with Ordered ItemLocate Store with Ordered ItemCurrentLocationLocationLocate Store with Ordered ItemLocate Store with Ordered ItemPOSLogFind Customer OrderFind Customer OrderARTS DataModelFind Nearest Store with ItemFind Nearest Store with ItemFind ItemsFind ItemsInventoryLookupARTS DataModelIdentify Store LocationIdentify Store LocationLocationLocationDisplay Nearest StoreDisplay Nearest Store

ARTS Location 2.0 Technical Specification

Scenario Description
On December 24, 2012 at 2:00 pm eastern, David orders an item on his mobile device to be
picked up at an ACME Batteries store. Before the order is completed, David keys in a request
for a list of ACME Batteries stores with the item in stock within 15 miles. David selects the store
he wants to retrieve the item from. His mobile device location is: Latitude: 29-57'09'' N
Longitude: 073-33'00'' W, Decimal Degrees Latitude: 29.952602 Longitude: -73.5499327.

Data Request

1.  Mobile device: 29-57'09'' N Longitude: 073-33'00'' W
2.  Mobile device Decimal Degrees: Latitude: 29.952602 Longitude: -73.5499327
3.  Current date: 2012-12-24
4.  Current time: 1400
5.  Time zone: Eastern
6.  Retailer brand name: ACME Batteries
7.  Max range in terms of miles: 15

Data Response

1.  List of stores within range
2.  Open and close hours by day of week
3.  Address of each store
4.  Distance from consumer's mobile device
5.  Longitude / Latitude of each store

10.2.1 ARTS XML Instance Document - Order Online – Pickup in Store Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>2012-12-24T14:00:00.000+01:00</DateTime>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <SourceLocation>
            <!-- my current location -->
            <Coordinates>
                <Latitude>
                    <Degrees>29</Degrees>
                    <Minutes>952</Minutes>
                    <Seconds>602</Seconds>
                </Latitude>
                <Longitude>
                    <Degrees>-73</Degrees>
                    <Minutes>549</Minutes>
                    <Seconds>9327</Seconds>
                </Longitude>
            </Coordinates>

Copyright  2017 NRF.  All rights reserved.

Page 61

ARTS Location 2.0 Technical Specification

            <!-- Store I'm looking for -->
            <BusinessUnit Name="ACME Batteries"/>
            <!-- within this range from my location -->
            <SearchRange UOM="SMI">15</SearchRange>
        </SourceLocation>
    </Location>
</Location>

10.2.1 ARTS XML Instance Document - Order Online – Pickup in Store Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <DestinationLocation>
            <Address>
                <AddressLine>123 Main</AddressLine>
            </Address>
            <BusinessUnit Name="Joe's Batteries"/>
            <URI Type="URL">www.JoesBatteries.com</URI>
        </DestinationLocation>
        <DestinationLocation>
            <Address>
                <AddressLine>2226 E 1st</AddressLine>
            </Address>
            <BusinessUnit Name="Best Batteries"/>
            <URI Type="URL">www.BestBatteries.com</URI>
        </DestinationLocation>
    </Location>
</Location>

10.2.2  Scenario: Locate Nearest Specific Retailer with this Item – V1.0.0

Locate closest stores to my computer location for a specific brand name retailer with ordered
item in stock.

Copyright  2017 NRF.  All rights reserved.

Page 62

ARTS Location 2.0 Technical Specification

Figure 19: Locate Nearest Specific Retailer with this Item BPM

Brief Description:
Need to find named retailer’s closest locations with ordered item in stock relative to a
consumer’s computer location. Think about closest location relative to mode of transportation
(driving, bicycle, walking, public transportation (train routes & schedules, bus routes &
schedules), fastest time, least distance, most use of freeways anything that influences time to
location. If location is in a mall response needs to include name of mall, mall location, mall
entrance and floor. Requested information could be entered verbally or keyed depending on
device, operating system and application.

Pre-conditions

1.  Assumes consumer’s computer provides access to the IP address (your exact location

isn’t provided, but using IP gives a chance to guess what location may be most relevant
for you) or the consumer can just type in the address or location they are at or plan on
being at

2.  Default settings for preferred modes of transportation (walk, drive, public

transportation) for consumer may be available

Scenario Description
On December 24, 2012 at 2:00 pm eastern, David orders an item on his computer to be picked
up at an ACME Batteries store.  Before the order is completed, David keys in a request for a list
of ACME Batteries stores with the item in stock within 15 miles.  David selects the store he
wants to retrieve the item from.  His computer device location is: Latitude: 29-57'09'' N
Longitude: 073-33'00'' W, Decimal Degrees Latitude: 29.952602 Longitude: -73.5499327.

Data Request

1.  Computer device: 29-57'09'' N Longitude: 073-33'00'' W
2.  Computer Decimal Degrees: Latitude: 29.952602 Longitude: -73.5499327

Copyright  2017 NRF.  All rights reserved.

Page 63

Business Process Find Store with ItemInventory ServiceLocation ServiceCustomerIdentify ItemIdentify ItemSearch for Nearest Store with this ItemSearch for Nearest Store with this ItemLocationLookup LocationLookup LocationARTS DataModelSearch InventorySearch InventoryInventoryLocation ItemLocation ItemARTS DataModelReport Store with ItemReport Store with ItemInventoryDisplay Store LocationDisplay Store LocationLocationCurrentLocation

ARTS Location 2.0 Technical Specification

3.  Current date: 2012-12-24
4.  Current time: 1400
5.  Time zone: Eastern
6.  Retailer brand name: ACME Batteries
7.  Max range in terms of miles: 15

Data Response

1.  List of stores within range
2.  Open and close hours by day of week
3.  Address of each store
4.  Distance from consumer's computer
5.  Longitude / Latitude of each store

10.2.2 ARTS XML Instance Document - Locate Specific Brand Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <!-- my current location -->
        <SourceLocation>
            <Axis>
                <X-Axis>0</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>2</Z-Axis>
            </Axis>
            <MerchandiseHierarchy Level="Category">gouda cheese</MerchandiseHierarchy>
            <MerchandiseHierarchy Level="Category">american cheese</MerchandiseHierarchy>
        </SourceLocation>
    </Location>
</Location>

10.2.2 ARTS XML Instance Document - Locate Specific Brand Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>

Copyright  2017 NRF.  All rights reserved.

Page 64

ARTS Location 2.0 Technical Specification

        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <DestinationLocation>
            <Address>
                <AddressLine>123 Main</AddressLine>
            </Address>
            <BusinessUnit Name="Joe's Batteries"/>
            <URI Type="URL">www.JoesBatteries.com</URI>
        </DestinationLocation>
        <DestinationLocation>
            <Address>
                <AddressLine>2226 E 1st</AddressLine>
            </Address>
            <BusinessUnit Name="Best Batteries"/>
            <URI Type="URL">www.BestBatteries.com</URI>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 65

ARTS Location 2.0 Technical Specification

10.3 Use Case: Customer Receives Targeted communication based on

their in-store location – V1.0.0

10.3.1  Scenario: Special Offer Based on In-Store Location – V1.0.0

While shopping inside a grocery store near a specific category, a consumer’s smartphone
beeps and displays a message: “Special Offer: 2 for 1 Acme Kids Cereal”. Retailer knows the
specific consumer location & category proximity and has ability to assess the loyalty and value
of the shopping consumer with attempts to influence spends a return visit and strengthens
loyalty.

Figure 20: Special Offer Based on In-Store Location BPM

Brief Description:
Retailers can influence purchase spend and a return shopping visit with ability to learn about
customer’s purchase patterns. This is enhanced with the ability to interact with the consumer
based on a known in-store position. Depending on the consumer’s previous shopping patterns,
a context relevant message is displayed on their smartphone of either product knowledge,
shopping list reminder or special offer.

Pre-conditions

•  Context relevant messages are considered in-store for this scenario.
•  Outside store relevant messages would be a different scenario.
•  While consumer privacy is a sensitive element to be considered, however, assumed

satisfied if consumer installs retailer application and agrees purchasing behavior will be
analyzed.

•  The user's mobile device is on and the has the retailer's application open.

Copyright  2017 NRF.  All rights reserved.

Page 66

Business Process Greet customer with couponLoyalty ServiceLocation ServicCustomerIdentify Current LocationIdentify Current LocationCompare LocationCompare LocationLocationARTS DataModelSelect CouponSelect CouponPOSLogARTS DataModelReturn CouponReturn CouponPOSLogDisplay CouponDisplay CouponPOSLogCurrentLocation

ARTS Location 2.0 Technical Specification

•  Assumes consumer’s mobile device has GPS, WIFI, and location services enabled and

on.

•  Assumes that the item has been supplied in supported format and that a specific store is

identified.

Scenario Description
Mary is a consumer with a common smartphone with a previously downloaded ‘Retailer A’
application and registered personal information. Retailer A knows Mary’s shopping frequency,
category and item preferences. They also know the contact policy based on Mary’s submitted
preferences for message and offer notification frequency.

Mary walks into her local store, as she has regularly done, and begins her shopping task. As
Mary walks through the Cereal aisle, an audible beep out from her smartphone sounds out and
notices a visual message display “2 for 1 Acme Kids Cereal”. She often buys cereal every other
week and because of a high probability of a cereal purchase this week, she is prompted by a
sponsor cereal vendor for a special offer.

The request data consists simply of whom, when and where. A mid-service would map this to
appropriate category proximity and offer optimization engine. The response data is a marketer’s
creative message of text, image, bar code, or image that represents a store layout, product
knowledge info or incentive offer.

The targeted message remains in display until she enters the next proximity triggered area
tailored for her. All targeted offers remain valid for the store and day and are one-time use. The
specially targeted offer for Mary is processed at the point-of-sale automatically without user
burden to acknowledge or accept on her phone.

Data Request

1.  Customer ID
2.  Date
3.  Store ID
4.  Customer-in store Location Coordinate

Data Request

1.  Customer ID
2.  Communication Content (“The Creative”) (URI)

a.  Text
b.  Image
c.  Audio
d.  Video

10.3.1 ARTS XML Instance Document - Special Offer Based on In-Store Location Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <!-- Inform store here is where I am -->
    <ARTSHeader ActionCode="Information" MessageType="Request">
        <MessageID>1234</MessageID>

Copyright  2017 NRF.  All rights reserved.

Page 67

ARTS Location 2.0 Technical Specification

        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <!-- my current location -->
        <SourceLocation>
            <Axis>
                <X-Axis>0</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>2</Z-Axis>
            </Axis>
        </SourceLocation>
    </Location>
</Location>

10.3.1 ARTS XML Instance Document - Special Offer Based on In-Store Location
Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Information" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <DestinationLocation>
            <URI Type="URL">www.myspecialoffer.com</URI>
            <ItemID Name="blue shirt"/>
            <Promotion>
                <PromotionID>abcd</PromotionID>
                <Percent>15</Percent>
            </Promotion>
        </DestinationLocation>
        <DestinationLocation>
            <URI Type="URL">www.myotherspecialoffer.com</URI>
            <ItemID Name="yellow hat"/>
            <Promotion>
                <PromotionID>asdffd</PromotionID>
                <Percent>10.00</Percent>
            </Promotion>
        </DestinationLocation>

Copyright  2017 NRF.  All rights reserved.

Page 68

ARTS Location 2.0 Technical Specification

    </Location>
</Location>

10.4 Use Case: Customer is looking for physically related objects –

V1.0.0

10.4.1  Scenario: Find the restroom – V1.0.0

A retail customer with a retailer's smartphone application would like to find the closest physical
object (rest rooms, staircases, elevators, entrances, exits, vending machines, customer service,
concessions, major departments (men’s, women’s), emergency exits, cash register, fire
extinguishers, ATMs, etc.) in a store using their mobile device.

Figure 21: Find Nearest Restroom BPM

Brief Description:
Customer is in a store and needs to find the nearest rest room.  The customer does a character
search for rest room or navigates a hierarchy of physical objects.

Pre-conditions

•  The user's mobile device is on and the has the retailer's application open (user needs to

opt in)

•  Assumes consumer’s mobile device has GPS, WIFI, and location services enabled and

on.

•  Assumes that the object has been supplied in a supported format and that a specific

store is identified

•  Assumes objects are included on floor maps (cad plans usually have physical objects) in

supported format

Copyright  2017 NRF.  All rights reserved.

Page 69

Business Process Find RestroomStore Layout ServiceLocation ServiceCustomerLocate RestroomLocate RestroomCurrentLocationLocationFind Nearest RestroomFind Nearest RestroomFind RestroomFind RestroomARTS DataModelLocationStoreLayoutDisplay Nearest RestroomDisplay Nearest RestroomDisplay Nearest RestroomDisplay Nearest RestroomLocation

ARTS Location 2.0 Technical Specification

Scenario Description
As an anonymous customer enters a store, he/she verbally asks their mobile device the location
of the nearest rest room. The app responds either with a character address (2nd floor next to
men’s pants) or renders actual graphic with location of customer and rest room.

Data Request

1.  Customer ID
2.  Date
3.  Store ID

Customer-Location Coordinate

4.  Object searched for

Data Response

1.  Customer ID
2.  Graphic with you are here, physical object (embedded image (store map) or url (image

generated by server))

3.  Text list of object with description (multiples if exist)

10.4.1 ARTS XML Instance Document - Find the restroom Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <!-- my current location -->
        <SourceLocation>
            <Axis>
                <X-Axis>0</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>2</Z-Axis>
            </Axis>
            <BusinessUnit>2332</BusinessUnit>
            <ObjectOfInterest>
                <ObjectID TypeCode="Restroom"/>
            </ObjectOfInterest>
        </SourceLocation>
    </Location>
</Location>

10.4.1 ARTS XML Instance Document - Find the restroom Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"

Copyright  2017 NRF.  All rights reserved.

Page 70

ARTS Location 2.0 Technical Specification

    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <BusinessUnit>123345</BusinessUnit>
        <!-- Here is where the nearest restroom is located -->
        <DestinationLocation>
            <Axis>
                <X-Axis>2</X-Axis>
                <Y-Axis>-72</Y-Axis>
                <Z-Axis>31</Z-Axis>
            </Axis>
            <!-- here is a map showing its location -->
            <URI Type="URL">www.mystorelayout.com</URI>
            <ObjectOfInterest>
                <ObjectID TypeCode="Restroom"/>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 71

ARTS Location 2.0 Technical Specification

11  Operations

11.1 Use Case: Store Setup – V1.0.0

11.1.1  Scenario: Get a Map of the Store – V1.0.0
Get the floor plan for a specific store and determine the orientation of the floor plan and the
location of the main entrance.

Figure 22: Get a Map of the Store BPM

Brief Description
The purpose of this is to arrive at the store and then be able to navigate around the store.
Reasons for this may include:

•  A 3rd party company may be doing research for competitive price lookup.
•  A survey team may be sent to store to review the current layout of a department.

The floor plan may not be orientated such that North is pointing up on the plan, and the
entrance may not be at the bottom of the floor plan.

There may also be multiple entrances, on different floors, particularly if it is a shopping mall.

The coordinates system used will be in accordance defined in the “LCWD ARTS Coordinate
System Insertion Points White Paper”, so that the origin is defined in the upper left corner of the
store as viewed on a floor-plan.

Pre-conditions:
The floor plan detail is defined as object data, using a Cartesian coordinate system.
Alternatively, the system may hold on file standard images of the floor-plan on which the
entrances are marked, or the images can be pre-rendered and then sent.

Copyright  2017 NRF.  All rights reserved.

Page 72

Business Process Get a Map of the StoreStore Layout ServiceCustomerCurrentLocationGet Store MapGet Store MapLocationGet Store MapGet Store MapARTS DataModelLocationDisplay Store MapDisplay Store Map

ARTS Location 2.0 Technical Specification

Dennis has a mobile device that knows his current geographical location.

The floor-plan has been mapped and the objects such as department-areas and entrance
locations are defined.

Scenario Description
Dennis has arrived at the store and found the main entrance. He now wants to see his current
location on a map of the store. He also wants to locate all other entrances and exits, if they
exist.

Dennis may not know the store number, in which case his geographical location can be used to
identify the store at which he has arrived.

Data Request
Description
Date of Request
Store Retailer
Desired format of
response
Floor Level
Store Number
Store Address

Latitude, Longitude
Date for data

Optional  Sample
N
N
N

1 Jun 2013 09:15:47
FoodMart
Map

Y
Y
Y

Y
Y

2
341
Unit 16, 108 Sixth
Avenue, New York
51.752725,-0.339436
2013-10-31

Comments

Picture / Map / List
/ Hyperlink
Default to Level 1

Alternative Input
Options

Indicate whether
we want a
historical, current
or future floor plan.
Default to current
date

Data Response
Description
Store Retailer
Date for Data

Floor Level
Floor Plan Orientation

Store Floor Plan

1)  Static Picture

2)  Data to Construct Store Map

a)  Units of Measure
b)  Building Outline
c)  Fixturing positions
d)  Position of each entrance

Comments

Date when plan was last
revised

Angle of North Arrow.
This would help the user
orient the map when
they are at the entrance
(assuming they know
where North is)
The response would be
determined by desired
format of response.

Sample
FoodMart
2013-09-15

2
45

101.jpg

Inches
(data structure
defined in
OP008)

Copyright  2017 NRF.  All rights reserved.

Page 73

ARTS Location 2.0 Technical Specification

(center position of each
entrance)

i.  Flag to indicate if Main

Entrance

Y
48.9, -50.0

3)  X,Y List (Need naming convention to

define locations)

a)  Department
b)  Aisle

4)  Hyperlink

11.1.1 ARTS XML Instance Document - Get a Map of the Store Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <!-- Requesting a map of the floor -->
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit Name="FoodMart">341</BusinessUnit>
        <!-- my current location in the store -->
        <SourceLocation>
            <Axis>
                <X-Axis>0</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>2</Z-Axis>
            </Axis>
            <ObjectOfInterest>
                <ObjectID TypeCode="Floor">2</ObjectID>
            </ObjectOfInterest>
        </SourceLocation>
    </Location>
</Location>

11.1.1 ARTS XML Instance Document - Get a Map of the Store Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>

Copyright  2017 NRF.  All rights reserved.

Page 74

ARTS Location 2.0 Technical Specification

        </Response>
    </ARTSHeader>
    <Location ResponseFormat="Picture">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit Name="FoodMart">341</BusinessUnit>
        <DestinationLocation>
            <!-- Map of the 2nd floor -->
            <URI Type="URL">2ndfloor.jpg</URI>
            <ObjectOfInterest>
                <ObjectID TypeCode="Floor">2</ObjectID>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 75

ARTS Location 2.0 Technical Specification

11.2 Use Case: Get Stock from Warehouse – V1.0.0

11.2.1  Scenario: Get Stock from Warehouse – V1.0.0

An order is being fulfilled at the warehouse to replenish merchandise at a store. The product
items are then stacked on the pallet in such a way that the pallet can be taken directly to the
floor.

NOTE: Accommodates the macro and isn’t dependent of the micro planogram detail. For
example, data fields #1 to #7 in the tech spec for this use-case are macro and still satisfy the
use case.

Figure 23: Get Stock from Warehouse BPM

Brief Description
To improve the logistics of delivering the products directly to the floor, the product items should
be packed on the pallet in the order that they are to be removed to restock. For instance, all the
product items for aisle #1 might be placed on pallet #1, and all the product items for aisle #9
placed on pallet #2.

Pre-conditions

1.  Presumes the store has a system that identifies where the item is merchandised (e.g. a
database of product locations typically populated by electronic planograms or electronic
shelf labels).

Copyright  2017 NRF.  All rights reserved.

Page 76

Business Process Get Stock from WarehouseLocation ServiceWarehouse ServiceReplenishment ServiceRestocking OrderReceive OrderReceive OrderSupplyOrderRequestBuild Pick ListBuild Pick ListARTS DataModelPick ListBuild PalletsBuild PalletsShip PalletsShip PalletsSupply Order RequestSupply Order RequestLocate ItemsLocate ItemsLocationLocation

Optional  Sample
N

2013-10-14T13:00

Comments
ISO 8601 date & time
format

ARTS Location 2.0 Technical Specification

Data Request

Description
1.    Date and time of

request
2.    Retailer
3.    Store ID
4.    List of Items, each

with unique identifier
or product description

5.   Sort Option

Data Response

N
N
N

Y

ACME
0198

•  GTIN (UPC, EAN,

JAN, etc.)

•  SKU (retailer item

code)

•  Product name, size
•  None (default)
•  Floor
•  Department
•  Aisle & Bay

Description

Sample

1.    Item unique identifier

•  GTIN (UPC, EAN, JAN,

2.    Product description

3.   Floor
4.    X, Y Position
5.    Department

6.    Aisle
7.   Bay

etc.)

•  SKU (retailer item

code)
Product name, size

•  1
•  45.0,-10.6
•  Mens
•  Frozen
•  12
•  6

Unique identifier type may
vary by retailer, but is
supported by the retailer’s
product master query
system

Comments
Unique identifier type
supported by the retailer’s
product master query
system
Provides faster
identification for associate

11.2.1ARTS XML Instance Document - Get Stock from Warehouse Request
<?xml version="1.0" encoding="UTF-8"?>
<Picking xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../PickingV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit Name="ACME">0198</BusinessUnit>
    </ARTSHeader>
    <Pick>
        <Sort SortOrder="Department"/>
        <Basket>
            <PickingOrder>
                <PickingLocation PickingSequence="RightToLeft"/>
                <ItemID>
                    <Quantity>2</Quantity>
                    <ItemID Type="GTIN">123</ItemID>
                </ItemID>

Copyright  2017 NRF.  All rights reserved.

Page 77

ARTS Location 2.0 Technical Specification

                <ItemID>
                    <ItemID Type="SKU">345345</ItemID>
                </ItemID>
            </PickingOrder>
        </Basket>
    </Pick>
</Picking>

11.2.1ARTS XML Instance Document - Get Stock from Warehouse Response
<?xml version="1.0" encoding="UTF-8"?>
<Picking xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../PickingV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <!-- Pick these items in this department in this order -->
    <Pick>
        <Basket>
            <PickingOrder>
                <PickingLocation PickingSequence="LeftToRight">
                    <Location>
                        <Axis>
                            <X-Axis>45</X-Axis>
                            <Y-Axis>0</Y-Axis>
                            <Z-Axis>0</Z-Axis>
                        </Axis>
                    </Location>
                </PickingLocation>
                <ItemID>
                    <Quantity>2</Quantity>
                    <ItemID>123</ItemID>
                </ItemID>
                <ItemID>
                    <ItemID>67896789</ItemID>
                </ItemID>
            </PickingOrder>
        </Basket>
        <AreaSort>Aisle</AreaSort>
        <MerchandiseHierarchy Level="Department">Men's</MerchandiseHierarchy>
    </Pick>
    <!-- Pick these items from this other department in this order -->
    <Pick>
        <Basket>
            <PickingOrder>
                <PickingLocation PickingSequence="RightToLeft">
                    <Location>
                        <Axis>
                            <X-Axis>23</X-Axis>
                            <Y-Axis>10</Y-Axis>

Copyright  2017 NRF.  All rights reserved.

Page 78

ARTS Location 2.0 Technical Specification

                            <Z-Axis>0</Z-Axis>
                        </Axis>
                    </Location>
                </PickingLocation>
                <ItemID>
                    <ItemID>str345</ItemID>
                </ItemID>
                <ItemID>
                    <Quantity>10</Quantity>
                    <ItemID>3456</ItemID>
                </ItemID>
            </PickingOrder>
        </Basket>
        <AreaSort>Aisle</AreaSort>
        <MerchandiseHierarchy Level="Department">grocery</MerchandiseHierarchy>
        <MerchandiseHierarchy Level="SubDepartment">Frozen</MerchandiseHierarchy>
    </Pick>
</Picking>

Copyright  2017 NRF.  All rights reserved.

Page 79

ARTS Location 2.0 Technical Specification

11.3 Use Case: Receiving Items - where to put pallets in store  – V1.0.0

11.3.1  Scenario: Where to put pallets in store – V1.0.0

1.  Pallet received at store and its items need to be unpacked and placed in their
backroom stock holding location to be stocked onto sales floor at future time.
2.  Pallet received at store and needs to be moved temporarily to sales floor aisle so it
can be unpacked and its merchandisable items stocked into its sales location.

3.  Pallet received at store and needs to be moved to sales floor for its point of purchase

display. Merchandise sold directly from pallet, for example a display area or a
warehouse-style retail outlet.

Figure 24: Receiving Pallet BPM

Brief Description
The Data Request is a notification that a pallet has been received at the store and it needs to be
processed. The notification process is not detailed here, but is likely a system generated
request when the pallet is received at the store and items checked into the store’s inventory
system.

Copyright  2017 NRF.  All rights reserved.

Page 80

Business Process Receive Items on PalletReceiving DockBackroomAssociateNotify Pallet ArrivedNotify Pallet ArrivedPallet Arrived NoticePallet Arrived NoticePlace in LocationPlace in LocationIdentify Pallet LocationIdentify Pallet LocationLocationPlace PalletPlace PalletARTS DataModelInventory

ARTS Location 2.0 Technical Specification

The Data Response provides the source location of the pallet, the target location for the pallet,
and instructions on whether the items are to be unpacked or merchandised on the pallet.

The pallet may contain different items with multiple locations, resulting in the data response
returning a list of target locations for its items.

Each pallet job would be a separate Data Request and corresponding Data Response.

Data Response does not perform wayfinder route calculations to optimize the journey from
source storage to target fixture (that is the responsibility of external applications).

Pre-conditions

1.  Presumes the associate and the pallet are in the store, no need to identify store location.
2.  Optimum efficiency assumes the store has a system that identifies the source location of

the pallet (e.g. receiving dock or backroom staging area), or the associate must
manually find the pallet.

Scenario Description
The associate is notified that a pallet was received at the store and needs to be processed. The
notification process will vary and is not covered by this use case. Examples could include a
verbal request by a manager, an electronic communication, or a scheduled delivery.

The associate is notified of the source location of the pallet, which could be a receiving dock or
backroom staging area. Associate retrieves the pallet, identifies the target location, and
transports the pallet to the target location.

The items may be unpacked from pallet into a backroom slot, or onto the designated fixture on
the sales floor.  The pallet may be the point of purchase display with the pallet placed into the
designated area directly on the sales floor (for example a display area, or a rack for warehouse-
style merchandising).

Additional information may be provided by the Data Response, such as instructions for handling
special materials and disposing of the pallet when it has been unpacked.

This use case does not detail the actual placement of items onto their merchandisable location
to adhere to planogram requirements.

Data Request
#

Description

1.   Date and Time of

Request

Optional  Sample
N

2013-10-14T13:00

2.   EffectiveDate

Y

▪  Urgent (now)
▪  Within specific time
frame (avoid out of
stocks)

▪  Sometime during shift

(non-urgent
restocking)

▪  An explicit time like
2013-10-15  14:30

Comments
ISO 8601 date & time
format YYYY-MM-DD
T:HH:MM
Optional, but if not
specified could result in
lost sales (out of stock).
Date range or singular?

3.   Pallet Identifier

N

▪  Shipping label from
distribution center
or direct store

Unique identifier type
may vary by retailer, but
is supported by the

Copyright  2017 NRF.  All rights reserved.

Page 81

ARTS Location 2.0 Technical Specification

4.   Special Material
Classification

5.   Pallet Location

Y

6.   Format of Response for
Target Destination

Y

retailer’s shipping
system

Indicates if special
processing is required
for transport or
unpacking

Location where
receiving crew has
temporarily placed the
pallet
Default format
determined by data
provider.

delivery from
vendor
▪  RFID tag
▪  Shipping invoice

▪  Corrosive liquid
▪  Flammable
▪  Fertilizer
▪  Fragile

▪  Receiving dock #3
▪  Staging area B

▪  X, Y floorplan
coordinate for
receiving device to
interpret

▪  Grocery dept.,

frozen vegetable,
cooler door 6
▪  Aisle 3, bay 5,

shelf 4, position
rank 6

▪  Electronic shelf ID

#n

▪  GLN (Global

Location Number)
for fixture
▪  Graphic map

Data Response
#

Description

1.   Date and Time to Process

2.   Pallet Identifier

3.   Special Material
Classification

Samples
▪  Urgent (now)
▪  Within specific time frame
(avoid out of stocks)

▪  Sometime during shift (non-

urgent restocking)

▪  An explicit time like 2013-

10-15  14:30

Comments
Optional, but if not
specified could result in
lost sales (out of stock)

▪  Shipping label from
distribution center or
direct store delivery from
vendor
▪  RFID tag

Unique identifier type
may vary by retailer, but
is supported by the
retailer’s distribution
system

▪  Corrosive liquid
▪  Toxic solid
▪  Flammable
▪  Fertilizer

Indicates whether
special processing is
required for transport or
unpacking

Copyright  2017 NRF.  All rights reserved.

Page 82

ARTS Location 2.0 Technical Specification

4.   Special Material Instructions

5.   Pallet Source Location

6.   Pallet Destination Location

7.   Pallet Unpacking
Instructions

▪  Glass or Ceramics
▪  Electronics

▪  Fragile ‘handle with care’
▪  Toxic ‘wear gloves and

respirator’

•

▪  Receiving dock #3
▪  Staging area B

▪  Backroom fixture
▪  Aisle for unpacking
▪  Fixed floorplan location
for point of purchase
display

▪  Explicit location similar
to other use cases:
▪  X, Y floorplan coordinate
▪  Graphic map
▪  Etc.

▪  Unpack into backroom

fixture location

▪  Unpack into sales floor

fixture location

▪  Fixed floorplan location
for point of purchase
display

Instructional template
per the Special Material
Classification

Location where
receiving crew has
temporarily placed the
pallet
Location to place pallet
and then process the
Unpacking Instructions

Instructions based on
the 3 scenarios

8.   Unpacked Item Location

▪  X, Y floorplan coordinate
▪  Graphic map
▪  Grocery dept., frozen

vegetable, cooler door 6

If items are to be
stocked onto a fixture
those details not listed
here

▪  Aisle 3, bay 5
▪  Aisle 3, bay 5, shelf 4
▪  Aisle 3, bay 5, shelf 4,

position rank 6

▪  Electronic shelf ID #n
▪  GLN (Global Location
Number) for fixture

▪  Stack in Staging Area X
▪  Stack in recycling dock

Instructions on what to
do with pallet after it has
been unpacked

9.   Pallet Disposal Instructions

11.3.1 ARTS XML Instance Document - Where to put pallets in store
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"

Copyright  2017 NRF.  All rights reserved.

Page 83

ARTS Location 2.0 Technical Specification

    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Instruction" MessageType="Publish">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <!-- Put these pallets -->
    <Location>
        <SourceLocation>
            <ObjectOfInterest>
                <Instructions Action="MoveFrom">
                    <ObjectID TypeCode="Pallet">1234</ObjectID>
                    <ObjectID TypeCode="Pallet">3456</ObjectID>
                    <Location>
                        <Location>
                            <Axis>
                                <X-Axis>1</X-Axis>
                                <Y-Axis>2</Y-Axis>
                                <Z-Axis>3</Z-Axis>
                            </Axis>
                        </Location>
                    </Location>
                </Instructions>
            </ObjectOfInterest>
        </SourceLocation>
        <!-- Unpack the pallet here -->
        <DestinationLocation>
            <ObjectOfInterest>
                <ObjectID TypeCode="Pallet">1234</ObjectID>
                <ObjectID TypeCode="Pallet">3456</ObjectID>
                <Instructions Action="Unpack">
                    <Location>
                        <Location>
                            <Axis>
                                <X-Axis>56</X-Axis>
                                <Y-Axis>57</Y-Axis>
                                <Z-Axis>58</Z-Axis>
                            </Axis>
                        </Location>
                    </Location>
                </Instructions>
            </ObjectOfInterest>
        </DestinationLocation>
        <!-- Stack the pallet there -->
        <DestinationLocation>
            <ObjectOfInterest>
                <ObjectID TypeCode="Pallet">1234</ObjectID>
                <ObjectID TypeCode="Pallet">3456</ObjectID>
                <Instructions Action="MoveTo">
                    <Location>
                        <Location>
                            <Axis>
                                <X-Axis>4</X-Axis>
                                <Y-Axis>5</Y-Axis>
                                <Z-Axis>6</Z-Axis>
                            </Axis>
                        </Location>

Copyright  2017 NRF.  All rights reserved.

Page 84

ARTS Location 2.0 Technical Specification

                    </Location>
                    <Description>Stack in Staging Area X</Description>
                </Instructions>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

11.4 Use Case: Send Floor Plan – V1.0.0

Figure 25: Send Floor Plan BPM

11.4.1  Scenario: Send Floor Plan – V1.0.0

Transfer data which defines a floor plan layout for a store.
Brief Description
A floor plan is required to help locate objects within the store.
The reason for sending this data may include:

•  Display a map of the store
•  Locate products items within the store

o  For restocking
o  For store picking for on-line order
•  Locate product categories within the store
•  Locate promotional bays
•  Locate signage within the store
•  Locate labels within the store
•  Locate serviced equipment within the store, such as a printer, or an oven

Copyright  2017 NRF.  All rights reserved.

Page 85

Business Process Get a Map of the StoreStore Layout ServiceCustomerCurrentLocationGet Store MapGet Store MapLocationGet Store MapGet Store MapARTS DataModelLocationDisplay Store MapDisplay Store Map

ARTS Location 2.0 Technical Specification

•  Locate a fixture bay within the store
•  Locate areas within the store, such as stock-room, entrance, rest rooms, service desk
•  Locate a department within the store
•  Locate an aisle within the store

Pre-conditions:
The floor plan detail is defined as object data, using a Cartesian coordinate system, in
accordance with the ARTS Coordinate System & Insertion Points White Paper.
Scenario Description
Another use case requires map information to render the store’s floor plan.
Data Request
Description
Date of Request
Retailer
Store Code
Floor Level

Optional  Sample
N
N
N
Y

1 Jun 2013 09:15:47
ACME
0002
1

Comments

Area Type
Area Name

Y
Y

Department
Grocery

Level of Detail

Y

Fixture

Date of Floor Plan

Y

1 Aug 2013

Return all floors if
empty
Indicate whether to
return the whole
floor-plan or just a
section of it, e.g.
department or
fixture bay; this
would then be
qualified by the
department name,
of fixture’s bay
number.
This defines how
far down the
parentage
hierarchy we start.
This defines how
far down the
parentage
hierarchy we finish;
for instance, the
user may only need
macro level detail,
in which case it
would stop at
fixture level, and
not send all the
shelf and SKU
details.
Indicate whether
we want a
historical, current
or future floor plan.
Default to current

Copyright  2017 NRF.  All rights reserved.

Page 86

ARTS Location 2.0 Technical Specification

Format

N

Picture / Map / List /
Hyperlink

date
Send data, or just
an image of the
floor-plan

Data Response
Description
Store Number
Floor Level
Effective Date
Expiry Date
Last Published Date
Store Prototype
Status
Units of Measure
List of Attributes

Comments

for Coordinates

Sample
0002
1
25 Jul 2013
1 Sep 2013
3 Jun 2013
01
Authorized
Inches
Manufacturer=Lozier
Number of
Checkouts=8
Store Manager=John
Doe
Language=English

11.4.1 ARTS XML Instance Document: Send Floor Plan Request
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Information" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>2013-01-06T09:15:47.032+01:00</DateTime>
    </ARTSHeader>
    <BusinessUnitConfiguration ResponseFormat="Map">
        <BusinessUnit Name="ACME">002</BusinessUnit>
        <OrganizationHierarchy Level="Department">Grocery</OrganizationHierarchy>
        <FloorSize Floor="1">100</FloorSize>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

11.4.1 ARTS XML Instance Document: Send Floor Plan Response
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>

Copyright  2017 NRF.  All rights reserved.

Page 87

ARTS Location 2.0 Technical Specification

        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <BusinessUnitConfiguration>
        <BusinessUnit Name="ACME">002</BusinessUnit>
        <OrganizationHierarchy Level="Department">Grocery</OrganizationHierarchy>
        <FloorSize Floor="1">100</FloorSize>
        <FloorPlan>
            <URI>www.find_it_here.com</URI>
        </FloorPlan>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

11.5  Use Case: Find Area of Interest – V1.0.0

Brief Description
The purpose of this use case is to find an area of interest within the store, as opposed to
products or items of equipment (which are described in other use cases).  These areas of
interest would represent any area or zone within store that either a store associate or a
customer may wish to find.

What is an area of interest? Region vs door vs find the closest door vs finding the bottom of the
stairs on the floor I am on.  This is application dependent and not message dependent.  The
message contains the coordinates.  What they mean is up to the application.

Pre-conditions:
The areas of interest have been previously captured as object data and stored within a
database.

Optionally, the system will be able to identify the current location of the customer / store
associate to locate the nearest area of interest.

Figure 26: Find "Area of Interest" BPM

Copyright  2017 NRF.  All rights reserved.

Page 88

Business Process Find Area of InterestLocation ServiceCustomerLocate "Area of Interest"Locate "Area of Interest"CurrentLocationLocationFind "Area of Interest"Find "Area of Interest"ARTS DataModelDisplay location of "Area of Interest"Display location of "Area of Interest"LocationArea of Interest include areas like the customerservices department, toys department, restroom, electrical room, elevator, concession area

ARTS Location 2.0 Technical Specification

11.5.1  Scenario: Locate Customer Services Department – V1.0.0

Brief Description
A customer wishes to locate the Customer Services department.

11.5.1 ARTS XML Instance Document: Find Area of Interest Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Inquiry" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location ResponseFormat="Picture">
        <BusinessUnit>100</BusinessUnit>
        <!-- my current location -->
        <SourceLocation>
            <Axis>
                <X-Axis>0</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>2</Z-Axis>
            </Axis>
        </SourceLocation>
        <!-- This is what I'm looking for -->
        <DestinationLocation>
            <ObjectOfInterest>
                <OrganizationHierarchy Level="Department">Customer Service
Department</OrganizationHierarchy>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

11.5.1 ARTS XML Instance Document: Find Area of Interest Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Inquiry" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <!-- This is where the restroom is located -->
        <BusinessUnit Name="FoodMart">341</BusinessUnit>
        <DestinationLocation>
            <Axis>
                <X-Axis>2</X-Axis>
                <Y-Axis>-72</Y-Axis>

Copyright  2017 NRF.  All rights reserved.

Page 89

ARTS Location 2.0 Technical Specification

                <Z-Axis>31</Z-Axis>
            </Axis>
        </DestinationLocation>
    </Location>
</Location>

11.5.2  Scenario: Locate Concession Area – V1.0.0

Brief Description
The Regional Manager for a Dry Cleaners wishes to locate their concession area within a
hypermarket.

Data Request
Description
Date of Request
Store Retailer
Desired format of
response
Floor Level
Store Number
Store Address

Latitude, Longitude
Date for data

Optional  Sample
N
N
N

1 Jun 2013 09:15:47
FoodMart
Map

Y
Y
Y

Y
Y

2
341
Unit 16, 108 Sixth
Avenue, New York
51.752725,-0.339436
2013-10-31

Search Criteria for
Area of interest

N

“Rest Room”

Find Nearest

Y

Yes

Data Response
Description
Store Retailer
Date for Data

Floor Level
Store Floor Plan

5)  Static Picture

Sample
FoodMart
2013-9-15

2

102.jpg

6)  Data to Construct Store Map

a)  Units
b)  Building Outline

Inches
(data structure

Comments

Picture / Map

Default to Level 1

Alternative Input
Options

Indicate whether
we want a
historical, current or
future floor plan.
Default to current
date.
This is the area of
interest to be
found. This could
be a freeform
description or an
enumerator.
Find all or nearest

Comments

Date when plan
was last revised

The response
would be
determined by
desired format of
response.

Copyright  2017 NRF.  All rights reserved.

Page 90

ARTS Location 2.0 Technical Specification

c)  Department boundaries
d)  Fixturing Positions
e)  Location marker(s) to

defined in
OP008)

identify area of interest

12.5,-78.6

•

11.5.2 ARTS XML Instance Document: Locate Concession Area Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Inquiry" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>2013-06-01T09:15:47.032+01:00</DateTime>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <BusinessUnit Name="FoodMart">341</BusinessUnit>
        <!-- my current location -->
        <SourceLocation>
            <Address>
                <AddressLine>108 Sixth Avenue</AddressLine>
                <AddressLine TypeCode="Unit">16</AddressLine>
                <City>New York</City>
            </Address>
        </SourceLocation>
        <!-- This is what I'm looking for -->
        <DestinationLocation>
            <ObjectOfInterest>
                <ObjectID TypeCode="Restroom"/>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

11.5.2 ARTS XML Instance Document: Locate Concession Area Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Inquiry" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <!-- This is where the restroom is located -->

Copyright  2017 NRF.  All rights reserved.

Page 91

ARTS Location 2.0 Technical Specification

        <BusinessUnit Name="FoodMart">341</BusinessUnit>
        <DestinationLocation>
            <Axis>
                <X-Axis>2</X-Axis>
                <Y-Axis>-72</Y-Axis>
                <Z-Axis>31</Z-Axis>
            </Axis>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 92

ARTS Location 2.0 Technical Specification

12  Associate Facing

12.1 Use Case: Locate a specific store within a geographic area –

V1.0.0

12.1.1  Scenario: Locate a specific store within a geographic area – V1.0.0

Locate closest stores to my mobile device location for a specific brand name retailer.

Brief Description:
Need to find named retailer’s closest locations relative to a consumer’s mobile GPS location.
Think about closest location relative to mode of transportation (driving, bicycle, walking, public
transportation (train routes & schedules, bus routes & schedules), fastest time, least distance,
most use of freeways anything that influences time to location.

If location is in a mall response needs to include name of mall, mall location, mall entrance and
floor. Requested information could be entered verbally or keyed depending on device, operating
system and application.

Pre-condition:
1.  Assumes consumer’s mobile device has GPS and it is turned on
2.  Assumes consumer's mobile device has voice recognition and translation to text
3.  Default settings for preferred modes of transportation (walk, drive, public transportation) for

consumer may be available

Scenario Description:
On January 11, 2013 at 3:00 pm eastern Dennis speaks a verbal request into his mobile
device to locate ACME Batteries locations within 10 miles.  His mobile device location
is: Latitude: 33-57'09'' N Longitude: 084-33'00'' W, Decimal Degrees Latitude: 33.952602
Longitude: -84.5499327

Data Request

1.  Mobile device: Latitude: 33-57'09'' N, Longitude: 084-33'00'' W
2.  Mobile device Decimal Degrees: Latitude: 33.952602, Longitude: -84.5499327
3.  Current date: 2013-01-11
4.  Current time: 1500
5.  Time zone: Eastern
6.  Retailer brand name: ACME Batteries
7.  Max range in terms of miles: 10

Data Response

1.  List of stores within range
2.  Open and close hours by day of week
3.  Address of each store

Copyright  2017 NRF.  All rights reserved.

Page 93

ARTS Location 2.0 Technical Specification

4.  Distance from consumer's mobile device
5.  Longitude / Latitude of each store

12.1.1 ARTS XML Instance Document: Locate a specific store: geographic area Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <!-- my current location -->
        <SourceLocation>
            <Coordinates>
                <Latitude>
                    <Degrees>33</Degrees>
                    <Minutes>57</Minutes>
                    <Seconds>09</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>084</Degrees>
                    <Minutes>33</Minutes>
                    <Seconds>00</Seconds>
                    <Direction>W</Direction>
                </Longitude>
            </Coordinates>
            <SearchRange UOM="SMI">10</SearchRange>
            <MerchandiseHierarchy Level="Category">ACME Batteries</MerchandiseHierarchy>
        </SourceLocation>
    </Location>
</Location>

12.1.1 ARTS XML Instance Document: Locate a specific store: geographic area Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>

Copyright  2017 NRF.  All rights reserved.

Page 94

ARTS Location 2.0 Technical Specification

    <Location ResponseFormat="Map">
        <Customer>
            <CustomerID>1234</CustomerID>
        </Customer>
        <BusinessUnit>123345</BusinessUnit>
        <DestinationLocation>
            <Address>
                <AddressLine>1234 Main</AddressLine>
            </Address>
            <Coordinates>
                <Latitude>
                    <Degrees>33</Degrees>
                    <Minutes>57</Minutes>
                    <Seconds>09</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>085</Degrees>
                    <Minutes>33</Minutes>
                    <Seconds>00</Seconds>
                    <Direction>W</Direction>
                </Longitude>
            </Coordinates>
            <BusinessUnit Name="Store 1">My Store</BusinessUnit>
            <!-- 1 mile away  -->
            <Range UOM="SMI">1</Range>
        </DestinationLocation>
        <DestinationLocation>
            <Address>
                <AddressLine>1234 Western</AddressLine>
            </Address>
            <Coordinates>
                <Latitude>
                    <Degrees>33</Degrees>
                    <Minutes>57</Minutes>
                    <Seconds>09</Seconds>
                    <Direction>N</Direction>
                </Latitude>
                <Longitude>
                    <Degrees>085</Degrees>
                    <Minutes>35</Minutes>
                    <Seconds>00</Seconds>
                    <Direction>W</Direction>
                </Longitude>
            </Coordinates>
            <BusinessUnit Name="Store 2">My Store</BusinessUnit>
            <!-- 3 mile away  -->
            <Range UOM="SMI">3</Range>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 95

ARTS Location 2.0 Technical Specification

12.2 Use Case Item Locations – V1.0.0

12.2.1  Scenario: Locate Multiple Items – V1.0.0

Figure 27: Locate Multipe Items BPM

Brief Description
Associate needs to locate a series of items within the store. Reasons for this may include:
1.  Requirement to fulfil a customer’s online order (in preparation for home delivery or customer

collection)

2.  Gaps had previously been recorded (that process is not part of this use case) where certain
items of stock were not on display – and a new delivery has now been received so the
associate needs to replenish the gaps

3.  Remerchandising the store for a new promotional period – needs to know where to locate

the various items

Copyright  2017 NRF.  All rights reserved.

Page 96

Business Process Store PickingOrder ManagementAssociateOnlineOrder ItemOrder ItemPOSLogStore OrderStore OrderARTS DataModelRetrieve OrderRetrieve OrderLocate ItemLocate Item

ARTS Location 2.0 Technical Specification

The response will only supply the location of each item, it will not perform any route calculations
to optimize the journey between each item – that is the responsibility of external applications.

Pre-conditions
Assumes that the list of items has been supplied in an agreed format and that a specific store is
identified.

Scenario Description
The associate is required to find the location of the following products in Store 101:
•  1x Toothpaste Brand A, 100ml
•  1x Shampoo Brand B, 250ml
•  2x Coffee Brand C, 200g

An alternative would be that an item doesn’t exist, in which case it would return null.

Data Request

Description

Optional

Sample

Effective Date of
Request

N

2013-04-25

Time of Request

N

1507

Time Zone
Store Retailer
Store Number

List of Items

N
Y
N

N

GMT
Office Works
101

0038753436531
5000174698107
5011546115481

Comments
This could be the date that the
list was created, or the current
date of the request or a future
date
This could be the time that the
list was created, or the current
time of the request or a future
time

Alphanumeric
EAN
Assume that we don’t need to
pass the Brand or Pack Size
etc.

Data Response

Description

Sample

Response Date

2013-04-25

Response Time

1507

Response Time Zone  GMT

Effective Date of
Request
Effective Time of
Request
Effective Time Zone
Store ID
Store Name

Items and Locations

2013-05-30

2130

GMT
101
Farnham Hart
0038753436531, Location 1
0038753436531, Location 2
5000174698107, Null

Comments
Is this duplication of data within the
header of the message
Is this duplication of data within the
header of the message
Is this duplication of data within the
header of the message

This could be in the future if the
request is for future data

Items could be in multiple locations, or
have no location

Copyright  2017 NRF.  All rights reserved.

Page 97

ARTS Location 2.0 Technical Specification

5011546115481, Location 3

12.2.1 ARTS XML Instance Document: Locate Multiple Items Request
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <Location>
        <BusinessUnit Name="Office Works">101</BusinessUnit>
        <SourceLocation>
            <Axis>
                <X-Axis>0</X-Axis>
                <Y-Axis>-2</Y-Axis>
                <Z-Axis>2</Z-Axis>
            </Axis>
            <ItemID Type="EAN13">0038753436531</ItemID>
            <ItemID Type="EAN13">5000174698107</ItemID>
            <ItemID Type="EAN13">5011546115481</ItemID>
        </SourceLocation>
    </Location>
</Location>

12.2.1 ARTS XML Instance Document: Locate Multiple Items Response
<?xml version="1.0" encoding="UTF-8"?>
<Location xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../LocationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Location>
        <BusinessUnit Name="Farnham Hart">101</BusinessUnit>
        <DestinationLocation>
            <Axis>
                <X-Axis>2</X-Axis>
                <Y-Axis>-72</Y-Axis>
                <Z-Axis>31</Z-Axis>
            </Axis>
            <ItemID>0038753436531</ItemID>
        </DestinationLocation>
        <DestinationLocation>
            <Axis>
                <X-Axis>1</X-Axis>
                <Y-Axis>-43</Y-Axis>

Copyright  2017 NRF.  All rights reserved.

Page 98

ARTS Location 2.0 Technical Specification

                <Z-Axis>22</Z-Axis>
            </Axis>
            <ItemID>5000174698107</ItemID>
        </DestinationLocation>
        <DestinationLocation>
            <ObjectOfInterest>
                <Item Status="NotAvailable">
                    <ItemID>5011546115481</ItemID>
                </Item>
            </ObjectOfInterest>
        </DestinationLocation>
    </Location>
</Location>

Copyright  2017 NRF.  All rights reserved.

Page 99

ARTS Location 2.0 Technical Specification

12.3 Use Case: Store Picking – V1.0.0

Figure 28: Store Picking BPM

12.3.1  Scenario: Store Picking – V1.0.0

A customer shops on-line and places an order. The order is then fulfilled by a store associate
who picks the product items in the store from their various locations.
Brief Description
An order is placed by a customer, who then requires the items to be picked and delivered. The
store associate then takes the order and picks the items in the store, and bags them ready for
delivery. For efficiency purposes, the store associate may have to fulfil multiple orders.

Although the system will not provide any shortest path algorithm, it will provide a sorted list of
items, so that the store associate can pick all the items within an area, for instance, they can
pick all the frozen items last.

Copyright  2017 NRF.  All rights reserved.

Page 100

Business Process Store PickingOrder ManagementAssociateOnlineOrder ItemOrder ItemPOSLogStore OrderStore OrderARTS DataModelRetrieve OrderRetrieve OrderLocate ItemLocate Item

ARTS Location 2.0 Technical Specification

Pre-conditions

1.  Presumes that the data request interface has access to retailer store inventory to
determine if items are in stock and will make any substitutions if appropriate.

2.  Presumes the store has a system that identifies where the item is merchandised (e.g. a
database of product locations typically populated by electronic planograms or electronic
shelf labels).

Data Request

Description

Optional  Sample

Comments

   Date and time of

request
  Retailer
   Store ID
   List of Items, each

with unique identifier
or product description

  Quantity requested

  Units of Measure

  Sort Option 1

  Sort Option 2

Basket

Data Response
Description

N

N
N
N

Y

Y

Y

Y

Y

2013-10-14T13:00

ISO 8601 date & time
format

ACME
0198

•  GTIN (UPC, EAN,

JAN, etc.)

•  SKU (retailer item

code)

•  Product name, size

•  1 (default)
•  2
•  Units (default)
•  Kg
•  Pint

•  None (default)
•  Temperature -
ascending
•  Temperature -
descending

•  Weight - ascending
•  Weight - descending
•  None (default)
•  Aisle
•  Department
•  Department, Aisle,

Bay

•  1

Unique identifier type may
vary by retailer, but is
supported by the retailer’s
product master query
system
Specific quantity

Specify whether the
quantity is in units, weight,
or volume.
Sort by temperature or
weight

Sort by area

Store Associate may be
picking for multiple
baskets. Default will be 1.

Sample

Comments

Item unique identifier

•  GTIN (UPC, EAN, JAN,

etc.)

•  SKU (retailer item

code)

Unique identifier type
supported by the retailer’s
product master query
system

Copyright  2017 NRF.  All rights reserved.

Page 101

ARTS Location 2.0 Technical Specification

Product description

Product name, size

Quantity
Units of Measure

Basket

Floor
X, Y Position
Department

Aisle
Bay
Destination

•  1
•  Units
•  Kg
•  Pint
•  1

•  1
•  45.0,-10.6
•  Men’s
•  Frozen
•  12
•  6
•  Take to delivery van

Provides faster
identification for associate
Same as input
 Same as input

 Same as input. Required
if the store associating is
fulfilling multiple orders.

12.3.1 ARTS XML Instance Document: Store Picking Request
<?xml version="1.0" encoding="UTF-8"?>
<Picking xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../PickingV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Picked" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <BusinessUnit Name="ACME">0198</BusinessUnit>
    </ARTSHeader>
    <Pick>
        <Sort Sort="Temperature"/>
        <Basket>
            <!-- ID for this basket -->
            <BasketID>122</BasketID>
            <PickingOrder>
                <!-- Pork -->
                <ItemID>
                    <Quantity>2</Quantity>
                    <ItemID>123</ItemID>
                </ItemID>
                <!-- Beans -->
                <ItemID>
                    <Quantity>3</Quantity>
                    <ItemID>345654</ItemID>
                </ItemID>
            </PickingOrder>
            <CustomerID>4567df</CustomerID>
        </Basket>
    </Pick>
</Picking>

Copyright  2017 NRF.  All rights reserved.

Page 102

ARTS Location 2.0 Technical Specification

12.3.1 ARTS XML Instance Document: Store Picking Response
<?xml version="1.0" encoding="UTF-8"?>
<Picking xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../PickingV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Picked" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <Pick>
        <Basket>
            <BasketID>122</BasketID>
            <PickingOrder>
                <PickingLocation>
                    <Location>
                        <Axis>
                            <X-Axis>9</X-Axis>
                            <Y-Axis>5</Y-Axis>
                            <Z-Axis>3</Z-Axis>
                        </Axis>
                    </Location>
                </PickingLocation>
                <!-- Pork -->
                <ItemID>
                    <Quantity>2</Quantity>
                    <ItemID>123</ItemID>
                </ItemID>
            </PickingOrder>
            <PickingOrder>
                <!-- Beans -->
                <PickingLocation>
                    <Location>
                        <Axis>
                            <X-Axis>7</X-Axis>
                            <Y-Axis>6</Y-Axis>
                            <Z-Axis>5</Z-Axis>
                        </Axis>
                    </Location>
                </PickingLocation>
                <ItemID>
                    <Quantity>3</Quantity>
                    <ItemID>345654</ItemID>
                </ItemID>
            </PickingOrder>
            <CustomerID>4567df</CustomerID>
            <DeliveryDestination>
                <Location>
                    <Axis>
                        <X-Axis>1</X-Axis>
                        <Y-Axis>2</Y-Axis>
                        <Z-Axis>3</Z-Axis>

Copyright  2017 NRF.  All rights reserved.

Page 103

ARTS Location 2.0 Technical Specification

                    </Axis>
                </Location>
            </DeliveryDestination>
        </Basket>
    </Pick>
</Picking>

12.4   Use Case: Locate retail operations equipment in store  – V1.0.0

Figure 29: Locate Retail Operations Equipment in Store BPM

Brief Discussion
UnifiedPOS is ARTS POS device interface.  Version 2.0 allows a dynamic POS to be
constructed.  To find the devices, UnifiedPOS V2.0 leverages the location schema to find the
nearest available devices.

There are 36 devices described in the UnifiedPOS standard.  This use case is meant to be
representative of the entire collection.

12.4.1  Scenario:  Find Shelf Label Printer to Reprint Damaged Signage – V1.0.0
While walking through a department reviewing the shelves, the store associate finds some
shelf-edge labels have been defaced. Several fixed and mobile printing devices are located
throughout the store. The store associate needs to locate a printing device and request shelf
label reprints to a nearby printer.

Brief Description:
When shelf-tags are damaged and new tags needs to be printed, location can assist the store
associate to select and find a printer to print and pick up the new shelf-tags to hang with the
merchandise.

Scenario Description
Joe walks through an aisle to perform a quick merchandising review. He notices a shelf label for

Copyright  2017 NRF.  All rights reserved.

Page 104

Business Process Locate EquipmentDevice RegistryUnifiedPOS PrinterAssociateRequest Nearest PrinterRequest Nearest PrinterDeviceRegistryFind Nearest PrinterFind Nearest PrinterLocate AssociateLocate AssociateEquipmentLocateEstablish LocationEstablish LocationLabel PrintLabel Print

ARTS Location 2.0 Technical Specification

milk that is unreadable so a new label needs to be printed. Joe scans the item’s barcode and
selects to print a replacement shelf-tag.

He is presented with a list of print devices in the store. Some are stationary (back-office laser
printer, deli counter label printer) and others are mobile in the store (label printer on a mobile
merchandising cart).

The list of printers tells Joe where each printer is located so he can pick an appropriate printing
device that is physically near and active, and find that device to pick up the new shelf-tag for
replacement on the shelf.

Joe selects the Deli Counter printer, prints the temporary replacement shelf tags, picks up the
new tags and hangs them on the shelf in place of the damaged tags.

Data Request

1.  Device Type (printer, pos, scale) “Printer”
2.  Store ID “510”
3.  Store Associate’s location in the store (optional)

Data Response

1.  Devices Discovered:

a.  Device Type (scale, printer, pos) “Printer”
b.  Extended Info “BW, Thermal, 2x3 adhesive labels, IP 10.1.1.52, DeviceID 746”
c.  Status “Operational”
d.  Location “Deli Counter, Store 746, x:4733 y:626”

12.4.1 ARTS XML Instance Document: Find Shelf Label Printer Request
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Request">
        <MessageID>1234</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
    </ARTSHeader>
    <BusinessUnitConfiguration>
        <BusinessUnit>510</BusinessUnit>
        <!-- Associates location within the store -->
        <Location>
            <Location>
                <Axis>
                    <X-Axis>1</X-Axis>
                    <Y-Axis>2</Y-Axis>
                    <Z-Axis>3</Z-Axis>
                </Axis>
            </Location>
        </Location>
        <!-- Looking for a printer -->
        <Equipment>
            <EquipmentID>

Copyright  2017 NRF.  All rights reserved.

Page 105

ARTS Location 2.0 Technical Specification

                <ID Name="Printer"/>
            </EquipmentID>
        </Equipment>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

12.4.1 ARTS XML Instance Document: Find Shelf Label Printer Response
<?xml version="1.0" encoding="UTF-8"?>
<BusinessUnitConfiguration xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/
../BusinessUnitConfigurationV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Search" MessageType="Response">
        <MessageID>9876</MessageID>
        <DateTime>1970-01-01T20:00:00.032+01:00</DateTime>
        <Response>
            <RequestID>1234</RequestID>
        </Response>
    </ARTSHeader>
    <BusinessUnitConfiguration>
        <BusinessUnit>510</BusinessUnit>
        <!-- This printer  -->
        <Equipment>
            <EquipmentID>
                <ID Name="BW, Thermal, 2x3 adhesive labels">746</ID>
                <URI>www.unifiedpos.com</URI>
            </EquipmentID>
            <!-- on this IP address -->
            <DeviceAddress>IP 10.1.1.52</DeviceAddress>
            <!-- is located here -->
            <Location>
                <Location TypeCode="Counter">
                    <Axis>
                        <X-Axis>3</X-Axis>
                        <Y-Axis>4</Y-Axis>
                        <Z-Axis>5</Z-Axis>
                    </Axis>
                </Location>
            </Location>
        </Equipment>
    </BusinessUnitConfiguration>
</BusinessUnitConfiguration>

Copyright  2017 NRF.  All rights reserved.

Page 106

ARTS Location 2.0 Technical Specification

13  Use Case:  Find Non Retail Items – V2.0.0

13.1 Scenario:  Printer has Run Out of Paper – V2.0.0

Scenario Description
Printer 123 is out of paper located in the administrative center.

Data Request

•  Equipment location
•  Equipment status
•  Path type
•  Current location

Data Response:

•  Path to the equipment
•  Path to the paper

13.1ARTS XML Instance Document: Printer has Run Out of Paper Request
<?xml version="1.0" encoding="UTF-8"?>
<Wayfinding xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../WayfindingV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Error" MessageType="Request">
        <MessageID>123123</MessageID>
        <DateTime>2006-05-04T18:13:51.0</DateTime>
        <BusinessUnit Name="My Grocery" TypeCode="RetailStore">A23</BusinessUnit>
    </ARTSHeader>
    <Request RouteType="Service">
        <RouteInstructions>ByDistance</RouteInstructions>
        <Description>Out of paper</Description>
        <!-- Printer -->
        <ObjectOfInterest TypeCode="Device">123</ObjectOfInterest>
        <Location TypeCode="AdministrationCenter"/>
    </Request>
</Wayfinding>

13.1ARTS XML Instance Document: Printer has Run Out of Paper Response
<?xml version="1.0" encoding="UTF-8"?>
<Wayfinding xmlns="http://www.nrf-arts.org/IXRetail/namespace/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/namespace/ ../WayfindingV1.0.0.xsd"
    MajorVersion="1" MinorVersion="0" FixVersion="0">
    <ARTSHeader ActionCode="Inquiry" MessageType="Response">
        <MessageID>sadflkj</MessageID>
        <DateTime>2006-06-04T18:13:51.0</DateTime>
        <Response ResponseCode="OK">
            <!-- the request message to which this is the response message -->
            <RequestID>123123</RequestID>

Copyright  2017 NRF.  All rights reserved.

Page 107

ARTS Location 2.0 Technical Specification

        </Response>
    </ARTSHeader>
    <Route>
        <SourceLocation>
            <Location TypeCode="FrontDoor">
                <SequenceNumber>1</SequenceNumber>
            </Location>
        </SourceLocation>
        <Path>
            <SequenceNumber>1</SequenceNumber>
            <Segment>
                <SequenceNumber>1</SequenceNumber>
                <!-- Printer -->
                <ObjectOfInterest TypeCode="Device">123</ObjectOfInterest>
                <!-- Move down this Aisle -->
                <Move Direction="Right">
                    <SequenceNumber>1</SequenceNumber>
                    <Aisle>1</Aisle>
                </Move>
                <Move Direction="Left">
                    <SequenceNumber>2</SequenceNumber>
                    <Aisle>5</Aisle>
                </Move>
            </Segment>
        </Path>
    </Route>
</Wayfinding>

Copyright  2017 NRF.  All rights reserved.

Page 108

ARTS Location 2.0 Technical Specification

14  GLOSSARY

Term
Facings

Planograms

Definition
The number of product slots on the front of the retail fixture or visible
from the customer viewpoint.
Planograms are documents within Macro Space Management that hold
details of merchandise to be placed into the fixtures within a store.
Planograms define the type, quantity, and arrangement of the sales
goods to be placed on the fixtures.

Fixtures

Lead In
POP

Location
Placement

Planograms are infinitely flexible and can be configured to hold any
combination of products that are suitable configuration for that specific
store fixture in which the products will be placed.
That holds products that are either customer facing or for immediate
replenishment. Examples: bay, gondola, shelf, peg hook, glass case
The starting point for facings (end of the shelf).
Point of Purchase materials. Signage or special fixtures that accompany
the product placement.
Location involves the merchandise within the store
Placement involves the placement within the merchandise fixture such
as shelves or pegs in the store

Copyright  2017 NRF.  All rights reserved.

Page 109

