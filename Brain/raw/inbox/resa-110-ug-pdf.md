---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/Other Retek Decks/resa-110-ug.pdf.md
tags: [retail, retek, rms, rib, rdm, 2003-2005]
project: retail
status: unprocessed
---

# resa-110-ug.pdf

## Source
File: `Brain/raw/.extract/Other Retek Decks/resa-110-ug.pdf.md`
Size: 140,878 bytes

## Raw content
Retek® Sales Audit™
11.0

User Guide

Corporate Headquarters:

Retek Inc.
Retek on the Mall
950 Nicollet Mall
Minneapolis, MN 55403
USA
888.61.RETEK (toll free US)
Switchboard:
+1 612 587 5000
Fax:
+1 612 587 5100

European Headquarters:

Retek
110 Wigmore Street
London
W1U 3RW
United Kingdom
Switchboard:
+44 (0)20 7563 4600
Sales Enquiries:
+44 (0)20 7563 46 46
Fax:
+44 (0)20 7563 46 10

The software described in this documentation is furnished
under a license agreement, is the confidential information of
Retek Inc., and may be used only in accordance with the
terms of the agreement.
No part of this documentation may be reproduced or
transmitted in any form or by any means without the express
written permission of Retek Inc., Retek on the Mall, 950
Nicollet Mall, Minneapolis, MN 55403, and the copyright
notice may not be removed without the consent of Retek Inc.
Information in this documentation is subject to change
without notice.
Retek provides product documentation in a read-only-format
to ensure content integrity.  Retek Customer Support cannot
support documentation that has been changed without Retek
authorization.
Retek® Sales AuditTM is a trademark of Retek Inc.
Retek and the Retek logo are registered trademarks of Retek
Inc.
This unpublished work is protected by confidentiality
agreement, and by trade secret, copyright, and other laws. In
the event of publication, the following notice shall apply:
©2004 Retek Inc. All rights reserved.
All other product names mentioned are trademarks or
registered trademarks of their respective owners and should
be treated as such.
Printed in the United States of America.

Retek Sales Audit

Customer Support

Customer Support hours

Customer Support is available 7x24x365 via email, phone, and Web access.

Depending on the Support option chosen by a particular client (Standard, Plus, or Premium), the
times that certain services are delivered may be restricted. Severity 1 (Critical) issues are
addressed on a 7x24 basis and receive continuous attention until resolved, for all clients on active
maintenance. Retek customers on active maintenance agreements may contact a global Customer
Support representative in accordance with contract terms in one of the following ways.

Contact Method  Contact Information

E-mail

support@retek.com

Internet (ROCS)   rocs.retek.com

Retek’s secure client Web site to update and view issues

Phone

+1 612 587 5800

Toll free alternatives are also available in various regions of the world:

Australia
France
Hong Kong
Korea
United Kingdom
United States

+1 800 555 923 (AU-Telstra) or +1 800 000 562 (AU-Optus)
0800 90 91 66
800 96 4262
00 308 13 1342
0800 917 2863
+1 800 61 RETEK or 800 617 3835

Mail

Retek Customer Support
Retek on the Mall
950 Nicollet Mall

  Minneapolis, MN 55403

When contacting Customer Support, please provide:

•  Product version and program/module name.

•  Functional and technical description of the problem (include business impact).

•  Detailed step-by-step instructions to recreate.

•  Exact error message received.

•  Screen shots of each step you take.

Contents

Contents

Chapter 1 – Introduction .................................................................. 1

What is Retek Sales Audit?........................................................................................... 1

Purpose of this guide..................................................................................................... 2

Prerequisites.................................................................................................................. 2

Retek Merchandising Solution Set Overview .................................................................... 3

Related documentation.................................................................................................. 4

Chapter 2 – Navigate ReSA ............................................................. 5

Overview....................................................................................................................... 5

Procedures..................................................................................................................... 5

Log on to and exit ReSA .................................................................................................... 5
Navigate within a window.................................................................................................. 5
Sort information ................................................................................................................. 6

Chapter 3 – System variables.......................................................... 7

System variables overview ........................................................................................... 7

Business process................................................................................................................. 7
Reports ............................................................................................................................... 7
System administration ........................................................................................................ 7

Procedures..................................................................................................................... 8

Chapter 4 – Sales Audit maintenance .......................................... 23

Sales audit maintenance overview .............................................................................. 23

Business process............................................................................................................... 23
Reports ............................................................................................................................. 23
System administration ...................................................................................................... 23

Procedures................................................................................................................... 24

Chapter 5 – ACH maintenance ...................................................... 35

Automated clearing house maintenance overview ..................................................... 35

Business process............................................................................................................... 35
Reports ............................................................................................................................. 35
System administration ...................................................................................................... 35

Procedures................................................................................................................... 36

i

Retek Sales Audit

Chapter 6 – Transaction maintenance.......................................... 43

Transaction maintenance overview............................................................................. 43

Business process............................................................................................................... 43
Reports ............................................................................................................................. 44
System administration ...................................................................................................... 44

Procedures................................................................................................................... 45

Chapter 7 – Store/day close audit................................................. 67

Store day close audit overview ................................................................................... 67

Business process............................................................................................................... 67
Reports ............................................................................................................................. 67
System Administration ..................................................................................................... 67

Procedures................................................................................................................... 68

Chapter 8 – Audit trail .................................................................... 73

Audit trail overview .................................................................................................... 73

Business process............................................................................................................... 73
Reports ............................................................................................................................. 73
System administration ...................................................................................................... 73

Procedures................................................................................................................... 74

Chapter 9 – Rule wizards ............................................................... 87

Procedures................................................................................................................... 87

Glossary ........................................................................................ 107

Index .............................................................................................. 159

ii

Chapter 1 – Introduction

Chapter 1 – Introduction

This user guide provides you with the information to effectively use Retek Sales Audit. The
Retek Sales Audit user guide is part of the four-volume Retek Merchandising Solution Set,
consisting of the following user guides:

•  Retek Merchandising System

•  Retek Sales Audit

•  Retek Trade Management

The topics covered in this chapter are:

•  What is Retek Sales Audit?

•  Purpose of this guide

•  Prerequisites

•  Retek Merchandising Solution Set overview

•  Related documentation

What is Retek Sales Audit?
Retek Sales Audit (ReSA) works with Retek Merchandising System (RMS), which is Retek’s
core transaction system. RMS includes key retailing functions such as item maintenance, pricing
and promotion management, supplier and location maintenance, and purchasing and receiving.

ReSA provides a seamless, integrated flow of data from the point-of-sale to major Retek and
other external software. ReSA is designed with flexibility in mind to accommodate varying
business practices by company and retail verticals. User defined audit rules can fine-tune the
system to focus validation on potential problem areas. Wizards are available to develop custom
totals for validation of calculations such as data entry and over/short. Interactive audit
functionality allows auditors to focus on exceptions and helps navigate the auditor through
resolution.

1

Retek Sales Audit

Purpose of this guide
This user guide concentrates on how to use the components of Retek Sales Audit. It provides you
with:

•  Overviews of each functional area within the software, including the business processes,

reports, and system administration functions pertaining to the module.

•  Step-by-step procedures for completing the specific tasks.

Prerequisites
You do not have to have experience using ReSA software to use this guide. You should be
familiar with operating a personal computer (PC), keyboard, and mouse.

Also, verify that all components of ReSA software have been successfully installed.

2

Chapter 1 – Introduction

Retek Merchandising Solution Set Overview

The Retek Merchandising Solution Set is divided into the following volumes. You may refer to
one of the following volumes for specific product information:

Volume 1

Volume 2

Volume 3

Volume 4

Retek Merchandising System
Chapter 1: Introduction
Chapter 2: Navigate RMS
Chapter 3: Foundation data
Chapter 4: Item maintenance
Chapter 5: Purchasing
Chapter 6: Cost management
Chapter 7: Inventory control
Chapter 8: Replenishment
Chapter 9: Financial management
Chapter 10: User tools
Chapter 11: System administration

Retek Sales Audit
Chapter 1: Introduction
Chapter 2: Getting started
Chapter 3: System variable
Chapter 4: Sales Audit maintenance
Chapter 5: ACH maintenance
Chapter 6: Transaction maintenance
Chapter 7: Store/day close audit
Chapter 8: Audit trail
Chapter 9: Rules wizards

Retek Trade Management
Chapter 1: Introduction
Chapter 2: Getting started
Chapter 3: Harmonized tariff schedules
Chapter 4: Letter of credit
Chapter 5: Transportation
Chapter 6: Maintain customs entry
Chapter 7: Maintain obligations
Chapter 8: Maintain actual landed costs

Retek Merchandising Report
Chapter 1: Retek Merchandising System
Chapter 2: Retek Sales Audit
Chapter 3: Retek Trade Management

3

Retek Sales Audit

Related documentation
Additional documentation is available for the core merchandising system. Those documents are
as follows:

Name of Manual

Description

Installation Guide

Operations Guide

Data Model

•  Hardware/software/browser requirements
•  Installation instructions

•  Functional overviews
•  RIB Publication designs
•  RIB Subscription designs
•  Batch designs-
•  Batch program overview

•  Relational integrity diagrams
•  Table names and descriptions
•  Column summaries
•  Primary and foreign keys
•  Check constraints

Online Help

•  Online help available with the  software

4

Chapter 2 – Navigate ReSA

Chapter 2 – Navigate ReSA

Overview
This section describes how to navigate within ReSA. The following topics are included:

•

•

•

Instructions to log on to and exit ReSA

Instructions to navigate within a window

Instructions to sort and filter columns

Procedures

Log on to and exit ReSA
(cid:9)  Note: The way that you access ReSA depends on how the system is set up at your

location. Contact you system administrator for instructions. After you have started ReSA,
you are prompted to log on to the system.

Log on to ReSA

1.

2.

3.

4.

On the Login window, enter your user name in the Username field.

In the Password field, enter your password.

In the Connect String field, enter the connect string for the application.

Click Logon. The Retek Enterprise Start window is displayed.

Exit ReSA

1.  From the Action menu, select Close.

2.  Select Close until the application closes.

Navigate within a window

Use a drop-down list

Some fields can accept values only from a predefined list of options. Such fields have a down
arrow

 button on the right side of the field.

1.  Click the down arrow

 button. A drop-down list of options displays.

2.  Select a value from the drop-down list. The selected option is entered in the appropriate field.

Use a List of Values button

The List of Values
values or options available for the field. The List of Values button is often referred to as a LOV
button.

 button is found to the right of a field. The button displays all defined

5

Retek Sales Audit

Security in lists of value

Lists of values for items and locations are limited by the security levels assigned to your user
group. Other types of lists of values, such as supplier LOVs, are not limited by security levels.

 button. A list of options is displayed.

1.  Click the LOV
(cid:9)  Note: The list of values is empty if no values are defined for the list.
2.  Select an option from the list.

3.  Click OK. The selected option is entered in the appropriate field.
(cid:9)  Note: You may also double click on an option in the list to populate a field.

Sort information

Many windows use column headings that are also buttons. Column heading button are used to
sort table data.

1.  To sort the list, click any column heading button. You can only sort by one column at a time.

2.  To reverse the current sort order, click the same column heading button again.

6

Chapter 3 – System variables

Chapter 3 – System variables

System variables overview
Users gain the most value from software when the system is optimized to meet their needs. The
system variables module provides a means of maintaining the relatively static information about a
retailer's business.

Business process

After you have added the sales audit maintenance information, you can define the information
above as appropriate for your company. The systems variable module allows to set up the
following information for Sales Audit:

•  System options: System validation methods, including escheatment, voucher options, and

information related to the automated clearing house.

•  Error code definitions: Error codes that will appear, and where in Sales Audit that you can

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
