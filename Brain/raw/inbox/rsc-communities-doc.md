---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/RSC Communities.doc.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# RSC Communities.doc

## Source
File: `Brain/raw/.extract/SWINDON/RSC Communities.doc.md`
Size: 15,922 bytes

## Raw content


T & K E-Channel CRM Project
BroadVision Community Definition and Rules Based Matching

Document Control
Revision History

Author
Version
Date
Description of Change
Geoff Lyle
1.0
February 1, 2000
First release
Geoff Lyle
1.1
February 14, 2000
Addition of Rulesets, rules and content
Distribution
Name
Location
Roger Haddon
T&K
Ros Rosewarne-Jenkins
T&K
Amar Shabbir
T&K
Simon Morgan
T&K
Iain Williamson
T&K
Bob Sherlock
T&K
BroadVision User Profile Definition and Enhancements
In order to define customer segments known as “communities” within BroadVision, we must build a profile creation / maintenance application for the T&K website.  The customer profile will be based primarily on the delivered BV_USER_PROFILE table for standard demographic attributes. However, in order to identify customer preferences that will drive of personalization of the web site we are required to modify the delivered table and to add list tables that support our needs.

The customer record can be broken down into three sections:
Basic User Account - This will include a unique customer ID, password, e-mail address, and T&K loyalty card account number.
Transactional data - Required data needed to support completion of a sales order.  (Billing address, shipping address, and payment information)
Personalized data – Combination of demographic and psychographic attributes combined to define the customer segments that will drive personalization of the website.
Basic User Account

The T&K profile questionnaire will ask the following “basic” questions:
Please provide your First and Last Name
Please provide your e-mail address
Please select a unique User Id
Please create a password and confirm your password
Are you member of the loyalty card program, and if so please provide your card number

At this point we have enough information to create a simple user account and begin observational tracking of the user.  We can base some basic matching at this point, and treat the customer as member of some default community until they provide us with either meaningful observations, purchasing history, or decide to offer us personal content by way of filling out the customer profile questionnaire.

Transactional Data
T&K will be able to obtain transactional data from the customer in three ways.
The customer will make a purchase from the website, and in so doing will be required to provide us with billing and address information as a criteria for completing the sales transaction.
The customer is already a member of the Loyalty card program, and we identify the customer as such.  We will have some name and address information as well as purchasing history from other channels.
The customer will tell us their address when they fill out their profile information.
Personalized Data
Customers will be prompted to fill out a customer profile that will tell us some of the family details, demographics and personal shopping preferences.  We will ask the following questions:
Address (if known it will be populated automatically)
Gender
Age Range
Number of adults in household
Number of children in Household
Food Brand Preference (Do you like brands or Generics)
Fashion Brand Preference (Do you like brands or Generics)
Price Preference (Do like Coupons / Sales or Every Day Low Price)
Functional preference (Functional vs. Luxury)
Preferred merchandise categories
Contact method (e-mail, direct mail)
In addition, to display taxonomy matching using the BroadVision matching engine we will ask customer who indicate a preference for the entertainment category of merchandise to fill out some additional questions regarding their movie preferences.  Customer will be asked to rate how they feel about certain types of movies (action, mystery / suspense, classics, comedies, romantic comedies), and whether or not they purchase children’s videos.

RSC E-channel Customer “Community” Definitions:

The information gathered from the customer profile will be used to segment customers.  Four BroadVision Communities will be defined using a combination of demographic and psychographic attributes from the table BV_USER_PROFILE and an associated list table to be created.  The Four communities are defined as follows:
Bargain Hunters:
Prefer sales and coupons
Buy Branded goods when on sale, generics otherwise
Rarely buy luxury items
All families in middle and down markets
Impulse Buyers:
Buy on an Every Day Fair Price basis, rarely use coupons
Prefer brands over generics
Tend to splurge on luxury items in each category
Young couples and singles in middle and up markets
Time Starved:
Will use coupons as available, less than average
Prefer brands, never buy generics
Purchase basic goods, rarely splurge
Families and households in middle and up markets
Budget Conscious:
Use coupons and buy sales items with average frequency
Mostly purchase generics
Purchase basic goods, rarely splurge
Younger parents in middle and down markets and older households in all markets

Demographic Community Attributes:

Demographic elements are obtained from the table BV_USER_PROFILE, and will require no modifications to the table as delivered.
FIELD
TABLE
DESCRIPTION
VALUES
GENDER
BV_USER_PROFILE
User gender
Male, Female
AGE_RANGE
BV_USER_PROFILE
User age range
18 to 25, 25 to 34, 35 to 44,  45 to 54, 55 to 64, 65+
NO_HOUSEHOLD
BV_USER_PROFILE
Number of People in Household.  Will be used to store the number of adults in the household
- Integer Value
Psychographic / Behavioural Community Attributes:
Enhancements to the user profile delivered by BroadVision will be in two forms.  We will extend the current definition of BV_USER_PROFILE to include new attributes at the user level.  Additionally we will add a list table to store pyschographic and taxonomy attributes at the user / category level.  This will allow a customer to express different preferences for the same attribute across categories, allowing a customer to switch community membership dynamically; based on the category of merchandise they are shopping.  We can then allow a customer to indicate brand preference across categories where a customer may have opposite preferences between two categories. For example, a customer may be very brand sensitive in clothing departments, shopping only for designer merchandise, but be indifferent to brand when shopping for food items.  For demonstration purposes category specific attributes will be stored at the four top-level merchandise categories initially. (Entertainment, Home Wares, Fashion, Food & Drink). It should also be stated that stating of direct questions about preferences might not be a preferred method for obtaining this type of data.  Intuitive mining of the purchasing history and observational data should be investigated as a means for determining the values of many customer specific attributes.  From the profile outline above, income range and brand preference, Functional preference would be excellent candidates for attributes to be mined from monitoring customer behaviour.  However, in the future, the profile maintenance screen could be modified to allow storage of attributes at any category within the BroadVision merchandise hierarchy.  This would not require modification of the database. The new table definitions are outlined below.
BV_USER_PROFILE - Extensions
FIELD
TABLE
DESCRIPTION
VALUES
NO_CHILD_HSHLD
BV_USER_PROFILE
Number of People in Household.  Will be used to store the number of adults in the household
- Integer Value
PRICE_PREF
BV_USER_PROFILE
User price preference.  True = I prefer coupons
False = I prefer EDLP
(T/F)

