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

KeyPlan™
Planner

Store / Week  Channel –

Week

NA

NA

NA

Store

Roles and the plan approval process

In TopPlan only the Manager and Planner roles participate in the plan approval
process. Additional roles may be added to the structure.  All measures within the
planning area must be duplicated for additional roles and base intersections
amended for existing roles as necessary.

For more about plan approval, see “Plan reconciliation and approval” on page 11.

The Plan Approval worksheet—TopPlan only

 Chapter 1 – Introduction   7

In Retek TopPlan, the Plan Approval worksheet is used to submit plans for
approval, to approve submitted plans, and view the status of submitted plans.
Your planning role determines the range of actions you can perform on this
worksheet. For example, if you are in a subordinate role such as the Planner role,
you can only submit plans for approval on the worksheet and view the status of
the submitted plan. If you are in a superior role such as Manager, you can
approve or reject submitted plans and comment on the plan being approved or
rejected.

For a description of the Plan Approval worksheet, see page 55.

Retek TopPlan

Retek TopPlan provides strategic and financial product planning functionality,
which includes business rules to support industry standard best practice for pre-
season and in-season processes. TopPlan also provides visibility to other plans,
as well as a forum for reconciliation and approval of pre-season and in-season
plans.

Plan versions for Retek TopPlan

The strategic and financial planning processes supported by TopPlan involve
several versions of plans throughout the planning horizon. These version names
and their abbreviations are used frequently in planning worksheets, for example,
to distinguish measures. Definitions for these plan versions are in the glossary at
the end of this guide.

•  Working Plan (Wp)

•  Last Year (Ly)

•  Forecast (Fcst)

•  Target (Tgt)

•  Original Plan (Op)

•  Current Plan (Cp)

•  Waiting for Approval (Wa)

•  Submitted Waiting for Approval (Swa)

•  Submitted Current Plan (SCp)

•  Submitted Original Plan (SOp)

•  Admin (Ad)

•  Reference Admin (Ra)

•  KeyPlan (Kp)

8    TopPlan

Plan versions and planning roles

The plan versions that are visible to TopPlan users depend on the users’ planning
roles, and are as follows:

•  Planner role: Working Plan, Last Year, Forecast, Target, KeyPlan, Waiting
for Approval, Administrative, Reference Administration, Original Plan,
Current Plan

•  Manager role: Working Plan, Last Year, Forecast, Target, KeyPlan,

Submitted Waiting for Approval, Administrative, Reference Administration,
Submitted Original Plan, Submitted Current Plan

•  Executive role: Working Plan, Last Year, Forecast, Submitted Waiting for

Approval, Reference Administration, Submitted Original Plan, Submitted
Current Plan

For more information on plan versions, see the following sections:

(cid:131)  Plan reconciliation and approval on page 11

(cid:131)  Planning roles on page 6

(cid:131)  Plan Approval Worksheet on page  55

Strategic planning

Strategic planning involves developing an executive level plan used during the
preseason planning process.  This plan provides the vehicle to set targets for key
planning measures such as sales, markdowns, profit margin, average inventory,
and turnover.  Characteristics of the strategic plan include:

•  Product Hierarchy:  Total Company to Division

•  Time Hierarchy:  Total Time to Month

•  Metrics:  Values only, no units for Sales, Markdowns, Gross Margin,

Average Inventory and Turnover

•  Plan Versions:  Working, Forecast, Last Year, Submitted Waiting for
Approval, Submitted Original Plan, Submitted Current Plan, Reference
Administration

After the plans are complete, they are made available to the balance of the
planning community and provide a foundation upon which lower levels of detail
will be created throughout the Financial Planning process for Product.

The Strategic Target Plan workbook

Strategic planning is performed through the Strategic Target Plan workbook. For
a description of this workbook and its worksheets, see page 28.

Financial planning: pre-season and in-season planning

 Chapter 1 – Introduction   9

Financial planning is the workhorse of the product planning process.  Multiple
users perform their planning duties using the financial planning workbooks.  Pre-
season and in-season processes are supported with sales and profit projections,
Open to Buy (OTB) management, and full value and unit calculations. The
process always brings the plans together through reconciliation, and ultimately,
plan approval.  This ensures that one version of the plan is approved and used as
a foundation against which the company manages its business. Characteristics of
the financial plan include:

•  Product Hierarchy:  Total Company to Sub-Class

•  Time Hierarchy:  Total Time to Week

•  Metrics:  Values and units

•  Plan Versions:  Working Plan, Forecast, Target, Original Plan, Current Plan,

Last Year, Submitted Waiting for Approval, Submitted Original Plan,
Submitted Current Plan, Administrative and Reference Administration

Pre-Season Financial Planning

The pre-season financial plan is used to develop a plan before the selling period
begins. The following diagram shows the process steps covered by the Pre-
Season Planning worksheets.

Multiple pre-season periods

Pre-Season Financial Planning process

You can create multiple pre-season periodsas needed through a system
administration wizard and automated process for creating pre-season planning
workbooks. This feature may be useful when different planners in the
organization require different pre-season periods. Some examples of situations
where multiple pre-season periods can be defined are:

•  When planners in the Executive role need a pre-season period defined for a
3-year Strategic Plan comprising the years , - 2004, 2005 & 2006 while the
rest of the company only needs Spring 2004.

•  For planners within the Planner role, multiple pre-season periods can be

defined when the whole company needs Spring 2004, but the Men's Import
Sweater planner needs to be working on Fall 2004 now.

10    TopPlan

The Pre-Season Financial Plan Workbook

Pre-season financial planning is performed through the Pre-Season Financial
Plan workbook. For a description of this workbook and its worksheets, see page
33.

In-Season Financial Planning

Once the selling period begins, the In-Season Planning worksheets can be used to
review progress and make adjustments.

The following diagram shows the process steps covered by the Pre-Season
Planning worksheets.

In-Season Financial Planning process

 Chapter 1 – Introduction   11

The In-Season Financial Plan workbook

In-season financial planning is performed through the In-Season Financial Plan
workbook. For a description of this workbook and its worksheets, see page 58.

Forecast driven planning

Retek Demand Forecasting (RDF) imbedded directly within TopPlan and
provides an automatic Sales Value forecast that has already been systemically
approved and visible each week upon workbook rebuild or refresh.  One forecast
method for all products is selected upon implementation for Pre-Season financial
planning and one for In-Season financial planning. There is no direct user
intervention when forecasting is directly imbedded within TopPlan.  This allows
the user to accept all or part of a Sales Value forecast.  Once that decision is
made, the remaining business measures are planned within Retek TopPlan.

Plan reconciliation and approval

Reconciliation, approval, and promotion of product financial plans at different
levels is an integral part of the merchandise planning process. Plan reconciliation
and approval helps to achieve one plan that all contributing parties have reviewed
and approved—a “single version of the truth”. It supports the philosophy of
managing according to one plan within the company, with all relevant parties
having access to this plan.

In basic terms, users first reconcile their own plans using the targeted plan data
that had been set from the management role above them. Reconciliation occurs
for key business measures such as sales, markdowns, gross margin, and turnover
for a specified amount of time at a specified level within the time and product
hierarchy. The culture within a given retailer dictates whether the reconciliation
is hard or soft at those levels.

Reconciliation is performed by users in two roles: the Planner and the Manager,
who acts as the plan approver. These roles are addressed in the order that they are
performed in the approval process. The process to reconcile and approve plans
involves users and approvers within the following high-level steps. This process
typically occurs once per planning season for Pre-Season ultimately achieving
anOriginal Plan (Op) and an estimated once per month, or as frequently as a
given retailers process dictates, during the In-Season each time resulting in a new
Current Plan (Cp).

The reconciliation steps require a full set of plan data for each plan used in the
comparison task.  Submission for approval and approval/rejection steps require
limited data (the planner submitting the plan, the plan version, the last plan
version change date and timestamp, the approver receiving, approving or
rejecting the plan, and any comments the approver may want to make).

Plan submission and approval is performed using the Plan Approval worksheet in
both the Planner and Managers workbooks. This worksheet is used for both pre-
season and in-season plans.

12    TopPlan

Step 1: Planner reconciliation

In this step, the planner reconciles his or her own Working Plan with the Target
Plan from the next level above. The planner compares their Working Plan to
other plan versions, for example a supervisor’s Target Plan , the Current Plan or
the Original Plan. . The planner may select different plan versions to include in
the reconciliation process.  For example, the planner may wish to view their
Working Plan, the Last Year plan at their level, and the Original Plan for
comparison while completing planner reconciliation during the in-season
planning process.  After the comparison is complete, the planner may change
their Working Plan to reflect one of the comparison plans, and save the
reconciled Working Plan. When reconciliation is complete, the plan is ready for
approval.

Step 2: Submission of plan for approval

This step is performed by users in the Planner role.  Once the planner completes
the reconciliation step and submits the plan for approval, the planner’s saved
Working Plan is promoted to the Waiting for Approval plan version.  As a result
of the promote action, the Working Plan data is copied to the Waiting for
Approval version, and the new plan version is committed to the database.  When
the version is changed, the following data describing the version change is saved:
the planner submitting the plan, the submission/promotion date, and the plan
version.  After the promotion is complete, the approver is notified that a Waiting
for Approval plan version exists and requires action. All plans in the Waiting for
Approval status are held in the master database until they are approved.

Step 3: Approver reconciliation

Users in the Manager role perform this step. The approver reviews the data
submitted in Waiting for Approval plans and notes any planners whose
outstanding plans are needed to complete the approver reconciliation.  When the
approver notes that all Waiting for Approval plans have been submitted, the
approver performs approver reconciliation. That is, the approver reconciles their
own Working Plan with the consolidation of plans from the planner level below.
In this step, the approver compares the consolidation of the planners’ Waiting for
Approval plans in the Manager’s Submitted Waiting for Approval (SWa) plan
version to their own Working Plan and to the the Target Plan received from the
managers supervisor, the Executive Role.  The approver may (but does not have
to) change his or her own Working Plan to reflect the consolidated Submitted
Waiting for Approval plans and save the reconciled Working Plan.

Step 4: Approve or reject the plan

After reviewing the Submitted Waiting for Approval Plans, the
approver/Manager either approves or rejects the plans. The approver/Manager
can make comments in a text line on the approval worksheet that are saved and
passed to the planner along with approved or rejected status of the plans. Such
comments can supply the planner with direction about what needs to improve or
change in the plan if the plan is rejected.

 Chapter 1 – Introduction   13

Approving a plan: When a plan is approved, it moves to either Original Plan
and /or Current Plan, depending on the business process.

•  For a pre-season plan, the plan moves to both the Original Plan (Op) and the

Current Plan (Cp) versions.

Promotion to Original Plan status sets a flag to create a flat file in a batch
process that contains all measures included in the Original Plan version.  This
flat file will be created once when the Original Plan measures are populated
and will be made available to Retek Data Warehouse for storage of Original
Plan measures.

•  For an in-season plan, the plan moves only to the Current Plan (Cp) version.

Promotion to Current Plan status sets a similar flag to create a flat file in a
batch process that contains all measures included in the Current Plan version.
This flat file will be created regularly during the in-season planning process
each time  the Current Plan version is updated.  The file will be made
available to Retek Data Warehouse for storage of Current Plan measures.
Data which resides in the Cp version is visible to the Manager and Executive
in the Submitted Current Plan (SCp) version measures. Data which resides in
the Op version is visible to the Manager and Executive in the Submitted
Original Plan (SOp ) version measures.

As a result of the promote action, the Submitted Waiting for Approval plan data
is copied to the Original Plan and / or Current Plan versions, and the new plan
version is committed to the database.  When the version is changed, the
following data describing the version change is saved: the planner submitting the
plan, the promotion date, the plan version, the approver’s comments, and the
approver promoting the plan.

Rejecting a plan: If the plan is rejected, it is not promoted to either Original Plan
or Current Plan.  The planner can make the necessary adjustments to his or her
Working Plan.  The plan can then be resubmitted for approval.

When the plan version is changed, the following data is saved: the planner
submitting the plan, the demotion date, the plan version, the approver’s
comments, and the approver demoting the plan.  After the demotion is complete,
the owner of the demoted plan is notified that their Waiting for Approval plan
has been rejected and that the plan requires action.

14    TopPlan

Retek ChannelPlan

Retek ChannelPlan provides financial location functionality for pre-season plans,
which includes business rules to support industry standard best practice for pre-
season processes.

Channel planning

Channel planning is a pre-season process for planning Sales Value and Average
Inventory for a business’s multiple locations, from stores to Internet-based sales.
Sales Values can be derived by planning percentage variances to historical data,
product plan data, and the automatically generated demand forecast.  Average
Inventory is derived through the input of a turnover measure, with displayed data
for Sales per Square Feet.  You can reconcile the aggregated level of Total Chain
with the aggregated level of Total Company from the financial product plan.
Characteristics of the location plan include:

•  Location Hierarchy:  Total Chain to Store

•  Time Hierarchy:  Total Time to Month

•  Metrics:  Values only

•  Plan Versions:  Original, Working, Forecast, Last Year

The Channel Planning workbook

Channel planning is performed through the Channel Planning workbook. For a
description of this workbook and its worksheets, see page 87.

Plan versions for Retek ChannelPlan

The merchandise planning process involves several versions of plans throughout
the planning horizon. These version names and their abbreviations are used
frequently in planning worksheets, for example, to distinguish measures.

•  Working Plan (Wp)

•  Last Year (Ly)

•  Forecast (Fcst)

•  Merchandise Plan (Mp)

 Chapter 2 — Getting Started   15

Chapter 2 — Getting Started

This chapter describes of how you can quickly get started using TopPlan.

Log in to TopPlan

Follow this procedure to log in to TopPlan.

1  From the Windows Start menu select Programs > Retek Predictive Solutions
> Retek Predictive Solutions. The Login Information dialog box is displayed.

Login Information dialog

2  From the Connection drop-down list, select TopPlan or the Connection name

your administrator has assigned to TopPlan.

3  Enter your User Name and your Password in their respective fields.

4  Click Login.

After you log in successfully as a TopPlan user, the Retek Predictive Solutions
window is displayed with the following menu bar and toolbar.

Retek Predictive Solutions main menu and toolbar – no workbooks open

16    TopPlan

Access Help

The Retek Predictive Solutions Help provides information that is common to the
use of all Retek Predictive Solutions products, including TopPlan. It includes
general topics, such as:

•  Main menu options and toolbar buttons

•  Workbooks and worksheets

•  System procedures

•  Database components

•  Wizards

•  Quick menus

•  Changing views of data in worksheets

•  Aggregation and spreading

•  Rotate Data

•  Pivot Data

•  Alerts

Note: Material in online Help is replicated in Retek Predictive Application Server
(RPAS) User Guide for offline access. Information specific to TopPlan is
provided in this user guide as outlined in the table of contents.

Because worksheet and workbook views are highly customizable, window
examples shown in this user guide may not match the actual look of your screen.
For a basic of understanding of how to change views of data, see the Retek
Predictive Solutions online Help or Retek Predictive Application Server (RPAS)
User Guide.

To become familiar with workbooks and worksheets, different views of the data,
and other general topics, open the Help and review the topics available to you.

For example, for details on all the menu options and toolbar buttons, follow this
procedure:

1  From the main menu, select Help > Contents (or press F1). The Help window

is displayed.

2  Within the Help window, select Basic Functions and Components > Menus

and Toolbars, then select an applicable topic.

 Chapter 2 — Getting Started   17

Help Contents – menu and toolbar topics

Open an existing workbook

If TopPlan workbooks have already been created, you can display a list of the
workbooks available to you and select one.

1  Select File > Open or click Open.

The Open window is displayed. It lists all the workbooks previously created.

2  Select a workbook to read or edit.

Open Workbooks window

3  Click OK. The workbook you selected is opened. The last visible window

when you saved the workbook is displayed.  Use the next or previous arrows
to navigate through the workbook windows as you edit.

18    TopPlan

Create a new workbook

Choosing File > New from the main menu, or clicking New  launches wizards,
which provide a step-by-step method for creating new workbooks.

Note: This procedure outlines the basic steps for creating a new workbook. Read
detailed information about building specific TopPlan workbooks in the Chapter 4
of this user guide.

1  From the main menu, select File > New or click New . The New dialog box

is displayed.

“New” window for creating workbooks

2  Click on one of the tabs: Administration (if available), Analysis, or Planning.

Each tab contains workbook templates for specific workbook types.

3  Click on the workbook template for the workbook type you want to build.

4  Click OK.

5  Follow the wizard instructions to create the workbook.

 Chapter 2 — Getting Started   19

Save a workbook

You can save a newly created workbook at any point in the planning process and
open it later to complete the planning process or edit previous steps.  This action
also allows the flexibility to revise your plan continuously as new information
comes in.

1  Select File > Save from the main menu. The Save As dialog is displayed.

Save As dialog for workbooks

The column fields in the list box describe existing plans:

•  Name:  Name of plan

•  Owner:  Administration or user

•  Template Group:  Administration, Analysis, or Planning

•  User Group:  Work group of the plan originator

•  Type: Type of workbook

•  Date: Date of origination

•  Access: User (originator), world or group access

The Save As window displays previously saved workbooks. The first field is
blank.  When you enter a name for this workbook, it will be displayed in the
list of workbooks that can be viewed or edited.  This workbook name is
displayed on the title line when the workbook is open for further build or
editing procedures.

2  Enter an identifying name in the Workbooks field.

3

In the Save Access As section, select User, World, or Group.  Selecting
Group allows other users within your group to view or edit your workbook.
Selecting User allows only the plan originator to view or edit this workbook.
Once selected, it cannot be changed.

20    TopPlan

4

If you want all workbooks from your group to be displayed for viewing or
editing, select the List All Workbooks check box. If this check box is
cleared, you will only see the workbooks created by you as Owner.

5  Click OK.  The parameters of this workbook are saved and the workbook
structure is available for continued planning or for access at another time.
The Step 1 window is still displayed.

Saving options

When you save workbook information, you are presented with a dialog that lists
the following options:

Option

Description

Save

Commit Now

Save and Commit
Now

Save and Commit
Later

Saves all information in the workbook, including the
current layout of worksheets within the steps.  This
has the same result as selecting File > Save, or
clicking Save on this toolbar.
If the current workbook has been previously saved,
then Save updates the stored information.  If the
workbook has not been previously saved, Save
produces the Save As dialog, in which you specify a
workbook name.  Save does not commit changes to
the master database.

Commits the current state of data in your workbook
to the master database.  This option has the same
result as selecting File, Commit Now.  If changes
have been made in the workbook since the last save,
you are asked whether or not you want to save the
workbook before committing your data.

Saves the workbook and immediately commits the
data to the master database.  Workbook information
may be available for other users.

Saves the workbook immediately.  Later, the
workbook is committed to the master database
during a batch process, when system utilization is
minimized.

Ignore Changes

Exits without saving changes made.  Information is
not committed to the database.

Cancel

Closes the dialog that displays the saving options
without further action.

 Chapter 2 — Getting Started   21

Synchronize Page Scrolling

Several tabs contained within the plan workbook contain multiple worksheets. To
ensure that the same product and location is displayed on all worksheets, you
must enable the Synchronize Page Scrolling option.

1  Open a plan workbook.

2  Select Workbook from the Format menu. The Format Options dialog is

displayed.

3  Click the Enable Synchronized Page Scrolling check box.

Format Options Dialog

4  Click OK.

22    TopPlan

Close a workbook

When you finish working with a workbook, follow this procedure to close it:

1  From the main menu, select File > Close.

2

If changes were made to the workbook, select a button to save, commit, or
ignore (discard) the changes.

The workbook is closed.

Delete a workbook

Choosing Delete from the File menu, or clicking Delete  displays a window that
lists all the plans and reports previously created.  You can select a workbook for
deletion.

1  From the main menu, select File > Delete or  Delete on the toolbar. The

Delete window is displayed, showing a list of workbooks.

2  Select the title of the workbook you want to delete.  The workbook title is

highlighted.

3  Click OK.  A dialog window is displayed which asks you to confirm your

decision.

4  Click OK to delete the workbook, or click Cancel to abort the process.

Log off of TopPlan

Follow this procedure to log off and exit the system completely.

1  Select File > Exit.

2

If changes were made to an open workbook, select a button to save, commit,
or ignore (discard) the changes.

Follow this procedure to log off the system and leave the Login dialog open for
use by another user or with another Retek planning product.

1  From the main menu, select File > Logoff.

2

If changes were made to an open workbook, select a button to save, commit,
or ignore (discard) the changes.

What’s Next

After you have become familiar with the procedures in this chapter, you can
explore the other features and functions of TopPlan as described in the remaining
chapters of this user guide.

 Chapter 3 – Workbook descriptions   23

Chapter 3 – Workbook descriptions

This chapter describes the following workbooks associated with TopPlan and
ChannelPlan, and worksheets in each workbook:

•  Planning Administration workbook

•  Retek TopPlan workbooks

(cid:131)  Strategic Target Plan workbook

(cid:131)  Pre-Season Financial Plan workbook

(cid:131)  In-Season Financial Plan workbook

•  Retek ChannelPlan workbook

Note:  Workbooks associated with system administration and data analysis are
the workbooks on the Administration and Analysis tabs of the New dialog box.
Besides the Planning Administration workbook, these workbooks are described
in the Retek Predictive Solutions online Help or Retek Predictive Application
Server (RPAS) User Guide.

24    TopPlan

Planning Administration workbooks

The Planning workbook templates allow authorized users to set up default
planning parameters.

•  Plan Administration:

(cid:131)  Redefine the current season — Set new values for start date, end date

or the label of a current in-season plan.

(cid:131)  Redefine an existing season — Set new values for start date, end date or

the label of an existing preseason.

(cid:131)  Define a new pre season — Set initial values for start date, end date or

the label of a new preseason.

(cid:131)  Seed data for a defined preseason — Populate the data fields of an
existing preseason with data from your merchandise and financial
systems.

(cid:131)  Delete a predefined preseason — Remove a previously defined

preseason from the TopPlan system.

•  Store Count Definition — Select available products, locations, and dates for

the plans.

•  Synchronize BOP and EOP — Select the season whose end-of-period

(EOP) data will be used to seed the next season at its beginning-of-period
(BOP).

You can easily define planning administration default parameters using software
“wizards”. Choosing File > New from the main menu, or clicking New  launches
wizards, which guides you step-by-step through the process of establishing
default planning parameters.

Process for using Planning wizards

1  From the main menu, select File > New or click New . The New dialog box

is displayed.

“New” window for creating workbooks

 Chapter 3 – Workbook descriptions   25

2  Click on the Planning tab.

3  From the list of workbook templates for the Planning group, click on the

workbook template for the workbook type you want to build.

4  Click OK. A “wizard” is displayed. The wizard guides you step-by-step

through the process of establishing default planning parameters.

5  Follow the wizard instructions on each window.

(cid:131)  Click Next and Back to move between consequentive windows.

(cid:131)  Click Cancel to stop the wizard during the process without accepting the

values you entered so far.

(cid:131)  Click Finish to accept values you have entered thus far and default

values for all remaining parameters.

(cid:131)  Click Help for general information about using wizards.

For example, to define a new preseason:

a  Select Plan Administration from the New dialog. This launches the Plan

Administration wizard.

b  Choose Define a New Preseason:

Plan Administration Wizard – Define a New Preseason

c  Click Next. A window for defining start and end dates as well as a name

for the preseeaon is displayed.

26    TopPlan

d  Enter a Start date, End date, and label (that is, a name) for the new

preseason.

Plan Administration Wizard – Define Preseaon Dates and Label

e  Click Next. A window is displayed that asks if you are sure you want to

create the new preaseason.

f  Confirm that you want to create this new preseason:

Plan Administration Wizard – Confirm New Preseason Creation

g  Click Next. A window is displayed that ackowldges whether the new

preseason was successfully created.

 Chapter 3 – Workbook descriptions   27

h  Click Finish.

Plan Administration Wizard – New Preseason Creation Results

The other Planning wizards function in a similar manner, though they allow you
to perform different activities.

28    TopPlan

Retek TopPlan workbooks

Retek TopPlan has a set of workbooks for developing Strategic and Financial
plans:

•  Planning Administration, for setting default parameters. See page 24 for

more information.

•  Strategic Target Plan workbook

•  Pre-Season Financial Plan workbook

•

In-Season Financial Plan workbook

Strategic Target Plan workbook

This plan is developed by users in the Executive (Ex) planning role. Executive-
level planners use the Strategic Target Plan workbook to develop a high-level
view of financial targets. Executives use these targets to set targets for the lower-
level planners, that is, those in the Manager and Planner roles, to view in their
own planning workbooks. The Strategic Target Plan can be used for the entire
planning horizon, for example, for developing a 5-year plan.

The Strategic Target Plan workbook contains the following worksheets:

•  Plan Annual Targets worksheet

•  Plan Monthly Sales worksheet

•  Review Plan Values worksheet

•  Approval worksheet

Process for using this workbook

1  The workbook is built as part of the regular automated workbook build

processes. It can also be built manually by stepping through the Planning
Workbook wizard.

2

3

Input the annual targets on the Plan Annual Targets worksheet.

Input and calculate the monthly sales figures on the Plan Monthly Sales
worksheet.

4  Review the plan values on the Review Plan Values worksheet, and adjust

values as needed.

5  Review the Plan Approval worksheet.

6  Commit the Workbook to the master database to enable Targets from the

Executive role to be seen in the Managers workbook.

 Chapter 3 – Workbook descriptions   29

Annual Targets worksheet

Workbook

Strategic Target Plan workbook

Worksheet 1: Annual Targets

Usage in process

Pre-season Planning, Set Financial Targets

Process for using this worksheet

1  You can choose to accept an automatic copy of the RDF Fcst Sls R by an

input to Sls varFcst R.

2  Adjust goals by company or division.

3  Enter either Sls R or Sls varLy R. All other metrics will calculate.

4  Enter Mkd % and GM%. Mkd R and GM will calculate based on Sls R.

5

Input TO to calculate AvgInv R.

Measures

The Annual Targets worksheet contains the following measures. For descriptions
of the measures and their calculations, see “TopPlan Strategic Target planning
measures” on page 94.

Wp AvgInv R
Ly AvgInv R
Wp AvgInv varLy R %
Wp GM %
Ly GM %
Wp GM R
Ly GM R
Wp Mkd %
Ly Mkd %
Wp Mkd R
Ly Mkd R
Wp Sls R
Fcst Sls R
Ly Sls R
Wp Sls varFcst R %
Wp Sls varLy R %
Wp TO
Ly TO

Calculated
Referenced
Calculated
Entered
Referenced
Calculated
Referenced
Entered
Referenced
Calculated
Referenced
Entered or calculated
Referenced
Referenced
Entered or calculated
Entered or calculated
Entered or calculated
Referenced

30    TopPlan

Monthly Sales worksheet

Workbook

Strategic Targets workbook

Worksheet 2 – Monthly Sales

Usage in planning process

Pre-season Planning, Set Financial Sales Targets by Month

Process for using this worksheet

1  Enter Sls R, Sls contProd R, Sls contTime R, Sls varLy R, or Sls var Fcst R

%. All other metrics are re-calculated.

2  Sls build rate R % is calculated only.

Measures

The Plan Monthly Sales worksheet contains the following measures. For
descriptions of the measures and their calculations, see “TopPlan Strategic Target
planning measures” on page 94.

Wp Sls build rate R %

Calculated

Fcst Sls build rate R %

Referenced

Ly Sls build rate R %

Referenced

Wp Sls contProd R %

Entered or calculated

Fcst Sls contProd R %

Ly Sls contProd R %

Referenced

Referenced

Wp Sls contTime R %

Entered or calculated

Fcst Sls contTime R %

Referenced

Ly Sls contTime R %

Referenced

Wp Sls R

Fcst Sls R

Ly Sls R

Entered or calculated

Referenced

Referenced

Wp Sls varFcst R %

Entered or calculated

Wp Sls varLy R %

Entered or calculated

 Chapter 3 – Workbook descriptions   31

Review Plan Values worksheet

Workbook

Strategic Targets workbook

Worksheet 3: Review Plan Values

Usage in process

Pre-season Planning

Process for using this worksheet

This worksheet lists all the values included in the Strategic Target Plan. Review
plan values and adjust values as needed.

Measures

The Review Plan Values worksheet contains the following measures. For
descriptions of the measures and their calculations, see “TopPlan Strategic Target
planning measures” on page 94.

Wp AvgInv R

Ly AvgInv R

SCp AvgInv R

SOp AvgInv R

Calculated

Referenced

Referenced

Referenced

Wp AvgInv varLy R %

Calculated

Wp GM%

Ly GM%

SCp GM %

SOp GM %

Wp GM R

Ly GM R

SCp GM R

SOp GM R

Wp Mkd %

Ly Mkd %

SCp Mkd %

SOp Mkd %

Wp Mkd R

Ly Mkd R

SCp Mkd R

SOp Mkd R

Entered or calculated

Referenced

Referenced

Referenced

Calculated

Referenced

Referenced

Referenced

Entered or calculated

Referenced

Referenced

Referenced

Calculated

Referenced

Referenced

Referenced

32    TopPlan

Wp Mkd varLy R %

Calculated

Wp Sls R

Ly Sls R

SCp Sls R

SOp Sls R

Entered or calculated

Referenced

Referenced

Referenced

Wp Sls R varLy % R

Entered or calculated

Wp TO

SCp TO

SOp TO

Ly TO

Approval worksheet

Entered or calculated

Referenced

Referenced

Referenced

Workbook

Strategic Targets workbook

Worksheet 4: Plan Approval

Usage in process

Pre-season Planning

Process for using this worksheet

This worksheet lists all the measures involved in the plan approval process.
Review the activity surrounding who submitted a plan for approval, the date, the
plan version, whether the plan was approved or rejected, by whom, and any
comments made regarding the plan on this worksheet.

Measures

The Plan Approval worksheet contains the following measures. For descriptions
of the measures and their calculations, see “TopPlan Strategic Target planning
measures” on page 94.

Ra Version

Ra Version Date

Ra Submitted By

Ra Approve/Reject

Referenced

Referenced

Referenced

Referenced

Ra Approval Comment

Referenced

Ra Approved By

Referenced

 Chapter 3 – Workbook descriptions   33

Pre-Season Financial Plan workbook

The Pre-Season Financial Plan workbook is used to set up, adjust, reconcile, and
approve a pre-season financial plan.

The Pre-Season Financial Plan workbook contains the following worksheets:

•  Opening Inventory Setup worksheet

•  Annual Goals worksheet

•  Sales worksheet

•  Markdowns worksheet

•  Receipts and Inventory worksheet

•  Gross Margin worksheet

•  Summary  Values worksheet

•  Units and AUR worksheet

•  Summary  Units worksheet

•  Reconcile worksheet

•  Approval worksheet

Process for using this workbook

1  The workbook is built as part of the regular automated workbook build

processes. It can also be built manually by stepping through the Planning
Worksheets wizard. System Administrators can set up multiple pre-season
planning periods as needed  so that plan  workbooks may be built for any of
the defined time periods.

2  Use the Opening Inventory Setup worksheet to populate initial BOP retail,

cost and unit  inventory values in the workbook.

3  Review your annual goals and targets from the Executive or Manager roles

using the Annual Goals worksheet.

4  Plan sales revenue using the Sales worksheet. This worksheet includes many
variances and other sales amalysis measures like contribution to time and
product. You can enter the straight sales value and let all the other measures
recalculate, or enter every value.

5  Plan markdowns using the Markdowns worksheet. Enter values into any of

the markdown types and have the total markdowns calculated or enter the
markdown percent to sales for any of the markdown types and have the
markdowns  result.  Total markdowns and the total markdown percent may
also be edited.   Employee Discount and Shortage are also entered on this
worksheet.

34    TopPlan

6  Plan receipt and inventory values using the Receipt and Inventory worksheet.
BOP inventory, EOP inventory and Projected Receipts may all be edited as
well as the stock-to-sales ratio.  Additional inventory additions and
reductions can be planned on the worksheet as well: Returns to Vendor,
Transfers In, Transfers Out, Reclassifications In and Reclassifications Out.
Initial Markup Percents (IMU%) are entered for Projected Receipts, Returns
to Vendor, Transfers In and Out and Reclassifications In and Out.  Review
the resulting Cumulative Markup percent (CMU%).

7  Review the resulting gross margin using the Gross Margin worksheet. If an
issue is identified here, typically you go back and adjust values on other
planning worksheets.  However, a change can be entered into any field that
can be edited on this worksheet.

8  Review plan values on the Summary Values worksheet.

9  Plan units and average unit retail.

(cid:131)  On the Units and AUR worksheet, given your retail values, plan AUR
amounts to determine what your units will be or plan unit amounts to
determine what your AURs (Average Unit Retails) will be.  Edits to
either units or AURs will not change the retail values.

(cid:131)  On the Unit Summary worksheet, review the unit plan and variances.

10  Use the Reconcile worksheet to reconcile the plan to the target, summary

and/or LY plan versions.

11  Use the Approval worksheet to either submit the plan for approval (planner)
or to approve the plan that has been submitted for approval (manager).

 Chapter 3 – Workbook descriptions   35

Opening Inventory Setup worksheet

Workbook

Pre-Season Financial Plan workbook.

Worksheet 1: Opening Inventory Setup

Usage in process

Set initial period BOP retail, cost and unit inventories for the Pre-season
Planning process

Process for using this worksheet

Use the Opening Inventory Setup worksheet to populate initial inventory values
in the plan workbook.  This worksheet is used to populate the first planning
period of the workbook only.

1  Change the display of the window to show the Calendar in outline mode with

the ALL [Calendar] dimension displayed.

2  Enter BOPI R to set the first period BOP R.

3  Enter either the IMU BOPI R % or the BOPI C to set the first period BOP C.

4  Enter BOPI U to set the first period BOP U.   BOP AUR will calculate.

Measures

The Opening Inventory Setup worksheet contains the following measures. For
descriptions of these measures, see “TopPlan Financial planning measures (Pre-
Season and In-Season)”on page 99.

Wp BOPI R

Wp IMU BOPI R %

Wp BOPI C

Wp BOPI U

Wp BOP R

Wp BOP C

Wp BOP U

Wp BOP AUR

Entered

Entered

Entered

Entered

Entered or Calculated

Calculated

Calculated

Calculated

36    TopPlan

Annual Goals worksheet

Workbook

Pre-Season Financial Plan workbook.

Worksheet 2: Annual Goals

Usage in process

Initial view of Targets in the Pre-Season Planning process

Process for using this worksheet

1

Initial view of the annual goals and targets.  Compare the Targets to Last
Year and the initial seeded plan.  Compare Target Sales to Forecast Sales.

2  The plan is automatically seeded with Ly data as a starting point for key

planning metrics such as Sales, Markdowns, Shrink, Projected Receipts.

3  No direct action is expected to be taken on the worksheet.

4  Plan adjustments should be made on the appropriate workflow worksheets
that follow this.  However, full measure functionality exists such that edits
made on this worksheet are valid.

Measures

The Annual Goals worksheet contains the following measures. For descriptions
of these measures, see “TopPlan Financial planning measures (Pre-Season and
In-Season)”on page 99.

Wp AvgInv R

Ly AvgInv R

Tgt AvgInv R

Calculated

Referenced

Referenced

Wp AvgInv varLy R %

Calculated

Wp AvgInv varTgt R %

Calculated

Wp GM %

Ly GM %

Tgt GM %

Wp GM R

Ly GM R

Tgt GM R

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Wp Markkdown R %

Entered or Calculated

Ly Markkdown R %

Tgt Markkdown R %

Referenced

Referenced

Wp Markkdown R

Entered or Calculated

Ly Markkdown R

Referenced

 Chapter 3 – Workbook descriptions   37

Tgt Markkdown R

Referenced

Wp Sls R

Fcst Sls R

Ly Sls R

Tgt Sls R

Entered or calculated

Referenced

Referenced

Referenced

Wp Sls varFcst R %

Entered or calculated

Wp Sls varLy R %

Entered or calculated

Wp Sls varTgt R %

Entered or calculated

Wp TO

Ly TO

Tgt TO

Calculated

Referenced

Referenced

38    TopPlan

Sales Value worksheet

Workbook

Pre-Season Financial Plan workbook

Worksheet 3: Sales

Usage in process

To plan Sales, Sales Types and Customer Returns in the Pre-Season Planning
process

Process for using this worksheet

1  Sales are manipulated by input to either Sls R, Sls var Ly R, Sls var Fcst R,

Sls cont Time R, Sls cont Prod R, or Sls var Tgt R. This input can be entered
at all planning levels for Product. In the planner role, Sales can be planned by
regular, promotional and clearance sales types or  by any of following: the
contribution of the sales types to total Sales, sales type contribution to time,
sales type % variation to LY  .

2  All other metrics are calculated.

3  Review Sales Build Rate.

4  Optionally, Customer Returns can be planned on this worksheet.  Customer
Returns are added to total Sales to arrive at total Gross Sales demand.

Measures

The Sales Value worksheet contains the following measures. For descriptions of
these measures, see “TopPlan Financial planning measures (Pre-Season and In-
Season)”on page 99.

Wp Sls build rate R %

Calculated

Fcst Sls build rate R %

Referenced

Ly Sls build rate R %

Referenced

Wp Sls contProd R %

Entered or calculated

Fcst Sls contProd R %

Ly Sls contProd R %

Referenced

Referenced

Wp Sls contTime R %

Entered or calculated

Fcst Sls contTime R %

Referenced

Ly Sls contTime R %

Referenced

Wp Sls R

Fcst Sls R

Ly Sls R

Tgt Sls R

Entered or calculated

Referenced

Referenced

Referenced

Wp Sls varFcst R %

Entered or calculated

 Chapter 3 – Workbook descriptions   39

Wp Sls varLy R %

Entered or calculated

Wp Sls varTgt R %

Entered or calculated

Wp Fcst Sls varLy R %

Referenced

Wp Reg Sls R

Wp Promo Sls R

Wp Clr Sls R

Ly Reg Sls R

Ly Prom Sls R

Ly Clr Sls R

Entered or calculated

Entered or calculated

Entered or calculated

Referenced

Referenced

Referenced

Wp Reg Sls var Ly R %

Entered or calculated

Wp Prom Sls var Ly R %

Entered or calculated

Wp Clr Sls var Ly R %

Entered or calculated

Wp Reg Sls cont Ttl Sls R %  Entered or calculated

Wp Prom Sls cont Ttl Sls R %  Entered or calculated

Wp Clear Sls cont Ttl Sls R %  Entered or calculated

Wp Cust. Returns R

Calculated

Wp Cust. Returns R %

Entered or calculated

Ly  Cust. Returns R %

Referenced

Wp Cust. Ret var LY R %

Entered or calculated

Note:  Sales contTime R is used to calculate Sales cont of Week or Month to the
Season by displaying Week, Month and Season dimensions on the worksheet.

40    TopPlan

Markdowns worksheet

Workbook

Pre-Season Financial Plan workbook

Worksheet 4: Markdowns

Usage in process

To plan Markdowns, Markdown Types, Employee Discount and Shortage in the
Pre-Season Planning process

Process for using this worksheet

This worksheet shows the three types of markdowns: Promotional, Clearance,
and Permanent, in addition to the sum of the three markdown categories stated as
values and as  percentages of total Sales, plus Emplolyee Discount and Shrinkage
percentages and values.

1  Markdowns are the result of direct inputs to one of the three Markdown type

buckets or to total Markdowns either as a value input or as an input to
Markdown  Percents . With an input to Markdown percents,  Markdowns are
generated as a percent  to the sales value (Sls R).

2  Mkd Perm, Mkd Promo and Mkd Clear R can be manipulated, with the

Markdown percentages (Mkd %) for each recalculating. Mkd Perm %, Mkd
Promo % and Mkd Clear % may be manipulated, with the Markdown values
(Mkd Rs) for each recalculating.

3  Total Mkd R can be manipulated and Total Mkd %recalculates.  An edit to

total Mkd R is spread proportionally between Mkd Clear R and Mkd Perm R
while Mkd Promo is held.  Edits may also be made to Mkd R %.  Mkd
Promo is held and the increase/decrease to total markdowns is spread
proportionally to Mkd Clear R and Mkd Perm R.

4  Shrink % can be input, with Shrink R recalculating.

5    Optionally, Employee Discount % can be input with Employee Discount R

recalculating.

Measures

The Markdowns worksheet contains the following measures. For descriptions of
these measures, see “TopPlan Financial planning measures (Pre-Season and In-
Season)”on page 99.

Wp Sls R

Ly Sls R

Entered or calculated

Referenced

Wp Markkdown R %

Entered or Calculated

Ly Markkdown R %

Tgt Markkdown R %

Referenced

Referenced

Wp Markkdown R

Entered or Calculated

Ly  Markkdown R

Referenced

 Chapter 3 – Workbook descriptions   41

Tgt Markkdown R

Referenced

Wp Mkd Clear R %

Entered or calculated

Ly Mkd Clear R %

Referenced

Wp Mkd Clear R

Ly Mkd Clear R

Entered or calculated

Referenced

Wp Mkd Perm R %

Entered or calculated

Ly Mkd Perm R %

Referenced

Wp Mkd Perm R

Ly Mkd Perm R

Entered or calculated

Referenced

Wp Mkd Promo R %

Entered or calculated

Ly Mkd Promo R %

Referenced

Wp Mkd Promo R

Entered or calculated

Ly Mkd Promo R

Referenced

Wp Shrink R %

Ly Shrink R %

Wp Shrink R

Ly Shrink R

Entered or calculated

Referenced

Calculated

Referenced

Wp Empl Disc R %

Entered or calculated

Ly Empl Disc R %

Wp Empl Disc R

Ly Empl Disc R

Referenced

Calculated

Referenced

42    TopPlan

Inventory and Receipt Value worksheet

Workbook

Pre-Season Financial Plan workbook

Worksheet 5: Receipts and Inventory

Usage in process

To plan receipts and Inventory in the Pre-season Planning process

Process for using this worksheet

1  Edit  ProjRec R to derive a new EOP R. A Projected Receipt edit will flow
through to all forward EOP R’s and BOP R’s.  Enter in the IMU ProjRec R
%.  ProjRec C will calculate.

(cid:131)  By smoothing EOP R,, Projected Receipts are shifted between the period
the edit is made and the following period.  The next periods Stk/Sls R is
recalculated and the ProjRec R for the current and following periods
adjust.

(cid:131)  Edits to BOP R will also shift Projected Receipts between the period the
edit is made and the prior period.  The prior periods EOP R adjusts to
match the BOP R edit, the current periods Stk/Sls R recalculates and
ProjRec R for the current and prior periods adjusts.

(cid:131)  Edits to SlsR, Markdowns R, Shrink R and Empl Disc R will reclaculate

Projected Receipts to hold the current periods EOP R.

(cid:131)  Edits to Return to Vendor R derive new EOP R’s.  Projected Receipts do
not recalculate with an edit to Return to Vendor R.  Enter in the IMU
Return to Vendor R %.  Return to Vendor C will calculate.

2  Change Stk/Sls R to derive a new BOP R; ProjRec R for the prior and current

periods recalc and shift to accommodate the new BOP R.

3

Input Transfer In R, Transfer Out R, Reclass In R and Reclass Out R to
derive a new EOP R.  Projected Receipts do not reclaculate with edits to
Transfers or Reclassifications.  Enter in the IMU Transfer In R %,  IMU
Transfer Out R %,  IMU Reclass In R % and the IMU Reclass Out R %.
Transfer In C, Transfer Out C, Reclass In C and Reclass Out C  will
calculate.

4  Review the Ttl Available CMU% that has been derived.

5  Review the AvgInv R, TO, Stk/Sls and WOS.

 Chapter 3 – Workbook descriptions   43

Measures

The Receipt and Inventory  worksheet contains the following measures. For
descriptions of these measures, see “TopPlan Financial planning measures (Pre-
Season and In-Season)”on page 99.

Wp Sls R

Wp BOP R

Ly BOP R

Wp BOP varLy R %

Entered or calculated

Entered or Calculated

Referenced

Calculated

Wp ProjRec R

Entered or calculated

Ly Recvd R

Referenced

Ly ProjRec varRecvd R

Calculated

Wp TtlRec R

Wp IMU% Proj Rec

Ly IMU% Recvd

Wp IMU%

Calculated

Entered

Referenced

Calculated

Wp Return to Vendor R

Entered

Ly Return to Vendor R

Referenced

Wp IMU% RTV

Ly IMU% RTV

Wp Transfer In R

Ly  Transfer In R

Wp Transfer Out R

Ly  Transfer Out R

Entered or calculated

Referenced

Entered

Referenced

Entered

Referenced

Wp IMU Trans In R %

Entered or calculated

Wp IMU Trans Out R %

Entered or calculated

Wp Reclass In R

Entered or calculated

Wp Reclass Out R

Entered or calculated

Ly Reclass In R

Ly Reclass Out R

Referenced

Referenced

Wp IMU Reclass In R %

Entered or calculated

Wp IMU Reclass  Out R %

Entered or calculated

Wp EOP R

Ly EOP R

Wp EOP varLy R %

Wp CMU%

Entered or calculated

Referenced

Calculated

Calculated

44    TopPlan

Ly CMU%

Wp Stk/Sls

Ly Stk/Sls

Wp AvgInv R

Ly AvgInv R

Tgt AvgInv R

Referenced

Entered or calculated

Referenced

Calculated

Referenced

Referenced

Wp AvgInv var Ly R %

Calculated

Wp AvgInv var Tgt R %

Calculated

Wp TO

Ly TO

Tgt TO

Wp WOS

Ly WOS

Wp SellThru R%

Ly SellThru R%

Calculated

Referenced

Referenced

Calculated

Referenced

Calculated

Referenced

 Chapter 3 – Workbook descriptions   45

 Gross Margin worksheet

Workbook

Pre-Season Financial Plan

Worksheet 6: Gross Margin

Usage in process

Review Gross Margin in the Pre-season Planning process

Process for using this worksheet

1  Enter/adjust IMU ProjRec % at lower time and product levels.

2  As desired, adjust Sls R, Markdown R %, Empl Disc R %, Shrink R % or

ProjRec R.

3  Review GM, GM%, Ttl Available CMU % and GMROI.

Measures

The Gross Margin worksheet contains the following measures. For descriptions
of these measures, see “TopPlan Financial planning measures (Pre-Season and
In-Season)”on page 99.

Wp CMU %

Ly CMU %

Tgt CMU %

Wp GM %

Ly GM %

Tgt GM %

Wp GM R

Ly GM R

Tgt GM R

Wp GMROI

Ly GMROI

Wp IMU ProjRec %

Ly IMU Recvd %

Wp ProjRec R

Ly Recvd R

Wp TtlRec R

Wp IMU R %

Wp Sls R

Wp Mkd R %

Wp Shrink %

Wp Empl Disc R %

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Entered

Referenced

Entered or calculated

Referenced

Calculated

Calculated

Entered or calculated

Entered or Calculated

Entered or calculated

Entered or calculated

46    TopPlan

Summary – Values worksheet

Workbook

Pre-Season Financial Plan workbook

Worksheet 7: Summary Values

Usage in process

To view the Value Plan Summary in the Pre-season Planning process

Process for using this worksheet

1  Review plan values with the ability to adjust numbers if needed.

2  Compare plan variances to LY.

Measures

The Summary Values worksheet contains the following measures. For
descriptions of these measures, see “TopPlan Financial planning measures (Pre-
Season and In-Season)”on page 99.

Wp BOP R

Ly BOP R

Wp Sls R

Ly Sls R

Calculated

Referenced

Entered or calculated

Referenced

Wp Sls varLy R %

Entered or calculated

Wp Cust Returns R %

Entered or Calculated

Ly  Cust Returns R %

Referenced

Wp Mkd %

Ly Mkd %

Wp Mkd R

Ly Mkd R

Wp Mkd varLy R %

Wp Empl Disc R %

Ly Empl Disc R %

Wp ProjRec R

Ly Recvd R

Calculated

Referenced

Calculated

Referenced

Calculated

Entered

Referenced

Entered or calculated

Referenced

Wp IMU ProjRec %

Entered

Ly IMU Recvd %

Wp CMU %

Ly CMU %

Wp EOP R

Referenced

Calculated

Referenced

Entered or calculated

 Chapter 3 – Workbook descriptions   47

Ly EOP R

Wp EOP varLy R %

Wp GM %

Ly GM %

Wp GM R

Ly GM R

Wp GMROI

Ly GMROI

Wp AvgInv R

Ly AvgInv R

Wp TO

Ly TO

Referenced

Calculated

Calculated

Referenced

Calculated

Referenced

Calculated

Referenced

Calculated

Referenced

Calculated

Referenced

48    TopPlan

 Units and AUR worksheet

Workbook

Pre-Season Financial Plan workbook

Worksheet 8: Units and AUR

Usage in process

Convert the value plan to a unit plan in the Pre-season Planning process

Process for using this worksheet

1

2

Input Sls AUR, Shrink AUR,  ProjRec AUR, Returns to Vendor AUR,
Transfer In AUR, Transfer Out AUR, Reclass In AUR and Reclass Out AUR
to derive Sls U, Shrink U, ProjRec U, Return to Vendor U, Transfer In U,
Transfer Out U, Reclass In U and Reclass Out U.  This calculation derives
EOP U and EOP AUR.

Input SlsU,  ProjRecU, Return to Vendor U, Transfer In U, Transfer Out U,
Reclass In U or Reclass Out U to derive SlsAUR,  ProjRecAUR, Return to
Vendor AUR, Transfer In AUR, Transfer Out AUR, Reclass In AUR and
Reclass Out AUR.  This calculation derives EOP U and EOP AUR.

3  Optionally, input Cust Returns AUR to derive Cust Returns U or input Cust

Returns U to derive Cust Returns AUR.

(cid:131)  Planners can also enter Reg Sls AUR, Promo Sls AUR and Clr Sls AUR

to derive Reg Sls U, Promo Sls U, Clr Sls U, Sls U and Sls AUR.

4  Review AvgInv U, TO U, Stk/Sls U, SellThru U and WOS U.

Measures

The Units and AUR worksheet contains the following measures. For descriptions
of these measures, see “TopPlan Financial planning measures (Pre-Season and
In-Season)”on page 99.

Wp BOP AUR

Ly BOP AUR

Wp BOP U

Ly BOP U

Wp BOP R

Ly BOP R

Wp Sls AUR

Ly Sls AUR

Wp Sls U

Ly Sls U

Wp Sls R

Ly Sls R

Calculated

Referenced

Calculated

Referenced

Entered or calculated

Referenced

Entered or calculated

Referenced

Entered or calculated

Referenced

Entered or calculated

Referenced

 Chapter 3 – Workbook descriptions   49

Wp SlsU contProd U %

Calculated

Ly SlsU contProd U %

Referenced

Wp SlsU contTime U %

Calculated

Ly SlsU contTime U %

Referenced

Wp Cust Returns R %

Entered

Wp Cust Returns R

Calculated

Wp Cust Returns AUR

Entered or calculated

Wp Cust Returns U

Entered or calculated

Wp Shrink %

Wp Shrink R

Wp Shrink AUR

Wp Shrink U

Wp ProjRec R

Entered or calculated

Calculated

Entered or calculated

Calculated

Entered or calculated

Wp ProjRec AUR

Entered or calculated

Wp ProjRec U

Entered or calculated

Ly Recvd R

Ly Recvd AUR

Ly Recvd U

Referenced

Referenced

Referenced

Wp Return to Vendor R

Entered or calculated

Wp Return to Vendor AUR

Entered or calculated

Wp Return to Vendor U

Entered or calculated

Ly Return to Vendor R

Referenced

Ly Return to Vendor U

Referenced

Wp Transfer In R

Entered or calculated

Wp Transfer In AUR

Entered or calculated

Wp Transfer In U

Ly Transfer In U

Entered or calculated

Referenced

Wp Transfer Out R

Entered or calculated

Wp Transfer Out AUR

Entered or calculated

Wp Transfer Out U

Entered or calculated

Ly Transfer Out U

Referenced

Wp Reclass In R

Entered or calculated

Wp Reclass In AUR

Entered or calculated

Wp Reclass In U

Ly Reclass In U

Entered or calculated

Referenced

50    TopPlan

Wp Reclass Out R

Entered or calculated

Wp Reclass Out AUR

Entered or calculated

Wp Reclass Out U

Entered or calculated

Ly Reclass Out U

Wp EOP AUR

Wp EOP U

Ly EOP U

Wp EOP R

Wp AvgInv U

Ly AvgInv U

Wp SellThru U %

Ly SellThru U  %

Wp Stk/Sls U

Ly Stk/Sls U

Wp TO U

Ly TO U

Wp WOS U

Ly WOS U

Referenced

Calculated

Calculated

Referenced

Entered or calculated

Calculated

Referenced

Calculated

Referenced

Entered or calculated

Referenced

Calculated

Referenced

Calculated

Referenced

Wp Reg Sls R

Entered or calculated

Wp Reg Sls AUR

Entered or calculated

Wp Reg Sls U

Wp Promo Sls R

Entered or calculated

Entered or calculated

Wp Promo Sls AUR

Entered or calculated

Wp Promo Sls U

Entered or calculated

Wp Clr Sls R

Entered or calculated

Wp Clr Sls AUR

Entered or calculated

Wp Clr Sls U

Entered or calculated

Wp Reg Sls var LY Sls U %

Calculated

Wp Promo Sls var LY Sls U %  Calculated

Wp Clr Sls var LY Sls U %

Calculated

 Chapter 3 – Workbook descriptions   51

Summary Units worksheet

Workbook

Pre-Season Financial Plan workbook

Worksheet 9: Summary Units

Usage in process

To view the Unit Plan Summary in the Pre-season Planning process

Process for using this worksheet

1  Review plan units and adjust numbers as needed.

2  Compare plan variances to LY.

Measures

The Summary Units worksheet contains the following measures. For descriptions
of these measures, see “TopPlan Financial planning measures (Pre-Season and
In-Season)”on page 99.

Wp BOP U

Wp BOP AUR

Ly BOP U

Wp Sls U

Ly Sls U

Wp SlsU varLy %

Wp Sls AUR

Ly Sls AUR

Wp SlsAUR varLy %

Wp Shrink U

Ly Shrink U

Calculated

Referenced

Referenced

Entered or calculated

Referenced

Calculated

Entered

Referenced

Calculated

Calculated

Referenced

Wp ProjRec U

Entered or calculated

Wp ProjRec AUR

Entered or calculated

Ly Recvd U

Ly Recvd AUR

Referenced

Referenced

Wp Return to Vendor U

Entered or calculated

Ly Return to Vendor U

Referenced

Wp Transfer In U

Entered or calculated

Wp Transfer Out U

Entered or calculated

Wp EOP AUR

Ly EOP AUR

Calculated

Referenced

52    TopPlan

Wp EOP U

Ly EOP U

Wp EOP U varLy %

Wp AvgInv U

Ly AvgInv U

Wp SellThru U %

Ly SellThru U %

Wp Stk/Sls U

Ly Stk/Sls U

Wp TO U

Ly TO U

Wp WOS U

Ly WOS U

Calculated

Referenced

Calculated

Calculated

Referenced

Calculated

Referenced

Entered or calculated

Referenced

Calculated

Referenced

Calculated

Referenced

 Chapter 3 – Workbook descriptions   53

Reconcile worksheet

Workbook

Pre-Season Financial Plan workbook

Worksheet 10: Reconcile

Usage in process

To compare plan to Targets, LY and/or Summary plan versions in the Pre-season
Planning process

Process for using this worksheet

The Reconcile worksheet is used for reconciling plan values to Target, LY and
Summary values. This worksheet is used by Planners reconciling to the Managers
Targets, and by Managers reconciling Planners’ data in a Summary version and/
or Strategic Targets set by Executives.

1  Adjust Sls R or Sls varTgt R %  as needed.

2  Adjust Markdowns R % as needed. The system calculates Markdowns R.

3  Adjust ProjRec R as needed. This calculates EOP R, AvgInv R, and TO.

4  Adjust IMU ProjRec % as needed. The system calculates GM R and GM R

%.

For more information about plan reconciliation and approval, see page 11.

Measures

The Reconcile worksheet contains the following measures. SWa measures are
only in the Managers workbook. Not all Tgt measures are available in the
Managers workbook because the Executive does not set Targets for the full set of
planning metrics. For descriptions of these measures, see “TopPlan Financial
planning measures (Pre-Season and In-Season)”on page 99.

Tgt BOP R

Wp BOP R

SWa BOP R

Tgt Sls R

Wp Sls R

SWa Sls R

Referenced

Entered or calculated

Referenced

Referenced

Entered or calculated

Referenced

Wp Sls varTgt R %

Entered or calculated

Wp Sls varSWa R %

Entered or calculated

Tgt Mkd R

Tgt Mkd %

Wp Mkd R

Wp Mkd %

Referenced

Referenced

Calculated

Calculated

54    TopPlan

Wp Mkd varTgt R %

SWa Mkd R

SWa Mkd %

Wp Mkd varSWa R %

Tgt ProjRec R

Wp ProjRec R

Calculated

Referenced

Referenced

Calculated

Referenced

Entered or calculated

Wp ProjRec varTgt R  %

Calculated

SWa ProjRec R

Referenced

Wp ProjRec varSWa R %

Calculated

Wp IMU ProjRec R %

Entered or calculated

SWa IMU ProjRec R %

Referenced

Tgt IMU R %

Wp IMU R %

Referenced

Calculated

Tgt Ttl Available CMU R %

Referenced

Wp Ttl Available CMU R %  Calculated

SWa Ttl Available CMU R %  Referenced

Tgt EOP R

Wp EOP R

Referenced

Entered or calculated

Wp EOP var Tgt R %

SWa EOP R

Calculated

Referenced

Wp EOP var SWa R %

Calculated

Tgt AvgInv R

Wp AvgInv R

SWa AvgInv R

Tgt TO

Wp TO

SWa TO

Wp GM %

SWa GM %

Tgt GM %

Wp GM R

SWa GM R

Tgt GM R

Wp GM varSWa R %

Wp GM varTgt R %

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Calculated

 Chapter 3 – Workbook descriptions   55

Approval worksheet

Workbook

Pre-Season Planning workbook

Worksheet 11: Plan Approval

In-Season Planning workbook

Worksheet 12: Plan Approval

Process for using this worksheet

The Plan Approval worksheet is used to submit plans for approval, to approve
submitted plans, and view status of submitted plans. Your planning role
determines the range of actions you can perform on this worksheet. For example,
if you are in the Planner role, you can only submit plans for approval on the
worksheet and view the status of the submitted plan. If you are in the Manager
role, you can approve or reject submitted plans. A separate version, Submitted
Waiting for Approval (Swa), is provided for the Manager to view the plans
submitted for approval from the Planner role. Separate versions, Submitted
Original Plan (SOp) and Submitted Current Plan (SCp), are provided for the
Manager and Executive to view the Planners approved Original Plan (Op) and
Current Plan (Cp) versions.

This worksheet provides a list of plan versions applicable to your role, and the
status associated with each plan.  Depending on your planning role, you can
amend the plan status to indicate whether a plan is ready for approval, has been
approved, or has been rejected.  When the Pre-Season or In-Season Planning
workbook is committed, version changes and approvals are processed.

For pre-season planning, the approval process promotes the plan from Submitted
Waiting for Approval to both  Original Plan (Op) and Current Plan (Cp). For in-
season planning, the approval process promotes the plan from Submitted Waiting
for Approval only to  Current Plan (Cp). The Original Plan approved during the
pre-season planning process is considered the locked “plan of record” and no
changes are be made to it.  The frequency of the plan version change is different
for each season – usually once for pre-season and monthly or as desired for in-
season.

There are several ways to use this worksheet, depending on your planning role
and the approval step you are performing.

Submit a plan for approval (Planner)

1  Fill Submit check boxes to submit plan for approval at the Department level.

2  Commit and Save the workbook. This action populates the Submitted By and

Version Date fields, and changes the plan version to Wa (Waiting for
Approval).

56    TopPlan

Approve or reject a submitted plan (Manager)

1  On the Approval worksheet, note the change in plan version on the Reference
Administration Version (Ra Version) to Waiting for Approval (Wa), and the
population of Version Date and Submitted By fields.

2  Review the plan Submitted Waiting for Approval on the Reconcile

worksheet in the SWa plan version.  Compare the SWa plan to Strategic
Targets and Managers Plan.

3  Select Approve or Reject from the Approve/Reject drop-down box on the

Approval worksheet.

4  Enter Approval Comment as desired.

5  Commit and Save the workbook. This action populates the Approved By

field and changes the plan version to WA.

View status of a submitted plan (Planner)

1  Refresh the workbook.

2  On the Approval worksheet, note population of information into the Ra
Approve/Reject, Ra Approved By, and Ra Approval Comment fields.

Note: The plan version changes from Waiting for Approval (Wa) to Wp, that
the Submit checkboxes change from checked to unchecked state and that the
Submitted By has cleared out.

3  Review the approved plan in the Original Plan (Op) and/ or the Current Plan

(Cp) versions on another worksheet.

For more information about plan reconciliation and approval, see page 11.

Measures

The Approval Worksheet contains the following measures. Measures are editable
based on the user’s planning role.  Values entered in this worksheet are extracted
and used in other parts of the system.

Submit

A check box used to indicate submitted plan.

Version

The plan version displayed shows whether a plan has been submitted for
approval or not.  If a plan has not been submitted for approval, the Ad
Version will display WP.  If a plan has been submitted and is waiting for
approval, the Ad Version will display WA.

Version Date

The date that the plan  was submitted.

Submitted By

The user submitting the plan for approval is displayed after the workbook has
been committed.

 Chapter 3 – Workbook descriptions   57

Approve/Reject

The indication of the manager’s approval decision.

Approved By

The user approving or rejecting the plan is displayed after a manager has
taken  action on a plan submitted for approval.

Approval Comment

A text field in which the manager can enter notes regarding the approval or
rejection of a specific plan.

58    TopPlan

In-Season Financial Plan workbook

The In-Season Financial Plan workbook is used to set up, adjust, reconcile, and
approve an in-season financial plan. The worksheets in this workbook show you
how the trading season is performing relative to plan. Actuals are updated
weeklyalong with the generation of a new demand sales forecaste (Fcst). The
most recent approved Current Plan (Cp (SCp)) and Last Year (Ly) values are also
displayed within the workbook. You can adjust plan values to see the results of
such changes, and re-plan as needed. When the new plan is approved, it
overwrites the Current Plan (Cp (SCp)).  The Original Plan approved during the
Pre-Season planning process is never changed. The OTB worksheets help you
control OTB and identify opportunities and actions.

The In-Season Financial Plan workbook contains the following worksheets:

•  Trend worksheet

•  Sales  worksheet

•  Markdowns worksheet

•  Receipt worksheet

•

Inventory worksheet

•  Gross Margin worksheet

•  Summary Values worksheet

•  Units and AUR worksheet

•  Summary Units worksheet

•  Reconcile worksheet

•  Value OTB worksheet

•  Unit OTB worksheet

•  Approval worksheet

Process for using this workbook

 Chapter 3 – Workbook descriptions   59

1  The workbook is built as part of the regular automated workbook build

processes. It can also be built manually by stepping through the Planning
Worksheets wizard.  On each worksheet the Current Plan (Cp (SCp)) version
is displayed in addition to actuals and LY.  As needed, users can call out the
Original Plan (Op (SOp)) version for the measures that they wish to see.

2  Review current trends and forecasted sales on the Trend worksheet. This
worksheet provides a snapshot of the current state of many of the key
planning performance indicators,  including  variances to LY and Current
Plan (CP (SCp)).

3  On the Sales worksheet, review values and change variances or change sales

values for any forward time period in the workbook.

4  Review markdowns using the Markdowns worksheet.   Enter values into any
of the markdown types for any forward time period in the workbook and
have the total markdowns calculated or enter the markdown percent to sales
for any of the markdown types and have the  markdowns  result.  Total
markdowns and the total markdown percent may also be edited.   Employee
Discount and Shortage are also entered on this worksheet.

5  Review actual receipts, future projected receipts and future on-order using

the Receipt worksheet.  Projected Receipts may all be adjusted for future
time periods in the workbook as necessary to maintain a balanced stock/sales
position.  View the Initial Markup Percents (IMU%) for receipts and on-
order.  IMU Percents many be adjusted for Projected Receipts in future time
periods.  To provide the most an accurate look at complete On- Order,
Commitments and On-Order Cancel measures may be used to account for
orders that have been placed and/or cancelled since the last on-order feed.
Review the resulting Cumulative Markup percent (CMU%).

6  Review inventory and receipt values using the Inventory worksheet.  BOP

inventory, EOP inventory and Projected Receipts may all be edited as well as
the stock-to-sales ratio for future time periods in the workbook.  Additional
inventory additions and reductions can be adjusted on the worksheet as well:
Returns to Vendor, Transfers In, Transfers Out, Reclassifications In and
Reclassifications Out.  Initial Markup Percents (IMU%) are entered for
Projected Receipts, Returns to Vendor, Transfers In and Out and
Reclassifications In and Out.  Review the resulting Cumulative Markup
percent (CMU%).

7  Review the resulting  gross margin using the Gross Margin worksheet.  If an
issue is identified here, typically you go back and adjust values on other
planning worksheets.  However, a change can be entered into any field that
can be edited on this worksheet.

8  Review all values on the Plan Summary Values worksheet. This worksheet is
similar to the Plan Summary – Values worksheet for pre-season planning
with the addition of the Current Plan (Cp (SCp)) version.

60    TopPlan

9  Review units and average unit retail.

(cid:131)  On the Units and AUR worksheet, review actual values and AUR’s.

Adjust future AUR amounts to re-plan future units or adjust unit amounts
to recalc the AURs (Average Unit Retails).  Edits to either units or AURs
will not change any of the retail values.

(cid:131)  On the Unit Summary worksheet, review the adjusted unit plan and

variances.

10  Use the Reconcile worksheet to reconcile the adjusted plan to LY, the last

approved Current Plan and/or Summay versions.

11  Use the Value OTB and Unit OTB worksheets to review and determine

future Open to Buy action.

12  Use the Approval worksheet to either submit the plan for approval to Current
Plan (planner) or to approve the plan that has been submitted as the most
recent Current Plan  (manager).

 Chapter 3 – Workbook descriptions   61

Trend worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 1: Review Trend

Usage in process

Review actual results, current trends and forecasted sales in the In-Season
Planning process.

Process for using this worksheet

The Trend worksheet is used to initially review the actual trading results of
during the in-season trading period against the Current Plan and Last Year’s
trading results.

1  Review results against the Current Plan (Cp) or Submitted Plan (SCp) and

Last Year (Ly).

2

Initial view of the annual goals and targets.  Compare the Targets to Last
Year and the initial seeded plan.  Compare Target Sales to Forecast Sales.

3  The plan is automatically seeded with Ly data as a starting point for key

planning metrics such as Sales, Markdowns, Shrink, Projected Receipts.

4  No direct action is expected to be taken on the worksheet.

5  Plan adjustments should be made on the appropriate workflow worksheets
that follow this.  However, full measure functionality exists such that edits
made on this worksheet are valid.

Measures

The Review Current Trend worksheet contains the following measures. For
descriptions of these measures, see “TopPlan Financial planning measures (Pre-
Season and In-Season)”on page 99.

Wp Sls R

Cp (SCp) Sls R

Fcst Sls R

Ly Sls R

Entered or calculated

Referenced

Referenced

Referenced

Wp Sls varCp (SCp) R %

Entered or calculated

Wp Sls varFcst R %

Entered or calculated

Wp Sls varLy R %

Entered or calculated

Wp Cust Returns R %

Entered

Cp (SCp) Cust Returns R %

Referenced

Ly Cust Returns R %

Wp Markdowns R %

Referenced

Calculated

62    TopPlan

Cp (SCp) Markdowns R %

Referenced

Ly Markdowns R %

Wp Markdowns R

Referenced

Calculated

Cp (SCp) Markdowns R

Referenced

Ly Markdowns R

Referenced

Wp Mkd varCp (SCp) R %

Calculated

Wp Mkd varLy R %

Calculated

Wp Ttl Rec R

Entered or calculated

Cp (SCp) Ttl Rec R

Ly Ttl Rec R

Wp IMU %

Ly IMU %

Cp (SCp) IMU %

Wp EOP R

Cp (SCp) EOP R

Ly EOP R

Referenced

Referenced

Calculated

Referenced

Referenced

Entered or calculated

Referenced

Referenced

Wp EOP varCp (SCp) R %

Calculated

Wp EOP varLy R %

Wp GM %

Cp (SCp) GM %

Ly GM %

Wp GM R

Cp (SCp) GM R

Ly GM R

Calculated

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Wp GM varCp (SCp) R %

Calculated

Wp GM varLy R %

Wp AvgInv R

Cp (SCp) AvgInv R

Ly AvgInv R

Wp TO

Cp (SCp) TO

Ly TO

Calculated

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

 Chapter 3 – Workbook descriptions   63

Sales worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 2: Sales

Usage in process

To review Sales, Sales Types and Customer Returns in the In-Season Planning
process

Process for using this worksheet

1  Review and adjust Sales.  Sales are manipulated by input to either Sls R, Sls
var Ly R, Sls var Fcst R, Sls cont Time R, Sls cont Prod R, or Sls var Tgt R
for forward time periods. This input can be entered at all planning levels for
Product. In the planner role, Sales can be adjusted either by regular,
promotional and clearance sales types or  by any of following: the
contribution of the sales types to total Sales, sales type contribution to time,
sales type % variation to LY  .

2  All other metrics are calculated.

3  Review Sales Build Rate.

4  Optionally, Customer Returns can be adjusted on this worksheet.  Customer
Returns are added to total Sales to arrive at total Gross Sales demand.

Measures

The Plan Sales Value worksheet contains the following measures. For
descriptions of these measures, see “TopPlan Financial planning measures (Pre-
Season and In-Season)”on page 99.

Wp Sls R

Cp (SCp) Sls R

Fcst Sls R

Ly Sls R

Entered or calculated

Referenced

Referenced

Referenced

Cp (SCp) Sls var Fcst R %

Calculated

Cp (SCp) Sls var Ly R %

Calculated

Fcst Sls varLy R %

Referenced

Wp Sls varCp (SCp) R

Entered or calculated

Wp Sls varFcst R %

Entered or calculated

Wp Sls varLy R %

Entered or calculated

Wp Sls build rate R %

Calculated

Cp (SCp) Sls build rate R %

Referenced

Fcst Sls R build rate R %

Referenced

64    TopPlan

Ly Sls build rate R %

Referenced

Wp Sls contProd R %

Entered or Calculated

Cp (SCp) Sls contProd R %

Referenced

Fcst Sls contProd R %

Ly Sls contProd R %

Referenced

Referenced

Wp Sls contTime R %

Entered or Calculated

Cp (SCp) Sls contTime R %

Referenced

Fcst Sls contTime R %

Referenced

Ly Sls contTime R %

Referenced

 Chapter 3 – Workbook descriptions   65

Markdowns worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 3: Markdowns

Usage in process

To review Markdowns, Markdown Types, Employee Discount and Shortage in
the In-Season Planning process

Process for using this worksheet

Review the three types of markdowns: Promotional, Clearance, and Permanent,
in addition to the sum of the three markdown categories stated as values and as
percentages of total Sales, plus Emplolyee Discount and Shrinkage percentages
and values.

Markdowns are the result of direct inputs to one of the three Markdown type
buckets or to total Markdowns either as a value input or as an input to Markdown
Percents. With an input to Markdown percents, Markdowns are generated as a
percent to the sales value (Sls R).

1  Mkd Perm, Mkd Promo and Mkd Clear R can be manipulated, with the

Markdown percentages (Mkd %) for each recalculating. Mkd Perm %, Mkd
Promo % and Mkd Clear % may be manipulated, with the Markdown values
(Mkd Rs) for each recalculating.

2  Total Mkd R can be manipulated and Total Mkd R %recalculates.  An edit to
total Mkd R is spread proportionally between Mkd Clear R and Mkd Perm R
while Mkd Promo R is held.  Edits may also be made to Mkd R %.  Mkd
Promo R is held and the increase/decrease to total markdowns is spread
proportionally to Mkd Clear R and Mkd Perm R.

3  Shrink % can be input, with Shrink R recalculating.

4  Optionally, Employee Discount % can be input with Employee Discount R

recalculating.

Measures

The Markdowns worksheet contains the following measures. For descriptions of
these measures, see “TopPlan Financial planning measures (Pre-Season and In-
Season)”on page 99.

Wp Sls R

Cp (SCp) Sls R

Ly Sls R

Wp Markdown R %

Entered or calculated

Referenced

Referenced

Calculated

Cp (SCp) Markdown R %

Referenced

Ly Markdown R %

Wp Markdown R

Referenced

Calculated

66    TopPlan

Cp (SCp) Markdown R

Referenced

Ly Markdown R

Referenced

Wp Mkd Clear R %

Entered or calculated

Cp (SCp) Mkd Clear R %

Referenced

Wp Mkd Clear R

Entered or calculated

Cp (SCp) Mkd Clear R

Referenced

Wp Mkd Perm R %

Entered or calculated

Cp (SCp)Mkd Perm R %

Referenced

Wp Mkd Perm R

Entered or calculated

Cp (SCp) Mkd Perm R

Referenced

Wp Mkd Promo R %

Entered or calculated

Cp (SCp) Mkd Promo R %

Referenced

Wp Mkd Promo R

Entered or calculated

Cp (SCp) Mkd Promo R

Referenced

Wp Shrink %

Ly Shrink %

Cp (SCp) Shrink %

Entered

Referenced

Referenced

Wp Empl Disc R %

Entered or calculated

Wp Empl Disc R

Ly Empl Disc R %

Calculated

Referenced

Cp (SCp) Empl Disc R %

Referenced

 Chapter 3 – Workbook descriptions   67

Receipt worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 4: Receipt

Usage in process

Review actual amounts Received, future On-Order and Projected Receipts in the
In-Season Planning process

Process for using this worksheet

1  Review Received R and the cooresponding IMU% for Received that have

occurred in elapsed time periods against the Current Plan Total Receipts  (Cp
Total Receipts R and Cp IMU% Received.).

2  Review future period On-Order R and the IMU% for On Order against the
Current Plan Projected Receipts for future periods (Cp Proj Receipt and Cp
IMU% Projected Receipt).  Adjust Wp Projected Receipts and the IMU%
Projected Receipts for future time peiods as necessary.  Edits to Projected
Receipts impact Total Receipts, IMU %, CMU % and EOP Inventory.

3  As necessary, input On Order Cancel R and Commitments R in future time
periods to reflect order commitments and cancellations that have occurred
since the last On Order was loaded.  Edits to Commitments and On Order
Cancel will increase or decrease the amount of Open to Buy available; they
do not impact Total or Projected Receipts.

Measures

The Receipt  Worksheet contains the following measures. For descriptions of
these measures, see “TopPlan Financial planning measures (Pre-Season and In-
Season)”on page 99.

Wp Sls R

Cp (SCp) Sls R

Ly Sls R

Wp BOP R

Cp (SCp) BOP R

Ly BOP R

Entered or Calculated

Referenced

Referenced

Entered or Calculated

Referenced

Referenced

Wp Ttl Available CMU%

Calculated

CP (SCp) Ttl Available CMU% Referenced

Ly Ttl Available CMU%

Referenced

Wp Commitmnts R

Entered

CP (SCp)Commitmnts R

Referenced

Wp IMU %

Calculated

68    TopPlan

CP (SCp) IMU %

Ly IMU%

Referenced

Referenced

Wp IMU% Commitmnts

Entered

CP (SCp) IMU% Commitmnts  Referenced

CP (SCp) IMU% On Order

Referenced

Wp IMU% On Order Cxl

Entered

CP (SCp) IMU% On Order Cxl  Referenced

Wp IMU% Proj Rec

Entered

CP (SCp) IMU% Proj Rec

Referenced

Wp IMU% Recvd

Referenced

Cp (SCp) IMU% Recvd

Referenced

Ly IMU% Recvd

Wp IMU% On Order

Referenced

Referenced

Wp On Order Cxl R

Entered

CP (SCp) On Order Cxl R

Referenced

Wp On Order R

Fed

CP (SCp) On Order R

Referenced

Wp ProjRec R

Entered or calculated

CP (SCp) ProjRec R

Referenced

Wp Recvd R

CP (SCp) Recvd R

Ly Recvd R

Wp TtlRec R

Cp (SCp) TtlRec R

Ly Ttl Rec R

Fed

Referenced

Referenced

Calculated

Referenced

Referenced

 Chapter 3 – Workbook descriptions   69

Inventory worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 5: Inventory

Usage in process

To review Inventory additions and reductions during the In-season Planning
process

Process for using this worksheet

1  Adjust ProjRec R to derive a new EOP R. A Projected Receipt edit will flow

through to all forward EOP R’s and BOP R’s.  Enter in the IMU ProjRec R
%.  ProjRec C will calculate.

2  By smoothing EOP R,, Projected Receipts are shifted between the period the

edit is made and the following period.   The next periods Stk/Sls R is
recalculated and the ProjRec R for the current and following periods adjust.

3  Edits to BOP R will also shift Projected Receipts between the period the edit
is made and the prior period.  The prior periods EOP R adjusts to match the
BOP R edit, the current periods Stk/Sls R recalculates and ProjRec R for the
current and prior periods adjusts.

4  Edits to SlsR will reclaculate Projected Receipts to hold the current periods

EOP R.

5  Edits to Return to Vendor R derive new EOP R’s.  Projected Receipts do not

recalculate with an edit to Return to Vendor R.  Enter in the IMU Return to
Vendor R %.  Return to Vendor C will calculate.

6  Change Stk/Sls R to derive a new BOP R;  ProjRec R for the prior and
current periods recalc and shift to accommodate the new BOP R.

7

Input Transfer In R and Transfer Out R to derive a new EOP R.  Projected
Receipts do not reclaculate with edits to Transfers.  Enter in the IMU
Transfer In R % and  IMU Transfer Out R %.  Transfer In C and  Transfer
Out C will calculate.

8  Review the Ttl Available CMU%.

9  Review the AvgInv R, TO, Stk/Sls and WOS.

70    TopPlan

Measures

The Inventory  worksheet contains the following measures. For descriptions of
these measures, see “TopPlan Financial planning measures (Pre-Season and In-
Season)”on page 99.

Calculated
Wp AvgInv R
Referenced
Ly AvgInv R
Calculated
Wp AvgInv varLy %
Referenced
CP (SCp) AvgInv R
Calculated
Wp BOP R
Referenced
Cp (SCp) BOP R
Referenced
Ly BOP R
Entered or calculated
Wp EOP R
Referenced
Cp (SCp) EOP R
Referenced
Ly EOP R
Referenced
Wp IMU %
Referenced
Cp (SCp) IMU %
Referenced
Ly IMU %
Wp Ttl Available CMU %
Referenced
Cp (SCp) Ttl Available CMU %  Referenced
Referenced
Ly Ttl Available CMU %
Entered
Wp IMU % RTV
Entered or calculated
Wp ProjRec R
Referenced
Cp (SCp) Proj Rec R
Referenced
Wp Received
Referenced
Cp (SCp) Received
Referenced
Ly Received
Wp Return to Vendor R
Entered or calculated
Cp (SCp) Return to Vendor R  Referenced
Referenced
Ly Return to Vendor R
Entered
Wp Transfer In R
Referenced
Cp (SCp) Transfer In R
Referenced
Ly Transfer In R
Entered
Wp Transfer Out
Referenced
Cp (SCp) Transfer Out R
Referenced
Ly Transfer Out R
Entered or calculated
Wp Sls R
Entered or calculated
Wp Stk/Sls
Referenced
Cp (SCp) Stk/Sls
Referenced
Ly Stk/Sls
Calculated
Wp TO
Referenced
Cp (SCp) TO

 Chapter 3 – Workbook descriptions   71

Ly TO
Wp TtlRec R
Cp (SCp) TtlRec R
Ly TtlRec R
Wp WOS
Cp (SCp) WOS
Ly WOS

Referenced
Calculated
Referenced
Referenced
Calculated
Referenced
Referenced

72    TopPlan

Gross Margin worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 6: Gross Margin

Usage in process

Review Gross Margin in the In-season Planning process

Process for using this worksheet

This worksheet is used to review and adjust gross margin figures.

1  Enter/adjust IMU ProjRec %, IMU On Order Cxl %, and IMU Commitmnts

% to calculate IMU %, CMU %, and GM.

2  As desired, adjust Sls R,  Markdown R %, Empl Disc R %, Shrink R % or

EOP R.

3  Review GM, GM%, Ttl Available CMU % and GMROI.

Measures

The Gross Margin worksheet contains the following measures. For descriptions
of these measures, see “TopPlan Financial planning measures (Pre-Season and
In-Season)”on page 99.

Wp Ttl Available CMU %

Calculated

Cp (SCp) Ttl Available CMU %  Referenced

Ly Ttl Available CMU %

Referenced

Wp EOP R

Cp (SCp) EOP R

Ly EOP R

Wp GM %

Cp (SCp) GM %

Ly GM %

Wp GM R

Cp (SCp) GM R

Ly GM R

Wp GMROI

Cp (SCp) GMROI

Ly GMROI

Wp IMU %

Cp (SCp) IMU %

Entered or Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

 Chapter 3 – Workbook descriptions   73

Ly IMU %

Wp Sls R

Cp (SCp) Sls R

Ly Sls R

Wp Mkd %

Cp (SCp) Mkd %

Ly Mkd %

Wp Shrink %

Cp (SCp) Shrink %

Ly Shrink %

Referenced

Entered or Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Entered or Calculated

Referenced

Referenced

Wp Empl Disc %

Entered or Calculated

Cp (SCp) Empl Disc %

Referenced

Ly Empl Disc %

Wp TtlRec R

Cp (SCp) TtlRec R

Ly TtlRec R

Referenced

Calculated

Referenced

Referenced

74    TopPlan

Summary Values worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 7: Summary Values

Usage in process

To view the Value Plan Summary in the In-Season Planning process

Process for using this worksheet

This worksheet is used to review and edit plan values.

1  Review plan values with the ability to adjust numbers if needed.

2  Compare plan variances to Current Plan (Cp/SCp) and LY.

Measures

The Summary Values worksheet contains the following measures. For
descriptions of these measures, see “TopPlan Financial planning measures (Pre-
Season and In-Season)”on page 99.

Wp AvgInv R

Ly AvgInv R

Cp (SCp) AvgInv R

Wp BOP R

Cp (SCp) BOP R

Ly BOP R

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Wp Ttl Available CMU %

Calculated

Cp (SCp) Ttl Available  CMU %  Referenced

Ly Ttl Available CMU %

Referenced

Wp EOP R

Cp (SCp) EOP R

Ly EOP R

Wp GM %

Cp (SCp) GM %

Ly GM %

Wp GM R

Cp (SCp) GM R

Ly GM R

Wp GMROI

Cp (SCp) GMROI

Entered or Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

 Chapter 3 – Workbook descriptions   75

Ly GMROI

Wp IMU %

Cp (SCp) IMU %

Ly IMU %

Wp Mkd %

Cp (SCp) Mkd %

Ly Mkd %

Wp Mkd R

Cp (SCp) Mkd R

Ly Mkd R

Wp Mkd varLy R%

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Wp Empl Disc R %

Entered or Calculated

Cp (SCp) Empl Disc R %

Referenced

Ly Empl Disc R %

Referenced

Wp Sls R

Cp (SCp) Sls R

Ly Sls R

Entered or Calculated

Referenced

Referenced

Wp Sls varCp (SCp) R%

Entered or Calculated

Wp Sls varLy R%

Entered or Calculated

Wp Stk/Sls

Cp (SCp) Stk/Sls

Ly Stk/Sls

Wp TO

Cp (SCp) TO

Ly TO

Wp TtlRec R

Cp (SCp) TtlRec R

Ly TtlRec R

Entered or Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

76    TopPlan

Units and AUR worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 8: Units and AUR

Usage in process

Convert the value plan to a unit plan in the In-Season Planning process

Process for using this worksheet

1

2

Input Sls AUR, Shrink AUR, ProjRec AUR, Returns to Vendor AUR,
Transfer In AUR, Transfer Out AUR, Reclass In AUR and Reclass Out AUR
to derive Sls U, Shrink U, ProjRec U, Return to Vendor U, Transfer In U,
Transfer Out U, Reclass In U and Reclass Out U.  This calculation derives
EOP U and EOP AUR.

Input Sls U, ProjRec U, Return to Vendor U, Transfer In U, Transfer Out U,
Reclass In U or Reclass Out U to derive SlsAUR,  ProjRecAUR, Return to
Vendor AUR, Transfer In AUR, Transfer Out AUR, Reclass In AUR and
Reclass Out AUR.  This calculation derives EOP U and EOP AUR.

(cid:131)  Optionally, input Cust Returns AUR to derive Cust Returns U or input

Cust Returns U to derive Cust Returns AUR.

3  Planners can also enter Reg Sls AUR, Promo Sls AUR and Clr Sls AUR to

derive Reg Sls U, Promo Sls U, Clr Sls U, Sls U and Sls AUR.

4  Review AvgInv U, TO U, Stk/Sls U, SellThru U and WOS U.

Measures

The Units and AUR worksheet contains the following measures. For descriptions
of these measures, see “TopPlan Financial planning measures (Pre-Season and
In-Season)”on page 99.

Wp AvgInv U

Cp (SCp) AvgInv U

Ly AvgInv U

Wp BOP U

Cp (SCp) BOP U

Ly BOP U

Wp BOP R

Cp (SCp) BOP R

Ly BOP R

Wp Cust Reteurns R

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Wp Cust Returns AUR

Entered or Calculated

Wp Cust Returns U

Entered or Calculated

 Chapter 3 – Workbook descriptions   77

Cp (SCp) Cust Returns U

Referenced

Ly Cust Returns U

Referenced

Wp Commitmnts AUR

Entered or calculated

Wp Commitmnts U

Entered or calculated

Wp Commitmnts R

Entered

Cp (SCp) Commitmnts U

Referenced

Wp EOP U

Cp (SCp)EOP U

Ly EOP U

Wp EOP R

Cp (SCp) EOP R

Ly EOP R

Wp On Order AUR

Wp On Order U

Wp On Order R

Calculated

Referenced

Referenced

Entered or calculated

Referenced

Referenced

Fed

Fed

Fed

Wp On Order Cxl AUR

Entered or calculated

Wp On Order Cxl U

Entered or calculated

Wp On Order Cxl R

Entered or calculated

Cp (SCp) On Order Cxl U

Referenced

Cp (SCp) On Order U

Referenced

Wp ProjRec AUR

Entered or calculated

Wp ProjRec U

Wp ProjRec R

Entered or Calculated

Entered or Calculated

Cp (SCp) ProjRec U

Referenced

Wp Recvd AUR

Wp Recvd U

Wp Recvd R

Fed

Fed

Fed

Cp (SCp) Recvd U

Referenced

Wp Return to Vendor R

Entered or calculated

Wp Return to Vendor AUR

Entered or calculated

Wp Return to Vendor U

Entered or calculated

Cp (SCp) Return to Vendor U  Referenced

Ly Return to Vendor U

Referenced

Wp Reclass In U

Entered or calculated

Wp Reclass Out U

Entered or calculated

78    TopPlan

Cp (SCp) Reclass In U

Referenced

Cp (SCp) Reclass Out U

Referenced

Ly Reclass In U

Ly Reclass Out U

Wp SellThru U %

Referenced

Referenced

Calculated

Cp (SCp) Sell Thru U %

Referenced

Wp Shrink U

Entered or calculated

Wp Shrink AUR

Entered or calculated

Cp (SCp) Shrink U

Ly Shrink U

Wp Sls AUR

Cp (SCp) Sls AUR

Ly Sls AUR

Referenced

Referenced

Entered or calculated

Referenced

Referenced

Wp Sls contProd U %

Entered or calculated

Ly Sls contProd U %

Referenced

Wp Sls contTime U %

Entered or calculated

Ly Sls contTime U %

Referenced

Wp Sls U

Cp (SCp) Sls U

Ly Sls U

Wp Sls R

CP (SCp) Sls R

Ly Sls R

Wp Stk/Sls U

Cp (SCp) Stk/Sls U

Wp TO U

Cp (SCp) TO U

Ly TO U

Entered or calculated

Referenced

Referenced

Entered or Calculated

Referenced

Referenced

Referenced

Referenced

Calculated

Referenced

Referenced

Wp Transfer In U

Enter or Calculated

Cp (SCp) Transfer In U

Referenced

Ly Transfer In U

Referenced

Wp Transfer Out U

Enter or Calculated

Cp (SCp) Transfer Out U

Referenced

Ly Transfer Out U

Wp TtlRec AUR

Referenced

Calculated

 Chapter 3 – Workbook descriptions   79

Cp (SCp) TtlRec AUR

Referenced

Ly TtlRec AUR

Wp TtlRec U

Cp (SCp) TtlRec U

Ly TtlRec U

Wp Ttl Rec R

CP (SCp) Ttl Rec R

Ly TtlRec R

Wp WOS U

Cp (SCp) WOS U

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Referenced

Refernced

80    TopPlan

Summary Units worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 9: Summary Units

Usage in process

To view the Unit Plan Summary in the In-Season Planning process

Process for using this worksheet

Review plan units and adjust numbers as needed.

Measures

The Plan Summary – Units worksheet contains the following measures. For
descriptions of these measures, see “TopPlan Financial planning measures (Pre-
Season and In-Season)”on page 99.

Wp AvgInv U

Cp (SCp) AvgInv U

Ly AvgInv U

Wp BOP U

Cp (SCp) BOP U

Ly BOP U

Wp EOP AUR

Cp (SCp) EOP AUR

Ly EOP AUR

Wp EOP U

Cp (SCp) EOP U

Ly EOP U

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

Wp EOP varCp (SCp) U %

Calculated

Wp EOP varLy U %

Calculated

Wp Return to Vendor U

Entered or Calculated

Cp (SCp) Return to Vendor U  Referenced

Ly Return to Vendor U

Referenced

Wp Transfer In U

Entered or Calculated

Cp (SCp) Transfer In U

Referenced

Ly Transfer In U

Referenced

Wp Transfer Out U

Entered or Calculated

Cp (SCp) Transfer Out U

Referenced

 Chapter 3 – Workbook descriptions   81

Ly Transfer Out U

Wp SellThru U %

Referenced

Calculated

Cp (SCp) SellThru U %

Referenced

Ly SellThru U  %

Wp Sls AUR

Cp (SCp) Sls AUR

Ly Sls AUR

Wp Sls AUR varLy %

Wp Sls U

Cp (SCp) Sls U

Ly Sls U

Referenced

Entered

Referenced

Referenced

Calculated

Entered or calculated

Referenced

Referenced

Wp Sls varCP (SCp) U %

Calculated

Wp Sls varLy U %

Calculated

Wp Stk/Sls U

Entered or Calculated

Cp (SCp) Stk/Sls U

Ly Stk/Sls U

Wp TO U

Cp (SCp) TO U

Ly TO U

Wp TtlRec AUR

Referenced

Referenced

Calculated

Referenced

Referenced

Calculated

Cp (SCp) TtlRec AUR

Referenced

Ly TtlRec AUR

Wp TtlRec U

Cp (SCp) TtlRec U

Ly TtlRec U

Wp WOS U

Cp (SCp) WOS U

Ly WOS U

Referenced

Calculated

Referenced

Referenced

Calculated

Referenced

Referenced

82    TopPlan

Reconcile worksheet

Workbook

In-Season Financial Plan workbook

Worksheet 10: Reconcile

Usage in process

To compare plan to Targets, Current Plan, LY and/or Summary plan versions in
the In-Season Planning process

Process for using this worksheet

The Reconcile worksheet is used for reconciling plan values to Target, Current
Plan, LY and Summary values. This worksheet is used  by Planners reconciling
to Managers Targets and by Managers reconciling Planners’ data in a Summary
version and/ or Strategic Targets set by Executives.

1  Adjust Sls R or Sls varTgt R %  as needed.

2  Adjust Markdowns R % as needed. The system calculates Markdowns R.

3  Adjust ProjRec R as needed. This calculates EOP R, AvgInv R, and TO.

4  Adjust IMU ProjRec % as needed. The system calculates GM R and GM R

%.

For more information about plan reconciliation and approval, see page 11.

Measures

The Reconcile worksheet contains the following measures. For descriptions of
these measures, see “TopPlan Financial planning measures (Pre-Season and In-
Season)”on page 99.

Wp AvgInv R

SWa AvgInv R

Cp (SCp) AvgInv R

Calculated

Referenced

Referenced

Wp AvgInv varSWa R   %

Calculated

Wp AvgInv varCp (SCp) R %  Calculated

Wp BOP R

Tgt BOP R

Cp BOP R

SWa BOP R

Wp EOP R

SWa EOP R

Cp (SCp) EOP R

Tgt EOP R

Entered or Calculated

Referenced

Referenced

Referenced

Entered or calculated

Referenced

Referenced

Referenced

 Chapter 3 – Workbook descriptions   83

Wp EOP varSWa R %

Calculated

Wp EOP varCp (SCp) R %

Calculated

Wp EOP varTgt R %

Wp GM %

Wp GM R

SWa GM R

SWa GM %

Cp (SCp) GM %

Cp (SCp) GM R

Tgt GM %

Tgt GM R

Wp GM varSWa R %

Calculated

Calculated

Calculated

Referenced

Referenced

Referenced

Referenced

Referenced

Referenced

Calculated

Wp GM varCp (SCp) R %

Calculated

Wp GM varTgt R %

Wp IMU %

Cp (SCp) IMU %

SWa IMU %

Tgt IMU %

Calculated

Calculated

Referenced

Referenced

Referenced

Wp Markdowns R %

Entered or Calculated

SWa Markdowns R %

Referenced

Cp (SCp) Markdowns R %

Referenced

Tgt Markdowns R%

Referenced

Wp Markdown R

Entered or Calculated

SWa Markdowns R

Referenced

Cp (SCp) Markkdowns R

Referenced

Tgt Markdowns R

Wp Mkd varSWa R %

Refernced

Calculated

Wp Mkd varCp (SCp) R %

Calculated

Wp Mkd varTgt R %

Calculated

Wp Sls R

SWa Sls R

Cp (SCp) Sls R

Tgt Sls R

Entered or calculated

Referenced

Referenced

Referenced

Wp Sls varSWa R %

Entered or calculated

Wp Sls R varCp (SCp) %

Calculated

84    TopPlan

Wp Sls R varTgt %

Entered or calculated

Wp TO

SWa TO

Cp (SCp) TO

Tgt TO

Wp TtlRec R

SWa TtlRec R

Cp (SCp) TtlRec R

Tgt  TtlRec R

Calculated

Referenced

Referenced

Referenced

Calculated

Referenced

Referenced

Referenced

Wp TtlRec var Cp (SCp) R%  Calculated

 Chapter 3 – Workbook descriptions   85

OTB worksheets

Workbook

In-Season Financial Plan workbook

Worksheet 11 and 12: Value OTB and Unit OTB

Usage in process

To review the available Value and Unit Open to Buy in the In-season Planning
process

Process for using this worksheet

On the OTB worksheets, Total Planned Receipts are compared with On Order,
On Order Cancellations and Commitments resulting in the available amount that
is “open to buy”.   From this worksheet, you can determine further actions, such
as whether to buy additional goods, shift future on order or to cancel on order.

1  Review OTB projection. As needed, perform the following optional steps:

2  Adjust Commitmnts R or U and On Order Cxl R or U.

3  Adjust ProjRec R or U.

Measures

The OTB worksheet contains the following measures. For descriptions of these
measures, see “TopPlan Financial planning measures (Pre-Season and In-
Season)”on page 99.

Wp BOP U

Wp BOP R

Wp Commitmnts U

Wp Commitmnts R

Wp EOP U

Cp (SCp) EOP U

Wp EOP R

Calculated

Calculated

Calculated

Entered

Calculated

Referenced

Entered or Calculated

Cp (SCp) EOP R

Referenced

Wp Mkd %

Wp Mkd R

Entered or Calculated

Entered or Calculated

Wp Empl Disc R

Wp Empl Disc R %

Calculated

Entered

Wp On Order Cxl U

Entered or calculated

Wp On Order Cxl R

Entered

Wp On Order U

Wp On Order R

Fed

Fed

86    TopPlan

Wp OTB U

Wp OTB R

Wp ProjRec U

Wp ProjRec R

Wp Recvd U

Wp Recvd R

Wp RetVen R

Wp RetVen U

Wp Sls U

Wp Sls R

Wp Shrink R

Wp Shrink %

Wp Shrink U

Wp TtlRec U

Wp TtlRec R

Calculated

Calculated

Entered or calculated

Entered or calculated

Fed

Fed

Entered

Entered

Entered or calculated

Entered or calculated

Calculated

Entered or Calculated

Calculated

Calculated

Calculated

Plan Approval worksheet

The Plan Approval worksheet is used to submit plans for approval, to approve
submitted plans, and view status of submitted plans.

This worksheet is used for approving both pre-season and in-season financial
plans. For a description of this worksheet, see page 55.

 Chapter 3 – Workbook descriptions   87

Retek ChannelPlan workbooks

Channel Planning workbook

Channel planning is a pre-season process for planning Sales Value and Average
Inventory by individual stores or channels.  Sales Values can be planned by using
comparable and non-comparable store data in addition to planning percent
variances to historical data (Ly), product plan data and the projected demand
forecast (Fcst).  Average Inventory is derived through the input of a turnover
measure, with displayed data for Sales per Square Feet.  You can reconcile the
aggregated level of Total Chain with the aggregated level of Total Company
from the product.

The Channel Planning workbook contains the following worksheets:

•  Sales worksheet

•  Density worksheet

•  Comp / Non-Comp Review worksheet

•  Reconcile worksheet

Process for using this workbook

1  Plan sales using the Sales worksheet.

2  Plan density using the Plan Density worksheet. On this worksheet, you

review sales, square footage, average inventory, and turn over.3
comparable and non-comparable store sales data on the Comp / Non-Comp
Review worksheet.

Review

3  Reconcile the channel plan with the product plan, using the Reconcile

worksheet.

88    TopPlan

Plan Sales worksheet

Workbook

Channel Planning workbook

Worksheet 1: Sales

Usage in process

Pre-season Planning, Plan Sales by individual stores and/or channels

Process for using this worksheet

1

2

Input Sls R. This can be done by store or at any aggregate of the location or
calendar hierarchy.

Inputs to SlsR var to Fcst, var to MP (Merchandise Plan), contChain,
contTime, and/ or var to Ly to derive Sls R.

Measures

The Sales worksheet contains the following measures. For descriptions of these
measures, see page 138.

Wp Sls contChain R

Entered or Calculated

Fcst Sls contChain R

Ly Sls R contChain

Referenced

Referenced

Wp Sls contTime R

Entered or Calculated

Fcst Sls contTime R

Ly Sls contTime R

Calculated

Calculated

Wp Sls R

Fcst Sls R

Ly Sls R

Mp Sls R

Wp Sls varFcst R

Wp Sls varLy R

Wp Sls varMp R

Entered or calculated

Calculated

Calculated

Calculated

Calculated

Calculated

Calculated

 Chapter 3 – Workbook descriptions   89

Plan Density worksheet

Workbook

Channel Planning workbook

Worksheet 2: Density

Usage in process

Pre-season Planning, Review sales and sales by square footage and average
inventory by individual store or channels.

Process for using this worksheet

1  Manipulate TO as needed to derive AvgInv R.

2  Review Sls/Sq Ft, make adjustments to Sls R as needed.

Measures

The Density worksheet contains the following measures. For descriptions of
these measures, see page 138.

Wp AvgInv R

Ly AvgInv R

Wp Avg Sq Ft

Wp Sls R

Wp Sls/Sq Ft

Ly Sls/Sq Ft

Wp Sq Ft

Wp TO

Ly TO

Calculated

Referenced

Calculated

Entered or calculated

Calculated

Referenced

Referenced

Entered or calculated

Referenced

90    TopPlan

Comp / Non-Comp Review worksheet

Workbook

Channel Planning workbook

Worksheet 3: Comp / Non-Comp Review

Usage in process

Pre-season Planning, Review comparable vs. non-comperable stores sales and
variations to LY

Process for using this worksheet

This worksheet is used to review the sales among stores. It presents cumulative
sales values, as well as sales in similar stores that have been open for some time
(Comp) and sales in new or closed stores (Non Comp).

Review Comp and NonComp data; input Sls R or Sls varLy R.

Measures

The Comp / Non-Comp Review worksheet contains the following measures. For
descriptions of these measures, see page 138.

Wp # of Stores

Wp # of Stores Comp

# of Stores NonComp

Wp Sls Comp R

Ly Sls Comp R

Referenced

Referenced

Referenced

Calculated

Referenced

Wp Sls Comp varLy R

Calculated

Wp Sls NonComp R

Calculated

Wp Sls R

Wp Ly Sls R

Entered or calculated

Referenced

Wp Sls varLy R

Entered or calculated

 Chapter 3 – Workbook descriptions   91

Reconcile worksheet

Workbook

Channel Planning workbook

Worksheet 4: Reconcile

Usage in process

Pre-season Planning, Reconcile the Location Sales plan with the Product Plan

Process for using this worksheet

1

Input Sls R or Sls varMP (Merchandise Plan) R to smooth sales. This input
can be entered at all levels of the location or time horizon.

2

Input TO to derive AvgInv R, keeping in line with MP (Merchandise Plan).

Measures

The Reconcile worksheet contains the following measures. For descriptions of
these measures, see page 138.

Wp AvgInv R

AvgInv R

Mp AvgInv varMp

Wp Sls R

Mp Sls R

Calculated

Referenced

Calculated

Entered or calculated

Referenced

Wp Sls varMp R

Entered or calculated

Wp TO

Mp TO

Wp TO varMp

Entered or Calculated

Referenced

Calculated

 Chapter 4 – Measure descriptions   93

Chapter 4 – Measure descriptions

This chapter provides more details on the rules and measures used in the Retek
Predictive Solutions.

Metrics and Measures

A metric is any item of data that can be represented on a grid in worksheets, such
as Sales, Markdowns or Receipts.

A measure is the combination of a metric with a Role, Plan Version and a Unit of
Measure.  Pl Wp Sls R is a measure =  Planners Working Plan Sales Retail.

A standard set of measures (also known as business measures) have been defined
within the application that enable the planning of Company to Sub-Class for both
Pre-Season and In-Season planning.  If business requirements call for additional
measures, they are definable by a System Administrator.

Business Rules

To support the business process, measures are combined into mathematical
equations creating business rules and giving the plan functionality.  Some
measures are changeable, others simply a result of manipulations made to
dependent metrics.  Inherent flexibility in the planning process enables the
planning of multiple measures to achieve a result.  An example is the planning of
End of Period (EOP) Inventory.  Projected Receipts can be calculated to derive
EOP or they can be input to derive EOP.  Beginning of Period (BOP) Inventory
can be derived from the resulting prior periods EOP, input directly, or a
Stock/Sales ratio can be input to derive BOP.  Note that in the latter case, receipts
for the previous period would be re-calculated.

Business rules, which support an industry standard business process, are built
into TopPlan. If business requirements call for additional rules, they are definable
by a System Administrator.

94    TopPlan

TopPlan measures

TopPlan Strategic Target planning measures

The Strategic Target Plan involves the following measures:

AvgInv R

•  Plan version: Wp, Ly, SCp, SOp

•  Planning role: Executive

•  Description: Average inventory value.

•  Calculation: Sales R / Turnover

AvgInv varLy R %

•  Plan version: Wp

•  Planning role: Executive

•  Description: Percentage increase or decrease in average inventory this year

over last year.

•  Calculation: ((Wp Avg Inv R - Ly Avg Inv R)/Ly Avg Inv R)

AppBy

•  Plan version:  Ra

•  Planning role:  Executive

•  Description:  Visibility to the Manager that approved or rejected the last

submitted plan

•  Calculation: None

AppCom

•  Plan version:  Ra

•  Planning role:  Executive

•  Description:  Visibility to the Comments that a Manager made while

approving or rejecting the last plan submitted for approval

•  Calculation: None

AppRej

•  Plan version:  Ra

•  Planning role:  Executive

•  Description:  Visibility to see if the last plan submitted for approval was

Approved or Rejected by the Manager

•  Calculation: None

 Chapter 4 – Measure descriptions   95

BOP R

•  Plan version:  SOp, SCp

•  Planning role:  Executive

•  Description:  Beginning of Period Inventory

•  Calculation: None (for this role)

CMU %

•  Plan version:  Wp, Ly, SCp, SOp, SWa

•  Planning role:  Executive

•  Description:  Cumulative Markup Percentage

•  Calculation: None (for this role)

CurVsn

•  Plan version:  Ra

•  Planning role:  Executive

•  Description:  Visibility to see the current version of the Planners Plan

•  Calculation: None

CurVsnDte

•  Plan version:  Ra

•  Planning role:  Executive

•  Description:  Visibility to the date the last plan was submitted for approval

by the Planner

•  Calculation: None

EOP R

•  Plan version:  SOp, SCp

•  Planning role:  Executive

•  Description:  End of Period Inventory

•  Calculation: None (for this role)

GM %

•  Plan version: Wp, Ly, SCp, SOp, SWa

•  Planning role: Executive

•  Description: Gross Margin  expressed as a percentage of Sales.

•  Calculation: (Gross Margin R / Sales R)

96    TopPlan

GM R

•  Plan version: Wp, Ly, SCp, SOp, SWa

•  Planning role: Executive

•  Description: Gross Margin value.

•  Calculation: Gross Margin % * Sales R

GMROI

•  Plan version: Wp, Ly, SCp, SOp

•  Planning role: Executive

•  Description: Gross Margin  Return on Investment.

•  Calculation: (Gross Margin R / Average Inventory C)

GM varLy R %

•  Plan version: Wp

•  Planning role: Executive

•  Description: Percentage increase or decrease in Gross Margin this year over

last year.

•  Calculation: ((Wp Gross Margin R - Ly Gross Margin R)/Ly Gross Margin

R)

GM varSCp R %

•  Plan version: Wp

•  Planning role: Executive

•  Description: Percentage increase or decrease in Gross Margin over Current

Plan.

•  Calculation: ((Wp Gross Margin R - SCp Gross Margin R)/SCp Gross

Margin R)

Mkd %

•  Plan version: Wp, Ly, SCp, SOp, SWa

•  Planning role: Executive

•  Description: Total Markdowns expressed as a percentage of Sales.

•  Calculation: (Markdown R / Sales R)

Mkd R

•  Plan version: Wp, Ly, SCp, SOp

•  Planning role: Executive

•  Description: Total Markdown value.

•  Calculation: (Markdown % * Sales R)

 Chapter 4 – Measure descriptions   97

Mkd varLy R %

•  Plan version: Wp

•  Planning role: Executive

•  Description: Percentage increase or decrease in Markdown this year over last

year.

•  Calculation: ((Wp Markdown R - Ly Markdown R)/Ly Markdown R)

Mkd varSCp R %

•  Plan version: Wp

•  Planning role: Executive

•  Description: Percentage increase or decrease in Markdown over Current

plan.

•  Calculation: ((Wp Markdown R – SCp Markdown R )/SCp Markdown R)

Sls R

•  Plan version: Wp, Ly, Fcst, SCp, SOp, SWa

•  Planning role: Executive

•  Description: Sales value.

•  Calculation: None

Sls build rate R %

•  Plan version: Wp, Ly, Fcst, SCp, SOp

•  Planning role: Executive

•  Description: Ratio of Sales for this period to sales for prior displayed period.

•  Calculation: (Sales R @ Curr Month / Sales R Last Month)  or (Sales R @

Curr Qtr / Sales R Last Qtr)

Sls contProd R %

•  Plan version: Wp, Ly, Fcst

•  Planning role: Executive

•  Description: The contribution that a Sales value at a specific product

hierarchy level makes to the total Sales value at the highest product level.

•  Calculation: (Sales R @ specific Product hierarchy Ievel / Sales R @ Highest

Product Parent level)

98    TopPlan

Sls contTime R %

•  Plan version: Wp, Ly, Fcst

•  Planning role: Executive

•  Description: The contribution that a Sales value at a specific calendar

hierarchy level makes to the total sales value at the highest calendar level.

•  Calculation: (Sales R @ specific calendar hierarchy level / Sales R @ highest

calendar level)

Sls varFcst R %

•  Plan version: Wp, SCp, SOp

•  Planning role: Executive

•  Description: Percentage increase or decrease in Sales over the Forecast Sales.

•  Calculation: ((Wp Sales R - Fcst Sales R)/Fcst Sales R)

Sls varLy R %

•  Plan version: Wp

•  Planning role: Executive

•  Description: Percentage increase or decrease in Sales this year over last year.

•  Calculation: ((Wp Sales R - Ly Sales R)/Ly Sales R)

Sls varSWa R %

•  Plan version: Wp

•  Planning role: Executive

•  Description: Percentage increase or decrease in sales over the Planners

Submitted Waiting for Approval Sales.

•  Calculation: ((Wp Sales R - SWa Sales R)/SWa Sales R)

SubBy

•  Plan version: Ra

•  Planning role: Executive

•  Description: Visibility to the Planner that submitted the plan waiting for

approval.

•  Calculation: None

TO

•  Plan version: Wp, Ly, SCp, SOp

•  Planning role: Executive

•  Description: Turnover based on values, or frequency with which inventory

value is sold and replaced over a stated time period.

•  Calculation: Sales R / Avg Inv R

 Chapter 4 – Measure descriptions   99

TopPlan Financial planning measures (Pre-Season and In-
Season)

AvgInv U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa

•  Planning role: Manager, Planner

•  Description: Average inventory units.

•  Calculation: (BOP U + cumulative EOP U) / (# periods + 1)

AvgInv R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt , Wa, SWa

•  Planning role: Manager, Planner

•  Description: Average Inventory value.

•  Calculation: (BOP R + cumulative EOP R) / (# periods + 1)

AvgInv varLy R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Average Inventory value this

year over last year.

•  Calculation: ((Avg Inv R - Ly Avg Inv R)/Ly Avg Inv R)

AvgInv varCp(SCp) R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Average Inventory value

over the current approved plan.

•  Calculation: ((Wp Avg Inv R – Cp (SCp) Avg Inv R)/Cp (SCp) Avg Inv R )

AvgInv varSWa R %

•  Plan version: Wp

•  Planning role: Manager

•  Description: Percentage increase or decrease in Average Inventory value

over the submitted waiting for approval plan.

•  Calculation: ((Wp Avg Inv R – SWa Avg Inv R)/SWa Avg Inv R )

100    TopPlan

AvgInv varTgt R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Average Inventory value

over superior’s plan. Target

•  Calculation: ((Wp Avg Inv R- Tgt Avg Inv R)/Tgt Avg Inv R)

AppBy

•  Plan version:  Ad, Ra

•  Planning role:  Manager, Planner

•  Description:  Visibility to the Manager that approved or rejected the last

submitted plan

•  Calculation: None

AppCom

•  Plan version:  Ad, Ra

•  Planning role:  Manager, Planner

•  Description:  Visibility to the Comments that a Manager made while

approving or rejecting the last plan submitted for approval

•  Calculation: Entered

AppRej

•  Plan version:  Ad, Ra

•  Planning role:  Manager, Planner

•  Description:  Visibility to see if the last plan submitted for approval was

Approved or Rejected by the Manager

•  Calculation: None

Avg Store Inv R

•  Plan version: Wp, Ly, Cp, SCp,Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: The amount of End of Period Inventory in the average store

expressed as a Value.

•  Calculation: (EOP R / Store Count #)

 Chapter 4 – Measure descriptions   101

Avg Store Inv U

•  Plan version: Wp, Ly, Cp, SCp,Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: The amount of End of Period Inventory in the average store

expressed as Units.

•  Calculation: (EOP U / Store Count #)

Avg Store Sls R

•  Plan version: Wp, Ly, Cp, SCp,Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: The amount of Sales in the average store expressed as a Value.

•  Calculation: (Sales R / Store Count #)

Avg Store Inv U

•  Plan version: Wp, Ly, Cp, SCp,Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: The amount of Sales in the average store expressed as Units.

•  Calculation: (Sales U / Store Count #)

BOP AUR

•  Plan version: Wp, Ly, Cp, Kp

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of the Beginning of Period Inventory.

•  Calculation: (BOP R / BOP U)

BOP C

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Beginning of Period Inventory cost.

•  Calculation: (BOP V * (1 – CMU%))

BOP U

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa, Kp

•  Planning role: Manager, Planner

•  Description: Beginning of Period Inventory units.

•  Calculation: (BOP R / BOP AUR)

102    TopPlan

BOP R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa, Kp

•  Planning role: Manager, Planner

•  Description: Beginning of Period Inventory value.

•  Calculation: (EOP R – TtlRec R – Markups R - Transfer In  - Reclass In R +
Sls R + Markdown R + Shrink R + Employee Discount R + Transfer Out R +
Reclass Out R + Return to Vendor R)

BOP Contr R %

•  Plan version: Kp

•  Planning role: Manager, Planner

•  Description: KeyPlan BOP Inventory Value expressed as a contribution to

TopPlan Wp BOP Inventory Value.

•  Calculation: (Kp BOP R / Wp BOP R)

BOP var SCp R %

•  Plan version: Wp

•  Planning role: Manager

•  Description: Percentage increase or decrease in Wp Beginning of Period
Inventory value over Current Plan Beginning of Period Inventory value.

•  Calculation: ((Wp BOP R - SCpBOP R))/SCp BOP R))

BOP var Ly R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Beginning of Period

Inventory value over last year.

•  Calculation: ((BOP R - Ly BOP R)/Ly BOP R)

BOPI C

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Used to initialize the very first Beginning of Period Inventory

Cost.

•  Calculation: Entered or (BOPI R * (1 – IMU BOPI R %))

 Chapter 4 – Measure descriptions   103

BOPI U

•  Plan version:  Wp

•  Planning role:  Manager, Planner

•  Description:  Used to initialize the very first Beginning of Period Inventory

Units.

•  Calculation:  Entered

BOPI R

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Used to initialize the very first Beginning of Period Inventory

Value.

•  Calculation: Entered

Cash Discount C

•  Plan version: Wp, Ly, Op, Sop, Cp, SCp, Tgt, SWa, Wa

•  Planning role: Manager, Planner

•  Description: Earned Cash Discounts.

•  Calculation: Entered

Cash Discount C %

•  Plan version: Wp, Ly, Op, Sop, Cp, SCp, Tgt, SWa, Wa

•  Planning role: Manager, Planner

•  Description: Cash Discounts expressed as a percent of Total Receipts Cost.

•  Calculation: (Cash Discount C / Ttl Receipts C )

Clr Sls AUR

•  Plan version: Wp, Ly, Cp, Op, Wa

•  Planning role: Planner

•  Description: Average Unit Retail value of Clearance Sales.

•  Calculation: (Clr Sls R / Clr Sls U)

Clr Sls C

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Clearance Sales Cost.

•  Calculation: None

104    TopPlan

Clr Sls R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Clearance Sales Value.

•  Calculation: Entered or  (Clr Sls cont Ttl Sls R % * Sls R)

Clr Sls U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Planner

•  Description: Clearance Sales Units.

•  Calculation: Entered or  (Clr Sls R / Clr Sls AUR)

Clr Sls cont Ttl Sls R %

•  Plan version: Wp, Ly

•  Planning role: Planner

•  Description: Clearance Sales value contribution to Sales.

•  Calculation: (Clr Sls R / Sls R)

Clr Sls cont Ttl Sls U %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Clearance Sale Units contribution to Sales.

•  Calculation: (Clr Sls U / Sls U)

Clr Sls cont Time R %

•  Plan version: Wp, Ly

•  Planning role: Planner

•  Description: The contribution that a Clearance Sales Value at a specific
calendar hierarchy level bears to the Total Clearance Sales Value at the
highest calendar level.

•  Calculation: (Clr Sls R / ‘Year’ Clr Sls R )

Clr Sls var Ly R %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp Clearance Sales value

over Last Year.

•  Calculation: ((Wp Clr Sls R - Ly Clr Sls R)/Ly Clr Sls R)

 Chapter 4 – Measure descriptions   105

Clr Sls var Ly U %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp Clearance Sale units

over Last Year.

•  Calculation: ((Wp Clr Sls U - Ly Clr Sls U)/Ly Clr Sls U)

CMU %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, Swa, Tgt

•  Planning role: Manager, Planner

•  Description: Cumulative markup percentage. The percentage difference

between total delivered cost and total original retail value of merchandise
handled within a stated time frame, inclusive of the accumulated inventory.

•  Calculation: [(First Period (BOP R) + cumulative TtlRec R + cumulative
Markups R + cumulative Transfer In R _- cumulative Transfer Out R  +
cumulative Reclass In V  - cumulative Reclass Out V – cumulative Return to
Vendor V) - (First Period (BOP C) + cumulative TtlRec C + cumulative
Transfer In C _- cumulative Transfer Out C  +  cumulative Reclass In C –
cumulative Reclass Out C – cumulative Return to Vendor C + cumulative
Freight C + cumulative Out Freight C)]/(First Period (BOP R) + cumulative
TtlRec R + cumulative Markups R +  cumulative Transfer In R _- cumulative
Transfer Out R  + cumulative Reclass In R  - cumulative Reclass Out R –
cumulative Return to Vendor R)

COGS C

•  Plan version:  Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, Swa

•  Planning role:  Manager, Planner

•  Description:  Cost of goods sold.

•  Calculation:  ((Sls R + Mkd R + Shrink R + Empl Disc R)*(1 - CMU%))

Commitmnts AUR

•  Plan version: Wp, Ly, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Average Units Retail Value of Commitments ordered but not

approved in the purchase order system.

•  Calculation: (Commitments R / Commitments U)

106    TopPlan

Commitmnts C

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cost of Commitments ordered but not approved in the purchase

order system.

•  Calculation: (Commitments R *(1 - IMU Commitmnts R %)

Commitmnts U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Unit Commitments ordered but not approved in the purchase

order system.

•  Calculation: (Commitments R / Commitments AUR)

Commitmnts R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Value of Commitments ordered but not approved in the

purchase order system.

•  Calculation: Entered

Cost Adjustment C

•  Plan version: Wp, Ly, Op, Sop, Cp, SCp, Tgt, SWa, Wa

•  Planning role: Manager, Planner

•  Description: Cost Adjustments.

•  Calculation: Entered

Cost Adjustment C %

•  Plan version: Wp, Ly, Op, Sop, Cp, SCp, Tgt, SWa, Wa

•  Planning role: Manager, Planner

•  Description: Cost Adjustments.

•  Calculation: (Cost ASdjustment C / Ttl Receipts C )

Cost Varience C

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Cost Varience.

•  Calculation: None

 Chapter 4 – Measure descriptions   107

CurVsn

•  Plan version:  Ad, Ra

•  Planning role:  Manager, Planner

•  Description:  Current version of  the Planners Plan

•  Calculation: None

CurVsnDte

•  Plan version:  Ad, Ra

•  Planning role:  Manager, Planner

•  Description:  Date the last plan was submitted for approval by the Planner

•  Calculation: None

Cust Ret AUR

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, Swa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Customer Returns.

•  Calculation: (Cust Returns R / Cust Returns U)

Cust Ret C

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Customer Returns Cost.

•  Calculation: None

Cust Ret R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Customer Returns Value.

•  Calculation: Cust Returns R % * Sls R

Cust Ret R %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Customer Returns expressed as a percentage of Sales.

•  Calculation: Cust Returns R / Sls R

108    TopPlan

Cust Ret U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Customer Returns Units.

•  Calculation: (Cust Returns R / Cust Returns AUR)

Cust Ret U %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Customer Return units expressed as a percentage of Sales units.

•  Calculation: Cust Returns U / Sls U

Cust Ret var Ly R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of the Wp Customer Return

value over Last Year.

•  Calculation: ((Wp Cust Returns R - Ly Cust Returns R)/Ly Cust Returns R)

Cust Ret var Ly U %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of the Wp Customer Return

units over Last Year.

•  Calculation: ((Wp Cust Returns U - Ly Cust Returns U)/Ly Cust Returns U)

Empl Disc R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Employee Discount Value.

•  Calculation:   (Empl Disc R % * Sls R)

Empl Disc R %

•  Plan version: Wp, Ly, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Employee Discount Value expressed as a percentage of Sales.

•  Calculation:  (Empl Disc R / Sls R)

 Chapter 4 – Measure descriptions   109

EOP AUR

•  Plan version: Wp, Ly, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of the End of Period Inventory.

•  Calculation: EOP R / EOP U

EOP C

•  Plan version: Wp, Ly, Cp, SCp, Op,  SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: End Of Period Inventory Cost.

•  Calculation: (EOP R * (1 - CMU%))

EOP U

•  Plan version: Wp, Ly, Cp, SCp, Op,  SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: End Of Period Inventory Units.

•  Calculation: (BOPU + TtlRecU - SlsU - ShrinkU - RetVenU + Transfer In U

– Transfer Out U + RclsInU – RclsOutU)

EOP R

•  Plan version: Wp, Ly, Cp, SCp, Tgt, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: End Of Period Inventory Value.

•  Calculation: (BOP R + TtlRec R + Markup R - Sls R - Mkd R - Shrink R -
RetVen R + Transfer In R – Transfer Out R + RclsIn R - RclsOut R)

EOP var Cp (SCp) R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp End of Period Inventory

value over Current Plan.

•  Calculation: (Wp EOP R – Cp (SCp) EOP R) / (Cp(SCp) EOP R)

EOP var Ly U %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp End of Period Inventory

units over Last Year.

•  Calculation: (Wp EOP U – Ly EOP U) / (Ly EOP U)

110    TopPlan

EOP var Ly R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp End of Period Inventory

value over Last Year.

•  Calculation: (Wp EOP R - Ly EOP R)/(Ly EOP R)

EOP var SWa R %

•  Plan version: Wp

•  Planning role: Manager

•  Description: Percentage increase or decrease of Wp End of Period Inventory

value over Summary Waiting for Approval.

•  Calculation: ((Wp EOP R - SWa EOP R)/(SWa EOP R)

EOP varTgt R %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp End of Period Inventory

value over Target.

•  Calculation: ((Wp EOP R - Tgt EOP R)/Tgt EOP R)

Event Text

•  Plan version:  Wp, Ly

•  Planning role:  Manager, Planner

•  Description:  Event Comments.

•  Calculation:  None

Forward Cover R

•  Plan version:  Wp, Ly, Cp, SCp

•  Planning role:  Manager, Planner

•  Description:  Inventory coverage of forward looking Sales Values.

•  Calculation:  (BOP R / (Sum of forward period Sales R for the number of

periods that the BOP R will cover)

Forward Cover U

•  Plan version:  Wp, Ly, Cp, SCp

•  Planning role:  Manager, Planner

•  Description:  :  Inventory coverage of forward looking Sales Units.

•  Calculation:  (BOP U / (Sum of forward period Sales U for the  number of

periods that the BOP U will cover)

 Chapter 4 – Measure descriptions   111

Freight C  (Inbound Freight C)

•  Plan version:  Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role:  Manager, Planner

•  Description:  Freight Cost (Inbound).

•  Calculation:  (Ttl Rec C * Freight C % )

Freight C %  (Inbound Freight C %)

•  Plan version:  Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role:  Manager, Planner

•  Description:  Freight (Inbound) expressed as a percent of Total Receipts

Cost.

•  Calculation:  (Freight C / Ttl Rec C)

Freight var Ly C %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Freight cost over Last

Year.

•  Calculation: (Wp Freight C - Ly Freight C)/(Ly Freight C)

GM %

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Gross margin expresses as a percentage of Sales -.

•  Calculation: (Gross Margin R / Sales R)

GM R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Gross Margin Value. Difference in Sales Value and Cost of

Goods Sold.

•  Calculation: (SlsR – COGS C)

GM var CP (SCp) R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Gross Margin over

Current Plan.

•  Calculation: (Wp GM R – Cp (SCp) GM R) / (Cp (SCp) GM R)

112    TopPlan

GM var Ly R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Gross Margin over Last

Year.

•  Calculation: ((Wp GM R - Ly GM R)/Ly GM R)

GM var SWa R %

•  Plan version: Wp

•  Planning role: Manager

•  Description: Percentage increase or decrease of Wp Gross Margin over

Summary Waiting for Approval.

•  Calculation: ((Wp GM R - SWa GM R)/SWa GM R)

GM varTgt R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Gross Margin over

Target.

•  Calculation: ((Wp GM R - Tgt GM R)/Tgt GM R)

GMROI

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, SWa

•  Planning role: Manager, Planner

•  Description: Gross Margin Return on Inventory Investment.

•  Calculation: Gross Margin R / Average Inventory Cost

Ttl Sls Dmnd – Grs Sls AUR

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Gross Sales.

•  Calculation: ( Ttl Sls Dmnd – Grs Sls R / Ttl Sls Dmnd – Grs Sls U )

Ttl Sls Dmnd – Grs Sls R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Total Demand (Gross Sales) Value , the combination of Sales

and Customer Returns.

•  Calculation: ( Sls R + Cust Returns R)

 Chapter 4 – Measure descriptions   113

Ttl Sls Dmnd – Grs Sls AUR

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Gross Sales.

•  Calculation: ( Ttl Sls Dmnd – Grs Sls R / Ttl Sls Dmnd – Grs Sls U )

Ttl Sls Dmnd – Grs Sls U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Total Demand (Gross Sales) Units, the combination of Sales and

Customer Returns.

•  Calculation: ( Sls U + Cust Returns U)

Ttl Sls Dmnd – Grs Sls var LY R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Gross Sales value over

Last Year.

•  Calculation: ( Wp Ttl Sls Dmnd – Grs Sls R – Ly Ttl Sls Dmnd – Grs Sls R /

Ly Ttl Sls Dmnd – Grs Sls R )

Ttl Sls Dmnd – Grs Sls var LY U %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Gross Sales units over

Last Year.

•  Calculation: ( Wp Ttl Sls Dmnd – Grs Sls U – Ly Ttl Sls Dmnd – Grs Sls U /

Ly Ttl Sls Dmnd – Grs Sls U )

IMU BOP R%

•  Plan version: Wp, Ly, Cp, SCp, Op,  SOp, Tgt, SWa

•  Planning role: Manager, Planner

•  Description: Difference between Beginning of Period Inventory Value and

Beginning of Period Inventory Cost expressed as a percentage of  Beginning
of Period Inventory Value.

•  Calculation:  ((BOP R –  BOP C) / BOP R)

114    TopPlan

IMU BOPI R%

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Difference between the very first Beginning of Period Inventory
Value and the very first Beginning of Period Inventory Cost expressed as a
percentage of the very first Beginning of Period Inventory Value.

•  Calculation:  ((BOP R –  BOP C) / BOP R)

IMU R %

•  Plan version: Wp, Ly, Cp, SCp, Op,  SOp, Tgt, Wa

•  Planning role: Manager, Planner

•  Description: Difference between  Total Receipt Value and  Total Receipt

Cost expressed as a percentage of  Total Receipt Value.

•  Calculation:  ((Ttl Rec R – Ttl Rec C ) / Ttl Rec R)

IMU Commitmnts R %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp

•  Planning role: Manager, Planner

•  Description: Difference between Commitment Value and Commitment Cost

expressed as a percentage of Commitment Value.

•  Calculation: ((Commitments R - Commitments C) / Commitments R)

IMU On Order R %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp

•  Planning role: Manager, Planner

•  Description: Difference between On-Order Value and On-Order Cost

expressed as a percentage of On-Order Value.

•  Calculation((On Order R - On Order C)/On Order R)

IMU On Order Cxl R %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp

•  Planning role: Manager, Planner

•  Description: Difference between Cancelled On-Order Value and  Cancelled
On-Order Cost expressed as a percentage of  Cancelled On-Order Value.

•  Calculation:((On Order Cancel R - On Order Cancel C)/On Order Cancel R)

 Chapter 4 – Measure descriptions   115

IMU ProjRec R %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, SWa

•  Planning role: Manager, Planner

•  Description: Difference between Projected Receipt Value and Projected
Receipt Cost expressed as a percentage of  Projected Receipt Value.

•  Calculation: ((Projected Receipts R - Projected Receipts C)/Projected

Receipts R)

IMU Reclass In R %

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description:  Difference between  Re-class In Value and  Re-class In Cost

expressed as a percentage of  Re-class In Value.

•  Calculation:  ((RclsIn R – RclsIn C)/RclsIn R)

IMU Reclass Out R %

•  Plan version: Wp, LyPlanning role: Manager, Planner

•  Description:  Difference between  Re-class Out Value and  Re-class Out Cost

expressed as a percentage of  Re-class Out Value.

•  Calculation:  ((RclsOut R – RclsOut C)/RclsOut R)

IMU Recvd R %

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Difference between Received Value and Received Cost

expressed as a percentage of Received Value.

•  Calculation: ((Received R - Received C)/Received R)

IMU RTV R %

•  Plan version:  Wp, Ly

•  Planning role:  Manager, Planner

•  Description:  Difference between Return to Vendor Value and Return to
Vendor Cost expressed as a percentage of Return to Vendor Value.

•  Calculation:  ((Return to Vendor R – Return to Vendor C)/Return to Vendor

R)

116    TopPlan

IMU Trans In R %

•  Plan version:  Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role:  Manager, Planner

•  Description:  Difference between Transfer In Value and Transfer In Cost

expressed as a percentage of Transfer In Value.

•  Calculation:  ((Transfer In R – Transfer In  C)/ Transfer In R)

IMU Trans Out R %

•  Plan version:  Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role:  Manager, Planner

•  Description:  Difference between Transfer Out Value and Transfer Out Cost

expressed as a percentage of Transfer Out Value.

•  Calculation:  ((Transfer In R – Transfer In C)/ Transfer In R)

In Transit R

•  Plan version:  Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role:  Manager, Planner

•  Description:  In-Transit Value.

•  Calculation:  (BOP R – Selling Store On Hand R)

In Transit U

•  Plan version:  Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role:  Manager, Planner

•  Description:  In-Transit Value.

•  Calculation:  (BOP U – Selling Store On Hand U)

Inventory Adjustment C

•  Plan version:  Wp, Ly

•  Planning role:  Manager, Planner

•  Description:  Inventory Adjustment Cost.

•  Calculation:  (BOP C – Stock On Hand C)

Inventory Adjustment R

•  Plan version:  Wp, Ly

•  Planning role:  Manager, Planner

•  Description:  Inventory Adjustment Value.

•  Calculation:  (BOP R – Stock On Hand R)

 Chapter 4 – Measure descriptions   117

Inventory Adjustment U

•  Plan version:  Wp, Ly

•  Planning role:  Manager, Planner

•  Description:  Inventory Adjustment Units.

•  Calculation:  (BOP U – Stock On Hand U)

Inventory Text

•  Plan version:  Wp, Ly

•  Planning role:  Manager, Planner

•  Description:  Inventory Comments.

•  Calculation:  None.

Markdowns R %

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Total Markdowns expressed as a percentage of Sales.

•  Calculation: (Markdowns R / Sales R)

Markdowns R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa, Kp

•  Planning role: Manager, Planner

•  Description: Total Markdowns Value.

•  Calculation: (Markdown Clearance R + Markdown Perm R + Markdown

Promo R)

Mkd Clear %

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Clearance Markdowns expressed as a percentage of Sales.

•  Calculation: (Markdown Clearance R / Sales R)

Mkd Clear R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Clearance Markdown.  Price reduction used to clear aged or

slow moving inventory expressed as a Value  .

•  Calculation: (Markdown Clearance R % * Sales R)

118    TopPlan

Mkdn Contr R %

•  Plan version: Kp

•  Planning role: Manager, Planner

•  Description: KeyPlan Markdown Value expressed as a contribution to

TopPlan Wp Markdown Value.

•  Calculation:  (Kp Markdown R / Wp Markdown R)

Mkdn Cxl R

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Markdown Cancel Value.

•  Calculation: None

Mkd Perm R %

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Permanent Markdowns expressed as a percentage of Sales  .

•  Calculation: (Markdown Perm R / Sales R)

Mkd Perm R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Permanent Markdown.  Permanent value decrease to the owned
inventory price of merchandise for strategic downward re-pricing decisions  .

•  Calculation: (Markdown Perm  R % * Sales R)

Mkd Promo R %

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Promotional Markdowns expressed as a percentage of Sales.

•  Calculation: (Markdown Promo R / Sales R)

Mkd Promo R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Promotional Markdown.  Temporary reduction to the owned

inventory price for promotional purposes expressed as a value  .

•  Calculation: (Markdown Promo R % * Sales R)

 Chapter 4 – Measure descriptions   119

Mkd varCP (SCp) R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Markdown value over

Current Plan.

•  Calculation: ((Markdown R - Cp (SCp) Markdown R)/Cp (SCp)Markdown

R)

Mkd varLy R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Markdown value over

Last Year.

•  Calculation: ((Markdown R - Ly Markdown R)/Ly Markdown R)

Mkd varSWa R %

•  Plan version: Wp

•  Planning role: Manager

•  Description: Percentage increase or decrease of Wp Markdown value over

Summary Waiting for Approval  .

•  Calculation: ((Markdown R - Markdown R Submitted Waiting for

Approval)/Markdown R Submitted Waiting for Approval)

Mkd varTgt R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Markdown value over

Target  .

•  Calculation: ((Markdown R - Tgt Markdown R)/Tgt Markdown R)

Markups R

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Mark-Up Value.  Permanent value increase to the owned

inventory price of merchandise for strategic upward re-pricing decisions.

•  Calculation: None

120    TopPlan

Mkup Cxl R

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Markup Cancel Value.

•  Calculation: None

On Order AUR

•  Plan version: Wp, Ly, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of On-Order.

•  Calculation: (On Order R / On Order U)

On Order C

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: On-Order Cost  .

•  Calculation:   None

On Order R

•  Plan version: Wp, Ly, Cp, SCp, , Op, SOp, Tgt,  Wa, SWa

•  Planning role: Manager, Planner

•  Description: On-Order Value.

•  Calculation: None

On Order U

•  Plan version: Wp, Ly, Cp, SCp, , Op, SOp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: On-Order Units  .

•  Calculation:  None

On Order Cxl AUR

•  Plan version: Wp, Ly, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Cancelled On-Order  .

•  Calculation: (On Order Cancel R / On Order Cancel U)

 Chapter 4 – Measure descriptions   121

On Order Cxl C

•  Plan version: Wp, Ly, Op, ,SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cancelled On-Order Cost  .

•  Calculation: (On Order Cancel R*(1 - IMU On Order Cancelled % )

On Order Cxl R

•  Plan version: Wp, Ly, Tgt, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cancelled On-Order Value.

•  Calculation: None

On Order Cxl U

•  Plan version: Wp, Ly, Tgt, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cancelled On-Order Units.

•  Calculation:  (On Order Cxl R / On Order Cxl AUR)

OTB C

•  Plan version: Wp, Tgt, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cost of goods that may be received into stock without exceeding

Current Plan End of Period Inventory levels.

•  Calculation:  (Ttl Receipts C – On Order C- Commitments C + On Order

Cancel C)

OTB R

•  Plan version: Wp, Tgt, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Value of goods that may be received into stock without

exceeding Current Plan End of Period Inventory levels .

•  Calculation: (Ttl Receipts R – On Order R- Commitments R + On Order

Cancel R)

122    TopPlan

OTB U

•  Plan version: Wp, Tgt, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Number of Unit that may be received into stock without

exceeding Current Plan End of Period Inventory levels.

•  Calculation:  (Ttl Receipts U – On Order U- Commitments U + On Order

Cancel U)

Outbound Freight C

•  Plan version: Wp, Tgt, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Outgoing Freight Cost on Returns to Vendor.

•  Calculation:  (Return to Vendor C * Outbound Freight C%)

Outbound Freight C %

•  Plan version: Wp, Tgt, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Outgoing Freight Cost expressed as a percent of Returns to

Vendor Cost.

•  Calculation: (Outbound Freight C/ Returns to Vendor C)

Outbound Freight varLY C%

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Outbound Freight cost

over Last Year.

•  Calculation:  (Wp Outbound Freight C – Ly Outbound Freight C)/Ly

Outbound Freight C)

ProjRec AUR

•  Plan version: Wp, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Projected Receipts.

•  Calculation: (Projected Receipts R / Projected Receipts U)

ProjRec C

•  Plan version: Wp, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cost of Projected Receipts.

•  Calculation: (Projected Receipts R *(1 - IMU  Projected Receipts  %)

 Chapter 4 – Measure descriptions   123

ProjRec U

•  Plan version: Wp, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Unit Projected Receipts.

•  Calculation: (Proj Rec R / Proj Rec AUR)

ProjRec R

•  Plan version: Wp, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Value of Projected Receipts.

•  Calculation: ( EOP R – BOPR + Sls R + Markdowns R – Markups R +

Shrink R + Return to Vendor R – Reclass In R + Reclass Out R – Received R
– Transfer In R + Transfer Out R + Empl Disc R)

ProjRec var Recvd Ly R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Projected Receipts value

over Last Year Receipt value  .

•  Calculation: ((Wp Proj Rec R – Ly Recvd R)/Ly Recvd R)

ProjRec var SWa R %

•  Plan version: Wp

•  Planning role: Manager

•  Description: Percentage increase or decrease of Wp Projected Receipts value

over Summary Waiting for Approval.

•  Calculation: ((Wp Proj Rec R - SWa Proj Rec R)/SWa Proj Rec R)

ProjRec var Tgt R %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp Projected Receipts value

over Target Receipt value.

•  Calculation: ((Wp Proj Rec R - Tgt Proj Rec R)/Tgt Proj Rec R)

Promo Sls AUR

•  Plan version: Wp, Ly, Cp, Op, SOp, Wa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Promotional Sales.

•  Calculation: (Promo Sls R / Promo Sls U)

124    TopPlan

Promo Sls C

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Promotional Sales Cost.

•  Calculation: None

Promo Sls R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Promotional Sales Value.

•  Calculation: Entered or  (Promo Sls cont Ttl Sls R % * Sls R)

Promo Sls U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Planner

•  Description: Promotional Sales Units.

•  Calculation: Entered or  (Clr Sls R / Clr Sls AUR)

Promo Sls cont Ttl Sls R %

•  Plan version: Wp, Ly

•  Planning role: Planner

•  Description: Promotional Sales value contribution to Sales.

•  Calculation: (Promo Sls R /Promo R)

Promo Sls cont Ttl Sls U %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Promo Sale Units contribution to Sales.

•  Calculation: (Promo Sls U / Promo U)

Promo Sls cont Time R %

•  Plan version: Wp, Ly

•  Planning role: Planner

•  Description: The contribution that a Last Year Promotional Sales Value at a
specific calendar hierarchy level bears to the Total Last Year Promotional
Sales Value at the highest calendar level.

•  Calculation: (Promo Sls R / ‘Year’ Promo Sls R )

 Chapter 4 – Measure descriptions   125

Promo Sls var Ly R %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp Promotional Sales value

over Last Year.

•  Calculation: ((Wp Promo Sls R - Ly Promo Sls R)/Ly Promo Sls R)

Promo Sls var Ly U %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp Promotional Sale units

over Last Year.

•  Calculation: ((Wp Promo Sls U - Ly Promo Sls U)/Ly Promo Sls U)

Reclass In AUR

•  Plan version: Wp, Ly Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Re-Classification additions.

•  Calculation: (Reclass In R / Reclass In U)

Reclass In C

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Inventory Re-Classification additions expressed at Cost.

•  Calculation:  (Reclass In R * (1 – IMU Reclass In R %)

Reclass In U

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Inventory Re-Classification additions expressed as Units.

•  Calculation:  (Reclass In R / Reclass In AUR)

Reclass In R

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op , SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Inventory Re-Classification additions expressed as a Value.

•  Calculation:  None

126    TopPlan

Reclass Out AUR

•  Plan version: Wp, Ly Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Re-Classification reductions.

•  Calculation: (Reclass Out R / Reclass Out U)

Reclass Out C

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Inventory Re-Classification reductions expressed at Cost.

•  Calculation: (Reclass Out R * (1 – IMU Reclass Out R %))

Reclass Out R

•  Plan version: Wp, Ly, Cp, Tgt, SCp, OP, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Inventory Re-Classification reductions expressed as a Value.

•  Calculation: None

Reclass Out U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Inventory Re-Classification reductions expressed as Units.

•  Calculation:  (Reclass Out R / Reclass Out AUR_)

Recvd AUR

•  Plan version: Wp, Ly,

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of merchandise Received into

inventory.

•  Calculation: (Received R / Received U)

Recvd C

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cost of merchandise received into inventory.

•  Calculation: None

 Chapter 4 – Measure descriptions   127

Recvd R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Value of merchandise Received into inventory.

•  Calculation: None

Recvd U

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Units of merchandise Received into inventory.

•  Calculation: None

Return to Vendor AUR

•  Plan version:  Wp, Ly,  Planning role: Manager, Planner

•  Description: Average Unit Retail value of merchandise Returned to Vendors.

•  Calculation: (Return to Vendor R / Return to Vendor U)

Return to Vendor C

•  Plan version:  Wp, Ly, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Cost of merchandise returned to vendor.

•  Calculation: (Return to Vendor R * (1 – IMU Return To Vendor R %))

Return to Vendor R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Value of merchandise Returned to Vendor

•  Calculation: None

Return to Vendor U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Units of merchandise Returned to Vendor.

•  Calculation: RetVen R/ RetVen AUR

128    TopPlan

Ret Process Fee per Unit C

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Per unit Return to Vendor Processing Fee Cost

•  Calculation: None

Reg Sls AUR

•  Plan version: Wp, Ly, Cp, Op, SOp, Wa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Regular Sales.

•  Calculation: (Reg Sls R / Reg Sls U)

Reg Sls C

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Regular Sales Cost.

•  Calculation: None

Reg Sls R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Regular Sales Value.

•  Calculation: Entered or  (Reg Sls cont Ttl Sls R % * Sls R)

Reg Sls U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Planner

•  Description: Regular Sales Units.

•  Calculation: Entered or  (Reg Sls R / Reg Sls AUR)

Reg Sls cont Time R %

•  Plan version: Wp, Ly

•  Planning role: Planner

•  Description: The contribution that a Last Year Regular Sales Value at a

specific calendar hierarchy level bears to the Total Last Year Regular Sales
Value at the highest calendar level.

•  Calculation: (Reg Sls R / ‘Year’ Reg Sls R )

 Chapter 4 – Measure descriptions   129

Reg Sls cont Ttl Sls R %

•  Plan version: Wp, Ly

•  Planning role: Planner

•  Description: Regular Sales value contribution to Sales.

•  Calculation: (Reg Sls R /Reg R)

Reg Sls cont Ttl Sls U %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Reg Sale Units contribution to Sales.

•  Calculation: (Reg Sls U / Reg U)

Reg Sls var Ly R %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp Regular Sales value over

Last Year.

•  Calculation: ((Wp Reg Sls R - Ly Reg Sls R)/Ly Reg Sls R)

Reg Sls var Ly U %

•  Plan version: Wp

•  Planning role: Planner

•  Description: Percentage increase or decrease of Wp Regular Sale units over

Last Year.

•  Calculation: ((Wp Reg Sls U - Ly Reg Sls U)/Ly Reg Sls U)

Selling Store On Hand R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manger, Planner

•  Description: Selling Store On Hand Value.

•  Calculation: None

Selling Store On Hand U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manger, Planner

•  Description: Selling Store On Hand Units.

•  Calculation: None

130    TopPlan

SellThru U %

•  Plan version: Wp, Ly Cp, SCpPlanning role: Manager, Planner

•  Description: Amount of merchandise sold in units expressed as a percentage

of total available inventory for a period of time  .

•  Calculation: (Sales U / (BOP U + TtlRec U))

SellThru R %

•  Plan version:  Wp, Ly, Cp, SCp, Op, SOp

•  Planning role: Manager, Planner

•  Description: mount of merchandise sold as a value expressed as a percentage

of total available inventory for a period of time.

•  Calculation: (Sales R / (BOP R + TtlRec R))

Shrink %

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Shrinkage expressed as a percentage of Sales.

•  Calculation: (Shrink R / Sales R )

Shrink AUR

•  Plan version: Wp, Ly, Cp, SCp, Op

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Shrinkage.

•  Calculation: (Shrink R / Shrink U)

Shrink R

•  Plan version: Wp, Ly, Tgt, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Shrinkage value, the total value of lost inventory over time due

to damage, misplacement, or theft.

•  Calculatio: (Sales R * Shrinkage %)

Shrink U

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Shrinkage units, the total units of lost inventory over time due to

damage, misplacement, or theft.

•  Calculation: (Shrink R / Shrink AUR)

 Chapter 4 – Measure descriptions   131

Sls AUR

•  Plan version: Wp, Ly, Kp, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Sales.

•  Calculation: (Sales R / Sales U)

Sls AUR var CP (SCp) R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales AUR over Current

Plan.

•  Calculation: ((Sales AUR - Cp (SCp) Sales AUR)/Cp (SCp Sales AUR))

Sls AUR var Ly R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales AUR over Last

Year.

•  Calculation: ((Sales AUR - Ly Sales AUR)/Ly Sales AUR))

Sls build rate R %

•  Plan version: Wp, Fcst, Frcst, Ly, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Ratio of Sales for this period to the Sales for the prior displayed

period.

•  Calculation: (Sales R Current Period / Sales R Last Period )

Sls Contr R%

•  Plan version: Kp

•  Planning role: Manager, Planner

•  Description: KeyPlan Sales Value expressed as a contribution to TopPlan

Wp Sales Value.

•  Calculation: (KP Sales R/WP Sales R)

Sls Contr U%

•  Plan version: Kp

•  Planning role: Planner

•  Description: KeyPlan Sales Units expressed as a contribution to TopPlan Wp

Sales Units.

•  Calculation: (KP Sales U / WP Sales U)

132    TopPlan

Sls contProd U %

•  Plan version: Wp, Ly, Cp, Fcst

•  Planning role: Manager, Planner

•  Description: The contribution of  Sales Units at a specific product hierarchy

level bears to the Total  Sales Units at the highest product level..

•  Calculation: (Sales U @ Base Intersection / Sales U @ Product Parent)

Sls contProd R %

•  Plan version: Wp, Fcst, Frcst, Ly, Cp

•  Planning role: Manager, Planner

•  Description: The contribution of a  Sales Value at a specific product

hierarchy level bears to the Total  Sales Value at the highest product level..

•  Calculation: (Sales R @ Base Intersection / Sales R @ Product Parent)

Sls contTime U %

•  Plan version: Wp, Ly, Cp

•  Planning role: Manager, Planner

•  Description: The contribution that  Sales Units at a specific calendar

hierarchy level bears to the Total  Sales Units at the highest calendar level.

•  Calculation: (Sales U @ Base Intersection / Sales U @ Time Parent)

Sls contTime R %

•  Plan version: Wp, Fcst, Frcst, Ly, Cp

•  Planning role: Manager, Planner

•  Description: The contribution that a  Sales Value at a specific calendar

hierarchy level bears to the Total  Sales Value at the highest calendar level

•  Calculation: (Sales R @ Base Intersection / Sales R @ Time Parent)

Sls Cost

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Workroom Cost and Other Cost of Sales.

•  Calculation: None

Sls Mrgn R %

•  Plan version: Kp

•  Planning role: Manager, Planner

•  Description: KeyPlan Selling Margin..

•  Calculation: None

 Chapter 4 – Measure descriptions   133

Sls U

•  Plan version: Wp, Ly, Tgt, Kp, Op, SOp, Cp, SCp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Sales Units

•  Calculation:  Manager:  (Mg Sales U / Mg Sales AUR)

•

 Planner:  (Pl Reg Sales U + Pl Promo Sales U + Pl Clr Sales U)

Sls R

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Wa, SWa Tgt, Fcst, Frcst, Kp

•  Planning role: Manager, Planner

•  Description: Revenue from sales expressed as a value.

•  Calculation: Manager:  None.

•

 Planner:  (Pl Reg Sales R + Pl Promo Sales R + Pl Clr Sales R)

Sls varCP (SCp) U %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales units over Current

Plan.

•  Calculation: ((Wp Sales U - Cp (SCp) Sales U)/Cp (SCp) Sales U)

Sls varCP (SCp) R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales value over Current

Plan.

•  Calculation: ((Wp Sales R - Cp (SCp)Sales R)/Cp (SCp) Sales R)

Sls var Fcst R %

•  Plan version: Wp, Cp, SCp, Op, SOp, Wa

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales value over the

Sales Forecast (In-Season).

•  Calculation: ((Wp Sales R - Fcst Sales R)/Fcst Sales R)

134    TopPlan

Sls var Frcst R %

•  Plan version: Wp, Cp, SCp, Op, SOp, Wa

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales value over the

Sales Forecast (Pre-Season).

•  Calculation: ((Wp Sales R - Frcst Sales R)/Frcst Sales R)

Sls var Ly U %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales units over Last

Year.

•  Calculation: ((Wp Sales U - Ly Sales U)/Ly Sales U)

Sls var Ly R %

•  Plan version: Wp, Cp, SCp, OP, SOp, Fcst, Frcst, Wa

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales value over Last

Year.

•  Calculation: ((Wp Sales R - Ly Sales R)/Ly Sales R)

Sls varTgt R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease in Wp Sales value over Target.

•  Calculation: ((Wp Sales R - Tgt Sales R)/Tgt Sales R)

Sls exc VAT

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op, SOp

•  Planning role: Manager, Planner

•  Description: Sales Excluding VAT Value.

•  Calculation: None

Stk OH C

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Stock On Hand Cost.

•  Calculation: None

 Chapter 4 – Measure descriptions   135

Stk OH R

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Stock On Hand Value.

•  Calculation: None

Stk OH U

•  Plan version: Wp, Ly

•  Planning role: Manager, Planner

•  Description: Stock On Hand Units.

•  Calculation: None

Stock Adjustment C

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Stock Adjustment Cost.

•  Calculation: (BOP C – Stock On Hand C)

Stock Adjustment R

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Stock Adjustment Value.

•  Calculation: (BOP R – Stock OnHand R)

Stock Adjustment U

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Stock Adjustment Units.

•  Calculation: (BOP U – Stock On Hand U)

Stk/Sls U

•  Plan version: Wp, Ly, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Stock to sales ratio units.

•  Calculation: (BOP U / Sales U)

136    TopPlan

Stk/Sls R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp

•  Planning role: Manager, Planner

•  Description: Stock-to-sales ratio.

•  Calculation: (BOP R / Sales R)

TO

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Turnover based on Values.  Frequency with which inventory

value is sold and replaced over a stated time period.

•  Calculation: (Sales R / Average Inventory R)

TO U

•  Plan version: Wp, Ly, Op, SOp, Cp, SCp, Tgt, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Turnover based on Units.  Frequency with which inventory units

are sold and replaced over a stated time period.

•  Calculation: (Sales U / Average Inventory U)

TtlRec AUR

•  Plan version: Wp, Ly, Kp, Cp, SCp

•  Planning role: Manager, Planner

•  Description: Average Unit Retail value of Total Receipts.

•  Calculation: (Total Receipts R / Total Receipts U)

TtlRec C

•  Plan version: Wp, Ly, Tgt, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Total receipts cost.

•  Calculation: (Receipts C + Projected Receipts C)

TtlRec U

•  Plan version: Wp, Ly, Tgt, Kp  Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Total receipts units.

•  Calculation:  (Receipts U + Projected Receipts U)

 Chapter 4 – Measure descriptions   137

TtlRec R

•  Plan version: Wp, Ly, Tgt, Kp, Cp, SCp, Op, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Total Receipts expressed as a Value.

•  Calculation: (Receipts R + Projected Receipts R)

TtlRec contr R%

•  Plan version: Kp

•  Planning role: Planner

•  Description: KeyPlan Receipt Value expressed as a contribution to TopPlan

Wp Total Receipt Value.

•  Calculation: (Kp Total Rcpt R / Wp Total Rcpt R )

TtlRec contr U%

•  Plan version: Kp

•  Planning role: Planner

•  Description: KeyPlan Receipt Units expressed as a contribution to TopPlan

Wp Total Receipt Units.

•  Calculation: (Kp Total Rcpt U / Wp Total Rcpt U)

TtlRec varCP (SCp) R

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Total Receipts value

over Current Plan.

•  Calculation: ((Ttl Receipts R - Cp (SCp) Ttl Receipts)/Cp (SCp)Ttl Receipts)

TtlRec var Ly R %

•  Plan version: Wp

•  Planning role: Manager, Planner

•  Description: Percentage increase or decrease of Wp Total Receipts value

over Last Year.

•  Calculation: ((Ttl Receipts R - Ly Ttl Receipts R)/Ly Ttl Receipts R)

Ttl Ret Process Fee

•  Plan version: Wp, Op, SOp, Cp, SCp, Ly, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Total Return to Vendor Processing Fee at Cost.

•  Calculation: (Return To Vendor  U * Ret Process Fee C)

138    TopPlan

WOS U

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Ratio of Beginning of Period Inventory Units to Sales Units for

a specific period of time.

•  Calculation: (BOP U / (Sales U / number of weeks in period))

WOS R

•  Plan version: Wp, Ly, Cp, SCp, Op, SOp, Wa, SWa

•  Planning role: Manager, Planner

•  Description: Ratio of Beginning of Period Inventory Value to Sales Value for

a specific period of time.

•  Calculation: (BOP R / (Sales R / number of weeks in period))

ChannelPlan measures

The Channel plan involves the following measures:

# of Stores

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Total number of stores.

•  Calculation:  None

# of Stores Comp

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Total number of stores open last year and this year.

•  Calculation: None

# of Stores NonComp

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Total number of stores not open last year.

•  Calculation: None

 Chapter 4 – Measure descriptions   139

AvgInv V

•  Plan version: Wp, Ly, Mp

•  Planning role: Channel

•  Description: Average inventory value.

•  Calculation: (Ch Wp Sales R/ Ch Wp Turnover -)

AvgInv var Ly R %

•  Plan version: Wp

•  Planning role: Channel

•  Description: Percentage increase or decrease in average inventory this year

over last year.

•  Calculation: ((Ch Wp Avg Inv R – Ch Ly Avg Inv R)/ Ch Ly Avg Inv R)

AvgInv var MP R %

•  Plan version: Wp

•  Planning role: Channel

•  Description: Percentage increase or decrease in average inventory over the

merchandise (product) plan.

•  Calculation: ((Ch Wp Avg Inv R - Mp Avg Inv R)/Mp Avg Inv R)

Avg Sq Ft

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Average square feet per channel hierarchy member.

•  Calculation: None

Sls V

•  Plan version: Wp, Ly, Mp, Fcst

•  Planning role: Channel

•  Description: Sales value.

•  Calculation: None

Sls Comp R

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Sales value for stores open last year and this year.

•  Calculation: (Ch Sales R * (Number of Stores Comp / Number of Stores))

140    TopPlan

Sls Comp var Ly R %

•  Plan version: Wp

•  Planning role: Channel

•  Description: Percentage increase or decrease in comparative sales this year

over last year.

•  Calculation: (Ch Wp Sales R Comp – Ch Ly Sales R Comp)/ Ch Ly Sales R

Comp )

Sls cont Chain R %

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: The contribution that a sales value at a specific channel

hierarchy level makes to the total sales value at the highest channel level.

•  Calculation: (Ch Wp Sales R at current location intersection/ Ch Wp Sales R

@ total channel)

Sls contTime R %

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: The contribution that a sales value at a specific calendar

hierarchy level makes to the total sales value at the highest calendar level.

•  Calculation: (Ch Wp Sales R at current time intersection/ Ch Wp Sales R @

year)

Sls NonComp R

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Sales value for stores not open last year.

•  Calculation: (Ch Sales R  * (Number of Stores NonComp / Number of

Stores))

Sls varFcst R %

•  Plan version: Wp

•  Planning role: Channel

•  Description: Percentage increase or decrease in markdown this year over the

sales forecast.

•  Calculation: (Ch Wp Sales R – Ch Fcst Sales R)/ Ch Fcst Sales R)

 Chapter 4 – Measure descriptions   141

Sls var Ly R %

•  Plan version: Wp

•  Planning role: Channel

•  Description: Percentage increase or decrease in sales this year over last year.

•  Calculation: (Ch Wp Sales R – Ch Ly Sales R)/ Ch Ly Sales R)

Sls var MP R %

•  Plan version: Wp

•  Planning role: Channel

•  Description: Percentage increase or decrease in sales over the merchandise

(product) plan.

•  Calculation: (Ch Wp Sales R - Mp Sales R)/Mp Sales R)

Sls/Sq Ft

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Sales per square foot.

•  Calculation: (Ch Wp Sales R / Ch Wp Square Feet )

Sq Ft

•  Plan version: Wp, Ly

•  Planning role: Channel

•  Description: Square footage applicable to a channel hierarchy member.

•  Calculation: None

TO

•  Plan version: Wp, Ly, Mp

•  Planning role: Channel

•  Description: Turnover based on values: the frequency with which inventory

is sold and replaced over a stated period.

•  Calculation: (Ch Wp Sales R / Ch Wp Average Inventory R)

TO varMP

•  Plan version: Wp

•  Planning role: Channel

•  Description: Percentage increase or decrease in turnover over the

merchandise (product) plan.

•  Calculation: (Ch Wp TO - Mp TO)/Mp TO )

Glossary   143

Glossary

Ad

See Admin (Ad) plan version.

Admin (Ad) plan version

A plan version used only for the plan approval process that contains the approval
measures that allow the Planner to submit a plan for approval and the Manager to
approve/reject plans submitted for approval.

aggregate

To summarize data at a lower hierarchy level into a single category at a higher
hierarchy level.

To roll-up worksheet data.

See also aggregation method.

aggregation method

The method used to aggregate data, or to provide a summary view of lower-level
data at a higher level of aggregation.  A measure’s aggregation method
determines how the system populates aggregate level cells based on the
component values of base-level cells.

In dialogs that prompt you to specify an aggregation method, the choices and
their meanings are as follows:

•

•

? :  Aggregate by displaying the first lower level value if they are all the
same; otherwise, display a ‘?.’

? of Populated:  Aggregate by displaying the first non-NA lower level value
if they are all the same; otherwise, display a ‘?.’

•  Avg:  Aggregate by displaying the average of all lower-level values.

•  First:  Aggregate by displaying the first of all lower-level values.

•  Last:  Aggregate by displaying the last of all lower-level values.

•  Last of Populated: Aggregate by displaying the last of all non-NA lower-

level values.

•  Logical Count:  Aggregate by counting the logical cells at the lower level and

displaying this value in the aggregate cell.

•  Logical Count of Populated:  Aggregate by counting the logical cells at the

lower level if there is at least one populated cell.

•  Max:  Aggregate by displaying the maximum of all lower-level values.

•  Min:  Aggregate by displaying the minimum of all lower-level values.

•  Period End Avg:  Aggregate by displaying the period-ending average.

144    TopPlan

•  Period End Total:  Aggregate by displaying the period-ending total, or total

value present at period end.

•  Period Start Avg:  Aggregate by displaying the period-starting average.

•  Period Start Total:  Aggregate by displaying the period-starting total, or total

value present at period start.

•  Pop Count:  Aggregate by counting the populated cells at the lower level and

displaying this value in the aggregate cell.

•  Total:  Aggregate by summing up all lower-level values.

approval

See plan approval.

approver

In Retek TopPlan – for merchandise planning, the person or persons in the
manager’s role within the organization responsible for approving plans from the
planner’s role, the level below the manager’s role.

See also approver reconciliation, plan approval.

approver reconciliation

The process of reconciling a working plan to the consolidation of plans from the
next level below. The approver/manager identifies the Waiting for Approval
plans that are needed to complete the approver reconciliation. Once all the plans
are submitted, the approver/manager compares the consolidation of the planners’
Waiting for Approval (WA) plans to the approver’s own Working plan and other
selected plan versions. The approver/manager may change the Working plan to
reflect the consolidated Waiting for Approval plans, and save this reconciled
Working plan.

See also reconciliation, planner reconciliation.

attribute

A piece of information associated with a given dimension that helps to further
describe the positions contained in that dimension.  For example, positions in the
SKU dimension of the product hierarchy could be described by the attributes
COLOR, SIZE, and LABEL.  Positions can be described by any number of
attributes; LABEL is the only required attribute.  Attributes can be displayed in
the grid, if desired, and attributes can be used to sort positions within a
dimension.

auto build queue

The automatic workbook build queue that specifies the Retek Predictive
Solutions workbooks to be automatically built during user-defined batch runs.
Workbooks are added to and deleted from this queue through the Workbook
Auto Build Maintenance wizard.

axis

On a grid, a row (x-axis), column (y-axis), or slice (pages).  Each axis is used to
display one dimension of an item.

Glossary   145

Ch

See Channel Planner (Ch) planning role.

channel plan

The result of the channel planning process, which consists of a channel hierarchy
(for example, Channel to Store) over a fixed period of time (for example,
preseason Fall 2001), and a set of measures in which the detailed data of the plan
are stored. Measures included in the channel plan include Sales V, Square Feet,
Sales per Square Foot, Sales Comparable, and Sales NonComparable data,
presented in different plan versions, such as merchandise plan values, forecast
values, last year’s values, and planned values.

See also channel planning, Channel Planner (Ch) planning role.

ChannelPlan

One of the Retek Predictive Solutions, used to plan Sales Value and Average
Inventory for the multiple channels in a business, from stores to Internet-based
sales.

See also channel plan, channel planning.

Channel Planner (Ch) planning role

A role assigned in Retek ChannelPlan, where the main task is planning Sales
Value and Average Inventory for the multiple channels in a business, from stores
to Internet-based sales.

See also channel plan, channel planning.

channel planning

Planning for multiple channels in a business, from stores to Internet-based sales
to catalog divisions.

See also channel plan, Channel Planner (Ch) planning role.

commit

Transferring saved workbook data to the master database, allowing other users to
access and use the data.

Current Plan (Cp)

An in-season plan that has been approved and promoted from Waiting for
Approval (Wa) to Current Plan (Cp) version.

The Current Plan version applies to users in the Planner role, while the Submitted
Current Plan (SCp) plan version applies to users in the Manager and Executive
planning roles. Only users in the Manager or Executive planning role can view
the Submitted Current Plan version.

146    TopPlan

The Planner’s plan is the only plan that gets approved and becomes the Current
Plan. The Manager and Executive have a view to the approved plan via the
Submitted Current Plan plan version.

Curve

An optional automated predictive solution that transforms organization-level
assortment plans into base-level weekly sales forecasts. Curve converts higher
level sales predictions (the assortment plan) to the lower level predictions
required by particular operating systems. Curve generates these lower level sales
predictions by exploding the assortment plan across the product, location, or time
hierarchies.  A series of profiles, or spreading ratios, are used in the explosion
process.  Typical profiles can include, but are not limited to, store participation,
size distribution, and time (phase-to-week) profiles.  The source and destination
levels of the forecast spreading (transformation) uniquely describe each profile.
Profiles are generated using historical data and phase definitions, based on your
system configuration.

dimension

A quality of an item (such as a product, location, or time) that can be displayed
on an axis of a grid.  For example, product, location, or time.

display area

One of three portions of a worksheet that contain the measures and hierarchy
tiles.

display order

The order in which the attributes of a dimension are displayed on a specific axis
of grid.  Users define which attributes to display and their display order.  Display
order is independent of sort order.

Ex

See Executive (Ex) planning role.

Executive (Ex) planning role

One of the planning roles supported in Retek TopPlan. The Executive role is
typically concerned with high-level strategic merchandise plans for an
organization.

Fcst

See Forecast (Fcst) plan version.

financial planning

The process of developing pre-season and in-season financial plans for a
business, including sales and profit projections, Open to Buy (OTB)
management, and full value and unit calculations.

See also pre-season financial plan, in-season financial plan.

Forecast (Fcst) plan version

A plan version that provides a reference to the sales forecast.

Glossary   147

forecast-driven planning

Planning that keys off of forecasts fed directly into a planning system.
Connection to Retek Demand Forecasting (RDF) is built directly into the
business process supported by Retek Predictive Planning through an automatic
approval of a forecast that is fed directly in the planning system. This allows you
to accept all or part of Sales Value forecast. Once that decision is made, the
balance of business measures are planned within Retek Predictive Planning.

hierarchies

Structures used to define subordinate relationships among items in a dimension,
such as product, location, time, or other.

hierarchy tile

Hierarchies are the structures used by an organization to describe the
relationships that exist between the many dimensions. Typically, any dimension
will belong to one of these hierarchies (there may be others, but these are the
most common): Product, Location, or Calendar (or Time). The Measure
hierarchy consists of the measures, or metrics on the worksheet. These
hierarchies are represented on the worksheet by hierarchy tiles, or named gray
rectangles that represent each hierarchy. The hierarchy tiles you will see in Retek
Predictive Solutions include:

in-season financial plan

A financial plan that provides a view of the financial picture once the trading
season has begun. By viewing the measures on the in-season plan, you can
identify and make changes and recognize issues and opportunities, such as
available Open to Buy amounts. Retek Predictive Planning allows you to revise
plans to review effects of changing key values in the trading process without
losing the Original plan approved prior to the start of the trading season. Revised
plans created in-season are approved and saved as the Current Plan.

See also financial planning, pre-season financial plan.

KeyPlan

One of the Retek Predictive Solutions, KeyPlan is a unit and value planning tool
that enables retailers to plan and monitor items or groups of items whose
revenue, profitability, and efficient use of inventory are recognized as being most
critical to the success of the retail operation.

These key items are set up pre-season and linked to the appropriate historical
data. In-season, actual information flows from the merchandise transactional
system into the key item plan and is compared to the historical figures. The
original plan, forecast, and trend are evaluated and any appropriate adjustments
can then be made. As the season progresses, this process continues as more
actual data becomes available, and visibility to the original plan and historical
data remains and can be used to make further adjustments.

In Retek TopPlan, measure labels from KeyPlan are visible through the KeyPlan
(Kp) plan version, though no actual measure data is displayed at this time.

148    TopPlan

KeyPlan (Kp) plan version

A plan version showing KeyPlan or key item planning measures within TopPlan.

Note:  While this plan version is visible (through the Show-Hide Measures
feature) and the appropriate measures can be created and inserted into a
worksheet, there is no data available. That is, the measure labels are visible, but
the data fields are just blank cells at this time.

Kp

See KeyPlan plan version.

Last Year (Ly) plan version

A plan version that provides a reference to last year’s historical data.

Ly

See Last Year (Ly) plan version.

Manager (Mg) planning role

One of the planning roles supported in Retek TopPlan. This planning role is
primarily concerned with developing financial plans and reconciling and
approving financial plans developed by planners in a subordinate Planning role.

master database

The main data repository where the application data for all the Retek Predictive
Solutions resides. To manipulate the data in the database, the appropriate
product, location, and time information is extracted from the database to a
workbook. The workbook is a temporary repository that you can use to
manipulate and analyze the data. The data in a workbook is committed, or
written, back to the master database through a commit function. For example,
planning data viewed on TopPlan worksheets is read from and written to the
master database.

Also referred to as the master cube.

measure

Any item of data that can be represented on a grid in worksheets. In the Retek
Planning Solutions, measures also specify exactly one role, version, metric, and
unit of measure For example, the measure for Planners Working Plan Sales
Value is expressed as Pl Wp Sales V.

measure description

The description of the measure that can be viewed in a workbook. This
description may contain relationships and calculations.

Merchandise Plan (Mp)

A plan version used by the Channel plannerin Retek ChannelPlan. The
Merchandise Plan provides a reference to the total Merchandise Plan from Retek
TopPlan (product plan) to compare to the total Channel Plan for Sales, Average
Inventory, and Turnover.

metric

A measure definition with the role, version, and units omitted, such as Sales,
Markdowns, Gross Margin.

Glossary   149

Mg

See Manager (Mg) planning role.

Mp

See Merchandise Plan.

Op

See Original Plan.

Original Plan (Op)

A pre-season plan that has been approved and promoted from Waiting for
Approval (Wa) to Original Plan (Op) version.  The Planner’s plan is the only
plan that gets approved and becomes the Original Plan. But the Manager and
Executive have a view to the approved plan via the Submitted Current Plan plan
version.

parent

For any cell at a given dimensional level, the cell at the next higher dimensional
level into which the original cell’s data values aggregate.  Along a particular path
of aggregation, a cell’s value can only roll up into one parent.

percent contribution

A measure attribute that specifies whether the measure displays actual data
values, or whether the measure displays the percentage of total that each measure
position represents relative to the next higher visible dimension in the grid.  The
Percent Contribution attribute can take on one of two values: None or Parent.

None: A measure with a percent contribution attribute value of ‘None’ displays
actual numeric data values for the measure in question (such as Sales Units).

Parent: For the same metric, a measure with a percent contribution attribute value
of ‘Parent’ displays for each position the percentage of total that the position
represents relative to the next higher visible dimension in the grid.

Also referred to as percent of parent.

pivot

To change the locations (relative to each other) of two or more hierarchy tiles on
the same axis of a grid.  This changes the display order of the data for the tiles.

150    TopPlan

plan approval

A phase in the planning process that occurs once plan reconciliation is complete.
As users in the Planner role submit the plans for approval to the approver in the
Manager role, the plan status is changed to Waiting for Approval.  All plans with
this status are held in the master database until they are approved.

Through the Alert Manager, the approver/manager can be notified that there are
plans ready for review and approval.  The approver accesses the plan and either
approves or rejects the lower level plan(s).  Once again, the Alert Manager can
highlight to the user/planner that this plan has been approved or rejected.

When approved, the plan moves to either Original Plan (Op) or Current Plan
(Cp), depending on the business process.  If the plan is rejected, it goes back to
the Working Plan (Wp) where the needed adjustments can be made.  The plan
can then be resubmitted for approval.

This approval process typically occurs once per planning season for Pre-Season
(Original Plan) and an estimated once per month, or as frequently as a retailer’s
specific process dictates, during In-Season (Current Plan).

See also reconciliation, plan rejection.

plan explosion

A forecasting application that transforms an assortment plan into an operational
sales plan.  Plan explosion meets the need of operational systems (such as
Demand Forecasting (RDF) or Retek Merchandising System (RMS)) for sales
predictions at a more detailed level than those provided by corresponding
planning programs.

plan rejection

Rejecting a plan at the plan approval phase. A rejected plan reverts from the
Waiting for Approval Plan (Wa) version to the Working Plan (Wp) version. The
planner responsible for the rejected plan is notified that the Waiting for Approval
(Wa) plan has been rejected, and can then make the necessary adjustments to the
Working Plan version. The plan can then be resubmitted for approval.

See also plan approval, reconciliation.

plan version

In Retek Predictive Planning, a unique set of data that provides access or
reference to merchandise or channel plans at different stages of the planning
work flow.

Planner (Pl) planning role

One of the planning roles in Retek TopPlan. This planning role is primarily
concerned with developing financial plans that must be reconciled with and
approved by planners in a Manager (Mg) planning role.

planner reconciliation

The process by which a planner reconciles a Working Plan (Wp) to the
manager’s Target Plan (Tgt) from the next level above.

See also reconciliation, approver reconciliation.

Glossary   151

planning horizon

The range of dates that encompass the total time periods involved in which all
pre-season and in-season planning activities occur. For example: Fall 2001
through Fall 2006.

planning measure

Measures that specify exactly one role, version, metric, and unit of measure. For
example, the measure for Planners Working Plan Sales Value is expressed as Pl
Wp Sales V.

planning role

A set of user groups built into products in the Retek Predictive Planning Suite
and associated with types of plans and measures in those plans. These roles are
customizable during implementation, and a default set of planning roles is
supplied. For example, in Retek TopPlan, the Executive (Ex) planning role is
concerned with developing a high-level strategic plan, while the Manager (Mg)
and Planner (Pl) roles are concerned with more detailed financial plans.

See also definitions for these planning roles: Executive (Ex), Manager (Mg),
Planner (Pl), Channel (Ch)

Pl

See Planner (Pl) planning role.

pre-season financial plan

A financial plan that provides a view of the financial picture before the trading
season has begun. Using the measures in the pre-season plan, you can compare
Working Plan sales to the automatically generated Forecasted Sales or compare
other measures to Last Year enabling the user to identify and recognize issues
and opportunities. Retek TopPlan allows you to create a plan in one role and to
view this plan as a plan version in another role such as a Target version or as a
Submitted version. Plans created pre-season are approved and saved as the
Original Plan.

Multiple pre-season periods can be defined for pre-season planning.

See also financial planning, in-season financial plan.

profile

Spreading ratios that are used in the SKU Explosion process.  Typical profiles
can include store participation, size distribution, and time (phase-to-week)
profiles, as well as other information.  Profiles are generated using historical data
and phase definitions, based on your system configuration.

Ra

See Reference Admin (Ra) plan version.

reconciliation

The process of reviewing and adjusting planned data to arrive at a plan that all
contributing parties have reviewed and approved.

See also planner reconciliation, approver reconciliation, plan approval, and plan
rejection.

152    TopPlan

Reference Admin (Ra) plan version

A plan version used only for the plan approval process that provides a reference
to plans that have been submitted for approval, and the status of the user’s plan.

register (a measure)

To store the measure in a standard way on the system server.

role

A user group that specifies a base intersection for a group of measures.

In dialogs that prompt you to specify the role attribute for the measure you want
to display, the choices and their meanings are as follows:

•  Pl = Planner

•  Mg = Manager

•  Ex = Executive

•  Ch = Channel

See also planning role.

rotate

To change the location of one hierarchy tile and its measure from one axis (y-
column, x-row, or page-slice) to another.

scaling factor

A multiplier associated with an individual measure that is applied to each edited
data value to speed the process of data entry.  Data values entered for measures
associated with a scaling factor are scaled to an internal value that is recognized
by the server (but not seen on the client display).  A scaling factor can be
specified as a prefix or a suffix:

•  Prefix:  A character string that appears before each data value for a selected
measure.  For example, the prefix ‘$’ could be specified for a measure to
indicate monetary data.

•  Suffix:  A character string that appears after each data value for a selected
measure.  For example, the suffix ‘k’ could be specified for a measure
associated with a scaling factor of 1000; then, entering the value ‘6’ in a cell
would result in the display of ‘6k’.

SCp

See Submitted Current Plan (SCp) version.

SOp

See Submitted Original Plan (SOp) plan version.

sort order

On a grid, the order by which displayed dimensions are listed.  Users define
which attributes to sort by and which to prioritize.  Sort order is independent of
display order.

Glossary   153

spread

To allocate data obtained from a single group at a higher hierarchy level into
groups in a lower level, in specified ratios or proportions.

stored measure

A stored measure is identical to an imported measure, except that no import
properties are specified.  If the measure is read/write, the user will be able to
commit data. If read-only, the measure may be imported internally from another
source.

Strategic Target Plan

An executive level plan used during the preseason planning process.  This plan
provides the vehicle to set targets for key merchandise planning measures such as
sales, average inventory, profit and turnover.

submission for approval

A step in the approval process performed by users in the Planner (Pl) role. The
planner submits the saved Working Plan (Wp) plan, which changes the plan
version to Waiting for Approval (Wa) version.  All plans with this Waiting for
Approval status are held in the master database until they are approved.

Submitted Current Plan (SCp) version

One of the plan versions involved in the financial planning process. The
Submitted Current Plan version is the Manager’s or Executive’s view of the most
recent Current Plan (Cp) version by a planner in a subordinate role. Data which
resides in the Current Plan is visible to the Manager and Executive via this
Submitted Current Plan version.

The Current Plan version applies to users in the Planner role, while the Submitted
Current Plan version applies to users in the Manager and Executive planning
roles. Only users in the Manager or Executive planning role can view the
Submitted Current Plan version.

The Planner’s plan is the only plan that gets approved and becomes the Current
Plan during the in-season planning process. The Manager has a view to the
approved plan via the Submitted Current Plan.

Submitted Original Plan (SOp) version

One of the plan versions involved in the financial planning process. The
Submitted Original Plan version is the Manager’s or Executive’s view of the
Original Plan (Op) version by a planner in a subordinate role. Data which resides
in the Original Plan is visible to the Manager and Executive via this Submitted
Original Plan version.

The Original Plan version applies to users in the Planner role, while the
Submitted Original Plan version applies to users in the Manager and Executive
planning roles. Only users in the Manager or Executive planning role can view
the Submitted Original Plan version.

154    TopPlan

The Planner’s plan is the only plan that gets approved and becomes the Original
Plan during the pre-season planning process The Manager has a view to that
approved plan via the Submitted Original Plan version.

Submitted Waiting for Approval (SWa) plan version

A plan version that exists for those the Executive (Ex) and Manager (Mg) roles to
view the Planner’s Working Plan that has been submitted for approval .

SWa

See Submitted Waiting for Approval (SWa) plan version.

Target (Tgt) plan version

A plan version that exists for planning roles that have a superior role; that is,
Manager (Mg) and Planner (Pl). The Manager receives a Target plan version
from the Executive and the Planner receives a Target plan version from the
Manager.

Tgt

See Target (Tgt) plan version.

top-down role

The planning role to which a particular planning role reports up to. For example,
in the planning roles supplied with Retek TopPlan, the Manager (Mg) planning
role reports up to the Executive (Ex) planning role. This is a top-down role for
the Manager planning role. The Planner (Pl) planning role reports up to the
Manager (MG) planning role. This is the top-down role for the Planner planning
role.

TopPlan

One of the Retek Predictive Solutions, used to develop financial plans, including
high-level strategic plans, and financial plans, both pre-season and in-season in
values and units.

units

The units that define how data will be processed and displayed.

In dialogs that prompt you to specify the units for measures, the choices and their
meanings are as follows:

•  Check = check box (Boolean)

•  C = cost

•  C% = cost value % variance or contribution

•  D = date

•  Select = picklist

•  Stores = number of stores

•  V = retail value

•  V% = retail value % variance or contribution

•  Text = text

Glossary   155

•  True-False = true-false (Boolean)

•  U = units

•  U% = units % variance or contribution

•  No Units = used within Retek TopPlan for ratios, Average Unit Retail (AUR)

X = none

user group

A subset of application users to which a given user belongs. Users must be
assigned to a user group. Assigning users to groups provides a level of security
into workbooks that users create and save. When users save a workbook, they
assign one of three access permissions to the workbook: allow any user to open
and edit the workbook, allow only those users in their same group to open and
edit the workbooks, or allow no other users to open and edit the workbook.

Users are typically assigned to groups based on similarities in job functions.
Users in the same group can be given access to workbooks that belong to that
group alone.

User groups are defined in the User Account Management workbook, and viewed
in the Groups Worksheet of the User & Template Administration workbook.

For Retek Predictive Planning, see also planning role.

version

A grouping of measures by workflow or data source. For products in the Retek
Predictive Planning Suite, this term is used to refer to plan versions.  In dialogs
that prompt you to specify the version, the choices and their meanings are as
follows:

•  Ad = Administrative
•  Cp = Current Plan
•  Fcst = Forecast
•  Kp = Key Plan
•  Ly = Last Year
•  Op = Original Plan
•  Ra = Reference Admin (Summary)
•  SCp = Submitted Current Plan
•  SOp = Submitted Original Plan
•  SWa = Submitted Waiting for Approval
•  Tgt = Target
•  Wa = Waiting for Approval

•  Wp = Working Plan

156    TopPlan

Waiting for Approval (Wa) plan version

A plan that is awaiting approval by planner’s manager in a superior role.

If the plan is approved, a Waiting for Approval plan is promoted to either the
Original Plan (Op) version or Current Plan (Cp).

If the plan is rejected, it goes back to the Working Plan (Wp) version, where the
needed adjustments can be made.

watch measure

A custom measure that is used as the basis for an alert. Watch measures are
created using the Measure Maintenance dialog, and associated with alerts using
the Alert Builder wizard.

wizard

A set of screens that guide you through the process of creating a new workbook
or performing other actions in an application, by asking you various questions
and having you select values.

workbook

The framework used for displaying data and user functions.  Workbooks are task-
specific and may contain one or more worksheets.  Users can define the format of
their workbooks.

See also workbook template, worksheet.

workbook template

The framework for creating a workbook. You build each new workbook from an
existing workbook template, such as Pre-Season Financial Plan or Forecasting
Administration.  Several workbook templates are supplied with the Retek
Predictive Solutions, and are available for selection when you choose File+New
to create a new workbook.

Working Plan (Wp)

The plan version that is editable for a particular pre-season or in-season period.
This plan version is used to develop and revise plans.

A plan that is rejected during the approval process reverts back to the Working
Plan version, where the needed adjustments can be made.

worksheet

A multidimensional spreadsheet used to display workbook-specific information.
Worksheet data can also be displayed in chart format.

Wp

See Working Plan.

zoom

When working with a grid, the zoom feature enlarges the grid contents of the
active window for easier viewing, or reduces the size of the contents in order to
fit as much data on the terminal display as possible.

