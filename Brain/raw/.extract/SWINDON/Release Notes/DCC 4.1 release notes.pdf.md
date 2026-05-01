1

One-To-One Command Center™
Version 4.1 Installation and Release

Notes

These release notes accompany the Version 4.1 release of the BroadVision® One-To-One Command
Center™. This version of the Command Center runs on Version 4.1 of BroadVision® One-To-One ™
Enterprise.

 These release notes provide the accurate, most current installation and configuration
instructions for the One-To-One Command Center Version 4.1.

The release is delivered on a CD-ROM that contains:

l The BroadVision One-To-One Command Center application and all other components of the

One-To-One application system.

l The printed and on-line versions of the One-To-One Command Center User’s Guide, which is the

documentation for this application. “Documentation” on page 2 explains how to access the on-
line versions from the CD-ROM.

Contents

These release notes cover the following information:

l “BroadVision Technical Support” on page 1.

l “License agreement” on page 2.

l “Documentation” on page 2.

l “New features and enhancements” on page 3.

l “Installing the One-To-One Command Center” on page 4.

l “Logging in as the Command Center administrator” on page 6.

l “Securing the administrator account” on page 8.

l “Working with services” on page 8.

l “Version 4.0 problems resolved in this release” on page 9.

l “Problems in the Version 4.1 Command Center” on page 9.

BroadVision Technical Support

Technical Support services are provided on an annual basis to BroadVision customers. A standard
90-day warranty is also provided with all software.

If you experience problems using BroadVision software products, contact the BroadVision World-
wide Customer Support Organization for assistance. Registered customers who have login names
and passwords can report problems via the BroadVision Web site at www.broadvision.com.

One-To-One Command Center TM  Release Notes

390-410-WAS

BroadVision, Inc.

2

One-To-One Command Center™ Version 4.1 Installation and Release Notes

On the Web site, you can use the Problem Reports pages to access support-related technical
information, report problems, and track report status and responses. Telephone contact information
for BroadVision Customer Support is also provided on the site. Contact your BroadVision Account
Representative to request a login name and password.

The Web site is the preferred method of reporting problems. When necessary, you can also report
problems via e-mail at bvhelp@broadvision.com. If you do so, be sure to include the case ID.

Support for Third-Party Software Products

To allow for complete testing, BroadVision certiﬁes BroadVision® One-To-One™ products for the
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
which includes limits on the number of copies that may be installed and used. To simplify the
installation and use of this product, One-To-One is packaged with all available components on each
CD. This packaging does not imply permission to use more copies of the components than is
permitted by your license agreement.

Documentation

The One-To-One Command Center documentation is delivered in print and electronically in the
HTML format and the Portable Document Format (PDF).

 The installation and configuration instructions in the Version 4.1 One-To-One Command Center
User’s Guide are not the most current. Use the installation and configuration instructions
provided in these release notes.

The documentation for this release includes:

l These release notes in print format only. They provide the most current installation and

conﬁguration instructions.

l A printed copy of the Version 4.1 One-To-One Command Center User’s Guide.

l HTML and PDF copies of the Version 4.1 One-To-One Command Center User’s Guide. You can
access the electronic documentation directly from the CD, or from the One-To-One system
directory. In your browser, enter the URL that points to the welcome.htm ﬁle.

BroadVision, Inc.

390-410-WAS

One-To-One Command Center TM  Release Notes

One-To-One Command Center™ Version 4.1 Installation and Release Notes
New features and enhancements

3

• If the One-To-One CD is your target on Solaris, enter a path similar to this:

file:/cdrom/cdrom0/pubs/onetoone/welcome.htm

• If you’re using a Windows system to view the CD and your CD-ROM drive is E, use a path

similar to this:

file:///E|/pubs/onetoone/welcome.htm

• To access the installed HTML ﬁles in the One-To-One system directory, enter the full path to

the welcome ﬁle, for example:

file:/opt/bv1to1/pubs/onetoone/welcome.htm

You can also link the tree from the CD to the document root directory of your HTML server.

 BroadVision periodically updates the electronic documentation, and makes it available to
customers. If you’re interested in being notified by e-mail when documentation updates
become available, send an e-mail message to bvpubs@broadvision.com, and enter subscribe
ccv41docs in the subject field. Notifications are sent to the reply address of the message.

New features and enhancements

The Version 4.1 Command Center offers these new features and enhancements.

New product name

All the BroadVision® One-To-One™ Enterprise products have been re-named for Version 4.1. What
was known as the One-To-One Dynamic Command Center in prior versions has been re-named the
One-To-One Command Center for Version 4.1.

The text in the One-To-One Command Center User’s Guide reﬂects the product name change. The
graphics do not.

Internationalization and localization

