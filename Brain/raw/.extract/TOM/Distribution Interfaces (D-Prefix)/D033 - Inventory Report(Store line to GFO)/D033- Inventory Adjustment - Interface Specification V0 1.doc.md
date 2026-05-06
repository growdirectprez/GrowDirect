		







TOM Integration

Interface Specification

STORELINE 

To 

GFO


[D019 to D033]





Project BEN Code:
W60416
Author:Debasis PattanaikDate:
05/02/2007
Version:
0.1
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:
Ganesan, Sankar

Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
05/02/2007
0.1D
Draft
Ganesan, Sankar








Reviewers

Name
Date
Version
Position
Ganesan, Sankar


Draft










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

Related Documents: XML Store Line source file schema, GFO system TSD document & Store line system FSD document 

Directory: <to give path>

File Name: 
XML Store Line source file schema - tes.jp.retail.storeline.invadjust.v2.7
 EMBED Package  
GFO system TSD document - TSD008 - Stock Record - non-sales events.doc
 EMBED Word.Document.8 \s 
Store line system FSD document - FS1847_BO_Stock_Interfaces.doc
 EMBED Word.Document.8 \s 


Information Architecture Context diagram
Will be provided

Mapping spreadsheet
Will be Provided
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc158541422 \h 7
1.1	Purpose of Document	 PAGEREF _Toc158541423 \h 7
1.2	Background	 PAGEREF _Toc158541424 \h 7
1.3	Scope	 PAGEREF _Toc158541425 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc158541426 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc158541427 \h 8
2.2	Architecture	 PAGEREF _Toc158541428 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc158541429 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc158541430 \h 10
3.1	Scope	 PAGEREF _Toc158541431 \h 10
3.2	Source Message Schema	 PAGEREF _Toc158541432 \h 10
3.3	Message Format	 PAGEREF _Toc158541433 \h 11
3.4	Message Transport Details	 PAGEREF _Toc158541434 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc158541435 \h 12
3.6	Environment and Security Context	 PAGEREF _Toc158541436 \h 12
3.7	Non-Functional Requirements	 PAGEREF _Toc158541437 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc158541438 \h 14
4.1	Scope	 PAGEREF _Toc158541439 \h 14
4.2	Data Validation	 PAGEREF _Toc158541440 \h 14
4.3	Filtering	 PAGEREF _Toc158541441 \h 14
4.4	Mapping	 PAGEREF _Toc158541442 \h 14
4.5	Stored Procedures	 PAGEREF _Toc158541443 \h 14
4.6	JIP00 – Package Set switch – new subroutine	 PAGEREF _Toc158541444 \h 14
4.7	JIP11 – process wastage – new subroutine	 PAGEREF _Toc158541445 \h 14
4.8	JIP12 – process stock counts – new subroutine	 PAGEREF _Toc158541446 \h 15
4.9	JIP13 – process stock takes – new subroutine	 PAGEREF _Toc158541447 \h 15
JIP14 – process miscellaneous stock movements – new subroutine	 PAGEREF _Toc158541448 \h 15
4.10	Message Format	 PAGEREF _Toc158541449 \h 16
4.7 Message Transport Details	 PAGEREF _Toc158541450 \h 16
4.11	Naming and Configuration	 PAGEREF _Toc158541451 \h 17
4.12	Environment and Security Context	 PAGEREF _Toc158541452 \h 17
4.13	Non-Functional Requirements	 PAGEREF _Toc158541453 \h 17
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc158541454 \h 18
5.1	Scope	 PAGEREF _Toc158541455 \h 18
5.2	Data Validation	 PAGEREF _Toc158541456 \h 18
5.3	Filtering	 PAGEREF _Toc158541457 \h 18
5.4	Mapping	 PAGEREF _Toc158541458 \h 18
5.5	Target Message Schema	 PAGEREF _Toc158541459 \h 18
5.6	Message Transport Details	 PAGEREF _Toc158541460 \h 18
5.7	Naming and Configuration	 PAGEREF _Toc158541461 \h 18
5.8	Environment and Security Context	 PAGEREF _Toc158541462 \h 18
5.9	Non-Functional Requirements	 PAGEREF _Toc158541463 \h 18
6	Testing Deliverables	 PAGEREF _Toc158541464 \h 19
7	Deployment	 PAGEREF _Toc158541465 \h 20
8	Assumptions and Outstanding Issues	 PAGEREF _Toc158541466 \h 21
8.1	Assumptions	 PAGEREF _Toc158541467 \h 21
8.2	Outstanding Issues	 PAGEREF _Toc158541468 \h 21
Appendix A Volumes	 PAGEREF _Toc158541469 \h 22
•	Glossary	 PAGEREF _Toc158541470 \h 23
Appendix B Document Control	 PAGEREF _Toc158541471 \h 24

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t. STORELINE inventory adjustment data e.g. Wastage (out-of-code and damaged), Stock counts, Stock takes & other movements into GFO.

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. Therefore the GFO system Technical System Document (TSD) and store line system Functional System Document are provided for better understanding of this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including STORE LINE and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Inventory Adjustment data from STORE LINE into GFO.

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
The interface is to upload the Inventory Adjustment data (Wastage, Stock counts, Stock takes & other movements) from STORE LINE into GFO. The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Inventory Adjustment data (| delimited flat file) from STORE LINE interface. The store line interface will put this file (*.dat) in the shared location through RTI SOAP adapter. The BizTalk server then transfers this flat file data by invoking GFO stored procedures through DB2 adopter. BizTalk will first invokes JIP00 – package set switch- stored procedure to get the stream information which is passed along with other input attributes (wastage/count date & time, Reason Code, Store No, Adjusted Quantity etc) to get updated/inserted in GFO underlying table. The output attributes returned by stored procedure will determine the success/failure of this updating.

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
The interface should be capable of extracting data in the form of flat file from the shared location at TIMS side and delivering the resulting to another shared location at ORMS side before the identified cut-off time. The interface should run on real time basis. 
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
STORELINE creates a pipe | delimited flat file on real time basis whenever it receives an inventory adjustment (D019) data. BizTalk in turn picks up the file from the shared location and invokes series of subroutines through DB2 Adopter to update/insert the underline table of GFO. 
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
TrsCostPrice-Excl-PerUOM

