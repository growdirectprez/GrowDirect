		







TOM Integration

Interface Specification 
For
Stock Transfer Receits

From STORELINE to ORMS



[D036 to D038]





Project BEN Code:
W60416
Author:
Debasis Pattanaik	
Date:
01/03/2007
Version:
0.1
Status:
Draft
Modified By:
Debasis Pattanaik
Reviewed By:


Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
01/003/2007
0.1D
Draft
Sankar G




Reviewers

Name
Date
Version
Position
Ganesan, Sankar



Erwin Oguz













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

Related Documents: STORELINE system FSD document 

Directory: Embedded in this document.

File Name: 

STORELINE system FSD document - FS1847_BO_Stock_Interfaces.doc

 EMBED Word.Document.8 \s 


Information Architecture Context diagram
D036  D038- StockTransfer Receits_Information_Context_Diagram.vsd

Mapping spreadsheet
D036  D038- StockTransfer Receits - mapping document.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc160859859 \h 7
1.1	Purpose of Document	 PAGEREF _Toc160859860 \h 7
1.2	Background	 PAGEREF _Toc160859861 \h 7
1.3	Scope	 PAGEREF _Toc160859862 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc160859863 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc160859864 \h 8
2.2	Architecture	 PAGEREF _Toc160859865 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc160859866 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc160859867 \h 10
3.1	Scope	 PAGEREF _Toc160859868 \h 10
3.2	Source Message Schema	 PAGEREF _Toc160859869 \h 10
3.3	Message Format	 PAGEREF _Toc160859870 \h 11
3.4	Message Transport Details	 PAGEREF _Toc160859871 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc160859872 \h 12
3.6	Environment and Security Context	 PAGEREF _Toc160859873 \h 13
3.7	Non-Functional Requirements	 PAGEREF _Toc160859874 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc160859875 \h 14
4.1	Scope	 PAGEREF _Toc160859876 \h 14
4.2	Data Validation	 PAGEREF _Toc160859877 \h 14
4.3	Filtering	 PAGEREF _Toc160859878 \h 14
4.4	Mapping	 PAGEREF _Toc160859879 \h 14
4.5	Target Message Schema	 PAGEREF _Toc160859880 \h 14
4.6	Message Format	 PAGEREF _Toc160859881 \h 15
4.7   Message Transport Details	 PAGEREF _Toc160859882 \h 16
4.7	Naming and Configuration	 PAGEREF _Toc160859883 \h 17
4.8	Environment and Security Context	 PAGEREF _Toc160859884 \h 17
4.9	Non-Functional Requirements	 PAGEREF _Toc160859885 \h 17
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc160859886 \h 18
5.1	Scope	 PAGEREF _Toc160859887 \h 18
5.2	Data Validation	 PAGEREF _Toc160859888 \h 18
5.3	Filtering	 PAGEREF _Toc160859889 \h 18
5.4	Mapping	 PAGEREF _Toc160859890 \h 18
5.5	Target Message Schema	 PAGEREF _Toc160859891 \h 18
5.6	Message Transport Details	 PAGEREF _Toc160859892 \h 18
5.7	Naming and Configuration	 PAGEREF _Toc160859893 \h 18
5.8	Environment and Security Context	 PAGEREF _Toc160859894 \h 18
5.9	Non-Functional Requirements	 PAGEREF _Toc160859895 \h 18
6	Testing Deliverables	 PAGEREF _Toc160859896 \h 19
7	Deployment	 PAGEREF _Toc160859897 \h 20
8	Assumptions and Outstanding Issues	 PAGEREF _Toc160859898 \h 21
8.1	Assumptions	 PAGEREF _Toc160859899 \h 21
8.2	Outstanding Issues	 PAGEREF _Toc160859900 \h 21
Appendix A Volumes	 PAGEREF _Toc160859901 \h 22
•	Glossary	 PAGEREF _Toc160859902 \h 23
Appendix B Document Control	 PAGEREF _Toc160859903 \h 24

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements with respect to STORELINE interface (D036) Stock Transfer receits (inter store transfer) data updating into the ORMS system interface (D038).

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. Therefore the STORELINE system Functional System Document are provided for better understanding of this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including STORELINE and ORMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Stock Transfer receits e.g. inter store transfer data from STORELINE into ORMS.

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
The interface is to upload the Stock Transfer receits e.g. inter store transfer data from STORELINE interface D036 into ORMS interface D038. The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Stock Transfer receits data for inter store transaction in (| delimited flat file) from STORELINE interface (D036). The STORELINE interface will put this file (*.dat) in the shared location through RTI SOAP adapter. The BizTalk server then transfers this flat file data to a XML file which then transfer to ORMS through RIB in form of RIB messages. The transformation from BizTalk XML file to RIB message will be done through JMS adopter with the usage of RIB assembler. In turn RIB messages then publish those messages for subscription to update ORMS database in real-time basis. The transformations of XML file to RIB message determine the success/failure. In case of failure it will write into an error log file and does not require any archive process.

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
STORELINE creates a pipe | delimited flat file whenever stock Transfer receits e.g. inter store transfer data has been taken and put the file in a dedicated shared location. The flat file extension is *.dat and BizTalk in turn picks up the file from the shared location and converts it to a XML file which in turn converted to RIB message through JMS adopter with the help of RIB assembler for update/insert of the underline table of ORMS. 
Source Message Schema
Sr. No
Field Name
Mandatory
Type
Description
HEADER RECORD
1
Type 
Y
H
Type of record
2
Date of file extract / creation
Y
Ccyymmdd
Store-line extraction date
3
Time of file extract / creation
Y
Hhmmss
Store-line extraction date
4
Store No.          / From Store
Y
Numeric
Store Id
5
Order Number /Transaction #
Y
Numeric
Order Number e.g. transaction number
6
Record Type

