		









`


TOM Integration

Interface Specification
Advanced Shipping Notice
From TIMS to RMS, RWMS


[J023]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
22/01/2007
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:
Supriyo Chakraborty

Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
22-01-2007
0.1D
Draft
Sankar G
12-02-2007
0.2D
Draft
Sankar G
16-02-2007
0.3D
Draft





Reviewers

Name
Date
Version
Position
Supriyo Chakraborty
22-01-2007
0.1D

Tomas Harper
12-02-2007
0.1D
Solution Architect










At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Andrew Barker
Position
Solution Architect
Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version
Andrew Barker
<Issue Date>
<Version No>
David Onyett


Venkateswara Rao









Document Source

Related Documents: 
File Name: 
1. RIB-intg/Documentation WIP/Integration Bus/12.0/Integration guide /ASNOutToASNOutATTAFR.htm
2. RIB-intg/Documentation WIP/Integration Bus/12.0/Integration guide/XML/ASNInDesc.XSD


Information Architecture Context diagram
J023 - Information Context Diagram - PO ASN (TIMS to RMS)

Mapping spreadsheet
J023-ASN Mapping Document
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 6
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 6
1.2	Background	 PAGEREF _Toc153956171 \h 6
1.3	Scope	 PAGEREF _Toc153956172 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 7
2.2	Architecture	 PAGEREF _Toc153956175 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153956177 \h 9
3.1	Scope	 PAGEREF _Toc153956178 \h 9
3.2	Source Message Schema	 PAGEREF _Toc153956179 \h 9
3.3	Message Transport Details	 PAGEREF _Toc153956180 \h 9
3.4	Naming and Configuration	 PAGEREF _Toc153956181 \h 10
3.5	Environment and Security Context	 PAGEREF _Toc153956182 \h 10
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153956183 \h 12
4.1	Scope	 PAGEREF _Toc153956184 \h 12
4.2	Data Validation	 PAGEREF _Toc153956185 \h 12
4.3	Filtering	 PAGEREF _Toc153956186 \h 12
4.4	Mapping	 PAGEREF _Toc153956187 \h 12
4.5	Target Message Schema	 PAGEREF _Toc153956188 \h 12
4.6	Message Format	 PAGEREF _Toc153956189 \h 14
4.7	Message Transport Details	 PAGEREF _Toc153956190 \h 14
4.8	Naming and Configuration	 PAGEREF _Toc153956191 \h 15
4.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 15
4.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 15
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153956194 \h 16
5.1	Scope	 PAGEREF _Toc153956195 \h 16
5.2	Data Validation	 PAGEREF _Toc153956196 \h 16
5.3	Filtering	 PAGEREF _Toc153956197 \h 16
5.4	Mapping	 PAGEREF _Toc153956198 \h 16
5.5	Target Message Schema	 PAGEREF _Toc153956199 \h 16
5.6	Message Transport Details	 PAGEREF _Toc153956200 \h 16
5.7	Environment and Security Context	 PAGEREF _Toc153956201 \h 16
6	Testing Deliverables	 PAGEREF _Toc153956202 \h 17
7	Deployment	 PAGEREF _Toc153956203 \h 18
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 19
8.1	Assumptions	 PAGEREF _Toc153956205 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 19
Appendix A Volumes	 PAGEREF _Toc153956207 \h 20
Appendix B Glossary	 PAGEREF _Toc153956208 \h 21
Appendix C Document Control	 PAGEREF _Toc153956209 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t for the Purchase Order, Advanced Shipping Notice (ASN) data between the Tesco Internet Management System (TIMS) and Retek Merchandising System (RMS), Retek Warehouse Management System (RWMS).

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US implementations.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including TIMS and RMS, RWMS. To achieve this functionality, high level process flow architecture has been designed and approved by TESCO Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Purchase Order ASN data from TIMS into RMS, RWMS.
Scope
The Interface Specification covers:

audit requirements across the interface
security requirements across the interface
timing/frequency requirements or constraints
support requirements
archiving
the data format to be used for the interface at each stage (e.g. xml messages)
the normal processing required at each stage
recovery from failure required at each stage
volumes.

Note that it is Tesco strategy to avoid placing any business logic in integration layer processing.
Description and Requirements for the End-to-End Interface
Description of the End-to-End Interface
The interface is a batch extract of Advanced Shipping Notice (ASN), from a flat file (delimited by pipe - |) via TIMS Integration Layer and uploads into the RMS, RWMS using RIB. The Upload is a full upload in nature.

The interface is meant to run at a pre-configured time interval, which on completion is expected to produce a XML file (containing reference data records) onto the shared location. The XML file will pass through RIB assembler and transferred to RMS location through JMS adaptor. This shared location would be monitored by RMS and RWMS systems Interface at the same interval. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into RMS, RWMS using RIB.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 
Architecture

Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data in the form of flat file from the shared location at TIMS side and delivering the resulting to another shared location at RMS side before the identified cut-off time. The interface should run on real time basis. 
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. 
Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
N/A 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope
TIMS pushes a delimited (delimiter - | (pipe)) flat file containing the ASN data, to a predefined shared location. The flat file is created at a predefined time interval. Once the file is created at the shared location, BizTalk picks up the file, transforms the file into a XML file and pass the file through RIB assembler delivers the file to another shared location through JMS adaptor for further processing. 

Source Message Schema

Code
Optional
Type
Description
ASN Header
RECTYPE

CHAR(1)
Type of record “H”
DH_DOCNO

CHAR(15)
ASN number
DH_DATETIME

TIMESTAMP
Date, when ASN created
DH_PONO

NUMBER(8)
Associated PO number
DH_DLVDATE

TIMESTAMP
Date of delivery
DH_SUPPID

NUMBER(9)
Supplier ID
DH_SUPPTID

CHAR(20)
Supplier VAT registration number
DH_SUPPCID

CHAR(20)
Supplier company registration number
DH_SITEDLV

NUMBER(10)
Delivery site ID
DH_VEHICLE

CHAR(35)
Carrier license ID
DH_DLVMODE

CHAR(1)
Delivery mode 
DH_TOTALQTY

NUMBER(8)
Total delivered qty in PU
DH_PALLETS

NUMBER(8)
Total of pallets
DH_EPALLETS

NUMBER(8)
Total of EU pallets
DH_CHPALLETS

NUMBER(8)
Total of CHEP1 pallets
Begin Group ‘A’
1:*
ASNItem will repeat multiple times under ASNHeader
ASN Item
RECTYPE

CHAR(1)
Type of record “L”
DI_EAN

CHAR(13)
UPC/EAN/GS21 item ID
DI_TPN

CHAR(13)
Tesco product number
DI_SPN

CHAR(13)
Supplier product number
DI_DESC

CHAR(35)
Product description
DI_QTY  

NUMBER(8)
Quantity in trading units
DI_UNIT

CHAR(30)
UOM of trading unit
DI_FREE

NUMBER(8)
Free stock
DI_UNITCASE

NUMBER(7)
Number of units per case
DI_TOTALCASE

NUMBER(7)
Total of cases
End Group ‘A’




Message Format
The source message is in the form of pipe | delimited file from TIMS is getting converted into the target file format in a package. The following sample message format is the source message format. 

The sample file will be attached.

Message Transport Details

Feature
Specification
Additional Information
Source System Name
TIMS

Source Platform / OS
LINUX

Source Physical Location


Source Underlying Data Storage Technology


Target System Name
Biztalk 2006

Target Platform / OS
Biztalk 2006 Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
RTI Adapter		

Data Format.
XML			
Delimited		
Positional		

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous		
Asynchronous		
Bulk Data		

Real-time/Scheduled Batch
Not yet decided

Archiving
There is no requirement to archive the messages.

Logging
Logging should occur, such that the message can be recreated if necessary.

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

Biztalk – 2006
Package Name: 
BizTalk Procedure
Name

<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
Biztalk monitors the file in the configured location for every new file and submits the same to the remote UNIX share via FTP. The resultant file is a XML file.
Data Validation
Data Validation will be done by the target RMS system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Target Message Schema in XML format:
 EMBED Package  
The Description of the fields as mentioned in the XSD file:

Code
Optional
Type
Description
ASNInDesc
to_location
 
Varchar(10)
Contains the location that the shipment will be delivered to.
From_location
 
Varchar(10)
Not used by RMS.
asn_nbr
 
Varchar(30)
Holds the advance shipping notice number associated with a shipment.
asn_type
 
Varchar(1)
This field is used to determine the ship origin. If asn_type is 'C', ship_origin will be set to '6' (ASN UCC-128) upon insert to the SHIPMENT table. Otherwise, SHIP_ORIGIN is defaulted to '0' (ASN Shipment). 
container_qty
 
Number(6)
Not used by RMS.
bol_nbr
 
Varchar(17)
Holds the transaction sequence number on the input message from the receiving PO or transfer process.
shipment_date
 
RIBDate
This field contains the date the transfer or PO was shipped.
est_arr_date
 
RIBDate
This field contains the estimated arrival date of a vendor PO shipment. It is updated by EDIUP856. It is used for vendor/lead time analysis.
Ship_address1
 
Varchar(240)
Not used by RMS.
Ship_address2
 
Varchar(240)
Not used by RMS.
Ship_address3
 
Varchar(240)
Not used by RMS.
Ship_address4
 
Varchar(240)
Not used by RMS.
Ship_address5
 
Varchar(240)
Not used by RMS.
Ship_city
 
Varchar(120)
Not used by RMS.
ship_state
 
Varchar(3)
Not used by RMS.
Ship_zip
 
Varchar(30)
Not used by RMS.
Ship_country_id
 
Varchar(3)
Not used by RMS.
trailer_nbr
 
Varchar(12)
Not used by RMS.
seal_nbr
 
Varchar(12)
Not used by RMS.
carrier_code
 
Varchar(4)
Contains the courier that will deliver the shipment.
vendor_nbr
 
Varchar(10)
This element is used to validate the order number(s) in ASNInPO (ASNInPO.po_nbr). The order number must be in the table ORDHEAD, in either the ORDER_NO column or VENDOR_ORDER_NO column. 
Ship_pay_method
 
Varchar(2)
Used to validate the order number(s) in ASNInPO (ASNInPO.po_nbr). The ship_pay_method in the message must match the value of the order's SHIP_PAY_METHOD in RMS (ORDHEAD table.) If the message field is blank, the ORDHEAD value must be NULL.
ASNInPO
 
 
*
comments
 
Varchar(2000)
Not used by RMS.
ASNInPO
po_nbr
 
Varchar(10)
Identifies the order number which relates to the goods delivered in the shipment. Validated against the ORDHEAD table, and also the SHIPMENT table if the message applies to an existing shipment.
doc_type
 
Varchar(1)
Not used by RMS.
not_after_date
 
RIBDate
Contains the last date that delivery of the order will be accepted.
comments
 
Varchar(2000)
Not used by RMS.
ASNInCtn
 
 
*
ASNInItem
 
 
*
ASNInCtn
Final_location
 
Varchar(10)
This will be the final destination of the carton. For a cross-dock order this will be the allocation location, otherwise it will be the direct to order location.
container_id
 
Varchar(20)
Holds the UCC-128 carton number.
container_weight
 
Number(12)
Not used by RMS.
container_length
 
Number(12)
Not used by RMS.
container_width
 
Number(12)
Not used by RMS.
container_height
 
Number(12)
Not used by RMS.
container_cube
 
Number(12)
Not used by RMS.
expedite_flag
 
Varchar2(1)
Not used by RMS.
in_store_date
 
RIBDate
Not used by RMS.
rma_nbr
 
Varchar(20)
Not used by RMS.
tracking_nbr
 
Varchar(25)
Not used by RMS.
freight_charge
 
Number(20)
Not used by RMS.
master_container_id
 
Varchar(20)
Not used by RMS.
ASNInItem
 
 
*
comments
 
Varchar(2000)
Not used by RMS.
ASNInItem
Final_location
 
Varchar(10)
Required if the order's pre_mark_ind is 'Y'. Validated against the ALLOC_DETAIL table. There needs to be at least one allocation with the same ORDER_NO that is in the ASNIn message, and the same TO_LOC as the final_location.
Item_id
 
Varchar(25)
Unique identifier for the item. Either vpn, item_id, or ref_item must be specified in the message.
unit_qty
 
Number(12)
Contains the number of items expected to be received based on the supplier's ASN for this Item/Shipment combination.
priority_level
 
Number(1)
Not used by RMS.
Vpn
 
Varchar2(30)
Used to find the Retek item number, found on the ITEM_SUPPLIER table. Either vpn, item_id, or ref_item must be specified in the message.
Order_line_nbr
 
Number(4)
Not used by RMS.
lot_nbr
 
Varchar(12)
Not used by RMS.
ref_item
 
Varchar(25)
Contains a reference item to the item field. Either vpn, item_id, or ref_item must be specified in the message.
distro_nbr
 
Varchar(10)
Not used by RMS.
distro_doc_type
 
Varchar(1)
Not used by RMS.
container_qty
 
Number(6)
Not used by RMS.
comments
 
Varchar(2000)
Not used by RMS.
Structure of the ASNDesc.XML


Message Format
The source message is a pipe | delimited flat file from TIMS and is getting converted into the target file format for RMS & RWMS in a package. The target message is a XML file. 

4.7 Message Transport Details 
For messages destined for RIB system, the following applies.	

Feature
Specification
Additional Information
Source System Name
BizTalk 2006

Source Platform / OS
BizTalk 2006 Server

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
RMS, RWMS

Target Platform / OS
IBM AIX

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
JMS Adapter 			

Data Format

RIB Message			
XML  				
Delimited 			
Positional 			

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous 			
Asynchronous 			
Bulk Data 			

Real-time/Scheduled Batch
Real-time

Archiving
There is no archiving requirement

Logging
Should logs be kept of all actions? For how long should these be stored?
Logging should occur, such that the message can be recreated if necessary.

Error Handling
Not yet decided

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

Biztalk 2006
Instruction Name: 
Instruction Details
Description
To be determined
Enabled
True
Type

Operational Window
Schedule
N/A
Enabled
False
Host Details
Account
To be determined 
Operational Details
Worker Threads

Priority

Batch Size

Period

Retry Attempts

Timeout

Require Data Send

Exception Management
Treat Fatal Adapter Exception As

Treat Unhandled Exceptions As



Environment and Security Context
Account details will be included here once we have visibility of the environments.

Non-Functional Requirements
On successful delivery of the file to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure the file should be written to the failed files location, and an alert should be raised.


Processing required in the <third stage of the interface>
Scope
There is no intermediate staging is required for this interface. So this section is not applicable.
Data Validation
Not Required

Filtering
Not Required

Mapping
Not Required

Target Message Schema
Not Required

Message Transport Details
Not Required

Naming and Configuration
Not Required

Environment and Security Context
Not Required

Non-Functional Requirements

Not RequiredTesting Deliverables
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption





Outstanding Issues
ID
Issue
To be addressed by
1
File naming format to be confirmed
Tomas Harper
2
Server Physical Location of the server and file 
Tomas Harper
3
Error handling
Tomas Harper





Volumes
Glossary

Acronym
Term
Description
EAI
Enterprise Application Integration
The process of meeting the data requirements of applications by providing a message based transport from disparate data sources across all forms of enterprise technology.
EAI Layer
Enterprise Application Integration Layer
Refers to the integration services provided to implement EAI. In contrast to the EIA Layer for data services. See below.
EIA
Enterprise Information Architecture
Creation of a strategic single view of data across the enterprise.
Interface
Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.
RMS
Retek Merchandising System
Retek Merchandising System is getting installed for TESCO Merchandising operations in US. This system will governs the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
RIB
Retek Integration Bus
This is an integration Interface between the Oracle Retek modules.
RWMS
Retek Warehouse Management System
RWMS is getting installed in US. This module is going to manage warehouse operations.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
22-Jan-2006
0.1D
Draft
Sankar G
12-Feb-2007
0.2D
Draft











Related Documents

Author	
Date
Version
Title
To be filled

















Distribution

Name
Position
Approver/Contributor/Other
Nathan Smith
Enterprise Architect

Andrew Barker
Engagement Architect

David Onyett
Project Lead

Thomas HarperSolution Architect























	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 9 of  NUMPAGES 23	Date:  SAVEDATE \@ "d MMM yyyy" 12 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































