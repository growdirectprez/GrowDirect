














Tesco Operating Model

Item Reference Data
Interface Specification
IDS to GFO


[J0054]







Project BEN Code:
W60416
Author:Supriyo CDate:
06/12/2006
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153186028 \h 3
1.1	Purpose of Document	 PAGEREF _Toc153186029 \h 3
1.2	Background	 PAGEREF _Toc153186030 \h 3
1.3	Scope	 PAGEREF _Toc153186031 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153186032 \h 4
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153186033 \h 4
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc153186034 \h 4
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153186035 \h 5
3.1	Scope	 PAGEREF _Toc153186036 \h 5
3.2	Source Message Schema	 PAGEREF _Toc153186037 \h 5
3.3	Message Transport Details	 PAGEREF _Toc153186038 \h 5
3.4	Environment and Security Context	 PAGEREF _Toc153186039 \h 5
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153186040 \h 6
4.1	Scope	 PAGEREF _Toc153186041 \h 6
4.2	Data Validation	 PAGEREF _Toc153186042 \h 6
4.3	Filtering	 PAGEREF _Toc153186043 \h 6
4.4	Mapping	 PAGEREF _Toc153186044 \h 6
4.5	Target Message Schema	 PAGEREF _Toc153186045 \h 7
4.6	Message Transport Details	 PAGEREF _Toc153186046 \h 7
4.7	Environment and Security Context	 PAGEREF _Toc153186047 \h 8
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153186048 \h 8
5.1	Scope	 PAGEREF _Toc153186049 \h 8
5.2	Data Validation	 PAGEREF _Toc153186050 \h 8
5.3	Filtering	 PAGEREF _Toc153186051 \h 8
5.4	Mapping	 PAGEREF _Toc153186052 \h 8
5.5	Target Message Schema	 PAGEREF _Toc153186053 \h 8
5.6	Message Transport Details	 PAGEREF _Toc153186054 \h 8
5.7	Environment and Security Context	 PAGEREF _Toc153186055 \h 9
6	Testing Deliverables	 PAGEREF _Toc153186056 \h 10
7	Deployment	 PAGEREF _Toc153186057 \h 11
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153186058 \h 12
8.1	Assumptions	 PAGEREF _Toc153186059 \h 12
8.2	Outstanding Issues	 PAGEREF _Toc153186060 \h 12
9	Assumptions and Outstanding Issues	 PAGEREF _Toc153186061 \h 13
9.1	Assumptions	 PAGEREF _Toc153186062 \h 13
9.2	Outstanding Issues	 PAGEREF _Toc153186063 \h 13
Appendix A Volumes	 PAGEREF _Toc153186064 \h 14
Appendix B Glossary	 PAGEREF _Toc153186065 \h 15
Appendix C Document Control	 PAGEREF _Toc153186066 \h 16

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Items reference data between Integration Data Store (IDS) and Group Forecasting System (GFO).
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORMS and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer business specific Item reference data between IDS and GFO systems.
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
The interface is a batch extract of commercial item reference data from an Integration Data Store and upload into the GFO system via integration layer. 

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
A scheduled batch job/s runs, at a pre-configured time, to extract the Item reference data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL procedures/queries against the data store and generates a required data-set as a file on a pre-configured file share. Batch job should extract the file in a temporary location first and then copy it to the configured location to avoid sharing/locks issues. As part of data-conversion an extract should convert numeric data to the packed decimal format as per Cobol Copybook format.
Source Message Schema
There is no source message as such. The source data resides in the form of RDBMS tables. The data model diagram provides necessary information to get the source data. 
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
RTI/BizTalk 2006

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
Shipping Agent monitors the file in the configured location for every new file and submits the same to the remote UNIX –AIX share via FTP.

Data Validation
There is no data validations requirement.

Filtering
There is no filtering requirement.

Mapping
Source Data Item
Target Data Item
Comments
 
JLTRB-REC-TYPE       
Record type (‘1’ for Detail)
Pack Item Level 1->> Item
JLTRB-TRADTPN        
Traded unit number
SKU Item Level 2->> Item
JLTRB-BASE-PRODUCT-NO
Base product number
Pack Item Level 1->> ItemDesc
JLTRB-TRAD-UNIT-DESC 
Traded unit description
Pack Item Level 2->> Item
JLTRB-EEAN           
Outer case code

JLTRB-TU-NOTIONAL-WT 
Notional weight of the traded unit.  For Turkey this weight is in KG.  For USA this weight is in LB (and decimal places of a LB - not ounces).
 Not resolved yet so for time being set to ZEROES.  Will need to be investigated further.

JLTRB-NOM-PACK-WEIGHT
Nominal pack weight  For Turkey this weight is in KG.  For USA this weight is in LB (and decimal places of a LB - not ounces).  Not resolved yet so for time being set to ZEROES.  Will need to be investigated further.
Pack Item BreakOut->>Pack_Item_Qty
JLTRB-UNIT-SIZE-X (group)
Unit size of the traded unit - set to spaces if no unit size exists.

JLTRB-UNIT-SIZE (redef)
Unit size of the traded unit	

Target Message Schema
PackItemLevel1 -> PackItemBreakout <- SKUItemLevel2

Field Name
Referenced in CR?
Insync format
Start
Length
COBOL  Format
Header Record
(needs to exist)
G
1
82
 
JLTRA-REC-TYPE     
Y
C 8
1
1
X
JLTRA-RUN-DATE     
Y
C 10
2
8
X(8)
JLTRA-RUN-TIME     
Y
C 6
10
6
X(6)
JLTRA-BUSINESS-DATE
Y
C 8
16
8
X(8)
FILLER             
N
C 59
24
59
X(59)
 
 
 
 
 
 
Detail Record
(needs to exist)
G
1
82
 
JLTRB-REC-TYPE       
Y
C 1
1
1
X
JLTRB-TRADTPN        
Y
Z 9
2
9
9(9)
JLTRB-BASE-PRODUCT-NO
Y
Z 9
11
9
9(9)
JLTRB-TRAD-UNIT-DESC 
Y
C 30
20
30
X(30)
JLTRB-EEAN           
Y
Z 14
50
14
9(14)
JLTRB-TU-NOTIONAL-WT 
Y
Z 5,2
64
7
9(5)V99
JLTRB-NOM-PACK-WEIGHT
Y
Z 3,2
71
5
999V99
JLTRB-UNIT-SIZE-X (group)
Y
G
76
7
X(7)
JLTRB-UNIT-SIZE (redef)
Y
Z 5,2
76
7
9(5)V99
 
 
 
 
 
 
Trailer Record
(needs to exist)
G
1
82
 
JLTRC-REC-TYPE 
Y
C 1
1
1
X
JLTRC-REC-COUNT
Y
Z 9
2
9
9(9)
FILLER         
N
Z 72
11
72
X(72)

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
JLTRB-TU-NOTIONAL-WT column value population yet to be decided. As a temporary value 0 will get stuffed in.
Business Analyst
2
JLTRB-NOM-PACK-WEIGHT column value population yet to be decided. As a temporary value 0 will get stuffed in.
Business Analyst
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
Supriyo C
06-12-2006
V0.1 Draft
First issue
Sankar G
07-12-2006
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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 8 of  NUMPAGES 15	Date:  SAVEDATE \@ "d MMM yyyy" 7 Dec 2006

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































