---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/Miv000.doc.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# Miv000.doc

## Source
File: `Brain/raw/.extract/BP/Miv000.doc.md`
Size: 12,805 bytes

## Raw content
 TOC \o "1-2" I. Inventory Valuation (Adjust MAC & Update MAC)	 GOTOBUTTON _TOC410470625   PAGEREF _TOC410470625 2
A. Objectives	 GOTOBUTTON _TOC410470626   PAGEREF _TOC410470626 2
B. Critical Success Factors	 GOTOBUTTON _TOC410470627   PAGEREF _TOC410470627 2
C. Assumptions	 GOTOBUTTON _TOC410470628   PAGEREF _TOC410470628 2
D. Requirements	 GOTOBUTTON _TOC410470629   PAGEREF _TOC410470629 2
E. Performance Measures	 GOTOBUTTON _TOC410470630   PAGEREF _TOC410470630 5
F. Issues	 GOTOBUTTON _TOC410470631   PAGEREF _TOC410470631 5
G. Jobs Analysis	 GOTOBUTTON _TOC410470632   PAGEREF _TOC410470632 6
H. Reports	 GOTOBUTTON _TOC410470633   PAGEREF _TOC410470633 6
I. Forms	 GOTOBUTTON _TOC410470634   PAGEREF _TOC410470634 7
J. Existing SAP functionality	 GOTOBUTTON _TOC410470635   PAGEREF _TOC410470635 7
K. Addendum	 GOTOBUTTON _TOC410470636   PAGEREF _TOC410470636 8

Inventory Valuation (Adjust MAC & Update MAC)
Objectives
To support correct profit reporting, pricing, and accounting based on immediate and accurate cost information
Critical Success Factors
Ability to efficiently maintain and monitor Moving Average Cost
Ability to calculate MAC consistently across transactions
Ability to fairly allocate costs across sites and articles
Assumptions
MAC is calculated by dividing the post-transaction extended inventory by the post-transaction on hand in real time. This eliminates the need to store MAC at greater than two decimal places.
MAC is currently maintained by SKU by site
On-hand adjustments will be done at MAC
Requirements
Full Cost Requirements
Maintain a “full cost” field for internal decision-making in addition to the standard financial MAC. Maintain the following components in the full cost: (01/07/98)
Expected vendor rebates
Expected vendor allowances
Cost of writing a Purchase Order
Cost of paying an invoice
Cost of carrying inventory
Cost of selected movements
Cost of arranging freight and optimization into the DC
DC costs, including receiving, handling/put away, picking, and packing/loading
Cost of arranging freight from the DC to the store
Freight cost from DC to Store
Store costs, including receiving, handling/put away, breakage, shrink, and other special costs, such as assembly
Allow users to pull cost components out of the full cost for analysis

Other Requirements
Use subsequent settlement based on sales to value merchandise sold during promotions.
Track tariff and duty fees to identify landing cost factor
Reverse transactions at the original transaction MAC--not necessarily the current MAC. (01/08/98)
Automatically notify inventory mangers, pricing analysts, and inventory control of large MAC changes (by pre-defined parameters) in % and $ amounts by vendor at the article-site level
Automatically notify pricing analysts of recommended retail and selling prices depending on the latest MAC fluctuation.
Calculate and display MAC consistently:
Minimum of three decimals for calculation (resolved: see existing SAP functionality)
Minimum of two decimals for display
Rounding using 4/5 rule
Track the cost and sales of promotional articles vs. regular articles in order to correctly value inventory before, after, and during promotions

Update MAC Requirements
The following transactions and events trigger an automatic MAC adjustment:
Freight Estimation :
Record freight estimates (in dollars) on purchase orders by receiving site
Allocate freight estimates to each article's MAC at the time of goods receipt
Determine the actual freight cost allocated to each article in the shipment by the article's proportion of shipment cost and this cost will be determined by either its proportion of weight, its cube proportion, its value, or number of units. This parameter (whether freight is allocated by weight, cube, value, or unit) may be entered into SAP by an external source and may differ by purchase order.
Track variances between estimated freight cost and actual freight cost by vendor, article, site, user that entered freight estimate, and freight carrier in order to make informed freight estimations and decisions in the future
Freight Adjustments :
When large freight variances are encountered and we still own the inventory, adjust the receipt cost of the original purchase order rather than accrue the variances for later allocation
Apply the variance between the freight estimate and the freight cost to the affected articles' MAC, prorated based on the original allocation method (by weight, cube, value, or unit)
Receipts (PO cost, discounts, warehouse allowance, and freight allowance)
Expense transfers in which on hands is increased and the transaction cost is not equal to MAC
Inventory movement from style to style (SKU to SKU) updates MAC of the receiving SKU in all stores
Site to site transfers to hit the receiving site’s MAC
Broker fees are adjusted into the MAC (Canadian stores)
If a store’s on hand is negative before a transaction is posted and positive after the transaction is posted, replace the MAC with the transaction cost
The following transactions and events do not trigger an automatic MAC adjustment:
Sales
Customer returns
Physical inventory adjustments
Expense transfers in which on hands decrease
If the post-transaction on hands is zero or negative
If the post-transaction MAC would be negative (except in the case of an RTV)

Adjust MAC Requirements
Manually adjust MAC without a transaction / document reference:
Allocate manual adjustments based on % of units on hand
Maintain an internal cross reference # for all manual adjustments
Support multiple levels of adjustment:
one article at one site
one article at multiple sites
multiple articles at one site
multiple articles at multiple sites
Manual adjustments include:
Periodic MAC adjustments: Small freight variances (backhaul), small PO variances, import fees, and other COGS are adjusted into MAC and allocated by departments and stores by %
MAC adjusted incorrectly due to error in automatic MAC transaction (PO or transfer written incorrectly, for instance)
Parameters for manual adjustments include:
reason code
company, regions, or stores
departments and/or store attribute codes
articles
article characteristics

