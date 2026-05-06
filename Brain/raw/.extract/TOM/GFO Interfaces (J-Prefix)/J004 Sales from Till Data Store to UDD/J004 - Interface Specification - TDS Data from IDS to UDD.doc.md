		









`


TOM Integration

Interface Specification
TDS Data
From IDS to UDD


[J004]






Project BEN Code:
W???
Author:Allister GreenDate:
26/01/2007
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
26/01/2007
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
J002 to J010 - Information Architecture Context Diagram - UDD data load from GFO and IDS.vsd

Mapping spreadsheet
J004 - Sales Data from TDS to UDD - Mappings.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 6
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 6
1.2	Background	 PAGEREF _Toc153956171 \h 6
1.3	Scope	 PAGEREF _Toc153956172 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 7
2.2	Architecture	 PAGEREF _Toc153956175 \h 7
2.2.1	Extraction of Aggregated Sales Data into Flat File	 PAGEREF _Toc153956174 \h 7
2.2.2	File Transport	 PAGEREF _Toc153956174 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 10
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153956177 \h 11
3.1	Scope	 PAGEREF _Toc153956178 \h 11
3.2	Source Message Schema	 PAGEREF _Toc153956179 \h 11
3.2.1	Extraction of Aggregated Sales Data into Flat File	 PAGEREF _Toc153956179 \h 11
3.2.2	Extract from Aggregated Sales Staging tables to Flat File	 PAGEREF _Toc153956179 \h 11
3.2.3	Database Table Schemas	 PAGEREF _Toc153956179 \h 11
3.2.4	Extraction and Aggregation From TDS Staging Tables	 PAGEREF _Toc153956179 \h 11
3.3	Message Transport Details	 PAGEREF _Toc153956180 \h 15
3.4	Naming and Configuration	 PAGEREF _Toc153956181 \h 15
3.5	Environment and Security Context	 PAGEREF _Toc153956182 \h 16
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153956183 \h 17
4.1	Scope	 PAGEREF _Toc153956184 \h 17
4.2	Data Validation	 PAGEREF _Toc153956184 \h 17
4.3	Filtering	 PAGEREF _Toc153956186 \h 17
4.4	Mapping	 PAGEREF _Toc153956187 \h 17
4.5	Target Message Schema	 PAGEREF _Toc153956188 \h 17
4.6	Message Format	 PAGEREF _Toc153956189 \h 17
4.7	Message Transport Details	 PAGEREF _Toc153956190 \h 19
4.8	Naming and Configuration	 PAGEREF _Toc153956191 \h 20
4.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 20
4.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 21
5	Testing Deliverables	 PAGEREF _Toc153956202 \h 22
6	Deployment	 PAGEREF _Toc153956203 \h 23
7	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 24
7.1	Assumptions	 PAGEREF _Toc153956205 \h 24
7.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 24
Appendix A Volumes	 PAGEREF _Toc153956207 \h 25
Appendix B Glossary	 PAGEREF _Toc153956208 \h 26
Appendix C Document Control	 PAGEREF _Toc153956209 \h 27

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of Till Data Store (TDS) data from the TDS staging tables within the Integration Layer (IL), to the User Data Database (UDD) also within the IL. This User Data is needed by the Allocations process.

The document is of a sufficiently technical nature to allow a developer to build an actual interface. 

Background
An allocations process is needed to work with the Forecasting and Ordering system where the centre supply chain pushes stock into store. This can be for a variety of reasons but typical scenarios are: 
Allocation of a new product
Allocations to get ready for an event e.g. initial (additional) promotional stock
Allocation to initially fill a new store
Etc.

The main components of the allocations process are:
Overnight extract of data from GFO and IDS into the User Data Database (UDD) which is also located within the IDS
User creating allocations files manually using data from the UDD and an Excel template
The User uploading this allocations files into RMS, where they are validated
RMS generating and transferring allocations files to GFO via the Integration Layer

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
This interface will run at least once an hour, and under normal operating conditions will, once a hour, extract a previous hours period of sales data from the TDS staging tables within the IL, aggregate it by Store and Item, create a flat file, and place it into a staging directory also within the IL ready for uploading into the UDD.


Architecture



A SQL Agent job (name?) located in the ‘TSD Staging’ database exists for execution of interface J035 (Sales data from TSD to GFO)(See TSD J035 ????), will run every fifteen minutes.

This job will:
Populate ‘TicketDetail_Stage’ and ‘TicketHeader_Stage’ tables with TSD Sales data,
Run extract to GFO,
Run this interface (J004)
Clear Sales data from ‘TicketDetail_Stage’ and ‘TicketHeader_Stage’ that is over 4 hours old,

This interface (J004) will be run by this job after the extract to GFO step has been run. This is because:
If the population of sales data into the ‘TicketDetail_Stage’ and ‘TicketHeader_Stage’ fails, the J004 interface will not be run (hence not producing empty files),
Because J004 and J035 are aggregating from the same tables, this ensures that both aggregations are not running at the same time, potentially creating performance issues.


This interface consists of two parts
An SSIS package (name / location?) to extract the aggregated sales data and place it in a flat file
Transportation of the flat file to the UDD upload directory using RTI Shipping Agent.


Extraction of Aggregated Sales Data into Flat File

This stage of the interface will all be contained within an SSIS package (name / location?), and will comprise of the following steps:

Step 1: Run a stored procedure ‘ControlDataCheckRunTimeOKSalesDataForUDD_Control’ (note: trying to use TOM naming conventions for SP, i.e. <Category><Action><Entity>) to 

check if the ‘LastExtractStartTime’ within the ‘SalesDataForUDD_Control’ table is over 1 hour and 40 minutes old. If it is not, exit this SSIS package with no further action.

The reasons for this check are:
To ensure sales data only aggregated once an hour, despite this SSIS package being run more than once an hour
If recovering from error situation (e.g. if population of sales data into the ‘TicketDetail_Stage’ and ‘TicketHeader_Stage’ failed resulting the running of this interface being delayed), this interface is able to produce aggregated sales files for all hourly periods that had not previously been produced.

check if the ‘LastExtractStartTime’ within the ‘SalesDataForUDD_Control’ table is greater than 30 minutes old. If it is not, exit this SSIS package with no further action.

The reasons for this check are:
The ‘TicketHeader_Stage’ and ‘TicketDetail_Stage’ tables are loaded with sales data which can be up to 15 minutes old, hence the 30 minute gap provides a 15 minute cushion. E.g. If aggregating sales data for period from 2AM to 3AM, this stored procedure should not be run before 3.30AM. 

Step 2: Log a Trackpoint using IMOF, which logs the start of the aggregation.

Step 3: Run the stored procedure ‘SalesDataSelectTicket_Stage’ located within the ‘TDS Staging’ database to:

Extract and aggregate Sales data from the TDS staging tables (‘TicketHeader_Stage’, ‘TicketDetail_Stage’) within the ‘TDS Staging’ database within the IL

See section 3.2.4 for details of extraction and aggregation

The price data to be extracted will be for an hour period. A control table (‘SalesDataForUDD_Control’) within the ‘TDS Staging’ database records the start time of the last extraction (‘LastExtractStartTime’), and is used to establish the start time (‘LastExtractStartTime’ + 1 hour) of the hour period to be extracted now.

Populate the ‘SalesDataForUDD’ table within the ‘RTS Staging’ database with the aggregated data.

Step 4: Log a Trackpoint using IMOF, which logs the end of the aggregation, and the beginning of the extract to flat file.

Step 5: Extract the aggregated sales data into a flat file:

Call stored procedure ‘SequenceNoAndPeriodSelectSalesDataForUDD_Control’ to:
Retrieve the ‘SequenceNumber’ from the ‘SalesDataForUDD’ table, to be used as part of the file name (see below),
Retrieve the ‘LastExtractStartTime’ + 1 hour (i.e. the current period of aggregated data), which is needed to populate the ‘PeriodStartTime’ of the file Header record.

Create a comma delimited flat file (TDS_Sales_History_nnnnnnn.csv) containing the aggregated data, and place the file in the staging directory ‘RTSStaging_outbox’ within the IL. The ‘nnnnnnn’ of the file name is the 7 character numeric right justified 0 padded ‘SequenceNumber’. 

Notes: 
Each file created for upload into the UDD will have a sequence number one greater than the file containing the previous hours data. This sequence number will never be reset, hence will increment indefinitely.
When there is no sales data for an hour period, a file will still be produced, and will have one header record and no detail records.

Step 6: Log a Trackpoint using IMOF, which logs the end of the flat file creation.

Step 7: Run the stored procedure ‘ControlDataUpdateSalesDataForUDD_Control’ located within the ‘TDS Staging’ database to:

update the ‘SalesDataForUDD_Control’ table:
One hour is to be added to the ‘LastExtractStartTime’ 
‘SequenceNumber’ is to be incremented by 1.

Truncate all data in the ‘SalesDataForUDD’ table.

Step 8: Loop back to Step 1 to see if any more hour periods need to be aggregated.


Each step of this SSIS package is only run on successful completion of the previous step. So if any steps fail prior to the control table being updated in step 7, a rerun of this interface will ensure the same hourly period that previously failed will be aggregated again.

Failure of the aggregation or file creation steps will result in an alert being raised using the IMOF ‘Error Processing’ component.

File Transport

An RTI Shipping Agent Hosted Instruction “J004.RTS to UDD.Sales Data File Delivery” will:
Subscribe to the ‘RTSStaging_outbox’ directory, identifying the Sales Data file based on name pattern: ‘TDS_Sales_History*.csv’,
Transport the file immediately upon receipt to the UDD upload directory (‘UD_inbox’) also within the IL,
Log the successful file transfer using the Trackpoint component of IMOF. 



At time of writing, IMOF specifications have not yet been completed, hence details of how RTI or SSIS will record an event using the ‘Trackpoint’ component, or raise an error using the ‘Error Processing’ component, are to be determined.



Requirements for the End-to-End Interface

Audit Requirements
The IMOF Trackpoint component will record the successful completion of each stage of this interface as specified in sections 2.2.1 and 2.2.2.

Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
None. Price data will be loaded into UDD by sequence, and will load files as they become available within the UDD upload directory.
Performance Requirements
The interface should be capable of extracting and aggregating data from the TDS Staging tables, creating the flat file, and delivering it to the UDD upload directory within 15 minutes. This allows at least four periods of aggregation to be run per hour, which will only be needed in recovery / maintenance situations where normal hourly job run has been interrupted.

Need to ensure no impact on J035 (Sales data to GFO) interface performance, which also will be aggregating from the TicketDetail_Stage and TicketHeader_Stage tables.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
Because aggregation is by store and item, additional stores and items will have an impact on the performance, hence this interface needs to be able to process the maximum no of stores and items envisages for it’s target country.
Operational Support Requirements
TDS Staging extract, file creation failure, or file transfer failure raised through the Error Processing component of the IMOF framework. 

Alert IDs, and how to interface to IMOF Error Processing component TBD.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
None 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in the Extract-Stage of the interface
Scope
This stage will extract and aggregate the sales data from the TDS Staging tables within the IL, and populate another staging table within the IL with this data. This data is then populated into a flat file from the staging table data, and placed within a shared directory in the IL. The data is also transformed to the required format within SSIS package.

Source Schema

As the extract is two stages (extract from TDS Staging tables to aggregated sales data staging table, and extract to flat file), there are effectively two sources.

Extract from TDS to Aggregated Sales Staging tables

Source: TicketHeader_Stage and TicketDetail_Stage tables. See section 3.2.3 for schemas.

Target: SalesDataForUDD table

See section 3.2.4 for extraction and populate details

Extract from Aggregated Sales Staging tables to Flat File

Source: SalesDataForUDD table

Tarrget: TDS_Sales_History_nnnnnnn.csv comma delimited flat file.

See mappings file “J004 - Sales Data from TDS to UDD - Mappings.xls”.

Database Table Schemas

TicketHeader_Stage
Field Name
Type
NULL
InsertedDateTime
datetime
NOT NULL
GeneratedID
int
NOT NULL
StoreNo
int
NOT NULL
POSNo
smallint
NOT NULL
TicketNo
smallint
NOT NULL
EndTransDateTime
datetime
NOT NULL
StartTransDateTime
datetime
NOT NULL
YearWeekDay
smallint
NOT NULL
ReturnType
tinyint
NULL
VoidTicketNo
smallint
NULL
FacturaNo
smallint
NULL
FacturaID
nvarchar(15)
NULL
HomeShoppingOriginNo
tinyint
NULL
MasterPFSTill
smallint
NULL
CashierNo
smallint
NULL
TV
tinyint
NULL
TillType
nchar(1)
NULL
CheckoutBank
tinyint
NULL
EFTLocation
int
NULL
TillPersonality
smallint
NULL
DocType
tinyint
NULL
NumberOfItems
smallint
NULL
TicketAmount
int
NULL
DepositBankableAmount
int
NULL
DepositNonBankableAmount
int
NULL
BadRecordInd
tinyint
NULL
ReceiptType
tinyint
NULL
StockReconcilFlg
bit
NULL
StartFlg
bit
NULL
NoSaleFlg
bit
NULL
VoidTransFlg
bit
NULL
TenderPurchaseFlg
bit
NULL
HomeShoppingFlg
bit
NULL
ExtDeviceFlg
bit
NULL
ReturnTicketFlg
bit
NULL
TrainingModeFlg
bit
NULL
PCGeneratedFlg
bit
NULL
POSOfflineFlg
bit
NULL
ClubCardReentryFlg
bit
NULL
VoidTicketFlg
bit
NULL
DepositFlg
bit
NULL
TakeAwayFlg
bit
NULL
EatInFlg
bit
NULL
DriveOffBalFlg
bit
NULL
CustToPayFlg
bit
NULL
DriveOffFlg
bit
NULL
FuelTestFlg
bit
NULL
WastageModeFlg
bit
NULL
CouponTicketFlg
bit
NULL
InfoFlg
bit
NULL
TenderTicketFlg
bit
NULL
RecalledTicketFlg
bit
NULL
SavedTicketFlg
bit
NULL
NetAmount
int
NULL
TaxValue
int
NULL

TicketDetail_Stage
Field Name
Type
NULL
InsertedDateTime
datetime
NOT NULL
GeneratedID
int
NOT NULL
StoreNo
int
NOT NULL
POSNo
smallint
NOT NULL
TicketNo
smallint
NOT NULL
EndTransDateTime
datetime
NOT NULL
TransSeqNo
int
NOT NULL
ItemDeptWasteType
tinyint
NOT NULL
TransDateTime
datetime
NULL
PluCode
bigint
NULL
DepartmentNo
smallint
NULL
ReturnType
tinyint
NULL
Qty
int
NULL
Price
int
NULL
Amount
int
NULL
PumpNo
tinyint
NULL
FuelGrade
tinyint
NULL
POOriginalPrice
int
NULL
POReducedPrice
int
NULL
PODiffPrice
int
NULL
APAuthPrice
int
NULL
APSoldPrice
int
NULL
APOriginalPrice
int
NULL
APDiffAmt
int
NULL
EPOriginalPrice
int
NULL
EPEmbeddedPrice
int
NULL
EPQty
int
NULL
EPDiffAmt
int
NULL
TaxBand
tinyint
NULL
WasCanceledFlg
bit
NULL
PriceOverideFlg
bit
NULL
ManualPriceFlg
bit
NULL
QtyIsWeightFlg
bit
NULL
QtyIsDecimalFlg
bit
NULL
QtyIsLtrFlg
bit
NULL
ScannedItemFlg
bit
NULL
PriceEmbeddedFlg
bit
NULL
CounterDeptFlg
bit
NULL
RetToStockFlg
bit
NULL
CSTaxCombFlg
bit
NULL
SupplierPromoFlg
bit
NULL
ProductKeyedFlg
bit
NULL
SoftkeyOtherFlg
bit
NULL
PEIBFlg
bit
NULL
VoidAuthFlg
bit
NULL
MSU
nvarchar(4)
NULL
NetAmount
int
NULL
VATAmount
int
NULL
SoldWeight
int
NULL
APACSProdCode
nvarchar(1)
NULL
ExtRecExistsFlg
bit
NULL
SubtractFlg
bit
NULL
CancelFlg
bit
NULL
NegativeItemFlg
bit
NULL
StaffDiscountableFlg
bit
NULL
ItemOnSaleFlg
bit
NULL
ManualPriceAllowedFlg
bit
NULL
WeightFromScaleFlg
bit
NULL
ChainedPrevItemFlg
bit
NULL
PromotionFlg
bit
NULL
ReductionFlg
bit
NULL
OfferFlg
bit
NULL
NonMerchandiseFlg
bit
NULL
StoreCouponFlg
bit
NULL
VendorCouponFlg
bit
NULL
ItemDiscountFlg
bit
NULL
ReadFromPCFlg
bit
NULL
NextInfoFlg
bit
NULL
MultiSaverFlg
bit
NULL
ExternalPromoFlg
bit
NULL
FastFoodDragsModFlg
bit
NULL
FastFoodModifierFlg
bit
NULL
OfferDiscountFlg
bit
NULL
OfferContinueFlg
bit
NULL
FreqShopperDiscountFlg
bit
NULL
FSPaymentFlg
bit
NULL
FastFoodModPriceFlg
bit
NULL
BottleDepositFlg
bit
NULL
CSSSSaleFlg
bit
NULL
APCEEmbeddedPriceFlg
bit
NULL
APCEEmbeddedWeightFlg
bit
NULL
OfferFirstFlg
bit
NULL
Free
nvarchar(6)
NULL
NotFoundSaleFlg
bit
NULL
CostPlusDeptFlg
bit
NULL
DeptDiscountFlg
bit
NULL
CostPlusFlg
bit
NULL
ExternalPromFlg
bit
NULL
NoDisplayWtQtyFlg
bit
NULL
TopupPLUFlg
bit
NULL
TopupAutoVoidFlg
bit
NULL
CCAsTopupFlg
bit
NULL


SalesDataForUDD
Field Name
Type
Notes
SKUID
varchar(25)

StoreID
int

Quantity
int

WeightTransactions
int
The number of transactions sold by weight.


Extraction and Aggregation From TDS Staging Tables

The sales data is to be aggregated by Store and Item for each hour period. Also needed within the aggregation is a count of transactions whose quantity is by weight.

The aggregation query will be as follows:

select 
D.PluCode,
D.StoreNo,
Sum(D.Qty) as Qty,
Sum(cast(D.QtyIsWeightFlg as smallint)) as WeightTransactions
from TicketDetail_Stage D 
inner join TicketHeader_Stage H 
 on D.InsertedDateTime = H.InsertedDateTime 
and D.POSNo = H.POSNo
and D.StoreNo = H.StoreNo
and D.TicketNo = H.TicketNo
where H.VoidTicketFlg = 0
    and H.TrainingModeFlg = 0
    and H.BadRecordInd = 0
    and (H.ReturnType = 1 
            or H.ReturnType = 2
            or H.ReturnType = 3
            or H.ReturnType = 0)
    and D.ItemDeptWasteType=1
    and D.PluCode IS NOT NULL
    and H.EndTransDateTime >= @PeriodStartTime
    and H.EndTransDateTime < @PeriodStartTime + 1 hour
group by D.PluCode, D.StoreNo


Notes:
- The @PeriodStartTime will be the dateTime of start of the hour period being aggregated
- This business logic deciding which records to include in the aggregation is identical to the aggregation for interface J035 (TDS to GFO extract (See TSD J035 ???).


Message Transport Details
n/a

Naming and Configuration

This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 



SSIS
Package Name: TBD
Stored Procedure
Name
ControlDataCheckRunTimeOKSalesDataForUDD_Control
Stored Procedure
Name
SalesDataSelectTicket_Stage
Stored Procedure
Name
SequenceNoAndPeriodSelectSalesDataForUDD_Control’
Stored Procedure
Name
ControlDataUpdateSalesDataForUDD_Control

SQL Agent Job
Name
TBD
Location
TBD


File and Directory Names
Description
Name
IDS Staging directory for Sales Data flat file
RTSStaging_outbox
Sales Data file name
TDS_Sales_History_nnnnnnn.csv


Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example employing BizTalk this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).

 
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Certain points in this interface will be logged using the Trackpoint component of IMOF.

Failure of this interface will result in an alert raised through the error processing component of the IMOF framework.


Processing required in the Messaging Stage of the interface
Scope
RTI Shipping Agent will monitor for the Sales Data file (identified by name pattern) in the staging directory, and transport it to the UDD upload directory immediately upon receipt.
Data Validation
None.
Filtering
There is no filtering requirement.
Mapping
Please refer to “J004 - Sales Data from TDS to UDD - Mappings.xls”.
Target Message Schema

Field Name
Description
Type
Format
Mandatory





Header Record




Type
Record type
Char(1)
“H” fixed value
Y
DateCreated
Date of extract from source system
Char(10)
CCYY-MM-DD
Y
TimeCreated
Time of extract from source system
Char(8)
HH:mm:ss
Y
PeriodStartTime
Start time of the hour period being aggregated
Char(23)
CCYY-MM-DD HH:mm:ss.nnn
Y
RecordCount
No of Header and Detail records
Int

Y
 
 

 

Detail Record




SKUID
Item ID
char(25)

Y
StoreID

varchar(250)

Y
StartTime
The start datetime of the hour period that this file will contain aggregated data for.
datetime
E.g “2007-01-29 12:43:21.000”
Y
Quantity

Int

Y
WeightTransactions
The number of transactions that are sold by weight
Int

Y


Message Format
The source message is from database tables and is getting converted to the target file format in a package. The following message format is the target message format. 

Note: The data is dummy

H,2007-04-01,15:41:01.000, 2007-02-02 23:20:02.000,3
D,123456789,123456789,2007-02-03 00:00:00.000,456423,40
D,234567890,567890123,2007-02-03 00:00:00.000,542,20

Message Transport Details 


Feature
Specification
Additional Information
Source System Name
TDS Staging

Source Platform / OS
Windows 2003

Source Physical Location
TBD

Source Underlying Data Storage Technology
SQL Server 2005

Target System Name
UDD

Target Platform / OS
Windows 2003

Target Physical Location
TBD

Target Underlying Data Storage Technology
SQL Server 2005

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
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
File delivery recorded by Trackpoint component of IMOF

Error Handling
Failure of file delivery raised through the ‘Error Processing’ component of IMOF.


Naming and Configuration
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 


RTI
Instruction Name: J004.RTS to UDD.Sales Data File Delivery
Instruction Details
Description
Transport of Sales Data from RTS Staging to UDD
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
1
Priority
Normal
Batch Size
1
Period
10
Retry Attempts
1
Timeout
900
Require Data Send
Yes
Exception Management
Treat Fatal Adapter Exception As
Fatal
Treat Unhandled Exceptions As
Fatal


Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Account details will be included here once we have visibility of the environments.


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Successful delivery of file will be logged using the Trackpoint component of IMOF.

Failure of the file transport to the UDD upload directory, will be raised through the error processing component of the IMOF framework.


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
Directory locations (section 4.6)

2
SQL Agent job name created for interface J035 (sections 2.2, 3.4)

3
TSD name for interface J035 (sections 2.2, Appendix C)

4
SSIS package name / locations (sections 2.2, 3.4)

5
Check naming of stored procedures (section 2.2)

6
How IMOF alerts and trackpoints integrated into interface (Sections 2.2, 2.3)
IMOF detailed specifications becoming available














Volumes
One file will be produced per hour for upload into the UDD.

File size estimates are as follows, and are based on extrapolating by number of stores from an hours sample of UK sales data.


UK
Turkey
US
TicketDetail rows
2,755,000


Number of stores
1,800
35
300
Aggregated data records
1,534,000
30,000
256,000
Sales Data File Size (MB) 1

31
0.6
5.1

Notes:
1 – File size estimate based on estimating each record as being 20 bytes:
SKUID – 9
StoreID – 4
Quantity – 5
Weight Transactions - 2



Glossary

Acronym
Term
Description
IDS
Integration Data Store
Data store within the Integration Layer
IL
Integration Layer
Enterprise layer for system integration
IMOF
Integration Management and Operational Framework
Audit and Traceability framework
SSIS
SQL Server Integration Services
A Microsoft tool for data integration
TDS
Till Data Store
Name of store system collecting sales data at Point Of Sale.
UDD
User Data Database
Database within the IL specifically to hold data needed by users creating the Allocations.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Allister Green
26-01-2007
V0.1 Draft
First issue















Related Documents

Author	
Date
Version
Title
James Keel
05/12/2006
0.1
TSD – Allocations Solution Part A, User Data Database.
Ben Wild


TSD – J035 ???


Distribution

Name
Position
Approver/Contributor/Other
Adrian Hinks
Engagement Architect

James Keel























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 17 of  NUMPAGES 27	Date:  SAVEDATE \@ "d MMM yyyy" 19 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Will be updated with details of the new VOB for TOM integration when this is set up.
New section added



























































