		









`


TOM Integration

Interface Specification for
TESCO Invoice
From ReIM to TIMS


[F014]






Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
04/02/2007
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
04-Feb-2007
V0.1D
Draft













Reviewers

Name
Date
Version
Position
Sankar G
07-Feb-2007
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
File Name: EDI Invoice Upload File based on EDI 812

2. TIMS_for_USA_BSD
3. TOM_TIMS_IN_INTERFACE (3)

Information Architecture Context diagram
Will be provided

Mapping spreadsheet
Will be provided
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc155242912 \h 6
1.1	Purpose of Document	 PAGEREF _Toc155242913 \h 6
1.2	Background	 PAGEREF _Toc155242914 \h 6
1.3	Scope	 PAGEREF _Toc155242915 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc155242916 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc155242917 \h 7
2.2	Architecture	 PAGEREF _Toc155242918 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc155242919 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc155242920 \h 9
3.1	Scope	 PAGEREF _Toc155242921 \h 9
3.2	Source Message Schema	 PAGEREF _Toc155242922 \h 9
3.3	Message Format	 PAGEREF _Toc155242923 \h 12
3.4	Message Transport Details	 PAGEREF _Toc155242924 \h 12
3.5	Naming and Configuration	 PAGEREF _Toc155242925 \h 13
3.6	Environment and Security Context	 PAGEREF _Toc155242926 \h 13
3.7	Non-Functional Requirements	 PAGEREF _Toc155242927 \h 13
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc155242928 \h 14
4.1	Scope	 PAGEREF _Toc155242929 \h 14
4.2	Data Validation	 PAGEREF _Toc155242930 \h 14
4.3	Filtering	 PAGEREF _Toc155242931 \h 14
4.4	Mapping	 PAGEREF _Toc155242932 \h 14
4.5	Target Message Schema	 PAGEREF _Toc155242933 \h 14
4.6	Message Format	 PAGEREF _Toc155242934 \h 15
4.7	Message Transport Details	 PAGEREF _Toc155242935 \h 15
4.8	Naming and Configuration	 PAGEREF _Toc155242936 \h 16
4.9	Environment and Security Context	 PAGEREF _Toc155242937 \h 16
4.10	Non-Functional Requirements	 PAGEREF _Toc155242938 \h 17
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc155242939 \h 18
5.1	Scope	 PAGEREF _Toc155242940 \h 18
5.2	Data Validation	 PAGEREF _Toc155242941 \h 18
5.3	Filtering	 PAGEREF _Toc155242942 \h 18
5.4	Mapping	 PAGEREF _Toc155242943 \h 18
5.5	Target Message Schema	 PAGEREF _Toc155242944 \h 18
5.6	Message Transport Details	 PAGEREF _Toc155242945 \h 18
5.7	Naming and Configuration	 PAGEREF _Toc155242946 \h 18
5.8	Environment and Security Context	 PAGEREF _Toc155242947 \h 18
5.9	Non-Functional Requirements	 PAGEREF _Toc155242948 \h 18
6	Testing Deliverables	 PAGEREF _Toc155242949 \h 19
7	Deployment	 PAGEREF _Toc155242950 \h 20
8	Assumptions and Outstanding Issues	 PAGEREF _Toc155242951 \h 21
8.1	Assumptions	 PAGEREF _Toc155242952 \h 21
8.2	Outstanding Issues	 PAGEREF _Toc155242953 \h 21
Appendix A Volumes	 PAGEREF _Toc155242954 \h 22
Appendix B Glossary	 PAGEREF _Toc155242955 \h 23
Appendix C Document Control	 PAGEREF _Toc155242956 \h 24

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Tesco Invoice data between Retek Invoice Matching (ReIM) and Tesco Internet Management System (TIMS). In turn the Tesco Invoice details will be downloaded from ReIM and be passed on to Supplier through TIMS.

This interface is only for US implementation.
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ReIM and TIMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to download and send Tesco Invoice from ReIM into TIMS.
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
The interface is a report of the Tesco Invoice downloaded from the ReIM system and sent to Suppliers through TIMS system via integration layer. The Upload is a full upload in nature. The transformation is a record order change. The interface is meant to run at a predefined time, which on completion is expected to produce a pipe-| delimited flat-file (containing Tesco Invoice data records) onto the shared location. This shared location would be monitored by TIMS at the same time. Once the file containing the extracted data appears on the shared location TIMS should pick up the file and upload the data (updates/inserts) into TIMS database. The Supplier Invoice data records are extracted from ReIM by EDI 812 batch process and transferred to the shared location in the form of positional flat file.

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
The interface should be capable of extracting data (Tesco Invoice data from ReIM) from the shared source location and delivering the resulting to TIMS. The Performance will be decided based on volume of data for transformation and upload.
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
Tesco Invoice data from ReIM will be downloaded and ultimately pushed into a predefined shared location by the EDI 812 batch process. Once the file has been created, BizTalk will pick up the file from the shared location for necessary transformation.. 

Source Message Schema
TIMS will create the Supplier Invoice file into the shared location. The structure of the file is defined below.

Record NameField NameField TypeDefault ValueOccurs / RequiredDescription / ValidationFHEAD



1:1
D: File header descriptor

Record descriptor
Char(5)
FHEAD
Y
D: File head marker

Line id
Char(10)
0000000001
Y
D: Generated Sequence line number

Gentran ID
Char(5)
DNINV
Y
D: Identifies transaction type

Current date
Char(14)

Y
D: Current date YYYYMMDDHH24MISS format
Begin Group A1:*Mandatory and group can repeat multiple timesTHEAD
Record descriptor
Char(5)
THEAD
1:1
D: Transaction header info

Line id
Char(10)

Y
D: Generated Sequential file line Number

Transaction Number
Number(10)

Y
D: Generated Sequential Transaction Line number. 

Document Type
Char(6)
DBMC for Debit Note-Cost,
DBMQ for Debit Note-Quantity,
CNRC for Credit Note-Cost,
CNRQ for Credit Note-Quantity
Y
D: Describes the type of document being downloaded. The document type will determine the types of detail information that are valid for the document downloaded.
Retrieved from IM_DOC_HEAD.TYPE where type is debit memo, credit note request or credit memo and in Approved or Posted Status.
V: Debit memo, credit note request cost,
credit note request quantity, credit memos in approved status

Vendor Document Number
Number(8)

Y
D: Vendor’s document number. Retrieved from IM_DOC_HEAD.EXT_DOC_ID.

Invoice
Number

Char(6) 


Y
D: Corresponding invoice resolved by the document. Retrieved from IM_DOC_HEAD.REF_DOC.

Vendor ID
Char(10)

Y
D: Vendor for this document. Retrieved from IM_DOC_HEAD.VENDOR

Document Date

Char(14) 
 

Y
D: Date the document was entered into the system in YYYYMMDDHH24MISS format. Retrieved from IM_DOC_HEAD.DOC_DATE 

Order 

Number(8) 

N
D: Order number for this document, if any. Retrieved from IM_DOC_HEAD.ORDER_NO

Location
Number(10) 

N
D: Location for this document, if any. Retrieved from IM_DOC_HEAD.LOCATION.

Location Type
Char(1)

N
D: Location Type for this document if any.
Retrieved from IM_DOC_HEAD.LOC_TYPE 

Terms
Char(15) 

N
Terms Char(15) Terms of this document.
Retrieved from IM_DOC_HEAD.TERMS.

Due Date
Char(14)

N
D: Date the amount due is due from the vendor (YYYYMMDDHH24MISS format). Retrieved from IM_DOC_HEAD.DUE_DATE.

Currency Code
Char(3)

Y
D: Currency code for this document. Retrieved from IM_DOC_HEAD.CURRENCY_CODE.

Exchange Rate
Number(12,4)

N
D: Exchange rate for conversion of document currency to the primary currency. Retrieved from
IM_DOC_HEAD.EXCHANGE_RATE.

Sign Indicator
Char(1) 

Y
Indicates either a positive (+) or a negative (-) total cost.

Total Cost
Number(20,4)

Y
D: Total document cost, including all items and costs on this document. This value is in the document currency. Retrieved from IM_DOC_HEAD.TOTAL_COST.

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) total VAT amount.

Total VAT Amount
Number(20,4)

N
D: Total VAT amount, including all items and costs on this document. This value is in the document currency.

Sign Indicator
Char(1) 

Y
D: Indicates a positive (+) or a negative (-) quantity.

Total Quantity
Number(12,4)

Y
D: Total quantity of items on this document. This value is in EACHES (no other units of measure are supported in ReIM).  Retrieved from
IM_DOC_HEAD.TOTAL_QTY.
Begin Sub-Group AA1:*Mandatory and subgroup can repeat multiple times within Group ATDETL
Record descriptor
Char(5)
TDETL
1:1
D: Transaction Detail info 

Line Id
Number(10) 

Y
D: Sequential file line Number

Transaction Number
Number(10)

Y
D: Internal SKU/Item for this document. This is always sent. Retrieved from
IM_DOC_DETAIL.ITEM.

UPC
Char(25) 

N
D: UPC Char(25) UPC for this detail record. Retrieved from UPC_EAN.UPC (RMS 9.0) or ITEM_MASTER.ITEM (RMS 10.1). This field is sent if available.
Note: UPC is used for RMS 9.0 and Ref-Item is used for RMS 10.1. Ref-Item consists of UPC and UPC-Supp appended together with a separating hyphen (-).

UPC supplement
Number(5)

N
D: Supplement for the UPC. Retrieved from UPC_EAN.UPC_SUPPLEMEN
T. This field is sent if available.
Note: UPC Supp is only valid for 9.0 implementation. For 10.1 implementation, this field will always be blank.

VPN 

Char(30) 

N
D: Vendor Product Number. This field is sent if available. Retrieved from ITEM_SUPPLIER.VPN.

Comments 

Char(200) 

Y
D: Comments associated with Reason Code. Retrieved from IM_DOC_DETAIL_COMMENTS.TEXT

Reason Code 
Char(6) 

Y
D: Reason Code for this document. Retrieved from IM_DOC_DETAIL_REASON_CODES.REASON_CODE_ID

Reason Code Description
Char(50) 


Y
D: Description associated with Reason Code. Retrieved from
IM_REASON_CODES.REASO
N_CODE_DESC

Sign Indicator
Char(1) 

Y
D: Indicates a positive (+) discrepant qty.

Discrepant Quantity

Number(12,4) 


Y
D: Quantity, in EACHES, of the item that is discrepant for this detail record. Retrieved from
IM_DOC_DETAIL_REASON_CODES.ADJUSTED_QTY.

Sign Indicator
Char(1) 

Y
Indicates either a positive (+) or a negative (-) discrepant cost.

Discrepant cost 

Number(20,4) 

Y
D: Unit cost, in document currency, of the item that is discrepant for this detail record. Retrieved from IM_DOC_DETAIL_REASON_CODES.ADJUSTED_UNIT_COST.

Original VAT Code
Char(6)

Y
D: VAT code for item

Original VAT Rate
Number(20,10)

Y
D: VAT Rate for the VAT code/item
End Sub-Group AABegin Sub-Group AB1:*Mandatory and subgroup can repeat multiple times within Group A
TNMRC – Non-Merchandise Record. Records of this type will contain non-merchandise costs. These costs are retrieved from the IM_DOC_NON_MERCH table. Non-merchandise cost records are only required when the document type is non-merchandise. Non-merchandise cost records are also associated with merchandise type documents if the vendor associated with the document allows non-merch costs on merchandise
invoices (IM_SUPPLIER_OPTIONS. MIX_MERCH_NON_MERCH_IND).TNMRC
Record Descriptor
Char(5) 
TNMRC
1:1
D: Describes file record type. Value TNMRC

Line ID
Number(10)

Y
D: Generated Sequential file line number.

Transaction Number
Number(10) 

Y
D: Generated Transaction number for this non-merchandise record.

Non Merchandise code
Char(6)

Y
Non-Merchandise code that describes this cost. Retrieved from IM_DOC_NON_MERCH.NON_MERCH_CODE.

Sign Indicator
Char(1)

Y
D: Indicates either a positive (+) or a negative (-) non merchandise amount.

Non-Merchandise Amt
Number (20,4)

Y
D: Cost in the document currency.
Retrieved from IM_DOC_NON_MERCH.NON_
MERCH_AMT.

Non-Merch VAT Code
Char(6)

Y
D: VAT Code for Non-Merchandise

Non-Merch VAT code at this VAT code
Number (20,4)

Y
D: VAT Rate corresponding to the VAT code
End Sub-Group ABBegin Sub-Group AC1:*Mandatory and subgroup can repeat multiple times within Group ATVATS
File record descriptor
Char(5)
TVATS
1:1
D: VAT detail info

Line Id
Char(10)

Y
D: Generated Sequential file line number.

Transaction Number
Number(10)

Y
D: Generated Transaction number for this VAT record.

VAT code
Char(6)

Y
D: VAT code that applies to cost

VAT rate
Number(20,10)

Y
D: VAT rate corresponding to VAT code

Sign Indicator
Char(1) 

Y
D: Indicates either a positive (+) or a negative (-) Original Document Quantity Amount. 

VAT Basis 

Number(20,4) 

Y
D: Total amount that must be taxed at the above VAT code
End Sub-Group ACTTAIL
Record Descriptor
Char(5)
TTAIL
1:1
D: Value is TTAIL. This will describe the end of transaction.

Line id 
Number(10) 

Y
D: Generated Sequential file line number.

Transaction number
Number(10) 

Y
D: Generated Transaction number for the transaction that this record is closing.

Transaction Lines
Number(6)

Y
D: Total number of detail lines within this transaction.
End Group AFTAIL
Record Descriptor
Char(5)

1:1
D: Describes file record type. FTAIL – File TAIL. Marks the end of the upload file.

Line Id
Number(10)

Y
D: Generated Sequential file line number

Number of lines
Number(10) 

Y
D: Total number of lines within this file excluding FHEAD and FTAIL.

Message Format
The source message is in the form of positional flat file from ReIM and is getting converted into the target pipe | Delimited flat file format in a package. The following sample message format is the source message format. 

The message format will be provided.

Message Transport Details
Feature
Specification
Additional Information
Source System Name
ReIM

Source Platform / OS
IBM AIX

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
File Drop(Windows) 	
RTI Adapter	 	

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

SSIS
Package Name: Tesco_TOM_Integration_TescoInvoice_File_for_TIMS
Stored Procedure
Name
USP_Tesco_TOM_Integration_TescoInvoice
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable



Processing required in the Messaging Stage of the interface
Scope
BIzTalk will collect the positional flat File/Files created ReIM by EDI 812 Batch Process to the shared location as input. This Supplier Invoice data will get transformed into a pipe delimited flat file and subsequently messaged to the target location from where TIMS will pick up the file and finally will send the Tesco Invoice to the Supplier.
Data Validation
There is no data validations requirement.
Filtering
No filtering is required at this stage.
Mapping
Mapping document will be provided subsequently.
Target Message Schema

Name
Optional
Type
Description
Invoice Header
RECTYPE

CHAR(1)
=H
DOCTYPE

CHAR(6)
Invoice type ="TIN" – TESCO Invoice
=”TDB” – TESCO Debit Note
DOCNO

CHAR(30)
Invoice number
SUPPTPYE

CHAR(6)
="SUPP" for Debit Notes
=”CUST” for TESCO Invoice
SUPPID

CHAR(10)
Partner ID
INVOICE_DATE

CHAR(14)
Timestamp, when invoice/Debit Note was created
SOURCE_DOCNO

NUMBER(10)
PO number/Return number/Original supplier invoice number
LOCATION

NUMBER(10)
TESCO delivery point for Debit Note
Customer Delivery Point for TESCO’s Invoice
DUE_DATE

CHAR(14)
Due Date
PAYMETHOD

CHAR(6)
Invoice payment method =B (bank transfer) =D (direct debit) =C (cash)
CURRENCY

CHAR(3)
Invoice currency
INVOICE_TOTAL

NUMBER(20,4)
Total invoice amount including VAT
TOTAL_VAT
Y
NUMBER(20,4)
Total amount of VAT on invoice
TOTAL_QTY

NUMBER(12,4)
Total Quantity
SUPP_BANKID
 
CHAR(30)
TESCO bank account  
SUPP_VATID
Y
CHAR(20)
Country specific value 
INVOICEE_VATID
Y
CHAR(20)
Country specific value 
DN_NUMBER
Y
CHAR(16)
Delivery number  
DELIVERY_DATE
Y
CHAR(8)
Delivery date
Begin Group ‘A’
1:*
InvoiceItem will repeat multiple times under InvoiceHeader
Invoice Item
RECTYPE

CHAR(1)
=L
UPC

CHAR(25)
OCC/UPC/EAN/GS1/BARCODE
QUANTITY

NUMBER(12,4)
Invoiced quantity
UNIT_PRICE

NUMBER(20,4)
Unit price
VAT_CODE
Y
CHAR(6)
VAT code
VAT_RATE
Y
NUMBER(20,10)
VAT rate
UOM
Y
NUMBER(3)
Country specific value (EACHES)
DESC
Y
CHAR(35)
Country specific value
TPN

CHGAR(14)
TPN
End Group ‘A’


Begin Group ‘AA’
1:*
InvoiceVATRate will repeat multiple times under InvoiceHeader
Invoice VAT Rate
RECTYPE
Y
CHAR(1)
=V
VAT_CODE
Y
CHAR(6)
VAT code
VAT_RATE
Y
NUMBER(20,10)
VAT rate
VAT_AMOUNT
Y
NUMBER(20,4)
Calculated VAT for given VAT percentage
End Group ‘AA’




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
RDBMS

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
RTI Adapter			

Data Format

XML  				
Delimited 			
Positional 			


| delimited
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
Instruction Name: Tesco_TOM_TescoInvoice_for_TIMS_File_Delivery
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
2
Server Physical Location of the server and file 

3
Error handling

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
ORMS
Oracle Retail Merchandising System
Oracle Retail Merchandising System is getting installed for TESCO Merchandising operations in US. This system will govern the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
TIMS
TESCO Internet Management System
TESCO Internet Management System is a gateway for the TESCO suppliers to access the data and give their responses. For TIMS the main data feed will be from RMS.
ReIM
Retek Invoice Matching
ReIM will be installed in US for uploading the supplier’s invoice, Invoice matching, Sending the Debit not to the supplier and ultimately sending the payment advice to the Internal Financial System.
EDI 812
Electronic Data Exchange 812
This is batch file which downloads Tesco invoice/debit notes from ReIM tables.




Document Control
Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
04-02-2007
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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 12 of  NUMPAGES 24	Date:  SAVEDATE \@ "d MMM yyyy" 7 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































