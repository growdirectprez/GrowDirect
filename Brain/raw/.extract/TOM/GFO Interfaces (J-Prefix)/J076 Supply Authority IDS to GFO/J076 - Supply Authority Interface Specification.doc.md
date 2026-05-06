		









`


Interface Specification for
Supply Authority 
From IDS to GFO


[J076]






Project BEN Code:
W60416
Author:Prasanth DukaramDate:
29/01/2007
Version:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT 1.0
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:


Change Record

Author
Date
Version
Change Reference, description
Prasanth Dukaram
19/01/2007
0.1
Draft
Prasanth Dukaram
29/01/2007
1.0
Review comments incorporated. Please refer the docshare for review comments









Reviewers

Name
Position
Adrian Hinks
Engagement Architect
Heather Rennoldson
Business Analyst




Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Adrian Hinks
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

<Issue Date>
<Version No>










Document Source


Information Architecture Context diagram
http://docshare/UK IT/TOM Integration/Shared Documents/1 - Design/Interface Design Documents/GFO Interfaces (J-Prefix)/J076 Supply Authority IDS to GFO/J076 - Information Context Diagram - Supply Authority.vsd

Mapping spreadsheet
http://docshare/UK IT/TOM Integration/Shared Documents/1 - Design/Interface Design Documents/GFO Interfaces (J-Prefix)/J076 Supply Authority IDS to GFO/J076 - Supply Authority to GFO Mappings.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc157177456 \h 5
1.1	Purpose of Document	 PAGEREF _Toc157177457 \h 5
1.2	Background	 PAGEREF _Toc157177458 \h 5
1.3	Scope	 PAGEREF _Toc157177459 \h 5
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc157177460 \h 6
2.1	Description of the End-to-End Interface	 PAGEREF _Toc157177461 \h 6
2.2	Architecture	 PAGEREF _Toc157177462 \h 6
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc157177463 \h 6
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc157177464 \h 8
3.1	Scope	 PAGEREF _Toc157177465 \h 8
3.2	Source Message Schema	 PAGEREF _Toc157177466 \h 8
3.3	Message Transport Details	 PAGEREF _Toc157177467 \h 8
3.4	Naming and Configuration	 PAGEREF _Toc157177468 \h 9
3.5	Environment and Security Context	 PAGEREF _Toc157177469 \h 9
3.6	Non-Functional Requirements	 PAGEREF _Toc157177470 \h 9
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc157177471 \h 10
4.1	Scope	 PAGEREF _Toc157177472 \h 10
4.2	Data Validation	 PAGEREF _Toc157177473 \h 10
4.3	Filtering	 PAGEREF _Toc157177474 \h 10
4.4	Mapping	 PAGEREF _Toc157177475 \h 10
4.5	Target Message Schema	 PAGEREF _Toc157177476 \h 10
4.6	Sample Target Message	 PAGEREF _Toc157177477 \h 11
4.7	Message Transport Details	 PAGEREF _Toc157177478 \h 11
4.8	Naming and Configuration	 PAGEREF _Toc157177479 \h 12
4.9	Environment and Security Context	 PAGEREF _Toc157177480 \h 12
4.10	Non-Functional Requirements	 PAGEREF _Toc157177481 \h 12
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc157177482 \h 13
5.1	Scope	 PAGEREF _Toc157177483 \h 13
5.2	Data Validation	 PAGEREF _Toc157177484 \h 13
5.3	Filtering	 PAGEREF _Toc157177485 \h 13
5.4	Mapping	 PAGEREF _Toc157177486 \h 13
5.5	Target Message Schema	 PAGEREF _Toc157177487 \h 13
5.6	Message Transport Details	 PAGEREF _Toc157177488 \h 13
5.7	Naming and Configuration	 PAGEREF _Toc157177489 \h 13
5.8	Environment and Security Context	 PAGEREF _Toc157177490 \h 13
5.9	Non-Functional Requirements	 PAGEREF _Toc157177491 \h 13
6	Testing Deliverables	 PAGEREF _Toc157177492 \h 14
7	Deployment	 PAGEREF _Toc157177493 \h 15
8	Assumptions and Outstanding Issues	 PAGEREF _Toc157177494 \h 16
8.1	Assumptions	 PAGEREF _Toc157177495 \h 16
8.2	Outstanding Issues	 PAGEREF _Toc157177496 \h 16
Appendix A Volumes	 PAGEREF _Toc157177497 \h 17
Appendix B Glossary	 PAGEREF _Toc157177498 \h 18
Appendix C Document Control	 PAGEREF _Toc157177499 \h 19

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements with regards to the Supply Authority data from Integration Data Store (IDS) to Group Forecast and Ordering System (GFO).

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is common for both US and Turkey.

Background
As part of the ordering process GFO requires details of each item (product) that can be ordered by the business. This interface extracts the details of the all SKU, its primary suppliers and to which warehouse it is delivered from IDS to GFO

The Oracle Retail Merchandising system is considered the master, and therefore the source for the item supplier data. This data is published into the integration layer (via RIB messages in Oracle Retail v12, via files in Oracle Retail v10), and is written to the IDS. This interface is concerned with moving supplier data from the IDS to GFO only. The flow of item supplier data from the source system, ORMS, to the IDS, is covered by different interface specifications (C001TR, C001US, C010TR and C010US). At the point of writing this interface specification, these documents were not in docshare. It will be put in Docshare in the location http://docshare/UK IT/TOM Integration/Shared Documents/1 - Design/Interface Design Documents/Commercial Interfaces (C-Prefix)
	
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
The interface is a batch extract of Supply Authority data from an Integration Data Store and upload into the GFO system via integration layer. 

Architecture
 EMBED Visio.Drawing.11  
Requirements of the End-to-End Interface
The interface will run once a day, on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IDS, and formats it into the target file format. The file is delivered to GFO via the Real-Time Integrator, to a folder on the GFO host.

GFO requires a full refresh of data each day. GFO will create a file of changes by comparing yesterday’s file with today’s file.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI, and SSIS. At the time of writing (2007-01-18) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

This interface shares common file delivery requirements with interfaces J0052, J0054, J0057, J0087, and J0088. A single RTI instruction will be used by each of these interfaces.

Non-Functional Requirements of the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised – requires discussion n with GFO team.
Performance Requirements
The interface should be capable of extracting data from the IDS and delivering the resulting to GFO before the identified cut-off time. To be finalised – identify the start time of the extract. This must take into account the cut-off point after which any updates from ORMS will not be interfaced to GFO until the following day i.e. any updates received after the extract has started, will not be interfaced to GFO until the following day’s extract.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. There will only ever be a single instance of the IDS and GFO in a TOM implementation and therefore no requirement for multiple files to multiple locations.
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
A scheduled batch job/s runs, at a pre-configured time, to extract the Supply Authority data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL server Integration Services package against the IDS and generates a complete unload of required data-set as a file on a pre-configured file share. The data is also transformed to the required format within SSIS package. As part of data-conversion an extract should convert numeric data to the packed decimal format as per Cobol Copybook format. 
Source Message Schema
In this context, the source being database tables, the source message is generated with the combination of data from the tables.
The data model diagram located at Docshare at  HYPERLINK "http://docshare/UK IT/TOM Integration/Shared Documents/1 - Design/IDS data model/TOM IDS Erwin model update" http://docshare/UK IT/TOM Integration/Shared Documents/1 - Design/IDS data model/TOM IDS Erwin model update 002.ER1 will provide necessary information to get the source data.

Message Transport Details
Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
Windows 2003 Server

Source Physical Location
Sql Server 2005 database

Source Underlying Data Storage Technology
RDBMS

Target System Name
RTI 2.0

Target Platform / OS
Windows 2003 Server

Target Physical Location
Tba

Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	

Data Format.
XML			
Delimited		
Positional		

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
N/A

Logging
Log via the Operational Framework.

Error Handling
On fail move the file to the failed transmissions location.



Naming and Configuration

SSIS
Package Name: TOM_IDSGFO_Supply_Authority_pkg
SSIS Procedure
Name
IDSGFOSupplyAuthorityUnload_sp
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
 
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example employing BizTalk this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).

 
Account details will be included here once we have visibility of the environments.  


Non-Functional Requirements

This section should contain any non-functional requirements pertaining to this stage of the interface.

Processing required in the Messaging Stage of the interface
Scope
RTI monitors the file in the configured location for every new file and submits the same to the remote UNIX –AIX share via RTI File Adapter. The file should be written first with a temporary name, and renamed once delivery is complete.
Data Validation
Data Validation will be done by the target GFO system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.

Please refer the spreadsheet at <location>
Target Message Schema
Field NameReferenced in CR?Insync formatStartLengthCOBOL FormatOccurs






Header Record
(needs to exist)
G
1
36
 
1:1
JLSUA-REC-TYPE
Y
C 1
1
1
X

JLSUA-RUN-DATE
Y
C 8
2
8
X(8)

JLSUA-RUN-TIME
Y
C 6
10
6
X(6)

FILLER
N
C 16
16
21
X(16)

 
 
 
 
 
 

Detail Record
(needs to exist)
G
1
36
 
1:*
JLSUB-REC-TYPE
Y
C 1
1
1
X

JLSUB-STOCK-CENTRE-NO
Y
Z 10
2
10
9(10)

JLSUB-BASE-PRODUCT-NO
Y
Z 9
12
9
9(9)

JLSUB-TRADTPN
Y
Z 9
21
9
9(9)

JLSUB-UNIT-SIZE
Y
Z 5,2
30
7
9(5) V99

 
 
 
 
 
 

Trailer Record
(needs to exist)
G
1
36
 
1:1
JLSUC-REC-TYPE
Y
C 1
1
1
X

JLSUC-REC-COUNT
Y
Z 9
2
9
9(9)

FILLER
N
C 21
11
26
X(26)



Sample Target Message
The source message is from database tables and is getting converted to the target file format in a package. The following message format is the target message format. Alternate fields are in bold for readability.
The numbers used here are part of the example given in the notes section of the mapping document

020070120200050                     
100000123452345678903456789010000005
100000234562345678903456789010000005
100000001232345678903456789010000005
100000002342345678903456789010000005
9000000006                          
Message Transport Details 
For messages destined for GFO system, the following applies.	

Feature
Specification
Additional Information
Source System Name
RTI 2.0

Source Platform / OS
Windows 2003 Server

Source Physical Location
Tba

Source Underlying Data Storage Technology
File System

Target System Name
GFO

Target Platform / OS
Unix – AIX 5.3

Target Physical Location
Tba

Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		

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
Bulk Data 			

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


Naming and Configuration
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages.

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

Naming and Configuration
Not Required
Environment and Security Context
Not Required

Non-Functional Requirements
Testing Deliverables
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption





Outstanding Issues
ID
Issue
To be addressed by
1
The design of the IMOF is still being worked and will require retro-fitting to the interface.

2
Alert numbers/identifiers are yet to be defined.









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
ORMS
Oracle Retek Merchandising System
Retek Merchandising System is getting installed for TESCO Merchandising operations in US. This system will governs the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
IMOF
Integration Management Operational Framework
IMOF is a framework which is pluggable to any Biztalk, RTI and SSIS for alerting, exception handling, defining rules, scheduling etc





















	
Document Control
Change Record

Author
Date
Version
Change Reference, description
Prasanth Dukaram
19/01/2007
0.1
Draft Version















Related Documents

Author	
Date
Version
Title
Heather Rennoldson


Product set-up in ORMS wrt Supply Authority.doc














Distribution

Name
Position
Approver/Contributor/Other
Adrian Hinks
Engagement Architect

David Onyett
Project Lead

Nathan Smith
Enterprise Architect






















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT J076 Supply Authority Interface Specification



	Page:  PAGE  \* MERGEFORMAT 10 of  NUMPAGES 19	Date:  SAVEDATE \@ "d MMM yyyy" 21 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT J076 Supply Authority Interface Specification


Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT J076 Supply Authority Interface Specification



	Page:  PAGE  \* MERGEFORMAT 19 of  NUMPAGES 19	Date:  SAVEDATE \@ "d MMM yyyy" 30 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT J076 Supply Authority Interface Specification





























































