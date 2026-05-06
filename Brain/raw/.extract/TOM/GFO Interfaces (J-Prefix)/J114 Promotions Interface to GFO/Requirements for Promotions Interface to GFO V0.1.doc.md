
 EMBED Word.Picture.8





Integration Requirements
Promotions Interface from ORMS10 to GFO























Author: Heather Rennoldson
Version: 0.1
Date: 13/02/2007 
Status: Draft

Table of Contents
 TOC \o "1-2" \h \z \t "Appendix,1"  HYPERLINK \l "_Toc159131968" 1.	Introduction	 PAGEREF _Toc159131968 \h 4
 HYPERLINK \L "_TOC159131969" 1.1	Background	 PAGEREF _TOC159131969 \H 4
 HYPERLINK \L "_TOC159131970" 1.2	Issues	 PAGEREF _TOC159131970 \H 4
 HYPERLINK \l "_Toc159131971" 2.	Promotions on ORMS10	 PAGEREF _Toc159131971 \h 5
 HYPERLINK \L "_TOC159131972" 2.1	Overview	 PAGEREF _TOC159131972 \H 5
 HYPERLINK \L "_TOC159131973" 2.2	Processing within ORMS10	 PAGEREF _TOC159131973 \H 6
 HYPERLINK \l "_Toc159131974" 3.	Requirements	 PAGEREF _Toc159131974 \h 7
 HYPERLINK \L "_TOC159131975" 3.1	GFO requirements	 PAGEREF _TOC159131975 \H 7
 HYPERLINK \L "_TOC159131976" 3.2	Assumptions	 PAGEREF _TOC159131976 \H 7
 HYPERLINK \L "_TOC159131977" 3.3	Logic for extracting from ORMS10	 PAGEREF _TOC159131977 \H 7
 HYPERLINK \L "_TOC159131978" 3.4	Additional notes	 PAGEREF _TOC159131978 \H 8
 HYPERLINK \l "_Toc159131979" Appendix A	Promotions File Mappings	 PAGEREF _Toc159131979 \h 9
 HYPERLINK \l "_Toc159131980" Appendix B	Glossary of Terms	 PAGEREF _Toc159131980 \h 10
Document Control

Project:
Operating Model – Integration 
Document Title:
Requirements Definition
Document Location:
Docshare


Distribution:
Lewis Stewart
Nuno Carvalho
Miles Thomas
Adrian Hinks
Allistair Green
Nikhil Rajwade
GFO
)
)
)TOM Integration team
)
)



Change Record

Date
Version
Change Description
Author
09/02/2007
0.1
Initial Draft
Heather Rennoldson

References

Document
Version
Date
Author
























Introduction
Background

The purpose of this document is to confirm the business requirements for the promotions interface from ORMS10 to Group, Forecast & Order (GFO) for Turkey. The information is based on the requirements for the GFO Promotions Interface file mappings (see Appendix A) and conversations with the GFO team.

This covers the requirements for interfaces C010TR (Promotion Data ORMS10 to IDS) and J114 (Promotion Data IDS to GFO). 
  
Promotions are structured in a different manner within ORPM12, so the GFO requirements for this data will be documented separately., although the ultimate receiving file/table will be the same. 

Issues
The architects need to define the technical detail of whether it is necessary to persist  promotions data in the IDS.
GFO is the first customer of the data. Space, Range and Display will also require promotion information, but the detail is not known yet.
The IDS has been designed for the ORPM12 view of promotions, and so would require a different ‘build’ for ORMS10.

Promotions on ORMS10
Overview


 EMBED Visio.Drawing.11  


The diagram above portrays how ORMS10 holds promotion details within its tables.
 Note: only tables pertinent to the GFO requirements are shown.

Table
Description
PROMHEAD
This holds the major promotional information – promotion, promotion_name, start and end dates. A promotion can be one of 4 types – mix match (aka buy-get), threshold, simple, departmental 
PROM_MIX_MATCH_HEAD
This describes the mix/match promotion. In ORMS terms there is a ‘buy list’ and a ‘get list’ and the customer has to buy any or all the items in the ‘buy list’ to get a discount on the items in the ‘get list’. This is similar to the UK Linksave promotion.
PROM_MIX_MATCH_BUY
This contains the ITEM (base product) in the buy list
PROM_MIX_MATCH_GET
This contains the ITEM (base product) in the get list
PROM_THRESHOLD_HEAD
In this promotion type the customer has to purchase a threshold number of a product to obtain a discount. This can be at product or at departmental level.
 This is similar to the UK Multisaver.
