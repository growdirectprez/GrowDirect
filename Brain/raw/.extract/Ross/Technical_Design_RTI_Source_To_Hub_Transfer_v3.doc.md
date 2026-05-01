

TECHNICAL DESIGN FOR
FILE TRANSFER REPLACEMENT PROJECT



CORPORATE SOURCE TO CORPORATE INTEGRATION HUB 
Version 003




Contents
 TOC \o "1-3" \h \z \u  HYPERLINK \L "_TOC292362656" 1	Document Review & Sign-off	 PAGEREF _TOC292362656 \H 3
 HYPERLINK \L "_TOC292362657" 1.1	Document Properties	 PAGEREF _TOC292362657 \H 3
 HYPERLINK \L "_TOC292362658" 1.2	Revision History	 PAGEREF _TOC292362658 \H 3
 HYPERLINK \L "_TOC292362659" 1.3	Document Approvers	 PAGEREF _TOC292362659 \H 3
 HYPERLINK \L "_TOC292362660" 1.4	Supporting Documents	 PAGEREF _TOC292362660 \H 3
 HYPERLINK \L "_TOC292362661" 2	Introduction	 PAGEREF _TOC292362661 \H 4
 HYPERLINK \L "_TOC292362662" 2.1	Purpose	 PAGEREF _TOC292362662 \H 4
 HYPERLINK \L "_TOC292362663" 2.2	Responsibility for this Document	 PAGEREF _TOC292362663 \H 4
 HYPERLINK \L "_TOC292362664" 2.3	Document Scope	 PAGEREF _TOC292362664 \H 4
 HYPERLINK \L "_TOC292362665" 2.4	Audience	 PAGEREF _TOC292362665 \H 4
 HYPERLINK \L "_TOC292362666" 3	Overview	 PAGEREF _TOC292362666 \H 5
 HYPERLINK \L "_TOC292362667" 3.1	Business and Technical Overview	 PAGEREF _TOC292362667 \H 5
 HYPERLINK \L "_TOC292362668" 4	Design	 PAGEREF _TOC292362668 \H 6
 HYPERLINK \L "_TOC292362669" 4.1	Interface/Service Pattern	 PAGEREF _TOC292362669 \H 6
 HYPERLINK \L "_TOC292362670" 4.2	Sequence Diagram	 PAGEREF _TOC292362670 \H 6
 HYPERLINK \L "_TOC292362671" 4.3	RTI Components	 PAGEREF _TOC292362671 \H 8
 HYPERLINK \l "_Toc292362672" 4.3.1	RTI Web Services	 PAGEREF _Toc292362672 \h 8
 HYPERLINK \l "_Toc292362673" 4.3.2	RTI Instructions	 PAGEREF _Toc292362673 \h 8
 HYPERLINK \L "_TOC292362674" 5	Operations	 PAGEREF _TOC292362674 \H 9
 HYPERLINK \L "_TOC292362675" 5.1	Restart/Recover conditions	 PAGEREF _TOC292362675 \H 9
 HYPERLINK \L "_TOC292362676" 6	Infrastructure considerations	 PAGEREF _TOC292362676 \H 9
 HYPERLINK \L "_TOC292362677" 7	Tokens	 PAGEREF _TOC292362677 \H 9
 HYPERLINK \L "_TOC292362678" 8	Special Unit Test Conditions	 PAGEREF _TOC292362678 \H 9
 HYPERLINK \L "_TOC292362679" 9	Assumptions	 PAGEREF _TOC292362679 \H 9
DOCUMENT REVIEW & SIGN-OFF
 Document Properties
AUTHOR
CREATION DATE
LAST UPDATED
VERSION
Geoff Lyle
04/29/2011
05/20/2011
003
Revision History
VER.
DATE
DESCRIPTION
AUTHOR
001
04/29/2011
Initial Draft
Geoff Lyle
002
05/05/2011
Updated after initial review
Geoff Lyle
003
05/20/2011
Sequence Diagram Update
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
The purpose of this document is to define the essential characteristics of the RTI Corporate source to hub file transfers initiated by the BPEL_InvokeStoreRTIWS_sCA. The document will identify the communication internal to RTI and define the flow of data between the SOA, RTI, Corporate Source systems and the Corporate Integration Hub.  Ross application and SOA teams are expected to reach a mutual agreement on the interface design prior to technical design.
Responsibility for this Document
Sysrepublic will own this document and subsequently is responsible for updates and versioning.  All changes and additions are subject to review prior to sign off.
Document Scope
This document will cover, at a detailed level, the design as described by the functional requirements for communication between ROSS systems integration and application. The document details the solution design and features the Integration components to be used for interfacing with the end applications. The document will also feature the common exception handling service for the RTI processes.

