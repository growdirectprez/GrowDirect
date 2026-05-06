		









`


TOM Integration

Interface Specification
Supplier Authority Data
From GFO to UDD


[J003]






Project BEN Code:
W???
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
J002 to J010 - Information Architecture Context Diagram - UDD data load from GFO and IDS.vsd

Mapping spreadsheet
n/a


Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 5
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 5
1.2	Background	 PAGEREF _Toc153956171 \h 5
1.3	Scope	 PAGEREF _Toc153956172 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 7
2.2	Architecture	 PAGEREF _Toc153956175 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 7
3	Processing required in the Integration Layer of the interface	 PAGEREF _Toc153956183 \h 9
3.1	Scope	 PAGEREF _Toc153956184 \h 9
3.2	Data Validation	 PAGEREF _Toc153956185 \h 9
3.3	Filtering	 PAGEREF _Toc153956186 \h 9
3.4	Mapping	 PAGEREF _Toc153956187 \h 9
3.5	Target Message Schema	 PAGEREF _Toc153956188 \h 9
3.6	Message Format	 PAGEREF _Toc153956189 \h 11
3.7	Message Transport Details	 PAGEREF _Toc153956190 \h 12
38	Naming and Configuration	 PAGEREF _Toc153956191 \h 13
3.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 13
3.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 14
4	Testing Deliverables	 PAGEREF _Toc153956202 \h 16
5	Deployment	 PAGEREF _Toc153956203 \h 17
6	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 18
6.1	Assumptions	 PAGEREF _Toc153956205 \h 18
6.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 18
Appendix A Volumes	 PAGEREF _Toc153956207 \h 19
Appendix B Glossary	 PAGEREF _Toc153956208 \h 20
Appendix C Document Control	 PAGEREF _Toc153956209 \h 21

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of Supplier Authority Data from the Group Forecast and Order system (GFO) to the User Data Database (UDD) within the Integration Layer (IL). This User Data is needed by the Allocations process.

The document is of a sufficiently technical nature to allow a developer to build an actual interface. 

Background
An allocations process is needed to work with the Forecasting and Ordering system where the centre supply chain pushes stock into store. This can be for a variety of reasons but typical scenarios are: 
Allocation of a new product
Allocations to get ready for an event e.g. initial (additional) promotional stock
Allocation to initially fill a new store
Etc.

The main components of the allocations process are:
Overnight extract of data from GFO and IDS into the User Data Database (UDD) which is also located within the IDS
User creating allocations files manually using data from the UDD and an Excel template
The User uploading this allocations files into RMS, where they are validated
RMS generating and transferring allocations files to GFO via the Integration Layer


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
After End of Store Day, GFO will produce one Supplier Authority data file which the Integration Layer (IL) will immediately pass to the UDD upload directory also within the IL ready for uploading into the UDD. The file will be passed as is, without changing it’s name or data structure.

The interface will make use of the audit and traceability components of IMOF (Integration Management and Operations Framework).


Architecture
GFO will publish the Supplier Authority data file (‘GFO_Supplier_Authority.csv’) within a shared windows (CIFS) directory (‘GFO_outbox’) on the GFO host.

An RTI Shipping Agent Hosted Instruction “J003.GFO to UDD.Supplier Authority File Delivery” will:

Identify the Supplier Authority file based on name: ‘GFO_Supplier_Authority.csv’

Transport the file immediately to the UDD upload directory (‘UD_inbox’) within the IL

Log the successful file transfer using the Trackpoint component of IMOF. At time of writing, IMOF specifications have not yet been completed, hence details of how RTI will raise a Trackpoint are to be determined.


Requirements for the End-to-End Interface

Audit Requirements
The IMOF Trackpoint component will record the successful file transfer.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
GFO will produce the file by 1AM. The transfer needs to be completed by 2AM, when the UDD upload process will run.
Performance Requirements
The interface should be capable of delivering the file produced by GFO to the UDD upload directory.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist.
Operational Support Requirements
None.

If file not delivered to UDD upload directory, operational support requirement raised by UDD upload.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
None 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.

Processing required in the Integration Layer of the interface
Scope
The integration layer transports the Supplier Authority data file from the GFO shared directory to the UDD upload directory without changing it’s name or structure.

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
GFO

Source Platform / OS
UNIX –AIX 5.3

Source Physical Location
TBD

Source Underlying Data Storage Technology
DB2

Target System Name
UDD

Target Platform / OS
Windows Server 2003

Target Physical Location
TBD

Target Underlying Data Storage Technology
SQL Server 2005

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
Instruction Name: J003.GFO to UDD.Supplier Authority File Delivery
Instruction Details
Description
File delivery of Supplier Authority Data file from GFO to UDD
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
GFO output directory
GFO_outbox
UDD upload directory
UD_Inbox
UDD upload file name
GFO_Supplier_Authority.csv




Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

Successful delivery of each of the two Allocations files to be logged using the Trackpoint component of IMOF. 


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



Volumes

One file a day
Glossary

Acronym
Term
Description
GFO
Group Forecasting and Ordering
Forecasting and ordering system
IL
Integration Layer
Enterprise layer for system integration
IMOF
Integration Management and Operational Framework
Audit and Traceability framework
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
James Keel
05/12/2006
0.1
TSD – Allocations Solution Part A, User Data Database.






Distribution

Name
Position
Approver/Contributor/Other
Adrian Hinks
Engagement Architect

James Keel



























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 14 of  NUMPAGES 18	Date:  SAVEDATE \@ "d MMM yyyy" 16 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture


Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 18 of  NUMPAGES 18	Date:  SAVEDATE \@ "d MMM yyyy" 16 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Will be updated with details of the new VOB for TOM integration when this is set up.
New section added



























































