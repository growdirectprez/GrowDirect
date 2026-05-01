---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/Other Retek Decks/topplan-100-ug.pdf.md
tags: [retail, retek, rms, rib, rdm, 2003-2005]
project: retail
status: unprocessed
---

# topplan-100-ug.pdf

## Source
File: `Brain/raw/.extract/Other Retek Decks/topplan-100-ug.pdf.md`
Size: 218,929 bytes

## Raw content
Retek® TopPlan
10.0

User Guide

 TopPlan

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

Retek® TopPlan™ and Retek® ChannelPlan™ are trademarks of Retek Inc.

Retek and the Retek logo are registered trademarks of Retek Inc.

©2002 Retek Inc. All rights reserved.

Corporate Headquarters:

Retek Inc.

Retek on the Mall

950 Nicollet Mall

Minneapolis, MN 55403

888.61.RETEK (toll free US)
+1 612 587 5000

European Headquarters:

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

Fax

E-mail

Internet

Mail

US & Canada: 1-800-61-RETEK (1-800-617-3835)
World: +1 612-587-5000

(+1) 612-587-5100

support@retek.com

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

Contents   i

Contents

Chapter 1 – Introduction......................................................... 1

Retek Predictive Planning products .................................................................... 1

Features of Retek planning products .......................................................................... 1
Process for using Retek Predictive Planning products ............................................... 4
Planning roles ............................................................................................................. 6

Retek TopPlan ..................................................................................................... 7

Plan versions for Retek TopPlan ................................................................................ 7
Strategic planning ....................................................................................................... 8
Financial planning: pre-season and in-season planning ............................................. 9
Plan reconciliation and approval .............................................................................. 11

Retek ChannelPlan ............................................................................................ 14

Channel planning...................................................................................................... 14
The Channel Planning workbook ............................................................................. 14
Plan versions for Retek ChannelPlan ....................................................................... 14

Chapter 2 — Getting Started ................................................ 15

Log in to TopPlan.............................................................................................. 15

Access Help....................................................................................................... 16

Open an existing workbook............................................................................... 17

Create a new workbook..................................................................................... 18

Save a workbook ............................................................................................... 19

Saving options .......................................................................................................... 20

Synchronize Page Scrolling .............................................................................. 21

Close a workbook.............................................................................................. 22

Delete a workbook ............................................................................................ 22

Log off of TopPlan............................................................................................ 22

What’s Next....................................................................................................... 22

ii    TopPlan

Chapter 3 – Workbook descriptions.................................... 23

Planning Administration workbooks................................................................. 24

Retek TopPlan workbooks ................................................................................ 28

Strategic Target Plan workbook ............................................................................... 28
Pre-Season Financial Plan workbook ....................................................................... 33
In-Season Financial Plan workbook ......................................................................... 58

Retek ChannelPlan workbooks ......................................................................... 87

Channel Planning workbook .................................................................................... 87

Chapter 4 – Measure descriptions....................................... 93

Metrics and Measures........................................................................................ 93

Business Rules................................................................................................... 93

TopPlan measures ............................................................................................. 94

TopPlan Strategic Target planning measures ........................................................... 94
TopPlan Financial planning measures (Pre-Season and In-Season)......................... 99

ChannelPlan measures..................................................................................... 138

Glossary............................................................................... 143

 Chapter 1 – Introduction   1

Chapter 1 – Introduction

Retek Predictive Planning products

The Retek Predictive Planning products are flexible applications providing top-
down, bottom-up, middle-out functionality for developing, reconciling, and
approving plans.  Supported by an industry standard process, the Retek
Predictive Planning products are scalable enough to plan at levels of detail
appropriate for any business, from high-level strategic planning to in-season
financial management.

Built on powerful predictive engines, the Retek Predictive Planning products use
integrated demand forecasting to provide an accurate view of customer demand
quickly, with little human intervention.  Exception management functionality
flags affected areas of a plan that may otherwise go unnoticed when managing
large amounts of data.

Retek TopPlan and Retek ChannelPlan are part of the Retek Predictive Planning
Suite.

Features of Retek planning products

Key features of the Retek Predictive Planning products include the following.
Several of these features are covered in much greater detail in the Retek
Predictive Solutions online Help or Retek Predictive Application Server (RPAS)
User Guide.

Workbooks

Many of the planning activities are performed through building workbooks and
viewing data in the workbooks. A workbook is a user-defined subset of data that
includes selected dimensions.  These workbooks consist of worksheets and
graphical charts for planning, viewing and analyzing business measures.
Workbooks provide a method of organizing various types of related information
and separating the levels of responsibility. This framework allows you to easily
view, create, modify and store sets of data that are common to specific tasks.  A
Workbook definition consists of:

•  Product levels and members to plan, for example, Department, Class, Sub-

Class for Men’s Sweater Department

•  Time levels and members to plan, for example, Season, Month, Week for

Spring 2002 Season

•  Location levels and members to plan. For example, within TopPlan these
members may reflect multiple channels within an organization at their
aggregate level such as total Brick & Mortar divisions, Catalog and /or e-
Commerce while in ChannelPlan the members might be Region, District,
Store for North America- East Coast

Note: (For more on Product, Time, and Location hierarchies, see the Retek
Predictive Solutions online Help or the Retek Predictive Application Server
User Guide.)

2    TopPlan

•  Plan versions, for example, Working Plan (Wp), Original Plan (Op), Current

Plan (Cp), and Last Year (Ly)

•  Measures and corresponding business rules, for example, Sales, Receipts,

Markdowns, Inventory

The workbooks can be automatically built in batch at night and contain all of the
planning windows, measures, and business rules needed for a complete plan.  To
use the workbooks, you log onto your system, open the workbooks, and begin
planning. Additionally, workbooks can be manually built by stepping through a
Planning Workbook wizard.

Data in a workbook can be displayed using both multi-dimensional spreadsheets
and charts. The data can be viewed at lower levels of detail or higher levels of
aggregation with the ease of a mouse click.

For descriptions of the Retek TopPlan and ChannelPlan workbooks, see Chapter
2. For more information on manipulating data in the worksheets, see the Retek
Predictive Solutions online Help or Retek Predictive Application Server (RPAS)
User Guide.

Worksheets

Planning worksheets are multi-dimensional spreadsheets that provide a view of
data within a workbook.  Retek Predictive Planning comes with a series of built-
in worksheets within a workbook that support an industry standard business
process.  Each worksheet can contain unique product, time, and metric
information.  This approach enables users to logically step through the planning
process in a consistent manner across the organization.

The worksheet feature is manageable within each user’s environment as well.  In
a planning session, worksheets can be created to suit an individual’s need.
Unique individual views can be created within the worksheets by rotating and
pivoting the dimensions and displaying information in a variety of formats..
Worksheets can also be toggled into charts, enabling graphical viewing and
analysis of a business function.

For descriptions of the Retek TopPlan and ChannelPlan worksheets, see Chapter
2. For more information on manipulating data in the worksheets, see the Retek
Predictive Solutions online Help or Retek Predictive Application Server (RPAS)
User Guide.

Editing data

 Chapter 1 – Introduction   3

Planning data is edited on the worksheets. Flexible business rules enable you to
execute the planning process using whatever series of planning worksheets you
choose.

Two options are available to ensure that data is not lost during the planning
process.

•  A Save option allows the updated data to be saved within the workbook,

without affecting the master database. This allows you to manipulate details
and evaluate the impact of their changes without changing the master data.
You could work within the worksheet throughout a given day, use the save
option, and keep the updates made.

•  Once you are satisfied with the changes, the Commit option sends data back
to the master database.  This makes the changes accessible to all users once
the workbooks are rebuilt or refreshed.

Batch processing brings in all relevant updates and changes from the master
database into workbooks that are rebuilt. The Refresh option brings updates and
changes from the master database into an existing workbook, in lieu of building a
new workbook.

Within a planning session, data can be modified at all levels of each hierarchy.  If
the data is modified at an aggregate level, then the modifications are distributed
down to the lower levels (spreading). The reverse is also possible; if data is
modified at the lower levels, the aggregates of the data reflect those changes at
the consolidated levels of each hierarchy.

For more information about editing data, aggregation, spreading and committing
changes, see the Retek Predictive Solutions online Help or Retek Predictive
Application Server (RPAS) User Guide.

Plan reconciliation and approval—TopPlan only

Reconciliation of planned data and promoting the data to approved status is an
important final step of the financial planning process performed through
TopPlan. The goal of this step is to achieve a plan that all contributing parties
have reviewed and approved. As plans are generated, they move through the
reconciliation phase, and on to the plan approval phase.

For more about plan reconciliation and approval, see “Plan reconciliation and
approval” on page 11.

Printing and Reporting

Within TopPlan, users can print planned data during a planning season at any
time. Pre-Season, the report data would be the Original Plan, Last Year and
variances to Last Year; In-Season, the report data would include the Working
Plan with any actuals, the Original Plan, the Current Plan, and Last Year and
appropriate variances. Retek Data Warehouse (RDW) provides the foundation for
reporting plan against actual data.  Once Original and Current plans are
approved, those figures are sent to RDW for analysis and reporting.

4    TopPlan

Exception management and alerts

Retek Predictive Planning includes an Alert Manager for highlighting
opportunities to users that might, because of the volume of data that needs to be
managed, otherwise go unnoticed.  You can set up business rules to alert users
about OTB opportunities, stock outages, sales performance against a plan,
margin opportunities, and so on.  Each of these alerts has a role within a business
process that demands highly accurate management of large amounts of business
information.  These alerts go beyond exception reporting, as the Alert Manager
will take you directly to the area of the plan that needs action.

Alerts are set up by identifying a business measure as the foundation, then
creating the alert via a mathematical rule.  A background program called the
Alert Finder runs in a batch process and finds the areas of a plan that fall outside
the thresholds declared within the alert rules.  This will create a message, or alert,
that is flagged to the user through the Alert Manager window.

At this point, the alerts have been identified and the user has the ability to go
directly to affected areas of the workbook and take appropriate action.

Additionally, users have the ability to set User Defined Exceptions on any
measure within their plan workbook and see the results immediately. Minimum
and/or Maximum tolerances are set by the user as well as specific formatting to
view the Exceptions such as a change in background color, a change in font or
text color to easily see any exceptions that qualify.

For more information about alerts, see the Retek Predictive Solutions online Help
or Retek Predictive Application Server (RPAS) User Guide.

Process for using Retek Predictive Planning products

Retek Predictive Planning supports the entire business process from strategic
planning to financial planning. Product and Channel (specifically location)
planning are supported with a pre-season planning process. Product planning is
also supported with an in-season planning process. The diagram shows the
business process supported by Retek Predictive Planning.

Process supported by Retek Predictive Planning products

 Chapter 1 – Introduction   5

As shown in the process flow diagrams for each type of planning within the
following topics, a number of processes within an organization must be pulled
together to achieve a finished plan from inception to reconciliation and plan
approval.  An application that supports a strong disciplined business process
gives all contributing parties access to the same planned data and ensures that the
entire organization works toward common business goals.

These processes are reflected and reinforced in the TopPlan and ChannelPlan
workbooks and worksheets.

6    TopPlan

Planning roles

Planning roles identify the levels at which planning occurs in a business, the
range of planning at that level, and the time period with which that level of
planning is concerned. These roles are defined by the base intersection at which
planning occurs and by the reporting structure within the planning organization.
Each role may have a bottom-up role and/or a top-down role associated with it,
reference chart below. The planning role you have defines the range of planning
for which you are responsible, and affects the measures you will see in planning
worksheets and your access permissions to those measures.

While you can customize the planning roles used in your business during
implementation, a generic set of planning roles is supplied with TopPlan and
ChannelPlan products:

•  Executive (Ex)

•  Manager (Mg)

•  Planner (Pl)

•  Channel Planner (Ch)

The range of planning and the role relationships for these roles are as follows:

Role

Base
Intersection

Range of
planning

Lowest level
time period

Bottom-up
role

Top-down
role

Executive
(Ex)

Manager
(Mg)

Planner (Pl)

Channel
Planner (Ch)

Division /
Month

Company –
Division

Department /
Week

Division –
Department

Month

Manager

NA

Week

Planner

Executive

Subclass /
Week

Department –
Subclass

Week

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
