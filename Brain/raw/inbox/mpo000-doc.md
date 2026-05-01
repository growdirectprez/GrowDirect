---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/mpo000.DOC.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# mpo000.DOC

## Source
File: `Brain/raw/.extract/BP/mpo000.DOC.md`
Size: 43,998 bytes

## Raw content
 TOC \o "1-2" I. Purchase Order Management (Level 2)	 GOTOBUTTON _TOC409997162   PAGEREF _TOC409997162 2
A. Objective and Definition	 GOTOBUTTON _TOC409997163   PAGEREF _TOC409997163 2
B. Critical Success Factors	 GOTOBUTTON _TOC409997164   PAGEREF _TOC409997164 2
C. Assumptions	 GOTOBUTTON _TOC409997165   PAGEREF _TOC409997165 2
D. Requirements	 GOTOBUTTON _TOC409997166   PAGEREF _TOC409997166 5
E. Performance Measures	 GOTOBUTTON _TOC409997167   PAGEREF _TOC409997167 8
F. Issues	 GOTOBUTTON _TOC409997168   PAGEREF _TOC409997168 8
II. Create Purchase Order (Level 3)	 GOTOBUTTON _TOC409997169   PAGEREF _TOC409997169 9
A. Requirements	 GOTOBUTTON _TOC409997170   PAGEREF _TOC409997170 9
B. Jobs Analysis	 GOTOBUTTON _TOC409997171   PAGEREF _TOC409997171 15
C. Reports	 GOTOBUTTON _TOC409997172   PAGEREF _TOC409997172 15
III. Communicate PO to Vendor / Stores (Level 3)	 GOTOBUTTON _TOC409997173   PAGEREF _TOC409997173 17
A. Requirements	 GOTOBUTTON _TOC409997174   PAGEREF _TOC409997174 17
B. Jobs Analysis	 GOTOBUTTON _TOC409997175   PAGEREF _TOC409997175 18
IV. Track Open Purchase Orders (Level 3)	 GOTOBUTTON _TOC409997176   PAGEREF _TOC409997176 18
A. Requirements	 GOTOBUTTON _TOC409997177   PAGEREF _TOC409997177 18
B. Jobs Analysis	 GOTOBUTTON _TOC409997178   PAGEREF _TOC409997178 19
C. Reports	 GOTOBUTTON _TOC409997179   PAGEREF _TOC409997179 20
V. Maintain Purchase Orders (Level 3)	 GOTOBUTTON _TOC409997180   PAGEREF _TOC409997180 20
A. Requirements	 GOTOBUTTON _TOC409997181   PAGEREF _TOC409997181 20
B. Job Analysis	 GOTOBUTTON _TOC409997182   PAGEREF _TOC409997182 21
VI. Manage Shipping Notices (Level 3)	 GOTOBUTTON _TOC409997183   PAGEREF _TOC409997183 21
A. Requirements	 GOTOBUTTON _TOC409997184   PAGEREF _TOC409997184 21
B. Jobs Analysis	 GOTOBUTTON _TOC409997185   PAGEREF _TOC409997185 21
C. Reports	 GOTOBUTTON _TOC409997186   PAGEREF _TOC409997186 21




Purchase Order Management (Level 2)
Objective and Definition
To insure the effective creation, management and communication of purchase order information throughout the supply chain.

Order Management:  involves the creation, tracking and reporting of purchase orders from time of initiation through time of receipt.
Critical Success Factors
Ability to maintain a continuous supply of product to our stores

Ability to manage outstanding purchase commitments
Assumptions

OTB (Open to Buy) may be included in PETsMART processes and encompasses either hard or soft warnings in the process Create Purchase Order.

Shipper creation is included in item set-up.

Store requests and feedback will be handled through a process in Store Operations and are fed through Purchase Order Management through Store Operations.

