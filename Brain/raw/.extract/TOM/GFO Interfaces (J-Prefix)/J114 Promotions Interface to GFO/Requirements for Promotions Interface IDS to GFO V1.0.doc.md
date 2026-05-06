
 EMBED Word.Picture.8





Integration Requirements
Promotions Interface (J114) from IDS to GFO
























Author: Heather Rennoldson
Version: 1.0
Date: 09/03/2007 
Status: Final

Table of Contents
 TOC \o "1-2" \h \z \t "Appendix,1"  HYPERLINK \l "_Toc161023465" 1.	Introduction	 PAGEREF _Toc161023465 \h 3
 HYPERLINK \L "_TOC161023466" 1.1	Background	 PAGEREF _TOC161023466 \H 3
 HYPERLINK \L "_TOC161023467" 1.2	Issues	 PAGEREF _TOC161023467 \H 3
 HYPERLINK \l "_Toc161023468" 2.	Promotions in the IDS	 PAGEREF _Toc161023468 \h 3
 HYPERLINK \L "_TOC161023469" 2.1	Overview	 PAGEREF _TOC161023469 \H 3
 HYPERLINK \l "_Toc161023470" 3.	Requirements	 PAGEREF _Toc161023470 \h 3
 HYPERLINK \L "_TOC161023471" 3.1	GFO requirements	 PAGEREF _TOC161023471 \H 3
 HYPERLINK \L "_TOC161023472" 3.2	Logic for extracting from the IDS	 PAGEREF _TOC161023472 \H 3
 HYPERLINK \L "_TOC161023473" 3.3	Additional notes	 PAGEREF _TOC161023473 \H 3
 HYPERLINK \l "_Toc161023474" Appendix A	Promotions File Mappings	 PAGEREF _Toc161023474 \h 3
 HYPERLINK \l "_Toc161023475" Appendix B	Glossary of Terms	 PAGEREF _Toc161023475 \h 3
Document Control

Project:
Operating Model – Integration 
Document Title:
Requirements Definition
Document Location:
Docshare


Distribution:
Lewis Stewart
Adrian Hinks
Allistair Green
Nikhil Rajwade
Nuno Carvalho
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
07/03/2007
0.1
Initial Draft
Heather Rennoldson
09/03/2007
1.0
Signed off following review


References

Document
Version
Date
Author
























Introduction
Background

The purpose of this document is to confirm the business requirements for the promotions interface from the Integration Data Store (IDS) to Group, Forecast & Order (GFO) for Turkey. The information is based on the requirements for the GFO Promotions Interface file mappings (see Appendix A) and conversations with the GFO team.

This covers the requirements for the J114 interface (Promotion Data IDS to GFO). 
  
Promotions are structured in a different manner within ORMS10, so the GFO requirements for this data have been documented separately, although the ultimate receiving file/table will be the same format. 

Issues
The promotion identifier used within ORPM (and also ORMS) allows for 10 digits, but that within GFO only allows for 9 digits.


Promotions in the IDS
Overview



The diagram above portrays how the Integration data Store (IDS) holds promotional data. This is broadly in line with the ORPM tables.
 
All the promotion data within the IDS has been exploded to Store/SKU level, so GFO will not receive any details of subgroup promotions.
The interface has been designed to  recognise ‘simple’, ‘threshold’ and ‘buy-get’ promotions. However, for the first year of operation, the US will only use feature promotions i.e. simple promotions with a ‘change type’ representing ‘no change’. These will be represented as ‘SKU’ promotions to GFO. 

Only approved promotions will be held in the IDS.

Table
Description
Promotion
This holds the major promotional information – promotion, promotion name. 
PromComponent
This describes a lower level of the promotion. Deals would be set at this level within ORPM but these are not captured in the IDS.
PromoComponentDetail
This has the start and end dates of the promotion and also indicates what type of promotion it is – simple, buy-get or threshold
StoreSKUItemPromoCompDetail
This contains the products on promotion linked to the stores


Requirements
GFO requirements
1. GFO require a Promotions interface provided daily c 2200hrs.

2. This will contain details of all SKUs on promotion currently, and at any time in the next 31 days. The data required is independent of the stores linked to the promotions.

3. GFO requires a complete file every day – not deltas.
Logic for extracting from the IDS

Select  Promotion ID, PromoComponentID, PromoComponentDetailID, PromoDetailTypeID from PromoComponentDetail  which are current between now and 31 days ahead i.e. where
StartDate is <= control date + 31 days and EndDate is >= control date.
(The control date will the current ‘ORMS date’)
.
The following paragraphs indicate how to identify the items in the promotion;

Select SKUID from StoreSKUItemPromoCompDetail where PromotionID, PromoComponentID, PromoComponentDetailID = that obtained above

Remove duplicates 
Additional notes
Since a promotion can transfer from approved back to worksheet status, it is possible that a promotion will disappear from the file, before the promotion is extracted.
  
 Promotions File Mappings

GFO Integration Layer Promotions File

IDS Source




Data ItemData TypeData LengthFixed DataData Format TableData ItemData TypeData LengthNotes?JIPMA-RECORD-TYPENUMERIC2"00"       JIPMA-DATECHAR  CCYYMMDD      FILLERCHAR SPACES       JIPMB-RECORD-TYPENUMERIC2"01"       JIPMB-BASE-PRODUCT-NOCHAR9   StoreSKUItemPromoCompDetailSKUIDvarchar25FILLERNUMERIC5ZEROES       FILLERCHAR1SPACES       JIPMB-PROMOTION-STARTNUMERIC8 CCYYMMDD PromoComponentDetailStartDatesmalldatetimeJIPMB-PROM-END-DATENUMERIC8 CCYYMMDD PromoComponentDetailEndDatesmalldatetimeJIPMB-BPR-UPLIFT-PERCNUMERIC8ZEROES+/-9999999      FILLERCHAR1SPACES       FILLERCHAR48SPACES       JIPMB-OFFER-IDCHAR9   PromotionPromotionIDbiginitJIPMB-OFFER-DESCCHAR50   PromoNamePromoNamenvarchar(160)160JIPMB-OFFER-BUKT-REQDCHAR1   ????Will be set to ‘N’JIPMB-FEATURE-SPCE-DISPCHAR1"Y"       JIPMB-BPR-REGNCHAR2"00"       JIPMB-AREA-CDCHAR1"1"       JIPMB-OFFER-TYPECHAR3   PromotionComponentDetailPromotionDetailTypeIDvarchar4‘BWG’ if PromotionDetailTypeID = B 
‘THR’  if PromotionDetailTypeID = T
‘SKU’ if PromotionDetailTypeID = S FILLERCHAR84SPACES       JIPMZ-RECORD-TYPENUMERIC2"99"       FILLERCHAR241SPACES       JIPMZ-REC-COUNTNUMERIC7        

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


Date: 09/03/2007, Version1.0		Page  PAGE 3 of  NUMPAGES 9
Author : Heather Rennoldson


	
Integration Team : Requirements Definition







Date: 09/03/2007, Version 1.0		Page  PAGE 2 of  NUMPAGES 9
Author : Heather Rennoldson







 EMBED Word.Picture.8  







