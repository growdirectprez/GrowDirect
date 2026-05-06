		












TOM Integration

Interface Specification
Item-Region data
From IDS to GFO


[J0052]






Project BEN Code:
W60416
Author:Nitin SinghaiDate:
07/12/2006
Version:
1.2
Status:

Modified By:
Sankar G
Reviewed By:
Adrian Hinks
Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
17/12/2006
0.1
Draft
Supriyo Chakraborty
20/12/2007
0.2
Draft
Sankar G
22/12/2007
1.0
Base lined for development
Supriyo Chakraborty
28/02/2007
1.1
CR for populating additional fields in the interface which are subsequently added in IDS
Sankar G
19/04/2006
1.2
CR raised for the following defects
1833 - No Section attributes available in IDS. Pickup Section ID from different source
1932 -  File should only contain one pack size per product
1869 - Output File Name incorrect
Mapping document is changed.

Reviewers

Name
Position
Adrian Hinks
Engagement Architect
Tony Stains

James Keel



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
Laurence Tang

<Version No>
Tony Stains


Rob McDonagh


David Onyett



Document Source
HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ100%20Item%2dWarehouse%2dSupplier%20Data%20%28IDS%20to%20GFO%29&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d"DocShare: UK IT/TOM Integration/Shared Documents

Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.

Information Architecture Context diagram
J0052 - Information Context Diagram -Item-region v13.vsd

Mapping spreadsheet
J0052 - Item-Region to GFO Mappings v3.0.xls


Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc164843937 \h 5
1.1	Purpose of Document	 PAGEREF _Toc164843938 \h 5
1.2	Background	 PAGEREF _Toc164843939 \h 5
1.3	Scope	 PAGEREF _Toc164843940 \h 5
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc164843941 \h 6
2.1	Description of the End-to-End Interface	 PAGEREF _Toc164843942 \h 6
2.2	Architecture	 PAGEREF _Toc164843943 \h 6
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc164843944 \h 6
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc164843945 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc164843946 \h 8
3.1	Scope	 PAGEREF _Toc164843947 \h 8
3.2	Source Message Schema	 PAGEREF _Toc164843948 \h 8
3.3	Message Transport Details	 PAGEREF _Toc164843949 \h 8
3.4	Naming and Configuration	 PAGEREF _Toc164843950 \h 9
3.5	Environment and Security Context	 PAGEREF _Toc164843951 \h 9
3.6	Non-Functional Requirements	 PAGEREF _Toc164843952 \h 10
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc164843953 \h 11
4.1	Scope	 PAGEREF _Toc164843954 \h 11
4.2	Processing Overview	 PAGEREF _Toc164843955 \h 11
4.3	Data Validation	 PAGEREF _Toc164843956 \h 11
4.4	Filtering	 PAGEREF _Toc164843957 \h 11
4.5	Mapping	 PAGEREF _Toc164843958 \h 11
4.6	Target Message Schema	 PAGEREF _Toc164843959 \h 12
4.7	Message Transport Details	 PAGEREF _Toc164843960 \h 13
4.8	RTI Configuration	 PAGEREF _Toc164843961 \h 13
4.9	Environment and Security Context	 PAGEREF _Toc164843962 \h 14
4.10	Non-Functional Requirements	 PAGEREF _Toc164843963 \h 14
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc164843964 \h 15
5.1	Scope	 PAGEREF _Toc164843965 \h 15
5.2	Data Validation	 PAGEREF _Toc164843966 \h 15
5.3	Filtering	 PAGEREF _Toc164843967 \h 15
5.4	Mapping	 PAGEREF _Toc164843968 \h 15
5.5	Target Message Schema	 PAGEREF _Toc164843969 \h 15
5.6	Message Transport Details	 PAGEREF _Toc164843970 \h 15
5.7	Environment and Security Context	 PAGEREF _Toc164843971 \h 15
6	Testing Deliverables	 PAGEREF _Toc164843972 \h 16
7	Deployment	 PAGEREF _Toc164843973 \h 17
8	Assumptions and Outstanding Issues	 PAGEREF _Toc164843974 \h 18
8.1	Assumptions	 PAGEREF _Toc164843975 \h 18
8.2	Outstanding Issues	 PAGEREF _Toc164843976 \h 18
Appendix A Volumes	 PAGEREF _Toc164843977 \h 19
Appendix B Glossary	 PAGEREF _Toc164843978 \h 20
Appendix C Document Control	 PAGEREF _Toc164843979 \h 21

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Item -Region data between Integration Data Store (IDS) and Global Forecasting System (GFO).	

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is common for both US and Turkey.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORMS and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer business specific Item -Region data from IDS into GFO systems.
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
The interface is a batch extract of Item-Region data from an Integration Data Store and upload into the GFO system via integration layer. 
The interface is meant to run at a pre-configured time, which on completion is expected to produce a flat-file (containing reference data records) onto the shared location. This shared location would be monitored by GFO system during specific hours. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into GFO.
Architecture

