		







TOM Integration

Interface Specification 
For
Stock Take Result

STORELINE 
To 
GFO



[D029 to D022]





Project BEN Code:
W60416
Author:
Debasis Pattanaik	
Date:
02/04/2007
Version:
1.1
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
09/02/2007
0.1D
Draft
Ganesan, Sankar
12/02/2007
0.1D
Draft
Debasis Pattanaik
13/02/2007
0.2D
Updated as per Erwin review comments
Debasis Pattanaik
02/04/2007
1.1
Signed Off – Incorporated DB2 specific Stored Proc by removing previously used COBOL formatted stored proc. 

Reviewers

Name
Date
Version
Position
Ganesan, Sankar
12/02/2007
0.1D
Draft
Erwin Oguz
13/02/2007
1.0
Sign-Off version






At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Erwin Oguz
Position
Solution Architect
Signature

Date
13/02/2007

Distribution List

Name
Date of Issue
Version
Oguz Erwin
13/02/2007
1.0
David Onyett
13/02/2007
1.0
Venkateswara Rao
13/02/2007
1.0







Document Source

Related Documents: XML STORELINE source file schema, GFO system TSD document & STORELINE system FSD document 

Directory: Embedded in this document.

File Name: 
XML STORELINE source file schema - tes.jp.retail.storeline.stocktakeRequest.v2.2.xml		

 EMBED Package  		

GFO system TSD document - TSD008 - Stock Record - non-sales events.doc

 EMBED Word.Document.8 \s 

STORELINE system FSD document - FS1847_BO_Stock_Interfaces.doc

 EMBED Word.Document.8 \s 


Information Architecture Context diagram
D022- Stock Take Result_Information_Context_Diagram.vsd
 EMBED Visio.Drawing.11  	

