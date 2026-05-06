		









`


TOM Integration

Interface Specification
Store Inventory Report Data
From RMS to TIMS


[D028]






Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
26/12/2006
Version:
0.3
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:
Nitin Singhai

Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
27-Dec-2006
V0.1D
Draft
Supriyo Chakraborty
29-Dec-2006
V0.2D
Draft
Sankar G
09-Jan-2007
V0.3D
Draft









Reviewers

Name
Date
Version
Position
Sankar G
27-Dec-2006
V0.1D
Review
Sankar G
31-Dec-2006
V0.2D
Review
Nitin Singhai
09-Jan-2007
V0.3D
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
Sankar G


Venkateswara Rao















Document Source

Related Documents:
Directory: Operations Guide\Volume 1 - Batch Overviews and Designs\
File Name: rms-120-og1
1. Oracle® Retail Merchandising System ORMS Operations Guide – Release 12.0 (Electronic Data Interchange  Sales and Stock Report Download).


Information Architecture Context diagram
Will be provided

Mapping spreadsheet
Will be provided
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc156135575 \h 6
1.1	Purpose of Document	 PAGEREF _Toc156135576 \h 6
1.2	Background	 PAGEREF _Toc156135577 \h 6
1.3	Scope	 PAGEREF _Toc156135578 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc156135579 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc156135580 \h 7
2.2	Architecture	 PAGEREF _Toc156135581 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc156135582 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc156135583 \h 9
3.1	Scope	 PAGEREF _Toc156135584 \h 9
3.2	Source Message Schema	 PAGEREF _Toc156135585 \h 9
3.3	Sample Source Message	 PAGEREF _Toc156135586 \h 10
3.4	Message Transport Details	 PAGEREF _Toc156135587 \h 11
3.5	Naming and Configuration	 PAGEREF _Toc156135588 \h 11
3.6	Environment and Security Context	 PAGEREF _Toc156135589 \h 11
3.7	Non-Functional Requirements	 PAGEREF _Toc156135590 \h 12
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc156135591 \h 13
4.1	Scope	 PAGEREF _Toc156135592 \h 13
4.2	Data Validation	 PAGEREF _Toc156135593 \h 13
4.3	Filtering	 PAGEREF _Toc156135594 \h 13
4.4	Mapping	 PAGEREF _Toc156135595 \h 13
4.5	Target Message Schema	 PAGEREF _Toc156135596 \h 13
4.6	Sample Target Message	 PAGEREF _Toc156135597 \h 13
4.7	Message Transport Details	 PAGEREF _Toc156135598 \h 14
4.8	Naming and Configuration	 PAGEREF _Toc156135599 \h 15
4.9	Environment and Security Context	 PAGEREF _Toc156135600 \h 15
4.10	Non-Functional Requirements	 PAGEREF _Toc156135601 \h 16
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc156135602 \h 17
5.1	Scope	 PAGEREF _Toc156135603 \h 17
5.2	Data Validation	 PAGEREF _Toc156135604 \h 17
5.3	Filtering	 PAGEREF _Toc156135605 \h 17
5.4	Mapping	 PAGEREF _Toc156135606 \h 17
5.5	Target Message Schema	 PAGEREF _Toc156135607 \h 17
5.6	Message Transport Details	 PAGEREF _Toc156135608 \h 17
5.7	Naming and Configuration	 PAGEREF _Toc156135609 \h 17
5.8	Environment and Security Context	 PAGEREF _Toc156135610 \h 17
5.9	Non-Functional Requirements	 PAGEREF _Toc156135611 \h 17
6	Testing Deliverables	 PAGEREF _Toc156135612 \h 18
7	Deployment	 PAGEREF _Toc156135613 \h 19
8	Assumptions and Outstanding Issues	 PAGEREF _Toc156135614 \h 20
8.1	Assumptions	 PAGEREF _Toc156135615 \h 20
8.2	Outstanding Issues	 PAGEREF _Toc156135616 \h 20
Appendix A Volumes	 PAGEREF _Toc156135617 \h 21
Appendix B Glossary	 PAGEREF _Toc156135618 \h 22
Appendix C Document Control	 PAGEREF _Toc156135619 \h 23

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Store Inventory Report data between Retek Merchandising System (RMS) and Tesco Internet Management System (TIMS). In turn these details will be published to Suppliers for their corresponding products via TIMS.

This interface is only for US integration.
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including RMS and TIMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture, there is a set of interfaces that has been identified to be developed to transfer Inventory Report data from RMS into TIMS.
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
The interface is a batch extract of Store Inventory Report data, from RMS and transforms and uploads into the TIMS system via integration layer. The Upload is a full upload in nature. The transform is a record order change. The interface is meant to run at a pre-configured time interval, which on completion is expected to produce a pipe | delimited flat-file (containing Store Inventory data records) onto the shared location. This shared location would be monitored by TIMS system at the same interval. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into TIMS.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture

Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be decided
Performance Requirements
The interface should be capable of extracting data (stock information data from RMS) from the shared source location and delivering the resulting to TIMS. The Performance will be decided based on volume of data for transformation and upload.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. There will only ever be a single instance of the RMS and TIMS in a TOM implementation and therefore no requirement for multiple files to multiple locations.
Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. 
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
No such requirement is known till point of writing this interface. 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope
The Inventory Report data will be populated by Pro-C program as part of EDI batch process in a shared location. Once the file creation is completed, the Retek scheduler will create a signature file. This signature file is an indicator file for BizTalk to pickup the inventory report for Process. BizTalk will process the file from RMS and create a new file (with | Delimited) and send it to TIMS shared location. TIMS interface will pickup the delimited file which is created by BizTalk for further processing to show the Inventory data in the Web interface which is created for TESCO suppliers. 
Source Message Schema
The Pro-C program which part of EDI batch Process will create the inventory report file required for other systems. The structure of the file will be finding below.

Record Name
Field Name
Field Type
Default Value
	Description
FHEAD
File record descriptor
Char(5)
FHEAD
Describes record type
Line number
Number(10)
0000000001
Sequential file line number
File source
Char(5)
DLPRD 
File Type
File create date
Char(8)
Period.vdate
Vdate in YYYYMMDD format
Begin Sub-Group ‘A’

1:*
THEAD will repeat multiple times under FHEAD
THEAD
File record descriptor
Char(5)
THEAD
Identifies record type
Line number
Number(10) 
		
Sequential file line number
Transaction number
Number(10)
	
Sequential transaction number
Report date
Char(8)
	
Vdate-lag days between reporting (vdate if supplier reports weekly) in YYYYMMDD format
Supplier
Number(10)

Supplier Number
Begin Sub-Group ‘AA’

1:*
TITEM will repeat multiple times under TITEM
TITEM
File record descriptor
Char(5)
TITEM
Identifies file record type
Line number
Number(10)

Sequential file line Number
Transaction number
Number(10)

Sequential transaction Number
Item
Char(25)

Item
Item_Num_Type
Char(6)

Item Number Type
Ref_Item
Char(25)

Reference item
Ref_Item_Num_Type
Char(6)

Reference Item Number Type
Vendor catalog Number
Char(30)

VPN (Vendor Product Number)
Item description
Char(250)

Item description (item desc)
Begin Sub-Group ‘AAA’

1:*
TQUTY will repeat maximum 3 times under TITEM depending on the Quantity descriptor field for a particular item and location.
TQUTY
File record descriptor
Char(5)
TQUTY
Identifies record type
Line number
Number(10)

Sequential file line Number
Transaction number
Number(10)

Sequential transaction Number
Quantity descriptor
Char(15)

‘On-hand’ (stock)/’Sold’(sales)/’In transit’
Location type
Char(2)

‘ST’for store or ‘WH’ Warehouse
Location
Number(10)

Store or warehouse Number
Unit cost
Number(20)

Unit cost (4 implied decimal places) from item_supp_country_loc table (in supplier currency)
Quantity
Number(12)

Quantity – 4 implied decimal places
End Sub-Group ‘AAA’



End Sub-Group ‘AA’



End Sub-Group ‘A’



TTAIL
File record descriptor
Char(5)
TTAIL
Identifies record type
Line number
Number(10)

Sequential file line Number
Transaction lines
Number(6)

Number of lines for this Transaction
FTAIL
File record descriptor
Char(5)

Identifies record type
Line number
Number(10)

Total number of lines in file.
Number of transaction lines
Number(10)

Number of transaction lines in file.
Sample Source Message
The source message is in the form of positional flat file from RMS and is getting converted into the target file format in a package. The following sample message format is the source message format. 

FHEAD0000000001DLPRD20061212
THEAD00000000010000000001200612120123456789
TITEM00000000010000000001123456789                IAN   123456788               EAN   8901234567890                 COCO-COLA 1 LTR                                                                                                                                                                                                                                                     
TQUTY00000000010000000001On-hand        ST0000012345000000000000001.12300000123.0000
TQUTY00000000020000000001sold           ST0000012345000000000000001.12300000300.0000
TQUTY00000000020000000001In transit     ST0000012345000000000000001.12300000400.0000
TTAIL0000000001000001
THEAD00000000020000000001200612120123456789
TITEM00000000020000000001123456789                IAN   123456788               EAN   8901234567890                 COCO-COLA 1 LTR                                                                                                                                                                                                                                                     
TQUTY00000000020000000001On-hand        ST0000012346000000000000001.12300000132.0000
TQUTY00000000020000000001sold           ST0000012346000000000000001.12300000200.0000
TQUTY00000000020000000001In transit     ST0000012346000000000000001.12300000100.0000
TITEM00000000020000000001123456787                IAN   123456788               EAN   8901234567980                 COCO-COLA 2 LTR                                                                                                                                                                                                                                                     
TQUTY00000000020000000001On-hand        ST0000012346000000000000001.12300000123.0000
TQUTY00000000020000000001sold           ST0000012346000000000000001.12300000500.0000
TQUTY00000000020000000001In transit     ST0000012346000000000000001.12300000900.0000
TTAIL0000000002000002
THEAD00000000030000000001200612120123456789
TITEM00000000030000000001123456789                IAN   123456788               EAN   8901234567890                 COCO-COLA 1 LTR                                                                                                                                                                                                                                                     
TQUTY00000000030000000001On-hand        ST0000012347000000000000001.12300000123.0000
TQUTY00000000020000000001sold           ST0000012347000000000000001.12300000100.0000
TQUTY00000000020000000001In transit     ST0000012347000000000000001.12300000300.0000
TTAIL0000000003000001
THEAD00000000040000000001200612120123456789
TITEM00000000040000000001123456789                IAN   123456788               EAN   8901234567890                 COCO-COLA 1 LTR                                                                                                                                                                                                                                                     
TQUTY00000000040000000001On-hand        ST0000012348000000000000001.12300000123.0000
TTAIL0000000004000001
THEAD00000000050000000001200612120123456789
TITEM00000000050000000001123456789                IAN   123456788               EAN   8901234567890                 COCO-COLA 1 LTR                                                                                                                                                                                                                                                     
TQUTY00000000050000000001On-hand        ST0000012349000000000000001.12300000123.0000
TTAIL0000000005000001
THEAD00000000060000000001200612120123456789
TITEM00000000060000000001123456789                IAN   123456788               EAN   8901234567890                 COCO-COLA 1 LTR                                                                                                                                                                                                                                                     
TQUTY00000000060000000001On-hand        ST0000012340000000000000001.12300000123.0000
TTAIL0000000006000001
FTAIL00000000010000000035
Message Transport Details
Feature
Specification
Additional Information
Source System Name
RMS

Source Platform / OS
IBM AIX

Source Physical Location


Source Underlying Data Storage Technology
File Share

Target System Name


Target Platform / OS
SQL Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
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
Not yet decided

Archiving
There is no requirement to archive the messages.

Logging
Logging should occur, such that the message can be recreated if necessary.

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

BizTalk
Package Name: Tesco_TOM_Integration_Extract_Inventory_File_for_TIMS
BizTalk Procedure
Name
USP_Tesco_TOM_Integration_Extract_Inventory
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable



Processing required in the Messaging Stage of the interface
Scope
BizTalk will collect the flat file/Files created by RMS at the shared location as input. This RMS Inventory data will get transformed and messaged to the target location where TIMS system will pool for the file. 
Data Validation
There is no data validations requirement.
Filtering
From the Inventory report produced by RMS will carry Stock on Hand, Stock in transit & Sold details of an Item. Only Stock on hand & Stock in transit data will be filtered and messaged out to TIMS.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Code
Optional
Type
Description
IR Header:
Record type

VARCHAR2(1)
=H
Inventory report date

DATE
YYYYMMDD
STONMAG

NUMBER(5)
Shop ID
STOCNUF

NUMBER(9)
Gold supplier ID
STODEPT

NUMBER(2)
Supplier department
Begin Sub-Group ‘A’
1:*
IRItems will repeat multiple times under IRHeader
IR Items:
Record type

VARCHAR2(1)
=L
EAN_ID

VARCHAR2(13)
Article EAN
SALES
Yes
NUMBER(20.3)
Sales in units 
STOCK
Yes
NUMBER(20.3)
Day’s closing stock
RECEIPTS
Yes
NUMBER(20.3)
Received units
OTHER
Yes
NUMBER(20.3)
Stock adjustments
STOCK_ON_ORDER
Yes
NUMBER(20.3)
Stock ordered but not received yet
ARTLIBL
Yes
VARCHAR2(30)
Article name
TPN
Yes
VARCHAR2(13)
TESCO Product Number
SPN
Yes
VARCHAR2(13)
SPN
End Sub-Group ‘A’



Sample Target Message
The source message is from RMS and is getting converted into the target file format in a package. The following message format is the target message format. 

H|20061212|12345|123456789|00
L|123456788|8901234567890|0000000000000000.000|0000000000000123.000|0000000000000000.000|0000000000000000.000|0000000000000400.000|COCO-COLA 1 LTR                        |1234567898901|2345678900123
H|20061212|12346|123456789|00
L|123456788|8901234567890|0000000000000000.000|0000000000000132.000|0000000000000000.000|0000000000000000.000|0000000000000100.000|COCO-COLA 1 LTR                        |1234567898901|2345678900123
L|123456787|8901234567980|0000000000000000.000|0000000000000132.000|0000000000000000.000|0000000000000000.000|0000000000000900.000|COCO-COLA 1 LTR                        |1234567898901|2345678900123
H|20061212|12347|123456789|00
L|123456787|8901234567980|0000000000000000.000|0000000000000123.000|0000000000000000.000|0000000000000000.000|0000000000000000.000|COCO-COLA 1 LTR                        |1234567898901|2345678900123
H|20061212|12348|123456789|00
L|123456787|8901234567980|0000000000000000.000|0000000000000123.000|0000000000000000.000|0000000000000000.000|0000000000000000.000|COCO-COLA 1 LTR                        |1234567898901|2345678900123
H|20061212|12349|123456789|00
L|123456787|8901234567980|0000000000000000.000|0000000000000123.000|0000000000000000.000|0000000000000000.000|0000000000000000.000|COCO-COLA 1 LTR                        |1234567898901|2345678900123
H|20061212|12340|123456789|00
L|123456787|8901234567980|0000000000000000.000|0000000000000123.000|0000000000000000.000|0000000000000000.000|0000000000000000.000|COCO-COLA 1 LTR                        |1234567898901|2345678900123

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


Source Underlying Data Storage Technology
File System

Target System Name
TIMS

Target Platform / OS
LINUX

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		

Data Format

XML  				
Delimited 			
Positional 			

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
Instruction Name: Tesco_TOM_Inventory_Report_for_TIMS_File_Delivery
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
Account details will be included here once we have visibility of the environments.


Non-Functional Requirements
On successful delivery of the file to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure the file should be written to the failed files location, and an alert should be raised.


Processing required in the <third stage of the interface>
Scope
There is no intermediate staging is required for this interface. So this section is not applicable.

Data Validation
Not applicable

Filtering
Not applicable

Mapping
Not applicable

Target Message Schema
Not applicable

Message Transport Details
Not applicable

Naming and Configuration
Not applicable

Environment and Security Context
Not applicable

Non-Functional Requirements
Not applicable
Testing Deliverables
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
This is Transaction record identifier. This string will get inserted at the beginning of every new supplier details.
TITEM
Item Detail Record
This is Item record identifier. This string will get inserted at the beginning of every new item transaction for a supplier.
TQUTY
Quantity Detail Record
This is Quantity detail record identifier. This string will get inserted at the beginning of every Item Quantity. Quantity descriptor column will identify the nature of this transaction.
TTAIL
Transaction Tail Record
This is Transaction tail record identifier.  This string will get inserted at the beginning of every transaction tail record to identify end of Supplier’s Items transaction. 
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
27-Dec-2006
V0.1D
Draft
Supriyo Chakraborty
29-Dec-2006
V0.2D
Draft
Sankar G
09-Jan-2007
V0.3D
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
Nathan Smith
Enterprise Architect

Andrew Barker
Engagement Architect

David Onyett
Project Lead






















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 9 of  NUMPAGES 23	Date:  SAVEDATE \@ "d MMM yyyy" 15 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































