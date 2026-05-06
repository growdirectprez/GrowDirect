Introduction

The purpose of this paper is to describe how items will be set up in ORMS, with particular reference to attributes required to derive the Supply Authority data for GFO. This excludes aspects not required for the GFO Supply Authority interface e.g. retail and cost price, and store location links..

Note this paper does not cover:
the issue of approved products. It is possible that a SKU will be approved before a pack is approved, so the pack details will not be available in the IDS. We might therefore need to exclude SKUs without related packs from the GFO base product interface.
 deposit items which will be set up as complex packs – and for the purposes of GFO, only the contents SKU (and not the bottle) should be included in the interface.
complex packs in the form of ratio packs

It is broken down into two  parts – the first gives the background into how the user will be setting up product details in ORMS; the second section goes through an example of how the tables will be populated and how the Supply Authority for GFO will be derived. 

Setting up a product in ORMS

1. Create a style

a) Create a Style with basic details.
b) Link the Style to a supplier (or number of suppliers) and identify a primary supplier.
c) For each style-supplier, identify origin counties, and for each country, specify a case size and identify a primary country.  (Note: in practice there is only one country which will be associated with an Item-Supplier, but coding in the Integration layer should allow for multiple countries). 
d) This data will populate the ITEM_MASTER, ITEM_SUPPLIER & ITEM_SUPP_COUNTRY tables.
e) In addition, it is necessary to populate retail price zones and links to locations before moving to the next stage. 


 EMBED Visio.Drawing.11  




2. Create the SKU

a) Create the child SKU(s) from Style.
b) It is possible, but not mandatory, to cascade the supplier and supplier-country data from Style to SKU (and similarly retail price and location data).
c) So, the Suppliers and Supplier-Countries linked to the SKU do not need to bear any relationship to the supplier related data set up at Style level. (Note from HR: I don’t believe this is too critical, one can view Style as primarily a quick way for setting up similar products. Having set the products up, it is the SKU which drives the on-going processing)
d) This data will populate the ITEM_MASTER, ITEM_SUPPLIER & ITEM_SUPP_COUNTRY tables
e) Now need to link the SKU to the DC locations which will stock it. (Note SKU will also be linked to store locations but this is not being covered in this document since not required for Supply Authority). This will set up the ITEM_LOC record. Within this, it is possible for the user to identify the primary supplier for the location. If this field is not set, it will default to the primary supplier flagged  against SKU-Supplier. 


















3. Create an EAN

a) Create the child EAN(s) from SKU. It is possible to give an EAN its own description (different from the SKU description)).
b) It is possible, but not mandatory, to cascade supplier data from SKU to EAN.
c) If not automatically cascaded, suppliers (already associated with the SKU) can be linked directly to the EAN.
d) There does not appear to be any way of linking a supplier in country to an EAN.
e) This data will populate the ITEM_MASTER & ITEM_SUPP.
 

 EMBED Visio.Drawing.11  


4. Create a Simple Pack 
Note: deposit items will be set up within complex packs (not simple packs …and have to be worked)

a) Create the Simple Pack from the SKU – the screen automatically populates the preferred supplier and preferred country for the SKU.
b) An ‘Item Quantity’ (i.e. number of SKUs in the pack) and a cost has to be provided but this does not have to match to the ‘supplier pack size’ and cost specified for the SKU item. The Simple Pack Number, SKU Number and Item Quantity is used to populate the PACKITEM table. An entry will also be created in ITEM_MASTER for the Simple Pack. 
c) The user has the option to cascade suppliers from the SKU to the Simple Pack.
 If the option is selected, all the suppliers’ information from the SKU will be used to create ITEM_SUPPLIER and ITEM_SUPP_COUNTRY entries for the Pack.
If the option is not selected, only the preferred supplier and preferred supplier in country data will be used to create ITEM_SUPPLIER and ITEM_SUPP_COUNTRY entries for the Pack.
 The user can enter a different pack size for the Simple Pack to that defined for its related SKU.
