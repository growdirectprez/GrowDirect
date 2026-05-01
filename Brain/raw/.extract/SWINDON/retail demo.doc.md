BroadVision Retail Template

T&K Online, the BroadVision retail template, is intended to demonstrate key aspects of vanilla BroadVision functionality.  The following document lays out the BroadVision features that currently exist in T&K Online, along with next steps for further development.  

Fully Developed
Logon  (username and password)
New user Registration
User profile containing:
General demographic information
Behavioral / Psychographics information
Preference attributes used for taxonomy matching

Address book (create, update, and delete entries)
Payment methods (create, update, and delete entries) for express checkout
Shopping list functionality- registered users can create and maintain shopping lists and place entire lists into their shopping carts
Shopping cart functionality—both registered and guest users can select products and add them to their shopping carts.  Registered users have a persistent shopping cart that is maintained from session to session.
Product browse from department level through product detail (includes product image, price, and description.)
Registered user check-out 
Address Book (selection or addition)
Payment Method (selection or addition)
Order Confirmation (e-mail confirmation requires use of an SMTP server to deliver the messages, minimal configuration required to complete). 
Order Review / Details
Order History
Customer product review, and matching using Visitor feedback as a metric for selecting products to display ( i.e., display top five reviewed products)
Cross-selling 
One to One marketing—advertisements, editorials, and products—based on pre-defined user communities, order history, user profiles, session behavior, and user-defined product preferences (movie ratings)
Incentives- coupons and storewide sales offered. Users can view coupons available to them, and can add them to or remove coupons from their wallet.  They can also view all T&K storewide sales in the “My Account” section.
Discussion Groups- users can post, view, and respond to messages on particular topics
Parametric search --allows user to search products by specific attributes
Quick search --allows user to search by product name from the homepage

Partially Developed
In-Session tracking—works for product display, but not written out to log files or added to permanent visitor profiles
Guest check-out—works for demo purposes, but will need to be further developed for actual client application
Order confirmation- static link to FedEx needs to be developed—should link to chosen shipping method
Notifications/ date reminders—scripts are written to create and display reminders, need to modify database tables to make this functional for e-mail and inbox notification
Develop choice in shipping method
Develop preferred payment method functionality for check-out
Data validation on all forms

Next Steps

The delivered shopping cart and checkout functionality of the BroadVision 4.0 release leaves much to be desired.  Significant time and effort should be spent to develop a PwC model of a “Best practice” Checkout Procedure using BroadVision as a base.  Functionality should include:
An fully developed solution for un-registered user checkout
Multiple Ship to’s (ship to by line item)
Multiple payment methods on a single order
Gift wrap / comments by line item
Full form field validation including Credit Card Mod 10 checks (check digit)
Shipping and tax calculation including development of interfaces to external applications (i.e., taxware)
Credit authorization and settlement
Secure server processing

Search is another area where significant time could be spent to develop an application using the BroadVision command center as a tool to assign and maintain search attributes across all categories of merchandise
Registry/ Wish list functionality (currently being developed in the UK)
Loyalty program (currently being developed in the UK)
Finish partially developed functionality- above

