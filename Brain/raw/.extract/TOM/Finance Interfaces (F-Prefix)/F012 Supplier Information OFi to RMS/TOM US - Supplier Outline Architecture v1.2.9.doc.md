












TOM 
Outline Architecture





Finance Package F012 – OFi Vendor Interface to ORMS Supplier

Version:
1.2.9
Author:
Thomas Harper
Date:
13.03.2007








Version:
1.2.9
Author:
Thomas Harper
Date:
13.03.2007
Project BEN Code:
W60416
Circulation Restrictions:
Tesco Internal Only
Status:
Final

Document Information

Change Record

Author
Date
Version
Change Reference, description
Thomas Harper
23/01/2007
1.0.0
Draft
Thomas Harper
30/01/2007
1.1.0
Incorporated OFi flexfield changes. Highlighted mapping assumptions.
Thomas Harper
31/01/2007
1.2.0
Finalised assumptions
Thomas Harper
01/02/2007
1.2.1
Added missing LAST_NAME field
Thomas Harper
12/02/2007
1.2.2
Changed input file to pipeline delimited
Thomas Harper
12/02/2007
1.2.3-4
PrePaid Supplier and Costing flags added
Thomas Harper
13/02/2007
1.2.5
PrePaid Supplier and Costing changes struck out
Thomas Harper
27/02/2007
1.2.6
End of record indicator aligned to .TXT file unix output (CRLF)
Thomas Harper
06/03/2007
1.2.7
Common Forms references added
IDS Supplier inserting clarified
Thomas Harper
07/03/2007
1.2.8
VENDOR_SITE_CODE will be concatenated to VENDOR_NAME
All SITE_TYPES will be 04 for USA
EMAIL will be included in the extract
Thomas Harper
13/03/2007
1.2.9
Outstanding issues added before sign off

Reviewers

Name
Date
Version
Role
Sidd Sarangi


Business Analyst
Nigel Glenn


Enterprise Architect
Nathan Smith


Enterprise Architect
David Onyett


Project Leader
Jonathan  Brimley


IBM Consultant, USA

Distribution

Name
Role
Nigel Glenn
Enterprise Architect
Nathan Smith
Enterprise Architect
Ann Merritt
Enterprise Architect
Duncan Wellberry
TOM Programme Manager
Rae Topp
TOM Integration Project Manager
David Onyett
TOM Integration Project Manager
David Briggs
Group IT Distribution and Head Office Systems Portfolio Manager
Jonathan Brimley
IBM Consultant, USA
Sidd Sarangi
Business Analyst
David Briggs
HO Portfolio Manager

References
All documents are held in Sharepoint.
Document
Where held
Version & date
Solutions Architecture
Not Available

Business Requirements Document
docshare

Project Technical Systems Design
Not Available

Funding Project Plan


Integration Context Diagram.vsd
TOM Vendors to ORMS Supplier Integration Context Dgm v1.1.vsd
page: VENDORS via Biztalk

IS Order Spec - Transformation of Oracle Finance Supplier to ORMS exploded Supplier  xml
TOM Integration Finance docshare


Sign-Off
By signing this form, I understand and agree with the contents of this document. 

Business Owner/Customer
Nigel Glenn
Role
Enterprise Architect
Signature
Nigel Glenn
Date
13/03/2007

Table of Contents
 TOC \o "1-3" \t "Appendix,1" Table of Contents	 PAGEREF _Toc161562211 \h v
1.	Introduction	 PAGEREF _Toc161562212 \h 7
1.1.	Purpose	 PAGEREF _Toc161562213 \h 7
1.2.	Background	 PAGEREF _Toc161562214 \h 7
1.3.	Scope	 PAGEREF _Toc161562215 \h 9
1.3.1.	In Scope	 PAGEREF _Toc161562216 \h 9
1.3.2.	Out of Scope	 PAGEREF _Toc161562217 \h 9
2.	TOM Project high-level requirements	 PAGEREF _Toc161562218 \h 9
3.	Information Architecture High Level Design	 PAGEREF _Toc161562219 \h 9
3.1.	The scope of this Integration  Design covers	 PAGEREF _Toc161562220 \h 9
3.2.	Interfaces	 PAGEREF _Toc161562221 \h 10
3.3.	Context Architecture	 PAGEREF _Toc161562222 \h 11
4.	Oracle Extraction Requirements (Application Project)	 PAGEREF _Toc161562223 \h 12
4.1.	Switch Off BPEL SendVendorToOracle Retail processing (Application Project)	 PAGEREF _Toc161562224 \h 12
4.2.	Extract File (Application Project)	 PAGEREF _Toc161562225 \h 12
4.3.	File Transmission (Application Project)	 PAGEREF _Toc161562226 \h 12
4.4.	Post Transmission Cleanup Script (Application Project)	 PAGEREF _Toc161562227 \h 12
5.	Information Services Requirements	 PAGEREF _Toc161562228 \h 12
5.1.	Interfaces (TOM Integration Project)	 PAGEREF _Toc161562229 \h 13
5.1.1.	 PAGEREF _Toc161562230 \h 13
5.2.	Data Requirements	 PAGEREF _Toc161562231 \h 13
6.	Physical Deployment	 PAGEREF _Toc161562232 \h 13
7.	Benefits and concerns	 PAGEREF _Toc161562233 \h 13
7.1.	Benefits/key features	 PAGEREF _Toc161562234 \h 13
7.2.	Concerns/risks	 PAGEREF _Toc161562235 \h 13
8.	Deliverables and high-level Estimate	 PAGEREF _Toc161562236 \h 14
Appendix A Data Definitions and Mappings	 PAGEREF _Toc161562237 \h 17
A.1	OFi Extracted Record Fields	 PAGEREF _Toc161562238 \h 17
A.2	The Extract Script	 PAGEREF _Toc161562239 \h 18
A.3	Sample extract file	 PAGEREF _Toc161562240 \h 23
A.4	End to End Mapping	 PAGEREF _Toc161562241 \h 23
8.1.	Mapping – Flat File to Common Form	 PAGEREF _Toc161562242 \h 27
8.2.	Mapping – Common Form to RIB	 PAGEREF _Toc161562243 \h 27
8.3.	Writing to the IDS	 PAGEREF _Toc161562244 \h 27
8.4.	Stored Procedures	 PAGEREF _Toc161562245 \h 27
8.5.	Common Form Schemas	 PAGEREF _Toc161562246 \h 27
A.5	OFi Source Data	 PAGEREF _Toc161562247 \h 28
A.6	RIB RMS message format	 PAGEREF _Toc161562248 \h 40


Introduction

The Oracle Vendor interface isn’t fit for Tesco use. The BPEL changes needed to make it fit for purpose won’t be ready in time for go live. We will develop our own interim solution with  the following caveats and assumptions

HIGH LEVEL ASSUMPTIONS

IN the ABSENCE of a SOLUTION ARCHITECTURE DOCUMENT:-
A flat file of Vendors + Sites will be extracted from Ofi 
Extracts from Oracle Financials will be updated records only (i.e first time through we get the lot, afterwards only changes)
Extraction is repeated hourly due to Supplier suspension requirements

IN the ABSENCE of a PROJECT TECHNICAL DESIGN:-
This document will provide sufficient information for the Interface Specification to be written.
It is assumed tha the Information in Oracle Technical manuals and a physically implemented database gives sufficient information to carry out the integration
Values held in certain fields will map directly between Ofi and ORMS applications e.g. Country.  

