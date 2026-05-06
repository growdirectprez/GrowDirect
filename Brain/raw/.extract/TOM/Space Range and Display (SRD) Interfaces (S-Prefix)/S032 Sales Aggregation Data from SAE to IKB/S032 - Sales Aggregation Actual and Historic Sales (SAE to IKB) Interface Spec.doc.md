		









`


TOM Integration
Interface Specification
On 
Sales Aggregation Data
From SAE to IKB


[S032]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
12/04/2007
Version:
0.2
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft
Modified By:
Nitin Singhai
Reviewed By:
Andrew Barker

Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
12-04-2007
0.1
Draft
Nitin Singhai
16-04-2007
0.2
Incorporated Review comments provided by Andrew Barker









Reviewers

Name
Position
Andrew Barker
Engagement Architect








At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Andrew Barker
Position
Engagement Architect
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



Document Source
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS036&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" DocShare: UK IT/TOM Integration/Shared Documents

Related Documents

A complete Interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.


Information Architecture Context diagram


Mapping spreadsheet
S032 - Sales Aggregation - Planogram (SAE to IKB) Mapping Specification
S032 - Sales Aggregation - Planogram Store (SAE to IKB) Mapping Specification
S032 - Sales Aggregation - Product - Planogram (SAE to IKB) Mapping Specification
S032 - Sales Aggregation - Product (SAE to IKB) Mapping Specification
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc164238677 \h 6
1.1	Purpose of Document	 PAGEREF _Toc164238678 \h 6
1.2	Background	 PAGEREF _Toc164238679 \h 6
1.3	Scope	 PAGEREF _Toc164238680 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc164238681 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc164238682 \h 7
2.2	Architecture	 PAGEREF _Toc164238683 \h 7
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc164238684 \h 7
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc164238685 \h 8
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc164238686 \h 9
3.1	Scope	 PAGEREF _Toc164238687 \h 9
3.2	Source Message Schema	 PAGEREF _Toc164238688 \h 9
3.3	Message Transport Details	 PAGEREF _Toc164238689 \h 11
4	Processing Required in the SSIS Stage of the Interface	 PAGEREF _Toc164238690 \h 11
4.1	Scope	 PAGEREF _Toc164238691 \h 11
4.2	Package Overview	 PAGEREF _Toc164238692 \h 11
4.3	Data Validation	 PAGEREF _Toc164238693 \h 12
4.4	Filtering	 PAGEREF _Toc164238694 \h 12
4.5	Mapping	 PAGEREF _Toc164238695 \h 12
4.6	Target Message Schema	 PAGEREF _Toc164238696 \h 12
4.7	Message Transport Details	 PAGEREF _Toc164238697 \h 13
4.8	Naming and Configuration	 PAGEREF _Toc164238698 \h 13
4.9	Environment and Security Context	 PAGEREF _Toc164238699 \h 14
4.10	Non-Functional Requirements	 PAGEREF _Toc164238700 \h 14
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc164238701 \h 15
5.1	Scope	 PAGEREF _Toc164238702 \h 15
5.2	Data Validation	 PAGEREF _Toc164238703 \h 15
5.3	Filtering	 PAGEREF _Toc164238704 \h 15
5.4	Mapping	 PAGEREF _Toc164238705 \h 15
5.5	Target Message Schema	 PAGEREF _Toc164238706 \h 15
5.6	Message Transport Details	 PAGEREF _Toc164238707 \h 15
5.7	Naming and Configuration	 PAGEREF _Toc164238708 \h 15
5.8	Environment and Security Context	 PAGEREF _Toc164238709 \h 15
5.9	Non-Functional Requirements	 PAGEREF _Toc164238710 \h 15
6	Testing Deliverables	 PAGEREF _Toc164238711 \h 16
7	Deployment	 PAGEREF _Toc164238712 \h 17
8	Assumptions and Outstanding Issues	 PAGEREF _Toc164238713 \h 18
8.1	Assumptions	 PAGEREF _Toc164238714 \h 18
8.2	Outstanding Issues	 PAGEREF _Toc164238715 \h 18
Appendix A Volumes	 PAGEREF _Toc164238716 \h 19
Appendix B Glossary	 PAGEREF _Toc164238717 \h 20
Appendix C Document Control	 PAGEREF _Toc164238718 \h 21

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Sales Aggregation data between the Sales Aggregation Engine (SAE) and JDA Intactix Knowledge Base (IKB). The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US and Turkey implementation.

Background
In Tesco Operating Model program, there is requirement to bridge the functionalities of SAE and IKB to feed aggregated financial performance data about products, planograms, floorplans and stores.  The Historic and the actual data are captured in the past for current products, planograms, floorplans and stores.  The principle business requirement for this type of data in IKB is for use when merchandisers analyse stock fill against inventory targets in pro/space.  This data can also be used for reporting purposes in the core JDA products.

To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed for product mapping.
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
This interface gets the Aggregated Historic and Actual Sales from SAE in the form of the 4 flat files. The files in turn are placed into a shared Network location. The Upload is a delta upload in nature. It is application’s responsibility to provide the deltas to integration layer.

The batch extract would initiate the SQL Server Integration service package.  The SSIS package processes the flat file and inserts the data into the holding tables of IKB. 
Architecture
 EMBED Visio.Drawing.11  

Requirements of the End-to-End Interface
The interface will run on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from flat files (4 in nos.) placed at SAE file share location and inserts into the corresponding Target IKB Holding Table. The 4 flat files represent the Historical and Actual Sales Data for Product-Planogram, Planogram, Planogram-Store and Product respectively.

The interface should transfer the Sales Aggregation Data from SAE file share to corresponding IKB Holding Table as soon as the source file is available. It is the Target Application’s responsibility to process from the Shadow Table to core table when it wants.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI and SSIS. At the time of writing (2007-04-12) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface
 
Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from the flat files (4 in nos. Identified by their name, placed at SAE File Share Location) through SSIS Service layer, Inserting the resulting data into the corresponding IKB Holding Tables. The Interface should run as soon as the source file is available. 
Reliability and Availability Requirements
The interface-run should be atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties (TBD).
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The successful delivery, failure in the creation of the extract, and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate. (Refer to 8.3 Outstanding Issues).
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
 
Source Message Schema
The data for this interface resides in the form of 4 flat files in the SRD SAE file Share. 

Product-Planogram Sales Data: 
File Name: yyyymmdd_IKB_SalesDataForProductPerPlanogram_yyyymmdd_hhmmss.txt

Field Name
String
Length
Starting Position
Notes
Header Record




RR
CHAR
2
1
Header record, always 00
YYYYMMDDhhmmss
CHAR
14
3
Date/Time file created
YYYYMMDD
CHAR
8
17
Date for which the data is processed
FILLER
CHAR
41
25
SPACES
Detail Record




RR
CHAR
2
1
Data record, always 01
Product ID
INTEGER
9
3
Product Number
Planogram ID
VARCHAR
6
12
Planogram Number
Actual Sales
Decimal 
12
18
Actual Sales
Actual Volume
Decimal
12
30
Actual Volume
Historical Sales
Decimal
12
42
Historical Sales
Historical Volume
Decimal
12
54
Historical Volume
Trailer Record




RR
CHAR
2
1
Footer record, always 99
CCCCCCCCCC
Integer
10
3
Record count, 9999999999
FILLER
CHAR
53
13
SPACES

Planogram Sales Data:
File Name: yyyymmdd_IKB_SalesDataForPlanogram_yyyymmdd_hhmmss.txt

Field Name
String
Length
Starting Position
Notes
Header Record




RR
CHAR
2
1
Header record, always 00
YYYYMMDDhhmmss
CHAR
14
3
Date/Time file created
YYYYMMDD
CHAR
8
17
Date for which the data is processed
FILLER
CHAR
32
25
SPACES
Detail Record




RR
CHAR
2
1
Data record, always 01
Planogram ID
VARCHAR
6
3
Planogram Number
Actual Sales
Decimal 
12
9
Actual Sales
Actual Volume
Decimal
12
21
Actual Volume
Historical Sales
Decimal
12
33
Historical Sales
Historical Volume
Decimal
12
45
Historical Volume
Trailer Record




RR
CHAR
2
1
Footer record, always 99
CCCCCCCCCC
Integer
10
3
Record count, 9999999999
FILLER
CHAR
44
13
SPACES

Planogram-Store Sales Data
File Name: yyyymmdd_IKB_SalesDataForPlanogramPerStore_yyyymmdd_hhmmss.txt

Field Name
String
Length
Starting Position
Notes
Header Record




RR
CHAR
2
1
Header record, always 00
YYYYMMDDhhmmss
CHAR
14
3
Date/Time file created
YYYYMMDD
CHAR
8
17
Date for which the data is processed
FILLER
CHAR
37
25
SPACES
Detail Record




RR
CHAR
2
1
Data record, always 01
Planogram ID
VARCHAR
6
3
Planogram Number
Store ID
Integer
5
9
Store Number
Actual Sales
Decimal 
12
14
Actual Sales
Actual Volume
Decimal
12
26
Actual Volume
Historical Sales
Decimal
12
38
Historical Sales
Historical Volume
Decimal
12
50
Historical Volume
Trailer Record




RR
CHAR
2
1
Footer record, always 99
CCCCCCCCCC
Integer
10
3
Record count, 9999999999
FILLER
CHAR
68
13
SPACES

Product Sales Data
File Name: yyyymmdd_IKB_SalesDataForProduct_yyyymmdd_hhmmss.txt

Field Name
String
Length
Starting Position
Notes
Header Record




RR
CHAR
2
1
Header record, always 00
YYYYMMDDhhmmss
CHAR
14
3
Date/Time file created
YYYYMMDD
CHAR
8
17
Date for which the data is processed
FILLER
CHAR
35
25
SPACES
Detail Record




RR
CHAR
2
1
Data record, always 01
Product ID
INTEGER
9
3
Planogram Number
Actual Sales
Decimal 
12
12
Actual Sales
Actual Volume
Decimal
12
24
Actual Volume
Historical Sales
Decimal
12
36
Historical Sales
Historical Volume
Decimal
12
48
Historical Volume
Trailer Record




RR
CHAR
2
1
Footer record, always 99
CCCCCCCCCC
Integer
10
3
Record count, 9999999999
FILLER
CHAR
47
13
SPACES

Message Transport Details

Feature
Specification
Additional Information
Source System Name
SAE

Source Platform / OS
Windows 2003 Server

Source Physical Location
File Share

Source Underlying Data Storage Technology
TBD

Target System Name
SSIS

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
SSIS	                             

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
Not yet decided

Archiving
There is no requirement to archive the messages.

Logging
Log via the Operational Framework.

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Processing Required in the SSIS Stage of the Interface
Scope
This section describes the discrete steps within the SSIS package to extract and format data. The target IKB Holding Tables format is included in this section. This segment will process the data extracted from flat files and transform into needed IKB Holding Table format.
Package Overview
SSIS extracts the data from flat file. In turn, the data is transformed into IKB Holding Table format.
Data Validation
N/A.
Filtering
There is no filtering requirement.
Mapping
Mapping document are available in docshare. Please see Page iii for more details.
Target Message Schema
csg_product_pog_performance_data 
Note: This Holding table corresponds to the Source file: yyyymmdd_IKB_SalesDataForProductPerPlanogram_yyyymmdd_hhmmss.txt

Holding Table Field Name
Type
Length
Description
Product_ID
Varchar
16
Product ID
Planogram_ID
Varchar
16
Planogram ID
Actual_Sales
Decimal
12,2
Actual Sales
Actual_Volume
Decimal
12,2
Actual Volume
Historical_Sales
Decimal
12,2
Historical Sales
Historical_Volume
Decimal
12,2
Historical Volume

csg_planogram_performance_data
Note: This Holding table corresponds to the Source file: yyyymmdd_IKB_SalesDataForPlanogram_yyyymmdd_hhmmss.txt

Holding Table Field Name
Type
Length
Description
Planogram_ID
Varchar
16
Planogram ID
Actual_Sales
Decimal
12,2
Actual Sales
Actual_Volume
Decimal
12,2
Actual Volume
Historical_Sales
Decimal
12,2
Historical Sales
Historical_Volume
Decimal
12,2
Historical Volume

csg_pog_store_performance_data
Note: This Holding table corresponds to the Source file: yyyymmdd_IKB_SalesDataForPlanogramPerStore_yyyymmdd_hhmmss.txt

Holding Table Field Name
Type
Length
Description
Planogram_ID
Varchar
16
Planogram ID
Store_No
Varchar
32
Store Number
Actual_Sales
Decimal
12,2
Actual Sales
Actual_Volume
Decimal
12,2
Actual Volume
Historical_Sales
Decimal
12,2
Historical Sales
Historical_Volume
Decimal
12,2
Historical Volume

csg_product_performance_data
Note: This Holding table corresponds to the  Source file: yyyymmdd_IKB_SalesDataForProduct_yyyymmdd_hhmmss.txt


Holding Table Field Name
Type
Length
Description
Product_ID
Varchar
16
Product ID
Actual_Sales
Decimal
12,2
Actual Sales
Actual_Volume
Decimal
12,2
Actual Volume
Historical_Sales
Decimal
12,2
Historical Sales
Historical_Volume
Decimal
12,2
Historical Volume

Message Transport Details 
For messages destined for IKB system, the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
Windows 2003 Server

Source Physical Location


Source Underlying Data Storage Technology


Target System Name
IKB

Target Platform / OS


Target Physical Location
RDBMS

Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter	                             
SSIS                                                  

Data Format

XML  				
Delimited 			
Positional 			
RDBMS                                            

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
N/A

Logging
Log via the Operational Framework.

Error Handling
Not yet decided


 
Naming and Configuration
SSIS
Package Name: TOM.S032.SAEtoIKB.SalesAggregationData.dtsx

Name

<Placeholder for other package components/steps>


<Placeholder for other package components/steps>





Environment and Security Context
Account details will be included here once we have visibility of the environments. 

Non-Functional Requirements
On successful delivery of the data to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure of transformation of data should be written to the failed log database, and an alert should be raised.






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
This section should contain a list of discrete deliverables. The following table is an illustrative template only. The exact deliverables will depend on the technologies employed in the interface. 

Deliverable
Description
TBD <stored proc name>

TBD <stored proc name>

TBD <service name>

TBD <SSIS package name> 
Package 
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
IKB table scripts are not yet available. Taking the field names, length and datatypes from a JDA Draft document for the Table layouts.
2
Source Files format from Sales Aggregation Engine to IKB are not defined. File layout prepared on assumption that it will be similar to the table definition mentioned in SAE TSD.

Outstanding Issues
ID
Issue
To be addressed by
1
JDA Technical Contact needs to be confirmed.
JDA
2
Timing requirements of interface not established.
SAE / JDA Team
3
Understand impact of non-delivery of the file.
SAE / JDA Team
4
The design of the IMOF is still being worked and will require retro-fitting to the interface.
IMOF team
5
Alert numbers/identifiers are yet to be defined.
TOM Solution Architects
6
Field definitions (datatype, size) for IKB tables is not yet defined. If the field definitions differ than what is currently assumed, then it may result in rework.
JDA


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
IKB
Intactix Knowledge Base
SQL Server Database provided by JDA Intactix to maintain Space Planning and Floor Planning data.
IMOF
Integration Management Operational Framework
IMOF is a framework which is pluggable to any BizTalk, RTI and SSIS for alerting, exception handling, defining rules, scheduling etc
SAE
Sales Aggregation Engine
SAE Holds the sales data, and present it to the SRD systems for summarisation across a cluster of stores (or all stores), a (display) group of products, and one or more weeks, up to 2 years of history.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
12-Apr-2007
0.1
Draft
Nitin Singhai
16-Apr-2007
0.2
Incorporated Review comments provided by Andrew Barker











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
Enterprise Architect

Andrew Barker
Solution Architect

Welch Mary
SRD Manager TOM Integration

























	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT ii of  NUMPAGES 21	Date:  SAVEDATE \@ "d MMM yyyy" 16 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































