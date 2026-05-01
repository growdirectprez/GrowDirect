1. Merchandise Hierarchy
   1. Business Division

Level 1 of the merchandise hierarchy representing major segments of a trading company’s business (e.g. General Merchandise, Food, and Automotive)

|  |  |  |
| --- | --- | --- |
| Entity Name | BusinessDivision | |
|  | | |
| Attribute | Type | Description |
| business\_div\_id | Number |  |
| business\_div\_desc | Text |  |

* 1. Department

Level 2 of the merchandise hierarchy, it is a single entity containing the two hierarchy levels currently known as accounting department and order department. Accounting and order departments have been collapsed into a single entity because order department was created due to a system constraint causing accounting departments to run out of available item numbers. There was no logical or business need and the Global Store Logical model (GSLM) is not constrained in the same manner.

|  |  |  |
| --- | --- | --- |
| Entity Name | Department | |
|  | | |
| Attribute | Type | Description |
| dept\_nbr | Number |  |
| acctg\_dept | Text? |  |
| dept\_desc | Text |  |
| business\_division | BusinessDivision | Refers to the parent BusinessDivision of the Department |

* 1. Section

Level 3 of the merchandise hierarchy, Section is an additional level added to the GSLM to support integration with new retail companies who might have additional levels in their existing hierarchy.

|  |  |  |
| --- | --- | --- |
| Entity Name | Section | |
|  | | |
| Attribute | Type | Description |
| section\_id | Number |  |
| section\_desc | Text |  |
| department | Department |  |

* 1. Class

Level 4 of the merchandise hierarchy, Class is an additional level added to the GSLM to support integration with new retail companies who might have additional levels in their existing hierarchy.

|  |  |  |
| --- | --- | --- |
| Entity Name | Class | |
|  | | |
| Attribute | Type | Description |
| class\_id |  |  |
| class\_desc |  |  |
| section | Section |  |

* 1. Subclass

Level 5 of the merchandise hierarchy, Class is an additional level added to the GSLM to support integration with new retail companies who might have additional levels in their existing hierarchy.

|  |  |  |
| --- | --- | --- |
| Entity Name | Subclass | |
|  | | |
| Attribute | Type | Description |
| subclass\_nbr | Number |  |
| subclass\_desc |  |  |
| Class | Class |  |

* 1. Fineline

Level 6 of the merchandise hierarchy, the GSLM fineline is a unique identifier composed of the current Walmart subclass and fineline (e.g. 24-3706). It is the level of the hierarchy where the Item structure is attached.

|  |  |  |
| --- | --- | --- |
| Entity Name | FineLine | |
|  | | |
| Attribute | Type | Description |
| fineline\_nbr | Number |  |
| fineline\_desc |  |  |
| subclass | SubClass |  |

1. Item
   1. Merchandise

Merchandise is a logical entity that groups multiple items types into a single container. It enables the ability to create attributes with multiple values across which are common cross item type. (E.g. creating item descriptions in multiple languages)

|  |  |  |
| --- | --- | --- |
| Entity Name | Merchandise | |
|  | | |
| Attribute | Type | Description |
| merchandise\_id | Number |  |
| merchandise\_type | Text |  |

* 1. MerchandiseAttributeInCountry

A logical entity which contains localized attributes across item type (e.g. shelf label fields by country)

|  |  |  |
| --- | --- | --- |
| Entity Name | MerchandiseAttributeLanguage | |
|  | | |
| Attribute | Type | Description |
| merchandise\_id | Merchandise |  |
| language\_code | Text? |  |
| shop\_desc | Text? |  |
| signing\_desc | Text? |  |
| shelf\_lbl\_size\_desc | Text? |  |
| shelf\_lbl\_colour\_desc | Text? |  |
| upc\_desc | Text? |  |
| item\_desc1 | Text? |  |
| item\_desc2 | Text? |  |
| country\_code | Code |  |

* 1. Style

Style is a logical grouping of like items with varying characteristics that are considered a single merchandising entity. The concept of style relates to the Walmart variant, it is a retail industry standard commonly used in apparel for mass sku creation sku items which vary by a predefined set of dimensions, and are tracked as separate units from an inventory standpoint. This has been added to create an item template structure which is common across the industry and a core component of most Retail ERP systems.

|  |  |  |
| --- | --- | --- |
| Entity Name | Style | |
|  | | |
| Attribute | Type | Description |
| Style\_id | Merchandise |  |
| fineline | Finelines |  |

* 1. SKUItem

The core logical entity which describes the stock keeping unit and the distinct merchandise unit that can be purchased by the consumer. It is the level at which merchandising and replenishment processes track inventory. In the GSLM the SKUItem record does not contain supply chain specific information (e.g. pack details or vendor data). The GSLM does not require multiple records for a single consumer unit as required in the current state.

