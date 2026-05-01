SAP White Paper

MULTI-CHANNEL
RETAILING

THE BEST-RUN E-BUSINESSES RUN SAP

© Copyright 2001 SAP AG. All rights reserved.

No part of this publication may be reproduced or transmitted
in any form or for any purpose without the express permission
of SAP AG. The information contained herein may be changed
without prior notice.

Some software products marketed by SAP AG and its distri-
butors contain proprietary software components of other soft-
ware vendors.

Citrix®, the Citrix logo, ICA®, Program Neighborhood®,
MetaFrame®, WinFrame®, VideoFrame®, MultiWin® and other
Citrix product names referenced herein are trademarks of
Citrix Systems, Inc.

HTML, DHTML, XML, XHTML are trademarks or registered
trademarks of W3C®, World Wide Web Consortium,
Massachusetts Institute of Technology.

JAVA® is a registered trademark of Sun Microsystems, Inc.

Microsoft®, WINDOWS®, NT®, EXCEL®, Word®, PowerPoint® and
SQL Server® are registered trademarks of Microsoft
Corporation.

JAVASCRIPT® is a registered trademark of Sun Microsystems,
Inc., used under license for technology invented and
implemented by Netscape.

IBM®, DB2®, OS/2®, DB2/6000®, Parallel Sysplex®, MVS/ESA®,
RS/6000®, AIX®, S/390®, AS/400®, OS/390®, and OS/400® are regis-
tered trademarks of IBM Corporation.

ORACLE® is a registered trademark of ORACLE Corporation.

INFORMIX®-OnLine for SAP and Informix® Dynamic ServerTM
are registered trademarks of Informix Software Incorporated.

UNIX®, X/Open®, OSF/1®, and Motif® are registered trademarks
of the Open Group.

SAP, SAP Logo, R/2, RIVA, R/3, SAP ArchiveLink, SAP Business
Workflow, WebFlow, SAP EarlyWatch, BAPI, SAPPHIRE,
Management Cockpit, mySAP.com Logo and mySAP.com are
trademarks or registered trademarks of SAP AG in Germany
and in several other countries all over the world. All other
products mentioned are trademarks or registered trademarks
of their respective companies.

Design: SAP Communications Media

2

CONTENTS

Executive Summary  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
A New Kind of Customer  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
A New Kind of Retailer  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
The New Realities of Retail  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

Customer Relationship Management and Marketing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
Today’s Customers are like Your Boss: They Want Results  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
Finding (or Building) the Tools You Need to Compete . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
CRM Marketing in the New Millennium  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7

Analytical CRM for Retail: How Well Do You Know Your Customers? . . . . . . . . . . . . . . 8
Digging for Gold: The Customer Knowledge Base . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
Turning Data Into Results  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9

The Retail Store Channel. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
Making the Synergy Produce Results  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
Preparing to go Multi-Channel  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

The Internet Sales Channel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
The Many Elements of Internet Sales  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
Big Potential, Big Challenges

The Retail Catalog Channel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
Putting the Pieces Together . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
– Customer Data Management  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
– Campaign Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
– Catalog Design and Mailing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
– Sales Order Processing  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
– Complaints Management and Service  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
– Telesales  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

The Mobile Commerce Channel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
The Perfect Retail Channel  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
Consumers Demand Perfect Service  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16

The Digital Interactive TV Channel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
Taking Retailing to the Next Level  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

How SAP Can Help You . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
Retail Store  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
Internet Sales  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
Catalog Retailing  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
Mobile Commerce  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
Meet the Multi-Channel Challenge with mySAP Retail  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19

3

4

This white paper will help you gain a deeper understanding of
the importance of multi-channel retailing for your company by:
•  Explaining the new multi-channel realities of retail, particu-

larly in terms of managing customer relationships.

•  Examining the growing role of information and analytics
•  Exploring the challenges and opportunities in each of the five
main channels: retail stores, e-commerce, catalog retailing
(including telesales), mobile commerce, and digital interac-
tive television.

•  Showing how mySAP Retail can help you develop an effective

multi-channel retail strategy

EXECUTIVE SUMMARY

The retail industry is in the middle of a revolution. The perva-
siveness of information and communication technologies has
shifted economic power from retailers, which once could dic-
tate the terms of purchase, to consumers, who can now change
loyalties as easily as they send e-mail. Recapturing those con-
sumers is the top priority for retailers, and success will go to
the companies that can rebuild that loyalty quickly, efficiently,
and without losing control of costs.

It is a daunting challenge. Customers recognize their growing
power. They are demanding lower prices, higher quality, better
selection, and round-the-clock access. Most important, retail-
ers’ wares must be accessible by whatever means customers
want – in a retail store, by phone, in a mail order catalog, from
handheld devices, or on the Web. Indeed, a growing segment of
shoppers now expects to reach a single retailer through all
possible channels.

