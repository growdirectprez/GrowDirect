---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Release Notes/Retail Commerce 4.1 NT release notes.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Retail Commerce 4.1 NT release notes.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Release Notes/Retail Commerce 4.1 NT release notes.pdf.md`
Size: 76,480 bytes

## Raw content
1

One-To-One Retail Commerce

Version 4.1.0 for Windows NT

Installation and Release Notes

This is Version 4.1.0 of BroadVision® One-To-One Commerce™ for the Windows NT operating
system. These release notes contain information about installing, conﬁguring, and starting
One-To-One Commerce. They also describe known problems and issues, and discuss supplemental
information not included in the documentation.

l “Documentation” on page 2

l “BroadVision Technical Support” on page 2

l “System and software requirements” on page 3

l “Changes since Version 3.0.0” on page 4

l “Problems ﬁxed in this release” on page 5

l “Known problems and issues” on page 6

l “One-To-One Commerce installation” on page 9

l “One-To-One Commerce conﬁguration” on page 11

l “Multiple host machine conﬁguration” on page 20

l “Database upgrade and migration” on page 22

l “Site-speciﬁc customization” on page 24

l “Supplemental information” on page 26

• “Conﬁguring AVP” on page 26

• “Conﬁguring CyberSource” on page 27

• “Conﬁguring the Shipping methods” on page 28

• “Using the Ofﬁce Express sample data” on page 33

• “Purging contents for deleted visitors” on page 33

l “Removing One-To-One Commerce” on page 34

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

2

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Documentation

Documentation

Because One-To-One Commerce is an application in BroadVision One-To-One Enterprise, all the
documentation for that product is applicable to One-To-One Commerce. The documentation that is
delivered with One-To-One Commerce Version 4.1.0 includes:

l These release notes.

l The One-To-One Commerce Developer’s Guide, which describes the application and how to

customize it.

To use the One-To-One Commerce HTML documentation, on your browser enter the URL that
points to the cwactoc.htm ﬁle.

l If you are reading the documentation from the CD-ROM specify the letter of your CD-ROM

drive.

For the One-To-One Commerce Developer’s Guide:

file:///E|/PUBS/commerce/b2c/devguide/cwactoc.htm

l If you are reading the ﬁles from the directory where the install program places them:

For the One-To-One Commerce Developer’s Guide:

file:/opt/bv1to1/pubs/commerce/b2c/devguide/cwactoc.htm

The /opt/bv1to1 path corresponds the value of the $BV1TO1 environment variable.

A Portable Document Format (PDF) version of the documentation is available in cwaug.pdf for the
One-To-One Commerce User’s Guide and CWAc.pdf for the One-To-One Commerce Developer’s Guide,
located in the same directory as the HTML ﬁles. To access the PDF ﬁles, you will need a PDF viewer,
such as Adobe's Acrobat Reader, which is available for free from Adobe's Web site at:

http://www.adobe.com/prodindex/acrobat/readstep.html

Additional BroadVision documents and white papers are available at:

http://www.broadvision.com

From time to time BroadVision updates the electronic documentation and makes it available to
customers. If you are interested in receiving a notification when updates are available, please
send an e-mail message to bvpubs@broadvision, and put "subscribe
commercev410docs" in the subject field. Notifications will be sent to the reply-address of the
message.

BroadVision Technical Support

Technical Support services are provided on an annual basis to BroadVision© customers. A standard
90-day warranty is also provided with all software.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
System and software requirements

3

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

System and software requirements

Installing and using One-To-One Commerce requires:

l A server machine that:

• runs BroadVision One-To-One Enterprise Version 4.1.0.

• accesses a CD-ROM drive.

• has 65 MB of available hard disk space.

• runs Netscape Communicator Version 4.6 or Internet Explorer Version 5.0. BroadVision

does not support other versions of these browsers for running the One-To-One Commerce.

• has a VGA monitor with a screen resolution of 800 x 600 or higher.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

4

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Changes since Version 3.0.0

l The same system and software requirements as BroadVision One-To-One Enterprise. See that

system’s Server Release Notes and Installation and System Administration Guide for details.

If you are using AVP TaxWare, you’ll need version 3.0. If you are using CyberSource for payment
handling, you’ll need CyberSource ICS2 3.0.1.1.

Changes since Version 3.0.0

This release includes the following changes to One-To-One Commerce:

l The BusinessExpress sample replaces the WebStore sample application.

l JavaScript ﬁles replace templates as the primary interface to the underlying components

(previously Dynamic Objects). This version is backward-compatible, and you may use the old
page templates.

l Components replace Dynamic Objects to provide the One-To-One functionality. This version is
backward-compatible, and you may use the old Dynamic Objects. Read more about the new
scripts and components in the Developer’s Guide to Components and Scripts.

l Address book functionality provides a means to write and read many addresses for shipping

destinations and billing addresses to and from the database.

l A persistent shopping cart maintains the contents of a shopping cart after session time-out.

l Purchase history functionality keeps track of purchases so that you can write rules that target

information to visitors based upon their purchasing patterns.

l Quotes functionality establishes the cost of an invoice in the event of special pricing and

quantity discounts. Instead of placing an order immediately, the visitor can obtain a quote for a
purchase. You determine when the quote expires.

l Shopping lists, designated by aliases, provide a record of items and quantities that the visitor

can refer to repeatedly. The visitor may have several shopping lists, recalling them and placing
them in the shopping cart for purchase on a regular basis.

l Extensible order management includes new APIs that allow you to create your own order

management processes and customize the order schema.

l Extensible payment method schema allow you to customize the payment method data.

l Purchase order payment types are included so that you can implement purchase order payment

handling.

l Conﬁgurable order ﬂow includes a new JavaScript order ﬂow engine which you can use to

direct the processing of different order types.

l Euro currency conversion in the payment record of an order is supported for those countries

participating in the ﬁxed euro conversion program.

l Support for the CyberSource Internet Commerce Services payment handler.

l One-To-One Commerce version 4.0.0 used a named gateway application (oexpress). All

applications in this software use the inetcgi gateway application by default.

See the introduction to the One-To-One Commerce Developer’s Guide and the for more information
about the product’s features.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Problems fixed in this release

5

Problems fixed in this release

With the complete redesign of One-To-One Commerce using components and JavaScript, problems
affecting versions prior to this release are corrected. If you intend to use Dynamic Objects and
templates with this version, you may continue to experience problems encountered with earlier
releases. These are documented in the release notes for those versions.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

6

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Known problems and issues

Known problems and issues

Note the following One-To-One Commerce tips, problems, and issues:

l 06504: The login page oexpress.html does not accept a double-byte visitor name. This affects
the Japanese version, speciﬁcally. To avoid this problem, add the following meta tag at the top
of the oexpress.html ﬁle:

<META HTTP-EQUIV=”Content-Type” CONTENT=”text/html;charset =x-euc-jp”>

l 07305: The Ofﬁce Express sample application’s parametric search does not work for long

descriptions on the MS SQL Server database. The long description column is a text type in the
MS SQL Server schema and cannot be searched. To search based on description, either alter the
schema to make long description a varchar or use the short description ﬁeld.

l 07446: In the Ofﬁce Express sample application the use of the "Enter" key when modifying a

quantity in a shopping list produces a script error. Visitors should click the "Update" button to
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

l 08759: In the Ofﬁce Express sample application on Japanese systems, the parametric search

“Reﬁning Attributes” do not appear when the category is selected. This is because the sample
data is in English. To correct the sample data for Japanese systems: In the One-To-One
Command Center, edit the Friendly Name attribute in the Search Attributes tab of the
categories, replacing the English friendly names with the proper Japanese friendly names.

Also, Japanese systems do not display the product comparison matrix. To correct the problem,
edit the Product Comparison Matrix attributes in the Product Comparison Information tab of
the Computer Products/Printers category. Replace the English friendly name list with the
Japanese friendly names of the attributes you want to display in the product comparison
matrix.

l 08946: Running commerce_setup will reinstall the order management tables, causing existing

data to be lost. Back up any existing order management data before running
commerce_setup.

l 09027: In the Ofﬁce Express sample application, changing the item quantity to zero to delete a
row in a purchasing list causes the row to be removed, but another empty row appears in its
place. The BVI_MRShopList::updateItem() method is in error. Use the removeItem() method,
instead.

l 09084: The sample fulﬁllment process code generates an unreliable agent_name. To generate

an agent name, the sample fulﬁllment process source code appends a dynamic process ID to the
static process name to generate the agent_name for the fulﬁllment agent. This method is
described under the example main() program in the discussion, “Building a fulﬁllment
process” in the One-To-One Retail Commerce Developer’s Guide. The process ID is dynamic
because each time One-To-One Commerce is started, new process IDs are created for the process

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Known problems and issues

7

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

l 09188: Migrating the address book from version 3.0.0 to version 4.1.0 does not work. If you are
migrating from version 3.0.0 to version 4.1.0, please download the Commerce 3.0.0 Migration
ﬁx from www.broadvision.com under support and software patches.

l 09410: Order conﬁrmation fails for payment methods with names exceeding 28 characters. The
table column for card name is declared as 30 char for both BV_PAYMENT and MR_PAYMENT.
So when the payment handler constructs the payment method name from the visitor’s ﬁrst,
middle and last name, it may generate error if the total name is longer than 28 characters.

l 09447: This version of One-To-One Commerce includes AVP that does not support Canadian

taxation.

l 09473: Ofﬁce Express does not display the EUR currency symbol correctly. The BVI_Money
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

with the sample application,

a. Replace inetcgi.exe with bvisapi.dll in your HTTP server’s cgi-bin directory.

Both of these are available in $BV1TO1/bin.

b. Edit the following login script ﬁles in your document root directory:

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

8

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Known problems and issues

• /oexpress/scripts/login.jsp

Change the lines that read,

Session.errorMessage += ’<P> Please retry the
<A HREF="’+server_url+loginPage+’"> Login Page </A> again.’;

removing the "server_url+" from the line so that it reads,

Session.errorMessage += ’<P> Please retry the
<A HREF="’+loginPage+’"> Login Page </A> again.’;

c. Edit the following login script ﬁles in your document root directory:

• /oexpress/scripts/login.jsp

• /oexpress/scripts/guest.jsp

Change the line that reads,

Response.redirect(server_url+makeScriptURL(mainFrameSet));

removing "server_url+" from the line so that it reads,

Response.redirect(makeScriptURL(mainFrameSet));

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce installation

9

One-To-One Commerce installation

If you have a running One-To-One site, back it up before performing this installation. This install
process modiﬁes the One-To-One database schema. If you have problems during the installation
and have to uninstall One-To-One Commerce, you should restore the database and schema
speciﬁcations from the backup. See the One-To-One Installation and System Administration Guide for
details about backing up your site.

If you intend to install the Broadway sample application, you must install it before installing
any BroadVision One-To-One application such as One-To-One Commerce.

Installing and conﬁguring includes:


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
