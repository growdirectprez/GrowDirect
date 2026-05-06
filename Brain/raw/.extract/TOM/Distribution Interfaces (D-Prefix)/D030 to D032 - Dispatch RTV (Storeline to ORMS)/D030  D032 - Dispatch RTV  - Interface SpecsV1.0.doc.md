		








TOM Integration

Interface Specification
For 
Dispatch RTV

STORELINE 
To 
ORMS

[D030 to D032]



Project BEN Code:
W60416
Author:
Debasis Pattanaik
Date:
02/03/2007

Signed-Off
Version:
1.0
Status:
Signed Off
Modified By:

Reviewed By:
Erwin Oguz

Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
21/02/2007
0.1D
Draft
Ganesan, Sankar
26/02/2007
0.2D
Draft
Debasis Pattanaik
02/03/2007
1.0
Signed-Off





Reviewers

Name
Date
Version
Position
Ganesan, Sankar
26/02/2007
0.2D
Draft
Erwin Oguz
02/03/2007
1.0
Signed-Off






At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Erwin Oguz
Position
Solution Architect
Signature

Date
02/03/2007

Distribution List

Name
Date of Issue
Version
Oguz Erwin
02/03/2007
1.0
David Onyett
02/03/2007
1.0
Venkateswara Rao
02/03/2007
1.0







Document Source

Related Documents: XML STORELINE source file schema, ORMS system TSD document & STORELINE system FSD document 

Directory: Embedded in this document

File Name: 
STORELINE source file schema for reference from Turkey – 
tes.chn.retail.storeline.dispatchrtv.v1.4.7						
 EMBED Package  
	

STORELINE system FSD document - FS1847_BO_Stock_Interfaces.doc

 EMBED Word.Document.8 \s 


Information Architecture Context diagram
D030  D032 - Dispatch RTV _Information_Context_Diagram.vsd

Mapping spreadsheet
D030  D032 - Dispatch RTV - mapping document.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc160851478 \h 7
1.1	Purpose of Document	 PAGEREF _Toc160851479 \h 7
1.2	Background	 PAGEREF _Toc160851480 \h 7
1.3	Scope	 PAGEREF _Toc160851481 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc160851482 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc160851483 \h 8
2.2	Architecture	 PAGEREF _Toc160851484 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc160851485 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc160851486 \h 10
3.1	Scope	 PAGEREF _Toc160851487 \h 10
3.2	Source Message Schema	 PAGEREF _Toc160851488 \h 10
3.3	Message Format	 PAGEREF _Toc160851489 \h 11
3.4	Message Transport Details	 PAGEREF _Toc160851490 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc160851491 \h 12
3.6	Environment and Security Context	 PAGEREF _Toc160851492 \h 13
3.7	Non-Functional Requirements	 PAGEREF _Toc160851493 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc160851494 \h 14
4.1	Scope	 PAGEREF _Toc160851495 \h 14
4.2	Data Validation	 PAGEREF _Toc160851496 \h 14
4.3	Filtering	 PAGEREF _Toc160851497 \h 14
4.4	Target Message Schema	 PAGEREF _Toc160851498 \h 14
4.5	Message Format	 PAGEREF _Toc160851499 \h 17
4.6	Message Transport Details	 PAGEREF _Toc160851500 \h 18
4.7	Naming and Configuration	 PAGEREF _Toc160851501 \h 19
4.8	Environment and Security Context	 PAGEREF _Toc160851502 \h 19
4.9	Non-Functional Requirements	 PAGEREF _Toc160851503 \h 19
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc160851504 \h 20
5.1	Scope	 PAGEREF _Toc160851505 \h 20
5.2	Data Validation	 PAGEREF _Toc160851506 \h 20
5.3	Filtering	 PAGEREF _Toc160851507 \h 20
5.4	Mapping	 PAGEREF _Toc160851508 \h 20
5.5	Target Message Schema	 PAGEREF _Toc160851509 \h 20
5.6	Message Transport Details	 PAGEREF _Toc160851510 \h 20
5.7	Naming and Configuration	 PAGEREF _Toc160851511 \h 20
5.8	Environment and Security Context	 PAGEREF _Toc160851512 \h 20
5.9	Non-Functional Requirements	 PAGEREF _Toc160851513 \h 20
6	Testing Deliverables	 PAGEREF _Toc160851514 \h 21
7	Deployment	 PAGEREF _Toc160851515 \h 22
8	Assumptions and Outstanding Issues	 PAGEREF _Toc160851516 \h 23
8.1	Assumptions	 PAGEREF _Toc160851517 \h 23
8.2	Outstanding Issues	 PAGEREF _Toc160851518 \h 23
Appendix A Volumes	 PAGEREF _Toc160851519 \h 24
•	Glossary	 PAGEREF _Toc160851520 \h 25
Appendix B Document Control	 PAGEREF _Toc160851521 \h 26

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements with respect to STORELINE interface (D030) Stock movement data (e.g. to supplier) updating into the ORMS interface (D032) system.

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. Therefore the STORELINE system Functional System Document is provided for better understanding of this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including STORELINE and ORMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Stock movement data from STORELINE into ORMS.

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
The interface is to upload the Stock movement data from STORELINE interface (D030) into ORMS interface (D032). The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Stock movement of item in (| delimited flat file) from STORELINE interface (D030). The STORELINE interface will put this file (*.dat) in the shared location through RTI SOAP adapter. The BizTalk server then transfers this flat file data to a XML file which then transfer to ORMS through RIB in form of RIB messages. The transformation from BizTalk XML file to RIB message will be done through JMS adapter with the usage of RIB assembler. In turn RIB publishes those messages for subscription to update ORMS database in real-time basis. The transformations of XML file to RIB message determine the success/failure. In case of failure it will write into an error log file and does not require any archive process.

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
STORELINE creates a pipe | delimited flat file whenever stock movement has been taken and put the file in a dedicated shared location. The flat file extension is *.dat and BizTalk in turn picks up the file from the shared location and converts it to a XML file which in turn converted to RIB message through JMS adopter with the help of RIB assembler for update/insert of the underline table of ORMS. 
Source Message Schema
Field Name
Optional
Type
Description
HEADER RECORDS
CapturedBy-CreatedBy
Yes
String
Extract file created user name
DateOfExtract

