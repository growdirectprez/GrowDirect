---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/Mrv000.doc.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# Mrv000.doc

## Source
File: `Brain/raw/.extract/BP/Mrv000.doc.md`
Size: 16,353 bytes

## Raw content
 TOC \o "1-2" I. Product Removal Processing (Initiate Product Removal)	 GOTOBUTTON _TOC410448532   PAGEREF _TOC410448532 2
A. Objectives	 GOTOBUTTON _TOC410448533   PAGEREF _TOC410448533 2
B. Critical Success Factors	 GOTOBUTTON _TOC410448534   PAGEREF _TOC410448534 2
C. Assumptions	 GOTOBUTTON _TOC410448535   PAGEREF _TOC410448535 2
D. Requirements	 GOTOBUTTON _TOC410448536   PAGEREF _TOC410448536 2
E. Performance Measures	 GOTOBUTTON _TOC410448537   PAGEREF _TOC410448537 7
F. Issues	 GOTOBUTTON _TOC410448538   PAGEREF _TOC410448538 7
G. Jobs Analysis	 GOTOBUTTON _TOC410448539   PAGEREF _TOC410448539 8
H. Better Practices Recommendations	 GOTOBUTTON _TOC410448540   PAGEREF _TOC410448540 8
I. Reports	 GOTOBUTTON _TOC410448541   PAGEREF _TOC410448541 9
J. Forms	 GOTOBUTTON _TOC410448542   PAGEREF _TOC410448542 10


Product Removal Processing (Initiate Product Removal)
Objectives
To ensure customer satisfaction and safety, improve profit and turnover, enhance vendor relationships, and refine merchandise presentation through timely, efficient, and accurate product removals

Product Removal Processing involves the execution and tracking of damaged, returned, recalled, discontinued, mis-packaged, and improperly coded merchandise that is returned to a vendor, transferred to a store loss, or adjusted from an allowance account
Critical Success Factors
Ability to effectively manage product removals from sites (stores and DCs)
Ability to maintain vendor compliance with established product removal guidelines
Ability to track the frequency and type of article removals from sites (01/19/98)
Ability to provide information in order to evaluate the cost / benefit of returns
Assumptions
SAP client PCs will be housed in sites
SAP will post shortage transactions to P&L in real time (12/14/97)
If DC consolidation is used, the store transfers to DC and the DC produces return documents (12/14/97)
If third-party consolidation is used, the store produces return documentation (ownership transfer) (12/14/97)
DCs own the process of consolidation, the determination of EXE requirements for consolidation, and the determination of the disposition of damages / shortages incurred during consolidation (12/22/97)
Handling fees or additional charges may be added to the removal transaction and allocated to a specific G/L account based on reason code default (profit, for example) (12/14/97)
The term product removal refers generally to an RTV, a defective allowance adjustment, or a transfer to loss
Requirements
Article Requirements
Maintain the following flags / fields in the article master:
Hazardous Recall flag - Signifies that the article is not to be sold under any circumstances.



Removal Screen Requirements
Maintain a single product removal screen on the SAP Client PC that allows store associates to enter the article, quantity (including “all”), and reason code for the removal.

Maintain the following (user-defined) reason codes for use on the Product Removal Screen:
Customer Return - Damaged
Customer Return - Dissatisfied
Customer Return - Harmed Pet
Customer Return - Sick / Dead
DC damage
MXC damage
Store damage
Vendor damage
Known theft
Livestock DOA
Livestock death after delivery
Outdated / Buggy
Mis-packaged
Discontinued
Hazardous Recall
Recall

When the removal is posted, the product removal screen should issue a disposition message and a removal transaction depending on the article, vendor, site, reason code, and date. The following dispositions are required:
Not Allowed
Transfer to Scrap (Destroy / donate)
RTV Direct to Vendor (Sales Order to Vendor)
RTV through DC (Stock Transport to DC)
RTV through Consolidator (Sales Order to Consolidator)
Defective Allowance (Markdown)
Defective Allowance (Destroy / donate)
Others to be determined

If further handling is required after the removal is posted, the SAP Client PC should also print the return document to attach to the product. This tag must contain the article, the reason code, the date, and a message regarding the disposition.

The dispositions allowed for article, vendor, site, reason code, and date range should be set up by the central merchandising organization when vendors and articles are created. Each disposition should be tied to:
One or more transactions to initiate automatically (a Sales Order to the vendor, for example)
A price (article’s MAC, a user-defined price, or any of these with a handling charge) at which to execute the transactions
One or more G/L accounts to credit / debit
A message to inform the store associate of further instructions (“destroy the product”, for example)

