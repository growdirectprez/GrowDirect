---
date: 2026-04-23
type: raw
source: Brain/raw/inbox/Secure Data Flow.pdf
tags: [secure]
project: secure
status: unprocessed
---

# Secure Data Flow

## Source

File: `Brain/raw/inbox/Secure Data Flow.pdf`
Size: 240,511 bytes
Extracted via: markitdown

## Extracted content

1.0  Customer Order Management
|     |            |                   | Order Picked  | Customer Pick  |                 |     |     |
| --- | ---------- | ----------------- | ------------- | -------------- | --------------- | --- | --- |
|     | From Store | Order Adjusted NO |               |                | Order Picked Up |     |     |
|     |            |                   | and Packed    | up in Store    |                 |     |     |
Webstore
Online Order
YES
 Delivery to Pick
Up Location
| Ship from store |     |     |     |     |     |     | Item Damaged |
| --------------- | --- | --- | --- | --- | --- | --- | ------------ |
Call Center
Intervention
Item Returned
| Kiosk |     |     |     | Delivery to  |                 |     |     |
| ----- | --- | --- | --- | ------------ | --------------- | --- | --- |
|       |     |     |     | Customer     | Order Delivered |     |     |
Address
| Call Center |     |     |     |     |     |     | Item Missing |
| ----------- | --- | --- | --- | --- | --- | --- | ------------ |
Ship from Store
|     |     |     |     | to Customer |     |     | Wrong Item |
| --- | --- | --- | --- | ----------- | --- | --- | ---------- |
Where is the
 Order Pending  order line item
Fulfillment
fulfilled Order Delivered
by Retailer
Wrong Price
|     | From Retailer  |                   | Order Picked  |                 |                  |                    |                |
| --- | -------------- | ----------------- | ------------- | --------------- | ---------------- | ------------------ | -------------- |
|     |                | Order Adjusted NO |               | Order Picked Up |                  | Order Adjusted YES |                |
|     | DC             |                   | and Packed    |                 |                  |                    |                |
|     |                |                   |               |                 | Order Delivered  |                    | Wrong Quantity |
|     |                | Yes               |               |                 | by Third Party   | NO                 |                |
Metrics:
| Return Item Count and Amount |     |     |     |     |     |     | Order Delayed |
| ---------------------------- | --- | --- | --- | --- | --- | --- | ------------- |
Call Center
Missing / Damaged Count and Amount Intervention Order Complete
Lost Order Count and Amount
Shipping Address Count and Frequency
|     |     | YES |     |     |     |     | Order Lost |
| --- | --- | --- | --- | --- | --- | --- | ---------- |
Shipping Adjustments Count and Amount
Call Center Adjustments Count and Amount
 From Third
| Count of unique Tenders   |                 |                   | Order Picked  |                 |     |     |                |
| ------------------------- | --------------- | ----------------- | ------------- | --------------- | --- | --- | -------------- |
|                           | Party / Vendor  | Order Adjusted No |               | Order Picked Up |     |     |                |
| Count of Tenders by Order |                 |                   | and Packed    |                 |     |     | Order Returned |
DC
Order
Undeliverable
Digital
Delivery

Secure Store / Online Inventory
Data Flow
Distribution Center
| Ecommerce Engine  | Retail Location |     |               |
| ----------------- | --------------- | --- | ------------- |
| Order Management  | Point of Sale   |     | Supply Chain  |
Call Center Activity
| System    | Transactions |             | Systems |
| --------- | ------------ | ----------- | ------- |
| Customer  |              | Adjustments |         |
Sales Data
| Order Details |     | Inquiries | Shipments to Store |
| ------------- | --- | --------- | ------------------ |
Transfers
Adjustments
       Secure Exception Based Reporting
Website Statistics
Device IDs
Common Retail Data
Model
Retail Item Master
Online Item Master
Product Hierarchy
|            |                   | Employees            | Location Master          |
| ---------- | ----------------- | -------------------- | ------------------------ |
| Price File | Tender Activity   | Customers            | Organizational Hierarchy |
| Promotions |                   | Cashiers / Operators |                          |
|            | Giftcard Activity |                      | Operational Alignments   |
| Coupons    |                   | Vendors / Delivery   |                          |
DC Personnel
Merchandising
|     | Financial Systems | People | Reference Data |
| --- | ----------------- | ------ | -------------- |
Systems

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
