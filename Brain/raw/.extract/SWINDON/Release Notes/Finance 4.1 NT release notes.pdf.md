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

$BV1TO1/finance/finance_setup

a. When the script asks you if you want to set up the application, press Return.

b. Press Return at the next prompt if you want to install the sample bank tables. If not, enter n

and press Return. Note that these sample tables are required to run the One-To-One
Financial sample application.

c. Press Return at the next prompt if you want to use the CheckFree integration. This is

required to run the sample application.

If you enter the default, the script prompts you for the following information:

• CheckFree DB Server

• CheckFree DB Database

• CheckFree DB Username

• CheckFree DB Password

d. Press Return at the next prompt if you want to load the sample CheckFree biller data.

e. When prompted for the location of the HTTP document root directory, enter the temporary

directory you identiﬁed in Step 7.

Enter path for http document root directory[/home/site/WWW/docs]::

The ﬁnance_setup script populates this directory with the One-To-One Financial scripts and
static ﬁles. Later you will copy these to the Interaction Manager script root and HTTP server
document root directories.

f. Answer “y” to the remaining prompts to set up the Fidelis sample application and install

sample data.

9. Stop the One-To-One servers by running:

$BV1TO1/bin/bvconf shutdown

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

8

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

Conﬁgure
One-To-One
Financial

To conﬁgure One-To-One Financial, you need to replace and modify the One-To-One Enterprise
conﬁguration ﬁle: $BV1TO1_VAR/etc/bv1to1.conf

10. Replace the default U.S. English configuration file with the one provided with One-To-One
Financial. If you are in a non-U.S. English locale, see the instructions in “Conﬁguring
One-To-One Financial” on page 13 for settings speciﬁc to your locale.

The sample is located in $BV1TO1/finance/setup. The one you need to overwrite is located
in $BV1TO1_VAR/etc/.

cd $BV1TO1/finance/setup
cp bv1to1.conf.finance.us $BV1TO1_VAR/etc/bv1to1.conf
cd $BV1TO1_VAR/etc

11. Change to the $BV1TO1/etc directory and edit the bv1to1.conf text ﬁle:

a. Deﬁne the CheckFree database parameters. These are separate from the BV_DB* database

parameters and must be deﬁned for the Fidelis sample application.

Change parameters that start with “fi_cf_db*” to point to the database you want to use
for the CheckFree plug-in. See the table under “Conﬁgurable parameters” on page 14” for
details about the parameters.

• Do not enter actual passwords in the bv1to1.conf ﬁle, even for test systems. The

bvconf utility prompts for these passwords and then encrypts them.

b. If your Interaction Manager host(s) is not on the root host machine, add hostmgr

parameter deﬁnitions for each machine. For example, if you are going to run Interaction
Manager servers on two machines named venus and mars, create two hostmgr deﬁnitions:

process hostmgr { parameter host="venus" }
process hostmgr { parameter host="mars" }

Each of these machines will need the same user account that you speciﬁed when you ﬁrst
started the One-To-One servers, per “Initialize One-To-One Enterprise” on page 6. When
you start the One-To-One servers, the bvconf utility will start Orbix servers on each of
these machines.

• One prompt asks for the account that One-To-One should use when starting the servers.

This Domain\Account identiﬁer must already exist on this Windows NT host, and should
have the access rights you deﬁned as described in the “Installing One-To-One on Windows
NT” section of the Installation and System Administration Guide.

c. Make any other site-speciﬁc changes. For example, if you are opting to change the site’s

service name, do that now.

d. Customize the bv1to1.conf ﬁle to include any other changes speciﬁc to your site.

12. Restart the One-To-One servers and execute the changes by running:

$BV1TO1/bin/bvconf execute

If you deﬁned hostmgr parameters for the Interaction Manager machines, you will be
prompted for the Domain\Account identiﬁer for each. However, you will also get error messages
at this time, because the One-To-One Enterprise software is not yet installed on those machines.

This completes the installation and One-To-One server conﬁguration.

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

9

Conﬁguring the Interaction Manager server

An Interaction Manager host is a machine that runs the Interaction Manager servers. A site may
have one or more of these hosts.

Root host

2

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

Conﬁguring One-To-One Financial to run on these machines is almost identical to the procedure
deﬁned in the Installation and System Administration Guide. Become familiar with the concepts
deﬁned in that manual before continuing with these steps.

To configure multiple Interaction Manager hosts, perform these steps on each machine.

Install One-To-One
and One-To-One
Financial

If the Interaction Manager host is the same as the root host, skip to Step 4. Otherwise, if the
Interaction Manager host is on a machine different from the root host:

1. Install the One-To-One and One-To-One Financial software on the Interaction Manager host per
the instructions in “Install One-To-One and One-To-One Financial on the root host” on page 6.
Speciﬁcally, follow the instructions from Step 1 through Step 5, and do not initialize the system.
Additionally:

a. The drive and directory path for $BV1TO1 must be the same as on the root host.

b. Each machine must have a user account to run the software. This must be the same as the

account used to start the One-To-One servers: a Domain\Account identiﬁer.

2. Replicate the $BV1TO1_VAR directory tree from root host to this machine. The drive and
directory path must be the same as on the root host. See “Conﬁguring multiple machine
installations” on page 16 for more steps.

3. Create the script root directory to contain the One-To-One scripts, then copy the ﬁles from the

temporary directory that the finance_setup script populated in Step e on page 7.

Conﬁgure the
Interaction
Manager

To conﬁgure the Interaction Manager:

4. Source the One-To-One shell settings. For example, in MKS:

. $BV1TO1_VAR/etc/bv1to1.conf.sh

5. Conﬁgure the Interaction Manager servers by running:

$BV1TO1/bin/imgr_conf -a configure

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

10

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

Answer the prompts as they appear; you can usually accept the default value. Additionally:

l The Fidelis scripts assume the existence of a default Interaction Manager, which uses the default

conﬁguration ﬁle: bvsm.cfg.

l For the gateway program name, use: /cgi-bin/inetcgi.exe. If you specify a different

program, change all the references in the sample HTML and page script ﬁles to the name of the
program you chose.

l For the default page to return to upon error, specify an HTML ﬁle. When an error occurs while

running One-To-One Financial, the visitor’s browser displays this page. BroadVision
recommends using $BV1TO1/finance/fidelis/scripts/error_page.jsp, which is
used by the Fidelis application error-handling functions. Copy this file to your script root
hierarchy.

l Reconﬁgure the startup scripts directory information to include the Fidelis startup scripts

directory. Add the startup script directory when prompted for changes to the startup-scripts
directories list.

The bold text in the following code segment shows the Fidelis startup script directory added to
the list of directories given at the prompt:

/bv1to1/script_library;/home/surf/login/bv1to1/lib/
script_library;/finance/fidelis/startup_scripts

You must enter the actual path of the scripts directory; do not use the environment variable in
the path. Also, the above entry is a single line; do not break the line.

6. Shutdown and restart the One-To-One servers to launch Orbix on the Interaction Manager host

machines:

$BV1TO1/bin/bvconf shutdown
$BV1TO1/bin/bvconf restart

7. Start the Interaction Manager by running:.

$BV1TO1/bin/imgr_conf -a start

Wait for the version message to appear, similar to this:

****bvsmgr/BV_SessionManager0 OneToOne version: 4.1.0****

See the One-To-One Installation and System Administration Guide for details.

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

11

Conﬁguring the HTTP server

An HTTP host is a machine that runs the HTTP servers. A site may have one or more of these hosts.
See the Installation and System Administration Guide for more information about these hosts.

Root host

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

The primary activity in conﬁguring the HTTP server is to setup the HTTP server to run the gateway
application, and to load the One-To-One Financial static ﬁles to that document root directory.

To configure multiple HTTP hosts, perform these steps on each machine.

Conﬁgure the
HTTP server

To conﬁgure the HTTP server

1. Follow the instructions in the Installation and System Administration Guide for “Conﬁguring the

gateway” in Chapter 4, “Setup”. Additionally:

• Do not copy the bvsm.cfg ﬁle per those instructions.

• Do not start the HTTP server.

2. Create the registry entries for One-To-One. These tell the gateway application where to ﬁnd the

conﬁguration ﬁle and where to write log ﬁles. Using the Windows NT regedit utility:

a. Pick the location where you want the bvsm.cfg conﬁguration ﬁle to be located, and create
that directory if it doesn’t already exist. For example, d:\BVSNsmgr\ is a good location.

b. Create this registry path:

\HKEY_LOCAL_MACHINE\SOFTWARE\BroadVision\

One-To-One Application System\4.1.0\Interaction Manager\
default\export\

If you are using a named application, replace “default” with the name, such as “appname”.

c. Create the BV1TO1_SESSION_CFG key, and enter the location you created above, such as

d:\BVSNsmgr\

d. Create the BVSNSMGR_LOGS key and enter the same location. (You may choose another

location.) This is where the gateway application writes it’s log ﬁles.

3. Copy the bvsm.cfg ﬁle from the Interaction Manager host to the location you identiﬁed in the

registry. On the Interaction Manager host, you can ﬁnd the ﬁle in
$BV1TO1_VAR/BVSNsmgr/hostname/bvsm.cfg

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

12

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Installing and configuring One-To-One Financial

4. Copy the gateway application from $BV1TO1/bin to the HTTP server’s executables location,

such as the location identiﬁed by /cgi-bin/.

5. Copy the static ﬁles from the temporary document root directory on the root host to the actual

document root directory on this machine.

6. Restart the HTTP server.

One-To-One Financial is now running. To test that it is running, load and run the Fidelis sample
application, as described next.

Running the Fidelis application

To run the Fidelis application:

1. Copy the login page for the Fidelis application to your HTTP server’s document root directory:

cp $BV1TO1/finance/fidelis/scripts/login_fidelis.html <doc-root>

Note that if you choose a gateway path different from /cgi-bin/inetcgi.exe, edit the
login_fidelis.html ﬁle and change the references from that gateway path to the one you
chose.

2. Visit the login_fidelis.html page, similar to this:

http://bvsn.com/login_fidelis.html

There are four sample users set up for the Fidelis application. For each user, the login name and the
password are the same:

l techstar

l settled

l goodlife

l student

For more information about the sample users and their proﬁles, see One-To-One Financial Overview.

Setting up customer care

To setup Customer Care, copy the Customer Care templates and static ﬁles to the Interaction
Manager’s script root directory, and to the HTTP server’s document root directory.

1. On Interaction Manager host(s):

mkdir <script-root>/finance
cp -R $BV1TO1/finance/templates <script-root>/finance

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Configuring One-To-One Financial

13

2. On HTTP server host(s):

mkdir <doc-root>/finance
cp -R $BV1TO1/finance/templates <doc-root>/finance
cp -R $BV1TO1/finance/images <doc-root>/finance

3. Test customer care by visiting the institution page, similar to this:

http://yourserver.com/finance/templates/institution/login.html

Configuring One-To-One Financial

One-To-One and One-To-One Financial maintain their conﬁguration information in the
$BV1TO1_VAR/etc/bv1to1.conf ﬁle. A sample One-To-One Financial conﬁguration for U.S.
English locales is located in $BV1TO1/finance/setup/bv1to1.conf.finance.us. This
section describes that ﬁle’s changes has compared to your default One-To-One bv1to1.conf ﬁle.

If you are running One-To-One Financial into a non-U.S. system, copy the One-To-One Financial-
speciﬁc sections into your bv1to1.conf ﬁle instead of using the example ﬁle as a starting point. If
you conﬁgured the bv1to1.conf ﬁle correctly for your country, the ﬁle has the correct locale
information in it already; the One-To-One Financial sample ﬁle is set up for U.S. systems only

One-To-One Financial changes

In the sample ﬁle, the One-To-One Financial-speciﬁc information is bracketed with these lines:

# FWA BEGIN -------------------------------------------------

and

# FWA END ---------------------------------------------------

CheckFree database parameters

The CheckFree database parameters are separate from the BV_DB* database parameters. This
arrangement allows you to use a separate database server, login, and password for CheckFree
data.You must set up these CheckFree parameters to use the sample application, Fidelis. To use the
bill pay functions in the sample application or to implement CheckFree, include and edit the
bv1to1.conf parameters that start with “ﬁ_cf_db” to point to the database you want the
CheckFree plug-in to use. See the table under “Conﬁgurable parameters” in the next section.

Do not enter an actual password in the bv1to1.conf file, even for test systems. The bvconf
utility prompts for these passwords and encrypts them. If you change the default value
$arg(bv_db_cf_passwd) for the CheckFree database password, for example, bvconf
execute does not run successfully.

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

14

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Configuring One-To-One Financial

Conﬁgurable parameters

The following bv1to1.conf parameters are conﬁgurable, although you may never need to change
all of them.

Parameter

bv_db_cf_passwd

ﬁ_balance_alert_plugin_lib

ﬁ_balance_alert_plugin_func

Description

Comments

CheckFree database
password

Set up during initial conﬁguration. Do not hard
code.

Name of library that
implements balance
alert plug-in

Change only if you implement alerts and change
the name of the library containing the balance
alert function.

Name of function
that implements
balance alert plug-in

Change only if you implement alerts and change
the name of the balance alert function.

ﬁ_delayedquote_maximumage Maximum age (in

ﬁ_srv_initial_connect_timeout

ﬁ_srv_initial_connect_retries

ﬁ_cf_dbuser

ﬁ_cf_dbpasswd

ﬁ_cf_dbhost

ﬁ_cf_dbname

process ﬁ_srv

seconds) for delayed
quote caches.

How long to wait for
a response before
trying a different
ﬁ_srv instance

How many server
instances to try
before giving up and
returning an error.

Database user for
CheckFree database

Database password
for CheckFree
database

Database server
name for CheckFree
database. Not
always the same as
the server’s host
name.

Name of CheckFree
database with
CheckFree database
host server

Financial Server
process

Default 120 seconds. See the chapter on alerts
and quotes in the One-To-One Financial
Developer’s Guide for more information.

Default 5000 milliseconds. See “Conﬁguring
multiple Financial Servers” on page 15” for more
information.

Default 5 times. See “Conﬁguring multiple
Financial Servers” on page 15 for more
information.

Can be the same as BV_DB_USER for the
sample application, but is generally different for a
production system.

Same as the value of bv_cf_dbpasswd. Do not
hard code.

Can be the same as BV_DB_SERVER for the
sample application but is generally different for a
production system.

This can be the same as BV_DB_DATABASE for
the sample application but is generally different
for a real installation.

To run multiple server instances, add additional
process ﬁ_srv blocks to bv1to1.conf. See
“Conﬁguring multiple Financial Servers,”
following, for more information about the ﬁ_srv
parameters.

The default ﬁ_srv conﬁguration includes a series
of class name parameters; these are set up for
the sample plug-in classes. For information
about these parameters, see the plug-in chapter
in the One-To-One Financial Developer’s Guide.

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Configuring One-To-One Financial

15

Parameter

Description

Comments

daemon quote_loader

Quote loader utility

The following shows how quote_loader is set in
bv1to1.conf.finance.us. This default
updates quotes for the BV_DELAYED_QUOTE
content type in the WebBank store.

daemon quote_loader {

parameter
storeName="WebBank"
contentType="BV_DELAYED_QUOTE"
newQueueLength="100"
maxQueueDelay="30"

}

For information on conﬁguring the quote loader
daemon, see the alerts and quotes chapter of
the One-To-One Financial Developer’s Guide.

Conﬁguring multiple Financial Servers

Like other One-To-One servers, the Financial Server (fi_srv) is a single-threaded process. While a
Financial Server is waiting for a response from a ﬁnancial institution, it cannot service any other
requests. If your site runs many simultaneous transactions, run multiple fi_srv processes.

To decide how many fi_srv processes to run, you need to experiment. Keep the following points
in mind:

l As the number of transactions a One-To-One Financial installation increases, the number of

fi_srv processes needed also increases.

l Batch or asynchronous mode backend transaction handlers respond to fi_srv requests faster

than real-time handlers.

l Running multiple fi_srv processes on a single-host machine may not result in an increase in

throughput. Run some processes on different machines by setting the optional host=
parameter to improve throughput.

For example, to run a Financial Server process on a host named “surf”, include the host name as
shown in the following lines:

process fi_srv {

parameter
host="surf"

...

Alternatively, you can use a single machine with multiple processors.

Note that you do not need to include the host name for a fi_srv process running on the same
machine as the One-To-One Financial installation.

How One-To-One assigns an ﬁ_srv process to a transaction

During the establishment of a new session, the component layer chooses an instance of fi_srv at
random. The component layer sends an “Are you alive?” message to a selected fi_srv instance. If
the selected instance does not respond quickly, two bv1to1.conf parameters specify what to do:

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

16

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Configuring multiple machine installations

l fi_srv_initial_connect_timeout speciﬁes how long to wait for a response before trying

a different fi_srv instance. The default is 5000 milliseconds.

fi_srv_initial_connect_timeout = "5000";

l fi_srv_initial_connect_retries speciﬁes how many fi_srv instances to try before

giving up and returning an error to the script. The default is ﬁve tries.

fi_srv_initial_connect_retries = "5";

If the ﬁrst fi_srv instance does not respond within the speciﬁed timeout, the component layer
sends an “Are you alive?” message to the next fi_srv instance in the sequence (for example, if
fi_srv instance 3 didn’t respond, the component layer tries fi_srv instance 4 next).

Set these parameters based on your optimistic appraisal of how you expect your site to perform. If
you are running a small number of Financial Servers, you may need to have a longer timeout period
to avoid having errors returned to the script. If your site repeatedly exceeds the conﬁgured number
of retries allowed, you need to do one of the following in bv1to1.conf:

l Increase the number of fi_srv processes.

l Increase the timeout period set in fi_srv_initial_connect_timeout.

l Increase the number of retries set in fi_srv_initial_connect_retries.

Session terms

The Fidelis application makes use of session terms to do targeting on account balances (see the
One-To-One Installation and System Administration Guide for information about session terms). In
order for this scheme to work correctly, it is necessary to deﬁne session terms in
$BV1TO1_VAR/etc/session_terms for every possible account type. For each account with type
T and subtype S, there should be a session term of type MONEY named “T_S”.

The information in the Product Proﬁle attribute and the information in the account balance session
terms is updated each time a user logs into Fidelis. This is done by the utility functions
fnProﬁleUpdateBalances() and fnProﬁleSetProductList() (in ﬁle
$BV1TO1/finance/fidelis/startup_scripts/fn_profile_utils.js).

Configuring multiple machine installations

The One-To-One, Interaction Manager, and One-To-One Financial servers are designed to run on
distributed hosts. All BroadVision servers communicate with each other via CORBA, and many of
them read ﬁles from and write ﬁles to common locations deﬁned by the $BV1TO1 and
$BV1TO1_VAR directories. If all of the hosts can access the common locations, such as with NFS on
UNIX or with UNC on Windows NT, you need do nothing special except possibly to deﬁne in the
bv1to1.conf ﬁle, the host machines and possibly identify the remote shell to use when accessing
those hosts [see Step 7 and Step 8 below for details].

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Configuring multiple machine installations

17

However, if the servers cannot access the same ﬁle locations, such as because of a ﬁrewall, you must
conﬁgure the system as follows:

On each host machine, log in with the same account, and that account must be the same one
that runs the One-To-One and Interaction Manager servers.

1. Install One-To-One in the same location — the $BV1TO1 directory — on each host machine,

such as d:/bv1to1/. The installation process populates this location with the One-To-One and
Interaction Manager executable ﬁles. This location must be the same on each host. See Chapter 2,
“Installation,” in the Installation and System Administration Guide for complete instructions.

2. Install One-To-One Financial in the $BV1TO1 directory on each host machine.

3. Set $IT_DAEMON_PORT to the same port number on each machine. The CORBA servers on

each machine use the same port number for communicating to the ORB.

4. Create identical $BV1TO1_VAR locations accessible to each host. This location is where the

servers get their conﬁguration information, and where the write observation and log ﬁle data.
This location must be the same on each host; for example, if it is d:/bv1to1_site/, it must be
that location on every host. Whenever you change the site conﬁguration, from the root host:

a. Copy the $BV1TO1_VAR/var/orb directory contents to each distributed host. This

directory contains the Orbix CORBA conﬁguration information.

b. Copy the $BV1TO1_VAR/etc/ directory contents to each distributed host. This directory

contains the site conﬁguration information.

c.

If you use the dump_taxon utility, copy the $BV1TO1_VAR/cache/taxon ﬁle to each
distributed host. This ﬁle is the category and matching attributes cache ﬁle that the
Interaction Manager can use for fast matching.

5. Make the log ﬁles directory accessible to all servers. Servers write observation and log message
data to the $BV1TO1_VAR/logs/hostName directory, where hostName is the name of the
server host machine. In a multiple-host conﬁguration environment, accessing $BV1TO1_VAR is
often inefﬁcient.

Instead, deﬁne $BVLOG_DIR in the bv1to1.conf ﬁle to identify the directory where servers
will write the ﬁles on the local host. Then, the ﬁles will be written to
$BVLOG_DIR/logs/hostName. The directory must exist on all host machines before starting the
servers on that machine.

• To aggregate observation data, the ﬁles from all hosts must ﬁrst be copied to a central

location. See the Database Administrator’s Guide for details.

6. Set the database environment variables on all machines running database accessor servers, and

the Interaction Manager servers. See “Database variables” in the Installation and System
Administration Guide for more information about setting these variables.

7. Deﬁne the hostmgr parameters in bv1to1.conf for each Interaction Manager host. When

you have Interaction Manager servers running on machines that do not also run a One-To-One
back-end server (which is usually the case for a medium or large production site), you need to
deﬁne hostmgr for each Interaction Manager host. This parameter tells the bvconf utility to
launch the CORBA server on the remote machine when bvconf starts the One-To-One servers.
See the description of the hostmgr parameter in the Installation and System Administration Guide
for details.

8. Set the BV_RSH_PATH parameter in bv1to1.conf if you need a different shell tool. The

bvconf utility uses a remote shell to execute commands on remote hosts, including Interaction
Manager hosts. However, for security reasons, some sites do not allow applications to run

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

18

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Removing One-To-One Financial

remote shells. If you have another utility that performs the remote shell functionality, you can
tell bvconf to use that utility with the BV_RSH_PATH parameter. See “Remote shell” in the
Installation and System Administration Guide for details.

9. Deﬁne the name for the One-To-One instance on all of the machines in the same instance; deﬁne

the name with the $BV1TO1_INSTANCE variable. This variable is created by the bvconf
execute command’s -i instance_name option, which adds it to the Shell start-up scripts in
the $BV1TO1_VAR/etc directory. Always “source” a start-up script before starting servers.

10. For each machine that will run the Interaction Manager, copy the contents of the script root

directory on the root host to the script root directory on the Interaction Manager machine.

This completes the instructions for conﬁguring multiple machine installations.

Removing One-To-One Financial

To remove One-To-One Financial Version 4.1.0:

1. Shut down the Interaction Manager and One-To-One servers by running the following

commands at the prompt:

imgr_conf -a stop
bvconf shutdown

1. Edit $BV1TO1_VAR/etc/bv1to1.conf by removing the sections that are surrounded by

these comments:

# FWA BEGIN -------------------------------------------------

and

# FWA END ---------------------------------------------------

2. Use Uninstall Shield from the Add-Remove Program Control Panel to uninstall One-To-One.

3. To put the conﬁguration changes you made to the bv1to1.conf ﬁle into effect, restart

One-To-One by running the following command at the prompt:

$BV1TO1/bin/bvconf execute

To reinitialize the One-To-One database tables, removing One-To-One Financial data, use the
install_all option:

$BV1TO1/bin/bvconf execute -a install_all

4. Restart the Interaction Manager by running the following command at the prompt:

$BV1TO1/bin/imgr_conf -a start

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Known problems and issues

19

Known problems and issues

l 06178: Downloading checking account statements in Fidelis gives a default name of

download_generator.jsp. The name of the download ﬁle should not be the same as the
name of the JavaScript script from which the download is generated.
Workaround: Type in an appropriate ﬁle name when saving from the browser.

l 06211: When you bring up a user in the “Edit Proﬁle” customer care page, there is a column of
padlocks along the right side of the screen. If you try clicking on one or more of the lock radio
buttons and then click on “Update Proﬁle”, you will notice unpredictable behavior. Sometimes
the changes you make to the state of the locks aren’t saved, and sometimes the lock buttons
change state unexpectedly when you update the user’s proﬁle.
Workaround: None

l 06805: Beginning and ending balances returned by the sample plug-in are relative to the set of

transactions retrieved for the speciﬁed time period. If no transactions are returned, the
beginning and ending balances are incorrectly displayed as $0.00.
Workaround: None

l 06986: The Fidelis application accepts past dates as the “start date” for scheduled bill-pay

sequences.
Workaround: None. See One-To-One Financial Developer’s Guide for a discussion of date-time
issues in One-To-One Financial.

l 07021:Bug 06066 (ﬁled against One-To-One Enterprise) indicates that ﬂoating point values are
always displayed using US-English formatting, regardless of what language an application is
set up to use. One-To-One Financial uses ﬂoating point values to represent stock prices (due to
the need for more than 2 decimal places). As a result, bug 6066 is visible to One-To-One
Financial customers in the Fidelis JavaScript pages where stock prices are displayed. The
formatting for user input of ﬂoating point values (such as the input of prices for stock alerts) is
affected by the same bug.
Workaround: None

l 07148: Authors of BV_FNBackendTransactionManager plugin objects are likely to assume that,

because the BV_FNBackendTransaction objects returned by the get_transaction() and
get_transactions() methods contain BV_FNBackendAccount objects, these calls must construct
complete BV_FNBackendAccount objects to specify the “from” and “to” accounts. This is not
the case. Although the API requires that transactions containing “from” or “to” accounts
represent such accounts by constructing BV_FNBackendAccount objects, implementors need
only set the "account_id" property. The ﬁnancial server will retrieve the additional account data
based on a cached copy of the account list obtained at login time (which is kept for the duration
of each session).

l 07221: The stock ticker applet does not work for Japanese language systems using the Internet
Explorer 4.0 browser. Internet Explorer 4.0 is missing two Java classes that would allow it to
display Japanese stock ticker information for Finance 4.1.0.

l 07711: If you include a “Money” type as part of inital_user_profile_attrs in

bv1to1.conf when running One-To-One Financial against an Oracle database, you will see an
error the ﬁrst time someone logs into the Fidelis application.
Workaround: The bv1to1.conf.finance.us ﬁle shipped with One-To-One Financial 4.1.0
does not contain FN_ASSETS in the initial_user_profile_attrs parameter. If you add
proﬁle attributes of your own to the initial_user_proﬁle_attrs variable, do not include any that
are of money type. For more information about this parameter, refer to the Installation and
System Administration Guide.

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

20

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Supplemental information

l 08824: The One-To-One Financial Developers Guide incorrectly states that the Interaction Manager

session ID can be used as the input value to the sessionID parameter of
BVI_FNFIRep::creator(). This is not true; use BVI_Session::sessionKey instead.

Additionally, the One-To-One Financial Developers Guide incorrectly states that
BV_FN_TRANSACTION.BV_SESSION_ID is varchar(32); actually, it is a varchar(256)

l 08861: The debug conﬁgurations of the One-To-One Financial sample projects do not use the

debug version of Microsoft C++ runtime libraries. Attempting to use those libraries might cause
the compile to fail, or the application to crash. Some of the compiler options that requires those
libraries include /MDd, /MLd, /MTd, and /D_DEBUG. For information this issue, see the Iona
knowledge base article at:
http://www.iona.com/online/support/kb/Orbix_C++/articles/226.27.html

l 08903: In non-English conﬁgurations that use Microsoft SQL Server, the

initial_user_profile_attrs in the bv1to1.conf conﬁguration ﬁle does not accept
DATE-type columns, such as LAST_LOGIN_DATE.

Supplemental information

The following topics were not included in the documentation.

Using Fidelis stock ticker applet with Internet Explorer 5

Running the Fidelis stock ticker applet requires the Java Virtual Machine (Java VM), which is not
automatically included when a user downloads Internet Explorer 5. When a person running
Internet Explorer 5 visits a Web site containing a Java applet, the browser automatically asks if the
person wants to download the Java VM. Sites that plan to use the stock ticker must notify their
customers that they need the Java VM to use the ticker.

JavaScript best practices in One-to-One Financial

Extensive testing at BroadVision has shown that to have a site run at an acceptable speed, any single
page on the site must be generated within 500 milliseconds of a request for it. Times exceeding that
rate tend to slow the performance of the servers that deliver the pages.

The development goal in tuning the Fidelis sample application for Version 4.1.0 of One-To-One
Financial was to provide examples of meeting this 500 millisecond goal (excluding delays in calling
the One-To-One Financial Server and backend plug-ins to legacy systems, which don’t directly
impact overall system throughput). You can then use these pages as good examples of best practice
in coding your own application pages.

BroadVision test data included, for a given user, 25 accounts and 50 pending payments, thus
providing a fairly typical case for a visiting customer.

In the majority of cases Fidelis pages meet this 500 millisecond goal easily. However, three pages are
still above the limit due to the complexity of the operations on those pages. The Fidelis developers
chose, however, to leave the pages as is because they demonstrate useful system functionality. In
developing your own applications, however, you should carefully consider how much of the
functionality on these pages you wish to use. The pages and operations described in this section are
covered in more detail in One-To-One Financial Developer’s Guide.

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

Fidelis login page

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Supplemental information

21

In BroadVision testing (on a Sun ULTRA 5 workstation) this page usually takes about 600
milliseconds. This time is used primarily in three areas of the page script.

Expensive operations:

l Initialization of the alert constants in fnInitAlertConstants so that the number of pending alerts

can be displayed on the home page. Alerts are expensive, so there are a large number of
constants to be initialized here.

l Fetching the BVI_Visitor object and updating its LAST_LOGIN_DATE so that the last login date
can be displayed in the upper right corner of the home page. Updating the proﬁle also requires
fetching the BroadVision account the visitor belongs to and the visitor’s proﬁle, and then
writing the new LAST_LOGIN_DATE back to the proﬁle. Fetching and storing proﬁle
information requires database reads and writes, which are inherently expensive.

l Updating the user’s account list to the visitor proﬁle to make it possible to include

personalization based on this information on the home page. The personalization is shown in
the ads displayed at the top.

Possible solutions:

l Delaying the display of the number of pending alerts until the visitor switches to the Alerts

page allows you to delay initializing the alerts information.

l While retrieving the BVI_Visitor object is needed in any case, choosing not to display or set the
LAST_LOGIN_DATE here would speed things up. Perhaps it could be moved to the main
display page (see next section, “Home page”).

l Choosing to display only ﬁxed ads on this page and do targeted ads elsewhere is a strategy

used in several sites.

This page is by nature quite expensive if you want to show a lot of information when the user ﬁrst
logs in. BroadVision developers calculated a page generation time of about 560 milliseconds in the
test conﬁguration. Several of the expensive areas here are tied to the login page.

Expensive operations:

l Retrieving and displaying the count of pending alerts.

l Retrieving targeted content for display. Currently the home page performs for targeting

operations—for personal messages, extra messages, ads, and ﬁnancial tips. Each of these is
fetched each time the visitor returns to the home page, which is even more expensive than the
login page because it happens several times.

l Formatting the account summary table. With a large number of accounts, this is easily the most

expensive part of the page.

l Displaying the stock ticker.

Possible solutions:

l If possible, remove the count of pending alerts. Or, have the visitor go to the alert page to check

on alerts.

l Cut down or eliminate some of the targeted information on the home page and display it

elsewhere.

Home page

One-To-One Financial Release Notes

790-410-NAS

BroadVision, Inc.

22

One-To-One Financial Version 4.1.0 for Windows NT Release Notes
Supplemental information

l BroadVision “solved” the display of the account summary table by using a new component

introduced in Version 4.1.0 ( BVI_Formatter) to speed up generation of text related to display of
tabular information. While the syntax of the format string is not easy to read (it’s a single long
string of HTML), the component reduced table-generation time to anywhere from 20 to 5 per
cent of its original value.

l The stock ticker display could be moved to a page devoted entirely to stocks.

Bill pay main page

This page came in just over the 500 millisecond limit, at 505. There are three types of information
displayed—pending payments, in-process payments, and account balances.

Expensive operations:

l Formatting the tables for each of these types of information is by far the most expensive part of
the operation—the original timing for the canonical case was over 2 seconds per page before
using the BVI_Formatter component.

Possible solutions:

l This page is almost at the bare minimum of processing for a page of its type—it fetches two
types of bill information and the accounts, and uses the BVI_Formatter to display their data.
One possible improvement, however, would be to remove the display of accounts from this
page and leave only the payment displays. This would put the page below the 500 millisecond
limit, but application usability might decrease.

General best practice principles

This section is just a quick reminder of several principles of best practice in using components and
JavaScript to generate pages.

1. Minimize the amount of JavaScript code executed to generate a given page—100 lines or fewer

work best.

2. Minimize page complexity as much as possible. Having less to do is faster and also leads to a

cleaner page design.

3. As much as possible, reduce the time needed to display the login page. This is the ﬁrst page

everyone sees, and if it’s too slow, they may not even enter your site.

4. Reduce the number of calls from JavaScript into C++. This includes such standard

programming “tricks” as using temporary variables to hold results rather than recomputing
them several times by calling component attributes.

5. Delay doing something until you absolutely have to. In Fidelis, if there is no need to display

alerts on the main page, there is no need to initialize alert information while on that page—wait
until the page where you actually do display alerts.

BroadVision, Inc.

790-410-NAS

One-To-One Financial Release Notes

