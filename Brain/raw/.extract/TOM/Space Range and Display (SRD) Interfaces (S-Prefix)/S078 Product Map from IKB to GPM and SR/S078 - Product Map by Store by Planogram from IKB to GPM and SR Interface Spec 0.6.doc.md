		









`


TOM Integration
Interface Specification
On 
Product Map by Store by Planogram
From IKB to GPM & SR


[S078]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
01/03/2007
Version:
0.6D
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft
Modified By:
Prasanth Dukaram
Reviewed By:
Andrew Barker

Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
01-03-2007
0.1
Draft
Prasanth Dukaram
16-03-2007
0.2
Merged S031 interface specification with this document
Prasanth Dukaram
19-03-2007
0.3
Updated review comments from Andy Barker
Prasanth Dukaram
10-04-2007
0.4
Updated the design change
Nitin Singhai
17-04-2007
0.5
Updated the design change
Prasanth Dukaram
10-04-2007



Reviewers

Name
Position
Andrew Barker
Engagement Architect








At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer
Andrew Barker
Position
Engagement Architect
Signature
<Physical signature or via email approval>
Date
dd/mm/yyyy (<version signed off>)

Distribution List

Name
Date of Issue
Version
Andrew Barker


John Cowper


Jon Braggs


David Onyett


Venkateswara Rao


Mary Welch



Document Source
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS036&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" DocShare: UK IT/TOM Integration/Shared Documents

Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.


Information Architecture Context diagram
S078 Information Context Diagram - Product Map by Store by Planogram (IKB to GPM).vsd

Mapping spreadsheet
S078 - Product Map by Store by Planogram (IKB to Integration Layer) Mappings.xls
S078 - Product Map by Store by Planogram (Integration Layer to GPM) Mappings.xls
S078 – Planogram Product Position (IKB to Store range) Mappings.xls
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc161828265 \h 6
1.1	Purpose of Document	 PAGEREF _Toc161828266 \h 6
1.2	Background	 PAGEREF _Toc161828267 \h 6
1.3	Scope	 PAGEREF _Toc161828268 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc161828269 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc161828270 \h 7
2.2	Architecture	 PAGEREF _Toc161828271 \h 7
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc161828272 \h 7
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc161828273 \h 9
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc161828274 \h 10
3.1	Scope	 PAGEREF _Toc161828275 \h 10
3.2	Source Message Schema	 PAGEREF _Toc161828276 \h 10
3.3	Message Transport Details	 PAGEREF _Toc161828277 \h 10
3.4	Naming and Configuration	 PAGEREF _Toc161828278 \h 11
3.5	Environment and Security Context	 PAGEREF _Toc161828279 \h 11
3.6	Non-Functional Requirements	 PAGEREF _Toc161828280 \h 12
4	Processing Required in the SSIS Stage of the Interface for GPM	 PAGEREF _Toc161828281 \h 13
4.1	Scope	 PAGEREF _Toc161828282 \h 13
4.2	Package Overview	 PAGEREF _Toc161828283 \h 13
4.3	Data Validation	 PAGEREF _Toc161828284 \h 13
4.4	Filtering	 PAGEREF _Toc161828285 \h 13
4.5	Mapping	 PAGEREF _Toc161828286 \h 13
4.6	Target Message Schema	 PAGEREF _Toc161828287 \h 13
4.7	Message Transport Details	 PAGEREF _Toc161828288 \h 14
5	Processing required in the SSIS Stage of the Interface for Store range	 PAGEREF _Toc161828289 \h 15
5.1	Scope	 PAGEREF _Toc161828290 \h 15
5.2	Data Validation	 PAGEREF _Toc161828291 \h 15
5.3	Filtering	 PAGEREF _Toc161828292 \h 15
5.4	Mapping	 PAGEREF _Toc161828293 \h 15
5.5	Target Message Schema	 PAGEREF _Toc161828294 \h 15
5.6	Sample Target Message	 PAGEREF _Toc161828295 \h 15
5.7	Message Transport Details	 PAGEREF _Toc161828296 \h 16
6	Testing Deliverables	 PAGEREF _Toc161828297 \h 17
7	Deployment	 PAGEREF _Toc161828298 \h 18
8	Assumptions and Outstanding Issues	 PAGEREF _Toc161828299 \h 19
8.1	Assumptions	 PAGEREF _Toc161828300 \h 19
8.2	Outstanding Issues	 PAGEREF _Toc161828301 \h 19
Appendix A Volumes	 PAGEREF _Toc161828302 \h 20
Appendix B Glossary	 PAGEREF _Toc161828303 \h 21
Appendix C Document Control	 PAGEREF _Toc161828304 \h 22

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Product Map by Store by Planogram data from the IKB (JDA) to GPM and Store range system. The document is of a sufficiently technical in nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US and Turkey implementation.

Background
As part of the process of managing Space, Range and Display activities in store it is important to identify that the store has accurately completed all space range and display activities. The process of product mapping will allow the update of capacities for replenishment systems wherever required. This will also help the centre to understand how well stores are conforming to the planograms, the product map can provide the store with a method by which to update the facings of a product on the shelf edge label. This in turn needs the details of the products to be loaded into Product mapping tables. This interface provides the location of Products to the Product by Store by Planogram table 
In Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including IKB, GPM and Store range. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed for product mapping and store range system 
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
This interface extracts Planogram Product Position data from IKB holding tables of JDA to Group Product Mapping (GPM) Holding Table and Store range system as a flat file using SSIS. The Upload is a delta upload in nature. It is application’s responsibility to provide the deltas to integration layer.

The batch extract would initiate the Sql Server Integration service package. A query will be fired by the SSIS package to fetch the data from the holding tables of IKB. Further steps within the SSIS package would transform the data in to a file formats required by store range and GPM. After successful creation of the flat files in the integration layer, the IKB holding table will be updated with the timestamp (the time when integration layer has picked up the data). When the process is complete, another SSIS package would read the flat file created for GPM and load the holding table of GPM. A RTI Instruction in parallel would transfer the store range file from the IL layer on to the file share of the store range system.

On the Integration layer, the transaction within SSIS package would either create both the files or none.
Once the files are transferred successfully to their respective target location i.e. into the GPM Holding Table and Store Range file share location, these Intermediate files in Integration layer should be deleted.
This interface caters to two logical interfaces S031 and S078
Architecture
 EMBED Visio.Drawing.11  




Requirements of the End-to-End Interface

The interface will run once a day, on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IKB, and transforms it into an intermediate files and transfers it into the target file format for store range and target table format for GPM.

For GPM, the interface should transfer the data for Product Location from IKB to a File Drop location in the Integration layer in a flat file format. Another SSIS package should then read the data from the flat file and Insert it into the GPM holding table. The above process should run at a pre-configured time (to be determined). On failure, this step can be repeated.  Once the process is successfully complete, this Intermediate file from the Integration layer will be deleted.

For Store range, the file is delivered to Store range system to a folder on the host. A RTI Instruction will transfer the flat file from Integration layer to the store range system host. On failure, this step can be repeated.  Once the process is successfully complete, the Intermediate file from the Integration layer will be deleted.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI and SSIS. At the time of writing (2007-03-01) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface
 
Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There is no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from IKB through SSIS Service layer using SQL Stored Procedure, delivering the resulting data into flat file for GPM and Store Range correspondingly. For GPM, The flat file should be read by another SSIS package and populate the data into a Holding Table (name TBD) in GPM. For Store Range, flat file should be transferred to store range. These processes should occur before the identified cut-off time. The interface should run on scheduled batch basis. 
Reliability and Availability Requirements
The interface-run should be atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties (TBD).
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The successful delivery, failure in the creation of the extract, and failure in message transport, must be recorded by the Integration Management Operational Framework (IMOF). In the event of failure, an alert should be raised. Alerts will be monitored by HSC Operations and passed to support as appropriate. (Refer to 8.3 Outstanding Issues).
Likelihood of Change Requirements
Since this interface is developed on assumptions There will be a change for this interface is expected.
Cultural/Global Consideration Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration. 
 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing Required in the Extract Stage of the Interface 
Scope
A scheduled batch job/s runs, at a pre-configured time, to extract the Product map by store by planogram data from the IKB holding table (csg_product_map) by executing SQL server Integration Services package. The returned data-set will be transformed to the required format within SSIS package and written to intermediate files before the actual transfer of data to store range flat file and GPM holding table.

After successful completion of data extraction, current date time stamp will be updated against all the records on IKB holding table. 
Source Message Schema
The data for this interface resides in the IKB in a holding table. 

Holding Table Field Name
Type
Length
Description
Datetime
Datetime

System Generated
Store_No
Varchar
32
Store Number of a Product
Live_Date
Datetime

Relevant to planogram or floorplan 
Planogram_ID
Varchar
16
Planogram Number
Module_Number
Varchar
32
Module Number of a Product
Segment_Number
Integer

Segment Number of a Product
Fixture_Number
Integer

Fixture Number of a Product
Position_Number
Integer

Position Number of a Product
Product_Code
Varchar
16
Product ID
Facings_wide
Integer

Facings Wide of a Product
Facings_high
Integer

Facings High of a Product
Facings_deep
Integer

Facings Deep of a Product
Multi_located_Indicator
Integer

Multi located indicator for a Product
Display_group
Varchar
30
Display group id in which the product belongs to
No_of_locations
Integer

Number of locations of a product
Number_of_labels
Integer

Number of labels for a product to be printed
SRP_indicator
Integer

Shelf Ready Package Indicator for a product
IL_Time_Stamp
Datetime

IL will update the timestamp after reading the records from IKB
Message Transport Details

Feature
Specification
Additional Information
Source System Name
IKB

Source Platform / OS
Windows 2003 Server

Source Physical Location
SQL SERVER 2005

Source Underlying Data Storage Technology
RDBMS

Target System Name
--

Target Platform / OS
Windows 2003 Server

Target Physical Location
--

Target Underlying Data Storage Technology
In Memory

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
SSIS			

Data Format.
XML			
Delimited		
Positional		
RDBMS       		                     

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
Log via the Operational Framework.

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.



 Naming and Configuration

SSIS
Package Name: TOM.S078.IKBtoGPMStorerange.PlanogramProductPosition.dtsx
SSIS Procedure
Name
S078_GetProductsbyPlanogram_usp.sql
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>




Files and Folders
Local Folder
Name

Local File
Temporary Name

Name



Environment and Security Context
 
This section should contain any additional environment specific details deemed necessary. The information will depend on the technologies used by the interface. For example employing BizTalk this section would include details of the host – In-Process Host, Isolated Host, and whether the host was Trusted/Untrusted. For interfaces employing the RTI indicate whether the instruction is Hosted/Unhosted.  

Also indicate the account that the process will run under. In projects where the target deployment environment does not exist at the time of writing the interface specification, the information should be added at a later date (but obviously, prior to deployment).

 
Account details will be included here once we have visibility of the environments.  


Non-Functional Requirements

This section should contain any non-functional requirements pertaining to this stage of the interface.



Processing Required in the SSIS Stage of the Interface for GPM
Scope
This section describes the discrete steps within the SSIS package to extract and format data. The target schema is included in this section. This segment will process the data picked from IKB database and transform into Intermediate flat file format which is hold in Integration layer. The data from the flat file is then transformed by another SSIS package and inserted into a GPM holding table (name of the holding table to be determined). In turn the holding table data will get loaded into tbl_ProductPlanogram in GPM database.
Package Overview
SSIS extracts the product reference data from IKB via SQL Server OLEDB connection, at a predefined time. In turn, the data is transformed into an Intermediate flat file which is hold in Integration layer. Another SSIS package should then run and insert the data from the Intermediate flat file to a Holding table at GPM using OLEDB connection.
Data Validation
N/A.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
IKB – GPM Intermediate flat file format

      File Name: S078_IKBtoGPMProductMapddmmyyhhMMss.txt

Field Name
String
Length
Occurs
Header Record

124
1:1
HeaderRECTYPE
Varchar
1
Always ‘0’
RUNDATE
Varchar
8
YYYYMMDD
RUNTIME
Varchar
6
HHMMSS
FILLER
Varchar
109
SPACES
Detail Record

124
1:*
DetailRECTYPE
Varchar
1
Always ‘1’
Planogram_ID
Varchar
16

SKUID
Varchar
16

StoreID
Integer
10

ModNumber
Integer
10

ShelfID
Integer
10

FacingWide
Integer
10

FacingsHigh
Integer
10

FacingsDeep
Integer
10

IsMultilocated
bit
1

ProdPositionNo
Integer
10

NoOfLocations
Integer
10

PlanogramLiveDate
Datetime
10

Trailer Record

124
1:1
TrailerRECTYPE
Varchar
1
Always ‘9’
RECCOUNT
Integer
9
XXXXXXXXX
FILLER
Varchar
114
SPACES

GPM Holding Table Format

Holding Table Field NameTypeLenPrecisionMandatoryDescriptionPlanogram_IDVarchar16YesUnique Identifier for  planogramStoreIDInteger410YesThis will contain the store idModNumberInteger410NoMod label in the storeShelfIdInteger410NoShelf number on the modProdPositionNoInteger410NoThis field will give the position of the product on the shelfSKUIDVarchar16YesItem number i.e. Tesco specific product numberFacingWideInteger410YesThis will give the no of products across the width of the shelfFacingsHighInteger410YesThis will give the no of products across the width of the shelfFacingsDeepInteger410YesThis will give the no of products across the breadth of the shelfIsMultilocatedBit11NoThis field will tell whether the product is multilocated or notNoOfLocationsInteger410NoNumber of locations PlanogramLiveDateDatetime4NoDate when Planogram goes active in a store
Message Transport Details 
For messages destined for GPM system (from IKB to Intermediate file in Integration layer), the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
Windows 2003 Server

Source Physical Location
SQL Server 2005 database

Source Underlying Data Storage Technology

	

Target System Name
File Share

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter			
SSIS						

Data Format

XML  				
Delimited 			
Positional 			
RDBMS                                            

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous 			
Asynchronous 			
Bulk Data 			

Real-time/Scheduled Batch
Scheduled Batch

Archiving
N/A

Logging
Log via the Operational Framework.

Error Handling
Not yet decided

For messages destined for GPM system (from Intermediate file in Integration layer to GPM), the following Message Transport Details applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
Windows 2003 Server

Source Physical Location


Source Underlying Data Storage Technology
File System
 	

Target System Name
GPM

Target Platform / OS
SQL Server

Target Physical Location


Target Underlying Data Storage Technology
RDBMS

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter			
SSIS						

Data Format

XML  				
Delimited 			
Positional 			
RDBMS                                            

Decryption/Encryption
No

Decompression/Compression
No

Transmission Mode
Synchronous 			
Asynchronous 			
Bulk Data 			

Real-time/Scheduled Batch
Scheduled Batch

Archiving
N/A

Logging
Log via the Operational Framework.

Error Handling
Not yet decided


Naming and Configuration

SSIS
Package Name: TOM.S078.SharedLocationtoGPM.dtsx
SSIS Procedure
Name

<Placeholder for other package components/steps>


<Placeholder for other package components/steps>





Processing required in the SSIS Stage of the Interface for Store range 
Scope
This section describes the parallel steps within the SSIS package to extract and format data to another target schema. The target schema is included in this section. This segment will process the data picked from IKB database and transform into flat file format which is required by Store range system. The flat files created will be in the integration layer. A RTI Instruction will then transfer the file from the IL to the Store range system.
Data Validation
Not Required
Filtering
Not Required
Mapping
Mapping document will be provided subsequently
Target Message Schema
Field Name
String
Length
Occurs
Header Record

132
1:1
HeaderRECTYPE
Varchar
1

RUNDATE
Varchar
10

RUNTIME
Varchar
6

FILLER
Varchar
115

Detail Record

132
1:*
DetailRECTYPE
Varchar
1

Store_no
Integer
10

Product_code
Varchar
25

Display_group
Varchar
30

Planogram_ID
Varchar
16

Facings_wide
Integer
10

Mod_sequence
Integer
10

Shelf_ID
Integer
10

Product_sequence
Integer
10

Start_mod
Integer
10

Trailer Record

132
1:1
TrailerRECTYPE
Varchar
1

RECCOUNT
Varchar
9

FILLER
Varchar
122


Sample Target Message
The source message is from database tables and is getting converted to the target file format in a package. The following message format is the target message format. Alternate fields are in bold for readability.
The numbers used here are part of the example given in the notes section of the mapping document

File Name: S078_PlanogramProdPositionddmmyyhhMMss.txt

02007-01-01120000
10000012345               1234567890                    0987654321          12345600000000100000000011000000002000000000100000000010
90000000003
Message Transport Details
Feature
Specification
Additional Information
Source System Name


Source Platform / OS
Windows 2003 Server

Source Physical Location


Source Underlying Data Storage Technology


Target System Name
Store Range

Target Platform / OS
Windows 2003 Server

Target Physical Location
Tba

Target Underlying Data Storage Technology
File Share

Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
RTI File Adaptor 			
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
Bulk Data 			

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


File Transfer to Store range through RTI Instruction
The file for Store range system will be available in the integration layer. A RTI Instruction will be configured to transfer the file to the store range system

RTI
Instruction Name: S078.IKB to SR.Product Map by store by Planogram
Instruction Details
Description
File delivery of Product Map by store by planogram file from IKB to Store range
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
15
Retry Attempts
4
Timeout
60
Require Data Send
True
Exception Management
Treat Fatal Adapter Exception As
Fatal
Treat Unhandled Exceptions As
Fatal

Testing Deliverables
This section should contain a list of discrete deliverables. The following table is an illustrative template only. The exact deliverables will depend on the technologies employed in the interface. 

Deliverable
Description
TBD <stored proc name>
Stored Procedure
TBD <stored proc name>
Stored Procedure
TBD <service name>

TBD <SSIS package name> 
Package 




TBD <script name> 
Unit Test Scripts. Scripts should be provided to:
Create databases (including stored procedures).
populate with the minimum set of test data to satisfy functional requirements
notes showing how to use scripts and describing the functions tested.
<installer>
Installers as appropriate to the technology being used.

Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
Since the Holding table details are not available for GPM, Data type and length of fields of destination table GPM Holding Table are based on tbl_ProductPlanogram.
2
The target file details are not available for store range, data type and length of the fields of destination file Store range are based on the source IKB holding table csg_product_data and IDS

Outstanding Issues
ID
Issue
To be addressed by
1
PlanogramProdDetails Holding Table generation script to be provided by GPM. Using PlanogramProdDetails table (name, datatypes and size based on tbl_PlanogramDetails table) may result in rework if there are significant changes when final script issued from GPM
GPM
2
Timings and cut-off constraints need to be defined. Require input from GPM
Product Mapping Solution Architects plus Information Architect.
3
Alert numbers/identifiers are yet to be defined
Solution Architect
4
The design of the IMOF is still being worked and will require retro-fitting to the interface.
IMOF team
5
BSD is not signed Off for this Interface and may result in change in requirements.
SRD Team
6
Complete Structure of the IKB holding table is not decided
JDA Team
7
Maintenance mechanism of IKB holding table to be decided
Solution Architect


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
RMS
Retek Merchandising System
Retek Merchandising System is getting installed for TESCO Merchandising operations in US. This system will governs the Merchandising operations; Receive base Master & Transaction data and from other systems and Provide data to next level of operation system as part of Retail systems chain.
GPM
GroupProductMapping
SQL Server Database provided by Product mapping for loading Product details.
IKB
Intactix Knowledge Base
SQL Server Database provided by JDA Intactix to maintain Space Planning and Floor Planning data.
IMOF
Integration Management Operational Framework
IMOF is a framework which is pluggable to any Biztalk, RTI and SSIS for alerting, exception handling, defining rules, scheduling etc

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
01-Mar-2007
0.1
Draft
Prasanth Dukaram
16-Mar-2007
0.2
Amended with S031 requirements
Prasanth Dukaram
19-Mar-2007
0.3
Review comments updated
Prasanth Dukaram
10-Apr-2007
0.4
Design Change updated
Nitin Singhai
17-Apr-2007
0.5
Design Change updated
Prasanth Dukaram
20-04-2007
0.6
Source Message Schema Updated



Related Documents

Author	
Date
Version
Title


















Distribution

Name
Position
Approver/Contributor/Other
Jon Braggs
Enterprise Architect

Andrew Barker
Solution Architect

Mary Welch
Manager – SRD TOM project



















	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version 0.1 REF DOC_VER , Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT ii of  NUMPAGES 25	Date:  SAVEDATE \@ "d MMM yyyy" 19 Apr 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