This document is intended to provide the technical design pattern for all RTI Corporate Source to Hub file transfers.  Specific inetrface configuration sheets will detail the specifcs of a particular file transfer.  This document will cover all manner of interface characteristics but should not exceed beyond the scope of defining the handshake for the interface.

The Sysrepublic team would use this document in the subsequent phases to build the integration components.
Audience
This document is intended for persons who seek to understand the high level agreement between the service development team and the consumer of the BPEL_InvokeStoreRTIWS_sCA interface.  The audience includes:
Project Managers
Functional Analysts
Application Architects
Software Developers
Testing Analysts
Production Support Personnel
OVERVIEW
Business and Technical Overview 
The purpose of this document is to provide a design pattern for any corporate hub to store file transfer requirement that requires a single file be delivered to all of the current stores in the Ross estate, or a store specific file be delivered to each store in the Ross estate.   This document does not make any assumptions as to the 'business objective or purpose' of the files being transferred, this information will form part of the end to end design of the business application utilizing this file transfer solution.

The pattern described here will enable a repeatable mechanism to invoke the transfer a file or set of files from a central corporate system location to the Corporate Integration Hub via web service call from SOA.

The pattern will cater for the following transmission options
SOA invocation
Flexible destination selection
Flexible file renaming 
Compression
Creation and explosion of ZIP archives for recursive directory requirements

The pattern will be invoked from the enterprise scheduler via the BPEL pattern described in detail in the document, ‘Techncial_Design_ BPEL_InvokeStoreRTIWS_sCA_Sync’.

Each file or set of files can be regarded as a 'transmission' from hub to store. Each transmission will be logged for audit purposes and alerting will be implemented to highlight non-transmission of data.

The file transfer solution will be built using the Sysrepublic RTI technology platform. RTI will provide the data movement and logging engine for all transmissions. For more information on RTI please see the 'RTI Help' documentation.

The following example interface types will be supported by the Pattern described in this Document:

Bin File
The Source - Update
Weekly Item File
Weekly Price File
Foreign Exchange
Store List





DESIGN
Interface/Service Pattern
Service would follow point to point pattern and frequency of file transfers will be scheduled/ondemand.
Sequence Diagram
Normal Flow Sequence Diagram



Normal Sequence Diagram Walkthrough
Normal Sequence #
Event
Component Invoked
Output
Alternate flow sequence#
1.



BPEL Calls RTI webservice pass XML payload:  
InvokeRTIFileTransferRequestMessage 

BPELsubcribe
RTIWS
RTI
instantiated.

2.
BPEL waits for RTI callback (success / failure)


A1
3.
BPELsubcribeRTIWS Web service calls unhosted RTI instruction

CorpTransfer
ReceiveRTI
CorpTransfer
ReceiveRTI Initiated
A1
4a.
MSMQ adapter writes transmission message to MSMQ
CorpTransfer
ReceiveRTI
Message added to StoreTransferMSMQ
A2
4b.
Callback SOA with Success Fail of the message receipt
InvokeStoreRTIWS BPEL
Webservice Callback
A1
5.
Validate message input to queue

StoreTransferMSMQ
None
A2
6a.

Scheduled RTI Instruction reads StoreTransferMSMQ looking for new transmission events:


CorpTransfer
RouterRTI
Property Bag Adpater
A2
6b.
RTI transform:  Property Bag adapter adds message attributes from: 
InvokeRTIFileTransferRequestMessage to Transmission Property Bag 

RTI evaluates Property Bag to determine Pattern Instruction to invoke
CorpTransfer
RouterRTI:
Property Bag Adpater
Call Pattern Specific Unhosted Receive 
A2
7a.
Unhosted receive initiates SFTP transfer from Source System.
  

