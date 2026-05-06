		







TOM Integration

Interface Specification for 
Inventory Adjustment

From STORELINE To ORMS


[D019 to D020]






Project BEN Code:
W60416
Author:Debasis PattanaikDate:
01/02/2007
Version:
1.0
Status:
Signed-Off
Modified By:

Reviewed By:
Erwin Oguz

Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
26/01/2007
0.1D
Draft
Chakraborty, Supriyo
29/01/2007
0.2D
Draft
Ganesan, Sankar
30/01/2007
0.3D
Draft





Reviewers

Name
Date
Version
Position
Chakraborty, Supriyo
29/01/2007
0.1D
Draft
Ganesan, Sankar
30/01/2007
0.2D
Draft
Erwin Oguz
01/02/2007
1.0
Signed-Off






At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Oguz, Erwin
Position
Solution Architect
Signature

Date
01/01/2007

Distribution List

Name
Date of Issue
Version
Oguz Erwin
02/02/2007
1.0
David Onyett
02/02/2007
1.0
Venkateswara Rao
02/02/2007
1.0







Document Source

Related Documents: XML files
Directory: <to put>
File Name: 
tes.jp.retail.storeline.invadjust.v2.7
tes.jp.retail.retek.invadjust.v2.7
mapto.tes.jp.retail.retek.invadjust.v2.7.4 


Information Architecture Context diagram
Will be provided

Mapping spreadsheet
Will be Provided
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc157930289 \h 7
1.1	Purpose of Document	 PAGEREF _Toc157930290 \h 7
1.2	Background	 PAGEREF _Toc157930291 \h 7
1.3	Scope	 PAGEREF _Toc157930292 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc157930293 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc157930294 \h 8
2.2	Architecture	 PAGEREF _Toc157930295 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc157930296 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc157930297 \h 10
3.1	Scope	 PAGEREF _Toc157930298 \h 10
3.2	Source Message Schema	 PAGEREF _Toc157930299 \h 10
3.3	Message Format	 PAGEREF _Toc157930300 \h 11
3.4	Message Transport Details	 PAGEREF _Toc157930301 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc157930302 \h 12
3.6	Environment and Security Context	 PAGEREF _Toc157930303 \h 12
3.7	Non-Functional Requirements	 PAGEREF _Toc157930304 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc157930305 \h 14
4.1	Scope	 PAGEREF _Toc157930306 \h 14
4.2	Data Validation	 PAGEREF _Toc157930307 \h 14
4.3	Filtering	 PAGEREF _Toc157930308 \h 14
4.4	Mapping	 PAGEREF _Toc157930309 \h 14
4.5	Target Message Schema	 PAGEREF _Toc157930310 \h 14
4.6	Message Format	 PAGEREF _Toc157930311 \h 14
4.7 Message Transport Details	 PAGEREF _Toc157930312 \h 15
4.7	Naming and Configuration	 PAGEREF _Toc157930313 \h 16
4.8	Environment and Security Context	 PAGEREF _Toc157930314 \h 16
4.9	Non-Functional Requirements	 PAGEREF _Toc157930315 \h 16
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc157930316 \h 17
5.1	Scope	 PAGEREF _Toc157930317 \h 17
5.2	Data Validation	 PAGEREF _Toc157930318 \h 17
5.3	Filtering	 PAGEREF _Toc157930319 \h 17
5.4	Mapping	 PAGEREF _Toc157930320 \h 17
5.5	Target Message Schema	 PAGEREF _Toc157930321 \h 17
5.6	Message Transport Details	 PAGEREF _Toc157930322 \h 17
5.7	Naming and Configuration	 PAGEREF _Toc157930323 \h 17
5.8	Environment and Security Context	 PAGEREF _Toc157930324 \h 17
5.9	Non-Functional Requirements	 PAGEREF _Toc157930325 \h 17
6	Testing Deliverables	 PAGEREF _Toc157930326 \h 18
7	Deployment	 PAGEREF _Toc157930327 \h 19
8	Assumptions and Outstanding Issues	 PAGEREF _Toc157930328 \h 20
8.1	Assumptions	 PAGEREF _Toc157930329 \h 20
8.2	Outstanding Issues	 PAGEREF _Toc157930330 \h 20
Appendix A Volumes	 PAGEREF _Toc157930331 \h 21
•	Glossary	 PAGEREF _Toc157930332 \h 22
Appendix B Document Control	 PAGEREF _Toc157930333 \h 23

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t. STORELINE inventory adjustment data (Stock Check adjustments & Wastage adjustments) to ORMS.

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including STORELINE and ORMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Inventory Adjustment data from STORELINE into ORMS.

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
The interface is to upload the Inventory Adjustment data (Stock Check adjustments & Wastage adjustments) from STORELINE into ORMS. The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Stock take result data in (| delimited flat file) from STORELINE interface (D019). The STORELINE interface will put this file (*.dat) in the shared location through RTI SOAP adapter. The BizTalk server then transfers this flat file data to a XML file which then transfer to ORMS through RIB in form of RIB messages. The transformation from BizTalk XML file to RIB message will be done through JMS adopter with the usage of RIB assembler. In turn RIB messages then publish those messages for subscription to update ORMS database in real-time basis. The transformations of XML file to RIB message determine the success/failure. In case of failure it will write into an error log file and does not require any archive process.


The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture
 EMBED Visio.Drawing.11  


Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data in the form of flat file from the shared location at STORELINE side and delivering the resulting to another shared location at ORMS side before the identified cut-off time. The interface should run on real time basis. 
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
STORELINE creates a pipe | delimited flat file on real time basis whenever it receives an inventory adjustment (D019) data. BizTalk in turn picks up the file from the same location and produces a positional flat file at another predefined shared location, used by ORMS to pick up the file. 
Source Message Schema
Field Name
Optional
Type
Description
HEADER RECORDS
CapturedBy – CreatedBy

String

DateOfExtract
Yes
String
Store-line extraction date
DelAfterDate

String
Delivery before date
DelBeforeDate

String
Delivery after date
Description

String
Free form description
DriversName-Courier

String
Courier Driver Name
ExpectedDelDate

String
Expected Delivery Date
InvoiceNumber

String
Invoice Number
InvoiceTaxTotal

String
Invoice Tax Total
InvoiceTotal

String
Invoice Total
NoOfDetailLines
Yes
Unsigned Int
No. of Detail Items
OrderDate

String
Count Order Date
OrderNumber-TransactionNo
Yes
Unsigned Int
Count Order Number
OrderType-CountType

Unsigned Int
Count Order Type
OriginalOrderNumber

Unsigned Int
Original Order Number
ReasonCode

number
Reason Code
RecordType
Yes
String
Record Type
RefNo1

String
Reference No 1
RefNo2

String
Reference No 2
Remarks

String
Remarks
ReprocessedFlag

number
Re-Processed Flag
StoreAddress

String
Location Address
StoreName

String
Location Name
StoreNo
Yes
Unsigned Int
Location of extracted data
SupplierAddress

String
Supplier Address
SupplierCode-ToStore

String
Supplier Code
SupplierName

String
Supplier Name
SupplierType

Unsigned Int
Supplier Type
TimeOfExtract
Yes
String
Extraction time of data
TotalQty

String
Total Quantity
TotalValue

String
Total Value
TransactionDateTime

String
Transaction Date and Time
UserName

String
Operator name
DETAIL RECORDS
DateOfExtract
Yes
String
Storeline extract date
InvoiceCost-Excl-PerUOM

String
Invoice cost excluding (Per UOM)
InvoiceQty

String
Invoice Quantity
ItemDescription

String
Item Description
ItemNumber

Unsigned Int
Item CodeItem Code
Used to populate ITEM field 
LineNumber

Unsigned Int
Transaction line number
Location

String
Location in store 
OrderNumber-TransactionNumber

Unsigned Int
Concatenated with store no to get Batch Number.
OrderQuantity-SentQuantity

Unsigned Int

OrderType

Unsigned Int

PackSize-Ratio

Unsigned Int

ReasonCode

Number
Reason Code field direct mapping
RecordType

String
Type of record as per Storeline 
Used to get Adjusted Qty
ReferenceNo

Unsigned Int

SellingPricePerUOM

String

Sign

String
Sign indicator 
 - negative 
+ positive
Used to get Adjusted Qty
StoreNo
Yes
Unsigned Int
Concatenated with Order Number-Transaction Number to get Batch Number.
SupplierItemNo-CatalogueNo

String

TaxPercentageOnCost

String

TimeOfExtract
Yes
String

TransactionQty

String
Transaction Quantity concatenated with sign indicator will give meaningful value.
Used to get Adjusted Qty
TrsCostPrice-Excl-PerUOM

String

UOMCode

