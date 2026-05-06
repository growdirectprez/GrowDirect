		









`


TOM Integration

Interface Specification
Goods Received Note
From ORWMS/ORMS to TIMS


[D028]






Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
29/01/2007
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
29-Jan-2007
V0.1D
Draft
Sankar G
16-Feb-2007
V0.2D
Draft









Reviewers

Name
Date
Version
Position
Sankar G
30-Jan-2007
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


Thomas Harper












Document Source

Related Documents:
1. Directory: rib-120-intg\Documentation WIP\Integration Bus\12.0\Integration Guide\Receiving.htm
File Name: AppointDesc

2. Directory: rwms-120-og.pdf/Appointments/Receipts
File Name: rwms-120-og

3. TIMS_for_USA_BSD

Information Architecture Context diagram
Will be provided

Mapping spreadsheet
D028 - GRN Mapping Document_updated
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
3.3	Message Format	 PAGEREF _Toc155242923 \h 10
3.4	Message Transport Details	 PAGEREF _Toc155242924 \h 10
3.5	Naming and Configuration	 PAGEREF _Toc155242925 \h 11
3.6	Environment and Security Context	 PAGEREF _Toc155242926 \h 11
3.7	Non-Functional Requirements	 PAGEREF _Toc155242927 \h 11
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc155242928 \h 12
4.1	Scope	 PAGEREF _Toc155242929 \h 12
4.2	Data Validation	 PAGEREF _Toc155242930 \h 12
4.3	Filtering	 PAGEREF _Toc155242931 \h 12
4.4	Mapping	 PAGEREF _Toc155242932 \h 12
4.5	Target Message Schema	 PAGEREF _Toc155242933 \h 12
4.6	Message Format	 PAGEREF _Toc155242934 \h 13
4.7	Message Transport Details	 PAGEREF _Toc155242935 \h 13
4.8	Naming and Configuration	 PAGEREF _Toc155242936 \h 14
4.9	Environment and Security Context	 PAGEREF _Toc155242937 \h 14
4.10	Non-Functional Requirements	 PAGEREF _Toc155242938 \h 15
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc155242939 \h 16
5.1	Scope	 PAGEREF _Toc155242940 \h 16
5.2	Data Validation	 PAGEREF _Toc155242941 \h 16
5.3	Filtering	 PAGEREF _Toc155242942 \h 16
5.4	Mapping	 PAGEREF _Toc155242943 \h 16
5.5	Target Message Schema	 PAGEREF _Toc155242944 \h 16
5.6	Message Transport Details	 PAGEREF _Toc155242945 \h 16
5.7	Naming and Configuration	 PAGEREF _Toc155242946 \h 16
5.8	Environment and Security Context	 PAGEREF _Toc155242947 \h 16
5.9	Non-Functional Requirements	 PAGEREF _Toc155242948 \h 16
6	Testing Deliverables	 PAGEREF _Toc155242949 \h 17
7	Deployment	 PAGEREF _Toc155242950 \h 18
8	Assumptions and Outstanding Issues	 PAGEREF _Toc155242951 \h 19
8.1	Assumptions	 PAGEREF _Toc155242952 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc155242953 \h 19
Appendix A Volumes	 PAGEREF _Toc155242954 \h 20
Appendix B Glossary	 PAGEREF _Toc155242955 \h 21
Appendix C Document Control	 PAGEREF _Toc155242956 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Goods Received Note data between Oracle Retail Warehouse Management System (ORWMS) / Oracle Retail Merchandising System (ORMS) and Tesco Internet Management System (TIMS). In turn these details will be published to Suppliers for their corresponding products via TIMS.

This interface is only for US integration.
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORWMS/ORMS and TIMS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Goods Received Note data from ORWMS/ORMS into TIMS.
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
The interface is a report of the Goods Received at ORWMS via RIB message, RIB message will be passed on to RMS. At the same time this message will be captured by JMS adaptor, pass through RIB dissembler and transforms and uploads into the TIMS system via integration layer. The Upload is a full upload in nature. The transformation is a record order change. 

The interface is meant to run at a pre-configured time interval, which on completion is expected to produce a pipe | delimited flat-file (containing Goods Received Note data records) onto the shared location. This shared location would be monitored by TIMS system at time interval. Once the file containing the extracted data appears on the shared location TIMS system should load the data (updates/inserts) into TIMS.

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
The interface should be capable of extracting data (Goods Received Note data from ORWMS/ORMS) from the shared source location and delivering the resulting to TIMS. The Performance will be decided based on volume of data for transformation and upload.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. There will only ever be a single instance of the ORWMS/ORMS and TIMS in a TOM implementation and therefore no requirement for multiple files to multiple locations.
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
The Goods Received Note RIB message gets generated for ORMS by ORWMS. The same RIB message will get transported through JMS adaptor and get converted into standard XML file while passed though RIB dissembler. 

Source Message Schema
ORWMS will create the Goods Received Note file through RIB required for other systems. The structure of the file as defined in ReceivedDesc.xsd is imbedded below.

 EMBED Package  

The source message detail is described further in tabular format.

Record Type
Field Name
DataType
Description
ReceiptDesc
appt_nbr
Number(9)

Begin Sub-Group ‘A’
1:*
Receipt will repeat multiple times under ReceiptDesc
Receipt
dc_dest_id
varchar2(10)

Receipt
po_nbr
varchar2(10)

Receipt
document_type
varchar2(1)

Receipt
asn_nbr
varchar2(30)

Receipt
receipt_type
varchar2(2)

Receipt
from_loc
varchar2(10)

Receipt
from_loc_type
varchar2(1)

Begin Sub-Group ‘AA’
1:*
ReceiptDtl will repeat multiple times under Receipt
ReceiptDtl
item_id
varchar2(25)

ReceiptDtl
unit_qty
Number(12)

ReceiptDtl
receipt_xactn_type
varchar2(1)

ReceiptDtl
receipt_date
RIBDate

ReceiptDtl
receipt_nbr
Number(9)

ReceiptDtl
dest_id
varchar2(10)

ReceiptDtl
container_id
varchar2(20)

ReceiptDtl
distro_nbr
varchar2(10)

ReceiptDtl
distro_doc_type
varchar2(1)

ReceiptDtl
to_disposition
varchar2(4)

ReceiptDtl
from_disposition
varchar2(4)

ReceiptDtl
to_wip
varchar2(6)

ReceiptDtl
from_wip
varchar2(6)

ReceiptDtl
to_trouble
varchar2(2)

ReceiptDtl
from_trouble
varchar2(2)

ReceiptDtl
user_id
varchar2(30)

ReceiptDtl
dummy_carton_ind
varchar2(1)

ReceiptDtl
tampered_carton_ind
varchar2(1)

ReceiptDtl
unit_cost
Number(20)

ReceiptDtl
shipped_qty
Number(12)

ReceiptDtl
weight_uom
varchar2(4)

ReceiptDtl
weight
Number(12)

End Sub-Group ‘AA’


Begin Sub-Group ‘AB’
1:*
ReceiptCartonDtl will repeat multiple times under Receipt
ReceiptCartonDtl
carton_status_ind
varchar2(1)

ReceiptCartonDtl
container_id
varchar2(20)

ReceiptCartonDtl
dest_id
varchar2(10)

ReceiptCartonDtl
receipt_xactn_type
varchar2(1)

ReceiptCartonDtl
receipt_date
RIBDate

ReceiptCartonDtl
receipt_nbr
Number(9)

ReceiptCartonDtl
user_id
varchar2(30)

ReceiptCartonDtl
to_disposition
varchar2(4)

ReceiptCartonDtl
weight
Number(12)

ReceiptCartonDtl
weight_uom
varchar2(4)

End Sub-Group ‘AB’


End Sub-Group ‘A’



Message Format
The source message is in the form of positional flat file from ORWMS and is getting converted into the target XML file format in a package. The following sample message format is the source message format. 

The message format will be provided.

Message Transport Details
Feature
Specification
Additional Information
Source System Name
ORWMS/ORMS

Source Platform / OS
IBM AIX

Source Physical Location


Source Underlying Data Storage Technology
File Share

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
JMS Adapter	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	

Data Format.
RIB Message		
Delimited		
Positional		

Decryption/Encryption
RIB Dissembler

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
Package Name: Tesco_TOM_Integration_GRN_File_for_TIMS
Stored Procedure
Name
USP_Tesco_TOM_Integration_GRN
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
Not Applicable



Processing required in the Messaging Stage of the interface
Scope
BizTalk will collect the XML File/Files created by RIB assembler as input. This ORWMS/ORMS Goods Received Note (GRN) data will get transformed and messaged to the target location where TIMS system will pool for the file. 
Data Validation
There is no data validations requirement.
Filtering
The GRN report produced by ORWMS/ORMS will carry number of Items and the respective quantities received by a warehouse from a supplier. The supplier in turn will be informed on quantity received by the warehouse through TIMS.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Name
Optional
Type
Description
VRN Header
NOT

VARCHAR2(1)
Type of record “H”
DOCNO

NUBMER(8)
RMS VRN number.
DATETIME

DATE
YYYYMMDDhhmmss
Document creation (original)
PONO

NUMBER(8)
Reference to associated PO
PODATE

DATE
YYYYMMDDhhmmss
Date of purchase order
GRNNO

VARCHAR2(15)
?
DLVDATE

DATE
Requested delivery date (from PO)
RETNO
Y
NUMBER(8)
Empty
RETDATE
Y
DATE
Empty
SUPPID

NUMBER(9)
Supplier ID
SITEINV

NUMBER(5)
RMS ID of Tesco invoicing site
SITEDLV

NUMBER(9)
RMS ID of Tesco delivery site
PAYDATE

DATE
Date of payment
VEHICLE

VARCHAR2(10)
Vehicle registration number
STAMP

VARCHAR2(10)
Stamp number (advice number) (blank)
POSITIVE

NUMBER(1)
=1
TOTALQTY

NUMBER(11,3)
Total quantity of VRN in SKU units
CURRENCY

VARCHAR2(3)
VRN currency
Begin Sub-Group ‘A’
1:*
VRN Items will repeat multiple times under VRN Header.
VRN Items
NOT

VARCHAR2(1)
Type of record “L”
LIN

NUMBER(4)
Sequential number of the line item on the VRN
EAN

VARCHAR2(13)
EAN/GS2/BARCODE
If there is more than one EAN, this will be the first Active EAN that is found.
TPN

VARCHAR2(13)
TPN
SPN
Y
VARCHAR2(13)
Supplier product ID (VPN)
STATNO
Y
VARCHAR2(30)
Article statistical code (Intrastat)
CUSTOMS

VARCHAR2(30)
Article customs code
DESCRIPTION

VARCHAR2(35)
Article description
QTYORDER

NUBMER(11,3)
Quantity in units as on purchase order
QTYRECVD

NUMBER(11,3)
Quantity in units as on VRN 
CATPRICE

NUMBER(11,3)
Unit price before discount
NETPRICE

NUMBER(11,3)
Net unit price
VATRATE

NUMBER(6,3)
Actual rate in %
UNIT

VARCHAR2(3)
SKU unit name (UOM)
VATCODE

VARCHAR2(1)
VAT code (S, E)?
End Sub-Group ‘A’




Message Format
The source message is from RMS and is getting converted into the target file format in a package. The following message format is the target message format. 

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

| (Pipe) Delimited
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
Instruction Name: Tesco_TOM_GRN_for_TIMS_File_Delivery
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
Supplier detail is not coming from RWMS. In that case how TIMS will send the GRN Info to the right vendor?
Dave Onyett
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
ORMS
Oracle Retail Merchandising System
Oracle Retail Merchandising System is getting installed for TESCO Merchandising operations in US. This system will govern the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
TIMS
TESCO Internet Management System
TESCO Internet Management System is a gateway for the TESCO suppliers to access the data and give their responses. For TIMS the main data feed will be from RMS.
ORWMS
Oracle Retail Warehouse Management System
ORWMS is getting installed in US. This module is going to manage warehouse operations.




Document Control
Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
29-01-2007
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

Andrew Barker
Engagement Architect

David Onyett
Project Lead






















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 10 of  NUMPAGES 22	Date:  SAVEDATE \@ "d MMM yyyy" 16 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































