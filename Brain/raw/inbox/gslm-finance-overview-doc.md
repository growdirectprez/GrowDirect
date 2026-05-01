---
date: 2026-05-01
type: raw
source: Brain/raw/.extract/tier1-md/gslm/GSLM Finance Overview.doc.md
tags: [canary, gslm, retail-data-model, walmart, comparison, tier1-extract]
project: canary
status: unprocessed
---

# GSLM Finance Overview.doc

## Source
File: `Brain/raw/.extract/tier1-md/gslm/GSLM Finance Overview.doc.md`
Size: 15,064 bytes

## Raw content
The Finance entities describe transactional financial information for Sales and Cash Office Transactions.
Sales data has been modeled to provide a clear picture of item movement at customer basket level.  This is the most granular level of sales information and therefore forms the basis of all flows of sales data throughout the home office systems, whether this be for PI, Pay on Scan or any other home office requirement. The sales model does not contain all attributes which are captured by the point of sale, but provides the core attributes required to support the retail business.
Cash Office transactions have been logically grouped into three areas within the model
Paid In / Paid Outs
Pickups
Financial Adjustments
Paid In / Paid Outs, models the transactions for all financial movements in and out of the store that are not encompassed by standard goods in receiving processes or standard retail sales. Examples could be Paid Outs for local store maintenance (glazier for broken window) and Paid Ins for revenue gained from on site tenants.
The pickup and adjustments parts of the model provide entities for tender and other miscellaneous pickups from the registers inside of a store. For example, credit card tenders and layaway payments.
The Financial adjustment entity  allow for the descriptive and quantitative differences between expect and actual inventory value  be accounted for at store department level
Assumptions:
There are no financial ledgers held in the store therefore the GSLM only contains entities to cover business transactions. These business transactions will be converted into financial ledger postings at the home office.
The financial entities of the GSLM cover Sales and Cash Office only. All business transactions relating to the receipting and acknowledgement of deliveries (which also have financial impact) are catered for in the Supply Chain part of the GSLM.
The logical model does not hold aggregates of sales basket information. Sales transactions are held at the most granular level, any aggregation required for downstream systems will be the responsibility of extra tools.
The following section describes the GSLM entities and their attributes which have been modeled as part of the Finance scope:
Entity Name
Description
SalesHeader
This entity describes the transaction level entities of each sales transaction that is processed through the point of sale
Attribute
Type
Description
associate_win
Associates
The Cashier or Operator Number of the person who performed the Transaction
sales_outlet_id
SalesOutlets
The sales outlet identifier where the transaction took place
register_bank_code
Code
The Register Bank that the Register is part of. For example (main bank, pharmacy, electronics)
register_nbr
Number
The register number that the transaction took place on
register_type_code
Code
The type of register that the transaction took place on (regular, self service, pay at pump etc)
business_trading_date
Date
The trading date that the transaction took place on. This may or may not be the same as the jullian day. If stores are 24 hour trading the logical business day (as defined by an end of day process) may be different to the calendar day, depending on when the end of day process runs
training_mode_ind
Indicator
An indicator to state if the sales transaction took place in training mode on the register or not.
transaction_amount
Amount
The total amount that the goods / service in the transaction totals
transaction_start_date
DateTime
The date and time that the transaction started
transaction_end_date
DateTime
The date and time that the transaction ended
transaction_nbr
Number
The register specific transaction number for the sales transaction
transaction_void_ind
Indicator
An indicator if this transaction was voided



Entity Name
Description
SalesLineItem
This entity describes the items when are being sold within a sales transaction
Attribute
Type
Description
sales_header
SalesHeader
A reference to the header that these items relate to
line_item_nbr
Number
The line item number of this item within the sales transaction
article_id
ArticleItems
Foreign key to the ArticleItem entity, defines the UPC of the SKUItem being sold
line_item_entry_code
Code
The indicator for how the item was entered into the register (scan, keyed, weighed, etc)
line_item_price_per_uom
Amount
How much does the item sell for by unit measure
line_item_qty
Number
How much of the item is sold (-ve means a return or void)
line_item_return_reason
Code
If the item is returned then this is the reason for why it is returned (wrong product, broken, bad etc)
line_item_tax_amount
Amount
The total amount of tax charged on this item
line_item_tax_exempt
Indicator
The item is exempt from sales taxes
line_item_voided_ind
Indicator
A flag to specify  if the item has been voided
line_item_reduction_reason
Code
If the item has been reduced in price the reason why is  reduced
line_item_date
DateTime
The date and time of when the item was entered into the register for this sale



