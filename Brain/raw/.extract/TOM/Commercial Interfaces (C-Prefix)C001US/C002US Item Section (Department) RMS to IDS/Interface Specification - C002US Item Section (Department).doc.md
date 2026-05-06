












TOM Commercial

Interface Specification C002US
Section details from RMS to the Integration Layer










Project BEN Code:

Author: AUTHOR  \* MERGEFORMAT James FullartonDate:
 DOCPROPERTY "Doc Issue Date"  \* MERGEFORMAT 01-Dec-2006 
Version:
 DOCPROPERTY "Doc Version"  \* MERGEFORMAT 0.2 
Status:
 DOCPROPERTY "Doc Status"  \* MERGEFORMAT Draft 

Table of Contents
 TOC \o "1-3" \t "Appendix,1" 1	Introduction	 PAGEREF _Toc155510211 \h 3
1.1	Purpose of Document	 PAGEREF _Toc155510212 \h 3
1.2	Background	 PAGEREF _Toc155510213 \h 3
1.3	Scope	 PAGEREF _Toc155510214 \h 3
2	Description and Requirements for the End-to-End Interface	 PAGEREF _Toc155510215 \h 4
2.1	Description of the End-to-End Interface	 PAGEREF _Toc155510216 \h 4
2.2	Requirements for the End-to-End Interface	 PAGEREF _Toc155510217 \h 4
3	Processing Required from RMS	 PAGEREF _Toc155510218 \h 6
3.1	Scope	 PAGEREF _Toc155510219 \h 6
3.2	Source Message Schema	 PAGEREF _Toc155510220 \h 6
3.3	Message Transport Details	 PAGEREF _Toc155510221 \h 6
4	Processing Required in the Integration Layer	 PAGEREF _Toc155510222 \h 8
4.1	Scope	 PAGEREF _Toc155510223 \h 8
4.2	Data Validation	 PAGEREF _Toc155510224 \h 8
4.3	Filtering	 PAGEREF _Toc155510225 \h 8
4.4	Mapping	 PAGEREF _Toc155510226 \h 8
4.5	Target Message Schema	 PAGEREF _Toc155510227 \h 8
4.6	Message Transport Details	 PAGEREF _Toc155510228 \h 8
5	Assumptions and Outstanding Issues	 PAGEREF _Toc155510229 \h 9
5.1	Assumptions	 PAGEREF _Toc155510230 \h 9
5.2	Outstanding Issues	 PAGEREF _Toc155510231 \h 9
Appendix A Volumes	 PAGEREF _Toc155510232 \h 10
Appendix B Glossary	 PAGEREF _Toc155510233 \h 11
Appendix C Document Control	 PAGEREF _Toc155510234 \h 12

Introduction
Purpose of Document
The purpose of this document is to describe the development required to achieve this interface, in each system that plays a part, including schemas and mappings.

Background
The purpose of the interface is to receive department merchandise hierarchy details from Oracle Retail Management System (RMS) via the Retail Integration Bus (RIB). These messages will be mapped to the Tesco common form and copied to the Integration Data Store (IDS). A Section is known in RMS as a Department.
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
This interface is the transmission of section (department) merchandise hierarchy details from RMS to the integration layer.

Requirements for the End-to-End Interface

Audit Requirements
Please provide details of any specific audit trail or audit processing, e.g. headers and trailers, audit reports etc. Note that finance interfaces must have an audit trail:
TBC
Security Requirements
Please provide details of any specific security requirements:
TBC
Timing/cutoff Constraints
Please provide details of any specific timing or cutoff constraints, e.g. that an interface must be received by 1am:
TBC
Performance Requirements
Provide details of any particular performance requirement:
TBC
Reliability and Availability Requirements
Provide details of any particular reliability or availability requirements over and above the normal level of service provided:
TBC
Scalability Requirements
Please provide specific details of any expected increase in the volume/frequency of data that must be accounted for. Include timescales:
TBC	

Operational Support Requirements
Please provide details of any particular operational support requirements over and above the normal level of service provided:
TBC
Likelihood of Change Requirements
If it is know that the specification of the interface is subject to change, please provide details of this requirement:
As this is an iterative approach these requirements will change as and when they are refined
Cultural/Global Consideration Requirements
If there are any specific cultural or global considerations that need to be taken into account in the integrating of any systems mentioned in this document, then please provide details here:
This interface will initially be used in the US
Legal Requirements
Please provide details of any Specific legal requirements, and include the country whose law will apply:
TBC
Compliance To Standards Requirements
Please provide details of any specific standards that apply, and provide links to where copies of relevant national and international standards can be located:
The interface will be part of The Operating Model and as such must adhere to the standards used for Tesco integration
Processing Required from RMS
Scope
The message will be produced by the Oracle Retail Management System and published on the Retail Integration Bus (RIB) using Java Messaging Service (JMS). The messages will take one of two forms, MrchHrDeptRef or MrchHrDeptDesc. MrchHrDeptRef is created when a department is deleted and MrchHrDeptDesc is generated on insert or update. The messages will belong to groups, known as families in JMS. The RIB message type will specify the operation performed and are as follows:
Deptcre – Creation
Deptmod - Update
Deptdel - Deletion

The message generated is published to the RIB which can have multiple subscribers; one of these subscribers will be this interface.

Source Message Schema
The message is uniquely identified by the RIB Message ID. The message can either be of the form MrchHrDeptRef or MrchHrDeptDesc. Both message formats are XML and the schemas can be found in .\MrchHrDeptDesc.xsd and .\MrchHrDeptRef.xsd.

Message Transport Details
Feature
Specification
Additional Information
Source System Name
RMS

Source Platform / OS
Oracle Retail

Source Physical Location
TBC

Source Underlying Data Storage Technology
Oracle

Target System Name
Integration Data Store

Target Platform / OS
BizTalk

Target Physical Location
TBC

Target Underlying Data Storage Technology
SQL Server

Transfer Function
Indicate which method will be used to transfer data to the next stage.
HTTP (Put/Post) 
HTTPS (Put/Post) 
Message Queue 
FTP 
File Drop (Windows) 
                 (XCOM) 
JMS 

Data Format
Indicate the physical format of the message encapsulating the data.
XML  
Delimited 
Positional 

Decryption/Encryption
Is the data encrypted? If so, does it need to be decrypted?
TBC

Decompression/Compression
Is the data compressed? If so does it need to be decompressed?
TBC

Transmission Mode
Synchronous transfers will receive confirmation of completion of the message delivery to final destination. Asynchronous transfers receive confirmation of message reception by the integration layer. Bulk transfers do not have a return message path.

Synchronous 
Asynchronous 
Bulk Data 

Real-time/Scheduled Batch
Is the data sent one change at a time, as the change occurs using real-time messaging? Or are changes communicated on a time schedule using a batch method
Provide scheduling details eg. Time, CA7 dependencies,etc.
Real Time

Archiving
Is there a requirement to store the being transformed? Incoming or outgoing data?  All data or a specific subset? For how long should the data be stored?
TBC – handled by framework if necessary

Logging
Should logs be kept of all actions? For how long should these be stored?
TBC – handled by framework if necessary

Error Handling
Specify what processing is required if an error occurs while transferring the data. Is retry required? How many times, with what interval? Is alerting required? Specify handling of duplicate messages.
TBC – handled by framework if necessary



Processing Required in the Integration Layer
Scope
When the department details are received by the integration layer, these details will be mapped to the Tesco common form and stored in the integration data store.
Data Validation
The Integration Layer will check that the data conforms to the input schema, and can be mapped to the common form schema. This will be type & format (syntax) validation, not semantic (meaning) validation.

Source Data Item
Validation
TBC



Filtering
Source Schema, Column to Filter
Possible Values
Rows with these values pass through
Rows with these values are discarded
TBC – None?








Mapping
Source Data Item
Target Data Item
Comments
dept
Section

group_no
Department

dept_name
SectionName





Target Message Schema
The common form schema for Items can be found in .\Section.xsd.
Message Transport Details 
For messages destined for the integration layer, the transport details can be found in 3.6.

 
 Assumptions and Outstanding Issues
Assumptions
ID
Assumption
1




Outstanding Issues
ID
Issue
To be addressed by
1
Unknown Requirements – Anything highlighted in Red
Nikhil Rajwade



Volumes
TBC
Glossary
Acronym
Term
Description
IDS
Integration Data Store
The data store in the integration layer
JMS
Java Messaging Service
The messaging protocol used by Oracle Retail applications
RIB
Retail Integration Bus
Creation of a strategic single view of data across the enterprise.
RMS
Retail Management System
Oracle Retail Management System application

Interface
Many definitions exist for 'interface'. In general, 'interface' refers to the link between a data source and a data target. And there are properties of the interface in this context. However more specifically 'interface' refers to one end of a data link, hence the terms source interface and target interface, and both the source interface and the target interface will have specific properties of their own.




Document Control
Change Record

Author
Date
Version
Change Reference, description
James Fullarton
01 Dec 2006
V0.1 Draft
First issue
James Fullarton
20 Dec 2006
V0.2 Draft
Updated details










Version
Section
Unknown Requirements
V0.1 Draft
2.2
Requirements for the End to End Interface table
3.3
Encryption, Compression, Auditing, Logging, Security, Error Handling, Source Physical Location, Target Physical Location
4.2
Data Validation
4.3
Filtering
Appendix A
Data Volumes
Appendix C
Related Documents
V0.2 Draft
As V0.1





















Related Documents

Author
Date
Version
Title



Add Pattern, TSD & solutions architecture













Distribution

Name
Position
Approver/Contributor/Other





























Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture



Version  REF DOC_VER 0.1, Issue  REF DOC_STATUS Draft	Page:  PAGE  \* MERGEFORMAT ii of  NUMPAGES 12	Date:  SAVEDATE \@ "d MMM yyyy" 2 Jan 2007

Tesco IT Group Technology and Architecture	 TITLE  \* MERGEFORMAT Architecture































