The following transactions should be carried out automatically depending on the removal disposition issued:
RTV Direct:
Create a Standard Order with the article, customer (vendor), and quantity fields populated
Allow the user to enter a price, use the article’s MAC, or use the article’s MAC plus a handling charge
Set the delivery date a user-specified number of days in the future (to be determined)
When the order is posted, issue an email or EDI message to the vendor listing the articles and quantities being returned
Print this list at the SAP client PC for the associate to attach to the product
When the call tags are received from the vendor, contact the vendor for an authorization number and write this on the tags. Write the lot number (date code) on the tags if the vendor requires
Post the delivery order, printing the removal reference number on the vendor chargeback, and ship the product
If the call tags are not received by the time the delivery order is created, the delivery will be posted and the product will be destroyed.
RTV through Consolidator
Create a Standard Order with the article, customer (consolidator), and quantity fields populated
Allow the user to enter a price, use the article’s MAC, or use the article’s MAC plus a handling charge
Set the delivery date to the date negotiated with traffic
Post the order
Post the delivery order according to instructions from traffic
RTV through DC
Issue a Stock Transfer to the DC (see the Transfer process)
Ensure that a reason code is entered and printed on the shipping documents so the DC personnel know what to do with the product--particularly if a separate location is used for consolidation
Defective Allowance (Markdown)
The system moves the article out of restricted inventory and into scrap.
The system prints a sticker (multiple size stickers must be available for selection) that contains a UPC corresponding to a value-only article and the sticker is attached to the product
The system generates the appropriate financial transactions for vendor allowance tracking, printing the removal reference number on the vendor chargeback
Defective Allowance (Destroy / Donate)
The system moves the article out of restricted inventory and into scrap
The system generates the appropriate financial transactions for vendor allowance tracking, printing the removal reference number on the vendor chargeback

Vendor Requirements
Maintain product removal history within the vendor scorecard (also Vendor Management req.):
Number of removals due to defective merchandise
$ (allowance, RTV chargeback)
% of sales over a period of time
Reason codes used for removals of the vendor’s merchandise

Maintain the following flags / fields in the vendor master:
Authorization Code Required - a flag that lets the store associate know that an authorization code must be obtained from the vendor and recorded on the shipping documents in order to complete the return
Authorization Code - The authorization code that is entered for a removal. (This is not an SAP gap. This information can be maintained in a text field)

When the removal is posted at the SAP Client PC, notify vendors of the removal via EDI or email

Point of Sale (POS) Requirements (gaps in this section are not SAP gaps)
For customer returns and exchanges at POS: (01/20/98)
POS needs to accept all articles returned by customers--not just those on the assortment list
Scan / enter the article and quantity
Enter one of the following reason codes for the return :
Customer Return - Damaged
Customer Return - Dissatisfied
Customer Return - Harmed Pet
Customer Return - Sick / Dead
Sellable
POS produces a disposition tag that will be attached to the product. The tag contains the article, reason code, and date. (The store associate attaches this tag to the product)
When the POS is polled, the return transaction and associated reason code are uploaded with the following inventory movements triggered:
For Harmed Pet product: a ‘warning’ email message containing the article number is issued to the inventory manager
For Sellable product: The article is received directly into unrestricted inventory

POS must be able to sell value-only articles (see the Defective Allowance - Markdown section in the SAP Client PC Interface Requirements below):
When a value-only article UPC is scanned at POS, the cashier enters the hand-written retail price into the register

When an article is scanned at the POS that has its “hazardous recall” flag marked, do not allow that article to be sold and issue a reason message to the cashier so the article is not sold under a “dummy” UPC (see the Article Requirements section)

Recall Requirements (at an SSG SAP Client)
To initiate a recall or other “mass” item removal from SSG: (01/20/98)
Buyer flips the article’s Hazardous Recall flag, if necessary (see Article Requirements)
Buyer creates a Recall Request Order which includes the following information:
Recall Request reference number (system generated)
Effective date range (to and from)
Article to recall
Vendor Bill-to
Vendor Ship-to
Reason Code
Sites to notify of the recall (may be a single site or multiple sites)
Quantity to remove (could be “all”)
Removal price
Transportation method
Execution instructions
Required authorization number
Any special instructions / comments
The Recall Request Order does the following when posted:
The appropriate transaction (Sales Order, Transfer to Scrap, etc.) is generated at each of the affected sites that is populated with the article, the customer (vendor), the comments, and the removal price.
An Inventory Audit of the article is added to each site’s Inventory Audit To-Do List
An email is issued to the affected sites regarding disposition handling

Reporting Requirements
Track and report the following product removal information:
Site
Article
Vendor (bill-to)
Vendor (ship-to)
Quantity
Disposition
Authorization Code
G/L Accounts
Reason Code
Removal price
Removal start dates and recall end dates

