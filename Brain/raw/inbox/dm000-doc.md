---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/BP/Dm000.doc.md
tags: [retail, consulting-reference, pwc, mh, petsmart, finance, 1997-1999]
project: retail
status: unprocessed
---

# Dm000.doc

## Source
File: `Brain/raw/.extract/BP/Dm000.doc.md`
Size: 16,749 bytes

## Raw content
 TOC \o "1-2" I. Hierarchy / Table Maintenance	 GOTOBUTTON _TOC410785862   PAGEREF _TOC410785862 2
A. Objectives	 GOTOBUTTON _TOC410785863   PAGEREF _TOC410785863 2
B. Critical Success Factors	 GOTOBUTTON _TOC410785864   PAGEREF _TOC410785864 2
C. Assumptions	 GOTOBUTTON _TOC410785865   PAGEREF _TOC410785865 2
D. Requirements	 GOTOBUTTON _TOC410785866   PAGEREF _TOC410785866 2
E. Issues	 GOTOBUTTON _TOC410785867   PAGEREF _TOC410785867 4
F. Reports	 GOTOBUTTON _TOC410785868   PAGEREF _TOC410785868 5
G. Existing SAP functionality	 GOTOBUTTON _TOC410785869   PAGEREF _TOC410785869 5
H. Addendum	 GOTOBUTTON _TOC410785870   PAGEREF _TOC410785870 7


Hierarchy / Table Maintenance
Objectives
To provide an accurate representation of PETsMART’s site and merchandise hierarchies in order to facilitate business decisions, aid efficient execution of mass maintenance procedures, and support profit generation
Critical Success Factors
Ability to provide accurate history on transactions
Ability to provide complete article and site descriptive information
Ability to consolidate information into meaningful hierarchies
Ability to quickly and effectively mass-maintain articles and sites
Ability to evaluate the performance of sites, merchandise, and personnel through formal and informal hierarchy levels
Assumptions
The organizational structure piece (corporate and sales / purchasing organizations) will not be addressed by this process
Requirements
Site Hierarchy Requirements
Place sites in multiple site groupings (for example, allow a store to be in the flea & tick group and the mild climate group)
Maintain site hierarchy maintenance security: assign owners of the site hierarchy and permit changes to existing site groups, characteristics, and the formal site hierarchy only with authorization
Group sites together for reporting and mass maintenance (assortment management, allocation, pricing, and promotional functions) based on the formal hierarchy, site groups, and site characteristics.
Mass maintain site characteristics based on the formal hierarchy (for instance, set a climate characteristic for all stores in the northeast region to the value, “cold”)
Allow multiple characteristic values for each site characteristic. (for example, a site has a characteristic called “competition” that is used to designate the store’s local competitors. Allow two or more competitors to be assigned to the site)
Allow sites to be regrouped into new hierarchies as the business and its requirements evolve
Maintain a personnel hierarchy that is independent of the site hierarchy, but can be linked to it. For example, attach a market manager to 15 sites and a market coordinator to a subset of those sites. As part of each associate’s performance evaluation, report on the sales history for the sites to which the manager is linked.
When creating a new site, allow a user to base the new site off a similar site, inheriting the model site’s characteristics and site group membership.

