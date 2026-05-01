---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/Ross/Technical_Design_Ross_File_Transfer_Solution_Overview_v6_loose.doc.md
tags: [ross, rti, store-transfer, archive-2011, tech-design]
project: 
status: unprocessed
---

# Technical_Design_Ross_File_Transfer_Solution_Overview_v6_loose.doc

## Source
File: `Brain/raw/.extract/Ross/Technical_Design_Ross_File_Transfer_Solution_Overview_v6_loose.doc.md`
Size: 24,633 bytes

## Raw content


STORE FILE TRANSFER


SOLUTION ARCHITECTURE
Technical Design

Version 002




Contents
 TOC \o "1-3" \h \z \u  HYPERLINK \L "_TOC293927947" 1	Document Review & Sign-off	 PAGEREF _TOC293927947 \H 3
 HYPERLINK \L "_TOC293927948" 1.1	Document Properties	 PAGEREF _TOC293927948 \H 3
 HYPERLINK \L "_TOC293927949" 1.2	Revision History	 PAGEREF _TOC293927949 \H 3
 HYPERLINK \L "_TOC293927950" 1.3	Document Reviewers	 PAGEREF _TOC293927950 \H 3
 HYPERLINK \L "_TOC293927951" 1.4	Supporting Documents	 PAGEREF _TOC293927951 \H 3
 HYPERLINK \L "_TOC293927952" 2	Introduction	 PAGEREF _TOC293927952 \H 4
 HYPERLINK \L "_TOC293927953" 2.1	Purpose	 PAGEREF _TOC293927953 \H 4
 HYPERLINK \L "_TOC293927954" 2.2	Responsibility for this Document	 PAGEREF _TOC293927954 \H 4
 HYPERLINK \L "_TOC293927955" 2.3	Document Scope	 PAGEREF _TOC293927955 \H 4
 HYPERLINK \L "_TOC293927956" 2.4	Audience	 PAGEREF _TOC293927956 \H 4
 HYPERLINK \L "_TOC293927957" 3	Overview	 PAGEREF _TOC293927957 \H 5
 HYPERLINK \L "_TOC293927958" 3.1	Business and Technical Overview	 PAGEREF _TOC293927958 \H 5
 HYPERLINK \L "_TOC293927959" 3.2	Architectural Entities	 PAGEREF _TOC293927959 \H 6
 HYPERLINK \L "_TOC293927960" 3.3	Architectural Interactions	 PAGEREF _TOC293927960 \H 7
 HYPERLINK \L "_TOC293927961" 4	Network	 PAGEREF _TOC293927961 \H 8
 HYPERLINK \L "_TOC293927962" 4.1	Network Overview	 PAGEREF _TOC293927962 \H 8
 HYPERLINK \L "_TOC293927963" 4.2	Corporate Network Bandwidth	 PAGEREF _TOC293927963 \H 8
 HYPERLINK \L "_TOC293927964" 4.3	Store Network Bandwidth	 PAGEREF _TOC293927964 \H 8
 HYPERLINK \L "_TOC293927965" 5	Security	 PAGEREF _TOC293927965 \H 8
 HYPERLINK \L "_TOC293927966" 5.1	Activity Directory Group Policies	 PAGEREF _TOC293927966 \H 8
 HYPERLINK \L "_TOC293927967" 5.2	Ross Security Policies	 PAGEREF _TOC293927967 \H 10
 HYPERLINK \L "_TOC293927968" 6	Hub Component Details	 PAGEREF _TOC293927968 \H 11
 HYPERLINK \L "_TOC293927969" 6.1	Component Overview	 PAGEREF _TOC293927969 \H 11
 HYPERLINK \L "_TOC293927970" 6.2	Component Ownership	 PAGEREF _TOC293927970 \H 11
 HYPERLINK \L "_TOC293927971" 6.3	DDS Alerts and Monitoring	 PAGEREF _TOC293927971 \H 12
 HYPERLINK \L "_TOC293927972" 6.4	DDS Maintenace	 PAGEREF _TOC293927972 \H 12
 HYPERLINK \L "_TOC293927973" 6.5	Impact of Outage	 PAGEREF _TOC293927973 \H 12
 HYPERLINK \L "_TOC293927974" 7	St ore Agent Details	 PAGEREF _TOC293927974 \H 12
 HYPERLINK \L "_TOC293927975" 7.1	Agent Overview	 PAGEREF _TOC293927975 \H 12
 HYPERLINK \L "_TOC293927976" 7.2	Store Rollout	 PAGEREF _TOC293927976 \H 13
 HYPERLINK \L "_TOC293927977" 7.3	Store Configuration Management	 PAGEREF _TOC293927977 \H 13
 HYPERLINK \L "_TOC293927978" 7.4	Store Alerts and Monitoring	 PAGEREF _TOC293927978 \H 13
 HYPERLINK \L "_TOC293927979" 8	configuration management	 PAGEREF _TOC293927979 \H 13
 HYPERLINK \L "_TOC293927980" 8.1	RTI source code and config file management	 PAGEREF _TOC293927980 \H 13
 HYPERLINK \L "_TOC293927981" 8.2	RTI Instructions deployment procedure	 PAGEREF _TOC293927981 \H 13
 HYPERLINK \L "_TOC293927982" 8.3	RTI software patch deployment procedure	 PAGEREF _TOC293927982 \H 14
 HYPERLINK \L "_TOC293927983" 9	Assumptions	 PAGEREF _TOC293927983 \H 14
 HYPERLINK \L "_TOC293927984" 10	Constraints	 PAGEREF _TOC293927984 \H 14
