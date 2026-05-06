		







TOM Integration

Interface Specification 
For
Stock Take Result

STORELINE 
To 
ORMS



[D029 to D021]





Project BEN Code:
W60416
Author:
Debasis Pattanaik	
Date:
19/02/2007
Version:
0.1
Status:
Draft
Modified By:

Reviewed By:


Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
19/02/2007
0.1D
Draft

Reviewers

Name
Date
Version
Position
Ganesan, Sankar













At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Erwin Oguz
Position
Solution Architect
Signature

Date


Distribution List

Name
Date of Issue
Version
Oguz Erwin


David Onyett


Venkateswara Rao









Document Source

Related Documents: XML STORELINE source file schema, ORMS system TSD document & STORELINE system FSD document 

Directory: Embedded in this document.

File Name: 
XML STORELINE source file schema - tes.jp.retail.storeline.stocktakeRequest.v2.2.xml		

 EMBED Package  		

ORMS system TSD document - TSD008 - Stock Record - non-sales events.doc

 EMBED Word.Document.8 \s 

STORELINE system FSD document - FS1847_BO_Stock_Interfaces.doc

 EMBED Word.Document.8 \s 


Information Architecture Context diagram
D029  D021- StockTake Result_Information_Context_Diagram.vsd


Mapping spreadsheet
D029  D021-StockTake Result - mapping document1.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc159837373 \h 7
1.1	Purpose of Document	 PAGEREF _Toc159837374 \h 7
1.2	Background	 PAGEREF _Toc159837375 \h 7
1.3	Scope	 PAGEREF _Toc159837376 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc159837377 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc159837378 \h 8
2.2	Architecture	 PAGEREF _Toc159837379 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc159837380 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc159837381 \h 10
3.1	Scope	 PAGEREF _Toc159837382 \h 10
3.2	Source Message Schema	 PAGEREF _Toc159837383 \h 10
3.3	Message Format	 PAGEREF _Toc159837384 \h 11
3.4	Message Transport Details	 PAGEREF _Toc159837385 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc159837386 \h 12
3.6	Environment and Security Context	 PAGEREF _Toc159837387 \h 13
3.7	Non-Functional Requirements	 PAGEREF _Toc159837388 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc159837389 \h 14
4.1	Scope	 PAGEREF _Toc159837390 \h 14
4.2	Data Validation	 PAGEREF _Toc159837391 \h 14
4.3	Filtering	 PAGEREF _Toc159837392 \h 14
4.4	Mapping	 PAGEREF _Toc159837393 \h 14
4.5	Target Message Schema	 PAGEREF _Toc159837394 \h 14
4.6	Message Format	 PAGEREF _Toc159837395 \h 15
4.7 Message Transport Details	 PAGEREF _Toc159837396 \h 16
4.7	Naming and Configuration	 PAGEREF _Toc159837397 \h 17
4.8	Environment and Security Context	 PAGEREF _Toc159837398 \h 17
4.9	Non-Functional Requirements	 PAGEREF _Toc159837399 \h 17
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc159837400 \h 18
5.1	Scope	 PAGEREF _Toc159837401 \h 18
5.2	Data Validation	 PAGEREF _Toc159837402 \h 18
5.3	Filtering	 PAGEREF _Toc159837403 \h 18
5.4	Mapping	 PAGEREF _Toc159837404 \h 18
5.5	Target Message Schema	 PAGEREF _Toc159837405 \h 18
5.6	Message Transport Details	 PAGEREF _Toc159837406 \h 18
5.7	Naming and Configuration	 PAGEREF _Toc159837407 \h 18
5.8	Environment and Security Context	 PAGEREF _Toc159837408 \h 18
5.9	Non-Functional Requirements	 PAGEREF _Toc159837409 \h 18
6	Testing Deliverables	 PAGEREF _Toc159837410 \h 19
7	Deployment	 PAGEREF _Toc159837411 \h 20
8	Assumptions and Outstanding Issues	 PAGEREF _Toc159837412 \h 21
8.1	Assumptions	 PAGEREF _Toc159837413 \h 21
8.2	Outstanding Issues	 PAGEREF _Toc159837414 \h 21
Appendix A Volumes	 PAGEREF _Toc159837415 \h 22
•	Glossary	 PAGEREF _Toc159837416 \h 23
Appendix B Document Control	 PAGEREF _Toc159837417 \h 24

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements with respect to STORELINE interface (D029) Stock take result data updating into the ORMS system interface (D021).

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. Therefore the ORMS system Technical System Document (TSD) and STORELINE system Functional System Document are provided for better understanding of this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including STORELINE and ORMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Stock take result data from STORELINE into ORMS.

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
The interface is to upload the Stock take result data from STORELINE interface D029 into ORMS interface D021. The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Stock take result data in (| delimited flat file) from STORELINE interface (D029). The STORELINE interface will put this file (*.dat) in the shared location through RTI SOAP adapter. The BizTalk server then transfers this flat file data to a XML file which then transfer to ORMS through RIB in form of RIB messages. The transformation from BizTalk XML file to RIB message will be done through JMS adopter. The RIB messages then publish those messages for subscription to update ORMS database in real-time basis. The transformations of XML file to RIB message determine the success/failure. In case of failure it will write into an error log file and does not require any achieve operation.

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
The interface should be capable of extracting data in the form of flat file from the shared location at STORELINE side and delivering the resulting into ORMS side database tables before the identified cut-off time. The interface should run on real time basis. 
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
STORELINE creates a pipe | delimited flat file whenever stock take has been taken and put the file in a dedicated shared location. The flat file extension is *.dat and BizTalk in turn picks up the file from the shared location and converts it to a XML file which in turn converted to RIB message through JMS adopter for update/insert of the underline table of ORMS. 
Source Message Schema
Field Name
Optional
Type
Description
HEADER RECORDS
CapturedBy-CreatedBy
Yes
string
Extract file created user name
DateOfExtract
Yes
date
Store-line extraction date
DelAfterDate
Yes
string
Delivery before date
DelBeforeDate
Yes
string
Delivery after date
Description
Yes
string
Free form description
DriversName-Courier
Yes
string
Courier Driver Name
InvoiceNumber
Yes
string
Invoice Number
InvoiceTaxTotal
Yes
ui8
Invoice Tax Total
InvoiceTotal
Yes
ui8
Invoice Total
NoOfDetailLines
Yes
ui8
No. of Detail Items
OrderDate
Yes
string
Count Order Date
OrderNumber-TransactionNo
Yes
ui8
Count Order Number
OrderType-CountType
Yes
ui8
Count Order Type
OriginalOrderNumber
Yes
ui8
Original Order Number
ReasonCode
Yes
string
Reason Code
RecordType
Yes
string
Record Type
RefNo1
Yes
string
Reference No 1
RefNo2
Yes
string
Reference No 2
Remarks
Yes
string
Remarks
ReProcessedFlag
Yes
string
Re-Processed Flag
SelectionCriteria
Yes
string
Criteria of selecting extract data
SelectionRange
Yes
string
Range of selecting extract data
StocktakeDueDate
Yes
string
Date when stock take taken
StoreAddress
Yes
string
Location Address
StoreName
Yes
string
Location Name
StoreNo
Yes
ui8
Location of extracted data
SupplierAddress
Yes
string
Supplier Address
SupplierCode-ToStore
Yes
string
Supplier Code
SupplierName

