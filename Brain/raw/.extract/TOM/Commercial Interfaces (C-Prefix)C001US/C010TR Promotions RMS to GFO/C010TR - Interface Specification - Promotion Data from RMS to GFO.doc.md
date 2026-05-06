		









`


TOM Integration

Interface Specification
Promotions Data
From RMS to GFO


[C010TR / J114]






Project BEN Code:
W60416
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
C010TR - Information Architecture Context Diagram - Promotion Data from RMS to GFO.vsd

Mapping spreadsheet
n/a


Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 5
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 5
1.2	Background	 PAGEREF _Toc153956171 \h 5
1.3	Scope	 PAGEREF _Toc153956172 \h 5
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 6
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 6
2.2	Architecture	 PAGEREF _Toc153956175 \h 6
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 6
3	Processing required in the messaging stage of the interface	 PAGEREF _Toc153956183 \h 8
3.1	Scope	 PAGEREF _Toc153956184 \h 8
3.2	Data Validation	 PAGEREF _Toc153956185 \h 8
3.3	Filtering	 PAGEREF _Toc153956186 \h 8
3.4	Mapping	 PAGEREF _Toc153956187 \h 8
3.5	Target Message Schema	 PAGEREF _Toc153956188 \h 8
3.6	Message Format	 PAGEREF _Toc153956189 \h 9
3.7	Message Transport Details	 PAGEREF _Toc153956190 \h 10
38	Naming and Configuration	 PAGEREF _Toc153956191 \h 11
3.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 11
3.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 12
4	Testing Deliverables	 PAGEREF _Toc153956202 \h 13
5	Deployment	 PAGEREF _Toc153956203 \h 14
6	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 15
6.1	Assumptions	 PAGEREF _Toc153956205 \h 15
6.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 15
Appendix A Volumes	 PAGEREF _Toc153956207 \h 15
Appendix B Glossary	 PAGEREF _Toc153956208 \h 17
Appendix C Document Control	 PAGEREF _Toc153956209 \h 18

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of promotion data from the Retail Management System (RMS) to the Group Forecast and Order system (GFO).

This interface is for Turkey only.

The document is of a sufficiently technical nature to allow a developer to build an actual interface. 

Background
As part of the forecasting process GFO requires details of product promotions 31 days in advance of the promotion starting. RMS will produce the promotion data once a day.

GFO expects the promotion data to include all promotions from 31 days prior to their start date, until the day that the promotion ends. Any promotion that is not included in this interface data will be treated as ended.

The promotion data will include updates to existing promotions, as well as new promotions.

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
Once a day, RMS will produce one Promotion data file, which will immediately be passed to GFO by the Integration Layer (IL) without changing it’s name or data structure.

The interface will make use of the audit and traceability components of IMOF (Integration Management and Operations Framework).

Architecture
RMS will publish the promotion data file, named ‘RMS_PROMOTION_CCYYMMDDHHmmss.dat’, to the ‘RMS_outbox’ shared windows (CIFS) directory on the RMS host

An RTI Shipping Agent Hosted Instruction “C010TR.RMS to GFO.Promotion File Delivery” will:

Identify the promotion data file based on name pattern: ‘RMS_PROMOTION_*.dat’

Transport the file immediately upon receipt to a shared windows (CIFS) directory (‘GFO_inbox’) on the GFO host

Log the successful file transfer using the ‘Trackpoint’ component of IMOF. At time of writing, IMOF specifications have not yet been completed, hence details of how RTI interfaces with IMOF regarding error alerts and Trackpoint logging are to be determined.

Note the CCYYMMDDHHmmss of the RMS file name is the date time RMS creates the file.


Requirements for the End-to-End Interface

Audit Requirements
The IMOF Trackpoint component will record the successful file transfer.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
RMS will produce the file by TBD. GFO needs to receive the file by 9PM (TBC)
Performance Requirements
The interface should be capable of delivering the file produced by RMS to the GFO upload directory.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist.
Operational Support Requirements
Failure of the file to being delivered by the specified cut off time to GFO will result in alert being raised through IMOF.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
None 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.

Processing required in the messaging stage of the interface
Scope
The integration layer purely passes promotion data file from the RMS shared directory to the GFO shared directory without changing it’s name or structure.

Data Validation
None
Filtering
There is no filtering requirement.
Mapping
None
Target Message Schema
n/a


Message Format
N/a
Message Transport Details 

Feature
Specification
Additional Information
Source System Name
RMS

Source Platform / OS
UNIX –AIX 5.3

Source Physical Location
TBD

Source Underlying Data Storage Technology
Oracle

Target System Name
GFO

Target Platform / OS
UNIX –AIX

Target Physical Location
TBD

Target Underlying Data Storage Technology
DB2

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
File transfer logged using IMOF Trackpoint component.

Error Handling
None


Naming and Configuration
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 


RTI
Instruction Name: C010TR.RMS to GFO.Promotion File Delivery
Instruction Details
Description
File delivery of Promotion Data file from RMS to GFO
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
60
Retry Attempts
1
Timeout
60
Require Data Send
True
Exception Management
Treat Fatal Adapter Exception As
Fatal
Treat Unhandled Exceptions As
Fatal


Directory and File Names
Description
Name
RMS output directory
RMS_outbox
GFO upload directory
GFO_Inbox
GFO upload file name
RMS_PROMOTION_CCYYMMDDHHmmss.dat’

Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Successful delivery of each of the promotion data file to be logged using the Trackpoint component of IMOF. 

Failure of the file to be delivered by cut off time to GFO will result in an alert raised through IMOF.

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
Details of how IMOF framework integrates with RTI to be defined.
IMOF specifications available
2
Source and target file locations to be established (section 3.7)

3
Cutoff time GFO needs file by, and time RMS will produce the file (section 2.3).
Lewis Stewart.

Volumes

One file a day
Glossary

Acronym
Term
Description
CIFS
Common Internet File System
Technology to produced virtual Windows directories on the UNIX – AIX platform
GFO
Group Forecasting and Ordering
Forecasting and ordering system
IL
Integration Layer
Enterprise layer for system integration
IMOF
Integration Management and Operational Framework
Audit and Traceability framework
RMS
Retail Management System
Oracle Retail Management System
UDD
User Data Database
Database within the Integration Layer used for storing the User Data used to manually create Allocations.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Allister Green
26/01/2007
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
Adrian Hinks
Engagement Architect

James Keel



























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT ii of  NUMPAGES 18	Date:  SAVEDATE \@ "d MMM yyyy" 14 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture


Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 18 of  NUMPAGES 18	Date:  SAVEDATE \@ "d MMM yyyy" 14 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Will be updated with details of the new VOB for TOM integration when this is set up.
New section added



























