Outstanding Issues
At the time of sign-off the following issues remain to be resolved
Finance SIPOCS 3.5 are still awaited.
OFi use of Country versus ORMS use of ISO Country Code.
This will probably be resolved using a reverse lookup translation table in the Integration Layer. In the meantime OFi Vendor setup will have to use the 2 digit ISO Country code when setting up addresses.
OFi Payment Terms verses ORMS Payment Terms. Similar issues  to country are expected around this field. 
Purpose
This document describes the TOM Programme’s high level requirements for a Vendor to Supplier interface between Oracle Financials (OFi) and Oracle Retail Merchandise System (ORMS) 
From these requirements the document proposes an Integration design and lists key involvements.  This will provide information to the application project, the Integration development and the TOM programme plan.

Background
The TOM Project is to implement repeatable Group based solutions mainly centred on Oracle Applications. Integration is required between these packages where the integration is either not yet completed by Oracle or the Oracle integration does not meet Tesco requirements. 
The Integration deliverables for Oracle Finance (OFi) replace the Oracle provided integration between OFi and ORMS and OFi and ReIM where the manufacturers solution is not fit for Tesco purpose.
ORMS Supplier setup will be controlled from OFi by sending Vendor information to ORMS.
The OFi Vendor table holds the Vendor as a Master Record with child Vendor  Site Addresses. If transferred directly to ORMS using the “out of the box” integration only the first address would ever be referenced as the Supplier. To overcome this difference it is necessary to “explode” the Financials Record such that there will be a main Supplier Record in ORMS corresponding to each Vendor Supplier Address as held in the Supplier_Site data flex field (DFF)  in Financials. 

The Vendor Address Supplier_Site DFF (ATTRIBUTE10) value will be used as the ORMS Supplier Key . The Vendor Id is held in SEGMENT1.

       SHAPE  \* MERGEFORMAT 

Note that the change means that the 5 digit PO_VENDORS_SITES_ALL.Attribute10 in Financials becomes the 5 digit SUP.SUPPLIER in ORMS.

For PO_vendors table, the "supplier number" data is stored in the Segment1 field. For the PO_vendors_sites_all table, the "vendor site dff " is Attribute10.

The Vendor and Vendor sites will also have a mandatory flex field ‘Costing Date’ with options ‘Order Date’ & ‘Delivery Date’. This information will be defaulted to Vendor sites from the Vendor level but can be changed at site level. This data will be interfaced to the ORMS supplier.
[assumption – this is yet to be confirmed and detailed]



Scope
In Scope

Integration of Oracle Vendors to ORMS Suppliers 
Persisting of Supplier data in the Integration Data Store (IDS) in the Integration Layer
Out of Scope

All Other OFi to ORMS and ReIM Interfaces
TOM Project high-level requirements
Information Architecture High Level Design
The scope of this Integration  Design covers 

Extract Vendor and Vendor Adress data from OFI using a script to create a flat file
Transmit extracted file from Oracle Financials to Biztalk using XCOM[Assumption] or will be written to a CIFS share 
File Receive into Biztalk using RTI Adapter.
Debatch Flat file 
Transform Flat file to the relevant Common Forms
Create copy of Common Forms 
Transform Common format to RIB format Supplier XML message
Use Sysrepublic Real Time Integrator Database Command Script adapter to publish  Supplier messages to the Supplier JMS Topic on the Retek Integration Bus (RIB)
Write the copies of the Common Format messages to a file share for IDS Import via SSIS

Interfaces
There is 1 interface between Oracle Financials and ORMS, as shown on the next page. Reference:
Context Diagram: 	Supplier to ORMS from Oracle Financials 
Page Name: 		Vendor via Biztalk
Context Architecture
 EMBED Visio.Drawing.11  
Interface 1: Oracle Financials Supplier to ORMS Supplier
Oracle Financials sends an extracted Supplier flat file to a Biztalk File Receive location. Biztalk converts the file to a Common Form then to RIB format and loads it to ORMS via the RIB. A SQL Supplier database in the Integration Layer will also be loaded using the Common Form during this process. 
Oracle Extraction Requirements (Application Project)
The Extraction Code will be specified and coded by the Application Project ]. 
Switch Off BPEL SendVendorToOracle Retail processing (Application Project)
Extract File (Application Project)
Only certain supplier sites are needed for ORMS. Only records with the Flex Field ORMS_FLAG  set to “Y”  will be extracted.
The Vendor (PO_VENDOR table) and Vendor Sites (PO_Vendor_Sites_All) records will be extracted using an inner join to create a combined record for each Vendor Site together with contact details from Vendor Contacts (PO_Vendor_Contacts). 
The combined records will hold information from the appropriate fields from the Vendor master and from each child Vendor Site and Associated Contact information. 
For PO_vendors table, the "supplier number" data is stored in the Segment1 field. For the PO_vendors_sites_all table, the "vendor site dff " is Attribute10.”
The extracted records will therefore use the data in Segment1 to provide the number for the Vendor id  and will use Attribute10 to provide the number for the Vendor Site Id
The extracted records will constitute a flat file. 
Fields will be pileline ‘|’ delimited. 
CRLF will delimit end of record.
The extraction will be scheduled for an hourly [Assumption] transmission. (If Vendors are suspended we will want the information propogated fairly rapidly). 
The extract will comprise all records changed since the last extract.
File Transmission (Application Project)
The file will be extracted to a CIFS based share. 
An hourly [Assumption] schedule will be set up to run the extraction.
Information Services Requirements
The Integration Interface Specification, the Mapping Spreadsheet and the coding of the Interface will be carried out by the Tom Integration Project.
Interfaces (TOM Integration Project)
The interface will be implemented on the BizTalk 2006 platform. 
The following interface makes up the TOM Integration Project interface package:


A Biztalk Orchestration Receives the extracted flat file into a Pipeline where it is debatched. 
The Orchestration transforms each flat file record into a Supplier, Address and Activity Common form XML message. 
A parallel process is created to make copies of the Common Forms and to pass them to the RTI Database Command Script adapater which will write the records to the IDS. 
(Note: The Supplier IDS is for use by other systems that need supplier information).
The Common Forms are Transformed into a RIB format message
The message is Published onto the RIB by the Sysrepublic RTI JMS Adapter. 
An MSI for this Interface will be configured and generated for deployment purposes together with a Release Note. 
Data Requirements
See the Appendix for data requirements.
Physical Deployment
The interface will be deployed into a standard Tesco EAI BizTalk 2006 environment using an MSI process.

A Release Note will document the installation process.
Benefits and concerns
Benefits/key features
The new interface will be implemented on the strategic BizTalk 2006 platform, replacing the Oracle provided Integration with an Integration that meets Tesco requirements.
Concerns/risks  
At the time of writing
 
There is no Solutions Architecture feeding into this design
There is no Project Technical Design feeding into this design
The BizTalk 2006 environment is new for Tesco, and the design / development / operational processes are not as mature as for the BizTalk 2002 environment


Deliverables and high-level Estimate
The column marked Gen/Spec shows whether the build is generic (G), e.g. reusable by other projects, or specific (S) to this project.

