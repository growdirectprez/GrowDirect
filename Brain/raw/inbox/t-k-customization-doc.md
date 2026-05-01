---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/T&K customization.doc.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# T&K customization.doc

## Source
File: `Brain/raw/.extract/SWINDON/T&K customization.doc.md`
Size: 7,889 bytes

## Raw content
Customizing the Command Center

The following document outlines the process of customizing  “T&K Online” , the BroadVision Retail Demo, for client presentations.  It assumes that no functionality will be added to or modified in the demo.   Therefore, the only changes necessary for customizing the demo can be made through the Command Center.
This document goes step-by-step through the Command Center, identifying all necessary changes and giving brief instructions on how to make them.  It is organized according to the overall Command Center design, and areas that must be changed are identified by pathname (e.g. Advertisements/Homepage advertisements/ lower_right.)
Currently, T&K Online is customized for a Swatch demo.  This document assumes that in customizing the demo for a new client presentation, T&K site communities will stay the same, and that only content and rules which are Swatch-specific will be taken off-line.

Content

Products:
Keep existing products in the Command Center
Add new categories, sub-categories, and products for Client offering.

**See “How to Load New Products” attachment for instructions on bulk loading Client products into the Command Center.


Advertisements:

Create new images for client-specific advertisements and store them in the T&K “ads” folder (/tk/images/ads/)
Advertisements/Homepage advertisements/logo—Take the following ad off-line:
Swatch Logo
Advertisements/Homepage advertisements/ lower_right—Take the following ads off-line:
Skin Collection
Irony/Scuba 200
Spring/Summer 2000 Collection
Beatstore collection
Add client-specific advertisements to the folders from Step 2 & 3.
New advertisements can be created entirely in the Command Center, following the format of existing ads.  New advertisements need the following information: (viewed when you double-click the advertisement)
In Basics tab: a Title, an On-line status (which should be “On-line”)
In Related Files tab: an Image File (which should be the pathname to the ad image, i.e. /tk/images/ads/adname, with extension)
*** Note:  The advertisements currently in  the “lower_right” folder are ads for sub-categories of “Watches” (e.g. Skin Collection).  When a site user clicks on these ads, they are taken to the “Show Products” page, which displays products from that sub-category (e.g. watches from the Skin Collection).  If one wants to replace them with similar ads, one must add an External URL in the Related Files tab.  This will be “show_products.jsp?oid=xxxx&”, where xxxx is the oid of the advertisement’s sub-category (e.g.  8055 for the Skin Collection.)


Editorials:

Create or collect text for client-specific editorials.
Create new images for client-specific editorials and store them in the T&K “editorials” folder (/tk/images/editorials/)
Editorials/Homepage Ed1 Editorials—Take the  “Swatch Collectors” editorial off-line
Add client-specific editorials to this folder
Editorials can be created entirely in the Command Center.  They need the following information :
In Basics tab:  a Title, an On-line status (which should be “On-line”)
In the Details tab:  a Type (chosen from a drop-down menu., in this case “Weekly Column”,  a Text Form (in this case “DB Column”), & Editorial Text appropriate to the client (created in Step 1)
If an image is to be associated with the Client editorial--- In the Related Files tab: a Full Image File (which should be the pathname to the editorial image, i.e. /tk/images/editorials/editorialname, with extension)

Editorials/ Homepage Swatch Editorials—Take the following editorials off-line:
Access Technology
Vienna- LIFE BALL 1999
Skin Technology
Boarder X history
Swatch Wave Tour
Internet Time
Swatch Talk
Add editorials specific to the client.  – Repeat step 5, with the following modification:  Details-Type should be “Welcome Note”

Incentives:
Create new images for client-specific incentives and store them in the T&K “incentives” folder (/tk/images/incentives/)
Incentives/Registration Confirmation—Take Swatch coupons off-line
Add coupons appropriate to client.  (Perhaps $10 off whatever department the client products are in.)
Coupons can be created entirely in the Command Center using the Wizard.  One must enter Incentive Type, Sale Dates, Distribution Dates, Max. Distribution Count, and Pricing Terms.
If coupons are to be displayed on-line, the path to the image files created in Step 1 should be added to the “Image File”  attribute (/tk/images/incentives/incentivename, with extension)
Incentives/Shopping Cart Incentives—Repeat steps 2-5

Discussion Groups:
Currently, Discussion Groups aren’t functional on the T&K web site.  But if they were functional…
Discussion Groups/ Homepage Discussion Groups—Take the “Swatch Collectors” discussion group off-line. Replace with a discussion group specific to the Client.
New Discussion Groups can be created in the Command Center.  They must include the following information:
In the Basics tab- a Title, an On-line status (which should be “On-line”)
In the Details tab- Moderation Type (chosen from a drop-down menu, for T&K the type is “Post-Moderate”)
Site users should then enter messages for the client-specific Discussion Groups via the web site.
It may also be possible for developers to create new messages in the Command Center.  See “Discussion Group Messages.”

Discussion Group Messages:
Discussion Group Messages/Swatch Collectors—take Message ID 2 off-line
Create new Discussion Group Messages in the Command Center using the Wizard.  New messages will need the following information:
In the Basics tab: a Message ID (should be a unique, sequential value, assigned in order of creation), an On-line status (“On-line’), a Message Title (which should be Re: Previous Message Title if it’s a response)
In the Details tab:  a Message Parent ID (the original Message ID, i.e. the thread ID),  Message Content (the message text itself), Author Name, Email Address (of Author)


Matching

***Assuming that T&K communities will stay the same and that rules only need to be modified if they display Swatch-specific content, follow these steps:

Rules:
Rules/Category/category_pd1—Modify “Impulse Buyers pd1”  rule.  Should retrieve a client product , rather than  a Swatch BeatStore product,  if the user is an Impulse Buyer
Rules/Homepage/homepage_ad1- Replace “Swatch Logo” with a rule to show the client logo, rather than the Swatch logo on the T&K homepage.
Rules/Homepage/homepage_ad4—Modify all rules: “Bargain Hunter Ad3”, “Time Starved Professional Ad3” and “Impulse Buyer Ad3” to show client-specific ads, rather than Swatch ads on the homepage.
Rules/Homepage/homepage_dg1—Replace “Swatch Collectors” rule with a rule to display a client-specific discussion group???
Rules/Homepage/homepage_ed1—Modify “Impulse Buyer Ed1” to show a client editorial, rather than a Swatch editorial if the user is an Impulse Buyer.
Rules/Homepage/homepage_ed2—Modify “Bargain Hunter Ed2” and “Time Starved Professional Ed2” to  show client-specific editorials
Rules/Homepage/homepage_in1—Replace “10% off every watch in Accessories” with a rule to retrieve a client-specific incentive
Rules/Homepage/homepage_pd1—modify “Impulse Buyer Pd1” to show a client-specific product, rather than a BeatStore watch to Impulse Buyers
Rules/Shopping Cart/ shopcart_in1—Modify Rule Set to pull up client-specific incentives
Rules/Shopping Cart/shopcart_in2-- Modify Rule Set to pull up client-specific incentives
Rules/Shopping Cart/shopcart_in3- Modify Rule Set to pull up client-specific incentives
***Note:  Rule Sets and Rules can be modified directly in the Command Center using the Wizard.  Follow the example of Rule Sets and Rules currently in the Command Center.

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
