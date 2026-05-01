---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Release Notes/Publishing Centre 4.1 NT release notes.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Publishing Centre 4.1 NT release notes.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Release Notes/Publishing Centre 4.1 NT release notes.pdf.md`
Size: 73,259 bytes

## Raw content
1

One-To-One Publishing Center™
version 4.1.0 for NT Installation and

Release Notes

This is version 4.1.0 of the BroadVision® One-To-One Publishing Center for the Windows NT
operating system. This release consists of:

l A CD-ROM that includes the One-To-One Publishing Center application and sample data. The
application includes HTML and PDF user documentation accessed from the application Help
command.

l The One-To-One Publishing Center User’s Guide, which is available in HTML and PDF form
accessed from the CD-ROM. See “Documentation” on page 3 for instructions on using this
guide.

l The One-To-One Publishing Center Developer’s Guide, which is available in HTML and PDF form
accessed from the CD-ROM. See “Documentation” on page 3 for instructions on using this
guide.

l These release notes contain information about installing, conﬁguring, and starting the

One-To-One Publishing Center. These release notes also describe known problems and issues,
and discuss supplemental information not included in the documentation.

• “‘BroadVision technical support” on page 2.

• “License agreement” on page 2.

• “System and software requirements” on page 3.

• “Documentation” on page 3.

• “Changes in version 4.1.0 Publishing Center” on page 4.

• “Problems ﬁxed in this release” on page 6.

• “Problems in this release” on page 7.

• “Migrating from version 3.0.0 to version 4.1.0” on page 8.

• “How cstudio_setup affects the ﬁle system and database” on page 11.

• “Installation and conﬁguration procedures” on page 13.

• “Multiple machine installations” on page 20.

• “Database and ﬁle system considerations” on page 21.

• “Optional application conﬁguration” on page 22.

• “Enabling the Find button for related content items” on page 26.

• “Optimizing application performance” on page 28.

• “Scheduling background processes” on page 28.

• “Removing the One-To-One Publishing Center” on page 29.

 In these release notes, forward slashes (/) are frequently used instead of backslashes (\), since
commands are typically performed in a MKS Toolkit shell instead of native Windows NT.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

2

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

‘BroadVision technical support

Technical Support services are provided on an annual basis to BroadVision customers. A standard
90-day warranty is also provided with all software.

If you experience problems using BroadVision software products, contact the BroadVision World-
wide Customer Support Organization for assistance. Registered customers who have login names
and passwords can report problems via the BroadVision Web site at www.broadvision.com. On
the Web site, you can use the Problem Reports pages to access support-related technical
information, report problems, track problem status, and check responses. Telephone contact
information for BroadVision Customer Support is also provided on the site. Contact your
BroadVision Account Representative to request a login name and password.

The Web site is the preferred method of reporting problems. When necessary, you can also report
problems via e-mail at bvhelp@broadvision.com. If you do so, be sure to include the case ID.

Support for third-party software products

To allow for complete testing, BroadVision certiﬁes BroadVision One-To-One products for the
versions of third-party products that are released and available sufﬁciently in advance of the
BroadVision software release date. This often means that third-party vendors release new versions
of their products prior to the next release of the BroadVision software. While BroadVision would
prefer that customers use the tested and certiﬁed software versions, we also understand that
customers occasionally want to use the newer versions of third-party products. As long as the
vendor guarantees forward compatibility, One-To-One products should also work on the newer
versions.

BroadVision usually tests and certiﬁes these new versions of third-party products in the next
product release. This can be a good indicator that the newer versions work with the previous
release. In exceptional cases BroadVision may determine that the newer version of a third-party
product cannot be used because it fails in some way during the testing cycle. In this case we
continue to certify the older version.

BroadVision supports customers who use newer versions of third-party products by working with
the customer to resolve compatibility problems with the third-party vendor. BroadVision also
considers, at our option, developing and releasing minor ﬁxes for our products to resolve problems
with new versions of third-party products.

License agreement

Use of the accompanying product is governed by the terms of your BroadVision license agreement,
which includes limits on the number of copies that may be installed and used. The packaging of this
product does not imply permission to use more copies than is permitted by your license agreement.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

3

System and software requirements

Installing and using the One-To-One Publishing Center requires:

l A Windows NT 4.0 server machine conﬁgured with the following:

• BroadVision One-To-One Enterprise Version 4.1.

• Microsoft Internet Information Server (IIS) version 4.0 or later.

• 30 MB of available disk space.

l A Windows 95 or Windows NT Workstation client machine conﬁgured with the following:

• Netscape Communicator version 4.5, or Microsoft Internet Explorer version 4.0 with Service

Pack 1 (version 4.72.3110.8), or Internet Explorer version 5.0. Note that Japanese client
machines require Netscape Communicator version 4.5 or Internet Explorer 5.0. Earlier
versions of these browsers are not supported.

• TCP/IP networking, or at least a 28.8 K BPS modem to run the application remotely.

• 750 KB of available disk space on the hard drive if you install the Java classes on each client
machine. See “Pre-loading instant publishing forms in the page request cache” on page 28
for instructions.

• A VGA monitor with a screen resolution of 800 x 600 or higher.

The One-To-One Publishing Center hardware requirements are the same as the BroadVision
One-To-One Enterprise hardware requirements, which are provided in the BroadVision One-To-One
version 4.1 for Windows NT Server Release Notes. Building One-To-One Web sites with content
managed in the One-To-One Publishing Center also requires the BroadVision One-To-One
Command Center application, which is included in version 4.1 of BroadVision One-To-One
Enterprise.

Documentation

The documentation is provided in HTML and PDF form on the CD-ROM in the $BV1TO1/pubs/
content directory. Due to a product name change in this release, the documentation titles for the
One-To-One Publishing Center have been changed as follows:

Prior document title

New document title

Content Management Center Installation and Release
Notes

One-To-One Publishing Center version 4.1.0 for NT
Installation and Release Notes

Content Management Center User’s Guide

One-To-One Publishing Center User’s Guide

Content Management Center Developer’s Guide

One-To-One Publishing Center Developer’s Guide

 See also “New product name” on page 6 for details about product name changes.

To display the PDF documentation on your browser, download the Adobe Acrobat Reader from the
Adobe site at http://www.adobe.com.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

4

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

 BroadVision periodically updates the electronic documentation and makes it available to
customers. If you are interested in being notified by e-mail when One-To-One Publishing
Center documentation updates become available, send an e-mail message to
bvpubs@broadvision.com, and enter subscribe contentv410docs in the subject field.
Notifications are sent to the reply address of the message.

Documents for One-To-One Publishing Center

The One-To-One Publishing Center User’s Guide is automatically installed along with the application.
Using the pubs ﬁle path, specify an HTML or PDF ﬁle location in your browser:

From the CD-ROM (assuming you are using drive E):

file:///E|/pubs/content/cmcug/contents.htm
file:///E|/pubs/content/cmcug/cmcug.pdf

From the hard drive:

$BV1TO1/pubs/content/usrguide/contents.htm
$BV1TO1/pubs/content/usrguide/cmcug.pdf

The One-To-One Publishing Center Developer’s Guide is automatically installed along with the
application, but is not accessible from One-To-One Publishing Center. Using the pubs ﬁle path,
specify an HTML or PDF ﬁle location in your browser:

From the CD-ROM (assuming you are using drive E):

file:///E|/pubs/content/cmcdg/contents.htm
file:///E|/pubs/content/cmcdg/cmcdev.pdf

From the hard drive:

$BV1TO1/pubs/content/devguide/contents.htm
$BV1TO1/pubs/content/devguide/cmcdev.pdf

Changes in version 4.1.0 Publishing Center

Version 4.1.0 of the One-To-One Publishing Center includes the changes from the prior version
described in this section.

l Support for One-To-One custom-deﬁned content types. One-To-One Publishing Center

developers can create content types speciﬁc to your site, use the BroadVision sample content
types, and customize the BroadVision sample types.

l Support for One-To-One content references in non-leaf categories. Prior versions permitted

content item references only in leaf categories. Version 4.1.0 permits content references in any
category or subcategory.

l Support for One-To-One related attributes that have multiple values. Database developers can
create new content attributes that have multiple values, and modify the BroadVision sample
attributes that have one value to include multiple values. Related attributes support, for
example, products that have related color and size attributes with multiple values for the colors

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

5

and sizes of content items. Related attributes also result in an attribute that normally has one
value having multiple values, such as attribute values in multiple languages rather than English
only.

l A Graphical User Interface (GUI) for workﬂow administration provides forms accessible from
the Admin menu command that service administrators use to create the workﬂow system for a
service. The One-To-One Publishing Center User’s Guide explains how to create workﬂow
systems.

l Workﬂow sets can have more than one initial workﬂow state.

l Instant Publisher (formerly Smart form) can include the Claim feature. See the One-To-One

Publishing Center Developer’s Guide for implementation instructions.

l New sample data based on the Broadway sample application delivered with One-To-One. You
can install the new Broadway-based One-To-One Publishing Center sample data when you
install the application.

l Components and scripts for Instant Publisher, Instant Find (formerly Smart ﬁnd), and preview.
The dynamic objects and page templates used in prior versions have been replaced with C++
components and JavaScript scripts. See the One-To-One Publishing Center Developer’s Guide for
implementation instructions.

l E-mail notiﬁcation alerts individuals and access group members of new content items in

personal and shared inboxes.

l Content items can be deleted from any One-To-One Publishing Center smart form or smart ﬁnd
designed to include this feature. See the One-To-One Publishing Center Developer’s Guide for
implementation instructions.

Changes from Version 3.0.0 One-To-One Publishing Center

The Version 4.1.0 One-To-One Publishing Center includes these changes from the prior version:

l Client-side Java classes are now automatically loaded during the ﬁrst use of the application. The
browser caches these classes, so application performance, especially on remote clients, may be
affected during the ﬁrst use only.

l Version 4.1.0 of the BroadVision One-To-One Enterprise now uses a site ID to generate an Object
ID (OID). The One-To-One Publishing Center Version 4.1.0 conforms to this standard, resulting
in a ten-digit OID upload ﬁle path rather than the nine-digit path used in prior versions.

l Access privilege inheritance among categories is now based on the greatest privilege granted to
any parent category. The greatest access privilege granted to any parent category that references
the item and is associated with the access group, is inherited by any subcategory to which an
access privilege has not been granted.

l Workﬂow sets are no longer associated with categories. A content item can potentially be set to
any workﬂow state in the workﬂow system for the service. The GUI used to select workﬂow
states when adding a new content item lets you select from all the initial states of all the deﬁned
workﬂow sets in the service.

l As part of creating the workﬂow system, the administrator is required to deﬁne the workﬂow
transition order of the states in each set. Deﬁning the transition order was optional in Version
3.0.0.

l Obsolete and unreferenced uploaded ﬁles are now deleted. In prior versions they were

archived.

l The One-To-One Publishing Center no longer supports the Incentives sample content type.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

6

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

Japanese translation of extended attributes

In this version of the One-To-One Publishing Center, the semantics and friendly names of the
required extended database attributes are translated into the Japanese language.

New product name

The BroadVision One-To-One suite of Internet applications have been re-named for version 4.1.0.
What was known as the Content Management Center in prior versions has been re-named the
One-To-One Publishing Center for version 4.1.0. In addition, Smart form has been re-named Instant
Publisher, and Smart ﬁnd has been re-named Instant Find.

Accordingly, the One-To-One Publishing Center document titles have been changed as follows:

Prior document title

New document title

Content Management Center Installation and Release
Notes

One-To-One Publishing Center version 4.1.0 for NT
Installation and Release Notes

Content Management Center User’s Guide

One-To-One Publishing Center User’s Guide

Content Management Center Developer’s Guide

One-To-One Publishing Center Developer’s Guide

Problems fixed in this release

Problems resolved in this release are listed below by the related BroadVision Quality Assurance
problem tracking numbers. If you contact BroadVision Technical Support regarding one of these
problems, be sure to quote the tracking number.

l 03042: Recreating group name — by assigning the name of a previously deleted group — causes

workﬂow problems and the workﬂow data ﬁles get out of sync.

l 03590: When making a query, choosing descending order and sort by “none” returns an empty

list of content items.

l 05069: The move-out date on the schedule does not include the colon separators between the

hours, minutes and seconds.

l 05284: When you complete the Add Content Item form, click the Save and Attach Files button,
complete the Attach Files form, then click the Attach button, the Add Content Item form does
not permit you to add another new item.

l 05354: Viewing a content item in a read-only Smart form template, then attempting to Preview

the item causes an error.

l 06855: Running the bvconf execute -a install_all command after installing the

One-To-One Publishing Center, then running the cstudio_setup script again can crash the
Interaction Manager.

l 07281: When running the One-To-One Publishing Center on a secure server, the Download link

does not work in the full forms.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

7

Problems in this release

This version of the One-To-One Publishing Center includes the following problems and issues. They
are listed by the related BroadVision Quality Assurance problem tracking numbers. If you contact
BroadVision Technical Support regarding one of these problems, be sure to quote the tracking
number. version 4.1.0 problems are classiﬁed as:

l “Browser-dependent and Java-related problems” on page 7.

l “Internationalization issues” on page 7.

l “Application problems” on page 7.

Browser-dependent and Java-related problems

l 03415: When you log into the One-To-One Publishing Center with Netscape Communicator

version 4.x running on Windows NT, the browser can hang and display the message starting
java... 96%. This is a Netscape or Windows NT problem, and occurs when loading Java, or
trying to open the Java Console. See http://help.netscape.com/kb/client/970805-
1.html and http://help.netscape.com/kb/client/981210-3.html for details.
Workaround: Check to see if the Matrox Millennium graphics driver is being used. If so, see if the
color depth is set to TrueVision, and reduce the color depth any amount. If that does not correct
the problem, get an updated version of the driver. For version 2.25 or later, contact the card
manufacturer.

l 04876: Using the Microsoft Internet Explorer 4.0 version 4.72.3110.8 incorrectly initializes the

inbox “Claim” button.

l 05403: Internet Explorer does not preserve the state of Java applets when you click the Back

button. Consequently, if you complete the ﬁelds in the Add or Modify Content Item full forms,
then click the Save button and get an error, when you go back to correct the error, the values you
entered in the applets are lost.

l 06653: In the Matching Attributes grid, selecting multiple rows using the Shift key does not

work when you have to scroll down to select rows.
Workaround: If you want to remove multiple rows, highlight and remove the visible rows ﬁrst,
scroll down and highlight and remove rows from those that are visible, and so on until you
have removed all the rows you need to.

Internationalization issues

l 06953: If you run a Full Find query using a criteria that is created with Japanese characters, due

to a Java problem, the query may fail to retrieve any content items.

l 07042: When entering monetary values in the Full Find, do not use thousands separators, and

always use the period as the decimal point.

Application problems

l 05051: Queries for Editorial text are not supported on the Microsoft SQL Server DBMS.

l 05098: If you open a content item from the Inbox or Full Find, preview the item, then click
Cancel in the Modify Content window, the Modify Content window becomes read-only.
Workaround: Go back to the Inbox or Full Find and re-open the content item.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

8

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

l 05681: Attaching a ﬁle using a non-existent path creates two zero-length ﬁles on the server.

l 06694: Previewing a content item that you are adding in the Add Content Item full form records
a One-To-One status message in the bvlog ﬁle informing you that the temporary preview item

## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
