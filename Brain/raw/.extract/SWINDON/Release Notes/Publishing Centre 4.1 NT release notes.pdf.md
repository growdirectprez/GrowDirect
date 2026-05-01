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
was successfully deleted.
Workaround: Ignore these messages.

l 06726: When adding a workﬂow state, ignore these errors messages in the bvlog ﬁle:

Error 3108: getting getStateId() and Error 3108: getting
getStateInfo()

l 07080: When adding a related attribute, a series of error messages may be incorrectly written to
the bvlog ﬁle. The add is successful, and you can ignore this series of messages. The series
begins with:

Reporting code: 13213, reason: Unknown content type.

l 07421: When adding new workﬂow states, do not use special characters in the workﬂow state

names.

l 07569: When you click the Find User menu command and list one or more users, and then

immediately click the List All Sets menu command, the Publishing Center lists the workﬂow
sets of a different service rather than the sets of the service you originally logged into. When
you click the Find User menu command and list one or more users, then immediately click the
Add Workﬂow Set command and add a workﬂow set, the Publishing Center adds the set to a
different service than you originally logged into.
Workaround: After using the Find User menu command, if you want to use the List All Sets or
Add Workﬂow Set commands, click any other Admin menu command ﬁrst before you click the
List All Sets or Add Workﬂow Set command.

Migrating from version 3.0.0 to version 4.1.0

Migration is performed automatically by the cstudio_setup script. Be sure to follow the
instructions in the “Installation and conﬁguration procedures” on page 13, which include backing
up your One-To-One site and database. The One-To-One Database Administrator’s Guide provides
backup instructions.

When migrating from version 3.0.0 to version 4.1.0 of the One-To-One Publishing Center, keep these
concepts in mind:

l If you have changed any of the One-To-One Publishing Center ﬁles in your template root or

document root directories, or if you are using version 3.0.0 sample Smart Form, Smart Find, or
Preview templates, back up your template root and document root directories before you run
the cstudio_setup script. When cstudio_setup prompts to conﬁrm overwriting the
scripts, images, and Java classes with the latest versions, answer Y. When the cstudio_setup
script is ﬁnished running, copy the templates and images from the back up to the template root
and document root directories.

l If you installed the version 3.0.0 Java classes on your client machines, delete those classes.

l If you are using version 3.0.0 Preview templates, you need to register them in the

bv1to1.conf ﬁle using the cmc_preview_templates parameter. Refer to the version 3.0.0
Content Management Center Installation and Release Notes for instructions on setting this
parameter. The Preview button in the full forms opens version 3.0.0 Preview templates. It does
not open version 4.1.0 Preview scripts. Note that the Preview button in Instant Publisher forms
opens version 4.1.0 Preview scripts.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

9

l The Instant Publisher button in the version 4.1.0 Publishing Center main menu displays Instant
Publisher scripts by default. To enable the button so that it displays version 3.0.0 Smart Form
templates as well, edit the /SCRIPT_ROOT/cstudio/scripts/publishing_forms.jsp
ﬁle to remove the comment delimiters so that the following code is no longer commented out:

// collectionID = matchingAgent.collectionID("Smart form targeting
//rules",
//                                           service, "TEMPLATE");
// if (!Error.set)
// {
//     //
//     // Run the matching rule
//     //
//     templateList = matchingAgent.matchContent(collectionID,
//service,
//                        "TEMPLATE", visitor, Session.sessionProfile,
//                        maxTemplates);
//     if (Error.set)
//     {
//         templateList = null;
//     }
// }

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

10

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

l The Instant Find button in the version 4.1.0 Publishing Center displays Instant Find scripts by
default. To enable the button so that it displays version 3.0.0 smart ﬁnd templates as well, edit
the /SCRIPT_ROOT/cstudio/scripts/query_forms.jsp ﬁle to remove the comment
delimiters so that the following code is no longer commented out:

// collectionID = matchingAgent.collectionID("Smart find targeting
//rules",
//                                          service, "TEMPLATE");
// if (!Error.set)
// {
//     //
//     // Run the matching rule
//     //
//     templateList = matchingAgent.matchContent(collectionID,
//service,
//                        "TEMPLATE", visitor, Session.sessionProfile,
//                        maxTemplates);
//     if (Error.set)
//     {
//         templateList = null;
//     }
// }

l After you run the cstudio_setup script, edit all version 3.0.0 Smart Form templates that use

One-To-One Publishing Center applets as follows:

If you run the One-To-One Publishing Center with Netscape on the client machines, and you are
using version 3.0.0 Smart Form templates, add this line inside the Smart Form template
<applet ...> tags:

archive="cmc410.zip"

If you run the One-To-One Publishing Center with Internet Explorer on the client machines, add
this line after the Smart Form template <applet ...> tags, before the applet close tags
</applet>:

<param name="cabbase" value="cmc410.cab">

The following is an example of a version 3.0.0 CategoryButton.class applet tag and
parameters:

<applet code=CategoryButton.class

codebase = "/webapps/cstudio"
name=CategoryButton
width=400
height=140
align=left>

<param name=... value=...>

...
</applet>

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

11

This example shows the CategoryButton.class applet edited for version 4.1.0 where the
One-To-One Publishing Center is run on client machines with Netscape and Internet Explorer:

<applet archive="cmc410.zip"
code=CategoryButton.class
codebase = "/webapps/cstudio"
name=CategoryButton
width=400
height=140
align=left>

<param name="cabbase" value="cmc410.cab">
<param name=... value=...>

...
</applet>

l The migration renames version 3.0.0 matching rule sets as follows:

Prior rule set name

New rule set name

Smart form matching rule set

Smart ﬁnd matching rule set

Instant publisher matching rule set

Instant ﬁnd matching rule set

l You need to update any references to the Smart form and Smart ﬁnd rule sets in your version

4.1.0 scripts.

l When you complete the migration tasks, be sure to refresh the browser caches on all the client

machines.

How cstudio_setup affects the file system and database

You run the cstudio_setup script as part of the application setup procedure described in
“Installation and conﬁguration procedures” on page 13. This section explains the effects of running
this script on the One-To-One database and ﬁle system.

In general, the cstudio_setup script performs the following:

l Extends the content schema to include the One-To-One Publishing Center attributes.

l Installs the One-To-One Publishing Center schema tables.

l Copies all scripts and templates to the script root and images to the document root.

l Sets up one service administrator.

l Installs the Java classes on the server.

l Adds a task to the NT Scheduling Service for the Schedule feature.

l Sets up the matching rule sets for the sample service.

l Loads the sample access groups, subtypes, and user accounts.

l Assigns Broadway sample content items to the sample users.

l Loads the sample workﬂow system.

l Designates which categories are sample destination categories for scheduling purposes.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

12

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

l Loads the sample Instant Publisher form, Instant Find form, and preview scripts.

 If you are installing the German version of One-To-One Publishing Center, modify the
$BV1TO1/bin/cp_install_purger and $BV1TO1/bin/cp_install_scheduler files to
change all instances of:

/every:M,T,W,Th,F,S,Su

to:

/every:Mo,Di,Mi,Do,Fr,Sa,So

Running the cstudio_setup script performs the following:

l Creates a directory called $BV1TO1_VAR/dbschema/tmp that contains the temporary ﬁles

used by the schema generator. You can delete this directory when cstudio_setup is ﬁnished
running.

l Extends the content database schema. The script adds columns with names that begin with the
CP_ preﬁx to the Products, Advertisements, Editorials, Discussion Groups, Templates, and
Scripts content type tables and to the BV_CATEGORY table. If you have service-speciﬁc schema
tables or custom content types, you need to manually extend them as directed in “Step 6:
Update the service-speciﬁc ﬁles and custom content types” on page 17.

l Creates 12 new database tables with names that begin with the BV_CP_ preﬁx. Adds a row to

the BV_SCHEMA_VERSIONS table that records the version number of the One-To-One
Publishing Center you are installing.

l Creates the following directories and copies ﬁles to them:

DOC_ROOT/cstudio
DOC_ROOT/webapps/cstudio

l Copies the publish.html ﬁle to the document root directory.

l Adds the cp_scheduler and cp_purge_temp_content utilities to the NT Scheduling

Service.

l Creates a .bvlog.conf ﬁle, if it does not exist, in $BV1TO1_VAR/etc, and modiﬁes

.bvlog.conf to turn on the logging of the One-To-One Publishing Center scheduler actions.
These actions are logged in the cmclog ﬁle.

l Creates the following directories and copies sample data ﬁles into them:

$BV1TO1_VAR/workflow
$BV1TO1_VAR/schedule
$BV1TO1_VAR/subtype

l Makes the following changes if you load the sample data:

• Creates these four rule sets in the Script content type for the MyBank sample service:

• Instant publisher matching rule set

• Instant ﬁnd matching rule set

• Product Preview matching rule set

• Editorial Preview matching rule set.

• Creates the following categories in the Script content type for the MyBank sample service:

• Instant Publisher

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

13

• Instant Find

• Preview

• Preview/Product

• Preview/Editorial

• Loads sample content items into the BV_SCRIPT table for the MyBank sample service,

which is the metadata for the sample Instant Publisher and Instant Find forms.

If you encounter errors when running cstudio_setup (for example, if cstudio_setup does
not complete the installation, if your database was rolled back to a previous state and your
$BV1TO1_VAR directory state does not match that database), perform the following cleanup
steps, then re-run cstudio_setup:

1. Remove the $BV1TO1_VAR/dbschema/cp_* ﬁles.

2. Connect to the database and run the following SQL command:

delete from BV_SCHEMA_VERSIONS where ACCESSOR_NAME =
"BV_CP_DB_ACCESSOR"

Installation and configuration procedures

This section provides the required installation and conﬁguration procedures for the One-To-One
Publishing Center. It also explains preliminary steps to take before you install and conﬁgure the
application. When you complete the required procedures, you can further conﬁgure the application
as described in “Optional application conﬁguration” on page 22.

 If you are running multiple machine configurations in which you are installing the
One-To-One Publishing Center when either the script root (/SCRIPT_ROOT) directory, the
document root (/DOC_ROOT) directory, or the $BV1TO1 directory is not accessible among
machines due to the presence of firewalls, go now to “Multiple machine installations” on
page 20 and follow the installation instructions in that section.

Installation and conﬁguration steps

Follow these steps in the listed order to complete the required One-To-One Publishing Center
installation, setup, and conﬁguration procedures:

l “Step 1: Get ready to install” on page 14.

l “Step 2: Install the One-To-One Publishing Center” on page 14.

l “Step 3: Conﬁgure the One-To-One Publishing Center” on page 15.

l “Step 5: Run cstudio_setup” on page 17.

l “Step 6: Update the service-speciﬁc ﬁles and custom content types” on page 17.

l “Step 7: Conﬁgure the attach ﬁles feature” on page 17.

