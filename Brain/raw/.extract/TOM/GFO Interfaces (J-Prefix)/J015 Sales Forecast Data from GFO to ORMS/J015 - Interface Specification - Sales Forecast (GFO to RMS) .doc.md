









`


TOM Integration

Interface Specification
Sales Forecast Data
From GFO to RMS


[J015]






Project BEN Code:
W60416
Author:Allister GreenDate:
16/01/2007
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:

Reviewed By:
Adrian Hinks 07/02/2007 (initial review)

Change Record

Author
Date
Version
Change Reference, description
Allister Green
16/01/2007
0.1
First Draft
Allister Green
12/02/2007
0.2
Second draft following review









Reviewers

Name
Date
Version
Position
Adrian Hinks


Integration Architect
Nathan Smith


Enterprise Architect
Richard Durley


Enterprise Architect










At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Laurence Tang 
Position
BSA (in lieu of Business Owner)
Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version
Laurence Tang
<Issue Date>
<Version No>
Lewis Stewart


Rob Mcdonagh


Dave Onyett


Andrew Knott









Document Source

 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fGFO%20Interfaces%20%28J%2dPrefix%29%2fJ015%20Sales%20Forec" DocShare: UK IT/TOM Integration/Shared Documents



Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents:


Information Architecture Context diagram
J0015 - Information Architecture Context Diagram - Sales Forecast (GFO to RMS).vsd

Mapping spreadsheet
n/a
n/a

Technical System Design
TSD001 - DC Replenishment v1.doc

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153956169 \h 6
1.1	Purpose of Document	 PAGEREF _Toc153956170 \h 6
1.2	Background	 PAGEREF _Toc153956171 \h 6
1.3	Scope	 PAGEREF _Toc153956172 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153956173 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153956174 \h 7
2.2	Architecture	 PAGEREF _Toc153956175 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc153956176 \h 7
3	Processing required in an GFO Extraction Stage of the interface	 PAGEREF _Toc153956177 \h 8
3.1	Scope	 PAGEREF _Toc153956178 \h 8
3.2	Source Message Schema	 PAGEREF _Toc153956179 \h 8
3.3	Message Transport Details	 PAGEREF _Toc153956180 \h 8
3.4	Naming and Configuration	 PAGEREF _Toc153956181 \h 9
3.5	Environment and Security Context	 PAGEREF _Toc153956182 \h 9
4	Processing required in the Integration Layer of the interface	 PAGEREF _Toc153956183 \h 10
4.1	Scope	 PAGEREF _Toc153956184 \h 10
4.2	Data Validation	 PAGEREF _Toc153956185 \h 10
4.3	Filtering	 PAGEREF _Toc153956186 \h 10
4.4	Mapping	 PAGEREF _Toc153956187 \h 10
4.5	Target Message Schema	 PAGEREF _Toc153956188 \h 10
4.5.1 Turkey Only	 PAGEREF _Toc153956188 \h 10
4.5.1 US Only	 PAGEREF _Toc153956188 \h 10
4.6	Message Format	 PAGEREF _Toc153956189 \h 10
4.7	Message Transport Details	 PAGEREF _Toc153956190 \h 11
4.8	Naming and Configuration	 PAGEREF _Toc153956191 \h 12
4.9	Environment and Security Context	 PAGEREF _Toc153956192 \h 12
4.10	Non-Functional Requirements	 PAGEREF _Toc153956193 \h 12
5	Processing required in the RMS import stage of the interface	 PAGEREF _Toc153956194 \h 13
5.1	Scope	 PAGEREF _Toc153956195 \h 13
5.2	Data Validation	 PAGEREF _Toc153956196 \h 13
5.3	Filtering	 PAGEREF _Toc153956197 \h 13
5.4	Mapping	 PAGEREF _Toc153956198 \h 13
5.5	Target Message Schema	 PAGEREF _Toc153956199 \h 13
5.6	Message Transport Details	 PAGEREF _Toc153956200 \h 13
5.7	Environment and Security Context	 PAGEREF _Toc153956201 \h 13
6	Testing Deliverables	 PAGEREF _Toc153956202 \h 14
7	Deployment	 PAGEREF _Toc153956203 \h 15
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153956204 \h 16
8.1	Assumptions	 PAGEREF _Toc153956205 \h 16
8.2	Outstanding Issues	 PAGEREF _Toc153956206 \h 16
Appendix A Volumes	 PAGEREF _Toc153956207 \h 17
Appendix B Glossary	 PAGEREF _Toc153956208 \h 18
Appendix C Document Control	 PAGEREF _Toc153956209 \h 19

Introduction
Purpose of Document
The purpose of this document is to describe the requirements for the interface of Sales Forecast data from the Group Forecast and Order system (GFO), to the Retail Management System (RMS).
 
The document is of a sufficiently technical nature to allow a developer to build an actual interface. 

This interface is identical for Turkey and US.

Background
As part of the DC Replenishment process, GFO will provide RMS a daily Sales Forecast of all items replenished by GFO. The Sales Forecast is sent to the Dynamic Calculation or Time Supply Calculation within RMS Replenishment. RMS will then calculate and generate a DC Purchase Order, which is sent to the relevant DC supplier via TIMS.

The sales forecast is produced each day for each of the following 21 days, aggregated by Item and DC.

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
Once a day on a scheduled basis, GFO will produce the Sales Forecast data file, and place it in a directory on the GFO host. The Integration Layer (IL) will transport this file to a directory on the RMS host, from where RMS will upload it.

Architecture

GFO will publish the Sales Forecast file, named ‘GFO_SALESFOR_CCYYMMDDHHmmss.dat’, to the ‘GFO_outbox’ shared windows (CIFS) directory on the GFO host

An RTI Shipping Agent Hosted Instruction “J015.GFO to RMS.Sales Forecast File Delivery” will:

Identify the Sales Forecast file based on name pattern: ‘GFO_SALESFOR_*.dat’

Transport the file immediately upon receipt to a shared windows directory (‘RMS_inbox’) on the RMS host

Log the successful file transfer using the Trackpoint component of IMOF. At time of writing, IMOF specifications have not yet been completed, hence details of how RTI or SSIS will record an event using the ‘Trackpoint’ component, or raise an error using the ‘Error Processing’ component, are to be determined.

Note the CCYYMMDDHHmmss of the GFO file name is the date time GFO creates the file.



Requirements for the End-to-End Interface

Audit Requirements
The IMOF Trackpoint component will record the successful file transfer
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
GFO will produce the file by 5AM. The latest time RMS must receive the file is TBD
Performance Requirements
No specific requirements. 
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A - No scalability issues exist. There will only ever be a single instance of the GFO and RMS in a TOM implementation and therefore no requirement for multiple files to multiple locations.
Operational Support Requirements
Failure of the Sales Forecast data file to be delivered to RMS by (time TBD) each day will raise an alert through the IMOF framework.

Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
Where the interface is implemented into a country in which a multi-byte character set is required to support the national language, the interface and all participating applications must support a multi-byte character set. 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in GFO Extraction Stage of the interface
Scope
Not Required
Source Message Schema
Not Required
Message Transport Details
Not Required

Naming and Configuration
Not Required

Environment and Security Context
Not Required

Non-Functional Requirements
Not Required
Processing required in the Integration Layer of the interface
Scope
The IL simply transports the sales forecast file produced by GFO to RMS.
Data Validation
Data Validation will be done by the target RMS system.
Filtering
There is no filtering requirement.
Mapping
Not required
Target Message Schema
Not required

Message Format
Not required

Message Transport Details 


Feature
Specification
Additional Information
Source System Name
GFO

Source Platform / OS
UNIX – AIX 

Source Physical Location
TBD

Source Underlying Data Storage Technology
DB2

Target System Name
RMS

Target Platform / OS
UNIX –AIX 5.3

Target Physical Location
TBD

Target Underlying Data Storage Technology
Oracle

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
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
Successfull file transfer will be logged using the Trackpoint component of IMOF.

Error Handling
If no sales forecast file delivered to RMS by (time TBD) the Error Processing component of the Operational Framework will raise an error.


Naming and Configuration
This section should contain details of naming and configuration for BizTalk ports, RTI instructions, SSIS packages. 

File and Database Names
What
Name
Sales forecast file produced by GFO
GFO_SALESFOR_CCYYMMDDHHmmss.dat
GFO export directory
GFO_outbox
RMS upload directory
RMS_inbox

RTI Shipping Agent
What
Name
Hosted instruction name
J015.GFO to RMS.Sales Forecast File Delivery


Environment and Security Context
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example, if employing BizTalk, this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).


Account details will be included here once we have visibility of the environments.


Non-Functional Requirements
This section should contain any non-functional requirements pertaining to this stage of the interface.

The successful transport of the Sales Forecast file to RMS will be logged using the Trackpoint component of IMOF.

Failure of the file to be delivered to RMS by (TBD) each day will result in an error being raised through the Error Processing component of IMOF.


Processing required in the RMS import stage of the interface
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
Not Required

Environment and Security Context
Not Required

Non-Functional Requirements
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
IMOF functionality yet to be included.

2
Event IDs and alerts yet to be defined.

3
Source and Target file locations still to be determined (section 4.7).

4
Latest time file to arrive at RMS (sections 2.3, 4.1)
Lawrence Tang
5
Error processing. Confirm if need to raise error within the integration layer if file not sent. 
Lawrence Tang


Volumes
The size of the sales forecast file, for Turkey and the US will be as follows:

CountryRecord Size (Bytes)DC Replenished Item CountNo of forecast daysFile Size Per DC 
(MB)US812000213.5TR815000218.5

GFO will produce one Sales Forecast file per day.
Glossary

Acronym
Term
Description
CIFS
Common Internet File System
CIFS defines a remote file-access protocol that enables file systems on different platforms to be shared. 
GFO
Group Forecasting and Ordering
Forecasting and ordering system
IL
Integration Layer
Enterprise layer for system integration
IMOF
Integration Management & Operations Framework
 
RMS
Retail Management System
Oracle Retail Management System

Document Control
Change Record

Author
Date
Version
Change Reference, description
Allister Green
17-01-2007
v0.1 Draft
First issue
Allister Green
12-02-2007
v0.2
Update following initial review











Related Documents

Author	
Date
Version
Title
Laurence Tang
21-12-2007
0.3
BSD DC Replenishment














Distribution

Name
Position
Approver/Contributor/Other
Adrian Hinks
Engagement Architect




























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 19 of  NUMPAGES 19	Date:  SAVEDATE \@ "d MMM yyyy" 13 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Creation and delivery of the file should be created as IMOF events so that we are able to alert in the event the file is late being created in GFO and / or late being delivered to RMS.
 (Note that this comment is written prior to the existence of the IMOF and hence without full appreciation of IMOF capability).

Alerts will be raised in the event of failure to deliver the file. Alert numbers / IDs are yet to be defined.

I note that Section 4.9 implies that no alert would be raised until a file had not been received for 24 hours. If this is acceptable we should state this here.

This suggests to me that, for Turkey (RMS 10),  we will have to map source to target in order to get the correct position in the output file for each  data field.  

This  means the interface will have to go through BizTalk to be mapped and I think this file is going to be too big?? (Is it really only 10MB per DC per day?). I would imagine there will need to be some custom Pro C required on the RMS side to import the file, and I think they should handle the US format. The process that loads data into tables in RMS should easily deal with the fact that ItemID on the tables is only 20  characters long, similarly the Quantity and Standard Deviation fields.

 
Add a description of the IMOF




























































