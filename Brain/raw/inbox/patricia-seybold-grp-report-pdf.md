---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Reading/Patricia Seybold Grp Report.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Patricia Seybold Grp Report.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Reading/Patricia Seybold Grp Report.pdf.md`
Size: 42,169 bytes

## Raw content
E-Business Strategies & Solutions / Product Review
One-To-One Commerce 4.1
BroadVision's Contribution to the Marketplace for Electronic Commerce Servers.
By Mitchell I. Kramer August 11, 1999
SELECTING ELECTRONIC COMMERCE
NETTING IT OUT
SERVERS
Electronic commerce servers are application
packages for transacting business on the Inter-
Mission-Critical Software
net. These packages are the “buy” alternative to
the “build” option of developing, integrating, and
With the huge anticipated growth in e-commerce
implementing the e-commerce business proc-
on the Web, the timely selection or development and
ess with programming tools.
the successful implementation of e-commerce serv-
ers are critical to the competitiveness of companies
One-To-One Commerce is BroadVision’s
of all sizes across all industries. This really is mis-
e-commerce server offering. One-To-One Retail
sion-critical software. It is the way that you deliver
Commerce product supports business-to-
marketing, sales, and service on the Web channel.
consumer applications, and the One-To-One
Business Commerce product supports sell-side
An Evaluation Framework
business-to-business applications. Both prod-
ucts provide a comprehensive implementation Almost two years ago, Patricia Seybold Group
of marketing, shopping, buying, and fulfillment began research on electronic commerce servers. Its
processes. purpose was to help your selection decision for
e-commerce servers. We’ve designed and validated
One-To-One Retail Commerce and One-To- a framework for evaluating and comparing these
One Business Commerce are best suited to products, and we’ve published two versions of an in-
large-scale, high-end e-commerce sites. The depth report that details our research and analysis.
key strengths of the product are its marketing This research and analysis, including product instal-
capabilities, including market analysis, mer- lation and review, interviews with e-commerce
chandising, and personalization; its CORBA server users and vendors, and tapping the PSG
implementation; and its rich shopping function- e-commerce knowledgebase, has led us to identify
ality. Limitations are heterogeneous administra- four sets of requirements for selecting e-commerce
tive tools that, as a toolset, are hard to learn servers. Analysis of the requirements in the context
and hard to use; reporting and analysis capa- of your organization can identify the key factors in
bilities that prevent sharing and in-depth analy- making your selection decision. The four sets of re-
sis; and limited support for market segments. quirements are:
FUNCTIONALITY. Functional requirements address
the capabilities that implement the commerce busi-
This article is an excerpt of an in-depth technical
ness processes for business-to-business (B2B) and
review about BroadVision, which we will be pub-
business-to-consumer (B2C) applications.
lishing in September as part of our forthcoming
special report “Comparative Evaluation of Leading ADMINISTRATION. Administrative requirements
Electronic Commerce Servers, 2nd Edition.” analyze the tools for managing e-commerce re-
E-Business Strategies & Solutions © 1999 Patricia Seybold Group (cid:127) 85 Devonshire St., 5th Fl., Boston, MA 02109 USA (cid:127) www.psgroup.com

2 (cid:127) One-To-One Commerce 4.1
sources, the facilities for security, and the tools for able marketers to create a wide range of incentives
reporting. and  promotions  and  to  apply  them  to  individual
products, orders, or information in orders. Cross-
| ARCHITECTURE.  |           | Architecture  |       | requirements  |     | ex-  |          |                  |     |      |             |     |              |
| -------------- | --------- | ------------- | ----- | ------------- | --- | ---- | -------- | ---------------- | --- | ---- | ----------- | --- | ------------ |
|                |           |               |       |               |     |      | selling  | and  up-selling  |     | are  | supported,  |     | but  through |
| amine          | how  the  | product       | does  | e-commerce.   |     | They |          |                  |     |      |             |     |              |
low-level facilities.
analyze how the product is organized, how its con-
Personalization has always been a hallmark and a
stituent parts communicate and how they are struc-
strength of the product. One-To-One Commerce’s
tured, and how the product may be modified and
personalization is dynamic and is based on sets of
extended.
declarative rules evaluated in response to the activi-
PRODUCT  MARKETING.  Product  marketing  re- ties of individual shoppers and customers. Illustra-
quirements  examine  the  business  aspects  of tion  1  shows  the  workspace  wherein  marketers
e-commerce servers and the companies that offer specify sets of personalization rules.
| them. |     |     |     |     |     |     | BroadVision was among the first to offer person- |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- |
alization and was alone in supporting such capabili-
| INTRODUCING  |               | ONE-TO-ONE  |             |     | COMMERCE |     |            |        |       |        |         |      |            |
| ------------ | ------------- | ----------- | ----------- | --- | -------- | --- | ---------- | ------ | ----- | ------ | ------- | ---- | ---------- |
|              |               |             |             |     |          |     | ties  for  | quite  | some  | time.  | Today,  | all  | e-commerce |
| FROM         | BROADVISION.  |             | One-To-One  |     | Commerce |     |            |        |       |        |         |      |            |
servers provide some level of personalization either
was one of the first e-commerce server products on
through built-in functionality or through the integra-
the market. First introduced in December 1995, it
tion of external products. BroadVision is no longer
has stood the test of time and continues to gather
alone. And, in fact, we believe that the company has
| market  | momentum.  | BroadVision's  |     | latest  |     | series  of |     |     |     |     |     |     |     |
| ------- | ---------- | -------------- | --- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
products—One-To-One  Retail  Commerce  4.1  and fallen behind in its rules-based approach to person-
alization.
| One-To-One  | Business  |     | Commerce—became  |     |     | gener- |     |     |     |     |     |     |     |
| ----------- | --------- | --- | ---------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
Although rules are easy to understand and easy to
ally available on June 30, 1999. To date, BroadVi-
specify and implement, there are issues with rules.
sion claims that it has 150 One-To-One Commerce
Specifying them is quite an effort. Their design, im-
customers. Most are large corporations.
plementation, and maintenance can be formidable
tasks for marketers and administrators. In addition,
FUNCTIONAL REQUIREMENTS
their power is limited. Other analytical techniques,
such as collaborative filtering, neural networks, dy-
Let's take a look at how BroadVision One-to-One
namic modeling, and pattern matching, offer richer
Commerce stacks up against our evaluation frame-
matching functionality. More traditional marketing
work.
techniques, such as (offline) modeling, scoring, and
segmentation, offer more power and have no impact
Marketing
on online resources and performance. Also, as rule
One-To-One  Commerce  has  strong  marketing, sets become large and as their evaluation is required
merchandising, and personalization capabilities. In
for every user request, they can slow the system
| marketing, information critical to marketing analysis |     |     |     |     |     |     | down. |     |     |     |     |     |     |
| ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
is collected, logged, and written to database tables in
| raw or aggregated formats. This information can be |     |     |     |     |     |     | Shopping |     |     |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
analyzed through packaged reports or further ana-
|     |     |     |     |     |     |     | One-To-One  |     | Retail  | Commerce  |     | offers  | strong |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | --------- | --- | ------- | ------ |
lyzed with external tools. Collection and organiza-
shopping capabilities. Browsing, product search, and
| tion  of  | marketing  | information  |     | is  a  | key  | product |     |     |     |     |     |     |     |
| --------- | ---------- | ------------ | --- | ------ | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
product comparison capabilities are built in. A rich,
strength.
|                |     |               |     |      |             |     | predefined  | product  |     | structure  | can  | support  | custom- |
| -------------- | --- | ------------- | --- | ---- | ----------- | --- | ----------- | -------- | --- | ---------- | ---- | -------- | ------- |
| Merchandising  |     | capabilities  |     | are  | implemented |     |             |          |     |            |      |          |         |
built shopping approaches. Illustration 2 shows the
| through  | a  flexible  | approach  |     | to  coupons  |     | and  dis- |     |     |     |     |     |     |     |
| -------- | ------------ | --------- | --- | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
advanced search capabilities.
counts. They may be applied by single session or
time period and combined with pricing rules to en-
© 1999 Patricia Seybold Group’s E-Business Strategies & Solutions

Product Review (cid:127) 3
Specifying Rule Sets
Illustration 1. One-To-One provides personalization through the evaluation of rule sets. They’re specified with the Rules wiz-
ard of the product’s Dynamic Command Center toolset. This illustration shows the workspace for the Rules wizard.
An attractive new shopping feature is shopping Buying
lists, which are collections of products from a store.
Retail Commerce buying functionality includes
Shoppers may use them to track products that
the creation and maintenance of a shopping cart, the
they’re interested in but are not ready to buy or to
generation of orders from a shopping cart’s contents,
remind themselves of products that they buy regu-
and the calculation of prices, taxes, shipping
larly. Sellers may use them to help inexperienced
charges, and order totals. Multiple ship-to addresses
shoppers get started in their stores or as a merchan-
are supported for orders. Business Commerce buy-
dising approach to encourage shoppers to buy re-
ing functionality includes the creation of purchase
lated products or on-sale products.
requisitions, the generation of invoices from the
One-To-One Business Commerce capabilities,
contents of the purchase requisitions, and the calcu-
new in the product’s current version, offer a B2B
lation of taxes, shipping charges, and invoice totals.
shopping process built on the B2C shopping foun-
Note that, for Business Commerce, product prices,
dation. Corporate buyers belonging to accounts se-
payment methods, ship-to addresses, and bill-to ad-
lect products from a catalog. The products are a sub-
dresses are defined and stored within buyers’ pro-
set of all the products offered by the site. Sales
files.
prices and discounts may be offered on an account
basis. A contract ties together the account, the prod-
ucts, and the prices.
© 1999 Patricia Seybold Group’s E-Business Strategies & Solutions

4 (cid:127) One-To-One Commerce 4.1
Advanced Search
Illustration 2. Advanced search allows shoppers to search on product categories and category attributes. The approach is a
two step process that lets them first select a category and then select category attributes. This illustration shows the first step.
Quotes are an attractive new feature of the buy- Fulfillment
ing process. They’re used when a shopper is not
One-To-One Retail Commerce and One-To-One
ready to buy the contents of a shopping cart. Rather
Business Commerce share fulfillment functionality.
than discarding the shopping cart or saving just its
Business Commerce supports purchase order pay-
contents (persistent shopping carts), the shopper can
ment as well as the credit/debit card payment sup-
request a quote for those contents in order to buy
ported by Retail Commerce. Credit/debit card pay-
them at later time at the current prices. (We’ve all
ment handling is implemented by an external appli-
dealt with quotes when we buy high-priced items,
cation. Order management for both B2B and B2C
such as automobiles.) Quotes are useful for expen-
also relies on the integration of external systems.
sive items. They’re also useful for comparison shop-
The system supports back orders, partial shipments,
ping between sites offering similar products. In ad-
and returns. It provides automatic order acknow-
dition, quotes are a natural in B2B applications,
ledgement and allows customers to check on order
where pricing can be quite dynamic.
and invoice status and on order and invoice history.
New in 4.1, a feature called Order Flows allows
the business process flow of order management to be
© 1999 Patricia Seybold Group’s E-Business Strategies & Solutions

Product Review (cid:127) 5
customized for B2B accounts or for individual B2C pers and customers to access e-commerce resources.
customers. The feature offers good flexibility and The secured resources protected are executables,
recognizes that the fulfillment process differs be- typically scripts or components. The approach to
tween B2B and B2C applications and between cus- access control is straightforward and effective as
tomers within those applications. well as easy to understand and easy to implement.
Reporting
ADMINISTRATION
One-To-One Commerce provides event-driven
mechanisms to collect, log, organize, and aggregate
Managing Electronic Commerce Resources
data about the behavior of individual shoppers and
A rather large set of tools is needed to manage customers during the shopping, buying, and
the resources of One-To-One Commerce systems. fulfillment processes. The product also collects and
The product packages two visual toolsets. organizes transaction data. And it packages a large
set of reports to help administrators and marketers
(cid:127) DYNAMIC COMMAND CENTER. The analyze the information in the aggregated tables of
Dynamic Command Center is a Windows-based the Observations system. The reports are written in
toolset used for managing content and person- Microsoft Access and run on Windows 98 and NT.
alization as well as for creating and managing Great data! Great reports! Not so great data stor-
the Business Commerce resources: accounts, age and reporting tools. The use of Access prevents
prices, products, and contracts. sharing and reuse of these reports. Access is not the
most sophisticated reporting tool, and this informa-
(cid:127) DESIGN CENTER. The Design Center is a tool- tion is quite sophisticated. Recognizing this limita-
set new in One-To-One Commerce 4.1. Devel- tion, BroadVision has been working with Androme-
opers use it to create and manage the scripts that dia to improve real-time reporting and with Broad-
generate Web pages. Design Center is a visual, Base to improve offline reporting.
Web-based toolset that is based on Dream-
weaver 2 from Macromedia.
ARCHITECTURE
A third toolset, called the Visual Design Center,
is packaged for compatibility with previous product Organization and Architecture
versions. One-To-One Commerce also packages an
One-To-One is implemented as a distributed ob-
assortment of utilities, some textual, some visual and
ject application that is accessed from Web browsers
Web based, to help administrators, marketers, and
through any of the standard Web servers. The prod-
developers perform various installation and mainte-
uct has five major components. They’re listed and
nance tasks. We believe that there are too many tool-
described below. Illustration 3 shows their architec-
sets within One-To-One and that the toolsets are
ture and organization.
poorly organized. We prefer a centralized approach,
where all the toolsets are Web based and accessible Interaction Manager. The Interaction Manager is
through a consolidated workspace. This approach the front end of the One-To-One system. It receives
makes it easier to learn and easier to use the tools requests in the form of URLs from shoppers, cus-
required to manage electronic commerce resources. tomers, developers, and administrators, and it returns
the system’s responses in the form of Web pages to
Security each of those user types. The ability to configure
multiple instances of the Interaction Manager, to
One-To-One Commerce itself can authenticate all
distribute those instances across multiple platforms,
users by username and password. Alternatively, the
to implement multiple Engines within each instance,
product may be configured to use external authenti-
and to access each instance from multiple Web serv-
cation facilities, such as LDAP or NT domains. One-
To-One Commerce provides authorization for shop-
© 1999 Patricia Seybold Group’s E-Business Strategies & Solutions

6 (cid:127) One-To-One Commerce 4.1
ers offers a very high level of configurable parallel popular RDBMSs: Informix Online Server, Micro-
processing. soft SQL Server, Oracle, or Sybase Adaptive Server.
IBM DB2 is a notable exception. The database is
Scripts and JavaScript-Visible Components. The
built on a predefined schema, although tables for
structure and processing flow of One-To-One Com-
content types, content, attributes, and related infor-
merce applications is controlled by JavaScript scripts
mation may be added, and some of the predefined
that contain, in addition to HTML tags, references to
tables contain “extra” columns to accommodate site-
| (JavaScript-visible)  |     |     | components  |     | to  | perform |           |                 |     |      |             |     |          |     |
| --------------------- | --- | --- | ----------- | --- | --- | ------- | --------- | --------------- | --- | ---- | ----------- | --- | -------- | --- |
|                       |     |     |             |     |     |         | specific  | customization.  |     | The  | One-To-One  |     | database |     |
e-commerce processing and to retrieve database in-
provides persistence for One-To-One Server objects
formation. The JavaScript-visible components per-
|     |     |     |     |     |     |     | and  transaction  |     | support  | for  | their  | processing.  |     | The |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------- | ---- | ------ | ------------ | --- | --- |
form infrastructure and electronic commerce proc-
information used by One-To-One is organized into
| essing.  | They’re  | called  | by  | the |     |     |     |     |     |     |     |     |     |     |
| -------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
nine groups of database tables.
scripts to begin application proc-
essing, and they, in turn, call One-
Infrastructure
| To-One servers for the processing |     |     |     |     | CORBA is a One-To-One |     |     |     |     |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
that they don’t perform as well as advantage and a smart The  Interaction  Manager  and
for database access. Both scripts
|     |     |     |     |     | infrastructure approach by |     |     |     | Web  | Gateway  |     | Module  | are  | the |
| --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | ---- | -------- | --- | ------- | ---- | --- |
and  components  execute  under front  end  of  the  One-To-One
BroadVision.
| control  | of  Interaction  |     | Manager |     |     |     |     |     |           |     |               |              |         |        |
| -------- | ---------------- | --- | ------- | --- | --- | --- | --- | --- | --------- | --- | ------------- | ------------ | ------- | ------ |
|          |                  |     |         |     |     |     |     |     | Commerce  |     | environment.  |              | They’re |        |
| Engines. |                  |     |         |     |     |     |     |     | deployed  |     | on  a         | proprietary  |         | infra- |
structure that uses standard Web
Web Gateway Module. Multiple
|            |          |              |     |          |      |         | server  | interfaces,  | TCP/IP  |     | for  communication  |     |     | and |
| ---------- | -------- | ------------ | --- | -------- | ---- | ------- | ------- | ------------ | ------- | --- | ------------------- | --- | --- | --- |
| instances  | of  the  | Interaction  |     | Manager  | may  | be  de- |         |              |         |     |                     |     |     |     |
operating system processes, and threads to control
ployed on a single server platform or across multiple
|     |     |     |     |     |     |     | their  execution.  |     | The  | approach  |     | is  quite  | typical. |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ---- | --------- | --- | ---------- | -------- | --- |
server platforms through the use of the (optional)
|     |     |     |     |     |     |     | E-commerce  |     | server  | vendors  | must  | use  | these  | low- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | -------- | ----- | ---- | ------ | ---- |
Web Gateway Module. The Web Gateway Module
level facilities for front-end infrastructure. Commer-
is deployed between the Web server and Engines of
|     |     |     |     |     |     |     | cially  available  |     | infrastructures  |     |     | do  not  | encompass |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ---------------- | --- | --- | -------- | --------- | --- |
the Interaction Manager(s). It allows the components
Web server processing.
of One-To-One Commerce to run a platform other
One-To-One Commerce Servers and the One-To-
than the platform hosting the Web server. The Web
One Commerce database are the back end of the en-
Gateway offers a scalability approach to the front
vironment. The servers are deployed on a CORBA
end on One-To-One Commerce. The product’s back
end, its servers, runs within a CORBA infrastruc- infrastructure. The use of CORBA can address re-
quirements for performance, scalability, and avail-
ture, which offers a range of scalability options.
ability. Components can be distributed across multi-
One-To-One  Servers.  One-To-One  Commerce ple platforms. Distribution can improve availability
| servers  implement  |     | the  | programming  |     | logic  | for  its |               |     |         |         |               |     |               |     |
| ------------------- | --- | ---- | ------------ | --- | ------ | -------- | ------------- | --- | ------- | ------- | ------------- | --- | ------------- | --- |
|                     |     |      |              |     |        |          | by  reducing  |     | single  | points  | of  failure.  |     | In  addition, |     |
e-commerce functionality, for services that support multiple instances of components can be started to
e-commerce, and for its supporting infrastructure. increase  execution  parallelism  and  improve  per-
Each of the servers comprises several objects, and
formance. Most significantly, both distribution and
each object encapsulates a number of methods and parallelism are transparent to application functional-
attributes. The objects are coarsely grained, mini-
ity.
mizing  object-to-object  communication  overhead. CORBA is a One-To-One advantage and a smart
Yet their granularity is fine enough to facilitate easy infrastructure approach by BroadVision. Transparent
| customization and integration of external  |     |     |     |     |     | applica- |     |     |     |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
distribution and parallelism can yield significant per-
| tions.      |     |            |             |     |          |     | formance and scalability benefits. In addition, the |          |     |              |     |     |        |     |
| ----------- | --- | ---------- | ----------- | --- | -------- | --- | --------------------------------------------------- | -------- | --- | ------------ | --- | --- | ------ | --- |
|             |     |            |             |     |          |     | approach                                            | enables  |     | BroadVision  |     | to  | focus  | on  |
| One-To-One  |     | Database.  | One-To-One  |     | manages  | a   |                                                     |          |     |              |     |     |        |     |
single  database  implemented  within  any  of  four e-commerce functionality and not become entangled
in the distributed computing infrastructure.
© 1999 Patricia Seybold Group’s E-Business Strategies & Solutions

Product Review (cid:127) 7
One-To-One Commerce Architecture and Organization
Web Server
CGI / CAPI, GW API / NSAPI
Interaction
Manager
Web Gateway
TCP / IP
Interaction
Manager
TCP / IP
One-to-One Commerce Servers
Pricing System
Observation System
Profile System Taxing System
Visitor System Payment Handling System
Content Management System Order Fulfillment System
Matching System
Shipping System
Sales Rep.
One-To-One
Commerce
Database
Illustration 3. One-To-One is a distributed object system that is accessed by shoppers through Web browsers connecting to a
Web server. This illustration shows the components and structure of One-To-One. The Interaction Manager runs as a CGI,
ISAPI, or NSAPI Web server application. Other components are accessed as distributed objects from the Interaction Man-
ager.
The Interaction Manager, JavaScript-visible lithic and difficult to understand. This object struc-
components, and all One-To-One servers are written ture is the ideal in object-oriented design.
in C++, and BroadVision’s developers used object-
oriented techniques to design and build them. We Customizing One-To-One Commerce
found their object structure to be coarsely grained.
BroadVision publishes the interfaces of all its
There are about 90 JavaScript-visible components
objects and its JavaScript-visible components, fa-
and about 90 components in the One-To-One serv-
cilitating their customization. Server customization
ers; they implement e-commerce, system manage-
can be accomplished in any programming language
ment and control, or database access functionality.
that supports CORBA IDL: C, C++, and Java. Note
There are not so many objects as to be unmanage-
that customized server objects and JavaScript-visible
able and not so few as to make the system mono-
© 1999 Patricia Seybold Group’s E-Business Strategies & Solutions

8 (cid:127) One-To-One Commerce 4.1
components must be written in C++. The objects PRODUCT MARKETING
within a server communicate through native C++
interfaces. And, JavaScript-visible components are
Product Positioning
accessed by JavaScript.
|     |     |     |     | BroadVision  | positions  |     | One-To-One  | Commerce |     |
| --- | --- | --- | --- | ------------ | ---------- | --- | ----------- | -------- | --- |
Integration with External Applications as an enterprise-class, scalable solution for business-
|     |     |     |     | to-consumer  | and  | business-to-business  |     | electronic |     |
| --- | --- | --- | --- | ------------ | ---- | --------------------- | --- | ---------- | --- |
One-To-One allows developers to integrate ex-
commerce. There are three elements to this posi-
ternal applications through CORBA. For integrating
tioning:
| non-CORBA  | applications,  | developers  | must  create |     |     |     |     |     |     |
| ---------- | -------------- | ----------- | ------------ | --- | --- | --- | --- | --- | --- |
(cid:127)  Relationship Marketing
CORBA wrappers that implement those interfaces
| for the external applications.  |     | Because intra-server |     | (cid:127)  Scalability |     |     |     |     |     |
| ------------------------------- | --- | -------------------- | --- | ---------------------- | --- | --- | --- | --- | --- |
communication  uses  C++  inter- (cid:127)  Electronic  Commerce  Solu-
| faces,  only  | certain  One-To-One |          |     |     |     | tion |     |     |     |
| ------------- | ------------------- | -------- | --- | --- | --- | ---- | --- | --- | --- |
| objects       | can  integrate      | external |     |     |     |      |     |     |     |
BroadVision positions
|     |     |     |     |     |     | The  | first  two  | elements  | play |
| --- | --- | --- | --- | --- | --- | ---- | ----------- | --------- | ---- |
applications. Five “adapter” ob-
One-To-One Commerce as
on the strengths of One-To-One
jects support integration of exter-
nal  applications for the follow- an enterprise-class, Commerce.  The  third  element
|                             |     |     |                       |     |     | plays  on                | one  of  | its  perceived |      |
| --------------------------- | --- | --- | --------------------- | --- | --- | ------------------------ | -------- | -------------- | ---- |
| ing:                        |     |     | scalable solution for |     |     |                          |          |                |      |
| (cid:127)  Payment Handling |     |     |                       |     |     | limitations—complexity.  |          |                | With |
business-to-consumer and
|     |     |     |     |     |     | services  | (that  is,  | programming |     |
| --- | --- | --- | --- | --- | --- | --------- | ----------- | ----------- | --- |
(cid:127)  Taxation
business-to-business
|     |     |     |     |     |     | services),  | any  technology  |     | can |
| --- | --- | --- | --- | --- | --- | ----------- | ---------------- | --- | --- |
(cid:127)  Shipping
|     |     |     | electronic commerce. |     |     | become a solution. One-To-One |     |     |     |
| --- | --- | --- | -------------------- | --- | --- | ----------------------------- | --- | --- | --- |
(cid:127)  Order Fulfillment
|     |     |     |     |     |     | Commerce  | can  require  |     | lots  of |
| --- | --- | --- | --- | --- | --- | --------- | ------------- | --- | -------- |
(cid:127)  Content Management
programming to become a solu-
tion in many situations.
| We  | like  BroadVision’s  | integration  | approach. |     |     |     |     |     |     |
| --- | -------------------- | ------------ | --------- | --- | --- | --- | --- | --- | --- |
CORBA wrappers can provide language neutrality
Market and Sales
and a good deal of platform independence for exter-
nal applications. However, integrating external ap- BroadVision targets One-To-One Commerce at
three market segments within Global 1000 corpora-
plications is never an easy task. This is a general
| issue, not a BroadVision issue. One-To-One’s ap- |                           |          |             | tions:            |     |     |     |     |     |
| ------------------------------------------------ | ------------------------- | -------- | ----------- | ----------------- | --- | --- | --- | --- | --- |
| proach                                           | requires  that  external  | systems  | be  object- | (cid:127)  Retail |     |     |     |     |     |
oriented and implementable in CORBA. That could
(cid:127)  Distribution
be a very difficult requirement, especially for cus-
(cid:127)  High technology
tom-built applications and packaged software.
BroadVision addresses this complexity and diffi- The company approaches these markets with the
culty through alliances with ISVs that specialize in One-To-One Commerce product backed by a com-
application integration, including Active Software,
prehensive array of consulting services designed to
TIBCO, and Vitria Technologies. All have products help  customers  develop,  implement,  and  support
that can be useful in the One-To-One environment. electronic commerce applications.
The use of these products increases the cost and the BroadVision sells One-To-One. It does not mar-
administration of the One-To-One Commerce envi- ket the product. Prospects are pinpointed, and the
ronment. However, the benefits of faster implemen- sales force is assigned territories of named accounts.
tation and the elimination of custom integration code This approach is classic for new companies offering
can outweigh the costs. new and innovative technologies. In time, BroadVi-
sion will be able to leverage its success in sales with
broader-based marketing programs.
© 1999 Patricia Seybold Group’s E-Business Strategies & Solutions


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
