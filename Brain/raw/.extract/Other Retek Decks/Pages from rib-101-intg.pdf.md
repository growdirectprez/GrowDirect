Retek® 10.1 Integration Bus

Integration Guide

Message Interface Overviews

Retek Integration Bus

The software described in this documentation is furnished under a license
agreement and may be used only in accordance with the terms of the
agreement.

No part of this documentation may be reproduced or transmitted in any form
or by any means without the express written permission of Retek Inc., Retek
on the Mall, 950 Nicollet Mall, Minneapolis, MN 55403.

Information in this documentation is subject to change without notice.

Retek provides product documentation in a read-only-format to ensure
content integrity.  Retek Customer Support cannot support documentation
that has been changed without Retek authorization.

Retek® Integration Bus is a trademark of Retek Inc.

Retek and the Retek logo are registered trademarks of Retek Inc.

This unpublished work is protected by confidentiality agreement, and by
trade secret, copyright, and other laws. In the event of publication, the
following notice shall apply:

©2002 Retek Inc. All rights reserved.

All other product names mentioned are trademarks or registered trademarks
of their respective owners and should be treated as such.

Printed in the United States of America.

Corporate Headquarters:

Retek Inc.

Retek on the Mall

950 Nicollet Mall

Minneapolis, MN 55403

888.61.RETEK (toll free US)
+1 612 587 5000

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
Fax:  +44 (0)20 7563 46 10

Retek® Confidential

Customer Support

Customer Support hours:

Customer Support is available 7x24x365 via e-mail, phone and Web access.

Depending on the Support option chosen by a particular client (Standard, Plus, or
Premium), the times that certain services are delivered may be restricted.  Severity 1
(Critical) issues are addressed on a 7x24 basis and receive continuous attention until
resolved, for all clients on active maintenance.

Contact Method

Contact Information

Internet (ROCS)   www.retek.com/support

E-mail

Phone

Mail

Retek’s secure client Web site to update and view issues

support@retek.com

US & Canada: 1-800-61-RETEK (1-800-617-3835)
World: +1 612-587-5800
EMEA: 011 44 1223 703 444
Asia Pacific: 61 425 792 927

Retek Customer Support
Retek on the Mall
950 Nicollet Mall
Minneapolis, MN 55403

When contacting Customer Support, please provide:

•  Product version and program/module name.

•  Functional and technical description of the problem (include business impact).

•  Detailed step by step instructions to recreate.

•  Exact error message received.

•  Screen shots of each step you take.

Contents   i

Contents

Chapter 1 – Introduction......................................................... 1

Message family functional areas ......................................................................... 2

Chapter 2 – Messaging concepts .......................................... 5

Common messaging concepts ............................................................................. 5

Adapters (e*Ways) ..................................................................................................... 5
Publish and subscribe ................................................................................................. 5
Message queue table................................................................................................... 5
Publishing message family manager (MFM) ............................................................. 5
Subscribing APIs ........................................................................................................ 5
TAFRs ........................................................................................................................ 6
RIB message envelope................................................................................................ 6

Application message concepts ............................................................................ 7

RMS – Publishing events ........................................................................................... 7
RCOM - Publishing events......................................................................................... 7
RDM - Publishing events ........................................................................................... 7

Chapter 3 – Message interface overviews ............................ 9

Foundation messages........................................................................................... 9

Vendor ........................................................................................................................ 9
Differentiator identifiers ........................................................................................... 14
Differentiator groups ................................................................................................ 17
User-defined attributes ............................................................................................. 21
Banners ..................................................................................................................... 23
Locations .................................................................................................................. 26
Items ......................................................................................................................... 33
Freight Terms (from financials) ............................................................................... 38
Payment Terms (from financials) ............................................................................. 40
Currency Rates (from financials) ............................................................................. 41
GL Chart of Accounts (from financials)................................................................... 43
Items from Warehouse.............................................................................................. 45
Space Locations........................................................................................................ 47

ii   Retek Integration Bus

Transaction messages ........................................................................................ 49

