		









`


TOM Integration

Interface Specification on
Actual Range in Store from
GFO to Store Range
=

[S077]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
16/03/2007
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1D
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:


Change Record

Author
Date
Version
Change Reference, description

















Reviewers

Name
Date
Version
Position


















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
Jon Braggs


Andrew Barker


David Onyett


Mary Welch






Document Source

Related Documents: 
File Name: 





Information Architecture Context diagram


Mapping spreadsheet
S077 Actual Range in Store (GFO to SR) Mapping Spec
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc161821487 \h 6
1.1	Purpose of Document	 PAGEREF _Toc161821488 \h 6
1.2	Background	 PAGEREF _Toc161821489 \h 6
1.3	Scope	 PAGEREF _Toc161821490 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc161821491 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc161821492 \h 7
2.2	Architecture	 PAGEREF _Toc161821493 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc161821494 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc161821495 \h 9
3.1	Scope	 PAGEREF _Toc161821496 \h 9
3.2	Source Message Schema	 PAGEREF _Toc161821497 \h 9
3.3	Message Format	 PAGEREF _Toc161821498 \h 9
3.4	Message Transport Details	 PAGEREF _Toc161821499 \h 9
3.5	Naming and Configuration	 PAGEREF _Toc161821500 \h 10
3.6	Environment and Security Context	 PAGEREF _Toc161821501 \h 10
3.7	Non-Functional Requirements	 PAGEREF _Toc161821502 \h 10
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc161821503 \h 11
4.1	Scope	 PAGEREF _Toc161821504 \h 11
4.2	Data Validation	 PAGEREF _Toc161821505 \h 11
4.3	Filtering	 PAGEREF _Toc161821506 \h 11
4.4	Mapping	 PAGEREF _Toc161821507 \h 11
4.5	Target Message Schema	 PAGEREF _Toc161821508 \h 11
4.6	Message Format	 PAGEREF _Toc161821509 \h 11
4.7 Message Transport Details	 PAGEREF _Toc161821510 \h 11
4.7	Naming and Configuration	 PAGEREF _Toc161821511 \h 13
4.8	Environment and Security Context	 PAGEREF _Toc161821512 \h 13
4.9	Non-Functional Requirements	 PAGEREF _Toc161821513 \h 13
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc161821514 \h 14
5.1	Scope	 PAGEREF _Toc161821515 \h 14
5.2	Data Validation	 PAGEREF _Toc161821516 \h 14
5.3	Filtering	 PAGEREF _Toc161821517 \h 14
5.4	Mapping	 PAGEREF _Toc161821518 \h 14
5.5	Target Message Schema	 PAGEREF _Toc161821519 \h 14
5.6	Message Transport Details	 PAGEREF _Toc161821520 \h 14
5.7	Naming and Configuration	 PAGEREF _Toc161821521 \h 14
5.8	Environment and Security Context	 PAGEREF _Toc161821522 \h 14
5.9	Non-Functional Requirements	 PAGEREF _Toc161821523 \h 14
6	Testing Deliverables	 PAGEREF _Toc161821524 \h 15
7	Deployment	 PAGEREF _Toc161821525 \h 16
8	Assumptions and Outstanding Issues	 PAGEREF _Toc161821526 \h 17
8.1	Assumptions	 PAGEREF _Toc161821527 \h 17
8.2	Outstanding Issues	 PAGEREF _Toc161821528 \h 17
Appendix A Volumes	 PAGEREF _Toc161821529 \h 18
Appendix B Glossary	 PAGEREF _Toc161821530 \h 19
Appendix C Document Control	 PAGEREF _Toc161821531 \h 20

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Store / Product Range Details.
The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US and Turkey implementations.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including GFO and SRD Store Range. To achieve this functionality, high level process flow architecture has been designed and approved by TESCO Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Store Range data from GFO to SRD Store Range Database.
Scope
The Interface Specification covers:

audit requirements across the interface
security requirements across the interface
timing/frequency requirements or constraints
support requirements
archiving
the data format to be used for the interface at each stage 
the normal processing required at each stage
recovery from failure required at each stage
volumes.

Note that it is Tesco strategy to avoid placing any business logic in integration layer processing.
Description and Requirements for the End-to-End Interface
Description of the End-to-End Interface
The interface is a batch extract of Group Forecast and Ordering (GFO), from a flat file (positional) and uploads into SRD Store Range. The Upload is a delta upload in nature. It is application’s responsibility to provide the deltas to integration layer.

The interface is meant to run at a pre-configured time interval, which on completion is expected to produce flat file. This shared location would be monitored by Store Range systems Interface at the same interval. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into Store Range Database.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 
Architecture
 EMBED Visio.Drawing.11  
Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data in the form of flat file from the shared location at GFO side and delivering the resulting to another shared location at Store Range side before the identified cut-off time. The interface should run as a batch process. 
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. 
Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
N/A 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope
GFO pushes a positional flat file containing the Store Range data, to a predefined shared location. The flat file is created at a predefined time interval. Once the file is created at the shared location, BizTalk picks up the file, transforms the file into a flat file and pass the file to another shared location accessible by Store Range for further processing. 

Source Message Schema
Field Name
Record Type
Data Type & Size
Starting Position
Notes
JLCXA-CR-TO-CRST-XFER-HDR
01



JLCXA-RETAIL-OUTLET-NO
03
PIC    9(5)
1
(Record Type ‘00000’ for Header)
JLCXA-DATE-CREATED
03
PIC X(10)
6
Date (CCCC-MM-DD) of sent file.
JLCXA-CREATE-TIME 
03
PIC X(5)
16
Time (HH:MM) od sent file
JLCXA-CA7RUNNO
03
PIC X
21

FILLER
03
PIC X(36)
22
SPACES
JLCXB-CR-TO-CRST-XFER-REC.
01



JLCXB-RETAIL-OUTLET-NO   
03
PIC 9(5)
1

JLCXB-BASE-PRODUCT-NO
03
PIC 9(9) 
6

JLCXB-STKD-PROD-STDT
03
PIC X(10)
15

JLCXB-STKD-PROD-ENDT
03
PIC X(10)
25

JLCXB-CR-RNGE-SRCE
03
PIC X
35

JLCXB-ACTL-RNGE-IN-DT
03
PIC X(10)
36

JLCXB-ACTL-RNGE-OUT-DT
03
PIC X(10)
46

JLCXB-PROM-IND 
03
PIC X
56

JLCXB-ON-PROMOTION
88
VALUE "Y”


JLCXB-NEG-BOOK-STOCK
03
PIC X
57

JLCXZ-CR-TO-CRST-XFER-TRLR.
01 



JLCXZ-RETAIL-OUTLET-NO
03
PIC 9 (5)
1
(Record Type ‘99999’ for Header)
JLCXZ-REC-COUNT 
03
PIC 9(9)
6
Record Count
FILLER
03
PIC X(43)
15
SPACES


Message Format
The source message is in the form of positional file from GFO and is getting converted into the target file format in a package. The following sample message format is the source message format. 

The sample file will be attached.

Message Transport Details

Feature
Specification
Additional Information
Source System Name
GFO

Source Platform / OS
UNIX –AIX 5.3

Source Physical Location
GFO_Output

Source Underlying Data Storage Technology


Target System Name
BizTalk 2006

Target Platform / OS
BizTalk 2006 Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
RTI Adapter		

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
Bulk Data		

Real-time/Scheduled Batch
Not yet decided

Archiving
Archiving of Source File should happen. Once the Interface has finished its run successfully, the file should be placed to GFO Archive Folder GFO_Archive. 

Logging
Logging should occur, such that the message can be recreated if necessary.

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

Biztalk – 2006
Package Name: Tesco_TOM_GFO_StoreRangeData_for_SR_File_Delivery
BizTalk Procedure
Name

<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
BizTalk monitors the file in the configured location for every new file and submits the same to the remote file share as a File Drop. The resultant file is a flat file.
Data Validation
Data Validation will be done by the target Target- Store Range system.
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

56

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
5
12


FILLER
CHAR
39
18


Detail Record

56

1:*

DetailRECTYPE
CHAR
1
1

Integration layer to set the record type to 1 for detail
Store Number  
Integer
5
2


Base Product Number
Integer
9
7


Stock Start Date
Datetime
10
16


Stock End Date
Datetime
10
26


Stock Reason Code
CHAR
1
36


Actual Range In Date
Datetime
10
37


Actual Range Out Date
Datetime
10
47


Trailer Record

56

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
46
11



Message Format
The source message is a positional flat file from GFO and is getting converted into the target file format for Store Range in a package. The target message is a flat file. 

4.7 Message Transport Details 
For messages destined for Store Range system, the following applies.	

Feature
Specification
Additional Information
Source System Name
BizTalk 2006

Source Platform / OS
BizTalk 2006 Server

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
SRD Store Range

Target Platform / OS
Windows 2003 Server

Target Physical Location
Tba

Target Underlying Data Storage Technology
File Share

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		

Data Format

RIB Message			
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
Not yet decided



Naming and Configuration

Biztalk 2006
Instruction Name: 
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
On successful delivery of the file to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure the file should be written to the failed files location, and an alert should be raised.


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
Unit Test Scripts and test cases are kept at the following location <location>

Deliverable
Description
TBD <stored proc name>
Stored Procedure
TBD <stored proc name>
Stored Procedure
TBD <service name>
Web Service
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
The target file format has not been decided at the time of writing this document from store range system. So the format provided is assumed at this point of time

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
Integration Solution Architect


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
GFO
Global Forecasting and Ordering
GFO is the brain of TESCO ordering procedure, which will advise RMS, Storeline for the Direct Store Order of quantity. 
Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
16-03-2007
0.1D
Draft















Related Documents

Author	
Date
Version
Title
To be filled

















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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 8 of  NUMPAGES 21	Date:  SAVEDATE \@ "d MMM yyyy" 28 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