ActivityInterfaceRequired by for Integration TestComplexityDev/UT Estimate (Days)Gen/SpecComments1
Program Specification for theOracle Extract
[Application Project]
28/03/2007
L
1
S
1. Must include layout for extracted records
2. Must specify that a record is output for each child site address. (This can be done using an inner JOIN for the site address in the SELECT statement). Only one set of contact details will be forwarded to ORMS. Where this is held in the Vendor_Contacts table only the first contact will be used.
3. As we are selecting changes the select statement should include something like:- “where  table VENDORS. LAST_UPDATE_DATE  > sysdate-1 (for updates today) or VENDORS. LAST_UPDATE_DATE  > date/time of start of last extract run.”
4. Only select where flex field ORMS_FLAG for orms is set to “YES”.
For PO_vendors table, the "supplier number" data is stored in the Segment1 field. For the PO_vendors_sites_all table, the "vendor site dff " is Attribute10.
2
Oracle Extract Script
[Application Project]
28/03/2007
L
1
S
Extract Vendors and Vendor Sites  Output a combined record for every site as a pileline ‘|’ delimited flat file.
3
Schedule Extracts
[Application Project]
28/03/2007
L
0.5
S
Configure the scheduler to run the extract at specified time intervals
4
Switch off BPEL process SendVendorToOracle Retail
[Application Project] 
28/03/2007
L
0.5
S
We don’t want to send Vendor updates via the manufacturer’s provided interface
5
Mapping Spreadsheet
[IS}
28/03/2007
M
1
S
Specify transformation rules 
6
Interface Specification [IS}

M
2
S
Specify the Interface
7
Extend Common Form to Support this Interface’s requirements [IS}
28/03/2007
M
2
G
Extend Supplier Common Form 
8
Flat File Schema [IS}
28/03/2007
M
1
S
Specify the schema for the incoming flat file
9
Maps [IS}
28/03/2007
M
1
S
Create Maps for Flat File to Common and Common to RIB
10
Biztalk Interface
Financials Vendor and Sites to ORMS Supplier and to IDS Supplier [IS}
28/03/2007
H
7
G
Receives file
Maps Supplier Vendor+Site records into separate Suppliers for ORMS (output is to Common RMS Supplier Message Schema).
Set up parallel flow. On first output the record to a share for IDS Import Processing. On the second, pass the common msg to a transform to RIB process.
Pass the message to the RTI Adapter to publish to the RIB.
Platform BizTalk 2006

11
Interface MSI [IS}
28/03/2007
M
3
S
Build the Deployment MSI for the Biztalk Assemblies
12
Release Note [IS}
28/03/2007
M
2
S
Specifies the Release Processes
Data Definitions and Mappings
These data requirements are derived from  :-
Oracle Accounts Payable Technical Reference manual
ORMS Data Dictionary manual
Oracle Retail RMS-Oracle Financials Implementation Guide manual
RIB Mapping Report Release 12.0.0 manual
ORMS Data Dictionary manual
It should be noted that there is no Project Technical Reference Document for this interface. 
OFi Extracted Record Fields
TABLE 
FIELD NAME
TYPE
PO_VENDORS
VENDOR_ID (from table key)
6 NUMBER
PO_VENDORS
VENDOR NUMBER VENDOR_ID (from SEGMENT1 field)
6 NUMBER 
PO_VENDOR_SITES_ALL
VENDOR_SITE_ID (from Table key)
5 NUMBER
PO_VENDOR_SITES_ALL
VENDOR_SITE_ID (from ATTRIBUTE10 field))
5 NUMBER 
PO_VENDORS PO_VENDOR_SITES_ALL
VENDOR_NAME + “ “ +
VENDOR_SITE_CODE
80  VARCHAR2
PO_VENDORS
VENDOR_STATUS *
“A” or “I” 
PO_VENDOR_CONTACTS
FIRST_NAME 
15 VARCHAR2
PO_VENDOR_CONTACTS
MIDDLE_NAME
15 VARCHAR2
PO_VENDOR_CONTACTS
LAST_NAME

PO_VENDOR_SITES_ALL
PAYMENT_CURRENCY_CODE
OR INVOICE_CURRENCY_CODE ***
15 VARCHAR2
PO_VENDOR_SITES_ALL
LANGUAGE ***
30 VARCHAR2
PO_VENDOR_SITES_ALL
TERMS_ID ***
NUMBER
PO_VENDOR_SITES_ALL
FREIGHT_TERMS_LOOKUP_CODE ***
25 VARCHAR2
PO_VENDOR_SITES_ALL
ADDRESS_LINE1
35 VARCHAR2
PO_VENDOR_SITES_ALL
ADDRESS_LINE2
35 VARCHAR2
PO_VENDOR_SITES_ALL
ADDRESS_LINE3
35 VARCHAR2
PO_VENDOR_SITES_ALL
CITY
25 VARCHAR2
PO_VENDOR_SITES_ALL
STATE
25 VARCHAR2
PO_VENDOR_SITES_ALL
COUNTRY
25 VARCHAR2
PO_VENDOR_SITES_ALL
ZIP
20 VARCHAR2
PO_VENDOR_SITES_ALL
PHONE
15 VARCHAR2
PO_VENDOR_CONTACTS
FAX
15 VARCHAR2
PO_VENDOR_SITES_ALL
SITE_TYPE **
“04” or “06”
PO_VENDOR_CONTACTS
EMAIL
100 VARCHAR2
PO_VENDOR_SITES_ALL
COSTING_DATE****
1 VARCHAR2
PO_VENDOR_SITES_ALL
PREPAID_SUPPLIER****
1 VARCHAR2






* 	The extract script should set the status to “I” or “A” based on the supplier status.
** 	The extract script should set the site type to “04” or “06” based on the type of site.
*** 	Payment Currency, language, terms_id, freight terms and country will be mapped directly across [assumption – same codes are used across the applications]
	The Country field should hold the two digit ISO country code as a Business process requirement will be to use this code when setting up the Vendors and their Sites in OFi.

****
This will be an option for the user to choose. There will be one LOV which will have two options. 'Order Date' and 'Delivery Date'. The user will simply pick the supplier to be either an Order date or a Delivery date supplier. No dates are to be entered. 
 
This data will be interfaced to ORMS as SUPS.TES_ORDER_COSTING which will be 'A' for Order Date (Also called approval date) suppliers and 'D' for delivery date suppliers

The supplier and supplier sites will also have a mandatory flex field ‘Prepaid Supplier’ with options ‘Y’ & ‘N’. The default will be N. This information will be defaulted to supplier sites from the supplier level but can be changed at site level. This data would need to be interfaced to the ORMS supplier. (SUPS.PREPAY_INVC_IND).

Fields should be pileline ‘|’ delimited.
Records should end with CRLF.
A definitive specification of the extract needed is given in the BSD.
The Extract Script
This is maintained on the Oracle OFi platform but is  shown here for convenience and is pre version 1.2.8 change to  VENDOR_SITE_CODE concatenating onto VENDOR_NAME.
----------------------------------------------------------------------
-- $Header:XXTC_SUPPLIER_EXTR_PKG.pls 11510.1 24-FEB-'07 Santhi    $ 
--	
-- File:	$XXTC_TOP/sql/XXTC_SUPPLIER_EXTR_PKG.pls
-- Name:	XXTC - F012 Vendor to ORMS and IDS Supplier Interface
-- Date:	24-FEB-2007
-- Author:	Santhi 
-- 
-- History
--
-- 11510.1  Santhi  (2007/02/24) - Created
--
---------------------------------------------------------------------- 
CREATE OR REPLACE PACKAGE XXTC_SUPPLIER_EXTR_PKG  AUTHID CURRENT_USER as
 PROCEDURE Supplier_Extract (errbuf                 OUT VARCHAR2 ,retcode  OUT NUMBER,p_output_directory in varchar , p_output_filename in varchar2  );
END XXTC_SUPPLIER_EXTR_PKG;
/
CREATE OR REPLACE PACKAGE BODY XXTC_SUPPLIER_EXTR_PKG   aS
PROCEDURE Supplier_Extract (errbuf OUT VARCHAR2,retcode  OUT NUMBER,p_output_directory in varchar , p_output_filename in varchar2  ) IS
CURSOR CUR_CUST IS
SELECT
pv.vendor_id VENDOR_ID,
pv.segment1 VENDOR_NUMBER,
pv.vendor_name VENDOR_NAME,
pv.enabled_flag VENDOR_STATUS,
pvc.first_name FIRST_NAME,
pvc.middle_name MIDDLE_NAME,
pvc.last_name LAST_NAME,
pvs.vendor_site_code vendor_site_code,
pvs.payment_currency_code PAYMENT_CURRENCY_CODE,
pvs.invoice_currency_code INVOICE_CURRENCY_CODE,
pvs.language LANGUAGE,
pvs.terms_id TERMS_ID,
pvs.freight_terms_lookup_code FREIGHT_TERMS_LOOKUP_CODE,
pvs.address_line1 ADDRESS_LINE1,
pvs.address_line2 ADDRESS_LINE2,
pvs.address_line3 ADDRESS_LINE3,
pvs.city CITY,
pvs.state STATE,
pvs.country COUNTRY,
pvs.zip ZIP,
pvs.phone PHONE,
pvs.fax FAX,
pvs.purchasing_site_flag purchasing_site_flag,
pvs.pay_site_flag  pay_site_flag,
pvc.first_name || pvc.middle_name || pvc.last_name CONTACT_NAME
FROM
po_vendors pv,
po_vendor_sites_all pvs,
po_vendor_contacts pvc
WHERE
pv.vendor_id=pvs.vendor_id
and pvs.vendor_site_id=pvc.vendor_site_id(+)
and pvs.attribute5 = 'YES'
and trunc(pvs.last_update_date)=trunc(sysdate);


v_territory_short_name varchar2(80);
p_out_directory varchar2(30)  ;
p_out_filename varchar2(30)  ;
REC_CUST	CUR_CUST%ROWTYPE;
num number :=0;
l_ret BOOLEAN;
v_active_flag varchar2(1);
V_VENDOR_SITE_number number;
v_site_type varchar(2);
FILE_CUST	utl_file.file_type;


BEGIN

 -----Opening the File in Write Mode-----
 FILE_CUST := utl_file.fopen(p_output_directory , p_output_filename , 'W');
 fnd_file.put_line(fnd_file.log,'************************************************************************************');
 fnd_file.put_line(fnd_file.log,'                   XXTC - OFi Vendor to ORMS and IDS Supplier Interface');
 fnd_file.put_line(fnd_file.log,'************************************************************************************');
 fnd_file.put_line(fnd_file.log,'Output File Directory   :' ||p_output_directory );
 fnd_file.put_line(fnd_file.log,'File Name               :' || p_output_filename);
 
 fnd_file.put_line(fnd_file.output,'************************************************************************************');
 fnd_file.put_line(fnd_file.output,'                   XXTC - OFi Vendor to ORMS and IDS Supplier Interface');
 fnd_file.put_line(fnd_file.output,'************************************************************************************');
 fnd_file.put_line(fnd_file.output,'Output File Directory            :' || p_output_directory );
 fnd_file.put_line(fnd_file.output,'Output File Name                 :' || p_output_filename);
  fnd_file.put_line(fnd_file.log,'************************************************************************************');
 FOR REC_CUST IN CUR_CUST
 LOOP
     v_site_type  :=' ';

    /* The SITE_TYPE should be set to '06' only If The 'Pay' Check Box is ticked AND 
            the 'Purchase' check box is NOT ticked*/


     IF REC_CUST.purchasing_site_flag ='N' and REC_CUST.pay_site_flag='Y'
     then
           v_site_type :='06';     
     else
           v_site_type :='04';
     End if;

     -----Selection of Country Name-----

     Begin 
       Select 
	      TERRITORY_SHORT_NAME
	   INTO v_territory_short_name
       From
          FND_TERRITORIES_VL FT
   	   Where
  	      FT.TERRITORY_CODE = REC_CUST.COUNTRY
          AND ROWNUM =1;
       Exception
	 When others then 
	   fnd_file.put_line(fnd_file.log,'Error :'|| substr(sqlerrm,1,300));
     End;

     ---------Active , Inactive Status Flag------------
     Begin 
      select decode(pvs.INACTIVE_DATE, null,'A', (Select 'I' FROM PO_VENDOR_SITES_ALL PVS,
                                                                  PO_VENDORS PV
                                                  WHERE PV.VENDOR_ID = PVS.VENDOR_ID
                                                  and PV.SEGMENT1 = REC_CUST.vendor_number
                                                  and PVS.VENDOR_SITE_CODE =REC_CUST.vendor_site_code
                                                  and PVS.ATTRIBUTE5 ='YES') )
      into v_active_flag
      from PO_VENDOR_SITES_ALL PVS,
           PO_VENDORS PV
      WHERE PV.VENDOR_ID = PVS.VENDOR_ID
            and PV.SEGMENT1 = REC_CUST.vendor_number
            and PVS.VENDOR_SITE_CODE =REC_CUST.vendor_site_code
            and PVS.ATTRIBUTE5 ='YES';

     Exception
	 When others then 
	   fnd_file.put_line(fnd_file.log,'Error :'|| substr(sqlerrm,1,300));
     End;

     -----Selection of Vendor_Site_Id-----     

     Begin
       Select 
 	PVS.VENDOR_SITE_ID
       INTO V_VENDOR_SITE_number
       FROM 
         PO_VENDOR_SITES_ALL PVS,
         PO_VENDORS PV
      WHERE PV.VENDOR_ID = PVS.VENDOR_ID
      and PV.SEGMENT1 = REC_CUST.vendor_number
      and PVS.VENDOR_SITE_CODE =REC_CUST.vendor_site_code
      and PVS.ATTRIBUTE5 ='YES';
      
     Exception
	 When others then 
	   fnd_file.put_line(fnd_file.log,'Error :'|| substr(sqlerrm,1,300));
     End;

     -----Updating the Attribute10 in po_vendor_sites_all-----     

     Begin
        Update po_vendor_sites_all
        set attribute10= V_VENDOR_SITE_number
        WHERE VENDOR_ID = REC_CUST.VENDOR_ID
        AND VENDOR_SITE_CODE =REC_CUST.vendor_site_code
        AND ATTRIBUTE5 ='YES';
      
     Exception
	 When others then 
	   fnd_file.put_line(fnd_file.log,'Error :'|| substr(sqlerrm,1,300));
     End;
        

     -----Displaying the output in the Viewoutput-----     
     
     fnd_file.put_line(fnd_file.output,substr(REC_CUST.VENDOR_ID,1,6) 
		||'|'||	substr(REC_CUST.VENDOR_NUMBER,1,6)
		||'|'|| substr(REC_CUST.VENDOR_NAME,1,80)
		||'|'||	substr(REC_CUST.VENDOR_STATUS,1,1)
		||'|'||	substr(REC_CUST.FIRST_NAME,1,15)
		||'|'|| substr(REC_CUST.MIDDLE_NAME,1,15)
		||'|'|| substr(REC_CUST.LAST_NAME,1,15)
		||'|'|| substr(V_VENDOR_SITE_NUMBER,1,5)
		||'|'||	substr(REC_CUST.PAYMENT_CURRENCY_CODE,1,15)
		||'|'||	substr(REC_CUST.INVOICE_CURRENCY_CODE,1,15)
		||'|'||	substr(REC_CUST.LANGUAGE,1,30)
		||'|'|| REC_CUST.TERMS_ID
		||'|'|| substr(REC_CUST.FREIGHT_TERMS_LOOKUP_CODE,1,25)
		||'|'||	substr(REC_CUST.ADDRESS_LINE1,1,35)
		||'|'||	substr(REC_CUST.ADDRESS_LINE2,1,35)
		||'|'||	substr(REC_CUST.ADDRESS_LINE3,1,35)
		||'|'||	substr(REC_CUST.CITY,1,25)
		||'|'||	substr(REC_CUST.STATE,1,25)
		||'|'||	substr(v_territory_short_name,1,25)
		||'|'||	substr(REC_CUST.ZIP,1,25)
		||'|'||	substr(REC_CUST.PHONE,1,15)
		||'|'||	substr(REC_CUST.FAX,1,15)
		||'|'||	substr(v_site_type,1,2)
		||'|'||	v_active_flag
		||'|'||	substr(REC_CUST.CONTACT_NAME,1,200));
	

     -----Writting the Supplier details in a file-----     
 
     utl_file.put_line(FILE_CUST,substr(REC_CUST.VENDOR_ID,1,6)
		||'|'||	substr(REC_CUST.VENDOR_NUMBER ,1,6)
		||'|'|| substr(REC_CUST.VENDOR_NAME,1,80)
		||'|'||	substr(REC_CUST.VENDOR_STATUS,1,1)
		||'|'||	substr(REC_CUST.FIRST_NAME,1,15)
		||'|'|| substr(REC_CUST.MIDDLE_NAME,1,15)
		||'|'|| substr(REC_CUST.LAST_NAME,1,15)
		||'|'|| substr(V_VENDOR_SITE_NUMBER,1,5)
		||'|'||	substr(REC_CUST.PAYMENT_CURRENCY_CODE,1,15)
		||'|'||	substr(REC_CUST.INVOICE_CURRENCY_CODE,1,15)
		||'|'||	substr(REC_CUST.LANGUAGE,1,30)
		||'|'|| REC_CUST.TERMS_ID
		||'|'|| substr(REC_CUST.FREIGHT_TERMS_LOOKUP_CODE,1,25)
		||'|'||	substr(REC_CUST.ADDRESS_LINE1,1,35)
		||'|'||	substr(REC_CUST.ADDRESS_LINE2,1,35)
		||'|'||	substr(REC_CUST.ADDRESS_LINE3,1,35)
		||'|'||	substr(REC_CUST.CITY,1,25)
		||'|'||	substr(REC_CUST.STATE,1,25)
		||'|'||	substr(v_territory_short_name,1,25)
		||'|'||	substr(REC_CUST.ZIP,1,25)
		||'|'||	substr(REC_CUST.PHONE,1,15)
		||'|'||	substr(REC_CUST.FAX,1,15)
		||'|'||	substr(v_site_type,1,2)
		||'|'||	substr(v_active_flag,1,1)
		||'|'||	substr(REC_CUST.CONTACT_NAME,1,200));
	num := num + 1;
  END LOOP;
 
 UTL_FILE.fclose(FILE_CUST);

 commit;

 If num > 0 then
  fnd_file.put_line(fnd_file.log,'Completed the Supplier Extraction Successfully');
  fnd_file.put_line(fnd_file.log,'Total Number of Records Extracted : ' || num);
  fnd_file.put_line(fnd_file.log,'************************************************************************************');
  fnd_file.put_line(fnd_file.output,'************************************************************************************');
 End if;

EXCEPTION
  WHEN utl_file.invalid_path THEN
     fnd_file.put_line(fnd_file.log,'ERROR: utl_file.invalid_path: '||p_output_directory );
     fnd_file.put_line(fnd_file.log, substr(sqlerrm,1,400));
     RAISE PROGRAM_ERROR;
  WHEN utl_file.invalid_mode THEN
     fnd_file.put_line(fnd_file.log,'ERROR: utl_file.invalid_mode: '||p_output_filename);
     fnd_file.put_line(fnd_file.log, substr(sqlerrm,1,400));
     RAISE PROGRAM_ERROR;
  WHEN utl_file.invalid_operation THEN
     fnd_file.put_line(fnd_file.log,'ERROR: utl_file.invalid_operation:'||p_output_filename);
     fnd_file.put_line(fnd_file.log, substr(sqlerrm,1,400));
     RAISE PROGRAM_ERROR;
  WHEN utl_file.invalid_filehandle THEN
     fnd_file.put_line(fnd_file.log,'ERROR: utl_file.invalid_filehandle:'||p_output_filename);
     fnd_file.put_line(fnd_file.log, substr(sqlerrm,1,400));
     RAISE PROGRAM_ERROR;
  WHEN utl_file.write_error THEN
     fnd_file.put_line(fnd_file.log,'ERROR: utl_file.write_error:'||p_output_filename);
     fnd_file.put_line(fnd_file.log, substr(sqlerrm,1,400));
     RAISE PROGRAM_ERROR;
  WHEN OTHERS THEN
     fnd_file.put_line(fnd_file.log,'Error while created interface file: '||p_output_filename || ' '|| SQLERRM);
     fnd_file.put_line(fnd_file.log, substr(sqlerrm,1,400));
     RAISE PROGRAM_ERROR;
END Supplier_Extract;

END XXTC_SUPPLIER_EXTR_PKG;
/
Sample extract file
23428|100215|TESCO Supplier|Y|Mandar|M|Kulkarni|21920|HUF|HUF|AMERICAN|10016|Prepaid|11|Kabul|Afganistan|Kabul||Afghanistan|1234|||04|A|MandarMKulkarni
23428|100215|TESCO Supplier|Y|Satyajit|Y|Gupta|21922|HUF|HUF|AMERICAN|10017|AIR|Aland Islands|Aland Islands|Aland Islands|Aland Islands|Aland Islands|Aland Islands||||04|A|SatyajitYGupta
23432|100215|TEST SUPPLIER|Y|Manish|K|Kanjikar|21927|HUF|HUF|AMERICAN|10001|AIR|111|Afganistan|Afganistan|Afganistan||Afghanistan|999999|||04|I|ManishKKanjikar
23432|100215|TEST SUPPLIER|Y|Thomas||Harper|21928|HUF|HUF|AMERICAN|10001|SHIP|222|Hungary Tesco||Budapest||Hungary|2222222|9980568958|9980568958|04|I|ThomasHarper
23432|100215|TEST SUPPLIER|Y|Divya|A|Shivprasad|21928|HUF|HUF|AMERICAN|10001|SHIP|222|Hungary Tesco||Budapest||Hungary|2222222|9980568958|9980568958|04|I|DivyaAShivprasad
23432|100215|TEST SUPPLIER|Y|Sidd||Sarangi|21932|HUF|HUF|AMERICAN|10008|Paid|666|Andorra|Andorra Branch|Andorra City||Andorra|66666666|99805 68958|99805 68958|04|I|SiddSarangi
23433|100215|TOM SUPPLIER|Y|Manish|K|Kanjikar|21933|HUF|HUF|AMERICAN|10005|RLWY|99999999999999999999|AntarticaAntarticaAntarticaAntartic|AntarticaAntartica|AntarticaAntartica||Antarctica|99999999999999999999|8888888888888|777777777777777|04|I|ManishKKanjikar
23433|100215|TOM SUPPLIER|Y|Jakkula|G|Vennugopal|21936|HUF|HUF|AMERICAN|10012|AIR|11|Hungary|Tesco HU|Budapest||Hungary|89765|4554555|6566565|06|A|JakkulaGVennugopal
End to End Mapping
The table below shows end to end what we are trying to achieve with this interface and is based on the out of the box interface. Mapping will be achieved via an intermediate conversion to the Supplier Common Forms. I.e. Flat file MapTo CommonForms and CommonForms MapTo RIB VendorHdrDesc and VendorAddrDesc. 