Purchase order .......................................................................................................... 50
Inbound Work orders................................................................................................ 54
Outbound Work orders ............................................................................................. 57
ASN inbound ............................................................................................................ 59
Receiving.................................................................................................................. 64
Stock orders .............................................................................................................. 67
ASN Outbound ......................................................................................................... 73
Stock order status ..................................................................................................... 78
ATP (available to promise)....................................................................................... 82
Customer Orders – Back order and reserve.............................................................. 85
Customer Sale........................................................................................................... 88
Inventory adjustments .............................................................................................. 90
Pending returns (from a customer order).................................................................. 92
Customer returns ...................................................................................................... 95
Return to vendor ....................................................................................................... 97
Customer order return sale ....................................................................................... 99
SKU Optimization .................................................................................................. 100

Chapter 1 – Introduction

Chapter 1 – Introduction   1

This document summarizes Retek 10.1 messaging integration by functional area.
These functional areas are “Message Families,” and are defined as the common
data, data structures, and messages shared by two or more applications on the
RIB.

In addition to message publication and subscription processing by applications,
the RIB can perform additional intermediate transformation and routing
operations on some messages before making them available to the subscribing
application. These “intermediate adapters” are called “TAFRs”–transformation,
addressing, filtering, and routing. A single TAFR may only transform a given
message, only filter the message, only route it, or combine any of the three
operations. See the Retek Integration Bus Technical Architecture Guide for
detailed descriptions of RIB TAFRs. In this guide, wherever a TAFR operation
takes place in a functional area, it is briefly described.

For each functional area, or message family, there are descriptions of:

•  The publishing application’s components and message documents

•  TAFR operations, if applicable

•  The subscribing application’s components and message documents

Applications involved with Messaging Integration

RMS –

Retek Merchandising System

RDM –

Retek Distribution Management

RCOM –

Retek Customer Order Management

RRS –

Retek Retail Server, This also includes the following products:
Integrator, Design, WebTrack and Retail Commerce.

Streamsoft –  Flowtrak Application. Streamsoft a third party partner of Retek.

2   Retek Integration Bus

Message family functional areas

The following table lists the message family functional areas and the Retek
application that publishes and subscribes to the messages.

Functional Area

Publishing Application

Foundation Data

Subscribing
Application

Banner (channels)

RMS

RCOM

Differentiator Identifiers  RMS

Differentiator Groups

RMS

Items

RMS

RCOM. RDM. RRS
(Retek Retail Server)

RCOM. RDM. RRS
(Retek Retail Server)

RCOM. RDM

Vendor/ Vendor (from
Financials)

RMS. External financials

RCOM. RDM

Stores and warehouses

RMS

Locations

UDAs

RIB

RMS

Freight Terms

External financials

Payment Terms

External financials

RCOM

RDM

RDM

RMS

RMS

Currency Rates

External financials

RMS. RCOM

GL Chart of Accounts

External financials

RMS

Items from Warehouse

Space Locations

RDM

RDM

Streamsoft

Streamsoft

Chapter 1 – Introduction   3

Functional Area

Publishing Application

Transaction Data

Appointments

ASN Outbound

ATP

Customer Order Back
Order Reserve

Customer Orders

Customer Return

Customer Return Sale

Customer Sale

External ASN (ASN
Inbound)

Inventory Adjustments

Inventory Balances

Pending Return

PO Receipts

Purchase Order
(for physical locations only)

RTV

Shipping Method

Stock Order
(allocations and transfers)

Stock Order Status

Work Order (Inbound)

Work Order (Outbound)

RDM

RDM

RMS

RCOM

RCOM

RDM

RCOM

RCOM

RDM, Supplier

RDM

RDM

RCOM

RDM

RMS

RDM

RCOM

RMS

RDM

RMS

SKU Optimization

Streamsoft

Subscribing
Application

RMS

RMS, RCOM

RCOM

RMS

RDM

RCOM

RMS

RMS

RMS

RMS

RMS

RDM

RMS

RDM

RMS

RDM

RDM

RMS, RCOM

RDM

RDM

RDM

