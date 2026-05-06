		









`


TOM Integration
Interface Specification
On 
Store 
Reference Data Update
From IDS to IKB


[S035]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
08/02/2007
Version:
0.2D
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
18-01-2007
0.1D
Draft
Nitin Singhai
07-03-2007
0.2D
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



Document Source
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS036&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" DocShare: UK IT/TOM Integration/Shared Documents






Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.

Information Architecture Context diagram
S035 Information Context Diagram – Store’s Update.vsd

Mapping spreadsheet
S035- Store Interface (IDS to IKB) Mappings

Other Reference Documents
Tesco - Stores' Update v1 2
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc161034103 \h 6
1.1	Purpose of Document	 PAGEREF _Toc161034104 \h 6
1.2	Background	 PAGEREF _Toc161034105 \h 6
1.3	Scope	 PAGEREF _Toc161034106 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc161034107 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc161034108 \h 7
2.2	Architecture	 PAGEREF _Toc161034109 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc161034110 \h 7
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc161034111 \h 8
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc161034112 \h 9
3.1	Scope	 PAGEREF _Toc161034113 \h 9
3.2	Source Message Schema	 PAGEREF _Toc161034114 \h 9
3.3	Message Transport Details	 PAGEREF _Toc161034115 \h 9
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc161034116 \h 10
4.1	Scope	 PAGEREF _Toc161034117 \h 10
4.2	Package Overview	 PAGEREF _Toc161034118 \h 10
4.3	Data Validation	 PAGEREF _Toc161034119 \h 10
4.4	Filtering	 PAGEREF _Toc161034120 \h 10
4.5	Mapping	 PAGEREF _Toc161034121 \h 10
4.6	Target Message Schema	 PAGEREF _Toc161034122 \h 10
4.7	Message Transport Details	 PAGEREF _Toc161034123 \h 11
4.8	Naming and Configuration	 PAGEREF _Toc161034124 \h 11
4.9	Environment and Security Context	 PAGEREF _Toc161034125 \h 12
4.10	Non-Functional Requirements	 PAGEREF _Toc161034126 \h 12
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc161034127 \h 13
5.1	Scope	 PAGEREF _Toc161034128 \h 13
5.2	Data Validation	 PAGEREF _Toc161034129 \h 13
5.3	Filtering	 PAGEREF _Toc161034130 \h 13
5.4	Mapping	 PAGEREF _Toc161034131 \h 13
5.5	Target Message Schema	 PAGEREF _Toc161034132 \h 13
5.6	Message Transport Details	 PAGEREF _Toc161034133 \h 13
5.7	Naming and Configuration	 PAGEREF _Toc161034134 \h 13
5.8	Environment and Security Context	 PAGEREF _Toc161034135 \h 13
5.9	Non-Functional Requirements	 PAGEREF _Toc161034136 \h 13
6	Testing Deliverables	 PAGEREF _Toc161034137 \h 14
7	Deployment	 PAGEREF _Toc161034138 \h 15
8	Assumptions and Outstanding Issues	 PAGEREF _Toc161034139 \h 16
8.1	Assumptions	 PAGEREF _Toc161034140 \h 16
8.2	Outstanding Issues	 PAGEREF _Toc161034141 \h 16
Appendix A Volumes	 PAGEREF _Toc161034142 \h 17
Appendix B Glossary	 PAGEREF _Toc161034143 \h 18
Appendix C Document Control	 PAGEREF _Toc161034144 \h 19

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Store reference data between the IDS to IKB. The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US implementation.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including IDS and IKB. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Store reference data from IDS into IKB.
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
The interface is a extract of Store Reference Data from IDS using Common Forms and uploads into the IKB Store Holding Table using SSIS. The Upload is a full upload in nature.

The interface is meant to run nightly at a pre-configured time, which on completion is expected to upload the Store data in a Store Holding Table in IKB.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 
Architecture
 EMBED Visio.Drawing.11  


Requirements for the End-to-End Interface
The interface will run once a day, on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IDS, and formats it into the target Table format. 

The interface is meant to run nightly at a pre-configured time 5 days a week (Tuesday to Saturday), which on completion is expected to upload the Store data in a Store Holding Table in IKB.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI, and SSIS. At the time of writing (2007-01-18) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.



Non-Functional Requirements of the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from IDS using Common Forms, delivering the resulting data to IKB Store Holding Table before the identified cut-off time. The interface should run on scheduled batch basis. 
Reliability and Availability Requirements
The interface-run should be non atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The successful delivery, failure in the creation of the extract, and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate. (Refer to 8.2 Outstanding Issues)
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
N/A 
Legal Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration.
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope

This section describes the data sources required by this interface and the services used to access the data.
Source Message Schema
The data for this interface resides in the IDS. Common Form Service cf_getstorehierarchy_usp is called by SQL Stored Procedure s035_getstoredetails_usp. The services are exposed as stored procedures and return row sets representing Store in the Location Common Form. 

Message Transport Details

Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
SQL SERVER 2005

Source Physical Location


Source Underlying Data Storage Technology
RDBMS

Target System Name
SSIS

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology
RDBMS

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
Common Forms  		

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
This section describes the discreet steps within the SSIS package to extract and format data. The target schema is included in this section. 
Package Overview
SSIS extracts the Store reference data from IDS using Common Forms, nightly at predefined time.  In turn, the data is inserted into an Intermediate table at IKB which is the Store Holding Table.
Data Validation
N/A
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Holding Table Field Name
Type
Length
Description
Datetime
Datetime
 
SystemGenerated
Store_number
Integer
 
Store Number 
Store_name
Varchar
50
Store Address
Rng_Attribute1
Varchar
50
Store Cluster Attribute
Rng_Attribute2
Varchar
50
Store Cluster Attribute
Rng_Attribute3
Varchar
50
Store Cluster Attribute
Rng_Attribute4
Varchar
50
Store Cluster Attribute
Rng_Attribute5
Varchar
50
Store Cluster Attribute
Rng_Attribute6
Varchar
50
Store Cluster Attribute
Rng_Attribute7
Varchar
50
Store Cluster Attribute
Rng_Attribute8
Varchar
50
Store Cluster Attribute
No_of_floors
Float
 
No Of Floors
Opening_Date
datetime
 
Store Opening Date
Address1
varchar
100
Address Line 1
Address2
varchar
100
Address Line 2
City
Varchar
100
City
State
Varchar
100
State
Postal Code
Varchar
20
Postal Code
Country
Varchar
50
Country
Email
Varchar
50
Email
Phone
varchar
20
Phone
ManagerName
varchar 
50
Manager’s Name
Size
float
 
Store Selling Size
Last_Update_Date
Varchar
8
Insert Today’s Date

Message Transport Details 
For messages destined for IKB system, the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
SQL Server 2005

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
IKB

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
RDBMS extract

Archiving
There is no archiving requirement

Logging
Should logs be kept of all actions? For how long should these be stored?
Logging should occur, such that the message can be recreated if necessary. It should be based upon the Operational Model (IMOF).

Error Handling
Not yet decided

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

SSIS
Package Name: TOM.S035.IDStoIKB.StoreUpdate.dtsx

Name
s035_getstoredetails_us
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


Outstanding Issues
ID
Issue
To be addressed by
1
BSD is not signed off. Requirements may change.
SRD BSA
2
Deployment not yet considered
Information Architect
3
Alert numbers/identifiers are yet to be defined
Information Architect
4
The design of the IMOF is still being worked and will require retro-fitting to the interface
Information Architect
5
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
IKB
Intactix Knowledge Base
SQL Server Database provided by JDA Intactix for Space Planning and Floor Planning.
IDS
Information Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Store, etc. IDS's reside in the EIA Layer, and are accessed through the EAI Layer.
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
18-Jan-2007
0.1D
Draft
Nitin Singhai
06-Mar-2007
0.2D
Changes 










Distribution

Name
Position
Approver/Contributor/Other
Jon Braggs
Enterprise Architect

Andrew Barker
Engagement Architect

David Onyett
Project Lead

























	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.2, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 10 of  NUMPAGES 19	Date:  SAVEDATE \@ "d MMM yyyy" 13 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































