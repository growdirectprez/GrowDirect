The Global Store Logical Model is based on a generic retail data model common to the industry; it is intended to provide for easier integration with a variety of ERP systems that may be encountered in acquired markets.  The Item components of the GSLM contain reference data for the Merchandise Hierarchy, SKU Item, Article Item, and their related entities.  
Use Cases:
Define the Merchandise Hierarchy
Create a style
Create a sellable item in SKUItem 
Create a sellable pack in SKUItem
Create an orderable PackItem
Assign a barcode for a SKU or Pack item
Assign SKUItem to locations
Assign PackItem to locations
Create multiple values for an item attribute (Descriptions in Multiple Languages)
Define tax codes for an item in a location
Create a complex pack
Define a pack hierarchy
Define the baseitem for a SKUItem
Create a sellable break pack item (Item sold in eaches and cases)
Create a SKUItem vendor relationship
Assumptions:
Inventory is maintained at the SKUItem each level.  
If an item can be sold in multiple configurations, the SKUItem number of the each will the base item number for all other items.  
Orderable packs are defined in the PackItem entity; there are no orderable packs in SKUItem.  If a pack can be ordered, distributed and sold in the same configuration, the sellable pack will have a SKUItem record separate from the PackItem.
ArticleItems define the scannable barcodes and other reference numbers that can be associated with all Merchandise Types.
Item traits that define the valid range of product for a location are not contained in the GSLM, the SKUItem in SalesOutlet entity which defines valid sku store combinations is loaded via the SN2000 process which is downstream from the Item Trait functionality in Home Office systems.
The GSLM merchandise hierarchy is a six level hierarchy.  The BusinessDivision, Department, Subclass, Fineline levels map to Home Office.  Other levels are intended to provide flexibility when mapping to the hierarchy which may exist in a non-converted store.
The GSLM style entities are not required for Home Office to Store mapping in the current state.  Style provides a link to standard retail merchandising systems and item classifications that may be encountered during physical implementations with other retail businesses.