l “Step 9: Start the application and log in as cmcadmin” on page 18.

l “Step 10: Create at least one access group” on page 18.

l “Step 11: Determine the destination categories for scheduling” on page 19.

l “Step 12: Create and target Instant Publisher and Instant Find content items” on page 19.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

14

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

l “Step 8: Edit the publish.html ﬁle” on page 18.

Step 1: Get ready to install

Before you install the One-To-One Publishing Center:

1. Install version 4.1 of BroadVision One-To-One Enterprise according to the instructions in the

One-To-One Installation and System Administration Guide.

To use the One-To-One Publishing Center sample data, which you can install during the
application installation, you must load the Broadway sample application before you install the
One-To-One Publishing Center.

2. If the One-To-One servers or Interaction Manager are running, shut them down now:

a. Log in as the same user who started One-To-One.

b. Shut down the One-To-One system:

$BV1TO1/bin/imgr_conf -a stop
$BV1TO1/bin/bvconf shutdown

3. If you have an existing One-To-One site, back up your One-To-One database and the

$BV1TO1_VAR directory. Installing the Publishing Center modiﬁes the One-To-One database
schema. If you have problems during the installation and need to uninstall the Publishing
Center, you can restore the database schema speciﬁcations from this backup. The One-To-One
Database Administrator’s Guide provides instructions for backing up your site and database.

4. Register in your Web browser all the MIME types you work with if you want to upload and

download ﬁles with the One-To-One Publishing Center. The browser Help provides
instructions.

5. Be sure that the bv1to1.conf ﬁle, which is the One-To-One system conﬁguration ﬁle, exists

and that you make a copy of it. During the Publishing Center installation, you modify
bv1to1.conf for the Publishing Center settings. As suggested in the One-To-One Installation
and System Administration Guide, keep the bv1to1.conf ﬁle under version control as you
would any source code.

• If the One-To-One system has been previously started, the bv1to1.conf ﬁle exists in

$BV1TO1_VAR/etc.

• Make a copy of the bv1to1.conf ﬁle now, before you modify it.

6. Have the following information on hand for running the cstudio_setup script:

• Your database password.

• The path to the document root directory of your HTTP server.

• The path to the script root directory of your Interaction Manager.

Step 2: Install the One-To-One Publishing Center

The One-To-One Publishing Center is installed using the setup.exe program. The installation
procedure in this section assumes that you are logged on to Windows NT as the owner of the
One-To-One application files. Although you use the Windows interface to run the setup.exe
program, you will also need MKS Korn shell windows (from MKS Toolkit) in which to run the
One-To-One Publishing Center scripts and utilities.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

15

To install the One-To-One Publishing Center:

1. Login as the owner (installer) of the One-To-One application ﬁles.

2. Run setup.exe from the /Windows/Content directory on the One-To-One Publishing

Center CD-ROM.

3. Follow the instructions on your screen to install One-To-One Publishing Center version 4.1.0.

4. The setup.exe script tells you when the installation is done.

5. Click the "Finish" button

The patch installer requests the following information:

a. your language

b. your company name

c.

the database you are connecting to (either MSSQL or Oracle).

After setup.exe installs several ﬁles, it asks you to read the text ﬁle accompanying the patch. The
ﬁle is located in:

$BV1TO1/bin/versions/cmc410-a-ns-aj.txt

Step 3: Conﬁgure the One-To-One Publishing Center

If a copy of the bv1to1.conf ﬁle exists on your system, you modify the contents of that ﬁle
according to the instructions in this step. If you just installed One-To-One Enterprise version 4.1 and
have never started it, the bv1to1.conf does not exist. In this case, before you can modify the ﬁle,
you need to copy the system example of it as follows:

mkdir $BV1TO1_VAR/etc
cp $BV1TO1/cstudio/examples/bv1to1.conf.example

$BV1TO1_VAR/etc/bv1to1.conf

Use an editor to modify the $BV1TO1_VAR/etc/bv1to1.conf ﬁle:

1. Search for the namepath deﬁnitions in the ﬁle (for example, cntdb_path) and add this line:

accessdb_path="PubCtr/AccessDB/accessdb" # access group db

2. Search for global processes in the ﬁle (for example, process cntdb) and add this line:

process pubdb {}                # instance of pubdb server

3. Add and set the enable_cmc_access_controls parameter for the One-To-One Publishing
Center. The parameter is set by default to a value of “1,” which turns on access control for the
One-To-One Publishing Center, Instant Publisher forms, and Instant Find scripts. Setting the
parameter to “0” turns off access control providing all users with unrestricted access. Add the
following line to the bv1to1.conf ﬁle and set the appropriate value:

enable_cmc_access_controls="1"

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

16

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

4. Add and set the HTTP document root directory parameter and path. The HTTP server looks for
static ﬁles in the directory deﬁned by this parameter. The document root directory is also the
parent directory of the cmc_upload directory, which contains attached ﬁles.

cmc_http_docroot="path_to_your_doc_root_directory"

If your site has multiple HTTP root directories for multiple servers, the One-To-One Publishing
Center can only see one of them. Changes made to that directory are not propagated to the
others.

5. Be sure that the bv_schedule_script_root directory as deﬁned in bv1to1.conf exists on

your system and contains a ﬁle named sched_header.jsp. If the Broadway sample
application has been installed, the ﬁle is already in the directory. If not, copy the ﬁle as follows:

cp $BV1TO1/lib/sched_header.jsp <value of bv_schedule_script_root>

6. When you ﬁnish modifying the bv1to1.conf ﬁle, shut down One-To-One, and then start it

again to install the One-To-One Publishing Center server.

a. Log in as the same user who started One-To-One.

b. Stop and start One-To-One:

$BV1TO1/bin/bvconf shutdown
$BV1TO1/bin/bvconf execute

If you are migrating and you have defined version 3.0.0 preview templates, follow the steps in
the version 3.0.0 Content Management Center Installation and Release Notes for setting the
cmc_preview_templates parameter in the bv1to1.conf file.

Step 4: Starting the NT Scheduling Service

The One-To-One Publishing Center background scheduler uses the NT Schedule Service to
periodically send users an alert when content is modiﬁed, and to periodically index the editorial
content for the Verity search engine. By default, the scheduler sends alerts and indexes the content
once per day, at midnight. To start the NT Schedule Service in automatic mode:

l From the Windows NT Start menu, choose

Settings | Control Panel | Services to open the Services dialog.

Scroll until you see the task schedule in the list of services, then double-click to open the Services
dialog.

l In the Services dialog, select Automatic Start Type.

l Click OK, then close the dialog.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

17

Step 5: Run cstudio_setup

When you are ready to run the cstudio_setup script, be sure that the One-To-One services are
running, and that the Interaction Manager is shut down.

If you are installing the German version of One-To-One Publishing Center, modify the
$BV1TO1/bin/cp_install_purger and $BV1TO1/bin/cp_install_scheduler files
before running the cstudio_setup script to change all instances of:

/every:M,T,W,Th,F,S,Su

to:

/every:Mo,Di,Mi,Do,Fr,Sa,So

To run the cstudio_setup script:

1. While logged in as the same user who started One-To-One, enter the following:

$BV1TO1/cstudio/cstudio_setup

2. Follow the instructions at the prompts.

3. When the script is ﬁnished running, start the Interaction Manager.

a. Log in as the same user who started One-To-One.

b. Start the Interaction Manager:

$BV1TO1/bin/imgr_conf -a start

Step 6: Update the service-speciﬁc ﬁles and custom content types

For instructions on extending a custom content type, see the One-To-One Publishing Center
Developer’s Guide. “Documentation” on page 3 explains how to access this on-line document.

Step 7: Conﬁgure the attach ﬁles feature

To use the attach ﬁles feature, you need to copy the upload.exe program to the /cgi-bin
directory. For example:

cp $BV1TO1/bin/upload.exe /<your http directory>/cgi-bin/upload.exe

Be sure the /cgi-bin directory is in the list of virtual directories for Microsoft IIS, and that the
upload.exe program is in the /cgi-bin directory.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

18

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

Step 8: Edit the publish.html ﬁle

If you are running the Interaction Manager with a named application, you may need to edit the
publish.html ﬁle (located in the /DOC_ROOT and /SCRIPT_ROOT/cstudio/templates
directories) to specify the gateway program that communicates with the Interaction Manager. To do
so, change the inetcgi.exe reference in the following line to a different reference.

This step may not be required for your site.

<META http-equiv="refresh" content="0;
URL=/cgi-bin/inetcgi.exe/cstudio/scripts/cp_init.jsp">

The installation loads the publish.html ﬁle into $BV1TO1/cstudio/templates/
publish.html, and the cstudio_setup script copies it to the HTTP document root directory. See
also “Running the Interaction Manager with a named application” on page 25.

Step 9: Start the application and log in as cmcadmin

After you run the installation and setup scripts, you can start your browser, log into the application,
and begin working with the administrative features.

The form used to open the application is /publish.html. The URL to open the application is
similar to the following where server_name is the name of your World Wide Web server:

http://server_name/publish.html

Establish the cmcadmin login account by entering the following information in the One-To-One
Publishing Center:

Login Name: cmcadmin
Password:
Service:

imcmcadmin
MyBank (for example)

As cmcadmin, you have access to all the interactive services created for the site, and any new
services that are added. Using the Admin menu commands, you can create access groups, set up
user accounts, and set up the workﬂow systems for these services. To view or create content items in
the One-To-One Publishing Center, you must be a member of an access group that grants you the
appropriate privileges. Refer to the One-To-One Publishing Center User’s Guide for instructions and
more information about administering a service. Click the Help command to access this document.

At some point, you need to create a One-To-One Publishing Center Service Administrator for each
service in your site. The service administrator creates and maintains user accounts, access groups,
and the workﬂow system for one service only.

Step 10: Create at least one access group

An existing access group is required before you can set up the workﬂow system. The One-To-One
Publishing Center User’s Guide provides more information about access groups.

To add an access group:

1. Click the Add Group command in the Admin menu to open the Add Access Group form.

2. Enter the group Name (required).

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

19

3. Enter an optional description.

4. Use the Choose Categories button to open the dialog where you select the content categories the

group members can access.

5. Determine the Category Permissions for the selected categories.

a. Scroll down to the Category Permissions section of the form.

b. In the ﬁeld next to each category name, open the list of access privileges and select one.

6. Click Add to save the access group.

Step 11: Determine the destination categories for scheduling

The One-To-One Publishing Center Schedule feature lets users re-categorize content items into and
out of destination categories at scheduled dates and times. Before this feature can be used, you need
to designate which categories are the destination categories for scheduling purposes. To do so, you
enter a value for the Scheduling Category attribute for each destination category.

You use the One-To-One Command Center application to enter category attribute values, including
values for the Scheduling Category attribute. Refer to the One-To-One Command Center User’s Guide
for information about entering category attribute values.

The default Scheduling Category value is “Is Not,” which means the category is not a destination
category that can be used to schedule the re-categorization of content items. The alternative value is
“Is,” which means that content items can be re-categorized into and out of the category according to
its schedule.

To designate that a category is a scheduling destination category:

1. Open the One-To-One Command Center.

2. Select the content type that contains the category. Selecting the content type displays its

category tree structure.

3. In the tree structure, locate and select the category.

4. Choose the Category|Properties menu command to open the Properties dialog for the selected

category.

5. Select the Scheduling tab in the Properties dialog.

6. In the Scheduling Category ﬁeld, open the drop-down list and choose “Is.”

7. Repeat Step 2 through Step 6 for each category that you want to designate as a destination

category for scheduling purposes.

Step 12: Create and target Instant Publisher and Instant Find content items

To use the Instant Publisher and Instant Find for a service, the Instant Publisher and Instant Find
scripts must exist as Script content items in your database. These items must also be targeted by
matching rules. You create the content items in the One-To-One Publishing Center as instructed in
the One-To-One Publishing Center User’s Guide. Use the One-To-One Command Center to create the
matching rule sets and rules that target the Instant Publisher and Instant Find content items. The
One-To-One Command Center User’s Guide explains how to create matching rule sets and rules.

Matching rule set and rule names are case sensitive.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

20

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

To use the Instant Publisher and Instant Find features in a service:

l Use the One-To-One Command Center to create a matching rule set for the Scripts content type.
Name the rule set Instant publisher matching rule set and create one or more rules
in this set. Typically, each rule targets a category in the Scripts content type that contains Instant
Publisher scripts.

l Use the One-To-One Command Center to create another matching rule set for the Scripts

content type named Instant find matching rule set. Create one or more matching
rules in this set. Typically, each rule in this set targets a category in the Scripts content type that
contains Instant Find scripts.

l Use the One-To-One Publishing Center to add one Script-type content item for each Instant

Publisher script to a category targeted by a rule in the Instant publisher matching rule set. Add
one Script-type content item for each Instant Find script to a category targeted by a rule in the
Instant ﬁnd matching rule set.

Multiple machine installations

A multiple machine installation is performed when either the script root directory, the document
root directory, or the $BV1TO1 directory is not accessible among machines.

Requirements

For multiple machine installations, the following requirements must be met:

l The $BV1TO1 directory path and contents must be identical on any machines running an

Interaction Manager or CORBA server; for example /opt/bv1to1.

l The IT daemon ports must be the same on any machines running an Interaction Manager or

CORBA server.

l You must copy $BV1TO1_VAR from the root host machine to the machines running the

Interaction Managers and CORBA servers.

l The $BV1TO1/bin directory on the root host must be identical to the $BV1TO1/bin directories

across machines.

l The $BV1TO1/lib directory on the root host must be identical to the $BV1TO1/lib directories

across machines.

Installation procedures

To perform multiple machine installations:.

1. Install version 4.1 of BroadVision One-To-One Enterprise on all machines, using the instructions
in the BroadVision One-To-One Enterprise Installation and System Administration Guide. This guide
also includes instructions for setting up One-To-One Enterprise in a multiple-site conﬁguration.
Be sure to set up and start the Web server as instructed in this guide.

2. Follow these steps on the root host machine:

• “Step 1: Get ready to install” on page 14.

• “Step 2: Install the One-To-One Publishing Center” on page 14.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

21

• “Step 3: Conﬁgure the One-To-One Publishing Center” on page 15.

• “Step 5: Run cstudio_setup” on page 17.

• “Step 6: Update the service-speciﬁc ﬁles and custom content types” on page 17.

3. Follow these steps on the machine running the Interaction Manager:

• Copy the contents of the script root directory from the root host to this machine.

• “Step 2: Install the One-To-One Publishing Center” on page 14.

• Start the Interaction Manager.

4. Follow these steps on the machine running the HTTP server:

• Copy the contents of the document root directory from the root host to this machine.

• “Step 7: Conﬁgure the attach ﬁles feature” on page 17.

• “Step 8: Edit the publish.html ﬁle” on page 18.

• Set up the Registry Editor for the HTTP server as described in “Supplemental

Documentation” in the BroadVision One-To-One Version 4.1 for Windows NT Server Release
Notes.

• Set up the bvsm.cfg ﬁle for the HTTP server as described in “Supplemental

Documentation” in the BroadVision One-To-One Version 4.1 for Windows NT Server Release
Notes.

At this point, be sure all the “Requirements” on page 20 are met.

5. Log into the One-To-One Publishing Center, and create your access groups as described in “Step

10: Create at least one access group” on page 18.

6. Mark the scheduling categories in the One-To-One Command Center as instructed in “Step 11:

Determine the destination categories for scheduling” on page 19.

7. Complete the procedure described in “Step 12: Create and target Instant Publisher and Instant

Find content items” on page 19.

Database and file system considerations

This information explains the important database and system administration considerations of
running the One-To-One Publishing Center application.

Database purge utility for temporary content items

The cp_purge_temp_content utility marks as deleted the temporary content items generated by
the Preview feature. Temporary content items marked as deleted still exist in the database but are
not visible to One-To-One Publishing Center, One-To-One Command Center, or other One-To-One
users.

It is important to regularly purge the One-To-One content database of the deleted content items. To
identify the deleted temporary content items generated by the One-To-One Publishing Center,
query each content type table for rows where the CP_IS_TEMPORARY attribute has a value of 1.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

22

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

