---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/Ross/Technical_Design_RTI_Hub_To_Source_Transfer_v2.doc.md
tags: [ross, rti, store-transfer, archive-2011, tech-design]
project: 
status: unprocessed
---

# Technical_Design_RTI_Hub_To_Source_Transfer_v2.doc

## Source
File: `Brain/raw/.extract/Ross/Technical_Design_RTI_Hub_To_Source_Transfer_v2.doc.md`
Size: 12,236 bytes

## Raw content


TECHNICAL DESIGN FOR
FILE TRANSFER REPLACEMENT PROJECT



CORPORATE INTEGRATION HUB
 TO CORPORATE SOURCE
Version 002




Contents
 TOC \o "1-3" \h \z \u  HYPERLINK \L "_TOC294194569" 1	Document Review & Sign-off	 PAGEREF _TOC294194569 \H 3
 HYPERLINK \L "_TOC294194570" Document Properties	 PAGEREF _TOC294194570 \H 3
 HYPERLINK \L "_TOC294194571" Revision History	 PAGEREF _TOC294194571 \H 3
 HYPERLINK \L "_TOC294194572" Document Approvers	 PAGEREF _TOC294194572 \H 3
 HYPERLINK \L "_TOC294194573" Supporting Documents	 PAGEREF _TOC294194573 \H 3
 HYPERLINK \L "_TOC294194574" 2	Introduction	 PAGEREF _TOC294194574 \H 4
 HYPERLINK \L "_TOC294194575" Purpose	 PAGEREF _TOC294194575 \H 4
 HYPERLINK \L "_TOC294194576" Responsibility for this Document	 PAGEREF _TOC294194576 \H 4
 HYPERLINK \L "_TOC294194577" Document Scope	 PAGEREF _TOC294194577 \H 4
 HYPERLINK \L "_TOC294194578" Audience	 PAGEREF _TOC294194578 \H 4
 HYPERLINK \L "_TOC294194579" 3	Overview	 PAGEREF _TOC294194579 \H 5
 HYPERLINK \L "_TOC294194580" Business and Technical Overview	 PAGEREF _TOC294194580 \H 5
 HYPERLINK \L "_TOC294194581" 4	Design	 PAGEREF _TOC294194581 \H 6
 HYPERLINK \L "_TOC294194582" Interface/Service Pattern	 PAGEREF _TOC294194582 \H 6
 HYPERLINK \l "_Toc294194583" 4.1	SOA Invoked Sequence Diagram	 PAGEREF _Toc294194583 \h 6
 HYPERLINK \L "_TOC294194584" Normal Flow Sequence Diagram	 PAGEREF _TOC294194584 \H 6
 HYPERLINK \l "_Toc294194585" 4.2	Event Driven Sequence Diagram	 PAGEREF _Toc294194585 \h 8
 HYPERLINK \l "_Toc294194586" 4.3	RTI Instructions	 PAGEREF _Toc294194586 \h 9
 HYPERLINK \L "_TOC294194587" 5	Operations	 PAGEREF _TOC294194587 \H 10
 HYPERLINK \L "_TOC294194588" Restart/Recover conditions	 PAGEREF _TOC294194588 \H 10
 HYPERLINK \L "_TOC294194589" 6	Assumptions	 PAGEREF _TOC294194589 \H 10
DOCUMENT REVIEW & SIGN-OFF
 Document Properties
AUTHOR
CREATION DATE
LAST UPDATED
VERSION
Geoff Lyle
05/04/2011
05/20/2011
002
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
Upadted
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
The purpose of this document is to define the essential characteristics of the RTI Corporate Integration Hub to Corporate System file transfers initiated by the store to hub transfer process.  The document will identify the communication internal to RTI and define the flow of data between the SOA, RTI, the Corporate Integration Hub and Corporate Source systems.  Ross application and SOA teams are expected to reach a mutual agreement on the interface design prior to technical design.
Responsibility for this Document
Sysrepublic will own this document and subsequently is responsible for updates and versioning.  All changes and additions are subject to review prior to sign off.
Document Scope
This document will cover, at a detailed level, the design as described by the functional requirements for communication between ROSS systems integration and application teams. The document details the solution design and features the Integration components to be used for interfacing with the end applications. The document will also feature the common exception handling service for the RTI processes.

This document is intended to provide the technical design pattern for all Corporate Integration Hub to Corporate sytem file transfers.  Specific inetrface configuration sheets will detail the specifcs of a particular file transfer.  This document will cover all manner of interface characteristics but should not exceed beyond the scope of defining the handshake for the interface.

The Sysrepublic team would use this document in the subsequent phases to build the integration components.
Audience
This document is intended for persons who seek to understand the high level agreement between the RTI component development team and consumers of the data which passes between of the RTI Corporate Integration Hub, Corporate sytems and the SOA integration team.  The audience includes:
Project Managers
Functional Analysts
Application Architects
Software Developers
Testing Analysts
Production Support Personnel
OVERVIEW
Business and Technical Overview
The purpose of this document is to provide a design pattern for any corporate hub to corporate destination transfer requirement that requires files to be delivered from all of the current stores in the Ross estate to a corporate destination by way of the integration hub. This document does not make any assumptions as to the 'business objective or purpose' of the files being transferred, this information will form part of the end to end design of the business application utilizing this file transfer solution.

