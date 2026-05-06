












TOM Commercial

Interface Specification C010US
Price Details from RMS to the Integration Layer










Project BEN Code:

Author:Shaun CallowDate:
 DOCPROPERTY "Doc Issue Date"  \* MERGEFORMAT 25-Jan-2007 
Version:
0.3
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc155514618 \h 3
1.1	Purpose of Document	 PAGEREF _Toc155514619 \h 3
1.2	Background	 PAGEREF _Toc155514620 \h 3
1.3	Scope	 PAGEREF _Toc155514621 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc155514622 \h 3
2.1	Description of the End-to-End Interface	 PAGEREF _Toc155514623 \h 3
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc155514624 \h 3
3	Processing Required from RMS	 PAGEREF _Toc155514625 \h 3
3.1	Scope	 PAGEREF _Toc155514626 \h 3
3.2	Source Message Schema	 PAGEREF _Toc155514627 \h 3
3.3	Message Transport Details	 PAGEREF _Toc155514628 \h 3
4	Processing Required in the Integration Layer	 PAGEREF _Toc155514629 \h 3
4.1	Scope	 PAGEREF _Toc155514630 \h 3
4.2	Data Validation	 PAGEREF _Toc155514631 \h 3
4.3	Filtering	 PAGEREF _Toc155514632 \h 3
4.4	Mapping	 PAGEREF _Toc155514633 \h 3
4.5	Target Message Schema	 PAGEREF _Toc155514634 \h 3
4.6	Message Transport Details	 PAGEREF _Toc155514635 \h 3
5	Assumptions and Outstanding Issues	 PAGEREF _Toc155514636 \h 3
5.1	Assumptions	 PAGEREF _Toc155514637 \h 3
5.2	Outstanding Issues	 PAGEREF _Toc155514638 \h 3
Appendix A Volumes	 PAGEREF _Toc155514639 \h 3
Appendix B Glossary	 PAGEREF _Toc155514640 \h 3
Appendix C Document Control	 PAGEREF _Toc155514641 \h 3

Introduction
Purpose of Document
The purpose of this document is to describe the development required to achieve this interface, in each system that plays a part, including schemas and mappings.

Background
The purpose of the interface is to receive price details from Oracle Retail Management System (RMS) via the Retail Integration Bus (RIB). These messages will be mapped to the Tesco common form and copied to the Integration Data Store (IDS).
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
This interface is the transmission of product details from RMS to the integration layer then onto the integration layer.

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
This interface will initially be used in the US
Legal Requirements
Please provide details of any Specific legal requirements, and include the country whose law will apply:
TBC
Compliance To Standards Requirements
Please provide details of any specific standards that apply, and provide links to where copies of relevant national and international standards can be located:
The interface will be part of The Operating Model and as such must adhere to the standards used for Tesco integration
Processing Required from RMS
Scope
The message will be produced by the Oracle Retail Management System and published on the RIB using Java Messaging Service (JMS). The RIB message type will specify the operation performed.

The message generated is published to the Retail Integration Bus (RIB) which can have multiple subscribers; one of these subscribers will be this interface.

Source Message Schema
The message is uniquely identified by the RIB Message ID. 

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
BizTalk

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
File Drop (Windows) 
                 (XCOM) 
JMS 

Data Format
Indicate the physical format of the message encapsulating the data.
XML  
Delimited 
Positional 

Decryption/Encryption
Is the data encrypted? If so, does it need to be decrypted?
TBC

Decompression/Compression
Is the data compressed? If so does it need to be decompressed?
TBC

Transmission Mode
Synchronous transfers will receive confirmation of completion of the message delivery to final destination. Asynchronous transfers receive confirmation of message reception by the integration layer. Bulk transfers do not have a return message path.

Synchronous 
Asynchronous 
Bulk Data 

Real-time/Scheduled Batch
Is the data sent one change at a time, as the change occurs using real-time messaging? Or are changes communicated on a time schedule using a batch method
Provide scheduling details eg. Time, CA7 dependencies,etc.
Real Time

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
When the price details are received by the integration layer, these details will be mapped to the Tesco common form and stored in the integration data store.
Data Validation
The Integration Layer will check that the data conforms to the input schema, and can be mapped to the common form schema. This will be both type & format (syntax) validation and a semantic (meaning) validation.
Filtering
Source Schema, Column to Filter
Possible Values
Rows with these values pass through
Rows with these values are discarded
TBC – None?
No filtering







Mapping
Datamodel tbl: StoreItemClearPriceChange

