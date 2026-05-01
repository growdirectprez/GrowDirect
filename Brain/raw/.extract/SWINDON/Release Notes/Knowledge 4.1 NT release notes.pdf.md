1

BroadVision One-To-One

Knowledge Version 4.1.0 for

Windows NT

Release Notes

This is Version 4.1.0 of BroadVision® One-To-One Knowledge™ for theWindows NT platform. This
document includes information about these topics:

l “Included in this release” on page 2.

l “License agreement” on page 2

l “Technical support” on page 2.

l “Documentation” on page 3.

l “System and software requirements” on page 4.

l “What’s new or changed in Version 4.1.0” on page 5.

l “Startup script parameters” on page 6.

l “Conﬁguring the bv1to1.conf ﬁle” on page 7.

l “Conﬁguring Alerts” on page 8.

l “Customizing Files” on page 10.

l “Before you install” on page 10.

l “Migrating from One-To-One Knowledge Version 3.0.0” on page 13.

l “Installing One-To-One Knowledge Version 4.1.0” on page 15.

l “Known One-To-One Knowledge problems and issues” on page 18.

l “Removing One-To-One Knowledge” on page 19.

This 4.1.0 release has been tested and certified to run on Windows NT 4.0.

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

2

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Included in this release

Included in this release

In addition to the One-To-One Knowledge system, this release includes:

l JavaScript interface ﬁles and libraries needed to write One-To-One Knowledge applications.

l Support for Verity Search’97, version 2.4.0. A license to use the Verity software is included with

this release.

License agreement

Use of the accompanying product is governed by the terms of your BroadVision license agreement,
which includes limits on the number of copies that may be installed and used. To simplify the
installation and use of this product, One-To-One is packaged with all available components on each
CD. This packaging does not imply permission to use more copies of the components than is
permitted by your license agreement.

Technical support

Technical Support services are provided on an annual basis to BroadVision customers. A standard
90-day warranty is also provided with all software.

If you experience problems in using any of BroadVision’s software products, contact BroadVision’s
World-wide Customer Support Organization for assistance. Registered customers who have a login
name and password can report problems via BroadVision’s Web site www.broadvision.com. On
the Web site you can access support-related technical information, report problems, and track report
status and responses on the Problem Reports pages. To request a login, please contact your
BroadVision Account Representative.

The Web site is the preferred method of reporting problems; however, if necessary you can report
problems via e-mail to bvhelp@broadvision.com. Please be sure to include the case ID when
communicating via e-mail.

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

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Documentation

3

BroadVision will support customers who use newer versions of third-party products by working
with the customer to resolve compatibility problems with the third-party vendor. BroadVision will
also consider, at our option, developing and releasing minor ﬁxes for our products in order to
resolve problems with new versions of third-party products.

Documentation

Documentation for One-To-One Knowledge is available electronically in HTML and PDF formats.
These release notes are available in print only.

From time to time BroadVision updates the electronic documentation and makes it available to
customers. If you are interested in receiving a notification when updates are available, please
send an e-mail message to bvpubs@broadvision.com, and put “subscribe knov41docs”
in the subject field. Notifications will be sent to the reply-address of the message.

To use the HTML or PDF documentation, you can either access it directly from the CD-ROM or from
the One-To-One Knowledge system directory. In your browser, enter the URL that points to the
contents.htm ﬁle.

l If you are using the Application CD-ROM as the target, assuming you are using drive E:, enter:

file:///E:/pubs/knowledge/usrguide/contents.htm
file:///E:/pubs/knowledge/devguide/contents.htm

l If you are using the installed files, enter the full path to the ﬁle, such as:

file:///D:/bv1to1/pubs/knowledge/usrguide/contents.htm
file:///D:/bv1to1/pubs/knowledge/devguide/contents.htm

Optionally, you can copy or link the tree into the document root of your HTML server.

To access the PDF (Portable Document Format) ﬁles, you will need a PDF viewer, such as Adobe’s
Acrobat Reader, which is available for free downloading from Adobe’s Web site at:

http://www.adobe.com/prodindex/acrobat/readstep.html

Additional BroadVision documents and white papers are available at:

http://www.broadvision.com

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

4

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
System and software requirements

System and software requirements

Installing and using One-To-One Knowledge requires:

l A server machine:

• running a new installation of the BroadVision One-To-One Enterprise Version 4.1.0 and

One-To-One Publishing Center Version 4.1.0

• that has access to a CD-ROM drive

• with an additional 110 MB of available hard disk space

l A client machine:

• with an additional 1.5 MB of available hard disk space for the client-side Java classes

automatically downloaded by the browser

