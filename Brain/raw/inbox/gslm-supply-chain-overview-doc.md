---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/gslm/GSLM Supply Chain Overview.doc.md
tags: [canary, gslm, retail-data-model, walmart, comparison, tier1-extract]
project: canary
status: unprocessed
---

# GSLM Supply Chain Overview.doc

## Source
File: `Brain/raw/.extract/tier1-md/gslm/GSLM Supply Chain Overview.doc.md`
Size: 18,666 bytes

## Raw content
The Global Store Interface Project Supply Chain entities define the inventory position of product in each store, and the data required to send and receive product in the store.

Use Cases:
Receive WMDC electronic invoice in store
Send WMDC electronic invoice acknowledgement to Home Office
Receive Vendor direct Purchase Order in store
Send PO receipt to Home Office
Create Manual Store Order
Send / Receive store to store transfer
Receive daily perpetual inventory synch in store
Send inventory adjustments from store to Home Office
Send claims, overs, shorts, to Home Office

The following section describes the GSLM entities and their attributes which have been modeled as part of the Supply Chain scope:
Entity Name
Description
Vendor
The logical entity where vendor master records are held in the GSLM.  It contains the subset of vendor attributes which are required for store processes, and only contains the suppliers who  supply merchandise which is delivered to store.
Attribute
Type
Description
vendor_nbr
 Number
The 9 digit Walmart supplier number which is composed of the 2 digit department, 6 digit supplier number and 1 digit sequence number
vendor_name
 Text
The description of the supplier



Entity Name
Description
SKUItemVendor
The logical entity which defines the relationship between a sku and the vendors which supply the sku.  The vendor entity contains all attributes of the SKU that can vary by supplier.  Although the current Item file requires that a new item be created for every vendor who supplies and item, this construct allows multiple vendors to be assigned as suppliers of a single item.
Attribute
Type
Description
vendor_stock_id
 Number
The internal number a vendor may use to describe the item it supplies to Walmart
sku_item_nbr
 SKUItems
The Foreign key to the SKUItem entity, the unique identifier of the SKU.
vndr_frst_avail_date
 DateTime
The date when the merchandise is first available to be ordered from the vendor.
item_type_code
 Code
The two digit numeric code used by replenishment systems to determine how an item is ordered and delivered to store
rpl_subtype_code
 Code
REPLENISHMENT SUBTYPE CODE determines the Shelf Label design and informs the store how the product is ordered
vendor_nbr
 Vendors
The foreign key to the Vendor entity, the unique identifier of the Vendor.
vndr_frst_ord_date
 DateTime
VENDOR FIRST ORDER DATE is the first date that product may be ordered from the Vendor (Supplier) by the Store, Club or Distribution Center.
country_of_origin
 Code
The country code of the location where the vendor manufactured the item



Entity Name
Description
PackItem
The enity which defines the GSLM PackItem.  GSLM packs can be vendor or warehouse packs, and represent the unit which can be ordered from a vendor or sent
Attribute
Type
Description
pack_item_id
 Merchandise
Primary Key, the unique identifer of the Pack
pack_type
 Code
Defines the pack type (warehouse or vendor)
pack_qty
 Number
Total number of units in the pack
cspk_code
 Code?
ASEPACK CODE - Case pack type.  C - Case: Vendor Pack is equal to the Warehouse Pack.  B - Breakpack: Multiple Warehouse Packs within a Vendor Pack.
pack_netwgt_qty
 Number
The weight of the pack
pack_netwgt_uom
 Code
The net weigh unit of measure
RFID_ind
 Indicator?
Indicates if apck has an RFID tag.
pack_assortment_code
 Code?
Indciates if the pack item is an assormtnet or complex pack of two or more invidual sku items.



Entity Name
Description
PackItemBreakout
The entity which defines the SKU items which are contained in the pack.  There can be one or more different sku items contained in a single pack.
Attribute
Type
Description
sku_item_nbr
 SKUItems
The unique identifier of each sku item in the pack.
pack_item_id
 PackItems
The foreign key reference to the Pack item entity.
sku_item_qty
 Number
The quantity in eaches of the sellable sku items contained in the pack.



Entity Name
Description
PackBreakout
The pack breakout entity creates a hierarchical structure which allows a group of pack items to be related to one another.  (e.g., The pallet, case, inner relationships of vendor and warehouse packs.)  This structure supports the global trade pack relationship standards.
Attribute
Type
Description
parent_pack_item_id
 PackItems
The unique identifier of the parent pack. (E.g. Pallet)
child_pack_item_id
 PackItems
The unique identifier of the child pack. (E.g. Case)

 Number
The number of children packs contained in the parent (E.g., 12 cases per pallet)