Source Data Item
Target Data Item
Comments
LocationID
ClrPrcChgDesc/location
ClrPrcChgDesc.xsd 
ItemNo
ClrPrcChgDesc/ClrPrcChgDtl/Item
ClrPrcChgDesc.xsd
ClearanceID
ClrPrcChgDesc/ClrPrcChgDtl/clearance_id
ClrPrcChgDesc.xsd
SellingUnitClearRetailPrice
ClrPrcChgDesc/ClrPrcChgDtl/selling_unit_retail
ClrPrcChgDesc.xsd
SellingUOM
ClrPrcChgDesc/ClrPrcChgDtl/selling_uom
ClrPrcChgDesc.xsd
SellingCurrency
ClrPrcChgDesc/ClrPrcChgDtl/selling_currency
ClrPrcChgDesc.xsd
LastUpdateDateTime

Database time stamp

Datamodel tbl: ClearPriceChangeEvent

Source Data Item
Target Data Item
Comments
ClearanceID
ClrPrcChgDesc/ClrPrcChgDtl/clearance_id
ClrPrcChgDesc.xsd 
PriceChangeEffectiveDate
ClrPrcChgDesc/ClrPrcChgDtl/ effective_date
ClrPrcChgDesc.xsd
ResetDate
Have a request with Nuno to get this added to the ClrPrcChgDtl message 
NOT FOUND IN RIB MESSAGE * PLEASE CONFIRM *
LastUpdateDateTime

Database time stamp

Datamodel tbl: StoreItemRegPriceChange

Source Data Item
Target Data Item
Comments
LocationID
RegPrcChgDesc/location
RegPrcChgDesc.xsd 
ItemNo
RegPrcChgDesc/RegPrcChgDtl/item
RegPrcChgDesc.xsd
PriceChangeID
RegPrcChgDesc/RegPrcChgDtl/price_change_id
RegPrcChgDesc.xsd
SellingUnitRetailPrice
RegPrcChgDesc/RegPrcChgDtl/selling_unit_retail
RegPrcChgDesc.xsd
SellingUOM
RegPrcChgDesc/RegPrcChgDtl/selling_uom
RegPrcChgDesc.xsd
SellingCurrency
RegPrcChgDesc/RegPrcChgDtl/selling_currency
RegPrcChgDesc.xsd
MultiUnits
RegPrcChgDesc/RegPrcChgDtl/multi_units
RegPrcChgDesc.xsd
MultiUnitRetail
RegPrcChgDesc/RegPrcChgDtl/multi_unit_retail
RegPrcChgDesc.xsd
MultiSellingUOM
RegPrcChgDesc/RegPrcChgDtl/multi_selling_uom
RegPrcChgDesc.xsd
MultiUnitRetailCurrency
RegPrcChgDesc/RegPrcChgDtl/multi_unit_retail_currency
RegPrcChgDesc.xsd
LastUpdateDateTime

Database time stamp



Datamodel tbl: RegularPriceChangeEvent

Source Data Item
Target Data Item
Comments
PriceChangeID
RegPrcChgDesc/RegPrcChgDtl/price_change_id
RegPrcChgDesc.xsd
PriceChangeEffectiveDate
RegPrcChgDesc/RegPrcChgDtl/effective_date
RegPrcChgDesc.xsd
LastUpdateDateTime

Database time stamp
Datamodel tbl: Promotion

Source Data Item
Target Data Item
Comments
PromotionID
PrmPrcChgDesc/PrmPrcChgDtl /promo_id
PrmPrcChgDesc.xsd
PromoName
PrmPrcChgDesc/PrmPrcChgDtl /promo_name
PrmPrcChgDesc.xsd
PromoDescription
PrmPrcChgDesc/PrmPrcChgDtl /promo_description
PrmPrcChgDesc.xsd
StartDate
PrmPrcChgDesc/PrmPrcChgDtl /start_date

PrmPrcChgDesc.xsd
In RPM there is a Promo start and end date – which are not captured on RIB message. I think populating this with the PrmPrcChgDtl dates is incorrect. We are considering removing from the model  – but awaiting clarification on how RPM works.
EndDate
PrmPrcChgDesc/PrmPrcChgDtl /end_date

PrmPrcChgDesc.xsd
As for StartDate
State

NOT FOUND IN RIB MESSAGE * PLEASE CONFIRM *
This too does not exist in a RIB message, so I think we will remove this from the model – but as above am awaiting clarification.
LastUpdateDateTime

Database time stamp

Datamodel tbl:  PromoComponent

Source Data Item
Target Data Item
Comments
PromotionID
PrmPrcChgDesc/PrmPrcChgDtl /promo_id
PrmPrcChgDesc.xsd
PromoComponentID
PrmPrcChgDesc/PrmPrcChgDtl /promo_comp_id
PrmPrcChgDesc.xsd
PromoComponentName
PrmPrcChgDesc/PrmPrcChgDtl/promo_comp_desc

Unsure if this is correct, please confirm?
This is correct. It originally comes RPM_PROMO_COMP.NAME .
LastUpdateDateTime

Database time stamp

Datamodel tbl: PromoComponentDetail

