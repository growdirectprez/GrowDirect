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

l One-To-One Commerce conﬁguration

• Conﬁguring One-To-One

• Conﬁguring One-To-One Commerce

• Conﬁguring the Interaction Manager for One-To-One Commerce

• Conﬁguring the HTTP server

l Multiple host machine conﬁguration

l Database upgrade and migration

• Migrating the order management data

• Migrating the address book schema

• Migrating the related content schema

l Site-speciﬁc customization

l Supplemental information

• Conﬁguring AVP

• Conﬁguring CyberSource

• Conﬁguring the Shipping methods

• Using the Ofﬁce Express sample data

• Purging contents for deleted visitors

Before installing One-To-One Commerce

1. Install BroadVision One-To-One Enterprise version 4.1. Follow the instructions in the Installation
and System Administration Guide. The "Commerce-speciﬁc conﬁguration" chapter of that guide
has information essential to One-To-One Commerce installation.

• If you are installing One-To-One for the ﬁrst time, it would be easiest if you do not conﬁgure

or start One-To-One yet. Wait until after you have installed One-To-One Commerce.

• If you have already installed and started One-To-One version 4.1, a later step in these
release notes tells you how to make changes to the conﬁguration for One-To-One
Commerce.

2. If you are upgrading One-To-One or One-To-One Commerce from an earlier version, follow the
instructions in the Installation and System Administration Guide for upgrading the One-To-One
application system.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

10

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce installation

3. Run setup.exe from the windows\Server4.1h directory. This will install the upgrade patch

H for BroadVision One-To-One Enterprise. You must install this patch before installing
One-To-One Commerce.

4. Check the BroadVision website for any updates or patches succeeding patch H.

http://www.broadvision.com

The CD-ROM for this version of One-To-One Commerce includes BroadVision One-To-One
Enterprise server patch H.

5. If the One-To-One servers or Interaction Manager servers are running, shut them down now.

From an MKS shell:

$BV1TO1/bin/imgr_conf -a stop
$BV1TO1/bin/bvconf shutdown

From the Start menu:

• Select Programs|BroadVision One-To-One Enterprise|Stop Interaction Manager

• Select Programs|BroadVision One-To-One Enterprise|Shutdown One-To-One Servers

You may now proceed with installing One-To-One Commerce.

One-To-One Commerce requires 65 megabytes of disk space.

To install One-To-One Commerce:

1. Insert the One-To-One Commerce CD-ROM into your CD-ROM drive.

2. Run setup.exe from the windows\Server4.1h directory. This will install the upgrade patch

H for BroadVision One-To-One Enterprise. You must install this patch before installing
One-To-One Commerce.

3. Run setup.exe from the windows\Retail directory. This will install One-To-One

Commerce.

4. Choose the language, depending on the locale.

The One-To-One Commerce components will be installed under the $BV1TO1 directory.

If you want to run the shipping editor, answer "yes" to the question about registering the MKS
toolkit.

You can now proceed to One-To-One Commerce conﬁguration, next.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

11

One-To-One Commerce configuration

Four procedures guide you through the conﬁguration process:

l “Conﬁguring One-To-One” on page 11

l “Conﬁguring One-To-One Commerce” on page 16

l “Conﬁguring the Interaction Manager for One-To-One Commerce” on page 18

l “Conﬁguring the HTTP server” on page 19

Conﬁguring One-To-One

Make the following conﬁguration changes to One-To-One. These changes allow you to start the
system and use the One-To-One Commerce Ofﬁce Express sample application.

l If you have just installed One-To-One, follow the instructions for “New One-To-One

installations.”

l If you have already started One-To-One at your site, follow the instructions for “Existing

One-To-One installations” on page 12.

New One-To-One
installations

If you have just installed One-To-One and not started it, edit the bv1to1.conf conﬁguration ﬁle
provided with One-To-One Commerce (run these commands from an MKS shell):

1. If you haven’t done so already, create the $BV1TO1_VAR/etc directory:

mkdir $BV1TO1_VAR/etc

2. If bv1to1.conf, the One-To-One conﬁguration ﬁle, is not already in $BV1TO1_VAR/etc,

a. Copy the default into that directory:

 cp $BV1TO1/merchant/examples/bv1to1.conf.example \

$BV1TO1_VAR/etc/bv1to1.conf

b. Make the ﬁle writable, the default is read-only:

 chmod +w $BV1TO1_VAR/etc/bv1to1.conf

3. Start One-To-One with bvconf.

bvconf execute -a install_all

Do not start the Interaction Manager servers yet.

You can now proceed to “Conﬁguring One-To-One Commerce” on page 16.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

12

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

Existing
One-To-One
installations

If you already have a bv1to1.conf conﬁguration ﬁle, edit it and make the following changes. You
can see examples of these settings in the $BV1TO1/merchant/examples/
bv1to1.conf.example conﬁguration ﬁle. Copy the new variables from the following sections of
the bv1to1.conf.example conﬁguration ﬁle, then deﬁne the variables according to your system.

1. Deﬁne“OfﬁceExpress” as an additional service to use the sample application data. Use this

example to deﬁne your own services.

service OfficeExpress {
parameter

email_address = "manager@OfficeExpress.com"
postal_address = "1100 First St, San Jose, CA"
www_url = "www.OfficeExpress.com"
phone_number = "800-555-1010"
fax_number = "800-555-2020"
pmttype_id = "0, 1, 2"
other1 = "Customer Service: P.O. Box 101, San Jose, CA"
# override the default payment processing methods
# if desired
# pmt_methods = "0=cybersourceics2, 1=cybersourceics2,
#

2=cybersourceics2"

}

Each service can have its own payment methods. These are disabled in the example above so
that it will use the default payment methods.

2. Deﬁne the variables in the “One-To-One Commerce” sections.

Variable

FABMSHIPCONFIG=

mr_oﬂow_script_root=

mr_oﬂow_startup_root=

mr_encrypt_card_num=

MR_ALT_CURRENCY=

Default Value

Description

$getenv(BV1TO1_VAR) + "/
etc/shipping.conf"

$getenv(BV1TO1_VAR) + /etc/
oﬂow/scripts"

Shipping conﬁguration
directory.Deﬁne this variable
in your bv1to1.conf ﬁle’s
export section.

Order ﬂow script root.

$getenv(BV1TO1_VAR) + /etc/
oﬂow/script_library"

Order ﬂow startup and script
libarary root.

"1"

" "

If set to "1" the CARD_NUM
column in the MR_PAYMENT
table is encrypted; if "0" the
column is not encrypted.

Alternate currency. To enable
euro currency conversion, set
this to "EUR" (or set the default
currency deﬁned by the OS
locale to "EUR" and this to an
alternate currency). When euro
currency conversion is not
applicable, set this to an empty
string.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

13

3. Set the content type cache size variable. The bv1to1.conf example below includes cache size

designations for the One-To-One Commerce content types:

cnt_type_cache_size="PRODUCT=300, AD=200, COLLECTION=0, COMMUNITY=0,
MR_PAYMENT_METHOD=0, MR_ORDERS=0,
MR_SHOPPING_LIST=0, MR_QUOTES=0"

4. Set the order management server path. The bv1to1.conf example ﬁle provides:

mr_om_srv_path="OrderMgmt/Server/mr_om_srv"

5. Deﬁne a process for the order management server. This must be the ﬁrst One-To-One

Commerce process deﬁned in the bv1to1.conf ﬁle.

process mr_om_srv {}

The processes for the order management and payment servers from previous versions of
One-To-One Commerce are also listed in the bv1to1.conf example ﬁle. Use these if you are
running the older order management system.

process ofbe_srv {}
process om_srv {}
process ofdb {}

6. Deﬁne a payment handler daemon for each payment process. There are three examples in the

bv1to1.conf example ﬁle, each is distinguished by its unique proc_num.

daemon mr_pmthdlr_d {
parameter

proc_num="3"
pmt_method="test"
store_id="-1"
poll_state="1"
transit_state="2"
max_orders="5"
sleep="180"
loop="0"
offline="1"

}

Likewise, the fulﬁllment and settlement handlers mr_fulfill_d and mr_pmtsettle_d are
also provided in the bv1to1.conf example ﬁle. As in the above example, be sure the daemons
are disabled with

offline="1"

Before you run commerce_setup (later on), the value of the offline parameter for all
daemons must be set to offline="1".

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

14

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

Leaving the order management daemons defined will cause bvconf to fail because
One-To-One Commerce is not yet set up and the processing agents cannot find the content
tables. Do not enable the daemons until after commerce_setup.

For older versions: The payment and fulﬁllment handlers for the order management system
from previous versions of One-To-One Commerce are also listed in the bv1to1.conf example
ﬁle. Use these if you are running the older order management system.

daemon pmtassign_d {}
daemon pmthdlr_d {}
daemon pmtsettle_d {}

7. Deﬁne an order ﬂow daemon, for example:

daemon mr_oflow_d {
parameter

sleep="180"
loop="0"
delay="300"
offline="1"

}

8. Set the default payment methods for each of the pmthdlr_d processes.

default_pmt_methods="0=test, 1=test,

2=test,

9. To use AVP TaxWare, remove the comments from the AVP variables. See “Conﬁguring the

Taxing system” in the One-To-One Installation and System Administration Guide for instructions.
Also, see “Conﬁguring AVP” on page 26 of these release notes.

10. If you are using the CyberSource payment processor, follow the instructions, “Conﬁguring

CyberSource” on page 27.

11. In the Site conﬁguration section, add the default shipping destination address ﬁeld values. For

U.S.A. locations, use these settings:

default_country="US"
default_city="Enter your city"
default_locality="CA"
default_postal_code="94087"

These setting must be deﬁned and the postal code value correct for your location before guest
visitors can review the items in their shopping carts.

12. Turn on the retrieval of billing address information from the visitor’s proﬁle by changing the

pmt_addr_from_profile setting from 0 to 1.

pmt_addr_from_profile = "1"

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

15

13. Enable the e-mail alert feature by setting this variable to your e-mail host:

bv_email_host="localhost"

Also, be sure the offline parameter’s value is zero ("0") in the deliv_smtp_d daemon:

daemon deliv_smtp_d {

parameter
shutdown="bvkill -w 2 USR1"
id="1"
delay="600"
sleep="120"
msg_delay="30"
offline="0"

# this daemon is now on line

}

Unlike the order management daemons, this daemon may be enabled before
commerce_setup.

14. Start One-To-One with bvconf.

bvconf execute

Do not start the Interaction Manager yet.

You can now proceed to the next section, “Conﬁguring One-To-One Commerce.”

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

16

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

Conﬁguring One-To-One Commerce

To set up and conﬁgure One-To-One Commerce, run the commerce_setup script. This script
allows you to selectively load or reload the sample data ﬁles. To run this script, you need to know:

l The database password.

l The path to your HTTP document root directory. This is the default directory where your HTTP

server looks for HTML ﬁles.

l The path to your script directory. The setup process creates oexpress/ as a subdirectory in the
script root directory, and then copies the One-To-One Commerce script and image ﬁles into that
subdirectory. The setup process also copies the oexpress.html ﬁle to the document root
directory.

Before you run the commerce_setup script:

l Make sure that the One-To-One services are running.

l Shut down the Interaction Manager.

l Verify the $BV1TO1_VAR/BVSNsmgr/<machine name> directory is established. It is set up

with the imgr_conf utility during One-To-One installation:

imgr_conf -a configure

You may also manually create the directory. See the Installation and System Administration Guide
for more information.

If you are using the Oracle database you must export the database variable. From an MKS shell,
issue the following command:

export BV_DB_DATABASE="yourDatabase"

To conﬁgure One-To-One Commerce:

1. Run the commerce_setup script.

Running commerce_setup will reinstall the order management tables, causing existing data to
be lost. Back up any existing order management data before running commerce_setup.

$BV1TO1/merchant/commerce_setup

2. Enter the default path to your HTTP document root directory. This is the default directory
where your HTTP server looks for ﬁles. The script will copy some HTML ﬁles into this
directory.

The document root is the same directory that was speciﬁed when conﬁguring the site’s
Interaction Manager and is the location that your HTTP server looks for ﬁles when the URL for
the site is the root locations, such as http://www.broadvision.com/.

3. Enter the default path to your script directory. This is the directory where you store the script
ﬁles for your site. The utility creates a subdirectory (oexpress/scripts) in the script root
directory, and copies the One-To-One Commerce script ﬁles into that directory.

4. Answer the prompts as they appear.

If you choose to load the sample data, commerce_setup loads the database with sample data,
and loads the sample script ﬁles and images into <script root>/oexpress/scripts and

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

17

<doc root>/oexpress/images. If commerce_setup cannot ﬁnd your <doc root>
directory, you’ll have to copy the ﬁles manually.

5. Enable the order management daemons. Edit the bv1to1.conf ﬁle, changing the value of the
offline parameter for each daemon. Each daemon’s offline parameter should read as
follows:

offline="0"

Make this edition for all of the order management daemons:

• mr_pmthdlr_d

• mr_pmtsettle_d

• mr_oflow_d

• mr_fulfill_d

6. Restart One-To-One with bvconf.

bvconf shutdown
bvconf execute

After setting up the application and loading the sample data files according to your answers to
the preceding questions, the script tells you that the setup is complete and instructs you to start
the Interaction Manager. Do not do so. Instead, proceed to the next section, “Configuring the
Interaction Manager for One-To-One Commerce.”

Installing the version 3.0.0 sample application

This section explains how to install the sample application and data from One-To-One Commerce
version 3.0.0.

Note that installing the version 3.0.0 WebStore sample application will change the One-To-One
database schema. This extension is necessary to run the One-To-One Commerce version 3.0.0
Dynamic Objects. If you do not plan to use the version 3.0.0 Dynamic Objects, do not run the
commerce_setup with the -w option. Also, be aware that running commerce_setup -w
overwrites and replaces the page template files from the earlier version. You might want to
consider reviewing the changed files and applying the changes to your existing application,
rather than running the following procedures.

Optionally, you may install the version 3.0.0 sample application with this version of One-To-One
Commerce. Run commerce_setup with the “-w” option, as follows:

commerce_setup -w

The sample application does not use the version 4.1.0 script ﬁles and components. Make sure that
the service is deﬁned in your bv1to1.conf ﬁle along with the Ofﬁce Express service.

After setting up the application and loading the sample data ﬁles according to your answers to the
preceding questions, the script tells you that the setup is complete and instructs you to start the
Interaction Manager. Do not do so. Instead, proceed to the next section, “Conﬁguring the Interaction
Manager for One-To-One Commerce.”

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

18

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

Conﬁguring the Interaction Manager for One-To-One Commerce

To setup the Interaction Manager for use by One-To-One Commerce:

1. Conﬁgure the Interaction Manager per the instructions in “Conﬁguring the Interaction
Manager” in the One-To-One Installation and System Administration Guide. Follow the
instructions for establishing a named application, ﬁrst running the conﬁguration editor with:

imgr_conf -a configure

Then answer “n” when prompted to name the conﬁguration.

2. When you are running the conﬁguration editor, set the values as speciﬁed in the Installation and

System Administration Guide.

For the default page to return to upon error, specify an HTML ﬁle that you will create. If an
error occurs while running One-To-One Commerce, this error page will be sent to the visitor’s
browser. However, the page will appear in a frame in the One-To-One Commerce page layout.
From there, if you want to provide a link back to the application’s welcome page, such as
oexpress.html, include target="_top" to remove the frame set. Otherwise, the welcome
page will appear in the same frame.

3. Start the Interaction Manager (see the One-To-One Installation and System Administration Guide

for details):

$BV1TO1/bin/imgr_conf -a start

If you examine the bvlog.out.xxx log ﬁle, you should see that the libmrcomponents.lib
library got loaded.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
One-To-One Commerce configuration

19

Conﬁguring the HTTP server

Copy the inetcgi.exe (or anamecgi.exe as yourname.exe for named applications) program
to your HTTP server’s cgi-bin directory.

You may also use ISAPI. However, the use of ISAPI requires modification to the sample
application scripts. See bug 09503 under “Known problems and issues” on page 6.

The install process puts all One-To-One Commerce sample application ﬁles in $BV1TO1/
merchant/oexpress. To make the HTML, scripts and graphics ﬁles available to your HTTP
server, the commerce_setup script copies all the ﬁles in that directory into a subdirectory called
oexpress in your document root directory. Additionally, it further copies the oexpress.html
into your document root.

$BV1TO1/merchant/oexpress/
<script root>/oexpress/scripts/
<HTTP document root>/oexpress/images
<HTTP document root>/oexpress.html

Original files
Copy of original files

Copy of original graphics files

Copy of original HTML file

If commerce_setup cannot ﬁnd your <doc root> you must copy the ﬁles manually.

To make oexpress.html the default page for your site, see your HTTP daemon documentation.
Sometimes it is as easy as creating a ﬁle named index.html in the HTTP document root directory,
like this:

cd <HTTP document root>
cp oexpress.html index.html

Restart your HTTP daemon to recognize these changes.

The installation is complete. You can now start the One-To-One Commerce OfﬁceExpress sample
application. See “Using the Ofﬁce Express sample data” on page 33.

When you are ready to begin your own site, follow the instructions in “Site-speciﬁc customization.”
If you have multiple machines running your One-To-One site, refer to ““Multiple host machine
conﬁguration” on page 20.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

20

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Multiple host machine configuration

Multiple host machine configuration

If you are installing One-To-One version 4.1.0 on multiple host machines, where either the script
root directory, doc root directory, or $BV1TO1 directory is not accessible among machines due to the
presence of ﬁrewalls or the fact that UNC is not in use, these requirements must be met:

l One-To-One Commerce must be installed on all host machines.

l The $BV1TO1 directory path and contents must be identical on any machines running an

Interaction Manager or CORBA server, for example C:/bv1to1.

• The $BV1TO1/bin directory on the root host must be identical to the $BV1TO1/bin

directories across machines.

• The $BV1TO1/lib directory on the root host must be identical to the $BV1TO1/lib

directories across machines.

l The IT daemon ports connected to the CORBA server must be the same on any machines

running an Interaction Manager or CORBA server.

l You must copy $BV1TO1_VAR from the root host machine to the machines running the

Interaction Managers and CORBA servers.

The One-To-One and Interaction Manager servers are designed to run on distributed hosts. All
One-To-One and Interaction Manager servers communicate with each other via CORBA, and many
of them read ﬁles from and write ﬁles to common locations deﬁned by the $BV1TO1 and
$BV1TO1_VAR directories. If all of the hosts can access the common locations, such as with UNC on
Windows NT, you need do nothing special except possibly to deﬁne in the bv1to1.conf ﬁle the
host machines and possibly identify the remote shell to use when accessing those hosts.

However, if the servers cannot access the same ﬁle locations because of a ﬁrewall, you must
conﬁgure the system as follows:

1. Install One-To-One in the same location — the $BV1TO1 directory — on each host machine,

such as /bv1to1/. The installation process populates this location with the One-To-One and
Interaction Manager executable ﬁles. This location must be the same on each host. See the
Installation and System Administration Guide for complete instructions.

2. Set $IT_DAEMON_PORT to the same port number on each machine. The CORBA servers on each

machine use the same port number for communicating to the ORB.

3. Deﬁne the hostmgr parameters in bv1to1.conf for each Interaction Manager stand-alone

host. For example:

process hostmgr {parameter host="host1"}

When One-To-One starts on the root host (the machine where you run bvconf), it launches a
CORBA servers on each hostmgr host to allow the Interaction Manager servers to
communicate with the One-To-One servers. You do not need to deﬁne hostmgr for hosts that
are also running One-To-One servers, because they automatically launch the ORB when
One-To-One starts. See the description of the hostmgr parameter in the Installation and System
Administration Guide for details.

4. Deﬁne the name for the One-To-One instance on all of the machines in the same instance; deﬁne
the name with the $BV1TO1_INSTANCE variable. This variable is created by the bvconf
execute command’s -i instance_name option, which adds it to the shell start-up scripts in
the $BV1TO1_VAR/etc directory. Always “source” a start-up script before starting servers.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Multiple host machine configuration

21

5. Set the database environment variables on all machines running database accessor servers, and

the Interaction Manager servers. See “Database variables” in the Installation and System
Administration Guide for more information about setting these variables.

6. Create identical $BV1TO1_VAR locations accessible to each Interaction Manager host. This
location is where the servers get their conﬁguration information, and where they write
observation and log ﬁle data. This location must be the same on each host; for example, if it is
/bv1to1_site/, it must be that location on every host.

Whenever you change the site configuration, from the root host:

a. Copy the $BV1TO1_VAR/var/orb directory contents to each distributed host. This

directory contains the Orbix CORBA conﬁguration information.

b. Copy the $BV1TO1_VAR/etc/ directory contents to each distributed host. This directory

contains the site conﬁguration information.

c.

If you use the dump_taxon utility, copy the $BV1TO1_VAR/cache/taxon ﬁle to each
distributed host. This ﬁle is the category and matching attributes cache ﬁle that the
Interaction Manager can use for fast matching.

7. Make the log ﬁles directory accessible to all servers. Servers write observation and log message
data to the $BV1TO1_VAR/logs/hostName directory, where hostName is the name of the
server host machine. In a multiple-host conﬁguration environment, accessing $BV1TO1_VAR is
often inefﬁcient.

Instead, deﬁne $BVLOG_DIR in the bv1to1.conf ﬁle to identify the directory where servers
will write the ﬁles on the local host. Then, the ﬁles will be written to $BVLOG_DIR/logs/
hostName. The directory must exist on all host machines before starting the servers on that
machine.

• To aggregate observation data, the ﬁles from all hosts must ﬁrst be copied to a central

location. See the Database Administrator’s Guide for details.

8. All machines must use the same login account to launch the One-To-One and Interaction

Manager servers, and that account must not be a root level account.

Later, when you start the servers, start the One-To-One servers on the root host, and then start the
Interaction Manager servers on the remote hosts.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

22

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Database upgrade and migration

Database upgrade and migration

This release replaces the orders and payment methods data from version 4.0.0 and earlier versions
with the new One-To-One Commerce order management and payment method tables. It also
replaces the version 3.0.0 address book and related content schema.

Migration involves:

l Migrating the order management data

l Migrating the address book schema

l Migrating the related content schema

Migrating the order management data

Before migrating existing order management data, do the following:

1. In bv1to1.conf, set the following variable:

MR_USE_V3_ORDER_SYSTEM=”0”

2. Update your environment in an MKS shell:

unset MR_USE_V3_ORDER_SYSTEM=

.$BV1TO1_VAR/etc/bv1to1.conf.sh

3. Make sure the order management system from the previous version continues to run.

The order management system for previous versions of One-To-One must continue to process
existing orders. The servers for previous versions (such as pmthdlr_d, om_srv, and so on)
should continue to run and update the old order management database tables
(BV_MAIN_INVOICE_TABLE, BV_PAYMENT, and so on). New orders will be processed with
the version 4.1.0 order management system. Order information will be stored in the
MR_ORDERS and related tables. The new process daemons like mr_pmthdlr_d can coexist
with the old process daemons like pmthdlr_d.

Wait until all existing orders are completed before going on to the next two steps.

4. Shut down the site.

5. Run the migration script located at $BV1TO1/merchant/scripts/mr_migrate_to_410.

6. Check the log ﬁle ($BV1TO1_VAR/dbschema/tmp/mr_migrate_to_410.log) for errors.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Database upgrade and migration

23

Order state mappings

By default, only orders of the following old order states will be migrated and given new order
states:

Old ORDER_STATE

New ORDER_STATE

8 _OrderComplete

11  OrderComplete

9 _OrderPartiallyComplete

12  OrderPartiallyComplete

17  _OrderReturnComplete

13 OrderReturnComplete

10  _OrderCancelled

14 OrderCancelled

999 UnknownError

Review the ﬁle $BV1TO1/merchant/scripts/README.migrate_to_410 for additional
migration information.

Migrating the address book schema

The MR_ADDR_BOOK table is a related attribute table of the user proﬁle system. This table replaces
the following columns in the BV_MR_USER_PROFILE table from version 3.0.0:

MR_NAME

MR_NAME1

MR_NAME2

MR_NAMEB

MR_ADDRESS

MR_ADDRESS1

MR_ADDRESS2

MR_ADDRESSB

MR_CITY

MR_STATE

MR_ZIP

MR_CITY1

MR_STATE1

MR_ZIP1

MR_CITY2

MR_STATE2

MR_ZIP2

MR_CITYB

MR_STATEB

MR_ZIPB

MR_COUNTRY

