---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/Ross/Technical_Design_RTI_Hub_To_Store_Transfer v3.doc.md
tags: [ross, rti, store-transfer, archive-2011, tech-design]
project: 
status: unprocessed
---

# Technical_Design_RTI_Hub_To_Store_Transfer v3.doc

## Source
File: `Brain/raw/.extract/Ross/Technical_Design_RTI_Hub_To_Store_Transfer v3.doc.md`
Size: 13,212 bytes

## Raw content


TECHNICAL DESIGN FOR
FILE TRANSFER REPLACEMENT PROJECT



CORPORATE INTEGRATION HUB TO STORE
Version 003




Contents
 TOC \o "1-3" \h \z \u  HYPERLINK \L "_TOC292353901" 1	Document Review & Sign-off	 PAGEREF _TOC292353901 \H 3
 HYPERLINK \L "_TOC292353902" 1.1	Document Properties	 PAGEREF _TOC292353902 \H 3
 HYPERLINK \L "_TOC292353903" 1.2	Revision History	 PAGEREF _TOC292353903 \H 3
 HYPERLINK \L "_TOC292353904" 1.3	Document Approvers	 PAGEREF _TOC292353904 \H 3
 HYPERLINK \L "_TOC292353905" 1.4	Supporting Documents	 PAGEREF _TOC292353905 \H 3
 HYPERLINK \L "_TOC292353906" 2	Introduction	 PAGEREF _TOC292353906 \H 4
 HYPERLINK \L "_TOC292353907" 2.1	Purpose	 PAGEREF _TOC292353907 \H 4
 HYPERLINK \L "_TOC292353908" 2.2	Responsibility for this Document	 PAGEREF _TOC292353908 \H 4
 HYPERLINK \L "_TOC292353909" 2.3	Document Scope	 PAGEREF _TOC292353909 \H 4
 HYPERLINK \L "_TOC292353910" 2.4	Audience	 PAGEREF _TOC292353910 \H 4
 HYPERLINK \L "_TOC292353911" 3	Overview	 PAGEREF _TOC292353911 \H 5
 HYPERLINK \L "_TOC292353912" 3.1	Business and Technical Overview	 PAGEREF _TOC292353912 \H 5
 HYPERLINK \L "_TOC292353913" 4	Design	 PAGEREF _TOC292353913 \H 6
 HYPERLINK \L "_TOC292353914" 4.1	Interface/Service Pattern	 PAGEREF _TOC292353914 \H 6
 HYPERLINK \L "_TOC292353915" 4.2	Sequence Diagram	 PAGEREF _TOC292353915 \H 6
 HYPERLINK \L "_TOC292353916" 4.3	RTI Components	 PAGEREF _TOC292353916 \H 9
 HYPERLINK \l "_Toc292353917" 4.3.1	RTI Web Services	 PAGEREF _Toc292353917 \h 9
 HYPERLINK \l "_Toc292353918" 4.3.2	RTI Instructions	 PAGEREF _Toc292353918 \h 10
 HYPERLINK \L "_TOC292353919" 5	Operations	 PAGEREF _TOC292353919 \H 10
 HYPERLINK \L "_TOC292353920" 5.1	Restart/Recover conditions	 PAGEREF _TOC292353920 \H 10
 HYPERLINK \L "_TOC292353921" 6	Infrastructure considerations	 PAGEREF _TOC292353921 \H 11
 HYPERLINK \L "_TOC292353922" 7	Tokens	 PAGEREF _TOC292353922 \H 11
 HYPERLINK \L "_TOC292353923" 8	Special Unit Test Conditions	 PAGEREF _TOC292353923 \H 11
 HYPERLINK \L "_TOC292353924" 9	Assumptions	 PAGEREF _TOC292353924 \H 11
DOCUMENT REVIEW & SIGN-OFF
 Document Properties
AUTHOR
CREATION DATE
LAST UPDATED
VERSION
Geoff Lyle
05/02/2011
05/21/2011
003
Revision History
VER.
DATE
DESCRIPTION
AUTHOR
001
05/02/2011
Initial Draft
Geoff Lyle
002
5/4/2011
Updates after initial review
Geoff Lyle
003
5/21//2011
Updated sequence diagram
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
The purpose of this document is to define the essential characteristics of the RTI Corporate Integration Hub to Store transfers. The document will identify the communication internal to RTI and define the flow of data between Hub and Store ISP.  Ross application and Store Systems teams are expected to reach a mutual agreement on the interface design prior to technical design.
Responsibility for this Document
Sysrepublic will own this document and subsequently is responsible for updates and versioning.  All changes and additions are subject to review prior to sign off.
Document Scope
This document will cover, at a detailed level, the design as described by the functional requirements for communication between ROSS systems integration and Store Systems. The document details the solution design and features the Integration components to be used for interfacing with the Store ISP. The document will also feature the common exception handling service for the RTI processes which manage the transfer of files between the two environments.

This document is intended to provide the technical design pattern for all RTI Corporate Integration Hub to Store transfers.  Specific interface configuration sheets will detail the requirements for individual file transfer.

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
The purpose of this document is to provide a design pattern for any Corporate Integration Hub transfer to the Store.  This process defines how the store will Poll the Integration hub looking for pending transfers and the initiate the movement of a file from the Hub to the Store ISP.  This document does not cover the process which moves a file form the source system to the Hub.  This document does not make any assumptions as to the 'business objective or purpose' of the files being transferred, this information will form part of the end to end design of the business application utilizing this file transfer solution.

The pattern described here will enable a repeatable mechanism poll the integration Hub and initiate and https stream to move a file from the hub to a destination on the store ISP. Transfer a file or set of files from a central corporate system location to a store location.

The pattern will cater for the following transmission options
Event based monitoring of the DDS database
Flexible file renaming
Compression
Creation and explosion of ZIP archives for recursive directory requirements
Initiating in store post processing as required

The pattern described in this document will be event based, with each store agent listening for new messages on the DDS database, and initiating a file transfer to store when a new message is received.

Each file or archive can be regarded as a 'transmission' from hub to store. Each transmission will be logged for audit purposes and alerting will be implemented to highlight non-transmission of data.

The file transfer solution will be built using the Sysrepublic RTI technology platform. RTI will provide the data movement and logging engine for all transmissions. For more information on RTI please see the 'RTI Help' documentation.

The following set example interfaces will be supported by the Pattern described in this Document:

Bin File
The Source - Update
Merchandise Hierarchy
Weekly Item File
Weekly Price File
Store List





DESIGN
Interface/Service Pattern
Service would follow point to point pattern and frequency of file transfers will be event driven.
Sequence Diagram
Normal Flow Sequence Diagram



Normal Sequence Diagram Walkthrough
Normal Sequence #
Event
Component Invoked
Output
Alternate flow sequence#
1.



DDS subscribe web service exposes DDS database messages to store agents polling for new events

DDSsubcribeWS
New DDS message Broadcast

2a.
Scheduled instruction on the RTI store agent polls DDS looking for new messages
StorePollDDS
https stream initiated

2b.
DDSadapter streams file from Hub to Store

StorePollDDS
File transferred

2c.
Store Agent will report success / fail back to DDS upon completion or failure of the https
StorePollDDS
Update to DDS

2d.

StorePollDDS transform step uncompress file at store

StorePollDDS
Transform step

2e.
StorePollDDS file adapter renames and writes file to disk

Note: If rename step complicated, may require post processing instruction at step 3a)
StorePollDDS
File adapter step

2f.
DSS adapter calls back DDS insert a new error message to DDS.  Will be picked up by a DDS Alert monitor
StorePollDDS
Insert DDS

2g.
On fail write message on store ISP application event log

StorePollDDS
On success / on Fail

2h.
On Success write to store ISP application event log / or call post processing instruction
StorePollDDS
Complete / Post Process

3a.
Unhosted receive executes required post processing step at store:

(Unzip, rename, respond message)


SourceToHub
Pattern(n)RTI
Call SFTP adapter

3b.
On success or failure call windows event log adapter to write status to store ISP event log
SourceToHub
Pattern(n)RTI
Complete



Alternate Flow




Normal Sequence #
Event
Component Invoked
Output
Alternate flow sequence#
1.



DDS subscribe web service exposes DDS database messages to store agents polling for new events

DDSsubscribeWS
New DDS message Broadcast

2a.
RTI instruction with Preprocessing rule runs on a schedule to execute a task on the ISP
StorePreProcessingRule(n)
Pre processing step completed