PROM_THRESHOLD_SKU
This contains the SKUs in the threshold promotion
PROM_THRESHOLD_DEPT
This contains the department or class or subclass included in a threshold promotion – and will therefore apply to all products in that grouping.
This is not being used in Turkey, since it does not map to the Storeline view of promotions.
PROMSKU
This is used for a simple promotion – money off, percentage off or fixed price promotion and this table contains all the ITEMs included in that promotion.
PROMDEPT
This is also used for a simple promotion – and is linked to all items in the subclass

Processing within ORMS10
Departmental promotions
Unlike UK subgroup promotions, the departmental promotions (PROMDEPT and PROM_THRESHOLD_DEPT) are cascaded to item level before the promotion is downloaded to the Point of Sale system. This normally happens on the day that the promotions information is transmitted to the POS system. 

This results in the PROM_THRESOLD_SKU and PROMSKU tables, respectively, being populated with the details, but the PROM_THRESHOLD_DEPT and PROMDEPT tables will still exist alongside.

Having exploded the departmental promotions to item level, it is not possible for the user to subsequently update the PROMDEPT and PROM_THRESHOLD_DEPT tables. Any amendments by the user are mad to the PROMSKU table.
 (Note that Turkey does not use the PROM_THRESHOLD_DEPT promotions).

Promotion Status
The promotion can move through different statuses: 
W=Worksheet
S=Submitted (for approval)
A=Approved
R=Rejected (after being submitted)
C=Cancelled
D=Deleted (to be deleted)
M =Completed
E=Extracted
I = submittal, approval in progress

Promotions can swap from approved back to worksheet status, ahead of the promotion being extracted.

Linking promotions to stores (not pertinent for GFO – just for information)
Having defined the promotion ORMS10 can then link it to a group of stores. This information is captured in the PROMSTORE table, and then this is used in the POS download process.

The start and end dates for the promotion can be changed at the promotion-store level, but must fall within the overall promotion start and end dates.

Requirements
GFO requirements
1. GFO require a Promotions interface provided daily (probably c 2200hrs but requires confirmation).

2. This will contain details of all SKUs on promotion currently and at any time in the next 31 days.
GFO are only interested in promotions in the approved or executed status.

3. GFO requires that departmental promotions are expanded to the SKU level on this interface.

4. GFO requires a complete file every day – not deltas.
Assumptions
Within ORMS, it appears to be possible for a promotion to include different promotion types e.g. PROMSKU and PROM_MIX_MATCH_HEAD can be held under the same PROMHEAD. In this design, it has been assumed that the business do not mix promotions of different types under the same header.

It is also possible for the PROMSKU, PROM_MIX_MATCH_GET_ITEM, and PROM_MIX_MATCH_BUY_ITEM to be linked to a transaction level item or the parent SKU item level (i.e. Style) with / without a DIFF specified. For example, at a transaction level, the user would select Red, Size 10 T shirt, at Style / Diff, the user would select Red T-shirt (and then all the different sizes for the red T shirt would be included in the promotions)  and Style level the user would select ‘T shirt’ (and all colour/size combinations would be included). It is again assumed that the business only link to the transaction level item.
Logic for extracting from ORMS10

Extract all PROMHEAD .PROMOTION, PROMHEAD.PROM_NAME, PROMHEAD.START_DATE and PROMHEAD.END.DATE where PROMHEAD.START_DATE is <= control date + 31 days and PROMHEAD.END_DATE is >= control date and PROMHEAD.STATUS = ‘A’ (approved) or ‘E’ (extracted).
(I assume that the control date will actually be ‘tomorrow’, since GFO is receiving a file tonight for action tomorrow)
.
The following paragraphs indicate how to identify the items in the promotion;

