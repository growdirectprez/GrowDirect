		












TOM Integration

Interface Specification
Store reference data
From IDS to GFO


[J087]






Project BEN Code:
W60416
Author:Kapil ChadhaDate:
17/11/2006
Version:
1.1
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
Kapil Chadha
21-11-2006
0.1D
Draft
Sankar G
06-12-2006
0.2D
Base lined for development
Supriyo Chakraborty
28-02-2006
1.0
CR for incorporating Common Form Services for fetching data from IDS.
Sankar G
20-04-2007
1.1
CR for the following Defects
1930 – State code mapping to CHBCB-REGION-GROUP-NO
1869 – The filename is not correct

Reviewers

Name
Position
Adrian Hinks
Engagement Architect
James Keel

Tony Stains



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
J0087 - GFO Store Information Context Diagram -Location-Stores v3.vsd

Mapping spreadsheet
J0087 -StoreLocations to GFO Mappings v30.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc160615781 \h 6
1.1	Purpose of Document	 PAGEREF _Toc160615782 \h 6
1.2	Background	 PAGEREF _Toc160615783 \h 6
1.3	Scope	 PAGEREF _Toc160615784 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc160615785 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc160615786 \h 7
2.2	Architecture	 PAGEREF _Toc160615787 \h 7
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc160615788 \h 7
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc160615789 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc160615790 \h 9
3.1	Scope	 PAGEREF _Toc160615791 \h 9
3.2	Source Message Schema	 PAGEREF _Toc160615792 \h 9
3.3	Message Transport Details	 PAGEREF _Toc160615793 \h 9
3.4	Naming and Configuration	 PAGEREF _Toc160615794 \h 10
3.5	Environment and Security Context	 PAGEREF _Toc160615795 \h 10
3.6	Non-Functional Requirements	 PAGEREF _Toc160615796 \h 10
3.7	Environment and Security Context	 PAGEREF _Toc160615797 \h 11
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc160615798 \h 12
4.1	Scope	 PAGEREF _Toc160615799 \h 12
4.2	Processing Overview	 PAGEREF _Toc160615800 \h 12
4.3	Data Validation	 PAGEREF _Toc160615801 \h 12
4.4	Filtering	 PAGEREF _Toc160615802 \h 12
4.5	Mapping	 PAGEREF _Toc160615803 \h 12
4.6	Target Message Schema	 PAGEREF _Toc160615805 \h 12
4.7	Message Transport Details	 PAGEREF _Toc160615806 \h 14
4.8	RTI Configuration	 PAGEREF _Toc160615807 \h 15
4.9	Environment and Security Context	 PAGEREF _Toc160615808 \h 15
4.10	Non-Functional Requirements	 PAGEREF _Toc160615809 \h 15
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc160615810 \h 16
5.1	Scope	 PAGEREF _Toc160615811 \h 16
5.2	Data Validation	 PAGEREF _Toc160615812 \h 16
5.3	Filtering	 PAGEREF _Toc160615813 \h 16
5.4	Mapping	 PAGEREF _Toc160615814 \h 16
5.5	Target Message Schema	 PAGEREF _Toc160615815 \h 16
5.6	Message Transport Details	 PAGEREF _Toc160615816 \h 16
5.7	Environment and Security Context	 PAGEREF _Toc160615817 \h 16
6	Testing Deliverables	 PAGEREF _Toc160615818 \h 17
7	Deployment	 PAGEREF _Toc160615819 \h 18
8	Assumptions and Outstanding Issues	 PAGEREF _Toc160615820 \h 19
8.1	Assumptions	 PAGEREF _Toc160615821 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc160615822 \h 19
Appendix A Volumes	 PAGEREF _Toc160615823 \h 20
Appendix B Glossary	 PAGEREF _Toc160615824 \h 21
Appendix C Document Control	 PAGEREF _Toc160615825 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Store reference data between Integration Data Store (IDS) and Global Forecasting System (GFO).	
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORMS and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer business specific Store reference data from IDS into GFO systems.
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
The interface is a batch extract of Store Reference data from Integration Data Store and uploads into the GFO system via integration layer. 

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
A scheduled batch job/s runs, at a pre-configured time, to extract the Store Reference data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL server Integration Service packages and calls the common form associated with IDS. After executing the common form service, a complete unload of required data set will be returned as input for the SSIS package. 

The common form service fetches complete data that gets stored in the temporary storage. 

The final data-set gets transformed into the COBOL Copy book format which is specified in section 4.6 within SSIS package. This Batch job should generate the COBOL copy book file with temporary file name and rename the temporary file to the target named file name as per section 3.4, which is required for GFO.
Source Message Schema
In this context, the source being database tables, the source message is generated with the combination of data from the tables.

The data model diagram located at 
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fIDS%20data%20model&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fIDS%20data%20model&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d  
will provide necessary information to get the source data.

Common Forms
Service Name
Description
TOM.Common.Schema.Stores
This common form returns the all Stores Information from IDS including Store Address Details.
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
RDBMS data stream 	

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
Package Name: TOM.J087.IDStoGFO.StoreReference.dtsx
SSIS Procedure
Name
J087IDSGFOStoreReferenceUnload_sp
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
Environment and Security Context
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
The Store Reference data to be picked up from the IDS tables and populate in a COBOL format file. All Store Reference data is to be sent to GFO.

Method:
There are five entities involved in picking up the data. 

The Store Reference information is coming from Store Common From. From that Common Form only one entity is getting used for this interface. The name of the entity is: Store. For this extract, TOM.Common.Schema.Store common form is used. 