• running Netscape Communicator Version 4.6 or Internet Explorer Version 5.0, or for
Japanese client machines, Netscape Communicator Japanese Version 4.6 or Internet
Explorer Version 5.0. BroadVision does not support other versions of these browsers for
running the One-To-One Knowledge

• with TCP/IP networking, or at least a 28.8 Kbps modem to run the application remotely

• that has a VGA monitor with a screen resolution of 800 x 600 or higher

l One-To-One Knowledge Administrator’s Guide also requires the One-To-One Publishing

Center and the BroadVision One-To-One Command Center™ applications.

Third party options

One-To-One Knowledge also supports the following third-party software options:

l Verity Search’97, version 2.4.0. Verity Search is installed when you install One-To-One

Knowledge; no separate license is required to use the Verity software included with this release.

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
What’s new or changed in Version 4.1.0

5

What’s new or changed in Version 4.1.0

Here are some of the new or improved features of the One-To-One Knowledge:

JavaScript navigation in components and scripts—One-To-One Knowledge Version 4.1.0 has replaced
its Java navagation applet with JavaScript. You can use the interface provided with the PC Inc.
sample, or you can create your own navigation controls.

Support for multi-level channel/program hierarchy—One-To-One Knowledge Version 4.1.0 supports
one or more levels of channels where each channel can contain any number of subchannels. Each
channel and subchannel can contain any number of programs. A program can also belong to more
than one channel.

Access to content in subcategories—In One-To-One Knowledge Version 3.0.0, when you create a
program in the Knowledge Admin Tool and choose a category as the source of content for the
program, the visitor sees all content in all subcategories under that category. The Version 4.1.0
Knowledge Admin Tool lets you choose between:

l all content directly in that category

l all content directly in that category plus all content directly in any descendant subcategory of

that category

Support for broadcast attributes—Broadcast attributes (classiﬁers and qualiﬁers) are a new feature of
One-To-One Knowledge Version 4.1.0. The sample data included with One-To-One Knowledge
Version 4.1.0 demonstrates the use of this feature.

Support for user-defined content types—One-To-One Knowledge Version 3.0.0 only supported one
content type: Editorials. One-To-One Knowledge Version 4.1.0 supports any content type, including
user-deﬁned content types.

Support mixing of content types in a channel—Each program is limited to retrieving content from a
single content type, but different programs in the same channel can get content from different
content types. A channel in a One-To-One Knowledge site can display content from different
content types via different programs.

Integration with 4.1 Verity search—One-To-One Knowledge Version 4.1.0 uses the BroadVision
One-To-One Enterprise Version 4.1 Verity search, which supersedes the Verity search built into
One-To-One Knowledge Version 3.0.0.  The BroadVision One-To-One Enterprise Version 4.1 Verity
search has additional functionality, such as the ability to restrict the search to speciﬁed attributes
and to do sorting.

One-To-One Knowledge Version 4.1.0 supports Verity search on content, but not on channels
and programs.

Alert notification by e-mail—One-To-One Knowledge Version 4.1.0 uses the BroadVision One-To-One
Enterprise Version 4.1 alert server, which supersedes the alert server built into One-To-One
Knowledge Version 3.0.0. The user proﬁle includes an attribute for choosing either inbox alerts or
both inbox and e-mail alerts.  The Set Alert button in the content page delivers the alert notiﬁcation
according to what the visitor chose in his or her proﬁle.

When the alert is on a content item, the visitor receives one e-mail each time the content is modiﬁed,
up to the frequency of the alert scheduled in the Command Center.  For example, if the alert is
scheduled for once a day, and the content is modiﬁed twice that day, the visitor only gets one e-mail
alert that day.

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

6

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
What’s new or changed in Version 4.1.0

When the alert is on a program, the visitor receives one e-mail alert, as well as an alert notiﬁcation
message in his or her inbox, each time content is added or modiﬁed in that program up to the
frequency of the alert scheduled in the Command Center.  For example, if the alert is scheduled for
once a day, and three content items are added or modiﬁed in that program during the day, the
visitor only gets one e-mail alert, as well as an alert notiﬁcation message in his or her inbox that day,
and it contains the names of the content.  If content is modiﬁed more than once in the program that
day, the content name appears only once in the alert.

Sample application—The sample application PC Inc. is shipped with One-To-One Knowledge
Version 4.1.0. You can modify the interface to suit your own site, or you can plug in your own user
interface.

Internationalization support—One-To-One Knowledge Version 4.1.0 has been internationalized and
tested with 3 character sets - English, Japanese, and German.

Ability to create a custom home page script for each user template—The Knowledge Admin Tool lets
the Channel Administrator associate a custom home page script with a user template.

Program type changes—In One-To-One Knowledge Version 3.0.0, when a program was created of a
particular program type, the program type’s icon and program template were copied into the
program.  Further changes to the program type’s template did not propagate to the programs
already created.  In One-To-One Knowledge Version 4.1.0, the program type does not store an icon
or script; instead, the program stores its script. Program icons are no longer used.

Support for rule sets categories— One-To-One Knowledge Version 4.1.0 now has an attribute in the
program type table for storing a rule set category. The interface for adding and modifying programs
created from that program type shows only rule sets in that category and all of its subcategories to
the visitor instead of all rule sets in the content type (the rule set speciﬁes what content is shown in
the program).

Control over community rules and access groups—Community rules are now created using the
One-To-One Command Center; creation of access groups is now done using the One-To-One
Publishing Center. (These were both automatically generated in One-To-One Knowledge 3.0.0.)

Startup script parameters

The startup script is $BV1TO1_VAR/lib/script_library/bv_km_utils.js. When you enter
“imgr_conf -a configure”, imgr_conf assumes your script library path is $BV1TO1/
script_library:$BV1TO1_VAR/lib/script_library. You can add additional directories,
but do not remove either of those two directories from your script library path.

The variables and functions in the script are:

km_service_name

Set this variable to the name of the service where you are running your
One-To-One Knowledge site. The Knowledge Admin Tool looks at this
variable and connects to that service. The default value for this variable
is PC Inc., the service name of the sample application that ships with
One-To-One Knowledge 4.1.0. Note that only one service in a site can
be running One-To-One Knowledge.

km_default_channel_page

This is the default value for the Add Channel form Channel Start Page
script.

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
What’s new or changed in Version 4.1.0

7

km_default_program_page

This is the default value for the Add Program form Program Start Page
script.

km_default_home_page

This is the default value for the Add User Template form Home script
parameter.

bv_km_build_inclusion_list()

Edit this function to specify which content types area available in the
knowledge site. The Knowledge Admin Tool uses this function to restrict
programs and preset bookmarked content to just those content types.
For example, if your knowledge site has content from Products,
Editorials, plus one of your custom content types, edit this function to
have only those three content types. This function controls what
choices appear in the content type picker for choosing the preset
bookmarked content in the Knowledge Admin Tool in the Add Program
Type, Add User Template, and Edit User Template forms. For example:

in_list.append(“PRODUCT”);
in_list.append(“AD”);
...
in_list.append(“MY_CUSTOM_CONTENT_TYPE”);

Conﬁguring the bv1to1.conf ﬁle

To better support One-To-One Knowledge, and to support new features, the bv1to1.conf
conﬁguration ﬁle contains these new settings. To see examples of the use of these settings, look at
the $BV1TO1/knowledge/examples/bv1to1.conf.example ﬁle.

New setting

cmc_http_docroot

enable_km_access_controls

Description

Set this parameter in bv1to1.conf to the full
path of your document root to view external ﬁles in
the PC Inc. sample site.

When set to “1”, read permission is checked (using
Publishing Center access controls) before content
is displayed in the knowledge site. When set to “0”,
all content is readable in the knowledge site by
everyone. The default value is “1” when this
parameter is not set in bv1to1.conf. (This was
called enable_kwa_access_controls in previous
releases of One-To-One Knowledge.)

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

8

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
What’s new or changed in Version 4.1.0

New setting

enable_km_classiﬁers

km_alert_content_type

km_user_cache_size

Description

When set to “1”, channels and programs in the
knowledge site are ﬁltered based on classiﬁers and
qualiﬁers. When set to “0”, all channels and
programs are visible to all visitors in the knowledge
site (no ﬁltering is performed). The default value is
“0” when this parameter is not set in
bv1to1.conf.

This parameter speciﬁes which content types the
One-To-One Knowledge alert plug-in processes to
get alerts. The value is a comma-separated list of
content type names with no white space allowed
around the commas, for example,
km_alert_content_type=”PRODUCT,EDIT
ORIAL”. In addition, the knowledge site must
check this parameter and not display the Set Alert
button in the content display script if the content is
not in a content type speciﬁed in this parameter.
When this parameter is not set in bv1to1.conf,
One-To-One Knowledge defaults to allowing alerts
on the following standard content types that ship
with BroadVision One-To-One Enterprise Version
4.1:

PRODUCT, AD, EDITORIAL, INCENTIVE,
DISCUSSION, TEMPLATE

This parameter conﬁgures the size of the One-To-
One Knowledge cache for storing visitors’
bookmarks, as well as classiﬁers and qualiﬁers
settings. The value is the number of visitors kept in
the cache. The default value is “500” when this
parameter is not set in bv1to1.conf.

Conﬁguring Alerts

The PC Inc. sample application has alerts already conﬁgured. Follow these instructions to conﬁgure
alerts when you are running One-To-One Knowledge in your own service:

1. Set the km_alert_content_type parameter in the bv1to1.conf ﬁle to the content types

you want visitors to be able to set alerts on in your service.

There are two types of alerts a visitor can set:

• on a content item

• on a program, where the program can only reference a category or content item

2. Either deﬁne a message script ﬁle for generating the text that goes into the alert inbox and the

text sent as e-mail when a content alert ﬁres, or modify $BV1TO1_VAR/msg_scripts/
km_content_alert.jsp. If the bv_schedule_script_root parameter in your
bv1to1.conf ﬁle is not set to $BV1TO1_VAR/msg_scripts, copy the message script ﬁle to
your bv_schedule_script_root directory.

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
What’s new or changed in Version 4.1.0

9

3. Deﬁne a message script ﬁle for generating the text that goes into the alert inbox and the text that

is sent as e-mail when a program alert ﬁres, or modify $BV1TO1_VAR/msg_scripts/
km_category_alert.jsp. If the bv_schedule_script_root parameter in your
bv1to1.conf ﬁle is not set to $BV1TO1_VAR/msg_scripts, copy the message script ﬁle to
your bv_schedule_script_root directory.

4. Use the One-To-One Command Center to create two visitor messages: one for your One-To-One
Knowledge content alerts, and one for your One-To-One Knowledge program alerts. The visitor
messages reference your message script ﬁles:

a. Login to the One-To-One Command Center in your service.

b. Click Notifications.

c. Click Visitor Messages.

d. Add a new visitor message (for example, “Content Alert Message”), select On-line, select

Yes for “Personalized Message”, External File for “Message Form”, select a ﬁle for “Message
Script File Path”. Use /km_content_alert.jsp if you want to use the content alert
message script that ships with One-To-One Knowledge. The One-To-One Knowledge
example message script is in $BV1TO1_VAR/msg_scripts.

e. Add a new visitor message (for example, “Program Alert Message”), select On-line, select
Yes for “Personalized Message”, External File for “Message Form”, and select a ﬁle for
“Message Script File Path”. Use /km_category_alert.jsp if you want to use the
program alert message script that ships with One-To-One Knowledge. The One-To-One
Knowledge example message script is in $BV1TO1_VAR/msg_scripts.

5. Use the Command Center to create two alert schedules: one for your One-To-One Knowledge
content alerts, and one for your One-To-One Knowledge program alerts. The content alert
schedule must reference the content alert visitor message, and the program alert schedule must
reference the program alert visitor message:

a. Login to the One-To-One Command Center in your service.

b. Click Notifications.

c. Click Alert Schedules.

6. Add a new alert schedule named “KWA Content Schedule” using the alert schedule wizard and
select “Alert for Latest Content Updates” in the alert type drop-down menu, “InBox” as the
delivery type, and “Content Alert Message” (the visitor message you created earlier) as the
message for the alert schedule. Select your desired alert schedule frequency in the wizard, then
make sure the alert is On-line. Simultaneous e-mail delivery is handled by the alert message script
in Visitor Messages.

7. Add a new alert schedule named “KWA Program Schedule” using the alert schedule wizard

and select “Alert for New Content Add to a Category” in the alert type drop-down menu, pick
InBox as the delivery type, and select “Program Alert Message” (the visitor message you
created earlier) as the message for the alert schedule. Pick your desired alert schedule frequency
in the wizard, then make sure the alert is On-line. Simultaneous e-mail delivery is actually
handled by the alert message script in Visitor Messages.

The following scripts in the PC Inc. sample application use alerts:

$BV1TO1_VAR/msg_scripts/km_category_alert.jsp
$BV1TO1_VAR/msg_scripts/km_content_alert.jsp
script_root/knowledge/scripts/alerts.jsp
script_root/knowledge/scripts/content.jsp
script_root/knowledge/scripts/editorialcontent.jsp
script_root/knowledge/scripts/productcontent.jsp

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

10

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Before you install

Customizing Files

In addition to the ﬁles covered in the previous sections ($BV1TO1_VAR/lib/script_library/
bv_km_utils.js and $BV1TO1_VAR/etc/bv1to1.conf), you can conﬁgure the following ﬁles:

File

Description

$BV1TO1_VAR/msg_scripts/km_content_alert.jsp

$BV1TO1_VAR/msg_scripts/km_category_alert.jsp

script_root/knowledge/admin/scripts/userprofupdate.jsp

used by the PC Inc. content alerts to
generate the text put in the alert inbox and
the text sent by e-mail when the content
alert ﬁres

used by the PC Inc. program alerts to
generate the text put in the alert inbox and
the text sent by e-mail when the program
alert ﬁres

used by the admin tool as the proﬁle editor
when the admin clicks the Proﬁle link in the
user admin section of the admin tool

