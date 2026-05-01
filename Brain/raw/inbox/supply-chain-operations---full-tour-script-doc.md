---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Supply chain operations - full tour script.doc.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Supply chain operations - full tour script.doc

## Source
File: `Brain/raw/.extract/SWINDON/Supply chain operations - full tour script.doc.md`
Size: 38,673 bytes

## Raw content
Supply Chain Operations


THIS PAGE FOR INFORMATION ONLY: TOUR OVERVIEW

Supply Chain Operations is Tour #5 and sits within the overall tour framework as follows:

Tour #4: Category Management and Planning (Head Office)
T&K’s category management approach
Planning business performance
Range development
Assortment planning
Managing Range Implementation to Stores
Sourcing and Procurement Policy

Tour #5: Supply Chain Operation (Supply Chain, Part I)
Replenishment
Allocations
Forecasting
Supplier Order Management
Distribution (Inbound Scheduling, Warehouse Management, Transport Management (not included))
Inventory Management

Tour #6: Day in Life of a T&K Store Manager, 6:30AM - 1:00PM (Store)
Goods receiving and processing
Inventory management
Store ordering

The Supply Chain Operations Tour will deal with the following areas:

Key messages
Most retail businesses operate multiple supply chains and therefore have an inherently complex supply chain operation. An ERP system such as SAP helps drive out clarity from complex supply chain processes by getting you to think about your business processes and configuring the system to support these processes.
There is a range of supply chain business transactions which have historically been done on separate systems interfaced to each other. This has presented problems in the maintenance of interfaces, having a single correct version of the data and having the capability to reduce lead times in business processes such as replenishment. An integrated system, such as SAP supports all of these business transactions, avoids the interface problems, provides a single accurate version of the data and removes constraints that prevent improvement in processes.
SAP is not necessarily the answer to all system requirements. Specialist systems may still be required in areas such as transport planning and warehouse automation, as well as replacing parts of SAP where the functionality may not match the business need.



THIS PAGE FOR INFORMATION ONLY: TOUR CONTENTS


Introduction

Our current distribution network and configuration.

Story

How orders are generated (both for the store and the DC),
Allocations
Replenishment
Forecasting
Supplier ordering
Quota arrangements
Loadbuilding
EDI to/from suppliers

How we receive and manage stock through the supply chain
Distribution
Inbound flow scheduling
Integration
Warehouse management
Cross docking
Inventory management

How we pick and despatch product (both to stores and customers).
Delivery to stores
Delivery to customers

Summary


Introduction

Hello, My name is Tom Cross-Dockray and I am the T&K Supply Chain Manager. Welcome to our Swindon Distribution Centre. Today, I will be showing you how the T&K supply chain business operates on a day to day basis and some of the processes involved.

I will start by explaining what our particular supply chain network looks like and some of the problems we have faced over recent years. We will then look at how T&K operates by looking at:
how orders are generated (for the stores, the DC and also from individual customers buying via kiosks or the internet);
how we receive and manage stock through the supply chain;
and finally how we pick and despatch product (both to stores and customers).
I will finish with a summary of the key benefits that an ERP system has provided with.

[ HAVE A DIAGRAM TO REPRESENT THIS CYCLE ]

Our current supply chain configuration

Today, T&K has X stores in the UK, 5 in France and 5 in Germany. We have a variety of formats ranging fom 20,000 square feet to 40,000 square feet with the average store being 32,000 square feet. As you saw in the store, our products are based on three main categories – homeware, fashion and ambient and frozen grocery, supplied from the UK, Europe and the Far East. You will have heard that our business has experienced a enormous growth in volumes and that there are plans to expand across Europe. In addition to stores, our Internet web site has also seen an increase in sales, particularly from customers across Europe.

To service all of this, we have the following supply chain network :

[Demonstrate UK & Europe Map showing T&K stores, NDCs and RDCs]

We have two National Distribution Centres (NDCs) in Swindon and Manchester and three Regional Distribution Centres in London, Nottingham and Newcastle.

The NDCS have four main functions. They :