Source Data Item
Target Data Item
Comments
PromotionID
PrmPrcChgDesc/PrmPrcChgDtl /promo_id
PrmPrcChgDesc.xsd
PromotionComponentID
PrmPrcChgDesc/PrmPrcChgDtl /promo_comp_id
PrmPrcChgDesc.xsd
PromotionComponentDetailID
PrmPrcChgDesc/PrmPrcChgDtl /promo_comp_detail_id
PrmPrcChgDesc.xsd
StartDate
PrmPrcChgDesc/PrmPrcChgDtl /start_date
Is this the same value as the one being mapped in table Promotion?
This is the correct mapping – the issue is with the Promotion table (see previous comment). 
EndDate
PrmPrcChgDesc/PrmPrcChgDtl /end_date
Is this the same value as the one being mapped in table Promotion?
As above
ApplyOrder
PrmPrcChgDesc/PrmPrcChgDtl /apply_order

ThresholdID
PrmPrcChgDesc/PrmPrcChgDtl /PrmPrcChgThr/threshold_id
Not currently being used?
Will not be used for the US – but needs to be captured for future use.
BuyItemType
PrmPrcChgDesc/PrmPrcChgDtl/ PrmPrcChgBuyGet/all_ind
NOT FOUND IN RIB MESSAGE * PLEASE CONFIRM *
BuyItemQty
PrmPrcChgDesc/PrmPrcChgDtl/ PrmPrcChgBuyGet/buy_qty
Not currently being used?
LastUpdateDateTime

Database time stamp
PromotionDetailTypeID
(missing from document)
This needs to be derived.
If the next level of the message is:
PrmPrcChgSMp  ‘S’
PrmPrcChgThr  ‘T’
PrmPrcChgBuyGet  ‘B’




Datamodel tbl: StoreItemPromoCompDetail

Source Data Item
Target Data Item
Comments
LocationID
PrmPrcChgDesc/location
PrmPrcChgDesc.xsd
ItemNo
PrmPrcChgDesc/PrmPrcChgDtl/ PrmPrcChgBuyGet/ PrmPrcChgGetItem/item
PrmPrcChgDesc.xsd
PromotionID
PrmPrcChgDesc/PrmPrcChgDtl /promo_id
PrmPrcChgDesc.xsd
PromoComponentID
PrmPrcChgDesc/PrmPrcChgDtl /promo_comp_id
PrmPrcChgDesc.xsd
PromoComponentDetailID
PrmPrcChgDesc/PrmPrcChgDtl /promo_comp_detail_id
PrmPrcChgDesc.xsd
PromoChangeType
PrmPrcChgDesc/PrmPrcChgDtl/ PrmPrcChgSmp /prm_chg_type
PrmPrcChgDesc.xsd
PromoChangeAmount
PrmPrcChgDesc/PrmPrcChgDtl/ PrmPrcChgSmp /prm_chg_value
This will only be populated if PromoChangeType not = 0
PrmPrcChgDesc.xsd
PromoChangeCurrency
Have a request with Nuno to get this added to the PrmPrcChgSmp message 
NOT FOUND IN RIB MESSAGE * PLEASE CONFIRM *
PromoChangePercent
PrmPrcChgDesc/PrmPrcChgDtl/ PrmPrcChgSmp /prm_chg_value
This will only be populated if PromoChangeType  = 0 (i.e. a percentage off promotion)
NOT FOUND IN RIB MESSAGE * PLEASE CONFIRM *
PromoChangeSellingUOM
PrmPrcChgDesc/PrmPrcChgDtl/ PrmPrcChgSmp /promo_selling_uom
PrmPrcChgDesc.xsd
ItemBuyGetRoleInd
This has to be derived:
If PrmPrcChgGetItem message, set to ‘G’ (for a ‘get’ list of products.
 If PrmPrcChgBuyItem message, set to ‘B’ (for a ‘buy’ list of products.

NOT FOUND IN RIB MESSAGE * PLEASE CONFIRM *
LastUpdateDateTime

Database time stamp

I see that you haven’t included the PromotionThreshold and ThresholdInterval tables. I know these are not required in the first instance for the US, but think we should build the generic process to update the IDS.
Target Message Schema
The common form schema for Items can be found in: StoreItemClearPriceChange.xsd and StoreItemRegPriceChange.xsd and PrmPrcChgDesc.xsd
Message Transport Details 
For messages destined for the integration layer, the transport details can be found in 3.6.
 

 Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1




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
Shaun Callow
07 Dec 2006
V0.1 Draft
First issue
James Fullarton
20 Dec 2006
V0.2 Draft
Updated some details










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
Appendix A
Data Volumes
V0.2 Draft
As V0.1





















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



Version  REF DOC_VER Error! Reference source not found., Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 13 of  NUMPAGES 16	Date:  SAVEDATE \@ "d MMM yyyy" 30 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT C001 - Interface Specification





























































