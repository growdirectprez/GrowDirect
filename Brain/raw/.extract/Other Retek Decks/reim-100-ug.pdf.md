Retek® Invoice Matching
10.0

User Guide

Retek Invoice Matching

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

Retek® Invoice Matching™ is a trademark of Retek Inc.

Retek and the Retek logo are registered trademarks of Retek Inc.

Corporate Headquarters:

Retek Inc.

Retek on the Mall

950 Nicollet Mall

Minneapolis, MN 55403

888.61.RETEK (toll free US)
+1 612 587 5000

European Headquarters:

©2002 Retek Inc. All rights reserved.

All other product names mentioned are trademarks or registered trademarks
of their respective owners and should be treated as such.

Printed in the United States of America.

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

Customer Support

Customer Support hours:

8AM to 5PM Central Standard Time (GMT-6), Monday through Friday,
excluding Retek company holidays (in 2002: Jan. 1, May 27, July 4,
July 5, Sept. 2, Nov. 28, Nov. 29, and Dec. 25).

Customer Support emergency hours:

24 hours a day, 7 days a week.

Contact Method  Contact Information

Phone

US & Canada: 1-800-61-RETEK (1-800-617-3835)
World: +1 612-587-5000

Fax

(+1) 612-587-5100

E-mail

support@retek.com

Internet

Mail

www.retek.com/support
Retek’s secure client Web site to update and view issues

Retek Customer Support
Retek on the Mall
950 Nicollet Mall
Minneapolis, MN 55403

When contacting Customer Support, please provide:

•  Product version and program/module name.

•  Functional and technical description of the problem (include business

impact).

•  Detailed step by step instructions to recreate.

•  Exact error message received.

•  Screen shots of each step you take.

Contents

Chapter 1 – Introduction......................................................... 1

What is Retek Invoice Matching? ....................................................................... 1

Purpose of this guide ........................................................................................... 2

Prerequisites ........................................................................................................ 2

Retek Merchandising Solution Set overview ...................................................... 3

Related documentation........................................................................................ 5

Chapter 2 - Getting started ..................................................... 7

Log on to and exit the system.............................................................................. 7

Navigation ........................................................................................................... 8

Window tools .................................................................................................... 10

Access the online help....................................................................................... 14

Contents.................................................................................................................... 15
Index ......................................................................................................................... 16
Search ....................................................................................................................... 17

Chapter 3 - Invoice matching ............................................... 19

Overview ........................................................................................................... 19

Invoice matching options.......................................................................................... 19
Invoice types............................................................................................................. 19
Item structure............................................................................................................ 20

Business process................................................................................................ 21

Merchandise invoice................................................................................................. 21
Consignment merchandise invoice........................................................................... 21
Non-merchandise invoice ......................................................................................... 22
Direct store delivery and invoice of merchandise .................................................... 22
Direct store delivery and invoice of a service .......................................................... 22
Invoice creation through Retek Trade Management ................................................ 22

ii   Retek Invoice Matching

Reports .............................................................................................................. 23

System administration ....................................................................................... 23

Procedures ......................................................................................................... 24

Index....................................................................................... 39

Chapter 1 - Introduction   1

Chapter 1 – Introduction

This user guide provides you with the information to effectively use the Retek
Invoice Matching application. The Retek Invoice Matching user guide is part of
the four-volume Retek Merchandising Solution Set, consisting of the following
user guides:

•  Retek Merchandising System

•  Retek Sales Audit

•  Retek Trade Management

•  Retek Invoice Matching

The topics covered in this chapter are:

•  What is Retek Invoice Matching?

•  Purpose of this guide

•  Prerequisites

•  Retek Merchandising Solution Set overview

•  Related documentation

What is Retek Invoice Matching?

Retek Invoice Matching (ReIM) works with Retek Merchandising System (RMS),
which is Retek’s core transaction system. RMS includes key retailing functions
such as item maintenance, pricing and promotion management, supplier and
location maintenance, and purchasing and receiving.

