---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Website_Functions.xls.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Website_Functions.xls

## Source
File: `Brain/raw/.extract/SWINDON/Website_Functions.xls.md`
Size: 9,181 bytes

## Raw content
## Sheet1
| Website Functions | Priority | Level of Effort | Score | Pages | Technical Effort / Sollution | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| Multi-currency handling (Simple Solution) | 5 | 4 | 20 | All pages, content | Single currency with false symbols. Affects images (select with rules) | Cosmetic solution with single price and multiple currency symbols |
| Tax Calculation | 5 | 4 | 20 | Order detail | 17.5% UK. Fixed rate US. How R prices stored in SAP | Use standard 17.5% sales tax for UK, and a 6% calculation for the US |
| Shipping / Handling charges | 5 | 4 | 20 | Order detail | Fixed rate excl special products (which have rate attr) | Define fixed rate handling charges |
| Specified Delivery Time | 5 | 4 | 20 | Checkout | Possible only for bulky items (eg.sofa). Clarify with Ros | Custom development of web functionality |
| Observation tracking and logging | 5 | 4 | 20 | All | Basis for rules governing content selection. | Incorporation of observation events into the webpage script |
| Shopping basket | 5 | 3 | 15 | Basket | Use BV functionality | Standard BroadVision Feature |
| Persistent Shopping basket | 5 | 3 | 15 | Basket | Use BV functionality. Unlikely Price locking (for how long?) | Standard BroadVision Feature |
| Implement Cookie functionality | 5 | 3 | 15 | NaN | Just store customer id? | Standard BroadVision Feature |
| E-mail order confirmations | 5 | 3 | 15 | Checkout | Need to check BV functionality | Standard BroadVision Feature |
| Keyword / Parametric search | 5 | 3 | 15 | Sidebar,results,adv | Need to check BV functionality | Standard BroadVision Feature |
| Credit Authorization / Settlement | 5 | 3 | 15 | Checkout | Fake | Simulate payment processes |
| Support multiple payment options / per order | 5 | 3 | 15 | Checkout | Card/voucher. Check BV func | Standard BroadVision Feature, custom dev to support payment w/ loyalty points |
| E-mail shipment updates to consumer | 5 | 3 | 15 | (background) | Back end scheduled job. Check BV func | Standard BroadVision Feature |
| Cross-sell and up-sell indicators | 5 | 3 | 15 | Product,cmatrix,basket | BV cross sell & NP | Manual identification of product relationships and location to display on Website |
| Use of BroadVision Incentives / Discounts | 5 | 3 | 15 | all with ads/incentives | Check BV func. Affects images. Order value related. | Incentives will be % offs and displayed as "Ads", effort refers to content development |
| Definition of customer database  custom attributes | 5 | 2 | 10 | NaN | Implement schema with input from analysts. | Majority of effort involves business analysis of data model |
| Definition of product database custom attributes | 5 | 2 | 10 | NaN | Implement schema with input from analysts. | Majority of effort involves business analysis of data model |
| Definition of BV Communities | 5 | 2 | 10 | NaN | Implement rules based on analysts' analysis | Majority of effort involves business analysis of data model |
| Personalisation based on Rules Based Matching | 5 | 2 | 10 | All | Incorporate use of rules into scripts (BV). | Majority of effort involves business analysis of data model |
| Personalisation based on Collaborative Filtering | 5 | 2 | 10 | Most | Incorporate use of rules into scripts (NP) | Majority of effort involves business analysis of data model |
| Sales order tracking | 5 | 1 | 5 | Order tracking | Need to check BV functionality | Standard BroadVision Feature |
| Loyalty Card Program Points Wallet / Account Review Page | 5 | 1 | 5 | Acct review / order detail | Display attr of cust and link old orders to Order detail page | Medium BroadVision Development Effort (does not take POS / in-store issues into account) |
| Loyalty Card Program Points earning logic | 5 | 1 | 5 | NaN | Hold earning as attr of order. | Medium BroadVision Development Effort (does not take POS / in-store issues into account) |
| User registration process | 5 | 1 | 5 | Register | NaN | Standard BV Functions / Integration with existing customer database |
| In-store Return Process for web purchases | 5 | 1 | 5 | Policy | Obtain policy content (and salvage from Ishop) | Store integration with Wesite sales order data |
| Track Store purchasing history | 5 | 1 | 5 | Acct review | NaN | Develop data model to store transactions / develop SAP interface |
| Real time fulfillment center Inventory check | 5 | 1 | 5 | Product, checkout | Make call to SAP (practical to do real-time?) | SAP integration issue |
| WAP - Wireless phone delivery of content | 5 | 1 | 5 | NaN | Need to identify applications for it | Custom development of web functionality |
| Out of stock functionality | 5 | 1 | 5 | Product, (rules) | Don't allow adding of out of stock items to basket (ensure always in stock!) | SAP integration issue |
| WAP - Ordering / Sales transactions | 5 | 1 | 5 | NaN | (see above) | Custom development of web functionality |
| Household / Family user accounts | 5 | 1 | 5 | NaN | Have individuals and maintain relationships seperately | Custom development of web functionality |
| Corporate Information (FAQ, Policies, Warranties, Financial, contact etc) | 4 | 5 | 20 | Cust service | Obtain policy content (and salvage from Ishop) | Text based basic HTML content |
| Product comparison matrix | 4 | 3 | 12 | cmatrix | Need to check BV functionality and obtain data from analysts | Identify products and features to base comparison on |
| Customer / Expert product reviews | 4 | 3 | 12 | product | Static reviews and dynamic customer review. Investigate. | Standard BroadVision Feature |
| E-mail promotions based on community | 4 | 3 | 12 | (background) | May be done with Valex, not BV. | Standard BroadVision Feature |
| Recipe Configurator | 4 | 3 | 12 | cookclub | Bespoke with scenario design by Ros | Custom development of web functionality |
| Furniture Configurator | 4 | 3 | 12 | furniture product | Bespoke with scenario design by Ros | Custom development of web functionality |
| Favorite Links | 4 | 3 | 12 | sidebar | NaN | Custom development of web functionality |
| Multiple Shopping lists | 4 | 3 | 12 | my acct/shoplist/product | Need to check BV functionality | Standard BroadVision Feature |
| Printing from the Kiosk | 4 | 3 | 12 | cookclub | Bespoke. | Standard windows functionality from the Kiosk / Custom development of web functionality |
| Aggregation / analysis of observation data | 4 | 2 | 8 | NaN | Not BV. Valex? | Identification of data mining tools / actions |
| Date reminder service (Calendering) | 4 | 2 | 8 | address book | Need to check BV functionality | Custom development of web functionality / Standard BV functions |
| Discussion Groups / Community Development (Food / Wine Club) | 4 | 2 | 8 | cookclub | Need to check BV functionality | Standard BroadVision Feature / Develop context for use |
| On-line gift registry functionality (wedding) | 4 | 1 | 4 | registry | Need to check BV functionality / bespoke | Custom development of web functionality |
| In-store pick up of web purchases | 4 | 1 | 4 | checkout/delivery sched | really do it? | Involves local / store inventory check, and ability to display Web order thru POS |
| Add-on services (gift wrap, gift card) | 3 | 3 | 9 | basket | Treat wrap and card as order items | Decide whether cosmetic or semi-functional |
| Streaming audio / video content | 3 | 3 | 9 | product | Link in supplied multimedia content | Development / placement of content |
| Affiliate Sales | 3 | 3 | 9 | product | Mock up 3rd party site, but fake commision system | Simulate the functionality if required |
| Multiple Ship to addresses on sales order | 3 | 1 | 3 | NaN | NOT DOING | Difficult BV modification, Difficult SAP interface issue |
| Loyalty Card Program Points redemption | 3 | 1 | 3 | checkout | NaN | Cross Channel / SAP Integration Issue |
| Point Bonuses based on dates or other events | 2 | 3 | 6 | product/checkout | NaN | Custom development of web functionality |
| CD Configurator | 2 | 2 | 4 | cd config | bespoke | Custom development of web functionality |
| Multi-language handling | 2 | 2 | 4 | NaN | Avoid country-specific language | Attempt to avoid regional language differences |
| Multi-currency handling (Full solution) | 2 | 2 | 4 | NaN | Opting for simple solution | Storage of multiple prices, w/ back office integration to incorporate price changes, exchange rates, and regional pricing strategies |
| B2C Replenishment functionality / Suggested shopping lists | 2 | 1 | 2 | NaN | NOT DOING | Custom development of web functionality |
| Real time local / store inventory check | 2 | 1 | 2 | product | call to SAP | SAP integration issue |
| Shopping Assistant (Java Applet, Chat, etc.) | 2 | 1 | 2 | NaN | Possibly do some elements of this. | Custom development of web functionality |
| B2C Auction functionality | 2 | 1 | 2 | NaN | NOT DOING | Custom development of web functionality |
| Full text search | 1 | 1 | 1 | NaN | Possibly doing - Investigate SQL Server capabilities | Involves additional investment |
| Natural language search | 1 | 1 | 1 | NaN | Possibly doing - Investigate SQL Server capabilities | Involves additional investment |

## Sheet2
|
|  |

## Sheet3
|
|  |

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