Before you install

You must install BroadVision One-To-One Enterprise Version 4.1 and One-To-One Publishing
Center Version 4.1.0 before you install One-To-One Knowledge Version 4.1.0.

Installing patches You must install the H base patch or higher before running the knowledge_setup script. Check the
Support area of http://www.broadvision.com for the latest patch, or install patch H from the CD-
ROM by running /windows/server_v4.1H/setup.exe. The version ﬁle describing the ﬁxes in
the patch is available on the CD-ROM at /windows/server_v4.1H/svr410-h-n.txt.

To install the patch ﬁle:

1. Reboot your machine.

2. Make sure imgr and bvconf are shut down.

3. Run setup.exe.

4. Click Finish at the end to read the readme ﬁle.

If you are installing these products for the ﬁrst time, refer to the following documents for
instructions:

l Installation and System Administration Guide, Version 4.1.

l BroadVision One-To-One Enterprise Version 4.1 for Windows NT Server Release Notes.

l One-To-One Publishing Center Version 4.1.0 for Windows NT Installation and Release Notes.

CAUTION Never:

• hard code database passwords in the bv1to1.conf conﬁguration ﬁle. Enter passwords in

response to a prompt in the conﬁguration ﬁle

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

Notiﬁcation system

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Before you install

11

When setting up a notiﬁcation system, copy sched_header.jsp into the directory
bv_schedule_script_root deﬁned in the bv1to1.conf ﬁle. There is a default copy in
$BV1TO1/lib. To implement a custom delivery method, edit the sched_header.jsp ﬁle.

When you load the PC Inc. sample application using the knowledge_setup script, the sample
message scripts km_content_alert.jsp and km_category_alert.jsp are copied from
$BV1TO1/knowledge/alerts to $BV1TO1_VAR/msg_scripts.

If bv_schedule_script_root is not set to $BV1TO1_VAR/msg_scripts, copy the One-To-One
Knowledge message scripts to your bv_schedule_script_root directory.

What knowledge_setup does to your ﬁle system and database

The knowledge_setup makes the following changes to the One-To-One database:

l It creates a directory called $BV1TO1_VAR/dbschema/tmp containing temporary ﬁles used by

the schema generator.

l It extends the proﬁle schema. The knowledge_setup script creates a BV_KM_UPROF table of

additional user proﬁle attributes.

l It creates four new content types and a total of 16 new database tables, all of which begin with

the preﬁx BV_KM_. It also adds a row to the BV_SCHEMA_VERSIONS table to record the
One-To-One Knowledge version number.

l It creates the following directories and copies ﬁles into them:

document_root/knowledge
document_root/webapps/knowledge
script_root/knowledge

l It copies kmadmin.html to document_root.

l It copies pcinc.html to document_root if you say “y” to loading sample data.

l It creates the following directories and copies sample data ﬁles into them:

$BV1TO1_VAR/pcinc_data (only when the sample data is loaded)
$BV1TO1_VAR/collection (used by the Verity indexer)

l When you load the sample data, it creates two matching rule sets named “Instant publisher
matching rule set” and “Instant ﬁnd matching rule set” and two categories named “Instant
publishing forms” and “Instant ﬁnd forms” in the SCRIPT content type in the PC Inc. service.

l When you load the sample data, knowledge_setup:

• loads sample content into the BV_PRODUCT, BV_EDITORIAL, and BV_SCRIPT tables

• creates sample categories in Product, Editorial, and Script content types

• loads sample subtypes, instant publisher forms, and instant ﬁnd forms

• creates sample user accounts

• loads sample user templates, channels, programs, and program types

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

12

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Before you install

Before you run knowledge_setup

Make sure:

l you know the database password

l you know the path to your document root directory for your HTTP server

l you know the path to your script root directory for the Interaction Manager

l the BroadVision One-To-One Enterprise servers are running

l the Interaction Manager is shut down

l you are logged into the root host if installing One-To-One Knowledge on a multi-system

conﬁguration

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Migrating from One-To-One Knowledge Version 3.0.0

13

Migrating from One-To-One Knowledge Version 3.0.0

You must migrate the base product before you can install One-To-One Publishing Center or
One-To-One Knowledge.

Follow these instructions to migrate your Version 3.0.0 One-To-One Knowledge installation to
Version 4.1.0:

CAUTION You must install BroadVision One-To-One Enterprise patch 4.1H or higher before you
begin migration of your BroadVision One-To-One Enterprise, One-To-One Publishing Center,
and One-To-One Knowledge.

1. Backup your $BV1TO1_VAR, document_root, and template_root directories, as well as

your BroadVision One-To-One Enterprise database.

2. Migrate your Version 3.0 BroadVision One-To-One Enterprise installation to Version 4.1. Refer