Mapping spreadsheet
Not required for this interface
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc163365643 \h 7
1.1	Purpose of Document	 PAGEREF _Toc163365644 \h 7
1.2	Background	 PAGEREF _Toc163365645 \h 7
1.3	Scope	 PAGEREF _Toc163365646 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc163365647 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc163365648 \h 8
2.2	Architecture	 PAGEREF _Toc163365649 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc163365650 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc163365651 \h 10
3.1	Scope	 PAGEREF _Toc163365652 \h 10
3.2	Source Message Schema	 PAGEREF _Toc163365653 \h 10
3.3	Message Format	 PAGEREF _Toc163365654 \h 11
3.4	Message Transport Details	 PAGEREF _Toc163365655 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc163365656 \h 12
3.6	Environment and Security Context	 PAGEREF _Toc163365657 \h 13
3.7	Non-Functional Requirements	 PAGEREF _Toc163365658 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc163365659 \h 14
4.1	Scope	 PAGEREF _Toc163365660 \h 14
4.2	Data Validation	 PAGEREF _Toc163365661 \h 14
4.3	Filtering	 PAGEREF _Toc163365662 \h 14
4.4	Stored Procedures	 PAGEREF _Toc163365663 \h 14
4.5	JH0S00 – Package to return STREAM info	 PAGEREF _Toc163365664 \h 14
4.6	JI0P13– process stock takes – new subroutine	 PAGEREF _Toc163365665 \h 14
4.7	Mapping	 PAGEREF _Toc163365666 \h 15
4.8	Mapping of JH0S00 – Package to return STREAM info	 PAGEREF _Toc163365667 \h 15
4.9	Mapping of JI0P13– process stock takes	 PAGEREF _Toc163365668 \h 16
4.10	Message Format	 PAGEREF _Toc163365669 \h 17
4.11	Message Transport Details	 PAGEREF _Toc163365670 \h 17
4.12	Naming and Configuration	 PAGEREF _Toc163365671 \h 18
4.13	Environment and Security Context	 PAGEREF _Toc163365672 \h 18
4.14	Non-Functional Requirements	 PAGEREF _Toc163365673 \h 18
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc163365674 \h 19
5.1	Scope	 PAGEREF _Toc163365675 \h 19
5.2	Data Validation	 PAGEREF _Toc163365676 \h 19
5.3	Filtering	 PAGEREF _Toc163365677 \h 19
5.4	Mapping	 PAGEREF _Toc163365678 \h 19
5.5	Target Message Schema	 PAGEREF _Toc163365679 \h 19
5.6	Message Transport Details	 PAGEREF _Toc163365680 \h 19
5.7	Naming and Configuration	 PAGEREF _Toc163365681 \h 19
5.8	Environment and Security Context	 PAGEREF _Toc163365682 \h 19
5.9	Non-Functional Requirements	 PAGEREF _Toc163365683 \h 19
6	Testing Deliverables	 PAGEREF _Toc163365684 \h 20
7	Deployment	 PAGEREF _Toc163365685 \h 21
8	Assumptions and Outstanding Issues	 PAGEREF _Toc163365686 \h 22
8.1	Assumptions	 PAGEREF _Toc163365687 \h 22
8.2	Outstanding Issues	 PAGEREF _Toc163365688 \h 22
Appendix A Volumes	 PAGEREF _Toc163365689 \h 23
•	Glossary	 PAGEREF _Toc163365690 \h 24
Appendix B Document Control	 PAGEREF _Toc163365691 \h 25

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements with respect to STORELINE interface (D029) Stock take result data updating into the GFO system interface (D022).

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. Therefore the GFO system Technical System Document (TSD) and STORELINE system Functional System Document are provided for better understanding of this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including STORELINE and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Stock take result data from STORELINE into GFO.

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
The interface is to upload the Stock take result data from STORELINE interface D029 into GFO interface D022. The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Stock take result data in (| delimited flat file) from STORELINE interface (D029). The STORELINE interface will put this file (*.dat) in the shared location through RTI SOAP adapter. The BizTalk server then transfers this flat file data by invoking GFO interface (D022) stored procedures through DB2 adopter. BizTalk will first invokes JH0S00– package return STREAM info - stored procedure to get the stream information which is passed along with other input attributes of JI0P13 – stored procedure to get updated/inserted in GFO underlying table. The output attributes returned by stored procedure will determine the success/failure of this updating.

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
The interface should be capable of extracting data in the form of flat file from the shared location at STORELINE side and delivering the resulting into GFO side database tables before the identified cut-off time. The interface should run on real time basis. 
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
STORELINE creates a pipe | delimited flat file whenever stock take has been taken and put the file in a dedicated shared location. The flat file extension is *.dat and BizTalk in turn picks up the file from the shared location and invokes series of subroutines through DB2 Adopter to update/insert the underline table of GFO. 
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
DETAIL RECORDS 
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
Windows

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
Package Name: TOM.D029toD022.StockTake.STORELINEtoGFO
BizTalk Procedure
Name
TOM.D029toD022.StockTake.STORELINEtoGFO
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
The BizTalk server transfers the source message schema file to GFO by invoking a series of stored procedures within DB2.This will first invokes JH0S00– stored procedure by taking Store No as input attributes- to get the stream information as output parameter which is passed along with other input attributes of JI0P13 stored procedure to get updated/inserted in GFO underlying table. 
Data Validation
Data Validation will be done by the target GFO system.
Filtering
There is no filtering requirement.
Stored Procedures
The stock event data from STORELINE then immediately use it to invoke the relevant stored procedure(s) within DB2. The types of stock event involved are:

Stock takes

The following description gives the details of stored procedure need to be invoked to pass data from STORELINE to GFO.
JH0S00 – Package to return STREAM info 
JIP00 will determine a store’s database stream then point subsequent processing to that package set.
JI0P13– process stock takes – new subroutine
JI0P13 will take stock take data and use it to update the following tables:

	TXJJ0ASC	applied stock count
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ003D)

STORELINE Reason Code 314 = stock count (absolute)
 


Mapping
The STORELINE Stock take ROWSET get created by BizTalk and passed to GFO subroutines as input attributes. The input attribute order with its source mapping are given below,
Mapping of JH0S00 – Package to return STREAM info 
The stored-procedure returns the STREAM field details. The input attribute to this store procedure is STORE ID which returns stream details and will be used with other store procedure as an input attributes. The foot-print of this stored procedure given below 

Sr NoAttribute Field NameFormatSource Field TypeSource 
Field NameDescriptionINPUT ATTRIBUTES
1
IN_RO_NO
DECIMAL(5 , 0)
SetDtl
Store No
I/P attributes to stored procedure.
OUTPUT ATTRIBUTES
1
OUT_STREAM
CHARACTER(1)


Stream Name(requires to be used in following stored procedures)
2
OUT_CODE_LEVEL
CHARACTER(1)



