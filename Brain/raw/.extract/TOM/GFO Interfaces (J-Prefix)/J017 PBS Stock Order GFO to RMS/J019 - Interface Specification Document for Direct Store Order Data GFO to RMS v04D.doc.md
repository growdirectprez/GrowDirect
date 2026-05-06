		









`


TOM Integration

Interface Specification
Direct Store Order data
From GFO to RMS


[J019]






Project BEN Code:
W60416
Author:
Sankar G
Date:
25/01/2007
Version:
0.4
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:


Change Record

Author
Date
Version
Change Reference, description
Sankar G
25-Jan-2007
0.1D
Draft
Sankar G
26-Jan-2007
0.2D
Draft
Sankar G
05-Feb-2007
0.3D
Draft
Sankar G
09-Feb-2007
0.4D
Draft

Reviewers

Name
Date
Version
Position
Rob McDonagh

0.1D
Solution Architect














At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Rob McDonagh
Position
Solution Architect
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
Doc Share



Related Documents
1. Technical System Design: Order routing TSD006 v5


Information Architecture Context diagram
J019 - Information Context Diagram - Direct Store Order (GFO to RMS)

Mapping spreadsheet

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 3
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 3
1.2	Background	 PAGEREF _Toc153956171 \h 3
1.3	Scope	 PAGEREF _Toc153956172 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 3
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 3
2.2	Architecture	 PAGEREF _Toc153956175 \h 3
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 3
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153956177 \h 3
3.1	Scope	 PAGEREF _Toc153956178 \h 3
3.2	Source Message Schema	 PAGEREF _Toc153956179 \h 3
3.3	Message Transport Details	 PAGEREF _Toc153956180 \h 3
3.4	Naming and Configuration	 PAGEREF _Toc153956181 \h 3
3.5	Environment and Security Context	 PAGEREF _Toc153956182 \h 3
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153956183 \h 3
4.1	Scope	 PAGEREF _Toc153956184 \h 3
4.2	Data Validation	 PAGEREF _Toc153956185 \h 3
4.3	Filtering	 PAGEREF _Toc153956186 \h 3
4.4	Mapping	 PAGEREF _Toc153956187 \h 3
4.5	Target Message Schema	 PAGEREF _Toc153956188 \h 3
4.6	Message Format	 PAGEREF _Toc153956189 \h 3
4.7	Message Transport Details	 PAGEREF _Toc153956190 \h 3
4.8	Naming and Configuration	 PAGEREF _Toc153956191 \h 3
4.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 3
4.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 3
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153956194 \h 3
5.1	Scope	 PAGEREF _Toc153956195 \h 3
5.2	Data Validation	 PAGEREF _Toc153956196 \h 3
5.3	Filtering	 PAGEREF _Toc153956197 \h 3
5.4	Mapping	 PAGEREF _Toc153956198 \h 3
5.5	Target Message Schema	 PAGEREF _Toc153956199 \h 3
5.6	Message Transport Details	 PAGEREF _Toc153956200 \h 3
5.7	Environment and Security Context	 PAGEREF _Toc153956201 \h 3
6	Testing Deliverables	 PAGEREF _Toc153956202 \h 3
7	Deployment	 PAGEREF _Toc153956203 \h 3
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 3
8.1	Assumptions	 PAGEREF _Toc153956205 \h 3
8.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 3
Appendix A Volumes	 PAGEREF _Toc153956207 \h 3
Appendix B Glossary	 PAGEREF _Toc153956208 \h 3
Appendix C Document Control	 PAGEREF _Toc153956209 \h 3

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Direct Store Order data between GFO (Group Forecasting and Ordering) and Retek Merchandising System (RMS) or ORMS (Oracle Retail Merchandising System)*. 

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally this document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no separate associated TSD for this interface. 

This interface is for both US implementations.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including RMS and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Direct Store Order data from GFO into RMS.
	
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


* From now on we will use RMS only. In the context of Turkey the same will mean RMS and in the context of US it will mean ORMS.
Description and Requirements for the End-to-End Interface
Description of the End-to-End Interface
The interface is an extract of Direct Store Order data from GFO by Unix Korn Shell Scripts and transfers to a shared location via XCOM, and uploads into the RMS system via integration layer BizTalk interfaces. The RMS EDI batch process will identify the record as Pick By Store record as JIROB-PBL-IND field in the source file with value as 3. The process is a delta upload in nature. 

The BizTalk interface is meant to run at a pre-configured time interval, which on completion is expected to produce a positional flat-file (containing Direct Store Order Data in required from by RMS) onto the shared location. This shared location would be monitored by RMS system at the same interval. In turn the file containing the extracted data appears on the shared location RMS system will start the processing the Direct Store Order Data.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture

Requirements for the End-to-End Interface
Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The scheduled batch job should be completed before the next batch of job gets scheduled.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements

Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
No such requirement till the time of writing this document.
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope
The Unix Korn Shell Scripts runs at a predefined time to generate Direct Store Order Records in a COBOL flat file. This flat file is transferred to a predefined location through XCOM. BizTalk picks up the COBOL flat file from the shared location for further processing and transformation.
Source Message Schema
In this context, the source carries the data in the format specified below. The data file is a positional file but variable record in length. Each row in the data file will carry first 5 characters as definition of row. Following table carries description column, which explain at row level and column level details.

File Name: GFO_DTSORD_<CCYYMMDDHHmmss>_RUN<RunID=X>.dat

Field Name
Record Type
Data Type & Size
Starting Position
Description
JIROA-RMS-ORD-HDR
01


Procurement/Final  Order Header Record Section
JIROA-REC-TYPE
   03
PIC X
1
Header Record Type
JIROA-HEADER-RECORD
     88
VALUE "0"

Header record value = “0”
JIROA-DETAIL-RECORD
     88
VALUE "1"

Detail  record value = “1”
JIROA-TRAILER-RECORD
     88
VALUE "9"

Trailer record value = “9”
JIROA-EXTRACT-DATE
   03
PIC 9(8)
2
Data Extraction Date
JIROA-EXTRACT-TIME
   03
PIC 9(6)
10
Data Extraction Time
JIROA-SEQUENCE-NO
   03
PIC 9(10)
16
Header Sequence No
FILLER
   03
PIC X(125)
26
Set to Spaces
JIROB-RMS-ORD-REC.
01


Detail Record Section
JIROB-REC-TYPE
   03
PIC X
1
Detail Record Type
JIROB-HEADER-RECORD
     88
VALUE "0"

Header record value = “0”
JIROB-DETAIL-RECORD
     88
VALUE "1"

Detail  record value = “1”
JIROB-TRAILER-RECORD
     88
VALUE "9"

Trailer record value = “9”
JIROB-BASE-PRODUCT-NO
   03
PIC 9(9)
2
TPNB
JIROB-STOCK-CENTRE-NO
   03
PIC 9(10)
11
Distribution Centre
JIROB-RMS-SUPPLIER
   03
PIC 9(10)
21
Supplier Code
JIROB-REQ-DELIVERY-DATE
   03
PIC 9(8)
31
Delivery date into store
JIROB-LM-ORD-TYPE
   03
PIC X
39
Order type
JIROB-EXTR-CONT-IND
   03
PIC X
40
Indicator to signify whether the order is Extracted ‘1’ or Contingency ‘2’
JIROB-RETAIL-OUTLET-NO
   03
PIC 9(5)
41
Store number
JIROB-RO-FCST-QTY
   03
PIC +9(9).99
46
Requested quantity in relevant Unit of Measure, e.g. kg, singles
JIROB-ACT-QTY
   03
PIC +9(9).99
59
Actual quantity after stock share
JIROB-PBL-IND
   03
PIC X
72
Indicator to signify replenishment mode
1 = Pick By Line
2 = Pick By Store
3 = Direct to Supplier
JIROB-PBL-TYPE-IND
   03
PIC X
73
Pick By Line indicator 
1 = procurement
2 = final
JIROB-RAW-QTY
   03
PIC +9(9).99
74
Raw demand quantity, i.e.
what the store actually requested before rounding
JIROB-UNIT-SIZE-X.
   03



JIROB-UNIT-SIZE
     05
PIC 9(5).99
87
Case size

JIROB-TRADTPN
   03
PIC 9(9)
95

JIROB-GFO-ORD-NO
   03
PIC 9(9)
104
GFO-generated order number 
JIROB-RMS-ORD-NO
   03
PIC 9(10)
113
Purchase Order or Transfer number from RMS 
JIROB-RMS-ORD-NO-X REDEFINES JIROB-RMS-ORD-NO
   03
PIC X(10)

Order group code – used when the file is passed back
JIROB-RMS-REASON-CD
   03
PIC X(10)
123

JIROB-ORDER-GROP         
   03
PIC XX
133
Order Group
FILLER
   03
PIC X(16)
135
Set to Spaces
JIROZ-RMS-ORD-TRLR.
01 


Trailer Record Section
JIROZ-REC-TYPE
   03
PIC X
1
Trailer Record Type
JIROZ-HEADER-RECORD
     88
VALUE "0"

Header record value = “0”
JIROZ-DETAIL-RECORD
     88
VALUE "1"

Detail  record value = “1”
JIROZ-TRAILER-RECORD
     88
VALUE "9"

Trailer record value = “9”
JIROZ-REC-COUNT
   03
PIC 9(10)
2
Total Record Count in the file
FILLER
   03
PIC X(139)
12
Set to Spaces

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
Biztalk 2006

Target Platform / OS
Biztalk 2006 Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	

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
Scheduled Batch

Archiving
N/A

Logging
Log via the Operational Framework.

Error Handling
On fail move the file to the failed transmissions location.

Naming and Configuration

BizTalk
Package Name: Tesco_TOM_Direct_Store_Order_For_RMS
Stored Procedure
Name

<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



Environment and Security Context
 Account details will be included here once we have visibility of the environments. 

Non-Functional Requirements
No Such requirement till time of writing this document.

Processing required in the Messaging Stage of the interface
Scope
BizTalk orchestration monitors the Direct Store order file arrival, which is created by Unix Korn Shell Scripts in the shared location in (IBM AIX Server) for every new data file and submits the same after re-naming it for upload. In turn this file will be updated into RMS through tsl_gfo_upl_dts.pc program.

Data Validation
No Validation required.

Filtering
There is no filtering requirement.

Mapping
Mapping document and physical mapping in BizTalk is not required for this interface. BizTalk RTI file adaptor will be capable of transferring the file from one location to another location just a name change of the file.

Target Message Schema
Field Name
Record Type
Data Type & Size
Starting Position
Description
JIROA-RMS-ORD-HDR
01


Procurement/Final  Order Header Record Section
JIROA-REC-TYPE
   03
PIC X
1
Header Record Type
JIROA-HEADER-RECORD
     88
VALUE "0"

Header record value = “0”
JIROA-DETAIL-RECORD
     88
VALUE "1"

Detail  record value = “1”
JIROA-TRAILER-RECORD
     88
VALUE "9"

Trailer record value = “9”
JIROA-EXTRACT-DATE
   03
PIC 9(8)
2
Data Extraction Date
JIROA-EXTRACT-TIME
   03
PIC 9(6)
10
Data Extraction Time
JIROA-SEQUENCE-NO
   03
PIC 9(10)
16
Header Sequence No
FILLER
   03
PIC X(125)
26
Set to Spaces
JIROB-RMS-ORD-REC.
01


Detail Record Section
JIROB-REC-TYPE
   03
PIC X
1
Detail Record Type
JIROB-HEADER-RECORD
     88
VALUE "0"

Header record value = “0”
JIROB-DETAIL-RECORD
     88
VALUE "1"

Detail  record value = “1”
JIROB-TRAILER-RECORD
     88
VALUE "9"

Trailer record value = “9”
JIROB-BASE-PRODUCT-NO
   03
PIC 9(9)
2
TPNB
JIROB-STOCK-CENTRE-NO
   03
PIC 9(10)
11
Distribution Centre
JIROB-RMS-SUPPLIER
   03
PIC 9(10)
21
Supplier Code
JIROB-REQ-DELIVERY-DATE
   03
PIC 9(8)
31
Delivery date into store
JIROB-LM-ORD-TYPE
   03
PIC X
39
Order type
JIROB-EXTR-CONT-IND
   03
PIC X
40
Indicator to signify whether the order is Extracted ‘1’ or Contingency ‘2’
JIROB-RETAIL-OUTLET-NO
   03
PIC 9(5)
41
Store number
JIROB-RO-FCST-QTY
   03
PIC +9(9).99
46
Requested quantity in relevant Unit of Measure, e.g. kg, singles
JIROB-ACT-QTY
   03
PIC +9(9).99
59
Actual quantity after stock share
JIROB-PBL-IND
   03
PIC X
72
Indicator to signify replenishment mode
1 = Pick By Line
2 = Pick By Store
3 = Direct to Supplier
JIROB-PBL-TYPE-IND
   03
PIC X
73
Pick By Line indicator 
1 = procurement
2 = final
JIROB-RAW-QTY
   03
PIC +9(9).99
74
Raw demand quantity, i.e.
what the store actually requested before rounding
JIROB-UNIT-SIZE-X.
   03



JIROB-UNIT-SIZE
     05
PIC 9(5).99
87
Case size

JIROB-TRADTPN
   03
PIC 9(9)
95

JIROB-GFO-ORD-NO
   03
PIC 9(9)
104
GFO-generated order number 
JIROB-RMS-ORD-NO
   03
PIC 9(10)
113
Purchase Order or Transfer number from RMS 
JIROB-RMS-ORD-NO-X REDEFINES JIROB-RMS-ORD-NO
   03
PIC X(10)

Order group code – used when the file is passed back
JIROB-RMS-REASON-CD
   03
PIC X(10)
123

JIROB-ORDER-GROP         
   03
PIC XX
133
Order Group
FILLER
   03
PIC X(16)
135
Set to Spaces
JIROZ-RMS-ORD-TRLR.
01 


Trailer Record Section
JIROZ-REC-TYPE
   03
PIC X
1
Trailer Record Type
JIROZ-HEADER-RECORD
     88
VALUE "0"

Header record value = “0”
JIROZ-DETAIL-RECORD
     88
VALUE "1"

Detail  record value = “1”
JIROZ-TRAILER-RECORD
     88
VALUE "9"

Trailer record value = “9”
JIROZ-REC-COUNT
   03
PIC 9(10)
2
Total Record Count in the file
FILLER
   03
PIC X(139)
12
Set to Spaces

Message Format
The source message is from GFO is in the form of positional flat file and is getting renamed at target location.
Message Transport Details 
For messages destined for TIMS system, the following applies.	

Feature
Specification
Additional Information
Source System Name
Biztalk 2006

Source Platform / OS
Biztalk 2006 Server

Source Physical Location
RMS_Input

Source Underlying Data Storage Technology
RDBMS

Target System Name
RMS

Target Platform / OS
IBM AIX

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
RTI File Adaptor			
File Drop (Windows) 		
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
Not yet decided

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

Biztalk
Instruction Name: Tesco_TOM_Direct_Store_Order_for_RMS_File_Delivery
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
Port Details
Receive Port

Receive Location

Receive Pipeline

Transport

Message Type

Receive Folder

Batch

No. of Messages

Max. Batch Size

Operational Details
Worker Threads

Priority

Period

Retry Attempts

Timeout

Require Data Send

Exception Management

Treat Fatal Adapter Exception As

Treat Unhandled Exceptions As





Environment and Security Context
Messaging will happen through BizTalk. The BizTalk2006 EAI tool will be set with the Environment specification (will be defined)


Account details will be included here once we have visibility of the environments.

Non-Functional Requirements
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
Assumptions





Outstanding Issues
ID
Issue
To be addressed by
1
Target File name and Shared folder location to be confirmed

2
Process which will update RMS from the flat file data coming out from BizTalk to be conformed.

3
Error handling at the destination side






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
ORMS
Oracle Retail Merchandising System
As same as above
GFO
Global Forecasting and Ordering
GFO is the brain of TESCO ordering procedure, which will advise RMS, Storeline for the Direct Store Order of quantity. 



	
Document Control
Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
16-Jan-2006
0.1D
Draft











Related Documents

Author	
Date
Version
Title
<to be Filled up>

















Distribution

Name
Position
Approver/Contributor/Other
Nathan Smith
Enterprise Architect

Rob McDonagh
Solution Architect

David Onyett
Project Lead






















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version: 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT v of  NUMPAGES 22	Date:  SAVEDATE \@ "d MMM yyyy" 7 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.1 REF DOC_VER , Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 14 of  NUMPAGES 22	Date:  SAVEDATE \@ "d MMM yyyy" 7 Feb 2007




























































