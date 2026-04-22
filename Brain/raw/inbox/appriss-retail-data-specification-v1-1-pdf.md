---
date: 2026-04-22
type: raw
source: /Users/gclyle/secure/Appriss Retail Data Specification v1.1.pdf
tags: [secure, secure, loss-prevention, retail]
project: secure
status: unprocessed
---

# Appriss Retail Data Specification v1.1.pdf

## Source
File: `/Users/gclyle/secure/Appriss Retail Data Specification v1.1.pdf`
Size: 103,709 bytes

## Raw content
Appriss Retail Platform
Data Specification Document

5/17/2018 – v1.1

Contents

2

3

3.1
3.2

2.1
2.2

Introduction .....................................................................................................................................4
AUDIENCE AND SCOPE ........................................................................................................................ 4
Data Request Overview ....................................................................................................................... 4
INTEGRATION OPTIONS ..........................................................................................................................4
Batch Processing .................................................................................................................................. 4
Real Time Integration. ......................................................................................................................... 5
POS Transactions ..............................................................................................................................7
Credit Card Tokens and Associated Data ............................................................................................ 7
5  Online Transactions ..........................................................................................................................8
DSD and Inventory ...........................................................................................................................8
6
Reference Data .................................................................................................................................8
7
User Security and Data Access ..........................................................................................................9
8
Hierarchies ........................................................................................................................................... 9

4.1

8.1

4

8.1.1

Locations Level Example ...................................................................................................................... 10

8.1.2

Location Membership Example ........................................................................................................... 11

9

8.2
8.3
8.4

Teams ................................................................................................................................................ 11
Application Use Case ......................................................................................................................... 12
Files Formats ...................................................................................................................................... 13
File Specifications ........................................................................................................................... 14
Files Required .................................................................................................................................... 14
File Naming Conventions ................................................................................................................... 14
File Schemas ...................................................................................................................................... 14
Trigger File ......................................................................................................................................... 14
10  Appendix A .................................................................................................................................... 15

9.1
9.2
9.3
9.4

10.1.1

Operator Action ............................................................................................................................... 15

10.1.2

Header ............................................................................................................................................. 17

10.1.3

Item.................................................................................................................................................. 19

10.1.4

Tender .............................................................................................................................................. 23

10.1.5

Customer ......................................................................................................................................... 25

10.1.6

Item Discount .................................................................................................................................. 28

10.1.7

Transaction Discount ....................................................................................................................... 31

10.1.8

Gift Card ........................................................................................................................................... 33

10.1.9

Loyalty Card ..................................................................................................................................... 35

10.1.10  Recalled Transaction ........................................................................................................................ 37

10.1.11  Age Information ............................................................................................................................... 39

10.1.12  Receipt ............................................................................................................................................. 40

2 | Proprietary and Confidential

11  Appendix B ..................................................................................................................................... 41

11.1.1

Employee ......................................................................................................................................... 41

12  Control ........................................................................................................................................... 48
12.1  Version ............................................................................................................................................... 48
12.2  Reviewers .......................................................................................................................................... 48

3 | Proprietary and Confidential

2  INTRODUCTION

This document describes different integration options Appriss Retail can provides as part of it’s service offering for data
ingestion to its products. The document covers all area in-scope of delivery of the EBR Application that require source data.
This includes

  Sales Data, both POS and Online
  DSD or Store based Inventory
  Reference Data

2.1  AUDIENCE AND SCOPE
This document is intended for the source producer of transactional and reference data for an organization, be that in-house
IT teams or third parties. This document describes different integration options the producer of data can choose from.

2.2  DATA REQUEST OVERVIEW

The Appriss Retail Optimization Platform contains all Appriss Retail products such as Verify, Secure, and Incent.  Since each
retailer’s data is unique, the descriptions contained herein will serve as guidelines for the data being requested.  Before
deciding on finalized requirements, interaction with the data experts at your company will be required.  This request may
be modified depending on the relative difficulty in obtaining the data requested and Appriss Retail is very flexible in the
data requested, data formats and data delivery mechanisms.
Data is requested for at least a twelve-month period for any data tests or product implementation.

3  INTEGRATION OPTIONS

3.1  BATCH PROCESSING
collects and extracts all data in a batch manner and delivers them to the Appriss Retail file servers. The batch can represent
any set of transactions desirable, the most common batching approaches include:

1.  One file per store per day.
2.  One file with transactions from all stores for a period of time (15 minutes, hour)

4 | Proprietary and Confidential

Sales

Reference Data

DSD

Online

POS

Location

Product

Movement

Item
Reference

Online
Orders

TLogs

HR

Overshort

File Share
Or FTP Service

File Share
Or FTP Service

File Share
Or FTP Service

Mapping and Transformation Operations

Secure Integration Layer

CRDM Inventory

CRDM PointOfSale

Secure Reference

As shown above the Appriss Retail Integration would then decrypt the files map the source data to the target schema and
load into the appropriate database.

3.2  REAL TIME INTEGRATION.

1.  The client posts individual transactions to a RESTful web service using HTTP POST method
2.  Alternatively, clients can post batches of transaction containing multiple transactions per HTTP POST call

5 | Proprietary and Confidential

In either of these scenarios we would expect the content of the HTTP POST to be the raw TLOG format provided
by the POS vendor whether that be XML, JSON, Binary or otherwise.

DSD

Sales

Reference Data

Online

POS

Location

Product

Item
Reference

HR

Overshort

Movement

Online
Orders

Sales

Restful
Endpoint

File Share
Or FTP

Restful
Endpoint

File Share
Or FTP

Mapping and Transformation Operations

Secure Integration Layer

CRDM Inventory

CRDM PointOfSale

Secure Reference

As shown above the Appriss Retail Integration would consume the Restful message on to a set of queues for
processing. A separate process would then de-queue the message, map and transform the source data to the
target schema and load into the appropriate database.

6 | Proprietary and Confidential

4  POS TRANSACTIONS

Appriss Retail prefers receiving raw TLOG data for POS data that has not been transformed in any way by the client. This
ensures that data that may be important for identification of exceptions is not lost in the transformation. This document
does not prescribe an interface schema but assumes that the TLOG will be shipped raw using one of the methods previously
described.

Since each retailer is different, we ask that all record types and variables be included within the feed.   The table
below shows a typical list of the types of information provided. (See Appendix A for typical fields found within
each type)

Information Type
Operator Actions

Header
Item
Tender
Customer

Item Discount
Transaction Discount
Gift Card
Loyalty Card
Recalled Transaction

Age Information

Receipt

Information Description
Actions on the register by an employee such as login,
logout, overrides, post voids, voids, etc.
Transaction header information
Item information from a transaction
Payment information from a transaction
Customer information from a loyalty program or
from shipping or other collected information during
a transaction
Discounts at the item level
Discounts at the transaction level
Gift card information
Loyalty accountholder information
Recalled transactions such as recall/suspends,
refunds, or post voids
Age information collected in instances where proof
of age is required (e.g. alcohol purchases)
Information on the receipt (e.g. image)

4.1  CREDIT CARD TOKENS AND ASSOCIATED DATA

Appriss Retail asks that the retailer not provide full credit card account numbers within the data feed.   Appriss
Retail requests that retailers provide a credit card token which uniquely identifies the credit card and is one to
one with the credit card.  One-to-one means that the same credit card will always produce the same token
across multiple transactions, and a provided token will only relate to one credit card versus many credit cards.
Additional fields which should be provided are (1) cardholder’s first and last name, (2) the last 4 digits of the
card number (which is typically the last 4 digits of the token), (3) the type of credit card such as American
Express, Mastercard, or Visa,  (4) the first 6 digits of the credit card number, and (5) the credit card authorization
value.

7 | Proprietary and Confidential

5  ONLINE TRANSACTIONS

Appriss Retail prefers receiving Online transactional data in its native form without any transformation. This ensures data
that may be important for identification of exceptions is not lost in the transformation. Therefore, this document does not
prescribe an interface schema.

To examine and provide the best possible analysis for online related orders Appriss Retail would highly recommend the
following data entities be provided.

Shipment and fulfillment data

  Orders
  Order modifications

  Discounts



Customer Information
Call Center Associate Data

6  DSD AND INVENTORY

A separate document exists by Appriss Retail regarding Inventory related data. This document details the expected data
feeds needed to examine DSD related activity.

The delivery of this data can be performed by either of the methods described above.

7  REFERENCE DATA

Reference data is cross reference information for elements contained within the raw point of sale data.   The
following categories of cross reference data are typically received by Appriss Retail.  (See Appendix B for typical
fields found within each type).

Information Type
Employee cross reference

Store cross reference

Item cross reference

8 | Proprietary and Confidential

Information Description
Provides information about the employee such as
job title, start date, termination date, primary store,
employee ID numbers, home address, etc.
Provides information about the stores such as
organizational hierarchy, store address, manager
information, phone number, open date, store
type/format, etc.
Also known as an item master, this file contains a
unique item identifier such as SKU or UPC, the
product’s hierarchy coded and with descriptions,
brand, cost, etc.

8  USER SECURITY AND DATA ACCESS

The Appriss Retail Platform supports two user authentication method:

  User Authentication
  Single Sign On (SSO)

When SSO is used, the user merely navigates to specified URL to login. The user’s identity and roles will be
passed to the Secure application – if the user is within a role which maps to a Secure role, the user will be logged
into the Secure application automatically without the need to re-enter their Windows logon details. During this
process the correct access privileges are assigned to the user based on content of SSO claim.

This section describes the data that may be required to augment information typically not supplied in the SSO
claim, to assist in the user management, and the use cases this supports.

There are three control components within the Platform for managing access to application functions and data.
These are

  Data Policies: Applies Mandatory Conditions on user searches in the application to limit the results to

the policy definition. Typically set to organizational retail hierarchy.

  Teams: A group of users assigned to the organizational role.
  Groups: A set of application object permissions grouped together to describe a specific job function

within the platform.

All the above control elements required by the platform can be mastered by a series administrative functions if
feeds aren’t easily available.

8.1  HIERARCHIES

The following describes how retail locations are organized to manage permissions and group data for
analysis/reporting by both hierarchies, teams, and groups

Hierarchies involve an organizational scheme using successive ranks or grades with each a level of users.  The
following diagrams shows how the platform organizes a hierarchy into its component parts

Hierarchy

Level(s)

User(s)

Team(s)

Member(s)

Location(s)

9 | Proprietary and Confidential

  Hierarchy: The type of Hierarchy being expressed. Typically, an instance of the platform will have the
organizational hierarchy constructed from the location reference data feed. However, additional
hierarchy can be configured to describe other organizational configurations which may be internal to LP
or other retail business units.
Level: The number of levels defined within the hierarchy. The platform allows for a maximum of 6 levels
per hierarchy to be configured. See the example below
Locations: Is the lowest level possible in the hierarchy and is derived from the locations supplied in the
reference data feed.





  Members: is the association of a user to a level in the Hierarchy.

8.1.1

Locations Level Example

Level 1 : Region

East

West

New York

Florida

California

Washington

Level 2 : State

New York

Miami

Orlando

Los Angeles

San Fransisco

Seattle

Level 3 : City

1

2

3

5

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