The following section describes the GSLM entities and their attributes which have been modeled as part of the Item scope:
Entity Name
Description
BusinessDivision
Level 1 of the Org hierarcional and Merchandise Hierarchies.  Business division represents major segments of the Walmart Business (E.g. Dvision1 - Wa,art Stores, Div 18 - Sam's Club).  The GSLM organizational hierarchy is a 4 level structure, the definiton of each level in the organizational heirarchy can vary by divison, and should be defined based upon the needs of the organization being mapped to the GSLM.
Attribute
Type
Description
business_div_id
Number
Unique identification number of the business division in the GSLM merchandise and organizational hierarchies.
business_div_desc
Text
Business division description 
country_code
Code
The country code of the Division, inherited by each sublevel of the hierarchy. 



Entity Name
Description
Department
Level 2 of the merchandise hierarchy, it is a single entity containing the two hierarchy levels currently known as accounting department and order department.  Accounting and order departments have been collapsed into a single entity because order department was created due to a system constraint causing accounting departments to run out of available item numbers.  There was no logical or business need and the Global Store Logical model (GSLM) is not constrained in the same manner.
Attribute
Type
Description
dept_nbr
Number
Unique identification number of new department entity which contains the current accounting and order departments.
acctg_dept 
Text?
Accounting department to which to department is assigned.
 
Text
Department description (E.g. Mens Boys, Frozen)
business_division
BusinessDivision
Refers to the BusinessDivision entity, the parent of the Department entity.



Entity Name
Description
Section
Level 3 of the merchandise hierarchy, Section is an additional level added to the GSLM to support integration with new retail companies who might have additional levels in their existing hierarchy.
Attribute
Type
Description
section_id
Number
Unique identification number of the Section in the GSLM merchandise hierarchy.
section_desc
Text
Section description (E.g. Mens, Seafood)
department
Department
Refers to the Department entity, the parent of the Section entity.



Entity Name
Description
Class
Level 4 of the merchandise hierarchy, Class is an additional level added to the GSLM to support integration with new retail companies who might have additional levels in their existing hierarchy.
Attribute
Type
Description
class_id
Number
Unique identification number of the Class in the GSLM merchandise hierarchy.
class_desc
Text
Class description (E.g. Shirts, Fish)
section
Section
Refers to the Section entity, the parent of the Class entity.



Entity Name
Description
SubClass
Level 5 of the merchandise hierarchy, subclass is an additional level added to the GSLM to support integration with new retail companies who might have additional levels in their existing hierarchy.  It may not map one for one to existing subclasses in the current Walmart enterprise systems.
Attribute
Type
Description
subclass_nbr
Number
Unique identification number of the Subclass in the GSLM merchandise hierarchy.
subclass_desc
Text
Subclass description (E.g.T-Shirts, Breaded Fish)
Class
Class
Refers to the Class entity, the parent of the SubClass entity.



Entity Name
Description
Fineline
Level 6 of the merchandise hierarchy, the GSLM fineline is a unique identifier composed of the current Walmart order department, subclass and fineline (e.g. 24-3706).  It is the level of the hierarchy where the Item structure is attached.
Attribute
Type
Description
fineline_nbr
Number
Unique identification number of the Fineline in the GSLM merchandise hierarchy.  This number will be a concatenated form of order department, subclaas, and fineline from the current enterprise systems.
fineline_desc
Text
Fineline description
subclass
SubClass
Refers to the subclass entity, the parent of the Fineline entity.

Entity Name
Description
Merchandise
Merchandise is a logical entity that groups multiple items types into a single container.   It enables the ability to create attributes with multiple values across which are common cross item type.  (E.g. creating item descriptions in multiple languages)
Attribute
Type
Description
merchandise_id
Number
The unique identifier for Merchandise across items types.  Merchandise ID has a foreign key relationship to SKUitem, PackItem, ArticleItem, OuterCase, and Style.  
merchandise_type
Text
A code value that identifies the type of the child item.



Entity Name
Description
MerchandiseType
The logical entity which defines the types of merchandise which can exist in the GSLM.  (E.g. SKU, STYLE, ARTICLE, PACKITEM)
 
 
 
merchandise_type
 Text(10)
The Type code of the merchandise type.



Entity Name
Description
MerchandiseAttributeLanguage
A logical entity which contains localized attributes across item type (e.g. shelf label fields by country)
Attribute
Type
Description
merchandise_id
Merchandise
PRIMARY KEY:  Unique identifier of the MerchandiseAttributeLanguage entity, also the foreign key to the merchandise entity. 
language_code
Text?
PRIMARY KEY: Second Primary key of the MerchandiseAttributeLanguage entity, defines the language used to describe the merchandise attributes in the entity.
shop_desc
Text?
SHOP DESCRIPTION: is used only in Softlines or Shoes and is a description for various groupings of clothing, i.e., Sportswear, Casual.  The Ticket description is created by combining the Fineline Number with the Shop Description.
signing_desc
Text?
SIGNING DESCRIPTION is displayed on shelf signs or flags at the store.  This is used for all lines of the business (Hardlines, Grocery...) but may be the same as Item1_desc.
shelf_lbl_colour_desc
Text?
SHELF LABEL COLOR DESCRIPTION (Shelf Label 1 Desc) is a 6 character description that is transmitted to the store and printed on the shelf label.  This is also known as the Color Description.  The name of this field is misleading for all hardline merchandise. It is in fact merely another six  character description of the merchandise.  In Softlines it is selected in the BIF system from the variants available and should have true color meaning for apparel and shoes.  Also transmitted to a third party for the preparation of merchandise price tags.
shelf_lbl_size_desc
Text?
SHELF LABEL SIZE DESCRIPTION (Shelf Label 2 Desc)  is a 6 character description that is transmitted to the store and printed on the shelf label.  The name of this field is misleading for all hardline merchandise. It is in fact merely another six  character description of the merchandise.  In Softlines it is selected in the BIF system from the variants available and should have true size meaning for apparel and shoes.  Also transmitted to a third party for the preparation of merchandise price tags.  This is called Shelf Label 2 description in MIM.
upc_desc
Text?
UPC DESC  - This is the item description that will print at the register on the customer receipt
item_desc1
Text?
ITEM1 DESC  is the first line of the item description.    NOTE: Only the first of the two item descriptions is sent to the store systems.
item_desc2
Text?
ITEM2 DESC ID - is the second line of the item description.  This description has been used for other things:  Cancel when out date is put here on the I2A.
country_code
Code
COUNTRY CODE a two character code to describe the country associated with values for each attribute



Entity Name
Description
Style
Style is a logical grouping of like items with varying characteristics that are considered a single merchandising entity. Style is a retail industry standard commonly used in apparel for mass sku creation sku items which vary by a predefined set of dimensions, and are tracked as separate units from an inventory standpoint.  This has been added to create an item template structure which is common across the industry and a core component of most Retail ERP systems.
Attribute
Type
Description
Style_id
Merchandise
Unique identification number for each style in the GSLM merchandise hierarchy
fineline
Finelines
Refers to the fineline entity, the parent of the Style entity.



Entity Name
Description
StyleVariantGroup
The logical construct which assigns valid variant groups to Style describing the unique characteristics of each SKUItem related to the style.
Attribute
Type
Description
style_variant_group_id 
 Number
The unique identifier of each style variant group
style_variant_group_desc 
 Text
The business description of the style variant group.  The description should contain a reference to the variant values which define the group, (E.g., Red Small, Blue Large)
style_id 
 Styles
The Foreign Key relationship of the Style Variant group to the Style



Entity Name
Description
StyleVariantValue
A logical entity containing the possible values for each valid style variant dimension.
Attribute
Type
Description
style_variant_id 
 StyleVariants
The Primary key of the StyleVariantValue entity
style_variant_value 
 Text(50)
The value definition for each unique Style Variant (E.g. Red, Blue, Green)



Entity Name
Description
StyleVariant
The logical grouping of variant values into a set of characteristics used to define one of the style dimensions. (E.g. Color, Size, Width)
Attribute
Type
Description
style_variant_id 
 Number
The Primary key of the Style Variant entity
style_variant_desc 
 Text
The description of the group to which variant values are assigned.  (E.g., Colors, Waist Sizes, Shoe Widths, Shirt Sizes)



Entity Name
Description
SkuItem
The core logical entity which describes the stock keeping unit and the distinct merchandise unit that can be purchased by the consumer.  It is the level at which merchandising and replenishment processes track inventory.  In the GSLM the SKUItem record does not contain supply chain specific information (e.g. pack details or vendor data).  The GSLM does not require multiple records for a single consumer unit as required in the current state.
Attribute
Type
Description
sku_item_nbr 
Merchandise
PRIMARY KEY:  The unique value for all stock keeping and sellable items in the GSLM, and foreign key to the Merchandise entity
style 
StyleVariantGroups
Foreign key to the style entity, which describes the group of sku items with similar merchandising characteristics
base_item 
 SKUItems?
A recursive reference to sku_item_nbr which provides the ability to model break to sell items in the GSLM, and also supports the concept of prime item in the GSLM
 consumer_item_nbr 
 Number?
CONSUMER ITEM NUMBER has been added to the GSLM as an attribute of skuitem to ensure that any enterprise functionality that it supports is not disrupted, it is unclear how this field is used exactly and to what extent.  It appears to have a similar purpose as the SKU_ITEM_NBR but is not an exact match due to current system limitations.  It has been described as an item that can be sold at the retail level as a single unit to the consumer.  It addresses those instances where there are multiple Item Numbers (Supply) created for a single Consumer Item. This occurs when there are different replenishment methods, vendors, costs and when the same merchandise is sold in multiple departments.  Any one of the Item Numbers (Supply) may to used to replenish the Consumer Item.   Once it is sent to the store it will become the number that will always serve as the store reference. It is the new number that will be printed on shelf labels and should reduce the effort currently expended on replacing shelf labels.   
 item_status_code 
 Code?
ITEM STATUS CODE represents the status of an item.  Valid values are A=Active, I=Inactive, D=Delete.    Active: The item is available for the buyer to use (replenishment, purchase orders, return sheet, etc.).  A non-replenishable item type with no purchase order activity will not automatically be in a stores file even though the item is classed and traited for the store.  If a purchase order is not written on the item it must be forced to the store by the UPC office using ITFI before it will scan.  
 item_create_date 
 DateTime?
ITEM CREATE DATE - Date the item was created.
 item_expire_date 
 DateTime?
ITEM EXPIRE DATE is the date this item number will go into "Inactive" status and begin the purge process.  Nonreplenishable items types should be set with a reasonable expiration date allowing time for the product to sell through.  
 send_store_date
 DateTime?
SEND TO STORE DATE is the date the item information is sent to the store. The item will be loaded into the store’s item file after the evening batch process.     At item creation the Send Store Date must be <= Item Effective Date i.e. the item is sent to the store before it can be reordered.  In Hardlines and Grocery the default is Today + 1 to allow review.  In Softlines the default is Today (no review is needed since Softline Items are not traited and classed).     At item maintenance, for active items, the Send to Store Date can be changed only if the current value is in the future.  No past dates are allowed.    The Send To Store date is updated when the Item Status has changed from Delete or Inactive to Active.     Note: If an item has not reached a send to store date, it will NOT go into a stores file to scan.  It is one of the tools that "can" be used to control an item when necessary.
 variable_wt_ind 
 Indicator?
VARIABLE WEIGHT IND should be named to SCALABLE AT FRONT REGISTER IND - Y/N whether item is weighable at front register.  This field is mutually exclusive with backrm_scale_ind).  NOTE: This works in conjunction with the PLU number of an item and is also used for merchandise that is sold by count such as peppers.
 backroom_scale_ind 
 Indicator?