to these documents for instructions:

• Installation and System Administration Guide, Version 4.1.

• BroadVision One-To-One Enterprise Version 4.1 for Windows NT Server Release Notes.

3. Migrate your Version 3.0.0 One-To-One Publishing Center to Version 4.1.0. Refer to the

One-To-One Publishing Center Version 4.1.0 for NT Installation and Release Notes for instructions.

If you need to migrate from versions earlier than those specified in Step 2 and Step 3, refer to
the appropriate versions of the cited documents for instructions.

4. Install One-To-One Knowledge Version 4.1.0. Follow the instructions under “Installing

One-To-One Knowledge Version 4.1.0” on page 15.

5. Run the script $BV1TO1/knowledge/knowledge_setup, answering “y” to the prompt for

setting up the application, “n” to the prompt for loading the sample data, and “y” to the prompt
for migration.

After knowledge_setup completes, all channels, programs, program types, and user
templates (formerly user types) from your Version 3.0.0 One-To-One Knowledge site are
migrated to the One-To-One Knowledge 4.1.0 schema.

6. All migrated programs are assigned a Version 4.1.0 program type named KM410 Default Program
Type. One-To-One Knowledge Version 4.1.0 program types have a rule set category; take the
rule sets used by your 3.0.0 programs and put them into the rule set category KM410 Default Rule
Set Category.

7. Replace the PC Inc. sample scripts with your own custom scripts for your service.

When a site is migrated to One-To-One Knowledge Version 4.1.0, it initially uses the sample channel
scripts, sample program scripts, sample user template home scripts, and sample content display
scripts from PC Inc. to display your migrated channels, programs, home pages, and content.

The script $BV1TO1/knowledge/knowledge_setup makes the following modiﬁcations to your
environment:

l The ﬁle document_root/service_name_410.html is created for logging into your

migrated site.

l The log ﬁle $BV1TO1_VAR/logs/hostname/km410_migration.log is created; it contains

information on what was migrated.

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

14

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Migrating from One-To-One Knowledge Version 3.0.0

l The variable km_service_name variable in the startup script

$BV1TO1_VAR/lib/script_library/bv_km_utils.js is modiﬁed to cause the script
document_root/kmadmin.html to log into the migrated service.

The following table shows how channels and programs are converted by the migration process:

One-To-One Knowledge Version 3.0.0

One-To-One Knowledge Version 4.1.0

Directory Channel

Home Channel

Service Channel

a Version 4.1.0 channel

a Version 4.1.0 channel

not represented as a channel in Version 4.1.0;
instead, use a script to display links. The sample
application PC Inc. uses links in the Tools page

Program (other than a Home Program)

a Version 4.1.0 program

Subscribed Channel

a bookmarked channel in the bookmarks dialog

Subscribed Program (also called a Home Program) a bookmarked program in the bookmarks dialog

Required Home Program (including
Announcements, Events, and Editorials)

Favorite

Default Subscribed Channel

Default Subscribed Program

Default Favorite

Alert Program

a Version 4.1.0 program in the Version 4.1.0
channel representing the Version 3.0.0 Home
Channel

a bookmarked content in the bookmarks dialog

a preset bookmarked channel of the user template

a preset bookmarked program of the user template

a preset bookmarked content of the user template

Alert Inbox

In addition, migrating from 3.0.0 to 4.1.0 causes all programs to default to a new program type. The
Program Type in One-To-One Knowledge Version 4.1.0 is different from One-To-One Knowledge
Version 3.0.0. In One-To-One Knowledge Version 4.1.0, the ﬁelds RuleSetCategory and Content Type
in program types cannot be edited. The Content Type for a Program Type in One-To-One Knowledge
Version 3.0.0 is always Editorial; there is no ﬁeld for RuleSetCategory in One-To-One Knowledge
Version 3.0.0.

The migration sets all migrated Program to a default program to force the site administrator to
create new program types.

Directory structure after migrating

The knowledge_setup script adds two new directories off the script_root/knowledge
directory, scripts and admin/scripts. All other directories and their contents from your
previous version remain unchanged.

script_root/knowledge/scripts
document_root/knowledge/admin/images
script_root/knowledge/admin/scripts
document_root/knowledge/images

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Installing One-To-One Knowledge Version 4.1.0

15

Installing One-To-One Knowledge Version 4.1.0

The setup.exe program on the CD-ROM automatically installs One-To-One Knowledge. To run
the installation procedure in this section you must be logged on to Windows NT as the owner of the
BroadVision One-To-One Enterprise application ﬁles. Although you use the Windows interface to
run the setup.exe program, you need MKS Korn shell windows (from MKS Toolkit) for running
the One-To-One Knowledge scripts and utilities.