Entity Name
Description
PackItemInSalesOutlet
The entity which defines the PackItem to SalesOutlet relationship,  it defines which stores are valid for the pack, the attributes of the PackItem which may vary by location.
Attribute
Type
Description
pack_item_id
 PackItems
Foreign key to the PackItem entity, the unique identifer of the Pack
sales_outlet_id
 SalesOutlets
Foreign key to the SalesOutlet entity, the unique identifier of the Sales Outlet
pack_cost_amount
 Amount
The cost amount of the pack in the store.
pack_sell_amount
 Amount
The retail value of the pack
pack_min_ord_qty
 Number
The minimum order quantity of the pack in the store
pack_max_ord_qty
 Number
The maximum order quantity of the pack in the store
pack_incrm_ord_qty
 Number
The order multiple of the pack in the store



Entity Name
Description
WarehouseShipment
The Warehouse Shipment entity defines the header record for warehouse to store shipments. It is the GSLM entity which describes the WMDC electronic invoice sent from Home Office systems to store
Attribute
Type
Description
invoice_nbr
 Number
 This contains 11 digit invoice number – first 5 digits depot number and 6 digit is reserved for WM, 7-11 digits are next sequence number starting with 1
invoice_date
 DateTime
Invoice date in CCYY-MM-DD format
sales_outlet_id
 SalesOutlets
The store number of the destination store.  Foreign key to the Sales Outlet entity.
dc_nbr
 Number
The location number of the sending warehouse.
dc_country
 Code
The country code of the sending warehouse.
invoice_type
 Code
The value field which can be used to define invoice types, or the source of the invoice.
trailer_nbr
 Number
Trailer number. Changed from 15, matching GLS global data model.
post_date
 DateTime
This needs to be the date for posting financials.
financial_date
 DateTime
The financial date of the transaction.
est_arrival_date
 DateTime
Estimated arrival date in CCYY-MM-DD format
shipment_nbr
 Number
This contains shipment number ~ Default to zeros on MGDS
carrier_id
 Number
The identification number of the carrier delivering the trailer to store
full_case_cnt
 Number
This indicates number of full cases in the invoice ~ Default to zeros on MGDS
brpk_repk_cnt
 Number
Number of sortation labels ~ Default to zeros on MGDS
brpk_pick_cnt
 Number
This is actual break-pack pick count contained in all sortation labels ~ Default to zeros on MGDS
void_case_cnt
 Number
This contains number of voided labels in the invoice ~ Default to zeros on MGDS
less_than_case_flag
 Flag
Contains the flag indicating if the item is less than a case ~ Default to spaces
no_of_details
 Number
Contains the number of line item details associated with the invoice header
invoice_charge_type
 Code
 This contains charge type.  01 – Inbound  02 – Outbound  03 -  Service / Handling  04 – Excise  05 – Insurance  06 – Cartage  07 – Ocean freight  08  - Upcharge
invoice_charge_amt
 Number
This contains the charge amount
invoice_cost
 Number
This contains total cost for the invoice
invoice_retail
 Number
This contains the retail value of the invoice
currency_code
 Code
The currency code of the cost and retail amounts on the invoice



Entity Name
Description
WarehouseShipmentDetail
The entity which defines the line item details of the Warehouse Shipment.
Attribute
Type
Description
invoice_nbr
 WarehouseShipments
Foreign key to the Warehouse Shipment entity, defines the header record associated with the line item detail.
invoice_line_nbr
 Number
The line number on the invoice
sku_item_nbr
 SKUItems
The sku item identifier of the product being shipped to store
pack_item_nbr
 PackItems
The warehouse packitem number of the pack being shipped to store
start_carton_nbr
 Number
This contains beginning bar code. Currently it is 11 digits.
end_carton_nbr
 Number
This contains ending bar code. Currently it is 11 digits.
item_cost
 Number
The item cost for the invoice line item
item_qty
 Number
The total number of sku item units being delivered to store
qty_uom
 Code
The quantity  unit of measure code for the units being delivered
invoice_item_charge_type
 Code
 This contains charge type.  01 – Inbound  02 – Outbound  03 -  Service / Handling  04 – Excise  05 – Insurance  06 – Cartage  07 – Ocean freight  08  - Upcharge   09 - Claims
invoice_item_charge_amt
 Number
Contains charge amount
currency_code
 Code
The currency code of the cost and retail amounts on the invoice
item_qty_weight
 Number
Total weight of the Sku items being shipped on the invoice line
act_whpk_ship_qty
 Number
The quantity of warehouse packs being shipped
whpk_to_label_ratio
 Number
This contains number of warehouse packs to a label
label_type
 Code
