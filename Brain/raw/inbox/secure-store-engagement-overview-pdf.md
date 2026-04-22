---
date: 2026-04-22
type: raw
source: /Users/gclyle/mnt/nas-archive/Work/Clients/KROGER/Secure Store Engagement Overview.pdf
tags: [secure, secure, kroger, retail, client-implementation]
project: secure
status: unprocessed
---

# Secure Store Engagement Overview.pdf

## Source
File: `/Users/gclyle/mnt/nas-archive/Work/Clients/KROGER/Secure Store Engagement Overview.pdf`
Size: 20,666 bytes

## Raw content
P a g e  | 1

Sysrepublic Secure Store Engagement Overview

Copyright © Sysrepublic Inc 2009

P a g e  | 2

Sysrepublic Secure Store Engagement Overview

This overview documents the phases, activities and participants required to conduct a successful
implementation of Secure.  We’ve leveraged our experience in the market to design an
approach which maximizes results while minimizing the effort required for a successful install;
this guide explains the overall approach.

Secure Engagement Overview – Step by Step guide

Step 1 – Project Kickoff

To get things started:

  Stakeholder Meeting - Review this guide and agree on participants, timelines and

communication.  Typically we suggest that all relevant parties including the key Business
owner, the IT owner and IT resources required to enable the data exchange process.
  Determine source for POS data - Determine the best approach to source your POS data
that will drive the Secure application.  Can we use the raw TLOGS (preferred), or do you
have a Data Warehouse that has all relevant POS information?  Sysrepublic will work
with you on establishing the best data source for the POC.

  Security Review – We will work with your information security team to gain the





necessary approvals for the project, review the technical architecture, and security
policies to ensure we are in compliance with company standards.
Loss Prevention Strategy Session – Develop a full understanding of the LP structure and
strategize how Secure is going to be integrated into loss prevention processes.
IT Project Planning – We will work with the Business and IT project teams to develop the
detailed project plan, identify roles and responsibilities , agree project dependencies
and delivery milestones

Step 2 - POS Data Capture and data mapping

The Secure application resides on an underlying base data model called the Common
Retail Data Model (CRDM).  The CRDM is a common representation of retail Point Of
Sale data; it contains a number of common data entities and fields that are found across
a wide range of POS vendors.  In order to configure CRDM for your business, we require
sample TLOG data and accompanying receipt transactions.   Sysrepublic will develop a
customized data map of your POS data into the CRDM.  We ask for the following inputs during
this phase of the Project:



 POS Application Resource - we require access to someone in your organization who
understands your POS data in detail.  Typically a week to two weeks of intermittent back
and forth coordination is enough when dealing with TLOGS.

Copyright © Sysrepublic Inc 2009

P a g e  | 3

  POS Data - We request a full complement of different transactions that are possible

from your POS.  This could be sourced from your test system or live store data, however
we ask that you include the corresponding receipts or electronic journal output to
ensure we’ve understood and mapped your data correctly.  (See CRDM data mapping
guide for requested data)

  The data collected from source systems should include all transaction types and register
activity that is collected by the RAW TLOG polled from the store.  The specific details will
be agreed during the detailed design phase, however  transaction records should
include the following types of information:

-

Transaction Header, and line item
details

-  Complete tender information
-  Gift card activity (activation and

redemption)
Item and tender Entry Modes
Item voids, refunds and returns
Transaction Discounts
Item Discounts
Staff Discounts

-
-
-
-
-

-

 Promotion and Coupon related
data
-
Tax amount and Tax exemptions
-  Operator actions and related data
-  No sale transactions
-  Manager overrides
-  Miscellaneous and uncategorized

Transaction-level facts
Suspended / Canceled Transactions

-
-  Register transfers

In addition to the POS data referenced above Sysrepublic requests that the following
reference data is provided to assist our mapping effort:

-  Register Location Codes
-
POS department Codes
-
Item and Store master data
-  Cashier Manual
-

Supplier / Franchisee Guides

  Transaction Reconciliation Report – As we progress through the mapping exercise it is
useful to have a secondary source of transaction counts in order to verify the accuracy
of the load process and that we can balance POS transactions.   We will work with an IT
or Business resource to define the specific parameters of such a reconciliation in your
environment.

  For any custom data feeds that we integrate into Secure, we will also require detailed
technical specification of the source data feed and sample data to begin development
work on integrating these additional data sources.

Step 3 – Source the Data

Sysrepublic requires a sample set of transaction data from Production.  We prefer to
take this offsite into our development environment for efficiency, but can work onsite
as well.  We will work with your networking and application teams to identify how and
where the data will be transferred, and begin to offload that data into our repositories

Copyright © Sysrepublic Inc 2009

P a g e  | 4

or an onsite archive.  This approach allows us to have historical data in the system from
day one and speeds the roll out once the Secure application is installed and configured
to your requirements.  In order to do this, we need the following:



Infrastructure and Network Resource:   We need to determine how application data
being loaded into Secure can be captured and securely transferred to the Sysrepublic
data center.

  Security Clearance:  Sales data is sensitive data in any retail organization, we need
information security approval before initiating any transfers or storage of data
  Transfer Method:  We will agree the secure transfer protocol and test connection

between our data centers.

  Operational daily feeds of Tlog data and other data sources included in the project

scope.

Step 4 – Build the Infrastructure

Our engineers will develop the server hardware and storage configuration based upon
your input into our standard capacity planning exercise.  Once completed, we review
that architecture agreeing on the number of environments and discussing some
configuration options and then develop a plan for procurement and install of the
system.

With onsite implementations we will perform the sizing and participate in solution
planning exercises to develop a Hardware configuration specific to your needs.  We will
then work with your IT resources to agree on how the environments are provisioned
and roles and responsibilities for the actual deployment of the solution.

What we need from you:

  Transaction Details - We ask that you provide us with detailed information about the

data you have available in your Tlogs, the number of stores, number of transactions per
day, number of items, etc.

  Agreement on the retention period and storage parameters of the data
  Network and Application Systems resources to plan the data integration strategy and

data transfer mechanism

Step 5 – Build the Risk Dictionary / Develop the Analysis Structure

After loading the transactional data we begin to configure the Risk Dictionary within Secure
application to target the goals of your organization.   Sysrepublic has proven data analysis
techniques to look for fraud in your organization.  Our client support team will work with
you to understand your business policies, and then marry that information with our analysis
techniques to begin targeting potential areas of risk such as scan avoidance, refunds,

Copyright © Sysrepublic Inc 2009

P a g e  | 5

markdowns, and gift card abuse, using Secure.  As we identify trends in the data, we continue
loading current transactions to validate our analysis and target irregular activity as it occurs.

What we need from you:

  A resource knowledgeable in your company’s business policies at the POS
  Policy and functional details about pricing rules, promotional  campaigns, coupons
  Details about specific PLUs, or UPC’s that support generic rings or other processes

associated with the Risk Dictionary

Step 6 – Acceptance Testing / Deliver results

Generally within a week to two weeks after the Risk Dictionary is configured and system is tuned
on production data, we will our begin acceptance testing the application with your business
team.  We will organize a training session for the user s and hand over the application from the
deployment team to our support organization

What we need from you:



Loss Prevention professional to review the results, assist in fine tuning the application,
investigate and confirm fraud or process inefficiencies identified by Secure.

  A super user / user community to work with developing training materials and defining

the training requirements

  Depending on the type of install and the service levels agreed in the Secure Master

Services Agreement, we will work within your Support Organization to develop a plan
for the help desk and support matrix.

Copyright © Sysrepublic Inc 2009

P a g e  | 6

Project Resources

A successful Secure Implementation project requires some key input from Subject Matter
Experts with the organization.  The following table outlines the skills necessary:

  Group

Project Steering
Committee

Roles

  Client Business Sponsors

  Sysrepublic Engagement Managers

Project Management

  Client Project Manager

Client  Project
Resources

  Sysrepublic Project Manager

  Business Subject Matter Expert (SME)

-

Loss Prevention

-  Store Operations

  Information Technology

-  Data Integration

-  Security & Networking

-  Store Systems

-  SME on any additional source systems
(Merchandizing, HR, Supply Chain)

Sysrepublic
Resources

  Infrastructure / Data Center

  Data Integration Lead

  Training Lead

Copyright © Sysrepublic Inc 2009

Sample Project Timeline

P a g e  | 7

8
1
k
e
e
W

7
1
k
e
e
W

6
1
k
e
e
W

5
1
k
e
e
W

4
1
k
e
e
W

3
1
k
e
e
W

2
1
k
e
e
W

1
1
k
e
e
W

0
1
k
e
e
W

9
k
e
e
W

8
k
e
e
W

7
k
e
e
W

6
k
e
e
W

5
k
e
e
W

4
k
e
e
W

3
k
e
e
W

2
k
e
e
W

1
k
e
e
W

d
e
e
r
g
A
e
n

i
l

e
m
T
,

i

h
c
a
o
r
p
p
A

:
f
f
o
k
c
i
K
t
c
e
o
r
P

j

l

i

g
n
n
n
a
P
e
r
u
t
c
u
r
t
s
a
r
f
n

I

/

y
t
i
c
a
p
a
C

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
