		







TOM Integration

Interface Specification
Historical Sales, Margin & Waste
From SAE to RPAS


[S003 & S082]





Project BEN Code:
W60416
Author:Supriyo ChakrabortyDate:
12-Apr-07
Version:
0.2
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 
Modified By:
Supriyo Chakraborty
Reviewed By:
Andy Barker

Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
12-Apr-07
0.1D
Draft
Supriyo Chakraborty
20-Apr-07
0.2D
Draft - Incorporated the review comments.









Reviewers

Name
Date
Version
Position
Andrew Barker
20-Apr-07
0.1D
Engagement Architect














At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Andrew Barker
Position
Solution Architect
Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy 

Distribution List

Name
Date of Issue
Version
David Onyett
<Issue Date>
<Version No>
Leon Benjamin
<Issue Date>
<Version No>
Mary Welch
<Issue Date>
<Version No>
Andrew Barker
<Issue Date>
<Version No>
Venkateswara Rao
<Issue Date>
<Version No>







Document Source
Doc Share – 
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS003%2cS082%20Sales%20History%2cMargin%20and%20Wastes%20from%20SAE%20to%20RPAS&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS003%2cS082%20Sales%20History%2cMargin%20and%20Wastes%20from%20SAE%20to%20RPAS&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d


Related Documents

UK Interface Specification No - UK 111
BSD for Sales Aggregation V0.5.doc
SalesAggregation_Technical_Specifications_V0.2.doc

Information Architecture Context diagram
S003, S082- Sales History,Margin and Wastes- Context Diagram

Mapping spreadsheet
S003, S082- Sales History,Margin and Wastes- Mapping document
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc164851079 \h 6
1.1	Purpose of Document	 PAGEREF _Toc164851080 \h 6
1.2	Background	 PAGEREF _Toc164851081 \h 6
1.3	Scope	 PAGEREF _Toc164851082 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc164851083 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc164851084 \h 7
2.2	Architecture	 PAGEREF _Toc164851085 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc164851086 \h 8
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc164851087 \h 9
3.1	Scope	 PAGEREF _Toc164851088 \h 9
3.2	Source Message Schema	 PAGEREF _Toc164851089 \h 9
3.3	Message Transport Details	 PAGEREF _Toc164851090 \h 10
3.4	Naming and Configuration	 PAGEREF _Toc164851091 \h 11
3.5	Environment and Security Context	 PAGEREF _Toc164851092 \h 11
3.6	Non-Functional Requirements	 PAGEREF _Toc164851093 \h 11
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc164851094 \h 12
4.1	Scope	 PAGEREF _Toc164851095 \h 12
4.2	Data Validation	 PAGEREF _Toc164851096 \h 12
4.3	Filtering	 PAGEREF _Toc164851097 \h 12
4.4	Mapping	 PAGEREF _Toc164851098 \h 12
4.5	Target Message Schema	 PAGEREF _Toc164851099 \h 12
4.6	Sample Message Format	 PAGEREF _Toc164851100 \h 13
4.7	Message Transport Details	 PAGEREF _Toc164851101 \h 14
4.8	Naming and Configuration	 PAGEREF _Toc164851102 \h 15
4.9	Environment and Security Context	 PAGEREF _Toc164851103 \h 15
4.10	Non-Functional Requirements	 PAGEREF _Toc164851104 \h 15
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc164851105 \h 16
5.1	Scope	 PAGEREF _Toc164851106 \h 16
5.2	Data Validation	 PAGEREF _Toc164851107 \h 16
5.3	Filtering	 PAGEREF _Toc164851108 \h 16
5.4	Mapping	 PAGEREF _Toc164851109 \h 16
5.5	Target Message Schema	 PAGEREF _Toc164851110 \h 16
5.6	Message Transport Details	 PAGEREF _Toc164851111 \h 16
5.7	Naming and Configuration	 PAGEREF _Toc164851112 \h 16
5.8	Environment and Security Context	 PAGEREF _Toc164851113 \h 16
5.9	Non-Functional Requirements	 PAGEREF _Toc164851114 \h 16
6	Testing Deliverables	 PAGEREF _Toc164851115 \h 17
7	Deployment	 PAGEREF _Toc164851116 \h 18
8	Assumptions and Outstanding Issues	 PAGEREF _Toc164851117 \h 19
8.1	Assumptions	 PAGEREF _Toc164851118 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc164851119 \h 19
Appendix A Volumes	 PAGEREF _Toc164851120 \h 20
Appendix B Glossary	 PAGEREF _Toc164851121 \h 21
Appendix C Document Control	 PAGEREF _Toc164851122 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements for Historical Sales, Margin & Waste from Sales Aggregation Engine (SAE) to RPAS. 