Reporting Requirements
Issue MAC Fluctuation Exception Reports based on exceptional MAC changes (see Reports section for more details)
Maintain MAC transaction history for at least six months. (See Reports section for more details)
Produce a Negative Inventory Journal report that: (01/29/98)
Must be run on demand
Shows all articles with negative on hands
Shows all articles with negative MAC
Limit by site, date, and merchandise category
Performance Measures
Accuracy / consistent automatic MAC updates
Number of ad-hoc MAC adjustments due to exceptions
Consistency of MAC
Issues
MAC is currently adjusted at the article-site level. Should MAC be adjusted company-wide by article in order to reduce MAC fluctuation among sites and over time? (Resolved: article-site MAC computation will remain) (01/08/98)
How can rebates and allowance be adjusted into activity based costs for comparison of vendors and products? If we were to apply rebates to the standard financial MAC as they were received, investors would be unpleasantly surprised at the end of the year when there was no profit “bump” (12/15/97)
How many different activity based costs are available in SAP? How flexible are they in terms of what they are loaded with? Can we use some in some reports and others in other reports (01/12/98)
How can we track the cost and sales of promotional articles vs. regular articles in order to correctly value inventory before, after, and during promotions? Can we use SAP’s split valuation? Can we use subsequent settlement based on sales? (12/15/97)
What is the feasibility of applying MAC changes to past sales? From an SAP standpoint? From a business standpoint? (Resolution: SAP can do this. From an accounting standpoint, this feature will not be implemented. However, exception reports may be produced for internal use that show the actual MAC at the time of sale) (01/08/98)
What is the correct method to allocate freight--should all freight estimation be done as a percentage of PO instead of a fixed cost? Is it a better business practice to apply freight costs to MAC immediately or accrue freight charges and distribute them across MAC at intervals? (12/15/97). Resolution: See the Update MAC Requirements section.
Currently, we can maintain MAC manually in order to correct mishaps and offer special promotions. SAP does not permit such loose manipulation of MAC. Is this okay? Resolution: it is a gap. SAP allows manual adjustment of MAC for a single article-site (12/29/97)
Can we break freight bills down by vendor? Is the Traffic department responsible for doing this and able to do this? (12/29/97)
Subsequent settlement based on purchases is standard in SAP. However, subsequent settlement based on sales is not.  This functionality would be invaluable as a tool for creating a receivable prior to a promotion and charging the vendor after the promotion for the number of promotional articles sold. This has been entered as a gap in SAP and a cross-functional issue for Event Management and Order Management. (01/12/98)
Jobs Analysis
Job: Inventory Control
Monitor MAC fluctuations, MAC history, and manual MAC adjustments
Make changes in MAC to correct order and freight discrepancies
Make temporary MAC changes for vendor buy one get one free promotions (current process)
Job: Pricing
Adjust retail and selling prices according to changes in MAC
Monitor MAC fluctuations, MAC history, and manual MAC adjustments
Reports
Retained Reports
MAC Transaction History (at least six months)
SKU
Site number
Transaction type (transfer, freight landing, receipt, RTV)
Transaction document reference, if applicable (PO#, Transfer control #)
Transaction description
Sending site number, if applicable
Date of transaction posting
Date of transaction
Transaction quantity
Transaction cost
MAC prior to transaction
MAC after transaction
% Change in MAC
On hand prior to transaction
On hand after transaction
Negative Inventory Journal (by site, date, and merchandise category)
Article
Site
On hand
On order
MAC
Transfer on order
Transfer in transit
Last sale date
Last receipt date
Last transfer date
Next receipt due date
Reports Added
Full Cost Component Analysis Report (shows the % and $ each cost component makes up of the total cost--freight, labor, product cost)
Full Cost Component Trend Report (shows the historical % of total a cost component makes up of the total ABC)
Actual vs. Estimated Freight Landings (by vendor, article, site, user that entered freight estimate, and freight carrier)
Excessive MAC Fluctuation Report (to Inventory Control and Inventory Manager)
by $
by %
by vendor
at the article-site level
Recommended Pricing Report (to pricing)
Store’s Daily Sales vs. COGS Report (to pricing)
Store’s COGS Greater Than Retail Price Exception Report (to pricing)
Manual MAC Adjustment Audit Report (Lists all manual MAC adjustment transactions for auditing) (01/08/98)
MAC Component History Report (Shows the four components of MAC and the proportion of total MAC they make up over time for an article: invoice cost, freight, vendor discount, warehouse discount)
Forms
Retained Forms
Manual MAC Adjustment Form (system form allows the entry of manual MAC adjustments)
Existing SAP functionality

MAC Computation
MAC is computed on a per transaction basis with the most recent post transaction extended inventory and on hands. In other words, there is not a “MAC field” where the most recent MAC is stored.

So, the three decimals computation gap is resolved.

MAC Adjustment
SAP allows manual MAC adjustments at the article-site level without reference to a previous document. However, there is no mass maintenance functionality for MAC. To adjust the MAC of an article in every site in the company, a user would need to key in the new MAC for every site.

The MAC of an article can be adjusted at a DC. This is a potential workaround as it would carry over to the stores replenished by that DC, but would not hit the MAC at those stores until they received DC product.
Addendum

PETsMART Promotional Cost Handling (current process)
Buy one article get another free promotion. Currently, the MAC of the free article is set to $0 for the promotion date range. After the promotion, the MAC reverts back to the pre-promotion level. Charge the vendor the difference between the original inventory and the new inventory.
Vendor offers $x for each article sold as a promotion. Reduce MAC by $x over the promotion date range. After the promotion, the MAC reverts back to the pre-promotion level. Charge the vendor the difference between the original inventory and the new inventory.


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
