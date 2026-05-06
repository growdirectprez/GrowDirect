		









`


TOM Integration
Interface Specification
On 
Store Range Data
From IKB to SR


[S057]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
19/03/2007
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
19-03-2007
0.1
Draft













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

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.


Information Architecture Context diagram


Mapping spreadsheet
S057 – Store Range (IKB to SR) Mapping Specification
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc162156079 \h 6
1.1	Purpose of Document	 PAGEREF _Toc162156080 \h 6
1.2	Background	 PAGEREF _Toc162156081 \h 6
1.3	Scope	 PAGEREF _Toc162156082 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc162156083 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc162156084 \h 7
2.2	Architecture	 PAGEREF _Toc162156085 \h 7
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc162156086 \h 7
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc162156087 \h 8
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc162156088 \h 9
3.1	Scope	 PAGEREF _Toc162156089 \h 9
3.2	Source Message Schema	 PAGEREF _Toc162156090 \h 9
3.3	Message Transport Details	 PAGEREF _Toc162156091 \h 9
4	Processing Required in the SSIS Stage of the Interface	 PAGEREF _Toc162156092 \h 10
4.1	Scope	 PAGEREF _Toc162156093 \h 10
4.2	Package Overview	 PAGEREF _Toc162156094 \h 10
4.3	Data Validation	 PAGEREF _Toc162156095 \h 10
4.4	Filtering	 PAGEREF _Toc162156096 \h 10
4.5	Mapping	 PAGEREF _Toc162156097 \h 10
4.6	Target Message Schema	 PAGEREF _Toc162156098 \h 10
4.7	Message Transport Details	 PAGEREF _Toc162156099 \h 12
4.8	Naming and Configuration	 PAGEREF _Toc162156100 \h 12
4.9	Environment and Security Context	 PAGEREF _Toc162156101 \h 13
4.10	Non-Functional Requirements	 PAGEREF _Toc162156102 \h 13
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc162156103 \h 14
5.1	Scope	 PAGEREF _Toc162156104 \h 14
5.2	Data Validation	 PAGEREF _Toc162156105 \h 14
5.3	Filtering	 PAGEREF _Toc162156106 \h 14
5.4	Mapping	 PAGEREF _Toc162156107 \h 14
5.5	Target Message Schema	 PAGEREF _Toc162156108 \h 14
5.6	Message Transport Details	 PAGEREF _Toc162156109 \h 14
5.7	Naming and Configuration	 PAGEREF _Toc162156110 \h 14
5.8	Environment and Security Context	 PAGEREF _Toc162156111 \h 14
5.9	Non-Functional Requirements	 PAGEREF _Toc162156112 \h 14
6	Testing Deliverables	 PAGEREF _Toc162156113 \h 15
7	Deployment	 PAGEREF _Toc162156114 \h 16
8	Assumptions and Outstanding Issues	 PAGEREF _Toc162156115 \h 17
8.1	Assumptions	 PAGEREF _Toc162156116 \h 17
8.2	Outstanding Issues	 PAGEREF _Toc162156117 \h 17
Appendix A Volumes	 PAGEREF _Toc162156118 \h 18
Appendix B Glossary	 PAGEREF _Toc162156119 \h 19
Appendix C Document Control	 PAGEREF _Toc162156120 \h 20

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Store Range data between the IKB and Store Range (SR). The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US and Turkey implementation.

Background
As part of the process of managing Space, Range and Display activities in store it is important to identify that the store has accurately completed all space range and display activities. This will help the centre to understand how well stores are conforming to the planograms. This interface provides Store Range Details from IKB to SR.
In Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including IKB and Store Range. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed for product mapping.
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
This interface extracts Store Range details from IKB using a SQL Server Connection and transforms the data into a file. The file in turn is placed into a shared Network location. The Upload is a delta upload in nature. It is application’s responsibility to provide the deltas to integration layer.

The batch extract would initiate the SQL Server Integration service package. A stored procedure will be called by the SSIS package to fetch the data from the holding tables of IKB. Further steps within the SSIS package would transform the data in to a file format required by store range. The file from the SSIS package is written on to the file share of the store range system.

On Extraction of data from IKB, Integration layer is responsible to update the IKB table with the date time stamp on the records which are read during the extraction process

Architecture
 EMBED Visio.Drawing.11  

Requirements of the End-to-End Interface
The interface will run on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IKB, and formats it into the target file Format.

The interface should transfer the data for Store Range from IKB to SR file Share at a pre-configured time (to be determined).  After successful completion, another SR process would then upload the Store Range data to the core tables of SR.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI and SSIS. At the time of writing (2007-03-19) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface
 
Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from IKB through SSIS Service layer using SQL Stored Procedure, delivering the resulting data to into a flat file, before the identified cut-off time. The interface should run on scheduled batch basis. 
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
The data for this interface resides in the IKB in a holding table. 

Holding Table Field Name
Type
Length
Description
Store_no
Varchar
32
Store Number
Product_code
Varchar
16
Product ID
Display_group
Varchar
10
Display Group
Planogram_ID
Varchar
16
Planogram Number
Promo_Indicator
Integer

Promotional Indicator
Live_date
Datetime

object live date
End_date 
Datetime

object end date, expect to be null
Capacity
Integer

cube i.e. facings W x H x D
Facings_Wide
Integer

Number of Facings wide
Number_of_labels
Integer

Number of Labels
SRP_indicator
Integer

SRP Indicator
IL_Time_stamp
Datetime

Set by Integration layer
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
SSIS	                             

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
This section describes the discrete steps within the SSIS package to extract and format data. The target positional flat file format is included in this section. This segment will process the data picked from IKB database (IKB Holding Table : “csg_replen_extract”) and transform into needed flat file format. In turn the Target flat file data will get loaded into a table defined in Store Range database.
Package Overview
SSIS extracts the Store Range data from IKB via SQL Server OLEDB connection, at a predefined time.  In turn, the data is transformed into a flat file and is placed into a file share location.
Data Validation
N/A.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Field Name
String
Length
Starting Position
Occurs
Notes
Header Record

105

1:1

HeaderRecType 
CHAR
1
1

Integration layer to set the record type to 0
RUNDATE
CHAR
10
2


RUNTIME
CHAR
6
12


FILLER
CHAR
88
18


Detail Record

105

1:*

DetailRECTYPE
CHAR
1
1

Integration layer to set the record type to 1 for detail
Store No
INTEGER 
10
2


Product Code
VARCHAR
16
12


Display Group
VARCHAR
10
28


Planogram ID
VARCHAR
16
38


Promotional indicator
INTEGER
1
54


start date
DATETIME
10
55


end date
DATETIME
10
65


Capacity
INTEGER
10
75


Facings wide
INTEGER
10
85


Number of Labels
INTEGER
10
95


SRP Indicator
INTEGER
1
105


Trailer Record

105

1:1

TrailerRECTYPE
CHAR
1
1

Integration layer to set the record type to 9 for trailer
RECCOUNT
CHAR
9
2


FILLER
CHAR
95
11



Message Transport Details 
For messages destined for SR system, the following applies.	

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
File
	

Target System Name
SR (Store Range)

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter	                             
SSIS                                                  

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
Scheduled Batch

Archiving
N/A

Logging
Log via the Operational Framework.

Error Handling
Not yet decided


 
Naming and Configuration

SSIS
Package Name: TOM.S057.IKBtoSR.StoreRange.dtsx

Name
S057_GetStoreRange_usp.sql
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
The target file format has not been decided at the time of writing this document from store range system. So the format provided is assumed at this point of time
2
The IKB holding table is subject to change due to change in requirements. The IKB holding table is taken from the document available at this point of time

Outstanding Issues
ID
Issue
To be addressed by
1
Target File name and Target location to be confirmed
Store range team
2
Timing requirements of interface not established.
Store range team
3
Understand impact of non-delivery of the file.
Store range team
4
The design of the IMOF is still being worked and will require retro-fitting to the interface.
IMOF team
5
Alert numbers/identifiers are yet to be defined.
TOM Solution Architects
6
Field definitions (datatype, size) for IKB csg_replen_extract table is not yet defined. If the field definitions differ than what is currently assumed, then it may result in rework.
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
RMS
Retek Merchandising System
Retek Merchandising System is getting installed for TESCO Merchandising operations in US. This system will governs the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
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
09-Mar-2007
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



Version 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 12 of  NUMPAGES 20	Date:  SAVEDATE \@ "d MMM yyyy" 26 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































