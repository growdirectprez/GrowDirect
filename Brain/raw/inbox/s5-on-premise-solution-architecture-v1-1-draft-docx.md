---
date: 2026-04-22
type: raw
source: /Users/gclyle/secure/S5 On Premise Solution Architecture v1.1 Draft.docx
tags: [secure, secure, loss-prevention, retail]
project: secure
status: unprocessed
---

# S5 On Premise Solution Architecture v1.1 Draft.docx

## Source
File: `/Users/gclyle/secure/S5 On Premise Solution Architecture v1.1 Draft.docx`
Size: 25,632 bytes

## Raw content
Secure 5 Solution Architecture.

09/20/2018 Version (Draft)

#

Contents

[1 Introduction 3](#_Toc525232626)

[2 Software Architecture 4](#_Toc525232627)

[2.1 Browser Support 5](#_Toc525232628)

[**2.2** **Presentation Layer** 5](#_Toc525232629)

[**2.3** **Dynamic Messaging service (DMS)** 6](#_Toc525232630)

[**2.4** **Service Layer** 6](#_Toc525232631)

[**Data Service Host** 6](#_Toc525232632)

[**2.5** **Data Layer** 6](#_Toc525232633)

[2.6 Dependencies 7](#_Toc525232634)

[3 Typical Architecture 8](#_Toc525232635)

[3.1 Server Inventory for Secure 9](#_Toc525232636)

[3.1.1 Storage and Networking Requirements 10](#_Toc525232637)

[3.1.2 Remote or SAN based 10](#_Toc525232638)

[3.1.3 Local for extreme IO 10](#_Toc525232639)

[4 Architecture Options 11](#_Toc525232640)

[4.1 Non-Redundant Scale Architecture 12](#_Toc525232641)

[4.1.1 Architecture breakdown 13](#_Toc525232642)

[4.1.2 Database Servers 13](#_Toc525232643)

[4.2 REDUNDANT ARCHITECTURE 15](#_Toc525232644)

[4.2.1 Single data center 15](#_Toc525232645)

[4.2.2 Cross Data Center Redundancy 16](#_Toc525232646)

[4.2.3 Architecture breakdown 18](#_Toc525232647)

[4.2.4 Database Servers 18](#_Toc525232648)

[5 Development Environment Architecture 19](#_Toc525232649)

[6 Test and Certification Environment 19](#_Toc525232650)

[7 Service Accounts and Database Permissions 20](#_Toc525232651)

[8 Data Volume 22](#_Toc525232652)

[8.1 Survey 22](#_Toc525232653)

[8.1.1 Transaction Volume 22](#_Toc525232654)

[8.1.2 Transaction Characteristics 22](#_Toc525232655)

[9 Document Control 24](#_Toc525232656)

[9.1 Version 24](#_Toc525232657)

[9.2 Reviewers 24](#_Toc525232658)

# Introduction

The purpose of this document is to describe the Physical Architecture scales available for implementing the Appriss Retail Platform. The document contains multiple architecture types, to demonstrate how Secure can be configured in a non-redundant / redundant manner. Variations of this configuration are available and depend upon Retailers IT governance and sizing. Appriss Retail would work with retailer’s IT Team to determine the best possible architecture to meet the business needs.

# Software Architecture

The Secure application architecture includes the following components:

* **Client Browser** uses Single Page Applications (SPAs) developed in JQuery, AngularJS, CSS and Html to render a user Interface with dynamic capabilities.
* **Presentation Layer** is built on the ASP.NET MVC Stack
* **Durable Message Store (DMS)** manages the internal application queues passing messages from the Web App to the Data Service Host (DSH).
* **Service Layer** contains the logic used to create and execute queries and manipulate results. This layer also contains application logging logic and integration services. (Services are built using Windows .NET Service solution and C# code.
* **Data Layer**, which includes databases containing the all transactional and reference data for the scope of the implementation as well as Case information, configuration settings for the application, and other application tables. The current release of all modules on the Secure platform are implemented on the Microsoft SQL server 2017 DBMS, Windows Services and .net.

![](data:image/x-emf;base64...)The following diagram provides an overview view of the components in each layer

## Browser Support

Based on the YUI graded browser support, Secure supports three main categories of browser. Secure does not "feature degrade" like YUI, instead it supports functionally based on the following categories. Grade A, X or C.

All browsers are required to be fully up to date with the latest service packs and updates.

#### Browser Settings

* JavaScript (ECMA Script) must be enabled and allowed to run.
* Secure uses fonts to display "image like" characters. This improves performance and reduces network traffic. Secure should be a trusted site, therefore it is also safe to trust the fonts downloaded from that site.

#### Grade A Browsers

A-grade browsers are identified, capable, modern and common. QA tests all A-grade browsers, and bugs are addressed with high priority.

* Microsoft Internet Explorer 11 or later.
* Google Chrome 60 or later

#### Grade X Browsers

X-grade browsers are assumed to be capable and modern. QA does not test, and bugs are not opened against X-grade browsers.

* Edge
* Firefox 52 or above
* Safari 5 or above
* Opera 18 or above
  1. **Presentation Layer**

In the diagram above, the green layer is the presentation layer which contains the UI. The functions it contains operates on data fed into the application by the CRDM (Common Retail Data Model) database server.

Standard Secure Platform applications available:

* Administration
* Dashboards
* User Data
* Files
* Reports
* Notifications
* Work View
* User Tasks
* EBR
* LP Case Management
  1. **Dynamic Messaging service (DMS)**

Secure Platforms uses DMS as a high performance and volume method to pass messages from the Web App to the Direct Service Host (DSH).

* 1. **Service Layer**

The service layer comprises of ARP Services. Common Services are those defined outside of the Secure platform and the Secure Services are those specific to the Secure application. Services are static operations, and these are used in turn dynamically by the modules. The following services are offered as part of the Secure:

**Data Service Host**

The Data Service Host (DSH) hosts Appriss Retail databases (SQL), exposes a communication stack and runs as a Windows Service.

All Data Service and Hosted services runs under a single windows service, under this windows service each hosted service can be administered.

DSH works on Windows Integrated Authentication. Each operation has a list of groups assigned to it. The Windows user making the request must be a local or AD group in the list to be granted permission.

***Caching***

Each web server and data service host in the farm maintains a cache in memory know as a Memory Vault**.**

***Jobs***

Secure has a scalable and manageable way to handle work of all kinds of tasks called the Job System. Typical tasks performed by the job system is loading data from the integration layer into the CRDM

* 1. **Data Layer**

The persistence or data layer provides the means to persist the application data and is split into a number of logical persistence stores.

|  |  |
| --- | --- |
| Persistence Store | Description |
| Reference | Contains client specific reference data; for example, People, Product, Place |
| Case Management | The store for all case related data. |
| Factboard | The store for all investigation information before it becomes a case |
| Job System | Chronological out of process operations |
| Membership | Users and permissions |
| CRDM | The store for the sales transaction data over which Secure operates. |
| SSO | Single Sign On |
| Notification | A store for notifications generated as output of monitors. |
| Standard Data Load | Logging progress of data load |
| Stats | For recording metrics, report and search stats |
| Structure | The store for hierarchies; for example, Product and Location |
| Generic Secure Schema | For repository and language resourcing and logging and user activity |
| Reporting | Generating reports |
| Work View | Work View Items |

## Dependencies

The Appriss Retail Platform (on top of which all our applications operate) was released at the latter end of 2017. This platform has been engineered from the bottom up using the latest technologies and frameworks including:

* Microsoft .NET Framework 4.7
* ASP.NET MVC 5
* Microsoft SQL Server 2017
* PostgresSQL 10.x
* Python 3.7
* Apache Lucene.NET 4.8
* AngularJS
* JQuery
* HighCharts/HighMaps 5.x

# Typical Architecture

The following two diagrams depicts the server architecture typically built to host the Client production implementation of either Secure Store. The infrastructure required can be scaled vertically and horizontally depending on the volume of data and user needed to access the application.

The diagram shows the components required for Appriss Retail Platform. The Infrastructure described below assumes components already exist in the Client environment such as Active Directory servers.

![](data:image/x-emf;base64...)

## Server Inventory for Secure

The following table contains the prerequisites components needed on each machine type

|  |  |  |
| --- | --- | --- |
| Machine Name | Application Function | Software |
| Secure Presentation Servers | Each machine has a web server handling all presentation requests for Secure Application. | Microsoft Windows 2016  Microsoft .NET Framework 4.7 (or above)  IIS 7.5 or 8.5 |
| Secure Database Server Store | Provides the Database Engine and to the Secure Application. | Microsoft Windows 2016  Microsoft .NET Framework 4.6.2  \*\*Microsoft SQL Server 2017 Enterprise Edition.  MSMQ Services  File Share Services |
| Integration Layer – Data Collect | Provides an atomic data loading function that collects or receives data for mapping | Microsoft Windows 2016  Microsoft .NET Framework 4.6.2  Appriss Retail Real Time Integrator (RTI) 4 cores / 8Gb  Python 3.7  MSMQ Service if dealing with a trickle feed  SFTP / FTP or File Share Services depending on network topology. |
| Integration Layer – Ingest Persistance | Provides an atomic data loading function that processes all received data into the appropriate database repository. | Microsoft Windows 2016 or Linux  Python 3.7  Postgresql |

\*\* SQL Enterprise Edition is required for both table partitioning and compression features of the software.

### Storage and Networking Requirements

Appriss Retail has built and specified many Secure infrastructures using a variety of hardware vendors and can recommend specific options aligned with Client’s preferences. There are usually two types storage architectures supported

### Remote or SAN based

In addition to 'standard' server, network and storage infrastructure. Appriss Retail has worked extensively with leading edge hardware options to provide high performance options for the Secure application. One of these vendors is 'Fusion IO' now ‘Sandisk’. Sandisk provide an Enterprise class high performance solid state storage platform which is ideally suited for the Secure application. The Fusion IO technologies form part of the infrastructure stack that Appriss Retail relies on for our hosted instances of the application.

### Local for extreme IO

Under exceptional circumstances the connectivity fabric between Remote storage and server can become the bottleneck in query performance. With recent advances in newer storage protocol, SSD or NVMe can dramatically reduce this constraint.

The below architecture assumes LAN connectivity of 10Gbe bandwidth between all servers. Storage requires connectivity to the database server via fiber channel at 16Gbe .

# Architecture Options

Secure deployment strategy is very versatile and allows for both Horizontal and Vertical scaling depending on Redundancy requirements, volume of data and the number of users likely to access the application.

Generally Secure is used as a non-mission critical business application, and consequently the architecture can be reduced to match this need. On Premise deployments will be governed by the Retailers IT policies and practices which will alter the approach. The following options show three different ways Secure can be deployed.

For each of the options below, the database servers will contain 1 or many of the server configurations. Appriss Retail procures hardware from HP. Each of the options will list Part numbers we suggest being placed into the server. However, Appriss Retail would expect the retailer to work with its preferred supplier to build a complete Bill of Material for each server.

For each server the following notes should apply

* Number of Front Raisers will need to be confirmed by Retailer’s Hardware Vendor
* The Server will require 10Gbit Network Adapters. The quantity will depend on Retailer’s networking policy and practices
* Appriss Retail would expect the retailer to provide the required resources to backup all the database and instances provided in this document.

## Non-Redundant Scale Architecture

The production system will be housed on multiple server machines as described in physical architecture diagram below. This option demonstrates horizontal scaling of certain roles to manage performance.

![](data:image/x-emf;base64...)

### Architecture breakdown

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Machine Name | Description | Cores | RAM | Quantity | Storage |
| Secure Web App | The application tier of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Web Application servers will host the main web user interface and should be load balanced via a network load balancer | 4 | 8 | 2 | OS Recommended Requirement |
| Secure Service Host | The application tier of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Application servers will perform data processing and loading. | 4 | 4 | 1 | OS Recommended Requirement |
| Integration Servers | The Integration Layer of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Integration Database servers will host the data processing and loading of flat or xml files, service based data flows and direct table connection from all source data systems. | 4 | 8 | 3 | OS Recommended Requirement |
| Integration Servers - Persistence | The Integration Layer of the Secure environment will contain one PostgreSQL instance as a Virtual machine to act as transient staging area. | 4 | 8 | 1 | OS Recommended Requirement. Additional storage would be required for the postgresql instance |

### Database Servers

The Database servers will act as the main storage repository for all application data. These servers will represent the highest point of contention on the system and therefore need to be adequately sized to ensure effective system performance. Disk, CPU and memory requirements are high and very specific.

The following table provides an example set of components Appriss Retail would propose for a database size around 10TB.

|  |  |  |
| --- | --- | --- |
| HP Part Number | Part Description | Quantity Per Server |
| 872770-L21 | Gold 6154 Processor (3.0GHz/18-core) | 4 |
| Part Number unknown | 256 GB (8x 16 GB Registered DIMMs, 2666 MT/s) | 8 |
| 875326-B21 | HPE 960GB SAS 12G 12G Read Intensive SFF (2.5in) SC | 22 |
| 869083-B21 | HPE Smart Array P816i-a SR Gen10 (16 Internal Lanes/4GB Cache/SmartCache) 12G SAS Modular Controller | 1 |

#### Storage Configuration

The storage architecture uses a stripping technique to produce the maximum amount of IO. This is achieved by adding as much spindles to the storage system. In a RAID5 configuration we estimate the amount of storage available on the server will exceed the 10TB required size, however the number of drives is the critical element in gaining the best possible IO.

Additional RAID Controllers maybe required for the quantity of drives. We recommend the retailer works with their hardware vendor to work on the best possible configuration.

## REDUNDANT ARCHITECTURE

The production system will be housed on multiple server machines as described in the physical architecture diagram below. The following requirements are meant to be suitable for a redundant environment spanning many Data Center if needed. The first example expands on from the typical architecture and assumes redundancy in a single data center.

### Single data center

![](data:image/x-emf;base64...)

#### Architecture Breakdown

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Machine Name | Description | Cores | RAM | Quantity | Storage |
| Secure Web App | The application tier of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Web Application servers will host the main web user interface and should be load balanced via a network load balancer | 4 | 8 | 2 | OS Recommended Requirement |
| Integration Servers | The Integration Layer of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Integration Database servers will host the data processing and loading of flat or xml files, service based data flows and direct table connection from all source data systems. | 4 | 8 | 3 | OS Recommended Requirement |
| Integration Servers - Persistence | The Integration Layer of the Secure environment will contain one PostgreSQL instance as a Virtual machine to act as transient staging area. | 4 | 8 | 1 | OS Recommended Requirement. Additional storage would be required for the postgresql instance |

#### Database Servers

Typically, the database will house Appriss Retail Service Host and it’s prerequisites. In the above the architecture these services have been clustered to provide redundancy to the presentation layer.

SQL Server redundancy will come in the form of building a Highly Available Group with the “Always On” feature of SQL Server. Appriss Retail is currently certifying the application with this technology configuration.

### Cross Data Center Redundancy

The second redundancy configuration shows how secure can be setup across multiple data centers. Archetypally Appriss Retail suggests placing as much of the architecture within Virtual Machines and allow VM replication technology manage the syncing between the sites.

![](data:image/x-emf;base64...)

### Architecture breakdown

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Machine Name | Description | Cores | RAM | Quantity | Storage |
| Secure Web App | The application tier of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Web Application servers will host the main web user interface and should be load balanced via a network load balancer | 4 | 8 | 2 | OS Recommended Requirement |
| Secure Service Host | The application tier of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Application servers will perform data processing and loading. | 4 | 4 | 1 | OS Recommended Requirement |
| Integration Servers | The Integration Layer of the Secure environment utilizes virtual servers running Windows Hyper V Server (VM Ware is also supported). The Integration Database servers will host the data processing and loading of flat or xml files, service based data flows and direct table connection from all source data systems. | 4 | 8 | 3 | OS Recommended Requirement |
| Integration Servers - Persistence | The Integration Layer of the Secure environment will contain one PostgreSQL instance as a Virtual machine to act as transient staging area. | 4 | 8 | 1 | OS Recommended Requirement. Additional storage would be required for the postgresql instance |

### Database Servers

There are 4 Database Servers in the above architecture, two in each data center. The Servers must be an identical specification, to meet the Microsoft Clustering prerequisites. The architecture assumes a singles highly available group spanning multiple datacenters.

# Development Environment Architecture

Appriss Retail recommends implementing a development environment for the purpose of landing initial set of application software and local configuration changes. The recommendation would be to follow typical architecture environment

|  |  |  |  |
| --- | --- | --- | --- |
| Machine Type | CPU | RAM | ROLE |
| Virtual Machine | 2 | 8 | Integration |
| Virtual Machine | 2 | 8 | Web Application |
| Shared DB Server |  |  | Database |

**Development Environment Data Security:**

In the Development environment, the Asset Protection project will use sample files sales data sources. The data will be PCI compliant; there are no personal identifiers or credit card tokens in the data sources.

# Test and Certification Environment

In addition to the Secure production environment it is required for two non-production environments to be put in place. The two environments are to act as a test/certification environment, where production changes are tested and a development environment where configuration changes are made to be presented to the user community before signoff.

Both non-prod environments can be fully virtualized and deployed to this platform, the Appriss Retail project team can provide a detailed recommendation for the sizing of non-production environments in line with the testing and IT governance procedures in place during the implementation project.

# Service Accounts and Database Permissions

Appriss Retail requests the following Windows Service account be created for each of the Development, Certification and Production environments described in the proceeding sections:

**Development: Certification: Production:**

DevSecureStoreSVC CertSecureStoreSVC SecureStoreSVC

|  |
| --- |
| Windows Service Account Permissions: |
| Run Services |
| Read, Write, Delete Access to Application directories |
| Read, Write, Delete Access to MSMQ |
| Read, Write, Delete Access to File Shares |
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

# Data Volume

To build a solution Architecture suitable to meet the needs of the retailer, Appriss Retail would perform a sizing exercise to estimate the amount of data required for the application. The following is a survey which Appriss Retail would ask to be filled out for this exercise to commence.

If the retailer is an exciting Appriss Retail customer with an on premise installation, this data can be obtained from the secure application.

## Survey

Below are three tables that used to estimate the potential scope of data volume for a given implementation.

### Transaction Volume

|  |  |  |
| --- | --- | --- |
|  | Daily Average | Peak |
| POS Transactions per store per day | Average Number of Transaction Per day per store | Average Number of Transaction Per day per store during peak periods |
| Items per POS Transaction (Basket Size) | Average Basket Size per Transaction | Average Basket Size per Transaction during peak periods |
| Number of Tender Types used per POS Transaction | Average number of tenders per transaction | Average number of tenders per transaction during peak periods |
| Number of discounted line items per POS Transaction | % of items that contain a discount | % of items that contain a discount during peak periods |

### Transaction Characteristics

The following information could not be estimated, but will only have a marginal effect on the overall sizing result.

|  |  |  |
| --- | --- | --- |
|  | Daily Average | Peak |
| Percent of Transactions with Staff Discounts | The daily average Percentage of Employee Sales and Returns | The daily average Percentage of Employee Sales and Returns during peak periods |
| Percent of Transactions with Loyalty Card | Average % of transactions that contain Loyalty Data | Average % of transactions that contain Loyalty Data during peak periods |
| Percent of Transactions with Age Verification | Average % of transactions that contain age verification | Average % of transactions that contain age verification during peak periods |
| Percent of Transactions with Discounts | Average % of transactions that contain transactional discounts | Average % of transactions that contain transactional discounts during peak periods |
| Percent of Recalled Transactions |  |  |
| # of Transactions Requiring Mgmt Override (Daily) | Average % of transactions that contain operator override or manager override | Average % of transactions that contain operator override or manager override during peak periods |
| Percent of Gift Cards | Average % of transactions that contain a gift card reload , activation or redemption | Average % of transactions that contain a gift card reload , activation or redemption during peak periods |

Upgrade

# Document Control

## Version

|  |  |  |  |
| --- | --- | --- | --- |
| Document Version | Author | Date | Notes |
| 1.0 | Richard Williams | 09/20/2018 | Initial Version |

## Reviewers

|  |  |  |
| --- | --- | --- |
| Reviewed By | Position | Date |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
