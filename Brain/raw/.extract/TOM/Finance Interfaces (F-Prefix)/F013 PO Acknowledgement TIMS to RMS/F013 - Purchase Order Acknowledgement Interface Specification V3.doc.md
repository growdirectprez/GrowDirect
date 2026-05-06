		









`


TOM Integration

Interface Specification
Purchase Order Acknowledgement Data
From TIMS to RMS


[F013]






Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
27/12/2006
Version:
0.3
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:
Sankar G

Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
27/12/2006
0.1D
Draft
Supriyo Chakraborty
29/12/2006
0.2D
Draft
Sankar G
04/01/2007
0.3D
Draft





Reviewers

Name
Date
Version
Position
Sankar G
27/12/2006
0.1D
Review
Sankar G
31/12/2006
0.2D
Review
Supriyo Chakraborty
04/01/2007
0.3D
Review






At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Andrew Barker
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
Andrew Barker
<Issue Date>
<Version No>
David Onyett


Venkateswara Rao









Document Source

Related Documents:
Directory: Operations Guide\Volume 1 - Batch Overviews and Designs\
File Name: rms-120-og1

1. Oracle® Retail Merchandising System ORMS Operations Guide – Release 12.0  Electronic Data Interchange  Supplier Order Acknowledgement and Changes.

Information Architecture Context diagram
Will be provided

Mapping spreadsheet
Will be Provided
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
The purpose of this document is to describe the interfacing requirements w.r.t the Purchase Order Acknowledgement data between Tesco Internet Management System (TIMS) and Retek Merchandising System (RMS).

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including TIMS and RMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Purchased Order Acknowledgement data from TIMS into RMS.

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
The interface is to upload the Purchase Order Acknowledgement data from TIMS into RMS via EDI batch process. The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the PO Acknowledgement data (delimited by |) from TIMS interface. On completion of this process expected to produce a positional flat file (containing PO Acknowledge data records) required for RMS onto the shared location. This output file will get transferred to RMS location via XCOM. In turn the transferred file which is produced by this interface will be further processed by EDI batch of RMS and load the data (updates/inserts) into RMS.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture
 SHAPE  \* MERGEFORMAT 


Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data in the form of flat file from the shared location at TIMS side and delivering the resulting to another shared location at RMS side before the identified cut-off time. The interface should run on real time basis. 
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
TIMS creates a pipe | delimited flat file on real time basis whenever it receives an order acceptance data from the supplier. TIMS produces the flat file at a predefined shared location. Biztalk in turn picks up the file from the same location and produces a positional flat file at another predefined shared location. 

Source Message Schema
Code
Optional
Type
Description
PO ACK Header:
RECTYPE

CHAR(1)
Type of record “H”
ECONCOM

NUMBER(8)
purchase order ID
ECOCNUF

NOT NULL NUMBER(9)
supplier ID
ECODSND
Y
CHAR(14)
Time, when Preorder was deliver to supplier (YYYYMMDDHH24MISS)
ECODREC

CHAR(14)
Time, when Preorder was confirmed by supplier (Written date in RMS?)
(YYYYMMDDHH24MISS)
ECOSTAT

NUMBER(1)
Order confirmation status: 0)      Order fully confirmed 1)      Partially confirmed 2)      Fully rejected 
PO ACK Items:
RECTYPE

CHAR(1)
Type of record “L”
EAN_ID

CHAR(13)
Cash register article code, EAN/UPC/GS1 code
DCOQTEC

NUMBER(9,3)
quantity ( selling unit )
DCOLOC

NUMBER(10)
location
DCOLOCT

CHAR(2)
Location Type
=”ST”
=”WH”
ARCRCOM

CHAR(30)
SPN



Message Format
The source message is in the form of pipe m| delimited file from TIMS is getting converted into the target file format in a package. The following sample message format is the source message format. 

H|00345019|012345678|20061230121000|20061231091500|0
L|123456789|00450.000|01000.000
L|234567890|00350.000|02230.000
L|345678901|00600.000|03000.000
H|00345020|012341234|20061230131500|20061231091700|1
L|123123123|01200.000|01000.000
L|234234234|03000.000|01500.000
Message Transport Details

Feature
Specification
Additional Information
Source System Name
TIMS

Source Platform / OS
LINUX

Source Physical Location


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
FTP			
File Drop(Windows) 	
                 (XCOM) 	

Data Format.
XML			
Delimited		
Positional		

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
Logging should occur, such that the message can be recreated if necessary.

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

Biztalk – 2006
Package Name: Tesco_ TOM_Integration_PO_ACK_for_RMS
BizTalk Procedure
Name
Tesco_TOM_Integration_PO_ACK
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
Biztalk monitors the file in the configured location for every new file and submits the same to the remote UNIX share via FTP. The resultant file is a positional flat file.
Data Validation
Data Validation will be done by the target RMS system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Record 
Name
Field Name

Field Type

Default
Value
Description

FHEAD

File head
descriptor

Char(5)

FHEAD

Describes file line type.

Line id
Number(10)
0000000001
Sequential file line number

File Type
Definition

Char(4)

ORAK

Identifies file as ‘Order
Acknowledgment Import’.
THEAD

File record
descriptor

Char(5)

THEAD

Describes file line type

Line id

Number(10)

Line number
in file

Sequential file line number

Transaction
number

Number(10)


Sequential transaction
number

Acknowledge
type

Char(2)


AP-product replenishment
AK- Acknowledge or change
CA-cancel order (no detail)

Order number

Char(15)


May be external order
number (vendor order
number) OR Oracle Retail
order number

Written_date

Char(8)


Written date in
YYYYMMDD format

Supplier
number

Number(10)


Supplier number

Not before date

Char(8)


Not_before_date
YYYYMMDD

Not after date

Char(8)


Not_after_date
YYYYMMDD

Purchase type

Char(6)


Specifies type of purchase –
may be blank

Pickup date

Char(8)


Pickup_date YYYYMMDD
– may be blank

TITEM

File record
descriptor

Char(5)

TITEM

Describes file line type

Line id

Number(10)

Line number
in file

Sequential file line number

Transaction
number

Number(10)


Sequential transaction
number

ITEM

Char(25)


Item (either item or ref_item
must be defined)

Ref_item

Char(25)


Reference item (either item
or ref_item must be defined)

Vendor catalog
number

Char(30)


VPN (Vendor Product
Number)

Unit cost value

Number(20)


Unit_cost * 10000 (4 implied
decimal places)

Loc_type

Char(2)


‘ST’ for store, ‘WH’ for
warehouse

Location

Number(10)


If NULL, apply to all
locations for this item.

Pickup
location

Char(250)


Location to pick up item –
may be blank

TSHIP

File record
descriptor

Char(5)

TSHIP

Describes file line type

Line id

Number(10)

Line number
in file

Sequential file line number

Transaction
number

Number(10)


Sequential transaction
number

Store/wh
indicator

Char(2)


‘ST’ for store, ‘WH’ for
warehouse

Ship to
location

Number(10)


Store or warehouse number

Quantity

Number(12)


Quantity ordered * 10000 (4
implied decimal places)

TTAIL

File record
descriptor

Char(5)

TTAIL

Describes file line type

Line id

Number(10)

Line number
in file

Sequential file line number

Transaction
number

Number(10)


Sequential transaction
number

Lines in
transaction

Number(6)


Total number of lines in this
transaction

FTAIL

File record
descriptor

Char(5)

FTAIL

Marks end of file

Line id

Number(10)

Line number
in file

Sequential file line number

Number of
transactions

Number(10)


Number of lines between
FHEAD and FTAIL


Message Format
The source message is a pipe | delimited flat file from TIMS and is getting converted into the target file format for RMS in a package. The target message is a positional flat file. 

Sample message format
FHEAD0000000001ORK
THEAD00000000010000000001AKPOXYZ00000000012007010200000000012007011520070201      20070129
THEAD00000000020000000001APPOXYZ00000000012007010200000000012007011520070201      20070129
TITEM00000000010000000001            SD01000000021                         XX                          XX00000000000012005000ST0000000010                                                                                                                                                                                                                                                          
TITEM00000000020000000001            SD01000000031                         XX                          XX00000000000024005000WH0000000010                                                                                                                                                                                                                                                          
TSHIP00000000010000000001ST0000000010000000100000
TSHIP00000000020000000001WH0000000020000000100000
TTAIL00000000010000000001000001
TTAIL00000000010000000001000001
FTAIL00000000010000000001
FTAIL00000000010000000001

4.7 Message Transport Details 
For messages destined for RMS system, the following applies.	

Feature
Specification
Additional Information
Source System Name
Biztalk 2006

Source Platform / OS
Biztalk 2006 Server

Source Physical Location


Source Underlying Data Storage Technology
File System

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
FTP						
File Drop (Windows) 		
                 (XCOM) 		

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

Biztalk 2006
Instruction Name: Tesco_TOM_Integration_PO_ACK_File_Delivery
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
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
The input file from RMS is assumed to be less than 10MB in size. Technology expert says that Messaging more than 10 MB through BizTalk is not advisable.



Outstanding Issues
ID
Issue
To be addressed by
1
File naming format to be confirmed
Andrew Barker
2
Server Physical Location of the server and file 
Andrew Barker
3
Error handling
Andrew Barker
4




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
TIMS
TESCO Internet Management System
TESCO Internet Management System is a gateway for the TESCO suppliers to access the data and give their responses. For TIMS the main data feed will be from RMS.
FHEAD
File Header Record
This is File header record identifier. This string will get inserted at the beginning of the file. 
THEAD
Transaction Header Record
This is Transaction record identifier. This string will get inserted at the beginning of every new purchaser order acknowledgement transaction.
TITEM
Item Detail Record
This is Item record identifier. This string will get inserted at the beginning of every new item transaction within a purchase order.
TSHIP
Shipping Detail Record
This is Shipping detail record identifier. This string will get inserted at the beginning of every shipping detail record against the Item record within a purchase order.
TTAIL
Transaction Tail Record
This is Transaction tail record identifier.  This string will get inserted at the beginning of every transaction tail record to identify end of Purchase Order transaction. 
FTAIL

File Tail Record
This is File tail record identifier. This stringed record will get inserted to identify the end of file.   

Document Control
Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
27/12/2006
0.1
















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
Nathan Smith
Enterprise Architect

Andrew Barker
Engagement Architect

David Onyett
Project Lead

























	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 9 of  NUMPAGES 23	Date:  SAVEDATE \@ "d MMM yyyy" 4 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































