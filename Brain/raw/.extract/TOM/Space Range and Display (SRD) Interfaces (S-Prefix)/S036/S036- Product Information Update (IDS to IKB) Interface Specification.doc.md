		









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
Nitin Singhai
18-01-2007
0.1D
Draft













Reviewers

Name
Date
Version
Position
Andrew Barker

















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
Clear Case

Related Documents

File Name: Tesco - Product Data Interface & Dimension Changes v1 0.doc




Information Architecture Context diagram


Mapping spreadsheet

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc157846016 \h 6
1.1	Purpose of Document	 PAGEREF _Toc157846017 \h 6
1.2	Background	 PAGEREF _Toc157846018 \h 6
1.3	Scope	 PAGEREF _Toc157846019 \h 6
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc157846020 \h 7
2.1	Description of the End-to-End Interface	 PAGEREF _Toc157846021 \h 7
2.2	Architecture	 PAGEREF _Toc157846022 \h 7
2.3	Requirements for the End-to-End Interface	 PAGEREF _Toc157846023 \h 7
3	Processing required in an Extract-Stage of the interface	 PAGEREF _Toc157846024 \h 9
3.1	Scope	 PAGEREF _Toc157846025 \h 9
3.2	Source Message Schema	 PAGEREF _Toc157846026 \h 9
3.3	Sample Message Format	 PAGEREF _Toc157846027 \h 9
3.4	Message Transport Details	 PAGEREF _Toc157846028 \h 9
3.5	Naming and Configuration	 PAGEREF _Toc157846029 \h 10
3.6	Environment and Security Context	 PAGEREF _Toc157846030 \h 10
3.7	Non-Functional Requirements	 PAGEREF _Toc157846031 \h 10
4	Processing required in the Messaging Stage of the interface	 PAGEREF _Toc157846032 \h 11
4.1	Scope	 PAGEREF _Toc157846033 \h 11
4.2	Data Validation	 PAGEREF _Toc157846034 \h 11
4.3	Filtering	 PAGEREF _Toc157846035 \h 11
4.4	Mapping	 PAGEREF _Toc157846036 \h 11
4.5	Target Message Schema	 PAGEREF _Toc157846037 \h 11
4.6	Message Transport Details	 PAGEREF _Toc157846038 \h 12
4.7	Naming and Configuration	 PAGEREF _Toc157846039 \h 14
4.8	Environment and Security Context	 PAGEREF _Toc157846040 \h 14
4.9	Non-Functional Requirements	 PAGEREF _Toc157846041 \h 14
5	Processing required in the <third stage of the interface>	 PAGEREF _Toc157846042 \h 15
5.1	Scope	 PAGEREF _Toc157846043 \h 15
5.2	Data Validation	 PAGEREF _Toc157846044 \h 15
5.3	Filtering	 PAGEREF _Toc157846045 \h 15
5.4	Mapping	 PAGEREF _Toc157846046 \h 15
5.5	Target Message Schema	 PAGEREF _Toc157846047 \h 15
5.6	Message Transport Details	 PAGEREF _Toc157846048 \h 15
5.7	Naming and Configuration	 PAGEREF _Toc157846049 \h 15
5.8	Environment and Security Context	 PAGEREF _Toc157846050 \h 15
5.9	Non-Functional Requirements	 PAGEREF _Toc157846051 \h 15
6	Testing Deliverables	 PAGEREF _Toc157846052 \h 16
7	Deployment	 PAGEREF _Toc157846053 \h 17
8	Assumptions and Outstanding Issues	 PAGEREF _Toc157846054 \h 18
8.1	Assumptions	 PAGEREF _Toc157846055 \h 18
8.2	Outstanding Issues	 PAGEREF _Toc157846056 \h 18
Appendix A Volumes	 PAGEREF _Toc157846057 \h 19
Appendix B Glossary	 PAGEREF _Toc157846058 \h 20
Appendix C Document Control	 PAGEREF _Toc157846059 \h 21

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

The interface is meant to run nightly at a pre-configured time 5 days a week (Tuesday to Saturday), which on completion is expected to upload the Product data in a Product Holding Table in IKB.

The interface will make use of the audit and traceability components that are being developed as part of the Operational Framework stream. Developers should put a ‘placeholder’ in their code / configurations as appropriate. 
Architecture
 EMBED Visio.Drawing.11  


Requirements for the End-to-End Interface

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
N/A - No scalability issues exist. 
Operational Support Requirements
No such requirement has been agreed upon at the time of writing this document. However, it is perceived that there would be interface support requirements after go-live date that would require an evaluation.
Likelihood of Change Requirements
There is no such requirement
Cultural/Global Consideration Requirements
N/A 
Legal Requirements
N/A
Compliance To Standards Requirements
No compliance exceptions.
Processing required in an Extract-Stage of the interface
Scope

SSIS extracts the product reference data from IDS using Common Forms, nightly at predefined time, 5 days a week.  In turn, the data is inserted into an Intermediate table at IKB which is the Product Holding Table. 
Source Message Schema
There is no source message as such. The source data resides in the form of RDBMS tables. The data is extracted via Product Common form. 

Sample Message Format
The source data flows from IDS via SSIS using Product Common Form. Sample message is not required.
 
Message Transport Details

Feature
Specification
Additional Information
Source System Name
IDS

Source Platform / OS
SQL SERVER 2005

Source Physical Location


Source Underlying Data Storage Technology
RDBMS

Target System Name
SSIS

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
File Drop(Windows) 	
                 (XCOM) 	
SSIS       		

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
Logging should occur, such that the message can be recreated if necessary. Should be based upon the Operational Model ( IMOF).

Error Handling
Not yet decided 

Processing should prevent sending of duplicate messages, unless this occurs during recovery from failure.


Naming and Configuration

SSIS
Package Name: 

Name

<Placeholder for other package components/steps>


<Placeholder for other package components/steps>



Environment and Security Context
Account details will be included here once we have visibility of the environments. 

Non-Functional Requirements
Not Applicable


Processing required in the Messaging Stage of the interface
Scope
SSIS will pickup the data from IDS, transforms the source data into target specification and stored in the holding table of IKB.
Data Validation
Data Validation will be done by the target IKB system.
Filtering
There is no filtering requirement.
Mapping
Mapping document will be provided subsequently.
Target Message Schema
File Field NameTypeLengthHolding Table Field NameIKB Product Table FieldNotes / TransformationsDateTimedatetimeDateTimeThis field will be populated with the current date/time that records are added. This will be done as part of the process that adds data to this table. This field will be used to sort the records to ensure that they are processed in the correct order.Productvarchar32NameNameProduct NameEAN Codevarchar13EAN_CodeUPCEAN/UPC CodeTPN Codevarchar7TPN_CodeIDTesco Product NumberDepartmentvarchar30DepartmentCategoryDepartment NumberDisplay Groupvarchar30Display_GroupSubcategoryManufacturervarchar30ManufacturerManufacturerManufacturer NameSuppliervarchar40SupplierSupplierSupplier NameCase Pack Sizeint4Case_Pack_SizeCaseTotal NumberHeightreal6HeightHeightHeight of ProductWidthreal6WidthWidthWidth of ProductDepthreal6DepthDepthDepth of the ProductTray Heightreal6Tray_HeightTray HeightTray Height of the ProductTray Widthreal6Tray_WidthTray WidthTray Width of the ProductTray Depthreal6Tray_DepthTray DepthTray Depth of the ProductTray Pack Sizereal4Tray_Pack_SizeTray Total NumberTray Total NumberColourreal30ColourDesc 1Color of the ProductProduct launch datedatetime8Product_launch_dateDesc 2Product end datedatetime8Product_end_datedbDateEffectiveToSEL typevarchar30SEL_typeDesc 4Shelf Edge Label TypeGood, better or bestvarchar30Good_better_bestDesc 5Product Characteristics as Good Better or BestWarehouse indicatorvarchar30Warehouse_indicatorDesc 6Indicator , whether the product will be available at warehouse or at store.Commercial unit heightfloat7Future_unit_heightValue 20Used for any product height change.Commercial unit widthfloat7Future_unit_widthValue 21Used for any product width change.Commercial unit depthfloat7Future_unit_depthValue 22Used for any product depth change.Commercial tray heightfloat7Future_tray_heightValue 23Used for any product tray height change.Commercial tray widthfloat7Future_tray_widthValue 24Used for any product tray width change.Commercial tray depthfloat7Future_tray_depthValue 25Used for any product tray depth change.Dummy productintDummy_productFlag 1Indicator to Indicate whether a Product is a dummy Product or Authorized.AuthorisedintAuthorisedFlag 2Indicator to Indicate whether a Product is a dummy Product or Authorized.Diamond lineintDiamond_lineFlag 3UpmarketintUpmarketFlag 4FinestintFinestFlag 5ValueintValueFlag 6Future dimension presentintFuture_dimension_presentFlag 8Price7PriceValue 1Case Cost7Case_costValue 2Unit Cost7Unit_costValue 3Subclass Code30Subclass_codeDesc 8Subclass Desc30Subclass_descDesc 14Traypack indicator30Traypack_indicatorDesc 9Seasonal30SeasonalDesc 10Phasing30PhasingDesc 11Brand30BrandBrandBuyer30BuyerDesc 12
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
File System

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
Instruction Name: 
Instruction Details
Description
To be determined
Enabled
True
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

Timeout

Require Data Send

Exception Management
Treat Fatal Adapter Exception As

Treat Unhandled Exceptions As



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
Unit Test Scripts and test cases are kept at the following location <location>Deployment
Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1
Source of Tray Dimensions Data is not yet confirmed. The default value is set to “1” until it is confirmed from SRD.
2
Data type and length of fields of destination table Product Holding Table are based on ix_spc_product table.

Outstanding Issues
ID
Issue
To be addressed by
1
Need to have a clear understanding of how the common form works

2
Product Holding Table generation script to be provided by JDA. Using dummy product holding table (name, datatypes and size based on ix_spc_product_table) may result in rework if there are significant changes when final script issued from JDA



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

Document Control
Change Record

Author
Date
Version
Change Reference, description
Nitin Singhai
18-Jan-2006
0.1D
Draft















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



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT 20 of  NUMPAGES 21	Date:  SAVEDATE \@ "d MMM yyyy" 12 Feb 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture





























