d) Additional suppliers can be linked to the pack, but these are restricted to those already linked to the SKU….. (but I don’t seem to be able to do this at the moment!)
e) OCCs are set up as ‘children’ of the packs – again creating ITEM_MASTER entries, and there would be a link between OCC and supplier (as with EAN), but this is not shown on the diagram.

 EMBED Visio.Drawing.11  




ORMS Table Contents
This section indicates how we would expect to see the ORMS tables populated for a relatively simple product (for purposes of GFO)..

Example product:

 EMBED Visio.Drawing.11  

Only the principal attributes are shown in the tables below.

1.ITEM_MASTER Table

ITEMITEM_DESCPACK_
INDITEM_
LEVELTRAN_
LEVELSIMPLE_
PACK_INDITEM_
PARENTITEM_
GRANDPARENTStyle123456789Men’s T ShirtN12NSKU234567890Men’s T Shirt Black Small N22N123456789EAN512346789012Men’s T Shirt Black SmallN32N234567890123456789Pack345678901Men’s T Shirt Black SmallY11YOCC52345678901234Men’s T Shirt Black SmallY21Y345678901

2.ITEM_SUPPLIER Table


ITEM
SUPPLIER
PRIMARY_SUPP_IND
Style
123456789
12345
Y
SKU
234567890
12345
Y
EAN
512346789012
12345
Y
Pack
345678901
12345
Y
OCC
52345678901234
12345
Y


3.ITEM_SUPP_COUNTRY Table


ITEM
SUPPLIER
ORIGIN_COUNTRY_ID
SUPP_PACK_SIZE
PRIMARY_LOC_IND
PRIMARY_SUPP_IND
Style
123456789
12345
US
5
Y
Y
SKU
234567890
12345
US
5
Y
Y
Pack
345678901
12345
US
5
Y
Y

Note that:
(a) PRIMARY_SUPP_IND appears to be cascaded down from the ITEM_SUPPLIER
(b) I have assumed that there will be no entry on this table for the EAN (because I can’t see a screen for it… but who knows what ORMS is doing behind the scenes!)
(c) there is nothing in ORMS  to enforce the rule that the SUPP_PACK_SIZE for the SKU and for the pack will be consistent.  

4. ITEM_ LOC Table


ITEM
LOC
PRIMARY_SUPPLIER
SKU
234567890
123
Nulls

Note that there would be additional rows to link the SKU to the store locations, and additional details captured such as retail and cost prices but these are not shown in this example since they are not relevant for deriving Supply Authority.

5. PACKITEM Table

PACKNO
ITEM
(SKU)
PACK_QTY
345678901
234567890
5

There is nothing in ORMS to enforce that the Pack Quantity matches the Supplier Pack Size entered on the ITEM_SUPP_COUNTRY table for the Pack..


Derivation of Supply Authority

The BSD for Supply Authority specifies the rules for deriving this.

GFO needs to be provided with a file containing all SKUs (TPNBs) and their links to:
suppliers and the associated packs (TPNDs), which GFO will use as a basis for ‘Directs’
DCs (which stock the SKU) and the associated packs (TPNDs)

Worked example
I have amended the example in the previous section to give a better example for the derivation rules. 

I have added:
(a) another supplier (23456) for  the Style, SKU, EAN  and original pack & OCC
(b) another pack (456789012) & OCC (53456789012345) with a different pack size, of 12,  related to the new supplier (23456)
(c) have added some other countries for ‘supplier in country’ records  


1.ITEM_MASTER Table