Requirements of the End-to-End Interface
The interface will run once a day, on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IDS through common forms, and transforms and formats it into the target file. The file is delivered to GFO via RTI file adaptor, to a folder on the GFO host.

GFO requires a full refresh of data each day. 

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI, and SSIS. 

A single RTI instruction will be used to transfer the target file.

Non-Functional Requirements of the End-to-End Interface

Audit Requirements
Each and every interface run should be audited/logged for the purpose of traceability
Security Requirements
The interface executes within a secure private domain. No additional security considerations are required
Timing/Cut-off Constraints
As of now there is no such requirement, however this needs to be re-visited
Performance Requirements
The performance requirements, are unknown at this point of time
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
There is no such requirement
Operational Support Requirements
The due start time and due delivery time of this interface must be defined as IMOF events. These events will be monitored. Alerts will be generated should the interface fail to start, fail to deliver, or deliver late.
The details regarding restart/recovery will be provided after discussion with the GFO team.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration
Legal Requirements
There is no such requirement
Compliance To Standards Requirements
To be filled in !!
Processing required in an Extract-Stage of the interface
Scope
A scheduled batch job/s runs, at a pre-configured time, to extract the Item-Region data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL server Integration Service packages and calls the common forms associated with IDS. After executing the common form service, a complete unload of required data set will be returned as input for the SSIS package. 

The common form services fetch complete data that gets stored in the temporary storage. Another stored procedure at this time joins the data in the temporary storage, into the form required by the target message schema. This data gets stored in another temporary storage.

The final data-set gets transformed into the COBOL Copy book format which is specified in section 4.6 within SSIS package. This Batch job should generate the COBOL copy book file with temporary file name and rename the temporary file to the target named file name as per section 3.4, which is required for GFO.
Source Message Schema
In this context, the source being database tables, the source message is generated with the combination of data from the tables.
The data model diagram located at  HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fIDS%20data%20model&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fIDS%20data%20model&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d  will provide necessary information to get the source data.

Common Forms
Service Name
Description
TOM.Common.Schema.Items
This common form will return all the Item entity details with corresponding entities viz. TradePack, Style and Article information. 
Version of the common form is 1.0
TOM.Common.Schema.MerchandiseHierarchy
This common form will return Merchandise hierarchy stating from Division-> Department -> Section -> Class -> SubClass. 
Version of the common form is 1.0



Message Transport Details
Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
SQL Server

Source Physical Location


Source Underlying Data Storage Technology
RDBMS

Target System Name
RTI

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
Common Form Services 	
SSIS 					

Data Format.
XML			
Delimited		
Positional		
RDBMS data stream 	

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous		
Asynchronous		
Bulk Data		

Real-time/Scheduled Batch
Scheduled Batch

Archiving
There is no requirement to archive the messages.

Logging
Logging should occur, such that the message can be recreated if necessary.

Error Handling
On fail move the file to the failed transmissions location.

Naming and Configuration

SSIS
Package Name: TOM_IDSGFO_Item_Region_pkg
SSIS Procedure
Name
IDSGFOItemRegionUnload_sp
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Files and Folders
Local Folder
Name

Local File
Temporary Name

Name



Environment and Security Context
 
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example employing BizTalk this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).

 
To be determined once environments and user accounts are clarified

Non-Functional Requirements

This section should contain any non-functional requirements pertaining to this stage of the interface.







Processing required in the Messaging Stage of the interface
Scope
This section describes the process of delivering the file produced in the previous stage.
Processing Overview
A Real-Time Integrator Instruction is configured to monitor the local folder location for the arrival of the file and then delivers the file to the GFO folder location. If the file cannot be delivered to the GFO folder location the file will be delivered to the failed files location. The file should be written first with a temporary name, and be renamed once delivery is complete.
Data Validation
Data Validation will be done by the target GFO system.
Filtering
There is no filtering requirement.
Mapping
Pseudo code of the mapping specification

Objective:
The Item-Region data to be picked up from the IDS tables and populate in a COBOL format file. All SKU-Item data with the corresponding merchandise hierarchy data to be sent to GFO.

