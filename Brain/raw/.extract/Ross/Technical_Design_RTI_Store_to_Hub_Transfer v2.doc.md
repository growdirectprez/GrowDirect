

TECHNICAL DESIGN FOR
FILE TRANSFER REPLACEMENT PROJECT



STORE TO CORPORATE INTEGRATION HUB
Version 002




Contents
 TOC \o "1-3" \h \z \u  HYPERLINK \L "_TOC294195993" 1	Document Review & Sign-off	 PAGEREF _TOC294195993 \H 3
 HYPERLINK \L "_TOC294195994" 1.1	Document Properties	 PAGEREF _TOC294195994 \H 3
 HYPERLINK \L "_TOC294195995" 1.2	Revision History	 PAGEREF _TOC294195995 \H 3
 HYPERLINK \L "_TOC294195996" 1.3	Document Approvers	 PAGEREF _TOC294195996 \H 3
 HYPERLINK \L "_TOC294195997" 1.4	Supporting Documents	 PAGEREF _TOC294195997 \H 3
 HYPERLINK \L "_TOC294195998" 2	Introduction	 PAGEREF _TOC294195998 \H 4
 HYPERLINK \L "_TOC294195999" 2.1	Purpose	 PAGEREF _TOC294195999 \H 4
 HYPERLINK \L "_TOC294196000" 2.2	Responsibility for this Document	 PAGEREF _TOC294196000 \H 4
 HYPERLINK \L "_TOC294196001" 2.3	Document Scope	 PAGEREF _TOC294196001 \H 4
 HYPERLINK \L "_TOC294196002" 2.4	Audience	 PAGEREF _TOC294196002 \H 4
 HYPERLINK \L "_TOC294196003" 3	Overview	 PAGEREF _TOC294196003 \H 5
 HYPERLINK \L "_TOC294196004" 3.1	Business and Technical Overview	 PAGEREF _TOC294196004 \H 5
 HYPERLINK \L "_TOC294196005" 4	Design	 PAGEREF _TOC294196005 \H 6
 HYPERLINK \L "_TOC294196006" 4.1	Interface/Service Pattern	 PAGEREF _TOC294196006 \H 6
 HYPERLINK \L "_TOC294196007" 4.2	Sequence Diagram	 PAGEREF _TOC294196007 \H 6
 HYPERLINK \L "_TOC294196008" 4.3	RTI Components	 PAGEREF _TOC294196008 \H 7
 HYPERLINK \l "_Toc294196009" 4.3.1	RTI Instructions	 PAGEREF _Toc294196009 \h 7
 HYPERLINK \L "_TOC294196010" 5	Operations	 PAGEREF _TOC294196010 \H 8
 HYPERLINK \L "_TOC294196011" 5.1	Restart/Recover conditions	 PAGEREF _TOC294196011 \H 8
 HYPERLINK \L "_TOC294196012" 6	Assumptions	 PAGEREF _TOC294196012 \H 8
DOCUMENT REVIEW & SIGN-OFF
 Document Properties
AUTHOR
CREATION DATE
LAST UPDATED
VERSION
Geoff Lyle
05/04/2011
05/25/2011
001
Revision History
VER.
DATE
DESCRIPTION
AUTHOR
001
05/04/2011
Initial Draft
Geoff Lyle
002
05/25/2011
Updates
Geoff Lyle
 Document Approvers
NAME
ROLE
SIGNATURE
SIGN-OFF DATE
Jeremy Sena
SysRepublic


Geoff Lyle
SysRepublic


Ned Bilkic
SOA Solution Architect


Soeren Ahrens
SOA Program Lead


Abhi Srivastava
SOA PD Lead



Supporting Documents 

DOCUMENT TITLE
DOCUMENT TYPE
AUTHOR
DATE
LOCATION
Technical_Design_Ross_File_Transfer_Solution_Overview_v2
Technical Design
Geoff Lyle
5/5/2011

INTRODUCTION
Purpose
The purpose of this document is to define the essential characteristics of Store to RTI Corporate Integration Hub transfers. The document will identify the communication internal to RTI and define the flow of data between the Store ISP and the Hub.  Ross application and Store Systems teams are expected to reach a mutual agreement on the interface design prior to technical design.
Responsibility for this Document
Sysrepublic will own this document and subsequently is responsible for updates and versioning.  All changes and additions are subject to review prior to sign off.
Document Scope
This document will cover, at a detailed level, the design as described by the functional requirements for communication between Store Systems and ROSS systems integration. The document details the solution design and features the Integration components to be used for Stores to interface with the Corporate Integration Hub.  The document will also feature the common exception handling service for the RTI processes which manage the transfer of files between the two environments.

This document is intended to provide the technical design pattern for all Stores to Hub transfers.  Specific interface configuration sheets will detail the requirements for each individual file transfer.

