		









`


Interface Specification for
Item-Warehouse-Supplier  
From IDS to GFO


[J100]






Project BEN Code:
W60416
Author:Sankar GDate:
20/02/2007
Version:
1.0
Status:

Modified By:
Sankar G
Reviewed By:
Adrian Hinks 2007-02-22

 Document Control
Change Record

Author
Date
Version
Change Reference, description
Sankar G
20/02/2007
0.1
Draft
Sankar G
22/02/2007
0.2
Draft
Adrian Hinks
22/02/2007
0.3
Changed while performing initial review
Sankar G
23/04/2007
1.0
CR Raised for the following defect 
1869 - The filename is not correct

Reviewers

Name
Position
Adrian Hinks
Engagement Architect






Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Laurence Tang (in lieu of Business Owner
Position
Business Analyst
Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version
Laurence Tang
<Issue Date>
<Version No>
Pardeep Sangha


Richard Durley


David Onyett




Document Source

HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ100%20Item%2dWarehouse%2dSupplier%20Data%20%28IDS%20to%20GFO%29&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d"DocShare: UK IT/TOM Integration/Shared Documents








Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.

Information Architecture Context diagram
J100 - Information Context Diagram - ItemWarehouseSupplier.vsd

Mapping spreadsheet
J100 - Mapping document for Item-Warehouse-Suppier from IDS to GFO v03.xls

Other Reference Documents
Product set-up in ORMS wrt Supply Authority.doc 
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc157177456 \h 7
1.1	Purpose of Document	 PAGEREF _Toc157177457 \h 7
1.2	Background	 PAGEREF _Toc157177458 \h 7
1.3	Scope	 PAGEREF _Toc157177459 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc157177460 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc157177461 \h 8
2.2	Architecture	 PAGEREF _Toc157177462 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc157177463 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc157177464 \h 10
3.1	Scope	 PAGEREF _Toc157177465 \h 10
3.2	Source Message Schema	 PAGEREF _Toc157177466 \h 10
3.3	Message Transport Details	 PAGEREF _Toc157177467 \h 11
3.4	Naming and Configuration	 PAGEREF _Toc157177468 \h 12
3.5	Environment and Security Context	 PAGEREF _Toc157177469 \h 12
3.6	Non-Functional Requirements	 PAGEREF _Toc157177470 \h 12
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc157177471 \h 13
4.1	Scope	 PAGEREF _Toc157177472 \h 13
4.2	Data Validation	 PAGEREF _Toc157177473 \h 13
4.3	Filtering	 PAGEREF _Toc157177474 \h 13
4.4	Mapping	 PAGEREF _Toc157177475 \h 13
4.5	Target Message Schema	 PAGEREF _Toc157177476 \h 13
4.6	Sample Target Message	 PAGEREF _Toc157177477 \h 14
4.7	Message Transport Details	 PAGEREF _Toc157177478 \h 14
4.8	Naming and Configuration	 PAGEREF _Toc157177479 \h 15
4.9	Environment and Security Context	 PAGEREF _Toc157177480 \h 15
4.10	Non-Functional Requirements	 PAGEREF _Toc157177481 \h 16
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc157177482 \h 17
5.1	Scope	 PAGEREF _Toc157177483 \h 17
5.2	Data Validation	 PAGEREF _Toc157177484 \h 17
5.3	Filtering	 PAGEREF _Toc157177485 \h 17
5.4	Mapping	 PAGEREF _Toc157177486 \h 17
5.5	Target Message Schema	 PAGEREF _Toc157177487 \h 17
5.6	Message Transport Details	 PAGEREF _Toc157177488 \h 17
5.7	Naming and Configuration	 PAGEREF _Toc157177489 \h 17
5.8	Environment and Security Context	 PAGEREF _Toc157177490 \h 17
5.9	Non-Functional Requirements	 PAGEREF _Toc157177491 \h 17
6	Testing Deliverables	 PAGEREF _Toc157177492 \h 18
7	Deployment	 PAGEREF _Toc157177493 \h 19
8	Assumptions and Outstanding Issues	 PAGEREF _Toc157177494 \h 20
8.1	Assumptions	 PAGEREF _Toc157177495 \h 20
8.2	Outstanding Issues	 PAGEREF _Toc157177496 \h 20
Appendix A Volumes	 PAGEREF _Toc157177497 \h 21
Appendix B Glossary	 PAGEREF _Toc157177498 \h 22
Appendix C Document Control	 PAGEREF _Toc157177499 \h Error! Bookmark not defined.

 
Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements with regards to the Item-Warehouse-supplier data from Integration Data Store (IDS) to Group Forecast and Ordering System (GFO).

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is common for both US and Turkey.

Background
As part of the ordering process GFO requires all SKU details described. Each item (SKU) attached to warehouse and linked with primary supplier. This interface extracts the details of the all SKU, its primary suppliers and to which warehouse it is delivered. This information flow from IDS to GFO

The Oracle Retail Merchandising system is considered the master, and therefore the source for the item supplier data. This data is published into the integration layer (via RIB messages in Oracle Retail v12, via files in Oracle Retail v10), and is written to the IDS. This interface is concerned with moving Item-Warehouse-Supplier data from the IDS to GFO only. The flow of Item-Warehouse-Supplier data from the source system ORMS to the IDS, is covered by a different interfaces viz. (C001US, C010US) for US and (C001TR, C010TR) for Turkey.
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
The interface is a batch extract of Item-Warehouse-Supplier data from common forms associated with Integration Data Store (IDS) picked through Web service calls. This data will be further transformed in SSIS packages and create a file in the format required by GFO. The file from the SSIS package is written locally first and then delivered via the Real-Time Integrator to the GFO file location.  

Architecture


Requirements of the End-to-End Interface
The interface will run once a day, on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IDS through common forms, and transforms and formats it into the target file. The file is delivered to GFO via RTI file adaptor, to a folder on the GFO host.

GFO requires a full refresh of data each day. GFO will create a file of changes by comparing yesterday’s file with today’s file.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI, and SSIS. 

A single RTI instruction will be used to transfer the target file.

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
The interface must be available at the scheduled extract time. Any outages scheduled should take copuor scheduled nce a day-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A – No scalability issues exist. There will only ever be a single instance of the IDS and GFO in a TOM implementation and therefore no requirement for multiple files to multiple locations.
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
A scheduled batch job/s runs, at a pre-configured time, to extract the Item-Warehouse-Supplier data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL server Integration Services package, calls the common forms which are associated with IDS. After executing the common form service, a complete unload of required data-set will be returned as output to SSIS package.  The retuned data-set will be captured and also transformed to the required format within SSIS package and write it to a local folder. 
Source Message Schema
In this context, the source being database tables, the source message is generated with the combination of data from the tables.
The data model diagram located at  HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fIDS%20data%20model&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fIDS%20data%20model&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d  will provide necessary information to get the source data.


Common Forms
Service Name
Description
<name>
Include a brief description of the common form service e.g. whether it’s a web service, stored procedure, version, names of common forms returned.  
<name>




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
BizTalk

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
File Drop(Windows) 	
                (XCOM) 	
SSIS 	                  	

Data Format.
XML			
Delimited		
Positional		
RDBMS data stream	

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
Package Name: TOM_IDSGFO_Item_Warehouse_Supplier_pkg
SSIS Procedure
Name
IDSGFOItemWarehouseSupplierUnload_sp
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

 
Account details will be included here once we have visibility of the environments.  


Non-Functional Requirements

This section should contain any non-functional requirements pertaining to this stage of the interface.

Processing required in the Messaging Stage of the interface
Scope
This section describes the process of delivering the file produced in the previous stage. 

Processing Overview
A Real-Time Integrator Instruction is configured to monitor the local folder location for the arrival of the file and then delivers the file to the GFO folder location. If the file cannot be delivered to the GFO folder location the file will be delivered to the failed files location. The file should be written first with a temporary name, and renamed once delivery is complete.
Data Validation
Data Validation will be done by the target GFO system.
Filtering
There is no filtering requirement.
Mapping
Pseudo code of the mapping specification

Objective:
The Item-Warehouse-Supplier data to be picked up form the IDS tables and populate in a COBOL format file. All SKUs for corresponding warehouse with the primary supplier data to be sent to GFO

Method:
There are three entities involved in picking up the data. They are Warehouse, Item and Supplier. For this in the logical data model TOM.Common.Schema.Warehouse.xml common form is getting used. The warehouse, linked with SKUs to be picked up primarily and subsequently corresponding Primary Supplier for the SKU to be stored. Primary supplier data is available in two relational entities. They are residing in SKUSupplier and SKUSupplierCountryOfOrigin.  Primarily the supplier should be looked up in SKUSupplier entity. If the Supplier is not available, then SKUSupplierCountryOfOrigin entity should be looked upon.

Mapping document will be provided subsequently.

Please refer the spreadsheet at   HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ100%20Item%2dWarehouse%2dSupplier%20Data%20%28IDS%20to%20GFO%29&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ100%20Item%2dWarehouse%2dSupplier%20Data%20%28IDS%20to%20GFO%29&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d

Target Message Schema
Field NameReferenced in CR?Insync formatStartLengthCOBOL FormatOccurs / 
Description






Header Record
(needs to exist)
G
1
30
 
1:1
JISDA-REC-TYPE     
Y
C 1
1
1
X
Record type (‘0’ for Header)
JISDA-RUN-DATE     
Y
C 8
2
8
X(8)
Date (CCYYMMDD) of sent file
JISDA-RUN-TIME     
Y
C 6
10
6
X(6)
Time (hhmmss) of sent file
FILLER         
N
C 15
16
15
X(15)
Spaces
 
 
 
 
 
 

Detail Record
(needs to exist)
G
1
36
 
1:*
JISDB-REC-TYPE       
Y
C 1
1
1
X
Record type (‘1’ for Detail)
JISDB-STOCK-CENTRE-NO
Y
Z 10
2
10
9(10)
Stock centre number (Warehouse)
JISDB-BASE-PRODUCT-NO      
Y
Z 9
12
9
9(9)
product Code (TPNB)
JISDB-SUPP-NO     
Y
Z 10
21
10
9(10)
Preferred Supplier Number 
 
 
 
 
 
 

Trailer Record
(needs to exist)
G
1
36
 
1:1
JISDC-REC-TYPE 
Y
C 1
1
1
X
Record type (‘9’ for Trailer)
JISDC-REC-COUNT
Y
Z 9
2
9
9(9)
Record count including the header and trailer records.
FILLER         
N
C 20
11
20
X(20)
Spaces









Target Message
The source message is from database tables and is getting converted to the target file format in a package. 

Message Transport Details 
For messages destined for GFO system, the following applies.	

Feature
Specification
Additional Information
Source System Name
BizTalk

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
File Drop (Windows) 		
RTI File Adaptor 			
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


Source Folder


Target Folder


Failure Folder


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
Target File name and Target location to be confirmed
Adrian Hinks
2
Timing requirements of interface not established.
Sankar Ganesan / Pardeep Sangha
3
Understand impact of non-delivery of the file.
Sankar Ganesan / Pardeep Sangha





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
Integration Monitoring & Operations Framework
A framework providing a way of defining key events and monitoring these events. It also provides a rules engine allowing recovery actions to be taken on failure. 
	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Interface Specification



	Page:  PAGE  \* MERGEFORMAT 18 of  NUMPAGES 23	Date:  SAVEDATE \@ "d MMM yyyy" 23 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Interface Specification



Guess we don’t know this time yet as we are waiting on the operating clock.
Need to identify the file share. (Action AH)
TODO: check against naming standards 
TODO: check against naming standards
To be determined.
To be determined.
To be  determined (AH)
To be determined (AH)
To be determined (AH)



























































