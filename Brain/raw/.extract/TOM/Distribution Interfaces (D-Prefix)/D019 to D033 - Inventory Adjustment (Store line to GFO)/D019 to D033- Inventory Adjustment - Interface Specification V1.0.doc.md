





TOM Integration
Interface Specification
Inventory Adjustment

STORELINE 
To 
GFO

[D019 to D033]





Project BEN Code:
W60416
Author:
Debasis Pattanaik
Date:
13/02/2007
Version:
1.0
Status:
Signed-Off 
Modified By:

Reviewed By:
Erwin Oguz

Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
05/02/2007
0.1D
Draft
Ganesan, Sankar
06/02/2007
0.2D
Draft
Debasis Pattanaik
09/02/2007
0.3D
Draft – incorporating Erwin review comments.
Debasis Pattanaik
13/02/2007
0.4D
Draft – incorporating Erwin comments to add JIP13 stored procedure.

Reviewers

Name
Date
Version
Position
Ganesan, Sankar
06/02/2007
0.2D
Draft
Erwin Oguz
13/02/2007
1.0
Sign-Off version






At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Erwin Oguz
Position
Solution Architect
Signature

Date
13/02/2007

Distribution List

Name
Date of Issue
Version
Oguz Erwin
14/02/2007
1.0
David Onyett
14/02/2007
1.0
Venkateswara Rao
14/02/2007
1.0







Document Source

Related Documents: XML STORELINE source file schema, GFO system TSD document & STORELINE system FSD document 

Directory: Embedded in this document

File Name: 
XML STORELINE source file schema - tes.jp.retail.storeline.invadjust.v2.7
 EMBED Package  
GFO system TSD document - TSD008 - Stock Record - non-sales events.doc
 EMBED Word.Document.8 \s 
STORELINE system FSD document - FS1847_BO_Stock_Interfaces.doc
 EMBED Word.Document.8 \s 


Information Architecture Context diagram
D033- Inventory Adjustment - Information_Context_Diagram.vsd
 EMBED Visio.Drawing.11  

Mapping spreadsheet
Not required for this interface
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc159229859 \h 7
1.1	Purpose of Document	 PAGEREF _Toc159229860 \h 7
1.2	Background	 PAGEREF _Toc159229861 \h 7
1.3	Scope	 PAGEREF _Toc159229862 \h 7
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc159229863 \h 8
2.1	Description of the End-to-End Interface	 PAGEREF _Toc159229864 \h 8
2.2	Architecture	 PAGEREF _Toc159229865 \h 8
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc159229866 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc159229867 \h 10
3.1	Scope	 PAGEREF _Toc159229868 \h 10
3.2	Source Message Schema	 PAGEREF _Toc159229869 \h 10
3.3	Message Format	 PAGEREF _Toc159229870 \h 11
3.4	Message Transport Details	 PAGEREF _Toc159229871 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc159229872 \h 12
3.6	Environment and Security Context	 PAGEREF _Toc159229873 \h 13
3.7	Non-Functional Requirements	 PAGEREF _Toc159229874 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc159229875 \h 14
4.1	Scope	 PAGEREF _Toc159229876 \h 14
4.2	Data Validation	 PAGEREF _Toc159229877 \h 14
4.3	Filtering	 PAGEREF _Toc159229878 \h 14
4.4	Stored Procedures	 PAGEREF _Toc159229879 \h 14
4.5	JH0S00 – Stream information retrieved	 PAGEREF _Toc159229880 \h 14
4.6	JIP11 – process wastage	 PAGEREF _Toc159229881 \h 14
4.7	JIP12 – process stock counts	 PAGEREF _Toc159229882 \h 14
4.8	JIP13 – process stock adjustment	 PAGEREF _Toc159229883 \h 15
4.9	Mapping	 PAGEREF _Toc159229884 \h 15
4.10	Mapping of JH0S00 – Package to return STREAM info	 PAGEREF _Toc159229885 \h 15
4.11	Mapping of JIP11 – process wastage	 PAGEREF _Toc159229886 \h 16
4.12	Mapping of JIP12 – process stock adjustment	 PAGEREF _Toc159229887 \h 17
4.13	Mapping of JIP13 – process stock adjustment	 PAGEREF _Toc159229888 \h 18
4.14	Message Format	 PAGEREF _Toc159229889 \h 19
4.7 Message Transport Details	 PAGEREF _Toc159229890 \h 19
4.15	Naming and Configuration	 PAGEREF _Toc159229891 \h 20
4.16	Environment and Security Context	 PAGEREF _Toc159229892 \h 20
4.17	Non-Functional Requirements	 PAGEREF _Toc159229893 \h 20
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc159229894 \h 21
5.1	Scope	 PAGEREF _Toc159229895 \h 21
5.2	Data Validation	 PAGEREF _Toc159229896 \h 21
5.3	Filtering	 PAGEREF _Toc159229897 \h 21
5.4	Mapping	 PAGEREF _Toc159229898 \h 21
5.5	Target Message Schema	 PAGEREF _Toc159229899 \h 21
5.6	Message Transport Details	 PAGEREF _Toc159229900 \h 21
5.7	Naming and Configuration	 PAGEREF _Toc159229901 \h 21
5.8	Environment and Security Context	 PAGEREF _Toc159229902 \h 21
5.9	Non-Functional Requirements	 PAGEREF _Toc159229903 \h 21
6	Testing Deliverables	 PAGEREF _Toc159229904 \h 22
7	Deployment	 PAGEREF _Toc159229905 \h 23
8	Assumptions and Outstanding Issues	 PAGEREF _Toc159229906 \h 24
8.1	Assumptions	 PAGEREF _Toc159229907 \h 24
8.2	Outstanding Issues	 PAGEREF _Toc159229908 \h 24
Appendix A Volumes	 PAGEREF _Toc159229909 \h 25
•	Glossary	 PAGEREF _Toc159229910 \h 26
Appendix B Document Control	 PAGEREF _Toc159229911 \h 27

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements with respect to STORELINE (D019) inventory adjustment data e.g. Wastage (out-of-code and damaged), Stock counts & Stock take adjustment into GFO interface (D033).

The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. Therefore the GFO system Technical System Document (TSD) and STORELINE system Functional System Document are provided for better understanding of this interface. 

This interface is only for US implementations. Turkey implementation does not require this interface. 

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including STORELINE and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Inventory Adjustment data from STORELINE into GFO.

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
The interface is to upload the Inventory Adjustment data (Wastage, Stock counts & Stock take adjustment) from STORELINE interface (D019) into GFO interface (D033). The Upload is a full upload in nature.

The interface will be governed by BizTalk Orchestration, which expects the Inventory Adjustment data (| delimited flat file) from STORELINE interface (D019). The STORELINE interface will put this file (*.dat) in the shared location through RTI SOAP adapter. The BizTalk server then transfers this flat file data by invoking GFO interfaces (D033) stored procedures through DB2 adopter. BizTalk will first invokes JH0S00  –  stored procedure to get the stream information which is passed to subsequent stored procedure JIP11 for stock wastage(Reason code-327),JIP12 for Stock Count(Reason Code-315) & JIP13 for Stock Adjustment(Reason Code-323). This then get updated/inserted in GFO underlying table. The output attributes returned by stored procedure will determine the success/failure of this updating.

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
The interface should be capable of extracting data in the form of flat file from the shared location at STORELINE side and delivering the resulting into GFO side database tables before the identified cut-off time. The interface should run on real time basis.
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
STORELINE interface D019 creates a pipe | delimited flat file on real time basis whenever it receives an inventory adjustment data. BizTalk in turn picks up the file from the shared location and invokes series of subroutines through DB2 Adopter to update/insert the underline table of GFO interface D033. The stream information would be passed as the input attribute to the stored procedures JIP11, JIP12 and JIP13.
Source Message Schema
Field Name
Optional
Type
Description
HEADER RECORDS
CapturedBy – CreatedBy
Yes
String

DateOfExtract

String
Store-line extraction date
DelAfterDate
Yes
String
Delivery before date
DelBeforeDate
Yes
String
Delivery after date
Description
Yes
String
Free form description
DriversName-Courier
Yes
String
Courier Driver Name
ExpectedDelDate
Yes
String
Expected Delivery Date
InvoiceNumber
Yes
String
Invoice Number
InvoiceTaxTotal
Yes
String
Invoice Tax Total
InvoiceTotal
Yes
String
Invoice Total
NoOfDetailLines

Unsigned Int
No. of Detail Items
OrderDate
Yes
String
Count Order Date
OrderNumber-TransactionNo

Unsigned Int
Count Order Number
OrderType-CountType
Yes
Unsigned Int
Count Order Type
OriginalOrderNumber
Yes
Unsigned Int
Original Order Number
ReasonCode
Yes
number
Reason Code
RecordType

String
Record Type
RefNo1
Yes
String
Reference No 1
RefNo2
Yes
String
Reference No 2
Remarks
Yes
String
Remarks
ReprocessedFlag
Yes
number
Re-Processed Flag
StoreAddress
Yes
String
Location Address
StoreName
Yes
String
Location Name
StoreNo

Unsigned Int
Location of extracted data
SupplierAddress
Yes
String
Supplier Address
SupplierCode-ToStore
Yes
String
Supplier Code
SupplierName
Yes
String
Supplier Name
SupplierType
Yes
Unsigned Int
Supplier Type
TimeOfExtract

String
Extraction time of data
TotalQty
Yes
String
Total Quantity
TotalValue
Yes
String
Total Value
TransactionDateTime
Yes
String
Transaction Date and Time
UserName
Yes
String
Operator name
DETAIL RECORDS – Grouping starts can have multiple detail record
DateOfExtract

String
Storeline extract date
InvoiceCost-Excl-PerUOM
Yes
String
Invoice cost excluding (Per UOM)
InvoiceQty
Yes
String
Invoice Quantity
ItemDescription
Yes
String
Item Description
ItemNumber
Yes
Unsigned Int
Item CodeItem Code
Used to populate ITEM field 
LineNumber
Yes
Unsigned Int
Transaction line number
Location
Yes
String
Location in store 
OrderNumber-TransactionNumber
Yes
Unsigned Int
Concatenated with store no to get Batch Number.
OrderQuantity-SentQuantity
Yes
Unsigned Int

OrderType
Yes
Unsigned Int

PackSize-Ratio
Yes
Unsigned Int

ReasonCode
Yes
Number
Reason Code field direct mapping
RecordType
Yes
String
Type of record as per Storeline 
ReferenceNo
Yes
Unsigned Int

SellingPricePerUOM
Yes
String

Sign
Yes
String
Sign indicator 
 - negative 
+ positive
Used to get Adjusted Qty
StoreNo

Unsigned Int
Concatenated with Order Number-Transaction Number to get Batch Number.
SupplierItemNo-CatalogueNo
Yes
String

TaxPercentageOnCost
Yes
String

TimeOfExtract

String

TransactionQty
Yes
String
Transaction Quantity concatenated with sign indicator will give meaningful value.
TrsCostPrice-Excl-PerUOM
Yes
String

UOMCode
Yes
Unsigned Int
Unit of measurement 
UOMDescription
Yes
String
Measurement description

Message Format
The source message is in the form of pipe | delimited flat file from STORELINE. 

Message Transport Details

Feature
Specification
Additional Information
Source System Name
STORELINE

Source Platform / OS
Windows

Source Physical Location


Source Underlying Data Storage Technology
SQL Server

Target System Name
Biztalk 2006

Target Platform / OS
Biztalk 2006 Server/Windows server 2003

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	

Data Format.
XML			
Delimited		
Positional		

| delimited
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
Package Name: TOM.D019 to D033 Inventory Adjustment STORELINE to GFO
BizTalk Procedure
Name
TOM.D019 to D033.Inventory Adjustment STORELINE to GFO
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



The naming standard to be followed as mentioned in the document – 

 EMBED Word.Document.8 \s 
Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
The BizTalk server transfers the source message schema file from STORELINE (D019) to GFO interface (D033) by invoking a series of stored procedures within DB2.This will first invokes JH0S00 – stored procedure to get the stream information which is passed along with other input attributes to get updated/inserted in GFO underlying table. 
Data Validation
Data Validation will be done by the target ORMS system.
Filtering
There is no filtering requirement.
Stored Procedures
The stock event data from STORELINE then immediately use it to invoke the relevant stored procedure(s) within DB2. The types of stock event involved are:

Wastage (out-of-code and damaged) – Reason Code 327
Stock counts – Reason Code 315
Stock Adjustment – Reason Code 323

The following description gives the details of stored procedure need to be invoked to pass data from STORELINE to GFO.
JH0S00 – Stream information retrieved 
JH0S00 will determine a store’s database stream then point subsequent processing to that package set.
JIP11 – process wastage 
JIP11 will take wastage data and use it to update the following tables:

	TXJJ0PDM	stock movements
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ004D)

STORELINE record type 327, GFO reason code 515 (discontinued) = out-of-code
STORELINE record type 327, GFO reason code 516 (end of season) = out-of-code
STORELINE record type 327, GFO reason code 517 = damaged
STORELINE record type 327, GFO reason code 518 = out-of-code
STORELINE record type 327, GFO reason code 519 (insufficient code) = out-of-code
JIP12 – process stock counts 
JIP12 will take stock count data and use it to update the following tables:

	TXJJ0ASC	applied stock count
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ004D)

STORELINE record type 315 = stock count (difference)
 

JIP13 – process stock adjustment 
JIP13 will take stock adjustment data and use it to update the following tables:

	TXJJ0ASC	applied stock count
	TXJJ0PPH	product profile history
	TXJJ0BKS	stock record (via module JJ003D)

STORELINE record type 323 = stock count (absolute)
Mapping
The STORELINE inventory adjustment data ROWSET get created by BizTalk and passed to GFO subroutines as input attributes. The input attribute order with its source mapping are given below,
Mapping of JH0S00 – Package to return STREAM info 
The stored-procedure returns the STREAM field details. The input attribute to this store procedure is STORE ID which returns stream details and will be used with other store procedure as an input attributes. The foot-print of this stored procedure given below 

Sr NoAttribute Field NameFormatSource Field TypeSource 
Field NameDescriptionINPUT ATTRIBUTES
1
IN_RO_NO
PIC 9(5) 
SetDtl
Store No
I/P attributes to stored procedure.
OUTPUT ATTRIBUTES
1
OUT_STREAM
PIC X


Stream Name(requires to be used in following stored procedures)
2
OUT_CODE_LEVEL
PIC X



3
OUT_CR_PART_NO
PIC X(2)



4
OUT_RO_NAME
PIC X(25)


Store Name
5
OUT_ERROR_CODE
PIC 9(2)



6
OUT_FATAL_ERROR_LOG
PIC X(29)




The return output attributes determine the success/failure of data insert/update in GFO e.g.
0 - successful update
1 - System unavailable
4 - Store not found
5 - Steam invalid
6 - Fatal error
8 - Code level invalid 
2009 - Product code not found
2019 - DB2 deadly embrace (contention)

In either cases the message need to be written on event log. In case of failure the subscription message get suspended but remain in disposable mode which keeps on trying to get success stream information from stored procedure to execute subsequent stored procedure. The failures of this stored procedure also stop execution of following stored procedure and move to next ROWSET.

In case of failure a log file has to be maintained as per the format given below e.g.

< Source File Name >. < Store Procedure Name >. < Processed DATE/TIME > -                                   < OUT_ERROR_CODE > - < OUT_FATAL_ERROR_LOG>

Mapping of JIP11 – process wastage 
The foot-print of this stored procedure with it’s ROWSET mapping details are given below –

Sr NoAttribute Field NameCobol FormatSource Field TypeSource 
Field NameDescriptionINPUT ATTRIBUTES
1
STREAM      
PIC X           


