		









`


TOM Integration

Interface Specification
Location Hierarchy Data
From IDS to UDD


[J002]






Project BEN Code:
W60416
Author:Allister GreenDate:
26/01/2007
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.2 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:


Change Record

Author
Date
Version
Change Reference, description
Allister Green
26/01/2007
0.1
First Draft
Adrian Hinks
01/03/2007
0.2
Applying review changes









Reviewers

Name
Date
Version
Position
Adrian Hinks
01/03/2007
0.1
Integration Architect (GT&A)
Richard Durley


Enterprise Architect (GT&A)
James Keel


Solution Architect (GFO)






At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Laurence Tang (in lieu of Business Owner)
Position
GFO Business Analyst
Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version
Laurance Tang
<Issue Date>
<Version No>
James Keel


Richard Durley















Document Source

HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ002%20Location%20Hierarchy%20from%20IDS%20to%20UDD&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d"DocShare: UK IT/TOM Integration/Shared Documents



Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents:  


Information Architecture Context diagram
J002 to J010 - Information Architecture Context Diagram - UDD data load from GFO and IDS.vsd

Mapping spreadsheet
J002 -  Location Hierarchy from IDS to UDD - Mappings.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc160534663 \h 5
1.1	Purpose of Document	 PAGEREF _Toc160534664 \h 5
1.2	Background	 PAGEREF _Toc160534665 \h 5
1.3	Scope	 PAGEREF _Toc160534666 \h 5
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc160534667 \h 6
2.1	Description of the End-to-End Interface	 PAGEREF _Toc160534668 \h 6
2.2	Architecture	 PAGEREF _Toc160534669 \h 6
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc160534670 \h 6
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc160534671 \h 7
3	Processing required in the Integration Layer of the interface	 PAGEREF _Toc160534672 \h 8
3.1	Scope	 PAGEREF _Toc160534673 \h 8
3.2	Processing Overview	 PAGEREF _Toc160534674 \h 8
3.3	Source Message Schema	 PAGEREF _Toc160534675 \h 8
3.4	Data Validation	 PAGEREF _Toc160534676 \h 8
3.5	Filtering	 PAGEREF _Toc160534677 \h 8
3.6	Mapping	 PAGEREF _Toc160534678 \h 8
3.7	Target Message Schema	 PAGEREF _Toc160534679 \h 8
3.8	Message Format	 PAGEREF _Toc160534680 \h 10
3.9	Message Transport Details	 PAGEREF _Toc160534681 \h 11
3.10	Naming and Configuration	 PAGEREF _Toc160534682 \h 12
3.11	Environment and Security Context	 PAGEREF _Toc160534683 \h 13
3.12	Non-Functional Requirements	 PAGEREF _Toc160534684 \h 13
4	Deliverables	 PAGEREF _Toc160534685 \h 15
5	Deployment	 PAGEREF _Toc160534686 \h 16
6	Assumptions and Outstanding Issues	 PAGEREF _Toc160534687 \h 17
6.1	Assumptions	 PAGEREF _Toc160534688 \h 17
6.2	Outstanding Issues	 PAGEREF _Toc160534689 \h 17
Appendix A Volumes	 PAGEREF _Toc160534690 \h 18
Appendix B Glossary	 PAGEREF _Toc160534691 \h 19

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of 
Location Hierarchy Data from the IDS to the User Data Database (UDD) also within the Integration Layer (IL). This User Data is needed by the Allocations process.

The document is of a sufficiently technical nature to allow a developer to build an actual interface. This interface is for Turkey and US Day 1.

Background
An allocations process is needed to work with the Forecasting and Ordering system where the centre supply chain pushes stock into store. This can be for a variety of reasons but typical scenarios are: 
Allocation of a new product
Allocations to get ready for an event e.g. initial (additional) promotional stock
Allocation to initially fill a new store
Etc.

The main components of the allocations process are:
Overnight extract of data from GFO and IDS into the User Data Database (UDD) which is also located within the IDS
User creating allocations files manually using data from the UDD and an Excel template
The User uploading this allocations files into RMS, where they are validated
RMS generating and transferring allocations files to GFO via the Integration Layer


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
The interface is a batch extract of Location (Store) Hierarchy data from the Integration Data Store, and transport to the User Data Database upload directory.

The interface will make use of the audit and traceability components of IMOF (Integration Management and Operations Framework).

Architecture
Refer to Information Architecture Context Diagram. 

Requirements of the End-to-End Interface
Job TOM.J002.IDStoUDD.LocationHierarchy will be scheduled to run at 1AM. The job will run an SSIS package to:
Extract Location Hierarchy data from the ‘Store’ table within the IDS.
Create a comma delimited flat file (“IDS_Store_Hierarchy.csv”) containing the aggregated data, and place the file in a staging directory “IS_outbox” within the IL.

J002.IDStoUDD.LocationHierarchy

An RTI Shipping Agent Hosted Instruction “J002.IDStoUDD.LocationHierarchy” monitors the staging directory IS_outbox and manages the delivery of the file to the target application. Specifically, the instruction:
Identifies the Location Hierarchy file based on name: “J002_IDS_Store_Hierachy.csv”
Transports the file immediately upon receipt to the UDD upload directory (‘UD_inbox’).
Logs the successful file transfer using the Trackpoint component of IMOF. At time of writing, IMOF specifications have not yet been completed, hence details of how RTI or SSIS will record an event using the ‘Trackpoint’ component, or raise an error using the ‘Error Processing’ component, are to be determined.

Non-Functional Requirements of the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements. Start of job, completion, and delivery of file should be defined as IMOF Track Points.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
Needs to be completed by 2AM, when the UDD upload process will run.
Performance Requirements
The interface should be capable of extracting data from the IDS and delivering the resulting file to the UDD upload directory.
Reliability and Availability Requirements
The interface must be available at the scheduled extract time. Any outages scheduled should take into account the impact of this interface not running on time.
Scalability Requirements
N/A – the interface runs once a day and will support the anticipated number of locations in any implementation. 
Operational Support Requirements
The successful delivery, failure in the creation of the extract, and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate. (Refer to 6.2 Outstanding Issues).
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration. 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.

Processing required in the Integration Layer of the interface
Scope
This section covers the processing required to extract the Location Hierarchy data from IDS, creating flat file within staging directory, and transporting the file to the UDD upload directory.

Processing Overview
An SSIS package calls the Location Common Form Service to obtain a list of stores. For each store, a data record will be written to the staging output file J076_IDS_Store_Hierachy_staging.csv in the staging folder IS_outbox.. An RTI instruction monitors the IS_outbox folder for the arrival of the staging file. On arrival the file is transmitted to the UD_inbox folder. If the file cannot be delivered successfully by the RTI the file should be written to the failed files location - IS_outbound_failures. 
Source Message Schema
The Location Hierarchy data will be obtained by calling the Location Common Form Service. 


Common Forms
Service Name
Description
CF_GetLocationHierarchy
This service returns location common form containing all stores. The service is implemented as a stored procedure that returns xml. 


Data Validation
None
Filtering
There is no filtering requirement.
Mapping
Mapping between IDS “Store” table and the target flat file is shown in document ‘J002 -  Location Hierarchy from IDS to UDD - Mappings.xls Target Message Schema’

Target Message Schema
Comma delimited flat file, record terminated with LF (x0A)

Field Name
Description
Type
Format
Mandatory





Header Record




Type
Record type
Char(1)
“H” fixed value
Y
DateCreated
Date of extract from source system
Char(10)
CCYY-MM-DD
Y
TimeCreated
Time of extract from source system
Char(8)
HH:mm:ss
Y
RecordCount
No of Header and Detail records
Int

Y
 
 

 

Detail Record




Type
Record type
Char(1)
“D” fixed value
Y
StoreID
Store ID
Bigint

Y
StoreName
Store Name
Varchar(150)

Y
StoreOpenDate
Store open date
datetime
E.g “2007-01-29 12:43:21.000”
Y
StoreCloseDate
Store closed date
datetime
E.g “2007-01-29 12:43:21.000”

Can be empty.
N



Message Format
The source date is from a database table, and is converted to a comma delimited, flat file format.

The following message format is the target message format. 
Note: The data is dummy

H,2007-04-01,15:41:01.000,3
D,1004,Store1004,2007-02-01 00:00:00.000,2007-06-01 00:00:00.000
D,1006,Store1006,2007-02-01 00:00:00.000,
Message Transport Details 

Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
Windows Server 2003

Source Physical Location
(Local disk or SAN storage ? To be confirmed.)
IS_outbox
Source Underlying Data Storage Technology
SQL Server 2005

Target System Name
UDD

Target Platform / OS
Windows Server 2003

Target Physical Location
(Windows file share – local disk or SAN storage? (To be confirmed)
UD_Inbox
Target Underlying Data Storage Technology
SQL Server 2005

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		

Data Format

XML  				
Delimited 			
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
File delivery recorded by Trackpoint component of IMOF

Error Handling
Failure of data extract or file delivery raised through the ‘Error Processing’ component of IMOF.


Naming and Configuration
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

SSIS
Package Name: TOM.J002.IDStoUDD.LocationHierarchy.dtsx
SSIS Step
Name
Developer to populate in accordance with naming convention
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Files and Folders
Staging folder
Name
IS_outbox
Staging file
Name
J002_IDS_Store_Hierachy.csv
UDD upload folder
Name
UD_Inbox
UDD upload file
Name
IDS_Store_Hierachy.csv
Failed files folder 
Name
IS_outbound_failures


RTI
Instruction Name: TOM.J002.IDStoUDD.LocationHierarchy
Instruction Details
Description
File delivery of Location Hierarchy Data file from IDS to UDD
Enabled
True
Type
Hosted
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
1
Priority
Normal
Batch Size
1
Period
60
Retry Attempts
1
Timeout
10
Require Data Send
True
Exception Management
Treat Fatal Adapter Exception As
Fatal
Treat Unhandled Exceptions As
Fatal



Scheduling
Job
Name
TOM.J002.IDStoUDD.LocationHierarchy
Scheduling Agent
SQL Server Agent (MSSQLSERVER)
Scheduled Start Time
01.00 am
Expected Job Duration
2 minutes





IMOF
Track Points
Track Point ID

Error Tracking






Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Account details will be included here once we have visibility of the environments.


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Successful delivery of the Location Hierarchy file will be logged using the Trackpoint component of IMOF.

Failure of the extract from IDS, or the file transport to the UDD upload directory, will be raised through the error processing component of the IMOF framework.


Deliverables
Deliverable
Description
CF_GetLocationHierarchy
Location Common Form Service
TOM.J002.IDStoUDD.LocationHierarchy.dtsx
SSIS Package
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
TBD


Assumptions and Outstanding Issues
Assumptions
ID
Assumption





Outstanding Issues
ID
Issue
To be addressed by
1
Details of how IMOF framework integrates with RTI and SSIS (sections 2.2, 2.3)
IMOF specifications becoming available










Volumes

One file a day
Approximate File size ??
Glossary

Acronym
Term
Description
IDS
Integration Data Store
Data store within the Integration Layer
IL
Integration Layer
Enterprise layer for system integration
IMOF
Integration Management and Operational Framework
Audit and Traceability framework
SSIS
SQL Server Integration Services
A Microsoft tool for data integration
UDD
User Data Database
Database within the IL specifically to hold data needed by users creating the Allocations.










Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 12 of  NUMPAGES 20	Date:  SAVEDATE \@ "d MMM yyyy" 1 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



TODO:  Take a final decision on actual track points. 
Service has not been written yet.
Changed from IDS to IS. IS meaning Information  Services
To be confirmed
To be determined
To be determined
Need to estimate the file size.



























































