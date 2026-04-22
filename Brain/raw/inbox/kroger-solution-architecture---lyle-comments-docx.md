---
date: 2026-04-22
type: raw
source: /Users/gclyle/mnt/nas-archive/Work/Clients/KROGER/Kroger Solution Architecture - lyle comments.docx
tags: [secure, secure, kroger, retail, client-implementation]
project: secure
status: unprocessed
---

# Kroger Solution Architecture - lyle comments.docx

## Source
File: `/Users/gclyle/mnt/nas-archive/Work/Clients/KROGER/Kroger Solution Architecture - lyle comments.docx`
Size: 17,053 bytes

## Raw content
![SysSecStore](data:image/png;base64...)

**Solution Architecture**

Contents

[Introduction 3](#_Toc442087989)

[Secure Store Application Overview 3](#_Toc442087990)

[Presentation Layer 4](#_Toc442087991)

[Service Layer 4](#_Toc442087992)

[Data Layer 5](#_Toc442087993)

[**Deployment Architectures** 5](#_Toc442087994)

[**Virtual Non-Redundant (typical)** 6](#_Toc442087995)

[Physical Architecture 7](#_Toc442087996)

[Server Inventory for Secure 3.2 8](#_Toc442087997)

[Redundancy and Load Balancing 9](#_Toc442087998)

[Virtual Machine Redundancy 9](#_Toc442087999)

[Additional Options 11](#_Toc442088000)

[Non Production Hardware Requirements 11](#_Toc442088001)

# Introduction

The purpose of this document is to describe the Physical Architecture scales available for the implementation of Secure Store, exception based reporting platform at Kroger. The document will contain two architecture scales:

* Large Configuration at 26 weeks
* Optimal Configuration at 7 weeks

The architecture is based on estimates Sysrepublic have made based on what it knows about Kroger. Sysrepublic however does suggest Kroger fills the sizing survey to get a more accurate idea on the architecture size required for the Secure implementation.

# Data Volume

Below are three tables that used to estimate the potential scope of data volume for this implementation

**Transaction Volume**

|  |  |  |
| --- | --- | --- |
|  | Daily Average | Peak |
| POS Transactions per store per day | 2,700 | unknown |
| Items per POS Transaction (Basket Size) | 6.6 | unknown |
| Number of Tender Types used per POS Transaction | 0.9 | unknown |
| Number of discounted line items per POS Transaction | 3.3 | unknown |

## Transaction Characteristics

The following information could not be estimated, but will only have a marginal effect on the overall sizing result.

|  |  |  |
| --- | --- | --- |
|  | Daily Average | Peak |
| Percent of Transactions with Staff Discounts | 0 % | 0 % |
| Percent of Transactions with Loyalty Card | 0 % | 0 % |
| Percent of Transactions with Age Verification | 0 % | 0 % |
| Percent of Transactions with Discounts | 0 % | 0 % |
| Percent of Recalled Transactions | 0 % | 0 % |
| # of Transactions Requiring Mgmt Override (Daily) | 0 % | 0 % |
| Percent of Gift Cards Sold | 0 % | 0 % |
| Percent of Gift Cards Reloaded | 0 % | 0 % |
| Percent of Transactions with Staff Discounts | 0 % | 0 % |
| Percent of Transactions with Loyalty Card | 0 % | 0 % |
| Percent of Transactions with Age Verification | 0 % | 0 % |

## Estate Characteristics

|  |  |
| --- | --- |
|  | Value |
| Number of Stores currently in the estate | 3100 |
| Estimated amount of weeks required for trending purposes? | 26 weeks |
| Are we storing the receipt image | No |
| Peak days | currently unknown |

**Sizing**

Sizing is based on the below information. Sysrepublic can estimate a storage needs of around 6.1TB.

This estimate is calculated with assumption that SQL Server Enterprise is used.

|  |  |
| --- | --- |
| Databases (including log size) | Size (GB) |
| Main Transactional Repository | **6000** |
| Application Databases | **100** |
| Total | **6100** |

The above estimates equate to an average of 236GB per week.

For the purposes of demonstrating two architectural configuration the document will use a

* Large Configuration at 26 weeks resulting in a 6.1TB detailed repository
* Optimal Configuration at 7 weeks resulting in a 1.6TB detailed repository

# Physical Architecture

The following two diagrams depicts the physical server architecture typically built to host the Client production implementation of either Secure Store. The infrastructure required can be scaled vertically and horizontally depending on the volume of data and user needed to access the application.

The first diagram shows the components required for Secure Store. The Infrastructure described below assumes components already exist in the Client environment such as Active Directory servers.

![](data:image/x-emf;base64...)

## Server Inventory for Secure Store

The following table contains the prerequisites components needed on each machine type

|  |  |  |
| --- | --- | --- |
| Machine Name | Application Function | Software |
| Secure Web App | Each machine has a web server handling all presentation requests for Secure Application. | Microsoft Windows 2012R2  Microsoft .NET Framework 4.5.2 (or above)  IIS 7.5 or 8.5 |
| Secure Module Host \* | Module Host Instance, executing Notification Services, Cached Results, Topic Services, Journal Reader and Maintenance | Microsoft Windows 2012R2  Microsoft .NET Framework 4.5.2 |
| Secure Database Server Store | Provides the Database Engine and Reporting Services to the Secure Application. | Microsoft Windows 2012R2  Microsoft .NET Framework 4.5.2  \*\*Microsoft SQL Server 2016 Enterprise Edition.  Microsoft SQL Server Reporting Services  Microsoft SQL Server Integration Services |
| Secure Report Server | An optional server for scaling out SQL Server Reporting Services. | Microsoft Windows 2012R2  Microsoft .NET Framework 4.5.2  Microsoft SQL Server Reporting Services |
| Data Loader | Provides an atomic data loading function that processes all received data into the appropriate database repository. | Microsoft Windows 2008R2/ 2012R2  Microsoft .NET Framework 4.5.2  Sysrepublic Real Time Integrator (RTI) 4 cores / 8Gb |
| SAN | Shared Storage for databases and VM images | Assumes a combination of FusionIO / SAN storage for backups etc. |

\*The module host is broken out onto a separate server in this architecture to plan for horizontal scaling of the infrastructure. However, depending on the number of executing monitors and their schedule, this service can be collapsed onto the web application server.

\*\* SQL Enterprise Edition is required for both table partitioning and compression feature of the software.

### Storage and Networking Requirements

Sysrepublic has built and specified many Secure infrastructures using a variety of hardware vendors and can recommend specific options aligned with Client’s preferences.

In addition to 'standard' server, network and storage infrastructure. Sysrepublic has worked extensively with leading edge hardware options to provide high performance options for the Secure application. One of these vendors is 'Fusion IO' now ‘Sandisk’. Sandisk provide an Enterprise class high performance solid state storage platform which is ideally suited for the Secure application. The Fusion IO technologies form part of the infrastructure stack that Sysrepublic relies on for our hosted instances of the application.

The above architecture assumes LAN connectivity of 10Gbe bandwidth between all servers. Storage requires connectivity to the database server via fiber channel and at 16Gbe .

# Non Production Hardware Requirements

In addition to the Secure production environment it is required for two non-production environments to be put in place. The two environments are to act as a test/certification environment, where production changes are tested and a development environment where configuration changes are made to be presented to the user community before signoff.

Each of the non-production environments will require one physical server as described above in the ‘Physical Application Server Hosts’ section. Both non-prod environments can be fully virtualized and deployed to this platform, the Sysrepublic project team can provide a detailed recommendation for the sizing of non-production environments in line with the testing and IT governance procedures in place at Kroger during the implementation project.

# Large Scale Architecture

## Production Hardware Requirements

The production system will be housed on multiple server machines as described in physical architecture diagram below. The following requirements are meant to be suitable for a production environment; final details will be refined as the full requirements of the solution are solidified.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Machine Name | Description | Cores | RAM | Quantity | Storage |
| Secure Web App | The application tier of the Secure Store environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Web Application servers will host the main web user interface. | 4 | 8 | 4 | OS Recommended Requirement |
| Secure Module Host \* | The application tier of the Secure Store environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Application servers will perform data processing and loading. | 4 | 8 | 4 | OS Recommended Requirement |
| Secure Report Server | The Reporting Servers in Secure Store environment are deployed virtually running Windows Hyper V Server (VM Ware is also supported). The Reports servers managed the aggregation and delivery of data to filed users and the investigation center within the Secure Application. | 2 | 8 | 2 | OS Recommended Requirement plus 150GB for SSRS |
| Data Loader | The Integration Layer of the Secure Store environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Integration Database servers will host the data processing and loading of flat or xml files, service based data flows and direct table connection from all source data systems. | 4 | 32 | 6 | 750 GB of SAN connected storage for SQL Server Databases and Log Files |
| SAN | Shared Storage for databases and VM images |  |  |  |  |

### Database Servers

The Database servers will act as the main storage repository for all application data. These servers will represent the highest point of contention on the system and therefore need to be adequately sized to ensure effective system performance. Disk, CPU and memory requirements are high and very specific.

Two Servers of the Following Specification

* Intel 10x Multi Core Xeon Processor - 2GHz or higher (suggested HP DL980 G7 or equivalent)
* 512 GB RAM or higher
* Windows Server x64 2016 with the following components installed:
  + Internet Information Services (IIS)Microsoft .NET Framework 4.5.2
  + All Windows service packs and updates
* SQL Server Enterprise 2016 x64
* SQL Server Reporting Services installed.
* SAN Connected Violin Solid State Storage (7Tb)
* SAN Connectivity for Backup Temporary Storage (14Tb) via Fiber Connectivity.

### Large Scale Production Environment Architecture

![](data:image/x-emf;base64...)

### Storage Configuration

|  |  |  |
| --- | --- | --- |
| Drive | Purpose | Size |
| 1 | CRDM Data 1 | 1.5 TB |
| 2 | CRDM Data 2 | 1.5 TB |
| 3 | CRDM Data 3 | 1.5 TB |
| 4 | CRDM Data 4 | 1.5 TB |
| 5 | CRDM Logs | 1 TB |
| 6 | Secure Application Data | 100 GB |
| 7 | Secure Application Logs and Temp DB Logs | 100 GB |
| 8 | Temp DB Data | TBD |

# Optimal Scale Architecture

## Production Hardware Requirements

The production system will be housed on multiple server machines as described in physical architecture diagram below. The following requirements are meant to be suitable for a production environment; final details will be refined as the full requirements of the solution are solidified.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Machine Name | Description | Cores | RAM | Quantity | Storage |
| Secure Web App | The application tier of the Secure Store environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Web Application servers will host the main web user interface. | 4 | 8 | 2 | OS Recommended Requirement |
| Secure Module Host | The application tier of the Secure Store environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Application servers will perform data processing and loading. | 4 | 8 | 2 | OS Recommended Requirement |
| Secure Report Server | The Reporting Servers in Secure Store environment are deployed virtually running Windows Hyper V Server (VM Ware is also supported). The Reports servers managed the aggregation and delivery of data to filed users and the investigation center within the Secure Application. | 2 | 8 | 2 | OS Recommended Requirement plus 150GB for SSRS |
| Data Loader | The Integration Layer of the Secure Store environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Integration Database servers will host the data processing and loading of flat or xml files, service based data flows and direct table connection from all source data systems. | 4 | 32 | 3 | 750 GB of SAN connected storage for SQL Server Databases and Log Files |
| SAN | Shared Storage for databases and VM images |  |  |  |  |

### Database Servers

The Database servers will act as the main storage repository for all application data. These servers will represent the highest point of contention on the system and therefore need to be adequately sized to ensure effective system performance. Disk, CPU and memory requirements are high and very specific.

Two Servers of the Following Specification

* Intel 10x Multi Core Xeon Processor - 2GHz or higher (suggested HP DL580 G9)
* 512 GB RAM or higher
* Windows Server x64 2016 with the following components installed:
  + Internet Information Services (IIS)
  + Microsoft .NET Framework 4.5.2
  + All Windows service packs and updates
* SQL Server Enterprise 2016 x64
* SQL Server Reporting Services installed.
* SAN Connected Violin Solid State Storage (2Tb)
* SAN Connectivity for Backup Temporary Storage (4Tb) via Fiber Connectivity.

### Optimal Scale Production Environment Architecture ![](data:image/x-emf;base64...)

### Storage Configuration

|  |  |  |
| --- | --- | --- |
| Drive | Purpose | Size |
| 1 | CRDM Data 1 | 500GB |
| 2 | CRDM Data 2 | 500GB |
| 3 | CRDM Data 3 | 500GB |
| 4 | CRDM Data 4 | 500GB |
| 5 | CRDM Logs | 200 GB |
| 6 | Secure Application Data | 100 GB |
| 7 | Secure Application Logs and Temp DB Logs | 100 GB |
| 8 | Temp DB Data | TBD |

# Development Environment Architecture

Sysrepublic recommends sharing the Lab Environment currently built for the Exception Based Reporting project using the same logical configuration as described in the Certification Architecture diagram on the following page. The server inventory for the existing Lab servers is as follows:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Location | MachineType | CPU | RAM | ROLE |
| CTF | VirtualMachine | 2 | 8 | Integration |
| CTF | VirtualMachine | 2 | 8 | Module Host |
| CTF | VirtualMachine | 2 | 8 | Report |
| CTF | VirtualMachine | 2 | 8 | Web Application |
| CTF | Shared DB Server |  |  | Database |

**Development Environment Data Security:**

In the Development environment, the Asset Protection project will use sample files Kroger sales data sources. The data will be PCI compliant; there are no personal identifiers or credit card tokens in the data sources.

## Certification Test Environment Architecture![](data:image/x-emf;base64...)

**Certification Environment Data Security:**

In the Certification environment, the EBR project will use sample files from Production Sales feed. The data will be PCI compliant; there are no personal identifiers or credit card tokens in the data sources. All credit card data is masked.

## Service Accounts and Database Permissions

Sysrepublic requests the following Windows Service account be created for each of the Development, Certification and Production environments described in the proceeding sections:

**Development: Certification: Production:**

DevSecureStoreSVC CertSecureStoreSVC SecureStoreSVC

|  |
| --- |
| Windows Service Account Permissions: |
| Run Services |
| Read, Write, Delete Access to Application directories |
| Read, Write, Delete Access to MSMQ |
|  |
| Recommended level: Local Admin |

|  |
| --- |
| SQK Agent Job Permissions: |
| SQLAgentOperatorRole |

|  |  |
| --- | --- |
| Intergation Databases | Permissions: |
| CRDM\_Staging | SELECT |
|  | UPDATE |
|  | EXECUTE |
|  | DROP |
|  | TRUNCATE |
|  | RESEED |
|  | INSERT |
|  | DELETE |

|  |  |
| --- | --- |
| Application Databases | Permissions |
| ALL | SELECT |
|  | UPDATE |
|  | INSERT |
|  | DELETE |
|  | EXECUTE |
| EXPRESS | DROP TEMP TABLES |
|  | CREATE TEMP TABLES |
|  | ALTER, REBUILD INDEX |
| CRDM | CREATE VIEW |
|  | DROP VIEW |
|  | ALTER PROCEDURE |
|  | ALTER FUNCTION |
|  | SWICTH PARTITION |
|  | CREATE PARTITION |
|  | ALTER TABLE |
|  | CREATE/DROP DEFAULTS |
|  | CREATE/DROP CONSTRAINTS |
|  | CREATE/DROP INDEX |
|  | TRUNCATE ON ARCHIVE SCHEMA |
| CRDM\_CONFIGURATION | TRUNCATE |
|  | ALTER PROCEDURE |
|  | ALTER FUNCTION |
|  | SWICTH PARTITION |
|  | CREATE PARTITION |
|  | ALTER TABLE |
|  | CREATE/DROP DEFAULTS |
|  | CREATE/DROP CONSTRAINTS |
|  | CREATE/DROP INDEX |
| Definitions | CREATE/DROP TEMP TABLES |
| Foundation | CREATE/DROP TEMP TABLES |
| Journal | CREATE/DROP TEMP TABLES |
| Maintenance | CREATE/DROP TEMP TABLES |
| Metadata | TRUNCATE |
|  | CREATE/DROP TEMP TABLES |
| Notifying | CREATE/DROP TEMP TABLES |

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