LIST_USER_PREF
FIELD
TABLE
DESCRIPTION
VALUES
USER_ID
BV_ USER_TK_PREF
User id from BV_USER_PROFILE
Valid user ID’s from BV_USER_PROFILE
CAT_OID
BV_ USER_TK_PREF
Category ID from BV_CATEGORY
Valid category OID’s from BV_CATEGORY
BRAND_PREF
BV_ USER_TK_PREF
User Brand preference:
True = I like brands
False = I like generics
(T/F)
FUNCTION_PREF
BV_ USER_TK_PREF
Taxonomy value for general functional purpose of the item (i.e., is it a luxury good, or is it more basic / functional)
Customer selects a value of 1 to 5 to indicate the functionality of goods they prefer (i.e.: 1 meaning customer prefers functional items high quality at a good value vs. 5 meaning customer prefers luxury goods
ACTION
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
SUSPENSE
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
COMEDY
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
ROMANCE
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
CLASSIC
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
CHILDREN
BV_ USER_TK_PREF
T/F value initially used in video to indicate a preference for purchasing children’s items.  Can be used in any category if the profile and questions are set-up online to support the attribute in other categories
(T/F)


Community Definition: The BroadVision Criteria Statement

In order to define the communities listed above in BroadVision, the descriptions of the customer preferences must be represented as a database query that will produce a sub-set of the customers stored in the BV_USER_PROFILE table.

Bargain Hunters:
GENDER (N/A)
AGE_RANGE (NA)
NO_HOUSEHOLD >=1
NO_CHILD_HSHLD >=1
PRICE_PREF = T
FUNCTION_PREF <=3
BRAND_PREF = F

Impulse Buyers:
GENDER (N/A)
AGE_RANGE <=35
NO_HOUSEHOLD <=2
NO_CHILD_HSHLD <1
PRICE_PREF = F
FUNCTION_PREF >=4
BRAND_PREF = T
Time Starved:
GENDER (N/A)
AGE_RANGE (NA)
INCOME_RANGE >=30,000
NO_HOUSEHOLD >=1
NO_CHILD_HSHLD >=1
PRICE_PREF = T
FUNCTION_PREF <=3
BRAND_PREF = F
Budget Conscious:
GENDER (N/A)
AGE_RANGE (N/A)
NO_HOUSEHOLD >=1
NO_CHILD_HSHLD (
PRICE_PREF = T
FUNCTION_PREF <=2
BRAND_PREF = F

Content Table Modifications
In order to support the matching process within BroadVision, content tables will also need to be modified to support custom attributes.  For the T&K website, we will add a list table to the Product data model, and extend the advertisement table to support two additional attributes.
BV_PRODUCT_TK
FIELD
TABLE
DESCRIPTION
VALUES
BRAND
BV_ PRODUCT_TK
True = Brand
False = Generic / NA
(T/F)
FUNCTION_PREF
BV_ USER_TK_PREF
Taxonomy value for general functional purpose of the item (i.e., is it a luxury good, or is it more basic / functional)
Each product using this value must be ranked 1 to 5 inorder to indicate the function of the good.
ACTION
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
SUSPENSE
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
COMEDY
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
ROMANCE
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.
CLASSIC
BV_ USER_TK_PREF
Taxonomy value
Customer choices range from strongly disagree to strongly agree, and are translated to a value from `1 to 5 in the DB.

BV_ADVERTSIEMENT – Extensions
FIELD
TABLE
DESCRIPTION
VALUES
BRAND
BV_ PRODUCT_TK
True = Brand
False = Generic / NA
(T/F) Is this a branded ad?
MARKET
BV_ USER_TK_PREF
STRING value to indicate the market (audience) for the ad.
Up Market
Middle Market
Down Market
BroadVision Rule Sets
BroadVision rule sets are used to define groups of rules that will be used in specific JavaScript page scripts to be developed by the RSC team.  JavaScript code is used to develop dynamic pages that will display personalized information based on the community of the visitor to the site.  As a result of the planning and analysis phase of the RSC E-channel project we have identified 13 distinct instances where BroadVision rule sets will be called by to display personalized information on various pages within the T&K web site.  Those instances are detailed in the following list.  Section 5 will discuss the actual rules to be used and the content being developed that will be displayed as a result of the matching process.

Home Page rule sets
homepage_ad1
homepage_ad2
homepage_inc
homepage_ed




Category and Sub-category Page rule sets
category_ad1
category_ad2







Product Detail Page rule sets
product_ad1
product_ad2








Cooking Club rule sets
cookclub_ad1
cookclub_ad2







Loyalty Card Review Page rule sets
loyalty_ad1
loyalty_ad2
loyalty_ed






Rules and Content
Using the rule sets defined above, we will create rules for each community (Impulse Buyers “IB”, Bargain Hunters “BH”, Time Starved Professionals “TS”, Budget Conscious “BC”) and a default rule initially.  The rules listed here are for planning purposes, the dynamic nature of BroadVision allows these rules to be modified at any time in response to changing business conditions or marketing iniatives.
Home Page Rules
Rule set: homepage_ad1 – Ad space 1 on the homepage (upper right)
Content Type: Advertisement
Community
Rule
Content
Bargain Hunters
Select specific item from advertisements
Levis on-sale
Impulse Buyers
Select specific item from advertisements
High end Branded ad
Time Starved
Select specific item from advertisements
Create a shopping list ad
Budget Conscious
Select specific item from advertisements
T&K brand ad
Default
Select specific item from advertisements
Loyalty card program registration

Rule set: homepage_ad2 – Ad space 2 on the homepage (middle right)
Content Type: Product
Community
Rule
Content
Bargain Hunters
Select weekly special product from preferred category
product.gif with link
Impulse Buyers
Select Product from luxury
product.gif with link
Time Starved

product.gif with link
Budget Conscious
Select weekly special product from preferred category
product.gif with link
Default
Select any product from weekly specials
product.gif with link

Rule set: homepage_inc – Incentive space on the homepage (lowerright)
Content Type: Incentive
Community
Rule
Content
Unregistered
Id user has no profile information
Display registration incentive
Bargain Hunters


Impulse Buyers


Time Starved


Budget Conscious


Default




Rule set: homepage_ed – Editorial space on the homepage (middle)
Content Type: Incentive
Community
Rule
Content
Bargain Hunters
Select specific editorial
BH Editorial
Impulse Buyers
Select specific editorial
IB Editorial
Time Starved
Select specific editorial
TS Editorial
Budget Conscious
Select specific editorial
DM Editorial
Default
Select specific editorial
Default Editorial

Category / Sub-category Rule Sets
Rule set: category_ad1 – Ad space on categrory and sub-category pages (upper right)
Content Type: Product
Community
Rule
Content
Bargain Hunters
Select product appropriate the community
Product.gif and desc.
Impulse Buyers
Select product appropriate the community
Product.gif and desc.
Time Starved
Select product appropriate the community
Product.gif and desc.
Budget Conscious
Select product appropriate the community
Product.gif and desc.
Default
Random pick from X category
Product.gif and desc.

Organisation: T & K
System:	 E-Channel CRM
Methodology: AscendantDate:		1-Feb-00
Sub-system:	BroadVisionPage  PAGE  \* MERGEFORMAT 1 of  NUMPAGES  \* MERGEFORMAT 12

Title
Community Definition and Rules Based Matching
Version No:	1.0

































## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