3
OUT_CR_PART_NO
CHARACTER(2)



4
OUT_RO_NAME
CHARACTER(25)


Store Name
5
OUT_ERROR_CODE
DECIMAL(2 , 0)


Contains the return code to indicate the success or failure of the call
6
OUT_ERROR_LOG
CHARACTER(29)


Contains some simple diagnostics of the programme causing a fatal error

The return output attributes determine the success/failure of data insert/update in GFO e.g.

0 - successful update
1 - System unavailable
4 - Store not found
5 - Steam invalid
6 - Fatal error
8 - Code level invalid 

In either cases the message need to be written on event log. In case of failure the subscription message get suspended but remain in disposable mode which keeps on trying to get success stream information from stored procedure to execute subsequent stored procedure. The failures of this stored procedure also stop execution of following stored procedure and move to next ROWSET.

In case of failure a log file has to be maintained as per the format given below e.g.

< Source File Name >. < Store Procedure Name >. < Processed DATE/TIME > -                                   < OUT_ERROR_CODE > - < OUT_ERROR_LOG >
Mapping of JI0P13– process stock takes 
The foot-print of this stored procedure with its ROWSET mapping details are given below –

Sr NoAttribute Field NameCobol FormatSource Field TypeSource 
Field NameDescriptionINPUT ATTRIBUTES
1
IN_STREAM     
CHARACTER(1)


Output attribute of JH0S00 Stored Procedure
2
IN_RO_NO      
CHARACTER(5)
SetDtl
Store No
Store id comes from source schema
3
IN_APPLIC_CD
CHARACTER(8)


It is a unique application identifier. Set to “D029D022”
4
IN_APP_DATETIME
CHARACTER(23)


It is the timestamp of when the calling application called. It will have the Format: yyyy-mm-dd-hh:mm:ss:ttt
5
IN_BPR_TPN    	
CHARACTER(9)
SetDtl
Item Number
Item number on which stock take has been taken
6
IN_COUNT_DATE 
CHARACTER(10)
SetDtl
Date of Extract
CCYY-MM-DD
7
IN_COUNT_TIME 
CHARACTER(8)
SetDtl
Time of Extract
HH.MM.SS
8
IN_QUANTITY   
CHARACTER(7)
SetDtl
Count Qty
Stock takes quantity
OUTPUT ATTRIBUTES
1
OUT_ERROR_CODE.  
DECIMAL(4 , 0)


Returned ZERO in case of success
2
OUT_ERROR_LOG   
CHARACTER(29)




The return output attributes determine the success/failure of data insert/update in GFO.In either cases the message need to be written on event log. In case of failure a log file has to be maintained as per the format given below e.g.

<Source File Name>.<Store Procedure Name>. <Processed DATE/TIME> . < OUT_ERROR_CODE > - < OUT_ERROR_LOG   > 


Message Format
  Message Transport Details
For messages destined for GFO system, the following applies.	

Feature
Specification
Additional Information
Source System Name
Biztalk 2006

Source Platform / OS
Biztalk 2006 Server/Windows Server 2003

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
DB2 Adapter                                    

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

Currently it will keep all error details in a txt file. Later this may change as per the business decision.


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
2
Assuming STREAM information is extracted from JH0S00 stored procedure through DB2 adopter for each input ROWSET.

Outstanding Issues
ID
Issue
To be addressed by
1
DB2 adopter specification to call sub procedures need to be defined
Erwin Oguz
2
Error handling with respect to DB2 copybook need to be defined
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
GFO
Group Forecasting and Ordering
The GFO operates on Tesco deals with the forecasting & Ordering.
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
DB2
Database access adopter
It is used to access AS/400 platform. This helps to invokes underlying database stored procedure from outside. It has capability to invoke stored procedure as per the ROWSET.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
09/02/2007
0.1D
Draft
Ganesan, Sankar
11/02/2007
0.1D
Draft
Debasis Pattanaik
12/02/2007
0.2D
Draft – incorporating Erwin review comments.
Debasis Pattanaik
02/04/2007
1.1
Signed Off – Incorporated DB2 specific Stored Proc by removing previously used COBOL formatted stored proc. 



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



Version 1.1 Signed Off	Page:  PAGE  \* MERGEFORMAT 16 of  NUMPAGES 25	Date:  SAVEDATE \@ "d MMM yyyy" 4 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture




