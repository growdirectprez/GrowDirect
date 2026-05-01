Cindy and Frank are on a temporary work assignment in the UK; they are getting married and have decided to register with the T&K bridal registry.  They visit the store nearest them to begin the process and select the products they would like on their registry.    While in the store they learn that the T&K gift registry has recently become available on-line so that friends and family can shop on line and have gifts sent directly to them.N/A HYPERLINK "http://www.macys.com" www.macys.com
 HYPERLINK "http://www.crateandbarrel.com" www.crateandbarrel.com


The BV shopping list contains some functionality to create a shopping / wish list, not registry functionality
Custom development to create gift registry functionality
Cindy’s uncle Bob hears about his niece’s upcoming marriage decides to make a purchase from their registry off the T&K website.  He is a new customer who enters the website for the first time.  He is presented with The T&K.com splash page where he has several options.  

Register as a new user and create a profile
Are you a T&K Store value cardholder? 
Enter the website through one of our regional homepages

Bob is in a hurry to shop, is looking for a specific product from the registry and is not concerned about providing personal information.  He clicks on the North America icon and in so doing indicates that he will be shopping is US dollars and viewing text in English.1.1
Splash pagegreeting message 
general description of T&K and its products 
graphics for dollar and pound to identify language/geography preference 
entry box for value card number
link to member join page 
T&K graphic logo to be repeated on every page 
pictures of products or store images
entry boxes for user id and password
select country shopping from HYPERLINK "http://www.ual.com" www.ual.com
 HYPERLINK "http://www.compaq.com" www.compaq.com

Multi language not demonstrated here, but at this point we could have discussion about how much international functionality the demo should have, and the effort required to maintain multiple versions of the text, etc.   At a minimum we could use a multi currency example

Could use example of e-mail targeting to contact people on registered users’ address book

Additional set-up of product tables to support multiple languages and currencies
Bob is directed to the North American home page where the standard ads and promotional offers are displayed for an unregistered customer.  He proceeds to the registry area of the website by clicking the horizontal “registry” tab.
1.2
U.S. Regional HomepageHorizontal navigation tabs on all pages other than splashshopping cart 
my account 
corporate info/contact us 
search 
join us (employment) 
registry and wish list
order status HYPERLINK "http://www.crateandbarrel.com" www.crateandbarrel.com

Rule based matching for unregistered user

BroadVision search functionality


Vertical navigation menu on all pages other than splash
service 
"never run out" automatic replenishment 
check my store's inventory 
view in-store specials 
gift ideas 
apply for T&K credit card 
store locator 
specialty shop 
Martha Stewart 
Calvin Klein 
Hewlett-Packard 
Wine club 
product categories 
Apparel 
Accessories 
Food and wine 
Housewares 
Home office 
Electronics 



Search box on every page -- keyword and/or natural language
Drop down box to select category of merchandise or site-wide search 
Entry box for keyword or sentence 
Ads in right hand space to be randomly assigned position
AD1 – merchant shop for CK 
AD2 – best 5 selling items (data mining example) 
AD3 – deal of the day 
Incentive
IN1 – BOGO in belts
Featured products in merchandising area
FP1 Food and wine – bottle of wine images and text 
FP2 Apparel and accessories -- 20% off women's sweaters 
FP3 Housewares -- new Martha Stewart stoneware 
FP4 Electronics -- Palm V 
Banner advertisement
BA1 -- T&K branded Visa card signup 
Logo
T&K logo 
"home" link 
Text hyperlinks that mirror navigation tabs
hyperlinks 
advertisement for BetterWeb 
Bob searches for Cindy and Frank by name and date.1.3
Registry searchBanner adBA13 – Check out our gift picks HYPERLINK http://www.landsend.om www.landsend.com
 HYPERLINK http://www.ford.com www.ford.com



Buttons
Purchase a gift from someone’s registry
View or modify your registry (with entry boxes for user id and password)



Editorial
ED1:  View instructions for registering
User inputs on form
FM6:  Find-a-registry search form
First name
Last name
Event
Month and year drop down boxes
He finds and displays their registry in order to select a gift.
1.4  Registry search results
Forms on page
FM14:  List of possible matches, each one hyperlinked to registry details page



Banner
BA13:  Check our gift picks
Forms on the page
FM6:  Find-a-registry search form
Bob decides to purchase a set of the china for which Cindy has registered.  He finds an ideal match and adds it to his shopping basket.