To install One-To-One Knowledge:

1. Login as the owner (installer) of the BroadVision One-To-One Enterprise application ﬁles.

2. Run setup.exe from the /windows/Knowledge directory on the One-To-One Knowledge

CD-ROM.

3. Follow the instructions on your screen to install One-To-One Knowledge version 4.1.0.

The setup.exe installer tells you when the installation is done.

4. Click the Finish button

After setup.exe installs several ﬁles, it asks you to read the text ﬁle accompanying the
application. The ﬁle is located in:

$BV1TO1/bin/versions/kno410-b-n.txt

When setup.exe ﬁnishes the installation it points you to any further ﬁles you need to read.

5. Set up the conﬁguration ﬁle $BV1TO1_VAR/etc/bv1to1.conf:

l If you are performing a clean install (you do not have a preexisting BroadVision One-To-One

Enterprise site), you can copy the example conﬁguration ﬁle:

% cd $BV1TO1/knowledge/examples
% cp bv1to1.conf.example $BV1TO1_VAR/etc/bv1to1.conf

l The $BV1TO1_VAR/etc/bv1to1.conf ﬁle already exists if you have a preexisting

BroadVision One-To-One Enterprise site. In that case, use the example ﬁle
$BV1TO1/knowledge/examples/bv1to1.conf.example to copy sample conﬁgurations
for One-To-One Knowledge and paste them into your existing bv1to1.conf ﬁle. When
conﬁguring the bv1to1.conf ﬁle, set the following parameters:

• Access control—enable_km_access_controls

If enable_km_access_controls is “1” (the default), read access permission is checked
in One-To-One Knowledge using One-To-One Publishing Center. If
enable_km_access_controls is “0”, all content in One-To-One Knowledge is readable.

enable_km_access_controls="1"

This was called enable_kwa_access_controls in previous releases of One-To-One
Knowledge.

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

16

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Installing One-To-One Knowledge Version 4.1.0

• Classiﬁers and qualiﬁers—enable_km_classifiers

If enable_km_classifiers is “1”, channels and programs in the site are ﬁltered for
visitors, based on classiﬁers and qualiﬁers. If enable_km_classifiers is “0”, all
channels and programs are displayed to visitors.

enable_km_classifiers="1"

• Content Types that you can put alerts on—km_alert_content_type

Set this parameter to specify which content types the One-To-One Knowledge alert plug-in
processes to get alerts. The value is a comma separated list of content type names, with no
white space allowed around the commas.

km_alert_content_type="PRODUCT,EDITORIAL"

• One-To-One Knowledge visitor cache size—km_user_cache_size

Conﬁgure the size of the cache for storing visitors’ bookmarks and classiﬁers and qualiﬁers
settings. The value is the number of visitors kept in the cache.

km_user_cache_size="500"

• Enable e-mail alert notiﬁcations—daemon deliv_smtp_d

In this section of the ﬁle, the offline parameter exists only on Windows NT systems. This
must be set to 0 for alert e-mail notiﬁcations to work.

daemon deliv_smtp_d {

parameter
shutdown="bvkill -w 2 USR1"    # Shutdown command.
id="1"                  # ID of this delivery server.
delay="600"             # Seconds to wait after being launched.
sleep="120"             # Seconds to wait between polls.
msg_delay="30"          # Seconds to wait between (50) messages.
offline="0"             # enable alert e-mail notifications

}

Make sure bv_email_host either points to a valid e-mail server or, if kept as “localhost,”
make sure your Windows NT system has an e-mail service installed. For example:

bv_email_host="my_mail_host.my_domain_name.com"

6. Start the BroadVision One-To-One Enterprise servers.

Shut down the BroadVision One-To-One Enterprise servers, and then start them back up for the
conﬁguration changes to take effect. Do not start the Interaction Manager.

% $BV1TO1/bin/bvconf shutdown
% $BV1TO1/bin/bvconf execute

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Database purge utility

17

7. Setup One-To-One Knowledge.

If the Interaction Managers are running, you must shut them down before running
knowledge_setup:

% $BV1TO1/bin/imgr_conf -a stop

Run the One-To-One Knowledge setup utility and follow the directions it provides:

% cd $BV1TO1/knowledge
% ./knowledge_setup

8. Start the Interaction Managers:

% $BV1TO1/bin/imgr_conf -a start

The first time you define a classifier, you need to stop and restart the session manager to make
broadcast attributes take effect.

Database purge utility

When you delete bookmarked content, the bookmark tables still contain an entry for the deleted
content.

To remove entries in the bookmark table that correspond to deleted content items, use the utility
$BV1TO1/bin/km_purger. To invoke this utility, enter:

% $BV1TO1/bin/km_purger service_name

