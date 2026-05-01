---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/Ross/Technical_Design_Ross_Alerts_and_Monitors_v_loose.doc.md
tags: [ross, rti, store-transfer, archive-2011, tech-design]
project: 
status: unprocessed
---

# Technical_Design_Ross_Alerts_and_Monitors_v_loose.doc

## Source
File: `Brain/raw/.extract/Ross/Technical_Design_Ross_Alerts_and_Monitors_v_loose.doc.md`
Size: 17,589 bytes

## Raw content


STORE FILE TRANSFER


RTI ALERTS AND MONITORING
Technical Design

Version 001




Contents
 TOC \o "1-3" \h \z \u  HYPERLINK \L "_TOC294165704" 1	Document Review & Sign-off	 PAGEREF _TOC294165704 \H 3
 HYPERLINK \L "_TOC294165705" 1.1	Document Properties	 PAGEREF _TOC294165705 \H 3
 HYPERLINK \L "_TOC294165706" 1.2	Revision History	 PAGEREF _TOC294165706 \H 3
 HYPERLINK \L "_TOC294165707" 1.3	Document Approvers	 PAGEREF _TOC294165707 \H 3
 HYPERLINK \L "_TOC294165708" 1.4	Supporting Documents	 PAGEREF _TOC294165708 \H 3
 HYPERLINK \L "_TOC294165709" 2	Introduction	 PAGEREF _TOC294165709 \H 4
 HYPERLINK \L "_TOC294165710" 2.1	Purpose	 PAGEREF _TOC294165710 \H 4
 HYPERLINK \L "_TOC294165711" 2.2	Responsibility for this Document	 PAGEREF _TOC294165711 \H 4
 HYPERLINK \L "_TOC294165712" 2.3	Document Scope	 PAGEREF _TOC294165712 \H 4
 HYPERLINK \L "_TOC294165713" 2.4	Audience	 PAGEREF _TOC294165713 \H 4
 HYPERLINK \L "_TOC294165714" 3	RTI Monitors and Alerts	 PAGEREF _TOC294165714 \H 5
 HYPERLINK \L "_TOC294165715" 4	DDS Alerts and Monitoring	 PAGEREF _TOC294165715 \H 7
 HYPERLINK \L "_TOC294165716" 5	RTI  Agent Alerts	 PAGEREF _TOC294165716 \H 8
DOCUMENT REVIEW & SIGN-OFF
 Document Properties
AUTHOR
CREATION DATE
LAST UPDATED
VERSION
Geoff Lyle
5/25/2011
5/25/2011
1.0
Revision History
VER.
DATE
DESCRIPTION
AUTHOR
1.0
5/25/2011
Initial Draft
Geoff Lyle




 Document Approvers
NAME
ROLE
SIGNATURE
SIGN-OFF DATE
Nediljko Bilkic
SOA Architecture Lead


Abhi Srivastava
SOA  Lead


Soeren Ahrens
SOA Program Lead


Nathan Smith
SysRepublic Lead



Supporting Documents

DOCUMENT TITLE
DOCUMENT TYPE
AUTHOR
DATE
LOCATION










INTRODUCTION
Purpose
This document describes the Standard RTI componetns which should be monitored for the File Transfer HUB, and provides a desction of the Standard alerts that an RTI agent will generate for the Windows Event Log. This document also covers any assumptions/pre-requisites for the infrastructure as well as identifying the specific areas where monitoring would be required.

It is intended that this document serves as a working document as certain areas are subject to change over the lifetime of the RTI Infrastructure project as well as with the introduction of new interfaces. Where such changes do occur, examples being the introduction of additional Processing servers or changes to the server details (defined in the Appendices), it is expected that such changes will result in a new document version and a change log being recorded in the version history table in Document Control section.
Responsibility for this Document
The project team will own this document and subsequently is responsible for updates and versioning.  All changes and additions are subject to review prior to sign off.
Document Scope
This document will cover, the Stanadrd errors and alerts the base componets of the RT solution will generate.  It is not intended to describe the specifc error conditions that may occur related the functional alerting requirments of a specifc interface or alerting conditons for the DDS Hub.  The Specifc Details of those requirmentss should be addressed as part of each intefrace functional interface or file transfer specification.
Audience
This document is intended for persons who seek to understand the design of the file transfer instructions for Pattern 1 Transfers: Same file form Corporate Hub to All Stores.  The audience includes:
Project Managers
Functional Analysts
Application Architects
Software Developers
Testing Analysts
Production Support Personnel
RTI MONITORS AND ALERTS

This section details component specific monitoring which Sysrepublic recommends Ross setup with the CA UNICENTER Event Agent System Monitoring Tools for the support of the RTI infrastructure.  Note that the scope of this section is restricted the components delivered by Sysrepublic and will therefore focus on only on the HUB Web and Database Servers as well as the SQL Server database jobs for the CMC and DDS databases.
It is expected that monitoring and alerting will be subject to changes or refinements depending on the alerts being raised once the system has been fully rolled out and operational for a duration of time. Sysrepublic recommend the error scenarios used for alerting be tested/replicated on the relevant environments to guarantee an accurate representation of the errors/warnings and the handling of these by the alerting applications being used. While such errors would typically be consistent, there is a possibility of variance between different environments which could have implications for the alerting applications being used.
Sysrepublic assume that processes and procedures to resolve issues detected during operational processing will be defined by the teams supporting the solution at a 1st and 2nd line level. Details on any testing to be performed in respect of this section, 3rd party alerting software and operational support processes are out of scope.
Sysrepublic assume General SQL Server availability and monitoring will be managed by existing infrastructure alerting guidelines.  If RTI Components in the Integration Hub solution cannot access SQL server, those components will raise an error to the Windows event log in accordance with the specific scenario.
The table below describes components requiring monitoring for each applicable server. Note that the following checks need to be done for each individual server regardless of whether the server is in Active/Passive mode (or being accessed via a logical load balancer address):

Server
Component
Component Type
Details
Hub Web Server(s)
IIS Admin Service
Windows Service
Alert in the event the service is not running.
Message Queuing
Windows Service
RTI Agent$[Instance]
Windows Service
RTI Broadcast Manager
Windows Service
World Wide Web Publishing Service
Windows Service
Source: RTI Agent*
Application Log
Alert on errors (only)
 HYPERLINK "http://[SERVER]/RTIAgent_Admin/ServiceManagement.asmx" http://[SERVER]/RTIAgent_Admin/ServiceManagement.asmxURL
Perform a direct http request on each Web Server and alert if a code other than 200 (indicating that the site can be contacted) is returned.
Hub Database Server
Message Queuing
Windows Service

RTI Agent$[Instance]
Windows Service
Source: RTI Agent*
Application Log
Alert on errors (only)
Source: Broadcast Manager
Application Log
DDS Database – All SQL Agent Jobs
SQL Agent Job
Alert on failure for all scheduled jobs.
CMC Database – All SQL Agent Jobs
SQL Agent Job
Scheduled DDS Alerts
RTI Instruction
Specific functional alerts configured to meet the requirements of the file transfer project


DDS ALERTS AND MONITORING
All DDS Alerts generated at System or Instruction level will be written to the Windows Application Event Log using the Event Log adapter native to RTI.  In addition, some Alerts will have the capability of raising Alert meesgaes back to SOA via the BPEL Callback Web Service.  The two Alerts types are described below:

Hub Application Alerts:
 The Alert message written to the log will be in the standard Windows log format, and will be available for integration with the CA UNICENTER Event Agent System Monitoring Tools.  The Error log will have the following format:

Category ID
Event ID
Machine Name
Source
Severity
Error Description

Scheduled Alerts monitoring the DDS Database for specific conditions of an interface requirement will use the following design sequence:


SOA Web Serice Callbacks:
 When conditions require a Success of Failure Alert message back to SOA via the BPEL Callback, RTI will deliver the alert message back to SOA via the  InvokeRTIFileTransferResponseMessage  schema described in theTechnical_Design_BPEL_InvokeRTIWS_sCA_Sync v002 document.

CORPORATE RTI  AGENT ALERTS
All RTI Alerts generated at System or Instruction level will be written to the Windows Application Event Log using the Event Log adapter native to RTI.   The Alert message written to the log will be in the standard Windows log format, and will be available for integration with the CA UNICENTER Event Agent System Monitoring Tools.  The Error log will have the following format:

Category ID
Event ID
Machine Name
Source
Severity
Error Description

The following section describes the standard alerts that an RTI Agent may create in the Windows Event Log if a system error occurs:


Event ID:	5
Severity:	Warning
Reason:	The RTI Agent cannot find (or access) the registry key\value HKEY_LOCAL_MACHINE\SOFTWARE\Sysrepublic\RTI 2.0\RTI Agent\Last Event Time. This key is used to store the time of the last event that was transmitted by the agent.
Impact:	The RTI Agent will resend the same windows event log entries every time a service pulse is generated
Resolution:	Create the key\value (as a string type) if it does not exist or reinstall the RTI product. If the key\value does exist ensure that the account used by the RTI Agent service has sufficient privileges to access this part of the registry

Event ID:	10
Severity:	Error
Reason:	The RTI Agent configuration file could not be loaded. The file exists in D:\Program Files\Sysrepublic\RTI 2.0\RTI Agent and is called Sysrepublic.RTI.RTIAgent.Configuration.xml. This file may have been removed, got corrupted or cannot be accessed by the agent using a specific security account
Impact:	The RTI Agent service will not start and all instruction processing will be suspended
Resolution:	Re-supply the file and ensure that the account used by the RTI Agent service has sufficient privileges to access the file and path

Event ID:	20
Severity:	Error
Reason:	The RTI Agent service could not create one or more system threads to assign instruction processing. It is not possible to define clear cases for this scenario.
Impact:	Some RTI Agent processing will not start
Resolution:	Check the Error Message and investigate the Exception Stack supplied. This may indicate reasons for the failure. Attempt to stop and start the RTI Agent service to determine if the issue is repeatable

Event ID:	25
Severity:	Information
Reason:	The RTI Agent service encountered a problem whilst stopping
Impact:	None
Resolution:	Check the Error Message and investigate the Exception Stack supplied. Start and Stop the RTI Agent service repeatedly to determine if the error reoccurs.

Event ID:	26
Severity:	Information
Reason:	A service stop request has been received by the RTI Agent service
Impact:	All RTI Agent processing will not occur

Resolution:	Determine if the service should be stopped

Event ID:	30
Severity:	Warning
Reason:	The RTI Agent service encountered a problem whilst stopping a service thread
Impact:	None
Resolution:	Check the Error Message and investigate the Exception Stack supplied. Start and Stop the RTI Agent service repeatedly to determine if the error reoccurs.

Event ID:	65
Severity:	Warning
Reason:	The instruction has been configured to run multi-threaded but one or more adapters are not thread safe
Impact:	The instruction will run single threaded
Resolution:	Ensure that the instruction configuration is correct.

Event ID:	85
Severity:	Error
Reason:	An instruction could not be started by the RTI Agent service
Impact:	The instruction will not run
Resolution:	Check the Error Message and investigate the Exception Stack supplied. Start and Stop the RTI Agent service repeatedly to determine if the error reoccurs.

Event ID:	90
Severity:	Information
Reason:	The RTI Agent service is being restarted due to either a configuration change or a server restart request
Impact:	None
Resolution:	None

Event ID:	95
Severity:	Error
Reason:	The RTI Agent service encountered a problem whilst restarting
Impact:	The RTI Agent service will not start and all instruction processing will be suspended
Resolution:	Check the Error Message and investigate the Exception Stack supplied. Issue more restarts via the RTI Agent Administrator to determine if the problem continues to occur.

Event ID:	100
Severity:	Warning
Reason:	An instruction thread has been in a state of execution for a time period that has exceeded the timeout value set in the instruction configuration. The instruction is being aborted and will be restarted
Impact:	None
Resolution:	Ensure that the instruction timeout value supplied is long enough for the operation to complete. Additionally, check that connectivity performance to external dependencies used by the instruction (e.g. remote servers, databases) is optimal

Event ID:	105
Severity:	Warning
Reason:	An instruction thread has been selected for timeout but could not be aborted
Impact:	The transaction state of all adapters being used by the instruction may be inconsistent. This should not result in data loss however, under certain circumstances data duplication may be encountered
Resolution:	Ensure that the instruction timeout value supplied is long enough for the operation to complete. Additionally, check that connectivity performance to external dependencies used by the instruction (e.g. remote servers, databases) is optimal

Event ID:	110
Severity:	Error
Reason:	An instruction thread could not be restarted after a timeout has been actioned
Impact:	The instruction processing will be suspended
Resolution:	Restart the RTI Agent service. Also check the Error Message and investigate the Exception Stack supplied

Event ID:	120
Severity:	Warning
Reason:	The time check processing against an instruction failed
Impact:	Instructions will not be timed \out
Resolution:	Restart the RTI Agent service. Also check the Error Message and investigate the Exception Stack supplied

Event ID:	125
Severity:	Warning
Reason:	The RTI Agent could not transmit a service pulse
Impact:	The site will not have contacted the RTI Central Management Console (RTICMC) and therefore may appear inactive in the console. This event should be investigated if it persists for an hour or more
Resolution:	Investigate the connectivity between:
Store and PLSIHWEBDEV.ROS.com (NLB)
PLSIHWEBDEV.ROS.com (NLB) and PLSIHWEBDEV01 (WebServer(s))
If connectivity is OK ensure that the MSMQ server is running on Database Server and start the service if it is not running
If MSMQ is running, ensure that the queues have not backed up significantly on Hub Database Server.
If the MSMQ server is using large amounts of RAM (i.e. 500MB - 1GB+) or disk space, this would indicate that MSMQ has a large volume of unprocessed messages

Event ID:	130
Severity:	Warning
Reason:	The RTI Agent could not successfully build the service pulse for transmission
Impact:	The site will not have contacted the RTI Central Management Console (RTICMC) and therefore may appear inactive in the console
Resolution:	Restart the RTI Agent service. Also check the Error Message and investigate the Exception Stack supplied

Event ID:	135
Severity:	Warning
Reason:	A transformation adapter has returned null data
Impact:	Destination adapters on this instruction will not be invoked. Therefore data may not be transmitted
Resolution:	This may be by design. Refer to the instruction design to determine if this should happen

Event ID:	140
Severity:	Error
Reason:	An instruction thread has failed and is being terminated
Impact:	Instruction processing will be suspended
Resolution:	Restart the RTI Agent service. Also check the Error Message and investigate the Exception Stack supplied

Event ID:	145
Severity:	Warning
Reason:	A problem was encountered on an instruction but the operations is being retried
Impact:	The instruction processing will be retried but will not complete until the issue is resolved.
Resolution:	This event should be investigated if it persists for an hour or more

Event ID:	150
Severity:	Error
Reason:	The on-completion task of an instruction could not be run
Impact:	The instruction processing will complete but the on-complete task will not have been run
Resolution:	Restart the RTI Agent service. Also check the Error Message and investigate the Exception Stack supplied. Ensure that the instruction configuration is correct

Event ID:	155
Severity:	Error
Reason:	The on-failure task of an instruction could not be run
Impact:	The instruction processing will complete but the on- failure task will not have been run
Resolution:	Restart the RTI Agent service. Also check the Error Message and investigate the Exception Stack supplied. Ensure that the instruction configuration is correct

STORE RTI  AGENT ALERTS
 All RTI Alerts generated on Store Agents at System or Instruction level will be written to the Windows Application Event Log using the Event Log adapter native to RTI.   The Alert message written to the log will be in the standard Windows log format, and will be available for integration with the CA UNICENTER Event Agent System Monitoring Tools.  The Error log will have the following format:

Category ID
Event ID
Machine Name
Source
Severity
Error Description




The following section describes the standard alerts that an RTI Agent may create in the Windows Event Log if a system error occurs:









ROSS FILE TRANSFER RTI ALERTS AND MONITORING	                                              VERSION 001



PAGE




	Page  PAGE 12 of  NUMPAGES 12


 SHAPE  \* MERGEFORMAT 	                                                                                                SHAPE  \* MERGEFORMAT
©2007 Accenture. All Rights Reserved.	 PAGE 1                                 DATE \@ "M/d/yyyy" 5/26/2011





## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