ITEMITEM_DESCPACK_
INDITEM_
LEVELTRAN_
LEVELSIMPLE_
PACK_INDITEM_
PARENTITEM_
GRANDPARENTStyle123456789Men’s T ShirtN12NSKU234567890Men’s T Shirt Black Small N22N123456789EAN512346789012Men’s T Shirt Black SmallN32N234567890123456789Pack345678901Men’s T Shirt Black SmallY11YOCC52345678901234Men’s T Shirt Black SmallY21Y345678901Pack456789012Men’s T Shirt Black SmallY11YNew packOCC53456789012345Men’s T Shirt Black SmallY21Y456789012New OCC

2.ITEM_SUPPLIER Table


ITEM
SUPPLIER
PRIMARY_SUPP_IND

Style
123456789
12345
Y

SKU
234567890
12345
Y

EAN
512346789012
12345
Y

Pack
345678901
12345
Y

OCC
52345678901234
12345
Y

Style
123456789
23456
N
New supplier attached to Style
SKU
234567890
23456
N
New supplier attached to SKU
EAN
512346789012
23456
N
New supplier attached to EAN
Pack
345678901
23456
N
New supplier attached to original pack
OCC
52345678901234
23456
N
New supplier attached to original OCC
Pack
456789012
23456
Y
New supplier attached to new pack
OCC
53456789012345
23456
Y
New supplier attached to new OCC


3.ITEM_SUPP_COUNTRY Table


ITEM
SUPPLIER
ORIGIN_COUNTRY_ID
SUPP_PACK_SIZE
PRIMARY_LOC_IND
PRIMARY_SUPP_IND

Style
123456789
12345
US
5
Y
Y

Style
123456789
12345
GB
5
N
Y
Country added
SKU
234567890
12345
US
5
Y
Y

SKU
234567890
12345
GB
5
N
Y
Country added
Pack
345678901
12345
US
5
Y
Y

Pack
345678901
12345
GB
5
N
Y
Country added
Style
123456789
23456
US
5
Y
N
New supplier
Style
123456789
23456
GB
12
N
N
New supplier
SKU
234567890
23456
US
5
Y
N
New supplier
SKU
234567890
23456
GB
12
N
N
New supplier
Pack
345678901
23456
US
5
Y
N
New supplier
Pack
345678901
23456
GB
5
N
N
New supplier
Pack
456789012
23456
US
12
Y
Y
New pack & supplier
Pack
456789012
23456
GB
12
N
Y
New pack & supplier

Note: 
a) PRIMARY_LOC_IND indicates the ‘primary country’ for the ITEM-SUPPLIER

b) The two packs are both supplied by supplier 23456 and have different pack sizes for the same country (US). However, the  SKU row for supplier 23456  and country of US can only have one pack size associated with it. In this example, I have assumed that the user has defined this to be a pack size of 5. 

4.ITEM_ LOC Table


ITEM
LOC
PRIMARY SUPPLIER

SKU
234567890
123
Nulls

SKU
234567890
456
23456
New location 

This table indicates that the primary supplier in DC 123, for the SKU will be the ‘default’ supplier for that SKU, but the primary supplier for DC 456 will be 23456. 


5. PACKITEM Table

PACKNO
ITEM
(SKU)
PACK_QTY

345678901
234567890
5

456789012
234567890
12
New pack

This is used in identifying the relationship between SKU and pack

Derivation

A simple view of the principal entities, SKU and Packs, and their relationships to supplier is shown in the diagram below. 

 EMBED Visio.Drawing.11  


1. For each SKU (TPNB) we need to obtain all its suppliers, and for each of these suppliers obtain the supplier’s preferred pack number (TPND), so that on the output record we create one record for each SKU/Supplier combination.

a) Obtain the preferred pack size for each  SKU-Supplier. 
Access the ITEM_SUPP_COUNTRY table to extract the records for the primary location (country) for each SKU-supplier.  Only one row for each SKU-supplier will be returned. This will then give us the ‘default’ supplier pack size.

We then obtain:

ITEM
SUPPLIER
ORIGIN_COUNTRY_ID
SUPP_PACK_SIZE
PRIMARY_LOC_IND
PRIMARY_SUPP_IND

