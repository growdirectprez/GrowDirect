---
classification: internal
type: wiki
status: active
date: 2026-05-03
last-compiled: 2026-05-03
needs-review: 2026-08-03
source: help.counterpoint.ncrvoyix.com (3,782 indexed pages), counterpointuniversity.com, direct topic fetches
purpose: Counterpoint-centric feature surface for Canary Go UX reverse-engineering; feeds screen inventory, user scenario mapping, and sitemap scaffold
companion: Brain/wiki/ncr-counterpoint-api-reference.md
companion: Brain/wiki/canary-go-ncr-counterpoint-crosswalk.md
companion: docs/superpowers/specs/2026-05-03-canary-go-ui-wave-plan.md
tags: [counterpoint, ncr, functional-decomp, ux-source, screen-inventory, feature-map]
---

# NCR Counterpoint — Full Functional Decomposition

**Governing thesis:** This is the atom-level decomposition of NCR Counterpoint's functional surface, organized by Counterpoint's own module/menu structure — not Canary's. ~600+ named functions, 95 discrete maintenance forms, 50+ named reports across 18 top-level modules. Serves as the source-of-truth for Canary Go UX reverse-engineering: every user scenario Counterpoint supports is enumerated here so Canary can match, improve, or deliberately displace it.

**API gap note:** Counterpoint's REST API (~97 endpoints) exposes only a fraction of this surface. The remainder is UI-only (Pervasive SQL direct). Canary's MCP layer must cover the full functional surface, not just what the API exposes.

---

## 1. CounterPoint Fundamentals

### Navigation & UI Conventions
- LookUps (field-level search/select on every record type)
- Filters (record filtering on list views)
- Common menu commands (New, Save, Delete, Cancel, Copy From, Enable Protected Changes, LookUp, Next/Previous Record, Notes, Print, Set Filter, Table View, Touchscreen Keyboard toggle, Help)
- Toolbar buttons (system-wide, present on every form)
- Date entry conventions and shortcut keys
- International date and time support
- Floating date parameters (dynamic date ranges for reports)

### Report Parameter System
- Per-report parameter sets (save, load, delete)
- Pre-defined parameter sets
- Floating date parameters across all reports
- Saving reports to disk (PDF, Excel, etc.)
- Assigning saved parameter sets to menu items
- Authorizing users to maintain report parameters
- Saved Report Parameters utility

---

## 2. Point of Sale

### Ticket Entry — Standard Interface
- Start Ticket Entry session
- Enter customer number / walk-in (anonymous) customer
- Scan or key item number
- Quantity entry and duplicate-line consolidation
- Sell substitute items when quantity insufficient
- Move lines up/down; sort lines by any column
- Find lines by item number
- Reprice all lines (on demand)
- Enter purchase order number on ticket
- Specify price-from location per document or per line (Enterprise)
- Specify ship-from location per document or per line (Enterprise)
- Specify profit center per document or per line (Enterprise)
- Point of Sale Document Zoom (detail pop-up)
- Enter ticket notes
- Modify sales tax on a ticket
- Process a return in Ticket Entry
- Sell a gift certificate (single or multiple)
- Pay code buttons (configured tender shortcuts)
- Payment Entry window — tender selection
- Split tender (multiple pay codes on one ticket)
- Reissue change / auto-issue change in tendered pay code
- Print gift receipts
- Ticket Completion dialog (receipt printing, post-close options)
- View open POS documents
- Pay-out transactions (cash out of drawer without sale)
- Validated returns (setup, perform, authorize users)
- Automatically create cash receipt application lines
- Pay-on-account transactions using customer card
- Package tracking numbers

### Ticket Entry — Touchscreen Interface
- Full touchscreen ticket workflow (parallel to standard interface)
- Sell multiple gift certificates (touchscreen)
- Touchscreen layout and button configuration
- Custom Action Touchscreen buttons
- User-defined Touchscreen buttons
- Expanded field choices for totals panel
- Remain-in-line mode options
- Entering gridded (matrix) items in multi-cell mode

### Document Types
- Sale ticket
- Return ticket
- Refund ticket
- Hold (suspend/recall)
- Quote
- Order (sales order — deposit, track, release/ship)
- Layaway (deposit, payment, pickup, cancel)

### Orders & Layaways Detail
- Create new order / layaway
- Add items; modify; cancel
- Release order (pick up / ship)
- Process transaction with multiple line types
- Freeze order/layaway prices option
- Order # / layaway # as release ticket # option
- Prompt for ship-to address on orders/layaways
- Allow orders/layaways to affect available credit
- Import order notes
- Holds: document hold lifecycle
- Reprinting tickets from history
- Order Activity report

### Drawer Management
- Activate a drawer session
- Open / close drawer
- Assign users to drawers
- Compulsory cash drawers (require open before sale)
- Open drawer alarm
- Pay-in / pay-out transaction setup and entry
- Drawer overage/shortage GL distributions
- Exclude pay codes from drawer functions

### End of Day
- X-Tape (mid-day totals report — no close)
- Z-Tape (end-of-day settlement close)
- Settlement process (credit card batch close, tender reconciliation)
- Purge settlement history

### POS Credit Card Processing
- Integrated authorization (CPGateway)
- Credit / debit card tender
- Debit card with PIN pad
- EBT food stamps
- Purchase cards
- American Express CAPN / direct authorization
- CVV2 / CVC2 verification
- AVS (Address Verification Service) — Visa/MC, AmEx, Discover
- AmEx AAV / CID verification
- Override CVV/CID mismatch
- CPDialup (dial-up fallback processor)
- Settling credit card batch
- Viewing full card numbers in ticket history (authorized users)

### POS Miscellaneous Features
- Signature capture
- Random weight barcodes (scale integration)
- Receipts with ticket number barcodes
- Preview receipts before print
- Enhanced receipt printing options
- Consolidated ticket lines on receipt
- Miscellaneous charges 1–5 per ticket (configurable names)
- Ticket profile codes (5 alpha, 5 code, 5 date, 5 numeric — custom fields)
- Auto-display item and customer images
- Automatically lock station after inactivity
- Default workgroup per workstation
- Minimum prices enforcement
- Treat-as-discount miscellaneous charge
- Reason codes for voids, returns, discounts
- Alcohol verification / ID scanning
- Repricing all lines after hold-and-recall

### POS Reports
- Ticket Journal
- Settlement Journal
- Closed Layaway Journal
- Closed Order Journal
- Drawer Summary Journal
- X-Tape
- Z-Tape
- Price Exceptions report
- Order Activity report
- Flash Sales report

---

## 3. Inventory

### Item Maintenance
- Define new items (full form)
- Quick Items (add-on-the-fly simplified form)
- Simplified item setup mode
- Template items (copy structure from template)
- Copy From existing item record
- Item number / description / short description / long description
- Item status (active / inactive); manage inactive items
- Item categories and sub-categories
- Item attributes (6 configurable attribute fields)
- Item profile codes (5 alpha, 5 code, 5 date, 5 numeric)
- Prompt codes (3 custom prompts per item, shown at POS)
- Serial prompt codes (3 per item; see Serial Tracking)
- Stocking unit / alternate units / associated units
- Unit-specific barcodes (multiple barcodes per unit)
- Quantity decimals / price decimals configuration
- Tax category assignment
- Tare weight code assignment
- Mix-and-match code assignment
- Label code assignment
- Primary vendor / vendor's item number
- Warranty period 1 / 2
- Image file assignment
- URL field
- COS% (cost of sales percentage)
- Freight amount
- Last cost
- Regular price / Price-1
- Location-specific prices
- Grid tab (color/size/dimension matrix — sells as cell combinations)
- Consolidated Grid report
- Barcode tab (generate and manage multiple barcodes per item)

### Pricing
- Regular price
- Location-specific prices (per store/location)
- Special prices (date-ranged, quantity-triggered)
- Contract prices (customer-specific, overrides regular)
- Promotional prices (planned promotions)
- Markdown history tracking
- Price rules: BOGO / twofer
- Price rules: mix-and-match codes and rules
- Price breaks (quantity-based tiered pricing)
- Customer Price List report
- Using total item quantity for pricing
- Simplified price rules entry mode
- Price Test window (test any item/customer/qty/date combination)
- Minimum prices enforcement
- Price Exceptions report and history

### Inventory Control & Quantities
- Establish on-hand quantities (initial setup)
- Establish min/max quantities per location
- Location groups (aggregate locations into logical groups)
- Locations setup (named stocking locations per store)
- Inventory Control settings (company-wide defaults and flags)
- Inventory adjustment entry (manual adjustments with reason code and GL)
- Import inventory adjustments from file
- Committed Inventory report (quantity reserved by open orders/layaways)
- Inventory Status report (with cell-level detail for matrix items)
- Inventory Analysis report (with cell-level detail)
- Inventory History report (with cell-level detail)
- Inventory Aging report
- Retail Inventory Value report
- Historical Valuation report (Enterprise)
- Twelve-month Item History report
- Create Inventory report
- Item report
- Merchandise Analysis report
- Inventory Grid Overview report

### Physical Count / Cycle Counting
- Create physical count (filter by location / item selection / inventory selection)
- Enter physical count (multi-user simultaneous entry)
- Post physical count
- Multi-location physical count with location-level locking
- Specify posting date for physical count transactions
- Import physical count from file
- Physical Count Adjustment GL distributions

### Transfers (Multi-Location)
- Enter Transfer Out (send from location)
- Enter Transfer In (receive at location)
- Quick Transfers (simplified transfer entry)
- Import transfer-out transactions
- Import transfer-in transactions
- Transfer clearing account setup
- Transfer batch setup
- Transfer reports and journals

### Inventory Adjustments
- Inventory adjustment entry (quantity, cost, reason)
- Purchasing adjustment entry
- Import inventory adjustments

### Bills of Material / Kits / Assembly (Enterprise Option)
- Bills of Material (define multi-component items including labor)
- Quick Assembly transactions entry
- Kits-Bills of Material option
- Sales kits
- Bill of Material reports
- Quick Assembly reports

### Serial / Lot Tracking
- Serial prompt codes (3 per item: data type, entry required, constraint, error message)
- Applicable to: adjustments, receivings, returns, RTVs, sales, transfers
- Print serial numbers on labels

### Barcode & Label Management
- Barcode Management utility
- Quick Barcodes (rapid barcode assignment)
- Generate barcodes (algorithm-based)
- Barcode types setup
- Label codes (assign label formats to items)
- Print labels: laser / inkjet / dedicated thermal
- Immediate label printing (at point of receiving or sale)
- Labels from Tags (reprint from pending tag queue)
- Printing a portion of labels (skip N labels)
- Print after posting
- Print user-defined label jobs
- Print shelf tags
- Print coded costs on labels
- Print serial numbers on labels
- Preview labels before print
- Purge printed / unprinted tags
- Label jobs setup (4-step process)
- Datamax printer label support
- NiceLabel software integration
- Admission ticket printing

---

## 4. Customers

### Customer Record Management
- Define new customers (full form)
- Quick Customers (add-on-the-fly simplified form)
- Customer categories
- Customer profile codes (5 alpha, 5 code, 5 date, 5 numeric)
- Customer terms codes
- Customer Control settings (company-wide A/R and loyalty configuration)
- Ship-to addresses (multiple per customer; Address tab + Contacts tab)
- Contact 1 / Contact 2 fields
- Phone 1/2, Fax 1/2, Email 1/2, URL 1/2
- Credit limit / credit rating
- Allow A/R charges / allow layaways / allow orders / allow tickets
- Statement codes
- Commission codes
- Prompt for custom customer fields (inline at ticket entry)

### Accounts Receivable
- A/R Account Management (view statements, open items, full history)
- Cash Receipts entry
- Auto-create cash receipt application lines
- Re-apply documents (reallocate payments across open items)
- Customer Adjustments entry (debit/credit memos)
- Finance charges calculation and posting
- Finance Charges Journal
- Cash Receipts Journal
- Customer Adjustments Journal
- Aging report (4 configurable aging periods with dunning messages)
- Statements printing
- Merge Customers utility
- Renumber Customers utility
- Import customers from file

### Loyalty Programs
- Define multiple loyalty programs per company
- Enroll customers in loyalty programs
- Earning rules: points per dollar / per stocking unit
- Vary points by item number, category, primary vendor
- Vary points by date, day of week, time of day
- Redemption rules (which items are eligible for point payment)
- Point redemption as tender (configurable value per point)
- Manual redemption (accumulate points; redeem outside system)
- Issue and redeem points in both Ticket Entry and Touchscreen
- Loyalty point adjustments entry
- Orders and layaways: points earned after release (not at order time)
- Returns: automatic point deduction
- Authorize users to redeem loyalty points
- Display point redemption messages at POS
- View point balances and full transaction history
- Mailing labels / files based on loyalty enrollment, balances, purchases, status
- Loyalty Point Adjustments Journal

### Gift Registry (Option)
- Create a gift registry (customer + occasion)
- Define occasions
- Add items to a gift registry
- Sell items from a gift registry (marks items as purchased)
- Print a gift registry for a customer
- Gift registry reports
- Purge expired gift registries
- Company settings for gift registry

### Ecommerce Customer Integration
- Share customer records with CPOnline
- Customer-specific discounts and discountable items
- Multiple member price lists (CPOnline tier pricing)

---

## 5. Purchasing

### Vendors
- Define new vendors (full record)
- Vendor categories
- Ship-via codes
- Vendor terms codes
- Identify items by vendor's item numbers (alternate item cross-reference)
- Import / export vendors
- Renumber Vendors utility

### Purchase Requests & Orders
- Create purchase order (Request → edit → post to PO)
- Vendor tab: vendor #, address, contact
- Ship-to tab: shipping address
- Order tab: order date, delivery date, cancel date, buyer, FOB, ship-via, terms, comments
- Lines tab: item number, qty, unit cost; grid entry for matrix items
- Misc charges tab: freight, handling, other charges (up to 5 configurable)
- Negative miscellaneous charges
- Allocate misc charges across lines
- Allocated purchase orders
- Add multiple items to a purchase request at once
- Auto-generate purchase requests (Purchasing Advice)
- Purchasing Advice report (min/max replenishment logic)
- Purchasing Advice by Days of Supply
- Purchasing Advice with cell-level quantities (matrix items)
- Customer-specific purchases (buy for a specific customer/order)
- Open Customer-specific Purchases report
- Copy purchase orders
- Change purchase orders
- Cancel purchase orders
- Reissue purchase orders
- Print Purchase Order form (Crystal Reports; fax/email capable)
- Print labels at time of order
- Purchase Requests Journal

### Receivings
- Receive against a purchase order (full workflow)
- Receiver tab: received date, vendor
- Lines tab: qty received, qty expected, qty to backorder, received cost override
- Grid entry for matrix items during receiving
- Misc charges tab (freight allocation at receiving)
- Print Receiver form
- Print receiving labels (immediate label printing at receiving)
- Receive without a purchase order (blind receiving)
- Enter receivings to cancel purchase orders
- Import receivings from file
- Import receivings for allocated purchase orders
- Receivings Journal
- Unvouchered Receivings report
- Vouchered Receivings report
- Voucher a receiving (approve for A/P posting)
- Multi-user vouchering
- Multiple vouchers per receiving

### Purchasing Adjustments
- Enter a Purchasing Adjustment (cost corrections post-receiving)

### Return-to-Vendor (RTV)
- Define next RTV numbers
- Define RTV GL accounts
- Enter an RTV (items, quantities, reason)
- Post RTVs
- Print RTVs Edit List
- RTV reports and journals

### Purchasing Control Settings
- Purchasing Control options (company-wide defaults)
- Purchase order defaults setup

---

## 6. Sales History

- View Ticket History (search, filter, view full ticket detail)
- Reprint a ticket from history
- Management History (aggregated sales views)
- MarketBasket view in Dashboard (basket analysis)
- Sales Analysis by Color/Size (matrix item sales)
- Flash Sales report (intraday pacing)
- Tax History report
- Price Exceptions History report
- Purge Ticket History utility
- Purge settlement history
- View full credit card numbers in ticket history (authorized users)
- Dashboard — install and configure (embedded analytics UI)
- Markdown History report

---

## 7. Ecommerce (CPOnline Integration)

- Automated Data Transfer with CPOnline (scheduled sync)
- Configure Automated Data Transfer
- Publish items to CPOnline (catalog sync)
- Publish item quantities only
- Publish alternate units
- Publish ticket history (in-store sales to CPOnline for unified history)
- Enhanced item publishing for custom templates
- Enhanced order import for custom templates
- Vendor source (brand) as additional item field
- Credit cards not charged for unshipped items
- Online credit card authorizations
- Pre-authorization of AVS information
- Import order notes from CPOnline
- Multiple member price lists (online tier pricing)
- Share customer information with CPOnline
- Ecommerce reports
- Redeem stored value cards in CPOnline
- Customer-specific discounts and discountable items

---

## 8. Timecards

- Clock in / clock out (employee time tracking)
- Maintain timecards (edit, correct entries — manager)
- Print Timecards report
- Export timecard entries (to payroll)
- Purge timecard entries
- Configure timecards (system settings)
- Define timecard settings per user
- Show timecard warnings at POS login
- Time Clock workstation mode (dedicated clock-in station)

---

## 9. System Administration & Setup

### Company & System Settings
- Company record (company-wide settings, logo, tax IDs)
- Registration (license key and feature activation)
- Multi-currency support
- Canadian sales tax setup
- Multiple tax authorities (tax jurisdiction table)
- Penny tax tables
- Calendars (seasonal date ranges for promotions/reports)
- Tax Codes setup
- Tax Authorities setup
- Commission Codes setup
- Menu Codes (configure menu structure per user/role)
- User Preferences
- Windows authentication setup
- Future / previous transaction months (date security)
- System security code
- Automatically display user configuration windows on login
- Default batches by workgroup
- Refresh Resources and Locks view

### Security
- Security codes (function-level authorization)
- User records (define users, roles, permissions)
- Copy settings from existing user record
- Authorize users by function (granular per-feature)
- Menu code verification
- New POS security settings (per POS function)

### Accounting Interface
- Supported systems: BusinessWorks, MAS 90/200, Microsoft Business Solutions, QuickBooks
- Direct interface (real-time posting)
- Export interface (batch file export)
- Customizable export (G/L integration)
- Customizable export (A/P integration)
- Define account mapping rules
- A/P account number for export interfaces
- Voucher numbers (accounting interface)
- Multi-user vouchering
- Multiple vouchers per receiving
- Import accounts from file
- Import and export vendors
- Report and transfer distributions
- Voucher receivings

### Accounting Distributions (GL Mapping)
Counterpoint generates GL distributions for all these transaction types:
- Inventory adjustments
- Physical count adjustments
- Purchasing (PO / receiving)
- Payables
- Sales (all tender types, line types)
- Drawer overage/shortage
- Gift certificates
- Stored value cards
- Finance charges
- Cash receipts
- Customer adjustments
- Loyalty point adjustments
- Purge Distributions utility

### Credit Cards Setup
- CPGateway configuration and TCP/IP settings
- Address verification and card identification setup
- American Express CAPN compliance
- CPDialup setup
- Direct authorization of American Express
- Industry types configuration
- Processor-specific configuration
- Troubleshooting credit card processing

### Stored Value Cards (Gift Cards)
- Sign up to process stored value cards
- Configure credit card processing for SVC
- Enable stored value cards for company
- Activate a stored value card
- Recharge a stored value card
- Redeem a stored value card
- Issue cash back for a stored value card
- Check stored value card balance
- Assign SVC codes to Touchscreen buttons
- Enable commissions for stored value cards
- Redeem stored value cards in CPOnline

### Gift Certificates
- Enable gift certificates for company
- Create a gift certificate pay code
- Set up gift certificate GL accounts
- Define gift certificate codes
- Auto-assign next gift certificate number
- Enable commissions for gift certificates
- Make gift certificates taxable
- Assign gift certificate codes to Touchscreen buttons

### Labels Setup
- Set up label jobs (4-step process)
- Update pre-defined label data
- Modify pre-defined label jobs
- Specify default label jobs
- Assign label codes to items
- Labels for Datamax printers
- NiceLabel software (installation, pre-defined files, pre-defined jobs)
- Working with barcodes (types, generate, assign)
- Working with tags (queue, purge)

### Utilities
- Data Verify utility (database integrity check)
- Database Customizations Report
- Menu Code Verification
- Purge Distributions utility
- Ticket Performance Test utility
- Renumber Customers
- Renumber Vendors
- Renumber Items
- Merge Customers
- Re-apply Documents
- Saved Report Parameters utility
- CounterPoint SQL Express configuration

### Data Migration
- Migrate from CounterPoint V7 (14-step process)
- Migrate from third-party software (12-step process)
- Create data migration tables
- Modify DTS packages
- Staged migrations
- Migrated modules: Customers, Ecommerce, History, Inventory, Point of Sale, Purchasing, System

---

## 10. Multi-Site (Enterprise Option)

- Multi-Site configuration editor
- DataXtend Replication Engine v8.2
- Automated work-set subscription for remote servers
- Merge customers in a multi-site environment
- Validated returns at remote sites
- Multi-site steps in V7 and third-party migration

---

## 11. Offline Ticket Entry (Option)

- Offline Ticket Entry environment overview
- Radiant CounterPoint Service (CPServices) — server-side sync daemon
- Choose stores for the server to manage
- Provision the server database
- Register offline workstations
- Synchronization schedule (full extract / incremental extract)
- Rebuild offline workstation database
- Rebuild multiple offline workstations simultaneously
- Radiant Log Viewer
- Manage an Offline Ticket Entry system
- CounterPoint Services Status utility
- Configure offline mode (menu codes, activities, auto-assign document numbers)
- Drawer-related activities in offline mode
- Compression of DataSync packages
- Custom schema (columns, tables, triggers, stored procedures) for offline databases

---

## 12. Pricing Deep-Dive (Cross-Module)

| Price Type | Where Defined | Precedence |
|---|---|---|
| Regular price | Item record — Prices tab | Baseline |
| Location-specific price | Item record — Prices tab | Overrides regular for that location |
| Special price | Special Prices form (date + qty triggered) | Overrides regular when active |
| Contract price | Contract Prices form (customer-specific) | Overrides regular for that customer |
| Promotional price | Planned Promotions form | Time-bounded campaign price |
| Price rule (BOGO/twofer) | Planned Promotions — Rules tab | Applied at line-group level |
| Mix-and-match price | Mix-and-match codes + rules | Applied when qualifying basket |
| Price break | Price Breaks table | Qty-triggered discount off regular |
| Minimum price | Item record | Floor — prevents discount below |
| Customer tier price | Customer category → price-list assignment | Segment-level regular price |

---

## 13. Maintenance Forms Index (95 Named Forms)

*Every discrete data-entry screen Counterpoint exposes. This is the screen inventory for the back-office UX:*

### Customer / A/R Forms
| Form | Purpose |
|---|---|
| `frmcustomers` | Full customer record (Main, A/R Documents, Contacts, Holds/Quotes, Orders/Layaways, Ticket History, Unposted Documents tabs) |
| `frmquickcustomers` | Simplified add-on-the-fly customer |
| `frmcustomercontrol` | All A/R + loyalty settings, aging periods, dunning messages, profile field config |
| `frmcustomercategories` | Customer segment codes |
| `frmcustomerprofilecodes` | Custom profile field definitions |
| `frmcustomertermscodes` | Payment terms |
| `frmcustomeradjustments` | Debit/credit memos |
| `frmaraccountmanagement` | View statements, open items, history |
| `frmarcashreceipts` | Cash receipts entry |
| `frmarloyptsadjustmentsenter` | Manual loyalty point adjustments |
| `frmarmergecustomers` | Merge two customer records |
| `frmarreapplydocs` | Reallocate payments |
| `frmarrenumbercustomers` | Renumber customer IDs |
| `frmshiptoaddresses` | Ship-to address + contacts per customer |
| `frmstatementcodes` | Statement format assignment |
| `frmshipviacodes` | Shipping method codes |
| `frmshipzonecodes` | Shipping zone definitions |

### Inventory / Item Forms
| Form | Purpose |
|---|---|
| `frmitems` | Full item record (all tabs) |
| `frmquickitems` | Simplified add-on-the-fly item |
| `frminventory` | Location/quantity view per item |
| `frminventorycontrol` | Company-wide inventory settings + flags |
| `frmitemcategories` | Item category definitions |
| `frmitemsubcategories` | Item sub-category definitions |
| `frmitemattributes` | 6 configurable attribute field definitions |
| `frmitemprofilecodes` | Custom profile field definitions |
| `frmitemprompt` | Item prompt codes (shown at POS) |
| `frmbarcodes` | Barcode management per item |
| `frmimquickbarcodes` | Quick barcode assignment |
| `frmlabelcodes` | Label format codes per item |
| `frmlocations` | Stocking location definitions |
| `frmimlocationgroups` | Location group definitions |
| `frmimtareweightcodes` | Tare weight code definitions |
| `frmimtaxcategories` | Tax category codes |

### Pricing Forms
| Form | Purpose |
|---|---|
| `frmprices` | Regular + location-specific + alternate unit prices |
| `frmpricetest` | Test pricing: item × customer × qty × date × mix-match |
| `frmimspecialprices` | Date-ranged / qty-triggered special prices |
| `frmimcontractprices` | Customer-specific contract prices |
| `frmimpromoprices` | Promotional prices |
| `frmimplannedpromotions` | Planned promotions (Main / Prices / Rules tabs) |
| `frmimmixmatchcodes` | Mix-and-match code definitions |

### Inventory Transaction Forms
| Form | Purpose |
|---|---|
| `frmimadjustmentsenter` | Manual inventory adjustments |
| `frmimphyscountcreate` | Create physical count batch (filter by location/item/inventory) |
| `frmimphyscountenter` | Enter physical count quantities |
| `frmimphysicalcountimport` | Import physical count from file |
| `frmimquicktransfers` | Simplified transfer entry |
| `frmimquickassembliesenter` | Quick assembly entry (with component serials) |
| `frmimmarkdownhistory` | View markdown history |
| `frmimpurgetags` | Purge printed/unprinted label tags |
| `frmimrenumberitems` | Renumber item IDs |
| `frmimsaleskits` | Define sales kits |

### Point of Sale Forms
| Form | Purpose |
|---|---|
| `frmpscontrol` | All POS settings (journals, distributions, profile fields, misc charges, flags) |
| `frmpsstores` | Store-level POS settings |
| `frmpsstations` | Workstation settings (offline next ticket #, device config) |
| `frmpsdrawers` | Drawer definitions |
| `frmpsuserdrawers` | User-to-drawer assignment |
| `frmdrawermanagement` | Active drawer management view |
| `frmpssecuritycodes` | POS-specific security codes |
| `frmsecuritycodes` | System-wide security codes |
| `frmpsreasoncodes` | Reason codes (voids, returns, discounts) |
| `frmpsticketprofilecodes` | Ticket custom field definitions |
| `frmpaycodes` | Pay code setup (tender type config, GL account) |
| `frmtouchscreencodes` | Touchscreen button definitions |
| `frmpspackagetrackingnumbers` | Package tracking # management |
| `frmpsviewstandinauths` | View standing payment authorizations |
| `frmsygiftcertificatecodes` | Gift certificate code definitions |
| `frmsycommissioncodes` | Commission code definitions |

### Purchasing / Vendor Forms
| Form | Purpose |
|---|---|
| `frmpopreqenter` | Purchase request / PO entry (full form) |
| `frmpochangepurchaseorders` | Change/cancel/reissue POs |
| `frmporeceivingsenter` | Receiving entry (all tabs + misc charges + serial prompts) |
| `frmpoquickreceivingsenter` | Simplified receiving |
| `frmporenumbervendors` | Renumber vendor IDs |
| `frmvendorcategories` | Vendor category definitions |
| `frmbatches` | Batch definitions (default batches per workgroup) |

### System Forms
| Form | Purpose |
|---|---|
| `frmcompany` | Company-wide settings |
| `frmregistration` | License and feature activation |
| `frmmenucodes` | Menu structure configuration |
| `frmuserpreferences` | Per-user preferences |
| `frmcalendars` | Seasonal date ranges |
| `frmsytaxcodes` | Tax code definitions |
| `frmtaxauthorities` | Tax jurisdiction setup |
| `frmsytimecardsenter` | Timecard entry and correction |
| `frmsytimeclock` | Time clock workstation mode |
| `frmserialprompt` | Serial prompt code definitions |

---

## 14. Reports Index (50+ Named Reports)

### Point of Sale
- Ticket Journal · Settlement Journal · Closed Layaway Journal · Closed Order Journal · Drawer Summary Journal · X-Tape · Z-Tape · Price Exceptions · Order Activity · Flash Sales

### Inventory
- Inventory Status · Inventory Analysis · Inventory History · Inventory Aging · Committed Inventory · Retail Inventory Value · Historical Valuation (Enterprise) · Consolidated Grid · Twelve-month Item History · Create Inventory · Item Report · Merchandise Analysis · Customer Price List · Bill of Material · Quick Assembly · Inventory Grid Overview · Transfer Journals · Adjustment Journals

### Purchasing
- Purchase Requests Journal · Purchase Order Form · Receivings Journal · Receiver Form · Unvouchered Receivings · Vouchered Receivings · RTVs Edit List · RTV Journals · Open Customer-specific Purchases · Purchasing Advice

### Customer / A/R
- Statements · Aging (4 periods with dunning) · Finance Charges Journal · Cash Receipts Journal · Customer Adjustments Journal · Loyalty Points Adjustments Journal · Mailing Labels/Files · Gift Registry Reports

### Sales History
- View Ticket History · Management History · Tax History · Price Exceptions History · Sales Analysis by Color/Size · MarketBasket Dashboard · Markdown History

### Timecard
- Timecards Report

### Accounting / GL
- Accounting Interface Distributions · GL Distributions by type (15+ transaction types)

### Labels / Tags
- Item Labels · Shelf Tags · Labels from Tags · Receiving Labels · PO Labels · Admission Tickets

### System
- Database Customizations · Menu Code Verification

---

## 15. API Coverage Gap Map

Counterpoint's REST API (~97 endpoints) covers a narrow slice of the full functional surface. This gap is Canary's opportunity: everything below is either unaddressed by the API or severely under-exposed.

| Domain | API Coverage | Gap |
|---|---|---|
| Items / Inventory | Partial (read-only: items, inventory by location, categories) | No price rules, no contract prices, no planned promotions, no mix-and-match rules |
| Customers | Partial (read-only: customer record, ship-to, open items, notes) | No loyalty adjustments, no cash receipts, no customer adjustments, no A/R management |
| Transactions (Tickets) | Partial (Document endpoint — read-only historical) | No live POS session, no ticket write, no drawer management |
| Purchase Orders | Partial (read-only: PO header + lines) | No receiving, no RTV, no purchasing advice, no purchasing adjustments |
| Vendors | Partial (read-only) | No vendor create/update via API |
| Physical Count | **None** | Create, enter, post entirely UI-only |
| Transfers | **None** | Transfer In / Transfer Out entirely UI-only |
| Timecards | **None** | Clock in/out, timecard maintenance entirely UI-only |
| Loyalty programs | **None** | Point earning rules, redemption, adjustments entirely UI-only |
| Finance charges | **None** | Entirely UI-only |
| A/R (cash receipts, adjustments) | **None** | Entirely UI-only |
| Labels / tag printing | **None** | Entirely UI-only |
| Multi-Site replication | **None** | Entirely UI-only |
| Offline sync (CPServices) | **None** | Entirely UI-only |
| Accounting Interface / GL | **None** | Entirely UI-only |
| Bills of Material / Quick Assembly | **None** | Entirely UI-only |
| Gift registry | **None** | Entirely UI-only |
| Planned promotions / price rules | **None** | Entirely UI-only |
| Report generation | **None** | Crystal Reports only |
| Setup / config forms (95 total) | **None** | All UI-only |
| Security / user management | Admin endpoints only | No granular function-level auth via API |

**Implication for Canary Go:** the API gets us into read-side data for core entities. Every workflow surface — receiving, physical count, transfers, loyalty management, A/R, label printing, promotion management — must be built natively by Canary, not delegated to Counterpoint.

---

## 16. UX Notes — Where Counterpoint Shows Its Age

Documented friction points from user pain-point research (see [[rapid-pos-counterpoint-user-pain-points]]):

- **Windows-native UI** — every screen is a modal form on Windows desktop; no browser, no mobile
- **Menu depth** — features buried 4–5 levels deep in a character-menu system
- **No real-time cross-store visibility** — Multi-Site replication is batch; inventory truth is always stale
- **Crystal Reports lock-in** — no ad-hoc query; every report is pre-built
- **No API for workflows** — receiving, physical count, transfers require a Windows desktop session at the store
- **Loyalty program complexity** — configuring earning rules requires navigating 3+ setup screens with no preview
- **Physical count UX** — create batch → print worksheets → enter counts → post is a sequential, blocking workflow with no mobile option
- **Pricing rule complexity** — BOGO, mix-and-match, contract, special, and promotional prices are managed in five separate forms with no unified price simulation
- **No audit trail visibility** — Canary's hash-chained evidentiary layer has no equivalent in Counterpoint
- **Timecard isolation** — timecards don't connect to transaction data; no labor-productivity-to-LP signal