You can run km_purger from the MKS UNIX command line or enter it into the Windows NT
Schedule service using the at command.

For example, to remove bookmarks to deleted content items in the PC Inc. service, enter:

sh bv1to1_path/bin/km_purger PCInc

where bv1to1_path is the hard-coded path to your BroadVision One-To-One Enterprise
installation.

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

18

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Known One-To-One Knowledge problems and issues

Known One-To-One Knowledge problems and issues

Please note the following One-To-One Knowledge problems and issues:

One-To-One Knowledge Administrator’s Guide

l 08896: The Add User Template form illustration shows two Status lines; the Knowledge Admin

Tool only has one Status line.

One-To-One Knowledge Developer’s Guide

l 08894: The sample home page scripts in the PC Inc. sample shows alerted program links even if
the program's classiﬁers and qualiﬁers don't match the visitor’s. This problem can be corrected
by modifying the home page scripts to call program.isVisible(userId) and hiding links
to programs that don't match the visitor’s classiﬁers and qualiﬁers.

l 09000: If you plan to load the PC Inc. sample data, make sure “.” (the current directory) is in

your path before running the knowledge_setup script.

l 09252: In the PC Inc. example application, the content.jsp script checks for the content type
of the given content item (contentTypeName == "Editorial"). In a Japanese locale, the
English friendly name must be translated to Japanese, otherwise the content.jsp script
produces an empty page.

l 09268: The e-mail alerts in the PC Inc. example are sent out in EUC. Windows e-mail clients

typically require Shift-JIS. E-mail must therefore be converted to Shift-JIS before being sent to a
Windows client.

l 09441: After deleting a channel that is a root level channel of a user template, a bvlog error
message similar to the following appears every time you visit the home page of that user
template:

Thu Sep 02 15:05:12 1999 (936309912.353906)
bvsmgr[3427]@achird:<25>:L1:S08 get_channel_by_id() :
get_cat_entry_by_oid()failed for channel_id = -8221
Thu Sep 02 15:05:12 1999 (936309912.354052)
bvsmgr[3427]@achird:<25>:L1:S08 get_channel_by_id_() failed for id=-
8221. status=-1

There are two workarounds for this problem:

a. Remove the channel from the root channel list of the user template before deleting the root

channel.

or

b. If you have already removed the root channel, edit the user template and save it without

making any changes.

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Removing One-To-One Knowledge

19

Removing One-To-One Knowledge

To remove the One-To-One Knowledge application ﬁles and directories, and to uninstall the
product, you need to know the:

l Document root directory for your HTTP server.

l Script root directory for your Interaction Manager.

Begin by removing the ﬁles and directories.

Step 1: Remove One-To-One Knowledge ﬁles and directories

To remove One-To-One Knowledge ﬁles and directories:

1. Login as the owner of One-To-One application ﬁles.

2. Shut down the One-To-One Knowledge servers and the Interaction Manager.

% $BV1TO1/bin/imgr_conf -a stop
% $BV1TO1/bin/bvconf shutdown

3. Back up all One-To-One ﬁles and directories.

Step 2: Remove conﬁguration settings for One-To-One Knowledge

To remove One-To-One Knowledge conﬁguration settings, edit the
$BV1TO1_VAR/etc/bv1to1.conf ﬁle and remove the settings you added when you installed
One-To-One Knowledge. Refer to “Conﬁguring the bv1to1.conf ﬁle” on page 7 for the exact settings
to remove.

Step 3: Remove data ﬁles for One-To-One Knowledge

When you installed One-To-One Knowledge, the setup program modiﬁed database schema and
values. Refer to “What knowledge_setup does to your ﬁle system and database” on page 11 for
more information about data ﬁles.

Step 4: Remove the One-To-One Knowledge database tables

Use SQL to manually drop all of the tables whose names begin with “BV_KM_”.

Step 5: Remove the One-To-One Knowledge installation

To remove the One-To-One Knowledge software libraries:

1. From the Start menu, choose Settings | Control Panel.

2. Click Add/Remove Programs.

3. On the Install/Uninstall tab, select BroadVision One-To-One Knowledge 4.1.0 from the list of

applications installed on your system.

4. Click Add/Remove and follow the instructions on your screen.

One-To-One Knowledge Release Notes

890-410-NAS

BroadVision, Inc.

20

BroadVision One-To-One Knowledge Version 4.1.0 for Windows NT Release Notes
Removing One-To-One Knowledge

Step 5: Restart the One-To-One application

After you modify the bv1to1.conf ﬁle, restart One-To-One Knowledge and the Interaction
Manager:

% $BV1TO1/bin/bvconf execute
% $BV1TO1/bin/imgr_conf -a start

BroadVision, Inc.

890-410-NAS

One-To-One Knowledge Release Notes

