		









`


TOM Integration
Interface Specification
On 
Store Reference Data
From IDS to GPM


[S074]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
17/04/2007
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1
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
17-04-2007
0.1D
Draft













Reviewers

Name
Date
Version
Position
Andrew Barker

















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



Document Source
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS036&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" DocShare: UK IT/TOM Integration/Shared Documents

Related Documents

Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.


Information Architecture Context diagram


Mapping spreadsheet
S074 Store Details from IDS to GPM Mapping Document.xls

Other Reference Documents

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc157846016 \h 6
1.1	Purpose of Document	 PAGEREF _Toc157846017 \h 6
1.2	Background	 PAGEREF _Toc157846018 \h 6
1.3	Scope	 PAGEREF _Toc157846019 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc157846020 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc157846021 \h 7
2.2	Architecture	 PAGEREF _Toc157846022 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc157846023 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc157846024 \h 9
3.1	Scope	 PAGEREF _Toc157846025 \h 9
3.2	Source Message Schema	 PAGEREF _Toc157846026 \h 9
3.3	Sample Message Format	 PAGEREF _Toc157846027 \h 9
3.4	Message Transport Details	 PAGEREF _Toc157846028 \h 9
3.5	Naming and Configuration	 PAGEREF _Toc157846029 \h 10
3.6	Environment and Security Context	 PAGEREF _Toc157846030 \h 10
3.7	Non-Functional Requirements	 PAGEREF _Toc157846031 \h 10
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc157846032 \h 11
4.1	Scope	 PAGEREF _Toc157846033 \h 11
4.2	Data Validation	 PAGEREF _Toc157846034 \h 11
4.3	Filtering	 PAGEREF _Toc157846035 \h 11
4.4	Mapping	 PAGEREF _Toc157846036 \h 11
4.5	Target Message Schema	 PAGEREF _Toc157846037 \h 11
4.6	Message Transport Details	 PAGEREF _Toc157846038 \h 12
4.7	Naming and Configuration	 PAGEREF _Toc157846039 \h 14
4.8	Environment and Security Context	 PAGEREF _Toc157846040 \h 14
4.9	Non-Functional Requirements	 PAGEREF _Toc157846041 \h 14
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc157846042 \h 15
5.1	Scope	 PAGEREF _Toc157846043 \h 15
5.2	Data Validation	 PAGEREF _Toc157846044 \h 15
5.3	Filtering	 PAGEREF _Toc157846045 \h 15
5.4	Mapping	 PAGEREF _Toc157846046 \h 15
5.5	Target Message Schema	 PAGEREF _Toc157846047 \h 15
5.6	Message Transport Details	 PAGEREF _Toc157846048 \h 15
5.7	Naming and Configuration	 PAGEREF _Toc157846049 \h 15
5.8	Environment and Security Context	 PAGEREF _Toc157846050 \h 15
5.9	Non-Functional Requirements	 PAGEREF _Toc157846051 \h 15
6	Testing Deliverables	 PAGEREF _Toc157846052 \h 16
7	Deployment	 PAGEREF _Toc157846053 \h 17
8	Assumptions and Outstanding Issues	 PAGEREF _Toc157846054 \h 18
8.1	Assumptions	 PAGEREF _Toc157846055 \h 18
8.2	Outstanding Issues	 PAGEREF _Toc157846056 \h 18
Appendix A Volumes	 PAGEREF _Toc157846057 \h 19
Appendix B Glossary	 PAGEREF _Toc157846058 \h 20
Appendix C Document Control	 PAGEREF _Toc157846059 \h 21

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Store reference data between the IDS and GPM Application. The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US implementation.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including IDS and GPM. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Store Reference data from IDS into GPM.
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
The interface is an extract of Store Reference Data from IDS using Common Forms and uploads into the GPM Holding Table using SSIS. The Upload is a full upload in nature.
Architecture
 EMBED Visio.Drawing.11  
Requirements for the End-to-End Interface
The interface is meant to run nightly at a pre-configured time, which on completion is expected to upload the Store reference data in a Store Holding Table in GPM.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI, and SSIS. At the time of writing (2007-04-17) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.
Non-Functional Requirements of the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from IDS using Common Forms, delivering the resulting data to GPM Store Holding Table before the identified cut-off time. The interface should run on scheduled batch basis. 
Reliability and Availability Requirements
The interface-run should be atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The successful delivery, failure in the creation of the extract, and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate. (Refer to 8.2 Outstanding Issues).
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration. 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope
This section describes the data sources required by this interface and the services used to access the data.
Source Message Schema
There is no source message as such. The source data resides in the form of RDBMS tables. The data is extracted via Location Common Form. 
Message Transport Details

Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
Windows 2003 Server

Source Physical Location
SQL SERVER 2005

Source Underlying Data Storage Technology
RDBMS

Target System Name
SSIS

Target Platform / OS


Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
SSIS       		
Common Forms                 

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







Processing required in the Messaging Stage of the interface
Scope
This section describes the discreet steps within the SSIS package to extract and format data. The target schema is included in this section
Package Overview
SSIS extracts the product reference data from IDS using Common Forms, nightly at predefined time.  In turn, the data is inserted into a Holding table in GPM Database which is the Store Holding Table.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Holding Table Field Name
Type
Length
Notes / Transformations
StoreId
Integer
4
This field will contain the store id of a store.
StoreFormat
Varchar
10
Description of type of store for e.g. Metro or PFS.
StoreSubnet
Varchar
20

ParentStoreID
Integer
4
This field will contain the store number of the store with which this store is mapped to e.g. a PFS is mapped to main store.
IL_TimeStamp
Datetime

TimeStamp to be used Internally by GPM Application

Message Transport Details 
For messages destined for GPM system, the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS


Source Physical Location


Source Underlying Data Storage Technology


Target System Name
GPM

Target Platform / OS
SQL Server 2005

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
RDBMS extract

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
Package Name: TOM.S074.IDStoGPM.StoreDetails.dtsx
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
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
Target Holding Table Details are not available. Data type and length of fields of destination table Store Holding Table are based on the core table tbl_Store.



Outstanding Issues
ID
Issue
To be addressed by
1
GPM Store Holding Table generation script to be provided. Using dummy Store holding table (name, datatypes and size based on tbl_Store core table in GPM) may result in rework if there are significant changes when final script issued from GPM.
GPM Team
2
Timings and cut-off constraints need to be defined. Require input from SRD. 
Space, Range, Display Solution Architects plus Information Architect
3
Deployment not yet considered
Information Architect
4
Alert numbers/identifiers are yet to be defined
Information Architect
5
The design of the IMOF is still being worked and will require retro-fitting to the interface
Information Architect
6
Specific IMOF event identifiers are yet to be defined
Information Architect


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
IDS
Information Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Store, etc. IDS's reside in the EIA Layer, and are accessed through the EAI Layer.
GPM
GroupProductMapping
SQL Server Database provided by Product mapping for loading Product details.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
17-Apr-2007
0.1D
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

John Cowper
Solution Architect

David Onyett
Project Lead




















	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 11 of  NUMPAGES 19	Date:  SAVEDATE \@ "d MMM yyyy" 5 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































