---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/gslm/GSLM Space Planning Overview.doc.md
tags: [canary, gslm, retail-data-model, walmart, comparison, tier1-extract]
project: canary
status: unprocessed
---

# GSLM Space Planning Overview.doc

## Source
File: `Brain/raw/.extract/tier1-md/gslm/GSLM Space Planning Overview.doc.md`
Size: 9,311 bytes

## Raw content

The GSLM space planning entities described in this document are representative of the data which flows from Home Office to store in the current state.  The structure and relationships of the entities in this model are based on industry standards and are intended to provide for integration with future functionality being developed.  The GSLM is an extensible model, the attributes of the entities contained can be altered to support additional space planning data as necessary.
Assumptions:
Items are traited to stores via Home Office processes which define the SN2000 file for each location (sales outlet)
The GSLM SKUIteminSalesOutlet defines the valid relationship between items and stores, the contents of this entity is defined via the ETL process which will load the SN2000 files to the model
 EMBED Visio.Drawing.11
The current ProSpace application which sends planogram and floorplan application files to stores may not exist in acquired markets.  Therefore Planogram files and Floorplan files will be delivered to store in an electronic document form that can be printed if the ProSpace application is not available.
The Smart Systems which receives product add / delete documentation will not exist in non converted stores, this documentation will be sent to store in a hard or soft copy packet with the Planogram and floorplan documents.
Use Cases:
Define the valid skuitems which should be sent to store
Deliver a planogram document to store
Deliver a Floorplan document to store
Deliver product add / delete documentation  to store
The following section describes the GSLM entities and their attributes which have been modeled as part of the space planning scope:
Sales Outlet
Entity Name
Description
SalesOutlet
The logical entity which contains the GSLM master records for all outlets where a consumer can purchase goods.  It provides the ability to distinguish between location types such as stores, clubs, websites, mobile devices, etc.
Attribute
Type
Description
sales_outlet_nbr
 Number
The Primary key of the sales outlet entity which uniquely identifies the outlet in the GSLM.
country_code
 Code
The two digit country code that describes the country or market where the outlet is located, in the current systems country code is part of the location key.
sales_outlet_type
 Code
A code value which defines the type of sales outlet.  (Club, Store, Web)

Sales Floor
Entity Name
Description
SalesFloor
The SalesFloor entity defines the possible layouts or formats which can be associated with a sales outlets in the organization.  A single SalesFloor (floorplan) can be assigned to one or more sales outlets.
Attribute
Type
Description
sales_floor_plan_id
 Number
The unique identifier for the floor plan
floorplan_desc
Text
The floorplan description (E.g. Supercenter Fall 2009)
flrplan_dept_nbr
 Number
An identifier used to group floorplans
flrplan_seq_nbr
 Number
A system assigned sequence number for a floorplan/department
flrplan_ver_nbr
 Number
A system assigned sequence number for a floorplan/department

Sales Floor in Sales Outlet
Entity Name
Description
SalesFloorsInSalesOutlet
The entity which defines the relationship between the sales floors and sales outlets at specific point in time.  A sales out let can have more than one sales floor assigned to it, but only one is active and represent the current layout of the store.
Attribute
Type
Description
sales_floor_plan_id
SalesFloors
Foreign key to the SalesFloor entity, the unique identifier of the floorplan
sales_outlet_id
 SalesOutlets
Foreign key to the SalesOutlet table the unique identifier of the store.
flrplan_status_cd
Number
The sales floor status code, Active, Finalized, discontinued, etc…
flrplan_relay_text
Text
A message from the HO to the store.
start_date
 Date
The date when the sales floor layout is communicated to store.
effective_date
 Date
The date when the new sales floor layout should be set in the store.
end_date
 Date
The end date of the sales floor layout.

Sales Floor Segment
Entity Name
Description
SalesFloorSegment
The sales floor segment entity defines the specific locations on the sales floor where space planning modulars (planograms) can be attached.  A segment can represent a modular department, modular category, or singular point in the store which has a specific fixture type; and can be planogrammed in the space planning systems. (E.g. hang tags in a aisle, peg location on a feature end)
Attribute
Type
Description
segment_id
Number
A unique identifier for a specific location on the sales floor where one or more SalesOutletAsset (fixtures) of the same type is attached
sales_floor_plan_id
 SalesFloors
Foreign key to the SalesFloor entity, the unique identifier of the floorplan.
sequence_nbr
Number
The sales floor sequence of the asset in the merchandise category
segment_width
Number
width of the section.
seg_x_coordinate
 Number
x coordinate of the segment location on the sales floor layout.
seg_y_coordinate
 Number
y coordinate of the segment location on the sales floor layout.
seg_z_coordinate
 Number
z coordinate of the segment location on the sales floor layout.

Modular on Sales Floor Segment
Entity Name
Description
ModularOnSalesFloorSegment
A logical construct which represents the relationship between modulars (planograms) and segments, the specific position on the sales floor where this mod is located.
Attribute
Type
Description
segment_id
Number
Foreign key to the SalesFloorSegment entity, the unique Identifier for the segment
modular_id
Number
Foreign key to the Modular entity, the unique Identifier for the modular planogram

Modular
Entity Name
Description
Modular
The Modular entity is the planogram header, it defines the product category of the merchandise, the type and number of assets which are attached to a segment, and the time period for which the relationship is valid.
Attribute
Type
Description
modular_id
Number
Unique Identifier for rather modular planogram
modular_plan_title
Text
User entered name for a modular.
mod_plan_status
Number
Status of the modular, finalized, discontinued, etc…
store_cluster_code
Number
Tells us if the modular is a clustered or store specific galleria modular.
modular_dept_nbr
Number
An idenfier used to group modulars
modular_catg_nbr
Number
An identifier to group modulars
mod_plan_uom_code
Code
Unit of measure for the modular, centimeters or inches.
mod_height
Number
Height of the Modular
mod_width
Number
Width of the Modular
mod_depth
Number
Depth of the Modular
asset_type
Code
The type of asset or fixture being planogrammed for the modular, a modular should have only one asset type.
asset_qty
Number
Number of assets of the same type in a modular
start_date
Date
The date when the asset layout is communicated to store.
effective_date
Date
The date when the new asset layout should be set in the store.
end_date
Date
The end date of the asset layout.
relay_ind
Flag
Tells the store if the modular is a re-set
relay_date
Date
Date the store begins to set the modular. Usually the same as relay date, but may be later if the store received the modular after other stores.
relay_message
Text
A message attached the modular to instruct the store.
confirm_ind
Flag
Tell the system whether or not the store is expected to confirm the modular.

Sales Outlet Asset
Entity Name
Description
SalesOutletAsset
The entity which defines the fixtures which can display merchandise for a customer to purchase.  (E.g. Rack, Shelf, Peg, Check Stand)
Attribute
Type
Description
sales_outlet_asset
SalesOutletAssets
Foreign key to the SalesOutletAsset entity, the unique identifier of the asset.
asset_type
Code
The type of asset (Shelf, peg, etc.)
asset_description
Text
The long description of the asset
asset_height
Number
Height of the base deck
asset_width
Number
Width of the base deck
asset_depth
Number
Depth of the base deck
notch_type_code
Number
notch_type_code
drawing_base_desc
Text
Description for a base deck
merchandise_id
Merchandise
The foreign key to the Merchandise entity.  This relationship allows for unique barcodes assigned to an individual asset.

Sales Outlet Asset on Modular
Entity Name
Description
SalesOutletAssetOnModular
The SalesOutletAssetOnModular is the planogram detail record, it defines the position or sequence of the asset on the modular, the consumer items  at article level (upc) which are display on the asset, and the details of the product in a specific location. (Facings, shelf sequence, capacity, etc.)
Attribute
Type
Description
Modular_id
Modular
Foreign key to the Modular table
sales_outlet_asset_id
SalesOutletAsset
Foreign key to the SalesOultletAsset, identifies the asset on which the merchandise is located
asset_seq_nbr
Number
Order of the fixture on the planogram
article_item_nbr
ArticeItem
Foreign key to the ArticleItem entity, defines the UPC for the specific product which is being planogrammed.
mdse_rank_nbr
Number
Position of the UPC within a section.
horiz_facings_nbr
Number
Number of facings across
vert_facings_nbr
Number
Number of vertical facings.
product_loc_nbr
Number
Combination of rank and section number
total_capacity
Number
Total number of an item that will fit in this position after min max settings are applied.









Global Store Logical Model – Space Planning

 PAGE   \* MERGEFORMAT 2 | Page




## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