Version 4.1 of the Command Center supports the English and Japanese character sets and
languages. The level of support BroadVision provides for these character sets and languages
includes:

l Full end-to-end character set support.

l Support for local currency symbols, date and time formats, and number formatting.

l Translation of the One-To-One Command Center and its documentation.

l Translation of the Command Center Graphical User Interface and the database friendly names.

One-To-One Command Center TM  Release Notes

390-410-WAS

BroadVision, Inc.

4

One-To-One Command Center™ Version 4.1 Installation and Release Notes
Installing the One-To-One Command Center

Installing the One-To-One Command Center

This section provides installation pre-requisites and describes how to install and conﬁgure the
Command Center. Be sure to install the Command Center on each PC that connects to a One-To-One
interactive service.

The One-To-One Command Center installation and conﬁguration instructions include these topics:

l “System and software requirements” on page 4.”

l “Before you install” on page 4.”

l “Installing the Command Center” on page 5.”

l “Installing the data access objects” on page 5.”

l “Installing COMCTL32.dll” on page 5.”

l “Downloading the euro font updates” on page 5.”

System and software requirements

Installing and using the Command Center requires:

l A PC running Windows 95 or Windows NT Version 4.0 Service Pack 3.

l TCP/IP networking.

l 15-20 megabytes of available disk space on the hard drive.

l 32 megabytes of RAM.

l A VGA monitor with a screen resolution of 800 x 600 or higher, and a color depth of at least 16

bits (65, 536 colors).

Before you install

Before you install the Command Center:

l Verify that BroadVision One-To-One Enterprise is installed and initialized on your network.

The version number of the installed One-To-One system must match the version number of the
Command Center you’re about to install.

l Check with your system administrator to learn whether DNS is enabled. It is recommended that
DNS be enabled. If it isn’t, you must specify the name of the One-To-One Root Host machine in
the Windows Host ﬁle. Your system administrator can give you this name.

l Ask your system administrator for your company Internet domain name. Be aware that this is

not the same as a Windows NT domain.

l Ask your system administrator for the name of the One-To-One Root Host server that the

Command Center communicates with, and its IT_DAEMON_PORT number.

l If you want to keep a different version of the Command Center on your computer when you
install this version, you must install this version in a unique directory. The installation process
automatically installs this version in a unique default directory unless you select a different one.

 Do not install this version of the Command Center in the same directory as a prior version.

BroadVision, Inc.

390-410-WAS

One-To-One Command Center TM  Release Notes

One-To-One Command Center™ Version 4.1 Installation and Release Notes
Installing the One-To-One Command Center

5

Installing the Command Center

To install the Command Center:

1. From the One-To-One CD in your CD-ROM drive, or from the One-To-One software on your

network, run setup.exe from the Windows\Dcc directory.

2. Follow the instructions on your screen.

 It’s recommended that you install the Command Center in the default directory, especially if
you keep a prior version of the application on your computer.

Installing the data access objects

To use the Command Center Import feature, the data access objects must be installed on the
computer that’s running the application. The Import feature is designed to copy information into
the One-To-One database through the Command Center using the Microsoft Data Access Objects.
Refer to Appendix C, “Importing data” in the One-To-One Command Center User’s Guide for more
information about this feature.

 You must install the Microsoft Data Access Objects to enable the Import menu commands in
the One-To-One Command Center. The Import menu commands are always disabled when the
data access objects are not installed.

To install the data access objects:

1. From the One-To-One CD in your CD-ROM drive, or from the One-To-One software on your

network, run setup.exe from the Windows\Dcc\Dao\Disk1 directory.

2. Follow the instructions on your screen.

Installing COMCTL32.dll

Installation of the COMCTL32.dll ﬁle is required for BroadVision Y2K compliance, and to use the
latest versions of the Windows common controls. If Internet Explorer 4.01 Service Pack 1 has been
installed on your machine, this ﬁle has also been installed, and you don’t need to re-install it. If this
ﬁle hasn’t been installed on your machine, you can install it as follows:

From the One-To-One CD in your CD-ROM drive, or from the One-To-One software on your
network, run 401comupd.exe from the Windows\Dcc directory.

See also problem number 07255 in “Problems in the Version 4.1 Command Center” on page 9.

Downloading the euro font updates

To display the euro symbol in the Command Center graphical user interface, you need to download
the euro support for Windows NT or Windows 95 as described in the Microsoft Euro Currency
Resource Center Web page at:

http://www.microsoft.com/euro/

See also problem number 07256 in “Problems in the Version 4.1 Command Center” on page 9.

One-To-One Command Center TM  Release Notes

390-410-WAS

BroadVision, Inc.

6

One-To-One Command Center™ Version 4.1 Installation and Release Notes
Logging in as the Command Center administrator