|  |  |  |
| --- | --- | --- |
| Entity Name | Subclass | |
|  | | |
| Attribute | Type | Description |
| sku\_item\_nbr | Merchandise |  |
| style | StyleVariantGroups |  |
| base\_item | SKUItems? |  |
| consumer\_item\_nbr | Number? |  |
| item\_status\_code | Code? |  |
| item\_create\_date | DateTime? |  |
| item\_ord\_eff\_date | DateTime? |  |
| item\_expire\_date | DateTime? |  |
| send\_store\_date | DateTime? |  |
| variable\_wt\_ind | Indicator? |  |
| backroom\_scale\_ind | Indicator? |  |
| temp\_sensitive\_ind | Indicator? |  |
| account\_nbr | Text(50)? |  |
| account\_nbr\_type\_code | Code? |  |
| base\_unit\_rtl\_amt | Amount? |  |
| base\_rtl\_uom\_code | Code? |  |
| sell\_qty | Number? |  |
| sell\_qty\_uom | Code? |  |
| item\_scanable | Indicator? |  |
| shelf\_rotation\_ind | Indicator? |  |
| guar\_sales\_ind | Indicator? |  |
| mfgr\_sugd\_rtl\_amt | Amount? |  |
| mfgr\_pre\_price\_amt | Amount? |  |
| brand\_id | Text? |  |
| variable\_comp\_ind | Indicator? |  |
| mdse\_catg\_nbr | Number? |  |
| mdse\_subcatg\_nbr | Number? |  |
| sell\_package\_qty | Number? |  |
| sell\_unit\_qty | Number? |  |
| sell\_unit\_uom | Code? |  |
| comp\_shop\_package\_qty | Number? |  |
| comp\_shop\_unit\_qty | Number? |  |
| comp\_legal\_price\_qty | Number? |  |
| comp\_legal\_price\_uom | Code? |  |
| never\_out\_ind | Indicator? |  |
| chemical\_ind | Indicator? |  |
| pesticide\_ind | Indicator? |  |
| aerosol\_ind | Indicator? |  |
| assoc\_disc\_flag | Flag? |  |
| foodstamp\_flag | Flag? |  |
| shelf\_life\_days | Number? |  |
| shelf\_life\_ind | Indicator? |  |
| warranty\_item\_nbr | SKUItems? |  |
| fsa\_flag | Flag? |  |
| visual\_verify\_flag | Flag? |  |
| return\_dc\_ind | Indicator? |  |
| diet\_type\_code | Code? |  |
| RFID\_ind | Indicator? |  |

* 1. ArticleItem

The logical entity which holds the relationship of Items to one or more reference articles defined by the BarcodeType entity. (E.g. UPC, PLU, EAN, GTIN).

|  |  |  |
| --- | --- | --- |
| Entity Name | Class | |
|  | | |
| Attribute | Type | Description |
|  |  |  |
|  |  |  |
|  |  |  |

* 1. PackItem

A logical entity which represent the orderable unit which can be received at store. The pack item is separate from the stock keeping item, and may contain multiple units of an SKU. The GSLM PackItem correlates to the current entities known as vendor pack, warehouse pack, and assortment item.

|  |  |  |
| --- | --- | --- |
| Entity Name | Class | |
|  | | |
| Attribute | Type | Description |
|  |  |  |
|  |  |  |
|  |  |  |

* 1. PackItemBreakout

The logical construct which defines the many to many relationships between SKUItem and PackItem. Skus may exist in more than one pack, and conversely packs may contain more than one sku. In the GSLM a sellable item which is also orderable, will have a separate logical record in the SKUItem and PackItem entities.

|  |  |  |
| --- | --- | --- |
| Entity Name | Class | |
|  | | |
| Attribute | Type | Description |
|  |  |  |
|  |  |  |
|  |  |  |

* 1. OuterCase

A logical entity which contains the scannable barcodes which are associated with a PackItem. It allows for multiple barcode types to be assigned to a single pack.

|  |  |  |
| --- | --- | --- |
| Entity Name | Class | |
|  | | |
| Attribute | Type | Description |
|  |  |  |
|  |  |  |
|  |  |  |

* 1. BarcodeNumberType

A logical entity which defines the possible barcode types which can be assigned to a pack in the OuterCase entity.

|  |  |  |
| --- | --- | --- |
| Entity Name | Class | |
|  | | |
| Attribute | Type | Description |
|  |  |  |
|  |  |  |
|  |  |  |

1. Vendor
   1. Vendor

The logical entity where vendor master records are held in the GSLM. It contains the subset of vendor attributes which are required for store processes.

* 1. SKUItemVendor

The logical entity which defines the relationship between a sku and the vendors which supply the sku. This construct allows multiple vendors to be assigned as suppliers of a single item. Although not used in the current state, this structure can reduce the number of item records required in the model, and could provide for better integration with ERP systems.

* 1. SKUItemVendorVarients

A cross reference between the various physical traits of an item as described in the Variants entity and the SKUItem provided by the vendor. This entity allows for a single SKUItem to have many variant versions of the product (for example, small, medium and large t-shirts all under one SKU)

* 1. Variants

This entity provides the physical description of variant items, attributes such as size, color etc. Typically used for apparel merchandise.

1. Location
   1. Store

The logical entity which contains store master records

* 1. StoreDepartment

The logical entity which describes the valid store operations departments which are assigned to the store. (E.g. grocery, automotive)

* 1. StoreHolidayCalendar

The logical entity which contains the store’s operating calendar, it defines the dates and reasons when a store is closed.

* 1. SKUItemInStore

The logical entity which defines the range of SKUItems which are assigned to a store. The SKUItemInStore entity contains all attributes of the sku which are location specific. (E.g. sell price, supply chain attributes which may vary by location)

* 1. PackItemInStore

The logical entity which defines the relationship between PackItem and location. PackItemInStore enables location specific ordering packs to be created for a single SKUItem. (E.g. large stores receive an item in pallets, and small stores receive a case or regional differences where multiple vendors supply packs to store based on their location)

* 1. ItemTaxInStore

The entity which hold the cross reference between the SKUItemInStore table and the taxes which are applicable at that location. There may be multiple taxes on any item in any store.

* 1. Taxes

The entity that holds the tax rates which may be applied to an item.