The Sysrepublic team would use this document in the subsequent phases to build the integration components.
Audience
This document is intended for persons who seek to understand the high level agreement between the RTI component development team and consumers of the data which passes between of the RTI Corporate Integration Hub and RTI Agents installed on the Store ISP.  The audience includes:

•	Project Managers
•	Functional Analysts
•	Application Architects
•	Software Developers
•	Testing Analysts
•	Production Support Personnel
OVERVIEW
Business and Technical Overview 
The purpose of this document is to provide a design pattern for any Store Initiated transfer to back to corporate systems.  This process defines how the store will push files to the Integration hub.  This document does not cover the process which moves a file form the Hub to the destination System.   This document does not make any assumptions as to the 'business objective or purpose' of the files being transferred, this information will form part of the end to end design of the business application utilizing this file transfer solution.

The pattern described here will enable a repeatable mechanism to push files to the integration Hub via an https stream which moves the file(s) from the store ISP to a storage location on the Hub.
 
The pattern will cater for the following transmission options
Scheduled Pre Process rules to initiate the transfer
Event based monitoring to initiate transfers
Flexible file renaming 
Compression
Encrypted https streaming between systems 

The pattern described in this document will either be scheduled; with each store to hub transfer configured using a preprocessing rule to define the contextual information for the transfer.  A generic DDS adapter will be sued to execute the store hub transfer once the prerequisites of the initiating rue lave been met.

Each file or archive can be regarded as a 'transmission' from store to hub. Each transmission will be logged for audit purposes and alerting will be implemented to highlight non-transmission of data.

The file transfer solution will be built using the Sysrepublic RTI technology platform. RTI will provide the data movement and logging engine for all transmissions. For more information on RTI please see the 'RTI Help' documentation.

The following set example interfaces will be supported by the Pattern described in this Document:

PCI Security
EDW Store Data
RMS Store Data
Zip Code Survey





DESIGN
Interface/Service Pattern
Service would follow point to point pattern and frequency of file transfers will be scheduled.
Sequence Diagram
Normal Flow Sequence Diagram



Normal Sequence Diagram Walkthrough
Normal Sequence #
Event
Component Invoked
Output
Alternate flow sequence#
1a.



At a scheduled time a Hosted Instruction on the RTI Store Agent will run a preprocessing rule to initiate a store to hub transfer 

StorePreProcessingRule(n)
Pre Process completed

1b.
Pass contextual details of the transmission to an unhosted send instruction on the store agent
StorePreProcessingRule(n)
Unhosted instruction invoked

1c.
On fail write to ISP event log
StorePreProcessingRule(n)
Error logged to event log

2a
File adapter gets file from source directory

Store to Hub Transfer
Call transform step

2b
Transform step internal to the instruction Compresses file(s)
Store to Hub Transfer
Call destination step

2c.

Https stream to Hub is initiated

Store to Hub Transfer
Https stream

2d.
Write success of fail to the ISP event log using the event log adapter in RTI
Store to Hub Transfer
Event added to log

2e.
Retry after fail
Store to Hub Transfer
Initiate unhosted send


RTI Components 
RTI Instructions	
The following RTI instruction templates will be required for the Hub to Store Service:
Instruction Name
Type
Details
StorePreProcessRule(n)
Scheduled
Scheduled instruction runs a pre process to define contextual information and execute any pre processing before initiating a new transfer
StoretoHubTransfer
Unhosted Receive
UnHosted Instruction to Push files to DSS when initiated by a preprocessing rule

OPERATIONS
Restart/Recover conditions
FAILURE POINTDESCRIPTIONRESUBMIT FUNCTIONALITYPROCESS TYPEGUIDING PRINCIPLESUPPORT PROCEDUREFREQUENCYStorePreProcess
Rule(n)
Fails to Complete Preprocess
None
N/A
Store Issue
?
Low
StoretoHub
Transfer
Fails to complete https stream
Error occurs and Retry / restart transmission
Https / Transfer
Infrastructure Issue
?
Low



ASSUMPTIONS
ID
DESCRIPTION
1
StorePostProcessingRule(n)RTI instruction is a variable component the specific instructions required will be determined by the details interface configuration sheets
2
Processing errors which occur at the store will be written to the Store’s ISP event application log
3
RTI is able to retry am unhosted instruction by the having the instruction invoke itself, may require a preprocessing step if not able to configure as diagramed
4










STORE TO CORPORATE INTEGRATION HUB	                                                                    VERSION 001                                      
  
               

PAGE  


	                                                                                                                                                 

STORE TO CORPORATE INTEGRATION HUB		Page  PAGE 3 of  NUMPAGES 8    


 SHAPE  \* MERGEFORMAT 	                                                                                                SHAPE  \* MERGEFORMAT 
©2007 Accenture. All Rights Reserved.	 PAGE 1                                 DATE \@ "M/d/yyyy" 5/26/2011