Merchandise Hierarchy Requirements
Group articles together in formal and informal hierarchies for reporting, pricing, cycle counts, promotions
Apply characteristics to every level of the merchandise hierarchy. For example, assign a “buyer” characteristic to the department level to designate the buyer responsible for that department.
Place articles in multiple article groups (for example, allow a flea-control shampoo to be in the flea & tick group and the dog HABA group)
Maintain merchandise hierarchy maintenance security: assign owners of the merchandise hierarchy and permit changes to existing article groups, characteristics, and the formal merchandise hierarchy only with authorization
When changing a parent article’s characteristic or other attribute (such as price), allow the user to choose to apply or not apply the change to the article’s children
Allow multiple characteristic values for each article characteristic. (for example, an article has a characteristic called “customer” that is used to designate the product’s target animal. Allow two or more customer values to be assigned to the article--”cat” and “dog” for an all-purpose pet brush)
Report articles to multiple summary levels within the informal hierarchies (List sales for all the flea & tick products ranked “best”, for example)
Produce standardized and ad hoc reporting on sales, inventory, receipts, gross margin, rebates and allowances, and markdowns at all levels
Perform mass maintenance of articles (pricing, replenishment, promotional planning, space planning) based on the formal hierarchy, article groups, and article characteristics.
Assign pricing parameters at any hierarchical level including:
Company, division, department, class, merchandise category, generic article
Across hierarchical level based on article characteristics
Combinations of two levels. For example, all articles in one department and two merchandise categories from another department.
Establish characteristics that cross merchandise categories. For example, report on (or mass maintain) all merchandise with the “lamb & rice” flavor.
Allow merchandise categories to be regrouped into new hierarchies as the business and its requirements evolve. Carry the history for the previous hierarchy into the new hierarchy.
Maintain a personnel hierarchy that is independent of the merchandise hierarchy, but can be linked to it. For example, attach an inventory manager to all the merchandise categories in one class and also to two merchandise hierarchies in a second class. As part of this associate’s performance evaluation, report on the sales history and removal rate for each of the inventory manager’s articles.
Issues
Can we include / exclude DCs and mixing centers from reports on the hierarchy? For example: Report on all the sites in a region (but not the DCs). Resolution: Yes, reports can filter data at the hierarchy level and the site attribute level
Can you create “personal clusters” that only you yourself can see? Resolution: No, clusters are global--a similar effect can be had using personal report filters. Related: grouping stores in cluster groups is a powerful tool, but there needs to be some sort of access limitation / cluster creation and modification methodology.
Are assortment modules and clusters tied together? So, can we create a flea & tick cluster and tie the flea & tick module to those stores? Resolution: No, store clusters and assortment management operate independently.
VP issue: Are we going to maintain the existing linear site hierarchy or develop a new linear site hierarchy? If we do change the hierarchy, why and how? (see the Addendum for additional detail). Possible changes:
Where sub-market coordinators are currently reporting directly to the regional VP, turn those sub-markets into markets
Redefine the hierarchy by pricing zone / advertising zone
Simplify the formal site hierarchy into Company-site.
VP issue: Are we going to maintain the existing merchandise hierarchy or define a new one? Resolution: We are re-aligning the merchandise hierarchy using a category-driven methodology. (01/05/98)
How many levels of site hierarchy and merchandise hierarchy are available? Is there a limit to the number you can drill down into? Resolution: There are many hierarchy levels available for sites and merchandise, but performance is a consideration. Per Test Month, we can drill down into three levels per information structure. To go above / below those three, the information structure would need to be reset. Changing the information structure is not difficult (01/12/98)
Characteristic profiles allow you to assign a group of characteristics to an article in a merchandise category in addition to the characteristics the article adopts from the merchandise category. Can you change a characteristic profile (add or remove characteristics, for instance) after it has been assigned to a merchandise category? (01/12/98)
Can you report on characteristics across merchandise category levels? For example, can you report on all "lamb & rice" flavors for all articles in the company? If this is possible, is it necessary to create the flavor characteristic above the merchandise category level (at the company or division level)? (01/12/98)
How will we tie a personnel hierarchy (VP - buyer, for example) to the merchandise and site hierarchies? What are the personnel hierarchies required for performance analysis? What information is required in the performance analysis of each position? (01/12/98)
Can we address issue #9 using "partners" to assign people responsible for a site (regional managers, VPs, market coordinators). What is the maintenance impact of using this route when there are personnel changes? For example, a regional manager moves laterally to another region: do all the stores in the two regions need to be manually updated? (01/12/98)
What is the performance impact of using a large number of characteristics in reports and for mass maintenance? (01/12/98)
Reports
Retained Reports
Department-Class List (This is an existing report on the merchandise hierarchy, but its structure will change depending on the merchandise hierarchy used in the target system)
Existing SAP functionality
Site Hierarchies
Sites can be grouped together for a number of functions. One site can be assigned to several groups. It is used as a method of ensuring that data is maintained for all the individual objects assigned to it (for example, in making mass article changes).

Grouping sites together has the following advantages:
It simplifies the maintenance process
It allows best possible use of store characteristics

Site groups are used mainly in the following functions:
Stock allocation
Promotion management
Listing procedure
Supply source determination
Mass article maintenance
Information system

Changing Site Hierarchies
In the future, there may be a point where the site hierarchy would change--a new region would be created or a market might be split into two markets. In order for SAP to apply the past transaction histories to the new hierarchy, a data conversion process must be completed.

Merchandise Hierarchies
This business process allows you to define merchandise categories and merchandise category hierarchy levels and create a merchandise category hierarchy. Each merchandise category can also be assigned descriptive characteristics or characteristics profiles.

Grouping articles together to form merchandise categories or merchandise category hierarchy levels makes it easier to monitor and control an organization.
Merchandise categories can provide assistance in creating articles: a merchandise category reference article can be created to offer standard values for articles in that merchandise category.
The merchandise category hierarchy enables characteristics to be inherited by lower levels from superior levels.
As a further aid to listing new articles or creating generic articles and variants, characteristics profiles exist that allow a "technical" segmentation of merchandise categories below the merchandise category level

Steps in the Process:
You create the new merchandise category hierarchy levels you need by maintaining/assigning basic data, catchwords (optional) and characteristics (optional) for the merchandise category hierarchy level in question.
You create the characteristics profiles you need by maintaining/assigning basic data, catchwords (optional) and characteristics (optional) for the characteristics profile in question.
You create the merchandise categories you need by maintaining the basic data of the merchandise category and that of a merchandise category article (if this setting has been made in Customizing) and by maintaining/assigning catchwords (optional) and characteristics (optional) for the merchandise category.
If necessary, you can maintain data for the merchandise category article and create a merchandise category reference article (if this setting has been made in Customizing); this takes place in Article Processing .
You assign merchandise category hierarchy levels (top-down assignment).
You assign a merchandise category directly to a merchandise category hierarchy level. You select the hierarchy articles you need and change the data in these articles in Article Processing, if desired.
You assign the characteristics profiles you need to the merchandise category.

Merchandise category hierarchy level
Further hierarchy levels (merchandise groupings) can be created above the merchandise category level. Every merchandise category hierarchy level is assigned to precisely one superior hierarchy level. There is, therefore, always an x:1 relationship between lower hierarchy levels and the level above.

Merchandise category hierarchy levels allow you to process sales at levels above the merchandise category level, if required. At merchandise category hierarchy level too, target and actual values can be planned and evaluations can be made in the Information System.

Merchandise category hierarchy
The complete merchandise category hierarchy is made up of all the assignments or relationships between the individual merchandise category levels and comprises the full spectrum of inter-dependencies and validation checks.

Characteristics profile
Below the level of the merchandise category (and therefore below the whole merchandise category hierarchy) it is possible to create characteristics profiles, a finer subdivision of the merchandise category. They generally serve to differentiate the parameters (required fields, variant-creating characteristics etc.) set when new generic articles/variants or single articles are created.

A number of characteristics profiles can be created per merchandise category. Each article must be assigned to precisely one merchandise category and can also be assigned to a characteristics profile.

If a characteristics profile exists, it takes precedence over the more general structure of the merchandise category when an article (or generic article) is created.

The relationship between characteristics profile and merchandise category is x:1.
Addendum
Current PETsMART Site Hierarchy


Rationale behind the current site hierarchy
Sales reporting
Geographic feasibility / control
Regional Vice President - responsible for about 70 stores
Market Manager - responsible for about 15 stores
Market Coordinator - responsible for about 6 stores
Compensation structures

Proposed PETsMART Site Hierarchy










In the proposed site hierarchy, mass maintenance and reporting on sites would, for the most part, not take place through the formal site hierarchy. Instead, informal site groups and characteristics would be utilized to these ends. The table below contains a short list of probable site groups / characteristics, but the definite list is yet to be determined

The following store operations positions need to be linked into the informal site hierarchy using groups and/or characteristics:  Regional VPs, Market Coordinator, Market Manager, Regional HR, Regional Grooming, Regional Services, Regional Loss Prevention, Regional Sales. The links (which position is responsible for which groups / characteristics) are still to be determined.

Site Characteristics / Groups Identified

Characteristic / GroupValuesVeterinary ServiceTrue / FalseFlea & TickTrue / FalseLive FishTrue / FalseTrue / FalseLive Small AnimalsTrue / FalseLive ReptilesTrue / FalseLive PlantsTrue / FalseEquineTrue / FalseDiscovery CenterTrue / FalseGroomingTrue / FalsePetCo, WalMart, Sam’s Club, etc.RegionSouthwest, West Coast, Southeast, etc.MarketS. Chicago, Missouri, Arizona, etc.Sub MarketPhoenix, Las Vegas, Albuquerque, etc.ClimateCold, Hot, Mild, etc.Consumable PreferenceGrocery, Premium
Proposed Merchandise Hierarchy


























In the proposed merchandise hierarchy, mass maintenance and reporting on articles will take place through a combination of the formal site hierarchy and through informal site groups and characteristics. The table below contains a short list of probable article groups / characteristics, but the definite list is yet to be determined.

The following merchandising positions must be linked into the formal merchandise hierarchy at various levels:  Merchandising VP, Buyer, Merchandise Manager, Inventory Manager, Pricing Analyst. The links (which position is responsible for which levels and groups / characteristics) are still to be determined.

Article Characteristics Identified

CharacteristicValuesLife StageYouth, Adult, Performance, ElderlyImportTrue / FalseCorporate BrandTrue / FalseCustomerDog, Cat, Fish, Hamster, etc.RatingGood, Better, Best

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