BACKROOM SCALE IND indicates that an item is weighed in the backroom (Deli, Bakery, Produce and Meat).  This field is mutually exclusive with variable_wt_ind (scalable at front register ind).  NOTE: This is used at the stores to determine which items must have pricing data sent from the Smart system to the scales that generate barcode labels that include the price.
 temp_sensitive_ind 
 Indicator?
TEMPERATURE SENSITIVE IND indicates if an item is sensitive to either excessive heat or cold.   This is currently used for new store openings when merchandise may sit in a truck waiting to be unloaded for an excessive amount of time.
temp_uom 
 Code?
Temparture Unit of measure (E.g., F,C)
 account_nbr
 Text(50)?
ACCOUNT NUMBER is the General Ledger account number that this item of merchandise is booked to.  Usually an item is booked to it’s Accounting Dept Number which is translated to an account number (8xx where xx is the accounting department number).  Account Number is initially going to be used for supply items and allows a more detailed breakout of expenses.  There are also plans to use account number for non-inventory items (Kiosk, Savings Stamps, Scratch off lottery tickets and Gift Cards).  Non-inventory items are:  Items that are not merchandise items and therefore do not get posted to a purchase account.  They are not part of the physical inventory that gets counted and they do not get registered sales.
 account_nbr_type_code 
 Code?
Denotes the what type of journal account the account number represents. Examples:  Department sales account 3 followed by department number, Other Income account, Service Income account, Consumable account.    CONSUMABLE ACCOUNT NUMBER is the General Ledger Account Number that consumable items (supplies) may be charged to.  Usually an item is booked to it’s Accounting Dept Number which is translated to an account number 8xx (where xx is the Accounting Department).  Entering the Consumable Account Number at item creation will allow a more detailed breakout of expenses while eliminating the need for a manual MTR (Merchandise Transfer Request) at the store.    OTHER INCOME ACCOUNT NUMBER is the General Ledger Account Number that may be used for crediting sales for items that are considered "Other Income" such as Gift Cards, Saving Stamps and Scratch off Lottery Tickets.    SERVICE INCOME ACCOUNT NUMBER is the General Ledger Account Number that may be used for Services.  Examples Cell Phone Plans.
 base_unit_rtl_amt 
 Amount?
BASE UNIT RETAIL AMOUNT - Corporate Base Unit Retail of an item. Also known as selling price.   NOTE: This is the default retail for many items, but has little if any meaning in Grocery due to the actual pricing policies which usually requires a store specific retail.
 base_rtl_uom_code 
 Code?
BASE RETAIL UOM CD - the Unit of Measurement that an item is sold in. Valid Values:  EA, FT, YD, IN, LB, QT, GL, OZ, CA, DZ.
 sell_qty 
 Number?
SELL QTY - Selling Quantity of an item.  This is used in unit price calculations used for Price Comparisons. Example: The Retail Price of Peter Pan Crunchy Peanut Butter is $1.68.  The Sell Qty  is 17.6 OZ.  The calculated price per oz is 9.60 cents.
 sell_qty_uom 
 Code?
SELL UOM CODE  - Unit of Measure of the Sell Qty.
 item_scanable 
 Indicator?
ITEM SCANNABLE IND indicates that this Item is sold through the Point of Sale Register.
 shelf_rotation_ind 
 Indicator?
SHELF ROTATION IND indicates that this item should be stocked at the store with the older merchandise toward the front of the shelf and the newer merchandise toward the back of the shelf.  This is used for product that has a "best if used by" date.  Examples: Milk, Batteries, Medicated Shampoo and Cosmetics.  An Indicator of ’Y’ will cause a symbol to be printed on the Shelf Label notifying the store associates to rotate the merchandise appropriately.
 guar_sales_ind 
 Indicator?
