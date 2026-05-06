






TOM Integration
Oracle Vendor to ORMS Supplier Interface
High Level Outline Requirements v1.2









Author
Version
Date
Thomas Harper
1.2
23/01/2007



 TOC \o "1-4" \h \z \u  HYPERLINK \l "_Toc157227947" 1	Oracle Vendor to ORMS Supplier Integration	 PAGEREF _Toc157227947 \h 2
 HYPERLINK \l "_Toc157227948" 1.1	Document History	 PAGEREF _Toc157227948 \h 2
 HYPERLINK \l "_Toc157227949" 1.1.1	Version History	 PAGEREF _Toc157227949 \h 2
 HYPERLINK \l "_Toc157227950" 1.1.2	Review	 PAGEREF _Toc157227950 \h 2
 HYPERLINK \l "_Toc157227951" 1.1.3	Sign Off	 PAGEREF _Toc157227951 \h 2
 HYPERLINK \l "_Toc157227952" 2	Overview	 PAGEREF _Toc157227952 \h 2
 HYPERLINK \l "_Toc157227953" 3	Requirements	 PAGEREF _Toc157227953 \h 2
 HYPERLINK \l "_Toc157227954" 3.1	ORMS Suppliers creation	 PAGEREF _Toc157227954 \h 2
 HYPERLINK \l "_Toc157227955" 3.2	References	 PAGEREF _Toc157227955 \h 2
 HYPERLINK \l "_Toc157227956" 3.3	Suppliers and their Maintenance	 PAGEREF _Toc157227956 \h 2
 HYPERLINK \l "_Toc157227957" 3.4	Tesco Business Pracice	 PAGEREF _Toc157227957 \h 2
 HYPERLINK \l "_Toc157227958" 3.4.1	Addresses	 PAGEREF _Toc157227958 \h 2
 HYPERLINK \l "_Toc157227959" 3.5	Tesco Interface Amendment	 PAGEREF _Toc157227959 \h 2
 HYPERLINK \l "_Toc157227960" 3.5.1	Vendor “explosion”	 PAGEREF _Toc157227960 \h 2
 HYPERLINK \l "_Toc157227962" 3.5.3	Amended Vendor to Supplier Mapping	 PAGEREF _Toc157227962 \h 2
 HYPERLINK \l "_Toc157227963" 4	Appendix	 PAGEREF _Toc157227963 \h 2
 HYPERLINK \l "_Toc157227964" 4.1	“Out of the Box” Mapping	 PAGEREF _Toc157227964 \h 2

Oracle Vendor to ORMS Supplier Integration
Document History
Version History
Name
Version
Comment
Date
Thomas Harper
1.0
Initial Draft
18/01/2007
Thomas Harper
1.1
Feedback Included
22/01/2007
Dave Onyett
1.2
Minor modification to wording
23/01/2007

Review
Position
Name
Date
Business Analyst
Sidd Sarangi

Enterprise Architect
Nigel Glenn

Project Leader
David Onyett

Oracle Consultant
Julian Watham



Sign Off
Position
Name
Date
Business Analyst
Sidd Sarangi

Enterprise Architect
Nigel Glenn

Project Leader
David Onyett

Overview
This document outlines the high level requirements for the Integration of Oracle Financials (OFi) and ORMS whereby ORMS Suppliers are set up and controlled through OFi.

Because the manufacturer’s provided solution is not fit for Tesco purpose an amendment is required. 

This document shows 
where statements in the Implementation manual are overridden by Tesco Business Practice 
where the interface is deficient and how it will be changed
how the mapping of the fields between Ofi Vendors and RMS Suppliers will be amended. 

An Appendix gives the manufacturers out of the box mapping.   

This document does not discuss the Technology that will be used to implement the amended interface. 
Requirements
ORMS Suppliers creation 
ORMS Suppliers will be set up and controlled via Oracle Financials. 
References
Oracle Retail RMS-Oracle Financials Implementation Guide 11.0.6 November 2005
Oracle Retail Merchandising System Oracle Financials Interface Implementation Guide Addendum Release 11.0.8 June 2006

Suppliers and their Maintenance 
page 40 of the Implementation Guide states -

“Suppliers are now created in the Oracle financials system and exported to RMS. They cannot be created using the RMS windows (This is because the supplier master flag in ORMS will be set to O/Fi. Otherwise they can be created in ORMS). However, once the Supplier exists in RMS, all data values for the Supplier (except Supplier Name and Status) will continue to be updated using the RMS windows.

Note: Functionality for Partners data is not affected by this project.”

This statement is partially overridden by Tesco Business Practice.

Tesco Business Practice
Tesco Business Practices dictate that the data that will be setup in O/Fi will continue to be maintained in O/Fi. The data shouldn’t be edited in ORMS. Although most interfaced fields are now editable in ORMS, editing of data in ORMS, which is mastered in O/Fi, cannot be allowed as a business practice.  

(ORMS specific fields which hold vendor information which does not exist in Financials will of course continue to be maintained in ORMS. )

Addresses
The Implementation Manual continues :-

“Supplier Address types of ‘Order’ and ‘Remittance’ are now created in the Oracle
financials system and exported to RMS. They cannot be created using RMS windows.
Once these addresses exist in RMS, the address fields (Street, City, State, and so on) are
updated in Oracle and fed to RMS”. …

“The RMS import process creates any other required Supplier Address types by copying
the Order or Remittance addresses received from Oracle….”
 