DOCUMENT REVIEW & SIGN-OFF
 Document Properties
AUTHOR
CREATION DATE
LAST UPDATED
VERSION
Geoff Lyle
4/26/11
5/28/2011
1.2
Revision History
VER.
DATE
DESCRIPTION
AUTHOR
1.0
4/26/2011
Initial Draft
Geoff Lyle
1.1
5/19/2011
Updates following reveiw
Geoff Lyle
1.2
5/28
Udtaed Config Management
Geoff Lyle
 Document Reviewers
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
This document describes the high level architecture for the RTI Infrastructure and provides a detailed description of the Sysrepublic software components and systems interactions to be implemented for Ross Store File Transfer project. This document also covers any assumptions/pre-requisites for the infrastructure as well as identifying the specific areas where monitoring would be required.

It is intended that this document serves as a working document as certain areas are subject to change over the lifetime of the RTI Infrastructure project as well as with the introduction of new interfaces. Where such changes do occur, examples being the introduction of additional Processing servers or changes to the server details (defined in the Appendices), it is expected that such changes will result in a new document version and a change log being recorded in the version history table in Document Control section.
Responsibility for this Document
The project team will own this document and subsequently is responsible for updates and versioning.  All changes and additions are subject to review prior to sign off.
Document Scope
This document will cover, at a detailed level, the solution architecture design to meet business requirements as described in the functional requirements document for file transfer between ROSS corporate systems and store. The scope of this document includes the following:

High level architecture including the definition of key entities and their interactions.
Security recommendations, including group policies.
Identification of key architectural components and the ownership of their implementation.
Details of the impact of failure for key entities of the architecture.
Definition of pre-requisites for installing components delivered by Sysrepublic.
Description of components delivered by Sysrepublic.
Identification of areas within the architecture that require monitoring.
Configuration management

The following points are not in scope of this document:
Detailed description of architectural elements not delivered by Sysrepublic (e.g. Operating System, SAN, SQL Server, clustering).
Components related to specific file transfer interfaces.

Audience
This document is intended for persons who seek to understand the overall solution design of the store file transfer project. .  The audience includes:
Project Managers
Functional Analysts
Application Architects
Software Developers
Testing Analysts
Production Support Personnel
OVERVIEW
Business and Technical Overview

The following diagram illustrates the architecture and integration links between various entities of the RTI Infrastructure at Ross:


 EMBED Visio.Drawing.11

	Figure 1.
The above architecture in Fig.1 will use SAN based storage for providing data resilience as well as load balancing against the Processing Servers and SQL Server clustering to achieve both performance under load as well as seamless continuity in the event of outages. Where appropriate, configuration files will also be stored on the SAN (rather than local machines) and scalability achieved by increasing the number Web Servers.
Resilience of the Web Servers will be managed by Ross’s virtualization software to quickly (and automatically) bring up new cloned virtual machines in the event of an outage. It is therefore assumed that the storage for MSMQ message queues will be located in a shared area on the network which is accessible to any new images that could be brought up.
Further details on the above entities and interactions, including information about entity and data resilience, are described in the tables below.

Architectural Entities

Entity
Details
Resilience
RTI Web Servers
Host RTI for CMC  / DDS integration
Host RTI Corporate Agents
Host RTI Web Services
Continuity achieved during failover by the Ross virtualization software bringing up a new image of the machine. It is assumed that such a cloned image could be brought online within a minute and that the process performing this task would be automated.

RTI Database Servers
Host Central Management Console (CMC)
Host DDS Operations Console
Host MSMQ Messaging Service
Host CMC Database
Host DDS Database
Continuity provided by a clustered SQL Server environment which will store data to resilient SAN drives. Transactional continuity achieved by having all working data persisted on the SAN.

SAN Storage
Store all operational data and configurations.
Architecture assumes that resilient SAN will be setup with failover capability.
Store ISP Server
Host RTI for Store Agent
Architecture assumes that existing ISP failover and resilience standards will be in place.

Architectural Interactions
Interaction Link
Functions
Details
IL-01
RTI Configuration view
CMC Broadcast

RTI will store all configurations and license files on the SAN This approach will ease maintenance and restoration processes for web servers.
Configuration broadcast to RTI agents on the store ISP is done via .net remoting on port 50005. The proprietary RTI message uses TripleDES encryption with a fixed key.
IL-02
DDS management
Monitor DDS file transfer progress/status
IL-03
File get / put
RTI will access the SAN as part of the interface processing for both file drops and file pickups.
IL-04
Service Pulse data from remote RTI Agents.
DDS Access
Service Pulse data sent to the CMC from Remote RTI Agents.  DDS access by Store agents for event based push / pull transfers initiated by store agents.

IL-05
Transfer Invocation
Interface solutions may require SOA / BEPL invocation of unhosted RTI instruction on corporate RTI agent.
IL-06
SOA Callback
Web service call back to SOA for asynchronous response to SOA invocation.
IL-07
Direct file drops
Direct file pickups
SFTP movement of source files to Hub SAN storage
SFTP movement of Store file from hub to corporate systems
IL-08
DDS file transfers
File transfer process to and from stores will be done via file streaming over https.

NETWORK
Network Overview
Corporate Network Bandwidth
To prevent overloading the RTI hub and limit the maximum bandwidth used on the corporate network to 20Mbps, the following configuration is proposed.
Store Network Bandwidth
Ross stores’ DSL network connectivity to corporate  is usually 256Kbps, and the fall back is dial-up (56Kbps). To prevent file transfers from taking over store network bandwidth, the RTI DDS will be configured to limit the network bandwidth used per connection for file transfers to the stores.


SECURITY
Activity Directory Group Policies

Sysrepublic assume that Ross will incorporate the above architecture into their existing security model and that this will be managed by Ross. Sysrepublic recommend that the security is managed using Active Directory group policies allowing access to be controlled centrally for the accounts defined in the following table:

Account
User/Group
Details
Privileges / Group Membership
RTI Infrastructure Administrators
Group
Members of this group will have full access to view, control and configure the RTI “Infrastructure” interfaces.

Remote access to Hub servers.
Stop / Start of “Infrastructure” RTI Windows Service on machines running RTI.
Read / Write access to RTI “Infrastructure” directories (containing all configuration files for the RTI Infrastructure).
Read/Write access to CMC SQL Server Database.
Read/Write access to any databases used specifically for the overall Infrastructure interfaces.
Read / Write access to “Infrastructure” MSMQ message queues.
RTI Infrastructure Readers
Group
Members of this group will have read access to view, control and configure the RTI “Infrastructure” interfaces.

Remote access to Management/Persistence and Processing servers.
Read access to RTI “Infrastructure” directories (containing all configuration files for the RTI Infrastructure).
Read access to CMC SQL Server Database.
Read access to any databases used specifically for the overall Infrastructure interfaces.
Read access to “Infrastructure” MSMQ message queues.
RTI Super Users
Group
Members of this group will have full access to the entire RTI infrastructure (including RTI interfaces and required access to 3rd party systems).
Member of all RTI Administrator groups (see the privileges for these groups for further details).
RTI Super Readers
Group
Members of this group will have read access to the entire RTI infrastructure (including RTI interfaces and required access to 3rd party systems).
Member of all RTI Reader groups (see the privileges for these groups for further details).
RTI Infrastructure Service Account
User
Used to run the Windows Services for the RTI Infrastructure interfaces (only) as well as all IIS based RTI web services (including interface related web services).
Account dedicated for Windows service use only and not for user access (to minimise the risk of account issues such as locking to causing the service not to run).
Member of the RTI Infrastructure Administrators group.
Although this account will also be used for running interface specific IIS web services for which the account permissions  may not be sufficient, the intention is that where such scenarios arise the relevant RTI [Interface] Service account will be used to override this at the individual RTI instruction level.
DDS Users
Group
Members of this group will have full access to view, control and configure DDS
Read/Write access to DDS SQL Server Database.

CMC Users
Group
Members of this group will have full access to view, control and configure CMC
Read/Write access to CMC SQL Server Database.

Specific User Accounts
User
User accounts of staff for the relevant teams (e.g. RTI Infrastructure Project/Support, RTI Interface Project/Support) can be added to the group memberships accordingly to their specific role(s).
Member of at least one of the groups (described in the table) according to the user’s role.

NB: The above RTI users / groups are named to reflect the roles only and their precise names (and domain) are currently out of scope of this document.
User access (e.g. for Support staff) and Windows service account access (i.e. Service Accounts for a given interface) will be manageable at both an infrastructure and interface level using the AD group memberships. The above groups will also allow Reader access to the specific areas should it be necessary to provide external departments access to view the setup without the ability to modify or control the overall interfaces. Overriding RTI Super User and RTI Super Reader groups will allow either full access or reader access to both the infrastructure and all interfaces.

Ross Security Policies

The overall solution is designed to meet the Ross security policy requirements.

The RTI web and database server environments will be secured and certified using Win2008 minimum security baseline
The RTI DB system will be secured and certified using SQL 2008 minimum security baseline
The RTI Web server will be secured and certified using the IIS 7.5 minimum security baseline
Administrative accounts will be limited to select list of authorized users only
Roles and Responsibilities will be defined as it pertains to account administration. Process for approval and periodic review of accounts will be documented as part of support processes.
Process and procedure for adding, modifying and deleting accounts will be documented as part for support processes.
The support Process and procedure for managing service accounts for periodic reset password will be documented
Network File transmission will happen thru secure channels - HTTPS for file transfer between RTI hub and store agents and SFTP for file transfers between RTI hub and Ross corporate systems.
Auto expiration of data files will be set up for each file transfer interface so data is not sitting around on the RTI hub server for any longer than required.

HUB COMPONENT DETAILS
Component Overview

The RTI Hub components are as follows:
Hardware/VM platform
SQL Server
Microsoft .NET Framework
IIS 7
RTI Hub Agent
RTI CMC
RTI DDS
RTI Web Services

Component Ownership
Component
Ownership
Comments
Hardware / VM Setup
Ross
Sysrepublic assume that these components are already setup on the existing shared SQL Server environment.
Operating System
Ross
.NET
Ross
IIS
Ross
SQL Server
Ross
RTI components
Sysrepublic

DDS Alerts and Monitoring
All DDS Alerts generated at System or Instruction level will be written to the Windows Application Event Log using the Event Log adapter native to RTI.  In addition, some Alerts will have the capability of raising Alert meesgaes back to SOA via the BPEL Callback Web Service.  The two Alerts types are described below:

Hub Application Alerts:
 The Alert message written to the log will be in the standard Windows log format, and will be available for integration with the CA UNICENTER Event Agent System Monitoring Tools.  The Error log will have the following format:

Category ID
Event ID
Machine Name
Source
Severity
Error Description



SOA Web Serice Callbacks:
 When conditions require a Success of Failure Alert message back to SOA via the BPEL Callback, RTI will deliver the alert message back to SOA via the  InvokeRTIFileTransferResponseMessage  schema described in theTechnical_Design_BPEL_InvokeRTIWS_sCA_Sync v002 document.

DDS Maintenace
The file transfer messages logged in the the RTI DDS database will be purged after a period of 90 days of file transfer completion or file transfer request expiry as applicable.
Impact of Outage
Sysrepublic assume that in the event of issues affecting the availability of SQL Server, the shared clustered SQL Server setup at Ross will support seamless failover. Sysrepublic also assume that Ross will setup the necessary SQL Server backup processes (with guidance from Sysrepublic where appropriate).

In the event one of the Processing Servers becomes unavailable, the load balancing setup should automatically route all connections to the available server(s). This process should occur seamlessly with the impact to the overall integration architecture being as follows:
Transmissions at the time of the outage will fail but would be expected to retry (and be successful on the first subsequent attempt routed by the load balancer to an available server).
Potential for reduced performance during high volumes when there is reduced server availability.
As all data is persisted on either the SAN or clustered SQL Server databases no data should be lost during an outage of a Processing Server.

ST ORE AGENT DETAILS
Agent Overview
Each Ross and DDs store will have an RTI Store Agent deployed on the Store ISP.  The Store RTI agent will be confugred to Poll the DDS Database for new messages indicating a file is ready to be pulled from the Hub to the store.  Store Agentss will also push files form the store to the Hub at scheduled intervals.
Store Agents are managed centrally from corporate systems via the RTI Cetral Management Console.  When a new agent is deployed to stores the base configuration file will contain the Serive Pulse instruction allowing a store to call home to the CMC and register itself on the network.
Store Agents will not require the RTI Webservceis to be deployed on store servers. After registration in the CMC, detailed file transfer configuration is pushed form the CMC out to stores and updated on an onging basis via .Net Remoting.
Store Rollout
Store Agent rollout will be facilitated by an automated install batch script which will be deployed via CA Software Delivery to store.  Sysrepiublic will develop unattended install and uninstall scripts to support store deployment.
The store package will conist of the following package components:
RTI Agent Install
RTI Adapter Install
DDS Adpater Install
RTI Zip Adapter
Service Pulse Configuration File
Store Configuration Management
Cofiguration details for all store agents will be managed on the CMC.  Communication to stores from the CMC will be via the .Net Remoting prootocal on Port 50005.
Store agents will have an RTI agent variable to hold the Hub DNS name.  All Hub URLS referenced by the store agentswill use this variable to reach their specific web services.
New store agent instructions will be exported from the DEV environemt test store after testing is completed and broadcasted from the production  CMC on the Hub to a target group of stores for the new interface.
Store Alerts and Monitoring
All RTI Alerts generated at System or Instruction level will be written to the Windows Application Event Log using the Event Log adapter native to RTI.   The Alert message written to the log will be in the standard Windows log format, and will be available for integration with the CA UNICENTER Event Agent System Monitoring Tools.  The Error log will have the following format:

Category ID
Event ID
Machine Name
Source
Severity
Error Description


CONFIGURATION MANAGEMENT
RTI source code and config file management
Current RTI configurations for both the store and hub will be maintained on Ross’ infrastructure and be made available for development and deployment to new stores.  Version information for each instruction will be maintained in its description field.


RTI Instructions deployment procedure
New RTI instructions will be deployed to the hub by promoting from dev or test environments.  Because any new instructions will depend heavily on settings specific to the environment, such as specific server names, these parameters will need to be changed when promoting from a test environment into a production environment.
Some environment dependent parameters will be stored as global “Agent variables” in the RTI agent and in this case each agent will hold settings for its environment outside of the instruction, which will ease deployment.  The variables include corporate server names, SFTP users and SSH key locations.  Changes will be maintained in a centrl place and described as part of installation instructions for a new/changed file transfer.
Because of these considerations, it is not possible to simply promote a configuration into production by copying a file.  The new instruction’s specific configuration may be copied to the destination agent, rather than an entire agent’s configuration.  This can be done through the RTI Agent Administrator by right-clicking on an instruction and selecting “copy”.  This operation will copy the underlying configuration xml for just that instruction, and that specific configuration piece can then be pasted into the next environment’s agent configuration.

RTI software patch deployment procedure
RTI software updates may be delivered by Sysrepublic when required due to reported issues or additional requirements.  These updates should be deployed with Sysrepublic’s guidance only, and the specific installation procedure must be considered on a case-by-case basis.
Ross Change Management Procedures for RTI Instructions

Chnages to the Ross file transfer Hub and Store agents will follow the Ross Chage managemen t procedures and Harvest Process.  The process we inclue the follwoig steps for introduction of new functionality to the File Transfer solution::
1.	Development and unit testing will be completed and approved in the DEV Environment
2.	The development team will raise a change order for the creations of a Harvest  package
3.	XML files from Dev will be checked in to Harvest
4.	Installation instructions, including global variable settings will be provided in the change order
5.	SOA support team will be responsible for deploying the new package to the PERF environment
a. Hub install will be directly on the Hub Servers by the SOA team
b. Store agent instructions changes will be broadcast to Perf Stores via the Perf CMC
6.	End-to-end and performance testing is done in PERF env
7.	Change order is approved
8.	SOA support team will install all approved changes to the PROD environment
a. Hub install will be directly on the Hub Servers by the SOA team
b. Store agent instructions changes will be broadcast to Prod Stores via the Prod CMC
ASSUMPTIONS

CONSTRAINTS












ROSS INTEGRATION HUB SOLUTION ARCHITECTURE	                                                          VERSION 001



PAGE




	Page  PAGE 14 of  NUMPAGES 14


 SHAPE  \* MERGEFORMAT 	                                                                                                SHAPE  \* MERGEFORMAT
©2007 Accenture. All Rights Reserved.	 PAGE 1                                 DATE \@ "M/d/yyyy" 5/31/2011





## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