string
Supplier Name
SupplierType

ui8
Supplier Type
TimeOfExtract

time
Extraction time of data
TotalQty

ui8
Total Quantity
TotalValue

ui8
Total Value
TransactionDateTime

string
Transaction Date and Time
UserName

string
Operator Name
DETAIL RECORDS – Grouping start(detail can have multiple record)
CountQty
Yes
ui8
Stock count Quantity
DateOfExtract

string
Extract date of data
InvoiceCost-Excl-PerUOM
Yes
ui8
Invoice cost per UOM
InvoiceQty
Yes
ui8
Invoice Quantity
ItemDescription
Yes
string
Description of Item
ItemNumber

ui8
Item Number
LineNumber

ui8
Record Line Number(Record starts from 1)
Location
Yes
string
Location of extract item
OrderNumber-TransactionNumber
Yes
ui8

OrderQuantity-SentQuantity
Yes
ui8

OrderType
Yes
ui8
Order Type
PackSize-Ratio
Yes
ui8
Item Pack size
ReasonCode
Yes
string
Reason code of Item
RecordType

string
Record Type
ReferenceNo
Yes
ui8
Reference No
SellingPricePerUOM
Yes
ui8
Selling price per UOM
Sign
Yes
string
Sign indicator 
 - negative 
+ positive
StoreNo