GUARANTEED SALES IND indicates if this item does not sell it may be returned to the Vendor.  This is to keep the stores from marking down these items.
 mfgr_sugd_rtl_amt 
 Amount?
MANUFACTURER SUGGESTED RETAIL AMOUNT is the selling price suggested by the Manufacturer for the product.
 mfgr_pre_price_amt 
 Amount?
MANUFACTURER PRE PRICE AMOUNT is the selling price printed on the sellable product by the manufacturer.
 brand_id 
 Text?
BRAND ID is a unique numeric identifier for the primary description of the product with which the consumer identifies. It usually includes a patent or trademark.  The brand will usually refer to the largest text found on the front of the pack, in a prominent position but may require some additional information in order to make it a meaningful and unique identifier.
 variable_comp_ind 
 Indicator?
Indicates the item can be competitive comp priced either by the price per weight or the item price. Used on items that are sold by the competition with a different pricing structure than Wal-Mart.
 mdse_catg_nbr 
 Number?
MERCHANDISE CATEGORY NUMBER unique identifies a grouping of like items for the purpose of reporting sales or other business transactions by the category.  Examples:    Software  Music  Health Care
 mdse_subcatg_nbr 
 Number?
MERCHANDISE SUBCATEGORY NUMBER uniquely identifies a low level grouping of like items (further defining a Merchandise Category) for the purpose of reporting sales or other business transactions by the category.
 sell_package_qty 
 Number?
Number of units contained in a sellable item.  Example: 6 pack of coke, package qty is 6.
 sell_unit_qty 
 Number?
The quantity of one unit that makes up a sellable package.  Example: if the sellable product is a 6 pack of 8 oz coke the sell unit qty is 8.
 sell_unit_uom 
 Code?
unit of measure for the sell_unit_qty.
comp_shop_package_qty 
 Number?
How the item is to be considered for comparison shopping.  Example a 6 pack of coke can be comp shopped with a package qty of 1 or 6.
 comp_shop_unit_qty 
 Number?
How the item is to be considered for comparison shopping.  Example: a 6 pack of coke can be comp shopped with a unit qty of 1 with a uom of each or a unit qty of 8 with a uom of oz.
comp_shop_unit_uom 
 Code?
The unit of measure for the comparsion shop quantity
 comp_legal_price_qty 
 Number?
PRICE COMPARISON QTY is where law requires that the price comparison that is printed on the shelf label comply with a legally mandated quantity and unit of measure instead of the quantity and unit of measure that the item is packaged in.  The Price Comparison calculation needs sell_qty, sell_uom_code, price_comp_qty and price_comp_uom_cd.  Example:  Item (Flour) - 10 LBS for $1.00  sell_qty: 10  sell_uom_cd: LB  price_comp_qty: 1  price_comp_uom_cd: OZ    The Price Comparison for this item is $.01 per OZ.
 comp_legal_price_uom 
 Code?
PRICE COMPARISON UNIT OF MEASURE CODE.
 never_out_ind 
 Indicator?
Indicates if an item has been designated for the stores to never be out of stock.
 chemical_ind 
 Indicator?
Chemical - any item that is made up of a liquid or powder not intended for human consumption.  Used to determine if Item is a Hazardous Waste if disposed of.
 pesticide_ind 
 Indicator?
Pesticide - product that is advertised or labeled to kill, repel or prevent the growth of any living organism.  Used to determine if Item is a Hazardous Waste if disposed of.
 aerosol_ind
Indicator?
Aerosol - compressed gas or propellant.  Used to determine if Item is a Hazardous Waste if disposed of.
cntrl_sbstnc_ind 
 Indicator?
Controlled substance indicator which may drive functionality on the POS.  (E.g., limit the number thatcna be purchased it a single basket, age verification)
prompt_price_ind 
 Indicator?
Indicator to trigger the POS to prompt the cashier to manually enter a price for an item
 assoc_disc_flag 
 Flag?
Item level flag which determines if the SKU is eligible for associate discounts
 foodstamp_flag 
 Flag?
Item level flag which determines if the SKU can be purchased with food stamps
 shelf_life_days 
 Number?
SHELF LIFE DAYS QTY (TEM SHELF LIFE DAYS) is the minimum number of days that must remain in the life of the product in order to receive it at the store.   NOTE: This data is critical in Grocery DCs for both the receiving and picking functions
 shelf_life_ind 
 Indicator?
The flag which identifies an item as perishable
link_item_nbr 
 SKUItems?
Recursive reference to SKUItem which enables functionality such as linking a warranty item to sellable sku, or linking valve stems to a tire purchase in the auto service center. 
 fsa_flag 
 Flag?
 
 visual_verify_flag 
 Flag?
The flag which triggers the cashier to visually verify the number of items being purchased when the upc of the item is scanned in the POS.
 return_dc_ind
 Indicator?
SKUItem flag which indicates if an item can be returned to a Distribution Center
 diet_type_code 
 Code?
The DIET TYPE CODE represents an food item that is within a particular diet.  Example: Vegetarian or Low Fat.  This was added for ASDA.
 RFID_ind 
 Indicator?
This item is tagged with an RFID chip (Radio Frequency Identifier).
fpp_target_thrwy_rtd_ind 
 Indicator?
Fresh product target throwayaway indicator
fpp_target_thrwy_pct 
 Decimal9?
Target throwawy percentage for fresh production items
fpp_prepn_hr_qty 
 Number?
Conatins the number of hours of preparation a fresh production item takes
shelf_life_hours 
 Number?
Conatines the shelf life for fresh product in hours
pallet_display_ind 
 Indicator?
Indicates if an item can be displayed ona pallet in the store
fpp_retard_range_ind 
 Indicator?
Fresh production planning indicator to describe if a bakery item should be allowed to rise / retard during the baking process



Entity Name
Description
SKUItemInSalesOutlet
The logical entity which defines the valid skuitem to sales outlet relationships.  The SKUItemInSalesOutlet entity contains all attributes of the sku which are location specific.  (E.g. sell price, supply chain attributes which may vary by location)
Attribute
Type
Description
sku_item_nbr 
 SKUItems
The foreign key relationship of SKUItemInStore to SKUItem
store_id 
SaleOutlets
Foreign key to the sales outlet entity
 item_ord_eff_date 
 DateTime?
ITEM ORDER EFFECTIVE DATE is the Date that an item becomes orderable at the store.  The system default for Staple Stock items (types 20, 22, 33, 37, 40, 42 and 50) is next Monday plus 2 weeks from the creation date.  The system default in ASDA is next Monday plus 1 week.  The system default for all other items is today.
item_cost 
 Amount
The current location Item Cost as fed from Home Office systems to Store
sell_price 
 Amount
The Current retail selling price for the location
rtl_notify_store_ind 
 Indicator?
 
price_start_date 
 DateTime
The effective date of the current sell price in store
price_end_date 
 DateTime
The end date of the current sell price in store
price_duration 
 Number
The duration of the price effective window in days.
price_comment 
 Text
Comment text field to describe the location  price
multi_delivery_ind 
 Indicator?
 
earliest_return_date
 DateTime
 
dsd_flag 
 Flag?
Indicates a direct store delivery item
mbm_flag 
 Flag?
 
min_amt 
 Number
The store specific minimum order quantity
max_amt 
 Number
The store specific maximum order quantity
eas_flag 
 Flag?
A flag to indicate that the item has a security surveillance tag
dvd_return_date 
 Date?
DVD's can not be returned through POS until after this date
send_store_date
 DateTime
Date when item should be downloaded to store file
last_pos_date 
 DateTime
Last date the item was sold in this store
promo_ordbk_code 
 Code?
Promotion Order book code value
perform_rating_code 
 Code?
Performance rating code from space planning for this item in the store
item_rplnshbl_ind 
 Indicator?
Idicates if an item is repelnishable to the store
replen_status 
 Code?
T he current replenishment staus for the item
carry_option 
 Code?
Contains the carry option code
max_sale_floor_qty 
 Number?
“max shelf” quantity that should fit on salesfloor (is this shelf capacity now?)
tss_qty 
 Number?
total safety stock or total shelf stock quantity; potentially shelf capacity for an item on the salesfloor
manl_ord_block_ind 
 Flag?
If yes then no manual order allowed, if no then subject to the max pipeline qty rules
max_pipln_ovrd_ind 
 Flag?
max pipeline override indicator 
max_pipeline_qty 
 Number?
maximum quantity allowed in the pipeline (on orders + manual order)