String

UOMCode

Unsigned Int

UOMDescription

String


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
Biztalk 2006 Server

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
Tesco_TOM_Integration_INV_ADJ_GFO
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
The BizTalk server transfers the source message schema file to GFO by invoking a series of stored procedures within DB2.This will first invokes JIP00 – package set switch- stored procedure to get the stream information which is passed along with other input attributes (wastage/count date & time, Reason Code, Store No, Adjusted Quantity etc) to get updated/inserted in GFO underlying table. 
Data Validation
Data Validation will be done by the target ORMS system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Stored Procedures
The stock event data from Store Line then immediately use it to invoke the relevant stored procedure(s) within DB2. The types of stock event involved are:

Wastage (out-of-code and damaged)
Stock counts
Stock takes
Other movements to / from other locations e.g. supplier, DC

The following description gives the details of stored procedure need to be invoked to pass data from STORE LINE to GFO.
JIP00 – Package Set switch – new subroutine
JIP00 will determine a store’s database stream then point subsequent processing to that package set.
JIP11 – process wastage – new subroutine
JIP11 will take wastage data and use it to update the following tables:

	TXJJ0PDM	stock movements
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ004D)

Retalix (StoreLine) record type 327, reason code 515 (discontinued) = out-of-code
Retalix (StoreLine) record type 327, reason code 516 (end of season) = out-of-code
Retalix (StoreLine) record type 327, reason code 517 = damaged
Retalix (StoreLine) record type 327, reason code 518 = out-of-code
Retalix (StoreLine) record type 327, reason code 519 (insufficient code) = out-of-code

The full specification is a separate document in the PROGRAM SPECS sub-folder.

JIP12 – process stock counts – new subroutine
JIP12 will take stock count adjustment data and use it to update the following tables:

	TXJJ0ASC	applied stock count
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ004D)

Retalix (StoreLine) record type 315 = stock count (difference)
 
The full specification is a separate document in the PROGRAM  SPECS sub-folder.
JIP13 – process stock takes – new subroutine
JIP13 will take stock take data and use it to update the following tables:

	TXJJ0ASC	applied stock count
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ003D)

Retalix (StoreLine) record type 314 = stock count (absolute)
 
The full specification is a separate document in the PROGRAM  SPECS sub-folder.
JIP14 – process miscellaneous stock movements – new subroutine
JIP14 will take miscellaneous stock record adjustment data and use it to update the following tables:

	TXJJ0PDM	stock movements
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ004D)

Retalix (StoreLine) record type 322 = store-to-store transfer in
Retalix (StoreLine) record type 323 = stock adjustment (+ve or -ve)
Retalix (StoreLine) record type 325 = return to supplier 
Retalix (StoreLine) record type 326 = return to DC
Retalix (StoreLine) record type 350 = store-to-store transfer out 

The full specification is a separate document in the PROGRAM SPECS sub-folder.

Message Format
4.7 Message Transport Details 
For messages destined for ORMS system, the following applies.	

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
GFO

Target Platform / OS
COBOL/UNIX

Target Physical Location


Target Underlying Data Storage Technology
RDBMS

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter                              
DB2 File Adapter                             

Data Format

XML  				
Delimited 			
Positional 			
COBOL format                                 

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
Rollback transaction supported by GFO in case of failure.



Outstanding Issues
ID
Issue
To be addressed by
1
Stored procedure JIP00 – package set switch (used to get STREAM information)  foot-prints need to be defined
Erwin Oguz
2
DB2 adopter specification to call sub procedures need to be defined
Erwin Oguz
3
Error handling with respect to DB2 copybook need to be defined
Erwin Oguz
4
Return output parameter of stored procedure need to be defined with details of its reason code & maintaining error log.
Erwin Oguz
5
Store Line source file Physical Location need to be defined
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
GFO
Group Forecasting and Ordering
The GFO operates on Tesco deals with the forecasting & Ordering.
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

Document Control
Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
05/02/2007
0.1D
Draft
Ganesan, Sankar










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































	


Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT ii of  NUMPAGES 24	Date:  SAVEDATE \@ "d MMM yyyy" 6 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture




