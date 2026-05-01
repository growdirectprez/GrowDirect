# Morrisons IT Architecture — Final Deliverable v1.0

**Source:** `Brain/raw/inbox/Morrisons.IT Architecture.Final Deliverable.v1.0.ppt`
**Extracted:** 2026-04-24, 104 slides
**Author of record:** IBM Business Consulting Services, 2006

---

## Slide 1

**Title:** IT Optimisation – IT ArchitectureMorrisons Supermarkets 2006

Assessing the Strategic Technology Options for Increased System Functionality

CONFIDENTIAL

---

## Slide 2

**Title:** Contents

Introduction
Business Overview and Background
Approach
Business Requirements
Implications for Current Legacy Systems
Strategic Options – Enhanced Legacy/Bespoke Development
Strategic Options – Package Implementation – Best of Breed
Strategic Options – Package Implementation – Integrated
Summary and Conclusion

Appendices:
I	Business Initiatives – Support for Optimisation and Aspiration
II	Business Initiatives – Applications to be Replaced

Presentation Title  | Confidential  |   Document ID

2

---

## Slide 3

**Title:** Introduction

---

## Slide 4

**Title:** Introduction

This document summarises the findings from the high level IT architecture review undertaken in January 2006.  The review was undertaken in a 4 week timeframe so the level of analysis has been at a very high level
All costs contained in this document are indicative only and are based on IBM experience with recent package implementations in the UK retail industry.  Costs are not to be used for anything other than budgetary purposes
This document is structured as follows:
Business Overview – summary of the business drivers for the review, the business improvement initiatives currently defined and a high level maturity profile which highlights the current level of process maturity in the business and the level to which it could be developed
Approach – brief overview of the approach and work undertaken 
Business Requirements – summary of the emerging and potential business requirements, as defined by the optimisation programmes and sessions with business management
Implications for Legacy Systems – overview of the level of support which the legacy systems provide for the emerging and potential functionality and the implications of trying to enhance the legacy systems to deliver this functionality
Strategic Options – 3 sections which summarise the options for delivering the required functionality: replacing core systems within the legacy landscape; implementing a combination of best of breed packages; implementing an ERP (integrated) package
Summary and Conclusion – brief synopsis of the key findings and the implications for the business systems going forward

Presentation Title  | Confidential  |   Document ID

4

---

## Slide 5

**Title:** Business Overview and Background

---

## Slide 6

**Title:** Business overview

Morrisons Core Business

Approximately 120 stores
Predominantly freehold properties
Standard format for stores (35-40,000 sq ft, large stock room in back)
Locations of stores all carefully selected to fit core model and customer profile
Regionally based (mainly NE)
Single range in all stores
National pricing policy
Simple processes implemented throughout the business – high level of manual input to provide flexibility
Systems developed carefully to support the core business processes but allow for manual flexibility

Safeway Acquisition

450+ Safeway stores
Predominantly leasehold
Formats vary considerably from large units to forecourt convenience stores
Locations vary to reflect development of the business (acquisitions) and different formats
National
Ranges tailored to store needs
Multiple pricing
Complex processes, sometimes over-engineered to provide flexibility to the business and reduce manual input
Systems developed to support the complex business processes and high degree of automation

Post Acquisition

378 stores
Mix of free and leasehold
Formats vary, majority are large stores but c 150 “small stores” experiencing trading issues
Locations vary as a result of the acquisition so stores have different customer profiles
National
Single range, some local tailoring
National pricing – core principle
Morrisons processes largely implemented to retain control from Morrisons head office, high degree of manual input remains
Systems essentially Morrisons apart from HR/Payroll and a few niche areas

Morrisons’ business performance has suffered as a result of the acquisition of Safeway and its integration with a first profit warning in company history, profits down to less than 1% of turnover (from nearly 7%)
The business is now looking at ways in which it can improve its performance (“Optimisation Programme”) and several initiatives have been identified which will have an impact on the IT systems

Presentation Title  | Confidential  |   Document ID

6

---

## Slide 7

**Title:** “Optimisation” programme

The overall programme objective is to drive to the following targets:

“Optimisation” Programme
Internal teams to assess ways to improve performance
Teams primarily working with in functional areas:
Trading
Distribution
Retail
Central
One cross functional team looking at “small stores” and how they can be returned to operational profitability

To achieve a 1% increase in gross margin by 2008

To reduce overhead costs by £100 million by 2008

To reduce headcount costs (FTE) by £120 million by 2008

To increase sales by 4.5% year on year (net of deflation)

To increase profits by £500 million net by 2008

Morrisons is currently working internally to determine ways in which business profitability can be improved

The majority of the initiatives will require support from IT systems

Margin

Overheads

Headcount

Sales

Profits

Presentation Title  | Confidential  |   Document ID

7

---

## Slide 8

**Title:** Approach

---

## Slide 9

**Title:** Approach

Week 4

IBM’s high level approach is split into four phases: Mobilisation, Understand Business Drivers, Define Architecture Options and Conclusions & Report:

Understand Business Drivers

Define Architecture Options

Confirm Project 
Scope and 
Objectives

High Level 
Project Plan

Arrange Meetings & Workshops

Agree criteria for comparison

Agree Deliverables

Define “aspirational” process objectives

Informal maturity profiling through workshops
with key business representatives 
and leveraging previous work (eg Finance
Capacity Review)

Compare findings with “Optimisation Review” recommendations

Enhance Legacy

Review business requirements with development team leads

Determine development options, effort and route maps

Compare architectural options

Road maps

Outline costs

Implementation challenges

Define “Optimisation” process requirements

Review documented output from the 
“Optimisation Programme”

Discuss requirements with key business
representatives to confirm understanding

Mobilisation

Weeks 2 - 3

Week 1

Best of Breed Package

Review business requirements with IBM SMEs

Determine package module options, effort and route maps

Integrated Package

Review business requirements with IBM SMEs

Determine package module options, effort and route maps

Conclusions & Report

The review has been undertaken within a limited time period and in parallel to the definition of business requirements.  Consequently, it has been limited to a high level review.  Implementation options will require further examination when business requirements and benefits have been finalised

Presentation Title  | Confidential  |   Document ID

9

---

## Slide 10

**Title:** The strategic options

To support the required business changes, investment will be required in new/enhanced systems.  Three options were investigated:
Enhanced Legacy
This option is characterised by custom development, building on the current systems in place in Morrisons
This would involve extending what the business has currently (predominantly mainframe-based applications, with some Visual Basic), re-writing the code on a different platform, or writing new code and interfacing/integrating to current systems
Where significant new functionality is to be added, the use of packaged systems is to be investigated

Best of Breed
This option evaluated the use of point solutions which are regarded as best in class for a specific set of functionality
This option is based around the Oracle Retail (Retek) solution set as this is generally regarded as the leading retail package and has the best track record in grocery retail

Integrated
This solution adopts a more integrated approach, a single solution is implemented to support as much of the business as possible
This option will be based around the SAP IS-Retail package as it is the only fully integrated solution with a track record in grocery retail

All three options have been developed at a high level and the outline architectures are defined in this pack:
Application architecture – ie the package modules to be deployed and the key links
Technical architecture – ie the hardware platforms the modules would be deployed on
Each of the three options is then evaluated at a high level, against the following:
Functionality (can the required functionality be delivered, is additional scope available for future business development)
Risk (what is the associated risk with this solution?)
Complexity (how complex is the solution set going to be?)
Scalability (will the solution easily scale, has this been demonstrated elsewhere?) 
Flexibility (how flexible will the solution be, in terms of adding/replacing functionality and its ability to integrate with other systems?)
Cost (how much will the hardware, software, effort and associated services cost?)
Supportability (how easily will this solution be supported, are skills readily available?)
Timescales (how long will it take to develop and implement?)

Presentation Title  | Confidential  |   Document ID

10

---

## Slide 11

**Title:** Business Requirements

---

## Slide 12

**Title:** Business requirements – Introduction

This summarises the business requirements, as they are currently defined
The business requirements have been summarised in two groups:
“Optimisation” – those requirements currently listed within “Optimisation” initiatives (including tactical developments) and which have some benefits attached
“Aspirational” – those requirements defined from the maturity profiles but which have not been included in the “optimisation” initiatives
The small stores workstream with the “Optimisation” programme has yet to define its requirements, but is looking like extending the “optimisation” requirements to include many of the “aspiration” elements
This section outlines:
The approach taken to define the “aspirational” requirements, the level of process change implied by the requirements and the potential implications on systems
The approach taken to define the “optimisation” requirements, the level of process change implied and the potential implications on systems
The difference between the “optimisation” and “aspirational” business requirements and the additional changes which might be needed to the legacy systems
The implications of the two levels of change on legacy systems are then assessed in the following section, although “aspirational” is treated as an extension of “optimisation”

Presentation Title  | Confidential  |   Document ID

12

---

## Slide 13

**Title:** Services

Trade

1

2

3

4

5

IBM Maturity Profiles define generic process levels which are found in retail companies – they provide a method of comparison and allow the rapid identification of key areas where benefits may be realised
Workshops with key business representatives were used to determine the approximate current level of process maturity and also identify the level to which the business would “aspire” to allow it to compete effectively
Leverage the findings from the “Finance Capacity Review” undertaken in 2005 to determine the approximate level of process maturity within the central function
This approach provides a simple, but effective, indication of the level of process change which may be required within the business and the areas where major benefits might be realised
The areas of process change are a good indication of where systems investment and change will be required

Business requirements – Defining “aspirational” requirements

Fresh

Ambient

Presentation Title  | Confidential  |   Document ID

13

---

## Slide 14

**Title:** Current

Current Processes:
Category planning undertaken across the business based on sales and buyer margin
No product level achieved margin data
National ranging with some localisation for small stores – space driven
Promotions essentially marketing or supplier driven, not category, and customer
Space is not optimised, products are spaced to fill the space

Target Processes:
Integrated processes for category, range and promotions planning
Driven by unit level sales and margin data
Promotions planned to increase category margins as opposed to sell supplier products
Clear understanding of category objectives and the role each product plays

Current Processes:
No KPIs and measures used to manage suppliers
Suppliers used on historical basis
No cost to serve in product costs
Own brand has a very high penetration with no formal PLM
Pricing to match Tesco
Supplier negotiation does not reflect category and margin requirements

Target Processes:
Supplier management structured around KPIs and category requirements
Pricing to match market and elasticity for each product
PLM to manage own brand and NPI
Cost to serve included in pricing

Current Processes:
Simplistic supply chain around manual efficiency within DC
No inclusion of store requirements in planning and scheduling
Bulk pick and despatch
Transport planned manually to reflect simple “shuttle” type runs to big stores – no schedules for small stores
Limited back haul – recharge suppliers
No E2E unit stock management / visibility 
Target Processes:
Efficient supply chain operations to reflect store demands and automation
Store picking, despatch/load management
Transport planned and managed in integrated way with store and DC
Bach haul integrated to category needs
Full E2E stock management / visibility

Current Processes:
Multiple EPOS systems - not integrated
Marketing material not store specific
Manual ordering for majority of store range
Financial processes for stock management
Stores still GRN all deliveries from DCs
Manual processing in store back office
Stores well managed, industry leading OSA, good customer service – but very manual
Stores carry excessive stocks to drive OSA
Is all waste and markdown captured ?
Target Processes:
Maintain OSA, customer service levels
Increased automation to reduce manual effort
Supply chain improvements to reduce stock holding and associated manual activities in stores
Integrated unit stock management, waste and markdown systems – full visibility
Scorecards to drive store management

Aspire to

Ambient

Fresh

1

2

3

4

5

Business requirements – “Aspirational” processes for target supply chain processes and their implications for business change

Presentation Title  | Confidential  |   Document ID

14

---

## Slide 15

**Title:** Current

Current Processes:
2 processes still operating for HR and payroll
Ts&Cs standard
Fixed schedules operated, especially in stores

Target Processes:
Harmonisation to standardise on single system
Flexible staff scheduling

1

2

3

4

5

Current Processes:
Service POs raised manually, not recorded on systems
No accruals for Services POs
Manual matching for Service invoices, long paper chase around the business
Trade orders raised semi-automatically and on systems
Limited EDI to suppliers for orders only
All orders are manually matched on the system
No use of EDI for remittances or invoices
Supplier payment terms are very long

Target Processes:
Service POs to be raised on core financials to support accruals and 3 way matching on automated basis
Integrate source ordering systems
EDI extended to all suppliers and all transactions
Full automated 3-way matching for all invoices
Self billing for best suppliers

Current Processes:
Sales recording and reporting still requires significant manual input and re-keying 
Cash management process has been automated between HO and store, although still significant staff levels in store
HO processes are not fully integrated to bank reconciliation
All payments are still made manually via cheque
Assets recorded on a variety of systems around the business, manually input to financials and depreciation
Target Processes:
Fully automated sales recording and reporting
Fully integrated bank reconciliation / treasury processes
Automated payment processing via BACS etc
Asset management systems linked to central ledgers to facilitate streamlined processes

Current Processes:
GL requires significant levels of manual input and reconciliation – reliance on Excel
Reconciliation processes are manual and prone to error
No budgeting/planning and no regular reporting processes to monitor spend
Management reporting very limited



Target Processes:
Fully integrated GL with automated reconciliation
Financial planning and budgeting with regular reporting/forecasting cycles
Emphasis on cost management
Management reporting to add value to the business beyond financial management

Aspire to

Trade

Services

Business requirements – “Aspirational” processes for target financial processes and their implications for business change

Presentation Title  | Confidential  |   Document ID

15

---

## Slide 16

**Title:** Current

Current Systems:
No category planning systems support – although Trading Information System provides sales based data
No product level achieved margin data
Planogram systems for store ranging – essentially a manual process
No systems to support store specific ranging, promotions analysis/management
Product and stock systems are not well integrated
Target Systems:
Integrated systems for category, range and promotions planning
Sales and space optimisation and planning systems – fully integrated
Provide full unit level sales and margin data
Support customer demographics and store characteristics all recorded / maintained

Current Systems:
Systems provide basic master file support – no store stock, margin, no attributes, no COO etc etc
No cost to serve in product costs
No supplier analysis and KPI management systems
No PLM/NPI systems support
Limited trade management systems to support supplier deal mgmnt
Core systems inflexible
Target Systems:
Core master files to support all requirements for product / supplier
Integrated supplier management against agreed KPIs
Full deal management systems
Integrated support for PLM and NPI
Links to suppliers (via MSD)

Current Systems:
No supply chain planning systems
No demand forecasting systems
Replenishment is essentially manual
Supplier ordering largely manual – suggested orders produced for review and authorisation
No unit stock management at store level, no history retained
Poor warehouse management systems
No transport planning systems
Target Systems:
Transport planning integrated to supply chain to optimise transport costs
Integrated warehouse management systems
Stock management integrated to stores
Forecasting to drive supplier replenishment and shared with suppliers
Automated store replenishment / ordering

Current Systems:
Multiple EPOS systems - not integrated
EPISYS for POS material - generic
Manual ordering for majority of store range
Manual processes for stock management
Stores still receiving all deliveries from DCs
Manual processing in store back office
Stores well managed, industry leading OSA, good customer service
Stores carry excessive stocks to drive OSA
Is all waste and markdown captured ?
Target Systems:
Consolidated/integrated EPOS systems
HHT based systems for stock and admin
Stock management systems integrated across supply chain, remove lot of store processes
Integrated waste and markdown systems
MIS / Scorecards to drive store management

Aspire to

Ambient

Fresh

1

2

3

4

5

Business requirements – “Aspirational” systems for target supply chain processes

Presentation Title  | Confidential  |   Document ID

16

---

## Slide 17

**Title:** Current

Current Systems:
2 payroll systems, reflect 2 legacy businesses
No staff scheduling

Target Systems:
Harmonisation to standardise on single system
Staff scheduling system

1

2

3

4

5

Current Systems:
No integrated POP systems for services invoices across whole business
No invoice matching system for services invoices
POP largely manual for trade goods
3 way invoice matching for trade goods but requires manual input of invoices
No accruals for services invoices

Target Systems:
Full integrated POP systems for whole business (Peoplesoft + some front end input systems (eg Archebus, which are integrated)
Automated accruals for services orders
Full 3 way automated matching for all orders (P/soft)
EDI implemented for all financial documents and transactions

Current Systems:
BCP system for cash management. Not integrated to financials for full bank reconciliation
Numerous manual systems to record and report sales 
Payments made by cheque from legacy ledger
Limited asset management systems (by function) and not integrated to core financial systems
Depreciation calculated manually

Target Systems:
Peoplesoft implemented for AR and Treasury, integrated to BCP to facilitate automated reconciliation
All sales reporting driven from EPOS and integrated
Automate payment processes from Peoplesoft
Asset management systems where suitable, integrated to central ledgers to automate maintenance of financial records and depreciation

Current Systems:
Legacy GL not integrated
Excel and manual journals
No planning and budgeting systems
Excel used for limited management reporting




Target Systems:
Peoplesoft GL integrated to other ledgers
Financial planning and budgeting system to facilitate processes
MIS for single reporting and analysis – one version of the truth

Aspire to

Trade

Services

Business requirements – “Aspirational” systems for target financial processes

Presentation Title  | Confidential  |   Document ID

17

---

## Slide 18

**Title:** Services

Trade

1

2

3

4

5

In October 2005, Morrisons started an internal programme to identify and implement process and systems improvements which would help it deliver and additional £500m of profit per annum
The recommendations from the “Optimisation” programme have been reviewed with the functional Directors and key business representatives to understand the process and systems implications
Process changes were then checked against the Maturity Profiles to give an approximate indication of how they will contribute towards the “Aspirational” process targets
The results of this high level analysis are shown on the following slides
Some optimisation areas had poorly defined process requirements and there is considerable potential for overlap between the small stores initiative and those from the functional areas
The small stores initiative is still not finalised, however, many of its emerging requirements are listed under ‘’Aspirational’’

Business requirements – ”Optimisation” Programme

Fresh

Ambient

Presentation Title  | Confidential  |   Document ID

18

---

## Slide 19

**Title:** Business requirements – Current “optimisation” initiatives delivering a claimed total of £388m benefits

Business Area

Initiative

Business Requirements

Systems Implications

Trading

Margin              £50m
Other Costs     £10m

Price and Promotions Management
Range and Merchandising Changes

EPOS sales based (achieved) margin
Promotion management system
SMS enhancements

Recording and tracking of promotions, analysis of promotions and modelling of future promotions
Unclear on process changes

Distribution

Enterprise       £10m
Mayflower       £56m
Other Costs    £37m

Enterprise
Mayflower
Transport Planning
Earlier Deliveries
Managing Backhaul

Network restructuring
Depot closures
Planning of transport schedules to support store needs
Other changes to be defined

Stores

Labour            £50m

Reduction in store labour costs and FTEs

In store process review
Automation to reduce manual effort
Small store review

4th wave
Additional disk run
Produce into Tranman
Backhaul management system
Transport planning system (Paragon)
Commader4 / Swisslog

Suggested order on order pad for all products
Production plans
Rota automation
HHT scanning enhancements
HHT stockcounting for SMS

Central

Costs               £25m
Small Stores £150m

Process efficiency and cost reduction

Finance process improvement
Services and trade
Payroll harmonisation
Other areas to be identified

Peoplesoft GL and AP for Services
Peoplesoft AP for Trade
Peoplesoft Payroll
MIS

Presentation Title  | Confidential  |   Document ID

19

---

## Slide 20

**Title:** Current

Initiatives:
Range and space planning improvements – using spreadsheets to deliver improvements in store ranges for small stores
Promotions management system to track promotions, record sales and other factors and to analyse effectiveness
Category planning will be tightened through use of spreadsheet analysis

Systems Implications:
Excel developments
Promotions management system – in house would require extensive changes to record sales history, maintain promotions details, track sales and other information against promotions, complex statistical analysis and modelling techniques – package may be better

Initiatives:
Improved buying and margin management
Track deals to maximise returns






Systems Implications:
If genuine unit achieved margins then changes are huge, impact on all product and supplier areas, plus record all stock transactions at unit level, plus maintain records at every SKU/location
Supplier deals enhancements and excel

Initiatives:
Network reduction – close DCs
Network strategy – new sites
Transport planning and tracking
Earlier deliveries to small stores
Improved back haul management
Small stores to improve supply chain to help stores with timed deliveries, picks to support stores, roll cages etc

Systems Implications:
Paragon transport planning and Qualcomm tracking
Changes to legacy to support earlier disk ordering run and introduce more picking waves
New warehouse management systems
Integrated unit stock control into the stores

Initiatives:
Reduction in store labour charges / costs
No specification of how this will be achieved
Small stores to further reduce admin and stock-handling in stores





Systems Implications:
Numerous EPOS changes to tighten up on processing, prevent use of wrong card types
EPISYS changes to tailor POS to each store
HHT and other enhancements to reduce manual effort in stores
Integrated unit stock control into all stores

Ambient

Fresh

The published initiatives are claiming a potential £388m of benefits*

1

2

3

4

5

* Including Finance on the following slide

Aspire to

Initiatives

Business requirements – “Optimisation” initiatives for supply chain processes and their implications on legacy systems

Presentation Title  | Confidential  |   Document ID

20

---

## Slide 21

**Title:** * Including Supply Chain on the previous slide

Initiatives:
Harmonisation to standardise and simplify payroll
Small stores – flexible staff scheduling

Systems Implications:
Remove legacy payroll and HR systems
Labour scheduling system for all stores

Current

1

2

3

4

5

Initiatives:
New AP/POP for Services
New SP for Trade
Automated accruals
(Scanning / Servin for invoice processing – reduce manual effort)
(Extend EDI to all trade suppliers for orders)


Systems Implications:
Peoplesoft AP, POP and Invoice Match systems to support trade and services areas of the business
Continued implementation of previous changes to support scanning of all invoices onto Content Manager and their input to finance via OCR
Continued extension of EDI to all suppliers for orders only

Initiative:
Assumes that Peoplesoft AR and treasury are implemented to enhance current processes and support full automated bank reconciliation
Assumes that Peoplesoft Fixed Asset module is implemented and interfaced to existing asset management systems (eg Tranman) to capture asset records and calculate depreciation

Systems Implications:
Peoplesoft AP and treasury modules
Integration to BCP
Integration of sales recording (including flash sales) to EPOS
Peoplesoft FA module for assets and depreciation
Possible asset management systems in areas which have high capex spend (eg stores, transport and IT)

Initiative:
Assumes implementation of all remaining Peoplesoft modules to provide full integration to the GL and support auto-reconciliation
Peoplesoft GL will provide basic maintenance of budgets and support management reporting against them
Excel for management reporting

Systems Implications:
Peoplesoft does not support high quality planning and forecasting processes as it is relatively inflexible and cannot support modelling / what-if analysis
Complex excel system for planning and budgeting
Management Information system

Aspire to

Trade

Initiatives

Level from implementing
all Peoplesoft modules

The published initiatives are claiming a potential £388m of benefits*

Business requirements – “Optimisation” initiatives for financial processes and their implications on legacy systems

Presentation Title  | Confidential  |   Document ID

21

---

## Slide 22

**Title:** Business requirements – There are still significant areas for further benefit

1

2

3

4

5

Comparing the level of process maturity resulting from the “Optimisation” initiatives to the “Aspirational” level highlights significant areas for improvement across the whole business
At the time of this review some of the ‘’Optimisation’’ initiatives had been finalised
However, the ‘’small stores’’ initiative had not finalised its requirements

The following slides highlight the major areas for improvement beyond the “Optimisation” programme, how they would help achieve £500m profits increase and the potential systems implications (    = major contribution)
The ‘’small stores’’ initiative is still defining its requirements and is beginning to highlight the areas we have highlighted as ‘’Aspirational’’, e.g. store range and space optimisation, category management, sales based EPOS margin, warehouse management, stock management and flexible working in stores

Presentation Title  | Confidential  |   Document ID

22

---

## Slide 23

**Title:** Business requirements – Beyond “Optimisation” – Trading initiatives which should be considered

Initiative

Business Requirements

Systems Implications

Category Planning

  Margin increase
  Sales increase

Core product & inventory system (maintain location/SKU stocks and capture all transactions)
Enhanced product and supplier files – contain all information and attributes to manage products and suppliers effectively
Unit margin system
Management information system
Supplier management system
Deal management system
Promotion management and analysis system

Understand role each category plays in the overall customer offer and function each individual product plays within the category
Manage each category in terms of achieved margin, both at category and product levels
Manage suppliers within overall categories
Manage trade funds (LTAs, rebates etc) within category plans and ensure that all funds are recovered and maximised
Manage promotions within category plans

Store Space and Range Optimisation

  Sales increase
  Margin increase

Range and space optimised local store space, sales and customer demographics
Ability to control multiple ranges across the end to end supply chain
Planograms available to all stores
Potential to support local range requests from retail operations management
Planograms to be adhered to throughout the supply chain

Galleria range and space optimisation
Product file enhancements
Core product & inventory system
Enhancements to RIS to maintain inventory of store space and fitments
SMS to adhere to planograms
New System for Customer profiles
Management information system
Planogram distribution system

Sales Based EPOS Margin Control

-  Margin increase

Margin to be tracked and managed at unit and achieved level
Supports category management
Manage Margin cost drivers
Warehouse/Store shrinkage
Markdowns
Unfunded promotions

Core product and inventory system
Stock ledger (summarises stock transactions)
Management information system
Product file enhancements

Presentation Title  | Confidential  |   Document ID

23

---

## Slide 24

**Title:** Business requirements – Beyond “Optimisation” – Distribution initiatives which should be considered

Initiative

Business Requirements

Systems Implications

Stock Management

  Margin increase
  Overhead reduction
  FTE reduction

Core product & inventory system (maintain location/SKU stocks and capture all transactions)
Enhanced product file
Integrated WMS system
Management information system
Use of RF/HHTs wherever possible – order pad, suggested orders, stock counting, waste management

Ability to manage, track and gain visibility of all stock in all locations
Ability to view and manage stocks across and between all locations to reduce the levels of safety stock holding
DC’s to move to perpetual inventory
Manages all stock movements through the business eg waste, shrink
Reduce levels of manual stock handing in stores (no GRN from DC, single handling)

Integrated and Transport Warehouse Management

  Overhead reduction
  FTE reduction

Integrate all warehouse processes from goods in to goods out – driven by requirements of all stores (especially small)
Move to just in time picking by load as directed by the Transport plan
Transport plan to optimise store service and fleet utilisation
All DC operations optimised to balance cost and service

Integrated WMS system
Integrated transport planning system
RF controlled WMS processes
Qualcomm vehicle telematics and tracking system
Integrated to company stock management system (See above)
Management information system

Forecasting and Replenishment 

  Overhead reduction
  Margin increase

Demand forecasting to more accurately predict product demand through the supply chain
Supplier re-ordering to reflect demand forecast and actual stocks – allow reduction in safety stocks
Store re-ordering to reflect forecast demand and actual stocks
Share information along the supply chain, including with suppliers

Demand forecasting system
Supplier re-ordering systems
Store replenishment and allocation systems
MSD enhancements to share information with suppliers

Presentation Title  | Confidential  |   Document ID

24

---

## Slide 25

**Title:** Business requirements – Beyond “Optimisation” – Retail initiatives which should be considered

Initiative

Business Requirements

Systems Implications

Stock Management
(See Distribution)

  FTE reduction 
  Overhead reduction
  Margin increase

Core product & inventory system (maintain location/SKU stocks and capture all transactions)
Enhanced product file
Integrated WMS system
Management information system
Use of RF/HHTs wherever possible– order pad, suggested orders, stock counting, waste management

Ability to manage, track and gain visibility of all stock in all stores
Stores to implement a more balanced method of stock counting for all ranges
Manages all stock movements through the business eg waste, shrink
Reduce levels of manual stock handing in stores (no GRN from DC, single handling)

Flexible Staff Scheduling

  FTE reduction 
  Overhead reduction

Move to more flexible operations in stores from rostering to multiple skills
Flexible rostering to allow management to match demand to staffing levels and reduce overall operating costs in the stores
Multi-skilling of store staff to better support store operating requirements

Labour scheduling system
HR system to record staff skills, contracts etc

Reduced Administration 

  FTE reduction 
  Overhead reduction

Review all processes in stores to see how they can be optimised to reduce the level of manual input in stores (eg cash, HR, recruitment, training)

Use of systems to integrate to HO processes and reduce the manual effort in stores

Presentation Title  | Confidential  |   Document ID

25

---

## Slide 26

**Title:** Business requirements – Beyond “Optimisation” – Central initiatives which should be considered

Initiative

Business Requirements

Systems Implications

Management Information System

  Margin increase
  Overhead reduction
  FTE reduction

Core management information database
MI tools for reporting and analysis
Data mining toolset for analysis / trends / patterns
ETL tools for loading the data and linking back to legacy

Integrated MI reporting – across the business – “single version of the truth”
Report and manage the business against common KPIs / scorecards
Manage key revenue and cost drivers
Flexible user reporting tools
Data mining tools for specific analysis (eg fraud detection on EPOS transactions) and also trend analysis

Finance BPR

  FTE reduction 
  Overhead reduction

Optimise all finance processes to reduce cost and improve service levels
Key emphasis on reducing store input to all processes

Integrated financial ledger and transaction system (Peoplesoft)
Integrated to all other finance systems (eg BCP)
EDI to support all financial transactions (eg remittance, invoice)
Integrated asset management systems

Central Process BPR

  FTE reduction 
  Overhead reduction

All HR and staff processes reviewed E2E to reduce manual effort at all levels, especially the stores
All overhead processes reduced to remove or reduce the level of manual input

HR/training/recruitment systems integrated at all levels of the business
Admin support systems (eg Intranet) to reduce costs and manual processing

Presentation Title  | Confidential  |   Document ID

26

---

## Slide 27

**Title:** Current

Ambient

Fresh

1

2

3

4

5

* Including Finance on the following slide

Aspire to

Initiatives

To deliver these improvements will require significant changes

Further Developments:
Category planning based on unit margin and sales information, also to include customer segmentation
Range and space planning to include unit level margin information (ideally at store level)
Promotions planning to include unit level margin information – allow promotions to be assessed and managed to increase cash profit

Potential Systems:
Unit level stock control – will drive the replacement of the current product file as too complex to deliver on the current platform
Category planning system
MIS system to support analysis
(Promotions management and Galleria included in optimisation initiatives – use sales)

Further Developments:
Supplier management processes to be defined E2E and include SLAs
Pro-active management of deals, LTAs etc to maximise return and ensure all entitlements are claimed
Supplier negotiations based on cost to serve and to include back haul etc – requires E2E data

Potential Systems:
Supplier management systems to highlight performance on SLA/KPIs
Trade management systems to record all deals/contracts and monitor/analyse on going situation
MIS system across whole business

Further Developments:
E2E supply chain planning to manage stock levels and movements through supply chain
Automated sales based replenishment for fresh and ambient/frozen
Forecasting based on historical sales and stock levels – manual input to support local variations
WMS processes optimised for overall supply chain efficiency and costs
Potential Systems:
New WMS to provide flexibility to improve warehouse operations and reduce costs
Advanced forecasting and replenishment systems to utilise sales history
MSD enhanced to share forecasts with suppliers
Supply chain planning to help optimise stocks across whole supply chain

Further Developments:
E2E processes, especially supply chain and administration to optimise in store processes
Full integration of in-store stock management systems into central stock and supply chain management systems
Removal of in-store ordering processes
Focus on customer service and shelf stocks
Increase flexible scheduling of staff to reduce payroll costs
Potential Systems:
Integrated EPOS systems across the store
Integrated store stock management systems with the emphasis on stock accuracy and shelf replenishment
Flexible labour scheduling systems
Full integration of all in-store systems to all HO systems

Business requirements – Beyond “Optimisation” – Supply chain processes and their implications for systems

Presentation Title  | Confidential  |   Document ID

27

---

## Slide 28

**Title:** Current

Further Developments:
Flexibility in staff scheduling
Use of E2E processes to reduce admin across the business
Potential Systems:
Staff scheduling systems
Intranet to share information etc
Workflow to enhance processes

1

2

3

4

5

Further Developments:
Integrated POP processes in all areas of the business
EDI extended beyond ordering to include all elements of the invoicing and settlement process
Possible integration into buying clubs for service areas




Potential Systems:
Extend EDI to include invoices, remittance advices and other supplier related documents – reduce all manual input to near zero
Implement self billing/invoicing on suppliers with excellent delivery records
Integrate all buying and POP systems
Potential integration to external buying systems

Initiative:
Move away from cheques as main settlement process
Asset management in all areas of the business






Potential Systems:
Implement automated payment systems for as many suppliers as possible
Implement asset management in all areas of the business which have significant capital equipment (eg Retail, IT) and integrate to the Peoplesoft FA module

Initiative:
Advanced planning and budgeting using systems to help develop models etc, plus re-forecasting
Systems allow dissemination of plans and actuals to the business to facilitate faster reporting and forecasting



Potential Systems:
Advanced financial planning systems

Trade

Level from implementing
all Peoplesoft modules

To deliver these improvements will require significant changes

Business requirements – Beyond “Optimisation” – Financial processes and their implications for systems

Aspire to

Initiatives

Presentation Title  | Confidential  |   Document ID

28

---

## Slide 29

**Title:** Implications for Legacy Systems

---

## Slide 30

**Title:** Legacy systems implications – Current level of functional support

Morrisons Legacy Architecture

Legacy systems mapped onto a functional grid to indicate which systems are used in which areas of the business
Good format for highlighting quality of systems support by areas

Morrisons Legacy by Process

Legacy systems re-mapped onto the IBM grocery retail process model
Good format for highlighting the quality of systems support for key business areas within the business – compatible with the maturity profile format

IBM Component Business Model

Defines a proven process model for retail businesses – adapted for grocery
Excellent format for highlighting areas where systems support for business processes is missing or could be enhanced

The current legacy systems are generally accepted as providing low levels of functional support to the business – partly deliberate as the Morrisons philosophy was to keep things simple with a high level of manual intervention
In addition the legacy systems are not very well integrated and are based on old file systems and development languages which further reduces the potential to modify them to support the defined business requirements
The legacy systems were assessed against the “Optimisation” and “Aspiration” requirements outlined in the previous section – RAG analysis for degree of functional support and level of manual input

Presentation Title  | Confidential  |   Document ID

30

---

## Slide 31

**Title:** Legacy systems – Level of functional support for “Optimisation” processes mapped against IBM Component Business Model

Manual process in most retail businesses

Process out of scope for this review

Good functional support – minimal changes required

Functional support,  manual input required

Legend

Poor or no functional support and high degree of manual input

Presentation Title  | Confidential  |   Document ID

31

---

## Slide 32

**Title:** Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Legacy systems – Level of functional support for “Optimisation” processes mapped against Morrisons functional structure

Presentation Title  | Confidential  |   Document ID

32

---

## Slide 33

**Title:** Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Legacy systems – Level of functional support for “Optimisation” processes mapped against retail best practice process model

Presentation Title  | Confidential  |   Document ID

33

---

## Slide 34

**Title:** Legacy systems – Functional support for “Optimisation” initiatives

The “heat maps” on the previous 3 slides highlight significant areas where the legacy systems will not supporting the target business requirements 
Key areas of weakness include:
Product and price master files – where significant enhancements are required to support the additional information requirements
Sales – where additional data, including historical sales, is required to support promotions management
Promotions management where there is no support for the stated requirements, which will be Excel based for ‘’Optimisation’’
Unit margins – where additional work is needed to ensure that all finance transactions are captured and reported
WREP and SMS2 replenishment systems – where significant amendments are needed to help move the business forward 
Transport planning – where new systems are required to support small stores and to deliver benefits from the transport and shipping costs
Category management – where additional reporting is needed to help drive margin, supported by Excel spreadsheets to undertake analysis
Finance – where the legacy systems will be replaced with Peoplesoft
Management information – where either a new system is needed to replace the Trading Information System to deliver a single view across the whole business
The legacy systems can be enhanced in most areas to support the stated requirements, although the product and price master files will require redevelopment

Presentation Title  | Confidential  |   Document ID

34

---

## Slide 35

**Title:** Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Legacy systems – Level of functional support for “Aspiration” processes mapped against Morrisons functional structure

Presentation Title  | Confidential  |   Document ID

35

---

## Slide 36

**Title:** Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Legacy systems – Level of functional support for “Aspiration” processes mapped against retail best practice process model

Presentation Title  | Confidential  |   Document ID

36

---

## Slide 37

**Title:** Legacy systems – Functional support for “Aspiration” initiatives

The “heat maps” on the previous 2 slides highlight significant areas where the legacy systems will not supporting the future business requirements 
Additional key areas of weakness include:
Category management where new development will be needed to support the enhanced management of categories by margin and contribution
Promotions management where new developments will be needed to track all promotions, analyse their performance and allow the modelling of future promotion options
Stock and inventory management where new development will be needed to support the capture of all stock transactions and their accurate processing to maintain central stock data
Warehouse management – complete replacement of Swisslog (or its re-implementation) to support the requirements fro integrated warehouse management and transport planning
Range and space optimisation – where Galleria will need to be implemented and integrated to support the planning if ranges for all non-standard stores in the business
Supplier master files and associated systems will have to be redeveloped/replaced to support the requirements for supplier management and deal management
Forecasting and replenishment/allocation – where new systems will be needed to support the automated forecasting and replenishment of stock throughout the supply chain, a swell as major enhancements to other systems to integrate the data and share with suppliers
EDI – major enhancements to support the automated transfer of all financial information between suppliers and Morrisons
The majority of the requirements are very complex and may best be supported by the implementation of packaged solutions
The legacy systems do not provide a sound platform for supporting the long term requirements of the business – significant replacement will be required for developments beyond a 12 month timeframe

Presentation Title  | Confidential  |   Document ID

37

---

## Slide 38

**Title:** Legacy systems – Additional, non-functional concerns

The review has highlighted a number of other non-functional issues relating to the legacy systems:

Program Code

Program Limits

File Sizes

Complexity

Staff

Risk

Flexibility

Scalability

Code is generally very old and an in a little used language for which skills are very scarce
Core code is now 20 – 30 years old, has been modified extensively and is increasingly hard to change

Modifications regularly cause problems with working storage limits being exceeded
New changes will repeat this problem and cause program re-writes

Core product file has no spare space – new requirements will force an extension to the file length
Last product file extension required the modification of c500 programs and took 6 months for 10 staff

Significant requirements demands complex functionality and integration
The level of man days to modify existing systems are very high – raise question of re-writing

There are very limited staff with the experience of your programming language
Enhancements have to rely on the limited pool of internal staff or re-write to different platform

No documentation available, relies on limited knowledge held by a few key staff
Risk of making complex changes are very high, will increase cost and timescale, or re-write

The systems are increasingly difficult to modify, requests from the business all require bespoke modifications
The underlying architecture does not support SQL, obtaining information is very hard and needs bespoke work

Legacy systems are regarded as scalable by the development teams, but have been changed for SW
The batch schedules are complex with key inter-dependencies, changing schedules will be difficult

Architecture

There are inherent limitations within the current systems design, eg “old number – new number”
These will make it extremely hard to integrate packages and will have to be removed – increases level of change

Presentation Title  | Confidential  |   Document ID

38

---

## Slide 39

**Title:** Legacy systems – Not a viable platform for long term development

Major redevelopment / re-write of core systems

The legacy systems can be enhanced in most areas to support the “BAU” and “Optimisation” requirements 
However, the following systems will have to be re-developed or developed:
Product and price management 
Sales recording, history and analysis
Management information system
Transport planning
Financial management (Peoplesoft)
This re-development will be required within the next 12 months

Our review has highlighted a number of other areas where significant systems investment will be required:
Range and space optimisation (Galleria)
Integrated unit stock and margin management (all locations) 
Warehouse management
Category planning and supplier management
Deal management (recovering all LTAs etc)
Forecasting, allocation and replenishment

The use of packaged solutions should be considered for all of these areas – even within the enhance legacy options

Presentation Title  | Confidential  |   Document ID

39

---

## Slide 40

**Title:** Legacy Enhancement Option

---

## Slide 41

**Title:** Legacy enhancement – Level of functional support for “Optimisation” processes mapped against Morrisons functional structure

Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Presentation Title  | Confidential  |   Document ID

41

---

## Slide 42

**Title:** Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Legacy enhancement – Level of functional support for “Optimisation” processes mapped against Morrisons functional structure

Presentation Title  | Confidential  |   Document ID

42

---

## Slide 43

**Title:** Legacy enhancement – ‘Optimisation’ development in man days

Initial estimates have been derived from interviews with WM IT development team leads (estimates for design and testing) with additional time estimated for design and implementation (based on experience in Morrisons over last 12 months). EPOS has been excluded – assuming that the team will implement 2 releases per year. Roll-out days include store training across 400 stores (see those marked *).   No contingency is included

| Application Area | Design | Build/Test | Dev Total | Roll-out | Total |
| --- | --- | --- | --- | --- | --- |
| Promotion Planning (Excel) | 30 | 50 | 80 | 25 | 105 |
| Order Pad on HHT | 400 | 500 | 900 | 800* | 1,700 |
| Suggested Order on HHT | 50 | 100 | 150 | 400* | 550 |
| Store Stock Movement on HHT | 200 | 300 | 500 | 400* | 900 |
| Product Master File & Sales History (Bespoke) | 1,500 | 3,000 | 4,500 | 200 | 4,700 |
| MIS (Bespoke) | 1,500 | 2,775 | 4,275 | 450 | 4,725 |
| Finance (Peoplesoft package) | 1,200 | 2,400 | 3,600 | 225 | 3,825 |
| Stock Transactions – Financial Margin | 100 | 200 | 300 | 25 | 325 |
| Product Development (Bespoke) | 225 | 450 | 675 | 225 | 900 |
| Transport Planning (Paragon package) | 600 | 975 | 1,575 | 100 | 1,675 |
| Category Management (Excel) | 225 | 450 | 675 | 225 | 900 |
| SMS2 Enhancements | 400 | 725 | 1,125 | 125 | 1,250 |
| SMS Enhancements | 300 | 600 | 900 | 90 | 990 |
| WREP/WHAM etc Enhancements | 400 | 600 | 1,000 | 100 | 1,100 |
| POP Forecasting Enhancements | 75 | 150 | 225 | 25 | 250 |
| EPISYS / Store Systems (excl EPOS) | 250 | 400 | 700 | 400* | 1,100 |
| Total Man Days | 7,455 | 13,725 | 21,180 | 3,815 | 24,995 |
| Total Man Years | 33 | 61 | 94 | 17 | 111 |

Presentation Title  | Confidential  |   Document ID

43

---

## Slide 44

**Title:** Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Legacy enhancement – Level of functional support for “Aspiration” processes mapped against Morrisons functional structure

Presentation Title  | Confidential  |   Document ID

44

---

## Slide 45

**Title:** Legend

Very good functional support – limited changes

Good functional support – large number of small changes

Good functional support – significant changes

Poor or no functional support – Major changes or re-write/ replace

Legacy enhancement – Level of functional support for “Aspiration” processes mapped against Morrisons functional structure

Presentation Title  | Confidential  |   Document ID

45

---

## Slide 46

**Title:** Legacy enhancement – Application architecture highlighting bespoke and packaged developments required to support “Aspirational” requirements

Presentation Title  | Confidential  |   Document ID

46

---

## Slide 47

**Title:** Legacy enhancement – Application architecture highlighting bespoke and packaged developments required to support “Aspirational” requirements

Presentation Title  | Confidential  |   Document ID

47

---

## Slide 48

**Title:** Legacy enhancement – ‘Aspirational’ development in man days

Indicative estimates have been derived from IBM experience of implementing systems for these areas in other retail organisations.  Man days include a mix of external and internal staff, typically between 1:2 and 1:3 internal v external, depending on the level of integration required
MIS enhancements have been assumed to be 100% of the “Optimisation” development on the basis that the database is being extended to cover all of the additional functional areas.  Roll-out estimates include stores and have assumed a number of days per location (for 400 stores, marked with an *).  No contingency is included

| Application Area | Design | Build/Test | Dev Total | Roll-out | Total |
| --- | --- | --- | --- | --- | --- |
| Category Planning (Bespoke) | 900 | 2,250 | 3,150 | 450 | 3,375 |
| Promotion Planning (Package) | 900 | 2,025 | 2,925 | 400 | 3,150 |
| Range Optimisation (Galleria package) | 500 | 1,260 | 1,760 | 215 | 2,210 |
| Macro Space and Store Clustering (Galleria package) | 500 | 1,260 | 1,760 | 215 | 2,210 |
| Unit Stock Control and Achieved Margin (Bespoke) | 1,900 | 2,900 | 4,800 | 600* | 5,400 |
| Stock Forecasting, Allocation, Replenish (Package) | 1,500 | 2,500 | 4,000 | 2,250* | 6,250 |
| Warehouse Management (Package) | 2,000 | 3,800 | 5,800 | 1,200 | 7,220 |
| Supplier Management (Bespoke) | 700 | 1,200 | 1,900 | 125 | 2,025 |
| Staff Scheduling (Package) | 600 | 1,200 | 1,800 | 2,000* | 3,800 |
| EDI for Finance (Package) | 300 | 600 | 900 | 1,800 | 2,700 |
| MSD Enhancements (Bespoke) | 450 | 900 | 1,350 | 200 | 1,550 |
| Administration and Intranet (Domino package) | 400 | 725 | 1,125 | 500* | 1,625 |
| MIS Enhancements (Bespoke) | 1,500 | 2,775 | 4,275 | 450 | 4,725 |
| Total Man Days | 12,150 | 23,395 | 35,645 | 9,110 | 46,240 |
| Total Man Years | 54 | 104 | 158 | 40 | 206 |

Presentation Title  | Confidential  |   Document ID

48

---

## Slide 49

**Title:** Legacy enhancement – ‘Optimisation’ cost implications

| Application Area | Internal Days | External Days | Internal £000’s | External £000s | Total £000s |
| --- | --- | --- | --- | --- | --- |
| Promotion Planning (Excel) | 105 | 0 | 35 | 0 | 35 |
| Order Pad on HHT | 1,520 | 180 | 455 | 215 | 670 |
| Suggested Order on HHT | 520 | 30 | 155 | 35 | 190 |
| Store Stock Movement on HHT | 800 | 100 | 240 | 120 | 360 |
| Product Master File & Sales History (Bespoke) | 2,350 | 2,350 | 705 | 1,880 | 2,585 |
| MIS (Bespoke) | 2,363 | 2,363 | 710 | 3,425 | 4,135 |
| Finance (Peoplesoft package) | 1,148 | 2,678 | 345 | 3,880 | 4,225 |
| Stock Transactions – Financial Margin | 163 | 163 | 50 | 130 | 180 |
| Product Development (Bespoke) | 450 | 450 | 135 | 360 | 495 |
| Transport Planning (Paragon package) | 1,173 | 503 | 350 | 690 | 1,040 |
| Category Management (Excel) | 900 | 0 | 270 | 0 | 270 |
| SMS2 Enhancements | 1,250 | 0 | 375 | 0 | 375 |
| SMS Enhancements | 495 | 495 | 150 | 395 | 445 |
| WREP/WHAM etc Enhancements | 550 | 550 | 165 | 440 | 605 |
| POP Forecasting Enhancements | 125 | 125 | 40 | 100 | 140 |
| EPISYS / Store Systems (excl EPOS) | 820 | 280 | 245 | 335 | 580 |
| Total Man Days | 14,730 | 10,265 | 4,425 | 12,005 | 16,430 |
| Total Man Years | 65 | 46 |  |  |  |

Cost estimates are derived from the man day estimates on the previous slide.  Man days have been split approximately between internal and external development staff to reflect the type of work being undertaken (ie package based will be 70% external, bespoke will be predominantly internal).  Internal staff have been costed at a notional £300 per day.  External staff have been costed at £800 per day for contractors and a mix of £1200 and £1450 for vendors and implementation partners.

Presentation Title  | Confidential  |   Document ID

49

---

## Slide 50

**Title:** Legacy enhancement – ‘Aspirational’ cost implications

| Application Area | Internal Days | External Days | Internal £000’s | External £000s | Total £000s |
| --- | --- | --- | --- | --- | --- |
| Category Planning (Bespoke) | 1,688 | 1,688 | 505 | 1,350 | 1,855 |
| Promotion Planning (Package) | 945 | 2,205 | 285 | 3,040 | 3,325 |
| Range Optimisation (Galleria package) | 819 | 1,392 | 245 | 1,770 | 2,195 |
| Macro Space and Store Clustering (Galleria package) | 819 | 1,392 | 245 | 1,770 | 2,195 |
| Unit Stock Control and Achieved Margin (Bespoke) | 2,700 | 2,700 | 810 | 2,160 | 2,970 |
| Stock Forecasting, Allocation, Replenish (Package) | 3,000 | 3,250 | 900 | 4,585 | 5,485 |
| Warehouse Management (Package) | 5,267 | 1,953 | 1,580 | 2,580 | 4,160 |
| Supplier Management (Bespoke) | 1,013 | 1,013 | 305 | 810 | 1,115 |
| Staff Scheduling (Package) | 2,900 | 900 | 870 | 720 | 1,590 |
| EDI for Finance (Package) | 2,250 | 450 | 675 | 540 | 1,215 |
| MSD Enhancements (Bespoke) | 505 | 1,045 | 150 | 1,255 | 1,405 |
| Administration and Intranet (Domino package) | 1,063 | 563 | 320 | 675 | 995 |
| MIS Enhancements (Bespoke) | 2,363 | 2,363 | 710 | 3,425 | 4,135 |
| Total Man Days | 25,329 | 20,911 | 7,600 | 24,680 | 32,280 |
| Total Man Years | 113 | 93 |  |  |  |

Cost estimates are derived from the man day estimates on the previous slide.  Man days have been split approximately between internal and external development staff to reflect the type of work being undertaken (ie package based will be 70% external, bespoke will be predominantly internal).  Internal staff have been costed at a notional £300 per day.  External staff have been costed at £800 per day for contractors and a mix of £1200 and £1450 for vendors and implementation partners.

Presentation Title  | Confidential  |   Document ID

50

---

## Slide 51

**Title:** Enhanced Legacy – Draft technical architecture

Mainframe/SAN
storage

VTS Tape
system

Mainframe

Dell cluster
Stores/HO/
storage

UNIX application & integration servers – clustered for resilience

WINTEL application servers – clustered for resilience

WINTEL web servers – clustered for resilience

Primary processing site

Secondary processing site

UNIX application & integration servers – all non production environments + DR

WINTEL application servers – all non production environments + DR

WINTEL web servers – clustered for resilience

Mainframe/SAN
storage

VTS Tape
system

Mainframe

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

This diagram summarises an indicative high level technical architecture which will be required to support the enhanced legacy application architecture – assuming that the current central store and office architecture remains unchanged
Mainframe – continues as the core database server running DB2 and also for legacy applications and batch
Storage – assumes that the current segregation between WINTEL and other platforms is retained
UNIX – introduced as the application server platform for new client server based applications and also as the integration hub platform, local resilience is factored in on each site, applications balanced across sites to reduce overhead
WINTEL – continues for current store and SMS2 architectures, some applications will also reside on WINTEL (eg Galleria)
WINTEL – used for web servers which will be required by some applications etc (eg Galleria and Domino)
Assumes current outsourced applications remain outsourced (eg MSD and Domino)
Second site is for DR and also resilience – capacity balanced across the two sites, mix of hot and warm failover

Presentation Title  | Confidential  |   Document ID

51

---

## Slide 52

**Title:** Enhanced Legacy – Draft technical architecture

Mainframe/SAN
storage

VTS Tape
system

Mainframe

Dell cluster
Stores/HO/
storage

UNIX application & integration servers – clustered for resilience

WINTEL application servers – clustered for resilience

WINTEL web servers – clustered for resilience

Primary processing site

Secondary processing site

WINTEL web servers – clustered for resilience

Mainframe/SAN
storage

VTS Tape
system

Mainframe

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

UNIX application & integration servers – all non production environments + DR

WINTEL application servers – all non production environments + DR

10 x 4 CPU Intel servers for web serving – numbers difficult to determine but all applications will use web servers

Galleria 2 x 8 CPU Intel servers, Transport Planning already in place

WMS will either be central servers (1 x 16way P590 & 1 x 8way P590) or 2 smaller servers in each DC; Websphere 2 x 8way P570s, Promotion Planning/Forecasting & Replen will be 2 x 18way P590s

Dell cluster/SAN for stores/HO assumed to remain the same as planned for Gain Lane

Mainframe capacity is very difficult to predict, but scope of applications is similar to Safeway + MIS, assumed to Safeway 23 CPUs + 800 MIPS extra for MIS database, allowing 2 extra CPUs

Tape will be the Safeway VTS 10 bay unit. DASD assumes additional 20 Tb in addition to Gain Lane

Configuration of the DR site is difficult to determine at this stage, options are either a mirror of the production site or to run similar number of smaller servers which are dedicated to all non production environments – assumed the latter for all UNIX (2x12way P590s, 2x8way P570s and 4x12way P590s) and Wintel (10x4way web, 2x4way Galleria)

Mainframe configuration of DR site will be very similar to the primary site as will be running parallel sysplex (assumed applications will be re-written to use).  DASD and tape will be a mirror of the primary site for full data back up.  Assumed that Dell cluster/SAN will be mirror of the primary site and is being resolved as part of the Gain Lane plan

Note: Machine sizings are indicative and based on implementations in similar retail businesses.  They are not the result of a formal sizing process.  A formal review will be required to confirm configurations

Presentation Title  | Confidential  |   Document ID

52

---

## Slide 53

**Title:** Legacy enhancement – Integration approach

A common integration infrastructure would reduce Morrisons’ integration costs & risks, and accelerate the deployment of new applications. Continuing with the existing approach and infrastructure would make the future applications landscape unmanageable
To support the required developments will require the increasing use of client server, which will prevent the use of common databases for integration, real time messaging will be needed
Industry best practice approach to integration is to use EAI (Enterprise Application Integration) tools such as Websphere
The diagram below highlights the typical integration architecture developed in EAI

An EAI based integration architecture would deliver benefits through:
Reduced development costs from the re-use of common components and sharing of integration routines
Increased robustness from the use of proven tools
Improved management from real time monitoring of all interfaces
Increased service levels from supporting real time integration and highlighting problems immediately
More functionally rich systems where information is shared across platforms

Presentation Title  | Confidential  |   Document ID

53

---

## Slide 54

**Title:** Legacy enhancement – Draft implementation roadmap

The implementation plan overleaf illustrates a possible approach for delivering the legacy enhancements. This option has been based on the following assumptions:
Product& price master and sales history file must be implemented before any significant “aspirational” system changes can be made, for example to unit stock control, which in turn must be implemented prior to stock ordering, allocation & replenishment functionality
“Aspirational’’ developments such as category management, price & promotions management, are also dependent on the product & price mater and sales history file
MIS development will be iterative as more data becomes available from new systems  developments and implementations
The “optimisation’’ developments will be undertaken in parallel with the product & price master and sales history file replacement as they will deliver short-term benefits
Some “aspirational’’ benefits can begin immediately as they are package based and can be implemented independently of the product & price master & sales history file replacement project (e.g. Galleria)
The WMS replacement should begin once the product & price master and sales history file development designs have completed as the potential benefits from a new WMS are significant and should not be delayed un-necessarily
Major system areas (eg SMS2, SMS, WREP, Store HHTs) will require enhancing every year to reflect changing business needs.  These future developments have not been shown on the plan as they have not been defined, but as previously stated they could add between 5,000 and 7,500 man days per year to the plan
The current development team contains approximately 70 staff of which roughly 50% are engaged on support and maintenance activities. This leaves between 35 and 40 FTEs to support the development workload – additional resources will be needed

Presentation Title  | Confidential  |   Document ID

54

---

## Slide 55

**Title:** Legacy enhancement – Draft implementation roadmap

The chart below illustrates a possible implementation approach for delivering the legacy enhancements. The plan has been based on the assumptions on the previous page:

Presentation Title  | Confidential  |   Document ID

55

---

## Slide 56

**Title:** Legacy Enhancement – Cost implications

Costs on slide are indicative only, final costs will be subject to vendor negotiation.  The indicative costs in the table below have been based on work undertaken with other retail clients in the last 2-3 years on the selection and implementation of packages

| Implementation Cost | One off Capital (£000’s) | Annual Revenue (£000’s) |
| --- | --- | --- |
| Optimisation Costs | 16,430 | 0 |
| Aspiration Costs | 32,280 | 0 |
| Hardware Costs | 10,800 | 1,000 |
| Software Costs (Applications) | 5,000 | 2,000 |
| Software Costs (DB/Utilities/Systems Management) | 3,000 | 1,000 |
| Total Costs | 67,510 | 4,000 |

Additional costs will be incurred, for example, the backfilling of business staff so that key individuals can be full time on major development projects.  These have not been estimated at this stage as the business policy towards this is not known

Presentation Title  | Confidential  |   Document ID

56

---

## Slide 57

**Title:** Legacy enhancement – Overall assessment

Based on discussions with IT Development management, the overall values for the enhance legacy option are:

| Criteria | Comments | Score |
| --- | --- | --- |
| Functionality | Can be made to support defined requirements but will not have additional functionality which the business can develop into. Will require constant further development to support on-going requirements. |  |
| Risk | Very high risk, requires a major bespoke development, Morrisons culture will prefer that development is done in-house, internal team will have to be re-skilled and extended, with extensive use of contractors. |  |
| Complexity | Whilst enhancing known systems initially appears to be simple, experience shows that it is often the most complex as it will retain the complexity of the current architecture and be further increased by ever changing and developing business requirements. |  |
| Scalability | The existing legacy architecture has scalability issues from the underlying batch design – these will all be carried forward into the enhanced legacy architecture.  Further compromise will come from the need to integrate packages into the underlying architecture |  |
| Flexibility | The underlying legacy architecture is increasingly inflexible.  This will not be removed or reduced unless a major redevelopment is undertaken.  Flexibility will always be restricted as limited functional options will be available.  Some core business requirements will have to be removed (eg old number/new number) |  |
| Cost | Cost of legacy initially appears compelling as developments are always under-estimated at the beginning and internal resources are not costed.  As design progresses, more functionality is requested and costs/timescales increase. |  |
| Supportability | Core skills within the exiting department are based around an old programming language and VSAM files.  Re-skilling will be needed to support the redevelopment work on DB2/Cobol/Java to provide use friendly applications.  External staff will have to be recruited or used as contractors. |  |
| Timescale | Initial timescales look to be the longest, with total timeframe over 4 years.  Experience shows that bespoke developments are the most likely to over-run as requirements evolve during the project and force re-writes. |  |

Best

Worst

Presentation Title  | Confidential  |   Document ID

57

---

## Slide 58

**Title:** ‘Best of Breed’ Package Option

---

## Slide 59

**Title:** Best of breed package – Overview of application architecture

This section summarises the application architecture which could be implemented using a “best of breed” packaged approach
There are a limited number of core retail packages on the market – Oracle Retail (was Retek), JDA and GOLD – are the only vendors with a proven track record in large grocery retail businesses
Of these vendors, Oracle Retail are the acknowledged market leaders and have the most grocery customers fully live – this system has been used as the core of the application architecture
Products from third party suppliers have been included where appropriate
In defining the architecture, the following has been undertaken:
Compare Oracle Retail functionality against the IBM component business model to ensure full functional fit
Compare known Oracle Retail functionality with that being demanded by the business
Identify which legacy applications would be retained in the final architecture
High level, indicative, estimate of the technical architecture required to operate the proposed Oracle Retail based architecture
High level, indicative, estimate of the potential implementation costs
In developing this architecture, it has been assumed that:
Oracle Retail modules will be used where they can provide the functionality
Complementary Oracle products will be used to support missing areas (eg financials, HR/payroll, customer management / marketing
The complete footprint is implemented (it is possible that not all modules will be implemented (eg Swisslog might be retained in place of Oracle RDW)

Presentation Title  | Confidential  |   Document ID

59

---

## Slide 60

**Title:** Best of breed package – Level of functional support for “Optimisation” processes mapped against IBM CBM

Manual process in most retail businesses

Process out of scope for this review

Oracle Retail - good functional support – minimal changes

Oracle Retail - Functional support,  changes needed or 3rd party solution

Legend

Poor or no functional support and high degree of manual input

Other Oracle products - good functional support

Legacy systems retained as provide a good fit

Presentation Title  | Confidential  |   Document ID

60

---

## Slide 61

**Title:** Best of breed package – Application architecture with CBM overlay

Presentation Title  | Confidential  |   Document ID

61

---

## Slide 62

**Title:** Best of breed package – Application architecture mapped against grocery retail process model

Presentation Title  | Confidential  |   Document ID

62

---

## Slide 63

**Title:** Best of breed package – Draft technical architecture

SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

UNIX Oracle Retail application and database servers – clustered (via LPARs) for resilience

WINTEL web & application servers – clustered for resilience

Primary processing site

Secondary processing site

SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

This diagram summarises an indicative high level technical architecture required to support the best of breed package (Oracle Retail) option – assuming that the current central store and office architecture remains unchanged
Mainframe – discontinued as legacy applications are migrated off onto packages or re-written onto client server
Storage – assumes that the current segregation between WINTEL and other platforms is retained
UNIX – introduced as the database and application server platform for all applications and integration work
WINTEL – continues for current store and SMS2 architectures, some applications will also reside on WINTEL (eg Galleria)
WINTEL – used for web servers which will be required by Oracle and other applications etc (eg Galleria and Domino)
Assumes current outsourced applications remain outsourced (eg MSD and Domino)
Second site is for DR and also resilience – Oracle Retail capacity is used for all non production environments to reduce total capacity needs

UNIX application and integration servers – clustered (via LPARs) for resilience

UNIX servers for dev/test/QA, web and integration applications + standby for DR

UNIX servers for dev/test/QA, application and integration + standby for DR

WINTEL web & application servers – clustered for resilience

RMS

RDW

RDM/AIP – Apps

Dev

QA

Training

WMS

Integration

WMS

Integration

RDW

RDM/AIP

RMS – DB

Presentation Title  | Confidential  |   Document ID

63

---

## Slide 64

**Title:** Best of breed package – Draft technical architecture

Mainframe capacity at the DR site will gradually be reduced to zero as applications are migrated off onto UNIX.  DASD and tape are mirrors of the production site to allow full data resilience.  Dell cluster for stores and HO is assumed to be the same as primary, as per Gain Lane plans

SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

UNIX Oracle Retail application and database servers – clustered (via LPARs) for resilience

WINTEL web & application servers – clustered for resilience

Primary processing site

Secondary processing site

SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

UNIX application and integration servers – clustered (via LPARs) for resilience

UNIX servers for dev/test/QA, web and integration applications + standby for DR

UNIX servers for dev/test/QA, application and integration + standby for DR

WINTEL web & application servers – clustered for resilience

RMS

RDW

RDM/AIP – Apps

Dev

QA

Training

WMS

Integration

WMS

Integration

RDW

RDM/AIP

RMS – DB

10x4way Intel servers for web servers.  Galleria will need 2x8 way Intel application servers

Websphere will need 2x8way servers, WMS will need 1x16 way & 1x8way P590, 2x4way P570 for systems management

Core Oracle Retail servers will be top end P590s, initial sizing indicates that 3 x 32 way P590s will be needed to support the production application and database volumes

Dell cluster/SAN for stores/HO assumed to remain the same as planned for Gain Lane

Mainframe capacity will be gradually reduced to zero as applications are migrated off onto UNIX

Tape will be the Safeway VTS 10 bay unit. DASD assumes additional 30 Tb in addition to Gain Lane

Configuration of the DR site is difficult to determine at this stage, options are either a mirror of the production site or to run similar number of smaller servers which are dedicated to all non production environments – assumed the latter for all UNIX (3x18way P590s, 2x8way P570s and 2x8way P590s). Wintel 10x4way web and 2x4way Galleria

Note: Machine sizings are indicative and based on implementations in similar retail businesses.  They are not the result of a formal sizing process.  A formal review will be required to confirm configurations

Presentation Title  | Confidential  |   Document ID

64

---

## Slide 65

**Title:** Best of breed package – Integration approach

Oracle Retail integration combines the following:
RETL – Extract transform and load is a data movement toll that supports high volume, repeatable interfaces and is supported within the product suite between core modules
EAI – message based integration which supports some standard interfaces between core modules and bespoke developments for each customer
Batch – combination of standard and bespoke developments which support batch based interfaces between core modules
Batch RETL – limited number of standard feeds which usually support the importing of data into the core modules

Note: The integration shown on this slide is a summary of the type of integration used in typical Oracle Retail implementations.  It shows the basic approach to integration between the core modules and also to third party packages

Oracle have announced their “Fusion” development which is aiming to deliver “out of the box” integration between all of their “Retail” products for May 2006.  We have not been provided with details on “Fusion”, but if delivered will provide a significant benefit to customers

Presentation Title  | Confidential  |   Document ID

65

---

## Slide 66

**Title:** Best of breed package – Draft implementation roadmap

The plan below illustrates a possible implementation approach for delivering a best of breed package architecture.  It is based on:
All in store systems remain on legacy platforms until core Oracle implementation completed
Galleria is an early project to deliver benefits from range and space optimisation
The PROMOTE modules are an early project a they will deliver benefits from category and promotions management
Core Oracle implementation begin with a Conference Room Pilot (CRP – overall design) and then implementation of the core RMS etc modules
Initial MIS work is undertaken on an in-house bespoke platform as the RDW module use the data structure of the core RMS/RPM modules 
Warehouse management design is run in parallel to RMS, this does increase the risk slightly but will deliver benefits significantly earlier
Final phases relate to the implementation of the advanced inventory planning module (AIP) to support forecasting, allocation and replenishment
The store inventory management module (RSIM) is optional, Morrisons may choose to remain on their legacy HHT based infrastructure

Presentation Title  | Confidential  |   Document ID

66

---

## Slide 67

**Title:** Best of breed package – Cost implications

Costs on slide are indicative only, final costs will be subject to vendor negotiation.  The indicative costs in the table below have been based on work undertaken with other retail clients in the last 2-3 years on the selection and implementation of packages. Core software licences are based on list price for similar sized retailers and should be reduced with negotiation

| Implementation Cost | One off Capital (£000’s) | Annual Revenue (£000’s) |
| --- | --- | --- |
| Software licences | 10,000 | 2,500 |
| Hardware (including production) - TBC | 10,550 | 1,000 |
| Third party software licences (databases, integration) – TBC | 3,000 | 600 |
| Implementation partner | 25-30,000 | 0 |
| Bespoke developments | 2,000 | 250 |
| Internal IT staff (1:2 ratio internal:external = 15,000 days) | 4,500 | 0 |
| Total Costs | 55-60,050 | 4,350 |

Additional costs will be incurred, for example, the backfilling of business staff so that key individuals can be full time on major development projects.  These have not been estimated at this stage as the business policy towards this is not known

Presentation Title  | Confidential  |   Document ID

67

---

## Slide 68

**Title:** Best of breed package – Overall assessment

Based on IBM experience of implementing Oracle Retail, the overall assessment against the stated criteria are:

| Criteria | Comments | Score |
| --- | --- | --- |
| Functionality | Oracle is functionally very rich and will provide functionality to support stated requirements with minimal enhancement. Some 3rd party products will be needed (eg Galleria) to provide full functionality in all areas.  Oracle has actively acquired 3rd party products to complement the core Retail/Financials/Hr/Payroll modules. |  |
| Risk | Oracle Retail is a very modular product so implementation risk an be reduced as long as focus is maintained on single module areas.  However, the modules are not all fully integrated so the implementation risk is increased due to the requirement for integration. |  |
| Complexity | Oracle Retail is a functionally rich product but is easier to configure than many of its competitors.  However, enhancements and integration will be needed so complexity increases.  The product does have an integration bus to help with the integration but this is not developed for all modules (mainly RMS to RDM and RDW).. |  |
| Scalability | Oracle Retail is very scalable and has been proven in major grocery retail companies.  Some of the newer modules require significant investment in processing power to support (eg AIP and RSIM) |  |
| Flexibility | Oracle Retail has a reputation for being flexible, however, this is only true if a careful approach is taken to the design with minimal enhancements to ensure that customers can take upgrades.  Flexibility is decreased with complex integration – again this has to be mitigated through careful design |  |
| Cost | In our experience Oracle Retail is roughly similar in implementation cost to SAP and other packages.  Lower configuration costs are balanced by the significantly higher integration costs.  Oracle maintenance costs can often be higher as they used to heavily discount module purchase costs but base maintenance on the original prices |  |
| Supportability | Morrisons currently has no skills in Oracle Retail so additional staff will need to be recruited (assuming support is to be retained in house).  There are is a shortage of Oracle Retail skills on the market  This can be overcome by working with an implementation partner |  |
| Timescale | Oracle Retail implementations can be completed in short timescales through careful scope management.  Typical implementation timescales are 9-12 months for core master file, pricing and unit stock management.  Additional modules take 9-12 months for each phase.  Roll-out will be dependent on the size of the business and approach |  |

Best

Worst

Presentation Title  | Confidential  |   Document ID

68

---

## Slide 69

**Title:** Integrated Package Option

---

## Slide 70

**Title:** Integrated package – Overview of application architecture

This section summarises the application architecture which could be implemented using an “integrated” packaged approach
There is only one true integrated retail package on the market – SAP IS-Retail – with a proven track record in large grocery retail businesses
The SAP IS-Retail system has been used as the core of the application architecture
Products from third party suppliers have been included where appropriate
In defining the architecture, the following has been undertaken:
Compare SAP IS-Retail functionality against the IBM component business model to ensure full functional fit
Compare known SAP IS-Retail functionality with that being demanded by the business
Identify which legacy applications would be retained in the final architecture
High level, indicative, estimate of the technical architecture required to operate the proposed SAP IS-Retail based architecture
High level, indicative, estimate of the potential implementation costs
In developing this architecture, it has been assumed that:
SAP IS-Retail modules will be used where they can provide the functionality
The complete footprint is implemented (it is possible that not all modules will be implemented (eg Swisslog might be retained in place of SAP WM)
SAP has a sub-option which assumes that PeopleSoft financials are not fully implemented and SAP Financials are implemented instead

Presentation Title  | Confidential  |   Document ID

70

---

## Slide 71

**Title:** Integrated package – Assessment of functional support

Manual process in most retail businesses

Process out of scope for this review

SAP Retail - good functional support – minimal changes

SAP Retail - Functional support,  changes needed or 3rd party solution

Legend

Poor or no functional support and high degree of manual input

Other SAP products - good functional support

Legacy systems retained as provide a good fit

Presentation Title  | Confidential  |   Document ID

71

---

## Slide 72

**Title:** Integrated package – Application architecture with CBM overlay, assuming Peoplesoft Financials is retained

Presentation Title  | Confidential  |   Document ID

72

---

## Slide 73

**Title:** Integrated package – Application architecture with CBM overlay, assuming Peoplesoft Financials is replaced

Presentation Title  | Confidential  |   Document ID

73

---

## Slide 74

**Title:** Integrated package – Application architecture mapped against  grocery process model, assuming Peoplesoft Financials retained

Presentation Title  | Confidential  |   Document ID

74

---

## Slide 75

**Title:** Integrated package – Application architecture mapped against  grocery process model, assuming Peoplesoft Financials replaced

Presentation Title  | Confidential  |   Document ID

75

---

## Slide 76

**Title:** Integrated package – Draft technical architecture, SAP running database on DB2 on mainframe

Mainframe/SAN
storage

VTS Tape
system

Mainframe – SAP database & legacy apps

Dell cluster
Stores/HO/
storage

UNIX SAP application servers – clustered (using LPARs) for resilience

WINTEL web & application servers – clustered for resilience

Primary processing site

Secondary processing site

Mainframe/SAN
storage

VTS Tape
system

Mainframe – SAP database and legacy apps

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

This diagram summarises the high level technical architecture required to support the integrated package (SAP) option – assuming that the current central store and office architecture remains unchanged
Mainframe – continues as the core database server for SAP (could be on UNIX) and also for legacy applications
Storage – assumes that the current segregation between WINTEL and other platforms is retained
UNIX – introduced as the application server platform for all SAP applications and integration work
WINTEL – continues for current store and SMS2 architectures, some applications will also reside on WINTEL (eg Galleria)
WINTEL – used for web servers which will be required by SAP and some other applications etc (eg Galleria and Domino)
Assumes current outsourced applications remain outsourced (eg MSD and Domino)
Second site is for DR and also resilience – SAP capacity is used for all non production environments to reduce total capacity needs

UNIX servers for applications and integration – clustered (via LPARs) for resilience

UNIX SAP servers for all non production environments + standby for DR

UNIX servers for application and integration developments + standby for DR

WINTEL web & application servers – clustered for resilience

Core SAP

BW

F&R - Apps

Dev

QA

Training

Integration

WMS

Integration

WMS

Presentation Title  | Confidential  |   Document ID

76

---

## Slide 77

**Title:** Integrated package – Draft technical architecture, SAP running database on DB2 on mainframe

Mainframe/SAN
storage

VTS Tape
system

Mainframe – SAP database & legacy apps

Dell cluster
Stores/HO/
storage

UNIX SAP application servers – clustered (using LPARs) for resilience

WINTEL web & application servers – clustered for resilience

Primary processing site

Secondary processing site

Mainframe/SAN
storage

VTS Tape
system

Mainframe – SAP database and legacy apps

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

UNIX servers for applications and integration – clustered (via LPARs) for resilience

UNIX SAP servers for all non production environments + standby for DR

UNIX servers for application and integration developments + standby for DR

WINTEL web & application servers – clustered for resilience

Core SAP

BW

F&R - Apps

Dev

QA

Training

Integration

WMS

Integration

WMS

Dell cluster/SAN for stores/HO assumed to remain the same as planned for Gain Lane

Mainframe capacity based on running SAP on DB2.  Indicates that 18 CPUs will be needed for the production database and 11 for development/QA – total of 37 CPUs (from projected 308) – 14 more than SW mainframes

Tape will be the Safeway VTS 10 bay unit. DASD assumes additional 30 Tb in addition to Gain Lane

Configuration of the DR site is difficult to determine at this stage, options are either a mirror of the production site or to run similar number of smaller servers which are dedicated to all non production environments – assumed the latter for all UNIX (2x16way P590s, 2x8way P570s and 2x8way P590s for WMS), & Wintel (10x4way web, 2x4way Galleria)

Mainframe configuration of DR site will be very similar to the primary site as will be running parallel sysplex.  DASD and tape will be a mirror of the primary site for full data back up.  Assumed that Dell cluster/SAN will be mirror of the primary site and is being resolved as part of the Gain Lane plan

10x4way Intel servers for web servers.  Galleria will need 2x8 way Intel application servers

Websphere will need 2x8way P590 servers, WMS will need 2x14 way P570s, system management on 2x4way P570s

Indicative sizing estimates 100,000 SAPS, core application servers will be 2x24way P590 unix servers. WMS on 1x16way P590 and 1x8way P590. Database will be on the mainframe

Note: Machine sizings are indicative and based on implementations in similar retail businesses.  They are not the result of a formal sizing process.  A formal review will be required to confirm configurations

Presentation Title  | Confidential  |   Document ID

77

---

## Slide 78

**Title:** Integrated package – Draft technical architecture, SAP running entirely on UNIX platforms

Mainframe/SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

UNIX SAP application and database servers – clustered (using LPARs) for resilience

WINTEL web & application servers – clustered for resilience

Primary processing site

Secondary processing site

Mainframe/SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

This diagram summarises an indicative high level technical architecture required to support the integrated package (SAP) option – assuming that the current central store and office architecture remains unchanged
Mainframe – essentially discontinued, all SAP run on UNIX, remaining legacy should be migrated off the mainframe
Storage – assumes that the current segregation between WINTEL and other platforms is retained
UNIX – introduced as the database and application server platform for all SAP applications and integration work
WINTEL – continues for current store and SMS2 architectures, some applications will also reside on WINTEL (eg Galleria)
WINTEL – used for web servers which will be required by SAP and some other applications etc (eg Galleria and Domino)
Assumes current outsourced applications remain outsourced (eg MSD and Domino)
Second site is for DR and also resilience – SAP capacity is used for all non production environments to reduce total capacity needs

UNIX servers for applications and integration – clustered (via LPARs) for resilience

UNIX SAP servers for all non production environments + standby for DR

UNIX servers for application and integration developments + standby for DR

WINTEL web & application servers – clustered for resilience

Core SAP

BW

F&R - Apps

Dev

QA

Training

BW

F&R

Core SAP - DB

Integration

WMS

Integration

WMS

Presentation Title  | Confidential  |   Document ID

78

---

## Slide 79

**Title:** Integrated package – Draft technical architecture, SAP running entirely on UNIX platforms

Mainframe/SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

UNIX SAP application and database servers – clustered (using LPARs) for resilience

WINTEL web & application servers – clustered for resilience

Primary processing site

Secondary processing site

Mainframe/SAN
storage

VTS Tape
system

Mainframe – discontinued

Dell cluster
Stores/HO/
storage

2 sites connected by high speed fibre to allow synchronisation of disk storage (either at SAN level, or at processor level)

UNIX servers for applications and integration – clustered (via LPARs) for resilience

UNIX SAP servers for all non production environments + standby for DR

UNIX servers for application and integration developments + standby for DR

WINTEL web & application servers – clustered for resilience

Core SAP

BW

F&R - Apps

Dev

QA

Training

BW

F&R

Core SAP - DB

Integration

WMS

Integration

WMS

Dell cluster/SAN for stores/HO assumed to remain the same as planned for Gain Lane

Mainframe capacity is gradually reduced to zero as applications are migrated off onto UNIX

Tape will be the Safeway VTS 10 bay unit. DASD assumes additional 10 Tb in addition to Gain Lane

Mainframe capacity at DR site is gradually reduced to zero as applications are migrated off.  Tape and DASD will be mirrors of the main production site for full data resilience.  Dell cluster for stores and HO will be a mirror of the production site as per Gain Lane planning

10x4way Intel servers for web servers.  Galleria will need 2x8 way Intel application servers

Websphere 2x8way P590 servers, WMS will need 1x16way & 1x8way P590s, system management 2x4way P570s.

Configuration of the DR site is difficult to determine at this stage, options are either a mirror of the production site or to run similar number of smaller servers which are dedicated to all non production environments – assumed the latter for all UNIX (3x16way P590s, 2x8way P570s and 2x8way P590s), Wintel (10x4way web, 2x4way Galleria)

Indicative sizing estimates 100,000 SAPS, core application and database servers will be 3x24 way P590 Unix servers

Note: Machine sizings are indicative and based on implementations in similar retail businesses.  They are not the result of a formal sizing process.  A formal review will be required to confirm configurations

Presentation Title  | Confidential  |   Document ID

79

---

## Slide 80

**Title:** Integrated package – Integration approach

SAP has re-developed its integration approach and tool kit in the last 2 years
SAP integration is now built around its NetWeaverTM toolset (see diagram below)
SAP NetWeaverTM provides a structured and layered integration architecture:
Presentation layer utilises the SAP portal to provide multi-channel / multi-device
Information layer provides seamless integration through a common set of applications
Integration layer based on messaging services to link to non-SAP products / systems
Application layer based on traditional SAP BAPIs, Java and ABAP code
All SAP applications are now developed and supported within a single framework
SAP provides a solution and configuration manager toolkit to control all elements of development

The presentation and interaction components of SAP. Allowing role based access through thin and thick clients and various device types. Also collaboration folders for working across organisation boundaries.

The information layer with functionality for business planning, data warehouse and mining, knowledge management, search engine and master data management and synchronisation.

Integration layer providing messaging services linking SAP and non SAP applications (exchange infrastructure), monitoring and business workflow management.

Application Server, providing Database, Operating System with JAVA and ABAP based coding platforms.

Software lifecycle toolkit including project (solution manager) and configuration management tools.

An environment for the design of composite applications that comply with Enterprise Services Architecture.

Presentation Title  | Confidential  |   Document ID

80

---

## Slide 81

**Title:** Integrated package – Draft implementation roadmap

The plan below illustrates a possible implementation approach for delivering an integrated package architecture.  It has been based on:
In store systems will be developed in house, based on current platforms
Galleria will be used for range and space optimisation and will be an early project to deliver benefits
SAP BW and POS DM will be an early project to provide MIS, sales audit and other benefits (eg category management)
Khimetrics will be an early project to provide price optimisation benefits
Core SAP will begin with a company wide E2E blueprinting phase to get the design right
Core SAP implementation will begin with product/price/supplier master files to replace core legacy files – this is the lowest risk approach
Stock management in SAP is dependent on core SAP master files, so all elements will be phased afterwards, this reduces integration risk
The SAP Store Manager portal is implemented with stock management – requires a long roll out
Peoplesoft financials will be retained and SAP integrated to it
Third party WMS is implemented in parallel to the core SAP master files

Presentation Title  | Confidential  |   Document ID

81

---

## Slide 82

**Title:** Integrated package – Cost implications

| Implementation Cost | One off Capital (£000’s) | Annual Revenue (£000’s) |
| --- | --- | --- |
| Software licences | 10,000 | 1,800 |
| Hardware (including production) - TBC | 10,100 | 1,000 |
| Third party software licences (databases, integration) – TBC | 3,000 | 600 |
| Implementation partner | 25-30,000 | 0 |
| Bespoke developments | 500 | 125 |
| Internal IT staff (1:2 ratio internal:external = 15,000 man days) | 4,500 | 0 |
| Total Costs | 53-58,100 | 3,525 |

Costs on slide are indicative only, final costs will be subject to vendor negotiation.  The indicative costs in the table below have been based on work undertaken with other retail clients in the last 2-3 years on the selection and implementation of packages.  Package licence costs are based on list prices for similar sized retailers and should be reduced in negotiation

Additional costs will be incurred, for example, the backfilling of business staff so that key individuals can be full time on major development projects.  These have not been estimated at this stage as the business policy towards this is not known

Presentation Title  | Confidential  |   Document ID

82

---

## Slide 83

**Title:** Integrated package – Overall assessment

Based on IBM experience of implementing SAP IS-Retail, the overall assessment against the stated criteria are:

| Criteria | Comments | Score |
| --- | --- | --- |
| Functionality | SAP is functionally very rich and will provide functionality to support stated requirements with minimal enhancement. Some 3rd party products will be needed (eg Galleria) to provide full functionality in all areas.  SAP is developing its products into all areas, or acquiring niche packages from other vendors (eg Khimetrics) |  |
| Risk | Implementation risk can be high if too great a scope is attempted, this has been balanced in the proposed approach.  Additional risk from recruiting new staff and skills to support major implementation.  Mitigate through working with experienced implementation partners |  |
| Complexity | SAP has a reputation for being a big complex system and it is.  However, it is extremely robust and complexity can be reduced from following best practice approaches using experienced staff.  Complexity is also reduced due to the integrated nature of the product. |  |
| Scalability | SAP is very scalable and has been proven in global companies.  Early versions of IS-Retail did have performance problems, but these have been addressed and SAP now has reference sites in major grocery retailers |  |
| Flexibility | SAP has a reputation for being inflexible once it has been implemented.  Experience has shown that this is reduced by configuring additional processes and managing development in phases.  The integrated system design also increases flexibility as there are fewer and less complex interfaces to manage |  |
| Cost | In our experience SAP is no more expensive to implement than other packages, including BoB.  Higher SAP implementation costs (configuration) are balanced out by the significantly lower integration costs.  SAP claims lower cost of ownership to be a key differentiator (ie they are the lowest), this is backed up by Gartner and others |  |
| Supportability | Morrisons currently has no skills in SAP so additional staff will need to be recruited (assuming support is to be retained in house).  There are no shortage of SAP skills on the market, although there is a shortage of staff who are experienced in the SAP IS-Retail variant.  This can be overcome by working with an implementation partner |  |
| Timescale | SAP IS-Retail implementations are becoming faster as the product matures and partners obtain greater experience.  Typical implementation timescales are 12 months for core master file and pricing and a further 9-12 months for stock management.  Roll-out timescales will be dependent on the size of the business and approach adopted |  |

Best

Worst

Presentation Title  | Confidential  |   Document ID

83

---

## Slide 84

**Title:** Summary and Conclusion

---

## Slide 85

**Title:** Summary of work undertaken

Business requirements are changing significantly and will continue to change as the business thinking develops

The core of the existing systems will need replacing to support the emerging business requirements

The review assessed the business requirements and grouped them into “Optimisation” and “Aspirational”, although the small store workstream is increasingly asking for the aspirational requirements

The review evaluated, at a high level, three options for supporting the changes:
Enhance legacy/bespoke development
Replacement with best of breed packages
Replacement with an integrated package

The 3 options were evaluated against a number of criteria:
Functional support
Risk
Complexity
Scalability
Flexibility
Cost
Supportability
Timescale

Presentation Title  | Confidential  |   Document ID

85

---

## Slide 86

**Title:** Integrated Package

Best of Breed Package

Enhanced Legacy

Summary of architectures reviewed

Advantages
Use of existing technical in-house skills (eg DB2) 
Greatest reuse of existing infrastructure (ie mainframe)
Most cost effective option for ‘’Optimisation’’ functionality
Wholesale replacement of core systems will be required to support “Aspirational” requirements – within 12 months
Disadvantages
Bespoke development on such a large scale will be very high risk
Functionality delivered will only match what the business requires today
Legacy technology platforms will lead to supportability and manageability issues
Significant re-skilling of the current IT department

Advantages
Support for ‘’Aspirational’’ processes
Best in class functionality
Quicker implementation of some components and therefore earlier payback/realisation of benefits
Implementation phases are smaller and as a result will require less business change

Disadvantages
Limited reuse of existing infrastructure
Integration development will be required between the core packages and their modules
Limited to Oracle databases & Unix platform so significant new skills will be needed

Advantages
Support for “Aspirational” processes
Integrated solution within the core package
Could reuse some existing infrastructure (ie mainframe and DB2)
Greatest availability of skilled implementation support
Robust and responsive architecture

Disadvantages
Longer payback period
More significant business change impact (larger implementation phases)
May not fit Morrisons culture of implementing small changes
New skills will be required

Presentation Title  | Confidential  |   Document ID

86

---

## Slide 87

**Title:** Integrated Package

Best of Breed Package

Enhanced Legacy

Summary of implementation options

The enhanced Legacy solution allows a practical and cost-effective solution to the ‘’Optimise’’ functional requirements
Has the longest implementation timescale to support the delivery of the “Aspirational” requirements – 6 years.  Slowest time to benefits
Has the highest risk of over-run due to the scale of bespoke development
Significant dependency on external resources to deliver – due to the small size of the current IT development team
Includes a significant number of packages to support key elements of the business – where functionality is so complex, bespoke development is not a viable option

A best of breed solution would allow Morrisons to implement key functionality earlier in the programme, therefore allowing an earlier return on investment
There is a greater dependency on external resources
The option ties Morrisons to Unix/Oracle technology and will prevent reuse of current infrastructure
Allows an implementation timeline of under 4 years
Modular approach will allow the implementation of more frequent and smaller business changes – might suit the business culture better

An integrated solution may have a longer benefits realisation period compared with a best of breed solution due to the larger phases being implemented
There is a greater dependency on external resources
This option would allow some reuse of the current infrastructure investment
Allows an implementation timeline of under 4 years
Less modular approach requires the implementation of larger functional changes – may not suit the business culture
Less integration work reduces risk

Presentation Title  | Confidential  |   Document ID

87

---

## Slide 88

**Title:** Summary of costs

Enhanced Legacy
Application s/w	£  5.00m
Hardware		£10.80m
3rd party s/w	£  3.00m
Impl partner/vendor	£20.60m
Bespoke development	£16.53m
Internal IT staff	£11.57m
------------------------------------------------
Total costs		£67.51m

Of the three options, only the enhance legacy option provides cost effective support for the “optimisation” initiatives
However, as the small stores programme is increasingly defining requirements which are currently classed as “Aspirational”, the package based options become realistic alternatives and will provide functionally rich solutions with more room for future development

Best of Breed
Application s/w	£10.00m
Hardware		£10.55m
3rd party s/w	£  3.00m
Impl partner/vendor	£30.00m
Bespoke development	£  2.00m
Internal IT staff	£  4.50m
------------------------------------------------
Total costs		£60.05m

Integrated
Application s/w	£10.00m
Hardware		£10.10m
3rd party s/w	£  3.00m
Impl partner/vendor	£30.00m
Bespoke development	£  0.50m
Internal IT staff	£  4.50m
------------------------------------------------
Total costs		£58.10m

Conclusion
All three options are very expensive, overall there is little to choose between the capital costs 
Enhanced legacy option has the greatest cost risk arising form the scale of bespoke development
Coupled with the implementation risk, the highest cost makes enhancing legacy the least attractive option
IBM’s experience of implementing both best of breed and integrated packages within retail businesses reinforces the equality of the overall costs
The choice of best of breed or integrated package cannot be made on the basis of cost alone

Presentation Title  | Confidential  |   Document ID

88

---

## Slide 89

**Title:** Summary of evaluation – Overall assessment

All three options have been assessed against the overall criteria of functionality, risk, complexity, scalability, flexibility, cost, staff and timescale.  Relative scores are highlighted below, as are the key comments relating to each option.

| Criteria | Enhance legacy | Best of breed package | Integrated package |
| --- | --- | --- | --- |
| Functionality | Can be made to support defined requirements but will not have additional functionality which the business can develop into – will require further development to support future needs | Extremely rich functionality and being developed on an on-going basis to support other customers.  Will allow room for future business development | Extremely rich functionality and being developed on an on-going basis to support other customers.  Will allow room for future business development |
| Risk | Extremely high risk, major bespoke development on a new development language and within an insular culture. Extremely likely to over run on time and therefore costs | High risk, implementing packages in a bespoke based culture requires a high degree of change and the importing of new skills.  Can be mitigated through working with an experienced partner and phased route | Very high risk, implementing packages in a bespoke based culture requires a high degree of change and the importing of new skills.  Can be mitigated through working with an experienced partner |
| Complexity | Very high level of complexity from replacing legacy systems with a combination of bespoke and packaged solutions.  Combines complexity of technical architecture and application architecture | High complexity from implementing a series of packaged modules.  Increased level of integration from this option raises its level of complexity | Reduced complexity from implementing an integrated  package.  Integration between modules is already in place.  Integration still needed with legacy applications during roll out |
| Scalability | Legacy applications are already facing issues in this area, especially from the complex batch architecture.  Enhancements will make much worse.  Re-writing will help to some extent but batch restrictions still remain | Fully proven scalable solution.  Some issue may be encountered during roll-out as new modules are integrated into the legacy landscape | Fully proven scalable solution.  Some issue may be encountered during roll-out as new modules are integrated into the legacy landscape |
| Flexibility | Limited flexibility inherent within the legacy applications – both functional and architectural – will remain when enhanced.  Re-writing will alleviate with those applications | Solution should be flexible, both form functional and architectural viewpoint.  Approach must be to have minimal modifications to retain potential to upgrade in the future | Solution should be flexible to support business and architectural needs going forward.  SAP has proven upgrade track record as long as minimal modifications.  Reputation for being hard to change once configured |
| Cost | Initial costs estimates for in-house development are always lower than packages, but final costs are invariably higher due to over-runs and re-designs caused from the approach of defining own solutions | Costs are high.  Package licences, database licences and new hardware all add to CAPEX, as does need to work with an implementation partner.  Package approach does help contain costs | Costs are high.  Package licences, database licences and new hardware all add to CAPEX, as does need to work with an implementation partner.  Package approach does help contain costs |
| Supportability | Internal development team are limited in size and skill base is out of date.  Major re-skilling will be needed to support bespoke developments.  Cultural resistance will be very high and difficult to manage | No relevant skills internally – new skills will be needed.  Cultural resistance will be high but can be better managed.  Retek skills are scarce in the market | No relevant skills internally – new skills will be needed.  Cultural resistance will be high but can be better managed.  SAP skills are readilly available, although IS-Retail skills are harder to find |
| Timescale | Initial estimates are already the longest of the three options.  Project will over-run due to need to design from scratch and having no functional framework to work within.  Development needs new skills – will slip too | Oracle’s modular approach allows faster implementation of some of the key areas.  Package provides a functional framework to control design and development phases | SAP’s integrated architecture allows some areas to be developed early, but core stock management will be delayed, as will the benefits.  Package provides a functional framework to control design & development |

Best

Worst

Presentation Title  | Confidential  |   Document ID

89

---

## Slide 90

**Title:** Conclusion

Enhance Legacy / Bespoke Development
Current “Optimisation” requirements might be supportable through legacy, although product/price file will need redeveloping
“Aspirational” requirements cannot be supported through enhancing legacy – most systems will require replacing or redeveloping
The scale of bespoke development makes this the highest risk and most expensive approach – and will deliver the least functionality
Packages will be used for many areas as they are the most cost effective and lowest risk approach to implementation
This option begins to look like the “best of breed” approach

Replace with Best of Breed Packages
Provides a viable option for Morrisons
Small stores initiative is driving additional functionality requirements which would be well supported by modern retail systems
Key functionality will best be provided by retail packages (eg range and space optimisation, warehouse and transport planning) as the processing is advanced and too complex to develop internally
A best of breed approach has an advantage in allowing a more flexible implementation programme which can be tailored to delivering benefits earlier to help fund the remainder of the programme

Replace with an Integrated Package
Provides a viable option for Morrisons
As with best of breed, small stores initiative is driving a much greater level of change, requirements which are standard in retail packages
An integrated system will deliver benefits from lower longer term cost of ownership, but offset by a less flexible implementation approach and increased risk from implementing a more complex system.  The risk is partially off set by reduced integration requirements
Integrated packages like SAP have a reputation for being less flexible once implemented, placing greater importance on the initial design phase

Summary
Enhance legacy does provide an option for the current “Optimisation” requirements, but the:
Functionality delivered will only be that which is required today, so there is no room for future growth
Timescales are the longest and at greatest risk
Core product file will have to be re-written
To support the “Aspirational” requirements, the legacy systems will have to be replaced with bespoke developments and niche package solutions
Modern retail packages are now functionally very rich, will support the business today and provide significant additional capability for the business to develop into
Some areas of functional requirements can only be delivered through implementing packages (eg range and space optimisation, promotions planning, transport planning) – so packages will be core to the architecture
All leading grocery retailers are either already on packaged solutions or are in the process of implementing them – reflecting the maturity of the product and the general perceived acceptance the approach
Recommendation is for Morrisons to pursue the package route through:
Immediate evaluation of options
Rapid selection and negotiation
Prepare to being implementing in Q2/3 2006
Some projects should be initiated immediately to deliver early benefits and fund the implementation, for example:
Galleria range and space
Transport planning and WMS
MIS

Presentation Title  | Confidential  |   Document ID

90

---

## Slide 91

**Title:** Appendix I – Business Initiatives – Support for “Optimisation” and “Aspiration”

---

## Slide 92

**Title:** “Plan” Supply Chain Processes – Systems Initiatives

Category Planning
Aspirational:
Category planning system based on sales, stocks and unit margins
Supplier master file and management systems to monitor and manage all aspects of supplier performance
Management information system
Unit stock control system (unit margins)
New product and price file

Optimisation Initiatives:
Enhanced Excel analysis



Current Position:
Product and price file with no unit margins and no view of company stock
Trading information system – no unit margins and implied store stocks
Excel based analysis

Promotions Planning
Aspirational:
Promotions planning system based on sales tracked against promotions, stocks and unit margins
Promotional history – including non sales data (eg advertising spend, weather)
Management information system
Unit stock control system (unit margins)
New product and price file

Optimisation Initiatives:
Excel based promotions tracking and analysis


Current Position:
No tracking of promotional sales and promotion history (last 2 price changes)
Ad hoc Excel based analysis
Trading information system – no unit margins and implied store stocks

Range Planning

Aspirational:
Galleria macro space planning to optimise space by category (sales and margin) in store groups
Galleria range optimisation to match store range to sales, product margins, space and customer
Management information system
Unit stock control system (unit margins)

Optimisation Initiatives:
Excel based analysis
Spaceman to manually tailor store range to space

Current Position:
Single range, planogrammed on Spaceman
Smaller stores have some adjustments on manual basis
Trading Information System – no unit margins and implied store stocks

Presentation Title  | Confidential  |   Document ID

92

---

## Slide 93

**Title:** “Buy” Supply Chain Processes – Systems Initiatives

Product Sourcing & Buying
Aspirational:
New product and price master file system
Category & supplier management systems to support sourcing and buying decisions
Management information system to provide margin and sales information
Unit stock control system to provide achieved margin information

Optimisation Initiatives:
Enhanced Excel analysis
SMS2 enhancements/extensions


Current Position:
Product and price file with no unit margins and no view of company stock
Trading information system – no unit margins and implied store stocks
Excel based analysis 
MSD for supplier information

Product Pricing
Aspirational:
New product and price master file system
Price optimisation system to maximise margin at product level
Promotions planning system to optimise promotional pricing
Management information system


Optimisation Initiatives:
Excel based promotions tracking and analysis


Current Position:
Legacy product and price file – only maintains current and previous price
Trading information system – no unit margins and implied store stocks
Excel based analysis

Presentation Title  | Confidential  |   Document ID

93

---

## Slide 94

**Title:** “Move” Supply Chain Processes – Systems Initiatives

Supply Chain Planning
Aspirational:
Integrated transport planning and warehouse management systems (also integrated to replenishment and forecasting)
Management information system
New product and price master file
Unit stock control system


Optimisation Initiatives:
Transport planning system
Warehouse operational review


Current Position:
Product and price file with no view of company or store level stocks
No transport planning systems 
Excel based analysis

Physical Logistics
Aspirational:
Integrated transport planning and warehouse management system
Management information system
New product and price master file system
Unit stock control system



Optimisation Initiatives:
Tactical changes to legacy (eg earlier DISC)
Warehouse operational review


Current Position:
2 warehouse management systems, neither one of which supports E2E process
Complete lack of integration between WMS and stock systems

Manage Replenishment

Aspirational:
DC level product forecasting to improve supplier availability
Automated supplier re-ordering with orders balanced across DCs 
Automated store replenishment based on sales and forecast data
New product and price master file system
Unit stock control system

Optimisation Initiatives:
Order Pad onto hand held and incorporate a suggested order for frozen and ambient
WREP developments to provide suggested supplier re-orders
SMS2 enhancements for fresh

Current Position:
SMS2 provides centralised allocation/ replenishment for fresh areas, semi automated supplier re-ordering
WREP provides manual support for ambient and frozen supplier re-ordering
Order Pad provides manual store based replenishment (in-store)
No forecasting systems

Presentation Title  | Confidential  |   Document ID

94

---

## Slide 95

**Title:** “Sell” Supply Chain Processes – Systems Initiatives

Sell Products
Aspirational:
Integrated EPOS systems throughout the store
Price changes applied automatically and linked to SEL/POS systems
Stock management to focus on counting and shrinkage, as opposed to replenishment and stock room
Stock management integrated to WMS and other supply chain systems

Optimisation Initiatives:
HHT enhancements for stock counting and other stock management activities

Current Position:
Multiple EPOS systems
SEL system
POS system (EPISYS)

Serve Customers
Aspirational:
HHT based stock management and shop floor replenishment systems to support on-shelf replenishment
Integrated planogram printing system
Customer information support through the tills and other systems in store



Optimisation Initiatives:
HHT enhancements for stock management activities 


Current Position:
Some HHT functionality for store stock management
SEL system
POS systems
Planogram printing system

Manage Branch

Aspirational:
Management information systems to support store management processes
Staff scheduling systems to support more flexible staff rostering
Automated cash management systems 
Automated administration wherever possible (e use of Intranet and Forms based systems)

Optimisation Initiatives:
In store process review
Staff rota automation

Current Position:
Staff scheduling essentially manual and based on a fixed roster
Cash management is semi automated (BCP)

Presentation Title  | Confidential  |   Document ID

95

---

## Slide 96

**Title:** “Processing” Finance Processes – Systems Initiatives

Accounts Payable (Trade and GNFR)

Aspirational:
Full three way matching of all invoices on core Peoplesoft system for trade and GNFR
Use of self invoicing for key suppliers with good delivery and invoice track record
EDI used to transfer all financial information between suppliers and business
Payment results from matched invoice, not from management authorisation

Optimisation Initiatives:
Limited integration of Tranman and Archebus
Scanning and OCR to capture invoice information and improve matching process

Current Position:
All invoices and other financial information keyed in manually and then matched (largely manually) for all areas
GNFR orders not on systems – long manual authorisation process

Purchase Order Processing
Aspirational:
Integrated financial management system (Peoplesoft) to support POP
Some source POP systems will still exist as point solutions for specific areas of the business (eg Tranman but will be integrated
All orders on Peoplesoft
EDI to transmit all orders to suppliers 
e-Catalogues for GNFR supplies

Optimisation Initiatives:
Tranman and Archebus to feed Peoplsoft but not all orders and large degree of manual processing for GNFR

Current Position:
Manual ordering for all GNFR areas
Orders for Trade but not on legacy ledgers

Accounts Receivable Retail
Aspirational:
Sales fully integrated into ledger systems (Peoplesoft) from EPOS 
All other AR transactions sourced in Peoplesoft





Optimisation Initiatives:
None 


Current Position:
Manual processing of sales into legacy ledgers 
Manual reconciliation against Trading Information System

Presentation Title  | Confidential  |   Document ID

96

---

## Slide 97

**Title:** “Control” Finance Processes – Systems Initiatives

Cash Management
Aspirational:
Bank reconciliation using PeopleSoft Treasury functionality
Automated Supplier payments (BACS, SWIFT etc)




Optimisation Initiatives:
Improved cheque printing
BCP enhancements



Current Position:
Manual cash to EPoS reconciliation in store
Semi automatic bank reconciliation
Electronic bank statements

Fixed Assets
Aspirational:
Integrated Fixed Asset register
Electronic journal depreciation entry to GL
Automated reconciliations




Optimisation Initiatives:
None




Current Position:
Stand alone mainframe application
Manual update of fixed asset register
Depreciation charge at asset group level manually input to GL

Presentation Title  | Confidential  |   Document ID

97

---

## Slide 98

**Title:** “Reporting” Finance Processes – Systems Initiatives

General Accounting & Reporting
Aspirational:
EPoS Margin at unit level
Performance reporting from Data Warehouse
Integrated MIS reporting to pre-defined KPI’s and measures
Financial and non Financial reporting capability


Optimisation Initiatives:
Improved margin reporting and control
Actual financial reporting to budget direct from GL
Flexible reporting capability from GL


Current Position:
Mainframe General Ledger
Actual financials only
No time recorded Ledger postings
Limited GL reporting functionality

Budgeting & Forecasting
Aspirational:
Defined Corporate Strategy
Budgets linked to Strategy
Management performance targets linked to budgets
Mechanism to manage performance and drive management control


Optimisation Initiatives:
Actual financials reported to budget in General Ledger




Current Position:
Annual budget process on spreadsheets
Budgets to be input to PeopleSoft GL

Presentation Title  | Confidential  |   Document ID

98

---

## Slide 99

**Title:** Appendix II – Business Initiatives – Applications to be Replaced

---

## Slide 100

**Title:** Beyond “Optimisation” – Category Management Systems Scope

Presentation Title  | Confidential  |   Document ID

100

---

## Slide 101

**Title:** Beyond “Optimisation” – Store Space and Range Optimisation Systems Scope

Presentation Title  | Confidential  |   Document ID

101

---

## Slide 102

**Title:** Beyond “Optimisation” – Stock Management and Sales Based EPOS Margin Systems Scope

Presentation Title  | Confidential  |   Document ID

102

---

## Slide 103

**Title:** Beyond “Optimisation” – Integrated Transport and Warehouse Management Systems Scope (including forecasting and replenishment)

Presentation Title  | Confidential  |   Document ID

103

---

## Slide 104

**Title:** Beyond “Optimisation” – Finance Re-engineering Systems Scope

Presentation Title  | Confidential  |   Document ID

104

---