This is shown in the mapping Spreadsheet.SYSTEMTABLE FIELD NAMETYPESYSTEMTABLE FIELD NAMETYPE
NOTESOFIPO_VENDORSVENDOR NUMBER “VENDOR_ID” (from SEGMENT1)6 NUMBER Held in IDSOFIPO_VENDOR_SITES_ALL“VENDOR_SITE_ID” (from ATTRIBUTE10)5 NUMBER ORMS
SUPS   SUPPLIER5 NumberKEYPO_VENDORS PO_VENDOR_SITES_ALLVENDOR_NAME
VENDOR_SITE_CODE80 15 VARCHARSUPS   SUP_NAME240 VARCHAR PADPO_VENDOR_CONTACTSFIRST_NAME + MIDDLE NAME + LAST NAME15 + 15 +25SUPS   CONTACT_NAME120 VARCHAR2ONLY FIRST OCCURENCEPO_VENDOR_SITES_ALLPHONE15 VARCHAR2SUPS   CONTACT_PHONE20 VARCHAR2PAD?VENDOR_STATUS1 VARCHAR2ORMSSUPS   CONTACT_PAGERExtract script should set to “I” or “A”SUPS   SUP_STATUS1 VARCHAR2‘A’ OR ‘I’PO_VENDOR_SITES_ALLPAYMENT_CURRENCY_CODE
OR INVOICE_CURRENCY_CODE15 VARCHAR2SUPS   CURRENCY_CODE
FK  to FND_CURRENCIES.CURRENCY_CODE3 VARCHAR2ASUMPTION [both systems are using the same 3 digit code)PO_VENDOR_SITES_ALLLANGUAGE30 VARCHAR2SUPS   LANG FK to LANG LANG.DESCRIPTION VARCHAR2(120)6 NUMBER[ASSUMPTION]
THESE WILL BE THE SAME FORMATPO_VENDOR_SITES_ALLTERMS_IDNUMBERSUPS   TERMS FK TERMS_HEAD.TERMS15 VARCHAR2[ASSUMPTION]
THESE WILL BE THE SAME FORMATPO_VENDOR_SITES_ALLFREIGHT_TERMS_LOOKUP_CODE25 VARCHAR2SUPS   FREIGHT_TERMS30 VARCHAR2[ASSUMPTION]
THESE WILL BE THE SAME FORMATPO_VENDOR_SITES_ALLPREPAID_SUPPLIER (FLEXFIELD)1 VARCHAR2SUPSPREPAY_INVC_IND1 varchar2“y” OR “N” Default is NPO_VENDOR_SITES_ALLCOSTING_DATE
(FLEXFIELD)1 VARCHAR2SUPSTES_ORDER_COSTING1 VARCHAR2“A” OR “D”??CONTACT_EMAIL100 VARCHAR2Default=”UNKNOWN”generatedADDRMODULE4 VARCHAR2‘SUPP’PO_VENDOR_SITES_ALLVENDOR_SITE_ID (ATTRIBUTE10)5 NUMBER ADDRKEY_VALUE_15 NUMBER ADDRSEQ_NONUMBER(4,0)GENERATEDPO_VENDOR_SITES_ALL
“site type” = the extraction script needs to determine this and set the value to a 04 or a 062 VARCHAR2ADDRADDR_TYPE2 VARCHAR2
“04” OR “06”01 =Busines
02= Postal
03=Returns
04=Order
05=Invoice
06=RemittanceADDRPRIMARY_ADDR_INDPO_VENDOR_SITES_ALLADDRESS_LINE135 VARCHAR2ADDRADD_1240 VARCHAR2PADPO_VENDOR_SITES_ALLADDRESS_LINE235 VARCHAR2ADDRADD_2240 VARCHAR2PADPO_VENDOR_SITES_ALLADDRESS_LINE335 VARCHAR2ADDRADD_3240 VARCHAR2PADPO_VENDOR_SITES_ALLCITY25 VARCHAR2ADDRCITY120 VARCHAR2PADPO_VENDOR_SITES_ALLSTATE25 VARCHAR2ADDRSTATE3 VARCHAR2TRUNCATEPO_VENDOR_SITES_ALLZIP20 VARCHAR2ADDRPOST30 VARCHAR2PADPO_VENDOR_SITES_ALLCOUNTRY25 VARCHAR2ADDRCOUNTRY_ID3 VARCHAR2[ASSUMPTION]
ORACLE IS USING A 2 DIGIT ISO CODE FOR COUNTRY
PO_VENDOR_CONTACTSFIRST_NAME + “ “ + Middle_name + “ “  + LastName15+15+25ADDRCONTACT_NAME120 VARCHAR2Default=”UNKNOWN”PO_VENDOR_SITES_ALLPHONE15 VARCHAR2ADDRCONTACT_PHONE20 VARCHAR2PADPO_VENDOR_CONTACTSSITES_ALLFAX15 VARCHAR2ADDRCONTACT_FAX20 VARCHAR2PADPO_VENDOR_SITES_ALLVENDOR_SITE_ID (FROM ATTRIBUTE10)5 NUMBERADDRORACLE_VENDOR_SITE_ID5 NUMBERPO_CONTACTS_ALLEMAIL2000 VARCHAR2SUPSEMAIL_CONTACT100 VARCHAR2
Mapping – Flat File to Common Forms
See Mapping Spreadsheet
Mapping – Common Forms to RIB
See Mapping Spreadsheet
Writing to the IDS
The Vendor\Supplier information is combined in the extract record. For the IDS the Master Vendor\Vendor Site ID hierarchy has to be reassembled from the incoming records. 

The interface creates an IDS master Vendor record using the 6 digit Vendor Number which is in field SEGMENT1. This has a SupplierType of "V".

The interface then creates the IDS child supplier records using the 5 digit Vendor_Site_ID which is held in field ATTRIBUTE10. This has a SupplierType of "S"

The interface will handle the fact that there can be multiple records coming in with the same 6 digit Vendor Number from SEGMENT1 but with differing Vendor Site IDs held in ATTRIBUTE10. 

Supplier activities are “Ordering” (we order from them) or “Paying” (we pay them) using the codes 04 and 06 from the codes of this nature in ORMS, i.e.:

01 = Business
02 = Postal
03 = Returns
04 = Order
05 = Invoice
06 = Remittance

SupplierType is mapped from SITE_TYPE on the extract. For the States this will always be This will normally be a 04.
In the IDS Table AddressforSupplierActivity
set Primary_Address_Ind to “Y”
set Sequence_in_Supplier_Activity to 1

Stored Procedures
The stored procedure that writes Vendors to the IDS will treat all occurences of the Vendor in the incoming record set as updates except where it detects that it is the first occurrence in which case the procedure will make an insert. 
Common Form Schemas
Common Forms and the IDS will be baselined to VERSION 5 for release 1 of this interface.
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/1%20-%20Design/Common%20Forms/Common%20Forms%202007-01-03/TOM.Common.Suppliers.xsd" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/1%20-%20Design/Common%20Forms/Common%20Forms%202007-01-03/TOM.Common.Suppliers.xsd

 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/1%20-%20Design/Common%20Forms/Common%20Forms%202007-01-03/TOM.Common.Suppliers.xsd" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/1%20-%20Design/Common%20Forms/Common%20Forms%202007-01-03/TOM.Common.Address.xsd

OFi Source Data
For information see the manuals below. It should be noted that there are fields in the implemented database that are not included in the Technical Documentation e.g. EMAIL in VENDOR_CONTACTS. The OFi extract is based on the physical implementation of the database.  
Accounts Payable Technical Reference Manual (aptrm.pdf) :-
Table and View definitions -
PO_Vendors
PO_Vendor_Sites_All
PO_Vendor_Contacts
These are copied below for convenience.


























RIB RMS message format
See RIB Integration Guide 12011\XML_schemas for the latest formats. The schema for VendorHdrDesc and VendorAddrDesc is given below for convenience:-
(This will change for the 12T version)

Application Name: Retail Management System 
Version 12.0.0 
XML-Schema or Node Name:VendorDesc.xsd

Tag Name
Table Name
Column Name
API Req
Description
VendorHdrDesc
*
*
Yes 
Child node - see below.
VendorAddrDesc
*
*
Yes 
Child node - see below. 
Application Name: Retail Management System 
Version 12.0.0 
XML-Schema or Node Name:VendorHdrDesc

Tag Name
Table Name
Column Name
API Req
Description
supplier
sups
supplier
Yes 
Unique identifying number for a supplier.
sup_name
sups
sup_name
Yes 
The supplier's trading name.
contact_name
sups
contact_name
No 
The contact name for the supplier.
contact_phone
sups
contact_phone
No 
Contact phone number for the supplier.
contact_fax
sups
contact_fax
No 
Fax number for supplier.
contact_pager
sups
contact_pager
No 
Pager number for supplier.
sup_status
sups
sup_status
No 
A code to indicate supplier status. A = Active, I = Inactive.
qc_ind
sups
qc_ind
No 
Determines whether orders from this supplier will default as requiring quality control.
qc_pct
sups
qc_pct
No 
The percentage of items per receipt that will be marked for quality checking.
qc_freq
sups
qc_freq
No 
The frequency for which items per receipt will be marked for quality checking.
vc_ind
sups
vc_ind
No 
Determines whether orders from this supplier will default as requiring vendor control.
vc_pct
sups
vc_pct
No 
The percentage of items per receipt that will be marked for vendor checking.
vc_freq
sups
vc_freq
No 
The frequency for which items per receipt that will be marked for vendor checking.
currency_code
sups
currency_code
No 
A code identifying the currency the supplier uses for business transactions.
lang
sups
lang
No 
A code for the supplier's preferred language.
terms
sups
terms
No 
A code indicating the payment terms that will default when an order is created for the supplier. 
freight_terms
sups
freight_terms
No 
A code indicating what freight terms will default when an order is created for the supplier.
ret_allow_ind
sups
ret_allow_ind
No 
Indicates whether or not the supplier will accept returns.
ret_auth_req
sups
ret_auth_req
No 
Indicates if returns must be accompanied by an authorization number when sent back to the vendor.
ret_min_dol_amt
sups
ret_min_dol_amt
No 
Contains a value if the supplier requires a minimum value to be returned in order to accept the return. Stored in the supplier's currency.
ret_courier
sups
ret_courier
No 
Contains the name of the courier that should be used for returns to the supplier.
handling_pct
sups
handling_pct
No 
The percent to be multiplied by an order's total cost to determine the handling cost for the return.
edi_po_ind
sups
edi_po_ind
No 
Indicates whether purchase orders will be sent to the supplier via Electronic Data Interchange.
edi_po_chg
sups
edi_po_chg
No 
Indicates whether purchase order changes will be sent to the supplier via EDI.
edi_po_confirm
sups
edi_po_confirm
No 
Indicates whether acknowledgements of purchase orders will be sent to the supplier via EDI.
edi_asn
sups
edi_asn
No 
Indicates whether the supplier will send Advance Shipment Notifications electronically.
edi_sales_rpt_freq
sups
edi_sales_rpt_freq
No 
This field contains the EDI sales report frequency for the supplier. Valid values are D = Daily, W = Weekly.
edi_supp_available_ind
sups
edi_supp_available_ind
No 
Indicates whether the supplier will send availability via EDI.
edi_contract_ind
sups
edi_contract_ind
No 
Indicates whether contracts will be sent to the supplier via EDI.
edi_invc_ind
sups
edi_invc_ind
No 
Indicates whether invoices, debit memos and credit note requests will be sent to/from the supplier via EDI.
cost_chg_pct_var
sups
cost_chg_pct_var
No 
Contains the cost change variance by percent. If an EDI cost change is accepted and falls within these boundaries, it will be approved when inserted into the cost change dialog.
cost_chg_amt_var
sups
cost_chg_amt_var
No 
Contains the cost change variance by amount. If an EDI cost change is accepted and falls within these boundaries, it will be approved when inserted into the cost change dialog.
replen_approval_ind
sups
replen_approval_ind
No 
Indicates whether contract orders for the supplier should be created in Approved status.
ship_method
sups
ship_method
No 
The method used to ship the items on the purchase order from the country of origin to the country of import. Check the RMS data model for valid values.
payment_method
sups
payment_method
No 
Indicates how the purchase order will be paid. Valid options are: LC (Letter of Credit), WT (Wire Transfer), OA (Open Account).
contact_telex
sups
contact_telex
No 
The telex number for the supplier's contact.
contact_email
sups
contact_email
No 
Contains an email address for the supplier's representative contact.
settlement_code
sups
settlement_code
No 
Indicates which payment process method is used for the supplier. Check the RMS data model for valid values.
pre_mark_ind
sups
pre_mark_ind
No 
Indicates whether or not the supplier has agreed to break an order into separate boxes (and mark them) that can be shipped directly to the stores.
auto_appr_invc_ind
sups
auto_appr_invc_ind
No 
Indicates whether or not the supplier's invoice matches can be automatically approved for payment.
dbt_memo_code
sups
dbt_memo_code
No 
Indicates when a debit memo will be sent to the supplier to resolve a discrepancy. Y = Yes, N = No, L = only if a credit note is not sent by the invoice due date.
freight_charge_ind
sups
freight_charge_ind
No 
Indicates whether a supplier is allowed to charge freight costs to the client.
auto_appr_dbt_memo_ind
sups
auto_appr_dbt_memo_ind
No 
Indicates whether debit memos sent to the supplier can be automatically approved on creation.
inv_mgmt_lvl
sups
inv_mgmt_lvl
No 
Indicates whether supplier inventory management information can be set up at the supplier/deparment level or just at the supplier level.
backorder_ind
sups
backorder_ind
No 
Indicates if backorders or partial shipments will be accepted.
vat_region
sups
vat_region
No 
The VAT region for the supplier.
prepay_invc_ind
sups
prepay_invc_ind
No 
Indicates whether or not all invoices for the supplier can be pre-paid invoices.
service_perf_req_ind
sups
service_perf_req_ind
No 
Indicates if the supplier's services must be confirmed as performed before paying an invoice from that supplier.
invc_pay_loc
sups
invc_pay_loc
No 
Indicates where invoices from this supplier are paid - at the store ('S') or centrally through corporate accounting ('C').
invc_receive_loc
sups
invc_receive_loc
No 
Indicates where invoices from this supplier are received - at the store ('S') or centrally through corporate accounting ('C').
addinvc_gross_net
sups
addinvc_gross_net
No 
Indicates if the supplier invoice lists items at gross cost ('G') or net cost ('N').
delivery_policy
sups
delivery_policy
No 
Contains the delivery policy of the supplier. Valid values come from the DLVY code on code_head/code_detail.
comment_desc
sups
comment_desc
No 
Any miscellaneous comments associated with the supplier.
default_item_lead_time
sups
default_item_lead_time
No 
Holds the default lead time for the supplier. The lead time is the time the supplier needs between receiving an order and having the order ready to ship. This value will be defaulted to item/supplier relationships.
duns_number
sups
duns_number
No 
The Dun and Bradstreet number of the supplier.
duns_loc
sups
duns_loc
No 
The Dun and Bradstreet number of the location of the supplier.
bracket_costing_ind
sups
bracket_costing_ind
No 
This field will determine if the supplier uses bracket costing pricing structures.
vmi_order_status
sups
vmi_order_status
No 
Determines the status in which any inbound PO's from this supplier are created. A NULL value indicates that the supplier is not a VMI supplier.
end_date_active
*
*
No 
Not used by RMS.
dsd_supplier_ind
sups
dsd_ind
No 
Specifies whether or not DSD shipments can be created for the supplier.
Application Name: Retail Management System 
Version 12.0.0 
XML-Schema or Node Name:VendorAddrDesc