ReIM provides accurate and efficient verification of supplier invoices against
actual merchandise quantities received at purchase order cost (receivers). ReIM
attempts to automatically match invoices with receivers within user-defined
tolerance limits. Matched invoices are passed to the retailer’s accounts payable
system for payment without user intervention. Discrepant invoices, that is those
not matched with corresponding receivers, can be resolved through system-
generated documents such as debit memos and credit notes request or force-
matched and exported to the accounts payable system for payment.

2   Retek Invoice Matching

Purpose of this guide

This user guide concentrates on how to use the components of Retek Invoice
Matching. It provides you with:

•  Overviews of each functional area within the application, including the

business processes, reports, and system administration functions pertaining to
the module.

•  Step-by-step procedures for completing the specific tasks.

Prerequisites

This user guide makes no assumption about your experience using the ReIM
software application. It does assume the following:

•  You are familiar with operating a personal computer (PC), keyboard, and

mouse.

•  You are familiar with Microsoft Windows 98 operating systems or higher

and Internet Explorer 5.0 web browser or higher.

•  All components of the software application have been successfully installed.

Chapter 1 - Introduction   3

Retek Merchandising Solution Set overview

The Retek Merchandising Solution Set is divided into the following four
volumes. You may refer to one of the following volumes for specific product
information:

Volume 1

Retek Merchandising System

Chapter 1: Introduction

Chapter 2: Getting started

Chapter 3: Foundation data

Chapter 4: Item maintenance

Chapter 5: Purchasing

Chapter 6: Price management

Chapter 7: Inventory control

Chapter 8: Replenishment

Chapter 9: Financial management

Chapter 10: User and grouping tools

Chapter 11: System administration

Volume 2

Retek Sales Audit

Chapter 1: Introduction

Chapter 2: Getting started

Chapter 3: Foundation data

Chapter 4: Automated totaling

Chapter 5: Automated audit

Chapter 6: Import and export data

Chapter 7: Interactive audit

Chapter 8: Audit trail

4   Retek Invoice Matching

Volume 3

Retek Trade Management

Chapter 1: Introduction

Chapter 2: Getting started

Chapter 3: Harmonized tariff schedules

Chapter 4: Letter of credit

Chapter 5: Transportation

Chapter 6: Customs entry

Chapter 7: Obligations

Chapter 8: Actual landed costs

Volume 4

Retek Invoice Matching

Chapter 1: Introduction

Chapter 2: Getting started

Chapter 3: Invoice matching

Chapter 1 - Introduction   5

Related documentation

Additional documentation is available for the core merchandising system. Those
documents are as follows:

Name of Manual

Description

Installation Guide

•  Hardware/software/browser

requirements

•

Installation instructions

Operations Guide

•  Dataflows within RMS

•  Dataflows between RMS and other

Retek products

•  Dataflows between Retek products

and third-party software applications.

•  Functional overviews of batch

programs.

•  Detailed designs of batch modules.

Data Model

•  Relational integrity diagrams

•  Table names and descriptions

•  Column summaries

•  Primary and foreign keys

•  Check constraints

Online Help

•  Online help available with the

application

Chapter 2 – Getting started   7

Chapter 2 - Getting started

This chapter shows you how to log on to and exit the system. An introduction to
the navigation and help features is also provided.

Log on to and exit the system

How you access the system depends on how the system is set up at your location.
Contact your system administrator for instructions. After you have started the
system, you are prompted to log on.

Log on to the system

1  On the RMS Logon window, enter your user name in the Username field.

RMS Logon window

2

In the Password field, enter your password.

3

In the Connect String field, enter the name of the database that you want to
access.

4  Click Logon. The Retek Enterprise Start window is displayed.

Exit RMS

(cid:194) Navigate: From the Action menu, select Close.

Action menu

•  Repeat this action until all the windows are closed and the program closes.

8   Retek Invoice Matching

Navigation

After you log on to the system, the main menu is displayed within the Retek
Enterprise Start window. Until you are familiar with the main menu setup, you
may find it easier to use the search feature in order to find an element.

Search for a folder or element on the main menu

1  On the Retek Enterprise Start window, enter a partial description of the

folder or element in the Search field.

Retek Enterprise Start window

2  Click the Search Forward

 button or the Search Backward

 icon.

3  When prompted that the folder or element has been found, click OK.

4

If the folder or element is not the one you want, click the Search Forward

button or the Search Backward

 button to continue the search.

5  When the desired folder or element is found, you can:

(cid:131)  Select the folder to display its contents. The subfolders and elements are

displayed on the right side of the window.

(cid:131)  Select the element and click Open. An element is most often a window
(also referred to as form). An element can also be a Web page, an
internal item, a user application, or an Oracle report.

Chapter 2 – Getting started   9

Access the options on the menu bar

The menu bar is located near the top of the application window. It provides
access to menus that are specific to the window that is currently displayed.

(cid:194) Navigate: On the menu bar, select the menu. A list of options is displayed.

•  Select the desired option.

The menu options may cause another window to open or some action to
occur. Some of the possible actions include:

(cid:131)  Access to another task that is related to the current task is provided

(Options menu).

(cid:131)  A predefined set of fields replaces the fields that are currently displayed

on a table (View menu).

(cid:131)  The currency in which monetary amounts are displayed is changed

(Options menu).

In the Items module, several windows have an Options list displayed on the left
side of the window. Each option is a hyperlink that provides access to another
window related to the current task. Click on the hyperlink to access the window.

Navigate a window

Generally, you press the tab key in order to move from field to field within a
window. You can also click on a field in order to place the cursor there.

You can use the mouse or the keyboard to activate a button on a window. The
label on most buttons contains one underlined letter. You can press the Alt key
plus the underlined letter on the keyboard in order to activate the button. If you
prefer to use the mouse, you can click the button.

10   Retek Invoice Matching

Window tools

There are several tools within a window that you should become familiar with.
These tools simplify the data entry process.

List of Values button

The List of Values (LOV)
Click the LOV button to display the popup window. You choose the appropriate
value from the popup window that displays the results of the query. The LOV

 button queries the database for a list of values.

 button is found to the right of a field. If the field is a two-part field where the

first field requires an ID or code and the second field requires a description, the

LOV

 button is found between the two fields.

List of Values window

(cid:194) Navigate: Click the LOV

 button to begin the query. A List of Values

window displays the results of the query.

1  Select a value from the list.

2  Click OK. The selected value is entered in the text field or fields.

For some fields, usually item fields, you are prompted to enter a partial
description before the query can begin. This reduces the results to a more
manageable number.

Chapter 2 – Getting started   11

Drop-down list

Some fields can only accept values from a predefined list of values. Such fields
have a down arrow button to the right of the text field.

1  Click the down arrow button.

Drop-down list

2  Select a value from the drop-down list. The value is entered in the data entry

field.

12   Retek Invoice Matching

Calendar button

The calendar button allows you to view a monthly calendar and select a date.

 button to display the calendar. The button is found to the
Click the calendar
right of a date field. When you select a date from the calendar, you need not be
concerned about the format of the date. The system enters the date for you in the
correct format.

Date Entry window

1  Click the calendar
month and year.

 button. The Date Entry window displays the current

2  To display a preceding or succeeding month, click the left arrow

 button

or right arrow
month field and select the month from the drop-down list.

button. You can also click the down arrow button by the

3  To display a different year, click the down arrow next to the year field and

select the year from the drop-down list.

4  Select a date. The value is entered in the date field.

Chapter 2 – Getting started   13

Comments button

The comments button displays a text editor in which you can enter an extensive
note or description. The button is found to the right of a text field.

Comments window

1  Click the comments

 button. The Comments window is displayed.

2  Enter the note.

3  Click OK to exit. The value is entered in the text field. If the note is longer
than the length of the text field, only the first part of the note is displayed.

14   Retek Invoice Matching

Access the online help

The online help can be accessed in the following ways:

•  From the Help menu on the menu bar, select Contents. The Online Help

overview is displayed.

•  Click the help

 button on the toolbar. Context sensitive help is displayed

for the window, which describes how the window helps you accomplish your
task.

There are three types of help topics: window topics, procedure topics, and
overview topics. The window topics provide you with a brief overview of the
window, field descriptions, button descriptions, and procedures related to the
window. The procedure topics provide you with the step-by-step instructions on
how to complete your task. The overview topics provide you with a module
overview, business process, report descriptions, and system administration
parameters related to the module.

You can look for topics by using one of the three help tools: Contents, Index, or
Search.

Chapter 2 – Getting started   15

Contents

The Contents tab displays the overview and the key procedures for each module.
The overview section describes the major functions of the module. The key
procedures provide you with the step-by-step instructions on how to complete
your task.

Online Help – Contents tab

16   Retek Invoice Matching

Index

The Index tab allows you to search the help by entering a keyword. The Index tab
provides a list of keywords in alphabetical order. To access a topic:

1  Scroll through the list and select a topic, or enter the keyword you are

looking for.

2  Click Display, found at the bottom on the index panel.

3  When you select a keyword associated with multiple topics, the topics are
listed in the Topics Found window. Select a topic and click Display. The
topic is displayed on the right half of the window.

Online Help – Index tab

Chapter 2 – Getting started   17

Search

The Search tab allows you to search the help by entering a word. The Search tab
lists all topics that contain the specified word.

1  Enter the word you are looking for.

2  Click Find found at the top of the search panel.

3  Select a topic, and click Display, found at the bottom on the search panel.

The topic is displayed on the right half of the window.

Online Help – Search tab

Chapter 3 – Invoice matching  19

Chapter 3 - Invoice matching

Overview

Retek Invoice Matching (ReIM) compares and matches supplier invoices against
corresponding receipts from shipments. Invoice matching uses a set of cross-
reference numbers, including receipt numbers, purchase order numbers,
locations, and/or advance shipping notice (ASN) numbers.

Invoice matching options

Invoice matching is performed in two ways.

•  Automatic invoice matching: ReIM batch processes automatically match as
many invoices as possible without user intervention. Matches are first
attempted at the summary invoice level; that is, the total cost and quantity of
the invoice is matched with the total cost and quantity of receipts. If a
summary level match is not made, a detail level match is attempted, in which
each item on the invoice is matched with an item on a receipt.

•  Manual invoice matching: Invoices can be manually matched at both the
summary and detail levels. When an invoice is partially matched with a
purchase order and advanced shipment notice, future receipts from the
referenced purchase orders and advanced shipment notices are automatically
associated with the merchandise invoice.

Invoice types

ReIM supports several types invoices:

•  Merchandise invoices: Merchandise invoices are for merchandise from a
supplier. Merchandise invoices are generally matched to receipts from
purchase orders or advanced shipment notices. Merchandise invoices may
include non-merchandise costs as well.

•  Consignment merchandise invoices: The supplier legally owns the

merchandise until the retailer sells the items.

•  Non-merchandise invoices: Sent by suppliers or partners for costs such as

taxes and freight, or services performed by the vendor for a store. This type
of invoice cannot include merchandise.

20   Retek Invoice Matching

•  Direct store delivery (DSD) and invoice of merchandise: Used to deliver

merchandise and/or services to a store without the benefit of a pre-approved
purchase order.

•  Direct store delivery and invoice of a service: Allows the creation of invoices
for services provided for a store. An invoice for a service is also considered
at non-merchandise invoice.

•

Invoice creation through Retek Trade Management (RTM): Uses RTM
software to create an invoice.

Item structure

The RMS item structure allows you to define three levels for managing RMS
data. Each item that is added to RMS is associated with one of three levels. Also,
you must specify the level that you will use to track transactions for that item.
Specifying a transaction level determines at which level stock, cost, average cost,
pricing, and all other transactions will occur within RMS. Cost, however, is
carried at the item/supplier/country/location level.

Levels above the transaction level serve as grouping mechanisms (i.e., "Parents"
and "Grandparents") by which users view information such as stock and sales.
Levels below the transaction level serve as a reference (i.e. PLU or UPC) to the
item that it is beneath. This number can be used as a lookup number and is
available in all unit movement transactions (e.g. ordering, receiving, transfers,
inventory adjustments, and physical counts) as well as to the Point of Sale (POS).

The user also defines what type of identifying number is used at each level within
an item. Possible choices include an internal nine-digit number, UPC-A, UPC-E,
Variable Weight UPC, EAN13, EAN8, ISBN, or Commodity Code (PLU). It is
assumed that all items are unique within the system regardless of the number
type. The length of the item identifier field is 25 characters.

Chapter 3 – Invoice matching  21

Business process

An invoice is received from a supplier, either on paper or via electronic data
interchange (EDI). ReIM automatically matches as many invoices as possible
without user intervention. Automatic matching is first performed at the summary
invoice level, if a match cannot be achieved, it will attempt to match detail line-
level data. Unmatched items remain in that status until they are completely
matched to receipts or resolved.

Discrepancies may be resolved by creating a debit memo or requesting a credit
note for the difference from the supplier. Otherwise, you can force-pay an
unmatched or partially matched invoice, marking the invoice as ready for
payment, even if it is not tied to any matching receipts.

Once an invoice is matched, or the discrepancy resolved, it is exported to your
accounts payable system for payment.

Types of invoices are as follows:

Merchandise invoice

Invoices remain unmatched until all items on the invoice are matched with a
receipt, until the discrepancies are resolved, or until the invoice is force paid.
Discrepancies can be resolved through debit memos, credit notes (in response to
credit note requests), and credit memos.

When an invoice is force paid, it is marked as 'ready to be paid', even though the
invoice is unmatched or partially matched. Once an invoice is matched or marked
as ready to be paid, the invoice is posted to a staging table. The invoice is then
posted to a financial application, such as Oracle Finance 11i.

Consignment merchandise invoice

Consignment invoices are created automatically from the upload from the store's
point of sale system. Consignment invoices are created at the supplier/department
level. Consignment invoices are created with a status of Matched.

22   Retek Invoice Matching

Non-merchandise invoice

Non-merchandise invoices can be created four ways:

•  Manually through the Invoice Header Details window [invoice.fmb].

•  Automatically through the invoice batch upload [ediupinv.pc].

•  Automatically through the ReSA batch upload [saexpim.pc].

•  Automatically through Trade Management.

Note: Non-merchandise invoices go through the same approval process that
merchandise invoices go through.

Direct store delivery and invoice of merchandise

Purchase orders are created based on what the supplier or vendor determines the
store needs. When the invoice is not paid at the store, a paper invoice is usually
sent to the retailer's corporate office. Stores can pay DSD invoices directly. When
the retailer is using ReSA, invoices are then created automatically with a status of
Matched through an upload to ReIM.

Direct store delivery and invoice of a service

This process is similar to the DSD of merchandise in that retailers can create
purchase orders, receipts, and invoices. If the retailer is using ReSA, when stores
can pay DSD invoices directly, invoices are then created automatically with a
status of Matched through an upload to ReIM. Depending on the invoicing
attributes of a supplier, an invoice for a service cannot be paid until the store
confirms the service has been performed. Services can be verified using the
Service Confirmation by Store Window (svcconf.fmb).

Invoice creation through Retek Trade Management

See Retek Trade Management (RTM) documentation for the business process
related to this type of invoice creation.

Reports

Chapter 3 – Invoice matching  23

The following reports relate to Invoice Matching:

Activity by User ID: Displays invoice details by user ID.

Forced Paid Invoices by Supplier: Displays invoice details by supplier.

Matched Invoices by Supplier: Displays matched invoices by supplier.

Standard Debit/Credit Print Out: Displays invoice cost details, such as the
item number and description, unit cost, VAT rate, and quantity.

Unmatched Receipts by Supplier: Displays unmatched receipts.

Unmatched/Partially Matched Invoices by Supplier: Displays partially and
unmatched invoices by supplier.

System administration

The system administrator can set the following options for invoice matching:

•

Invoice Matching Indicator: When selected, indicates that invoice
matching functionality is enabled.

•  Match Invcs to Rcpts from Other Suppliers: When selected, indicates that

invoices can be matched to receipts from other suppliers.

•  Match Total Quantity: When selected, indicates that when summary level
invoice matching occurs, whether automatic or manual, invoices must be
matched at both quantity and cost levels. If this indicator is not selected, only
the total cost of the invoice and receipt must match in order for the invoice to
be considered matched. The total quantity is not considered.

•  Debit Memo Send Days: Indicates the number of days prior to the invoice
due date that a debit memo should be sent if a credit note has not been
received.

•  Max Debit Memo Percent: Indicates the maximum percentage of an invoice

that a debit memo can be before a warning is issued.

•  Close Open Shipment Days: Indicates the number of days that a shipment

can remain in unmatched to an invoice before it is closed.

24   Retek Invoice Matching

Procedures

Add a default invoice matching tolerance

(cid:194) Navigate: From the main menu, select Control > Setup > Invoice Matching

Tolerances > Edit.

The Invoice Matching Tolerances window is displayed.

Invoice Matching Tolerances window

Note: Default invoice matching tolerances are added at the corporate level.

1

In the Level field, select Corporate.

2  Click Add Line.

3  On the next available line, select the level for the tolerance in the Tolerance

Level field.

4

In the Difference In Favor Of field, select whether the tolerance is for
differences in favor of the supplier or your organization.

5

In the Lower Limit field, enter the lower threshold of the tolerance.

6

In the Upper Limit field, enter the upper threshold of the tolerance.

7

In the Tolerance Type field, select the type of tolerance, Amount or Percent.

8

In the Tolerance Value field, enter the value of the tolerance.

9  Click OK to save your changes and close the window.

Chapter 3 – Invoice matching  25

Add a non-merchandise code

(cid:194) From the main menu, select Control > Setup > Invoice Non-Merchandise

Codes > Edit.

The Invoice Non-Merchandise Codes Maintenance window is displayed.

Invoice Non-Merchandise Codes Maintenance window

1  Click Add.

2  On the next available line, enter a unique ID in the Non-Merchandise Code

field.

3

In the Description field, enter a description for the non-merchandise code.

4  When applicable, select the Service Indicator check box.

5  Click OK to save your changes and close the window.

26   Retek Invoice Matching

Create a credit memo

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

Invoice Header Details window

1

In the Action field, select New and click OK. The Invoice Header Details
window is displayed.

2

In the Type field, select Credit Memo.

3  Select the type of vendor and identify the vendor:

Note: For credit notes referenced by an invoice or RTV order, you can only
select a supplier.

a

If you select Partner, select the type of partner in the Partner Type field.

b

In the Partner or Supplier field, enter the ID of the vendor, or click the

LOV

 button and select the vendor.

4

In the Reference field, select the reference type for the credit note.

5

In the Reference ID field, enter the ID of the reference, or click the LOV
button and select the reference.

Note: You do not specify a reference ID when the reference is Stand Alone
Debit/Credit

Chapter 3 – Invoice matching  27

6

7

In the Reason field, enter the code for the reason, or click the LOV
button and select a reason.

In the Total Mrch Cost field, enter the total cost of the merchandise on the
invoice.

8  When applicable, enter the total VAT amount in the Total Mrch VAT Incl

Dscnt field.

9

In the Total Invoice Cost field, enter the total cost of the invoice.

10  Click OK to save your changes and close the window.

Create a credit note

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

1

In the Action field, select New.

2  Click OK. The Invoice Header Details window is displayed.

3

In the Type field, select Credit Note.

4  Select the type of vendor and identify the vendor:

a  Select either the Partner or Supplier option.

Note: For credit notes referenced by an invoice or RTV order, you can only
select a supplier.

b

If you select Partner, select the type of partner in the Partner Type field.

c

In the Partner or Supplier field, enter the ID of the vendor, or click the

LOV

 button and select the vendor.

5

In the Reference field, select the reference type for the credit note.

6

In the Reference ID field, enter the ID of the reference, or click the LOV
button and select the reference.

Note: You do not specify a reference ID when the reference is Stand Alone
Debit/Credit

7

In the Reason field, enter the code for the reason, or click the LOV
button and select a reason.

28   Retek Invoice Matching

8

In the Total Mrch Cost field, enter the total cost of the merchandise on the
invoice.

9  When applicable, enter the total VAT amount in the Total Mrch VAT Incl

Dscnt field.

10  In the Total Invoice Cost field, enter the total cost of the invoice.

11  Click OK to save your changes and close the window.

Create a credit note request

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

1

In the Action field, select New.

2  Click OK. The Invoice Header Details window is displayed.

3

In the Type field, select Credit Note Request.

4  Select the type of vendor and identify the vendor:

a  Select either the Partner or Supplier option.

Note: For credit notes referenced by an invoice or RTV order, you can only
select a supplier.

b

If you select Partner, select the type of partner in the Partner Type field.

c

In the Partner or Supplier field, enter the ID of the vendor, or click the

LOV

 button and select the vendor.

5

In the Reference field, select the reference type for the credit note.

6

In the Reference ID field, enter the ID of the reference, or click the LOV
button and select the reference.

Note: You do not specify a reference ID when the reference is Stand Alone
Debit/Credit

7

8

In the Reason field, enter the code for the reason, or click the LOV
button and select a reason.

In the Total Mrch Cost field, enter the total cost of the merchandise on the
invoice.

9  When applicable, enter the total VAT amount in the Total Mrch VAT Incl

Dscnt field.

Chapter 3 – Invoice matching  29

10  In the Total Invoice Cost field, enter the total cost of the invoice.

11  Click OK to save your changes and close the window.

30   Retek Invoice Matching

Create a debit memo

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

1

In the Action field, select New.

2  Click OK. The Invoice Header Details window is displayed.

3

In the Type field, select Debit Memo.

4  Select the type of vendor and identify the vendor:

a  Select either the Partner or Supplier option.

Note: For credit notes referenced by an invoice or RTV order, you can only
select a supplier.

b

If you select Partner, select the type of partner in the Partner Type field.

c

In the Partner or Supplier field, enter the ID of the vendor, or click the

LOV

 button and select the vendor.

5

In the Reference field, select the reference type for the credit note.

6

In the Reference ID field, enter the ID of the reference, or click the LOV
button and select the reference.

Note: You do not specify a reference ID when the reference is Stand Alone
Debit/Credit

7

8

In the Reason field, enter the code for the reason, or click the LOV
button and select a reason.

In the Total Mrch Cost field, enter the total cost of the merchandise on the
invoice.

9  When applicable, enter the total VAT amount in the Total Mrch VAT Incl

Dscnt field.

10  In the Total Invoice Cost field, enter the total cost of the invoice.

11  Click OK to save your changes and close the window.

Chapter 3 – Invoice matching  31

Create a merchandise invoice

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

1

In the Action field, select New.

2  Click OK. The Invoice Header Details window is displayed.

3

In the Supplier field, enter the ID of the supplier, or click the LOV
and select a supplier.

 button

4

In the Vendor Invoice Date field, enter the date of the invoice from the

vendor, or click the calendar

 button and select the date.

5

6

In the Vendor Invoice Number field, enter the number of the invoice from
the vendor.

In the Total Mrch Cost field, enter the total cost of the merchandise on the
invoice.

7

In the Total Invoice Cost field, enter the total cost of the invoice.

8  To associate a receipt with the invoice:

a  Click Receipts. The Invoice/Receipt Summary-Level Match window is

displayed.

Invoice/Receipt Summary-Level Match window

\

32   Retek Invoice Matching

b

In the Receipt No field, enter the number of the receipt, or click the LOV

 button and select a receipt.

c  Click OK to close the Invoice/Receipt Summary-Level Match window.

9  Click OK to save your changes and close the window.

Create a non-merchandise invoice

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

1

In the Action field, select New and click OK. The Invoice Header Details
window is displayed.

2

In the Type field, select Non-Merchandise Invoice.

3  Select the type of vendor and identify the vendor:

a  Select either the Partner or Supplier option.

b

If you select Partner, select the type of partner in the Partner Type field.

c

In the Partner or Supplier field, enter the ID of the vendor, or click the

LOV

 button and select the vendor.

4

In the Vendor Invoice Date field, enter the date of the invoice from the

vendor, or click the calendar

 button and select the date.

5

In the Vendor Invoice Number field, enter the number of the invoice from
the vendor.

Chapter 3 – Invoice matching  33

6  Click Non-MrchDtls. The Invoice Non-Mrch Cost Details window is

displayed.

Invoice Non-Mrch Cost Details window

7  Click Add.

8

In the Code field, enter the code for the non-merchandise cost, or click the

LOV

 button and select the cost.

9

In the Non-Mrch Amt field, enter the amount of the non-merchandise cost.

10  In the Store field, enter the ID of the store, or click the LOV

 button and

select a store. This field is optional.

11  When applicable, select the Svc Perf’d check box.

12  When required, enter the VAT code in the VAT Code field, or click the LOV

 button and select a VAT code. The VAT Amt field is filled in

automatically based on the VAT code you select.

13  Click OK to save your changes and close the window.

34   Retek Invoice Matching

Search for an invoice document

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

1

In the Action field, select Edit or View.

Invoice Find window

2  Enter additional criteria as desired to make the search more restrictive.

Note: When entering an item, or selecting an item, the Item's status must be
Approved.

3  Click Search. The Invoice Find window displays the invoices that match the

search criteria.

4  Select a task:

a  To perform another search, click Refresh.

b  To display the invoice information, select a record and click OK. The

Invoice Header Details window is displayed.

5  Click Close to save your changes and close the window.

Chapter 3 – Invoice matching  35

Confirm performance of service

(cid:194) Navigate: From the main menu, select Finance > Service Confirmation by

Store.

The Service Confirmation by Store window is displayed.

Service Confirmation by Store window

1

In the Store field, enter the ID of the store at which the service was

performed, or click the LOV

 button and select the store.

2  To further limit the services that are displayed:

a

In the Invoice Date field, enter the date of the invoice document, or click

the calendar

 button and select the date.

b  Select the type of vendor, either Partner or Supplier.

c  When the vendor is a partner, select the type of partner in the Partner

field. In the next field, enter the ID of the partner or click the LOV
button and select a partner.

d  When the vendor is a supplier, enter the ID of the supplier in the Supplier

field, or click the LOV

 button and select the supplier.

3  Click Search.

4  Select the Service Performed check box for the service that has been

performed.

5  Click OK to save your changes and close the window.

36   Retek Invoice Matching

Approve an invoice document

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

Search for and retrieve an invoice document in Edit mode.

The Invoice Header Details window is displayed.

1  Select Options > Approve. The Status field changes to Approved.

2  Click OK to save your changes and close the window.

Unapprove an invoice document

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

Search for and retrieve an invoice document in Edit mode.

The Invoice Header Details window is displayed.

1  Select Options > Unapprove.

2  Click OK to save your changes and close the window.

Force pay a merchandise invoice

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

Search for and retrieve a merchandise invoice in Edit mode.

The Invoice Header Details window is displayed.

1  Select Options > Force Pay Invoice. The Force Paid check box on the

Invoice Header Details window is selected.

2  Click OK to close the window and save your changes.

Chapter 3 – Invoice matching  37

Cancel the force pay of a merchandise invoice

(cid:194) Navigate: From the main menu, select Finance > Invoice Matching.

The Invoice Find window is displayed.

Search for and retrieve a merchandise invoice in Edit mode.

The Invoice Header Details window is displayed.

1  Select Options > Cancel Force Pay. The Force Paid check box on the Invoice

Header Details window is cleared.

2  Click OK to save your changes and close the window.

Index
Advance shipping notices............................19
Approvals....................................................36
Cancellations ..............................................37
Codes

Non-merchandise codes.............................25
Confirmations ............................................35
Credit memos .......................................26, 34
Credit note requests .............................28, 34
Credit notes..........................................27, 34
Debit memos.........................................30, 34
Invoice matching ............................19, 36, 37
Tolerances...................................................24

Index   39

Invoices ......................................... 31, 32, 34
Approval process ........................................ 36
Invoice matching ................................. 36, 37
Merchandise invoices........................... 31, 34
Approval process ........................................ 36
Invoice matching ................................. 36, 37
Non-merchandise codes ............................. 25
Non-merchandise invoices.......................... 32
Overviews.................................................. 19
Performance of service............................... 35
Tolerances ................................................. 24