Unsigned Int

UOMDescription

String


Message Format
The source message is in the form of pipe | delimited file from STORELINE is getting converted into the target file format in a package. 

Message Transport Details

Feature
Specification
Additional Information
Source System Name
STORELINE

Source Platform / OS
IBM AIX

Source Physical Location


Source Underlying Data Storage Technology
SQL Server

Target System Name
Biztalk 2006

Target Platform / OS
Biztalk 2006 Server/Windows 2003

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	

Data Format.
XML			
Delimited		
Positional		

| delimited
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
Package Name: Tesco_ TOM_Integration_INVENTORY_ADJ_from_STORELINE_to_ORMS
BizTalk Procedure
Name
Tesco_TOM_Integration_INV_ADJ_ORMS
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
BizTalk monitors the file in the configured location for every new file and submits the same to the remote UNIX share via FTP. The resultant file is a XML file.
Data Validation
Data Validation will be done by the target ORMS system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Target Message Schema in XSD format:

 EMBED Package  

The Description of the fields as mentioned in the XSD file:

Record 
NameField Name
Field Type
Start PosEnd PosDescriptionFHEAD

CreateDate
String
36
43
Storeline extraction data date - DateofExtract
CreateTime
String
44
49
Storeline extraction data time – TimeofExtract
FileLineNumber
ui8
6
15
Constant value - ‘1’ (one-numeric).
FileTypeDefinition
String
16
35
Constant value - TSCINVADJUPLD_v1.6
Location
ui8
51
60
Source schema field - Store No 
LocationType
String
50
50
Constant value – ‘S’
FDETL

AdjQty
ui8
55
67
Calculated field (RecordType, TransactionQty & Sign.)
BatchNumber
String
16
29
Concatenated field ("00000000",OrderNumber-TransactionNumber & Store No.)
DateTime
String
72
85
Concatenated field - DateofExtract & TimeofExtract.
FileLineNumber
ui8
6
15
Positional record number
Item
String
30
54
Source schema field - ItemNumber
ReasonCode
String
68
71
Compared both (SetHdr & SetDtl) ReasonCode and pass the non-empty field.
FTAIL
FileRecordNumber
ui8
6
15
Total record including FHEAD & FTAIL.
NumberofFileDetailLines
ui8
16
25
Total no of detail record

Message Format
The source message is a pipe | delimited flat file from STORELINE and is getting converted into the target file format for ORMS in a package. The target message is a XML file. 
4.7 Message Transport Details 
For messages destined for ORMS system, the following applies.	

Feature
Specification
Additional Information
Source System Name
Biztalk 2006

Source Platform / OS
Biztalk 2006 Server/Windows 2003

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
ORMS

Target Platform / OS
IBM AIX

Target Physical Location


Target Underlying Data Storage Technology
RDBMS

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
JMS Adopter          		
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter                              

Data Format

XML  				
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
Erwin Oguz
2
Server Physical Location of the server and file 
Erwin Oguz
3
Error handling
Erwin Oguz
4
URL in XSD needs to be defined
Erwin Oguz
5
Failure Folder Location to be defined
Erwin Oguz


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
Oracle Retek Merchandising System
Retek Merchandising System is getting installed for TESCO Merchandising operations in US. This system will governs the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
RIB
Retek Integration Bus
This is an integration Interface between the Oracle Retek modules.
Storeline
STORE used for inventory purposes.
The store line operates on Tesco deals with the inventory control. 
XSD
XML Schema Definition
It describe the elements in an Extensible Markup Language (XML) document
XML
Extensible Markup Language
An open standard for describing data. It is used for defining a common method for identifying data. It supports business-to-business transactions and also uses electronic data interchange and Web services. 
FTP
File Transfer Protocol
The Internet File Transfer Protocol (FTP) is defined facilities for transferring files to and from remote computer systems.
FHEAD
File Header Record
This is File header record identifier. This string will get inserted at the beginning of the file. 
FTAIL

File Tail Record
This is File tail record identifier.   
FDETL

File Detail Record
This is File Detail record identifier.   

Document Control
Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
26-Jan-2007
0.1D
Draft
Chakraborty, Supriyo
29/01/2007
0.2D
Draft
Ganesan, Sankar
30/01/2007
0.3D
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
Erwin Oguz
Enterprise Architect
Approver






























	









Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 23 of  NUMPAGES 23	Date:  SAVEDATE \@ "d MMM yyyy" 5 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture




