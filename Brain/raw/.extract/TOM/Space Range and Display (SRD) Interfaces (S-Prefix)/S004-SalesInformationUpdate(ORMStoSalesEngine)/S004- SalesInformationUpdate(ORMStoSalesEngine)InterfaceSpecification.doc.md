		









`


TOM Integration
Interface Specification
On 
Sales Information Update
From RMS to Sales Engine


[S004]





Project BEN Code:
W60416
Author:Shajitha MohammedDate:
13/04/2007
Version:
0.1
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft
Modified By:

Reviewed By:


Change Record

Author
Date
Version
Change Reference, description
Shajitha Mohammed
13-04-2007
0.1
Draft













Reviewers

Name
Date
Version
Position


















At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer

Position

Signature
<Physical signature or via email approval>
Date
Dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version
Andrew Barker


John Cowper


Jon Braggs


David Onyett


Venkateswara Rao


Mary Welch


Prasanth Dukaram



Document Source
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS036&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" DocShare: UK IT/TOM Integration/Shared Documents

Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.

Mapping spreadsheet
S004- SalesInformationUpdate(RMStoSalesEngine) Mappings.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc160870575 \h 5
1.1	Purpose of Document	 PAGEREF _Toc160870576 \h 5
1.2	Background	 PAGEREF _Toc160870577 \h 5
1.3	Scope	 PAGEREF _Toc160870578 \h 5
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc160870579 \h 6
2.1	Description of the End-to-End Interface	 PAGEREF _Toc160870580 \h 6
2.2	Architecture	 PAGEREF _Toc160870581 \h 6
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc160870582 \h 6
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc160870583 \h 7
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc160870584 \h 7
3.1	Scope	 PAGEREF _Toc160870585 \h 7
3.2	Source Message Schema	 PAGEREF _Toc160870586 \h 8
3.3	Message Transport Details	 PAGEREF _Toc160870587 \h 9
4	Processing Required in the SSIS Stage of the Interface	 PAGEREF _Toc160870588 \h 10
4.1	Scope	 PAGEREF _Toc160870589 \h 10
4.2	Package Overview	 PAGEREF _Toc160870590 \h 10
4.3	Data Validation	 PAGEREF _Toc160870591 \h 10
4.4	Filtering	 PAGEREF _Toc160870592 \h 10
4.5	Mapping	 PAGEREF _Toc160870593 \h 10
4.6	Target Message Schema	 PAGEREF _Toc160870594 \h 10
4.7	Message Transport Details	 PAGEREF _Toc160870595 \h 11
4.8	Naming and Configuration	 PAGEREF _Toc160870596 \h 11
4.9	Environment and Security Context	 PAGEREF _Toc160870597 \h 12
4.10	Non-Functional Requirements	 PAGEREF _Toc160870598 \h 12
5	Testing Deliverables	 PAGEREF _Toc160870599 \h 12
6	Deployment	 PAGEREF _Toc160870600 \h 13
7	Assumptions and Outstanding Issues	 PAGEREF _Toc160870601 \h 14
7.1	Assumptions	 PAGEREF _Toc160870602 \h 14
7.2	Outstanding Issues	 PAGEREF _Toc160870603 \h 14
Appendix A Volumes	 PAGEREF _Toc160870604 \h 15
Appendix B Glossary	 PAGEREF _Toc160870605 \h 16
Appendix C Document Control	 PAGEREF _Toc160870606 \h 17

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements to transfer the sales data from RMS to Sales Aggregation engine. The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US and Turkey implementation.

Background
The Space, Range and Display (SRD) stream within Group IT has identified a need to summarise sales data to assist with Ranging and Display.  In the Operating Model there is a need to source this sales data, and present it to the SRD systems for summarisation across a cluster of stores (or all stores), a (display) group of products, and one or more weeks, up to 2 years of history. This aggregated sales history data will be available to Range system and IKB to generate store ranges and Planogram.
The purpose of this interface is to transmit the sales information from RMS to the Sales Aggregation Engine system. 
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
The interface is a batch extract of sales information from RMS tables and sends it as a flat file for the sales aggregation engine via integration layer. 

Architecture
 EMBED Visio.Drawing.11  

Requirements of the End-to-End Interface
The interface will run once a day on scheduled basis and consists of a SQL Server Integration Services package that extracts daily data from the RMS tables and formats it into the target file format for sales engine. The extracted file is kept in a shared folder in the integration layer. The Sales aggregation system would pick the files from the windows shared location.
	
The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI and SSIS. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface
 
Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting the data from RMS tables and deliver the resulting data into a flat file before the identified cut-off time. The interface should run on scheduled batch basis during night. 
Reliability and Availability Requirements
The interface-run should be non atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The successful delivery, failure in the creation of the extract, and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate. (Refer to 7.2 Outstanding Issues).
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration. 
 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing Required in the Extract Stage of the Interface 
Scope
This section describes the data sources required by this interface and the services used to access the data.
A scheduled batch job/s runs, at a pre-configured time, to extract the sales information from RMS tables. This batch job in turn kicks off a process that executes SQL server Integration Services package against these tables and generates a complete unload of required data-set as a flat file to a shared location in the integration layer. The data is also transformed to the required format within SSIS package
Source Message Schema
The data for this interface resides in the RMS tables and the source messages are generated from the IF_TRAN_DATA and ITEM_LOC tables. The details of the source tables are as follows.

IF_TRAN_DATA: Source Message Schema for RMS 10

Field Name
Type
ITEM
VARCHAR2 (25)
DEPT
NUMBER (4)
CLASS
NUMBER (4)
SUBCLASS
NUMBER (4)
PACK_IND
VARCHAR2 (1)
STORE
NUMBER (10)
WH
NUMBER (10)
TRAN_DATE
DATE
TRAN_CODE
NUMBER (2)
ADJ_CODE
VARCHAR2 (1)
UNITS
NUMBER (12, 4)
TOTAL_COST
NUMBER (20, 4)
TOTAL_RETAIL
NUMBER (20, 4)
REF_NO_1
NUMBER (10)
REF_NO_2
NUMBER (10)
OLD_UNIT_RETAIL
NUMBER (20, 4)
NEW_UNIT_RETAIL
NUMBER (20, 4)
PGM_NAME
VARCHAR2 (100)
SALES_TYPE
VARCHAR2 (1)
VAT_RATE
NUMBER (12, 4)
AV_COST
NUMBER (20, 4)
 
IF_TRAN_DATA: Source Message Schema for RMS 12

Field Name
Type
ITEM
VARCHAR2 (25)
DEPT
NUMBER (4)
CLASS
NUMBER (4)
SUBCLASS
NUMBER (4)
PACK_IND
VARCHAR2 (1)
LOC_TYPE
VARCHAR2 (1)
LOCATION
NUMBER (10)
TRAN_DATE
DATE
TRAN_CODE
NUMBER (2)
ADJ_CODE
VARCHAR2 (1)
UNITS
NUMBER (12, 4)
TOTAL_COST
NUMBER (20, 4)
TOTAL_RETAIL
NUMBER (20, 4)
REF_NO_1
NUMBER (10)
REF_NO_2
NUMBER (10)
GL_REF_NO
NUMBER (10)
OLD_UNIT_RETAIL
NUMBER (20, 4)
NEW_UNIT_RETAIL
NUMBER (20, 4)
PGM_NAME
VARCHAR2 (100)
SALES_TYPE
VARCHAR2 (1)
VAT_RATE
NUMBER (12, 4)
AV_COST
NUMBER (20, 4)
 
ITEM_LOC: Source Message Schema for RMS 10

Field Name
Type
ITEM
VARCHAR2 (25)
LOC
NUMBER (10)
ITEM_PARENT
VARCHAR2 (25)
ITEM_GRANDPARENT
VARCHAR2 (25)
LOC_TYPE
VARCHAR2 (1)
UNIT_RETAIL
NUMBER (20, 4)
SELLING_UNIT_RETAIL
NUMBER (20, 4)
SELLING_UOM
VARCHAR2 (4)
PROMO_RETAIL
NUMBER (20, 4)
PROMO_SELLING_RETAIL
NUMBER (20, 4)
PROMO_SELLING_UOM
VARCHAR2 (4)
CLEAR_IND
VARCHAR2 (1)
TAXABLE_IND
VARCHAR2 (1)
LOCAL_ITEM_DESC
VARCHAR2 (100)
LOCAL_SHORT_DESC
VARCHAR2 (20)
TI
NUMBER (12, 4)
HI
NUMBER (12, 4)
STORE_ORD_MULT
VARCHAR2 (1)
STATUS
VARCHAR2 (1)
STATUS_UPDATE_DATE
DATE
DAILY_WASTE_PCT
NUMBER (12, 4)
MEAS_OF_EACH
NUMBER (12, 4)
MEAS_OF_PRICE
NUMBER (12, 4)
UOM_OF_PRICE
VARCHAR2 (4)
PRIMARY_VARIANT
VARCHAR2 (25)
PRIMARY_COST_PACK
VARCHAR2 (25)
PRIMARY_SUPP
NUMBER (10)
PRIMARY_CNTRY
VARCHAR2 (3)
RECEIVE_AS_TYPE
VARCHAR2 (1)
CREATE_DATETIME
DATE
LAST_UPDATE_DATETIME
DATE
LAST_UPDATE_ID
VARCHAR2 (30)
SOURCE_METHOD
VARCHAR2 (1)
SOURCE_WH
NUMBER (10)

ITEM_LOC: Source Message Schema for RMS 12
Field Name
Type
ITEM
VARCHAR2 (25)
LOC
NUMBER (10)
ITEM_PARENT
VARCHAR2 (25)
ITEM_GRANDPARENT
VARCHAR2 (25)
LOC_TYPE
VARCHAR2 (1)
UNIT_RETAIL
NUMBER (20, 4)
REGULAR_UNIT_RETAIL
NUMBER (20, 4)
MULTI_UNITS
NUMBER (12, 4)
MULTI_UNIT_RETAIL
NUMBER (20, 4)
MULTI_SELLING_UOM
VARCHAR2 (4)
SELLING_UNIT_RETAIL
NUMBER (20, 4)
SELLING_UOM
VARCHAR2 (4)
PROMO_RETAIL
NUMBER (20, 4)
PROMO_SELLING_RETAIL
NUMBER (20, 4)
PROMO_SELLING_UOM
VARCHAR2 (4)
CLEAR_IND
VARCHAR2 (1)
TAXABLE_IND
VARCHAR2 (1)
LOCAL_ITEM_DESC
VARCHAR2 (250)
LOCAL_SHORT_DESC
VARCHAR2 (120)
TI
NUMBER (12, 4)
HI
NUMBER (12, 4)
STORE_ORD_MULT
VARCHAR2 (1)
STATUS
VARCHAR2 (1)
STATUS_UPDATE_DATE
DATE
DAILY_WASTE_PCT
NUMBER (12, 4)
MEAS_OF_EACH
NUMBER (12, 4)
MEAS_OF_PRICE
NUMBER (12, 4)
UOM_OF_PRICE
VARCHAR2 (4)
PRIMARY_VARIANT
VARCHAR2 (25)
PRIMARY_COST_PACK
VARCHAR2 (25)
PRIMARY_SUPP
NUMBER (10)
PRIMARY_CNTRY
VARCHAR2 (3)
RECEIVE_AS_TYPE
VARCHAR2 (1)
CREATE_DATETIME
DATE
LAST_UPDATE_DATETIME
DATE
LAST_UPDATE_ID
VARCHAR2 (30)
INBOUND_HANDLING_DAYS
NUMBER (2, 0)
SOURCE_METHOD
VARCHAR2 (1)
SOURCE_WH
NUMBER (10)
STORE_PRICE_IND
VARCHAR2 (1)
RPM_IND
VARCHAR2 (1)

Message Transport Details

Feature
Specification
Additional Information
Source System Name
RMS

Source Platform / OS
Oracle10g

Source Physical Location
AIX

Source Underlying Data Storage Technology
RDBMS

Target System Name
SSIS

Target Platform / OS
Windows

Target Physical Location
TBD

Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
SSIS  	               	


Data Format.
XML			
Delimited		
Positional		
RDBMS       		
                     

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous		
Asynchronous		
Bulk Data		

Real-time/Scheduled Batch
Scheduled Batch

Archiving
There is no requirement to archive the messages.

Logging
Log via the Operational Framework.

Error Handling



Processing Required in the SSIS Stage of the Interface
Scope
This section describes the discrete steps within the SSIS package to extract and format data. The target schema is included in this section. 
Package Overview
SSIS extracts the current days required information on sales by joining the IF_TRAN_DATA and ITEM_LOC table, at a predefined time formatted as required for the Sales aggregation system. The data formatted to the target system is kept in the shared folder in the integration layer.
Data Validation
N/A.
Filtering
The data from the IF_TRAN_DATA is extracted on daily basis. Following are the filtering conditions used to extract the data from IF_TRAN_DATA table.

The TRAN_CODE = ‘01’ or TRAN_CODE = ‘02’ or TRAN_CODE = ‘22’

For every item in the location, their corresponding Selling Unit of Measure information is fetched from the ITEM_LOC table. 

Mapping
Mapping document is placed in the shared location.
	S004-SalesInformationUpdate(ORSMtoSalesEngine)Mappings.xls


Target Message Schema
Field Name
String
Length
Occurs




Header Record

104
1:1
HeaderRECTYPE
Varchar
2

File Creation date
Datetime
14

Date
Date
8

FILLER
Varchar
80

Detail Record

104
1:*
DetailRECTYPE
Varchar
2

ProductID
Varchar
25

TranDate
Date
8

StoreID
Number
10

LocType
Varchar
1

Units
Number
(12,4)

TotalRetail
Number
(20,4)

TotalCost
Number
(20,4)

TranCode
Number
2

UOM
Varchar
4

Trailer Record

104
1:1
TrailerRECTYPE
Varchar
2

RECCOUNT
Number
10

FILLER
Varchar
92

Message Transport Details 
For messages destined for Store Range system, the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
Windows 2003 Server

Source Physical Location
SQL SERVER 2005

Source Underlying Data Storage Technology
RDBMS
	

Target System Name
Integration Layer

Target Platform / OS
Windows

Target Physical Location
Local Folder (Viewed by Sales Engine as share)

Target Underlying Data Storage Technology
Folder share

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter                              
SSIS                                                  

Data Format

XML  				
Delimited 			
Positional 			
RDBMS                                            

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous 			
Asynchronous 			
Bulk Data 			

Real-time/Scheduled Batch
Scheduled Batch

Archiving
There is no archiving requirement

Logging
Should logs be kept of all actions? For how long should these be stored?
Logging should occur, such that the message can be recreated if necessary.

Error Handling
Not yet decided

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.

 
Naming and Configuration

SSIS
Package Name: TOM.S004.ORMStoSalesEngine.SalesUpdate.dtsx

Name
S004_ORMStoSalesEngineSalesUpdate_usp
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



Environment and Security Context
Account details will be included here once we have visibility of the environments. 
Non-Functional Requirements
On successful delivery of the data to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure of transformation of data should be written to the failed log database, and an alert should be raised.
Testing Deliverables
This section should contain a list of discrete deliverables. The following table is an illustrative template only. The exact deliverables will depend on the technologies employed in the interface. 

Deliverable
Description
TBD <stored proc name>
Common Form Stored Procedure
TBD <stored proc name>
Common Form Stored Procedure
TBD <service name>
Common Form Web Service
TBD <SSIS package name> 
Package 
TBD <RTI configuration file>
Xml configuration file exported from RTI. For testing, this should contain the configuration required to support this interface only. 
For production, configuration should be documented under section 7 Deployment.


TBD <script name> 
Unit Test Scripts. Scripts should be provided to:
create databases (including stored procedures).
populate with the minimum set of test data to satisfy functional requirements
notes showing how to use scripts and describing the functions tested.
<installer>
Installers as appropriate to the technology being used.

Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
It is presumed that the IF_TRAN_DATA table is not overwritten unless the day’s sales data is not read by the integration layer.
2.
The Unit of measure information is yet to be clarified by the sales engine team, as of now it is taken as the selling unit of measure from the ITEM_LOC table.

Outstanding Issues
ID
Issue
To be addressed by



1
Data filtered using TRAN_CODE = 22 hold the information for data including and Excluding VAT. Waiting for clarification from business.
Sudha Vaidyanathan
2
Alert numbers/identifiers are yet to be defined






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
GPM
GroupProductMapping
SQL Server Database provided by Product mapping for loading Product details .
IDS
Information Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Store, etc. IDS's reside in the EIA Layer, and are accessed through the EAI Layer.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Shajitha Mohammed
16-Apr-2007
0.1
Draft















Related Documents

Author	
Date
Version
Title


















Distribution
Name
Position
Approver/Contributor/Other
Jon Braggs


Andrew Barker


Welch Mary


Dukaram Prasanth

David Onyett


John Cowper


















	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 8 of  NUMPAGES 18	Date:  SAVEDATE \@ "d MMM yyyy" 17 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