Method:
There are seven entities involved in picking up the data. 

The merchandise hierarchy is constituted of five entities namely: Division, Department, Section, Class and Subclass. For this extract, TOM.Common.Schema.MerchandiseHierarchy common form is used.

The item information is coming from Items hierarchy, In that hierarchy only SKUItem entity is getting used for this interface. For this extract TOM.Common.Schema.Items common form is used. 

There is a moving entity is getting used PackItemBreakout. This entity is not falling under any common model. So this entity will picked up directly from IDS data store. 

The merchandise hierarchy is linked with the SKUItem through Class, Subclass and Section elements. 
The PackItemBreakout is linked with the SKUItem through SKUID. 
Finally, these extracts will get merged and transformed.

Mapping document will be provided subsequently.

Please refer the spreadsheet at the following location:
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ052%20Base%20Product%20details%20IL%20to%20GFO&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ052%20Base%20Product%20details%20IL%20to%20GFO&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d

Target Message Schema
The source message is from Tables and gets converted into COBOL Copy Book format at the integration layer.

Field NameReferenced in CR?Insync formatStartLengthCOBOL Format





Header Record
(needs to exist)
G
1
170
 
JLBOA-REC-TYPE
Y
C 1
1
1
X
JLBOA-DATE
Y
C 10
2
10
X(10)
FILLER
N
C 159
12
159
X(159)
 
 
 
 
 
 
Detail Record
(needs to exist)
G
1
170
 
JLBOB-REC-TYPE
Y
C 1
1
1
X
JLBOB-BASE-PRODUCT-NO
Y
Z 9
2
9
9(9)
JLBOB-BPR-REGN
Y
C 2
11
2
X(2)
JLBOB-BASE-PROD-RNGE-CLASS
Y
C 2
13
2
X(2)
JLBOB-BPR-METRO-RCLASS
Y
C 2
15
2
X(2)
JLBOB-STORE-ORDERABLE-IND
Y
C 1
17
1
X
JLBOB-DEVELOPMENT-LINE
Y
C 1
18
1
X
JLBOB-DIAMOND-PROD-IND
Y
C 1
19
1
X
JLBOB-SRCE-TYPE-IND
Y
C 1
20
1
X
JLBOB-ORDER-GROUP
Y
C 2
21
2
X(2)
JLBOB-RMS-COMM-HIER
Y
G
23
20
 
JLBOB-RMS-DIVISION
Y
Z 4
23
4
9(4)
JLBOB-RMS-GROUP
Y
Z 4
27
4
9(4)
JLBOB-RMS-DEPT
Y
Z 4
31
4
9(4)
JLBOB-RMS-CLASS
Y
Z 4
35
4
9(4)
JLBOB-RMS-SUBCLASS
Y
Z 4
39
4
9(4)
JLBOB-BASE-PROD-DESCRIPTION
Y
C 48
43
48
X(48)
JLBOB-SELL-WT-ITEM-IND
Y
C 1
91
1
X
JLBOB-SALEABLE-EFF-DATE
Y
C 10
92
10
X(10)
JLBOB-S-B-W-UNIT-MEASURE
Y
C 4
102
4
X(4)
JLBOB-UNIT-SIZE      
Y
Z 5, 2
106
7
9(5)V99
JLBOB-LOW-LEVEL-GRP-CD
Y
C 2
113
2
X(2)
JLBOB-BASE-PROD-SEQ-NO
Y
C 3
115
3
X(3)
JLBOB-DGRP-CODE
Y
C 3
118
3
X(3)
JLBOB-MERCH-GRP-CODE
Y
C 3
121
3
X(3)
JLBOB-SUPP-MERCHG-GRP-CODE
Y
C 3
124
3
X(3)
JLBOB-MIN-SHELF-LIFE
Y
Z 3
127
3
9(3)
JLBOB-EXPCTD-SHELF-LIFE-1
Y
Z 3
130
3
9(3)
JLBOB-DELY-AVAILABLE-IND-1
Y
C 1
133
1
X
JLBOB-EXPCTD-SHELF-LIFE-2
Y
Z 3
134
3
9(3)
JLBOB-DELY-AVAILABLE-IND-2
Y
C 1
137
1
X
JLBOB-EXPCTD-SHELF-LIFE-3
Y
Z 3
138
3
9(3)
JLBOB-DELY-AVAILABLE-IND-3
Y
C 1
141
1
X
JLBOB-EXPCTD-SHELF-LIFE-4
Y
Z 3
142
3
9(3)
JLBOB-DELY-AVAILABLE-IND-4
Y
C 1
145
1
X
JLBOB-EXPCTD-SHELF-LIFE-5
Y
Z 3
146
3
9(3)
JLBOB-DELY-AVAILABLE-IND-5
Y
C 1
149
1
X
JLBOB-EXPCTD-SHELF-LIFE-6
Y
Z 3
150
3
9(3)
JLBOB-DELY-AVAILABLE-IND-6
Y
C 1
153
1
X
JLBOB-EXPCTD-SHELF-LIFE-7
Y
Z 3
154
3
9(3)
JLBOB-DELY-AVAILABLE-IND-7
Y
C 1
157
1
X
JLBOB-DIR-ORD-GRP
Y
C 2
158
2
X(2)
JLBOB-NOM-PACK-WEIGHT
Y
Z 3,2
160
5
9(3)V99
JLBOB-TU-NOTIONAL-WT
Y
Z 4,2
165
6
9(4)V99
 
 
 
 
 
 
Trailer Record
(needs to exist)
 
 
 
 
JLBOZ-REC-TYPE
Y
C 1
1
1
X
JLBOZ-REC-COUNT
Y
Z 8
2
8
9(8)
FILLER
N
C 161
10
161
X(161)