Date
Store-line extraction date
DelAfterDate
Yes
String
Delivery before date
DelBeforeDate
Yes
String
Delivery after date
Description
Yes
String
Free form description
DriversName-Courier
Yes
String
Courier Driver Name
ExpectedDelDate
Yes
String
Expected delivery date
InvoiceNumber
Yes
String
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
String
Order Date
OrderType-CountType
Yes
ui8
Order Type
OriginalOrderNumber
Yes
ui8
Order Number
ReasonCode
Yes
ui8
Reason Code
RecordType

String
Record Type
RefNo2
Yes
String
Reference No 2
Remarks
Yes
String
Remarks
ReProcessedFlag
Yes
String
Re-Processed Flag
StoreAddress
Yes
String
Store address
StoreName
Yes
String
Store Name
StoreNo-FromStore

ui8
Store Id
SupplierAddress
Yes
String
Supplier address
SupplierCode

String
Supplier Code
SupplierName
Yes
String
Supplier Name
SupplierType
Yes
ui8
Supplier Type
TimeOfExtract

Time
Extraction time
TotalQty
Yes
ui8
Total movement Qty
TotalValue
Yes
ui8
Total movement value
TransactionDateTime

String
Transaction Date
TransactionNo

ui8
Transaction No
UserName
Yes
String
Operator Name
WayBill
Yes
String
Waybill Number
DETAIL RECORDS –Group starts it will contain multiple record
DateOfExtract

String
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
String
Description of Item
ItemNumber

ui8
Item Number
LineNumber
Yes
ui8
Record Line Number(Record starts from 1)
Location
Yes
string
Location of extract item
OrderNumber-TransactionNumber

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
ui8
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
TransactionQty

float
Transaction Quantity
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
FTP			
SOAP Adopter 	               
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
Package Name: TOM.D030 to D032 Integration Dispatch RTV from STORELINE to ORMS
BizTalk Procedure
Name
TOM.D030 to D032 Integration Dispatch RTV from STORELINE to ORMS
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



The naming standard to be followed as mentioned in the document – 

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
  Target Message Schema
Target Message Schema in XML format before it passed on to RIB assembler:

 EMBED Package  The Description of the fields as mentioned in the XML file:

Record 
NameField Name
Field Type
Start PosEnd PosDescription
FileHdr

LineNumber
Number
6
15
Sequential line number in the file 
FileTypeDefination
Char
16
35
Constant Value- “TSCDSPRTVUPLD_V2.0”
CreateDate
Date
36
43
setHdr  DateofExtract (YYYYMMDD)
CreateTime
Time
44
49
setHdr  TimeofExtract (HHMMSS)
LocationType
Char
50
50
Constant Value- “S”
Location
Number
51
60
setHdr  StoreNo-FromStore

FileDtl

FileRecordNumber
Number
6
15
Sequential record number incremented by 1 
Ext_Ref_No
Char
26
39
Concatenated field & for every record it get repeated - 