Tag Name
Table Name
Column Name
API Req
Description
module
addr
module
Yes 
Indicates the data type that the address is attached to. In this case, it will always be 'SUPP'.
key_value_1
addr
key_value_1
Yes 
Holds the id the address is attached to. In this case, it will be the supplier number.
key_value_2
*
*
No 
Field not used.
seq_no
*
*
No 
Field not used.
addr_type
addr
addr_type
Yes 
The address type. Valid values (e.g. 01 - Business, 02 - Postal, etc.) are on the add_type table.
primary_addr_ind
*
*
No 
Field not used.
add_1
addr
add_1
Yes 
The first line of the address.
add_2
addr
add_2
No 
Contains the second line of the address.
add_3
addr
add_3
No 
Contains the third line of the address.
city
addr
city
Yes 
Contains the name of the city associated with the address.
state
addr
state
No 
Contains the state abbreviation for the address.
country_id
addr
country_id
Yes 
Contains the country where the address exists.
post
addr
post
No 
The zip code for the address.
contact_name
addr
contact_name
No 
The name of the contact at this address.
contact_phone
addr
contact_phone
No 
The phone number for this address.
contact_telex
addr
contact_telex
No 
The telex number for this address.
contact_fax
addr
contact_fax
No 
The fax number for this address.
contact_email
addr
contact_email
No 
The email address for this address.
oracle_vendor_site_id
*
*
No 
Field not used.
OracleOUDesc
*
*
No 
Child node.
Application Name: Retail Management System 
Version 12.0.0 
XML-Schema or Node Name:OracleOUDesc

Tag Name
Table Name
Column Name
API Req
Description
OUDtlDesc
*
*
No 
Child node.
Application Name: Retail Management System 
Version 12.0.0 
XML-Schema or Node Name:OUDtlDesc

Tag Name
Table Name
Column Name
API Req
Description
ou_id
org_unit_add_site
org_unit_id
Yes 
The Oracle Financials org unit associated with this address.
site_id
org_unit_addr_site
oracle_vendor_site_id
Yes 
The Oracle Financials site id associated with this address.













 DOCPROPERTY "Doc Dept"  \* MERGEFORMAT Group Technology & Architecture	 TITLE  \* MERGEFORMAT Information Services - High Level Information Requirements

COMMERCIAL IN CONFIDENCE



Version  DOCPROPERTY "Doc Version"  \* MERGEFORMAT 1.0 REF DOC_STATUS 	Page:  PAGE  \* MERGEFORMAT vi of  NUMPAGES 48	Date:  SAVEDATE \@ "d MMM yyyy" 27 Feb 2007

 DOCPROPERTY "Doc Dept"  \* MERGEFORMAT Group Technology & Architecture	 TITLE  \* MERGEFORMAT Information Services - High Level Information Requirements

COMMERCIAL IN CONFIDENCE

 
The information contained in this document represents the current view of Tesco Stores Ltd on the issues discussed as of the date of publication. Because Tesco must respond to changing market conditions, it should not be interpreted to be a commitment on the part of Tesco, and Tesco cannot guarantee the accuracy of any information presented after the date of publication.
This document is for informational purposes only. TESCO MAKES NO WARRANTIES, EXPRESS OR IMPLIED, IN THIS Document.
©  SAVEDATE \@ "yyyy" 2007 Tesco Stores Ltd. All rights reserved.
Tesco, is either registered trademarks or trademarks of Tesco Plc in the United Kingdom and/or other countries.



 DOCPROPERTY "Doc Dept"  \* MERGEFORMAT Group Technology & Architecture	 TITLE  \* MERGEFORMAT Information Services - High Level Information Requirements

COMMERCIAL IN CONFIDENCE



Version  DOCPROPERTY "Doc Version"  \* MERGEFORMAT 1.0 REF DOC_STATUS 	Page:  PAGE  \* MERGEFORMAT 7 of  NUMPAGES 48	Date:  SAVEDATE \@ "d MMM yyyy" 27 Feb 2007

 DOCPROPERTY "Doc Dept"  \* MERGEFORMAT Group Technology & Architecture	 TITLE  \* MERGEFORMAT Information Services - High Level Information Requirements

COMMERCIAL IN CONFIDENCE

 
The information contained in this document represents the current view of Tesco Stores Ltd on the issues discussed as of the date of publication. Because Tesco must respond to changing market conditions, it should not be interpreted to be a commitment on the part of Tesco, and Tesco cannot guarantee the accuracy of any information presented after the date of publication.
This document is for informational purposes only. TESCO MAKES NO WARRANTIES, EXPRESS OR IMPLIED, IN THIS Document.
©  SAVEDATE \@ "yyyy" 2007 Tesco Stores Ltd. All rights reserved.
Tesco, is either registered trademarks or trademarks of Tesco Plc in the United Kingdom and/or other countries.



 DOCPROPERTY "Doc Dept"  \* MERGEFORMAT Group Technology & Architecture	 TITLE  \* MERGEFORMAT Information Services - High Level Information Requirements

COMMERCIAL IN CONFIDENCE



Version  DOCPROPERTY "Doc Version"  \* MERGEFORMAT 1.0 REF DOC_STATUS 	Page:  PAGE  \* MERGEFORMAT 47 of  NUMPAGES 48	Date:  SAVEDATE \@ "d MMM yyyy" 27 Feb 2007

 DOCPROPERTY "Doc Dept"  \* MERGEFORMAT Group Technology & Architecture	 TITLE  \* MERGEFORMAT Information Services - High Level Information Requirements

COMMERCIAL IN CONFIDENCE

 
The information contained in this document represents the current view of Tesco Stores Ltd on the issues discussed as of the date of publication. Because Tesco must respond to changing market conditions, it should not be interpreted to be a commitment on the part of Tesco, and Tesco cannot guarantee the accuracy of any information presented after the date of publication.
This document is for informational purposes only. TESCO MAKES NO WARRANTIES, EXPRESS OR IMPLIED, IN THIS Document.
©  SAVEDATE \@ "yyyy" 2007 Tesco Stores Ltd. All rights reserved.
Tesco, is either registered trademarks or trademarks of Tesco Plc in the United Kingdom and/or other countries.





















Master



















Trait

Supplier 3

Supplier  2

Supplier 1

Supplier 
Supplier 2

Supplier 
Supplier 3

Supplier
Supplier 1

Master
 Supplier



SUP

PO_VENDORS

Supplier Id, 
Receipts

Master Vendor

PO_VENDOR_SITES_ALL

Vendor Site 1


System

Supplier Id Size

OFI

30

RMS

10

GFO

5

ORWMS

10

Storeline

8



Supplier 3


ORMS

Store Systems

Store Systems


Raw Sales

Vendor Site 3


Supplier Id

Supplier 2

Supplier 1

FINANCIALS

Vendor Site 2

ORWMS











