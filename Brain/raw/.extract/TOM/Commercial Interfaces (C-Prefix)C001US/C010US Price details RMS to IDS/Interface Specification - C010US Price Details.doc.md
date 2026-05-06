












TOM Commercial

Interface Specification C010US
Price Details from RMS to the Integration Layer










Project BEN Code:

Author:Shaun CallowDate:
 DOCPROPERTY "Doc Issue Date"  \* MERGEFORMAT 07-Dec-2006 
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.2 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc155514618 \h 3
1.1	Purpose of Document	 PAGEREF _Toc155514619 \h 3
1.2	Background	 PAGEREF _Toc155514620 \h 3
1.3	Scope	 PAGEREF _Toc155514621 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc155514622 \h 4
2.1	Description of the End-to-End Interface	 PAGEREF _Toc155514623 \h 4
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc155514624 \h 4
3	Processing Required from RMS	 PAGEREF _Toc155514625 \h 6
3.1	Scope	 PAGEREF _Toc155514626 \h 6
3.2	Source Message Schema	 PAGEREF _Toc155514627 \h 6
3.3	Message Transport Details	 PAGEREF _Toc155514628 \h 6
4	Processing Required in the Integration Layer	 PAGEREF _Toc155514629 \h 8
4.1	Scope	 PAGEREF _Toc155514630 \h 8
4.2	Data Validation	 PAGEREF _Toc155514631 \h 8
4.3	Filtering	 PAGEREF _Toc155514632 \h 8
4.4	Mapping	 PAGEREF _Toc155514633 \h 8
4.5	Target Message Schema	 PAGEREF _Toc155514634 \h 8
4.6	Message Transport Details	 PAGEREF _Toc155514635 \h 8
5	Assumptions and Outstanding Issues	 PAGEREF _Toc155514636 \h 9
5.1	Assumptions	 PAGEREF _Toc155514637 \h 9
5.2	Outstanding Issues	 PAGEREF _Toc155514638 \h 9
Appendix A Volumes	 PAGEREF _Toc155514639 \h 10
Appendix B Glossary	 PAGEREF _Toc155514640 \h 11
Appendix C Document Control	 PAGEREF _Toc155514641 \h 12

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








Mapping
ClearPriceChange 

Source Data Item
Target Data Item
Comments
LocationID
location

ItemNo
Item

ClearPriceChange
clearance_id

SellingUnitClearPrice
selling_unit_retail

SellingUOM
selling_uom

SellingCurrency
selling_currency


RegularPriceChange
Source Data Item
Target Data Item
Comments
LocationID
location

ItemNo
item

PriceChangeID
price_change_id

SellingUnitRetailPrice
selling_unit_retail

SellingUOM
selling_uom

SellingCurrency
selling_currency


Promotion

Source Data Item
Target Data Item
Comments
PromotionID
promo_id

PromoName
promo_name

PromoDescription
promo_description

StartDate
start_date

EndDate
end_date

State

NOT FOUND IN RIB MESSAGE

PromoComponent

Source Data Item
Target Data Item
Comments
PromotionID
promo_id

PromoComponentID
promo_comp_id

PromoComponentName

NOT FOUND IN RIB MESSAGE

PromoComponentDetail

Source Data Item
Target Data Item
Comments
PromotionID
promo_id

PromotionComponentID
promo_comp_id

PromotionComponentDetailID
promo_comp_detail_id

StartDate
start_date
Is this the same value as the one being mapped in table promotion?
EndDate
end_date
Is this the same value as the one being mapped in table promotion?
ApplyOrder
apply_order

ThresholdID
threshold_id
Not currently being used
BuyItemType

NOT FOUND IN RIB MESSAGE
BuyItemQty
buy_qty
Not currently being used

StoreItemPromoCompDetail

Source Data Item
Target Data Item
Comments
LocationID
location

ItemNo
item

PromotionID
promo_id

PromotionComponentID
promo_comp_id

PromotionComponentDetailID
promo_comp_detail_id

PromotionComponentID
promo_comp_id

PromoChangeType
prm_chg_type

PromoChangeAmount
prm_chg_value

PromoChangeCurrency

NOT FOUND IN RIB MESSAGE
PromoChangePercent

NOT FOUND IN RIB MESSAGE
PromoChangeSellingUOM
promo_selling_uom


Target Message Schema
The common form schema for Items can be found in .\ StoreItemClearPriceChange.xsd and \ StoreItemRegPriceChange.xsd.
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





























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT ii of  NUMPAGES 14	Date:  SAVEDATE \@ "d MMM yyyy" 2 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture































































