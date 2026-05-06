		









`


TOM Integration

Interface Specification
Shipment notification (Bill of lading) to GFO

[J097]






Project BEN Code:
TBC
Author:Chris RippingaleDate:
20/02/2007
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
Chris Rippingale
20/02/2007
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
TBC

Mapping spreadsheet
J097 – BOL OL to GFO Mappings v1.xls
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
5	Testing Deliverables	 PAGEREF _Toc153956202 \h 17
6	Deployment	 PAGEREF _Toc153956203 \h 18
7	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 19
8.1	Assumptions	 PAGEREF _Toc153956205 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 19
Appendix A Volumes	 PAGEREF _Toc153956207 \h 20
Appendix B Glossary	 PAGEREF _Toc153956208 \h 21
Appendix C Document Control	 PAGEREF _Toc153956209 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of an ASN containing a Bill of Lading (BOL) into the Integration Layer (IL), enriched with Purchase Order Details (POD) and sent to Group Forecast and Order system (GFO).

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is the same for both the Turkey and US implementations.

Background
As part of the ordering process GFO requires order details of each delivery sent out to store. This interface contains details of the process of alerting GFO of the ANS.
 
ORWMS is the source of the ASN which contains the BOL and Allocation Number. The ASN is published into the integration layer (via RIB messages in Oracle Retail v12, via files in Oracle Retail v10), and is enriched from the IDS. This interface is concerned with translating data from ASN and IDS to GFO. 
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
The interface is a transform of an ASN, enriched with PO details from IDS and upload into the GFO system via integration layer. The interface will run when an ASN is received and passed in via sequencing component and consists of a BizTalk Orchestration and supporting assembles that extract data from the IDS and format the output target flat file for GFO.

TBC: FULL DESCRIPTIOIN OF WHAT HAPPENS NEEDED HERE?

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk. TBC At the time of writing (2007-02-20) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture

































Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
TBC.
Performance Requirements
Once received the ASN, the interface should be capable of extracting data from the IDS and delivering the resulting to GFO before the identified cut-off time. To be finalised –This must take into account the cut-off point after which any updates from OWRMS will not be interfaced to GFO..
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. There will only ever be a single instance of the IDS and GFO in a TOM implementation and therefore no requirement for multiple files to multiple locations.
Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
Where the interface is implemented into a country in which a multi-byte character set is required to support the national language, the interface and all participating applications must support a multi-byte character set. 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing Required from ORWMS
Scope
The message will be produced by the Oracle Retail Warehouse Management System and published on the RIB using Java Messaging Service (JMS). The RIB message type will specify the operation performed.

The message generated is published to the Retail Integration Bus (RIB) which can have multiple subscribers; one of these subscribers will be this interface.

Source Message Schema
The message is uniquely identified by the ASN Number (equivalent of BOL No). The message format is XML and the schema is located in TBC

Message Transport Details
Feature
Specification
Additional Information
Source System Name
ORWMS

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
TBC

Archiving
Is there a requirement to store the being transformed? Incoming or outgoing data?  All data or a specific subset? For how long should the data be stored?
TBC – handled by framework if necessary

Logging
Should logs be kept of all actions? For how long should these be stored?
TBC – handled by framework if necessary

Error Handling
Specify what processing is required if an error occurs while transferring the data. Is retry required? How many times, with what interval? Is alerting required? Specify handling of duplicate messages.
TBC – handled by framework if necessary


Naming and Configuration

This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

TBC
Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example employing BizTalk this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).

 Account details will be included here once we have visibility of the environments. 
Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.



Processing Required in the Integration Layer
Scope
Shipping Agent monitors the file in the configured location for every new file and submits the same to the remote UNIX –AIX share via FTP.

When the ASN with BOL details is received by the integration layer, these details will be mapped to a common form and stored in the integration data store.

TBC: How does GFO want to react to 354 Deletes?

The ANS message contains items at pack level. A previous interface (D015) will break these packs into item level. Next the ASN is enriched with the POD from a local API. The POD comes from the IDS. This data is added to the ASN message.
Data Validation
Data Validation will be done by the target GFO system.
Filtering
There is no filtering requirement.
Mapping
RIB ASN -> Common ASN -> Denver.
The target flat file is called Denver and specified in 4.5 Target Message Schema

Please refer the mapping spreadsheet at <location> for mapping.
Target Message Schema
Field Name
Start
Length
COBOL Format
Header



01  JLPMA-DENVER-HEADER.                     



    03  JLPMA-FILE-KEY-PM

18
X(18)
    88  DENVER-HEADER VALUE LOW-VALUES.       



    03  FILLER 

2
X(2)
    03  JLPMA-FIRST-KEY-EXTRACTED.            



        05  JLPMA-FIRST-DATE 

8
9(8)
        05  JLPMA-FIRST-TIME 

6
9(6)
        05  JLPMA-FIRST-SEQ-NO 

4
9(4)
    03  FILLER 

2
X(2)
    03  JLPMA-LAST-KEY-EXTRACTED.             



        05  JLPMA-LAST-DATE 

8
9(8)
        05  JLPMA-LAST-TIME 

6
9(6)
        05  JLPMA-LAST-SEQ-NO 

4
9(4)
    03  FILLER 

2
X(2)
    03  JLPMA-MOVEMENTS-EXTRACTED 

7
9(7)
    03  FILLER

2
X(2)
    03  JLPMA-COMPLETION-STATUS-PM

8
X(8)
    03  FILLER

1
X
    03  JLPMA-DATE-CREATED-PM  

8
9(8)
    03  FILLER 

1
X
    03  JLPMA-TIME-CREATED-PM      

6
9(6)
    03  FILLER

1
X
    03  JLPMA-SEQUENCE-NO

10
9(10)
    03  FILLER 

96
X(96)




Detail Record



01  JLPMB-DENVER-DETAIL.                              



     03 JLPMB-FILE-KEY-PM.                             



        05 JLPMB-KEY-DATE-PM

8
9(8)
        05 JLPMB-KEY-TIME-PM            

6
9(6)
        05 JLPMB-KEY-SEQUENCE-NO-PM                    

4
9(4)
     03 JLPMB-DIST-WAREHOUSE-GROUP.                    



        05 JLPMB-DISTRIBUTION-CENTRE-PM                

2
9(2)
        05 JLPMB-WAREHOUSE-PM

2
9(2)
     03 JLPMB-PRODUCT-ID-PM 

9
9(9)
     03 JLPMB-TRANSACTION-TYPE-PM 

4
9(4)
     03 JLPMB-REASON-CODE-PM 

2
X(2)
     03 JLPMB-QUANTITY-PM 

4
S9(4)
     03 JLPMB-MOVEMENT-IN-PM      PIC 

1
X(1) 
     03 JLPMB-WEIGHT-PM 

6
9(4)V99
     03 JLPMB-SOURCE-DESTINATION-PM                    

8
X(8)
     03 JLPMB-REFERENCE-PM 

8
X(8)
     03 JLPMB-SCHEDULED-DELY-DATE-PM 

8
9(8)  
     03 JLPMB-TRANSACTION-ID-PM 

4
X(4)   
     03 JLPMB-BALANCE-ON-HAND-PM 

6
S9(6)
     03 JLPMB-FREE-STOCK-IND-PM 

1
X(01)
     03 JLPMB-PRODUCT-STATUS-PM 

1
9(01)
     03 JLPMB-ORDD-TRADTPN-PM 

7
9(07)
     03 JLPMB-ORDERED-QUANTITY-PM 

4
S9(04)
     03 JLPMB-REFUSAL-REASON-PM 

1
X(01)
     03 JLPMB-VARIABLE-WGT-FORCED-PM 

1
X(01)
     03 JLPMB-PURCHASE-ORDER 

8
X(8)
     03 JLPMB-DENVER-RECEIPT-NO 



     03 JLPMB-RATIO-PACK 

1
X(01)
     03 JLPMB-FILL-UP-TOP-UP 

1
X(01)
        88  FILL-UP-ORDER 

1
“F” or “T”
     03 JLPMB-ORDER-TYPE-PM

1
X(01). 
        88  NORMAL-ORDER-TYPE

1
“N” or “C”
     03 JLPMB-BILLED-ORDER-NUMBER-PM 

6
X(06)
     03 JLPMB-BILLED-ORD-SEG-NUMBER-PM 

3
X(03)
     03 JLPMB-DELIVERY-WAVE-PM 

1
X(01)
     03 JLPMB-CODE-DATE-PM 

8
9(08)
     03 JLPMB-FILLER 

61
X(61)
     03 JLPMB-STOCK-CENTRE-NO 

5
9(5)
     03 FILLER 

3
X(3)




Trailer Record



01  JLDNV-DENVER-BATCH-REC.                 



     03 JLDNV-KEY 

18
X(18)
     03 FILLER 

2
XX
     03 JLDNV-START-DATE 

8
X(8)
     03 JLDNV-START-TIME 

6
X(6)
     03 FILLER 

6
X(6)
     03 JLDNV-END-DATE 

8
X(8)
     03 JLDNV-END-TIME 

6
X(6)
     03 FILLER 

4
X(4)
     03 JLDNV-SEQ-NO 

2
XX
     03 JLDNV-REC-COUNT 

7
X(7)
     03 JLDNV-DL-SYSTEM-MNEMONIC 

2
XX
     03 FILLER

131
X(131)


Message Format
An example of the expected message format
Message Transport Details 

TBC
For messages destined for TOM system, the following applies

Feature
Specification
Additional Information
Source System Name
RTI

Source Platform / OS
WOF

Source Physical Location


Source Underlying Data Storage Technology
File System

Target System Name
CR

Target Platform / OS
UNIX –AIX 5.3

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
If the message cannot be delivered, retry 6 times at 10 minute intervals, then raise alert.

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration
TBC
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 


RTI
Instruction Name: Tesco_TinaB_GFO_File_Delivery
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

On successful delivery of the file to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure the file should be written to the failed files location, and an alert should be raised.


Testing Deliverables
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
BOL number is unique
2
If a Denver or Load Left Off fails, the orchestration fails.

Outstanding Issues
ID
Issue
To be addressed by





Volumes
Glossary

Acronym
Term
Description
ASN
Advanced Shipment Notice
When a lorry leaves DC
Denver
Expected GFO file
Notification of lorry leaving 
SKU
Stock Keeping Unit

EAI
Enterprise Application Integration
The process of meeting the data requirements of applications by providing a message based transport from disparate data sources across all forms of enterprise technology.


































Document Control
Change Record

Author
Date
Version
Change Reference, description
Chris Rippingale
20-02-2007
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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 10 of  NUMPAGES 21	Date:  SAVEDATE \@ "d MMM yyyy" 23 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































