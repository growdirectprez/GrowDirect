		









`


TOM Integration

Interface Specification
Sales Data 
TDS to GFO


[J035]






Project BEN Code:
W???
Author:B.WildDate:
16/02/2007
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
B.Wild
16/02/2007
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
To do

Mapping spreadsheet
To do
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 6
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 6
1.2	Background	 PAGEREF _Toc153956171 \h 6
1.3	Scope	 PAGEREF _Toc153956172 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 7
2.2	Architecture	 PAGEREF _Toc153956175 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 9
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153956177 \h 10
3.1	Scope	 PAGEREF _Toc153956178 \h 10
3.2	Source Message Schema	 PAGEREF _Toc153956179 \h 10
3.3	Message Transport Details	 PAGEREF _Toc153956180 \h 14
3.4	Naming and Configuration	 PAGEREF _Toc153956181 \h 14
3.5	Environment and Security Context	 PAGEREF _Toc153956182 \h 15
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153956183 \h 16
4.1	Scope	 PAGEREF _Toc153956184 \h 16
4.2	Data Validation	 PAGEREF _Toc153956185 \h 16
4.3	Filtering	 PAGEREF _Toc153956186 \h 16
4.4	Mapping	 PAGEREF _Toc153956187 \h 16
4.5	Target Message Schema	 PAGEREF _Toc153956188 \h 16
4.6	Message Format	 PAGEREF _Toc153956189 \h 17
4.7	Message Transport Details	 PAGEREF _Toc153956190 \h 18
4.8	Naming and Configuration	 PAGEREF _Toc153956191 \h 19
4.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 19
4.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 20
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153956194 \h 21
5.1	Scope	 PAGEREF _Toc153956195 \h 21
5.2	Data Validation	 PAGEREF _Toc153956196 \h 21
5.3	Filtering	 PAGEREF _Toc153956197 \h 21
5.4	Mapping	 PAGEREF _Toc153956198 \h 21
5.5	Target Message Schema	 PAGEREF _Toc153956199 \h 21
5.6	Message Transport Details	 PAGEREF _Toc153956200 \h 21
5.7	Environment and Security Context	 PAGEREF _Toc153956201 \h 21
6	Testing Deliverables	 PAGEREF _Toc153956202 \h 22
7	Deployment	 PAGEREF _Toc153956203 \h 23
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 24
8.1	Assumptions	 PAGEREF _Toc153956205 \h 24
8.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 24
Appendix A Volumes	 PAGEREF _Toc153956207 \h 25
Appendix B Glossary	 PAGEREF _Toc153956208 \h 26
Appendix C Document Control	 PAGEREF _Toc153956209 \h 27

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of Till Data Store (TDS) data to the TDS staging tables within the Integration Layer (IL), to GFO. 
Background
GFO needs to keep track of the current stock levels in store for the purposes of reordering.  This is achieved within GFO by aggregating orders by store, price and item on an hourly basis.  The feed that is used to produce this aggregation is data aggregated on a short term basis from the till data store.  This interface specification documents the process of producing this short term aggregated data for GFO from the TDS.

Scope
The Interface Specification covers:

audit requirements across the interface
security requirements across the interface
timing/frequency requirements or constraints
support requirements
the normal processing required at each stage
recovery from failure required at each stage
volumes.

Description and Requirements for the End-to-End Interface
Description of the End-to-End Interface
This interface will run every 5 minutes at the end which imports data from the TDS.  The end of the interface which exports aggregated date to GFO will run every fifteen minutes.  In between either end of the interface the aggregation takes place and the intermediate data is staged with in a SQL 2005 database.  The process is driven by a number of SQL agent jobs running on the server which host the staging database.


Architecture
 EMBED Visio.Drawing.11  


A SQL Agent job drives the above process within the Sales Data Staging Database it runs every 5 minutes however it only executes the aggregation every 15 minutes or every 3 times the agent job runs.

This job will:
Populate ‘TicketDetail_Stage’ and ‘TicketHeader_Stage’ tables with TSD Sales data,
Clear Sales data from ‘TicketDetail_Stage’ and ‘TicketHeader_Stage’ that is over 4 hours old,
Aggregate the sales data every 15 minutes

The aggregation runs in the same job as the import from TDS so that in the case that the import data fails then the aggregation will not run.  This will also lower the load on the tables by ensuring that the job run sequentially

The other end of the interface makes use of RTI 2.0 to extract the data from the staging tables to GFO in a continuous process at a rate of 10000 Chunk Detail rows per run and 1000 Chunk Control rows per run.

This interface consists of two parts
An SSIS package to extract the aggregated sales data and place it the staging tables
An RTI job continuously exporting the latest aggregated data to GFO.


Extraction of Sales Data From TDS to Staging Tables

This stage of the interface will all be contained within an SSIS package, and will comprise of the following steps:

Step 1: Run a stored procedure ‘SelectLastInsetedDatetime’ to Select the maximum InsertedDateTime from the staging tables this is the point from which new records will need to be copied from the TDS.  If the tables are empty the stored procedure will return the current date and time minus some period (fifteen minutes).

Step 2: Run a stored procedure on the TDS called ‘selectDetailForAgregation’ (NAME???) passing the datetime from the previous step as a parameter.  This stored procedure will return all the TicketDetail rows since the value of the parameter passed.

Step 3: Copy the set returned by the previous step to the detail staging table TicketDetail_Stage.

Step 4: Run a stored procedure on the TDS called ‘selectHeaderForAgregation’ (NAME???) passing the datetime from the previous step as a parameter.  This stored procedure will return all the TicketDetail rows since the value of the parameter passed.

Step 5: Copy the set returned by the previous step to the detail staging table TicketHeader_Stage.

Step 6: Set IMOF tackpoint to mark the successful import of  a set of data from the TDS.

Update Pricing and Quantities on Staging Tables

The TDS stores quantities and pricing as integers however this data would often be better represented as decimal data.  Similarly there are a number of reductions that can be applied to each row of sales data this step calculates the original price for each item and stores it in a new row OriginalPrice.  These steps executed by the stored procedure UpdatePricingOnTicketDetailStage simplify the aggregation step considerably and reduce the complexity of the stored procedure and therefore hopefully will improve performance.  

The OriginalPrice column also has a second purpose it marks where the stored procedure has already updated the row.  In the case where the row’s original price column is null then the row has not been updated if it is not null the row has been updated.

Step 1:  Divide all the pricing columns values by 10 for every row where the OriginalPrice is null and the PumpNo is not null.  This updates all rows that have not been updated where the row represent petrol.  Petrol pricing is stored in the TDS as an integer however it is sold by the 10th of a penny this step converts the prices in to pence from 10ths of pence.

Step 2: Divide the Qty by 1000 if the OriginalPrice is null and the QtyIsWeightFlg is true.  This step updates all rows that have not been updated where the item was sold my litres or kilograms but the qty is recorded in either grams or millilitres.  This leaves the table in a state where all quantities are in the same unit as the item in question was sold by.

Step 3: If the PriceOverideFlg is true and the PriceEmbeddedFlg is false and the OriginalPrice is null set the OriginalPrice equal to POOriginalPrice.

Step 4: If the PriceOverideFlg is true and the PriceEmbeddedFlg is false and the OriginalPrice is null and the POOriginalPrice is null set the OriginalPrice equal to Price.

Step 5: If the PriceOverideFlg is true and the PriceEmbeddedFlg is true and the OriginalPrice is null and the EPOriginalPrice is less than POOriginalPrice set the OriginalPrice equal to EPOriginalPrice.

Step 5: If the PriceOverideFlg is true and the PriceEmbeddedFlg is true and the OriginalPrice is null and the EPOriginalPrice is greater than or equal to POOriginalPrice set the OriginalPrice equal to POOriginalPrice.

Step 6: If the PriceOverideFlg is true and the PriceEmbeddedFlg is true and the OriginalPrice is null and the EPOriginalPrice is null and the POOriginalPrice is null set the OriginalPrice equal to Price.

Step 7: If the PriceOverideFlg is false and the OriginalPrice is null set the OriginalPrice equal to Price.

Aggregation

The aggregation step of the agent job will run every time the agent job runs however it will only aggregate the data in the staging tables since the last aggregation every 3 times the stored procedure is called.  This ensures that the aggregation does not run if the SSIS copy from TDS failed as that would have caused the agent job to quit.  The process of aggregation is as follows:

Step 1: Read the RunCount from the AggregationControl table and add one too it.

Step 2: Write the new RunCount form step 1 to the AggregationControl table.

Step 3: If the RunCount is not equal to 3 quit the step with out processing the step 4 onwards.

Step 4: Write a RunCount of 0 to the AggregationControl table.

Step 5: Select the last aggregated time from the AggreagrionControl table and add fifteen minutes too it this will form the start time and the stop time for the aggregation.

Step 6: Aggregate data from the staging tables by store number where both the InsertedDateTime and the EndTransDateTime fall between the start time and the stop time from step 4 into the aggregated staging table CHUNK_CONTROL

Step 7: Aggregate data from the staging tables by store number where the InsertedDateTime falls between the start time and the stop time from step 5 and the EndTransDateTime fall before the start time into the aggregated staging table CHUNK_CONTROL

Step 8: Aggregate data from the staging tables by store number where the InsertedDateTime falls between the start time and the stop time from step 5 and the EndTransDateTime fall after the stop time into the aggregated staging table CHUNK_CONTROL

Step 9: Aggregate data from the staging tables by store number, price, PLU code, and original price where both the InsertedDateTime and the EndTransDateTime fall between the start time and the stop time from step 5 into the aggregated staging table CHUNK_DETAIL

Step 10: Aggregate data from the staging tables by store number, price, PLU code, and original price where the InsertedDateTime falls between the start time and the stop time from step 5 and the EndTransDateTime fall before the start time into the aggregated staging table CHUNK_DETAIL

Step 11: Aggregate data from the staging tables by store number, price, PLU code, and original price where the InsertedDateTime falls between the start time and the stop time from step 5 and the EndTransDateTime fall after the stop time into the aggregated staging table CHUNK_DETAIL

Step 12: Write the stop time from step 5 to the AggregationControl table as the AggregatedUpTo time.

Step 13: Set IMOF tackpoint to mark the successful aggreagtion.

Copy to GFO from CHUNK_DETAIL Staging Table

The aggregated data needs to be copied to GFO on regular basis from the staging tables.  RTI will be used to achieve this.  RTI will select the data from the aggregation staging table continually until all the current data has been copied. It will copy the data in a series of batches to improve performance and ensure that the impact on the GFO tables in minimized. The following steps detail the process.

Step 1: RTI calls the stored procedure SelectChunkDetailForGFO which will return the set of data to be copied to GFO in this batch.

Step 2: The stored procedure selects the ID of detail chunk last copied to GFO from the AggregationControl table.

Step 3: The stored procedure looks up the timestamp of the row with the ID from previous step from the CHUNK_DETAIL table.

Step 4: The stored procedure looks up the DateOfLastAggregated from the AggregationControl table.

Step 5: The stored procedure selects the top 10000 rows between the DateOfLastAggregated from step 5 and the timestamp from step 3 and returns them to RTI.  If there are no records the query returns an empty set to RTI. (Three is also a cross database join at this point to ensure that the data is sent to the correct GFO stream as yet un-designed) 

Step 5: Finally the stored procedure updates the aggregation control table setting the CopiedUpTo column to the ID of last record of the set passed to RTI.

Step 5: With the data returned from the previous steps RTI passes it to a stored procedure on the GFO table called InsertAggData (NAME???) which inserts it in to the correct partition.  (Streams???)

Step 6: RTI notifies IMOF of the successful batch copy.

Copy to GFO from CHUNK_CONTROL Staging Table

This process is much the same as the one outlined in previous section except the voulumes of data are much lower and so the RTI job can run with a longer wait period.

Step 1: RTI calls the stored procedure SelectChunkHeaderForGFO which will return the set of data to be copied to GFO in this batch.

Step 2: The stored procedure selects the ID of header chunk last copied to GFO from the AggregationControl table.

Step 3: The stored procedure looks up the timestamp of the row with the CHUNK_ID from previous step from the CHUNK_HEADER table.

Step 4: The stored procedure looks up the DateOfLastAggregated from the AggregationControl table.

Step 5: The stored procedure selects the top 1000 rows between the DateOfLastAggregated from step 5 and the timestamp from step 3 and returns them to RTI.  If there are no records the query returns an empty set to RTI. (Three is also a cross database join at this point to ensure that the data is sent to the correct GFO stream as yet un-designed) 

Step 5: Finally the stored procedure updates the aggregation control table setting the CopiedControlUpTo column to the CHUNK_ID of last record of the set passed to RTI.

Step 5: With the data returned from the previous steps RTI passes it to a stored procedure on the GFO table called InsertChunkControl (NAME???) which inserts it in to the correct partition.  (Streams???)

Step 6: RTI notifies IMOF of the successful batch copy.

Requirements for the End-to-End Interface

Audit Requirements
The IMOF Trackpoint component will record the successful completion of each stage of this interface.

Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
Data older than 24 hours which has not been copied to GFO will be ignored this period may need to be shortened.
Performance Requirements
Performance for this interface is key the volumes of data could be huge performance testing will be key and performance should be kept in mind at all phases of design and implementation.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
Because aggregation is by store and item, additional stores and items will have an impact on the performance, hence this interface needs to be able to process the maximum no of stores and items envisages for it’s target country.
Operational Support Requirements
Failures raised through the Error Processing component of the IMOF framework. Alert IDs, and how to interface to IMOF Error Processing component TBD.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
None 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required the interface
Scope
This interface will extract and aggregate the sales data from the TDS Staging tables within the IL, and populate another staging table within the IL with this data. This data is then passed to GFO via RTI from the staging table data. The data is also transformed to the required aggregated format within stored procedures.

Source Schema

As the extract is two stages (extract from TDS Staging tables to aggregated sales data staging table, and extract from aggregated data to GFO), there are effectively two sources.

Extract from TDS to Aggregated Sales Staging tables

Source: TicketHeader_Stage and TicketDetail_Stage tables. See section 3.2.2 for schemas.

Target: CHUNK_DETAIL and CHUNK_CONTROL staging table

See section 3.2.4 for extraction and populate details

Extract from Aggregated Sales Staging tables to GFO

Source: CHUNK_DETAIL and CHUNK_CONTROL staging table

Tarrget: CHUNK_DETAIL and CHUNK_CONTROL tables with in GFO



Database Table Schemas

TicketHeader_Stage
Field Name
Type
NULL
InsertedDateTime
datetime
NOTNULL
GeneratedID
int
NOTNULL
StoreNo
int
NOTNULL
POSNo
smallint
NOTNULL
TicketNo
smallint
NOTNULL
EndTransDateTime
datetime
NOTNULL
StartTransDateTime
datetime
NOTNULL
YearWeekDay
smallint
NOTNULL
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
NOTNULL
GeneratedID
int
NOTNULL
StoreNo
int
NOTNULL
POSNo
smallint
NOTNULL
TicketNo
smallint
NOTNULL
EndTransDateTime
datetime
NOTNULL
TransSeqNo
int
NOTNULL
ItemDeptWasteType
tinyint
NOTNULL
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

CHUNK_CONTROL
Field Name
Type
NULL
CR_PART_NO	
char(10)
NULL
INSERTED_DATE
timestamp
NOT NULL
CHUNK_ID
decimal(9, 0)
NOT NULL
RO_NO
datetime
NOT NULL
SALES_DATE
datetime
NOT NULL
SALES_DATE_END
datetime
NOT NULL
START_TIME
datetime
NOT NULL
END_TIME
decimal(2, 2)
NOT NULL
NO_OF_HOURS
char(1)
NULL
DRIP_TYPE
char(1)
NULL
CHUNK_TYPE
smallint
NULL
STATUS
decimal(7, 0)
NULL
GFO_ERROR_CODE
smallint
NULL
SALES_RECORD_CT
decimal(7, 0)
NULL
TOTAL_QUANTITY_SOLD
float
NOT NULL

CHUNK_DETAIL
Field Name
Type
NULL
ID	
uniqueidentifier
NOT NULL
CHUNK_ID
decimal(9, 0)
NOT NULL
BPR_TPN
bigint
NOT NULL
PLU
bigint
NULL
RO_NO
bigint
NOT NULL
ORIGINAL_PRICE
money
NOT NULL
REDUCTION_TYPE
nchar(1)
NULL
TIME_FIRST_SOLD
datetime
NOT NULL
TIME_LAST_SOLD
datetime
NOT NULL
QUANTITY_SOLD
float
NOT NULL
VALUE_LOST_TO_REDUCTION
money
NULL
SELLING_PRICE
money
NULL
STATUS
decimal(7, 0)
NULL
INSERTED_DATE
timestamp
NOT NULL

Extraction and Aggregation from TDS Staging Tables

The sales data is to be aggregated by Store, Price and Item for each fifteen minute period into the CHUNK_DETAIL table.
 
The aggregation query will be as follows:

SELECT DISTINCT  
	Price,
	PluCode,
	StoreNo,
	OriginalPrice,
	SUM(Qty),
	MIN(EndTransDateTime),
	MAX(EndTransDateTime),
	SUM(OriginalPrice*Qty-Price*Qty),
	(
	SELECT CHUNK_ID 
	FROM CHUNK_CONTROL 	
    	WHERE s2.StoreNo = RO_NO
	)
	
	FROM 
		(
			 SELECT 
			 D.[InsertedDateTime]
			,D.[StoreNo]
			,D.[EndTransDateTime]		  
			,D.[Qty]
			,D.[OriginalPrice]
			,D.[Price]
			,D.[PluCode]		  	  
			FROM [TicketDetail_Stage] D INNER JOIN [TicketHeader_Stage] H 
			ON D.[InsertedDateTime] = H.[InsertedDateTime] 
			AND D.[POSNo] = H.[POSNo]
			AND D.[StoreNo] = H.[StoreNo]
			AND D.[TicketNo] = H.[TicketNo]
			AND D.[InsertedDateTime] = H.[InsertedDateTime]
			WHERE H.VoidTicketFlg = 0
			AND H.TrainingModeFlg = 0
			AND H.BadRecordInd = 0
			AND 
			(
				[H].ReturnType = 1 
				OR [H].ReturnType = 2
				OR [H].ReturnType = 3
				OR [H].ReturnType = 0
			)
			AND D.[ItemDeptWasteType]=1
			AND D.[PluCode] IS NOT NULL			
		) AS s2	GROUP BY Price, PluCode, StoreNo, OriginalPrice;

The sales data is also to be aggregated by Store for each fifteen minute period into the CHUNK_DETAIL table.
 
The aggregation query will be as follows:


SELECT DISTINCT 
		[StoreNo],
		MIN(EndTransDateTime),
		MAX(EndTransDateTime),
		@STARTTIME,
		@STOPTIME,
		0.25,
		1,
		1,		
		1,
		0,
		COUNT([InsertedDateTime]),
		SUM(Qty)
		FROM 
		(
			 SELECT 
			 D.[InsertedDateTime]
			,D.[StoreNo]
			,D.[EndTransDateTime]		  
			,D.[Qty]		  	  
			FROM [TicketDetail_Stage] D INNER JOIN [TicketHeader_Stage] H 
			ON D.[InsertedDateTime] = H.[InsertedDateTime] 
			AND D.[POSNo] = H.[POSNo]
			AND D.[StoreNo] = H.[StoreNo]
			AND D.[TicketNo] = H.[TicketNo]
			AND D.[InsertedDateTime] = H.[InsertedDateTime]
			WHERE H.VoidTicketFlg = 0
			AND H.TrainingModeFlg = 0
			AND H.BadRecordInd = 0
			AND 
			(
				[H].ReturnType = 1 
				OR [H].ReturnType = 2
				OR [H].ReturnType = 3
				OR [H].ReturnType = 0
			)
			AND D.[ItemDeptWasteType]=1
			AND D.[PluCode] IS NOT NULL
			AND D.InsertedDateTime < @StopTime
			AND D.InsertedDateTime >= @StartTime
			AND D.EndTransDateTime < @StopTime
			AND D.EndTransDateTime >= @StartTime
		) AS s1 GROUP BY [StoreNo];


Message Transport Details
Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
SQL Server 2005

Source Physical Location


Source Underlying Data Storage Technology
RDBMS

Target System Name
RTI

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

Data Format.
XML			
Delimited		
Positional		

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous		
Asynchronous		
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
Package Name: TOM.JO35GFO.AggregatedSales.ImportFromTDS
Stored Procedure
Name
??? Select detail from TDS
Stored Procedure
Name
??? Select header from TDS
Stored Procedure
Name
SelectLastInsetedDatetime


RTI
Package Name: TOM.JO35GFO.AggregatedSales.ExportToGFO
Stored Procedure
Name
??? Insert detail to GFO
Stored Procedure
Name
??? Insert header to GFO
Stored Procedure
Name
SelectChunkControlForGFO
Stored Procedure
Name
SelectChunkHeaderForGFO

Testing Deliverables
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
The Ticket_Detail will only ever have columns added at the end.
2
OriginalPrice = Price 
where PriceOverideFlg = True
and PriceEmbeddedFlg = True
and POOriginalPrice is Null
and EPOriginalPrice is Null

3
OriginalPrice =  Price
WHERE PriceOverideFlg = True
and PriceEmbeddedFlg = False
and POOriginalPrice is Null
4
The IDS will be hosted on the same server as this solution. 
5
The CR_PART_NO lookup table will be hosted on the same server as the solution.

Outstanding Issues
ID
Issue
To be addressed by
1






















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
HIS
Host Integration Server
A gateway to transferring data between a Mainframe system and another system.

Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.
ODS
Operation Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Customer, etc. ODS's reside in the EIA Layer, and are accessed through the EAI Layer.
TIB
Tesco Integration Bus
The managed service provided by Tesco's EAI Layer for data transportation and the integration of applications with legacy data sources and Operational Data Stores. 'Larger' in concept than the EAI Layer to include implementation details and interfacing between the EAI (integration services) Layer and the EIA (data services) Layer
WOF
Wintel Operational Framework
The Windows software/Intel hardware environment
->
One to Many Relationship
In a Subject hierarchy the entities defined as parent and child symbolize in this way.
<->
Many to Many Relationship
In a Subject hierarchy the relationship between the entities defined with many to many relationship without relationship table symbolize this way.

Commercial Hierarchy (Merchandise Hierarchy) 
Provides a structure for grouping and reporting products. It is used in the commercial areas of the business.  In the ORMS world, the term Merchandise Hierarchy is used to represent what the Tesco business knows as Commercial Hierarchy. Moving forward the term Merchandise Hierarchy is likely to gain wider use, we therefore recommend using the term Display Hierarchy in place of Merchandising Hierarchy.

Display Hierarchy
This is the hierarchy that links products to their location in store. This has been known previously, in Tesco, as the Merchandising Hierarchy. In the ORMS world, the term Merchandise Hierarchy is used to represent what the Tesco business knows as Commercial Hierarchy. Moving forward the term Merchandise Hierarchy is likely to gain wider use, we therefore recommend using the term Display Hierarchy in place of Merchandising Hierarchy. 

Document Control
Change Record

Author
Date
Version
Change Reference, description
B.Wild
19/02/07
V 0.1
First Draft















Related Documents

Author	
Date
Version
Title


















Distribution

Name
Position
Approver/Contributor/Other






























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 22 of  NUMPAGES 25	Date:  SAVEDATE \@ "d MMM yyyy" 16 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Will be updated with details of the new VOB for TOM integration when this is set up.
New section added



























