Contract agreements and policies regarding the handling of Pet Tags and Greeting Cards will be managed in Vendor Management.  The actual process of Pet Tag and Greeting Card ordering will be handled in Purchase Order Management.

Vendor Acknowledgment with the exception of system acknowledgments in EDI (ASN) is not required as part of PO processing.

Rounding requirements are included in both the PO Management and Replenishment processes.

During input all line item order quantities should be listed in eaches.  Base order level is in eaches/pieces.

Different units of measure will not be mixed on a PO.

Truck Building parameters will be managed at the article/vendor master.

Backorder capability will not be provided at the Store level;  Backorders will be allowed at the DC level by Vendor/Site.

Purchase Order updates/changes to quantity, cost, dates, etc. which are initiated by the vendor enter the PO Management process via Vendor Management.

For purposes of the process Communicate PO to Internal/External Party, PETsMART partners can include Vendors, Shipping Lines, and Brokers.

Buyers will negotiate ASN procedures with vendors and any vendor that is able will EDI its ASN.

Discrepancy standards are maintained in vendor management and collected for the vendor scorecard.

Policies and procedures must be identified to make PO shipping and delivery dates consistent and should be set in conjunction with transportation.

Policies and procedures will specify what information is necessary to send to third parties (such as shipping lines, mixing centers, etc.) when a purchase order is created.

Approval for most purchase order will be automatic except in cases of excessive order quantities or variances from previous orders.

Subsequent settlement processing is managed in Finance.

Ability to interface with an external Store Receiving System (RF) and send PO data to that system.

All external interface feeds are managed and validated before the Create Purchase Order process begins. (i.e., UPC database, vendor pricing database, etc.)

Policies and procedures surrounding Vendor Managed Inventory (VMI) will be created so as to support vendor removal of non-selling merchandise (i.e., magazines) and replenishment of merchandise.

Expense Purchase Order Management

Expense purchase orders include orders of items and services not intended for sale.

Expense purchase orders will support the following functional areas:
Facilities
New Stores
Construction
Advertising
Real Estate
Supplies

Expense purchase order and purchase requisition creation is case specific where either a purchase requisition is created and a purchase order is triggered or a purchase order is simply created.  All expense purchases or services will eventually generate an expense purchase order.

Stores have the ability to order supplies and services, but are subject to policies and procedures surrounding store ordering of expense items or services as defined by store operations.

Creation and approval of expense orders and purchase requisitions (PR) will be based in part on order type.

An SAP terminal will be provided in every store in order to create purchase orders and purchase requisitions.

The individual who creates a PO or PR also has the authority to cancel that order or requisition.

Payment for services in Expense POs is based on service/order completion (services are paid for when the PO is accepted).

Changes to an Expense PO require the re-transmission of the order or requisition to the vendor/service provider and will be handled as part of the Maintain Purchase Order process.

Field Managers and Market Managers will have the ability to override purchase order approvals during store emergency situations.

Except as noted below, the Expense PO processes will be defined similarly as processes in Purchase Order Management:
Expense Purchase Order Management inputs into Create Expense PO process include:
Master Data:  site, vendor, item information
Store Operations:  fixtures, equipment, service orders
Capital Budget:  fixtures, equipment, repairs, services
New Store Setup/Construction:  fixtures, equipment, services, studies, surveys.
Advertising/Event Management:  signage, coupons, give-aways, services.
A separate Create Expense PO/PR process has been specified and for expense items replaces the Create PO in Purchase Order Management.

Livestock Purchase Order Management

For the purposes of the Create Livestock Purchase Orders process, livestock includes reptiles, crickets, fish, hand-fed birds and small animals.  Birds other than hand-feds will run through the standard replenishment process.

Cycle counting and the weekly item removal processes will continue.

SSG is responsible for the creation of store livestock assortments (plan-o-grams) and the communication of those assortments to the stores.  SSG is also responsible for managing the availability of livestock items and communicating that availability to the appropriate stores.