This contains order filling method(Pallet pulls / case pulls etc.,). For ex : LBSS /PLSS
pick_label_flag
 Flag
This indicates whether picks have label or not (Y/N)  ~ Default to "Y"
cwo_flag
 Flag
The cancel when out flag, informs the store that the units being shipped will no longer be stocked in the warehouse once the current supply is depleted
dot_com_flag
 Flag
Indicates the invoice line item is part of a site to store order
package_type
 Code
 This indicated package type case(101), Break-pack each (102), Pallet each(103), Pallet (201), Break-pack (202)
stocking_date
 DateTime
Date in CCYY-MM-DD format. This is the stocking date on which merchandise needs to be stocked



Entity Name
Description
WarehouseShipmentReceipt
The entity which defines the invoice acknowledgment message which is sent form store to Home Office
Attribute
Type
Description
whse_ship_rcpt_nbr
 Number
The unique identifier of the invoice receipt
invoice_nbr
 WarehouseShipments
The number of the invoice being received
rcvg_user_id
 Associates
The user id of the associate receiving the invoice
terminal_id
 Number
The terminal id of the machine used to process the invoice receipt
shipment_rcpt_date
 DateTime
The date of the invoice receipt transaction



Entity Name
Description
StoreOrder
The entity which defines the header record of a manual a store order
Attribute
Type
Description
store_order_nbr
 Number
The unique identifier of the store order
sales_outlet_id
 SalesOutlets
The store id of the originating location
store_order_date
 DateTime
The date the store order was created
store_order_type
 Code
The manual order type (manual, assembly, ors)
store_order_status
 Code
The status code of the manual order
ors_sheet_nbr
 Number
The order sheet number if the order type is ORS.  A calculated field: (Item’s accounting dept * 100) + (WMT day of week *10)
ors_ord_flag
 Flag
The order review sheet flag if the order type is ORS.  (May not be required in future if all manual order types can be contained in a single store order entity, the order type filed could be translated to this indicator)



Entity Name
Description
StoreOrderDetail
The line item details of a store order, contains the sku item number, quantity and current inventory position from store PI of the item being requested by the store.
Attribute
Type
Description
store_order_nbr
 StoreOrders
Foreign key to the store order table, the unique identifier of store order to which the line item is associated.
store_order_line_nbr
 Number
The link number of the item on the store order
sku_item_nbr
 SKUItems
The sku item number of the product being ordered
ordered_qty
 Number
The quantity requested
on_hand_qty
 Number
The current store on hand from store systems
in_transit_qty
 Number
The current in transit qty from store systems
on_order_qty
 Number
The current on order quantity from store systems



Entity Name
Description
PurchaseOrder
The logical entity which describes the purchase order stores receive for products which are being shipped direct to store from a vendor
Attribute
Type
Description
po_nbr
 Number
The unique purchase order number for this order
po_status
 Code
The status of the purchase order, valud status's are (A)ctive, (I)nactive, (D)eleted
sales_outlet_id
SalesOutlets
The sales outlet where the goods are being receipted
po_vendor_nbr
 Vendors
The vendor who provides the goods to be purchased
carrier_vendor
Vendors
The vendor number of the carrier who is physcially delivering the goods.
carrier_processing_nbr
 Number
The reference number of the shipment from the carriers perspecitve
carrier_processing_date
 DateTime
The date the carrier processed the shipment
bill_code
 Code
Indicates if the goods were prepaid or collect
actual_weight
 Number
The actual weight of the shipment
weight uom
Code
Unit of measure
actual_freight_charge
 Number
The freight charge for the shipment
currency code
Code
Currency code of the charge amount
pickup_date
 DateTime
The date the carrier picked up the shipment from the vendor
process_date
 DateTime
The date the order was procesed



Entity Name
Description
PurchaseOrderDetail
The logcial entity for the line items within the purchase order
Attribute
Type
Description
po_nbr
 PurchaseOrders
The reference number of the purchase order header this line is attached to
po_line_nbr
 Number
The unique line number in the purchase order for this item
sku_item_nbr
 SKUItems
The SKU number of the item on the purchase order
pack_item_nbr
 PackItems
The pack number of the delivered unit
ordered_item_qty
 Number
How many of this item was ordered (at SKU Level)
shipped_item_qty
 Number
How many of this item was shipped (At SKU Level)
shipped_pack_qty
 Number
How many packs of this item shipped



Entity Name
Description
PurchaseOrderReceipt
The entity for receipting goods which were supplied direct to store. This is related to the Purchase Order and PurchaseOrderDetail Entities as it is the logical receipt for a PO.
Attribute
Type
Description
po_recvr_nbr
 Number
A unique identifier for this receipt
po_nbr

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