The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally this document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. 

This interface is for both US and Turkey implementations.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including SAE and RPAS. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Historical Sales, Margin & Waste from SAE to RPAS.
	
Scope
The Interface Specification covers:

audit requirements across the interface
security requirements across the interface
timing/frequency requirements or constraints
support requirements
archiving
the data format to be used for the interface at each stage 
the normal processing required at each stage
recovery from failure required at each stage
volumes.

Note that it is Tesco strategy to avoid placing any business logic in integration layer processing.

Description and Requirements for the End-to-End Interface
Description of the End-to-End Interface

The interface is dealing with transfer of Historical Sales, Margin & Waste Data from SAE to RPAS. The format of this file will be as defined by the existing UK SRM Interface specification number 111. This single physical interface corresponds to the two SRD Logical Data Flows S003 & S082. This interface will be delta upload in nature.

The data extraction is done by SAE. The extracted data is processed inside SAE system to apply the business logic to suit the requirement of the RPAS system and then the final data, in the form of positional flat file, is placed into a shared location inside SAE system. 

Once the file is placed in the shared location by SAE, BizTalk picks up the same file to transform and then finally to write the file in integration layer shared location which RPAS system can access through CIFS.

The BizTalk interface will poll for the file, at the SAE system shared location for the positional flat file i.e. YYYYMMDD _RPAS_AggregatedPerformanceData_ ccyymmdd_hhmmss.txt.Once the required file containing the extracted data appears on the shared location BizTalk interface will start the processing of Historical Sales, Margin & Waste positional flat file to transform and transfer it from SAE system to the shared location within the integration server which RPAS can access via CIFS file-share. The both the source and target shared locations will be put in a configuration state so that while in implementation this can be changed as per the requirement.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 

Architecture

Requirements for the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The scheduled batch job should be completed before the next batch of job gets scheduled.
Reliability and Availability Requirements
The interface-run should be atomic in nature. Where it is not possible to implement an atomic nature of interface, appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
N/A
Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
No such requirement till the time of writing this document.
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope
The SAE generates Historical Sales, Margin & Waste positional flat file after applying the necessary business logic and transfers to a predefined location. BizTalk interface picks up the flat file from the shared location and transports it to RPAS after necessary transformation for further processing.
Source Message Schema
Name
Optional
Type
Description
Header Record
Record Type


Header record, always 00
Date/Time File Created


Date/Time file created
Date


Date
Data Record
Begin Sub-Group ‘A’
1:*
Multiple numbers of Data Record for single Header Record.
Record Type


Data record, always 01
ItemNo


Unique Item number
Range Event ID


Range Event to which the item belongs to.
Store Cluster ID


Cluster ID for that store
Space Break


It is the indication of space allocated for a merchandising group in a store.
The space break generally falls under A-K (11 count). A being the least space allocation and K being the most space allocation
Average Sales Per Week (ex. VAT)


Average of the total sale of the item excluding VAT for a particular week
Average Singles Per Week


Average of the total item sold as singles for a particular week
Average Weight Per Week


Average of the total weight of the item sold for a particular week
Average No Of Stores for Sales


Average of the total number of stores which have sold that item for a particular week
Average Waste Value Per Week


Average of the total waste sale of the item for a particular week
Average No Of Stores for Waste


Average of the total number of stores which have wasted that item for a particular week
Average Margin Value Per Week