Right ( "00000000"  
+ 
Trim( setHdr  Transaction No ) , 8) 
+ 
Trim ( setHdr  StoreNo-FromStore)
Item
Char
40
64
setDtl  ItemNumber
Ret_Auth_Num
Char
65
76
setHdr  WayBill
Unit_Qty
Number
77
89
setDtl  Transaction Qty
Supplier
Char
90
99
For every record it get repeated - 
setHdr  Supplier Code
From_Disp
Char
596
599
Constant Value  “ATS”
Tran_Date
Char
600
613
Concatenated field & will be resulted -

setDtl  DateofExtract
+
setDtl  TimeofExtract
Reason
Char
635
640
It’s get evaluated as per the expression given below,

(rc is a local variable)

if (Trim(setHdr  Reason Code) = "") Then
   rc = Cint(setDtl  Reason Code)

Else
  rc = Cint(setHdr  Reason Code)

End if
  if( rc = 501 )   then ReasonCode="A"
  if( rc = 502 )   then ReasonCode="B"
  if( rc = 503 )   then ReasonCode="C"
  if( rc = 504 )   then ReasonCode="D"
  if( rc = 505 )   then ReasonCode="E"
  if( rc = 506 )   then ReasonCode="F"
  if( rc = 507 )   then ReasonCode="G"
  if( rc = 508 )   then ReasonCode="H"
  if( rc = 509 )   then ReasonCode="I"
  if( rc = 510 )   then ReasonCode="J"
  if( rc = 511 )   then ReasonCode="K"
  if( rc = 512 )   then ReasonCode="M"
  if( rc = 513 )   then ReasonCode="N"
  if( rc = 514 )   then ReasonCode="O"
  if( rc = 515 )   then ReasonCode="P"
  if( rc = 516 )   then ReasonCode="R"
  if( rc = 517 )   then ReasonCode="S"
  if( rc = 518 )   then ReasonCode="T"
  if( rc = 519 )   then ReasonCode="V"

Comments
Char
641
895
Concatenated field & for every record it get repeated - 

setHdr  OrginalOrderNumber
+ 
space(3)
+
setHdr  CapturedBy-CreatedBy
+ 
space(3)
+
setHdr  Remarks   

City
Char
463
582
Pass SPACE
Country
Char
593
595
Pass SPACE
Pcode
Char
583
592
Pass SPACE
Rtv_Order_No
Char
16
25
Pass SPACE
Ship_Addr1
Char
100
219
Pass SPACE
Ship_Addr2
Char
220
339
Pass SPACE
Ship_Addr3
Char
340
459
Pass SPACE
State
Char
460
462
Pass SPACE
Unit_Cost
Number
614
634
Pass ZERO

FileTrlr
DetailRecordCount
Number
16
25
Detail record count incremented to step 1.
FileRecordNumber
Number
6
15
Detail record count decremented to step 2.


Message Format
The source message is a pipe | delimited flat file from STORELINE and is getting converted into the target file format for ORMS in a package. The target message is a XML file. This file again mapped in RIB assembler for conversion of a RIB message.

  Message Transport Details
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
1
Rollback transaction supported by ORMS in case of failure.
2
Assuming the output target schema of this interface is same as ORMS input RIB schema

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
5
ORMS target schema is not similar to the RIB RTVDesc  schema.
Erwin Oguz
6
The reason code for US need to be defined 
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
Tesco Store used for POS, inventory and Cash office management
The STORELINE operates on Tesco Stores for Point of sales operations, Store inventory management & Store Cash Office operation. 
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
RIB Assembler
Retek Integration Bus Assembler
This is a custom code written for TESCO Integration Model to post the RIB message is a required format which is required by RETEK systems. This assembler will convert the XML message with the mapping elements into RIB message. 

Document Control
Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
21/02/2007
0.1D
Draft
Ganesan, Sankar
26/02/2007
0.2D
Draft
Debasis Pattanaik
02/03/2007
1.0
Signed Off



Related Documents

Author	
Date
Version
Title
Isaac
18-Aug-2004
4.0
StoreLine FS1847 – BO Stock Interfaces










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


























	











Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT 



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Error! Reference source not found.	Page:  PAGE  \* MERGEFORMAT 22 of  NUMPAGES 26	Date:  SAVEDATE \@ "d MMM yyyy" 5 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT 


Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT 



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Error! Reference source not found.	Page:  PAGE  \* MERGEFORMAT 26 of  NUMPAGES 26	Date:  SAVEDATE \@ "d MMM yyyy" 5 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT 



This should be stock count on individual or limited range of products.
Is this right? In principle D029 is different. Storeline might be using similar mechanism to extract the message. Nevertheles D029 is different.
Is the name in compliance with what Adrian is proposing? Please confirm
Is this pointing to the document that Adrian is working on
We don’t need URL token for RIB messaging
Reason codes might change for US