SKU
234567890
12345
US
5
Y
Y

SKU
234567890
23456
US
5
Y
N
New supplier

b). Access the related packs for the SKU through the PACKITEM table:

PACKNO
ITEM
PACK_QTY

345678901
234567890
5

456789012
234567890
12
New pack

c) Obtain the preferred pack size for each Packitem-Supplier 
Access the ITEM_SUPP_COUNTRY table to extract the records for the primary location (country) for each Pack -supplier.  Only one row for each Pack-supplier will be returned. This will then give us the ‘default’ supplier pack size. This is similar to the process in (a)


ITEM
SUPPLIER
ORIGIN_COUNTRY_ID
SUPP_PACK_SIZE
PRIMARY_LOC_IND
PRIMARY_SUPP_IND

Pack
345678901
12345
US
5
Y
Y

Pack
345678901
23456
US
5
Y
N
New supplier
Pack
456789012
23456
US
12
Y
Y
New pack&supplier

Note that this has returned two possible pack sizes for supplier 23456.

d) Then to finally obtain the preferred pack for a SKU-supplier, match on supplier & supplier pack size from the results in (a) and (c) to obtain the correct pack:

SKU ITEM (TPNB)
SUPPLIER
SUPP_PACK_SIZE
PACK ITEM
(TPND)
234567890
12345
5
345678901
234567890
23456
5
345678901

The pack 456789012 (with a pack size of 12), has not been selected because this pack size has not been identified as a preferred pack size of the SKU.

Note that since the pack size set up for the Pack can be entirely different from that set up for the SKU, it is possible that a match will not be found! (Might need to build a work around for this scenario).

2. For each SKU (TPNB) we need to obtain all DCs that stock the product, and for each of these DCs obtain the  preferred pack number (TPND), so that on the output record we create one record for each SKU/DC combination.

a) Extract all records for a SKU  item and a DC locations from the ITEM_LOC table:
(This will be where LOC_TYPE = that of the warehouse)


ITEM
LOC
PRIMARY_SUPP


234567890
123
Nulls


234567890
456
23456
New location 

b) Where the PRIMARY_SUPP is populated in the ITEM_LOC table, look-up against the ITEM_SUPP_COUNTRY table to obtain the ‘primary country’ record for the SKU and supplier  to obtain the SUPP_PACK_SIZE. Only 1 record should be identified.:
For location 456, this will return: 

ITEM
SUPPLIER
ORIGIN_COUNTRY_ID
SUPP_PACK_SIZE
PRIMARY_LOC_IND
PRIMARY_SUPP_IND
SKU
234567890
23456
US
5
Y
N

Where the PRIMARY_SUPPLIER is not populated, look-up against the ITEM_SUPP_COUNTRY record for the SKU where PRIMARY_LOC_IND = Y and PRIMARY_SUPP_IND = Y. 
For location 123, this will return:


ITEM
SUPPLIER
ORIGIN_COUNTRY_ID
SUPP_PACK_SIZE
PRIMARY_LOC_IND
PRIMARY_SUPP_IND
SKU
234567890
12345
US
5
Y
Y

d) We now need to identify the pack relating to this SKU/ Supplier following the same rules as in 1 (b), 1 (c) and 1 (d). This will identify the ‘preferred pack (TPND) ’ in both instances being 345678901.

SKU ITEM (TPNB)
DC
SUPP_PACK_SIZE
PACK ITEM
(TPND)
234567890
123
5
345678901
234567890
456
5
345678901


3.  Combining the Directs suppliers and the DC  information

The resultant GFO file will show:

TPNB
TPND
Unit Size
Stock centre

234567890
345678901
5
12345
Stock centre = supplier number
234567890
345678901
5
23456
Stock centre = supplier number
234567890
345678901
5
123
Stock centre = Location
234567890
345678901
5
456
Stock centre = Location



 EMBED Visio.Drawing.11  






