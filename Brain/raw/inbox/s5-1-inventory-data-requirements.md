---
date: 2026-04-23
type: raw
source: Brain/raw/inbox/S5.1 Inventory Data Requirements.docx
tags: [secure]
project: secure
status: unprocessed
---

# S5.1 Inventory Data Requirements

## Source

File: `Brain/raw/inbox/S5.1 Inventory Data Requirements.docx`
Size: 438,031 bytes
Extracted via: markitdown

## Extracted content

![](data:image/png;base64...)

Inventory Data Requirements

Secure Data Requirements document.

## Document Versions

|  |  |  |
| --- | --- | --- |
| **Version** | **Author** | **Description** |
| **Initial** | **Richard Williams** |  |
|  |  |  |

## Reviewed.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Role** | **Name** | **Title** | **Signature** | **Date** |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

# Content

[Content 3](#_Toc462913048)

[Introduction 4](#_Toc462913049)

[Design 5](#_Toc462913050)

[Requirements 7](#_Toc462913051)

[Conceptual Data Model 9](#_Toc462913052)

[Exceptions 11](#_Toc462913053)

[Shrink Exceptions 11](#_Toc462913054)

[Stock Availability Exceptions 14](#_Toc462913055)

[DC or Warehouse Exceptions 17](#_Toc462913056)

[Data Integration 19](#_Toc462913057)

[Detail Data Definitions 20](#_Toc462913058)

[Location Hierarchy 20](#_Toc462913059)

[Transactional Data 24](#_Toc462913060)

# Introduction

This document describes the key data components needed to benefit from Secure Inventory application. Appriss Retail understands due to the source of the data being across a variety of operational systems, obtaining these elements can be challenging and consequently have set what elements are needed for each possible exception.

### Audience

-Though Asset protection / Loss Prevention -may be the primary user of the Secure Application, taking action on inventory based exceptions will require the assistance of retail operations. Therefore, due to the cross functional nature of the applications output and the systems involved; Sysrepublic suggests this document be read by the following roles within -the organization.

* Enterprise Architects with a deep knowledge on how the different Enterprise applications are integrated.
* Senior Business Analysts familiar with Inventory management business process and systems

# Design

A critical piece to the Secure Inventory data model is establishing the relationship between the merchandise hierarchy used for displaying and tracking performance of products and the ordering scheme for products at unit level.

The merchandise hierarchy creates the reporting structure under which sales and inventories of products are tracked and managed. The number of levels within the hierarchy will differ from organization to organization. The diagram below shows how the Secure Foundational data model is designed manage the traditional hierarchy as well as define organizational alignments and establish the relationship of the way items are sold to the way they are purchased and delivered to store. The Secure Inventory module relies on being able to rationalize all item movement within a retail organization down to the individual sellable unit regardless of the quantity or pack configuration it moves within the supply chain.

![](data:image/x-emf;base64...)

Figure

The design allows for

* Six levels in the Merchandise Hierarchy
* The grouping of sellable product items to n levels down to the barcode.
* The grouping of Orderable items that breakout to sellable items.
* Supply Chain and Merchandising Organizational Alignment to Item Setup.
* Supplier Alignment to Orderable Items through demand groups.

Taking a typical retail scenario the conceptual model can be used in the following way

![](data:image/x-emf;base64...)

Figure Example Item Setup

Requirements.

At a high level the following section covers fundamental data concepts that require analysis and understanding by Sysrepublic or Business Analyst team.

### Active Items

A key challenge in implementing the inventory module is keeping the amount of data retained to a minimum. However many organization don’t remove obsolete item data from their systems or have very relaxed maintenance routines, resulting in a high percentage of unwanted data.

To assist with this prerequisite Sysrepublic requires information to be delivered that can be used to ascertain when items become first active in a location and when to cease tracking the movement. Typically this information would be provided with the range.

### Item Relationship

A key component in tracking inventory movement is to understand at which level in the item mastering do transactions occur. Figure 3 is a continuation of Figure 2, to show when Ordering is done within the organization using packs, but pricing of items is done at SKU. This means a relationship must be established between pack and SKU.

![](data:image/x-emf;base64...)

Figure

### Date and Time on Item Movement

Time is an important data point as it will present the sequence of inventory movement, actions, and events.

### Reason Codes

Sysrepublic would need to understand the various reason code types that may be in use within the organization. Typically reason codes are found on adjustments, but can also be seen on other movement activities; example code types can exist for undelivered items on the receiving.

The mapping between the code and fiscal accounting is the vital piece of data Sysrepublic would need to understand.

Table Adjustment Reason Example

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Reason Code | Reason Code Group | Description | Family Grouping | Accounting Cost Codes |
| 001 | 1 | Defective Item | Recall |  |
| 002 | 1 | Vendor Recall | Recall |  |
| 001 | 2 | CONCEALED DAMAGE | Damage |  |
| 002 | 2 | Customer Damage | Damage |  |
| Etc… | | | | |

### Cost based items

These are delivered items to store that are not intended for sale independently or are broken-out to make sellable items. Sysrepublic would need to understand how the “make to sell” items are initially pulled out of the inventory and accounted for.

Sysrepublic would need to understand how yield reconciliations are done on these items.

### Consignment Items / Sell by Trade

The responsibility of Sell By Trade (SBT) items falls on the vendor until they are sold. Sysrepublic typically finds that these items bypass some organizational processes that could make report values incorrectly calculated. Due to these issues, Sysrepublic would therefore ignore these items.

### Associates

Understanding the employee and/or vendor representative that performs item activity movement is an important factor for identifying who’s performing incorrect business processes or potentially defrauding the organization.

Sysrepublic understands many of the devices used in tracking inventory movement may have a general login, which essentially anonymizes the activity. If the intention is to track this activity within the back and center of stores, Sysrepublic recommends addressing this issue.

### Units

In the Detail Data Definitions section unit quantity will be dependent on the items unit of measure. Sysrepublic expects the UOM to be set at a global level, if this changes from location to location then it can be moved to the range definition as needed.

### Value

Value in the detail data definition is concerned with the monetary value of the product, and it’s the Werth. Depending on the accounting method used this value is usually be the item cost or the retail price.

If the value can’t be delivered in conjunction with Unit in all circumstance and therefore it must be calculated. Sysrepublic would expect unit value to be supplied in a reference feed, with an appropriate applicable period supplied.

Table Data Entity Requirements

|  |  |
| --- | --- |
| Data Entity | Key Data Points |
| Location Hierarchy Information | Store No, Address, Regional and District rollup of location responsibility, Warehouse information etc |
| Product Hierarchy | UPC / EAN, SKU, Style, Product Hierarchy, Buyers and Supply Chain Analyst associated or responsible for item |
| Range Information | Location, Sellable Product Information (SKU), Expected Location Sell through, Shelf size, Planogram Information, Security of Product. |
| Orderable Product Hierarchy | Packs or Cases, Demand Group Relationships to Supplier, Outer case codes |
| Product Breakout | Pack to SKU relationship, Case Unit Breakout, Begin and End Period of Case Size |
| Supplier | Supplier or Vendor Reference Information |
| Purchase Orders | Packs or Cases Orders, Supplier, Quantity, Costs, Shipment Costs, Manual or Automated Order. |
| DC Shipment and Transfer | ?? DC Shipment: Location being shipped to, date of shipment, shipment origin, shipment value, shipment status. What type of transfers are we referring to here? Inter store transfers? |
| Inventory Adjustments | Sellable Product Information, Location, Quantity Adjusted +/-, Adjustment Reason Codes, Associate who performed Adjustment, date/time of adjustments, on hand prior to the adjustment |
| Sales | Data from Point Of Sale |
| Store Inventory | Location, Sellable Product Information, Quantity On Hand at Location, last movement date, item status |
| Code Or Shelf Life |  |
| Promotions Reduction Information | Reference Information |
| Receiving records? | Where are we capturing the details of any receiving records - is this just being passed through as an adjustment type? |

## Conceptual Data Model

![](data:image/x-emf;base64...)

Figure

Sysrepublic understand item movement can be represented in many different ways within an organization. The Inventory data model and secure application is designed to provide flexibility in capturing the movement transaction. As an example, Receiving items into location, this can be represented an inventory adjustment with a receiving adjustment type or it can be captured in a Good Received Note message, sent to the invoicing system.

# Exceptions

The following tables show the data dependency that are set of need identify the following process exceptions. These exceptions are broken into three main categories; Shrink, Availability and DC and Warehouse.

## Shrink Exceptions

|  |  |
| --- | --- |
| **Exception** | **Components Required** |
| **Item on hand in store  but not sold at till / no inventory adjustment** | Location , Item , Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info,  Store Inventory |
| **Negative on hand - Item sold but never ordered / delivered** | Location , Item , Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info |
| **Item wasted immediately after delivery** | Location , Item , Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info,  Store Inventory |
| **Item wasted without sales or little sales – high ratio of delivered units to waste units** | Location , Item , Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info,  Store Inventory |
| **Item not selling but being delivered** | Location , Item , Purchase Order , DC Shipment And Transfer ,  Inventory Adjustments, Sales Information, Store Range Info, Store Inventory |
| **Item reported shrink in multiples or near multiples of Case size ( Case used as item instead of SKU )** | Location , Item , Orderable Items, Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info,  Store Inventory |
| **Item sales higher than ordered or delivered quantity in a set period of time** | Location , Item , Orderable Items, Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info,  Store Inventory |
| **Item-Case information is setup wrong to be ordered less but received more** | Location , Orderable Items, Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info,  Store Inventory |
| **Item wastage significantly higher than average rolling wastage** | Location , Sellable Item , Orderable Items, Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info,  Store Inventory |
| **Higher out of code wastage on a given category – supplier issue** | Location , Sellable Item , Orderable Items, Purchase Order , DC Shipment and Transfer ,  Inventory Adjustments, Sales Information, Store Range Info, , Hierarchy ,  Store Inventory |
| **Item sell through before the next scheduled delivery** | Location details, Sellable Item details ,purchase order details, DC Shipment and Transfer details,  inventory adjustments, sales information, store range info,  store inventory details, delivery information |
| **Item in stock and never received by the store** | Location details, Sellable Item details ,purchase order details, DC Shipment and Transfer details,  inventory adjustments, sales information, store range info,  store inventory details, ordering details, delivery information |
| **2 or more counts or inventory adjustments on the same day** | Location details, Sellable Item details ,purchase order details, DC Shipment and Transfer details,  inventory adjustments, sales information, store range info,  current inventory |
| **2 or more inventory adjustments between deliveries for high valued items** | Location details, Sellable Item details ,purchase order details, DC Shipment and Transfer details,  inventory adjustments, sales information, store range info,  store inventory details, ordering details, delivery information |
| Credit to Debit unit ratio is higher than expected for a particular item vendor combination | Location details, Sellable Item details, Vendor details, Receiving Details, Invoice Details |
| Credit to Debit value ratio is higher than expected for a particular item vendor combination |  |
| On hand availability is high and sales rate drops | Location details, Sellable Item details, Vendor details, Receiving Details, Invoice Details, Sales |
| On hand drops to zero sales lower than expected |  |
| Item on hand but no sales |  |

## Stock Availability Exceptions

|  |  |  |  |
| --- | --- | --- | --- |
| **Exception** | **Components required** |  |  |
|  |  | 1 | Out of stock reporting |
|  |  | 1 |  |
|  |  | 1 |  |
|  |  | 1 |  |

## Direct Store Delivery (DSD) Exceptions

|  |  |  |  |
| --- | --- | --- | --- |
| **Exception** | **Components required** |  |  |
|  |  | 1 |  |
|  |  | 1 |  |
|  |  | 1 | Implies a vendor did not credit or did not deliver an item |
|  |  | 1 | Implies vendor forecasting is not accurate, not delivering enough product to meet demand |
|  |  | 1 | Implies vendor delivering product not on file, or item selling under a generic sku |
|  |  |  |  |

# Data Integration

Two methods of Integration are available to provide data to the Secure Inventory module: either batch or real-time.

Typically a batch involves extract from the companies’ data warehouse, which is used for all management reporting. If desired Sysrepublic can provide an integration proxy service (using our own integration tool - RTI) to subscribe to Enterprise systems that master the different data points involved in inventory management.

![](data:image/x-emf;base64...)

Figure Integration Collection Bus

# Detail Data Definitions

The following covers field definitions Sysrepublic expects to see in the Inventory movement data feeds. They are not set in stone but more as a guide to primary fields needed.

The section is broken up into two sections reference and transactions. Reference covers item and location setups. Transactions covers the movement of items.

Note an assumption is made that sales will come in from POS integration.

## Reference

### Location Hierarchy

Table 3- Location Hierarchy

|  |  |  |
| --- | --- | --- |
| Field Name | Data Type |  |
| LocationId | Numeric | Location Identification, example Store or Warehouse |
| Hierarchy1 | String | Top level of the hierarchy. Example District Code |
| Hierarchy1Description | String | Top level of the hierarchy description. Example District Name |
| Hierarchy2 | String | Next Level down. Example Region Code |
| Hierarchy2Description | String | Next Level down. Example Region Name |
| Hierarchy3 | String | Keep filling in until all levels of location hierarchy applicable are filled in. Leave Blank if n/a. |
| Hierarchy3Description | String |
| Hierarchy4 | String |
| Hierarchy4Description | String |
| Hierarchy5 | String |
| Hierarchy5Description | String |
| Hierarchy6 | String |
| Hierarchy6Description | String |
| Name | String | Name of the Location |
| LocationType | String | Store or Warehouse |
| Pricing Location | Numeric | The store used in zone pricing |
| Brand | String | Store Brand |
| StoreIdentifier | String |  |
| PhoneNo | String | Main Phone No for the Location |
| FaxNo | String |  |
| EmailAddress | String | Email address for the locations manager. |
| AddressLine1 | String | Address Lines |
| AddressLine2 | String |
| AddressLine3 | String |
| AddressLine4 | String |
| PostalCode | String | Post Code or Zip Code |
| Country | String | Country Location. Use ISO 3166-1 alpha-3 |
| Currency | String | ISO 4217 |

### Product

Table 4 Product Hierarchy

|  |  |  |
| --- | --- | --- |
| FieldName | DataType | Description / Example |
| ItemID | String | Item ID (e.g. UPC / EAN) – Primary Key |
| Hierarchy1 | String | Top level of the hierarchy. Example from Figure 3 Division Code |
| Hierarchy1Description | String | Top level of the hierarchy. Example from Figure 3 Division Name |
| Hierarchy2 | String | Next Level down. Example from Figure 3 Department Code |
| Hierarchy2Description | String | Next Level down. Example from Figure 3 Department Name |
| Hierarchy3 | String | Next Level down. Example from Figure 3 Section Code |
| Hierarchy3Description | String | Next Level down. Example from Figure 3 Section Name |
| Hierarchy4 | String | Next Level down. Example from Figure 3 Class Code |
| Hierarchy4Description | String | Next Level down. Example from Figure 3 Class Name |
| Hierarchy5 | String | Next Level down. Example from Figure 3 Sub Class Code |
| Hierarchy5Description | String | Next Level down. Example from Figure 3 Sub Class Name |
| Hierarchy6 | String | Next Level down. Blank based Example from Figure 3 |
| Hierarchy6Description | String | Next Level down. Blank based Example from Figure 3 |
| ItemName | String | e.g.“BIC Lighter” |
| ItemDescription | String | e.g. “Blue BIC lighter 5 ml” |
| ItemReceiptDescription | String | e.g. “BIC LTR” |
| ItemStatus | String | e.g. “1” = Active, “2” = inactive |
| AlternateSKU | String | Leave Null if N/A |
| UOM | Numeric | An Enumeration of Units of Measure. 1 = Each, 2=LB etc |

### Pack

Table 5 Orderable Hierarchy

|  |  |  |
| --- | --- | --- |
| FieldName | DataType | Description / Example |
| ItemID | String | Pack ID |
| Hierarchy1 | String | Top level of the hierarchy. Example from Figure 3 Division Code |
| Hierarchy1Description | String | Top level of the hierarchy. Example from Figure 3 Division Name |
| Hierarchy2 | String | Next Level down. Example from Figure 3 Department Code |
| Hierarchy2Description | String | Next Level down. Example from Figure 3 Department Name |
| Hierarchy3 | String | Next Level down. Example from Figure 3 Section Code |
| Hierarchy3Description | String | Next Level down. Example from Figure 3 Section Name |
| Hierarchy4 | String | Next Level down. Example from Figure 3 Class Code |
| Hierarchy4Description | String | Next Level down. Example from Figure 3 Class Name |
| Hierarchy5 | String | Next Level down. Example from Figure 3 Sub Class Code |
| Hierarchy5Description | String | Next Level down. Example from Figure 3 Sub Class Name |
| Hierarchy6 | String | Next Level down. Blank based Example from Figure 3 |
| Hierarchy6Description | String | Next Level down. Blank based Example from Figure 3 |
| Pack Description |  | Pack Description |
| Status |  | e.g. “1” = Active, “2” = inactive |
| UOM |  | An Enumeration of Units of Measure. 1 = Each, 2=LB etc |
| Pack Type |  | Complex Simple |

### Pack Supplier

Table 6 Vendor Orderable Item

|  |  |  |
| --- | --- | --- |
| FieldName | DataType | Description / Example |
| PackID | String | Pack ID |
| Vendor Id |  |  |
| Primary Supplier | Boolean | Indicator to show this Vendor is the Primary Supplier for this pack |
| Vendor Swell Amount | DECIMAL(9,5) | The amount of swell cost attributed to the vendor. |
| Vendor Product Id | String | If the Vendor has unique deification number for the product |
|  |  |  |

### Pack Breakout

Table 7 - Breakout

|  |  |  |
| --- | --- | --- |
| FieldName | DataType | Description / Example |
| PackID | String | Pack ID |
| Sellable Item Id |  |  |
|  |  |  |
| Pack Size | Numeric | Indicator to show this Vendor is the Primary Supplier for this pack |
| Pack Valid Start Date |  |  |
| Pack Valid End Date | String | If the Vendor has unique deification number for the product |

### Range

Table 8 - Range

|  |  |  |  |
| --- | --- | --- | --- |
| name | name | max\_length | Descrption |
| LocationId | Numeric | 4 | Location of Item, example Store or Warehouse |
| Sellable Item | String | 8000 |  |
| OrderableItem | String | 8000 |  |
| MerchandisingStartDate | datetime | 8 | When the Item will become authorized in the location |
| MerchandisingEndDateTime | datetime | 8 | When the Item will become deactivated in the location |
| OrderStartDateTime | datetime | 8 | When the Item becomes orderable for the given location; usually x number of days before the MerchandisingStartDate |
| OrderEndDateTime | datetime | 8 | When does the item become un-orderable for the location |
| ShelfCapacity | Numeric | 4 | The maximum number units available at the location |
| MinimumOrderQuantity | Numeric | 4 | Number of Units before the Item is auto ordered. |
| MasterProductID | String | 8000 |  |
| IsSBT |  |  | Is the Item in this Location and Sell By Trade or consignment based item |

### Vendor

Table 9 - Vendor

|  |  |  |  |
| --- | --- | --- | --- |
| name | name | max\_length | Description |
| VendorNumber | String | 8000 | Vendor Id number |
| ParentVendorNumber | String | 8000 | If the Vendor is subsidiary business then link to another vendor |
| VendorName | String | 8000 | The Name of the Vendor |
| DeliveryType | Numeric | 2 | Delivery |
| AccountPayableNumber | String | 8000 | The Finance Account Payable Number |
| DUNSNumber | String | 8000 | Dun & Bradstreet Number |
| InvoiceOriginCode | String | 8000 |  |
| OrderOriginCode | String | 8000 |  |
| OrderSendCode | String | 8000 |  |
| DeliveryTerms | String | 8000 | Vendor Credit Terms |
| PaymentMethodTerms | Numeric | 2 |  |
| DistributionCenterId | Numeric | 2 | The Primary DC the Vendor Delivers too. Leave Blank for DSD |
| AddressType | Numeric | 1 | Billing Address, Warehouse Address etc. |
| Address1 | String | 8000 | Address Lines |
| Address2 | String | 8000 |
| Address3 | String | 8000 |
| Address4 | String | 8000 |
| PostalCode | String | 8000 | Post Code or Zip Code |
| Country | String | 8000 | Country Location. Use ISO 3166-1 alpha-3 |
| FaxNumber | String | 8000 |  |

## Transactional Data

### Adjustments

The adjustments entity is used to capture movement data where the transactional message could not be captured. It is also used to capture miscellaneous movement.

Units in this data would normally be represented as a delta into the on hand figure.

Table 10 - Adjustments

|  |  |  |  |
| --- | --- | --- | --- |
| Name | name | max\_length | Description |
| Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Sellable Item | String | 8000 |  |
| Day | datetime | 8 | The Business day the adjustment occurred |
| SeqNo | Numeric | 8 | If Time is not available or two adjustments occurred at the same time, sequence is used represent the order the activity occurred in |
| AdjustmentType | Numeric | 4 | The Type of Adjustment occurred. |
| AdjustmentDateTime | datetime | 8 | The Day and Time of the adjustment |
| OrderableItem | String | 8000 |  |
| UPCID | String | 8000 | The Bar code used during the adjustment operation |
| ReasonGroupCode | Numeric | 4 | The Family Group the reason code is associated with. |
| InitialReasonCode | Numeric | 4 | The initial reason code that was given to the adjustment |
| ReasonCode | Numeric | 4 | Final or last reason code given to the adjustment |
| ReasonDescription | String | 8000 | Any additional Comments Associated to the Reason Code |
| VendorID | String | 8000 | If item is being adjusted back to the vendor, the Vendor Id associated with the Item |
| VendorItem | String | 8000 | If the Vendor has its own hierarchy and item numbers, then the vendors item number |
| Units | decimal | 17 | The unit change (as a delta) in the inventory. Example -2 for reduce the on hand by 2) |
| Amount | money | 8 | The retail change as a value (as a delta) in the inventory. |
| Cost | money | 8 | The cost associated with the change (as a delta) in the inventory. |
| AuthorizedFlag | bit | 1 | Was the adjustment made against an authorized item |
| Comments | String | 8000 | Any Comments associated with the adjustment |
| LinkReferenceNo | Numeric | 8 | An internal Reference Associated with the adjustment. Normally a Transaction number from the adjustment gun |
| ExternalReferenceID | String | 8000 | If the ad  justment is linked to a vendor. The number given to the vendor |
| AdjustmentDateCreated | datetime | 8 | The system date the adjustment was first recorded or created |
| AdjustmentDateModified | datetime | 8 | The system date and time the adjustment was changed |
| AssociateCreated | String | 8000 | The Initial User that performed the adjustment |
| AssociateModified | String | 8000 | The Initial User that performed the adjustment |

### Counts

Contains information regarding a cycle count or stack taken made for the item.

Table 11 – Counts

|  |  |  |  |
| --- | --- | --- | --- |
| Name | Data Type | Size | Description |
| Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Sellable Item | String | 8000 |  |
| Orderable Item | String | 8000 |  |
| Count Type | Numeric | 4 | Cycle Count, Stock Counts etc |
| Day | datetime | 8 | The Business day the Count occurred |
| SequenceNo | Numeric | 4 | If the item is count in multiple places within the location, then please provide a record sequence number |
| UnitCount | decimal | 17 | An Absolute figure the units counted |
| CountRetail | money | 8 | An Absolute figure of total retail amount for the quantity found at the location |
| CountCost | money |  | An Absolute figure of total cost amount for the quantity found at the location |
| PlanogramCode or Space plan code | Numeric | 2 | A planogram code for where in the loca |
| Associate | String | 8000 | The User or Associate Information of who counted the items |
| SourceOfCount | Numeric | 2 | How did the count occur? |
| CreationDate | datetime | 8 | The system date the adjustment was first recorded or created |
| IsUpdate | Bit |  | Is the record an amendament to previously posted count |

### Invoice

Table 12 - Invoice

|  |  |  |  |
| --- | --- | --- | --- |
| LocationId | SMALLNUMERIC | 1 | Unique identification number of a Winn-Dixie Store. |
| Vendor Id | NUMERICEGER | 3 | The Vendor ID Number |
| Invoice Number | Numeric | 4 | Invoice Number |
| Orderable Item | Numeric | 5 | Pack Id. |
| Delivery Date | Date | 7 | Used for history tracking--The date upon which a vendor record became effective. |
|  |  |  |  |
| Invoice Source | Numeric | 9 | Defines the type of host system that the invoice came from (Manual, self-bill, Invoice Matching etc) |
| Order Item UOM |  |  | The Unit of Measure of the Item. Example Weight or Each etc |
| Pack or Case Type | String | 8000 | Each, Pack / Case or Pallet |
| Pack Size | decimal | 17 | The Size of cases |
| Shipped Quantity | Numeric | 12 | The number of ordered items. This is used to check the difference between ordered and shipped. Average weight of the product(s) shipped |
| Cost Amount | DECIMAL | 16 | The cost associated with either a unit or a package of a particular item. |
| Unit Retail Price | DECIMAL | 22 | Unit retail price of the item. Note: in deal cases this must be used in conjunction with the Shipped Unit Retail multiple. In cases where the price is 2/1.09 or 3/1.00. The unit price would be 1.09 and 1.00 with a multiple of 2 and 3 respectively. |
| Retail multiplie | Numeric | 23 | Retail multiplier associated with the item. |
| FinalShippingCost | DECIMAL(9,2) | 25 | The final cost associated with shipping products to the store, taking Numerico account adjustments. |
| WarehouseCost | DECIMAL(9,2) | 26 | Total warehousing costs related to this shipment. |
| RetailCostAmount | DECIMAL(9,2) | 27 | The retail cost amount of the specific product. |
| Original Order Unit Quantity | Numeric | 32 | The number of items that was on the invoice for the original order. |
| Net Item Cost for DSD | DECIMAL(10,4) | 36 | Item net cost for DSD items |
| Invoice Has Changed Flag | String | 38 | Invoice cost change flag |
| Item Dispute Flag | String | 39 | Invoice difference flag |
| Billing Dept id | Numeric | 47 | Department used by billing system for invoice prNumeric. |
|  |  |  |  |

### Orders

Contains information about orders raised against a given item.

Table 13 - orders

|  |  |  |  |
| --- | --- | --- | --- |
| Name | Data Type | Size | Description |
| Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Orderable Item | String | 8000 | The Item used to order |
| Day | Datetime | 8 |  |
| OrderNo | Numeric | 8 | PO Order number |
| SeqNo or Line Number | Numeric | 4 |  |
| Status | Numeric | 4 | Order Status |
| Order Unit Quantity | Decimal | 17 | The amount ordered |
| Order Value Quantity | Decimal | 17 | Value of ordered. |
| Order Item UOM |  |  | The Unit of Measure of the Item. Example Weight or Each etc |
| Pack or Case Type | String | 8000 | Each, Pack / Case or Pallet |
| Pack Size | Decimal | 17 | The Size of cases |
| Associate Raised Order |  |  | If a manual order, the associate who raised the order |
| System Raised Order |  |  | Order was auto generated by OMS |
| Order Type Code |  |  | Code for the type of order. Example Regular Order, Promotion Allocation etc |
| VendorItem | String | 8000 |  |
| DealAppliedCode | String | 8000 | Is there Vendor Deal applied to order. |
| Is Change |  |  |  |

### Stock Ledger / Daily On Hand

Stock Ledger should contain end of day on hand figures for the given location.

Table 14 - On hand Ledger

|  |  |  |  |
| --- | --- | --- | --- |
| Name | Data Type | Length | Description |
| Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Item | String | 8000 |  |
| Day | Datetime | 8 |  |
| OrderableItem | String | 8000 |  |
| UOM | Numeric | 4 | Item UOM |
| Stock On Hand in Units | decimal | 17 | The Quantity On hand By Unit |
| Stock On Hand By Value | money | 8 | The Quantity On hand By Value |
| Change | bit | 1 | Indicates if this an updated record to ledger entires previously provided. |

### Receiving

Table 15 – Receiving

The receiving entity is designed to capture good received notification or notes message from store system to the invoice matching system.

|  |  |  |  |
| --- | --- | --- | --- |
| Name | Data Type |  |  |
| Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Sellable Item | String | 8000 |  |
| Orderable Item | String | 8000 |  |
| Day | datetime | 8 | The Business day the Count occurred |
| SequenceNo | Numeric | 4 | If the item is count in multiple places within the location, then please provide a record sequence number |
| ReceiveDateTime | datetime | 8 | Date and Time Item was received |
| ReceivingType | Numeric | 1 | DSD or DC Items received |
| OrderNo | Numeric | 8 | PO Order |
| Status | Numeric | 4 | Status Of the receiving |
| UPCID | String | 8000 |  |
| DCNo | Numeric | 1 |  |
| Vendor ID | String | 8000 | Vendor |
| VendorItem | String | 8000 |  |
| OutOfStockReason | Numeric | 1 | Reason Code for why the items weren’t delivered |
| ReceivedQty | decimal | 17 | Quantity Received |
| OrderedQty | decimal | 17 | The Quantity ordered in units |
| BackorderedQty | decimal | 17 | The Quantity not delivered in units |
| PackQty | Numeric | 4 | Pack Size |
| UnitType | Numeric | 1 |  |
| OrderType | Numeric | 1 |  |
| PackUOM | String | 8000 |  |
| ExternalRefID | String | 8000 |  |
| ReceivingAssociate | String | 8000 |  |
| AssociateModified | String | 8000 |  |
| Substitution Reason Code | CHAR(1) | 31 | Code indicating the reason one item was substituted on an order for another item. |
| New Orderable Item | NUMERICEGER | 30 | The inventory product identifier (new Orderable code) that was on the original order. |

### Shipments

Table 16 – Shipments

Shipment captures Bill of Leiden or Advanced Shipment Notification messages from DC to Stores

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Name | Data Type | | Length | | Description | |
| Source Location | Numeric | | 4 | | Usually Warehouse Number | |
| Destination Location | Numeric | | 4 | | Usually Store No | |
| Sellable Item | String | | 8000 | |  | |
| Orderable Item |  | |  | |  | |
| Day | datetime | | 8 | | Business Day of Shipment | |
| ShipDateTime | datetime | | 8 | | The Date and Time the Shipment left e soucrce location | |
| Estimated Delivery DateTime | datetime | | 8 | | The Date and Time the Shipment is due to arrive at the destimation location | |
| OrderNo | bigNumeric | | 8 | | The Original Order No | |
| SeqNo or Line Number | Numeric | | 4 | |  | |
| Shipment Unit Quantity | decimal | | 17 | | The Quantity of Items in the Shipment | |
| Shipment Value |  | |  | | The Retail Value of the Shipment based on the quantity | |
| Supplemental Shipment Costs |  | |  | | Transportation Costs | |
| SourceDocNo | String | | 8000 | |  | |
| CaseID | String | | 8000 | |  | |
| VendorItem | String | | 8000 | | If the vendor has separate item identifier | |
| UPCID or OCC | String | | 8000 | | The Bar Code on the side of the packages | |
| Status | String | | 8000 | | Shipment Status, i.e transit, delivered, cancelled, undelivered etc | |
| Delivery Driver Name or Associate Id |  | |  | | Name of the person delivering the item. | |
| Is Change Record | bit | |  | |  | |
| User\_view.Invc\_Dtl.Shp\_Mod\_Cd | | CHAR(1) | | 28 | | Shipping UOM Code describes how a product is typically shipped, whether by Weight (W) or by Quantity (Q). | |
|  |  | |  | |  | |
| LastUpdated | datetime | | 8 | |  | |

### Transfers

Table 17 – Transfers

Transfers are used to capture inter store transfer notifications or item movement within store based on planogram changes.

|  |  |  |  |
| --- | --- | --- | --- |
| Name | Data Type | Length | Description |
| Source Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Target Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Sellable Item | String | 8000 |  |
| Orderable Item | String | 8000 |  |
| Day | datetime | 8 | Trading Day of when the Transfer Started |
| TransferNo | bigNumeric | 8 | Transfer Allocated Number |
| Reason Code |  |  | Reason for transfer |
| SeqNo | Numeric | 4 | Sequence No of Item in the Transfer |
| Status | Numeric | 4 | Status of Transfer |
| Transfer Requested Unit Quantity | numeric | 17 | The amount requested |
| Shipped Unit Quantity | numeric | 17 | The number of units shipped out of location |
| Shipped Value Quantity |  |  | The value of the shipped |
| Date Time Shipped |  |  | Date and Time the items were shipped |
| Associate Packaged and Shipped Item |  |  | The Associate who is delivering or packaged the shipment. |
| Received Unit Quantity | numeric | 17 | The number of units received in at target location |
| Received Value Quantity |  |  | The value of the received |
| Date Time Received |  |  | Date and Time the items were received |
| Associate Received Item | Numeric | 4 | The Associate who received the shipment. |

### Shrink

Table 18 - Shrink

|  |  |  |  |
| --- | --- | --- | --- |
| Name | Numeric | 4 |  |
| Location | Numeric | 4 | Location of Item, example Store or Warehouse |
| Sellable Item | String | 8000 |  |
| OrderableItem | String | 8000 |  |
| Begin InventoryDateTime | datetime | 8 | The Start of Shrink Period |
| EndInventoryDateTime | datetime | 8 | The End of Shrink Period |
| DaysBetween | smallNumeric | 2 | Number of Days |
| Begin Inventory Count | decimal | 17 | The Count of On Hand at the beginning of the period |
| End Inventory Count | decimal | 17 | The Count of On Hand at the end of the period |
| Begin Value | money | 8 | The Total Value of On Hand at the beginning of the period |
| End Value | money | 8 | The Total Value of On Hand at the end of the period |
| Units Sold In Period | smallNumeric | 2 | Total Number Units Sold in The Period |
| Amount Sold In Period | money | 8 | Total value Sold in the period |
| Units Received | decimal | 17 | Total Number of Units Received in the Period |
| Amount Received | money | 8 | The Total value of Item received |
| Case / Pallets Orders | decimal | 17 | The Number of Cases and Pallets Ordered |
| Case Value / Pallet Value Order | money | 8 | The value of Cases and Pallets Ordered |
| ReclaimQty | decimal | 17 |  |
| FullRetailReclaimAmt | money | 8 |  |
| DiscardQty | decimal | 17 |  |
| FullRetailDiscardAmt | money | 8 |  |
| ShrinkQty | decimal | 17 | Calculated Shrink Units |
| ShrinkAmt | money | 8 | Calculated Shrink Value |
| TransferQty | decimal | 17 |  |
| TransferRetailPriceAmt | money | 8 |  |

[Table 1 Adjustment Reason Example 7](#_Toc463297993)

[Table 2 Data Entity Requirements 8](#_Toc463297994)

[Table 3- Location Hierarchy 20](#_Toc463297995)

[Table 4 Product Hierarchy 21](#_Toc463297996)

[Table 5 Orderable Hierarchy 22](#_Toc463297997)

[Table 6 Vendor Orderable Item 22](#_Toc463297998)

[Table 7 - Breakout 23](#_Toc463297999)

[Table 8 - Range 23](#_Toc463298000)

[Table 9 - Vendor 24](#_Toc463298001)

[Table 10 - Adjustments 25](#_Toc463298002)

[Table 11 - Counts 26](#_Toc463298003)

[Table 12 - Invoice 26](#_Toc463298004)

[Table 13 - orders 27](#_Toc463298005)

[Table 14 - On hand Ledger 28](#_Toc463298006)

[Table 15 - Receiving 28](#_Toc463298007)

[Table 16 - Shipments 30](#_Toc463298008)

[Table 17 - Transfers 31](#_Toc463298009)

[Table 18 - Shrink 31](#_Toc463298010)

[Figure 1 5](#_Toc463298011)

[Figure 2 Example Item Setup 6](#_Toc463298012)

[Figure 3 7](#_Toc463298013)

[Figure 4 9](#_Toc463298014)

[Figure 5 Numericegration Collection Bus 19](#_Toc463298015)

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