Act as bulk stores for manufacturers who cannot ship directly to our Regional Distribution Centres ( however, products are not stored here for any length of time as the bulk deliveries are broken up and sent on to the appropriate RDC in full pallet loads);
Hold our slow moving products which are picked and sent to RDCs;
Hold our frozen product lines;
Acts as an RDC for their own set of stores delivering frozen products in frozen trucks - Swindon services our stores in the South West and Manchester the North West; In the future, we are also looking to deliver slow movers together with forzen products in composite trucks;

Our supply chain objectives are to hold as little stock as possible in our distribution network. However, some stock may be held in the NDCs where it is more economical to do so than receiving smaller and more frequent deliveries. This is usually part pallets of stock which have not been sent to either RDC.

We have segmented our Swindon DC into two parts – one part that services stores and the other which holds stock for our mail order catalogue, internet and kiosk shopping lines. When a customer order is received, a picking list is generated, products are singles picked, sent on to one of the RDCs where a private courier network picks it up for onward delivery to the customer.

Our Manchester NDC also acts as our clothing distribution centre, with specialist receiving, storage, picking and packing equipment installed in one part of the DC.

Our RDCs have the following functions :

Receive deliveries directly from suppliers (in case loads which may include part pallets) for chilled and fast-moving products;
Do any pre-retailing i.e. converting stock into shelf-ready format;
Consolidate deliveries from NDCs and suppliers into single deliveries for stores;
Receive consolidated mail order deliveries from Swindon NDC which are sorted and picked up by a private courier network for delivery to customer homes or pick-points.

These RDCs are virtually stockless because most incoming deliveries are cross-docked and sent straight out to stores. If there is any stock held in our network, then it is at the NDC. All stores get daily deliveries from our RDCs and we have the capability to increase or decrease this frequency based on need.

Our 5 stores in Germany and 5 stores in France are currently supplied by a third party distribution company. However with the growth of our European business, both from stores and the Internet, we are going to have to look at European distribution more carefully. It is likely that we will be making an acquisition in Europe. That will be the right time to look at this issue.

The supply chain: Problems we used to have and recent advances

I would now like to take you back in time to a dark and dismal period. When I first joined the company about 5 years ago it was very difficult for me to do my job effectively. At T&K, we were experiencing high levels of residual stock, larger than expected mark-downs and poorer than planned margins. We simply could not address some of these problems because of systems and infrastructure limitations. In particular, :
We had to use several separate systems for ordering stock, forecasting, allocations, replenishment, managing stock in the stores, warehouse management and also a separate product master file.
Ordering was often haphazard, forecasting wildly inaccurate, replenishment orders were generated automatically but not trusted and frequently changed.
My staff often had to re-enter information into different systems and had to look at different systems to obtain information. Often we found that information was different in different places or out of date. Reconciling data was a nightmare and often impossible.
 There was no visibility of inventory along the supply chain. Stores could not tell what they would get when, whether or not we had the stock in our DCs or if it was on order. Head office had no visibility of what was on order or when it would be delivered. Tracking imports in this way was particularly difficult.
We were unable to get improvements in our processes such as reducing some of the lead times in replenishing stores, placing orders for products and so on.

To summarise, we were just about getting by with bandages and plaster addressing the symptoms rather than the causes of our problems.

As part of our IT strategy, we had to take a long and hard look at the replacement for a set of ageing bespoke and package applications. Initially, there was resistance to using an ERP system given the perceived lack of functionality, lengthy implementation timescales, high cost and risk associated with them. We selected SAP Retail because we believe the product is reaching the level of maturity that we require and will be a leading contender within 18 months given the level of investment being made in its development.

Now things have improved significantly. T&K has improved supply chain performance considerably over the last year or so by developing our supply chain managers’ capabilities in managing the supply chain. Our new SAP system has been fundamental in developing this with its provision of integrated information.
All areas of the business can see the same data easily within a single system.
Purchasing, forecasting, replenishment, allocations, warehouse management, inventory management and customer order fulfilment (home shopping) are all integrated so that we can now see what orders we have in place, what requirements the stores have on the DC, when suppliers will be delivering stock and so on.
We have an EDI gateway set up so that data can be exchanged with our suppliers.
We spend less time fire-fighting which has given us more time to plan and manage our business.