Logging in as the Command Center administrator

To initially conﬁgure the Command Center, you need to log into the application and interactive
service using the Command Center administrator account. The administrator account is a special
Command Center account with administrator permissions. This topic assumes that the application
has been installed according to the instructions in “Installing the One-To-One Command Center” on
page 4.

Starting the Command Center

To start the Command Center, choose Programs|BroadVision|Command Center 4.1 from the
Windows Start menu. The ﬁrst time you start the application, it displays the Options dialog where
you conﬁgure the host and port connection. The host is the One-To-One Root Host server that the
Command Center communicates with. To conﬁgure the host, you need the name and Orbix daemon
port number of the One-To-One Root Host server.

Conﬁguring the One-To-One Root Host server and port connections

You initially conﬁgure the host and port connection in the Options dialog, which is automatically
displayed the ﬁrst time you start the Command Center. Later, you can use this dialog to modify this
connection, create connections to other servers, and delete server connections. To open the Options
dialog in the future, select the Tools|Options menu command.

To conﬁgure the host and port connections that communicate with the Command Center:

1. Enter the name assigned to the One-To-One Root Host server by your system administrator.

2. Enter the Orbix daemon Port for that host server.

3. Enter a Description for the connection. Example descriptions are “Staging” for a server where

your site development takes place, and “Production” for a server where you create the
information that’s actually displayed on your site.

4. Click Add to enter the host and port connection to the list.

5. Repeat Step 1 through Step 4 for each host and port connection you want to add.

6. When you ﬁnish adding host connections, click OK.

• If this is the only host and port connection you’ve conﬁgured, clicking OK closes the dialog

and opens the login window.

• If you’re adding a new host and port connection, clicking OK closes the dialog.

Modifying a host connection

To modify a One-To-One Root Host and port connection:

1. Choose Tools|Options to open the Options dialog with the Connection tab displayed.

2. From the list of connections, select the one to modify.

3. Make the necessary changes to the Description, Host, and Port.

4. Click Modify, and then click OK when you ﬁnish.

BroadVision, Inc.

390-410-WAS

One-To-One Command Center TM  Release Notes

One-To-One Command Center™ Version 4.1 Installation and Release Notes
Logging in as the Command Center administrator

7

Deleting a host connection

To delete a One-To-One Root Host and port connection:

1. Choose File|Options to open the Options dialog with the Connection tab displayed.

2. From the list of connections, select the one to delete.

3. Click Delete, and then click OK when you ﬁnish.

Setting the Connection Retries

The Connection Retries option on the Connections tab of the Options dialog determines the total
length of time that the Command Center attempts to connect to the host server when you log in.
How quickly the Command Center succeeds depends on factors such as the speed of your network
and servers.

After you click the Login button, a bar displays the login progress. Setting the Connection Retries to
a higher number gives the Command Center more time to connect to the server. Lower numbers
give the application less time to try to connect. It’s recommended that you set the Connection
Retries to 15, and then change the setting as required.

Logging in as administrator

If you’re logging in for the ﬁrst time, after you conﬁgure the host and port connection, clicking OK
in the Options dialog opens the login window. After the ﬁrst login, starting the application displays
the login window. The information that you type in the login window is case sensitive.

To log in:

1. Click Refresh Services, and select the Service that you want to work with.

2. In the User Name ﬁeld, enter dccadmin.

3. In the Password ﬁeld, enter imdccadmin.

4. Click Login.

 If it takes a long time to connect to the host server, you may need to increase the Connection
Retries number on the Connection tab in the Options window. To open this window, select
Tools|Options. Refer to “Setting the Connection Retries” on page 7 for instructions.

5. After you log in with this user name and password, you need to change the administrator user

name and password so that others can’t log in as the administrator. Go to “Securing the
administrator account” on page 8 for instructions.

One-To-One Command Center TM  Release Notes

390-410-WAS

BroadVision, Inc.

8

One-To-One Command Center™ Version 4.1 Installation and Release Notes
Securing the administrator account

Securing the administrator account

Use the Modify User dialog for the Command Center administrator account to change the user
name and password for the service you’re logged into. To change the administrator user name and
password for a different service, exit the current service, and log into a that one.

 Your password is case sensitive.

To open the Modify User dialog, select the Users module in the Tools group. Choose the
User|Modify menu command to open the Name and Password tab of the dialog.

To update the administrator account:

1. Enter your User Name.

2. Enter your New Password.

3. Verify the new password by entering it again in the Repeat Password ﬁeld.

4. Click OK.

Working with services

Your Command Center administration work, such as creating accounts, applies to one interactive
service—the service you select when you log in. If you administer more than one service, you can
change to a different service, update the list of services with current information, and exit a service
without closing the Command Center.

Changing to a different service

To change the interactive service after logging into the Command Center:

1. Choose File|Exit Service to leave the currently selected service and open the login window.

2. From the list of Services, select the one that you want to work with.

3. Type your Password.

4. Click Login.

Refreshing the list of services

The Refresh Services button updates the list of available services for any recently added services.
When new interactive services have been added to the site, click this button to display the current
list of the available services before you select one during login.

Exiting a Service

To exit a service and leave the Command Center application open, select the File|Exit Service menu
command.

BroadVision, Inc.

390-410-WAS

One-To-One Command Center TM  Release Notes

One-To-One Command Center™ Version 4.1 Installation and Release Notes
Version 4.0 problems resolved in this release

9

Exiting the Command Center

Exiting the Command Center closes the service and the application with one action, unless you close
the service before you exit. There are two ways to exit the Command Center:

l Select the File|Exit menu command.

l Click the close button in the upper right corner of the desktop.

What’s next?

After you install the application:

l Review the “Version 4.0 problems resolved in this release” on page 9 and the “Problems in the

Version 4.1 Command Center” on page 9.

l Go to Appendix B, “Administering the Command Center” in the One-To-One Command Center

User’s Guide. This appendix explains how to set up user accounts, assign user permissions, and
conﬁgure the One-To-One Command Center.

Version 4.0 problems resolved in this release

Problems in the Version 4.1 Command Center resolved in this release are listed below by the related
BroadVision Quality Assurance problem tracking numbers. If you contact BroadVision Technical
Support regarding one of these problems, be sure to quote the problem tracking number.

l 05851: When the Command Center runs on a server with the Japanese language, it can now

determine the maximum number of characters allowed in a ﬁeld.

l 05887: The Command Center does not let you modify the key ﬁeld values in external tables.

This is the correct behavior for the application.

l 05994, 5997: The Edit|Replace menu command now works correctly for monetary values,

numbers with decimal points, and integers.

l 06047: Double-clicking the column separator of a hidden column always correctly displays the
column, except in the Advertisements sample content type. See problem number 07474 in
“Problems in the Version 4.1 Command Center” on page 9.

Problems in the Version 4.1 Command Center

Problems in the Version 4.1 Command Center are listed by the related BroadVision Quality
Assurance problem tracking numbers. If you contact BroadVision Technical Support regarding one
of these problems, be sure to quote the problem tracking number.

l 04927: When you modify items in the Properties dialogs and the items have related attributes,
modifying both the regular and related attributes in the same work session results in an error
message.
Work Around: Modify the regular attributes, close the Properties dialog, re-open the dialog, and
then modify the related attributes, or vice versa.

l 06023: If you’re working in the Command Center and see this message: The category cannot be

found in the database, someone has deleted the category you’re trying to work with since you last
refreshed your category view. To continue your work, close the message, and choose the
Category|Refresh All menu command.

One-To-One Command Center TM  Release Notes

390-410-WAS

BroadVision, Inc.

10

One-To-One Command Center™ Version 4.1 Installation and Release Notes
Problems in the Version 4.1 Command Center

l 06078: The One-To-One Command Center installation fails at 81% if the wininet.dll ﬁle is

not installed on the computer.
Work Around: Before installing the Command Center, install the wininet.dll ﬁle by installing
Microsoft Internet Explorer Version 3.0 or a later version. You can also call BroadVision
Technical Support to obtain a copy of this ﬁle. Refer to “BroadVision Technical Support” on
page 1 for contact information.

l 06448: When using an external database as the content source for a matching rule, the rule

action cannot query that database to retrieve content.

l 07255: The One-To-One Command Center Version 4.1 is built using the Microsoft Visual C++

Version 6.0 Service Pack 2. The minimum requirements of the operating system are:

• Windows NT 4.0 requires Windows NT 4.0 Service Pack 3, or Windows NT 4.0 Service

Pack 4 when available, and the hot ﬁxes located at:

http://backoffice.microsoft.com/downtrial/moreinfo/y2kfixes.asp

• The updated comctl32.dll, which can be downloaded from:

http://www.microsoft.com/msdownload/ieplatform/ie/comctrl.asp

For more information about Y2K compliance of the operating system on which you run the
Command Center, see:

http://www.microsoft.com/technet/year2k/product/user_view59286EN.htm

l 07256: To display the euro currency symbol in the Command Center graphical user interface,

you must install the euro currency support for Windows NT or Windows 95, according to which
operating system you use.

l 07474: In the Advertisements sample content type, double-clicking the column separator of a

hidden column does not re-display the hidden column.
Work Around: Select the Window|Close menu command, and then re-open the module.

BroadVision, Inc.

390-410-WAS

One-To-One Command Center TM  Release Notes

