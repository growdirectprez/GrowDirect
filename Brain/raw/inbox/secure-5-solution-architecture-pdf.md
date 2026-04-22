---
date: 2026-04-22
type: raw
source: /Users/gclyle/secure/Secure 5 Solution Architecture.pdf
tags: [secure, secure, loss-prevention, retail]
project: secure
status: unprocessed
---

# Secure 5 Solution Architecture.pdf

## Source
File: `/Users/gclyle/secure/Secure 5 Solution Architecture.pdf`
Size: 33,535 bytes

## Raw content
Secure 5 Solution Architecture.

09/20/2018 Version v2

Contents

1
2

Introduction .....................................................................................................................................3
Software Architecture ......................................................................................................................4
Browser Support .................................................................................................................................. 5
PRESENTATION LAYER .............................................................................................................................. 5
DYNAMIC MESSAGING SERVICE (DMS) ...................................................................................................... 6
SERVICE LAYER ........................................................................................................................................ 6
Data Service Host ................................................................................................................................................6

2.1
2.2
2.3
2.4

3

2.5
2.6

DATA LAYER ........................................................................................................................................... 6
Dependencies ...................................................................................................................................... 7
Typical Architecture..........................................................................................................................8
Server Inventory for Secure ................................................................................................................. 9
3.1.1  Storage and Networking Requirements .............................................................................................. 10

3.1

3.1.2  Remote or SAN based .......................................................................................................................... 10

3.1.3

Local for extreme IO ............................................................................................................................ 10

4

4.1

Architecture Options ...................................................................................................................... 11
Non-Redundant Scale Architecture ................................................................................................... 12
4.1.1  Architecture breakdown ...................................................................................................................... 13

4.1.2  Database Servers ................................................................................................................................. 13

4.2

REDUNDANT ARCHITECTURE ............................................................................................................ 15
4.2.1  Single data center ................................................................................................................................ 15

4.2.2  Cross Data Center Redundancy ........................................................................................................... 16

4.2.3  Architecture breakdown ...................................................................................................................... 18

4.2.4  Database Servers ................................................................................................................................. 18

5
6
7
8

Development Environment Architecture ......................................................................................... 19
Test and Certification Environment ................................................................................................. 19
Service Accounts and Database Permissions .................................................................................... 20
Data Volume .................................................................................................................................. 22
Survey ................................................................................................................................................ 22
8.1.1  Transaction Volume ............................................................................................................................. 22

8.1

8.1.2  Transaction Characteristics ................................................................................................................. 22

9

Document Control .......................................................................................................................... 24
Version ............................................................................................................................................... 24
Reviewers .......................................................................................................................................... 24

9.1
9.2

2 | Proprietary and Confidential

1  INTRODUCTION

The purpose of this document is to describe the Physical Architecture scales available for implementing the
Appriss Retail Platform. The document contains multiple architecture types, to demonstrate how Secure can be
configured in a non-redundant / redundant manner. Variations of this configuration are available and depend
upon Retailers IT governance and sizing. Appriss Retail would work with retailer’s IT Team to determine the best
possible architecture to meet the business needs.

3 | Proprietary and Confidential

2  SOFTWARE ARCHITECTURE

The Secure application architecture includes the following components:

  Client Browser uses Single Page Applications (SPAs) which are web apps developed in JQuery
Framework, HTML5, AngularJS, CSS that render an HTML page with dynamic capabilities. ()

  Presentation Layer is built in the Common Presentation Framework (CPF) leveraging the ASP.NET Stack
  Dynamic Messaging Service (DMS) manages the internal application queues passing messages from the

Web App to the Direct Service Host (DSH).

  Service Layer contains the logic used to create and execute queries and manipulate results. This layer
also contains application logging logic and integration services. (Services are built using Windows .NET
Service solution and C# code.

  Data Layer, which includes databases containing the all transactional and reference data for the scope
of the implementation as well as Case information, configuration settings for the application, and other
application tables.  The current release of all modules on the Secure platform are implemented on the
Microsoft SQL server 2017 DBMS.

The following diagram provides an overview view of the components in each layer

Client Browser

Single Page Applications

Load Balancer

Secure Application

Presentation Layer
Web

Apps

Administration

Reports

Dashboards

Notifications

User Data

Work View

Files

EBR

User Tasks

LP Case
Management

Service Layer
DSH

Cache

Microservices

Jobs
ARDM –
CRDM

Storage Layer

I
I

S

S
e
c
u
r
i
t
y

DMS

MSMQ

Secure

CRDM

MetricBase

FactboardEventStore

Application Tier Scalability

The application tier is deployed on one or
more load balanced virtual application
servers.  Configuration and sizing of the
Application tier is determined based
upon anticipated peak load and  can be
horizontally scaled to meet increasing
demand

Storage Layer Sizing

During implementation the peak load and
transaction volume and retention period
are agreed and the core transactional
data storesfor the application are
established.  Secure application
databases scale dynamically as
application data grows.

4 | Proprietary and Confidential

2.1  BROWSER SUPPORT
Based on the YUI graded browser support, Secure supports three main categories of browser. Secure does not
"feature degrade" like YUI, instead it supports functionally based on the following categories. Grade A, X or C.

All browsers are required to be fully up to date with the latest service packs and updates.

2.1.1.1  Browser Settings

JavaScript (ECMA Script) must be enabled and allowed to run.


  Secure uses fonts to display "image like" characters. This improves performance and reduces network
traffic. Secure should be a trusted site, therefore it is also safe to trust the fonts downloaded from that
site.

2.1.1.2  Grade A Browsers
A-grade browsers are identified, capable, modern and common. QA tests all A-grade browsers, and bugs are
addressed with high priority.

  Microsoft Internet Explorer 10 or later.
  Google Chrome 60 or later

2.1.1.3  Grade X Browsers
X-grade browsers are assumed to be capable and modern. QA does not test, and bugs are not opened against X-
grade browsers.

  Edge
  Firefox 52 or above
  Safari 5 or above
  Opera 18 or above

2.2  PRESENTATION LAYER
In the diagram above, the green layer is the presentation layer which contains the UI. The functions it contains
operates on data fed into the application by the CRDM (Common Retail Data Model) database server.

Standard Secure Platform applications available:

  Administration
  Dashboards
  User Data
  Files
  Reports
  Notifications
  Work View
  User Tasks
  EBR


LP Case Management

5 | Proprietary and Confidential

2.3  DYNAMIC MESSAGING SERVICE (DMS)
Secure Platforms uses DMS in order to pass messages from the Web App to the Direct Service Host (DSH).

2.4  SERVICE LAYER
The service layer comprises of ARP Services. Common Services are those defined outside of the Secure platform
and the Secure Services are those specific to the Secure application. Services are static operations, and these are
used in turn dynamically by the modules. The following services are offered as part of the Secure:

Data Service Host
The Data Service Host (DSH) hosts Appriss Retail databases (SQL), exposes a communication stack and runs as a
Windows Service.

All Data Service and Hosted services runs under a single windows service, under this windows service each
hosted service can be administered.

DSH works on Windows Integrated Authentication. Each operation has a list of groups assigned to it. The
Windows user making the request must be a local or AD group in the list to be granted permission.

Caching
Each web server and data service host in the farm maintains a cache in memory know as a Memory Vault.

Jobs
Secure has a scalable and manageable way to handle work of all kinds of tasks called the Job System. Typical
tasks performed by the job system is loading data from the integration layer into the CRDM

2.5  DATA LAYER
The persistence or data layer provides the means to persist the application data and is split into a number of
logical persistence stores.

Persistence Store
Reference
Case Management
Factboard
Job System
Membership
CRDM
SSO
Notification
Standard Data Load
Stats
Structure
Generic Secure
Schema
Reporting
Work View

Description
Contains client specific reference data; for example, People, Product, Place
The store for all case related data.
The store for all investigation information before it becomes a case
Chronological out of process operations
Users and permissions
The store for the sales transaction data over which Secure operates.
Single Sign On
A store for notifications generated as output of monitors.
Logging progress of data load
For recording metrics, report and search stats
The store for hierarchies; for example, Product and Location
For repository and language resourcing and logging and user activity

Generating reports
Work View Items

6 | Proprietary and Confidential

2.6  DEPENDENCIES
The Appriss Retail Platform (on top of which all our applications operate) was released at the latter end of 2017.
This platform has been engineered from the bottom up using the latest technologies and frameworks including:

  Microsoft .NET Framework 4.7
  ASP.NET MVC 5
  Microsoft SQL Server 2017
  PostgresSQL 10.x
  Python 3.7
  Apache Lucene.NET 4.8
  AngularJS

JQuery
  HighCharts/HighMaps 5.x

7 | Proprietary and Confidential

3  TYPICAL ARCHITECTURE

The following two diagrams depicts the server architecture typically built to host the Client production
implementation of either Secure Store. The infrastructure required can be scaled vertically and horizontally
depending on the volume of data and user needed to access the application.

The diagram shows the components required for Appriss Retail Platform. The Infrastructure described below
assumes components already exist in the Client environment such as Active Directory servers.

Secure Presentation Servers

Virtual Machine
specifications:
Windows Sever 2016 -  VM 50
GB Storage 4 CPU 8 GB Ram
with IIS 8.0 and .net 4.6.2 or
higher

Secure.Domain.com

Web Server

Integration Layer

Secure Database Servers

Data Flow and Mapping

s
u
B
e
c
i
v
r
e
S
e
s
i
r
p
r
e
t
n
E

Ingest Persistance
HPDL380 G10
Windows Server 2016 or Linux
Python 3.7
Postgresql

Virtual Machine
Integration Server specifications:
Windows Sever 2016
VM 150 GB Storage 4 CPU 8 GB Ram
Python 3.7 or higher
MSMQ Services
SFTP or FTP Services
Appriss Retail RTI 2.0

POS Database Server specifications:
HPDL560 G10
Windows Server 2016
Microsoft SQL Server Enterprise 2017

** Inventory Database Server
specifications:
HPDL380 G10 Microsoft Server 2016
Microsoft SQL Server Enterprise 2017

Other Components :
Appriss Retail Service Host
.net 4.6.2 or higher
SMP 2.0 or 3.0 file share
Data Loading Volume

8 | Proprietary and Confidential

3.1  SERVER INVENTORY FOR SECURE

The following table contains the prerequisites components needed on each machine type

Machine Name
Secure Presentation
Servers

Secure Database Server
Store

Application Function
Each machine has a web server
handling all presentation requests for
Secure Application.
Provides the Database Engine and to
the Secure Application.

Integration Layer – Data
Collect

Provides an atomic data loading
function that collects or receives data
for mapping

Integration Layer – Ingest
Persistance

Provides an atomic data loading
function that processes all received
data into the appropriate database
repository.

Software
Microsoft Windows 2016
Microsoft .NET Framework 4.6.2 (or above)
IIS 7.5 or 8.5
Microsoft Windows 2016
Microsoft .NET Framework 4.6.2
**Microsoft SQL Server 2017 Enterprise Edition.
MSMQ Services
File Share Services

Microsoft Windows 2016
Microsoft .NET Framework 4.6.2
Appriss Retail Real Time Integrator (RTI) 4 cores / 8Gb
Python 3.7
MSMQ Service if dealing with a trickle feed
SFTP / FTP or File Share Services depending on
network topology.
Microsoft Windows 2016 or Linux
Python 3.7
Postgresql

** SQL Enterprise Edition is required for both table partitioning and compression features of the software.

9 | Proprietary and Confidential

3.1.1  Storage and Networking Requirements

Appriss Retail has built and specified many Secure infrastructures using a variety of hardware vendors and can
recommend specific options aligned with Client’s preferences. There are usually two types storage architectures
supported

3.1.2  Remote or SAN based

In addition to 'standard' server, network and storage infrastructure. Appriss Retail has worked extensively with

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
