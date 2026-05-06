		









`


TOM Integration
Interface Specification
On 
Base Product Data Update
From IDS to IKB


[S036]





Project BEN Code:
W60416
Author:Nitin SinghaiDate:
18/01/2007
Version:
0.4D
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft
Modified By:

Reviewed By:
Adrian Hinks (initial review 16/02/07)

Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
18-01-2007
0.1D
Draft
Nitin Singhai
14-02-2007
0.2D
Draft
Adrian Hinks
16-02-2007
0.3D
Changes resulting from review
Nitin Singhai
06-03-2007
0.4D
Changes resulting from review

Reviewers

Name
Date
Version
Position
Andrew Barker



Adrian Hinks
16-02-2007
0.2D
Engagement Architect










At least one reviewer is required.

Sign-Off

By signing this form, I understand and agree with the contents of this document.

Business Owner/Customer

Position

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



Document Source
 HYPERLINK "http://docshare/UK%20IT/TOM%20Integration/Shared%20Documents/Forms/AllItems.aspx?RootFolder=%2fUK%20IT%2fTOM%20Integration%2fShared%20Documents%2f1%20%2d%20Design%2fInterface%20Design%20Documents%2fSpace%20Range%20and%20Display%20%28SRD%29%20Interfaces%20%28S%2dPrefix%29%2fS036&View=%7bDFD57AEE%2d4D2D%2d4A52%2d8E91%2dA19AEFB34619%7d" DocShare: UK IT/TOM Integration/Shared Documents

Related Documents

A complete interface specification requires three documents- an Interface Specification, an Information Architecture Context diagram, and a Mapping spreadsheet. This section identifies these documents plus other documents as appropriate.


Information Architecture Context diagram
S036 Information Context Diagram - Product Information Update.vsd

Mapping spreadsheet
S036- Product Information Update (IDS to IKB) Mappings.xls

Other Reference Documents
Tesco - Product Data Interface & Dimension Changes v1 0.doc
Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc160950160 \h 6
1.1	Purpose of Document	 PAGEREF _Toc160950161 \h 6
1.2	Background	 PAGEREF _Toc160950162 \h 6
1.3	Scope	 PAGEREF _Toc160950163 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc160950164 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc160950165 \h 7
2.2	Architecture	 PAGEREF _Toc160950166 \h 7
2.3	Requirements of the End-to-End Interface	 PAGEREF _Toc160950167 \h 7
2.4	Non-Functional Requirements of the End-to-End Interface	 PAGEREF _Toc160950168 \h 8
3	Processing Required in the Extract Stage of the Interface	 PAGEREF _Toc160950169 \h 9
3.1	Scope	 PAGEREF _Toc160950170 \h 9
3.2	Source Message Schema	 PAGEREF _Toc160950171 \h 9
3.3	Message Transport Details	 PAGEREF _Toc160950172 \h 9
4	Processing Required in the SSIS Stage of the Interface	 PAGEREF _Toc160950173 \h 10
4.1	Scope	 PAGEREF _Toc160950174 \h 10
4.2	Package Overview	 PAGEREF _Toc160950175 \h 10
4.3	Data Validation	 PAGEREF _Toc160950176 \h 10
4.4	Filtering	 PAGEREF _Toc160950177 \h 10
4.5	Mapping	 PAGEREF _Toc160950178 \h 10
4.6	Target Message Schema	 PAGEREF _Toc160950179 \h 10
4.7	Message Transport Details	 PAGEREF _Toc160950180 \h 12
4.8	Naming and Configuration	 PAGEREF _Toc160950181 \h 12
4.9	Environment and Security Context	 PAGEREF _Toc160950182 \h 13
4.10	Non-Functional Requirements	 PAGEREF _Toc160950183 \h 13
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc160950184 \h 14
5.1	Scope	 PAGEREF _Toc160950185 \h 14
5.2	Data Validation	 PAGEREF _Toc160950186 \h 14
5.3	Filtering	 PAGEREF _Toc160950187 \h 14
5.4	Mapping	 PAGEREF _Toc160950188 \h 14
5.5	Target Message Schema	 PAGEREF _Toc160950189 \h 14
5.6	Message Transport Details	 PAGEREF _Toc160950190 \h 14
5.7	Naming and Configuration	 PAGEREF _Toc160950191 \h 14
5.8	Environment and Security Context	 PAGEREF _Toc160950192 \h 14
5.9	Non-Functional Requirements	 PAGEREF _Toc160950193 \h 14
6	Testing Deliverables	 PAGEREF _Toc160950194 \h 15
7	Deployment	 PAGEREF _Toc160950195 \h 16
8	Assumptions and Outstanding Issues	 PAGEREF _Toc160950196 \h 17
8.1	Assumptions	 PAGEREF _Toc160950197 \h 17
8.2	Outstanding Issues	 PAGEREF _Toc160950198 \h 17
Appendix A Volumes	 PAGEREF _Toc160950199 \h 18
Appendix B Glossary	 PAGEREF _Toc160950200 \h 19
Appendix C Document Control	 PAGEREF _Toc160950201 \h 20

Introduction
Purpose of Document
The purpose of this document is to describe the interfacing requirements w.r.t Product reference data between the IDS to IKB. The document is of a sufficiently technical nature to allow a developer to build an actual interface. Additionally the document contains detail that might sit logically within a Technical System Design (TSD) document, but is contained here for expediency. There is therefore no associated TSD for this interface. 

This interface is for US implementation.

Background
As part of Tesco Operating Model program, there is requirement to bridge the functionalities of enterprise applications including IDS and IKB. To achieve this functionality, high level process flow architecture has been designed and approved by Tesco’s Enterprise Architecture team. As part of this process flow architecture there is a set of interfaces that has been identified to be developed to transfer Product reference data from IDS into IKB.
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
The interface is a extract of Product Reference Data from IDS using Common Forms and uploads into the IKB Product Holding Table using SSIS. The Upload is a full upload in nature.
Architecture
 EMBED Visio.Drawing.11  

Requirements of the End-to-End Interface
The interface will run once a day, on scheduled basis, and consists of a SQL Server Integration Services package that extracts data from the IDS, and formats it into the target Table format. 

The interface is meant to run nightly at a pre-configured time 5 days a week (Tuesday to Saturday), which on completion is expected to upload the Product data in a Product Holding Table in IKB.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. These components will be pluggable, and will be useable from BizTalk, RTI, and SSIS. At the time of writing (2007-01-18) the components are in design. Although not ready for use, they are included on the Information Architecture Context diagram where their functionality is required. Developers should put a ‘placeholder’ in their code / configurations as appropriate.

Non-Functional Requirements of the End-to-End Interface

Audit Requirements
The interface will use the components provided by the Operational Framework to satisfy audit requirements.
Security Requirements
The interface executes within a secure private domain. There are no additional security considerations required.
Timing/Cut-off Constraints
To be finalised.
Performance Requirements
The interface should be capable of extracting data from IDS using Common Forms, delivering the resulting data to IKB Product Holding Table before the identified cut-off time. The interface should run on scheduled batch basis. 
Reliability and Availability Requirements
The interface-run should be non atomic in nature. Appropriate mechanisms should be in place to raise/alert appropriate parties.
Scalability Requirements
No Scalability requirement. The requirement is to deliver a single extract. It is anticipated that the volume of data transferred will continue to remain within the capability provided by this implementation.
Operational Support Requirements
The scheduled start of the extract job and/or the completion of the target table update should be defined as IMOF events.  
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
Although multi-byte character set support is not required for US or Turkey, the interface will support multi-byte character sets through integration. 
 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing Required in the Extract Stage of the Interface 
Scope
This section describes the data sources required by this interface and the services used to access the data.
 
Source Message Schema
The data for this interface resides in the IDS. Common Form Service CF_GetSKUHierarchy, cf_getdivisionhierarchy_usp, cf_getsupplierhierarchy_usp are called by the s036_getitemdetails_usp. The services are exposed as stored procedures and return row sets representing SKU Items in the Item Common Form. 
Message Transport Details

Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
Windows 2003 Server

Source Physical Location
SQL SERVER 2005

Source Underlying Data Storage Technology
RDBMS

Target System Name
SSIS

Target Platform / OS
Windows 2003 Server

Target Physical Location


Target Underlying Data Storage Technology
RDBMS

Transfer Function
HTTP (Put/Post) 		
HTTPS (Put/Post) 	
Message Queue	 	 
FTP			
File Drop(Windows) 	
                 (XCOM) 	
Common Forms 		

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
Bulk Data		

Real-time/Scheduled Batch
Not yet decided

Archiving
There is no requirement to archive the messages.

Logging
Log via the Operational Framework.

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.



 


Processing Required in the SSIS Stage of the Interface
Scope
This section describes the discreet steps within the SSIS package to extract and format data. The target schema is included in this section. 
Package Overview
SSIS extracts the product reference data from IDS using Common Forms, nightly at predefined time, 5 days a week.  In turn, the data is inserted into an Intermediate table at IKB which is the Product Holding Table
Data Validation
N/A
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
Holding Table Field Name
Type
Length
Description
IsProcessed
int

Field used by JDA for Internal purpose. Pass null from integration.
DateTime
datetime

This field will be populated with the current date/time that records are added. This will be done as part of the process that adds data to this table. This field will be used to sort the records to ensure that they are processed in the correct order.
Product_description
varchar
32
Product Name
UPC
varchar
13
UPC Code
Product_ID
varchar
16
Tesco Product Number
EAN_Code
varchar
13
EAN Code
Department
varchar
30
Department Number
Display_Group
varchar
30
Display Group of the Product
Manufacturer
varchar
30
Manufacturer Name
Supplier
varchar
40
Supplier Name
Case_Pack_Size
real

CaseTotal Number
Height
real

Height of Product
Width
real

Width of Product
Depth
real

Depth of the Product
Tray_Height
real

Tray Height of the Product
Tray_Width
real

Tray Width of the Product
Tray_Depth
real

Tray Depth of the Product
Tray_Pack_Size
real

Tray Total Number
Colour
varchar
30
Color of the Product
Product_launch_date
datetime

Product Launch date 
Product_end_date
datetime

Product End date
SEL_type
varchar
30
Shelf Edge Label Type
Good_better_best
varchar
30
Product Characteristics as Good Better or Best
Warehouse_indicator
varchar
30
Indicator
Commercial_unit_height
real
7
Used for any product height change.
Commercial_unit_width
real
7
Used for any product width change.
Commercial_unit_depth
real
7
Used for any product depth change.
Commercial_tray_height
real
7
Used for any product tray height change.
Commercial_tray_width
real
7
Used for any product tray width change.
Commercial_tray_depth
real
7
Used for any product tray depth change.
Dummy_product
int

Indicator to Indicate whether a Product is a dummy Product or Authorized.
Authorised
int

Indicator to Indicate whether a Product is a dummy Product or Authorized.
Diamond_line
int

Product Quality Attribute 
Organic
int

Product Quality Attribute
Finest
int

Product Quality Attribute
Value
int

Product Quality Attribute
Future_dimension_present
int

Internal use for JDA to identify any product Dimension changes.
Price
Float
7
Price of the Product
Case_cost
Float
7
This is a derived field. (Unit Cost X Case Pack Size)
Unit_cost
Float
7
Unit Cost of the Product
Subclass_code
varchar
30
Subclass ID
Subclass_desc
varchar
30
Subclass Name
Traypack_indicator
varchar
30
Indicator. If Tray Pack can break to adjust on shelf.
Seasonal
varchar
30
Attribute of a Product.
Phasing
varchar
30
Attribute of a Product.
Brand
varchar
30
TescoBrand of the Product
Buyer
varchar
30
Buyer
Tray_Units_High
int

Number of Units high in a Tray
Tray_Units_Wide
int

Number of Units Wide in a Tray
Tray_Units_Deep
int

Number of Units Deep in a Tray

Message Transport Details 
For messages destined for IKB system, the following applies.	

Feature
Specification
Additional Information
Source System Name
SSIS

Source Platform / OS
SQL Server 2005

Source Physical Location


Source Underlying Data Storage Technology


Target System Name
IKB

Target Platform / OS
SQL Server

Target Physical Location


Target Underlying Data Storage Technology


Transfer Function

HTTP (Put/Post			
HTTPS (Put/Post) 		
Message Queue			
FTP						
File Drop (Windows) 		
                 (XCOM) 		
RTI File Adapter                              
SSIS                                                  

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
RDBMS extract

Archiving
There is no archiving requirement

Logging
Should logs be kept of all actions? For how long should these be stored?
Logging should occur, such that the message can be recreated if necessary.

Error Handling
Not yet decided

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


 
Naming and Configuration

SSIS
Package Name: TOM_IDSIKB_Product_Update_pkg

Name
IDSIKBProductUnload_sp
<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



Environment and Security Context
Account details will be included here once we have visibility of the environments. 

Non-Functional Requirements
On successful delivery of the data to the target system, the audit log should be updated via the Operational Framework pipeline component or adapter (to be determined).

In the event of a failure of transformation of data should be written to the failed log database, and an alert should be raised.






Processing required in the <third stage of the interface>
Scope
There is no intermediate staging is required for this interface. So this section is not applicable.
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

Not RequiredTesting Deliverables
This section should contain a list of discrete deliverables. The following table is an illustrative template only. The exact deliverables will depend on the technologies employed in the interface. 

Deliverable
Description
TBD <stored proc name>
Common Form Stored Procedure
TBD <stored proc name>
Common Form Stored Procedure
TBD <service name>
Common Form Web Service
TBD <SSIS package name> 
Package 
TBD <RTI configuration file>
Xml configuration file exported from RTI. For testing, this should contain the configuration required to support this interface only. 
For production, configuration should be documented under section 7 Deployment.


TBD <script name> 
Unit Test Scripts. Scripts should be provided to:
create databases (including stored procedures).
populate with the minimum set of test data to satisfy functional requirements
notes showing how to use scripts and describing the functions tested.
<installer>
Installers as appropriate to the technology being used.

Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption



Outstanding Issues
ID
Issue
To be addressed by
1
Timings and cut-off constraints need to be defined. Require input from SRD. 
Space, Range, Display Solution Architects plus Information Architect
2
Deployment not yet considered
Information Architect
3
Alert numbers/identifiers are yet to be defined



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
IKB
Intactix Knowledge Base
SQL Server Database provided by JDA Intactix for Space Planning and Floor Planning.
IDS
Information Data Store
A store of data, logically residing in the EIA layer, that provides an authoritative single view of a discrete data component specific to the enterprise. Eg: Product, Store, etc. IDS's reside in the EIA Layer, and are accessed through the EAI Layer.
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
18-Jan-2007
0.1D
Draft
Nitin Singhai
06-Mar-2007
0.4D
Incorporated Review comments.











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
Engagement Architect

David Onyett
Project Lead

























	








Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT ii of  NUMPAGES 20	Date:  SAVEDATE \@ "d MMM yyyy" 6 Mar 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































