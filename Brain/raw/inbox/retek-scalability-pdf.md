---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/Other Retek Decks/Retek Scalability.pdf.md
tags: [retail, retek, rms, rib, rdm, 2003-2005]
project: retail
status: unprocessed
---

# Retek Scalability.pdf

## Source
File: `Brain/raw/.extract/Other Retek Decks/Retek Scalability.pdf.md`
Size: 17,076 bytes

## Raw content
Retek Scalability

sls-100-techscal

Copyright Notice

  Copyright © 2002 by Retek Inc.

All rights reserved.

Page 2 of 2

No part of this documentation may be reproduced or transmitted in any form or by any means
without the express written permission of Retek Inc., Retek on the Mall, 950 Nicollet Mall,
Minneapolis, MN 55403.

Information in this documentation is subject to change without notice.

Printed in the United States of America.

Retek, Inc.
950 Nicollet Mall
Minneapolis, MN 55403

Retek Confidential Information
Access to this information and documentation is permitted only for its authorized
business purpose by authorized personnel subject to confidentiality and nondisclosure
provisions.
Printed Material Valid Only As of Print Date

Filename:
Retek Scalability.doc
Last Printed:
        5/28/2003 10:57 PM

   Scalability Background:

Page 3 of 3

Retek has built our Applications on a foundation of Oracle with a focus on Scalability. This heritage in
Scalability has provided Retek with the ability to scale from the very small to the very largest or retailers
today. Retek has invested in over 10 benchmarks over the years to prove to our clients and prospects
that our Applications can meet the needs of today, but most importantly tomorrow. This focus has allowed
Retek to gain clients like Best Buy, Gap, Tesco (UK), Ann Taylor, RadioShack, Family Dollar Stores and
the United States Postal Service (USPS).

Each of these clients provides a unique and different challenge to Retek and our Applications. These
challenges include, the United States Postal Service is an organization with very low sku (250 Skus)
count but extremely high number of stores (40,000 Stores), thus requiring Retek to prove we can process
all the transactions in an acceptable timeframe. Family Dollar Stores provided Retek with a very different
problem from USPS; they have extremely high transaction volumes with an above average number of
locations (4,600 Stores). A third example is Best Buy who required an Application with 800 concurrent
Corporate Application users while sales processing is occurring every ten minutes. This dual load on the
machines was easily handled and configured for their implemented. In all of these situations it was
required to provide a solution that could meet the solution effectively.

This required Retek to invest in the ability to deliver a center where we could test to ensure Applications
can achieve these business goals. Retek created the ‘Retek Performance Lab’ which is within the
Worldwide Headquarters of Retek in Minneapolis, Minnesota. The Performance Lab is tasked with
executing internal and external benchmarks on our Applications in the test-to-scale and test-to-volume
benchmark formats. Each test provides different insight into how the Application will function; Retek is
primarily concerned with test-to-scale benchmarks as they are designed to ensure that the Application
does not have any performance limits that would require a different approach to development. These test-
to-scale benchmarks have been very successful in conjunction with test-to-volume testing that is
conducted at the client site at a later date to ensure the client will not encounter any processing impact
once the Application has been implemented.

Since 2000, Retek has invested over $7.5 in people and hardware to ensure this is an asset for all clients
in an on-going manner. This investment can be directly tied back into many of the performance
improvements and tips that have released to our clients over the past few years, no matter their size.

Retek, Inc.
950 Nicollet Mall
Minneapolis, MN 55403

Retek Confidential Information
Access to this information and documentation is permitted only for its authorized
business purpose by authorized personnel subject to confidentiality and nondisclosure
provisions.
Printed Material Valid Only As of Print Date

Filename:
Retek Scalability.doc
Last Printed:
        5/28/2003 10:57 PM

Page 4 of 4

Scalability Tests:

Overview
The following information is a brief overview of the information that is currently available to Retek clients
and internal resources to assist in the performance tuning and scalability of our Applications. Each of the
Benchmarks referenced have detailed documentation that outlines a detailed scope and results of the
benchmark. Please note, some information has been withheld at the request of specific clients.
Additionally, some Benchmarks Retek has performed are not publicly available.

Sales Processing Volume Tests
The goal of the Sales processing tests is to ensure the Application can process the needed transactions
in the time required. The time required is typically based on the business needs and will vary by client and
desires.

Carrefour Benchmark
The goal of this benchmark was to process 16 Million Sales Transactions distributed across 200 Stores in
under 4 hours. This benchmark was configured to include VAT processing.
Retek Applications: Retek Merchandising System 8.0 and Retek Sales Audit 8.0

Eckerd Benchmark
The goal of this benchmark was to process 16 Million Sales Transactions distributed across 200 Stores in
under 3 hours.
Retek Applications: Retek Merchandising System 8.0 and Retek Sales Audit 8.0

Best Buy
The goal of this benchmark was to process all Sales transactions for all Stores every 10 minutes. The
goal was to process 20,000 sales transactions across 450 Stores in under 10 minutes or 80,000 sales
transactions in under 40 Minutes.
Retek Applications: Retek Merchandising System 9.0 and Retek Sales Audit 9.0

United States Postal Service (USPS)
The goal of this benchmark was to process 30 Million Sales Line Items (10 Million Sales Transactions)
distributed across 40,000 Stores in under 8 hours.
Retek Applications: Retek Merchandising System 9.0 and Retek Sales Audit 9.0

Benchmark

Machine

Processors

Summary of Results

Carrefour
Eckerd
Best Buy

HP v2500
IBM-RS6000 S80
HP N4000

32 (440Mhz)
24 (450Mhz)
8 (550Mhz)

USPS

IBM-p680

24 (600Mhz)

Volume to
Process
16 Million
16 Million
80,000
20,000
30 Million

Time (in
minutes)
148
79
20
7
444

Replenishment Process Volume Tests
The goal of the Replenishment test is to ensure the scalability of the Replenishment module of the
Merchandising System. This was to ensure the system could process and generate all of the Vendor to
Store, Vendor to DC and DC to Store within the needed timeline to facilitate the business requirements.

Carrefour Benchmark
The goal of this benchmark was to process 13.776 Million Sku/Locations in under 4 hours.

Retek, Inc.
950 Nicollet Mall
Minneapolis, MN 55403

Retek Confidential Information
Access to this information and documentation is permitted only for its authorized
business purpose by authorized personnel subject to confidentiality and nondisclosure
provisions.
Printed Material Valid Only As of Print Date

Filename:
Retek Scalability.doc
Last Printed:
        5/28/2003 10:57 PM

  Retek Applications: Retek Merchandising System 8.0

Page 5 of 5

Eckerd Benchmark
The goal of this benchmark was to process 13.766 Million Sku/Locations in under 3 hours.
Retek Applications: Retek Merchandising System 8.0

Benchmark

Machine

Processors

Summary of Results

Carrefour
Eckerd

HP v2500
IBM-RS6000 S80

32 (440Mhz)
24 (450Mhz)

Volume to
Process
13.776 Million
13.776 Million

Time (in
minutes)
111
60

User Load Tests
The goal of User Load testing is to ensure the Application Architecture can handle the number of users
required within an Organization. These tests are also designed to ensure the response time of the
Application is acceptable.
A sampling of the User functions performed includes:

a. Manual Item creation
b. Manual Purchase Order creation
c. Manual Receipt of Transfer
d. Query Stock on Hand for item at Stores
e. Manual Promotion creation

Carrefour
The goal of this benchmark was to show the maximum number of on-line users the Retek Merchandising
System could support.
Retek Applications: Retek Merchandising System 8.0

Best Buy
The goal of this benchmark was to prove the scalability of the on-line user aspect of the system. Total
load on all Servers during this test never exceeded 35%.
Retek Applications: Retek Merchandising System 9.0

United States Postal Service (USPS)
The goal of this benchmark was to show the scalability and response times of the Application with many
users with extreme load.
Retek Applications: Retek Merchandising System 9.0

Benchmark

Database Server

Application Server

Machine

Processors

Machine

Processors

Summary of Results

Carrefour

HP v2500

32 (440Mhz)

Best Buy
USPS

Sun 4500
IBM-p680

8 (400Mhz)
24 (600Mhz)

1x HP V2500
2x HP V2250
5x N4000
2x Sun 420

32 (440Mhz)
16 (240Mhz)
8 (440Mhz)
4 (400Mhz)
Included on Database Server

Users
(active and
concurrent)
1,492

Response
time

NA

230
250

< 3 Seconds
<3 Seconds

Retek, Inc.
950 Nicollet Mall
Minneapolis, MN 55403

Retek Confidential Information
Access to this information and documentation is permitted only for its authorized
business purpose by authorized personnel subject to confidentiality and nondisclosure
provisions.
Printed Material Valid Only As of Print Date

Filename:
Retek Scalability.doc
Last Printed:
        5/28/2003 10:57 PM

   Mix Processing Tests

Page 6 of 6

A mixed Benchmark is a test that includes functions from multiple components of the Retek
Merchandising System. This is typically the processing of batch information; such as Sales or
Replenishment at the same time Users are activity on the system. This type of scenario is designed to
show the impact either batch or on-line activity has on the Application resources.

Carrefour
The goal of this benchmark was to show the system performance under batch processing and on-line
(OLTP) activity. To accomplish the Replenishment functionality was tested along with standard OLTP
functions.
Retek Applications: Retek Merchandising System 8.0

Best Buy
The goal of this benchmark was to demonstrate the scalability of Application when Retek Store Systems
users and trickle processing of Sales transactions being executed.
Retek Applications: Retek Merchandising System 9.0 and Retek Store System 9.0

Benchmark

Database Server
Machine  Processors

Application Server

Machine

Processors

Carrefour

HP v2500  32 (440Mhz)

Best Buy

HP rp7400  8 (750Mhz)

1x HP V2500
2x HP V2250
5x N4000
1x HP rp7400
1x Sun Ultra60
(LDAP Server)

32 (440Mhz)
16 (240Mhz)
8 (440Mhz)
8 (750Mhz)
2 (450Mhz)

Users
(active and
concurrent)
1,260

Response
time

Process  and
Volume

Time (in
minutes)

NA

Replenishment
13.776 Million

157

2,000

4,000

6,000

Avg. <.7
Second

Avg. <.7
Second
Avg. <.6
Second

Sales
Processing
 11,260
Sales
 22,320
Sales
 33,480

29

15

14

RPAS Benchmark Summary

Retek’s  Replenishment  Planning  application  has  been  built  upon  Retek’s  Predictive  Application  Server
(RPAS).   The  proven  scalability  of  this  platform  has  been  shown  in  over  thirty  different  real  world
implementations involving a variety of different business applications (Forecasting, Planning, VMI, CPFR).
In addition a variety of performance benchmarks have occurred over the years to validate the scalability
of the RPAS platform under a variety of scenarios.   The following is a summary of a sampling of these
benchmarks and how they relate to questions concerning RPAS performance.

How fast does Retek’s Forecasting Engines perform?

Benchmark

Testing

Machine

Processors  SKUs  Stores

TimeSeries

RDF-IBM
(Drug)
Promote
(Hardlines)
RDF

AutoES

IBM-S80

24 (450 Mhz)

12,000

5000

60 Mliion

Promote

IBM-RS6000

4 (333 Mhz)

4330

1022  4.4 Million

AutoES

IBM-P680  12 (600 Mhz)

109,000

1100  119 Million

Time
(in Minutes)
56

51

30

Retek, Inc.
950 Nicollet Mall
Minneapolis, MN 55403

Retek Confidential Information
Access to this information and documentation is permitted only for its authorized
business purpose by authorized personnel subject to confidentiality and nondisclosure
provisions.
Printed Material Valid Only As of Print Date

Filename:

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