The pattern described here will enable a repeatable mechanism to invoke the transfer of a file or set of files from the Corporate Integration Hub to a corporate destination via web service call from SOA or event driven rule native to the Hub.

The pattern will cater for the following transmission options
SOA invocation
Event driven invocation
Flexible destination selection
Flexible file renaming
Compression
Creation and explosion of ZIP archives for recursive directory requirements

The patterns described in this document will be invoked from the enterprise scheduler via the BPEL pattern described in detail in the document, ‘Techncial_Design_ BPEL_InvokeStoreRTIWS_sCA_Sync’, or maybe invoked via an event driven schedule native to the Hub.

Each file or set of files can be regarded as a 'transmission' from hub to store. Each transmission will be logged for audit purposes and alerting will be implemented to highlight non-transmission of data.

The file transfer solution will be built using the Sysrepublic RTI technology platform. RTI will provide the data movement and logging engine for all transmissions. For more information on RTI please see the 'RTI Help' documentation.

The following example interface types will be supported by the Pattern described in this Document:

RMS Data from Hub to RMS
EDW Data from Hub to Data warehouse
Zip Code Survey from to Data warehouse






DESIGN
Interface/Service Pattern
Service would follow point to point pattern and frequency of file transfers will be scheduled/ondemand.
SOA Invoked Sequence Diagram
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
6c.
Call unhosted receive instruction to iniate push from Hub to Corporate Sytem


CorpTransfer
RouterRTI
Call to Corp Transfer Instruction
A2
7a.
DDS Subsribe checks for new messages on the Hub
HubtoCorp
Pattern(n)RTI
New DDS event identified

A2
7b.
RTI file adapter writes file from DDS to Hub staging area
HubtoCorp
Pattern(n)RTI
File available to move from Hub
A2
7c.
Call unhosted send instruction to move file from Hub to Destination directory
HubtoCorp
Pattern(n)RTI
SFTP Transfer
A2
8a
Unhosted send initiates SFTP transfer from Hub to Corporate System
HubtoCorp
Transfer
Invoke Transform
A2
8b.
Transform StepUncompress and rename at destination
HubtoCorp
Transfer
File transformed
A2
8c
On success write to Hub event log
HubtoCorp
Transfer
Message to HUB event log
A2
Alternate Walkthrough
Alternate Sequence #
Output/Action for alternate flow
A1
RTI failure will call back error event to BPEL via BPELpublish
RTIWS
A2
Error writes to HUB Event log using RTI event log adapter


Event Driven Sequence Diagram

Normal Flow Sequence Diagram


Normal Sequence Diagram Walkthrough
Normal Sequence #
Event
Component Invoked
Output
Alternate flow sequence#
1a.
Scheduled Instruction checks for new DDS messages on the Hub
HubtoCorp
Pattern(n)RTI
New DDS event identified

A1
1b.
RTI file adapter writes file from DDS to Hub staging area
HubtoCorp
Pattern(n)RTI
File available to move from Hub
A1
1c.
Call unhosted send instruction to move file from Hub to Destination directory
HubtoCorp
Pattern(n)RTI
SFTP Transfer
A1
2a
Unhosted send initiates SFTP transfer from Hub to Corporate System
HubtoCorp
Transfer
Invoke Transform
A1
2b.
Transform StepUncompress and rename at destination
HubtoCorp
Transfer
File transformed
A1
2c
On success write to Hub event log
HubtoCorp
Transfer
Message to HUB event log
A1

Alternate Walkthrough
Alternate Sequence #
Output/Action for alternate flow
A1
Error writes to HUB Event log using RTI event log adapter

RTI Instructions
The following RTI instruction templates will be required for the Source to Hub Service:
Instruction Name
Type
Details
CorpTransfer
ReceiveRTI
UnHosted Receive
Unhosted instruction receives XML payload from web service and inserts to MSMQ on DB Server
Corp
RouterRTI
Scheduled
Scheduled instruction read from MSMQ and routes message to the appropriate transfer pattern

HubtoCorp
Pattern(n)RTI
Unhosted Receive
Unhosted instruction designed to interpret the contextual information of each transmission and perform the steps required to write the file to disk from the DDS database on the hub and move to the source system.  Can be SOA invoked or Scheduled
HubtoCorpTransfer
UnHosted Send
Unhosted instruction moves file via SFTP from hub staging to destination directory.

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
HubtoCorpPattern(n)RTI instruction is a variable component the specific instructions required will b determined by the details interface configuration sheets
3
General Alert and Error handling of events in the DDS database will are included in the Solution Architecture Technical Design









HUB TO CORPORATE SOURCE		                           		                                     VERSION 001



PAGE




HUB TO CORPORATE SOURCE		Page  PAGE 2 of  NUMPAGES 10


 SHAPE  \* MERGEFORMAT 	                                                                                                SHAPE  \* MERGEFORMAT
©2007 Accenture. All Rights Reserved.	 PAGE 1                                 DATE \@ "M/d/yyyy" 5/26/2011





## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
