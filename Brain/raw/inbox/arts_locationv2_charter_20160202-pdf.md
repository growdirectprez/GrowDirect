---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/arts/location/ARTS_LocationV2_Charter_20160202.pdf.md
tags: [canary, arts, retail-data-model, standards-reference, tier1-extract]
project: canary
status: unprocessed
---

# ARTS_LocationV2_Charter_20160202.pdf

## Source
File: `Brain/raw/.extract/tier1-md/arts/location/ARTS_LocationV2_Charter_20160202.pdf.md`
Size: 19,336 bytes

## Raw content
ARTS Location 2.0 Charter
2nd February 2016

Copyright  2016 NRF.  All rights reserved.

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
2 of 14

Table of Contents

1.

INTRODUCTION ........................................................................................... 4

2.  VERSION CHANGE DOCUMENTATION ..................................................... 4

3.  TEAM NAME ................................................................................................ 4

4.  TEAM MISSION ............................................................................................ 4

5.  BUSINESS JUSTIFICATION ........................................................................ 7

6.  RETAIL MODEL INTERFACES/ARCHITECTURAL MODEL ...................... 8

7.  REQUIREMENTS SCOPE FOR VERSION 1.0.0 ......................................... 9

In Scope for Version 1.0 ............................................................................................... 9

Out of Scope for Version 1.0 ........................................................................................ 9

8.  REQUIREMENTS SCOPE FOR VERSION 2.0.0 ....................................... 10

In Scope for Version 2.0.0 .......................................................................................... 10

Out of Scope for Version 2.0.0 ................................................................................... 11

9.  PCI AND SECURITY IMPLICATIONS ........................................................ 11

10.  PRIVACY IMPLICATIONS ......................................................................... 11

11.  INDUSTRY STANDARDS IMPLICATIONS ................................................ 11

12.  BUSINESS VALUE PROPOSITION ........................................................... 12

13.  USE CASE SURVEY .................................................................................. 13

14.  REFERENCES............................................................................................ 14

15.  OUTSTANDING ISSUES ............................................................................ 14

16.  PLANNED DELIVERABLES ...................................................................... 14

Copyright  2016 NRF.  All rights reserved.

Page 2

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
3 of 14

17.  GLOSSARY ................................................................................................ 14

Copyright  2016 NRF.  All rights reserved.

Page 3

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
4 of 14

1. Introduction
This document serves as the ARTS Location Work Team Charter and executive
overview document.  It has been developed following the, ARTS Development Process.

2. Version Change Documentation
Event

Changes
Initial Draft
2nd Draft
3rd Draft
Last Call Working Draft (LCWD)
LCWD submitted to TC for approval
LCWD TC approval with modifications
Version 2
Submitted for Review
Submitted for Approval

Final Review

Circulated to the team  for Approval

Date

3 Nov 2015
22 Dec 2015
14 January
2016
27 January
2016
2 February 2016

Please see the ARTS Technical Report:  Best Practices -- Schema Extensibility
available at https://nrf.com/resources/retail-library/arts-white-papers for the approved
method to extend this and all ARTS schemas.

3. Team Name
The proposed name for this ARTS Work Team is the Location Work Team.

4. Team Mission
Increasing widespread use of mobile devices by both employees and consumers makes
location information extremely important to retailers.  The Location Work Team intent is
to provide a common interface to access location information that can be used by
higher-level applications such as Store Locator, Product Locator, Shelf Restocking,
Geo-Fenced Marketing, etc.

Standardized common interfaces to access information between retail mobile
applications and systems reduce TCO of innovative solutions and permit vendors and
retailers to concentrate on differentiating themselves on service rather than
integrations..

The Location Work Team mission is to define schemas for standardization of the
exchange of location information with mobile devices used by retail customers and
employees.  Categories of business applications include:

Copyright  2016 NRF.  All rights reserved.

Page 4

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
5 of 14

Inventory Management

•  Marketing
•  Visual Merchandising (primary user)
•
•  Customer Service
•  Operations
•  Analytics

Copyright  2016 NRF.  All rights reserved.

Page 5

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
6 of 14

Membership Roster

Board Sponsor:
Bart McGlothin

Chairman:
Graeme Shaw

Authors:
Graeme Shaw
Richard Halter

Contributors:
Kent Ruesink
Andy Mattice
Matthew Kulig
Dennis Blankenship
Karen Shunk
Shannon Byers
John Glaubitz
Michele Kosow
Tai NGama

Cisco

Oracle

Oracle
Global Technology Advisors/ARTS

JDA
Lexmark
Aisle411
Verizon
NRF-ARTS
Nielsen
Vertex Inc
Sophelle
FGL Sports

Copyright  2016 NRF.  All rights reserved.

Page 6

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
7 of 14

5. Business Justification
What would be the
benefits of an ARTS XML
Location/Planogram
standard?

•

•  Promotions based on consumer’s location within and near

the store to drive traffic and conversion
Improved omni-channel customer shopping experience,
for example: ordering on-line and knowing where to pick it
up in the store

•  Retailers and their suppliers can readily exchange

planograms and location documents in standard format
regardless of the application that creates or consumes the
documents. (CPGs currently support multiple major
application formats), which benefits the retailer and
supplier by;

o  Facilitating improved communication and

collaboration, eg displaying planogram details so
that a store associate can set the planogram
o  Reducing errors in the translation of planogram

and location documents

o  Providing standard planogram/location error
handling and correction (collaboration)

o  Reduced implementation time for new suppliers
and internal applications which utilize planogram
and location documents.

o  Reduced integration costs for retailers who

