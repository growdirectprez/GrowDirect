












TOM Commercial

Interface Specification C001TR
Product Details from RMS to the Integration Layer










Project BEN Code:

Author: AUTHOR  \* MERGEFORMAT James FullartonDate:
01-Jan-2007
Version:
0.1 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc155510261 \h 3
1.1	Purpose of Document	 PAGEREF _Toc155510262 \h 3
1.2	Background	 PAGEREF _Toc155510263 \h 3
1.3	Scope	 PAGEREF _Toc155510264 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc155510265 \h 4
2.1	Description of the End-to-End Interface	 PAGEREF _Toc155510266 \h 4
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc155510267 \h 4
3	Processing Required from RMS	 PAGEREF _Toc155510268 \h 6
3.1	Scope	 PAGEREF _Toc155510269 \h 6
3.2	Source Message Schema	 PAGEREF _Toc155510270 \h 6
3.3	Message Transport Details	 PAGEREF _Toc155510271 \h 6
4	Processing Required in the Integration Layer	 PAGEREF _Toc155510272 \h 8
4.1	Scope	 PAGEREF _Toc155510273 \h 8
4.2	Data Validation	 PAGEREF _Toc155510274 \h 8
4.3	Filtering	 PAGEREF _Toc155510275 \h 8
4.4	Mapping	 PAGEREF _Toc155510276 \h 8
4.5	Target Message Schema	 PAGEREF _Toc155510277 \h 12
4.6	Message Transport Details	 PAGEREF _Toc155510278 \h 12
5	Assumptions and Outstanding Issues	 PAGEREF _Toc155510279 \h 13
5.1	Assumptions	 PAGEREF _Toc155510280 \h 13
5.2	Outstanding Issues	 PAGEREF _Toc155510281 \h 13
Appendix A Volumes	 PAGEREF _Toc155510282 \h 14
Appendix B Glossary	 PAGEREF _Toc155510283 \h 15
Appendix C Document Control	 PAGEREF _Toc155510284 \h 16

Introduction
Purpose of Document
The purpose of this document is to describe the development required to achieve this interface, in each system that plays a part, including any schemas and mappings.

Background
The purpose of the interface is to receive product details from Oracle Retail Management System (RMS). These messages will be mapped to the Integration Data Store (IDS). 
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
This interface is the transmission of product details from RMS to the integration layer.

Requirements for the End-to-End Interface

Audit Requirements
Please provide details of any specific audit trail or audit processing, e.g. headers and trailers, audit reports etc. Note that finance interfaces must have an audit trail:
TBC
Security Requirements
Please provide details of any specific security requirements:
TBC
Timing/cutoff Constraints
Please provide details of any specific timing or cutoff constraints, e.g. that an interface must be received by 1am:
TBC
Performance Requirements
Provide details of any particular performance requirement:
TBC
Reliability and Availability Requirements
Provide details of any particular reliability or availability requirements over and above the normal level of service provided:
TBC
Scalability Requirements
Please provide specific details of any expected increase in the volume/frequency of data that must be accounted for. Include timescales:
TBC	

Operational Support Requirements
Please provide details of any particular operational support requirements over and above the normal level of service provided:
TBC
Likelihood of Change Requirements
If it is know that the specification of the interface is subject to change, please provide details of this requirement:
As this is an iterative approach these requirements will change as and when they are refined
Cultural/Global Consideration Requirements
If there are any specific cultural or global considerations that need to be taken into account in the integrating of any systems mentioned in this document, then please provide details here:
This interface will initially be used in Turkey
Legal Requirements
Please provide details of any Specific legal requirements, and include the country whose law will apply:
TBC
Compliance To Standards Requirements
Please provide details of any specific standards that apply, and provide links to where copies of relevant national and international standards can be located:
The interface will be part of The Operating Model and as such must adhere to the standards used for Tesco integration
Processing Required from RMS
Scope
The message will be produced by the Oracle Retail Management System in a flat file format. The messages will be contain a header and a footer for description of the message payload. The payload itself will be positional delimited with the position determined by the underlying Oracle data type. i.e. Varchar2(20) will have a positional delimiter after 20 characters.

These messages are to be processed at set intervals and copied to the integration data store.

Source Message Schema
The source message schema will be based on the flat file schema.
This is still TBC

Message Transport Details
Feature
Specification
Additional Information
Source System Name
RMS

Source Platform / OS
Oracle Retail

Source Physical Location
TBC

Source Underlying Data Storage Technology
Oracle

Target System Name
Integration Data Store

Target Platform / OS
SSIS

Target Physical Location
TBC

Target Underlying Data Storage Technology
SQL Server

Transfer Function
Indicate which method will be used to transfer data to the next stage.
HTTP (Put/Post) 
HTTPS (Put/Post) 
Message Queue 
FTP 
File Drop (Windows) 
                 (XCOM) 
JMS 

Data Format
Indicate the physical format of the message encapsulating the data.
XML 
Delimited 
Positional 

Decryption/Encryption
Is the data encrypted? If so, does it need to be decrypted?
TBC

