		









`


TOM Integration

Interface Specification
Item-Subgroup
From IDS to GFO


[J0057]






Project BEN Code:
W60416
Author:Nitin SinghaiDate:
06/12/2006
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.1 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:
Sankar G
Reviewed By:
Sankar G

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc153188374 \h 3
1.1	Purpose of Document	 PAGEREF _Toc153188375 \h 3
1.2	Background	 PAGEREF _Toc153188376 \h 3
1.3	Scope	 PAGEREF _Toc153188377 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc153188378 \h 4
2.1	Description of the End-to-End Interface	 PAGEREF _Toc153188379 \h 4
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc153188380 \h 4
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc153188381 \h 5
3.1	Scope	 PAGEREF _Toc153188382 \h 5
3.2	Source Message Schema	 PAGEREF _Toc153188383 \h 5
3.3	Message Transport Details	 PAGEREF _Toc153188384 \h 5
3.4	Environment and Security Context	 PAGEREF _Toc153188385 \h 5
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc153188386 \h 6
4.1	Scope	 PAGEREF _Toc153188387 \h 6
4.2	Data Validation	 PAGEREF _Toc153188388 \h 6
4.3	Filtering	 PAGEREF _Toc153188389 \h 6
4.4	Mapping	 PAGEREF _Toc153188390 \h 6
4.5	Target Message Schema	 PAGEREF _Toc153188391 \h 7
4.6	Message Transport Details	 PAGEREF _Toc153188392 \h 7
4.7	Environment and Security Context	 PAGEREF _Toc153188393 \h 8
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc153188394 \h 9
5.1	Scope	 PAGEREF _Toc153188395 \h 9
5.2	Data Validation	 PAGEREF _Toc153188396 \h 9
5.3	Filtering	 PAGEREF _Toc153188397 \h 9
5.4	Mapping	 PAGEREF _Toc153188398 \h 9
5.5	Target Message Schema	 PAGEREF _Toc153188399 \h 9
5.6	Message Transport Details	 PAGEREF _Toc153188400 \h 9
5.7	Environment and Security Context	 PAGEREF _Toc153188401 \h 9
6	Testing Deliverables	 PAGEREF _Toc153188402 \h 10
7	Deployment	 PAGEREF _Toc153188403 \h 11
8	Assumptions and Outstanding Issues	 PAGEREF _Toc153188404 \h 12
8.1	Assumptions	 PAGEREF _Toc153188405 \h 12
8.2	Outstanding Issues	 PAGEREF _Toc153188406 \h 12
Appendix A Volumes	 PAGEREF _Toc153188407 \h 13
Appendix B Glossary	 PAGEREF _Toc153188408 \h 14
Appendix C Document Control	 PAGEREF _Toc153188409 \h 15

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t the Item-Subgroup data between Integration Data Store (IDS) and Global Forecasting System (GFO).	
Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including ORMS and GFO. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer business specific Item-Subgroup data from IDS into GFO systems.
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
The interface is a batch extract of Item Subgroup data from an Integration Data Store and upload into the GFO system via integration layer. 
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
A scheduled batch job/s runs, at a pre-configured time, to extract the Item Subgroup data from the Integration Data Store (IDS). This batch job in turn kicks off a process that executes SQL procedures/queries against the data store and generates a required data-set as a file on a pre-configured file share. Batch job should extract the file in a temporary location first and then copy it to the configured location to avoid sharing/locks issues. As part of data-conversion an extract should convert numeric data to the packed decimal format as per Cobol Copybook format.
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
Shipping Agent monitors the file in the configured location for every new file and submits the same to the remote LINUX share via FTP.
Data Validation
There is no data validations requirement.
Filtering
There is no filtering requirement.
Mapping
Division <-> Dept <-> Section -> Class -> SubClass

Source Data Item
Target Data Item
Comments
 
JLPS-REC-TYPE     
Record type (‘0’ for Header)
System date
JLPS-RUN-DATE     
Date (CCYYMMDD) of sent file
System time
JLPS-RUN-TIME     
Current time in HHMMSS format
 
JLPS-BUSINESS-DATE
Business date of file in CCYYMMDD format.  Set to SPACES. 
 
FILLER            
SPACES
 
 
 
 
Detail Record
 
 
JLPS-REC-TYPE               
Record type (‘1’ for Detail)
 
JLPS-RMS-COMM-HIER
The RMS commercial hierarchy.  This is the equivalent of the Sub group code.  It is a 20 character string split into 5 fields as follows.  CR will translate this into the appropriate CR 5 character Subgroup code.
Division - >>Division
JLPS-RMS-DIVISION
RMS Division for this product.  Equivalent to the UK Division.  Supply as a number with leading zeroes.  
Department - >>Department
JLPS-RMS-GROUP
RMS Group for this product.  Equivalent to the UK Department.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero.
Section - >>Section
JLPS-RMS-DEPT
RMS Department for this product.  Equivalent to the UK Section.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero.
Class - >>Class
JLPS-RMS-CLASS
RMS Class for this product.  Equivalent to the UK Product Group.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero.
SubClass - >>SubClass
JLPS-RMS-SUBCLASS
RMS Sub Class for this product.  Equivalent to the UK Sub Group.  Supply as a number with leading zeroes.  If this field is not relevant given the level then supply as zero.  

JLPS-SG-LEVEL               
Sub group level.  Currently set to a number between 1 and 5 inclusive.
SubClass->>SubClassDesc
JLPS-HIERARCHY-SUBGROUP-DESC
Subgroup description.

Target Message Schema

Field NameReferenced in CR?Insync formatStartLengthCOBOL Format





Header Record
(needs to exist)




JLPS-REC-TYPE     
Y
C 1
1
1
X
JLPS-RUN-DATE     
Y
C 8
2
8
X(8)
JLPS-RUN-TIME     
Y
C 6
10
6
X(6)
JLPS-BUSINESS-DATE
Y
C 8
16
8
X(8)
FILLER            
N
C 23
24
23
X(23)
 
 
 
 
 
 
Detail Record
(needs to exist)
G
1
46
 
JLPS-REC-TYPE               
Y
C 1
1
1
X
JLPS-RMS-COMM-HIER
Y
G
2
20
 
JLPS-RMS-DIVISION
Y
Z 4
2
4
9(4)
JLPS-RMS-GROUP
Y
Z 4
6
4
9(4)
JLPS-RMS-DEPT
Y
Z 4
10
4
9(4)
JLPS-RMS-CLASS
Y
Z 4
14
4
9(4)
JLPS-RMS-SUBCLASS
Y
Z 4
18
4
9(4)
JLPS-SG-LEVEL               
Y
C 1
22
1
X
JLPS-HIERARCHY-SUBGROUP-DESC
Y
C 24
23
24
X(24)
 
 
 
 
 
 
Trailer Record
(needs to exist)
G
1
46
 
JLPS-REC-TYPE 
Y
C 1
1
1
X
JLPS-REC-COUNT
Y
Z 7
2
7
9(7)
FILLER        
N
C 38
9
38
X(38)


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
Unix

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
JLPS-SG-LEVEL - Purpose of this field   in target field and populating logic needs to be defined.
Business Associate
2
JLPS-RMS-COMM-HIER – Derivation Method need to be de defined
Engagement Architect 


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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 8 of  NUMPAGES 15	Date:  SAVEDATE \@ "d MMM yyyy" 7 Dec 2006

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