Min/max parameters as defined for livestock items will provide system warnings only and are not hard-coded in the system to cancel an order.  Min/max parameters are guidelines to be utilized by the store specialty manager.  Ultimately, the store specialty manager will order the quantity he/she believes to be appropriate for his/her store and be held accountable for that quantity.

In order to manage livestock freight issues, stores will have insight into cost and freight for those items which they are responsible for ordering.

Field Managers will contribute to the creation of a store’s livestock assortment.

Store Operations policies and procedures to be developed will include:
Training to support the livestock ordering process
Training to manage plan-o-grams and min/max quantities as defined by merchandising
Training to understand and analyze item forecasts sent from SSG
Acceptance of orders placed
Scheduling for vendor-to-store and DC-to-store orders
Requirements
Note on font usage in this section:  Italic font is used to indicate requirements where there is a potential gap with SAP;  and Bold font is used for known gaps.

Provide the ability to set tolerances by quantity and cost at the line item level that warns user of high/low orders. (i.e., ability to stop user from ordering 1,000,000 vs. 1,000 units).

Systematically support order creation, tracking and reporting by line item based on the following dates:
Vendor ship date (truck load date)
Due date at ship via point (mixing center or cross dock date)
In-store date (estimated arrival date at store)
Cancel date (order cancellation date)

Provide a soft warning when entering same day or past day due dates.  Vendor due dates will be handled similarly.  [No Gap]

Provide three shipping related fields at the line item level:
Source/Ship From
Multiple Ship Via (Consolidation Point, Mixing Center)
Multiple Ship To (final destinations / Stores)

Support backorder indication at the site/vendor level.  Maintain a site/vendor notification that will control back orders or cancel.  Accept or reject a short shipment based on site/vendor designation.  If short shipment is rejected, systematically backorder merchandise. Purchase order should continue to reflect actual quantity ordered, while receiving documents should reflect actual quantity received.  The system must support ASN Quantity, as well as Order Quantity and Actual Receipt Quantity.
[No Gap - as long as short shipment rejects follow a standard set of procedures implemented in SAP.]

In addition to the existing order quantity fields, provide a line item field for pack and re-pack quantities as defined by EDI standards.  [No Gap]

Support store ordering by providing the capability to turn purchase requisitions into purchase orders.  This capability will support expense orders, livestock orders and potentially pet tag/greeting card orders with the first two types managed by the store and the latter managed by the vendor. [No Gap ]