Does this mean that everything is now perfect? No, this is only the first stage in our development. There are still areas where SAP functionality is either weak or non-existent. Going forward, we have further plans:
To utilise other emerging SAP functionality such as the SAP Supply Chain Management Initiative (a new piece of SAP functionality due out shortly) and the Business Information Warehouse
Decide what to use for warehouse management - we are currently doing an evaluation where SAP is one of the contenders.
Further automate our warehouses by the use of radio frequency terminals
Use a transport planning tool to help manage our transportation processes.
Use data from our ERP systems as an input to strategic planning.

Story

So how does this all work in reality? Today, within T&K, we obviously order a number of different types of products from our suppliers. Through the supply chain some of these are performing well and some still require improvement.

We will be using 3 main examples to illustrate this:
We will take an example of one of our existing fast moving grocery items, our own brand of T&K crisps. These are performing badly and we want to use new suppliers. These are replenished on a daily basis both into store and DCs.
In our Home department, we have a slow moving article, candles, which have been performing well. These are replenished on a weekly basis, both into store and DCs.
We will be introducing a new seasonal article, men’s khaki trousers into our stores. These will be allocated to the stores initially then ordered via replenishment.
[ Check these are still valid, there are now more articles and stories through the tour ]

We will start by looking at some of the ways product is ordered. In the previous tours we have seen how a product’s life starts in the category management process as initial purchasing quantities are decided upon and also how a product’s life ends as Mrs Jones buys product in the store. However, both these processes drive out orders for the supply chain. We’ll take a look at how these initial orders are generated and pushed through to the stores, then how Mrs Jones’ purchase is replenished in both the stores and then the DCs, and finally how other types of order can be created.


Allocations

Allocations are a way to push merchandise through from the DC into the stores. As we said earlier, we often did not know how much to allocate to the stores, and what to reserve in the warehouse for replenishment. We are now able to use allocations to help us.
Allocations can be calculated using:
Fixed allocation rules where merchandise will be distributed to sites according to fixed quotas (either in values or percentages) – for instance homeware
Generated allocation rules, where the quota each store receives is based on figures such as sales – for instance fashion
Allocations can be to specific stores or groups of stores. They can be generated in a number of ways:
Simply entered manually
Based on historical information, such as allocating by percentage using the previous sales figures of the merchandise category
Using a general mechanism such as store grade and the range assortment plan

[ This demo picks up from the Head Office tour and we create an allocation table for the men’s khaki trousers. These are then ordered from the vendor. ]



Replenishment

We will start by looking at what has happened within the store where we saw Mrs Jones buy some products. How does the store reorder and refill its stock? Then how does the DC replenish its stock?

Replenishment: Problems and solutions

In the past, we faced a number of problems including:
We replenished the stores and the DCs separately often ordering product for a DC when we were about to stop selling it in stores.
We allowed far too many replenishment orders to be modified.  The system suggested orders were rarely used as the staff did not trust the suggested quantities.
POS data was not readily available in a timely manner to drive replenishment.
It took 3 days between generating a store stock requirement and picking stock at the DC or sending an order to a supplier.
In certain lines, such as seasonal apparel, we did not know how much to allocate to the stores, and what to reserve in the warehouse for replenishment.

We have now been able to solve these because:
Replenishment is centralised and integrated across the business and stock is visible throughout the supply chain so we only buy stock if it is genuinely needed.
We have established replenishment guidelines for certain categories.  This has resulted in category profits improving, inventory levels falling, and warehouse space costs falling.
A key objective is to move product through the supply chain as rapidly as possible.  POS data and forecasted demand are used together with new replenishment algorithms to drive replenishment across the entire supply chain. This has eliminated huge stock build ups and allowed only the required stock to be sent to the store.
There is an ongoing focus on enhancing our replenishment algorithms.
We now use sales to drive replenishment, with call-offs to the DC and also to the supplier as required. The supplier order is now for a limited amount initially, although there are blanket agreements that specify total seasonal quantities. We are able to wait until the season is underway before placing repeat orders to local suppliers, in the sizes and colours currently selling.

Overnight the replenishment run for the stores takes place. For the Swindon store, we can see that the products Mrs Jones bought now needs to be re-ordered. This has automatically generated a replenishment order on our Swindon DC. This has two main effects:
First, it obviously places a requirement on the DC which is automatically taken into account when replenishment runs for the DC.
Second, the DC needs to pick, pack and delivery the required product at the correct time. We’ll look at this later during this tour.


Overview of SAP replenishment

We can take a more detailed look at how an ERP system such as SAP has helped us with replenishment both in the stores and in the DCs. SAP provides a number of benefits and the replenishment runs take into account not only the current stock position but also any stock on order and any planned goods issues – i.e. it looks ahead and only orders what is genuinely required. We can replenish based on the article and the store or DC. Also, using different replenishment profiles and groups has enabled us to improve our replenishment and made the maintenance of parameters easier.

We are able to replenish products in a number of different ways with differing criteria including:
Manual and automatic re-order points
Replenishment based on forecasts of sales
Time phased planning (taking into account delivery cycles)
Automatic selection of source of supply (including quota arrangements where appropriate)
Determination of replenishment requirements based on stock data taking into account expected receipts and issues
Determination of a target stock level (manually, or automatically using a forecast)
Creation of safety stock

SAP offers many different types of replenishment, the main options are:
Replenishment planning (RP): stores are supplied with merchandise in line with their demand (sales) for merchandise. The standard RP method of replenishment works on a weekly forecast (for instance the box of candles that we have seen already).
Simplified replenishment planning: articles replenished on a sell one replenish one basis (for instance some of our homeware products like the candle stick holder and also high value slow selling items)
MRP time phased planning with automatic re-order point or MRP with re-order point planning: merchandise is ordered by the DC according to a delivery cycle. The MRP replenishment method can work on a daily, weekly or monthly forecast. Demand from the stores is accumulated and calculated with other expected goods issues and goods receipts to determine the required order quantity (for instance most products from the DC)

Forecasting

Associated with replenishment is forecasting, which drives much of replenishment. Within forecasting, we often wondered how we could improve the accuracy of forecasts, particularly seasonal and promotional items. Within SAP, different forecast models (e.g. trend, seasonal or constant models) can be referenced. The target stock can be entered manually or calculated automatically using forecasts. Forecasts (and their associated fields) can be monitored and easily changed and updated as required. We can manipulate and change forecasts at both article level and merchandise hierarchy level.

It has also meant that there is increased ownership of forecasts and better collaboration between areas. In the past forecasting was not good and the stores simply placed numerous emergency orders. Now the stores and Head Office must work closely together to ensure that the orders are generated correctly.

 [ Use articles that were bought in the store ]
Start by showing forecasting. Explain replenishment parameters at article/store level and show the replenishment run at store level. Show how this has generated a store order and that this is now a requirement on the DC.
 [ This is quite a long example showing replenishment from store to DC to supplier ]
The stores are replenished using the standard RP method. In the DC replenishment takes place using MRP, the requirement on the DC is accumulated and goods issues and goods receipts are taken into account to determine the order quantity on the supplier.


Supplier ordering

The replenishment run has now generated a supplier order to be placed on a vendor.

In the past, orders were created in a largely manual process and on a different system to the inventory management system. We had poor controls on who could order what and how much they could order. Also, we often double ordered because we could not easily see what orders were already in the system. Now, as you can see, most of our ordering is automated and we have good but flexible controls in place.

Usually all purchase requisitions and supplier orders on suppliers are generated automatically or manually by Head Office. Purchase requisitions are checked by exception before being converted to supplier orders (this is usually by either store or by value). We do have the flexibility that by exception the store managers can create purchase requisitions which are always checked against certain authorisation criteria. These can then be converted into supplier orders at Head Office to be placed on the supplier. The manual purchase requisitions can have different delivery dates so that the orders can be delivered to a specified schedule.

Orders will be sent via EDI to the suppliers and we would expect to receive an ASN (advanced shipping notification) from the supplier to confirm that they will be delivering the agreed quantities on the agreed dates.

We can now look at some other examples of how purchase requisitions and supplier orders can be created, looking particularly at store managers creating requesting product, release procedures and open to buy.

[ Demonstrating creation of purchase requisitions and supplier orders ]

Ice cream are always ordered manually by the store as demand is unpredictable due to shrinkage and differing sales. The store manager raises a purchase requisition which is checked at Head Office before being converted into a supplier order.

