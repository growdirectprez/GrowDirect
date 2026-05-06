		









`


TOM Integration

Interface Specification
Invoice from Supplier
From TIMS to ReIM


[F004]






Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
31/01/2007
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1 
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
02-Feb-2007
V0.1D
Draft













Reviewers

Name
Date
Version
Position
Sankar G
05-Feb-2007
V0.1D















At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer

Position

Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version
David Onyett
<Issue Date>
<Version No>
Sankar G


Venkateswara Rao















Document Source

Related Documents:
1. Directory: ReIM-12\invoicematch\pdf\120\reim-120-og.pdf\Interfaces and File layouts
File Name: EDI Invoice Upload File based on EDI 810

2. TIMS_for_USA_BSD
3. TOM_TIMS_IN_INTERFACE (3)
Information Architecture Context diagram
Will be provided

Mapping spreadsheet
Will be provided
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc155242912 \h 3
1.1	Purpose of Document	 PAGEREF _Toc155242913 \h 3
1.2	Background	 PAGEREF _Toc155242914 \h 3
1.3	Scope	 PAGEREF _Toc155242915 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc155242916 \h 3
2.1	Description of the End-to-End Interface	 PAGEREF _Toc155242917 \h 3
2.2	Architecture	 PAGEREF _Toc155242918 \h 3
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc155242919 \h 3
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc155242920 \h 3
3.1	Scope	 PAGEREF _Toc155242921 \h 3
3.2	Source Message Schema	 PAGEREF _Toc155242922 \h 3
3.3	Message Format	 PAGEREF _Toc155242923 \h 3
3.4	Message Transport Details	 PAGEREF _Toc155242924 \h 3
3.5	Naming and Configuration	 PAGEREF _Toc155242925 \h 3
3.6	Environment and Security Context	 PAGEREF _Toc155242926 \h 3
3.7	Non-Functional Requirements	 PAGEREF _Toc155242927 \h 3
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc155242928 \h 3
4.1	Scope	 PAGEREF _Toc155242929 \h 3
4.2	Data Validation	 PAGEREF _Toc155242930 \h 3
4.3	Filtering	 PAGEREF _Toc155242931 \h 3
4.4	Mapping	 PAGEREF _Toc155242932 \h 3
4.5	Target Message Schema	 PAGEREF _Toc155242933 \h 3
4.6	Message Format	 PAGEREF _Toc155242934 \h 3
4.7	Message Transport Details	 PAGEREF _Toc155242935 \h 3
4.8	Naming and Configuration	 PAGEREF _Toc155242936 \h 3
4.9	Environment and Security Context	 PAGEREF _Toc155242937 \h 3
4.10	Non-Functional Requirements	 PAGEREF _Toc155242938 \h 3
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc155242939 \h 3
5.1	Scope	 PAGEREF _Toc155242940 \h 3
5.2	Data Validation	 PAGEREF _Toc155242941 \h 3
5.3	Filtering	 PAGEREF _Toc155242942 \h 3
5.4	Mapping	 PAGEREF _Toc155242943 \h 3
5.5	Target Message Schema	 PAGEREF _Toc155242944 \h 3
5.6	Message Transport Details	 PAGEREF _Toc155242945 \h 3
5.7	Naming and Configuration	 PAGEREF _Toc155242946 \h 3
5.8	Environment and Security Context	 PAGEREF _Toc155242947 \h 3
5.9	Non-Functional Requirements	 PAGEREF _Toc155242948 \h 3
6	Testing Deliverables	 PAGEREF _Toc155242949 \h 3
7	Deployment	 PAGEREF _Toc155242950 \h 3
8	Assumptions and Outstanding Issues	 PAGEREF _Toc155242951 \h 3
8.1	Assumptions	 PAGEREF _Toc155242952 \h 3
8.2	Outstanding Issues	 PAGEREF _Toc155242953 \h 3
Appendix A Volumes	 PAGEREF _Toc155242954 \h 3
Appendix B Glossary	 PAGEREF _Toc155242955 \h 3
Appendix C Document Control	 PAGEREF _Toc155242956 \h 3

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Supplier Invoice data between Retek Invoice Matching (ReIM) and Tesco Internet Management System (TIMS). In turn the Supplier Invoice details will be uploaded to ReIM from the Supplier via TIMS.

This interface is only for US integration.
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ReIM and TIMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to upload and receive Supplier Invoice from TIMS into ReIM.
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
The interface is a report of the Invoice received from the Suppliers through TIMS and uploads into the ReIM system via integration layer. The Upload is a full upload in nature. The transformation is a record order change. The interface is meant to run real time basis, which on completion is expected to produce a positional flat-file (containing Supplier Invoice data records) onto the shared location. This shared location would be monitored by ReIM EDI 810 batch process at the same interval. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into ReIM. The Supplier Invoice data records comes from TIMS in the form of pipe | delimited flat file.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture
 EMBED Visio.Drawing.11  
Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be decided
Performance Requirements
The interface should be capable of extracting data (Supplier Invoice data from TIMS) from the shared source location and delivering the resulting to ReIM. The Performance will be decided based on volume of data for transformation and upload.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. There will only ever be a single instance of the ReIM and TIMS in a TOM implementation and therefore no requirement for multiple files to multiple locations.
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
Supplier Invoice data will be pushed into a predefined shared location by TIMS. Once the file has been created the BizTalk will pick up the file from the shared location. 

Source Message Schema
TIMS will create the Supplier Invoice file into the shared location. The structure of the file is defined below.

Name
Optional
Type
Description
Invoice Header
Record type

CHAR(1)
=H
Document type

CHAR(6)
Invoice type ="MRCHI"
Vendor Document Number

CHAR(30)
Invoice number
Vendor Type

CHAR(6)
="SUPP"
Vendor ID

CHAR(10)
Supplier ID
Vendor Document Date

CHAR(14)
Timestamp, when invoice record was inserted
Order Number / RTV order number

NUMBER(10)
PO number
Location

NUMBER(10)
TESCO delivery point
Location Type

CHAR(1)
Location type ="S" (Store) ="W" (Warehouse)
Terms
Y
CHAR(15)
Empty
Due Date
Y
CHAR(14)
Empty
Payment method
Y
CHAR(6)
Invoice payment method =B (bank transfer) =D (direct debit) =C (cash)
Currency code

CHAR(3)
Invoice currency
Exchange rate
Y
NUMBER(12,4)
Empty
Total cost
Y
NUMBER(20,4)
Total invoice amount including VAT
Total VAT amount
Y
NUMBER(20,4)
Total amount of VAT on invoice
Total Quantity

NUMBER(12,4)
Total Quantity
Total Discount

NUMBER(12,4)
=0
Freight type
Y
CHAR(6)
Empty
Paid Ind.

CHAR(1)
="N"
Multi-location

CHAR(1)
Invoice relating to multiple stores
Consignment indicator

CHAR(1)
="N"
Deal Id
Y
NUMBER(10)
Empty
Deal Approval Indicator
Y
CHAR(1)
Empty
RTV indicator

CHAR(1)
="N"
Custom Document Reference 1
Y
CHAR(30)
Empty
Custom Document Reference 2
Y
CHAR(30)
Empty
Custom Document Reference 3
Y
CHAR(30)
Empty
Custom Document Reference 4
Y
CHAR(30)
Empty
Crossreference document number 
Y
NUMBER(10)
Empty
Supplier bank account number
Y
CHAR(30)
Country specific value 
Supplier VAT registration number
Y
CHAR(20)
Country specific value 
Invoicee VAT registration number
Y
CHAR(20)
Country specific value 
Delivery number
Y
CHAR(16)
Country specific value 
Delivery date YYYYMMDD
Y
CHAR(8)
Country specific value
Begin Group ‘A’
1:*
InvoiceItem will repeat multiple times under InvoiceHeader
Invoice Item
Record type

CHAR(1)
=L
UPC

CHAR(25)
UPC/EAN/GS1/BARCODE
UPC supplement
Y
NUMBER(5)
Empty
Item
Y
CHAR(25)
empty (Retek item number)
Original Document Quantity

NUMBER(12,4)
Invoiced quantity
Original Unit cost

NUMBER(20,4)
Unit price
Original VAT code
Y
CHAR(6)
VAT code
Original VAT rate
Y
NUMBER(20,10)
VAT rate
Total allowance
 
NUMBER(20,4)
=0
SWW code
Y
CHAR(20)
Country specific value
PKWiU code
Y
CHAR(20)
Country specific value
Unit of measure
Y
NUMBER(3)
Country specific value (EACHES)
Article description
Y
CHAR(35)
Country specific value
Destination site
Y
CHAR(10)
Country specific value
Comment
Y
CHAR(70)
Country specific value
End Group ‘A’


Begin Group ‘AA’
1:*
InvoiceVATRate will repeat multiple times under InvoiceHeader
Invoice VAT Rate
Record type
Y
CHAR(1)
=L
VAT code
Y
CHAR(6)
VAT code
VAT rate
Y
NUMBER(20,10)
VAT rate
Cost at this VAT code
Y
NUMBER(20,4)
Calculated VAT for given VAT percentage
End Group ‘AA’



Message Format
The source message is in the form of pipe | delimited flat file from TIMS and is getting converted into the target positional flat file format in a package. The following sample message format is the source message format. 

The message format will be provided.

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
RDBMS

Target System Name
Biztalk 2006

Target Platform / OS
Windows 2006

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
RTI file adaptor		
File Drop(Windows) 	
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

BizTalk
Package Name: Tesco_TOM_Integration_SupplierInvoice_File_for_ReIM
Stored Procedure
Name
USP_Tesco_TOM_Integration_SupplierInvoice
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable



Processing required in the Messaging Stage of the interface
Scope
BIzTalk will collect the pipe delimited File/Files created by TIMS at the shared location as input. This Supplier Invoice data will get transformed and messaged to the target location from where ReIM EDI 810 Batch Process will pick up the file and subsequently upload into the ReIM tables. 
Data Validation
The data validation will be based on the necessities at ReIM EDI 810 Batch process requirements. The validations explained extensively in the target message structure. 
Filtering
The Supplier Invoice report produced by TIMS will carry the Supplier Invoice details including the Item, price and tax details and the respective quantities supplied by the supplier. 
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Record NameField NameField TypeDefault ValueOccurs / RequiredDescription / ValidationFHEAD



1:1
D: File header descriptor

Record descriptor
Char(5)
FHEAD
Y
D: File head marker
V: Halt execution if not FHEAD

Line id
Char(10)
0000000001
Y
D: Sequence line id
V: Halt execution if not 0000000001

Gentran ID
Char(5)
UPINV
Y
D: Identifies transaction type
Halt execution if not UPINV

Current date
Char(14)

Y
D: Current date YYYYMMDDHH24MISS format
V: Halt execution if not valid file format
Begin Group A1:*Mandatory and group can repeat multiple timesTHEAD
Record descriptor
Char(5)
THEAD
1:1
D: Order header info

Line id
Char(10)

Y
D: Sequential file line Number
V: Halt execution if not in sequence

Transaction Number
Number(10)

Y
D: Sequential Line number. All records within transaction will also have this transaction number
V: Reject entire file if transaction number is not numeric or not in sequence or filet transaction number is not 0000000001

Document Type
Char(6)
MRCHI
Y
D: Describes the type of document being uploaded. The document type determines the types of detail information that are valid for the document upload. 
V: Reject Transaction file if document type is not MRCHI

Vendor Document Number
Number(8)

Y
D: Vendor’s document number.
V: Rejects entire upload file if 
The same vendor document occurs more than once in a file
Reject the transaction to file if
Vendor document is null
Vendor document is not alphanumeric
Vendor document contain special characters.


Vendor Type
Char(6)

Y
D: Type of vendor - value ‘SUPP’
V: Reject transaction to file if 
Vendor type is null ot if it not a valid vendor type
Document type is ‘MERCH’ and vendor type is not ‘S’upplier

Vendor ID
Char(10)

Y
D: Vendor for this document
V: Reject transaction to file if
Vendor Id is null
Vendor type is partner and not valid partner
Reject transaction to tables if
Vendor is a supplier and vendor is not valid partner
Vendor is a supplier and vendor ID is not numeric

Vendor Document Date
Char(14) 

Y
D: Date document was issued by the vendor (in YYYYMMDDHH24MISS format).
V: Reject transaction to file if
Vendor document data is null
Date is not a valid date format 

Order Number / RTV Order Number
Number(10)

N
D: Merchandising system order number for this document.
Required for merchandise invoices and optional for others. This field can also contain the RTV order number if the RTV flag is ‘Y’
V: Reject transaction to file if
Order Number / RTV Order Number exists and is not numeric
Order Number / RTV Order Number is null and Vendor type is ‘S’upplier
Order Number / RTV Order Number is null and deal ID is null
Order Number / RTV Order Number exists and vendor type is not a ‘S’upplier
Reject transaction to tables if RTV flag is null or ‘N’ and:
Order number exists but not a valid for the supplier or the supplier’s linked suppliers
Order number exists bit is not valid for location / location type
Reject transaction to tables if RTV flag is ‘Y’ and:
RTV order number exists but is not valid for the  supplier or the supplier’s linked suppliers
RTV order number exists but is not valid for the location / location type

Location
Number(10) 

Y
D: Merchandising system location for this document
V: Reject transaction to file if
Location or Location type do not exist
Location exits but not numeric
Location exists but location type is not ‘S’tore or ‘W’arehouse.
Reject transaction to tables if
Location or Location type does not exists but are not valid 

Location Type
Char(1)

N
D: Merchandising system location type (either ‘S’tore or ‘W’arehouse) for this document.
Required for merchandise invoices and optional for others.
V: Reject transaction to file if
Location type exists and location is null

Terms
Char(15) 

N
D: Terms of this document. If terms are not provided, the vendor’s default terms are associated with this record.
V: Reject transaction to tables if
Terms exists are not valid

Due Date
Char(14)

N
D: Date the amount due is due to the vendor (YYYYMMDDHH24MISS format). If due date is not provided, default due date is calculated based on vendor and terms.
V: Reject transaction to file if
Due date exists and not a valid format
Due date is before the vendor document date

Payment method
Char(6) 

N
D: Method for paying this document.
V: Reject transaction to file if
Payment Method exists and is not valid

Currency Code
Char(3)

Y
D: Currency code for all monetary amounts on this document.
V: Reject transaction to file if
Currency code is null
Currency code is not valid
Order Number exists and currency code does not match the order’s currency

Exchange Rate
Number(12,4)

N
D: Exchange rate *10000 (implied 4 decimal places) for conversion of document currency to the primary currency.
V: Reject transaction to file if
Exchange exists and not numeric

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) total cost amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Total Cost
Number(20,4)

Y
D: Total document cost *10000 (implied 4 decimal places), including all items and costs on this document. This value is in the document currency.
V: Reject transaction to file if
Total Cost is null
Total cost is not numeric
Total cost does not equal the sum of extended costs for all item detail records in the transaction
Total cost is not negative and vendor document type is CRDNT 

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) total VAT amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Total VAT Amount
Number(20,4)

N
D: Total VAT amount *10000 (implied 4 decimal places), including all items and costs on this document. This value is in the document currency.
V: Reject transaction to file if
Total VAT amount is not null but not numeric
Total VAT amount does not equal the sum of VAT for all item detail records PLUS the sum of VAT all Non-Merchandising items in this transaction PLUS the sum of VAT for all allowances in this transaction

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) total quantity amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Total Quantity
Number(12,4)

Y
D: Total quantity of items *10000 (implied 4 decimal places) on this document. This value is in
EACHES (no other units of measure are supported in ReIM).
V: Reject transaction to file if
Total Quantity is null
Total quantity is not numeric
Total quantity does not equal the sum of quantities for all item detail records in this transaction.
Total quantity is not 0 when vendor document type is ‘NMRCHI’

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) total discount amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Total Discount
Number(12,4)

Y
D: Total discount *10000 (implied 4 decimal places) applied to this document. This value is in the document currency.
V: Reject transaction to file if
Total discount is null
Total discount is not numeric

Freight Type
Char(6) 


N
D: NULL The freight method for this document. Always blank.
V: Reject transaction to file if
Freight Type exists and is not valid

Paid Ind
Char(1)


Y
D: Indicates if this document is paid.
V: Reject transaction to file if
Paid Ind is null
Paid Ind is not Y or N

Multi Location
Char(1)

Y
D: Value ‘N’ 
‘Y’ Indicates if this invoice goes to multiple locations.
V: Reject transaction to file if
Multi-location is null
Multi-location is not ‘Y’ or ‘N’
Multi-location is ‘Y’ and Consignment is ‘Y’

Consignment Indicator
Char(1) 

Y
D: Indicates if this invoice is a consignment invoice.
V: Reject transaction to file if
Consignment Indicator is null
Consignment Indicator is not ‘Y’ or ‘N’

Deal Id
Number(10) 

N
D: NULL Deal Id from RMS if this invoice is a deal bill back invoice. Always blank.
V: If Deal Id is not null Deal approval indicator must be ‘M’ or ‘A’
Do not reject transaction to table if deal id is not null

Deal Approval Indicator
Char(1) 

N
D: NULL Indicates if the document on IM_DOC_HEAD is to be created in Approved or Submitted status. Always blank.
V: Reject to file if not blank ‘M’ for submitted status and ‘A’ for approval status.
Do not reject transaction to table if value is not null.

RTV Indicator
Char(1) 

Y
D: Indicates if this invoice is a RTV invoice.
V: Reject transaction to file if
RTV indicator is null
RTV indicator is not ‘Y’ or ‘N’
Do not reject transaction to table if RTV is ‘Y’

Custom Document Reference1
Char(30)

N
D: NULL This optional field is included in the upload file for client customization. No validation is performed on this field. Always blank.

Custom Document Reference2
Char(30)

N
D: NULL This optional field is included in the upload file for client customization. No validation is performed on this field. Always blank.

Custom Document Reference3
Char(30)

N
D: NULL This optional field is included in the upload file for client customization. No validation is performed on this field. Always blank.

Custom Document Reference4
Char(30)

N
D: NULL This optional field is included in the upload file for client customization. No validation is performed on this field. Always blank.

Cross-reference document number
Number(10) 

N
D: Document that a credit note is for.
Blank for all document types other than merchandise invoices.
V: Reject transaction to file if
Cross-reference document number exists and is not numeric
Begin Sub-Group AA1:*Mandatory and subgroup can repeat multiple times within Group ATVATS
File record descriptor
Char(5)
TVATS
1:1
D: VAT detail info

Line Id
Char(10)

Y
D: Sequential line number
V: Halt execution if not in Sequence

Transaction Number
Number(10)

Y
D: Same Transaction Id mentioned in THEAD of this transaction
V: Reject entire file if
Transaction number is not numeric
Transaction number is not the same as the current transaction

VAT code
Char(6)

Y
D: VAT code that applies to cost
V: Reject to file if VAT code is not valid

VAT rate
Number(20,10)

Y
D: VAT rate corresponding to VAT code
V: Reject to file if VAT rate is not numeric

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) total VAT amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Cost at this VAT code
Number(20,4)

N
D: Total amount must be taxed at the above VAT code.
V: Reject to file if not numeric
End Sub-Group AABegin Sub-Group AB1:*Mandatory and subgroup can repeat multiple times within Group ATDETL
Record descriptor
Char(5)
TDETL
1:1
D: Transaction Detail info 

Line Id
Number(10) 

Y
D: Sequential file line Number
V: Halt execution if not in sequence

Transaction Number
Number(10)

Y
D: Same Transaction Id mentioned in THEAD of this transaction
V: Reject entire file if
Transaction number is not numeric
Transaction number is not the same as the current transaction

UPC
Char(25) 

Y
Exclusive with Item
D: NULL UPC for this detail record. Valid item number is retrieved for the UPC. Always blank.
V: Reject entire file if
UPC is null and item is null
Both UPC and item are not null
Reject transaction to file if
Valid Item is not found for UPC and UPC supplement
Valid Item is not associated with supplier
The item found is identical to another detail item for this transaction (no duplicate items)

UPC supplement
Number(5)

N
D: NULL Supplement for the UPC. Always blank.
V: Reject transaction to file if
UPC supplement exist but UPC doesn’t exist
UPC supplement exist but it is not numeric

Item
Char(25)

Y
Exclusive with UPC 
D: Item for this detail record
V: Reject transaction to file if
UPC is null and Item is null
Both UPC and Item are not null
Valid Item is not associated with supplier
The item found is identical to another detail item for this transaction ( No duplicate item)

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) Original quantity amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Original Document Quantity
Number(12,4) 

Y
D: Quantity *10000 (implied 4 decimal places), in EACHES, of the item on this detail record.
V: Reject transaction to file if
Original document quantity is null
Original document quantity is not numeric

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) Original unit cost amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Original Unit cost
Number(20,4)

Y
D: Unit cost *10000 (implied 4 decimal places), in document currency, of the item on this detail record.
V: Reject transaction to file if
Original unit cost is null
Original unit cost is not numeric

Original VAT Code
Char(6)

Y
D: VAT code for item
V: Reject to file if VAT code is invalid 

Original VAT Rate
Number(20,10)

Y
D: VAT Rate for the VAT code/item
V: Reject to file if VAT rate is invalid

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) total allowance.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Total Allowance
Number(20,4)

Y
D: Sum of allowance details for this item detail record *10000 (implied 4 decimal places). If no allowances exist for this item detail record, value is 0
V: Reject transaction to file if
Total allowance is null
Total allowance is not numeric
Total Allowance does not equal the sum of allowance amount for all allowance records in this item detail record
Total allowance is not 0 and vendor document type is CRDNT
End Sub-Group ABBegin Sub-Group AC1:*Mandatory and subgroup can repeat multiple times within Group ATALLW
Record Descriptor
Char(5)
TALLW
1:1
D: Allowance Detail info 

Line Id
Number(10)

Y
D: Sequential file line Number
V: Halt execution if not in sequence

Transaction Number
Number(10)

Y
D: Same Transaction Id mentioned in THEAD of this transaction
V: Reject entire file if
Transaction number is not numeric
Transaction number is not the same as the current transaction

Allowance code
Char(6)

Y
D: Allowance code for this record
V: Reject transaction to file
Allowance code is null
Allowance code is not valid

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) allowance amount.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘ 

Allowance Amount
Number(20,4)

Y
D: Amount of allowance in document currency. 
V: Reject transaction to file if allowance amount is null or non-numeric.

Allowance VAT code
Char(6)

Y
D: VAT code  for allowance
V: Reject to file if VAT code is not valid

Allowance VAT rate at the VAT code
Number(20,10)

Y
D: VAT rate corresponding to the VAT code
V: Reject to file if not numeric
End Sub-Group ACBegin Sub-Group AD1:*Mandatory and subgroup can repeat multiple times within Group ATNMRC
Record Descriptor
Char(5) 
TNMRC
1:1
D: Describes file record type.

Line ID
Number(10)

Y
D: Sequential File line number
V: Halt execution if not in sequence

Transaction Number
Number(10) 

Y
D: Transaction number for this nonmerchandise record. Same Transaction Id mentioned in THEAD of this transaction
V: Reject entire file if 
Transaction number is not numeric
Transaction number is not the same as the current transaction

Non Merchandise code
Char(6)

Y
D: Non-Merchandise code that describes this cost.
V: Reject entire file if
Non-Merchandise code is null
Non-Merchandise code is not valid

Sign Indicator
Char(1)

Y
D: Indicates either a positive (+) or a negative (-) Non Merchandise Amt.
V: Reject transaction to file if
Sign indicator is null or if not ‘+’ or ‘-‘

Non-Merchandise Amt
Number (20,4)

Y
D: Cost *10000 (implied 4 decimal places) in the document currency.
V: Reject transaction to file if
Non-Merchandise Amt is not null
Non-Merchandise Amt is not numeric
Non-Merchandise Amt does not have a negative value and this part of credit note. Document ‘THEAD’ Vendor document type = ‘’CRDNT’

Non-Merch VAT Code
Char(6)

Y
D: VAT Code for Non-Merchandise
V: Reject to file if VAT code is not valid

Non-Merch VAT code at this VAT code
Number (20,4)

Y
D: VAT Rate corresponding to the VAT code
V: Reject to file if not numeric

Service Performed Indicator
Char(1)

Y
D: Indicates if a service has actually performed.
V: Reject to file if 
Service Performed indicator is null
Service Performed indicator id not ‘Y’ or ‘N’

Store
Number(10)


D: Store at which the service was performed.
V: Reject to file if
Store exits and not numeric
Service performed indicator is ‘Y’ and store is not valid
End Sub-Group ADTTAIL
file record type 
Char(5)
TTAIL
1:1
D: Value is TTAIL. This will describe the end of transaction.

Line id 
Number(10) 

Y
D: Sequential File line number
V: Halt execution if not in sequence

Transaction number
Number(10) 

Y
D: Transaction number for the transaction that this record is closing.
V: Reject entire file if
Transaction Number is not numeric
Transaction Number is not the same as the current transaction

Transaction Lines
Number(6)

Y
D: Total number of detail lines within this transaction.
V: Reject transaction to file if transaction lines value is not numeric, if it does not match the count of lines within the transaction, or if it is 0.  
(transaction must have details)
End Group AFTAIL
Record Descriptor
Char(5)

1:1
D: Describes file record type. Value TTAIL 
This indicates that this is end of file

Line Id
Number(10)

Y
D: Sequential File line number
V: Halt execution if not in sequence

Number of lines
Number(10) 


Y
D: Total number of lines within this file excluding FHEAD and FTAIL.
V: halt execution if  number of lines is not numeric or if does not match the count of lines within the file. (excluding FHEAD and FTAIL ) or if it is 2 FHEAD and FTAIL only, file has not transactions.



Message Format
The source message is from TIMS and is getting converted into the target file format in a package. The following message format is the target message format. 

The message format will be provided.

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
ReIM

Target Platform / OS
IBM AIX

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
RTI file adaptor			
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
Instruction Name: Tesco_TOM_SupplierInvoice_for_TIMS_File_Delivery
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





Outstanding Issues
ID
Issue
To be addressed by
1
Server Physical Location of the server and file 

2
Error handling






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
ORMS
Oracle Retail Merchandising System
Oracle Retail Merchandising System is getting installed for TESCO Merchandising operations in US. This system will govern the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
TIMS
TESCO Internet Management System
TESCO Internet Management System is a gateway for the TESCO suppliers to access the data and give their responses. For TIMS the main data feed will be from RMS.
ReIM
Retek Invoice Matching
ReIM will be installed in US for uploading the supplier’s invoice, Invoice matching, Sending the Debit not to the supplier and ultimately sending the payment advice to the Internal Financial System.
EDI 810
Electronic Data Exchange 810
This is batch file which uploads the Suppliers’ invoice to the ReIM tables.













Document Control
Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
03-02-2007
V0.1 Draft
First issue















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

David Onyett
Project Lead

























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 11 of  NUMPAGES 28	Date:  SAVEDATE \@ "d MMM yyyy" 5 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