The system needs to track removals (dollars and units) under the disposition codes: Defective Allowance (destroy / donate) and Defective Allowance (markdown) by vendor in order to maintain the amount of each vendor’s defective allowance actually used (01/20/98)

Produce two audit reports that may contain some or all of the information above: (01/20/98)
Removal Audit Report: A report produced for Buyers and Inventory Managers that lists all types of product removals the Buyer and Inventory Manager are responsible for over a given period of time. Used instead of a direct approval for all removals
Excessive Removal Exception Report: A report produced automatically for Inventory Managers, Buyers, and Operations Managers when, at the article level, the vendor level, or the site level, removals are outside a user-specified range. For example, the report may be generated for Loss Prevention when a site has removed 100 articles due to store damage in the past week.
Performance Measures
Cost-benefit analysis of removal
Timeliness of removal
Accuracy of removal
Issues
What are the target guidelines for establishing product removal agreements with vendors? How will these guidelines be evaluated? (issue being addressed in the Vendor Management process)
How are Mixing Centers and DCs involved in returns? (per Jim Nelson: Mixing centers should not be considered as consolidators.  However, we will develop a return logistics strategy to handle all types of returns to a central point: either a DC or 3rd party consolidator) (12/10/97)
How will EXE interface with SAP in order to create financial documents? Will the return order itself be initiated in EXE and kicked up to SAP or initiated in SAP and kicked down to EXE?
How is the freight / handling component tied into returns?
What are the ramifications of real-time posting of shortages? (12/14/97)
Do we really need inventory buckets for damaged / removed items? They would ensure tight control over inventory, but the coordination of the buckets could be a difficult task prone to error. Are they more trouble than they’re worth? (12/12/97)
When shortages / damage occur at different points of the process, who is responsible for the shortage (for example, a store transfers RTV articles to a DC for consolidation before return. The DC receives five fewer articles than expected--who “owns” this shortage?) (12/16/97)
There is a discussion outside this session regarding how vendor allowance $ will be allocated to stores. The frontrunner is to allocate allowance $ as a percent of store sales. This determination will impact the financial transactions required for product removals. (12/22/97)
Who receives the profit from the removal handling charge? Stores? They do the work to remove the product; Merchandising? Buyer did the up-front work to negotiate the allowance; Traffic / DC? They would do the consolidation work possibly. (12/22/97)
Jobs Analysis
Jobs:
Merchandise Manager / Buyer:
Negotiates product removal agreements with vendors
Enters combinations of article-vendor-site-reason-date dispositions to represent removal agreements
Issues mass product removal requests in the case of recalls and discontinues
Tracks product removals using the Removal Audit Report and the Excessive Removals Exception Report
Store / DC Operations:
Receives customer returns, recall notifications, and locates damaged products in the site
Initiates product removal transactions
Disposes of product based on system recommendations
Tracks product removals using the Removal Audit Report and the Excessive Removals Exception Report
Inventory Manager
Tracks product removals using the Removal Audit Report and the Excessive Removals Exception Report
Better Practices Recommendations
Using historical performance, negotiate agreements with suppliers to receive damage allowances based estimates from shipment not actuals. Re-negotiate as needed
Negotiate supplier agreements that do not involve physical returns
Merchandise is returned from the store or DC based on a comprehensive evaluation of the costs involved
If necessary, accumulation rules are built around economic shipment quantities subject to some practical time limits related to the life of the product.
“Blanket” return authorizations or authorized disposal methods are used when a lump sum dollar or item amount is pre-negotiated and part of the supplier agreement
Communicate any pre-negotiated amounts to the RTV facility for planning purposes
When products are shipped, return shipment notices are sent and receipt acknowledgments required

Benefits of Better Practices
Improved inventory productivity
Decreased cost
Improved product quality
Reports
Retained Reports
Vendor Return Notification
Packing Slip / BOL
Removal history by vendor, site, or article with reason codes, cost $, retail $, and date range
Removal Tracking Reports
By G/L Account
Summary by Week and Store
Summary by Store and Account
Top x Articles (cost and units)
By Vendor (detail by G/L account, summary by article, detail by article)
By Store as a % of Sales
Reports Added
Disposition Tag (POS and SAP Client PC)
Open Removal Exception Report (lists recalls and returns that have been initiated and not yet completed)
Excessive Removals Report (by reason code, vendor, site, and article)
Removal Audit Report (Post-Audit report containing all removals over the course of a week or other amount of time. Used to monitor the removals that are taking place on a daily basis)
Forms
Retained Forms
Return / Removal Initiation Form (This was a StockRight form. It needs to be a form on the SAP Client PC)
Forms Added
Recall Request Form (Issues a recall request to sites and creates appropriate recall transactions)

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
