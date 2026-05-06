		









`


TOM Integration

Interface Specification
Directs PO Receipt
From Integration Layer to RMS


[D031TR]






Project BEN Code:

Author:Allister GreenDate:
23/02/2007
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
23/02/2007
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
TBC
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
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153956194 \h 16
5.1	Scope	 PAGEREF _Toc153956195 \h 16
5.2	Data Validation	 PAGEREF _Toc153956196 \h 16
5.3	Filtering	 PAGEREF _Toc153956197 \h 16
5.4	Mapping	 PAGEREF _Toc153956198 \h 16
5.5	Target Message Schema	 PAGEREF _Toc153956199 \h 16
5.6	Message Transport Details	 PAGEREF _Toc153956200 \h 16
5.7	Environment and Security Context	 PAGEREF _Toc153956201 \h 16
6	Testing Deliverables	 PAGEREF _Toc153956202 \h 17
7	Deployment	 PAGEREF _Toc153956203 \h 18
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 19
8.1	Assumptions	 PAGEREF _Toc153956205 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 19
Appendix A Volumes	 PAGEREF _Toc153956207 \h 20
Appendix B Glossary	 PAGEREF _Toc153956208 \h 21
Appendix C Document Control	 PAGEREF _Toc153956209 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of PO (Purchase Order) Receipt data, for direct deliveries only, from the Integration Layer (IL), to the Retail Management System (RMS).

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for Turkey only.

Background
A store is notified of a delivery of goods being shipped by a Purchase Order (PO) (as per interface D016).  When the store receives the delivery, Storeline will issue a Purchase Order (PO) Receipt message to the Group Forecast and Ordering (GFO) system and Retail Management System (RMS) via the IL.

This interface details the delivery of the PO Receipt from the IL to RMS.

Scope
This interface details PO Receipts for deliveries from direct suppliers only. PO Receipts for Distribution Center (DC) deliveries are NOT covered by this interface. 

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
The PO Receipt message, existing as a correlated orchestration within the IL, will have SKU level items converted to Pack level, will be converted to a format suitable for upload by RMS, and placed in a shared directory on the RMS host ready for upload by RMS.

The successful placement of the file into the shared directory on the RMS host will be logged using the Trackpoint component of the IMOF framework:

Failure of file creation or transport will be raised using the Error Processing framework of IMOF:

At time of writing, IMOF specifications have not yet been completed, hence details of how IMOF will interface with Biztalk, RTI, etc, are to be determined.

Architecture

Add overview diag

Requirements for the End-to-End Interface

Audit Requirements
The interface will use the Trackpoint component of IMOF to record the successful file transfer to the RMS shared directory.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
None.
Performance Requirements
The interface should be capable of transporting the PO Receipt file to the RMS host.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
None
Operational Support Requirements
Response to failure of file creation or transport.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
None. 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope

n/a, PO Receipt message exists as a correlated orchestration.

Source Message Schema
TBD


Message Transport Details

n/a

Naming and Configuration

This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

N/a

Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example employing BizTalk this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

None.


Processing required in the Messaging Stage of the interface
Scope
A Biztalk orchestration within the IL will:

- Convert SKU level items to Pack level, for items that are held at pack level (details TBC).

- Transform the PO Receipt to the format suitable for RMS upload,

- Name the PO Receipt file ‘IL_PORECEIPT_DIRECT_CCYYMMDDHHmmss.dat’ (TBC), where the CCYYMMDDHHmmss is the datetime that the IL produced the file,

- Place the file in the shared directory ‘RMS_inbox’ on the RMS host.

Data Validation
None
Filtering
There is no filtering requirement.
Mapping
TBD
Target Message Schema
TBD
Message Format
TBD

Message Transport Details 
Feature
Specification
Additional Information
Source System Name
Biztalk

Source Platform / OS
Windows 2003

Source Physical Location
TBD

Source Underlying Data Storage Technology
SQL Server 2005

Target System Name
RMS

Target Platform / OS
Unix AIX

Target Physical Location
TBD

Target Underlying Data Storage Technology
Oracle

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
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
Synchronous		
Asynchronous		
Bulk Data		

Real-time/Scheduled Batch
Real-time

Archiving
N/A

Logging
Log via Trackpoint component of the IMOF framework.

Error Handling
Raised through the error Error Management component of the IMOF framework.

Naming and Configuration
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

TBD

Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Account details will be included here once we have visibility of the environments.


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Successful file transfer to RMS_inbox to be logged using Trackpoint component of IMOF.

Failure of SKU to Pack conversion, file creation, or file delivery to be raised through Error Processing component of IMOF.



Processing required in the <third stage of the interface>
Scope
Not Required

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
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

Environment and Security Context
Not Required

Non-Functional Requirements
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
TBD

2


3


4


5


6


7




Volumes
No of files, records per file, file size, TBD.	

Glossary

Acronym
Term
Description
DC
Distribution Center

IDS
Integration Data Store
The data store in the integration layer
IL
Interface Layer

IMOF


PO
Purchase Order

RMS
Retail Management System
Oracle Retail Management System application



















Document Control
Change Record

Author
Date
Version
Change Reference, description
Allister Green
06-12-2006
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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 20 of  NUMPAGES 20	Date:  SAVEDATE \@ "d MMM yyyy" 26 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Will be updated with details of the new VOB for TOM integration when this is set up.
New section added



























