2b.
Scheduled instruction calls unhosted Poll DSS to initiate pull from Hub
StorePreProcessingRule(n)
UnHostedPollDDS initiated

3a.
Unhosted instruction on the RTI store agent polls DDS looking for new messages
StorePollDDS
https stream initiated

3b.
DDSadapter streams file from Hub to Store

StorePollDDS
File transferred

3c.
Store Agent will report success / fail back to DDS upon completion or failure of the https process
StorePollDDS
Update to DDS

3d.

StorePollDDS transform step uncompress file at store

StorePollDDS
Transform step

3e.
StorePollDDS file adapter renames and writes file to disk

Note: If rename step complicated, may require post processing instruction at step 3a)
StorePollDDS
File adapter step

3f.
DSS adapter calls back DDS insert a new error message to DDS.  Will be picked up by a DDS Alert monitor
StorePollDDS
Insert DDS

3g.
On fail write message on store ISP application event log

StorePollDDS
On success / on Fail

3h.
On Success write to store ISP application event log / or call post processing instruction
StorePollDDS
Complete / Post Process

4a.
Unhosted receive executes required post processing step at store:

(Unzip, rename, respond message)


SourceToHub
Pattern(n)RTI
Call SFTP adapter

4b.
On success or failure call windows event log adapter to write status to store ISP event log
SourceToHub
Pattern(n)RTI
Complete


RTI Components
RTI Web Services

WEB Service Name
URL
DETAILS
DDSsubscribeWS
XX
Incoming DDS web service

RTI Instructions
The following RTI instruction templates will be required for the Hub to Store Service:
Instruction Name
Type
Details
HostedPollDDS
Scheduled
Hosted Instruction to Poll DDS
StorePreProcessRule1
Scheduled
Scheduled instruction runs a pre process to ensure that no file exists in destination directory before initiating a new transfer
UnHostedPollDDS
Unhosted Receive
UnHosted Instruction to Poll DDS when initiated by a preprocessing rule
StorePost
ProcesingRule1
Unhosted Receive
Unzip archive to a specific directory after transfer to ISP complete
StorePost
ProcesingRule2
Unhosted Receive
Rename file at destination if rule too complex for base file adapter functionality
StorePost
ProcesingRule3
Unhosted Receive
Respond to DDS with file complete message if required for message correlation

OPERATIONS
Restart/Recover conditions
FAILURE POINTDESCRIPTIONRESUBMIT FUNCTIONALITYPROCESS TYPEGUIDING PRINCIPLESUPPORT PROCEDUREFREQUENCYHostedPollDDS /
UnhostedPollDDS
Fails to connect to DDS WS
Error occurs and Retry
N/A
Infrastructure Issue
?
Low
HostedPollDDS /
UnhostedPollDDS
RTI fails to transfer file
Error occurs and Retry / restart transmission
Https / Transfer
Infrastructure Issue
?
Low
HostedPollDDS /
UnhostedPollDDS
RTI fails to uncompress at store
None update DDS with fail
Uncompress
Store Issue
?
Low
HostedPollDDS /
UnhostedPollDDS
RTI fails to Write to disk
None update DDS with fail
Disk write
Store Issue
?
Low
StorePost
ProcessingRule(n)
RTI fails to complete post processing step
None update store ISP event log with error code.
Event log
Store Issue
?
Low
StorePre
ProcessingRule(n)
RTI fails to complete post processing step
None update store ISP event log with error code.
Event log
Store Issue
?
Low



ASSUMPTIONS
ID
DESCRIPTION
1
All the attributes defined in the message body of the invocation message should be treated as overrides for any default value defined in the RTI file transfer metadata.
2
StorePostProcessingRule(n)RTI instruction is a variable component the specific instructions required will be determined by the details interface configuration sheets
3
General Alert and Error handling of events in the DDS database will are included in the Solution Architecture Technical Design
4
Processing errors which occur at the store will be written to the Store’s ISP event application log









CORPORATE INTEGRATION HUB TO STORE	                                                                    VERSION 002



PAGE




CORPORATE INTEGRATION HUB TO STORE		Page  PAGE 3 of  NUMPAGES 11


 SHAPE  \* MERGEFORMAT 	                                                                                                SHAPE  \* MERGEFORMAT
©2007 Accenture. All Rights Reserved.	 PAGE 1                                 DATE \@ "M/d/yyyy" 5/26/2011





## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