Decompression/Compression
Is the data compressed? If so does it need to be decompressed?
TBC

Transmission Mode
Synchronous transfers will receive confirmation of completion of the message delivery to final destination. Asynchronous transfers receive confirmation of message reception by the integration layer. Bulk transfers do not have a return message path.

Synchronous 
Asynchronous ο
Bulk Data ⎭

Real-time/Scheduled Batch
Is the data sent one change at a time, as the change occurs using real-time messaging? Or are changes communicated on a time schedule using a batch method
Provide scheduling details eg. Time, CA7 dependencies,etc.
Batched?

Archiving
Is there a requirement to store the being transformed? Incoming or outgoing data?  All data or a specific subset? For how long should the data be stored?
TBC – handled by framework if necessary

Logging
Should logs be kept of all actions? For how long should these be stored?
TBC – handled by framework if necessary

Error Handling
Specify what processing is required if an error occurs while transferring the data. Is retry required? How many times, with what interval? Is alerting required? Specify handling of duplicate messages.
TBC – handled by framework if necessary



Processing Required in the Integration Layer
Scope
When the product details are received by the integration layer, these details will be stored in the integration data store.
Data Validation
The Integration Layer will check that the data conforms to the input schema, and can be mapped to the integration data store. There will also be checks to determine if the message relates to an item or pack. This will be both type & format (syntax) validation and a semantic (meaning) validation.

Source Data Item
Validation
Item_Level
1,2,3 Determines the level that the item or pack belongs to
Pack_ind
Y/N Determines whether the item is a pack


Pack Indicator Y
Pack Indicator N
Item Level 1	
Pack
Style
Item Level 2
OCC
SKU
Item Level 3
-
EAN
Filtering
Source Schema, Column to Filter
Possible Values
Rows with these values pass through
Rows with these values are discarded
TBC – None?
I don’t believe there is any (so far)








Mapping
Style
Source Data Item
Start Position
Target Data Item
Comments
item

StyleID

section

Section

class

Class

subclass

SubClass

Status

Status

item_desc

ItemDesc



ItemDescSecondary
Mapping unknown
Only appear in ORMS – not RIB message, so will remove it from IDS
short_desc

ItemDescShort

merchandise_ind

MerchandiseInd

-

LastUpdateDateTime
Timestamp

StyleSupplier
Source Data Item
Start Position
Target Data Item
Comments
supplier

SupplierID

supp_label

SupplierLabel

primary_supp_ind

PrimarySupplierInd

supp_discontinue_date

SupplierDiscountDate

-

LastUpdateDateTime
Timestamp

SKUItem
Source Data Item
Start Position
Target Data Item
Comments
item

SKUID

status

Status

item_desc

ItemDesc



ItemDescSecondary
Mapping Unknown
This is on ORMS but not in message – will remove it from the IDS
short_desc

ItemDescShort

standard_uom

StandardUOM

uom_conv_factor

UOMConversionFactor

merchandise_ind

MerchandiseInd

-

LastUpdateDateTime
Timestamp
retail_label_type

RetailLableType

retail_label_value

RetailLabelValue

handling_temp

HandlingTempCode

handling_sensitivity

HandlingSensitivity

catch_weight_ind

CatchWeightInd

const_dimen_ind

ConstantDimensionInd

-

DiamondInd
UDA – will appear in extract
?

ImportItemInd
Mapping unknown
Will be a UDA
-

TescoBrand
UDA – will appear in extract
-

TaxCategory
Waiting for Tax details
Will be a UDA
item_parent

StyleItem

dept

Section

class

Class

subclass

Subclass

orderable_ind

OrderableInd

?

DistributionGroup
UDA? YES
?

OrderGroup
UDA? YES
?

ManualPriceEntryInd
UDA? YES
?

DepositItemReturnCode
UDA? YES
?

CounterScaleInd
UDA? YES
?

POSMessage
UDA? YES
?

SupervisorAuthRqdInd
UDA? YES
?

PlaceOfOrigin
UDA? YES
ticket_type

TicketTypeID
I now believe that this will come from Space, Range & Display, and am awaiting some detail on this.
?

EPISELDescription
UDA? YES
?

EDISELEffectiveDate
UDA? YES
?

EPISELEnd_Date
UDA? YES

SKUSupplier
Source Data Item
Start Position
Target Data Item
Comments
item

ItemNo
SKUID
SKUItemNo is derived from the SKU Item, should this be SKUID in Data Model?
Yes – but think it has been re-named now
supplier

SupplierID

primary_supp_ind

PrimarySupplierInd

supp_diff1

SupplierDiff1
Is this needed?
This should be removed from the physical model
supp_discontinue_date

SupplierDiscontinueDate

-

LastUpdateDateTime
Timestamp

SKUSupplierCountryOfOrigin
Source Data Item
Start Position
Target Data Item
Comments
item

ItemNo
SKUID
SKUItemNo is derived from the SKU Item, should this be SKUID?
Yes –  think it has been re-named now
supplier


