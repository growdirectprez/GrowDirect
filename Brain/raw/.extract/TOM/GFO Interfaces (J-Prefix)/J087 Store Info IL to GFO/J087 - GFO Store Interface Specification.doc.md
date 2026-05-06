		









`


TOM Integration

Interface Specification
Store reference data
From IDS to GFO


[J0087]






Project BEN Code:
W60416
Author:Kapil ChadhaDate:
17/11/2006
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:
Sankar G
Reviewed By:
Sankar G

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153180764 \h 3
1.1	Purpose of Document	 PAGEREF _Toc153180765 \h 3
1.2	Background	 PAGEREF _Toc153180766 \h 3
1.3	Scope	 PAGEREF _Toc153180767 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153180768 \h 4
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153180769 \h 4
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc153180770 \h 4
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153180771 \h 5
3.1	Scope	 PAGEREF _Toc153180772 \h 5
3.2	Source Message Schema	 PAGEREF _Toc153180773 \h 5
3.3	Message Transport Details	 PAGEREF _Toc153180774 \h 5
3.4	Environment and Security Context	 PAGEREF _Toc153180775 \h 5
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153180776 \h 6
4.1	Scope	 PAGEREF _Toc153180777 \h 6
4.2	Data Validation	 PAGEREF _Toc153180778 \h 6
4.3	Filtering	 PAGEREF _Toc153180779 \h 6
4.4	Mapping	 PAGEREF _Toc153180780 \h 6
4.5	Target Message Schema	 PAGEREF _Toc153180781 \h 8
4.6	Message Transport Details	 PAGEREF _Toc153180782 \h 9
4.7	Environment and Security Context	 PAGEREF _Toc153180783 \h 10
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153180784 \h 11
5.1	Scope	 PAGEREF _Toc153180785 \h 11
5.2	Data Validation	 PAGEREF _Toc153180786 \h 11
5.3	Filtering	 PAGEREF _Toc153180787 \h 11
5.4	Mapping	 PAGEREF _Toc153180788 \h 11
5.5	Target Message Schema	 PAGEREF _Toc153180789 \h 11
5.6	Message Transport Details	 PAGEREF _Toc153180790 \h 11
5.7	Environment and Security Context	 PAGEREF _Toc153180791 \h 11
6	Testing Deliverables	 PAGEREF _Toc153180792 \h 12
7	Deployment	 PAGEREF _Toc153180793 \h 13
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153180794 \h 14
8.1	Assumptions	 PAGEREF _Toc153180795 \h 14
8.2	Outstanding Issues	 PAGEREF _Toc153180796 \h 14
Appendix A Volumes	 PAGEREF _Toc153180797 \h 15
Appendix B Glossary	 PAGEREF _Toc153180798 \h 16
Appendix C Document Control	 PAGEREF _Toc153180799 \h 17

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Store reference data between Integration Data Store (IDS) and Global Forecasting System (GFO).	
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORMS and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer business specific Store reference data from IDS into GFO systems.
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
The interface is a batch extract of Store reference data from an Integration Data Store and upload into the GFO system via integration layer. 
The interface is meant to run at a pre-configured time, which on completion is expected to produce a flat-file (containing reference data records) onto the shared location. This shared location would be monitored by GFO system during specific hours. Once the file containing the extracted data appears on the shared location it should load the data (updates/inserts) into GFO.
Requirements for the End-to-End Interface

Audit Requirements
Each and every interface run should be audited/logged for the purpose of traceability
Security Requirements
No security requirements. 
Timing/Cut-off Constraints
As of now there is no such requirement, however this needs to be re-visited
Performance Requirements
The performance requirements, are unknown at this point of time
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
There is no such requirement
Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
There is no such requirement
Legal Requirements
There is no such requirement
Compliance To Standards Requirements
To be filled in !!
Processing required in an Extract-Stage of the interface
Scope
A scheduled batch job/s runs, at a pre-configured time, to extract the Store reference data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL procedures/queries against the data store and generates a required data-set as a file on a pre-configured file share. Batch job should extract the file in a temporary location first and then copy it to the configured location to avoid sharing/locks issues. As part of data-conversion an extract should convert numeric data to the packed decimal format as per Cobol Copybook format.
Source Message Schema
There is no source message as such. The source data resides in the form of RDBMS tables. The data model diagram will provide necessary information to get the source data. 
Message Transport Details
Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
SQL Server

Source Physical Location


Source Underlying Data Storage Technology
RDBMS

Target System Name
RTI

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	

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
Bulk Data		

Real-time/Scheduled Batch
Scheduled Batch

Archiving
There is no requirement to archive the messages.

Logging
Logging should occur, such that the message can be recreated if necessary.

Error Handling
If the message cannot be delivered, retry 6 times at 10 minute intervals, then raise alert.

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.

Environment and Security Context
Processing required in the Messaging Stage of the interface
Scope
Shipping Agent monitors the file in the configured location for every new file and submits the same to the remote UNIX-AIX share via FTP.
Data Validation
There is no data validations requirement.
Filtering
There is no filtering requirement.
Mapping
Source Data Item
Target Data Item
Comments
Store -> StoreId
CHBCB-ORGANISATION-UNIT-NO
Retail outlet number

CHBCB-INFO-DATA-GRP (group)
branch details

CHBCB-PROPERTY-NO
property number from the OU/PY database to which branch number is linked
Store -> STORE_NAME
CHBCB-ORG-UNIT-NAME
branch name

CHBCB-LINE1-ADDRESS
set to spaces

CHBCB-LINE2-ADDRESS
set to spaces

CHBCB-LINE3-ADDRESS
set to spaces

CHBCB-LINE4-ADDRESS
set to spaces

CHBCB-POST-CODE
set to spaces

CHBCB-RETAIL-OUTLET-TYPE
A very old branch classification:  1 = store 2 = H&W 3 = dummy branch 5 = PFS  CR only uses this field in one place to identify PFS stores.  It can do this by checking the RO-TYPE-CLASS instead.  Set to SPACE 
Store -> PHONE_NUMBER
CHBCB-RO-PHONE-1-NO
branch phone number
Region -> Region
CHBCB-RO-TV-REG-NO (occurs 2)


CHBCB-RO-NLSN-REG-NO
Nielsen region
Not referred in GFO
Set to Spaces
Store -> STORE_OPEN_DATE
CHBCB-DATE-OPENED
original branch opening date - see 'STORE' table in RMS. Format of date DDMMCCYY.
Store -> STORE_CLOSE_DATE
CHBCB-DATE-CLOSED
date branch ceased trading - see 'STORE' table in RMS.  Format of date DDMMCCYY.
Store -> STORE_REMODELLED_DATE
CHBCB-REFIT-DATE
date of last refit - see 'STORE' table in RMS. Format of date DDMMCCYY.
Store -> ParentStoreID
CHBCB-ASSOCIATED-UNIT-NO(1)
'Mother' store (ie main branch if this is a PFS) with leading zeros.  For stores that are not a PFS et to 00000.

CHBCB-ASSOCIATED-UNIT-NO(2)
child' store (i.e. PFS if this is a main branch)
Not referred in GFO
Set to Spaces

CHBCB-ASSOCIATED-UNIT-NO(3)
Unused
Not referred in GFO
Set to Spaces

CHBCB-SITE-LOCN-DESC-CDE
?
Not referred in GFO
Set to Spaces

CHBCB-OS-GRID-REF-NO-GRP (group)
Not referred in GFO
Set to Spaces

CHBCB-OS-GRID-REF-NO
Not referred in GFO
Set to Spaces

CHBCB-OU-DAY-OP-SEG-GRP (group)  occurs 7
these branch opening times are generally thought to be less accurate than those held in C.R.
Not referred in GFO
Set to Spaces

CHBCB-OU-DLY-OPEN-TIME-GRP (group)
Not referred in GFO
Set to Spaces

CHBCB-DAILY-OPENING-HRS
Not referred in GFO
Set to Spaces

CHBCB-DAILY-OPENING-MINS
Not referred in GFO
Set to Spaces

CHBCB-OU-DLY-CLOSE-TIME-GRP (group)
Not referred in GFO
Set to Spaces

CHBCB-DAILY-CLOSING-HRS
Not referred in GFO
Set to Spaces

CHBCB-DAILY-CLOSING-MINS
Not referred in GFO
Set to Spaces

CHBCB-REGION-GROUP-NO-GRP
Not referred in GFO
Set to Spaces

CHBCB-REGION-GROUP-NO
Number of the SD region grouping to which the branch belongs. Recently expanded from 2 to 3 digits.  Does an approriate code exist in RMS?   Set to '000'

CHBCB-REGION-MD-INITS
initials of the SD for the region
Not referred in GFO
Set to Spaces

CHBCB-REGION-EXEC-INITS
initials of the OD for the region
Not referred in GFO
Set to Spaces

CHBCB-TRDG-STAT-CODE
T – trading D - development (not yet open) R - currently closed for refit C – closed
Not referred in GFO
Set to Spaces

CHBCB-SHELF-EDGE-LABEL-CD
Not referred in GFO
Set to Spaces

CHBCB-MANAGERS-TITLE
e.g. Mr, Mrs etc
Not referred in GFO
Set to Spaces

CHBCB-MANAGERS-INITIALS
Not referred in GFO
Set to Spaces
Store -> STORE_MANAGER_NAME
CHBCB-MANAGERS-NAME
store manager's surname

CHBCB-COUNTY-CODE
Set to '00'

CHBCB-CAR-PARK-SPACES-QTY
Not referred in GFO
Set to Spaces

CHBCB-CHECKOUTS-QTY
Not referred in GFO
Set to Spaces
Region -> Region
CHBCB-REGION-CODE
Old, probably obsolete division, NOT to be confused with Region-Group-No, which is more important.
Coutry Code is not directly related to Location Hierachy
CHBCB-COUNTRY-CODE
Current settings 1 - England 2 - Wales 3- Scotland 4 - France 5 - Northern Ireland 7 - ROI Set to '0'

CHBCB-RO-RNGE-CLASS
branch-level range character which is of limited use since ranging tends to be at MGRP/product level
Not referred in GFO
Set to Spaces

CHBCB-CPLUS-STORE-IND
Y or N
Not referred in GFO
Set to Spaces
Store -> SellingSqFt
CHBCB-METRO-STORE-IND
If (Store -> SellingSqFt) >= 5000 and Store -> SellingSqFt <= 18000 then
   'Y'
Else 
   'N'
Store -> SellingSqFt
CHBCB-RO-TYPE-CLASS
If ((Store -> SellingSqFt) / 10.76) < 300 then
   'E'
Elsif ((Store -> SellingSqFt) / 10.76) > 300 and ((Store -> SellingSqFt) / 10.76) <= 2000 then
   'SM'
Elsif ((Store -> SellingSqFt) / 10.76) >= 2500 and ((Store -> SellingSqFt) / 10.76) <= 4500 then
   'S'
Elsif ((Store -> SellingSqFt) / 10.76) > 5000 then
   'HY'

Target Message Schema
Chain -> Area <-> Region <-> District <-> Store

Field NameReferenced in CR?Insync formatStartLengthCOBOL Format





CHBCA-INFO-HDR (group)
Needs to exist.
G
1
325
X(325)
CHBCA-INFO-KEY-GRP (group)

G
1
6
X(6)
CHBCA-REC-TYPE
Y
Z
1
1
9
Filler
Y
C
2
316
X(316)
CHBCA-MACH-DTE
Y
Z
318
8
9(8)






CHBCB-INFO-DET-REC (redef) (group)

G
1
325
X(325)
CHBCB-INFO-KEY-GRP

G
1
6
X(6)
CHBCB-REC-TYPE
Y
Z
1
1
9
CHBCB-ORGANISATION-UNIT-NO
Y
Z
2
5
9(5)
CHBCB-INFO-DATA-GRP (group)

G
7
319
X(319)
CHBCB-PROPERTY-NO

Z
7
4
9(4)
CHBCB-ORG-UNIT-NAME
Y
C
11
21
X(21)
CHBCB-LINE1-ADDRESS

C
32
24
X(24)
CHBCB-LINE2-ADDRESS

C
56
24
X(24)
CHBCB-LINE3-ADDRESS

C
80
24
X(24)
CHBCB-LINE4-ADDRESS

C
104
24
X(24)
CHBCB-POST-CODE

C
128
12
X(12)
CHBCB-RETAIL-OUTLET-TYPE
Y
C
140
1
X
CHBCB-RO-PHONE-1-NO

C
141
17
X(17)
CHBCB-RO-TV-REG-NO (occurs 2)

C
158
2
XX
CHBCB-RO-NLSN-REG-NO

C
162
2
XX
CHBCB-DATE-OPENED
Y
C
164
8
X(8)
CHBCB-DATE-CLOSED
Y
C
172
8
X(8)
CHBCB-REFIT-DATE
Y
C
180
8
X(8)
CHBCB-ASSOCIATED-UNIT-NO(1)
Y
C
188
5
X(5)
CHBCB-ASSOCIATED-UNIT-NO(2)

C
193
5
X(5)
CHBCB-ASSOCIATED-UNIT-NO(3)

C
198
5
X(5)
CHBCB-SITE-LOCN-DESC-CDE

C
203
5
X(5)
CHBCB-OS-GRID-REF-NO-GRP (group)

G
205
5
X(5)
CHBCB-OS-GRID-REF-NO

PS
205
5
S9(4)V9(4) comp-3
CHBCB-OU-DAY-OP-SEG-GRP (group)  occurs 7

G
210
56
X(56)
CHBCB-OU-DLY-OPEN-TIME-GRP (group)

G
210
4
X(4)
CHBCB-DAILY-OPENING-HRS

C
210
2
XX
CHBCB-DAILY-OPENING-MINS

C
212
2
XX
CHBCB-OU-DLY-CLOSE-TIME-GRP (group)

G
214
4
X(4)
CHBCB-DAILY-CLOSING-HRS

C
214
2
XX
CHBCB-DAILY-CLOSING-MINS

C
216
2
XX
CHBCB-REGION-GROUP-NO-GRP

G
266
3
XXX
CHBCB-REGION-GROUP-NO
Y
Z
266
3
999
CHBCB-REGION-MD-INITS

C
269
3
XXX
CHBCB-REGION-EXEC-INITS

C
272
3
XXX
CHBCB-TRDG-STAT-CODE

C
275
1
X
CHBCB-SHELF-EDGE-LABEL-CD

C
276
1
X
CHBCB-MANAGERS-TITLE

C
277
4
X(4)
CHBCB-MANAGERS-INITIALS

C
281
3
XXX
CHBCB-MANAGERS-NAME

C
284
16
X(16)
CHBCB-COUNTY-CODE
Y
C
300
2
XX
CHBCB-CAR-PARK-SPACES-QTY

PS
302
3
S9(5) comp-3
CHBCB-CHECKOUTS-QTY

PS
305
2
S999 comp-3
CHBCB-REGION-CODE

C
307
1
X
CHBCB-COUNTRY-CODE
Y
C
308
1
X
CHBCB-RO-RNGE-CLASS

C
309
1
X
CHBCB-CPLUS-STORE-IND

C
310
1
X
CHBCB-METRO-STORE-IND
Y
C
311
1
X
CHBCB-RO-TYPE-CLASS
Y
C
312
2
XX






CHBCZ-INFO-TRLR (redef) (group)
Needs to exist
G
1
325
X(325)
CHBCZ-INFO-KEY-GRP (group)

G
1
6
X(6)
CHBCZ-REC-TYPE
Y
Z
1
1
9
Filler
Y
C
2
5
X(5)
CHBCZ-RECNT
Y
PS
7
5
9(5)
Filler
N
C
12
314
X(314)


Message Transport Details 
For messages destined for TO system, the following applies.	

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
UNIX-AIX

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		

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




Environment and Security Context
Messaging will happen through Shipping Agent. The Real Time Integrator or BizTalk2006 EAI tool will be set with the Environment specification (will be defined)
 

 
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

Environment and Security Context
Not Required
Testing Deliverables
Unit Test Scripts
Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
The messaging task will be started at EOD



Outstanding Issues
ID
Issue
To be addressed by
1
Source Data missing in the data model
John Jolley
2
Compliance To Standards Requirements yet to get



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
HIS
Host Integration Server
A gateway to transferring data between a Mainframe system and another system.

Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.
ODS
Operation Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Customer, etc. ODS's reside in the EIA Layer, and are accessed through the EAI Layer.
TIB
Tesco Integration Bus
The managed service provided by Tesco's EAI Layer for data transportation and the integration of applications with legacy data sources and Operational Data Stores. 'Larger' in concept than the EAI Layer to include implementation details and interfacing between the EAI (integration services) Layer and the EIA (data services) Layer
WOF
Wintel Operational Framework
The Windows software/Intel hardware environment
->
One to Many Relationship
In a Subject hierarchy the entities defined as parent and child symbolize in this way.
<->
Many to Many Relationship
In a Subject hierarchy the relationship between the entities defined with many to many relationship without relationship table symbolize this way.

Document Control
Change Record

Author
Date
Version
Change Reference, description
Kapil Chadha
21-11-2006
V0.1 Draft
First issue
Sankar G
06-12-2006
V0.2 Draft
Second issue











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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 8 of  NUMPAGES 18	Date:  SAVEDATE \@ "d MMM yyyy" 7 Dec 2006

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































