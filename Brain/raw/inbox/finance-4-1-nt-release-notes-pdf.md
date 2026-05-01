---
date: 2026-04-24
type: raw
source: Brain/raw/.extract/SWINDON/Release Notes/Finance 4.1 NT release notes.pdf.md
tags: [retail, pwc, swindon, sap-retail, broadvision, coe, 1999]
project: retail
status: unprocessed
---

# Finance 4.1 NT release notes.pdf

## Source
File: `Brain/raw/.extract/SWINDON/Release Notes/Finance 4.1 NT release notes.pdf.md`
Size: 59,259 bytes

## Raw content
1

One-To-One Financial

Version 4.1.0 for Windows NT

Release Notes

This is Version 4.1.0 of the BroadVision® One-To-One™ Financial application for the Windows NT
platform. These release notes include information about the following topics:

l “BroadVision Technical Support,” described next.

l “License agreement” on page 2.

l “Documentation” on page 2.

l “System and software requirements” on page 3.

l “Installing and conﬁguring One-To-One Financial” on page 4.

l “Conﬁguring multiple machine installations” on page 16.

l “Removing One-To-One Financial” on page 18.

l “Known problems and issues” on page 19.

l “Supplemental information” on page 20.

BroadVision Technical Support

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

Software updates

Before you install any software, check the BroadVision Web site, www.broadvision.com, for any
patches you may need to install with One-To-One Enterprise or One-To-One Financial.

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

2

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
License agreement

Support for third-party software products

To allow for complete testing, BroadVision certiﬁes BroadVision One-To-OneTM products against
the versions of third-party products that are released and available sufﬁciently in advance of the
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

License agreement

Use of the accompanying product is governed by the terms of your BroadVision license agreement,
which includes limits on the number of copies that may be installed and used. The packaging of this
product does not imply permission to use more copies than are permitted by your license
agreement.

Documentation

Because One-To-One Financial extends BroadVision One-To-One Enterprise functionality, you need
to refer to the One-To-One documentation. In addition, the documentation speciﬁc to this release
includes:

l One-To-One Financial Overview in HTML and PDF format that is installed during the application

installation. This document includes the following topics:

• A high-level overview of One-To-One Financial.

• An overview of the Fidelis sample application, with an emphasis on targeted content.

l One-To-One Financial Developer’s Guide in HTML and PDF format that is installed during the

application installation. This document includes the following topics:

• An overview of One-To-One Financial, with an emphasis on topics of interest to developers.

• The Fidelis sample application.

• Functions written for the Fidelis sample application.

• One-To-One Financial JavaScript components.

• One-To-One Financial C++ interfaces for backend plug-in development.

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
System and software requirements

3

l These release notes.

From time to time BroadVision updates the electronic documentation and makes it available to
customers. If you are interested in receiving a notification when updates are available, please
send an e-mail message to bvpubs@broadvision.com, and put
“subscribe financev410docs” in the subject field. Notifications will be sent to the reply-
address of the message.

To use the One-To-One Financial HTML documentation, start your browser and enter the URL that
points to the contents.htm ﬁle for the document.

l If you are reading the documentation from the CD-ROM:

file:///E|/pubs/finance/directory_name/contents.htm

directory_name is either devguide or overview.

l If you are reading the ﬁles from the directory where the install program places them:

file:/$BV1TO1/pubs/finance/directory_name/contents.htm

Where $BV1TO1 corresponds to the value of the $BV1TO1 environment variable and
directory_name is either devguide or overview.

There are also PDF (Portable Document Format) versions of the manuals, FinDev.pdf and
FinOver.pdf, each located in the same directory as the document’s HTML ﬁles. To access the PDF
ﬁles, you will need a PDF viewer, such as Adobe’s Acrobat Reader, which is available for free
downloading from Adobe’s Web site at:

http://www.adobe.com/prodindex/acrobat/readstep.html

Additional BroadVision documents and white papers are available at:

http://www.broadvision.com

System and software requirements

These requirements are the same as those for Version 4.1 of BroadVision One-To-One Enterprise. See
the Server Release Notes and Installation and System Administration Guide for details.

If you plan to do backend or CheckFree backend plug-in development, you must purchase a
RogueWave Tools.h++ developer’s license. This is true whether or not you plan to use the
sample plug-ins, because One-To-One Financial exposes a RogueWave data structure in the
C++ plug-in interface.

If you plan to build either the sample or CheckFree plug-in implementations that are provided
for the Fidelis application, you must also purchase a license for DBTools.h++. For more
information see the One-To-One Financial Developer’s Guide.

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

4

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

Installing and configuring One-To-One Financial

Here are the general steps for installing and conﬁguring One-To-One Financial. Detailed
instructions appear in the sections — beginning with “Install One-To-One and One-To-One
Financial on the root host” on page 6 — following this list:

Pre-install

1. Check the BroadVision Web site, www.broadvision.com, for any patches you may need to

install for or with this software.

2. Determine which gateway and path your site will use, such as /cgi-bin/inetcgi.exe,

which is what the Fidelis sample application looks for. If you are not sure, read the information
about “Conﬁguring the gateway” in the Installation and System Administration Guide. You will
need to know this before you conﬁgure the Interaction Manager servers.

3. Decide how many host machines you need, for example, for a simple development system, you

can use one host, but for a production system, you should separate hosts each for the
One-To-One servers, Interaction Manager servers, and HTTP server. These instructions assume
that you are installing a production conﬁguration.

1

Root host

2

Interaction
Manager host

3

HTTP host

Install One-To-One
Install One-To-One Financial
Start default servers
Create temporary script root
Setup One-To-One Financial
Configure for One-To-One Financial
Start One-To-One servers

Install One-To-One
Install One-To-One Financial
Replicate $BV1TO1_VAR
Copy script root
Source environment
Configure Interaction Manager
Start Interaction Manager

Create registry
Copy bvsm.cfg
Copy gateway application
Copy document root
Configure HTTP server
Start HTTP server

• Make a note of the Interaction Manager host machine name, or names if you will be using
more than one. you will need these names when you conﬁgure the One-To-One servers.

• The root host and Interaction Manager machines will need a user account that One-To-One
will use. This Domain\Account identiﬁer must already exist on this Windows NT host,
and should have the access rights you deﬁned as described in the “Installing One-To-One
on Windows NT” section of the Installation and System Administration Guide.

For detailed information about conﬁgurations, see the One-To-One Enterprise Installation and
System Administration Guide.

Root host steps

The root host is the machine that runs the One-To-One Enterprise and One-To-One Financial
servers. The instructions for installing and conﬁguring it are described in “Install One-To-One and
One-To-One Financial on the root host” on page 6. In brief, on that machine:

4. Install One-To-One Enterprise and One-To-One Financial.

5. Start the One-To-One servers and initialize the conﬁguration by running:

bvconf execute -a install_all

6. If the Interaction Manager host is different from the root host or HTTP host, create a temporary

directory for the One-To-One Financial scripts and HTTP server document root.

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

5

7. Initialize the One-To-One Financial environment by running: finance_setup

8. Stop the One-To-One servers by running: bvconf shutdown

9. Overwrite (replace) the $BV1TO1_VAR/etc/bv1to1.conf conﬁguration ﬁle with the one

provided with One-To-One Financial: bv1to1.conf.finance.us

10. Customize the bv1to1.conf ﬁle to include your site’s conﬁguration.

11. Restart the One-To-One servers and read the change by running: bvconf execute

Interaction
Manager host
steps

An Interaction Manager host is a machine that runs the Interaction Manager servers. A site may
have one or more of these hosts. To conﬁgure them, follow the instructions in “Conﬁguring the
Interaction Manager server” on page 9.

In brief, on the Interaction Manager host machine, if the Interaction Manager host is the same as the
root host, skip to Step 12. Otherwise, if it is on a different machine:

a. Install One-To-One Enterprise and One-To-One Financial. The drive and directory path for

$BV1TO1 must be the same as on the root host.

b. Replicate the $BV1TO1_VAR directory tree from root host to this machine. The drive and
directory path must be the same as on the root host. See “Conﬁguring multiple machine
installations” on page 16 for more steps.

c. Copy temporary script root from root host to this machine

12. Source the One-To-One shell settings. For example, in an MKS shell: . bv1to1.conf.sh

13. Conﬁgure the Interaction Manager servers by running: imgr_conf -a configure

HTTP host steps

If the HTTP host is the same as the Interaction Manager host, skip to step Step 14. Otherwise, if it is
on a different machine:

a. Create the registry entries for One-To-One.

b. Copy the bvsm.cfg ﬁle from the Interaction Manager host to this one

c. Copy the gateway application to the HTTP server’s executables location.

d. Copy temporary document root from root host to this machine

14. Conﬁgure the HTTP server to use the gateway application.

15. Restart the HTTP server.

Post-conﬁguration
activities

One-To-One Financial is now installed and conﬁgured. To verify the installation:

16. Test the conﬁguration by “Running the Fidelis application” on page 12.

17. Test the Customer care system by “Setting up customer care” on page 12.

The following sections describe these activities in detail.

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

6

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

Install One-To-One and One-To-One Financial on the root host

The root host is the machine that runs the One-To-One Enterprise and One-To-One Financial
servers.

1

Root host

Interaction
Manager host

HTTP host

Install One-To-One
Install One-To-One Financial
Start default servers
Create temporary script root
Setup One-To-One Financial
Configure for One-To-One Financial
Start One-To-One servers

Install One-To-One
Install One-To-One Financial
Replicate $BV1TO1_VAR
Copy script root
Source environment
Configure Interaction Manager
Start Interaction Manager

Create registry
Copy bvsm.cfg
Copy gateway application
Copy document root
Configure HTTP server
Start HTTP server

To install on that machine:

Install One-To-One
Enterprise

1.

Install One-To-One Enterprise Version 4.1 by following the instructions in the Version 4.1
Installation and System Administration Guide.

• Set the environment variables per the instructions in the Installation and System

Administration Guide.

• Do not conﬁgure or start the One-To-One servers at this time.

• Do not conﬁgure or start the Interaction Manager servers at this time.

Install One-To-One
Financial

2. Log in with an “administrator” account. The account that you use to install and run One-To-One
must have “administrator” privileges, and must have the right to “Log on as a Service”. This
right is granted with the Windows NT User Manager tool. This is the account that the
One-To-One servers use.

3.

Install One-To-One Financial. Run the Setup program from the Windows directory on the CD.

\windows\setup.exe

A message will inform you that One-To-One Enterprise Patch “F” is being installed, if your site
does not already have the BroadVision software patch.

4. Select the database management system that your site is using.

5. Confirm the installation conﬁguration.

Initialize
One-To-One
Enterprise

6.

Initialize the One-To-One Enterprise servers by running, in an MKS shell:

$BV1TO1/bin/bvconf execute -a install_all

While bvconf is running, it will prompt you to enter the passwords necessary to access your
database management system. You might see other prompts as bvconf conﬁgures and starts
the system, answer them as necessary; most have default answers, or prompts that you can
answer “Yes” to without a problem. Additionally:

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

7

• One prompt asks for the account that One-To-One should use when starting the servers.

This Domain\Account identiﬁer must already exist on this Windows NT host, and should
have the access rights you deﬁned as described in the “Installing One-To-One on Windows
NT” section of the Installation and System Administration Guide.

• Other prompts will ask you for passwords, possibly for the Domain\Account or database
password. One-To-One will remember these passwords for future use with these accounts.

• SQL Server users will see a prompt asking if you want the database log truncated after the
installation. Conﬁrming that prompt will truncate the logs to free up log space. Do this if
you are short of log space in your environment.

The One-To-One Enterprise servers should now be running on this machine. If the system does not
start correctly, refer to the Installation and System Administration Guide. Often a problem at this point
occurs because

• the environment variables are not set correctly, or

• the servers cannot connect to the database.

Setup
One-To-One
Financial

7. Create a temporary directory accessible from the root host to contain the One-To-One Financial
application scripts and static ﬁles. Later, you will copy the ﬁles to the Interaction Manager and
HTTP hosts.

8.

Initialize the One-To-One Financial environment by running:


## Key takeaways
<!-- Session fills these in during processing -->

## Links to existing knowledge
<!-- What wiki articles or project docs does this connect to? -->