SupplierID is derived from the SKU Supplier
origin_country_id

ISOCountryCode

primary_supp_ind

PrimarySuppInd

primary_country_ind

PrimaryCountryInd

-

LastUpdateDateTime
Timestamp


SupplierPackSize


SKUSupplierCountryOfOriginDim
Source Data Item
Start Position
Target Data Item
Comments
item


SKUItemNo is derived from the SKU Item – should be SKUID
supplier


SupplierID is derived from the SKU Supplier
origin_country_id


OriginCountryId is derived from SKU Supplier Country of Origin
dim_object

DimObject

-

LastUpdateDateTime
Timestamp

ArticleItem
Source Data Item
Start Position
Target Data Item
Comments
Item

ArticleID

format_id

FormatID

Prefix

Prefix

Status

Status

primary_ref_item_ind

PrimaryRefItemInd

-

LastUpdateDateTime
Timestamp
item_parent

SKUID






OuterCase
Source Data Item
Start Position
Target Data Item
Comments
Item

OCC

format_id

FormatID

prefix

Prefix

primary_ref_item_ind

PrimaryRefItemInd

item_parent

PackID



LastUpdateDateTime
Timestamp

TradePack
Source Data Item
Start Position
Target Data Item
Comments
Item

PackID

Status

Status

item_desc

PackDesc



PackDesc
Mapping unknown
This is on ORMS but not in message – will remove field from the IDS
Short_desc

PackDescShort

standard_uom

StandardUOM

merchandise_ind

MerchandiseInd

Catch_weight_ind

CatchWeightInd

dept

Section

class

Class

subclass

SubClass



LastUpdateDateTime
Timestamp

TradePackSupplier
Source Data Item
Start Position
Target Data Item
Comments
item

ItemNo
PackID
PackItemNo is derived from the Pack Item, should this be PackID?
Yes
supplier

SupplierID

supp_discontinue_date

SupplierDiscontinueDate

-

LastUpdateDateTime
Timestamp

TradePackSupplierCountryOfOrigin
Source Data Item
Start Position
Target Data Item
Comments
item

ItemNo
PackID
PackItemNo is derived from the Pack Item, should this be PackID?
Yes
supplier

SupplierID
SupplierID is derived from the Pack Supplier
origin_country_id

ISOCountryCode

supp_pack_size

SupplierPackSize



PrimarySupplierInd

-

LastUpdateDateTime
Timestamp


PrimaryCountryInd


PackSupplierCountryOfOriginDim
Source Data Item
Start Position
Target Data Item
Comments
item


PackItemNo is derived from the Pack Item
supplier


SupplierID is derived from the Pack Supplier
origin_country_id


OriginCountryId is derived from Pack Supplier Country of Origin
dim_object

DimObject

-

LastUpdateDateTime
Timestamp


Target Message Schema
The target is the IDS so schema relates to the database schema.
Message Transport Details 
For messages destined for the integration layer, the transport details can be found in 3.6. 



 Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
The Extract will only contain product and supplier details
We will also need to capture the SKUItemInWarehouse captured in ItemLocVirt message from ORMS ITEM_LOC tables) & Commercial hierarchy details, captured in MerchHr…. Messages,  to satisfy requirements for the GFO interface
2
The Extract will be positional delimited

Outstanding Issues
ID
Issue
To be addressed by
1
Unknown Requirements – Anything highlighted in Red
Nikhil Rajwade



Volumes
TBC
Glossary
Acronym
Term
Description
IDS
Integration Data Store
The data store in the integration layer
JMS
Java Messaging Service
The messaging protocol used by Oracle Retail applications
RIB
Retail Integration Bus
Creation of a strategic single view of data across the enterprise.
RMS
Retail Management System
Oracle Retail Management System application

Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.










Document Control
Change Record

Author
Date
Version
Change Reference, description
James Fullarton
01 Jan 2007
V0.1 Draft
First issue














Version
Section
Unknown Requirements
V0.1 Draft
2.2
Requirements for the End to End Interface table
3.3
Encryption, Compression, Auditing, Logging, Security, Error Handling, Source Physical Location, Target Physical Location
4.3
Filtering
4.4
Mappings unknown:
Style – ItemAggregateInd, ItemDescSecondary will request this is removed from model

SKU – ItemDescSecondary, DiamondInd, ImportItemInd, TescoBrand, TaxCategory – all UDAs

SKUSupplier – ConcessionRate  -will request this is removed from model
Pack – PackDescSecondary will request this is removed from model
PackSupplier – RoundToInnerPercent, RoundToCasePercent, RoundTo_LayerPercent, RoundToPalletPercent will request these are removed from model

Appendix A
Data Volumes























Related Documents

Author
Date
Version
Title



Add Pattern, TSD & solutions architecture













Distribution

Name
Position
Approver/Contributor/Other





























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT C001 - Interface Specification



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 16 of  NUMPAGES 17	Date:  SAVEDATE \@ "d MMM yyyy" 31 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT C001 - Interface Specification



Style Supplier has been removed
Has been removed
Has now been removed



























