Entity Name
Description
ArticleItem
The logical entity which assigns all of the possible article types and numbers that can be associated to particular merchandise id.  (E.g. Sku to UPC relationships, PACK to GTIN, etc.) 
Attribute
Type
Description
article_id
 Merchandise
The primary key, the unique identifier of an article.
merchandise_item_nbr
 Merchandise
The foreign key to the merchandise entity, the merchandise id number to which the article is assigned.
article_nbr
 Text
The article number, the unique number which is represented as a barcode or PLU number on a SKUItem or PackItem.
article_nbr_type_id
 ArticleTypes
Foreign key to the Articletype entity, the article number type defines the format of the article number (UPC, UPC-8, GTIN, EAN, PLU, ISBN, etc.)
restriction_num
 Number
A code value which is passed to the point of sale system to trigger rules that must be adhered to when a particular barcode is scanned at POS.



Entity Name
Description
ArticleType
ArticleType defines the possible formats of article numbers which are supported by the organization.  It is a single container for all of the barcode types that may be applied any type of merchandise. (UPC, UPC-8, GTIN, EAN, PLU, ISBN, etc.)
Attribute
Type
Description
article_type_id
 Number
Foreign key to the Articletype entity, the article number type defines the format of the article number (UPC, UPC-8, GTIN, EAN, PLU, ISBN, etc.)
article_type_desc
 Text
The long description of the article number type.



Entity Name
Description
Tax
The logical entity which defines the structure of the tax rates which exist within the organization.
Attribute
Type
Description
tax_id 
Number
The primary key, a unique identifier of the tax rate
tax_code 
Code
A code which identifies a tax rate, normally defined by and fed by a external tax rate table
tax_rate 
Number
The tax rate % associated with the tax code
tax_desc 
Text
A description of the tax code
vat_flag 
Flag
The value added tax indicator, if this flag is set to yes then the vat tax rate would be added to the base price of the item in location to determine the customer retail price.



Entity Name
Description
ItemTaxInSalesOutlet
The entity which defines the specific tax components which are applicable to an item in each location.  There can be many tax_ids, or tax rates applied to a single item in a location. (State sales tax, local sales tax, etc.)
Attribute
Type
Description
tax_id 
Tax
The foreign key to the Tax entity
sku_item_in_sales_outlet_id
SKUItemInSalesOutlet
The foreign key to the skuitem in sales outlet entity, which defines the sku to store relationships.  Each item can have a different set of tax id's associated to it depending on the requirement of the tax jurisdiction which apply to a specific sales outlet.



Entity Name
Description
Ingredient
The GSLM entity which supports fresh production planning.  This structure allows SKUITems to be related to each other to support recipes and replenishment of items used for in store food production.
Attribute
Type
Description
sku_item_nbr
 SKUItems
The SKUItem number of the finished product
ingredient_sku_item_nbr
 SKUItems
The SKUItem number of the component or ingredient product
volume_qty
 Number?
The volume of the component used in the production process.
volume_qty_uom
 Code?
The unit of measure associated with the volume quantity (e.g. lbs, oz, kg, mg, etc.)
ingrdnt_qty
 Number?
The number of ingredient sku items 
ingrdnt_qty_uom
 Code?
 



Entity Name
Description
UserDefinedAttribute
The logical construct which allows for custom user defined attributes to be associated with any merchandise type in the GSLM.  The is entity must be closely governed to ensure that it is not abused.  The primary use identified in the GSLM is to provide an entity where cross reference data can be maintained for translating the primary key values of SKUItmes between Walmart and nonconverted systems.
Attribute
Type
Description
uda_id
 Number
The primary key, a globally unique identifier for the UDA
merchandise_type
 MerchandiseType
Foreign key to the merchandise entity, identifies the merchandise that the UDA relates to
uda_desc
 Text
The description of the user defined attribute
data_type
Code?
 Defines the value types which are valid for this UDA. Valid types are NUM, ALPHA, DATE
single_value_ind
 Indicator?
 



Entity Name
Description
UserDefinedAttributeValue
The entity which contains the valid values which are possible for the user defined attribute of the merchandise.
 
Attribute
Type
Description
uda_value_id
 Number
The primary key, a unique identifier for the uda value.
uda_id
 UserDefinedAttributes
Foreign key to the UDA entity, defines the group of related uda values.
uda_value
 Text
The value of the uda that will be assigned to a merchandise id (E.g. the Item xref number)
uda_value_desc
 Text
The description of the value.










Global Store Logical Model – Location



