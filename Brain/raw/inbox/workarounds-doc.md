---
date: 2026-04-22
type: raw
source: /Users/gclyle/mnt/nas-archive/Work/Projects/Kroger CRP/Workarounds.doc
tags: [secure, secure, kroger, retail, client-implementation]
project: secure
status: unprocessed
---

# Workarounds.doc

## Source
File: `/Users/gclyle/mnt/nas-archive/Work/Projects/Kroger CRP/Workarounds.doc`
Size: 2,642 bytes

## Raw content
Area
Retek Gap
Process Workarounds
Allocation
Reserving New Store Stock – Java allocation does not have a method for reserving stock at the DC for new stores.
Utilized base RMS functionality to create a “new store” hold bucket within the “non-sellable” bucket.  Manual unit inventory adjustments were made from the DC location to the new store non-sellable location.  When the new store was ready for receipts, additional logic in the upload allocation interface moved inventory from the new store non-sellable location.
Allocation
Reallocating on Short Shipped PO’s – Java allocation does not automatically reallocate a PO that has been significantly short shipped, as a result, some stores may receive 100% of their allocation, while another store may receive 0%.
The preferred method is to do the allocations against an ASN (EDI 856), but for non-ASN vendors, a client only allocated the average fill rate % quantity. If this non-ASN vendor shipped greater than the average, a second allocation was created for the remaining receipt quantities.
Pricing/ Markdowns
Addition to Clearance Markdowns – If you are adding an item after a clearance promotion was created, you have to add each store individually rather than the whole chain or zone.
Additional items would be setup as a separate clearance markdown.
Purchasing
Multiple OTB Month POs – RMS does not allow for the allocation of a single PO across multiple OTB months.
Created separate PO for each OTB month.
Transfers
Approved Transfer Adjustments – RMS allows transfer quantities to be modified after the transfer is approved.
Developed a policy and procedure.
Reporting
Stock Ledger at Total Company – RMS does not have an on-line view of the total company stock ledger for balancing.  Nor does RMS have any on-line summary level higher than department.
Created a hard copy report out of RMS.
Inventory
Dollar Inventory Adjustments – RMS requires that all dollar inventory adjustments at the SKU/store level rather than at a vendor/ department or vendor/ department/ class level
Created “dummy” classes and SKUs to book dollar inventory adjustments.
Inventory
Indirect Items Hitting Stock Ledger – Even though there is a flag on the item header screen for non-sellable merchandise, RMS posts all purchases to the stock ledger thus requiring a resulting adjustment to take non-sellable goods out of inventory.
Created a separate department for non-sellable merchandise and customized the interface from RMS stock ledger to financials to exclude the non-sellable merchandise departments.  Excluded the same department from all stock ledger reports.


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