Average of the total retail price minus the total cost for the item for that particular week
Average No Of Stores for Margin


Average of the total number of stores considered for the margin for the particular week
End Group ‘A’


Footer Record
Record Type


Footer record, always 99
Record count


Record count, 9999999999 (Integer 10), this will count data records only. The number will contain leading zeros.

Message Transport Details
Feature
Specification
Additional Information
Source System Name
SAE

Source Platform / OS
Windows 2003

Source Physical Location
Configurable

Source Underlying Data Storage Technology


Target System Name
BizTalk 2006

Target Platform / OS
Windows 2003

Target Physical Location
Configurable

Target Underlying Data Storage Technology
File Share

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
RTI Adapter                       
File Drop(Windows) 	
                 (XCOM) 	

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
Scheduled Batch

Archiving
N/A

Logging
Log via the Operational Framework.

Error Handling
On fail move the file to the failed transmissions location. The file drop failure will be tracked through IMOF functionality and will be done through a change request.

Naming and Configuration

Biztalk – 2006
Package Name: TOM.S003andS082.SAEtoRPAS.HistoricalSalesMargin&Waste
BizTalk Procedure
Name
TOM.S003andS082.SAEtoRPAS
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



Environment and Security Context
Account details will be included here once we have visibility of the environments. 


Non-Functional Requirements
No Such requirement till time of writing this document.

Processing required in the Messaging Stage of the interface
Scope
BizTalk monitors the shared location at SAE side for every new file. Once received, BizTalk picks up the file from the shared location and passes on to the shared location within the integration server (which RPAS can access via CIFS) after carrying out the necessary transformation. Since RPAS is under UNIX environment, the RPAS shared folder will be mounted in Windows environment at BizTalk end using CIFS. 

The file will be created with a temporary name and then it will be renamed once the file creation is complete.
Data Validation
Not Required

Filtering
Not Required

Mapping
Separate mapping document is generated for this interface. The interface is available at the following place in Docshare.

 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS003%2cS082%20Sales%20History%2cMargin%20and%20Wastes%20from%20SAE%20to%20RPAS&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS003%2cS082%20Sales%20History%2cMargin%20and%20Wastes%20from%20SAE%20to%20RPAS&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d

Target Message Schema
Name
Optional
Type
Description
Header Record
Record Type

Alphanumeric
Header record, always 00
Date/Time File Created

Alphanumeric
Date/Time file created
Sequence number

Alphanumeric
Sequence number, increments for all file types (regardless of partial or full refresh files)
Date

Alphanumeric
Date
File Id

Alphanumeric
File ID
Data Record
Begin Sub-Group ‘A’
1:*
Multiple numbers of Data Record for single Header Record.
Record Type

Numeric
Data record, always 01
TPNB

Numeric
Right justified. Pad with zeros on the left 
(e.g. “000000054”).
Range Event ID

Numeric
Right justified. Pad with zeros on the left 
(e.g. “00000001”).
Store Cluster

Numeric
Right justified. Pad with zeros on the left 
(e.g. “00001”).
Space Break

Numeric
Space Break is 1 character and will always fill the field 
(e.g. “A”).
Average Sales Per Week (inc. VAT) This Year

Numeric
Right justified. Pad with zeroes and leading sign on the left. Two decimal places.
(e.g.
“+00000205.95”)
Average Sales Per Week (inc. VAT) Last Year

Numeric
Right justified. Pad with zeroes and leading sign on the left. Two decimal places.
(e.g.
“+00000205.95”)
Average Sales Per Week (ex. VAT)

Numeric
Right justified. Pad with zeroes and leading sign on the left. Two decimal places.
(e.g.
“+00000205.95”)
Average Singles Per Week

Alphanumeric
Right justified. Pad with zeroes and leading sign on the left. Two decimal places.
(e.g.
“+00000205.95”)
Average Weight Per Week

Numeric
Right justified. Pad with zeroes and leading sign on the left. Two decimal places.
(e.g.
“+00000205.95”)
Average No Of Stores for Sales