To survive this revolution, you must shift to multi-channel
retailing. But as many retailers have discovered, an effective and
profitable strategy for multi-channel retailing requires far more
than simply bolting on a dot.com division or a telesales service
center. To be competitive, your retail channels must operate
as an integrated whole. There can be no conflict between
channels, no cannibalizing of one channel by another. Your
channels must operate in total harmony, seamlessly exchanging
data and customers, enhancing each other’s business, and all
contributing to the revenues, market share, and profitability of
your company.

5

INTRODUCTION

For retailers, the new, New Economy has brought as many
obstacles as opportunities. Consolidation and globalization
have chipped away at fat margins. Competition is forcing even
name retailers to slash prices and to develop novel offerings.
Shoppers, too, have changed. They expect better selections,
lower prices, and instant service – and they will happily dump
retailers that can’t deliver.

In this harsh new environment, the traditional rules for retail-
ing and for managing customer relationships are being com-
pletely rewritten. Gone, for example, is the belief that retailers
should pay more attention to attracting new customers than to
retaining current customers. Smart retailers know that it costs
four times as much to find a new customer as it does to keep a
current one.

A NEW KIND OF CUSTOMER
Gone, too, is the idea of a single retail channel. Traditionally,
retailers approached customers through one dominant channel
– face-to-face store retail, for example, through phone sales, or,
more recently, via pure-play online catalogs. But today, to
effectively build your customer base, you must become experts
in synchronizing your operations across multiple retail chan-
nels.

Yet even as most retailers are moving toward multi-channel
retailing, the concept itself is still evolving and poses numerous
challenges. For example, until recently, most retailers looked at
multi-channel retailing mainly as an extra – a way for pure-
play companies to go after niche customers. But increasingly,
experts say, even mainstream customers are demanding multi-
ple channels for their retail activities.

These shoppers routinely use all available channels – from
traditional brick-and-mortar stores and phone sales to Web
catalogs and even mobile commerce. Statistically, they tend to
spend more than their single-channel counterparts. That
makes them an extremely attractive new market. And multi-
channel retailing is the only effective way to reach them.

A NEW KIND OF RETAILER
Tapping this important new market requires more than simply
selling across multiple channels. It requires an entirely new
business model and infrastructure. For example, a retailer’s
channels are often so disconnected that the company back
office doesn’t recognize when one customer uses two separate
channels. And what’s worse, each time customers enter a dif-
ferent channel, they feel as if they’re interacting with a com-
pletely different company, not a single, familiar retailer.

To overcome these challenges, you must integrate your multi-
ple channels and back-office operations into a single, seamless
retail enterprise that can minimize conflict between channels.
One that can recognize and welcome each customer no matter
which channel they use. One that can offer the same quality
experience across all channels. And one that can integrate con-
sumer data across all channels, leveraging customer knowledge
to satisfy current customers while appealing to new prospects.

Making the move to a viable model for multi-channel retailing
is one of the biggest challenges you face. It involves integrating
multiple channels with existing operations, enterprise applica-
tions, and supply chains. But with the right technology, tools,
and expertise, retail organizations of any size can thrive, not
just survive.

6

CUSTOMER RELATIONSHIP MANAGEMENT AND MARKETING

THE NEW REALITIES OF RETAIL
Despite all the new commercial technologies and radical busi-
ness paradigms to emerge in the last decade, the most impor-
tant retail discovery has been the simplest: your customers are
still the king – and now they know it.

Gone are the days when retailers could claim to be customer-
oriented, yet still try to dictate terms and conditions. With the
increasingly competitive markets, declining margins, and new
technologies that enable consumers to easily comparison shop
and switch retailers, if you’re not delivering the lowest prices
and the best goods and services, “your” customers will quickly
become someone else’s.

This new reality has forced retailers to become truly customer
oriented instead of simply talking about it. For many, that has
meant completely reengineering their entire operations and
processes around the single goal of customer satisfaction. And
when you consider the need to continually control costs, drive
new efficiencies, and optimize processes without losing the
flexibility to adapt to future market trends, it’s clear why retail-
ers face a substantial challenge.

TODAY’S CUSTOMERS ARE LIKE YOUR BOSS:

THEY WANT RESULTS
It’s one thing for retailers to market themselves as having a
strong presence across all retail channels. But it’s quite another
to maintain a multi-channel presence in ways that provides
the results and experience that value-conscious consumers
demands. The same holds for every other element in the retail
operation – from supply chain management to marketing to
customer relationship management (CRM) and store operations.

But delivering that kind of performance means answering a
whole range of questions about your entire retail operations.
How well do you know your most valuable customers? Who are
they? What will keep them coming back? Do your employees
have this kind of information, or the capabilities to use it?

Do you interact consistently with all customers across all chan-
nels? Can your customers drive self-service interactions conve-
niently for routine elements of the search, buy, and service
processes?

Is your enterprise ready to handle these new tasks? Do your
employees have the information they need, and if they do, do
they know how to use it? Have sales, marketing, and service
been integrated throughout your enterprise and across all
channels? Does your front office communicate with your back
office? How do you manage your customer relationships, and
does that management help differentiate you from your com-
petition? Do you know what your customer retention rate is?

Companies that answer these questions are taking the first
steps toward becoming next-generation retailers. Those that
aren’t will continue to struggle.

7

You must also develop the capability to measure and to modify
performance in each of those critical processes. And you need
to combine advanced forecasting and simulation tools with the
latest point-of-sale data to create rolling sales projections. This
allows decision makers to not only monitor costs and revenues,
but to improve all future marketing campaigns.

CRM MARKETING IN THE NEW MILLENNIUM
For retailers today, the market reality is a blend of traditional
truths and new expectations. Customers are not only always
right, but now have considerably more power. Now, when they
demand to be treated right, they have the tools to compare
your performance. And, if they find you lacking, they will
switch to one of your competitors.

This smarter, more demanding generation of customers is forc-
ing retailers to rebuild themselves around total customer satis-
faction. More and more, retailers must personalize their offer-
ings, treating all customers as if they were the only one in the
world – all while maintaining an enterprise that is efficient,
profitable, and flexible enough to master the inevitable and
constant change that has always defined the retail industry.

FINDING (OR BUILDING) THE TOOLS

YOU NEED TO COMPETE
The new realities and rules of the retail market require an
entirely new category of business capabilities. For example, it’s
now increasingly clear that retailers must develop a fundamen-
tally new approach to marketing, one that can make highly
personalized offers to each customer using the most effective
sales channel.

It’s also clear that, to achieve such sophistication and cus-
tomization, you will require complete access to an extensive
array of customer data, including past interactions and trans-
actions, buying behaviors, and preferences. You will need the
tools to extract this data from any source, as well as powerful
analytical tools to search for buying habits, product prefer-
ences, and other critical patterns. You will need similar access
to information on segments, competitors, market channels,
trends, and profitability.

You must also be capable of executing these sophisticated cam-
paigns across all available channels. Such campaigns require sig-
nificant new technologies, as well as the expertise to tailor the
campaign to each channel, yet maintain a consistent presence
across all channels.

To control costs and continually drive efficiencies, you must
automate, integrate, and optimize your entire chain of critical
processes – from initial customer contact and sales closing to
accounting and reorder. At the same time, you must improve
your organization’s ability to move quickly by breaking down
information silos and improving communication and informa-
tion access at all levels.

8

ANALYTICAL CRM FOR RETAIL:
HOW WELL DO YOU KNOW YOUR CUSTOMERS?

Few industries illustrate the importance of knowledge manage-
ment as dramatically as the retail business. What you know
about your customers, markets, and competitors – and how
effectively you use that information to enrich your customer
relationships – has rapidly become the defining characteristic of
successful retailers.

Although analytical CRM is sharply focused on customers, that
focus in recent years has broadened to include related objec-
tives. For example, you now need to examine your customer
relationships against a variety of activities (such as marketing,
sales, and service) and in a variety of contexts (such as the
separate channels you use to reach your customers).

Who are your customers? How much value can each of them
bring to your enterprise over the course of the relationship?
What factors influence their buying decisions? Which channels
do they prefer and why?

But whatever the focus, the broad objectives of any analytical
CRM capability remain the same: enabling you to build better,
more profitable, longer-lasting customer relationships by im-
proving what you know about those customers.

Which of your customers drive most of your profits today?
Who will drive them tomorrow? Which of your customers are
most likely to leave you for a competitor, and what factors
cause them to leave?

Analytical customer relationship management (CRM) – the
capability to ask and answer questions like these, quickly and
accurately – provides a substantial competitive advantage for
retailers. With solid customer data, you can not only identify
your high-value customers, you can also target them with
short-term initiatives and smart strategies to extend these prof-
itable relationships over the long haul.

Effective analytical CRM offers three vital functions. First, it
enables you to gather customer information from all relevant
sources – internal operations as well as third-party sources.
Second, it provides tools to thoroughly analyze that data to
deepen your understanding of each customer’s value, needs,
and behavior, as well as to identify those customers with great-
est long-term profit potential. Third, and most important, ana-
lytical CRM lets you leverage these findings throughout your
enterprise, improving the way you interact with customers,
how you organize your business, set strategy, and make future
plans.

DIGGING FOR GOLD:

THE CUSTOMER KNOWLEDGE BASE
At the heart of an effective analytical CRM system is a robust
data base with all relevant information about your customers:
Who they are, how and when they shop, and through which
channels. With this information, you can not only gain a better
understanding of your customers’ needs, you can also more
clearly see how to orient your organization to meet those
needs.

But gaining such deep knowledge is a complex task, especially if
you operate across multiple channels. First, you must develop a
systematic approach that captures data from all relevant
sources, ranging from point-of-sale in each channel to third-
party information about trends in customer spending.

For example, to gather maximum customer data, customers
themselves must be willing to become “known” to your organi-
zation, to supply information about themselves and their buy-
ing behaviors. You can encourage this by using loyalty schemes,
which reward customers for sharing information. These loyalty
schemes are typically linked to devices that automatically iden-
tify customers as they enter your system.

9

Second, you need the capacity to gather, manage, and analyze
all categories of data, from simple billing data to more complex
data sets. Attitudinal data, for example, includes such important
variables as customer satisfaction, customer demographics, and
customer profiles. Behavior data includes customer contracts,
transaction data, customer responses to promotions or queries,
customer complaints, and other information on customer
interactions.

Third, you need the tools and know-how to analyze each chan-
nel for performance, profitability, and preference by customer
group, including both known and unknown customers. You
must also be able to assess and measure buying behaviors and
purchase patterns in each channel. Most important, you must
be able to quickly apply the resulting knowledge to enhance
the existing customer relationships while simultaneously
attracting new customers.

Any one of these categories constitutes a massive volume of
data. Yet to be effective, your customer knowledge base must
not only be able to easily handle such loads, but integrate it all
seamlessly and rapidly for both an analysis and for back-office
functions, such as billing, financial planning, and overall prof-
itability analysis.

TURNING DATA INTO RESULTS
Clearly, once customer data has been extracted and integrated,
the main function of any analytical CRM system is to translate
that raw information into useable results. You must be able to
analyze each channel for performance, profitability, and prefer-
ence by customer group, as well as to assess the buying behav-
iors and patterns of customers in each channel. You must be
able to quickly use these insights to enhance existing customer
relationships while simultaneously attracting new customers.

For example, you can look for models for customer behavior
that help predict future sales and use them to make plans and
allocate resources. Modeling the behavior of high-value cus-
tomers especially can help you make the best decisions in
resource allocation, marketing campaigns, and even long-term
strategy.

At the same time, an effective analytical process can provide
benefits besides better customer relationship management. You
gain increased transparency and organizational control. You
can better streamline the planning process, and you can more
closely align strategy with other core functions. An analytical
function that can integrate its analysis across all channels
ensures cohesive multi-channel planning and minimizes inter-
channel conflict.

Ensuring a steady stream of fast, accurate customer information
poses one of your most complex challenges. These systems must
simultaneously collect, manage, and analyze vast volumes of
data from a welter of data sources and still be flexible enough
to handle the subtle differences of your customers, markets,
and strategic goals. Yet what is clear that without such a capa-
bility you will find it hard, if not impossible, to compete in
today’s data-saturated retail economy.

10

THE RETAIL STORE CHANNEL

It’s hardly surprising that brick-and-mortar retail still com-
pletely dwarfs its virtual counterparts. Despite the clear benefits
of shopping online, most consumers clearly prefer, at least peri-
odically, the features of a physical retail environment. Among
these: the smell, touch, and taste of goods; the emotional
impact of the environment; the face-to-face contact with store
staff; and the instant availability of goods. In-store retail pro-
vides even successful multi-channel retailers with 90% of their
turnover.

But for all the success of this traditional channel, the retail store
cannot stand on its own in the new, New Economy. Instead, the
store must become an integral piece of a synergistic multi-chan-
nel retail model that draws on the specific strengths of all chan-
nels.

Just as the retail store channel can help spin off benefits for
online retail and other channels, these other channels can cre-
ate new customers and business for the retail store. The chal-
lenge, therefore, is twofold: further improving the ability of tra-
ditional stores to compete against other brick-and-mortar
retailers, while simultaneously reengineering them to function
seamlessly within a new, integrated multi-channel retail organ-
ization.

MAKING THE SYNERGY PRODUCE RESULTS
Although multi-channel retailing isn’t a new idea, many retail-
ers are still learning about the complex interplay between
channels and how the strengths and weaknesses of one channel
can impact others. For example, existing retail store business
can help build business in other channels in a variety of ways.
Its strong customer base and familiar brands can be quickly
transferred to other channels with relative ease and minimal
advertising and marketing costs. The stores’ existing supply
chain, distribution network, and selling environments provide
other channels with a ready-made infrastructure and a network
of critical vendor relationships. And with its physical qualities
and instant product availability, the store can compensate for
what other channels lack: the immediate touch and feel of the
merchandise.

The retail store channel also receives important benefits from
its sister channels. For example, Internet sales and catalog
retailing can point customers to retail stores. These channels
also tend to prime customers for eventual purchase by giving
them fast, no-pressure product information and whetting their
appetite to see the product in person. And because Internet and
catalog shoppers tend to spend more than store-only cus-
tomers do, these channels can play an important function by
feeding high-value customers to your retail store channel for
additional purchases.

By providing additional ways to access your products, Web,
catalog, and other channels encourage customers to feel they
are being served by all means possible. And that leads to better
customer loyalty and helps build longer-lasting, high-value
customer relationships.

11

PREPARING TO GO MULTI-CHANNEL
To fully exploit its position in the multi-channel enterprise,
the retail store must become more efficient and integrated in
core functions, such as the management assortment and price,
replenishment, customer relationships, inventory manage-
ment, and human resources. In this way, the retail store can
simultaneously improve its capacities to compete in its own
channel, while working more seamlessly with its sister
channels.

Consider price management, for example. Whenever the sales
price of an item changes, that change must not only be commu-
nicated instantly to all other internal systems, such as cashier
systems and electronic shelf labels, but all other sales channels,
as well. If you expect your customers to pay different prices for
the same goods, you better give them a very good explanation.

Similarly, in promotions management, all channels carrying
the promotion must be in sync to exploit cross-channel syner-
gies – or, at the very least, to avoid cross-channel discrepancies.
For example, if a retail store offers a particular promotion, Web,
catalog, and e-mail channels can enhance the campaign by pro-
viding information to consumers, as well as by providing con-
sumers with additional opportunities to purchase.

Nowhere is cross-channel integration more critical than in the
area of customer data. Retail stores must not only collect and
manage customer data for their own internal needs, they must
also share that information with other channels, as well as with
back-office operations.

This integration is not only important for smooth and efficient
back-office functions, it is also necessary to present a single face
to consumers, who increasingly want to interact with your
organization across multiple channels. If you can’t follow your
customers as they cross channels, they won’t be your customers
for very long.

Consider, for example, the customer who has just placed an
order on your Web site or using your mail order catalog and
now is standing in your retail store asking to place an order in
person. He will quite reasonably expect to be recognized by the
store’s systems and afforded the same financial terms and relat-
ed offers. He may wish to call up his account and view orders
he has placed on other channels and perhaps even deal with an
earlier complaint. Being able to satisfy this multi-channel shop-
per – and retain his loyalty – largely depends on integrated,
cross-channel data management.

Multi-channel shoppers aren’t the only change that you must
face, but they do represent an important and growing new
market that you must adapt to. They also offer a dramatic illus-
tration of the need for successful retail store operations to
embrace a truly multi-channel model.

12

THE INTERNET SALES CHANNEL

Nearly a decade into the New Economy, few in the retail busi-
ness would deny the huge potential of e-commerce as a retail
channel. Accessible, flexible, and instantaneous, it has empow-
ered consumers, while giving retailers an entirely new, relative-
ly low-cost means to reach customers.

Yet the same short history has also demonstrated the chal-
lenges still facing Internet sales as a viable business-to-cons-
umer (B2C) channel. Supply chain infrastructure, for example,
has posed huge problems, both for pure-play e-retailers, which
lack adequate facilities of their own, and especially for e-retail
spin-offs, which often find themselves competing with their
parent retailer for supply chain support.

On the other side of the counter, many customers have been
reluctant to become perfect e-consumers. They resist surren-
dering the kind of private information that retailers need to
fully exploit Internet sales. Worse, the same technology that
has empowered consumers to shop when and how they want
has also made it far easier for them to switch retailers effort-
lessly.

In short, what many online retailers seem to lack are the very
things their store counterparts have in spades, namely, loyal
customers, proven supply chains, and established vendor rela-
tionships.

However, while it’s clear that Internet sales must be reengi-
neered to achieve these characteristics, it’s also clear that the
next generation of e-retailers mustn’t necessarily seek to dupli-
cate or compete with retail store channels. Instead, the Internet
sales channel must become far more closely integrated with the
retail store channel, while simultaneously improving your abil-
ity to compete in the online retail space.

THE MANY ELEMENTS OF INTERNET SALES
Despite its relative newcomer status, the Internet is rapidly
becoming a mature retail channel. Gone are days when compa-
nies could compete simply by launching a Web site, patching
together a fulfillment operation, or bolting a Web site to an
existing retail operation. Internet sales today is a sophisticated,
complex enterprise that depends on a long chain of distinct
business functions to meet established standards for quality and
service. To be successful, you must master these functions,
which range from customer relationship management and
product display to payment and fulfillment, and perform them
faster, better, and more cheaply than your competitors.

13

For example, e-retailing relies on aggressive, yet sophisticated
tools to reach customers. You can use click-through Web adver-
tisements and tie-ins from partner Web sites to bring potential
buyers to you Web sites. But increasingly, Internet sales retailers
are shifting to smart marketing, such as using e-mail to target
specific consumers with personalized offers.

These smart campaigns have a comparatively high rate of suc-
cess, but only at a cost; they require e-retailers to have an
extensive base of information on each customer’s buying habits
and preferences. Building, maintaining, and exploiting these
databases will become a main challenge, as well as a major
means of competitive differentiation.

E-retailing also requires sophisticated product display technolo-
gies. Internet shoppers today have declining tolerance for poor-
ly organized online catalogs or dysfunctional search engines.
Catalogs must also be fully integrated with order-fulfillment
operations, inventory replenishment, and back-office functions,
such as customer payment.

Catalogs must also share product information and prices with
all other channels. Today’s high-value shoppers demand inter-
action with your organization across multiple channels. A
shopper who has just seen an item in your store or in a print
catalog will expect to find it online at the same price. This
cross-channel capability also requires a sophisticated customer
database and the capability to move that information where it’s
needed, quickly and accurately.

BIG POTENTIAL, BIG CHALLENGES
Few channels lend themselves so naturally to the multi-chan-
nel retailing strategy as Internet sales does. Much of what
makes up online retailing – Internet connections, digitized
data, Web-based content, and customer interface – can be mod-
ified and expanded to work with other channels. That same
flexibility makes it easier for you to adapt to other market
changes, such as new products, new competitors, or new cus-
tomer preferences.

At the same time, however, Internet sales retailers face numer-
ous challenges, especially declining customer loyalty. Because it
costs so little for customers to switch retailers, you must offer
substantial benefits to these fair-weather shoppers to secure
their loyalty. Typically, these benefits include personalized serv-
ice, which in turn requires you to learn as much as you can
about a particular shopper.

Unfortunately, today’s Internet consumers are far skeptical of
request for information. Any retailer that insists their cus-
tomers surrender personal data – for example, by requiring
them to register to use the site – risks losing that customer to a
less demanding competitor. In the coming years, the retailers
who succeed online will be those that can gather the most data
in the least intrusive way and quickly turn it into goods and
services that customers instantly recognize as valuable.

14

THE RETAIL CATALOG CHANNEL

The retail catalog channel has seen a renaissance in recent years,
with catalog retailers enjoying higher sales. This channel (and
its associated telesales function) has emerged as a critical busi-
ness builder for other channels in multi-channel retail enter-
prises, and it has the potential to become a major asset in
future retailing strategies.

PUTTING THE PIECES TOGETHER
In most cases, improving a catalog order operation requires an
end-to-end assessment of all core processes, including customer
management, campaign management, order processing, fulfill-
ment, payments, catalog design, analysis, and, perhaps most
important, customer data management.

The retail industry has already seen many cross-channel hybrids,
as traditional catalog retailing companies have opened retail
stores and traditional stores have offered mail order catalogs.

In many respects, catalog retailing is ideally suited to a multi-
channel strategy. Customers peruse catalogs – usually printed
or online – then make their purchases through multiple chan-
nels, including telephone, fax, e-mail, or even conventional
mail.

But as many retailers have discovered, despite its capacities as a
companion retail channel, the catalog retail channel is distin-
guished by its own specific characteristics, requirements, and
challenges in product presentation, sales processing transac-
tion, and delivery and fulfillment. Before catalog retailing can
fully assume its new role in a multi-channel retail enterprise,
you must ensure these functions have been streamlined for
maximum efficiency and cross-channel integration.

Customer Data Management
Catalog retailers are completely dependent on high-quality
customer data. The better you know your customers’ histories
and buying habits, the better you can provide services and tar-
geted offerings. To be effective, customer data must be centrally
managed and quickly available to sales and customer-service
employees, as well as to back-office billing functions and to
other channels. You also need the capacity to acquire new cus-
tomer names from third-party vendors and quickly and accu-
rately incorporate these potential shoppers into your existing
databases.

Campaign Management
Because most catalog retailing revenue is generated at a distance,
advertising and marketing campaigns are critical. Campaigns
must be carefully planned to target specific customer segments,
based on customer data analysis. Different formats, such as cat-
alogs, mail, or outbound phone calls, must be synchronized
both in form and content to ensure a consistent message. And
campaigns must be closely evaluated to determine their impact
and to help guide future campaigns.

15

Catalog Design and Mailing
For catalog retailers, the catalog is easily the most important
marketing tool. Whether online or printed, catalogs must be
carefully laid out in ways that provide the information cus-
tomers need to make buying decisions. At the same time, the
catalog process must be fully integrated with other related
internal processes, such as fulfillment and replenishment.
The catalog process must also be fully integrated with product
information processes in other channels to cater to multi-
channel buyers.

Sales Order Processing
Because mail order customers have many vendors to choose
from, the ability to provide flawless service is paramount.
Catalog retailers must develop or acquire the capacity to
process sales orders quickly and accurately, yet at a minimum
cost to the company. Catalog retail companies need front- and
back-office systems that allow sales representatives to quickly
take orders, check on product availability, check a customer’s
credit limit, check on any sale items or discounts available to
that customer, and, finally, call up a list of other products to
suggest to the customer based on the customer data. At the
same time, call center agents can combine the sales order func-
tion with service orders, thus offering the full range of cus-
tomer service.

Complaints Management and Service
Complaining customers aren’t an enemy to be avoided; they’re
a potential source of feedback that can help your company
improve its vital customer-facing functions. Therefore, cus-
tomer service employees must have the tools to not only quick-
ly solve customer problems – thereby turning customer dissat-
isfaction into customer loyalty – but to ensure that the sub-
stance of the complaint is made available to those who can
address the root causes of the problem.

Telesales
For the catalog channel, the telephone remains both a key sales
tool and a critical point of customer interaction. To bring tele-
sales into the larger multi-channel model and to exploit new
business and information technologies, you must enhance the
ways you handle both incoming and out-bound telesales. For
example, with inbound calls, you must quickly determine
whether the caller wants to buy a product or requires service
for an existing purchase. Agents must have access to all kinds of
information, including customer accounts, product and order-
ing information, and customer service options, and they must
also be able to route calls efficiently and accurately. These capa-
bilities, in turn, require a seamless integration between all cus-
tomer-facing call center functions, all back-office processes, and
all relevant processes in neighboring channels.

16

THE MOBILE COMMERCE CHANNEL

Mobile commerce (m-commerce), the ability to make purchas-
es anywhere in the world via mobile phone or other handheld
device like a personal digital assistant, may be the most radical
new development in retail. Although initial users were mainly
business buyers who needed to make procurement or travel
purchases quickly, m-commerce is becoming increasingly pop-
ular among consumers. That has created a great deal of excite-
ment among multi-channel retailers, which see m-shopping as
a new means to boost market share and profitability, enhance
customer loyalty, and cut costs.

However, if mobile commerce is to truly achieve its potential as
a bold new strategic retail channel, it must make the transition
from a rough novelty to a seamless interaction that adds value
for both consumer and retailer. For retailers, that means refin-
ing the mobile commerce sales channel into one that can be
simultaneously personalized for each potential customer, yet
fully synchronized with the company’s other retail channels, its
back-office operation, and its strategic plans.

THE PERFECT RETAIL CHANNEL
Mobile commerce is ideally suited for impulse purchases –
goods and services that consumers decide to buy at the spur of
the moment, such as tickets for an evening show or the CD of
an artist they have just heard on the radio.

But as mobile commerce develops, its use will spread to other
kinds of purchases, especially in retail situations where cons-
umers need fast product and pricing information. For example,
picture a consumer standing in stereo store wishing she had an
instant price comparison. With mobile commerce, she could
dial in to a subscriber service and have the information within
seconds.

M-commerce can also take targeted marketing to the next
level. Suppose, for example, that you had a music product tai-
lored for 14- to 21-year olds. Using customer data bases, you
could compile lists of those potential customers with mobile
commerce capability, such as cell phones or PDAs. You could
then quickly alert these customers to the promotion and pro-
vide the location of the nearest store and any relevant dead-
lines. The alert could also contain the number for a call center,
which the shopper’s phone could automatically dial, allowing
the consumer to purchase the product simply by pressing a
button. At the same time, all transaction data would be
returned to the retailer’s data base, where it where it could be
used to design even better marketing campaigns in the future.

17

TAKING RETAILING TO THE NEXT LEVEL
All in all, the greatest advantage of mobile commerce is that it
brings you much closer to consumers than ever before. You
can now directly address consumers with the latest product
information, promotions, or other important news.

Mobile commerce is clearly one of the most exciting develop-
ments in the retail world. It meets the consumer’s desire for
instant gratification, any time, and place, while functioning as a
kind of mobile gateway to your multi-channel enterprises.

CONSUMERS DEMAND PERFECT SERVICE
To achieve these kinds of transactions with any sort of volume,
mobile commerce systems must provide near-flawless perform-
ance. Shoppers will expect mobile commerce not only to increase
shopping opportunities, but to be efficient and reliable. With so
many other channels available, consumers simply won’t tolerate
awkward ordering mechanisms, unreliable product information,
or late or missed product deliveries.

In general terms, that means retailers must create an end-to-
end system for reaching customers, providing information,
processing orders and fulfilling orders, and settling payment.
The system must be easy to use, provide personalized contract
with targeted offers, and generate provide accurate, up-to-date
information on pricing and availability. It must also ensure fast
order completion and fulfillment, order status tracking and
delivery, secure payment, and correct billing. Finally, it must be
able to exchange customer and product information instantly
with other channels.

18

THE DIGITAL INTERACTIVE TV CHANNEL

Gloomy day? It won't stop raining? Can’t imagine your cus-
tomers leaving their comfortable homes to come to your stores?

What if they didn’t have to? What if you could bring the retail
store experience directly into your customers’ homes, instead?
With the rapid development of digital interactive television,
you will soon be able to do just that.

Combining the rich visual images of broadband television with
the interactive, point-and-click interface of the Internet, digital
interactive TV offers a powerful new retail channel. From the
comfort of their homes, customers can quickly and easily find,
view, and purchase goods and services from a comprehensive,
well-organized catalog.

Digital interactive TV is already making significant advances in
the retail market. In the United Kingdom, for example, more
than four million households can already shop using digital
interactive TV. Access to the service costs only a few pounds a
month and is provided via a set-top box with an infrared key-
board and user-friendly remote control. In addition to shop-
ping opportunities, providers are already integrating more and
more interactive content into digital interactive TV, such as
electronic banking and e-mail.

Yet, digital interactive TV is more than simply another channel.
Like all retail channels, it has its own characteristics and require-
ments, and it must be carefully integrated into your entire retail
operation and multi-channel strategy.

19

HOW SAP CAN HELP YOU

Multi-channel retailing is no longer an option or niche play; it
is a necessity for creating customer satisfaction and ensuring
sound financial performance. mySAP Retail has been specifical-
ly engineered to help support and integrate your operations
across all key retail channels – retail stores, Internet sales, cata-
log retailing, interactive television, and mobile commerce.
Designed in collaboration with some of the world’s top retail-
ers, mySAP Retail offers a truly comprehensive approach to
your entire operation, from all customer-facing functions to
every core and back-office process.

mySAP Retail delivers the full range of capabilities you need to
master the new multi-channel retailing model. Sophisticated
business warehouse capabilities help you understand and ana-
lyze all your customers, markets, and competitors in incredible
detail. Powerful customer relationship management tools help
you build and maintain long-lasting relationships with your
most profitable customers. And market-specific solutions help
you optimize operations across channels and within each indi-
vidual channel.

RETAIL STORE
mySAP Retail helps you to maximize retail store operations
while you simultaneously benefit from closer integration with
your other channels. Leveraging state-of-the art, Web-based
technologies, mySAP Retail helps integrate to your central
merchandising system, links point-to-point sales systems, and
automates labor scheduling. It provides fast access to all critical
data – sales, operations, and workforce data – so you have accu-
rate reports, budgets, and forecasts to assess profitability at any
level of detail, right down to individual products.

INTERNET SALES
With mySAP Retail, you can provide your customers with an
online shopping environment that is not only smooth and
effortless, but fully integrated with your back-office processes
and your other retail channels. Engineered for the latest devel-
opments in Internet shopping, mySAP Retail lets you create the
ideal customer-facing Web presence, with personalized, easy-to-
use interfaces, fast search functions, and real-time product pric-
ing. With mySAP Retail, your Web operations are fully synchro-
nized with other channels, and your Internet sales channel can
share customers, business, and critical information with your
other channels for greater revenues and lower expenses.

CATALOG RETAILING
With mySAP Retail, you can build an efficient catalog sales
operation that not only maximizes its own revenue streams,
but guides customers and potential revenue to your other retail
channels. Sophisticated front-end tools let your telesales and
customer service agents interact with customers with optimum
efficiency, taking orders, checking product availability and
account status, expediting complaints and service requests, and
even guiding customers to other channels. At the same time, a
fully integrated suite of back-office solutions lets you quickly
process orders, manage inventory and analyze sales, customer
behavior, and product profitability.

20

MOBILE COMMERCE
mySAP Retail lets you take advantage of the growing segment
of mobile commerce. This powerful, cutting-edge solution
gives you the tools to exploit the kind of impulse shopping
behavior that this channel favors. You can quickly identify
potential markets, create highly targeted mini promotions with
special content tailored for cell phones and other mobile
devices, and build an order entry and fulfillment system that
rewards impulse purchases with on-time, accurate deliveries.
mySAP Retail can support the transition to a mobile sales chan-
nel, helping you evaluate the impact of m-commerce on your
supply chain and your existing customers, as well as what this
new channel will mean for such core functions as security and
finances.

MEET THE MULTI-CHANNEL CHALLENGE

WITH mySAP RETAIL
The days of the single retail channel are over. Customers today
expect to shop any time, anywhere, using whatever channel
suits them. If you can’t offer a consistent presence across all
retail channels, your customers will find a retailer who can.

With mySAP Retail, you can compete in this new, more complex
multi-channel environment. You can meet customers on their
own terms, ensuring better loyalty and long-term interactions,
while simultaneously leveraging multiple channels to expand
your own enterprise.

21

22

23

THE BEST-RUN E-BUSINESSES RUN SAP

SAP AG
Neurottstraße 16
69190 Walldorf
Germany
T +49/1805/34 34 24
F +49/1805/34 34 20
www.sap.com

50 0xx xxx (YYMM/xx) Printed on environmentally friendly paper.

