		









`


TOM Integration

Interface Specification
Allocation Information for PBL Orders
In intermediate storage
From RMS to IDS


[J113]






Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
13/02/2007
Version:
0.1
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:
Sankar G

Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
13/02/2007
0.1D
Draft













Reviewers

Name
Date
Version
Position
Sankar G
13/02/2007
0.1D
Draft














At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Rob McDonagh
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
Adrian Hinks
<Issue Date>
<Version No>
David Onyett


Venkateswara Rao


Rob McDonagh






Document Source

Related Documents:
rib-120-intg\Documentation WIP\Integration Bus\12.0\Integration Guide\XML\AllocDesc.xsd


Information Architecture Context diagram
Will be provided

Mapping spreadsheet
J113-Allocation Information to IDS Mapping Document
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 6
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 6
1.2	Background	 PAGEREF _Toc153956171 \h 6
1.3	Scope	 PAGEREF _Toc153956172 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 7
2.2	Architecture	 PAGEREF _Toc153956175 \h 9
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153956177 \h 10
3.1	Scope	 PAGEREF _Toc153956178 \h 10
3.2	Source Message Schema	 PAGEREF _Toc153956179 \h 10
3.3	Message Transport Details	 PAGEREF _Toc153956180 \h 11
3.4	Naming and Configuration	 PAGEREF _Toc153956181 \h 11
3.5	Environment and Security Context	 PAGEREF _Toc153956182 \h 12
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153956183 \h 13
4.1	Scope	 PAGEREF _Toc153956184 \h 13
4.2	Data Validation	 PAGEREF _Toc153956185 \h 13
4.3	Filtering	 PAGEREF _Toc153956186 \h 13
4.4	Mapping	 PAGEREF _Toc153956187 \h 13
4.5	Target Message Schema	 PAGEREF _Toc153956188 \h 13
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
The purpose of this document is to describe the interfacing requirements w.r.t the Allocation Details for PBL Orders between Oracle Retail Merchandising System (ORMS) and Integrated Data Store (IDS). The necessity for storing the information in Integration layer is to reference Purchase Order (PO) number and pickup the Original PO Quantity when the (Bill of Laden) BOL data sent back to GFO by other interfaces in the loop.

The document is sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is required for both US and Turkey implementations.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORMS and IDS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Allocation Details for PBL Orders from ORMS into IDS.

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
The interface is to upload the Allocation Details for PBL orders from ORMS into IDS. The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Allocation Details for PBL Orders from RMS in the form of XML message. This message is actually a RIB message, which ORMS is communicating to ORWMS about the Allocation details. JMS adaptor pickup the RIB message and converts into standard XML message and delivers the message to BizTalk. On completion of this process BizTalk is expected to upload the Allocation Details into tables in IDS through SQL adaptor. 

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

History behind this interface
1.  The Pick By Line (PBL) orders will get created in GFO based on forecasting module. Since the GFO is a forecasting system the proper purchase order document will not be created at GFO. GFO will flow the Procurement order data to RMS. 
2(b)Appropriate documents will get created at RMS. These documents will be sent as allocation details along with the PO number to GFO and RWMS. In turn the PO details and allocation details will be sent to Suppliers via TIMS interface. The allocation data sent by RMS will be dealt with allocation number further on in RWMS. So the PO number link which sent by RMS was lost. 
3(a)Suppliers will communicate their Advance Shipping Notice (ASN IN) via TIMS interface to RIB. From RIB, the message will flow into RMS and RWMS.
3(b)Based on ASN IN information RMS will send PO receivable quantities to GFO.
4(a)GFO will re-allocate the Stock Share quantities and send as final stock share based on the PO receivable quantities received from RMS. 
4(b)After RMS received the final stock share from GFO and correct the allocation details and send it to RWMS for allocations based on its receiving stocks.
5(a)The Bill of Lading (BOL) information will be sent to Storeline. 
5(b)Billing of Laden (BOL) information will be sent to GFO to update Store stock.

Gap: 
BOL data sent by RWMS will carry only Distro No which is equivalent to Allocation No sent by RMS. The other important data which is PO data is getting missed in the loop. GFO needs PO No for further process. 
GFO needs the information that what is the original PO quantity against supplied quantity. The BOL data didn’t carry Original PO quantity information.

Solution:
2(c)The PO and the allocation data sent by RMS through RIB to RWMS, will be captured through JMS adaptor and stored in a Intermediate Storage. 
4(c)The fresh allocation data from GFO based on the ASN IN from suppliers will get altered in the Intermediate Storage. 

Following data flow diagram is self explanatory


Architecture


Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of capturing the RIB message from ORMS side and inserting the information into the tables in IDS before the identified cut-off time. The interface should run on real time basis. 
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
ORMS creates an XML file as RIB message containing Allocation Details for PBL Orders and places the file where ORWMS will pickup as input file. JMS adaptor also pickup the same RIB Message and converts into standard XML format and deliver the file to BizTalk. Biztalk in turn will process the file and update the IDS tables using SQL Adapter. 

Source Message Schema
The source message is created at RMS side in the form of XML file. The XSD file containing the field definition is imbedded below.

 EMBED Package  
The tabular form of the file with the grouping information is given below:

Field Type
Field Name
Optional
Field Type
Description
AllocDesc
alloc_no

number(10)

doc_type

varchar2(1)

physical_wh

number(10)

wh

number(10)

item

varchar2(25)

pick_not_before_date

RIBDate

pick_not_after_date

RIBDate

order_type

varchar2(9)

order_no

varchar2(10)

order_doc_type

varchar2(1)

event

varchar2(6)

event_description

varchar2(1000)

priority

number(4)

ticket_type_id

varchar2(4)

context_type

varchar2(6)

context_value

varchar2(25)

Begin Sub-Group 'A'

1:*
AllocDtl will repeat multiple times under AllocDesc
AllocDtl
physical_to_loc

number(10)

to_loc

varchar2(10)

loc_type

varchar2(1)

qty_allocated

number(12)

price

number(20)

selling_uom

varchar2(4)

priority

number(4)

store_ord_mult

varchar2(1)

Begin Sub-Group 'AA'

1:*
AllocDtlTckt will repeat multiple times under AllocDtl
AllocDtlTckt
comp_item

varchar2(25)

comp_price

number(20)

comp_selling_uom

varchar2(4)

End Sub-Group 'AA'



End Sub-Group 'A'




Message Format
The source message is in the form of XML file from ORMS 

Message Transport Details

Feature
Specification
Additional Information
Source System Name
ORMS

Source Platform / OS
IBM AIX

Source Physical Location


Source Underlying Data Storage Technology
RDBMS

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
                 (XCOM) 	
JMS adopter		

Data Format.
XML			
Delimited		
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
Package Name: Tesco_ TOM_Integration_Alloc_Dtl_for_IDS
BizTalk Procedure
Name
Tesco_ TOM_Integration_Alloc_Dtl_IDS
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
JMS Adapter picks up the message containing the Allocation Details coming from ORMS and converts the message into standard XML message and delivers the file to Biztalk. Once received BizTalk transforms the file and after transformation, uploads the IDS tables through SQL Adaptor.
Data Validation
Data Validation will be done by the target system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema

Target Table Structure: The target table structure is given below.

Table Name: PurchaseOrder

Sl No
Field Name
Constraints
Type
Description 
1
PONumber
PK
INTEGER
Original Purchase Order number
2
SupplierID
FK
INTEGER
Supplier Id
3
SupplierType
FK
CHAR(1)
Type of Supplier
4
LastUpdateDateTime

DATETIME
Last Update Time

Table Name: PurchaseOrderLine

Sl No
Field Name
Constraints
Type
Description 
1
PONumber
PK
INTEGER
Original Purchase Order number
2
POLineNo
PK
BIGINT
PO Order Line Number
3
PackID
FK
VARCHAR(25)
Item Number
4
OriginalPOQty
 
BIGINT
Original PO Quantity
5
NewPOQty
 
BIGINT
New PO Quantity
6
LastUpdateDateTime
 
DATETIME
Last Update Time

Table Name: Allocation

Sl No
Field Name
Constraints
Type
Description 
1
AllocationNo
PK
VARCHAR(10)
Allocation Number
2
WarehouseID
FK
INTEGER
Warehouse Id
3
PackID
FK
VARCHAR(25)
Item Numaber
4
ASNNumber
FK
VARCHAR(30)
Advanced Shipment Notification Number
5
PONumber
FK
INTEGER
Original Purchase Order Number
6
POLineNO
FK
INTEGER
Purchase Order Line Number
7
LastUpdateDateTime
 
DATETIME
Last Update Time

Table name: AllocationLine

Sl No
Field Name
Constraints
Type
Description 
1
AllocationNo
PK
VARCHAR(10)
Allocation Number
2
StoreID
PK
INTEGER
Store ID
3
AllocationQty

BIGINT
Allocated Quantity
4
LastUpdateDateTime

DATETIME
Last Update Time

Message Format
The source message is an XML file which is converted from RIB message of ORMS and is the integration layer uploads the data directly into the IDS tables. 

There is no message format associated with the output.
4.7 Message Transport Details 
For messages destined for RMS system, the following applies.	

Feature
Specification
Additional Information
Source System Name
Biztalk 2006

Source Platform / OS
Biztalk 2006 Server

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
IDS

Target Platform / OS


Target Physical Location


Target Underlying Data Storage Technology
RDBMS

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
SQL Adapter 			

Data Format

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
Instruction Name: Tesco_TOM_Integration_Alloc_Dtl_File_Delivery
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
1
The input file from RMS is assumed to be less than 10MB in size. Technology expert says that Messaging more than 10 MB through BizTalk is not advisable.



Outstanding Issues
ID
Issue
To be addressed by
1
File naming format to be confirmed
Adrian Hinks
2
Server Physical Location of the server and file 
Adrian Hinks
3
Error handling
Adrian Hinks 
4




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
ORMS
Oracle Retail Merchandising System
ORMA is getting installed for TESCO Merchandising operations in US. This system will governs the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
IDS
Integrated Data Store
IDS is the data store for information like Product, Supplier, Location etc. The IDS keeps information regarding Allocation and PO to facilitate the functioning of other system modules.
JMS Adapter
JMS Adapter
JMS Adapter is used to pick up RIB message and convert the message into the standard XML format. JMS Adapters are used by BizTalk to pick up such messages.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
27/12/2006
0.1
















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

Adrian Hinks
Engagement Architect

David Onyett
Project Lead

Rob McDonaghSolution Architect























	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Interface Specification Document



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT iv of  NUMPAGES 22	Date:  SAVEDATE \@ "d MMM yyyy" 15 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Interface Specification Document





























