Output attribute of JH0S00  Stored Procedure
2
RO-NO       
PIC 9(5)             
SetDtl
Store No

3
BPR-TPN     
PIC 9(9)             
SetDtl
Item Number

4
WASTAGE-DATE
PIC X(10)            
SetDtl
Date of Extract
CCYY-MM-DD
5
WASTAGE-TIME
PIC X(8)            
SetDtl
Time of Extract
HH.MM.SS
6
WASTAGE-CODE
PIC 9(3)             
SetDtl
Reason Code
STORELINE record type 327, reason code 515 (discontinued) = out-of-code

STORELINE record type 327, reason code 516 (end of season) = out-of-code

STORELINE record type 327, reason code 517 = damaged

STORELINE record type 327, reason code 518 = out-of-code

STORELINE record type 327, reason code 519 (insufficient code) = out-of-code

7
QUANTITY
PIC 9(5)V99
SetDtl
Transaction Qty

OUTPUT ATTRIBUTES
1
RETURN-CODE.  
PIC 9(4). 


Returned ZERO in case of success
2
FILLER              
PIC X.    



3
REASON-CODE   
PIC 9(4). 



4
FILLER         
PIC X.    



5
REASON-PROGRAMME 
PIC X(8). 



6
FILLER         
PIC X.    



7
ERROR-SQLCODE
PIC -9(9).




The return output attributes determine the success/failure of data insert/update in GFO.In either cases the message need to be written on event log. In case of failure a log file has to be maintained as per the format given below e.g.

<Source File Name>.<Store Procedure Name>. <Processed DATE/TIME> . <RETURN-CODE> - < REASON-CODE   > - < REASON-PROGRAMME > - < ERROR-SQLCODE>

Mapping of JIP12 – process stock adjustment 
This stored procedure get invoked when the ROWSET contains the Reason Code 315.The foot-print of this stored procedure with it’s ROWSET mapping details are given below –

Sr NoAttribute Field NameCobol FormatSource Field TypeSource 
Field NameDescriptionINPUT ATTRIBUTES
1
STREAM     
PIC X.


Output attribute of JH0S00  Stored Procedure
2
RO-NO      
PIC 9(5).
SetDtl
Store No

3
BPR-TPN    
PIC 9(9).
SetDtl
Item Number

4
COUNT-DATE 
PIC X(10).
SetDtl
Date of Extract
CCYY-MM-DD
5
COUNT-TIME 
PIC X(8).
SetDtl
Time of Extract
HH.MM.SS
6
QUANTITY   
PIC 9(5)V99
SetDtl
Transaction Qty

OUTPUT ATTRIBUTES



Transaction Qty
1
RETURN-CODE.  
PIC 9(4). 


Returned ZERO in case of success
2
FILLER              
PIC X.    



3
REASON-CODE   
PIC 9(4). 



4
FILLER         
PIC X.    



5
REASON-PROGRAMME 
PIC X(8). 



6
FILLER         
PIC X.    



7
ERROR-SQLCODE
PIC -9(9).




The return output attributes determine the success/failure of data insert/update in GFO.In either cases the message need to be written on event log. In case of failure a log file has to be maintained as per the format given below e.g.

<Source File Name>.<Store Procedure Name>. <Processed DATE/TIME> . <RETURN-CODE> - < REASON-CODE   > - < REASON-PROGRAMME > - < ERROR-SQLCODE>

Mapping of JIP13 – process stock adjustment 
This stored procedure get invoked when the ROWSET contains the Reason Code 323.The foot-print of this stored procedure with it’s ROWSET mapping details are given below –

Sr NoAttribute Field NameCobol FormatSource Field TypeSource 
Field NameDescriptionINPUT ATTRIBUTES
1
STREAM     
PIC X.