MR_COUNTRY1

MR_COUNTRY2

MR_COUNTRYB

MR_EMAIL

MR_PHONE

MR_FAX

MR_EMAIL1

MR_PHONE1

MR_FAX1

MR_EMAIL2

MR_PHONE2

MR_FAX2

MR_EMAILB

MR_PHONEB

MR_FAXB

The migration script will scan the existing user proﬁle and copy the address information into the
normalized MR_ADDR_BOOK table.

The migration scripts, located in $BV1TO1/merchant/dbschema, are deﬁned for the following
databases:

l mr_migrate_to_4.1.0_addressbook.ora for Oracle.

l mr_migrate_to_4.1.0_addressbook.syb for MSSQL.

Before running a migration script, back up your database. Also, source the bv1to1.conf.sh ﬁle to
set the environment variables.

You may customize the following variables, corresponding to the four default address aliases listed
above:

l PRINCIPAL_ADDR

l ALTERNATE1_ADDR

l ALTERNATE2_ADDR

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

24

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Site-specific customization

l ALTERNATE3_ADDR

The script provides default aliases for these, but you may change them based on your requirements.

You may also customize the DEFAULT_SHIPPING variable, new to this release. It is an option in the
address book entry which you can pre-populate. The default value is an empty string.

Once the migration is complete, you can check the MR_ADDR_BOOK content with the One-To-One
Command Center, or log in to the OfﬁceExpress sample application after you’ve installed and
conﬁgured it, and use the address book feature.

Migrating the related content schema

The MR_REL_CONTENT table is a related attribute table of the BV_PRODUCT content table. It
replaces the MR_RELATED_PRODUCT column of the BV_PRODUCT table. Whereas in the version
3.0.0 MR_RELATED_PRODUCT column the products appeared as a list separated by commas, in
this version’s MR_REL_CONTENT table each related product occupies a row. The
MR_REL_CONTENT table also includes the content type and relationship type for each row of data.

The migration script, mr_migrate_to_4.1.0_relatedcnt located in the $BV1TO1/merchant/
dbschema/ directory will scan the BV_PRODUCT table for any product with a non-empty
MR_RELATED_CONTENT column and then create a row in the MR_REL_CONTENT table for each
product. Each product will have a content type of “0” for PRODUCT, and a relation type of
“CrossSell.”

Before running the migration script, set the $BV1TO1 environment variable, and be sure
One-To-One is running.

Site-specific customization

The default installation and setup creates an application called OfﬁceExpress. The easiest way to
create a new application speciﬁc to your site is to customize that application. The following
instructions customize the script ﬁles, images, and static HTML ﬁles that form the framework of the
application. When you have ﬁnished with these steps, you can begin deﬁning rules and collections,
and loading product data.

Customize the
One-To-One
conﬁguration

To customize the One-To-One conﬁguration for your site:

1. Locate the “Default shipping destination address ﬁelds” in the Site conﬁguration section and

make sure that they are correct for your site and locale.

default_country="US"
default_city="Enter your city"
default_locality="CA"
default_postal_code="94087"

These setting must be deﬁned and the postal code value correct for your location before a guest
visitors can review the items in their shopping carts. The example above is for U.S.A. locales. To
see an example that is appropriate for your locale, see the sample conﬁguration ﬁle $BV1TO1/
merchant/examples/bv1to1.conf.example.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Site-specific customization

25

2. Near the end of the bv1to1.conf ﬁle, look for OfficeExpress service deﬁnition and

duplicate and modify it to match your services’s settings.

service OfficeExpress {

parameter
email_address = "mgr@YourStoreName.com"
postal_address = "12345 Main St, San Jose, CA"
www_url = "www.YourStoreName.com"
phone_number = "800-555-1234"
fax_number = "800-555-1235"
pmttype_id = "0, 1, 2"
other1 = "Customer Service: P.O. Box 5, Los Altos, CA"
# override the default payment processing methods, optional
# pmt_methods = "0= , 1= ,
# 2=

}

For details about creating a new service deﬁnition, see the “Adding, changing, or removing a
service” section in the Installation and System Administration Guide.

3. Review “Supplemental information” on page 26 for additional conﬁguration tasks that might

apply to your application.

You can now proceed to customize the OfﬁceExpress application.

To customize the OfﬁceExpress application for your site:

1. Customize the e-mail address, subject, to, and from ﬁelds for a conﬁrmation e-mail by editing

the oexpress/scripts/order/confirmation.jsp script.

2. Edit the other script ﬁles to change the look and feel to match your site’s requirements.

3. Load the databases with your data. You can either enter information from the One-To-One
Command Center, or load the information from ﬁles directly into the database per the
instructions in “Bulk loading data” chapter in the One-To-One Database Administrator’s Guide.

4. Deﬁne the rules and rule sets for your site using the One-To-One Command Center.

This concludes the instructions for customizing your application.

Customize the
Ofﬁce Express
application

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

26

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

Supplemental information

This section discusses the following topics which were not included in the documentation.

l “Conﬁguring AVP” described next.

l “Conﬁguring CyberSource” on page 27

l “Conﬁguring the Shipping methods” on page 28

l “Using the Ofﬁce Express sample data” on page 33

l “Purging contents for deleted visitors” on page 33

Conﬁguring AVP

The Installation and System Administration Guide discusses conﬁguring AVP in greater detail. Note,
also, the following changes in the "Commerce-speciﬁc conﬁguration" chapter of the Installation and
System Administration Guide:

l Under "AVP tax program," only the AVPIN variable need be deﬁned in bv1to1.conf;

AVPIN="1"

l The AVPIN variable must be deﬁned in the export section of bv1to1.conf. This will enable its

placement in the Windows system registry, HKEY_LOCAL_MACHINE/Software/
BroadVision/One-To-One Application System/4.1/def/export.

l Remove or comment-out the simple_tax_rate variable in bv1to1.conf.

Additionally, two environment variables affect the AVP taxing software. These should be deﬁned in
bv1to1.conf as well:

l $TAX_FROM_STATE speciﬁes the FromState parameter to calls to AVP. This is a two-letter U.S.A.

state name abbreviation, such as CA for California.

l $TAX_FREIGHTCODE speciﬁes the ProdCode parameter used when passing shipping costs to AVP
for tax calculation. This speciﬁes how freight charges get taxed; see the AVP documentation for
valid freight (product) codes. For example:

