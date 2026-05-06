		









`


TOM Integration
Interface Specification
On 
Store Details Update
From IDS to CRDB


[S008]





Project BEN Code:
W60416
Author:Shajitha MohammedDate:
23/04/2007
Version:
0.1
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft
Modified By:

Reviewed By:
Andrew Barker

Change Record

Author
Date
Version
Change Reference, description
Shajitha Mohammed
20-04-2007
0.1
Draft













Reviewers

Name
Date
Version
Position
Andrew Barker

0.1
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



Document Source
HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d"DocShare: UK IT/TOM Integration/Shared Documents

Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.


Mapping spreadsheet
S009-StoreDetailsUpdate(IDStoCRDB) Mappings.xls

Other Reference Documents
Interface 001 Store Details v3.1.doc
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc165359040 \h 5
1.1	Purpose of Document	 PAGEREF _Toc165359041 \h 5
1.2	Background	 PAGEREF _Toc165359042 \h 5
1.3	Scope	 PAGEREF _Toc165359043 \h 5
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc165359044 \h 6
2.1	Description of the End-to-End Interface	 PAGEREF _Toc165359045 \h 6
2.2	Architecture	 PAGEREF _Toc165359046 \h 6
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc165359047 \h 6
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc165359048 \h 7
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc165359049 \h 8
3.1	Scope	 PAGEREF _Toc165359050 \h 8
3.2	Source Message Schema	 PAGEREF _Toc165359051 \h 8
3.3	Message Transport Details	 PAGEREF _Toc165359052 \h 8
4	Processing Required in the SSIS Stage of the Interface	 PAGEREF _Toc165359053 \h 10
4.1	Scope	 PAGEREF _Toc165359054 \h 10
4.2	Package Overview	 PAGEREF _Toc165359055 \h 10
4.3	Data Validation	 PAGEREF _Toc165359056 \h 10
4.4	Filtering	 PAGEREF _Toc165359057 \h 10
4.5	Mapping	 PAGEREF _Toc165359058 \h 10
4.6	Target Message Schema	 PAGEREF _Toc165359059 \h 10
4.7	Message Transport Details	 PAGEREF _Toc165359060 \h 12
4.8	Naming and Configuration	 PAGEREF _Toc165359061 \h 13
4.9	Environment and Security Context	 PAGEREF _Toc165359062 \h 13
4.10	Non-Functional Requirements	 PAGEREF _Toc165359063 \h 13
5	Testing Deliverables	 PAGEREF _Toc165359064 \h 15
6	Deployment	 PAGEREF _Toc165359065 \h 16
7	Assumptions and Outstanding Issues	 PAGEREF _Toc165359066 \h 17
7.1	Assumptions	 PAGEREF _Toc165359067 \h 17
7.2	Outstanding Issues	 PAGEREF _Toc165359068 \h 17
Appendix A Volumes	 PAGEREF _Toc165359069 \h 18
Appendix B Glossary	 PAGEREF _Toc165359070 \h 19
Appendix C Document Control	 PAGEREF _Toc165359071 \h 20

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements to transfer the store details between the IDS to CRDB. The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for both US and Turkey implementations.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including IDS and CRDB. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer store details from IDS into CRDB.
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
The interface is a batch extract of store details from IDS using Common Forms and sends it to the CRDB system as a positional Flat file via integration layer.

Architecture
 EMBED Visio.Drawing.11  

Requirements of the End-to-End Interface
The interface will run once a day, on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IDS, and formats it into the target file format. 

The interface is meant to run nightly at a pre-configured time which on completion is expected to upload the Store details in a Flat file into CRDB shared directory.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI, and SSIS. At the time of writing (2007-01-20) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from IDS using Common Forms, delivering the resulting data to CRDB in form of Flat file before the identified cut-off time. The interface should run on scheduled batch basis. 
Reliability and Availability Requirements
The interface-run should be non atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The scheduled start of the extract job and/or the completion of the target table update should be defined as IMOF events.  
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
A scheduled batch job/s runs, at a pre-configured time, to extract the store information from IDS. This batch job in turn kicks off a process that executes SQL server Integration Services package and creates a required data-set as a flat file to a shared location in the integration layer. The data is also transformed to the required format within SSIS package

Source Message Schema
The data for this interface resides in the IDS. Common Form Service TOM.Common.Schema.Location  is called by the SSI package to extract the store details. The services are exposed as stored procedures and return row sets representing all the details of location and store in the Location Common Form. 
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
Windows 2003 Server

Target Physical Location
SQL SERVER 2005

Target Underlying Data Storage Technology
RDBMS

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
Common Forms 		

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
This section describes the discreet steps within the SSIS package to extract and format data. The target file format is included in this section. 
Package Overview
SSIS extracts the store details from IDS using Common Forms, nightly at predefined time.  In turn, the data is formatted as per the target CRDB systems file structure and uploaded same into the CRDB allocated inbox shared directory.
Data Validation
N/A
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Header Record
Column Name
Type
Length

Description
Record Type
Alphanumeric
2
Set to '00' for the header record.
Date/Time File Created
Alphanumeric
14
File Creation Date
Sequence number
Alphanumeric
0
Set to '000000'
Date
Alphanumeric
8
System date
File Id
Alphanumeric
9
Set to '000'
Detail Record
Column Name
Type
Length

Description
Record Type
Numeric
2
Set to ‘01’
Branch Number
Numeric
5
Store Number
Branch Name
Alphanumeric
21

Original Store Opening Date
Date
8

Store Closure Date
Date
8

Actual Country
Alphanumeric
1

Actual Format
Alphanumeric
2

Filler
Alphanumeric
7

Trailer Record
Column Name
Type
Length

Description
Record Type
Alphanumeric
2
Set to '99' for the footer records
Record Count
Alphanumeric
10
Number of records (inc header & trailer)
Filler
Alphanumeric
21
Spaces

Message Transport Details 
For messages destined for CRDB system, the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
SQL Server 2005

Source Physical Location
IDS

Source Underlying Data Storage Technology
RDBMS

Target System Name
CRDB

Target Platform / OS
Windows

Target Physical Location
Configurable

Target Underlying Data Storage Technology
File-Based

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter                              
SSIS File Adopter                            

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
RDBMS extract

Archiving
There is no archiving requirement

Logging
Should logs be kept of all actions? For how long should these be stored?
Logging should occur, such that the message can be recreated if necessary.

Error Handling
On fail move the file to the failed transmissions location. The file drop failure will be tracked through IMOF functionality and will be done through a change request.


Naming and Configuration

SSIS
Package Name: TOM_IDSCRDB_StoreDetailsUpdate_pkg

Name
IDSCRDBStoreDetailsUpdate
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



Outstanding Issues
ID
Issue
To be addressed by
1
Timings and cut-off constraints need to be defined. Require input from CRDB. 

2
Destination  Shared location to be confirmed

3
Error handling to be confirmed with respect to archiving process









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
IMOF
Integration Management Operational Framework
IMOF is a framework which is pluggable to any Biztalk, RTI and SSIS for alerting, exception handling, defining rules, scheduling etc

Document Control
Change Record

Author
Date
Version
Change Reference, description
Shajitha Mohammed
19-April-2007
0.1D
Draft















Related Documents

Author	
Date
Version
Title
Andy J Smith
08/09/2006
v3.1
Interface 080 Product Description 














Distribution

Name
Position
Approver/Contributor/Other
Andrew Barker
Engagement Architect

John Cowper
Solution Architect

Jon Braggs
Enterprise Architect

David Onyett
Project Lead

Venkateswara Rao
Delivery Manager














	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 17 of  NUMPAGES 20	Date:  SAVEDATE \@ "d MMM yyyy" 26 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