One-To-One Publishing Center modiﬁcations to your ﬁle system

When the One-To-One Publishing Center runs, it modiﬁes the ﬁles and directories in your ﬁle
system.

If you use the attach ﬁles feature, which uploads client-side ﬁles to a server, the One-To-One
Publishing Center creates the /DOC_ROOT/cmc_upload directory and its subdirectories to store
the uploaded ﬁles. The One-To-One Publishing Center creates a unique directory path when ﬁles are
attached to a content item. For example, the ﬁles attached to a content item having an OID of 12345
are stored in the /DOC_ROOT/cmc_upload/0/000/012/345 directory.

Optional application configuration

After you have completed the required procedures described in “Installation and conﬁguration
procedures” on page 13, you can further conﬁgure the One-To-One Publishing Center application at
any time using the required conﬁguration procedures described in that section, or the optional
procedures described in this section.

Refer to the One-To-One Publishing Center Developer’s Guide for information on modifying the
sample configuration files.

You can modify the One-To-One Publishing Center conﬁguration data using the following optional
procedures:

l “Changing the size of the Matching Agent applet” on page 22.

l “Changing the default Inbox and Find display parameters” on page 23.

l “Running the Interaction Manager with a named application” on page 25.

l “Conﬁguring e-mail notiﬁcation” on page 25.

Changing the size of the Matching Agent applet

You can use this modiﬁcation to change the width of any of the columns in, or the overall size of, the
Matching Attributes grid.

1. Open the ﬁle named content_main.tmpl in /SCRIPT_ROOT/cstudio/templates.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

23

2. Search for the following lines. Unit measurements are in pixels.

<applet

archive="cmc410.zip"
code=Taxonomy.class
codebase="/webapps/cstudio"
name=Taxonomy
width=578
height=300 >
<param name="cabbase" value="cmc410.cab">
<param name=AttrNameLabel value="Attribute Name">
<param name=AttrFieldLabel value="Attribute Field">
<param name=RatingLabel value="Rating Name">
<param name=AttrNameWidth value="150">
<param name=AttrFieldWidth value="150">
<param name=RatingWidth value="150">
<param name=AddLabel value="Add">
<param name=RemoveLabel value="Remove">
<param name=AllStr value="All">

3. The widths of the Attribute Name, Attribute Field, and Rating Name columns can be adjusted
by setting the respective parameters, which are the AttrNameWidth, AttrFieldWidth, and
RatingWidth parameters.

4. After you change a column width, be sure the total width of the applet is adequate by setting

the width parameter. To adjust the height, set the height parameter.

5. Save the content_main.tmpl ﬁle.

6. If the Interaction Manager is running, purge the cache to make the changes effective:

$BV1TO1/bin/tmpl_mgr -p

Changing the default Inbox and Find display parameters

You can change the appearance of the Inbox and the Find features, and determine the maximum
number of items displayed in both. You do so by changing parameters in the inbox.tmpl and
find.tmpl ﬁles.

 Be sure to make a copy of these files before you edit them.

These ﬁles are located in the following directory where SCRIPT_ROOT represents the fully qualiﬁed
path to your Interaction Manager script:

/SCRIPT_ROOT/cstudio/templates

You can use either of these procedures to modify the inbox and Find display parameters.

l “Changing the maximum number of items displayed” on page 24.

l “Changing the column display” on page 24.

For additional information, refer to the One-To-One Publishing Center Developer’s Guide.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

24

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

Changing the maximum number of items displayed

To set the maximum number of items displayed in personal and shared inboxes, change the
maxItems parameter in the inbox.tmpl ﬁle. For example:

<param name=maxItems value=50>

To set the maximum number of items displayed in the Find Results tab, change the maxItems
parameter in the find.tmpl ﬁle. For example:

<param name=maxItems value=50>

If the Interaction Manager is running, purge the cache to make the changes to inbox.tmpl and
find.tmpl effective:

$BV1TO1/bin/tmpl_mgr -p

Changing the column display

To specify which columns are displayed, the order in which they are displayed, and the width of
each column in the display grid of the Inbox or Find Results features, change the following lines in
either the inbox.tmpl or find.tmpl ﬁle according to which feature you are modifying. field1
corresponds to width1, field2 to width2, and so on. field1/width1 speciﬁes that the NAME
column from the database is displayed ﬁrst at a width of 170 pixels, and the STATUS column is
displayed next at a width of 90 pixels, and so on.

<param name=field1 value="NAME">
<param name=field2 value="STATUS">
<param name=field3 value="CONTENT_TYPE">
<param name=field4 value="CP_DATE_ONLINE">
<param name=field5 value="CP_DATE_ASSIGNED">
<param name=field6 value="CP_ASSIGNED_BY">
<param name=field7 value="CP_ASSIGNED_TO">
<param name=field8 value="CP_WORKFLOW_STATE">

<param name=width1 value=170>
<param name=width2 value=90>
<param name=width3 value=140>
<param name=width4 value=140>
<param name=width5 value=160>
<param name=width6 value=160>
<param name=width7 value=120>
<param name=width8 value=120>

If the Interaction Manager is running, purge the cache to make the changes to inbox.tmpl and
find.tmpl effective:

$BV1TO1/bin/tmpl_mgr -p

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

25

Running the Interaction Manager with a named application

If you are running an Interaction Manager with a named application, you need to modify the
cgi-bin path in the following ﬁles:

DOC_ROOT/publish.html
SCRIPT_ROOT/cstudio/templates/publish.html

