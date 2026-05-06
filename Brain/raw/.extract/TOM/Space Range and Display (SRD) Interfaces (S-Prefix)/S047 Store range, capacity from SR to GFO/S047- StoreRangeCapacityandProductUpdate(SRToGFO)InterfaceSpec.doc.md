		









`


TOM Integration
Interface Specification
On
Store Range Capacity And New & Discontinued Product Information Update from Store Range to GFO


[S047]





Project BEN Code:
W60416
Author:Shajitha MohammedDate:
16/03/2007
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
16/03/2007
0.1
Draft













Reviewers

Name
Date
Version
Position
Andrew Barker
19/03/07
0.1
Engagement Architect














At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer

Position

Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

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

This interface specification requires three documents- an Interface Specification and two Mapping spreadsheets. This section identifies these documents plus other documents as appropriate.

Mapping spreadsheet
S047- Store Range And Capacity Information Update (Store Range to GFO) Mappings.xls
S047-NewAndDiscontinuedProductInformationUpdate(StoreRangetoGFO)Mappings.xls
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
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc160870584 \h 8
3.1	Scope	 PAGEREF _Toc160870585 \h 8
3.2	Source Message Schema	 PAGEREF _Toc160870586 \h 8
3.3	Message Transport Details	 PAGEREF _Toc160870587 \h 8
4	Processing Required in the SSIS Stage of the Interface	 PAGEREF _Toc160870588 \h 9
4.1	Scope	 PAGEREF _Toc160870589 \h 9
4.2	Package Overview	 PAGEREF _Toc160870590 \h 9
4.3	Data Validation	 PAGEREF _Toc160870591 \h 9
4.4	Filtering	 PAGEREF _Toc160870592 \h 9
4.5	Mapping	 PAGEREF _Toc160870593 \h 9
4.6	Target Message Schema	 PAGEREF _Toc160870594 \h 10
4.7	Message Transport Details	 PAGEREF _Toc160870595 \h 10
4.8	Naming and Configuration	 PAGEREF _Toc160870596 \h 11
4.9	Environment and Security Context	 PAGEREF _Toc160870597 \h 11
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
The purpose of this document is to describe the Following interfacing requirements 
To provide the Store Range and Capacity information from Store range system to GFO (Logical interface for S051.5).
To provide the New and Discontinued Product information from Store range system to GFO (Logical interface for S047 and S050).
The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US and Turkey implementation.

Background
The Space Range and Display stream within Group IT has identified a need to understand central ranges at a store level and to communicate store range information downstream to the relevant systems in order to support ordering stock into stores and maintaining the correct range indicators on Shelf Edge Labels.  The range data at store level will also be available to support reporting requirements of Space, Range and Display Operating Model solution
The GFO system needs the store range and capacity information from the Store Range system to feed range data in order to identify the store/product combinations that stock needs to be ordered and replenished. This interface transmits the store range, capacity and information on new and discontinued products from Store range system to GFO. 
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
The interface extracts the store range, capacity and product information from Store Range System to GFO and sends it as two flat files as required for GFO. 

Architecture
 EMBED Visio.Drawing.11  

Requirements of the End-to-End Interface
The interface is a batch extract of Store Range, Capacity and Product data from Store Range and uploads into the GFO system via integration layer. The interface is meant to run at a pre-configured time, which on completion is expected to produce flat-files onto the shared location. This shared location would be monitored by GFO system during specific hours and would be processes by the GFO system. 
The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI and SSIS. At the time of writing (2007-03-16) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface
 
Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting the data from Store Range system and deliver the processed data into flat files before the identified cut-off time. The interface should run on scheduled batch basis. 
Reliability and Availability Requirements
The interface-run should be non atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The successful delivery, failure in the creation of the extract, and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate.
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
This section describes the data source required by this interface and the services used to access the data.
This interface extracts the Store Range, Capacity and Product information from store range system using RTI File Adapter in Biztalk and uploads into the GFO system via integration layer. This on completion is expected to produce a flat-file onto the shared location in GFO using the RTI file adapter.
Source Message Schema
The data for this interface resides in the file and the source messages are generated from the same. The details of the source file.
	
Field Name
String
Size
Occurs




Header Record

44
1:1
HeaderRECTYPE
Integer
2

FileCreatedDate
Varchar
8

FileCreatedTime
Varchar
8

FILLER
Varchar
26

Detail Record

44
1:*
DetailRECTYPE
Integer
2

Store_Number
Integer
5

Product_Number
Integer
9

Range_Start_Date
Varchar
10

Range_End_Date
Varchar
10

Capacity
Integer
4

Promo_Ind
Varchar
1

Display_Group_Code
Varchar
3

Trailer Record

44
1:1
TrailerRECTYPE
Integer
2

RecordCount
Integer
9

FILLER
Varchar
33



Message Transport Details

Feature
Specification
Additional Information
Source System Name
StoreRange

Source Platform / OS
Windows 

Source Physical Location
File Shared Location(TBD)

Source Underlying Data Storage Technology
Flat File

Target System Name


Target Platform / OS


Target Physical Location


Target Underlying Data Storage Technology
In Memory

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
SSIS                                    
RTI File Adapter(BizTalk) 

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
Asynchronous		
Bulk Data		

Real-time/Scheduled Batch
Scheduled Batch

Archiving
There is no requirement to archive the messages.

Logging
Log via the Operational Framework.

Error Handling
On fail move the file to the failed transmissions location.


Naming and Configuration


Package Name: 

Name

<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Processing Required in Biztalk Interface to transfer Store Range and Capacity Data (Logical interface for S051.5)
Scope
This section describes the discrete steps within the Biztalk interface to extract and format data as required for the GFO system. The target schema to load the store range and capacity information is included in this section. 
Process Overview
This interface extracts the Store Range and Capacity information from Store Range, at a predefined time and sends it as a flat file to GFO.
Data Validation
N/A.
Filtering
There is no filtering requirement.
Mapping
Mapping document is placed in the docshare.
	S047-StoreRangeAndCapacityInformationUpdate(StoreRangetoGFO)Mappings.xls



Target Message Schema
Field NameInsync formatStartLengthCOBOL FormatOccurs / 
Description





Header Record
G
1
26
 
1:1
JISCA-RECORD-TYPE	
Integer(2)
1
2
9(2)
Record type (00 for Header)
JLSCA-PROGRAM-NAME        
Varchar(8)

3
8
X(8)
Spaces
JLSCA-DATE-CREATED
Varchar(8)
11
8
X(8)
Date (CCYYMMDD) of sent file
JLSCA-CREATE-TIME
Varchar(8)
19
8
X(8)
Time (hhmmss) of sent file

 
 
 


Detail Record
G
1
26

1:*
JISCB-RECORD-TYPE
Integer(2)
1
2
9(2)
Record type (01 for Detail)
JISCB-RETAIL-OUTLET-NO
Integer(5)
3
5
9(5)

JISCB-BASE-PRODUCT-NO
Integer(9)
8
9
9(9)

JISCB-SHELF-CAPACITY
Integer(5)
17
5
9(5)

JISCB-SHELF-FACING
Integer(2)
 22
 2
99

FILLER
Varchar(3)
24
3
XXX



1
1


Trailer Record
G
1
26

1:1
JISCZ-RECORD-TYPE
Integer(2)
1
2

Record type (99 for Trailer)
JISCZ-PROGRAM-NAME
Varchar(8)
3
8
X(8)

JISCZ-REC-COUNT
Integer(9)
11
9
9(9)
Record count including the header and trailer records.
FILLER
Varchar(7)
20
7
X(7)
Spaces
Message Transport Details 
For messages destined for GFO system, the following applies.	
	
Feature
Specification
Additional Information
Source System Name


Source Platform / OS


Source Physical Location


Source Underlying Data Storage Technology
In Memory	

Target System Name
GFO

Target Platform / OS
Unix

Target Physical Location
GFO_INBOX

Target Underlying Data Storage Technology
Flat File

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter(BizTalk)               
SSIS                                                  

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
Asynchronous 			
Bulk Data 			

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

 
Processing Required in Biztalk Interface to transfer New And Discontinued Product Data (Logical interface for S047 & S050)
Scope
This section describes the discrete steps within the Biztalk interface to extract the information about the new and discontinued product and format data as required by the target GFO system. The target schema is included in this section. 
Process Overview
This interface extracts the New and Discontinued Product information from Store Range, at a predefined time and sends it as a flat file to GFO.
Data Validation
N/A.
Filtering
There is no filtering requirement.
Mapping
Mapping document is placed in the docshare.
	S047-NewAndDiscontinuedProductInformationUpdate(StoreRangetoGFO)Mappings.xls

Target Message Schema
Field NameInsync formatStartLengthCOBOL FormatOccurs / 
Description





Header Record
G
1
80
 
1:1
JLAUA-RETAIL-OUTLET-NO
Integer(5)
1
5
9(5)
Record type (‘00000’ for Header)
JLAUA-DATE-CREATED
Varchar(10)

6
10
X(10)
Date (CCYY-MM-DD) of sent file
JLAUA-CREATE-TIME
Varchar(5)
16
5
X(5)
Time (HH:MM) of sent file
JLAUA-SEQUENCE-NO
Varchar(5)
21
5
X(5)
Unique Sequence Number
FILLER
Varchar(55)
26
55
X(55)
Set to spaces
Detail Record
G
1
80

1:*
JLAUB-RETAIL-OUTLET-NO
Integer(5)
1
5
9(5)
Store Number
JLAUB-BASE-PRODUCT-NO
Integer(9)
6
9
9(9)
Base Product Number
JLAUB-RNGE-CHG-IND
Varchar(1)
15
1
X
Set to Spaces
JLAUB-RANGE-EFFV-DATE
Varchar(10)
16
10
X(10)
Proposed stocked Start Date (CCYY-MM-DD) – May be blank
JLAUB-RANGE-EFFV-END-DATE
Varchar(10)
 26
 10
X(10)
Proposed stocked End Date (CCYY-MM-DD) – May be blank
JLAUB-MERCH-GROUP-CODE
Varchar(3)
36
3
X(3)
Set to Spaces
JLAUB-PRODUCT-TYPE
Varchar(5)
39
5
X(5)
Set to Spaces
JLAUB-TYPE-DESC 
Varchar(5)
44
5
X(5)
Set to Spaces
JLAUB-IMPORTANCE-IND
Varchar(1)
49
1
X
Set to Spaces
JLAUB-SALES-QTY
Integer(11)
50
11
9(8)V9(3)
Set to Zero
FILLER
Varchar(20)
61
20
X(20)
Set to Spaces
Trailer Record
G
1
80

1:1
JLAUZ-RETAIL-OUTLET-NO
Integer(5)
1
5
9(5)
Record type (‘99999’ for Trailer)
JLAUZ-REC-COUNT
Integer(9)
6
9
9(9)
Record count including the header and trailer records.
FILLER
Varchar(66)
15
66
X(66)
Spaces








Message Transport Details 
For messages destined for GFO system, the following applies.	
	
Feature
Specification
Additional Information
Source System Name


Source Platform / OS


Source Physical Location


Source Underlying Data Storage Technology
In Memory	

Target System Name
GFO

Target Platform / OS
Unix

Target Physical Location
GFO_INBOX

Target Underlying Data Storage Technology
Flat File

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter(BizTalk)               
SSIS                                                  

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
Asynchronous 			
Bulk Data 			

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
As there is a need for more clarity on the fields which would be populated by the store range system the spec is written based on assumptions and after gaining more clarity, the spec might undergo minor changes

Outstanding Issues
ID
Issue
To be addressed by



1
Details about the source file structure are to be provided by Store Range System. It may result in rework if there are significant changes to the existing structure. 
Store Range
2
Alert numbers/identifiers are yet to be defined

3
The design of the IMOF is still being worked and will require retro-fitting to the interface.
IMOF team








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
16-Mar-2007
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


Mary Welch


Prasanth Dukaram

David Onyett


John Cowper


















	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 16 of  NUMPAGES 19	Date:  SAVEDATE \@ "d MMM yyyy" 19 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