Output attribute of JH0S00 Stored Procedure
2
RO-NO      
PIC 9(5).
SetDtl
Store No
Store id comes from source schema
3
BPR-TPN    
PIC 9(9).
SetDtl
Item Number
Item number on which stock take has been taken
4
COUNT-DATE 
PIC X(10).
SetDtl
Date of Extract
CCYY-MM-DD
5
COUNT-TIME 
PIC X(8).
SetDtl
Time of Extract
HH.MM.SS
6
QUANTITY   
PIC 9(5)V99
SetDtl
Transaction Qty
Stock takes quantity
OUTPUT ATTRIBUTES
2
RETURN-CODE.  
PIC 9(4). 


Returned ZERO in case of success
3
FILLER              
PIC X.    



4
REASON-CODE   
PIC 9(4). 



5
FILLER         
PIC X.    



6
REASON-PROGRAMME 
PIC X(8). 



7
FILLER         
PIC X.    



8
ERROR-SQLCODE
PIC -9(9).




The return output attributes determine the success/failure of data insert/update in GFO.In either cases the message need to be written on event log. In case of failure a log file has to be maintained as per the format given below e.g.

<Source File Name>.<Store Procedure Name>. <Processed DATE/TIME> . <RETURN-CODE> - < REASON-CODE   > - < REASON-PROGRAMME > - < ERROR-SQLCODE>

Message Format
4.7 Message Transport Details 
For messages destined for ORMS system, the following applies.	

Feature
Specification
Additional Information
Source System Name
Biztalk 2006

Source Platform / OS
Biztalk 2006 Server/Windows server 2003

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
GFO

Target Platform / OS
COBOL/UNIX

Target Physical Location


Target Underlying Data Storage Technology
RDBMS

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter                              
DB2 Adapter                                    

Data Format

XML  				
Delimited 			
Positional 			
COBOL format                                 

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
Currently it will keep all error details in a txt file. Later this may change as per the business decision.


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
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
Rollback transaction supported by GFO in case of failure.
2
Assuming STREAM information is extracted from JH0S00 stored procedure through DB2 adopter for each input ROWSET.

Outstanding Issues
ID
Issue
To be addressed by
1
DB2 adopter specification to call sub procedures need to be defined
Erwin Oguz
2
Error handling with respect to DB2 copybook need to be defined
Erwin Oguz
3
STORELINE source file Physical Location need to be defined
Erwin Oguz
4
Reason code from STORELINE to GFO need to be defined
Erwin Oguz


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
Group Forecasting and Ordering
The GFO operates on Tesco deals with the forecasting & Ordering.
Storeline
STORE used for inventory purposes.
The STORELINE operates on Tesco deals with the inventory control. 
XSD
XML Schema Definition
It describe the elements in an Extensible Markup Language (XML) document
XML
Extensible Markup Language
An open standard for describing data. It is used for defining a common method for identifying data. It supports business-to-business transactions and also uses electronic data interchange and Web services. 
FTP
File Transfer Protocol
The Internet File Transfer Protocol (FTP) is defined facilities for transferring files to and from remote computer systems.
DB2
Database access adopter
It is used to access AS/400 platform. This helps to invokes underlying database stored procedure from outside. It has capability to invoke stored procedure as per the ROWSET.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Debasis Pattanaik
05/02/2007
0.1D
Draft
Ganesan, Sankar
06/02/2007
0.2D
Draft
Debasis Pattanaik
09/02/2007
0.3D
Draft – incorporating Erwin review comments.
Debasis Pattanaik
12/02/2007
0.4D
Draft – incorporating Erwin review comments to include JIP013 in the interface.



Related Documents

Author	
Date
Version
Title
Isaac
18/Aug/2004
4.0
StoreLine FS1847 – BO Stock Interfaces
Neil Williams
26/Jan/2007
0.02
Technical System Design - TSD008 Stock Record - non-sale events










Distribution

Name
Position
Approver/Contributor/Other
Erwin Oguz
Enterprise Architect
Approver
David Onyett
Project Leader

Venkateswara Rao
Offshore Co-ordinator

























	










Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT 



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 15 of  NUMPAGES 27	Date:  SAVEDATE \@ "d MMM yyyy" 9 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT 