ui8
Store Id
SupplierItemNo-CatalogueNo
Yes
string
Supplier Item No 
TaxPercentageOnCost
Yes
ui8
Tax percentage on Invoice Cost
TimeOfExtract

string
Time of Extract
TrsCostPrice-Excl-PerUOM
Yes
ui8
Transaction cost value excluding per  UOM
UOMCode
Yes
ui8
Unit of measure details
UOMDescription
Yes
string
Unit of measure description

Message Format
The source message is in the form of pipe | delimited flat file from STORELINE. 

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
Biztalk 2006 Server/Window Server 2003

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
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
Package Name: TOM.D029 to D021_Integration_STOCK _TAKE_STORELINE_to_ORMS
BizTalk Procedure
Name
TOM.D029 to D021_Integration_STOCK_Take_ STORELINE_to_ORMS
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



The naming standard to be followed as mentioned in this document – 

 EMBED Word.Document.8 \s 

Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
The interface is meant to run at a pre-configured time interval, which on completion is expected to produce a XML file (containing reference data records) onto the shared location. The XML file will pass through RIB assembler and transferred to ORMS location through JMS adaptor. This shared location would be monitored by ORMS systems Interface at the same interval. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into ORMS using RIB.

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
Start PosEnd PosDescriptionURL
URLToken
Char
1
300
The target File name  “FILE=tsc_disprtvupld_{Store No}_yyyymmddhhmmss_{system date to millisecond fraction}”

FileHdr

CreateDate
Date
20
27
setHdrDateofExtract
CreateTime
Time
28
33
setHdrTimeofExtract
CycleCountId
Char
48
55
setHdrRefNo1
FileLineNumber
Number
6
15
Sequential line number in the file 
FileTypeDefination
Char
16
19
Constant Value- “STKU”
Location
Number
57
66
setHdrStoreNo
LocationType
Char
56
56
Constant Value- “S”
StockTakeDate
Char
34
47
setHdrStockTakeDueDate

FileDtl

FileLineNumber
Number
6
15
Record No +1 
InventoryLocationDescription
Char
56
85
setDtlStoreNo
InventoryQuantity
Number
44
55
setDtlCountQty
Item
Char
19
43
setDtlItemNumber
ItemType
Char
16
18
Constal Value- “ITM”

FileTrlr
FileLineNumber
Number
6
15
Detail record count incremented to step 1.
NumberOfFileDetailLines
Number
16
25
Detail record count decremented to step 2.

Message Format
The source message is a pipe | delimited flat file from STORELINE and is getting converted into the target file format for ORMS in a package. The target message is a XML file. 
4.7 Message Transport Details 
For messages destined for RIB system, the following applies.	

Feature
Specification
Additional Information
Source System Name
BizTalk 2006

Source Platform / OS
BizTalk 2006 Server – Windows server 2003

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
1
Rollback transaction supported by ORMS in case of failure.

Outstanding Issues
ID
Issue
To be addressed by
2
Error handling
Erwin Oguz
3
Error log file location need to de defined
Erwin Oguz
4
STORELINE source file Physical Location need to be defined
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
Group Forecasting and Ordering
The ORMS operates on Tesco deals with the forecasting & Ordering.
STORELINE
STORE used for inventory purposes.
The STORELINE operates on Tesco deals with the inventory control. 
XSD
XML Schema Definition
It describe the elements in an Extensible Markup Language (XML) document
XML
Extensible Markup Language
An open standard for describing data. It is used for defining a common method for identifying data. It supports business-to-business transactions and also uses electronic data interchange and Web services. 
FTP
File Transfer Protocol
The Internet File Transfer Protocol (FTP) is defined facilities for transferring files to and from remote computer systems.
RIB
Retek Integration Bus
This is an integration Interface between the Oracle Retek modules.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
19/02/2007
0.1D
Draft



Related Documents

Author	
Date
Version
Title
Isaac
18-Aug-2004
4.0
StoreLine FS1847 – BO Stock Interfaces
Neil Williams
26-Jan-2007
0.02
Technical System Design - TSD008 Stock Record - non-sale events










Distribution

Name
Position
Approver/Contributor/Other
Erwin Oguz
Enterprise Architect
Approver
David Onyett
Project Leader

Venkateswara Rao
Offshore Co-ordinator


























	










Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 8 of  NUMPAGES 24	Date:  SAVEDATE \@ "d MMM yyyy" 21 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture




