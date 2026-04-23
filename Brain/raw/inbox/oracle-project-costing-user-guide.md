---
date: 2026-04-23
type: raw
source: Brain/raw/inbox/Oracle Project Costing User Guide.pdf
tags: []
project: 
status: unprocessed
---

# Oracle Project Costing User Guide

## Source

File: `Brain/raw/inbox/Oracle Project Costing User Guide.pdf`
Size: 3,640,878 bytes
Extracted via: markitdown

## Extracted content

Oracle® Project Costing
User Guide
Release 11i

Part No. B10855-02

May2005

Oracle Project Costing User Guide, Release 11i

Part No. B10855-02

Copyright © 1994, 2005, Oracle. All rights reserved.

Primary Author:

Jeffrey Colvard, Stephen A. Gordon

Contributing Author:

Janet Buchbinder, Juli Anne Tolley

Contributor:
Lowell, Cedric Ng, Murali Sundaresan

Peter Budelov, Nalin Chouhan, Barbara Fox, Neeraj Garg, Dinakar Hituvalli, Jeanne

The Programs (which include both the software and documentation) contain proprietary information; they
are provided under a license agreement containing restrictions on use and disclosure and are also protected
by copyright, patent, and other intellectual and industrial property laws. Reverse engineering, disassembly,
or decompilation of the Programs, except to the extent required to obtain interoperability with other
independently created software or as specified by law, is prohibited.

The information contained in this document is subject to change without notice. If you find any problems
in the documentation, please report them to us in writing. This document is not warranted to be error-free.
Except as may be expressly permitted in your license agreement for these Programs, no part of these Programs
may be reproduced or transmitted in any form or by any means, electronic or mechanical, for any purpose.

If the Programs are delivered to the United States Government or anyone licensing or using the Programs on
behalf of the United States Government, the following notice is applicable:

U.S. GOVERNMENT RIGHTS
Programs, software, databases, and related documentation and technical data delivered to U.S. Government
customers are "commercial computer software" or "commercial technical data" pursuant to the applicable
Federal Acquisition Regulation and agency-specific supplemental regulations. As such, use, duplication,
disclosure, modification, and adaptation of the Programs, including documentation and technical data, shall be
subject to the licensing restrictions set forth in the applicable Oracle license agreement, and, to the extent
applicable, the additional rights set forth in FAR 52.227-19, Commercial Computer Software--Restricted Rights
(June 1987). Oracle Corporation, 500 Oracle Parkway, Redwood City, CA 94065.

The Programs are not intended for use in any nuclear, aviation, mass transit, medical, or other inherently
dangerous applications. It shall be the licensee's responsibility to take all appropriate fail-safe, backup,
redundancy and other measures to ensure the safe use of such applications if the Programs are used for such
purposes, and we disclaim liability for any damages caused by such use of the Programs.

The Programs may provide links to Web sites and access to content, products, and services from third parties.
Oracle is not responsible for the availability of, or any content provided on, third-party Web sites. You bear
all risks associated with the use of such content. If you choose to purchase any products or services from
a third party, the relationship is directly between you and the third party. Oracle is not responsible for: (a)
the quality of third-party products or services; or (b) fulfilling any of the terms of the agreement with the
third party, including delivery of products or services and warranty obligations related to purchased products
or services. Oracle is not responsible for any loss or damage of any sort that you may incur from dealing
with any third party.

Oracle, JD Edwards, and PeopleSoft are registered trademarks of Oracle Corporation and/or its affiliates.
Other names may be trademarks of their respective owners.

Contents

Send Us Your Comments

Preface

1 Overview of Project Costing

Calculating Costs

Overview of Costing .

.

.

.

.

.
.

.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
Costing in Oracle Projects .
.
Costing Processes
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
Calculating Labor Cost
Calculating Cost for Expense Reports, Usages, and Miscellaneous Transactions .
.
.
.
Calculating Burden Cost
.
Calculating Cost for Supplier Invoices
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
Selecting Expenditure Items .
.
.
Processing Straight Time
.
.
Creating Overtime .
.
.
Processing Overtime
.
Generating Labor Output Reports
Calculating and Reporting Utilization .

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.

.
.

.
.

.

.

.

.

.

.

Distributing Labor Costs .

2 Expenditures

.

.

.

.

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.

Overview of Expenditures

.
.
.
.
Expenditure Classifications
.
.
Expenditure Amounts
.
Expenditure Entry Methods .
Expenditure Item Validation .
.
Expenditure Rejection Reasons .
Processing Pre-Approved Expenditures

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
Entering Pre-Approved Expenditure Batches .
.
.
Entering Expenditures
.
.
Entering Currency Fields
Uploading Expenditure Batches from Microsoft Excel
.
Copying an Expenditure Batch .
.
.
Verifying Control Totals and Control Counts .

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.

.

.

.

.

.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

1- 1
1- 2
1- 3
1- 5
1- 5
1- 5
1- 6
1- 6
1- 6
1- 8
1- 8
1- 9
1-10
1-11
1-11

2- 1
2- 2
2- 2
2- 2
2- 2
2- 3
2-10
2-12
2-14
2-17
2-19
2-20
2-21

iii

Controlling Expenditures

Viewing Expenditures .

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.
.

.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
Submitting an Expenditure Batch .
Reviewing and Releasing Expenditure Batches .
.
Reversing an Expenditure Batch .
.
.
.
.
.
.
Correcting Expenditure Batches
.
.
.
.
.
Using Transaction Control Extensions .
.
.
Inclusive and Exclusive Transaction Controls
.
.
Determining if an Item is Chargeable .
Determining if an Item is Billable or Capitalizable
.
Examples of Using Transaction Controls .

.
.
.
.
.
.
.
.
.
.
.
CASE 1: Limited employees charge limited expenses
CASE 2: Different expenditures charged during different phases of a project
CASE 3: Some tasks, but not all, are only chargeable for labor expenditures
.
.
.
.
Viewing Expenditure Items
.
Viewing Accounting Lines .
.
.
Expenditure Items Windows Reference .
.
.
Find Expenditure Items Window .
.
.
.
Expenditure Items Window .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
Audit Reporting for Expenditure Adjustments .
.
Types of Expenditure Item Adjustments .
.
Restrictions for Adjusting Converted Items
.
.
Adjusting Expenditure Items
.
.
Mass Adjustment of Expenditures
.
.
Transferring Expenditure Items
.
.
.
Splitting Expenditure Items
.
Adjustments to Multi-Currency Transactions
.
.
Adjustments to Burden Transactions
.
.
Adjustments to Related Transactions
.
.
.
Marking Items for Adjustments
.
.
.
.
Processing Adjustments
.
.
.
Results of Adjustment Processing
.
.
.
Adjustments to Supplier Invoices .

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.

.
.

.
.

.

.

.

.

.

.

.

.

.

.

Adjusting Expenditures

3 Burdening

Building Up Costs .

Overview of Burdening

Using Burden Structures .

.

.

.

.

.

.

.

.
.
.
.
.

Burden Calculation Process

.
Example of Cost Buildup .
.

.
.
.
.
.
Burden Structure Components .
.
.

.
.
.
.
.
.
.
.
.
Types of Burden Schedules
Defining Burden Schedule Versions .

.
.
.
.
.
.
.
.

.
.

.

.

Using Burden Schedules .

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

iv

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

2-22
2-22
2-22
2-23
2-24
2-25
2-25
2-28
2-30
2-31
2-31
2-32
2-33
2-38
2-38
2-40
2-41
2-41
2-42
2-44
2-44
2-45
2-48
2-49
2-50
2-51
2-51
2-52
2-53
2-54
2-55
2-57
2-59
2-62

3- 1
3- 2
3- 4
3- 4
3- 6
3- 7
3- 9
3-10
3-10

.

.

.

.

.

.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

Assigning Burden Schedules .

Assigning Burden Multipliers
.

.
.
.
.
Defining Burden Schedules for Project Types .
.
Assigning Burden Schedules at the Project and Task Level
.
Assigning Fixed Dates for Burden Schedules .
.
.
Changing Default Burden Schedules
.
.
Overriding Burden Schedules
.
Determining Which Burden Schedule to Use .
.
Storing, Accounting, and Viewing Burden Costs
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
Storing Burden Cost on the Same Expenditure Item .
.
Storing Burden Costs as a Separate Expenditure Item on the Same Project
Storing Burden Cost as Summarized Expenditures on a Separate Project .
.
.
Choosing a Burden Storage Method
.
Setting Up The Burden Cost Storage Method .
.
.
Accounting for Burden Costs
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
Accounting for Burden Costs by Burden Cost Component
.
.
Accounting for Total Burdened Cost
.
Storing Burden Costs with No Accounting Impact
.
.
Troubleshooting Burden Transactions .
.
.
.
.
.
.
.

.
.
.
.
Burden Multiplier Algorithm .
.
Accounting Transactions for Burden Cost Reporting .
Burdening Options for General Ledger Accounting and Reporting
.
.

.
.
.
Processing Transactions After a Burden Schedule Revision .
.
Reporting Burden Components in Custom Reports .
.
.
Revenue and Billing for Burden Transactions .
.
.
Reporting Requirements for Project Burdening .
.
.
.
GL and Upper Management Reporting .
.
.
.
.
.

.
Middle Management Reporting
Project Management Reporting .
.
Setting Up Burden Cost Accounting to Fit Reporting Needs

.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.

.
.
.
.

.
.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

4 Allocations

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.
.
.
.
.

Creating Allocations .

Overview of Allocations .

.
.
Understanding the Difference Between Allocation and Burdening
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
Defining Allocation Rules .
.
.
.
Allocating Costs
.
.
Releasing Allocation Runs .
.
.
.
Viewing Allocation Runs
.
Viewing Allocation Transactions .
.
.
.
Reversing Allocation Runs
.
.
Full and Incremental Allocations
About Previous Amounts and Missing Amounts in Allocation Runs
.
.
.
.

.
.
Creating AutoAllocations Sets .

AutoAllocations .

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.

.

.

.

.

.

.
.
.
.
.
.
.
.
.
.

.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.

3-11
3-13
3-13
3-13
3-13
3-14
3-14
3-15
3-15
3-15
3-17
3-18
3-19
3-19
3-20
3-21
3-23
3-25
3-25
3-25
3-29
3-30
3-31
3-31
3-33
3-35
3-36
3-40
3-41
3-43

4- 1
4- 2
4- 2
4- 3
4- 4
4- 6
4- 6
4- 9
4-10
4-10
4-11
4-11
4-11

v

.
Submitting an AutoAllocation Set
Viewing the Status of AutoAllocation Sets .

.

.

.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

4-13
4-15

5 Asset Capitalization

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.
.

.
.

.
.

.
.

.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

Defining and Processing Assets .

Overview of Asset Capitalization .
.

.
.
About Capital Projects
Capital Projects Processing Flow .

.
.
.
.
Accounting for Asset Costs in Oracle Projects and Oracle Assets
.
.
.
.
.
Creating Assets in Oracle Projects
.
Creating a Capital Asset .
.
.
.
Creating a Retirement Adjustment Asset .
Capital Project Flow .
.
.
.
Specifying Which Capital Asset Transactions To Capitalize .
.
.
Defining Assets
.
.
Copying Assets
.
.
.
.
.

.
.
.
.
.
.
.
Creating Purchase Orders for Capital Projects
.
Charging Supplier Invoice Lines to Projects
Charging Labor, Expense Reports, Usages, and Miscellaneous Transactions to Capital
.
.
.
.
Projects
.
Placing CIP Assets in Service .
.
.
Creating Fixed Assets from Capital Projects
.
Sending Retirement Costs to Oracle Assets .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
Asset Attributes
.
Placing an Asset in Service
Specifying a Retirement Date for Retirement Adjustment Assets
Creating and Preparing Asset Lines for Oracle Assets .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
Reversing Capitalization of Assets in Oracle Projects
.
Reversing Capitalization of an Asset or Event
.
Recapitalization of Reverse Capitalized Assets

.
.
.
.
.
.
.
.
.
Assigning an Asset to Unassigned Asset Lines .
Changing the Asset Assigned to an Asset Line .
.
.
Splitting an Asset Line
.
Adjusting Assets After Interface
.
Adjusting Capital Project Costs
Reversing Capitalization of Assets in Oracle Projects

.
.
.
.
Sending Asset Lines to Oracle Assets .
.
Asset Summary and Detail Grouping Options
.
.
.
.

.
.
Asset Grouping Levels
Specifying Grouping Level Types .
.
Assigning Assets to Grouping Levels .
.

Creating Capital Events .
.
Generating Summary Asset Lines
.
Allocating Asset Costs .

Reviewing and Adjusting Asset Lines .

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.

.
.

.
.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

5- 1
5- 1
5- 2
5- 4
5- 4

5- 5
5- 5
5- 5
5- 6
5- 6
5- 9
5- 9
5-10
5-10
5-11
5-12
5-13
5-13
5-14
5-18
5-18
5-19
5-20
5-21
5-25
5-26
5-27
5-27
5-27
5-28
5-32
5-32
5-33
5-33
5-33
5-34
5-34
5-35
5-35
5-36

vi

Capitalizing Interest .

.

.

.

.

Abandoning a Capital Asset in Oracle Projects .
.
.
.

.
.
.
.
Overview of Capitalized Interest
Defining Capitalized Interest Rate Names and Rate Schedules
.
.
Setting Up Capital Projects for Capitalized Interest
.
Generating Capitalized Interest Expenditure Batches
.
Reviewing Capitalized Interest Expenditure Batches

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.

6 Cross Charge

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

Transfer Pricing

Overview of Cross Charge .

.
Processing Flow for Cross Charge .

.
Cross Charge Business Needs and Example

.
Cross Charge Types .
Cross Charge Processing Methods and Controls

.
.
Project Structure: Distinct Projects by Provider Organization .
Project Structure: Single Project .
.
Project Structure: Primary Project with Subcontracted Projects
.

.
Cross Charge Processing Methods
.
.
.
Cross Charge Controls .
.
Cross Charge Processing Controls .
.
.
.
.
.
.
Borrowed and Lent Processing Flow .
Intercompany Billing Processing Flow .
Creating Cross Charge Transactions .
.
Processing Borrowed and Lent Accounting .

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
Determining Accounts for Borrowed and Lent Transactions
Generating Accounting Transactions for Borrowed and Lent Accounting
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
Run the Interface Cross Charge Distributions to General Ledger process .
.
.
.
.

.
Determining Accounts for Intercompany Billing Accounting .
.
.
.
Generating Intercompany Invoices .
.
.
.
.
Approving and Releasing Intercompany Invoices .
.
.
.
Interfacing Intercompany Invoices to Receivables
.
.
Interfacing Intercompany Invoices to Oracle Payables .
.
Interface Tax Lines from Payables to Oracle Projects .
.
.
.
Interfacing Cross Charge Distributions to General Ledger .

.
.
Overview of Cross Charge Adjustments .
.
Processing Flow for Cross Charge Adjustments

Processing Intercompany Billing Accounting .

Adjusting Cross Charge Transactions

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.

.
.
.
.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.

.
.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

7 Integration with Other Oracle Applications

Overview of Oracle Project Costing Integration .
.
Integrating Expense Reports with Oracle Payables and Oracle Internet Expenses .
.
.

.
Overview of Expense Report Integration
Setting Up in Payables and Oracle Projects .

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.
.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.

.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.

5-36
5-37
5-37
5-38
5-39
5-39
5-40

6- 1
6- 2
6- 4
6- 5
6- 6
6- 7
6- 8
6- 8
6- 9
6-10
6-13
6-14
6-14
6-15
6-16
6-18
6-18
6-19
6-21
6-22
6-26
6-28
6-28
6-30
6-31
6-31
6-32
6-32
6-32
6-35

7- 1
7- 1
7- 2
7- 3

vii

.

.

.
.
.

.
.
.
.

.
.
.
.
.
.

Processing Expense Reports Created in Oracle Projects

.
.
.
Distributing Expense Report Costs
.
Interfacing Expense Reports to Payables .
.
.
Importing Expense Reports in Payables
.
Tying Back Expense Reports from Payables
.
Submitting the Interface Streamline Processes
Transferring Payables Accounting Information to General Ledger .
.
.
.
.
.

Processing Expense Reports Created in Oracle Internet Expenses .
.
.
.
Advances and Prepayments .
.
.
.
.
Adjusting Expense Reports
.
.
.
.
Purging Expense Reports
.
Viewing Expense Reports in Oracle Payables .

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.
.
.

.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
.
.
.

.
Integrating with Oracle Assets

Integrating with Oracle Purchasing and Oracle Payables (Requisitions, Purchase Orders, and
.
Supplier Invoices) .
.
.
.
.
Project-Related Document Flow .
.
Integrating with Oracle Purchasing .
Integrating with Oracle Payables .
.
.
Entering Project-Related Information for Requisitions, Purchase Orders, and Supplier
.
.
.
.
Invoices .
.
Validating Purchase Orders, Requisitions, and Supplier Invoices
.
.
Accounting Transactions Created by the Account Generator
.
.
.
.
.
Commitment Reporting
Adjusting Project-Related Documents in Oracle Purchasing, Oracle Payables, and Oracle
.
.
Projects .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
Entering Project-Related Transactions in Oracle Inventory .
.
.
.
Collecting Inventory Costs
.
Transferring Inventory Costs to Oracle Projects .
.
.
.
Importing Inventory Transactions
.
.
Reviewing Imported Inventory Transactions .
.
.
.
Adjusting Inventory Transactions

.
.
.
.
.
.
.
.
Implementing Oracle Assets .
.
Interfacing Assets to Oracle Assets
.
.
.
Mass Additions
Viewing Capital Project Assets in Oracle Assets
.
.
Adjusting Assets .
.
Integrating with Oracle Project Manufacturing .
.
Importing Project Manufacturing Costs .
.
.

Integrating with Oracle Inventory .

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.
.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.
.

.
.
.
.

.
.
.

.
.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

.

7- 4
7- 5
7- 5
7- 6
7- 8
7- 9
7-10
7-10
7-13
7-13
7-15
7-15

7-16
7-17
7-17
7-18

7-20
7-23
7-24
7-24

7-28
7-31
7-32
7-32
7-33
7-34
7-34
7-35
7-35
7-36
7-37
7-38
7-38
7-38
7-38
7-39

Index

viii

Send Us Your Comments

Oracle Project Costing User Guide, Release 11i

Part No. B10855-02

Oracle welcomes your comments and suggestions on the quality and usefulness of this publication. Your
input is an important part of the information used for revision.

• Did you find any errors?
• Is the information clearly presented?
• Do you need more information? If so, where?
• Are the examples correct? Do you need more examples?
• What features did you like most about this manual?

If you find any errors or have any other suggestions for improvement, please indicate the title and part
number of the documentation and the chapter, section, and page number (if available). You can send
comments to us in the following ways:

• Electronic mail: appsdoc_us@oracle.com
• FAX: 650-506-7200 Attn: Oracle Projects Documentation Manager
• Postal service:

Oracle Projects Documentation Manager
Oracle Corporation
500 Oracle Parkway
Redwood Shores, CA 94065
USA

If you would like a reply, please give your name, address, telephone number, and electronic mail address
(optional).

If you have problems with the software, please contact your local Oracle Support Services.

ix

Preface

Intended Audience

Welcome to Release 11i of the Oracle Project Costing User Guide.

This guide contains the information you need to understand and use Oracle Project
Costing.

See Related Documents on page xii for more Oracle Applications product information.

TTY Access to Oracle Support Services

Oracle provides dedicated Text Telephone (TTY) access to Oracle Support Services
within the United States of America 24 hours a day, seven days a week. For TTY support,
call 800.446.2398.

Documentation Accessibility

Our goal is to make Oracle products, services, and supporting documentation accessible,
with good usability, to the disabled community. To that end, our documentation
includes features that make information available to users of assistive technology.
This documentation is available in HTML format, and contains markup to facilitate
access by the disabled community. Accessibility standards will continue to evolve over
time, and Oracle is actively engaged with other market-leading technology vendors to
address technical obstacles so that our documentation can be accessible to all of our
customers. For more information, visit the Oracle Accessibility Program Web site at
http://www.oracle.com/accessibility/ .

Accessibility of Code Examples in Documentation

Screen readers may not always correctly read the code examples in this document. The
conventions for writing code require that closing braces should appear on an otherwise
empty line; however, some screen readers may not always read a line of text that consists
solely of a bracket or brace.

Accessibility of Links to External Web Sites in Documentation

This documentation may contain links to Web sites of other companies or organizations
that Oracle does not own or control. Oracle neither evaluates nor makes any
representations regarding the accessibility of these Web sites.

xi

Structure

1 Overview of Project Costing

This chapter gives you an overview of project costing in Oracle Projects.

2 Expenditures
This chapter describes how to enter and manage expenditures using Oracle Projects.

3 Burdening

This chapter describes how to use burdening in Oracle Projects.

4 Allocations

This chapter describes how you can allocate costs to projects and tasks.

5 Asset Capitalization
This chapter describes how to create and maintain capital projects in Oracle Projects. It
provides a brief overview of capital projects and explains how to create, place in
service, adjust, and account for assets and retirement costs in Oracle Projects.

6 Cross Charge

This chapter describes accounting within and between operating units and legal entities.

7 Integration with Other Oracle Applications

This chapter describes integrating Oracle Projects with other Oracle Applications to
perform project costing.

Related Documents

You can choose from many sources of information, including online
documentation, training, and support services, to increase your knowledge and
understanding of Oracle Projects.

Online Documentation

All Oracle Applications documentation is available online (HTML or PDF).

• Online Help - Online help patches (HTML) are available on Oracle MetaLink.

• About Documents - Refer to the About Document for the mini-pack or family pack

that you have installed to learn about new documentation or documentation patches
that you can download. About Documents are available on Oracle MetaLink.

Guides Related to All Products

Oracle Applications User’s Guide

This guide explains how to enter data, query, run reports, and navigate using the
graphical user interface (GUI) available with this release of Oracle Projects (and any
other Oracle Applications products). This guide also includes information on setting
user profiles, as well as running and reviewing reports and concurrent processes.

You can access this user’s guide online by choosing "Getting Started with Oracle
Applications" from any Oracle Applications help file.

xii

Oracle Projects Documentation Set

Oracle Projects Implementation Guide

Use this manual as a guide for implementing Oracle Projects. This manual also includes
appendixes covering function security, menus and responsibilities, and profile options.

Oracle Projects Fundamentals

Oracle Project Fundamentals provides the common foundation shared across the Oracle
Projects products (Project Costing, Project Billing, Project Resource Management, Project
Management, and Project Collaboration). Use this guide to learn fundamental
information about the Oracle Projects solution.

This guide includes a Navigation Paths appendix. Use this appendix to find out how
to access each window in the Oracle Projects solution.

Oracle Projects Glossary

This glossary provides definitions of terms that are shared by all Oracle Projects
applications. If you are unsure of the meaning of a term you see in an Oracle Projects
guide, please refer to the glossary for clarification. You can find the glossary in the online
help for Oracle Projects, and in Oracle Projects Fundamentals.

Oracle Project Billing User Guide

Use this guide to learn how to use Oracle Project Billing to process client invoicing and
measure the profitability of your contract projects.

Oracle Project Management User Guide

This guide shows you how to use Oracle Project Management to manage projects
through their lifecycles -- from planning, through execution, to completion.

Oracle Project Resource Management User Guide

This guide provides you with information on how to use Oracle Project Resource
Management. It includes information about staffing, scheduling, and reporting on
project resources.

Oracle Projects APIs, Client Extensions, and Open Interfaces Reference

This manual gives detailed information about all public application programming
interfaces (APIs) that you can use to extend Oracle Projects functionality.

User Guides Related to This Product

Oracle Assets User Guide

In Oracle Assets, you can post capital project costs to become depreciable fixed
assets. Refer to this guide to learn how to query mass additions imported from Oracle
Projects to Oracle Assets and to review asset information. Use this manual when
you plan and define your chart of accounts, accounting period types and accounting
calendar, functional currency, and set of books. The manual also describes how to define
journal entry sources and categories so you can create journal entries for your general
ledger. If you use multiple currencies, use this manual when you define additional

xiii

rate types, and enter daily rates. This manual also includes complete information on
implementing Budgetary Control.

Oracle General Ledger User Guide

Use this manual when you plan and define your chart of accounts, accounting period
types and accounting calendar, functional currency, and set of books. The manual also
describes how to define journal entry sources and categories so you can create journal
entries for your general ledger. If you use multiple currencies, use this manual when you
define additional rate types, and enter daily rates. This manual also includes complete
information on implementing Budgetary Control.

Oracle HRMS Documentation Set

This set of guides explains how to define your employees, so you can give them
operating unit and job assignments. It also explains how to set up an organization
(operating unit). Even if you do not install Oracle HRMS, you can set up employees and
organizations using Oracle HRMS windows. Specifically, the following manuals will
help you set up employees and operating units:

• Using Oracle HRMS - The Fundamentals

This user guide explains how to set up and use enterprise modeling, organization
management, and cost analysis.

• Managing People Using Oracle HRMS

Use this guide to find out about entering employees.

Oracle Inventory User Guide

If you install Oracle Inventory, refer to this manual to learn how to define project-related
inventory transaction types and how to enter transactions in Oracle Inventory. This
manual also describes how to transfer transactions from Oracle Inventory to Oracle
General Ledger.

Oracle Payables User Guide

Refer to this manual to learn how to use Invoice Import to create invoices in Oracle
Payables from Oracle Projects expense reports data in the Oracle Payables interface
tables. This manual also explains how to define suppliers, and how to specify supplier
and employee numbering schemes for invoices created using Oracle Projects.

Oracle Project Manufacturing Implementation Manual

Oracle Project Manufacturing allows your company to associate manufacturing costs
and inventory to a specific project and task. Use this manual as your first source of
information if you are implementing Oracle Project Manufacturing.

Oracle Purchasing User Guide

If you install Oracle Purchasing, refer to this user guide to read about entering and
managing the requisitions and purchase orders that relate to your projects. This manual
also explains how to create purchase orders from project-related requisitions in the
AutoCreate Documents window.

xiv

Oracle Receivables User Guide

Use this manual to learn more about Oracle Receivables invoice processing and invoice
formatting, defining customers, importing transactions using AutoInvoice, and Defining
Automatic Accounting in Oracle Receivables.

Oracle Business Intelligence System Implementation Guide

This guide provides information about implementing Oracle Business Intelligence (BIS)
in your environment.

BIS 11i User Guide Online Help

This guide is provided as online help only from the BIS application and includes
information about intelligence reports, Discoverer workbooks, and the Performance
Management Framework.

Using Oracle Time Management

This guide provides information about capturing work patterns such as shift hours so
that this information can be used by other applications such as General Ledger.

Installation and System Administration

Oracle Applications Concepts

This guide provides an introduction to the concepts, features, technology
stack, architecture, and terminology for Oracle Applications Release 11i. It provides a
useful first book to read before installing Oracle Applications.

Installing Oracle Applications

This guide provides instructions for managing the installation of Oracle Applications
products. In Release 11i, much of the installation process is handled using Oracle Rapid
Install, which minimizes the time to install Oracle Applications and the technology
stack by automating many of the required steps. This guide contains instructions
for using Oracle Rapid Install and lists the tasks you need to perform to finish your
installation. You should use this guide in conjunction with individual product user’s
guides and implementation guides.

Upgrading Oracle Applications

Refer to this guide if you are upgrading your Oracle Applications Release 10.7 or
Release 11.0 products to Release 11i. This guide describes the upgrade process and
lists database and product-specific upgrade tasks. You must be either at Release 10.7
(NCA, SmartClient, or character mode) or Release 11.0, to upgrade to Release 11i. You
cannot upgrade to Release 11i directly from releases prior to 10.7.

Maintaining Oracle Applications

Use this guide to help you run the various AD utilities, such as
AutoUpgrade, AutoPatch, AD Administration, AD Controller, AD Relink, License
Manager, and others. It contains how-to steps, screenshots, and other information that
you need to run the AD utilities. This guide also provides information on maintaining
the Oracle Applications file system and database.

xv

Oracle Applications System Administrator’s Guide

This guide provides planning and reference information for the Oracle Applications
System Administrator. It contains information on how to define security, customize
menus and online help, and manage concurrent processing.

Oracle Alert User’s Guide

This guide explains how to define periodic and event alerts to monitor the status of
your Oracle Applications data.

Oracle Applications Developer’s Guide

This guide contains the coding standards followed by the Oracle Applications
development staff. It describes the Oracle Application Object Library components
needed to implement the Oracle Applications user interface described in the Oracle
Applications User Interface Standards for Forms-Based Products. It also provides information
to help you build your custom Oracle Forms Developer forms so that they integrate
with Oracle Applications.

Other Implementation Documentation

Oracle Applications Product Update Notes

Use this guide as a reference for upgrading an installation of Oracle Applications. It
provides a history of the changes to individual Oracle Applications products between
Release 11.0 and Release 11i. It includes new features, enhancements, and changes made
to database objects, profile options, and seed data for this interval.

Multiple Reporting Currencies in Oracle Applications

If you use the Multiple Reporting Currencies feature to record transactions in more than
one currency, use this manual before you implement Oracle Projects. This manual
details additional steps and setup considerations for implementing Oracle Projects with
Multiple Reporting Currencies.

Multiple Organizations in Oracle Applications

This guide describes how to set up and use Oracle Projects with Oracle Applications’
Multiple Organization support feature, so you can define and support different
organization structures when running a single installation of Oracle Projects.

Oracle Workflow Administrator’s Guide

This guide explains how to complete the setup steps necessary for any Oracle
Applications product that includes workflow-enabled processes, as well as how to
monitor the progress of runtime workflow processes.

Oracle Workflow Developer’s Guide

This guide explains how to define new workflow business processes and customize
existing Oracle Applications-embedded workflow processes. It also describes how to
define and customize business events and event subscriptions.

xvi

Oracle Workflow User’s Guide

This guide describes how Oracle Applications users can view and respond to workflow
notifications and monitor the progress of their workflow processes.

Oracle Workflow API Reference

This guide describes the APIs provided for developers and administrators to access
Oracle Workflow.

Oracle Applications Flexfields Guide

This guide provides flexfields planning, setup and reference information for the
Oracle Projects implementation team, as well as for users responsible for the ongoing
maintenance of Oracle Applications product data. This manual also provides
information on creating custom reports on flexfields data.

Oracle eTechnical Reference Manuals

Each eTechnical Reference Manual (eTRM) contains database diagrams and a detailed
description of database tables, forms, reports, and programs for a specific Oracle
Applications product. This information helps you convert data from your existing
applications and integrate Oracle Applications data with non-Oracle applications, and
write custom reports for Oracle Applications products. Oracle eTRM is available on
Oracle MetaLink.

Oracle Applications User Interface Standards for Forms-Based Products

This guide contains the user interface (UI) standards followed by the Oracle Applications
development staff. It describes the UI for the Oracle Applications products and tells you
how to apply this UI to the design of an application built by using Oracle Forms.

Oracle Manufacturing APIs and Open Interfaces Manual

This manual contains up-to-date information about integrating with other Oracle
Manufacturing applications and with your other systems. This documentation includes
APIs and open interfaces found in Oracle Manufacturing.

Oracle Order Management Suite APIs and Open Interfaces Manual

This manual contains up-to-date information about integrating with other Oracle
Manufacturing applications and with your other systems. This documentation includes
APIs and open interfaces found in Oracle Order Management Suite.

Oracle Applications Message Reference Manual

This manual describes all Oracle Applications messages. This manual is available in
HTML format on the documentation CD-ROM for Release 11i.

Training and Support

Training

Oracle offers a complete set of training courses to help you and your staff master
Oracle Projects and reach full productivity quickly. These courses are organized into
functional learning paths, so you take only those courses appropriate to your job or
area of responsibility.

xvii

You have a choice of educational environments. You can attend courses offered by
Oracle University at any of our many Education Centers, you can arrange for our
trainers to teach at your facility, or you can use Oracle Learning Network (OLN), Oracle
University’s online education utility. In addition, Oracle training professionals can tailor
standard courses or develop custom courses to meet your needs. For example, you may
want to use your organization structure,

Support

From on-site support to central support, our team of experienced professionals provides
the help and information you need to keep Oracle Projects working for you. This team
includes your Technical Representative, Account Manager, and Oracle’s large staff of
consultants and support specialists with expertise in your business area, managing an
Oracle server, and your hardware and software environment.

Do Not Use Database Tools to Modify Oracle Applications Data

Oracle STRONGLY RECOMMENDS that you never use SQL*Plus, Oracle Data Browser,
database triggers, or any other tool to modify Oracle Applications data unless otherwise
instructed.

Oracle provides powerful tools you can use to create, store, change, retrieve, and
maintain information in an Oracle database. But if you use Oracle tools such as SQL*Plus
to modify Oracle Applications data, you risk destroying the integrity of your data and
you lose the ability to audit changes to your data.

Because Oracle Applications tables are interrelated, any change you make using an
Oracle Applications form can update many tables at once. But when you modify Oracle
Applications data using anything other than Oracle Applications, you may change a row
in one table without making corresponding changes in related tables. If your tables get
out of synchronization with each other, you risk retrieving erroneous information and
you risk unpredictable results throughout Oracle Applications.

When you use Oracle Applications to modify your data, Oracle Applications
automatically checks that your changes are valid. Oracle Applications also keeps track of
who changes information. If you enter information into database tables using database
tools, you may store invalid information. You also lose the ability to track who has
changed your information because SQL*Plus and other database tools do not keep a
record of changes.

xviii

1
Overview of Project Costing

This chapter gives you an overview of project costing in Oracle Projects.

This chapter covers the following topics:

• Overview of Costing

• Calculating Costs

• Distributing Labor Costs

Overview of Costing

Costing is the processing of expenditures to calculate their cost to each project and
determine the GL accounts to which the costs will be posted. Costing is performed
for the following types of expenditures:

• Pre-approved expenditures. See: Overview of Expenditures, page 2- 1 .

• Labor

• Expense Reports

• Usages

• Miscellaneous Transactions

• Burden transactions. See: Overview of Burdening, page 3- 1 .

• Expenditures submitted from Oracle Internet Expenses. See: Integrating Expense

Reports with Oracle Payables and Oracle Internet Expenses, page 7- 1 .

• Supplier Invoices from Oracle Payables. See: Integrating with Oracle Purchasing

and Oracle Payables, page 7-16.

• Imported expenditures. See: Transaction Import, Oracle Projects APIs, Client

Extensions, and Open Interfaces Reference.

• Adjusted expenditures in Oracle Projects that need re-costing. See: Adjusting

Expenditures, page 2-44.

Related Topics

Costing in Oracle Projects, page 1- 2

Costing Processes, page 1- 3

Calculating Costs, page 1- 5

Overview of Project Costing

1-1

Distributing Labor Costs, page 1- 6

Costing in Oracle Projects

The following illustration shows how costing is performed in Oracle Projects.

Costing in Oracle Projects

As shown in the illustration Costing in Oracle Projects, page 1- 2 , costing includes the
following major steps:

1. Enter and approve expenditures through the Oracle Projects user interface, or import

transactions (for example, through Transaction Import).

1-2 Oracle Project Costing User Guide

2. Distribute costs and perform accounting. The costing process performs the following

tasks on uncosted expenditures:

• Calculates raw cost (by multiplying quantity times rate) in transaction currency

• Calculates burdened cost.

• Calls the following client extensions. See: Client Extensions, Oracle Projects

APIs, Client Extensions, and Open Interfaces Reference.

• Overtime Calculation

• Labor Costing

• Create Related Items

• Converts all transaction currency amounts to functional and project cost

currency amounts

• Performs accounting to determine the account numbers to post to in General

Ledger.

3.

Interface costs to other applications

• You interface expense reports to Oracle Payables via the Oracle Payables

Interface. After you transfer expense reports to the Payables Invoice Interface
tables, you submit the Payables Invoice Import process to create an invoice from
the expense report.

• You interface all other cost expenditures to General Ledger via the General
Ledger Interface if the expenditures have not previously been accounted
for in other applications. These costs include labor, usage, miscellaneous
transactions, burden transactions, work-in-process (WIP) and inventory. The
General Ledger Journal Import program takes the summary interface
information stored in the General Ledger interface table and automatically
creates cost and revenue journal entries for posting in General Ledger.

4. Tieback costs from Oracle Payables and General Ledger to verify your Oracle

Projects data.

Costing Processes

The following illustration shows the flow of costing processes in Oracle Projects.

Overview of Project Costing

1-3

Costing Processes

As shown in the illustration Costing Processes, page 1- 4 , create and distribution
processes perform the following tasks:

• Calculate raw cost (quantity rate)

• Calculate burden and burdened cost

• Create and distribute raw cost distribution lines

• Create and distribute burden and burdened cost distribution lines

• Determine accounting

Interface and tieback processes perform the following tasks:

• Accumulate raw and burdened costs in project accumulators

• Determine accounting

• Interface raw and burdened cost distribution lines to General Ledger or Accounts

Payable

• Verify costs distributed to General Ledger and Accounts Payable

Note: If you are not performing burdening, you can skip the
processes that create and distribute burden and burdened cost.

1-4 Oracle Project Costing User Guide

Calculating Costs

This section briefly describes how Oracle Projects calculates costs for expenditures. For
more detailed information about the costing process, refer to the labor costing example
in this chapter. See: Distributing Labor Costs, page 1- 6 .

Each transaction has two cost amounts when processed, raw and burdened. Oracle
Projects calculates these amounts for each detail transaction when you distribute costs
using any of the following processes:

• Distribute Labor Costs

• Distribute Expense Report Costs

• Distribute Usage and Miscellaneous Costs

• Distribute Supplier Invoice Adjustment Costs

The raw cost is the actual cost of the work performed, and the burden cost is the indirect
cost of work performed. The burden costs are created to apply overhead costs to
projects to provide an accurate total cost figure. The burdened cost is the total cost of
the expenditure, or the sum of raw cost and burden cost. Oracle Projects calculates the
burden cost using the raw cost and a burden multiplier.

Calculating Labor Cost

Oracle Projects calculates cost for labor transactions using quantity and rates as
follows:

• Raw cost is the result of multiplying hours by a rate.

• Burden cost is the result of multiplying raw cost by a burden multiplier.

• Burdened cost is the sum of raw cost and burden cost.

Note: You can define a unique labor costing algorithm using the
Labor Costing Extensions. See: Labor Costing Extensions, Oracle
Projects APIs, Client Extensions, and Open Interfaces Reference.

Related Topics

Distributing Labor Costs, page 1- 6

Overview of Expenditures, page 2- 1

Overview of Burdening, page 3- 1

Calculating Cost for Expense Reports, Usages, and Miscellaneous Transactions

Oracle Projects calculates the cost for expense reports, usages, and miscellaneous
transactions as follows:

• Raw cost is equal to quantity (if quantity is in currency, for example, a currency
amount), or alternatively, raw cost is the result of multiplying hours by a rate (if
quantity is not in currency).

• cost rates by expenditure type, or

• cost rates by non-labor resource and owning organization for usages (optional);

overrides expenditure type cost rate

• Burden cost is the result of multiplying raw cost by a burden multiplier.

Overview of Project Costing

1-5

• Burdened cost is the sum of raw cost and burden cost.

Related Topics

Overview of Expenditures, page 2- 1

Overview of Burdening, page 3- 1

Integrating Expense Reports with Oracle Payables and Oracle Internet Expenses, page
7- 1

Using Rates for Costing, Oracle Projects Fundamentals

Calculating Burden Cost

Oracle Projects calculates burden cost transactions, which represent only the burden or
overhead cost, as follows:

• Quantity is zero.

• Raw cost is zero.

• Burden cost is the calculated burden cost amount.

• Burdened cost is equal to burden cost.

Related Topics

Overview of Burdening, page 3- 1

Calculating Cost for Supplier Invoices

Oracle Projects calculates the raw cost for supplier invoices using the cost amount
entered as the invoice amount for the invoice in Oracle Payables.

• Raw cost is equal to the supplier invoice amount from Oracle Payables.

• Burden cost is the result of multiplying raw cost by a burden multiplier.

• Burdened cost is the sum of raw cost and burden cost.

Oracle Projects calculates the burdened cost for supplier invoice transactions during
the following processes:

• PRC: Interface Supplier Costs

• PRC: Distribute Supplier Invoice Adjustment Costs

Related Topics

Overview of Burdening, page 3- 1

Integrating with Oracle Purchasing and Oracle Payables, page 7-16

Distributing Labor Costs

This section illustrates the costing process using Labor Costing as an example.

Oracle Projects allows you to enter detail labor transactions charged to your projects so
that you can monitor labor work performed. Oracle Projects costs the items to compute
the labor costs for your project, and determines the GL accounts to charge.

1-6 Oracle Project Costing User Guide

The following illustration shows the steps in the PRC: Distribute Labor Costs process:

Steps in the PRC: Distribute Labor Costs Process

The PRC: Distribute Labor Costs process handles labor items in the following order:

• Selects eligible expenditure items, based on the parameters you entered for

project, employee, and week ending date.

• Costs the straight time items.

• Calls the Overtime Calculation program, if it is enabled.

• Costs overtime items, including overtime items created by the Overtime Calculation

program.

Note: If your transactions are not costing properly, you can view
rejection reasons in the Expenditure Items window. From the
Folder menu, choose the Show Field option to display all cost
distribution rejections.

Related Topics

Distribute Labor Costs Process, Oracle Projects Fundamenatals

Labor Costing Definitions, Oracle Projects Implementation Guide

Overview of Project Costing

1-7

Rate Schedule Definition, Oracle Projects Implementation Guide

Using Rates for Costing, Oracle Projects Fundamentals

Selecting Expenditure Items

The Distribute Labor Costs program first selects all expenditure items that are eligible for
costing. To be eligible for costing, an expenditure item must meet the following criteria:

• Classified with an expenditure type having the Straight Time or Overtime

expenditure type class

• Included in the specified project for straight time items (if you specify a project)

• For the specified employee (if you specify an employee)

• In a week ending on or before the end date (if you specify a week ending date)

• In a released pre-approved timecard batch

• Not already cost distributed (new items or items marked for adjustment)

Expenditure items selected are processed in sets according to the Expenditures Per Set
profile option For more information, see: Profile Options in Oracle Projects, Oracle
Projects Implementation Guide.

Processing Straight Time

Distribute Labor Costs performs three steps to process straight time:

• Calculate costs

• Run AutoAccounting

• Create cost distribution lines

Important: Throughout this document, the term resource applies equally
to employees and non-employees (contingent workers) when used in
discussions about features that support capturing, processing, and
reporting time and costs that pertain to people. Similarly, the term
employee is also meant to apply to contingent workers. For more
information about contingent workers, see: Support for Contingent
Workers, Oracle Projects Fundamentals.

Calculating Costs

Oracle Projects calculates straight time cost (raw cost) for expenditure items by
multiplying hours worked by an employee’s labor cost rate. This calculation is
represented in the following formula:

Straight Time Cost = (Hours Worked x Employee’s Labor Cost Rate)

Distribute Labor Costs uses the labor cost rate that is in effect for an employee as of the
week ending date for each selected expenditure item. This amount can be overridden by
the Labor Costing Extension to handle unique labor costing rules.

Note: If a timecard for a contingent worker is associated with a purchase
order, then the labor cost rates for the contingent worker are defined
on the purchase order.

1-8 Oracle Project Costing User Guide

If an employee’s labor cost is burdened, Oracle Projects calculates the burdened cost by
multiplying straight time cost times a factor equal to one plus the burden multiplier. This
calculation is represented in the following formula:

Burdened Cost = (Straight Time Cost x (1 + Burden Multiplier))

To determine if a labor cost is burdened, Oracle Projects checks the project type of the
project to which an expenditure item is charged. The burden multiplier is determined
from the burden schedule (or burden schedule override) assigned to the project or
task. In addition, Oracle Projects compares the expenditure item date to the effective
dates of the burden schedule to determine the burden multiplier to use.

Running AutoAccounting

After the process calculates cost for each selected expenditure item, it runs
AutoAccounting to determine account codes for each cost distribution line that it will
create.

If an organization distribution override exists, the destination organization of the
override supersedes the actual expenditure organization of affected items.

When you run the cost distribution programs for labor, expense reports, or usages and
miscellaneous transactions, Oracle Projects redirects the Expenditure Organization to
the Override To Organization if you have specified any of the following organization
distribution overrides for the organization:

• Incurred by Employee and Expenditure Category

• Incurred by Employee

• Expenditure Organization and Expenditure Category

• Expenditure Category

If you do not specify any of these overrides, Oracle Projects uses the Incurred by
Organization or the Expenditure Organization.

Creating Cost Distribution Lines

After the Distribute Labor Costs process runs AutoAccounting, it creates cost distribution
lines. Each item originally has one distribution line for raw cost. If an item is re-costed
and the cost rate or account coding changes, Distribute Labor Costs creates a reversing
cost distribution line and a new line for the updated cost or account coding.

Related Topics

Overview of Burdening, page 3- 1

Labor Costing Extensions, Oracle Projects APIs, Client Extensions, and Open Interfaces
Reference

Accounting Transactions for Cost, Oracle Projects Fundamentals

Creating Overtime

You can use Oracle Projects to track the cost of overtime and other premium
compensation, allowing you to determine the true cost of labor.

Overview of Project Costing

1-9

When an employee works overtime, in addition to charging the total hours an employee
worked to the project(s) on which the employee worked, you calculate and charge the
overtime hours and costs. Therefore, the employee’s pay includes two components:

• Straight time cost

• Overtime or premium cost

Note: If a timecard for a contingent worker is associated with a purchase
order, then the overtime price differential multipliers for the contingent
worker can be defined on the purchase order.

Tracking Overtime

When you enter timecards in Oracle Projects, you charge the total hours an employee
worked to the project(s) on which the employee worked.

You can track overtime premium costs in Oracle Projects in three primary ways:

• Charge to an indirect project.

• Charge to a project on which overtime was worked.

• Charge to a project on which overtime was worked and track premium amounts

separately.

Oracle Projects creates overtime when you enter it manually or when the Overtime
Calculation program creates it automatically. If you enter overtime manually, the
Distribute Labor Costs program does not create overtime, and instead proceeds directly
to calculating overtime cost. If you enable the Overtime Calculation program, then the
Distribute Labor Costs process calls the program to create overtime automatically.

Related Topics

Distribute Labor Costs, Oracle Projects Fundamentals

Implementing Overtime Processing, Oracle Projects Implementation Guide

Overtime Calculation Extension, Oracle Projects APIs, Client Extensions, and Open
Interfaces Reference

Processing Overtime

Distribute Labor Costs performs three steps to process overtime:

1. Calculate costs

2. Run AutoAccounting

3. Create cost distribution lines

Calculating Overtime Cost

Oracle Projects calculates premium overtime cost (raw cost) for overtime items by
multiplying an employee’s labor cost rate by a labor cost multiplier that corresponds to
the type of overtime worked. This calculation is represented in the following formula:

Premium Overtime Cost = (Hours Worked x Employee’s Labor Cost Rate) x Labor
Cost Multiplier

Overtime may or may not be burdened, depending on your burdening setup.

1-10 Oracle Project Costing User Guide

Running AutoAccounting

After the process calculates cost for each selected expenditure item, it runs
AutoAccounting to determine account codes for each cost distribution line that the
process creates.

If an organization distribution override exists, then the destination organization of the
override supersedes the actual expenditure organization of affected items.

Creating Cost Distribution Lines

After the process runs AutoAccounting, it creates cost distribution lines. Each item
originally has one distribution line for raw cost. If an item is re-costed and the cost rate
or account coding changes, Distribute Labor Cost creates a reversing cost distribution
line and a new line for the updated cost or account coding.

Generating Labor Output Reports

The Distribute Labor Costs process generates output reports that list detail items that
were processed and exception items.

Related Topics

Distribute Labor Costs Process, Oracle Projects Fundamentals

Calculating and Reporting Utilization

The utilization functionality of Oracle Project Costing and Oracle Project Resource
Management enables you to generate and report on your resource’s actual and
scheduled utilization. Using Oracle Project Costing, you can report on your
resource’s actual resource utilization based on actual hours from timecards. For more
information, see: Utilization, Oracle Project Fundamentals.

Overview of Project Costing

1-11

2
Expenditures

This chapter describes how to enter and manage expenditures using Oracle Projects.

This chapter covers the following topics:

• Overview of Expenditures

• Processing Pre-Approved Expenditures

• Controlling Expenditures

• Viewing Expenditures

• Adjusting Expenditures

Overview of Expenditures

An expenditure is a group of expenditure items, or transactions, incurred by an
employee or an organization for an expenditure period. You charge expenditures to a
project to record actual work performed or cost incurred, and you charge commitments
to future, committed costs you expect to incur.

You must charge all actual expenditure items and future commitments to a project and
task. Examples of actual expenditures are timecards, expense reports, usage logs, and
supplier invoices. Examples of commitments are requisitions and purchase orders.

The following are examples of expenditures and commitments:

• You have worked eight hours on Monday, June 6 for project A, task 1 doing

Professional work (expenditure)

• You travelled twenty miles on Tuesday, June 7 for project X, task 1 using your own

vehicle (expenditure)

• You made ten copies of a blueprint on Thursday, June 9 for project Y, task 1 using

copier number 1243 (expenditure)

• You issued a purchase order for 200 pounds of cement on Friday, June 10 for project

Z, task 2.3 (commitment)

You associate each expenditure item with an expenditure type class, (such as Straight
Time or Supplier Invoice). The expenditure type class tells Oracle Projects how to process
the expenditure item. For more information, see: Expenditure Type Classes, Oracle
Projects Implementation Guide.

Expenditures

2-1

Expenditure Classifications

Expenditure types (such as Administrative, Hotel, or Overtime) classify the type of cost
incurred. You can categorize costs and revenues by grouping the expenditure types
into expenditure categories such as Materials and Labor. You define all expenditure
types, expenditure categories, and revenue categories during implementation.

Expenditure Amounts

During processing, the system associates each expenditure item with a unit quantity and
two cost amounts, raw and burden cost, when processed. The raw cost is the actual cost
of the work performed; the burden cost is the indirect cost of the work performed. For
example, the raw cost could be the hours multiplied by the hourly cost rate, and the
burden could be the cost of the office space or benefits. The total burdened cost is the
raw cost plus the burden cost.

Related Topics

Using Rates for Costing, Oracle Projects Fundamentals

Expenditure Entry Methods

You can create expenditure items in Oracle Projects to record actual work performed or
costs incurred against a project in one of the following ways:

• Enter pre-approved expenditure batches. See: Processing Pre-Approved

Expenditures, page 2-10.

• Upload pre-approved expenditure batches from Microsoft Excel. See: Uploading

Expenditures from Microsoft Excel, page 2-19.

• Enter expenditures in other Oracle Applications, such as Oracle Payables and

Oracle Inventory, and import them into Oracle Projects. See: Overview of Oracle
Project Costing Integration, page 7- 1 .

• Import transactions from external sources. See: Transaction Import, Oracle Projects

APIs, Client Extensions, and Open Interfaces Reference.

Expenditure Item Validation

When you enter expenditure items, you are charging hours, expenses, or non-labor
resources to a project and a task. Oracle Projects validates expenditure items against
predefined criteria and any transaction controls and transaction control client extensions
that you set up during the implementation.

Standard Validation Process

The standard validation process performs the following checks:

• Project

• Expenditure item falls within project dates

• Project status allows transactions

• Transaction controls and transaction control extensions allow charges of this type

• Project allows cross-charges from the user’s operating unit in a

multi-organization environment

2-2 Oracle Project Costing User Guide

• Task

• Expenditure item falls within task dates

• Task is a lowest task and chargeable

• Transaction controls and transaction control extensions allow charges of this type

• Expenditure type

• Expenditure type is active

• Is valid for multiple currencies

• Employee

• Employee is active

• Existing expenditure item (for adjustments only)

• Matching expenditure item exists (unless you enter an unmatched, negative

transaction)

Note: Oracle Projects validates pre-approved expenditure
batches as you enter expenditure item details. Expenditures
created using external cost collection systems are validated
during the Submit and Transaction Import processes, but before
Oracle Projects creates an expenditure.

Funds Checks for Transactions

When a transaction is charged to a project, funds check processes are activated in both
General Ledger and Oracle Projects. Funds checks are activated for new transactions
and for adjusted transactions.

You can review Oracle Projects funds check results online. The system displays results
for transactions that pass a funds check and transactions that fail a funds check.

Note: You must baseline the budget before transactions can be funds
checked by the funds check processes.

Related Topics

Funds Check Activation in Oracle Purchasing and Oracle Payables, page 7-23

Funds Check Activation in Oracle Projects, Oracle Project Management User Guide

Using Budgetary Controls, Oracle Project Management User Guide

Expenditure Rejection Reasons

Possible reasons for expenditure transaction rejection are listed in the following table. If
you receive a rejection reason not included in the table, check with your implementation
team for rejection reasons defined in the transaction control extensions. If you cannot
access a window mentioned in the table, contact the key member for the project for
assistance.

Expenditures

2-3

Rejection Reason (Error
Lookup Code)

Burdened cost is not valid for
the given system linkage

(INVALID_BURDENED_

AMOUNT)

Troubleshooting Tips

Expenditure

All

A transaction with an
expenditure type class of
Burden Transactions should
have a burden cost of NULL.
For other expenditure type
classes, the burden cost should
equal zero if the transaction
source or project does not
allow burdening.

CCID for credit is NULL
(INVALID_CR_CCID)

CCID for debit is NULL
(INVALID_DR_CCID)

The code combination ID for
the credit account cannot be
NULL for transactions that
have been accounted for in an
external system.

The code combination ID for
the debit account cannot be
NULL for transactions that
have been accounted for in an
external system.

GL accounted transactions

GL accounted transactions

All

All

All

Cannot lock original item for
reversal

(CANNOT_LOCK_

ORIG_ITEM)

Another user or a process
is currently accessing the
original item to be adjusted.
Try to revise the expenditure
item later.

Cross charge validation failed

(CROSS_CHARGE_

PROJECT_INVALID)

Different system linkage
(DIFF_SYS_LINKAGE)

You will get this message
only if you have implemented
multiple organization support
and are using Transaction
Import to charge expenditure
items to a project owned by an
operating unit that does not
share your operating unit’s set
of books, PA period type, and
business group. Revise the
expenditure item by entering a
project owned by an operating
unit to which you can charge.

During Transaction Import,
Oracle Projects verifies that
the expenditure type class
of the transaction matches
the expenditure type class of
the expenditure type. You
can either associate the
expenditure type class with
the expenditure type using the
Expenditure Types window, or
you can change either the
expenditure type or the
expenditure type class on the
transaction so they form a
valid combination.

2-4 Oracle Project Costing User Guide

Rejection Reason (Error
Lookup Code)

Duplicate item (DUPLICATE_
ITEM)

Troubleshooting Tips

Expenditure

All

An expenditure item with
the same transaction source
and original system reference
already exists. Change
the transaction source or
original system reference of
the expenditure item to be
imported.

Employee is mandatory

(EMP_MAND_FOR_

ER/TIME)

Employee or organization is
mandatory

(EMP_OR_ORG_MAND

Expenditure item cannot be
charged to a Closed project
(PA_EX_PROJECT_

CLOSED)

Expenditure item date is after
the expenditure ending date

(EI_DATE_AFTER_END_
DATE)

Expenditure item date is not
within the active dates of the
project (PA_EX_PROJECT_
DATE)

Expenditure item date is not
within the active dates of the
task (PA_EXP_TASK_EFF)

Expenditure item date is not
within the expenditure week
(ITEM_NOT_IN_WEEK)

Enter information into the
employee number field.

Timecards and expense reports

All except timecards and
expense reports

All

All

All

All

Timecards

Enter either the employee
name and number or
expenditure organization
in the appropriate expenditure
field.

Project status does not allow
transactions to be charged to
this project. Change the status
of the project or charge the
expenditure item to another
project.

The expenditure item date is
after the expenditure ending
date. Verify that both the
expenditure item and the
expenditure dates are correct
and change, if necessary.

Change the expenditure
item date or the project’s
active dates, or charge the
expenditure item to another
project.

Change the expenditure item
date or the task’s active dates,
or charge the expenditure item
to another task.

Verify that the expenditure
item date and the expenditure
date are both correct and
change, if necessary. You can
also create a new expenditure
for the expenditure item.

Expenditure organization is
not active (PA_EXP_ORG_
NOT_ACTIVE)

The expenditure organization
is not active or is not within
the current expenditure
organization hierarchy.

All

Expenditures

2-5

Rejection Reason (Error
Lookup Code)

Expenditure type/
expenditure type class inactive
(ETYPE_SLINK_INACTIVE)

Expenditure type inactive
(EXP_TYPE_INACTIVE)

GL date is NULL (INVALID_
GL_DATE)

Troubleshooting Tips

Expenditure

The combination of the
expenditure type and
expenditure type class is
inactive as of the expenditure
item date. Refer to PA_EX
PEND_TYP_SYS_LINKS
for valid expenditure type/
expenditure type class
combinations.

The expenditure type has been
defined, but it is either not
yet effective or has already
expired as of the expenditure
item date. Refer to the
Expenditure Types window
to view all valid expenditure
types and their effective dates
or to change the expenditure
type’s effective dates.

A transaction that has already
been accounted for in an
external system must have a
GL date.

All

All

GL accounted transactions

Invalid burden transaction (
INVALID_BURDEN_TRANS)

Raw cost and quantity must
equal zero or NULL for burden
transactions.

Burden transactions

Invalid employee (INVALID_
EMPLOYEE)

Invalid ending date (INVAL
ID_END_DATE)

Invalid expenditure type
(INVALID_EXP_TYPE)

Invalid expenditure type
class (INVALID_EXP_TYPE_
CLASS)

Oracle Projects does not
recognize the employee
number. Verify that you
have entered the information
correctly or add a new
employee.

The expenditure ending date
does not fall on the day of
the week defined as your
expenditure cycle end day.
Refer to the Implementation
Options window (Costing) for
the valid expenditure cycle
start day.

The expenditure type does not
exist. Refer to the Expenditure
Types window for a list of all
valid expenditure types or to
create a new expenditure type.

The expenditure type
class of the transaction
is invalid. Refer to PA_
SYSTEM_LINKAGES for
valid expenditure type classes.

All

All

All

All

2-6 Oracle Project Costing User Guide

Rejection Reason (Error
Lookup Code)

Invalid expenditure type/
system linkage combination
(INVALID_ETYPE_SLINK)

Invalid non-labor resource
(INVALID_NL_RSRC)

Invalid non-labor resource
organization (INVALID_NL_
RSRC_ORG)

Invalid organization (INVAL
ID_ORGANIZATION)

Invalid project (INVALID_
PROJECT)

Troubleshooting Tips

Expenditure

All

The combination of the
expenditure type and
expenditure type class is
invalid. Refer to PA_EX
PEND_TYP_SYS_LINKS
for valid expenditure type/
expenditure type class
combinations.

Usage logs

Usage logs

All

All

The non-labor resource
does not exist. Refer to the
Non-Labor Resources window
for a list of all valid non-labor
resources or to create a new
non-labor resource.

The non-labor resource
organization does not exist.
Refer to the Non-Labor
Resources window for a list
of all valid organizations for a
particular non-labor resource
or to assign a new organization
to a non-labor resource.

The expenditure organization
does not exist. Refer to the
expenditure organization
hierarchy set up in Oracle
Projects to determine all
organizations defined as valid
expenditure organizations.

The project number does not
exist. Refer to the Projects
Summary window for a list
of all valid projects or to the
Projects, Templates Summary
window to create a new
project by copying an existing
project or template.

Invalid project type (INVAL
ID_PROJECT_TYPE)

The project type for the given
project is invalid.

All

Invalid task (INVALID_ TASK) The task number does not

All

exist for the project, or the task
is not a lowest task. Open your
project and choose the Tasks
option to view all valid tasks
or to create a new lowest task.

Expenditures

2-7

Rejection Reason (Error
Lookup Code)

Invalid transaction source
(INVALID_TRX_SOURCE)

Troubleshooting Tips

Expenditure

All

Oracle Projects does not
recognize the transaction
source. Refer to the
Transaction Sources window
for a list of valid transaction
sources or to create a new
transaction source.

No open or future PA period
for the expenditure item and
GL dates (INVALID_PA_
DATE)

There is no open or future
PA period for the given
expenditure item and GL
dates.

GL accounted transactions

Non-labor resource
expenditure type different
(NL_EXP_TYPE_DIFF)

Non-labor resource inactive
(NL_RSRC_INACTIVE)

Usage logs

Usage logs

The non-labor resource is
not associated with the
expenditure type. Refer to
the Non-Labor Resources
window for a listing of all
valid non-labor resources
and their expenditure types
or to create a new non-labor
resource.

The non-labor resource has
been defined, but it is either
not yet effective or has already
expired as of the expenditure
item date. Refer to the
Non-Labor Resources window
for a list of valid non-labor
resources and their effective
dates or to change the effective
dates.

Non-labor resource
mandatory for usages (NL_
RSRC_MAND_

FOR_USAGES)

A non-labor resource has
not been specified. Enter the
non-labor resource name for
the rejected expenditure item
in your usage log.

Non-labor resource owning
organization mandatory for
usages (NL_RSRC_ORG_

MAND_FOR_USAGES)

A non-labor resource
organization has not
been specified. Enter the
appropriate organization
name.

Usage logs

Usage logs

No assignment (NO_ASS
IGNMENT)

All

The employee does not have
an active HR assignment to
a specific organization and
job as of the expenditure item
date. Verify the expenditure
item date and the employee
assignment in Oracle Human
Resources and make change, if
necessary.

2-8 Oracle Project Costing User Guide

Rejection Reason (Error
Lookup Code)

No matching item (NO_
MATCHING_ITEM)

Troubleshooting Tips

Expenditure

Adjusting transactions

If the transaction is an
adjustment with a negative
quantity, and the unmatched
negative flag is not set to
Yes, an original, approved,
unreversed expenditure item
matching the transaction’s
employee/organization,
item date, expenditure
type, project, task, reversing
quantity, reversing cost (if
loading costed items via
Transaction Import), and non-
labor resource and non-labor
organization (for usages) must
exist. Also, the matching
expenditure item must have
been originally loaded from
the same transaction source. If
more than one item matches
the original item, Oracle
Projects uses the first one that
was created.

No raw cost (NO_RAW_
COST)

Transaction currency raw
cost amount is missing.
Expenditure items with a
costed transaction source must
include this information.

All

Organization does not own
the non-labor resource (ORG_
NOT_OWNER_

OF_NL_RSRC)

Project is not chargeable
(PA_PROJECT_NOT_VALID)

The non-labor resource has not
been assigned to the non-labor
resource organization as of the
expenditure item date. Refer
to the Non-Labor Resources
window for a list of all
organizations associated with
the resource or to associate
a new organization with the
resource.

The project is a template; has
a transaction control that does
not allow charges; does not
share a business group, set
of books, and PA period type
with the user’s operating unit;
or the project status does not
allow new transactions.

Project does not allow
burdening or burden
transactions (PROJ_
NOTALLOW_BURDEN)

Burden transactions and
transactions with burden
amounts are not allowed for
this project.

Usage logs

All

All

Expenditures

2-9

Rejection Reason (Error
Lookup Code)

Project/Task-level
expenditure transaction
control violated (PA_EXP_PJ/
TASK_TC)

Project/Task validation error
(PA_EXP_INV_PJTK)

The task is not chargeable
(PA_EXP_TASK_STATUS)

Transaction source does not
allow burdening or burden
transactions (TRXSRC_
NOTALLOW_BURDEN)

Transaction source inactive
(TRX_SOURCE_INACTIVE)

Troubleshooting Tips

Expenditure

All

All

All

All

All

The transaction violates the
project level or task level
transaction controls defined
for the project. Refer to the
Transaction Controls window
for a list of the transaction
controls on the project or task
or to change the transaction
controls. You can also charge
the expenditure item to
another project or task.

The project or task does not
exist, or the task does not
belong to the project. Change
the expenditure item’s project
or task.

The task’s Allow Charges flag
has not been enabled. Enable
this flag from the task’s Task
Details window or charge the
item to another task.

Burden transactions and
transactions with burden
amounts are not allowed for
transactions you import from
this transaction source.

The transaction source has
been defined, but either
is not yet effective or has
already expired as of the
expenditure item date. Refer
to the Transaction Sources
window for a list of all valid
transaction sources and their
effective dates or to change the
effective dates.

Processing Pre-Approved Expenditures

Pre-approved expenditures include the following items:

• timecards

• expense reports

• usage logs

• miscellaneous transactions

• burden transactions

• inventory transactions

• work in process transactions

2-10 Oracle Project Costing User Guide

These entries are generally completed on paper and approved by a supervisor, then
entered into Oracle Projects.

Note: Transactions with an expenditure type class of Work in Process or
Inventory are usually imported from a manufacturing system. Related
burden transactions are usually generated and imported via
Transaction Import. See: Transaction Import, Oracle Projects APIs, Client
Extensions, and Open Interfaces Reference.

You enter pre-approved expenditures into Oracle Projects in a batch, submit them for
review, and then release them for cost distribution.

The following illustration shows the steps for entering pre-approved expenditures
into Oracle Projects.

Pre-Approved Expenditure Flow

Expenditures

2-11

Entering Pre-Approved Expenditure Batches

Enter pre-approved expenditures, such as timecards, expense reports, or usage logs, in
batches. If you enter expenditures in a batch, Oracle Projects processes them as a
group. In addition, when you release the batch for cost distribution, Oracle Projects
releases all expenditures in the batch simultaneously.

Batch entry promotes accuracy and efficiency. You can use batches to:

• Reduce data entry. You can create a new timecard batch by copying any previously

created batch.

• Verify accuracy by tracking variances between actual and entered totals.

• Easily locate a group of expenditures to correct, submit for review, or release for

cost distribution.

When you enter pre-approved expenditures, you first create a new batch, then enter
the expenditures in the batch and their associated expenditure items. When you have
entered all expenditures and expenditure items, you can submit the contents of the
batch. Typically, your supervisor reviews your submitted batches and releases them for
cost distribution.

Note: Your implementation team can decide to allow the same person
or job responsibility to enter, submit, and release pre-approved
expenditures. For more information, see: Security in Oracle
Projects, Oracle Projects Fundamentals, and Project and Organization
Security, Oracle Projects Implementation Guide.

Statuses for Pre-Approved Expenditure Batches

Pre-approved expenditure batches can have one of the following statuses:

Working

The expenditure batch is not ready for review. You can
enter timecards, expense reports, usages, miscellaneous
transactions, burden transactions, inventory transactions, or
work-in-process transactions and modify their expenditures
and expenditure items.

2-12 Oracle Project Costing User Guide

Submitted

Released

The batch is awaiting review. You can still retrieve the batch
if you need to make corrections.

The expenditure batch has been released for cost
distribution. You can reverse incorrectly entered
expenditure items within the batch. See: Correcting
Expenditures Batches, page 2-23.

Note: You can choose Unreleased from the Status poplist in the Find
Expenditure Batches window to retrieve both Working and Submitted
expenditure batches.

Entering Transactions for Future-Dated Employees

You cannot enter actual project transactions for future-dated employees until they
become active employees. An employee is considered active when his or her start date is
equal to or earlier than the current date.

However, if an expenditure batch is dated in the future, you can enter transactions for
future-dated employees who are active as of the transaction dates.

Creating Automatically Reversing Expenditure Batches

You can create automatically reversing expenditure batches to record cost accruals in
Oracle Projects. Frequently, items and services are received in one accounting period and
invoiced in another. You can use automatically reversing expenditure batches to accrue
cost in the period in which it is incurred. When you receive and enter the invoice, the
accrual is reversed and actual cost is recorded.

To enter an automatically reversing batch, you must use a miscellaneous class. When
the batch is released, Oracle Projects creates reversing entries that are accounted in
the next General Ledger period.

Defining Accounting Rules for Cost Accruals

When you use automatically reversing expenditure batches to enter cost accruals in
Projects, you can apply unique accounting rules to the accrual transactions by following
these steps:

1. Define a new expenditure category for accruals.

2. Define a new expenditure type for each type of accrual you plan to enter. For

example, to accrue labor and supplier costs, define two expenditure types called
Labor Accrual and Supplier Cost Accrual.

3. Assign the new expenditure types to the Miscellaneous Transaction expenditure

type class.

4. Modify the AutoAccounting rules to generate accrual accounts for transactions

charged to the accrual expenditure types.

For more information on defining AutoAccounting rules, see: Defining
AutoAccounting Rules, Oracle Projects Implementation Guide.

Creating a Pre-Approved Expenditure Batch

Sort paper expenditure reports into batches containing the same Expenditure
Ending date and Expenditure Type Class (Straight Time, Overtime, Expense
Reports, Usages, Supplier Invoices, Miscellaneous Transactions, or Burden Transactions).

Expenditures

2-13

Tip: If you integrate with Oracle Manufacturing or Oracle Inventory, use
function security to prevent users from entering pre-approved batch
items with an expenditure type class of Inventory or Work in Process.

To create a new batch:

1. Navigate to the Expenditure Batches window.

2. Batch. Enter a unique Batch name to identify this set of expenditures.

Tip: Choose a unique, identifiable, and memorable batch name. For
example, a timecard batch name might include your organization
code, the letter T to indicate Timecards, and the week ending date.

3. Ending Date. Enter the expenditure Ending Date for the batch. If you enter a date

that is not the last day of an expenditure week, the system automatically updates the
date to the next valid week ending date.

4. Description. Optionally enter a Description of the batch, or leave the field blank to

use the name of the expenditure type class.

5. Class. Choose the expenditure type class for this batch.

6. Reverse Expenditures In a Future Period. Optionally, check this check box to

automatically reverse the batch.

See: Creating Automatically Reversing Expenditure Batches, page 2-13.

7. Amounts. Optionally enter Control Totals and Control Count in the Amounts

region. Use the Running Totals and Counts and the Difference column to verify
actual versus entered totals.

See: Verifying Control Totals and Control Counts, page 2-21.

8. Choose Expenditures to enter the batch. The status of a new batch is always Working.

9. Enter the expenditures and expenditure items in the batch. See: Entering

Expenditures, page 2-14.

10. Save your work.

Related Topics

Uploading Expenditure Batches from Microsoft Excel, page 2-19

Entering Expenditures

This section describes how to enter expenditures and expenditure items in Oracle
Projects.

2-14 Oracle Project Costing User Guide

To enter an expenditure:

You enter expenditures using the Expenditures window.

1. Employee and Organization. In the Expenditures window, enter the employee

or organization that incurred the cost.

• For time and expense reports, enter an employee.

• For asset usages, miscellaneous, and burden transactions, enter an employee

or organization.

• For all other expenditures, enter an organization.

Note: When you enter an employee name, the Organization field is
populated by default with the organization to which the employee
belongs. You can only update the Organization value if you have the
function security required to do so. If you do not have the required
function security, you must enter an expenditure belonging to the
default organization.

2. Control Total. Optionally enter the total units of measure in the Control Total

field. (Some companies record the total units of measure on the paper expenditure
report. Record that total in the Control Total field.)

When you have entered all the expenditure items, you can compare the Control
Total with the Running Total, to verify your entries. See: Verifying Control Totals
and Control Counts, page 2-21.

3. Currency Fields. If the expenditure type class for the expenditure batch is
Expense Reports, the currency fields are enabled. For descriptions of these
fields, see: Currency Fields for Expenditures, page 2-17.

Expenditures

2-15

Note: The currency fields are not shown in the default folder. You
can modify the folder to display these fields.

4. Expenditure Items. Enter the expenditure items In the Expenditure Items

region. See: Entering Expenditure Items, page 2-16.

5. Optionally rework the expenditure to add or revise transactions, and save your

changes.

6. When you have completed the expenditure batch, submit the batch for

review. See: Submitting an Expenditure Batch, page 2-22.

To enter expenditure items:

Oracle Projects validates expenditure item information as you enter it. For a list of the
validation criteria Oracle Projects uses, see:Expenditure Item Validation, page 2- 2 .

For each expenditure item, enter the following information:

1. Expenditure Item Date. The date of the expenditure item.

2. Project Number. The Project Number to charge for this expenditure item.

3. Task Number. The lowest level Task Number to charge for this expenditure item.

4. Assignment Name. When Oracle Project Resource Management is installed, you

can associate labor and expense report expenditures to scheduled work
assignments. Refer to the Oracle Project Resource Management User Guide for more
information.

5. Work Type. You can choose any active work type. This field is required when the
PA: Require Work Type Entry for Expenditures profile option has a value of Yes.

6. Expenditure Type. You can choose any expenditure type within the current

expenditure type class.

7. Non-Labor Resource and Non-Labor Organization. If the expenditure type class for

the batch is Usages, enter the non-labor resource and its owning organization. This
enables you to track usage of company-owned assets.

8. Currency Fields. You can optionally display and enter the currency fields. For

descriptions of these fields, see: Currency Fields for Expenditure Items, page 2-18.

9. Quantity. The quantity of units (the unit of measure is determined by the
expenditure type). For example, on a timecard, you enter the quantity for
professional labor in hours. You can enter a mixture of units, such as currency and
miles, for an expense report.

If a currency amount is entered in this field, it is the Reimbursement Amount.

10. Reimbursement Amount. If the Reimbursement Currency is different from the

Receipt Currency, and you enter receipt currency attributes, then the reimbursement
amount is calculated automatically and displayed in this field. Alternatively, you
can enter the reimbursement amount directly.

If you enter a value in this field, then the receipt currency attribute fields are
disabled. This is because your entry is one of the following amounts:

• Reimbursement Amount. As described above, no conversion attributes are

required if you enter the reimbursement amount.

2-16 Oracle Project Costing User Guide

• Quantity. The quantity for an expenditure item with an associated cost rate, in
which case there is no associated Receipt Currency Amount to be converted.

11. Comment. Optionally enter a free text Comment.

12. Save your work.

Related Topics

Uploading Expenditure Batches from Microsoft Excel, page 2-19

Entering Currency Fields

To enable you to process transactions that involve currencies other than the project
currency, Oracle Projects provides currency fields for expenditures and expenditure
items.

Notes:

• In general, when rate type, rate date, and rate fields are displayed for a currency, you
can enter the rate only if the rate type is User. Otherwise, the rate is calculated by the
system based on the rate type and rate date.

• The Expenditure Items window is a folder-type window, and many of the fields are
not displayed in the default folder. You may want to create folders that display the
fields you need, for the types of entries you need to make. For example, you may
need to display Receipt Currency fields for expense reports, if expense report items
originate in a currency other than the reimbursement currency.

For information on using folders, see the Oracle Applications User’s Guide.

• Each of the attributes is determined separately. That is, if a rate type is overridden at
one level, but no rate date is entered at that level, the entered rate type is used and
the default rate date is used.

• For Timecards, Oracle Projects displays currency attributes only for the project

currency.

For additional information about entering multiple currency transactions, including how
default currency attributes are determined, see: Converting Multiple Currencies, Oracle
Projects Fundamentals.

Currency Fields for Expenditures

If you are entering an expense report, you can specify any Reimbursement Currency. You
specify one reimbursement currency for the entire expenditure (rather than for each
expenditure item).

The following table shows expenditure currency fields for expense reports:

Expenditures

2-17

Field

Functional Currency

Reimbursement Currency

Functional Rate Date

Functional Rate Type

Functional Exchange Rate

Description

This is a display-only field that shows the
functional currency of the expenditure
operating unit.

This field defaults to the functional currency. If
you want to be reimbursed in a different
currency from the functional currency, enter
the reimbursement currency.

The exchange rate date that will be used to
determine the exchange rate to convert the
reimbursement currency to the functional
currency. You can accept the default rate
date, or override it.

The default value of this field depends on
the value of Exchange Rate Date Type in the
Currency Implementation Options:

- If the implementation option is set to
PA Period Ending Date, no default date
is displayed. You can enter a date, or the
cost distribution processes will calculate the
exchange rate date.

- If the implementation option is set to
Expenditure Item Date, Oracle Projects uses
the transaction date as the default date.

See: Currency Implementation Options, Oracle
Projects Implementation Guide

The exchange rate type that will be used to
convert the reimbursement currency to the
functional currency. You can accept the default
rate type, or override it.

The exchange rate that will be used to
convert the reimbursement currency to the
functional currency. If the Functional Rate
Type is USER, you can enter a value in this
field. Otherwise, this field is calculated by the
system, based on the rate date and rate type.

Currency Fields for Expenditure Items

The currency fields for expenditure items are shown in the following table:

2-18 Oracle Project Costing User Guide

Field

Description: Expense
Reports

Description: Expenditures
Other than Expense Reports

Reimbursement Currency

The reimbursement currency. Not displayed.

Transaction Currency

Not displayed.

The transaction currency
code. Enter the code for
the currency in which the
transaction occurred.

Functional Currency

The currency code for the
functional currency (display
only).

The currency code for the
functional currency (display
only).

Functional Rate Type

Functional Rate Date

Functional Exchange Rate

These fields are display-only,
since they are controlled for
the entire expenditure in the
Expenditure window region.

The currency attributes for the
functional currency.

Project Currency

Project Rate Type

Project Rate Date

Project Exchange Rate

Receipt Currency

Receipt Amount

The currency code for the
project currency (display
only).

The currency code for the
project currency (display
only).

If the project currency is
the same as the functional
currency, these fields are
display-only. They display the
same values as the functional
currency attribute fields.

If the project currency is
the same as the functional
currency, these fields are
display-only. They display the
same values as the functional
currency attribute fields.

If the project currency is not
the same as the functional
currency, you can enter these
currency attributes.

If the project currency is not
the same as the functional
currency, you can enter these
currency attributes.

The currency in which the
expenditure item originally
occurred.

NOTE: If a cost rate is
associated with an expenditure
item, the receipt currency
fields are disabled for that
item.

The amount of the expenditure
item in the receipt currency
(the actual amount paid
for goods or services in the
original currency.)

Not displayed.

Not displayed.

Receipt Exchange Rate

The exchange rate to convert
from the receipt currency to
the reimbursement currency.

Not displayed.

Uploading Expenditure Batches from Microsoft Excel

You can enter and upload pre-approved expenditure batches using Microsoft Excel
spreadsheets. You can validate records during entry by connecting to the database

Expenditures

2-19

or you can create the spreadsheet offline and allow validation to occur during the
transaction upload.

Note: If you choose to create the spreadsheet offline, only mandatory
fields associated with a list of values are validated during transaction
upload. The transaction upload calls the Transaction Import process
where additional transaction validations take place.

To download an entry template:

1. Using Microsoft Internet Explorer, log into Oracle Self-Service Applications.

2.

Select the Project Super User Responsibility or a user-defined responsibility that
includes the Microsoft entry options.

3. Use the scroll bar on the right to access the Expenditure Entry Using Microsoft

Excel menu options.

4.

Select a template.

5. Enter data in the spreadsheet.

All fields marked with an asterisk are mandatory. If List-text appears under
the column name, then a list of values is available. To access the list of
values, double-click in the column or select List of Values from the Oracle menu
option located at the top of the spreadsheet template.

To upload spreadsheet entries to Oracle Projects

1.

Select Upload from the Oracle menu option located at the top of the spreadsheet
template.

2. Optionally, select the Parameters button to select upload options. After viewing
the Parameters window, you must select Close or Proceed to Upload to return to
the Upload window.

3.

Select Upload to launch the upload process. The upload process updates the message
column for each record in the spreadsheet to indicate whether the upload was
successful.

Note: The upload process populates the transaction import
table. You can optionally use the upload parameter to run
the transaction import process automatically. For more
information, see: Transaction Import, Oracle Projects APIs, Client
Extensions, and Open Interfaces Reference.

Copying an Expenditure Batch

If you frequently enter similar groups of timecard expenditures, you can reduce manual
data entry by copying data from one week to the next. The Copy function copies all
expenditures and, optionally, all expenditure items from a specified source batch. Then
you need to revise only the items that are different in the new batch. There are two
approaches to copying expenditure data:

• Create, then copy a batch template.

• Copy expenditures from any previously created timecard batch.

2-20 Oracle Project Costing User Guide

To create a batch template:

A timecard template is a generic batch containing the most frequently used data
elements. For example, if you expect timecards from certain employees to be
submitted each week, you can create a template that contains just the expenditure
information. Or, if employees generally perform the same tasks for the same projects
week after week, you can enter expenditure items in your template as well.

1. To create a batch template, follow the normal steps for creating a batch. See: Entering

Pre-Approved Expenditure Batches, page 2-12.

Tip: Give the batch a name that will indicate it is a template.

2. Do not submit the batch, since the batch template does not contain real expenditures

and expenditure items.

To copy a batch:

1. Navigate to the Expenditure Batches window.

2. Enter the Batch name, Ending Date, Class, and Description.

3.

Save your new batch.

4. Choose Copy From.

5.

In the Copy From Expenditure Batch window, enter the name and description of the
batch you want to copy. If you want to copy the expenditure items associated with
the batch, choose Copy Expenditure Items.

6. Choose OK.

7. Revise the batch information (such as the Expenditure Ending date), make any

changes to individual expenditure items, and save your work.

Verifying Control Totals and Control Counts

When you enter a Control Total or Control Count on the Expenditure Batch window, or
enter a Control Total on the Expenditures window, Oracle Projects keeps track of the
running total and running count of expenditures within a batch, and the running total
for expenditure items associated with an expenditure. As you enter expenditure
items, the system maintains a running total of each amount.

• To verify that the total hours, usages, expenses, or miscellaneous, burden, inventory,
or work in process transaction amounts entered for a batch match the total recorded
on the paper expenditure reports, calculate the total Units of Measure in the batch
and enter the result as the Control Total.

Note: The Running Total field will tabulate a total only if each
expenditure item in the batch uses the same Unit of Measure.

• To verify that the total number of expenditures entered matches the total number

of expenditures in the batch, count the paper expenditure records and enter the
result as the control Count.

Oracle Projects verifies control totals and control counts when you submit a batch. If the
running total or running count does not equal your control totals, the system does not let
you submit the expenditure batch until your totals match. If you do not enter control
totals, the system does not check that control totals match.

Expenditures

2-21

Submitting an Expenditure Batch

After entering a batch of expenditures and verifying data entry, you submit the batch
for review. Your supervisor typically reviews the batch and either releases it for cost
distribution or returns it to you to rework. When you rework a batch, the status changes
from Submitted to Working.

Note: You can choose Unreleased from the Status poplist in the Find
Expenditure Batches window to retrieve both Working and Submitted
expenditure batches.

To submit a batch for review:

1. Navigate to the Expenditure Batches window and choose the batch you want to

submit.

Tip: You can use the Find Expenditure Batches window to query a
particular batch in the Expenditure Batches window.

2. Choose the Submit button. The status of the batch changes from Working to Submitted

after Oracle Projects validates the control totals and counts.

Reviewing and Releasing Expenditure Batches

Once submitted, batches of pre-approved expenditures are reviewed and released for
cost distribution or returned to the user who entered the batch for reworking. You release
a batch of expenditures by changing its status from Submitted to Released. Releasing a
batch automatically releases all the expenditures and expenditure items in the batch.

To review an expenditure batch:

Find the batch you want to review in the Find Expenditure Batches window. In the
Expenditure Batches Summary window, choose the batch you want to review and
choose Open to review information for the batch, or choose Expenditures to review
expenditure and expenditure item information.

To release an expenditure batch:

From the Expenditure Batches or the Expenditure Batches Summary windows, select the
batch or batches you want to release and choose Release. For information on selecting
multiple records, see the Oracle Applications User’s Guide.

Related Topics

Correcting Expenditure Batches, page 2-23

Reversing an Expenditure Batch

The Reverse button is enabled only if the current batch is released. In addition, an
expenditure batch can be reversed only if the transaction source of the batch allows
adjustments.

When you reverse an expenditure batch, all the expenditure items are reversed except
the following:

• Related items

2-22 Oracle Project Costing User Guide

• Expenditure items that have already been reversed

• Reversing items (net zero adjusted items)

• Expenditure items that were created as a result of a transfer adjustment

To reverse an expenditure batch:

1. Navigate to the Find Expenditure Batches window.

2. Find the batch that you want to reverse.

3.

4.

In the Expenditure Batches window, choose Reverse.

In the Reverse an Expenditure Batch window, enter the name of the new reversing
batch and choose OK .

When the reversal is complete, Oracle Projects displays the number of items that
were adjusted and the number of items that were rejected.

Related Topics

Creating Automatically Reversing Expenditure Batches, page 2-13

Correcting Expenditure Batches

After you submit a batch, you can add, delete, and revise expenditures and expenditure
items. You also must correct a batch if your supervisor rejects and returns a submitted
batch to you.

If the batch has a status of Submitted, locate the batch, return its status to Working, and
change the expenditure or expenditure item before resubmitting the batch.

If the batch has a status of Released, correct the individual expenditure items by reversing
the full amount of the original item and then entering the correct information. For
example, if you entered six hours on a timecard expenditure item when the correct
number of hours is four, create a reversing item equal to a negative six hours, then add a
new expenditure item of four hours. To enter the corrected items, create a new batch and
then follow the normal steps for submitting and releasing expenditures.

To rework (correct) a submitted or returned batch:

1. Navigate to the Find Expenditure Batches window and find the expenditure batch

you want to rework.

2. From the Expenditure Batches window, choose Rework. The status of the batch

changes from Submitted to Working.

3. Choose the Expenditures button to display the expenditures in the Expenditures

window, then make corrections to any expenditure or expenditure items in the batch.

4.

Save your work and submit the batch again. See: Submitting an Expenditure Batch,
page 2-22.

To correct a released expenditure item:

1. Create a new batch for the correction items. The Expenditure Ending date must

identify the week that includes the expenditure item you are reversing. See: Entering
Pre-Approved Expenditure Batches, page 2-12.

Expenditures

2-23

Note: Optionally check the All Negative Transactions Entered As
Unmatched check box if you want to enter transactions with
negative amounts and do not want Oracle Projects to search for
corresponding existing transactions.

2.

In the Expenditure Items window, select the Reverse Original button.

Note: Instead of choosing the Reverse Original button, you can
enter a negative amount in the Quantity field. Negative amounts are
preceded by a minus (-) sign. If you have checked the All Negative
Transactions Entered As Unmatched check box, Oracle Projects will not
search for corresponding existing transactions. Otherwise, Oracle
Projects will prompt you to confirm the creation of each negative
transaction that does not have a corresponding existing transaction.

3.

In the Reverse Expenditure Items window, fill in all the fields to specify the item
you want to reverse. Then choose the Reversal button.

The system inserts a reversing (negative) expenditure item into the batch.

4. Finish entering the batch and submit the batch as usual. See: Submitting an

Expenditure Batch, page 2-22.

Note: Expenditure batches can contain both positive and negative
transactions.

Related Topics

Reviewing and Releasing Expenditure Batches, page 2-22

Controlling Expenditures

This section describes how to use transaction controls to control the expenditures that
can be charged to a project.

Oracle Projects provides you with many levels of charge controls:

Project Status

You can use the project status to control whether any
charges are allowed for the project.

Task Chargeable Status

Start and Completion
Dates

Transaction Controls

You can specify a lowest task as chargeable or
non-chargeable, to control whether any charges are allowed
for the task.

You can specify the start and completion dates of a lowest
task, to record the date range for which charges are allowed
for the task. The start and completion dates of the project
also limit when transactions can be charged.

You can define transaction controls to specify the types of
transactions that are chargeable or non-chargeable for the
project and tasks.

Use transaction controls to configure your projects and tasks to allow only charges that
you expect or plan. You can also define which items are billable and non-billable on
your contract projects. For capital projects, you can define which items are capitalizable

2-24 Oracle Project Costing User Guide

and non-capitalizable. This proactive means to control charges to projects enables you
to better manage your projects.

You enter transaction controls in the Project Options and Task Options
windows. See: Project and Task Information, Oracle Projects Fundamentals.

You can configure transaction controls by the following:

• Expenditure Category

• Expenditure Type

• Employee (includes contingent workers)

• Non-Labor Resource

You can create any combination of transaction controls that you want; for example, you
can create a transaction control for a specific person and expenditure type, or you can
create a combination for a person, expenditure type, and non-labor resource.

You also specify the date range to which each transaction control applies.

If you do not enter transaction controls, you can charge expenditure items from any
person, expenditure category, expenditure type, and non-labor resource to all lowest
tasks on the project.

Using Transaction Control Extensions

To define more complex rules for implementing company-specific expenditure entry
policies, you may need to use transaction control extensions.

See: Transaction Control Extensions, Oracle Projects APIs, Client Extensions, and Open
Interfaces Reference

Inclusive and Exclusive Transaction Controls

You specify whether the transaction controls you enter are inclusive or exclusive.

• Inclusive transaction controls limit charges to only the transaction controls entered;
Oracle Projects then rejects any charges that are not listed as chargeable in the
transaction controls.

You make your transaction controls inclusive by checking the Limit to Transaction
Controls box on the Transaction Controls window.

• Exclusive transaction controls allow all charges except those that are specified as
non-chargeable in the transaction controls. Oracle Projects defaults to exclusive
transaction controls.

For either method of transaction controls, you can enter the following information:

• Expenditure category

• Expenditure type

• Non-labor resource

• Employee (or contingent worker)

• Scheduled Expenditure Only

• Chargeable

Expenditures

2-25

• Workplan Resources Only

• Person Type

• Billable (contract projects)

• Capitalizable (capital projects)

• Effective from

• Effective to

You must specify a person (employee or contingent worker) or expenditure category for
each record. You can specify a non-labor resource for usage expenditure types.

Employee Controls with Usage and Supplier Transactions

Transaction controls that you define for people (employees and contingent workers) do
not apply to transactions that are not associated with people. This includes purchasing
and supplier invoice transactions entered for a supplier not associated with a person, and
usage items incurred by an organization and not a person.

If you define transaction controls to list people who can charge to your project, Oracle
Projects allows transactions incurred by those people. It also allows any purchasing
transactions, supplier invoice transactions, and usage items incurred by an
organization, and any other transactions that do not require an employee number.

Employee Controls with Expense Reports Entered in Oracle Payables

If you enter expense reports in Oracle Payables, and use suppliers associated with
employees, Oracle Projects validates the transaction using the person associated with the
supplier. For example, if you specify that Donald Gray cannot charge to the project, and
you enter an expense report item for the supplier GRAY, DONALD who is associated
with the person Donald Gray, Oracle Projects does not allow you to charge the item to
the project, because it validates the transaction controls that you have defined.

Allowable Charges for Each Transaction Control

You can further control charges for each transaction control record by specifying whether
to allow charges. The default value is to allow charges.

You usually select Chargeable when you are using inclusive transaction controls. For
example, if you wanted to allow people to charge only labor to your project, you would
check Limit To Transaction Controls to limit charges to only the transaction controls
entered. Then you would define a transaction control with the Labor category, and
allow charges to that transaction control.

You usually do not select Chargeable when you are using exclusive transaction controls
because exclusive transaction controls list the exceptions to chargeable transactions.

You can also record exceptions by defining some transaction controls to allow charges
and others not to allow charges. For example, say you want to define that people can
charge all labor except administrative labor. Select Limit To Transaction Controls to make
the transaction control inclusive. You then enter one transaction control record with
the Labor category that allows charges, and another transaction control record with the
Labor category, Administrative type that does not allow charges.

2-26 Oracle Project Costing User Guide

Scheduled Expenditures Only Controls

When Oracle Project Resource Management is installed, you can specify that only
people with scheduled work assignments are allowed to charge their labor and expense
report transactions to your project.

Workplan Resources Only Controls

You can control charges to tasks based on the people assigned to the workplan tasks. The
following table summarizes the validation rules for timecards and expense reports when
the Workplan Resources Only control is set with the other transaction control attributes.

Validation Rules for Workplan Resources Only Control

Control Value

Category

Category/Type

Category/Type/Person

Person

Validation Rules

People can enter their timecards and expense
reports for the category if they have a
named-person assignment on a workplan task.

People can enter their timecards and expense
reports for the category and type if they have a
named-person assignment on a workplan task.

The specified person can enter timecards and
expense reports for the category and type if
they have a named-person assignment on a
workplan task.

The specified person can enter timecards and
expense reports if they have a named-person
assignment on a workplan task.

Person Type Control

You can select no value, Employee Only, or Contractor Only from the list in the Person
Type field. You can use this control to specify whether transactions incurred by only
employees, only contractors (contingent workers), or both are chargeable.

Expenditures

2-27

Validation Rules for Person Type Control

Limit To Check Box

Person Type

Validation Rules

Checked

No Value

Checked

Checked

Employee Only

Contractor Only

Not Checked

No Value

Not Checked

Employee Only

Not Checked

Contractor Only

Transactions incurred by both
employees and contingent
workers are chargeable.

Only transactions incurred by
employees are chargeable.

Only transactions incurred
by contingent workers are
chargeable.

Transactions incurred by both
employees and contingent
workers are not chargeable.

Transactions incurred by
employees are not chargeable.

Transactions incurred by
contingent workers are not
chargeable.

Specifying Billable and Capitalizable Transactions

You can control what transactions for contract projects are non-billable and
what transactions for capital projects are non-capitalizable when you set the
Billable/Capitalizable field. You can choose between the options of No or Task Level. You
select No if you want the charges to be non-billable or non-capitalizable; you select Task
Level if you want the billable or capitalizable status to default from the task to which the
item is charged.

You define the billable or capitalizable status for a task in the Task Details window. This
value defaults to all expenditure items charged to the task.

Specifying Effective Dates for Transaction Controls

You can define transactions as chargeable for a given date range by entering an Effective
From and Effective To date for each transaction control record. You must specify a start
date; Oracle Projects defaults this value to the Effective From date of the project or
task. The Effective To date is optional.

Determining if an Item is Chargeable

Oracle Projects checks all levels of chargeability control when you try to charge a
transaction to a project. The check is performed when you save the record. Oracle
Projects checks the control when you:

• enter an online or pre-approved expenditure item

• copy a pre-approved timecard item

• transfer items to a new project or task

• enter a project-related requisition or purchase order distribution in Oracle Purchasing

2-28 Oracle Project Costing User Guide

• enter a project-related invoice distribution in Oracle Payables

Chargeability Controls

The transaction validation checks are performed using the following tests (chargeability
controls):

• Project status allows new transactions

• Task is chargeable

• Expenditure item date is between the start and end dates for the project and task

• Expenditure item passes validation based on applicable project or task transaction

controls

If the expenditure item passes the first three chargeability controls, then Oracle Projects
checks the transaction controls.

The system first looks for an applicable task level transaction control. If it does not find
applicable task level controls, it looks for project level controls. If the item matches an
applicable transaction control at the task level, project level controls are not checked. The
task level controls override the project level controls.

Applicable transaction controls are all of the transaction control records that apply to an
expenditure item based on the person, expenditure category, expenditure type, non-labor
resource, and dates.

Determining the Chargeable Status of an Expenditure Item

The following illustration shows the steps Oracle Projects uses to determine the
chargeable status of an expenditure item. The steps, which are explained in the
paragraphs that follow, are first followed when checking transaction controls at the task
level, then are repeated at the project level, if required.

Expenditures

2-29

Determining the Chargeable Status of an Expenditure Item

• If the Limit to Transaction Controls check box is selected and applicable transaction

controls do not exist, then the transaction is not chargeable. If applicable controls do
exist, then the system checks whether the controls allow charges. If the Chargeable
check box is selected for an applicable control, then the transaction is chargeable. If
the Chargeable check box is not selected, then the transaction is not chargeable.

• If the Limit to Transaction Controls check box is not selected and there are no applicable
controls, then the transaction is chargeable. If applicable controls do exist, then
the system checks whether the controls allow charges. If the Chargeable check
box is selected for an applicable control, then the transaction is chargeable. If the
Chargeable check box is not selected, then the transaction is not chargeable.

Determining if an Item is Billable or Capitalizable

You specify whether an item is billable for contract projects. Oracle Projects provides
you with two levels of billability control.

Task Billable Status

You can specify a lowest level task as billable or
non-billable. This billable status defaults to all expenditure
items charged to that task.

Transaction Controls

You can define transaction controls to specify what
transactions are non-billable.

2-30 Oracle Project Costing User Guide

Note: You can override the billable status of an expenditure item in the
Expenditure Items and Invoice Line Details window.

You control the capitalizability of transactions for capital projects just as you control the
billability of transactions for contract projects. For more information, see: Specifying
Which Capital Asset Transactions to Capitalize, page 5-12.

Billable Controls

If a transaction is chargeable, Oracle Projects next determines if it is billable using the
following transaction validation checks:

A transaction must meet ALL of the following criteria to be billable:

• Transaction is chargeable

• Task is billable

• Billable field must be set to Task Level in all applicable rows in Transaction Controls

You can specify what is non-billable using transaction controls.

For an item to be billable, the task must be billable. You can make an item non-billable by
setting the Billable field to No for a transaction control record. You cannot mark a task as
non-billable, and then mark expenditure items as billable through transaction controls.

Examples of Using Transaction Controls

Following are some examples of what you can do with transaction controls. You can
study the example configurations to help you better understand how to use transaction
controls in different business scenarios. The examples show you how you can use:

• A combination of employee, expenditure category, expenditure type, and non-labor

resource in your transaction controls

• A combination of project and task level transaction controls

• Transaction controls to control both billability and chargeability

Note: You control capitalizability just as you control billability.

The case studies are:

• CASE 1: Limited employees charge limited expenses, page 2-31

• CASE 2: Different expenditures during different phases of a project, page 2-32

• CASE 3: Some tasks, but not all, are only chargeable for labor expenditures, page 2-33

CASE 1: Limited employees charge limited expenses

In this example, only two employees can charge a project, and they can charge only labor
and expenses, not including entertainment expenses.

Scenario

Project SF100 begins on September 1, 1999. The only people working on the project are
Donald Gray and Amy Marlin; therefore, they are the only employees who can charge to
the project. They can charge only labor and in-house recoverables; however, computer
expenses are not allowed. All charges are billable and reimbursable by the client.

Expenditures

2-31

Setup

Logic

You create Project SF100 and create all tasks as billable. You enter the project-level
transaction controls shown in the following table in the options window of the
Projects, Templates window. Transaction controls that have the Limit to Transaction
Controls flag set are those with the letter X in the Chargeable column

Expenditure
Category

Expenditure
Type

Non-
Labor
Resource

Employee Chargeable Billable Effective

From

Effective
To

Labor

Labor

In-House
Recoverables

In-House
Recoverables

In-House
Recoverables

Computer
Services

Marlin

Gray

Marlin

Gray

X

X

X

X

Task
Level

01-SEP-
99

Task
Level

01-SEP-
99

Task
Level

01-SEP-
99

Task
Level

01-SEP-
99

Task
Level

01-SEP-
99

When the transaction controls have the Limit to Transaction Controls flag set:

• a transaction only needs to match the listed expenditure combination on a given line

OR match the listed employee, AND

• the transaction must not qualify under a Non-Chargeable condition.

Resulting Transactions

Any expenditure that has Amy Marlin or Donald Gray in the employee field may be
charged to the project except Computer Services.

Any expenditure with the expenditure category Labor or In-House Recoverables may be
charged against the project unless the In-House Recoverable is Computer Service, in
which case it is rejected.

All charges are billable as defined by the billable field.

Supplier invoices, expense report charges, and other costs are not allowed.

CASE 2: Different expenditures charged during different phases of a project

In Case 2, different types of expenditures should be charged to the project at different
phases in the project.

Scenario

You have negotiated Project SF200. The project charges will include supplier invoices
for material, labor, and employee travel expenses. You know that supplier invoices are
charged throughout the life of the project; you know that supplier invoices will be
charged before the work even begins since you have ordered materials that you must
have before you can start the project work. The project work is scheduled to last two

2-32 Oracle Project Costing User Guide

Setup

months; employees submit timecards each week, but are allowed a two week lag to
submit their expense reports.

The project is scheduled to begin on September 1, 1995. The project work, which is
dependent on receiving materials purchased, is scheduled for October 1 to December
31, 1995. Expense reports can be charged until January 15, 1996, two weeks after the
project ends.

You create Project SF200 with a duration from 01-SEP-95 to 15-JAN -96. You create the
transaction controls shown in the following table. Transaction controls that have the
Limit to Transaction Controls flag set are those with the letter X in the Chargeable column.

Expenditure
Category

Expenditure
Type

Non-
Labor
Resource

Employee Chargeable Billable

Effective
From

Effective
To

Material

Labor

Labor

Administrative

Travel

X

X

X

X

Task
Level

Task
Level

No

01-SEP-
95

01-OCT-
95

31-DEC-
95

01-OCT-
95

31-DEC-
95

Task
Level

01-OCT-
95

15-JAN-
96

Resulting Transactions

Supplier invoices for materials can be charged to the project from 01-SEP-95 to the
end of the project.

Labor can be charged to the project from 01-OCT-95 to 31-DEC-95. Any labor charged
outside those dates is not allowed. All labor, except Administrative, is billable based on
the billable field; Administrative labor is non-billable based on the transaction control
billable field.

Travel expenses can be charged to the project from 01-OCT-95 to 15-JAN-96. Any
expenses charged outside those dates are not allowed.

CASE 3: Some tasks, but not all, are only chargeable for labor expenditures

Only labor can be charged to the project. There are exceptions to this rule for specific
tasks, which are configured using task transaction controls.

Scenario

Project SF300 has been negotiated to perform an environmental study for the proposed
site of a new housing development. You organize the project so that you can easily
manage its status and control the charges using the project work breakdown structure
shown in the following table. All tasks except Task 1 are defined as billable.

Expenditures

2-33

Task Number

Task 1

Task 2

Task 3

Task 3.1

Task 3.2

Task 4

Task Name

Administration

Purchases

Analysis

Onsite Analysis

In-house Analysis

Writeup

Most of the charges on the project are labor. All labor is billable, except for
Administrative labor. Some tasks involve charges other than labor.

• All administration for the project, which includes only labor and computer usage, is

charged to task 1. Donald Gray, the project manager, and Sharon Jones, his
assistant, are the only people handling the administration of the project.

• You know that you must make a few purchases to perform the analysis for the

project; you will monitor the charges for the supplier invoices in task 2.

• You have reserved Field Equipment and a van for the onsite analysis (Task 3.1), but

know that your client will not reimburse vehicle charges on this project.

• You have arranged for Susan Marshall from the East Coast office to fly in for a week
to help with the in-house analysis since she has done this type of analysis before. She
will charge her expenses to the same task, but your client will not be invoiced for
those expenses. No other expenses are allowed on that task.

In summary, the controls you want to define for your project are shown in the following
table:

2-34 Oracle Project Costing User Guide

Project/Task

Task Name

Transaction Controls

Project

Task 1

Administration

Task 2

Task 3

Task 3.1

Purchases

Analysis

Onsite Analysis

- only labor allowed

- Administrative labor is
non-billable

- only labor and computer
allowed

- only Gray and Jones can
charge

- all charges non-billable

- only supplier invoices
allowed

- labor, equipment, and van
charges allowed

- van charges are non-billable

Task 3.2

In-house Analysis

- labor allowed

Task 4

Writeup

Setup: Project Level

- no expenses allowed, except
for expenses from Susan
Marshall; her expenses are
non-billable

- only labor allowed

- Administrative labor is
non-billable

You create Project SF300 with your work breakdown structure. You enter the transaction
controls shown in the following table at the project level. Transaction controls that have
the Limit to Transaction Controls flag set are those with the letter X in the Chargeable
column.

Expenditure
Category

Expenditure
Type

Non-
Labor
Resource

Employee Chargeable Billable Effective

From

Effective
To

Labor

Labor

Administrative

X

X

Task
Level

01-SEP-
95

No

01-SEP-
95

Setup: Task 1

You enter the transaction controls shown in the following table for Task 1 (task is
non-billable). Transaction controls that have the Limit to Transaction Controls flag set are
those with the letter X in the Chargeable column.

Expenditures

2-35

Expenditure
Category

Expenditure
Type

Non-
Labor
Resource

Labor

In-House
Recoverables

Computer

Effective
To

Employee Chargeable Billable Effective

From

01-SEP-
95

01-SEP-
95

01-SEP-
95

01-SEP-
95

X

X

X

X

Task
Level

Task
Level

Task
Level

Task
Level

Gray

Jones

Resulting Transactions: Task 1

Setup: Task 2

Donald Gray and Sharon Jones can charge to all expenditure categories and types
for this task.

All other employees can only charge to Labor and to In-House Recoverables / Computer
for this task.

The project transaction controls are not evaluated for charges to this task, because the
Limit to Transaction Controls is selected.

You enter the transaction controls shown in the following table for Task 2. Transaction
controls that have the Limit to Transaction Controls flag set are those with the letter X in
the Chargeable column.

Expenditure
Category

Expenditure
Type

Non-
Labor
Resource

Employee Chargeable Billable

Effective
From

Effective
To

Material

Outside
Services

Other
Expenses

Other
Invoice

X

X

X

Task
Level

Task
Level

Task
Level

01-SEP-
95

01-SEP-
95

01-SEP-
95

Resulting Transactions: Task 2

Only supplier invoice expenditures can be charged to this task. The charges are billable
as defined by the billable field.

All other types of charges are not allowed. The project transaction controls are not
evaluated for charges to this task, because the Limit to Transaction Controls is selected.

2-36 Oracle Project Costing User Guide

Setup: Task 3.1

You enter the transaction controls shown in the following table for Task 3.1 (task is
billable). Transaction controls that have the Limit to Transaction Controls flag set are
those with the letter X in the Chargeable column.

Expenditure
Category

Expenditure
Type

Non-
Labor
Resource

In-House
Recoverables

Field
Equipment

In-House
Recoverables

Vehicle

Van

Labor

Employee Chargeable Billable Effective

From

01-SEP-
95

01-SEP-
95

Task
Level

No

Task
Level

01-SEP-
95

X

X

X

Effective
To

Resulting Transactions: Task 3.1

Setup: Task 3.2

The only type of in-house recoverable expenditures allowed are Field Equipment and
Vehicle. The only type of Vehicle charge allowed is the use of a van. The Van charges are
non-billable as defined by the transaction control.

All labor can also be charged to this task. Expense report charges, supplier
invoices, in-house recoverables other than Field Equipment and Vehicle usage of
a Van, and other costs (such as Miscellaneous Transactions, Inventory, Work in
Process, and Burden Transactions) cannot be charged to this task, as defined by the task
transaction controls using Limit to Transaction Controls selected.

You enter the transaction controls shown in the following table for Task 3.2 (task is
billable). Transaction controls that have the Limit to Transaction Controls flag set are
those with the letter X in the Chargeable column.

Expenditure
Category

Expenditure
Type

Non-
Labor
Resource

Employee Chargeable Billable Effective

From

Effective
To

Travel

Travel

Task
Level

01-SEP-
95

Marshall

X

No

01-SEP-
95

Resulting Transactions: Task 3.2

Susan Marshall can charge travel expenses, which are non-billable as defined by the task
transaction controls. No other employee can charge travel expenses to this task.

All labor can also be charged to this task. Because this task’s Limit to Transaction
Controls is set to No and no applicable transaction control was found at the task level
for the following types of charges, the charges are evaluated based on the project
transaction controls; these type of charges include: labor, supplier invoices, and in-house
recoverables. Supplier invoices, in-house recoverables, and other costs are not allowed
since they are not listed in the project level transaction controls.

Expenditures

2-37

Setup: Task 4

You do not enter transaction controls for this task.

Resulting Transactions: Task 4

All labor can be charged to this task. All other charges are not allowed based on the
project transaction controls.

All charges are evaluated based on the project transaction controls, because no
transaction controls are entered for the task.

Viewing Expenditures

This section describes use of the Expenditure Items and View Expenditure Accounting
windows to review project expenditures.

Viewing Expenditure Items

Use the Expenditure Items window to review a project’s expenditure items. You can see
the amount and type of expenditure items charged to a project, the date an expenditure
item occurred, accrued revenue, and other information. You can also drill down to
Oracle Payables to view the Invoice Overview form, or to Oracle General Ledger to
view T-accounts.

To view expenditure items (perform an expenditure inquiry):

1. Navigate to the Find Project Expenditure Items or Find Expenditure Items window.

Your ability to navigate to either window (by selecting Project or All) depends
on your user responsibility.

If you select Project, you can view expenditure items for a single project. If your
system uses project security, you can select only projects that you are allowed to
see. You can view expenditure items for a project that are specific to the current
operating unit, as well as those expenditure items that are charged across operating

2-38 Oracle Project Costing User Guide

units. You can enter search criteria to determine whether Oracle Projects queries
expenditure items specific to the current operating unit, expenditure items charged
across operating units, or both.

If you select All, you can view expenditure items across projects, and can
structure your query to retrieve information across projects. No project security is
enforced. Oracle Projects shows only the expenditure items that correspond to the
current operating unit. If a project has expenditure items that are charged across
operating units, then you are not able to view these expenditure items using the Find
Expenditure Items window. In this case, you must use the Find Project Expenditure
Items window to view these expenditure items.

2.

In the Find Expenditure Items window, enter your search criteria. See: Expenditure
Items Windows Reference, page 2-41.

3. Choose Find if you want to execute the search, or choose Mass Adjust if you want to

process mass adjustment of expenditures. See: Mass Adjustment of Expenditures,
page 2-50.

4. From the Expenditure Items window, choose:

• Run Request to create Project Streamline Requests to process adjustments. You

can select multiple processes to run for your project. The requests will run in the
correct order. See: Adjusting Expenditure Items, page 2-49.

• Totals to view the totals for the expenditure items returned based on your

search criteria.

Note: This window does not display events. If your project
uses event-based or cost-to-cost revenue accrual or invoice
generation, use the Events window to view the total project
revenue and bill amounts.

• Item Details to select a window for reviewing the details of this expenditure
item. The Inquiry Options window will be displayed, from which you can
choose one of the following options:

• Choose Cost Distribution Lines to view individual transactions and the

debit and credit GL accounts charged for raw and burdened costs for each
expenditure item. You can also view other information about the cost
lines, such as PA and GL period and interface status and the rejection reason
if transactions could not be interfaced.

• Choose Revenue Distribution Lines to view the revenue transactions generated
for a specific expenditure item. The GL account credited for the revenue is
displayed. You can also see the GL and PA posting period for the revenue
and the interface status. The rejection reason will be displayed for any
transactions that are rejected during the interface to GL.

• Choose AP Invoice to drill down to the Invoice Overview form in Oracle
Payables. (This option is only enabled for expenditure items whose
expenditure type class is either Supplier Invoices or Expense Reports.)

Note: You can also view rejection reasons for transactions
rejected during the costing or revenue generation
processes from the Expenditure Items window. From the
Folder menu, choose Show Field and select either Cost
Distr. Rejection or Revenue Distr. Rejection.

Expenditures

2-39

Viewing Accounting Lines

You can see how a transaction will affect the account balances in your general ledger by
viewing the detail accounting lines for the transaction as balanced accounting entries
(debits equal credits) or T-accounts.

To view accounting lines:

1. Query the expenditure transaction you want to view.

2. From the Expenditure Items window, choose View Accounting from the Tools menu.

You see the View Expenditure Accounting window.

Note: The View Expenditure Accounting window is a
folder form that you can customize to display additional
columns. See: Customizing the Presentation of Data in a
Folder, Oracle Applications User’s Guide.

3.

(Optional) To view the accounting detail for the selected line as T-accounts, choose
T-Accounts. In the Options window that opens, select from the Default Window
poplist, and then choose from the window buttons to drill down in General Ledger.

See: T-Accounts, Oracle General Ledger User Guide

Drilling Down to Oracle Projects from Oracle General Ledger

From General Ledger, you can drill down to subledger details from the Account
Inquiry, Enter Journals, or View Journals windows for journals that have specific journal
sources assigned to them. For example, if a journal source is Projects, you can drill down
to the transaction details in Oracle Projects.

2-40 Oracle Project Costing User Guide

Depending on the nature of the originating Projects transaction, drilling down from
General Ledger will open the Project Expenditure Accounting or Project Revenue
Accounting window.

To drill down to detail transactions or to view transaction accounting:

1. From the Project Expenditure Accounting or Project Revenue Accounting

window, select a detail accounting line.

2. Choose the Show Transaction button to view detail transactions.

3. Choose the Show Transaction Accounting button to view the transaction accounting.

Expenditure Items Windows Reference

This section describes the expenditure items windows.

Find Expenditure Items Window, page 2-41

Expenditure Items Window, page 2-42

Find Expenditure Items Window

Use the Find Expenditure Items window to enter search criteria for expenditures and
expenditure items. This section describes some of the attributes you can use to search
for expenditure items.

Inventory Item: Enter an inventory item number to search for inventory transactions
imported from Oracle Project Manufacturing.

WIP Resource: Enter a work-in-process resource to search for work-in-process
transactions imported from Oracle Project Manufacturing.

Set of Books Currency: The reporting set of books currency in which you want to
view the expenditure items. In the windows that display expenditure items and their
details, you can toggle between the primary set of books currency and the reporting set
of books currency you select here.

Note: You can select an alternate set of books currency only if Multiple
Reporting Currencies (MRC) is enabled. See: Multiple Reporting
Currencies, Oracle Projects Fundamentals.

Item Dates: The date of the expenditure items you want to find. You can enter a date
range, or either a start or end date.

Exp Ending Dates: The expenditure ending dates of the items you want to find. You can
enter a date range, or either a start or end date.

Billing Status: You can choose from the following status types:

Billable

Billing Hold

Choose Yes to view only billable expenditure items.

Choose Yes to view expenditure items that are on hold
indefinitely. Choose No to view items that are not on
hold. Choose Both to view items that are on both one-time
hold, and on hold indefinitely. Choose Once to view
expenditure items that are on one-time hold from this
project’s next invoice.

Expenditures

2-41

Billed

Choose Yes to view expenditure items that have ever
appeared on an invoice, regardless of invoice status. When
you choose this option, Oracle Projects retrieves
expenditure items on a project invoices that have a status of
Unapproved, Approved, Released, and Accepted.

CIP/RWIP Status: You can choose from the following status types:

Capitalizable

Grouped CIP

Grouped RWIP

Choose Yes to view only capitalizable expenditure items.

Choose Yes to view expenditure items that have been
grouped into CIP asset lines.

Choose Yes to view expenditure items for tasks that are set
up for retirement cost processing.

Expensed

Choose Yes to view only expensed expenditure items.

Processing Status: You can choose from the following status types:

Costed

Choose Yes to view only costed expenditure items.

Revenue Distributed

Choose Yes to view only revenue distributed expenditure
items, or choose Partial to view expenditure items that
have partially distributed revenue due to a hard limit
on the agreement.

Expenditure Batch: Choose an expenditure batch name if you want to find expenditure
items grouped and entered by batch.

Transaction Source: The source of the imported expenditure items you want to
find. Examples of transaction sources include faxed timecards and PBX. You can choose
from a valid list of values.

Exclude Net Zero Items: Choose this check box if you want to exclude net zero
expenditure items from the items you query. Net zero items consist of an original
item and a reversing item for the entire amount of the original item. Together, these
two items net to zero.

Expenditure Items Window

The Expenditure Items window displays detailed information about each expenditure
item.

Note: When displaying inventory transactions imported from Oracle
Project Manufacturing, the Expenditure Items window shows the
base unit of measure associated with the inventory item. For all other
transactions, the window shows the unit of measure associated with the
expenditure type. For information on defining expenditure types, see
the Oracle Projects Implementation Guide.

For an expenditure item, when the base unit of measure associated
with the inventory item and the unit of measure associated with the
expenditure type are same, then Oracle Projects attaches a prefix of @
to the base unit of measure from Oracle Project Manufacturing or
Oracle Inventory. For Example, if the unit of measure associated with
an inventory item is Each and the unit of measure associated with the
expenditure type is also Each, then Oracle Projects displays the unit of
measure as @Each for the transaction.

2-42 Oracle Project Costing User Guide

Currency Fields

This window is a folder form, which allows you to set up a folder that contains the fields
you need to view. For example, some of the currency fields are not visible in the default
folder. Currency fields are listed in the following table:

Currency Field

Bill Amount

Description

The bill amount in the project currency

Accrued Revenue

The accrued revenue in the project currency

Project Burdened Cost

The burdened cost in the project currency

Transaction Currency

The transaction currency code

Transaction Raw Cost

The raw cost in the transaction currency

Transaction Burdened Cost

The burdened cost in the transaction currency

Functional Currency

The functional currency code

Functional Rate Type

The rate type used to determine the functional
currency exchange rate

Functional Exchange Rate

The functional currency exchange rate

Functional Raw Cost

The raw cost in the functional currency

Functional Burdened Cost

The burdened cost in the functional currency

Project Currency

Project Rate Type

Project Rate Date

The project currency code

The rate type used to determine the project
currency exchange rate

The date used to determine the project
currency exchange rate

Project Exchange Rate

The project currency exchange rate

Project Raw Cost

Receipt Currency

Receipt Amount

The raw cost in the project currency

The receipt currency code

The expenditure amount in the receipt currency

Receipt Exchange Rate

The receipt currency exchange rate

Multiple Reporting Currency Fields

If you have selected a reporting set of books currency in the Find Expenditures
window, then reporting currency amounts and information can also be selected for
viewing in the Expenditure Items window. The reporting currency information is
shown in the following table:

Expenditures

2-43

Type of MRC Information

Available Fields

MRC Conversion Information

Currency Code, Rate Date, Rate Type, Exchange
Rate

MRC Transfer Price Information

Rate Type, Rate Date, Exchange Rate, Transfer
Price

MRC Cost Information

Raw Cost Rate, Burdened Cost Rate, Raw
Cost, Burdened Cost

MRC Revenue Conversion Information

Conversion Date, Exchange Rate, Rate Type

MRC Revenue Information

Raw Revenue, Accrued Revenue, Adjusted
Revenue, Bill Amount, Forecast Revenue Bill
Rate, Accrual Rate, Adjusted Rate

MRC Project Functional Currency: Invoice
Conversion Information

Rate Type, Rate Date, Exchange Rate

MRC Project Functional Currency: Forecast
Conversion Information

Rate Type, Rate Date, Exchange Rate

Adjusting Expenditures

Oracle Projects provides powerful features that allow you to:

• adjust expenditure items on your projects

• interface the adjustments to other Oracle applications

• report the audit trail of the adjustments

You can make adjustments to expenditure items after the items have been costed, revenue
distributed, and invoiced. Oracle Projects automatically processes the adjusted items
and interfaces the adjusting accounting transactions to other Oracle Applications.

The project status of a project can restrict your ability to enter adjustments to project
transactions. See : Project Statuses, Oracle Projects Implementation Guide.

Audit Reporting for Expenditure Adjustments

Oracle Projects provides an audit trail of all adjustments performed on an expenditure
item. The audit trail records the following information about the adjustment:

• The name of the user who performed the adjustment

• The type of adjustment action performed

• The date and time that the adjustment was performed

• The window from which the adjustment action was performed

Oracle Projects also records the audit trail to the original item for transfers, splits, and
corrections to approved items. With this audit trail, you can identify where an item was
transferred or where an item was transferred from.

2-44 Oracle Project Costing User Guide

You can review the expenditure adjustment audit information for a project in the
AUD:Project Expenditure Adjustment Activity report. You can review the transfer
activity for a project using the MGT: Transfer Activity report.

Related Topics

Project Expenditure Adjustment Activity, Oracle Projects Fundamentals

Transfer Activity Report, Oracle Projects Fundamentals

Types of Expenditure Item Adjustments

This section describes the types of adjustments you can make to expenditure
items. Whether you can adjust expenditure items depends on:

• The project status of the project charged.

• The transaction source (if the expenditure item was imported via Transaction

Import).

Except where noted, you can also adjust project invoice lines. See: Adjusting Project
Invoices, Oracle Project Billing User Guide.

Correct Approved Expenditure Items

You can correct the following attributes of an approved expenditure item using the
Pre-Approved Expenditure Entry windows.

• date

• expenditure type

• project

• task

• amount

You make the corrections by reversing the original item and then creating a new item
using the correct information. You cannot correct these items using the Expenditure
Items window.

You can also change the project and task assignment of an expenditure item by selecting
the Transfer adjustment action.

You cannot correct the amount, date, expenditure type, or supplier of supplier invoice
items in Oracle Projects. You must correct these attributes of supplier invoice item in
Oracle Payables.

You must correct expenditure items imported from Oracle Inventory or Oracle
Manufacturing in their respective systems except for the transactions with transaction
source Inventory Misc. You cannot reverse or correct expenditure items from these
applications in Oracle Projects.

Change Billable Status

Use the adjustment actions Billable to Non-Billable and Non-Billable to Billable to change
the billable status of an expenditure item.

• A billable item accrues work-based revenue and can be invoiced.

• A non-billable item does not accrue work-based revenue and is not invoiced.

Expenditures

2-45

You may want to check the setup of the billable status of your project to reduce the
number of items you need to adjust for billable classification. You can define tasks as
billable or non-billable. You can further specify which items are non-billable using
transaction controls. See: Controlling Expenditures, page 2-24.

Change Capitalizable Status

Use the adjustment actions Capitalizable to Non-Capitalizable and Non-Capitalizable to
Capitalizable to change the capitalizable status of an expenditure item.

• A capitalizable item can be grouped into an asset line you send to Oracle Assets.

• A non-capitalizable item cannot become an asset cost in Oracle Assets.

You can define tasks as capitalizable or non-capitalizable; you can further specify which
items are non-capitalizable using transaction controls. See: Controlling Expenditures,
page 2-24.

Set and Release Billing Hold

You can place an expenditure item on billing hold. An item on billing hold is not
included on an invoice until you release the billing hold on the item.

One-Time Hold

Release Hold

You can place an expenditure item on one-time billing hold. An item on one-time billing
hold is not billed on the current invoice but is eligible for billing on the next invoice. The
one-time billing hold is released when you release the current invoice.

If you have placed an expenditure item on billing hold, you use the release hold to
take it off hold so the item can be billed.

Recalculate Burden Cost

You can recalculate the burden cost of an expenditure item if you find that the burdened
cost amount is incorrect. To produce correct recalculation results, you must correct the
source of the problem before redistributing the items.

Notes

• When you select Recalculate Burden Cost for a burden transaction, no recalculation

of the burden amount takes place.

• You can recalculate the burden cost of an invoice line.

Recalculate Raw Cost

You can recalculate the raw cost of an expenditure item if you find that the raw cost
amount is incorrect. To produce correct recalculation results, you must correct the source
of the problem before redistributing the item.

Notes

• You cannot recalculate raw cost on expenditure items that were imported through

Transaction Import as costed items.

2-46 Oracle Project Costing User Guide

• You can recalculate the raw cost of an invoice line for accounting purposes. Raw cost

will still not change for such transactions.

Recalculate Revenue

You can recalculate revenue if you find that:

• The revenue or bill amount is incorrect due to incorrect bill rate or markup

• AutoAccounting is incorrect

You must correct the source of the problem before redistributing the items.

Recalculate Cost and Revenue

You can recalculate cost and revenue if you find that:

• The raw cost rate is incorrect

• The burden cost multiplier is incorrect

• AutoAccounting is incorrect

You must correct the source of the problem before redistributing the items.

If you recalculate cost, the revenue is automatically adjusted to ensure that revenue that
is based on the cost (with markup or labor multipliers) is correct.

Change Work Type

You can change the work type of an item. You can use this adjustment to reclassify an
item for reporting and billing purposes.

Change Comment

You can edit the expenditure comment of an item. You can use this adjustment to
make the expenditure comment clearer if you are including the comment on an invoice
backup report.

Split Item

Transfer Item

You can split an item into two items so that you can process the two resulting split
items differently. The resulting split items are charged to the same project and task as
the original item.

For example, you may have an item for 10 hours, of which you want 6 hours to be
billable and 4 hours to be non-billable. You would split the item of 10 hours into two
items of 6 hours and 4 hours, marking the 6 hours as billable and 4 hours as non-billable.

You can transfer an item from one project and task to another project and task.

Oracle Projects provides security as to which employees can transfer items between
projects. Cross-project users can transfer to all projects. Key members can transfer to
projects to which they are assigned. See:Security in Oracle Projects, Oracle Projects
Fundamentals.

Oracle Projects performs a standard validation on all transferred items. For a description
of the standard validation process and resulting rejection reasons, see: Expenditure Item
Validation, page 2- 2 .

Expenditures

2-47

Oracle Projects also ensures that you only transfer items which pass the charge controls
of the project and task to which you are transferring. If the items you are transferring
do not pass the new project and task’s charge controls, then you cannot transfer the
item. See: Controlling Expenditures, page 2-24.

Change Currency Attributes

You can change the functional or project currency attributes of multi-currency
transactions. When you select Change Functional Currency Attributes or Change Project
Currency Attributes from the Reports menu, a window is displayed where you can enter
changes in the following fields:

• Rate Type

• Rate Date

• Exchange Rate

The windows display the project or functional currency, depending on which currency
you have selected, as well as the transaction currency.

The same conditions apply to changes in currency attributes that apply during
transaction entry. See: Entering Currency Fields, page 2-17.

You can also change currency attributes for an expenditure using the Mass Adjustments
feature. When you select Change Functional Currency Attributes or Change Project
Currency Attributes under Mass Adjustments, most of the validations are performed by
the costing program. See: Mass Adjustment of Expenditures, page 2-50.

Note: If the project currency and the functional currency for an
expenditure item are the same, only the Function Currency Attributes
option is displayed on the Reports menu. Any changes you make to
the functional currency attribute are copied to the project currency
attributes.

Related Topics

Restrictions for Adjusting Converted Items, page 2-48

Project Statuses, Oracle Projects Implementation Guide

Transaction Sources, Oracle Projects Implementation Guide

Restrictions for Adjusting Converted Items

You can mark expenditure items as converted when you load expenditure items
from another system into Oracle Projects during conversion. To do this, you set the
CONVERTED_FLAG to Y (for Yes) in the PA_EXPENDITURE_ITEMS_ALL table.

Some adjustment actions are not permitted for converted items. The following table
shows which adjustment actions are and are not allowed for converted items.

2-48 Oracle Project Costing User Guide

Adjustment Action

Allowed for Converted Items

Correct Approved Expenditure Item

Allow Billing

Billable to Non-Billable

Non-Billable to Billable

Capitalizable to Non-Capitalizable

Non-Capitalizable to Capitalizable

Billing Hold

One-Time Hold

Release Hold

Recalculate Burden Cost

Recalculate Raw Cost

Recalculate Revenue

Recalculate Cost/Revenue

Change Comment

Split

Transfer

Work Type

YES

YES

NO

NO

NO

NO

YES

YES

YES

NO

NO

NO

NO

YES

NO

NO

NO

If an item is marked as converted, Oracle Projects assumes that the item does
not have all the data required to support the recalculation of cost, revenue, and
invoice. Therefore, you cannot perform the adjustment actions that may result in the
recalculation of cost, revenue, or invoices for converted items.

Note: Marking items as converted has a similar effect to enabling the
transaction source attribute that disallows adjustments on imported
transactions originating from that source.

Adjusting Expenditure Items

Use the Expenditure Items window to adjust project expenditure items.

To adjust expenditure items:

1. Navigate to the Find Project Expenditure Items or Find Expenditure Items

window. See: Viewing Expenditure Items, page 2-38.

2. Find the expenditure items you want to adjust.

Expenditures

2-49

3.

In the Expenditure Items window, choose the items you want to adjust. See: Selecting
Multiple Records, Oracle Applications User’s Guide. You can also use the Mass Adjust
feature to adjust items. See: Mass Adjustment of Expenditures, page 2-50.

4. Choose an option from the Tools menu or the Reports menu to specify how you

want to adjust the expenditure items.

The following table shows the adjustment options for each menu.

Menu

Tools

Reports

Selection

Billing Hold

Capitalizable

Change Comment

Non-Billable

Non-Capitalizable

One-Time Hold

Recalculate Burden Cost

Recalculate Cost/Revenue

Recalculate Raw Cost

Recalculate Revenue

Release HoldSplit

Transfer

Change Functional Currency Attributes

Change Project Currency Attributes

Change Transfer Price Currency Attributes

Mark for no Cross Charge Processing

Reprocess Cross Charge

For a description of adjustment options, see: Types of Expenditure Item
Adjustments, page 2-45.

5. Choose Run Request to select the Project Streamline Request process for the

adjustment. See: Processing Adjustments, page 2-57.

Mass Adjustment of Expenditures

Use the Find Expenditure Items window to process mass adjustment of expenditures.

You can optionally use the multi-select functionality in the Expenditure Items
window to perform adjustments on more than one expenditure. However, the mass
adjustment feature provides improved performance when you adjust a large number
of expenditures.

To perform mass adjustment of expenditures:

1. Navigate to the Find Project Expenditure Items or Expenditure Items

window. See: Viewing Expenditure Items, page 2-38.

2-50 Oracle Project Costing User Guide

2. Enter your search criteria. For example, if you want to make an identical adjustment
to all billable expenditures by a specific employee, enter the Employee Name field
and select Yes for Billable under the Billing Status fields.

3. Choose Mass Adjust.

4. From the Mass Adjust poplist, select the adjustment you want to perform on the

selected expenditures. When the adjustment process is complete, view the message
indicating the results of the process.

Transferring Expenditure Items

You can transfer an expenditure item from its current project or lowest task assignment
to another project or lowest task.

Run the Transfer Activity report to view the activity of expenditure items that you
transfer.

To transfer expenditure items:

1. Navigate to the Find Project Expenditure Items or Find Expenditure Items

window. See: Viewing Expenditure Items, page 2-38.

2. Find the expenditure items you want to transfer.

3.

In the Expenditure Items window, choose the items you want to
transfer. See: Selecting Multiple Records, Oracle Applications User’s Guide. You
can also use the Mass Adjust feature to adjust items. See: Mass Adjustment of
Expenditures, page 2-50.

4. Choose Transfer from the Tools menu.

5.

In the Transfer Items to Project/Task window, enter the Project Number and Task
Number to which you want to transfer the expenditure items.

6. Choose OK to mark the expenditure items for transfer.

7. Enter Yes if you want to re-query your expenditure items so you can see the new

expenditure items created from the transfer. Select the Search Criteria to use to
re-query the records.

8. Process the adjustments. See: Processing Adjustments, page 2-57.

Related Topics

New Expenditure Items Resulting from Transfer and Split, page 2-57

Splitting Expenditure Items

You can split an expenditure item to change its billing, capitalizable, and hold status for
a portion of the original item’s quantity.

When you split an expenditure item, you create a reversing entry for the original
expenditure item, and create two new expenditure items for that expenditure, totalling
the same quantity as the original item.

Note: You cannot split an original expenditure item that has already
been split or transferred. You can, however, split or transfer the new
expenditure items created from a split or transfer.

Expenditures

2-51

To split expenditure items:

1. Navigate to the Find Project Expenditure Items or Find Expenditure Items

window. See: Viewing Expenditure Items, page 2-38.

2. Find the expenditure items you want to split.

3.

In the Expenditure Items window, choose the items you want to split. See: Selecting
Multiple Records, Oracle Applications User’s Guide.

4. Choose Split from the Tools menu.

5.

In the Split Expenditure Item window, enter the Split Quantity/Raw Cost/Burdened
Cost that you want to allocate to the first item from the expenditure item you are
splitting.

The system prompts you to enter a quantity, raw cost, or burdened cost based
on what amounts are assigned to the original expenditure item, as shown in the
following table:

If the quantity is ...

and the raw cost is ...

then the amount split is ...

non-zero

zero

zero

non-zero

non-zero

zero

the quantity

the raw cost

the burdened cost

• Expenditure items with a zero quantity and a nonzero raw cost include costed

transactions imported via Transaction Import.

• Expenditure items with both quantity and raw cost equal to zero include burden

transactions imported via Transaction Import.

The system calculates the difference between the quantity or cost of the original
expenditure item and the quantity or cost you enter for the first item, and
displays the remaining amount as the quantity or cost of the second item.

6. Choose OK to mark the expenditure item to be split.

7. Enter Yes if you want to re-query your expenditure items to see the new expenditure
items created from the transfer. Select the Search Criteria to use to re-query the
records.

8. Process the adjustments. See: Processing Adjustments, page 2-57.

Related Topics

New Expenditure Items Resulting from Transfer and Split, page 2-57

Adjustments to Multi-Currency Transactions

When multi-currency transactions are adjusted, the system must determine currency
attributes for the transactions that result.

If the original item is not an imported, accounted item, the following rules apply:

• The original expenditure item is reversed, with all the same amounts and currency

attributes as the original item.

2-52 Oracle Project Costing User Guide

• The new expenditure items are created and treated as new transactions, following

the standard default logic for currency attributes.

Reversals and Splits

For reversals and splits, the reversing and new items have the same currency attributes
as the original transaction.

Transfers

For a transfer, the reversing item has the same currency attributes as the original
transaction. For the new item, the cost distribution program uses the conversion rules
for a new transaction, taking the default currency attributes from the destination
project. See: Converting Multiple Currencies, Oracle Projects Fundamentals.

Adjustments to Accounted Imported Transactions

Imported, accounted transactions can be adjusted in Oracle Projects only if
ALLOW_ADJUSTMENTS_FLAG is set to Y for the transaction source.

For imported multi-currency transactions that have been posted to GL by the feeder
system, adjustments are processed as shown below:

Note: For these adjustments, both the reversing transactions and their
cost distribution lines are created online.

Recalculation Adjustments

The cost distributed flag for the item is set to N, and the transaction is treated as
costed and burdened.

The cost distribution program recalculates project currency amounts. All other amounts
are copied from the original transaction.

The cost distribution program creates a reversing cost distribution line and a new
cost distribution line. Both lines will be interfaced to GL (their transfer status is set
to P (Pending)).

Transfers and Splits

Reversing items are created with the attributes of the original item.

Transfers: For the new item, all amounts and attributes are copied from the original
item, except for the project currency amounts. For the project currency amounts, the
cost distribution program uses the conversion rules for a new transaction, taking the
default currency attributes from the destination project. See: Converting Multiple
Currencies, Oracle Projects Fundamentals.

Splits: For new items, all currency amounts are prorated based on the split ratio.

Both reversing and new items create cost distribution lines that will be interfaced to GL
(their transfer status is set to P (Pending)).

Adjustments to Burden Transactions

You can perform adjustments on burden transactions that are not system-generated.

You can perform billing adjustments on burden transaction expenditure items that are
created by the Create and Distribute Burden Transactions process. For example, the

Expenditures

2-53

items can be placed on billing hold. To make any other type of adjustment on a
system-generated burden transaction, you must adjust the source expenditure item
related to these burden transactions.

You can adjust a burden transaction that is imported via Transaction Import only
if ALLOW_ADJUSTMENTS_FLAG is set to Y for the transaction source. For the
predefined transaction sources Inventory, Inventory Miscellaneous, and Work In
Process, ALLOW_ADJUSTMENTS_FLAG is set to N.

Adjustments to Related Transactions

Whenever an adjustment is performed on a source transaction that requires the item to
be backed out (transfer, split, manual reversal through the Pre-Approved Expenditure
form), Oracle Projects creates reversals for the related transactions of the source
transaction.

Oracle Projects creates related items via labor transaction extensions. See: Labor
Transaction Extensions, Oracle Projects APIs, Client Extensions, and Open Interfaces
Reference.

You cannot independently process related transactions from the source
transactions. However, there are adjustment actions for which related transactions are
processed with the source transaction.

You can transfer only the source transaction. When you transfer the source
transaction, Oracle Projects reverses the source transaction and the related
transactions, and creates only the new source transaction in the destination
project. Oracle Projects does not create related transactions in the destination project
because the related transactions may not be appropriate under the conditions of the
project.

You can create new related transactions using the labor transaction extension when the
transferred source transaction is cost-distributed.

You can split only the source transaction. When you split the source transaction, Oracle
Projects reverses the source transaction and the related transactions, and creates the two
new source transactions. Oracle Projects does not create related transactions in the
destination project because the related transactions may not be appropriate under the
conditions of the project.

You can create new related transactions using the labor transaction extension when the
new source transactions are cost-distributed.

Transfer

Split

Recalculate Cost/Revenue

You can mark only the source transaction for cost or revenue recalculation. However,
when you mark the source transaction, Oracle Projects automatically marks the related
transactions of the source transaction for recalculation.

Change Billable Status

You can change the billable status on both the source transaction and the related
transactions independently. However, a reclassification on a source transaction only

2-54 Oracle Project Costing User Guide

will not automatically result in the reclassification of related transactions since these
related transactions may have been created with a billable status independent of the
source transaction. For example, you may create the source transaction as billable and
the related transaction as non-billable.

Bill Hold/Release

You can perform bill holds and releases on both source transactions and related
transactions independently. However, an action performed on a source transaction will
not automatically result in the same action on the related transactions. For example, since
the transactions are treated independently, a bill hold on a source transaction will not
automatically place a bill hold on any related transactions.

Comment Change

You can change the comment on both the source transaction and the related transactions
independently.

Manual Reversal

You can reverse source transactions using the Expenditures form. When you reverse a
source transaction, Oracle Projects automatically reverses the related transactions. If
you delete the source transaction, Oracle Projects automatically deletes the related
transactions.

Reversal Using Transaction Import

You can reverse source transactions using Transaction Import. When you reverse a
source transaction, Oracle Projects automatically reverses the related transactions if the
transaction being loaded is an adjustment and the unmatched negative flag is set to No.

Work Type

You can change the work type on both the source transaction and related transactions
independently.

Marking Items for Adjustments

When you select an adjustment action, the expenditure items are marked for adjustment
processing. Most adjustment actions require additional processing to be completed.

The following table shows how each adjustment action marks expenditure items for
adjustment processing.

• The first eleven adjustment actions update the expenditure item with the values as

noted below for subsequent adjustment processing.

• The Change Comment adjustment action updates the comment and does not require

additional adjustment processing.

• The Split and Transfer adjustment actions create reversing and new items to be

processed.

Expenditures

2-55

Adjustment
Action

Cost
Distributed

Revenue
Distributed

Billable /
Capitalizable

Bill Hold

New Items
Created

No

Yes

No

Yes

Yes

Once

No

No

No

No

No

No

No

No

No

No

No

No

No

Billable to
Non-Billable

Non-Billable
to Billable

Capitalizable
to Non-
Capitalizable

Non-
Capitalizable
to
Capitalizable

Billing Hold

One-Time
Hold

Release Hold

Recalculate
Burden Cost

Recalculate
Raw Cost

Recalculate
Revenue

Recalculate
Cost/
Revenue

Change
Comment

Split

Transfer

Yes

Yes

Work Type

See Note

See Note

See Note

Note: If a work type change results in a change in the billable
status, then expenditure items are marked for adjustment processing
as required.

A billable reclassification requires an item to be re-costed so that the billable and
non-billable costs are correctly maintained in the project summarization tables, and
(optional) to change the assignment of the general ledger cost account. Also, if

2-56 Oracle Project Costing User Guide

you change from billable to non-billable, the assignment of the GL cost account in
AutoAccounting may change. The same is true for a capitalizable reclassification.

New Expenditure Items Resulting from Transfer and Split

When you transfer or split an item, the original item is reversed and new items are
created automatically by Oracle Projects. These items are similar to the items that you
create manually when you correct an approved expenditure item.

Transfer Example

Split Example

The following table shows an example of an original item (Item 1) and the new items
(Items 2 and 3) resulting from the transfer of an item from project TM1 to project
SF1, task 2.

Item
Number

Item
Reversed

Expenditure
Item Date

Expenditure
Type

Project

Task

Quantity Billable

1

2

3

01-JAN-96

Professional TM1

1

01-JAN-96

Professional TM1

01-JAN-96

Professional

SF1

1

1

2

10

-10

10

Yes

Yes

Yes

Note: The billable status of Item 3 is determined from the billable status
of the project and task to which it is transferred.

The following table shows an example of an original item (Item 1) and the new items
(Items 2 through 4) resulting from the split of an item on the same project and task. The
original item had 10 billable hours, which are split into 6 billable hours and 4 non-billable
hours. When you split an item, you specify the billable status and bill hold status
of each of the two new items.

Item
Number

Item
Reversed

Expenditure
Item Date

Expenditure
Type

Project Task

Quantity Billable

1

2

3

4

01-JAN-96

Professional

TM1

1

01-JAN-96

Professional

TM1

01-JAN-96

Professional

TM1

01-JAN-96

Professional

TM1

1

1

1

1

10

-10

6

4

Yes

Yes

Yes

No

Processing Adjustments

After you have performed the adjustment actions, you need to run the appropriate
processes to process the adjustments.

The following table shows which processes to run for each adjustment action.

Expenditures

2-57

Distribute Costs Generate Asset

Adjustment
Action

Correct
Approved
Expenditure Item

Billable to Non-
Billable

Non-Billable to
Billable

Capitalizable
to Non-
Capitalizable

Non-
Capitalizable to
Capitalizable

Billing Hold

One-Time Hold

Release Hold

Recalculate
Burden Cost

Recalculate Raw
Cost

Recalculate
Revenue

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Recalculate
Cost/Revenue

Yes

Change
Comment

Split

Transfer

Yes

Yes

Lines

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Generate Draft
Revenue

Generate Draft
Invoices

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Work Type

See Note

See Note

See Note

Note: If a work type change results in a change in the billable status, then
you must run the appropriate processes to process this change.

You can use the Submit Request window to run the appropriate the processes for your
project only.

2-58 Oracle Project Costing User Guide

You can also mark items for adjustment and allow the items to be processed
automatically the next time you run the processes to distribute costs, generate asset
lines, and generate draft revenue and invoices.

Related Topics

Submitting Requests, Oracle Projects Fundamentals

Results of Adjustment Processing

After you run the appropriate processes to recalculate the adjusted expenditure
items, you can review the results of the adjustments.

Cost Adjustments

• Raw cost amount

• Burden cost amount

• Account to which the cost is charged

• Billable/Capitalizable status of the item

When the Distribute Costs program encounters an item requiring a cost adjustment, the
program updates the expenditure item with the new raw and burden cost rates and
amounts, and creates new cost distribution lines. The program creates a reversing cost
distribution line and a new cost distribution line. These lines form the audit trail of
cost adjustments.

The following table shows an example of cost distribution lines for an expenditure item
that was re-costed due to a cost rate change in a subsequent month. Lines 2 and 3 are
new lines resulting from the cost adjustment. Line 2 reverses the same amount and
account as Line 1. Line 3 uses the new cost multiplier and account based on current
AutoAccounting rules.

Line
Number

Line
Reversed

Amount

Quantity

Billable

Account

GL Date

1

2

3

1

100

-100

200

10

-10

10

Yes

Yes

Yes

04.401.4100

31-JAN-94

04.401.4100

28-FEB-94

04.401.4100

28-FEB-94

You can review these distribution lines in the Cost Distribution Lines window.

Corrections to Approved Items, Transfers, and Splits

When processing a reversing item which resulted from a correction of an approved
expenditure item, a transfer, or a split, the Distribute Costs program uses the same
cost rate used by the original item to ensure that the cost nets to zero for the original
and reversing item. The reversing item is charged to an account based on the current
AutoAccounting rules.

The new positive item resulting from a transfer is processed just as a new expenditure
item is processed; no special adjustment processing is performed. But to process a

Expenditures

2-59

correction of an approved expenditure item or a split just as a new expenditure item is
processed, it has to be marked for recalculation.

Interfacing Adjustments to General Ledger and Payables

The Interface process will send lines 2 and 3 (shown in the table above) to Oracle General
Ledger or Oracle Payables to reflect the cost adjustment originating in Oracle Projects.

The cost adjustment lines are posted to the earliest open or future GL period. See
also: Date Processing in Oracle Projects, Oracle Projects Fundamentals.

Note: Lines 2 and 3 are posted to a new GL period of February 1994
since the original GL period of January 1994 was closed when the
cost adjustment occurred.

Revenue Adjustments

When the Generate Draft Revenue program encounters a item requiring a revenue
adjustment, the program updates the expenditure item with the new revenue
amount, and creates new revenue distribution lines. The program creates a reversing
and new revenue distribution lines, which records the audit trail of revenue adjustments.

The following table shows an example of revenue distribution lines for an expenditure
item with a revenue adjustment caused by a change in a bill rate in a subsequent
month. Lines 2 and 3 are new lines resulting from the revenue adjustment. Line 2
reverses the same amount and account as Line 1. Line 3 has the new revenue amount
based on the new bill rate/markup and the account based on current AutoAccounting
rules.

Line
Number

Line
Reversed

Amount

Account

Draft
Revenue
Number

Transfer
Status

GL Date

1

2

3

1

100

-100

200

04.401.3100

04.401.3100

04.401.3100

1

2

3

Accepted

31-JAN-96

Pending

28-FEB-96

Pending

28-FEB-96

Each revenue distribution line is grouped into a draft revenue. A draft revenue may
credit another draft revenue. Line 2 above is grouped into Draft Revenue 2, which credits
Draft Revenue 1, in which Line 1 is grouped. Line 3 is included on a new draft revenue 3.

You can review these distribution lines in the Revenue Distribution Lines window. You
also can view the distribution lines in the Revenue Line Details window accessed from
the Revenue Review window.

Transfers, Splits, and Corrections to Approved Items

When processing a reversing item which resulted from a correction of an approved
expenditure item, a transfer, or a split, the Generate Draft Revenue program reverses
the revenue of the original item to ensure that the revenue nets to zero for the original
and reversing item. The reversing item is charged to a revenue account based on the
original distribution line.

2-60 Oracle Project Costing User Guide

The new positive item resulting from a correction of an approved expenditure item, a
transfer, or a split are processed just as a new expenditure item is processed; no special
adjustment processing is performed on these items.

Interfacing Adjustments to Oracle General Ledger

The Interface Revenue to General Ledger process will send lines 2 and 3 (shown in the
previous table) to Oracle General Ledger to reflect the revenue adjustment originating
in Oracle Projects.

The revenue adjustment lines are posted to the earliest open or future GL period. See
also: Date Processing in Oracle Projects, Oracle Projects Fundamentals.

Note: Lines 2 and 3 are posted to a new GL period of February 1994
since the original GL period of January 1994 was closed when the
revenue adjustment occurred.

Invoice Adjustments

The Generate Draft Invoice program compares the bill amount on the item’s revenue
distribution lines to determine if the item needs to be adjusted. When program
encounters a item requiring a invoice adjustment, it creates a crediting invoice and a
new invoice.

The following table shows an example of invoices created for the items shown in the
table above. Assume the project’s invoices only bill the one item and that the item was
originally billed on Invoice 1 in January. Invoices 2 and 3 are new invoices resulting
from the invoice adjustment.

Invoice Number

Invoice Credited Amount

Transfer Status GL Date

1

2

3

1

100

-100

200

Accepted

31-JAN-96

Pending

28-FEB-96

Pending

28-FEB-96

You can review these invoices in the Invoice Summary window in the Invoice Review
window.

Transfers, Splits, and Corrections to Approved Items

When processing a reversing item which resulted from a correction of an approved
expenditure item, a transfer, or a split, the Generate Draft Invoice program credits the
invoice on which the original item was billed.

The new positive item resulting from a correction of an approved expenditure item, a
transfer, or a split are processed just as a new expenditure item is processed; no special
adjustment processing is performed on these items.

Interfacing Adjustments to Oracle Receivables

The Interface Invoices to Receivables process will send invoices 2 and 3 (shown in
the previous table) to Oracle Receivables.

Expenditures

2-61

The invoices are posted to the open or future GL period in which the invoice date falls
in Oracle Receivables.

Note: Lines 2 and 3 are posted to a new GL period of February 1994
since the original GL period of January 1994 was closed when the
invoice adjustment occurred.

Refer to the following essay regarding how a credit memo is interfaced to Oracle
Receivables, if the outstanding balance is less than the credit memo amount.

Related Topics

Integrating with Oracle Receivables, Oracle Project Billing User Guide

Adjustments to Supplier Invoices

You can perform a number of adjustments to supplier invoices in Oracle Projects and
Oracle Payables. In Oracle Projects, you can perform the following adjustments on a
supplier invoice:

• Transfer an item to another project or task

• Split an item

• Reclassify an item’s billable or capitalizable status

In Oracle Payables, you can adjust the following items on a project-related supplier
invoice:

• Invoice amount

• Supplier

• Expenditure type

Example of an Adjustment to a Supplier Invoice

In the example shown in the following table, Item 1 represents an original invoice for
$100 that is entered in Oracle Payables. The invoice includes one invoice distribution
line charged to project A that is interfaced to Oracle Projects. An Oracle Projects project
manager transfers the item from project A to project B, resulting in a net zero difference
accounting transaction. The adjusting transactions, Item 2 and Item 3, are interfaced
to Oracle Payables and attached to the original invoice. Oracle Projects provides the
amount, the accounts, and the GL date to which the transactions are to be posted.

Item

Project

Amount

Account

Comment

1

2

3

A

A

B

2-62 Oracle Project Costing User Guide

100

-100

01.101.5200

Entered in AP

01.101.5200

100

02.201.5200

Created in PA
and interfaced
to AP via the
transfer process

Adjusted in PA
and interfaced
to AP via the
transfer process

To process supplier invoice adjustments from Oracle Projects to Oracle Payables:
1. Perform the adjustment in Oracle Projects.

2. Process the adjustment by running the PRC: Distribute Supplier Invoice Adjustment
Costs process, or you can submit the streamline process Distribute and Interface
Supplier Invoice Adjustments to Payables. If you run the streamline process, you
can skip Step 3.

3.

Interface the supplier invoice adjustments to Oracle Payables using the
PRC: Interface Supplier Invoice Adjustment Costs to Payables process.

Note: All new invoice lines created from the adjustment are
linked to the originating invoice in Oracle Payables. This allows
you to reconcile all project-related supplier invoices in Oracle
Payables, and accurately account for your cash books if you use
Cash Basis Accounting.

4. Run AutoApproval in Oracle Payables to approve the new invoice distribution lines.

5. Post the supplier invoices from Oracle Payables to Oracle General Ledger.

To process supplier invoice adjustments from Oracle Payables to Oracle Projects:
1. Perform the adjustment in Oracle Payables.

Related Topics

2. Run AutoApproval in Oracle Payables to approve the new invoice distribution lines.

3. Post the supplier invoices from Oracle Payables to Oracle General Ledger.

4.

Send the adjustment to Oracle Projects using the Oracle Projects PRC: Interface
Supplier Costs process.

Note: Before interfacing adjustments to Oracle Projects, the process
checks whether the original and adjusting invoice items net to
zero. If so, then neither item is transferred to Oracle Projects.

Adjusting Project-Related Documents in Oracle Purchasing, Oracle Payables, and Oracle
Projects, page 7-28

Restrictions to Supplier Costs Adjustments, page 7-30

Distribute Supplier Invoice Adjustment Costs, Oracle Projects Fundamentals

Interface Supplier Invoice Adjustment Costs to Payables, Oracle Projects Fundamentals

Submitting Streamline Processes, Oracle Project Fundamentals

Interface Supplier Costs, Oracle Project Fundamentals

Invoice Validation, Oracle Payables User Guide

Payables Transfer to General Ledger Program, Oracle Payables User Guide

Expenditures

2-63

3
Burdening

This chapter describes how to use burdening in Oracle Projects.

This chapter covers the following topics:

• Overview of Burdening

• Building Up Costs

• Using Burden Structures

• Using Burden Schedules

• Assigning Burden Schedules

• Storing, Accounting, and Viewing Burden Costs

• Reporting Requirements for Project Burdening

Overview of Burdening

Burdening (also known as cost plus processing) is a method of calculating burden costs
by applying one or more burden cost components to the raw cost amount of each
individual transaction. You can then review the raw cost and total burdened cost (the
sum of raw cost and burden cost) of each transaction.

Oracle Projects displays the raw cost and burdened cost in expenditure inquiry
windows, and shows the cost of each detail transaction in reports. You can choose
to account for the individual burden cost components to either track the overhead
absorption or to account for the total burdened costs. You can write custom reports using
standard views to report all burden cost components for each detail transaction.

Using burdening, you can perform internal costing, revenue accrual, and billing for
any type of burdened costs that your company applies to raw costs. Oracle Projects
calculates costs using the following formulas. (The formulas for cost also apply to
revenue and billing amounts.)

Oracle Projects calculates burden cost by multiplying raw cost by a burden
multiplier. This calculation is represented in the following formula:

Burden Cost = Raw Cost x Burden Multiplier

Oracle Projects calculates total burdened cost by adding burden cost to the raw cost
amount. This calculation is represented in the following formula:

Total Burdened Cost = Raw Cost + Burden Cost

Burdening

3-1

You use the burden multiplier to derive the total amount of the burden cost. For
example, you may burden the raw cost of labor using a multiplier of thirty percent to
derive the fringe component, and in turn, compute the total burdened cost of labor as
shown in the following table:

Cost Component

Labor (raw cost)

Add: Fringe at 30% (burden cost)

Total Burdened Cost

Amount

1,000

300

1,300

On a project for which costs are burdened, you can create some transactions that are
burdened and others that are not burdened. You define which projects should be
burdened by setting the Burden Cost indicator for each project type in the Project Types
window. When you specify that a project type is burdened, you must then specify the
burden schedule to be used. The burden schedule stores the rates and indicates which
transactions are burdened, based on cost bases defined in the burden structure. You
specify which expenditure types are included in each cost base. With burdening, you
can use an unlimited number of burden cost codes, easily revise burden schedules, and
retroactively adjust multipliers. You can define different multipliers for costing, revenue
accrual, and billing.

Burden Calculation Process

The following illustration shows the burden calculation process.

3-2 Oracle Project Costing User Guide

Burden Calculation Process

As shown in the illustration Burden Calculation Process, page 3- 3 , the calculation of
burden cost includes the following processing decision logic and calculations:

1. Expenditure items with a raw cost amount are selected for processing.

2. The process determines if the related project type of the expenditure item is defined

for burdening.

3.

If Yes (the project type is defined for burdening), then the process determines the
burden schedule to be used.

Burdening

3-3

4.

If No (the project type is not defined for burdening), then the item is not
burdened. The process assumes the burden multiplier is zero (burden cost is
zero, thus burdened cost equals raw cost).

5. To determine which burden multiplier to use, the process determines if there is a

burden schedule override for the expenditure:

6. The process uses the task burden schedule override on the associated task, if such an

override exists.

7.

8.

If no task burden schedule override exists on the associated task, then the process
uses the project burden schedule override on the associated project.

If there are no burden schedule overrides, the process determines which standard
burden schedule to use for burden cost calculations in the following order:

9.

Standard task burden schedule

10. Standard project burden schedule

11. After a schedule has been determined, the process verifies that the expenditure
item’s expenditure type is found in any of the cost bases of the selected burden
schedule revision.

12. If an expenditure type is excluded from all cost bases in the burden structure, then
the expenditure items that use that expenditure type are not burdened (burden cost
equals zero, thus burdened cost equals raw cost).

13. Otherwise, burden multipliers from the appropriate burden schedule revision are

used. If a schedule ID override exists, the process uses that revision.

14. The system calculates burden cost and total burdened cost amounts according

to the following calculation formulas:

15. burden cost equals raw cost multiplied by a burden multiplier

16. total burdened cost equals the sum of raw cost and burden cost

Building Up Costs

The objective of burdening is to provide you with a buildup of raw and burden costs, so
you can accurately represent the total cost of doing business. You can choose to calculate
total burdened costs as a buildup of costs using a precedence of multipliers. Taking the
raw cost, Oracle Projects performs a buildup of burden costs on top of raw costs to
provide you with a true representation of costs. You provide the multiplier that is used
to calculate the cost. The buildup is performed for each detailed transaction.

Example of Cost Buildup

The following table provides an example of how Oracle Projects calculates total
burdened cost as a buildup of raw and burden costs.

3-4 Oracle Project Costing User Guide

Reference

Cost Amount

Formula

Cost Type

Labor (raw cost)

Overhead at 95% (burden cost)

Total Labor (total burdened cost)

Materials (raw cost)

(A)

(B)

(C)

(D)

Material Handling at 15% (burden cost)

(E)

Total Materials (total burdened cost)

Total Labor and Materials (total
burdened cost)

General and Administrative at 15%
(burden cost)

Total Burdened Cost (total burdened
cost)

(F)

(G)

(H)

(I)

1,000.00

950.00

1,950.00

500.00

75.00

575.00

2,525.00

.95 A

A + B

.15 D

D + E

C + F

378.75

.15 G

2,903.75

G + H

In this example, raw costs are categorized by the Labor and Materials cost bases. Each
raw cost has one or more types of burden cost applied to it to derive the total burdened
cost amount.

The first-tier multipliers are applied to the raw costs of each cost base. For labor, the
first-tier multiplier is for Overhead. For materials, the first-tier multiplier is for Material
Handling costs.

The second-tier multiplier is then applied to the sum of the raw cost and the first-tier
burden cost amount for each cost base. In the example in the table, the second tier
multiplier for General and Administrative is applied to the total raw and burden costs
for Labor and Materials.

The cost buildup in this example is calculated as follows:

• First, the raw labor cost of $1,000 is burdened by overhead at a multiplier of 95
percent, resulting in a burden cost of $950 and a total labor cost of $1,950.

• Then, the general and administrative multiplier of 15% is applied against the total

labor cost of $1,950, for a total of $292.50 of general and administrative cost. The
total burdened labor cost is the sum of $1,950 plus $292.50, or $2,242.50.

• Next, the raw materials cost of $500 is burdened by material handling at a multiplier
of 15 percent, resulting in a burden cost of $75 and a total materials cost of $575.

• Finally, the general and administrative multiplier of 15% is applied to the total of the
buildup of burdened Materials cost, yielding $86.25, resulting in a total burdened
Material cost amount of $ 661.25.

The following illustration shows the flow of the cost buildup calculations in the table
above.

Burdening

3-5

Cost Buildup Flow

The illustration Cost Buildup Flow, page 3- 6 illustrates the following cost buildup steps:

1. Overhead is applied to the raw labor cost.

2. Material handling is applied to the raw materials cost.

3. General and administrative is then applied to the buildup of the total burdened costs

for Labor and Materials to derive the total burdened cost amount.

Using Burden Structures

You define the cost buildup using a burden structure. A burden structure determines
how cost bases are grouped and establishes the method of applying burden costs to raw
costs. Expenditure types classify raw costs, and burden cost codes classify burden
costs. The relationship between expenditure types and burden cost codes within cost
bases determines what burden costs are applied to specific raw costs, and the order in
which they are applied.

Note: To account for burden cost codes separately, you
also define unique expenditure types to link to burden cost
codes. See: Storing, Accounting, and Viewing Burden Costs, page 3-15.

Your company may have several different burden structures for unique business
requirements. For example, you may use a different structure for internal costing than
you use for government billing.

Note: If you change your burden structure and subsequently transfer an
expenditure item burdened with the old structure, then the reversed

3-6 Oracle Project Costing User Guide

amount and the amount charged to the new task each equals the
original burdened amount.

The following illustration shows the components of a burden structure.

Components of a Burden Structure

The illustration Components of a Burden Structure, page 3- 7 shows a burden structure
with the following cost bases:

• The Labor cost base:

• includes the expenditure types Professional, Clerical, and Administrative.

• is assigned the burden cost codes Fringe, Overhead, and General and Administrative

(G&A).

• The Material cost base:

• includes the expenditure types Supplies and Construction Materials.

• is assigned the burden cost codes Material Handling and General and

Administrative (G&A).

• The Expense cost base:

• includes the expenditure types Travel and Meals.

• is assigned the burden cost code General and Administrative (G&A).

Related Topics

Burden Structures, Oracle Projects Implementation Guide

Burden Structure Components

A burden cost code represents the type of burden costs you want to apply to raw costs. For
each burden cost code in the burden structure, you specify what cost base it is applied
to, the expenditure type or types it is linked to, and the order in which it is applied to
raw costs within the cost base.

Burdening

3-7

You burden a type of cost with burden costs to obtain a more accurate representation
of your company’s operating costs. For example, each hour of employee time costed
directly to a project may be supported by burden costs for benefits and office space.

You specify which costs are burdened through the definition of cost bases. A cost base
is a grouping of raw costs to which you apply burden costs. A cost base assignment
consists of expenditure types. You specify the types of transactions that constitute
the cost base when you assign expenditure types to the cost base. These expenditure
types assignments represent the raw costs to which you apply the burden costs of the
cost base. If you exclude an expenditure type from all cost bases in a structure, the
expenditure items that use that expenditure type will not be burdened (burden cost
equals zero, thus burdened cost equals raw cost).

If you want to burden transactions using a new expenditure type, you must add the
expenditure type to the appropriate burden structures. You should do this before you
enter transactions using this expenditure type. This will ensure that all transactions
using this expenditure type are burdened. If you have charged transactions using this
expenditure type before you added the expenditure type to the appropriate burden
structures, you must mark these transactions to be reprocessed to burden the costs.

Cost bases also consist of burden cost codes. While the expenditure types represent
the raw costs, the burden cost codes represent the burden costs that support the raw
costs. Cost bases may be different within the context of different burden structures. For
example, you may use a different definition of a labor cost base in a billing schedule than
you would use in an internal costing schedule.

You also assign an expenditure type to each burden cost code. You may use any
expenditure type that has been defined with the Burden Transaction expenditure type
class or, if you want to account for the burden cost components in the GL or budget by
burden cost component, you can define an expenditure type with the same name as
the burden cost code.

In summary, cost bases are comprised of expenditure types and burden cost
codes. Expenditure types represent the raw costs, and burden cost codes represent the
burden costs that support the raw costs. Cost bases may be different within the context
of different burden structures. For example, you may use a different definition of a labor
cost base in a billing schedule than you would use in an internal costing schedule.

An expenditure type classifies each detailed transaction according to the type of raw
cost incurred.

A burden structure can be additive or precedence based. If you have multiple burden
cost codes, an additive burden structure applies each burden cost code to the raw
costs in the appropriate cost base. A precedence burden structure is cumulative and
applies each cost code to the running total of the raw costs, burdened with all previous
cost codes. The examples in the following two tables illustrate how different burden
structures using the same cost codes can result in different total burdened costs.

The following table shows the calculation of total burdened cost using the additive
burden structure.

3-8 Oracle Project Costing User Guide

Cost Type

Labor (A)

Overhead at 95% (B)

Fringe at 25% (C)

General and Administrative at 15% (D)

Total Burdened Cost

Cost Amount

Formula

100.00

95.00

25.00

15.00

235.00

.95 A

.25 A

.15 A

A + B + C + D

The following table shows the calculation of total burdened cost using the precedence
burden structure.

Cost Type

Labor (A)

Overhead at 95% (B)

Fringe at 25% (C)

General and Administrative at 15% (D)

Total Burdened Cost

Cost Amount

Formula

100.00

95.00

48.75

36.56

280.31

.95 A

.25 (A + B)

.15 (A + B + C)

A + B + C + D

Note: The order of the burden cost codes has no effect on the total
burdened cost with either additive or precedence burden structures.

Related Topics

Example of Cost Buildup, page 3- 4

Cost Bases and Cost Base Types, Oracle Projects Implementation Guide

Burden Cost Codes, Oracle Projects Implementation Guide

Using Burden Schedules

Burden schedules establish the multipliers used to calculate the burdened
cost, revenue, or bill amount of each expenditure item charged to a project. You can
define different burden schedules for use in internal costing, revenue accrual, and
invoicing. When you define burden schedules, you specify the burden structure
on which the schedule is based.

You can use both burden schedules and bill rate schedules within a project to accrue
revenue and invoice. You can also use a bill rate schedule for non-labor expenditure
items, and use a burden schedule for labor expenditure items.

You specify default burden schedules for each project type. You can use different
schedules for different types of projects. You can override the default burden schedules
for each project by using a schedule of multipliers negotiated for the project or task.

Burdening

3-9

Types of Burden Schedules

There are two types of schedules you can use in Oracle Projects: firm and provisional.

Use firm schedules if you do not expect your multipliers to change. Generally, firm
schedules are used for internal costing or commercial billing schedules.

Because burden multipliers may not always be known at the time that you are calculating
total burdened costs, you use interim, or provisional multipliers. Provisional multipliers
are generally estimates based on a company’s forecast budget for the year based on the
previous year’s results. When you determine the actual multipliers that apply to costs
(after the multipliers are audited), then you replace the provisional multipliers with the
actual multipliers. Oracle Projects processes the adjustments from provisional to actual
changes for costing, revenue, and billing.

Defining Burden Schedule Versions

You define schedule versions for a burden schedule to record the date range within
which multipliers are effective. You can have an unlimited number of versions for each
burden schedule, but use one active version at a given point in time. However, after you
apply actuals, you can have one active provisional version and one active actual version
existing at the same time within a schedule.

In addition, you may have a number of versions for each quarter of the fiscal year in
which your company does business, especially for government billing projects. At the
end of the year, when the government audits your burden multipliers, you create a new
version that reflects the actual billing rates. The following illustrations shows and
example of the use of schedule versions.

Burden Schedule Versions

In the illustration Burden Schedule Versions, page 3-10, a company defines provisional
burden schedules on a quarterly basis, based on a forecast of budgeted costs. Each
quarter, the company creates a new version of the burden schedule to reflect updates in
the budget. At the end of the fiscal year, when the company is audited, actual multipliers
are applied which reflect the true burdened cost of affected items.

3-10 Oracle Project Costing User Guide

Related Topics

Applying Actuals, Oracle Projects Implementation Guide

Burden Calculation Process, page 3- 2

Assigning Burden Multipliers

When you create burden schedules, you assign a multiplier to an organization and
burden cost code. The multiplier specifies the amount by which to multiply the raw
cost to obtain the burden cost amount.

When you compile a burden schedule version, Oracle Projects calculates and stores the
multipliers for each organization and burden cost code in a schedule version. Additional
information stored includes compiled multipliers, which allow Oracle Projects to quickly
determine burden cost amounts based on the burden multipliers used for a particular
organization as of a particular date.

Instead of performing a buildup of costs each time you calculate burden amounts, Oracle
Projects uses the compiled multipliers to multiply the compiled multiplier by the raw
cost to determine each burden cost component.

The following table shows an example of the multipliers a company uses to determine
the burden cost amounts for labor during cost calculation.

Organization

Burden Cost Code

Multiplier

Headquarters

Headquarters

Fringe

Overhead

Headquarters

General and Administrative

Los Angeles

General and Administrative

.35 .95

.15 .20

Suggestion for Organizations that Have No Burden

You may need to set up special procedures for organizations that have no burden. For
example, your company may use contractors that do not have a particular type of burden
cost (such as fringe) applied to their raw cost. To implement this scenario, you can first
set up a new organization for contractors. Then, create a zero burden cost amount
by assigning that organization to the burden schedule and using a multiplier of zero
for the burden cost of Fringe. Each time that burden cost for Fringe is calculated for
the contractor’s organization, Oracle Projects will multiply the contractor’s raw cost
multiplier by zero, resulting in a burden cost amount of zero, which reflects the true
representation of the raw cost and burden multipliers.

Burden Multiplier Hierarchy

Effective multipliers cascade down the Project Burdening Hierarchy, starting
with the parent organization. If Oracle Projects finds a level in the hierarchy that
does not have a multiplier defined, it uses the multipliers entered for the parent
organization. Therefore, an organization multiplier schedule hierarchy is really a
hierarchy of exceptions; you define only the multipliers for an organization if they
override the multipliers of its parent organization.

Burdening

3-11

The following illustration shows an example of how multipliers are assigned for a
multi-level organization.

Assigning Multipliers to Organizations

In the illustration Assigning Multipliers to Organizations, page 3-12, the parent
organization, Headquarters (HQ), has two defined multipliers: Overhead (OH) with a
multiplier of 2.0, and General and Administrative (G & A) with a multiplier of 3.0.

• When Oracle Projects processes transactions for the East organization, no

multipliers are found. Therefore, the system assigns the multipliers from the parent
organization, Headquarters. However, when Oracle Projects looks for multipliers
for the Boston and New York (NYC) organizations, a multiplier of 3.1 for General
and Administrative is found for each organization. Therefore, the system uses the
General and Administrative multiplier of 3.1 from these organizations.

• When Oracle Projects processes transactions for the West organization, the multiplier
of 2.3 for Overhead from the West organization overrides the multiplier of 2.0 from
its parent organization, Headquarters. Since no multiplier is found for General and
Administrative, the system assigns the multiplier of 3.0 from the Headquarters
organization. No multipliers are found for the San Francisco (SF) and Los Angeles
(LA) organizations. Therefore, Oracle Projects, assigns the multipliers from their
parent organization, West.

Suggestion for Burdening a Borrowed or Lent Resource

When lending a resource to another organization for a specific project, you may want to
burden the resource using the borrowing organization’s multipliers.

For example, the Los Angeles organization lends a resource to the New York City
organization, and it is agreed that the borrowed resource is to be burdened using
the New York City multipliers. For burdening, Oracle Projects uses the destination
organization of an organization distribution override, in place of the expenditure
organization, if an organization distribution override exists. If you want the project to
have the New York City burden multipliers use burdened costs of the borrowed resource
from Los Angeles, then enter an organization distribution override with a source
organization of Los Angeles and a destination organization of New York City.

3-12 Oracle Project Costing User Guide

Related Topics

Organization Overrides, Oracle Projects Fundamentals

Assigning Burden Schedules

You can assign burden schedules to project types, projects, and tasks. When you assign
schedules to a project type, the schedules are the default schedules for projects and tasks
that use the project type. Assigning burden schedules to project types allows you to
implement company policies; for example, you can implement a policy that requires
all projects of a particular project type to maintain the same multipliers for internal
costing purposes.

You can change the default schedule for a project or task. You can also override default
schedules at the project and task level by using burden schedule overrides. Burden
schedule overrides generally reflect multipliers that have been negotiated specifically
for a particular project or task.

Defining Burden Schedules for Project Types

You define default standard burden schedules for each project type. These schedules
default to each project defined with that project type. You can override the default
schedules at the project and task level. See: Project Types, Oracle Projects Implementation
Guide.

Assigning Burden Schedules at the Project and Task Level

When you assign a project type to a new project, Oracle Projects automatically provides
default burden schedules from the project type. These schedules are also the default
schedules for each top task added to the project, and schedules for a top task are the
default schedules for lower level tasks.

The schedules used for burdening and billing are those assigned to the lowest task.

Note: When you change the burden schedule assignment for a project
that already has tasks set up, the schedules assigned to tasks that already
exist do not automatically change. You may need to review schedules
for the existing WBS to make sure they are correct.

Related Topics

Costing Burden Schedules, Oracle Projects Fundamentals

Assigning Fixed Dates for Burden Schedules

You can assign fixed dates for each of your burden schedules, just as you can for bill
rate schedules. You can assign fixed dates only to firm schedules. You cannot use
fixed dates with provisional schedules.

The fixed date specifies the date for determining the schedule revision to use in
calculations, regardless of the expenditure item date.

You enter a fixed date for a cost burden schedule only if the project type definition allows
you to override the cost burden schedule.

You can enter schedule fixed dates for standard burden schedules only. Schedule fixed
dates are not used for burden schedule overrides.

Burdening

3-13

Changing Default Burden Schedules

You can change the default burden schedules for a project or task.

If you change the burden schedule for a lowest level task that has items processed, then
the items are not automatically marked for reprocessing. Only new items charged to
the task will use the new burden schedule. You can mark the items for recalculation in
the Expenditure Inquiry window. This will cause the items to be reprocessed using the
new burden schedule assigned to the task.

• Changing Cost Burden Schedule

You can override the cost burden schedule if the project type definition allows you to
override the cost burden schedule, and the project is burdened.

• Changing Revenue or Invoice Burden Schedule

You can change the revenue or invoice burden schedule within a schedule type
at any time.

• Changing the Type of Revenue or Invoice Burden Schedule Used

You can change the burden schedule type of any task or project at any time. You
may change a task from a burden schedule type of Bill Rate to Burden, even after
you have defined bill rate overrides. These bill rate overrides will not be used in
processing. You can also define burden schedule overrides and then change your
task to use a bill rate schedule. The burden schedule overrides will not be used.

Overriding Burden Schedules

You can define burden schedules at the project level to override the default burden
schedules from the project type. You can also define burden schedules at the task level to
override the default schedules from the project and project type.

• Defining Burden Schedule Overrides

You can define a schedule of negotiated burden multipliers for your projects and tasks
which overrides the schedule that you assigned to the project and tasks. When you
define burden schedule overrides, you cannot override just one multiplier for the
standard schedule; you need to define an entire schedule for the project or task that
overrides the standard burden schedule.

Defining burden schedule overrides is similar to defining burden schedules. You
specify the revisions and the associated multipliers. The revisions are created as
firm revisions. You cannot apply actuals to provisional multipliers with burden
schedule overrides. You can select only burden structures that are allowed for use in
burden schedule overrides.

The burden schedule overrides that you define are created as burden schedules in
Oracle Projects. You must compile schedule revisions as you do with standard
burden schedules.

Important: You do not define override multipliers by
organization. The multipliers that you define are used for all
items, regardless of the organization.

• Assigning Burden Schedule Overrides

You can enter override burden schedules for a project or task in the Project, Templates
window or the Tasks window.

3-14 Oracle Project Costing User Guide

The burden schedule override option is available only if the project is burdened
and the project type allows override of the cost schedule. You can also choose this
option if the schedule type for labor or non-labor is Burden, if you want to allow
overrides of revenue and invoice schedules.

• Adjusting Burden Schedule Overrides

You can correct, adjust, and create new revisions for your burden schedule override
as you do for standard burden schedules.

Determining Which Burden Schedule to Use

The costing and revenue programs in Oracle Projects determine the effective burden
schedule to use for burden cost calculations in the following order:

• Task-level burden schedule override

• Project-level burden schedule override

• Task standard burden schedule

Oracle Projects uses the first schedule it finds to process all items charged to that task.

Distribute Costs and Interface Supplier Invoices from Payables

The Distribute Costs programs and the Interface Supplier Invoices from Payables
program use the overrides and schedules to burden transactions charged to projects that
are defined to be burdened for internal costing based on the project type definition. These
programs calculate the burdened cost for all transactions on these projects.

Related Topics

Burden Calculation Process, page 3- 2

Storing, Accounting, and Viewing Burden Costs

You can choose how you want to store, account, and view burden costs for individual
expenditure items, using one of the following methods:

• Burden cost on the same expenditure item, page 3-15

• Burden cost as a separate, summarized expenditure item on the same project, page

3-17

• Burden cost as summarized expenditure items on a separate project, page 3-18

You decide how to store the burden costs based on your requirements for budgeting and
reporting burden costs. You specify the method for each burdened project type that you
define. See: Choosing a Burden Storage Method, page 3-19.

To define a burdened project type, you enable the Burdened check box in the Costing
Information region of the Project Types window. Oracle Projects then displays
the Burden Cost Display and Accounting region, where you enter all burden cost
information. See: Project Types, Oracle Projects Implementation Guide.

Storing Burden Cost on the Same Expenditure Item

You can choose to store the total burdened cost as a value along with the raw cost on
each expenditure item. The total burdened cost equals the raw cost plus the sum of the

Burdening

3-15

burden cost components. With this method, you can easily view the total burdened cost
and the raw cost of each item. Oracle Projects displays the raw and burdened costs of the
expenditure items on windows and reports.

The example in the following table illustrates the total burdened cost method. With
this method, the raw cost is stored on each expenditure item. The burdened cost is
calculated and then also stored on each expenditure item. The burden cost shown in
the table is an interim value that is not stored. In this example, Labor is burdened and
Computer Rental is not.

Item

Transaction

Raw Cost

Burden Cost

Burdened Cost

1

2

3

Project A, Task 1.
1, Labor, August
29, Amy Marlin

Project A, Task 1.
1, Labor, August
29, Don Gray

Project A, Task
1.1, Computer
Rental, August
29, Data Systems

100.00

200.00

300.00

200.00

400.00

600.00

500.00

0.00

500.00

Totals

800.00

600.00

1,400.00

The following table shows the detail of the burden cost on Item 1 in the table above.

Burden Cost Element

Amount

Fringe

Overhead

General and Administrative

Total Burden Cost

40.00

100.00

60.00

200.00

Oracle Projects calculates the burdened cost of each expenditure item in the Distribute
Cost processes. For supplier invoices, the burdened cost of each expenditure item is
calculated in the Interface Supplier Invoices from Payables process.

Note: The burden cost of each item may be comprised of a buildup of
individual burden cost components, as shown in the table above. This is
not readily visible by looking at the expenditure item. However, Oracle
Projects provides the ability to report this buildup of burden cost for
each individual expenditure item. For more information on reporting
the individual burden cost components when you use this method of
storing burden amounts, see: Reporting Burden Components in Custom
Reports, page 3-29.

3-16 Oracle Project Costing User Guide

Storing Burden Costs as a Separate Expenditure Item on the Same Project

You can choose to hold the burden cost components as a separate expenditure item
on the same project. The expenditure items storing the burden cost components are
identified with a different expenditure type that is classified by the expenditure type
class Burden Transaction.

The example in the following table illustrates burden cost as a separate, summarized
expenditure item on the same project.

Item

Transaction

Raw Cost

Burden Cost

Burdened Cost

1

2

3

4

5

6

Project A, Task 1.
1, Labor, August
29, Amy Marlin

Project A, Task 1.
1, Labor, August
29, Don Gray

Project A, Task
1.1, Computer
Rental, August
29, Data Systems

Project A, Task
1.1, Fringe,
September 1,
Consulting East

Project A, Task
1.1, Overhead,
September 1,
Consulting East

Project A, Task
1.1, General and
Administrative,
September 1,
Consulting East

100.00

0.00

100.00

200.00

0.00

200.00

500.00

0.00

500.00

0.00

120.00

120.00

0.00

300.00

300.00

0.00

180.00

180.00

Totals

800.00

600.00

1400.00

Note: The expenditure items that incur the raw cost have a burdened
cost equal to the raw cost, because the burden cost of those transactions
are included in the burden transactions. The burden transactions have
a raw cost of zero and a summarized burden cost from the incurred
raw costs.

Oracle Projects creates the burden transactions by summarizing the burden
cost components by project, lowest task, expenditure organization, expenditure
classification, supplier, PA period, and burden cost code.

If you use this method of storing burden costs, you must assign an expenditure type to
each burden cost code. You may also want to define an expenditure type for each burden
cost code to use for reporting and budgeting purposes. The Create and Distribute Burden
Transactions process summarizes the burden costs for all costed, burdened items. If

Burdening

3-17

you are processing new items for a task that already has burden transactions, Oracle
Projects will create new burden transactions. The existing burden transactions are not
updated. Each new transaction will be assigned the system date when the process is run.

For transactions imported from external systems via transaction import, such as supplier
invoices imported from Payables, burden costs on separate items are created only after
running the Create and Distribute Burden Transactions process.

Expenditure Item Date of Summary Burden Transactions

The expenditure item date of the new summary burden transactions matches the latest
expenditure item date of the expenditures being burdened.

The following table shows examples of expenditure item dates for burden transactions.

PA Period
of Burdened
Expenditures

Latest
Expenditure
Item Date
of Source
Expenditures

Length of PA
Period

Expenditure
Cycle Start Day

Expenditure
Item Date
of Burden
Transactions

Monday, 10/19
through Sunday,
10/25

Monday, 10/12
through Sunday,
10/25

Thursday, 10/
1 through
Saturday, 10/31

Sunday, 10/25

1 Week

Monday

Sunday, 10/25

Sunday, 10/18

2 weeks

Monday

Sunday, 10/18

Saturday, 10/24

1 month

Monday

Saturday, 10/24

See also: Creating and Interfacing the Accounting for Burden Costs by Burden Cost
Component, page 3-22.

Storing Burden Cost as Summarized Expenditures on a Separate Project

You can choose to additionally show the burden cost as summarized expenditures on
a separate project. You assign this separate Burden Cost Project in the Project Types
window. The Burden Cost Project can be a single, indirect project that collects all burden
costs or a project you define for a particular Project Type. These separate expenditures
are generated in the same manner as the separate expenditures described in Burden
Cost as Separate, Summarized Expenditure Items in the following section. The link to
the original expenditure item is maintained but is not readily visible by looking at
the summarized expenditures.

The example in the following table illustrates accounting for summarized burden cost
expenditures on a separate project.

3-18 Oracle Project Costing User Guide

Item

Transaction

Raw Cost

Burden Cost

Burdened Cost

1

2

3

Project
Overhead, Task
1, Fringe, Sept
1, Consulting
East

Project
Overhead, Task
1, Overhead, Sept
1, Consulting
East

Project
Overhead, Task
1, General and
Administrative,
Sept 1,
Consulting East

0.00

120.00

120.00

0.00

300.00

300.00

0.00

180.00

180.00

Choosing a Burden Storage Method

The key difference between burden storage methods is how you view the burden costs
on your project. You view the burden costs as another value on the same expenditure
item or as a separate expenditure item.

The way you budget your projects may influence how you choose to store burden cost:

• If you budget burden components as separate elements in your budget, you would

typically choose to view the actuals in a similar way (as a separate expenditure item).

• If you budget burdened costs as a calculation of the raw cost for a given resource, you
would typically choose to view the actuals in a similar way (with the burdened costs
as a value for the individual expenditure items).

Note: To budget by burden cost component, you use the expenditure
type assigned to the burden cost code during setup.

Regardless of which method you choose to store the burden cost, the total raw and
burdened costs of the project do not change. The key difference is how you view
the information. Also, these methods only apply to storing the cost amounts of
the transactions. If you are using cost plus processing for revenue accrual and/or
invoicing, then the revenue or invoice amounts are held as an amount along with the
raw cost on the expenditure item. You cannot store the burden costs applied for revenue
accrual and invoicing as separate summarized, burden transactions.

Related Topics

Overview of Project Budgeting and Forecasting, Oracle Project Management User Guide

Setting Up The Burden Cost Storage Method

You choose the method by which you want to store burden amounts on each burdened
project type.

Burdening

3-19

If you want to store the burdened cost as an amount on the same expenditure item, you perform the
following step:

In the Costing Information region of the Project Types window, enable the Burden
Cost on Same Expenditure Item check box.

If you want to store the burden costs as separate, summarized transactions on the same project, you
perform the following steps:

1.

2.

3.

In the Costing Information region of the Project Types window, enable the Burden
Cost as Separate Expenditure Item check box.

In the Expenditure Types window, define an expenditure type with expenditure
type class Burden Transaction.

In the Burden Cost Codes window, assign the appropriate burden transaction
expenditure type to each burden cost code.

If you want to store burden amounts on each burdened expenditure item and, additionally, store the
burden amounts in a separate project, you perform the following steps:

1. Define a destination project and task for generated burden transactions.

2.

3.

4.

In the Costing Information region of the Project Types window, enable the Account
for Burden Cost Components check box and add the Project and Task name.

In the Expenditure Types window, define an expenditure type with expenditure
type class Burden Transaction.

In the Burden Cost Codes window, assign the appropriate burden transaction
expenditure type to each burden cost code.

If you want to create total burdened cost credit and debit lines, you perform the following step:

1.

In the Costing Information region of the Project Types window, enable the Enable
Accounting for Total Burdened Cost check box.

Note: When the Enable Accounting for Total Burdened Cost check box is
enabled, Oracle Projects creates total burdened cost credit and debit
lines for all transactions, including summarized burden transactions.

If you do not want to create total burdened cost credit and debit lines, you perform the following step:
In the Costing Information region of the Project Types window, disable the Enable
Accounting for Total Burdened Cost check box.

1.

Note: If the project type class of the project type is Capital and the
Cost Type for capitalization is Burdened Costs, Oracle Projects does
not allow you to disable the Enable Accounting for Total Burdened
Cost check box and save the change. Oracle Projects requires total
burdened cost credit and debit lines to capitalize burdened costs.

Accounting for Burden Costs

You determine if you want to account for the burden costs. You can choose one of the
following accounting methods:

• Account for burden costs by burden cost component, page 3-21

3-20 Oracle Project Costing User Guide

• Account for the total burdened costs, page 3-23

• Perform no accounting -- calculate burden costs only for use in management

reporting with no accounting impact, page 3-25

Oracle Projects supports all of these accounting methods for burden costs regardless
of the method that you choose to store the burden costs, either as a value on the
expenditure item or as separate, summarized expenditure items. There are cases
in which you may choose to use both of the methods of accounting for burdened
costs, based on different objectives.

Accounting for Burden Costs by Burden Cost Component

You can account for the individual burden cost components when you want to track the
burdening in General Ledger.

Example of Accounting for Burden Costs by Burden Cost Component

The following two tables provide an example of the accounting for the expenditure items
shown in the example data for the topic: Storing Burden Costs as a Separate Expenditure
Item on the Same Project, page 3-17. The following table shows the accounting for
the raw cost amounts.

Transaction

Item

Accounting Transactions

Debit

Credit

Labor Cost

Labor Cost

Expense

1

2

3

Labor Expense

Payroll Clearing

Labor Expense

Payroll Clearing

100

200

Computer Rental Expense

500

Payables Liability

100

200

500

The following table shows the accounting for the burden cost amounts.

Transaction

Item

Accounting Transactions

Debit

Credit

Fringe

Overhead

General and
Administrative

4

5

6

Project Fringe Expense

120

Fringe Absorption/Recovery

Project Overhead Expense

300

Overhead Absorption/Recovery

Project General and
Administrative Expense

180

General and Administrative
Absorption/Recovery

120

300

180

Burdening

3-21

Setting Up Accounting for Burden Costs by Burden Cost Component

To set up accounting for burden costs by burden cost component you must perform the
following steps:

1. Define AutoAccounting rules for the Burden Transaction Debit (Burden Cost
Account) and Burden Transaction Credit (Burden Cost Clearing Account)
AutoAccounting functions. These rules are used to determine the debit and
credit GL accounts to be charged. You use the expenditure type parameter to
distinguish between different types of burden cost components. You also have the
AutoAccounting Function Burden Cost Revenue Account to account for revenue.

2.

If you have chosen to store burden costs as a summarized value on a separate project
and task (as defined by selecting the Burden Cost on the same expenditure item
indicator on the project type), you must perform the following additional steps:

• Define a project and appropriate tasks, which will be used as a storing bucket

for summarized, burden transactions used for accounting for the individual
burden costs. You typically would not do project reporting from these collection
projects. However, you may choose to perform some analysis for burden
absorption using these projects. After you account for the burden costs to
General Ledger, you can perform additional analysis within General Ledger.

• Specify the above project and task on the project type. This project and task

are used for collecting the summarized burden transactions that are used only
for the burden accounting.

Creating and Interfacing the Accounting for Burden Costs by Burden Cost Component

To create and interface the accounting for the burden transactions, you run the following
processes:

• PRC: Create and Distribute Burden Transactions. This process summarizes the
burden costs, creates the expenditure items for the burden transactions, and runs
the distribution process. The burden transactions are created on different projects
depending on the method you use to store burden costs. If you store burden costs
as separate, summarized burden transactions, the burden transactions are created
on the same project that incurred the costs. If you choose to store burden costs as
a value along with raw cost on the expenditure item on the project that incurred
the transactions, the burden transactions are created on the collection project and
task used for collecting burden transactions intended for accounting by burden
cost components only.

• PRC: Interface Usage and Miscellaneous Costs to General Ledger. This process

interfaces the burden transactions to Oracle General Ledger. Based on the
expenditure type class you enter as a process parameter, this process will interface
only those transactions that match the parameter. If no parameter is entered, then
this process picks up all Burden Transactions, Miscellaneous Transactions, Usage
Transactions, Inventory Transactions and WIP Transactions for processing.

• PRC: Tieback Usage Costs from General Ledger. This process ties back all

transactions processed in the PRC: Interface Usage and Miscellaneous Costs process.

You can also use the streamline processes to create distribution lines for burdened costs.

Related Topics

Create and Distribute Burden Transactions, Oracle Projects Fundamentals

Interface Usage and Miscellaneous Costs to General Ledger, Oracle Projects Fundamentals

3-22 Oracle Project Costing User Guide

Tieback Usage Costs from General Ledger, Oracle Projects Fundamentals

Implementing AutoAccounting, Oracle Projects Implementation Guide

Accounting for Total Burdened Cost

You may choose to account for the total burdened cost of the items, without
distinguishing the amounts by burden cost components. This is typically done when you
track the total burdened cost in a cost asset or cost WIP (work in process) account. This
method is also sometimes referred to as project inventory. You may track cost WIP
when you:

• capitalize total burdened costs

• track the total burdened costs as project inventory (also known as cost WIP) on

contract projects and later calculate a cost accrual when you generate the revenue.

Note: You must run the appropriate processes to create and interface
total burdened costs distribution lines if you are capitalizing
burdened costs for capital projects or are using burdened costs for
the cost accrual calculation during revenue generation.

Example of Accounting for Total Burdened Cost

The following two tables provide an example of the accounting for the expenditure items
shown in the example for the topic: Storing Burden Cost on the Same Expenditure Item,
page 3-15. The following table shows the accounting for the raw cost amounts.

Transaction

Item

Accounting Transactions

Debit

Credit

Labor Cost

Labor Cost

Expense

1

2

3

Labor Expense

Payroll Clearing

Labor Expense

Payroll Clearing

100

200

Computer Rental Expense

500

Payables Liability

100

200

500

The following table shows the accounting for the total burdened cost amounts.

Burdening

3-23

Transaction

Item

Accounting Transactions

Debit

Credit

Labor

Labor

Expense

1

2

3

Project Cost Inventory

300

Labor Burdened Inventory
Transfer

Project Cost Inventory

600

Labor Burdened Inventory
Transfer

Project Cost Inventory

500

Computer Burdened Inventory
Transfer

300

600

500

Note: The Computer Rental expense is included in the total burdened
cost accounting, even though it is not burdened. This is done to include
the total project cost in the cost WIP accounts.

Setting Up Accounting for Total Burdened Cost

To set up an Account for Total Burdened Costs configuration, you must perform the
following step:

• Define AutoAccounting rules for the Total Burdened Costs Debit and Total Burdened

Cost Credit AutoAccounting functions. These rules are used to determine the
debit and credit GL accounts that will be charged. You must ensure that your
AutoAccounting rules handle all transactions charged to burdened projects, not just
those transactions that are burdened.

Creating and Interfacing the Accounting for Total Burdened Costs

To create and interface the accounting for the total burdened costs, you run the following
processes:

• PRC: Distribute Total Burdened Costs. This process creates the total burdened cost
distribution lines for all transactions charged to burdened projects, even if the
transaction is not burdened, to account for the total project costs in the cost WIP
account.

• PRC: Interface Total Burdened Costs to General Ledger. This process interfaces

total burdened cost distribution lines to Oracle General Ledger.

• PRC: Tieback Total Burdened Costs from General Ledger. This process ties back

total burdened cost distribution lines from Oracle General Ledger.

You can also use the streamline processes to create distribution lines for burdened costs.

Related Topics

Overview of Asset Capitalization, page 5- 1

Revenue-Based Cost Accrual, Oracle Project Billing User Guide

Distribute Total Burdened Cost, Oracle Project Fundamentals

Interface Total Burdened Cost to General Ledger, Oracle Projects Fundamentals

3-24 Oracle Project Costing User Guide

Tieback Total Burdened Cost from General Ledger, Oracle Projects Fundamentals

Implementing AutoAccounting, Oracle Projects Implementation Guide

Storing Burden Costs with No Accounting Impact

You can choose to calculate the burden costs for project transactions for management
reporting without an accounting impact.

If you store burden costs as a value on the expenditure item, you have no extra setup to
perform and no accounting processes to run on the burden costs.

If you store the burden costs as separate, summarized expenditure items and perform
the accounting in Oracle Projects (rather than importing the accounting), you must set
up AutoAccounting for those burden transaction expenditure items to post the debit and
the credit to the same GL account. Oracle Projects requires that you interface the cost
distribution lines of these expenditure items to Oracle General Ledger.

Troubleshooting Burden Transactions

If Oracle Projects does not properly distribute cost or generate revenue for an
expenditure item, you can view revenue rejection reasons from the Expenditure Items
window. Use the Folder option Show Field to display either Cost Distr. Rejection or
Revenue Distr. Rejection.

To be burdened, an expenditure item must meet the following conditions:

• For internal costing, the item must be charged to a project with a project type set

up to burden cost

• For revenue accrual and billing, the item must be charged to a task with a labor
schedule type of Burden, if the item is a labor item; or with a non-labor schedule
type of Burden, if the item is a non-labor item

• Must be categorized by an expenditure type that belongs in a cost base

• Must be included in a compiled schedule

• The lowest task that the expenditure item is charged to must have an assigned
compiled burden schedule for the appropriate calculation of costing, revenue,
or invoicing

Processing Transactions After a Burden Schedule Revision

When you recompile burden schedules, Oracle Projects identifies the existing
transactions that are impacted by the adjustments and marks the transactions for
reprocessing. For example, when the multiplier for a given organization and burden cost
code changes, the system marks for reprocessing all transactions for the organization that
are charged to an expenditure type that is linked to the burden cost code. You must then
reprocess the items by running the appropriate cost, revenue, and invoice processes.

Accounting for Cost Adjustments Resulting from Burden Schedule Revisions

When accounting for the adjusted cost, you can choose to reverse the original accounting
entries and generate new ones for the adjusted cost, or you can choose to generate
new accounting lines for the difference between the original and new burden cost
amounts. To select the accounting option that best fits your business needs, enable
or disable the PA: Create Incremental Transactions for Cost Adjustments Resulting from a
Burden Schedule Recompilation profile option.

Burdening

3-25

For more information on this profile option, see: PA: Create Incremental Transactions
for Cost Adjustments Resulting from a Burden Schedule Recompilation, Oracle Projects
Implementation Guide.

Note: Enabling this profile option does not affect raw and burden cost
recalculation adjustments that you make from the Expenditure Items
window. Although raw cost amounts and accounts are not affected
by a burden cost recalculation, Oracle Projects always accounts for
burden cost recalculation adjustments made from the Expenditure Items
window with a full reversing and rebooking accounting entry that
includes both the raw cost and burden cost amounts. See: Adjusting
Expenditure Items, page 2-49.

Examples of Transaction Accounting After a Burden Schedule Revision

The examples that follow illustrate the original accounting entries generated for a labor
transaction and the adjusting accounting entries generated when the transaction is
reprocessed after a burden schedule is recompiled.

The following assumptions are made in all examples:

• Transaction Raw Cost = $100

• Original Total Burden Cost = $300

• Adjusted Total Burdened Cost = $400

Example One: Total Burdened Cost Accounting

When the PA: Create Incremental Transactions for Cost Adjustments Resulting from a Burden
Schedule Recompilation profile option is set to No, Oracle Projects reverses the original
accounting entries and creates new entries for the adjusted cost amounts.

The following table illustrates the accounting entries generated for raw cost when
total burdened cost is accounted.

Note: The raw accounting lines are reversed and new adjusted lines are
generated even though the raw cost amount does not change.

Item Number

Accounting
Type

Accounting Transactions

Debit

Credit

1

1

Original

Labor Expense

Payroll Clearing

Adjusting

Labor Expense

Payroll Clearing

Labor Expense

Payroll Clearing

100

100

100

100

100

100

The following table illustrates the accounting entries generated for total burdened cost.

3-26 Oracle Project Costing User Guide

Transaction

Item Number

Accounting Transactions

Debit

Credit

Labor Cost

1

Project Cost Inventory

300

Labor Burdening Inventory
Transfer

Project Cost Inventory

Labor Burdening Inventory
Transfer

Project Cost Inventory

Labor Burdening Inventory
Transfer

300

300

400

300

400

When the PA: Create Incremental Transactions for Cost Adjustments Resulting from a Burden
Schedule Recompilation profile option is set to Yes, Oracle Projects does not reverse the
original accounting entries. Instead, Oracle Projects creates new accounting entries for
the difference between the original and new burden cost amounts.

The following table illustrates the accounting entries generated for raw cost when
total burdened cost is accounted.

Transaction

Item Number

Accounting Transactions

Debit

Credit

Labor Cost

1

Labor Expense

100

Payroll Clearing

100

The following table illustrates the accounting entries generated for total burdened cost.

Transaction

Item Number

Accounting Transactions

Debit

Credit

Labor Cost

1

Project Cost Inventory

300

Labor Burdening Inventory
Transfer

Project Cost Inventory

100

Labor Burdening Inventory
Transfer

300

100

Example Two: Accounting for Summarized Burden Cost Components

When the PA: Create Incremental Transactions for Cost Adjustments Resulting from a Burden
Schedule Recompilation profile option is set to No, Oracle Projects reverses the original
accounting entries for the raw cost. Oracle Projects then creates new raw cost entries and
burden entries for the difference between the original and new burden cost amounts.

The following table illustrates the accounting entries generated for raw cost.

Burdening

3-27

Transaction

Item Number

Accounting Transactions

Debit

Credit

Labor Cost

1

Labor Expense

Payroll Clearing

Labor Expense

Payroll Clearing

Labor Expense

Payroll Clearing

100

100

100

100

100

100

The following table illustrates the accounting entries generated for burden costs.

Transaction

Item Number

Accounting Transactions

Debit

Credit

Fringe

Overhead

General and
Administrative

2

3

4

Project Fringe Expense

Fringe Absorption/Recovery

Project Fringe Expense

Fringe Absorption/Recovery

40

20

Project Overhead Expense

100

40

20

Overhead Absorption/Recovery

100

Project Overhead Expense

Overhead Absorption/Recovery

Project General and
Administrative Expense

General and Administrative
Absorption/Recovery

Project General and
Administrative Expense

General and Administrative
Absorption/Recovery

50

60

30

50

60

30

When the PA: Create Incremental Transactions for Cost Adjustments Resulting from a Burden
Schedule Recompilation profile option is set to Yes, Oracle Projects does not reverse the
original accounting entries. Instead, Oracle Projects creates new burden entries for the
difference between the original and new burden cost amounts.

The following table illustrates the accounting entries that are generated for raw cost.

3-28 Oracle Project Costing User Guide

Transaction

Item Number

Accounting Transactions

Debit

Credit

Labor Cost

1

Labor Expense

100

Payroll Clearing

100

The following table illustrates the accounting entries that are generated for burden costs.

Transaction

Item Number

Accounting Transactions

Debit

Credit

Fringe

Overhead

General and
Administrative

2

3

4

Project Fringe Expense

Fringe Absorption/Recovery

Project Fringe Expense

Fringe Absorption/Recovery

40

20

Project Overhead Expense

100

40

20

Overhead Absorption/Recovery

100

Project Overhead Expense

Overhead Absorption/Recovery

Project General and
Administrative Expense

General and Administrative
Absorption/Recovery

Project General and
Administrative Expense

General and Administrative
Absorption/Recovery

50

60

30

50

60

30

Related Topics

Adjustments to Burden Transactions, page 2-53

Reporting Burden Components in Custom Reports

You can report the buildup of costs for each detail transaction, by invoice, in summary
for a project, by GL period, by PA period, or in any way that you want to review
information. This applies only if you stored the burdened cost as a value on the
expenditure item and not if you store it as a summarized burden transaction. You may
want to report this information for internal reporting and for customer billing. For
example, your company may need to create an invoice backup report that displays the
raw cost as well as the related burden cost components on an invoice.

You report the individual burden cost components for costing, revenue, and invoicing
using the appropriate view from the following list:

Burdening

3-29

• PA_CDL_BURDEN_DETAILS_V

• PA_CDL_BURDEN_SUMMARY_V

• PA_COST_BURDEN_DETAILS_V

• PA_INV_BURDEN_DETAILS_V

• PA_REV_BURDEN_DETAILS_V

To create error reports, use the following views:

• PA_CDL_BURDEN_SUM_ERROR_V

• PA_BURDEN_EXP_ITEM_CDL_V

To create the reports for burdened commitments, use the following views:

• PA_CMT_BURDEN_DETAIL_V

• PA_CMT_BURDEN_SUMMARY_V

• PA_CMT_BURDEN_SUM_ERROR_V

• PA_CMT_BURDEN_TXN_V

For more information, refer to the Oracle eBusiness Suite Electronic Technical Reference
Manual (eTRM), available on Oracle MetaLink

Revenue and Billing for Burden Transactions

All expenditure types that will be used on a project must be included in the bill rate
schedule that will be used by that project. If they are not, you will receive an error
message when you generate invoices or revenue.

Including Burden Transactions in Revenue and Invoices

The expenditure type Burden Transaction is a non-labor expenditure type. To include
burden transactions in revenue and invoice calculations, you must include Burden
Transactions as an expenditure type when you set up the non-labor bill rate schedule.

Markup is based on the raw cost amount, except in the case of burden transactions, where
markup is based on burden cost. If you need to distinguish the bill rate or markup for
each type of cost base, then you must define burden cost codes and expenditure types
for each category.

For example, if all expenditures are burdened with General and Administrative
burden, but you want to distinguish the labor value of this burden on an invoice, or
mark it up differently, you must create a General and Administrative burden cost code
expenditure type for labor. (Burden cost code expenditure types are defined under
Entities that Affect Burdening, page 3-44.)

Revenue and Billing for Burdened Labor

If your employee bill rates are based on quantity and hours, then burden cost does not
affect revenue and billing. However, if you bill for labor based on markup, you may
need to distinguish labor burden cost by defining burden cost codes and expenditure
types for labor.

3-30 Oracle Project Costing User Guide

Revenue Burdening Using Revenue or Invoice Schedules

If you use revenue or invoice schedules and you want the burden transaction to be
revenue burdened, then you must include the burden expenditure types in the burden
structures that are used for revenue and invoicing.

Showing Non-Labor Burden Transactions on an Invoice

If you show burden transactions for non-labor expenditures on a project invoice, the
quantity for burden transactions will be displayed as zero.

Reporting Requirements for Project Burdening

The following illustration shows how the reporting requirement for project costs
generally has three levels.

Project costs reporting pyramid

Oracle Projects provides several ways to set up burdening to serve project reporting
needs. For example:

• You can show burden transactions individually on a project, and also record the

detail transactions in the general ledger.

• You can charge burden costs to internal projects to provide visibility within Oracle

Projects of total recovered overhead costs.

• You can choose not to view the individual burden transactions in Oracle

Projects, while charging total burdened cost to project inventory in the general ledger.

GL and Upper Management Reporting

During the financial cycle, the financial reports (income statement and balance sheet)
provide a summary view of a company’s fiscal performance. Before the beginning of a
new fiscal year, a company develops budgets for the coming year based on the prior
year’s performance, as well as expectations and plans for the coming fiscal year. The
accountants review the total budgeted burden costs such as overhead, fringe, and G&A
(general and administrative). They then estimate, for each project type, the burden
multipliers and basis (such as labor hours) for applying the burden.

Burdening

3-31

An overhead cost may be associated with the entire company and therefore must be
shared across organizations. A burden multiplier algorithm can be implemented
to distribute (burden) overhead costs to selected organizations and/or projects. To
monitor the burdening of projects, the costing processes must capture the burden
information. Management reports must track the recovery of overhead, identify
overhead costs that have been insufficiently or excessively recovered (unders and
overs), and show comparison ratios such as actual revenue to actual total cost, and
budget to actual cost.

In the income statement and balance sheet shown in the following two tables, overhead
is recovered at the general ledger level. These statements do not reflect the use of
project burdening.

Income Statement

The following income statement shows overhead recovered at the general ledger level.

Income Statement Item

Revenue

Less: Direct Cost of Projects

Contribution Margin 1

Less: Burden 1 Cost (Project Indirect Cost)

Contribution Margin 2

Less: Burden 2 Cost (Corporate Expense)

PROFIT

Amount

100

30

70

10

60

27

33

Balance Sheet:

The following balance sheet shows overhead recovered at the general ledger level.

3-32 Oracle Project Costing User Guide

Balance Sheet Item

Amount

ASSETS

Project Inventory

Construction in Progress (CIP)

TOTAL ASSETS

LIABILITIES

Accounts Payable

EQUITY

Owners’ Shares and Retained Earnings

Plus: Raw Cost Profit

TOTAL EQUITY

TOTAL LIABILITIES AND EQUITY

200

138

338

75

230

33

263

338

In the financial statements shown in the tables above, project expenditures are charged
directly to projects and are subtracted from revenue to produce the Contribution Margin
1. Overhead (project indirect cost) is subtracted from Contribution Margin 1 to produce
Contribution Margin 2. Corporate expense is then subtracted, to determine the profit.

If overhead is recovered at the project level, expense components of the income
statement are reclassified as direct project cost elements. This provides management
with an alternative view of the cost of doing business.

Burden Multiplier Algorithm

The cost of doing business may vary from department to department or from project to
project. How you apply burden costs can be driven directly by how much overhead
an organization or project incurs. You typically determine the burden multiplier based
on a forecast of the amount of overhead cost incurred.

The table below shows an example of a burden multiplier algorithm.

Cost Element

Cost

Reference / Formula

Raw Labor (1 hour)

Burden 1 (30%)

Burden 2 (69%)

Total Labor

10

3

9

22

A

B = A x .3

C = (A+B) x .69

D = A + B + C

In this algorithm, indirect costs (Burden 1) are weighted at a rate of 30% of an employee’s
hour of labor. Burden 2 is weighted at 69% of a labor hour after Burden 1 is applied.

Burdening

3-33

If the algorithm shown in the table above were implemented in Oracle Projects, the
financial statements would be restated to show overhead recovery. This is shown in
the reclassified income statement and reclassified balance sheet represented in the
following two tables.

Reclassified Income Statement

The following income statement is restated to show overhead recovery.

Income Statement Item

Burden Detail
Amounts

Net Amounts

Revenue

Less: Cost of Projects (Total cost incurred,
including overhead)

Contribution Margin 1

Burden 1 Cost

Less: Recovered Income Statement

Less: Recovered Balance Sheet

Net Burden 1 Cost

Contribution Margin 2

Burden 2 Cost

Less: Recovered Income Statement

Less: Recovered Balance Sheet

Net Burden 2 Cost

PROFIT

10

7

2

27

21

5

100

58

42

1

41

1

40

Reclassified Balance Sheet

The following balance sheet is restated to show overhead recovery.

3-34 Oracle Project Costing User Guide

Balance Sheet Item

Amount

ASSETS

Project Inventory

Plus: Burden Cost

Total Inventory Cost

Construction in Progress (CIP)

Plus: Burden Cost

Total Construction in Progress (CIP)

TOTAL ASSETS

LIABILITIES

Accounts Payable

EQUITY

Owners’ Shares and Retained Earnings

Plus Burdened Profit

TOTAL EQUITY

TOTAL LIABILITIES AND EQUITY

200

5

205

138

2

140

345

75

230

40

270

345

Accounting Transactions for Burden Cost Reporting

Examples of typical accounts payable (AP), purchasing (PO), and general ledger (GL)
transactions that result in cost reporting in the general ledger are shown in the following
table:

Transaction Type

Direct, Burden 1 and
Burden 2 Costs

Debit Account

Credit Account

AP/PO

AP/PO

GL

Material Purchase
- Raw Cost

Cost of Project

Stationery Purchase
- Burden 1

Stationery

Interest Expense -
Burden 2

Interest Expense

AP Liability

AP Liability

Bank

Burdening

3-35

The Oracle Projects transactions shown in the table below are used to offset the overhead
entries shown in the table above. Labor hours are used as the cost basis for applying
overhead.

Generated Transactions

Debit Account

Credit Account

Labor Hour

Labor Expense

Burden 1

Project Burden 1

Burden 2

Project Burden 2

Payroll Clearing

Burden 1 Recovered

Burden 2 Recovered

Burdening Options for General Ledger Accounting and Reporting

Oracle Projects provides the following options for accounting for and reporting project
burdening in the general ledger:

1. Track burden amount for each burden cost code

2.

3.

4.

Show burdening in one account

Show total burdened cost as one sum

Show total burdened cost as one sum, and expense project burden

5. No burden tracking in GL

Following are descriptions and examples of these options.

Note: The examples that follow use a three-segment general ledger
account. The segments are company, cost center, and account. Because
all transactions occur within the same company, the journal entries show
only the cost center segment and account. Additionally, the Type of
Account (Acct) column in each table reflects whether each account is an
income statement (I.S.) account or a balance sheet (B.S.) account.

GL Option 1: Track Burden Amount for Each Burden Cost Code

In this option, shown in the following table, each burden transaction (Burden 1
and Burden 2 in our example) is charged to a general ledger account set up for the
appropriate burden cost code. This provides visibility to overhead recovery information
at the burden cost code level.

The burden transactions can optionally be charged (debited) to the same account as
the raw cost, but the credit transaction will go to a recovery account set up for each
burden cost code.

3-36 Oracle Project Costing User Guide

Generated
Transactions

Cost Center
Segment

Account

Dr.

Cr.

Type of Acct

Labor Costs

Project
Organization

Project
Expense

Expenditure
Org.

Payroll
Clearing

Burden 1
Costs

Project
Organization

Project
Burden 1

Expenditure
Org.

Burden 1
Recovered

Burden 2
Costs

Project
Organization

Project
Burden 2

Expenditure
Org.

Burden 2
Recovered

20

6

18

Usage Cost

Project
Organization

Project
Expense

100

Expenditure
Org.

Usage
Clearing

I.S.

I.S.

I.S.

I.S.

I.S.

I.S.

I.S.

I.S.

20

6

18

100

GL Option 2: Show Burdening in One Account

In this option, shown in the following table, burden is accounted for separately from raw
cost for reconciliation and reporting purposes. It is recovered in one recovery account. A
separate account is not required for each burden cost code.

The balance in the Burden Recovered account is the summary burden cost. The Project
Inventory balance is total burdened cost (raw cost plus burden cost).

Generated
Transactions

Cost Center
Segment

Account

Dr.

Cr.

Type of Acct

Labor Costs

Project Org.

Project
Inventory

Expenditure
Org.

Payroll
Clearing

Overhead
(Burden 1 and
Burden 2)

Project Org.

Project
Inventory

20

24

Expenditure
Org.

Burden
Recovered

Usage Cost

Project Org.

Project
Inventory

100

Expenditure
Org.

Usage
Clearing

B.S.

I.S.

B.S.

I.S.

B.S.

I.S.

20

24

100

Burdening

3-37

GL Option 3: Show Total Burdened Cost as One Sum

As in GL option 2, the net balance in the Burden Recovered account is the summary
burden cost (24), and the Project Inventory balance is the total burdened cost
(Labor=44, Usage=100). However, the amount for each burden cost code is not visible in
the general ledger. GL option 3 is summarized in the following table:

Generated
Transactions

Cost Center
Segment

Account

Dr.

Cr.

Type of Acct

Raw Labor
Costs

Expenditure
Org.

Burden
Recovered

20

Expenditure
Org.

Payroll
Clearing

Raw Usage
Cost

Expenditure
Org.

Usage
Expense

100

Expenditure
Org.

Usage
Clearing

Total
Burdened
Labor Costs

Project Org.

Project
Inventory

44

Expenditure
Org.

Burden
Recovered

Total
Burdened
Usage Cost

Project Org.

Project
Inventory

100

20

100

44

I.S.

I.S.

I.S.

I.S.

B.S.

I.S.

B.S.

Expenditure
Org.

Usage
Transferred
Out

100

I.S.

GL Option 4: Show Total Burdened Cost as One Sum, and Expense Project Burden

For this option, shown in the following table, total burdened cost is shown as one
sum, as in GL option 3. In addition, total overhead costs, summarized by burden cost
code, are accounted as expense. With this method, the Project Inventory account shows
the total burdened cost, but details of the burden (by burden cost code) are stored
separately for burden recovery purposes.

3-38 Oracle Project Costing User Guide

Generated
Transactions

Cost Center
Segment

Account

Dr.

Cr.

Type of Acct

Raw Labor
Costs

Expenditure
Org.

Burden
Recovered

20

Expenditure
Org.

Payroll
Clearing

Raw Usage
Cost

Expenditure
Org.

Usage
Expense

100

Expenditure
Org.

Usage
Clearing

Total
Burdened
Labor Costs

Project Org.

Project
Inventory

44

Expenditure
Org.

Burden
Recovered

Total
Burdened
Usage Cost

Project Org.

Project
Inventory

100

Expenditure
Org.

Usage
Transferred
Out

Burden 1
Costs

Expenditure
Org.

Burden 1
Expense

Expenditure
Org.

Burden 1
Recovered

Burden 2
Costs

Expenditure
Org.

Burden 2
Expense

6

18

Expenditure
Org.

Burden 2
Recovered

I.S.

I.S.

I.S.

I.S.

B.S.

I.S.

B.S.

I.S.

I.S.

I.S.

I.S.

I.S.

20

100

44

100

6

18

GL Option 5: No Burden Tracking in GL

In this option, shown in the table below, the project managers need to track burden but
upper and accounting managers do not.

Using this option, the burden cost journals in the general ledger net to zero. Only the
raw cost is shown in the Project Inventory balance.

Burdening

3-39

Generated
Transactions

Cost Center
Segment

Account

Dr.

Cr.

Type of Acct

Labor Costs

Project Org.

Project
Inventory

20

Expenditure
Org.

Payroll
Clearing

Usage Cost

Project Org.

Project
Inventory

100

Expenditure
Org.

Usage
Clearing

Total
Burdened
Cost

Expenditure
Org.

Burden
Recovered

24

Expenditure
Org.

Burden
Recovered

Usage Cost

Expenditure
Org.

Usage
Clearing

100

Expenditure
Org.

Usage
Clearing

B.S.

I.S.

B.S.

I.S.

I.S.

I.S.

I.S.

I.S.

20

100

24

100

Middle Management Reporting

As shown in the illustration Project Costs Reporting Pyramid, page 3-31, middle
management relies on both Oracle Projects and the general ledger for their required
information.

A division or department manager looks for project information at the summary projects
level. This manager may want to see total project burdening by burden cost code
(Burden 1 and Burden 2), as shown in the following table:

All Projects

Total

Revenue

Raw Cost

Burden 1

Burden 2

Contribution Margin

60

18

5

17

20

Or, the division or department manager may want to see only the total burdened costs of
all projects, as shown in the following table:

3-40 Oracle Project Costing User Guide

All Projects

Revenue

Total Cost of Projects

Contribution Margin

Total

60

40

20

Project Management Reporting

During a project life cycle, project managers review project information in the Oracle
Projects application. They review comparison ratios (revenue to cost, budget to
actual, etc.) for each project and/or for all projects in a division or department.

The project manager and accounting manager may want to view the same level of detail
for projects as for GL accounts, or their needs may be different.

A project manager is concerned about revenue and cost on an individual project
basis. How is the project doing compared to the budget? When burden recovered in
the project, at the expenditure item level, the project manager can review total project
cost on an ongoing basis.

A project manager may want to see the burden cost on a project by burden cost code
(Burden 1 and Burden 2), or may only want to see total burdened cost (raw and burden).

Burdening Options for Project Reporting

Oracle Projects provides flexible options to provide solutions for different project
reporting requirements. Some examples of these requirements are:

• Burden costs are visible on each project

• Budgeting is done by burden cost code

• Only total cost needs to be visible on a project

• A project requires separation of raw cost and burden cost for a complete project

management picture

The following burdening options are provided by Oracle Projects for project reporting.

1. Burden transactions on the original project/task

2. Total burdened cost and separate burden transactions

3. Total burdened cost only

These options are described below.

In the examples, labor costs are burdened with Burden 1 and Burden 2, and usage costs
are not burdened. This rule is for these examples only -- In practice, usage can be
burdened. The examples are designed this way because

• it is a common practice to burden labor but not usage, and

• with this scenario we can illustrate how both burdened and non-burdened

transactions are handled in each example.

Burdening

3-41

Projects Option 1: Burden transactions on the original project/task

In this option, summarized burden transactions are shown on the same project/task as
the original expenditures.

Using this option, the project manager can view the total project cost, and can also
view the burden costs separately from the raw cost. The following table shows this
information as it might be viewed in Project Status Inquiry or in a custom report.

Project ABC Cost

Raw Cost

Burdened Cost

Labor Cost (Employee 1)

Labor Cost (Employee 2)

Burden 1 (30%)

Burden 2(69%)

Total Labor Cost

Usage Cost

Total Burdened Cost

10

10

0

0

20

100

120

10

10

6

18

44

100

144

Projects Option 2: Total burdened cost and separate burden transactions

In this option, the project shows total burdened cost for each burdened expenditure, as
shown in the following table. Summarized burden transactions are shown on a separate
project.

Using this option, analysis and reporting on burden are done on an overview basis, not
project by project. Budgeting can be done by burden cost code on the separate
project. This enables budget-to-actual analysis of the overall project burden.

Project ABC Cost

Raw Cost

Burdened Cost

Labor Cost (Employee 1)

Labor Cost (Employee 2)

Total Labor Cost

Usage Cost

Total Project Cost

10

10

20

100

120

22

22

44

100

144

The details of the total burdened cost are visible in database views, as shown in the
following table. Custom solutions can be developed for individual implementations
to report the required details.

3-42 Oracle Project Costing User Guide

Project ABC

Total

Cost Breakdown

Revenue

Total Cost

Contribution Margin

4

3

1

Raw Cost - 1.5, Burden 1
- 0.4, Burden 2 - 1.1

A separate project, Project XYZ, is set up to collect burden transactions on Project ABC
and other projects. The following table shows the burden costs collected by project XYZ
for the labor cost incurred on project ABC.

In this table, the burden costs are displayed in the Burdened Cost/Burden Element
column. While the amounts represent only the burden element, they would be displayed
in the Burdened Cost column when viewed in the Project Status Inquiry window.

Project XYZ Cost

Raw Cost

Burdened Cost /Burden
Element

Burden 1 (30%)

Burden 2(69%)

0

0

6

18

Project Option 3: Total burdened cost only

In this option, the project shows total burdened cost, as shown in the following
table. Separate burden transactions are not created.

You can use this option when the project manager does not need to view the burden
transactions. Total burdened cost provides the information required to manage the
project.

Project ABC Cost

Raw Cost

Burdened Cost

Labor Cost (Employee 1)

Labor Cost (Employee 2)

Total Labor Cost

Usage Cost

Total Project Cost

10

10

20

100

120

22

22

44

100

144

Setting Up Burden Cost Accounting to Fit Reporting Needs

The following table shows how burden cost accounting can be set up in Oracle Projects
and GL to accommodate reporting needs. The table shows which of the following four
setup options you can use for each Oracle Projects and GL setup combination:

• Setup A: Maximum Detail, page 3-44

• Setup B: Detail in Oracle Projects, One Sum in GL, page 3-45

Burdening

3-43

• Setup C: Total Burdened Cost, page 3-46

• Setup D: No Project Burden Tracking in GL, page 3-46

Oracle
Projects
Options:

GL Option 1:
By Burden
Cost Code

GL Option
2: One
Account

GL Option
3: One Sum

GL Option 4:
Expensed

GL Option 5:
Not Tracked

1. Burden
transactions
on the
original
project

2. Total
burdened
cost and
separate
burden
transactions

3. Total
burdened
cost

Setup A

Setup A

n/a

n/a

Setup D

n/a

n/a

Setup B

Setup B

Setup D

n/a

n/a

Setup C

n/a

Setup D

Entities That Affect Burdening

How a project is burdened depends on the setup of the following entities:

1. Burden Cost Code Expenditure Types

The expenditure types you set up to associate with burden cost codes are used
only for burden transactions. These expenditure types are referred to as burden
cost code expenditure types.

2. Burden Cost Codes

3. Burden Structures

When you define burden structures, you associate expenditure types with each cost
base you enter. Therefore, although an expenditure type can be associated with
multiple expenditure type classes, the burden structure is based on the expenditure
type, not the expenditure type class.

4. Burden Schedules

5. Project Types

6. AutoAccounting for raw, burden, and/or total burdened cost

The following sections tell you how to set up these entities for the four burdening
setup options referenced in the table above.

Setup A: Maximum Detail

This solution provides maximum visibility of burden costs on the original project, and
shows details of the recovered burden in the general ledger.

Use this implementation to set up GL options 1 and 2 with Projects option 1. To track
maximum detail, you follow these steps:

1. Burden Cost Code Expenditure Types

3-44 Oracle Project Costing User Guide

In the Expenditure Types window, create an expenditure type for each of the burden
cost codes you plan to use. Each expenditure type must have the expenditure type
class Burden Transaction. If you define each expenditure type with the same name as
the corresponding burden cost code, it will make it easier to reconcile and set up
AutoAccounting for your burden costs.

2. Burden Cost Codes

Assign the burden cost code expenditure types to burden cost codes in the Burden
Cost Codes window.

3. Burden Structures and Burden Schedules

Create burden structures that map the different burden cost codes to cost bases and
expenditure types. Create burden schedules that use appropriate burden multipliers.

4. Project Types

Define one or more project types with the following options selected in the Costing
Information region:

5. Enable the Burdened check box and select a burden schedule.

6. Enable the Burden Cost as Separate Expenditure Item check box. This selection
generates summarized burden transactions on the same project/task where
expenditures are incurred.

7. AutoAccounting

Set up AutoAccounting rules for all raw and burden costs.

Warning: Do not enable the rules for Total Burden Cost for this
option.

Setup B: Detail in Oracle Projects, One Sum in GL

With this solution, you report overall burden cost by burden cost code in Oracle
Projects. In the general ledger, burden cost will be tracked as one sum. This solution
implements Projects option 2, combined with either GL option 3 or GL option 4. To track
detail in Oracle Projects, and show one sum in GL, follow these steps:

1. Burden Cost Code Expenditure Types

Create an expenditure type for each of the burden cost codes you plan to use. Each
expenditure type must have the expenditure type class Burden Transaction. If you define
each expenditure type with the same name as the corresponding burden cost code, it will
make it easier to reconcile and set up AutoAccounting for your burden costs.

1. Burden Cost Codes

Assign the burden cost code expenditure types to burden cost codes in the Burden Cost
Codes window. This step is necessary only if you have created expenditure types
for burdening in step 1 above.

1. Burden Structures and Burden Schedules

Create burden structures that incorporate the multiple burden cost codes. Create burden
schedules that use appropriate burden multipliers.

1. Project Types

Define one or more project types with the following options selected in the Costing
Information region:

Burdening

3-45

• Enable the Burdened check box and select a burden schedule.

• Enable the Burden Cost on Same Expenditure Item option and the Account for Burden

Cost Components check box. This selection generates summarized burden transactions
on a separate project as well as total burdened cost on the original expenditure.

• Enter a project/task for the burden transactions.

• AutoAccounting

Set up AutoAccounting rules for all raw, burden, and total burdened costs.

Setup C: Total Burdened Cost

With this solution, total burdened cost will be shown on the project. The general ledger
will show total burdened cost as one sum.

This solution implements Projects option 3 with GL option 3. To show total burdened
cost on the project and one sum in GL, follow these steps:

1. Burden Structures

Create burden structures that incorporate the multiple burden cost codes. Create
burden schedules that use appropriate burden multipliers.

2. Project Types

Define one or more project types with the following options selected in the Costing
Information region:

3. Enable the Burdened check box and select a burden schedule.

4. Enable the Burden Cost on Same Expenditure Item check box. This selection generates

total burdened cost balances on each burdened expenditure item.

5. AutoAccounting

Set up AutoAccounting rules for all raw, burden, and total burdened costs. Burden
transaction accounting is configured to handle one off, manual, or imported burden
transactions.

Setup D: No Project Burden Tracking in GL

With this solution, there is no tracking in the general ledger of burden recovered on
projects. This solution implements GL option 5.

Steps 1 and 2 below are required if the you require visibility of burden transactions on
the project. If you only want to report by summary burden cost codes, then these steps
are not necessary. For reporting purposes, the individual burden expenditures are
available internally. To track burdening only in Oracle Projects, follow these steps:

1. Burden Cost Code Expenditure Types

Create an expenditure type for each of the burden cost codes you plan to use. Each
expenditure type must have the expenditure type class Burden Transaction. If you define
each expenditure type with the same name as the corresponding burden cost code, it
will make it easier to assign expenditure types correctly.

1. Burden Cost Codes

Assign the new expenditure types to burden cost codes in the Burden Cost Codes
window.

3-46 Oracle Project Costing User Guide

1. Burden Structures

Create burden structures that incorporate the multiple burden cost codes. Create burden
schedules that use appropriate burden multipliers.

1. Project Types

Define one or more project types with the following options selected in the Costing
Information region:

• Enable the Burdened check box and select a burden schedule.

• Projects option 1: If you want to view burden costs as separate transactions on the
same project, enable the Burden Cost as Separate Expenditure Item check box. This
selection generates summarized burden transactions on the same project where
expenditures are incurred.

• Projects option 2: If you want to view burden costs on the same project, and collect
summary burden transactions on a different project, enable the Burden Cost on Same
Expenditure Item option and the Account for Burden Cost Components check box, and
enter the project and task name. This selection generates summarized burden
transactions on a separate project while generating total burdened cost on the
original expenditure.

• AutoAccounting

Set up AutoAccounting rules for all raw and burden costs.

Although this solution does not require general ledger tracking of burden
recovery, Oracle Projects will still interface the burden transactions to the general
ledger. To create a net zero transaction, set up AutoAccounting to post the debit and
credit to the same account.

Warning: Do not enable the rules for Total Burden Cost for this option.

Burdening

3-47

4
Allocations

This chapter describes how you can allocate costs to projects and tasks.

This chapter covers the following topics:

• Overview of Allocations

• Creating Allocations

• Full and Incremental Allocations

• AutoAllocations

Overview of Allocations

Project managers often need to allocate certain costs (amounts) from one project to
another. The allocations feature in Oracle Projects can distribute amounts between
and within projects and tasks, or to projects in other organizational units. For
example, a manager could distribute across several projects (and tasks) amounts such as
salaries, administrative overhead, and equipment charges. Your allocations can be as
simple or elaborate as you like.

Note: Oracle Projects performs allocations among and within projects
and tasks. MassAllocations in Oracle General Ledger performs
allocations among GL accounts. You can use AutoAllocations in either
General Ledger or Oracle Projects to run MassAllocations.

You identify the sources-costs or amounts you want to allocate-and then define targets-the
projects and tasks to which you want to allocate amounts. If you want, you can offset the
allocations with reversing transactions.

The system gathers source amounts into a source pool, and then allocates to the targets
at the rate (basis) that you specify.

When you allocate amounts, you create expenditure items whose amounts are derived
from one or more of the following:

• Existing summarized expenditure items in Oracle Projects

• A fixed amount

• Amounts in a General Ledger account balance

You can specify exactly how and where you want to allocate selected amounts. For
example, you may want to:

• Allocate the actual cost of office supplies equitably among various projects

Allocations

4-1

• Charge certain projects a larger percentage of costs

• Allocate overhead costs, charging them to projects that benefited from the overhead

activities

Understanding the Difference Between Allocation and Burdening

Allocation uses existing project amounts to generate expenditure items, which you can
then assign to specified projects.

Burdening estimates overhead by increasing expenditure item amounts by a set
percentage.

Allocations and burdening are not mutually exclusive. Whether your company uses
allocations, burdening, or both in a particular situation depends on how your company
works and how you have implemented Oracle Projects.

Related Topics

Overview of Burdening, page 3- 1

Creating Allocations

Creating allocation transactions involves several stages. Each of these stages is described
in the pages listed below:

1. Define one or more allocation rules. See: Defining Allocation Rules, page 4- 3 .

2. Create a draft allocation run by selecting a rule and generating allocation

transactions. See: Allocating Costs, page 4- 4 .

3. Use the Review Allocation Runs window to review the results of the draft allocation

run. Delete the run if it is unsatisfactory, then correct the rule and rerun the
allocation. See: Viewing Allocation Runs, page 4- 6 .

4. Release the draft run. See: Releasing Allocation Runs, page 4- 6 .

You can also reverse runs that have been released. See: Reversing Allocation Runs,
page 4-10.

Related Topics

Viewing Allocation Transactions, page 4- 9

4-2 Oracle Project Costing User Guide

Defining Allocation Rules

Allocation rules define how allocation transactions are to be generated, including:

• The source of the amounts you are allocating

• The targets-the projects and tasks to which you want to allocate amounts

• How much of the source pool you want to allocate, and if you want to include a
fixed amount, GL balance, or client extension (or any combination of these)

• The time period during which the rule is valid

You can create as many rules as you want, and use them in as many allocation runs
as you want.

You can leave the original expenditure amounts in the source project, or offset the
amounts with reversing transactions. In most cases, the reversing transactions decrease
the project balance by the amount of the allocation.

Allocations and Operating Units (Cross Charging)

Each allocation rule belongs to an operating unit and cannot be shared with other
operating units.

Allocation rule source projects must be from the same operating unit unless cross charge
is enabled. If cross-charge is enabled, you can allocate to target projects that are in
different operating units from the source project operating unit. Offset projects must
always be in the same operating unit as source projects. See: Implementation Options in
Oracle Projects: Cross Charge: Allow Cross Charges to All Operating Units Within Legal
Entity, Oracle Projects Implementation Guide.

Related Topics

Full and Incremental Allocations, page 4-10

Allocations

4-3

Defining Allocation Rules, Oracle Projects Implementation Guide

Allocating Costs

Once you have created a rule for allocating costs, you can use the rule in an allocation
run. Processing the rule generates allocation transactions and (if specified) offset
transactions in a draft, a trial allocation run that you can review and evaluate. If the
draft allocation fails or does not produce the results you expect, you can delete the
draft, change the rule parameters, and then create another draft. When you are satisfied
with the draft run and its status is Draft Success, you can release the allocation run.

Any source projects that you include in an allocation must not be closed. Any target or
offset project that you include in an allocation run must have a status that allows the
creation of transactions (as defined by your implementation team).

You can create, review, and delete draft runs until you are satisfied with the
results. However, you cannot create a draft if another draft exists for the same rule.

Although you can run the Generate Allocations Transactions process at any time, it is
a good practice to prepare for the allocation run by distributing costs and running
all interfaces and summarization processes. Doing so ensures that the allocation run
includes all relevant amounts.

Warning: If you use an allocation rule that is set up for full allocation
more than once in a run period, you will generate duplicate
transactions in your target projects. If this happens, you can reverse
the run. See: Reversing Allocation Runs, page 4-10 and see: Full and
Incremental Allocations, page 4-10.

Precedence

Excluded lines take precedence over included lines, and the allocation rule processes
lower line numbers first. For more information about precedence, see: Defining the
Targets, Oracle Projects Implementation Guide.

About the Run Status

The run status shows the progress and state of the allocation run. The following table
describes the possible statuses for an allocation run. For information on the actions you
can take for each status, see: Viewing Allocation Runs, page 4- 6 .

Note: You may have to wait a short time for the system to change
the status.

4-4 Oracle Project Costing User Guide

Status

In Process

Draft Success

Draft Failure

Release Success

Release Failure

Description

The process is not yet complete.

The process has created draft transactions
which are ready for release.

Note: The system will not create the
transactions in the target and (if specified)
offset projects and tasks until you release the
draft.

The process encountered problems and could
not create draft transactions.

The system has written the transactions to the
target and (if specified) offset projects and
tasks.

The system has not written the transactions,
perhaps because projects or tasks included in
the draft run were deleted or closed after the
process created the draft. Delete the run, fix
the problem, and then run the rule again.

Viewing Process Results

The PRC: Generate Allocations Transactions process produces the Allocation Run
Report. For more information on this process, see: Generate Allocations Transactions,
Oracle Projects Fundamentals.

To create an allocations run:

1. Navigate to the Submit a New Request window.

2.

Submit a request for the PRC: Generate Allocations Transactions process.

3. The following table shows the parameters you specify for each field in the

Parameters window.

For this field...

Rule Name

Period Name

Expenditure Item Date

Do this...

Enter the name of the allocation rule that
you want to use in this allocation run.

Select the period from which the process will
accumulate the source amount.

Enter a date for the allocation transactions.
The default is the system date.

Note: If the list of values in the Parameters window of the
PRC: Generate Allocations Transactions process does not display
an allocation rule that you are looking for, then the rule may not
be currently in effect. Allocation rules are available only within a

Allocations

4-5

certain time period, as defined by the Effective Dates fields in the
Allocation Rule window. For more information, see: Defining
Allocation Rules, Oracle Projects Implementation Guide.

(If a rule is in effect on the day you create a draft run for the rule, you
can release the draft later, even if the rule is no longer in effect.)

Releasing Allocation Runs

After you create a successful draft run, the process has created the allocation transactions
but not yet allocated each transaction to the targets you specified. To allocate the
transactions to the targets, you release the run.

Note: You can release a draft run after the effective dates of the rule.

To release an allocation run:

1. Navigate to the Find Allocations Runs window and enter selection criteria. (To see

all existing allocation runs, leave all the fields blank.)

The Review Allocation Runs window opens.

2.

Select the allocation run you want to release (the status must be Draft Success), and
then choose Release.

After you release the run, the status changes to Release Success or Release Failure. You
may have to wait a short while for the status to change. For more information about
the status see: About the Run Status, page 4- 4 .

Note: You can also use the Requests window to release the run.

Viewing Allocation Runs

4-6 Oracle Project Costing User Guide

You can view various aspects of an allocation run in the Review Allocation Runs
window, including the run status.

You can also view allocation transactions by querying by batch name. See: Viewing
Allocation Transactions, page 4- 9 .

To view allocation runs:

1. Navigate to the Find Allocations Runs window and enter selection criteria. (To see

all existing allocation runs, leave all the fields blank.)

The Review Allocation Runs window opens.

2.

Select the allocation run that you want to view and choose an action button. The
following table describes the actions that you can perform when you are viewing
allocation runs, depending on the run status. Also see: About the Run Status,
page 4- 4 .

To...

With this status...

Do this...

Delete an allocation run

Draft Success

Draft Failure

Release Failure

Draft Failure

View the exceptions for a
failed allocation run

Reverse an allocation run

Release Success

Release an allocation run

Draft Success

See missing amounts for the
second and subsequent runs
of an incremental allocation

Release Failure

Draft Success

Draft Failure

Release Success

Release Failure

Choose Delete, and then
confirm the deletion.

Choose Exceptions. You
see information about the
draft failure in the Draft
Exceptions window. (The
Allocation Run Report
also includes a list of the
exceptions. See: Generate
Allocations Transactions,
Oracle Projects Fundamentals).

Choose Reverse. See:
Reversing Allocation Runs,
page 4-10.

Choose Release, and then
confirm the release. See
Releasing Allocation Runs,
page 4- 6 .

Choose Missing Amounts.
To limit the display in the
Missing Amounts window,
specify the type of amount
you want to see, and then
choose Find. To see the total
missing amounts, choose
Totals. See: About Previous
Amounts and Missing
Amounts in Allocation Runs,
page 4-11.

Allocations

4-7

To...

With this status...

Do this...

See the basis details for an
allocation run that used a
rule whose basis is prorated

See the source detail lines for
an allocation run

See the transactions created
by an allocation run

Draft Success

Draft Failure

Release Success

Release Failure

Draft Success

Draft Failure

Release Success

Release Failure

Reversed

Draft Success

Draft Failure

Release Success

Release Failure

Reversed

Choose Basis Details. The
Basis Details window
displays basis information
about the target lines in the
allocation run. To see the
total basis amounts, choose
Totals.

Choose Source Details. The
Source Details window
displays information about
the sources used in the
allocation run. To see total
pool amounts, choose Totals.

Choose Transactions. The
Transactions window
displays information about
the transactions associated
with the allocation run.
To limit the number of
transactions displayed, select
a check box and then choose
Find.

Note: When you choose to delete a draft allocation run, Oracle
Projects submits the concurrent process PRC: Delete Allocations
Transactions. Before submitting the request, Oracle Projects
ensures that no other request for the same rule and allocation run
combination is in a non-completed status.

You can customize the columns that are visible for several of the windows that are
displayed when you select one of the viewing options shown in the table above. For
more information on the fields you can choose, refer to the following table:

4-8 Oracle Project Costing User Guide

Window

Fields you can add using Folder Tools

Review Allocation Runs

Missing Amounts

Source Details

Transactions

Many fields, including Draft Request ID, Pool
Amount, Transaction Currency, parameters
for various aspects of allocation, basis,
missing amounts, offsets, and sources, and
others.

Project Amounts

Release Request ID

Task Name

Client Extension

Project Name

Task Name

Expnd Type

Project Name

Target Line Num

Task Name

For more information about adding folder fields, see: Customizing the Presentation
of Data in a Folder, Oracle Applications User’s Guide.

Troubleshooting Allocation Runs

If the pool amount for an allocation run is different from what you anticipate, check for
one or more of the following conditions:

• If you specify a percentage to allocate from a resource list (in the Resources

window), the rule calculates the pool amount using both the percentage specified
in the Allocation Pool % field (Sources window) and the percentage specified in
the Resources window.

• The amount included in the source pool can change each time you run

the allocation. To create a stable source pool, define each project and task
individually, either by specifying the source project and tasks in the Project Sources
region in the Sources window, or by using a fixed amount as the source.

• For any run period, the rule creates the allocation pool during the time period defined
by the amount class and run period. The amount class is based on the allocation
period type (Allocation Rule window) and the amount class (Sources window).

For more information, see: Defining Allocation Rules, Oracle Projects Implementation
Guide.

Viewing Allocation Transactions

You can view individual the individual transaction (expenditure items) created by the
PRC:Generate Allocations Transactions process.

To view individual allocation transactions:

1. Navigate to the Find Project Expenditure Items or Find Expenditure Items window.

Allocations

4-9

2. Enter the Project Number and Transaction Source fields. You can also enter other

fields to further limit your search.

3. Choose Find.

To query by batch name:

1. Navigate to the Find Expenditure Batches window.

2.

In the Batch field, enter the name of the batch you want to see and then choose Find.

Reversing Allocation Runs

You can reverse any successful allocation run (that is, the status is Release Success). The
reversal creates reversing expenditure items. If expenditure items have been transferred
or split before reversal, then the rule reverses the transferred or split items. The reversal
process creates reversal entries in the allocation history, so that the reversed amounts
are considered for the next incremental allocation, if any.

Note: Reversing the allocation run reverses all of the transactions. You
cannot reverse individual transactions. You cannot reverse an allocation
run if any of the target projects in the run cannot accept new transactions.

To reverse an allocation run:

1. Navigate to the Review Allocation Runs window

2.

3.

Select an allocation run that has a status of Release Success, and then choose Reverse.

In the Reverse an Allocation Run window, enter the parameters:

• For Reversed Exp Batch, enter a name for the reversing expenditure batch.

• For Reversed Offset Exp Group, enter a name for the reversing offset batch, if

any. (This field appears only for rules that specify an offset.)

• Choose OK.

Full and Incremental Allocations

The allocation method is an attribute of every allocation rule and affects how
the rule collects and allocates amounts. You choose whether you want a rule
to use full or incremental allocation on the Allocation Rule window. For more
information, see: Naming the Allocation Rule, Oracle Projects Implementation Guide.

Full allocations distribute all the amounts in the specified projects in the specified amount
class. The full allocation method is generally suitable if you want to process an allocation
rule only once in a run period.

Warning: Plan to run allocation rules that are set up for full allocation
only once in a run period. If you generate allocation transactions using
a full allocation rule more than once in a run period, you will create
duplicate transactions in your target projects. If this happens, you can
reverse the duplicates. See: Reversing Allocation Runs, page 4-10.

Incremental allocations create expenditure items based on the difference between the
transactions processed in the previous and current run. This method is generally

4-10 Oracle Project Costing User Guide

suitable if you want to use the allocation rule in allocation runs several times in a given
run period.

Note: Incremental allocations may slow system performance because of
the need to calculate the amounts allocated in previous runs.

The system keeps track of the results of previous incremental allocation
runs. Therefore, you can run an incremental allocation multiple times within the same
run period without creating duplicate transactions for target projects. You can review
and delete draft runs until you are satisfied with results.

Both full and incremental allocation distribute all the amounts accumulated during the
run period.

About Previous Amounts and Missing Amounts in Allocation Runs

Previous amounts and missing amounts occur only during incremental allocation
runs, and are significant only for the second and subsequent run in the same run
period. Full allocation runs do not have or use previous or missing amounts.

Previous amounts are those amounts that have been allocated in a previous run. For the
second and subsequent runs for the same time period, the rule allocates only differences
from the previous run or additional expenditures.

Missing amounts occur when a source, target or offset project or task has been closed
or has become inactive since the previous allocation run. During subsequent runs, the
system tracks the missing amounts, so that the source, target or offset amounts will be
accurate. Source amounts may be missing because:

• The task is closed, perhaps because the task has been completed

• The source line on which a task appears has been excluded (by selecting the Exclude

check box for that line on the Sources window)

• An attribute, such as the service type or task organization, has changed

AutoAllocations

To generate allocations more efficiently, you can group allocations rules and then run
them in a specified sequence (step-down allocations) or at the same time (parallel allocations).

Related Topics

Overview of Allocations, page 4- 1

Setting Up for AutoAllocations, Oracle Projects Implementation Guide

Creating AutoAllocations Sets

AutoAllocations is an Oracle General Ledger and Oracle Projects feature. In General
Ledger, the allocation definition is called a batch. In Projects, the allocation definition is
called a rule.

Step-down allocations use the results of each step in subsequent steps of the autoallocation
set. Oracle Workflow controls the flow of the autoallocations set.

Allocations

4-11

Parallel allocations carry out the specified rules all at once and do not depend on previous
allocation runs.

As shown in the following tables, each rule or batch has a different effect when you
run the autoallocation set, depending on the set type. The following table shows the
processes submitted by set type for project allocation rules.

Set Type

Step Down

Parallel

Processes Submitted

Generate Allocations Transactions

Release Allocation Transactions

Distribute Miscellaneous Costs and Usages

Update Project Summary Amounts

Generate Allocations Transactions

Release Allocation Transactions (Note: The
system submits this process only if Auto
Release is selected on the Allocation Rule
window.)

The following table shows the processes submitted by set type for mass allocation, mass
budget, mass encumbrances, and recurring journal allocation batches:

Set Type

Step Down

Parallel

Processes Submitted

Run MassAllocations

Recurring Journal Entry

Budget Formulas

Posting

Run MassAllocations

Recurring Journal Entry

Budget Formulas

What you can do with AutoAllocations depends on the responsibility you use when you
log on to your database:

• From the Projects responsibility, you can:

• Create autoallocation sets that contain Projects allocation rules. If Oracle Projects
is integrated with General Ledger, you can also include GL allocation batches.

• View autoallocation sets that were created using the Oracle Projects responsibility

• From the General Ledger responsibility, you can:

• Create autoallocation sets that contain only General Ledger batches

• View autoallocation sets that were created using the General Ledger

responsibility

For more information about AutoAllocations in Oracle General
Ledger, see: AutoAllocations, Oracle General Ledger User Guide.

4-12 Oracle Project Costing User Guide

Prerequisites

• If you want to allocate amounts from Oracle General Ledger, integrate Oracle

General Ledger with Oracle Projects. See: Integrating with Oracle General Ledger,
Oracle Projects Fundamentals. (You can use AutoAllocations in a standalone
installation of Oracle Projects.)

• (Step-down allocations only) AutoAllocations uses Oracle Workflow processes to
carry out step-down allocations. Although you can use the workflow without
modification, you can customize some processes. See: Step-Down Allocations
Workflow, Oracle Projects Implementation Guide.

• Set the directory for the debug log written by Oracle Workflow. You set the directory
in two places, the PA: Debug Log Directory profile option (see: PA: Debug Log
Directory, Oracle Projects Implementation Guide), and the init.ora file.

Submitting an AutoAllocation Set

The procedure below describes how to submit a request from the AutoAllocation
Workbench.

To submit the process:

1. Using the Projects responsibility, navigate to the AutoAllocation Workbench window.

2.

In the Allocation Set field, find the set that you want to submit. (You can choose
Find, Find All, or one of the Query commands from the View menu.)

3. Choose Submit or Schedule.

The Parameters window opens.

4. Enter information for this autoallocation set. The fields displayed vary depending
on whether the allocation set contains Oracle Projects rules, General Ledger
batches, or both.

The following table lists fields for General Ledger batches and describes the
information you can enter.

Allocations

4-13

If the Parameters window displays...

Then do this...

Name

Period

Nothing - field is for display only.

Select or enter an accounting period for your
GL batches.

Budget (Optional)

Select or enter a budget.

Journal Effective Date

Select a date.

Calculation Effective Date

Usage

Note: You can specify any date if the
profile option GL: Allow Non-Business Day
Transactions is set to Yes. Otherwise, specify
a business date.

Select a date in any open, future (that can
be entered), closed, or permanently closed
period. The default is the closest business
day in the chosen period.

Select Standard Balances or Average
Balances

Note: The system displays the Journal Effective Date, Calculation
Effective Date, and Usage fields for General Ledger batches when
General Ledger uses an average balance set of books.

The following table lists fields for Oracle Projects rules and describes
the information you can enter.

If the Parameters window displays...

Then do this...

GL Period

PA Period

Select a period.

If the project rules belong only to the GL
period type, enter only the GL Period
field. Otherwise, enter both fields. If all
project rules belong only to the PA period
type, enter only the PA Period field.

Expenditure Item Date

Select or enter the expenditure item date for
your allocations transactions.

5. Choose Submit or Schedule. If you are scheduling the process to run at a later

time, select a date and time, and then choose Submit.

Troubleshooting AutoAllocations

If a step down autoallocation set appears to run, but stops before executing all steps
and the process does not generate any exceptions, then check for one or both of the
following conditions:

• The Auto Release setting for the allocation rule, timeout setting, and Oracle
Workflow notification parameters may be interacting in a way that stops the
autoallocation run.

4-14 Oracle Project Costing User Guide

If Auto Release is deselected on the Allocation Rule window, then Oracle Workflow
processes the allocation rule. The workflow timeout attribute (set to a certain
number of minutes) executes three times. If the person notified by the workflow
does not respond in that amount of time, the step down autoallocation stops at that
point in the autoallocation set. See: Processes for the PA Step Down Allocation
Workflow, Oracle Projects Implementation Guide; and Timeout Attribute, Oracle Projects
Implementation Guide.

• The directory used for the debug log written by Oracle Workflow is set

incorrectly. Set the utl_file_dir parameter in the init.ora file to the same directory
that is specified in the PA: Debug Log Directory profile option (see: PA: Debug Log
Directory, Oracle Projects Implementation Guide). If the two do not match, the PA Step
Down Allocation workflow will fail (return an exception).

Viewing the Status of AutoAllocation Sets

To view the status of an autoallocation set:

1. Using the Projects responsibility, navigate to the View AutoAllocation Statuses

window.

2.

Select the set you want to view and then choose a Find or Query command from
the View menu.

For more information about finding records, see: Using Query Find, Oracle
Applications User’s Guide.

3. To see the Allocation Workbench for this set, choose Allocation Workbench. As

shown in the following table, you can see more information about a step by selecting
the step, and then selecting an option:

Allocations

4-15

To see more information about...

Choose...

A step

Step Detail

The workflow process for the step

Monitor Workflow

4-16 Oracle Project Costing User Guide

5
Asset Capitalization

This chapter describes how to create and maintain capital projects in Oracle Projects. It
provides a brief overview of capital projects and explains how to create, place in
service, adjust, and account for assets and retirement costs in Oracle Projects.

This chapter covers the following topics:

• Overview of Asset Capitalization

• Defining and Processing Assets

• Asset Summary and Detail Grouping Options

• Reviewing and Adjusting Asset Lines

• Capitalizing Interest

Overview of Asset Capitalization

Using capital projects, you can define capital assets and capture construction-in-process
(CIP) and expense costs for assets you are creating. When you are ready to place assets
in service, you can generate asset lines from the CIP costs and send the lines to Oracle
Assets for posting as fixed assets.

You can also define retirement adjustment assets and capture cost of removal and
proceeds of sale amounts (collectively referred to as retirement costs, retirement
work-in-process, or RWIP) for assets you are retiring that are part of a group asset in
Oracle Assets. When your retirement activities are complete, you can generate asset lines
for the RWIP amounts and send the lines to Oracle Assets for posting as adjustments to
the accumulated depreciation accounts for the group asset that corresponds to each asset.

About Capital Projects

You use capital projects to capture the costs of capital assets you are building, installing, or
acquiring. You also use capital projects to create retirement adjustment assets that you
associate with a group asset in Oracle Assets. You use a retirement adjustment asset to
capture the costs of removing, abandoning, or disposing of assets you want to retire. You
can set up capital projects to capture capital asset costs only, retirement costs only, or
to capture both capital asset costs and retirement costs.

Using Capital Projects to Create Capital Assets

You define and build capital assets in capital projects using information specified in the
project work breakdown structure (WBS). You define asset grouping levels and assign
assets to the grouping levels to summarize the CIP costs for capitalization.

Asset Capitalization

5-1

You can review and adjust capital project costs before and after capitalization. For
example, you can allocate costs collected under common tasks to multiple CIP assets
before you place them in service. You can also account for additional costs incurred
after capitalization, since Oracle Projects allows you to place assets in service before
completion of a project.

When a CIP asset is ready to be placed in service, you send the capital project amounts
to Oracle Assets as asset lines. Oracle Assets places the asset lines in a holding area
where your fixed assets department can post the capital costs in Oracle Assets as fixed
assets. You can review detail transactions associated with the asset lines in Oracle Projects
and Oracle Assets. If necessary, you can reverse capitalize an asset in a capital project.

Using Capital Projects to Process Retirement Costs

You capture retirement costs in a capital project by recording cost of removal and
proceeds of sale amounts to a task that is designated as a retirement cost task. To
distinguish cost of removal and proceeds of sale amounts, you must enter proceeds of
sale amounts using expenditure types that you define to specifically classify these
amounts. Oracle Projects automatically classifies amounts for all other expenditure types
as cost of removal. For more information, see: Defining Proceeds of Sale Expenditure
Types, Oracle Projects Implementation Guide.

To associate retirement costs with a group asset in Oracle Assets, you create a retirement
adjustment asset in the capital project and identify it with a specific group asset. As with
capital assets, you define asset grouping levels and assign retirement adjustment assets
to the grouping levels to summarize the retirement cost amounts for posting to Oracle
Assets. For more information, see: Creating a Retirement Adjustment Asset, page 5-10.

When retirement activities are complete, you generate asset lines for the retirement
cost amounts and send the lines to Oracle Assets for posting as adjustments to the
accumulated depreciation accounts for the group assets. To communicate notice of an
asset retirement to Oracle Assets, you can optionally initiate retirement requests in
Oracle Projects that are automatically passed to Oracle Assets.

Important: To use Oracle Projects retirement cost processing windows
and features, the value of the site-level profile option PA: Retirement Cost
Processing Enabled must be set to Yes. For more information, see: Profile
Options in Oracle Projects, Oracle Projects Implementation Guide.

Capital Projects Processing Flow

The Following illustration shows the processing flow for capital projects.

5-2 Oracle Project Costing User Guide

Capital Projects Processing Flow

Related Topics

You can enter expenditure items for CIP and RWIP amounts directly to capital projects
from within Oracle Projects. You also can collect supplier invoice costs for your
capital projects from Oracle Payables. When you are ready to place a CIP asset in
service, you can send the associated CIP asset lines to Oracle Assets to become fixed
assets. When you are ready to retire an asset in Oracle Assets, you can send the
associated RWIP asset lines to Oracle Assets and post the lines as group depreciation
reserve account adjustments. You use AutoAccounting in Oracle Projects to post entries
to the appropriate accounts in Oracle General Ledger.

Integrating with Oracle Purchasing and Oracle Payables (Requisitions, Purchase
Orders, and Supplier Invoices), Oracle Projects Fundamentals

Integrating with Oracle General Ledger, Oracle Projects Fundamentals

Integrating with Oracle Assets, page 7-31

Specifying a Retirement Date for Retirement Adjustment Assets, page 5-18

Creating and Preparing Asset Lines for Oracle Assets, page 5-19

Sending Asset Lines to Oracle Assets, page 5-26

Processing Pre-Approved Expenditures, page 2-10

Capitalizing Interest, page 5-37

Overview of AutoAccounting, Oracle Projects Implementation Guide

Placing an Asset in Service, page 5-18

Creating and Preparing Asset Lines for Oracle Assets, page 5-19

Asset Capitalization

5-3

Creating Purchase Orders for Capital Projects

When you create a purchase order for a capital project in Oracle Purchasing, you can
enter a project, task number, and expenditure type for each project-related distribution
line. You match this purchase order to an invoice in Oracle Payables, and then send
the appropriate lines to Oracle Projects.

You can use the asset category to assign an inventory item’s cost on a purchase order
to an asset on a capital project in Oracle Projects. You define default asset categories
for inventory items in Oracle Purchasing. After you match the purchase order to
an invoice, and interface the invoice from Oracle Payables, Oracle Projects assigns
the inventory item’s cost to an asset on the project that has the same asset category
as the inventory item.

If you assign purchase order distribution lines to asset clearing accounts instead of
projects, Oracle Payables matches the purchase order to an invoice and sends the lines to
Oracle Assets using the Mass Additions Create process.

If both a project and an asset clearing account are used in the distribution line, the
following occurs:

• If the project is a capital project:

• Oracle Payables posts the costs to the asset clearing account and the costs remain

there until you place the asset in service in Oracle Projects.

• You can send the costs to Oracle Projects after you post the invoice to Oracle

General Ledger.

• You cannot send costs to Oracle Assets from Oracle Payables when you run

the Mass Additions Create process.

• If the project is a contract or indirect project:

• Oracle Payables posts the costs to the asset clearing account and, if you have
sent the costs to Oracle Projects, Oracle Assets interfaces the costs to an asset
cost account when you post the transaction from Oracle Assets to Oracle
General Ledger.

• You can send the costs to Oracle Projects after you post the invoice to Oracle

General Ledger.

• You can send costs to Oracle Assets from Oracle Payables when you run the

Mass Additions Create process.

A distribution line can have both a project and an asset clearing account only if the
Account Generator process is set up to create the asset clearing account as the
account segment, or if you enter the distribution line manually.

Charging Supplier Invoice Lines to Projects

The procedure for sending supplier invoice lines to Oracle Assets depends on whether or
not the lines are associated with a capital project.

If the Invoice is Associated with a Capital Project

CIP and RWIP Lines: You cannot send supplier invoice lines directly from Oracle
Payables to Oracle Assets if the invoice lines are associated with a capital project and are
CIP or RWIP lines. Instead, in Oracle Payables you must do the following:

• Create the distribution lines on a supplier invoice

5-4 Oracle Project Costing User Guide

• Post the distribution lines to Oracle General Ledger.

In Oracle General Ledger, your Account Generator setup determines to which
accounts the invoices are posted. The usual practice is to charge capital projects to
asset clearing accounts.

• Interface those lines to Oracle Projects

Then, in Oracle Projects, place your CIP assets in service, specify retirement dates for any
retirement adjustment assets, and interface the costs to Oracle Assets.

Expense Lines: You can send distribution lines from Oracle Payables directly to
Oracle Assets using the Mass Additions Create process. See: Mass Additions Create
Program, Oracle Payables User Guide.

If the Invoice is Associated with a Contract or Indirect Project

You can send supplier invoice lines that are associated with contract or indirect projects
directly from Oracle Payables to Oracle Assets. To do so, use the Mass Additions Create
process. See: Mass Additions Create Program, Oracle Payables User Guide.

In Oracle General Ledger, your Account Generator setup determines to which accounts
the invoices are posted. The usual practice is to charge contract and indirect projects to
an asset account.

Charging Labor, Expense Reports, Usages, and Miscellaneous Transactions to Capital Projects

You can enter labor, expense reports, asset usage, and miscellaneous transactions for
your capital projects in Oracle Projects. You can set up Oracle Projects to calculate
and record capitalized interest for CIP assets that require an extended amount of
time to prepare for their intended use. The Distribute Labor, Expense Report, and
Usage and Miscellaneous Costs processes charge the capital project costs to a CIP or
RWIP account in Oracle General Ledger. Your AutoAccounting setup determines these
accounts. Oracle Projects is the subsidiary ledger for your CIP and RWIP accounts in
Oracle General Ledger. You can review the details for your CIP and RWIP accounts by
querying your capital projects in Oracle Projects.

Placing CIP Assets in Service

You enter a date placed in service for the CIP assets that are completed for a capital
project. Then, you can run the Generate Asset Lines process, which uses the grouping
method and levels you define to summarize all costs (supplier invoice, labor, expense
reports, usages, and miscellaneous transactions) into asset lines. You associate these asset
lines with one or more assets and send the lines to Oracle Assets to become fixed assets.

Creating Fixed Assets from Capital Projects

You run the Interface Assets process to send asset lines from Oracle Projects to Oracle
Assets. This process merges the asset lines into one mass addition line for each asset. The
mass addition line appears in the Prepare Mass Additions Summary window in Oracle
Assets as a merged parent with a cost amount of zero and a status of MERGED. The
line description is identical to the description of the supplier invoice expenditure item
in Oracle Projects.

The following table shows an example of asset lines in Oracle Assets for an asset
interfaced from Oracle Projects. When you submit the Post Mass Additions
process, Oracle Assets assigns the same asset number to these lines. See: Group Supplier
Invoices in Project Types: Capitalization Information, Oracle Projects Implementation Guide.

Asset Capitalization

5-5

Description

Cost

Merge Parent

Category

Queue

POST

MERGED

MERGED

CELL RADIO

0.00

COMPUTER
SERVICES

OTHER EX
PENSES

3,442.00

1,150.00

MERGED

LABOR

22,332.00

MERGED

MATERIAL

19,251.00

Yes

No

No

No

No

EQUIPMENT.
TRANSMISSION

EQUIPMENT.
TRANSMISSION

EQUIPMENT.
TRANSMISSION

EQUIPMENT.
TRANSMISSION

EQUIPMENT.
TRANSMISSION

If you completely defined the asset in Oracle Projects and it is ready for posting, then
Oracle Assets places the mass addition in the POST queue. If the asset definition is not
complete, then Oracle Assets places the mass addition in the NEW queue. To complete
the asset definition, you must enter the additional information in the Prepare Mass
Additions window. After the asset definition is complete, you can update the queue
status to POST. You do not need to change the queue status for lines with a status
of MERGED.

Use the Post Mass Additions process to create fixed assets from your mass addition
lines. When you run the Create Journal Entries program, Oracle Assets creates journal
entries to the appropriate CIP and asset cost accounts in Oracle General Ledger. For CIP
assets, the CIP account comes from the asset lines generated in Oracle Projects and the
asset account comes from the asset category associated with the asset.

Sending Retirement Costs to Oracle Assets

The process flow for sending retirement costs to Oracle Assets is similar to that for
placing CIP assets in service and sending CIP asset lines to Oracle Assets. When
retirement activities are complete and you are ready to interface the retirement cost
amounts to Oracle Assets, you must specify a date retired and ensure that a valid Oracle
Assets group asset number is specified for the retirement adjustment asset.

You submit the Generate Asset Lines process to create retirement cost lines for each
retirement adjustment asset and expenditure type grouping (cost of removal and
proceeds of sale). After you generate asset lines, you submit the Interface Assets
process to post the retirement adjustment asset lines to the accumulated depreciation
accounts for each group asset.

Accounting for Asset Costs in Oracle Projects and Oracle Assets

You use AutoAccounting to define the accounting for your project costs in Oracle
Projects. For capital projects, you must define AutoAccounting to account for
CIP, RWIP, and expensed costs.

When you use Oracle Projects to track your capital projects, Oracle Projects acts as a
subsidiary ledger for CIP and RWIP costs, and Oracle Assets acts as a subsidiary ledger
for the capitalized asset costs and the accumulated depreciation account adjustments.

5-6 Oracle Project Costing User Guide

As you charge costs to a capital project, you create journal entries and post the entries to
Oracle General Ledger. As you send the costs to Oracle Assets, you create journal entries
to account for these transactions and also post them to Oracle General Ledger.

Example of Accounting for Asset Costs

In this example, a company creates a capital project to capture the costs of building a
new clean room and installing air quality monitors. As part of this project, several air
quality monitors are being removed and retired from an existing clean room that is
being designated for other uses.

Accounting for Capital Project Costs

The following table shows the supplier invoice and expenditure item amounts charged
to the capital project.

Project Cost Details

Amounts

Supplier invoice for architectural drawings

Supplier invoice for building contractor

Supplier invoice for building permit penalty

Subtotal

Supplier invoice for new air quality monitors

Total supplier invoice costs

Employee labor for construction project management

Employee expense report for miscellaneous costs

Usage for use of company car

Total construction costs

Employee labor for removing old air quality monitors

Total project costs

2,000.00

5,500.00

200.00

7,700.00

2,500.00

10,200.00

1,400.00

250.00

55.00

11,905.00

500.00

12,405.00

Account for Supplier Invoice Transactions

You post supplier invoice transactions from Oracle Payables to Oracle General Ledger
before sending them to Oracle Projects. Workflow determines the journal entry in the
following table for the supplier invoice transactions sent to Oracle Projects.

Account

CIP - Clean Room

CIP - Air Quality Monitors

Accounts Payable Trade

Debit

Credit

7,700.00

2,500.00

10,200.00

Asset Capitalization

5-7

Account for Expenditure Items Entered in Oracle Projects

You account for the employee labor, employee expense report, and usage transactions
you enter in Oracle Projects with the journal entry shown in the following table:

Account

CIP - Clean Room

RWIP - Air Quality Monitors - Cost of Removal

Debit

Credit

1,705.00

500.00

Payroll Liability

Expense Report Liability

Usage Clearing

Account for a Capital Cost Adjustment

1,900.00

250.00

55.00

After reviewing the project costs, you determine that you cannot capitalize the building
permit penalty that you recorded as part of the journal entry for the supplier invoice
transactions. To correct this, you change the original transaction from capitalizable to
non-capitalizable. Oracle Projects interfaces the supplier invoice transaction adjustment
to Oracle Payables when you submit the Distribute Supplier Invoice Adjustment
process. Oracle Payables then generates the adjustment entry shown in the following
table and posts the entry to Oracle General Ledger.

Account

Debit

Credit

Building Permit Penalty Expense

200.00

CIP - Clean Room

200.00

Note: After you post the adjustment transaction, the total amount in
Oracle General Ledger for the CIP - Clean Room account is 9,205.00.

Accounting for Asset Costs

Each asset line created by the Generate Asset Lines process has an associated general
ledger account. After you post the asset lines in Oracle Assets, you can run the Create
Journal Entries process to create journal entries to transfer the cost amounts from either
the CIP or RWIP account (as determined by the capital or retirement adjustment asset
lines) to the corresponding fixed asset account or accumulated depreciation account
(as determined by the asset category that is assigned to the capital or retirement
adjustment asset).

Account for Capital Assets

After the clean room is complete and the new monitors are installed, you place the assets
in service and interface the CIP asset lines to Oracle Assets. After you post the assets
in Oracle Assets, you submit the Create Journal Entries process to record the entry
shown in the following table:

5-8 Oracle Project Costing User Guide

Account

Assets - Clean Room

Assets - Air Quality Monitors

CIP - Clean Room

CIP - Air Quality Monitors

Debit

Credit

9,205.00

2,500.00

9,205.00

2,500.00

Account for Retirement Adjustment Assets

After the existing air quality monitors are removed, you specify a retirement date for the
retirement adjustment asset and interface the RWIP asset lines to Oracle Assets. You
submit the Create Journal Entries process to record the entry shown in the following
table:

Account

Debit

Credit

Accumulated Depreciation - Air Quality Monitors - Cost of
Removal

500.00

RWIP - Air Quality Monitors - Cost of Removal

500.00

Note: As the final step in the process of accounting for the asset
transactions illustrated in this example, you would initiate an asset
retirement transaction in Oracle Assets for the air quality monitors
that were removed from the clean room that is being taken out of
service. You would then create journal entries to account for the
retirement of the group asset cost associated with these monitors. For
more information on processing retirement transactions, see: Asset
Retirements, Oracle Assets User Guide.

Related Topics

Costing in Oracle Projects, page 1- 2

Overview of AutoAccounting, Oracle Projects Implementation Guide

Defining and Processing Assets

You can create capital assets and retirement adjustment assets using capital
projects. When a capital asset is ready for use, you can place it in service in Oracle
Projects and send the project asset information and asset cost amounts to Oracle Assets
for posting as a fixed asset. When you retire an asset that is associated with a group asset
in Oracle Assets, you can enter a retirement date for the retirement adjustment asset in
Oracle Projects and send the retirement cost amounts to Oracle Assets for posting as an
adjustment to the accumulated depreciation accounts for the group asset.

Creating Assets in Oracle Projects

After you create a capital project, you can create capital assets for assets you want to
place in service as fixed assets. You can also create retirement adjustment assets to

Asset Capitalization

5-9

collect retirement costs for assets you want to retire that are associated with a group
asset in Oracle Assets.

You can define capital assets and retirement adjustment assets separately in
different projects or together in the same project. You can define assets from either
the Capital Projects window or from the Projects, Templates window. For more
information, see: Defining Assets, page 5-13.

Creating a Capital Asset

You create capital assets and accumulate costs for fixed assets you are
building, installing, or acquiring. You define an asset in Oracle Projects for each capital
asset you want to place in service. To interface a capital asset to Oracle Assets, you must
specify an in- service date for the asset in Oracle Projects. For a complete list of attributes
you can define for assets, see: Asset Attributes, page 5-14.

Creating a Retirement Adjustment Asset

You create retirement adjustment assets to collect cost of removal and proceeds of
sale amounts for assets associated with a group asset in Oracle Assets that you are
retiring, removing, abandoning, or otherwise disposing.

When you define a retirement adjustment asset in Oracle Projects, you must specify a
valid Oracle Assets group asset identifier as the target asset. You can create retirement
adjustment assets and interface retirement costs to Oracle Assets only for fixed assets that
are classified as group assets in Oracle Assets. To interface a retirement adjustment asset
to Oracle Assets, you must specify a retirement date for the asset in Oracle Projects. For a
complete list of attributes you can define for an asset, see: Asset Attributes, page 5-14.

Processing Retirement Requests

You can initiate a retirement request in Oracle Projects to identify one or more assets that
you are retiring from service. Retirement requests serve as an advice that you can use to
notify your fixed asset department about assets that need to be retired in Oracle Assets.

To process a retirement request:

1. Navigate to the Capital Projects window and choose the Requests button to open the

Retirement Requests window.

2. Choose the Create New Request button to open the Mass Retirements window and

specify any combination of asset attributes to find one or more assets you want to
retire.

3.

Save your work.

After a retirement request is processed in Oracle Assets, you can return to the Retirement
Requests window in Oracle Projects to view the retirement information.

To view retirements:

1. Navigate to the Capital Projects window and choose the Requests button to open the

Retirement Requests window.

2.

Select a retirement transaction you want to view and choose View Retirements.

5-10 Oracle Project Costing User Guide

Capital Project Flow

The following illustration shows the capital projects flow in Oracle Projects before you
send asset lines to Oracle Assets. The steps shown in this flow are described in the
text that follows the diagram.

Capital Project Flow

To create an asset in Oracle Projects:

1. Create a new capital project and WBS using a project template whose project type is
set up for a capital project. Update project and task details if necessary. See: Creating
a New Template, Oracle Projects Fundamentals.

You can also create assets when you copy an existing capital project. Assets
associated with the existing project are copied to the new project, along with asset
assignments. See: Creating a New Project from a Project Template or Existing
Project, Oracle Projects Fundamentals.

2. Update the Transaction Controls, as appropriate, including which transactions can
be capitalized by employee, expenditure category, expenditure type, or non-labor
resource. See: Specifying Which Capital Asset Transactions to Capitalize, page 5-12.

3. Collect CIP, RWIP, and expensed costs for your capital project and make adjustments

if necessary.

4. Define CIP and retirement adjustment assets if necessary. See: Defining Assets,
page 5-13. You can define assets manually or using project asset APIs. For more
information see: Oracle Projects APIs, Client Extensions, and Open Interfaces Reference.

Asset Capitalization

5-11

5.

6.

Specify asset grouping levels and grouping level types within the WBS. You can
then associate assets with the various grouping levels. See: Assigning Assets to
Grouping Levels, page 5-28.

Specify the date in service for completed CIP assets or the date retired for retirement
adjustment assets. See: Placing an Asset in Service, page 5-18, and Specifying a
Retirement Date for Retirement Adjustment Assets, page 5-18.

7. Optionally, define capital events to control how assets and costs are grouped, and

placed in service or retired. See: Creating Capital Events, page 5-20.

8. Generate Asset Lines. Review asset cost lines and make any necessary

adjustments. See: Generating Summary Asset Lines, page 5-21.

9. Run the Interface Assets process. See: Sending Asset Lines to Oracle Assets,

page 5-26.

Specifying Which Capital Asset Transactions To Capitalize

For capital assets, you must specify whether to capitalize or expense each transaction
charged to a capital project. The capitalizable classification is similar to the billable
classification for transactions charged to a contract project. The task and transaction
controls you define determine the default value for this classification.

Note: You cannot make an election on how to account for retirement
costs you record to a retirement adjustment asset. Oracle Projects
automatically classifies retirement costs as cost of removal or proceeds
of sale amounts based on the expenditure type you use to record
retirement transactions.

To specify the level at which a capital asset transaction is capitalized:

1. Decide at which level you want to specify if a transaction can be capitalized, then

navigate to the appropriate window, as shown in the following table:

Control Level

Entire Task

Employee

Window

Task Details

Transaction Controls

Expenditure Category

Transaction Controls

Non-Labor Resource

Transaction Controls

Expenditure Item

Expenditure Items (Tools menu)

2.

3.

Related Topics

Select the Capitalizable check box for the task control level you want.

Save your work.

Controlling Expenditures, page 2-24

Transaction Controls, Oracle Projects Fundamentals

Copying Assets, page 5-13

5-12 Oracle Project Costing User Guide

Defining Assets

To define a CIP and retirement adjustment assets for a capital project, you enter asset
information, such as the asset name, asset number, book, asset category, and date
placed in service or date retired. For a complete list of attributes you can define for an
asset, see: Asset Attributes, page 5-14.

When you create a capital project type, you can specify whether a complete
asset definition is required in Oracle Projects before you can place the asset in
service. See: Project Types, Oracle Projects Implementation Guide.

To define assets in the Capital Projects window:

1. Navigate to the Capital Projects window.

2.

3.

4.

In the Find Capital Projects window, find the capital project for which you want
to define assets.

In the Capital Projects window, choose Assets.

In the Assets window, select either the Capital Project Assets Workbench or the
Retirement Adjustment Assets Workbench.

5.

Select or enter asset information in each tab of the Assets window.

Tip: To view and enter all attributes for an asset in a single
window, choose the Open button on the Assets window to open the
Asset Details window.

To create an asset, you must enter at least the Asset Name and
Description. To create a retirement adjustment asset, you must also
enter a valid group asset identifier in the Target Asset field.

6.

Save your work.

To define assets in the Projects window:

1. Navigate to the Projects window.

2.

In the Find Projects window, find the capital project for which you want to define
assets.

3.

In the Projects, Templates Summary window, choose Open.

The Project, Templates window opens.

4. For Options, choose Asset Information, Assets.

5. Enter information for an asset. You can use the down arrow key or Edit, New Record
from the menu if you want to enter more than one asset for this capital project.

To create an asset, you must enter at least the Asset Name and Description. To create
a retirement adjustment asset, you must also enter a valid group asset identifier in
the Target Asset field.

6.

Save your work.

Copying Assets

To streamline the definition of multiple project assets that have similar attributes, you
can use the Copy Asset option on the Assets and Asset Details windows to copy assets
within a project. When you select an asset and choose the copy option, Oracle Projects
copies the selected asset to a new row and opens the Copy To window. The Copy To

Asset Capitalization

5-13

window prompts you to enter values for several key asset attributes that define a unique
asset. Oracle Projects prompts you to enter the following attributes on the Copy To page:

• Asset Name

• Asset Description

• Project Asset Type

When you copy an asset, Oracle Projects copies the asset with the same project asset
type. For estimated assets, you can optionally copy the asset as an as-built asset.

• Asset Date

The date you enter varies according to the project asset type you select. The date can
be an estimated date placed in service (Estimated project asset type), actual date
placed in service (As-Built project asset type), or a retirement date (Retirement
Adjustment project asset type).

• Units

Similar to the asset date, the unit amount you enter varies according to the project
asset type you select. The unit amount can be estimated units (Estimated project
asset type), actual units (As-Built project asset type), or retirement units (Retirement
Adjustment project asset type).

• Asset Number

When you enter attribute values in the Copy To window, you can also choose whether
to copy the asset assignments. However, you cannot use the Copy Assets feature to
copy asset lines or other asset information.

Asset Attributes

You must enter asset information when you define an asset in Oracle Projects. The
Interface Assets process sends all asset information to Oracle Assets except for the
asset name and estimated date in service. This section describes the attributes you
can define for assets in Oracle Projects.

Asset Name

Asset Number

Description

You must define a unique asset name for each asset within a project. You cannot
change the asset name after you place the asset in service or specify a retirement date
in Oracle Projects.

An asset number uniquely identifies each asset. You can enter a unique asset number, or
use automatic asset numbering in Oracle Assets during the Mass Additions process. You
cannot update this field after you send the asset to Oracle Assets.

If you enter an asset number, it must be unique and not in the range of numbers reserved
for automatic asset numbering in Oracle Assets. You can enter any unique number that is
less than the number in the Starting Asset Number field in the System Controls form, or
you can enter any non-numeric value.

Use this field to provide a description of the asset you are building. You cannot update
this field after you send the asset to Oracle Assets.

5-14 Oracle Project Costing User Guide

Asset Category

Asset Key

Book

Location

The asset category determines the default asset cost account and depreciation rules for
the asset after you send the asset to Oracle Assets. You cannot update this field after you
send the asset to Oracle Assets.

Oracle Projects provides you with a list of asset category values defined in Oracle Assets
and associated with the corporate book of the CIP asset. The asset category you choose
here is not displayed in the Asset Lines window.

You can define an asset key to group assets or identify groups of assets independently of
the asset category. This field does not have a financial impact.

The Book field defines the corporate depreciation book of the asset. Oracle Assets
determines default financial information from the asset category, book, and date placed
in service for your asset after you send it to Oracle Assets.

By default, this field displays the asset book defined in Oracle Projects Implementation
Options. You can override this value at the asset level. Oracle Projects provides you
with a list of corporate book values defined in Oracle Assets which match the Oracle
Projects set of books. You can have multiple corporate books associated with one set of
books in Oracle Assets.

The location identifies the expected physical location of the asset after it is placed in
service. Oracle Projects provides you with a list of valid locations defined in Oracle
Assets.

Project Asset Type

This field identifies whether an asset represents an Estimated or complete, As-Built
capital asset, or a Retirement Adjustment asset.

Event Number

This field identifies the capital event, if any, associated with the asset.

Estimated In-Service Date

Enter the date you estimate placing an asset in service. Use the Estimated In-Service
Date to query and review assets you expect to be in service.

Estimated Retirement Date

Enter the date you estimate retiring an asset from service. Use the Estimated Retirement
Date to query and review assets you expect to be retired.

Actual In-Service Date

This date represents the actual date you place an asset in service and begin using it. The
date can be in the current or a prior accounting period. You must specify an actual
in-service date for a completed asset in order to interface the asset to Oracle Assets. You
cannot change this date after you place the asset in service in Oracle Projects.

Asset Capitalization

5-15

You may want to begin creating and reviewing asset lines prior to the period you intend
to place the asset in service. You can enter a date in a future accounting period.

Note: The Interface Assets process automatically rejects an asset with
a future date in service.

Use this field to enter the date you retire an asset from service. You cannot change this
date after you interface a retirement adjustment asset to Oracle Assets.

Use this field to capture an estimate of the number of components that make up or
are installed for an asset.

The actual number of components for an asset. For example, if you build two assembly
machines, enter 2 units for the asset. You cannot update this field after you send the asset
to Oracle Assets. Oracle Projects uses the value in this field to allocate unassigned and
common costs to assets when you select an asset cost allocation method of Actual Units.

You can use this field to identify a parent asset for assets that you separately track and
manage as asset components.

You can use this field to specify an estimated cost for the asset. Oracle Projects uses the
value in this field to allocate unassigned and common costs to assets when you select an
asset cost allocation method of Estimated Cost.

Use this field to identify the manufacturer of an asset.

Use this field to identify the model number of an asset.

Use this field to capture the serial number of an asset. This number must be unique
for the manufacturer in Oracle Assets.

Use this field to enter a user-defined tracking number for an asset. This number must be
unique in Oracle Assets.

This field identifies the external asset management asset system from which an asset is
imported, if any.

Retirement Date

Estimated Units

Actual Units

Parent Asset

Estimated Cost

Manufacturer

Model Number

Serial Number

Tag Number

Product Source

5-16 Oracle Project Costing User Guide

Source Reference

The external asset management system identifier for an asset imported from an external
asset management asset system, if any.

Employee Name

The name of the employee responsible for the asset when it is placed in service (not
the project owner).

Employee Number

The employee number of the person responsible for the asset when it is placed in service.

Reverse

Capital Hold

Depreciate

You can select this check box to identify an asset you want to reverse.

You can select this check box to prevent any further costs from being charged to the asset.

Check the Depreciate check box if you want to depreciate the asset in Oracle Assets.

Amortize Adjustments

Check the Amortize Adjustments check box if you want to amortize the catchup
depreciation on a cost adjustment over the remaining life of the asset. If you do not check
Amortize Adjustments, Oracle Assets expenses the catchup depreciation expense for
the adjustment in one period.

If you check this check box, you cannot deselect it once the asset has been interfaced
to Oracle Assets.

Important: If you select this field and reverse capitalize the asset, Oracle
Assets will amortize the catch up depreciation on the negative
cost adjustment over the remaining life of the asset. Therefore, the
depreciation expense per period on the original asset cost will not match
the depreciation amount generated per period to account for the asset
cost reversal in Oracle Assets.

Target Asset

This field is displayed only for assets with a project asset type of Retirement
Adjustment. You must use this field to specify the group asset in Oracle Assets
that corresponds to the retirement adjustment asset for which you want to capture
retirement costs.

Depreciation Account

This field identifies the expense account to which you charge depreciation for a capital
asset. You must specify a book before you can enter a depreciation expense account. In
addition, you must specify a depreciation account for a capital asset before you can
interface the asset to Oracle Assets. You can optionally set up the Depreciation Account
Override Extension to automatically derive the depreciation expense account based on

Asset Capitalization

5-17

the book and asset category that you define for the asset. You cannot update this field
after you send the asset to Oracle Assets.

Related Topics

Asset Setup Information, Oracle Assets User Guide

Sending Asset Lines to Oracle Assets, page 5-26

Placing an Asset in Service

When a CIP asset is complete, you place it in service. If your project has more than one
CIP asset, you can place each asset in service as it is completed. You do not have to
complete the entire project to place an asset in service. You place an asset in service by
entering the Actual In-Service Date for the asset. Although you can collect expensed
costs for a capital project, you cannot capitalize these costs.

The Actual In-Service Date can be a past, current, or future date. After you enter the
date, generate and interface the asset lines. Oracle Assets will calculate and record how
much depreciation should have been taken for the asset.

To capitalize CIP asset costs:

1. Navigate to the Capital Projects window.

2. Find the capital project whose assets you want to place in service by entering

search criteria, such as estimated in service date, project name or number, project
type, organization, key member, or class code, in the Find Capital Projects window.

In the Capital Projects window, Oracle Projects displays the summarized
expensed, CIP and interfaced project costs for each capital project. The Update
Project Summary Amounts process updates expensed, CIP amounts; the Interface
Assets process updates the interfaced amount.

3. Choose the capital project you want and choose the Assets button.

4.

In the Assets window, select the Capital Project Assets Workbench option (if not
already displayed), and enter the Actual In-Service Date for the asset you are placing
in service.

Compare the Estimated In-Service Date to the Actual In-Service Date. If unreasonable
discrepancies exist, verify that the Actual In-Service Date for the asset is correct.

Note: You cannot send assets to Oracle Assets whose actual date
placed in service is later than the current Oracle Assets period date.

5. Enter a complete asset definition for the asset if you have set up Oracle Projects to

only allow complete definitions to be sent to Oracle Assets.

For a list of the fields required for a complete asset definition, see: Asset Attributes,
page 5-14.

6.

Save your work.

Specifying a Retirement Date for Retirement Adjustment Assets

When the activities associated with retiring, removing, abandoning, or disposing of an
asset are complete, you can specify a retirement date for the retirement adjustment asset
to signify the retirement. Specifying a retirement date enables you to generate asset lines

5-18 Oracle Project Costing User Guide

for the retirement costs captured in Oracle Projects. You can then interface the retirement
asset lines to Oracle Assets for posting to the accumulated depreciation accounts for
the associated group asset. If your project has more than one retirement adjustment
asset, you can retire each asset as retirement activities are completed.

To specify a retirement date for retirement adjustment assets:

1. Navigate to the Capital Projects window.

2. Find the capital project whose assets you want to retire by entering search

criteria, such as project name or number, project type, organization, key member, or
class code, in the Find Capital Projects window.

In the Capital Projects window, Oracle Projects displays the summarized
expensed, CIP, RWIP, and interfaced project costs for each capital project. The
Update Project Summary Amounts process updates expensed and CIP and RWIP
amounts; the Interface Assets process updates the interfaced amount.

3. Choose the capital project you want and choose the Assets button.

4.

In the Assets window, select the Retirement Adjustment Assets Workbench option
and enter the Retirement Date for the asset you are retiring.

Compare the Estimated Retirement Date with the actual Retirement Date. If
unreasonable discrepancies exist, verify that the Retirement Date for the asset is
correct.

5.

Save your work.

Creating and Preparing Asset Lines for Oracle Assets

After you place your capital assets in service and specify retirement dates for your
retirement adjustment assets, you can create, prepare, and send asset lines for the cost
amounts to Oracle Assets. First, you must run the Generate Asset Lines process to
create summary asset lines from the CIP and RWIP expenditure items and any cost
adjustments. Before you run the Interface Assets process, review and adjust your asset
lines if necessary. You can perform the following adjustments on your asset lines:

• Associate assets with unassigned asset lines

Note: You can set up your capital projects to automatically associate
assets with unassigned asset lines by defining an asset cost
allocation method. For more information, see: Allocating Asset
Costs, page 5-25.

• Change which asset is associated with a line

• Split an asset line into multiple asset lines and associate the new lines with different

assets

• Change the line description

Related Topics

Generate Asset Lines, Oracle Projects Fundamentals

Reviewing and Adjusting Asset Lines, page 5-32

Asset Capitalization

5-19

Creating Capital Events

You can create periodic and manual capital events to control how capital project assets
and costs are interfaced to Oracle Assets over time. You use capital events to group assets
and costs before you generate asset lines for capitalization and retirement cost processing.

When you use periodic event processing, you submit a concurrent process that
selects unprocessed assets and cost amounts for a project based on the in-service and
expenditure item dates you specify in the process parameters. When you use manual
event processing, you can specify the assets and costs that you want to include in the
event, as well as the in-service and expenditure item dates.

When you submit the Generate Asset Lines process for a capital project that uses capital
events, Oracle Projects automatically generates asset lines for all defined, unprocessed
capital events.

You can specify a default event processing method for a capital project type and override
it at the project level.

• For information on specifying an event processing method in the Capitalization
Information tab of the Project Types window, see: Project Types, Oracle Projects
Implementation Guide.

• To specify an event processing method for a project, select a processing method in
the Capital Information window for the project. For information, see: Capital
Information, Oracle Projects Fundamentals.

Creating Periodic Events

To create a periodic capital event, you must submit the PRC: Create Period Capital
Events process. For information, see: Create Periodic Capital Events, Oracle Projects
Fundamentals.

Creating Manual Events

You can create capital events from the Capital Projects window.

To create a capital event:

1. Navigate to the Capital Projects window.

2. Find the capital project for which you want to define a capital event in the Find

Capital Projects window.

3. Choose the capital project you want and choose the Capital Events button.

4.

5.

In the Capital Events window, select either the Capital Project Assets Workbench or
the Retirement Adjustment Assets Workbench.

Insert a new row to derive the (next) sequential event number, an event name, and
optionally select a different asset allocation method.

6.

Save your work.

7. To select assets for the event, choose the Assets button to open the Event Assets

window and choose Attach New Assets.

8.

In the Attach New Asset window, enter selection criteria to find one or more assets
to attach to the event and choose OK to return to the Event Assets window.

Note: To detach an asset after it is selected, you can deselect the
Include check box for the asset line. You can detach an asset from an

5-20 Oracle Project Costing User Guide

event if asset lines have not been generated for the event, or if all
asset lines for the event are reversed.

9.

Save your work and close the Event Assets window to return to the Capital Events
window.

10. To select costs for the event, choose the Costs button to open the Event Costs

window and choose Attach New Costs.

11. In the Attach New Costs window, enter selection criteria to find costs to attach to the

event and choose OK to return to the Event Costs window.

Note: To detach a cost item after it is selected, you can deselect the
Include check box for the cost line. You can detach a cost item from
an event if it has not been generated and grouped into an asset
line, or if all asset lines for the cost item are reversed.

12. Save your work and close the Event Costs window to return to the Capital Events

window.

13. To generate asset lines for the event, choose Generate. For more
information, see: Generating Summary Asset Lines, page 5-21.

You can view the status of the request in the Events window.

Note: You can optionally reverse all assets for the event by choosing
the Reverse button.

Generating Summary Asset Lines

The Generate Asset Lines process creates summarized asset lines for capital assets and
retirement adjustment assets.

• For capital assets, the process generates capital asset lines only from capitalizable
expenditure items on tasks that are assigned to a capital asset with an actual date
placed in service.

• For retirement adjustment assets, the process generates retirement adjustment asset
lines only from expenditure items on tasks that are marked as Retirement Cost
tasks, and are assigned to a retirement adjustment asset with a defined retirement
date.

Oracle Projects creates asset lines based on the asset grouping level you choose within a
project and the CIP grouping method you designate for the corresponding project
type. The grouping level represents the WBS level at which you assign assets or group
common costs.

You determine the grouping level by assigning assets to a WBS component (for
example, the project, a top task, or a lowest task), or by designating a WBS component as
a grouping level for common costs. For more information on grouping levels, see: Asset
Summary and Detail Grouping Options, page 5-27.

The CIP grouping method determines how Oracle Projects summarizes asset costs
within an asset grouping level. For example, you can choose to summarize asset costs
by expenditure type or expenditure category. For more information on specifying a
grouping method, see: Project Types, Oracle Projects Implementation Guide.

Asset Capitalization

5-21

The AutoAccounting rules you define for CIP and RWIP costs also influence the amount
of summarization. Oracle Projects creates asset lines by summarizing by grouping
level, grouping method, and CIP/RWIP account.

When more than one asset is assigned to a grouping level or common costs are entered
for a project, you must define an asset allocation method if you want Oracle Projects
to automatically assign all asset costs to assets. Otherwise, you must manually assign
any unassigned or common costs. For information on defining an asset allocation
method, see Allocating Asset Costs, page 5-25.

The following table describes how Oracle Projects maps costs to assets:

Number of assets assigned to a grouping
level

Expected results after running Generate
Asset Lines process

One asset assigned to a grouping level

All detail costs charged to that level are
automatically mapped to that asset.

More than one asset assigned to a grouping
level, only one asset is placed in service

If the asset allocation method specified for
the project has a value of None, then Oracle
Projects generates asset lines for all costs, but
does not assign an asset to the asset lines. If
the asset allocation method is other than
None, then Oracle Projects generates asset
lines for the grouping level. However, costs
are allocated and assigned only to the assets
being placed in service.

The cost distribution is for purchased goods
from a purchase order which has an inventory
item with a default asset category

Costs are mapped to the single asset that
matches the default asset category for that
grouping level.

More than one asset has the same asset
category as the default asset category for a
purchased item

When the asset allocation method specified for
the project has a value other than None, Oracle
Projects creates asset lines, and allocates costs
and assigns assets having the same default
asset category to the asset lines. When the asset
allocation method has a value of None, the
assets are not assigned automatically.

Example of Mapping Costs to Assets

For example, assume you assign one asset to a capital project at the project grouping
level. As shown in the following table, you charge the following expenditure items to the
project, all of which are capitalizable and charged to the same CIP account:

5-22 Oracle Project Costing User Guide

Expenditure Type

Expenditure Category

Amount

Supplies

Supplies

Professional

Clerical

Computer

Meals

Lodging

Air Travel

Operating

Operating

Labor

Labor

Service Center

Travel

Travel

Travel

Miscellaneous

Operating

Total Costs

5,000.00

20,000.00

5,800.00

1,500.00

14,000.00

300.00

500.00

900.00

5,000.00

53,000.00

If you use a grouping method of Expenditure Category, Oracle Projects creates the asset
lines shown in the following table:

Asset Lines

Labor

Operating

Service Center

Travel

Amount

7,300.00

30,000.00

14,000.00

1,700.00

If you use a grouping method of Expenditure Type, Oracle Projects creates the asset lines
shown in the following table:

Asset Capitalization

5-23

Asset Lines

Air Travel

Clerical

Computer

Lodging

Meals

Miscellaneous

Professional

Supplies

Amount

900.00

1,500.00

14,000.00

500.00

300.00

5,000.00

5,800.00

25,000.00

If you use a grouping method of All, Oracle Projects creates a single asset line for the
total cost amount of 53,000.00.

Prerequisites:

Before you run the Generate Asset Lines process, cost the transactions by running
the following processes:

• Distribute Labor Costs

• Distribute Expense Report Costs

• Distribute Usage and Miscellaneous Costs

• Distribute Supplier Invoice Adjustments

• Interface Supplier Invoices to Oracle Projects

• Distribute Total Burdened Costs (required if you are capitalizing burdened

costs). You do not need to interface these costs to Oracle General Ledger before
you create asset lines.

• Run the Update Project Summary Amounts process so you can see the total

expensed, CIP, and RWIP amounts in the Capital Projects window.

You can generate asset lines for a single project or capital event, and for a range of
projects.

To generate summary asset lines for a single project or capital event

1. Navigate to the Capital Projects or Capital Events window.

For capital events, select either the Capital Project Events Workbench or the
Retirement Cost Events Workbench to continue.

2. Find and select a capital project or capital event for which you want to generate

asset lines.

3. Choose the Generate button.

4. Enter the Asset Date Through. Oracle Projects creates asset lines from assets with an
actual date placed in service/retirement date before and including this date only.

5-24 Oracle Project Costing User Guide

5. For PA Through Date, enter the last day of the PA period through which you want

the costs to be considered for capitalization.

If you enter a date that falls within the PA period, the process uses the period
ending date of the preceding period. If the date you enter is the end date of a
period, the process uses the end date of that period, as shown in the example in the
following table:

Period

Start Date

End Date

You enter...

The process
uses...

P1

P2

07-Jun-99

13-Jun-99

19-Jun-99

13-Jun-99

14-Jun-99

20-Jun-99

20-Jun-99

20-Jun-99

6. Choose Include Common Tasks, if you want to create asset lines from costs assigned

to a grouping level type of Common Cost.

7. Choose OK to submit the Generate Asset Lines process. Oracle Projects creates asset

lines for your project or event and runs the Generate Asset Lines Report.

8. Review the Generate Asset Lines Report. See: Generate Asset Lines Report, Oracle

Projects Fundamentals.

You can also generate asset lines for a single project or capital event by submitting the
PRC: Generate Asset Lines for a Single Project process from the Submit Request window.

To generate summary asset lines for a range of projects:

Choose the PRC: Generate Asset Lines for a Range of Projects process in the Submit
Request window. In the Parameters window, enter a project or range of projects, date
placed in service/retirement date through, and PA through date. Also indicate if you
want to include common tasks. Choose Submit to generate asset lines and run the
Generate Asset Lines Report. Review the report to verify the creation of asset lines.

Allocating Asset Costs

You can specify an asset allocation method to enable Oracle Projects to automatically
allocate unassigned asset lines and common costs across multiple assets. Unassigned
asset lines typically occur when more than one asset is assigned to an asset grouping
level.

You can specify a default asset allocation method for a capital project type and override
it at the project level.

• For information on specifying an asset allocation method in the Capitalization
Information tab of the Project Types window, see: Project Types, Oracle Projects
Implementation Guide.

• To specify an asset allocation method for a project, select an allocation method in
the Capital Information window for the project. For information, see: Capital
Information, Oracle Projects Fundamentals.

You can select one of the following asset allocation methods:

• Actual Units: Costs are allocated based on the number of actual units specified for

each asset in the Assets window. See: Asset Attributes, page 5-14.

Asset Capitalization

5-25

• Client Extension: Costs are allocated based on the Asset Allocation Basis

extension. For information, see: Asset Allocation Basis Extension, Oracle Projects
APIs, Client Extensions, and Open Interfaces Reference.

• Current Cost: Costs are allocated based on the grouped CIP cost of each asset.

• Estimated Cost: Costs are allocated based on the estimated cost specified for each

asset in the Assets window. See: Asset Attributes, page 5-14.

• Standard Unit Cost: Costs are allocated based on a standard unit cost defined
for the asset book and category in the Project Assets Standard Unit Cost
window. See: Define Standard Unit Costs for Asset Cost Allocations, Oracle Projects
Implementation Guide.

• Spread Evenly: Costs are allocated evenly based on the number of assets being

capitalized for the project or the event.

Sending Asset Lines to Oracle Assets

Run the Interface Assets process to send valid capital asset and retirement adjustment
asset lines to Oracle Assets. Then, in Oracle Assets, you can review the mass addition
lines created from the project asset lines in the Prepare Mass Additions window. For
Oracle Projects to send asset lines to Oracle Assets, the asset line must meet these
specific conditions:

• The actual date in service or retirement date must fall in the current or a prior

Oracle Assets accounting period

• The CIP or RWIP costs for summarized asset lines must be interfaced to Oracle

General Ledger

• The CIP or RWIP costs for supplier invoice adjustments must be interfaced to

Oracle Payables

• A capital asset or retirement adjustment asset must be associated with the asset line

The process creates one mass addition line in Oracle Assets for each asset line in Oracle
Projects, assigning the asset information you entered for the asset in Oracle Projects
to the mass addition line in Oracle Assets. You use the Mass Additions process in
Oracle Assets to prepare and post these mass additions. If you did not enter all required
asset information in Oracle Projects, you must enter it for the line in the Prepare Mass
Additions window before you can post it.

In Oracle Assets you can query and review assets posted to Oracle Assets by project
number and task number in the Financial Inquiry window.

Prerequisites:

• Interface your capital project costs from Oracle Projects to Oracle General Ledger.

• Interface costs for your supplier invoice adjustments to Oracle Payables

• If you are sending cost adjustments for an asset from Oracle Projects to Oracle
Assets, ensure that the original mass addition was posted to Oracle Assets. If
the mass addition has not become an asset, the Interface process will reject the
adjustment line.

To send asset lines for a range of projects:

Choose PRC: Interface Assets process in the Submit Request window and enter the
project or range of projects, and the date placed in service/retirement date up to which

5-26 Oracle Project Costing User Guide

you want to process capitalized costs. Choose Submit to start the process and run the
Interface Assets Report.

Related Topics

Interface Assets, Oracle Projects Fundamentals

Overview of the Mass Additions Process, Oracle Assets User Guide

About the Mass Additions Interface, Oracle Assets User Guide

Mass Additions Reports, Oracle Assets User Guide

Asset Summary and Detail Grouping Options

This section describes how Oracle Projects summarizes expenditures items into asset
lines, how to group asset lines, and how to assign asset lines to assets.

Asset Grouping Levels

Grouping levels control how Oracle Projects summarizes expenditure items into asset
lines. You can group by project, top task, or lowest level task. For example, if you group
at the project level, Oracle Projects summarizes all capitalizable costs or retirement
costs at all task levels into asset lines at the project level. If you group at a top task
level, Oracle Projects summarizes all tasks below that top task into asset lines for that top
task. See: Assigning Assets to Grouping Levels, page 5-28.

If you have summarized the top task in the WBS branch, you cannot also summarize at
the lowest level. For example, if Top Task 1 is a grouping level, you cannot also group at
Task 1.1.1. If Task 2.2.1 is a grouping level, you cannot group at Top Task 2. If you group
at the project level, you cannot group at any top or lowest level task.

Note: You also use the grouping method assigned to your project type to
summarize expenditure items.

Grouping level types determine whether you can associate assets with the grouping level.

For examples of grouping levels and grouping level types, see: Examples of Asset
Grouping Levels, page 5-29 and Example of Asset Grouping Level Types, page 5-28.

Specifying Grouping Level Types

You can change the grouping level type at any time. If you change a grouping level type
from Specific Assets to Common Costs, Oracle Projects deletes existing asset assignments
from the grouping level. Changing the grouping level after you have interfaced assets
does not affect the asset lines previously sent to Oracle Assets.

To specify grouping level types:

1. Navigate to the Find Projects window and enter selection criteria for a capital project.

2.

Select a project and choose Open.

The Projects, Templates Summary window opens.

3. To group by project, select Asset Information (in the Options area), select Asset

Assignments, and then choose Detail.

Asset Capitalization

5-27

4. To group by task, choose Tasks (in the Options area). In the Find Tasks window, enter

selection criteria. In the Tasks window, select a task and then choose Options.

5. For the project or each task, choose a grouping level type:

6. Specific Assets: Select this option to associate assets with the project or task. The

Generate Asset Lines process generates asset lines from the specific assets and costs
you associate with this grouping level.

7. Common Costs: Select this option to group projects or tasks that capture costs you
want to allocate to multiple assets. You cannot associate assets with this grouping
level type. If you specify an asset allocation method for the project with a value other
than None, then the Generate Asset Lines process can allocate these costs across all
project assets. If you specify an asset allocation method of None, then the Generate
Asset Lines process creates unassigned asset lines for your common cost grouping
levels, and you must manually allocate these common costs across assets.

8.

Save your work.

Assigning Assets to Grouping Levels

To associate an asset with project costs, assign the asset to a grouping level.

Oracle Projects associates with the specified asset all the asset lines created from the
capital or retirement cost expenditure items for a grouping level. If you associate
multiple assets with the same grouping level, then you must specify an asset allocation
method (other than None) for the project to enable Oracle Projects to assign or allocate
the asset lines to the various assets. Otherwise, you must perform this task manually.

To assign assets to grouping levels:

1. Navigate to the Find Projects window, find your capital project, and then choose

Open.

The Projects, Templates window opens.

2.

Select a project and choose Open.

The Projects, Templates Summary window opens.

3. To group by project, select Asset Information (in the Options area), select Asset

Assignments, and then choose Detail.

4. To group by task, choose Tasks (in the Options area). In the Find Tasks window, enter
selection criteria. In the Tasks window, select a task and then choose Options. Assign
a specific asset for each task that is in a Specific Asset grouping level. In the Task
Options window, select Asset Assignment.

Note: You can assign assets only to grouping levels with a type of
Specific Assets.

5. Choose the assets you want to assign to the grouping level.

6.

Save your work.

Example of Asset Grouping Level Types

You set up a construction management or an administrative task to capture project
management activities. These costs do not apply to any specific asset. When the project
is complete, you use a standard procedure to split the costs over all the assets. You

5-28 Oracle Project Costing User Guide

associate these tasks with a grouping level so you can create asset lines from them, but
you use a grouping level type of Common Costs so you can use the Split Asset Lines
window to assign the costs to various assets manually.

Examples of Asset Grouping Levels

The following four illustrations show four possible variations of asset grouping levels
for the same project.

Each illustration shows that the project has two top tasks, Task 1 and Task 2.

• Task 1 has two subtasks, 1.1 and 1.2. These are the lowest tasks for Task 1.

• Task 2 has two subtasks, 2.1 and 2.2. Task 2.1 is a lowest task, and Task 2.2 has

two subtasks, 2.2.1 and 2.2.2.

The following illustration shows grouping at the project level.

Group at the Project level

The following illustration shows grouping at the top task level (Task 1 and Task 2).

Group at Top Task level

The following illustration shows grouping at the lowest task level (tasks
1.1, 1.2, 2.1, 2.2.1, and 2.2.2).

Asset Capitalization

5-29

Group at lowest level Tasks

The following illustration shows grouping at the top task level for the Task 1 branch (at
Task 1) and at the lowest task level for the Task 2 branch (at Task 2.1, Task 2.2.1, and
Task 2.2.2).

Group at different levels in each WBS

Example of Asset Grouping and Assignment

The following illustration shows and example of a capital project.

5-30 Oracle Project Costing User Guide

Example of a Capital Project

The illustration Example of a Capital Project, page 5-31 shows an example of a capital
project with the following breakdown structure:

• The project has three top tasks, Task 1, Task 2, and Task 3.

• Task 1 has two subtasks, 1.1 and 1.2. These are the lowest tasks for Task 1.

• Task 2 has three subtasks, Task 2.1, 2.2, and 2.3. These are the lowest tasks for Task 2.

• Task 3 has no subtasks.

All transactions on all tasks, except for Task 2.3, are capitalizable. The following
grouping and assignment actions are applicable:

• Grouping levels:

• You create asset lines for Task 1.1, Task 1.2, Top Task 2, and Top Task 3 grouping

levels

• You charge expenditure items to Tasks 2.1 and 2.2, and they are grouped

together into asset lines for Top Task 2

• You can charge expensed transactions only to Task 2.3, because Task 2.3 is

not capitalizable

• Grouping level types:

• Task 1.1, Task 1.2, and Top Task 2 grouping levels are assigned the grouping

level type Specific Assets

• Top Task 3 has a Common Costs grouping level type. Asset lines are created, but

specific assets cannot be assigned to this grouping level

• You have to manually assign assets to the asset lines created for Top Task 3

• Asset assignments:

• You associate Asset 1 with Task 1.1 and Task 1.2 (Single Asset associated with

multiple grouping levels)

Asset Capitalization

5-31

• You associate Asset 1 and Asset 2 with Task 1.2, and Asset 3 and Asset 4 to Top

Task 2 (Multiple assets associated with a single grouping level)

Related Topics

Creating a Capital Asset in Oracle Projects, page 5- 9

CIP Grouping Client Extension, Oracle Projects APIs, Client Extensions, and Open Interfaces
Reference

Reviewing and Adjusting Asset Lines

This section describes how you can adjust asset lines created by the Generate Asset
Lines process.

Assigning an Asset to Unassigned Asset Lines

When the Generate Asset Lines process creates asset lines without an asset
assignment, you need to manually assign an asset to the line before you can send it
to Oracle Assets.

If you choose the Include Common Tasks check box when you generate asset
lines, Oracle Projects creates asset lines from common task grouping levels as well as
from specific assets grouping levels. Use the Common Costs grouping level type to
group together tasks that capture costs you want to allocate to multiple assets.

For more information on generating asset lines and how Oracle Projects maps costs to
assets, see: Generating Summary Asset Lines, page 5-21. For information on how to
define an asset cost allocation method for a project to automatically allocate common
costs across multiple assets, see: Allocating Asset Costs, page 5-25.

You can assign an asset to unassigned asset lines for a project or a capital event from
the Asset Lines window.

Note: If unassigned asset lines are associated with an event, you can
only assign the lines to an asset that is included in the event.

To assign an asset to unassigned lines:

1. Navigate to the Capital Projects window, choose the project you want, and choose

the Lines button.

2. Choose Find from the toolbar to open the Find Asset Lines window.

3.

4.

Select No from the Assigned poplist within the Line region, and choose the Find
button to find all unassigned asset lines for the project

(Optional) Choose Details to view detail information for an asset line so you can
identify the asset to assign.

5. Assign an asset to the lines by entering the asset Name.

6.

Save your work.

Note: The Asset Line Details window is a folder. You can create folders
to display additional fields. See: .

5-32 Oracle Project Costing User Guide

Changing the Asset Assigned to an Asset Line

You can change the asset or description for an asset line in the Asset Lines
window. However, you cannot change asset lines you have already sent to Oracle Assets.

Splitting an Asset Line

You can split an asset line and assign the split costs to multiple assets by using
percentages or amounts. You can split lines with and without asset assignments. You can
split an asset line for a project or a capital event from the Asset Lines window.

To split an asset line for a project or a capital event:

1. Navigate to the Asset Lines window for a project or capital event.

2. To open the Asset Lines window for a project, navigate to the Capital Projects

window, select a project, and choose the Lines button.

3. To open the Asset Lines window for a capital event, perform the following steps in

the order listed:

• Navigate to the Capital Projects window, select a project, and choose the Capital

Events button.

• In the Capital Events window, select a workbench option, if any, to display

capital events or retirement cost events. Select an event and choose the Assets
button.

• In the Event Assets window, select an asset and choose the Asset Lines button.

• Choose the asset line you want to split.

• Choose the Split Line button to open the Split Asset Line window.

• Enter the Asset Name and the Amount or Percentage you want to split. The

Unassigned fields indicate the amount and percent of the asset line’s cost you
have not yet assigned to an asset.

• Choose OK when you finish splitting the line.

• Save your work.

Related Topics

Generate Asset Lines Report, Oracle Projects Fundamentals

Adjusting Assets After Interface

You can adjust assets after they have been interfaced to Oracle Assets.

You can adjust expenditure items whose costs are sent to Oracle Assets, and collect
new expenditure items for an asset in Oracle Projects after you capitalize or retire an
asset, and send the summarized asset lines to Oracle Assets. You process these cost
adjustments in Oracle Projects and send them to Oracle Assets as adjusting asset lines.

Your cost adjustments can be either positive or negative. For example, you receive a
credit memo from a supplier for a capitalized asset you sent and posted to Oracle
Assets. When you send this credit memo to Oracle Projects, you create new negative
asset lines, which you can send to Oracle Assets as a negative cost adjustment to the
original asset.

Asset Capitalization

5-33

Oracle Projects includes the information you enter for the asset on the adjusting asset
line you send to Oracle Assets. Thus, if you specify to amortize depreciation adjustments
for a capital asset in Oracle Projects, Oracle Assets amortizes any catchup depreciation
amount for the adjustment over the remaining life of the asset. Otherwise, it expenses
the catchup depreciation for the adjustment in the current period.

Note: You cannot send cost adjustments to Oracle Assets until you have
posted the original mass addition line (imported asset line) to Oracle
Assets using the Post Mass Additions process.

Adjusting Capital Project Costs

You can adjust capital project expenditure items associated with an asset you placed
in service or sent to Oracle Assets. You can generate new asset lines for these adjusted
expenditure items and interface them to Oracle Assets to adjust the original asset cost.

To adjust capital project costs:

1. Navigate to the Expenditure Items window.

2.

In the Find Expenditure Items window, enter your search criteria. To query
by capitalizability or grouping level for your capital project, choose Yes in the
Capitalizable poplist for the CIP/RWIP Status option.

3. Choose the expenditure item you want to adjust.

4. Use the Tools menu to choose the type of adjustment you want to make. You can

choose from the following options:

Capitalizable or Non-Capitalizable to change the capitalizability of a capital asset
expenditure item.

Split to split the cost of the expenditure item. You must specify how you want to
split the item in the Split Expenditure Item window.

Transfer to transfer the expenditure item to another project or task. You must
specify the destination project or task for this transfer in the Transfer Expenditure
Item window.

5.

Save your work.

6. Generate Asset Lines. See: Generating Summary Asset Lines, page 5-21.

Reversing Capitalization of Assets in Oracle Projects

If you placed an asset in service in error or sent inappropriate asset costs to Oracle
Assets, you can reverse capitalization of the asset in Oracle Projects, and send the
reversing line to Oracle Assets as an adjustment.

When you reverse a capitalized asset in Oracle Projects, Oracle Projects creates reversing
(negative) asset lines to offset the asset lines previously interfaced to Oracle Assets. The
asset remains in Oracle Assets with a value of zero. Oracle Projects does not delete or
dispose of the asset in Oracle Assets. You can use functionality within Oracle Assets to
retire the asset if you do not ever plan to re-capitalize the reversed asset.

Notes:

• If you reverse capitalize an asset in Oracle Assets that was created from Oracle
Projects, this transaction is recorded in Oracle Assets only, and not in Oracle

5-34 Oracle Project Costing User Guide

Projects. If this happens, you cannot manually update the corresponding asset in
Oracle Projects.

• You cannot send a reversing line to Oracle Assets until you have posted the original
asset using the Post Mass Additions process. You cannot make a negative cost
adjustment (reversal) to a mass addition not yet posted to Oracle Assets.

• When you choose the action to reverse capitalize an asset, Oracle Projects checks
Oracle Assets to determine if the asset was retired previously. If yes, then Oracle
Projects issues a warning message and you can either continue processing or cancel
the reversal action.

Related Topics

Asset Retirements, Oracle Assets User Guide

Depreciation, Oracle Assets User Guide

Overview of Asset Capitalization, page 5- 1

Reversing Capitalization of Assets in Oracle Projects

Oracle Assets processes reversal transactions from Oracle Projects as negative cost
adjustments to the original asset. If you have begun depreciating this asset, Oracle Assets
must reverse the depreciation expense in the period you reverse capitalize the asset.

Important: Before you reverse an asset, ensure that the Amortize
Adjustment check box is unchecked for the asset. If you reverse
capitalize an asset for which you specify to amortize adjustments, the
monthly depreciation on the original cost will not equal the monthly
depreciation generated to account for the asset cost reversal in Oracle
Assets. Oracle Assets will amortize the catch up depreciation on the
negative cost adjustment over the remaining life of the asset.

Reversing Capitalization of an Asset or Event

You can reverse capitalize an asset on a project from the Assets window. If the asset is
associated with a capital event, then you must reverse the entire event. You can reverse a
capital event from the Capital Events window.

To reverse capitalization of an asset:

1. Navigate to the Capital Projects window.

2. Find the project you want and choose Assets to open the Assets window.

3. Choose the asset you want to reverse capitalize.

Ensure that you do not amortize depreciation adjustments for a capital asset you
want to reverse capitalize or recapitalize. You can specify whether to amortize
adjustments in the asset definition. See: Defining Assets, page 5-13.

4. Choose the Reverse button.

Oracle Projects automatically enables the Reverse check box for the asset you want
to reverse capitalize.

If you reversed the wrong asset, or you want to unreverse an asset before you run
the Generate Asset Lines process, choose the asset and the Reverse button again to
deselect the asset for reversal.

Asset Capitalization

5-35

5.

Save your work.

6. Run the Generate Asset Lines process to create reversing entries you can send to

Oracle Assets. See: Generating Summary Asset Lines, page 5-21.

7. Review the Generate Asset Lines Report to verify creation of the reversing
lines. See: Generate Asset Lines Process, Oracle Projects Fundamentals.

To reverse capitalization of a capital event:

1. Navigate to the Capital Projects window.

2. Find the project you want and choose the Capital Events button.

3.

4.

5.

In the Capital Events window, select a workbench option, if any, to display capital
events or retirement cost events.

Select an event and choose the Reverse button.

Save your work.

6. Run the Generate Asset Lines process to remove the Actual Date In Service or

Retirement Date from the assets and create reversing entries you can send to Oracle
Assets. See: Generating Summary Asset Lines, page 5-21.

7. Review the Generate Asset Lines Report to verify creation of the reversing
lines. See: Generate Asset Lines Process, Oracle Projects Fundamentals.

Recapitalization of Reverse Capitalized Assets

If you need to recapitalize an asset, put the new Date Placed in Service in the Assets
form in Oracle Projects so new asset lines will be created.

Important: You must also manually change the Date Placed in Service
for the asset in the Asset Workbench in Oracle Assets, as the Date Placed
in Service cannot be updated through the Mass Additions process.

To recapitalize a reverse capitalized asset:

1. Navigate to the Capital Projects window.

2. Find the project you want and choose Assets to open the Assets window.

3. Enter the Actual Date In Service or Retirement Date for the reverse capitalized asset.

4.

5.

Save your work.

In Oracle Assets, change the date placed in service or retirement date to match the
date in Oracle Projects. See: Changing Asset Details, Oracle Assets User Guide.

6. Generate asset lines to create new lines for the asset. See: Generating Summary

Asset Lines, page 5-21.

Abandoning a Capital Asset in Oracle Projects

You can abandon a capital asset at any time.

Before Interfacing to Oracle Assets

You can abandon a capital project prior to interfacing to Oracle Assets by changing all
transactions from capitalizable to non-capitalizable.

5-36 Oracle Project Costing User Guide

To change transactions from capitalizable to non-capitalizable:

1. Navigate to the Expenditure Inquiry window.

2.

Select all expenditures for the project where the Capitalizable column is checked.

3. From the Tools menu, choose Non-Capitalizable. If cost distribution has been run on
the expenditures, the Cost Distributed column check box will change to unchecked.

4. Run the distribute labor, expense, and usage costs processes and the PRC: Distribute
Supplier Invoice Adjustment Costs process. If you are using burdening, run the
PRC: Distribute Total Burdened Costs process.

5.

Interface the costs to GL and AP. When you post the costs to Oracle General
Ledger, the system will create entries that transfer these costs from the CIP account
to the Expense account. The AutoAccounting rules you set up determine these
accounts.

After Interfacing to Oracle Assets

If you have already interfaced the asset you want to abandon, you must reverse
capitalize the asset in the Assets window in Oracle Projects. You also need to send the
reversing lines to Oracle Assets to account for the abandoned CIP asset.

The Generate Asset Lines process creates reversal lines and the Interface Assets process
interfaces them to Oracle Assets.

Related Topics

Specifying Which Capital Asset Transactions to Capitalize, page 5-12

Reversing Capitalization of Assets in Oracle Projects, page 5-34

Capitalizing Interest

This section describes how to calculate and record capitalized interest for capital projects.

Overview of Capitalized Interest

Capitalized interest (also referred to as Allowance for Funds Used During Construction)
is an estimate of the interest cost that enterprises incur when they invest in long-term
capital projects. Subject to accounting rules and regulatory guidelines, enterprises can
capitalize interest as part of the total cost of acquiring and constructing assets that
require an extended amount of time to prepare for their intended use.

To accommodate this business requirement, Oracle Projects enables you to calculate and
record capitalized interest for capital projects. To meet the requirements of regulated
businesses such as those in the utilities industry that can recognize multiple types of
capital interest, you can set up Oracle Projects to separately calculate capitalized interest
for multiple interest types such as debt and equity.

Oracle Projects calculates capitalized Interest on open CIP amounts. You can spread the
cost for one expenditure item across multiple assets. If you have previously capitalized
any of the assets to which the cost is allocated, then Oracle Projects excludes the total
item cost from the interest calculation.

The process for generating and recording capitalized interest transactions includes the
following tasks:

Asset Capitalization

5-37

• Defining rate names and rate schedules: You define capitalized interest rate

names to represent the interest types you want to capitalize. After you define rate
names, you can create and maintain capitalized interest rate schedules to assign rates
to each organization. For more information, see: Defining Capitalized Interest Rate
Names and Rate Schedules, page 5-38.

• Setting up capital projects for capitalized interest: To correctly calculate capitalized

interest for all eligible capital projects, you must ensure that the capital information
options for each project are defined. You must also assign each project a status that
allows capitalized interest. For more information, see: Setting Up Capital Projects for
Capitalized Interest, page 5-39.

• Generating capitalized interest expenditure batches: To generate interest

expenditures, you periodically submit the Generate Capitalized Interest Transactions
process. See: Generating Capitalized Interest Expenditure Batches, page 5-39.

• Reviewing capitalized interest expenditure batches: After you generate capitalized

interest expenditure batches, you can review the transactions for accuracy. If
necessary, you can delete or reverse a batch to allow regeneration. See Reviewing
Capitalized Interest Expenditure Batches, page 5-40.

Defining Capitalized Interest Rate Names and Rate Schedules

To calculate capitalized interest, you must define a rate name for each type of interest
you want to capitalize and define rate schedules to assign interest rates to organizations.

Defining Capitalized Interest Rate Names

You define a unique rate name for each type of interest you want to capitalize. For
example, you can define a rate name to maintain interest rates for debt and another to
maintain interest rates for equity.

For each rate name, you can define thresholds that determine when the calculation of
interest begins for eligible projects. You can select interest calculation basis attributes that
determine how interest amounts are calculated. For example, you can select an interest
method to specify whether interest is calculated on a simple or compound basis. You
can also specify a period rate convention to determine whether interest amounts are
spread evenly across accounting periods or are derived based on the number of days in
each accounting period.

You can control the CIP balance on which interest is calculated by specifying a
current period convention and expenditure type exclusions. The current period
convention specifies how much of the current period CIP costs are included in the CIP
balance. Expenditure type exclusions enable you to specify types of costs that you
want to exclude from the CIP balance.

For more information, see: Capitalized Interest Rate Names, Oracle Projects
Implementation Guide.

Defining Capitalized Interest Rate Schedules

You define interest rate schedules to create and maintain rates for interest
calculation. You maintain rates by organization and rate name. You can specify an
interest rate schedule for each project type. The rate schedule you define for a project
type is the default rate schedule for all projects you create for the project type. You can
optionally allow override of the default rate schedule at the project level.

5-38 Oracle Project Costing User Guide

For more information, see: Capitalized Interest Rate Schedules, Oracle Projects
Implementation Guide.

Setting Up Capital Projects for Capitalized Interest

To correctly calculate capitalized interest for all eligible capital projects, you must ensure
that the capital information options for each project are defined appropriately, and
assign each project a status that allows capitalized interest.

Defining Capital Information Options

The following fields in the Capital Information options window control the calculation
of capitalized interest for a capital project:

• Allow Capital Interest: This field defines whether a project is eligible for capitalized
interest. By default, Oracle Projects enables this option for all capital projects. You
can deselect or select this option at any time.

• Capital Interest Schedule: This field displays the default capitalized interest rate

schedule specified for the project type, if any. If the Allow Schedule Override option is
enabled for the project type, then you can override the default interest rate schedule
value at the project level.

• Capital Interest Stop Date: You can optionally specify a date beyond which a

project is not eligible for capitalized interest. To calculate interest, this field must
either be blank or contain a date that is later than the end date of the GL period for
which you want to calculate interest.

Note: The Allow Capital Interest and Capital Interest Stop Date fields
are also available at the task level. You can use these fields to control
the calculation of capitalized interest for individual tasks.

For additional information on defining capital information options for projects and
tasks, see: Capital Information, Oracle Projects Fundamentals.

For information on assigning capitalized interest rate schedules to project
types, see: Specifying Capitalized Interest Rate Schedules for Project Types, Oracle
Projects Implementation Guide.

Assigning a Project Status

In addition to defining capital information options to enable the calculation of capitalized
interest, you must assign each eligible project a status that allows capitalized interest. For
more information, see: Setting Project Status Controls for Capitalized Interest, Oracle
Projects Implementation Guide.

Generating Capitalized Interest Expenditure Batches

To generate and record capitalized interest expenditures, you must submit the
PRC: Generate Capitalized Interest Transactions process. This process calculates
capitalized interest and generates transactions for eligible projects and tasks. For
information on submitting this process and the processing parameters that you can
select, see: Generate Capitalized Interest Transactions, Oracle Projects Fundamentals.

When you submit the Generate Capitalized Interest Transactions process, you can
specify whether expenditure batches are released automatically. If the expenditure

Asset Capitalization

5-39

batches are not released automatically, then you must release them manually in the
Review Capitalized Interest Runs window. For more information, see: Reviewing
Capitalized Interest Expenditure Batches, page 5-40.

The generate process charges interest expenditures to the same tasks as the expenditure
items on which interest was calculated. The expenditure organization and expenditure
type values for the interest transactions are derived based on the expenditure
organization source and expenditure type attributes defined for the interest rate
name. For more information, see: Capitalized Interest Rate Names, Oracle Projects
Implementation Guide.

Reviewing Capitalized Interest Expenditure Batches

After you submit the PRC: Generate Capitalized Interest Transactions process, you can
check the status of each run and review the process results in the Review Capitalized
Interest Runs window. From this window you can view capitalized interest expenditure
batches, transactions, and exceptions.

You can generate, review, and delete draft expenditure batches until you are satisfied
with the results. To view transactions that generated successfully, select a batch and
choose the Transactions button. If a batch generated with warnings or errors, then you
can select the draft and choose the Exceptions button to view the exception details. To
record the transactions in an expenditure batch, you must release the batch. You can
reverse an expenditure batch after it is released successfully.

Note: You cannot generate a draft expenditure batch if a draft already
exists for the same projects and GL period.

The following table describes the possible run statuses displayed in the Review
Capitalized Interest Runs window.

Run Status

In Process

Draft Success

Draft Failure

Release Success

Release Failure

Description

The process is not complete.

The process created draft transactions that are
ready for release.

The process encountered warnings or
errors. Draft transactions may be incomplete.
Review the exceptions. If exceptions exist
for one or more projects, then you can
release the batch to release the successfully
generated transactions. After you resolve the
exceptions, you can create a new run to process
the exception project or projects.

Transactions are released.

The release process failed. After you resolve
the release issues, you can release the batch
again.

5-40 Oracle Project Costing User Guide

Releasing, Reversing, and Deleting Capitalized Interest Expenditure Batches

The rules for releasing, reversing, and deleting capitalized interest expenditure batches
are as follows:

• Releasing expenditure batches: You can release batches with the status Draft

Success or Release Failure.

• Reversing expenditure batches: You can reverse expenditure batches with the

status Release Success.

• Deleting expenditure batches: You can delete expenditure batches with the status
Draft Success, Draft Failure, and Release Failure. You cannot delete batches with the
status In Process. In addition, you cannot delete batches after they are reversed or
released successfully.

Asset Capitalization

5-41

6
Cross Charge

This chapter describes accounting within and between operating units and legal entities.

This chapter covers the following topics:

• Overview of Cross Charge

• Processing Flow for Cross Charge

• Processing Borrowed and Lent Accounting

• Processing Intercompany Billing Accounting

• Interfacing Cross Charge Distributions to General Ledger

• Adjusting Cross Charge Transactions

Overview of Cross Charge

Enterprises face complex accounting and operational project issues that result from
centralized project management through sharing of resources across organizations.

Oracle Projects provides the following cross charge features to address these issues:

• Borrowed and Lent Accounting: This feature creates accounting entries to pass costs

and revenue across organizations without generating internal invoices.

• Intercompany Billing Accounting: This feature creates internal invoices and
accounting entries to pass costs and share revenue across organizations.

In addition to these two features that enable you to charge costs across
organizations, Oracle Projects inter-project billing features enable you to charge costs
between projects. For detailed information on this feature, see Inter-Project Billing,
Oracle Project Billing User Guide.

Cross charge features depend on multiple organization support in Oracle Projects
and other Oracle Applications. In addition, these features support multinational
projects, which also call for other currency exchange management functionality. For
more information, see: Providing Data Access Across Business Groups, Oracle Project
Fundamentals.

Note: To use the intercompany billing feature (for cross charge) you
must implement both Oracle Project Costing and Oracle Project Billing.

Cross Charge

6-1

Related Topics

Setting Up for Cross Charge Processing: Borrowed and Lent, Oracle Projects
Implementation Guide

Setting Up for Cross Charge Processing: Intercompany Billing, Oracle Projects
Implementation Guide

Cross Charge Business Needs and Example

When projects share resources within an enterprise, it is common to see those resources
shared across organization and country boundaries. Further, project managers may
also divide the work into multiple projects for easier execution and management. The
legal, statutory, or managerial accounting requirements of such projects often present
complex operational control, billing, and accounting challenges.

Oracle Projects enables companies to meet these challenges by providing timely
information for effective project management. Project managers can easily view
the current total costs of the project, while customers receive bills as costs are
incurred, regardless of who performs the work or where it is performed.

Project Structures Example

To provide a better understanding of cross charge concepts and the difference between
cross charge and inter-project billing options, the scenarios shown in the following
example illustrate how projects can be structured.

Note: The project in this example is a contract project and is used for
illustrative purposes only. You can apply most of the features described
in this document to other types of projects.

The following illustration shows Company ABC, an advertising company with the
following organization structure:

• Company ABC has two sets of books: US and Japan.

• The legal entity US is assigned to the US set of books and the legal entity Japan is

assigned to the Japanese set of books.

• The legal entity US is comprised of three operating units: Los Angeles, San Francisco

and New York

• The legal entity Japan is comprised of the Tokyo operating unit.

• The legal entity US and the Japanese set of books belong to the business group BGI.

6-2 Oracle Project Costing User Guide

Organization Structure of Company ABC

The Los Angeles operating unit, ABC’s headquarters, receives a contract from a customer
in the United Kingdom (UK). The customer wants ABC to produce and air live shows
in San Francisco, New York, and Tokyo to launch its new line of high-end women’s
apparel. The customer wants to be billed in British Pounds (GBP). ABC calls this project
Project X and will track it using Oracle Projects. ABC will plan and design the show
using resources from the Los Angeles operating unit. Employee EMPJP from its Japan
subsidiary will act as an internal consultant to add special features to suit the Japanese
market. The San Francisco, New York, and Tokyo operating units are each responsible
for the successful execution of these live shows with their local resources.

Based on this scenario, each operating unit can incur costs against Project X. Consider
the following labor transaction, which is summarized in the table that follows.

• Employee EMPJP of Japan worked 10 hours meeting with the customer in Japan to

learn about the new product.

• Employee EMPJP’s cost rate is 5,000 JPY per hour.

• Employee EMPJP’s standard bill rate is USD 400 per hour.

• Employee EMPJP’s internal bill rate, if applicable, is USD 200 per hour, or 50% of

the standard bill rate.

Note: Currency conversion rates: 1 USD = 100 JPY; 1 USD = .75 GBP

Cross Charge

6-3

Sample Transaction

(10 hours of labor)

Transaction
Currency Amounts

Functional Currency
Amounts

Project Currency
Amounts

Cost

Revenue

Invoice

50,000 JPY

50,000 JPY

500 USD

4,000 USD

4,000 USD

4,000 USD

3,000 GBP

4,000 USD

4,000 USD

Internal Billing
Revenue

2,000 USD

200,000 JPY

Project Structure: Distinct Projects by Provider Organization

The illustration Distinct Projects By Provider Organization, page 6- 4 shows the following
structure:

• Company ABC divides Project X into four distinct contract projects: Project

X-1, Project X-2, Project X-3 and Project X-4.

• Each operating unit owns its respective project (Los Angeles owns X-1, San Francisco

owns X-2, New York owns X-3, and Tokyo owns X-4) and bills the project customer
directly.

Distinct Projects by Provider Organization

Requirements:

• Oracle Project Costing

• Oracle Project Billing

Advantages: Simplicity, since the operating units create and process their projects
independently.

Disadvantages: The company must divide the project work properly, and each resulting
project requires an agreement, funding, and a budget to generate customer invoices. In

6-4 Oracle Project Costing User Guide

addition, the customer may not want to receive separate invoices from different
organizations in your enterprise. Communication and control across the projects for
collective status can be difficult.

Project Structure: Single Project

The following illustration shows a structure where the Los Angeles operating unit
(the project owner, or receiver organization) centrally manages Project X. All four
operating units (the provider organizations) incur project costs and charge them directly
to Project X.

Single Project

Requirements:

• Oracle Project Costing

• Oracle Project Billing

• Implementation of the cross charge feature

• Depending on the method you choose to process cross charge transactions (borrowed
and lent accounting or intercompany billing accounting), this solution may also require
intercompany billing for the automatic creation of internal invoices.

Advantages: Simple project creation and maintenance, since this solution requires
a single project. All of the expenditures against ProjectX, cross charged or not, are
available for external customer billing and project tracking via Project Status Inquiry. The
customer receives timely, consolidated invoices from Los Angeles for all the work
performed regardless of which operating unit provides the resources.

Cross Charge

6-5

Disadvantages: Requires additional initial overhead for implementing the cross charge
feature and creating intercompany billing projects to collect cross charge transactions
within each provider organization.

Project Structure: Primary Project with Subcontracted Projects

The following illustration shows how Company ABC divides Project X into several
related contract projects. The Los Angeles operating unit owns the primary customer
project, or receiver project, and bills the external customer. The related projects, or
provider projects, are subcontracted to their respective internal organizations and
internally bill the Los Angeles organization to recoup their project costs.

Primary Project with Subcontracted Projects

Requirements:

• Oracle Project Costing

• Oracle Project Billing

• Implementation of inter-project billing features

Advantages: Flexibility in managing the provider projects. Each provider project is
treated and processed the same way as any external customer contract project.

Disadvantages: As with the distinct project structure, this solution requires additional
overhead in creating and managing three additional provider projects. The receiver
project’s status and external customer invoicing depend upon timely completion of the
internal billing from all provider projects.

6-6 Oracle Project Costing User Guide

Cross Charge Types

Oracle Projects provides three types of cross charge transactions as shown in the
following table. A transaction’s cross charge type depends on whether the provider
operating unit, organization, and legal entity are different from those of the receiver.

Cross Charge Type

Conditions

Intercompany

Inter-operating unit

Intra-operating unit

Operating units and legal entities are different

Operating units are different, but legal entities
are the same

Operating units and legal entities are the
same, but the organizations are different

Note: You cannot change the provider or receiver operating unit, but
you can use the Provider and Receiver Organizations Override client
extension to override the default provider organization and receiver
organization. For more information on this client extension, see: Oracle
Projects APIs, Client Extensions, and Open Interfaces Reference.

The following illustration shows the potential cross charge type relationships for the four
organizations shown in the illustration Organization Structure of Company ABC, page 6- 3
when they charge costs to Project X in the Los Angeles operating unit.

Potential Cross Charge Types for Company ABC

Cross Charge

6-7

The following table summarizes the characteristics of the potential cross charge type
relationships shown in the illustration Potential Cross Charge Types for Company ABC,
page 6- 7 .

Cost
Transactions
from the
following
Provider
Operating Units

Expenditure
Organization
Equals Project
Organization

Los Angeles

Yes

Los Angeles

San Francisco

New York

Tokyo

No

No

No

No

Same Legal
Entity

Same Business
Group

Cross-
Charge Type
Relationship

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Non Cross-
Charged
Transactions

Intra-Operating
Unit Transactions

Inter-Operating
Unit Transactions

Inter-Operating
Unit Transactions

Inter-Company
Transactions

Cross Charge Processing Methods and Controls

This section describes cross charge processing methods and processing control options.

Cross Charge Processing Methods

You can choose one of the following processing methods for cross charge transactions:

• Borrowed and Lent Accounting (inter-operating unit and intra-operating unit

cross charges)

• Intercompany Billing Accounting (intercompany and inter-operating unit cross

charges)

• No Cross Charge Process (intercompany, inter-operating unit, and intra-operating

unit cross charges)

Borrowed and Lent Accounting

When you use this method, Oracle Projects creates accounting entries to pass costs and
revenue across organizations without generating internal invoices. Oracle Projects
determines the appropriate cost or revenue amounts based on the transfer price rules of
the provider and receiver organizations.

Borrowed and lent accounting entries provide a financial view of an organization’s
performance. This processing method is generally used to measure organizational
financial performance for management reporting purposes. For more
information, see: Processing Borrowed and Lent Accounting, page 6-18.

6-8 Oracle Project Costing User Guide

Intercompany Billing Accounting

Companies choose the intercompany billing method largely due to legal and statutory
requirements. When you use this method, Oracle Projects generates physical invoices
and corresponding accounting entries at legal transfer prices between the internal
seller (provider) and buyer (receiver) organizations when they cross a legal entity
boundary or operating units. For more information, see: Processing Intercompany
Billing Accounting, page 6-21.

No Cross Charge Process

Companies generally process cross charges in Oracle Projects using the borrowed and
lent or intercompany billing method. However, companies may not need to process
cross charge transactions, if, for example, intercompany billing has been performed
manually in General Ledger or automatically by an external system. You can use cross
charge controls to identify which cross charge transactions will undergo cross charge
processing. See: Cross Charge Controls, page 6- 9 .

Cross Charge Controls

Cross charge controls specify:

• Which projects and tasks in which operating units can receive transactions from a

provider operating unit

• How Oracle Projects processes these cross charged transactions

Cross-charge controls affect all cross charge transactions, regardless of how you enter
them. For maximum control, you can use a combination of cross charge and transaction
controls to ensure that only valid cross charges are charged to a specific project and task.

Cross charge controls are defined at the operating unit, project, and task levels. Oracle
Projects applies these controls based on a transaction’s cross charge type and cross
charge processing method.

Intra-Operating Unit Cross Charge Controls

You can charge intra-operating unit cross charges (that is, charges within an operating
unit) to any project and task owned by your expenditure operating unit. You can modify
the transaction control extension to restrict intra-operating unit cross charge transactions.

Inter-Operating Unit Cross Charge Controls

Oracle Projects provides controls to identify:

• Which projects and tasks in a receiver operating unit can receive inter-operating unit

cross charges from a provider operating unit

• Which cross charge processing method to apply to these transactions.

Steps performed by the provider operating unit:

• Define cross charge implementation options: Specify whether to allow cross charge

and select a default processing method.

• Define internal billing implementation options: Specify whether the operating

unit is a provider for internal billing.

• Define provider controls: Select a processing method and specify the name of the

intercompany billing project.

Steps performed by the receiver operating unit:

Cross Charge

6-9

• Define internal billing implementation options: Specify whether the operating

unit is a receiver for internal billing.

• Define receiver controls: Specify the name of each provider operating unit that can

charge transactions to the specified receiver operating unit.

• Enable cross charge for projects: In the Projects window (Cross Charge

option), select Allow Charges from other Operating Units.

Intercompany Cross Charge Controls

Oracle Projects provides flexible controls to identify:

• Which projects and tasks in a receiver operating unit can receive intercompany cross

charges from a provider operating unit

• Which cross charge processing method to apply to these transactions.

Steps performed by the provider operating unit

• Define internal billing implementation options: Specify whether the operating

unit is a provider for internal billing.

• Define provider controls: Specify the name of each receiver operating unit that

can receive transactions from the specified provider operating unit. Also, select a
processing method and specify the name of the intercompany billing project.

Steps performed by the receiver operating unit

• Define internal billing implementation options: Specify whether the operating

unit is a receiver for internal billing.

• Define receiver controls: Specify the name of each provider operating unit that can

charge transactions to the specified receiver operating unit.

• Enable cross charge for projects: In the Projects window (Cross Charge

option), select Allow Charges from other Operating Units.

Note: If Cross Business Group Access is enabled, the provider and
receiver operating units can be in different business groups. See
Security, Customizing, Reporting, and System Administration in Oracle
HRMS.

Cross Charge Processing Controls

Cross charge processing controls determine which cross charge method and transfer
price rule should be applied to the cross charged transaction. This section describes the
cross charge process controls.

Implementation Options

For each provider operating unit or receiver operating unit involved in the cross
charge, the Implementation Options window Cross Charge and Internal Billing tabs
specify:

• The default transfer price conversion attributes

• The default cross charge methods for intra-operating unit and inter-operating

unit cross charges

• Attributes required as the provider of internal billing

• Attributes required as the receiver of internal billing

6-10 Oracle Project Costing User Guide

See: Define Cross Charge Implementation Options, and Defining Internal Billing Options
in the Oracle Projects Implementation Guide.

Provider and Receiver Controls Setup

For each provider operating unit or receiver operating unit involved in the cross
charge, the Provider/Receiver Controls window Provider Controls and Receiver Controls
tabs specify:

• The cross charge method to use to process intercompany cross charges and to
override default cross charge method for inter-operating unit cross charges.

• Attributes required for the provider operating unit to process intercompany billing
to each receiver operating unit. This includes the Intercompany Billing Project and
Invoice Group.

• Attributes required for the receiver operating unit to process intercompany billing

from each provider operating unit. This includes the supplier site, expenditure type
and expenditure organization.

See: Defining Provider and Receiver Controls, Oracle Projects Implementation Guide.

Transfer Price Rules and Schedule Setup

Transfer price rules control the calculation of transfer prices for labor and non-labor cross
charged transactions. To drive transfer price calculation for cross charge transactions
between the provider and receiver, use the Transfer Price Schedule window to assign
labor or non-labor (or both) transfer price rules to the provider and receiver pair on a
schedule line. See: Transfer Pricing, page 6-13.

Multiple lines in a transfer price schedule could potentially apply to a cross charged
transaction. Oracle Projects identifies the appropriate schedule line based on the
following hierarchy (in ascending order):

• Organization

• Parent Organization

• Operating unit

• Legal entity

• Business group

The following steps are performed to identify the appropriate schedule line:

1.

2.

If a schedule line exists for the transaction expenditure organization (provider)
and the project/task owning organization (receiver), then the corresponding rule
is used to calculate the transfer price.

If a schedule line is not located, Oracle Projects checks for a line with the provider
organization and (in order) a receiver parent organization, the receiver operating
unit, the receiver legal entity, or the receiver business group.

3. When searching for receiver organization parents, the Project/Task Owning

Organization Hierarchy defined in the Implementation Options of the receiver
operating unit is used.

4.

If the receiver organization has multiple intermediate parents and schedule lines
are defined for more than one of the parents, the schedule line defined for the
lowest level parent takes precedence over schedule lines defined for parents higher
in the organization hierarchy.

Cross Charge

6-11

5.

If a schedule line is not located, Oracle Projects checks for a line with a provider
parent organization and (in order) the receiver organization, receiver parent
organization, receiver operating unit, receiver legal entity, or business group.

6. When searching for provider organization parents, the Expenditure/Event

Organization Hierarcy defined in the Implementation Options of the provider
operating unit is used.

7.

8.

9.

If the provider organization has multiple intermediate parents and schedule lines
are defined for more than one of the parents, the schedule line defined for the
lowest level parent takes precedence over schedule lines defined for parents higher
in the organization hierarchy.

If a schedule line is not located, Oracle Projects checks for a line with the
Provider Operating unit and (in order) the receiver organization, receiver parent
organization, receiver operating unit, receiver legal entity, or business group.

If a schedule line is not located, Oracle Projects checks for a line with the
provider legal entity and (in order) the receiver organization, receiver parent
organization, receiver operating unit, receiver legal entity, or business group.

10. If a schedule line is not located, Oracle Projects checks for a line with the

provider business group and (in order) the receiver organization, receiver parent
organization, receiver operating unit, receiver legal entity, or business group.

Project and Task Setup

For each project or task, you can decide whether to process labor and non-labor cross
charge transactions, and which transfer price schedules are used for transfer price
calculation. See: Cross Charge, Oracle Projects Fundamentals.

Transaction Source Setup

To cause the cross charge processes to skip a transaction source, deselect the Process Cross
Charge option in the Transaction Sources window. See: Transaction Sources, Oracle
Projects Implementation Guide.

Expenditure Item Adjustments

You can mark an expenditure item to be skipped by the cross charge processes by
choosing Mark for No Cross Charge Processing from the Tools menu on the Expenditure
Items window.

Client Extensions

Oracle Projects provides following client extensions that you can use to implement your
business rules to control cross charge processing:

• Provider and Receiver Organizations Override Extension

• Cross Charge Processing Method Override Extension

• Transfer Price Determination Extension

• Transfer Price Override Extension

• Transfer Price Currency Conversion Override Extension

For more information, see: Oracle Projects APIs, Client Extensions, and Open Interfaces
Reference.

6-12 Oracle Project Costing User Guide

Transfer Pricing

Legal transfer price refers to the legally accepted billing prices for internal sales. In Oracle
Projects, transfer price refers to the billing price that two organizations agree upon for
cross charge purposes.

Transfer Price Rules

You can define transfer price rules that determine the transfer price amount of
cross charge transactions that require borrowed and lent or intercompany billing
processing. Oracle Projects provides flexible transfer pricing rules for transfer price
calculations. The calculations are based on the:

• Transfer price basis. Base your transfer price on a cross charged transaction’s

raw cost, burdened cost, or revenue.

• Cross-charge calculation method. You can optionally perform an additional
calculation and apply a markup or discount to the amount determined by the
transfer price basis. For the additional calculations, you can apply any burden
schedule or standard bill rate schedule in your business group.

Note: Using a standard bill rate schedule allows you to define the
schedule in a single operating unit and enforce it across all operating
units in your business group.

Oracle Projects automatically converts transfer price amounts to the functional
currency of the provider operating unit using the transfer price currency conversion
attributes defined in that operating unit. You can use the Transfer Price Currency
Conversion Override Extension to adjust these conversion attributes. For more
information, see: Oracle Projects APIs, Client Extensions, and Open Interfaces Reference.

Transfer Price Schedules

Once you define your transfer price rules, you create a transfer price schedule to
associate these rules to pairs of provider and receiver organizations. In the simplest
transfer price schedule, an enterprise would have a single transfer price rule that
every organization follows. Oracle Projects supports more complex schedules so your
organizations can negotiate their own transfer price rules. You can also define a schedule
with one rule that applies to cross charges to a particular organization and another rule
for cross charges to all other organizations. You can define one transfer price schedule
consisting of different rules for different organization pairs or multiple schedules
consisting of different rules for the same pair of organizations.

You can assign different transfer price schedules at the project and task levels to drive
transfer price calculations, similar to the way that you can assign standard bill rate
schedules at the project and task level to drive project billing for external customers. At
the project and task level, you can use separate transfer price schedules for labor and
non-labor cross charge transactions.

Related Topics

Cross Charge, Oracle Projects Fundamentals

Defining Transfer Price Rules, Oracle Projects Implementation Guide

Defining Transfer Price Schedules, Oracle Projects Implementation Guide

Cross Charge

6-13

Processing Flow for Cross Charge

This section describes the processing flow for cross charge transactions.

The following illustration shows the processing flows for cross charge transactions that
require either borrowed and lent or intercompany billing processing. For a description
of these flows, see: Borrowed and Lent Processing Flow, page 6-14, and Intercompany
Billing Processing Flow, page 6-15.

Overview of Cross Charge Processing Flow

Related Topics

Creating Cross Charge Transactions, page 6-16

Borrowed and Lent Processing Flow

Borrowed and lent processing requires the following steps:

1. The provider operating unit enters or imports cross charge transactions.

2. The provider operating unit distributes the costs of the cross charges, which are

identified as cross charge transactions by the cost distribution processes. The cross
charge distribution process is independent of revenue generation. The process
distributes the costs even if revenue has not been generated.

6-14 Oracle Project Costing User Guide

3. The provider operating unit runs PRC: Distribute Borrowed and Lent Amounts to

determine the transfer price amount and generate the borrowed and lent accounting
entries.

4. The provider operating unit runs PRC: Interface Cross Charge Distributions to GL to

interface the borrowed and lent accounting entries to Oracle General Ledger.

5.

6.

(Optional) You may require the receiver operating unit to run additional customized
processes and interface additional accounting entries to Oracle General Ledger. For
example, your implementation team may develop customized processes to handle
organizational profit elimination to satisfy your company’s accounting practices.

(Optional) The provider operating unit may adjust cross charge transactions
or perform steps resulting in the reprocessing of borrowed and lent
transactions. See: Adjusting Cross Charge Transactions, page 6-32.

Intercompany Billing Processing Flow

Intercompany billing processing requires the following steps:

1. The provider operating unit enters or imports cross charge transactions.

2. The provider operating unit distributes costs of the cross charges, which are
identified as cross charge transactions by the cost distribution processes. The
distribution of the costs is independent of revenue generation and are distributed
even if revenue has not been generated.

3. The provider operating unit runs PRC: Generate Intercompany Invoice to generate
draft intercompany invoices with the associated intercompany receivable and
revenue accounts and transfer price.

4. The provider operating unit reviews, approves, and releases the intercompany

invoices.

5. The provider operating unit interfaces the approved intercompany invoices to
Oracle Receivables. You can include the following activities in this process:

6. Accounting for invoice rounding

7. Creation of the receivable invoices including sales tax

8. PRC: Tieback Invoices from Receivables, which automatically creates corresponding

intercompany invoice supplier invoices ready to be interfaced to the receiver
operating unit’s Oracle Payables.

Use Oracle Receivables to print the invoice as well as to interface the accounting
entries to the provider operating unit’s General Ledger.

9. The receiver operating unit imports the intercompany supplier invoices to Oracle
Payables. This import process calculates recoverable and non-recoverable tax
amounts. Upon review and approval in Oracle Payables, the receiver operating unit
interfaces the accounting entries to Oracle General Ledger.

10. The receiver operating unit interfaces the supplier invoice to Oracle Projects, which

pulls in the non-recoverable tax amounts as additional project costs.

11. The provider operating unit interfaces any cost reclassification entries to Oracle

General Ledger.

12. (Optional) The receiver operating unit runs additional customized processes and

interfaces additional accounting entries to Oracle General Ledger. For example, your

Cross Charge

6-15

implementation team may develop customized processes to handle organizational
profit elimination to meet your company’s accounting practices.

13. (Optional) The provider operating unit adjusts cross charge transactions or performs
the steps resulting in the reprocessing of intercompany transactions. See Adjusting
Cross Charge Transactions, page 6-32.

Creating Cross Charge Transactions

To create cross charge transactions, you enter expenditures, distribute costs, and then
generate revenue.

Enter Expenditures

Enter or import the cross charge transactions as you would for any project
transactions. Oracle Projects enforces cross charge controls and transaction controls to
ensure that only valid transactions are charged to a project or task. See Cross Charge
Controls, page 6- 9 .

Distributing Costs

In addition to determining the raw and burden cost amounts and the accounting
information for project transactions, the cost distribution processes also determine the
following information for cross charge transactions:

• Provider and receiver operating units and organizations

• Cross-charge type, which indicates whether a transaction is an intra-operating

unit, inter-operating unit, or intercompany cross charged transaction or not a cross
charged transaction

• Cross-charge processing method, which indicates whether a transaction is subject to

cross charge processing and which processing method to use

Determining the cross charge type

Oracle Projects determines a transaction’s cross charge type as follows:

• Provider organization defaults to the expenditure or non-labor resource organization

• Receiver organization defaults to the task organization

• Call the Provider and Receiver Organizations Override extension to determine

whether to override these values

• Cross charge type is based on the values above and the logic indicated in the

following table:

6-16 Oracle Project Costing User Guide

Cross Charge Type

Conditions

Intra-operating unit

Inter-operating unit

Provider operating unit equals receiver
operating unit

Provider organization does not equal
receiver organization

Provider operating unit does not equal
receiver operating unit

Provider legal entity equals receiver legal
entity

Intercompany

Provider legal entity does not equal receiver
legal entity

Determining the cross charge processing method

A transaction can have one of the following cross charge processing methods:

• Borrowed and lent accounting

• Intercompany billing

• No cross charge processing

Oracle Projects determines the cross charge processing method for a transaction, based
on how you have implemented the following items:

• Transaction source options.If you enable the option Process Cross Charge for the

transactions source, Oracle Projects performs cross charge processing for transactions
originating from that transaction source.

• Project attributes for processing labor and non-labor cross charge transactions. If
you do not enable cross charge processing for cross charge labor transactions at the
project level, no labor transactions for that project will be subject to cross charge
processing. The same applies to non-labor transactions.

• Cross-charge options for provider operating unit

• Intra-operating unit transactions. Implementation options determine processing

method.

• Inter-operating unit transactions. If you have enabled users to charge to all

operating units within the legal entity, the implementation options determine
the default processing method.

• Provider and receiver controls

• Cross Charge Processing Method Override extension

Generating Revenue

If you use revenue as your transfer price basis, you must run PRC: Generate Revenue
to determine your cross charged transactions’ revenue amount before running the
cross charge processes.

Note: You can use revenue as a transfer price basis only for contract
projects (Oracle Projects generates revenue only for contract projects).

Cross Charge

6-17

Processing Borrowed and Lent Accounting

The borrowed and lent processing method creates accounting entries to pass costs or
share revenue (cost and revenue amounts are determined by the transfer price amount)
between the provider and receiver organizations within a legal entity.

If costs are being passed from the provider to the receiver, this processing method:

• Debits the cost from the receiver (or lent) organization

• Credits the cost account of the provider (or borrowed) organization

Similarly, if revenue is being shared, this method:

• Debits the revenue from the receiver organization

• Credits the revenue to the provider organization

You can view these accounting entries in the corresponding reporting sets of books.

Oracle Projects provides AutoAccounting functions for borrowed and lent
processing. See: AutoAccounting Functions, Oracle Projects Implementation Guide.

Determining Accounts for Borrowed and Lent Transactions

An inter-operating unit cross charge transaction against a contract project results in the
borrowed and lent accounting entries shown in the following two tables.

The following table show the entries generated for the provider operating unit.

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Cost

Labor Expense

Labor Clearing

Borrowed and
Lent

Lent

Borrowed

Dr

Cr

Dr

Cr

500 USD

500 USD

500 USD

500 USD

2,000 USD

2,000 USD

2,000 USD

2,000 USD

The following table show the entries generated for the receiver operating unit

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Client Revenue

UBR/UER

Client Invoice

Revenue

Accounts
Receivable

UBR/UER

Dr

Cr

Dr

Cr

4,000 USD

4,000 USD

4,000 USD

4,000 USD

3,000 GBP

4,000 USD

3,000 GBP

4,000 USD

6-18 Oracle Project Costing User Guide

An intra-operating unit cross charge transaction against a contract project results in the
borrowed and lent accounting entries shown in the following table for the receiver
operating unit.

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Cost

Labor Expense

Labor Clearing

Borrowed and
Lent

Lent

Borrowed

Client Revenue

UBR/UER

Client Invoice

Revenue

Accounts
Receivable

UBR/UER

Dr

Cr

Dr

Cr

Dr

Cr

Dr

Cr

500 USD

500 USD

500 USD

500 USD

2,000 USD

2,000 USD

2,000 USD

2,000 USD

4,000 USD

4,000 USD

4,000 USD

4,000 USD

3,000 GBP

4,000 USD

3,000 GBP

4,000 USD

Note: The automatic intercompany balancing feature in Oracle General
Ledger can be used to create additional entries as necessary if the
borrowed and lent entries are posted to different balancing segments.

Generating Accounting Transactions for Borrowed and Lent Accounting

Running the standard cost distribution processes in the provider operating unit
identifies which transactions require borrowed and lent processing. Oracle Projects
provides a separate process, PRC: Distribute Borrowed and Lent Amounts, to compute
the transfer price of these transactions and determine the GL accounts for borrowed and
lent accounting entries.

The provider operating unit runs this process to perform the following steps on cross
charge transactions identified for borrowed and lent processing:

1. Calculate the transfer price amount, page 6-19

2. Run AutoAccounting, page 6-21

3. Create cross charge distribution lines, page 6-21

Calculate the Transfer Price Amount

Distribute Borrowed and Lent Amounts calculates the transfer price amount of a given
cross charge transaction, as follows:

Note: If the process cannot determine a transfer price for the cross
charge transaction, Oracle Projects flags the transaction with an error
and proceeds to the next item. The transfer price is stored in the
transaction and functional currencies.

Cross Charge

6-19

1. Call the Transfer Price Determination extension.

Oracle Projects calls the Transfer Price Determination extension at the beginning
of the process in case you want to bypass the standard transfer price calculation
for certain borrowed and lent transactions. If you implement this extension, Oracle
Projects calculates the transfer price amount based on the extension logic and
generates borrowed and lent accounting entries based on this amount. See: Transfer
Price Determination Extension, Oracle Projects APIs, Client Extensions, and Open
Interfaces Reference.

2.

Identify the applicable transfer price schedule.

Oracle Projects identifies the labor or non-labor transfer price schedule specified for
the task to which the transaction is charged.

Note: If Project Resource Management is installed, transfer price
overrides can be defined at the assignment level. For more details
refer to the Oracle Project Resource Management User Guide.

3.

Identify the applicable transfer price schedule line.

If the transfer price schedule identified by the Distribute Borrowed and Lent
Amounts process contains more than one line, Oracle Projects must determine
which line to apply. Oracle Projects first selects all schedule lines whose effective
dates contain the Expenditure Item Date of the cross charge transaction. Oracle
Projects then selects the appropriate line based on the provider and receiver
organization, operating unit, legal entity, or business group.

4. Calculate the transfer price amount.

The process then calculates the transfer price amount by applying the transfer price
rule and any additional percentage you have specified in the schedule line.

The actual transfer price calculation is carried out like this:

• Determine the transfer price basis (raw cost, burdened cost, or revenue)

identified in the transfer price rule.

Note: If you use revenue or cost amounts as your transfer price
basis, Oracle Projects verifies that you have performed the
appropriate revenue generation or cost distribution processes. If
you have not run the prerequisite processes, Oracle Projects
marks the transaction with an error.

• Apply a burden schedule or standard bill rate schedule to the basis, as indicated

in the transfer price rule. If the process identifies a rate in the specified bill rate
schedule, it applies the rate to the quantity of the transaction.

• Apply any additional percentage specified in the rule.

• Apply any additional percentage specified for labor or non-labor transactions

in the schedule line.

5. Call the Transfer Price Override extension.

You can use this extension to override the transfer price amount calculated by the
Distribute Borrowed and Lent Amounts process. See: Transfer Price Override
Extension, Oracle Projects APIs, Client Extensions, and Open Interfaces Reference.

6-20 Oracle Project Costing User Guide

6. Perform required currency conversions.

If the functional currency is different from the transfer price base currency, the
process performs the required currency conversion to generate functional currency
amounts using the currency conversion attributes defined in the provider operating
unit’s cross charge implementation options. You can override these attributes using
the Transfer Price Currency Conversion Override extension.

7. Call the Transfer Price Currency Conversion Override extension.

You can use this extension to override the default transfer price currency conversion
attributes defined in the cross charge implementation options. See: Transfer Price
Currency Conversion Override Extension, Oracle Projects APIs, Client Extensions, and
Open Interfaces Reference.

Run AutoAccounting

After the Distribute Borrowed and Lent Amounts process calculates the transfer price
amounts for each selected borrowed and lent transaction, it runs AutoAccounting
to determine the account code for each distribution line that it will create. Oracle
Projects provides the functions Borrowed Account and Lent Account for borrowed and
lent transactions.

Create Cross Charge Distribution Lines

After the Distribute Borrowed and Lent Amounts process runs AutoAccounting, it
creates cross charge distribution lines.

The PA date for the distribution lines is determined based on the ending date of the
earliest open PA period on or after the expenditure item date.

You can use the View Accounting window to view cross charge distributions for a
specific item. (To do so, query an invoice transaction in the Expenditure Items window
and choose View Accounting from the Tools menu. See: Viewing Accounting Lines, page
2-40.) The following transaction attributes support cross charge distributions:

• Provider organization and operating unit

• Receiver organization and operating unit

• Cross charge processing method and type

Processing Intercompany Billing Accounting

This section covers the following topics:

• Determining Accounts for Intercompany Billing Accounting, page 6-22

• Generating Intercompany Invoices, page 6-26

• Approving and Releasing Intercompany Invoices, page 6-28

• Interfacing Intercompany Invoices to Receivables, page 6-28

• Interfacing Intercompany Invoices to Oracle Payables, page 6-30

• Interface Tax Lines from Payables to Oracle Projects, page 6-31

Cross Charge

6-21

Determining Accounts for Intercompany Billing Accounting

Intercompany billing accounting entries are based on documents generated by the
provider and receiver organizations. The provider and receiver organizations may be in
the same set of books or in different sets of books with different charts of accounts. If
Cross Business Group Access is enabled, the provider and receiver organizations can
also be in different business groups. You can view intercompany billing accounting
entries in the corresponding reporting sets of books. As this processing method may
require input from multiple organizations and employees in your organization, you
should establish clear user procedures to ensure the successful completion of the
entire process flow. Failure to follow these procedures can result in out of balance
intercompany accounts.

Determining Accounts for Intercompany Receivables Invoices

Oracle Projects provides two AutoAccounting functions to determine the revenue
and invoice accounts of a provider operating unit’s intercompany Receivables
invoice. See: AutoAccounting Functions, Oracle Projects Implementation Guide.

• Intercompany Revenue. This function determines which account receives the credit

entry of an intercompany billing Receivables invoice.

• Intercompany Invoice Accounts. This function includes the function transactions

Intercompany Receivables and Intercompany Rounding.

• Intercompany Receivables determines which account receives the debit entry of an

intercompany billing Receivables invoice.

• Intercompany Rounding determines the accounts for the pair of debit and credit

entries due to intercompany billing invoice currency rounding.

Determining Accounts for Intercompany Payables Invoices

You can modify the Supplier Invoice Charge Account Workflow process to determine
and post the accounting entries for a receiver operating unit’s intercompany Payables
invoice. The process usually debits an internal cost or construction-in-process account
and credits the intercompany payables account in the receiver operating unit. See
Workflow: Project Supplier Invoice Account Generation, Oracle Projects Implementation
Guide.

Intercompany Billing Accounting Examples

An intercompany cross charge transaction against an indirect project results in the
intercompany billing accounting entries shown in the following two tables.

The following table shows entries for the provider operating unit.

6-22 Oracle Project Costing User Guide

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Cost

Labor Expense

Intercompany
Accounts
Receivable -
Invoice

Labor Clearing

Intercompany
Accounts
Receivable

Intercompany
Revenue

Dr

Cr

Dr

Cr

50,000 JPY

50,000 JPY

50,000 JPY

50,000 JPY

200,000 JPY

200,000 JPY

200,000 JPY

200,000 JPY

The following table shows entries for the receiver operating unit.

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Intercompany
Accounts
Payable -Invoice

Intercompany
Cost

Intercompany
Accounts
Payable

Dr

Cr

200,000 JPY

2,000 USD

200,000 JPY

2,000 USD

An intercompany cross charge transaction against a contract project results in the
intercompany billing accounting entries shown in the following two tables.

The following table shows entries for the provider operating unit.

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Cost

Labor Expense

Intercompany
Accounts
Receivable -
Invoice

Labor Clearing

Intercompany
Accounts
Receivable

Intercompany
Revenue

Dr

Cr

Dr

Cr

50,000 JPY

50,000 JPY

50,000 JPY

50,000 JPY

200,000 JPY

200,000 JPY

200,000 JPY

200,000 JPY

The following table shows entries for the receiver operating unit

Cross Charge

6-23

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Intercompany
Accounts
Payable -Invoice

Intercompany
Cost

Intercompany
Accounts
Payable

Client Revenue

UBR/UER

Client Invoice

Revenue

Accounts
Receivable

UBR/UER

Dr

Cr

Dr

Cr

Dr

Cr

200,000 JPY

2,000 USD

200,000 JPY

2,000 USD

4,000 USD

4,000 USD

4,000 USD

4,000 USD

4,000 USD

4,000 USD

4,000 USD

4,000 USD

Determining Accounts for Provider Cost Reclassification

Oracle Projects provides a pair of debit and credit AutoAccounting functions to
support the reclassification of cost in the provider operating unit upon generating
intercompany invoices. For example, a provider operating unit may need to reclassify
project construction-in-process costs against a contract project using cost accrual as
intercompany costs upon billing the receiver operating unit. Oracle Projects provides the
following AutoAccounting functions for this purpose:

• Provider Cost Reclass Dr. This function determines which account receives the

debit entry of the cost reclassification.

• Provider Cost Reclass Cr. This function determines which account the credit entry

of the cost reclassification.

A provider cost reclassification results in the intercompany billing accounting entries shown
in the following two tables.

The following table shows entries for the provider operating unit.

6-24 Oracle Project Costing User Guide

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Cost

Provider Cost
Reclassification

Intercompany
Accounts
Receivable -
Invoice

Construction - In
- Process

Labor Clearing

Labor Expense

Construction - In
- Process

Intercompany
Accounts
Receivable

Intercompany
Revenue

Dr

Cr

Dr

Cr

Dr

Cr

50,000 JPY

50,000 JPY

50,000 JPY

50,000 JPY

50,000 JPY

50,000 JPY

50,000 JPY

50,000 JPY

200,000 JPY

200,000 JPY

200,000 JPY

200,000 JPY

The following table shows entries for the receiver operating unit.

Process

Accounting

Debit (Dr) Credit
(Cr)

Transaction
Currency

Functional
Currency

Intercompany
Accounts
Payable -Invoice

Intercompany
Construction - In
- Process

Intercompany
Accounts
Payable

Client Revenue

UBR/UER

Revenue

Cost Accrual

Cost Accrual

Client Invoice

Construction - In
- Process Contra

Accounts
Receivable

UBR/UER

Dr

Cr

Dr

Cr

Dr

Cr

Dr

Cr

200,000 JPY

2,000 USD

200,000 JPY

2,000 USD

4,000 USD

4,000 USD

4,000 USD

4,000 USD

500 USD

500 USD

500 USD

500 USD

3,000 GBP

4,000 USD

3,000 GBP

4,000 USD

Close Project

Cost Accrual

Dr/Cr (see note)

1,500 USD

1,500 USD

Intercompany
Construction - In
- Process

Cr

1,500 USD

1,500 USD

Cross Charge

6-25

Note: The examples in the previous two tables show that the provider
operating unit originally posted a cross charge transaction to a
construction-in-process account during the cost distribution process. The
intercompany billing process then transfers the construction-in-process
amount with a markup to the receiver operating unit and generates
the provider cost reclassification accounting entries. The consolidated
expenditure is always booked as construction-in-process after costing
and intercompany billing.

Generating Intercompany Invoices

Running the standard cost distribution processes in the provider operating unit
identifies which transactions require intercompany billing processing. Oracle Projects
provides separate processes to compute the transfer price of the intercompany billing
transactions and generate draft intercompany invoices and (optionally) provider cost
reclassification entries.

To use the intercompany billing processing method, you must perform several setup
steps, including creating an intercompany billing project. See: Setting Up for Cross
Charge Processing: Intercompany Billing, Oracle Projects Implementation Guide.

The Generate Intercompany Invoice processes (The PRC: Generate Intercompany
Invoices for a Single Project and PRC: Generate Intercompany Invoices for a Range of
Projects) carry out the following steps:

1. Create invoice details, page 6-26

2. Create invoices and invoice lines, page 6-27

3.

(Optional) Generate provider cost reclassification entries, page 6-28

See: Generate Intercompany Invoices, Oracle Projects Fundamentals.

Calculate the Transfer Price Amount

The Generate Intercompany Invoices processes calculate the transfer price amount using
the same steps as described for the Distribute Borrowed and Lent Amounts process.

Run AutoAccounting

After the process calculates the transfer price amounts for each selected intercompany
billing transaction, it runs AutoAccounting to determine the intercompany revenue
account for each cross charged transaction, using the Intercompany Revenue function.

Determine Tax Codes

The Oracle Receivables tax code is defaulted for each transaction based on the tax
defaulting hierarchy defined in your implementation options. The process also
determines the intercompany tax receiving task for the transaction.

Create Intercompany Invoice Details

The process then creates intercompany invoice details for each transaction with the
transfer price amount, intercompany revenue account, and tax code.

6-26 Oracle Project Costing User Guide

Create Invoices and Invoice Lines

The Generate Intercompany Invoice process groups the invoice details of cross charged
transactions into invoices and invoice lines.

The Generate Intercompany Invoice process:

• Verifies intercompany billing projects

• Creates invoice

• Creates invoice lines

• Generates provider cost reclassification entries

Verify intercompany billing projects

Create invoice

The process verifies that each specified intercompany billing project meets the following
criteria before generating an invoice and invoice lines:

• (Mass generation only) Billing cycle criteria have been met.

• Invoice details exist that have not yet been included in an invoice.

• The project customer, and customer bill and ship to sites must all be

active. Otherwise, Oracle Projects creates an invoice marked with generation error.

• The project customer must not be on credit hold. Otherwise, Oracle Projects creates

an invoice marked with generation error.

• The status of the intercompany billing project must not be Closed.

Depending on how the provider operating unit has implemented the provider
controls, this step creates:

• A consolidated intercompany invoice for all cross charged projects of a receiver
operating unit. In other words, one draft invoice for each intercompany billing
project.

• One intercompany invoice for each cross charged project. In other words, multiple
invoices for an intercompany billing project when multiple cross charged projects
exist for a receiver operating unit. Oracle Projects orders such invoices by generating
status (invoices with errors appear last) and the project number of the cross charged
project.

The process uses the date of the invoice as the GL date.

Create invoice lines

The process uses the following criteria to group invoice details to generate invoice lines:

• Cross-charged project

• Tax attributes

• Intercompany revenue account

• Invoice format components

Invoice lines are then created for the invoices based on the grouped invoice details.

Cross Charge

6-27

Note: If an invoice line amount is zero due to offsetting invoice
details, the process does not create the invoice line and includes the
invoice details for that line in an exception report.

Generate Provider Cost Reclassification Entries

Depending on how the provider operating unit has set up the internal billing
implementation options, this process optionally creates the cost reclassification
accounting entries using the following AutoAccounting functions:

• Provider Cost Reclass Dr

• Provider Cost Reclass Cr

You can review the entries from the View Accounting window. See Create Cross Charge
Distribution Lines, page 6-21 for more information on using the View Accounting
window.

You can interface these entries to Oracle General Ledger using the Interface Cross Charge
Distributions to GL process only after you have interfaced the related intercompany
invoices to Oracle Receivables.

Approving and Releasing Intercompany Invoices

Approving and releasing intercompany invoices consists of the following actions:

1. Review intercompany invoices in the Invoice Review window.

From this window, you can drill down from a draft intercompany invoice to draft
intercompany invoice lines to the underlying cross charged transactions.

2. Approve intercompany invoices as you would a customer invoice.

3. Release intercompany invoices as you would a customer invoice.

Note: Oracle Projects generates the invoice number for
intercompany invoices and customer invoices from different
sequences because different batch sources are used to interface these
invoices to Oracle Receivables.

4.

(Optional) Delete unapproved intercompany invoices as you would a customer
invoice.

Interfacing Intercompany Invoices to Receivables

The PRC: Interface Intercompany Invoices to Receivables process interfaces released
intercompany invoices to Oracle Receivables. You can run this process separately
or as a streamline process (choose the XIC: Interface Intercompany Invoices to AR
parameter). The streamline process includes the following processes:

1.

Interface Intercompany Invoices to Receivables, page 6-29

2. AutoInvoice, page 6-29

3. Tieback Invoices from Receivables, page 6-29

6-28 Oracle Project Costing User Guide

Interface Intercompany Invoices to Receivables

This process interfaces intercompany invoices with active Bill To and Ship To address
to the Oracle Receivables interface table. It identifies the following debit accounts for
intercompany invoices:

• Intercompany Receivables

• Intercompany Rounding

Oracle Projects provides the AutoAccounting function Intercompany Invoice Accounts to
determine the receivables and rounding accounts. The intercompany revenue account is
already available on the invoice lines for intercompany invoices.

Once in Oracle Receivables, intercompany invoices are identified with a batch source of
PA Internal Invoices and a transaction type of either Internal Invoice or Internal Credit
Memo. You can query receivables information by project-related query data. Project
information in Oracle Receivables is located in the Transaction Flexfield and Reference
field. The fields in Oracle Receivables which hold project-related data for intercompany
invoices (reference field of the PA Internal Invoices batch source) are shown in the
following table:

Oracle Receivables Field Name

Oracle Projects Data

Transaction Flexfield Value 1

Project number of the intercompany billing
project

Transaction Flexfield Value 2

Draft invoice number from Oracle Projects

Transaction Flexfield Value 3

Receiving operating unit

Transaction Flexfield Value 4

Project manager

Transaction Flexfield Value 5

Project number of the cross charged project

Transaction Flexfield Value 6

Line number of the invoice line

Transaction Flexfield Value 7

Invoice type of the invoice

Line grouping rule and line ordering rule in Oracle Receivables for intercompany
invoices are as follows:

• Line grouping. Uses Transaction Flexfield Values 1 through 4.

• Line ordering. Uses Transaction Flexfield Values 5 through 7.

Decentralized invoice collections are not enabled for intercompany invoices.

AutoInvoice

The Oracle Receivables Invoice Import process pulls invoices from the Oracle
Receivables interface tables. See: Oracle Receivables User Guide.

Tieback Invoices from Receivables

The Tieback Invoices from Receivables process verifies the successful interface of
intercompany invoices to Oracle Receivables. Intercompany invoices successfully
interfaced to Oracle Receivables are also automatically interfaced to the Oracle Payables

Cross Charge

6-29

system of the receiver operating unit. See: Tieback Invoices from Receivables, Oracle
Projects Fundamentals.

Interfacing Intercompany Invoices to Oracle Payables

Interfacing intercompany invoices to the invoice tables in Oracle Payables consists
of the following steps:

1.

Interfacing intercompany invoices to the Payables interface table, page 6-30

2. Running the Open Interface Import process in Payables, page 6-31

Interface intercompany invoices to the Payables interface table

When the provider operating unit runs the Tieback Invoices from Receivables
process, the intercompany invoices are automatically copied into the interface table of
the receiver operating unit’s Payables. Intercompany invoices interfaced to Payables are
identified with the following attributes:

• Source. All intercompany invoices have a source of Oracle Projects Intercompany.

• Supplier. The supplier is identified by the provider operating unit’s internal billing

implementation options.

• Supplier Site. The supplier site is based on how the provider operating unit defines

the receiver controls for the receiver operating unit.

• Invoice Amount. The Payables invoice amount is the amount of the related

Receivables invoice, including taxes.

The interface process populates the project-related attributes for intercompany Payables
invoice distributions, as indicated below:

• Project Number. The number of the cross charged project indicated in the invoice

line.

• Task Number. The number of the task specified in the Intercompany Tax Receiving

Task field on the cross charged project.

• Expenditure Item Date. The invoice date of the intercompany Receivables invoice.

• Expenditure Type. The expenditure type specified by the receiver operating unit

in the Receiver Controls tab.

• Expenditure Organization. The expenditure organization specified by the receiver

operating unit in the Receiver Controls tab.

In addition, the interface process matches the tax code from each invoice line of the
Receivables invoice to the appropriate Oracle Payables tax code. This process indicates
that the Payables invoice distributions do not include tax amounts, so that the Payables
Open Interface process creates the invoice distributions for the entire invoice by
grouping the tax lines based on the following attributes:

• Tax code

• Project information (project, task, expenditure item date, expenditure

type, expenditure organization)

Note: Tax group support in Oracle Payables is provided only by the
Canadian or other localizations.

6-30 Oracle Project Costing User Guide

Run the Open Interface Import process in Payables

The receiver operating unit runs the Open Interface Import process in Payables to
create intercompany Payables invoices. Payables Open Interface Import performs the
following steps:

• Convert amounts from the transaction currency to the functional currency of the
receiver operating unit based on the default conversion attributes defined in the
receiver operating unit’s Payables system options. (The Receivables invoice amounts
are copied as the transaction currency amounts on the Payables invoice.)

You can customize the Payables Open Interface workflow process to override the
default currency conversion attributes for the invoice and distribution amounts.

• Derive the intercompany Payables account from supplier information. You can either
associate supplier types for internal suppliers with intercompany cost accounts or
otherwise modify the Workflow-based account generation process to determine the
appropriate intercompany cost account. Payables Invoice Import generates the
following sample accounting entries:

DR Intercompany Cost

CR Intercompany Payables

• Generate recoverable and non-recoverable tax lines (if you have specified a

percentage for recoverable tax amounts), based on the tax codes matched from
Oracle Receivables.

Oracle Payables uses the rounding accounts specified in the Oracle Payables system
options to account for discrepancies due to rounding tax amounts.

Interface Tax Lines from Payables to Oracle Projects

After the Payables Invoice Import process generates non-recoverable tax lines for the
intercompany invoice, you must run the Interface Supplier Costs process to interface
these non-recoverable tax lines to Oracle Projects as project costs.

Tax lines interfaced from Oracle Payables are not subject to any cross charge processing
and are not adjustable in Oracle Projects.

Related Topics

Interfacing Supplier Costs, page 7-20

Interface Supplier Costs, Oracle Projects Fundamentals

Interfacing Cross Charge Distributions to General Ledger

If you use borrowed and lent accounting or intercompany billing with cost
reclassification enabled, you must interface the resulting accounting entries from Oracle
Projects to Oracle General Ledger. Interfacing cross charge distributions to Oracle
General Ledger consists of the following steps:

1. Run the Interface Cross Charge Distributions process to General Ledger process,

page 6-32.

2. Run Journal Import. See: Oracle General Ledger User Guide.

3. Run the Tieback Cross Charge Distributions from General Ledger

process (see: Tieback Cross Charge Distributions from GL, Oracle Projects

Cross Charge

6-31

Fundamentals), which determines whether the Journal Import process rejected any
cross charge distributions.

You can run these processes individually or as part of a streamline process. To run the
streamline process, choose the parameter XC: Interface Cross Charge Distributions to GL.

Run the Interface Cross Charge Distributions to General Ledger process

The provider operating unit runs the PRC: Interface Cross Charge Distributions to
General Ledger process.

This process does not interface accounting entries of the intercompany
invoices. Instead, the provider operating unit interfaces intercompany invoice revenue
and receivables to Oracle General Ledger using the standard functionality of Oracle
Receivables. The receiver operating unit posts intercompany Payables invoice
distributions using the Payables Transfer to Oracle General Ledger process.

PRC: Interface Cross Charge Distributions to General Ledger performs the following
actions:

• Identify cross-distributions that have not yet been interfaced to Oracle General

Ledger

Note: You cannot interface cross charge distributions for provider
cost reclassification entries until you have interfaced the associated
intercompany invoices to Receivables.

• Determine the GL date for all distributions eligible for interfacing based on the

earliest open or future GL period ending on or after the distribution’s PA date

• Generate a batch name by concatenating the credit account and GL date and store

this information on each distribution

• Summarize distributions by debit account and line type

• Summarize distributions by credit account and line type

• Create journal entries in the Oracle General Ledger interface tables

Adjusting Cross Charge Transactions

This section provides an overview and a description of the processing flow for
adjustments to cross charge transactions.

Overview of Cross Charge Adjustments, page 6-32

Processing Flow for Cross Charge Adjustments, page 6-35

Overview of Cross Charge Adjustments

Due to data entry errors or changes in your organization or business rules, you may need
to adjust certain attributes of cross charged transactions. Doing so causes Oracle Projects
to reprocess the transactions or to skip the cross charge processes completely. You
can adjust a cross charged transaction by:

1. Marking transactions for cross charge reprocessing, page 6-33

2. Marking transactions to skip cross charge processing, page 6-34

6-32 Oracle Project Costing User Guide

3. Changing transfer price conversion attributes, page 6-34

4. Making the following miscellaneous adjustments, page 6-34

5. Changing transfer price base amounts

6. Changing the provider or receiver organization using the mass update feature

7. Recompiling burden schedules

8. Performing splits and transfers

9. Performing adjustments on the Receivables or Payables invoices

Marking transactions for cross charge reprocessing

You can mark one or more transactions for cross charge reprocessing in the Expenditure
Items window. For example, if you have changed cross charge setup data and want
this new information reflected in the affected transfer price amounts and accounting
entries, select the Reprocess Cross Charge option in the Reports menu of the Expenditure
Items window.

Marking a transaction for cross charge reprocessing:

• Resets the cross charge type to Null

• Resets the cross charge processing method to Pending

• Resets the cross charge processing status to Never Processed

• Resets the transfer price amount in all currencies to Null

• Redetermines the cross charge type and processing method

The next time you run the cross charge processes, they will process these transactions as
new cross charged transactions.

You should mark affected transactions for cross charge reprocessing if you have changed
any of the following information:

• Provider or receiver organization. Modifying the Provider and Receiver

Organizations Override extension or changes in your organizational structure
can result in changes to the provider or receiver organization of a cross charged
transaction, which could affect the cross charge type, the processing method, or
the transfer price rules.

• Transfer price setup data. Any change to your transfer price rules could result in
a new transfer price amount determined for cross charged transactions that have
already been processed.

• Cross-charge setup data. Any change to your cross charge or internal billing

implementation options, provider and receiver controls, or cross charge project and
task information can affect how Oracle Projects processes cross charged transactions.

• Account codes. Changes to the provider reclassification accounting options can

result in changes to the provider cost reclassification accounts. Any changes to the
AutoAccounting setup for cross charge functions can also affect existing cross
charge accounting entries.

• Billable flag. For cross charged transactions processed by intercompany billing with
the provider cost reclassification feature enabled, changes to the Billable flag of a
transaction on a contract project can result in new provider cost reclassification
accounting entries.

Cross Charge

6-33

• Tax codes. The Generate Intercompany Invoice processes determine the appropriate
tax code for each invoice line. If you modify the logic used to derive the tax codes
and have already released invoices, you must mark the affected transactions for
cross charge reprocessing. Oracle Projects automatically creates a credit memo for
the original invoice and a new invoice with the new tax codes.

Marking transactions to skip cross charge processing

You can mark one or more transactions so that the cross charge processes skip the
specified transactions. To do this, choose Mark For No Cross Charge Processing in the
Reports menu of the Expenditure Items window.

Marking a transaction as not requiring cross charge processing resets the cross charge
processing method to No Cross Charge Processing and the cross charge processing
status to Never Processed.

Changing transfer price conversion attributes

You can reconvert transfer price amounts from the transaction currency if you change
the transfer price exchange rate date type and exchange rate type, which govern how
Oracle Projects converts the transfer price amount from the transaction currency to
the functional currency. To do this, you choose the Change Transfer Price Currency
Attributes option from the Reports menu in the Expenditure Items window. A change
in these conversion attributes may result in a change to the transfer price amount in
the functional currency.

Both provider and receiver operating units can change the transfer price conversion
attributes.

Changing your transfer price currency conversion attributes:

• Replaces conversion attributes for the functional currency

• Resets existing transfer price amounts in the functional currency to Null

• Resets the cross charge processing status to Never processed

Making miscellaneous cross charge adjustments

You can perform the following adjustments to cross charged transactions. These
adjustments automatically mark the transaction for cross charge reprocessing.

• Changing transfer price base amounts. If you recalculate raw or burdened cost
or revenue amounts, the amount of the transfer price basis (and the final transfer
price amount) of a cross charged transaction may also change. The respective
cost distribution and revenue generation processes determine whether such
recalculations affect the transfer price amount of any cross charged transactions and
automatically mark the transactions for cross charge reprocessing.

The cost distribution and revenue generation processes automatically resets the
cross charge processing status to Never Processed and blanks out the transaction’s
transfer price amount.

• Changing the provider or receiver organization using the mass update feature. If
you use the mass update feature to change the organization that owns a project or
task, Oracle Projects marks all transactions (with an expenditure date after the
effective date of the organization change) for cross charge reprocessing. A different
project (or receiver) organization could result in a change to the transaction’s cross
charge processing method.

6-34 Oracle Project Costing User Guide

Oracle Projects automatically marks the affected items for cross charge processing.

• Recompiling burden schedules. If the user changes and recompiles a burden

schedule that has been used for determining the transfer price of some items, the
recompile process will mark these items for cross charge reprocessing by resetting
the cross charge type to Null, the cross charge processing method to Pending, and
the cross charge processing status to Never Processed.

• Performing transfers and splits. Transferring or splitting a cross charged transaction

does not affect the cross charge processing method of the existing transactions. The
reversing and new transactions will undergo the cross charge processes as usual.

The Generate Intercompany Invoice processes group the invoice details for all
adjusting transactions by the invoice number and line number of the original
transactions for credit memo processing.

• Performing adjustments on the Receivables or Payables invoices. You can adjust
invoice level accounting information for Receivables and Payables invoices, as
described below:

• Intercompany Receivables account (for Receivables invoices). The Interface
Intercompany Invoices to Receivables process determines the intercompany
receivables account for each invoice. If you change the rules used to determine
this account, you must manually cancel the invoice from the Invoice Review
window. Oracle Projects automatically creates a credit memo with details
reversing each line in the original invoice. All items on the cancelled invoice are
eligible for intercompany rebilling. Once rebilled, the Interface Intercompany
Invoices to Receivables process will determine the account for the new invoice
using the modified rules.

You cannot cancel an invoice if payments have been applied against it in Oracle
Receivables or if an invoice has credit memos applied against it. You can cancel
an invoice only if it is released and has no payments, adjustments, or crediting
invoices applied against it. Once the cancellation is completed, you cannot
delete the credit memo created by the cancellation action. That is, you cannot
reverse an invoice cancellation.

• Intercompany cost account (for Payables invoices). In Oracle Payables, reverse

the invoice distribution with the incorrect intercompany cost account and create
a new line with the correct account information.

Processing Flow for Cross Charge Adjustments

After you mark an adjustment to a cross charged transaction for reprocessing, Oracle
Projects processes these adjustments similarly to the original transactions. The
processing flow for adjustments is described in further detail on the following pages.

The cross charge processes perform the following common steps on adjustments marked
for cross charge reprocessing, regardless of whether the transactions require borrowed
and lent or intercompany billing processing:

• Recalculate the transfer price if no transfer price amount exists in the transaction

currency

• Reconvert the transfer price amount from the transaction currency to the functional
currency if an amount exists in the transaction currency but not the functional
currency

Cross Charge

6-35

Processing Borrowed and Lent Adjustments

After the PRC: Distribute Borrowed and Lent Amounts process completes the common
processing steps for cross charge adjustments, it performs the steps for borrowed and
lent adjustments, as described below.

• Regenerate accounting entries. If any of the accounts have changed from entries
already interfaced to Oracle General Ledger, the Distribute Borrowed and Lent
Amounts process reverses the original cross charge distributions and creates
new ones. The process also determines the PA dates for the reversing and new
distributions. If the original accounting entries have not yet been transferred to
Oracle General Ledger and the accounts or amounts have changed, the process
replaces them with the new entries.

• Reverse existing distributions if processing method has changed. If the cross

charge processing method for the transaction changes from borrowed and lent to
intercompany billing or no cross charge processing, the process reverses existing
entries that have been interfaced to Oracle General Ledger.

Processing Intercompany Billing Accounting Adjustments

After the Generate Intercompany Invoice process completes the common processing
steps for cross charge adjustments, it performs the following steps:

1. Redetermine the intercompany revenue account and tax code.

The revenue account and tax code is redetermined for the adjusted transactions. If
intercompany invoice details already exist for the transaction, the Generate
Intercompany Invoice process compares the recalculated transfer price amount
to the existing transfer price amount. If they are different, you must reverse the
existing invoice detail line and create a new one. Similarly, if the process detects a
difference in the new intercompany revenue account or tax code and the existing
values, reversing and new invoice details are created.

2. Create a credit memo.

The Generate Intercompany Invoice process creates a credit memo, in which
reversing invoice details are grouped together by the invoice number and invoice
line number on which the original invoice details are billed.

3. Create new invoices.

New invoice details reflecting changed values for the transfer price, revenue
account, and tax code are grouped into new invoices.

4.

(Optional) Regenerate provider cost reclassification accounting entries.

If any of the accounts have changed from entries already interfaced to Oracle
General Ledger, the Generate Intercompany Invoice process reverses the original
distributions and creates new ones. The process also determines the PA date for
both the reversing and new distributions. If the original accounting entries have not
yet been transferred to Oracle General Ledger and the accounts or amounts have
changed, the process replaces them with the new entries.

6-36 Oracle Project Costing User Guide

7
Integration with Other Oracle Applications

This chapter describes integrating Oracle Projects with other Oracle Applications to
perform project costing.

This chapter covers the following topics:

• Overview of Oracle Project Costing Integration

• Integrating Expense Reports with Oracle Payables and Oracle Internet Expenses

• Integrating with Oracle Purchasing and Oracle Payables (Requisitions, Purchase

Orders, and Supplier Invoices)

• Integrating with Oracle Assets

• Integrating with Oracle Project Manufacturing

• Integrating with Oracle Inventory

Overview of Oracle Project Costing Integration

This chapter describes Oracle Projects integration with other Oracle Applications to
perform project costing and includes the following topics:

• Integrating Expense Reports with Oracle Payables and Oracle Internet Expenses,

page 7- 1

• Integrating with Oracle Purchasing and Oracle Payables (Requisitions, Purchase

Orders and Supplier Invoices), page 7-16

• Integrating with Oracle Assets, page 7-31

• Integrating with Oracle Project Manufacturing, page 7-35

• Integrating with Oracle Inventory, page 7-36

For information on overall Oracle Projects integration and detail information on
integration with applications such as General Ledger, and Oracle Human Resources, see
the Integrating with Other Oracle Applications chapter in Oracle Projects Fundamentals.

Integrating Expense Reports with Oracle Payables and Oracle Internet
Expenses

You can enter expense reports containing project and task information in Oracle
Projects, Oracle Internet Expenses, or Oracle Payables. Additionally, you can import

Integration with Other Oracle Applications

7-1

project-related expense reports in Oracle Projects from third-party systems through
Transaction Import.

This section describes how to ensure that transactions resulting from project-related
expense reports are properly accounted.

Related Topics

Transaction Import, Oracle Projects APIs, Client Extensions, and Open Interfaces Reference

Overview of Expense Report Integration

Project-related expense reports can be entered directly into Oracle Projects through batch
entry. Additionally, external expense report data can be imported directly into Oracle
Projects via Transaction Import. Oracle Projects processes these expense reports and
sends them to Oracle Payables.

You can also create project-related expense reports through Oracle Internet
Expenses. Additionally, you can enter project-related expense reports directly into the
Oracle Payables invoice entry screens. Payables creates invoices from the expense
reports, maintains and tracks payments, and then sends the accounting transactions
to Oracle General Ledger. After these tasks are accomplished, the expense reports
can be sent to Oracle Projects.

All accounting entries from project-related expense reports are interfaced to General
Ledger from Oracle Payables.

Expense Reports Entered in Oracle Projects

When expense reports are created in Oracle Projects, they are entered through
preapproved expenditure entry. An expense report must first be cost distributed, then
sent to Oracle Payables (for invoice creation and payment) and finally, tied back to
Oracle Projects. For more information see: Processing Expense Reports Created in
Oracle Projects, page 7- 4 .

Expense Reports Imported into Oracle Projects

Expense reports imported directly into Oracle Projects from an external source, such
as a third-party application, are processed in the same way as expense reports entered
via preapproved expenditure entry. After the transactions are imported, they must be
costed (if necessary), then sent to Payables (for invoice creation and payment), and
finally tied back to Oracle Projects.

Expense Reports Entered in Oracle Internet Expenses

Employees can include project and task information in an expense report created in
Oracle Internet Expenses. (Click the Enter Receipts tab to display the window containing
the Project Number and Task Number fields. The window displays these fields if you
select an expense type that is associated with an Oracle Projects expenditure type.)

Expense reports entered in Oracle Internet Expenses must be sent to Payables and then to
Oracle Projects. These expense reports have an expenditure type class of Expense Report
and do not need to be tied back to Oracle Projects. For more information, see: Processing
Expense Reports Created in Oracle Internet Expenses, page 7-10.

7-2 Oracle Project Costing User Guide

Expense Reports Entered in Payables

You can enter project and task information on expense reports in the Invoices window
in Payables (enter Expense Report in the Type field). Expense reports entered in the
Invoices window are assigned an expenditure type class of Expense Report and are
processed in Oracle Projects similarly to expense reports entered in Oracle Internet
Expenses. The Expense Report window in Payables does not record project information
for expense report lines. Use the Invoices window instead. For information, see Oracle
Payables User Guide.

For All Expense Reports

You can use standard reports to track your expense reports as the expense report
information moves from one application to another.

You can also use Payables features to create advances (prepayments) and
adjustments, and then apply them against Oracle Projects expense reports and invoices
in Payables. See: Advances and Prepayments, page 7-13 and Adjusting Expense
Reports, page 7-13.

Setting Up in Payables and Oracle Projects

Before you can interface project-related expense reports between Oracle
Projects, Payables, and Oracle Internet Expenses, you must carry out certain tasks.

• In Payables:

• Define employees as suppliers

• Accept or override the employee address

• Determine the expense report cost account

• (Optional) In the System Administrator responsibility, set profile options

Define Employees as Suppliers

Before Payables can create invoices for an employee’s expense reports, the employee
must be defined as a supplier. You can either enable Payables to create a supplier
automatically for employees lacking a supplier record or enter the employee manually
as a supplier in the Suppliers window.

If an employee is not a supplier, Payables does not create an invoice and lists the expense
report as an exception.

To define employees as suppliers:

1.

In Payables, navigate to the Payables Options window.

2. Choose the Expense Report tab.

3. Enable Automatically Create Employee as Supplier.

Accept or Override the Employee Address

Payables sends the reimbursement to the employee’s default address (Home or
Office), which is set for the employee in HR. You can override the Home or Office setting
in the Expense Reports window in Payables.

Payables uses the same value when creating supplier sites for the supplier record.

Integration with Other Oracle Applications

7-3

Determine the Expense Report Cost Account

For expense reports entered in Oracle Projects and adjustments made to those expense
reports, Oracle Projects uses AutoAccounting (not the employee’s default expense
account) to determine the expense report cost account.

For expense reports entered in Oracle Internet Expenses and the Invoices window, an
account generator (the Project Expense Report Account Generator, a process in Oracle
Workflow) determines the expense account for each transaction that includes project and
task information. The Default Account Generator for Expense Reports process used the
CCID (code combination identifier) entered for the employee in Human Resources.

For more information, see: Using the Account Generator in Oracle Projects, and
AutoAccounting and the Account Generator, Oracle Projects Implementation Guide.

(Optional) Set Profile Options

Using the System Administrator responsibility, open the System Profile Values window
and set the following profile options:

• PA: Summarize Expense Report Lines specifies whether lines in expense reports created
in Oracle Projects are summarized by code combination ID when you interface
the expense reports to Payables. See: Profile Option-Summarize Expense Report
Line, Oracle Projects Implementation Guide.

• PA: Allow Project Time and Expense Entry specifies whether a user can

enter project-related transactions in Oracle Internet Expenses. See: Profile
Option-PA: Allow Project Time and Expense Entry, Oracle Projects Implementation
Guide.

• PA: Expense Report Invoices Per Set specifies the number of Payables invoices to

process each time the Interface Expense Reports from Payables (a Payables process)
is run. See Profile Option-PA: Expense Report Invoices Per Set, Oracle Projects
Implementation Guide.

• PA: Allow Override of PA Distributions in AP/PO indicates whether a user is allowed
to update the accounting flexfield combination that is generated by FlexBuilder
for Oracle Projects distributions in Oracle Payables and Oracle Purchasing. See
Profile Option-PA: Allow Override of PA Distributions in AP/PO, Oracle Projects
Implementation Guide.

Related Topics

Integrating with Oracle Payables, page 7-18

Implementing Oracle Payables for Projects Integration, Oracle Projects Implementation
Guide

Profile Options for Integration with Other Products, Oracle Projects Implementation Guide

Resource Definition, Oracle Projects Implementation Guide

Processing Expense Reports Created in Oracle Projects

To prepare for interfacing expense reports created in Oracle Projects, you must first
distribute the expense report costs. Then, you can send the costed expense reports to
Payables whenever you are ready and as many times during an accounting period
as you wish.

7-4 Oracle Project Costing User Guide

The following illustration shows the processing flow when expense reports are created
in Oracle Projects.

Processing Expense Reports Created in Oracle Projects

The illustration Processing Expense Reports Created in Oracle Projects, page 7- 5 shows the
following steps:

1. Costed expense reports are interfaced into the Payables interface table from Projects.

2. The Expense Report Import process imports the data into Payables invoice tables

and creates expense report invoices.

3. The Projects Tieback process verifies that the project-related expense reports were

successfully imported into Oracle Payables.

4. Payables interfaces the accounting for the invoices to General Ledger.

Distributing Expense Report Costs

You must run the Distribute Expense Report Costs process before you interface expense
reports with Payables. This process groups expenditure items into batches of expense
reports and determines the expense account held in the cost distribution line.

Interfacing Expense Reports to Payables

Note: Two processes have very similar names. The process described
here sends expense report information to Payables.

The Interface Expense Reports to Payables process collects eligible costed expense
reports in Oracle Projects and sends them to the Payables Invoice interface tables. Once
loaded onto these interface tables, the expense reports await further processing by the
Expense Report Import program.

When you send invoices to Payables, Oracle Projects sets the purgeable flag for each
expense report in Payables to No.

This process also sends costed adjustments to Oracle Internet Expenses expense
reports that you interfaced from Payables. Payables loads these adjustments into the

Integration with Other Oracle Applications

7-5

Payables invoice tables automatically, so you do not need to run the Expense Report
Import program.

Before you interface expense reports to Payables, run the PRC: Distribute Expense
Report Costs process to distribute costs for any adjustments you have made.

Note: If expense reports from any source fail to post to Payables, you
may need to redistribute costs (using the PRC: Distribute Expense Report
Costs process) before you send the expense reports to Payables again.

For more information, see: Interface Expense Reports to Payables, Oracle Projects
Fundamentals.

Determining the Accounting Period

The GL Date of the expense report cost determines the accounting period in which a
transaction is posted to a general ledger account. In Oracle Projects, the GL Date for
costs is the end date of the earliest open or future GL Period that is on or after the latest
PA Date of the cost distribution lines included in an expense report. All cost distribution
lines for an expense report are sent together to Payables and use the same GL Date. This
GL Date becomes the GL Date of the invoice in Payables. See: Date Processing in Oracle
Projects, Oracle Projects Fundamentals.

Determining the Liability Account

The Interface Expense Reports to Payables process uses AutoAccounting to determine
the liability account when the expense reports costs are distributed. (Oracle Projects
does not use the employee’s default expense account.) The process sends the accounting
information for expense reports to the Payables interface tables.

Reports

Oracle Projects generates a report that lists the interfaced and rejected expense
reports. Correct the rejected expense reports and resubmit them to Payables.

Importing Expense Reports in Payables

Expense Report Import is a Payables program. See: Expense Report Import
Program, Oracle Payables User Guide.

The Expense Report Import program creates invoices and invoice distribution lines
from Oracle Projects expense report information that you load into Payables interface
tables. Payables imports the expense report data into Payables invoice tables.

Note: Expense Report Import does not call Workflow. If you manually
populate the invoice import tables, you must supply the accounting
flexfield information.

Oracle Payables identifies invoices you create from Oracle Projects expense reports
with a source of Oracle Projects.

If you submit the program from Payables, you must specify a source of Oracle
Projects. Leave the batch name and GL date blank. You can also use one of the Oracle
Projects streamline options to submit the Expense Report Import program from Payables.

Adjustments are a special case. You do not need to run Expense Report Import for
adjustments to expense reports already interfaced or tied back from Payables.

7-6 Oracle Project Costing User Guide

Prerequisites:

• Enter expense reports in Oracle Projects.

• Run the Oracle Projects PRC: Distribute Expense Report Costs process to calculate

the amount and generate accounts.

• Submit Oracle Projects PRC: Interface Expense Reports to Payables process to

transfer expense reports to the Payables Invoice Interface Tables.

• If the Automatically Create Employee As Supplier option is not enabled in

Payables, enter the employee as a supplier in the Suppliers window.

To import invoices from Oracle Projects:

In the Submit Request window, choose the Request Type and select Expense
Report Import.

• Enter the report parameters.

Do not enter a batch name or a GL date field. Select Oracle Projects for the source.

If you want to purge expense reports from the Invoice Import Interface Tables, enter
the date criteria you want Payables to use. Payables will delete all Oracle Projects
expense reports that were entered before this date and have already been imported
and tied back to the original expense report in Oracle Projects.

• Choose OK.

When the program is complete, you can query the new invoices in the Invoices
window. The new invoices are ready for approval and payment.

Payables creates invoices with the attributes shown in the following table:

Integration with Other Oracle Applications

7-7

Attribute

Type

Supplier Name

Invoice Date

Invoice Number

Invoice Distributions

Invoice Liability Account

Description

Expense Report

Employee name

Week ending date

The expenditure batch name from Oracle
Projects appended to a unique identifier for
the expense report

Based on cost distribution of expense
report items. Each invoice distribution in
Oracle Projects includes expenditure item
information, such as project information,
amount, and account coding.

Based on AutoAccounting rules in Oracle
Projects

Scheduled Payments

Defaults from supplier site

Payment Method

Income Tax Type

Defaults from supplier site

For federally reportable 1099 suppliers,
Payables provides the income tax type for
each invoice distribution

Payables automatically produces the following reports so you can review the
invoices that Expense Report Import successfully created, and the invoices that
Expense Report Import was unable to import:

• Expense Report Import Report

• Expense Report Import Exceptions Report

• Expense Report Import Prepayments Applied Report

• In Oracle Projects, run the PRC: Tieback Expense Reports from Payables process.

Reports

Oracle Projects generates a report that lists the interfaced and rejected expense
reports. Correct the rejected expense reports and resubmit them to Payables.

Tying Back Expense Reports from Payables

The Tieback Expense Reports from Payables process links the expense report in Oracle
Projects to the invoice in Payables, but does not tie back the invoice details. (To view
details, drill down in the Expenditures Inquiry window. You can also query the invoice
in the Invoices window in Payables.)

The tieback process identifies expense reports rejected by Expense Report Import. Correct
the rejected expense reports and send them to Payables again.

Tying back the invoices causes Oracle Projects to update the purgeable flag for each
expense report in the Payables interface tables from No to Yes.

7-8 Oracle Project Costing User Guide

For more information, see: Tieback Expense Reports from Payables, Oracle Projects
Fundamentals.

Submitting the Interface Streamline Processes

Streamline processes submit two or more one processes in one step. You can use
streamline processes to interface expense reports to Payables, import the invoices, and
tie back the invoices to Oracle Projects. Streamline processes submit each process
sequentially.

If you want to perform a single function, such as interfacing expense reports, you
can use an individual process.

Some processes use a lot of system resources, so do not run processes that distribute costs
(DXES, DXEU and DTE) during critical processing times. Instead, run the distribution
processes separately, and then run the interface and tieback streamline processes later.

To submit the streamline process, use one of the streamline options shown in the
following table:

Process Abbreviation

Process Name

DXES

DXEU

XES

XEU

DTE

ITES

ITEU

Distribute and Interface Expense Report Costs
to AP

Distribute and Interface Expense Report Costs
to AP

Interface Expense Report Costs to AP

Interface Expense Report Costs to AP

Distribute and Transfer Expense Report Costs
to AP

AP Invoice Import and Tieback Expense
Reports

AP Invoice Import and Tieback Expense
Reports

Note: In the preceding table, the following processes create
summarized reports that display expense report lines summarized
by code combination identifier: DXES, XES, and ITES (AP Invoice
Import). See: PA: Summarize Expense Report Lines, Oracle Projects
Implementation Guide.

In the preceding table, the following processes are detailed report
processes that generate an invoice distribution in Oracle Payables for
each detail expense report cost distribution line: DXEU, XEU, ITEU (AP
Invoice Import).

You must use the same report mode (see notes above), either summarized or
detailed, to interface expense report costs to Payables and then tie back those expense
reports, regardless of whether you submit a streamline process or an individual process.

Integration with Other Oracle Applications

7-9

For more information, see: Submitting Streamline Processes, Oracle Projects Fundamentals.

Transferring Payables Accounting Information to General Ledger

After the Expense Report Import program creates invoices, and you approve, pay, and
account for them in Payables, use the Payables Transfer to General Ledger program to
send the invoice information to General Ledger interface tables.

In General Ledger, post the invoice interface data to update your account balances. For
information on importing and posting journals, see the Oracle General Ledger User Guide.

Processing Expense Reports Created in Oracle Internet Expenses

This section covers the following topics:

• Importing Expense Reports in Payables, page 7-11

• Transferring Payables Accounting Information to General Ledger, page 7-11

• Interfacing Expense Reports from Payables, page 7-11

Note: Except as noted, the information in this section also applies to
expense reports created in the Invoices window (in Payables).

The following illustration shows the steps in processing project-related expense reports
created in Oracle Internet Expenses.

Processing Expense Reports Created in Oracle Internet Expenses

The illustration Processing Expense Reports Created in Oracle Internet Expenses, page
7-10 shows that expense reports created in Oracle Internet Expenses go directly
to the Payables interface tables. You run the Expense Report Import program to

7-10 Oracle Project Costing User Guide

send this information from the Payables interface tables to the Payables invoice
tables. Additionally, project-related expense reports that are entered through the Invoices
window in Payables go directly to the Payables invoice tables.

Once the expense reports are in the Payables invoice tables, Payables creates the
appropriate accounting transactions for these project-related expense reports. Payables
creates these project-related transactions based on business rules you defined in the
Projects Expense Report Account Generator.

Internet expenses are interfaced to Oracle Projects by the Interface Expense Reports from
Payables. This information initially goes to the Oracle Projects interface tables. The
process continues and automatically imports the transactions to the Projects Expenditure
Items Table.

Expense reports that are entered directly into Oracle Projects are interfaced to Payables
through the Interface Expense Reports to Payables process.

You can adjust expense reports entered in Oracle Internet Expenses in either Payables
or Oracle Projects. You can also transfer or split expense report items (net zero
adjustments), recost the entered expense reports, and then send the information
to Payables. Payables ultimately posts these adjusted transactions to General
Ledger. See: Adjusting Expense Reports, page 7-13.

Importing Expense Reports In Payables

Note: You do not need to import expense reports entered directly in
the Invoices window, because the system saves those expense reports
directly to the Payables invoice tables.

The Expense Report Import program processes expense reports created in Oracle
Internet Expenses as well as those entered in Oracle Projects and interfaced to Payables.

Payables identifies invoices created from Oracle Internet Expenses expense reports
with a source of Oracle Internet Expenses.

Adjustments to expense reports created in Self-Service Expenses or the Invoices window
(in Payables) are loaded directly into the AP invoice tables. You do not need to run
Expense Report Import, either as an individual process or as part of the streamline
interface processes ITES and ITEU.

For prerequisites and procedures for importing project-related expense reports from
Self-Service Expenses, see: Expense Report Import Program, Oracle Payables User Guide.

Transferring Payables Accounting Information to General Ledger

After the Expense Report Import program creates invoices, and the invoices (expense
reports) are approved, paid, and accounted in Payables, use the Payables Transfer to
General Ledger program to send the invoice information to the General Ledger interface
tables.

In General Ledger, you post the invoice interface data to update your account
balances. For detailed information about interfacing and posting journals see the Oracle
General Ledger User Guide.

Interfacing Expense Reports from Payables

Note: Two processes have very similar names. The process described
here gets expense report information from Payables.

Integration with Other Oracle Applications

7-11

After you post the invoice accounting entries to General Ledger, use the Interface
Expense Reports from Payables process to import the invoice to Oracle Projects. This
process calls the Transaction Import process, which:

• Loads project-related invoice accounting entries

• Calculates the burden amounts for the appropriate imported raw costs

• Creates a pre-approved expense report batch in Oracle Projects, based on the

project-related invoice accounting entries

• Imports descriptive flexfield information entered in Oracle Internet Expenses or

Payables

Note: Projects holds 10 descriptive flexfield segments. If you are
using more than 10 segments in Payables, only the first 10 are
imported to Projects.

See: Descriptive Flexfield Mapping Client Extension, Oracle Projects
APIs, Client Extensions, and Open Interfaces Reference

Oracle Projects generates transactions with a source of Oracle Payables. The Allow
Adjustments option is enabled for the Oracle Payables source, but only net zero
adjustments are allowed. You cannot reverse or recalculate burdened costs.

For more information about this process, see: Interface Expense Reports from Payables,
Oracle Projects Fundamentals.

Prerequisites:

Before you run this process:

• Enter expense reports in Oracle Internet Expenses or the Invoices window.

• Verify that employees are designated as suppliers. (If they are not, the interface

program will not import the invoice.) Conversely, suppliers must be designated as
employees. See: Setting Up in Payables and Oracle Projects, page 7- 3 .

Invoices generated for contingent workers are made payable to the supplier of the
contingent worker rather than the worker. To process expense reports for contingent
workers, the assignment record associated with the contingent worker in Oracle
Human Resources Management System must specify a supplier.

• Run the Payables Transfer to General Ledger program in Payables.

This process generates a report that lists the interfaced and rejected invoice distribution
lines, as well as a summary of the total number and cost of the distribution lines.

Correct the rejected invoice distribution lines (refer to the rejection reasons shown on the
report), and then resubmit the process.

Generating Accounts for Oracle Payables, Oracle Projects Implementation Guide

Expense Report Import Program, Oracle Payables User Guide

Transferring Payables Accounting Information to General Ledger, page 7-10

Reports

Related Topics

7-12 Oracle Project Costing User Guide

Advances and Prepayments

In Payables, you can create an advance, or prepayment, to an employee for travel or
other expenses. After an expense report is loaded into Payables, you can use Payables
to apply the prepayment against Oracle Projects expense reports. When an employee
incurs an expense and submits an expense report, you reduce the amount of the expense
report reimbursement by applying outstanding prepayments to it.

You can apply prepayments to an expense report when the expense report is in the
Payables interface tables or when the expense report is loaded in Payables as an invoice.

To apply prepayments to expense reports:

1. Use Payables to enter a prepayment, approve it, and pay it (see: More About

Prepayments, page 7-13).

2. Enter and approve the expense report in Oracle Projects and then release the

expense report batch.

3. Distribute expense reports and interface them to Payables using Oracle Projects

processes.

You can use the DTE Distribute and Interface Expense Report Costs to AP streamline
option.

4. Apply the prepayment to an expense report using the Expense Reports window in

Payables (see below).

5. Run the Expense Report Import program and tie back invoices from Payables
to Oracle Projects. You can use either of the following Oracle Projects interface
streamline options:

6.

7.

ITES: AP Invoice Import and Tieback Expense Reports

ITEU: AP Invoice Import (Unsummarized Report) and Tieback Expense Reports.

8. Review invoices and payments in Payables.

More About Prepayments

When you enter a prepayment, Payables automatically creates invoice distributions and
a scheduled payment.

Use the Invoices window in Payables to create and approve prepayments. You must
approve and pay a prepayment before you can apply it to an invoice to reduce the
amount you owe. You can use the Payments window in Payables to pay a prepayment.

Use the Expense Reports window in Payables to apply a prepayment or enter a hold
against an expense report. You can apply prepayments and holds to expense reports
after you interface expense reports into Payables, but before you run Expense Report
Import and create invoices from the expense reports. You cannot change any information
for an Oracle Projects expense report in the Expense Report window; you can only
apply prepayments or holds.

You can also apply prepayments and holds to expense reports after you run Expense
Report Import when the expense reports are invoices in Payables.

For more information, see: Prepayments, Oracle Payables User Guide.

Adjusting Expense Reports

How you adjust an expense report depends on which application was used to create it.

Integration with Other Oracle Applications

7-13

Note: Adjustments interfaced to Payables appear on the same invoice in
Payables. Adjustments interfaced from Payables appear in a separate
expense report batch.

Adjusting Expense Reports Created in Oracle Projects

If you created an expense report in Oracle Projects, you should generally make the
adjustments in Oracle Projects. You can adjust an expense report in Oracle Projects at
any time, but you cannot interface adjustments to Payables until an invoice exists in
Payables and you have run the tieback process.

Interfacing expense reports links adjusting transactions in Oracle Projects to the
corresponding invoice in Payables. This linkage allows you to reconcile all project-related
expense reports in Payables, and accurately account for your cash books if you use
Cash Basis Accounting.

Note: Any adjustments made in Oracle Payables to expense reports that
originated in Oracle Projects are not interfaced back to Oracle Projects
and will result in out-of-balance subledgers.

Adjusting Expense Reports Created in Oracle Internet Expenses

Note: The information in this section also applies to expense reports
created in the Invoices window (in Payables).

Expense reports created in Oracle Internet Expenses and the Invoices window can be
adjusted in both Oracle Projects and Payables:

• In Oracle Projects, you can transfer or split expense lines (net zero adjustments). You

cannot reverse expenditure items or recalculate burdened costs.

• In Payables, you can:

• Modify line amount, project, task, or expense types by reversing existing invoice

distribution lines and then creating new ones

• Cancel the invoice completely

Before you can make adjustments in Oracle Payables or cancel an invoice in
Payables, each application checks for outstanding adjustments or cancellations in
the other. If outstanding adjustments exist, you must interface the adjustments
before continuing.

You cannot adjust an Oracle Internet Expenses expense report if any of the following
conditions are true:

• The invoice has been cancelled in Payables

• Adjustments made to this invoice in Payables have not been sent to Oracle Projects

• The item has been fully or partially prepaid

• The invoice has been fully or partially paid and either the Allow Adjustments to
Paid Invoices option is disabled, or discount payment distributions have been
associated with the invoice

• You are using cash basis accounting

For more information, see: Adjusting Invoices, Oracle Payables User Guide.

7-14 Oracle Project Costing User Guide

Purging Expense Reports

After you create invoices in Payables and then tie them back, you can create more
space in your database by purging imported Oracle Projects expense reports from
the Payables interface tables. To do so, identify the date through which you want to
purge expense reports when you submit Expense Report Import. Payables purges the
expense reports during the import process.

For expense reports created in Oracle Internet Expenses, you can have the Expense
Report Import program purge imported information. The purge occurs after the program
creates invoices from expense report information and the tieback process is complete.

It is a good practice to purge expense reports periodically.

Viewing Expense Reports in Oracle Payables

After you successfully send expense reports to Payables and run the Expense Report
Import program, each expense report in Payables is converted to a Payables invoice. You
can view these expense reports in Payables (just as you can any other invoice), as well as
in Oracle Projects.

To view invoices that have been created from Oracle Projects expense reports, open the
Invoices or Distributions window, query the project, task, and expenditures. In other
windows, query the information that Oracle Projects passes to Payables:

• The employee name becomes the supplier name. The name appears in uppercase

when it is generated by the system in Payables.

• The week ending date, or expenditure ending date, becomes the invoice date

in Payables.

• The total expense report cost becomes the total invoice amount in Payables.

For each invoice distribution in Payables, you can also view information for each
expenditure item, such as the project information, the amount, and the account coding.

To query the payment status of an employee’s expense report, use the Find Invoices
window and query by supplier name and invoice date. See Example: Finding an
expense report, page 7-16.

Note: You can use the Expense Reports window in Payables to
view expense reports submitted from Oracle Internet Expenses. The
window also displays expense reports interfaced from Oracle Projects
to Payables. Note that the Expense Reports window does not display
project and task information.

Interpreting Invoice Numbers

For expense reports entered in Oracle Projects, the invoice number is the expenditure
batch name (from Oracle Projects) plus an expense report identifier. For example, the
invoice number EX-DEN-125 R11-DEC-95 12:00:00-1000 is an invoice that was processed
in the expenditure batch of EX-DEN-125 R11-DEC-95 12:00:00, which is identified by
the number 1000.

Interpreting Expense Report Batch Names

For expense reports entered in Oracle Projects, the expenditure batch name is a
concatenation of the expenditure batch parameter, the type of batch, and the creation
date and time.

Integration with Other Oracle Applications

7-15

If you do not specify an expenditure batch parameter when you submit the Distribute
Expense Report Costs process, the batch name prefix is ALL. The letter R represents a
regular expense report batch, and the letter A represents an adjusted expense report
batch. For example, a regular expense report batch could be named ALL R16-SEP-98
14:46:05 and a specific batch could be named EX-HQ-D523 A16-SEP-98 12:00:05.

Example: Finding an expense report

Your employee, Amy Marlin, wants to know the status of an expense report that she
submitted on October 1, 1998. The expenditure ending date of her expense report was
15-SEP-1998. Expense reports are submitted to the local accounting staff for entry
into Oracle Projects. You don’t know when the expense report was entered in Oracle
Projects or sent to Payables.

In Payables, navigate to the Find Invoices window and enter %Marlin% in the supplier
name field. Enter invoice dates beginning September 1, 1998. Choose the Find button.

The Invoices window displays all of Amy Marlin’s expense reports with expenditure
ending dates after August 31, 1998 that have been sent to Payables. You will see if the
expense report is in Payables, and has been posted to General Ledger, approved, and
paid. You can also drill down to the individual distribution line items and see project
information.

If the Invoices window does not display the expense report, check to see if the expense
report has been sent to Payables but not yet imported. Navigate to the Expense Reports
window and query by Employee Name or Number.

Related Topics

Integrating with Oracle Payables, page 7-18

Expense Reports and Credit Cards, Oracle Payables User Guide

Reviewing and Adjusting Invoices, Oracle Payables User Guide

Integrating with Oracle Purchasing and Oracle Payables (Requisitions,
Purchase Orders, and Supplier Invoices)

Oracle Projects fully integrates with Oracle Purchasing and Oracle Payables and allows
you to enter project-related requisitions, purchase orders, and supplier invoices using
those products.

When you enter project-related transactions in Oracle Purchasing and Oracle
Payables, you enter project information on your source document. Oracle
Purchasing, Oracle Payables, and Oracle Projects carry the project information through
the document flow: from the requisition to the purchase order in Oracle Purchasing, to
the supplier invoice in Oracle Payables, and to the project expenditure in Oracle Projects.

Oracle Purchasing and Oracle Payables use the Account Generator to determine
the account number for each project-related distribution line based on the project
information that you enter.

Using Oracle Projects views, you can report committed costs of requisitions and purchase
orders that are outstanding against your projects in Oracle Projects.

7-16 Oracle Project Costing User Guide

Related Topics

Oracle Payables and Oracle Purchasing Integration, Oracle Projects Implementation Guide

Project-Related Document Flow

When you enter project-related documents, you specify project information in addition
to the information you normally specify for a document. You can use all the standard
features of Oracle Purchasing and Oracle Payables, including encumbrance accounting
and funds checking, when you enter project-related documents.

Integrating with Oracle Purchasing

When you enter project-related transactions in Oracle Purchasing, you only need to enter
project information on the source document -- either the requisition or the purchase
order. When you automatically create purchase orders from requisitions using Oracle
Purchasing AutoCreate feature, the project information from the requisition is copied
to the purchase order.

Entering Requisitions

You enter project-related purchase requisitions using the Requisitions window in
Oracle Purchasing. You can enter default project information in the Requisitions
Preferences window in the Project Information tabbed region. This default information
will be used to populate requisition distribution lines you create during your current
session. The requisitions distribution line has a Project tabbed region for you to enter
project-related information. A requisition can have a combination of project-related
and non-project-related distribution lines.

Using AutoCreate

When you automatically create purchase orders from project-related requisitions in the
AutoCreate Documents window, Oracle Purchasing copies the project information and
the accounting information from the requisition to the purchase order. You do not need
to enter any additional project-related information on your purchase order when you use
this feature. See: AutoCreate Documents Overview, Oracle Purchasing User’s Guide.

You can change the project information on the purchase order that was copied from the
requisition; the project information on the requisition is not updated.

Entering Purchase Orders

If your company does not use online requisitions or the AutoCreate feature, you can
enter project-related information directly on your standard purchase orders using the
Purchase Orders window in Oracle Purchasing. When you use this window, you specify
project-related information in the Project tabbed region of the distribution line. The
account information will automatically be created by the Account Generator, based on
the project-related information you enter. See: Overview of Purchase Orders, Oracle
Purchasing User’s Guide.

Entering Releases

You enter project-related releases against blanket purchase agreements and planned
purchase orders using the Enter Releases window in Oracle Purchasing. When you
use this window, you specify if the release distribution line is project-related. If it is

Integration with Other Oracle Applications

7-17

project-related, you continue to enter project information for the line. See: Entering
Release Headers, Oracle Purchasing User’s Guide.

Recording Receipts and Delivery

You can track receipt and delivery of goods for project-related purchase orders using the
Receipts window in Oracle Purchasing. You can report the delivery of purchased goods
in your commitment reporting. Oracle Purchasing does not record the received goods as
delivered for your project until the goods are delivered and assigned to a purchase order
distribution line. See: Overview of Receipts, Oracle Purchasing User’s Guide.

When a purchase order line is flagged to accrue on receipt and the purchased goods
are delivered to an expense destination, you can interface receipt accrual accounting
entries from Oracle Purchasing to Oracle Projects as actual transactions. This allows
you to recognize the cost to your project in the period in which it is incurred rather
than in the period in which it is invoiced. For more information, see: Overview of
Receipt Accounting, Oracle Purchasing User’s Guide, and Interface Supplier Costs, Oracle
Projects Fundamentals.

Entering Default Project-Related Information for Requisitions and Purchase Orders

You can enter default project-related information for requisitions and purchase orders.

To enter default project information for requisitions and purchase orders:

1.

2.

In Oracle Purchasing, open either the Requisitions or Purchase Orders window.

Select the Tools menu option at the top of the window and choose Preferences.

3. Open the Project Information tabbed region and enter default project information

to be used to create requisition and purchase order distribution lines during the
current session.

4.

Save.

Integrating with Oracle Payables

When you match an invoice to a purchase order or receipt in Oracle Payables, the project
information from the purchase order or receipt is copied to the invoice. When you
enter new project-related invoices in Oracle Payables, you only need to enter project
information on the source document, the invoice. If you use distribution sets with
project information, Oracle Payables automatically supplies project information for
your supplier invoice distribution lines.

Matching Invoices

If you use Oracle Purchasing and have already associated project-related information to
a purchase order, and you are matching an invoice to a purchase order or receipt using
the Invoices windows instead of manually creating invoice distribution lines, Oracle
Payables automatically copies the project information from the purchase order or
receipt to the invoice.

You cannot change the project information that is copied from the purchase order to
the invoice.

7-18 Oracle Project Costing User Guide

Entering Invoices

You can enter project-related invoices directly in the Invoices windows in Oracle
Payables. You can enter project-related information in the Invoices window which will
default to all distributions you enter for the invoice. These values can be overridden. You
also enter project-related information in the Distributions window. You can create a
folder with project-related fields to be used for entering information. An invoice can
have both project-related and non-project-related distribution lines. See: Entering
Invoices Overview, Oracle Payables User Guide.

Note: You can also import through the Payables Open Interface tables
projects-related invoices from the Invoice Gateway and other systems.

Using Distribution Sets

You can define distribution sets to make it easier to enter invoices. Use the Distribution
Sets window to specify project information for the distribution set lines. You
can use project-related distribution sets for recurring costs for any project class
(contract, indirect, and capital). See: Distribution Sets, Oracle Payables User Guide.

When you enter invoices, you can enter a distribution set. You can use distribution sets
to create project-related invoices in the following Oracle Payables forms:

• Invoices

• Recurring Invoices

Posting Invoices

After you process invoices according to your business policies, you approve them in
Oracle Payables, and interface the invoice information to Oracle General Ledger interface
tables. You use the Payables Transfer to General Ledger process in the Submit Request
window in Oracle Payables to interface invoices to General Ledger.

In General Ledger, you post the invoice interfaced data to update your account
balances. See: Posting Journals, Oracle General Ledger User Guide.

Entering Default Project-Related Information for Supplier Invoices

You can enter default project-related information in Oracle Payables.

To enter default project information for a single supplier invoice:

1.

In Oracle Payables, open the Invoices window.

2. Enter default project information to be used to create the distribution lines for

the invoice.

3.

Save and continue entering the invoice information.

Tip: Create project-oriented folders at the invoice and invoice
distribution line level to make it easier and faster to enter project
related information for your invoices.

To enter default project information in supplier invoice distribution sets:

1.

In Oracle Payables, open the Distribution Sets window located under Setup, Invoice.

2. For project-related distribution lines, check the Project Related box. This will open

the Project Information window.

Integration with Other Oracle Applications

7-19

3. Enter default project information to be used to create the distribution lines, then

select OK to close the window.

4.

Save.

You can review and change project information in the distribution set by selecting the
Project Information button at the bottom of the window.

Interfacing Supplier Costs

To load invoices and receipt accruals from Oracle Payables and Oracle
Purchasing, respectively, to Oracle Projects, use the PRC: Interface Supplier Costs
process in Oracle Projects.

The Interface Supplier Costs process uses the project and task information to determine
if the items are billable, capitalizable, or both. You can accrue revenue and invoice
billable items in Oracle Projects.

The process selects transactions based on the parameter values entered. It first retrieves
all eligible accounted, project-related receipt accrual information, supplier invoice
distributions (including non-recoverable tax lines) and all payment discounts that are
distributed to project-related distributions. The process then interfaces the amounts
to Oracle Projects.

The interfaced items are grouped into expenditure batches. All invoice
distributions, excluding non-recoverable tax lines, are included in one
batch. Non-recoverable tax lines are grouped into a second batch, payment discounts
are included in a third batch, and receipt accruals for project related items with a
destination type of Expenses are grouped in the fourth batch. Within each batch, an
expenditure is created for each invoice and an expenditure item is created for each
invoice or discount distribution.

Each time you run Interface Supplier Costs process, Oracle Projects generates reports you
can use to track the interfaced supplier invoices distribution lines, receipt accruals, as
well as those invoice lines and receipt accruals that are rejected during interface from
Oracle Payables and Oracle Purchasing, respectively.

Related Topics

Recoverable Tax, Oracle Payables User Guide

Entering Project-Related Information for Requisitions, Purchase Orders, and Supplier
Invoices

You enter project information at the distribution line level for project-related requisitions
and purchase orders in Oracle Purchasing, and for project-related supplier invoices in
Oracle Payables.

Default Project Information

You can specify default project information at the header level for requisitions, purchase
orders, and supplier invoices; this information defaults to the document’s distribution
lines. For purchase orders, you can also specify default project information at the
purchase order line and purchase order shipment levels.

The default project information for requisitions and purchase orders are session defaults
which are lost when you exit the entry forms. The default project information for
invoices is stored with the invoice and is retained when you query the invoice.

7-20 Oracle Project Costing User Guide

Project-Related Information

When you enter requisitions, purchase orders, and supplier invoices in Oracle
Purchasing or Oracle Payables, and have Oracle Projects installed, you specify the
following project-related information:

The Project Number segment is the project number incurring the charge from the
requisition, purchase order, or invoice.

The Task Number is the lowest level task incurring the charge from the
requisition, purchase order, or invoice.

The Expenditure Type is an expenditure type classified with an expenditure type class of
Supplier Invoices.

The Expenditure Organization is the organization that is ordering or has ordered the goods
or services, which may be different from the project owning organization.

This organization defaults to the organization you specify in the profile option PA: Default
Expenditure Organization in AP/PO. This profile option provides a default value for the
expenditure organization segment each time you create project information in Oracle
Payables or Oracle Purchasing. You can choose from any expenditure organization that
has an HR Classification as your default value. Your system administrator can configure
this default profile at the site, application, responsibility, and user levels; each user can
also specify their own personal value for this profile.

The Expenditure Item Date is the date that you expect to incur the expense for the goods
or services that you are requesting for a requisition or purchase order, or the date that
you incur the charge for an invoice. This date is used during online validation against
project transaction controls, and becomes the expenditure item date on the expenditure
item in Oracle Projects. This date defaults to the current date each time you create a
new Accounting Flexfield combination.

The Quantity is the quantity of goods or services that you are charged for. You can
enter data in this field only in Oracle Payables, as this field is applicable for invoice
distributions only.

This value is required if you have defined the expenditure type with Cost Rate Required
set to Yes. For expenditure types that require a cost rate, the quantity on the invoice
distribution becomes the quantity in the expenditure item and a cost rate is calculated
as the amount divided by the quantity when Oracle Projects interfaces the invoice
distribution and creates an expenditure item in Oracle Projects.

For other expenditure types that do not require a cost rate, the quantity in the invoice
distribution is not copied to the expenditure item; instead the amount of the line is
copied as the quantity and the amount on the expenditure item.

Entering Project-Related Fields by Document

You do not need to enter information for each project field for all documents in Oracle
Purchasing and Oracle Payables. For example, you do not need to enter information for
expenditure item date and quantity if you are entering invoice distribution sets.

The following table specifies the project information that you enter for each document
in Oracle Purchasing.

Integration with Other Oracle Applications

7-21

Document

Requisition

Purchase Order

Location

- Requisition Level (default
only)

Fields

- Project

- Task

- Requisition Distribution Line
Level

- Expenditure Type

- Expenditure Organization

- Expenditure Item Date

- Project

- Task

- Expenditure Type

- Expenditure Organization

- Expenditure Item Date

- Purchase Order Level
(default only)

- Purchase Order Line Level
(default only)

- Purchase Order Shipment
Level (default only)

- Purchase Order Distribution
Line level

Release

- Release Distribution Line
Level

- Project

- Task

- Expenditure Type

- Expenditure Organization

- Expenditure Item Date

The following table specifies the project information that you enter for each document in
Oracle Payables.

Document

Invoice

Location

Fields

- Invoice Level (default only)

- Project

- Invoice Distribution Line
Level

- Task

- Expenditure Type

- Expenditure Organization

- Expenditure Item Date

- Quantity (Distribution level
only)

Distribution Set

- Distribution Set Line Level

- Project

- Task

- Expenditure Type

- Expenditure Organization

Requisition, Purchase Order, and Release

You do not enter the quantity for documents in Oracle Purchasing because you do not
know the quantity for which you will be invoiced.

Oracle Payables automatically sets the quantity field to the quantity invoiced of the
invoice distribution line when you match an invoice to a purchase order or receipt.

7-22 Oracle Project Costing User Guide

Invoice

Distribution Set

You can enter all of the project fields for an invoice line. The quantity field is optional if
the expenditure type does not require a quantity.

You do not enter the Expenditure Item Date in the distribution set lines you create
in Oracle Payables because you use the distribution sets for an indefinite period of
time. When you use the distribution set to create an invoice, Oracle Payables sets the
expenditure item date of the invoice distributions to the invoice date of the invoice.

Validating Purchase Orders, Requisitions, and Supplier Invoices

When you enter project information and save the record, the information is validated
against the project transaction control information in Oracle Projects. This validation
ensures that you can charge the type of expenditure to the project and task on the
expenditure item date that you specified. If the information that you entered does not
pass the project transaction control validation, you will see an error message displayed
on the bottom line of the screen. You must enter valid chargeable project information
based on the transaction controls in Oracle Projects before you can continue.

Note: The expenditure item date and the date of the invoice must both
be in an open or future Projects period.

If you cannot determine valid project information that is chargeable, you can delete the
project-related fields and close the window. You should then determine valid project
information and return to the document to enter the project information.

Validation of Distribution Set Project Information

When you create a distribution set in Oracle Payables, the project information for a
distribution set line is not validated against the project transaction controls information
in Oracle Projects, because you do not enter an expenditure item date which is required
for transaction control validation.

Usually, distribution sets are used on recurring transactions, and the associated project
does not have transaction controls. The only validation Oracle Projects performs on
a distribution set is at the time you create the distribution set lines. Oracle Projects
validates the project and task number.

Funds Check Activation in Oracle Purchasing and Oracle Payables

In Oracle Purchasing and Oracle Payables, funds check processes are activated when
you select the Check Funds option for a transaction, and also during the transaction
approval process.

When you select the Check Funds option, a successful funds check result does not
update budgetary control balances. You use the Check Funds option to verify available
funds for a transaction before requesting approval for the transaction.

During the transaction approval processes, a funds check is automatically performed. At
that time, if the funds check is successful, the transaction is approved and budgetary
control balances are updated.

Integration with Other Oracle Applications

7-23

Related Topics

Controlling Expenditures, page 2-24

Budgetary Controls, Oracle Project Management User Guide

Accounting Transactions Created by the Account Generator

Oracle Purchasing and Oracle Payables use the Account Generator to determine the
GL account number for each project-related distribution line based on the project
information that you enter.

Oracle Purchasing builds the account number for the charge, accrual, and variance
distribution accounts based on the Account Generator assignments that you define
during implementation. You can define your Account Generator processes so that
project-related requisitions and purchase orders use project-related information in the
Account Generator assignments and non-project-related documents use the Account
Generator assignments predefined by Oracle Purchasing.

If you are using Encumbrance Accounting, you can also define assignments for the
budget account based on project information.

The Account Generator builds the expense account number for project-related invoices
using assignments that you define during implementation. You must enter the account
number for non-project-related invoices. The Account Generator determines the
liability account for all invoices based on the liability account defaults provided by
Oracle Payables.

You can control whether users can override the account number determined by the
Account Generator for project-related distributions using the profile option PA: Allow
Override of PA Distributions in AP/PO.

For example, you may want only the Purchasing Manager and Payables Manager to
have the ability to override the project-related distributions. In this example, you set
the profile to No at the Site level and to Yes for the Payables Manager and Purchasing
Manager responsibilities.

Related Topics

Financial Periods and Date Processing for Financial Accounting, Oracle Projects
Fundamentals

Using the Account Generator in Oracle Projects, Oracle Projects Implementation Guide

Commitment Reporting

You can report the total costs of a project by reporting the committed costs along with
the actual costs. Committed costs are the uninvoiced, outstanding requisitions and
purchase orders charged to a project.

Total Project Costs = (Committed Costs + Actual Costs)

You can report the flow of committed costs, including associated nonrecoverable tax
amounts, through Oracle Purchasing and Oracle Payables. These committed costs
can include:

• Open requisitions (unpurchased requisitions)

• Open purchase orders (uninvoiced and non-delivered)

7-24 Oracle Project Costing User Guide

• Pending invoices (supplier invoices not yet interfaced to Oracle Projects to be

included in project costs)

Note: Both unapproved and approved open requisitions and purchase
orders show as commitments after you run the concurrent process to
update project summary amounts. When you drill-down to view
commitment details, if the Approved check box is enabled, then the
requisition or purchase order associated with the commitment has
been approved.

You can report summary committed cost amounts for your projects and tasks, and can
also review detail requisitions and purchase orders that backup the summary amounts.

Example of Commitment Reporting

Study the following example to understand the flow of committed costs through Oracle
Purchasing, Oracle Payables, and Oracle Projects.

You use requisitions, purchase orders, and receipt and delivery in Oracle Purchasing. You
record cost when goods are received to better manage your project progress and
schedule.

The following table provides examples of the charges that are incurred as you record
transactions. The table shows the effect of various actions, such as receiving the
goods against a purchase order, on committed costs and the total costs charged to a
project. Descriptions of each action are provided after the table.

In the table, certain column values are calculated as follows:

• Open Purchase Orders equals Ordered Purchase Orders less Delivered Purchase

Orders

• Total Committed Costs equals the sum of Open Requisitions, Open Purchase

Orders, and Pending Invoices

• Total Project Costs equals the sum of Total Committed Costs and Actual Costs.

Integration with Other Oracle Applications

7-25

Action Open

Requisitions

Ordered
Purchase
Orders

Delivered
Purchase
Orders

Open
Purchase
Orders

Pending
Invoices

Total
Committed
Costs

Actual
Costs

Total
Project
Costs

1000

200

800

200

200

200

800

800

800

500

500

500

800

300

300

300

200

800

500

300

200

0

0

0

0

0

0

400

0

0

0

0

0

0

0

400

1000

1000

500

500

600

1000

1000

500

1000

500

1000

500

1100

500

600

1100

200

600

800

0

0

600

600

5600

5600

400

5600

6000

100

0

0

0

0

0

Enter
Requisition

Create
Purchase
Order
from
Requisition

Receive
Goods

Receive
Invoice

Enter
Non-
Purchase
Order
Invoice

Interface

Invoices

Close
Purchase
Order

Close
Requisition

Charge
labor to
Project

Charge
Blanket
Purchase
Order

Detail for Example of Commitment Reporting Actions
1. Enter requisition

You enter and approve a requisition totalling $1000, with two lines of $800 and $200.

The requisition amount is included in the Open Requisitions and the Total
Committed Costs amounts.

2. Create purchase order from requisition

You create a purchase order for the first line of the requisition, totalling $800. You
approve the purchase order.

7-26 Oracle Project Costing User Guide

The Open Requisition amount decreases by $800 and the Ordered Purchase Order
and Open Purchase Order amounts increase by $800. The total committed costs
remain the same.

3. Receive delivery of purchased goods

The supplier delivers $500 of the $800 of goods that you ordered.

The Delivered Purchase Order amount increases by $500. The Open Requisition, and
Ordered Purchase Order, do not change. Because you accrue on receipt, the Open
Purchase Order and Total Committed Costs amounts decrease by $500 and the
Actual Costs amounts increases by $500.

4. Receive invoice for delivered goods

You are invoiced for the $500 of goods that you received. The Payables department
matches the invoice to the purchase order.

The Open Purchase Order amount, the Pending Invoice amount,the Total Committed
Costs amount, and the Ordered Purchase Order amount does not change.

5. Enter supplier invoice not associated with purchase order

You receive another invoice for $100 that is not associated with a purchase order. The
Payables department enters the invoice.

Both the Pending Invoice amount and the Total Committed Cost amounts increase
by $100. The Total Project Cost also increases because the Total Committed Costs
amount increases.

6.

Interface invoices to Oracle Projects

The Payables department approves, accounts for, and posts all invoices and accruals
to Oracle General Ledger, and then interfaces the supplier invoices to Oracle
Projects. The invoice costs totalling $100 are now recorded against your project in
Oracle Projects.

The Pending Invoice amount decreases by $100. The Total Committed Costs amount
decreases by $100. The Actual Costs amount increases by $100. The Total Project
Costs amount does not change.

7. Close purchase order

You close the purchase order that has $300 remaining, because you do not expect
any more activity against that purchase order. The purchase order is no longer
reported in your committed costs.

Closed purchased orders are not reported in the commitment reporting, so all of
the Purchase Order amounts are reduced for the purchase order closed. The Total
Committed Costs amount, and in turn, the Total Project Cost amount, decreases by
$300, which was the Open Purchase Order amount for the purchase order closed.

8. Close requisition

You close the requisition for $200 because you no longer need the goods
requested. The requisition is no longer reported in your committed costs.

Closed requisitions are not reported in the commitment reporting, so Open
Requisition amount decreases by $200 for the requisition that you close. The Total
Committed Costs amount, along with the Total Project Costs, also decreases by $200.

9. Charge labor costs to project

Integration with Other Oracle Applications

7-27

Employees working on your project record time to your project, which totals $5000.

The Actual Costs amount increases by $5000. The Total Project Costs amount also
increases.

10. Enter release against blanket purchase agreement

You need to order supplies for your project. You create a $400 release against a
blanket purchase agreement that your company has negotiated with a supplier.

The Ordered Purchase Order and Open Purchase Order amounts increase by
$400. In turn, the Total Committed Costs and Total Project Costs also increase.

Related Topics

Project Summary Amounts, Oracle Project Management User Guide

Implementing Commitments from External Systems, Oracle Projects Implementation Guide

Adjusting Project-Related Documents in Oracle Purchasing, Oracle Payables, and Oracle
Projects

This section describes the adjustments that you can make to project-related documents in
Oracle Purchasing, Oracle Payables, and Oracle Projects.

Requisition Adjustments

You can update project information on a requisition. If the requisition is included on a
purchase order before you update the project information, the purchase order is not
updated with the new project information. If the requisition line is included on a new
purchase order after you change the project information, Oracle Purchasing copies the
new project information to the new purchase order.

The Account Generator builds a new account number value when you change the project
information. The new project information is used in commitment reporting.

Purchase Order Adjustments

You can update project information on a purchase order, even after it is approved
and invoiced. However, you cannot update project information if there has been any
accounting activity on the purchase order (for example, if it is encumbered, or if it is
accrued on receipt and the distribution has been received or billed). If the purchase order
is invoiced before you update the project information, the invoice is not updated with
the new project information. If the purchase order line is invoiced on a new invoice after
you change the project information, Oracle Payables copies the new project information
to the new invoice.

The Account Generator builds a new account number when you change the project
information. The new project information is used in commitment reporting.

Supplier Invoice Adjustments in Payables

You can perform supplier invoice adjustments in Oracle Payables at any stage in the
process flow.

7-28 Oracle Project Costing User Guide

Adjusting project information for matched invoices

If you have matched an invoice to a purchase order, you cannot directly change any
of the project information copied from the purchase order. You may encounter cases
in which you want to change the project information; in particular, you may want to
change the expenditure item date that was copied from the purchase order, because the
expenditure item date on the purchase order was not maintained.

If you want to change the project information in this case, there are two ways of making
the change.

You can reverse the matching distribution line from the purchase order in the
Distributions window in Oracle Payables, change the purchase order project information
in Oracle Purchasing, and match the invoice to the purchase order again. See: Adjusting
Invoice Distributions, Oracle Payables User Guide.

You can also create two adjusting invoice distributions on the original invoice which
net to zero, but have different project information. This is a generally a simpler way
to correct the project information. Using either the Invoices or Distributions windows
in Oracle Payables, you first enter a negative distribution line with the same project
information as on the incorrect invoice distribution line. You then enter a positive
distribution line with the correct project information. The two lines that you entered
net to zero, but record the correction to the project information, without having to
match to the purchase order again.

Note: If you use the Retroactive Pricing of Purchase Orders feature in
Oracle Purchasing, and change project information on an invoice, you
must update the same project information on any subsequent
purchase order price adjustment or adjustment documents. For more
information, see: Retroactive Pricing of Purchase Orders, Oracle
Purchasing User Guide.

Adjusting manually entered, unposted invoices

You can directly change any or all of the project information before an invoice is
posted. The Account Generator derives a new account number based on the new project
information that you enter.

Adjusting manually entered, posted invoices

You cannot directly change any project information on a posted invoice. You must
reverse the distribution line and create a new distribution line with the new project
information using the Distributions window in Oracle Payables. See: Adjusting Invoice
Distributions, Oracle Payables User Guide.

Interfacing adjusting lines to Oracle Projects

If the original invoice distribution line that was reversed was not yet interfaced
to Oracle Projects, the Interface Supplier Invoices from Payables process does not
interface the original or reversing items, that are included on the same invoice, to
Oracle Projects. These items are marked as net zero adjustment lines that are not to
be interfaced to Oracle Projects. The new line with the correct project information
is interfaced to Oracle Projects.

If the original invoice distribution line that was reversed was interfaced to Oracle
Projects before the adjustment, the Interface Supplier Invoices from Payables process

Integration with Other Oracle Applications

7-29

interfaces the reversing and new invoice adjustment lines that you created to correctly
maintain project costs in Oracle Projects.

Supplier Invoice Adjustments in Oracle Projects

You perform the following adjustments for supplier invoices in Oracle Projects:

• Transfer between projects/tasks

• Split expenditure item

• Adjust supplier invoice expenditure items

• Enter a miscellaneous pre-approved expenditure item to adjust the related discount

amounts.

• Reclassify item as billable or non-billable

• Reclassify item as capitalizable or non-capitalizable

• Edit comment

• Hold or release from billing

Project users can perform these adjustments in Oracle Projects because the actions do
not change the amount of the invoice which is processed in Oracle Payables. These
adjustment actions change the project information of the supplier invoice item, which is
used in Oracle Projects processing.

After you have made adjustments to supplier invoice items, you must send the
adjustment information back to Oracle Payables so the Payables distribution lines match
what is recorded in Oracle Projects. Oracle Payables will interface adjustments that affect
the GL account number to Oracle General Ledger. You run the following processes in
Oracle Projects for supplier invoice adjustments:

• PRC: Distribute Supplier Invoice Adjustment Costs

• PRC: Interface Supplier Invoice Adjustment Costs to Payables

If you need to change the invoice amount, supplier, or expenditure type, organization, or
item date for a supplier invoice line, reverse the line and create a new line in Oracle
Payables. See: Adjusting Project Information for Matched Invoices, page 7-29.

Restrictions to Supplier Costs Adjustments

Adjustments to supplier costs in Oracle Projects must adhere to the specific business
rules for supplier invoices and receipt accruals.

Supplier Invoices

When Projects is integrated with Payables, you cannot adjust supplier invoices (either in
Oracle Projects or in Oracle Payables) if the invoice is:

• Cancelled

When you cancel an invoice in Payables, reversing distribution lines are created
for each distribution line, and the invoice amount is set to zero. The invoice status
is set to Cancelled, and its distribution lines are posted to GL the next time the
Transfer to General Ledger program is run in Payables. When an invoice has a
status of Cancelled, it cannot be adjusted.

• Paid, if any of the following conditions apply:

7-30 Oracle Project Costing User Guide

• The Payables setup option Allow Adjustments to Paid Invoices is disabled

Oracle Payables provides a system-level control to prevent users from adjusting
paid invoices. If you want to allow adjustments to paid invoices, enable the
Allow Adjustments to Paid Invoices setup option in the Payables Options window.

• You are using the Prorate Expense or Prorate Tax discount distribution method

Oracle Payables does not allow adjustments to paid invoices if a prorated
discount distribution method is used.

• You are using cash basis accounting

• Prepaid, either fully or partially

• Selected for payment

You cannot adjust an invoice selected for payment until the Confirm Payment Batch
action has been performed.

Receipt Accruals

You cannot adjust the item in Oracle Projects when the item is interfaced from Oracle
Purchasing. If the invoice is matched to an accrue on receipt purchase order line and
the invoice line (rather than the purchase order receipt) is interfaced, then the invoice
line can be adjusted in Oracle Projects.

Related Topics

Adjustments to Supplier Invoices, page 2-62

Integrating with Oracle Assets

Oracle Projects integrates with Oracle Assets, allowing you to manage capital projects in
Oracle Projects and update your fixed assets records when assets are ready to be placed
in service or retired. In a capital project, you can collect construction-in-process (CIP) and
expense costs for each asset you are building. In addition, you can perform retirement
cost processing to capture retirement-work-in process (RWIP) costs (cost of removal
and salvage) associated with the retirement of group assets in Oracle Assets. Oracle
Projects collects labor, expenses, usages, miscellaneous transactions, and supplier invoice
costs, and using a combination of AutoAccounting and Workflow, assigns the costs
either to a CIP, RWIP, or expense account.

When you are ready to place a capital asset in service, you use Oracle Projects processes
to collect all eligible CIP cost distribution lines, summarize them, and create capital
asset lines. When you complete the tasks that are necessary to retire a group asset in
Oracle Assets, you can summarize the RWIP amounts into retirement adjustment asset
lines. You can review and make changes to the asset lines before interfacing them to
Oracle Assets. When you are satisfied that the asset lines are correct, you use Oracle
Projects processes to interface the costs to the Oracle Assets Mass Additions table.

After you interface the costs to the Oracle Assets Mass Additions table, you can make
changes to the asset definition, if necessary, and then run the Post Mass Additions
process. This program creates the asset records in Oracle Assets. When you run the
Create Journal Entries process in Oracle Assets, journal entries are created and sent to
Oracle General Ledger to relieve the CIP or RWIP account and transfer the amount to the
appropriate asset cost or group depreciation reserve account.

Integration with Other Oracle Applications

7-31

You can interface asset costs from Oracle Projects to Oracle Assets whenever you are
ready and as many times during an accounting period as you wish.

There is currently no interface between Oracle Assets and Oracle Projects which allows
you to post depreciation expenses directly to projects.

Related Topics

Overview of Asset Capitalization, page 5- 1

Implementing Oracle Assets

If you plan to interface capital assets and retirement adjustment assets to Oracle
Assets, you must implement Oracle Assets before you can create capital and retirement
adjustment asset lines for your capital projects . The following information is used by
Oracle Projects to validate your asset definition:

• Corporate Book

• Category FlexField

• Location FlexField

• Automatic Asset Numbering

• Accounting FlexField

You may elect to interface costs without the category, location, depreciation expense
account or asset number defined. You will then be required to add this information after
the asset is posted to the mass additions table in Oracle Assets. However, you cannot
create asset lines for an asset until it has a corporate book assigned to it. Whether
a complete asset definition is required before interfacing the asset to Oracle Assets is
determined by the Project Type setup in Oracle Projects.

There are no additional implementation requirements in either Oracle Assets or Oracle
Projects to interface costs from Oracle Projects to Oracle Assets.

When Oracle Assets is not installed

When Oracle Assets is not installed, the capital projects forms disables the following
fields:

• Location

• Category

• Book

• Depreciation Expense Account

Interfacing Assets to Oracle Assets

Submitting Processes

For detailed information on defining and processing assets, including the interface of
assets and asset costs to Oracle Assets, refer to Defining and Processing Assets, page 5- 9 .

7-32 Oracle Project Costing User Guide

Accounting Transactions

Each asset cost line sent to Oracle Assets from Oracle Projects includes the CCID (code
combination ID) for the account number charged for the CIP costs.

Output Reports

Related Topics

Each time you run the Interface Assets process, Oracle Projects prints output reports
which allow you to track you successfully interfaced assets, as well as those assets
which failed to interface.

Sending Asset Lines to Oracle Assets, page 5-26

Mass Additions

Successfully interfaced asset cost lines from Oracle Projects are written to the Mass
Additions table. You can use the Prepare Mass Additions window to review the
interfaced assets. You can use all the normal functionality of Oracle Assets for assets
that originate in Oracle Projects. You can perform the following operations on assets
within Mass Additions:

• Split assets with more than 1 units into multiple assets.

• Add the new asset to an existing asset in Oracle Assets.

• Merge 2 or more new asset records into a single asset .

• Change the asset information defined in Oracle Projects; for example, asset

category, asset key, or asset location.

Asset records created by Oracle Projects will have one of the following queue statuses:

• POST - A new asset from Oracle Projects with all required fields populated. The

records for this asset can be posted to the FA tables.

• NEW - A new asset from Oracle Projects which needs to have required fields

manually populated before it can be posted to the FA tables.

• MERGED - The individual summarized cost lines created in Oracle Projects. These
records are merged into a single asset record in Oracle Assets. You do not make
changes to the merged records.

• COST ADJUSTMENT - New costs for a previously interfaced asset. These costs
can be either positive or negative. You can make changes to certain fields on cost
adjustments, as allowed by Oracle Assets.

When you have finished making changes to the asset records in Mass Additions, run
the Post Mass Additions process in Oracle Assets. Records that have been successfully
posted to FA tables will have a queue status of posted.

Related Topics

Sending Asset Lines to Oracle Assets, page 5-26

Integration with Other Oracle Applications

7-33

Viewing Capital Project Assets in Oracle Assets

Once capitalized assets have been interfaced from Oracle Projects to Oracle Assets, you
can locate the assets by project and task. You can also drill down to the underlying
expenditure items that support the asset costs from within Oracle Assets.

The following table lists where project-related information is located in Oracle Assets.

Menu Item

Window Name

Project-Related Information

Prepare Mass Additions

Find Mass Additions

Prepare Mass Additions

Mass Additions Summary

Prepare Mass Additions

Mass Additions (select
Open from Mass Additions
Summary window)

Find criteria include Project/
Task fields

Folder includes Project/Task
fields

Source tabbed region includes
Project/Task fields

Window includes Project
Details button to drill down to
Lines Details folder in Oracle
Projects

Prepare Mass Additions

Find Assets (select Add to
Asset from Mass Additions
Summary window)

Find by Source Line tabbed
region includes Project/Task
fields

Prepare Mass Additions

Merge Mass Additions (select
Merge from Mass Additions
Summary window)

Lines folder includes Project/
Task fields

Asset Workbench

Find Assets

Asset Workbench

View Source Lines (select
Source Lines from Assets
window)

Financial Information Inquiry

Find Assets

Financial Information Inquiry View Source Lines (select
Source Lines from Assets
window)

Find by Source Line tabbed
region includes Project/Task
fields

Cost tabbed region includes
Project/Task fields

Window includes Project
Details button to drill down to
Lines Details folder in Oracle
Projects

Find by Source Line tabbed
region includes Project/Task
fields

Folder includes Project/Task
fields

Window includes Project
Details button to drill down to
Lines Details folder in Oracle
Projects

Adjusting Assets

You can make changes in Oracle Assets to the asset information and cost amounts for
assets interfaced from Oracle Projects. However, any changes made in Oracle Assets
will not be reflected in Oracle Projects.

7-34 Oracle Project Costing User Guide

You cannot change the Project or Task information associated with assets interfaced
from Oracle Projects.

Cost Adjustments

You can adjust an asset’s cost after you have interfaced the asset to Oracle Assets. For
example, expense reports or supplier invoices may be processed after you have placed
the asset in service which are part of the asset’s costs. You process these costs the same as
you normally do. Generate new asset lines for the costs by running the Generate Asset
Lines process in Oracle Projects. These new asset lines will be interfaced to Oracle
Assets as cost adjustments.

Related Topics

Adjusting Assets After Interface, page 5-33

Integrating with Oracle Project Manufacturing

Oracle Project Manufacturing is a solution for companies that manufacture products
using projects or contracts. Oracle Project Manufacturing combines three major
applications:

• Oracle Projects, which provides the project costing, project billing, and project

budgeting functions.

• Oracle Manufacturing

• Third-party project planning and scheduling systems (project management systems)

When used as a part of the Project Manufacturing functionality, Oracle Projects acts as a
cost repository for manufacturing-related activities from other products in the Project
Manufacturing suite.

The incorporation of Oracle Projects in the Project Manufacturing suite allows you to:

• Set up the WBS for a manufacturing project in Oracle Projects. All manufacturing
costs are then tracked by project and task, and are imported to Oracle Projects
using the Transaction Import process.

• Track projects and tasks defined in Oracle Projects throughout various

manufacturing applications.

• Charge project costs from inventory and work in process to a project and task.

• Include project costs from manufacturing and distribution in your budget to actual

cost analysis in Oracle Projects.

Related Topics

Importing Project Manufacturing Costs, page 7-35

Implementing Oracle Project Manufacturing, Oracle Projects Implementation Guide

Importing Project Manufacturing Costs

When costs are incurred in Oracle Manufacturing that are related to a project, the Cost
Collector process in Oracle Cost Management passes those costs to Oracle Projects. The
Cost Collector finds all costed transactions in Manufacturing that have a project reference
and passes the referenced transaction costs to the correct project, task, and expenditure

Integration with Other Oracle Applications

7-35

type in Oracle Projects. Oracle Projects imports the costs using the Transaction Import
process.

Tip: If you integrate with Oracle Manufacturing, use function security
to prevent users from entering pre-approved batch items with an
expenditure type class of Inventory or Work in Process.

Adjusting Project Manufacturing Transactions

Transactions imported into Oracle Projects from Oracle Project Manufacturing with
transaction source Inventory Misc. can be adjusted in Oracle Projects. All other
transactions must be adjusted in Oracle Project Manufacturing.

Related Topics

Transaction Import, Oracle Projects Fundamentals

Transaction Import, Oracle Projects APIs, Client Extensions, and Open Interfaces Reference

Loading Project Manufacturing Costs, Oracle Projects APIs, Client Extensions, and Open
Interfaces Reference

Integrating with Oracle Inventory

Oracle Projects fully integrates with Oracle Inventory to allow you to enter inventory
transactions in Oracle Inventory and transfer them to Oracle Projects. You can order and
receive items into inventory before assigning them to a project. You can then assign the
items to a project as they are taken out of or received into Oracle Inventory.

When you enter project-related transactions in Oracle Inventory, you enter the project
information on the source transaction. Oracle Inventory and Oracle Projects carry the
project information through from the Issue To or Receipt From transaction in Oracle
Inventory to the project expenditure in Oracle Projects.

For more detailed information about project-related transactions in Oracle Inventory, see
the Oracle Inventory User’s Guide.

Tip: If you integrate with Oracle Inventory, use function security
to prevent users from entering pre-approved batch items with an
expenditure type class of Inventory or Work in Process.

The following illustration shows the flow of project-related inventory transactions
in a non-manufacturing environment.

7-36 Oracle Project Costing User Guide

Integration with Oracle Inventory

You enter issues and receipts into Oracle Inventory. After you run the Cost Processor
in Inventory, these become costed transactions. Next, run the Cost Collector in
Inventory. The transactions are now eligible for transfer to the Oracle Projects Transaction
Import interface table. Use Transaction Import to create expenditures in Oracle
Projects. If necessary, correct transactions and interface them again to the interface table.

The transactions are imported into to Oracle Projects as accounted and costed. The cost
distribution cannot be modified in Oracle Projects.

For information about transferring transactions from Oracle Inventory to Oracle General
Ledger, please refer to the Oracle Inventory User’s Guide.

Related Topics

Implementing Oracle Inventory for Projects Integration, Oracle Projects Implementation
Guide

Entering Project-Related Transactions in Oracle Inventory

You enter project-related transactions using the Miscellaneous Transactions window in
Oracle Inventory. You enter the following project-related information:

• Inventory Organization

• Expenditure Item Date as the Transaction Date

• Project

• Task

• Expenditure Type (optional)

To understand whether you need to enter the expenditure type, see: Oracle
Inventory Profile Options, Oracle Inventory User’s Guide.

Integration with Other Oracle Applications

7-37

• Organization

Related Topics

Overview of Expenditures, page 2- 1

Performing Miscellaneous Transactions, Oracle Inventory User’s Guide

Transaction Types, Oracle Inventory User’s Guide

Collecting Inventory Costs

After entering project-related inventory transactions in Oracle Inventory, the next step in
moving the transactions to Oracle Projects is to run the Cost Collector in Inventory. The
Cost Collector is a batch job that you run using Standard Report Submission. After you
run the Cost Collector, transactions are eligible for import from Oracle Inventory to
Oracle Projects. The total Inventory Cost becomes the Raw Cost in Oracle Projects.

For information on collecting inventory costs, see: Cost Collector, Oracle Inventory
User’s Guide.

Transferring Inventory Costs to Oracle Projects

Oracle Inventory transfers expenditures to Oracle Projects using the Project Cost
Transfers window.

• Organization

• Number of Days to Leave Costs Uncollected

The Project Cost Transfers window submits a batch job that transfers the amount and
quantities of the inventory transactions to the Oracle Projects Transaction Import
Interface table.

Importing Inventory Transactions

To import inventory transactions, you submit the PRC: Transaction Import process. The
transactions are imported as costed and accounted transactions with the expenditure
type class and the transaction source that were defined during implementation.

Related Topics

Transaction Import, Oracle Projects Fundamentals

Transaction Import, Oracle Projects APIs, Client Extensions, and Open Interfaces Reference

Reviewing Imported Inventory Transactions

If transactions are rejected during the Transaction Import process, you can review and
correct them using the Review Transactions window. After you correct transactions, you
resubmit the Transaction Import process.

Related Topics

Transaction Import, Oracle Projects Fundamentals

Transaction Import, Oracle Projects APIs, Client Extensions, and Open Interfaces Reference

7-38 Oracle Project Costing User Guide

Viewing Rejected Transactions, Oracle Projects APIs, Client Extensions, and Open Interfaces
Reference

Adjusting Inventory Transactions

You cannot adjust expenditure items in Oracle Projects that you have imported from
Oracle Inventory. The transaction source does not allow adjustments.

Integration with Other Oracle Applications

7-39

A
account generator

Oracle Payables, 7-24
Oracle Purchasing, 7-24

accounting for burden costs, 3-15

burden cost component, by, 3-21
burden cost component, setup, 3-22
no accounting impact, when, 3-25
overview, 3-20
schedule revisions, 3-25
total burdened cost, by, 3-23
total burdened cost, setup, 3-24

accounting lines
viewing, 2-40

drill down from General Ledger, 2-40

accounting transactions

capital project costs, 5- 7
adjusting expenditures, 2-44

mass, 2-50
restrictions, 2-48

adjusting supplier invoices, 2-62

in Oracle Payables, 2-63
in Oracle Projects, 2-63

adjustments

asset lines, 5-32

after interface to Oracle Assets, 5-33

assets, 7-34
burden transactions, 2-53
capital project costs, 5-34
cross charge transactions, 6-32
expenditure items, 2-44

approved item attributes, 2-45
billable status change, 2-45
billing hold, set and release, 2-46
burden cost recalculation, 2-46
burden transactions, 2-53
capitalizable status change, 2-46
comment change, 2-47
cost and revenue recalculation, 2-47
currency attributes change, 2-48
marking, 2-55
mass, 2-50
multi-currency transactions, 2-52
raw cost recalculation, 2-46
related transactions, 2-54
restrictions, 2-48

Index

revenue recalculation, 2-47
split item, 2-47
splitting, 2-51
transfer item, 2-47
transfers, 2-51
types of, 2-45
viewing, 2-38
work type change, 2-47

expense reports, 7-13

created in Oracle Internet Expenses, 7-14
created in Oracle Projects, 7-14
interfacing to other products, 2-60
invoices, 2-62
marking expenditure items, 2-55
multi-currency transactions, 2-52
processing, 2-57

reviewing results of, 2-59

purchase orders, 7-28
receipt accruals

restrictions, 7-30

related transactions, 2-54
reporting

audit, 2-44
requisitions, 7-28
restrictions, 2-44
reviewing, 2-59
cost, 2-59
invoice, 2-61
revenue, 2-60

supplier invoices, 7-28

in Oracle Payables, 7-28
in Oracle Projects, 7-30
restrictions, 7-30

advances, 7-13
allocating costs, 4- 4
Allocation Rule window, 4- 3
allocations

and burdening, 4- 2
and cross charge, 4- 3
AutoAllocations, 4-11
creating, 4- 2 , 4- 4
incremental and full, 4-10
missing amounts, 4-11
overview, 4- 1
previous amounts, 4-11
processing, 4- 4

Index-1

creating runs, 4- 5
missing amounts, 4-11
precedence, 4- 4
previous amounts, 4-11
releasing runs, 4- 6
reversing, 4-10
run status, 4- 4
troubleshooting, 4- 9
viewing results, 4- 5
viewing runs, 4- 6

releasing, 4- 6
reversing, 4-10
rules, 4- 3

defining, 4- 3
run status, 4- 4
runs

creating, 4- 5
releasing, 4- 6
reversing, 4-10
troubleshooting, 4- 9
viewing, 4- 6

transactions

creating, 4- 4
viewing, 4- 9

viewing, 4- 6

transactions, 4- 9

asset lines

adjusting, 5-32
assigning

unassigned lines, 5-32
changing assignments, 5-33
generating, 5-21, 5-22
reversing capitalized, 5-34
reviewing, 5-32
sending to Oracle Assets, 5-26
splitting, 5-33

assets

abandoning, 5-36
accounting, 5- 6
adjusting

after interface to Oracle Assets, 5-33

adjustments, 7-34
allocating costs, 5-25
asset lines

adjusting, 5-32
changing assignments, 5-33
generating, 5-21, 5-22
reviewing, 5-32
splitting, 5-33
unassigned, 5-32

Assets window

attributes, 5-14

assigning

to grouping levels, 5-28

assignments

example, 5-30

attributes, 5-14
capital events, 5-20

Index-2

capital projects

accounting for, 5- 6

capitalization, 5- 1
category, 5-15
copying, 5-13
creating, 5- 5 , 5- 9

capital assets, 5-10
retirement adjustment assets, 5-10

creating asset lines, 5-19
defining and processing, 5- 9 , 5-13

allocating costs, 5-25
attributes, 5-14
capital assets, 5-10
capital project flow, 5-11
creating asset lines, 5-19
creating assets, 5- 9
creating capital events, 5-20
generating asset lines, 5-21, 5-22
interface to Oracle Assets, 5-26
placing in service, 5-18
retirement adjustment assets, 5-10
specifying a retirement date, 5-18

description, 5-14
grouping options, 5-27

grouping level types, 5-27
grouping levels, 5-27

integration with Oracle Assets, 7-31
interface to Oracle Assets, 5-26, 7-32
key, 5-15
mass additions, 7-33
name, 5-14
number, 5-14
overview, 5- 1
placing in service, 5-18
reversing

capitalization, 5-35, 5-35
recapitalization, 5-36

reversing capitalization, 5-34
specifying a retirement date, 5-18
viewing in Oracle Assets, 7-34

assigning

asset lines

changing, 5-33
unassigned, 5-32

assets, 5-28
burden multipliers, 3-11
burden schedules, 3-13

audit reporting

expenditure adjustments, 2-44

AutoAccounting

cost accruals, 2-13
labor costs

overtime, 1-11
straight time, 1- 9

AutoAllocations, 4-11
creating sets, 4-11

prerequisites, 4-13

profile option, 4-13

submitting sets, 4-13

troubleshooting, 4-14

viewing

set status, 4-15

B
billable controls, 2-31
billing

burden schedules, 3- 9
burdening

transactions, 3-30
intercompany, 6-21

approving and releasing invoices, 6-28
determining accounts, 6-22
generating invoices, 6-26
interface tax lines, 6-31
interface to Payables, 6-30
interface to Receivables, 6-28
processing flow, 6-15
processing methods, 6- 8
borrowed and lent accounting

adjustments, 6-36
processing, 6-18

determining accounts, 6-18
flow, 6-14
generating transactions, 6-19
methods, 6- 8
budgetary controls
funds check

in Oracle Payables, 7-23
in Oracle Purchasing, 7-23
burden calculation process, 3- 2
burden schedules
assigning, 3-13

fixed dates, 3-13
project level, 3-13
task level, 3-13

changing, 3-14
default

changing, 3-14
defining, 3-13
overriding, 3-13, 3-14

determining which to use, 3-15
multipliers

assigning, 3-11
hierarchy, 3-11
overriding, 3-14, 3-14
project types, 3-13
types, 3-10
using, 3- 9
versions

defining, 3-10

burden structures

components, 3- 7
using, 3- 6

burden transactions
adjusting, 2-53

expenditure item date, 3-18

burdening

accounting for

burden cost component, by, 3-21
burden cost component, setup, 3-22
no accounting impact, when, 3-25
overview, 3-20
schedule revisions, 3-25
total burdened cost, by, 3-23
total burdened cost, setup, 3-24

accounting for costs, 3-15
accounting transactions
cost reporting, 3-35

and allocations, 4- 2
billing transactions, 3-30
building costs, 3- 4
example, 3- 4
schedules, 3- 9
schedules, assigning, 3-13
schedules, changing, 3-14
schedules, overriding, 3-14
structures, 3- 6

burden transactions, troubleshooting, 3-25
calculating costs, 1- 6 , 3- 4
calculation, 3- 4
costs

accounting for by component, 3-21
accounting for no impact, 3-25
accounting for schedule revisions, 3-25
accounting for total burdened cost, 3-23
accounting for, overview, 3-20
basis for, 3-36
building, 3- 4
reporting, 3-29, 3-31
schedule revisions, 3-25
storing, accounting, and viewing, 3-15

expenditure items

costs, storing, 3-15, 3-17, 3-18

labor costs, 1- 9
multipliers

algorithm, 3-33
assigning, 3-11

overview, 3- 1
process, 3- 2

process, 3- 2
reporting, 3-31, 3-43

custom reports, in, 3-29
general ledger, 3-31
middle management, 3-40
project management, 3-41
to GL, 3-36
upper management, 3-31

revenue transactions, 3-30
schedule revisions

processing transactions, 3-25

schedules

assigning, 3-13, 3-13
changing, 3-14

Index-3

default, changing, 3-14
determining which to use, 3-15
fixed dates, assigning, 3-13
multipliers, assigning, 3-11
multipliers, hierarchy, 3-11
overriding, 3-13, 3-14, 3-14
types, 3-10
using, 3- 9
versions, defining, 3-10

storing costs, 3-15

same expenditure item, 3-15
same project, 3-17
separate expenditure item, 3-17
separate project, 3-18
storage method, choosing, 3-19
storage method, setting up, 3-19

structures

components, 3- 7
using, 3- 6
transactions

billing, 3-30
burden cost components, 3-21
revenue, 3-30
schedule revisions, 3-25
total burdened cost, 3-23

using, 3- 4
viewing costs, 3-15

C
calculating costs, 1- 5

burden, 1- 6
expense reports, usages, miscellaneous, 1- 5
labor, 1- 5
supplier invoices, 1- 6

capital events, 5-20
capital information options
capitalized interest, 5-39

capital projects

abandoning assets, 5-36
accounting for costs, 5- 7
adjusting costs, 5-34
allocating asset costs, 5-25
asset grouping options, 5-27
grouping level types, 5-27
grouping levels, 5-27

asset lines

adjusting, 5-32
assigning, 5-32
changing assignments, 5-33
generating, 5-21, 5-22
reviewing, 5-32
sending to Oracle Assets, 5-26
splitting, 5-33

assets

accounting for, 5- 6

assigning assets

to grouping levels, 5-28

Index-4

capital events, 5-20
capital information options
capitalized interest, 5-39

capitalized interest, 5-37

capital information options, 5-39
generating expenditure batches, 5-39
project status, 5-39
rate names, 5-38
rate schedules, 5-38
releasing, reviewing, and deleting
expenditure batches, 5-41
reviewing expenditure batches, 5-40
setting up, 5-39

charging expenditures to, 5- 5
copying assets for, 5-13
defining and processing, 5- 9
defining assets for, 5-13
expenditures

capitalized interest, 5-39

integration, 5- 2
invoices, 5- 4
overview, 5- 1
placing assets in service, 5- 5 , 5-18
processing flow, 5- 2
purchase orders for, 5- 4
retirement costs, 5- 6
reversing capitalized assets, 5-34
specifying a retirement date, 5-18
supplier invoices, 5- 4
capitalizable controls, 2-31
capitalization

for capital project WBS levels, 5-12

capitalized interest, 5-37

capital information options, 5-39
capital projects

setting up, 5-39
expenditure batches
generating, 5-39
releasing, reversing, and deleting, 5-41
reviewing, 5-40

overview, 5-37
project status, 5-39
rate names, 5-38
rate schedules, 5-38
setting up, 5-39

changing burden schedules, 3-14
charge controls, 2-24
project status, 2-24
start and completion dates, 2-24
task chargeable status, 2-24
transaction controls, 2-24

chargeable controls, 2-29
commitments

from Oracle Payables, 7-24
from Oracle Purchasing, 7-24
reporting, 7-24

example, 7-25
control counts, 2-21

control totals, 2-21
copying

expenditure batches, 2-20
timecard batches, 2-20

correcting expenditure batches, 2-23
cost accruals, 2-13

accounting rules, 2-13

costing

burden, 1- 6
burden schedules, 3- 9
calculating costs, 1- 5

burden, 1- 6
expense reports, usages, miscellaneous, 1- 5
labor, 1- 5
supplier invoices, 1- 6

expense reports, usages, miscellaneous, 1- 5
labor, 1- 5
overview, 1- 1 , 1- 2
processes, 1- 3
supplier invoices, 1- 6

costing processes, 1- 3
costs

burdening, 3- 1
calculating, 1- 5
burden, 1- 6
expense reports, usages, miscellaneous, 1- 5
labor, 1- 5
supplier invoices, 1- 6

distributing

expense report, 7- 5
labor, 1- 6

labor

distributing, 1- 6

creating

allocation runs, 4- 5
allocations, 4- 2
AutoAllocations sets, 4-11
expenditure batches, 2-13

cross charge

adjustments, 6-32

borrowed and lent accounting, 6-36
intercompany billing accounting, 6-36
overview, 6-32
process flow, 6-35
allocations and, 4- 3
borrowed and lent accounting

adjustments, 6-36
generating transactions, 6-19
processing, 6-18
business needs, 6- 2
controls, 6- 9

inter-operating unit, 6- 9
intercompany, 6-10
intra-operating unit, 6- 9
processing, 6-10

distributions

interface to GL, 6-31

example

distinct projects by provider organization,
6- 4
overview, 6- 2
primary project with subcontracted projects,
6- 6
single project, 6- 5

intercompany billing accounting, 6-21

adjustments, 6-36
approving and releasing invoices, 6-28
determining accounts, 6-22
generating invoices, 6-26
interface tax lines, 6-31
interface to Payables, 6-30
interface to Receivables, 6-28

overview, 6- 1
process flow, 6-14

borrowed and lent, 6-14
intercompany billing, 6-15

processing

borrowed and lent, 6-14, 6-18
intercompany billing, 6-15
intercompany billing accounting, 6-21
methods, 6- 8
overview, 6-14

processing controls, 6-10
client extensions, 6-12
expenditure item adjustments, 6-12
implementation options, 6-10
project and task, 6-12
provider and receiver, 6-11
transaction source, 6-12
transfer price, 6-11
processing methods, 6- 8

borrowed and lent accounting, 6- 8
intercompany billing accounting, 6- 9
no cross charge process, 6- 9

transactions

adjusting, 6-32
creating, 6-16
types of, 6- 7

transfer pricing, 6-13
types, 6- 7

cross charge processing methods and controls,
6- 8
currency fields, 2-17

expenditure items, 2-18
expenditures, 2-17

D
defining

allocation rules, 4- 3
assets, 5- 9
burden schedule
versions, 3-10

distributing labor costs, 1- 6

expenditure items
selecting, 1- 8

Index-5

overtime

overview, 1- 9
processing, 1-10

straight time, 1- 8

drill down

from General Ledger, 2-40

drill down to

Oracle Payables, 2-39

E
employees

as suppliers, 7- 3

entering

expenditure batches, 2-12
expenditure items, 2-14
expenditures, 2-14

events

capital, 5-20
reversing

capitalization, 5-35

expenditure batches

control totals and control counts, 2-21
copying, 2-20
correcting, 2-23
creating, 2-13
entering, 2-12

Microsoft Excel, 2-19

Microsoft Excel, 2-19
overview, 2-10
processing, 2-10
reversing, 2-22

automatically, 2-13

reviewing and releasing, 2-22
statuses, 2-12
submitting, 2-22

Expenditure Batches window, 2-12
expenditure inquiry, 2-38
expenditure items
accounting lines

drill down from General Ledger, 2-40
viewing, 2-40

adjusting, 5-34
adjustments, 2-44

approved item attributes, 2-45
audit reports, 2-44
billable status change, 2-45
billing hold, set and release, 2-46
burden cost recalculation, 2-46
burden transactions, 2-53
capitalizable status change, 2-46
comment change, 2-47
cost and revenue recalculation, 2-47
currency attributes change, 2-48
Expenditure Items window, 2-49
marking items, 2-55
mass, 2-50
multi-currency transactions, 2-52

Index-6

processing, 2-57
raw cost recalculation, 2-46
related transactions, 2-54
restrictions, 2-48
revenue recalculation, 2-47
reviewing results of, 2-59
split item, 2-47
splitting, 2-51
supplier invoices, 2-62
transfer item, 2-47
transfers, 2-51
types of, 2-45
work type change, 2-47

burdening

storing, accounting, viewing, 3-15

control functions, 5-12
currency fields, 2-17
dates

summary burden transactions, 3-18

entering, 2-14

currency fields, 2-17

Expenditure Items window, 2-38, 2-41, 2-42
Find Expenditure Items window, 2-41
splitting, 2-51

new transactions generated, 2-57

supplier invoices
adjusting, 2-62
transferring, 2-51
validation, 2- 2
viewing, 2-38

Expenditure Items window, 2-38, 2-42

adjusting expenditures, 2-49
reference, 2-41

expenditures

accounting lines
viewing, 2-40
adjustments, 2-44

audit reports, 2-44
burden transactions, 2-53
Expenditure Items window, 2-49
marking items, 2-55
mass, 2-50
multi-currency transactions, 2-52
processing, 2-57
related transactions, 2-54
restrictions, 2-44, 2-48
reviewing results of, 2-59
splitting, 2-51
supplier invoices, 2-62
transfers, 2-51
types of, 2-45

amounts, 2- 2
batches

control totals and control counts, 2-21
copying, 2-20
correcting, 2-23
creating, 2-13
entering, 2-12

reversing, 2-22
reviewing and releasing, 2-22
submitting, 2-22
billable controls, 2-30
burdening, 3- 1
calculating costs, 1- 5
capitalizable controls, 2-30
capitalized interest
generating, 5-39
releasing, reviewing, and deleting, 5-41
reviewing, 5-40

chargeable controls, 2-28
chargeable status

determining, 2-29

classifications, 2- 2
control totals, 2-21
controlling, 2-24
billable, 2-30
capitalizable, 2-30
chargeable, 2-28
examples, 2-31, 2-31, 2-32, 2-33
transaction control extensions, 2-25

copying, 2-20
correcting, 2-23
costing

burden, 1- 6
expense reports, usages, miscellaneous, 1- 5
labor, 1- 5
supplier invoices, 1- 6

currency fields, 2-17
distributing
labor, 1- 6
entering, 2-14

currency fields, 2-17
Microsoft Excel, 2-19

entry methods, 2- 2
expenditure items

adjustments, types of, 2-45

funds check, 2- 3
future-dated employees, 2-13
labor costs

distributing, 1- 6
overtime, 1- 9 , 1-10
straight time, 1- 8
Microsoft Excel, 2-19
overview, 2- 1 , 2-10
processing, 2-10
rejection reasons, 2- 3
reports

adjustments, 2-44

reversing, 2-22

automatically, 2-13

reviewing and releasing, 2-22
submitting, 2-22
supplier invoices
adjusting, 2-62

transaction controls, 2-24

billable, 2-30

capitalizable, 2-30
chargeable, 2-28
examples, 2-31, 2-31, 2-32, 2-33
exclusive, 2-25
extensions, 2-25
inclusive, 2-25

validation, 2- 2

funds checks, 2- 3
rejection reasons, 2- 3

View Expenditure Accounting window, 2-40
viewing, 2-38
expenditures items

drill down from General Ledger, 2-40
View Expenditure Accounting window, 2-40

Expenditures window, 2-14
expense reports, 1- 5
adjusting, 7-13

created in Oracle Internet Expenses, 7-14
created in Oracle Projects, 7-14

advances, 7-13
batch naming, 7-15
created in Oracle Internet Expenses

processing, 7-10

created in Oracle Projects

processing, 7- 4
distributing costs, 7- 5
error reports, 7- 8 , 7-12
GL date for, 7- 6
importing in Payables

from Oracle Internet Expenses, 7-11
from Oracle Projects, 7- 6

integrating with Oracle Internet Expenses

overview, 7- 2
setup, 7- 3

integrating with Oracle Payables

overview, 7- 2
setup, 7- 3

integration

Oracle Internet Expenses, 7- 1
Oracle Payables, 7- 1

interface

Oracle General Ledger, 7-10, 7-11

interface from Payables, 7-11
interface to Payables, 7- 5
liability account, 7- 6
prepayments, 7-13
purging, 7-15
reports and listings, 7- 6
streamline processes

streamline processes, 7- 9

tying back from Oracle Payables, 7- 8
viewing in Oracle Payables, 7-15

F
Find Expenditure Items window, 2-41
funds check
activation

Index-7

in Oracle Payables, 7-23
in Oracle Purchasing, 7-23

funds checks, 2- 3
future-dated employees

entering transactions, 2-13

G
GL date

expense reports, 7- 6

I
integration

capital projects, 5- 2
Oracle Assets, 5- 5 , 5-26, 7-31

adjusting assets, 7-34
implementing, 7-32
interface assets, 7-32
mass additions, 7-33
viewing assets, 7-34

Oracle Internet Expenses, 7- 1

overview, 7- 2
setup, 7- 3

Oracle Inventory, 7-36

adjusting transactions, 7-39
collecting costs, 7-38
entering project-related transactions, 7-37
importing transactions, 7-38
reviewing transactions, 7-38
transferring costs, 7-38

Oracle Payables, 5- 4

document flow, 7-17
entering default information for supplier
invoices, 7-19
entering supplier invoices, 7-19
expense reports, 7- 1
interface supplier costs, 7-20
interface supplier invoices, 7-20
matching invoices, 7-18
overview, 7- 2
posting invoices, 7-19
setup, 7- 3
supplier invoices, 7-16, 7-18
using distribution sets, 7-19
Oracle Project Manufacturing, 7-35
Oracle Purchasing, 5- 4
document flow, 7-17
entering default information, 7-18
entering purchase orders, 7-17
entering releases, 7-17
entering requisitions, 7-17
recording receipt and delivery, 7-18
requisitions and purchase orders, 7-16, 7-17
using AutoCreate, 7-17

overview, 7- 1

intercompany billing accounting

adjustments, 6-36

Index-8

processing, 6-21

approving and releasing invoices, 6-28
determining accounts, 6-22
flow, 6-15
generating invoices, 6-26
interface tax lines, 6-31
interface to Payables, 6-30
interface to Receivables, 6-28
methods, 6- 8

interface supplier costs, 7-20
interface supplier invoices, 7-20
interfaces

Oracle Assets, 5-26, 7-31
adjustments, 5-33
Oracle General Ledger

expense reports, 7-10, 7-11
Oracle Internet Expenses, 7- 1

expense reports, 7-10

Oracle Inventory, 7-36
Oracle Payables

expense reports, 7- 1 , 7- 4
supplier invoices, 7-16

Oracle Project Manufacturing, 7-35
Oracle Purchasing

requisitions and purchase orders, 7-16

invoices

capital project, 5- 4
intercompany

approving and releasing, 6-28
interface to Payables, 6-30
interface to Receivables, 6-28
interfacing tax lines, 6-31

transactions

for capital projects, 5- 4

L
labor, 1- 5
labor costs

distributing, 1- 6

overtime, 1- 9 , 1-10
straight time, 1- 8

expenditure items
selecting, 1- 8

overtime

AutoAccounting, 1-11
calculating, 1-10
cost distribution lines, 1-11
overview, 1- 9
processing, 1-10
tracking, 1-10

reports, 1-11
straight time, 1- 8

AutoAccounting, 1- 9
calculating, 1- 8
cost distribution lines, 1- 9

utilization, 1-11

M
marking expenditure items for adjustment, 2-55
mass adjustment of expenditures, 2-50
Microsoft Excel

using to enter expenditures, 2-19

miscellaneous transactions, 1- 5
multi-currency transactions

adjusting, 2-52

O
Oracle Assets

creating asset lines for, 5-19
integration, 7-31

adjusting assets, 7-34
implementing, 7-32
interface assets, 7-32
mass additions, 7-33
viewing assets, 7-34

Oracle General Ledger
burden amounts

reporting to, 3-31

Oracle Internet Expenses

integration, 7- 1
overview, 7- 2
setup, 7- 3

Oracle Inventory

integration, 7-36

adjusting transactions, 7-39
collecting costs, 7-38
entering project-related transactions, 7-37
importing transactions, 7-38
reviewing transactions, 7-38
transferring costs, 7-38

Oracle Payables

account generator, 7-24
adjustments, 7-28

supplier invoices, 7-28
advances (prepayments), 7-13
funds check activation, 7-23
importing expense reports

from Oracle Internet Expenses, 7-11
from Oracle Projects, 7- 6

integration

document flow, 7-17
entering default information for supplier
invoices, 7-19
entering supplier invoices, 7-19
expense reports, 7- 1
interface supplier costs, 7-20
interface supplier invoices, 7-20
matching invoices, 7-18
overview, 7- 2
posting invoices, 7-19
setup, 7- 3
supplier invoices, 7-16, 7-18
using distribution sets, 7-19

project information

entering, 7-20

viewing expense reports, 7-15

Oracle Project Manufacturing

importing Project Manufacturing costs, 7-35
integration, 7-35
Oracle Purchasing

account generator, 7-24
adjustments, 7-28

purchase orders, 7-28
requisitions, 7-28

funds check activation, 7-23
integration

document flow, 7-17
entering default information, 7-18
entering purchase orders, 7-17
entering releases, 7-17
entering requisitions, 7-17
recording receipt and delivery, 7-18
requisitions and purchase orders, 7-16, 7-17
using AutoCreate, 7-17

project information
entering, 7-20

overriding burden schedules, 3-14, 3-14
overviews

allocations, 4- 1
asset capitalization, 5- 1
burdening, 3- 1
capital projects, 5- 1
capitalized interest, 5-37
controlling expenditures, 2-24
costing, 1- 1 , 1- 2
cross charge, 6- 1
expenditure batches, 2-10
expenditures, 2- 1 , 2-10
integration with other applications, 7- 1
transaction controls, 2-24

P
prepayments, 7-13
processes

costing, 1- 3
Create and Distribute Burden Transactions,
3-22
Distribute Expense Report Costs, 7- 5
Distribute Labor Costs

reports, 1-11

Expense Report Import

from Oracle Internet Expenses, 7-11
from Oracle Projects, 7- 6

Interface Expense Reports from Payables, 7-11
Interface Expense Reports to Payables, 7- 5
Interface Supplier Costs, 7-20
Interface Usage and Misc. Costs to GL, 3-22
Payables Transfer to General Ledger, 7-10, 7-11
streamline

streamline processes, 7- 9

Tieback Expense Reports from Payables, 7- 8

Index-9

Tieback Usage and Miscellaneous Costs from
GL, 3-22
processing

related transactions
adjusting, 2-54

releasing

adjustments

expenditure items, 2-57
reviewing results of, 2-59

burden transactions

schedule revisions, 3-25
expenditure batches, 2-10
expense reports

created in Oracle Internet Expenses, 7-10
created in Oracle Projects, 7- 4

profile options

PA: Allow Override of PA Distributions in
AP/PO, 7- 4
PA: Allow Project Time and Expense Entry, 7- 4
PA: Expense Report Invoices Per Set, 7- 4
PA: Summarize Expense Report Lines, 7- 4
Project Expenditure Accounting window, 2-41
project options

capital information

capitalized interest, 5-39

transaction controls, 2-24

Project Revenue Accounting window, 2-41
project status

adjustment restrictions, 2-44
capitalized interest, 5-39

project templates

expenditure batch, 2-21

project types

burden schedules, 3-13

projects

capital, 5- 1
commitments, 7-24
costs

reporting, 3-31

Projects window

copying assets, 5-13
defining assets, 5-13

purchase orders, 7-17

adjustments, 7-28, 7-28
AutoCreate, 7-17
commitments, 7-24
creating for capital projects, 5- 4
default information, 7-18
entering, 7-17
project-related information, 7-20
receipt and delivery, 7-18
releases, 7-17
validating, 7-23

purging

expense reports, 7-15

R
receipt accruals
adjustments

restrictions, 7-30

Index-10

allocation runs, 4- 6
expenditure batches, 2-22

reporting burdening

custom reports, 3-29

reports

expenditure adjustments
audit reporting, 2-44

reports and listings

interfaced and rejected
expense reports, 7- 6
invoice distributions, 7-12

requisitions, 7-17

adjustments, 7-28, 7-28
commitments, 7-24
default information, 7-18
entering, 7-17
project-related information, 7-20
validating, 7-23

restrictions

receipt accrual adjustments, 7-30
supplier invoice adjustments, 7-30

revenue

burden schedules, 3- 9
burdening

transactions, 3-30

reversing

allocation runs, 4-10
assets, 5-34
cost accruals

automatically, 2-13
expenditure batches, 2-22
automatically, 2-13

Review Allocation Runs window, 4- 6
reviewing

expenditure batches, 2-22
reviewing adjustments, 2-59

cost, 2-59
invoice, 2-61
revenue, 2-60

S
schedules

burden, 3-14

assigning, 3-13

setting up

capital projects

capitalized interest, 5-39
expense report integration

Oracle Internet Expenses, 7- 3
Oracle Payables, 7- 3

splitting

asset lines, 5-33
expenditure items

new transactions generated, 2-57

splitting expenditure items, 2-51

new transactions generated, 2-57

storing burden costs, 3-15

same expenditure item, 3-15
same project, 3-17
separate expenditure item, 3-17
separate project, 3-18
storage method

choosing, 3-19
setting up, 3-19
streamline processes

streamline processes, 7- 9

submitting

AutoAllocation sets, 4-13
expenditure batches, 2-22

supplier costs
adjustments

in Oracle Payables, 7-28
in Oracle Projects, 7-30
restrictions, 7-30

interfacing, 7-20

supplier invoices, 1- 6 , 7-18
adjustments, 2-62, 7-28

in Oracle Payables, 2-63, 7-28
in Oracle Projects, 2-63, 7-30
restrictions, 7-30
commitments, 7-24
default information, 7-19
distribution sets, 7-19
entering, 7-19
interfacing, 7-20
matching, 7-18
posting, 7-19
project-related information, 7-20
validating, 7-23

suppliers

as employees, 7- 3

T
task options

transaction controls, 2-24

tasks

control functions, 5-12

taxes

interface from Payables, 6-31
non-recoverable, 7-24

tie back

expense reports, 7- 8
transaction controls, 2-24
allowable charges, 2-26
billable, 2-28, 2-30
capitalizable, 2-28, 2-30
chargeable, 2-28

determining status, 2-29

effective dates, 2-28
employee

expense reports, 2-26

scheduled work assignments, 2-27
usage and supplier transactions, 2-26

examples, 2-31, 2-31, 2-32, 2-33
exclusive, 2-25
extensions, 2-25
in projects, 5-12
inclusive, 2-25
person type, 2-27
Workplan resources only, 2-27

transaction types

cross charge, 6- 7

transactions
adjusting

burden, 2-53
multi-currency, 2-52
related, 2-54
capitalized, 5-12
cross charge

creating, 6-16
funds checks, 2- 3
unmatched negative, 2-23

transfer pricing

overview, 6-13

transferring expenditure items, 2-51
troubleshooting allocation runs, 4- 9

U
usages, 1- 5
using

burden schedules, 3- 9
burden structures, 3- 6
burdening, 3- 4

utilization

calculating and reporting, 1-11

V
View AutoAllocation Statuses window, 4-15
View Expenditure Accounting window, 2-40
viewing

accounting lines, 2-40

drill down from GL, 2-40

allocation runs, 4- 6
allocation transactions, 4- 9
AutoAllocation sets

status, 4-15
burden costs, 3-15
expenditure items, 2-38
expenditures, 2-38

W
window illustrations

Allocation Rule, 4- 3
Expenditure Batches, 2-12
Expenditure Items, 2-38
Expenditures, 2-14

Index-11

Review Allocation Runs, 4- 6
View AutoAllocation Statuses, 4-15

View Expenditure Accounting, 2-40

Index-12

Index-13



## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