Numeric
Right justified. Pad with zeroes and leading sign on the left. No decimal places.
(e.g. “+0000085”)
Average Waste Value Per Week

Numeric
Right justified. Pad with zeroes and leading sign on the left. Two decimal places.
(e.g.
“-00000006.73”)
Average No Of Stores for Waste

Numeric
Right justified. Pad with zeroes and leading sign on the left. No decimal places.
(e.g. “+0000085”)
Average Margin Value Per Week

Numeric
Right justified. Pad with zeroes and leading sign on the left. Two decimal places.
(e.g.
“+00000205.95”)
Average No Of Stores for Margin

Numeric
Right justified. Pad with zeroes and leading sign on the left. No decimal places.
(e.g. “+0000085”)
Launch / Promo

Numeric
Left justified. Pad with spaces on the right.
(e.g. “L  “).
End Group ‘A’


Footer Record
Record Type

Alphanumeric
Footer record, always 99
Record count

Alphanumeric
Record count, 9999999999 (Integer 10), this will count data records only. The number will contain leading zeros.

Sample Message Format
<Will be provided>
Message Transport Details 
Feature
Specification
Additional Information
Source System Name
BizTalk

Source Platform / OS
Windows 2003 Server

Source Physical Location
Configurable

Source Underlying Data Storage Technology
File System

Target System Name
Shared folder within Biztalk (IL) which PRAS can access using CIFS.

Target Platform / OS
UNIX

Target Physical Location
TBA

Target Underlying Data Storage Technology
File System

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
RTI File Adaptor 			
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
Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.

Naming and Configuration
BizTalk
Instruction Name: TOM.S003andS082.SAEtoRPAS.HistoricalSalesMargin&Waste
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
Host Details
Account
To be determined 
Operational Details
Worker Threads

Priority

Batch Size

Period

Retry Attempts
4
Timeout
15
Require Data Send

Exception Management
Treat Fatal Adapter Exception As

Treat Unhandled Exceptions As

Environment and Security Context
Not Required
Non-Functional Requirements
Not Required


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
Not Required
Environment and Security Context
Not Required

Non-Functional Requirements
Testing Deliverables
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumptions
1
CIFS will provide link to Windows system for talking to UNIX system and vice-versa.
2
Files will be created with a temporary name and then it will be renamed once creation is complete
3
Source file will not carry information regarding Sales (incl. VAT) and Launch/Promo

Outstanding Issues
ID
Issue
To be addressed by
1
Shared location to be confirmed
Andrew Barker
2
Destination  Shared location to be confirmed
Andrew Barker
3
Error handling to be confirmed with respect to archiving process
Andrew Barker
5
IMOF implementation need to be confirmed
Andrew Barker

	
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
RTI Adapter
Real Time Integrator
Used to transfer file from one location to other.
SAE
Sales Aggregation Engine
A new system under development which will deal with sales summarisation.
RPAS
Ranging System
A participate system inside Space Range Display deals ranges and basic modelling of products. 
CIFS
Common Internet File Sharing
A utility used to provide common platform between disparate systems.
	
Document Control
Change Record

Author
Date
Version
Change Reference, description
Supriyo Chakraborty
12-Apr-07
0.1D
Draft
Supriyo Chakraborty
20-Apr-07
0.2D
Incorporated the review comments.











Related Documents

Author	
Date
Version
Title
Bob Trewin
13-Apr-2006
V 3.0
UK 111
Sudha Vaidyanathan
12-Apr-2007
V0.4
BSD for Sales Aggregation V0.4.doc
Sudha Vaidyanathan
12-Apr-2007
V0.1
SalesAggregation_Technical_Specifications_V0.1.doc






Distribution

Name
Position
Approver/Contributor/Other
David Onyett


Leon Benjamin


Mary Welch


Andrew Barker


Venkateswara Rao


















Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version: 0.2, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT v of  NUMPAGES 23	Date:  SAVEDATE \@ "d MMM yyyy" 23 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.2, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 23 of  NUMPAGES 23	Date:  SAVEDATE \@ "d MMM yyyy" 23 Apr 2007