Entity Name
Description
SalesTender
This entity describes the tenders that have been applied to a specific sales transaction for payment
Attribute
Type
Description
sales_header
SalesHeader
A reference to the transaction header this tender relates to
tender_amount
Amount
The amount of money tendered in the base currency that the transaction is calculated in
tender_cashback_amount
Amount
If this tender includes cashback, this is the cashback amount received by the customer
tender_type_code
Code
The type of the tender taken (eg Cash, Credit Card etc)
tender_subtype_code
Code
An optional sub tender type (eg Visa, Mastercard)
payment_card_id
Text
A payment card number
tender_entry_code
Code
The way the tender was entered into the POS (swiped, keyed, chip / pin)
tender_voided_ind
Indicator
A flag to indicate if the tender was voided
tender_coupon_qty
Number

tender_coupon_type_code
Code
The type of coupon tendered (Manufacturer, Own brand etc)
coupon_barcode_id
Text
The barcode of the coupon scanned as a Tender
tender_change_ind
Indicator
An indicator which designates if this tender is 'change' ie money given back to the customer
tender_authorization_code
Text
The authorization code received from a 3rd party entity to authorize a payment
foreign_currency_code
Code
If the tender was received in a foreign currency then this will be the code for the currency tendered
exchange_rate
Number
The exchange rate applied if the tender was in a foreign currency
foreign_currency_amount
Amount
The amount of foreign currency tendered
tender_date
DateTime
The date and time of when the tender was entered into the register
tender_offline_ind
Indicator
Flag to indicate if the credit  payment was approved offline.



Entity Name
Description
SalesLineItemDiscount
This entity describes discounts that are applied to individual items
Attribute
Type
Description
sales_item
SalesItems
A reference to the sales item which is being discounted
discount_amount
Number
The amount of discount that is applied to the item
discount_entry_code
Code
The way the discount is entered into the register (Manual, Scanned, Auto etc)
discount_date
DateTime
The timestamp of when the discount was applied
promotion
SalesOutletSKUItem  PromoCompDetails
A reference to a promotion which may be associated with the discount
discount_voided_ind
Indicator
A flag to indicate if the discount has been voided



Entity Name
Description
SalesLoyalty
This entity describes any loyalty information attached to a sale
Attribute
Type
Description
sales_header
SalesHeader
Foreign Key to the Sales Header entity, defines the sales transaction to which the loyalty information is associated.
loyalty_native_key
NativeKeys
The Loyalty Card Number
loyalty_entry_code
Code
Entry method used for this loyalty card (e.g. Scanned, Key Entered)
loyalty_points
Number
The number of Points awarded for this Transaction
loyalty_points_reentered_ind
Indicator
Indicates the Loyalty Card points were added to this Loyalty account in a separate transaction.
loyalty_points_todate
Number
Lotalty Card Points awarded to date for this Loyalty account at the time of this Transaction
loyalty_qualifying_spend
Amount
The amount from this transaction which qualifies for the loyalty scheme - e.g. excludes tobacco.
loyalty_redeemed_amount
Amount
The Amount redeemed from this loyalty account as part payment for this transaction
loyalty_card_scheme_ind
Indicator
The indicator for different loyalty schemes
loyalty_staff_discount_ind
Indicator
Indicates whether the loyalty card is also a staff discount card
loyalty_voided_ind
Indicator
Indicates this Loyalty Card was Voided in this Transaction



Entity Name
Description
SalesTax
The entity which describes the tax on a sales transaction at the header level
Attribute
Type
Description
sales_header
SalesHeader
Foreign Key to the Sales Header entity, defines the sales transaction to which the tax information is associated.
tax_code
Code
Tax code to describe the tax type and jurisdiction being charged on the sales transaction.
tax_amount
Amount
The total amount of tax for the related tax code that was charged on the sales transaction.



Entity Name
Description
SalesLineItemTax
The entity which describes the tax associated with a single line item on a sales transaction.  A single item can multiple tax code and amount records. (State, Federal, Municipal, etc)
Attribute
Type
Description
sales_header
SalesHeader
Foreign Key to the SalesItem entity, defines the sales transaction line number to which the tax information is associated.
sales_line_item_nbr
SalesItems
Line number of the sales transaction.
tax_code
Code
Tax code to describe the tax type and jurisdiction being charged on the sales line item.
tax_amount
Amount
The total amount of tax for the related tax code that was charged on the sales line item.

Entity Name
Description
PaidOut
This entity describes any money that is paid out of the store which has not been subject to a register transaction. Examples would be (Petty Cash, Local emergency building maintainance, local product purchasing etc)
Attribute
Type
Description
associate_win
Associates
Associate id number who created the transaction
account_nbr
 Number
Account number that the 'Paid Out' is being drawn from
paid_out_date
 Date
The date the 'Paid Out' occurred
paid_out_amount
 Amount
The amount of the 'Paid Out'
retail_value
 Amount
The retail value of any goods which have been purchased from this 'Paid Out'
paid_out_invoice_nbr
 Number
The invoice number associated with the 'Paid Out', either a Walmart or a supplier reference
paid_out_type_code
 Code
What type of 'Paid Out' is this (eg Procurement, Maintainance etc)
dept_nbr
Departments
Which department was the 'Paid Out' for?



Entity Name
Description
PaidIn
This entity describes any money that is paid into the store accounts which has note been paid in through a register. An example could be tenant payments for instore concession stands.
Attribute
Type
Description
associate_win
Associates
Associate id number who created the transaction
account_nbr
 Number
The account number the money is paid into
paid_in_date
 Date
The date the money is paid in
paid_in_amount
 Amount
The amount of money paid in
dept_nbr
Departments
The sales department that the money relates to
paid_in_type_code
 Code
The type of 'Paid In' (3rd party vendor, tenant etc)
paid_in_id
 Number
A reference ID for the 'Paid In' transaction



Entity Name
Description
PickUp
This entity describes a pick up event that has taken place at a register. A pickup may be a cash collection or a collection of a particular type of sales, either at end of day or within day.
Attribute
Type
Description
pick_up_id
 Number
The reference number of the pickup
pick_up_date
 DateTime
When the pickup occurred
opening_balance
 Amount
What was the opening balance of the register
closing_balance
 Amount
What was the closing balance of the register
register_fund
 Amount
The float amount in the register
change_fund
 Amount
The change amount in the register
final_pick_up_of_day_ind
 Indicator?
Was this the final pickup of the day from this register
register_nbr
 Number?
The register number of the pickup
pick_up_business_date
 Date?
The business date of the pickup (this may be different from the actual calendar day based on when end of day occurs)
bad_checks_purchased
 Amount?
How many bad checks were purchased from the bank for this register
bad_checks_redeemed
 Amount?
How many bad checks were redeemed on this register
bad_checks_redeposited
 Amount?
How many bad checks were redepositied for this register
sales_outlet
 SalesOutlets
The sales outlet number



Entity Name
Description
PickUpDetail
This entity describes the detail behind the Pick Up entity
Attribute
Type
Description
pick_up_detail_id
 Number
The reference number of this pickup detail line
pick_up_id
 PickUps
The reference number of the pickup header
pick_up_type
 Code?
What type of pickup is this eg (Tender, Voids, Layaway Payments)
pick_up_category
 Code?
What category is the pickup eg (Visa, Mastercard etc)
pick_up_amt
 Amount?
How much was picked up
pick_up_date
Date
When was the pickup made
adjustment_amount
 Amount?
How much does the pickup need to be adjusted eg (Unknown Losses)
adjustment_reason_code
 Code?
What was the reason for the adjustment (Unknown Loss, Fake Bills etc)



Entity Name
Description
Financial Adjustment
This entity describes store initiated financial adjustments which are made at department level, and not assoicated with specific items.
Attribute
Type
Description
location_id
Locations
Unique identifier of the location which created the financial adjustment
account_nbr
Number
Account number the adjsutment is made against
transaction_date
Date
Date of the transaction
transaction_nbr
Number
Transaction number
adjustment_amount
Number
Amount of the adjsutment
adjustment_type_code
Code
What was the reason for the adjustment (Unknown Loss, Fake Bills etc)
associate_win
Associates
Foreign key to the associate table, the WIN for the associate who created the adjsutment transaction



Entity Name
Description
Markdowns
This entity describes permanent markdowns that revalue inventory in the store at skuitem level
Attribute
Type
Description
sales_outlet_nbr
SalesOutlets
The store which took the markdown, the FK to the SalesOutlet entity
sku_item_nbr
SKUItems
The SKUItem against which the markdown was taken, FK to the SKUItem entity
event_id
Code
The markdown event code, or price change number the markdown is associated with
markdown_type_code
Code
The type of markdown.  (Price Change, Competitor, etc.)
old_retail
Number
Old retail price
new_retail
Number
New retail price
actual_item_qty
Number
Number of items being marked down
markdown_date
Date
Date of the markdown transaction
journal_post_date
Date
Date the markdown is posted in the journal
competitor_code
Code
If the markdown type is competitor, the code for the competitor being price matched.





## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
