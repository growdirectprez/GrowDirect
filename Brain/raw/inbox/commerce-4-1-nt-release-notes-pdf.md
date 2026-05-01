---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Release Notes/Commerce 4.1 NT release notes.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Commerce 4.1 NT release notes.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Release Notes/Commerce 4.1 NT release notes.pdf.md`
Size: 97,626 bytes

## Raw content
1

One-To-One Business Commerce

Version 4.1.0 for Windows NT

Installation and Release Notes

This is Version 4.1.0 of BroadVision® One-To-One Commerce™ for the Windows NT operating
system. These release notes contain information about installing, conﬁguring, and starting
One-To-One Commerce. They also describe known problems and issues, and discuss supplemental
information not included in the documentation.

l “Documentation” on page 2

l “BroadVision Technical Support” on page 3

l “System and software requirements” on page 4

l “Changes since Version 3.0.0” on page 4

l “Problems ﬁxed in this release” on page 5

l “Known problems and issues” on page 6

l “One-To-One Commerce installation” on page 9

l “One-To-One Commerce conﬁguration” on page 11

l “Multiple host machine conﬁguration” on page 21

l “Database upgrade and migration” on page 23

l “Site-speciﬁc customization” on page 25

l “Supplemental information” on page 27

• “Conﬁguring AVP” on page 27

• “Conﬁguring CyberSource” on page 28

• “Conﬁguring the Shipping methods” on page 29

• “Using the Business Express sample data” on page 34

• “Purging contents for deleted visitors” on page 35

l “Commerce for Command Center installation” on page 36

l “Logging in and setting the administrator password” on page 37

l “Logging in as the merchant administrator” on page 39

l “Exiting the One-To-One Command Center” on page 41

l “Removing One-To-One Commerce” on page 41

One-To-One Business Commerce Release Notes

591-410-NAS

BroadVision, Inc.

2

One-To-One Business Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Documentation

Documentation

Because One-To-One Commerce is an application in BroadVision One-To-One Enterprise, all the
documentation for that product is applicable to One-To-One Commerce. The documentation that is
delivered with One-To-One Commerce Version 4.1.0 includes:

l These release notes.

l The One-To-One Commerce Developer’s Guide, which describes the application and how to

customize it.

l The One-To-One Commerce User’s Guide, which describes how to use Commerce for Command

Center.

To use the One-To-One Commerce HTML documentation, on your browser enter the URL that
points to the cwabtoc.htm ﬁle.

l If you are reading the documentation from the CD-ROM specify the letter of your CD-ROM

drive.

For the One-To-One Commerce Developer’s Guide:

file:///E|/PUBS/commerce/b2b/devguide/cwabtoc.htm

For the One-To-One Commerce User’s Guide:

file:///E|/PUBS/commerce/b2b/usrguide/contents.htm

l If you are reading the ﬁles from the directory where the install program places them:

For the One-To-One Commerce Developer’s Guide:

file:/opt/bv1to1/pubs/commerce/b2b/devguide/cwabtoc.htm

For the One-To-One Commerce User’s Guide:

file:/opt/bv1to1/pubs/commerce/b2b/usrguide/contents.htm

The /opt/bv1to1 path corresponds the value of the $BV1TO1 environment variable.

A Portable Document Format (PDF) version of the documentation is available in CWAb.pdf for the
One-To-One Commerce Developer’s Guide, located in the same directory as the HTML ﬁles. To access
the PDF ﬁles, you will need a PDF viewer, such as Adobe's Acrobat Reader, which is available for
free from Adobe's Web site at:

http://www.adobe.com/prodindex/acrobat/readstep.html

Additional BroadVision documents and white papers are available at:

http://www.broadvision.com

From time to time BroadVision updates the electronic documentation and makes it available to
customers. If you are interested in receiving a notification when updates are available, please
send an e-mail message to bvpubs@broadvision, and put "subscribe
commercev410docs" in the subject field. Notifications will be sent to the reply-address of the
message.

BroadVision, Inc.

591-410-NAS

One-To-One Business Commerce Release Notes

One-To-One Business Commerce Version 4.1.0 for Windows NT Installation and Release Notes
BroadVision Technical Support

3

BroadVision Technical Support

Technical Support services are provided on an annual basis to BroadVision© customers. A standard
90-day warranty is also provided with all software.

If you experience problems in using any of BroadVision's software products, contact BroadVision's
World-wide Customer Support Organization for assistance. Registered customers who have a login
name and password can report problems via BroadVision's Web site:

www.broadvision.com.

On the Web site you can access support-related technical information, report problems, and track
report status and responses on the Problem Reports pages. To request a login, please contact your
BroadVision Account Representative.

The Web site is the preferred method of reporting problems; however, if necessary you can report
problems via e-mail to:

bvhelp@broadvision.com

Please be sure to include the case ID when communicating via e-mail.

Information on how to contact Customer Support ofﬁces by telephone can be found on the
BroadVision Web site.

Support for Third-Party Software Products

To allow for complete testing, BroadVision certiﬁes BroadVision One-To-One products against the
versions of third-party products that are released and available sufﬁciently in advance of the
software release date. This often means that third-party vendors release new versions of their
products prior to the next release of the BroadVision software. While BroadVision would prefer that
customers use the tested and certiﬁed software versions, we also understand that customers will
occasionally want or need to use these new versions of third-party products. As long as the vendor
guarantees forward compatibility, One-To-One products should work on these new versions.

BroadVision will usually test and certify these newer versions of third-party products in the next
product release. This can be a good indicator that the newer versions will work with the previous
release. In exceptional cases BroadVision may determine that the newer version of a third-party
product cannot be used because it fails in some way during the testing cycle. In this case we will
continue to certify the older version.

BroadVision will support customers who use newer versions of third-party products by working
with the customer to resolve compatibility problems with the third-party vendor. BroadVision will
also consider, at our option, developing and releasing minor ﬁxes for our products in order to
resolve problems with new versions of third-party products.

One-To-One Business Commerce Release Notes

591-410-NAS

BroadVision, Inc.

4

One-To-One Business Commerce Version 4.1.0 for Windows NT Installation and Release Notes
System and software requirements

System and software requirements

Installing and using One-To-One Commerce requires:

l A server machine that:

• runs BroadVision One-To-One Enterprise Version 4.1.0.

• accesses a CD-ROM drive.

• has 65 MB of available hard disk space.

• runs Netscape Communicator Version 4.6 or Internet Explorer Version 5.0. BroadVision

does not support other versions of these browsers for running the One-To-One Commerce.

• has a VGA monitor with a screen resolution of 800 x 600 or higher.

l The same system and software requirements as BroadVision One-To-One Enterprise. See that

system’s Server Release Notes and Installation and System Administration Guide for details.

If you are using AVP TaxWare, you’ll need version 3.0. If you are using CyberSource for payment
handling, you’ll need CyberSource ICS2 3.0.1.1.

Changes since Version 3.0.0

This release includes the following changes to One-To-One Commerce:

l The OfﬁceExpress sample replaces the WebStore sample application.

l JavaScript ﬁles replace templates as the primary interface to the underlying components

(previously Dynamic Objects). This version is backward-compatible, and you may use the old
page templates.

l Components replace Dynamic Objects to provide the One-To-One functionality. This version is
backward-compatible, and you may use the old Dynamic Objects. Read more about the new
scripts and components in the Developer’s Guide to Components and Scripts.

l Address book functionality provides a means to write and read many addresses for shipping

destinations and billing addresses to and from the database.

l A persistent requisition maintains the contents of a requisition after session time-out.

l Purchase history functionality keeps track of purchases so that you can write rules that target

information to visitors based upon their purchasing patterns.

l Quotes functionality establishes the cost of an invoice in the event of special pricing and

quantity discounts. Instead of placing an order immediately, the visitor can obtain a quote for a
purchase. You determine when the quote expires.

l Purchasing lists, designated by aliases, provide a record of items and quantities that the visitor

can refer to repeatedly. The visitor may have several purchasing lists, recalling them and
placing them in the requisition for purchase on a regular basis.

l Extensible order management includes new APIs that allow you to create your own order

management processes and customize the order schema.

l Extensible payment method schema allow you to customize the payment method data.

l Purchase order payment types are included so that you can implement purchase order payment

handling.

l Conﬁgurable order ﬂow includes a new JavaScript order ﬂow engine which you can use to

direct the processing of different order types.

BroadVision, Inc.

591-410-NAS

One-To-One Business Commerce Release Notes

One-To-One Business Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Problems fixed in this release

5

l Euro currency conversion in the payment record of an order is supported for those countries

participating in the ﬁxed euro conversion program.

l Corporate account management includes new components that let you manage transactions for

visitors with respect to their corporate accounts.

l Contract product selection and pricing program components let you set up corporate contracts

for pre-deﬁned product lists and prices.

l Corporate account administration includes the new account administration application that

facilitates setting up corporate accounts.

l Support for the CyberSource Internet Commerce Services payment handler.

l One-To-One Commerce version 4.0.0 used a named gateway application (oexpress). All

applications in this software use the inetcgi gateway application by default.

See the introduction to the One-To-One Commerce Developer’s Guide and the One-To-One Commerce
User’s Guide for more information about the product’s features.

Problems fixed in this release

With the complete redesign of One-To-One Commerce using components and JavaScript, problems
affecting versions prior to this release are corrected. If you intend to use Dynamic Objects and
templates with this version, you may continue to experience problems encountered with earlier
releases. These are documented in the release notes for those versions.

One-To-One Business Commerce Release Notes

591-410-NAS

BroadVision, Inc.

6

One-To-One Business Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Known problems and issues

Known problems and issues

Note the following One-To-One Commerce tips, problems, and issues:

l 06504: The login page bexpress.html does not accept a double-byte visitor name. This affects
the Japanese version, speciﬁcally. To avoid this problem, add the following meta tag at the top
of the bexpress.html ﬁle:

<META HTTP-EQUIV=”Content-Type” CONTENT=”text/html;charset =x-euc-jp”>

l 07305: The Business Express sample application’s parametric search does not work for long

descriptions on the MS SQL Server database. The long description column is a text type in the
MS SQL Server schema and cannot be searched. To search based on description, either alter the
schema to make long description a varchar or use the short description ﬁeld.

l 07446: In the Business Express sample application the use of the "Enter" key when modifying a
quantity in a purchasing list produces a script error. Visitors should click the "Update" button to
enter a new quantity.

l 08399: Using large quantities with volume-based pricing may cause slow performance. Using

quantities of greater than 999 units causes a noticeable decrease in performance. With quantities
of greater than 5,000 system failure may result. This affects only volume-based pricing
calculations. Use the following work-arounds:

• Limit the “Quantity” input to not more than three digits on the HTML form with

MAXLENGTH=3 for the input ﬁeld.

• Provide SKUs of larger quantities for items sold normally in bulk. For example, set up an

SKU of 1000 toner cartridges that the visitor can purchase in single digit quantities: 3 lots of
1000 cartridges instead of 3000 cartridges.

• Use the BVI_MRPriceLookup component to determine if an item is volume-based and

restrict the purchase of that item accordingly.

l 08759: In the Business Express sample application on Japanese systems, the parametric search
“Reﬁning Attributes” do not appear when the category is selected. This is because the sample
data is in English. To correct the sample data for Japanese systems: In the One-To-One
Command Center, edit the Friendly Name attribute in the Search Attributes tab of the
categories, replacing the English friendly names with the proper Japanese friendly names.

Also, Japanese systems do not display the product comparison matrix. To correct the problem,
edit the Product Comparison Matrix attributes in the Product Comparison Information tab of
the Computer Products/Printers category. Replace the English friendly name list with the
Japanese friendly names of the attributes you want to display in the product comparison
matrix.

l 08905: The access control list permissions ﬁle for the mradmin and mrcatalogue applications
requires editing. The commerce_setup program enters permissions for the mradmin and
mrcatalog applications in the ﬁle /etc/opt/BVSNsmgr/bvsm.ACL. It erroneously ascribes a
preceding slash ‘/’ to each permission list. After running commerce_setup, edit the
bvsm.ACL ﬁle, removing the preceding slash from each of the entries. For example,

/mrcatalog/scripts/rebuild/* [Merchant_Administrator]+:@ALL-

should read as follows:

mrcatalog/scripts/rebuild/* [Merchant_Administrator]+:@ALL-

Then restart the interaction manager if it is already running.

BroadVision, Inc.

591-410-NAS

One-To-One Business Commerce Release Notes

One-To-One Business Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Known problems and issues

7

l 08941: The price and product list caches in the Interaction Manager are not ﬂushed as part of the

Notify Server operation in the One-To-One Command Center. To ﬂush these caches, run
cache_utl from the command line:

cache_utl -e mr_price_lookup
cache_utl -e mr_prod_filter

l 08946: Running commerce_setup will reinstall the order management tables, causing existing

data to be lost. Back up any existing order management data before running
commerce_setup.

l 08957: Parametric search result count may not be accurate with contract based product

selection. The search count is based upon the entire product catalog, not the contract based
selection (subset), and the search result reﬂects the count of items in the entire catalog. Avoid
using the search count feature if count accuracy is important.

l 09027: In the Business Express sample application, changing the item quantity to zero to delete a
row in a purchasing list causes the row to be removed, but another empty row appears in its
place. The BVI_MRShopList::updateItem() method is in error. Use the removeItem() method,
instead.

l 09084: The sample fulﬁllment process code generates an unreliable agent_name. To generate

an agent name, the sample fulﬁllment process source code appends a dynamic process ID to the
static process name to generate the agent_name for the fulﬁllment agent. This method is
described under the example main() program in the discussion, “Building a fulﬁllment
process” in the One-To-One Business Commerce Developer’s Guide. The process ID is dynamic
because each time One-To-One Commerce is started, new process IDs are created for the process
daemons. The resulting agent_name is unreliable because all orders for the fulﬁllment agent
still in process before a shutdown will be remain unprocessed when that agent’s agent_name
is recreated with a new process ID at start up.

The sample code ﬁles with this bug are:

$BV1TO1/merchant/examples/agent/mr_fulfill/mr_fulfill_main.cc
$BV1TO1/merchant/examples/agent/mr_fulfill/mr_sample_agent.cc

The errant code above is implemented in the mr_fulfill_d sample fulﬁllment daemon.

To avoid this problem, implement your fulﬁllment or other process agents with an
agent_name that does not append the process ID from the system. Create an agent_name that
is repeatable if you restart the system. To create multiple instances of the process, append the
numeric process number (proc_num from bv1to1.conf) instead of the process ID to the
process name to generate the agent_name.

l 09119: Duplicate order ﬂows are possible. The system allows you to set up more than one order

ﬂow for the same order type and service (store). In such a case, the most recently created
orderﬂow is referenced. Remove any duplicate order ﬂows.

l 09181: On a German system, the payment method screen of the Account Admin application

generates an error if you try to update an existing payment method using the expiration date
format that was displayed. To work around this problem, manually reset the expiration date to
the MM/YY format before updating.

l 09410: Order conﬁrmation fails for payment methods with names exceeding 28 characters. The
table column for card name is declared as 30 char for both BV_PAYMENT and MR_PAYMENT.
So when the payment handler constructs the payment method name from the visitor’s ﬁrst,
middle and last name, it may generate error if the total name is longer than 28 characters.

l 09447: This version of One-To-One Commerce includes AVP that does not support Canadian

taxation.

One-To-One Business Commerce Release Notes

591-410-NAS

BroadVision, Inc.

8

One-To-One Business Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Known problems and issues

l 09473: Business Express does not display the EUR currency symbol correctly. The BVI_Money
component’s stringValue property displays the wrong symbol after euro conversion. Avoid
using the BVI_Money.stringValue property to print the value obtained with the euroConvert()
method. Instead, print the currency and value properties from the BVI_Money object. Set the
symbol property of the euro value’s BVI_Money object to "none" and concatenate the currency
property and value property to display the euro symbol and currency value. A pseudo-code
example:

a = new BVI_Money(100);
100 DM
e = a.euroConver(’EUR’);
20,25 DM
e.symbol = ’none’;
print(e.currency + ’ ’ + e.doubleValue);
EUR 20,25

// wrong symbol displayed

// right symbol displayed

l 09503: The use of ISAPI requires modiﬁcation to the sample application scripts. To use ISAPI

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
