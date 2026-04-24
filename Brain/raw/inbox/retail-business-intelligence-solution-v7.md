---
date: 2026-04-23
type: raw
source: Brain/raw/inbox/GAP/GAP BI/RBIS background/Retail Business Intelligence Solution V7.ppt
tags: [secure, rbis, ibm, retail-bi, bst, rdwm, gap, 2005, spine-candidate]
project: secure
status: unprocessed
---

# Retail Business Intelligence Solution V7

## Source

File: `Brain/raw/inbox/GAP/GAP BI/RBIS background/Retail Business Intelligence Solution V7.ppt`
Size: 4,147,200 bytes (Oct 31 2005)
Companion: `Brain/raw/inbox/GAP/GAP BI/RBIS background/RBIS Update.PDF` (Sep 21 2005)
Slides: 45
Images extracted: 77 (in `/tmp/rbis-extract/images/`)
Extraction tooling: soffice .ppt→.pptx + python-pptx structured walk + speaker notes

## Reading guide

- The deck is the IBM Retail BI canonical decomposition: **RDW** (warehouse) → **RDWM** (logical model, 71 subject areas, 671 entities, 4067 attrs) → **RBSTs** (Retail Business Solution Templates) → **Reports**.
- Slide 19 is the spine candidate — five-domain BST grid (Customer, Products & Services, Merchandising, Store Operations, Multi-Channel/Corporate Finance).
- Slides 38–42 enumerate sample BSTs + their reports per domain. This is the cell-level matrix.
- No CBM (Component Business Model) explicit reference. RBIS is the BI/data-model layer; CBM is its operating-model cousin. They map but are not the same artifact.

## Full transcription (slide-by-slide)

Source: `Brain/raw/inbox/GAP/GAP BI/RBIS background/Retail Business Intelligence Solution V7.ppt`
Slides: 45

---

## Slide 1

**Title:** Retail Business Intelligence Solutionv7 Master Presentation

```
[PlaceHolder 1 (0.32,3.65)]
  Retail Business Intelligence Solutionv7 Master Presentation
[shape (-0.73,7.1)]
  DTG
[shape (-0.73,7.1)]
  DTG
```

**Speaker notes:**

Chart 1: Title Slide
Hello and welcome to this presentation where we will take a close look at how you can build a strong platform for leveraging your information assets and at how IBM business intelligence solutions can help.  My name is XXXX  and I am the xxxxxxx.
 



Author: Daniel Graham/Somers/IBM   March 2004

---

## Slide 2

**Title:** Agenda

```
[PlaceHolder 1 (0.32,0.68)]
  Agenda
[PlaceHolder 2 (0.98,1.43)]
  Key Retail Business Issues Addressed by BI 
  The Retail Enterprise Data Warehouse
  Sample Scenario
  Advanced Analytics
  RBST’s in Detail
```

---

## Slide 3

**Title:** Retail Industry Trends Addressed By Business Intelligence

```
[PlaceHolder 1 (0.67,2.67)]
  Retail Industry Trends Addressed By Business Intelligence
```

---

## Slide 4

**Title:** Retail leaders will enhance traditional intuitive approaches with Advanced Analytics

```
[PlaceHolder 1 (1.0,0.68)]
  Retail leaders will enhance traditional intuitive approaches with Advanced Analytics
[shape (0.46,3.83)]
  Enterprise
  Data Management
[shape (0.36,3.27)]
  POS
[shape (0.11,5.57)]
  In-store monitoring
[shape (0.36,2.81)]
  Market research
[shape (1.56,3.11)]
  ERP
[shape (1.43,5.61)]
  Vendor data
[shape (0.62,6.16)]
  Supply chain
[shape (0.61,1.7)]
  Increased Performance via Systematic Intelligence
[shape (0.4,7.08)]
  Source: IBM Institute for Business Value
[shape (1.19,2.91)]
  RFID
[GROUP: ]
  [shape (2.52,3.4)]
    1100 10 01 10010
  [shape (3.99,3.37)]
    111010 0 0 1 0 01101
  [shape (3.25,3.27)]
    1100 10 01 10010 11 1 1
  [IMAGE pos=(2.91,4.08) size=(1.39x0.92) -> slide_04_pic_157.jpg]
  [shape (2.39,2.17)]
    Real-time analytics, decision support, and predictive intelligence…
  [shape (2.57,5.5)]
    …augmenting traditional creative/intuitive methods
[shape (0.15,2.17)]
  Customer, operational, and competitive data
[GROUP: ]
  [GROUP: ]
    [IMAGE pos=(5.48,2.84) size=(0.69x0.89) -> slide_04_pic_164.jpg]
    [shape (5.23,3.7)]
      Customers
  [GROUP: ]
    [IMAGE pos=(5.48,4.2) size=(0.69x0.89) -> slide_04_pic_167.jpg]
    [shape (5.23,5.09)]
      Store Ops
  [GROUP: ]
    [shape (5.07,6.48)]
      Supply Chain
    [IMAGE pos=(5.48,5.59) size=(0.69x0.89) -> slide_04_pic_171.jpg]
  [shape (5.18,2.17)]
    Business insights
[GROUP: ]
  [shape (7.18,2.29)]
    Optimized operations
  [shape (7.15,4.07)]
    Stores
    Store design and presentation
    Employee management
  [shape (7.15,2.82)]
    Merchandising
    Assortment planning
    Pricing and promotions
  [shape (7.15,5.56)]
    Supply Chain
    Demand forecasting
    Inventory management
    Warehouse management
```

**Speaker notes:**

Many retailers caught in the gunsights of Wal-Mart, Tesco, and similar mega-retailers are, unsurprisingly, focused on reducing costs in order to afford lowering prices and stay “in the game”.  But we would caution companies to heed the lessons of Kmart – where trying to compete on price led to a downward spiral of poor service, decreased customer satisfaction, and further losses.

Instead, retailers need to “play smarter”, not just “harder” with a sole focus on costs.  And so the point we made about customer insights in the previous imperative applies equally well to core retail operations – not just customer management but also merchandising, store operations, and supply chain management.  The successful retailers of the future will have highly flexible operations driven by what we call “systematic intelligence”.

Retailers have a wealth of data at their disposal – employee and enterprise data through ERP; supply chain data, such as orders, inventories, and forecasts; supplier data including account-specific services (such as category management); competitive information through more structured and formal information gathering and third-party information providers; and soon the explosion of RFID data, whether in the supply chain or in the store.

[click mouse to animate]

The challenge is to augment traditional, intuitive approaches to decision-making with the advanced analytical tools that are increasingly available. 
Automated, real-time analytics
Data-driven decision support tools
Predictive modeling (e.g., for requirements forecasting, capacity allocation, or resource assessment)

[click mouse to animate]

…And thus to generate new insights about customers, operations and supply chain conditions…

[click mouse to animate]

..and ultimately to reach a higher level of operating excellence.
For instance, how can you boost profitability another 20-30% by having the capability to optimize prices or markdowns at the store-level on a weekly or even daily basis?  Are you giving up too much margin, or not maximizing demand?  How can you figure this out, and how can you act upon it quickly?

---

## Slide 5

**Title:** Business Intelligence is Critical to Achieving These Goals

```
[PlaceHolder 1 (0.0,0.67)]
  Business Intelligence is Critical to Achieving These Goals
[shape (0.07,1.21)]
  BI addresses pain points in the following processes:
```

---

## Slide 6

**Title:** It’s all about the Customer…

```
[PlaceHolder 1 (0.24,0.53)]
  It’s all about the Customer…
[PlaceHolder 2 (0.45,1.72)]
  Acquire, retain, & extend customer’s lifetime value
  Get the right customers
  Retain the profitable ones
  Migrate low profit clients to low cost channels
[shape (0.43,4.46)]
  Solution areas
  Customer segmentation
  Customer acquisition 
  Retention & Loyalty programs
  Winback Programs
[shape (5.46,4.48)]
  Campaign management
  Market basket analysis
  Profitability analysis
[shape (-0.73,7.1)]
  DTG
[IMAGE pos=(6.0,1.68) size=(2.78x2.64) -> slide_06_pic_190.jpg]
```

**Speaker notes:**

Customer analytics give your company a better understanding of consumer needs and how they vary.   First, we have to start with the customer’s life events and current attributes.  Who are they, what do they want to buy, are they a prospect now or later?  What is their lifetime value and how do we ensure that the interactions with the client are profitable? Some clients are unprofitable early in life –for example university students – but later are the best customers –now that the university educated person is a professional with 3 children and a home.  So lifetime value is one measure we want for each type of customer.
Dozens of customer relationship experts have declared that acquiring a customer costs 5 times more than keeping one.  Prospecting to new “white space” clients is expensive and solicitation response rates are usually poor. Consequently, developing a plan based on customer segmentation profiles, similar prospects, and personalized offers is the only way to ensure your prospecting money is well spent. 
Existing customers tend to produce the bulk of revenues and profits which means that customer loyalty is a competitive necessity.  So losing current customers –churn or lapses-- can be devastating to the financial bottom line.  Most companies have the data to detect and predict which consumers will “attrite” and go to the competition.  Some customer segments are high risk whereas certain interactions with the customer are telltale signs they will abandon you and go elsewhere.  However, your first decision should be to determine if the client is profitable before spending marketing or sales energy on retaining them as a customer.
All of these activities have been proven to be effective using IBM’s DB2 data mining and data warehouse technologies.  Gathering past transactions and even externally purchased data is the best way to get a clear understanding of customer segments, propensities to purchase, buying patterns, and cross sell opportunities. Generally, we like to treat the customers as if they were a portfolio, like a mutual fund or bond fund.  We need to know when to invest, when to divest for the maximum value to the enterprise.   Using the DB2 relational database and statistics, IBM software can compute a prospects life time value, the next most likely purchase, even the month or quarter that purchase is most likely.  Knowing this, you can optimize your marketing and sales investments to mutual benefit with your clients. IBM DB2 deployments (State Farm) have shown the ability to improve the leads to closure rate from 24-to-1 down to 7-to-1, that is 7 cold calls to yield one closed deal.  Similarly, we can dramatically cut the investment in direct and indirect campaigns while increasing the success per campaign from a mere 3% response rate to 8-11% response rate (Credit Union of Texas).



D.Graham

---

## Slide 7

**Title:** …and Collaborative Commerce

```
[PlaceHolder 1 (0.3,0.63)]
  …and Collaborative Commerce
```

---

## Slide 8

**Title:** Why You Need an Enterprise Data Warehouse

```
[PlaceHolder 1 (0.71,0.69)]
  Why You Need an Enterprise Data Warehouse
[PlaceHolder 2 (0.59,1.54)]
  Bernard Liautaud – CEO of Business Objects in Business Week Online 8-31-05
  “…. because CRM really automates your sales force. Business intelligence is at a different level. For instance, you want to know what your most profitable products are. Where are the data to help with that analysis? Well some of it is in the CRM, some is in the manufacturing system, and some is in the finance system. So you need to have a solution that cuts across all the different types of systems. 	… on average companies have between five and seven different types of databases and between 100 and 300 different types of applications. By definition, the infrastructure of companies is extremely heterogeneous. Even a company that says "I am an SAP shop" has hundreds of applications that are not covered by SAP, and when they do the analysis of their business, they need to have them in the fold. “
  Forrester Report 8-9-05 Retail Gets Ready for In-Store Analytics
  In the past, a lack of accessible above-store information, either because of constrained bandwidth or decentralized store applications, hindered real-time alerts and analytics for store users.  But while centralized deployments of in-store applications have come in and out of favor in the past, the pressure is on to increase them, as applications for both store employees and customers increasingly rely on information that is not held locally at the store. For in-store analytics and alerting, it means an opportunity to provide stores with information that they haven’t had regular access to before, such as how a store compares to its peers. Retailers should be cautiously optimistic about the opportunity — balancing a desire to provide stores with better tools with the temptation to provide too much information.
```

---

## Slide 9

**Title:** Retail Enterprise Data Warehouse

```
[PlaceHolder 1 (0.67,2.67)]
  Retail Enterprise Data Warehouse
```

---

## Slide 10

**Title:** The IBM Retail Business Intelligence Solution:

```
[PlaceHolder 1 (0.17,0.95)]
  The IBM Retail Business Intelligence Solution:
[PlaceHolder 2 (0.67,1.94)]
  Provides a consistent view of information across the enterprise.  
  Delivers advanced analytics and insight into core Retail process areas:  
  Customer Management,  Product & Service Management, Store Operations, Merchandising, Multi-Channel Management, Finance, HR, & Supply Chain.  
  Enables rapid, phased deployment
  Offers a packaged, customizable, open environment 
  Leverages a retailer’s existing investment in people, process and technology 
  Combines IBM’s leading edge research, services, systems and software with deep industry knowledge.
[IMAGE pos=(5.83,2.02) size=(3.42x4.11) -> slide_10_pic_201.png]
```

---

## Slide 11

**Title:** The IBM Retail Business Intelligence Solution includes:

```
[PlaceHolder 1 (0.17,0.95)]
  The IBM Retail Business Intelligence Solution includes:
[PlaceHolder 2 (1.22,1.94)]
  Retail Business Intelligence Reference Architecture and ARTS Compliant Enterprise Data Warehouse Model
  Retail Optimized Business Intelligence Infrastructure (server, storage and software)
  Retail specific templates for quick start analytics and reporting for Store Operations, Merchandising, Customer Management, Product Management and Multi-Channel
  Retail Design and Implementation Services to help retailers prioritize their high business impact areas and allow for an easy deployment
```

---

## Slide 12

**Title:** Reporting without an Enterprise Data Warehouse

```
[PlaceHolder 1 (0.27,0.49)]
  Reporting without an Enterprise Data Warehouse
[shape (2.9,1.37)]
  Inconsistent
  Reporting
[shape (2.9,3.59)]
  High 
  Maintenance 
  Costs
[shape (5.47,1.6)]
  Incorrect 
  Reporting
[shape (3.43,5.22)]
  Slow Report 
  Creation
[shape (5.24,3.22)]
  No 
  Consolidated 
  View
[shape (5.32,5.46)]
  Duplication 
  of  Work
[GROUP: ]
  [GROUP: ]
    [GROUP: ]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bee8ef0>)]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bee8ef0>)]
      [GROUP: ]
      [IMAGE pos=(8.42,2.96) size=(0.4x0.41) -> slide_12_pic_254.png]
    [shape (7.6,2.28)]
      Customer
      Management
  [GROUP: ]
    [GROUP: ]
      [GROUP: ]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bee8ef0>)]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bee8ef0>)]
        [GROUP: ]
        [IMAGE pos=(8.4,6.56) size=(0.4x0.41) -> slide_12_pic_268.png]
      [shape (7.61,5.88)]
        Store
        Operations
    [GROUP: ]
      [GROUP: ]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2250>)]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2250>)]
        [GROUP: ]
        [IMAGE pos=(8.41,5.35) size=(0.4x0.41) -> slide_12_pic_281.png]
      [shape (7.62,4.65)]
        Product & Services
        Management
    [GROUP: ]
      [shape (7.92,1.1)]
        Corporate
        Finance
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1e40>)]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1e40>)]
      [GROUP: ]
      [IMAGE pos=(8.43,1.81) size=(0.4x0.41) -> slide_12_pic_294.png]
    [GROUP: ]
      [shape (7.92,3.47)]
        Merchandising
        Management
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1e40>)]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1e40>)]
      [GROUP: ]
      [IMAGE pos=(8.43,4.18) size=(0.4x0.41) -> slide_12_pic_306.png]
[GROUP: ]
  [GROUP: ]
  [shape (0.81,1.83)]
    Sales
  [shape (0.79,3.75)]
    Credit
    Card
  [shape (0.76,2.76)]
    Inventory
  [shape (0.74,2.3)]
    Purchsg
  [shape (0.68,3.36)]
    Order Mgmt
  [shape (0.74,4.14)]
    General
    Ledger
  [shape (1.3,1.07)]
    Operational
    Sources
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [shape (0.79,6.53)]
    Other
    Apps
  [GROUP: ]
  [shape (1.0,4.75)]
    Hr
  [shape (0.84,5.2)]
    Payroll
  [shape (0.91,5.6)]
    Cash
    Mgmt
  [shape (0.74,6.14)]
    Investmnts
```

---

## Slide 13

**Title:** Consistent Reporting leveraging an enterprise Data Warehouse

```
[PlaceHolder 1 (0.17,0.49)]
  Consistent Reporting leveraging an enterprise Data Warehouse
[GROUP: ]
  [GROUP: ]
  [shape (3.11,3.75)]
    Retail Data Warehouse
      Enterprise Wide
      Consistent Reporting
      Reuse of extracts from Operational Sources
      Cost Effective Reporting
      Support all types of Sources & Reporting Apps 
      Proven Scalability
[GROUP: ]
  [GROUP: ]
  [shape (0.81,1.83)]
    Sales
  [shape (0.79,3.75)]
    Credit
    Card
  [shape (0.76,2.76)]
    Inventory
  [shape (0.74,2.3)]
    Purchsg
  [shape (0.68,3.36)]
    Order Mgmt
  [shape (0.74,4.14)]
    General
    Ledger
  [shape (1.3,1.07)]
    Operational
    Sources
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [GROUP: ]
  [shape (0.79,6.53)]
    Other
    Apps
  [GROUP: ]
  [shape (1.0,4.75)]
    Hr
  [shape (0.84,5.2)]
    Payroll
  [shape (0.91,5.6)]
    Cash
    Mgmt
  [shape (0.74,6.14)]
    Investmnts
[GROUP: ]
  [GROUP: ]
    [GROUP: ]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1fd0>)]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1fd0>)]
      [GROUP: ]
      [IMAGE pos=(8.42,2.96) size=(0.4x0.41) -> slide_13_pic_543.png]
    [shape (7.6,2.28)]
      Customer
      Management
  [GROUP: ]
    [GROUP: ]
      [GROUP: ]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1fd0>)]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a1fd0>)]
        [GROUP: ]
        [IMAGE pos=(8.4,6.56) size=(0.4x0.41) -> slide_13_pic_557.png]
      [shape (7.61,5.88)]
        Store
        Operations
    [GROUP: ]
      [GROUP: ]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2110>)]
        [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2110>)]
        [GROUP: ]
        [IMAGE pos=(8.41,5.35) size=(0.4x0.41) -> slide_13_pic_570.png]
      [shape (7.62,4.65)]
        Product & Services
        Management
    [GROUP: ]
      [shape (7.92,1.1)]
        Corporate
        Finance
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2430>)]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2430>)]
      [GROUP: ]
      [IMAGE pos=(8.43,1.81) size=(0.4x0.41) -> slide_13_pic_583.png]
    [GROUP: ]
      [shape (7.92,3.47)]
        Merchandising
        Management
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2430>)]
      [IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2430>)]
      [GROUP: ]
      [IMAGE pos=(8.43,4.18) size=(0.4x0.41) -> slide_13_pic_595.png]
```

---

## Slide 14

```
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bdad530>)]
[shape (4.06,3.59)]
  Transactions
  POS
  Product Change
  Customer Touch
[IMAGE pos=(2.18,3.99) size=(0.71x0.7) -> slide_14_pic_601.png]
[GROUP: ]
  [IMAGE pos=(7.1,4.1) size=(0.62x0.38) -> slide_14_pic_603.png]
  [IMAGE pos=(7.1,5.09) size=(0.62x0.46) -> slide_14_pic_604.png]
  [IMAGE pos=(7.1,4.55) size=(0.62x0.48) -> slide_14_pic_605.png]
  [IMAGE pos=(7.1,5.6) size=(0.65x0.44) -> slide_14_pic_606.png]
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bdad530>)]
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bdad530>)]
[shape (6.72,4.24)]
  Web
[shape (6.41,4.77)]
  Call Center
[shape (6.55,5.25)]
  Catalog
[shape (6.49,5.65)]
  Pervasive
[shape (3.98,5.96)]
  Inventory Analysis 
  Assortment / Allocation Analysis 
  Promotion Analysis 
  Physical Merchandising
  Space Management Analysis 
  Pricing Analysis
[shape (0.3,4.14)]
  Core Business Reporting 
  Product Analysis
  Vendor Performance
  Service Delivery
  Planning and Forecasting
[shape (0.87,1.47)]
  Purchase Profiles 
  Customer Profiles 
  Product Purchasing Recency, Frequency & Quantity 
  Campaign & Promotion Analysis 
  Cross Purchase Behavior Analysis 
  Target Product Analysis 
  Customer Movement Dynamic 
  Market Basket Analysis and Clienteling
[shape (7.5,1.87)]
  Loss Prevention 
  Store Location Analysis 
  Store Optimization Staffing
[shape (7.65,5.03)]
  e-Commerce Analysis 
  Catalog Analysis 
  Call Centre Performance
[shape (6.25,3.78)]
  Location
[shape (0.4,0.75)]
  IBM’s RDW 1st Generation: Functional Areas Addressed
[shape (0.3,3.67)]
  Product & Services Group
[shape (3.31,5.74)]
  Merchandising  Group
[shape (6.47,1.61)]
  Store Operations Group
[shape (7.65,4.56)]
  Multi-Channel
  Group
[shape (1.74,1.25)]
  Customer Management Group
[shape (0.69,5.86)]
  Capital Allocation
  Partner Credit Risk
  Finance Management
  Income Analysis
[shape (0.64,5.64)]
  Corporate Finance
[shape (6.88,6.26)]
  A end-to-end 
  cross-organizational 
  perspective
```

---

## Slide 15

```
[IMAGE pos=(1.0,4.58) size=(2.42x1.42) -> slide_15_pic_636.png]
[shape (0.42,6.02)]
  M1 Tool
[GROUP: ]
  [IMAGE pos=(0.42,3.0) size=(1.08x0.64) -> slide_15_pic_639.png]
  [shape (1.57,2.92)]
    Retail Services Data Model (RSDM) 
    Classification (Meta data) model for defining business meaning across all models and databases
[GROUP: ]
  [IMAGE pos=(0.42,1.25) size=(1.08x0.63) -> slide_15_pic_642.png]
  [shape (1.58,1.17)]
    Retail Data Warehouse Model (RDWM)  
    Logical Entity-Relationship Model for the central data warehouse
[GROUP: ]
  [IMAGE pos=(0.42,2.07) size=(1.08x0.68) -> slide_15_pic_645.png]
  [shape (1.57,2.0)]
    Retail Business Solution Templates (RBSTs)  
    Logical Measure/Dimension Models for multidimensional analysis
[shape (0.35,0.52)]
  The IBM DB2 RDW Models  3 models in 1
[shape (0.43,6.6)]
  IBM’s solution is unique – other competitors have RDWM equivalent model only
[IMAGE pos=(4.17,4.75) size=(4.0x1.06) -> slide_15_pic_649.png]
[GROUP: ]
  [IMAGE pos=(3.5,4.75) size=(0.67x0.5) -> slide_15_pic_651.png]
  [IMAGE pos=(3.5,5.25) size=(0.67x0.5) -> slide_15_pic_652.png]
  [IMAGE pos=(3.5,4.25) size=(0.67x0.5) -> slide_15_pic_653.png]
  [IMAGE pos=(4.17,4.25) size=(0.67x0.5) -> slide_15_pic_654.png]
  [IMAGE pos=(4.83,4.25) size=(0.67x0.5) -> slide_15_pic_655.png]
  [IMAGE pos=(5.5,4.25) size=(0.67x0.5) -> slide_15_pic_656.png]
  [IMAGE pos=(6.17,4.25) size=(0.67x0.5) -> slide_15_pic_657.png]
  [IMAGE pos=(6.83,4.25) size=(0.67x0.5) -> slide_15_pic_658.png]
  [IMAGE pos=(7.5,4.25) size=(0.67x0.5) -> slide_15_pic_659.png]
  [IMAGE pos=(8.17,4.75) size=(0.67x0.5) -> slide_15_pic_660.png]
  [IMAGE pos=(8.17,5.25) size=(0.67x0.5) -> slide_15_pic_661.png]
  [IMAGE pos=(8.17,4.25) size=(0.67x0.5) -> slide_15_pic_662.png]
  [IMAGE pos=(3.5,5.75) size=(0.67x0.5) -> slide_15_pic_663.png]
  [IMAGE pos=(4.17,5.75) size=(0.67x0.5) -> slide_15_pic_664.png]
  [IMAGE pos=(4.83,5.75) size=(0.67x0.5) -> slide_15_pic_665.png]
  [IMAGE pos=(5.5,5.75) size=(0.67x0.5) -> slide_15_pic_666.png]
  [IMAGE pos=(6.17,5.75) size=(0.67x0.5) -> slide_15_pic_667.png]
  [IMAGE pos=(6.83,5.75) size=(0.67x0.5) -> slide_15_pic_668.png]
  [IMAGE pos=(7.5,5.75) size=(0.67x0.5) -> slide_15_pic_669.png]
  [IMAGE pos=(8.17,5.75) size=(0.67x0.5) -> slide_15_pic_670.png]
[GROUP: ]
  [shape (5.41,1.22)]
    
  [shape (5.85,1.16)]
    Consolidate the data from throughout the enterprise into one comprehensive view
[GROUP: ]
  [shape (5.42,2.18)]
    
  [shape (5.86,2.06)]
    Organize the data into specific areas for advanced analysis… guided analysis
[GROUP: ]
  [shape (5.41,3.09)]
    
  [shape (5.85,3.01)]
    Define the business meaning and relationships of all the data captured in the RDWM and RBST model
```

---

## Slide 16

**Title:** The RDW Architecture

```
[GROUP: ]
  [shape (-0.29,4.92)]
    Physical Design
  [shape (-0.23,1.79)]
    Logical Design
[PlaceHolder 1 (-0.0,0.49)]
  The RDW Architecture
[GROUP: ]
  [shape (0.81,1.16)]
    Data Warehouse design specific for Retail Organizations gives full enterprise DW blueprint
[GROUP: ]
  [shape (4.16,2.49)]
    Mapping between BSTs and RDWM enable rapid scoping
  [IMAGE pos=(5.73,1.45) size=(1.57x0.78) -> slide_16_pic_693.png]
  [shape (7.64,1.51)]
    Data Mart Templates for Retail Organizations, enable fast accurate requirements gathering
[GROUP: ]
  [shape (7.43,0.64)]
    RSDM provides overall corporate model with common language & terms
[GROUP: ]
  [shape (4.03,5.63)]
    ETL/Messaging
[GROUP: ]
  [shape (2.8,3.53)]
    Enterprise Data  Warehouse
  [GROUP: ]
  [GROUP: ]
  [shape (4.53,4.04)]
    Summary
  [GROUP: ]
  [shape (4.63,4.51)]
    Analysis
  [GROUP: ]
    [GROUP: ]
    [shape (2.77,4.18)]
      Staging
      Area
  [GROUP: ]
  [shape (3.61,4.09)]
    System
    Of
    Record
  [shape (3.53,5.0)]
    Classified 
    Sources
  [GROUP: ]
  [shape (4.59,4.94)]
    Feedback
[shape (6.73,5.69)]
  Data Mart 
  Structures
[shape (6.58,3.82)]
  ROLAP
[shape (6.59,4.9)]
  Relational
[IMAGE pos=(7.55,4.28) size=(0.32x0.33) -> slide_16_pic_762.png]
[shape (6.66,5.35)]
  Other
[shape (6.61,4.29)]
  OLAP 
  Server *
[shape (6.58,3.37)]
  Essbase
[IMAGE pos=(7.55,3.31) size=(0.32x0.33) -> slide_16_pic_766.png]
[GROUP: ]
[GROUP: ]
[GROUP: ]
[GROUP: ]
[GROUP: ]
[shape (0.98,3.45)]
  Sources
[shape (1.09,3.9)]
  POS
[shape (0.75,4.54)]
  Front 
  Office
[shape (0.51,6.48)]
  Other 
  Sources
[shape (0.7,6.16)]
  HR
[shape (0.81,5.16)]
  Accounting
[shape (0.51,5.67)]
  Inventory
[GROUP: ]
[GROUP: ]
[GROUP: ]
[GROUP: ]
[GROUP: ]
[GROUP: ]
[GROUP: ]
  [GROUP: ]
    [shape (8.39,3.12)]
      Business 
      Applications
    [shape (8.46,4.45)]
      Products
    [shape (8.46,3.71)]
      Customers
    [shape (8.46,4.08)]
      Merchandizing
    [shape (8.46,4.82)]
      Store Ops
    [shape (8.46,6.59)]
      Mgt  Reporting
    [shape (8.46,5.78)]
      Data Mining
    [shape (8.46,6.15)]
      Predictive
      Modeling
    [shape (8.25,5.26)]
      Data Analysis
       & Reporting
  [GROUP: ]
[GROUP: ]
  [shape (2.65,6.48)]
    Warehouse Management & Administration
    Metadata Management & Metadata Repository
  [GROUP: ]
[shape (0.8,2.24)]
  EDW designed for Retail Organizations can be generated over a series of manageable phases
[shape (7.42,2.44)]
  Data Mart DB design can be generated from Templates
[GROUP: ]
```

---

## Slide 17

**Title:** What is the RDWM?

```
[shape (0.05,2.66)]
  Enterprise-wide Logical Model
   Entity-Relationship 
   Consists of over 71 Subject Areas, 671 Entities, 4067 Attributes
  Fully defined and documented
[shape (1.35,1.02)]
  Contains : 
  Flexible System of Record
  Commonly-required Summaries
  Sample Analysis Schemas
  Feedback Area
[shape (4.17,1.19)]
  Intended to be customized
  Approx 80% of Customer’s Requirements for a Central Warehouse
[shape (6.99,1.19)]
  Low-level flexible model
  Generic
  “One-step from Physical”
[PlaceHolder 1 (0.17,0.47)]
  What is the RDWM?
[shape (2.01,0.05)]
  The RDW Environment
```

---

## Slide 18

**Title:** What are RBSTs? - Definitions

```
[PlaceHolder 1 (0.46,0.56)]
  What are RBSTs? - Definitions
[IMAGE pos=(0.61,2.09) size=(2.34x1.28) -> slide_18_pic_894.png]
[shape (3.82,1.6)]
  What are the Business Solution Templates?
  The Retail Business Solution templates are a grouping of measures and  dimensions that satisfy a particular business requirement.
  
  What are measures?
  Measures are facts that are used to quantify business performance indicators. These measures may be made up of other measures (known as sub-measures) in the context of the measure to which they contribute. An example of a Measure is 'Number Of Customers'
  
  What are dimensions?
  Dimensions consist of criteria or segments by which the measures may be broken down. Dimensions consist of at least one level of Dimension Members. An example of a Dimension is 'Time Period'
```

---

## Slide 19

**Title:** What do the RBSTs Cover? - Overview

```
[PlaceHolder 1 (0.23,0.58)]
  What do the RBSTs Cover? - Overview
[IMAGE pos=(2.41,1.2) size=(1.11x1.44) -> slide_19_pic_903.jpg]
[shape (3.49,1.21)]
  Campaign & Promotion Analysis
  Cross Purchase Behavior Analysis
  Cross Sell Analysis
  Customer Attrition Analysis
  Customer Complaints Analysis
  Customer Credit Risk Profile
  Customer Delinquency Analysis
  Customer Interaction Analysis
[shape (0.23,1.68)]
  Customer Management
[shape (0.21,3.86)]
  Products & 
  Services
  Management
[shape (3.35,2.77)]
  Assortment and Allocation Analysis
  Inventory Analysis
  Physical Merchandising / Space Management  Analysis
  Pricing Analysis
  Promotion Analysis
[shape (0.23,2.89)]
  Merchandising
  Management
[shape (5.62,5.04)]
  Non Performing Loan Analysis
  Organization Unit Profitability
  Performance Measurement
  Staffing Analysis
[shape (0.2,5.17)]
  Store Operations
  Management
[IMAGE pos=(2.4,5.0) size=(1.11x0.92) -> slide_19_pic_911.jpg]
[shape (3.35,3.99)]
  Business Performance Analysis
  Planning and Forecasting Analysis
  Product Analysis
  Product profitability
[shape (3.52,6.26)]
  Capital Allocation Analysis
  Credit Risk Analysis
[shape (0.21,6.15)]
  Corporate Finance
  Management
[shape (5.85,1.21)]
  Customer Lifetime Value Analysis
  Customer Loyalty
  Customer Movement Dynamics 
  Customer Profile Analysis
  Customer Profitability
  Involved Party Exposure
  Lead Analysis
  Market Analysis
[shape (7.86,1.38)]
  Market Basket Analysis
  Product Purchasing RFQ 
   Analysis
  Purchase Profile Analysis
  Target Product Analysis
[shape (3.35,5.04)]
  Activity Based Costing Analysis
  Location Exposure
  Location profitability
  Loss Prevention Analysis
[shape (7.73,5.04)]
  Store Location Analysis
  Store Optimization Analysis
  Suspicious Activity Analysis
[IMAGE pos=(2.43,2.77) size=(1.09x0.99) -> slide_19_pic_920.jpg]
[IMAGE pos=(2.41,3.86) size=(1.11x1.03) -> slide_19_pic_921.jpg]
[shape (5.62,3.99)]
  Service Delivery Analysis
  Transaction Profitability Analysis
  Vendor Performance Analysis
[shape (5.62,6.26)]
  Financial Management Accounting
  Income Analysis
[IMAGE pos=(2.37,6.04) size=(1.09x0.87) -> slide_19_pic_924.jpg]
```

---

## Slide 20

**Title:** What is the RSDM?

```
[PlaceHolder 1 (0.39,0.62)]
  What is the RSDM?
```

---

## Slide 21

**Title:** Why is IBM’s RDW Solution Important?

```
[PlaceHolder 1 (0.17,0.5)]
  Why is IBM’s RDW Solution Important?
[PlaceHolder 2 (0.17,1.5)]
  Retailer requirements:
  A system that allows integration of information related to: CRM, multi-channel order mgmt., inventory analysis, product sales analysis, trends, category management, promotional (markdown) analysis, product returns, dead inventory, increased product turns, reduced out-of-stocks, maximize promotional effectiveness, RFID, and provide cashier metrics.
  
  A well-organized, fast, and easy to access repository of analytics and metrics to support BPM and provide for “activity based monitoring” for real-time (on-demand) action to address business conditions in role-based portal (LOB) workplaces:  Merchant, Marketing, Store Operations.
[PlaceHolder 3 (5.2,1.5)]
  Value to Retailers:
  Essential to retail BPM:   Business Performance Management
  Sense and Respond
  Triggers and Alerts responding to business conditions
  Useful to Merchandisers for category mgmt., buying criteria, vendor analysis/performance, (markdown allowance)
  Valued by Marketing for CRM RFM and real-time promotions and offers.
  Real world use in Store Operations for real-time inventory alerts, labor scheduling, etc.
  Provides retailers with (not only) access to timely information; but provides for real-time alerts and triggers to business conditions
```

---

## Slide 22

**Title:** Embedded Advanced Analytics

```
[PlaceHolder 1 (0.17,0.56)]
  Embedded Advanced Analytics
[shape (0.42,1.76)]
  Solution Differentiator
  
  DB2 has a unique capability called Easy Mining that enables solutions based on data mining implemented in a business analyst’s workplace.  Reporting tool vendors have developed interfaces to allow the solutions to integrate with existing reporting capabilities.
  
  Embedded Business Solutions:
  
  Customer Segmentation
  Store Profiling
  Market Basket Analysis
  Promotion Targeting
[shape (5.0,1.7)]
  Why Should You Care?
  
  The business value of the solutions IBM is embedding in DB2  is well known.  Retailers get insights into how their products sell together and how their stores and customers perform.  These advanced analytical solutions were once reserved for retailers with sophisticated statistical staffs but can now be enjoyed by all retailers.
[IMAGE pos=(7.67,5.72) size=(1.13x0.7) -> slide_22_pic_938.png]
[shape (6.54,5.81)]
  Transaction
   File
[IMAGE pos=(7.73,4.72) size=(1.05x0.65) -> slide_22_pic_945.png]
[shape (7.36,5.4)]
  Segmentation, Promotions
[shape (7.36,6.47)]
  Market Basket Analysis
[shape (4.13,6.47)]
  Data Sources
[shape (3.89,5.5)]
  T Logs
[shape (4.07,4.51)]
  Customers
[shape (6.44,5.23)]
  Summary
   Table
```

---

## Slide 23

**Title:** Case Study   Mass Merchant

```
[PlaceHolder 1 (0.17,0.95)]
  Case Study   Mass Merchant
[shape (1.84,6.36)]
  $46B+ Mass Merchant Retailer
  1337 Stores in 47 States
[PlaceHolder 2 (0.16,1.56)]
  Challenge:  
  To create support across the company for an enterprise data warehouse solution in an environment that is highly silo’d
  To develop an enterprise view of financial profitability across all business areas, products and departments (Consumer Credit, Merchandising and Store Operations)
  
  Solution: 
  IBM’s Retail Business Intelligence Solution with the REDW Data Model
  Services to support customization of the model to stress financial reporting issues
  DB2 Data Warehouse Edition with Business Objects
  	
  Benefits:
  Now able to see the complete profitability picture
```

**Speaker notes:**

Target

---

## Slide 24

**Title:** Case Study   Specialty Apparel

```
[PlaceHolder 1 (0.17,0.95)]
  Case Study   Specialty Apparel
[shape (0.17,1.42)]
  Challenge:  
  Integrate and operate new Disney Store acquisition
  Develop enterprise view of store and product information in short time frame (6 months or less)
  Deliver transaction level information to end users which can be leveraged by the Finance, Marketing and other business functions within the organization
  Leverage, not re-do, processing and technology that is already being done by the finance and marketing teams
  
  Solution: 
  	Retail Business Intelligence Solution with Retail Enterprise Data Model
  	DB2 DWE
  	Alphablox
  
  Benefits:
  	Short time frames can be met and analytics leveraged
  	Marketing and Finance able to work on same page
[shape (6.48,5.86)]
  $1.2b specialty retailer focused on children 0-10
  Completed Disney Store acquisition in 2005
```

**Speaker notes:**

Target

---

## Slide 25

**Title:** Summary

```
[PlaceHolder 1 (0.38,0.61)]
  Summary
[PlaceHolder 2 (0.71,1.51)]
  Retailers are heading into the next generation of advanced analytics with a global perspective
  More and more they are incorporating close to real time decision capabilities
  ROI is mature so that adding more BI capabilities inside the enterprise is common
  Analyzing the store in real time is important 
  Open systems are driving standards based approaches
  User communities continue to grow 
  Delivery of data to executive decision makers is common
  Delivery to the store and store management
  A common foundation for supporting all of these activities is derived through an enterprise model
```

---

## Slide 26

**Title:** Sample Scenario

```
[PlaceHolder 1 (0.43,2.73)]
  Sample Scenario
```

---

## Slide 27

**Title:** Using an example “Back to School” promotion for children’s clothing

```
[PlaceHolder 1 (0.37,0.43)]
  Using an example “Back to School” promotion for children’s clothing
[PlaceHolder 2 (0.37,1.62)]
  Business Scenario
  Planning and execution of a children’s clothing promotion,across Merchandise, Marketing & Store Management functions
  
  Flow of this Scenario
  
  
  
  
  
  
  
  Technology components:
  Cognos as the front-end analysis tool, over an Intranet
  DB2 as the Data Warehouse RDBMS and OLAP service
  RDW  as the Retail Enterprise Data Warehouse Model, including classification of data 	meanings (metadata) and pre-defined analytic templates (BST’s)
[IMAGE pos=(8.55,1.62) size=(1.01x1.42) -> slide_27_pic_977.jpg]
[IMAGE pos=(7.6,1.31) size=(1.06x1.42) -> slide_27_pic_978.jpg]
[GROUP: ]
  [shape (0.59,3.51)]
    1
  [shape (0.59,4.04)]
    2
  [shape (0.59,4.54)]
    3
  [shape (1.06,3.51)]
    Identification of a new merchandising opportunity for a key customer segment
  [shape (1.06,4.04)]
    Identification of a relevant offer based on purchasing behaviour
  [shape (1.06,4.54)]
    Planning for execution of the promotion at store
[shape (2.01,0.06)]
  RDW typical usage scenario
```

---

## Slide 28

```
[shape (0.16,0.74)]
  “Back to School” promotion : Childrens Clothing Merchandiser identifies an opportunity with a customer segment, identified from store-card usage
[IMAGE pos=(0.59,1.29) size=(8.7x5.53) -> slide_28_pic_988.png]
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10bdad2b0>)]
[shape (0.59,4.92)]
  Purchase Profiles 
  Customer Profiles 
  Product Purchasing Recency, Frequency & Quantity 
  Campaign & Promotion Analysis 
  Cross Purchase Behavior Analysis 
  Target Product Analysis 
  Customer Movement Dynamic 
  Market Basket Analysis and Clienteling
[shape (0.59,4.6)]
  Source: RDW Customer Management
[GROUP: ]
  [shape (8.51,0.49)]
    1
  [shape (8.9,0.49)]
    2
  [shape (9.29,0.49)]
    3
[shape (2.01,0.06)]
  RDW typical usage scenario
```

---

## Slide 29

```
[shape (0.24,0.74)]
  “Back to School” promotion : Childrens Clothing Merchandiser identifies an offer based on ‘affinity’ with another prod dept (calculators)
[GROUP: ]
  [shape (8.76,0.55)]
    1
  [shape (9.15,0.55)]
    2
  [shape (9.55,0.55)]
    3
[IMAGE pos=(2.03,2.23) size=(7.94x4.91) -> slide_29_pic_1004.png]
[IMAGE pos=(0.27,1.23) size=(5.0x0.95) -> slide_29_pic_1007.png]
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a23e0>)]
[shape (-0.04,5.15)]
  Purchase Profiles 
  Customer Profiles 
  Product Purchasing RFQ 
  Campaign & Promotion Analysis 
  Cross Purchase Behavior Analysis 
  Target Product Analysis 
  Customer Movement Dynamic 
  Market Basket Analysis and Clienteling
[shape (0.04,4.38)]
  Source: RDW Customer Management
[shape (2.01,0.06)]
  RDW typical usage scenario
```

---

## Slide 30

```
[IMAGE pos=(2.03,1.31) size=(7.77x4.97) -> slide_30_pic_1012.png]
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a2520>)]
[shape (1.1,5.9)]
  Loss Prevention 
  Store Location Analysis 
  Store Optimization Staffing
[shape (0.35,0.75)]
  “Back to School” promotion : Childrens Clothing Once aware of the impending promotion, the Store Manager looks at previous year revenue and staffing levels – preparing the ‘balancing act’
[GROUP: ]
  [shape (8.66,0.54)]
    1
  [shape (9.06,0.54)]
    2
  [shape (9.45,0.54)]
    3
[shape (-0.16,5.39)]
  Source: RDW Store Operations
[shape (2.01,0.06)]
  RDW typical usage scenario
```

---

## Slide 31

**Title:** Advanced Analytics

```
[PlaceHolder 1 (0.43,2.73)]
  Advanced Analytics
```

---

## Slide 32

**Title:** Solutions through Analytics

```
[PlaceHolder 1 (0.24,0.48)]
  Solutions through Analytics
[PlaceHolder 2 (0.37,1.68)]
  Query
  Question and Answer
  “Drill Down”
  Standard Reports
  Online Analytical Processing (OLAP)
  Multi-dimensional queries and reports
  Complex Q&A
  Data Mining (Advanced Analytics)
  Discover previously unknown trends and patterns
  “We don’t know what we don’t know”
[shape (0.77,6.26)]
  IBM has a new approach to make data mining easy
[IMAGE pos=(5.99,2.57) size=(3.82x2.5) -> slide_32_pic_1031.jpg]
```

**Speaker notes:**

We can loosely group the methods of gathering and analyzing information from databases into three areas, query, OLAP and mining.  
Query is exactly what its name implies, the ability to ask questions and get answers.  This is sometimes called “drill down”.  An analyst might want to know what sales were for a particular store for a given item.  The answer to that question might generate additional questions such as how that store sold a similar item, or how the item performed at a similar store.  The analyst postulates a theorem, and the tool enables the analyst to check its validity.  For instance, the analyst might think that a certain purse would appeal to high income shoppers and may ask questions of the data to verify that belief.  Query is usually done through a query tool, such as QMF, or for more analytically oriented analysts may be done through a spreadsheet. 
OLAP is a special form of query where multidimensional questions may be asked and multidimensional responses obtained.  It’s more complex, but it yields rich reports which may be broken out in a number of ways.  An analyst could get a report showing sales of all purse skus, across all stores, totaled by region, store type, market segment …  Again, however, we are in a question and answer mode with the analyst testing predispostions about the outcome.  The data is still just answering questions.

Mining is about using statistical algorithms on data to find trends and patterns that may not have been previously known.  The analyst asks very general questions without necessarily having an idea of the result.  Which of my stores behave similarly?  Which of my customers are similar in their buying behavior? Which of my products sell together, how strong is the relationship?

---

## Slide 33

**Title:** Partners Support Business Intelligence Solutions

```
[PlaceHolder 1 (0.17,0.6)]
  Partners Support Business Intelligence Solutions
[PlaceHolder 2 (0.67,1.59)]
  Mining invoked by end user tool
  Familiar, easy to use tool 
  DB2 mining is just a menu button!
  “Easy Data Mining” solutions
  Customer Segmentation
  Store Segmentation
  Promotion Targeting
  Market Basket Analysis
  
  Business analyst does the mining
  Expert data miner not required 
  
  Ease of use emphasis
[IMAGE pos=(7.36,4.54) size=(2.14x0.42) -> slide_33_pic_1034.png]
[IMAGE pos=(7.28,1.55) size=(2.28x0.59) -> slide_33_pic_1035.png]
[IMAGE pos=(7.36,2.5) size=(2.1x0.65) -> slide_33_pic_1036.png]
[shape (-0.73,7.1)]
  DTG
[IMAGE pos=(7.38,5.38) size=(1.86x0.43) -> slide_33_pic_1038.png]
[shape (7.03,3.5)]
  DB2 Alphablox
```

**Speaker notes:**

The PTM is an IBM patented methodology to enable DB2 to perform data mining without a data miner. We will go into some detail on the PTM.

---

## Slide 34

**Title:** Store Segmentation

```
[PlaceHolder 1 (0.17,0.52)]
  Store Segmentation
[PlaceHolder 2 (0.27,1.35)]
  Opportunities
  Markdowns are too high
  Stores have to put items on sale to move them
  We aren’t stocking what our customers want
  Which stores should run selected promotions?
  Which items should be promoted in which stores?
  What factors determine store profitability?
  
  Solution
  Store segmentation provided by partner reporting tool using DB2
  Reporting tool is for control and display
  DB2 does the mining in the background
[shape (5.0,1.73)]
  Transaction (TLOG POS) summaries by store
  Customer or postal code demographics (nice to have)
  Transaction log data summed by:
  SKU
  Category
  Department
  Day, week, month etc.
  Normalized data
  Eliminate size as a factor
  Isolate behavior
  Subset of products selected to address opportunity
  Experienced thought leaders
  Data
  Business
```

**Speaker notes:**

Data mining is the key to doing any kind of consumer segmentation.  Using actual data and purchase behaviors is infinitely preferable to extensive surveys and executive anecdotes about the types of consumers. Only by segmenting can an enterprise organize their spending priorities, their messages and offers, and in general all resources associated with the customer. 
Segmentation lets you identify both the high value spenders now and those that can easily become high spenders.  Keep in mind that not everyone who spends high amounts of money are profitable.  Some milkt the warranty, call centers, or promotions until they produce little or no profit.  So finding the right kinds of consumers is not simply looking at who spent the most money. 
Within each target segment, you can organize your messaging and offers.  That is, your brochures, your contract terms, your advertising, and the direct mail.   The brochures should have pictures that look similar to the audience –for example a hispanic family versus a retired couple illustration.  And the Ts & Cs of each offer must be built to match the financial position of the consumer.  Each major segment should be communicated throughout the company and be used to drive business process behaviors.  It must not be bottled up in the marketing department.  The shipping, order entry, call center, sales, and other departments need to know how to treat and manage each segment of client.
Ultimately, segmentation allows you to buy external data to locate new prospects.  By comparing their attributes to known profitable customer segments, you can determine the type of “treatment” most likely to attract that consumer to do business with you.  Whether its direct mail, sales leads, of SPAM, you can now prospect to clients in a more personalized way.  
Similarly, segmentation lets you identify consumer groups who are most likely to switch to competitors.  Therefore, you can prioritize some amount of funding to communicate with those customers to remind them of the value of your relationship.   Since you cannot spend money to “remind” all clients, segmentation lets you prioritize the ones you want to keep vis-à-vis the ones most likely to leave.

---

## Slide 35

**Title:** Requirements for Customer Segmentation

```
[PlaceHolder 1 (0.17,0.65)]
  Requirements for Customer Segmentation
[PlaceHolder 2 (0.3,1.53)]
  Summaries of transactions about selected opportunity for each potential target customer by:
  Day , Week, Month, Year, Life time
  Store
  Web
  Response to promotions
  Years as customer
  Life time spend
  …
  Demographics
  Append by postal code
  Derive from spending history
  Legal environment on purchased data changing
  Experienced thought leader
[GROUP: ]
  [IMAGE pos=(8.08,2.76) size=(1.2x2.25) -> slide_35_pic_1047.jpg]
  [IMAGE pos=(5.83,3.77) size=(0.78x1.22) -> slide_35_pic_1048.jpg]
  [IMAGE pos=(8.09,2.53) size=(1.2x0.98) -> slide_35_pic_1049.jpg]
  [IMAGE pos=(6.59,2.53) size=(1.5x1.24) -> slide_35_pic_1050.jpg]
  [IMAGE pos=(5.83,2.53) size=(0.76x1.45) -> slide_35_pic_1051.jpg]
  [IMAGE pos=(6.59,3.72) size=(1.49x1.27) -> slide_35_pic_1052.jpg]
```

---

## Slide 36

**Title:** Promotion Targeting

```
[PlaceHolder 1 (0.3,0.48)]
  Promotion Targeting
[PlaceHolder 2 (0.25,1.4)]
  Opportunities
  “Our response rate on customer promotions is too low.”
  “We don’t have data miners to target promotions, so we just do it using our experience.”
  
  Solution
  Promotion targeting provided by partner reporting tool using DB2.
  Reporting tool is for control and display
  DB2 does the mining in the background
  New statistical algorithm makes promotion targeting available to business analysts
[shape (5.79,1.86)]
  . “ Promotion targeting uses the most complex form of data mining and so only retailers with a skilled data mining staff or who are willing to outsource could use it.”
  
   IBM’s easy mining makes promotion targeting available as a function performed by a business analyst.
```

**Speaker notes:**

Promotion targeting:  Using past purchasing as a guide we can identify a group of customers who are good targets for a selected product.  The PTM will identify our other customers who are most similar to them.

Promotion targeting is based on predictive analysis.

---

## Slide 37

**Title:** Vendor Collaboration / Promotion Targeting Provides the ability to efficiently create, present and drive customized offers, across multiple channels, to individual shopper, based on purchase history

```
[PlaceHolder 1 (0.0,0.68)]
  Vendor Collaboration / Promotion Targeting Provides the ability to efficiently create, present and drive customized offers, across multiple channels, to individual shopper, based on purchase history
[PlaceHolder 2 (5.39,2.25)]
  Offer Promotions to customers most likely to respond
  Similar to those who already buy the product
  Total view of customer used to determine
  All good targets identified, even those not previously understood to be targets.
  Promotion not offered to those who purchase anyway
[PlaceHolder 3 (1.06,2.25)]
  Attract more promotions from all CPG suppliers.
  Offer better campaign feedback.
  Provide information about identified prospects beyond the targeting criteria.
  Provide feedback on success segmented by customer attributes.
  Enrich every promotion.
  Provide requested targets, but also offer other, similar groups with high probability of success.
[shape (0.97,1.7)]
  Vendor Collaboration
[shape (5.3,1.7)]
  Promotion Targeting
```

**Speaker notes:**

Vendor collaboration is about maximizing vendor dollars and promoting all potential customers.  Promotion targeting entails only promoting those customers not currently heavily buying the promoted product.  So with promotion targeting we don’t send the promotion to the extracted good customers, but only to the similar ones.

---

## Slide 38

**Title:** Sample Customer BST’s and Reports

```
[PlaceHolder 1 (0.51,0.29)]
  Sample Customer BST’s and Reports
[PlaceHolder 2 (0.38,1.39)]
  Purchase Profiles BST 	
  	Category Sales Report by Demographics	
  	Loyalty Points Issued by Store	
  	Sales Value / Quantity by Products vs Customers
  	Product Group Average Sales Quantity per 			Transaction	
  	Product Group Average Sales Value per 			Transaction	
  	Product Penetration (to Geography, geo-			demographic mix)	
  Customer Profiles BST	
  	Customers Attribute report	
  	Customers Status by Attribute report	
  	Cumulative Percentage Sales by Decile (10% 		segment) report	
  	Sum of Purchase Made by Decile report	
  	Customer Base Dynamics report	
  	Loyal Purchasers Subsequent Behavior report
  	Customer Details report 	
  Product Purchasing  Recency, Frequency & Quantity  BST	6 Month Customer Age Group Segment RFQ 		report	
  	Repurchase Interval	
  	Repurchase Propensity	
  	Distribution of Customers by Number of Units
  	Distribution of Transactions by Number of Units
[shape (5.16,1.39)]
  Campaign & Promotion Analysis BST	
  	Sales Performance by Campaign Response	
  	Sales Performance by Campaign Cell	
  	Target Period Sales Proportion Index Sub-Class
  	Target Period Sales Value Index by Age Range
  	Target Period Sales Value Index by Product	
  Cross Purchase Behavior Analysis BST	
  	Count of Cross Purchasers	
  	Cross Purchasers Subsequent Behavior	
  Target Product Analysis BST 	
  	Sales Quantity Proportion	
  	Average Transaction Quantity	
  	Average Transaction Value	
  	Sales Value Proportion	
  Customer  Movement  Dynamic
  	Customer Acquisition & Defection report	
  	Segment Migration Comparison report	
  Market Basket Analysis (Clienteling)	
  	Cross Merchandising (what’s in a basket)	
  	Demographic profile to  market basket	
  	Statistical reports	
  	Association report – product
```

---

## Slide 39

**Title:** Sample Product and Services BST’s and Reports

```
[PlaceHolder 1 (0.51,0.29)]
  Sample Product and Services BST’s and Reports
[PlaceHolder 2 (0.38,1.39)]
  Business  Performance Analysis BST	
  	New Item Introduction	
  	Vendor Performance – sales reports by vendor
  	Discontinue analysis 	
  	Sales Quantity by Products	
  	Vendor Compliance  - billing, delivery, 	
  	Vendor Fulfillment 	
  	Vendor Rebate	
  	Cannibalization impact  	
  	New Item Launch coverage	
  	Sales Quantity Proportion by Products	
  	Sales Value by Products	
  	Sales Value Proportion by Products	
  	Sales Value Proportion by Sub-Department	
  	Target Product Transactions: Average 			Transaction Quantity
  	Target Product Transactions: Average 			Transaction Value
  	Target Product Transactions: Sales Quantity 		Proportion
  	Target Product Transactions: Sales Value 			Proportion	
  	Vendor In Stock Position
[shape (5.16,1.39)]
  Product Analysis BST	
  	Product Performance by Store, Geography report
  	Product Category Performance report	
  	Detail Product Category Breakdown report	
  	Target Product to Customer report	
  	Product Category Breakdown report	
  	Product Equalization report
```

---

## Slide 40

**Title:** Sample Merchandising BST’s and Reports

```
[PlaceHolder 1 (0.51,0.29)]
  Sample Merchandising BST’s and Reports
[PlaceHolder 2 (0.38,1.39)]
  Inventory Analysis BST	
  	On  Order  V On Hand 	
  	Days of supply 	
  	Lag Time Report 	
  	Out of Stock .. by Product 	
  	Total cost of goods on hand by location	
  	Damages / Stressed (garments) / Aged  Products
  	Safety Stock Report	
  	Slow moving inventory report 	
  	Transfer Report and Management	
  Assortment / Allocation Analysis  BST 	
  	Traited  v Value 	
  	Base Profit Contribution	
  	Product Sales by  Store Format	
  	Category Performance by Store 	
  	Product Affinity	
  	Product to Customer Profiles	
  Promotion Analysis BST	
  	Promotion Sales Performance report	
  	Overall  Profit Contribution report	
  	Promotion Effect by Media report	
  	Promotion Effect by Media2 report	
  	Promotional Response by Customer Segments
  	Promotional Response by Market Basket report
  	Promotional Impact on Store Traffic report	
  	Promotional Category Impact report	
  	Promotion Fade report
[shape (5.08,1.36)]
  Physical Merchandising/Space Management  Analysis  BST
  	Same Layout Comparisons 
  	Demographic Response to different Layouts 
  	Revenue per sq Ft.  	
  	Category Profitability to Physical Presence	
  	Days off of Supply of Product to Category 	
  	Optimization of Linear Footage to total store
  	Section elasticity / adjacency 	
  Pricing  Analysis BST	
  	Set vs Actual Price Sold report	
  	Price Competitive Exception report	
  	Family Pricing (related products) report	
  	Competitive Marketbasket report	
  	Multi-Channel Price report	
  	Markdown Trend report	
  	Price Elasticity report
```

---

## Slide 41

**Title:** Sample Store Operations BST’s and Reports

```
[PlaceHolder 1 (0.51,0.29)]
  Sample Store Operations BST’s and Reports
[PlaceHolder 2 (0.38,1.39)]
  Loss Prevention BST	
  	Baseline exception reports 	
  	Cashier exceptions report -  over and under, 		Voids	
  	Inventory discrepancy 
  	Employee Schedule compliance associated 		with loss	
  	Receiver exception report 	
  Staffing BST	
  	Employee Schedule compliance	
  	Cashier  performance metrics	
  	Cross training reports 	
  	Sales Person Productivity	
  	Skills v Employees	
  	Years of services  report	
  	Employee Details report
[shape (5.16,1.39)]
  Store Location Analysis BST	
  	Performance by Store Format report	
  	Age of Stores report	
  	Store Geo-Demographic Profiles  report
  	Location Segmentation report	
  	Performance by Store Type  report	
  	Store Detail report	
  Store Optimization
  	Projected Inventory V  Sales Projections
  	Actual Inventory V Projected Inventory 
  	On Order- Relationships V  On –Hand 		Inventory
```

---

## Slide 42

**Title:** Sample Multi-Channel BST’s and Reports

```
[PlaceHolder 1 (0.51,0.29)]
  Sample Multi-Channel BST’s and Reports
[PlaceHolder 2 (0.37,1.39)]
  eCommerce Analysis BST	
  	Session cycle count analysis by period report	
  	Session cycle comparison analysis by period report	
  	Identified Shopper Segmentation analysis by segment by period 
  	Identified Shopper Segmentation analysis by segment by period 
  	Product Category analysis by period by trait report	
  	Product Category Breakdown by time period report	
  	Product Category Customer Segmentation by time period report
  	Clickstream patterns with sales results	
  	Method used for payment to actual sales	
  Catalog Analysis BST	
  	Cross catalog purchase profiles	
  	Catalog mix to demographic response	
  	Product placement to purchase propensity	
  Call Center Analysis BST	
  	Operator closure rates	
  	Script success rate to demographic	
  	Cold call conversions to qualified	
  	Failure causes and statistics
```

---

## Slide 43

```
[shape (0.34,0.54)]
  The M1 Tool provides a graphical interface to the RDW environment
[shape (2.01,0.06)]
  The RDW  Environment
[shape (0.43,0.96)]
  The M1 gives a common place for the retailer user to see the environment in terms that are easily understood and defined the business user.  It is the prime way of quickly customizing the RDW to your specific reporting and analytical needs.
[IMAGE pos=(1.51,2.29) size=(6.41x4.4) -> slide_43_pic_1078.png]
```

---

## Slide 44

**Title:** Customer Management

```
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a36f0>)]
[PlaceHolder 1 (0.37,0.49)]
  Customer Management
[IMAGE pos=(0.98,1.47) size=(7.87x5.63) -> slide_44_pic_1082.png]
```

---

## Slide 45

**Title:** Customer Management

```
[IMAGE (failed to extract: cannot identify image file <_io.BytesIO object at 0x10c3a39c0>)]
[PlaceHolder 1 (0.37,0.49)]
  Customer Management
[shape (0.51,1.15)]
  Marketbasket Analysis Measures and Dimensions
[IMAGE pos=(0.98,1.48) size=(7.8x5.58) -> slide_45_pic_1087.png]
```

---