implement planogram/shelf optimization solutions
o  Reduced maintenance costs over the planogram

solution lifecycle

o  Reduce the number of formats that suppliers need

to provide retailers.

o  Freedom to change/adopt components from

technology supplier, so a retailer can switch to
using a different vendor without breaking all
integration points

o  Being able to communicate with automated

devices, such as robots or tablets that check for
compliance, or picking

o  Support for IoT – smart products, smart fixtures,

smart stores

As with other ARTS XML Standards, these benefits are only achievable when a critical

number of participating solutions are in compliance with the standard. For many retailers,
compliance with ARTS XML Standards may become criteria for selection of a planogram/shelf
optimization solution.

Copyright  2016 NRF.  All rights reserved.

Page 7

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
8 of 14

6. Retail Model Interfaces/Architectural Model

Copyright  2016 NRF.  All rights reserved.

Page 8

LocationReplenishmentPrice Optimization(Digital)SignageFixturingProduct Lifecycle ManagementAsset ManagementAssortment PlanningVideo AnalyticsFloorplanPlanogramStore OperationsData Warehouse BIDirect Store DeliveryLoss PreventionMobileIn-Store FulfillmentWEB Orders

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
9 of 14

7. Requirements Scope for Version 1.0.0

In Scope for Version 1.0

For Version 1.0, the primary scope was to enable consumers to interact with the retailer’s
location based apps and to influence higher basket, increased sales and consumer retention.
That is, to enable customers to locate items which are displayed, where they are located, and
how they are presented on a shelf.

•

Identify Store Location, Customer presence near the store or within the store.

•  Location in terms of store, floor, dept/category, aisle, fixture bay, orientation, shelf, XYZ
floor coordinates which would enable a 2d overview of what the store interior looks like.

•  Detailed item information (most specifically unit size)
•  Fixed dimension products only
•  Unit inventory
•
•  Basically linear display and pegs
•  Effective date of planogram and store layout changes

Item placement within a set of fixtures

Out of Scope for Version 1.0

•  Turn by turn directions (way finding) from point A to point B
•  Path of travel from point A to point B
•  Point in time stationary location of entities – movement (path) of customers, products

and associates

•  Define a store layout (macro store space) (store video)

o  Apparel, random weight products
o  Contractual information.
o  Detailed shelf construction information
o  Requires MFG coupon standards for personalized promotions

•  Way finding path obstructions

Copyright  2016 NRF.  All rights reserved.

Page 9

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
10 of 14

8. Requirements Scope for Version 2.0.0
In Scope for Version 2.0.0

Feature
Planogram
Detail

Description

       Detailed fixture/shelf/equipment construction and location
       Product item details (assortment, with core and optional,

add/keep/drop, brand, dimensions etc)

       Product positions
       Inventory model & replenishment methods/periods
       User defined attributes (for product items, planograms, equipment,

product positions, planogram segment)

•  Labels/Signage/Promotional
•  Localization (units, languages, tax codes)
•  Financial Plan/ Reconciliation (to act as an input target to help the Visual

Merchandiser design the planogram)

•  Descriptions (source, author etc, version, dates)
•  Drawing elements (red-lining, notes, text, revision clouds)
•
•  Technology to support Planograms (such as RFID & smart fixtures)

Include Fashion and Random weight categories

Way Finding  Provide directions for a path between two points, or a number of points if

given a shopping list of items to pick.
The standard wouldn’t define how to calculate the shortest path, but would
define how the path would be described.
Localization of path description (Path description could be floor/aisle/bay, or
turn left at a landmark, i.e. using different terminology based on recipient)
Inclusion of obstructions, elevators, escalators, stairs
Require assistance: Item is on top shelf, too heavy, wheelchair route, aisle
widths
Alternate paths
Sorting method for pick lists, eg heavy/frozen items last
Include outside yards/backroom
Picking for multiple lists (compare with warehouse standard)
Take account of IoT standard, with reference to movable objects, such as:

•  Person location
•  Customer
•  Employee
•  Fork lift
•  Shopping Cart
•  Floor waxer
•  Portable Equipment, eg product pallets

Both planogram and way finding require some kind of map or floorplan context.  The floorplan or
map contextual data consists of:

•  A raster image of the store floor plan, as an output
•  A vector image, comprising  of  Cartesian coordinate values to define areas and objects,

including building architectural elements, such as elevators, stairs, common areas,
bathrooms, etc, as well as features that identify, name and describe areas of interest to
the business, such as fixturing and equipment.

•  Planogram and SKU performance data, for analytical purposes.

Copyright  2016 NRF.  All rights reserved.

Page 10

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
11 of 14

Out of Scope for Version 2.0.0

Feature

Description
Virtual worlds
Calculate shortest path
Warehouse Inventory Allocation

9. PCI and Security Implications
If these capabilities are used with PCI compliant payments additional security features may
need to be implemented.

10.  Privacy Implications
Customer location inside or outside a store may be an issue even if the customer has opted-in.
These issues may vary by country, state or city.

Industry Standards Implications

11.
Existing industry standards related to this work will be used as needed.  Examples of industry
standards related to location include:

•  GS1 Global Location Number
•  GS1 EPC Tag Data Standards
•  GPS global positioning standard of longitude, latitude and altitude coordinates
•
•  National BIM Standard US

ISO 17438 Standardization for Indoor Navigation

Copyright  2016 NRF.  All rights reserved.

Page 11

ARTS Location V2.0.0 Charter

Revision Date:
2016-02-02

Page
12 of 14

12.  Business Value Proposition

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