40000 - FOB Destination via Common Carrier Intrastate with No Option
to avoid freight charges
41150 - FOB Destination via Own Carrier Intrastate with Option to
avoid freight charges

When calculating taxes, One-To-One Commerce calls AVP for each line-item in the shopping
cart. To use the product-speciﬁc tax calculation, for each product set the MR_TAX_PRODCODE
database ﬁeld (“Product Tax Code”) to the ProdCode values speciﬁed by AVP. See the AVP
documentation for details.

This version of One-To-One Commerce includes AVP that does not support Canadian taxation.
See bug number 09447 under “Known problems and issues” on page 6.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

27

Conﬁguring CyberSource

See the CyberSource documentation for a complete description of the CyberSource payment
handler.

One-To-One Commerce supports the CyberSource Internet Commerce Services version ics3.0.1.1.
Follow these steps to conﬁgure this payment processor:

1. Install CyberSource ICS2 3.0.1.1

2. Set the environment variable.

export ICSPATH=C:/cybersource

3. Set the payment processing method in the $BV1TO1_VAR/etc/bv1to1.conf ﬁle. For both
the mr_pmthdlr_d and mr_pmtsettle_d processes, include the following speciﬁcation:

pmt_method=”cybersourceics2”

Also, set the payment processing methods for the services, which should include the following
speciﬁcation (for lack of space this is broken into two lines, but your speciﬁcation should not
contain any return characters):

pmt_methods=”0=cybersourceics2, 1=cybersourceics2, 2=cybersourceics2,

10001=po, 10002=po”

4. Deﬁne the library path for CyberSource ICS2. Edit the bv1to1.conf ﬁle, ﬁnd the following

lines, and add the last line as in this example:

BV_PATH=$getenv(BV1TO1) + "/bin"

+ ";" + $getenv(BV1TO1) + "/orbix/bin"
+ ";" + $getenv(BV1TO1) + "/orbix/bin"
+ ";" + $getenv(BV1TO1) + "/lib"
+ ";" + $getenv(BV1TO1) + "/lib/objects"
+ ";" + $getenv(BV1TO1) + "/orbix/lib"
+ ";" + $getenv(BV1TO1) + "/rogue/lib"
+ ";" + $getenv(ICSPATH)

5. Deﬁne the variables in the “CyberSource ICS2 variables” section of the bv1to1.conf ﬁle.

Variable

ICSPATH=

Default Value

Description

“C:/cybersource”

Top of the installed directory for the
CyberSource payment handler. It
should contain the following:

• /include/ics.h
• /lib/libics2.a
• /lib/libics2.so
• /keys/*crt
• /keys/*pvt
• /etc

cybersourceics2_merchant_id=

“ICS2Test”

Merchant identiﬁcation.

cybersourceics2_server_host=

“ics2test.ic3.com”

Server host.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

28

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

Variable

Default Value

Description

cybersourceics2_server_port=

“80”

Server port number.

cybersourceics2_merchant_ref_number= “07”

cybersourceics2_fraud_scoring=

cybersourceics2_fraud_cap=

“ON”

”500”

cybersourceics2_avs=

cybersourceics2_disable_avs=

cybersourceics2_product_table=

cybersourceics2_electronic=

“ “

“ “

“ “

“ “

Site-supplied number that can be
used for tracking. Set this to a ﬁxed
arbitrary number.

Support fraud scoring.

The transaction amount over which
fraud scoring will be triggered.

AVS request level ﬁeld for fraud
scoring.

Disable avs for fraud scoring.
Values are Y/N.

Speciﬁes the name of the list table
for product schema.

Speciﬁes the column in the list
table that tells if the product is
electronic.

cybersourceics2_offer_ﬂags=

“^score_threshold:50^sc
ore_category_time:Nor
mal:“

Speciﬁes the ﬂags added to each
product ﬁeld given to
CyberSource.

cybersourceics2_offer_column=

“ “

cybersourceics2_debug_ﬂag=

"ON"

Speciﬁes the column in the list
table that lists other offer ﬂags.

Set this ﬂag to "ON" to see the
credit card expiration month and
year.

6. Set the offer ﬂags (optional) according to the CyberSource installation instructions. If you are

using offer ﬂags at the product/item level, create the offer ﬂag table as a multi-value table. Use
the speciﬁcation from the $BV1TO1_VAR/dbschema/cybersource_ics2.src ﬁle, copying
that ﬁle to the name of your new table’s source ﬁle.

7. Continue “Existing One-To-One installations” on page 12, Step 11

or restart the site:

bvconf shutdown
bvconf execute

Conﬁguring the Shipping methods

A shipping conﬁguration ﬁle is a text ﬁle that deﬁnes one of the One-To-One Commerce Shipping
methods. The ﬁles all have names that end with “.ship”, and they all reside in the
$FABMSHIPCONFIG directory (as deﬁned during One-To-One Commerce installation).

Shut down the One-To-One system before installing a new shipping configuration file.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

29

Conﬁguration ﬁles contain lines of text that deﬁne properties of the shipping method. Most
properties require single line descriptions. However, some allow multiple lines terminated by a
single-line that begins with a ‘@’ character. For example:

# No-charge conditions.
NOCHARGE
ATTRIBUTE "FREESHIPPING"
PRODUCTID 200-wmsw-10
@

In the above example, the first line is a comment. There must be a space following the ’#’
character. Also, there must not be any additional spaces or lines following the ‘@’ character.

A shipping conﬁguration ﬁle has four parts:

l Required information that includes the shipping method name, a description, and how the

charges are calculated.

l Rates to charge based on a single rate, or based on a table of rates.

l Exceptions to make based on the destination location, product ID, or some other database

attribute. The charges may be adjustments, exclusions, inclusions, or “no charge” items. This
section is optional.

l Visibility conditions that determine whether or not a shipping method can be presented to the

visitor as a shipping option for the order.

The rest of this section describes these parts in detail.

Required information

A shipping method’s required information includes, in this order, the method name and type, a
description of the method, and how the charges are calculated.

# Name: A single line description that is unique to the site.
Ultra Shipping
# Type: 50 characters or less that define the type of method.
Ultra Shipping
# Description: One or more lines that describe the method.
My shipping method to be used by the Ultra system for
charges in the U.S.A. only.
@
# Cost factor: either WEIGHT, PRICE, QUANTITY, or NONE (the default).
PRICE

Name

Type

The name identiﬁes the method, but obsolete and no longer used by the system. However, you must
still deﬁne a name, usually with the same value as the Type deﬁnition.

Ultra Shipping

A single line that identiﬁes the shipping method to the system. This is a text string of less than 50
characters, and is the name that the visitor sees when this method is presented as a shipping option.

Ultra Shipping

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

30

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

To identify a shipping method as the default method for the site, assign the shipping method’s name
to the MR_SHIP_DEFAULT in the bv1to1.conf conﬁguration ﬁle, like this:

MR_SHIP_DEFAULT="Ultra Shipping"

Description

This is the “friendly” name that describes the shipping method. It can be one or more lines of text,
terminated by a line that contains a single ‘@’ character.

This is the Ultra shipping rate
for US shipping.
@

Cost factor

Identiﬁes how the shipping charges are determined. The text must be one of WEIGHT, PRICE,
QUANTITY, or NONE (the default).

WEIGHT

Rates

The rate deﬁnitions are the currency amounts to use when calculating shipping charges. Note that
“which” country’s currency is deﬁned for the site in the bv1to1.conf conﬁguration ﬁle.

CAUTION You must use U.S.A. currency format if you enter the values with the Shipping editor.

Every shipping method conﬁguration ﬁle must deﬁne a constant amount for the method’s “ﬁxed
rate” charge, even if the rate is zero; this entry is required. When a site is using the ﬁxed rate charge,
that is the value of the entire cost of the shipping for the order, regardless of the destination, count of
items, or any other factor. If this method doesn’t support ﬁxed rate charges, set this amount to 0.00.

# Fixed charge amount: Use 0.00 for "do not use this value".
0.00

Optionally, a shipping method can deﬁne either:

l a rate to apply to each item in the order, or

l a table of rates based on the count, weight, or price of items in the order.

To deﬁne a rate or table of rates, specify “# shipping rate” or “# shipping table”, followed
by the rate information, and terminate the deﬁnition with a line that contains a single ‘@’ character.
For example, to specify a rate of 9.99 to charge for each item, use this deﬁnition:

# shipping rate
9.99
@

To calculate the charge based on the count, weight, or price of items in the order, deﬁne a table of
range of items and the rate to charge. Each line of the table is in the form range rate. After the set
of valid rates, put “0 0” on a line by itself, and then terminate the table with a line that contains a

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

31

single ‘@’ character. After the terminator, deﬁne the “overcharged” amount and rate. In the
following example, the shipping cost for one item is 14.94 (9.99+4.95); for eight items is 18.94
(9.99+8.95); for nine items is 20.24 (9.99+10.00+(1*0.25));

# shipping table
2 4.95
4 5.95
6 7.95
8 8.95
0 0
@
10.00 0.25

An overcharge is the rate to apply when the order contains more items that are deﬁned by the highest
range value in the table. For example, in the deﬁnition above, when the order contains more than
eight items, the shipping system charges 10.00, and adds 0.25 for each additional item more than
eight; nine items cost 10.25, ten items cost 10.50, and so on.

Exceptions

Exceptions are additional adjustments that can increase or decrease a charge based on the order
destination, a product ID, or some other attribute of the order record. Each speciﬁc exception is a
line that begins with a keyword that identiﬁes the exception type. The type is followed by some
value, and for adjustments, it ends with an adjustment amount.

<exception_type> <value> [ <adjusted_amount> ]

<exception_type>

Identiﬁes the type of exception and is either:

ATTRIBUTE

A database attribute that is in the order record.

PRODUCTID

The ID of a product in the order.

LOCATION

The state or country of the order destination. This option is not
available for No Charge exceptions.

<value>

A string that speciﬁes what causes the exception.

ATTRIBUTE

A quoted string that is the name of the database attribute. The
attribute must appear in the order record.

PRODUCTID

The product ID as deﬁned in the product database record.

LOCATION

The location. See below for details.

<adjusted_amount> Currency amount to adjust the charge for this exception.

A location <value> is a state abbreviation, country identiﬁer, or a wildcard. If the name contains
spaces, enclose the string in quotes. The asterisk (‘*’) wildcard identiﬁes an exception for all
locations not in the same set. For example, the following assigns an adjustment value of 7.50 for all
locations not in the United Kingdom or Alaska:

AK

LOCATION
7.00
LOCATION "United Kingdom" 5.00
7.50
LOCATION

*

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

32

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

 Avoid country identifiers of less than three characters because these might be confused with
state names in the U.S.A. If the system sees a location that maps to a state name, it assumes the
location is in the U.S.A. For example, do not use “CA” for Canada because it would be
overridden by California.

Adjustments

An adjustment deﬁnes the amount to charge in addition to the other charges already applied. The
adjustment deﬁnitions must precede the Exclusion and Inclusion deﬁnitions, and must follow the
Rate deﬁnitions. You can have multiple adjustments or none, but you must terminate the
Adjustment section with a line that contains a single ‘@’ symbol.

# additional charges:
7.00
AK
LOCATION
LOCATION
7.00
HI
ATTRIBUTE "oversized" 5.00
PRODUCTID 12345
10.00
@

No charge

Items can be shipped free of charge based either on an item’s ID or some database attribute on the
order having a non-zero value. To deﬁne free shipping, begin the speciﬁcation with “NOCHARGE”,
and identify the attribute or product ID to ship free. For example, the following deﬁnes free
shipping for all products with a non-zero FREESHIPPING attribute, or for items with product “ID
200-wmsw-10”:

NOCHARGE
ATTRIBUTE "FREESHIPPING"
PRODUCTID 200-wmsw-10
@

Only the ATTRIBUTE and PRODUCTID conditions are valid with NOCHARGE; the LOCATION
condition is not valid.

Visibility conditions

Visibility conditions determine whether or not a shipping method can be presented to the visitor as
a shipping option for the order. The result of the condition determines if the method is excluded or
included when the system presents a list of shipping methods. Each condition is a line that begins
with a keyword that identiﬁes the condition type, and is followed by the value that must be met for
the condition to be true. The syntax of each condition is identical to the syntax of the deﬁnitions
described in “Exceptions” on page 31. See that description for details.

Exclusions

Exclusions identify conditions that would keep the system from presenting this shipping method.
For example, if the visitor’s order destination is Greenland, this method will not be presented as an
available shipping method:

EXCLUDE
LOCATION "Greenland"
@

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Supplemental information

33

Inclusions

Inclusions identify condition that would cause the system to present this shipping method as one
that is available to the visitor. For example, if the site used one speciﬁc shipping service to transport
all of its fragile items, the deﬁnition for the shipping method might contain this deﬁnition.

INCLUDE
ATTRIBUTE "FRAGILE"
@

Shipping editor

Included in the product is a utility that you can use to edit the contents of the shipping conﬁguration
ﬁles. The editor, shipSearch.cgi, is a CGI program and must be installed in your cgi-bin
directory. For information about using this editor, see $BV1TO1/merchant/examples/
shipedit/Readme.

 If your site is configuring shipping for non-U.S.A. locations, add the following line to the
shipEdit.cgi file.

export INTERNATIONAL_LOCATION; INTERNATIONAL_LOCATION="1"

The line must appear in the shipEdit.cgi ﬁle before the following command line:

$CGIBIN_DIR/shipEdit

You must use U.S.A. currency format (1234.56) if you enter the values with the Shipping editor.

Using the Ofﬁce Express sample data

See “Conﬁguring the HTTP server” on page 19 to set up your HTTP server to work with the sample
application.

To use the Ofﬁce Express sample application, point your browser to /oexpress/scripts/
oexpress.html or index.html under your script root directory.

First time visitors to Ofﬁce Express click one of the following under "Shopping for":

l Myself

l Home Ofﬁce

l Small Business

They then select the My Account menu and click on Register Now to register.

Purging contents for deleted visitors

Periodically you’ll want to remove the shopping lists and quotes that pertain to deleted visitors. The
following SQL statements accomplish these tasks.

Back-up your database before running these statements.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

34

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Removing One-To-One Commerce

Purging shopping lists

This statement purges deleted visitors from MR_SHOP_LIST_ITEMS.

delete from MR_SHOP_LIST_ITEMS where OID in (select a.OID from
MR_SHOPPING_LIST a, BV_USER b where a.DELETED = 0 and a.LIST_TYPE = 0 and
a.OWNER_ID = b.USER_ID and b.USER_STATE = 2);

This statement purges deleted visitors from MR_SHOPPING_LIST.

delete from MR_SHOPPING_LIST where DELETED = 0 and LIST_TYPE = 0 and
OWNER_ID in (select USER_ID from BV_USER where USER_STATE = 2);

Purging quotes

This statement purges deleted visitors from MR_QUOTE_ITEMS.

delete from MR_QUOTE_ITEMS where OID in (select a.OID from MR_QUOTES a,
BV_USER b where a.DELETED = 0 and a.USER_ID = b.USER_ID and b.USER_STATE
= 2);

This statement purges deleted visitors from MR_QUOTES.

delete from MR_QUOTES where DELETED = 0 and USER_ID in (select USER_ID
from BV_USER where USER_STATE = 2);

Removing One-To-One Commerce

To remove the One-To-One Commerce ﬁles and directories, and to uninstall the product, you need
to know the:

l Document root directory for your HTTP server.

l Script root directory for your Interaction Manager.

Begin by removing the ﬁles and directories.

Removing the One-To-One Commerce ﬁles and directories

To remove the One-To-One Commerce ﬁles and directories:

1. Shutdown the One-To-One servers and the Interaction Manager.

2. Remove the directory and ﬁles under the HTTP doc root:

/oexpress

Remove the doc root ﬁle<HTTP doc root>/oexpress.html.

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Removing One-To-One Commerce

35

3. Remove the directory and ﬁles under the script root:

/oexpress

4. Remove the directory and ﬁles under $BV1TO1_VAR/etc/shipping.conf

5. Remove the service OfficeExpress from bv1to1.conf (and WebStore if applicable).

When the script displays a message that the removal is complete, remove the conﬁguration settings,
described next.

Removing the conﬁguration settings

To remove the conﬁguration settings, edit the $BV1TO1_VAR/etc/bv1to1.conf conﬁguration
and remove these settings:

FABMSHIPCONFIG=$getenv(BV1TO1_VAR)+ "/etc/shipping.conf"
MR_MAIL_MESSAGE=$getenv(BV1TO1_VAR) + "/etc/purchase.msg"
MR_MAIL_CMD="/usr/lib/sendmail -o dq -f orders@YourStoreName.com"
MR_SHIP_ADDR_NAME= …
MR_SHIP_DEFAULT= …

After removing the conﬁguration information:

l If you are uninstalling One-To-One Commerce, proceed to the next step, “Removing the

One-To-One Commerce packages.”

l If you are leaving One-To-One Commerce installed, but not using it, proceed to “Restarting

One-To-One” on page 36.

Removing the One-To-One Commerce packages

Removing this version of One-To-One Commerce also removes the 4.0b patch to the One-To-One
servers by removing essential libraries from the installation. If you intend to continue running
One-To-One after uninstalling One-To-One Commerce, review all of the instructions in this section
before continuing.

To remove the One-To-One Commerce application packages installed by the install shield:

1. From the Start menu, choose Settings|Control Panel|Add/Remove Programs.

2. On the Install/Uninstall tab, select "BroadVision One-To-One Commerce 4.1.0" from the list of

applications installed on your system.

3. Choose Add/Remove, and follow the instructions as they appear on the screen.

If you have installed both One-To-One Business Commerce and Retail Commerce, removing
either one will cause the other to malfunction. Essentially you must remove both applications.

One-To-One Retail Commerce Release Notes

590-410-NAS

BroadVision, Inc.

36

One-To-One Retail Commerce Version 4.1.0 for Windows NT Installation and Release Notes
Removing One-To-One Commerce

Restarting One-To-One

After removing the One-To-One Commerce conﬁguration settings from bv1to1.conf, you need to
restart One-To-One with the execute command to effect the changes:

1. Restart the One-To-One servers:

$BV1TO1/bin/bvconf execute

2. Restart the Interaction Manager:

$BV1TO1/bin/imgr_conf -a start

BroadVision, Inc.

590-410-NAS

One-To-One Retail Commerce Release Notes

