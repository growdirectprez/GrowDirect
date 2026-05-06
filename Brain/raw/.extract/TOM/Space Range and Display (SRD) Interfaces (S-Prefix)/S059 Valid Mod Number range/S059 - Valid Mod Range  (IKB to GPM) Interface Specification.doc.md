		









`


TOM Integration
Interface Specification
On 
Valid Mod Number Range
From IKB to GPM


[S059]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
08/03/2007
Version:
0.1D
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft
Modified By:

Reviewed By:


Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
08-03-2007
0.1
Draft













Reviewers

Name
Position
Andrew Barker
Solution Architect








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

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.


Information Architecture Context diagram


Mapping spreadsheet
S059 - Valid Mod Range (IKB to GPM) Mapping Specification
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc161116255 \h 6
1.1	Purpose of Document	 PAGEREF _Toc161116256 \h 6
1.2	Background	 PAGEREF _Toc161116257 \h 6
1.3	Scope	 PAGEREF _Toc161116258 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc161116259 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc161116260 \h 7
2.2	Architecture	 PAGEREF _Toc161116261 \h 7
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc161116262 \h 7
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc161116263 \h 8
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc161116264 \h 9
3.1	Scope	 PAGEREF _Toc161116265 \h 9
3.2	Source Message Schema	 PAGEREF _Toc161116266 \h 9
3.3	Message Transport Details	 PAGEREF _Toc161116267 \h 9
4	Processing Required in the SSIS Stage of the Interface	 PAGEREF _Toc161116268 \h 10
4.1	Scope	 PAGEREF _Toc161116269 \h 10
4.2	Package Overview	 PAGEREF _Toc161116270 \h 10
4.3	Data Validation	 PAGEREF _Toc161116271 \h 10
4.4	Filtering	 PAGEREF _Toc161116272 \h 10
4.5	Mapping	 PAGEREF _Toc161116273 \h 10
4.6	Target Message Schema	 PAGEREF _Toc161116274 \h 10
4.7	Message Transport Details	 PAGEREF _Toc161116275 \h 11
4.8	Naming and Configuration	 PAGEREF _Toc161116276 \h 11
4.9	Environment and Security Context	 PAGEREF _Toc161116277 \h 12
4.10	Non-Functional Requirements	 PAGEREF _Toc161116278 \h 12
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc161116279 \h 13
5.1	Scope	 PAGEREF _Toc161116280 \h 13
5.2	Data Validation	 PAGEREF _Toc161116281 \h 13
5.3	Filtering	 PAGEREF _Toc161116282 \h 13
5.4	Mapping	 PAGEREF _Toc161116283 \h 13
5.5	Target Message Schema	 PAGEREF _Toc161116284 \h 13
5.6	Message Transport Details	 PAGEREF _Toc161116285 \h 13
5.7	Naming and Configuration	 PAGEREF _Toc161116286 \h 13
5.8	Environment and Security Context	 PAGEREF _Toc161116287 \h 13
5.9	Non-Functional Requirements	 PAGEREF _Toc161116288 \h 13
6	Testing Deliverables	 PAGEREF _Toc161116289 \h 14
7	Deployment	 PAGEREF _Toc161116290 \h 15
8	Assumptions and Outstanding Issues	 PAGEREF _Toc161116291 \h 16
8.1	Assumptions	 PAGEREF _Toc161116292 \h 16
8.2	Outstanding Issues	 PAGEREF _Toc161116293 \h 16
Appendix A Volumes	 PAGEREF _Toc161116294 \h 17
Appendix B Glossary	 PAGEREF _Toc161116295 \h 18
Appendix C Document Control	 PAGEREF _Toc161116296 \h 19

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Valid Mod Range in a Store between the IKB and GPM. The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US and Turkey implementation.

Background
As part of the process of managing Space, Range and Display activities in store it is important to identify that the store has accurately completed all space range and display activities. This will help the centre to understand how well stores are conforming to the planograms. This interface provides the Valid Mod Range that exists in a Store.
In Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including IKB and GPM. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed for product mapping.
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
This interface extracts valid Mod range details from IKB using a SQL Server Connection and uploads into the Group Product Mapping (GPM) Holding Table using SSIS. The Upload is a full upload in nature.
Architecture
 EMBED Visio.Drawing.11  

Requirements of the End-to-End Interface
The interface will run on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IKB, and formats it into the target Table format.

The interface should transfer the data for Valid Mod Range from IKB to GPM holding table at a pre-configured time (to be determined).  After successful completion, another GPM process would then upload the Valid Mod Range data to the core tables of GPM.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI and SSIS. At the time of writing (2007-03-08) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface
 
Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from IKB through SSIS Service layer using SQL Stored Procedure, delivering the resulting data to Holding Table (name TBD) before the identified cut-off time. The interface should run on scheduled batch basis. 
Reliability and Availability Requirements
The interface-run should be non atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties (TBD).
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
The data for this interface resides in the IKB in a holding table. 

Holding Table Field Name
Type
Length
Description
Store_No
varchar
32
Store Number
Module_number
varchar
32
Module Number in Store
IL_Time_stamp
Datetime

Integration layer set to todays datetimstamp when all records fetched successfully.
Message Transport Details

Feature
Specification
Additional Information
Source System Name
IKB

Source Platform / OS
Windows 2003 Server

Source Physical Location
SQL SERVER 2005

Source Underlying Data Storage Technology
RDBMS

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
File Drop(Windows) 	
                 (XCOM) 	
SSIS                                    

Data Format.
XML			
Delimited		
Positional		
RDBMS       		                     

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
This section describes the discrete steps within the SSIS package to extract and format data. The target schema is included in this section. This segment will process the data picked from IKB database and transform into needed format which is required by GPM holding table. After processing, transformed data will get loaded into GPM holding table (name of the holding table to be determined). In turn the holding table data will get loaded into tbl_ModDetails in GPM database.
Package Overview
SSIS extracts the Valid Mod Range data from IKB via SQL Server OLEDB connection, at a predefined time.  In turn, the data is inserted into an Intermediate table at GPM.
Data Validation
N/A.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Holding Table Field Name
Type
Length
Mandatory
Description
ModNumber
Integer

Yes
This field will contain   mod number displayed on the mod label.
StoreID
Integer

Yes
This field contains the ID of the Store. Foreign key referencing tbl_Store(StoreID)
InsertDate
datetime

Yes
SysDate()

Message Transport Details 
For messages destined for GPM system, the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
Windows 2003 Server

Source Physical Location
SQL Server 2005 database

Source Underlying Data Storage Technology
RDBMS
	

Target System Name
GPM

Target Platform / OS
SQL Server

Target Physical Location


Target Underlying Data Storage Technology


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
Package Name: TOM.S059.IKBtoGPM.ValidModRange.dtsx

Name
S059_GetValidModRange_usp.sql
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
Stored Procedure
TBD <stored proc name>
Stored Procedure
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
Since the Holding table details are not available, Data type and length of fields of destination table GPM Holding Table are based on tbl_ModDetails.

Outstanding Issues
ID
Issue
To be addressed by
1
ModDetails Holding Table generation script to be provided by GPM. Using the details for a Holding table (name, datatypes and size based on tbl_ModDetails table) may result in rework if there are significant changes when final script issued from GPM
GPM
2
Timings and cut-off constraints need to be defined. Require input from GPM
Product Mapping Solution Architects plus Information Architect.
3
Alert numbers/identifiers are yet to be defined
Solution Architect
4
The design of the IMOF is still being worked and will require retro-fitting to the interface.
IMOF team
5
Complete Structure of the IKB holding table is not decided
JDA Team
6
Maintenance mechanism of IKB holding table to be decided
Solution Architect
7
Time window for updating the IKB holding table to be decided
JDA Team


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
SQL Server Database provided by Product mapping for loading Product details.
IKB
Intactix Knowledge Base
SQL Server Database provided by JDA Intactix to maintain Space Planning and Floor Planning data.
IMOF
Integration Management Operational Framework
IMOF is a framework which is pluggable to any Biztalk, RTI and SSIS for alerting, exception handling, defining rules, scheduling etc

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
08-Mar-2007
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
Enterprise Architect

Andrew Barker
Solution Architect

Welch Mary
SRD Manager TOM Integration

























	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.1 REF DOC_VER , Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 9 of  NUMPAGES 19	Date:  SAVEDATE \@ "d MMM yyyy" 23 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