SourceToHub
Pattern(n)RTI
Call SFTP adapter
A2
7b.
RTI SFTP adapter gets source system, server name, filepath and file details from Property Bag 
SourceToHub
Pattern(n)RTI
RTI connect to SFTP Server

A2
7c.
RTI Transfrom compress file
SourceToHub
Pattern(n)RTI
File Compress
A2
7d.
SFTP  get file(s); move from source to Hub
SourceToHub
Pattern(n)RTI
SFTP Transfer
A2
8a
Unhosted send received by DDS Adapter when transfer to Hub complete
CorpInsert
DDSDatabase
Call DDS Adapter 
A2
8b.
Insert transmission to DDS Database
CorpInsert
DDSDatabase
On complete Step
A2
9a.
DDS Alert rule monitors DDS for success / fail conditons
MonitorDDS
DatabaseRule(n)
Message to SOA
A2
9b.
Success callback to SOA
BPELpublish
RTIWS
complete
None



Alternate Walkthrough
Alternate Sequence #
Output/Action for alternate flow
A1
BPEL will error out and BPEL ErrorLogger will be invoked. Send the Failure to CA
A2
RTI failure will call back error event to BPEL via BPELpublish
RTIWS

RTI Components 
RTI Web Services 
 
WEB Service Name
URL
DETAILS
BPELsubcribeRTIWS
XX
Incoming SOA invocation service
BPELpublishRTIWS
XX
Outbound SOA callback service

RTI Instructions	
The following RTI instruction templates will be required for the Source to Hub Service:
Instruction Name
Type
Details
CorpTransfer
ReceiveRTI
UnHosted Receive
Unhosted instruction receives XML payload from web service and inserts to MSMQ on DB Server
CorpTransfer
RouterRTI
Scheduled
Scheduled instruction read from MSMQ and routes message to the appropriate transfer pattern

SourceToHub
Pattern(n)RTI
Unhosted Receive
Unhosted instruction designed to interpret the contextual information of each transmission and perform the steps required to pull the file form a source system and move to hub
CorpInsert
DDSDatabase
UnHosted Send
DDS Adapter which inserts new messages to the DDS database and provides the event which Store agents will poll for to initiate the file pull to store
MonitorDDS
DatabaseRule(n)
Scheduled
DDS Apadter configured to monitor for the Hub alerting requirments of a specific interface

OPERATIONS
Restart/Recover conditions
FAILURE POINTDESCRIPTIONRESUBMIT FUNCTIONALITYPROCESS TYPEGUIDING PRINCIPLESUPPORT PROCEDUREFREQUENCYRTI Webservice
Fails to connect to Corporate Agent
Error occurs and callback SOA
N/A
Infrastructure Issue
?
Low
RTI MSMQ Adapter
RTI fails insert to MSMQ
Error occurs and callback SOA
Add to Queue
Infrastructure Issue
?
Low
RTI SFTP Adapter
Fail to connect to SFTP
Error occurs and callback SOA
SFTP Transfer
Infrastructure Issue
?
Low
RTI DSS Adapter
Failure to connect to DB
Retry and Error occurs and callback SOA
DB Connect
Infrastructure Issue
?
Low







ASSUMPTIONS
ID
DESCRIPTION
1
All the attributes defined in the message body of the invocation message should be treated as overrides for any default value defined in the RTI file transfer metadata.
2
SourceToHubPattern(n)RTI instruction is a variable component the specific instructions required will b determined by the details interface configuration sheets
3
General Alert and Error handling of events in the DDS database will are included in the Solution Architecture Technical Design









CORPORATE SOURCE TO HUB	                               		                                     VERSION 002                                      
  
               

PAGE  


	                                                                                                                                                 

CORPORATE SOURCE TO HUB		Page  PAGE 3 of  NUMPAGES 9    


 SHAPE  \* MERGEFORMAT 	                                                                                                SHAPE  \* MERGEFORMAT 
©2007 Accenture. All Rights Reserved.	 PAGE 1                                 DATE \@ "M/d/yyyy" 5/26/2011