Message Transport Details
For messages destined for TO system, the following applies.

Feature
Specification
Additional Information
Source System Name
BizTalk

Source Platform / OS
Windows2003

Source Physical Location
Tba

Source Underlying Data Storage Technology
File System

Target System Name
GFO

Target Platform / OS
UNIX –AIX

Target Physical Location
Tba

Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI file adaptor			

Data Format

XML  				
Delimited 			
Positional 			

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous 			
Asynchronous 			
Bulk Data 			

Real-time/Scheduled Batch
Real-time

Archiving
There is no archiving requirement

Logging
Should logs be kept of all actions? For how long should these be stored?
Logging should occur, such that the message can be recreated if necessary.

Error Handling
If the message cannot be delivered, retry 6 times at 10 minute intervals, then raise alert.

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.



RTI Configuration
RTI
Instruction Name: TOM_IDSGFO_FileTransfer
Instruction Details
Description
To be determined
Enabled
Activate
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
4
Timeout
15
Require Data Send

Exception Management
Treat Fatal Adapter Exception As

Treat Unhandled Exceptions As


Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Account details will be included here once we have visibility of the environments.


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

On successful delivery of the file to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure the file should be written to the failed files location, and an alert should be raised.

 
Processing required in the <third stage of the interface>
Scope
Not Required

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

Environment and Security Context
Not Required
Testing Deliverables
Unit Test Scripts
Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
The messaging task will be started at EOD



Outstanding Issues
ID
Issue
To be addressed by
1
Alert numbers/identifiers are yet to be defined.
Engagement Architect
2
Security Context yet to be identified.  
Engagement Architect


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
HIS
Host Integration Server
A gateway to transferring data between a Mainframe system and another system.

Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.
ODS
Operation Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Customer, etc. ODS's reside in the EIA Layer, and are accessed through the EAI Layer.
TIB
Tesco Integration Bus
The managed service provided by Tesco's EAI Layer for data transportation and the integration of applications with legacy data sources and Operational Data Stores. 'Larger' in concept than the EAI Layer to include implementation details and interfacing between the EAI (integration services) Layer and the EIA (data services) Layer
WOF
Wintel Operational Framework
The Windows software/Intel hardware environment
->
One to Many Relationship
In a Subject hierarchy the entities defined as parent and child symbolize in this way.
<->
Many to Many Relationship
In a Subject hierarchy the relationship between the entities defined with many to many relationship without relationship table symbolize this way.
IMOF
Integration Management and Operations Framework
IMOF is based on MS.Net 3.0 rules engine, exists in parallel to the integration layer and gives Operational and Management frame work underpinning the Integration Service.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
06-12-2006
0.1D
First issue
Sankar G
07-12-2006
0.2D
Second Issue
Sankar G
22-12-2007
1.0
Third Issue
Supriyo Chakraborty
28-02-2007
1.1
CR for populating additional fields in the interface which are subsequently added in IDS
Sankar G
19-04-2007
1.2
CR raised for the following defects 
1833 - No Section attributes available in IDS. Pickup Section ID from different source
1932 -  File should only contain one pack size per product
1869 - Output File Name incorrect



Related Documents

Author	
Date
Version
Title


















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




















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 6 of  NUMPAGES 22	Date:  SAVEDATE \@ "d MMM yyyy" 19 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