“Any optional Supplier Address types are created and updated only in RMS.
Any non-Supplier Addresses (that is, partner addresses, store addresses, and so on.) are
created and updated only in RMS.”

Tesco Interface Amendment
The way the out of the box integration works is not fit for Tesco purposes.

We will be changing the integration so that the Financial hierarchical structure of Master  Vendor (PO_Vendor) with multiple Vendor Sites (PO_Vendor_Sites_All) will be “exploded” so that each Vendor Site becomes an RMS Supplier. (This is to allow Items to be attached at  Supplier “Site” level. Without this change only the first Vendor Site would become an RMS Supplier  and Items could only be attached to that single site.) 

Vendor “explosion”  SHAPE  \* MERGEFORMAT 
Note that the change means that the 5 digit PO_VENDORS_SITES_ALL.VENDOR_SITE_ID in Financials becomes the 5 digit SUP.SUPPLIER in ORMS.

The Vendor and Vendor sites will also have a mandatory flex field ‘Costing Date’ with options ‘Order Date’ & ‘Delivery Date’. This information will be defaulted to Vendor sites from the Vendor level but can be changed at site level. This data will be interfaced to the ORMS supplier.

Amended Vendor to Supplier Mapping
SYSTEMTABLE FIELD NAMETYPESYSTEMTABLE FIELD NAMETYPE
NOTESOFIPO_VENDORSVENDOR_ID6 NUMBER ORMS
SUP_TRAITSMASTER_SUP6 NUMBER Master Vendor key in OraclePO_VENDOR_SITES_ALLVENDOR_SITE_ID5 NUMBER SUPS   SUPPLIER5 NumberKEYPO_VENDORSVENDOR_NAME80 VARCHARSUPS   SUP_NAME240 VARCHAR PAD??SUPS   CONTACT_NAME120 VARCHAR2PO_VENDOR_SITES_ALLPHONE15 VARCHAR2SUPS   CONTACT_PHONE20 VARCHAR2PAD??SUPS   CONTACT_PAGER?derivedSUPS   SUP_STATUS1 VARCHAR2‘A’ OR ‘I’PO_VENDOR_SITES_ALLPAYMENT_CURRENCY_CODE
OR INVOICE_CURRENCY_CODE15 VARCHAR2SUPS   CURRENCY_CODE
FK  to FND_CURRENCIES.CURRENCY_CODE3 VARCHAR2PO_VENDOR_SITES_ALLLANGUAGE?30 VARCHAR2SUPS   LANG FK to LANG LANG.DESCRIPTION VARCHAR2(120)6 NUMBERPO_VENDOR_SITES_ALLTERMS_IDNUMBERSUPS   TERMS FK TERMS_HEAD.TERMS15 VARCHAR2PO_VENDOR_SITES_ALLFREIGHT_TERMS_LOOKUP_CODE25 VARCHAR2SUPS   FREIGHT_TERMS30 VARCHAR2CONTACT_EMAIL100 VARCHAR2Default=”UNKNOWN”generatedADDRMODULE4 VARCHAR2‘SUPP’PO_VENDOR_SITES_ALLVENDOR_SITE_ID5 NUMBER ADDRKEY_VALUE_15 NUMBER ADDRSEQ_NONUMBER(4,0)GENERATEDPO_VENDOR_SITES_ALLADDRADDR_TYPE2 VARCHAR2
“04” OR “06”01 =Busines
02= Postal
03=Returns
04=Order
05=Invoice
06=RemittanceADDRPRIMARY_ADDR_INDPO_VENDOR_SITES_ALLADDRESS_LINE135 VARCHAR2ADDRADD_1240 VARCHAR2PADPO_VENDOR_SITES_ALLADDRESS_LINE235 VARCHAR2ADDRADD_2240 VARCHAR2PADPO_VENDOR_SITES_ALLADDRESS_LINE335 VARCHAR2ADDRADD_3240 VARCHAR2PADPO_VENDOR_SITES_ALLCITY25 VARCHAR2ADDRCITY120 VARCHAR2PADPO_VENDOR_SITES_ALLSTATE25 VARCHAR2ADDRSTATE3 VARCHAR2TRUNCATEPO_VENDOR_SITES_ALLZIP20 VARCHAR2ADDRPOST30 VARCHAR2PADADDRCONTACT_NAME120 VARCHAR2Default=”UNKNOWN”PO_VENDOR_SITES_ALLPHONE15 VARCHAR2ADDRCONTACT_PHONE20 VARCHAR2PADPO_VENDOR_SITES_ALLFAX15 VARCHAR2ADDRCONTACT_FAX20 VARCHAR2PADPO_VENDOR_SITES_ALLVENDOR_SITE_IDADDRORACLE_VENDOR_SITE_ID5 NUMBERorg_idADDRoracle_org_unit_idPO_VENDOR_SITES_ALLvendor_site_idADDRoracle_vendor_site_id5 NUMBER



Note that the Invoice Posting Interface which goes in the reverse direction will have to substitute supplier ID with vendor master ID – we are working on this.

Appendix

“Out of the Box” Mapping
























Oracle Vendor to ORMS Supplier Integration Page  PAGE 1


Master Vendor

Vendor Site 1

Vendor Site 2

Vendor Site 3

ORMS

FINANCIALS

Supplier 1

Supplier 2

Supplier 3

PO_VENDOR_SITES_ALL

PO_VENDORS

SUPS

SUP_TRAITS

VENDOR_ID




