---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Release Notes/Knowledge 4.1 NT release notes.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Knowledge 4.1 NT release notes.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Release Notes/Knowledge 4.1 NT release notes.pdf.md`
Size: 44,488 bytes

## Raw content
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

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