Refer to “Step 8: Edit the publish.html ﬁle” on page 18 and the One-To-One Installation and System
Administration Guide for additional information.

Conﬁguring e-mail notiﬁcation

When a content item is assigned to a user or access group, that user, or all users that are members of
the access group, can be alerted via e-mail. Follow this procedure to implement the e-mail
notiﬁcation feature. Keep in mind the following:

l Your One-To-One site does not send e-mail notiﬁcations to individuals or access group members

unless it is conﬁgured to do so.

l The default e-mail subject header and message body are deﬁned in the One-To-One Publishing

Center message catalog, providing locale-speciﬁc values for these parameters.

Failing to send e-mail is not an error, so problems incurred in the process do not appear in the
bvlog unless you are generating an extremely detailed log.

To conﬁgure e-mail notiﬁcation:

1. Conﬁgure these parameters in the bv1to1.conf ﬁle:

a. cmc_enable_new_content_message

This parameter determines whether an e-mail message is sent to individual users each time
a content item is assigned to them. The default value for this parameter is “0” which
suppresses e-mail notiﬁcation. Setting the value to “1” sends users a message when an item
is assigned to them. This parameter works in conjunction with, and supersedes, the
cmc_enable_new_group_content_message parameter.

cmc_enable_new_content_message="1"

b. cmc_enable_new_group_content_message

This parameter determines whether an e-mail message is sent to every member of an access
group each time a content item is assigned to the access group. Setting the value to “0”
suppresses e-mail notiﬁcation of access group members. Setting it to “1” sends the members
a message when an item is assigned to the access group. When the value of the
cmc_enable_new_content_message parameter is set to “0” the value of the
cmc_enable_new_group_content_message is ignored and the default value “0” is
used.

cmc_enable_new_group_content_message="1"

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

26

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

c. cmc_message_subject_header

This parameter sets the subject header of the e-mail message that is sent when a user is
assigned a content item. At run time, the expression $content_name$ is replaced by the
name of the content item. When the cmc_message_subject_header parameter is not
deﬁned, the system uses a default that is deﬁned in the system message ﬁle.

cmc_message_subject_header=’$content_name$: has been assigned to
you.’

d. cmc_message_body_file_path

This parameter sets the full path to the e-mail message body ﬁle that is sent when a user is
assigned a content item. At run time, the expression $content_name$ is replaced by the
name of the content item. When this parameter is not deﬁned, or the body ﬁle does not exist,
the system uses a default message body that is deﬁned in the system message ﬁle.

2. Be sure that e-mail addresses are registered for all users to be notiﬁed that a content item has
been assigned to them. Addresses must be registered for at least two users, and at least one of
them must have the Approve or Write access privilege to the category containing the content
they want to assign, enabling them to assign the items to other users. The One-To-One
Publishing Center does not send e-mail when the e-mail addresses of the sender and receiver
are not speciﬁed, and does not send a user e-mail when they assign a content item to
themselves.

If you have a proﬁle editor, register the e-mail address in each user’s proﬁle. If you do not have
a proﬁle editor, you can use SQL to register the e-mail addresses in your database, as in the
following example:

update BV_USER_PROFILE set EMAIL = ’yourname@yourcompany.com’
where USER_ID=your_user_id;

3. Shut down One-To-One, and then start it again.

a. Log in as the same user who started One-To-One.

b. Stop and start One-To-One:

$BV1TO1/bin/bvconf shutdown
$BV1TO1/bin/bvconf execute

Enabling the Find button for related content items

Using the Find button for related content items, One-To-One Publishing Center users can locate and
relate one content item to another. For example, if your product database includes a certain
television set, your content publishers can use the Find button for related content to locate and relate
that particular TV to an advertisement created for it.

To implement this feature, you add new related content ﬁelds to your content schema.

By default, One-To-One version 4.1 sample data is delivered with certain related content
implemented. For example, the Advertisement content type provides a related Product ID field
where you can select the product that is related to a particular advertisement.

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

27

To create a content attribute that displays the Find button for a related content item, you extend the
appropriate content database schema, such as the BV_PRODUCT table, using the schema generator.
Refer to the One-To-One Database Administrator’s Guide for instructions on using the schema
generator.

The attribute type for the new content attribute must be a derivation of the OID, and the LINK for
the type must be a content type name. For example, the type OID_PRODUCT in $BV1TO1_VAR/
dbschema/cnt_type.src is derived from the OID type, and its LINK is PRODUCT.

The following line from $BV1TO1_VAR/dbschema/adv_spec.src deﬁnes a content attribute
that relates products to advertisements:

ATTRIBUTE: PRODUCT_ID
TYPE: OID_PRODUCT
COLUMN: int
ATTR_KIND: REQ_ATTR
FRIENDLY_NAME: Product ID
SEMANTICS: Related Product Object ID

When you create new content attributes and extend the appropriate schema, the One-To-One
Publishing Center automatically displays new input text ﬁelds and Find related content buttons for
those attributes.

To display a new attribute for a content subtype, you need to modify the subtype using the
MODIFY_SUBTYPE command as described in the One-To-One Publishing Center Developer’s
Guide.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

28

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

Optimizing application performance

The following recommendations help you optimize One-To-One Publishing Center performance.

Pre-loading the caches for optimal performance

When the Interaction Manager is ﬁrst started, the One-To-One Publishing Center caches are empty.
The ﬁrst person to log into the One-To-One Publishing Center after the Interaction Manager is
started must wait while the caches are loaded. To prevent this person from waiting too long, pre-
load the One-To-One Publishing Center caches by running the cache_util utility as follows:

$BV1TO1/bin/cache_utl -e bvsn_cmc

For more information regarding the cache_util utility, refer to the One-To-One Enterprise
Installation and Administration Guide.

Pre-loading instant publishing forms in the page request cache

The Interaction Manager page request cache is designed to optimize the number of times a dynamic
Web page is generated for multiple requests. Refer to the One-To-One Enterprise Installation and
System Administration Guide for general guidelines on what can be put in the page request cache.
This topic points you to an example of how you can use the request page cache to optimize
One-To-One Publishing Center performance.

The $BV1TO1/cstudio/examples/cmc.req.example illustrates which Publishing Center ﬁles
can be put in the page request cache for performance improvement. This example designates three
instant publishing forms to be put in the cache. To put these forms in the cache, the rule (contentOID
is undeﬁned) must be true. When true, this rule speciﬁes that when a site visitor requests one of
these three forms to add a new content item, the blank forms are retrieved from the page request
cache.

Scheduling background processes

Rather than run the One-To-One Publishing Center background maintenance processes individually
at the command line each time, you can schedule the processes to run automatically as described in
this section.

Scheduling content program actions

The One-To-One Publishing Center provides the cp_scheduler utility that performs scheduled
actions on content items, such as making items on-line or re-categorizing them. By default, the
program is run hourly on the hour. When adding the program to the NT Schedule Service using the
at program, enter the following command:

sh $BV1TO1/bin/cp_scheduler $BV1TO1 $BV1TO1_VAR

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
System and software requirements

29

Purging temporary content items

The One-To-One Publishing Center Preview feature creates temporary content items. The
One-To-One Publishing Center cp_purge_temp_content utility marks these temporary items as
deleted in the database. By default, the program is run daily at midnight. You can change the
program run frequency in the NT Schedule Service. When adding the program to the NT Schedule
Service using the at program, enter the following command:

sh $BV1TO1/bin/cp_purge_temp_content $BV1TO1_VAR

Logging the scheduler actions

The One-To-One Publishing Center logs the scheduler actions in a ﬁle named $BV1TO1_VAR/
logs/<host>/cmclog.YYYYMMDD where YYYYMMDD is the current date, such as 19990601. You
can use a different log ﬁle, or turn off logging. Refer to the One-To-One Installation and System
Administration Guide for instructions.

The default value for blank date fields is the local time and date, which translates to 1/1/1901,
one second after midnight Universal Time. For instance, for Pacific Standard Time, this
translates to 12/31/1900 16:00:01. If you see this value in the log, it means that no date was
entered in the field. Note that this value is displayed in the One-To-One Command Center, but
not in the One-To-One Publishing Center.

Removing the One-To-One Publishing Center

To remove the One-To-One Publishing Center application ﬁles and directories and uninstall the
application, you need to know the following

l Document root directory for your HTTP server

l Script root directory for your Interaction Manager

Step 1: Remove the ﬁles and directories

To remove the One-To-One Publishing Center ﬁles and directories:

1. Log in as the same user who started One-To-One.

2. Shut down the One-To-One servers and the Interaction Manager:

$BV1TO1/bin/imgr_conf -a stop
$BV1TO1/bin/bvconf shutdown

3. Back up all the One-To-One ﬁles and directories.

4. Delete One-To-One Publishing Center ﬁles and directories from the server. Before removing
data ﬁles, refer to “How cstudio_setup affects the ﬁle system and database” on page 11 for
information about the ﬁles that were modiﬁed when the application was installed.

One-To-One Publishing Center Release Notes

690-410-NAS

BroadVision, Inc.

30

One-To-One Publishing Center™ Version 4.1.0 for NT Installation and Release Notes
BroadVision technical support

Step 2: Remove the conﬁguration settings

To remove the One-To-One Publishing Center conﬁguration settings, remove the settings added to
this ﬁle when the application was conﬁgured: $BV1TO1_VAR/etc/bv1to1.conf. Refer to “Step 3:
Conﬁgure the One-To-One Publishing Center” on page 15 for information about the parameters
added to this ﬁle during the application conﬁguration. Then, in the bv1to1.conf ﬁle, search for
each One-To-One Publishing Center parameter, and delete it or comment it out.

Step 3: Remove One-To-One Publishing Center programs from the Schedule Service

Use the at command from within in an MKS shell to remove all One-To-One Publishing Center
programs that were added to the NT Schedule Service.

Step 4: Uninstall the application

To remove the One-To-One Publishing Center software libraries:

1. From the Start menu, choose Settings | Control Panel | Add/Remove Programs.

2. On the Install/Uninstall tab, select “BroadVision One-To-One Publishing Center” from the list

of applications installed on your system.

3. Select Add/Remove, and follow the instructions on your screen.

Step 5: Delete BV_CP_DB_ACCESSOR from BV_SCHEMA_VERSIONS

Connect to the database and use SQL to delete BV_CP_DB_ACCESSOR from the
BV_SCHEMA_VERSIONS table. Use the following command:

delete from BV_SCHEMA_VERSIONS where ACCESSOR_NAME = "BV_CP_DB_ACCESSOR"

Step 6: Remove the database tables

Use SQL to manually drop all the tables with names that begin with BV_CP_.

Step 7: Restart One-To-One

Restart the One-To-One system:

$BV1TO1/bin/bvconf execute
$BV1TO1/bin/imgr_conf -a start

BroadVision, Inc.

690-410-NAS

One-To-One Publishing Center Release Notes

