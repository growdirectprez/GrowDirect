		









`


TOM Integration

Interface Specification
Directs PO
From RMS to Storeline


[D016TR]






Project BEN Code:

Author:Allister GreenDate:
23/02/2007
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
Allister Green
23/02/2007
0.1
First Draft













Reviewers

Name
Date
Version
Position


















At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
<Business Owner/Customer>
Position
<Relationship to the Programme> e.g. Stakeholder
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
Clear Case



Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents:  


Information Architecture Context diagram
To complete

Mapping spreadsheet
POs to Storeline v1.5.5.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 6
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 6
1.2	Background	 PAGEREF _Toc153956171 \h 6
1.3	Scope	 PAGEREF _Toc153956172 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 7
2.2	Architecture	 PAGEREF _Toc153956175 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153956177 \h 9
3.1	Scope	 PAGEREF _Toc153956178 \h 9
3.2	Source Message Schema	 PAGEREF _Toc153956179 \h 9
3.3	Message Transport Details	 PAGEREF _Toc153956180 \h 9
3.4	Naming and Configuration	 PAGEREF _Toc153956181 \h 10
3.5	Environment and Security Context	 PAGEREF _Toc153956182 \h 10
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153956183 \h 11
4.1	Scope	 PAGEREF _Toc153956184 \h 11
4.2	Data Validation	 PAGEREF _Toc153956185 \h 11
4.3	Filtering	 PAGEREF _Toc153956186 \h 11
4.4	Mapping	 PAGEREF _Toc153956187 \h 11
4.5	Target Message Schema	 PAGEREF _Toc153956188 \h 11
4.6	Message Format	 PAGEREF _Toc153956189 \h 12
4.7	Message Transport Details	 PAGEREF _Toc153956190 \h 13
4.8	Naming and Configuration	 PAGEREF _Toc153956191 \h 14
4.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 14
4.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 15
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153956194 \h 16
5.1	Scope	 PAGEREF _Toc153956195 \h 16
5.2	Data Validation	 PAGEREF _Toc153956196 \h 16
5.3	Filtering	 PAGEREF _Toc153956197 \h 16
5.4	Mapping	 PAGEREF _Toc153956198 \h 16
5.5	Target Message Schema	 PAGEREF _Toc153956199 \h 16
5.6	Message Transport Details	 PAGEREF _Toc153956200 \h 16
5.7	Environment and Security Context	 PAGEREF _Toc153956201 \h 16
6	Testing Deliverables	 PAGEREF _Toc153956202 \h 17
7	Deployment	 PAGEREF _Toc153956203 \h 18
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 19
8.1	Assumptions	 PAGEREF _Toc153956205 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 19
Appendix A Volumes	 PAGEREF _Toc153956207 \h 20
Appendix B Glossary	 PAGEREF _Toc153956208 \h 21
Appendix C Document Control	 PAGEREF _Toc153956209 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of PO (Purchase Order) data for directs only between the Retail Management System (RMS) and Storeline.

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for Turkey only.

Background
As part of the shipment of goods notification and acknowledgement process, RMS will create PO data files (when ??) detailing goods that are being delivered to stores directly by supplier. Each PO data file can contain multiple PO’s for multiple stores. Each PO within the PO data file will contain a list of goods (at either pack or item level) which are being delivered to a particular store.

This interface will transport the PO data file to the Integration Layer (IL), extract each purchase order into separate files, and transport each file to the relevant store, ready for upload into Storeline.

As well as containing ‘create’ PO’s (record type ‘352’), the PO Data file may contain PO records intended to cancel a previously sent PO. These ‘delete’ PO’s (record type ‘351’) 

Scope
This interface is for Turkey only, and details the transports of PO data from RMS to Storeline only for direct deliveries to store from supplier. 

PO’s for DC deliveries are NOT covered by this interface.

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
A Biztalk orchestration within the Integration Layer will:
Load the PO data file produced by RMS immediately upon it being produced,
RMS will place file in a shared CIFS directory on the RMS host, called ‘RMS_outbox’,
The file will be named ‘RMS_PODIRECT_CCYYMMDDHHmmss.dat’ (TBC), where the CCYYMMDDHHmmss is the datetime that RMS produced the file,
The file will be identified by the integration layer by name pattern ‘RMS_PODIRECT_*.dat’

Extract each PO to a separate file, in a format suitable for upload by Storeline. Each file will be for a particular store,

Extract Pack level items to SKU level using the ‘GetSinglePackBreakout’ stored procedure in the IDS

Obtain a batch number (6 characters, left padded with 0’s) for the file naming (see next point) using the GetBatchNumber method of the TOM.Common.BatchNumbers.BatchNumber class (see ??? for details). This method will simply retrieve a number one more than the last time it was called.

Create three promoted properties for each PO message sent to Storeline:
BatchNumber- 6 character numeric batch number generated by step above, left padded with zeros,
StoreNumber – 6 character numeric store id, left padded with zeros,
FileType – 3 character numeric to hold message type (‘352’ = create, ‘351’ = delete)

Send each PO message to the relevant store Storeline host using RTI shipping agent:
Target Hosted instruction: ‘PODownload’,
Adapter: RTI Legacy Instruction adapter (because Turkey is using RTI 1.0).
Target Address: ‘S’ + StoreNumber 7 digit context property, e.g. ‘S0000001’.
Hosts config file on Biztalk orchestration host contains mapping of Store identifier to actual store IP address.
Transport protocol: SOAP

The Hosted Instruction ‘PODownload’ on the store RTI host will,
Create file, named as follows:

‘STK<6-digit batchnumber>_TTT_<6 digit Store ID>_YYYYMMDDHHMMSS.dat’, where the ‘YYYYMMDDHHMMSS’ is the file create date and time, and the ‘TTT’ is the 3 digit message type (‘351’ = Create, ‘352’ = Delete).

An example is: ‘STK000712_351_001092_20061029095930.dat’.

Place file in shared directory named ?? on RTI host, ready for upload by Storeline.



This interface shares common file delivery requirements with interfaces D015. The RTI instruction ‘PODownload’ will be used by both of these interfaces.

The following points will be logged using the Trackpoint component of the IMOF framework:
Receipt of file from RMS.
File sent to Storeline.

The following errors will be raised using the Error Processing framework of IMOF:
Failure to import file from RMS into orchestration,
Failure of Pack to SKU conversion,
Failure to obtain a batch number for the file naming,
Failure of PO message creation for Storeline import,
Failure of the RTI Instruction to create PO data file on Storeline host.

At time of writing, IMOF specifications have not yet been completed, hence details of how IMOF will interface with Biztalk, RTI, etc, are to be determined.

Architecture

Add overview diag


Requirements for the End-to-End Interface

Audit Requirements
The interface will use the Trackpoint component of IMOF to log successful file transfer.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
None.
Performance Requirements
The interface needs to be capable of creating and transporting PO Receipt messages with volumes of files and data as specified by Appendix A.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
The interface needs to be able to support the continual addition of new stores.
Operational Support Requirements
Operational response will be required for alerts stated in 2.1.
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
The Integration Layer will retrieve each PO data file from the ‘RMS_outbox’ shared directory on the RMS host as soon as they appear. Each PO contained in this file will be extracted, transformed into a structure suitable for upload by Storeline, and have any pack levels details converted to SKU level.
Source Message Schema
Note the record structure of the PO file produced by RMS is as follows:

FHEAD - one per file     TORDR - one per Purchase Order ** may be multiple per FHEAD set         TITEM - one per item on the PO ** may be multiple per TORDR set            TSHIP - one per TITEM set     TTAIL - one per TORDR set FTAIL - one per file

 Record NameField NameField Type Start PosEnd PosSizeMandatoryDefault Value/Format1FHEADFile Record Type Descriptorchar155Y‘FHEAD’2 File Line Numbernumber61510Y00000000013 File Type Definitionchar163520YTSC_PODNLD4 Create Datechar36438YYYYYMMDD5 Create Timechar44496YHHMMSS6 Location Typechar50501YS = Store7 Locationnumber516010Y          1TORDRRecord descriptorChar155Y'TORDR'2 Line idChar61510Y 3 Transaction idchar162510Y 4 Order change typechar26272Y‘CH’ (changed) or ‘NW’ (new)5 Order numbernumber28358Y 6 Supplier Number364510Y 7 Vendor order idchar466015N 8 Old order written date Char617414N yyyymmddhhmm9 New order written datechar758814Y yyyymmddhhmm10 Old Currency Code Char89913N 11 New Currency Codechar92943Y 12 Old Shipment Method of payment Char95962N 13 New Shipment Method of Paymentchar97982N 14 Old Transportation Responsibility Char991002N 15 New Transportation Responsibility Char1011022N 16 Old Trans. Resp. Descriptionchar10314745N 17 New Trans. Resp. Description Char14819245N 18 Old Title Passage Location Char1931942N 19 New Title Passage Locationchar1951962N 20 Old Title Passage Descriptionchar19724145N 21 New Title Passage Descriptionchar24228645N 22 Old not before datechar28730014N yyyymmddhhmm23 New not before datechar30131414Y yyyymmddhhmm24 Old not after datechar31532814N yyyymmddhhmm25 New not after datechar32934214Y yyyymmddhhmm26 Old Purchase typechar3433486N 27 New Purchase typechar3493546Y 28 Backhaul allowancenumber35537420N 29 Old terms descriptionchar375614240N 30 New terms descriptionchar615854240N 31 Old pickup datechar85586814N yyyymmddhhmm32 New pickup datechar86988214N yyyymmddhhmm33 Old ship methodchar8838886N 34 New ship methodchar8898946N 35 Old comment descriptionchar8951144250N 36 New comment descriptionchar11451394250N 37 Supplier DUNS numbernumber139514039N 38 Supplier DUNS locationnumber140414074N          1TITEMFile record descriptor Char155Y‘TITEM’2 Line idchar61510Y 3 Transaction idchar162510Y 4 Item Number Typechar26316Y 5 Itemchar325625Y 6 Old Ref Item Number typechar57626N 7 Old Ref Itemchar638725N 8 New Ref Item Number typechar88936N 9 New Ref Itemchar9411825N 10 Vendor catalog numberchar11914830N 11 Free Form Descriptionchar149248100N 12 Supplier Diff 1char24932880N 13 Supplier Diff 2char32940880N 14 Supplier Diff 3char40948880N 15 Supplier Diff 4char48956880N 16 Pack Sizenumber56958012N          1TPACKFile record descriptorchar155Y‘TPACK’2 Line idchar61510Y 3 Transaction idchar162510Y 4 Pack idchar265025Y 5 Inner pack idchar517525N 6 Pack Quantitynumber768712Y Packitem_breakout.pack_item_qty (4 implied decimal places)7 Component Pack Quantitynumber889912N Packitem_breakout.comp_pack_qty (4 implied decimal places)8 Item Parent Part Quantitynumber10011112NPackitem_breakout.item_parent_pt_qty (4 implied decimal places)9 Item Quantitynumber11212312N Packitem_breakout.item_qty (4 implied decimal places)10 Item Number Typechar1241296Y 11 Itemchar13015425Y 12 Item Number Typechar1551606N 13 Ref Itemchar16118525N 14 VPNchar18621530N 15 Supplier Diff 1char21629580N 16 Supplier Diff 2char29637580N 17 Supplier Diff 3char37645580N 18 Supplier Diff 4char45653580  19 Item Parentchar53656025N 20 Pack templatechar5615688N 21 Template descriptionchar56960840N          1TSHIPRecord typechar155Y'TSHIP'2 Line idchar61510Y 3 Transaction idchar162510Y 4 Location typechar26272Y‘ST’ store or ‘WH’ warehouse5 Ship to locationnumber283710Y 6 Old unit costnumber385720NOld unit cost (4 implied decimal places)7 New unit costnumber587720YNew unit cost (4 implied decimal places)8 Old quantitynumber788912NOld qty_ordered or qty_allocated (4 implied decimal places)9 New quantitynumber9010112YChanged qty_ordered  (4 implied decimal places)10 Old outstanding quantitynumber10211312NOld qty_ordered-qty_received (4 implied decimal places)(or qty_allocated-qty transferred, for an allocation)11 New outstanding quantitynumber11412512YChanged qty_ordered-qty_received (4 implied decimal places)(or qty_allocated-qty_transferred, for an allocation)12 Cancel codechar1261261N 13 Old cancelled quantitynumber12713812NPrevious quantity cancelled (4 implied decimal places)14 New cancelled quantityNumber13915012NChanged quantity cancelled (4 implied decimal places)15 Quantity type flagchar1511511Y‘S’hip to ‘A’llocate16 Store or warehouse indicatorchar1521532Y‘ST’ (store) or ‘WH’ (warehouse)17 Old x-dock locationnumber15416310NAlloc_detail location (store or wh)18 New x-dock locationnumber16417310NAlloc_detail location (store or wh)19 Case lengthnumber17418512NCase length (4 implied decimal places)20 Case widthnumber18619712NCase width (4 implied decimal places)21 Case heightnumber19820912NCase height (4 implied decimal places)22 Case LWH unit of measurechar2102134NCase LWH unit of measure23 Case weightnumber21422512NCase weight (4 implied decimal places)24 Case weight unit of measurechar2262294NCase weight unit of measure25 Case liquid volumenumber23024112NCase liquid volume (4 implied decimal places)26 Case liquid volume unit of measurechar2422454NCase liquid volume unit of measure27 Location DUNS numbernumber2462549N 28 Location DUNS locnumber2552584N 29 New unit cost initnumber25927820NNew unit cost init (4 implied decimal places)30 Old unit cost initnumber27929820NOld unit cost init (4 implied decimal places)31 Item/loc discountsnumber29931820NItem/loc discounts (4 implied decimal places)         1TTAILRecord typechar155Y 'TTAIL'2 Line idchar61510Y 3 Transaction idchar162510Y 4 no of lines in transactionnumber263510Y          1FTAILRecord typechar155Y 'FTAIL'2 Line idchar61510Y 3 no of linesnumber162510Y 



Message Transport Details
Feature
Specification
Additional Information
Source System Name
RMS

Source Platform / OS
UNIX AIX

Source Physical Location
TBD

Source Underlying Data Storage Technology
Oracle

Target System Name
Biztalk

Target Platform / OS
Windows 2003 Server

Target Physical Location
TBD

Target Underlying Data Storage Technology
SQL Server 2005

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
Bulk Data		

Real-time/Scheduled Batch
Real-time

Archiving
N/A

Logging
Log via Trackpoint component of the IMOF framework.

Error Handling
Raised through the error Error Management component of the IMOF framework.


Naming and Configuration

This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

Directory and File Names
Description
Name
RMS output directory
RMS_outbox
PO Data file
RMS_PODIRECT_CCYYMMDDHHmmss.dat (TBC)


Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example employing BizTalk this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).

 
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Errors and audit points raised using the IMOF framework.


Processing required in the Messaging Stage of the interface
Scope
Each PO message created by the IL for upload to Storeline will be transported to a shared directory on the relevant store Storeline server using RTI Shipping Agent hosted instruction ‘PODownload’.

Data Validation
Data Validation will be done by the target Storeline syste.
Filtering
There is no filtering requirement.
Mapping
See the ‘Mapping’ tab of the ‘POs to Storeline v1.5.5.xls’ spreadsheet.
Target Message Schema

Note PO ‘delete’ messages (Type = ‘351’) will have no detail records.

Header

 Field Name
Type
Size
Mandatory
Notes
1
Type 
Char
1
M 
‘H'
2
Date of file extract / creation
Ccyymmdd
8
M 
 
3
Time of file extract / creation
Hhmmss
6
M 
 
4
Store No.          / From Store
Numeric
8
M 
 
5
Order Number /Transaction #
Numeric
14
M 
 
6
Record Type
Char 
3
M 
‘352' for create, '351' for delete
7
Store Name
Char
20
 
 
8
Store Address
Char
100
 
 
9
Supplier Code /       To Store
Char
8
M 
 
10
Supplier Name
Char
32
 
 
11
Supplier Address
Char
64
 
 
12
Supplier Type
Numeric 
1
 
 
13
Order Date 
Ccyymmdd
8
M 
 
14
Expected Del Date
Ccyymmdd
8
OR
 
15
Del After Date
Ccyymmdd
8
 
16
Del Before Date
Ccyymmdd
8
 
17
Transaction date & time
Ccyymmddhhmmss
14
 
 
18
Order Type/   Count Type
Numeric
8
 
 
19
Invoice Number
Char
24
 
 
20
Ref No 1
Char
24
 
 
21
Ref No 2
Char
24
 
 
22
Captured by/ Created by
Char
30
 
 
23
Driver's name/Courier
Char
30
 
 
24
Original Order number
Numeric
14
 
 
25
Remarks
Char
60
 
 
26
Reason Code
Numeric
4
 
 
27
No. of Detail Lines
Numeric
7
M 
 
28
Total Qty
Numeric (10,4)
14
 
 
29
Total Value
Numeric (7,2)
9
 
 
30
Invoice Total
Numeric (7,2)
9
 
 
31
Invoice Tax Total
Numeric (7,2)
9
 
 
32
Description
Char
20
 
 
33
User name
Char
30
 
 
34
Re-processed flag (export only)
Numeric (0/1)
1
 
 

Detail

 Field Name
Type
Size
Mandatory
Notes
1
Type 
D
1
M 
‘D'
2
Date of extract
Ccyymmdd
8
M 
 
3
Time of extract
Hhmmss
6
M 
 
4
Store No.
Numeric
8
M 
 
5
Order Number /Transaction #
Numeric
14
M 
 
6
Record Type
Char 
3
M 
‘352'
7
Line number
Numeric
7
M 
 
8
Item Number 
Numeric
14
M 
 
9
Item Description
Char
60
 
 
10
Supplier item # / catalogue #
Char
24
 
 
11
UOM Code
Numeric
4
 
 
12
UOM Description
Char
20
 
 
13
Pack size / Ratio
Numeric
5
M 
 
14
Order Quantity / Sent quantity
Numeric (8,4)
12
M 
 
15
Trs cost price (excl) per UOM
Numeric (6,2)
8
 
 
16
Order Type
Numeric
6
 
 
17
Reference No.
Numeric
9
 
 
18
 Transaction Qty / Count qty  / Acknowledged qty
Numeric (8,4)
12
 
 
19
Reason Code
Numeric
4
 
 
20
Invoice Qty
Numeric (8,4)
12
 
 
21
Invoice Cost (excl) per UOM
Numeric (6,2)
8
 
 
22
Tax % on cost
Numeric (6,2)
8
 
 
23
Selling Price per UOM
Numeric (6,2)
8
 
 
24
Location
Char
20
 
 
25
Sign (Only for 315 & 323)
+ / -
1
 
 


Message Format
The message format is a pipe delimited flat file. Each PO Header and PO Details line is delimited by a carriage return, line feed.

Message Transport Details 

Feature
Specification
Additional Information
Source System Name
Biztalk

Source Platform / OS
Windows 2003

Source Physical Location
TBD

Source Underlying Data Storage Technology
SQL Server 2005

Target System Name
Storeline

Target Platform / OS
TBD

Target Physical Location
TBD

Target Underlying Data Storage Technology
TBD

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
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
File transfer will be logged using the Trackpoint component of the IMOF framework.

Error Handling
If the message cannot be delivered, retry 3 times at 10 minute intervals, then raise alert using the Error Processing component of IMOF.



Naming and Configuration
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 


RTI
Instruction Name: PODownload
Instruction Details
Description
To be determined
Enabled
True
Type
Hosted
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
TBD
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
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Account details will be included here once we have visibility of the environments.


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Successful delivery of PO file will logged using the Trackpoint component of the IMOF framework.

Failure of the file delivery will be raised through the Error Component of the IMOF framework..


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
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

Environment and Security Context
Not Required

Non-Functional Requirements
Testing Deliverables
TBD

Deployment
TBD


Assumptions and Outstanding Issues
Assumptions
ID
Assumption





Outstanding Issues
ID
Issue
To be addressed by
1
TBD

2


3


4


5


6


7




Volumes
No of files, records per file, file size, TBD.

Glossary

Acronym
Term
Description
DC
Distribution Center

IDS
Integration Data Store
The data store in the integration layer
IL
Interface Layer

IMOF
Integration Management and Operational Framework
Audit and Traceability framework
PO
Purchase Order
The message type containing a list of goods being delivered to a store.
RMS
Retail Management System
Oracle Retail Management System application



















Document Control
Change Record

Author
Date
Version
Change Reference, description
Allister Green
06-12-2006
V0.1 Draft
First issue















Related Documents

Author	
Date
Version
Title


















Distribution

Name
Position
Approver/Contributor/Other
Nathan Smith
Enterprise Architect

Adrian Hinks
Engagement Architect

David Onyett
Project Lead






















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 25 of  NUMPAGES 27	Date:  SAVEDATE \@ "d MMM yyyy" 23 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Will be updated with details of the new VOB for TOM integration when this is set up.
New section added



























