Unfortunately, when he decides to add a flatware selection to his order, he sees that the product is out of stock on the site at the moment.  T&K.com offers Bob several choices in order to complete the sale:

The product is on backorder and will be delivered when it becomes available
He can provide his postal/zip code and T&K will check to see if the place setting is available in inventory at a local store

He provides Frank and Cindy’s postal code (in the UK) and finds that the item is available for pickup at their local store.  He places the item in the shopping basket.
1.5
Reigstry product list page
Forms on the page
FM7:  Registry details product list
Item description
Number requested
Number still needed
Price
Check boxes to select products to purchase
Inventory position on the site and in the closest store
Each item hyperlinked to product detail page
Ability to sort based on price or number needed
Closest store should be hyperlinked to show name and location of store and allow for new zip code to be entered (maybe separate page?)

Use of extended product attributes to indicate gift wrapping
Integration with back office systems to support local store inventory
Buttons
Continue shopping
Proceed to checkout
Clear selections
Applet
AP1:  Shopping assistant for registry purchases, local inventory via postal/zip code entry, gift messages and gift cards
Message
MS3:  Frank and Cindy’s wedding announcement (registry/date, etc.)
He selects the checkout button to begin the checkout process.

Realizing that the purchase is off the registry, the site automatically selects gift wrap for all items, and a T&K shopping assistant pops up to ask Bob if he would like to send a personalized message to the Bride and Groom.

1.6
Shopping cartButtonsContinue shopping
Checkout button
Update shopping cart HYPERLINK "http://www.circuitcity.com" www.circuitcity.com
 HYPERLINK "http://www.compusa.com" www.compusa.com
Online inventory check of standard BV product tables
Possible link to external database for real time inventory check
Banner ad
BA5: We’re certified by Better Web so you can rest assured that your information is confidential and secure



Shopping cart info
Leverage Broadvision functionality
Applet
AP1:  Shopping assistant for registry purchases, local inventory via postal/zip code entry, gift messages and gift cards
Using the microphone attached to his PC, Bob records a personalized message sending his best wishes to the new couple.  The message is attached to an e-mail to be sent to Bob and Cindy.  Bob also chooses to send a personalized card and write his message in the space provided.

The assistant also asks Bob if he would like to be reminded in regular intervals of the occasion for which he gave the gift.  He chooses annual reminders to be sent to his email address on the 15th of the month and calls it “Frank and Cindy’s Anniversary”.1.7
Shopping AssistantT&K assistantAP1: Shopping assistant for registry purchases, gift messages and gift cards HYPERLINK "http://www.bluemountain.com" www.bluemountain.com

Email targeting and simple message delivery for sending the card
Custom work to develop gift cards, and recorded wav / mp3 file
Forms on the page
FM8:  Gift card/personalized message
Input box for gift message
Button for voice recording



Buttons
Continue shopping
Checkout
Voice recording button
New window within applet
Assistant tells user to press record button in the window and press stop when finished speaking
Allows user to replay message
Finalize order
Gift reminder
Check box for reminder service, entry box for desired reminder date, and drop-down for frequency (annual, monthly, etc)
Banner ad
BA17:  Shopping assistant banner ad
In order to complete the purchase, Bob must provide his name, billing address, e-mail address, and payment information.
1.8
CheckoutForms on the pageFM2: customer name, billing information and address  from “My Account” page HYPERLINK "http://www.circuitcity.com" www.circuitcity.com
Standard Shopping cart / Sales rep functionality 
Display integration with tax and credit software
FM4:  payment information



FM15: order shipping address(es)
Buttons
Confirm order
Adjust/change order
Shop more
Banner ad
BA1:  T&K branded Visa card
Field verification
Make sure that required information is entered properly and is not missing
If missing, return user and highlight fields in red to fix/fill out
After the sales transaction is complete, Frank and Cindy’s registry is updated to reflect the sale
N/A HYPERLINK "http://www.crateandbarrel.com" www.crateandbarrel.com


Custom development to display an update of registry information
Bob is sent a confirmation e-mail and url to track the status of his order online.
N/A HYPERLINK "http://www.onsale.com" www.onsale.com

BV e-mail and purchase history functionality









Customer Storyboard	Slide	 Slide Elements 	Example Website 	BroadVision Features 	Custom / Enhancement



	Scenario 1: Uncle Bob	Page  PAGE 5 of  NUMPAGES 5







