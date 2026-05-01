---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/Mpi000.doc.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# Mpi000.doc

## Source
File: `Brain/raw/.extract/BP/Mpi000.doc.md`
Size: 20,398 bytes

## Raw content
 TOC \o "1-2" I. Physical Inventory - SSG	 GOTOBUTTON _TOC410125816   PAGEREF _TOC410125816 3
A. Objectives	 GOTOBUTTON _TOC410125817   PAGEREF _TOC410125817 3
B. Critical Success Factors	 GOTOBUTTON _TOC410125818   PAGEREF _TOC410125818 3
C. Assumptions	 GOTOBUTTON _TOC410125819   PAGEREF _TOC410125819 3
D. Performance Measures	 GOTOBUTTON _TOC410125820   PAGEREF _TOC410125820 3
E. Issues	 GOTOBUTTON _TOC410125821   PAGEREF _TOC410125821 3
F. Better Practices Recommendations	 GOTOBUTTON _TOC410125822   PAGEREF _TOC410125822 4
G. Existing SAP functionality	 GOTOBUTTON _TOC410125823   PAGEREF _TOC410125823 4
II. Manage Physical Inventory Schedule	 GOTOBUTTON _TOC410125824   PAGEREF _TOC410125824 5
A. Objectives	 GOTOBUTTON _TOC410125825   PAGEREF _TOC410125825 5
B. Requirements	 GOTOBUTTON _TOC410125826   PAGEREF _TOC410125826 5
C. Performance Measures	 GOTOBUTTON _TOC410125827   PAGEREF _TOC410125827 6
D. Jobs Analysis	 GOTOBUTTON _TOC410125828   PAGEREF _TOC410125828 6
E. Reports	 GOTOBUTTON _TOC410125829   PAGEREF _TOC410125829 7
F. Forms	 GOTOBUTTON _TOC410125830   PAGEREF _TOC410125830 7
III. Initiate Physical Inventory	 GOTOBUTTON _TOC410125831   PAGEREF _TOC410125831 7
A. Objectives	 GOTOBUTTON _TOC410125832   PAGEREF _TOC410125832 7
B. Requirements	 GOTOBUTTON _TOC410125833   PAGEREF _TOC410125833 7
C. Performance Measures	 GOTOBUTTON _TOC410125834   PAGEREF _TOC410125834 8
D. Jobs Analysis	 GOTOBUTTON _TOC410125835   PAGEREF _TOC410125835 8
E. Interface Files	 GOTOBUTTON _TOC410125836   PAGEREF _TOC410125836 8
F. Reports	 GOTOBUTTON _TOC410125837   PAGEREF _TOC410125837 8
IV. Validate Physical Inventory	 GOTOBUTTON _TOC410125838   PAGEREF _TOC410125838 9
A. Objectives	 GOTOBUTTON _TOC410125839   PAGEREF _TOC410125839 9
B. Requirements	 GOTOBUTTON _TOC410125840   PAGEREF _TOC410125840 9
C. Performance Measures	 GOTOBUTTON _TOC410125841   PAGEREF _TOC410125841 9
D. Jobs Analysis	 GOTOBUTTON _TOC410125842   PAGEREF _TOC410125842 10
E. Reports	 GOTOBUTTON _TOC410125843   PAGEREF _TOC410125843 10
V. Reconcile Physical and Book Inventory	 GOTOBUTTON _TOC410125844   PAGEREF _TOC410125844 10
A. Objectives	 GOTOBUTTON _TOC410125845   PAGEREF _TOC410125845 10
B. Requirements	 GOTOBUTTON _TOC410125846   PAGEREF _TOC410125846 10
C. Performance Measures	 GOTOBUTTON _TOC410125847   PAGEREF _TOC410125847 11
D. Jobs Analysis	 GOTOBUTTON _TOC410125848   PAGEREF _TOC410125848 11
E. Reports	 GOTOBUTTON _TOC410125849   PAGEREF _TOC410125849 12
F. Forms	 GOTOBUTTON _Toc410125850   PAGEREF _Toc410125850 13

Physical Inventory - SSG
Objectives
To support sales and profit generation through the accurate reporting and update of perpetual inventories and to satisfy accounting requirements