Batteries are a standard product which are usually replenished on a weekly basis. However, due to the overwhelming and unexpected success of a new toy, batteries are in great demand. The inventory planner creates a manual purchases requisition which exceeds his authorisation level of £10,000 and the purchase requisition is blocked. His manager can view all blocked purchase requisitions and agrees to release this which is successfully converted into a supplier order.



Quota arrangements

Quota arrangements are a special form of supplier order which allow us to automatically split orders between suppliers based on a certain percentage so that each supplier receives a proportion of the order, for instance:
Always order part from a local supplier and part from a foreign supplier
We want to monitor performance of two suppliers without being totally reliant on any single supplier.

Looking at SAP,

[ Demonstrate creating a quota arrangement then raising a supplier order to show how the order is automatically split ]
In our example, as the crisps are performing badly due to supplier difficulties, we set up a quota arrangement where one supplier will now receive 60% of the order and new supplier will receive the remaining 40% of the order. As we create the supplier order, the system will automatically select the required supplier.


Loadbuilding (– no demonstration)

Loadbuilding is a way to help us to optimise our purchasing. We used to find that we would receive a container from a supplier only half full or we would order from a supplier then order a different product from the supplier only shortly after. We now use loadbuilding to:
Minimise transport costs by making best possible use of the means of transport (freight container, truck, etc.)
Achieve the best possible purchase prices by making full use of any scaled conditions from the suppliers
Reduce number of times we need to order from a supplier
The SAP system helps us by determining our actual requirements on a supplier and then additionally looking at other articles that we order from that supplier. If we can make up the order to a convenient quantity (e.g. complete container) then the order is amended to take other products as well.



EDI to/from suppliers

[ Note: we will not actually demonstrate EDI, pretend it has been EDI’d to supplier and show an existing ASN within SAP ]

We have seen how we can create supplier orders, but what do we do with them? In the past, we had to print them off, and either post or fax them to the supplier. This wasted time, they often got lost and were difficult to keep track of. Now, we simply send them via EDI to our supplier so they receive them immediately.

Also we have arrangements with our suppliers so that they send us an ASN (advanced shipping notification) confirming that the quantities, dates and instructions will be met, or highlighting any differences. This is automatically linked to the original supplier order within SAP. This provides a much quicker and more efficient working relationship with our suppliers.

We will just have a quick look at an example of an ASN within SAP:

Demonstrate an ASN based on one of the supplier orders generated above.


Distribution

We will now look at how we manage some of the distribution processes, particularly goods receipt of product, cross docking, picking and goods issues to stores.

We always had problems knowing when product was due in which meant that often product was not checked properly and we were unable to reconcile stock differences. Stores would often complain that deliveries arrived at random and they had no way to know what to expect. We are now able to efficiently manage our inventory through the supply chain and now we are able to:
Know when to expect deliveries from suppliers, receive goods, check that we have received the correct articles and carry out quality checks where appropriate (this would include goods receipt tolerances)
Pick and pack goods ready for delivery to either customers or through to stores.

An ERP system has provided us with a number of opportunities to improve our process:
Goods receipts can be carried out quickly by referencing the original supplier order or the supplier ASN
We automatically set up some orders to be quality checked
We have set goods receipt tolerances for different orders and/or vendors that can automatically close orders if required
Picking and packing is more efficient and stores can see what stock they can expect and when


Inbound flow scheduling

[ Possibly EQOS or some parts of SAP. Currently within phase 1, we are only using EQOS for promotions. However, our plan is that we will be managing our inbound delivery scheduling using EQOS. ]

EQOS is a collaborative planning tool that we use to talk to our different trading partners for sharing information, particularly for inbound delivery scheduling. It allows us to create delivery slots and for our suppliers to access these and accept specific delivery slots. Delivery slots are created taking into account different parameters such as DC capacity and warehouse staffing.

Within SAP, we can enter a specific delivery date and time on the supplier order and then review a list of the expected deliveries by date and time. (Obviously changes to the schedule will be entered manually.)


We can now see how SAP carries out some of these tasks:

[ Allocation table processing ]
However, for the men’s khaki trousers, we receive product and then update the allocation table. Then create the stock transport orders form the allocation atble.


Integration

The goods receipt area is a good example of some of the benefits SAP has brought regarding integration. Compared to the old days this is a huge step forward. The supplier order is generated automatically or entered by Head Office and we can see it immediately together with any ASN from the supplier. The system tells us what we can expect in, we enter the details on the goods receipt and our stock position is automatically updated. Data only has to be keyed in once saving time and avoiding re-keying mistakes and all areas can see the same data in one place.
Additionally, as we carry out the goods receipt, a number of key integration aspects can be demonstrated. Obviously we would expect the stock quantities to be updated but also:
Within financial accounting: goods receipt increases inventory values and an accounting document is generated
The goods receipt automatically ties in to the invoice to show what we should actually pay. Additionally we have automated invoice paying (SAP ERS evaluated receipt settlements) for some vendors and as we process the goods receipt this amount is automatically paid even if it differs from the original order
The goods receipt automatically updates the supplier evaluation records so that we can monitor performance based on defined criteria (such as on time deliveries, correct quantities etc). This will be looked at in greater detail within the next Supply Chain Management Tour.

[ Integration demo required – details to be confirmed ]


Now we can look at some of the processes within the DC itself.


Warehouse management

We have progressed from a time when we had no warehouse management systems which was chaotic, to having a specific warehouse management package which was good but again we had integration problems, through to now using the SAP warehouse management module. This now provides a number of important benefits, particularly:
The warehouse management system is fully integrated with other SAP modules
Visibility of stock (enabling us to get rid of “squirrel stock”)
We can manage our complex warehouse structures with different types of warehousing facilities including automatic warehouses, bulk storage and picking faces and fixed bin storage
Ability to manage special products within the warehouse such as hazardous materials, those that are batch managed or those with shelf lives and expiry dates
It will support our proposed use of automated barcode scanners and radio frequency
Key advantage has been to allow us to monitor and improve our picking efficiency through the warehouse


Cross docking

[ Will not demonstrate but explain as if we have it in place currently. Cross-docking functionality is not good in 4.0, it will be significantly improved with version 4.5 ]

We used to have to carry high stock levels of all products but cross docking is now an important area for us as it allows us to reduce our inventory levels in the DC and move product quickly through to the stores. As I explained earlier, we use RDCs to cross dock fast moving articles or articles with short lead times (mainly grocery). We also cross dock pre-picked product from DC for shipment on to the stores (e.g. beers, wines, sprits and cigarettes).


Inventory management

We frequently had problems with managing our inventory. We found that we did not have good visibility of stock throughout the stores, inventory counts were difficult to manage and returns were a constant problem. We needed to be able to efficiently manage our inventory through the supply chain and we are now able to:
Review stock levels in different stores and by exception move stock from one store to another if customers specifically make requests
Carry out physical inventory checks within the DCs and the stores and update our stock levels as appropriate.
Stock adjustments will have reason codes and audit trails are required for the different types of stock adjustments.
Carry out returns simply and efficiently

We will look at two of these areas in more detail.


First of all, physical inventory. Stock within the DC will be subject to physical inventory counts based on cycle counting. This is a method whereby stock is given a cycle and different cycles are counted at different intervals. This allows fast moving or valuable stock to be counted more frequently while slow moving stock can be counted less frequently.

Looking at SAP,

The physical inventory counts for this week are generated and all stock with cycle counting indicator A (fast moving) requires counting. This includes the stocks of crisps. Count the crisps and variance from expected. Expected 110 packs and actually 95, enter result and reason code for difference. Show inventory level change.


The other key area is in returns. Returns are a fact of life for all retailers including T&K. We used to waste huge amounts of time and effort dealing with returns, the amount of processing was enormous and matching invoices was a nightmare. Now, we get returns from an even wider variety of sources, products returned to the store, and returns that do not come via the store, e.g. from our internet business and mail order business. The returns processing is now far easier. We process returns from a customer to a store, stores to DCs, stores to suppliers and DCs to suppliers.

We can see how this process works within SAP:

[ SAP demonstration showing returns from customer to store to DC to supplier ]
We demo the return of a pair of shoes form the customer to the store to the DC to the vendor.

[ Note: this shows returning product through the chain back to the vendor. The other main options with returns are to dispose of the product in the store or to generate a complete recall of the faulty product from all store. ]

Stock visibility is vital throughout the company, and as a supply chain manager I have access to key data, for instance that shows me stock positions through the stores, open supplier orders and so on.


Delivery to stores

Also in the past stores never had access to basic information such as their own stock holdings and also visibility of forthcoming deliveries, now they can view this easily within SAP. If you remember, Mrs Jones bought her XXXX in the store and this triggered a replenishment order to be placed on the DC. We can now see how first of all the DC processes this order and at the same time the store is able to see the progress of the same order.


 [ Creation of deliveries, picking lists, goods issues and displaying selected lists of deliveries ]
The men’s khaki trousers are due to be sent to the stores. Also there are orders ready for the following articles: crisps, box of candles, suntan lotion, lemonade (or any soft drink) and tomato soup.
As deliveries are created, the stores can view what they expect to receive and when. This gives the stores more visibility to track down orders. Picking lists are created by store and the stock picked and packed in the DC and shipped to the stores.

[ Store goods receipt ]
The goods issue document is printed off and sent with the goods to the stores. As the stores receive the new product most will carry out a goods receipt to check they have received the correct product and then display this on their shelves with the appropriate advertising.

We will see in the next tour in the store how this is actually receipted at the store.

However, some stores will simply receive the product and display it immediately. The goods receipt process happens automatically within the system at the point of goods issue from the DC (e.g. stores very close to the DC where in-transit time is minimal and/or stores which put stock directly onto the shelves without any interim storage facilities)


Delivery to customers

In the past, the supply chain would not be particularly interested in customers! Our aim was simply to ensure that the stores had sufficient stock to be able to meet the demands of the customer. Now this is changing. We still need to make sure that the stores have enough stock but this is no longer the only way we sell to customers. The traditional store is just one aspect. We now have a number of alternative channels and we sell to our customers through both our mail order catalogue and via the internet. Deliveries can be sent from the DC to the customers’ home or work.

One of our future aims is that we will be able to increase our range of products without needing to carry any stock. Our customers will be able to order articles and these will be delivered to the customer directly from the supplier.

We will have a quick look at how the SAP system supports these developments by looking at how it deals with an internet order:

We have a number of sales orders for customers who have ordered the men’s khaki trousers via the internet. We create deliveries for these customers and these are shipped separately.

We will see later in the Home tour how this product is delivered to the home of the customer.


Summary

These have been a series of major improvements to get to this stage but we still have exciting opportunities in the future. For instance, we are also looking to implement a new piece of SAP functionality, the SAP Supply Chain Management Initiative which will provide the following benefits:
Understand demand throughout the supply chain (including manufacturers, T&K and the customers)
Manage all significant factors that influence demand and the supply chain
Analyse different scenarios to meet our planning goals
Integration between SAP modules using the new supply chain cockpit view


We have now demonstrated some of the key day to day processes within the supply chain and how SAP has benefited us. So as you can see we been able to make big improvements in recent years, I can now see stock and orders throughout the system and we have been able to reduce stock levels significantly. Integration has been a huge benefit and we still have further developments to come.

Key messages

Let me repeat the key messages :

Most retail businesses operate multiple supply chains and therefore have an inherently complex supply chain operation. An ERP system such as SAP helps drive out clarity from complex supply chain processes by getting you to think about your business processes and configuring the system to support these processes.
There is a range of supply chain business transactions which have historically been done on separate systems interfaced to each other. This has presented problems in the maintenance of interfaces, having a single correct version of the data and having the capability to reduce lead times in business processes such as replenishment. An integrated system, such as SAP supports all of these business transactions, avoids the interface problems, provides a single accurate version of the data and removes constraints that prevent improvement in processes.
SAP is not necessarily the answer to all system requirements. Specialist systems may still be required in areas such as transport planning and warehouse automation, as well as replacing parts of SAP where the functionality may not match the business need.


Any questions?

Thank you. Can I now invite you to move through to the store where you can see the tour relating to a day in life of a T&K Store Manager.
Supply Chain Operations – Draft Tour Script

 DATE \@ "dd/MM/yy" 02/02/99		Page  PAGE 3 of  NUMPAGES 17




## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