Match PROMHEAD.PROMOTION against PROM_THRESHOLD_SKU.PROMOTION, and PROM_THRESHOLD_SKU.ITEM respectively. 
Note:
there won’t always be an entry in this table
this promotion is a ‘Threshold’ promotion.

Similarly, match PROMHEAD.PROMOTION against PROM_MIX_MATCH_BUY.PROMOTION, and PROM_MIX_MATCH_GET.PROMOTION and extract PROM_MIX_MATCH_BUY.ITEM and PROM_MIX_MATCH_GET.ITEM respectively. 
Note:
there won’t always be an entry in these tables
this promotion is a ‘Buy-Get’ promotion.

Then match PROMHEAD.PROMOTION against PROMDEPT.PROMOTION. For any matches, check for the existence of the same promotions in the PROMSKU tables.

If a match is found here, it can be assumed that the department promotion has already been exploded to the item level, so capture all PROMSKU.ITEM, and note this as a departmental promotion.
If no match is found, the departments in the promotion need to be exploded to the transaction items. This will be achieved by matching: the DEPT, CLASS and SUBCLASS on the PROMDEPT table against the same fields on ITEM_MASTER, where ITEM_MASTER.ITEM_LEVEL = 2 and PACK_IND = Y .DEPT. The ITEM_MASTER.ITEM fields will be the sellable transaction level items within the subclass. Note as a departmental promotion.

Then match PROMHEAD.PROMOTION against PROMSKU.PROMOTION (but exclude any promotions which have already been identified as departmental promotions above), and extract all PROMSKU.ITEM. 

Additional notes
Since a promotion can transfer from approved back to worksheet status, it is possible that a promotion will disappear from the file, before the promotion is extracted.


  
 Promotions File Mappings

GFO Integration Layer Promotions File

ORMS10 Source




Data ItemData TypeData LengthFixed DataData Format TableData ItemData TypeData LengthNotes?JIPMA-RECORD-TYPENUMERIC2"00"       JIPMA-DATECHAR  CCYYMMDD      FILLERCHAR SPACES       JIPMB-RECORD-TYPENUMERIC2"01"       JIPMB-BASE-PRODUCT-NOCHAR9   Various.
See section 3ITEMVARCHAR225FILLERNUMERIC5ZEROES       FILLERCHAR1SPACES       JIPMB-PROMOTION-STARTNUMERIC8 CCYYMMDD PROMHEADSTART_DATEDATE?JIPMB-PROM-END-DATENUMERIC8 CCYYMMDD PROMHEADEND_DATEDATE?JIPMB-BPR-UPLIFT-PERCNUMERIC8ZEROES+/-9999999      FILLERCHAR1SPACES       FILLERCHAR48SPACES       JIPMB-OFFER-IDCHAR9   PROMHEADPROMOTIONNUMBER10JIPMB-OFFER-DESCCHAR50   PROMHEADNAMEVARCHAR240JIPMB-OFFER-BUKT-REQDCHAR1   ????Will be set to ‘N’JIPMB-FEATURE-SPCE-DISPCHAR1"Y"       JIPMB-BPR-REGNCHAR2"00"       JIPMB-AREA-CDCHAR1"1"       JIPMB-OFFER-TYPECHAR3   ????Will be departmental, buy-get, threshold or SKU. GFO team to specify the mnemonic required.   FILLERCHAR84SPACES       JIPMZ-RECORD-TYPENUMERIC2"99"       FILLERCHAR241SPACES       JIPMZ-REC-COUNTNUMERIC7        


Glossary of Terms

Mnemonic
Description
GFO
Group Forecast & Order
IDS
Integration Data Store
ORMS
Oracle Retail Management System
ORPM
Oracle Retail Price Management
POS
Point of Sale
RIB
Retek Integration Bus











	 Integration Team: Requirements Definition




PAGE  


Date: 13/02/2007, Version0.1		Page  PAGE 3 of  NUMPAGES 10
Author : Heather Rennoldson


	
Integration Team : Requirements Definition







Date: 13/2007, Version 0.1		Page  PAGE 2 of  NUMPAGES 10
Author : Heather Rennoldson







 EMBED Word.Picture.8  