Physical Inventory - SSG is the process in which physical inventory counts are scheduled, count-related resources and information are provided to sites and third-party inventory service companies, and physical-book inventory discrepancies are identified and resolved.
Critical Success Factors
Ability to provide accurate site inventories
Ability to manage shrinkage at the site and department level
Compliance with accounting requirements
Compliance with Inventory Service requirements
Ability to minimize the impact to customers in stores (12/23/97)
Ability to receive data transfers at the store terminal (12/26/97)
Ability to perform snapshots (freeze articles) in stores (12/26/97)
Assumptions
Sites will possess SAP terminals
SAP terminals will be equipped with printers
Sites will possess RF technology (guns and antennae) and the RF technology will interface with the SAP terminal
Clear receipt cut-off guidelines will be adopted and maintained
Performance Measures
Accuracy of physical inventory
Variance of accruals and accounts
Shrink %
Timeliness of shrink, physical inventory history, and variance reporting
Issues
What is the capacity of SAP to perform site builds and snapshots to post inventory and create adjustments? How much time is required? How much system processing is diverted? (communicated to Geoff Brim for inclusion in the stress test 12/1/97)
How will DC physical inventories be reconciled with SAP? Does EXE send the counts (as store do) with SAP creating adjustments to reconcile or does EXE send adjustments to the SAP inventory? (resolved 12/05/97: EXE will send counts to SAP)
Can SAP manage postings of delinquent sales transactions that come in the middle or just after the physical inventory process (see Reconcile Physical and Book Inventory requirements)?
SAP has the ability to freeze and block articles for physical inventories and cycle counts. Can SAP block only a particular type of transaction (sales, for instance)? Transactions that involve blocked articles are not posted until the articles have been un-blocked. Do we want to use this functionality? Resolution: Article freezes are the equivalent of the current snapshot. Articles that are blocked are blocked from ALL inventory movement types. The blocking ability has been marked as optional in the process documentation. (01/16/98)
EXE will send counts to SAP for physical inventories and adjustments to SAP for cycle counts (confirmed 12/97).
What information will appear on cycle count and recount sheets? Locations, articles? What is the format required for these sheets? (12/24/97)
Can we maintain a separate trailer location for stores? Will inventory in the trailer roll up and be counted in the store’s complete on hands? Business reason: It would be useful from an Inventory Control perspective to see that 8 of a store’s 10 Dogloos were in a trailer and not on the floor. (Resolution: Yes, inventory can be maintained in a trailer according to SAP and yes, this inventory would be included in the store’s on hands. However, this increases the amount of inventory management required by the store) (01/16/98)
Better Practices Recommendations
Rigorously scheduled individual store inventories (1 - 2 times per year).
Application of data warehousing and flexible information systems to support inventory report requirements
Implementation of new decision criteria that help stores recognize the implications of physical inventories on replenishment
Utilization of physical inventory summary and exception reporting to identify trends
Existing SAP functionality

Preparation
Schedule Store Physical Inventory
Prepare Physical Inventory Documents (can be done at any time)
Includes schedule date, site number, and storage location (default 001)
Articles concerned are blocked (this blocks all types of inventory transactions at the site. Optional)
Book Inventory balance is frozen (this is the equivalent of the snapshot. Optional, but recommended)
Create Physical Inventory Documents
Physical Inventory Intermediate Documents (IDocs) sent to store or Inventory Service