Char 
Record Type determine inter store transfer.(e.g. 322-store to store transfer)
7
Store Name

Char
Store Name
8
Store Address

Char
Store Address
9
Supplier Code /       To Store
Y
Char
Item Supplier Code
10
Supplier Name

Char
Name of Supplier
11
Supplier Address

Char
Address of supplier
12
Supplier Type

Numeric 
Type of supplier
13
Order Date 

Ccyymmdd
Order e.g. transaction date
14
Expected Del Date

Ccyymmdd
Expected delivery date
15
Del After Date

Ccyymmdd
Delivery after date
16
Del Before Date

Ccyymmdd
Delivery before date
17
Transaction date & time
Y
Ccyymmddhhmmss
Date Time of transaction
18
Order Type/   Count Type

Numeric
Type of Order e.g. Criteria of selecting extract data
19
Invoice Number

Char
Invoice Number
20
Ref No 1

Char
First Reference Number
21
Ref No 2

Char
Second Reference Number
22
Captured by/ Created by

Char
File created person 
23
Driver's name/Courier

Char
Driver of this file
24
Original Order number

Numeric
Original Order No
25
Remarks

Char
Remarks
26
Reason Code

Numeric
Reason Code
27
No. of Detail Lines

Numeric
Number of detail lines
28
Total Qty

Numeric (10,4)
Total Quantity of stock transfer
29
Total Value

Numeric (7,2)
Total Value of transfer
30
Invoice Total

Numeric (7,2)
Total Value of invoice
31
Invoice Tax Total

Numeric (7,2)
Invoice Tax total paid of invoice amount
32
Description

Char
Description of inter-stock transfer
33
User name

Char
Created user name
34
Re-processed flag (export only)

Numeric (0/1)
Re-processing flag
DETAIL RECORD
1
Type 
Y
D
Type of record
2
Date of extract
Y
Ccyymmdd
Extract date of data
3
Time of extract
Y
Hhmmss
Extract time of data
4
Store No.
Y
Numeric
Store No
5
Order Number /Transaction #
Y
Numeric
Order Number e.g. transaction number
6
Record Type
Y
Char 
Record Type determine inter store transfer.(e.g. 322-store to store transfer)
7
Line number
Y
Numeric
Record Line Number(Record starts from 1)
8
Item Number 
Y
Numeric
Inter-store transfer item number
9
Item Description

Char
Inter-store transfer item description
10
Supplier item # / catalogue #

Char
Inter-store transfer supplier item catalogue no
11
UOM Code

Numeric
Unit of measure code
12
UOM Description

Char
Unit of measure details
13
Pack size / Ratio
Y
Numeric
Pack size
14
Order Quantity / Sent quantity

Numeric (8,4)
Order Quantity
15
Transaction cost price (excl) per UOM

Numeric (6,2)
Transaction cost price excl UOM
16
Order Type

Numeric
Inter-transfer order type
17
Reference No.

Numeric
Reference Number
18
 Transaction Qty / Count qty  / Acknowledged qty
Y
Numeric (8,4)
Inter-transfer sent quantity
19
Reason Code

Numeric
Reason Code
20
Invoice Qty

Numeric (8,4)
Invoice Quantity
21
Invoice Cost (excl) per UOM

Numeric (6,2)
Invoce cost excl per UOM
22
Tax % on cost

Numeric (6,2)
Tax % on invoice cost
23
Selling Price per UOM

Numeric (6,2)
Selling price per Unit of measure
24
Location

Char
Store Location
25
Sign (Only for 315 & 323)

+ / -
Sign indicator 
 - negative 
+ positive

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
SOAP/Web service  	
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
Package Name: TOM.D036 to D038 Integration STOCK TRANSFER RECEITS STORELINE to ORMS
BizTalk Procedure
Name
TOM.D036 to D038 Integration STOCK Transfer Receits STORELINE to ORMS
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
The target message schema has been given in below table format,

Record 
NameField Name
Field Type
Start PosEnd PosDescription
Header 
Record Type descriptor
char
1
5
Single File Header record
Indicates the structure of the rest of the current record. 
Constant value  FHEAD
File record number
integer
6
15
Line number of record in the file - not validated - but used when reporting errors/rejections. 
It starts with  0000000001
File Type Descriptor
char
16
35
Constant Code to indicate file type. 
Constant  Value  TSC_TSFIUPLD
Create Date
char
36
43
Date when file was generated 'YYYYMMDD’. It will be mapped to – 
SetHdr Date of extract
Create Time
char
44
49
Time when file was generated ' HHMMSS’. It will be mapped to – 
SetHdr Timeof extract
Location Type
char
50
50
Constant Value ‘S’
Location
number
51
60
This is to location.It is mapped to –
SetHdr Supplier Code/To Store

TxnHdr

Record Type descriptor
char
1
5
Indicates the structure of the rest of the current record.
Constant value  THEAD
File record number
integer
6
15
Line number of record in the file. It will be start from  000000000n
Receipt sequence no
integer
16
25
unique for each receipt within the current transaction e.g. 1 for first receipt, and then increment for each subsequent receipt
from Location
char
26
35
This is to location.It is mapped to –
SetHdr  Store No. / From Store
transfer no
char
36
49
ORMS transfer external reference mapped to SetHdr  Order Number /Transaction #
waybill
char
50
63
SetHdr  WayBill
Comments
char
64
223
SetHdr  Captured by/ Created by

Rcpt Dtl
Record Type descriptor
char
1
5
Indicates the structure of the rest of the current record.This has constant value  TRDTL
File record number
integer
6
15
Line number of record in the file. It will be sequential number with format 
000000000n
Receipt sequence no
integer
16
25
Matches RCPT receipt sequence no of TxnHdr.
Detail sequence no
integer
26
35
Unique for each receipt within the current transaction e.g. 1 for first receipt, and then increment for each subsequent receipt
item_id
char
36
60
Set Dtl  Item Number
unit_qty
number
61
73
Set Dtl  Transaction Qty
to_disposition
char
88
91
Constant Value ‘ATS’
receipt_date
char
74
87
setDtlDateofExtract || setDtlTimeofExtract
Txn Trailer
Record Type descriptor
char
1
5
Constant Value – TTAIL
File Line Number
number
6
15
Line number of record in the file. The format will be  000000000n
Txn Record count
number
16
21
Transaction Record Count in format  000000000n
File Trailer

Record Type descriptor
char
1
5
Single File Trailer Record
Indicates the structure of the rest of the current record. 
Constant Value  FTAIL
File record number
number
6
15
Line number of record in the file. The format will be  000000000n
Detail record count
number
16
25
count of number of records in the file excluding the file header and trailer record. The format will be  000000000n
Message Format
The source message is a pipe | delimited flat file from STORELINE and is getting converted into the target file format for ORMS in a package. The target message is a XML file. This file again mapped in RIB assembler for conversion of a RIB message.
4.7   Message Transport Details 
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
1
Error handling
Erwin Oguz
2
Error log file location need to de defined
Erwin Oguz
3
STORELINE source file Physical Location need to be defined
Erwin Oguz
4
ORMS RIB expected target schema need to be defined
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
01/03/2007
0.1D
Draft
Sankar G






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


























	










Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Interface Specification



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Error! Reference source not found.	Page:  PAGE  \* MERGEFORMAT 24 of  NUMPAGES 24	Date:  SAVEDATE \@ "d MMM yyyy" 5 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Interface Specification




