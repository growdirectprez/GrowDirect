---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/Traffic.doc.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# Traffic.doc

## Source
File: `Brain/raw/.extract/BP/Traffic.doc.md`
Size: 4,211 bytes

## Raw content
 TOC \o "1-2" I. Traffic	 GOTOBUTTON _TOC410792727   PAGEREF _TOC410792727 2
A. Objectives	 GOTOBUTTON _TOC410792728   PAGEREF _TOC410792728 2
B. Critical Success Factors	 GOTOBUTTON _TOC410792729   PAGEREF _TOC410792729 2
C. Assumptions	 GOTOBUTTON _TOC410792730   PAGEREF _TOC410792730 2
D. Requirements	 GOTOBUTTON _TOC410792731   PAGEREF _TOC410792731 2
E. Performance Measures	 GOTOBUTTON _TOC410792732   PAGEREF _TOC410792732 3
F. Issues	 GOTOBUTTON _TOC410792733   PAGEREF _TOC410792733 3
G. Jobs Analysis	 GOTOBUTTON _TOC410792734   PAGEREF _TOC410792734 3
H. Reports	 GOTOBUTTON _TOC410792735   PAGEREF _TOC410792735 3
I. Forms	 GOTOBUTTON _TOC410792736   PAGEREF _TOC410792736 3
J. Existing SAP functionality	 GOTOBUTTON _TOC410792737   PAGEREF _TOC410792737 3
K. Addendum	 GOTOBUTTON _TOC410792738   PAGEREF _TOC410792738 3



Traffic
Objectives
Critical Success Factors
Assumptions
The traffic system used has not been confirmed, but will probably be Manugistics (01/30/98)
The traffic system will provide SAP with the following data: (01/30/98)
Method of freight allocation (weight, cube, units, value)
Freight estimate (by site)
Freight variance (estimate vs. actual) by vendor, site, and freight carrier
Vendor fill rate (order changes)
The traffic system will estimate freight and allocate freight estimates using the best method for the article mix--weight, cube, etc. (01/30/98)
The traffic system will track freight billing variances by site and vendor and produce reports on these variances (01/30/98)
The traffic system will receive vendor Advance Shipping Notifications (ASNs) from vendors (01/30/98)
Requirements
SAP must provide the following data to the traffic system: (01/30/98)
Purchase Orders
Due date
Vendor
Buyer
Receiving sites
Article cost
Article quantity
Article Master
Weight
Cube
Units of Measure
Site Master
Location
Freight will be estimated using the following method: (01/30/98)
The traffic system receives purchase order from SAP, estimates the freight, and sends to the freight estimates back to SAP
Record freight estimates (in dollars) on purchase orders by receiving site
Post product cost and freight simultaneously
Allocate freight estimates to each article's MAC at the time of goods receipt
Determine the actual freight cost allocated to each article in the shipment by the article's proportion of shipment cost and this cost will be determined by either its proportion of weight, its cube proportion, its value, or number of units. This parameter (whether freight is allocated by weight, cube, value, or unit) may be entered into SAP by an external source (traffic system) and may differ by purchase order.
Track variances between estimated freight cost and actual freight cost by vendor, article, site, user that entered freight estimate, and freight carrier in order to make informed freight estimations and decisions in the future
Freight cost will be adjusted at the purchase order level using the following method: (01/30/98)
When large freight variances are encountered and we still own the inventory, adjust the receipt cost of the original purchase order rather than accrue the variances for later allocation
Apply the variance between the freight estimate and the freight cost to the affected articles' MAC, prorated based on the original allocation method (by weight, cube, value, or unit) as communicated by the traffic system
Create a report that lists these “relandings” of actual freight
Performance Measures
Issues
Traffic must be involved in the Wholesale Diverting process when the customer asks for a preferred truck line or shipping method (UPS, for example). We need to be able to convey this default information in the customer master and override it in the sales order. We also need to be able to communicate the shipping method to the DC. How is traffic going to be involved? How does traffic schedule? (01/12/98)
Can SAP handle prepaid freight and collect freight at the same time? (01/30/98)
Is it necessary to implement a G/L account for every freight vendor? Can we break out the freight cost from purchase orders to match invoices from these vendors? (01/30/98)
Jobs Analysis
Reports
Forms
Existing SAP functionality
Addendum

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