Count
Receive IDocs
Physical Inventory count
Prepare and send count data to SSG
Count data is uploaded in SAP
Counts are posted
Articles concerned are un-blocked (see #4 in the preparation stage above)
Book Inventory balance is un-frozen (see #5 in the preparation stage above)

Analysis
System then compares the results of count against book inventory balance
Create Difference List
User decides which articles displaying large variances to be recounted or not
Triggers a recount
See Count (above)

Post Inventory Adjustments and Reconciliation available in SAP
Physical Inventory History Reporting
Physical Inventory Controlling via LIS (Can be used proactively before posting)
Post-Physical Inventory Adjustments

Physical Inventory Document Examples:

Physical Inventory document 10001234
ArticleDescriptionMoving Average CostBook QuantityQuantity CountedDifference QuantityDifference Value50004790Cat Collar Green$1.49100955$7.45

Article Document 4900009876
DescriptionQuantitySiteStorage LocationMovement Type+/-50004790Cat Collar Green507540001702-(outward movement)
Accounting Document 4900007564
AccountDebitCreditStock of Dog/Cat Hardgoods$7.45Expenditure from Physical Inventory Differences$7.45Manage Physical Inventory Schedule
Objectives
To optimize physical inventory effectiveness by selecting appropriate stores for inventory and through improved scheduling
Requirements
The system must support the identification of site candidates for the physical inventory process based on site performance for use in the Physical Inventory Schedule.  Examples of decision criteria are :
Sales volume
Shrinkage
Negative inventory adjustments
Ad hoc cycle counts (shoot the hole)
Receipt corrections
Store management turnover
In addition, the envisioned scheduling application must accept availability and "black out dates" from multiple sources, including:
User-defined days for Physical Inventory scheduling, for example on Mondays and Wednesdays only
Traffic (to schedule on days with no DC deliveries)
Third-party inventory service availability
New store planning (to schedule unopened stores for future inventory)
DC Operations (for availability)
Store Operations (for availability)
IS Organization (for system processing availability)
Holidays
Weight P.I. scheduling components to establish P.I. optimal schedule
Communicate the physical inventory schedule to sites, inventory services, traffic, MIS, store operations, internal audit, and Price Waterhouse
Publish the physical inventory schedule on the network or the world wide web (www) to make it accessible company-wide (12/26/97)
Support 75+ physical inventories per month
Support multiple physical inventories per site each year
Performance Measures
Number of hours spent creating, coordinating physical inventory schedule
Number of physical inventory schedule revisions over the course of a year
Effectiveness of discretionary physical inventory (cost-benefit) (12/14/97)
Jobs Analysis
Job:  Inventory Control (Schedule Person)
Request store, DC, and inventory service availability, MIS capacity, traffic schedules, new store listings
Produce and analyze shrink history reports
Enter this data into scheduling application
Resolve scheduling conflicts using alternate availability
Distribute the final physical inventory schedule.
Reports
Retained Reports
Annual / Quarterly Physical Inventory Schedule (this report is maintained manually. The envisioned schedule would be produced in a more system-facilitated manner)
Forms
Retained Forms
Physical Inventory Availability Request Form (this form is used in the current system, but its content and format may change in the future)
Initiate Physical Inventory
Objectives
To provide sites and inventory services with the resources necessary to complete the physical inventory accurately and efficiently.
Requirements
Interface Requirements
Permit stores to enter counts using RF technology
Permit stores to enter counts by location for use during the physical inventory
SAP must be able to produce the following reports from a common pre-inventory preparation screen:
Open Cycle Count Report
Delinquent Transaction Report
Inventory Bucket Report
Open Transfer Report
Allow inventory services to import UPC master files and snapshots from the site’s SAP terminal into their PC (12/10/97)
Make the snapshot available to the site of the physical inventory before the inventory is over. Contains: SKU, Site, On hand, MAC (not used), SUM retail, Record number, Key item code (12/10/97)
Build and hold store and DC snapshots for eventual reconciliation with physical inventories
Schedule polling of sites with pending physical inventories at the beginning of the nightly batch window OR limit the length of the nightly batch window in order to produce timely snapshots (12/26/97 )
Limit transactions to EXE and stores during DC physical inventory

Topstock Precount Requirements
Scan topstock and enter quantities using an RF gun (01/19/98)
Support the following topstock counting process:
Maintain a separate topstock precount IDoc file that holds scanned UPCs and quantities by temporary location (01/19/98)
Make adjustments to the topstock precount IDoc file as inventory moves in and out of the precount locations (01/19/98)
Merge the topstock precount IDoc file with the physical inventory IDoc when the physical inventory begins (01/19/98)

Other Requirements
The site master will contain an inventory service “flag” that designates the format of the snapshot and UPC master files (12/26/97)
Performance Measures
Time required for snapshot build and download to a site
Accuracy of top stock precounts
Time required to make adjustments to top stock precounts
Jobs Analysis
Job:  Store Operations
Prepare precount count sheets
Precount and adjust topstock inventory
Produce pre-Inventory Preparation Reports
Close incomplete transactions.
Interface Files
Retained Files
UPCDUMP (UPC master list used by the Inventory Service company and in the site’s RF guns)
SKUDUMP (Site snapshot/freeze used to capture the perpetual inventory values at the time of the count. May be used by the Inventory Service company if In-Store Variance Reports cannot be produced using the store system)
Files Added
Topstock Precount File (Precount IDoc maintained at the site and merged into the physical inventory IDoc)
Reports
Retained Reports
Physical Inventory Checklist (Used to ensure that open transactions have been closed, the site’s inventory has been frozen, the site’s inventory has been unfrozen, etc.)
Reports Added
Pre-inventory Preparation Reports:
Open Cycle Count Report (Lists open cycle counts and any frozen or blocked inventory at the site)
Delinquent Transaction Report listing:
Open sales transactions / sales that could not post or were kicked out.   i.e. 'error log'
Any open transactions (not posted) that could affect inventory ownership
SAP also needs to provide the functionality to select or de-select the above listed articles and quantity from inclusion in Physical Inventory.
Inventory Bucket Report (Lists all articles in any other inventory bucket aside from Unrestricted.  The physical inventory process allows for counting only a single type of stock.  i.e. Unrestricted)
Open Transfer Report (Lists transfers and purchase orders that are past due and not posted)
Validate Physical Inventory
Objectives
To efficiently and accurately reconcile initial inventory variance and invalid SKUs in the site, leverage inventory service counting resources, and reduce dependence on inventory services for preliminary variance reporting.
Requirements
Enter counts using RF technology
Produce perpetual snapshots and send them down to sites in a timely manner. This could be accomplished in two ways:
Schedule polling of sites with pending physical inventories at the beginning of the nightly batch window
Use the regular schedule, but ensure that the batch window never exceeds the length of a physical inventory count.
Allow third party inventory service to import physical counts into the SAP terminal at the site
Produce In-Store Variance, No Count, and UPC Exception Reports if possible. If not, supply the appropriate information (count IDoc, UPC master IDoc, and snapshot IDoc) to the Inventory Service company for them to produce the reports
Allow the store director to cancel the physical inventory before posting inventory adjustments
Finish counts and post units before the store opens
Performance Measures
Time needed to complete the count validation
Inventory service resources required for count validation
Units posted before the store opens for business
Jobs Analysis
Job: Store operations
Correct miscounts at the store as identified by the inventory service’s In-Store Variance and Invalid SKU reports
Decide whether or not to cancel the physical inventory based on the results of the In-Store Variance Report
Upload the final count into SAP.
Job: IS
Freeze the inventory (take a snapshot) of every article in the site. (this may be a Store Operations task)
Reports
Retained Reports
In-Store Variance Report / No Count Report (generated by inventory service)
Invalid SKU Exceptions (generated by inventory service)
Reports
Interface Files Added
Count Upload File (IDoc from Inventory Service)
Reconcile Physical and Book Inventory
Objectives
To improve inventory performance through the timely update of book inventory based on physical inventory counts
Requirements
Allow items to be entered into SAP using RF technology
Maintain a history of inventory adjustments for the current physical inventory
Initiate recounts based on established variance parameters at the merchandise category level (12/14/97)
Initiate an ‘emergency’ replenishment cycle for the site to correct critical on hands errors immediately. (01/19/98)
Unfreeze the articles at the site and freeze only those that need to be recounted. (01/19/98)
Hold the transactions from each site’s last two physical inventories
Recognize transactions that occurred prior to the snapshot, but were not included, and create appropriate adjustments to reconcile the discrepancy.

For example, in the following table 9/10 is the first day of the physical inventory. 10 articles are missing from the book (and therefore snapshot) as a sale on 9/9 was not posted. On 9/12, the 10 articles are transferred to loss. On 9/13 the sales transaction finally posts, but we only want to keep the financial part--the units should have been reconciled on 9/12. (12/11/97)

DateActualSnapCountAdjust.Book9/109010090n/a1009/129010090-10909/1390n/an/a+10100wrong way9/1390n/ano change90right way
The following table indicates another way the book inventory could be reconciled to account for delinquent transactions. 9/10 is the first day of the physical inventory. 10 articles are missing from the book (and therefore snapshot) as a sale on 9/9 was not posted. On 9/11, the sales transaction posts, and the book inventory still has not been reconciled, so the snapshot is adjusted to the correct count instead. On 9/12, there is no need to adjust the book as it matches the count.

DateActualSnapCountAdjust.Book9/109010090n/a⎬⎬⎬⎬9/11909090n/a1009/129090n/ano change90
Performance Measures
Timeliness of corrections update
Accuracy of book to actual inventory
Jobs Analysis
Store Operations
Recount problem articles according to Inventory Control specifications using RF technology
Upload counts at the SAP terminal
Unfreeze articles that do not need to be recounted (may be IS task)
Freeze articles that need to be recounted (may be IS task)
Inventory Control
Analyze variances and issue recount requests
IS
Unfreeze articles that do not need to be recounted (may be Store Operations task)
Freeze articles that need to be recounted (may be Store Operations task)
Reports
Retained Reports
Variance Report (Difference List)
Physical units and cost
Book units and cost
Variance units and cost
Sales since last count
Date of last physical inventory
Shrink %
Shrink % / sales
Physical Inventory History Reports
Articles that represent the greatest shrink for a site or a group of sites
Ad hoc histories of article shrink and merchandise hierarchies per site manager request
Dates of physical inventories
Physical to Perpetual Reconciliation Report (by store over the last 18 months) containing:
Physical inventory dates
Beginning shrink reserve balance (balance after previous PI)
Accounts payable receiving adjustments (unit/dollar differences between Vendor Invoice and PO documentation)
Unit corrections (adjustments made to correct PI miscounts identified after the store’s perpetual inventory was updated with the physical count quantities)
Monthly shrink accrual (budgeted % of net merchandise sales since the previous PI that has been adjusted to Cost of Sales each period)
Perpetual unit variance (the cost variance from comparing the current PI to the perpetual unit inventory)
Shoot the hole write-offs (activity in the 1231 account since the store’s previous PI)
Receiving corrections adjustment (activity in the 1232 account since the store’s previous PI)
Negative on hand adjustments (activity in the 1233 account since the store’s last PI)
Prior period accounts payable adjustment (dollar adjustments in the 1234 account since the last PI)
Reports Added
Article Out of Place Exception Report
Articles that were counted, but are not listed at the site or are marked as recalls (12/12/97)
Forms
Retained Forms
Physical Inventory Unit Reconciliation Form

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