Allow for the creation of multiple purchase orders  from a date-phased allocation (i.e., multiple deliveries for a given allocation due to storage and size restrictions at receiving site.  [No Gap]

Systematically convert cubic feet for each order into number of containers and number of vendor master packs as defined in the article/vendor master.

Round orders to an even multiple of the purchasing unit of measure as defined in the item master.   [No Gap]

Round orders to the nearest pallet or master pack by total order or line item.  Allow for manual override.  [No Gap]

Support the creation, tracking and reporting of orders based on the following order status codes:
Open  - order remains flexible for updates, order has not been confirmed by source, articles remain in the sending store's on-hands.
Sent - order has been approved by source, articles are in-transit and committed to the receiving site.
Late - order has not been received based on due date assigned.
Received - order has been received at the site, articles are included in receiving site's on-hands.
Closed - complete order has been received and all articles accounted for.
Canceled - order has been deleted from the system.
Paid - invoice associated with an order has been paid.
Approved - order has been approved for delivery.

Via an external interface that periodically updates vendor pricing and available quantities, provide the capability to systematically choose the lowest cost vendor for an item ordered based on quantity availability and distribution chain.  (For example:  Fill order for green beans - Systematically choose vendor who can supply the lowest cost product and has quantity available.  Then move to next lowest cost vendor with quantity availability.  Continue until order is filled.  Choose only those vendors who regularly ship to the stores who are on this order.)
Note can  be handled via SAP Request For Quotation (RFQ) functionality.

Allow for dynamic lead time where delivery dates are based on the automatic calculation of vendor lead times and the purchase order is systematically updated by  an ASN .
Note: can do systematic updates by ASN - gap is related to lack of a dynamic lead time capability.  See Replenishment (RP) Gap Documentation.

Set-up and maintain purchase orders for selected item/vendor combinations with automatic approvals, while simultaneously setting up other item/vendor combinations with manual approvals.  At the vendor master, maintain a flag which manages whether item is approved or non-approved based on merchandise hierarchy, site and vendor.   [No Gap]

Allow for automatic update and posting to vendor once order has been approved.   [No Gap]

Support the ability to define by vendor, merchandise category and user certain rules that control what level of purchase order approval is required for an order.  These rules must be defined by user depending on that user's level of authorization.
Approval based on purchase order dollar amount (cost) limit set by user, article, vendor and merchandise category
Approval based on receipt open-to-buy limit (cost) for the scheduled receipt month set by vendor and merchandise category
Approval based on weeks of supply parameters (units) for the scheduled month set by vendor and merchandise category
If not approval is required, replenishment orders must be created and "approved."
If an approval is required, replenishment orders must be created in a "pending" status, and require an approval by user with the authorized level of approval ability.
[Gap Note - Above items not currently included in SAP Release Strategies. RS would handle only most of manual requirements.]

Allow for the mixing of  zero cost items on a  purchase order with other standard cost items.   [No Gap]

Provide the capability to create a single consolidated purchase order from an allocation. (i.e. create an allocation first, then create one PO.)  [No Gap]

Support staged deliveries for ad/event merchandise.  Create multiple purchase orders for ad/event merchandise based on due date at the store while still leveraging bracket pricing or price breaks from the vendor for those multiple purchase orders.  [No Gap]

Support special orders for customers of items which are not carried at a site.  Allow for the order to be set-up as a direct delivery to a customer and accept special margin adjustments at the line item level which differ from the regular pricing strategy.  [No Gap - Done through SAP Third Party Order process.]

Support the manual or automatic management of purchase order line item numbering for articles and structured articles.  Ability to set defaults that begin numbering scheme at any level. (i.e., 1’s, 2’s, 5’s, 10’s, etc. )
[No Gap - but not that once the user begins to renumber items manually, automatic renumbering does not happen.]

Provide the capability for Finance to manage the cost (mark-up) of an item, group of items, or total PO on an open purchase order.
[No Gap - Can change cost either via the article master or PO.]

Support the capability to line item post, as well as total PO post.  System must be able to close out a quantity received at the line item level even if all merchandise was not received or discrepancies occurred.

Support receiving documentation which clarifies for stores combined vendor DSD orders by date and site. The system must be able to combine all DSD orders by vendor, date, and site that are created through either replenishment, allocation or manually.  Stores must view combined DSD orders to appropriately receive those orders as they have been shipped.
[Cross Functional Requirement assigned to Store Systems Team.]

Support item designation by line regarding “type” of product (i.e., dry, wet, hazardous material, etc.) and systematically generate separate purchase orders based on the “type’s” handling procedures.
Note believe SAP allows use of material types for HazMats (Hazardous Materials)  - and that SAP can also generate the related special handling procedures.  Gap relates to the additional capability to identify a HazMat item and place it on a separate order for load building.

Provide the capability to structure replenishment generated purchase orders based on elements of the merchandising hierarchy(article, generic article, class, sub dept., dept., sub vendor, vendor) and organizational hierarchy(site or site group).   For example, a purchase order will be generated with the following constraints:
Vendor (A)
Department (B) - within vendor (A)
Class (C) - within department (C)
Stores 1,2,8,12,15

Provide the ability to measure the fill rate for store demand to include the ability to measure  the percentage of store demand for which the system calculates there is sufficient supply.  [Requirement relates to differences between system estimates on hands are - and the actual levels found when  physical picking is performed (i.e.  an inventory shortage is identified and the store order is shipped short).

Performance Measures
ℵℵℵℵℵℵℵℵℵℵPO header information (setup/maintenance)
PO cost (manual only)

 Timeliness:
ℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵℵ
ℵℵℵℵℵℵℵℵℵℵℵℵℵℵData integrity (setup/maintenance)

Issues

Will we use stock paper for PO’s?  Decision to use paper stock will impact how we choose to display order pack and inner pack quantities.   Resolved. Yes we will use stock paper for POs (JB).

Does deleting all the line items on a PO automatically delete the header information on that PO?  Assigned to SAP.

How does SAP support pre-paid purchase orders and purchase order deposits prior to receipt?  Assigned to SAP.

What procedures and system interfaces will be utilized between SAP and SPAN FM? (supports Real Estate, New Construction, Utilities and Facilities Management related functions) Open Issue.

How will freight costs associated with Expense ordered items be tracked?  Assigned to Susan Fickes.


Create Purchase Order (Level 3)
Requirements
Support entry, change, delete line item information or entire PO.   Support cancellation (SAP delete) and reinstatement (SAP Undelete) of purchase orders for domestic or  foreign vendors for delivery into multiple sites.  [No Gap]

Automatically generate unique purchase order numbers where:
One PO can service/support multiple locations.
Each PO has a single bill-to address.
Note:  Not a gap - assuming the single bill to address is defined  at the header level; and that each line item supports only one location and has same company code.

Permit input of manually-generated purchase orders with a check against a table of valid/available PO numbers and update any vendor contracts once order has been created.
[No Gap - assumes use of both an Internal and Externally Assigned numbering schemes:  Externally assigned numbers can not conflict with an internally generated order number.]

Provide full prompting of vendor related information at the header level for the following including:
Vendor name and address
Payment terms (dating)
Freight terms
Pick up address (leading)
Buyer Number / Name  [via Purchase Group Match Code Listing]
FOB terms
Allowances and discounts  [via Conditions screen]
Note:  Lead time can be displayed from Vendor Display Record - without interrupting PO creation process.

Provide full prompting of article-site related information at the line item level for the following:
Cost [OK ]
Allowances [GAP]
Discounts  [GAP]
UPC
Lead time
Article description   [OK]
Vendor style number  [OK]
Order units of measure  [OK]
System needs to provide full prompting of article-site related information at the line item level for ad allowances and discounts. It must also support the management of ad allowances and discounts at each line item, as well as, the for the total purchase order.
Note:  Freight, Pick Up and FOB only at header level - Gap at Line item level;  EAN/UPC appears in the Article Master and can be printed on PO.

Provide the capability to split delivery quantities for multiple distribution centers on a single purchase order, and then receive by line item while the purchase order remains open.  [No Gap]

Allow item entry by SKU and item selection by department or class.
Note:  Can do line item entry SKU, Category or Other Search;  but Search will not make multiple line item entries (i.e. all items in a Merchandise Category) - see mass maintenance gap MPO010for more details.

Via an external interface that periodically updates UPC, EAN, JAN and ISBN codes, validate appropriate code is utilized as order is created.
Note:  No Gap, but expected validation to be done during article set up - and for PO process to use only Match Code search (for the validated UPC).

Via an external interface that periodically updates currency information, support purchase order creation with a choice of currency based on average month-to-date conversion exchange rate or on a daily conversation exchange rate.
[SAP can support online currency exchange rate feed.]

Support foreign and mixed currency purchase orders.
Note:  No Gap.  SAP allows multiple currencies do be used at the item level - with an automatic system conversion to order currency set at the Header level;

Support inventory control, ticketing and pre-allocation for merchandise ordered in one country/currency and destined for multiple countries.  [No Gap]

Provide the ability to enter special commentary on the PO by header and individual line items.  Text field should included room for  “internal only” comments (i.e., customer special order), vendor comments, and warehouse receiving comments.  Utilize this text field to transmit sufficient detail to the vendor to assemble and ship the order.  [No Gap]

Provide the ability to enter multiple lines of special comments for each purchase order and transmit the order to the vendor with sufficient detail to assemble and ship the order.  Allow for the inclusion of packing instructions by line item on the purchase order.
[No Gap - accomplished via existing Header and Line Item text fields.]

Specify on the purchase order alternative methods of distributing goods including:
Direct shipment to stores (DSD)
Distribution Center
Pre-distribution (bulk flow through )
Direct shipment to consumers (special order, mail order)
Mixing Center (store-specific cross dock)

Allow automatic creation of purchase orders based on a replenishment-driven ordering system.  [No Gap]

Allow new order creation by duplication of header information or segments of line item information off an existing order currently on file regardless of PO status.   [No Gap]

Provide capability to specify required terms by header or by line item including:
Cash Discounts
PO line item discounts
PO total discounts
Ad Allowances (CoOp, Rebate)
Freight Terms
Adding Costs as % of PO (e.g. freight charges)
[Gap note: Payment terms are not supported at the line item level; and that some items (b-g) are available in Pricing.]

Allow payment terms to be specified in dates as well as by parameter driven codes for common terms.
[No Gap for payment terms by parameter codes;  Gap for payment terms in dates because there is field to directly enter date info.]

Based on potential open-to-buy requirements, including the non-mixture of OTB classes on a purchase order, provide the ability to order by multiple departments and classes, while maintaining full merchandise reporting integrity at lower levels.
[Req to be converted into a cross functional issue with Hierarchy Group - Need to work details of how this would work with OTB.]

Provide the capability to specify order quantities in either buying, stocking, or selling units of measure.   [No Gap]

Provide a conversion capability  which automatically converts from units to cost.
[No Gap - Can autoconvert from PO Units to Currency  in Retail Info System.]

Support the ability for store to initiate orders/requisitions,  SSG to consolidate  into a single order,  and then systematically allocate on the basis of the original store order documents.  [No Gap]

Provide the ability to manually or automatically estimate landed cost based on the application of various factors.
[No Gap as is defined now - additional Pricing Details will be required for implementation.]

Capture and track buyer, order originator, and subsequent activity maintainer by name or staff number.
[Note:  No Gap, captured in PO Changes Record.]

Provide for security to restrict PO creation/ maintenance/ approval (Security).
[Note: No Gap, Buyer and Transaction/Approval security much easier to implement than field level capabilities. ]

Provide the capability to suggest order splitting between DC’s based on the sum of the suggested order quantities (SOQ) for all stores within a DC’s region.

Support different costs by line item for each ship date specified on the same purchase order.

Provide color/size matrix ordering on a purchaser order. (i.e., dog collars)
[No Gap]

After purchase order creation, automatically trigger the printing of product warnings (HAZ mats), price ticketing information, and other signage/labeling.
[No Gap]

Support ordering by sets and the ability to view the master set and/or components of that set on the purchase order screen and in printed format.
[No Gap - handled as a Sub Contractor Bill Of Material item in SAP.]

Support order creation through the use of master or "dummy" purchase orders.  A "dummy" order is defined as a permanent purchase order in the system with pre-set fields that can be used repeatedly during actual purchase order creation.  The "dummy" order is maintained on file in the system, but does not affect inventories or reporting until quantities are entered and the order is approved.  This reference purchase order must support the following:
Master purchase order which defaults to certain fields
Example:  Supports new store set-up where the same SKUs are ordered from the same vendor for each new store (i.e. lacking only site number).
Supports store ordering of expense articles (i.e. lacking only quantities).
Copy function that allows for copy of master purchase order elements.
Purchase order approval ability even with zero line item quantities from a copied master purchase order.
Notes:  Once a PO is created, the status of its line items  become statistics within Retail Info System;  Because of this each model/dummy PO would adversely effect Ordering Reporting information.  Existing SAP Copy and Copy be Reference would enable the user to copy all or any selected part of an existing (real) PO.

Ability to order and track an assembler (co-packer). (i.e.  vendor who creates an item  from 2 or 3 other items)  [No Gap]

Support Vendor Managed Inventory (VMI) of specific SKUs by supporting vendor created purchase orders.  Vendors must have the capability of sending purchase order information via EDI to PETsMART where it will interface with SAP and create a purchase order.
[Note - Is possible via EDI/SAP customization. ]

Allow the use of rounding rules to achieve Bracket Pricing goals while providing the ability to override rounding at the line item level for both manual and system suggested purchase orders.
[No Gap for manually created orders.]


Expense Purchase Order Management

Provide the capability for stores to create purchase requisitions (PR) with the following information attached:
expense type
item
site
quantity
cost
cube
weight
vendor information

Support PR fields as listed above by line item and summarized by site.
[No Gap - See Report object ME5A Show All by Site, Buyer, etc.]

Allow PR to become a purchase order based upon the appropriate approval processing as defined in Purchase Order Management.
Provide the capability to set dollar amount caps based on expense type during the generation of an expense PR or PO.
[No Gap - Cap & Approve reqs by Site, Article, Buyer rules OK.]

Provide the capability for stores to create a purchase order (PO) with or without approval processing.  [No Gap]

Provide for a field on the purchase requisition and purchase order which flags the expense type including the following choices:
Standard Merchandise (sellable items)
Signage
Supplies
Maintenance
Repair
Fixture
Equipment
Promotional Item (key chains, pens, etc.)
Advertising
Service
Contracted Service (national account contract as defined by SSG)
Note that Maintenance, Service and Repair items can be managed through a Service Requisition available in SAP; and that  merchandise used for  internal consumption can also be supported. Need to look at specific procedures here - appears possible to support a lot of this functionality either though new Customized (Expense) PO or existing Service Req (& Material Types).

The system must support the automatic generation of an expense purchase order.  This functionality can be triggered by a re-occurring date either weekly, monthly or over a specified time period.  Invoice payment must be triggered by store validation of the purchase order once work has been successfully completed.

Provide a system warning based on freight exceptions when generating a purchase requisition.  Freight exceptions are defined as those orders which exceed the “freight threshold.”  The freight threshold is calculated by comparing total order cost vs. total freight delivery cost.  If the total freight delivery cost exceeds the cost of an item, the “freight threshold” has been reached and the system must provide a warning of this action to the order initiator, kick-off a report to the appropriate inventory manager, but still provide the order initiator the ability to send this order to the vendor.

Support pre-paid purchase orders and purchase order deposits.
[No Gap - also note this SAP functionality is another possible way to handle Pet Tags & Greeting Cards.]

Ability to flag an expense purchase requisition and purchase order as high, medium or low priority and systematically move high priority items through approval processing first.

The system must support assignment of expense type by line item.  This way the appropriate functional department is charged for the expense articles ordered.  Example:  Purchase order includes fixturing and signage from the same vendor.  Fixturing will charge Real Estate's general ledger account, while signage will charge Advertising's general ledger account.

Support the daily generation of an Expense PO/PR Summary Report detailing:
POs created automatically by the system (example: national contracts)
PO/PRs pending approval (example: maintenance)
PO/PRs rejected (example: equipment)
PO/PRs approved (example: supplies)
PO/PR substitutions (example: supplies)
Late shipments/services based on due dates
Shipments over/under order quantity based on receipts
Weekly receipt projection based on PO receipt dates


Livestock Purchase Order Management

Support systematic store delivery of item forecasts, min/max reports, and availability reports for store ordering.  Item forecasts and min/max reports leverage pre-defined parameters.  Availability reports are managed by buyers and e-mailed periodically to the stores.
Example:  Store 146 carries angel and gold fish.  Livestock buyer sends store 146 min and max quantities for angel and gold fish.  Livestock buyer also sends store 146 article forecasts for angel and gold fish.  Finally, livestock buyer sends store 146 its assortment availability.  All of these tools are provided to store 146 in order to manage the store's livestock ordering process.

Support systematic store delivery of handling instructions that list conditions for special goods (i.e., for livestock or perishables).  The system must have the ability to interface with a word processing program and image database.  The system must then send these completed care sheets with image to the stores.

Support the ability to forecast articles at the distribution center based on historical store demand (articles requested, not filled) adjusted for events.
Example:  forecast angel fish based on store sales outside of promotional events.

Provide the capability of generating exception reports that track DC overstocks.  Utilize this report to trigger allocations against store orders.  These allocations must be based on a the total quantity ordered by all stores and distributed by an stores percent to total.
Example:  Stores 146, 147 and 148 each order 100 angel fish.  Distribution center 012 only has 280 angel fish available.  Because of the shortage of angel fish at the DC, system creates an allocation for 70 angel fish to each store.

Provide a system warning based on freight exceptions when generating a purchase requisition.  Freight exceptions are defined as those orders which exceed the "freight threshold."  The freight threshold is calculated by comparing total order cost vs. total freight delivery cost.  If the total freight delivery cost exceeds the cost of an item, the "freight threshold" has been reached and the system must provide a warning of this action to the order initiator, kick-off a report to the appropriate inventory manager, but still provide field the order initiator the ability to send this order to the vendor.
The system must provide a field that holds vendor/site freight information  (basic freight requirements) for store ordering purposes.


Import Purchase Order Management

Interface with and support letter of credit creation, tracking, and maintenance functions.
Accommodate the linking of the Letter of Credit to the purchase order once an import order has been created.

 Jobs Analysis
See process maps for job delegation.
Reports

Reports Added

Expense Purchase Order/Purchase Requisition Summary Report - Summarizes by type all expense orders or requisitions that were placed over a certain time period, their approval status, their order status, and any substitutions that were made to the order.

Livestock Forecast/Plan-o-gram Report - Details by store the item forecasts and min/max presentation requirements for livestock items in a store’s assortment.

Livestock Availability Report - Details all livestock items available for sale now and in the future.  This report is periodically updated depending on vendor, DC and SSG feedback.

Livestock Allocation Exception Report - Details store re-allocations which DC was forced to make in order to manage over or understock conditions.

Livestock Freight Exception Report - Details freight costs associated with livestock orders.

Store Feedback Report - Details store feedback regarding item quantities, end-cap display parameters, and any other assortment management input.

Livestock Min/Max Exception Report - Details those orders which were above or below the tolerance set for a livestock item.  Generated for Livestock Buyer and Market Manager review.

Fish DC Pricing Report:  Details line item fill rate by site serviced; Summary fill rate by SKU; and summary fill rate (by site serviced) summarized  to reflect all sites  for one week.

Communicate PO to Vendor / Stores (Level 3)
Requirements
Support the transmission of a single purchase order to a partner via EDI, fax or email.  Allow communication of a single PO to multiple partners.  Partners receiving purchase orders can include:
Store
Vendor
Consolidator
Importer
Shipping Line
Mixing Center
Broker
Daymon
Any combination of the above
[No Gap but each PO recipient must be defined as a partner organizational structure in the system.]

Provide the capability of sending replenishment or buyer-generated orders to the vendor immediately.  [No Gap]

Provide the ability to enter multiple lines of special comments for each PO (i.e., customer special order merchandise) and transmit the order to the vendor/ partner with sufficient detail to assemble and ship the order.  [No Gap]

Ability to trigger an open order release based on vendor order due dates.  Establish due dates for stores, districts, or regions for each vendor and then automatically release approved orders by the specified vendor due date.
[Note requirement - why hold created orders?  As written, requirement will have accuracy impacts for RIS ]


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