Mapping document will be provided subsequently.

Please refer the mapping spreadsheet at the following location: 
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ052%20Base%20Product%20details%20IL%20to%20GFO&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ052%20Base%20Product%20details%20IL%20to%20GFO&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d
Target Message Schema

Field NameReferenced in CR?Insync formatStartLengthCOBOL Format





CHBCA-INFO-HDR (group)
Needs to exist.
G
1
325
X(325)
CHBCA-REC-TYPE
Y
Z
1
1
9
Filler
Y
C
2
316
X(316)
CHBCA-MACH-DTE
Y
Z
318
8
9(8)






CHBCB-INFO-DET-REC (redef) (group)

G
1
325
X(325)
CHBCB-REC-TYPE
Y
Z
1
1
9
CHBCB-ORGANISATION-UNIT-NO
Y
Z
2
5
9(5)
CHBCB-INFO-DATA-GRP (group)

G
7
319
X(319)
CHBCB-PROPERTY-NO

Z
7
4
9(4)
CHBCB-ORG-UNIT-NAME
Y
C
11
21
X(21)
CHBCB-LINE1-ADDRESS

C
32
24
X(24)
CHBCB-LINE2-ADDRESS

C
56
24
X(24)
CHBCB-LINE3-ADDRESS

C
80
24
X(24)
CHBCB-LINE4-ADDRESS

C
104
24
X(24)
CHBCB-POST-CODE

C
128
12
X(12)
CHBCB-RETAIL-OUTLET-TYPE
Y
C
140
1
X
CHBCB-RO-PHONE-1-NO

C
141
17
X(17)
CHBCB-RO-TV-REG-NO (occurs 2)

C
158
2
XX
CHBCB-RO-NLSN-REG-NO

C
162
2
XX
CHBCB-DATE-OPENED
Y
C
164
8
X(8)
CHBCB-DATE-CLOSED
Y
C
172
8
X(8)
CHBCB-REFIT-DATE
Y
C
180
8
X(8)
CHBCB-ASSOCIATED-UNIT-NO(1)
Y
C
188
5
X(5)
CHBCB-ASSOCIATED-UNIT-NO(2)

C
193
5
X(5)
CHBCB-ASSOCIATED-UNIT-NO(3)

C
198
5
X(5)
CHBCB-SITE-LOCN-DESC-CDE

C
203
2
X(2)
CHBCB-OS-GRID-REF-NO-GRP (group)

G
205
5
X(5)
CHBCB-OS-GRID-REF-NO

PS
205
5
S9(4)V9(4) comp-3
CHBCB-OU-DAY-OP-SEG-GRP (group)  occurs 7

G
210
56
X(56)
CHBCB-OU-DLY-OPEN-TIME-GRP (group)

G
210
4
X(4)
CHBCB-DAILY-OPENING-HRS

C
210
2
XX
CHBCB-DAILY-OPENING-MINS

C
212
2
XX
CHBCB-OU-DLY-CLOSE-TIME-GRP (group)

G
214
4
X(4)
CHBCB-DAILY-CLOSING-HRS

C
214
2
XX
CHBCB-DAILY-CLOSING-MINS

C
216
2
XX
CHBCB-REGION-GROUP-NO-GRP
Y
G
266
3
XXX
CHBCB-REGION-GROUP-NO

Z
266
3
999
CHBCB-REGION-MD-INITS

C
269
3
XXX
CHBCB-REGION-EXEC-INITS

C
272
3
XXX
CHBCB-TRDG-STAT-CODE

C
275
1
X
CHBCB-SHELF-EDGE-LABEL-CD

C
276
1
X
CHBCB-MANAGERS-TITLE

C
277
4
X(4)
CHBCB-MANAGERS-INITIALS

C
281
3
XXX
CHBCB-MANAGERS-NAME

C
284
16
X(16)
CHBCB-COUNTY-CODE
Y
C
300
2
XX
CHBCB-CAR-PARK-SPACES-QTY

PS
302
3
S9(5) comp-3
CHBCB-CHECKOUTS-QTY

PS
305
2
S999 comp-3
CHBCB-REGION-CODE

C
307
1
X
CHBCB-COUNTRY-CODE
Y
C
308
1
X
CHBCB-RO-RNGE-CLASS

C
309
1
X
CHBCB-CPLUS-STORE-IND

C
310
1
X
CHBCB-METRO-STORE-IND
Y
C
311
1
X
CHBCB-RO-TYPE-CLASS
Y
C
312
2
XX
Filler

C
314
12
X(12)






CHBCZ-INFO-TRLR (redef) (group)
Needs to exist
G
1
325
X(325)
CHBCZ-REC-TYPE
Y
Z
1
1
9
Filler
Y
C
2
5
X(5)
CHBCZ-RECNT
Y
PS
7
3
S9(5) Comp-3
Filler
N
C
10
316
X(316)


Message Transport Details 

For messages destined for TO system, the following applies.

Feature
Specification
Additional Information
Source System Name
RTI

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
Kapil Chadha
21-11-2006
0.1D
First issue
Sankar G
06-12-2006
0.2D
Second issue
Supriyo Chakraborty
02-03-2007
1.0
Third issue
Sankar G
20-04-2007
1.1
CR for the following Defects
1930 – State code mapping to CHBCB-REGION-GROUP-NO
1869 – The filename is not correct



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



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT iii of  NUMPAGES 22	Date:  SAVEDATE \@ "d MMM yyyy" 20 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture




